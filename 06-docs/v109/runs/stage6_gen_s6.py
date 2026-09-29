"""Write Censer's stage 6 into tools/censer_build.py from the labs' byte-exact row files.

The pattern's (ironwood build/iw6, widowmaker, angelus, lightkeeper s6int): the rows the labs RETURNED
equal the files (their reports as relayed, a prefix: check_inline.py); the voice rows alone and the
picture rows alone each reproduce their lab's own page; both orders of the two sets give the same bytes;
no row's anchor sits inside another row's anchor or code; rows that share an anchor are MERGED into one
edit. Writes an S6 list of triple-quoted strings into the builder and wires a --stage 6 that refuses to
run twice and scans S6 for ultFx (and the rest). Run once; it refuses if the builder already carries S6.
"""
import hashlib, json, pathlib, re, subprocess, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/censer")
BASE = S / "links" / "sc-censer-consecration-b25.5.html"
FV, FP = S / "stage6-voice" / "rows_final.json", S / "stage6-picture" / "rows_final.json"
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/censer_build.py")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]
DRY = "--dry" in sys.argv


def load(p):
    r = json.loads(p.read_text(encoding="utf-8"))
    return r["rows"] if isinstance(r, dict) else r


print(f"voice rows   {FV.name} {sha(FV.read_bytes())}")
print(f"picture rows {FP.name} {sha(FP.read_bytes())}")
assert sha(FV.read_bytes()) == "63c842fa690c5f02" and sha(FP.read_bytes()) == "5133d7afb3acb9e9", "a row file moved"
fv, fp = load(FV), load(FP)
assert len(fv) == 3 and len(fp) == 10
# THE ROWS THE LABS RETURNED ARE THE FILES: their reports, as the orchestrator relayed them (truncated),
# are a prefix of json.dumps({"rows": rows}) of each file
r = subprocess.run([sys.executable, str(S / "s6" / "check_inline.py")], capture_output=True, text=True)
print(r.stdout.rstrip())
assert r.returncode == 0 and r.stdout.count("PREFIX OK") == 2, "the relayed reports are not the row files"
for x in fv + fp:
    assert x["mode"] in ("before", "after", "replace"), x["label"]
    for k in ("label", "anchor", "code"):
        assert "'''" not in x[k] and "\\" not in x[k] and "\r" not in x[k], (x["label"], k)
    assert not x["code"].endswith("'") and not x["anchor"].endswith("'"), x["label"]

g = BASE.read_text(encoding="utf-8")
assert sha(g) == "56c49ad3f0ccb3aa", "the base moved"


def new_of(x):
    return {"before": x["code"] + x["anchor"], "after": x["anchor"] + x["code"], "replace": x["code"]}[x["mode"]]


def apply(t, rows, tag):
    for x in rows:
        assert t.count(x["anchor"]) == 1, (tag, x["label"], t.count(x["anchor"]))
        t = t.replace(x["anchor"], new_of(x), 1)
    return t


tp = apply(g, fp, "picture")
tv = apply(g, fv, "voice")
print(f"picture rows alone -> {sha(tp)}  (the picture lab's stamp: b3f790861677e2bd)")
print(f"voice rows alone   -> {sha(tv)}  (the voice lab's page:  6af8bc7cac4bf257)")
assert sha(tp) == "b3f790861677e2bd" and sha(tv) == "6af8bc7cac4bf257"
assert tp.encode("utf-8") == (S / "stage6-picture" / "ce-final.html").read_bytes(), "not the picture lab's ce-final.html"
assert tv.encode("utf-8") == (S / "stage6-voice" / "sc-censer-voice.html").read_bytes(), "not the voice lab's page"
vp, pv = apply(tv, fp, "voice+picture"), apply(tp, fv, "picture+voice")
assert vp == pv, "the two orders differ"
assert sha(vp) == "3d68c7648a9cb3a8", "not the picture lab's co-apply (order.out [4])"
print(f"both sets, either order -> {sha(vp)} (identical; the picture lab's co-apply 3d68c7648a9cb3a8)")

