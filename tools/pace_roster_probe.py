#!/usr/bin/env python3
"""Roster-wide duration at a pace cell -- every pairing, not pace_sweep's ten.

    python pace_roster_probe.py --game ../02-chain/sc-lastthree.html --cells 1.0:1.0,1.27:1.27 --n 3

pace_sweep.py prices a cell on ten old pairings; Rick's "average" is the
roster. This runs the same SWEEP_JS over every pairing on the build so the
mean, p90, max and the worst PAIRING are the roster's numbers. The timeout is
kept and scaled with the clock (pace_sweep removes it), so the t/out column
can come back non-zero -- that is the check that can fail.
"""
from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game
from pace_sweep import SWEEP_JS, BASE_JS


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--cells", default="1.0:1.0", help="S:H, comma separated")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--seed0", type=int, default=25064)
    ap.add_argument("--json")
    a = ap.parse_args()
    path = resolve_game(a.game)
    cells = [tuple(float(x) for x in c.split(":")) for c in a.cells.split(",")]
    seeds = [(a.seed0 + i * 7919) & 0xFFFFFFFF for i in range(a.n)]
    out = {}
    with game(game_path=path) as (page, errors):
        base = page.evaluate(BASE_JS)
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pairs = [f"{x}:{y}" for x, y in itertools.combinations(ids, 2)]
        print(f"{len(ids)} relics, {len(pairs)} pairings x {len(seeds)} seeds = "
              f"{len(pairs)*len(seeds)} fights per cell; source baseHP {base['hp']} "
              f"seals {base['acts'][1]}/{base['acts'][2]} timeout {base['timeout']}")
        print(f"  {'S':>5}{'H':>6}{'baseHP':>8}{'seal2':>7}{'seal3':>7}{'t/o':>6}"
              f"{'mean':>7}{'med':>7}{'p90':>7}{'max':>7}{'t/out':>7}{'unres':>6}"
              f"{'ults':>6}   worst pairing")
        for S, H in cells:
            rows = page.evaluate(SWEEP_JS, [pairs, seeds, H, S, False])
            d = sorted(r["t"] for r in rows)
            by = {}
            for r in rows:
                by.setdefault((r["a"], r["b"]), []).append(r["t"])
            worst = max(by.items(), key=lambda kv: statistics.mean(kv[1]))
            # Per-relic roster winrate. n = (relics-1) * seeds fights each, so
            # at --n 3 that is ~96 fights and +/-5pp: enough to name a relic
            # that moved ten points, not enough to tune one. verify.py --n 40
            # on the pinned runtime is the gate.
            wins = {i: 0 for i in ids}
            for r in rows:
                if r["win"]:
                    wins[r["win"]] += 1
            per = (len(ids) - 1) * len(seeds)
            rates = {i: 100.0 * w / per for i, w in wins.items()}
            rec = dict(S=S, H=H, baseHP=round(base["hp"] * H),
                       seal2=base["acts"][1] * S, seal3=base["acts"][2] * S,
                       timeout=base["timeout"] * S,
                       mean=statistics.mean(d), median=statistics.median(d),
                       p90=d[int(0.9 * (len(d) - 1))], max=d[-1],
                       timeouts=sum(1 for r in rows if r["reason"] == "timeout"),
                       unresolved=sum(1 for r in rows if not r["over"]),
                       ults=statistics.mean(r["casts"] for r in rows),
                       worst=("/".join(worst[0]), statistics.mean(worst[1])),
                       n=len(rows), winrates=rates)
            out[f"{S}:{H}"] = rec
            print(f"  {S:>5.2f}{H:>6.2f}{rec['baseHP']:>8}{rec['seal2']:>7.1f}"
                  f"{rec['seal3']:>7.1f}{rec['timeout']:>6.0f}{rec['mean']:>7.1f}"
                  f"{rec['median']:>7.1f}{rec['p90']:>7.1f}{rec['max']:>7.1f}"
                  f"{rec['timeouts']:>7}{rec['unresolved']:>6}{rec['ults']:>6.1f}"
                  f"   {rec['worst'][0]} {rec['worst'][1]:.1f}s", flush=True)
        if errors:
            print("! page errors:", *errors[:5], sep="\n  ")
            return 1
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
