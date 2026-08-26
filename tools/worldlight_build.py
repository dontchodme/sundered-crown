#!/usr/bin/env python3
"""OPTION B — hoist the world light OUT of the shape functions.

    python3 worldlight_build.py --src sc-bow.html --out sc-lit.html

WHY
---
`sundered-crown-baked-art.md`: `--worldlight` wired `_lit` into the TYPE layer
(`_gsBase`, `_whBase`, ...). The art is authored at the SCHOOL layer, and three
of seven grammars REPLACE the type rather than extend it, while vigil calls it
and then plates over it. Measured: **18 of 42 cells have no world lighting at
all**, including every runic and verdant cell and the whole bow and flail head.

Wiring `_lit` into each grammar is ~40 sites and still cannot help a shape that
has no faces. This does it in ONE site instead, at the layer that actually
knows where the world is:

    draw the weapon into a sprite  ->  composite a world-oriented gradient
    over it with `source-atop`     ->  blit

`source-atop` paints only where the sprite already has ink, so the light lands
on the weapon and nothing else, whatever any grammar drew. All 42 cells, the
bow and the flail head included, with no grammar edited.

THE SPRITE IS CACHED THE SAME WAY THE GLOW ALREADY IS.
`weaponGlow` already bakes a per-(shape, L, W, colour, k) offscreen canvas and
blits it, so this reuses that idea rather than inventing one: the UNLIT shape
is baked once per key, and only the gradient pass runs per frame. The gradient
direction is the one thing that must be live, because it is the whole point.

WORLD-DOWN IN LOCAL COORDINATES.
The sprite is blitted through the weapon's own rotation `a`, so a gradient
authored inside the sprite has to be counter-rotated or it turns with the
weapon and we are back where we started. World (0,1) maps to local
(sin a, cos a). That single expression is the entire fix.

WHAT THIS DOES NOT DO
---------------------
It does not remove `_lit` from the base shapes. Both would then apply and the
facets would be lit twice. `--strip` removes the `_lit` calls; run it once the
A/B says the hoisted light is the one to keep. Until then this is ADDITIVE and
deliberately so, because the point of the build is to be timed, not shipped.

COST, WHICH IS THE WHOLE REASON THIS EXISTS
-------------------------------------------
Per weapon per frame: one clearRect, one sprite blit into scratch, one gradient
fill, one blit out. Against the current cost of one direct shape call. Whether
that is free or ruinous is not knowable in this container -- `bench_build.py`'s
own docstring records three in-container methods disagreeing by three orders of
magnitude. Build both perf pages and run BENCH on real hardware.
"""
from __future__ import annotations
import argparse, pathlib, sys

HELPER = r'''
/* ------------------------------------------------------ HOISTED WORLD LIGHT
   The light belongs to the world, so it is applied by the thing that knows
   where the world is -- not by 40 shading sites inside shape functions, 18 of
   whose 42 cells never run. sundered-crown-baked-art.md.

   THE SHAPE IS DRAWN LIVE, NOT FROM A CACHED SPRITE, and that is not an
   oversight. v1 of this baked the weapon into a sprite keyed like `weaponGlow`
   does and blitted it. Measured, it made two shapes WORSE:

       greatsword  24.9% -> 12.8%      umbral greatsword  61.5% -> 4.4%
       twinblade   22.1% -> 12.0%

   because `_lit` reads `c.getTransform()`, and a sprite is baked through a pure
   translate. The cached sprite has no rotation in it, so every facet `_lit`
   already drives freezes at its unrotated value and the existing world light is
   destroyed by the thing meant to extend it.

   So the scratch is WORLD-ORIENTED: the rotation goes into the scratch, the
   shape is drawn through it, `_lit` sees a live transform and keeps working,
   and the gradient needs no counter-rotation because the buffer is already in
   world space. The blit counter-rotates once on the way out.

   The cost is that nothing can be cached across frames. That is the whole
   question this build exists to price. */
let _litScratch = null;
function litWeapon(c, shape, L, W, pal, k, ang){
  const fn = SHAPES[shape];
  if (!fn) return false;
  /* THE SCRATCH IS SIZED IN DEVICE PIXELS, NOT LOCAL UNITS. v2 baked at scale 1
     and let the blit magnify it, which was soft on screen AND made this build
     nine times cheaper to draw than the real thing -- so the perf number it
     produced would have been a measurement of a smaller weapon. Read the live
     CTM scale and rasterise at it. */
  const m = c.getTransform();
  const kx = Math.hypot(m.a, m.b) || 1;
  const R = Math.ceil(L * 1.25 + W * 1.5) + 12;
  const S = Math.ceil(R * 2 * kx);
  if (!_litScratch) _litScratch = document.createElement("canvas");
  const s = _litScratch;
  if (s.width < S || s.height < S){ s.width = S; s.height = S; }
  const sx = s.getContext("2d");
  sx.setTransform(1, 0, 0, 1, 0, 0);
  sx.globalCompositeOperation = "source-over";
  sx.globalAlpha = 1;
  sx.clearRect(0, 0, s.width, s.height);
  sx.save();
  sx.translate(S / 2, S / 2);
  sx.scale(kx, kx);
  sx.rotate(ang);                       /* world orientation, so _lit still works */
  if (shape === 'flailHead') fn(sx, W, pal, k); else fn(sx, L, W, pal, k);
  sx.restore();
  /* The buffer is in world space, so "down" is just +y. No counter-rotation,
     which is the point: one expression instead of a per-site normal. */
  /* THE RAMP MUST SPAN THE WEAPON, NOT THE BUFFER. v3 ran the gradient across
     the whole scratch, which is sized for the weapon's LENGTH -- so across a
     thin blade lying flat the ramp barely changed and the light did nothing.
     Project the weapon's own local bounding box through `ang` and use its
     world-space vertical extent, so a horizontal blade gets the full top-to-
     bottom ramp across its thickness and a vertical one gets it across its
     length, which is what a real directional light does. */
  const bx0 = -L * 0.10, bx1 = L * 1.06, by0 = -W * 1.6, by1 = W * 1.6;
  const ca = Math.cos(ang), sa = Math.sin(ang);
  let ymin = Infinity, ymax = -Infinity;
  for (const [px, py] of [[bx0,by0],[bx1,by0],[bx1,by1],[bx0,by1]]){
    const wy = (px * sa + py * ca) * kx;
    if (wy < ymin) ymin = wy;
    if (wy > ymax) ymax = wy;
  }
  const g = sx.createLinearGradient(0, S / 2 + ymin, 0, S / 2 + ymax);
  /* Light from above. The contrast in this art runs DOWNWARD -- every school's
     steel is near-white and every dark near-black -- so the top face gets a
     small lift and the underside takes the school's own `dark`. */
  g.addColorStop(0.00, "rgba(255,255,255,0.14)");
  g.addColorStop(0.45, "rgba(255,255,255,0.00)");
  g.addColorStop(0.55, pal.dark + "00");
  g.addColorStop(1.00, pal.dark + "8C");
  sx.fillStyle = g;
  sx.globalCompositeOperation = "source-atop";
  sx.fillRect(0, 0, S, S);
  sx.globalCompositeOperation = "source-over";
  c.save();
  c.rotate(-ang);                       /* undo the caller's rotation */
  c.scale(1 / kx, 1 / kx);              /* work in device pixels so the blit is 1:1 */
  c.drawImage(s, 0, 0, S, S, -S / 2, -S / 2, S, S);
  c.restore();
  return true;
}
'''