# no row's anchor inside another row's anchor or code (both sets); identical anchors are MERGED
rows = fv + fp
for i, x in enumerate(rows):
    for j, q in enumerate(rows):
        if i == j or x["anchor"] == q["anchor"]:
            continue
        assert x["anchor"] not in q["anchor"], ("anchor inside anchor", x["label"], q["label"])
        assert x["anchor"] not in q["code"], ("anchor inside another row's code", x["label"], q["label"])
# and no two anchors' spans overlap in the base
spans = sorted((g.index(x["anchor"]), g.index(x["anchor"]) + len(x["anchor"]), x["label"]) for x in rows)
for (a0, a1, la), (b0, b1, lb) in zip(spans, spans[1:]):
    assert a1 <= b0, ("anchor spans overlap", la, lb)
groups, order = {}, []
for x in rows:
    if x["anchor"] not in groups:
        groups[x["anchor"]] = []
        order.append(x["anchor"])
    groups[x["anchor"]].append(x)
edits, merged = [], 0
for anc in order:
    grp = groups[anc]
    if len(grp) == 1:
        x = grp[0]
        edits.append((x["label"], anc, new_of(x)))
        continue
    assert all(x["mode"] != "replace" for x in grp), ("a replace row shares an anchor", [x["label"] for x in grp])
    merged += len(grp) - 1
    new = "".join(x["code"] for x in grp if x["mode"] == "before") + anc + \
          "".join(x["code"] for x in grp if x["mode"] == "after")
    edits.append((" + ".join(x["label"] for x in grp), anc, new))
t = g
for label, old, new in edits:
    assert t.count(old) == 1, label
    t = t.replace(old, new, 1)
assert t == vp, "the merged edits do not give the rows' page"
print(f"{len(rows)} rows -> {len(edits)} edits ({merged} merged on a shared anchor); edits reproduce {sha(t)}")
consumed = [lab for lab, old, new in edits if old not in new]
print(f"anchors NOT re-emitted by their edit ({len(consumed)}): {consumed}")
assert len(consumed) == 4

# THE NAMES stage 6 brings, free on the base on identifier boundaries
S6_NAMES = ("tickConsecration", "drawConsecration", "drawConsecrationTop", "_consLive", "_consGeom", "_consFill",
            "_consHatch", "_consEdge", "_consMotes", "_consRim", "_consDrift", "consFade", "consAge", "consOut",
            "consEnd", "consPic", "consFoeOn", "consSelfOn", "consFoeLit", "consSelfLit", "consPulse", "consSeen",
            "consTagS", "consTagB", "censer-disc")
free = lambda name, code: not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)
for nm in S6_NAMES:
    assert free(nm, g), f"{nm} is on the base"
    assert not free(nm, vp), f"{nm} is not in the page"
print(f"{len(S6_NAMES)} names: free on the base, all in the page")


def strip_comments(js):
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


