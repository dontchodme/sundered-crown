"""Heartwood's stages 1,2,3,5 carried by tools/heartwood_build.py onto a 02-chain tip (the orchestrator's own
carry, dry, in scratch). usage: hw_carry.py <tip-name> [<tip-name>...] -> carry/hw-on-<tip>.html. SCRATCH."""
import hashlib, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
REPO = pathlib.Path(r"C:\dev\sundered-crown"); TOOLS = REPO / "tools"
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
for tip in sys.argv[1:]:
    src = REPO / "02-chain" / f"{tip}.html"; d = HERE / "carry" / f"tmp-{tip}"; d.mkdir(parents=True, exist_ok=True)
    cur = src
    for st, nm in (("1", "stub"), ("2", "root"), ("3", "rootfast"), ("5", "b11")):
        o = d / f"sc-heartwood-{nm}.html"
        r = subprocess.run([PY, str(TOOLS / "heartwood_build.py"), "--stage", st, "--src", str(cur), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(TOOLS))
        assert r.returncode == 0 and o.exists(), (tip, st, r.stdout[-400:], r.stderr[-400:])
        cur = o
    out = HERE / "carry" / f"hw-on-{tip}.html"
    out.write_bytes(cur.read_bytes())
    for f in d.glob("*.html"): f.unlink()
    d.rmdir()
    print(f"{tip} ({sha(src)}) -> {out.name} {sha(out)}")
