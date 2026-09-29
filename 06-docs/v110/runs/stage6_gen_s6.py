"""Write Aureole's stage 6 into tools/aureole_build.py from the labs' byte-exact row files.

The pattern's (ironwood build/iw6, censer s6): the rows the labs RETURNED equal the files (their
reports as relayed, a prefix: check_inline.py); the voice rows alone and the picture rows alone each
reproduce their lab's own page; both orders of the two sets give the same bytes; no row's anchor sits
inside another row's anchor or code; rows that share an anchor are MERGED into one edit. Writes an S6
list of triple-quoted strings into the builder and wires a --stage 6 that refuses to run twice and
scans S6 for ultFx (and the rest). Run once; it refuses if the builder already carries S6.
"""
import hashlib, json, pathlib, re, subprocess, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/aureole")
BASE = S / "links" / "sc-aureole-b12.5.html"
FV, FP = S / "stage6-voice" / "rows_final.json", S / "stage6-picture" / "rows_final.json"
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/aureole_build.py")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]
DRY = "--dry" in sys.argv


def load(p):
    r = json.loads(p.read_text(encoding="utf-8"))
    return r["rows"] if isinstance(r, dict) else r


print(f"voice rows   {FV.name} {sha(FV.read_bytes())}")
print(f"picture rows {FP.name} {sha(FP.read_bytes())}")
assert sha(FV.read_bytes()) == "5a43210cd9d13019" and sha(FP.read_bytes()) == "ed67bd6722cbbe2b", "a row file moved"
fv, fp = load(FV), load(FP)
assert len(fv) == 4 and len(fp) == 9
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
assert sha(g) == "21ea91d0f3c14274", "the base moved"


def new_of(x):
    return {"before": x["code"] + x["anchor"], "after": x["anchor"] + x["code"], "replace": x["code"]}[x["mode"]]


def apply(t, rows, tag):
    for x in rows:
        assert t.count(x["anchor"]) == 1, (tag, x["label"], t.count(x["anchor"]))
        t = t.replace(x["anchor"], new_of(x), 1)
    return t


