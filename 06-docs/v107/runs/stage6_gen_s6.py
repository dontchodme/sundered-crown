"""Write Lightkeeper / Bulwark's stage 6 into tools/lightkeeper_build.py from the labs' byte-exact row files.

    python gen_s6.py            (checks everything, then writes the builder once)

It checks, before it writes:
  - each row file is the lab's own (its sha256 as the lab's STATE records it) and every row has the
    four fields a row carries;
  - the picture rows alone reproduce the picture lab's stamp on sc-lightkeeper-bulwark-b9.5
    (728d64f8397290a1), the voice rows alone the voice lab's (a8629a7fe94d50b9), and both, in either
    order, the same page (e3f16bf01f0e2995, the voice lab's co-apply);
  - no row's anchor sits inside another's; rows that share an anchor LINE are merged into one edit
    (none do here: the list is printed);
  - no row carries a triple quote or a backslash (it is written as a Python ''' string).
"""
import hashlib, json, pathlib, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-"
                 "claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper")
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/lightkeeper_build.py")
sha = lambda b: hashlib.sha256(b).hexdigest()
FILES = {"voice": (S / "stage6-voice/rows_final.json", "814d0a16d8911102"),
         "picture": (S / "stage6-picture/rows_final.json", "f9b7579caa065664")}
rows = {}
for k, (p, want) in FILES.items():
    b = p.read_bytes()
    assert sha(b)[:16] == want, (k, sha(b)[:16])
    r = json.loads(b.decode("utf-8"))
    r = r["rows"] if isinstance(r, dict) else r
    for x in r:
        assert set(x) >= {"label", "anchor", "mode", "code"} and x["mode"] in ("before", "after", "replace"), x
    rows[k] = r
    print(f"{k}: {len(r)} rows, {p.name} sha16 {sha(b)[:16]} (the lab's)")
fv, fp = rows["voice"], rows["picture"]


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rs):
    for r in rs:
        assert t.count(r["anchor"]) == 1, r["label"]
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


base = (S / "links/sc-lightkeeper-bulwark-b9.5.html").read_text(encoding="utf-8")
assert sha(base.encode())[:16] == "d60a5c63b785ad04"
h16 = lambda t: sha(t.encode("utf-8"))[:16]
pic, voi = apply(base, fp), apply(base, fv)
both_vp, both_pv = apply(voi, fp), apply(pic, fv)
print("picture rows alone", h16(pic), "(the picture lab's stamp: 728d64f8397290a1)")
print("voice rows alone  ", h16(voi), "(the voice lab's: a8629a7fe94d50b9)")
print("voice then picture", h16(both_vp), " picture then voice", h16(both_pv), "(the voice lab's co-apply: e3f16bf01f0e2995)")
assert h16(pic) == "728d64f8397290a1" and h16(voi) == "a8629a7fe94d50b9"
assert both_vp == both_pv and h16(both_vp) == "e3f16bf01f0e2995"

# no row's anchor inside another's; merge rows that share an anchor LINE (none expected)
allr = fv + fp
for i, a in enumerate(allr):
    for j, b in enumerate(allr):
        if i != j:
            assert a["anchor"] not in b["anchor"], (a["label"], b["label"])
# A SHARED ANCHOR is one span of the base two rows both hang on (the same anchor text); such rows
# would be merged into one edit. Spans that merely overlap would be refused. Read on the base.
spans = []
for r in allr:
    i = base.find(r["anchor"])
    assert i >= 0 and base.count(r["anchor"]) == 1, r["label"]
    spans.append((i, i + len(r["anchor"]), r["label"]))
spans.sort()
same = [(a[2], b[2]) for a, b in zip(spans, spans[1:]) if (a[0], a[1]) == (b[0], b[1])]
overlap = [(a[2], b[2]) for a, b in zip(spans, spans[1:]) if b[0] < a[1] and (a[0], a[1]) != (b[0], b[1])]
print("rows on one anchor span:", same or "none -- nothing to merge", "| overlapping spans:", overlap or "none")
assert not same and not overlap, "merge / refuse by hand (the pattern's merge step)"
edits = [(r["label"], r["anchor"], new_of(r)) for r in fv + fp]
t = base
for _, old, new in edits:
    assert t.count(old) == 1
    t = t.replace(old, new, 1)
assert t == both_vp
for label, old, new in edits:
    for s in (label, old, new):
        assert "'''" not in s and "\\" not in s, label