# the sim-path lines, read off the rows (the builder carries them as literals and checks them whole)
sim = {}
for label, old, new in edits:
    ins = strip_comments(new.replace(old, "", 1) if old in new else new)
    if label.startswith("resolveHit: the disc bell") or label.startswith("tickHolyGround: the heal chime"):
        sim[label] = [ln.strip() for ln in ins.splitlines() if ln.strip()]
    for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
        print(f"   write  {label[:44]:44s} {mw.group(1)}.{mw.group(2)}")
    for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort)\(", ins):
        print(f"   mutate {label[:44]:44s} {mw.group(1)}.{mw.group(2)}(")
    for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
        print(f"   index  {label[:44]:44s} {mw.group(1)}[...]")
print("sim-path lines:", json.dumps(sim, indent=1))
SIM_WANT = {
    "resolveHit: the disc bell": ['{ const sd_ = self === this.a ? "a" : "b";', 'let n_ = 0;',
                                  'for (const d_ of this.holyGround) if (d_.side === sd_) n_++;',
                                  'SFX.play("ult", { w: "censer-disc", n: n_ }); }'],
    "tickHolyGround: the heal chime": ['SFX.play("spark", { collect: true, n: f.stacks("blessing") });'],
}
for k, v in SIM_WANT.items():
    got = [sim[lab] for lab in sim if lab.startswith(k)]
    assert got == [v], (k, got)

if DRY:
    print("DRY: not writing the builder")
    sys.exit(0)

# ------------------------------------------------------------------ the builder
b = BUILDER.read_text(encoding="utf-8")
assert sha(b) == "78501578c5773570", "the builder moved"
assert "\nS6 = [" not in b, "the builder already carries S6"
out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (design §4 \"Picture\" and \"Sound\"; its §5",
       "# \"Stage 4 -- picture, voice, carry\"), picked on measurements under Rick's",
       "# \"you pick i overrule\" by the picture lab (scratch, `ce_rows.py`) and",
       "# `censer_voice_lab.py` (v109 §5). PRESENTATION ONLY: engine_ab over all 38",
       "# relics, Censer included, is the proof, and the probe's [10]-[11] read the",
       "# voices and the picture's hook inside the fight. The rows are byte-exact to",
       "# the labs' own files (voice 63c842fa690c5f02, 3 rows; picture",
       "# 5133d7afb3acb9e9, 10 rows); the picture rows alone reproduce the picture",
       "# lab's stamp (b3f790861677e2bd), the voice rows alone the voice lab's page",
       "# (6af8bc7cac4bf257), and the two sets give the same bytes in either order",
       "# (3d68c7648a9cb3a8). No two rows share an anchor, so none is merged.",
       "#   THE VOICE: two arms -- the cast's thurible swing and the disc's bell --",
       "#   ADDED before the shared rune-crack fallback, which is re-emitted",
       "#   unchanged, last; two calls on the sim path, each after a count this",
       "#   build's stage 2 already keeps (the bell after `holyTally.discs++` in",
       "#   resolveHit, the heal chime after `T.bless++` in tickHolyGround).",
       "#   THE PICTURE: `tickConsecration` in tickPresentation; the floor in the",
       "#   world pass under both balls (the discs, the lattice, the rims, the",
       "#   incense, the foe's rim, Censer's drift); the head's hot core in the",
       "#   emissive pass over both fighters; the nova's art retired (the glyph",
       "#   ring, the smoke, the life entry) and the charge rune redrawn.",
       "# COMPOSITION: nine anchors are re-emitted; four are consumed, all Censer's",
       "# own (the nova's two art branches, ULTSIG.censer, and the life map's",
       "# narrowest token `censer: 1.6,`, which leaves Aureole's entry on the same",
       "# line to its own build). The rows ride on three of stage 2's own lines",
       "# (the fields, the plant's count, the blessing's count) and on shared lines",
       "# every stage 6 of the batch uses as `after` / `before` anchors",
       "# (tickPresentation's first call, tickWinnow, the world and emissive passes,",
       "# drawMotes, the rune-crack fallback).",
       "S6 = ["]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]"]
block = "\n".join(out)

