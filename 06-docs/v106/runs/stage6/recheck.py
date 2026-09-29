"""Resume re-check: the reports' rows equal the files; the builder's S6 applied to the base equals the rows applied
(either order) and the fx link on disk."""
import hashlib, json, pathlib, sys, importlib.util
S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]
def load(p):
    r = json.loads(p.read_text(encoding="utf-8")); return r["rows"] if isinstance(r, dict) else r
for kind in ("voice", "picture"):
    rep = json.loads((S / f"stage6-{kind}-report.json").read_text(encoding="utf-8"))
    f = load(S / f"stage6-{kind}" / "rows_final.json")
    print(kind, "report rows == file rows:", rep["rows"] == f, len(f))
spec = importlib.util.spec_from_file_location("wb", "C:/dev/sundered-crown/tools/widowmaker_build.py")
wb = importlib.util.module_from_spec(spec); spec.loader.exec_module(wb)
g = (S / "links/sc-widowmaker-b1075.html").read_text(encoding="utf-8")
t = g
for label, old, new in wb.S6:
    assert t.count(old) == 1, label; t = t.replace(old, new, 1)
def new_of(r): return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]
def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1; t = t.replace(r["anchor"], new_of(r), 1)
    return t
fv, fp = load(S / "stage6-voice/rows_final.json"), load(S / "stage6-picture/rows_final.json")
print("picture alone", sha(apply(g, fp)), "voice alone", sha(apply(g, fv)))
print("S6 applied", sha(t), "== rows v+p", t == apply(apply(g, fv), fp), "== p+v", t == apply(apply(g, fp), fv))
fx = (S / "links/sc-widowmaker-b1075-fx.html").read_text(encoding="utf-8")
print("fx link", sha(fx), "== S6 applied", fx == t, "S6 edits", len(wb.S6))
