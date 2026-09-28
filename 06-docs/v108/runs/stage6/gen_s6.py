"""Write Ironhail / Quarrelstorm's stage 6 into tools/ironhail_build.py from the labs' byte-exact row files.

Ironwood's / Bindweed's / Coldiron's gen_s6 pattern: verify the rows the labs returned equal their
files, check the picture rows alone reproduce the picture lab's stamp, assert no row's anchor sits
inside another's, MERGE rows that share an anchor into one edit, write an S6 list into the builder with
triple-quoted strings, and wire a --stage 6 that refuses to run twice and scans S6 (no ultFx, no RNG,
no call into the simulation, writes only presentation fields). Refuses to run on a builder that
already has S6.

THE RETURNED ROWS. The labs' reports reached this session relayed inline in the task text, cut off
mid-row (no report file on disk for Ironhail). What was relayed whole is checked here to the
character: the labels, anchors and modes of the relayed rows (voice row 1, picture rows 1-3) and a
line of each relayed body. The files are then tied to the labs' own records: the voice file equals
the lab's final confirmation run `rows_lab4.json` byte for byte (its STATE.md: sha16 5d2a679a52632527),
and the picture file's sha is the one the picture lab recorded (f97048b0e0bf1d99), whose rows alone
reproduce its stamp (f03b657a1d99d86c) on sc-ironhail-sunder.
"""
import json, pathlib, hashlib, re, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail")
REPO = pathlib.Path("C:/dev/sundered-crown")
STAMP = "f03b657a1d99d86c"          # the picture lab's ih-final.html: picture rows alone on the base
PIC_FILE_SHA = "f97048b0e0bf1d99"   # the picture lab's STATE.md / order.out: rows_final.json
VOICE_FILE_SHA = "5d2a679a52632527"  # the voice lab's STATE.md: rows_final.json = rows_lab4.json
PICVOICE_SHA = "b8ff2014a954be3f"   # the voice lab's sc-ironhail-picvoice.html (either order)
BASE_SHA = "1bedab05b9803465"       # sc-ironhail-sunder.html (stage 3 = THE FINAL)
BUILDER_SHA = "13d0df8b674c873d"    # tools/ironhail_build.py before stage 6

sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
fv_p, fp_p = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
assert sha(fp_p.read_bytes()) == PIC_FILE_SHA, "the picture rows file is not the one the lab recorded"
assert sha(fv_p.read_bytes()) == VOICE_FILE_SHA, "the voice rows file is not the one the lab recorded"
assert fv_p.read_bytes() == (S / "stage6-voice/rows_lab4.json").read_bytes(), \
    "the voice rows file is not the lab's final confirmation run"
