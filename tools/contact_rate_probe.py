#!/usr/bin/env python3
"""IS THE TWINBLADE ACTUALLY THE FASTEST THING ON THE FLOOR?

    python3 contact_rate_probe.py --game ../02-chain/sc-twinshade-scrunch.html

RESTORED FROM THE PROJECT, 2026-08-20. This is v36's tool. It was never checked
into the tree because v36's design was set aside, but its OUTPUT was not: the
type ordering it produced is quoted in `purpledagger_probe.py`'s header, in
v36 §2, and in v37's write-up, and every one of those quotes is load-bearing.

    bow 0.360 . greatsword 0.283 . twinblade 0.271 .
    scythe 0.228 . flail 0.205 . warhammer 0.183

`--noult` IS NEW AND IT IS THE POINT OF THE RESTORE. `flail_probe.py` found
that the two shipped flails -- which share reach, spin, mass and mode byte for
byte -- returned 0.141 and 0.196 hits/s with damage pinned, a 39% gap on a
number that should not vary at all, and that the gap closes to 1% when the
ultimates are suppressed. Slagheart's Ironbloom sprays nine shards that each
resolve a hit. **The instrument was counting the ultimate as contact.**

`hits` is `Fighter.hits`, incremented in `resolveHit` -- the same counter
verify.py's six-hit floor reads -- and ult damage goes through `resolveHit` too,
so this is not a bug in the counter. It is a bug in what the number was called.

Run it both ways. The delta per type is how much of "this type's contact rate"
was its ultimate.

Writes nothing.
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

ROSTER_JS = """() => AC.WEAPONS.map(w => ({ id: w.id, name: w.name,
  shape: w.shape, aff: w.aff, mode: w.mode, reach: w.reach, spin: w.spin,
  mass: w.mass, blades: w.blades.length, dmg: w.dmg }))"""

RUN_JS = """([id, foes, seeds, pin, allIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const saved = {}, savedUlt = {};
  for (const pid of allIds){
    const w = AC.WEAPONS.find(x => x.id === pid);
    saved[pid] = w.dmg; w.dmg = pin;
    if (noult){ savedUlt[pid] = w.ult.charge; w.ult.charge = 1e9; }
  }
  const rows = [];
  for (const f of foes){
    if (f === id) continue;
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      let steps = 0, first = null, last = 0;
      while (!m.over && steps < 120 / DT){
        m.step(DT); steps++;
        if (me.hits > last){ if (first === null) first = steps * DT; last = me.hits; }
      }
      rows.push({ foe: f, dur: steps * DT, hits: me.hits, first: first });
    }
  }
  for (const pid of allIds){
    const w = AC.WEAPONS.find(x => x.id === pid);
    w.dmg = saved[pid];
    if (noult) w.ult.charge = savedUlt[pid];
  }
  return rows;
}"""


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--pin", type=float, default=14.0)
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")
    seeds = [A.seed + i * 7919 for i in range(A.seeds)]

    both = {}
    with game(game_path=g) as (page, errors):
        roster = page.evaluate(ROSTER_JS)
        ids = [w["id"] for w in roster]
        field, seen = [], set()
        for w in roster:
            if w["shape"] not in seen:
                seen.add(w["shape"]); field.append(w["id"])
        print(f"\nfield ({len(field)}): " + ", ".join(field))
        print(f"{len(seeds)} seeds, damage pinned to {A.pin} on all {len(ids)} relics")
        print(f"build {g.name}\n")

        for noult in (False, True):
            out = []
            for w in roster:
                rows = page.evaluate(RUN_JS, [w["id"], field, seeds, A.pin, ids, noult])
                out.append({
                    "id": w["id"], "shape": w["shape"], "aff": w["aff"],
                    "hps": statistics.mean(r["hits"] / r["dur"] for r in rows),
                    "first": med([r["first"] for r in rows]),
                })
            both[noult] = {r["id"]: r for r in out}
        if errors:
            print("PAGE ERRORS:", errors[:5])

    shapes = {}
    for rid, r in both[False].items():
        shapes.setdefault(r["shape"], []).append(rid)

    print(f"  {'type':<12}{'relics':>7}{'ULTS ON':>10}{'spread':>9}"
          f"{'ULTS OFF':>11}{'spread':>9}{'ult share':>11}")
    print("  " + "-" * 69)
    rows = []
    for t, members in shapes.items():
        on = [both[False][m]["hps"] for m in members]
        off = [both[True][m]["hps"] for m in members]
        rows.append((t, len(members), statistics.mean(on), max(on) - min(on),
                     statistics.mean(off), max(off) - min(off)))
    rows.sort(key=lambda x: -x[2])
    for t, n, mon, son, moff, soff in rows:
        share = (mon - moff) / mon if mon else 0
        print(f"  {t:<12}{n:>7}{mon:>10.3f}{son:>9.3f}{moff:>11.3f}{soff:>9.3f}"
              f"{100*share:>10.0f}%")

    print("\n  'spread' is the disagreement BETWEEN relics of one type. They share")
    print("  reach, spin, mass and mode exactly, so with the ultimate removed the")
    print("  only channels left are the STATUS and the instrument -- entangle slows")
    print("  the foe's swing, hex stuns its weapon, sunder multiplies what it takes.")
    print("  That residual is NOT pure noise and should not be called noise. What")
    print("  the collapse from the left column to the right one shows is only that")
    print("  the ULTIMATE was the dominant term, and that any type ordering read")
    print("  off the left column is partly an ordering of ultimates.\n")

    print(f"  {'relic':<14}{'type':<12}{'ULTS ON':>10}{'ULTS OFF':>11}{'delta':>9}")
    print("  " + "-" * 56)
    for rid in sorted(both[False], key=lambda k: -both[False][k]["hps"]):
        a, b = both[False][rid]["hps"], both[True][rid]["hps"]
        print(f"  {rid:<14}{both[False][rid]['shape']:<12}{a:>10.3f}{b:>11.3f}"
              f"{a-b:>+9.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
