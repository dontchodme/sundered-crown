#!/usr/bin/env python
"""AUREOLE / BENEDICTION, REDESIGNED -- a halo stands around her. v110.

Built from `06-docs/v82/aureole-benediction-redesign-v82.md` (Cowork,
2026-09-26), its §5 build brief and its runs (`06-docs/v82/runs/halo_base.*`,
`tools/overlays/halo.js`), which are the input and the only input. CLAUDE.md
§3 rule 0: nothing here is a design decision. A REDESIGN: the relic ships in
the base; its ultimate is replaced.

    stage 1   the new ultimate stubbed (1e9); the beam out
                                          <tip> -> sc-aureole-stub.html   (= arm A)
    stage 2   the halo and the smite      -> sc-aureole-halo.html         (arm B, brief stage 1)
    stage 3   the blessing                -> sc-aureole-bless.html        (arm C, brief stage 2)
    stage 5   the blade to the shipped rate (brief stage 3), 16.01 -> 12.5
                                          -> sc-aureole-b12.5.html        (stage 6 goes on it)
              `--stage 5 --alt50` writes Rick's other choice, 50%: blade 11.5
                                          -> sc-aureole-b11.5.html        (not the carry)
    stage 6   the picture and the voice (brief stage 4), on stage 5's link
                                          -> sc-aureole-b12.5-fx.html     THE FINAL LINK
              presentation only; no fx.js field (reading 19): the beam's
              SPECS.aureole is the orchestrator's `fx_remove.py` at the carry

§1: "For a duration a halo of light stands around Aureole, wide enough to
reach half the hall. An enemy inside the halo is smitten for as long as it
stays there -- and for as long as an enemy is inside it, Aureole is blessed."

Declared (§4, the lab `overlays/halo.js`, whose defaults ARE the settled
numbers: haloR 150, tickCd 0.5, blessCd 0.8):
  THE HALO     for the window a disc of radius haloR (150) on the caster's
               centre; the foe is INSIDE when its centre is strictly within
               haloR + R of the caster's centre (the lab's `<`).
  THE SMITE    while the foe is inside, foe.apply("smite", smite) every
               tickCd (0.5s): the cooldown runs through the whole window,
               inside or not, and a smite lands on the first inside frame it
               is clear -- the first on the cast frame if the foe is inside.
  THE BLESSING while the foe is inside, the caster's own apply("blessing",
               bless) every blessCd (0.8s), on its own cooldown, run the same
               way (stage 3). It heals through tickStatus (1.2 hp/s a stack).
  "No damage, no knock, no beat": the halo calls no hurt, moves nobody,
  stops nothing and files nothing. The smite's own ticks are tickStatus's,
  which already files a fatal tick's beat. No rng.

THE CHARGE. The design names none. Every run it was priced on
(`halo_base.json`: "charge": 16.0) cast every 16 seconds of the LAB's step
clock, the harness's default, which counts hit-stop freezes. Rick,
2026-09-27, for the whole batch: "use the game's equivalent". Measured for
this fighter on the lab's arm C (v110 §0): 14. (The shipped Benediction also
charged 14 on the engine's clock.)

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE WINDOW IS 8s: §1 says "for a duration"; every run used the
     harness's dur 8.
  2. THE CHARGE is the lab's 16 converted (above).
  3. THE INSIDE TEST is the foe's centre strictly within haloR + R of the
     caster's centre, on the ticker's frame (§4 "inside = foe centre within
     150 + R"; the lab's `<`).
  4. THE TWO COOLDOWNS run through the whole window, inside or not, and each
     fires on the first inside frame it is clear (the lab's `cd -= dt` every
     open frame; what was priced). Both start clear at the cast (the lab's
     onCast). They are separate clocks: a smite frame is not a blessing
     frame unless both are clear.
  5. THE SMITE AND THE BLESSING ARE apply() AND NOTHING ELSE (§4 "No damage,
     no knock, no beat"): no hurt, no float, no tag, no stop, no push.
  6. `apply`'s SOURCE IS A SIDE LETTER (Rick's ruling 4; §4 and the lab pass
     the Fighter). Smite's source is read only by a fatal tick's beat in
     tickStatus (`st.src === "a" ? this.a : this.b`): the side letter credits
     HER side; the lab's Fighter would credit side b every time (the probe's
     [8]). Blessing's source has no reader.
  7. NO BEAT. The halo files none (§4); a smite tick that kills files its own
     fatal beat inside tickStatus, as every smite does (ruling 5 is met by
     the engine's existing path: the halo itself has no damage path).
  8. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).
  9. THE WINDOW CLOSES on its clock or EITHER death (the lab's); nothing is
     applied after the close.
 10. NO CAST WAITS. The design asks none, and a cast cannot find its window
     open: the charge is 14 of unfrozen time against a window of 8 on the
     same clock (the probe asserts it).
 11. NO ARROWS THROUGH THE HALO (arm D, +1; §6.3 "no, by the numbers"): the
     bow's shot, its blows and its onHit smite 1 are untouched.
 12. THE CARD is the design's own (§4, 67 characters): `A halo: foes inside
     it are smitten, and she is blessed while one is`.
 13. THE BEAM IS OUT (brief stage 1): Aureole's ult block (kind "beam", dmg
     15, heal 28) is replaced. `kind:"beam"` stays -- Goreshard's Bloodprice
     is a beam and runs fireUlt's generic tail. The tail's `if (u.heal)`
     block was Aureole's alone (no other ult block carries `heal:`; the
     builder asserts it) and is RETIRED with the beam. The beam's PICTURE
     (drawUltUnder's lit ground and drawUltOver's lance, keyed on the ultFx
     slot's "aureole"; the charge rune `ULTSIG.aureole`), its cast voice (the
     rune-crack fallback) and its field spec (`SPECS.aureole`, mode 'beam')
     are the brief's stage 4 (the picture, the voice, "beam's field spec
     out"), not this builder's stages 1-5, which leave them playing at the
     cast; stage 6 (readings 14-20) retires the picture and voices the halo,
     and the field spec is the orchestrator's to take out (reading 19).
     Nothing in the simulation reads any of them.

STAGE 6, THE PICTURE AND THE VOICE (§4's picture and sound; the brief's stage
4, "picture, voice, beam's field spec out"). Picked on measurements under
Rick's "you pick i overrule" by the picture lab (scratch) and
`aureole_voice_lab.py` (v110 §5); the rows are the labs', byte-exact.
Declared:
 14. THE PICTURE READS THE WINDOW OFF `ultHalo && alive && !over` and keeps
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

THE CLOCK. The window and both cooldowns run on the window tickers' clock,
which stops through a hit stop (Corollary's, Daybreak's, Zenith's, Canopy's,
Onslaught's, Tendril's and the hail's convention). The lab ran all three
through freezes; v110 §2 measures what that is worth here.

THE BASE is asserted BY CONTENT, never by which relic is last: Aureole's row
with the shipped Benediction verbatim and its shipped blade, the heal block
used by no other relic, the statuses the halo pays through, and every anchor
below exactly once. Every insert goes AFTER or BEFORE a stable line, so the
builder re-applies on a later tip that carries other new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "aureole"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v82 §4-§5.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v110 §0)
    "dur": 8,         # "for a duration" -- the harness's 8, every halo_base arm
    "haloR": 150,     # §4 "a disc r 150 on the caster's centre"
    "tickCd": 0.5,    # §4 `foe.apply("smite", 1, f)` "every 0.5s inside"
    "smite": 1,       # §4 smite +1
    "blessCd": 0.8,   # §4 `f.apply("blessing", 1, f)` "every 0.8s while inside"
    "bless": 1,       # §4 blessing +1 -- stage 3
}
TIP = "A halo: foes inside it are smitten, and she is blessed while one is"
SHIPPED_ULT = ('''    ult:{ name:"Benediction", charge:14, kind:"beam", dmg:15, heal:28, '''
               '''tip:"Shaft of light: 15 damage, heals 28" },
''')
SHIPPED_DMG = "16.01"
HEAL_BLOCK = '''    if (u.heal){
      const before = f.hp;
      f.hp = Math.min(f.maxHp, f.hp + u.heal);
      const got = Math.round(f.hp - before);
      if (got >= 1){
        f.mend = 1.6;
        this.float(f.x, f.y - 46, "+" + got, "#8FE3A0", 30 + got * 0.7);
      }
    }
'''


def ult_block(charge, bless) -> str:
    return (f'''    ult:{{ name:"Benediction", charge:{charge}, kind:"halo", dur:{ULT["dur"]},
          haloR:{ULT["haloR"]}, tickCd:{ULT["tickCd"]}, smite:{ULT["smite"]}, blessCd:{ULT["blessCd"]},
          bless:{bless},          // v82: the blessing (stage 3)
          tip:"{TIP}" }},
''')


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH to check the page")
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 "parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip()
                                               .splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


# ---------------------------------------------------------------- stage 1 --
# THE NEW ULTIMATE, STUBBED at charge 1e9 (the clock can never reach it, and
# `fireUlt` never runs for this relic), AND THE BEAM OUT. The row keeps every
# physical stat, the bow's shot, the school's channel and the blurb; only the
# ult block changes. Nothing else reads the ult block's fields, so this link
# must be the lab's arm A (the relic with no ultimate) fight for fight.
S1 = [

("Benediction becomes the halo, stubbed",
 SHIPPED_ULT,
 '''    /* BENEDICTION, REDESIGNED (v82; built v110): THE HALO. The beam that hit
       for 15 and healed 28 is retired. For the window a halo of radius haloR
       stands on her centre: a foe inside it is smitten every tickCd, and
       while one is she is blessed every blessCd. See `tickHalo`. */
''' + ult_block("1e9", 0)),

("the beam's heal is retired: `heal` was Aureole's alone",
 HEAL_BLOCK,
 '''    /* THE BEAM'S HEAL IS RETIRED (v82 §5 stage 1, "beam out"; built v110).
       `u.heal` restored `heal` hp at the cast and was read by no ult block but
       Aureole's shipped Benediction (heal 28); its ultimate is now the halo
       (`kind:"halo"`), which heals only through the blessing it earns. The
       beam's kind stays -- Goreshard's Bloodprice is a beam -- and so does
       the damage clause below. */
'''),

]

# ---------------------------------------------------------------- stage 2 --
# THE HALO AND THE SMITE (brief stage 1: "beam out, `f.ultHalo` in, the inside
# test and the smite"), the blessing written but inert at 0, and the charge on
# the game's clock.
S2 = [

("the halo has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Benediction", charge:1e9, kind:"halo", dur:8,
''',
 f'''    ult:{{ name:"Benediction", charge:{ULT["charge"]}, kind:"halo", dur:{ULT["dur"]},   // v82 stage 2: the halo stands
'''),

("the fighter carries the halo",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd, bcd} while AUREOLE's halo stands (v82). null on every other
       relic and on this one outside its window: `tickHalo`'s loop is two
       iterations that do nothing. `haloTally` is the probe's count, cumulative
       over the fight; nothing in the simulation reads it. */
    this.ultHalo = null;
    this.haloTally = null;
'''),

("the cast opens the halo and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "halo"){
      /* BENEDICTION (v82). NOTHING RESOLVES HERE: the cast raises the halo for
         `u.dur` seconds and `tickHalo` smites and blesses. Both cooldowns
         start clear, so a foe already inside is smitten (and she blessed) on
         the cast frame (the lab's). No damage and no heal at the cast: the
         beam is retired. */
      f.ultHalo = { t: 0, dur: u.dur, cd: 0, bcd: 0 };
      if (!f.haloTally)
        f.haloTally = { casts: 0, frames: 0, inFrames: 0, smite: 0, bless: 0, foeStk: 0 };
      f.haloTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the halo ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickHalo(dt);                  // BENEDICTION (v82)
'''),

("tickHalo smites and blesses",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE HALO ========
     v82 §1 / §4 / §5. While the window runs a halo of radius `haloR` stands
     on the caster's centre, and the foe is INSIDE when its centre is strictly
     within haloR + R of hers:
       THE SMITE     inside, and the smite cooldown clear: foe.apply("smite",
                     smite) and cd = tickCd.
       THE BLESSING  inside, and the blessing cooldown clear: her own
                     apply("blessing", bless) and bcd = blessCd (stage 3; 0
                     before it). It heals through tickStatus.
     BOTH COOLDOWNS RUN THROUGH THE WHOLE WINDOW, inside or not, and each
     fires on the first inside frame it is clear (the lab's cadence, and what
     was priced). The halo is apply() and NOTHING ELSE: no hurt, no knock, no
     stop, no beat (a smite tick that kills files its own inside tickStatus).
     The window closes on its clock or EITHER death. The target is the
     OPPONENT only. On the window tickers' clock, so all of it freezes through
     a hit stop. `apply`'s source is a side letter. No rng. */
  tickHalo(dt){
    const R = CONFIG.physics.ballR;
    for (const f of [this.a, this.b]){
      const Z = f.ultHalo;
      if (!Z) continue;
      const u = f.w.ult, T = f.haloTally;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHalo = null; continue; }
      T.frames++;
      Z.cd -= dt;
      Z.bcd -= dt;
      T.foeStk += foe.stacks("smite");
      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;
      T.inFrames++;
      const side = f === this.a ? "a" : "b";
      if (Z.cd <= 0){
        Z.cd = u.tickCd;
        foe.apply("smite", u.smite, side);
        T.smite += u.smite;
      }
      if (u.bless > 0 && Z.bcd <= 0){
        Z.bcd = u.blessCd;
        f.apply("blessing", u.bless, side);
        T.bless += u.bless;
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the blessing",
 '''          bless:0,          // v82: the blessing (stage 3)
''',
 f'''          bless:{ULT["bless"]},          // v82: the blessing (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE TO THE SHIPPED RATE (brief stage 3: "the blade, wide on 151 at
# 13.5 / 14 / 14.5 to the shipped rate"; §3: "the blade comes from 16.01 to
# about 14 (the bow row 9.5-16.2), settled wide to the shipped rate"). The
# target is the design's own: THE SHIPPED RATE, read on 151 -- Aureole as
# shipped (the beam at 16.01) on the base, relic_rate both sides, two blocks
# (seed0 2207 / 2317, every other relic a foe, 10 seeds a foe a side, 1480
# fights): 801 of 1480, 54.1%.
# Both sides, two blocks, 1480 fights a point, relic_rate on sc-aureole-bless
# (--set dmg; 16.01 is the link itself), in wins against the shipped 801:
#   16.01 -> 1085 (73.3%, +284)
#   the brief's grid  14.5 -> 1011 (68.3%, +210)  14 -> 985 (66.6%, +184)
#                     13.5 -> 910 (61.5%, +109)   -- ALL ABOVE THE SHIPPED RATE
#   under it  13 -> 854 (57.7%, +53)   12.5 -> 830 (56.1%, +29)
#             12 -> 770 (52.0%, -31)   11 -> 698 (47.2%, -103)  10 -> 544 (36.8%)
# The design's "about 14" took back a lab gap priced on 141, side A (C 69.4
# against a SHIP of 55.5); on 151, both sides, the redesign at the shipped blade
# reads 73.3 against the shipped 54.1, so the crossing of the shipped rate falls
# BELOW the brief's grid, at ~12.4. THE BRIEF NAMES NO KNOB TO MOVE FIRST, so
# the blade moves outside the grid, inside the bow row the design names
# (9.5-16.2), and it is said (v110 §4). The two measured points nearest the
# shipped rate are 12.5 (+29 wins) and 12 (-31): 12.5 is the nearer, by two
# wins (a tie inside one standard error, ~19 wins), and every tiebreak points
# the same way (the nearer to the design's "about 14" and to the brief's grid).
# SO THE BLADE IS 12.5. Rick's other choice, 50%: see ALT50_BLADE.
BLADE = "12.5"
# RICK'S OTHER CHOICE, 50% (the batch's standard for a new relic, not this
# design's target): the 50% line crosses between 12 (770 of 1480, +30 wins over
# half) and 11.5 (722, -18), at ~11.7; 11.5 is the measured point nearest it.
# `--stage 5 --alt50` writes it (sc-aureole-b11.5); it is NOT the carry.
ALT50_BLADE = "11.5"


STAGE_OUT = {"1": "sc-aureole-stub", "2": "sc-aureole-halo", "3": "sc-aureole-bless",
             "5": "sc-aureole-b12.5", "5 --alt50": "sc-aureole-b11.5", "6": "sc-aureole-b12.5-fx"}
NAMES = ("ultHalo", "haloTally", "tickHalo")


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def relic_row(code: str, rid: str) -> str:
    i = code.find(f'{{ id:"{rid}"')
    if i < 0:
        raise SystemExit(f"no {rid} in this source")
    return code[i:code.find("blurb:", i)]


def relic_ult(code: str) -> str:
    row = relic_row(code, RELIC)
    j = row.find("ult:{")
    k = row.find("},", j)
    return row[j:k + 2]


def ult_rows(code: str) -> list:
    """Every WEAPONS row's ult block, (id, block)."""
    out = []
    for m in re.finditer(r'\{ id:"([a-z]+)", name:"', code):
        row = code[m.start():code.find("blurb:", m.start())]
        j = row.find("ult:{")
        if j >= 0:
            out.append((m.group(1), row[j:row.find("},", j) + 2]))
    return out


