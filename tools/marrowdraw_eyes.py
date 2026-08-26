#!/usr/bin/env python3
"""THE HUNTER'S EYES, BIG. Rick's animation, at three counts and mid-blink.

    python3 marrowdraw_eyes.py --game ../02-chain/sc-marrowdraw-frame.html

Rick: *"can we also give the ball itself an animation when its bloodhunting?
maybe piercing red hunters eyes floating above it?"*

A ball is 34 world units in a 520-wide hall, so the eyes are a few dozen pixels
in a posted short and completely undecidable from a filmstrip. This runs a real
fight to a frame inside the window, draws with the shipped renderer, and crops
in on the caster -- and it varies `artEyes` and the blink phase across the row,
so the count and the aliveness can be judged rather than guessed at.

Writes one PNG into 05-reference/v42. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v42"

CAP_JS = r"""([id, foe, seed, warm, into, eyes, tOff]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const w = AC.WEAPONS.find(x => x.id === id);
  const u0 = w.ult.artEyes;
  if (eyes !== null) w.ult.artEyes = eyes;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  let n = 0;
  while (n < Math.round(into / DT) && !m.over){ m.step(DT); n++; }
  m.shake = 0;
  /* The blink is a function of m.t, so a phase offset is the only honest way
     to photograph a shut eye without freezing the sim at a different moment
     in the FIGHT. Presentation clock only; nothing in the sim reads it. */
  /* THE BLINK IS 4.5% OF A 2.4s CYCLE, so photographing one by nudging the
     clock is luck -- the first cut asked for an offset of 1.06s and caught
     every eye wide open. `ph = (t*0.42 + i*0.37) % 1` is invertible, so the
     frame is SOLVED for instead: the smallest t at or after this one that
     puts eye `tOff` inside its own blink. */
  if (tOff !== null && tOff !== undefined && tOff >= 0){
    const want = 0.985, i = tOff | 0;
    for (let k = 0; k < 400; k++){
      const cand = (want - i * 0.37 + k) / 0.42;
      if (cand >= m.t){ m.t = cand; break; }
    }
  }
  AC.__draw(m);
  const R = renderer;
  const out = { png: document.getElementById('cv').toDataURL('image/png'),
                k: R.k, pad: R.pad, top: R.arenaTop, scale: R.scale,
                x: me.x, y: me.y, up: !!me.ultBal,
                left: me.ultBal ? +(me.ultBal.dur - me.ultBal.t).toFixed(1) : 0 };
  w.ult.artEyes = u0;
  return out;
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
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw-frame.html")
    ap.add_argument("--id", default="marrowdraw")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=8801)
    ap.add_argument("--warm", type=float, default=8.0)
    ap.add_argument("--into", type=float, default=2.2)
    ap.add_argument("--zoom", type=float, default=2.4)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    out_p = pathlib.Path(a.out) if a.out else OUT / "hunters-eyes.png"

    PANES = [("two", 2, None), ("three — shipping", 3, None),
             ("four", 4, None), ("three, one eye blinking", 3, 1)]

    tiles = []
    with game(game_path=gp) as (page, errors):
        for label, n, off in PANES:
            r = page.evaluate(CAP_JS, [a.id, a.foe, a.seed, a.warm, a.into, n, off])
            assert r["up"], "the window was not open at that frame — raise --into"
            full = Image.open(io.BytesIO(base64.b64decode(
                r["png"].split(",", 1)[1]))).convert("RGB")
            cx = r["k"] * (r["pad"] + r["x"] * r["scale"])
            cy = r["k"] * (r["top"] + r["y"] * r["scale"])
            bw, bh = 420, 380
            box = (max(0, int(cx) - bw // 2), max(0, int(cy) - int(bh * 0.72)),
                   min(full.width, int(cx) + bw // 2),
                   min(full.height, int(cy) + int(bh * 0.28)))
            im = full.crop(box)
            im = im.resize((int(im.width * a.zoom), int(im.height * a.zoom)),
                           Image.LANCZOS)
            tiles.append((label, r["left"], im))
            print(f"  {label:<20} {r['left']:.1f}s left in the window")
        assert not errors, errors[:3]

    PAD, HEAD, GAP = 26, 58, 18
    W = PAD * 2 + sum(t[2].width for t in tiles) + GAP * (len(tiles) - 1)
    H = PAD * 2 + HEAD + max(t[2].height for t in tiles)
    sheet = Image.new("RGB", (W, H), (11, 10, 13))
    d = ImageDraw.Draw(sheet)
    d.text((PAD, PAD - 4), "THE HUNTER'S EYES — the shipped renderer, cropped "
           "to the caster. The pupils are looking at the quarry.",
           font=font(23), fill=(240, 232, 234))
    x = PAD
    for label, left, im in tiles:
        d.text((x, PAD + HEAD - 26), label, font=font(18), fill=(238, 226, 228))
        sheet.paste(im, (x, PAD + HEAD))
        x += im.width + GAP
    sheet.save(out_p)
    print(f"  wrote {out_p}  ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
