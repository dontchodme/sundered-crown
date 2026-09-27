#!/usr/bin/env python
"""A RADIANCE WINDOW, TO FILM. v95.

    python _crozier_pick.py --game ../02-chain/sc-crozier-fx.html

`_watchlight_pick.py`'s shape. What has to be ON SCREEN is the design's whole
sentence: needles becoming shafts as they fly and landing big (a grown landing
counts by how far it had grown), and a lance passing THROUGH a blade (the one
thing no other shot does). Prints the `--at` and `--window` to hand
`cinema_clip` with `--end-at-window`.
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
    const oRH = m.resolveHit;
    m.resolveHit = function(self, tgt, x, y, seg, mul, over){
      const cs = this._cineShot;
      if (W && self === me && cs && cs.grow){ W.grown++; W.kSum += cs.grow.k; }
      return oRH.call(this, self, tgt, x, y, seg, mul, over);
    };
    while (!m.over && step < secs / DT){
      const thr = new Set(m.shots.filter(s => s.through));
      m.step(DT); step++;
      const R = me.ultRadiance;
      if (R && !W) W = { t0: m.t, grown: 0, kSum: 0, through: 0 };
      if (W) for (const s of m.shots) if (s.spell === 'lance' && s.through && !thr.has(s)) W.through++;
      if (W && !R){
        W.end = m.t;
        W.score = W.kSum * 2 + Math.min(W.through, 4) * 1.5;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crozier-fx.html")
    ap.add_argument("--relic", default="crozier")
    ap.add_argument("--foes", default="grudgebearer,oathwound,widowmaker,twinshade,slagheart,cindercleave,emberedge,nightfell")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Radiance windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  grown landings {r['grown']:>2} (k {r['kSum']:4.1f})  through a blade {r['through']:>2}"
              f"   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
