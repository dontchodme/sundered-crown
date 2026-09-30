"""Hand-wire --stage 6 into tools/goreshard_build.py (after gen_s6.py wrote the S6 table)."""
import pathlib, hashlib
p = pathlib.Path("C:/dev/sundered-crown/tools/goreshard_build.py")
s = p.read_bytes().decode("utf-8")
assert "\r" not in s and "\nS6 = [" in s
if "def s6_static_checks" in s:
    raise SystemExit("already wired")

reps = []

# ---- the docstring: the stage table
reps.append(('''    stage 5   the blade                 -> sc-goreshard-b<blade>.html
              the design's stage 2 ("the blade"), settled by Rick's 2026-09-29
              ruling: the measured point nearest 50% both sides (reading 12)
    (stage 6, the picture and the voice -- the design's stage 3 -- is not
    this builder's yet; the beam's field spec leaves both fx.js copies at the
    carry, by the orchestrator.)
''', '''    stage 5   the blade                 -> sc-goreshard-b<blade>.html
              the design's stage 2 ("the blade"), settled by Rick's 2026-09-29
              ruling: the measured point nearest 50% both sides (reading 12)
    stage 6   the picture and the voice -> sc-goreshard-b<blade>-fx.html
              the design's stage 3 ("picture, voice, carry; beam's field spec
              out"), on stage 5's link: the labs' rows, byte for byte (S6,
              readings 13-21). No fx.js field (reading 15): the beam's
              `SPECS.oathwound` leaves BOTH fx.js copies at the carry, by the
              orchestrator's fx_remove; stage 6 leaves the inlined copy as it
              is, and refuses if its edits touch it.
'''))

# ---- the docstring: reading 8's tail, then readings 13-21 after reading 12
reps.append(('''     are keyed on the relic, not the kind. Stage 6 (the design's stage 3:
     "the beam art is retired") retires them. Nothing in the simulation reads
     any of them. The beam had no `radius`, so fireUlt's record is as it was.
''', '''     are keyed on the relic, not the kind. Stage 6 (the design's stage 3:
     "the beam art is retired") retires the pool, the seam and the sigil and
     adds the cast's own voice (readings 13-21); `SPECS.oathwound` goes at the
     carry (reading 15). Nothing in the simulation reads any of them. The
     beam had no `radius`, so fireUlt's record is as it was.
'''))

