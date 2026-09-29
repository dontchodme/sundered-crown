"""The ladder from relic_rate jsons: pool two blocks (seed0 2207 + 2317) of one point, print by
type and by foe (40 fights a foe: 10 seeds x 2 sides x 2 blocks), with a reference beside it.
    python ladder.py <label> <pointA_2207.json> <pointA_2317.json> [<ref label> <ref_2207> <ref_2317>]"""
import json, sys
def pool(p1, p2):
    a, b = json.load(open(p1)), json.load(open(p2))
    foes = {k: (a["byFoe"][k] + b["byFoe"][k]) / 2 for k in a["byFoe"]}
    types = {k: (a["byType"][k] + b["byType"][k]) / 2 for k in a["byType"]}
    return a, b, foes, types
lab = sys.argv[1]; a, b, foes, types = pool(sys.argv[2], sys.argv[3])
ref = None
if len(sys.argv) > 6: rlab = sys.argv[4]; ra, rb, rfoes, rtypes = pool(sys.argv[5], sys.argv[6]); ref = True
print(f"LADDER  {lab}: pooled {(a['rate'] + b['rate']) / 2:.1%} ({a['rate']:.1%} / {b['rate']:.1%}), "
      f"side A {(a['rateA'] + b['rateA']) / 2:.1%}, side B {(a['rateB'] + b['rateB']) / 2:.1%}, "
      f"mean {(a['dur'] + b['dur']) / 2:.1f}s" + (f"   | {rlab}: {(ra['rate'] + rb['rate']) / 2:.1%}" if ref else ""))
print("\nBY TYPE (the relic's rate against each type)" + ("        [reference]" if ref else ""))
for k, v in sorted(types.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<12} {v:6.1%}" + (f"   [{rtypes[k]:6.1%}]  {100 * (v - rtypes[k]):+5.1f}" if ref else ""))
print("\nBY FOE (40 fights a foe)" + ("        [reference]" if ref else ""))
for k, v in sorted(foes.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<14} {v:6.1%}" + (f"   [{rfoes[k]:6.1%}]  {100 * (v - rfoes[k]):+6.1f}" if ref else ""))