READINGS_S6 = '''
STAGE 6, THE PICTURE AND THE VOICE (design §4 "Picture" and "Sound"; §5's
"Stage 4 -- picture, voice, carry"). Picked on measurements under Rick's "you
pick i overrule" by the picture lab (scratch) and `censer_voice_lab.py` (v109
§5); the rows are the labs', byte-exact. Declared:
 13. THE PICTURE READS THE WINDOW OFF `ultHoly && alive && !over` and keeps
     its own state on the fighter (`cons*`), never on `m.ultFx` (one slot,
     and the foe's cast takes it: open item 25). `tickConsecration` runs in
     `tickPresentation`, on the presentation clock, which runs through hit
     stops and after `over`. So the head cools over 0.3s at a clock close, a
     death or the verdict (`tickHolyGround` never runs once `over` is set,
     and a window open at the kill would otherwise stay lit), and the ground
     fades out over 0.3s after the kill.
 14. THE DISCS ARE THE SIMULATION'S, READ AND NEVER WRITTEN: a picture record
     {d, age} per disc of `m.holyGround`, made the frame the disc exists and
     dropped the frame the simulation removes it. A disc blooms out of the
     impact point over 0.3s on the PRESENTATION clock (the planting blow's
     hit stop stops `holyT`; v54's lesson) and fades over the last second of
     its SIM life (`holyT - t0` against `groundLife`), reaching 0 the step it
     goes. It is drawn for its whole life: LIVE (fill 0.18) while its
     caster's window is open, INERT (0.07) once it closes -- the ground acts
     only in a window (reading 2) and works again at the next cast.
 15. ON THE GROUND IS `tickHolyGround`'S OWN TEST AS IT RAN, found by watching
     `holyTally` rise: a step the window ticked (`frames` rose) is a foe-on
     step iff `foeOn` rose with it, a Censer-on step iff `selfOn` did; a
     smite tick is `ticks` rising, a blessing `bless` rising. So the ticker
     makes no call for the picture. The tag rule (Corona's, Daybreak's,
     Zenith's, Canopy's, Benediction's): the first smite of each on-ground
     stretch tags SMITE on the foe, the first blessing BLESSING on Censer.
     The picture writes its `cons*` fields, the tags and `taught` only, and
     draws no rng (shellHash and the clocks place the incense).
 16. THE VOICES ON THE SIM PATH ARE TWO `SFX.play` CALLS, each a no-op
     headless that writes nothing the simulation reads: the disc's bell in
     `resolveHit`, once per disc planted, after `holyTally.discs++`, with n
     the caster's discs standing (a block-scoped count that reads
     `m.holyGround`), clamped to 1..5 in the arm; and the heal, the existing
     spark collect, unchanged, once per blessing after `T.bless++`, with the
     blessing Censer now carries (Zenith's call word for word). The cast's
     voice is fireUlt's own `SFX.play("ult", { w: f.w.id })`, which found no
     arm and fell through to rune-crack: the arms are ADDED before that
     shared fallback, which is re-emitted unchanged for the relics that
     still use it. The smite tick has no voice ("nothing new"; no smite voice
     exists in the synth). There is no close voice: the design names none.
 17. A DISC PLANTED BY A KILLING BLOW RINGS ITS BELL on the step the death
     voice plays (the survey: 32 of 716 discs); the bell is the blow's own
     consequence, and the design's "a disc opening" has no exception.
 18. NO fx.js FIELD (design §4: "incense motes rising from each disc (both
     fx.js copies)"). A SPECS field rides the one ultFx slot, fires once, at
     the cast, where Censer stood -- and no disc exists at the cast: the slot
     is Censer's a median 0.68s of the 8s window, and 10 of 163 discs exist
     while it is (the picture lab's fxprobe, 101 windows). The incense is
     drawn instead, off every disc, in the world pass. This builder edits
     neither fx.js copy, and stage 6 refuses if its edits touched the
     inlined one. The nova's `SPECS.censer` burst is the retired ultimate's:
     the orchestrator takes it out of both copies at the carry
     (`fx_remove.py --relic censer`). Rick's to overrule.
 19. THE NOVA'S ART IS RETIRED WITH THE NOVA: drawUltUnder's glyph ring and
     drawUltOver's smoke and incense sparks (both drawn at every cast from the
     ultFx record, out to the 300 fallback radius), and the life map's
     `censer: 1.6` (the cast's record falls to the map's own 1.5, and nothing
     draws from it). The charge rune, ULTSIG.censer, is redrawn: the censer
     swung over a disc of holy ground that fills with the charge. The four
     are replaced, not re-emitted: every other anchor is.
'''