ANCHOR_HELPER = "const _glowCache = new Map();"

CALL_OLD = """      const fn = SHAPES[f.w.shape];
      if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);"""
CALL_NEW = """      if (!litWeapon(c, f.w.shape, reach + 6, f.w.artW, pal, f.drawK, a)){
        const fn = SHAPES[f.w.shape];
        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }"""

FLAIL_OLD = """      c.translate(f.headX, f.headY);
      c.shadowColor = pal.core; c.shadowBlur = 22;
      SHAPES.flailHead(c, f.w.artW, pal, f.headSpin);
      c.restore();
      return;"""

FLAIL_NEW = """      c.translate(f.headX, f.headY);
      c.shadowColor = pal.core; c.shadowBlur = 22;
      /* The flail head is drawn on its own path -- it never reaches the blades
         loop below -- so it needs the hoisted light wired separately or it stays
         the one shape in the game with no world lighting at all. `ang` is 0:
         the head does not ride a rotated arm, it hangs, so the caller's frame
         is already world-aligned. */
      if (!litWeapon(c, 'flailHead', f.w.artW, f.w.artW, pal, f.headSpin, 0)){
        SHAPES.flailHead(c, f.w.artW, pal, f.headSpin);
      }
      c.restore();
      return;"""

PROTECTED = "sundered-crown.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="sc-bow.html")
    ap.add_argument("--out", default="sc-lit.html")
    a = ap.parse_args()
    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    here = pathlib.Path(__file__).parent
    t = (here / a.src).read_text(encoding="utf-8")

    for name, anc in (("helper", ANCHOR_HELPER), ("call site", CALL_OLD)):
        if t.count(anc) != 1:
            print(f"! anchor for {name} appears {t.count(anc)} times, expected 1",
                  file=sys.stderr)
            return 1
    t = t.replace(ANCHOR_HELPER, HELPER + "\n" + ANCHOR_HELPER, 1)
    t = t.replace(CALL_OLD, CALL_NEW, 1)
    if t.count(FLAIL_OLD) != 1:
        print(f"! flail anchor appears {t.count(FLAIL_OLD)} times, expected 1", file=sys.stderr)
        return 1
    t = t.replace(FLAIL_OLD, FLAIL_NEW, 1)
    print("  [worldlight] flail head rewired (its own draw path)")
    # export it so bake_probe can measure the same function the renderer calls
    exp = "window.AC = { CONFIG, AFFINITIES, STATUS, WEAPONS, SHAPES,"
    if t.count(exp) != 1:
        print("! could not find the AC export to attach litWeapon", file=sys.stderr)
        return 1
    t = t.replace(exp, "window.AC = { litWeapon, CONFIG, AFFINITIES, STATUS, WEAPONS, SHAPES,", 1)
    print("  [worldlight] litWeapon exported on AC for probing")
    print("  [worldlight] helper injected beside the glow cache")
    print("  [worldlight] 1 call site rewired  (was ~40 shading sites)")

    out = here / a.out
    out.write_text(t, encoding="utf-8")
    print(f"{a.src} -> {a.out}")

    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        bad = pg.evaluate("""() => {
          const out = [];
          for (const s of ['greatsword','warhammer','scythe','twinblade','bow','flailHead'])
            for (const k in AC.AFFINITIES){
              try {
                const cv = document.createElement('canvas');
                cv.width = 400; cv.height = 400;
                const c = cv.getContext('2d');
                c.translate(200,200);
                if (!window.litWeapon) { out.push('litWeapon not exported'); return out; }
              } catch(e){ out.push(s + '/' + k + ': ' + e.message); }
            }
          return out; }""")
        if errs:
            print("! PAGE ERRORS:\n  " + "\n  ".join(errs), file=sys.stderr)
            return 1
    print("  check: page loads clean, no exceptions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
