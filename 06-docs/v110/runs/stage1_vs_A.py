"""Stage 1 (sc-aureole-stub, its own stubbed ultimate = the SHIP arm) against the lab's arm A on
the base, FIGHT BY FIGHT (labx.py keeps every fight's row): winner, duration to the step, blows
in and out of windows, casts. Also the json byFoe and blow totals."""
import json, sys
S = sys.argv[1]
print("STAGE 1 (sc-aureole-stub, SHIP arm = its own stubbed ultimate) AGAINST THE LAB'S ARM A (base), FIGHT BY FIGHT")
print("(labx.py = ult_overlay.py + census + every fight's row; 33 foes x 20 seeds, Aureole side A)\n")
allok = True
for B in ("2207", "2317"):
    LA = json.load(open(f"{S}/lx_ABC_{B}.json")); LS = json.load(open(f"{S}/pf_stub_{B}.json"))
    A = [r for r in LA["rows"] if r["arm"] == "A"]; T = LS["rows"]
    key = lambda r: (r["foe"], r["seed"])
    a = {key(r): r for r in A}; t = {key(r): r for r in T}
    diff = [k for k in a if k not in t or any(a[k][f] != t[k][f] for f in ("win", "dur", "hitsIn", "hitsOut", "casts"))]
    ok = len(a) == len(t) == len(A) == len(T) == 660 and not diff
    aA, aS = LA["arms"]["A"], LS["arms"]["SHIP"]
    same_foe = aA["byFoe"] == aS["byFoe"]
    same_tot = (aA["win"], aA["hitsIn"], aA["hitsOut"], aA["casts"]) == (aS["win"], aS["hitsIn"], aS["hitsOut"], aS["casts"])
    ok = ok and same_foe and same_tot
    allok &= ok
    wa = sum(r["win"] == 1 for r in A); wt = sum(r["win"] == 1 for r in T)
    print(f"block {B}: {len(A)} / {len(T)} fights; wins {wa} / {wt} ({aA['win']:.4f} / {aS['win']:.4f}); blows a fight "
          f"{aA['hitsOut']:.6f} / {aS['hitsOut']:.6f}; byFoe identical: {same_foe}; fights differing in winner, "
          f"duration (to the step), blows in/out or casts: {len(diff)}  -> {'IDENTICAL FIGHT BY FIGHT' if ok else 'DIFFERENT: ' + str(diff[:5])}")
print("\nSTAGE 1 IS ARM A FIGHT BY FIGHT" if allok else "\nSTAGE 1 IS NOT ARM A")
sys.exit(0 if allok else 1)
