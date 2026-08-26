#!/usr/bin/env python3
"""IS THE CROWD SCORING HIGHER, OR JUST MORE OFTEN?

The two have different fixes and only one of them is a bar. If crowded beats
score like ordinary ones and there are simply three times as many, no score
threshold thins them in the right proportion — the cure would have to be a
rate, not a level.
"""
import pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foes, seeds]) => {
  const crowd = [], plain = [];
  let cq = 0, pq = 0, cs = 0, ps = 0;
  for (const foe of foes) for (const s of seeds){
    const p = window.cinePlan(id, foe, s);
    for (const b of p.scored){
      if (b.kind !== "hit" || b.fatal) continue;
      if (b.crowd){ crowd.push(b.score); if (b.score >= CINE.floor) cq++; }
      else        { plain.push(b.score); if (b.score >= CINE.floor) pq++; }
    }
  }
  return { crowd, plain, cq, pq, floor: CINE.floor };
}"""

FOES = ["emberedge", "axiom", "ironhail", "grudgebearer", "thornwake"]
SEEDS = [113967 + i * 7919 for i in range(10)]
with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    r = p.evaluate(JS, ["twinshade", FOES, SEEDS])
    if e: print("PAGE ERRORS:", e[:3])

def pct(xs, q):
    xs = sorted(xs); return xs[min(len(xs)-1, int(len(xs)*q))]
def line(name, xs, q):
    print(f"  {name:<10} n={len(xs):>5}  mean {statistics.mean(xs):.2f}  "
          f"med {statistics.median(xs):.2f}  p80 {pct(xs,.80):.2f}  "
          f"p90 {pct(xs,.90):.2f}  p95 {pct(xs,.95):.2f}  max {max(xs):.2f}  "
          f"| >= floor: {q} ({100*q/len(xs):.1f}%)")
print(f"  global floor {r['floor']}\n")
line("crowded", r["crowd"], r["cq"])
line("ordinary", r["plain"], r["pq"])
c, p_ = r["crowd"], r["plain"]
print(f"\n  beats per fight   crowded {len(c)/50:.1f}   ordinary {len(p_)/50:.1f}")
print(f"  qualifying rate   crowded {100*r['cq']/len(c):.1f}%   "
      f"ordinary {100*r['pq']/len(p_):.1f}%")
print(f"\n  => {'LEVEL: crowded beats score higher' if statistics.mean(c) > statistics.mean(p_)*1.08 else 'RATE: the score distributions are alike; there are simply more of them'}")
