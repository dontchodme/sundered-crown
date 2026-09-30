"""Compare two rf_lab.py runs FIGHT BY FIGHT: arm X of json 1 against arm Y of json 2, on the same
(foe, seed) set -- the winner, the duration to the step, the blows in and out of windows, the casts.
    python perfight_cmp.py <label> <json1> <armX> <json2> <armY>"""
import json, sys
label, j1, x, j2, y = sys.argv[1:6]
A = [r for r in json.load(open(j1))["rows"] if r["arm"] == x]
B = [r for r in json.load(open(j2))["rows"] if r["arm"] == y]
key = lambda r: (r["foe"], r["seed"])
a = {key(r): r for r in A}; b = {key(r): r for r in B}
F = ("win", "dur", "hitsIn", "hitsOut", "casts")
diff = [k for k in a if k not in b or any(a[k][f] != b[k][f] for f in F)]
ok = len(a) == len(b) == len(A) == len(B) and not diff
wa = sum(r["win"] == 1 for r in A); wb = sum(r["win"] == 1 for r in B)
ha = sum(r["hitsIn"] + r["hitsOut"] for r in A); hb = sum(r["hitsIn"] + r["hitsOut"] for r in B)
print(f"{label}: {len(A)} / {len(B)} fights; wins {wa} / {wb}; blows {ha} / {hb}; fights differing in winner, "
      f"duration (to the step), blows in/out or casts: {len(diff)}  -> "
      + ("IDENTICAL FIGHT BY FIGHT" if ok else "DIFFERENT: " + str(diff[:5])))
sys.exit(0 if ok else 1)
