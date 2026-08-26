#!/usr/bin/env python3
"""THE BALLISTA WINDOW, PHOTOGRAPHED. The bolt bending, the pierce, the forks
   coming back.

    python3 marrowdraw_strip.py --game ../04-experiments/sc-marrowdraw.html

FULL-HALL frames, deliberately. This ultimate is a JOURNEY -- a bolt leaves the
bow pointing somewhere else and arrives at the quarry -- so a crop around
either ball would photograph the one thing that does not need looking at. The
whole point is the curve BETWEEN them.

TWO PASSES, for `bulwarden_strip`'s reason. The interesting frames cannot be
predicted: which bolt lands depends on the whole fight. Pass one steps a seed
and records the frame of the cast, of every bolt that curved, of every pierce
and of every fork that connected; pass two replays the same seed -- replay is
exact, the seed IS the fight -- and captures at those indices.

Writes PNGs into 05-reference/v42. Touches no build.
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
OUT = HERE.parent / "05-reference" / "v42"

FIND_JS = r"""([id, foe, seed, warm, cap]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;

  let n = 0, cast = -1, close = -1;
  const pierces = [], forkHits = [], curved = [];
  const turn = new Map();

  const oRes = AC.Match.prototype.resolveHit;
  m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
    const s = m._cineShot;
    const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
    if (s && self === me){
      if (s.fork) forkHits.push(n);
      else if (s.bal) pierces.push(n);
    }
    return r;
  };

  while (n < cap / DT && !m.over){
    m.step(DT); n++;
    if (me.ultBal && cast < 0) cast = n;
    if (!me.ultBal && cast > 0 && close < 0) close = n;
    /* How far each live bolt has turned since it was loosed. The frame worth
       photographing is one where a bolt is visibly OFF the line it left on
       and has not arrived yet -- a straight bolt in flight is a picture of
       the thing this ultimate is not. */
    for (const s of m.shots){
      if (!s.bal) continue;
      const p = turn.get(s);
      if (p === undefined){ turn.set(s, { a0: s.a, acc: 0, last: s.a }); continue; }
      let d = s.a - p.last;
      while (d >  Math.PI) d -= 2 * Math.PI;
      while (d < -Math.PI) d += 2 * Math.PI;
      p.acc += Math.abs(d); p.last = s.a;
      if (p.acc > 0.55) curved.push({ n, acc: +p.acc.toFixed(2),
                                      d: Math.round(Math.hypot(s.x - th.x, s.y - th.y)) });
    }
  }
  return { cast, close, pierces, forkHits, curved, n,
           dur: Math.round(me.w.ult.dur / DT) };
}"""

CAP_JS = r"""([id, foe, seed, warm, at]) => {
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
  const B = me.ultBal;
  const mine = m.shots.filter(s => s.own === (me === m.a ? "a" : "b"));
  return { png: document.getElementById('cv').toDataURL('image/png'),
           up: !!B, left: B ? +(B.dur - B.t).toFixed(1) : 0,
           bolts: B ? B.bolts : 0, forks: B ? B.forks : 0,
           inAir: mine.filter(s => s.bal).length,
           forksInAir: mine.filter(s => s.fork).length,
           meHp: Math.round(me.hp), thHp: Math.round(th.hp),
           bleed: th.stacks("hemorrhage") };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def font(sz, bold=True):
    for p in (HERE / "fonts" / ("AtkinsonHyperlegibleNext-Bold.ttf" if bold
                                else "AtkinsonHyperlegibleNext-Regular.ttf"),
              pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if p.exists():
            try:
                return ImageFont.truetype(str(p), sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--id", default="marrowdraw")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=8801)
    ap.add_argument("--warm", type=float, default=8.0)
    ap.add_argument("--cap", type=float, default=45.0)
    ap.add_argument("--scale", type=float, default=0.30)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    out_p = pathlib.Path(a.out) if a.out else OUT / f"ballista-strip-{a.seed}.png"

    with game(game_path=gp) as (page, errors):
        f = page.evaluate(FIND_JS, [a.id, a.foe, a.seed, a.warm, a.cap])
        if f["cast"] < 0:
            raise SystemExit(f"no cast inside {a.cap}s on seed {a.seed} — try another")
        if not f["pierces"]:
            raise SystemExit(f"no bolt landed on seed {a.seed} — try another "
                             f"(cast at {f['cast']}, {len(f['curved'])} curved frames)")
        print(f"  cast f{f['cast']}, window closed f{f['close']}, "
              f"{len(f['pierces'])} pierce(s), {len(f['forkHits'])} fork hit(s)")

        pierce = f["pierces"][0]
        # A bolt that is visibly OFF its launch line and still has ground to
        # cover. Taken from the curved frames BEFORE the first pierce, and the
        # one furthest from the quarry among the last few, so the picture has
        # a journey left in it.
        pre = [c for c in f["curved"] if c["n"] < pierce - 4]
        bend = max(pre[-14:], key=lambda c: c["d"])["n"] if pre else f["cast"] + 20
        fk = [x for x in f["forkHits"] if x > pierce]
        want = [("the window opens", f["cast"] + 4),
                ("the bolt bends", bend),
                ("the pierce", pierce + 1),
                ("the forks come about", min(pierce + 34, f["n"] - 1))]
        if fk:
            want.append(("a fork connects", fk[0] + 1))
        want.sort(key=lambda t: t[1])

        shots = []
        for label, at in want:
            r = page.evaluate(CAP_JS, [a.id, a.foe, a.seed, a.warm, at])
            shots.append((label, at, r))
            print(f"    {label:<22} f{at:<6} window {r['left']:>4}s  "
                  f"bolts {r['bolts']} forks {r['forks']}  "
                  f"air {r['inAir']}+{r['forksInAir']}  "
                  f"{r['meHp']}v{r['thHp']}  bleed {r['bleed']}")
        assert not errors, errors[:4]

    ims = [png(r["png"]) for _, _, r in shots]
    w, h = int(ims[0].width * a.scale), int(ims[0].height * a.scale)
    pad, top = 12, 40
    sheet = Image.new("RGB", (w * len(ims) + pad * (len(ims) + 1),
                              h + top + pad), (12, 11, 14))
    d = ImageDraw.Draw(sheet)
    fb, fs = font(17), font(14, bold=False)
    for i, ((label, at, r), im) in enumerate(zip(shots, ims)):
        x = pad + i * (w + pad)
        sheet.paste(im.resize((w, h), Image.LANCZOS), (x, top))
        d.text((x + 3, 6), label, font=fb, fill=(242, 226, 230))
        d.text((x + 3, 23),
               f"{r['left']}s left · {r['bolts']} bolts, {r['forks']} forks · "
               f"{r['meHp']}v{r['thHp']} · bleed {r['bleed']}",
               font=fs, fill=(152, 130, 140))
    sheet.save(out_p)
    print(f"\n  wrote {out_p}  ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
