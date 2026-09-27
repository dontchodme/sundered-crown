#!/usr/bin/env python
"""A BLOOM WINDOW, TO FILM. v93.

    python _briarwand_pick.py --game ../02-chain/sc-bloom.html

`_culverin_pick.py`'s shape. What has to be ON SCREEN is the design's whole
sentence: the cloud leaving the caster and going after the foe, the foe inside
it and bitten, the entangle stacking -- so a window is scored on bites, on the
share of it the foe spends inside, and on how far the cloud actually travelled
(a cloud that sits on a foe who never moved says nothing about the drift).
Prints the `--at` and `--window` to hand `cinema_clip` with `--end-at-window`.
"""
from __future__ import annotations
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd); m.slLive = false;
    const me = m.a.w.id === rid ? m.a : m.b, fo = me === m.a ? m.b : m.a;
    let step = 0, W = null;
    while (!m.over && step < secs / DT){
      const b0 = me.pollenTally ? me.pollenTally.bites : 0;
      m.step(DT); step++;
      const P = me.ultPollen;
      if (P && !W) W = { t0: m.t, bites: 0, inF: 0, frames: 0, x0: P.x, y0: P.y, travel: 0, lx: P.x, ly: P.y };
      if (W && P){
        W.frames++; if (Math.hypot(fo.x - P.x, fo.y - P.y) < me.w.ult.cloudR + R) W.inF++;
        W.travel += Math.hypot(P.x - W.lx, P.y - W.ly); W.lx = P.x; W.ly = P.y;
        W.bites += me.pollenTally.bites - b0;
      }
      if (W && !P){
        W.end = m.t;
        W.score = W.bites * 1.0 + (W.inF / Math.max(1, W.frames)) * 8 + Math.min(W.travel, 500) / 100;
        out.push(Object.assign({ foe, seed: sd }, W)); W = null;
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bloom.html")
    ap.add_argument("--relic", default="briarwand")
    ap.add_argument("--foes", default="grudgebearer,axiom,oathwound,nightfell,ravelbone,cindercleave,spellbreaker,farwarden")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Bloom windows")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6); win = (r["end"] - r["t0"]) + 1.2
        print(f"  {r['score']:5.1f}  {r['foe']:<13}{r['seed']:>6}  bites {r['bites']:>3}  inside {r['inF']/max(1,r['frames']):.0%}"
              f"  travel {r['travel']:4.0f}   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
