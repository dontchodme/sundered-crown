#!/usr/bin/env python3
"""THE LAST FOUR BLURS — bake the HUD bar glows.

    python3 hudglow_build.py --src sc-buf.html --out sc-hud.html

`sundered-crown-perf-results.md`: after the world light and the ball buffer,
four blurred draws remain on the full 1080x1920 canvas and they cost **8.34 ms,
42% of the frame**. Traced, three of the four are `drawBar`:

    2x  blur 16   an 11-pixel colour swatch, one per fighter
    1x  blur 14   the ult charge bar, only while it is READY

An 11-pixel circle is being blurred at full-canvas price. So is a 300x9 bar.

THE FIX IS THE ONE THIS CODEBASE ALREADY TRUSTS. `weaponGlow` bakes a blur once
into a small offscreen canvas and blits it, drawing the crisp shape live on top
with no shadow — its own comment records taking eleven blurred draws per weapon
per frame down to zero. This is that, for the HUD.

The sprite holds the GLOW AND NOTHING ELSE, using `weaponGlow`'s own trick: the
shape is painted far off the sprite and `shadowOffsetX` brings its shadow back
into frame. Baking the shape *with* its shadow and then drawing the shape again
live composites it twice and comes out visibly hotter — a mistake `weaponGlow`
made in v1 and documents.

CACHE KEYS
  swatch    colour only. Seven schools, seven sprites, for the life of the page.
  ult bar   colour + width bucketed to 4px. The bar is only drawn glowing above
            85% charge, so the width range is ~45px: a dozen entries at most.
"""
from __future__ import annotations
import argparse, pathlib, sys

HELPER = r'''
/* ------------------------------------------------------------- HUD GLOW
   Same idea as `weaponGlow` and for the same measured reason: a Canvas2D
   shadow costs in proportion to the SURFACE it runs on, not the size of the
   thing being blurred, so an 11-pixel swatch blurred on a 2.07 Mpx canvas
   costs what a full-canvas blur costs. Measured on an Adreno 660: the three
   drawBar blurs were most of 8.34 ms a frame.

   The sprite holds the glow and nothing else — the shape is painted off the
   sprite and its shadow offset back on — so the crisp shape can be drawn live
   on top without compositing it twice. sundered-crown-perf-results.md. */
const _hudGlowCache = new Map();
function hudGlow(key, w, h, blur, color, paint){
  let g = _hudGlowCache.get(key);
  if (g) return g;
  const PAD = Math.ceil(blur * 1.5) + 4;
  const cw = Math.ceil(w) + PAD * 2, ch = Math.ceil(h) + PAD * 2;
  const cv = document.createElement("canvas");
  cv.width = cw; cv.height = ch;
  const cx = cv.getContext("2d");
  const OFF = cw + 1000;
  cx.translate(PAD, PAD);
  cx.shadowColor = color; cx.shadowBlur = blur; cx.shadowOffsetX = OFF;
  cx.translate(-OFF, 0);
  paint(cx);
  g = { cv, ox: -PAD, oy: -PAD };
  if (_hudGlowCache.size > 200) _hudGlowCache.clear();
  _hudGlowCache.set(key, g);
  return g;
}
'''
HELPER_ANCHOR = "const _glowCache = new Map();"

SWATCH_OLD = """    c.save();
    c.fillStyle = f.aff.core;
    c.shadowColor = f.aff.core; c.shadowBlur = 16;
    c.beginPath(); c.arc(pad + 11, y + 26, 11, 0, TAU); c.fill();
    c.restore();"""
SWATCH_NEW = """    c.save();
    {                                          /* glow from a sprite, then the crisp disc */
      const col = f.aff.core;
      const g = hudGlow("sw|" + col, 22, 22, 16, col, (x) => {
        x.fillStyle = col; x.beginPath(); x.arc(11, 11, 11, 0, TAU); x.fill();
      });
      c.drawImage(g.cv, pad + 11 - 11 + g.ox, y + 26 - 11 + g.oy);
    }
    c.fillStyle = f.aff.core;
    c.beginPath(); c.arc(pad + 11, y + 26, 11, 0, TAU); c.fill();
    c.restore();"""

ULT_OLD = """    c.fillStyle = hot ? "#FFF4D0" : f.aff.glow;
    if (hot){ c.shadowColor = "#FFF4D0"; c.shadowBlur = 14; }
    this.roundRect(cx, y + 36, cw * cf, 9, 4); c.fill();"""
ULT_NEW = """    if (hot){                                  /* glow from a sprite, width bucketed */
      const bw = Math.max(8, Math.round(cw * cf / 4) * 4);
      const self = this;
      const g = hudGlow("ult|" + bw, bw, 9, 14, "#FFF4D0", (x) => {
        x.fillStyle = "#FFF4D0";
        self.roundRect.call({ ctx: x, roundRect: self.roundRect }, 0, 0, bw, 9, 4);
        x.fill();
      });
      c.drawImage(g.cv, cx + g.ox, y + 36 + g.oy);
    }
    c.fillStyle = hot ? "#FFF4D0" : f.aff.glow;
    this.roundRect(cx, y + 36, cw * cf, 9, 4); c.fill();"""

PROTECTED = "sundered-crown.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="sc-buf.html")
    ap.add_argument("--out", default="sc-hud.html")
    a = ap.parse_args()
    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    here = pathlib.Path(__file__).parent
    t = (here / a.src).read_text(encoding="utf-8")
    for name, anc in (("helper", HELPER_ANCHOR), ("swatch", SWATCH_OLD), ("ult bar", ULT_OLD)):
        if t.count(anc) != 1:
            print(f"! anchor {name} appears {t.count(anc)} times, expected 1", file=sys.stderr)
            return 1
    t = t.replace(HELPER_ANCHOR, HELPER + HELPER_ANCHOR, 1)
    t = t.replace(SWATCH_OLD, SWATCH_NEW, 1)
    t = t.replace(ULT_OLD, ULT_NEW, 1)
    print("  [hudglow] hudGlow injected")
    print("  [hudglow] swatch  -> sprite (2 blurs/frame)")
    print("  [hudglow] ult bar -> sprite (1 blur/frame when READY)")
    out = here / a.out
    out.write_text(t, encoding="utf-8")
    print(f"{a.src} -> {a.out}")
    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        pg.evaluate("""()=>{ AC.setResolution(1080,1920);
          const m=new AC.Match('grudgebearer','spellbreaker',20260813);
          m.introT=0; const dt=AC.CONFIG.physics.dt;
          for(let i=0;i<2400;i++){ m.step(dt); if(i%400===0) AC.__draw(m); }
          AC.__draw(m); return 1; }""")
        if errs:
            print("! PAGE ERRORS:\n  " + "\n  ".join(errs[:4]), file=sys.stderr)
            return 1
    print("  check: 2400 steps, 7 draws, no page errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
