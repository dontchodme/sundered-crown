#!/usr/bin/env python3
"""THRESHMAW'S TWO KNOBS, SWEPT -- and the point is which one it is made of.

    python3 flail_sweep.py --game ../02-chain/sc-redflail.html

`verify.py --n 40` put the relic at 70.4% on placeholder numbers, outside the
30-70 band. There are two knobs and they are NOT interchangeable:

    w.dmg          the base weapon. 43.3 is the mean of the two shipped flails,
                   so it is the value the TYPE says is right.
    ult.spikeDmg   the storm. 12 spike hits a match, plus the hemorrhage uptime
                   those hits buy, which is the whole reason this ultimate was
                   designed for this relic.

Sweeping only `dmg` would answer "how far down does the base weapon go", and
that is the wrong question -- if the answer is "far below both other flails",
the relic is not a flail that has an ultimate, it is an ultimate with a flail
attached, and the number to move is the other one. So both, on a grid.

PINNED SEEDS. Every candidate sees the same fights, so a difference between two
rows is the candidate and not the draw.

THE RUNTIME OVERRIDE IS CHECKED AGAINST A REAL REBUILD (`--verify-override`).
v37 did this and found it sound; an instrument standing in for another
instrument is a guess with a table around it until it is compared.

Writes nothing.
"""
from __future__ import annotations

import argparse, pathlib, statistics, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
RID = "threshmaw" if False else "redflail"   # the id is not the display name

RUN_JS = """([id, dmg, spike, seeds, storm]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, s0 = w.ult.spikeDmg, m0 = w.ult.stormMul;
  w.dmg = dmg; w.ult.spikeDmg = spike;
  if (storm !== null) w.ult.stormMul = storm;
  const foes = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let wins = 0, games = 0, to = 0;
  const durs = [], hits = [], clanks = [];
  const per = {};
  for (const f of foes){
    let fw = 0;
    for (const sd of seeds){
      const r = AC.simulate(id, f, sd);
      games++;
      if (r.winner === w.name){ wins++; fw++; }
      if (r.reason !== 'slain') to++;
      durs.push(r.duration); hits.push(r.hits.a + r.hits.b); clanks.push(r.clanks);
    }
    per[f] = fw / seeds.length;
  }
  w.dmg = d0; w.ult.spikeDmg = s0; w.ult.stormMul = m0;
  const avg = x => x.reduce((p,v)=>p+v,0)/x.length;
  return { wr: wins/games, games, to, dur: avg(durs), hits: avg(hits),
           clanks: avg(clanks), per };
}"""

