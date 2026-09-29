"""The ladder (v109 §4): Consecration's win by foe and by type, both sides, two blocks, beside the shipped nova on
the same seeds. From relic_rate jsons; each foe has the same number of fights, so a type is the mean of its foes.
    python ladder.py LABEL BUILT_2207.json BUILT_2317.json [REF_2207.json REF_2317.json]"""
import json, re, sys, pathlib
lab = sys.argv[1]
b1, b2 = (json.load(open(p)) for p in sys.argv[2:4])
r1, r2 = (json.load(open(p)) for p in (sys.argv[4:6] if len(sys.argv) > 5 else ("ref_shipped_rr_2207.json", "ref_shipped_rr_2317.json")))
src = pathlib.Path("C:/dev/sundered-crown/02-chain/sc-tendril-t3.html").read_text(encoding="utf-8")
shape = dict(re.findall(r'\{ id:"([a-z]+)", name:"[^"]*", aff:"[^"]*", shape:"([a-z]+)"', src))
def pool(j1, j2): return {f: (j1["byFoe"][f] + j2["byFoe"][f]) / 2 for f in j1["byFoe"]}
def rate(j1, j2): return (j1["rate"] * j1["games"] + j2["rate"] * j2["games"]) / (j1["games"] + j2["games"])
B, R = pool(b1, b2), pool(r1, r2)
assert set(B) == set(R) and all(f in shape for f in B), "foe sets differ"
def types(P):
    t = {}
    for f, v in P.items(): t.setdefault(shape[f], []).append(v)
    return sorted(((k, sum(v) / len(v)) for k, v in t.items()), key=lambda kv: -kv[1])
per = 2 * b1["n"] * len(b1["sides"])
print(f"Censer / Consecration ({lab}) win by foe, both sides,\nrelic_rate seed0 {b1['seed0']} + {b2['seed0']} "
      f"({per} fights a foe: {b1['n']} seeds x {len(b1['sides'])} sides x 2 blocks). Beside it, the SHIPPED nova on the base\n"
      f"(sc-tendril-t3, blade 28.77, the same seeds). Pooled: Consecration {100*rate(b1, b2):.1f}%   shipped nova {100*rate(r1, r2):.1f}%\n")
print("by type   " + "  ".join(f"{k} {100*v:.0f}%" for k, v in types(B)))
print("shipped   " + "  ".join(f"{k} {100*v:.0f}%" for k, v in types(R)))
print(f"\n{'foe':13} {'type':11} {'Consecration':>8} {'shipped':>8} {'move':>7}")
for f in sorted(B, key=lambda f: (B[f], f)):
    print(f"{f:13} {shape[f]:11} {100*B[f]:7.1f}% {100*R[f]:7.1f}% {100*(B[f]-R[f]):+6.1f}")
