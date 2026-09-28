#!/usr/bin/env python
"""A GYRE WINDOW, TO FILM. v90.

    python _bloodwick_pick.py --game ../02-chain/sc-bloodwick-fx.html

`_crozier_pick.py`'s shape. What has to be ON SCREEN is the design's sentence
-- the drops circling the ball, then lunging AS ONE -- and that is the rare
case (91% of lunges carry a single globule, v90 build §4), so a window is
scored first on its BIGGEST lunge, then on how long the orbit stood with
three or more in it, then on lunged landings. Prints the `--at` and
`--window` to hand `cinema_clip` with `--end-at-window`.
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
    const oB = m.beat;
    m.beat = function(o){ if (W && o && o.kind === 'ult' && o.w === rid && o.lunge !== undefined) W.big = Math.max(W.big, o.lunge); return oB.call(this, o); };
    const oRH = m.resolveHit;
    m.resolveHit = function(self, tgt, x, y, seg, mul, over){
      const cs = this._cineShot;
      if (W && self === me && cs && cs.spell === 'bloodseeker' && cs.home === me.w.ult.lungeHome) W.landed++;
      return oRH.call(this, self, tgt, x, y, seg, mul, over);
    };
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const G = me.ultGyre;
      if (G && !W) W = { t0: m.t, big: 0, full: 0, landed: 0 };
      if (W && G && G.orb.length >= 3) W.full += DT;
      if (W && !G){
        W.end = m.t;
        W.score = W.big * 3 + Math.min(W.full, 4) + W.landed * 0.5;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bloodwick-fx.html")
    ap.add_argument("--relic", default="bloodwick")
    ap.add_argument("--foes", default="farwarden,aureole,ironhail,gloamwire,lightkeeper,axiom,emberedge,cindercleave")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Gyre windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  biggest lunge {r['big']}  3+ orbiting {r['full']:4.1f}s  lunged landings {r['landed']:>2}"
              f"   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
