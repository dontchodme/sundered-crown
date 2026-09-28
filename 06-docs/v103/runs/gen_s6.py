"""Write Coldiron / Temper's stage 6 into tools/coldiron_build.py from the labs' byte-exact row files.

Ironwood's and Bindweed's gen_s6 pattern: verify the rows the labs returned equal their files, check
the picture rows alone reproduce the picture lab's stamp, assert no row's anchor sits inside
another's, MERGE rows that share an anchor into one edit, write an S6 list into the builder with
triple-quoted strings, and wire a --stage 6 that refuses to run twice and scans S6 (no ultFx, no RNG,
no call into the simulation, writes only presentation fields). Refuses to run on a builder that
already has S6.

THE RETURNED ROWS. The labs' reports reached this session relayed inline in the task text, cut off
mid-row (no report file on disk). What was relayed whole is checked here to the character: the
labels, anchors and modes of the relayed rows (voice row 1, picture rows 1-3). The files are then
tied to the labs' own outputs: the voice rows' anchor/mode/code equal the lab's own
`rows_lab.json` (which its confirmation run `rows_lab3.json` reproduces byte for byte), and the
picture file's sha is the one the picture lab recorded (2c035026c727a316), whose rows alone
reproduce its stamp on b93.
"""
import json, pathlib, hashlib, re, sys

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron")
REPO = pathlib.Path("C:/dev/sundered-crown")
STAMP = "94bb7580047f01bc"          # the picture lab's ci-final.html: picture rows alone on b93
PIC_FILE_SHA = "2c035026c727a316"   # the picture lab's STATE.md: rows_final.json
BASE_SHA = "324b42d5b36fac98"       # sc-coldiron-temper-b93.html

sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
fv_p, fp_p = S / "stage6-voice/rows_final.json", S / "stage6-picture/rows_final.json"
assert sha(fp_p.read_bytes()) == PIC_FILE_SHA, "the picture rows file is not the one the lab recorded"
fv = json.loads(fv_p.read_text(encoding="utf-8"))
fp = json.loads(fp_p.read_text(encoding="utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
assert len(fv) == 3 and len(fp) == 11, (len(fv), len(fp))

lab = json.loads((S / "stage6-voice/rows_lab.json").read_text(encoding="utf-8"))
lab3 = (S / "stage6-voice/rows_lab3.json").read_bytes()
assert lab3 == (S / "stage6-voice/rows_lab.json").read_bytes(), "the voice lab's confirmation run differs"
lab = lab["rows"] if isinstance(lab, dict) else lab
assert len(lab) == 3
for a, b in zip(lab, fv):
    assert all(a[k] == b[k] for k in ("label", "anchor", "mode", "code")), a["label"]

# What the relayed reports carried whole (label, anchor, mode), to the character.
RELAYED = [
    (fv[0], "Sfx: Coldiron's cast, anvil and close arms, before the shared rune-crack fallback",
     "        } else {                                        // rune-crack", "replace"),
    (fp[0], "temper picture: fighter fields", "    this.temperTally = null;\n", "after"),
    (fp[1], "temper picture: the presentation call", "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n", "after"),
    (fp[2], "temper picture: tickIron", "  tickWinnow(dt){\n", "before"),
]
for r, label, anchor, mode in RELAYED:
    assert (r["label"], r["anchor"], r["mode"]) == (label, anchor, mode), label
# ... and a line of each relayed code body, verbatim from the relay.
assert '          this._sweep(t, { f0: 7500, f1: 5000, q: 2.5, gain: g, dur: 0.32, atk: 0.012 });\n' in fv[0]["code"]
assert "    this.ironSparks = [];\n" in fp[0]["code"]
assert fp[1]["code"] == "    this.tickIron(dt);                  // TEMPER'S PICTURE (v73 section 6.1)\n"
assert "      const Z = (this.over || !f.alive) ? null : f.ultTemper;\n" in fp[2]["code"]
print("the returned rows equal the files: voice 3/3 (== the lab's rows_lab.json, reproduced by its "
      "confirmation run), picture 11/11 (the lab's recorded file); the relayed rows' labels, anchors, "
      "modes and a line of each body match")

base_p = S / "links/sc-coldiron-temper-b93.html"
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
# A replace row must re-emit its anchor (then it composes) or be a true replacement of text no
# other relic anchors on; either way the old text is exactly once in the base.
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
      f"{len(edits) - reemit} replace text outright)")

p = REPO / "tools/coldiron_build.py"
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "\nS6 = [" in s:
    raise SystemExit("the builder already has S6 -- not writing it twice")
assert sha(s.encode()) == "155eec593ce9e6c2", "the builder is not the one this generator was written for"

out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v73 §6.1-6.2, brief §2 stage 6), picked on",
       "# measurements under Rick's \"you pick i overrule\" by `coldiron_voice_lab.py`",
       "# and the picture lab (v103 §7). Presentation only: engine_ab over all 39",
       "# relics, Coldiron included, is the proof. The rows are byte-exact to the",
       "# labs' own files (voice 3, picture 11; no two share an anchor, so none is",
       "# merged); the picture rows alone reproduce the picture lab's stamp",
       f"# ({STAMP}) on sc-coldiron-temper-b93. Voice first, then picture; the",
       "# other order writes the same bytes.",
       "#   THE VOICE: the cast (fireUlt's own `ult`/coldiron call, which fell",
       "#   through to rune-crack: the quench), the anvil on every won bind (inside",
       "#   resolveClank's iron clause, after the loser's sunder, pitched by the",
       "#   loser's count), and the close (a clock close with both alive; never on",
       "#   a death, never after `over`). Plain SFX.play; nothing is read back.",
       "#   THE PICTURE: `tickIron` in tickPresentation reads `ultTemper && !over`,",
       "#   `temperTally.won` rising and the clank's own beat, and writes only its",
       "#   own `iron*` fields, a tag's count and colour, and `taught`. The blades",
       "#   quench, hold black iron 1.4x wide and cool back to steel; a won bind",
       "#   rings the anvil ring and throws forge sparks; sunder past 6 prints and",
       "#   spalls in the forge's glow; `_tbBuilt` (the dwarven twinblade, which",
       "#   only Coldiron draws) becomes two riveted cleavers. No beat, no stop.",
       "#   No fx.js field: the forge sparks are drawn (v103 §7, Rick's to overrule).",
       "#   NAMES: the labs'. `tickIron` is a prefix of the staff row's",
       "#   `tickIronfall` (not on this tip; the tickVine / tickVines trap), so",
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
# (`tickIron` is a prefix of the staff row's `tickIronfall`).
S6_NAMES = ("tickIron", "drawIronWeapon", "drawIronTop", "ironPalette", "_ironPal",
            "_stSunderPast", "ironFade", "ironRings", "ironSparks", '"coldiron-anvil"',
            '"coldiron-close"', 'w === "coldiron"')