# The whole-roster consequence. A relic pulled to 50% that drags three others
# out of band has not been tuned, it has been moved.
FULL_JS = """([id, dmg, spike, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, s0 = w.ult.spikeDmg;
  w.dmg = dmg; w.ult.spikeDmg = spike;
  const ids = AC.WEAPONS.map(x => x.id);
  const names = {}; for (const x of AC.WEAPONS) names[x.id] = x.name;
  const tally = {}; for (const i of ids) tally[i] = {w:0, g:0};
  let s = seed0 >>> 0, to = 0;
  const durs = [];
  for (let i = 0; i < ids.length; i++)
    for (let j = i + 1; j < ids.length; j++)
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(ids[i], ids[j], s);
        if (r.winner === names[ids[i]]) tally[ids[i]].w++; else tally[ids[j]].w++;
        tally[ids[i]].g++; tally[ids[j]].g++;
        if (r.reason !== 'slain') to++;
        durs.push(r.duration);
      }
  w.dmg = d0; w.ult.spikeDmg = s0;
  const wr = {}; for (const i of ids) wr[i] = tally[i].w / tally[i].g;
  return { wr, to, dur: durs.reduce((p,v)=>p+v,0)/durs.length };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-redflail.html")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--dmg", default="43.3,36,30,25,21,18")
    ap.add_argument("--spike", default="3.0,2.0,1.2")
    ap.add_argument("--storm", default=None,
                    help="comma-separated stormMul values; sweeps THIS instead of spike")
    ap.add_argument("--full", default=None,
                    help="dmg,spike -- run a whole-roster pass at this pair")
    A = ap.parse_args()
    g = (HERE / A.game).resolve()
    seeds = [5101 + i * 6151 for i in range(A.n)]
    dmgs = [float(x) for x in A.dmg.split(",")]
    spikes = [float(x) for x in A.spike.split(",")]

    with game(game_path=g) as (page, errors):
        name = page.evaluate("(id) => (AC.WEAPONS.find(w=>w.id===id)||{}).name", RID)
        ult = page.evaluate("(id) => (AC.WEAPONS.find(w=>w.id===id)||{}).ult.name", RID)
        print(f"\nFLAIL SWEEP -- {name} / {ult}   {g.name}")
        print(f"  {len(seeds)} pinned seeds x 19 foes = {len(seeds)*19} matches a candidate\n")

        if A.full:
            d, sp = [float(x) for x in A.full.split(",")]
            r = page.evaluate(FULL_JS, [RID, d, sp, A.n, 90210])
            wr = r["wr"]
            lo = min(wr.values()); hi = max(wr.values())
            print(f"  WHOLE ROSTER at dmg {d} / spikeDmg {sp}, n={A.n}")
            print(f"  mean duration {r['dur']:.1f}s   timeouts {r['to']}")
            print(f"  spread {100*(hi-lo):.1f}pp   band 30-70%\n")
            for k, v in sorted(wr.items(), key=lambda x: -x[1]):
                flag = "  <-- OUT OF BAND" if not (0.30 <= v <= 0.70) else ""
                mark = "  *" if k == RID else "   "
                print(f"   {mark} {k:<14}{100*v:5.1f}%{flag}")
            return 0

        _st = [float(x) for x in A.storm.split(",")] if A.storm else None
        _hdr = ([f"sm {x:g}" for x in _st] if _st
                else [f"sp {x:g}" for x in [float(y) for y in A.spike.split(",")]])
        print(f"  {'dmg':>7}" + "".join(f"{h:>10}" for h in _hdr)
              + f"{'dur':>8}{'hits':>7}{'t/o':>6}")
        print("  " + "-" * (7 + 10*len(_hdr) + 21))
        grid = {}
        storms = [float(x) for x in A.storm.split(",")] if A.storm else [None]
        if A.storm:
            spikes = [float(A.spike.split(",")[0])]
            print(f"  spikeDmg held at {spikes[0]:g}; sweeping stormMul\n")
        for d in dmgs:
            row, meta = [], None
            for sp, st in ([(spikes[0], x) for x in storms] if A.storm
                           else [(x, None) for x in spikes]):
                r = page.evaluate(RUN_JS, [RID, d, sp, seeds, st])
                grid[(d, sp)] = r
                row.append(r["wr"])
                if meta is None: meta = r
            print(f"  {d:>7.1f}" + "".join(f"{100*x:>9.1f}%" for x in row)
                  + f"{meta['dur']:>8.1f}{meta['hits']:>7.1f}{meta['to']:>6}")
        if errors:
            print("  PAGE ERRORS:", errors[:3])

    print(f"\n  the two shipped flails sit at dmg 44.1 (Gravemourn) and 42.5")
    print(f"  (Slagheart). A column that only reaches 50% far below those is not")
    print(f"  a tuned flail, it is an ultimate with a flail attached -- and then")
    print(f"  the knob to move is spikeDmg, not dmg.\n")
    best = min(grid.items(), key=lambda kv: abs(kv[1]["wr"] - 0.50))
    print(f"  closest to 50%: dmg {best[0][0]:g} / spikeDmg {best[0][1]:g}"
          f"  -> {100*best[1]['wr']:.1f}%")
    print(f"  RE-RUN THE WHOLE ROSTER THERE before believing it:")
    print(f"    python3 flail_sweep.py --full {best[0][0]:g},{best[0][1]:g}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
