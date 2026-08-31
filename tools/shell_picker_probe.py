#!/usr/bin/env python3
"""THE APP'S FIGHTER PICKER, ASSERTED. School, then fighter.

    python shell_picker_probe.py

Rick, 2026-08-30: *"can we reorganize the dropdown menus for the fighters? im
thinking 2 separate menus. one to chose school and then a second one to chose
the fighter from within that school."*

WHY THIS FILE EXISTS AT ALL. `app/ui/` had no test of any kind, and the change
it now carries has a failure mode with no error attached to it:

    EVERY RELIC STAYS IN THE FIGHTER SELECT AND THE SCHOOL MENU ONLY HIDES
    THEM. `$('selA').value = 'thornshear'` has to keep working from anywhere —
    Random sets it, the short pipeline reads it, `displayName()` reads it. If
    the fighter list were REBUILT per school instead, an assignment would
    silently do nothing whenever the wrong school happened to be showing, and
    the first symptom would be a short rendered on the wrong relic.

That is this project's own defect class — wrong and right producing the same
absence of complaint — so it gets a check rather than a paragraph.

HOW IT AVOIDS BEING A SECOND COPY OF THE SHELL. The real shell cannot be
opened outside Electron: its CSP is `self swb:`, `window.swb` is the preload
bridge, and the roster comes out of the game iframe. So this builds a harness
AT RUN TIME out of the shipping `shell.html` fight card, the shipping
`shell.css` and the shipping `shell.js`, with the roster read out of the
shipping build — nothing here is transcribed, so nothing here can drift. The
only fake is where `AC` comes from.

Writes one PNG next to the reference sheets. Touches no build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
UI = HERE.parent / "app" / "ui"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def roster(game: pathlib.Path):
    """id / name / school, off the shipped WEAPONS table rather than a list."""
    g = game.read_text(encoding="utf-8")
    w = [{"id": m.group(1), "name": m.group(2), "aff": m.group(3)}
         for m in re.finditer(r'\{ id:"([a-z]+)", name:"([^"]+)", aff:"([a-z]+)"', g)]
    aff = {m.group(1): {"name": m.group(2)} for m in
           re.finditer(r'\n  ([a-z]+):\s*\{ key:"[a-z]+", name:"([^"]+)"', g)}
    if not w or not aff:
        raise SystemExit("could not read the roster out of the build")
    return {"WEAPONS": w, "AFFINITIES": aff}


def harness(stub) -> str:
    """The shipping fight card, the shipping stylesheet, the shipping script."""
    html = (UI / "shell.html").read_text(encoding="utf-8")
    css = (UI / "shell.css").read_text(encoding="utf-8")
    js = (UI / "shell.js").read_text(encoding="utf-8")
    # the fight card, lifted whole out of shell.html by its own heading
    m = re.search(r'(<div class="card">\s*<h2>The fight</h2>.*?</div>\s*</div>)',
                  html, re.S)
    if not m:
        raise SystemExit("the fight card is not where shell.html used to keep it")
    card = m.group(1)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{css}
/* THE RAIL IS 340px FROM THE SHELL'S OWN GRID (`grid-template-columns:1fr
   340px`). There is no game pane here, so it is pinned to the shipping width
   — a screenshot at any other width is of a layout that does not exist. */
main{{display:block}} .rail{{width:340px}}
</style></head><body><main>
<!-- `frame` is `$('game')` captured at load, and a null there would take out
     wireControls() before it reached the buttons under test. -->
<iframe id="game" hidden></iframe>
<aside class="rail">
{card}
</aside></main>
<script>window.__STUB = {json.dumps(stub)};</script>
<script>
{js}
</script>
<script>
/* `AC` is a script-level `let` in shell.js, so a later classic script shares
   the binding and can fill it — which is exactly what onGameLoad does. */
window.__ready = (() => {{
  try {{ AC = window.__STUB; fillRoster(); }}
  catch (e) {{ return "THREW: " + e.message; }}
  /* THE BUTTONS ARE WIRED TOO, because Random is one of the things under test
     — it used to set `selectedIndex`, which is wrong the moment the menu is
     filtered. `startFight` is replaced first: it drives the game in the frame
     and there is no game here, and a throw inside a click handler would count
     as a page error against the shell. wireControls() also wires the
     announcer and the short pipeline, none of which exist in this card, so it
     is allowed to stop early — the fight card's buttons are wired first. */
  window.startFight = () => {{ window.__fights = (window.__fights || 0) + 1; }};
  try {{ wireControls(); }} catch (e) {{ window.__wire = "stopped at: " + e.message; }}
  return "ok";
}})();
</script></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--out", default="../05-reference/v47/app-picker.png")
    A = ap.parse_args()
    from playwright.sync_api import sync_playwright

    game = resolve_game(A.game)
    stub = roster(game)
    tmp = UI / "_picker_probe.html"
    tmp.write_text(harness(stub), encoding="utf-8", newline="\n")
    out = (HERE / A.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nTHE APP'S FIGHTER PICKER — school, then fighter")
    print(f"  {len(stub['WEAPONS'])} relics, {len(stub['AFFINITIES'])} schools, "
          f"off {game.name}\n")

    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True,
                                   args=["--disable-gpu", "--no-sandbox"])
            pg = b.new_page(viewport={"width": 400, "height": 620},
                            device_scale_factor=2)
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(tmp.as_uri())
            pg.wait_for_timeout(400)

            ready = pg.evaluate("() => window.__ready")
            check("the shipping shell.js builds the picker", ready == "ok", ready)

            n = pg.eval_on_selector("#selA", "e => e.options.length")
            check("EVERY relic is in the fighter select, always",
                  n == len(stub["WEAPONS"]),
                  f"{n} options against {len(stub['WEAPONS'])} relics — the "
                  f"school menu HIDES, it does not rebuild")

            schools = pg.eval_on_selector(
                "#schoolA", "e => [...e.options].map(o => o.value)")
            first = []
            for w in stub["WEAPONS"]:
                if w["aff"] not in first:
                    first.append(w["aff"])
            check("the school menu is every school, in roster order",
                  schools == first, ", ".join(schools))

            # ---- one school at a time, against the roster it should show ----
            bad = []
            for k in schools:
                pg.select_option("#schoolA", k)
                vis = pg.eval_on_selector(
                    "#selA",
                    "e => [...e.options].filter(o => !o.hidden).map(o => o.value)")
                want = [w["id"] for w in stub["WEAPONS"] if w["aff"] == k]
                picked = pg.eval_on_selector("#selA", "e => e.value")
                if vis != want or picked != want[0]:
                    bad.append(f"{k}: showed {vis}, picked {picked}")
            check("choosing a school shows exactly that school and lands on "
                  "its first relic", not bad, "; ".join(bad) or
                  f"all {len(schools)} schools")

            # ---- the one that would fail silently --------------------------
            worst = None
            for w in stub["WEAPONS"]:
                if w["aff"] != pg.eval_on_selector("#schoolA", "e => e.value"):
                    worst = w
                    break
            pg.eval_on_selector("#selA", f"e => {{ e.value = '{worst['id']}'; }}")
            pg.evaluate("() => syncSchool('A')")
            got = pg.eval_on_selector("#selA", "e => e.value")
            sch = pg.eval_on_selector("#schoolA", "e => e.value")
            check("an id assigned from OUTSIDE the menu still takes, and the "
                  "school follows it",
                  got == worst["id"] and sch == worst["aff"],
                  f"set {worst['id']} while the menu showed another school; "
                  f"read back {got} / {sch}")

            # ---- and Random, which used to set selectedIndex ---------------
            seen = set()
            for _ in range(24):
                pg.evaluate("() => document.getElementById('btnRandom').click()")
                a = pg.eval_on_selector("#selA", "e => e.value")
                sa = pg.eval_on_selector("#schoolA", "e => e.value")
                aff = next(w["aff"] for w in stub["WEAPONS"] if w["id"] == a)
                seen.add((a, sa == aff))
            fights = pg.evaluate("() => window.__fights || 0")
            check("Random reaches relics outside the showing school, and the "
                  "school box never lies about what is selected",
                  len(seen) > 6 and all(ok for _, ok in seen) and fights == 24,
                  f"{len(seen)} distinct picks over {fights} clicks, "
                  f"{sum(1 for _, ok in seen if not ok)} mismatched")

            # ---- the layout, at the two longest strings in the roster ------
            longest = max(stub["AFFINITIES"].values(), key=lambda a: len(a["name"]))
            k = next(k for k, v in stub["AFFINITIES"].items() if v is longest)
            pg.select_option("#schoolA", k)
            pg.select_option("#schoolB", "dwarven")
            pg.eval_on_selector("#selB", "e => { e.value = 'grudgebearer'; }")
            pg.evaluate("() => syncSchool('B')")
            fit = pg.evaluate("""() => {
              const r = document.querySelector('.pickrow');
              const [a, b] = r.querySelectorAll('select');
              return { over: r.scrollWidth - r.clientWidth,
                       a: a.getBoundingClientRect().width,
                       b: b.getBoundingClientRect().width };
            }""")
            check("the two menus fit the 340px rail side by side",
                  fit["over"] <= 0 and fit["a"] > 90 and fit["b"] > 120,
                  f"school {fit['a']:.0f}px, fighter {fit['b']:.0f}px, "
                  f"overflow {fit['over']}px — longest school "
                  f"{longest['name']!r}")

            pg.locator(".rail").screenshot(path=str(out))
            # `window.swb` IS THE PRELOAD BRIDGE AND IT DOES NOT EXIST HERE,
            # so boot() and the announcer's voice list throw by construction.
            # The two known ones are named rather than the whole class
            # filtered: a THIRD missing bridge should show up as a failure and
            # make somebody look, not disappear into a wildcard.
            KNOWN = ("gamePath", "voices")
            real = [e for e in errs if not any(k in e for k in KNOWN)]
            check("no page errors from the shell's own code", not real,
                  "; ".join(real[:2]) or
                  f"(only the missing `window.swb` bridge: {len(errs)} errors, "
                  f"all of them {' / '.join(KNOWN)})")
            b.close()
    finally:
        tmp.unlink(missing_ok=True)

    print(f"\n  wrote {out}")
    ok = sum(1 for _, p in PASS if p)
    print(f"\n{ok}/{len(PASS)} checks passed"
          + ("" if ok == len(PASS) else f"  ({len(PASS) - ok} FAILED)"))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
