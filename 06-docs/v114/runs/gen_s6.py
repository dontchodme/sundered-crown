"""Write Goreshard's stage 6 (the S6 table) into tools/goreshard_build.py from the labs'
byte-exact row files. The pattern's (build/iw6/gen_s6.py, by way of Spellbreaker's s6/gen_s6.py):
  - the row files are the labs' own (their sha256s), each row {label, anchor, mode, code};
  - the picture rows alone reproduce the picture lab's stamp, the voice rows alone the voice lab's page,
    and both sets give the same bytes in either order (and reversed);
  - no row's anchor sits inside another row's anchor or code, no two anchors' spans overlap on the base,
    and rows that share an anchor LINE are merged into one edit;
  - the S6 list is written with triple-quoted strings (no backslash, no ''' in any string);
  - it refuses a builder that already carries S6.
The --stage 6 wiring and its scans are hand edits after this."""
import hashlib, json, pathlib, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/goreshard")
VF, PF = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
V_SHA, P_SHA = "780b26fd136cfa59", "1b95d5d4e1c71ed6"
print("voice rows  ", VF.name, sha(VF.read_bytes()), f"(lab: {V_SHA})")
print("picture rows", PF.name, sha(PF.read_bytes()), f"(lab: {P_SHA})")
assert sha(VF.read_bytes()) == V_SHA and sha(PF.read_bytes()) == P_SHA
fv = json.loads(VF.read_text(encoding="utf-8"))
fp = json.loads(PF.read_text(encoding="utf-8"))
assert isinstance(fv, list) and isinstance(fp, list) and len(fv) == 3 and len(fp) == 10
for r in fv + fp:
    assert r["mode"] in ("before", "after", "replace"), r["label"]
    for k in ("label", "anchor", "code"):
        s_ = r[k]
        assert "'''" not in s_ and "\\" not in s_, (r["label"], k)
        assert "\r" not in s_, (r["label"], k)

BASE = S / "links/sc-goreshard-b10.25.html"
g = BASE.read_bytes().decode("utf-8")
assert "\r" not in g
print("base        ", BASE.name, sha(g.encode()), "(the final stage-5 link: 8eb3c1634184c1bd)")
assert sha(g.encode()) == "8eb3c1634184c1bd"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


pic = apply(g, fp)
print("picture rows alone ->", sha(pic.encode()), "(the picture lab's stamp: 1f0248fee32086ba)")
assert sha(pic.encode()) == "1f0248fee32086ba"
lab = (S / "stage6-picture/gs-final.html").read_bytes()
assert lab == pic.encode("utf-8"), "gs-final.html is not the picture rows on the base"
print("                      == the lab's own gs-final.html, byte for byte")
voi = apply(g, fv)
print("voice rows alone   ->", sha(voi.encode()), "(the voice lab's page: 8323dc9c2a8302b5)")
assert sha(voi.encode()) == "8323dc9c2a8302b5"
vp, pv = apply(g, fv + fp), apply(g, fp + fv)
print("voice then picture ->", sha(vp.encode()), "; picture then voice ->", sha(pv.encode()))
assert vp == pv
rev = apply(g, list(reversed(fv + fp)))
assert rev == vp
print("reversed order     ->", sha(rev.encode()), "(the same)")

rows = fv + fp
# NO NESTED ANCHOR: a row's anchor inside another row's anchor or inside another row's code
for i, a in enumerate(rows):
    for j, b in enumerate(rows):
        if i != j:
            assert a["anchor"] not in b["anchor"], (a["label"], "inside the anchor of", b["label"])
            assert a["anchor"] not in b["code"], (a["label"], "inside the code of", b["label"])
# NO TWO ANCHORS' SPANS OVERLAP ON THE BASE, and rows sharing an anchor LINE are merged
spans = []
for r in rows:
    i = g.find(r["anchor"])
    spans.append((i, i + len(r["anchor"]), r["label"]))
spans.sort()
for (a0, a1, la), (b0, b1, lb) in zip(spans, spans[1:]):
    assert a1 <= b0, ("overlap", la, lb)
line_of = lambda i: g.count("\n", 0, i)
lines = {}
for r in rows:
    i = g.find(r["anchor"])
    a = r["anchor"]
    lo = line_of(i + (1 if a.startswith("\n") else 0))
    hi = line_of(i + len(a) - (1 if a.endswith("\n") else 0))
    for ln in range(lo, hi + 1):
        lines.setdefault(ln, []).append(r["label"])
