"""CHAIN_AUDIT for the picture rows (ce_chain.py's pattern). tools/chain_audit.py reads a builder's insert table;
the rows are not a builder, so hw_table.py (scratch) holds them as (label, anchor, code) tuples straight out of
rows_final.json. Relic = hw-final-fx.html (b11 + the rows + SPECS.heartwood out). Tips: Heartwood's stages 1,2,3,5
rebuilt by tools/heartwood_build.py --src <tip>, then Heartwood's voice rows if on disk, then these rows, then the
spec out, on (a) the base's own tip sc-tendril-t3, (b) sc-tendril-fx (the first with Tendril's root, which the
root reuses), (c) the newest 02-chain file sc-spellbreaker-fxout. CONTROL that must fail: the base link (no rows)
as the tip. usage: hw_chain.py. SCRATCH."""
import json, pathlib, subprocess, sys, os, hashlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import hw_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
TOOLS = pathlib.Path(r"C:\dev\sundered-crown\tools"); REPO = TOOLS.parent
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
R = json.loads((HERE / "rows_final.json").read_bytes().decode("utf-8"))
VP = HERE.parent / "stage6-voice" / "rows_final.json"
V = json.loads(VP.read_bytes().decode("utf-8")) if VP.exists() else []
print("voice rows:", VP, len(V) if V else "(not on disk yet)")
tab = "ROWS = [\n" + "".join(f"    ({json.dumps(r['label'])}, {json.dumps(r['anchor'])}, {json.dumps(r['code'])}),\n" for r in R) + "]\n"
(HERE / "hw_table.py").write_text('"""the picture rows as an insert table, for chain_audit (scratch)."""\n' + tab, encoding="utf-8")


def ap(s, rows):
    for r in rows:
        s = P.one(s, r["anchor"], r["code"], r["mode"], r["label"])
    return s


def carry(tip: pathlib.Path, name: str):
    d = HERE / "carry" / ("chain-" + name); d.mkdir(parents=True, exist_ok=True)
    src = tip
    for st, nm in (("1", "stub"), ("2", "root"), ("3", "rootfast"), ("5", "b11")):
        o = d / f"sc-heartwood-{nm}.html"
        p = subprocess.run([PY, str(TOOLS / "heartwood_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(TOOLS))
        assert p.returncode == 0 and o.exists(), (name, st, p.stdout[-300:], p.stderr[-300:])
        src = o
    s = src.read_bytes().decode("utf-8")
    s = ap(ap(s, V), R)
    s, _, _ = P.fx_out(s)
    P.syntax_check(s)
    out = HERE / "carry" / f"chain_tip_{name}.html"
    out.write_bytes(s.encode("utf-8"))
    for f in d.glob("*.html"): f.unlink()
    d.rmdir()
    return out


tips = [carry(REPO / "02-chain" / "sc-tendril-t3.html", "t3"),
        carry(REPO / "02-chain" / "sc-tendril-fx.html", "tendrilfx"),
        carry(REPO / "02-chain" / "sc-spellbreaker-fxout.html", "sbfxout"),
        P.BASE]
bad = 0
for i, t in enumerate(tips):
    ctl = i == len(tips) - 1
    print(("=== CONTROL (must report LOST): " if ctl else "=== ") + f"{t.name} ({sha(t)})", flush=True)
    p = subprocess.run([PY, str(TOOLS / "chain_audit.py"), "--relic", str(HERE / "hw-final-fx.html"), "--tip", str(t),
                        "--builder", str(HERE / "hw_table.py")], capture_output=True, text=True, cwd=str(TOOLS),
                       encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print(p.stdout.strip()); print("exit", p.returncode, flush=True)
    if (p.returncode == 0) == ctl: bad += 1
print("CHAIN AUDIT:", "PASS (3 tips survive, the control fails)" if not bad else f"FAIL ({bad})")