fv = json.loads(fv_p.read_text(encoding="utf-8"))
fp = json.loads(fp_p.read_text(encoding="utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
assert len(fv) == 3 and len(fp) == 12, (len(fv), len(fp))

# What the relayed reports carried whole (label, anchor, mode), to the character.
RELAYED = [
    (fv[0], "Sfx: Ironhail's cast, landing and miss arms, before the shared rune-crack fallback",
     "        } else {                                        // rune-crack", "replace"),
    (fp[0], "quarrelstorm picture: fighter fields", "    this.ultHail = null;\n    this.hailTally = null;\n", "after"),
    (fp[1], "quarrelstorm picture: the presentation call", "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n", "after"),
    (fp[2], "quarrelstorm picture: tickQuarrel", "  tickWinnow(dt){\n", "before"),
]
for r, label, anchor, mode in RELAYED:
    assert (r["label"], r["anchor"], r["mode"]) == (label, anchor, mode), label
# ... and a line of each relayed code body, verbatim from the relay.
assert '          this._sweep(t + 0.32, { f0: 400, f1: 150, q: 0.7, gain: g, dur: 0.58, atk: 0.02, type:"lowpass" });\n' in fv[0]["code"]
assert "          const f = 103.83, g = 0.05227, D = 0.213;\n" in fv[0]["code"]
assert "    this.quarrelFx = [];\n" in fp[0]["code"]
assert fp[1]["code"] == "    this.tickQuarrel(dt);               // QUARRELSTORM'S PICTURE (v83 section 4)\n"
assert "      const Z = (this.over || !f.alive) ? null : f.ultHail;\n" in fp[2]["code"]
assert "    if (__world) this.drawQuarrel(m);\n" in fp[3]["code"]
print("the returned rows equal the files: voice 3/3 (== the lab's rows_lab4.json, its final confirmation "
      "run), picture 12/12 (the lab's recorded file); the relayed rows' labels, anchors, modes and a line "
      "of each relayed body match")

base_p = S / "links/sc-ironhail-sunder.html"
g = base_p.read_text(encoding="utf-8")
assert "\r\n" not in g
assert sha(g.encode()) == BASE_SHA
print("base", base_p.name, BASE_SHA)


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


t = g
for r in fp:
    assert t.count(r["anchor"]) == 1, r["label"]
    t = t.replace(r["anchor"], new_of(r), 1)
pic_sha = sha(t.encode())
print("picture-only sha", pic_sha, f"(the picture lab's stamp: {STAMP})")
assert pic_sha == STAMP

rows = fv + fp
# NO ROW'S ANCHOR MAY SIT INSIDE ANOTHER ROW'S ANCHOR (identical anchors are merged below instead).
for i, a in enumerate(rows):
    for j, b in enumerate(rows):
        if i != j and a["anchor"] != b["anchor"]:
            assert a["anchor"] not in b["anchor"], (a["label"], b["label"])
for r in rows:
    assert g.count(r["anchor"]) == 1, r["label"]

# MERGE rows that share an anchor into one edit, in row order.
groups = {}
for r in rows:
    groups.setdefault(r["anchor"], []).append(r)
edits, merged = [], 0
for anc, rs in groups.items():
    if len(rs) == 1:
        r = rs[0]
        edits.append((r["label"], anc, new_of(r)))
        continue
    merged += 1
    pre = "".join(r["code"] for r in rs if r["mode"] == "before")
    post = "".join(r["code"] for r in rs if r["mode"] == "after")
    reps = [r for r in rs if r["mode"] == "replace"]
    assert len(reps) <= 1, [r["label"] for r in rs]
    mid = anc
    if reps:
        assert reps[0]["code"].count(anc) == 1, reps[0]["label"]
        mid = reps[0]["code"]
    edits.append((" + ".join(r["label"] for r in rs), anc, pre + mid.replace(anc, anc + post, 1) if post else pre + mid))
print(f"{len(rows)} rows -> {len(edits)} edits ({merged} merged at a shared anchor)")

# Applied as the builder will apply them (exactly one occurrence at each step), and in the other order.
nv = len(fv)
t1 = g
for label, old, new in edits:
    assert t1.count(old) == 1, label
    t1 = t1.replace(old, new, 1)
t2 = g
for label, old, new in edits[nv:] + edits[:nv]:
    assert t2.count(old) == 1, label
    t2 = t2.replace(old, new, 1)
assert t1 == t2, "voice-then-picture and picture-then-voice differ"
reemit = 0
for label, old, new in edits:
    if old in new:          # the row re-emits its anchor: still exactly once
        assert t1.count(old) == 1, ("anchor not unique after all rows", label)
        reemit += 1
    else:                   # a true replace: the old text is gone, the new once
        assert t1.count(old) == 0 and t1.count(new) == 1, ("replace", label)
full_sha = sha(t1.encode())
print(f"voice+picture sha {full_sha} (both orders identical; {reemit} edits re-emit their anchor, "
      f"{len(edits) - reemit} replace text outright); the voice lab's picture+voice page: {PICVOICE_SHA}")
assert full_sha == PICVOICE_SHA

p = REPO / "tools/ironhail_build.py"
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "\nS6 = [" in s:
    raise SystemExit("the builder already has S6 -- not writing it twice")
assert sha(s.encode()) == BUILDER_SHA, "the builder is not the one this generator was written for"

out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v83 §4, brief stage 4), picked on measurements",
       "# under Rick's \"you pick i overrule\" by `ironhail_voice_lab.py` and the",
       "# picture lab (v108 §7). Presentation only: engine_ab over all 38 relics,",
       "# Ironhail included, is the proof. The rows are byte-exact to the labs' own",
       "# files (voice 3, picture 12; no two share an anchor, so none is merged); the",
       f"# picture rows alone reproduce the picture lab's stamp ({STAMP}) on",
       "# sc-ironhail-sunder. Voice first, then picture; the other order writes the",
       "# same bytes.",
       "#   THE VOICE: the cast (fireUlt's own `ult`/ironhail call, which fell",
       "#   through to rune-crack: the bellows huff), a landing (in tickHail, after",
       "#   its hurt and its sunder, pitched by the foe's count) and a miss (in",
       "#   tickHail, before the miss line, on that line's own test). The close has",
       "#   none (v83 §4). Plain SFX.play; nothing is read back.",
       "#   THE PICTURE: `tickQuarrel` in tickPresentation reads `ultHail && !over`,",
       "#   `hailTally` rising and the bolts in `m.hail`, and writes only its own",
       "#   `quarrel*` fields, a tag's count, `tags` (statusTag) and `taught`. The",
       "#   limbs glow forge-orange for the window and cool 0.5s after it; each bolt",
       "#   is a rune on its spot with a ring closing on it and a streak falling",
       "#   from the top of the live hall; a landing splashes, dusts, throws six",
       "#   sparks and four iron-spark motes and ticks the sunder tag; a miss",
       "#   splashes in dust. The nova's art (the release flash and floor dust on",
       "#   the ultFx slot, the charge rune's eight heads, the banner's fan) is",
       "#   retired. No beat, no stop, no fx.js edit: the design's field is drawn",
       "#   (reading 20), and the nova's field spec leaves BOTH copies by the",
       "#   orchestrator's sync_fx_remove, not here (fx.js is shared).",
       "#   NAMES: the labs'. `drawQuarrel` is a prefix of `drawQuarrelGlow`, so",
       "#   every stage-6 name check below is on identifier boundaries.",
       "S6 = ["]
