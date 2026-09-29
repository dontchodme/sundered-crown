"""Write Oracle's stage 6 into tools/oracle_build.py from the labs' byte-exact row files.

    python gen_s6.py            # check only (prints what it would write)
    python gen_s6.py --write    # patch the builder

ironwood's gen_s6.py pattern: the rows are the labs' files verbatim; the returned
rows (the task's quoted text) are checked against the files; the picture rows alone
must reproduce the picture lab's stamp and the voice rows alone the voice lab's; no
row's anchor may sit inside another's; rows that share an anchor LINE are merged
into one edit; the S6 list is written with triple-quoted strings; --stage 6 refuses
to run twice and scans S6 (ultFx, rng, calls into the sim, writes).
"""
import json, pathlib, hashlib, sys, random

B = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/oracle")
WRITE = "--write" in sys.argv
fv_raw = (B / "stage6-voice/rows_final.json").read_bytes()
fp_raw = (B / "stage6-picture/rows_final.json").read_bytes()
print("voice rows  ", hashlib.sha256(fv_raw).hexdigest()[:16], len(fv_raw), "bytes")
print("picture rows", hashlib.sha256(fp_raw).hexdigest()[:16], len(fp_raw), "bytes (picture lab: 72e885b17b2e193e)")
assert hashlib.sha256(fp_raw).hexdigest()[:16] == "72e885b17b2e193e"
assert hashlib.sha256(fv_raw).hexdigest()[:16] == "4f3e2656c44f9237"      # v_order_final.txt's
fv = json.loads(fv_raw.decode("utf-8"))
fp = json.loads(fp_raw.decode("utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
assert len(fv) == 4 and len(fp) == 7

# THE RETURNED ROWS (the task's quoted text of each lab's report) against the files
Q_V0 = ("Sfx: Oracle's cast, sigil, snap and close arms, before the shared rune-crack fallback",
        "        } else {                                        // rune-crack", "before",
        '        } else if (w === "oracle"){                     // the rune-eye opens\n'
        "          /* ORACLE'S CAST, THE EYE OPENING -- v75 \u00a76.2: \"cast: a rune-eye\n"
        "             'open' -- a filtered inhale into a soft chime, 0.4s\". SIGIL, of 5,\n")
assert (fv[0]["label"], fv[0]["anchor"], fv[0]["mode"]) == Q_V0[:3] and fv[0]["code"].startswith(Q_V0[3]), "voice row 0"
assert "          const g = 0.09833;\n          this._sweep(t, { f0: 660, f1: 6652.4, q: 1.2, gain: g * 2.124, dur: 0.55, atk: 0.33, type:\"bandpass\" });\n" in fv[0]["code"]
assert "          this._tone(t, { freq: 2640, gain: 0.001924, dur: 0.3, type:\"sine\" }).frequency.value = 2640;\n" in fv[0]["code"]
assert "          this._tone(t, { freq: 3100 * k, to: 2500 * k, gain: 0.138, dur: 0.045, type:\"triangle\" });\n" in fv[0]["code"]
assert "apart, ending where the chime began, cut there. ENV-CORR 0.92 with\n             the chime's own samples" in fv[0]["code"]
Q_P = [("foresight picture: fighter fields", "    this.ultSight = null;\n    this.sightTally = null;\n", "after"),
       ("foresight picture: the presentation call", "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n", "after"),
       ("foresight picture: tickForesight", "  tickWinnow(dt){\n", "before"),
       ("foresight picture: the floor call (world, under both balls)", "    if (__world) this.drawTree(m);\n", "after")]
for r, q in zip(fp, Q_P):
    assert (r["label"], r["anchor"], r["mode"]) == q, q[0]
assert fp[0]["code"].endswith("    this.foreFade = 0;\n    this.foreAge = 0;\n    this.foreOut = 0;\n    this.foreT = -1;\n"
                              "    this.foreLead = null;\n    this.foreRune = null;\n    this.foreSeen = [0, 0];\n    this.foreFx = [];\n")
assert fp[1]["code"] == "    this.tickForesight(dt);             // FORESIGHT'S PICTURE (v75 section 6.1)\n"
assert "          const tof = Math.hypot(foe.x - f.x, foe.y - f.y) / f.w.shot.speed;\n" in fp[2]["code"]
assert "              && Math.hypot(g.x - foe.x, g.y - foe.y) < Rb * 3){ g.val = k; left--; }\n" in fp[2]["code"]
assert fp[3]["code"].startswith("    /* FORESIGHT'S FLOOR (v75 section 6.1): the rune where the foe will be,\n"
                                "       the sight-line from the bow to it and the rune")
print("returned rows == the files (labels, anchors, modes, the quoted code)")

base = (B / "links/sc-oracle-b10.html").read_text(encoding="utf-8")
assert hashlib.sha256(base.encode()).hexdigest()[:16] == "72dcd8aa43e5b501"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, (r["label"], t.count(r["anchor"]))
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


sha = lambda t: hashlib.sha256(t.encode()).hexdigest()[:16]
tp = apply(base, fp)
print("picture rows alone:", sha(tp), f"({len(tp) - len(base):+d})", "(picture lab's stamp 1bdec440699e6fd7, +16149)")
assert sha(tp) == "1bdec440699e6fd7"
tv = apply(base, fv)
print("voice rows alone:  ", sha(tv), f"({len(tv) - len(base):+d})", "(voice lab's e2e b65621b4f4847be5, +6856)")
assert sha(tv) == "b65621b4f4847be5"
tb = apply(base, fv + fp)
print("voice then picture:", sha(tb), f"({len(tb) - len(base):+d})", "(voice lab's interleaving 4e8f47301b97d7d7, +23005)")
assert sha(tb) == "4e8f47301b97d7d7"
assert apply(base, fp + fv) == tb
rows = fv + fp
rnd = random.Random(105)
for _ in range(20):
    o = rows[:]; rnd.shuffle(o)
    assert apply(base, o) == tb
print("picture-then-voice and 20 shuffles: byte-identical")

# no row's anchor inside another's; anchor LINE spans in the base; merge rows that share a line
for i, a in enumerate(rows):
    for j, b in enumerate(rows):
        if i != j:
            assert a["anchor"] not in b["anchor"], (a["label"], b["label"])
            assert a["anchor"] not in b["code"], (a["label"], "in the code of", b["label"])


def span(r):
    p = base.index(r["anchor"])
    l0 = base.count("\n", 0, p)
    l1 = base.count("\n", 0, p + len(r["anchor"].rstrip("\n")))
    return l0 + 1, l1 + 1


spans = [(span(r), r) for r in rows]
for (s, r) in spans:
    print(f"  line {s[0]:>6}-{s[1]:<6} {r['mode']:<6} {r['label'][:80]}")
groups = []
for (s, r) in sorted(spans, key=lambda x: x[0]):
    if groups and s[0] <= groups[-1][0][1]:
        groups[-1][0] = (groups[-1][0][0], max(groups[-1][0][1], s[1])); groups[-1][1].append(r)
    else:
        groups.append([s, [r]])
shared = [g for g in groups if len(g[1]) > 1]
print(f"{len(rows)} rows, {len(groups)} anchor-line groups; rows sharing an anchor line: {len(shared)}")
edits = []
for r in rows:                         # voice then picture, as ironwood / bindweed
    g = next(g for g in groups if r in g[1])
    if len(g[1]) == 1:
        edits.append((r["label"], r["anchor"], new_of(r)))
    elif r is g[1][0]:
        raise SystemExit("rows share an anchor line: merge by hand (none expected)")
t = base
for label, old, new in edits:
    assert t.count(old) == 1
    t = t.replace(old, new, 1)
assert t == tb
for label, old, new in edits:
    for s_ in (label, old, new):
        assert "'''" not in s_ and "\\" not in s_, label
print(len(edits), "edits; none carries ''' or a backslash")

if not WRITE:
    sys.exit(0)

out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v75 §6.1-6.2), picked on measurements under",
       "# Rick's \"you pick i overrule\" by `oracle_voice_lab.py` (the four voices) and",
       "# the picture lab (the eye, the rune and its sight-line, the rune motes, the",
       "# window arrows' rune, the flare and the count on the HEX tag) -- v105 §5.",
       "# Presentation only: engine_ab over all 39 relics, Oracle included, is the",
       "# proof, and probe [8] / [9] read it inside the hooks. The rows are byte-exact",
       "# to the labs' own files (voice 4, picture 7; no two share an anchor line, so",
       "# none is merged). No fx.js field: the cast's one `m.ultFx` slot is Oracle's",
       "# for a median 0.67s of the 8s window, so the design's rune motes are DRAWN.",
       "S6 = ["]
