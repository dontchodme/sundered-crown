#!/usr/bin/env python3
"""What does the bar produce? Not the mean -- the DISTRIBUTION.

AUDIT NOTE: the first version of this probe re-implemented the selection rule
in Python and drifted three revisions behind the module -- no volleys, the old
dedupe -- so its numbers were fiction. It now asks cinePlan itself, with
CINE.floor set per sweep value, so it measures the selection that ships.

  python3 cinema_rate_probe.py --n 120
"""
from __future__ import annotations
import argparse, collections, pathlib, sys
from scpage import game

HERE = pathlib.Path(__file__).parent
JS = r"""
([ids, n, seed0, floors]) => {
  const rows = [];
  for (const f of floors) {
    CINE.floor = f;
    let s = seed0 >>> 0;
    const dist = {}, kinds = { volley: 0, hit: 0, ult: 0, clank: 0 };
    let kills = 0, killCuts = 0, total = 0;
    for (let k = 0; k < n; k++) {
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const i = s % ids.length;
      let j = (s >>> 8) % ids.length; if (j === i) j = (j + 1) % ids.length;
      const p = window.cinePlan(ids[i], ids[j], s); if (p.err) continue;
      total++;
      const c = p.cuts.length;
      dist[Math.min(c, 5)] = (dist[Math.min(c, 5)] || 0) + 1;
      if (p.scored.some(b => b.fatal)) kills++;
      if (p.cuts.some(x => x.fatal)) killCuts++;
      for (const x of p.cuts) kinds[x.kind === "volley" ? "volley" : x.kind]++;
    }
    rows.push({ f, dist, kills, killCuts, total, kinds });
  }
  return rows;
}
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sc-cinema.html")
    ap.add_argument("--n", type=int, default=120)
    a = ap.parse_args()
    ids = ("dawnbringer,widowmaker,grudgebearer,thornwake,gravemourn,"
           "spellbreaker,ironhail,lightkeeper,farwarden").split(",")
    floors = [1.05, 1.25, 1.45, 1.65, 1.90, 2.20]
    with game(game_path=(HERE / a.game).resolve()) as (page, err):
        rows = page.evaluate(JS, [ids, a.n, 0x5CE7E, floors])
        if err: print("page errors", err[:2])
    print(f"{rows[0]['total']} matches per floor\n")
    print("bar     0     1     2    3+   mean   finishes filmed   volley share")
    for r in rows:
        n = r["total"]; d = r["dist"]
        g = lambda k: d.get(str(k), d.get(k, 0))
        mean = sum(int(k) * v for k, v in d.items()) / n
        vol = r["kinds"]["volley"]; tot = sum(r["kinds"].values()) or 1
        p3 = sum(v for k, v in d.items() if int(k) >= 3)
        print(f"{r['f']:4.2f} {g(0)/n*100:4.0f}% {g(1)/n*100:4.0f}% {g(2)/n*100:4.0f}%"
              f" {p3/n*100:4.0f}%  {mean:5.2f}   {r['killCuts']}/{r['kills']}"
              f" ({r['killCuts']/max(1,r['kills'])*100:3.0f}%)        {vol/tot*100:3.0f}%")
    print("\n^ 'finishes filmed' is how many killing blows earn their own"
          "\n  set-piece at that bar. The kill has no exemption.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
