#!/usr/bin/env python3
"""WHO IS ACTUALLY WEAKEST, AND IS THE ULT THE REASON?

`verify.py --n 60` ranks the roster, but at 900 games per relic its standard
error is ~1.7pp and the bottom six sit inside 2pp of each other. "Farwarden is
weakest" is therefore a claim the instrument cannot support. This tool exists to
either support it or kill it, and to answer the question that actually decides
where an ult redesign goes:

    axis 1  HOW STRONG IS THE RELIC          winrate, with a Wilson interval
    axis 2  HOW MUCH OF THAT IS THE ULT      paired-seed winrate with the ult
                                             disabled; the delta is the ult's
                                             whole contribution in pp

Axis 2 is the one that picked Dawnbringer last session (weakest ball carrying
the strongest ult => the budget was in the wrong place). A relic that is weak
AND whose ult is worth nothing is a different, better target: the redesign has
somewhere to spend.

METHOD, and why each choice is falsifiable

* Common random numbers. Every pairing plays the SAME seed list, so relic-to-
  relic comparisons share their luck instead of each drawing fresh noise.
* The ult is disabled by pushing `ult.charge` to 1e9 — the single gate at
  `f.charge >= f.w.ult.charge`. Nothing else is touched, so an ult-off run is
  the same fighter with the same blade.
* That disabling is CHECKED, not trusted: every match reports `ultsFired` per
  side, the baseline must show the relic firing, and the ult-off run must show
  it firing zero times. A silently-still-firing ult would otherwise read as
  "this ult is worth 0pp", which is exactly the wrong answer.
* Ult-off runs only the 15 pairings the relic is in. The opponent keeps its
  own ult, so the delta is "what this ult is worth against a live field".

  python3 weak_probe.py --game ../02-chain/sc-daybreak.html --n 400 --ultn 150
  python3 weak_probe.py ... --shard 0/2   # two processes, merge with --merge
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time

from scpage import game

# One Match constructed per seed so `ultsFired` can be read off the fighters —
# AC.simulate()'s summary() does not expose it, and an unchecked ult-off run is
# worthless.
RUN_JS = r"""
([jobs, seeds, offId]) => {
  const byId = {}; for (const w of AC.WEAPONS) byId[w.id] = w;
  // The gate reads WEAPON_BY_ID via Fighter.w. Prove AC.WEAPONS is that same
  // object graph before relying on a mutation to it.
  const probe = new AC.Match(jobs[0][0], jobs[0][1], 1);
  if (probe.a.w !== byId[jobs[0][0]]) return { err: "AC.WEAPONS is not the sim's weapon table" };

  const saved = offId === null ? null : byId[offId].ult.charge;
  if (offId !== null) byId[offId].ult.charge = 1e9;
  const out = [];
  try {
    for (const [a, b] of jobs) {
      const wins = [];           // 1 = a won, per seed, in seed order
      let ua = 0, ub = 0, dur = 0;
      for (const s of seeds) {
        const m = new AC.Match(a, b, s >>> 0);
        const dt = AC.CONFIG.physics.dt;
        let guard = 0;
        while (!m.over && guard++ < 200000) m.step(dt);
        wins.push(m.winner === m.a ? 1 : 0);
        ua += m.a.ultsFired; ub += m.b.ultsFired; dur += m.t;
      }
      out.push({ a, b, wins, ua, ub, dur: dur / seeds.length });
    }
  } finally {
    if (offId !== null) byId[offId].ult.charge = saved;
  }
  return { out };
}
"""

META_JS = r"""
() => AC.WEAPONS.map(w => ({
  id: w.id, name: w.name, aff: w.aff, dmg: w.dmg,
  ultKind: w.ult.kind, ultName: w.ult.name, ultCharge: w.ult.charge,
}))
"""


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def seed_list(n, seed0):
    s = seed0 & 0xFFFFFFFF
    out = []
    for _ in range(n):
        s = (s * 1103515245 + 12345) & 0xFFFFFFFF
        out.append(s)
    return out


def chunk(page, jobs, seeds, off_id, errors, note):
    """Run jobs in slices so one evaluate() cannot run past the timeout."""
    res = []
    per = max(1, 40000 // max(1, len(seeds)))
    for i in range(0, len(jobs), per):
        sl = jobs[i:i + per]
        r = page.evaluate(RUN_JS, [sl, seeds, off_id])
        if r.get("err"):
            raise RuntimeError(r["err"])
        res.extend(r["out"])
        if errors:
            raise RuntimeError(f"page errors: {errors[:3]}")
        print(f"    {note}: {min(i + per, len(jobs))}/{len(jobs)} pairings",
              flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--n", type=int, default=400, help="seeds/pairing, baseline")
    ap.add_argument("--ultn", type=int, default=150, help="seeds/pairing, ult-off")
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--shard", default="0/1", help="i/k")
    ap.add_argument("--ultonly", default=None,
                    help="comma ids: run ult-off for these only (confirm pass)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    si, sk = (int(x) for x in a.shard.split("/"))
    path = pathlib.Path(a.game).resolve()
    t0 = time.time()

    with game(game_path=path) as (page, errors):
        meta = page.evaluate(META_JS)
        ids = [m["id"] for m in meta]
        base_seeds = seed_list(a.n, a.seed)
        ult_seeds = base_seeds[:a.ultn]          # nested, so ult-off is paired

        pairs = [(ids[i], ids[j])
                 for i in range(len(ids)) for j in range(i + 1, len(ids))]

        # Work list: baseline (off_id None) + one ult-off block per relic.
        off_ids = ids if not a.ultonly else [s.strip() for s in a.ultonly.split(",")]
        unknown = [x for x in off_ids if x not in ids]
        if unknown:
            raise SystemExit(f"unknown relic id(s): {unknown}")
        work = [(None, pairs)] + [
            (x, [p for p in pairs if x in p]) for x in off_ids
        ]
        # Flatten to pairing-level units so the shards are balanced.
        units = []
        for off_id, ps in work:
            for p in ps:
                units.append((off_id, p))
        mine = [u for k, u in enumerate(units) if k % sk == si]
        print(f"shard {si}/{sk}: {len(mine)} pairing-runs", flush=True)

        by_off = {}
        for off_id, p in mine:
            by_off.setdefault(off_id, []).append(p)

        results = {}
        for off_id, ps in by_off.items():
            seeds = base_seeds if off_id is None else ult_seeds
            tag = "baseline" if off_id is None else f"ult-off {off_id}"
            rows = chunk(page, ps, seeds, off_id, errors, tag)
            results[off_id or "__base__"] = rows

        if errors:
            raise RuntimeError(f"page errors: {errors[:3]}")

    pathlib.Path(a.out).write_text(json.dumps(
        {"meta": meta, "n": a.n, "ultn": a.ultn, "seed": a.seed,
         "shard": a.shard, "results": results,
         "secs": round(time.time() - t0, 1)}))
    print(f"shard {si} done in {time.time() - t0:.0f}s -> {a.out}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
