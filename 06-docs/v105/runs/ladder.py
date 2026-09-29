"""Scratch (v105 §4): the stage-5 grid table and the ladder, from relic_rate --json files.

  python ladder.py grid <runs dir>                 # every stage5_rr_*.json, pooled by point
  python ladder.py ladder <a.json> <b.json> ...     # by type and by foe, pooled (40 fights a foe for 2 blocks)
  python ladder.py same <a.json> <b.json>           # two runs identical: every foe's rate and the mean duration
"""
import json, pathlib, re, sys
from collections import defaultdict


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def grid(d):
    pts = defaultdict(dict)
    for p in sorted(pathlib.Path(d).glob("stage5_rr_*.json")):
        m = re.match(r"stage5_rr_(.+)_(\d+)\.json", p.name)
        if not m:
            continue
        pts[m.group(1)][m.group(2)] = load(p)
    print(f"{'point':<14}{'block 2207':>11}{'block 2317':>11}{'pooled':>9}{'n':>6}{'side A':>8}{'side B':>8}{'mean s':>8}")
    for k in sorted(pts, key=lambda s: float(re.sub(r'[^0-9.]', '', s.split('_')[0]) or 0)):
        b = pts[k]
        g = sum(r["games"] for r in b.values())
        w = sum(r["rate"] * r["games"] for r in b.values()) / g
        wa = sum(r["rateA"] * r["games"] / 2 for r in b.values()) / (g / 2)
        wb = sum(r["rateB"] * r["games"] / 2 for r in b.values()) / (g / 2)
        dur = sum(r["dur"] * r["games"] for r in b.values()) / g
        c1 = f"{100*b['2207']['rate']:.1f}" if "2207" in b else "-"
        c2 = f"{100*b['2317']['rate']:.1f}" if "2317" in b else "-"
        print(f"{k:<14}{c1:>11}{c2:>11}{100*w:>9.1f}{g:>6}{100*wa:>8.1f}{100*wb:>8.1f}{dur:>8.1f}")


def ladder(files):
    R = [load(p) for p in files]
    foes = R[0]["byFoe"].keys()
    per = 2 * R[0]["n"]                     # fights a foe a block (both sides)
    byFoe = {f: sum(r["byFoe"][f] for r in R) / len(R) for f in foes}
    print(f"THE LADDER: {R[0]['relic']} on {pathlib.Path(R[0]['game']).name}  set {R[0]['set']}  "
          f"{per * len(R)} fights a foe ({len(R)} blocks x {R[0]['n']} seeds x 2 sides)")
    types = defaultdict(list)
    shape = {}
    for r in R:
        for t in r["byType"]:
            types[t].append(r["byType"][t])
    print("  by type   " + "  ".join(f"{t} {100*sum(v)/len(v):.0f}%" for t, v in
                                   sorted(types.items(), key=lambda kv: -sum(kv[1]))))
    srt = sorted(byFoe.items(), key=lambda kv: kv[1])
    print("  by foe (worst first):")
    for i in range(0, len(srt), 6):
        print("    " + "   ".join(f"{f} {100*v:.1f}" for f, v in srt[i:i + 6]))
    tot = sum(r["rate"] * r["games"] for r in R) / sum(r["games"] for r in R)
    print(f"  pooled {100*tot:.1f}%   mean {sum(r['dur'] for r in R)/len(R):.1f}s")


def same(a, b):
    A, B = load(a), load(b)
    keys = ("rate", "rateA", "rateB", "games", "dur", "timeouts")
    diff = [k for k in keys if A[k] != B[k]] + [f for f in A["byFoe"] if A["byFoe"][f] != B["byFoe"].get(f)]
    print(f"{pathlib.Path(a).name} vs {pathlib.Path(b).name}: "
          + ("IDENTICAL (rate, sides, mean duration, timeouts, every foe of %d)" % len(A["byFoe"])
             if not diff else f"DIFFER: {diff[:8]}"))
    print(f"  {100*A['rate']:.2f}% / {100*B['rate']:.2f}%   mean {A['dur']:.4f} / {B['dur']:.4f}")
    return 0 if not diff else 1


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "grid":
        grid(sys.argv[2])
    elif cmd == "ladder":
        ladder(sys.argv[2:])
    elif cmd == "same":
        sys.exit(same(sys.argv[2], sys.argv[3]))
