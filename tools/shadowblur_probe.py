#!/usr/bin/env python3
"""Is `shadowBlur` scaled by the CTM? No -- and that is a look bug, not a nit.

`Renderer`'s constructor states the invariant the whole art layer is written
against:

    this.W = 1080; this.H = 1920; this.k = canvas.width / 1080;
    /* ... Everything downstream keeps drawing in design pixels, which is why
       every hand-tuned 188, 66 and 12 in the HUD still means what it meant. */

That comment is true of every length EXCEPT `shadowBlur`, which the Canvas2D
spec puts in the coordinate space of the output bitmap. `c.shadowBlur = 22` is
22 DEVICE pixels whatever `k` is, while the radius beside it is a design pixel
that `k` shrinks. Halve the capture width and every glow in the game gets
twice as wide RELATIVE TO THE FRAME.

Which means the three surfaces this project judges its picture on have never
shown the same glow:

    post_spread.py, where the bloom was chosen  1080x1920   k = 1.000
    the app Rick watches fights in                453x805   k = 0.419
    the clip that actually ships (--w 540)        540x960   k = 0.500

WHAT WOULD COUNT AS EVIDENCE AGAINST: the BLUR-ONLY reach, measured in design
pixels, coming back equal across k. It does not; it goes as 1/k.

THE INSTRUMENT HAS THE SAME FAULT THE ART DOES, so it is decomposed the same
way (`CLAUDE.md` §4.1c). The first version of this test measured total reach
from the centre and concluded "shadowBlur IS scaled" -- wrong, because the
disc's radius scales and its blur does not, and one number over both cannot
tell them apart. The disc is measured bare, then with the glow, and subtracted.

    python shadowblur_probe.py
    python shadowblur_probe.py --census
    python shadowblur_probe.py --census --json ../05-reference/shadowblur.json

`--census` traps the setter through one drawn frame per relic and reports which
canvas and which function every non-zero write came from. THE STATIC COUNT
PRICES THE EDIT; THE CENSUS PRICES THE PICTURE, and they disagree — 74 live
sites in the file is 2 to 38 writes in a frame, ten ultimates write none at
all, and 200 of the writes across the roster are one function on an OFFSCREEN
canvas that `docs/DELIVERY-QUALITY-BRIEF.md` §1 does not mention.

Runs on the pinned runtime through scpage.py. The measurement itself needs no
game -- it is a property of the canvas -- but this repo pins playwright 1.62.0
for a reason (`docs/RUNTIME-DRIFT.md`) and a finding measured anywhere else is
not a finding about what ships. It also counts the call sites in the build,
because the size of the fix is half of what makes it a Rule 2 spread.

Exits non-zero if the blur turns out to be CTM-scaled after all, because then
`docs/DELIVERY-QUALITY-BRIEF.md` §1 is wrong and the plan built on it changes.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-hold-clamp.html"

# The surfaces that matter, not a sweep. 1080 is what the art was authored at
# and what the bloom spread was rendered at; 540 is what --w ships; 453 is the
# app's canvas width from docs/ARCHITECTURE.md.
SURFACES = [
    (1080, "the design resolution -- and the bloom spread"),
    (540, "cinema_clip.py --w default, what ships today"),
    (453, "the app's canvas"),
]

MEASURE_JS = """
(widths) => {
  const D = 1080, R = 40, BLUR = 20;

  /* One disc at the centre of a k-scaled backing store, drawn in DESIGN
     coordinates exactly as Renderer.draw() does -- setTransform(k,0,0,k,0,0)
     and then every length quoted at 1080-scale. Returns the reach of the
     rightmost lit pixel from the centre, in device px, along the middle row. */
  function reach(k, blur){
    const n = Math.round(D * k);
    const cv = document.createElement('canvas'); cv.width = n; cv.height = n;
    const c = cv.getContext('2d');
    c.setTransform(k, 0, 0, k, 0, 0);
    c.fillStyle = '#000'; c.fillRect(0, 0, D, D);
    if (blur){ c.shadowColor = '#FFFFFF'; c.shadowBlur = BLUR; }
    c.fillStyle = '#FFFFFF';
    c.beginPath(); c.arc(D / 2, D / 2, R, 0, Math.PI * 2); c.fill();
    const d = c.getImageData(0, 0, n, n).data, cy = (n / 2) | 0;
    let last = 0;
    /* 8/255 rather than 0: the shadow's gaussian tail never reaches exactly
       zero, so a >0 threshold measures the float precision of the rasteriser
       instead of the blur. */
    for (let x = 0; x < n; x++) if (d[(cy * n + x) * 4] > 8) last = x;
    return last - n / 2;
  }

  const rows = [];
  for (const w of widths){
    const k = w / D;
    const bare = reach(k, false), glow = reach(k, true);
    rows.push({
      w: w, k: k,
      discDevicePx: bare,
      discDesignPx: +(bare / k).toFixed(1),
      blurOnlyDevicePx: glow - bare,
      blurOnlyDesignPx: +((glow - bare) / k).toFixed(1),
    });
  }
  return { blur: BLUR, radius: R, rows: rows };
}
"""

ASSIGN = re.compile(r"shadowBlur\s*=\s*([^;]+)")

LIFE = {"dawnbringer": 1.6, "widowmaker": 1.3, "grudgebearer": 1.7,
        "thornwake": 2.4, "gravemourn": 1.6, "spellbreaker": 1.4,
        "oathwound": 1.5, "heartwood": 2.2, "nightfell": 1.4, "axiom": 1.5,
        "ironhail": 1.3, "lightkeeper": 1.5, "farwarden": 2.6, "aureole": 1.6,
        "censer": 1.6, "emberedge": 1.5, "slagheart": 4.9, "vinesower": 5.4,
        "bulwarden": 9.5, "marrowdraw": 8.6, "paradox": 9.5}

# A STATIC COUNT PRICES THE EDIT. IT DOES NOT PRICE THE PICTURE -- one relic's
# branch runs per frame, so 74 live sites in the file is not 74 writes in a
# frame. This traps the setter and records which canvas and which function each
# non-zero write came from, which is the number that says whether the fix is
# visible and where.
CENSUS_JS = r"""([id, foe, block, t, life, w]) => {
  const proto = CanvasRenderingContext2D.prototype;
  const base = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
  const seen = [];
  Object.defineProperty(proto, 'shadowBlur', {
    configurable: true,
    get(){ return base.get.call(this); },
    set(v){
      if (v){
        const c = this.canvas;
        /* frame 2 of the stack is the caller; frame 0 is the setter itself
           and frame 1 is the Error construction. */
        const st = (new Error().stack || '').split('\n')[2] || '';
        seen.push({ id: (c && c.id) || '-', w: c ? c.width : 0,
                    fn: (st.match(/at ([\w.$]+)/) || [0, '?'])[1] });
      }
      base.set.call(this, v);
    }
  });
  AC.setResolution(w, Math.round(w * 16 / 9));
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, 25064);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.shake = 0;
  const wp = AC.WEAPONS.find(x => x.id === id);
  m.ultFx = block
    ? Object.assign({}, block, { src:"a", tgt:"b", x:m.a.x, y:m.a.y,
        tx:m.b.x, ty:m.b.y, aff:m.a.aff, t:t, life:life })
    : { w:id, kind:wp.ult.kind, src:"a", tgt:"b", x:m.a.x, y:m.a.y,
        tx:m.b.x, ty:m.b.y, hit:true, radius:wp.ult.radius||300,
        aff:m.a.aff, t:t, life:life };
  AC.__draw(m);
  Object.defineProperty(proto, 'shadowBlur', base);   /* harness, not a change */
  return seen;
}"""


def census(page, lib, at=0.35, width=540):
    """Non-zero shadowBlur writes in ONE drawn ult frame, per relic."""
    rows = []
    for ident, entry in lib.items():
        phase = entry["phases"][-1]
        block = entry["blocks"][phase]
        life = LIFE.get(ident, 1.5)
        foe = "dawnbringer" if ident == "grudgebearer" else "grudgebearer"
        seen = page.evaluate(CENSUS_JS,
                             [ident, foe, block, at * life, life, width])
        main = [s for s in seen if s["id"] == "cv"]
        off = [s for s in seen if s["id"] != "cv"]
        fns = collections.Counter(s["fn"] for s in main)
        ult = (fns.pop("Renderer.drawUltOver", 0)
               + fns.pop("Renderer.drawUltUnder", 0))
        rows.append({"id": ident, "phase": phase, "ult": ult,
                     "main": len(main), "off": len(off),
                     "offw": sorted({s["w"] for s in off}),
                     "offfn": dict(collections.Counter(s["fn"] for s in off)),
                     "other": dict(fns)})
    return rows


def count_sites(path: pathlib.Path) -> dict:
    """How many `shadowBlur =` sites are there, and how many honour `this.k`?

    Deliberately looks for `this.k` and not a bare `k`. Three sites read
    `22 * k`, `26 * k`, `8 + k * 16` -- and in every one of them `k` is the
    ult's own `t / life` ratio, a number between 0 and 1, not the resolution
    scale. Matching on `k` alone would report three fixed sites that are not
    fixed, which is the wrong direction for a count that prices a change.
    """
    src = path.read_text(encoding="utf-8", errors="replace")
    hits = ASSIGN.findall(src)
    scaled = [h.strip() for h in hits if "this.k" in h]
    zeroed = [h for h in hits if h.strip() in ("0", "0.0")]
    return {
        "assignments": len(hits),
        "scaled_by_this_k": len(scaled),
        "scaled_examples": scaled[:5],
        "zeroing": len(zeroed),
        "live": len(hits) - len(zeroed),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD),
                    help="only used to open the pinned runtime and to count "
                         "call sites; the measurement is game-independent")
    ap.add_argument("--json", metavar="PATH", help="write the result")
    ap.add_argument("--census", action="store_true",
                    help="also trap the setter and count the writes in one "
                         "drawn ult frame per relic -- what the fix touches, "
                         "as against how many lines it edits")
    ap.add_argument("--lib", default=str(REPO / "05-reference" / "post" /
                                        "ultfx-library.json"))
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    cen = None
    widths = [w for w, _ in SURFACES]
    with game(game_path=path) as (page, errors):
        out = page.evaluate(MEASURE_JS, widths)
        agent = page.evaluate("() => navigator.userAgent")
        if args.census:
            libp = pathlib.Path(args.lib)
            if not libp.exists():
                print(f"! --census needs {libp.name}; run ult_fx_capture.py")
                return 2
            cen = census(page, json.loads(libp.read_text(encoding="utf-8")))
    if errors:
        print("! page errors:")
        for e in errors[:10]:
            print("   ", e)
        return 1

    chrome = re.search(r"Chrome/([\d.]+)", agent)
    print(f"[blur] Chromium {chrome.group(1) if chrome else '?'}  "
          f"shadowBlur = {out['blur']}, disc r = {out['radius']} design px\n")

    print("                                     disc      disc      BLUR ONLY"
          "   BLUR ONLY")
    print("   width      k                  (device)  (design)     (device)"
          "    (design)")
    for row, (_, why) in zip(out["rows"], SURFACES):
        print(f"   {row['w']:>5}  {row['k']:.3f}  "
              f"{row['discDevicePx']:>18}  {row['discDesignPx']:>8}  "
              f"{row['blurOnlyDevicePx']:>11}  {row['blurOnlyDesignPx']:>10}")
        print(f"          {why}")

    base = out["rows"][0]
    dev = {r["blurOnlyDevicePx"] for r in out["rows"]}
    print()
    print(f"   the disc scales with k, as design pixels should: "
          f"{' / '.join(str(r['discDesignPx']) for r in out['rows'])} design px")
    print(f"   the blur does not: {' / '.join(str(r['blurOnlyDevicePx']) for r in out['rows'])}"
          f" DEVICE px at every k")

    if len(dev) > 1:
        print("\n   (device-px reach is not perfectly constant -- the "
              "rasteriser quantises\n    the tail differently at each size. "
              "The design-px column is the finding.)")

    print()
    for r in out["rows"][1:]:
        f = r["blurOnlyDesignPx"] / base["blurOnlyDesignPx"]
        print(f"   at {r['w']:>4} every glow in the game is {f:.2f}x wider "
              f"relative to the frame than at 1080.")

    sites = count_sites(path)
    print(f"\n[sites] {path.name}")
    print(f"   {sites['assignments']} `shadowBlur =` assignments, "
          f"{sites['zeroing']} of them zeroing it, {sites['live']} live")
    print(f"   {sites['scaled_by_this_k']} multiply by `this.k`")
    if sites["scaled_by_this_k"] == 0:
        print("   -- not three, as docs/DELIVERY-QUALITY-BRIEF.md §1 says. The "
              "three sites\n      reading `22 * k`, `26 * k` and `8 + k * 16` "
              "take `k` as the ult's own\n      t/life ratio, not the "
              "resolution scale. NOTHING in the build is\n      "
              "resolution-independent here.")

    if cen is not None:
        print(f"\n[census] non-zero shadowBlur writes in ONE drawn frame, "
              f"at --w 540, t/life 0.35\n")
        print(f"   {'relic':<14}{'phase':<9}{'ult':>5}{'main':>6}{'off':>6}"
              f"   the rest of the main canvas")
        for r in cen:
            print(f"   {r['id']:<14}{r['phase']:<9}{r['ult']:>5}"
                  f"{r['main']:>6}{r['off']:>6}   {r['other'] or ''}")
        silent = [r["id"] for r in cen if r["ult"] == 0]
        offw = sorted({w for r in cen for w in r["offw"]})
        print(f"\n   {len(cen) - len(silent)}/{len(cen)} ult set-pieces write "
              f"shadowBlur on the main canvas at all.")
        print(f"   {len(silent)} write NONE and the fix cannot touch them: "
              f"{', '.join(silent)}")
        print("   Daybreak is among them -- CLAUDE.md §4.1b's own subject "
              "draws its corona\n   as a radial gradient under `lighter`, not "
              "as a shadow. `--w` does not\n   widen it, and no `_blur` helper "
              "narrows it.")
        offfn = collections.Counter()
        for r in cen:
            offfn.update(r["offfn"])
        print(f"\n   `off` is OFFSCREEN canvases -- widths {offw} across the "
              f"roster,\n   not one buffer. Who writes to them:")
        for fn, n in offfn.most_common():
            print(f"      {n:>4}  {fn}")
        print("\n   drawGlassRelic is the constant one. _ballBuf (:13790) bakes "
              "each relic\n   body into a canvas sized ceil(rad * 2 * k), "
              "scaled by that same k, and\n   draws it back 1:1 -- so its halo "
              "(`shadowBlur = 8 + hpFrac * 26`) is\n   device-space ON THE "
              "FRAME exactly as the main canvas is. It is on screen\n   for "
              "BOTH relics on EVERY FRAME OF EVERY FIGHT, not only during an "
              "ult.")
        print("\n   AND IT IS NOT A RENDERER METHOD. drawGlassRelic is a "
              "module-level\n   function taking `c`, so `this.k` is not in "
              "scope. The helper cannot be\n   dropped in there; the factor has "
              "to be passed through its `o` bag.\n   DELIVERY-QUALITY-BRIEF.md "
              "§1's '129 mechanical replacements' does not\n   describe this "
              "half of the edit.")

    ok = base["blurOnlyDesignPx"] > 0 and all(
        r["blurOnlyDesignPx"] > base["blurOnlyDesignPx"] * 1.2
        for r in out["rows"][1:])

    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(
            {"userAgent": agent, "measure": out, "sites": sites,
             "census": cen, "ctm_scaled": not ok}, indent=1))
        print(f"\n   wrote {p}")

    if ok:
        print("\nCONFIRMED  shadowBlur is in device space on the pinned "
              "runtime.")
        print("           `--w` is a look knob. Raising it without the "
              "`_blur(px)` helper")
        print("           changes every glow in the game.")
        return 0

    print("\n! shadowBlur came back CTM-SCALED on this runtime.")
    print("  docs/DELIVERY-QUALITY-BRIEF.md §1 is then wrong and the "
          "sequencing it\n  imposes on §7 steps 2 and 3 does not apply. "
          "Do not proceed on the brief.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
