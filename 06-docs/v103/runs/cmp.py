"""built vs lab: one built SHIP json against one lab arm json, foe by foe and blow counts."""
import json, sys
b, l, arm = sys.argv[1], sys.argv[2], sys.argv[3]
B = json.load(open(b))["arms"]["SHIP"]; L = json.load(open(l))["arms"][arm]
d = {k: (L["byFoe"][k], B["byFoe"].get(k)) for k in L["byFoe"] if abs(L["byFoe"][k] - B["byFoe"].get(k, -9)) > 1e-12}
print(f"lab {arm} {L['win']:.4f} (n {L['n']}, hits {L['hitsIn']:.4f}/{L['hitsOut']:.4f})   built {B['win']:.4f} (n {B['n']}, hits {B['hitsIn']:.4f}/{B['hitsOut']:.4f})")
print(f"  foes differing: {len(d)} of {len(L['byFoe'])}" + ("" if not d else "  " + ", ".join(f"{k} {v[0]:.2f}/{v[1]:.2f}" for k, v in list(d.items())[:12])))
tot = lambda A: A["hitsIn"] + A["hitsOut"]
print(f"  blows a fight: lab {tot(L):.6f}  built {tot(B):.6f}  {'IDENTICAL' if abs(tot(L)-tot(B)) < 1e-12 and not d and abs(L['win']-B['win']) < 1e-12 else 'DIFFERENT'}")
