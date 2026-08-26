#!/usr/bin/env python3
"""Merge weak_probe shards into the two-axis table that picks the next ult.

    python3 weak_report.py /tmp/wp0.json /tmp/wp1.json

Prints, per relic: winrate with a Wilson 95% interval, the same winrate with
its own ultimate disabled on paired seeds, and the difference — the ult's
contribution in percentage points. Separation between two relics is reported
against the interval, not eyeballed off the bar chart, because the whole point
of this pass is that `verify.py --n 60` cannot tell the floor apart.
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main(paths):
    shards = [json.load(open(p)) for p in paths]
    meta = {m["id"]: m for m in shards[0]["meta"]}
    n, ultn = shards[0]["n"], shards[0]["ultn"]

    # blocks[off_id][(a,b)] = row
    blocks = defaultdict(dict)
    for sh in shards:
        assert sh["n"] == n and sh["ultn"] == ultn and sh["seed"] == shards[0]["seed"], \
            "shards disagree on n/ultn/seed"
        for off, rows in sh["results"].items():
            for r in rows:
                key = (r["a"], r["b"])
                assert key not in blocks[off], f"duplicate pairing {key} in {off}"
                blocks[off][key] = r

    base = blocks["__base__"]
    assert len(base) == 120, f"baseline has {len(base)} pairings, expected 120"

    # --- axis 1: winrate on the full baseline round robin
    wins = defaultdict(int)
    games = defaultdict(int)
    ults = defaultdict(int)
    for (a, b), r in base.items():
        aw = sum(r["wins"])
        wins[a] += aw
        wins[b] += len(r["wins"]) - aw
        games[a] += len(r["wins"])
        games[b] += len(r["wins"])
        ults[a] += r["ua"]
        ults[b] += r["ub"]

    # --- axis 2: paired ult-off
    off_stats = {}
    for x in meta:
        rows = blocks.get(x)
        if not rows:
            continue
        assert len(rows) == 15, f"{x} ult-off has {len(rows)} pairings"
        ow = og = 0
        fired = 0
        bw = bg = 0          # baseline restricted to the SAME seeds, for pairing
        flips_lost = flips_won = 0
        for (a, b), r in rows.items():
            k = len(r["wins"])
            xa = (x == a)
            ow += sum(r["wins"]) if xa else k - sum(r["wins"])
            og += k
            fired += r["ua"] if xa else r["ub"]
            br = base[(a, b)]
            bwins = br["wins"][:k]
            bw += sum(bwins) if xa else k - sum(bwins)
            bg += k
            for i in range(k):
                xo = r["wins"][i] if xa else 1 - r["wins"][i]
                xb = bwins[i] if xa else 1 - bwins[i]
                if xb == 1 and xo == 0:
                    flips_lost += 1
                elif xb == 0 and xo == 1:
                    flips_won += 1
        off_stats[x] = dict(ow=ow, og=og, fired=fired, bw=bw, bg=bg,
                            flips_lost=flips_lost, flips_won=flips_won)

    rows = []
    for x, m in meta.items():
        wr = wins[x] / games[x]
        lo, hi = wilson(wins[x], games[x])
        o = off_stats.get(x)
        rows.append(dict(
            id=x, name=m["name"], kind=m["ultKind"], ult=m["ultName"],
            dmg=m["dmg"], aff=m["aff"],
            wr=wr * 100, lo=lo * 100, hi=hi * 100, games=games[x],
            ults_per_match=ults[x] / games[x],
            off=(o["ow"] / o["og"] * 100) if o else float("nan"),
            paired_on=(o["bw"] / o["bg"] * 100) if o else float("nan"),
            delta=((o["bw"] / o["bg"]) - (o["ow"] / o["og"])) * 100 if o else float("nan"),
            fired_off=o["fired"] if o else -1,
            flips=(o["flips_lost"], o["flips_won"]) if o else None,
        ))
    rows.sort(key=lambda r: r["wr"])

    # fired_off == -1 means no ult-off block was requested for that relic
    # (--ultonly confirm pass); only relics that actually ran are gated.
    bad = [r for r in rows if r["fired_off"] > 0]
    print(f"# weak_probe — baseline n={n}/pairing ({n*15} games per relic), "
          f"ult-off n={ultn} paired")
    print(f"# ult-off gate check: "
          + ("PASS — 0 ults fired in every ult-off block"
             if not bad else f"FAIL — {[(r['id'], r['fired_off']) for r in bad]}"))
    zero_ult = [r["id"] for r in rows if r["ults_per_match"] < 0.05]
    print(f"# baseline ult-fire check: "
          + ("PASS — every relic fires its ult"
             if not zero_ult else f"FAIL — never fires: {zero_ult}"))
    print()
    print(f"{'relic':14}{'ult':15}{'kind':10}"
          f"{'winrate':>8}{'95% CI':>16}{'ult-off':>9}{'ult worth':>11}"
          f"{'McNemar z':>11}")
    for r in rows:
        mc = ""
        if r["flips"]:
            b, c = r["flips"]            # b = lost by turning it off, c = won
            mc = (f"{(b - c) / math.sqrt(b + c):9.2f}"
                  if (b + c) else "      n/a")
            mc += " " if abs(b - c) / math.sqrt(b + c or 1) > 1.96 else "~"
        print(f"{r['name']:14}{r['ult']:15}{r['kind']:10}"
              f"{r['wr']:7.1f}%  [{r['lo']:4.1f},{r['hi']:4.1f}]"
              f"{r['off']:8.1f}%{r['delta']:+10.1f}pp{mc:>11}")
    print("  (~ marks an ult whose contribution is NOT distinguishable "
          "from zero at 95%)")

    print("\n# separation at the floor (is the bottom relic actually the bottom?)")
    floor = rows[0]
    for r in rows[1:6]:
        # paired difference across the 14 shared opponents, same seeds
        d = r["wr"] - floor["wr"]
        se = math.sqrt(
            floor["wr"] / 100 * (1 - floor["wr"] / 100) / floor["games"]
            + r["wr"] / 100 * (1 - r["wr"] / 100) / r["games"]) * 100
        print(f"  {r['name']:14} is {d:+5.2f}pp above {floor['name']}"
              f"   (se {se:.2f}pp, z={d/se:5.2f})"
              + ("  SEPARATED" if abs(d) > 1.96 * se else "  tied"))


if __name__ == "__main__":
    main(sys.argv[1:])