reps.append(('''     "confirm 9.17" (the design's own target, measured beside it, v114 §4).
     The design names no other knob, and none moved.
''', '''     "confirm 9.17" (the design's own target, measured beside it, v114 §4).
     The design names no other knob, and none moved.

STAGE 6 -- THE PICTURE AND THE VOICE (v81 §4: "Picture: the beam art is
retired. Cast: the blade darkens to arterial red for the window; the blade's
glow SCALES with the foe's current stack count (0 -> 4 maps alpha 0.2 -> 0.8),
so 'harder the more you bleed' is on the sword itself; the damage float on a
scaled blow is drawn larger. Field: blood motes off the blade, both copies.
Sound: cast -- a wet drawn-blade hiss, 0.4s; a scaled blow -- the sword's strike
voice pitched DOWN by the stack count (bigger = lower); close -- nothing.").
Every look and sound is Code's pick on measurements under Rick's "you pick i
overrule" (the picture lab, scratch `gs_rows.py`; `goreshard_voice_lab.py`;
v114 §5). The rows are the labs' own, byte for byte (the S6 table below says
how that is proved).
  13. THE PICTURE HANGS OFF THE FIGHTER (`gore*` fields), never `m.ultFx`:
     that slot is one, and the opponent's cast takes it (open item 25). It is
     driven on the presentation clock (`tickGore`, called from
     tickPresentation), which runs through a hit stop and after `over`.
  14. THE WINDOW IS READ OFF `ultPrice && !over`, with both fighters standing
     (reading 5: about one window in seven is still set at `over`), so the
     blade drains at the verdict; THE CAST IS FOUND BY `priceTally.casts`
     RISING, so fireUlt makes no call for the picture.
  15. NO fx.js FIELD. "Field: blood motes off the blade, both copies" is drawn
     as motes shed off the blade's barbs (`_goreShed`, `drawGoreDrops`: world
     pass, under both balls, placed by shellHash, never the RNG), not a SPECS
     field: a field rides the one ultFx slot, which the picture lab measured
     as Goreshard's at 89 of 107 casts and for a median 0.67 s of an 8 s
     window (7.5%), lost to the opponent's cast 18 times; and a field bursts
     where the cast was, a median 220 units from the blade it is to come off.
     The beam's own `SPECS.oathwound` (a beam field) is retired at the carry,
     out of both copies, by the orchestrator's fx_remove; stage 6 does not
     touch the inlined copy (checked, and refused if it does).
  16. THE GLOW is the blade's own glow sprite (weaponGlow's cache, baked once a
     reach, never per frame), in the school's bright `glow`, added at 0.2 +
     0.15 x the foe's Hemorrhage read live through `stacks` (a pure read),
     eased; the design's 0 -> 4 maps 0.2 -> 0.8.
  17. THE FLOAT on a scaled blow is x(1 + 0.1 x priceN), the stacks the blow
     paid on: `priceN` is 0 on every blow the price did not scale (the window
     shut, the struck body not bleeding, every other relic), so every other
     float is the old size exactly. It REPLACES resolveHit's shared float-size
     line with its own text times that factor: one of the two lines stage 6
     puts on the sim path, and it writes only the float (presentation).
  18. THE SCALED BLOW'S VOICE is the plain strike at the damage dealt (its
     weight, level, jitter and crit the blow's own), every frequency down a
     semitone a stack (SEMI, of five; a major third at 4), held at 4's voice
     above Hemorrhage's cap. It plays for a blow priced on n > 0: a window blow
     on a body with no Hemorrhage is x1 and keeps the plain call. The other
     line on the sim path passes `price: priceN` to that call, before the
     hit-voice line, which follows unchanged for every other blow.
  19. THE CAST'S VOICE is its own arm (DRIP, of four: a Q 5 scrape rising
     2.6 -> 8 kHz in two strokes, three drops chirping off the blade),
     ADDED before the shared rune-crack fallback, which eleven other relics
     still use and which is re-emitted unchanged, last. fireUlt already plays
     `ult/oathwound` once a cast. THE CLOSE plays nothing (the design's "close
     -- nothing").
  20. THE BEAM'S ART IS RETIRED: drawUltUnder's pool and drawUltOver's seam
     (`u.w === "oathwound"`) go, and the charge sigil `ULTSIG.oathwound`
     (it drew a beam and the pool under it) is redrawn as a greatsword that
     reddens as the charge fills. The ultFx `life` entry `oathwound: 1.5` is
     KEPT: it equals the map's default 1.5, and a line other relics' rows
     anchor on is not worth a row that changes nothing.
  21. NOTHING OF IT REACHES THE SIMULATION: no RNG, no spawnFx, no ultFx, no
     Math.random, no call into the simulation, no write but its own `gore*`
     fields, its motes, the renderer's canvas and cache and the synth's nodes;
     the voice and the float its only two lines on the sim path, each whole
     and where it belongs. The probe's [11]-[12] and engine_ab (all 38 relics,
     Goreshard included) are the dynamic proof.
'''))