tp = apply(g, fp, "picture")
tv = apply(g, fv, "voice")
print(f"picture rows alone -> {sha(tp)}  (the picture lab's stamp: b8d571f46a2681af)")
print(f"voice rows alone   -> {sha(tv)}  (the voice lab's e2e page: 50d4b2dfd385397e)")
assert sha(tp) == "b8d571f46a2681af" and sha(tv) == "50d4b2dfd385397e"
assert tp.encode("utf-8") == (S / "stage6-picture" / "au-final.html").read_bytes(), "not the picture lab's au-final.html"
vp, pv = apply(tv, fp, "voice+picture"), apply(tp, fv, "picture+voice")
assert vp == pv, "the two orders differ"
print(f"both sets, either order -> {sha(vp)} (identical)")

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
S6_NAMES = ("tickBenediction", "drawBenediction", "_beneGeom", "_beneWash", "_beneRing", "_beneMotes",
            "_beneRim", "beneFade", "beneAge", "beneOut", "beneIn", "beneLit", "beneSeen", "beneTagS",
            "beneTagB", "voiceIn", "aureole-enter", "aureole-close")
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
    if label.startswith("tickHalo:"):
        sim[label] = [ln.strip() for ln in ins.splitlines() if ln.strip()]
    for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
        print(f"   write  {label[:44]:44s} {mw.group(1)}.{mw.group(2)}")
    for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort)\(", ins):
        print(f"   mutate {label[:44]:44s} {mw.group(1)}.{mw.group(2)}(")
    for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
        print(f"   index  {label[:44]:44s} {mw.group(1)}[...]")
print("sim-path lines:", json.dumps(sim, indent=1))
SIM_WANT = {
    "tickHalo: the entry note": ['const voiceIn = Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R;',
                                 'if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });',
                                 'Z.voiceIn = voiceIn ? 1 : 0;'],
    "tickHalo: the heal chime": ['SFX.play("spark", { collect: true, n: f.stacks("blessing") });'],
    "tickHalo: the close": ['if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });'],
}
for k, v in SIM_WANT.items():
    got = [sim[lab] for lab in sim if lab.startswith(k)]
    assert got == [v], (k, got)
assert len(sim) == 3

if DRY:
    print("DRY: not writing the builder")
    sys.exit(0)

# ------------------------------------------------------------------ the builder
b = BUILDER.read_text(encoding="utf-8")
assert sha(b) == "c7641c026661b686", "the builder moved"
assert "\nS6 = [" not in b, "the builder already carries S6"
out = ["", "", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v82 §4's picture and sound; its §5 brief stage 4,",
       "# \"picture, voice, beam's field spec out\"), picked on measurements under",
       "# Rick's \"you pick i overrule\" by the picture lab (scratch, `au_rows.py`) and",
       "# `aureole_voice_lab.py` (v110 §5-§6). PRESENTATION ONLY: engine_ab over all",
       "# 38 relics, Aureole included, is the proof, and the probe's [9]-[10] read the",
       "# voices and the picture's hook inside the fight. The rows are byte-exact to",
       "# the labs' own files (voice 5a43210cd9d13019, 4 rows; picture",
       "# ed67bd6722cbbe2b, 9 rows); the picture rows alone reproduce the picture",
       "# lab's stamp (b8d571f46a2681af), the voice rows alone the voice lab's page",
       "# (50d4b2dfd385397e), and the two sets give the same bytes in either order",
       f"# ({sha(vp)}). No two rows share an anchor, so none is merged.",
       "#   THE VOICE: three arms -- the cast's swell, a foe's entry, the close --",
       "#   ADDED before the shared rune-crack fallback, which is re-emitted",
       "#   unchanged, last; three things on the sim path, all inside tickHalo,",
       "#   each around a line this build's stage 2 already wrote (the entry before",
       "#   the inside test, the heal chime after `T.bless += u.bless;`, the close",
       "#   before the window's own close line).",
       "#   THE PICTURE: `tickBenediction` in tickPresentation; the halo in the",
       "#   world pass under both balls (the ring, the wash, the motes, the foe's",
       "#   rim); the beam's art retired (the lit ground, the lance, the life",
       "#   entry) and the charge rune redrawn.",
       "# COMPOSITION: nine anchors are re-emitted; four are consumed, all",
       "# Aureole's own (the beam's two art branches, ULTSIG.aureole, and the life",
       "# map's narrowest token `aureole: 1.6, `, which leaves Consecration's entry",
       "# on the same line to its own build). The rows ride on four of stage 2's own",
       "# lines (the fields, the inside test, the blessing's count, the close) and on",
       "# shared lines every stage 6 of the batch uses as `after` / `before` anchors",
       "# (tickPresentation's first call, tickWinnow, the world pass's drawTree,",
       "# drawMotes, the rune-crack fallback).",
       "S6 = ["]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]"]
block = "\n".join(out)

