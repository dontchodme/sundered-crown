#!/usr/bin/env python3
"""THE SHAPE + PALETTE AUDIT, ON TWO SHEETS, AT 1:1.

`palette_probe.py` and `school_probe.py` produce numbers. Numbers are how you
choose what to try; they are not how you decide. Rule 7: *you cannot judge
legibility from a screenshot, a statistic, or a browser window* — and its v8
corollary, *pull a contact sheet at 1:1 before believing an effect works.*

Two sheets, because two separate questions are being asked and one sheet
answering both would be a sheet answering neither. §4 of the night plan:
"If the night produces more than a handful of things needing judgement, it has
produced work that cannot be judged."

  --marks     `audit-marks.png`
              warhammer and scythe, every school, BEFORE over AFTER.
              THE QUESTION: does a maker's mark read as a different weapon, or
              as the same weapon with a sticker on it? If it is a sticker, the
              §3.3 pattern — share the routine, bespoke one real detail — does
              not carry 48 cells and we should find that out on shape two, not
              shape eight.

  --dwarven   `audit-dwarven.png`
              every shape, against the pair that has been the worst in the game
              on all six shapes, plus the pair a fix could break.
              THE QUESTION: does dwarven still look like a SCHOOL, or has it
              just become the desaturated one? The score cannot see the
              difference; that is the whole reason this file exists.

Columns are rendered through the real SHAPES functions with the shadowBlur a
live weapon carries, because a weapon without its glow is not the picture
anybody watches.

DO NOT SCALE THESE TO JUDGE THEM.

  python3 audit_sheet.py --marks --dwarven
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib

from PIL import Image, ImageDraw

from scpage import game

SCHOOLS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral", "runic", "vigil"]
DIM = {
    "greatsword": (116, 40), "warhammer": (76, 54), "scythe": (104, 46),
    "twinblade": (62, 30), "bow": (54, 44), "flailHead": (96, 52),
}

# The two survivors of palette_sweep.py round 2, re-priced after --steel made
# the metal load-bearing. Both are bronze-cored; they differ in how cold and how
# dark the iron is. G keeps a little warmth in the metal, I does not.
# The combined fix. Every dwarven-only candidate reads on the sheet as "the
# duller one" rather than as a different school, because `core` drives the
# shadowBlur and both schools' cores stay warm. Moving BOTH ends of the pair --
# dwarven to bronze-on-iron, sanctified to white-hot -- separates them on VALUE,
# which is the axis this codebase has now learned three times actually survives
# phone size and motion. It also puts each school back on its own thesis: holy
# light is not gold leaf, and a forge is not a treasury.
PAIR_NEW = {
    "dwarven":    {"core": "#9C6326", "glow": "#E8A34E", "dark": "#2E1B0A", "steel": "#6A6E74"},
    "sanctified": {"core": "#FFF6E2", "glow": "#FFFFFF", "dark": "#5A4E30", "steel": "#FFFFFF"},
}

DWARVEN = {
    "SHIPPED": {"core": "#E0994A", "glow": "#FFD9A0", "dark": "#452710", "steel": "#C6CBD4"},
    "D bronze": {"core": "#9C6326", "glow": "#D99A4E", "dark": "#2E1B0A", "steel": "#8D8577"},
    "G warm iron": {"core": "#A2661F", "glow": "#F0A840", "dark": "#2A1B0C", "steel": "#7F7A6E"},
    "I cold iron": {"core": "#9C6326", "glow": "#E8A34E", "dark": "#2E1B0A", "steel": "#6A6E74"},
}

JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  /* AFFINITIES is a live object on the page and an override MUTATES it. Without
     this, column 3's override is still in force when the next row draws column
     1, and the "before" column silently becomes an "after" column from row two
     onward -- the first sheet showed a white sanctified in every NOW cell but
     the top one. Snapshot once, restore before every draw. This is v12's "do
     not compare builds on a field that is not the field you think it is",
     wearing a different hat. */
  if (!window.__AFF0){
    window.__AFF0 = {};
    for (const k in AC.AFFINITIES) window.__AFF0[k] = Object.assign({}, AC.AFFINITIES[k]);
  }
  for (const k in AC.AFFINITIES) Object.assign(AC.AFFINITIES[k], window.__AFF0[k]);
  for (const ov of cfg.overrides){
    if (AC.AFFINITIES[ov[0]]) AC.AFFINITIES[ov[0]][ov[1]] = ov[2];
  }
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;
  const p  = AC.AFFINITIES[cfg.aff];
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  c.fillStyle = "#0B0910"; c.fillRect(0,0,1080,1920);
  c.save();
  c.translate(cfg.ox, cfg.oy);
  c.scale(s, s);
  c.shadowColor = p.core; c.shadowBlur = 20;
  const fn = AC.SHAPES[cfg.shape];
  if (!fn) return null;
  if (cfg.shape === 'flailHead') fn(c, cfg.W, p, 0.5);
  else fn(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  return cv.toDataURL('image/png').slice(22);
}"""


# (width, height, origin-from-left, origin-from-top) per shape, in CANVAS px at
# scale ~2.03. Sized from each shape's real extents: the scythe reaches W*1.32
# ABOVE its origin and a fixed cell was cutting its crescent off, which is the
# exact failure mode rule 7's corollary warns about — an instrument aimed at the
# wrong part of the geometry.
CELL = {
    "greatsword": (300, 175, 0.15, 0.50), "warhammer": (300, 175, 0.22, 0.50),
    "scythe":     (300, 320, 0.15, 0.74), "twinblade":  (300, 175, 0.22, 0.50),
    "bow":        (300, 260, 0.42, 0.50), "flailHead":  (300, 260, 0.50, 0.50),
}


