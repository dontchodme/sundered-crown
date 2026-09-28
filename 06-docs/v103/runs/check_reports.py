"""Session 6: the labs' report files (on disk since 16:52) against the row files and the built link.
Each report's rows equal its rows_file field for field; the picture rows alone reproduce the stamp;
voice + picture (either order) reproduce the fx link the builder wrote; the builder's S6 is those rows."""
import json, pathlib, hashlib, importlib.util
S = pathlib.Path(__file__).resolve().parent.parent
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
def rows(p):
    o = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    return o["rows"] if isinstance(o, dict) else o
out = []
for lab, n in (("voice", 3), ("picture", 11)):
    rep = json.loads((S / f"stage6-{lab}-report.json").read_text(encoding="utf-8"))
    rf = pathlib.Path(rep["rows_file"])
    fr, rr = rows(rf), rep["rows"]
    assert len(fr) == len(rr) == n, (lab, len(fr), len(rr))
    for a, b in zip(fr, rr):
        for k in ("label", "anchor", "mode", "code"):
            assert a[k] == b[k], (lab, a["label"], k)
    whys = sum(1 for a, b in zip(fr, rr) if a.get("why") == b.get("why"))
    out.append(f"{lab}: report {n} rows == {rf.name} ({sha(rf.read_bytes())}) on label/anchor/mode/code; 'why' equal on {whys}/{n}")
rep_p = json.loads((S / "stage6-picture-report.json").read_text(encoding="utf-8"))
base = (S / "links/sc-coldiron-temper-b93.html").read_text(encoding="utf-8")
assert sha(base.encode()) == "324b42d5b36fac98"
new_of = lambda r: {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]
def apply(t, rs):
    for r in rs:
        assert t.count(r["anchor"]) == 1, r["label"]
        t = t.replace(r["anchor"], new_of(r), 1)
    return t
V = json.loads((S / "stage6-voice-report.json").read_text(encoding="utf-8"))["rows"]
P = rep_p["rows"]
pic = sha(apply(base, P).encode())
out.append(f"picture rows alone on b93: {pic} (the report's stamp {rep_p['stamp']}) {'OK' if pic == rep_p['stamp'] else 'DIFFERENT'}")
vp, pv = sha(apply(apply(base, V), P).encode()), sha(apply(apply(base, P), V).encode())
fx = sha((S / "links/sc-coldiron-temper-fx.html").read_bytes())
out.append(f"voice then picture {vp}, picture then voice {pv}; the built fx link {fx}: {'IDENTICAL' if vp == pv == fx else 'DIFFERENT'}")
spec = importlib.util.spec_from_file_location("cb", "C:/dev/sundered-crown/tools/coldiron_build.py")
cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb)
want = [(r["label"], r["anchor"], new_of(r)) for r in V + P]
same = [tuple(e) for e in cb.S6] == want
out.append(f"coldiron_build.py S6: {len(cb.S6)} edits, == the report rows as (label, anchor, new) in order: {same}")
assert pic == rep_p["stamp"] and vp == pv == fx and same
print("\n".join(out))
