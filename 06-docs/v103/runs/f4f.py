"""STAGE 1 == ARM A, FIGHT FOR FIGHT (v103 §2; the review noted the ult_overlay jsons keep
per-foe rates, not fights). Runs ult_overlay.py's own JS (read from the file, unmodified) twice:
the lab's arm A on the base (widowmaker as dwarven:twinblade, overlays/anvil.js, winCap=9) and
the built stage 1's SHIP (coldiron, its ult stubbed at 1e9), the same 33 foes and 20 seeds, and
compares every fight: the winner, the duration in steps, the blows in and out of windows.
CONTROL THAT CAN FAIL: the same comparison with the built fights paired one seed off must
differ. usage: f4f.py <base> <stage1> <seed0> <out.json>"""
import json, pathlib, re, sys, time
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
base, s1, seed0, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
src = pathlib.Path("C:/dev/sundered-crown/tools/ult_overlay.py").read_text(encoding="utf-8")
JS = re.search(r'JS = r"""(.*?)"""', src, re.S).group(1)
MECH = pathlib.Path("C:/dev/sundered-crown/tools/overlays/anvil.js").read_text()
foes = pathlib.Path(__file__).with_name("foes33.txt").read_text().strip().split(",")
seeds = [seed0 + 11 * i for i in range(20)]
P = {"charge": 16.0, "dur": 8.0, "blade": None, "winCap": 9, "__chan": ["onHit", "sunder", 1]}
t0 = time.time()
def run(path, relic, cell, arm):
    with game(game_path=pathlib.Path(path).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        rows = page.evaluate(JS, [relic, cell, foes, seeds, 160.0, P, [arm], MECH])
        assert not errors, errors
    return ver, {(r["foe"], r["seed"]): (r["win"], round(r["dur"] * 120), r["hitsIn"], r["hitsOut"]) for r in rows}
ver, L = run(base, "widowmaker", ["dwarven", "twinblade"], "A")
_, B = run(s1, "coldiron", None, "SHIP")
diff = [k for k in L if L[k] != B.get(k)]
shift = {(f, s): B.get((f, s + 11)) for (f, s) in L if (f, s + 11) in B}
cdiff = sum(1 for k, v in shift.items() if L[k] != v)
n = len(L); winL = sum(v[0] for v in L.values() if v[0] >= 0) / sum(1 for v in L.values() if v[0] >= 0)
print(f"STAGE 1 v ARM A, FIGHT FOR FIGHT  block {seed0}  Chromium {ver}  {n} fights ({len(foes)} foes x {len(seeds)} seeds)")
print(f"  lab A {winL:.4f}   fights differing (winner, steps, blows in, blows out): {len(diff)} of {n}"
      + ("" if not diff else "  e.g. " + ", ".join(f"{k}: {L[k]} / {B.get(k)}" for k in diff[:4])))
print(f"  mean steps {sum(v[1] for v in L.values())/n:.2f} / {sum(v[1] for v in B.values())/n:.2f}   "
      f"blows a fight {sum(v[2]+v[3] for v in L.values())/n:.6f} / {sum(v[2]+v[3] for v in B.values())/n:.6f}")
print(f"  CONTROL (built paired one seed off): {cdiff} of {len(shift)} differ -> {'the comparison can fail' if cdiff else 'CONTROL DID NOT FAIL'}")
print(f"  {'IDENTICAL, FIGHT FOR FIGHT' if not diff and cdiff else 'NOT IDENTICAL'}   {time.time()-t0:.0f}s")
pathlib.Path(outp).write_text(json.dumps({"block": seed0, "n": n, "differ": len(diff), "control_differ": cdiff,
    "lab": {f"{k[0]}:{k[1]}": v for k, v in L.items()}, "built": {f"{k[0]}:{k[1]}": v for k, v in B.items()}}))
sys.exit(0 if not diff and cdiff else 1)
