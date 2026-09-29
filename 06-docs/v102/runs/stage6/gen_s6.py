"""Write Lodestone / Rebuttal's stage 6 into tools/lodestone_build.py from the labs' byte-exact row files.

Ironwood's / Bindweed's / Coldiron's / Ironhail's gen_s6 pattern: verify the rows the labs returned
equal their files, check the picture rows alone reproduce the picture lab's stamp, assert no row's
anchor sits inside another's, MERGE rows that share an anchor into one edit, write an S6 list into the
builder with triple-quoted strings, and wire a --stage 6 that refuses to run twice and scans S6 (no
ultFx, no RNG, no call into the simulation, writes only presentation fields). Refuses to run on a
builder that already has S6.

THE RETURNED ROWS. The labs' reports reached this session relayed inline in the task text, cut off
mid-row (no report file on disk for Lodestone). What was relayed whole is checked here to the
character: the labels, anchors and modes of the relayed rows (voice row 1, picture rows 1-4) and lines
of each relayed body. The files are then tied to the labs' own records: the voice file equals the
lab's final confirmation run `rows_lab5.json` byte for byte (its STATE.md: sha16 b6f01158a986b7e1),
and the picture file's sha is the one the picture lab recorded (1ab82ea2383e20de), whose rows alone
reproduce its stamp (b40d52b7561c45f2, `ld-final.html`) on sc-lodestone-b205.
"""
import json, pathlib, hashlib, re, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone")
REPO = pathlib.Path("C:/dev/sundered-crown")
STAMP = "b40d52b7561c45f2"           # the picture lab's ld-final.html: picture rows alone on the base
PIC_FILE_SHA = "1ab82ea2383e20de"    # the picture lab's STATE.md (R2/R3): rows_final.json
VOICE_FILE_SHA = "b6f01158a986b7e1"  # the voice lab's STATE.md: rows_final.json = rows_lab5.json
PICVOICE_SHA = "7a095b143d66fbdb"    # the voice lab's sc-lodestone-picvoice.html (either order)
VOICE_ONLY_SHA = "8921a39052799d17"  # the voice lab's sc-lodestone-voice.html (the voice rows alone)
BASE_SHA = "6d736451a1ffc2df"        # sc-lodestone-b205.html (stage 5 = THE FINAL)
BUILDER_SHA = "0731db270893647b"     # tools/lodestone_build.py before stage 6

sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
fv_p, fp_p = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
assert sha(fp_p.read_bytes()) == PIC_FILE_SHA, "the picture rows file is not the one the lab recorded"
assert sha(fv_p.read_bytes()) == VOICE_FILE_SHA, "the voice rows file is not the one the lab recorded"
assert fv_p.read_bytes() == (S / "stage6-voice/rows_lab5.json").read_bytes(), \
    "the voice rows file is not the lab's final confirmation run"
