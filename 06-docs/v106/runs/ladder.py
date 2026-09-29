"""v106 scratch: the ladder at the built blade (10.75), by type and by foe, beside
the shipped relic and the drain at 11 (Rick's other choice). relic_rate jsons,
both sides, blocks 2207 + 2317, 40 fights a foe."""
import json, re, sys, pathlib
W = pathlib.Path(sys.argv[1]); base = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
shape = dict(re.findall(r'\{ id:"([a-z]+)", name:"[^"]*", aff:"[^"]*", shape:"([a-z]+)"', base))
def pooled(stem):
    J = [json.load(open(W / f"{stem}_{b}.json")) for b in (2207, 2317)]
    foe = {f: sum(j["byFoe"][f] for j in J) / 2 for f in J[0]["byFoe"]}
    typ = {t: sum(j["byType"][t] for j in J) / 2 for t in J[0]["byType"]}
    return sum(j["rate"] for j in J) / 2, foe, typ
R, F, T = pooled("stage5_rr_built_b1075")
S, SF, ST = pooled("ship_rr")
E, EF, ET = pooled("stage5_rr_d11")
order = sorted(T, key=lambda t: -T[t])
print(f"Widowmaker / Exsanguinate (sc-widowmaker-b1075: the drain, blade 10.75, the blade that holds the shipped rate)\n"
      f"win by foe, both sides, relic_rate seed0 2207 + 2317 (40 fights a foe: 10 seeds x 2 sides x 2 blocks). Pooled: {100*R:.1f}%.\n"
      f"Beside it: the SHIPPED relic (the nova, 11.95) on the base, pooled {100*S:.1f}%, and the drain at 11 (the crossing,\n"
      f"Rick's other choice under v76 6.2), pooled {100*E:.1f}%.\n")
print("by type   " + "  ".join(f"{t} {100*T[t]:.0f}%" for t in order))
print("shipped   " + "  ".join(f"{t} {100*ST[t]:.0f}%" for t in order))
print("at 11     " + "  ".join(f"{t} {100*ET[t]:.0f}%" for t in order))
print(f"\n{'foe':<13} {'shape':<11} {'drain 10.75':>11} {'shipped':>8} {'move':>6} {'at 11':>7}")
for f in sorted(F, key=lambda f: (F[f], f)):
    print(f"{f:<13} {shape.get(f,'?'):<11} {100*F[f]:>10.1f}% {100*SF[f]:>7.1f}% {100*(F[f]-SF[f]):>+6.1f} {100*EF[f]:>6.1f}%")