HEAD = '''
# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v77 §5, the brief's "Stage 4 -- picture, voice,
# carry"), picked on measurements under Rick's "you pick i overrule" by
# `lightkeeper_voice_lab.py` and the picture lab (v107 §5). Presentation only:
# engine_ab over all 38 relics, Lightkeeper included, is the proof. The rows
# are byte-exact to the labs' own files (voice 4, picture 9; no two share an
# anchor, so none is merged; seven re-emit their anchor, six replace it). The
# picture rows alone reproduce the picture lab's stamp on the final
# (728d64f8397290a1), the voice rows alone the voice lab's (a8629a7fe94d50b9),
# and both, in either order, the same page (e3f16bf01f0e2995). Voice first,
# then picture.
#   THE VOICE: the raise is the cast's own `ult`/lightkeeper call in fireUlt's
#   shared prelude, which fell through to rune-crack (PLATE: a plate's ring
#   gliding A3 -> A4 in 0.36s, swelling); a gong a ball block (LOW-E, a plate
#   on E2), in the block branch after its tally; a tink an arrow (PIN, a small
#   plate on C8), after its tally, flammed 26 ms x min(5, k) by its index k in
#   the frame; the fold (FADE, the slide falling A4 -> A3) before the close
#   line, on a close BY THE CLOCK with both alive only (a death's close is the
#   death voice's; a wall standing when the fight ends folds in the picture
#   only). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickBulwark` in tickPresentation reads `ultWall && alive &&
#   !over`, `wallTally` rising and the shots in the air, and writes only its
#   own `bulwark*` fields, a float, a tag and `taught`: the bar (6 wide, vigil
#   pink, a pale heart, a soft 14-unit halo, ten motes off its faces) rises
#   out of the ward ring over 0.25s and folds back into it; a block flashes it
#   white for two frames; an arrow leaves a 0.3s scorch where it died on the
#   bar; a bank floats "+N" on the caster and, once a window, the WARD tag.
#   `drawBulwark` draws it over both fighters, every ball's disc cut out. The
#   nova's art is retired: the two plate branches on the ultFx slot, the life
#   map's 1.5, the charge rune's ring and shield. No beat, no stop, no fx.js
#   edit: the design's motes are drawn (reading 13), and the nova's field spec
#   (`SPECS.lightkeeper`) leaves BOTH copies by the orchestrator's
#   `fx_remove.py`, not here (fx.js is shared; reading 14).
S6 = ['''
out = [HEAD]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

TAIL = '''
# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`bulwarkScorch` is a suffix of `_bulwarkScorch`; the base's renderer reads
# `u.w === "lightkeeper"` in the two nova branches stage 6 retires, so the Sfx
# arm is found by its whole `} else if (w === "lightkeeper"){` line, never by
# the comparison).
S6_NAMES = ("tickBulwark", "drawBulwark", "_bulwarkBar", "_bulwarkAt", "_bulwarkLine", "_bulwarkHalo",
            "_bulwarkMotes", "_bulwarkBody", "_bulwarkScorch", "bulwarkFade", "bulwarkAge", "bulwarkOut",
            "bulwarkFlash", "bulwarkSeen", "bulwarkShots", "bulwarkScorch", "bulwarkTagged", "tinkK",
            '"lightkeeper-gong"', '"lightkeeper-tink"', '"lightkeeper-fold"')
S6_CAST_ARM = '} else if (w === "lightkeeper"){'
# What stage 6's ADDED code may write: its own bulwark* fields (and their
# arrays' length), the canvas, a scorch record's own clock, `taught.ward`, an
# oscillator's pitch, and the length of `P` (tickBulwark's alias of its own
# `bulwarkShots`). Arrays it may push to, splice, sort or index-write: its own
# bulwark* arrays, their aliases `P` (bulwarkShots) and `S` (bulwarkSeen), and
# the locals `near` and `pts`.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("bulwark") or obj.startswith("bulwark") or obj == "c"
               or (obj, prop) in {("q", "t"), ("taught", "ward"), ("frequency", "value"), ("P", "length")})
S6_ARRAY_OK = (lambda obj: obj.startswith("bulwark") or obj in ("P", "S", "near", "pts"))


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies, with fx_remove.py)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]

'''
src = BUILDER.read_text(encoding="utf-8")
assert sha(src.encode())[:16] == "0cc27d7b775b6d2c", sha(src.encode())[:16]
anchor = '''BLADE = 9.5

S5 = [
("the blade: the shipped rate",
 \'\'\'  { id:"lightkeeper", name:"Lightkeeper", aff:"vigil", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, dmg:10.54,\'\'\',
 f\'\'\'  {{ id:"lightkeeper", name:"Lightkeeper", aff:"vigil", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, dmg:{BLADE},\'\'\'),
]
'''
assert src.count(anchor) == 1
src = src.replace(anchor, anchor + block + TAIL, 1)

