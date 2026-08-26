#!/usr/bin/env python3
"""FIND A FIGHT WORTH FILMING FOR THE CONVERSE.

    python3 foregone_pick.py --game ../02-chain/sc-foregone.html

`cinema_pick` scores a seed on its cut list alone, which is the right question
for a director demo and the wrong one for a relic reveal. A Converse fight is
only worth filming if the ULTIMATE is legible in it, and that needs things the
cut list cannot see:

  - at least two casts, so the viewer sees the trail laid AND sees it happen
    a second time knowing what is coming
  - a trail that is actually long. Sigils are laid by TRAVEL, so a cast made
    while the caster is pinned in a corner lays three and the reversal is a
    twitch. `orbs` is the number to sort on.
  - a reversal that CONNECTS. Eight of seventy-four rings reach the foe in an
    average cast; a cast where none do is a light show with no fight in it.
  - the two casts far enough apart not to read as one event.

It also reports the cut count against the SAME fight with `crowdMul` off, so
the cost of the director exception on the chosen seed is visible rather than
assumed -- v38 open decision 8, where two crowding ultimates on one floor
halved the cut count of the marquee fight and nothing was decided about it.

Writes nothing.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent

JS = r"""([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const s of seeds){
    const m = new AC.Match(id, foe, s);
    m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b;
    const casts = [];
    let cur = null, n = 0;
    while (!m.over && n < 120 / DT){
      m.step(DT); n++;
      const S = me.ultTrace;
      if (S && !cur) cur = { t0: m.t, orbs: 0, blooms: 0, hits: 0 };
      if (S && cur){
        cur.orbs = Math.max(cur.orbs, S.orbs.length + S.blooms);
        cur.blooms = Math.max(cur.blooms, S.blooms);
        cur.hits = Math.max(cur.hits, S.hits);
      }
      if (!S && cur){ cur.t1 = m.t; casts.push(cur); cur = null; }
    }
    if (cur){ cur.t1 = m.t; casts.push(cur); }
    if (!m.over) continue;
    const p = window.cinePlan(id, foe, s);
    if (p.err) continue;
    const cuts = (p.cuts || []).length;
    const kill = (p.cuts || []).some(c => c.fatal);
    const gap = casts.length > 1
      ? Math.min.apply(null, casts.slice(1).map((c, i) => c.t0 - casts[i].t1))
      : 999;
    out.push({ foe, seed: s, dur: +m.t.toFixed(1),
               won: !!(m.winner && m.winner.w.id === id),
               winner: m.winner ? m.winner.w.name : "-",
               casts: casts.length,
               orbs: casts.map(c => c.orbs),
               hits: casts.map(c => c.hits),
               maxOrbs: Math.max.apply(null, casts.map(c => c.orbs).concat([0])),
               totHits: casts.reduce((a, c) => a + c.hits, 0),
               gap: +gap.toFixed(1), cuts, kill,
               at: casts.map(c => +c.t0.toFixed(1)) });
  }
  return out;
}"""

# The same fights, replanned with the exception off. crowdMul does not touch
# the sim, so this is the cut list of the identical fight -- not a comparison
# across two different populations.
COST_JS = r"""([id, picks]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const foeMuls = {};
  const out = [];
  for (const p of picks){
    const on = (window.cinePlan(id, p.foe, p.seed).cuts || []).length;
    const sv = w.ult.crowdMul; w.ult.crowdMul = 0;
    const fw = AC.WEAPONS.find(x => x.id === p.foe);
    const fsv = fw.ult ? fw.ult.crowdMul : undefined;
    if (fw.ult) fw.ult.crowdMul = 0;
    const off = (window.cinePlan(id, p.foe, p.seed).cuts || []).length;
    w.ult.crowdMul = sv;
    if (fw.ult) fw.ult.crowdMul = fsv;
    out.push({ foe: p.foe, seed: p.seed, on, off,
               foeDeclares: !!(fw.ult && fsv) });
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--id", default="foregone")
    ap.add_argument("--foes", default="redflail,thornwake,grudgebearer,nightfell")
    ap.add_argument("--n", type=int, default=180)
    ap.add_argument("--seed0", type=int, default=910000)
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    foes = a.foes.split(",")
    seeds = [a.seed0 + 37 * i for i in range(a.n)]

    with game(game_path=gp) as (page, errors):
        rows = page.evaluate(JS, [a.id, foes, seeds])
        print(f"\n  {len(rows)} resolved fights across {len(foes)} foes "
              f"x {a.n} seeds")

        # Score. Two casts is the floor; beyond that the trail LENGTH and
        # whether the reversal connects are what make it legible.
        def score(r):
            if r["casts"] < 2 or r["gap"] < 6.0:
                return -1
            return (min(r["casts"], 3) * 3
                    + r["maxOrbs"] * 0.6
                    + min(r["totHits"], 20) * 0.5
                    + r["cuts"] * 0.8
                    + (2 if r["kill"] else 0)
                    - abs(r["dur"] - 40) * 0.10)

        rows.sort(key=score, reverse=True)
        best = [r for r in rows if score(r) > 0][:a.top]
        print(f"\n  {'foe':<14}{'seed':>9}{'dur':>7}{'casts':>7}{'orbs':>12}"
              f"{'ringHits':>11}{'cuts':>6}{'kill':>6}  winner")
        for r in best:
            print(f"  {r['foe']:<14}{r['seed']:>9}{r['dur']:>6.1f}s"
                  f"{r['casts']:>7}{str(r['orbs']):>12}{str(r['hits']):>11}"
                  f"{r['cuts']:>6}{('Y' if r['kill'] else '-'):>6}  "
                  f"{r['winner']}  @ {r['at']}")

        cost = page.evaluate(COST_JS, [a.id, best])
        print(f"\n  THE EXCEPTION'S COST ON THESE SEEDS "
              f"(cuts with crowdMul on / off):")
        for c in cost:
            print(f"    {c['foe']:<14}{c['seed']:>9}   {c['on']:>2} / {c['off']:>2}"
                  + ("   <- foe also declares crowdMul" if c["foeDeclares"] else ""))
        assert not errors, errors[:4]
    return 0


if __name__ == "__main__":
    sys.exit(main())
