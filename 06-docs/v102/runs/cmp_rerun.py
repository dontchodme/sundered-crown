# Review round 3: a lab/SHIP run re-run on the round-3 link (the row comment reworded) against the same run on the
# round-2 link: every arm's numbers (win, n, casts, blows, stats, byFoe) must be identical.
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
keys = ("win", "n", "casts", "hitsIn", "hitsOut", "stats", "byFoe")
res = []
for arm in a["arms"]:
    A, B = a["arms"][arm], b["arms"].get(arm, {})
    d = [k for k in keys if A.get(k) != B.get(k)]
    res.append(f"{arm} {A['win']:.4f}/{B.get('win', -1):.4f} " + ("identical" if not d else "DIFFERENT: " + ",".join(d)))
ok = all(r.endswith("identical") for r in res) and set(a["arms"]) == set(b["arms"])
print(f"{sys.argv[2].split('/')[-1].split(chr(92))[-1]}: " + "; ".join(res) + ("   IDENTICAL TO ROUND 2" if ok else "   NOT IDENTICAL"))
sys.exit(0 if ok else 1)
