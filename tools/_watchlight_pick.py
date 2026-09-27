#!/usr/bin/env python
"""A BEACON WINDOW, TO FILM. v92.

    python _watchlight_pick.py --game ../02-chain/sc-watchlight-fx.html

`_cipher_pick.py`'s shape. What has to be ON SCREEN is the design's whole
sentence: a lantern LEFT on the floor while the caster moves on without it
(so the mean distance between the two across the window counts), the lantern
firing and landing on the foe, and the staff's own shoves. Prints the `--at`
and `--window` to hand `cinema_clip` with `--end-at-window`.
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
      if (W && self === me && cs){ if (cs.lamp) W.lamp++; else if (cs.spell === 'wardbolt') W.shove++; }
      return oRH.call(this, self, tgt, x, y, seg, mul, over);
    };
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const B = me.ultBeacon;
      if (B && !W) W = { t0: m.t, lamp: 0, shove: 0, dist: 0, n: 0 };
      if (W && B){ W.dist += Math.hypot(me.x - B.x, me.y - B.y); W.n++; }
      if (W && !B){
        W.end = m.t; W.away = W.dist / Math.max(1, W.n);
        W.score = W.lamp * 2 + W.shove * 0.8 + Math.min(W.away, 300) / 60;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-watchlight-fx.html")
    ap.add_argument("--relic", default="watchlight")
    ap.add_argument("--foes", default="grudgebearer,axiom,oathwound,nightfell,ravelbone,cindercleave,emberedge,gloamwire")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Beacon windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  lantern hits {r['lamp']:>2}  shoves {r['shove']:>2}  away {r['away']:4.0f}"
              f"   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