fv = json.loads(fv_p.read_text(encoding="utf-8"))
fp = json.loads(fp_p.read_text(encoding="utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
assert len(fv) == 3 and len(fp) == 9, (len(fv), len(fp))

# What the relayed reports carried whole (label, anchor, mode), to the character.
RELAYED = [
    (fv[0], "Sfx: Lodestone's cast, touch and close arms, before the shared rune-crack fallback",
     "        } else {                                        // rune-crack", "replace"),
    (fp[0], "rebuttal picture: fighter fields", "    this.ultRunes = null;\n    this.runeTally = null;\n", "after"),
    (fp[1], "rebuttal picture: the presentation call", "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n", "after"),
    (fp[2], "rebuttal picture: the hall's loop", "function shellHash(a, b){\n", "before"),
    (fp[3], "rebuttal picture: tickLode", "  tickWinnow(dt){\n", "before"),
]
for r, label, anchor, mode in RELAYED:
    assert (r["label"], r["anchor"], r["mode"]) == (label, anchor, mode), label
# ... and lines of each relayed code body, verbatim from the relay.
V0 = fv[0]["code"]
assert V0.startswith('        } else if (w === "lodestone"){                  // the walls are runed\n'
                     "          /* LODESTONE'S CAST, THE WALLS RUNED -- v70 \u00a76.2: \"a rising four-note\n")
for line in ('          const g = 0.1906, D = 0.228;\n',
             '          [0, 3, 7, 12].forEach((s, k) => {\n',
             '        } else if (w === "lodestone-touch"){            // a wall answers\n',
             '          const n = clamp(Math.round(p.n || 1), 1, 5), f = 220 * Math.pow(2, [0, 3, 5, 7, 10][n - 1] / 12), g = 0.1946, D = 0.1;\n',
             '          this._burst(t, { freq: 6000, q: 0.7, gain: g * 0.5, dur: 0.012, type:"highpass" });\n',
             '        } else if (w === "lodestone-close"){            // and the runes go dark\n',
             '          const top = 0.040788, D = 0.228, A = -65.602;\n'):
    assert line in V0, line
assert fp[0]["code"].startswith("    /* REBUTTAL'S PICTURE (v70 section 6.1), and none of it is the sim's: the\n")
for line in ("    this.lodeFade = 0;\n", "    this.lodeSeen = 0;\n", "    this.lodeFx = [];\n"):
    assert line in fp[0]["code"], line
assert fp[0]["code"].endswith("    this.lodeFx = [];\n")
assert fp[1]["code"] == "    this.tickLode(dt);                  // REBUTTAL'S PICTURE (v70 section 6.1)\n"
for line in ("function lodeHall(n){\n",
             "  const A = CONFIG.arena, x0 = n, y0 = n, x1 = A.w - n, y1 = A.h - n;\n",
             "function lodeNear(G, x, y){\n"):
    assert line in fp[2]["code"], line
for line in ("  tickLode(dt){\n",
             "      if (!T && !(f.lodeFade > 0)) continue;                   // <- zero burden\n",
             "      const Z = (this.over || !f.alive) ? null : f.ultRunes;\n",
             "        /* THE TOUCH. Not on the kill's step: the shatter o"):
    assert line in fp[3]["code"], line
print("the returned rows equal the files: voice 3/3 (== the lab's rows_lab5.json, its final confirmation "
      "run), picture 9/9 (the lab's recorded file); the relayed rows' labels, anchors, modes and lines "
      "of each relayed body match")

base_p = S / "links/sc-lodestone-b205.html"
g = base_p.read_text(encoding="utf-8")
assert "\r\n" not in g
assert sha(g.encode()) == BASE_SHA
print("base", base_p.name, BASE_SHA)


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply_rows(text, rows):
    for r in rows:
        assert text.count(r["anchor"]) == 1, r["label"]
        text = text.replace(r["anchor"], new_of(r), 1)
    return text


pic_sha = sha(apply_rows(g, fp).encode())
print("picture-only sha", pic_sha, f"(the picture lab's stamp: {STAMP})")
assert pic_sha == STAMP
voice_sha = sha(apply_rows(g, fv).encode())
print("voice-only sha", voice_sha, f"(the voice lab's voice page: {VOICE_ONLY_SHA})")
assert voice_sha == VOICE_ONLY_SHA

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

p = REPO / "tools/lodestone_build.py"
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "\nS6 = [" in s:
    raise SystemExit("the builder already has S6 -- not writing it twice")
assert sha(s.encode()) == BUILDER_SHA, "the builder is not the one this generator was written for"

out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v70 §6.1-6.2, brief stage 6), picked on",
       "# measurements under Rick's \"you pick i overrule\" by `lodestone_voice_lab.py`",
       "# and the picture lab (v102 §5). Presentation only: engine_ab over all 39",
       "# relics, Lodestone included, is the proof. The rows are byte-exact to the",
       "# labs' own files (voice 3, picture 9; no two share an anchor, so none is",
       f"# merged); the picture rows alone reproduce the picture lab's stamp",
       f"# ({STAMP}) on sc-lodestone-b205, the voice rows alone the voice lab's",
       f"# voice page ({VOICE_ONLY_SHA}). Voice first, then picture; the other order",
       "# writes the same bytes.",
       "#   THE VOICE: the cast (fireUlt's own `ult`/lodestone call, which fell",
       "#   through to rune-crack: EVEN, a rising four-note chime), a touch (in",
       "#   tickRunes, after its hex, pitched by the foe's count: ARC3, with the",
       "#   school's `hex-snap` under it) and the close (in tickRunes, on a clock",
       "#   close with both alive, before the close line: MIRROR, the chime",
       "#   reversed). Plain SFX.play; nothing is read back.",
       "#   THE PICTURE: `tickLode` in tickPresentation reads `ultRunes && !over &&",
       "#   alive` and `runeTally.touches` rising, and writes only its own `lode*`",
       "#   fields, a record's clock and path, a tag's count, `tags` (statusTag)",
       "#   and `taught`. The rune chain lights along the live hall's four walls",
       "#   from the caster's nearest wall (0.3s) and sheds 28 motes; a touch",
       "#   flares the wall's 60-unit span (0.15s), snaps a bar from the wall into",
       "#   the ball for one frame and trails a rune-streak off the hurled ball;",
       "#   the HEX tag prints the foe's count; the head burns its sigil while the",
       "#   walls are lit; the close runs dark from the far wall inward (0.4s), or",
       "#   all at once on the caster's fall. The runic warhammer's route",
       "#   (`_whConjured`, drawn by no relic before this one) becomes the design's",
       "#   square head on a dark haft. No beat, no stop, no fx.js edit: the",
       "#   design's field is drawn (reading 14); SPECS has no Lodestone entry.",
       "#   NAMES: the labs'. `drawLode` is a prefix of `drawLodeTop`, and `tickRunes`",
       "#   of nothing new, so every stage-6 name check below is on identifier",
       "#   boundaries.",
       "S6 = ["]
