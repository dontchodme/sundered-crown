#!/usr/bin/env python3
"""THE BOLT, BIG. Four silhouettes of the same code path, side by side.

    python3 marrowdraw_bolt_zoom.py --game ../04-experiments/sc-marrowdraw.html

Rick, on the first cut: *"the balista shots look a little cartooney. can we go
for a longer slimmer and more realistic look?"* -- which is a judgement a
filmstrip at 30% scale cannot support either way. A bolt is about 130px long in
a 1080-wide hall and every look decision about it was being made from a picture
in which it is nine pixels.

So this photographs THE REAL `drawShots`, on the real arena, at the real
resolution, and then crops in. Nothing is re-implemented: synthetic shots are
pushed into a real match's `shots` array with the same fields `spawnShot` would
have set, the shipped renderer draws them, and the crop is the only thing this
file adds. `marrowdraw_probe [3]` is why this is safe to iterate on freely -- `r`
is on both sides of the engine's ledger and the parried-per-landed ratio does
not move with it, so the bolt's size and shape are pure look.

Writes one PNG into 05-reference/v42. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import io
import math
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v42"

# label, artLen, artW, artHead, artFletch, r
VARIANTS = [
    # NOT the old drawing -- the old drawing is gone. These are cut 2's
    # PROPORTIONS through the new code, which is the honest comparison:
    # it isolates the numbers from the construction.
    ("cut 2's proportions, drawn the new way", 3.40, 0.085, 0.62, 0.18, 44),
    ("shipping — from the reference", 3.20, 0.048, 0.34, 0.26, 44),
    ("longer, thinner still", 3.90, 0.038, 0.30, 0.22, 44),
    ("shorter, more feather", 2.70, 0.055, 0.36, 0.34, 44),
]

SHOT_JS = r"""([id, foe, seed, warm, variants, cx, ys, ang, fork]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  /* The balls are moved out of the way rather than deleted: a hall with no
     fighters in it draws a different floor, and the point is to see the bolt
     against the ground it really flies over. */
  const A = AC.CONFIG.arena;
  m.a.x = 40; m.a.y = A.h - 40; m.b.x = A.w - 40; m.b.y = A.h - 40;
  m.shake = 0;
  m.shots.length = 0;
  m.fx.length = 0; m.rings.length = 0; m.floats.length = 0;
  const own = me === m.a ? "a" : "b";
  variants.forEach((v, i) => {
    const [lbl, bL, bW, bH, bF, r] = v;
    const y = ys[i];
    /* A CURVED trail, because a straight one would hide the one thing the
       trail exists to show. Laid out as the arc a bolt turning at `home`
       rad/s actually flies, so this is the shape the game draws and not a
       flourish invented here. */
    /* INTEGRATED BACKWARDS from the bolt, not swept forwards from a guess.
       The first cut built the arc from a chord and put the trail on the wrong
       side of the object -- the bolt pointed up-right and its own history
       came in from down-right, which is a picture of nothing. */
    const T = [];
    let tx = cx, ty = y, ta = ang;
    const back = [];
    for (let k = 0; k < 13; k++){
      back.push(tx, ty);
      tx -= Math.cos(ta) * 14; ty -= Math.sin(ta) * 14;
      ta += 0.055;
    }
    for (let k = back.length - 2; k >= 0; k -= 2) T.push(back[k], back[k + 1]);
    m.shots.push({ own, x: cx, y, x0: cx, y0: y, spd0: 0, t0: m.t,
                   vx: Math.cos(ang) * 220, vy: Math.sin(ang) * 220,
                   r, life: 5, max: 5, grav: 0, dmgMul: 2.2,
                   bal: true, home: 3, aff: me.aff, a: ang,
                   bL, bW, bH, bF, trail: T });
    if (fork){
      for (const sgn of [-1, 1]){
        const a2 = ang + sgn * 0.45;
        m.shots.push({ own, x: cx + Math.cos(a2) * 150, y: y + Math.sin(a2) * 150,
                       x0: cx, y0: y, spd0: 0, t0: m.t,
                       vx: Math.cos(a2) * 220, vy: Math.sin(a2) * 220,
                       r: r * 0.55, life: 2.2, max: 2.2, grav: 0, dmgMul: 0.5,
                       fork: true, home: 4, aff: me.aff, a: a2,
                       bL: bL * 0.62, bW: bW * 1.30, bH: bH * 0.90,
                       bF: bF * 1.15, trail: [] });
      }
    }
  });
  AC.__draw(m);
  /* WORLD COORDINATES ARE NOT CANVAS PIXELS. The arena is 520x800 design
     units drawn into a 1080x1920 backing store through
     `c.translate(pad, arenaTop); c.scale(scale, scale)`. The first cut of
     this tool cropped at the world coordinates and photographed the HUD. The
     mapping is read back off the renderer rather than reconstructed here, so
     it cannot drift from the one that drew the frame. */
  const R = renderer;
  return { png: document.getElementById('cv').toDataURL('image/png'),
           k: R.k, pad: R.pad, top: R.arenaTop, scale: R.scale,
           aw: R.aw, ah: R.ah };
}"""


def font(sz, bold=True):
    for p in (HERE / "fonts" / ("AtkinsonHyperlegibleNext-Bold.ttf" if bold
                                else "AtkinsonHyperlegibleNext-Regular.ttf"),
              pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if p.exists():
            try:
                return ImageFont.truetype(str(p), sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--id", default="marrowdraw")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=8801)
    ap.add_argument("--warm", type=float, default=9.0)
    ap.add_argument("--zoom", type=float, default=1.55)
    ap.add_argument("--fork", action="store_true", help="draw the two forks too")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    out_p = pathlib.Path(a.out) if a.out else OUT / (
        "bolt-zoom-fork.png" if a.fork else "bolt-zoom.png")

    cx = 260                                     # arena is 520 x 800
    ys = [120 + i * 170 for i in range(len(VARIANTS))]
    ang = -0.34

    with game(game_path=gp) as (page, errors):
        res = page.evaluate(SHOT_JS, [a.id, a.foe, a.seed, a.warm,
                                      [list(v) for v in VARIANTS], cx, ys, ang,
                                      a.fork])
        assert not errors, errors[:4]

    full = Image.open(io.BytesIO(base64.b64decode(
        res["png"].split(",", 1)[1]))).convert("RGB")
    K, PADX, TOP, SC = res["k"], res["pad"], res["top"], res["scale"]
    print(f"  canvas {full.width}x{full.height}  k={K}  pad={PADX:.1f} "
          f"top={TOP:.1f} scale={SC:.3f}")

    def px(x, y):
        return (K * (PADX + x * SC), K * (TOP + y * SC))

    bw, bh = 760, 300
    tiles = []
    for (lbl, bL, bW, bH, bF, r), y in zip(VARIANTS, ys):
        ox, oy = px(cx, y)
        box = (max(0, int(ox) - bw // 2), max(0, int(oy) - bh // 2),
               min(full.width, int(ox) + bw // 2),
               min(full.height, int(oy) + bh // 2))
        im = full.crop(box)
        im = im.resize((int(im.width * a.zoom), int(im.height * a.zoom)), Image.LANCZOS)
        tiles.append((lbl, bL, bW, bH, bF, r, im))

    PAD, HEAD, GAP = 26, 52, 16
    W = PAD * 2 + tiles[0][6].width
    H = PAD * 2 + HEAD + sum(t[6].height for t in tiles) + GAP * len(tiles) * 2
    sheet = Image.new("RGB", (W, H), (11, 10, 13))
    d = ImageDraw.Draw(sheet)
    fb, fs = font(24), font(16, bold=False)
    d.text((PAD, PAD - 4), "THE BALLISTA BOLT — the shipped renderer, cropped in",
           font=fb, fill=(240, 232, 234))
    y = PAD + HEAD
    for lbl, bL, bW, bH, bF, r, im in tiles:
        d.text((PAD, y - 2), lbl, font=font(18), fill=(238, 226, 228))
        aspect = bL / (bW * 2)
        d.text((PAD + 300, y), f"len {bL:g}r   shaft {bW:g}r   head {bH:g}r   "
                               f"fletch {bF:g}L   aspect {aspect:.0f}:1",
               font=fs, fill=(150, 132, 138))
        y += GAP + 8
        sheet.paste(im, (PAD, y))
        y += im.height + GAP
    sheet.save(out_p)
    print(f"  wrote {out_p}  ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