def cell(pg, shape, aff, ox, oy, tw, th, overrides=()):
    L, W = DIM[shape]
    png = pg.evaluate(JS, {"shape": shape, "aff": aff, "L": L, "W": W,
                           "ox": ox, "oy": oy, "overrides": [list(o) for o in overrides]})
    im = Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB")
    tw, th, fx, fy = CELL[shape]
    x0, y0 = int(ox - tw * fx), int(oy - th * fy)
    return im.crop((x0, y0, x0 + tw, y0 + th))


def grid(pg, rows, cols, out, title):
    """rows: [(label, shape, overrides)]  cols: [(label, aff, overrides)]"""
    GUT, TOP = 150, 34
    tw = max(CELL[s][0] for _, s, _ in rows)
    hs = [CELL[s][1] for _, s, _ in rows]
    sheet = Image.new("RGB", (GUT + tw * len(cols), TOP + sum(h + 20 for h in hs)),
                      (10, 8, 14))
    d = ImageDraw.Draw(sheet)
    d.text((10, 9), title + "   —   1:1, DO NOT SCALE THIS TO JUDGE IT",
           fill=(233, 213, 168))
    for ci, (clab, _, _) in enumerate(cols):
        d.text((GUT + ci * tw + 6, 22), clab.upper(), fill=(190, 180, 168))
    y = TOP
    for ri, (rlab, shape, rov) in enumerate(rows):
        th = CELL[shape][1]
        for line, ly in zip(rlab.split("|"), range(0, 99, 13)):
            d.text((8, y + th // 2 - 10 + ly), line, fill=(150, 142, 132))
        for ci, (_, aff, cov) in enumerate(cols):
            im = cell(pg, shape, aff, 700, 900, tw, th, list(rov) + list(cov))
            sheet.paste(im, (GUT + ci * tw, y))
        y += th + 20
    sheet.save(out)
    print(f"{out.name}  {sheet.size}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", default="sundered-crown-next.html")
    ap.add_argument("--after", default="sc-shape.html")
    ap.add_argument("--marks", action="store_true")
    ap.add_argument("--dwarven", action="store_true")
    ap.add_argument("--pair", action="store_true")
    ap.add_argument("--matrix", action="store_true",
                    help="the full 6x7 matrix IN COLOUR. The silhouette\n                          sheet is the blueprint; this is what the\n                          weapons actually look like, and the two had\n                          never been pulled side by side.")
    a = ap.parse_args()
    here = pathlib.Path(__file__).parent
    if not (a.marks or a.dwarven or a.pair or a.matrix):
        a.marks = a.dwarven = True

    if a.matrix:
        cols = [(s, s, []) for s in SCHOOLS]
        with game(game_path=(here / a.after).resolve()) as (pg, errs):
            rows = [(s, s, []) for s in
                    ["greatsword", "warhammer", "scythe", "twinblade",
                     "bow", "flailHead"]]
            grid(pg, rows, cols, here / "matrix-colour.png",
                 f"the full matrix, IN COLOUR — {a.after}")
            if errs:
                raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

    if a.pair:
        ov = [(s, f, v) for s, pal in PAIR_NEW.items() for f, v in pal.items()]
        cols = [("sanctified NOW", "sanctified", []),
                ("dwarven NOW", "dwarven", []),
                ("sanctified FIXED", "sanctified", ov),
                ("dwarven FIXED", "dwarven", ov)]
        with game(game_path=(here / a.after).resolve()) as (pg, errs):
            rows = [(s, s, []) for s in
                    ["warhammer", "scythe", "greatsword", "flailHead", "bow", "twinblade"]]
            grid(pg, rows, cols, here / "audit-pair.png",
                 "the worst pair in the game, before and after — "
                 "CIEDE2000 8.05 -> 16.5+")
            if errs:
                raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

    if a.marks:
        cols = [(s, s, []) for s in SCHOOLS]
        for tag, path in (("BEFORE", a.before), ("AFTER", a.after)):
            with game(game_path=(here / path).resolve()) as (pg, errs):
                rows = [(f"warhammer|{tag}", "warhammer", []),
                        (f"scythe|{tag}", "scythe", [])]
                grid(pg, rows, cols, here / f"audit-marks-{tag.lower()}.png",
                     f"maker's mark — {tag} ({path})")
                if errs:
                    raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

    if a.dwarven:
        cols = [("sanctified", "sanctified", []),
                ("dwarven SHIPPED", "dwarven", [("dwarven", f, v)
                                                for f, v in DWARVEN["SHIPPED"].items()]),
                ("dwarven D", "dwarven", [("dwarven", f, v)
                                          for f, v in DWARVEN["D bronze"].items()]),
                ("dwarven G", "dwarven", [("dwarven", f, v)
                                          for f, v in DWARVEN["G warm iron"].items()]),
                ("dwarven I", "dwarven", [("dwarven", f, v)
                                          for f, v in DWARVEN["I cold iron"].items()]),
                ("bloodsworn", "bloodsworn", [])]
        with game(game_path=(here / a.after).resolve()) as (pg, errs):
            rows = [(s, s, []) for s in
                    ["warhammer", "scythe", "greatsword", "flailHead", "bow", "twinblade"]]
            grid(pg, rows, cols, here / "audit-dwarven.png",
                 f"dwarven candidates on the fixed shapes — {a.after}")
            if errs:
                raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))
    print("\nsanctified is column 1 for a reason: it is the pair dwarven has lost "
          "to on\nall six shapes. bloodsworn is last because it is what a fix "
          "toward red breaks.")


if __name__ == "__main__":
    main()