# ---- after the S6 table: the stage-6 scans
reps.append(('''
STAGE_OUT = {"1": "sc-goreshard-stub", "2": "sc-goreshard-price",
             "5": f"sc-goreshard-b{TUNED['dmg']}"}
''', '''
# THE STAGE-6 SCANS (readings 13-21). Everything the table's ADDED code may do.
S6_NAMES = ("tickGore", "_goreShed", "drawGoreWeapon", "_gorePal", "_gorePals", "_goreGlow", "_goreSteel",
            "_goreFront", "drawGoreDrops", "goreFade", "goreAge", "goreOut", "goreGlow", "goreSeen", "goreAcc",
            "goreDropN", "goreDrops", "goreTh", "goreT", "goreW")
S6_SFX_ROWS = ("Sfx: the scaled blow", "Sfx: Goreshard's cast arm")
S6_TICK_ROW = "bloodprice picture: tickGore"
S6_DRAW_ROW = "bloodprice picture: the drawing methods"
# THE TWO LINES ON THE SIM PATH, whole (readings 17 and 18): each row's added
# code, comments stripped, line for line.
S6_SIM_LINES = {
    "resolveHit: a scaled blow's hit voice": ['if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });', "else"],
    "bloodprice picture: the priced blow's float": [
        "const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);"],
}
FLOAT_OLD = "    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1);\\n"
HIT_VOICE = '    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });\\n'
# THE SHARED MODULE TABLES STAGE 6 MAY READ, by exact path, and no other
# reference to one (no write: a table written holds for every later match).
S6_TABLE_READS = ("CONFIG.physics.ballR", "CONFIG.arena", "SHAPES[f.w.shape]")
RUNE_CRACK = "        } else {                                        // rune-crack"
S6_ARM = '} else if (w === "oathwound"){'
PRICED_HIT = 'else if (kind === "hit" && p.price){'
PLAIN_HIT = '      else if (kind === "hit"){\\n'
BEAM_GONE = ('u.w === "oathwound"', "BLOODPRICE -- a beam, and the toll paid under it.",
             "Bloodprice: what runs out of the wound", "Bloodprice: a seam torn open in the air")


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 15)."""
    head = re.search(r"/\\* ---- src/render/fx\\.js, inlined by fx_build\\.py\\. "
                     r"sha256:([0-9a-f]{64}) ---- \\*/\\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_added(old: str, new: str) -> str:
    """A stage-6 row's ADDED code, comments out: its new text less the anchor it
    re-emits (a replace row adds all of its new text)."""
    return strip_comments(new.replace(old, "", 1) if old in new else new)


def s6_bound_once(ins: str, name: str, expr: str) -> bool:
    """`name` is bound exactly once in the insert, as `const name = expr` (alone
    or the first of a const list), and bound or assigned nowhere else."""
    decl = "const " + name + " = " + expr
    if len(re.findall(re.escape(decl) + r"[;,]", ins)) != 1:
        return False
    rest = ins.replace(decl, "", 1)
    return not re.search(r"\\b(?:const|let|var)\\s+" + re.escape(name) + r"\\b|[,(]\\s*" + re.escape(name)
                         + r"\\s*=(?!=)|(?<![\\w.$])" + re.escape(name) + r"\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)",
                         rest)


def s6_local_array(ins: str, name: str) -> bool:
    """`name` is the insert's own fresh array: bound once as `const name = [`,
    and bound or assigned nowhere else."""
    return (len(re.findall(r"\\bconst " + re.escape(name) + r" = \\[", ins)) == 1
            and not re.search(r"\\b(?:let|var)\\s+" + re.escape(name) + r"\\b|(?<![\\w.$])" + re.escape(name)
                              + r"\\s*(?:=(?!=)|\\+=|-=)", ins.replace("const " + name + " = [", "", 1)))


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION (reading 21). Its ADDED code (a row's re-emitted
    anchor aside) draws no RNG, never takes the one ultFx slot (open item 25),
    calls nothing that hurts, applies, resolves, beats, floats or knocks, never
    writes the shared weapon row or a module table (it reads three of them by
    exact path), writes only its own `gore*` fields, its motes' clocks, the
    renderer's canvas and cache and the synth's nodes; mutates only its own
    motes; `SFX` and the float size only in their two sim-path rows, each whole;
    the synth only in the Sfx arms. The probe's [11]-[12] and engine_ab are the
    dynamic proof. Run on every stage: it reads the table."""
    WRITE = r"\\s*(?:=(?!=)|\\+=|-=|\\*=|/=|\\+\\+|--)"
    labels = [lb for lb, _o, _n in S6]
    for want in list(S6_SIM_LINES) + list(S6_SFX_ROWS) + [S6_TICK_ROW, S6_DRAW_ROW]:
        if sum(1 for lb in labels if lb.startswith(want)) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- the S6 table has no single row '{want}'")
    for label, old, new in S6:
        ins = s6_added(old, new)
        sfx = label.startswith(S6_SFX_ROWS)
        tick = label.startswith(S6_TICK_ROW)
        draw = label.startswith(S6_DRAW_ROW)
        if re.search(r"\\brng\\b", ins) or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|breakSpin|"
                     r"takeHitstun|tickPrice|tickStatus|tickWeapon|tickHits|tickCharge|spawnShot|spawnSpark|note|"
                     r"checkEnd|statusTag|step|ring|burst)\\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\\bw\\.[A-Za-z_]\\w*(\\.\\w+)*" + WRITE, ins) or re.search(r"\\bw\\[", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        for mt in re.finditer(r"\\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES|ULT_LIFE|ACTS)\\b"
                              r"(?:\\s*\\.\\s*[A-Za-z_$][\\w$]*|\\s*\\[[^\\]]*\\])*", ins):
            if mt.group(0) not in S6_TABLE_READS or re.match(WRITE, ins[mt.end():]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reaches a shared "
                                 f"module table other than by the reads it may make: {mt.group(0)!r}")
        if re.search(r"\\.\\s*(beat|beats|hurt|knock|shake|hitStop|pin|stun|stunDR|charge|status|ultPrice|priceTally|"
                     r"hp|alive|over|winner|theta|swingPhase|spinDir|vx|vy|x|y|hitCd|bleedCap|dealt|hits|crits)\\b"
                     + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the window, "
                             "the tally, a status or a body")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its own text alone:\\n{ins}")
        elif re.search(r"\\bSFX\\b|\\bfsz\\b|\\bfloats\\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice or sizes "
                             "a float outside its two sim-path rows")
        if re.search(r"\\b_tone\\s*\\(|\\b_burst\\s*\\(|\\b_sweep\\s*\\(|\\.play\\s*\\(|\\bfrequency\\b|"
                     r"\\bcreateOscillator\\b|\\bctx\\.destination\\b", ins) and not sim and not sfx:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if re.search(r"\\bdelete\\s|Object\\.(defineProperty|defineProperties|setPrototypeOf)\\s*\\(", ins) \\
                or re.search(r"Object\\.assign\\s*\\((?!\\{\\}\\s*,)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes or "
                             "redefines a property, or assigns into an object it did not make")
        # THE CANVAS: `c` only as the renderer's own context, or a method's first parameter
        for mb in re.finditer(r"\\b(?:const|let|var)\\s+c\\s*=\\s*([^,;\\n]+)", ins):
            if mb.group(1).strip() != "this.ctx":
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' binds "
                                 f"`c` to {mb.group(1).strip()!r}, not the renderer's context")
        if re.search(r"(?<![\\w.$])c\\s*=(?!=)", ins.replace("const c =", "")):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reassigns `c`")
        for mw in re.finditer(r"([\\w\\]\\)]+)\\s*\\.\\s*(\\w+)" + WRITE, ins):
            obj, prop = mw.group(1), mw.group(2)
            ok = ((obj == "f" and prop.startswith("gore"))
                  or (obj == "this" and draw and prop == "_gorePals")
                  or obj == "c"
                  or (tick and obj == "i]" and prop == "t" and "f.goreDrops[i].t += dt;" in ins))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes {obj}.{prop}")
        for mw in re.finditer(r"([\\w\\]\\)$.]+)\\s*\\.\\s*(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\\s*\\(", ins):
            if not ((tick and mw.group(1) == "f.goreDrops") or s6_local_array(ins, mw.group(1))):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' mutates {mw.group(1)}")
        # an index write (a destructuring `const [a, b] = ...` is a declaration, not one): only the
        # renderer's own palette cache, bound once as `const C = this._gorePals || (...)`
        for mi in re.finditer(r"([\\w\\]\\)$]+)\\s*\\[[^\\]]*\\]" + WRITE, re.sub(r"\\b(?:const|let|var)\\s*\\[[^\\]]*\\]", "D", ins)):
            if not (draw and mi.group(1) == "C"
                    and s6_bound_once(ins, "C", "this._gorePals || (this._gorePals = {})")):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes through an index")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page (readings 15-21): the inlined fx.js
    untouched; the rune-crack fallback kept once and after Goreshard's arm; the
    priced-blow branch before the plain hit arm, which stays once; the beam's
    art gone; the two sim-path lines each once, where they belong, after the
    price's read; every call, pass and method wired exactly once; no
    Math.random added or taken."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 15; SPECS.oathwound goes at the carry)")
    if s.count(RUNE_CRACK) != 1 or not 0 <= s.find(S6_ARM) < s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Goreshard's cast arm")
    if s.count(PLAIN_HIT) != 1 or not 0 <= s.find(PRICED_HIT) < s.find(PLAIN_HIT):
        raise SystemExit("REFUSING TO WRITE -- the priced-blow branch is not before the plain hit "
                         "arm, or the plain arm is not there once")
    for gone in BEAM_GONE:
        if gone in s:
            raise SystemExit(f"REFUSING TO WRITE -- the beam's art is still drawn: {gone!r}")
    for need in ("this.tickGore(dt);", "if (__world) this.drawGoreDrops(m);", "  tickGore(dt){",
                 "  _goreShed(f){", "  drawGoreWeapon(m, f, reach, dim){", "  drawGoreDrops(m){",
                 "if (f.goreFade > 0 && this.drawGoreWeapon(m, f, reach, dim)) return;", S6_ARM, PRICED_HIT,
                 "  oathwound(c, t, cf, P){"):
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        for ln in v[:1]:
            if out_code.count(ln) != code.count(ln) + 1:
                raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    if FLOAT_OLD in s:
        raise SystemExit("REFUSING TO WRITE -- resolveHit's old float-size line is still there")
    rh = out_code[out_code.find("  resolveHit(self, foe, hx, hy, seg"):]
    rh = rh[:rh.find("\\n  }\\n")]
    i_n = rh.find('const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;')
    i_f = rh.find("const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);")
    m_v = re.search(r'if \\(priceN > 0\\) SFX\\.play\\("hit", \\{ dmg, crit, price: priceN \\}\\);\\s*else\\s*'
                    r'SFX\\.play\\("hit", self\\.ultTree \\? \\{ dmg, crit, bough: self\\.w\\.ult\\.winDmg \\} : '
                    r'\\{ dmg, crit \\}\\);', rh)
    if not (0 <= i_n < i_f and m_v and i_f < m_v.start()):
        raise SystemExit("REFUSING TO WRITE -- the float and the priced voice are not in resolveHit, "
                         "after the price's read, the voice just before the hit-voice line")
    if "  tickPresentation(dt){\\n    this.tickNovaFx(dt);\\n    this.tickGore(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickGore does not follow tickNovaFx in tickPresentation")
    if out_code.count('SFX.play("ult", { w: f.w.id });') != code.count('SFX.play("ult", { w: f.w.id });'):
        raise SystemExit("REFUSING TO WRITE -- fireUlt's cast voice moved")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- stage 6 moves a Math.random")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes its own gore* "
          "fields, its motes, the canvas and the synth only; the priced voice and the float its two lines on "
          "the sim path, each where it belongs); the inlined fx.js untouched; the rune-crack fallback kept; "
          "the beam's art gone; every call, pass, arm and method once")


STAGE_OUT = {"1": "sc-goreshard-stub", "2": "sc-goreshard-price",
             "5": f"sc-goreshard-b{TUNED['dmg']}", "6": f"sc-goreshard-b{TUNED['dmg']}-fx"}
'''))

