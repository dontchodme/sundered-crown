#!/usr/bin/env python
"""LODESTONE / REBUTTAL -- the runic warhammer, a NEW relic. v102.

Built from `06-docs/v70/LODESTONE-BUILD-BRIEF.md` and
`runic-warhammer-design-v70.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-lodestone.html
    stage 2   the hex on touch, no hurl   -> sc-lodestone-runes.html     (arm H)
    stage 3   the hurl                    -> sc-lodestone-rebuttal.html  (arm C)
    stage 4   (none: the brief has three stages)
    stage 5   the blade                   -> sc-lodestone-b205.html      (20.5)
    stage 6   picture, voice              -> sc-lodestone-b205-fx.html
              (on the final; no field: the rune motes are drawn, reading 14)

§1: "For a duration the four walls of the hall are runed. Every time the
enemy's ball touches a wall the rune under it flares, hexes them, and hurls
them straight back at the hammer. The hammer's own knock throws them into the
wall in the first place, so the fight becomes a rally: hit, wall, hurled back,
hit. The walls do no damage -- they hand the enemy back."

Declared (design §5, brief §0-§1):
  THE WINDOW  8s; `f.ultRunes = {t, dur, cd}`, null elsewhere. The brief's
              §1 gives the state as `{ t0, end, cd }`, which reads as
              timestamps; on this engine a timestamp sits on `m.t`, which runs
              through hit stops, so that shape IS the lab's clock (8
              match-seconds). It is built as `{t, dur, cd}`, `t` counted on the
              window tickers' clock -- the batch's standing ruling (THE CLOCK,
              below); v102 §2's lab-clock control prices the difference.
  A TOUCH     the foe's centre within inset + R + 1.5 of any side (the CURRENT
              inset: the runes walk in with the seals), the foe alive and not
              pinned, once per 0.5s. The engine clamps a ball at n + R, so this
              is a contact test, not a proximity one.
  THE HEX     foe.apply("hex", 1, side) per touch, the real status.
  THE HURL    foe.vx, vy = 700 x unit(caster - foe) -- an ASSIGNMENT, not an
              impulse. No damage, no resolveHit, no beat, no hit stop. Nothing
              writes f.stun or f.pin.
  The caster's own touches do nothing. The next cast waits for nothing.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm C (v102 §0, the census).

THE READINGS, where the build had to choose and the doc, the lab or the engine
decides:
  1. THE WINDOW CLOSES ON THE CLOCK OR EITHER DEATH (the lab closes on either
     death; the design is silent). A dead foe cannot touch anything, and a dead
     caster's runes hand the foe back to nobody. ON THIS ENGINE THE FOE-DEATH
     CLOSE IS UNREACHABLE: the only thing Lodestone does that can kill is a
     blow, in `tickHits`, after `tickRunes`; that step's `checkEnd` ends the
     match and `step` returns early from then on, so `tickRunes` never runs
     again. A kill by a blow therefore ENDS THE MATCH WITH `ultRunes` STILL SET
     (the lab closed on `m.over` as well). The simulation never reads it after
     the verdict; a picture must gate on `!m.over` (v102 §5). Kept as the lab's
     reading; the probe counts caster-death and foe-death closes apart.
  2. THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, touching or not, and starts
     clear at the cast (the lab's `cd = 0` at onCast; `cd -= dt` every window
     frame), so a foe already on a wall is touched on the first frame. ONE
     FRAME: `Z.t += dt` comes before the close test, so the cast step's own
     tick is window frame 1 and the 960th tick closes the window -- 959
     working frames where the lab's window is open for 960, 1/120s short on
     the window clock. Nothing measurable moves with it (v102 §0).
  3. A PINNED FOE IS NOT TOUCHED, and its frames still spend the cooldown
     (the lab's `cd -= dt` comes before its pin test and its return).
  4. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract, Rick's ruling);
     the lab passed the Fighter. Hex reads no source (no dps, no feed).
  5. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).
  6. THE HURL IS ASSIGNED ON THE WINDOW FRAME OF THE TOUCH, in the window
     tickers' slot (after `ballCollision`, before `tickHits`): a blow landing on
     that same frame knocks on top of the hurl. The lab assigned after the
     whole step, over the blow's knock. v102 §2 prices the order.
  7. THE HAMMER IS GRUDGEBEARER'S PROFILE AND ITS BLADE, 23.5, until stage 5
     (the lab's donor, `cell_ults_on.TYPE_DONOR`, and every shipped hammer's
     profile); the school's channel, onHit hex 1.
  8. THE BLURB is COMPOSED BY THE BUILD, not a quoted line: the batch's
     "A <type> that ..." pattern (Canopy's, Onslaught's, Tendril's builds did
     the same), from §1's words, "hurls them straight back at the hammer".
     The design's title line reads "The walls are runed: whoever touches one
     is hexed and hurled back at the hammer"; the card (68) is the brief's.

STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
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
which stops through a hit stop (Corollary's, Daybreak's, Zenith's, Canopy's,
Onslaught's and Tendril's convention). The lab ran both through freezes, and
touched walls during them; v102 §2 measures what that is worth here.

THE BASE is asserted BY CONTENT: the window tickers' slot after Tendril's, the
anchors this builder needs, the donor's hammer profile, the runic channel, the
runic hammer head's route, hex's numbers and the wall clamp at n + R. It never
asserts which relic is last, so it re-applies on a tip that carries more.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "lodestone"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v102 §0)
    "dur": 8,         # "the window 8s every 16s"
    "pad": 1.5,       # "foe centre within inset + R + 1.5 on any side"
    "cd": 0.5,        # "once per 0.5s"
    "hex": 1,         # "apply("hex", 1, f)"
    "hurl": 700,      # "foe.vx, vy = 700 x unit(caster - foe)" -- stage 3
}
TIP = "The walls are runed: a foe that touches one is hexed and hurled back"
# Grudgebearer's hammer profile, the lab's donor (cell_ults_on.TYPE_DONOR) and
# the whole type's; dmg 23.5 is its blade, which stage 5 settles.
DONOR_PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.50, spin:1.6, '
              'mode:"spin", mass:5.0, knockMul:2.3')
PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.5, spin:1.6, '
        'mode:"spin", mass:5.0, knockMul:2.3')
HAMMERS = ("grudgebearer", "censer", "bulwarden", "shroudmaul", "ravelbone")
RUNIC = ("spellbreaker", "axiom", "foregone", "paradox")
BLURB = ("A hammer that runes the hall: whoever touches a wall is hexed and "
         "hurled straight back at the hammer.")
HEX_DEF = 'hex:        { name:"Hex",        maxStacks:5, dur:2.6, stunEvery:1.15, stunFor:0.20,'
CLAMP = "    const loX = n + R, hiX = A.w - n - R, loY = n + R, hiY = A.h - n - R;\n"
# The names this relic adds; each must be free on the base.
NAMES = ("ultRunes", "runeTally", "tickRunes", 'kind:"runes"', 'id:"lodestone"')


def ult_block(charge, hurl) -> str:
    return (f'''    ult:{{ name:"Rebuttal", charge:{charge}, kind:"runes", dur:{ULT["dur"]},
          pad:{ULT["pad"]}, cd:{ULT["cd"]}, hex:{ULT["hex"]},
          hurl:{hurl},          // v70: the hurl (stage 3)
          tip:"{TIP}" }},''')


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
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
        return
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
# THE RELIC, APPENDED AT THE END OF THE WEAPONS ARRAY, ITS ULTIMATE STUBBED at
# charge 1e9 (the clock can never reach it, `fireUlt` never runs) --
# Starwarden's stage-1 pattern. The anchor is the array's closing and the
# comment under it, which names no relic, so a row another build appends first
# still leaves it in place. Every other table keyed by relic id falls back, and
# SHAPES.warhammer already routes runic to `_whConjured`, which no shipped
# relic has drawn.
ROW_ANCHOR = '\n\n];\n/* The single source of truth for "which status does this relic teach".'

S1 = [

("lodestone joins the roster at the end of the array, its ultimate stubbed",
 ROW_ANCHOR,
 f'''

  /* LODESTONE / REBUTTAL (v70; built v102) -- THE RUNIC WARHAMMER. A new
     relic. Grudgebearer's hammer profile (the lab's donor and the whole
     type's) on the donor's blade until stage 5 settles its own; the school's
     channel, onHit hex 1. The ultimate is stubbed at stage 1 (charge 1e9);
     stages 2-3 give it its runed walls and their hex, then the hurl. */
  {{ id:"{RELIC}", name:"Lodestone", aff:"runic", shape:"warhammer",
    {PHYS},
    onHit:{{ hex:1 }},
{ult_block("1e9", 0)}
    blurb:"{BLURB}" }},''' + ROW_ANCHOR),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the runes have a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Rebuttal", charge:1e9, kind:"runes", dur:8,
''',
 f'''    ult:{{ name:"Rebuttal", charge:{ULT["charge"]}, kind:"runes", dur:{ULT["dur"]},   // v70 stage 2: the walls are runed
'''),

("the fighter carries the runed walls",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd} while LODESTONE's walls are runed (v70). null on every
       other relic and on this one outside its window: `tickRunes` returns
       after a two-iteration loop that does nothing. `runeTally` is the
       probe's count, cumulative over the fight; nothing in the simulation
       reads it. */
    this.ultRunes = null;
    this.runeTally = null;
'''),

("the cast runes the walls and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "runes"){
      /* REBUTTAL (v70). NOTHING RESOLVES HERE: the cast runes the four walls
         for `u.dur` seconds and `tickRunes` does everything the window does.
         `cd` starts at zero, so a foe already on a wall is touched on the
         first frame (the lab's). */
      f.ultRunes = { t: 0, dur: u.dur, cd: 0 };
      if (!f.runeTally)
        f.runeTally = { casts: 0, frames: 0, touches: 0, hexes: 0, hurls: 0,
                        foeStk: 0 };
      f.runeTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the runes tick with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickRunes(dt);                 // REBUTTAL (v70)
'''),

("tickRunes touches, hexes and hurls",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE RUNES =======
     v70 §1 / §5, brief §0-§1. While the window runs the four walls are
     runed, on the CURRENT inset (they walk in with the seals):
       A TOUCH   the foe's centre within inset + R + pad of any side, the foe
                 alive and not pinned, the cooldown clear. The engine clamps a
                 ball at n + R, so this is contact. Once per `cd`; the
                 cooldown runs through the whole window, touching or not.
       THE HEX   apply("hex", hex) on the foe, the real status, by side letter.
       THE HURL  the foe's velocity ASSIGNED to hurl x unit(caster - foe):
                 the wall answers with its own throw; `move` spends it next
                 step. Not an impulse.
     No damage, no resolveHit, no beat, no hit stop; nothing writes stun or
     pin. The caster's own touches do nothing, and the target is the OPPONENT
     only. The window closes on its clock or either death. On the window
     tickers' clock, so all of it freezes through a hit stop. */
  tickRunes(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultRunes;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }
      const u = f.w.ult, T = f.runeTally;
      T.frames++;
      T.foeStk += foe.stacks("hex");
      Z.cd -= dt;
      if (foe.pin > 0 || Z.cd > 0) continue;
      const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset, e = u.pad;
      if (!(foe.x <= n + R + e || foe.x >= A.w - n - R - e ||
            foe.y <= n + R + e || foe.y >= A.h - n - R - e)) continue;
      Z.cd = u.cd;
      T.touches++;
      if (u.hurl > 0){
        const dx = f.x - foe.x, dy = f.y - foe.y, d = Math.hypot(dx, dy) || 1;
        foe.vx = dx / d * u.hurl;
        foe.vy = dy / d * u.hurl;
        T.hurls++;
      }
      if (u.hex > 0){
        foe.apply("hex", u.hex, f === this.a ? "a" : "b");
        T.hexes += u.hex;
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the hurl",
 '''          hurl:0,          // v70: the hurl (stage 3)
''',
 f'''          hurl:{ULT["hurl"]},          // v70: the hurl (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief header: "The build owns the blade"; brief §2 stage 5:
# "Wide, both sides, two blocks, 21 / 22 / 23 on 151. Expect 21.5-22."; the
# v87 handoff: every design blade is a bracket, and every build settles its
# blade wide, both sides, two blocks, on 151). Both sides, two blocks, 1520
# fights a point (relic_rate, 38 foes; v102 §4): 19 -> 43.4, 20 -> 45.3,
# 20.5 -> 49.0, 21 -> 53.9, 21.5 -> 53.6, 22 -> 54.0, 23 -> 57.2,
# 23.5 -> 57.8 (the integers first; 20.5, 21.5 and 23.5 added after an
# earlier cut had picked 21 -- v102 §4 says the order).
# THE CRITERION THAT PICKS IT: the measured point whose POOLED RATE IS
# NEAREST 50% -- 20.5 at 49.0% (0.8 SE under) against 21's 53.9% (3.0 SE
# over); the two points that bracket 50% cross, locally, at about 20.6.
# BY BLADE DISTANCE TO A FITTED LINE IT IS 21: a line through all eight
# crosses at 20.78 (3.36 points a damage point), 0.22 from 21 and 0.28 from
# 20.5, and predicts 50.7% at 21 and 49.0% at 20.5 (v100 and v101 wrote "the
# measured point nearest the crossing"; there both criteria picked the same
# blade, here they part). The curve is not a line -- flat from 21 to 22,
# the hammer's kill steps; the eight points scatter 1.7 points around the fit
# against a 1.3 binomial SE -- so the build reads the measured rates and
# puts 20.5 against 21 to Rick (v102 §6). Above Bulwarden's 20.1, the
# design's row floor. The brief's forecast, 21.5-22, is where the LAB crosses
# on 151 (50.4% at 21.5); the built relic reads 53.6% there, the window
# clock's +4 (v102 §2, §4). No knob moves: the brief names none (§3 closes
# the hurl speed, the cadence and the bite).
BLADE = 20.5

S5 = [
("the blade: the measured point whose pooled rate is nearest 50%",
 '''  { id:"lodestone", name:"Lodestone", aff:"runic", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:23.5,''',
 f'''  {{ id:"lodestone", name:"Lodestone", aff:"runic", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:{BLADE},'''),
]


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v70 §6.1-6.2, brief stage 6), picked on
# measurements under Rick's "you pick i overrule" by `lodestone_voice_lab.py`
# and the picture lab (v102 §5). Presentation only: engine_ab over all 39
# relics, Lodestone included, is the proof. The rows are byte-exact to the
# labs' own files (voice 3, picture 9; no two share an anchor, so none is
# merged); the picture rows alone reproduce the picture lab's stamp
# (b40d52b7561c45f2) on sc-lodestone-b205, the voice rows alone the voice lab's
# voice page (8921a39052799d17). Voice first, then picture; the other order
# writes the same bytes.
#   THE VOICE: the cast (fireUlt's own `ult`/lodestone call, which fell
#   through to rune-crack: EVEN, a rising four-note chime), a touch (in
#   tickRunes, after its hex, pitched by the foe's count: ARC3, with the
#   school's `hex-snap` under it) and the close (in tickRunes, on a clock
#   close with both alive, before the close line: MIRROR, the chime
#   reversed). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickLode` in tickPresentation reads `ultRunes && !over &&
#   alive` and `runeTally.touches` rising, and writes only its own `lode*`
#   fields, a record's clock and path, a tag's count, `tags` (statusTag)
#   and `taught`. The rune chain lights along the live hall's four walls
#   from the caster's nearest wall (0.3s) and sheds 28 motes; a touch
#   flares the wall's 60-unit span (0.15s), snaps a bar from the wall into
#   the ball for one frame and trails a rune-streak off the hurled ball;
#   the HEX tag prints the foe's count; the head burns its sigil while the
#   walls are lit; the close runs dark from the far wall inward (0.4s), or
#   all at once on the caster's fall. The runic warhammer's route
#   (`_whConjured`, drawn by no relic before this one) becomes the design's
#   square head on a dark haft. No beat, no stop, no fx.js edit: the
#   design's field is drawn (reading 14); SPECS has no Lodestone entry.
#   NAMES: the labs'. `drawLode` is a prefix of `drawLodeTop`, and `tickRunes`
#   of nothing new, so every stage-6 name check below is on identifier
#   boundaries.
S6 = [

("Sfx: Lodestone's cast, touch and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "lodestone"){                  // the walls are runed
          /* LODESTONE'S CAST, THE WALLS RUNED -- v70 §6.2: "a rising four-note
             rune chime, one per wall, 0.5s total". EVEN, of 5, picked on the
             numbers by `lodestone_voice_lab.py` under Rick's "you pick i
             overrule" (v102). Lodestone had no arm and fell through to
             rune-crack, which 12 other relics on its stage-5 link still use,
             so this ADDS arms before that fallback and leaves it alone.

             One note a wall: A C E A, the score's tonic triad up through its
             octave, from A4, each note a free bar's modes (a triangle and
             sines at 2.76x and 5.40x, the upper decaying faster), a note every
             125 ms, each struck (rise 0 ms) and each jumping 32 dB or more in
             its own band at its onset. Audible 495 ms; its loudest 50 ms -2.9
             dB re Lodestone's blow; +22.4 dB over the score where a phone
             hears it. Register at most 0.66 against rune-crack, the runic and
             warhammer casts, the seal's chime, Zenith's cast and the blow. */
          const g = 0.1906, D = 0.228;
          [0, 3, 7, 12].forEach((s, k) => {
            const f = 440 * Math.pow(2, s / 12), tk = t + k * 0.125;
            this._tone(tk, { freq: f, gain: g, dur: D, type:"triangle" });
            this._tone(tk, { freq: f * 2.76, gain: g * 0.35, dur: D * 0.5, type:"sine" });
            this._tone(tk, { freq: f * 5.4, gain: g * 0.12, dur: D * 0.25, type:"sine" });
          });
        } else if (w === "lodestone-touch"){            // a wall answers
          /* A WALL ANSWERS -- "a sharp electric snap (<=80ms, peak <=0.5) with
             the hex's own stun voice underneath if it lands; pitch steps up
             with the stack count" (v70 §6.2). ARC3, of 7
             (`lodestone_voice_lab.py`). `tickRunes` plays it once per touch,
             after the hex lands, with n = the foe's hex count (the tag's
             number, 1-5), and `hex-snap` under it.

             A 12 ms highpass crack (the spark) on a held square at the count's
             note, low -- an arc's buzz, its partials clear of the hex-snap's
             2.6 kHz. The note steps up the A-minor pentatonic with the count,
             220 / 262 / 294 / 330 / 392 Hz at 1-5 (measured 218 / 260 / 292 /
             329 / 391 Hz, every step 201 cents or more). Rise under 1 ms; gone
             by 60 ms and peak 0.424 at most, at every count and draw; its
             harmonics -7.5 dB re its note (a buzz); its loudest 50 ms -3.9 to
             -3.4 dB re the blow and +6.3 dB or more over the hex-snap, which
             still stands +4.6 dB or more over it at 2.6 kHz. Register at most
             0.43 against the hex-snap, the wall tick, the blow, rune-crack,
             the clank, the burn and the cast. */
          const n = clamp(Math.round(p.n || 1), 1, 5), f = 220 * Math.pow(2, [0, 3, 5, 7, 10][n - 1] / 12), g = 0.1946, D = 0.1;
          this._burst(t, { freq: 6000, q: 0.7, gain: g * 0.5, dur: 0.012, type:"highpass" });
          this._tone(t, { freq: f, gain: g, dur: D, type:"square" }).frequency.value = f;
        } else if (w === "lodestone-close"){            // and the runes go dark
          /* THE RUNES GO DARK -- "the chime reversed, quiet" (v70 §6.2).
             MIRROR, of 4 (`lodestone_voice_lab.py`): the cast's four notes,
             each RE-STRUCK every whole number of cycles nearest 11 ms (in
             phase: `.frequency.value = f`, v97 §4b) at a level climbing as the
             cast's own decay reversed, each cut at its mirrored onset -- all
             four swell and drop out from the top down, the root last. -9.0 dB
             under the cast's top; gone 685 ms after the window shuts. Envelope
             correlation 0.93 with the literal reversal, which cannot ship: it
             needs an async render, and every clip rebuilds this synth
             synchronously (v88 §6b). `tickRunes` plays it only when the window
             closes by its clock with both fighters alive, never on a death and
             never at the verdict. */
          const top = 0.040788, D = 0.228, A = -65.602;
          [0, 3, 7, 12].forEach((s, k) => {
            const f = 440 * Math.pow(2, s / 12), c = 0.375 + D - k * 0.125;
            const dt = Math.max(1, Math.round(f * 0.011)) / f;
            const s0 = Math.max(0, c - D * 40 / -A);
            for (let j = Math.ceil(s0 / dt); j * dt < c - 1e-9; j++){
              const u = c - j * dt;
              this._tone(t + j * dt, { freq: f, gain: top * Math.pow(10, A * u / D / 20), dur: 0.1, type:"triangle" }).frequency.value = f;
              this._tone(t + j * dt, { freq: f * 2.76, gain: top * 0.35 * Math.pow(10, A * u / (D * 0.5) / 20), dur: 0.1, type:"sine" }).frequency.value = f * 2.76;
              this._tone(t + j * dt, { freq: f * 5.4, gain: top * 0.12 * Math.pow(10, A * u / (D * 0.25) / 20), dur: 0.1, type:"sine" }).frequency.value = f * 5.4;
            }
          });
        } else {                                        // rune-crack'''),

('tickRunes: the touch voice and the hex-snap under it, once per touch, after its hex',
 '''        T.hexes += u.hex;''',
 '''        T.hexes += u.hex;
        /* REBUTTAL'S TOUCH (v70 §6.2: "a sharp electric snap (<=80ms, peak
           <=0.5) with the hex's own stun voice underneath if it lands; pitch
           steps up with the stack count"): once per touch, after its hex
           lands, pitched by the count the foe now carries (the tag's number,
           1-5; at the cap the hex's clock refreshes and it snaps at 5's
           note), and under it the hex's own voice, `hex-snap` -- the runic
           school's, the one Corollary's echo plays when its hex lands.
           Presentation only: SFX.play draws nothing, is a no-op headless,
           and nothing here is read back (lodestone_voice_lab: fights
           identical). */
        SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });
        SFX.play("hex-snap");'''),

('tickRunes: the close, when the window runs out by its clock with both fighters alive',
 '''      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }''',
 '''      /* REBUTTAL'S CLOSE (v70 §6.2: "the chime reversed, quiet"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive --
         never on a death, and never once the fight is over (step() stops
         calling this after a kill, so a window still lit at the verdict
         plays nothing). Presentation only; nothing here is read back. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lodestone-close" });
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }'''),

('rebuttal picture: fighter fields',
 '''    this.ultRunes = null;
    this.runeTally = null;
''',
 '''    this.ultRunes = null;
    this.runeTally = null;
    /* REBUTTAL'S PICTURE (v70 section 6.1), and none of it is the sim's: the
       walls go dark for 0.4s after `ultRunes` is gone (and `ultRunes` itself
       stays set through the verdict when a blow ends the match), and a
       touch's flare, bar and streak outlive the frame that touched, so the
       picture keeps its own state. On the FIGHTER and never on `m.ultFx`
       (one slot, and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation` (`tickLode`); nothing in the simulation reads any
       of it.
         lodeFade -- 1 while the walls are lit; eased to 0 as they go dark
         lodeAge  -- the presentation clock since the cast (the chain lights)
         lodeOut  -- the presentation clock since the close (the go-dark)
         lodeDie  -- 1 when the close was the caster's fall (all out at once)
         lodeU0   -- where the chain lit from: the caster's nearest wall at
                     the cast, as a fraction of the hall's loop (`lodeAt`)
         lodeU1   -- the same at the close: the dark runs from the far side
         lodeSeen -- `runeTally.touches` as last seen (a rise is a touch)
         lodeFx   -- a touch: its walls, its spot, the match time (the bar),
                     the hurled ball's path (the streak) */
    this.lodeFade = 0;
    this.lodeAge = 0;
    this.lodeOut = 0;
    this.lodeDie = 0;
    this.lodeU0 = 0;
    this.lodeU1 = 0;
    this.lodeSeen = 0;
    this.lodeFx = [];
'''),

('rebuttal picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickLode(dt);                  // REBUTTAL'S PICTURE (v70 section 6.1)
'''),

("rebuttal picture: the hall's loop",
 '''function shellHash(a, b){
''',
 '''/* REBUTTAL'S WALLS (v70 section 6.1): the live hall's four walls as one loop,
   clockwise from the top-left corner; `u` is a fraction of its length. The
   hall is the CURRENT one (`m.inset`), so the runes walk in with the seals.
   Read by `tickLode` (where the caster stands at the cast and the close, and
   which walls a touch met) and by the renderer (where each rune sits). Pure
   functions of their arguments; nothing in the simulation calls them. */
function lodeHall(n){
  const A = CONFIG.arena, x0 = n, y0 = n, x1 = A.w - n, y1 = A.h - n;
  return { x0, y0, x1, y1, w: x1 - x0, h: y1 - y0, P: 2 * ((x1 - x0) + (y1 - y0)) };
}
/* -> [x, y, inward nx, ny, wall]: wall 0 the top, 1 the right, 2 the floor, 3 the left */
function lodeAt(G, u){
  let s = (((u % 1) + 1) % 1) * G.P;
  if (s < G.w) return [G.x0 + s, G.y0, 0, 1, 0];
  s -= G.w; if (s < G.h) return [G.x1, G.y0 + s, -1, 0, 1];
  s -= G.h; if (s < G.w) return [G.x1 - s, G.y1, 0, -1, 2];
  s -= G.w; return [G.x0, G.y1 - s, 1, 0, 3];
}
/* the point of `wall` level with (x, y), as u */
function lodeOn(G, wall, x, y){
  const cx = Math.min(G.x1, Math.max(G.x0, x)), cy = Math.min(G.y1, Math.max(G.y0, y));
  const s = wall === 0 ? cx - G.x0 : wall === 1 ? G.w + (cy - G.y0)
          : wall === 2 ? G.w + G.h + (G.x1 - cx) : 2 * G.w + G.h + (G.y1 - cy);
  return s / G.P;
}
/* the wall nearest (x, y) */
function lodeNear(G, x, y){
  const d = [y - G.y0, G.x1 - x, G.y1 - y, x - G.x0];
  let k = 0;
  for (let i = 1; i < 4; i++) if (d[i] < d[k]) k = i;
  return lodeOn(G, k, x, y);
}

function shellHash(a, b){
'''),

('rebuttal picture: tickLode',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------------ REBUTTAL'S PICTURE ---
     v70 section 6.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.6 is the
     cast's 0.3s draw along the walls, 0.8 the close's 0.4s go-dark, 0.3
     a touch's 0.15s flare. The bar is timed on the MATCH clock (`t0`): it
     stands for the touch's step and the next -- one frame of a 60 fps
     picture -- and a hit stop that begins under it does not hold it.
     A TOUCH IS FOUND BY WATCHING `runeTally.touches` RISE, so `tickRunes`
     makes no call and keeps no record for the picture: this runs at the end
     of the step that touched (decay, after `checkEnd`), nothing between the
     touch test and here moves a ball, so the foe stands where the test found
     it, and the walls it met are the test's own sides read again (inset + R
     + pad; a corner meets two). THE WALLS ARE READ OFF `ultRunes && !over &&
     alive`: `tickRunes` never runs again once `over` is set and a blow's kill
     leaves `ultRunes` set through the verdict (v102 section 5), so the walls
     go dark at the kill -- from the far wall inward, or all at once when the
     caster is the one that fell. Writes presentation fields, `tags` and
     `taught` only, and draws no rng. */
  tickLode(dt){
    for (const f of [this.a, this.b]){
      const T = f.runeTally;
      if (!T && !(f.lodeFade > 0)) continue;                   // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      for (let i = f.lodeFx.length - 1; i >= 0; i--){
        const q = f.lodeFx[i];
        q.t += dt;
        if (q.t >= 0.8){ f.lodeFx.splice(i, 1); continue; }
        /* the hurled ball's path, for the streak */
        const n = q.pts.length;
        if (foe.alive && q.t < 0.8 && n < 96
            && (foe.x !== q.pts[n - 3] || foe.y !== q.pts[n - 2])) q.pts.push(foe.x, foe.y, q.t);
      }
      const Z = (this.over || !f.alive) ? null : f.ultRunes;
      if (Z){
        if (!(f.lodeFade > 0) || f.lodeOut > 0){                 // a cast: the chain lights
          f.lodeAge = 0; f.lodeOut = 0; f.lodeDie = 0;
          f.lodeU0 = lodeNear(lodeHall(this.inset || 0), f.x, f.y);
        }
        f.lodeFade = 1;
        f.lodeAge += dt;
      } else if (f.lodeFade > 0){
        if (!(f.lodeOut > 0)){                                   // the close
          f.lodeU1 = lodeNear(lodeHall(this.inset || 0), f.x, f.y);
          f.lodeDie = f.alive ? 0 : 1;
        }
        f.lodeOut += dt;
        f.lodeFade = Math.max(0, 1 - f.lodeOut / (f.lodeDie ? 0.2 : 0.8));
      }
      if (!T) continue;
      if (T.touches > f.lodeSeen){
        f.lodeSeen = T.touches;
        /* THE TOUCH. Not on the kill's step: the shatter owns that frame. */
        if (this.over || !foe.alive) continue;
        const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset || 0, e = f.w.ult.pad;
        const G = lodeHall(n), walls = [];
        if (foe.y <= n + R + e)       walls.push(0);
        if (foe.x >= A.w - n - R - e) walls.push(1);
        if (foe.y >= A.h - n - R - e) walls.push(2);
        if (foe.x <= n + R + e)       walls.push(3);
        f.lodeFx.push({ k: T.touches, walls, x: foe.x, y: foe.y, t: 0, t0: this.t, pts: [foe.x, foe.y, 0] });
        if (f.lodeFx.length > 6) f.lodeFx.shift();
        /* THE HEX TAG WITH ITS COUNT (v70 6.1: "the hex tag on the foe prints
           its count"), on every touch. ONE HEX TAG ON THE FOE AT A TIME
           (Tendril's rule): the hammer's own blow tags hex too (`resolveHit`),
           so a tag already up there takes the new count in place instead of
           a second printing over it. */
        if (foe.hp > 0){
          const k = foe.stacks("hex");
          const g = this.tags.find(g2 => g2.key === "hex" && !g2.first && g2.life > 0.3
                                         && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
          if (g) g.val = k;
          else {
            const first = !this.taught.hex && !!STATUS.hex.tip;
            if (first) this.taught.hex = true;
            this.statusTag(foe.x, foe.y, "hex", first, k);
          }
        }
      }
    }
  }

  tickWinnow(dt){
'''),

('rebuttal picture: the world call (under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* REBUTTAL'S WALLS (v70 section 6.1): the rune chain on the live hall's
       walls, its motes, a touch's flare and the hurled ball's rune-streak.
       The WORLD pass and under both balls -- a ball on a wall stands on the
       runes it touched (CLAUDE.md section 4.1b), and none of it reaches the
       bloom (section 4.1c). */
    if (__world) this.drawLode(m);
'''),

('rebuttal picture: the world call (over both fighters)',
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* REBUTTAL'S BAR, over both fighters: it snaps from the wall INTO the
       ball it hexes. World pass, one frame. */
    this.drawLodeTop(m);
'''),

("rebuttal picture: the head's rune in drawWeapon",
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
''',
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
      /* REBUTTAL (v70 section 6.1): the hammer's head carries a rune while
         the walls are lit, in the shape's own frame, over the shape. Zero on
         every other relic, so this is a comparison on a field nothing else
         writes. */
      if (f.lodeFade > 0) this._lodeHead(f, reach + 6);
'''),

('rebuttal picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------ REBUTTAL'S PICTURE ---
     v70 section 6.1. THE WALLS: a rune chain on the live hall's four walls
     (the school's core on the wall line, 12 runes on the top and the floor
     and 18 down each side, 12 units in, so a ball touching a wall
     stands on them). THE CAST lights it outward from the caster's nearest
     wall over 0.3s -- the near wall, the two beside it, the far one last --
     and it stays lit for the window, shedding rune motes (the design's
     field, drawn: `fx.js` fires once, at the cast, on the one ultFx slot).
     A TOUCH flares the 60-unit span of wall under the foe in the glow for
     0.15s, a bar snaps from the wall into the ball for one frame, and the
     ball leaves on a rune-streak. THE CLOSE runs dark from the far wall
     inward over 0.4s; the caster's fall puts it out at once.
     No new object in the hall: everything is on the walls or the foe. The
     WORLD pass, source-over; no rng, no spawnFx, no Math.random. */
  drawLode(m){
    for (const f of [m.a, m.b]){
      if (!(f.lodeFade > 0) && !(f.lodeFx && f.lodeFx.length)) continue;   // <- zero burden
      const G = lodeHall(m.inset || 0), P = f.aff;
      if (f.lodeFade > 0){ this._lodeWalls(m, f, G, P); this._lodeMotes(m, f, G, P); }
      if (f.lodeFx.length){ this._lodeFlare(m, f, G, P); this._lodeStreak(m, f, P); }
    }
  }

  drawLodeTop(m){
    for (const f of [m.a, m.b]){
      if (!(f.lodeFx && f.lodeFx.length)) continue;                         // <- zero burden
      this._lodeBolt(m, f, lodeHall(m.inset || 0), f.aff);
    }
  }

  /* How lit the rune at `u` is: the cast's front runs out from `lodeU0` both
     ways round the loop, the close's runs back from the far side to `lodeU1`,
     each with a soft edge 2% of the loop long. */
  _lodeLit(f, u){
    if (f.lodeOut > 0){
      if (f.lodeDie) return f.lodeFade;
      const d = Math.abs(u - f.lodeU1), dd = Math.min(d, 1 - d);
      const front = 0.52 * (1 - Math.min(1, f.lodeOut / 0.8));
      return clamp((front - dd) / 0.02, 0, 1);
    }
    const k = Math.min(1, f.lodeAge / 0.6), front = 0.52 * (1 - (1 - k) * (1 - k));
    const d = Math.abs(u - f.lodeU0), dd = Math.min(d, 1 - d);
    return clamp((front - dd) / 0.02, 0, 1);
  }

  /* A rune: one of six staves, in a unit box, `up` away from its wall. */
  _lodeRunePath(c, j){
    c.beginPath();
    switch (j % 6){
      case 0: c.moveTo(0, 1); c.lineTo(0, -1); c.moveTo(0, -0.15); c.lineTo(-0.62, -0.9);
              c.moveTo(0, -0.15); c.lineTo(0.62, -0.9); break;
      case 1: c.moveTo(-0.3, 1); c.lineTo(-0.3, -1); c.moveTo(-0.3, -0.5); c.lineTo(0.45, 0);
              c.lineTo(-0.3, 0.5); break;
      case 2: c.moveTo(0, -1); c.lineTo(0.62, 0); c.lineTo(0, 1); c.lineTo(-0.62, 0); c.closePath(); break;
      case 3: c.moveTo(-0.6, -1); c.lineTo(0.6, 1); c.moveTo(0.6, -1); c.lineTo(-0.6, 1); break;
      case 4: c.moveTo(0, 1); c.lineTo(0, -1); c.moveTo(-0.62, -0.38); c.lineTo(0, -1); c.lineTo(0.62, -0.38); break;
      default: c.moveTo(0.5, -1); c.lineTo(-0.4, -0.3); c.lineTo(0.4, 0.3); c.lineTo(-0.5, 1);
    }
  }

  /* Each rune's place: [u, x, y, inward nx, ny, index, wall, along]. 12 a
     wall on the top and the floor, 18 on each side, spaced over the CURRENT
     hall, `up` pointing into it. */
  _lodeRunes(G){
    const out = [];
    let j = 0;
    for (let wall = 0; wall < 4; wall++){
      const N = wall % 2 ? 18 : 12, len = wall % 2 ? G.h : G.w;
      const s0 = wall === 0 ? 0 : wall === 1 ? G.w : wall === 2 ? G.w + G.h : 2 * G.w + G.h;
      for (let i = 0; i < N; i++, j++){
        const u = (s0 + len * (i + 0.5) / N) / G.P, p = lodeAt(G, u);
        out.push([u, p[0] + p[2] * 12, p[1] + p[3] * 12, p[2], p[3], j, wall,
                  wall % 2 ? p[1] : p[0]]);
      }
    }
    return out;
  }

  _lodeWalls(m, f, G, P){
    const c = this.ctx, full = !(f.lodeOut > 0) && f.lodeAge >= 0.6;
    const a0 = f.lodeDie ? f.lodeFade : 1;
    const X0 = G.x0 + 2, Y0 = G.y0 + 2, X1 = G.x1 - 2, Y1 = G.y1 - 2;
    const K = [[X0, Y0], [X1, Y0], [X1, Y1], [X0, Y1]];
    c.save();
    c.lineJoin = "round";
    /* the chain: a soft band and a hard line on the wall, 2 units in; while
       it lights or goes dark, in pieces two to a rune, each as lit as the
       loop is at its middle */
    const band = (w, col, al) => {
      c.strokeStyle = col; c.lineWidth = w;
      if (full){ c.globalAlpha = al; c.strokeRect(X0, Y0, X1 - X0, Y1 - Y0); return; }
      c.lineCap = "butt";
      for (let wall = 0; wall < 4; wall++){
        const N = 2 * (wall % 2 ? 18 : 12), A0 = K[wall], A1 = K[(wall + 1) % 4];
        for (let i = 0; i < N; i++){
          const xa = A0[0] + (A1[0] - A0[0]) * i / N, ya = A0[1] + (A1[1] - A0[1]) * i / N;
          const xb = A0[0] + (A1[0] - A0[0]) * (i + 1) / N, yb = A0[1] + (A1[1] - A0[1]) * (i + 1) / N;
          const lit = this._lodeLit(f, lodeOn(G, wall, (xa + xb) / 2, (ya + yb) / 2));
          if (lit < 0.01) continue;
          c.globalAlpha = al * lit;
          c.beginPath(); c.moveTo(xa, ya); c.lineTo(xb, yb); c.stroke();
        }
      }
    };
    band(9, P.core, 0.13 * a0);
    band(2.2, P.core, 0.75 * a0);
    c.lineCap = "round";
    /* the runes */
    const RS = 6.5;
    for (const q of this._lodeRunes(G)){
      const lit = full ? 1 : this._lodeLit(f, q[0]);
      if (lit < 0.01) continue;
      c.save();
      c.translate(q[1], q[2]); c.rotate(Math.atan2(q[3], -q[4]));
      c.scale(RS, RS);
      c.globalAlpha = lit * a0;
      this._lodeRunePath(c, Math.floor(shellHash(9951, q[5]) * 6));
      c.strokeStyle = P.dark; c.lineWidth = 3.6 / RS; c.stroke();
      c.strokeStyle = P.core; c.lineWidth = 1.7 / RS; c.stroke();
      c.restore();
    }
    /* the draw's leading edge: a spark running out along the wall each way */
    if (!(f.lodeOut > 0) && f.lodeAge < 0.6){
      const k = f.lodeAge / 0.6, front = 0.52 * (1 - (1 - k) * (1 - k)) - 0.01;
      for (const sg of [-1, 1]){
        const p = lodeAt(G, f.lodeU0 + sg * Math.min(0.5, front));
        c.globalAlpha = 1;
        c.fillStyle = P.glow; c.beginPath(); c.arc(p[0] + p[2] * 2, p[1] + p[3] * 2, 4.2, 0, TAU); c.fill();
        c.fillStyle = "#FFFFFF"; c.beginPath(); c.arc(p[0] + p[2] * 2, p[1] + p[3] * 2, 1.8, 0, TAU); c.fill();
      }
    }
    c.restore();
  }

  /* THE FIELD, DRAWN: motes shed off the lit walls and drifting a little way
     into the hall, 28 of them, each on its own place and phase by
     shellHash on its index against the window's presentation clock. */
  _lodeMotes(m, f, G, P){
    const c = this.ctx, a0 = f.lodeDie ? f.lodeFade : 1;
    c.save();
    c.fillStyle = P.glow;
    for (let i = 0; i < 28; i++){
      const u = shellHash(9961, i), lit = this._lodeLit(f, u);
      if (lit < 0.01) continue;
      const k = ((f.lodeAge + f.lodeOut) / 3.2 + shellHash(9963, i)) % 1;
      const p = lodeAt(G, u), tx = -p[3], ty = p[2], dr = (shellHash(9965, i) - 0.5) * 18 * k;
      const d = 5 + 26 * k;
      c.globalAlpha = 0.8 * Math.sin(Math.PI * k) * lit * a0;
      c.beginPath();
      c.arc(p[0] + p[2] * d + tx * dr, p[1] + p[3] * d + ty * dr, 1.3 + 0.9 * shellHash(9967, i), 0, TAU);
      c.fill();
    }
    c.restore();
  }

  /* A TOUCH'S FLARE: the 60-unit span of each wall the foe met, level
     with it (kept whole on its own wall), in the glow, source-over, 0.15s. */
  _lodeFlare(m, f, G, P){
    const c = this.ctx, H = 60 / 2;
    c.save();
    c.lineCap = "round";
    const runes = this._lodeRunes(G);
    for (const q of f.lodeFx){
      if (q.t >= 0.3) continue;
      const k = q.t / 0.3, a = k < 0.12 ? 0.55 + 0.45 * k / 0.12 : 1 - (k - 0.12) / 0.88;
      for (const wall of q.walls){
        const side = wall % 2, lo = side ? G.y0 : G.x0, hi = side ? G.y1 : G.x1;
        const s = Math.max(lo + H, Math.min(hi - H, side ? q.y : q.x));
        const wx = wall === 1 ? G.x1 : G.x0, wy = wall === 2 ? G.y1 : G.y0;
        const nx = wall === 1 ? -1 : wall === 3 ? 1 : 0, ny = wall === 0 ? 1 : wall === 2 ? -1 : 0;
        const ax = side ? wx : s - H, ay = side ? s - H : wy, bx = side ? wx : s + H, by = side ? s + H : wy;
        c.globalAlpha = 0.35 * a; c.strokeStyle = P.core; c.lineWidth = 16;
        c.beginPath(); c.moveTo(ax + nx * 5, ay + ny * 5); c.lineTo(bx + nx * 5, by + ny * 5); c.stroke();
        c.globalAlpha = a; c.strokeStyle = P.glow; c.lineWidth = 5;
        c.beginPath(); c.moveTo(ax + nx * 2.5, ay + ny * 2.5); c.lineTo(bx + nx * 2.5, by + ny * 2.5); c.stroke();
        c.strokeStyle = "#FFFFFF"; c.lineWidth = 1.6;
        c.beginPath(); c.moveTo(ax + nx * 2.5, ay + ny * 2.5); c.lineTo(bx + nx * 2.5, by + ny * 2.5); c.stroke();
        /* the runes in the span flare with it */
        const RS = 6.5 * (1.25 + 0.25 * (1 - k));
        for (const r of runes){
          if (r[6] !== wall || Math.abs(r[7] - s) > H) continue;
          c.save();
          c.translate(r[1], r[2]); c.rotate(Math.atan2(r[3], -r[4])); c.scale(RS, RS);
          c.globalAlpha = a;
          this._lodeRunePath(c, Math.floor(shellHash(9951, r[5]) * 6));
          c.strokeStyle = P.dark; c.lineWidth = 4 / RS; c.stroke();
          c.strokeStyle = P.glow; c.lineWidth = 2.2 / RS; c.stroke();
          c.restore();
        }
      }
    }
    c.restore();
  }

  /* THE RUNE-STREAK: the hurled ball's own path over its last 0.2s, drawn
     under it, tapering to the tail, with runes riding it every 26 units. */
  _lodeStreak(m, f, P){
    const c = this.ctx, RS = 5;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of f.lodeFx){
      const Q = q.pts, n = Q.length / 3;
      if (n < 2) continue;
      const fade = q.t < 0.8 / 2 ? 1 : 1 - (q.t - 0.8 / 2) / (0.8 / 2);
      let run = 0;
      for (let i = 1; i < n; i++){
        const age = q.t - Q[3 * i + 2];
        if (age > 0.4) continue;
        const x0 = Q[3 * i - 3], y0 = Q[3 * i - 2], x1 = Q[3 * i], y1 = Q[3 * i + 1];
        const w = 20 * (1 - age / 0.4);
        c.globalAlpha = 0.45 * fade; c.strokeStyle = P.core; c.lineWidth = w;
        c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
        c.globalAlpha = 0.9 * fade; c.strokeStyle = P.glow; c.lineWidth = Math.max(1, w * 0.25);
        c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
        const d = Math.hypot(x1 - x0, y1 - y0);
        const r0 = run; run += d;
        for (let z = Math.ceil(r0 / 24) * 24; z < run; z += 24){
          const s = (z - r0) / (d || 1), x = x0 + (x1 - x0) * s, y = y0 + (y1 - y0) * s;
          c.save(); c.translate(x, y); c.rotate(Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2); c.scale(RS, RS);
          c.globalAlpha = fade * Math.min(1, 1.6 * (1 - age / 0.4));
          this._lodeRunePath(c, (q.k + z / 24) | 0);
          c.strokeStyle = P.dark; c.lineWidth = 3.4 / RS; c.stroke();
          c.strokeStyle = P.glow; c.lineWidth = 1.6 / RS; c.stroke();
          c.restore();
        }
      }
    }
    c.restore();
  }

  /* THE BAR: from the wall into the ball it hexes, one frame -- a jagged
     rune-light, three kinks by shellHash on the touch's count. */
  _lodeBolt(m, f, G, P){
    const c = this.ctx, foe = f === m.a ? m.b : m.a;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of f.lodeFx){
      if (m.over || !(m.t - q.t0 < 0.0125) || !foe.alive) continue;
      for (const wall of q.walls){
        const p = lodeAt(G, lodeOn(G, wall, q.x, q.y));
        const dx = foe.x - p[0], dy = foe.y - p[1], d = Math.hypot(dx, dy) || 1;
        const nx = -dy / d, ny = dx / d;
        const pts = [[p[0], p[1]]];
        for (let i = 1; i < 4; i++){
          const o = (shellHash(9971 + wall, q.k * 4 + i) - 0.5) * 16;
          pts.push([p[0] + dx * i / 4 + nx * o, p[1] + dy * i / 4 + ny * o]);
        }
        pts.push([foe.x, foe.y]);
        for (const [w, col] of [[6, P.dark], [3, P.glow], [1.2, "#FFFFFF"]]){
          c.globalAlpha = 1; c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
          c.stroke();
        }
      }
    }
    c.restore();
  }

  /* THE HEAD'S RUNE, in the weapon's own frame (drawWeapon's): the sigil
     etched in the head's face (`_whConjured`'s maker mark, the same ring and
     triangle at the same place) burns in the glow while the walls are lit,
     and goes dark with them. */
  _lodeHead(f, L){
    const c = this.ctx, P = f.aff, W = f.w.artW, hs = W * 0.8 / 2, sc = hs * 0.52;
    const path = () => {
      c.beginPath(); c.arc(0, 0, sc * 0.92, 0, TAU);
      for (let i = 0; i < 3; i++){
        const a = i * TAU / 3 - Math.PI / 2;
        if (i) c.lineTo(Math.cos(a) * sc * 0.60, Math.sin(a) * sc * 0.60);
        else { c.moveTo(Math.cos(a) * sc * 0.60, Math.sin(a) * sc * 0.60); }
      }
      c.closePath();
    };
    c.save();
    c.globalAlpha *= f.lodeFade;
    c.translate(L - hs, 0);
    c.lineCap = "round"; c.lineJoin = "round";
    path(); c.strokeStyle = P.dark; c.lineWidth = W * 0.11; c.stroke();
    path(); c.strokeStyle = P.glow; c.lineWidth = W * 0.055; c.stroke();
    path(); c.strokeStyle = "#FFFFFF"; c.lineWidth = W * 0.02; c.stroke();
    c.restore();
  }

  drawMotes(m){
'''),

('rebuttal picture: the runic warhammer, a rune-etched square head on a dark haft',
 '''  /* -------------------------------------------------------------- RUNIC --
     IN PIECES, HELD BY NOTHING. The grammar's second type. There is no haft at
     all and no head -- three blocks hang in a head-shaped cluster with real
     daylight between them, light bleeds down the axis where a shaft would be,
     and the sigil turns backwards where a hand would be.

     THE CELL'S FLAIR: a hammer's whole argument is that its mass is out at the
     end, so the chunks get BIGGER toward the striking face instead of tapering
     like a blade. The twinblade's shards narrow to a point; these grow into
     one. Same grammar, opposite gesture, because the type is different. */
  _whConjured(c, L, W, p){
    const hh = W * 0.50, gap = L * 0.34;
    const prof = (cc) => {
      cc.beginPath();
      cc.moveTo(L*0.56, -hh*0.42);
      cc.lineTo(L*0.93, -hh);
      cc.lineTo(L,      -hh*0.66);
      cc.lineTo(L,       hh*0.66);
      cc.lineTo(L*0.93,  hh);
      cc.lineTo(L*0.56,  hh*0.42);
      cc.closePath();
    };
    SHAPES._conjure(c, L, W, p, { n:3, gap, bw:hh, prof, frac:0.76,
                                  sliceFrom:L*0.56, sliceTo:L*1.0,
                                  beam:0.040, drift:0.050, cant:0.045,
                                  sigil:0.26 });
  },

''',
 '''  /* -------------------------------------------------------------- RUNIC --
     LODESTONE'S HAMMER (v70 section 6.1, "a rune-etched square head on a
     dark haft, first cut"). This route was the runic grammar's conjured
     hammer -- three slices held in formation, no haft, a sigil where a hand
     would be -- which no relic drew until Lodestone, the school's first
     warhammer. Measured at the app's 453x805 among the seven hammers
     (the weapon's |dL| over the floor, median of 5 frames):
     the conjured slices 0.243 on 2850 u2, this square head 0.239 on
     4361 u2 -- first of the seven, the other six 0.126-0.219 on 4100-6000
     u2: as legible, and a hammer-sized object.
     Runic's grammar is kept in the ETCHING: the school's triangle-in-ring
     sigil (`_makerMark`) cut into the face, and it burns while the walls are
     lit (`_lodeHead`). Only a runic warhammer reaches this route; every
     other school's hammer is untouched.
     THE HEAD IS SIZED OFF THE WIDTH, NOT THE LENGTH (Canopy's lesson on
     `_whGrown`): a square block 0.8 x W on a side at the end of the reach,
     and the haft runs from the ball to it. */
  _whConjured(c, L, W, p){
    const hs = W * 0.8 / 2, xb = L - 2 * hs, hw = W * 0.075;
    c.fillStyle = SHAPES._shade(p.dark, 1.15, 0.15);            // the dark haft
    c.fillRect(0, -hw, xb + 2, hw * 2);
    c.fillStyle = SHAPES._shade(p.dark, 2.4, 0.25);             // its two iron collars
    c.fillRect(xb - W * 0.10, -hw * 1.45, W * 0.07, hw * 2.9);
    c.fillRect(-L * 0.02, -W * 0.10, L * 0.05, W * 0.20);
    const head = (cc) => { cc.beginPath(); cc.rect(xb, -hs, 2 * hs, 2 * hs); };
    head(c); c.fillStyle = p.steel; c.fill();
    c.save(); c.shadowBlur = 0; c.globalAlpha = SHAPES._lit(c);  /* world light */
    head(c); c.clip();
    c.fillStyle = SHAPES._facet(p.steel, p.dark, 0.30);          // the lower face
    c.fillRect(xb, hs * 0.30, 2 * hs, hs * 0.75);
    c.fillStyle = SHAPES._facet(p.steel, p.dark, 0.62);          // the underside
    c.fillRect(xb, hs * 0.74, 2 * hs, hs * 0.30);
    c.restore();
    head(c);
    c.strokeStyle = SHAPES._shade(p.dark, 1.0, 0.2); c.lineWidth = Math.max(1, W * 0.05); c.stroke();
    /* the etching: a border cut round the face and the school's sigil in it */
    c.strokeStyle = SHAPES._facet(p.steel, p.dark, 0.72); c.lineWidth = Math.max(0.8, W * 0.028);
    c.strokeRect(xb + hs * 0.22, -hs * 0.78, 2 * hs - hs * 0.44, hs * 1.56);
    SHAPES._makerMark(c, xb + hs, 0, hs * 0.52, W, p);
    c.fillStyle = p.core;                                        // the striking face
    c.fillRect(L - W * 0.035, -hs, W * 0.035, 2 * hs);
  },

'''),

]

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
S6_HOOKS = ('SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });\n'
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
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


STAGE_OUT = {"1": "sc-lodestone", "2": "sc-lodestone-runes", "3": "sc-lodestone-rebuttal",
             "5": "sc-lodestone-b205", "6": "sc-lodestone-b205-fx"}


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


def assert_base(code: str, stage: str) -> None:
    """THE BASE BY CONTENT: every feature this builder reads or anchors on."""
    for need, why in (("tickTendril(dt){", "no tickTendril -- the window tickers' slot this "
                                           "builder follows is not there"),
                      ("this.tickTendril(dt);", "no tickTendril call"),
                      ("tickWinnow(dt){", "no tickWinnow"),
                      ("this.vineTally = null;", "no vineTally field line"),
                      ('if (u.kind === "tendril"){', "no tendril cast branch"),
                      ("if (f.charge >= f.w.ult.charge && !f.ultCorona", "no cast line"),
                      ("this.inset", "no inset"),
                      ('if (key === "runic")      return SHAPES._whConjured(',
                       "SHAPES.warhammer no longer routes runic to _whConjured")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if strip_comments(CLAMP) not in code:
        raise SystemExit("wrong base: `move` no longer clamps a ball at n + R -- the touch "
                         "would stop being a contact test")
    if HEX_DEF not in code:
        raise SystemExit("wrong base: STATUS.hex is not {5 stacks, 2.6s, a 0.2s stun every 1.15s}")
    if DONOR_PHYS not in relic_row(code, "grudgebearer"):
        raise SystemExit("Grudgebearer's hammer profile has moved -- the donor is not what "
                         "this builder copies")
    for h in HAMMERS:
        row = " ".join(relic_row(code, h).split())
        if not re.search(r'shape:"warhammer",\s*blades:\[0\], reach:76, width:26, '
                         r'artW:54, dmg:[\d.]+, spin:1\.6, mode:"spin", mass:5\.0, '
                         r'knockMul:2\.3', row):
            raise SystemExit(f"{h} is not the type's hammer profile any more")
    for v in RUNIC:
        if "onHit:{ hex:1 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, hex 1")
    if stage == "1":
        for name in NAMES:
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    if A.stage == "5" and BLADE is None:
        raise SystemExit("stage 5 has no blade yet -- v102 §4 sets it")

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nLODESTONE / REBUTTAL -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    assert_base(code, A.stage)
    print("  base  by content: the window tickers' slot, the anchors, the five hammers' "
          "profile, the runic channel, the runic hammer head, hex, the wall clamp")

    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        blk0 = relic_ult(code)
        if A.stage == "2":
            if "ultRunes" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultRunes" not in code or "hurl:0," not in blk0:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["hurl"])
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
            if f'hurl:{ULT["hurl"]},' not in blk0 or "dmg:23.5," not in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["hurl"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Lodestone's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
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
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickRunes|checkEnd|breakSpin)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort|fill)\(", ins):
            if not S6_ARRAY_OK(mw.group(1)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
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
        ins = strip_comments(new.replace(_old, "", 1) if _old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(dmg|spin|reach|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        # THE WALLS DO NO DAMAGE AND HOLD NOTHING (brief §1: "Nothing writes
        # f.stun or f.pin; nothing goes through resolveHit"; design §5: no
        # beat, no hit stop).
        if re.search(r"\.(stun|pin|pinMax|pinFree|pinV|hitStop)\s*=[^=]", ins) or \
           re.search(r"\b(resolveHit|hurt|beat)\s*\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stuns, pins, "
                             "stops, hurts or files a beat")
    if len(re.findall(r'kind:"runes"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one runes ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    last = re.findall(r'\{ id:"([a-z]+)", name:"', out_code)[-1]
    print(f"  ok    one runes ultimate, Lodestone's; no insert draws the RNG, writes the "
          f"shared weapon, stuns, pins, stops, hurts or files a beat; {n_ids} relics "
          f"in the roster (last in the array: {last})")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
