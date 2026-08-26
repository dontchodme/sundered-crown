#!/usr/bin/env python3
"""THE CONVERSE, PHOTOGRAPHED. The trail and the reversal, on one seed.

    python3 foregone_strip.py --game ../02-chain/sc-foregone.html

FULL-HALL frames, deliberately, where `flail_strip` crops. The spike storm was
a 52px head in a 520x800 room and a full frame at strip scale showed a red dot;
this ultimate IS the room -- a line laid across the whole floor is the thing to
look at, and cropping it would photograph the one part that does not matter.

TWO PASSES. The reversal begins on a fixed clock, but `hitStop` does not
advance it, so the wall-frame the turn lands on varies with how hard the caster
is being hit. Pass one steps until the phase flips and records the frame index;
pass two replays the same seed -- replay is exact, the seed IS the fight -- and
captures at turn + offset. Offsets measured from `fireUlt` would land somewhere
different every seed and the strip would be photographing the variance.

Writes PNGs into 05-reference/v39. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v39"
RID = "foregone"

# Frames as a fraction of the LAY phase, then seconds after the turn.
LAY_AT = [0.04, 0.34, 0.66, 0.99]
TRACE_AT = [0.10, 0.38, 0.70, 1.02]

FIND_JS = """([id, foe, seed, warm]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  let n = 0, cast = -1, turn = -1, end = -1;
  while (n < 30 / DT && !m.over){
    m.step(DT); n++;
    const S = me.ultTrace;
    if (S && cast < 0) cast = n;
    if (S && S.phase === "trace" && turn < 0) turn = n;
    if (!S && turn > 0){ end = n; break; }
  }
  return { cast, turn, end, warm };
}"""

CAP_JS = """([id, foe, seed, warm, at]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  for (let i = 0; i < at && !m.over; i++) m.step(DT);
  AC.__draw(m);
  const S = me.ultTrace;
  return { png: document.getElementById('cv').toDataURL('image/png'),
           phase: S ? S.phase : "-", orbs: S ? S.orbs.length : 0,
           blooms: S ? S.blooms : -1, hp: Math.round(me.hp),
           foeHp: Math.round((me === m.a ? m.b : m.a).hp) };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=337)
    ap.add_argument("--warm", type=float, default=6.0)
    ap.add_argument("--scale", type=float, default=0.30)
    ap.add_argument("--out", default="foregone-strip.png")
    a = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    gp = (HERE / a.game).resolve()

    with game(game_path=gp) as (page, errors):
        f = page.evaluate(FIND_JS, [RID, a.foe, a.seed, a.warm])
        if f["turn"] < 0:
            raise SystemExit(f"no reversal on this seed: {f}")
        dt = 1 / 120
        print(f"\n  cast at frame {f['cast']}, turn at {f['turn']} "
              f"(+{(f['turn'] - f['cast']) * dt:.2f}s), "
              f"ends at {f['end']} (+{(f['end'] - f['turn']) * dt:.2f}s)")

        want = ([(int(f["cast"] + (f["turn"] - f["cast"]) * k), f"lay {k:.0%}")
                 for k in LAY_AT]
                + [(int(f["turn"] + s / dt), f"reversal +{s:.2f}s")
                   for s in TRACE_AT])
        shots = []
        for n, lab in want:
            r = page.evaluate(CAP_JS, [RID, a.foe, a.seed, a.warm, n])
            shots.append((png(r["png"]),
                          f"{lab}  ·  {r['orbs']} sigils"
                          + (f", {r['blooms']} bloomed" if r["blooms"] > 0 else "")))
            print(f"    frame {n:>5}  {r['phase']:<6} orbs {r['orbs']:>2}  "
                  f"blooms {r['blooms']:>2}  hp {r['hp']}/{r['foeHp']}")
        assert not errors, errors[:4]

    tw = int(shots[0][0].width * a.scale)
    th = int(shots[0][0].height * a.scale)
    cols, PAD, LBL = 4, 14, 26
    rows = (len(shots) + cols - 1) // cols
    W = cols * (tw + PAD) + PAD
    H = rows * (th + PAD + LBL) + PAD + 24
    sheet = Image.new("RGB", (W, H), (12, 10, 18))
    dr = ImageDraw.Draw(sheet)
    dr.text((PAD, 7), f"FOREGONE — the Converse, seed {a.seed} v {a.foe}",
            fill=(74, 158, 255))
    for i, (im, lab) in enumerate(shots):
        x = PAD + (i % cols) * (tw + PAD)
        y = 24 + (i // cols) * (th + PAD + LBL)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y + LBL))
        dr.text((x + 2, y + LBL - 14), lab, fill=(212, 228, 255))
    p = OUT / a.out
    sheet.save(p)
    print(f"\n  {p.name}  ({sheet.width}x{sheet.height})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