for label, old, new in edits:
    for x in (label, old, new):
        assert "'''" not in x and "\\" not in x and not x.endswith("'") and not x.startswith("'"), label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

tail = '''
# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`drawLode` is a prefix of `drawLodeTop`). The Sfx's cast arm is found by
# its whole `} else if (w === "lodestone"){` line.
S6_NAMES = ("tickLode", "drawLode", "drawLodeTop", "lodeHall", "lodeAt", "lodeOn", "lodeNear",
            "_lodeLit", "_lodeRunePath", "_lodeRunes", "_lodeWalls", "_lodeMotes", "_lodeFlare",
            "_lodeStreak", "_lodeBolt", "_lodeHead", "lodeFade", "lodeAge", "lodeOut", "lodeDie",
            "lodeU0", "lodeU1", "lodeSeen", "lodeFx", '"lodestone-touch"', '"lodestone-close"')
S6_CAST_ARM = '} else if (w === "lodestone"){'
# What stage 6's ADDED code may write: its own lode* fields (and a touch
# record's own clock), the canvas (`c`, `cc`), a tag's count, `taught.hex` and
# an oscillator's pitch. Arrays it may push to, splice or shift: its own
# records (`lodeFx`), a record's path and the drawers' local lists.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("lode") or obj.startswith("lode")
               or obj in ("c", "cc") or (obj, prop) in {("q", "t"), ("g", "val"),
                                                         ("taught", "hex"), ("frequency", "value")})
# (The canvas's own `fill()` is a draw, not an array's: `c` and `cc` pass.)
S6_ARRAY_OK = (lambda obj: obj.startswith("lode") or obj in ("pts", "walls", "out", "c", "cc"))
# The stage-6 hooks, each in the page exactly once (the touch's voice with the
# hex-snap on the line under it: other relics play `hex-snap` on their own).
S6_HOOKS = ('SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });\\n'
            '        SFX.play("hex-snap");',
            'SFX.play("ult", { w: "lodestone-close" });',
            S6_CAST_ARM, "this.tickLode(dt);", "this.drawLode(m);", "this.drawLodeTop(m);",
            "this._lodeHead(f, reach + 6);")


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (SPECS has no Lodestone entry, and the design's field is
    drawn: reading 14)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]

'''