HELPERS = '''

# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `cons*` fields, a picture record's clock, a
# tag's `taught`, the canvas and the synth's own nodes. Everything else is the
# simulation's.
S6_NAMES = ("tickConsecration", "drawConsecration", "drawConsecrationTop", "_consLive", "_consGeom", "_consFill",
            "_consHatch", "_consEdge", "_consMotes", "_consRim", "_consDrift", "consFade", "consAge", "consOut",
            "consEnd", "consPic", "consFoeOn", "consSelfOn", "consFoeLit", "consSelfLit", "consPulse", "consSeen",
            "consTagS", "consTagB", "censer-disc")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("cons") or obj.startswith("cons") or obj == "c"
               or (obj, prop) in {("p", "age"), ("taught", "smite"), ("taught", "blessing"),
                                  ("frequency", "value")})
# THE TWO CALLS ON THE SIM PATH, whole (reading 16): each row's added code,
# comments stripped, line for line.
S6_SIM_LINES = {
    "resolveHit: the disc bell": ['{ const sd_ = self === this.a ? "a" : "b";', 'let n_ = 0;',
                                  'for (const d_ of this.holyGround) if (d_.side === sd_) n_++;',
                                  'SFX.play("ult", { w: "censer-disc", n: n_ }); }'],
    "tickHolyGround: the heal chime": ['SFX.play("spark", { collect: true, n: f.stacks("blessing") });'],
}
S6_SFX_ROW = "Sfx: Censer's cast"
S6_TICK_ROW = "consecration picture: tickConsecration"
RUNE_CRACK = "        } else {                                        // rune-crack"


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 18)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_array_ok(obj: str, ins: str) -> bool:
    """An array stage 6 may change: its own `cons*` ones, or a name its row
    binds once, as `const X = f.cons...;` (tickConsecration's P and S)."""
    if obj.startswith("cons"):
        return True
    bound = re.findall(r"\\bconst " + re.escape(obj) + r" = \\w+\\.(cons\\w+);", ins)
    decls = re.findall(r"\\b(?:const|let|var)\\s+" + re.escape(obj) + r"\\b|[,(]\\s*" + re.escape(obj)
                       + r"\\s*=(?!=)|(?<![\\w.$])" + re.escape(obj) + r"\\s*=(?!=)", ins)
    return len(bound) == 1 and len(decls) == 1


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, beats, floats, rings or knocks,
    never writes the shared weapon row, writes only what S6_WRITE_OK names and
    mutates only its own arrays. Its two lines on the sim path are the two
    voice calls, whole, each in its own row; the synth's nodes only in the Sfx
    row; the tags and `taught` only in tickConsecration. The probe's [10]-[11]
    and engine_ab are the dynamic proof. Run on every stage: it reads the
    table."""
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickHolyGround|tickStatus|tickStasis|tickWeapon|tickHits|spawnShot|note|checkEnd)\\(", ins) \\
                or re.search(r"(?<!SG)\\.ring\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\\bw\\.[A-Za-z_]\\w*(\\.\\w+)*\\s*(=[^=]|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\\b(beat|hurt|knock|shake|hitStop)\\b", ins):
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
                             "outside the disc's bell and the heal")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickConsecration")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(push|splice|pop|shift|unshift|reverse|sort|fill|copyWithin)\\(", ins):
            if not s6_array_ok(mw.group(1), ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\[[^\\]]*\\]\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not s6_array_ok(mw.group(1).split(".")[-1], ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
        if re.search(r"\\bdelete\\s", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes a property")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched, the
    shared rune-crack fallback kept once and after Censer's arms, the nova's
    art gone, and every arm, call and pass wired exactly once."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 18)")
    if s.count(RUNE_CRACK) != 1 or s.find('} else if (w === "censer-disc"){') > s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Censer's arms")
    for gone in ('u.w === "censer"', "censer: 1.6"):
        if gone in out_code:
            raise SystemExit(f"REFUSING TO WRITE -- the nova's art is still drawn ({gone!r})")
    for need in ["this.tickConsecration(dt);", "if (__world) this.drawConsecration(m);",
                 "this.drawConsecrationTop(m);", "  tickConsecration(dt){", "  drawConsecration(m){",
                 "  drawConsecrationTop(m){", "  censer(c, t, cf, P){",
                 '} else if (w === "censer"){', '} else if (w === "censer-disc"){']:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        ln = [x for x in v if x.startswith("SFX.play(")][0]
        if out_code.count(ln) != code.count(ln) + 1:
            raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    if "  tickPresentation(dt){\\n    this.tickNovaFx(dt);\\n    this.tickConsecration(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickConsecration is not tickPresentation's second call")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the disc's bell and the heal chime its two lines on the sim path); "
          "the inlined fx.js untouched; the rune-crack fallback kept; the nova's art gone; every "
          "arm, call and pass once")
'''

