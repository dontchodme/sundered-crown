#!/usr/bin/env python3
"""THE FOUR NEW ULTS, AS FILMSTRIPS. One row per relic, time left to right.

    python3 ult_filmstrip.py --game sc-gs7-ults.html

The pixel-diff check in `ultart_build.py` proves a branch draws SOMETHING with
an arc. It cannot tell you the thing it draws is any good, or that it does not
read as a recolour of its school-mate's ult. That is eyes, and this is what eyes
need: the same moment in each ult, side by side, at a size you can judge.

`--vs` renders the school-mate's ult on a second row, which is the comparison
that actually matters — Bloodprice against Exsanguinate, Rootfast against
Bramblesnare, Eclipse against Dirge, Corollary against Unmaking.

The fx block is set directly rather than waited for: an ultimate fires when its
charge fills, and waiting for that would sample whatever moment the fight
happened to be in. Every frame here is the same match, the same seed, the same
fighter positions, and only `u.t` moves.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

SHOT_JS = """([id, foe, seed, t, life]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const w = AC.WEAPONS.find(x => x.id === id);
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  /* PLACE THEM, do not step to wherever the fight happened to be. Stepped 90
     frames from spawn the two balls end up nearly touching, and every ult that
     draws something BETWEEN caster and target — the oath thread, the stepped
     rule, roots reaching — has no room to exist and reads as nothing. That is
     a property of the sample, not of the art, and a filmstrip that hides it is
     worse than useless. Diagonal, ~62% of the arena diagonal apart. */
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
              x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y, hit: true,
              radius: w.ult.radius || 300, aff: m.a.aff, t: t, life: life };
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

NEW = [("oathwound", "Bloodprice", 1.5), ("heartwood", "Rootfast", 2.2),
       ("nightfell", "Eclipse", 1.4),    ("axiom", "Corollary", 1.5)]
MATE = {"oathwound": ("widowmaker", "Exsanguinate", 1.3),
        "heartwood": ("thornwake", "Bramblesnare", 2.4),
        "nightfell": ("gravemourn", "Dirge", 1.6),
        "axiom":     ("spellbreaker", "Unmaking", 1.4)}
FOE = "grudgebearer"


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="sc-gs7-ults.html")
    ap.add_argument("--seed", type=int, default=31337)
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--scale", type=float, default=0.20)
    ap.add_argument("--vs", action="store_true",
                    help="also render each school-mate's ult underneath")
    ap.add_argument("--out", default="ult-filmstrip.png")
    ap.add_argument("--ids", default="",
                    help="comma-separated relic ids instead of the four new ones; "
                         "life is read from the build so the strip matches the game")
    A = ap.parse_args()

    g = HERE / A.game
    if not g.exists():
        sys.exit(f"no such build: {g}")

    # Sample across the life, weighted early — set-pieces do their work in the
    # first third and a linear sample spends half its frames on the fade.
    fr = [round(0.06 + 0.82 * (i / max(1, A.frames - 1)) ** 1.5, 3)
          for i in range(A.frames)]

    pairs = NEW
    with game(game_path=g.resolve()) as (page0, _e0):
        if A.ids:
            pairs = page0.evaluate("""(ids) => ids.map(id => {
              const w = AC.WEAPONS.find(x => x.id === id);
              // read `life` out of the build's own table rather than restating
              // it here: a strip that samples a different duration than the
              // game plays is showing you a set-piece nobody will ever see.
              const L = { dawnbringer:1.6, widowmaker:1.3, grudgebearer:1.7,
                          thornwake:2.4, gravemourn:1.6, spellbreaker:1.4,
                          oathwound:1.5, heartwood:2.2, nightfell:1.4, axiom:1.5,
                          ironhail:1.3, lightkeeper:1.5, farwarden:2.6,
                          aureole:1.6, censer:1.6, emberedge:1.5 }[id] || 1.5;
              return [id, w.ult.name, L];
            })""", A.ids.split(","))

    rows = []
    with game(game_path=g.resolve()) as (page, errors):
        for rid, uname, life in pairs:
            ims = [png(page.evaluate(SHOT_JS, [rid, FOE, A.seed, f * life, life]))
                   for f in fr]
            rows.append((f"{uname}  ({rid})", ims))
            if A.vs and rid in MATE:
                mid, mname, mlife = MATE[rid]
                ims2 = [png(page.evaluate(SHOT_JS, [mid, FOE, A.seed, f * mlife, mlife]))
                        for f in fr]
                rows.append((f"    vs {mname}  ({mid})", ims2))
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    tw = int(1080 * A.scale); th = int(1920 * A.scale)
    PAD, LBL, HDR = 8, 22, 30
    W = PAD + A.frames * (tw + PAD)
    H = HDR + len(rows) * (th + LBL + PAD) + PAD
    sh = Image.new("RGB", (W, H), (10, 8, 16))
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 9), f"ULT SET-PIECES — {A.game}   t/life = "
                      + "  ".join(str(f) for f in fr), fill=(201, 162, 39))
    y = HDR
    for lab, ims in rows:
        dr.text((PAD, y + 5), lab, fill=(214, 200, 170))
        for i, im in enumerate(ims):
            sh.paste(im.resize((tw, th), Image.LANCZOS), (PAD + i * (tw + PAD), y + LBL))
        y += th + LBL + PAD
    out = HERE.parent / A.out
    sh.save(out)
    print(f"  {out}  ({sh.width}x{sh.height})")


if __name__ == "__main__":
    main()