for label, old, new in edits:
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", "",
        "# The names stage 6 adds, free on the base (`drawSigils` / `m.sigils` are",
        "# Converse's, `vine` / `tickVines` the Thicket's; `sight` is only stage 2's).",
        "S6_NAMES = (\"tickForesight\", \"drawForesight\", \"_foreEye\", \"foreFade\", '\"oracle-sigil\"',",
        "            '\"oracle-hex\"', '\"oracle-close\"', 'w === \"oracle\"')",
        "# What stage 6's ADDED code may write: its own fore* fields, the canvas, a",
        "# tag's count (`val`), a flare record's clock, and an oscillator's pitch.",
        "S6_WRITE_OK = (lambda obj, prop: prop.startswith(\"fore\") or obj == \"c\" or prop == \"val\"",
        "               or (prop == \"t\" and obj.endswith(\"]\"))",
        "               or (obj, prop) == (\"frequency\", \"value\"))",
        ""]
block = "\n".join(out)
p = pathlib.Path("C:/dev/sundered-crown/tools/oracle_build.py")
s = p.read_text(encoding="utf-8")
assert hashlib.sha256(s.encode()).hexdigest()[:16] == "1e18f0642c2de40c", "the builder moved"
anchor = ('\nSTAGE_OUT = {"1": "sc-oracle", "2": "sc-oracle-aim", "3": "sc-oracle-sight",\n'
          '             "5": "sc-oracle-b{blade}"}\n')
