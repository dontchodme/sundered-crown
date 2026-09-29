"""Write Widowmaker's stage 6 into tools/widowmaker_build.py from the labs' byte-exact row files.

ironwood's gen_s6.py shape (build/iw6), plus: rows that share an anchor are MERGED into one edit, the
voice rows alone and the picture rows alone each reproduce their lab's own page, and both orders of the
two sets give the same bytes. Run once; it refuses if the builder already carries S6.
"""
import hashlib, json, pathlib, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
BASE = S / "links" / "sc-widowmaker-b1075.html"
FV, FP = S / "stage6-voice" / "rows_final.json", S / "stage6-picture" / "rows_final.json"
BUILDER = pathlib.Path("C:/dev/sundered-crown/tools/widowmaker_build.py")
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()[:16]


def load(p):
    r = json.loads(p.read_text(encoding="utf-8"))
    return r["rows"] if isinstance(r, dict) else r


print(f"voice rows   {FV.name} {sha(FV.read_bytes())}")
print(f"picture rows {FP.name} {sha(FP.read_bytes())}")
assert sha(FV.read_bytes()) == "ff78068cbe2fa1f2" and sha(FP.read_bytes()) == "42121c10265e101c", "a row file moved"
fv, fp = load(FV), load(FP)
assert len(fv) == 2 and len(fp) == 10
for r in fv + fp:
    assert r["mode"] in ("before", "after", "replace"), r["label"]
    for k in ("label", "anchor", "code"):
        assert "'''" not in r[k] and "\\" not in r[k] and "\r" not in r[k], (r["label"], k)

g = BASE.read_text(encoding="utf-8")
assert sha(g) == "a9977a757d5772b7", "the base moved"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows, tag):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (tag, r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


tp = apply(g, fp, "picture")
tv = apply(g, fv, "voice")
print(f"picture rows alone -> {sha(tp)}  (the picture lab's stamp: 518477d4537ec077)")
print(f"voice rows alone   -> {sha(tv)}  (the voice lab's page:  373f16b7e0a85770)")
assert sha(tp) == "518477d4537ec077" and sha(tv) == "373f16b7e0a85770"
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

# ------------------------------------------------------------------ the builder
b = BUILDER.read_text(encoding="utf-8")
assert "\nS6 = [" not in b, "the builder already carries S6"
out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v76 §4; the design's stage 3), picked on",
       "# measurements under Rick's \"you pick i overrule\" by the picture lab and",
       "# `widowmaker_voice_lab.py` (v106 §5). PRESENTATION ONLY: engine_ab over all",
       "# 38 relics, Widowmaker included, is the proof, and the probe's [11]-[12] read",
       "# the voices and the picture's hook inside the fight. The rows are byte-exact",
       "# to the labs' own files (voice ff78068cbe2fa1f2, 2 rows; picture",
       "# 42121c10265e101c, 10 rows); the picture rows alone reproduce the picture",
       "# lab's stamp (518477d4537ec077), the voice rows alone the voice lab's page",
       "# (373f16b7e0a85770), and the two sets give the same bytes in either order.",
       "#   THE VOICE: the cast's inhale REPLACES the nova's \"wet slice\" arm in place",
       "#   (the shared rune-crack fallback is not touched); the drain's reversed drip",
       "#   is the one call stage 6 puts on the sim path -- tickStatus's drain block,",
       "#   once per whole hp drained, n = the bleeding foe's hemorrhage stacks. The",
       "#   close plays nothing.",
       "#   THE PICTURE: `tickSiphon` in tickPresentation reads `drainTally` rising",
       "#   (casts: the flush; drained: the \"+n\") and `ultDrain && !over` (the",
       "#   thread; the snap at the close), and writes only its own `siphon*` fields",
       "#   and `floats`. The thread is drawn in the world pass under both balls, the",
       "#   flush over them. The nova's art is retired: drawUltOver's fang burst, the",
       "#   banner's fan and drops (the word fills) and its spread entry; the ultFx",
       "#   `life` entry keeps its number (the cast's record). No fx.js edit:",
       "#   `SPECS.widowmaker` leaves BOTH copies at the carry by `tools/fx_remove.py`",
       "#   (reading 16).",
       "S6 = ["]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