for label, old, new in edits:
    for x in (label, old, new):
        assert "'''" not in x and "\\" not in x and not x.endswith("'") and not x.startswith("'"), label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

tail = '''
# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`drawQuarrel` is a prefix of `drawQuarrelGlow`; the base's own renderer
# reads `u.w === "ironhail"` and `b.w === "ironhail"`, so the cast arm is found
# by its whole `} else if (w === "ironhail"){` line, never by the comparison).
S6_NAMES = ("tickQuarrel", "drawQuarrel", "drawQuarrelGlow", "_quarrelLimbs", "_quarrelSplash",
            "quarrelFade", "quarrelFx", "quarrelSeen", "quarrelAir", '"ironhail-land"',
            '"ironhail-miss"')
S6_CAST_ARM = '} else if (w === "ironhail"){'
# What stage 6's ADDED code may write: its own quarrel* fields (and their
# arrays' length), the canvas, a tag's count, a puff record's own clock,
# `taught`, and an oscillator's pitch. Arrays it may push to or splice: its
# own quarrel* arrays and the banner's local width list.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("quarrel") or obj.startswith("quarrel")
               or obj == "c" or (obj, prop) in {("g", "val"), ("q", "t"), ("taught", "sunder"),
                                                ("frequency", "value")})
S6_ARRAY_OK = (lambda obj: obj.startswith("quarrel") or obj == "ws")


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]

'''

