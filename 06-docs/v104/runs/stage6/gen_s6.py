"""Write Angelus's stage 6 into tools/angelus_build.py from the labs' byte-exact row files.

Widowmaker's gen_s6.py shape (batch/widowmaker/s6), after ironwood's (build/iw6): the rows the labs
RETURNED equal the files; the voice rows alone and the picture rows alone each reproduce their lab's own
page; both orders of the two sets give the same bytes; no row's anchor sits inside another row's anchor
or code; rows that share an anchor are MERGED into one edit. Run once; it refuses if the builder already
carries S6.
"""
import hashlib, json, pathlib, re, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/angelus")
BASE = S / "links" / "sc-angelus-b9.html"
FV, FP = S / "stage6-voice" / "rows_final.json", S / "stage6-picture" / "rows_final.json"
RV, RP = S / "s6" / "lab_report_voice.json", S / "s6" / "lab_report_picture.json"
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/angelus_build.py")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]


def load(p):
    r = json.loads(p.read_text(encoding="utf-8"))
    return r["rows"] if isinstance(r, dict) else r


print(f"voice rows   {FV.name} {sha(FV.read_bytes())}")
print(f"picture rows {FP.name} {sha(FP.read_bytes())}")
assert sha(FV.read_bytes()) == "70f47a5acf37e4f7" and sha(FP.read_bytes()) == "324d3654c51b4d04", "a row file moved"
fv, fp = load(FV), load(FP)
assert len(fv) == 4 and len(fp) == 8
# THE ROWS THE LABS RETURNED ARE THE FILES (their StructuredOutput, read out of the workflow's transcripts)
assert load(RV) == fv, "the voice lab returned other rows than its file"
assert load(RP) == fp, "the picture lab returned other rows than its file"
assert json.loads(RP.read_text(encoding="utf-8"))["stamp"] == "32d61ac685db232f"
print("the rows the labs returned == the row files (voice 4, picture 8)")
for r in fv + fp:
    assert r["mode"] in ("before", "after", "replace"), r["label"]
    for k in ("label", "anchor", "code"):
        assert "'''" not in r[k] and "\\" not in r[k] and "\r" not in r[k], (r["label"], k)

