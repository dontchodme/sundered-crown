"""v106 scratch: the builder re-applied on LATER tips carrying other new relics
(round 3: the builder after its docstring moved; plus the real chain tip). For each tip: stages 1 / 2 / 5,
and the build's added/removed lines against that tip compared with the same on
the base -- the same lines in the same order."""
import difflib, hashlib, pathlib, subprocess, sys, shutil
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
T = pathlib.Path(r"C:/dev/sundered-crown/tools"); BASE = pathlib.Path(r"C:/dev/sundered-crown/02-chain/sc-tendril-t3.html")
PY = sys.executable
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:16]
def build(tip, d):
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    src, outs, logs = tip, [], []
    for st, name in (("1", "sc-widowmaker-stub.html"), ("2", "sc-widowmaker-drain.html"), ("5", "sc-widowmaker-b1075.html")):
        o = d / name
        r = subprocess.run([PY, "widowmaker_build.py", "--stage", st, "--src", str(src), "--out", str(o)], cwd=T, capture_output=True, text=True, encoding="utf-8")
        logs.append(r.stdout + r.stderr)
        if r.returncode: raise SystemExit(f"stage {st} on {tip.name} REFUSED:\n{r.stdout}{r.stderr}")
        outs.append(o); src = o
    return outs, "".join(logs)
def delta(a, b):
    A = a.read_text(encoding="utf-8").splitlines(); B = b.read_text(encoding="utf-8").splitlines()
    return [l for l in difflib.unified_diff(A, B, n=0, lineterm="") if l[:1] in "+-" and not l.startswith(("+++", "---"))]
print("v106 compose check, round 3 (the builder after the review-3 docstring edit, sha16 " + sha(T / "widowmaker_build.py") + "): widowmaker_build.py re-applied on LATER tips (scratch, not the chain)")
print(f"base = {BASE.name} {sha(BASE)}")
ob, _ = build(BASE, W / "compose7" / "base")
dB = delta(BASE, ob[-1])
print(f"  on the base: stages 1 / 2 / 5 {' / '.join(sha(o) for o in ob)}; +{sum(l[0]=='+' for l in dB)} -{sum(l[0]=='-' for l in dB)} lines")
print(f"  == the links in links/: {[sha(o) == sha(W / 'links' / o.name) for o in ob]}")
tips = [("(a) + lodestone_build.py 1,2 + ironhail_build.py 1,2", W / "compose3" / "sc-ironhail-hail.html"),
        ("(b) + lightkeeper_build.py 1,2,3,5 (Bulwark: Lightkeeper off the nova)", W / "compose4" / "sc-lightkeeper-bulwark-b9.5.html"),
        ("(c) (b) with Censer's nova row renamed in scratch (NO other relic a nova)", W / "compose4" / "sc-nonova-tip.html"),
        ("(d) THE REAL CHAIN TIP now (Bindweed stage 6, read only)", pathlib.Path(r"C:/dev/sundered-crown/02-chain/sc-tendril-fx.html"))]
for i, (what, tip) in enumerate(tips):
    outs, log = build(tip, W / "compose7" / "abcd"[i])
    d = delta(tip, outs[-1])
    kept = [l for l in log.splitlines() if "nova's tail kept" in l][:1]
    print(f"{what} -> {tip.name} {sha(tip)}")
    print(f"    stages 1 / 2 / 5: {' / '.join(sha(o) for o in outs)}; every anchor found once")
    print(f"    +{sum(l[0]=='+' for l in d)} -{sum(l[0]=='-' for l in d)}; the same lines in the same order as on the base: {d == dB}")
    if kept: print("    builder: " + kept[0].strip()[:200])
