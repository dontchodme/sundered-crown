#!/usr/bin/env python3
"""THE CANDIDATE CELLS, PHOTOGRAPHED, BESIDE THE RELIC THEY WILL BE SEEN NEXT TO.

    python3 cand_strip.py --game ../02-chain/sc-bulwarden-frame.html

`cell_survey [3]` scores art with the PALETTE HELD, which is the right
instrument for "did the dispatch draw something else" and the wrong one for
"can a viewer tell these two apart in a fight" -- twice over:

  * in a fight the palettes are NOT held, and the school's colour is most of
    the read;
  * its nearest-sibling column ranks against all seven schools including the
    OPEN ones, so it can name a neighbour that does not exist. Three of the
    four cells here were reported nearest to a cell nobody has built.

So the neighbour is chosen among FILLED cells only, scored palette-held (the
dispatch question), and then both are drawn in their OWN colours (the fight
question). Nothing here is a verdict. It is a photograph, for a choice a table
cannot make.

Writes one PNG. Touches no build.
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

META_JS = """() => {
  const rep = {};
  for (const w of AC.WEAPONS) if (!rep[w.shape])
    rep[w.shape] = { D: w.reach, artW: w.artW };
  const filled = {};
  for (const w of AC.WEAPONS) filled[w.aff + "|" + w.shape] = w.name;
  return { rep, filled, schools: Object.keys(AC.AFFINITIES) };
}"""

# Palette HELD -- one school's colours, `key` the only thing that varies, so a
# differing pixel differs because the DISPATCH drew something else there.
NEAR_JS = """([shape, keys, D, artW, zoom, S, cx]) => {
  const draw = (palKey, hold) => {
    const cv = document.createElement("canvas");
    cv.width = S * zoom; cv.height = S * zoom;
    const c = cv.getContext("2d");
    c.scale(zoom, zoom); c.translate(S * cx, S / 2);
    const pal = hold
      ? Object.assign({}, AC.AFFINITIES.dwarven, { key: palKey })
      : AC.AFFINITIES[palKey];
    if (shape === "flail") AC.SHAPES.flailHead(c, artW, pal, 0.7);
    else AC.SHAPES[shape](c, D, artW, pal, 0.55);
    return { c, cv };
  };
  const ink = (palKey) => {
    const { c, cv } = draw(palKey, true);
    const d = c.getImageData(0, 0, cv.width, cv.height).data;
    const n = cv.width * cv.height, px = new Int32Array(n);
    let x0 = cv.width, y0 = cv.height, x1 = -1, y1 = -1;
    for (let p = 0; p < n; p++){
      const i = p << 2;
      if (d[i+3] > 24){
        px[p] = 1 + ((d[i] << 16) | (d[i+1] << 8) | d[i+2]);
        const yy = (p / cv.width) | 0, xx = p % cv.width;
        if (xx < x0) x0 = xx; if (xx > x1) x1 = xx;
        if (yy < y0) y0 = yy; if (yy > y1) y1 = yy;
      }
    }
    return { px, box: [x0, y0, x1, y1] };
  };
  const shots = {}; for (const k of keys) shots[k] = ink(k);
  const cmp = (A, B) => {
    let u = 0, dd = 0; const a = A.px, b = B.px;
    for (let p = 0; p < a.length; p++){ const x = a[p], y = b[p];
      if (x || y){ u++; if (x !== y) dd++; } }
    return u ? dd / u : 0;
  };
  const M = {}; for (const k of keys) if (k !== keys[0]) M[k] = cmp(shots[keys[0]], shots[k]);
  const boxes = {}; for (const k of keys) boxes[k] = shots[k].box;
  return { m: M, boxes, w: shots[keys[0]].px.length / (S * zoom), W: S * zoom };
}"""

DRAW_JS = """([shape, palKey, D, artW, zoom, S, cx]) => {
  const cv = document.createElement("canvas");
  cv.width = S * zoom; cv.height = S * zoom;
  const c = cv.getContext("2d");
  c.scale(zoom, zoom); c.translate(S * cx, S / 2);
  if (shape === "flail") AC.SHAPES.flailHead(c, artW, AC.AFFINITIES[palKey], 0.7);
  else AC.SHAPES[shape](c, D, artW, AC.AFFINITIES[palKey], 0.55);
  return cv.toDataURL("image/png");
}"""


def fit(page, shape, keys, D, aw, zoom):
    """Grow the canvas until no school's ink touches an edge.

    `_artBox`'s own comment says reach and artW predict a greatsword's box and
    lie about a bow's; cell_survey learned the same thing the expensive way,
    having scored a whole row against a crop.
    """
    S = int(aw * 3.0) if shape == "flail" else int(D * 1.9)
    cx, tries = 0.55, 0
    while True:
        r = page.evaluate(NEAR_JS, [shape, keys, D, aw, zoom, S, cx])
        bx = list(r["boxes"].values())
        W = r["W"]
        clip = any(b[0] <= 0 or b[1] <= 0 or b[2] >= W - 1 or b[3] >= W - 1 for b in bx)
        if not clip or tries >= 6:
            return r, S, cx, clip
        if any(b[2] >= W - 1 for b in bx):
            cx = max(0.18, cx - 0.12)
        if any(b[0] <= 0 for b in bx):
            cx = min(0.85, cx + 0.12)
        S = int(S * 1.35)
        tries += 1


def grab(page, shape, key, D, aw, zoom, S, cx, pad=10):
    url = page.evaluate(DRAW_JS, [shape, key, D, aw, zoom, S, cx])
    im = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGBA")
    bb = im.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad),
                    min(im.width, x1 + pad), min(im.height, y1 + pad)))


def font(sz, bold=True):
    for p in (HERE / "fonts" / ("AtkinsonHyperlegibleNext-Bold.ttf" if bold
                                else "AtkinsonHyperlegibleNext-Regular.ttf"),
              pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
              pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")):
        if p.exists():
            try:
                return ImageFont.truetype(str(p), sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--cells", default="runic:flail,umbral:scythe,"
                                       "verdant:twinblade,bloodsworn:bow")
    ap.add_argument("--zoom", type=int, default=5)
    ap.add_argument("--cap", type=int, default=430, help="max panel px")
    ap.add_argument("--out", default="../05-reference/v42/candidates.png")
    a = ap.parse_args()

    cells = [tuple(c.split(":")) for c in a.cells.split(",")]
    gp = (HERE / a.game).resolve()
    out = (HERE / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    panels = []
    with game(game_path=gp) as (page, errors):
        meta = page.evaluate(META_JS)
        rep, filled, schools = meta["rep"], meta["filled"], meta["schools"]
        for aff, shape in cells:
            assert (aff + "|" + shape) not in filled, f"{aff}x{shape} is not open"
            sibs = [s for s in schools if s != aff and (s + "|" + shape) in filled]
            D, aw = rep[shape]["D"], rep[shape]["artW"]
            r, S, cx, clip = fit(page, shape, [aff] + sibs, D, aw, a.zoom)
            near = min(r["m"], key=lambda k: r["m"][k])
            me = grab(page, shape, aff, D, aw, a.zoom, S, cx)
            you = grab(page, shape, near, D, aw, a.zoom, S, cx)
            panels.append({"aff": aff, "shape": shape, "sib": near,
                           "sibName": filled[near + "|" + shape],
                           "diff": r["m"][near], "clip": clip,
                           "n": len(sibs), "me": me, "you": you})
            print(f"  {aff:11}x {shape:11} nearest FILLED sibling "
                  f"{filled[near+'|'+shape]:13}({near}) {r['m'][near]*100:5.1f}%"
                  f"   of {len(sibs)}   fit={'n' if clip else 'y'}")
        assert not errors, errors[:3]

    for p in panels:                       # one scale for the pair, or the
        k = min(1.0, a.cap / max(p["me"].width, p["me"].height,   # comparison
                                 p["you"].width, p["you"].height))  # is a lie
        if k < 1.0:
            for f in ("me", "you"):
                im = p[f]
                p[f] = im.resize((max(1, int(im.width * k)),
                                  max(1, int(im.height * k))), Image.LANCZOS)

    PAD, GAP, HEAD, SUB = 34, 30, 52, 30
    cw = max(max(p["me"].width, p["you"].width) for p in panels)
    ch = max(p["me"].height for p in panels)
    ch2 = max(p["you"].height for p in panels)
    W = PAD * 2 + len(panels) * cw + (len(panels) - 1) * GAP
    H = PAD * 2 + HEAD + SUB + ch + 26 + SUB + ch2
    sheet = Image.new("RGBA", (W, H), (13, 14, 18, 255))
    d = ImageDraw.Draw(sheet)
    fb, fs, ft = font(26), font(19), font(16, bold=False)

    d.text((PAD, PAD - 6), "THE OPEN CELLS ON OFFER — in their own colours, above "
           "the SHIPPED relic on that type they sit closest to", font=fb,
           fill=(238, 238, 242, 255))

    for i, p in enumerate(panels):
        x = PAD + i * (cw + GAP)
        y = PAD + HEAD
        d.text((x, y), f"{p['aff'].upper()} × {p['shape'].upper()}", font=fs,
               fill=(232, 232, 238, 255))
        y += SUB
        sheet.alpha_composite(p["me"], (x + (cw - p["me"].width) // 2,
                                        y + (ch - p["me"].height) // 2))
        y2 = y + ch + 26
        d.text((x, y2), f"nearest of {p['n']} shipped:  {p['sibName']}"
                        f"   {p['diff']*100:.0f}% apart", font=ft,
               fill=(150, 152, 162, 255))
        sheet.alpha_composite(p["you"], (x + (cw - p["you"].width) // 2, y2 + SUB))

    sheet.convert("RGB").save(out)
    print(f"wrote {out}  {sheet.width}x{sheet.height}")


if __name__ == "__main__":
    main()