READINGS_S6 = ''' 14. THE PICTURE READS THE WINDOW OFF `ultHalo && alive && !over` and keeps
     its own state on the fighter (`bene*`), never on `m.ultFx` (one slot,
     and the foe's cast takes it: open item 25). `tickBenediction` runs in
     `tickPresentation`, on the presentation clock, which runs through hit
     stops and after `over`. So the ring grows out of the ball over 0.3s at
     the cast and shrinks back into it over 0.3s at a clock close, a death or
     the verdict (`tickHalo` never runs once `over` is set, and a halo
     standing at the kill would otherwise stand through the verdict).
 15. INSIDE IS `tickHalo`'S OWN TEST AS IT RAN, found by watching `haloTally`
     rise: a step the window ticked (`frames` rose) is an inside step iff
     `inFrames` rose with it; through a hit stop the last answer holds, as
     the halo does. The ring brightens 0.4 -> 0.7 while a foe is inside (0.1s
     in, 0.25s out) -- the tell that the blessing is running -- and a foe
     inside wears a rim of the light. The tag rule (Corona's, Daybreak's,
     Zenith's, Canopy's): the first smite of each inside stretch tags SMITE
     on the foe with its count, the first blessing BLESSING on her with hers.
     So the ticker makes no call for the picture. The picture writes its
     `bene*` fields, the tags and `taught` only, and draws no rng
     (`shellHash` and the clocks place the motes).
 16. A RING, NOT A DISC: a 10-unit band at `haloR` read off the relic (so the
     ring is where the simulation's test is), a 0.04 wash inside it, motes
     drifting in along it; the WORLD pass, under both balls, source-over
     only -- nothing under `lighter` and nothing the bloom can see.
 17. THE VOICES ON THE SIM PATH ARE THREE THINGS INSIDE `tickHalo`, each a
     no-op headless that writes nothing the simulation reads: the ENTRY
     (the ticker's own inside test repeated into a const, `SFX.play` when it
     is true after a false tick of the same window, and the answer kept on
     the window's record as `voiceIn` -- a field born undefined with every
     cast and read by nothing but this row, so a foe already inside when the
     halo rises is no entry: the cast's swell has that moment); the HEAL,
     the existing spark collect, unchanged, once per blessing after
     `T.bless += u.bless;`, with the blessing she now carries (Zenith's call
     word for word); the CLOSE, before the window's own close line, on a
     close BY ITS CLOCK with both fighters alive. The cast's voice is
     fireUlt's own `SFX.play("ult", { w: f.w.id })`, which found no arm and
     fell through to rune-crack: the arms are ADDED before that shared
     fallback, which is re-emitted unchanged for the relics that still use
     it. The smite has no voice (none named).
 18. NO CLOSE VOICE ON A DEATH: a caster's death ends the fight and a close
     after the foe's death belongs to its kill flight, so both are left to
     the death voice (Tendril's, Canopy's, Zenith's and Lightkeeper's rule);
     a halo still up when the fight ends closes in the picture only.
 19. NO fx.js FIELD (§4's motes are drawn instead, 16). A SPECS field rides
     the one ultFx slot, fires once, at the cast, where Aureole stood -- and
     the ring rides her for 8s: the slot is hers a median 0.68s of the
     window (7.9%), the opponent's cast took it in 16 of 113 windows, and
     after the first second she stands a median 214 units from the spawn
     point (the picture lab's fxprobe). This builder edits neither fx.js
     copy, and stage 6 refuses if its edits touched the inlined one. The
     beam's `SPECS.aureole` (mode 'beam') is the retired ultimate's: the
     orchestrator takes it out of both copies at the carry
     (`fx_remove.py --relic aureole`). Rick's to overrule.
 20. THE BEAM'S ART IS RETIRED WITH THE BEAM: drawUltUnder's lit ground and
     drawUltOver's lance and rings (both drawn at every cast from the ultFx
     record), and the life map's `aureole: 1.6` (the cast's record falls to
     the map's own 1.5, and nothing draws from it). The charge rune,
     ULTSIG.aureole, is redrawn: the halo round the ball, the monstrance's
     six rays and motes drifting in, brightening as the charge fills. The
     four are replaced, not re-emitted: every other anchor is.
'''

