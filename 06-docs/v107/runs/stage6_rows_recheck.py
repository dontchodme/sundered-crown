"""Re-check on the resume (2026-09-29): the builder's S6 list, as the builder holds it, is the two labs'
rows byte for byte (voice then picture), the rows files are the hashes the reports name, and the picture
rows alone / voice rows alone / S6 reproduce the labs' stamps and the fx link on the b9.5 link."""
import hashlib, json, pathlib, runpy, sys
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper")
B = pathlib.Path("C:/dev/sundered-crown/tools/lightkeeper_build.py")
h = lambda b: hashlib.sha256(b).hexdigest()[:16]
print("builder", h(B.read_bytes()))
sys.argv = ["x"]; g = runpy.run_path(str(B), run_name="not_main")
S6 = g["S6"]
rows = []
for k, want in (("voice", "814d0a16d8911102"), ("picture", "f9b7579caa065664")):
    p = S / f"stage6-{k}/rows_final.json"; raw = p.read_bytes()
    print(f"{k} rows_final.json {h(raw)} (want {want})", "ok" if h(raw) == want else "FAIL"); assert h(raw) == want
    r = json.loads(raw.decode("utf-8")); r = r["rows"] if isinstance(r, dict) else r
    rows.append((k, r))
def new_of(x):
    return {"replace": x["code"], "after": x["anchor"] + x["code"], "before": x["code"] + x["anchor"]}[x["mode"]]
flat = [x for _, r in rows for x in r]
assert len(flat) == len(S6), (len(flat), len(S6))
for x, (label, old, new) in zip(flat, S6):
    assert label == x["label"] and old == x["anchor"] and new == new_of(x), x["label"]
print(f"S6 == the rows, byte for byte, in order: {len(S6)} edits (voice {len(rows[0][1])}, picture {len(rows[1][1])})")
base = (S / "links/sc-lightkeeper-bulwark-b9.5.html").read_text(encoding="utf-8")
def apply(t, rs):
    for x in rs:
        assert t.count(x["anchor"]) == 1, x["label"]; t = t.replace(x["anchor"], new_of(x), 1)
    return t
for name, rs, want in (("picture rows alone", rows[1][1], "728d64f8397290a1"), ("voice rows alone", rows[0][1], "a8629a7fe94d50b9"),
                       ("voice then picture", rows[0][1] + rows[1][1], "e3f16bf01f0e2995"), ("picture then voice", rows[1][1] + rows[0][1], "e3f16bf01f0e2995")):
    got = h(apply(base, rs).encode("utf-8")); print(f"{name:<20} {got} (want {want})", "ok" if got == want else "FAIL"); assert got == want
fx = (S / "links/sc-lightkeeper-bulwark-b9.5-fx.html").read_bytes()
print("the fx link", h(fx), "CR", fx.count(b"\r"))
