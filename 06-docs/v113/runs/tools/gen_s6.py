"""Write Thornwake's stage 6 (the S6 table) into tools/thornwake_build.py from the labs'
byte-exact row files. The pattern's (build/iw6/gen_s6.py, by way of Spellbreaker's):
  - the row files are the labs' own (their sha256s), each row {label, anchor, mode, code};
  - the picture rows alone reproduce the picture lab's stamp, the voice rows alone the voice lab's page,
    and both sets give the same bytes in either order (and reversed);
  - no row's anchor sits inside another row's anchor or code, no two anchors' spans overlap on the base,
    and rows that share an anchor LINE are merged into one edit (none here: said);
  - the S6 list is written with triple-quoted strings (no backslash, no ''' in any string);
  - it refuses a builder that already carries S6.
The --stage 6 wiring and its scans are hand edits after this."""
import hashlib, json, pathlib, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake")
VF, PF = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
print("voice rows  ", VF.name, sha(VF.read_bytes()), "(lab: a539532139eb01b7)")
print("picture rows", PF.name, sha(PF.read_bytes()), "(lab: f80fbfe244abacde)")
assert sha(VF.read_bytes()) == "a539532139eb01b7" and sha(PF.read_bytes()) == "f80fbfe244abacde"
fv = json.loads(VF.read_text(encoding="utf-8"))
fp = json.loads(PF.read_text(encoding="utf-8"))
assert isinstance(fv, list) and isinstance(fp, list) and len(fv) == 4 and len(fp) == 12
for r in fv + fp:
    assert r["mode"] in ("before", "after", "replace"), r["label"]

BASE = S / "links/sc-thornwake-b26.5.html"
g = BASE.read_text(encoding="utf-8")
assert "\r" not in g
print("base        ", BASE.name, sha(g.encode()), "(the final stage-5 link: fd5031063ecb6807)")
assert sha(g.encode()) == "fd5031063ecb6807"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


pic = apply(g, fp)
print("picture rows alone ->", sha(pic.encode()), "(the picture lab's stamp, tw-final.html: 65a84cedda239548)")
assert sha(pic.encode()) == "65a84cedda239548"
assert pic == (S / "stage6-picture/tw-final.html").read_text(encoding="utf-8")
voi = apply(g, fv)
print("voice rows alone   ->", sha(voi.encode()), "(the voice lab's end-to-end page: 8f8d06e90d66fc3f)")
assert sha(voi.encode()) == "8f8d06e90d66fc3f"
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
if shared:
    raise SystemExit("rows share an anchor line: merge them (not needed so far)")
merged = [(r["label"], r["anchor"], new_of(r)) for r in rows]
kinds = {m: sum(1 for r in rows if r["mode"] == m) for m in ("before", "after", "replace")}
print("modes:", kinds)

# THE TABLE, triple-quoted
out = [
    "",
    "# ---------------------------------------------------------------- stage 6 --",
    "# THE PICTURE AND THE VOICE (v84 §4's picture and sound; its §5 brief stage 4,",
    "# \"picture, voice\"), picked on measurements under Rick's \"you pick i overrule\"",
    "# by the picture lab (scratch, `tw_rows.py`) and `thornwake_voice_lab.py` (v113",
    "# §5). PRESENTATION ONLY: engine_ab over all 38 relics, Thornwake included, is",
    "# the proof, and the probe's [9]-[10] read the voices and the picture's hook",
    "# inside the fight. The rows are byte-exact to the labs' own files (voice",
    "# a539532139eb01b7, 4 rows; picture f80fbfe244abacde, 12 rows); the picture rows",
    "# alone reproduce the picture lab's stamp (65a84cedda239548), the voice rows",
    "# alone the voice lab's end-to-end page (8f8d06e90d66fc3f), and the two sets",
    f"# give the same bytes in either order ({sha(vp.encode())}). No two rows share an",
    "# anchor line, so none is merged.",
    "#   THE VOICE: the synth's arm keyed on this relic, the freeze's \"creak and",
    "#   cinch\", REPLACED by four arms -- the cast (NEEDLES), a bramble opening",
    "#   (KNOTS), the snare (Tendril's root, transcribed) and a bite (STEM); the",
    "#   shared rune-crack fallback is not touched. Three lines on the sim path,",
    "#   each one SFX.play after a count stage 2 already wrote: the crackle after",
    "#   `planted++` in plantBramble, the snare after `T.snares++` and the bite after",
    "#   the cooldown's re-arm in tickBramble. The cast is fireUlt's own prologue",
    "#   voice (`w: f.w.id`), unchanged. There is no close voice.",
    "#   THE PICTURE: `tickBrier` in tickPresentation (the blade's green, a picture",
    "#   record a bramble, the snare's shoots on the held ball, the bite flashes and",
    "#   the ENTANGLE tag); the brambles in the world pass under both balls; the",
    "#   clench and the bite flash over both fighters; the blade greening in",
    "#   drawWeapon; the hexagon kept off a snared ball in _drawField; the freeze's",
    "#   art retired (drawUltUnder's roots, drawUltOver's thorns, the life entry",
    "#   2.4 and the banner's seat on the quarry).",
    "# COMPOSITION: eleven anchors are re-emitted and five replaced: the synth's own",
    "# arm (four lines), the freeze's two drawUlt branches, and the narrowest",
    "# tokens of the life map (`thornwake: 2.4, `) and the onTarget map",
    "# (`thornwake:1, `), which leave the other entries on those lines to their",
    "# own builds. The rows ride on four of stage 2's own lines (the fighter's",
    "# fields, plantBramble's count, the snare's count, the cooldown's re-arm) and",
    "# on shared lines other stage 6s use as `after` / `before` anchors",
    "# (tickPresentation's first call, the world pass's drawTree and drawTreeTop,",
    "# drawWeapon's ultDraw, _drawField's guard, drawMotes, tickWinnow).",
    "S6 = [",
]
for label, old, new in merged:
    for s_ in (label, old, new):
        assert "'''" not in s_ and "\\" not in s_, label
        assert not s_.endswith("'") and not s_.startswith("'"), label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

p = pathlib.Path("C:/dev/sundered-crown/tools/thornwake_build.py")
src = p.read_bytes().decode("utf-8")
assert "\r" not in src
if "\nS6 = [" in src:
    raise SystemExit("REFUSING: the builder already carries S6 -- the generator runs once")
before = sha(src.encode())
anchor = "\n\n# ------------------------------------------------------- the insert scan --\n"
assert src.count(anchor) == 1
src = src.replace(anchor, "\n" + block + anchor, 1)
# the table, read back, is the rows
ns = {}
exec(compile(block, "S6", "exec"), ns)
assert [(a, b, c) for a, b, c in ns["S6"]] == merged
print("read back: the S6 table == the rows (label, anchor, new) x", len(merged))
if "--dry" in sys.argv:
    print("dry run: not written")
    sys.exit(0)
p.write_bytes(src.encode("utf-8"))
print(f"S6 written into {p.name}: {len(merged)} edits; builder {before} -> {sha(src.encode())}")