# What stage 6's ADDED code may write: its own iron* fields (any object), the
# canvas, a tag's count and colour, a record's clock, `taught`, and an
# oscillator's pitch.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("iron") or obj == "c" or prop == "val"
               or (obj, prop) == ("g", "c") or (prop == "t" and obj.endswith("]"))
               or obj == "taught" or (obj, prop) == ("frequency", "value"))


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)

'''

reps = [
 ("THE BASE is asserted by CONTENT (the sites and features this builder needs),\n",
  """STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
and sound are Code's picks under "you pick i overrule"; v103 §7):
  8. THE ANVIL CARRIES THE LOSER'S COUNT after the bind's sunder, the one its
     tag shows (2..9 at bind 2, cap 9) -- a Twinshade shade's when a shade
     loses the bind; a won bind at the cap (9 -> 9) still strikes, at 9's note.
  9. THE CLOSE VOICE IS THE CLOCK CLOSE'S (both alive): a death close (a kill
     flight) and a window still set at `over` play nothing and are left to the
     death voice (Zenith's, Canopy's and Onslaught's rule). The picture reads
     `ultTemper && !over` (reading 4), so the blades cool at the verdict.
 10. "THE SUNDER TAG ON THE FOE TICKING UP": a won bind prints the loser's
     count on its rim toward the bind, one sunder tag on the foe at a time (a
     tag already up takes the new count in place); the blade's own sunder tag
     carries its count while the foe's ceiling is raised (Bloodletting's rule
     one status along). Past 6 it prints in dwarven's glow, and the ball shows
     the flakes past 6, hot.
 11. "FORGE SPARKS OFF THE BLADES" ARE DRAWN, not an fx.js field: a field rides
     the one ultFx slot, which Coldiron holds for a median 0.65s of its 8s
     window, and it fires once, at the cast; 31 of 427 won binds came while the
     slot was still Coldiron's.
 12. THE SILHOUETTE: `_tbBuilt`, the dwarven twinblade route that only Coldiron
     draws, becomes two riveted cleavers (the rivets on the outline, open item
     34's rule); the window draws the same shape 1.4x wide in its iron palette.

THE BASE is asserted by CONTENT (the sites and features this builder needs),
"""),
 ('    stage 6   picture, voice, field       (not written yet)\n',
  '    stage 6   picture, voice              -> sc-coldiron-temper-fx.html (no field: forge sparks drawn, v103 §7)\n'),
 ('\n\ndef stage_out(stage: str) -> str:\n    return {"1": "sc-coldiron", "2": "sc-coldiron-mass", "3": "sc-coldiron-bind",\n'
  '            "4": "sc-coldiron-temper",\n'
  '            "5": f"sc-coldiron-temper-b{str(BLADE).replace(\'.\', \'\')}"}[stage]\n',
  block + tail +
  '\ndef stage_out(stage: str) -> str:\n    return {"1": "sc-coldiron", "2": "sc-coldiron-mass", "3": "sc-coldiron-bind",\n'
  '            "4": "sc-coldiron-temper",\n'
  '            "5": f"sc-coldiron-temper-b{str(BLADE).replace(\'.\', \'\')}",\n'
  '            "6": "sc-coldiron-temper-fx"}[stage]\n'),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "4", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "4", "5", "6"], required=True)'),
 ('''        else:
            if f'cap:{ULT["cap"]},' not in relic_ult(code) or "dmg:11.95," not in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 4, once")
''',
  '''        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: Coldiron's ult block is stage 5's to
            # the character and its blade is stage 5's; none of stage 6's names
            # is in the source yet (on identifier boundaries).
            want = ult_block(ULT["charge"], ULT["bind"], ULT["cap"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{BLADE}," not in relic_row(code, RELIC)):
                raise SystemExit("stage 6 goes on stage 5: Coldiron's ult block or blade is not stage 5's")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            edits = S6
        else:
            if f'cap:{ULT["cap"]},' not in relic_ult(code) or "dmg:11.95," not in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 4, once")
'''),
 ('''    for label, _old, new in S1 + S2 + S3 + S4 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:''',
  '''    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or shatters, and writes only
    # what S6_WRITE_OK names. It READS the window, the tally and the clank's
    # beat; the probe's [8]-[9] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
    for label, _old, new in S1 + S2 + S3 + S4 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("stage 6 written into", p.name, ":", len(edits), "edits;", "sha", sha(s.encode()))
(S / "s6/expected_fx_sha.txt").write_text(full_sha + "\n")