g = BASE.read_text(encoding="utf-8")
assert sha(g) == "db58100b3aa0092a", "the base moved"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows, tag):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (tag, r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


tp = apply(g, fp, "picture")
tv = apply(g, fv, "voice")
print(f"picture rows alone -> {sha(tp)}  (the picture lab's stamp: 32d61ac685db232f)")
print(f"voice rows alone   -> {sha(tv)}  (the voice lab's page:  32d55d74179c4335)")
assert sha(tp) == "32d61ac685db232f" and sha(tv) == "32d55d74179c4335"
assert tp.encode("utf-8") == (S / "stage6-picture" / "an-final.html").read_bytes(), "not the picture lab's an-final.html"
assert tv.encode("utf-8") == (S / "stage6-voice" / "sc-angelus-voice.html").read_bytes(), "not the voice lab's page"
vp, pv = apply(tv, fp, "voice+picture"), apply(tp, fv, "picture+voice")
assert vp == pv, "the two orders differ"
print(f"both sets, either order -> {sha(vp)} (identical)")

# no row's anchor inside another row's anchor or code (both sets); identical anchors are MERGED
rows = fv + fp
for i, r in enumerate(rows):
    for j, q in enumerate(rows):
        if i == j or r["anchor"] == q["anchor"]:
            continue
        assert r["anchor"] not in q["anchor"], ("anchor inside anchor", r["label"], q["label"])
        assert r["anchor"] not in q["code"], ("anchor inside another row's code", r["label"], q["label"])
groups, order = {}, []
for r in rows:
    if r["anchor"] not in groups:
        groups[r["anchor"]] = []
        order.append(r["anchor"])
    groups[r["anchor"]].append(r)
edits, merged = [], 0
for anc in order:
    grp = groups[anc]
    if len(grp) == 1:
        r = grp[0]
        edits.append((r["label"], anc, new_of(r)))
        continue
    assert all(r["mode"] != "replace" for r in grp), ("a replace row shares an anchor", [r["label"] for r in grp])
    merged += len(grp) - 1
    new = "".join(r["code"] for r in grp if r["mode"] == "before") + anc + \
          "".join(r["code"] for r in grp if r["mode"] == "after")
    edits.append((" + ".join(r["label"] for r in grp), anc, new))
t = g
for label, old, new in edits:
    assert t.count(old) == 1, label
    t = t.replace(old, new, 1)
assert t == vp, "the merged edits do not give the rows' page"
print(f"{len(rows)} rows -> {len(edits)} edits ({merged} merged on a shared anchor); edits reproduce {sha(t)}")
consumed = [lab for lab, old, new in edits if old not in new]
print(f"anchors NOT re-emitted by their edit: {consumed}")

# ------------------------------------------------------------------ the builder
b = BUILDER.read_text(encoding="utf-8")
assert sha(b) == "e5b0d70b8555a916", "the builder moved"
assert "\nS6 = [" not in b, "the builder already carries S6"
out = ["", "", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (the brief's stage 6; design §6.1 and §6.2),",
       "# picked on measurements under Rick's \"you pick i overrule\" by the picture",
       "# lab (scratch) and `angelus_voice_lab.py` (v104 §5). PRESENTATION ONLY:",
       "# engine_ab over all 39 relics, Angelus included, is the proof, and the",
       "# probe's [11]-[12] read the voices and the picture's hook inside the fight.",
       "# The rows are byte-exact to the labs' own files (voice 70f47a5acf37e4f7, 4",
       "# rows; picture 324d3654c51b4d04, 8 rows); the picture rows alone reproduce",
       "# the picture lab's stamp (32d61ac685db232f), the voice rows alone the voice",
       "# lab's page (32d55d74179c4335), and the two sets give the same bytes in",
       "# either order. No two rows share an anchor, so none is merged.",
       "#   THE VOICE: four arms -- the cast's chord, the shaft-hit tap, the close,",
       "#   the landing thud -- ADDED before the shared rune-crack fallback, which",
       "#   is re-emitted unchanged, last; three calls on the sim path (the tap and",
       "#   the close in tickRise, the thud in `move`: readings 14, 15 and 18).",
       "#   THE PICTURE: `tickAscend` in tickPresentation (readings 12-13); the",
       "#   world pass under both balls (the column, the halo, the pools); the",
       "#   shafts inside drawWeapon (bodies, motes, the blades at rest); the cores",
       "#   and the threads over both fighters; the body trail hidden while it is",
       "#   up (reading 16).",
       "# COMPOSITION: every anchor is re-emitted but the body trail's,",
       "# \"    const tr = f.trail;\" (reading 16), which no builder in tools/ contains",
       "# on 2026-09-28. The rows ride on four of stage 2's own lines (the fields,",
       "# the heal, the close) and on shared lines every stage 6 of the batch uses",
       "# as `after` / `before` anchors (tickPresentation, the world and emissive",
       "# passes, drawWeapon's tree hook, drawMotes, tickWinnow, move's bounce).",
       "S6 = ["]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]"]
block = "\n".join(out)

READINGS_S6 = '''
STAGE 6, THE PICTURE AND THE VOICE (the brief's stage 6; design §6.1 "the
picture" and §6.2 "sound"). Picked on measurements under Rick's "you pick i
overrule" by the picture lab (scratch) and `angelus_voice_lab.py` (v104 §5);
the rows are the labs', byte-exact. Declared:
 12. THE PICTURE READS THE WINDOW OFF `ultRise && !over && alive` (Canopy's
     rule) and keeps its own state on the fighter (`ascend*`), never on
     `m.ultFx` (one slot, and the foe's cast takes it: open item 25).
     `tickAscend` runs in `tickPresentation`, on the presentation clock, which
     runs through hit stops and after `over`. So the picture closes the window
     reading 10 leaves open at the kill -- the shafts shorten to blades over
     0.3s and the halo goes -- and, with `reachMul` still 10 through the
     verdict, `drawWeapon` draws the blades at rest. The sim's ball stays
     where it hung: no presentation-only drop (the picture lab's reading).
 13. THE PICTURE FINDS A SHAFT BLOW BY WATCHING `hits` RISE WHILE LIT (a blow
     on a shade counts, and heals: reading 11) and starts the blow's thread
     at the `hit` beat `resolveHit` filed that step, read and never written;
     it finds a heal by watching `riseTally.bless` rise. So neither tickRise
     nor resolveHit makes a call for the picture. It writes its own `ascend*`
     fields, the tags (the BLESSING tag, one on the caster at a time: a tag
     already up takes the new count) and `taught`, which nothing in the
     simulation reads; it draws no rng (shellHash and the clocks).
 14. THE VOICES ON THE SIM PATH ARE THREE `SFX.play` CALLS, each a no-op
     headless that writes nothing the simulation reads: the shaft-hit tap in
     tickRise's heal, once per shaft hit healed, after its blessing lands (n =
     the caster's blessing stacks, 1-5); the close chord in tickRise's close;
     the landing thud in `move`, on the first floor contact after that close
     with the caster alive. The thud's flag is `riseTally.falling`, on the
     probe's tally, which nothing in the simulation reads. The cast's voice is
     fireUlt's own `SFX.play("ult", { w: "angelus" })`, which found no arm and
     fell through to rune-crack: the arms are ADDED before that shared
     fallback, which is re-emitted unchanged for the relics that still use it.
 15. THE CLOSE CHORD (and so the thud) ONLY ON A CLOSE BY THE CLOCK WITH BOTH
     ALIVE. A caster's death closes the window in a kill flight, and a match
     that ends inside the window never reaches the tick again (reading 10):
     both are the death voice's moment, as for Zenith's, Canopy's and
     Onslaught's closes. A foe killed by its smite earlier in that step is
     not alive (the hp getter), so no chord plays over it.
 16. THE BODY TRAIL IS NOT DRAWN WHILE THE PICTURE IS UP (`ascendFade` > 0):
     `move` feeds the trail and skips a pinned ball, and `tickRise` carries
     the ball away, so for the whole window the trail drew a ghost of the ball
     at the cast point. This row REPLACES "    const tr = f.trail;" and does
     not re-emit it: the second anchor Angelus consumes (no builder in tools/
     contains it on 2026-09-28; the first is reading 8's spin product).
 17. NO fx.js FIELD (the brief's "the field in both copies"). A SPECS field
     rides the one ultFx slot, which Angelus holds a median 0.633s of window
     clock (7.4% of the window; the shafts light at 0.35), and fires once at
     the cast point, a median 226 units from the hang point the shafts turn
     about (the picture lab's fxprobe, 133 windows). The design's motes are
     drawn instead, in the world pass, down each shaft (Zenith's and Canopy's
     precedent). This builder edits neither copy, and stage 6 refuses if its
     edits touched the inlined one. Rick's to overrule.
 18. THE LANDING THUD IS NEW. The design names it (§6.2 "the ball's landing
     thud") and the engine had none: every floor contact plays the wall tick,
     which still plays under it.
'''

HELPERS = '''

# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `ascend*` fields, a thread record's clock, a
# tag's count, `taught`, the landing flag on the probe's tally, the canvas and
# the synth's own nodes. Everything else is the simulation's.
S6_NAMES = ("tickAscend", "drawAscend", "drawAscendTop", "drawAscendWeapon", "_ascendColumn", "_ascendHalo",
            "_ascendPools", "_ascendEdge", "_ascendLen", "_ascendBody", "_ascendMotes", "_ascendThreads",
            "ascendFade", "ascendAge", "ascendLit", "ascendOut", "ascendSeen", "ascendHeal", "ascendFx",
            "angelus-shaft", "angelus-close", "angelus-land")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("ascend") or obj.startswith("ascend") or obj == "c"
               or (obj, prop) in {("q", "t"), ("g", "val"), ("taught", "blessing"), ("T", "falling"),
                                  ("riseTally", "falling"), ("frequency", "value")})
S6_ARRAY_OK = (lambda obj: obj.startswith("ascend"))
# THE THREE CALLS ON THE SIM PATH, whole (reading 14): each row's added code,
# comments stripped, line for line.
S6_SIM_LINES = {
    "tickRise: the shaft-hit tap": ['SFX.play("ult", { w: "angelus-shaft", n: f.stacks("blessing") });'],
    "tickRise: the close": ["if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){",
                            'SFX.play("ult", { w: "angelus-close" });', "T.falling = 1;", "}"],
    "move: the landing thud": ["if (f.riseTally && f.riseTally.falling && f.alive && f.y >= hiY){",
                               "f.riseTally.falling = 0;", 'SFX.play("ult", { w: "angelus-land" });', "}"],
}
S6_SFX_ROW = "Sfx: Angelus's cast"
S6_TICK_ROW = "ascension picture: tickAscend"
RUNE_CRACK = "        } else {                                        // rune-crack"


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 17)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, beats, floats or knocks, never
    writes the shared weapon row, writes only what S6_WRITE_OK names and
    mutates only its own arrays. Its three lines on the sim path are the three
    voice calls, whole, each in its own row; the synth's nodes only in the Sfx
    row; the tag and `taught` only in tickAscend. The probe's [11]-[12] and
    engine_ab are the dynamic proof. Run on every stage: it reads the table."""
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickRise|tickStatus|tickStasis|tickWeapon|spawnShot|note|checkEnd)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\\bw\\.[A-Za-z_]\\w*(\\.\\w+)*\\s*(=[^=]|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\\b(beat|hurt|knock|ring|shake|hitStop)\\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' hurts, knocks, "
                             "stops or files a beat")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its voice call alone:\\n{ins}")
        elif "SFX" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the tap, the close and the landing")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickAscend")
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


def s6_output_checks(s: str, s0: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched, the
    shared rune-crack fallback kept once and after Angelus's arms, and every
    arm, call and pass wired exactly once."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 17)")
    if s.count(RUNE_CRACK) != 1 or s.find('} else if (w === "angelus-land"){') > s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Angelus's arms")
    for need in ["this.tickAscend(dt);", "this.drawAscend(m);", "this.drawAscendTop(m);",
                 "this.drawAscendWeapon(m, f, dim)", "const tr = f.ascendFade > 0 ? [] : f.trail;",
                 '} else if (w === "angelus"){', '} else if (w === "angelus-shaft"){',
                 '} else if (w === "angelus-close"){', '} else if (w === "angelus-land"){'] + \\
                [ln for v in S6_SIM_LINES.values() for ln in v if ln.startswith("SFX.play(")]:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the tap, the close and the landing its three lines on the sim path); "
          "the inlined fx.js untouched; the rune-crack fallback kept; every arm, call and pass once")
'''

reps = [
 # the docstring: the stage table
 ('    stage 5   the blade                   -> sc-angelus-b9.html      (11.95 -> 9)\n',
  '    stage 5   the blade                   -> sc-angelus-b9.html      (11.95 -> 9)\n'
  '    stage 6   the picture and the voice   -> sc-angelus-b9-fx.html   (presentation)\n'
  '              on stage 5\'s link; no fx.js field (reading 17). The carry is the\n'
  '              orchestrator\'s: stages 1, 2, 3, 5 and 6 on its tip.\n'),
 # the docstring: stage 6's readings, after reading 11
 ('''     the same `hits` delta, and the prose says "every hit heals".
''',
  '''     the same `hits` delta, and the prose says "every hit heals".
''' + READINGS_S6),
 # the tables and the helpers, before relic_row
 ('\n\n\ndef relic_row(code: str, rid: str) -> str:',
  block + HELPERS + '\n\ndef relic_row(code: str, rid: str) -> str:'),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''        else:
            if (f'healPer:{ULT["healPer"]},' not in blk0
                    or PHYS_OF(LAB_BLADE) not in " ".join(row0.split())):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = s5_edits(), ult_block(ULT["charge"], ULT["healPer"])''',
  '''        elif A.stage == "5":
            if (f'healPer:{ULT["healPer"]},' not in blk0
                    or PHYS_OF(LAB_BLADE) not in " ".join(row0.split())):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = s5_edits(), ult_block(ULT["charge"], ULT["healPer"])
        else:
            # STAGE 6 GOES ON STAGE 5, ONCE: the heal on, the blade BLADE names,
            # none of stage 6's names in the source yet (on identifier
            # boundaries), and the picture's hash function there to read.
            if (f'healPer:{ULT["healPer"]},' not in blk0 or "tickRise(dt){" not in code
                    or PHYS_OF(BLADE) not in " ".join(row0.split())):
                raise SystemExit("stage 6 goes on stage 5 (the heal, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if ".falling" in code or 'w === "angelus"' in code:
                raise SystemExit("Angelus's cast voice or its landing flag is already in this "
                                 "source -- stage 6 goes on once")
            if "function shellHash(" not in code:
                raise SystemExit("wrong base: no shellHash (the picture's hash, never the RNG)")
            edits, want = S6, ult_block(ULT["charge"], ULT["healPer"])'''),
 ('    blade = BLADE if A.stage == "5" else LAB_BLADE\n',
  '    blade = BLADE if A.stage in ("5", "6") else LAB_BLADE\n'),
 ('''    if len(re.findall(r'kind:"rise"', out_code)) != 1:''',
  '''    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, out_code)
    if len(re.findall(r'kind:"rise"', out_code)) != 1:'''),
]
for a_, b_ in reps:
    assert b.count(a_) == 1, a_[:80]
    b = b.replace(a_, b_, 1)
BUILDER.write_text(b, encoding="utf-8", newline="\n")
print(f"stage 6 written into {BUILDER.name}: {len(edits)} edits; builder now {sha(b)}")
(S / "s6" / "fx_expected.sha").write_text(sha(vp) + "\n")
