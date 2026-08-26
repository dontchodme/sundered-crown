#!/usr/bin/env python3
"""SHOW ME THE NEW FIGHTERS. Fight cards and in-arena stills, in colour.

    python3 newrelic_sheet.py --game sc-gs7.html

The silhouette sheet answers "are these outlines distinct" and nothing else —
it is colour-stripped by design. This answers the question that decides whether
a relic stays: what does it look like on screen, next to something familiar.

Two sheets:

  newrelics-cards.png   the v2 fight card mid-hold, one per new relic, each
                        paired against Dawnbringer. Art, name, school colour,
                        the tale of the tape, the status line and the ultimate
                        — everything the viewer is told, at 1080x1920.

  newrelics-arena.png   the same four mid-fight, weapon lit and swinging, so
                        the art is judged the way it is actually seen rather
                        than posed on a card.

Frames are pinned (`new AC.Match(a, b, seed)`, fixed step count, `introT` set
directly) so re-running this compares like with like.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
W, H = 1080, 1920

CARD_JS = """([a, b, seed, e]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = Math.max(0, AC.CONFIG.intro.dur - e);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

ARENA_JS = """([a, b, seed, steps]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  for (let i = 0; i < steps; i++) m.step(1 / 60);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

NEW = [("oathwound", "Oathwound", "bloodsworn"),
       ("heartwood", "Heartwood", "verdant"),
       ("nightfell", "Nightfell", "umbral"),
       ("axiom",     "Axiom",     "runic")]
FOIL = "dawnbringer"


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def contact(sheet_imgs, label_rows, out, scale, title):
    cols = len(sheet_imgs)
    tw = int(W * scale); th = int(H * scale)
    PAD, LBL = 16, 34
    sh = Image.new("RGB", (cols * (tw + PAD) + PAD, th + PAD * 2 + LBL), (12, 10, 18))
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 8), title, fill=(201, 162, 39))
    for i, (im, lab) in enumerate(zip(sheet_imgs, label_rows)):
        x = PAD + i * (tw + PAD)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, PAD + LBL))
        dr.text((x + 2, PAD + LBL - 15), lab, fill=(214, 200, 170))
    sh.save(out)
    print(f"  {out}  ({sh.width}x{sh.height})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="sc-gs7.html")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--hold", type=float, default=2.2,
                    help="seconds elapsed into the 4s intro — mid-hold by default")
    ap.add_argument("--steps", type=int, default=150,
                    help="sim steps for the arena still (150 = 2.5s in)")
    ap.add_argument("--scale", type=float, default=0.30)
    A = ap.parse_args()

    g = HERE / A.game
    if not g.exists():
        sys.exit(f"no such build: {g}")

    cards, arenas, labels = [], [], []
    with game(game_path=g.resolve()) as (page, errors):
        for rid, name, school in NEW:
            cards.append(png(page.evaluate(CARD_JS, [rid, FOIL, A.seed, A.hold])))
            arenas.append(png(page.evaluate(ARENA_JS, [rid, FOIL, A.seed, A.steps])))
            labels.append(f"{name}  ({school})  v Dawnbringer")
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    contact(cards, labels, HERE.parent / "newrelics-cards.png", A.scale,
            f"THE FIGHT CARD — {A.game}, {A.hold}s into the intro")
    contact(arenas, labels, HERE.parent / "newrelics-arena.png", A.scale,
            f"MID-FIGHT — {A.game}, {A.steps} steps in, seed {A.seed}")


if __name__ == "__main__":
    main()
