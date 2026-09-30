"""The lab's `patches` against its `hitsIn`, per fight (review note, 2026-09-30). Reads the full scratch jsons
(per-fight rows) of stage 0 and the dur-9.17 control; prints per arm and block the two per-cast counts and the
per-fight difference, split by the fight's outcome. ult_overlay.py closes the window on a death BEFORE it calls
onFrame, so the lab never plants on the killing blow; hitsIn counts it."""
import json, collections, sys, pathlib
R = pathlib.Path(sys.argv[1])
print(__doc__.strip()); print()
print(f"{'run':<22}{'arm':<4}{'fights':>7}{'casts/f':>9}{'hitsIn/cast':>13}{'patches/cast':>14}{'gap/cast':>10}   hitsIn-patches by (diff, win)")
for f in ["s0_ASBC_2207", "s0_ASBC_2317", "lab_dur917_2207", "lab_dur917_2317"]:
    d = json.load(open(R / (f + ".json")))
    for arm in ("B", "C"):
        rs = [r for r in d["rows"] if r["arm"] == arm]
        n = len(rs); c = sum(r["casts"] for r in rs); hi = sum(r["hitsIn"] for r in rs); pa = sum(r["S"].get("patches", 0) for r in rs)
        dw = collections.Counter((r["hitsIn"] - r["S"].get("patches", 0), r["win"]) for r in rs)
        print(f"{f:<22}{arm:<4}{n:>7}{c/n:>9.2f}{hi/c:>13.3f}{pa/c:>14.3f}{(hi-pa)/c:>10.3f}   " +
              "  ".join(f"diff {k[0]} {'won' if k[1]==1 else 'lost' if k[1]==0 else 'draw'}: {v}" for k, v in sorted(dw.items())))
