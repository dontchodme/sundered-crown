"""Published (Chromium 141, sc-trunk, seed0 2207, 10 seeds) against the same 330 fights replayed on
151 (runs/s0_trunk151_n10.json), and against the tip on 151 (stage 0, 20 seeds, two blocks)."""
import json, sys
S = sys.argv[1]
pub = json.load(open("C:/dev/sundered-crown/06-docs/v82/runs/halo_base.json"))["arms"]
rep = json.load(open(f"{S}/s0_trunk151_n10.json"))["arms"]
t1 = json.load(open(f"{S}/s0_2207.json"))["arms"]; t2 = json.load(open(f"{S}/s0_2317.json"))["arms"]
print("arm    published 141 (sc-trunk, n10)   same fights on 151 (sc-trunk)   foes identical   tip on 151 (20 seeds, 1 / 2 -> pooled)")
for arm in ("A", "SHIP", "B", "C", "D"):
    p, r = pub[arm], rep[arm]
    same = sum(1 for k in p["byFoe"] if abs(p["byFoe"][k] - r["byFoe"].get(k, -1)) < 1e-9)
    print(f"{arm:<6} {100*p['win']:6.1f}                          {100*r['win']:6.1f}                         {same:>2}/{len(p['byFoe'])}"
          f"            {100*t1[arm]['win']:.1f} / {100*t2[arm]['win']:.1f} -> {50*(t1[arm]['win']+t2[arm]['win']):.1f}")
print("\nmechanism (per cast; f_ per fight):  published | trunk on 151 | tip on 151 block 1 / 2")
for arm in ("B", "C", "D"):
    for k in ("smite", "bless", "f_foeInPct", "f_foeStk", "arrowSmite"):
        if k in pub[arm]["stats"]:
            print(f"  {arm} {k:<11} {pub[arm]['stats'][k]:7.2f} | {rep[arm]['stats'][k]:7.2f} | {t1[arm]['stats'][k]:7.2f} / {t2[arm]['stats'][k]:7.2f}")
    print(f"  {arm} casts       {pub[arm]['casts']:7.2f} | {rep[arm]['casts']:7.2f} | {t1[arm]['casts']:7.2f} / {t2[arm]['casts']:7.2f}")
