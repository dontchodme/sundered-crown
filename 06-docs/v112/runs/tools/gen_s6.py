"""Write Heartwood's stage 6 (the S6 table) into tools/heartwood_build.py from the two labs' byte-exact row files.

ironwood's gen_s6.py pattern: the rows are read from the labs' own files (their shas checked against the labs'
reports), applied to the final link (sc-heartwood-b11, aff84a04b303a402) to prove
  - every anchor occurs exactly once on the base, no anchor sits inside another row's anchor or code,
  - the PICTURE rows alone reproduce the picture lab's stamp (4ce2e98655411557),
  - the VOICE rows alone reproduce the voice lab's end-to-end page (6a19b58add3cf38e),
  - the two sets give the same bytes in either order,
and rows that share an anchor LINE would be merged into one edit (none do: asserted).
The S6 list is written with triple-quoted strings between the S5 table and the insert scan. SCRATCH tool.
"""
import hashlib, json, pathlib, sys

S = pathlib.Path(__file__).resolve().parent.parent          # batch/heartwood
BASE = S / "links" / "sc-heartwood-b11.html"
FV, FP = S / "stage6-voice" / "rows_final.json", S / "stage6-picture" / "rows_final.json"
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_build.py")
sha = lambda b: hashlib.sha256(b).hexdigest()[:16]

assert sha(FV.read_bytes()) == "4c38682da549a943", "the voice rows moved since the voice lab's report"
assert sha(FP.read_bytes()) == "184f5cb47c0bb5e7", "the picture rows moved since the picture lab's report"
base_b = BASE.read_bytes()
assert sha(base_b) == "aff84a04b303a402", "not the final link"
base = base_b.decode("utf-8")
fv = json.loads(FV.read_text(encoding="utf-8"))
fp = json.loads(FP.read_text(encoding="utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
assert len(fv) == 2 and len(fp) == 9


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


rows = fv + fp
for r in rows:
    assert base.count(r["anchor"]) == 1, r["label"]
    if r["mode"] == "replace" and r["anchor"] in r["code"]:
        assert r["code"].count(r["anchor"]) == 1, r["label"]
for i, a in enumerate(rows):
    for j, b in enumerate(rows):
        if i != j:
            assert a["anchor"] not in b["anchor"], (a["label"], b["label"])
            assert a["anchor"] not in b["code"], (a["label"], "in the code of", b["label"])


def line_span(r):
    i = base.find(r["anchor"])
    s0 = base.rfind("\n", 0, i) + 1
    e = base.find("\n", i + len(r["anchor"]) - 1)
    return base.count("\n", 0, s0), base.count("\n", 0, e)


spans = [(line_span(r), r["label"]) for r in rows]
for i, (a, la) in enumerate(spans):
    for j, (b, lb) in enumerate(spans):
        if i < j and not (a[1] < b[0] or b[1] < a[0]):
            sys.exit(f"rows share an anchor line and would need merging: {la} / {lb}")
print("no two rows share an anchor line: none merged")

pic = apply(base, fp)
voc = apply(base, fv)
both1 = apply(apply(base, fv), fp)
both2 = apply(apply(base, fp), fv)
print("picture rows alone", sha(pic.encode()), "(the picture lab's stamp 4ce2e98655411557)")
print("voice rows alone  ", sha(voc.encode()), "(the voice lab's end-to-end page 6a19b58add3cf38e)")
print("both, voice first ", sha(both1.encode()), " picture first", sha(both2.encode()))
assert sha(pic.encode()) == "4ce2e98655411557"
assert sha(voc.encode()) == "6a19b58add3cf38e"
assert both1 == both2

edits = [(r["label"], r["anchor"], new_of(r)) for r in rows]
for label, old, new in edits:
    for s in (label, old, new):
        assert "'''" not in s and "\\" not in s and not s.endswith("'"), label
out = [
    "# ---------------------------------------------------------------- stage 6 --",
    "# THE PICTURE AND THE VOICE (v85 §4's picture and sound; its §5 brief stage 4,",
    "# \"picture, voice, carry\"), picked on measurements under Rick's \"you pick i",
    "# overrule\" by the picture lab (scratch, `stage6-picture/hw_rows.py`, 9 rows)",
    "# and `heartwood_voice_lab.py` (2 rows), v112 §7. PRESENTATION ONLY: engine_ab",
    "# over all 38 relics, Heartwood included, is the proof, and the probe's [9]-[10]",
    "# read the voices and the picture's hook inside the fight. The rows are",
    "# byte-exact to the labs' own files (voice 4c38682da549a943, picture",
    "# 184f5cb47c0bb5e7); the picture rows alone reproduce the picture lab's stamp",
    f"# (4ce2e98655411557), the voice rows alone the voice lab's end-to-end page",
    f"# (6a19b58add3cf38e), and the two sets give the same bytes in either order",
    f"# ({sha(both1.encode())}). No two rows share an anchor line, so none is merged.",
    "#   THE VOICE: two arms added BEFORE the shared rune-crack fallback, which is",
    "#   re-emitted unchanged (Heartwood had no arm and fell through to it): the",
    "#   cast (RISING, \"a green creak, 0.4s\") and the root (`heartwood-root`,",
    "#   Tendril's root voice transcribed with its gain 0.5179 -> 0.2313). One line",
    "#   on the sim path: SFX.play after `T.rooted++;` in rootBlow (every rooted",
    "#   blow; a killing blow returns above it). The cast is fireUlt's own prologue",
    "#   voice (`w: f.w.id`), unchanged. There is no close voice.",
    "#   THE PICTURE: `tickGrove` in tickPresentation (the blade's green, the",
    "#   sprout and the leaf motes, the wither and its leaves, the held ball's four",
    "#   `twine*` markers for Tendril's root picture, the ENTANGLE tag's count);",
    "#   the motes and the falling leaves in the world pass under both balls; the",
    "#   blade greening in drawWeapon; the freeze's art retired (drawUltUnder's",
    "#   plate, drawUltOver's cage, the life entry 2.2).",
    "S6 = [",
]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", "", ""]
block = "\n".join(out)

if "--write" in sys.argv:
    s = BUILDER.read_text(encoding="utf-8")
    assert "\nS6 = [\n" not in s, "S6 is already in the builder"
    anchor = "# ------------------------------------------------------- the insert scan --\n"
    assert s.count(anchor) == 1
    s = s.replace(anchor, block + anchor, 1)
    BUILDER.write_text(s, encoding="utf-8", newline="\n")
    print("S6 written:", len(edits), "edits;  builder", sha(BUILDER.read_bytes()))
else:
    print("(dry: pass --write to write S6 into the builder)", len(edits), "edits")
