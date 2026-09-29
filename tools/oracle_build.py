#!/usr/bin/env python
"""ORACLE / FORESIGHT -- the runic bow, a NEW relic. v105.

Built from `06-docs/v75/ORACLE-BUILD-BRIEF.md` and `runic-bow-design-v75.md`
(Cowork, 2026-09-26), which are the input and the only input. CLAUDE.md §3
rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-oracle.html        (arm A)
    stage 2   the aim                     -> sc-oracle-aim.html          (arm B)
    stage 3   the double hex              -> sc-oracle-sight.html        (arm C)
    stage 5   the blade                   -> sc-oracle-b10.html          (16.23 -> 10, TUNED)
    stage 6   the picture and the voice   -> sc-oracle-fx.html           (no field: drawn motes, v105 §5)

§1 (the brief's §0): "For a duration the bow foresees: a rune marks where the
enemy will be when the next arrow lands, every arrow of the stream flies to it,
and an arrow that lands hexes twice."

Declared (design §5, brief §0-§1):
  THE AIM     for the window, each window frame, theta turns at `turn` rad/s the
              shortest way round toward atan2(lead - f), lead = foe + v_foe x
              (|foe - f| / shot.speed) -- ballisticAngle, which IS atan2 for a
              grav-0 bow (this one's); the spin does not advance theta while the
              window runs (Tendril's construction). tickFire is untouched: the
              stream fires on its own cadence along the aimed facing.
  THE HEX     in resolveHit, when a SHOT owned by a caster with ultSight lands:
              foe.apply("hex", hex, side) in addition to the channel's own.
  Charge 16 (the lab's clock), window 8. Nothing waits. No stasis, no pin.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm C (v105 §0, the census).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE WINDOW IS {t, dur} ON THE WINDOW TICKERS' CLOCK, not the brief's
     `{ t0, end }` in match time: every window in the batch runs on that clock
     (Corollary, Daybreak, Zenith, Canopy, Onslaught, Tendril), and the ruling
     is that a freeze freezes the world. `tickSight` advances it.
  2. THE AIM TURNS WHILE STUNNED (the lab turned it on every window frame; the
     design says "each window frame" and names Tendril's construction, which
     turns while stunned). A stunned bow still cannot FIRE (tickFire's own
     rule, untouched). It does NOT turn in a hit stop: tickWeapon does not run
     there (the engine's convention; the lab's overlay turned through freezes).
     THE TEXT AGAINST IT is the brief's §1: "theta turns toward the lead
     instead of `theta += spin·dt` (the ranged branch)" -- and in the engine
     the ranged branch sits AFTER the stun lock, so a stunned bow never reaches
     it. Read as naming the statement the aim replaces (the spin's advance),
     not as placing the aim under the lock: the design's "each window frame"
     and "Tendril's construction" are the explicit words, and the lab priced
     the turn on every frame. Priced in v105 §2: the bow held while stunned
     (variants.py mut-stunlock, relic_rate both sides at blade 10, 1520
     fights) reads 44.1 / 49.2 = 46.6% against the link's 50.7 / 48.3 =
     49.5%: the reading is worth about +3 (a standard error of a difference
     is about 1.8).
  3. THE SPIN DOES NOT ADVANCE THETA IN THE WINDOW (the prose, twice: design
     §5 and brief §0). The lab left the engine's spin running and turned at 6
     on top of it, so its turn was 6 -/+ 2.8 while acquiring and exact while
     locked; the build turns at 6 flat. Priced in v105 §2.
  4. THE SECOND HEX IS ON A SHOT ONLY (design §5: "when a SHOT owned by a
     caster with ultSight lands"; §1: "an arrow that lands hexes twice"). The
     lab added it on every `me.hits` step, which also counts the bow's blade
     blows; the prose is explicit. A shot is `mul !== undefined` in
     resolveHit (the engine's own test: "`mul === undefined` is an ordinary
     melee connect and not a projectile"); this relic's only such call is
     tickShots' hit branch.
  5. THE SECOND HEX GOES ON A LIVE FOE, the opponent only (the lab's
     `foe.alive`; never a Twinshade shade), after the channel's own apply.
  6. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; the lab passed
     the Fighter, and hex has no reader of its source).
  7. THE WINDOW CLOSES ON EITHER DEATH (the lab's close; the match ends there
     anyway), or its clock.
  8. THE AIM HOLDS (no spin, no turn) on a window frame where either fighter is
     dead (the lab aimed only while both were alive); the window closes in
     that step's tickSight.
  9. THE BLURB is the design's own §0/§1 sentence, shortened; the card is the
     design's (68 chars). Rick's to overrule, as every name is. The card says
     "each hit hexes twice"; by reading 4 only an arrow does (a blade blow in
     the window hexes once). Worth +0.4 (v105 §2); the wording is Rick's.
 10. THE BRIEF'S STAGE-2 LOCK GATE ("theta within 6·dt of the lead bearing on
     every window frame after the first half-second (asserted)") CANNOT HOLD,
     and does not in the lab either: the lead is foe + v_foe x tof, and the
     foe's velocity jumps on every bounce and knock, so the lead bearing jumps
     faster than 6 rad/s can follow. The lab's own facing sits within 6·dt of
     it on 43.6% (arm B) / 43.5% (arm C) of those frames; the build's on
     ~40%. What the probe ASSERTS on every window frame is the construction
     itself (theta + clamp(shortest angle to the lead, +-turn x dt)); the lock
     is printed, not gated.

THE CLOCK. The window and the turn run on the window tickers' clock (tickWeapon
and tickSight both stop in a hit stop). The lab ran both through freezes; v99
§4, v100 §2 and v101 §2 measured what that is worth on the builds before this.

THE BASE is asserted BY CONTENT: the anchors (each exactly once), the bow
type's profile on Ironhail's row (the lab's donor; its blade may move under a
redesign, the profile may not), the runic channel on the runic relics, hex,
ballisticAngle's grav-0 branch, and the names this relic adds, free. Never by
which relic is last: the row goes at the END of WEAPONS, whatever is there.

STAGE 6 (design §6.1-6.2, brief §2 stage 6; v105 §5). Art and sound are Code's
picks on measurements under Rick's "you pick i overrule", made by two labs in
parallel on sc-oracle-b10 (`oracle_voice_lab.py`; the picture lab's scratch
rows). The S6 table below is their row files, byte-exact: voice 4, picture 7,
no two on one anchor line (so nothing is merged); either order writes the same
bytes. THE READINGS the labs declared, and this build carries:
 11. THE RUNE IS THE LEAD THE AIM TURNS TOWARD, re-read only on a step the
     window clock moved (the aim ran), so it holds its point through a hit
     stop as the bow does. The lead is outside the live hall on 67.9% of live
     window frames, so the rune is drawn where the bow's line to it leaves the
     hall (the bearing kept, the rune on the floor), eased at 0.05s.
 12. NO fx.js FIELD, though the brief says "Field in both copies": the cast's
     one `m.ultFx` slot is Oracle's for a median 0.67s of the 8s window, and
     the sight-line sits a median 209 units from where a field would spawn.
     The design's "rune motes along the sight-line" are DRAWN, for the whole
     window. Both copies of fx.js are untouched. Rick's to overrule.
 13. A LANDED WINDOW ARROW is seen by `sightTally` rising (resolveHit makes no
     call for the picture): a flare on the foe, and the arrow's own HEX tag
     takes the foe's count, so "the hex tag ticks by two". A killing arrow
     neither flares nor re-counts a tag (the shatter owns that frame).
 14. THE EYE is strokes and no fill (the health level reads through it); it
     shuts over 0.3s at any close, a death or the verdict included.
 15. THE SIGIL'S "sustained shimmer" is a note RE-STRUCK on the window's 1st,
     9th, 17th ... frame, on the window clock (a held note does not exist in
     the synth); never on the closing frame. "Pitch by count" is the foe's hex
     count just after the second hex (2-5 in play: the channel's hex lands
     first). The close voice plays on a clock close with both alive, never on
     a death. The cast is fireUlt's own `ult`/oracle call, whose arm goes
     before the rune-crack fallback (re-emitted for the relics still on it).
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "oracle"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v105 §0)
    "dur": 8,         # "the window 8s every 16s"
    "turn": 6,        # "theta turned at 6 rad/s toward lead"
    "hex": 1,         # "+1 hex in resolveHit on a shot landed by a caster with ultSight" -- stage 3
}
TIP = "Every arrow flies to where the foe will be, and each hit hexes twice"
# The bow type's profile, Ironhail's (the lab's donor: `ult_overlay --relic
# ironhail --cell runic:bow`), at Ironhail's blade 16.23 until stage 5.
BLADE0 = "16.23"
PROFILE = ('blades:[0], reach:54, width:9, artW:44, dmg:{dmg}, spin:2.8, '
           'mode:"ranged", mass:1.6,')
SHOT = ('shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0, '
        'tip:"Fires along its facing · shots can be clanked" },')
RUNIC = ("spellbreaker", "axiom", "foregone", "paradox")
BLURB = ("A runic bow that foresees: a rune marks where the foe will be, every "
         "arrow flies to it, and each hit hexes twice.")


def ult_block(charge, hex_) -> str:
    return (f'''    ult:{{ name:"Foresight", charge:{charge}, kind:"sight", dur:{ULT["dur"]}, turn:{ULT["turn"]},
          hex:{hex_},          // v75: the double hex (stage 3)
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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH, the output "
                         "cannot be syntax checked")
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
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse (node --check)")


# ---------------------------------------------------------------- stage 1 --
# THE RELIC, APPENDED AT THE END OF WEAPONS, ITS ULTIMATE STUBBED at charge 1e9
# (the clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. THE ANCHOR is the line that closes the array and the comment that
# follows it; it names no relic, so the row lands after whatever relic is last
# on the tip it is built on. Every other table keyed by relic id falls back.
ROW_ANCHOR = ('''
];
/* The single source of truth for "which status does this relic teach".''')

S1 = [

("oracle joins the roster at the end of WEAPONS, its ultimate stubbed",
 ROW_ANCHOR,
 f'''
  /* ORACLE / FORESIGHT (v75; built v105) -- THE RUNIC BOW. The bow type's
     profile and Ironhail's blade, 16.23 (the lab's donor; stage 5 settles
     it), and the school's channel, onHit hex 1. Stage 1 stubs the ultimate
     at charge 1e9; stage 2 gives it its aim, stage 3 its second hex. */
  {{ id:"oracle", name:"Oracle", aff:"runic", shape:"bow",
    {PROFILE.format(dmg=BLADE0)}
    shot:{{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" }},
    onHit:{{ hex:1 }},
{ult_block("1e9", 0)}
    blurb:"{BLURB}" }},
''' + ROW_ANCHOR),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the sight has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Foresight", charge:1e9, kind:"sight", dur:8, turn:6,
''',
 f'''    ult:{{ name:"Foresight", charge:{ULT["charge"]}, kind:"sight", dur:{ULT["dur"]}, turn:{ULT["turn"]},   // v75 stage 2: the bow aims
'''),

("the fighter carries the sight",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while ORACLE's FORESIGHT runs (v75), on the window tickers'
       clock. null on every other relic and on this one outside its window:
       tickWeapon reads it once, resolveHit once for a projectile, and
       `tickSight` returns after a two-iteration loop that does nothing.
       `sightTally` is the probe's count, cumulative over the fight; nothing
       in the simulation reads it. */
    this.ultSight = null;
    this.sightTally = null;
'''),

("the bow aims at the lead, each window frame, stunned or not",
 '''    else if (f.stun > 0){ /* weapon locked */ }
''',
 '''    /* FORESIGHT'S AIM (v75 §5, brief §1). For the window, each window frame,
       the facing turns at `turn` rad/s the shortest way round toward the
       LEAD -- where the foe will be when an arrow loosed now arrives:
       lead = foe + v_foe x (|foe - f| / shot.speed) -- and the spin does not
       advance it (Tendril's construction). Stunned or not, as the lab turned
       it: a stunned bow still cannot fire (tickFire's rule), it only comes
       out of the stun already aimed. The bearing is `ballisticAngle`, which
       is atan2 for a grav-0 bow (this one's) and the aimed shot's arc for
       any other. tickFire is untouched: the stream fires on its own cadence
       along whatever facing this leaves. `ultSight` is null on every other
       relic, so this branch is never taken but by Oracle's window. The
       locals are named for the lead (leadX / leadY / bearing), so no line of
       this insert is also a line of Tendril's seek and chain_audit can
       watch it at every carry. */
    else if (f.ultSight){
      if (f.alive && foe.alive){
        const S = f.w.shot;
        const tof = Math.hypot(foe.x - f.x, foe.y - f.y) / S.speed;
        const leadX = foe.x + foe.vx * tof, leadY = foe.y + foe.vy * tof;
        const bearing = ballisticAngle(leadX - f.x, leadY - f.y, S.speed, S.grav || 0);
        const dl = Math.atan2(Math.sin(bearing - f.theta), Math.cos(bearing - f.theta));
        const k = f.w.ult.turn * dt;
        f.theta += clamp(dl, -k, k);
      }
    }
    else if (f.stun > 0){ /* weapon locked */ }
'''),

("the cast opens the sight and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "sight"){
      /* FORESIGHT (v75). NOTHING RESOLVES HERE: the cast opens the window
         for `u.dur` seconds, and tickWeapon (the aim), resolveHit (the second
         hex) and `tickSight` (the clock) do everything the window does. */
      f.ultSight = { t: 0, dur: u.dur };
      if (!f.sightTally)
        f.sightTally = { casts: 0, frames: 0, foeHex: 0, arrows: 0, hex: 0 };
      f.sightTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("an arrow that lands in the window hexes twice",
 '''    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit
''',
 '''    /* FORESIGHT'S SECOND HEX (v75 §5): "when a SHOT owned by a caster with
       ultSight lands: foe.apply("hex", 1, f) in addition to the channel's".
       AFTER the `onHit` loop, so the channel's own stack is on first. A shot
       is `mul !== undefined` -- the engine's own test, and this relic's only
       such call is tickShots' hit branch -- so the bow's blade blows never
       pay it. A live foe, the opponent only; the source is a side letter.
       Nothing else: no damage, no stop, no beat. `hex` is 0 at stage 2. */
    if (mul !== undefined && self.ultSight){
      const T = self.sightTally;
      T.arrows++;
      if (self.w.ult.hex > 0 && foe.alive && !foe.shade){
        foe.apply("hex", self.w.ult.hex, self === this.a ? "a" : "b");
        T.hex += self.w.ult.hex;
      }
    }

    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit
'''),

("the sight ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickSight(dt);                 // FORESIGHT (v75)
'''),

("tickSight runs the window's clock",
 '''  tickWinnow(dt){
''',
 '''  /* ============================================== THE FORESIGHT ========
     v75 §1 / §5, brief §0-§1. The window's CLOCK and nothing else: the aim is
     tickWeapon's (each window frame, before the fighter fires) and the second
     hex is resolveHit's (each arrow that lands). The window closes by its
     clock or on either death; nothing waits for it and nothing lingers after
     it. On the window tickers' clock, so it freezes through a hit stop, and
     so does the aim (tickWeapon does not run there). The tally is the
     probe's: window frames and the foe's hex on them. */
  tickSight(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultSight;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultSight = null; continue; }
      const T = f.sightTally;
      T.frames++;
      T.foeHex += foe.stacks("hex");
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the double hex",
 '''          hex:0,          // v75: the double hex (stage 3)
''',
 f'''          hex:{ULT["hex"]},          // v75: the double hex (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief §2 stage 5: "Wide on 151 at 11.5 / 12 / 12.5. Expect
# 11.5-12."). Filled from the measurement (v105 §4): relic_rate, both sides,
# seed0 2207 + 2317, 1520 fights a point on sc-oracle-sight --set dmg=X:
#   9.5 -> 48.9   10 -> 49.5   10.5 -> 54.7   11 -> 57.7
#   11.5 -> 61.4   12 -> 67.3   12.5 -> 69.5
# The crossing is ~10.05, UNDER the brief's 11.5-12, and the brief names no
# other knob (its §3 lists the turn as "NOT TO RE-BUY"; charge and window are
# the design's). So the blade goes to the measured point nearest 50%, 10, and
# the miss is said (v105 §4) and left to Rick. The gap is attributed in v105
# §2: the engine's window clock and the prose's no-spin aim, +5 and +4 at
# 16.23 (stage 3), +8 and +18 at 10; the lab's constructions put back land on
# the lab's arm C at both blades.
TUNED = {"dmg": 10}

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v75 §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule" by `oracle_voice_lab.py` (the four voices) and
# the picture lab (the eye, the rune and its sight-line, the rune motes, the
# window arrows' rune, the flare and the count on the HEX tag) -- v105 §5.
# Presentation only: engine_ab over all 39 relics, Oracle included, is the
# proof, and probe [8] / [9] read it inside the hooks. The rows are byte-exact
# to the labs' own files (voice 4, picture 7; no two share an anchor line, so
# none is merged). No fx.js field: the cast's one `m.ultFx` slot is Oracle's
# for a median 0.67s of the 8s window, so the design's rune motes are DRAWN.
S6 = [

("Sfx: Oracle's cast, sigil, snap and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "oracle"){                     // the rune-eye opens
          /* ORACLE'S CAST, THE EYE OPENING -- v75 §6.2: "cast: a rune-eye
             'open' -- a filtered inhale into a soft chime, 0.4s". SIGIL, of 5,
             picked on the numbers by `oracle_voice_lab.py` under Rick's "you
             pick i overrule" (v105). Oracle had no arm and fell through to
             rune-crack, which 12 other relics on its stage-5 link still use,
             so this ADDS arms before that fallback and leaves it alone.

             The breath: band-passed noise swelling for 0.33 s (the longest
             attack a `_sweep` allows), its band climbing 660 -> 6652.4 Hz so
             it passes the chime's note at its top (x1.27 over its swell, rise
             87 ms, no peak more than 2.5 dB over its neighbours: air). At its
             top (3 ms off) the chime: the sigil's own note, E7 (2640 Hz), with
             a faint bar mode, struck as four in-phase strikes over 30 ms, so
             it enters in 23 ms and not as a click. Audible 395 ms; loudest 50
             ms -3.2 to -2.4 dB re the blow. Register at most 0.65 against
             rune-crack, the runic and bow casts, the school's snap, the
             bowstring, the blow and the death voice. */
          const g = 0.09833;
          this._sweep(t, { f0: 660, f1: 6652.4, q: 1.2, gain: g * 2.124, dur: 0.55, atk: 0.33, type:"bandpass" });
          for (const [r, k, d] of [[1, 1, 1], [2.76, 0.25, 0.5]]){
            const f = 2640 * r;
            for (let i = 0; i < 4; i++)
              this._tone(t + 0.33 + Math.round(f * 0.03 * i / 4) / f, { freq: f, gain: g * k / 4, dur: 0.317 * d, type:"sine" }).frequency.value = f;
          }
        } else if (w === "oracle-sigil"){               // the sigil shimmers
          /* THE SIGIL'S SHIMMER -- "a very quiet sustained shimmer (re-struck,
             2-3 kHz band, peak <= 0.15) while it is drawn" (v75 §6.2). FLICK,
             of 9 (`oracle_voice_lab.py`). One strike a call: `tickSight`
             re-strikes it on the window's first frame and every 8th window
             frame after, so the strikes are the held note (CLAUDE.md 4.5) and
             stop with the window.

             2640 Hz (whole multiples of 120 Hz: a clip places every strike on
             a 1/120 s frame, so they all start in phase and sum as one note);
             each strike 0.3 s long, falling 26 dB before it stops (`_tone`
             ramps to 0.0001 absolute), so 4.5 overlap: a 5.1 dB shimmer at 15
             Hz. Steady loudest 50 ms +3.0 dB re the bowstring and -9.0 dB re
             the wall tick (the quietest voice in the fight), +29.4 dB over the
             score in its third-octave (+28.4 at the least); peak 0.0065; 100%
             of its power in 2-3 kHz; under the score 0.27 s after the close. */
          this._tone(t, { freq: 2640, gain: 0.001924, dur: 0.3, type:"sine" }).frequency.value = 2640;
        } else if (w === "oracle-hex"){                 // an arrow hexes twice
          /* A WINDOW ARROW HEXES TWICE -- "a hit: the bow's own arrow voice
             plus a hex snap; pitch by count" (v75 §6.2). SEMI, of 3
             (`oracle_voice_lab.py`): the school's own snap (the `hex-snap`
             below), every frequency x 2^(step / 12), step 0, 1, 2, 3, 4
             semitones at counts 1-5, n = the count the foe's tag shows after
             the second hex; at count 1 it IS the school's snap. `resolveHit`
             plays it on the arrow's own frame, over the arrow's own hit voice.

             Measured pitch 3003 / 3184 / 3377 / 3581 / 3790 Hz; on the blow it
             stands +9.2 dB or more over it in its own third-octave; register
             at most 0.63 against the blow, the wall tick, the bowstring,
             rune-crack and the death voice. */
          const n = clamp(Math.round(p.n === undefined ? 1 : p.n), 1, 5), k = Math.pow(2, [0, 1, 2, 3, 4][n - 1] / 12);
          this._burst(t, { freq: 2600 * k, q: 1.2, gain: 0.38, dur: 0.022, type:"bandpass" });
          this._burst(t, { freq: 1300 * k, q: 1, gain: 0.15, dur: 0.03, type:"bandpass" });
          this._tone(t, { freq: 3100 * k, to: 2500 * k, gain: 0.138, dur: 0.045, type:"triangle" });
        } else if (w === "oracle-close"){               // the eye shuts
          /* THE EYE SHUTS -- "close: the chime reversed" (v75 §6.2). FULL, of
             8 (`oracle_voice_lab.py`): every mode of the cast's chime, its
             fall run backwards as a climb re-struck at whole cycles ~11 ms
             apart, ending where the chime began, cut there. ENV-CORR 0.92 with
             the chime's own samples reversed; loudest 50 ms 0.0 dB off the
             chime's; audible 325 ms. `tickSight` plays it once, on the frame
             the window runs out by its clock with both fighters alive. */
          const g = 0.1055, L = 0.317;
          for (const [r, k, d, R] of [[1, 1, 1, 0.004068], [2.76, 0.25, 0.5, 0.01627]]){
            const f = 2640 * r, dt = Math.max(1, Math.round(f * 0.011)) / f, q = Math.pow(0.0001, dt / 0.1);
            for (let s = Math.max(0, L - 0.317 * d); s < L - 1e-9; s += dt)
              this._tone(t + s, { freq: f, gain: g * k * (1 - q) * Math.pow(R, (L - s) / (0.317 * d)), dur: 0.1, type:"sine" }).frequency.value = f;
          }
        } else {                                        // rune-crack'''),

("tickSight: the sigil's shimmer, re-struck every 8 window frames while the window runs",
 '''      T.foeHex += foe.stacks("hex");''',
 '''      T.foeHex += foe.stacks("hex");
      /* FORESIGHT'S SIGIL (v75 §6.2: "a very quiet sustained shimmer
         (re-struck, 2-3 kHz band, peak <= 0.15) while it is drawn"): a held
         note does not exist in this toolkit, so the window re-strikes it --
         on its first frame and every 8th window frame after, while it runs
         (never on the closing frame, which `continue`s above). On the window's
         clock, so a hit stop holds the strikes as it holds the sigil.
         Presentation only: SFX.play draws nothing, is a no-op headless, and
         nothing here is read back (oracle_voice_lab: fights identical). */
      if (Math.round(Z.t / dt) % 8 === 1) SFX.play("ult", { w: "oracle-sigil" });'''),

("resolveHit: the snap, pitched by the foe's hex count, once per second hex",
 '''        T.hex += self.w.ult.hex;''',
 '''        T.hex += self.w.ult.hex;
        /* THE SNAP (v75 §6.2: "a hit: the bow's own arrow voice plus a hex
           snap; pitch by count"): the school's snap, pitched by the count
           the foe's tag now shows, once per arrow that hexes twice. The
           arrow's own hit voice and hit beat are the engine's, untouched.
           Presentation only; nothing here is read back. */
        SFX.play("ult", { w: "oracle-hex", n: foe.stacks("hex") });'''),

('tickSight: the close voice, on a clock close with both fighters alive',
 '''      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultSight = null; continue; }''',
 '''      /* FORESIGHT'S CLOSE (v75 §6.2: "close: the chime reversed"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive --
         never on a death, never once the fight is over (step() stops calling
         this). Presentation only; nothing here is read back. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "oracle-close" });
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultSight = null; continue; }'''),

('foresight picture: fighter fields',
 '''    this.ultSight = null;
    this.sightTally = null;
''',
 '''    this.ultSight = null;
    this.sightTally = null;
    /* FORESIGHT'S PICTURE (v75 section 6.1), and none of it is the sim's:
       the eye shuts and the rune fades for 0.3s after `ultSight` is gone, and
       the rune holds its point through a hit stop, so the picture keeps its
       own state. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickForesight`); nothing in the simulation reads any of it.
         foreFade -- 1 while the window runs; eased to 0 over the close
         foreAge  -- the presentation clock since the cast (the eye opening)
         foreOut  -- the presentation clock since the close (the eye shutting)
         foreT    -- the window clock as last seen: it moves only on a step
                     the aim ran, so the lead is re-read only then
         foreLead -- the lead the aim turned toward, as last read [x, y]
         foreRune -- the floor rune as drawn [x, y]: the lead, kept inside
                     the live hall, eased
         foreSeen -- `sightTally`'s arrows and hex, as last seen
         foreFx   -- a window arrow's rune flare on the foe (records) */
    this.foreFade = 0;
    this.foreAge = 0;
    this.foreOut = 0;
    this.foreT = -1;
    this.foreLead = null;
    this.foreRune = null;
    this.foreSeen = [0, 0];
    this.foreFx = [];
'''),

('foresight picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickForesight(dt);             // FORESIGHT'S PICTURE (v75 section 6.1)
'''),

('foresight picture: tickForesight',
 '''  tickWinnow(dt){
''',
 '''  /* ---------------------------------------------- FORESIGHT'S PICTURE ---
     v75 section 6.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.5 is the
     eye's 0.25s opening, 0.6 the 0.3s close, 0.6 a hit's 0.3s flare.
     THE RUNE IS THE LEAD THE AIM TURNS TOWARD, re-read from the state only on
     a step the window clock moved -- the aim ran on exactly those -- so it
     holds its point through a hit stop as the bow does (a lead re-read there
     would slide on the gravity a frozen ball keeps earning). THE LEAD IS
     OUTSIDE THE HALL ON TWO WINDOW FRAMES IN THREE (a ball at cruise meets a
     wall inside one arrow's flight), so the rune is drawn where the bow's
     line to the lead leaves the live hall: the bearing the aim turns to is
     kept, and the rune stays on the floor. It chases that point with a
     time constant of 0.1 (0.05s), so a bounce that throws the lead across
     the hall reads as the rune sliding there rather than a jump cut. A WINDOW
     ARROW THAT LANDS IS FOUND BY WATCHING `sightTally` RISE: resolveHit makes no
     call for the picture: `arrows` is the flare on the foe, and on `hex` the
     tag the arrow's own onHit printed this step takes the foe's count, so it
     ticks by two. Writes presentation fields and a tag's `val` only, and
     draws no rng. */
  tickForesight(dt){
    for (const f of [this.a, this.b]){
      const T = f.sightTally;
      if (!T && !(f.foreFade > 0)) continue;                   // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      for (let i = f.foreFx.length - 1; i >= 0; i--){
        f.foreFx[i].t += dt;
        if (f.foreFx[i].t >= 0.6) f.foreFx.splice(i, 1);
      }
      const Z = (this.over || !f.alive) ? null : f.ultSight;
      if (Z){
        if (!(f.foreFade > 0) || f.foreOut > 0){               // a cast
          f.foreAge = 0; f.foreOut = 0; f.foreT = -1;
          f.foreLead = null; f.foreRune = null;
        }
        f.foreFade = 1;
        f.foreAge += dt;
        if (Z.t !== f.foreT && foe.alive){
          f.foreT = Z.t;
          const tof = Math.hypot(foe.x - f.x, foe.y - f.y) / f.w.shot.speed;
          f.foreLead = [foe.x + foe.vx * tof, foe.y + foe.vy * tof];
        }
        if (f.foreLead){
          const A = CONFIG.arena, e = (this.inset || 0) + 16;
          const dx = f.foreLead[0] - f.x, dy = f.foreLead[1] - f.y;
          let s = 1;
          if (dx < 0 && f.x + dx < e) s = Math.min(s, (e - f.x) / dx);
          if (dx > 0 && f.x + dx > A.w - e) s = Math.min(s, (A.w - e - f.x) / dx);
          if (dy < 0 && f.y + dy < e) s = Math.min(s, (e - f.y) / dy);
          if (dy > 0 && f.y + dy > A.h - e) s = Math.min(s, (A.h - e - f.y) / dy);
          s = Math.max(0, s);
          const tx = f.x + dx * s, ty = f.y + dy * s;
          if (!f.foreRune) f.foreRune = [tx, ty];
          else {
            const k = 1 - Math.exp(-dt / 0.1);
            f.foreRune[0] += (tx - f.foreRune[0]) * k;
            f.foreRune[1] += (ty - f.foreRune[1]) * k;
          }
        }
      } else if (f.foreFade > 0){
        f.foreOut += dt;
        f.foreFade = Math.max(0, 1 - f.foreOut / 0.6);
      }
      if (!T) continue;
      const na = T.arrows - f.foreSeen[0], nh = T.hex - f.foreSeen[1];
      f.foreSeen[0] = T.arrows; f.foreSeen[1] = T.hex;
      /* A KILLING ARROW FLARES AND TAGS NOTHING: the shatter owns that frame. */
      if (!foe.alive || !(foe.hp > 0)) continue;
      if (na > 0){
        f.foreFx.push({ t: 0, n: T.arrows });
        if (f.foreFx.length > 6) f.foreFx.shift();
      }
      if (nh > 0){
        const Rb = CONFIG.physics.ballR, k = foe.stacks("hex");
        let left = nh;
        for (let i = this.tags.length - 1; i >= 0 && left > 0; i--){
          const g = this.tags[i];
          if (g.key === "hex" && !g.val && g.life === g.max
              && Math.hypot(g.x - foe.x, g.y - foe.y) < Rb * 3){ g.val = k; left--; }
        }
      }
    }
  }

  tickWinnow(dt){
'''),

('foresight picture: the floor call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* FORESIGHT'S FLOOR (v75 section 6.1): the rune where the foe will be,
       the sight-line from the bow to it and the rune motes running along it.
       The WORLD pass and under both balls -- the rune is on the floor, and a
       foe standing on its own rune is where the prophecy came true -- and
       none of it reaches the bloom. */
    if (__world) this.drawForesight(m);
'''),

('foresight picture: the emissive call (over both fighters)',
 '''    this.drawShots(m);
''',
 '''    this.drawShots(m);
    /* FORESIGHT'S ARROWS AND FLARES: a window arrow's rune and core trail
       on the bow's own arrow, and a landed one's rune flare on the foe.
       Light, so this pass, with the shots it rides on. */
    this.drawForesightTop(m);
'''),

('foresight picture: the eye on the glass',
 '''    this._drawBark(m, f, c);  // CANOPY'S BARK, on the glass (v69 section 7.1)
''',
 '''    this._drawBark(m, f, c);  // CANOPY'S BARK, on the glass (v69 section 7.1)
    /* FORESIGHT'S EYE (v75 section 6.1): it opens on the glass at the cast
       and shuts at the close. `foreFade` is 0 on every other relic, so this
       is one comparison on a field nothing else writes. */
    if (f.foreFade > 0) this._foreEye(c, f, R);
'''),

('foresight picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------ FORESIGHT'S PICTURE ---
     v75 section 6.1, drawn off the fighter's `fore*` fields and the MATCH's
     shots (read, never written) -- never `m.ultFx`, one slot the opponent's
     cast takes (open item 25). One method a component, so each can be
     measured alone; nothing here keeps state or draws from the rng.
       drawForesight     WORLD, under both balls: the sight-line from the
                         bow's nock to the rune, the rune motes running
                         along it (the design's field, drawn), the rune.
       drawForesightTop  EMISSIVE, over both fighters: each window arrow's
                         core trail and rune; a landed arrow's flare.
       _foreEye          on the caster's glass, in drawFighter. */
  drawForesight(m){
    if (!(m.a.foreFade > 0) && !(m.b.foreFade > 0)) return;
    const c = this.ctx;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [m.a, m.b]){
      if (!(f.foreFade > 0) || !f.foreRune || !f.alive) continue;
      const al = this._foreAl(f);
      if (!(al > 0.004)) continue;
      this._foreLine(c, m, f, al);
      this._foreMotes(c, m, f, al);
      this._foreRune(c, f, al);
    }
    c.restore();
  }
  /* the window's envelope: up over the eye's opening, down over the close */
  _foreAl(f){
    const o = clamp(f.foreAge / 0.5, 0, 1);
    return (1 - (1 - o) * (1 - o)) * f.foreFade;
  }
  /* where the bow's arrows leave: the nock, at the reach along the facing */
  _foreNock(m, f){
    const R = CONFIG.physics.ballR, L = R + f.w.reach * m.actMods.reach * f.reachMul;
    return [f.x + Math.cos(f.theta) * L, f.y + Math.sin(f.theta) * L];
  }
  /* THE SIGHT-LINE: thin, from the nock to the rune's rim. When the bow has
     turned onto the lead it is the arrows' own path; until then the angle
     between it and the bow is the turn still to make. */
  _foreLine(c, m, f, al){
    const [nx, ny] = this._foreNock(m, f), [rx, ry] = f.foreRune;
    const d = Math.hypot(rx - nx, ry - ny);
    if (!(d > 14 + 4)) return;
    const ux = (rx - nx) / d, uy = (ry - ny) / d;
    c.globalAlpha = al * 0.34;
    c.strokeStyle = f.aff.glow; c.lineWidth = 1.4;
    c.beginPath(); c.moveTo(nx, ny); c.lineTo(rx - ux * (14 + 2), ry - uy * (14 + 2)); c.stroke();
  }
  /* RUNE MOTES along the line, nock to rune (the design's field, drawn: a
     SPECS field fires once, at the cast, on the one ultFx slot, and this line
     moves with the bow for the whole window). Placed on the presentation
     clock: no state, no rng. */
  _foreMotes(c, m, f, al){
    const [nx, ny] = this._foreNock(m, f), [rx, ry] = f.foreRune;
    const d = Math.hypot(rx - nx, ry - ny);
    if (!(d > 14 + 4)) return;
    const ux = (rx - nx) / d, uy = (ry - ny) / d, L = d - 14 - 2;
    c.fillStyle = f.aff.glow;
    for (let j = 0; j < 5; j++){
      const p = (f.foreAge * 1.0 + j / 5) % 1;
      const x = nx + ux * L * p, y = ny + uy * L * p, s = 2.2;
      c.globalAlpha = al * 0.8 * Math.sin(Math.PI * p);
      c.beginPath();
      c.moveTo(x + ux * s * 1.6, y + uy * s * 1.6);
      c.lineTo(x - uy * s, y + ux * s);
      c.lineTo(x - ux * s * 1.6, y - uy * s * 1.6);
      c.lineTo(x + uy * s, y - ux * s);
      c.closePath(); c.fill();
    }
  }
  /* THE RUNE: the bow's grip sigil laid on the floor -- a ring and the
     triangle inside it, turning -- r 14, the school's glow at 0.5. */
  _foreRune(c, f, al){
    const [x, y] = f.foreRune, r = 14, P = f.aff;
    c.globalAlpha = al * 0.45;
    c.fillStyle = P.dark;
    c.beginPath(); c.arc(x, y, r + 2, 0, TAU); c.fill();
    c.globalAlpha = al * 0.5;
    c.strokeStyle = P.glow; c.lineWidth = 2;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke();
    const a0 = -f.foreAge * 1.2;
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = a0 + i * TAU / 3;
      const px = x + Math.cos(a) * r * 0.66, py = y + Math.sin(a) * r * 0.66;
      if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
    }
    c.closePath(); c.stroke();
  }
  drawForesightTop(m){
    const A = m.a, B = m.b;
    if (!(A.foreFade > 0) && !(B.foreFade > 0) && !A.foreFx.length && !B.foreFx.length) return;
    const c = this.ctx;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const s of m.shots){
      const f = m[s.own];
      if (!f || !(f.foreFade > 0) || s.stuck) continue;
      const al = this._foreAl(f);
      if (!(al > 0.004)) continue;
      this._foreTrail(c, s, f.aff, al);
      this._foreGlyph(c, s, f.aff, al);
    }
    for (const f of [A, B]){
      const foe = f === A ? B : A;
      if (!f.foreFx.length || !foe.alive) continue;
      for (const q of f.foreFx) this._foreFlare(c, foe, q, f.aff);
    }
    c.restore();
  }
  /* A SHORT CORE TRAIL, drawn from the velocity like the arrow's own streak,
     so a window arrow reads as a different arrow at any size. */
  _foreTrail(c, s, P, al){
    const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
    const tl = Math.min(120, sp * 0.15);
    const g = c.createLinearGradient(s.x - ux * tl, s.y - uy * tl, s.x, s.y);
    g.addColorStop(0, P.core + "00");
    g.addColorStop(1, P.core);
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = al * 0.9;
    c.strokeStyle = g; c.lineWidth = s.r * 0.22;
    c.beginPath(); c.moveTo(s.x - ux * tl, s.y - uy * tl); c.lineTo(s.x - ux * s.r * 0.4, s.y - uy * s.r * 0.4); c.stroke();
  }
  /* THE RUNE ON THE SHAFT: the grip sigil, small, a dark disc under it so it
     reads over the streak, riding behind the head. */
  _foreGlyph(c, s, P, al){
    const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
    const r = s.r * 0.34, x = s.x - ux * s.r * 1.15, y = s.y - uy * s.r * 1.15;
    c.globalCompositeOperation = "source-over";
    c.globalAlpha = al * 0.85;
    c.fillStyle = P.dark;
    c.beginPath(); c.arc(x, y, r * 1.25, 0, TAU); c.fill();
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = al;
    c.strokeStyle = P.glow; c.lineWidth = Math.max(1, s.r * 0.07);
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke();
    const a0 = Math.atan2(uy, ux);
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = a0 + i * TAU / 3;
      const px = x + Math.cos(a) * r * 0.62, py = y + Math.sin(a) * r * 0.62;
      if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
    }
    c.closePath(); c.stroke();
  }
  /* A LANDED WINDOW ARROW'S RUNE FLARE, on the foe: the sigil's ring thrown
     out round the shell and a triangle turning in it, over 0.3s. A ring and
     not a disc, so no ball -- the white sanctified one included -- is lit
     over its own body (CLAUDE.md section 4.1b). */
  _foreFlare(c, foe, q, P){
    const k = clamp(q.t / 0.6, 0, 1);
    if (k >= 1) return;
    const R = CONFIG.physics.ballR, e = 1 - Math.pow(1 - k, 3);
    const r = R + 4 + 20 * e;
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = (1 - k) * 0.9;
    c.strokeStyle = P.glow; c.lineWidth = 3.2 * (1 - k) + 0.8;
    c.beginPath(); c.arc(foe.x, foe.y, r, 0, TAU); c.stroke();
    c.globalAlpha = (1 - k) * 0.75;
    c.strokeStyle = P.core; c.lineWidth = 2.2 * (1 - k) + 0.6;
    const a0 = q.n * 2.1 + k * 1.4;
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = a0 + i * TAU / 3;
      const px = foe.x + Math.cos(a) * (r + 6), py = foe.y + Math.sin(a) * (r + 6);
      const bx = foe.x + Math.cos(a) * (r - 2), by = foe.y + Math.sin(a) * (r - 2);
      c.moveTo(bx, by); c.lineTo(px, py);
    }
    c.stroke();
  }
  /* THE RUNE-EYE on the caster's glass: a sigil ring round the shell in the
     school's core, drawn on over the opening, and an eye across the glass
     whose lids part over the opening and meet again over the close. The iris
     looks at the rune. STROKES AND NO FILL: the health level reads through
     the eye (91% of its contrast kept, median, where a dark almond kept 83%
     and 28% at worst), and nothing here is light added over the body. */
  _foreEye(c, f, R){
    const o = clamp(f.foreAge / 0.5, 0, 1), eo = 1 - (1 - o) * (1 - o);
    const open = eo * f.foreFade, P = f.aff;
    if (!(open > 0.004)) return;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    /* the sigil ring, sweeping round from the top */
    c.globalAlpha = 0.8 * f.foreFade;
    c.strokeStyle = P.core; c.lineWidth = 2.4;
    c.beginPath(); c.arc(f.x, f.y, R + 5, -Math.PI / 2, -Math.PI / 2 + TAU * eo); c.stroke();
    const t0 = f.foreAge * 0.6;
    c.lineWidth = 2;
    c.beginPath();
    for (let i = 0; i < 6; i++){
      const a = t0 + i * TAU / 6;
      if (((a + Math.PI / 2) % TAU + TAU) % TAU > TAU * eo) continue;
      c.moveTo(f.x + Math.cos(a) * (R + 2), f.y + Math.sin(a) * (R + 2));
      c.lineTo(f.x + Math.cos(a) * (R + 9), f.y + Math.sin(a) * (R + 9));
    }
    c.stroke();
    /* the eye */
    const EW = R * 0.80, EH = R * 0.42 * open;
    const lids = () => {
      c.beginPath();
      c.moveTo(f.x - EW, f.y);
      c.quadraticCurveTo(f.x, f.y - EH * 2, f.x + EW, f.y);
      c.quadraticCurveTo(f.x, f.y + EH * 2, f.x - EW, f.y);
      c.closePath();
    };
    c.globalAlpha = 1;
    c.save();
    lids(); c.clip();
    let lx = 0, ly = 0;
    if (f.foreRune){
      const dx = f.foreRune[0] - f.x, dy = f.foreRune[1] - f.y, d = Math.hypot(dx, dy) || 1;
      lx = dx / d * R * 0.22; ly = dy / d * R * 0.10;
    }
    c.fillStyle = P.core;
    c.beginPath(); c.arc(f.x + lx, f.y + ly, R * 0.27, 0, TAU); c.fill();
    c.strokeStyle = P.dark; c.lineWidth = 1.6; c.stroke();
    c.fillStyle = P.glow;
    c.beginPath(); c.arc(f.x + lx, f.y + ly, R * 0.11, 0, TAU); c.fill();
    c.restore();
    lids();
    c.strokeStyle = P.dark; c.lineWidth = 4.2; c.stroke();
    c.strokeStyle = P.glow; c.lineWidth = 1.6; c.stroke();
    c.restore();
  }

  drawMotes(m){
'''),

]

# The names stage 6 adds, free on the base (`drawSigils` / `m.sigils` are
# Converse's, `vine` / `tickVines` the Thicket's; `sight` is only stage 2's).
S6_NAMES = ("tickForesight", "drawForesight", "_foreEye", "foreFade", '"oracle-sigil"',
            '"oracle-hex"', '"oracle-close"', 'w === "oracle"')
# What stage 6's ADDED code may write: its own fore* fields, the canvas, a
# tag's count (`val`), a flare record's clock, and an oscillator's pitch.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("fore") or obj == "c" or prop == "val"
               or (prop == "t" and obj.endswith("]"))
               or (obj, prop) == ("frequency", "value"))

STAGE_OUT = {"1": "sc-oracle", "2": "sc-oracle-aim", "3": "sc-oracle-sight",
             "5": "sc-oracle-b{blade}", "6": "sc-oracle-fx"}


def S5():
    b = TUNED["dmg"]
    return [
    ("the blade: at the crossing",
     f'''  {{ id:"oracle", name:"Oracle", aff:"runic", shape:"bow",
    {PROFILE.format(dmg=BLADE0)}''',
     f'''  {{ id:"oracle", name:"Oracle", aff:"runic", shape:"bow",
    {PROFILE.format(dmg=b)}'''),
    ]


# the stage-5 row as a module-level table, so chain_audit (which imports this
# builder and reads its (label, old, new) tables) sees it too
S5_ROWS = S5() if TUNED else []


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


def assert_base(code: str) -> None:
    """THE BASE, BY CONTENT: what this builder copies and what its inserts need."""
    # the bow type's profile, on the lab's donor (its blade may move; the profile may not)
    row = " ".join(relic_row(code, "ironhail").split())
    prof = re.escape(PROFILE).replace(r"\{dmg\}", r"[0-9.]+")
    if not re.search(prof, row) or " ".join(SHOT.split()) not in row:
        raise SystemExit("the bow type's profile has moved on Ironhail's row -- the "
                         "donor is not what this builder copies")
    for v in RUNIC:
        r = relic_row(code, v)
        if "aff:\"runic\"" not in r or "onHit:{ hex:1 }" not in r:
            raise SystemExit(f"{v} does not carry the school's channel, onHit hex 1")
    if not re.search(r"hex:\s*\{ name:\"Hex\",\s*maxStacks:5,", code):
        raise SystemExit("STATUS.hex has moved")
    if "if (!(g > 0)) return Math.atan2(dy, dx);" not in code:
        raise SystemExit("ballisticAngle is no longer atan2 at grav 0")
    # the ranged branch the aim replaces, and the order the second hex needs
    rh = code.find("  resolveHit(self, foe, hx, hy, seg, mul, over){")
    loop = code.find("(over && over.onHit) || self.w.onHit || {})){", rh)
    fig = code.find("if (mul === undefined && self.ultDeadfall && foe.alive", loop)
    tc = code.find("  tickCharge(f, foe, dt){", rh)
    if not (0 <= rh < loop < fig < tc):
        raise SystemExit("resolveHit's onHit loop is not where the second hex goes")
    if not re.search(r"else if \(f\.stun > 0\)\{\s*\}\s*else if \(f\.w\.mode === \"swing\"\)\{"
                     r"[\s\S]{0,260}?\} else \{\s*f\.theta \+= spin \* dt \* f\.spinDir;\s*\}", code):
        raise SystemExit("tickWeapon's ranged branch has moved")
    if "this.tickShots(dt);" not in code or code.find("this.tickShots(dt);") > code.find("this.tickTendril(dt);"):
        raise SystemExit("the window tickers no longer run after tickShots")


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

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
        raise SystemExit("the source has CRLF line endings -- not a chain link")
    s = s0
    print(f"\nORACLE / FORESIGHT -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    assert_base(code)
    if A.stage == "1":
        for name in ("ultSight", "sightTally", "tickSight", 'kind:"sight"', "Foresight",
                     'id:"oracle"', 'name:"Oracle"'):
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  by content: the bow profile (Ironhail's row), the runic channel, hex, "
          "ballisticAngle at grav 0, the ranged branch, resolveHit's onHit loop")

    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultSight" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultSight" not in code or "hex:0," not in relic_ult(code):
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["hex"])
        elif A.stage == "6":
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
                raise SystemExit("stage 5 is not measured yet (TUNED is None)")
            if (f'hex:{ULT["hex"]},' not in relic_ult(code)
                    or f"dmg:{BLADE0}," not in relic_row(code, RELIC)):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5(), ult_block(ULT["charge"], ULT["hex"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Oracle's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    row = " ".join(relic_row(out_code, RELIC).split())
    blade = TUNED["dmg"] if A.stage in ("5", "6") else BLADE0
    if (" ".join(PROFILE.format(dmg=blade).split()) not in row or " ".join(SHOT.split()) not in row
            or "onHit:{ hex:1 }" not in row or 'aff:"runic", shape:"bow"' not in row):
        raise SystemExit(f"REFUSING TO WRITE -- Oracle's row is not the bow at {blade}, runic")
    print(f"  ok    row   the bow profile at dmg {blade}, onHit hex 1")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor aside)
    # draws no RNG, never takes the one ultFx slot (open item 25), calls nothing
    # that applies, hurts, heals, resolves, shatters, casts or knocks, and writes
    # only what S6_WRITE_OK names. The probe's [8] / [9] and engine_ab are the
    # dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|beat|resolveHit|shatter|fireUlt|knock|spawnShot)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
    for label, old, new in S1 + S2 + S3 + (S5() if TUNED else []) + S6:
        # WHAT THE INSERT ADDS: an anchor it re-emits is the base's, not the insert's.
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\b(pin|pinMax|pinFree|pinV|hitStop|stun)\s*(=[^=]|\+=|-=)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' pins, stuns or "
                             "stops the world (the design: none)")
        if re.search(r"\.(hurt|beat|knock|resolveHit|shatter)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' deals, files or "
                             "knocks (the design: the second hex only)")
    # CHAIN_AUDIT CAN WATCH EVERY INSERT (the v105 review). The line chain_audit
    # recognises an insert by -- its own `_cands`, the first one the build
    # contains -- must be in this output EXACTLY ONCE. The aim's first draft
    # shared its longest line with Tendril's seek, so a carry that swallowed the
    # aim would still have read "ok" off Tendril's copy.
    sys.path.insert(0, str(HERE))
    from chain_audit import _cands
    done = {"1": S1, "2": S1 + S2, "3": S1 + S2 + S3, "5": S1 + S2 + S3 + (S5() if TUNED else []),
            "6": S1 + S2 + S3 + (S5() if TUNED else []) + S6}[A.stage]
    for label, old, new in done:
        mk = [l for l, _ in _cands(new, old) if s.count(l)]
        if not mk or s.count(mk[0]) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- chain_audit could not watch insert '{label}': "
                             f"its marker is in the output {s.count(mk[0]) if mk else 0}x "
                             f"({(mk[0] if mk else '')[:80]!r})")
    print(f"  ok    chain_audit's marker for each of the {len(done)} inserts is in the output once")
    if len(re.findall(r'kind:"sight"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one sight ultimate")
    ids = re.findall(r'\{ id:"([a-z]+)", name:"', out_code)
    if ids.count(RELIC) != 1 or ids[-1] != RELIC and A.stage == "1":
        raise SystemExit(f"REFUSING TO WRITE -- Oracle is not appended once at the end ({ids[-3:]})")
    print(f"  ok    one sight ultimate, Oracle's; no insert draws the RNG, takes the "
          f"ultFx slot, writes the shared weapon row, pins, stops or deals; "
          f"{len(ids)} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