reps = [
 ('''    stage 6   picture, voice, field       (not written yet)
''',
  '''    stage 6   picture, voice              -> sc-lodestone-b205-fx.html
              (on the final; no field: the rune motes are drawn, reading 14)
'''),
 ('''THE CLOCK. The window and the touch cooldown run on the window tickers' clock,
''',
  '''STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
and sound are Code's picks under "you pick i overrule"; v102 §5):
  9. THE CAST VOICE is the cast's own `SFX.play("ult", {w: "lodestone"})` in
     fireUlt's generic head, which fell through to rune-crack: an arm is ADDED
     before that shared fallback (EVEN: A C E A from A4, one note a wall, a
     note every 125 ms) and the fallback line is re-emitted unchanged for the
     relics that still fall through.
 10. A TOUCH'S VOICE plays once per touch in tickRunes, AFTER its hex, pitched
     by the count the foe then carries (the number its tag shows, 1-5; at the
     cap the hex's clock refreshes and it snaps at 5's note): ARC3, a 12 ms
     crack on a held square stepping up the A-minor pentatonic.
 11. "THE HEX'S OWN STUN VOICE UNDERNEATH IF IT LANDS" is the runic school's
     `hex-snap` (v80's "the hex -- its snap", the voice Corollary's echo plays
     when its hex lands), played under every touch: the hex's stun itself
     (tickStatus, every 1.15s) has no voice on this engine, and at hex 1 every
     touch's hex lands (at the cap it refreshes).
 12. THE CLOSE VOICE ("the chime reversed, quiet") plays only when the window
     closes BY ITS CLOCK with both fighters alive, on the close line's own
     clock test: never on a death (the caster's), and never at the verdict
     (tickRunes is not called once `over` is set, reading 1). MIRROR: the
     literal reversal needs an async render, and every clip rebuilds the synth
     synchronously (v88 §6b), so each note is re-struck in phase at a level
     climbing as the cast's decay reversed (envelope correlation 0.93).
 13. THE PICTURE lives on the FIGHTER (`lode*`), never on `m.ultFx` (open item
     25), driven by `tickLode` in tickPresentation. The walls read `ultRunes
     && !over && alive`, so they go dark at a kill that leaves `ultRunes` set
     through the verdict (reading 1): from the far wall inward over 0.4s, or
     all at once (0.1s) when the caster is the one that fell. A touch is found
     by watching `runeTally.touches` rise, so tickRunes keeps no record for the
     picture and the probe's whole-state reads ([6], [7]) need no new skip. A
     touch on the kill's step draws nothing (the shatter owns that frame).
 14. "FIELD SPEC: RUNE MOTES ALONG THE LIT WALLS, BOTH COPIES" IS DRAWN, not an
     fx.js field: a SPECS field fires once, at the cast edge, on the one ultFx
     slot, which Rebuttal holds for a median 0.66s of its 8s window, and
     spawns at the caster (a median 87 units from its nearest wall), where the
     lit walls run the whole hall. So 28 motes are shed off the lit walls for
     the window, drawn. fx.js is untouched (SPECS has no Lodestone entry).
 15. THE HEX TAG prints the foe's count on every touch, ONE HEX TAG ON THE FOE
     AT A TIME (Tendril's rule): the hammer's own blow tags hex too, so a tag
     already up takes the new count in place.
 16. THE SILHOUETTE: "a runic warhammer has no art -- a rune-etched square head
     on a dark haft, first cut". The runic warhammer's route, `_whConjured`
     (three conjured slices, drawn by no relic before this one), is redrawn as
     that head, with the school's sigil etched in its face; only a runic
     warhammer reaches it, and Lodestone is the only one. The bar is timed on
     the MATCH clock (the touch's step and the next: one frame at 60 fps).

THE CLOCK. The window and the touch cooldown run on the window tickers' clock,
'''),
 ('''STAGE_OUT = {"1": "sc-lodestone", "2": "sc-lodestone-runes", "3": "sc-lodestone-rebuttal",
             "5": "sc-lodestone-b205"}
''',
  block + tail + '''
STAGE_OUT = {"1": "sc-lodestone", "2": "sc-lodestone-runes", "3": "sc-lodestone-rebuttal",
             "5": "sc-lodestone-b205", "6": "sc-lodestone-b205-fx"}
'''),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''            edits, want = S3, ult_block(ULT["charge"], ULT["hurl"])
        else:
''',
  '''            edits, want = S3, ult_block(ULT["charge"], ULT["hurl"])
        elif A.stage == "6":
            # STAGE 6 GOES ON THE FINAL, ONCE: Lodestone's ult block is stage
            # 3's to the character and its blade stage 5's; none of stage 6's
            # names is in the source yet (on identifier boundaries) and the
            # Sfx has no Lodestone arm.
            want = ult_block(ULT["charge"], ULT["hurl"])
            if (" ".join(strip_comments(want).split()) != " ".join(blk0.split())
                    or f"dmg:{BLADE}," not in relic_row(code, RELIC)):
                raise SystemExit(f"stage 6 goes on the final (stage 5's link, blade {BLADE}): "
                                 "Lodestone's ult block or blade is not the final's")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_CAST_ARM in code:
                raise SystemExit("the Sfx already has a Lodestone arm -- stage 6 goes on once")
            edits = S6
        else:
'''),
 ('''    for label, _old, new in S1 + S2 + S3 + (S5 if BLADE is not None else []):
        ins = strip_comments(new)''',
  '''    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves, shatters or ticks the
    # runes, writes only what S6_WRITE_OK names and mutates only its own
    # arrays. It READS the window, the tally, the foe's count and position;
    # the probe's [10]-[11] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickRunes|checkEnd|breakSpin)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(push|splice|pop|shift|unshift|reverse|sort|fill)\\(", ins):
            if not S6_ARRAY_OK(mw.group(1)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\[[^\\]]*\\]\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_ARRAY_OK(mw.group(1).split(".")[-1]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
    if A.stage == "6":
        if inlined_fx(s) != inlined_fx(s0):
            raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy")
        for need in S6_HOOKS:
            if out_code.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields); the inlined fx.js untouched; three voices and the "
              "picture's four hooks wired once each")
    for label, _old, new in S1 + S2 + S3 + (S5 if BLADE is not None else []) + S6:
        ins = strip_comments(new.replace(_old, "", 1) if _old in new else new)'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("stage 6 written into", p.name, ":", len(edits), "edits;", "sha", sha(s.encode()))
(S / "s6/expected_fx_sha.txt").write_text(full_sha + "\n")
