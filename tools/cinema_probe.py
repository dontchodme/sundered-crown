#!/usr/bin/env python3
"""What does the director actually pick, and is it the same four things every time?

A cut list that is always [ult, ult, kill] is not a director, it is a trigger on
`kind === "ult"`. This prints the score distribution by beat kind and the
composition of the chosen cuts across many matches, which is the only way to
see that failure -- it is invisible in any single fight.

  python3 cinema_probe.py --n 60
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import statistics
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""
([ids, n, seed0]) => {
  let s = seed0 >>> 0;
  const rows = [], cuts = [];
  for (let k = 0; k < n; k++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const i = s % ids.length;
    let j = (s >>> 8) % ids.length; if (j === i) j = (j + 1) % ids.length;
    const p = window.cinePlan(ids[i], ids[j], s);
    if (p.err) continue;
    for (const b of p.scored)
      rows.push([b.kind, +b.score.toFixed(3), b.crit ? 1 : 0, b.fatal ? 1 : 0,
                 (b.why || []).join("|")]);
    cuts.push(p.cuts.map(c => [c.fatal ? "kill" : c.kind, +c.score.toFixed(3),
                               (c.why || []).join("|")]));
  }
  return { rows, cuts };
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sc-cinema.html")
    ap.add_argument("--n", type=int, default=60)
    a = ap.parse_args()

    ids = ("dawnbringer,widowmaker,grudgebearer,thornwake,gravemourn,"
           "spellbreaker,ironhail,lightkeeper,farwarden").split(",")
    with game(game_path=HERE / a.game) as (page, errors):
        r = page.evaluate(JS, [ids, a.n, 0x5CE7E])
        if errors:
            print("page errors:", errors[:3])

    rows, cuts = r["rows"], r["cuts"]
    print(f"{len(cuts)} matches, {len(rows)} beats\n")

    by = collections.defaultdict(list)
    for kind, sc, crit, fatal, why in rows:
        if fatal:
            continue
        by[kind].append(sc)
    print("SCORE BY BEAT KIND (the killing blow excluded, it is always 9)")
    for k, v in sorted(by.items()):
        v.sort()
        print(f"  {k:6} n={len(v):5}  med {statistics.median(v):5.2f}"
              f"  p90 {v[int(len(v)*0.90)]:5.2f}  p99 {v[int(len(v)*0.99)]:5.2f}"
              f"  max {v[-1]:5.2f}")

    crit = [s for k, s, c, f, w in rows if c and not f]
    non = [s for k, s, c, f, w in rows if k == "hit" and not c and not f]
    if crit and non:
        print(f"\n  crits      med {statistics.median(crit):5.2f}"
              f"   non-crit hits med {statistics.median(non):5.2f}")

    print("\nWHAT GETS CHOSEN (composition of the cut list, kill excluded)")
    comp = collections.Counter()
    per = collections.Counter()
    reasons = collections.Counter()
    for cl in cuts:
        nonkill = [c for c in cl if c[0] != "kill"]
        per[len(nonkill)] += 1
        for kind, sc, why in nonkill:
            comp[kind] += 1
            for w in why.split("|"):
                if w:
                    # bucket by the SHAPE of the reason -- "traded 129" and
                    # "traded 84" are the same reason and must not each show up
                    # as a unique one-count row, which is how the first version
                    # of this probe hid the exchange term entirely.
                    reasons["".join("#" if ch.isdigit() else ch
                                    for ch in w).replace("##", "#")
                            .replace("##", "#").replace("##", "#")] += 1
    tot = sum(comp.values()) or 1
    for k, v in comp.most_common():
        print(f"  {k:6} {v:4}  {v/tot*100:5.1f}%")
    print("  set-pieces per match:", dict(sorted(per.items())))
    print("\n  reasons given:")
    for w, v in reasons.most_common(12):
        print(f"    {v:4}  {w}")

    ident = sum(1 for cl in cuts
                if [c[0] for c in cl if c[0] != "kill"] == ["ult", "ult"])
    print(f"\n  matches whose entire cut list is [ult, ult, kill]: "
          f"{ident}/{len(cuts)}  ({ident/max(1,len(cuts))*100:.0f}%)")
    print("  ^ this is the number that says whether it is a director or a trigger")
    return 0


if __name__ == "__main__":
    sys.exit(main())
