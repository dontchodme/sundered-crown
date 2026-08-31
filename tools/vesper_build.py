#!/usr/bin/env python3
"""VESPER. The vigil scythe, and THE SENTINEL -- the first thing in this game
that persists, turns, and is paid for with the armour it is wearing.

    python vesper_build.py --src ../02-chain/sc-thornshear.html \
                           --out ../02-chain/sc-vesper.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in `06-docs/v48/vesper-design-v48.md`:

    "pink sycthes ult -- when the ult fires the scythe charges up (with a loud
     glowing animation) and then fires a targeted beam (thick, at least half
     the thickness of an artifact) the beam has limited range and points at
     the tip. the beam slowly rotates to track the enemy ball. while it
     persists it does rapid ticks of damage that push enemies towards its tip
     where it does bonus damage. the beam uses the scythes banked shield to
     increase its duration."

"Pink" is the school naming itself: `AFFINITIES.vigil.core` is `#F06BB8`.

EVERY GEOMETRIC SENTENCE WAS PRICED BEFORE THIS FILE WAS OPENED
(`beam_probe.py`, 14/14, re-run at THIS tip 2026-08-30 and unmoved). What the
measurement decided, and every one of these is a thing this build does
differently from the sentence that asked for it:

    THE POOL      READ AT THE CAST IT IS A MEDIAN OF ZERO. 59% of casts find
                  an empty shell at this tip (57% at the last one), because
                  charge is pure wall time and the ward is up 42% of the
                  fight -- the two are uncorrelated by construction. So the
                  beam DRINKS CONTINUOUSLY, which is Aegis's own precedent
                  ("feed the wall while it stands"), and the loop closes: a
                  four-second beam banks 8.1 points while it runs.
    THE TIP       FREE. Mounting the beam on a blade that orbits at 3.2 rad/s
                  costs 4.9 points of time-on-target against a turn-rate axis
                  that moves the same number by 43. So `points at the tip`
                  is kept, and it is kept because it is cheap.
    THE TRACKING  RICK CHOSE THE LIGHTHOUSE. Offered fast tracking, slow
                  tracking with the damage redesigned, or a lock-on, he took
                  the second -- so at turn 1.6 the beam holds the quarry for
                  0.28s at a time and breaks 3.5 times in a four-second
                  window, and THE UNIT OF THE MECHANIC IS A PASS.
    THE PUSH      CUT. Six times the force moves the quarry from 0.56 to 0.59
                  of the way down the beam, because you cannot push a thing
                  along a line for 0.3 seconds. See "WHAT IS NOT IN THIS
                  BUILD" below -- it is not silently dropped, it is Rick's.

## THE UNIT IS A PASS, AND THAT IS THE ONE THING TO GET RIGHT

A pass BEGINS when the ball enters the beam volume and ENDS when it leaves. A
pass deals its damage ONCE, on entry. A pass that reached the far quarter AT
ANY POINT deals the bonus, once, at the instant it first gets there.

DO NOT read this as a per-frame tick with a hit cooldown. That is the lance
design and it is the one Rick did not take: `CONFIG.combat.hitCd` is 0.45s and
a 0.28s mean contact would make "rapid ticks" mean "one tick, sometimes".
`vesper_relic_probe [2]` asserts entering, leaving and re-entering is TWO
passes and that a frame inside a pass is not a pass.

## THE HALL SWEEPS THE BEAM AS MUCH AS THE BEAM SWEEPS THE HALL

A beam that does not turn at all is still crossed 2.2 times in four seconds;
tracking at 1.6 takes that to 3.5. That is worth saying in the builder because
it is what the ART is built around: a slow line laid across a dark room that a
ballistic ball keeps blundering through, brightest at the far end.

## WHAT IS NOT IN THIS BUILD, AND IT IS NAMED RATHER THAN DROPPED

**THE PUSH.** §1's "push enemies towards its tip" is measured inert (design
§5) and the build brief's §3.4 says build it as a token shove for the picture
OR NOT AT ALL -- and that if it ships it must not be a dead knob. This project
already carries two dead knobs it cannot get rid of (`shot.life: 3.4` on all
five bows, open item 7; `s.snap`, open item 13) and both are in the open items
list precisely because a knob that does nothing teaches the next person they
are protected when they are not. So it is CUT, and it is Rick's to put back:
the honest options are a shove at the tip on the bonus (a different sentence),
or nothing. Open decision 1 of the write-up.

## EVERY NUMBER BELOW IS A PLACEHOLDER AND IS MARKED AS ONE

`dmg` must be bisected against all 26 opponents (v43 §6: bisect BEFORE reading
a cell's telemetry). `range` x `tipMul` is the sweep's main axis and between
them they set WHAT SHARE OF THE SENTINEL IS THE TIP, which is the question to
put to Rick -- the way v43 put "how much of Paradox IS the field" rather than
a win rate. `vesper_sweep.py` solves them.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# VESPER / THE SENTINEL. Both Rick's, and both from a SECOND spread -- the
# first four fighter names were all [modifier][guardian role] because Farwarden,
# Lightkeeper and Bulwarden are, which is v43 §15's error (generalising from a
# subset) for the second time in this project. Vesper is the evening star and
# the prayer said at nightfall, and `AFFINITIES.vigil.core` is #F06BB8 -- the
# pink of a sky just after sundown, so the name and the colour are one fact.
#
# SENTINEL names a POSTURE where Reprisal, Bulwark and Aegis all name a thing
# done. That is deliberate, it is Rick's, and it is not a slip.
#
# AND IT IS "SENTINEL", NOT "THE SENTINEL". Rick, 2026-08-30, off the
# first-look clip. The design doc and the build brief both wrote it with the
# article; he did not. The bare noun is also the register the roster actually
# uses -- Reprisal, Aegis, Bulwark, Retrace, Daybreak, Slagburst carry no
# article, and the two that do (the Winnowing, the Harrowing) are gerunds,
# where the article is doing grammatical work rather than decorative work.
RELIC_ID = "vesper"
RELIC_NAME = "Vesper"
ULT_NAME = "Sentinel"

# A PLACEHOLDER UNTIL RICK WORDS IT -- the scrunch card is one of the seven
# things this project asks him for, and it is one of the two still open on this
# relic. It says the mechanic twice, which is the rule Rick's own Winnowing
# wording taught (v47): the sweep, and then the thing that makes the sweep
# matter. It carries NO NUMBER -- Bulwarden's precedent, and
# `vesper_relic_probe` asserts that IF a percentage ever appears in this line
# it must equal the weapon's own field.
# AND THE FIRST WORDING WENT STALE THE MOMENT THE ORIGIN MOVED. It read
# "Sweeps a beam from the blade tip", which was true of the build Rick
# watched and false of the one he asked for thirty seconds later. A card
# that describes the previous build is v40's "5s" fault in words rather
# than in numbers.
ULT_TIP = "Sweeps a slow beam. Its far end deals bonus damage"

# A PLACEHOLDER, AND IT MUST BE BISECTED AGAINST THE WHOLE FIELD.
# The type ships 17.50 (Lastlight) .. 31.35 (Thornwake) -- the widest damage
# spread of any three-relic type at x1.79, because Lastlight pays for the
# Harrowing and Thornwake does not. Vesper pays for a four-second window AND
# for a school channel that re-prices at +15.2% delivered at this tip (the
# strongest cell on the row by seven points), so the expectation going in is
# that it lands NEAR LASTLIGHT rather than near Thornwake. That expectation is
# written here so `vesper_sweep` can refute it.
#
# v41 open decision 2 is why "the whole field" is in this comment: Bulwarden's
# dmg was bisected on a five-foe subset that read 50% and the full field read
# 55.2% on the same number.
#
# BISECTED, THEN CONFIRMED, AND THE CONFIRMATION IS NOT OPTIONAL.
# `vesper_sweep [2]` returned 16.04 against all 26 opponents with an escalating
# sample (1092 fights). Its last three steps read 42.9% / 45.3% / 44.6% across
# half a damage point at n=312 -- an ordering that is NOISE, because +-2.8pp of
# sampling error is wider than the effect of the interval being resolved. A
# bisection in that state lands wherever the last coin came down. Confirmed
# directly at n=1040 a point instead, and the crossing was 0.76 HIGHER than
# the bisection returned.
#
# SIZE THE BISECTION'S TOP TO THE INTERVAL IT ENDS ON, OR CONFIRM THE ANSWER
# WITH ONE WIDE DIRECT MEASUREMENT.
#
# THEN RICK MOVED THE ORIGIN TO THE BALL AND ASKED FOR A POINT ON THE END,
# AND BOTH CHANGED THE HIT VOLUME, SO ALL OF IT WAS RE-MEASURED. Two
# independent seed streams, n=1040 each, on the SHIPPED geometry:
#
#     dmg    seed A   seed B    mean
#    16.60    48.5%    49.0%    48.8%
#    17.20    49.5%    50.2%    49.9%    <- the crossing
#    17.80    51.9%    53.5%    52.7%
#    18.40    56.2%    56.2%    56.2%
#
# THE TAPER DID NOT MEASURABLY MOVE THIS NUMBER, and saying so is the point of
# writing it down. The ball-centred beam WITHOUT the point crossed at 17.50;
# with it, 17.25. That is 0.25 damage on a curve running ~5pp per damage
# point, against +-1.5pp on each measurement -- the two are the same number
# inside error. 17.25 ships because it is the better-measured of the two and
# it is measured on the geometry that actually ships, NOT because the point
# changed the balance. A later session reading a 0.25 move as a finding would
# be reading noise, which is the mistake this file has now made twice.
TUNED_VS = 17.25

# EVERY ONE OF THESE IS A PLACEHOLDER. The ones that are RICK'S rather than
# mine say so.
ULT = {
    # The roster band is 15..17 and both other vigil casters are 15/16.
    "charge":     16.0,
    # THE CHARGE-UP. §1's first sentence, and the design doc's open decision 1:
    # the one sentence `beam_probe` did not price, because an overlay cannot
    # measure a thing that changes when the fight can see it.
    #
    # 0.32 AND NOT 0.85 SINCE 2026-08-30. Rick, on the measured loss rate:
    # "if the wind up loses to stun that often we need to make it wind up
    # faster. its fine for it to lose sometimes but not that often."
    #
    # **AND SPEED ALONE DOES NOT FIX IT.** Measured against the four relics
    # that can apply a true stun, 8 seeds each:
    #
    #     wind   lost to the 4 hex appliers    control of 4
    #     0.85          51.2%                      0.0%
    #     0.60          48.8%                      0.0%
    #     0.45          41.5%                      0.0%
    #     0.32          40.2%   <- ships           0.0%
    #     0.22          34.5%                      0.0%
    #     0.14          21.0%                      0.0%
    #
    # A SIX-FOLD CUT IN LENGTH BUYS A HALVING OF THE LOSS RATE, and 0.14s is
    # seventeen frames -- not a telegraph, and the telegraph is the only
    # reason the wind-up exists. The curve is shallow because hex is not a
    # point event: `stunEvery` 1.15 is advanced by `dt * stacks`, so at five
    # stacks a stun is APPLIED every 0.23s, and `breakSpin` fires on every
    # application. A window of any length lands inside that comb.
    #
    # So 0.32 is Rick's instruction honoured as far as it goes -- 0.85 -> 0.32
    # is a real cut and still 38 frames of glow -- and the remaining 40% is a
    # STRUCTURAL question, not a speed one. See the write-up's open decisions:
    # a true stun could PAUSE the wind-up instead of cancelling it, which is
    # exactly the choice v44 put to Rick for the Crucible and exactly the one
    # he took there.
    "wind":        0.32,
    # THE BASE DURATION, before a single point of ward is drunk. The floor of
    # the ultimate: a Vesper that has landed NOTHING gets exactly this and no
    # more, and the probe asserts that loop closes.
    "dur":         4.0,
    # THE CEILING ON THE WHOLE WINDOW, drink included. Not a balance number so
    # much as a guarantee: a `drink` under the ward's own income would
    # otherwise be a beam that never ends, and an ultimate with no upper bound
    # is a timeout waiting to be discovered by somebody else (the aimedshot's
    # cap, same reasoning). Aegis's 9s window is the roster's longest and this
    # sits on it deliberately.
    "durcap":      9.0,
    # RADIANS A SECOND. **RICK'S**, and the whole design rests on it: he was
    # shown turn 0.8 / 1.6 / 3.2 / 6.0 against time-on-target 16.2% / 23.4% /
    # 42.3% / 59.5% and took the slow one with the damage redesigned around
    # sweeping. THE DESIGN IS THE LIGHTHOUSE, NOT THE LANCE.
    "turn":        1.6,
    # HOW FAR IT REACHES. THE SWEEP'S MAIN AXIS, and the cleanest trade in the
    # design: range 180 -> 2.8 passes with 73% reaching the tip, 300 -> 3.5 at
    # 60%, 420 -> 3.8 at 45%. §1's "limited range" turns out not to be a
    # restriction on the ultimate but the thing that makes its own bonus fire.
    "range":     300.0,
    # HALF-WIDTH. §1 asked for "at least half the thickness of an artifact",
    # and an artifact is 68 across, so 17 is the FLOOR the sentence sets and
    # not a starting point chosen freely. Thickness is the knob that buys
    # contact where the turn rate must not: 17 -> 26 moves the mean pass 0.28s
    # -> 0.30s and passes 3.5 -> 3.7.
    # 28 AND NOT 22 SINCE 2026-08-30, AND IT IS A LOOK CALL INSIDE A MEASURED
    # BAND. Rick, on the first-look clip: "it needs to be this quality or
    # better", against a reference frame whose shaft is a substantial object.
    # At 22 the beam rendered as a bright line; `beam_probe [4]` prices the
    # whole 17 -> 26 range at +0.02s of mean pass and +0.2 passes a window, so
    # thickness is very nearly free in the mechanic and is not free at all in
    # the picture. 28 is a beam 56 wide against a 68-wide artifact -- clearly
    # more than §1's "at least half" floor of 34, and still narrower than a
    # relic.
    "half":       28.0,
    # HOW LONG THE SHAFT TAKES TO REACH ITS FULL LENGTH. **RICK'S**, 2026-08-30:
    # "it also needs an animation showing it grow", against a reference frame
    # he supplied. THE GROWTH IS IN THE GEOMETRY AND NOT ONLY IN THE PICTURE --
    # `beamLen` is read by `inBeam`, so a half-grown beam has a half-length hit
    # volume and cannot touch anything the viewer cannot see it touching.
    # Drawing a growth the simulation did not have would be v43's hexagon with
    # a clock on it.
    "open":        0.30,
    # AND HOW LONG IT TAKES TO GO OUT, retracting rather than being cut. Same
    # rule: it is in `beamLen`, so the volume goes with it.
    "close":       0.22,
    # THE POINT. **RICK'S**, 2026-08-30: "it needs to end in a point. like the
    # tip of a dull pencil." `taper` is where the cone starts as a fraction of
    # the length and `tipw` is the half-width at the very end as a fraction of
    # `half` -- so 0.62 / 0.26 is a long gentle cone ending BLUNT rather than
    # a needle, which is what "dull pencil" asks for and what a needle would
    # not be.
    #
    # AND IT IS IN THE HIT TEST. `beamHalfAt` is read by `inBeam`, so the
    # volume tapers with the picture. A drawn taper over a rectangular volume
    # would put the disagreement exactly where the tip bonus fires, which is
    # the worst possible place for it -- v43's hexagon, aimed at the mechanic.
    "taper":       0.62,
    "tipw":        0.26,
    # WHERE THE FAR QUARTER BEGINS, as a fraction of the CURRENT length. §1's
    # "towards its tip where it does bonus damage" -- and it is the current
    # length rather than `range`, so the lit band the viewer sees IS the band
    # that pays, at every instant of the growth.
    "tipfrom":     0.75,
    # WHAT A PASS IS WORTH. Absolute, the way every other ultimate in this game
    # prices its own damage, so the tuner moving `dmg` does not move it.
    "passdmg":     9.0,
    # AND WHAT THE TIP IS WORTH, as a MULTIPLE of a plain pass -- so this
    # number means exactly what the sweep is being asked to choose. A tip pass
    # totals `passdmg * tipmul`; the bonus lands as its own second hit so the
    # viewer can see two events rather than one bigger number.
    "tipmul":      1.8,
    # SECONDS BETWEEN HUM RE-STRIKES. **RICK'S**, 2026-08-30: he heard four
    # sustains as full 3.6-second runs with passes and a tip over the top and
    # said "1. dynamo is perfect" -- `sentinel_hum_lab.py`, first spread, one
    # round trip, which is rule 2 working exactly as it is written.
    #
    # 0.24 IS THE CHARACTER AND NOT A DETAIL. The decays are 0.42s long, so at
    # 0.24 they OVERLAP into a continuous floor; slower and it stutters,
    # faster and it fuses into one buzz. The spike storm's `chuff` comment is
    # the precedent and the warning both.
    #
    # AND IT IS ALSO THE AUDIO'S SAMPLE RATE FOR "AM I CONNECTING", which is
    # what Rick asked this sound to carry. The mean pass is 0.25s against this
    # 0.24s -- so close that the strike clock and the contact can beat against
    # each other, which is why the tick tracks the PEAK load since the last
    # strike rather than the instantaneous one. Moving this number without
    # reading that comment is how the cue starts missing passes.
    "hum":         0.24,
    # POINTS OF WARD A SECOND THE BEAM DRINKS. The measured income is about
    # 2.0 a second from the blade's own blows during the window, so a drink
    # ABOVE that empties the plate and a drink BELOW it is fed for free.
    # SWEEP THIS AGAINST `dur` -- brief §3.2 -- rather than picking it.
    "drink":       6.0,
    # SECONDS BOUGHT PER POINT DRUNK. At drink 6.0 a full 90-point plate buys
    # 10.8s and `durcap` is what actually stops it; at the measured 12ish mean
    # pool it buys about 1.4s on top of the base.
    "durper":      0.12,
}


# --------------------------------------------------------------- the relic --

RELIC_NEW = r'''    blurb:"A hedge-blade that lets go of its edges. What it throws comes back off the wall bigger than it left." },

  /* VESPER -- the vigil scythe, and the twenty-seventh relic. Physics are
     Thornwake's and Lastlight's and Foregone's exactly (the type owns them,
     field for field); the school owns Ward and the pink, and SHAPES._scythe
     has drawn this weapon since before it existed.

     THE CELL, priced by DELIVERED EFFECT and not by occupancy
     (`row_price.py`, re-run at this tip):

       +15.2% -- THE STRONGEST CHANNEL ON THE SCYTHE ROW BY SEVEN POINTS,
       against bloodsworn's +8.0%, dwarven's +6.0% and umbral's -1.2%. And it
       is the first time a VIGIL cell has been priced at all: the school has
       no `onHit` channel, so `cell_survey` prints vigil as a dash on every
       row and has never ranked one against its own type.

       AND THE LIFT IS NOT FLAT ACROSS THE FIELD. Split by the foe's mode it
       is +34.0% against RANGED, +17.5% against chain, +13.3% against spin and
       +2.9% against swing -- the plate is worth most against the thing that
       lands little blows from across the hall, which is the exact opposite
       shape to the relic built immediately before it.

       THE TYPE LANDS A BLOW EVERY 5.31 SECONDS AGAINST A WARD THAT LIVES 5.0,
       and that turned out NOT to be the leak: the plate ends by being
       SHATTERED 4.8 times a minute and by expiring 0.9 times, and the scythe
       keeps 89% of everything it banks.

     So the weapon banks well and spends it on being hit. THE SENTINEL SPENDS
     IT ON BEING LIT: the plate is the fuel, drunk continuously while the beam
     stands, and the beam is what the blade's own blows are paying for.

     `dmg` is a PLACEHOLDER (vesper_build.TUNED_VS) and MUST be bisected. */
  { id:"%ID%", name:"%NAME%", aff:"vigil", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:%DMG%, spin:3.2, mode:"spin", mass:2.4,
    onSelf:{ ward:1 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"sentinel",
          wind:%WIND%, dur:%DUR%, durCap:%DURCAP%,
          turn:%TURN%, range:%RANGE%, half:%HALF%,
          /* THE SHAFT GROWS. Rick's, off a reference frame, and it is in the
             GEOMETRY: `beamLen` is what `inBeam` measures against, so the hit
             volume opens and closes with the picture. */
          open:%OPEN%, close:%CLOSE%,
          /* AND IT COMES TO A BLUNT POINT. Rick's, off the v2 clip, and it is
             in `beamHalfAt` -- which `inBeam` reads -- so the tested volume
             tapers with the drawn one. */
          taper:%TAPER%, tipW:%TIPW%,
          tipFrom:%TIPFROM%, passDmg:%PASSDMG%, tipMul:%TIPMUL%,
          /* THE POOL IS DRUNK WHILE THE BEAM STANDS, not read at the cast.
             §1's last sentence, and the ONE sentence in it that the
             measurement changed outright: read at the cast the pool is a
             median of ZERO over 290 casts and 59% of casts find an empty
             shell. Aegis's `feed` is the precedent and it was added for
             exactly this measurement one relic-family ago. */
          drink:%DRINK%, durPer:%DURPER%,
          /* AND IT HUMS WHILE IT STANDS. Rick's, off a rendered spread. */
          hum:%HUM%,
          /* THE NUMBER IN THIS LINE IS SUBSTITUTED, not typed. v40 shipped a
             card reading "5s" after a sweep moved the number to 8.1 and
             nothing caught it, because verify.py only asks that a tip EXISTS.
             And verify.py fails an ult tip over 72 characters.

             A PLACEHOLDER UNTIL RICK WORDS IT. It carries no number, which is
             Bulwarden's precedent and is guarded by the probe. */
          tip:"%TIP%" },
    blurb:"A watch kept with a light. It does not chase — it turns, and the room walks into it." },

];'''


# ------------------------------------------------------------ fighter state --

FIGHTER_STATE_NEW = r'''    this.ultWinnow = null;
    /* {phase, t, dur, ang, drunk, passes, tips, in, tipped, best} while the
       Sentinel is winding or standing. null on every other relic and on this
       one outside its own window, which is the whole zero-burden argument:
       `tickSentinel` returns on its first line, `_drawBeam` returns on its
       first line, and `breakSpin`'s new clause is a comparison against null
       on a field nothing else writes. */
    this.ultBeam = null;'''


# ---------------------------------------------------------------- the cast --

FIRE_ULT_NEW = r'''    if (u.kind === "sentinel"){
      /* NOTHING RESOLVES HERE, AND NOTHING RESOLVES FOR ANOTHER `wind`
         SECONDS EITHER. §1's first sentence is a charge-up, so the cast
         starts a wind-up and the beam is what the wind-up produces -- the
         same two-phase shape as Bloodmill's, and it uses the same hook to
         lose it (`breakSpin`).

         THE WIND-UP IS THE ONLY WINDOW IN WHICH THIS ULTIMATE CAN BE TAKEN
         AWAY, and that is deliberate rather than an omission: once the beam
         is lit it stands, because a light that could be switched off by a
         blow is a light nobody would build a set-piece around. What a stun
         does to a STANDING beam is stop the blade turning, which stops the
         ORIGIN moving and not the bearing -- the weapon is locked, the watch
         is not.

         THE BEARING IS NOT SET HERE. It is taken at the release, off the
         quarry's position at that instant, so a wind-up spent watching the
         ball cross the hall does not open pointing where it used to be. */
      f.ultBeam = { phase: "wind", t: 0, dur: u.dur, ang: 0, drunk: 0,
                    passes: 0, tips: 0, in: false, tipped: false, best: 0,
                    /* the hum's clock, its strike index, how hard it is
                       working right now, and the HARDEST it has worked since
                       the last strike -- see the tick */
                    hum: 0, hn: 0, load: 0, peak: 0 };
      /* The fx clock runs at 2x sim time -- `decay()` calls `tickPresentation`
         once directly and once through `decayImpactOnly` -- so every `life`
         in this engine is in half-seconds. The window can run to `durCap`, so
         the set-piece is sized for the longest one it can be asked to cover.
         The map entry in the table above is only the fallback if this is
         missed. */
      this.ultFx.life = (u.wind + u.durCap + 0.6) * 2;
      return;
    }

    if (u.kind === "ballista"){'''


# ------------------------------------------------------- losing the wind-up --

BREAK_SPIN_NEW = r'''    /* AND THE SENTINEL'S CHARGE-UP, which is the second ultimate to ask this
       hook for the same thing and the first to ask it while carrying no
       `ultSpin` at all -- so it has to be ABOVE the early return, exactly the
       way the Crucible's hold is and for exactly the same reason.

       ONLY THE WIND-UP. A standing beam is not interruptible (see the cast),
       so this is gated on the phase and not on the field: a true stun that
       arrives 0.9 seconds into a four-second window finds nothing to take.

       THE CAST IS LOST OUTRIGHT rather than delayed. v44 offered Rick three
       strengths for the Crucible and he took the mildest, which is why that
       one is a delay -- but the Crucible's hold has no phase to be cancelled
       and this one is a charge-up with nothing behind it, which is the shape
       `windCap` and Bloodmill already established. ANNOUNCED, never silent:
       the Harrowing shipped an 11.5% dud rate nobody could see. */
    if (trueFor !== undefined && f.ultBeam && f.ultBeam.phase === "wind"){
      f.ultBeam = null;
      this.spawnFx(f.x, f.y, AFFINITIES.vigil.core, 14, 190, 0.5, 3.0);
      SFX.play("ult", { w: "redflail-break" });
      this.note(`${f.w.name} — the watch goes out`);
    }
    if (!f.ultSpin) return;'''


# --------------------------------------------------------------- the window --

TICK_SENTINEL_NEW = r'''  /* ----------------------------------------------------------- SENTINEL --
     THE SENTINEL. A charge-up, and then a slow line laid across the hall out
     of the blade's own tip, fed by the plate the blade has been banking all
     fight.

     THE UNIT IS A PASS AND NOT A FRAME, and that is Rick's call with the
     numbers in front of him. At the tracking rate §1 asks for, the beam holds
     the quarry for a mean 0.28 seconds and breaks 3.5 times in a four-second
     window -- so "while it persists it does rapid ticks" describes a thing
     that does not persist. Offered fast tracking (which makes the sentence
     work as written), slow tracking with the damage redesigned around
     sweeping, or a lock-on, he took the second.

       A PASS BEGINS      when the ball enters the volume
       A PASS ENDS        when it leaves
       A PASS PAYS ONCE   on entry
       AND THE TIP        pays once more, the instant the pass first reaches
                          the far quarter -- AT ANY POINT during the pass, not
                          where it happened to be on the last frame

     AND THE HALL SWEEPS THE BEAM AS MUCH AS THE BEAM SWEEPS THE HALL. A beam
     that does not turn AT ALL is still crossed 2.2 times in four seconds;
     tracking at 1.6 takes that to 3.5. Nothing in this game steers, so what
     produces most of the contact is a ballistic ball blundering through a
     line -- which is the honest description of this ultimate and is what the
     art is built around.

     ORDER. Called after the fighter loop, so `move` has already run and the
     positions are current, and before `tickHits`. Exactly where `tickStasis`
     and `tickAegis` sit, and for the same reason.

     RETURNS ON ITS FIRST LINE for every relic that is not casting. */
  tickSentinel(dt){
    if (!this.a.ultBeam && !this.b.ultBeam) return;
    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const B = f.ultBeam;
      if (!B) continue;
      const u = f.w.ult;
      /* A DEAD CASTER'S WATCH GOES OUT. Not a kindness -- a beam sweeping out
         of a corpse would keep dealing damage after the killing blow. */
      if (!f.alive){ f.ultBeam = null; continue; }
      B.t += dt;

      if (B.phase === "wind"){
        if (B.t < u.wind) continue;
        /* THE RELEASE. The bearing is taken HERE and off the quarry's
           position at this instant, so a wind-up spent watching the ball
           cross the hall does not open the beam pointing where it used to
           be. From here on `B.ang` is the beam's OWN angle and the weapon's
           theta is not read by the bearing again -- Aegis's rule, one relic
           over. */
        const o0 = this.beamOrigin(f);
        B.phase = "beam"; B.t = 0;
        /* the hum starts on the frame the beam stands up, not at the cast --
           the wind-up has its own voice and the two must not overlap */
        B.hum = 0; B.hn = 0; B.load = 0; B.peak = 0;
        B.ang = Math.atan2(foe.y - o0[1], foe.x - o0[0]);
        this.shake = Math.min(38, this.shake + 12);
        this.ring(o0[0], o0[1], f.aff.core, 8, 120, 0.40, 6);
        this.spawnFx(o0[0], o0[1], f.aff.glow, 22, 260, 0.50, 3.4);
        SFX.play("ult", { w: "vesper-open" });
        continue;
      }

      /* AND A WATCH DOES NOT SWEEP A CORPSE, however the corpse got there.
         The two guards below the pass catch the beam's OWN killing blow on
         the frame it lands; this one catches every other way the quarry can
         die while the window is standing -- a blade blow in `tickHits`, a
         ward shatter, a projectile -- and it has to exist separately because
         `checkEnd` RETURNS EARLY while a killFlight is up ("the slain ball
         has a wall to meet first"), so the match is not over and `step()`
         keeps reaching this function. Measured before it was written:
         `vesper_relic_probe [7]` counted 7 steps of standing beam over a dead
         quarry across 57 windows without it. Seven frames is nothing to the
         simulation and it is a picture fault, which is this project's own
         defect class. */
      if (!foe.alive || foe.hp <= 0){ f.ultBeam = null; continue; }

      /* THE DRINK, AND IT IS CONTINUOUS. §1's last sentence, and the one the
         measurement changed outright: read at the cast the pool is a MEDIAN
         OF ZERO and 59% of casts find an empty shell, because charge is pure
         wall time and the ward is up 42% of the fight. Aegis was changed to
         "feed the wall while it stands" for exactly this measurement; this is
         the same shape pointed the other way -- Aegis banks INTO the wall,
         the Sentinel drinks OUT of the plate.

         SO THE BLADE PAYS FOR THE BEAM WHILE THE BEAM IS STANDING. A Vesper
         landing blows during its own window is refilling the thing it is
         burning, at a measured 2.0 points a second. A Vesper landing nothing
         gets `dur` and not one frame more, and the probe asserts that. */
      const got = this.drinkWard(f, u.drink * dt);
      if (got > 0){
        B.drunk += got;
        B.dur = Math.min(u.durCap, B.dur + got * u.durPer);
      }
      if (B.t >= B.dur){ f.ultBeam = null; continue; }

      /* THE HUM, AND IT IS THE ONLY REASON THIS BEAM IS NOT SILENT.
         Sentinel's other four voices are all EVENTS -- the wind-up, the
         release, a pass, the tip -- and the beam is a STATE that stands for
         four to nine seconds. Without this the set-piece makes no sound for
         most of its own duration, which is v42's silent ultimate with the
         volume turned down instead of off, and just as invisible to every
         probe in this repo.

         A RE-STRIKE AND NOT A HELD NOTE, because this toolkit cannot hold
         one: `_tone` ends on an exponential ramp over its whole length and
         `_burst` does not loop its 0.6s noise buffer. Both are chain-wide
         (CLAUDE.md §4.5, open item 6) and neither is a relic build's to fix,
         so this is written inside their envelope the way v43's was. The
         decays are 0.42s against a 0.24s cadence, so they OVERLAP into a
         floor rather than repeating as a stutter.

         `hn` IS CARRIED INTO THE VOICE so the pair can detune across the run
         -- a hum that plays one identical sample forty times is a buzz, which
         is the spike storm's `chuff` warning arriving on a different relic.
         Nothing in the simulation reads it, and `SFX.play` returns on its
         first line headless, so `engine_ab` is expected to come back
         IDENTICAL. */
      /* THE LOAD. **RICK'S**, 2026-08-30: "we need the sound effect to reflect
         weather or not the beam is connecting. the audio should be our cue
         that its doing damage", then "so a static hum and then the sawtooth
         of dynamo is the damage connecting". So the hum is TWO layers: a flat
         bed that plays whenever the beam stands, and the dynamo's sawtooth
         pair ON TOP OF IT in proportion to this number.

         AND IT IS DRIVEN BY THE PAYMENT, NOT BY THE CONTACT. The first cut
         held the load up for as long as the beam was touching the quarry, and
         the audition off a real window refuted it: `..##########::...` --
         twelve loaded strikes, 2.4 seconds of dynamo, for TWO payments. The
         beam pays ONCE PER PASS ON ENTRY, so a long contact is not more
         damage, and a cue that swells for the whole of it says "lots of
         damage" while one hit is landing. Rick asked for the audio to be the
         cue that it IS doing damage; sustained contact is a different fact.

         So `beamHit` sets this to 1 and nothing else raises it, and it decays
         at 3.4/s -- about 0.3s of swell, a little over one strike at the
         0.24s cadence. THE NUMBER OF SWELLS IN A WINDOW IS THE NUMBER OF
         TIMES THE RELIC WAS PAID, which is the sentence the sound is being
         asked to say.

         AND `peak` IS WHY NO CONNECTION IS EVER MISSED. The mean pass is
         0.25s and the hum strikes every 0.24s, so sampling `load` AT the
         strike would silently drop passes that fall between two strikes --
         the audio cue would be wrong exactly when it matters, and nothing in
         this repo would say so. `peak` is the hardest the beam has worked
         since the last strike, so a pass anywhere in the gap still colours
         the next one. */
      B.load = Math.max(0, B.load - dt * 3.4);
      B.peak = Math.max(B.peak, B.load);
      B.hum -= dt;
      if (B.hum <= 0){
        B.hum += u.hum;
        SFX.play("ult", { w: "vesper-hum", n: B.hn++, load: B.peak });
        B.peak = B.load;
      }

      /* THE TURN, RATE LIMITED, and the rate is the entire counterplay: a
         quarry that out-turns the beam gets round the outside of it, and that
         is a failure the viewer can watch happen. Aimed from the ORIGIN --
         which since Rick's 2026-08-30 note is the ball's own centre, so the
         bearing and the shaft start at the same point and there is nothing to
         keep in sync. */
      const o = this.beamOrigin(f);
      const want = Math.atan2(foe.y - o[1], foe.x - o[0]);
      const d = angDiff(B.ang, want), step = u.turn * dt;
      B.ang += Math.abs(d) <= step ? d : Math.sign(d) * step;

      /* THE PASS. `inBeam` is the ONE definition of "inside", called by the
         simulation here and by `_drawBeam` and by nothing else -- so the
         drawn beam and the tested volume are the same object, which is
         v43's hexagon rule and is `vesper_relic_probe [1]`.

         A SHADE IS NOT A QUARRY. `foe` is the real fighter and `this.shades`
         is never walked here, so a Twinshade copy crossing the beam resolves
         nothing and files nothing. v43 §11 caught the converse of this once,
         one frame in six thousand. */
      const g = (foe.alive && !foe.shade)
                  ? this.inBeam(f, B.ang, foe.x, foe.y, u, B) : null;
      if (!g){ B.in = false; continue; }

      if (!B.in){
        B.in = true; B.tipped = false; B.passes++;
        this.beamHit(f, foe, g, 1, false);
        /* A LETHAL PASS ENDS THE BEAM rather than sweeping a corpse for
           another three seconds. */
        if (!foe.alive || foe.hp <= 0){ f.ultBeam = null; continue; }
      }
      B.best = Math.max(B.best, g.along);
      /* THE BONUS FIRES ON THE PASS'S FURTHEST REACH, not on where it
         happened to be at the last frame -- a latch, set the first instant
         the pass gets out past `tipFrom` and cleared only when the pass ends.
         A pass that ENTERS past the tip line pays both on the same frame,
         which is correct: it reached the far quarter. */
      if (!B.tipped && g.along >= u.tipFrom){
        B.tipped = true; B.tips++;
        this.beamHit(f, foe, g, u.tipMul - 1, true);
        if (!foe.alive || foe.hp <= 0){ f.ultBeam = null; continue; }
      }
    }
  }

  /* WHERE THE BEAM COMES OUT OF, AND IT IS THE BALL. **RICK'S**, 2026-08-30,
     off the first-look clip: "first lets have it center from the ball, not
     the scythe."

     §1 ASKED FOR "POINTS AT THE TIP" AND THIS IS THE SENTENCE HE CHANGED.
     It was built on the tip because the measurement said the mount was nearly
     free -- `beam_probe [2]`, 23.4% on target from the tip against 28.3% from
     the centre, against a turn-rate axis that moves the same number by 43
     points. So the centre is not a compromise: it is the arm that was already
     BETTER by 4.9 points, and the bisection compensates for that.

     AND IT FIXES A PICTURE FAULT THE FILM FOUND. A beam fired from a tip that
     orbits at 3.2 rad/s is laid straight ACROSS its own caster every time the
     blade swings round to the far side -- for a moment the ball reads as the
     thing being shot rather than the thing shooting. Fired from the centre it
     only ever radiates outward, which is also what the reference frame Rick
     supplied shows.

     Two lines, and it is a function anyway: it is the ONE definition of where
     the shaft starts, read by `inBeam` and by `_drawBeam` and by nothing
     else. If it ever moves again, both follow. */
  beamOrigin(f){
    return [f.x, f.y];
  }

  /* HOW LONG THE SHAFT IS RIGHT NOW. **The growth is a mechanic, not a
     flourish** -- this is what `inBeam` measures against, so a half-grown beam
     has a half-length hit volume. A beam drawn growing over a volume that was
     full-length from the first frame is v43's hexagon with a clock on it: the
     drawn boundary and the tested boundary would be two objects again, and the
     disagreement would last exactly as long as the animation.

     OUT ON A CUBIC AND BACK ON A LINEAR. The open is eased so the shaft snaps
     out and settles -- a linear open reads as a bar being slid rather than as
     a light being thrown -- and the close is linear so the retraction is even.
     Both are pure functions of `B.t`, so the post chain drawing the frame four
     times cannot advance them. */
  /* THE PROFILE. How wide the shaft is at `t` along its own length, and it is
     ONE function -- `inBeam` asks it for the hit test and `_drawBeam` asks it
     for every band it fills, so the pencil point and the volume that hits are
     the same object. Rick's "like the tip of a dull pencil": full width to
     `taper`, then a straight cone down to `tipW`, which is a BLUNT end rather
     than a needle.

     Defaults so an ult block with neither field is a plain rectangle -- and
     `=== undefined` rather than `||`, because a `tipW` of 0 is a legitimate
     setting for a sweep to ask for and `|| 0.26` would silently refuse it
     (CLAUDE.md §4.3, and v41's `feed` is the time this project paid for it). */
  beamHalfAt(u, t){
    const tp = u.taper === undefined ? 1 : u.taper;
    if (t <= tp) return u.half;
    const w = u.tipW === undefined ? 1 : u.tipW;
    return u.half * (1 - (1 - w) * ((t - tp) / Math.max(1e-6, 1 - tp)));
  }

  beamLen(B, u){
    const g = 1 - Math.pow(1 - clamp(B.t / Math.max(1e-4, u.open), 0, 1), 3);
    const sh = clamp((B.dur - B.t) / Math.max(1e-4, u.close), 0, 1);
    return u.range * g * sh;
  }

  /* ONE definition of "inside", called by the simulation and by the renderer
     and by nothing else -- v43's hexagon rule, which exists because the
     Harrowing shipped a drawn boundary and a tested boundary that were two
     objects. Returns null for a miss and `{along, x, y}` for a hit, where
     `along` is the fraction of the way down the beam at the closest point.

     `segDist` clamps to the segment, so `along` is in [0,1] and a ball past
     the far end reads 1.0 rather than running off the number line -- which is
     what makes "limited range" a real boundary and not a tapering one. */
  inBeam(f, ang, x, y, u, B){
    const o = this.beamOrigin(f);
    const L = B ? this.beamLen(B, u) : u.range;
    if (L <= 1e-6) return null;
    const ex = o[0] + Math.cos(ang) * L;
    const ey = o[1] + Math.sin(ang) * L;
    const g = segDist(o[0], o[1], ex, ey, x, y);
    /* AGAINST THE CURRENT LENGTH, not against `range`. The far quarter is the
       outer quarter of the shaft that is actually standing, so the lit band
       the viewer can see IS the band that pays -- at every instant of the
       growth and of the retraction, not only when the beam is full. */
    const along = Math.hypot(g.x - o[0], g.y - o[1]) / L;
    /* AND AGAINST THE PROFILE AT THAT POINT, not against `half`. The shaft
       comes to a blunt point, so the volume does: a quarry level with the
       last tenth of the beam has to be closer to the axis than one level with
       its middle. Cheapest possible version of the hexagon rule -- the drawn
       silhouette and the tested one are one function apart. */
    if (g.d > CONFIG.physics.ballR + this.beamHalfAt(u, along)) return null;
    return { along, x: g.x, y: g.y, len: L };
  }

  /* A PASS LANDING, or a pass reaching the far quarter. `mul` is what share
     of `passDmg` this event pays, so the base pass is 1 and the tip bonus is
     `tipMul - 1` and a tip pass totals `passDmg * tipMul` -- which is exactly
     what `tipMul` is being asked to mean by the sweep.

     TWO EVENTS AND NOT ONE BIGGER NUMBER. The bonus lands as its own hit with
     its own float, its own ring and its own voice, because the tip is the
     legible moment of this ultimate and a viewer who cannot tell a tip pass
     from a plain one cannot learn the mechanic.

     THE DIRECTOR HAS TO BE TOLD. Rule 3, seventh relic running: a pass is a
     unit nothing else in the frame knows about, and `cinePlan` would score
     the best moment of this ultimate as empty air. Written to a list the
     simulation never reads -- `engine_ab` is the proof of that, not this
     comment. */
  beamHit(f, foe, g, mul, tip){
    const u = f.w.ult;
    const dmg = Math.round(u.passDmg * mul * this.actMods.dmg
                           * foe.dmgTakenMul());
    if (dmg <= 0) return;
    this.hurt(foe, dmg, f);
    f.dealt += dmg; f.hits++;
    foe.flash = 1;
    if (tip) foe.ringFlash = 1;
    this.float(g.x, g.y - 34, dmg, tip ? "#FFFFFF" : AFFINITIES.vigil.glow,
               (tip ? 34 : 24) + dmg * 0.5);
    this.ring(g.x, g.y, tip ? "#FFFFFF" : f.aff.core, tip ? 6 : 3,
              tip ? 96 : 54, tip ? 0.34 : 0.22, tip ? 5 : 3);
    this.spawnFx(g.x, g.y, f.aff.glow, tip ? 16 : 7, tip ? 240 : 130,
                 tip ? 0.42 : 0.26, tip ? 3.4 : 2.4);
    if (tip){
      this.shake = Math.min(38, this.shake + 8);
      this.hitStop = Math.max(this.hitStop, 0.04);
    }
    if (foe.hp > 0) foe.takeHitstun(dmg);
    /* THE DYNAMO REVS ON THE PAYMENT. Rick's: the sawtooth IS the damage
       connecting, so it is raised HERE -- where the damage actually is -- and
       nowhere else. A tip pays twice on one frame and that is correct: the
       far end is supposed to sound bigger. */
    if (f.ultBeam) f.ultBeam.load = 1;
    SFX.play("ult", { w: tip ? "vesper-tip" : "vesper-pass" });
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: g.x, y: g.y,
                w: f.w.id, foeHpFrac: Math.max(0, foe.hp) / foe.maxHp });
  }

  tickAegis(dt){
    if (!this.a.ultAegis && !this.b.ultAegis) return;'''


TICK_CALL_NEW = r'''    this.tickStasis(dt);
    this.tickSentinel(dt);'''


# ------------------------------------------------------------- the drink --

DRINK_WARD_NEW = r'''  /* DRINK. The ward's FOURTH ending, and the second one the relic chooses.

     THIS IS NOT `spendWard` AND IT IS NOT `shatter`, and keeping the three
     apart is the whole of it. `spendWard` takes the entire pool in one call
     and hands the number back, which is what a wall made of the plate wants;
     `shatter` bursts the pool at the holder and flings the attacker, which is
     what BREAKING it means. A drink is neither: it takes a sip, it is
     repeated every frame, and NOTHING is burst and nobody is flung -- because
     nobody broke the plate, the relic drank it.

     scythe_survey §4.2 is the standing warning here: a shatter and an expiry
     already write the same three fields, so nothing outside the engine can
     tell a plate that was broken from one that lapsed. A drink written as
     either of them would be a third indistinguishable ending.

     `shieldMax` IS LEFT ALONE WHILE THE POOL FALLS, so the gauge drains
     rather than shrinking -- the plate visibly being spent is the picture §1
     is buying with its last sentence. Both are zeroed only when it runs
     dry. */
  drinkWard(f, want){
    if (want <= 0 || f.shield <= 0) return 0;
    const got = Math.min(f.shield, want);
    f.shield -= got;
    if (f.shield <= 1e-9){
      f.shield = 0; f.shieldMax = 0;
      delete f.status.ward;
    }
    return got;
  }

  spendWard(f){'''


# ------------------------------------------------- and it cannot outlive it --
# `decay()` ALREADY CARRIES THIS RULE THREE TIMES and says why each time: the
# shades, the spike storm and the Converse are all cleared on `over`, because
# `step()` returns from the `over` branch ABOVE their ticks and a set-piece
# left running sits frozen through the entire verdict beat. Sentinel is
# exactly that shape -- a shaft drawn from LIVE state, across the hall, for as
# long as `ultBeam` exists -- so it is a fourth entry in the same block rather
# than a new rule.
#
# THE TICK'S OWN GUARDS CANNOT REACH THIS. They end the beam when the quarry
# dies, and they do reach the case where a killFlight defers `checkEnd` -- but
# a kill with no flight sets `over` in the same step, one function below
# `tickSentinel`, and the tick never runs again.
DECAY_NEW = r"""    if (this.over && (this.a.ultTrace || this.b.ultTrace)){
      this.a.ultTrace = null; this.b.ultTrace = null;
    }
    /* And the Sentinel cannot either, for the third time verbatim: `step()`
       returns from the `over` branch before `tickSentinel` is reached, so a
       beam left standing would be a pink shaft laid across the hall, frozen,
       for the whole 2.4s the verdict panel is up -- over the most legible
       moment in the match. `vesper_relic_probe [7]` counts it.

       THE TICK'S OWN GUARDS DO NOT REACH THIS ONE. They end the window when
       the quarry dies and they cover the case where a killFlight defers
       `checkEnd`; a kill with no flight sets `over` in the same step, one
       function below `tickSentinel`, and the tick never runs again. */
    if (this.over && (this.a.ultBeam || this.b.ultBeam)){
      this.a.ultBeam = null; this.b.ultBeam = null;
    }
    this.decayImpactOnly(dt);"""

# ------------------------------------------------------------------- art --

DRAW_BEAM_NEW = r'''  /* THE WATCH, AND THE LIGHT IT KEEPS. Returns on its first line for every
     relic that is not casting.

     BUILT AGAINST A REFERENCE FRAME RICK SUPPLIED, 2026-08-30, with the bar
     set as "this quality or better to pass". What that frame actually
     contains, read off it rather than paraphrased, and every one of these is
     a thing the first cut did not have:

       A MUZZLE COLLAR   a bright flared ring AT THE SOURCE, wider than the
                         shaft, with the shaft emerging from inside it. The
                         first cut had a small white dot.
       BANDED STRIATION  not one gradient. A white-hot core with discrete
                         thin bands above and below it, each its own colour
                         and alpha, with dark between them. That banding is
                         what makes it read as ENERGY rather than as a
                         painted bar.
       A SPLASH AT THE END  the far end is not a cap, it is a spray of jagged
                         rays thrown outward. The beam is HITTING something.
       ORBIT MARKS       dashed arcs around the muzzle, turning.

     DRAWN FROM THE LIVE FIGHTER AND ITS LIVE `ultBeam`, not from the frozen
     cast record -- the ball moves and the bearing turns, and a set-piece
     drawn from a copy describes a fight that has moved on. Aegis's rule and
     `_retraceField`'s, and the reason both say so.

     AND THE GEOMETRY IS `inBeam`'s, NOT A SECOND COPY OF IT. The shaft is
     drawn from `beamOrigin` along `ang` for `beamLen` -- the SAME growing
     length the hit test measures against -- at `half` either side. The ball's
     own radius is what the test adds on top, so a ball that looks like it is
     grazing the edge is a ball that is being hit. v43's hexagon shipped a
     drawn boundary and a tested boundary that were two objects; a growth
     animation over a full-length volume would be the same fault with a clock
     on it. */
  _drawBeam(m, f){
    const B = f.ultBeam;
    if (!B) return;
    const c = this.ctx, u = f.w.ult, P = f.aff, R = CONFIG.physics.ballR;
    /* `m.beamOrigin`, NOT `this.beamOrigin`. THE SEAM IS REAL AND THIS IS
       WHERE IT BITES: these are MATCH methods and this is the RENDERER, and
       the first cut wrote `this.` -- which threw on the first frame a beam was
       drawn and passed every headless check in the repo, including this
       relic's own probe, because the probe was regexing the SOURCE for the
       call and a string does not resolve a reference. Caught by filming it,
       which is build brief §0.3 and CLAUDE.md §4.0 arriving on schedule.
       `vesper_relic_probe [1]` now CALLS this function against a live standing
       beam rather than reading it. */
    const o = m.beamOrigin(f);

    if (B.phase === "wind"){
      /* THE CHARGE-UP. §1 asked for "a loud glowing animation", and the loud
         half is the voice -- this is the glowing half, and it is a TELEGRAPH
         before it is a flourish: the wind-up is the only window in which this
         ultimate can be taken away, so the four relics that can take it need
         to be able to see it coming.

         IT GATHERS ONTO THE BALL rather than radiating off it, which is the
         one grammar that says "about to fire" rather than "just fired": a
         ring closing in, a core swelling inside the shell, and the collar
         forming early so the muzzle the beam will come out of is already
         there when it does.

         DETERMINISTIC OFF `m.t`, the way SHAPES._t is, because the post chain
         draws every frame four times and an accumulated phase would advance
         four times as fast in the app and not at all in the capture. */
      const k = clamp(B.t / Math.max(0.01, u.wind), 0, 1);
      c.save();
      c.globalCompositeOperation = "lighter";

      /* the ring closing in */
      c.globalAlpha = 0.18 + 0.55 * k;
      c.strokeStyle = P.glow; c.lineWidth = 1 + 4 * k;
      c.shadowColor = P.core; c.shadowBlur = 10 + 26 * k;
      c.beginPath(); c.arc(o[0], o[1], 100 * (1 - k) + R * 0.9, 0, TAU);
      c.stroke();
      c.shadowBlur = 0;

      /* two dashed orbit marks, turning opposite ways -- the reference frame
         carries these at the muzzle and they are what stops a round glow
         reading as a bloom */
      c.setLineDash([7, 9]);
      for (let i = 0; i < 2; i++){
        const dir = i ? -1 : 1;
        c.globalAlpha = 0.30 * k;
        c.lineWidth = 2;
        c.strokeStyle = i ? "#FFFFFF" : P.core;
        c.beginPath();
        c.arc(o[0], o[1], R * (1.5 + i * 0.28),
              m.t * 2.2 * dir, m.t * 2.2 * dir + 4.2);
        c.stroke();
      }
      c.setLineDash([]);

      /* the core swelling inside the shell */
      c.globalAlpha = 0.30 + 0.65 * k;
      c.fillStyle = P.core;
      c.beginPath(); c.arc(o[0], o[1], 4 + R * 0.7 * k * k, 0, TAU); c.fill();
      c.globalAlpha = 0.60 * k * k;
      c.fillStyle = "#FFFFFF";
      c.beginPath(); c.arc(o[0], o[1], 2 + R * 0.34 * k * k, 0, TAU); c.fill();

      /* THE COLLAR, FORMING EARLY. The muzzle exists before the shaft does,
         so the beam comes OUT of something rather than appearing beside it.
         Last third of the wind-up only. */
      if (k > 0.62){
        const ck = clamp((k - 0.62) / 0.38, 0, 1);
        /* SAVE/RESTORE AND NOT setTransform. `_drawBeam` is called with the
           arena's own transform already on the context; resetting it by hand
           would put every later relic's art at the top-left of the canvas.
           The Winnowing's own under-layer learned this rule; this is it
           honoured rather than rediscovered. */
        c.save();
        c.translate(o[0], o[1]); c.rotate(B.ang);
        c.translate(R * 0.72, 0);
        this._beamCollar(c, u.half, ck * 0.8, P);
        c.restore();
      }
      c.restore();
      return;
    }

    /* THE SHAFT. Its length is `beamLen`, which is the hit volume's own
       length -- so the growth, the full stand and the retraction are one
       number read by both. */
    const L = m.beamLen(B, u);
    if (L <= 2) return;
    const H = u.half;
    const grow = clamp(L / u.range, 0, 1);

    c.save();
    c.translate(o[0], o[1]);
    c.rotate(B.ang);
    c.globalCompositeOperation = "lighter";

    /* THE SILHOUETTE, AND EVERY LAYER FOLLOWS IT. `beamHalfAt` is the same
       function `inBeam` tests against, sampled along the shaft -- so the
       pencil point in the picture and the pencil point in the hit volume are
       one object, not two that agree. Sampled at 20 steps because the profile
       is piecewise linear with one corner: fewer and the corner lands between
       samples on some frames, more buys nothing.

       `strip` fills a band between two fractions of the profile, mirrored
       above and below the axis; `solid` fills a shape that spans the axis. */
    const SEG = 20;
    const pr = (t) => m.beamHalfAt(u, t) / H;
    const strip = (yOut, yIn, col, a2) => {
      c.globalAlpha = a2;
      c.fillStyle = col;
      for (const sg of [-1, 1]){
        c.beginPath();
        for (let i = 0; i <= SEG; i++){
          const t = i / SEG;
          c.lineTo(t * L, sg * H * yOut * pr(t));
        }
        for (let i = SEG; i >= 0; i--){
          const t = i / SEG;
          c.lineTo(t * L, sg * H * yIn * pr(t));
        }
        c.closePath(); c.fill();
      }
    };
    const solid = (yOut, col, a2) => {
      c.globalAlpha = a2;
      c.fillStyle = col;
      c.beginPath();
      for (let i = 0; i <= SEG; i++){
        const t = i / SEG;
        c.lineTo(t * L, -H * yOut * pr(t));
      }
      for (let i = SEG; i >= 0; i--){
        const t = i / SEG;
        c.lineTo(t * L, H * yOut * pr(t));
      }
      c.closePath(); c.fill();
    };

    /* ---- THE HALO, first and widest. It reaches PAST `half`, and that is
       honest rather than generous: the tested volume is `ballR + half at this
       point along the shaft`, because `inBeam` compares against the quarry's
       own radius -- so a shaft drawn at exactly the profile UNDER-draws the
       thing that hits by 34 units, and a ball that looks like it is clearing
       the edge is a ball that is being hit. The hard banding below still
       marks the profile exactly; this is the soft part of a volume that
       really is softer at its edge. */
    for (const [hy, a2] of [[1.85, 0.10], [1.45, 0.14], [1.15, 0.20]])
      solid(hy, P.core, a2 * (0.5 + 0.5 * grow));

    /* ---- THE BANDS. Not a gradient: the reference frame's shaft is a
       white-hot core carrying DISCRETE bright bands above and below it with
       dark between them, and that banding is what makes it read as ENERGY
       rather than as a painted bar. Drawn outermost first so the core lands
       on top of everything.

       A first cut had five bands crowded into the outer third and they fused
       into one pink smear at render scale -- the arena is 520 wide and ships
       at 540, so a band under about 1.5 device pixels is not a band. */
    strip(1.00, 0.80, P.core,    0.60 * (0.55 + 0.45 * grow));
    strip(0.74, 0.61, P.glow,    0.72 * (0.55 + 0.45 * grow));
    strip(0.55, 0.45, "#FFD9F0", 0.80 * (0.55 + 0.45 * grow));

    /* THE CORE, and it is the MASS of the object rather than a centre line.
       The reference frame is most of the way white across the middle of the
       shaft; a thin white line with pink either side is a laser pointer, not
       a beam. Two passes so the core has a hot centre of its own -- and both
       taper, so the white comes to the point with everything else. */
    solid(0.46, "#FFE9F7", 0.72 * (0.6 + 0.4 * grow));
    solid(0.30, "#FFFFFF", 0.98);

    /* ---- THE FAR QUARTER. Where `tipFrom` actually is, read off the same
       field the hit test reads and against the same CURRENT length, so the
       lit band and the paying band cannot drift apart. A brighter wash and a
       hard divider, because the tip bonus is the mechanic and a viewer who
       cannot see where the far quarter starts cannot learn why one pass hurt
       more than the last one. The wash follows the profile too, so it is the
       point that is lit rather than a rectangle over it. */
    const tf = u.tipFrom;
    c.globalAlpha = 0.26;
    c.fillStyle = P.glow;
    c.beginPath();
    for (let i = 0; i <= SEG; i++){
      const t = tf + (1 - tf) * (i / SEG);
      c.lineTo(t * L, -H * pr(t));
    }
    for (let i = SEG; i >= 0; i--){
      const t = tf + (1 - tf) * (i / SEG);
      c.lineTo(t * L, H * pr(t));
    }
    c.closePath(); c.fill();
    c.globalAlpha = 0.55;
    c.strokeStyle = "#FFFFFF"; c.lineWidth = 1.5;
    c.beginPath();
    c.moveTo(tf * L, -H * pr(tf) * 0.92);
    c.lineTo(tf * L,  H * pr(tf) * 0.92);
    c.stroke();

    /* ---- THE POINT. **RICK'S**, 2026-08-30: "it needs to end in a point.
       like the tip of a dull pencil." The v2 build ended in a 22-ray splash
       thrown across 2.3 radians -- which read as an impact and is the exact
       opposite of a point, so it is GONE rather than shrunk. What is left is
       the blunt end the taper already makes, with a hot nub on it so the
       point reads as lit rather than as a shaft that simply stopped, and a
       short forward-only flare along the axis so it still has somewhere to
       go. Nothing here is wider than the profile's own end. */
    const tw = H * pr(1);
    c.globalAlpha = 0.55 * grow;
    c.fillStyle = P.glow;
    c.beginPath(); c.ellipse(L, 0, tw * 0.85, tw * 1.05, 0, 0, TAU); c.fill();
    c.globalAlpha = 0.95 * grow;
    c.fillStyle = "#FFFFFF";
    c.beginPath(); c.ellipse(L, 0, tw * 0.50, tw * 0.62, 0, 0, TAU); c.fill();
    /* the forward flare: four short glints ALONG the bearing, inside a
       0.30-radian cone, so the point has a direction and not a spray */
    for (let i = 0; i < 4; i++){
      const a2 = (shellHash(7717, i) - 0.5) * 0.60;
      const len = tw * (1.5 + shellHash(7727, i) * 2.2)
                * (0.75 + 0.25 * Math.sin(m.t * 8.0 + i * 2.1));
      c.globalAlpha = (0.24 + 0.30 * shellHash(7733, i)) * grow;
      c.strokeStyle = i % 2 ? "#FFFFFF" : P.core;
      c.lineWidth = 1 + 1.6 * shellHash(7741, i);
      c.beginPath();
      c.moveTo(L - tw * 0.3, 0);
      c.lineTo(L + Math.cos(a2) * len, Math.sin(a2) * len);
      c.stroke();
    }

    /* ---- THE MUZZLE COLLAR, last, so it sits over the shaft it emits, and
       translated out to the SHELL EDGE: at the origin it is behind the ball
       and the viewer never sees it. On the rim it reads as the port the light
       is coming out of, which is where the reference frame puts it. */
    c.translate(R * 0.72, 0);
    this._beamCollar(c, H, 1, P);

    c.restore();

    /* THE PLATE BEING DRUNK, on the caster and outside the rotated frame: a
       thin ring that pulses while there is still a pool to burn, so the
       viewer can see the armour going into the light rather than being told
       about it. */
    if (f.shield > 0){
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = 0.20 * (0.6 + 0.4 * Math.sin(m.t * 16));
      c.strokeStyle = AFFINITIES.vigil.glow; c.lineWidth = 2;
      c.beginPath(); c.arc(f.x, f.y, R + 9, 0, TAU); c.stroke();
      c.restore();
    }
  }

  /* THE COLLAR, in the beam's own local frame: the flared ring the shaft
     comes out of. Its own function because the wind-up draws it forming and
     the standing beam draws it whole, and two copies of a shape is how the
     two stop matching.

     A RING AND NOT A DISC. A filled blob at the origin sits ON TOP of the
     ball and reads as damage to the caster; a ring with the hole cut in the
     path leaves the shell an object -- which is §4.1b's fix for Daybreak's
     corona, one relic-family over, and the reason a radial gradient was not
     used here at all. */
  _beamCollar(c, H, k, P){
    const rx = H * 0.42 * k, ry = H * 1.55 * k;
    c.globalAlpha = 0.55 * k;
    c.strokeStyle = P.core; c.lineWidth = H * 0.30 * k;
    c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.stroke();
    c.globalAlpha = 0.85 * k;
    c.strokeStyle = "#FFE6F7"; c.lineWidth = H * 0.13 * k;
    c.beginPath(); c.ellipse(0, 0, rx * 0.86, ry * 0.84, 0, 0, TAU); c.stroke();
    /* the flare, thrown back along the shaft's own axis */
    c.globalAlpha = 0.30 * k;
    c.fillStyle = P.glow;
    c.beginPath();
    c.moveTo(-H * 0.55 * k, 0);
    c.lineTo(H * 0.30 * k, -ry * 1.02);
    c.lineTo(H * 0.30 * k, ry * 1.02);
    c.closePath(); c.fill();
  }

  _drawField(m, f){'''


DRAW_CALL_NEW = r'''    this._drawField(m, f);
    this._drawBeam(m, f);'''


DRAW_UNDER_NEW = r'''    /* ---- THE SENTINEL, under -------------------------------------------
       Deliberately SMALL, and for the same reason the Winnowing's and the
       Thicket's are: everything a viewer needs in order to read this ultimate
       is already drawn from live state by `_drawBeam` -- the shaft, the far
       quarter lit, the plate draining on the shell. A set-piece competing
       with that would be light drawn on top of light, and this is the school
       whose ultimates have already blown the bloom out twice (§4.1b).

       WHAT IS HERE IS THE ONE THING THE BEAM CANNOT SAY ABOUT ITSELF: THAT
       THE ROOM IS DARKER FOR IT. A slow wash in the school's pink, centred on
       the caster and reaching a third past the beam's own range, on while the
       window stands -- so the shaft has something to be the brightest thing
       in. Drawn UNDER everything, never above a seventh, and read off the
       LIVE `ultBeam` rather than off `u.t`, because this window's length is
       a number the ward decides at runtime. */
    if (u.w === "%ID%"){
      /* `u` HERE IS THE `ultFx` RECORD, NOT THE WEAPON'S ULT. It carries
         {w, kind, src, tgt, x, y, tx, ty, hit, radius, aff, t, life} and
         nothing else -- so `u.range` is `undefined`, `undefined * 1.35` is
         NaN, and `createRadialGradient` throws "The provided double value is
         non-finite" on the first frame of the first cast. The reach comes off
         the LIVE weapon.

         SECOND PICTURE FAULT IN THIS BUILD, same shape as the first: both
         were invisible to 27 probe checks, a 280-match engine A/B and
         post_identity, and both died on a rendered frame. `_drawBeam` reached
         for a Match method from the Renderer; this reached for a weapon field
         on a set-piece record. `vesper_relic_probe [1]` now CALLS
         `drawUltUnder` and `drawUltOver` as well. */
      const B = src && src.ultBeam;
      if (B && B.phase === "beam"){
        const rng = src.w.ult.range;
        const g2 = c.createRadialGradient(src.x, src.y, 40,
                                          src.x, src.y, rng * 1.35);
        g2.addColorStop(0, "rgba(240,107,184,0.13)");
        g2.addColorStop(1, "rgba(240,107,184,0)");
        c.globalAlpha = clamp(Math.min(B.t / 0.35, (B.dur - B.t) / 0.35), 0, 1);
        c.fillStyle = g2;
        c.fillRect(0, 0, A.w, A.h);
        c.globalAlpha = 1;
      }
    }

    if (u.w === "vinesower"){'''


# ----------------------------------------------------------------- sound --

SFX_NEW = r'''        } else if (w === "%ID%"){                   // the cast IS the wind-up
          /* `fireUlt` plays `SFX.play("ult", { w: f.w.id })` for every relic
             in the game, so the bare id has to BE a voice. On this relic the
             cast IS the wind-up, so it routes to the wind-up's sound rather
             than inventing a fifth one that would play over the top of it.
             `vesper_relic_probe [9]` renders the BARE ID as well as the four
             parts, because a routing clause that reaches nothing is exactly
             the silent-ultimate shape v42 shipped. */
          this.play("ult", { w: "%ID%-wind" });
        } else if (w === "%ID%-wind"){              // the watch being lit
          /* THE CHARGE-UP. §1 asked for a LOUD one, and the wind-up is also
             the only window in which this ultimate can be taken away -- so
             the sound is a telegraph before it is a flourish, and it has to
             be recognisable across a hall that is already making noise.

             A RISE, which almost nothing in this game is. Twenty-six voices
             and the two that rise are the draws (Reprisal, the ballista) --
             both of which are also "something is about to leave", which is
             exactly the sentence wanted here. It is not a blast run backwards
             and it is not a bell.

             WRITTEN INSIDE THE ENVELOPE OF TWO KNOWN BUGS RATHER THAN FIXING
             THEM. `_tone` ends on an exponential ramp over its whole length,
             so a rise has to be a rise in FREQUENCY across a decaying voice
             and is RE-STRUCK rather than held; `_burst` does not loop its
             0.6s noise buffer, so every burst here is under 0.6s. Both are
             live on twenty-six shipped voices and both are chain-wide and
             Rick's, not a thing a relic build gets to slip in.
             `vesper_relic_probe [9]` RENDERS this in an OfflineAudioContext
             and measures it rather than trusting the paragraph -- v42 shipped
             a SILENT ultimate through every green check in this repo. */
          this._tone (t,        { freq: 180, to: 620,  gain: 0.16, dur: 0.42, type:"triangle" });
          this._tone (t + 0.16, { freq: 300, to: 900,  gain: 0.14, dur: 0.36, type:"sine" });
          this._tone (t + 0.34, { freq: 520, to: 1240, gain: 0.13, dur: 0.30, type:"triangle" });
          this._burst(t + 0.30, { freq: 1800, q: 0.9, gain: 0.09, dur: 0.34, type:"bandpass" });
        } else if (w === "%ID%-open"){              // the beam standing up
          /* THE RELEASE, and it is a THUMP with a ring on top rather than a
             crack: the light does not go off, it comes ON and then stays for
             four seconds. The long triangle that does NOT rise is Aegis's
             trick one relic over -- a rising tail would promise something
             about to happen, and what happens next is that this stands. */
          this._burst(t, { freq: 900, q: 0.8, gain: 0.20, dur: 0.09, type:"bandpass" });
          this._tone (t, { freq: 210, to: 96, gain: 0.22, dur: 0.30, type:"sine" });
          this._tone (t + 0.03, { freq: 784, to: 784, gain: 0.10, dur: 0.70, type:"triangle" });
          this._tone (t + 0.05, { freq: 1176, to: 1176, gain: 0.05, dur: 0.62, type:"triangle" });
        } else if (w === "%ID%-hum"){               // the beam, standing
          /* DYNAMO. **RICK'S**, from a spread of four rendered as full
             3.6-second runs with passes and a tip over the top --
             `sentinel_hum_lab.py`, and he took the first one on the first
             pass. A machine under load: two sawtooths a fifth apart with a
             thin octave over them, and the pair DETUNES across the run so
             forty strikes are forty different sounds rather than one sample
             forty times.

             IT SITS AT 58 Hz ON PURPOSE. `vesper-pass` lives at 470-1500 and
             `vesper-tip` at 880-2600, and telling those two apart is the only
             thing a viewer has to learn from this ultimate -- a hum in their
             band would mask the mechanic. This one goes UNDER them, which is
             also why the spread was auditioned with a tip playing over it
             rather than alone.

             THE 260 Hz THUMP EVERY THIRD STRIKE is what stops a continuous
             floor reading as a synth pad: it gives the run a slower pulse
             that is not a multiple of the cadence. */
          const hn = p.n || 0, L = Math.max(0, Math.min(1, p.load || 0));
          const hw = 1 + Math.sin(hn * 0.7) * 0.012;

          /* THE BED, and it plays whether the beam is touching anything or
             not. Rick: "a static hum and THEN the sawtooth of dynamo is the
             damage connecting" -- so the bed is what standing sounds like and
             it is deliberately characterless. A sine and a soft low band,
             nothing that rasps: everything with an edge on it is reserved for
             the layer that means CONTACT, or the contrast is gone. */
          this._tone (t, { freq: 52 * hw, to: 49 * hw, gain: 0.052, dur: 0.40, type:"sine" });
          this._burst(t, { freq: 190, q: 0.9, gain: 0.020, dur: 0.36, type:"lowpass" });

          /* THE DYNAMO, ON TOP, IN PROPORTION TO THE LOAD. This is the cue --
             the sawtooth pair only exists while the beam is on the quarry, so
             a viewer who has heard it once knows what it means without being
             told. It also REVS: the fundamental climbs a fifth of an octave
             under load, so the machine is audibly working harder rather than
             just louder, and loudness alone would be lost the moment anything
             else in the mix is busy.

             THE FLOOR IS 0.03 AND NOT 0. `>` a threshold rather than scaling
             from zero, because a sawtooth at gain 0.001 is not a quiet
             sawtooth, it is an artefact -- and the bed is supposed to be
             clean when nothing is connecting. */
          if (L > 0.03){
            const rev = 1 + 0.14 * L;
            this._tone (t, { freq: 58 * hw * rev,  to: 54 * hw * rev,  gain: 0.125 * L, dur: 0.42, type:"sawtooth" });
            this._tone (t, { freq: 87 * hw * rev,  to: 82 * hw * rev,  gain: 0.060 * L, dur: 0.38, type:"sawtooth" });
            this._tone (t, { freq: 174 * hw * rev, to: 166 * hw * rev, gain: 0.026 * L, dur: 0.30, type:"triangle" });
            /* THE 260 Hz THUMP EVERY THIRD STRIKE is what stops a continuous
               floor reading as a synth pad: it gives the run a slower pulse
               that is not a multiple of the cadence. Under load only, because
               it is part of the machine and not part of the room. */
            if (hn % 3 === 0)
              this._burst(t, { freq: 260, q: 0.7, gain: 0.034 * L, dur: 0.30, type:"lowpass" });
          }
        } else if (w === "%ID%-pass"){              // the room walks into it
          /* A PASS. Fires about three and a half times a window, so it is
             quiet by design and short by design -- and it is deliberately
             SOFTER than the tip, because the one thing a viewer has to learn
             from this ultimate is which of the two just happened. */
          this._burst(t, { freq: 1500, q: 1.1, gain: 0.09, dur: 0.07, type:"bandpass" });
          this._tone (t, { freq: 470, to: 330, gain: 0.08, dur: 0.10, type:"triangle" });
        } else if (w === "%ID%-tip"){               // the far end connecting
          /* THE FAR END. §1's bonus, and the legible moment of the whole
             ultimate -- so it is the one voice on this relic that is allowed
             to be bright. A hard transient and a RISING chime over the pass
             sound's own band, so it reads as the same event with something
             extra on it rather than as a different event. */
          this._burst(t, { freq: 2600, q: 1.6, gain: 0.20, dur: 0.05, type:"bandpass" });
          this._tone (t, { freq: 880, to: 1480, gain: 0.16, dur: 0.16, type:"triangle" });
          this._tone (t + 0.02, { freq: 1320, to: 1320, gain: 0.08, dur: 0.26, type:"sine" });
        } else if (w === "bulwarden"){              // a hall door closing'''

ULTFX_LIFE_NEW = r'''              thornshear: 9.4,
              /* THE SENTINEL is set from `ult.wind + ult.durCap` at the cast
                 site, the way Aegis, the Thicket, the ballista, the Stasis
                 Field and the Winnowing are. This entry is the fallback if
                 that is ever missed. */
              vesper: 19.7,'''


# ---------------------------------------------------------- the particles --
# THE TWENTY-SEVENTH SPEC. `src/render/fx.js` carries twenty-six and every one
# of the shipped ultimates has a field; a relic with no entry is not an error
# (`ULTFX.sync` returns on `!spec`) which is exactly why it would ship missing.
# Written into the INLINED copy here and into `src/render/fx.js` by hand in the
# same commit, so a rebuild through `fx_build.py` cannot lose it.
FX_SPEC_NEW = r'''    /* THE SENTINEL. A SWIRL and not a beam, and the choice is the mechanic:
       `mode: 'beam'` spawns along the cast-time axis and FREEZES there, which
       is right for the seven instantaneous shafts that carry it and wrong for
       the one beam in the game that turns -- the motes would sit on a bearing
       the beam left two seconds ago. A swirl holds them at a radius instead,
       tangential rather than launched, which is what a turning thing looks
       like and is the honest picture of the design's §6.1: the light is not
       thrown, the room is being swept. Slow, long-lived and sparse, because
       the shaft is already the brightest object in the frame and this must
       not compete with it (§4.1b, twice, on this school). */
    vesper: { mode: 'swirl', n: 1050, sp: [40, 150], grav: -14, drag: 0.7,
              life: [0.90, 2.10], heavy: 0.0, size: [0.6, 1.9],
              spawn: 0.85, up: 0 },
    /* ---- IMPLOSION: a burst run backwards ---------------------------- */'''

FX_SPEC_OLD = r'''    /* ---- IMPLOSION: a burst run backwards ---------------------------- */'''


EDITS = [
    ("the relic",
     '''    blurb:"A hedge-blade that lets go of its edges. What it throws comes back off the wall bigger than it left." },

];''',
     RELIC_NEW),

    ("fighter state",
     '''    this.ultWinnow = null;''',
     FIGHTER_STATE_NEW),

    ("the cast",
     '''    if (u.kind === "ballista"){''',
     FIRE_ULT_NEW),

    ("losing the wind-up",
     '''    if (!f.ultSpin) return;''',
     BREAK_SPIN_NEW),

    ("the window",
     '''  tickAegis(dt){
    if (!this.a.ultAegis && !this.b.ultAegis) return;''',
     TICK_SENTINEL_NEW),

    ("the tick call",
     '''    this.tickStasis(dt);''',
     TICK_CALL_NEW),

    ("the drink",
     '''  spendWard(f){''',
     DRINK_WARD_NEW),

    ("the beam cannot outlive the match",
     '''    if (this.over && (this.a.ultTrace || this.b.ultTrace)){
      this.a.ultTrace = null; this.b.ultTrace = null;
    }
    this.decayImpactOnly(dt);''',
     DECAY_NEW),

    ("the beam, drawn",
     '''  _drawField(m, f){''',
     DRAW_BEAM_NEW),

    ("the draw call",
     '''    this._drawField(m, f);''',
     DRAW_CALL_NEW),

    ("the set-piece",
     '''    if (u.w === "vinesower"){''',
     DRAW_UNDER_NEW),

    ("the ult voice",
     '''        } else if (w === "bulwarden"){              // a hall door closing''',
     SFX_NEW),

    ("the fx clock",
     '''              thornshear: 9.4,''',
     ULTFX_LIFE_NEW),

    ("the particle field", FX_SPEC_OLD, FX_SPEC_NEW),
]


def one(src: str, old: str, new: str, label: str) -> str:
    # A BUILDER THAT WRITES BROKEN JAVASCRIPT SHOULD SAY SO, NOT HAND IT TO A
    # PROBE THAT TIMES OUT AFTER TWENTY SECONDS WITH A PLAYWRIGHT STACK TRACE.
    # v43 shipped an unbalanced `*/` once -- a comment paragraph appended after
    # the block it belonged inside -- and the only signal was the page failing
    # to load. These blocks are almost all prose; counting the delimiters is
    # the cheapest thing that catches it.
    if new.count("/*") != new.count("*/"):
        raise SystemExit(
            f"BLOCK {label}: {new.count('/*')} '/*' against "
            f"{new.count('*/')} '*/'. A comment in this insert is not closed "
            f"the way it is opened, and the page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--out", default="../02-chain/sc-vesper.html")
    ap.add_argument("--id", default=RELIC_ID)
    ap.add_argument("--name", default=RELIC_NAME)
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=TUNED_VS)
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=v)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nVIGIL SCYTHE BUILD -- the Sentinel")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    # THE CHAIN IS LINEAR AND THIS ONE BUILDS OFF THORNSHEAR, NOT OFF THE
    # IGNITION TIP. The build brief's §0 item 1 is not negotiable and this is
    # the line that enforces it.
    if '"winnow"' not in s0:
        raise SystemExit("this source has no winnow -- Thornshear lands FIRST "
                         "(v48 brief §0). Build off sc-thornshear.html.")
    if '"sentinel"' in s0:
        raise SystemExit("this source already has a sentinel -- already built")

    # BUILDERS ECHO WHAT THEY ARE ABOUT TO WRITE, AND SOMEBODY READS IT.
    # v42 rule 6: a `dmgMul` edit was silently eaten by a stale anchor and a
    # 4600-fight bisection ran at the wrong value.
    print(f"  id  {A.id} / {A.name} / {A.ult}     dmg {A.dmg:g}")
    print("  ult " + "  ".join(f"{k} {getattr(A, k):g}" for k in ULT))

    # §1'S OWN FLOOR, ARITHMETIC, BEFORE ANY FIGHT RUNS. "thick, at least half
    # the thickness of an artifact" is a NUMBER: an artifact is 2 * ballR
    # across, so the beam must be at least ballR wide and `half` at least
    # ballR / 2. A sweep is allowed to look up from there and is not allowed
    # to walk under the sentence.
    BALL_R = 34.0
    if A.half < BALL_R / 2:
        raise SystemExit(
            f"THICKNESS: half {A.half:g} makes a beam {A.half * 2:g} wide "
            f"against a {BALL_R * 2:g}-wide artifact. §1 asks for at least "
            f"half of one, so `half` may not go below {BALL_R / 2:g}.")
    # AND THE LOOP HAS TO BE ABLE TO CLOSE. A drink rate at or under the ward's
    # measured income (about 2.0 points a second on this type, beam_probe [4])
    # is a beam fed faster than it burns, which runs to `durCap` every cast and
    # makes `dur` -- the sweep's other axis -- unreadable. Said here rather
    # than left for a 960-fight sweep to discover.
    INCOME = 2.0
    if A.drink <= INCOME:
        print(f"  WARN drink {A.drink:g}/s is at or under the measured ward "
              f"income of {INCOME:g}/s -- the beam is fed faster than it "
              f"burns and will run to durCap {A.durcap:g}s every cast")
    print(f"  win {A.wind:g}s wind-up, then {A.dur:g}s base and up to "
          f"{A.durcap:g}s with the plate  "
          f"({(A.durcap - A.dur) / A.durper:.0f} points of ward to reach "
          f"the cap, against a 90 cap and a measured mean pool of 12)")

    subs = {"%ID%": A.id, "%NAME%": A.name, "%ULT%": A.ult,
            "%TIP%": A.tip, "%DMG%": f"{A.dmg:g}"}
    for k in ULT:
        subs["%" + k.upper() + "%"] = f"{getattr(A, k):g}"

    for label, old, new in EDITS:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # THE TIP HAS A HARD LIMIT AND verify.py IS WHERE IT IS ENFORCED -- which
    # is 12000 fights too late to find out. v43 hit 73 characters on its first
    # cut of the same line.
    if len(A.tip) > 72:
        raise SystemExit(f"ULT TIP is {len(A.tip)} characters against "
                         f"verify.py's limit of 72:\n  {A.tip}")
    if s.count(f'tip:"{A.tip}"') != 1:
        raise SystemExit("the ult tip did not land exactly once")
    print(f"  tip {len(A.tip)}/72  {A.tip}")

    # THE INLINED MODULE AND THE FILE ON DISK MUST STAY THE SAME OBJECT.
    # `fx_build.py` inlines `src/render/fx.js` verbatim and STAMPS ITS SHA256
    # into the page twice, and this builder writes a twenty-seventh spec into
    # the inlined copy. Written only there, the next rebuild through fx_build
    # would silently drop the field -- an ultimate with no particles among
    # twenty-six that have them, which is a picture fault with no number
    # attached to it. So the same spec goes into `src/render/fx.js` in the same
    # commit, and this block REFUSES TO WRITE unless the two are byte
    # identical, then re-stamps the sha.
    fx_js = HERE.parent / "src" / "render" / "fx.js"
    mod = fx_js.read_text(encoding="utf-8")
    new_sha = hashlib.sha256(mod.encode("utf-8")).hexdigest()
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    old_sha = head.group(1)
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    if not tm:
        raise SystemExit("no ULT FIELDS glue after the inlined fx.js")
    tail = tm.start()
    inlined = s[head.end():tail].rstrip("\n")
    if inlined != mod.rstrip():
        raise SystemExit(
            "src/render/fx.js and the copy inlined in this build have "
            "DIVERGED.\n  The spec this builder writes into the page must "
            "also be in the file\n  fx_build.py inlines, or the next rebuild "
            "drops it.\n  inlined "
            f"{len(inlined)} bytes against {len(mod.rstrip())} on disk.")
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
    print(f"  fx  src/render/fx.js re-stamped {old_sha[:16]} -> "
          f"{new_sha[:16]}  (inlined copy verified byte-identical)")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT, and item one is not optional (v43 §13, brief §0.3):")
    print(f"    python cinema_clip.py --game {A.out} --a vesper "
          f"--b emberedge --seed <seed> --full   # FILM IT FIRST")
    print(f"    python vesper_relic_probe.py --relic {A.out}")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python verify.py --game {A.out} --n 40")
    print("    python vesper_sweep.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