HELPERS = '''


# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `bene*` fields, the entry's `voiceIn` on the
# window's record (reading 17), a tag's `taught`, the canvas and the synth's
# own nodes. Everything else is the simulation's.
S6_NAMES = ("tickBenediction", "drawBenediction", "_beneGeom", "_beneWash", "_beneRing", "_beneMotes",
            "_beneRim", "beneFade", "beneAge", "beneOut", "beneIn", "beneLit", "beneSeen", "beneTagS",
            "beneTagB", "voiceIn", "aureole-enter", "aureole-close")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("bene") or obj == "c"
               or (obj, prop) in {("Z", "voiceIn"), ("taught", "smite"), ("taught", "blessing"),
                                  ("frequency", "value")})
# THE THREE THINGS ON THE SIM PATH, whole (reading 17): each row's added
# code, comments stripped, line for line.
S6_SIM_LINES = {
    "tickHalo: the entry note": ['const voiceIn = Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R;',
                                 'if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });',
                                 'Z.voiceIn = voiceIn ? 1 : 0;'],
    "tickHalo: the heal chime": ['SFX.play("spark", { collect: true, n: f.stacks("blessing") });'],
    "tickHalo: the close": ['if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });'],
}
S6_SFX_ROW = "Sfx: Aureole's cast"
S6_TICK_ROW = "benediction picture: tickBenediction"
RUNE_CRACK = "        } else {                                        // rune-crack"
INSIDE_TEST = "      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;"


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 19)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_array_ok(obj: str, ins: str) -> bool:
    """An array stage 6 may change: its own `bene*` ones, or a name its row
    binds once, as `const X = f.bene...;` (tickBenediction's S)."""
    if obj.startswith("bene"):
        return True
    bound = re.findall(r"\\bconst " + re.escape(obj) + r" = \\w+\\.(bene\\w+);", ins)
    decls = re.findall(r"\\b(?:const|let|var)\\s+" + re.escape(obj) + r"\\b|[,(]\\s*" + re.escape(obj)
                       + r"\\s*=(?!=)|(?<![\\w.$])" + re.escape(obj) + r"\\s*=(?!=)", ins)
    return len(bound) == 1 and len(decls) == 1


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, beats, floats or knocks, never
    writes the shared weapon row, writes only what S6_WRITE_OK names and
    mutates only its own arrays. Its lines on the sim path are the three
    voice rows, whole, each in its own row; the synth's nodes only in the
    Sfx row; the tags and `taught` only in tickBenediction. The probe's
    [9]-[10] and engine_ab are the dynamic proof. Run on every stage: it
    reads the table."""
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickHalo|tickStatus|tickWeapon|tickFire|tickHits|spawnShot|note|checkEnd)\\(", ins) \\
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
                                 f"('{label}') is not its voice alone:\\n{ins}")
        elif "SFX" in ins or "voiceIn" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the entry, the heal and the close")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickBenediction")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\\(", ins):
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
    shared rune-crack fallback kept once and after Aureole's arms, the beam's
    art gone, the entry's test the ticker's own and just before it, and every
    arm, call and pass wired exactly once."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 19)")
    arms = ['} else if (w === "aureole"){', '} else if (w === "aureole-enter"){',
            '} else if (w === "aureole-close"){']
    if s.count(RUNE_CRACK) != 1 or any(not 0 <= s.find(a) < s.find(RUNE_CRACK) for a in arms):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Aureole's arms")
    for gone in ('u.w === "aureole"', "aureole: 1.6"):
        if gone in out_code:
            raise SystemExit(f"REFUSING TO WRITE -- the beam's art is still drawn ({gone!r})")
    for need in ["this.tickBenediction(dt);", "if (__world) this.drawBenediction(m);",
                 "  tickBenediction(dt){", "  drawBenediction(m){", "  aureole(c, t, cf, P){",
                 INSIDE_TEST.strip()] + arms:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        for ln in (x for x in v if "SFX.play(" in x):
            if out_code.count(ln) != code.count(ln) + 1:
                raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    # the entry's test is the ticker's own, repeated just before it, in tickHalo
    th = out_code[out_code.find("  tickHalo(dt){"):]
    th = th[:th.find("\\n  }\\n")]
    i_v = th.find(S6_SIM_LINES["tickHalo: the entry note"][0])
    i_t = th.find(INSIDE_TEST.strip())
    if not 0 <= i_v < i_t or th[i_v:i_t].count("\\n") != 3:
        raise SystemExit("REFUSING TO WRITE -- the entry's test is not the ticker's own, "
                         "repeated just before it in tickHalo")
    if "  tickPresentation(dt){\\n    this.tickNovaFx(dt);\\n    this.tickBenediction(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickBenediction does not follow tickNovaFx in "
                         "tickPresentation")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the entry, the heal chime and the close its three lines on the sim "
          "path); the inlined fx.js untouched; the rune-crack fallback kept; the beam's art "
          "gone; every arm, call and pass once")'''

