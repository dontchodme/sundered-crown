"""The ult_overlay SHIP runs on the FIXED links (and their lab-clock controls) against the same runs on
the pre-review links (runs/prev/): every arm field ult_overlay writes (win, casts, blows in / out,
byFoe and the rest), both blocks. Identical => §2's built-vs-lab table and its controls stand.
    python built_same.py <runs dir>"""
import json, sys, os
S = sys.argv[1]
ok = True
for tag in ("built_stun", "built_unm", "ctl_stun", "ctl_unm"):
    for B in ("2207", "2317"):
        p1, p0 = f"{S}/{tag}_{B}.json", f"{S}/prev/{tag}_{B}.json"
        if not os.path.exists(p1): print(f"{tag}_{B}: not run yet"); ok = False; continue
        a, b = json.load(open(p0)), json.load(open(p1))
        A, Bm = a["arms"]["SHIP"], b["arms"]["SHIP"]
        d = sorted(k for k in set(A) | set(Bm) if A.get(k) != Bm.get(k))
        ok &= not d
        print(f"{tag}_{B}: pre-review win {100*A['win']:.2f}%  fixed {100*Bm['win']:.2f}%  hits in/out {Bm.get('hitsIn', 0):.4f}/{Bm.get('hitsOut', 0):.4f}"
              f"  casts {Bm.get('casts', 0):.4f}  fields {len(A)}: " + ("IDENTICAL" if not d else f"DIFFER in {d}"))
print("THE FIXED LINKS PLAY THE PRE-REVIEW LINKS' FIGHTS" if ok else "NOT (YET) IDENTICAL")