READINGS = '''STAGE 6 -- THE PICTURE AND THE VOICE (design §5, the brief's stage 4), on the
final (stage 5's link), picked on measurements by `lightkeeper_voice_lab.py`
and the picture lab under Rick's "you pick i overrule" (v107 §5). The
readings, where the labs had to choose:
 10. THE RAISE IS THE CAST'S OWN VOICE. fireUlt's shared prelude already plays
     SFX.play("ult", { w: f.w.id }) on every cast; Lightkeeper had no arm and
     fell through to rune-crack. The raise is an Sfx arm keyed "lightkeeper",
     added before that shared fallback (which eleven other relics on the
     final still use), so the cast needs no row in the simulation.
 11. THE FOLD SOUNDS ONLY ON A CLOSE BY THE CLOCK WITH BOTH ALIVE (Tendril's,
     Canopy's and Zenith's rule): a caster's death ends the fight and a close
     after the foe's death is its kill flight's, both the death voice's; a
     wall still up when the fight ends is never closed by tickLightwall (it
     does not run once `over` is set) and folds in the picture only.
 12. THE TINKS OF ONE FRAME ARE FLAMMED: the k-th arrow the wall stops in one
     call is struck 26 ms x min(5, k) late (the nova's flam), so four arrows
     are four tinks. `k` is a `var` local to the ticker's call.
 13. THE DESIGN'S "motes along the bar (both fx.js copies)" ARE DRAWN, not a
     SPECS field: a field fires once, at the one ultFx slot's cast edge and
     spot, and the slot is Lightkeeper's for a median 0.64s of the 8s window
     (the opponent's cast takes it at once on 24 of 145); after that the
     bar's centre stands a median 181 units from the cast point, and the bar
     turns a median 7.6 rad a window. Ten motes shed off both faces of the
     bar, placed by shellHash (no rng). Rick's to overrule (Zenith's,
     Canopy's, Temper's and Quarrelstorm's precedent).
 14. THE NOVA'S FIELD SPEC (`SPECS.lightkeeper`, a 1500-particle burst) is the
     brief's "nova's field spec out", and fx.js is shared by every build in
     the batch: it leaves BOTH copies by the orchestrator's `fx_remove.py
     --relic lightkeeper`, not here. This builder asserts its inlined copy
     untouched; until the removal the stage-6 link still fires the burst at
     each cast.
 15. THE BAR IS READ OFF `ultWall && alive && !over` and folds on either, so a
     fight that ends with the wall up folds it in the verdict.
 16. A BLOCK AND AN ARROW ARE FOUND BY WATCHING `wallTally` RISE: the ticker
     makes no call for the picture. A stopped arrow is spliced before the
     picture sees it, so its scorch is placed from where each live shot will
     be after its next move (tickShots' own arithmetic, kept as plain
     numbers), nearest the wall first; an arrow loosed and stopped inside one
     step scorches where the foe's bow tip meets the bar.
 17. A CONTACT WHILE THE BAR IS STILL RISING SNAPS IT UP (Canopy's sprout
     rule): the wall is live from the cast's first frame.
 18. THE BANK SHOWS ON THE CASTER in the vigil branch's own float ("+N": its
     colour, size and seat), a block's and an arrow's alike, and nothing at
     the cap; once a window, the WARD tag (the first in a match carrying its
     one line: the vigil branch's own teaching).
 19. THE NOVA'S ART IS RETIRED WITH THE NOVA: its plate ring (drawUltUnder)
     and its eighteen plates (drawUltOver) on the ultFx slot, the life map's
     1.5 (the slot falls to the map's own 1.5: no change in what it does), and
     the charge rune's ring and shield (ULTSIG), redrawn as five ward plates
     with a bar standing up out of their front as the charge fills.
 The picks are measurements, not readings: the raise PLATE, the gong LOW-E,
 the tink PIN, the fold FADE; the picture's sizes are the design's (220 x 6,
 a 14-unit halo, 50 ahead, out of the R + 17 ward ring, a 0.25s rise and
 fold, a two-frame flash, a 0.3s scorch).

THE CLOCK. The window and the cooldown run on the window tickers' clock, which'''