reps = [
 (anchor,
  block + '\nSTAGE_OUT = {"1": "sc-oracle", "2": "sc-oracle-aim", "3": "sc-oracle-sight",\n'
          '             "5": "sc-oracle-b{blade}", "6": "sc-oracle-fx"}\n'),
 ('    (stage 6, the picture and the voice, is a later claim: v105 §5)\n',
  '    stage 6   the picture and the voice   -> sc-oracle-fx.html           (no field: drawn motes, v105 §5)\n'),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''        else:
            if TUNED is None:
                raise SystemExit("stage 5 is not measured yet (TUNED is None)")''',
  '''        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: Oracle's ult block and blade are
            # stage 5's, and none of stage 6's names is in the source yet.
            want = ult_block(ULT["charge"], ULT["hex"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f'dmg:{TUNED["dmg"]},' not in relic_row(code, RELIC)):
                raise SystemExit("stage 6 goes on stage 5: Oracle's ult block or blade is not stage 5's")
            for name in S6_NAMES:
                if name in code:
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            edits = S6
        else:
            if TUNED is None:
                raise SystemExit("stage 5 is not measured yet (TUNED is None)")'''),
 ('''    blade = TUNED["dmg"] if A.stage == "5" else BLADE0''',
  '''    blade = TUNED["dmg"] if A.stage in ("5", "6") else BLADE0'''),
 ('''    for label, old, new in S1 + S2 + S3 + (S5() if TUNED else []):
        # WHAT THE INSERT ADDS''',
  '''    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor aside)
    # draws no RNG, never takes the one ultFx slot (open item 25), calls nothing
    # that applies, hurts, heals, resolves, shatters, casts or knocks, and writes
    # only what S6_WRITE_OK names. The probe's [8] / [9] and engine_ab are the
    # dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|beat|resolveHit|shatter|fireUlt|knock|spawnShot)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\.(\\w+)\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
    for label, old, new in S1 + S2 + S3 + (S5() if TUNED else []) + S6:
        # WHAT THE INSERT ADDS'''),
 ('''    done = {"1": S1, "2": S1 + S2, "3": S1 + S2 + S3, "5": S1 + S2 + S3 + (S5() if TUNED else [])}[A.stage]''',
  '''    done = {"1": S1, "2": S1 + S2, "3": S1 + S2 + S3, "5": S1 + S2 + S3 + (S5() if TUNED else []),
            "6": S1 + S2 + S3 + (S5() if TUNED else []) + S6}[A.stage]'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("stage 6 written into oracle_build.py:", len(edits), "edits;", hashlib.sha256(s.encode()).hexdigest()[:16])