# ---- main(): the stage choices
reps.append(('''    ap.add_argument("--stage", choices=["1", "2", "5"], required=True)''',
             '''    ap.add_argument("--stage", choices=["1", "2", "5", "6"], required=True)'''))

# ---- main(): the base's Goreshard head (stage 6 goes on stage 5, whose blade is TUNED)
reps.append(('''    if SHIP_HEAD not in s0:
        raise SystemExit("wrong base: Goreshard's row (greatsword, 9.17, hemorrhage 2) has moved")
''', '''    head = SHIP_HEAD if A.stage != "6" else SHIP_HEAD.replace(f"dmg:{SHIP_BLADE},", f"dmg:{TUNED['dmg']},")
    if head not in s0:
        raise SystemExit("wrong base: Goreshard's row (greatsword, "
                         f"{SHIP_BLADE if A.stage != '6' else TUNED['dmg']}, hemorrhage 2) has moved")
'''))

# ---- main(): the stage-6 branch
reps.append(('''    else:
        if f'charge:{ULT["charge"]}, kind:"price"' not in code or "tickPrice(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want, blade = S5, ult_block(ULT["charge"]), TUNED["dmg"]
''', '''    elif A.stage == "5":
        if f'charge:{ULT["charge"]}, kind:"price"' not in code or "tickPrice(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want, blade = S5, ult_block(ULT["charge"]), TUNED["dmg"]
    else:
        # STAGE 6 GOES ON STAGE 5, ONCE: the price at its charge, the tuned
        # blade on Goreshard's row, and none of stage 6's names in the source
        # yet (on identifier boundaries).
        if (f'charge:{ULT["charge"]}, kind:"price"' not in code or "tickPrice(dt){" not in code
                or f"dmg:{TUNED['dmg']}," not in relic_row(code, RELIC)):
            raise SystemExit("stage 6 goes on stage 5 (the price at its charge, the blade at "
                             f"{TUNED['dmg']})")
        for name in S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
        if S6_ARM in code or PRICED_HIT in code:
            raise SystemExit("Goreshard's voices are already in this source -- stage 6 goes on once")
        edits, want, blade = S6, ult_block(ULT["charge"]), TUNED["dmg"]
'''))

# ---- main(): run the stage-6 scans on every stage (they read the table), before the S1-S5 scan
reps.append(('''    # WHAT THE ADDED CODE MAY DO, AND NOTHING ELSE (readings 4 and 10). The
    # anchor each row re-emits is taken out first.
    for label, old, new in S1 + S2 + S5:
''', '''    # STAGE 6'S TABLE IS PRESENTATION (reading 21): read on every stage.
    s6_static_checks()
    # WHAT THE ADDED CODE MAY DO, AND NOTHING ELSE (readings 4 and 10). The
    # anchor each row re-emits is taken out first.
    for label, old, new in S1 + S2 + S5:
'''))

# ---- main(): the output checks
reps.append(('''    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\\n")
''', '''    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\\n")
'''))

for a, b in reps:
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)
p.write_bytes(s.encode("utf-8"))
print("wired; builder sha16", hashlib.sha256(s.encode()).hexdigest()[:16])