GUARD6 = '''    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or moves, writes only what
    # S6_WRITE_OK names and mutates only its own arrays. It READS the window,
    # the tally, the shots and the fighters; the probe's [9]-[10] and
    # engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickLightwall|tickShots|spawnShot|move)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(push|splice|pop|shift|unshift|reverse|sort|fill|copyWithin)\\(", ins):
            if mw.group(2) == "fill" and mw.group(1) == "c":
                continue                                   # the canvas's fill(), not an array's
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
                             "(the nova's field spec is the orchestrator's fx_remove.py)")
        if re.search(r'\\bu\\.w === "lightkeeper"', out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's art on the ultFx slot is still drawn")
        if re.search(r"\\blightkeeper: 1\\.5\\b", out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's life entry is still in the map")
        for need, n in (('SFX.play("ult", { w: "lightkeeper-tink", k: tinkK++ });', 1),
                        ('SFX.play("ult", { w: "lightkeeper-gong" });', 1),
                        ('if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });', 1),
                        (S6_CAST_ARM, 1), ('} else if (w === "lightkeeper-gong"){', 1),
                        ('} else if (w === "lightkeeper-tink"){', 1), ('} else if (w === "lightkeeper-fold"){', 1),
                        ("this.tickBulwark(dt);", 1), ("  tickBulwark(dt){", 1),
                        ("this.drawBulwark(m);", 1), ("  drawBulwark(m){", 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields); the inlined fx.js untouched; the nova's art out; "
              "four voices and one picture hook wired once each")
'''

reps = [
 ('    stage 6   picture, voice, field           (not written yet: the design\'s stage 4)\n',
  '    stage 6   picture, voice (brief stage 4)  -> sc-lightkeeper-bulwark-b9.5-fx.html\n'
  '              (on the final; the nova\'s field spec leaves BOTH copies of fx.js by the\n'
  '              orchestrator\'s fx_remove.py, not here: reading 14)\n'),
 ('this build\'s stage 6. Nothing in the simulation reads any of it.\n',
  'this build\'s stage 6 (readings 10-19). Nothing in the simulation reads any of it.\n'),
 ('THE CLOCK. The window and the cooldown run on the window tickers\' clock, which', READINGS),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''        else:
            if f'bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},' not in row \\
                    or "dmg:10.54," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")''',
  '''        elif A.stage == "6":
            # STAGE 6 GOES ON THE FINAL, ONCE: the bank 3 / 3 and the blade
            # 9.5 (stage 5's link); none of stage 6's names is in the source
            # yet (on identifier boundaries) and the Sfx has no Lightkeeper arm.
            if (f'bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},' not in row
                    or f"dmg:{BLADE}," not in row):
                raise SystemExit("stage 6 goes on the final (stage 5's link: the bank "
                                 f"{ULT['bankBall']} / {ULT['bankShot']}, blade {BLADE})")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_CAST_ARM in code:
                raise SystemExit("the Sfx already has a Lightkeeper arm -- stage 6 goes on once")
            edits, want = S6, ult_block(ULT["charge"], ULT["bankBall"], ULT["bankShot"])
        else:
            if f'bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},' not in row \\
                    or "dmg:10.54," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")'''),
 ('    for label, _old, new in S1 + S2 + S3 + S5:\n',
  GUARD6 + '    for label, _old, new in S1 + S2 + S3 + S5 + S6:\n'),
 ('''    row = relic_row(code, RELIC)
    if PHYS not in " ".join(row.split()):''',
  '''    row = relic_row(code, RELIC)
    # Stage 6 goes on stage 5's link, whose blade is BLADE; the rest of the
    # profile is still the shipped one.
    phys = PHYS if A.stage != "6" else PHYS.replace("dmg:10.54,", f"dmg:{BLADE},")
    if phys not in " ".join(row.split()):'''),
]
for a, b in reps:
    assert src.count(a) == 1, a[:70]
    src = src.replace(a, b, 1)
pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else BUILDER).write_text(src, encoding="utf-8", newline="\n")
print(f"S6 written: {len(edits)} edits ({len(fv)} voice, {len(fp)} picture) -> {sys.argv[1] if len(sys.argv) > 1 else BUILDER}")
