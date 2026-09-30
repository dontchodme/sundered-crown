"""Write Spellbreaker's stage 6 (the S6 table) into tools/spellbreaker_build.py from the labs'
byte-exact row files. The pattern's (build/iw6/gen_s6.py, by way of Aureole's):
  - the row files are the labs' own (their sha256s), each row {label, anchor, mode, code};
  - the picture rows alone reproduce the picture lab's stamp, the voice rows alone the voice lab's page,
    and both sets give the same bytes in either order;
  - no row's anchor sits inside another row's anchor or code, no two anchors' spans overlap on the base,
    and rows that share an anchor LINE are merged into one edit (none here: said);
  - the S6 list is written with triple-quoted strings (no backslash, no ''' in any string);
  - it refuses a builder that already carries S6.
The --stage 6 wiring and its scans are hand edits after this (v111 §5e says so)."""
import hashlib, json, pathlib, sys

S = pathlib.Path("<scratch>")
VF, PF = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
print("voice rows  ", VF.name, sha(VF.read_bytes()), "(lab: 090b35214e0efe05)")
print("picture rows", PF.name, sha(PF.read_bytes()), "(lab: 6a3c73a527df3e45)")
assert sha(VF.read_bytes()) == "090b35214e0efe05" and sha(PF.read_bytes()) == "6a3c73a527df3e45"
fv = json.loads(VF.read_text(encoding="utf-8"))
fp = json.loads(PF.read_text(encoding="utf-8"))
assert isinstance(fv, list) and isinstance(fp, list) and len(fv) == 3 and len(fp) == 12
for r in fv + fp:
    assert r["mode"] in ("before", "after", "replace"), r["label"]

BASE = S / "links/sc-spellbreaker-b7.5.html"
g = BASE.read_text(encoding="utf-8")
assert "\r" not in g
print("base        ", BASE.name, sha(g.encode()), "(the final stage-5 link: da7936dccd8f5f15)")
assert sha(g.encode()) == "da7936dccd8f5f15"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


pic = apply(g, fp)
print("picture rows alone ->", sha(pic.encode()), "(the picture lab's stamp: 176458b0df4a79cd)")
assert sha(pic.encode()) == "176458b0df4a79cd"
voi = apply(g, fv)
print("voice rows alone   ->", sha(voi.encode()), "(the voice lab's page: 149b777b7f1ccb90)")
assert sha(voi.encode()) == "149b777b7f1ccb90"
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
# NO TWO ANCHORS' SPANS OVERLAP ON THE BASE, and rows sharing an anchor LINE would be merged
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
merged = []
if shared:
    raise SystemExit("rows share an anchor line: merge them (not needed so far)")
for r in rows:
    merged.append((r["label"], r["anchor"], new_of(r)))
kinds = {m: sum(1 for r in rows if r["mode"] == m) for m in ("before", "after", "replace")}
print("modes:", kinds)

# THE TABLE, triple-quoted
out = [
    "",
    "# ---------------------------------------------------------------- stage 6 --",
    "# THE PICTURE AND THE VOICE (v79 §4's picture and sound; its §5 brief stage 4,",
    "# \"picture, voice, carry; bolt's field spec out\"), picked on measurements under",
    "# Rick's \"you pick i overrule\" by the picture lab (scratch, `sb_rows.py`) and",
    "# `spellbreaker_voice_lab.py` (v111 §5). PRESENTATION ONLY: engine_ab over all",
    "# 38 relics, Spellbreaker included, is the proof, and the probe's [7]-[8] read the",
    "# voices and the picture's hook inside the fight. The rows are byte-exact to the",
    "# labs' own files (voice 090b35214e0efe05, 3 rows; picture 6a3c73a527df3e45, 12",
    "# rows); the picture rows alone reproduce the picture lab's stamp",
    "# (176458b0df4a79cd), the voice rows alone the voice lab's page",
    f"# (149b777b7f1ccb90), and the two sets give the same bytes in either order",
    f"# ({sha(vp.encode())}). No two rows share an anchor line, so none is merged.",
    "#   THE VOICE: three arms -- the cast's crack into a hum, a lengthened stun,",
    "#   the hum cutting out -- ADDED before the shared rune-crack fallback, which is",
    "#   re-emitted unchanged, last; two lines on the sim path, each beside a line",
    "#   this build's stage 2 already wrote (the stun voice after the hex proc's",
    "#   breakSpin, the close voice before the window's own close line).",
    "#   THE PICTURE: `tickUnmaking` in tickPresentation (the script's clock, the",
    "#   rune motes, the HEX +2 tag, the grey); the motes in the world pass under",
    "#   both balls; the grey and the script in drawWeapon; the bolt's art retired",
    "#   (drawUltOver's branch, the banner's seat on the quarry, the life entry).",
    "# COMPOSITION: eleven anchors are re-emitted and four replaced: three",
    "# consumed, all Spellbreaker's own (the bolt's drawUltOver branch, the onTarget",
    "# map's narrowest token `spellbreaker:1, ` and the life map's",
    "# ` spellbreaker: 1.4,`, which leave Thornwake's, Emberedge's and the other",
    "# entries on their lines to their own builds), and drawWeapon's dim line,",
    "# replaced by its own text with the grey's alpha in it. The rows ride on four",
    "# of stage 2's own lines (the fields, the hex proc's breakSpin, the window's",
    "# close line and tickUnmake's end) and",
    "# on shared lines every stage 6 of the batch uses as `after` / `before` anchors",
    "# (tickPresentation's first call, the world pass's drawTree, the fx banner",
    "# comment, shellHash, drawWeapon, the rune-crack fallback).",
    "S6 = [",
]
for label, old, new in merged:
    for s_ in (label, old, new):
        assert "'''" not in s_ and "\\" not in s_, label
        assert not s_.endswith("'") and not s_.startswith("'"), label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

p = pathlib.Path("C:/dev/sundered-crown/tools/spellbreaker_build.py")
src = p.read_bytes().decode("utf-8")
assert "\r" not in src
if "\nS6 = [" in src:
    raise SystemExit("REFUSING: the builder already carries S6 -- the generator runs once")
before = sha(src.encode())
anchor = "\n\nSTAGE_OUT = {"
assert src.count(anchor) == 1
src = src.replace(anchor, "\n" + block + "\nSTAGE_OUT = {", 1)
if "--dry" in sys.argv:
    print("dry run: not written")
    sys.exit(0)
p.write_bytes(src.encode("utf-8"))
print(f"S6 written into {p.name}: {len(merged)} edits; builder {before} -> {sha(src.encode())}")
# the table, read back, is the rows
ns = {}
exec(compile(block, "S6", "exec"), ns)
assert [(a, b, c) for a, b, c in ns["S6"]] == merged
print("read back: the S6 table == the rows (label, anchor, new) x", len(merged))
