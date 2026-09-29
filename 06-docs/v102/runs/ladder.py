# The ladder: win by foe and by type, both sides, two relic_rate blocks pooled.
import json, sys
a, b, out, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
A, B = json.load(open(a)), json.load(open(b))
foes = sorted(A["byFoe"], key=lambda k: (A["byFoe"][k] + B["byFoe"][k], k))
bt = {k: (A["byType"][k] + B["byType"][k]) / 2 for k in A["byType"]}
L = [f"Lodestone / Rebuttal ({title}) win by foe, both sides, relic_rate seed0 {A['seed0']} + {B['seed0']}",
     f"(40 fights a foe: 10 seeds x 2 sides x 2 blocks). Pooled: {(A['rate'] + B['rate']) / 2:.1%}   side A {(A['rateA'] + B['rateA']) / 2:.1%}   side B {(A['rateB'] + B['rateB']) / 2:.1%}   mean {(A['dur'] + B['dur']) / 2:.1f}s",
     "", "by type  " + "  ".join(f"{k} {v:.0%}" for k, v in sorted(bt.items(), key=lambda kv: -kv[1])), ""]
L += [f"{k:<15} {100 * (A['byFoe'][k] + B['byFoe'][k]) / 2:5.1f}%" for k in foes]
open(out, "w").write("\n".join(L) + "\n"); print("\n".join(L))
