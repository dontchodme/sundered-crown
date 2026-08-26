#!/usr/bin/env python3
"""AEGIS, PHOTOGRAPHED. The wall going up, tracking, blocking, and standing down.

    python3 bulwarden_strip.py --game ../02-chain/sc-bulwarden-frame.html

FULL-HALL frames, deliberately. This ultimate is a RELATIONSHIP between two
balls -- the wall faces the quarry and turns to keep facing it -- so a crop
around the caster would photograph the one thing that does not need looking at.
Both balls in every frame or the picture is a lie.

TWO PASSES, for `foregone_strip`'s reason. The block frames cannot be predicted:
a block happens when the foe's blade arrives inside the arc, which depends on
the whole fight. Pass one steps a seed and records the frame index of the cast,
of every block, and of the ending; pass two replays the same seed -- replay is
exact, the seed IS the fight -- and captures at those indices.

Writes PNGs into 05-reference/v41. Touches no build.
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
OUT = HERE.parent / "05-reference" / "v41"
RID = "bulwarden"

FIND_JS = """([id, foe, seed, warm, cap]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  let n = 0, cast = -1, end = -1, broke = false;
  const blocks = [];
  let ate = 0;
  while (n < cap / DT && !m.over){
    m.step(DT); n++;
    const A = me.ultAegis;
    if (A && cast < 0) cast = n;
    if (A && A.ate > ate){ blocks.push(n); ate = A.ate; }
    if (!A && cast > 0){ end = n; broke = ate > 0 && n - cast < (me.w.ult.dur / DT) - 2; break; }
  }
  return { cast, end, blocks, ate, broke,
           dur: Math.round(me.w.ult.dur / DT) };
}"""

CAP_JS = """([id, foe, seed, warm, at]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  for (let i = 0; i < at && !m.over; i++) m.step(DT);
  AC.__draw(m);
  const A = me.ultAegis;
  const want = Math.atan2(th.y - me.y, th.x - me.x);
  let off = A ? (A.ang - want) : 0;
  off = Math.atan2(Math.sin(off), Math.cos(off));
  return { png: document.getElementById('cv').toDataURL('image/png'),
           up: !!A, hp: A ? Math.round(A.hp) : 0, hp0: A ? A.hp0 : 0,
           ate: A ? Math.round(A.ate) : 0, back: A ? Math.round(A.back) : 0,
           flash: A ? +A.flash.toFixed(2) : 0,
           offDeg: +(off * 180 / Math.PI).toFixed(1),
           meHp: Math.round(me.hp), thHp: Math.round(th.hp) };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--foe", default="emberedge")
    ap.add_argument("--seed", type=int, default=118)
    ap.add_argument("--warm", type=float, default=6.0)
    ap.add_argument("--cap", type=float, default=40.0)
    ap.add_argument("--scale", type=float, default=0.30)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    out_p = pathlib.Path(a.out) if a.out else OUT / f"aegis-strip-{a.seed}.png"

    with game(game_path=gp) as (page, errors):
        f = page.evaluate(FIND_JS, [RID, a.foe, a.seed, a.warm, a.cap])
        if f["cast"] < 0:
            raise SystemExit(f"no cast inside {a.cap}s on seed {a.seed} — try another")
        print(f"  cast at frame {f['cast']}, ended {f['end']}, "
              f"{len(f['blocks'])} block(s), {f['ate']} eaten"
              + ("  BROKE" if f["broke"] else ""))

        cast, dur = f["cast"], f["dur"]
        end = f["end"] if f["end"] > 0 else cast + dur
        # the conjure, then the wall at rest, then every block we can fit,
        # then the last frame it is on screen
        want = [("raised", cast + 3),
                ("tracking", cast + int(dur * 0.30))]
        for i, b in enumerate(f["blocks"][:2]):
            want.append((f"block {i+1}", b + 2))
        want.append(("standing down" if not f["broke"] else "the wall gives",
                     max(cast + 4, end - 3)))
        want.sort(key=lambda t: t[1])

        shots = []
        for label, at in want:
            r = page.evaluate(CAP_JS, [RID, a.foe, a.seed, a.warm, at])
            shots.append((label, at, r))
            print(f"    {label:<16} f{at:<6} hp {r['hp']:>3}/{r['hp0']:<3} "
                  f"ate {r['ate']:<4} back {r['back']:<4} "
                  f"off {r['offDeg']:>6}deg  {r['meHp']}v{r['thHp']}")
        assert not errors, errors[:4]

    ims = [png(r["png"]) for _, _, r in shots]
    w = int(ims[0].width * a.scale)
    h = int(ims[0].height * a.scale)
    pad, top = 10, 34
    sheet = Image.new("RGB", (w * len(ims) + pad * (len(ims) + 1),
                              h + top + pad), (14, 12, 16))
    d = ImageDraw.Draw(sheet)
    for i, ((label, at, r), im) in enumerate(zip(shots, ims)):
        x = pad + i * (w + pad)
        sheet.paste(im.resize((w, h), Image.LANCZOS), (x, top))
        d.text((x + 3, 6), f"{label}", fill=(240, 226, 236))
        d.text((x + 3, 19),
               f"hp {r['hp']}/{r['hp0']}  ate {r['ate']}  back {r['back']}  "
               f"off {r['offDeg']}deg", fill=(150, 130, 145))
    sheet.save(out_p)
    print(f"\n  wrote {out_p}  ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
