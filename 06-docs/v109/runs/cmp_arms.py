"""Compare one arm of two ult_overlay jsons: win, blows in/out, stats, and every foe's rate.
    python cmp_arms.py LAB.json ARM BUILT.json ARM2"""
import json, sys
a = json.load(open(sys.argv[1]))["arms"][sys.argv[2]]
b = json.load(open(sys.argv[3]))["arms"][sys.argv[4]]
same = all(abs(a["byFoe"][k] - b["byFoe"].get(k, -1)) < 1e-12 for k in a["byFoe"]) and set(a["byFoe"]) == set(b["byFoe"])
print(f"  {sys.argv[2]:>5} win {a['win']:.4f}  hits {a['hitsIn']:.4f}/{a['hitsOut']:.4f}  casts {a['casts']:.3f}  n {a['n']}")
print(f"  {sys.argv[4]:>5} win {b['win']:.4f}  hits {b['hitsIn']:.4f}/{b['hitsOut']:.4f}  casts {b['casts']:.3f}  n {b['n']}")
diff = [k for k in a["byFoe"] if abs(a["byFoe"][k] - b["byFoe"].get(k, -1)) > 1e-12]
print(f"  every foe's rate identical: {same}   blows identical: {a['hitsIn']==b['hitsIn'] and a['hitsOut']==b['hitsOut']}   foes differing: {diff}")
