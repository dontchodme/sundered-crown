"""Does relic_rate on the built stage-5 link (no --set) reproduce the --set run on stage 3 exactly?
    python cmp_rr.py BUILT.json SET.json   -- compares every foe's rate, byType, rate/rateA/rateB, games, timeouts, dur."""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
bad = [k for k in ("rate", "rateA", "rateB", "games", "timeouts", "dur", "byType", "byFoe", "n", "seed0", "sides") if a[k] != b[k]]
print(f"{sys.argv[1].split('/')[-1]} (set {a['set']}) vs {sys.argv[2].split('/')[-1]} (set {b['set']}): "
      f"rate {100*a['rate']:.2f} / {100*b['rate']:.2f}  A {100*a['rateA']:.2f} / {100*b['rateA']:.2f}  "
      f"B {100*a['rateB']:.2f} / {100*b['rateB']:.2f}  dur {a['dur']:.4f} / {b['dur']:.4f}  foes {len(a['byFoe'])}  "
      + ("IDENTICAL" if not bad else f"DIFFER in {bad}"))