reps = [
 # the docstring: the stage table
 ("                                          -> sc-aureole-b12.5.html        THE FINAL LINK\n",
  "                                          -> sc-aureole-b12.5.html        (stage 6 goes on it)\n"),
 ("                                          -> sc-aureole-b11.5.html        (not the carry)\n",
  "                                          -> sc-aureole-b11.5.html        (not the carry)\n"
  "    stage 6   the picture and the voice (brief stage 4), on stage 5's link\n"
  "                                          -> sc-aureole-b12.5-fx.html     THE FINAL LINK\n"
  "              presentation only; no fx.js field (reading 19): the beam's\n"
  "              SPECS.aureole is the orchestrator's `fx_remove.py` at the carry\n"),
 # the docstring: reading 13's tail, and stage 6's readings after it
 ("     out\"), not this builder's stages 1-5: they still play at the cast until\n"
  "     then, and nothing in the simulation reads any of them.\n",
  "     out\"), not this builder's stages 1-5, which leave them playing at the\n"
  "     cast; stage 6 (readings 14-20) retires the picture and voices the halo,\n"
  "     and the field spec is the orchestrator's to take out (reading 19).\n"
  "     Nothing in the simulation reads any of them.\n"
  "\n"
  "STAGE 6, THE PICTURE AND THE VOICE (§4's picture and sound; the brief's stage\n"
  "4, \"picture, voice, beam's field spec out\"). Picked on measurements under\n"
  "Rick's \"you pick i overrule\" by the picture lab (scratch) and\n"
  "`aureole_voice_lab.py` (v110 §5-§6); the rows are the labs', byte-exact.\n"
  "Declared:\n" + READINGS_S6),
 # the tables and the helpers, after S5
 ("\nS5 = s5_edits(BLADE)\n",
  "\nS5 = s5_edits(BLADE)\n" + block + HELPERS + "\n"),
 ('''STAGE_OUT = {"1": "sc-aureole-stub", "2": "sc-aureole-halo", "3": "sc-aureole-bless",
             "5": "sc-aureole-b12.5", "5 --alt50": "sc-aureole-b11.5"}''',
  '''STAGE_OUT = {"1": "sc-aureole-stub", "2": "sc-aureole-halo", "3": "sc-aureole-bless",
             "5": "sc-aureole-b12.5", "5 --alt50": "sc-aureole-b11.5", "6": "sc-aureole-b12.5-fx"}'''),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''            edits, want = S3, ult_block(ULT["charge"], ULT["bless"])
        else:
''',
  '''            edits, want = S3, ult_block(ULT["charge"], ULT["bless"])
        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: the blessing on, the blade BLADE
            # names (never Rick's 50% link), the halo's ticker, none of stage
            # 6's names in the source yet (on identifier boundaries), and what
            # the picture and the voice read there.
            if (f'bless:{ULT["bless"]},' not in row or f"dmg:{BLADE}," not in row
                    or free_name("tickHalo", code) or INSIDE_TEST.strip() not in code):
                raise SystemExit("stage 6 goes on stage 5 (the blessing on, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if '} else if (w === "aureole"){' in code:
                raise SystemExit("Aureole's cast voice is already in this source -- stage 6 goes on once")
            for need, why in (("function shellHash(", "no shellHash (the motes' hash, never the RNG)"),
                              ("function hexA(", "no hexA (the band's falloff and the foe's rim)"),
                              ("  statusTag(x, y, key, first, val){", "no statusTag (the tags)"),
                              ("  spokes(c, n, r0, r1, phase, col, w, al){", "no SG.spokes (the rune's rays)"),
                              ('SFX.play("ult", { w: f.w.id });', "fireUlt no longer voices the cast by id"),
                              ('SFX.play("spark", { collect: true, n: f.stacks("blessing") });',
                               "no spark collect voice to reuse")):
                if need not in code:
                    raise SystemExit(f"wrong base for stage 6: {why}")
            blade = BLADE
            edits, want = S6, ult_block(ULT["charge"], ULT["bless"])
        else:
'''),
 ('''    for label, _old, new in S1 + S2 + S3 + S5 + s5_edits(ALT50_BLADE):
''',
  '''    for label, _old, new in S1 + S2 + S3 + S5 + s5_edits(ALT50_BLADE) + S6:
'''),
 ('''    if len(re.findall(r'kind:"halo"', out_code)) != 1:
''',
  '''    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    if len(re.findall(r'kind:"halo"', out_code)) != 1:
'''),
]
for a_, b_ in reps:
    assert b.count(a_) == 1, a_[:80]
    b = b.replace(a_, b_, 1)
BUILDER.write_text(b, encoding="utf-8", newline="\n")
print(f"stage 6 written into {BUILDER.name}: {len(edits)} edits; builder now {sha(b)}")
(S / "s6" / "fx_expected.sha").write_text(sha(vp) + "\n")