reps = [
 ('''    stage 6   picture, voice, the nova's field out (brief stage 4; not written yet)
''',
  '''    stage 6   picture, voice (brief stage 4) -> sc-ironhail-sunder-fx.html
              (on the final; the nova's field spec leaves BOTH copies of fx.js
              by the orchestrator's sync_fx_remove, not here: reading 20)
'''),
 ('''THE CLOCK. The window, the drop cadence and every bolt's fall run on the
''',
  '''STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
and sound are Code's picks under "you pick i overrule"; v108 §7):
 15. THE CAST VOICE is the cast's own `SFX.play("ult", {w: "ironhail"})` in
     fireUlt's generic head, which fell through to rune-crack: an arm is ADDED
     before that shared fallback (the bellows huff) and the fallback line is
     re-emitted unchanged for the relics that still fall through.
 16. THE LANDING VOICE plays once per landed bolt, in tickHail after its hurt
     and its sunder, pitched by the count the foe then carries (the number its
     tag shows, 1-6); a killing landing thuds too, under the death voice.
 17. THE MISS VOICE plays once per missed bolt, on its landing frame, on the
     miss line's own test read first (the anchor guards it: if that line
     changes, the row stops applying).
 18. THE CLOSE HAS NO VOICE (v83 §4: "close -- nothing").
 19. THE PICTURE is drawn from the match's bolts (`m.hail`, read) and the
     fighter's own `quarrel*` fields (never `m.ultFx`, open item 25); a bolt
     that resolves is found by `hailTally` rising, so tickHail makes no call
     for the picture. The limbs read `ultHail && !over` and cool at the
     verdict; a bolt the kill leaves in the air fades on `quarrelEnd`. ONE
     SUNDER TAG ON THE FOE AT A TIME (Tendril's and Temper's rule): a landing
     with a tag already up sets its count in place; a killing landing tags
     nothing (the shatter owns that frame).
 20. "FIELD: IRON-SPARK MOTES ON LANDINGS, BOTH COPIES" IS DRAWN, not an fx.js
     field: a SPECS field fires once, at the cast edge, on the one ultFx slot,
     which Ironhail holds for a median 0.62s of its 8s window; 15 of 417
     landings came while it was still Ironhail's, a median 254 units from the
     field's spawn point. So four motes rise off every landing, drawn. The
     NOVA's field spec (`SPECS.ironhail`, a beam of 1300) is the brief's
     "nova's field spec out": it leaves both copies by the orchestrator's
     sync_fx_remove (fx.js is shared), and this builder never edits either.
 21. THE NOVA'S ART IS RETIRED with the nova: drawUltUnder's floor dust and
     drawUltOver's release flash (keyed on the ultFx slot's "ironhail"), the
     charge rune's eight heads (now three bolts onto a crossed rune) and the
     banner's fan (the letters now fall).

THE CLOCK. The window, the drop cadence and every bolt's fall run on the
'''),
 ('''STAGE_OUT = {"1": "sc-ironhail-stub", "2": "sc-ironhail-hail", "3": "sc-ironhail-sunder",
             "5 --alt50": "sc-ironhail-b14"}
''',
  block + tail + '''
STAGE_OUT = {"1": "sc-ironhail-stub", "2": "sc-ironhail-hail", "3": "sc-ironhail-sunder",
             "5 --alt50": "sc-ironhail-b14", "6": "sc-ironhail-sunder-fx"}
'''),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''            edits, want = S3, ult_block(ULT["charge"], ULT["sunder"])
        else:
''',
  '''            edits, want = S3, ult_block(ULT["charge"], ULT["sunder"])
        elif A.stage == "6":
            # STAGE 6 GOES ON THE FINAL, ONCE: Ironhail's ult block is stage 3's
            # to the character, its blade the shipped one (not the 50% link);
            # none of stage 6's names is in the source yet (on identifier
            # boundaries) and the Sfx has no Ironhail arm.
            want = ult_block(ULT["charge"], ULT["sunder"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 6 goes on the final (stage 3's link, blade "
                                 f"{SHIPPED_DMG}): Ironhail's ult block or blade is not the final's")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_CAST_ARM in code:
                raise SystemExit("the Sfx already has an Ironhail arm -- stage 6 goes on once")
            edits = S6
        else:
'''),
 ('''    for label, _old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:''',
  '''    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or shatters, writes only
    # what S6_WRITE_OK names and mutates only its own arrays. It READS the
    # window, the tally, the bolts and the foe's count; the probe's [10]-[11]
    # and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickHail|spawnShot)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(push|splice|pop|shift|unshift|reverse|sort)\\(", ins):
            if not S6_ARRAY_OK(mw.group(1)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\[[^\\]]*\\]\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_ARRAY_OK(mw.group(1).split(".")[-1]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
    if A.stage == "6":
        if inlined_fx(s) != inlined_fx(s0):
            raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                             "(the nova's field spec is the orchestrator's sync_fx_remove)")
        if re.search(r'\\bu\\.w === "ironhail"', out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's art on the ultFx slot is still drawn")
        for need, n in (('SFX.play("ult", { w: "ironhail-land", n: foe.stacks("sunder") });', 1),
                        ('SFX.play("ult", { w: "ironhail-miss" });', 1),
                        (S6_CAST_ARM, 1), ("this.tickQuarrel(dt);", 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields); the inlined fx.js untouched; the nova's art out; "
              "three voices wired once each")
    for label, _old, new in S1 + S2 + S3 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("stage 6 written into", p.name, ":", len(edits), "edits;", "sha", sha(s.encode()))
(S / "s6/expected_fx_sha.txt").write_text(full_sha + "\n")
