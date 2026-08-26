"""AXIOM AT SIZE — render the runic greatsword large, at several clock phases.

Not a check. A pair of eyes. The weapon ships at L=122, W=40 and is on screen
for a few frames at a time while spinning, so nobody has ever looked at the
fracture geometry itself. This draws it at 6x on a dark ground, at five values
of `SHAPES._t` across the drift period, plus one strip at true game size for
the honest read.

    python3 axiom_shot.py --src ../02-chain/sc-cardspin.html --out /home/claude/out/axiom-now.png
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent

SHOT = """([shape, aff, L, W, S, t, k]) => {
  const cv = document.createElement('canvas');
  cv.width = Math.round(L * S * 1.30);
  cv.height = Math.round(W * S * 3.2);
  const c = cv.getContext('2d');
  c.fillStyle = '#0B0910'; c.fillRect(0, 0, cv.width, cv.height);
  AC.SHAPES._t = t;
  c.save();
  c.translate(W * S * 0.55, cv.height / 2);
  c.scale(S, S);
  const p = AC.AFFINITIES[aff];
  const fn = AC.SHAPES[shape];
  fn(c, L, W, p, k, aff);
  c.restore();
  return cv.toDataURL('image/png').slice(22);
}"""


def png(b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="/home/claude/out/axiom-now.png")
    ap.add_argument("--shape", default="greatsword")
    ap.add_argument("--aff", default="runic")
    ap.add_argument("--scale", type=float, default=6.0)
    A = ap.parse_args()

    src = (HERE / A.src).resolve() if not pathlib.Path(A.src).is_absolute() else pathlib.Path(A.src)
    if not src.exists():
        print(f"! missing {src}")
        return 2

    L, W = 122, 40
    phases = [0.0, 0.9, 1.8, 2.7, 3.6]

    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--no-sandbox"])
        pg = br.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(src.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
        big = [png(pg.evaluate(SHOT, [A.shape, A.aff, L, W, A.scale, t, 0.5])) for t in phases]
        small = [png(pg.evaluate(SHOT, [A.shape, A.aff, L, W, 1.0, t, 0.5])) for t in phases]
        br.close()

    if errs:
        print("! page errors:", errs[:3])

    bw, bh = big[0].size
    sw, sh = small[0].size
    pad = 10
    sheet = Image.new("RGB", (bw, bh * len(big) + pad + sh + pad), "#141018")
    for i, im in enumerate(big):
        sheet.paste(im, (0, i * bh))
    y = bh * len(big) + pad
    for i, im in enumerate(small):
        sheet.paste(im, (i * (sw + 8), y + (sh // 2)))

    out = pathlib.Path(A.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"  {out}  {sheet.size[0]}x{sheet.size[1]}  phases {phases}  scale {A.scale}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
