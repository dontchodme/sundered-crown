#!/usr/bin/env python
"""THE WINNOWING'S HIT STOP -- the freeze is the size of the rung. v67.

Built from `06-docs/v67/WINNOWING-HITSTOP-BRIEF-v67.md` (Cowork, 2026-09-03),
which is the input and the only input. Every number below is Rick's; nothing
here is bisected and nothing here is a design decision. CLAUDE.md §3 rule 0.

    stage 1   the two edits        sc-trunk -> sc-leaf.html

RICK WATCHED THORNSHEAR AND SAID THE HIT STOP "reads as lag even though its
probably not." He chose this patch AND the engine-wide rule in
`HITSTOP-BURST-BRIEF-v67.md`, over a kunai-with-no-freeze patch alone and over
the engine rule alone. This is the small one and it lands first.

THE DIAGNOSIS WAS MEASURED BEFORE ANYTHING WAS BUILT, because the brief makes
it a stop condition: `winnow_hitstop_probe.py` on the unpatched tip, 96 fights,
279 windows -- **1.825s of frozen picture a cast, 22.9% of the window**, 6002
of 7304 freezes caused by a kunai, and 5433 of those writes at or under 0.060s.
The brief predicted "several hundred ms"; it is nearly two seconds.

THE BASE IS THE CHAIN TIP AND THE FORK IS SETTLED UNDER IT. `sc-trunk.html`:
34 relics, the minute pace, Starwarden, and Crossweave's stages 7-12 -- the
first build that has had everything since the chain forked, and what
`app/main.js` loads. The brief was written when the tip was `sc-minute` and
says to name the branch; this is that name.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "thornshear"

# RICK'S NUMBERS, AND THE ONLY ONES IN THIS FILE. Brief §1: nothing fresh, a
# little off a wall, and 0.02 is Bloodletting's unit. They are PICTURE numbers
# -- the build does not bisect them and `verify` is a guard rail here rather
# than a target.
#
#   rung 0   a fresh kunai     0.000   the loose is the picture; the hit is a leaf
#   rung 1   off one wall      0.020
#   rung 2   off two           0.040
#   rung 3   off three         0.060   about a rung-0 kunai's freeze TODAY, on a
#                                      kunai twice its size -- the growth becomes
#                                      legible with no number on screen
RUNG_STOP = 0.02


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 "parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip()
                                               .splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


S1 = [

("the kunai carries no weight",
 '''      aff: f.aff, a,
    });
    f.shotsFired++;''',
 '''      /* AND IT CARRIES NO WEIGHT WHEN IT LANDS. Rick, having watched this
         ultimate: the hit stop "reads as lag even though its probably not."

         MEASURED BEFORE IT WAS TOUCHED (`winnow_hitstop_probe.py`, 96 fights,
         279 windows): **1.825 seconds of frozen picture a cast, 22.9% of the
         window**, of which 6002 of 7304 freezes were caused by a kunai and
         5433 of those writes were 0.060s or under. `stopBase` is a FLOOR --
         `min(stopMax, 0.045 + dmg * 0.0022)` -- so it does not scale down for
         a chip, and a 1.8-damage leaf was holding the whole picture for about
         half of what a 30-damage swing holds. Sixty-odd of them, at irregular
         moments, across five or six seconds. That is what a dropped frame
         looks like.

         SCOUR IS THE PRECEDENT AND IT IS EXACT: `over.stop` exists because a
         grind at 7 ticks a second would have frozen the world for 45% of every
         second it held someone, and "a grind is the one thing in this game
         that must not stutter". A ten-kunai fan is the same sentence with a
         different noun; the Winnowing simply shipped a version earlier and
         never got the ruling.

         `stop` IS THE ONLY FIELD SET. `over.onHit` and `over.knock` stay
         undefined, so `resolveHit` falls through to `self.w.onHit` for entangle
         and to the shot's own `knock` -- the ultimate's damage, its status, its
         shove and its rung schedule are byte-identical, and `engine_ab` over
         the other 33 relics is the proof. What moves is the match clock `t`,
         which advances through every freeze, so THORNSHEAR'S OWN pairings must
         differ and everyone else's must not. */
      over: { stop: 0 },
      aff: f.aff, a,
    });
    f.shotsFired++;'''),

("the freeze grows with the rung",
 '''    const u = src.w.ult;
    s.rung++;
    s.r *= u.growR;
    s.dmgMul *= u.growDmg;
    s.knock *= u.growKnock;''',
 '''    const u = src.w.ult;
    s.rung++;
    s.r *= u.growR;
    s.dmgMul *= u.growDmg;
    s.knock *= u.growKnock;
    /* AND THE FREEZE GROWS WITH IT -- Rick's ruling, chosen over "no freeze at
       all". 0 fresh, then 0.020 / 0.040 / 0.060 off one, two and three walls.

       THE GROWTH BECOMES LEGIBLE WITH NO NUMBER ON SCREEN, which is the
       Crucible's rule -- the freeze is the size of the meal. A rung-3 kunai is
       twice the size of a fresh one and now lands with about the weight a
       FRESH one used to have; a fresh one lands with none, because the loose
       is the picture and the hit is a leaf.

       IT IS WRITTEN HERE, WITH THE OTHER GROWTH, AND THAT IS ONE DEFINITION
       FOR BOTH REFLECTION PATHS. A kunai rungs up off a wall and off a parry,
       and this function is the only place either one goes -- so there is no
       second site to keep in step. `0.02 * s.rung` rather than a table for the
       same reason.

       A KILL KEEPS `killStop` AND A CRIT DOES NOT KEEP `critStopMul`.
       `resolveHit` guards `!fatal` before it honours an override, so the kill
       is untouched -- and the override replaces the WHOLE formula, so a crit
       kunai takes the rung's number rather than 1.7x it. Declared in the brief
       and fine: a crit kunai is still a 4-damage leaf. */
    s.over.stop = %UNIT% * s.rung;'''),

]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1"], default="1")
    ap.add_argument("--src", default="../02-chain/sc-trunk.html")
    ap.add_argument("--out", default="../02-chain/sc-leaf.html")
    ap.add_argument("--unit", type=float, default=RUNG_STOP)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nTHE WINNOWING'S HIT STOP -- the freeze is the size of the rung")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED, NOT GUESSED. The brief was written when
    # the tip was `sc-minute` and the chain was forked; this one has to be the
    # branch that carries BOTH, or the link it produces re-forks it.
    if 'id:"thornshear"' not in code:
        raise SystemExit("no Thornshear in this source -- wrong build")
    if 'id:"starwarden"' not in code:
        raise SystemExit(
            "this source is not the settled trunk -- no Starwarden in it.\n"
            "  Building on the other side of the fork would re-fork the chain.")
    if "novaDmg" not in code:
        raise SystemExit(
            "this source does not carry Crossweave's stages 7-12, so it is the\n"
            "  short branch. Build on the trunk.")
    print("  base  34 relics, minute pace, Starwarden AND Crossweave's nova "
          "-- the settled trunk")

    if "s.over.stop" in code:
        raise SystemExit("this source already carries the patch -- built")
    # AND THE OVERRIDE IT LEANS ON HAS TO BE THERE. Two edits are worth nothing
    # if `resolveHit` does not honour `over.stop`, and that is somebody else's
    # code -- Scour's.
    if "over && over.stop !== undefined && !fatal" not in code:
        raise SystemExit(
            "REFUSING TO WRITE -- `resolveHit` does not honour `over.stop`, or\n"
            "  no longer guards it with `!fatal`. This patch is TWO FIELDS and\n"
            "  a rule somebody else wrote; without that line it does nothing.")
    if "s.over" not in code:
        raise SystemExit(
            "REFUSING TO WRITE -- the shot path does not pass `s.over` to\n"
            "  `resolveHit`, so a kunai's override would never be read.")
    print("  path  resolveHit honours `over.stop` and guards `!fatal`; the "
          "shot path passes `s.over`")

    for label, old, new in S1:
        s = one(s, old, new.replace("%UNIT%", f"{A.unit:g}"), label)

    # WHAT SHIPPED IS WHAT THIS RUN PRINTED (`ult_matches`'s argument, one
    # relic along): the two writes are the whole patch, so both are read back
    # out of the output rather than trusted.
    out_code = strip_comments(s)
    if "over: { stop: 0 }," not in out_code:
        raise SystemExit("REFUSING TO WRITE -- the fresh kunai does not carry "
                         "a zero override")
    if f"s.over.stop = {A.unit:g} * s.rung;" not in out_code:
        raise SystemExit("REFUSING TO WRITE -- the rung does not set the stop")
    # AND NO OTHER PROJECTILE GAINED ONE. `over` on a shot is read by every
    # relic's hit path; this brief is one relic's and says so in its title.
    n_over = out_code.count("over: { stop:")
    if n_over != 1:
        raise SystemExit(f"REFUSING TO WRITE -- {n_over} shot overrides in the "
                         "output, expected exactly 1 (this is ONE relic's "
                         "patch)")
    print(f"  ok    one shot override in the whole build, and it is the kunai's")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")
    print(f"  rung 0 -> 0s, rung 1 -> {A.unit:g}s, rung 2 -> {2*A.unit:g}s, "
          f"rung 3 -> {3*A.unit:g}s   (Rick's; not bisected)")
    print("  a kill keeps killStop; a crit takes the rung's number, not 1.7x")
    print("\n  GATE -- in this order, and each can fail:")
    print("    python engine_ab.py --a ../02-chain/sc-trunk.html \\")
    print("      --b ../02-chain/sc-leaf.html --ids <the 33 others> --n 8")
    print("      IDENTICAL. Thornshear's OWN pairings differ -- run it "
          "separately\n      and say how many; that difference is the pass.")
    print("    python winnow_hitstop_probe.py --game ../02-chain/sc-leaf.html")
    print("      rung-0 freezes 0 EXACTLY, rung-3 0.060 EXACTLY, a kill 0.55.")
    print("      BEFORE was 1.825s a cast and 22.9% of the window.")
    print("    python verify.py --game ../02-chain/sc-leaf.html --n 40")
    print("      Thornshear was in band; the match clock alone should not move")
    print("      it past the n~700 noise. If it does, that is a FINDING.")
    print("    AND FILM ONE CAST, next to the same seed on sc-trunk. Rick said")
    print("      it reads as lag; whether it still does is his to say.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