shared = {k: v for k, v in lines.items() if len(v) > 1}
print("rows sharing an anchor line:", shared or "none -- so none is merged")
if shared:
    raise SystemExit("rows share an anchor line: merge them (not needed so far)")
merged = [(r["label"], r["anchor"], new_of(r)) for r in rows]
kinds = {m: sum(1 for r in rows if r["mode"] == m) for m in ("before", "after", "replace")}
print("modes:", kinds)

# THE TABLE, triple-quoted
out = [
    "",
    "# ---------------------------------------------------------------- stage 6 --",
    "# THE PICTURE AND THE VOICE (v81 §4's picture and sound; its §5 brief stage 3,",
    "# \"picture, voice, carry; beam's field spec out\"), picked on measurements under",
    "# Rick's \"you pick i overrule\" by the picture lab (scratch, `gs_rows.py`) and",
    "# `goreshard_voice_lab.py` (v114 §5). PRESENTATION ONLY: engine_ab over all 38",
    "# relics, Goreshard included, is the proof, and the probe's [11]-[12] read the",
    "# voices and the picture's hook inside the fight. The rows are byte-exact to the",
    f"# labs' own files (voice {V_SHA}, 3 rows; picture {P_SHA}, 10",
    "# rows); the picture rows alone reproduce the picture lab's stamp",
    "# (1f0248fee32086ba), the voice rows alone the voice lab's page",
    "# (8323dc9c2a8302b5), and the two sets give the same bytes in either order",
    f"# ({sha(vp.encode())}). No two rows share an anchor line, so none is merged.",
    "#   THE VOICE: the scaled blow's branch before the plain hit arm (taken only",
    "#   with `price`), the cast's arm before the shared rune-crack fallback (which",
    "#   is re-emitted unchanged, last), and one line on the sim path, before",
    "#   resolveHit's hit-voice line: a blow priced on n > 0 passes `price: priceN`.",
    "#   THE PICTURE: `tickGore` in tickPresentation (the red's run and drain, the",
    "#   glow's ease toward 0.2 + 0.15 x the foe's Hemorrhage, the motes); the",
    "#   blade in drawWeapon; the motes in the world pass under both balls; the",
    "#   priced blow's float x(1 + 0.1 x priceN); the beam's art retired",
    "#   (drawUltUnder's pool, drawUltOver's seam, the charge rune redrawn).",
    "# COMPOSITION: nine anchors are re-emitted and four replaced: three",
    "# Goreshard's own (the pool, the seam, ULTSIG.oathwound), and resolveHit's",
    "# shared float-size line, replaced by its own text with the price's factor on",
    "# it (x1 exactly wherever `priceN` is 0: every other relic's blow).",
    "# The rows ride on two of stage 2's own lines (the fields, tickPrice's end)",
    "# and on shared lines every stage 6 of the batch uses as `after` / `before`",
    "# anchors (tickPresentation's first call, drawWeapon's tree hook, the world",
    "# pass's drawTree, drawMotes, the rune-crack fallback, the plain hit arm).",
    "S6 = [",
]
for label, old, new in merged:
    for s_ in (label, old, new):
        assert "'''" not in s_ and "\\" not in s_, label
        assert not s_.endswith("'") and not s_.startswith("'"), label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

p = pathlib.Path("C:/dev/sundered-crown/tools/goreshard_build.py")
src = p.read_bytes().decode("utf-8")
assert "\r" not in src
if "\nS6 = [" in src:
    raise SystemExit("REFUSING: the builder already carries S6 -- the generator runs once")
before = sha(src.encode())
anchor = "\n\nSTAGE_OUT = {"
assert src.count(anchor) == 1
src = src.replace(anchor, "\n" + block + "\nSTAGE_OUT = {", 1)
# the table, read back, is the rows
ns = {}
exec(compile(block, "S6", "exec"), ns)
assert [(a, b, c) for a, b, c in ns["S6"]] == merged
print("read back: the S6 table == the rows (label, anchor, new) x", len(merged))
(S / "s6/expected_fx_sha.txt").write_text(sha(vp.encode()) + "\n")
if "--dry" in sys.argv:
    print("dry run: not written")
    sys.exit(0)
p.write_bytes(src.encode("utf-8"))
print(f"S6 written into {p.name}: {len(merged)} edits; builder {before} -> {sha(src.encode())}")