reps = [
 # the docstring: the stage table
 ("    stage 6   picture, voice, the nova's art out (not written: design §5's stage 4)\n",
  "    stage 6   the picture and the voice  -> sc-censer-consecration-b<BLADE>-fx.html (presentation)\n"
  "              design §5's \"Stage 4 -- picture, voice, carry\", on stage 5's link;\n"
  "              no fx.js field (reading 18). The carry is the orchestrator's:\n"
  "              stages 1, 2, 3, 5 and 6 on its tip, and `fx_remove.py` for the\n"
  "              nova's SPECS entry.\n"),
 # the docstring: stage 6's readings, after reading 12
 (" 12. NOTHING ELSE: the hammer swings as ever.\n",
  " 12. NOTHING ELSE: the hammer swings as ever.\n" + READINGS_S6),
 # the tables and the helpers, before relic_row
 ("\n\n\ndef relic_row(code: str, rid: str) -> str:",
  "\n" + block + HELPERS + "\n\ndef relic_row(code: str, rid: str) -> str:"),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''        else:
            if BLADE is None:
                raise SystemExit("stage 5: BLADE is not set -- the blade is measured first "
                                 "(v109 §4)")
            if f'bless:{ULT["bless"]},' not in row or "dmg:28.77," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bless"])''',
  '''        elif A.stage == "5":
            if BLADE is None:
                raise SystemExit("stage 5: BLADE is not set -- the blade is measured first "
                                 "(v109 §4)")
            if f'bless:{ULT["bless"]},' not in row or "dmg:28.77," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bless"])
        else:
            # STAGE 6 GOES ON STAGE 5, ONCE: the heal on, the blade BLADE names,
            # none of stage 6's names in the source yet (on identifier
            # boundaries), and what the picture and the voice read there.
            if (BLADE is None or f'bless:{ULT["bless"]},' not in row
                    or f"dmg:{BLADE}," not in row or "tickHolyGround(dt){" not in code):
                raise SystemExit("stage 6 goes on stage 5 (the heal, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if '} else if (w === "censer"){' in code:
                raise SystemExit("Censer's cast voice is already in this source -- stage 6 goes on once")
            for need, why in (("function shellHash(", "no shellHash (the incense's hash, never the RNG)"),
                              ("function hexA(", "no hexA (the foe's rim)"),
                              ("  statusTag(x, y, key, first, val){", "no statusTag (the tags)"),
                              ('SFX.play("ult", { w: f.w.id });', "fireUlt no longer voices the cast by id"),
                              ('SFX.play("spark", { collect: true, n: f.stacks("blessing") });',
                               "no spark collect voice to reuse")):
                if need not in code:
                    raise SystemExit(f"wrong base for stage 6: {why}")
            edits, want = S6, ult_block(ULT["charge"], ULT["bless"])'''),
 ('''    for label, old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        check_insert(label, ins)
''',
  '''    for label, old, new in S1 + S2 + S3 + S5 + S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        check_insert(label, ins)
    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
'''),
]
for a_, b_ in reps:
    assert b.count(a_) == 1, a_[:80]
    b = b.replace(a_, b_, 1)
BUILDER.write_text(b, encoding="utf-8", newline="\n")
print(f"stage 6 written into {BUILDER.name}: {len(edits)} edits; builder now {sha(b)}")
(S / "s6" / "fx_expected.sha").write_text(sha(vp) + "\n")
