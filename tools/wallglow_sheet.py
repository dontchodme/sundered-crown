#!/usr/bin/env python3
"""EYES ON THE CORNERS. The one thing the numbers were never going to settle.

    python3 wallglow_sheet.py

NEXT-SESSION §3 said replacing the closing-wall glow "changes how the corners
look, so it needs eyes." This renders the corner, at the collapse, from each
candidate, at 1:1 and at 4x, plus a signed error map so a difference too small
to see is still visible somewhere.

The error map is amplified 12x and centred on grey: red means the candidate is
BRIGHTER than the shipped glow, blue means dimmer. Flat grey is agreement.
"""
from __future__ import annotations
import base64, io, pathlib, sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
W, H = 1080, 1920
SEED, INSET = 424242, 64.0
A, B = "dawnbringer", "grudgebearer"

FRAME = r"""
([a, b, seed, inset, w, h]) => {
  AC.setResolution(w, h);
  const m = new AC.Match(a, b, seed);
  m.inset = inset;
  AC.__draw(m);
  return document.querySelector("canvas").toDataURL("image/png");
}
"""

BUILDS = [("shipped  shadowBlur 30", "sundered-crown.html"),
          ("buffer   D=4",           "sc-wall.html"),
          ("strips   §3's proposal", "sc-wall-strips.html")]


def _png(d):
    im = Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")
    return np.asarray(im).astype(np.int16)


def shot(path):
    """Return (frame at inset, frame with the walls open). The second is what
    makes the corner findable: the arena's own gold frame is brighter and more
    contrasty than the wall glow, so anything that hunts for 'the strongest
    edge' in a finished frame locks onto the frame corner at (35, 30) and
    crops a picture of the wrong thing. Differencing removes everything that
    is not the walls."""
    with game(game_path=path) as (page, errors):
        page.evaluate(FRAME, [A, B, SEED, INSET, W, H])   # warm
        lit = _png(page.evaluate(FRAME, [A, B, SEED, INSET, W, H]))
        dark = _png(page.evaluate(FRAME, [A, B, SEED, 0.0, W, H]))
        if errors:
            sys.exit(f"{path.name}: {errors[:2]}")
    return lit, dark


def main():
    imgs = []
    for label, name in BUILDS:
        p = HERE / name
        if not p.exists():
            sys.exit(f"missing build: {name}")
        lit, dark = shot(p)
        imgs.append((label, lit, dark))

    ref = imgs[0][1]
    refdiff = np.abs(imgs[0][1] - imgs[0][2])
    # MEAN across the other axis, not max. The left and right wall lines are
    # equally bright in EVERY row, so a per-row max is that same value at every
    # y and argmax picks a row essentially at random — it returned y=900, which
    # is nowhere near the top wall. A full-width horizontal line moves the row
    # MEAN; a single vertical line barely does.
    top = int(np.argmax(refdiff.mean(axis=(1, 2))[: H // 2]))
    left = int(np.argmax(refdiff.mean(axis=(0, 2))[: W // 2]))
    S = 150
    y0, x0 = max(0, top - S // 2), max(0, left - S // 2)
    print(f"corner at ({left}, {top}), cropping {S}x{S} from ({x0}, {y0})")

    ZOOM, PAD, LBL = 4, 14, 26
    cw = S * ZOOM
    cols = len(imgs) + 2                       # +2 error maps
    sheet = Image.new("RGB", (cols * (cw + PAD) + PAD,
                              cw + PAD * 2 + LBL), (14, 12, 20))
    dr = ImageDraw.Draw(sheet)

    panels = [(lbl, np.clip(im[y0:y0 + S, x0:x0 + S], 0, 255).astype(np.uint8))
              for lbl, im, _ in imgs]
    for lbl, im, _ in imgs[1:]:
        err = (im[y0:y0 + S, x0:x0 + S] - ref[y0:y0 + S, x0:x0 + S])
        amp = np.clip(128 + err * 12, 0, 255).astype(np.uint8)
        panels.append((f"err x12  {lbl.split()[0]}", amp))

    for i, (lbl, arr) in enumerate(panels):
        tile = Image.fromarray(arr).resize((cw, cw), Image.NEAREST)
        x = PAD + i * (cw + PAD)
        sheet.paste(tile, (x, PAD + LBL))
        dr.text((x + 2, PAD + 6), lbl, fill=(214, 200, 170))

    out = HERE.parent / "wallglow-corners.png"
    sheet.save(out)
    print(f"wrote {out}  ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
