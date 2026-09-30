"""CHAIN_AUDIT for the picture rows (the lk_chain.py pattern). tools/chain_audit.py reads a builder's insert
table; the rows are not a builder, so gs_table.py (scratch) holds them as (label, anchor, code) tuples straight
out of rows_final.json. Relic = gs-final-fx.html (the rows + SPECS.oathwound out). Tips: Goreshard's stages
1/2/5 rebuilt by tools/goreshard_build.py --src <tip> (gs_order.py's carry/), then Goreshard's voice rows if any
are on disk (stage6-voice rows_final.json, else rows_lab.json), then these rows, then the spec out, on (a) the real
base tip sc-tendril-t3, (b) the batch line's newest link on disk, sc-spellbreaker-fxout, (c) sc-ironhail-fxout.
CONTROL that must fail: the base link (no rows) as the tip. usage: gs_chain.py. SCRATCH."""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import gs_rows as P
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"
TOOLS = pathlib.Path(r"C:\dev\sundered-crown\tools")
R = json.loads((HERE / "rows_final.json").read_bytes().decode("utf-8"))
VD = HERE.parent / "stage6-voice"
VP = VD / "rows_final.json" if (VD / "rows_final.json").exists() else VD / "rows_lab.json"
V = json.loads(VP.read_bytes().decode("utf-8")) if VP.exists() else []
if isinstance(V, dict): V = V.get("rows", [])
print("voice rows:", VP.name if VP.exists() else "none on disk", len(V))
tab = "ROWS = [\n" + "".join(f"    ({json.dumps(r['label'])}, {json.dumps(r['anchor'])}, {json.dumps(r['code'])}),\n" for r in R) + "]\n"
(HERE / "gs_table.py").write_text('"""the picture rows as an insert table, for chain_audit (scratch)."""\n' + tab, encoding="utf-8")


def ap(s, rows):
    for r in rows:
        s = P.one(s, r["anchor"], r["code"], r["mode"], r["label"])
    return s


def carry(s5: pathlib.Path, out: pathlib.Path):
    s = s5.read_bytes().decode("utf-8")
    s = ap(ap(s, V), R)
    s, _, _ = P.fx_out(s)
    P.syntax_check(s)
    out.write_bytes(s.encode("utf-8"))
    return out


tips = [carry(HERE / "carry" / "t3" / "sc-goreshard-b10.25.html", HERE / "chain_tip_t3.html"),
        carry(HERE / "carry" / "spellbreaker-fxout" / "sc-goreshard-b10.25.html", HERE / "chain_tip_sbfxout.html"),
        carry(HERE / "carry" / "ironhail-fxout" / "sc-goreshard-b10.25.html", HERE / "chain_tip_ihfxout.html"),
        (HERE.parent / "links" / "sc-goreshard-b10.25.html").resolve()]
bad = 0
for i, t in enumerate(tips):
    ctl = i == len(tips) - 1
    print(("=== CONTROL (must report LOST): " if ctl else "=== ") + t.name, flush=True)
    p = subprocess.run([PY, str(TOOLS / "chain_audit.py"), "--relic", str(HERE / "gs-final-fx.html"), "--tip", str(t),
                        "--builder", str(HERE / "gs_table.py")], capture_output=True, text=True, cwd=str(TOOLS), encoding="utf-8", errors="replace", env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"))
    print(p.stdout.strip()); print("exit", p.returncode, flush=True)
    if (p.returncode == 0) == ctl: bad += 1
print("CHAIN AUDIT:", "PASS (3 tips survive, the control fails)" if not bad else f"FAIL ({bad})")
