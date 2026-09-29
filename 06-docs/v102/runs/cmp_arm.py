# Compare a built link's SHIP arm with a lab arm, foe for foe (win rate) and blow counts.
import json, sys
lab, larm, built = sys.argv[1], sys.argv[2], sys.argv[3]
L = json.load(open(lab))["arms"][larm]; B = json.load(open(built))["arms"]["SHIP"]
diff = [k for k in L["byFoe"] if abs(L["byFoe"][k] - B["byFoe"].get(k, -9)) > 1e-12]
same = (not diff and set(L["byFoe"]) == set(B["byFoe"]) and L["n"] == B["n"] and abs(L["win"] - B["win"]) < 1e-12
        and abs(L["hitsIn"] - B["hitsIn"]) < 1e-9 and abs(L["hitsOut"] - B["hitsOut"]) < 1e-9)
print(f"lab arm {larm} {L['win']:.4f} n {L['n']} hits {L['hitsIn']:.4f}/{L['hitsOut']:.4f}  |  built SHIP {B['win']:.4f} n {B['n']} "
      f"hits {B['hitsIn']:.4f}/{B['hitsOut']:.4f}  casts {L['casts']:.3f}/{B['casts']:.3f}  |  foes differing {len(diff)} of {len(L['byFoe'])}"
      + ("  IDENTICAL, foe for foe and blow for blow" if same else "  " + ", ".join(f"{k} {L['byFoe'][k]:.2f}->{B['byFoe'].get(k,-1):.2f}" for k in diff[:8])))
