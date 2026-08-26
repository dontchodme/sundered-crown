#!/usr/bin/env python3
"""HOW MANY SUNDER STACKS ARE ACTUALLY ON THE FOE WHEN EMBEREDGE CASTS?

The Detonation consumes Sunder, so its per-stack curve is only as good as the
stack count it will really see. Guessing "assume 4" and tuning around it is
how an ult ends up feeling great in a hand-built test and dead in a match.

Instruments `fireUlt` — no sim change, the wrapper reads state and calls
through — and records, at every Forgefall cast across the whole field:

  * stacks of Sunder on the FOE at cast (the detonation's fuel)
  * stacks of every other status on the foe (what else is riding along)
  * match time of the cast, and whether the foe was stunned

Also reports the same for Grudgebearer's Crucible, because the Crucible
consumes the same resource and the two curves have to be comparable — if
Emberedge routinely casts on more stacks than Grudgebearer, "the same move
pointed outward" is not the same move at all.

    python3 sunder_probe.py --game ../02-chain/sc-daybreak.html --n 60
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys
from collections import Counter, defaultdict

from scpage import game

JS = r"""
([ids, seeds, watch]) => {
  const rec = [];
  const orig = AC.Match.prototype.fireUlt;
  AC.Match.prototype.fireUlt = function(f, foe){
    if (watch.includes(f.w.id)) {
      const st = {};
      for (const k in foe.status) st[k] = foe.status[k].stacks;
      rec.push({ id: f.w.id, foe: foe.w.id, t: this.t,
                 sunder: foe.stacks("sunder"), other: st,
                 foeStun: foe.stun > 0, hp: foe.hp, selfHp: f.hp });
    }
    return orig.call(this, f, foe);
  };
  try {
    for (let i = 0; i < ids.length; i++) {
      for (let j = 0; j < ids.length; j++) {
        if (i === j) continue;
        if (!watch.includes(ids[i])) continue;
        for (const s of seeds) {
          const m = new AC.Match(ids[i], ids[j], s >>> 0);
          const dt = AC.CONFIG.physics.dt;
          let guard = 0;
          while (!m.over && guard++ < 200000) m.step(dt);
        }
      }
    }
  } finally { AC.Match.prototype.fireUlt = orig; }
  return rec;
}
"""


def seeds_for(n, seed0=20260815):
    s = seed0 & 0xFFFFFFFF
    out = []
    for _ in range(n):
        s = (s * 1103515245 + 12345) & 0xFFFFFFFF
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--watch", default="emberedge,grudgebearer")
    a = ap.parse_args()

    watch = [s.strip() for s in a.watch.split(",")]
    with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        rec = page.evaluate(JS, [ids, seeds_for(a.n), watch])
        if errors:
            raise RuntimeError(errors[:3])

    by = defaultdict(list)
    for r in rec:
        by[r["id"]].append(r)

    for wid in watch:
        rows = by.get(wid, [])
        if not rows:
            print(f"\n{wid}: NO CASTS RECORDED — the probe is broken or the "
                  f"ult never fires")
            continue
        sund = [r["sunder"] for r in rows]
        c = Counter(sund)
        n = len(sund)
        print(f"\n=== {wid} — {n} casts over {len(ids)-1} opponents "
              f"x {a.n} seeds ===")
        print(f"  Sunder on foe at cast: mean {statistics.mean(sund):.2f}  "
              f"median {statistics.median(sund):.0f}  "
              f"max {max(sund)}  zero-stack casts {c[0]/n*100:.1f}%")
        for k in range(0, 7):
            bar = "#" * round(c[k] / n * 60)
            print(f"    {k} stacks  {c[k]/n*100:5.1f}%  {bar}")
        print(f"  cast time: mean {statistics.mean([r['t'] for r in rows]):.1f}s"
              f"   foe stunned at cast: "
              f"{sum(r['foeStun'] for r in rows)/n*100:.0f}%")
        other = Counter()
        for r in rows:
            for k, v in r["other"].items():
                if k != "sunder":
                    other[k] += 1
        if other:
            print("  other statuses riding on the foe at cast: "
                  + ", ".join(f"{k} {v/n*100:.0f}%"
                              for k, v in other.most_common(6)))
        # Per-opponent floor: the matchups where the detonation would fizzle.
        per = defaultdict(list)
        for r in rows:
            per[r["foe"]].append(r["sunder"])
        worst = sorted(per.items(), key=lambda kv: statistics.mean(kv[1]))[:4]
        best = sorted(per.items(), key=lambda kv: -statistics.mean(kv[1]))[:3]
        print("  driest matchups: " + ", ".join(
            f"{k} {statistics.mean(v):.1f}" for k, v in worst))
        print("  richest matchups: " + ", ".join(
            f"{k} {statistics.mean(v):.1f}" for k, v in best))


if __name__ == "__main__":
    sys.exit(main())