reps = [
 # the docstring: the stage table
 ('    stage 6   picture, voice, carry     (the design\'s stage 3; not written yet)\n',
  '    stage 6   picture and voice         -> sc-widowmaker-b1075-fx.html\n'
  '              the design\'s stage 3, on the final (stage 5\'s link). The carry is\n'
  '              the orchestrator\'s: stages 1, 2, 5 and 6, then SPECS.widowmaker out\n'
  '              of both fx.js copies by tools/fx_remove.py (reading 16), not here.\n'),
 # the docstring: stage 6's readings, after reading 11
 ('''  11. THE BLADE HOLDS THE SHIPPED WIN RATE (§3, §5 stage 2): the stage-5
     comment at TUNED below says how it was measured and what the band's 50
     would take instead (Rick's §6.2).
''',
  '''  11. THE BLADE HOLDS THE SHIPPED WIN RATE (§3, §5 stage 2): the stage-5
     comment at TUNED below says how it was measured and what the band's 50
     would take instead (Rick's §6.2).

STAGE 6, THE PICTURE AND THE VOICE (the design's stage 3; v76 §4: "her shell
flushes dark red for 0.25s and a thin red thread appears from the foe's bleed
drips to her shell for as long as the foe bleeds inside the window ... a red
'+n' floats on her every 1 hp drained ... Close: the thread snaps. No new
object"; the voice "cast -- a low inhale, 0.4s", "the drain -- the bleed's own
drip voice reversed and pitched by the foe's stack count, quiet"). Picked on
measurements under Rick's "you pick i overrule" (v106 §5); the rows are the
labs', byte-exact. Declared:
  12. THE "+n" IS FILED IN `tickPresentation` (`tickSiphon`), NEVER IN
      `tickStatus`: "the drain files none" (§5), and the probe's [7] holds a
      drain tick to no float. One "+n" each time her drained total crosses a
      whole hp (hurt()'s rule: no float for a fraction).
  13. THE PICTURE FINDS THE CAST AND THE DRAIN BY WATCHING `drainTally` RISE
      (`casts`, `drained`), so neither `fireUlt` nor `tickStatus` makes a call
      for it. The one stage-6 call on the sim path is the drip VOICE, in
      tickStatus's drain block: once per whole hp crossed, n = the bleeding
      foe's hemorrhage stacks (a read). SFX.play draws nothing, writes nothing
      the simulation reads and returns on its first line with no audio context.
  14. THE THREAD IS READ OFF `ultDrain && !over`, both standing and the foe
      bleeding: about one window in eight is still set at `over` (reading 5),
      so the thread snaps at the verdict instead of hanging on the corpse.
  15. THE CLOSE HAS NO VOICE (v76 §4). Its picture is the snap -- on the
      clock, a death or the verdict alike.
  16. THE NOVA'S ART IS RETIRED (reading 8): drawUltOver's fang burst; the
      "wet slice" (its three lines replaced IN PLACE by the inhale, so the
      shared rune-crack fallback is untouched); the banner's fan and drops (the
      word now fills from the foot) and its spread entry. The ultFx `life`
      entry keeps its number, annotated as the cast's record (Daybreak's and
      Corollary's precedent). `SPECS.widowmaker`, the nova's particle field,
      is the one piece left: it leaves BOTH copies of fx.js at the carry, by
      the orchestrator's `tools/fx_remove.py` (fx.js is shared), and this
      builder edits neither -- stage 6 refuses if the inlined copy moved.
      `ULTSIG.widowmaker`, the charge sigil ("a drop, and a ring drawn INTO
      it"), is not named by the design and is kept.
'''),
 ('\nSTAGE_OUT = {"1": "sc-widowmaker-stub", "2": "sc-widowmaker-drain", "5": "sc-widowmaker-b1075"}\n',
  block + '\nSTAGE_OUT = {"1": "sc-widowmaker-stub", "2": "sc-widowmaker-drain", "5": "sc-widowmaker-b1075",\n'
          '             "6": "sc-widowmaker-b1075-fx"}\n'
          '''
# STAGE 6'S NAMES, free on the base on identifier boundaries (`drawSiphon` is a
# prefix of `drawSiphonTop`), and what its inserts may write: their own
# `siphon*` fields, the snap's clock, the canvas and the synth's own nodes, and
# the banner's local widths. Everything else is the simulation's.
S6_NAMES = ("tickSiphon", "drawSiphon", "drawSiphonTop", "_siphonPath", "_siphonAt", "_siphonCord",
            "_siphonThread", "_siphonBeads", "_siphonSnap", "siphonFade", "siphonAge", "siphonSeen",
            "siphonHp", "siphonSide", "siphonSnap", "widowmaker-drain")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("siphon") or (obj, prop) in {("siphonSnap", "t"),
                                                                             ("frequency", "value")}
               or obj == "c")
S6_ARRAY_OK = (lambda obj: obj == "ws")
S6_DRIP = 'SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") });'


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies, tools/fx_remove.py)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]
'''),
 ('    ap.add_argument("--stage", choices=["1", "2", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "5", "6"], required=True)'),
 # the base check: at stage 6 the row carries the tuned blade
 ('''    if SHIP_HEAD not in s0:
        raise SystemExit("wrong base: Widowmaker's shipped row (twinblade, 11.95, "
                         "hemorrhage 2) has moved")''',
  '''    head = SHIP_HEAD if A.stage != "6" else SHIP_HEAD.replace("dmg:11.95,", f"dmg:{TUNED['dmg']},")
    if head not in s0:
        raise SystemExit("wrong base: Widowmaker's row (twinblade, "
                         + ("11.95" if A.stage != "6" else f"stage 5's {TUNED['dmg']}")
                         + ", hemorrhage 2) has moved")'''),
 ('''    else:
        if f'charge:{ULT["charge"]}, kind:"drain"' not in code or "tickDrain(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want = S5, ult_block(ULT["charge"])''',
  '''    elif A.stage == "5":
        if f'charge:{ULT["charge"]}, kind:"drain"' not in code or "tickDrain(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want = S5, ult_block(ULT["charge"])
    else:
        # STAGE 6 GOES ON STAGE 5, ONCE: the drain at its charge, the blade
        # TUNED names, none of stage 6's names in the source yet (on identifier
        # boundaries), and the picture's hash function there to read.
        if (f'charge:{ULT["charge"]}, kind:"drain"' not in code or "tickDrain(dt){" not in code
                or f'dmg:{TUNED["dmg"]},' not in relic_row(code, RELIC)):
            raise SystemExit("stage 6 goes on stage 5 (the drain, at the blade TUNED names)")
        for name in S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
        if "function shellHash(" not in code:
            raise SystemExit("wrong base: no shellHash (the picture's hash, never the RNG)")
        edits, want = S6, ult_block(ULT["charge"])'''),
 # stage 6's own refusals, before the S1+S2+S5 loop
 ('''    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
''',
  '''    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor aside)
    # draws no RNG, never takes the one ultFx slot (open item 25), calls
    # nothing that hurts, applies, resolves, beats or knocks, writes only what
    # S6_WRITE_OK names and mutates only the banner's local widths. The drip
    # voice is its one line on the sim path and the "+n" float its one match
    # write (the picture's presentation list), each in its own row only. The
    # probe's [11]-[12] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickDrain|tickStatus|spawnShot|note)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if "float(" in ins and label != "exsanguinate picture: tickSiphon":
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' floats a "
                             "number outside tickSiphon (the drain files none)")
        if label.startswith("tickStatus"):
            if [ln.strip() for ln in ins.splitlines() if ln.strip()] != [
                    "const k0 = Math.floor(me.drainTally.drained);",
                    "if (Math.floor(me.drainTally.drained) > k0)", S6_DRIP]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"is not the drip voice alone:\\n{ins}")
        elif "SFX" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside tickStatus's drain block")
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
                             "(SPECS.widowmaker is the orchestrator's fx_remove)")
        for gone, why in (('u.w === "widowmaker"', "the nova's fang burst on the ultFx slot"),
                          ("freq: 3400, q: 1.6, gain: 0.34, dur: 0.20", "the nova's wet slice"),
                          ("widowmaker: 52,", "the banner's spread for the nova's fan")):
            if gone in out_code:
                raise SystemExit(f"REFUSING TO WRITE -- {why} is still here")
        for need, n in ((S6_DRIP, 1), ("this.tickSiphon(dt);", 1), ("this.drawSiphon(m);", 1),
                        ("this.drawSiphonTop(m);", 1), ('} else if (w === "widowmaker"){', 1),
                        ('} else if (w === "widowmaker-drain"){', 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields; the drip voice its one line on the sim path, the \\"+n\\" "
              "filed in tickSiphon); the inlined fx.js untouched; the nova's burst, slice, "
              "fan and spread out; the inhale, the drip, the thread, the flush wired once each")
'''),
]
for a_, b_ in reps:
    assert b.count(a_) == 1, a_[:80]
    b = b.replace(a_, b_, 1)
BUILDER.write_text(b, encoding="utf-8", newline="\n")
print(f"stage 6 written into {BUILDER.name}: {len(edits)} edits; builder now {sha(b)}")