def s5_edits(blade: str) -> list:
    return [
        ("the blade: to the shipped rate",
         f'''  {{ id:"aureole", name:"Aureole", aff:"sanctified", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:{SHIPPED_DMG},''',
         f'''  {{ id:"aureole", name:"Aureole", aff:"sanctified", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:{blade},'''),
    ]


# THE CARRY'S BLADE AS A MODULE-LEVEL TABLE, so `tools/chain_audit.py` (which
# reads module-level `(label, old, new)` tables and `*_NEW` constants, never a
# function's return) watches the blade like every other insert: a later tip
# that puts Aureole back at 16.01 reads "S5:the blade: to the shipped rate
# LOST" (v110 §4, runs/chain_audit_blade_control.txt). The v110 review found the
# blade unwatched while it lived only inside `s5_edits`. Rick's other choice
# (`--alt50`) is deliberately NOT a table: the carry is 12.5, and a table for
# 11.5 would read as LOST on the final link.
S5 = s5_edits(BLADE)


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v82 §4's picture and sound; its §5 brief stage 4,
# "picture, voice, beam's field spec out"), picked on measurements under
# Rick's "you pick i overrule" by the picture lab (scratch, `au_rows.py`) and
# `aureole_voice_lab.py` (v110 §5). PRESENTATION ONLY: engine_ab over all
# 38 relics, Aureole included, is the proof, and the probe's [9]-[10] read the
# voices and the picture's hook inside the fight. The rows are byte-exact to
# the labs' own files (voice 5a43210cd9d13019, 4 rows; picture
# ed67bd6722cbbe2b, 9 rows); the picture rows alone reproduce the picture
# lab's stamp (b8d571f46a2681af), the voice rows alone the voice lab's page
# (50d4b2dfd385397e), and the two sets give the same bytes in either order
# (f3228d8d1509edbb). No two rows share an anchor, so none is merged.
#   THE VOICE: three arms -- the cast's swell, a foe's entry, the close --
#   ADDED before the shared rune-crack fallback, which is re-emitted
#   unchanged, last; three things on the sim path, all inside tickHalo,
#   each around a line this build's stage 2 already wrote (the entry before
#   the inside test, the heal chime after `T.bless += u.bless;`, the close
#   before the window's own close line).
#   THE PICTURE: `tickBenediction` in tickPresentation; the halo in the
#   world pass under both balls (the ring, the wash, the motes, the foe's
#   rim); the beam's art retired (the lit ground, the lance, the life
#   entry) and the charge rune redrawn.
# COMPOSITION: nine anchors are re-emitted; four are consumed, all
# Aureole's own (the beam's two art branches, ULTSIG.aureole, and the life
# map's narrowest token `aureole: 1.6, `, which leaves Consecration's entry
# on the same line to its own build). The rows ride on four of stage 2's own
# lines (the fields, the inside test, the blessing's count, the close) and on
# shared lines every stage 6 of the batch uses as `after` / `before` anchors
# (tickPresentation's first call, tickWinnow, the world pass's drawTree,
# drawMotes, the rune-crack fallback).
S6 = [

("Sfx: Aureole's cast, entry and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "aureole"){                    // the halo rises
          /* AUREOLE'S CAST, THE HALO RISES -- v82 s4: "cast -- a soft choir
             swell (two re-struck tones, a fifth), 0.5s". PURE, of 5, picked on
             the numbers by `aureole_voice_lab.py` under Rick's "you pick i
             overrule" (v110). Aureole had no arm and fell through to
             rune-crack, which eleven other relics on its stage-5 link still
             used, so this ADDS arms before that fallback and leaves it alone.

             C4 and a just G4 (261.63 / 392.44 Hz, the score's III), the fifth
             at 0.8 of the root, as two sines. Each tone is held by re-striking
             it in phase at its own whole cycles nearest every 11 ms (a held
             note does not exist in this toolkit), each strike 0.25 s long,
             with `.frequency.value` set on every strike, the first carrying
             0.6 of its plateau. It swells +12.3 dB with no dip to a crest 350
             ms after the cast -- as the ring finishes opening -- and is gone
             by 560 ms (audible 555); both tones within 0.3 cents and 0.7 dB of
             each other from the start to the crest; flutter 1.7 dB; every
             partial a harmonic of C3 (a voice, not a chime), nothing over 4.9x
             the root within 56 dB of it (no edge). Its crest -2.7 dB re
             Aureole's blow; +17.2 dB over the score at its crest. Register at
             most 0.46 against rune-crack, the sanctified and bow casts, BAR,
             the seal, the blow and the death voice, and Angelus's cast and
             close. */
          const g = 0.0154, sw = 19.76, L = 0.36, D = 0.25, F = 261.6256;
          const lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);
          for (const [r, k] of [[1, 1], [1.5, 0.8]]){
            const f = F * r, dt = Math.max(1, Math.round(f * 0.011)) / f;
            const q = Math.pow(0.0001 / lv(0), dt / D);
            for (let j = 0; j * dt < L - 1e-9; j++){
              const s = j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, 0.6 / (1 - q)));
              this._tone(t + s, { freq: f, gain: a, dur: D, type:"sine" }).frequency.value = f;
            }
          }
        } else if (w === "aureole-enter"){              // a foe comes inside
          /* A FOE ENTERS THE HALO -- "a foe entering -- a single bright note"
             (v82 s4). CHIME, of 4 (`aureole_voice_lab.py`). `tickHalo` plays
             it on an inside tick that follows an outside tick of the same
             window.

             A harmonic chime struck on C6 (1046.50 Hz, the halo's root two
             octaves up): its 2nd and 3rd partials at 0.5 / 0.25, each dying
             faster. One onset; its note 1046 Hz holds (-0.0 cents) and stands
             55 dB over the noise round it; its 2.00x partial -7.5 dB re the
             note (bright); peak at 6 ms, audible 200 ms; loudest 50 ms -8.5 dB
             re the blow and +11.4 dB re the wall tick. It shares a frame with
             the heal chime on most entries: register at most 0.17 against it
             at any count, each keeping its own band within 0.0 dB; at most
             0.41 against the wall tick, hex-snap, the spark, Zenith's tick,
             the bowstring, the blow, the clank and the cast. */
          const g = 0.04991, f = 1046.502, D = 0.314;
          this._tone(t, { freq: f, gain: g, dur: D, type:"sine" }).frequency.value = f;
          for (const [m, km, d] of [[2, 0.5, 0.6], [3, 0.25, 0.4]])
            this._tone(t, { freq: f * m, gain: g * km, dur: D * d, type:"sine" }).frequency.value = f * m;
        } else if (w === "aureole-close"){              // and it closes
          /* THE HALO CLOSES -- "close -- the swell reversed" (v82 s4). TIGHT,
             of 5 (`aureole_voice_lab.py`): the cast run backward -- its
             release as a 200 ms climb on the dyad, then the swell unwinding
             19.76 dB over 0.2 s, the fall's length solved so the whole is as
             long as the cast.

             Its envelope correlates 0.91 with the cast's samples literally
             reversed; LATE 0.43 (the cast's 0.55); audible 555 ms; loudest 50
             ms +0.0 dB re the cast's (a reversal keeps its level). `tickHalo`
             plays it when the halo runs out by its clock with both alive. */
          const g = 0.01659, sw = 19.76, L = 0.2, D = 0.25, F = 261.6256;
          const lv = (s) => g * Math.pow(10, -sw * s / L / 20);
          const H = 0.2;
          for (const [r, k] of [[1, 1], [1.5, 0.8]]){
            const f = F * r, dt = Math.max(1, Math.round(f * 0.011)) / f;
            for (let j = 0; j * dt < H + L - 1e-9; j++){
              const u = j * dt, a = k * (u < H ? g * Math.pow(10, -1.7 * (1 - u / H)) : lv(u - H));
              this._tone(t + u, { freq: f, gain: a, dur: D, type:"sine" }).frequency.value = f;
            }
          }
        } else {                                        // rune-crack'''),

('tickHalo: the entry note, on an inside tick after an outside tick of the same window',
 '''      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;''',
 '''      /* BENEDICTION'S ENTRY (v82 s4: "a foe entering -- a single bright
         note"): an inside tick that follows an outside tick of the same
         window -- the foe crossing into the ring. `Z.voiceIn` is the voice's
         own memory of the last tick's inside test (1 / 0): born undefined
         with every cast, so a foe already inside when the halo rises is not
         an entry (the cast's swell has that moment). Nothing in the
         simulation reads it; the test is the ticker's own, repeated.
         Presentation only (aureole_voice_lab: fights identical). */
      const voiceIn = Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R;
      if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });
      Z.voiceIn = voiceIn ? 1 : 0;
      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;'''),

('tickHalo: the heal chime (spark collect, unchanged), once per blessing, with the count',
 '''        T.bless += u.bless;''',
 '''        T.bless += u.bless;
        /* BENEDICTION'S BLESSING (v82 s4: "the blessing -- the `spark
           collect` voice reused"): the EXISTING heal chime, unchanged, called
           as Zenith's tickSun calls it -- n = the blessing she now carries.
           Once per blessing, on its frame. Presentation only; nothing here
           is read back. */
        SFX.play("spark", { collect: true, n: f.stacks("blessing") });'''),

('tickHalo: the close, on a clock close with both alive, before the close line',
 '''      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHalo = null; continue; }''',
 '''      /* BENEDICTION'S CLOSE (v82 s4: "close -- the swell reversed"): on
         the frame the halo runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill flight, so both are left to the death voice
         (Tendril's, Canopy's, Zenith's and Lightkeeper's rule); a halo still
         up when the fight ends closes in the picture only. Presentation
         only; the next line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHalo = null; continue; }'''),

('benediction picture: fighter fields',
 '''    this.ultHalo = null;
    this.haloTally = null;
''',
 '''    this.ultHalo = null;
    this.haloTally = null;
    /* BENEDICTION'S PICTURE (v82 section 4), and none of it is the window:
       the ring contracts into the ball for 0.3s after `ultHalo` is gone, and
       "a foe inside" holds through a hit stop, so the picture keeps its own
       state. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickBenediction`); nothing in the simulation reads any of it.
         beneFade -- 1 while the halo stands; eased to 0 over the close
         beneAge  -- the presentation clock since the cast (the expansion)
         beneOut  -- the presentation clock since the close (the contraction)
         beneIn   -- the foe was inside on the last step the halo ticked
         beneLit  -- the ring's brightening, 0 -> 1 while the foe is inside
         beneSeen -- `haloTally`'s frames, inFrames, smite and bless as last seen
         beneTagS, beneTagB -- this inside stretch has had its SMITE / its
                     BLESSING tag */
    this.beneFade = 0;
    this.beneAge = 0;
    this.beneOut = 0;
    this.beneIn = false;
    this.beneLit = 0;
    this.beneSeen = [0, 0, 0, 0];
    this.beneTagS = false;
    this.beneTagB = false;
'''),

('benediction picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickBenediction(dt);           // BENEDICTION'S PICTURE (v82 section 4)
'''),

('benediction picture: tickBenediction',
 '''  tickWinnow(dt){
''',
 '''  /* --------------------------------------------- BENEDICTION'S PICTURE ---
     v82 section 4, on the presentation clock. HALF-SECONDS, like every `life`
     in `tickPresentation` (it runs twice a normal step): 0.6 is the ring's
     0.3s expansion out of the ball at the cast, 0.6 its 0.3s contraction
     back into it at the close, 0.2 / 0.5 the ring's brightening on a
     foe's way in (0.1s) and out (0.25s). The window is `ultHalo`, and not
     once the caster falls or the match ends: `tickHalo` never runs again once
     `over` is set, so a halo standing at the kill would otherwise stand
     through the verdict. INSIDE IS `tickHalo`'S OWN TEST AS IT RAN: a step the
     window ticked (`haloTally.frames` rose) is an inside step iff `inFrames`
     rose with it; through a hit stop nothing ticks and the last answer holds,
     as the halo does. THE TAG RULE (Corona's, Daybreak's, Zenith's,
     Canopy's): the first smite of each inside stretch tags SMITE and the
     foe's count on the foe, the first blessing tags BLESSING and hers on her,
     both re-armed the first step the foe is out -- found by watching
     `haloTally.smite` and `.bless` rise, so `tickHalo` makes no call for the
     picture. Writes presentation fields, `tags` and `taught` only, and draws
     no rng. */
  tickBenediction(dt){
    for (const f of [this.a, this.b]){
      const T = f.haloTally;
      if (!T && !(f.beneFade > 0)) continue;                   // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      const Z = (this.over || !f.alive) ? null : f.ultHalo;
      if (Z){
        if (!(f.beneFade > 0) || f.beneOut > 0){               // a cast
          f.beneAge = 0; f.beneOut = 0; f.beneIn = false; f.beneLit = 0;
          f.beneTagS = false; f.beneTagB = false;
        }
        f.beneFade = 1;
        f.beneAge += dt;
      } else if (f.beneFade > 0){
        f.beneOut += dt;
        f.beneFade = Math.max(0, 1 - f.beneOut / 0.6);
      }
      if (!T) continue;
      const S = f.beneSeen;
      const dF = T.frames - S[0], dI = T.inFrames - S[1], dS = T.smite - S[2], dB = T.bless - S[3];
      S[0] = T.frames; S[1] = T.inFrames; S[2] = T.smite; S[3] = T.bless;
      if (!Z) f.beneIn = false;
      else if (dF > 0) f.beneIn = dI > 0;
      if (!f.beneIn){ f.beneTagS = false; f.beneTagB = false; }
      if (f.beneIn || f.beneLit > 0)
        f.beneLit = f.beneIn ? Math.min(1, f.beneLit + dt / 0.2)
                             : Math.max(0, f.beneLit - dt / 0.5);
      if (!Z || !foe.alive || !(foe.hp > 0)) continue;
      if (dS > 0 && !f.beneTagS){
        f.beneTagS = true;
        const fs = !this.taught.smite && !!STATUS.smite.tip;
        if (fs) this.taught.smite = true;
        this.statusTag(foe.x, foe.y, "smite", fs, foe.stacks("smite"));
      }
      if (dB > 0 && !f.beneTagB){
        f.beneTagB = true;
        const fb = !this.taught.blessing && !!STATUS.blessing.tip;
        if (fb) this.taught.blessing = true;
        this.statusTag(f.x, f.y, "blessing", fb, f.stacks("blessing"));
      }
    }
  }

  tickWinnow(dt){
'''),

('benediction picture: the floor call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* BENEDICTION'S HALO (v82 section 4): the ring, the wash inside it, the
       motes drifting in along it and the rim on a foe inside. The WORLD pass
       and under both balls -- the ring runs through whichever shell is on it
       and a white light over a near-white body erases it (CLAUDE.md section
       4.1b) -- and SOURCE-OVER only, so none of it reaches the bloom (4.1c). */
    if (__world) this.drawBenediction(m);
'''),

('benediction picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* --------------------------------------------- BENEDICTION'S PICTURE ---
     v82 section 4, drawn off the fighter's `bene*` fields -- never `m.ultFx`,
     one slot the opponent's cast takes (open item 25). A RING, NOT A DISC: a
     10-unit band at `haloR` (150, read off the relic, so the ring is where
     the sim's test is) in the school's glow at 0.4, 0.7 while a foe is inside
     -- the tell that the blessing is running -- with the hole cut in the
     path, a 0.04 wash inside it, and motes drifting in along it. The ring
     grows out of the ball over 0.3s at the cast and shrinks back into it at
     the close. WORLD pass, under both balls, source-over: nothing under
     `lighter` and nothing the bloom can see. One method a component, so each
     can be measured alone; nothing here keeps state or draws from the rng.
       drawBenediction  the pass: clipped to the live hall
       _beneGeom        the ring's radius and envelope this frame
       _beneWash        the 0.04 wash inside the band
       _beneRing        the band and its drawn falloff
       _beneMotes       the motes (the design's field, drawn)
       _beneRim         a foe inside wears a rim of the light */
  drawBenediction(m){
    const a = m.a, b = m.b;
    if (!(a.beneFade > 0) && !(b.beneFade > 0)) return;      // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    for (const f of [a, b]){
      if (!(f.beneFade > 0)) continue;
      const g = this._beneGeom(f);
      if (!(g.on > 0.004)) continue;
      this._beneWash(c, f, g);
      this._beneRing(c, f, g);
      this._beneMotes(c, m, f, g);
      this._beneRim(c, m, f, g);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* the radius (out of the shell at the cast, back into it at the close)
     and the envelope; `A` is the band's alpha this frame */
  _beneGeom(f){
    const R = CONFIG.physics.ballR, H = f.w.ult.haloR;
    const s = clamp(f.beneAge / 0.6, 0, 1), fade = f.beneFade;
    const k = Math.min(1 - (1 - s) * (1 - s), 1 - (1 - fade) * (1 - fade));
    const on = Math.min(1, s * 3) * Math.min(1, fade * 2);
    const rr = R + (H - R) * k;
    return { rr, k, on, A: (0.4 + (0.7 - 0.4) * f.beneLit) * on };
  }
  _beneWash(c, f, g){
    const r0 = g.rr - 5;
    if (!(r0 > 1)) return;
    c.globalAlpha = 0.04 * g.on;
    c.fillStyle = f.aff.glow;
    c.beginPath(); c.arc(f.x, f.y, r0, 0, TAU); c.fill();
  }
  /* THE BAND, flat at the design's alpha, THE HOLE CUT IN THE PATH (a radial
     gradient with an inner radius still fills its inner circle with
     colorStop(0) -- CLAUDE.md section 4.1b), and a drawn falloff either side
     of it in the school's core so it reads as light rather than a painted
     line: the bloom never sees any of it. */
  _beneRing(c, f, g){
    const x = f.x, y = f.y, r0 = Math.max(0, g.rr - 5), r1 = g.rr + 5;
    c.globalAlpha = g.A;
    c.fillStyle = f.aff.glow;
    c.beginPath();
    c.arc(x, y, r1, 0, TAU);
    if (r0 > 0) c.arc(x, y, r0, TAU, 0, true);             // the hole
    c.fill();
    const s0 = Math.max(0, r0 - 6), s1 = r1 + 6, sa = g.A * 0.12;
    c.globalAlpha = 1;
    const o = c.createRadialGradient(x, y, r1, x, y, s1);
    o.addColorStop(0, hexA(f.aff.core, sa)); o.addColorStop(1, hexA(f.aff.core, 0));
    c.fillStyle = o;
    c.beginPath(); c.arc(x, y, s1, 0, TAU); c.arc(x, y, r1, TAU, 0, true); c.fill();
    if (r0 > s0 + 0.5){
      const i = c.createRadialGradient(x, y, s0, x, y, r0);
      i.addColorStop(0, hexA(f.aff.core, 0)); i.addColorStop(1, hexA(f.aff.core, sa));
      c.fillStyle = i;
      c.beginPath(); c.arc(x, y, r0, 0, TAU);
      if (s0 > 0) c.arc(x, y, s0, TAU, 0, true);
      c.fill();
    }
  }
  /* MOTES DRIFTING IN ALONG THE RING (the design's field, drawn: a SPECS
     field fires once, at the cast, on the one ultFx slot, where the caster
     stood, and this ring rides her for 8s). Born just outside the band,
     drifting 30 units in and a little along it, fading in and out; placed by
     shellHash on the match clock (and the death clock after the kill), so
     they keep moving through a hit stop. No state, no rng. */
  _beneMotes(c, m, f, g){
    const T = m.t + (m.deathAge || 0), s = g.rr / f.w.ult.haloR, sd = f.side ? 8340 : 8300;
    c.fillStyle = f.aff.glow;
    for (let i = 0; i < 24; i++){
      const ph = (T * (0.32 + 0.3 * shellHash(sd, i)) + shellHash(sd + 1, i)) % 1;
      const q = TAU * shellHash(sd + 2, i) + ph * 0.3 * (shellHash(sd + 3, i) < 0.5 ? -1 : 1);
      const r = g.rr + (5 + 2 - ph * 30) * s;
      if (!(r > 1)) continue;
      c.globalAlpha = 0.8 * g.on * Math.sin(ph * Math.PI);
      c.beginPath();
      c.arc(f.x + Math.cos(q) * r, f.y + Math.sin(q) * r, 1.8 - 0.6 * ph, 0, TAU);
      c.fill();
    }
  }
  /* A FOE INSIDE WEARS A RIM OF THE LIGHT while the ring is bright. Drawn
     here, under its ball, from the shell outward with the hole cut at the
     shell: it can only ever be a rim, whatever the school (the white
     sanctified shell included), and a ball squashed by a blow shows the
     floor at its edge, not the light (measured: m1 had the hole at R - 1 and
     the rim showed +0.012 on a white foe's disc in a hit stop). */
  _beneRim(c, m, f, g){
    const foe = f === m.a ? m.b : m.a, L = f.beneLit * g.on;
    if (!(L > 0.01) || !foe.alive) return;
    const R = CONFIG.physics.ballR, x = foe.x, y = foe.y;
    const h = c.createRadialGradient(x, y, R, x, y, R + 7);
    h.addColorStop(0, hexA(f.aff.glow, 0.5 * L)); h.addColorStop(1, hexA(f.aff.glow, 0));
    c.globalAlpha = 1;
    c.fillStyle = h;
    c.beginPath(); c.arc(x, y, R + 7, 0, TAU); c.arc(x, y, R, TAU, 0, true); c.fill();
  }

  drawMotes(m){
'''),

("benediction picture: the beam's lit ground retired",
 '''    /* ---- Benediction: the lit ground under the blessing -------------------- */
    else if (u.w === "aureole"){
      const open = clamp((u.t - 0.06) / 0.24, 0, 1);
      const fade = 1 - clamp((u.t - 0.45) / 0.95, 0, 1);
      c.globalAlpha = 0.5 * fade * open;
      const g = c.createRadialGradient(u.tx, u.ty, 3, u.tx, u.ty, 150 * open);
      g.addColorStop(0, "#FFF6E2AA"); g.addColorStop(1, "#FFF6E200");
      c.fillStyle = g;
      c.beginPath(); c.ellipse(u.tx, u.ty, 150 * open, 62 * open, 0, 0, TAU); c.fill();
    }
''',
 '''    /* ---- Benediction's lit ground was the BEAM's (a 150-unit pool at the
       target for the cast's 1.6); retired with it (v82, v110 stage 6). The
       halo is `drawBenediction`, off the fighter, where the one ultFx slot
       cannot erase it; the cast's record now carries the CAST only and
       nothing draws from it. */
'''),

("benediction picture: the beam's lance retired",
 '''    /* ---- Benediction: sent OUT, not called down ---------------------------- */
    else if (u.w === "aureole"){
      const open = clamp((u.t - 0.06) / 0.20, 0, 1);
      const fade = 1 - clamp((u.t - 0.42) / 1.0, 0, 1);
      const dx = u.tx - u.x, dy = u.ty - u.y, L = Math.hypot(dx, dy) || 1;
      c.save();
      c.globalCompositeOperation = "lighter";
      /* the lance, along the shot line. Judgement falls vertically; a bow
         sends its blessing where it was aimed. */
      c.save();
      c.translate(u.x, u.y); c.rotate(Math.atan2(dy, dx));
      const w = 34 * open * (0.4 + 0.6 * fade);
      const g = c.createLinearGradient(0, -w, 0, w);
      g.addColorStop(0, "#FFF6E200"); g.addColorStop(0.5, "#FFFFFFCC");
      g.addColorStop(1, "#FFF6E200");
      c.fillStyle = g; c.globalAlpha = 0.55 * fade;
      /* THE LANCE STARTS AT THE SHELL, NOT AT THE CENTRE. It was drawn from
         (0,0) -- the caster's own middle -- as a `lighter` bar whose centre
         stop is #FFFFFFCC, so its first 34px sat on top of a sanctified body
         already near white. Same fault Daybreak's corona had, different
         shape: measured 0.506 bare -> 0.663 on the disc with 18.7% of it past
         0.98. The bar is otherwise unchanged -- same width, same gradient,
         same alpha, same length to the target. */
      const R0 = CONFIG.physics.ballR * 1.06;
      c.fillRect(R0, -w, Math.max(0, L * open - R0), w * 2);
      c.restore();
      /* halo rings opening at the target */
      for (let i = 0; i < 3; i++){
        const q = clamp(open * 1.2 - i * 0.18, 0, 1);
        if (q <= 0) continue;
        c.globalAlpha = fade * (1 - q * 0.6) * 0.9;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 3 - i * 0.6;
        c.shadowColor = "#FFF6E2"; c.shadowBlur = 16;
        c.beginPath(); c.arc(u.tx, u.ty, 26 + q * (58 + i * 30), 0, TAU); c.stroke();
        c.shadowBlur = 0;
      }
      /* the heal: rings CLOSING into the caster — Dawnbringer's motes rise,
         these contract, so the two sanctified heals do not read alike */
      for (let i = 0; i < 4; i++){
        const q = (u.t * 0.85 + i / 4) % 1;
        c.globalAlpha = (1 - q) * fade * 0.85;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 2.2;
        /* They CONTRACT INTO the caster, and they used to contract THROUGH
           it: r fell to 16 against a ball radius of 34, so the last third of
           every ring was stroked white across the body. Floored at the shell
           -- they now land ON it, which is the read the comment above always
           claimed. The outer radius is held at its old 90 so the gesture is
           the same size it was. */
        const rIn = CONFIG.physics.ballR * 1.06, rOut = 90;
        c.beginPath(); c.arc(src.x, src.y, rIn + (1 - q) * (rOut - rIn), 0, TAU);
        c.stroke();
      }
      c.restore();
    }
''',
 '''    /* ---- Benediction's lance and its rings were the BEAM's (sent out along
       the shot line, the heal's rings closing into the caster); retired with
       it (v82, v110 stage 6). The cast is the ring growing out of the ball
       (`drawBenediction`). */
'''),

('benediction picture: the charge rune',
 '''  /* BENEDICTION -- the halo, and the shaft through it. Heals, so the shaft
     grows DOWN into the frame rather than out of it. */
  aureole(c, t, cf, P){
    const g = c.createLinearGradient(0, -1, 0, 1);
    g.addColorStop(0, P.glow + "00"); g.addColorStop(0.5, P.glow);
    g.addColorStop(1, P.glow + "00");
    SG.a(c, 0.3 + cf * 0.55); c.fillStyle = g;
    c.fillRect(-0.17 - cf * 0.08, -1, 0.34 + cf * 0.16, 2); SG.a(c, 1);
    c.save(); c.scale(1, 0.36);
    SG.ring(c, 0, -1.5, 0.62, P.core, 0.16, 0.9);
    c.restore();
    for (let i = 0; i < 3; i++){
      const y = 0.9 - ((t * 0.5 + i / 3) % 1) * 1.7;
      SG.disc(c, 0, y, 0.06, P.glow, 0.5 * cf);
    }
  },
''',
 '''  /* BENEDICTION -- the halo stands round her. The beam's shaft went out with
     the beam (v82): a ring round the ball, brightening as the charge fills,
     the monstrance's six rays out of it, and motes drifting in along it to
     the ball. */
  aureole(c, t, cf, P){
    SG.spokes(c, 6, 0.74, 0.92, 0.3 + t * 0.12, P.core, 0.06, 0.25 + cf * 0.45);
    SG.ring(c, 0, 0, 0.62, P.glow, 0.13, 0.3 + cf * 0.6);
    SG.disc(c, 0, 0, 0.22, P.core, 0.55 + cf * 0.45);
    for (let i = 0; i < 5; i++){
      const ph = (t * 0.45 + i / 5) % 1, a = i * TAU / 5 + ph * 0.5;
      const r = 0.6 - ph * 0.3;
      SG.disc(c, Math.cos(a) * r, Math.sin(a) * r, 0.055, P.glow,
              (0.25 + 0.65 * cf) * Math.sin(ph * Math.PI));
    }
  },
'''),

("benediction picture: the cast record's life",
 '''aureole: 1.6, ''',
 ''''''),

]


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
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_array_ok(obj: str, ins: str) -> bool:
    """An array stage 6 may change: its own `bene*` ones, or a name its row
    binds once, as `const X = f.bene...;` (tickBenediction's S)."""
    if obj.startswith("bene"):
        return True
    bound = re.findall(r"\bconst " + re.escape(obj) + r" = \w+\.(bene\w+);", ins)
    decls = re.findall(r"\b(?:const|let|var)\s+" + re.escape(obj) + r"\b|[,(]\s*" + re.escape(obj)
                       + r"\s*=(?!=)|(?<![\w.$])" + re.escape(obj) + r"\s*=(?!=)", ins)
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
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickHalo|tickStatus|tickWeapon|tickFire|tickHits|spawnShot|note|checkEnd)\(", ins) \
                or re.search(r"(?<!SG)\.ring\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\b(beat|hurt|knock|shake|hitStop)\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' hurts, knocks, "
                             "stops or files a beat")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its voice alone:\n{ins}")
        elif "SFX" in ins or "voiceIn" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the entry, the heal and the close")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickBenediction")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\(", ins):
            if not s6_array_ok(mw.group(1), ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not s6_array_ok(mw.group(1).split(".")[-1], ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
        if re.search(r"\bdelete\s", ins):
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
    th = th[:th.find("\n  }\n")]
    i_v = th.find(S6_SIM_LINES["tickHalo: the entry note"][0])
    i_t = th.find(INSIDE_TEST.strip())
    if not 0 <= i_v < i_t or th[i_v:i_t].count("\n") != 3:
        raise SystemExit("REFUSING TO WRITE -- the entry's test is not the ticker's own, "
                         "repeated just before it in tickHalo")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickBenediction(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickBenediction does not follow tickNovaFx in "
                         "tickPresentation")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the entry, the heal chime and the close its three lines on the sim "
          "path); the inlined fx.js untouched; the rune-crack fallback kept; the beam's art "
          "gone; every arm, call and pass once")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--alt50", action="store_true",
                    help="stage 5 only: write Rick's other choice, 50%% (blade "
                         f"{ALT50_BLADE}); NOT the carry")
    A = ap.parse_args()
    if A.alt50 and A.stage != "5":
        raise SystemExit("--alt50 is stage 5's")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-aureole"):
        raise SystemExit(f"refusing {out_p.name}: this builder's links are sc-aureole*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: 02-chain already has a link of that name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    if A.stage == "5" and BLADE is None:
        raise SystemExit("stage 5: the blade is not measured yet (v110 §4)")

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nAUREOLE / BENEDICTION (REDESIGN) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The relic this builder redesigns, with its shipped
    # body; the engine's gates the halo pays through; the window clock.
    row = relic_row(code, RELIC)
    for need, why in (('aff:"sanctified", shape:"bow"', "Aureole is not the sanctified bow"),
                      ('mode:"ranged"', "Aureole is not ranged"),
                      ("onHit:{ smite:1 }", "Aureole does not carry the sanctified channel"),
                      ("shot:{ cadence:0.34,", "Aureole's shot has moved")):
        if need not in row:
            raise SystemExit(f"wrong base: {why}")
    for need, why in (("apply(key, n, src){", "no Fighter.apply(key, n, src)"),
                      ("get alive(){ return this.hp > 0; }", "no Fighter.alive"),
                      ("stacks(", "no Fighter.stacks"),
                      ("fireUlt(f, foe){", "no fireUlt")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'\n  smite:\s+\{ name:"Smite",\s+maxStacks:4, dur:3\.2, dps:1\.5,', code):
        raise SystemExit("wrong base: STATUS.smite is not the one priced (4 stacks, 3.2s, 1.5/s)")
    if not re.search(r'\n  blessing:\s+\{ name:"Blessing",\s+maxStacks:5, dur:6\.0, hps:1\.2,', code):
        raise SystemExit("wrong base: STATUS.blessing is not the one priced (5 stacks, 6s, 1.2/s)")
    if 'if (key === "blessing"){' not in code or "def.hps * st.stacks * dt" not in code:
        raise SystemExit("wrong base: tickStatus does not heal the blessing")
    # THE WINDOW CLOCK: a hit stop returns from step() before the window tickers.
    st = code[code.find("  step(dt){"):]
    hs = st.find("if (this.hitStop > 0){")
    tt = st.find("this.tickTendril(dt);")
    if tt < 0:
        raise SystemExit("wrong base: no `this.tickTendril(dt);` in step() -- the halo's ticker "
                         "goes after Tendril's (v68), so this is not the Tendril lineage")
    if hs < 0 or not hs < st.find("return;", hs) < tt:
        raise SystemExit("wrong base: the window tickers do not stop in a hit stop")
    if A.stage == "1":
        for name in NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")
        if 'kind:"halo"' in code or '"halo"' in code:
            raise SystemExit("the kind \"halo\" is already in the base")
        if s0.count(SHIPPED_ULT) != 1:
            raise SystemExit("wrong base: Aureole does not carry the shipped Benediction")
        if f"dmg:{SHIPPED_DMG}," not in row:
            raise SystemExit("wrong base: Aureole is not at its shipped blade")
        heals = [rid for rid, blk in ult_rows(code) if re.search(r"\bheal:", blk)]
        if heals != [RELIC]:
            raise SystemExit(f"wrong base: the ult blocks carrying `heal` are {heals}, not "
                             "Aureole's alone -- the beam's heal cannot be retired")
        if len(re.findall(r"\bu\.heal\b", code)) != 2 or s0.count(HEAL_BLOCK) != 1:
            raise SystemExit("wrong base: fireUlt's heal block is not the one this builder retires")
    print("  base  Aureole's shipped body (sanctified bow, ranged, smite 1, the shot); "
          "apply / stacks / STATUS.smite / STATUS.blessing and the blessing's heal; the "
          "window tickers stop in a hit stop")

    blade = SHIPPED_DMG
    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"halo"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if not free_name("tickHalo", code) or "charge:1e9" not in row:
                raise SystemExit("stage 2 goes on stage 1, once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if free_name("tickHalo", code) or "bless:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["bless"])
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
            if f'bless:{ULT["bless"]},' not in row or f"dmg:{SHIPPED_DMG}," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            blade = ALT50_BLADE if A.alt50 else BLADE
            edits = s5_edits(ALT50_BLADE) if A.alt50 else S5
            want = ult_block(ULT["charge"], ULT["bless"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Aureole's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:104]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if f"dmg:{blade}," not in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S5 + s5_edits(ALT50_BLADE) + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if re.search(r"\.(hurt|heal|resolveHit|shatter|knock|beat|spawnShot)\(", ins) \
                or re.search(r"\b(hitStop|pin|stun|vx|vy)\s*(=[^=]|\+=|-=)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' hurts, moves, "
                             "stops or files a beat (v82 §4: no damage, no knock, no beat)")
    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    if len(re.findall(r'kind:"halo"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one halo ultimate")
    if 'kind:"beam", dmg:15, heal:28' in out_code or re.search(r"\bu\.heal\b", out_code):
        raise SystemExit("REFUSING TO WRITE -- the beam is still here")
    if any(re.search(r"\bheal:", b) for _r, b in ult_rows(out_code)):
        raise SystemExit("REFUSING TO WRITE -- an ult block still carries `heal`, which "
                         "nothing reads now")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one halo ultimate, Aureole's; the beam out; no insert draws the RNG, "
          f"writes the shared weapon, hurts, moves or files a beat; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
