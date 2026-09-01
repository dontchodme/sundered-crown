#!/usr/bin/env python3
"""WHAT THE FOUR CANDIDATE CELLS ACTUALLY LOOK LIKE, next to the sibling the
ink-mask column says they are closest to.

cell_survey's diff % is measured on a colour-stripped ink mask with ONE palette
held for every school, which is the right way to ask "is the outline its own
shape" and the wrong way to ask "does this read as a different weapon on
screen" — v58. This draws each candidate in its OWN school's palette beside its
nearest sibling in that sibling's palette, which is how a viewer meets them.
"""
import argparse, base64, pathlib, sys
from PIL import Image, ImageDraw
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--game", required=True)
ap.add_argument("--pairs", required=True, help="aff:type:sibling,...")
ap.add_argument("--out", default="/tmp/cand-art.png")
a = ap.parse_args()
sys.path.insert(0, str(pathlib.Path(a.repo) / "tools"))
from scpage import game

JS = r"""([shape, palKey, S, zoom, cx, artW, D]) => {
  const cv = document.createElement("canvas");
  cv.width = S*zoom; cv.height = S*zoom;
  const c = cv.getContext("2d");
  c.scale(zoom, zoom); c.translate(S*cx, S/2);
  const pal = AC.AFFINITIES[palKey];
  if (shape === "flail") AC.SHAPES.flailHead(c, artW, pal, 0.7);
  else AC.SHAPES[shape](c, D, artW, pal, 0.55);
  return cv.toDataURL("image/png");
}"""
SHAPE_D = {"greatsword":116,"twinblade":92,"warhammer":96,"scythe":104,"flail":90,"bow":110}
SHAPE_W = {"greatsword":40,"twinblade":30,"warhammer":54,"scythe":46,"flail":34,"bow":38}
pairs = [p.split(":") for p in a.pairs.split(",")]
S, ZOOM = 300, 2
tiles = []
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    for aff, typ, sib in pairs:
        row = []
        for k in (aff, sib):
            u = page.evaluate(JS, [typ, k, S, ZOOM, 0.30, SHAPE_W[typ], SHAPE_D[typ]])
            row.append(Image.open(__import__("io").BytesIO(
                base64.b64decode(u.split(",", 1)[1]))).convert("RGBA"))
        tiles.append((f"{aff} x {typ}", f"{sib} x {typ}", row))
    assert not errors, errors
W = S*ZOOM; H = S*ZOOM
sheet = Image.new("RGBA", (W*2 + 60, (H + 46)*len(tiles) + 20), (16, 16, 20, 255))
d = ImageDraw.Draw(sheet)
for i, (na, nb, (ia, ib)) in enumerate(tiles):
    y = 20 + i*(H + 46)
    sheet.alpha_composite(ia, (20, y)); sheet.alpha_composite(ib, (W + 40, y))
    d.text((20, y + H + 8), na.upper() + "   <- the candidate", fill=(235, 235, 240))
    d.text((W + 40, y + H + 8), nb.upper() + "   nearest sibling", fill=(150, 150, 160))
sheet.convert("RGB").save(a.out)
print("wrote", a.out, sheet.size)
