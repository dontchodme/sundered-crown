#!/usr/bin/env python
"""A BACKLASH WINDOW, TO FILM. v91.

    python _nightglass_pick.py --game ../02-chain/sc-nightglass-fx.html

`_bloodwick_pick.py`'s shape. What has to be ON SCREEN is the design's
sentence -- blows landing on the shroud and coming straight back, cursing --
so a window is scored on how many blows it threw back, then on the biggest
one (a large number floating over the foe reads; a 1 does not), then on the
total. Prints the `--at` and `--window` to hand `cinema_clip` with
`--end-at-window`.
"""
from __future__ import annotations
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd); m.slLive = false;
    const me = m.a.w.id === rid ? m.a : m.b;
    let step = 0, W = null;
    const oSB = m.shroudBack;
    m.shroudBack = function(f, taken, src, hx, hy){
      const c0 = f.shroudTally.count, b0 = f.shroudTally.back;
      const r = oSB.call(this, f, taken, src, hx, hy);
      if (W && f === me && f.shroudTally.count > c0) W.big = Math.max(W.big, f.shroudTally.back - b0);
      return r;
    };
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const S = me.ultShroud;
      if (S && !W) W = { t0: m.t, big: 0, c0: me.shroudTally.count, b0: me.shroudTally.back };
      if (W && !S){
        W.end = m.t; W.n = me.shroudTally.count - W.c0; W.back = me.shroudTally.back - W.b0;
        W.score = W.n + W.big * 0.5 + W.back * 0.05;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightglass-fx.html")
    ap.add_argument("--relic", default="nightglass")
    ap.add_argument("--foes", default="emberedge,grudgebearer,redflail,cindercleave,oathwound,widowmaker,slagheart,axiom")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Backlash windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  thrown back {r['n']:>2}  biggest {r['big']:>3}  total {r['back']:>4}"
              f"   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
