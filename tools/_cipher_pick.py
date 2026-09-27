#!/usr/bin/env python
"""A CONVERGENCE WINDOW, TO FILM. v94.

    python _cipher_pick.py --game ../02-chain/sc-cipher-fx.html

`_briarwand_pick.py`'s shape. What has to be ON SCREEN is the design's whole
sentence: runes hanging on the walls when the window opens, flaring and
leaving in sequence, the in-window ones leaving half a second after they land,
and the runes arriving on the foe -- so a window is scored on how many were
hanging at the cast (the sequence is only a sequence at three or more), how
many left, and how many landed. Prints the `--at` and `--window` to hand
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
      if (W && self === me && cs && cs.flown) W.landed++;
      return oRH.call(this, self, tgt, x, y, seg, mul, over);
    };
    while (!m.over && step < secs / DT){
      const T0 = me.convergeTally ? { a: me.convergeTally.atCast, l: me.convergeTally.launched } : { a: 0, l: 0 };
      m.step(DT); step++;
      const C = me.ultConverge;
      if (C && !W) W = { t0: m.t, hang: 0, launched: 0, landed: 0 };
      if (W && me.convergeTally){ W.hang += me.convergeTally.atCast - T0.a; W.launched += me.convergeTally.launched - T0.l; }
      if (W && !C){
        W.end = m.t;
        W.score = Math.min(W.hang, 6) * 2 + W.launched * 0.6 + W.landed * 1.2;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-cipher-fx.html")
    ap.add_argument("--relic", default="cipher")
    ap.add_argument("--foes", default="grudgebearer,axiom,oathwound,nightfell,ravelbone,cindercleave,emberedge,farwarden")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Convergence windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  hanging {r['hang']:>2}  left {r['launched']:>3}  landed {r['landed']:>3}"
              f"   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
