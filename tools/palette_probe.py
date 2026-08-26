#!/usr/bin/env python3
"""WHO OWNS THE PIXELS? — per-shape accounting of every palette field.

WHY THIS EXISTS
---------------
`sundered-crown-night-plan.md` §1 found that the three palette rows in
`palette-sheet.png` are pixel-indistinguishable on scythe, twinblade, bow and
flailHead, and concluded that the matrix doc's "six hex values improves every
one of 48 cells" is false. That is a correct reading of the sheet, but the sheet
answers the question with an EYE. §1.4 then sets the real job:

    "Make `steel` load-bearing before trusting a material palette."

You cannot do that without knowing, per shape, what fraction of the weapon each
field actually paints. This is that number.

METHOD
------
For each shape, render it once as a baseline, then once per palette field with
ONLY that field swapped to a wildly out-of-gamut colour. Count the pixels that
moved. Express each field's count as a share of the weapon's total ink.

The residue is the finding: **ink that no field controls** is hardcoded in the
shape function and is therefore byte-identical in all 48 cells. That is the
same disease as the dwarven chevron, measured instead of eyeballed.

Two passes, because they answer different questions:

    --no-glow   the shape's own ink. What the ART is made of.
    (default)   with the shadowBlur the live renderer puts on a weapon. What a
                VIEWER sees. `core` will dominate here and that is exactly
                §1.2's "it collapses to the glow, and the glow separates".

TRAPS THIS AVOIDS
-----------------
* A field can be read into a gradient stop and still move almost nothing. Only
  counting pixels catches that; reading the source does not.
* Two fields can paint the SAME pixels (a fill then an edge over it). Shares
  therefore do not have to sum to 100, and the script says so rather than
  normalising and lying.
* Alpha-suffixed reads (`p.core + "77"`) still register, because the swap
  changes the RGB under the alpha.

  python3 palette_probe.py --game sundered-crown-next.html
  python3 palette_probe.py --no-glow --shapes greatsword,warhammer
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib

import numpy as np
from PIL import Image

from scpage import game

# reach / artW lifted from the relic that owns each shape
DIM = {
    "greatsword": (116, 40), "warhammer": (76, 54), "scythe": (104, 46),
    "twinblade": (62, 30), "bow": (54, 44), "flailHead": (96, 52),
    "daggers": (56, 30), "runeblade": (70, 30),
}

# Out-of-gamut markers, far from each other AND from every real palette value,
# so a moved pixel is unambiguous. Never shipped; runtime only.
PROBE = "#FF00FF"
FIELDS = ["steel", "core", "glow", "dark"]

BG = (11, 9, 16)

JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;
  const p  = Object.assign({}, AC.AFFINITIES[cfg.aff]);
  if (cfg.field) p[cfg.field] = cfg.probe;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over';
  c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  c.fillStyle = "#0B0910"; c.fillRect(0,0,1080,1920);
  c.save();
  c.translate(cfg.ox, cfg.oy);
  c.scale(s, s);
  if (cfg.glow){ c.shadowColor = p.core; c.shadowBlur = 20; }
  const fn = AC.SHAPES[cfg.shape];
  if (!fn) return null;
  if (cfg.shape === 'flailHead') fn(c, cfg.W, p, 0.5);
  else fn(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  return cv.toDataURL('image/png').slice(22);
}"""


def shot(pg, **cfg) -> Image.Image:
    png = pg.evaluate(JS, cfg)
    if png is None:
        raise SystemExit(f"SHAPES.{cfg['shape']} does not exist in this build")
    return Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB")


def arr(im: Image.Image) -> np.ndarray:
    return np.asarray(im, dtype=np.int16)


def moved(a: np.ndarray, b: np.ndarray, thresh: int = 8) -> np.ndarray:
    """Boolean mask where b differs from a by more than `thresh` in any channel."""
    return np.abs(a - b).max(axis=-1) > thresh


def ink_of(a: np.ndarray, thresh: int = 8) -> np.ndarray:
    return np.abs(a - np.array(BG, dtype=np.int16)).max(axis=-1) > thresh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sundered-crown-next.html")
    ap.add_argument("--shapes", default="greatsword,warhammer,scythe,twinblade,bow,flailHead")
    ap.add_argument("--aff", default="dwarven",
                    help="school to probe through; the accounting is the same in any")
    ap.add_argument("--no-glow", action="store_true",
                    help="measure the shape's own ink, without the renderer's shadow")
    a = ap.parse_args()

    here = pathlib.Path(__file__).parent
    shapes = [s.strip() for s in a.shapes.split(",") if s.strip()]
    glow = not a.no_glow
    # A generous window around the draw origin. It MUST be sized in CANVAS
    # pixels, not shape units: the renderer draws at AC.renderer.scale (~2.03 at
    # 1080x1920), so a box of L+pad clips every shape at half its length and
    # silently over-weights whatever is near the grip. Caught by dumping a diff
    # mask and finding the ink bounding box flush against the crop edge.
    ox, oy, pad = 700, 900, 30

    print(f"=== who owns the pixels — {a.game}, school={a.aff}, "
          f"{'WITH renderer glow' if glow else 'shape ink only'} ===")
    print(f"{'shape':<12}{'ink':>8}  " + "".join(f"{f:>10}" for f in FIELDS)
          + f"{'UNOWNED':>10}")

    rows = []
    with game(game_path=(here / a.game).resolve()) as (pg, errs):
        scale = pg.evaluate("()=>{AC.setResolution(1080,1920);return AC.renderer.scale;}")
        for shape in shapes:
            L, W = DIM.get(shape, (100, 40))
            base = shot(pg, shape=shape, aff=a.aff, L=L, W=W, ox=ox, oy=oy,
                        glow=glow, field=None, probe=PROBE)
            # crop tight around the draw so the scan is over thousands of px, not 2M
            r = L * scale * 1.45 + pad
            box = (int(ox - r), int(oy - r), int(ox + r), int(oy + r))
            base = arr(base.crop(box))
            ink = ink_of(base)
            owned = np.zeros_like(ink)
            shares = {}
            for f in FIELDS:
                im = arr(shot(pg, shape=shape, aff=a.aff, L=L, W=W, ox=ox, oy=oy,
                              glow=glow, field=f, probe=PROBE).crop(box))
                m = moved(base, im)
                shares[f] = m
                owned |= m
            nink = int(ink.sum())
            unowned = int((ink & ~owned).sum())
            rows.append((shape, nink, shares, unowned))
            pct = lambda n: (100.0 * n / nink) if nink else 0.0
            print(f"{shape:<12}{nink:>8}  "
                  + "".join(f"{pct(int(shares[f].sum())):>9.1f}%" for f in FIELDS)
                  + f"{pct(unowned):>9.1f}%")
        if errs:
            raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

    print("\nShares overlap (a fill then a lit edge over it), so they need not sum "
          "to 100.\nUNOWNED is ink no palette field can move: identical in all 48 "
          "cells, by construction.")
    worst = sorted(rows, key=lambda r: -r[3])[:3]
    print("\nmost hardcoded: " + ", ".join(
        f"{s} {100.0*u/max(1,i):.0f}%" for s, i, _, u in worst))
    thin = [s for s, i, sh, _ in rows if i and 100.0 * int(sh["steel"].sum()) / i < 10.0]
    if thin:
        print(f"steel paints <10% of the ink on: {', '.join(thin)}")


if __name__ == "__main__":
    main()
