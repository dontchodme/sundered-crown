# Review rounds 2-3 (round 3: + Cold Iron stage 6, sc-coldiron-temper-fx): the builder (stages 1,2,3,5 at blade 20.5) onto the other batch builds' current links; every composed
# diff must equal base -> b205 line for line (the +/- lines), and chain_audit must find all inserts on the composed tip.
import difflib, hashlib, pathlib, subprocess, sys
PY = "C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
B = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch")
L = B / "lodestone"; OUT = L / "ctl" / "compose205"; OUT.mkdir(parents=True, exist_ok=True)
T = pathlib.Path("C:/dev/sundered-crown/tools"); CH = pathlib.Path("C:/dev/sundered-crown/02-chain")
TIPS = [CH / "sc-tendril-fx.html", CH / "sc-onslaught-fx.html",
        B / "coldiron/links/sc-coldiron-temper-b93.html", B / "coldiron/links/sc-coldiron-temper-fx.html", B / "ironhail/links/sc-ironhail-b14.html",
        B / "lightkeeper/links/sc-lightkeeper-bulwark-b9.5.html", B / "widowmaker/links/sc-widowmaker-b1075.html",
        B / "angelus/links/sc-angelus-b9.html", B / "oracle/links/sc-oracle-sight.html"]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
def pm(a, b):
    d = difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
    return [x for x in d if x[:1] in "+-" and not x.startswith(("+++", "---"))]
want = pm((CH / "sc-tendril-t3.html").read_text(encoding="utf-8"), (L / "links/sc-lodestone-b205.html").read_text(encoding="utf-8"))
allok = True
for tip in TIPS:
    stem = tip.stem; prev = tip; print(f"=== on {stem} ({sha(tip)})"); ok = True
    for st in "1235":
        o = OUT / f"{stem}-{st}.html"
        if o.exists(): o.unlink()
        r = subprocess.run([PY, str(T / "lodestone_build.py"), "--stage", st, "--src", str(prev), "--out", str(o)], capture_output=True, text=True, cwd=T)
        if r.returncode: print(f"  stage {st} REFUSED:", (r.stdout + r.stderr).strip().splitlines()[-3:]); ok = False; break
        last = [x for x in r.stdout.splitlines() if "relics in the roster" in x or x.strip().startswith("out ")]
        print("  " + " | ".join(x.strip()[:140] for x in last)); prev = o
    if ok:
        got = pm(tip.read_text(encoding="utf-8"), prev.read_text(encoding="utf-8"))
        same = got == want
        print(f"  the composed diff is the base->b205 diff, line for line: {same} ({len(got)} +/- lines)")
        r = subprocess.run([PY, str(T / "chain_audit.py"), "--relic", str(prev), "--tip", str(prev), "--builder", "lodestone_build.py"], capture_output=True, text=True, cwd=T)
        tail = [x for x in r.stdout.splitlines() if "SURVIVE" in x or "MISSING" in x or "FAIL" in x]
        print("  chain_audit:", tail[-1] if tail else r.stdout.strip().splitlines()[-1:], f"rc={r.returncode}")
        ok = same and r.returncode == 0
    allok &= ok
print("\nALL COMPOSE" if allok else "\nCOMPOSE FAILED")
