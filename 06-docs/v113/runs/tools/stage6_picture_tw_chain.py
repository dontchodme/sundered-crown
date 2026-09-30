"""CHAIN_AUDIT for the picture rows (ce_chain.py's pattern). tools/chain_audit.py reads a builder's insert table; the
rows are not a builder, so tw_table.py (scratch) holds them as (label, anchor, code) tuples straight out of
rows_final.json. The two cut rows add no text (they cut `thornwake: 2.4, ` and `thornwake:1, `), so there is nothing
for a marker to find: they are checked here instead, by the tokens' absence at each tip. Relic = tw-final-fx.html (the
rows + SPECS.thornwake out). Tips: Thornwake's stages 1/2/3/5 rebuilt by tools/thornwake_build.py --src <tip>, then
these rows, then the spec out (tw_rows.fx_out: the page fx_remove.py computes), on (a) the real base tip
sc-tendril-t3, (b) sc-tendril-fx (Tendril's picture and its guard), (c) the batch line's newest link
sc-spellbreaker-fxout. CONTROL that must fail: the base link (no rows) as the tip. usage: tw_chain.py. SCRATCH."""
import json, pathlib, subprocess, sys, os
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import idle  # noqa
import tw_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
TOOLS = pathlib.Path(r"C:\dev\sundered-crown\tools")
REPO = TOOLS.parent
R = json.loads((HERE / "rows_final.json").read_bytes().decode("utf-8"))
T = [r for r in R if r["code"]]
tab = "ROWS = [\n" + "".join(f"    ({json.dumps(r['label'])}, {json.dumps(r['anchor'])}, {json.dumps(r['code'])}),\n" for r in T) + "]\n"
(HERE / "tw_table.py").write_text('"""the picture rows as an insert table, for chain_audit (scratch)."""\n' + tab, encoding="utf-8")
CUT = [r for r in R if not r["code"]]


def ap(s, rows):
    for r in rows:
        s = P.one(s, r["anchor"], r["code"], r["mode"], r["label"])
    return s


def carry(tip: pathlib.Path, name: str):
    d = HERE / "carry" / ("chain-" + name); d.mkdir(parents=True, exist_ok=True)
    src = tip
    for st in "1235":
        o = d / f"sc-thornwake-carry-s{st}.html"
        p = subprocess.run([PY, str(TOOLS / "thornwake_build.py"), "--stage", st, "--src", str(src), "--out", str(o)],
                           capture_output=True, text=True, cwd=str(TOOLS))
        assert p.returncode == 0 and o.exists(), (name, st, p.stdout[-300:], p.stderr[-300:])
        src = o
    s = src.read_bytes().decode("utf-8")
    s = ap(s, R)
    s, _, _, _ = P.fx_out(s)
    P.syntax_check(s)
    out = HERE / f"chain_tip_{name}.html"
    out.write_bytes(s.encode("utf-8"))
    for f in d.glob("*.html"): f.unlink()
    return out


tips = [carry(REPO / "02-chain" / "sc-tendril-t3.html", "t3"),
        carry(REPO / "02-chain" / "sc-tendril-fx.html", "tendrilfx"),
        carry(REPO / "02-chain" / "sc-spellbreaker-fxout.html", "sbfxout"),
        (HERE.parent / "links" / "sc-thornwake-b26.5.html").resolve()]
bad = 0
for i, t in enumerate(tips):
    ctl = i == len(tips) - 1
    print(("=== CONTROL (must report LOST): " if ctl else "=== ") + t.name, flush=True)
    p = subprocess.run([PY, str(TOOLS / "chain_audit.py"), "--relic", str(HERE / "tw-final-fx.html"), "--tip", str(t),
                        "--builder", str(HERE / "tw_table.py")], capture_output=True, text=True, cwd=str(TOOLS), encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print(p.stdout.strip()); print("exit", p.returncode, flush=True)
    s = t.read_bytes().decode("utf-8")
    for r in CUT:
        gone = s.count(r["anchor"]) == 0
        print(f"    {'ok ' if gone else 'NOT CUT'}  {r['label']}: '{r['anchor']}' {s.count(r['anchor'])}x at the tip")
        if not ctl and not gone: bad += 1
    spec = s.count(P.FX_BLOCK)
    print(f"    SPECS.thornwake block at the tip: {spec}x {'(out, as the carry takes it)' if not ctl else '(the control keeps it)'}")
    if not ctl and spec: bad += 1
    if (p.returncode == 0) == ctl: bad += 1
print("CHAIN AUDIT:", "PASS (3 tips survive, the control fails)" if not bad else f"FAIL ({bad})")
