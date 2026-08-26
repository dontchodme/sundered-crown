#!/usr/bin/env python3
"""FOREGONE and THE CONVERSE. The runic scythe, and the twenty-first relic.

    python3 foregone_build.py --src ../02-chain/sc-redflail.html \
                              --out ../02-chain/sc-foregone.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v39 design document:

    "when the ult procs the ball begins to leave behind small orbs. the orbs
     pulse a blue electric ring of damage while they presist. a line draws the
     orbs together. then at the end of the ult the artifact quickly reverses
     through the line, retracing its path. every time it makes it back to an
     orb it pulses again, this time larger, applying the status effect and
     dealing extra damage."

Four interview answers, and every one of them is load-bearing:

    the BALL ITSELF retraces, on rails, and is left at the OLDEST orb
    an orb is dropped every N units TRAVELLED, not every N seconds
    the line is PRESENTATION -- it deals nothing
    NOTHING interrupts it once it procs. Not hitstun, not a true stun

## What is new, and it is nearly all of it

Nothing in this engine has ever recorded where a fighter HAS BEEN. `f.trail`
is 18 points of rolling art and is overwritten four times a second. Nothing
has ever taken the caster off its own steering either: the Crucible pulls the
FOE, Dirge pulls the FOE, Ironbloom latches the FOE. Fourteen ult kinds and
not one of them is a path.

So this is two new things at once -- a path memory and a caster on rails --
and the second is the one with teeth, because `move()` has already integrated
gravity and the walls by the time the retrace runs. The retrace therefore
OVERWRITES position rather than applying a force. A force would be a very
strong shove that a knock could out-push, and a line that is sometimes not
retraced is not a line.

## What is free

The pulses are `ring` + `hurt` + `apply`, which is the nova's own resolution
with an (x, y) that is not the caster's. `ballCollision` runs AFTER the
retrace, so the reversing ball shoulders the foe out of its way and the foe
can crowd the line, and neither of those needed writing.

## The zero-burden argument, kept structurally

    ALL STATE LIVES IN `f.ultTrace`, WHICH IS null ON EVERY OTHER RELIC.

`tickRetrace` returns on its first line when neither fighter has one. There is
no edit anywhere else in the tick -- unlike the spike storm, which had to
touch the chain drive multiplier. `engine_ab` on the twenty pre-existing ids
is the proof, not this paragraph.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `orbDmg`, `bloomDmg`, `bloomHex` and `lay` are unset in the design and
cannot be guessed. The pulse economy especially: an orb laid at t=0 pulses
seven times and one laid at t=3.6 pulses once, so the ultimate's damage is
quadratic in a duration nobody has swept, and how much of it LANDS depends on
where the foe is relative to a trail the caster left while running from it.
`foregone_probe.py` is the instrument and it is the next thing.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC_ID = "foregone"
# FOREGONE. The runic register is logic -- Axiom, Corollary, Unmaking -- and
# the word does two jobs at once that no other candidate did. "Fore-gone" is
# literally *already travelled*, which is what the trail is; and a foregone
# conclusion is one whose end is settled before it arrives, which is Rick's
# fourth interview answer stated as a name. The rule and the word are the
# same sentence.
RELIC_NAME = "Foregone"
# CONVERSE. The logical operation that reverses a statement, sitting beside
# Corollary in the same vocabulary, and the mechanic in one word.
ULT_NAME = "Converse"

# PLACEHOLDER. The type's own damage is Thornwake's 31.35 against Lastlight's
# 17.5, and Lastlight is the precedent for a scythe whose ultimate is most of
# what it is. Runic already carries the two lowest blades in the game (Axiom
# 7.42, Spellbreaker 8.81) as the price of hex. Swept by foregone_sweep.py.
# SWEPT THREE TIMES, AND THE THIRD ONE UNDID THE SECOND.
#
#   22 -> 50.8%   before the waves travelled
#   22 -> 62.9%   once they travelled and KNOCKED, so 16 was taken
#   16 -> 34.5%   once the knock pointed the right way
#
# The middle row was a bug wearing a balance number. The knock added an
# outward impulse to a foe that was 95% of the time moving INTO the wave, so
# it cancelled momentum instead of throwing: measured, a bloom left the foe
# 121 u/s SLOWER. A braked foe stays in the trail and eats the next eleven
# waves, which is why the relic looked strong and why the blade had to come
# down to 16 to compensate.
#
# With the inward component killed first -- 100% of connections now leave
# going outward -- the knock does the opposite: it shoves the foe OUT of the
# trail it is standing in. Re-swept, 20 foes x 30 pinned seeds, SE 2.0pp:
#
#   dmg   31.35   28     26     24     22     20     18     16
#   win    64.5  56.7   54.0   49.7   45.2   41.8   37.3   34.5
#
# 24 TAKEN. The type's own mean is 24.4 -- Thornwake's 31.35 against
# Lastlight's 17.5 -- so this relic pays 2% in the blade and is a scythe that
# HAS an ultimate, the opposite shape to Lastlight after all.
#
# v39c recorded that this relic had become "an ultimate with a scythe
# attached ... by accident". It had, and the accident was the knock's
# DIRECTION. Fixing the direction put the shape back. Worth keeping both
# rows: a balance number that moves 15 points on a sign error is a balance
# number that was measuring the bug.
TUNED_FG = 24.0

ULT = {
    # PHASE 1. Four seconds is long enough for the line to become a shape the
    # eye can hold and short enough that the fight does not stop being a fight.
    "lay": 4.0,
    # Distance, not time -- Rick's answer. Cruise is 405 u/s, so 130 units is a
    # sigil every 0.32s for a ball travelling freely, and none at all for one
    # pinned in a corner.
    "gap": 130,
    # A ceiling, so the retrace's length has an upper bound and so does the
    # pulse economy. 12 sigils x 130 units is a 1560-unit path in a hall whose
    # diagonal is 950 -- the trail is expected to cross itself.
    "maxOrbs": 12,
    "pulse": 0.62,      # seconds between a sigil's own rings
    "orbDmg": 2.0,      # PLACEHOLDER
    "orbR": 88,         # 2.6 ball radii
    # THE WAVE. Rick, on Razor's Plasma Field: thicker, slower, with weight.
    # `band` is the HALF-THICKNESS of the plasma in sim units, and it is one
    # number for the picture and the rule -- `_wave` draws across r +/- band
    # and `_tickWaves` connects across r +/- band, so what the viewer sees is
    # the hitbox.
    "orbBand": 15,
    # HOW JAGGED, as a fraction of the band. One number for both wave kinds
    # so the lightning is the same lightning at both sizes. 0.50 was Rick's
    # "too jagged" -- at half the band the radial swing is the same order as
    # the band's own thickness and the loop reads as a saw. 0.26 keeps the
    # sharp corners and the straight runs and stops the silhouette fighting
    # the band.
    "jag": 0.26,
    # How often the field crackles on its own, in seconds. The ultimate used
    # to be silent unless a wave CONNECTED, which meant the loudest thing on
    # screen made no sound at all most of the time.
    "arcEvery": 0.13,
    "orbTravel": 0.70,  # 88/0.70 = 126 u/s against a 405 cruise
    # MEASURED, not guessed. With the direction fixed, 95% of connections
    # catch the foe moving INTO the wave at -360 and it left at +78 -- out,
    # correctly, but a nudge against a cruise of 405 and invisible for it.
    "orbKnock": 150,

    # "quickly reverses". 1600 u/s against a cruise of 405: four times the
    # speed of anything else in the hall, and a full 1560-unit path in ~1s.
    "speed": 1600,
    "bloomDmg": 9.0,    # PLACEHOLDER
    "bloomR": 130,
    "bloomBand": 26,      # the reversal's wave is the heavy one
    "bloomTravel": 0.62,  # 130/0.62 = 210 u/s -- half a ball's cruise
    # 210 reversed the foe from -425 to +214, which reads. 300 is
    # deliberately above CONFIG.combat.knock's 165 by the same margin
    # Grudgebearer's knockMul 2.3 puts it above -- this is the heavy one.
    "bloomKnock": 300,
    # PLACEHOLDER, and the one the whole cell turns on. Hex caps at 5 and runs
    # 2.6s; twelve applications inside one second is the only way this school's
    # status reaches its own cap on the type that contacts least.
    "bloomHex": 2,
    # SWEPT, on 160 pinned matches with the fights simulated ONCE and only
    # the plan recomputed per value -- crowdMul does not touch the sim, so a
    # row that re-simulated would be measuring the same fights twice at the
    # cost of the sweep's resolution:
    #
    #   crowdMul    0     3     4    4.5    5     6     7     8     9    10+
    #   ex-kill  15.61 10.17  4.32  3.82  2.66  2.49  1.83  1.33  1.16  1.00
    #
    # 7 TAKEN. Not "the last value above parity" this time -- the curve does
    # not fall off a cliff here the way Bloodmill's did, it FLATTENS at
    # exactly 1.00x from 10 onward, because the cuts that survive are single
    # hits and a grouping rule cannot touch a single hit (v38 found the same
    # floor). So the choice is between parity and a value above it, and
    # v37's argument decides it: 1.00x would be wrong, because the ultimate
    # does put more real spectacle on the floor. 7 lands the third crowding
    # ultimate in the band the first two were tuned into --
    # Triplicate 1.69x, Bloodmill 2.16x, the Converse 1.83x.
    "crowdMul": 7,
}

EDITS = [
    # ---------------------------------------------------------------- 1 --
    ("the relic",
     '''    blurb:"Pit chain and a fistful of hooks. Wind it up far enough and it throws its own teeth." },


];''',
     '''    blurb:"Pit chain and a fistful of hooks. Wind it up far enough and it throws its own teeth." },

  /* FOREGONE -- the runic scythe, and the first relic in the game whose
     ultimate is made out of WHERE IT HAS BEEN. Physics are Thornwake's and
     Lastlight's exactly (the type owns them); the school owns Hex and the
     blue. `_scConjured` already draws it and always has -- a crescent on a
     haft of detached shards, Axiom's own grammar, "held in formation by
     nothing at all" -- and until this relic existed nothing could reach it.

     THE CELL'S PROBLEM, measured before the design existed
     (`runic_scythe_probe.py`, and the survey that chose the cell):

       hex holds >=2 stacks for 18% of a fight here and reaches its cap 1% of
       the time, because hex runs 2.6s -- the shortest clock in the game --
       and the scythe contacts 0.196 times a second, the second lowest.

     And the finding that reframed it: hex is not a QUANTITY like every other
     school's status, it is a RATE. `hexClock += dt * stacks`, fire at 1.15.
     One stack already locks the foe's weapon every 1.15s, so 18%-at-two-
     stacks still delivers a weapon shut for 24.8% of the fight, +10.1pp of it
     hex's own against an A/B with `onHit` deleted. The ladder is a rate
     multiplier, not a gate -- which is why an ultimate that drives the foe to
     the CAP, twelve times inside one second, is the thing this cell has been
     missing rather than a bigger blade.

     `dmg` is a PLACEHOLDER -- foregone_build.TUNED_FG -- and MUST be swept. */
  { id:"%ID%", name:"%NAME%", aff:"runic", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:%DMG%, spin:3.2, mode:"spin", mass:2.4,
    onHit:{ hex:1 },
    ult:{ name:"%ULT%", charge:15, kind:"retrace",
          lay:%LAY%, gap:%GAP%, maxOrbs:%MAXORBS%,
          pulse:%PULSE%, orbDmg:%ORBDMG%, orbR:%ORBR%,
          orbBand:%ORBBAND%, orbTravel:%ORBTRAVEL%, orbKnock:%ORBKNOCK%, jag:%JAG%, arcEvery:%ARCEVERY%,
          speed:%SPEED%, bloomDmg:%BLOOMDMG%, bloomR:%BLOOMR%, bloomHex:%BLOOMHEX%,
          bloomBand:%BLOOMBAND%, bloomTravel:%BLOOMTRAVEL%, bloomKnock:%BLOOMKNOCK%,
          crowdMul:%CROWDMUL%,
          tip:"Leaves sigils as it moves, then rewinds its path through them" },
    blurb:"Shards that remember the room. What it has already done to you, it can do again, backwards." },

];'''),

    # ---------------------------------------------------------------- 2 --
    ("the state field",
     '''    this.ultSpin = null;     // {t, dur} while the shades walk''',
     '''    this.ultSpin = null;     // {t, dur} while the shades walk
    /* {phase,t,orbs,i,since,lx,ly,sp0} while the Converse lays its trail and
       then reverses through it. null on every other relic, which is the whole
       zero-burden argument -- and unlike the spike storm there is no second
       edit anywhere in the tick, so the guard in tickRetrace is the only
       cost this relic imposes on a match it is not in. */
    this.ultTrace = null;'''),

    # ---------------------------------------------------------------- 3 --
    ("fireUlt — the retrace does not resolve here",
     '''    if (u.kind === "spinstorm"){
      f.ultSpin = { phase: "wind", t: 0, stun: 0, acc: 0, n: 0, peak: 0, chuff: 0 };
    }''',
     '''    /* THE CONVERSE RESOLVES NOTHING HERE. It starts a trail. Everything
       below this point is skipped for the reason the aimed shot, the
       Crucible and Ironbloom skip it: an ultimate that had already paid out
       before the reversal would make the reversal decorative -- and the
       reversal is the entire ultimate. */
    if (u.kind === "retrace"){
      f.ultTrace = { phase: "lay", t: 0, orbs: [], waves: [], i: -1, since: 0,
                     lx: f.x, ly: f.y, sp0: Math.hypot(f.vx, f.vy),
                     blooms: 0, pulses: 0, laid: 1, hits: 0, waveN: 0,
                     released: false };
      /* THE FIRST SIGIL IS WHERE THE CAST HAPPENED, and it is not a
         convenience. Orbs are laid by DISTANCE, so a caster killed, cornered
         or pinned before it travels `gap` would otherwise hold an ultimate
         made of nothing and a retrace with no destination -- the picture
         simply would not happen. It also makes the LAST thing the reversal
         reaches the place the ultimate was called from, which is the sentence
         the mechanic is. */
      f.ultTrace.orbs.push({ x: f.x, y: f.y, p: u.pulse, born: 0 });
      this.ultFx.phase = "lay";
      /* NORMAL path: the fx clock runs at 2x sim time. See the note on
         Slagburst's fuse -- every `life` in this engine is in half-seconds. */
      this.ultFx.life = (u.lay + 1.4) * 2;
      /* No banner. The name goes on the REVERSAL, where the thing happens --
         the Crucible, Ironbloom and the aimed shot all place it the same way.
         You do not caption a promise. */
      this.banner = null;
      return;
    }
    if (u.kind === "spinstorm"){
      f.ultSpin = { phase: "wind", t: 0, stun: 0, acc: 0, n: 0, peak: 0, chuff: 0 };
    }'''),

    # ---------------------------------------------------------------- 4 --
    ("tickRetrace",
     '''  tickSpinStorm(dt){
    if (!this.a.ultSpin && !this.b.ultSpin) return;''',
     '''  /* THE CONVERSE. Rick's words are quoted in full in the v39 design doc;
     the two sentences this method is are

       "the ball begins to leave behind small orbs ... a line draws the orbs
        together. then at the end of the ult the artifact quickly reverses
        through the line, retracing its path."

     Called deliberately AFTER the fighter loop and BEFORE `ballCollision`.
     `move()` has already integrated gravity and bounced this frame's walls by
     the time this runs, and the retrace OVERWRITES the position it produced.
     That is what makes it rails: an impulse would be a very strong shove that
     a warhammer could out-push, and a line that is sometimes not retraced is
     not a line. `ballCollision` still runs afterwards, so the reversing ball
     shoulders the foe out of its way and the foe can crowd the line -- both
     free, neither written.

     ALL STATE LIVES IN `f.ultTrace`, null on every other relic. */
  tickRetrace(dt){
    if (!this.a.ultTrace && !this.b.ultTrace) return;
    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const S = f.ultTrace;
      if (!S) continue;
      const u = f.w.ult;
      S.t += dt;
      /* THE PLASMA OUTLIVES THE RAILS. A wave born on the last sigil needs
         `bloomTravel` more seconds to finish crossing the floor, and the
         caster gets its steering back the instant the reversal ends. Those
         are two different moments, and conflating them either cuts the last
         wave off mid-flight or holds the ball hostage to its own art. */
      this._tickWaves(f, foe, dt);
      if (S.phase === "spent"){
        if (!S.waves.length) f.ultTrace = null;
        continue;
      }

      /* Every sigil still on the floor pulses on ITS OWN clock, in both
         phases. They are laid at different moments so they are deliberately
         out of phase with each other -- one clock for all of them would read
         as a single flashing object that happens to have several bodies. */
      for (const o of S.orbs){
        o.p -= dt;
        if (o.p <= 0){
          o.p += u.pulse;
          S.pulses++;
          this._traceBurst(f, foe, o, u.orbR, u.orbDmg, 0, false);
        }
      }

      if (S.phase === "lay"){
        /* DISTANCE, not time -- Rick's answer, and the failure modes are why.
           Time-gated, a ball pinned in a corner drops every sigil on top of
           itself and the line collapses to a dot with nothing to retrace.
           Distance-gated, that same ball lays almost nothing, which is a
           smaller ultimate rather than an incoherent one. The trail is a
           record of where the fight actually went. */
        S.since += Math.hypot(f.x - S.lx, f.y - S.ly);
        S.lx = f.x; S.ly = f.y;
        if (S.since >= u.gap && S.orbs.length < u.maxOrbs){
          S.since = 0;
          S.orbs.push({ x: f.x, y: f.y, p: u.pulse, born: S.t });
          S.laid++;
          this.ring(f.x, f.y, f.aff.glow, 3, 46, 0.30, 4);
          SFX.play("ult", { w: "foregone-orb", n: S.laid });
        }
        if (S.t >= u.lay){
          S.phase = "trace";
          S.i = S.orbs.length - 1;
          S.t = 0;
          /* THE RAIL CARRIES ITS OWN POSITION, and this is not bookkeeping.
             `move()` has already integrated `f.vx` into `f.x` by the time
             this method runs, and the reversal sets `f.vx` for the ART -- the
             trail, the blur and the weapon's lean all read velocity. Advance
             `f.x` from wherever move() left it and the two integrations ADD:
             measured at 2645 u/s against a `speed` of 1600, so the knob did
             not mean what it said and the reversal was 65% too fast. The rail
             is advanced instead and `f.x` is assigned from it, so move()'s
             contribution is overwritten rather than compounded, and
             `ballCollision` can still shove the ball for a frame without the
             displacement accumulating into the path. */
          S.px = f.x; S.py = f.y;
          /* THE NAME GOES HERE, on the payoff. */
          this.banner = { text: u.name, life: 2.1, max: 2.1, color: f.aff.core,
                          glow: f.aff.glow, w: f.w.id, bx: f.x, by: f.y };
          this.shake = Math.max(this.shake, 26);
          /* CINEMA. The cast beat fired four seconds ago on a promise; this
             is the beat the director should actually be cutting to. */
          this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: f.x, y: f.y,
                      w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
          SFX.play("ult", { w: "foregone-reverse" });
        }
        continue;
      }

      /* THE REVERSAL. Newest sigil to oldest, on rails, and NOTHING STOPS IT
         -- Rick's answer, and it is the rule the relic's name is. The trade
         an uninterruptible ultimate has to make is made in the TELEGRAPH: the
         sigils are on the floor and drawn together by the line for four
         seconds before the reversal begins, so what is coming is legible long
         before it arrives.

         The weapon is NOT stopped. The relic does not stop being a scythe
         because it is travelling -- Bloodmill's answer to the same question,
         "the caster keeps fighting throughout" -- so the reversal can connect
         on contact as well as on a bloom, under the rules every swing lives
         under. */
      let budget = u.speed * dt;
      if (S.px === undefined){ S.px = f.x; S.py = f.y; }
      /* Bounded. `speed * dt` is 13 units against a `gap` of 130, so one
         sigil a frame is already the ceiling; the guard exists so that a
         future gap smaller than a frame's travel cannot hang the match. */
      let guard = 0;
      while (budget > 0 && S.i >= 0 && guard++ < 8){
        const o = S.orbs[S.i];
        const dx = o.x - S.px, dy = o.y - S.py;
        const d = Math.hypot(dx, dy);
        if (d <= budget || d < 1e-6){
          S.px = o.x; S.py = o.y;
          budget -= d;
          S.blooms++;
          this._traceBurst(f, foe, o, u.bloomR, u.bloomDmg, u.bloomHex, true);
          S.orbs.splice(S.i, 1);      // spent: it has already fired
          S.i--;
        } else {
          S.px += dx / d * budget;
          S.py += dy / d * budget;
          /* Set for the ART and the facing, not for the motion -- the
             position above is the motion. The trail, the blur and the
             weapon's own lean all read velocity, and a ball crossing the hall
             at 1600 with `vx` left at its cruise would draw as if it were
             standing still. */
          f.vx = dx / d * u.speed;
          f.vy = dy / d * u.speed;
          budget = 0;
        }
      }
      /* The rail is authoritative. Assigned once, after the whole budget has
         been spent, so a frame that crosses several sigils lands where the
         last one left it rather than at the first. */
      f.x = S.px; f.y = S.py;
      if (S.i < 0){
        /* Control returns AT the oldest sigil, and at the speed the ball was
           carrying before the cast rather than at 1600. `move()`'s relax term
           takes 1/0.62 of a second to pay back an overspeed, so handing the
           ball back at retrace speed would fire it across the hall as a
           parting gift the design does not describe. */
        const sp = Math.hypot(f.vx, f.vy) || 1;
        const k = (S.sp0 || CONFIG.physics.cruise) / sp;
        f.vx *= k; f.vy *= k;
        /* SPENT, not gone. The rails are over and the ball is its own again;
           what is left is plasma still crossing the floor, and it still
           connects. `released` is the moment the reversal ENDED --
           `ultTrace` going null is a later event now, and foregone_probe
           measures against `released`. */
        S.released = true;
        S.phase = "spent";
        if (!S.waves.length) f.ultTrace = null;
      }
    }
  }

  /* ONE BURST, TWO SIZES. The small one is a sigil ticking over while it
     waits and carries NO status; the big one is the reversal arriving and is
     the only thing in this ultimate that applies hex.

     NOT routed through `resolveHit`, and `f.hits` is deliberately NOT
     incremented. v38 §7 found the published contact-rate table had been
     counting ultimates as contact and that a type-ordering finding drawn from
     it was wrong. A pulse is not a swing. Damage still goes through `hurt`,
     so a ward eats it exactly like anything else. */
  /* A WAVE IS SPAWNED HERE. IT IS NOT RESOLVED HERE.

     The first cut resolved on the frame the ring was born and then drew a
     ring expanding for half a second afterwards, which is a picture that
     lies about its own rule -- and Rick asking for the wave to be SLOWER
     makes the lie worse, not better: at `bloomTravel` 0.62 the damage would
     land two thirds of a second before the plasma arrived. So the wave
     travels and connects when it passes, which is also the thing worth
     taking from Plasma Field: a band with a POSITION, that you can be
     outside of.

     `_traceBurst` keeps its name because it is still the single site a bloom
     happens at, and foregone_probe wraps it to count them. */
  _traceBurst(f, foe, o, R, dmg, hexN, big){
    const u = f.w.ult, S = f.ultTrace;
    if (!S) return;
    S.waves.push({
      x: o.x, y: o.y, t: 0, big: !!big,
      /* BORN AS A RING, not as a dot. A wave whose radius is smaller than
         its own band cannot draw as a band -- the widest pass swallows the
         hole and it reads as a filled star. Starting at 0.8 band means the
         first frame is already a loop. */
      r0: (big ? (u.bloomBand || 26) : (u.orbBand || 15)) * 0.8, r1: R,
      dur: big ? (u.bloomTravel || 0.62) : (u.orbTravel || 0.70),
      band: big ? (u.bloomBand || 26) : (u.orbBand || 15),
      dmg, hexN, knock: big ? (u.bloomKnock || 210) : (u.orbKnock || 70),
      /* Deterministic per wave -- the crackle has to reproduce frame for
         frame or a re-render is a different video, so the seed is a counter
         out of the sim and never `Math.random()`. */
      seed: (S.waveN = (S.waveN || 0) + 1),
      hit: false,
    });
    if (S.waves.length > 26) S.waves.shift();
    if (big) this.spawnFx(o.x, o.y, f.aff.glow, 12, 200, 0.45, 4);
  }

  /* THE WAVES TRAVEL, AND THEY CONNECT WHEN THEY ARRIVE.

     Linear in radius, deliberately. `drawRings`' shared easing is
     `k*k*0.7 + k*0.3`, which ACCELERATES -- correct for a shockwave leaving
     an impact and wrong for a field being driven outward, which is what this
     is. A constant rate is also the only one a viewer can lead. */
  _tickWaves(f, foe, dt){
    const S = f.ultTrace;
    if (!S || !S.waves.length) return;
    /* THE FIELD HAS A VOICE OF ITS OWN. Every other sound this relic makes
       is fired by an EVENT -- a sigil laid, a wave connecting, the turn --
       so a cast that never touched anything was silent while filling the
       screen. This is the arc frying, on a clock, for as long as there is
       plasma on the floor. `waveN` varies the grain and is a sim counter,
       so a render reproduces. */
    S.arc = (S.arc || 0) - dt;
    if (S.arc <= 0){
      S.arc = f.w.ult.arcEvery || 0.13;
      SFX.play("ult", { w: "foregone-arc", n: S.waveN + S.waves.length });
    }
    for (let i = S.waves.length - 1; i >= 0; i--){
      const w = S.waves[i];
      w.t += dt;
      const k = w.t / w.dur;
      if (k >= 1){ S.waves.splice(i, 1); continue; }
      if (w.hit || !foe.alive) continue;
      const r = w.r0 + (w.r1 - w.r0) * k;
      const d = Math.hypot(foe.x - w.x, foe.y - w.y);
      /* Inside the band, OR still inside the leading edge on the first
         frames -- a foe standing on the sigil is enclosed by the wave before
         it has any radius to speak of, and must not be missed for it. */
      if (Math.abs(d - r) > w.band && !(d < r && w.t <= dt * 2)) continue;
      w.hit = true;
      this._traceHit(f, foe, w, d);
    }
  }

  /* ONE CONNECTION, TWO SIZES. The small wave is a sigil ticking over while
     it waits and carries NO status; the big one is the reversal arriving and
     is the only thing in this ultimate that applies hex.

     NOT routed through `resolveHit`, and `f.hits` is deliberately NOT
     incremented. v38 s7 found the published contact-rate table had been
     counting ultimates as contact and that a type-ordering finding drawn
     from it was wrong. A wave is not a swing. Damage still goes through
     `hurt`, so a ward eats it exactly like anything else. */
  _traceHit(f, foe, w, d){
    const n = Math.round(w.dmg * this.actMods.dmg * foe.dmgTakenMul());
    if (n > 0){
      this.hurt(foe, n, f);
      f.dealt += n;
      foe.flash = 1;
      this.float(foe.x, foe.y - 40, n, w.big ? "#FFF4D0" : f.aff.glow,
                 w.big ? 44 : 26);
    }
    /* THE WEIGHT. Rick: "they should cause knockback and feel like they have
       some weight to them." Outward from the WAVE'S OWN CENTRE -- the sigil,
       not the caster -- because the plasma is the thing pushing and it
       pushes away from where it came from. Priced against
       `CONFIG.combat.knock` (165): a bloom at 210 is heavier than an
       ordinary blow, a sigil's own wave at 70 is a shove.

       x knockMul like every other knock in the game, so this relic is not
       quietly exempted from the one rule knockback has. */
    const dl = d || 1;
    const kx = (foe.x - w.x) / dl, ky = (foe.y - w.y) / dl;
    const power = w.knock * (f.w.knockMul || 1);
    /* THE INWARD COMPONENT IS KILLED FIRST, and that is the difference
       between a knockback and a brake.

       Adding an outward impulse to a ball that is travelling INTO the wave
       just cancels momentum: measured over 566 connections, a bloom left the
       foe 121 units a second SLOWER and a sigil wave 45 slower. Rick, on the
       video: "where is the knockback happening on the rings? i see the green
       ball passing right through them with no knockback." He was right, and
       it was not that the knock never fired -- it was that a ball which
       merely slows does not read as a ball that was hit.

       So the radial velocity is zeroed when it points inward, and only then
       is the impulse applied. A body caught by an expanding front always
       leaves it going outward. This is not a bigger number, it is the
       right direction -- and it is what `resolveHit`'s knock gets for free,
       because a swing that connects has already carried the foe away. */
    const vr = foe.vx * kx + foe.vy * ky;
    if (vr < 0){ foe.vx -= vr * kx; foe.vy -= vr * ky; }
    foe.vx += kx * power; foe.vy += ky * power;
    if (w.hexN){
      foe.apply("hex", w.hexN);
      const first = !this.taught.hex && !!(STATUS.hex && STATUS.hex.tip);
      if (first) this.taught.hex = true;
      this.statusTag(foe.x, foe.y, "hex", first);
    }
    if (w.big){
      foe.ringFlash = 1;
      this.shake = Math.max(this.shake, 18);
      /* ON CONNECTION ONLY. Twelve unconditional freezes inside one second
         would be a third of a second of stopped hall -- and because `step()`
         returns above `tickRetrace` while `hitStop` runs, they would be
         stopping the very reversal that caused them. */
      this.hitStop = Math.max(this.hitStop, 0.035);
    }
    if (f.ultTrace) f.ultTrace.hits++;
    SFX.play("ult", { w: w.big ? "foregone-bloom" : "foregone-tick",
                      n: w.seed });
  }

  tickSpinStorm(dt){
    if (!this.a.ultSpin && !this.b.ultSpin) return;'''),

    # ---------------------------------------------------------------- 5 --
    ("the tick call",
     '''    this.tickSpinStorm(dt);''',
     '''    this.tickSpinStorm(dt);
    /* AFTER the fighter loop, so `move()` has already had its say and the
       retrace overwrites it; BEFORE `ballCollision`, so the reversing ball
       still shoulders the foe. Both are load-bearing -- see tickRetrace. */
    this.tickRetrace(dt);'''),

    # ---------------------------------------------------------------- 6 --
    ("the match cannot outlive the trail",
     '''    if (this.over && (this.a.ultSpin || this.b.ultSpin)){
      this.a.ultSpin = null; this.b.ultSpin = null;
    }''',
     '''    if (this.over && (this.a.ultSpin || this.b.ultSpin)){
      this.a.ultSpin = null; this.b.ultSpin = null;
    }
    /* And the Converse cannot either, for exactly the same reason: `step()`
       returns from the `over` branch before `tickRetrace` is reached, so a
       reversal left running would sit frozen mid-flight -- with the ball
       parked between two sigils, off its own physics -- through the whole
       verdict beat. */
    if (this.over && (this.a.ultTrace || this.b.ultTrace)){
      this.a.ultTrace = null; this.b.ultTrace = null;
    }'''),

    # ---------------------------------------------------------------- 7 --
    ("dropped when the caster dies",
     '''    if (f.ultHarrow && (!f.alive || !foe.alive || this.over)){
      f.ultHarrow = null;
      this.unstick(foe);
    }''',
     '''    if (f.ultHarrow && (!f.alive || !foe.alive || this.over)){
      f.ultHarrow = null;
      this.unstick(foe);
    }
    /* ABOVE THE GUARD, for the reason the Harrowing's fuse is above it: a
       fatal blow arms `killFlight` and `checkEnd` holds the match OPEN while
       the loser flies into the wall, and during those frames `over` is false
       and `move()` is still running. A caster that dies mid-reversal has to
       be handed back to its own physics before that flight begins, or it
       spends its death on rails.

       `!foe.alive` is deliberately NOT in this condition. The Harrowing needs
       it because its fuse detonates ON the foe; the reversal is a thing the
       caster does to the FLOOR, and a trail that stops being retraced the
       instant the foe drops would cut the ultimate off mid-picture on exactly
       the casts that won the fight. */
    if (f.ultTrace && (!f.alive || this.over)){
      const sp = Math.hypot(f.vx, f.vy) || 1;
      const k = (f.ultTrace.sp0 || CONFIG.physics.cruise) / sp;
      f.vx *= k; f.vy *= k;
      f.ultTrace = null;
    }'''),

    # ---------------------------------------------------------------- 8 --
    ("the trail, drawn",
     '''  drawUltUnder(m){
    if (m.wallCrack) this._wallCrack(m);''',
     '''  /* THE LINE AND THE SIGILS. Presentation only -- Rick's answer -- and it
     is the entire telegraph. An ultimate that nothing can interrupt has to be
     legible BEFORE it arrives, so the route the reversal will take is drawn
     on the floor from the moment the second sigil lands, and the viewer has
     four seconds to read it.

     Drawn from `f.ultTrace` and NOT from `m.ultFx`. ultFx is a fire-and-
     forget record with a clock of its own that expires; these are live
     simulation objects whose positions the sim keeps updating, and drawing
     them from a copy is how a set-piece ends up describing a fight that has
     moved on. Called ABOVE the `_ult` guard, because that guard returns when
     ultFx has expired and the trail outlives it. */
  _retraceField(m){
    if (!m.a.ultTrace && !m.b.ultTrace) return;
    const c = this.ctx;
    for (const f of [m.a, m.b]){
      const S = f.ultTrace;
      if (!S || (!S.orbs.length && !S.waves.length)) continue;
      const u = f.w.ult, aff = f.aff;
      c.save();
      c.globalCompositeOperation = "lighter";
      c.lineCap = "round"; c.lineJoin = "round";

      /* THE PLASMA, AND IT IS A BAND RATHER THAN A STROKE.

         What a plasma field looks like is not a fat line -- it is a VOLUME
         with structure in it, and four passes is what that takes:

           a wide soft bloom in `core`, which is the field's own light
           the body, saturated, at the full band width
           a hot core inside it, a third the width
           filaments, cracking around the band and rotating as it opens

         Composited with `lighter`, so the four SUM where they overlap and
         the middle of the band goes white while its edges stay school blue.
         That is the one thing a single stroke of any width cannot do.

         The band barely tapers -- `1 - k*0.22` against `drawRings`' shared
         `1 - k*0.7`. A shockwave thins as it spreads because it is spending
         itself; a driven field does not, and Rick's note is about exactly
         that difference. */
      for (const w of S.waves){
        const wk = clamp(w.t / w.dur, 0, 1);
        const wr = w.r0 + (w.r1 - w.r0) * wk;
        const bw = w.band * (1 - wk * 0.22);
        /* Held flat for the first fifth, then out. A field that starts
           fading the instant it is born never looks like it had any. */
        let fd = 1 - Math.max(0, (wk - 0.2) / 0.8);
        /* A SPENT WAVE LOOKS SPENT. There is one opponent, so a wave that has
           connected has nothing left to do -- and it was still drawing at
           full brightness, so the foe spent 26% of every cast standing inside
           a band that could not touch it while only 8% of those frames were
           a real connection. That is a picture promising something the rule
           has already delivered, which is the same failure as the old
           instant-damage ring with the sign flipped.

           Discharged, not deleted: it keeps travelling and keeps fading, so
           the eye can still see where the front got to. */
        if (w.hit) fd *= 0.34;

        /* A JAGGED CIRCLE OF THICK LIGHTNING, and the jag is a PATH rather
           than a decoration on an arc. Rick: "lets not make the rings so
           perfectly circular. a jagged circle of thick lightning."

           `lineTo` and never a curve: lightning is straight runs with sharp
           changes of direction, and a smoothed ring reads as a ripple in
           water. The ANGLES are jittered as well as the radii, so the
           segments come out uneven -- evenly spaced vertices with uneven
           radii still read as a machined cog.

           AND IT MORPHS RATHER THAN SCALING. A fixed jagged shape blown up
           over 0.6s is a logo zooming, not a discharge. The offsets lerp
           between two hash sets three times across the wave's life, so the
           filament reconfigures continuously the way a real arc does --
           deterministic, because the seed is a sim counter and a re-render
           has to be the same video.

           AMPLITUDE IS HALF THE BAND, deliberately. The hit test is
           `|d - r| <= band`, so a jag that reached past `band` would draw
           outside its own hitbox and the promise that what you see is what
           connects would stop being true. */
        /* FEWER VERTICES, SHALLOWER SWING. Lightning is long straight runs
           with sharp changes of direction; 46 vertices at half a band of
           amplitude is a cog. */
        const N = w.big ? 34 : 22;
        /* AND CLAMPED TO THE RADIUS. A newborn wave is 7 units across and a
           band of 26 gives an amplitude of 13, so vertices swung THROUGH the
           centre and the first two frames of every bloom came out as a solid
           white starburst -- an easy thing to miss, because it only happens
           while the ring is too small to look at. Tight jagged dot, opening
           into a jagged ring. */
        const amp = Math.min(w.band * (u.jag || 0.26), wr * 0.40);
        const ph = wk * 3.0, st = Math.floor(ph), tt = ph - st;
        const ez = tt * tt * (3 - 2 * tt);
        const pts = [];
        for (let i = 0; i < N; i++){
          const a0 = shellHash(w.seed * 977 + st, i) - 0.5;
          const b0 = shellHash(w.seed * 977 + st + 1, i) - 0.5;
          const rr = wr + (a0 + (b0 - a0) * ez) * amp * 2;
          const ang = (i / N) * TAU
                    + (shellHash(w.seed * 31, i) - 0.5) * (TAU / N) * 0.6;
          pts.push([w.x + Math.cos(ang) * rr, w.y + Math.sin(ang) * rr]);
        }
        const trace = () => {
          c.beginPath();
          c.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < N; i++) c.lineTo(pts[i][0], pts[i][1]);
          c.closePath();
        };

        /* Four passes over ONE path, so the layers stay registered: a wide
           soft bloom that is the field's own light, the saturated body, and
           a hot core a third the width. Composited with `lighter`, so they
           SUM where they overlap and the middle of the filament goes white
           while its edges stay school blue -- the one thing a single stroke
           of any width cannot do. */
        /* HAIRLINE FILAMENTS, AND HALF OF THEM ARE BEHIND THE BAND.

           Rick, with the reference in front of him: "how about some thinner
           hair line arcs coming off the ring to give it a more realistic
           look and a sense of 3d?"

           The reference is the thing worth reading closely. Its core band is
           SMOOTHER than this one -- the lightning read there does not come
           from the silhouette at all, it comes from a corona of fine
           filaments hugging the band. The first cut of these was six stubs
           at 0.14 of the band width, which is 3.6px on a bloom: chunky spurs
           off a wire, not a corona.

           So: many, thin, and walked rather than drawn as a segment. Each is
           three short runs that kink -- a straight line has no charge in it
           and a curve reads as smoke.

           THE 3D IS THE DRAW ORDER AND THE ALPHA, not perspective. A third
           of them are stroked BEFORE the band and come out dim and partly
           occluded, reading as the far side of a torus; the rest are drawn
           after and read as the near side. Per-filament alpha does the rest.
           This is the cheapest honest depth cue available to a flat canvas
           and it is the one the reference is using. */
        const fil = (behind) => {
          const fn = w.big ? (behind ? 9 : 16) : (behind ? 4 : 7);
          for (let i = 0; i < fn; i++){
            const q = i + (behind ? 200 : 0);
            const pick = Math.floor(shellHash(w.seed * 613 + st, q) * N) % N;
            const p0 = pts[pick];
            let dx = p0[0] - w.x, dy = p0[1] - w.y;
            const dl = Math.hypot(dx, dy) || 1;
            dx /= dl; dy /= dl;
            const out = shellHash(w.seed * 613, q + 32) > 0.34 ? 1 : -1;
            /* Hairline. 1.0-1.7px at a bloom's band of 26, against the
               band's own 26 -- two orders of thinness apart, which is what
               "hairline" has to mean next to a stroke that wide. */
            c.lineWidth = 0.9 + shellHash(w.seed * 613, q + 16) * 0.8;
            c.globalAlpha = fd * (behind ? 0.16 + shellHash(w.seed*613, q+48) * 0.16
                                         : 0.30 + shellHash(w.seed*613, q+48) * 0.45);
            let px = p0[0], py = p0[1];
            let ax = dx * out, ay = dy * out;
            c.beginPath(); c.moveTo(px, py);
            for (let k2 = 0; k2 < 3; k2++){
              const turn = (shellHash(w.seed * 613 + st, q + 64 + k2 * 8) - 0.5) * 1.9;
              const ca = Math.cos(turn), sa = Math.sin(turn);
              const nx2 = ax * ca - ay * sa, ny2 = ax * sa + ay * ca;
              ax = nx2; ay = ny2;
              const len = bw * (0.22 + shellHash(w.seed * 613, q + 96 + k2 * 8) * 0.55);
              px += ax * len; py += ay * len;
              c.lineTo(px, py);
            }
            c.stroke();
          }
        };
        /* THE FAR SIDE FIRST, under the band, so the band occludes it. */
        c.lineCap = "round"; c.lineJoin = "round";
        c.strokeStyle = aff.glow;
        fil(true);

        c.lineJoin = "miter"; c.miterLimit = 2.5;
        /* The soft bloom is CLAMPED TO THE RADIUS. At 2.4 band widths it is
           36px on a ring 45 across, which fills the hole and turns the band
           back into a disc -- the exact thing the band was for. */
        c.globalAlpha = fd * 0.20;
        c.strokeStyle = aff.core;
        c.lineWidth = Math.min(bw * 2.4, Math.max(bw * 0.8, wr * 0.85));
        trace(); c.stroke();
        c.globalAlpha = fd * 0.52;
        c.lineWidth = bw;
        trace(); c.stroke();
        c.globalAlpha = fd * 0.80;
        c.strokeStyle = aff.glow; c.lineWidth = bw * 0.34;
        trace(); c.stroke();


        /* AND THE NEAR SIDE, over it. */
        c.lineCap = "round"; c.lineJoin = "round";
        c.strokeStyle = "#EAF4FF";
        fil(false);
        c.lineJoin = "round";
      }

      /* The line runs through the sigils in the order they were LAID, and on
         to the ball itself while it is still laying -- so it is always
         attached to the thing drawing it and the viewer never has to work out
         which end is live. During the reversal the ball is at the other end
         of the same line, walking it back. */
      const pts = S.orbs.map(o => [o.x, o.y]);
      if (S.phase !== "spent") pts.push([f.x, f.y]);
      if (pts.length > 1){
        /* `core` and NOT `glow`. This is v37 3.2 for the fourth time in the
           project: runic's glow is #BCDDFF, which is near-white, and under
           `lighter` at the alpha the reversal needs it blows out to pure
           white -- so the one element that is supposed to say RUNIC on a
           floor full of it said nothing at all. Measured off the filmstrip,
           not off the palette sheet: at 0.30 it still read blue and at 0.58
           it did not, which is exactly the trap, because the lay phase
           looked correct. `core` is #4A9EFF and holds its hue at any alpha
           this needs. Rick's word for the rings is ELECTRIC and electric is
           saturated, not bright. */
        c.globalAlpha = S.phase === "lay" ? 0.38 : 0.70;
        c.strokeStyle = aff.core;
        c.lineWidth = S.phase === "lay" ? 1.6 : 2.6;
        c.beginPath();
        c.moveTo(pts[0][0], pts[0][1]);
        for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
        c.stroke();
      }

      /* THE SIGIL BREATHES ON ITS OWN PULSE CLOCK, so the ring the viewer
         watches expand is the same clock the damage fires on. Ward's plate
         brightness IS its timer; this is that rule again, and it is why this
         ultimate needs no second HUD element either. */
      for (const o of S.orbs){
        const k = 1 - clamp(o.p / u.pulse, 0, 1);   // 0 just fired, 1 about to
        /* The breathing ring thickens with the same argument as the pulse:
           a 1.4px hairline on a hall 880 units across is a scratch. It also
           now TAPERS as it opens, so the sigil's own tell has the shape of
           the discharge it is counting down to. */
        c.globalAlpha = 0.16 + 0.30 * k;
        c.strokeStyle = aff.core;
        c.lineWidth = 7.0 * (1 - k * 0.62);
        c.beginPath();
        c.arc(o.x, o.y, 7 + u.orbR * 0.86 * k, 0, TAU);
        c.stroke();
        c.globalAlpha = 0.55 + 0.35 * (1 - k);
        c.fillStyle = aff.glow;
        c.beginPath(); c.arc(o.x, o.y, 3.6, 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  drawUltUnder(m){
    this._retraceField(m);
    if (m.wallCrack) this._wallCrack(m);'''),

    # ---------------------------------------------------------------- 9 --
    # --------------------------------------------------------------- 10 --
    ("the director's crowd exception",
     '''    for (const f of [this.a, this.b]){
      if (f.ultSpin){
        o.crowd = true;                                   // the volley rule
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);  // the score bar
      }
    }''',
     '''    for (const f of [this.a, this.b]){
      if (f.ultSpin){
        o.crowd = true;                                   // the volley rule
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);  // the score bar
      }
      /* v39: AND THE CONVERSE, whose crowding is not extra objects at all.

         Triplicate crowds with BODIES and the spike storm with PROJECTILES;
         this relic puts nothing extra on the floor -- its pulses are
         deliberately outside `resolveHit` and emit no beat, exactly so that
         they could not do this. It crowds anyway, and the mechanism is the
         reversal itself: the caster crosses the hall at 1600 against a cruise
         of 405, through twelve sigil positions in about a second, and every
         time it passes through the foe `tickHits` resolves a contact at four
         times the usual closing speed. Measured, 50 matches, by cut KIND:

              kind     in/min  out/min   pref   median score in/out
              ult        0.00     0.00      -   the ult beats are never cut
              hit        3.39     0.19  18.0x   2.51 / 2.11
              volley     1.23     0.19   6.6x   3.15 / 2.26

         Not one `ult` cut in fifty matches. Every cut inside the window is an
         ORDINARY BLOW, landing more often and scoring higher because the ball
         throwing it is moving four times as fast. So the comment above --
         "anything that puts extra hits on the floor belongs in this loop" --
         is right and is not quite general enough: what belongs here is
         anything that puts extra CUTS on the floor, however it does it. */
      if (f.ultTrace){
        o.crowd = true;
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);
      }
    }'''),

    ("the voice",
     '''        } else if (w === "gravemourn"){                 // a drop into the grave''',
     '''        } else if (w === "foregone"){                   // the coil charges
          /* THE CONVERSE, IN SIX VOICES, AND THE INSTRUMENT IS A TESLA COIL.

             Rick, on the first cut: "i cant tell if im hearing balls
             bouncing or lightning. im thinking long zapping sounds like a
             tesla coil." He is right and the diagnosis is DURATION. Those
             sounds were 18 to 140 milliseconds -- at that length anything is
             a click, and the hall is already full of clicks, so they read as
             the thing the ear already had a name for.

             A coil does not click. Its voice is the SPARK-GAP BREAK RATE: a
             harsh sustained buzz around 130 Hz with enormous harmonic
             content, which is a SAWTOOTH, plus the tear of the arc itself,
             which is sustained bandpass noise. Both have to last long enough
             to be heard as a tone rather than as an event -- 0.2s is the
             floor, and the long ones here run to half a second.

             `_tone`'s gain only ever DECAYS, so a SUSTAIN has to be built the
             way the spike storm builds a swell: overlapping events, each
             refreshing the envelope before the last has died. Three stages
             is what holds half a second flat.

             Deliberately NOT Bloodmill's instrument. That was two sawtooths
             a few hertz apart so the ear hears the BEAT as a growl; these are
             a fifth apart so they read as one harsh voice with no throb. */
          [[0.00, 116, 0.10], [0.16, 152, 0.13], [0.32, 208, 0.16]].forEach(
            ([d, f0, g0]) => {
              this._tone(t + d, { freq: f0, to: f0 * 1.5, gain: g0,
                                  dur: 0.24, type:"sawtooth" });
              this._tone(t + d, { freq: f0 * 1.5, to: f0 * 2.25, gain: g0 * 0.5,
                                  dur: 0.24, type:"sawtooth" });
            });
          [[0.00, 1500], [0.16, 2600], [0.32, 4200]].forEach(
            ([d, fq]) => this._burst(t + d, { freq: fq, q: 2.4, gain: 0.075,
                                              dur: 0.24, type:"bandpass" }));

        } else if (w === "foregone-orb"){               // one more is laid
          /* The trail COUNTS ITSELF -- `p.n` is the real sigil index, so the
             pitch climbs a step per orb and the ear hears the line getting
             longer without looking at it. Deterministic, so a render
             reproduces. SAWTOOTH now, not a triangle: the triangle was a
             xylophone, and a xylophone in a hall of bouncing balls is one
             more bounce. */
          const j = Math.min(11, (p.n || 1) - 1);
          const f0 = 150 * Math.pow(1.0595, j * 2);
          this._tone (t, { freq: f0, to: f0 * 0.86, gain: 0.060,
                           dur: 0.17, type:"sawtooth" });
          this._burst(t, { freq: 2600 + j * 180, q: 3.0, gain: 0.038,
                           dur: 0.15, type:"bandpass" });

        } else if (w === "foregone-arc"){               // the coil, running
          /* THE BED, AND IT IS THE SOUND OF THE WHOLE ULTIMATE.

             Fired on a 0.13s clock for as long as there is plasma on the
             floor, and every event is 0.20s long -- so they OVERLAP, and
             what the ear gets is not eight events a second, it is one
             continuous rasp that starts when the ultimate does and stops
             when the last wave dies. That overlap is the entire trick: the
             clock is faster than the decay.

             It has to be quiet, because it is running the whole time. The
             mill's lesson was that a rhythm nobody can hear may as well not
             exist; the opposite lesson is here, and it is that a bed loud
             enough to notice is a bed you cannot stop noticing. */
          const a = (p.n || 0) % 7;
          this._tone (t, { freq: 128 + a * 7, to: 116 + a * 5, gain: 0.042,
                           dur: 0.20, type:"sawtooth" });
          this._tone (t, { freq: 192 + a * 11, to: 174, gain: 0.024,
                           dur: 0.20, type:"sawtooth" });
          this._burst(t, { freq: 2900 + a * 360, q: 3.0, gain: 0.034,
                           dur: 0.20, type:"bandpass" });

        } else if (w === "foregone-tick"){              // a small wave lands
          /* A short zap, not a tick. Same instrument as the big one at a
             fifth of the length -- these fire a few times a second at their
             busiest and must not out-shout the bloom. */
          const k = (p.n || 0) % 5;
          this._burst(t,        { freq: 5200, q: 0.8, gain: 0.070, dur: 0.025, type:"highpass" });
          this._tone (t,        { freq: 158 + k * 11, to: 92, gain: 0.080,
                                  dur: 0.18, type:"sawtooth" });
          this._burst(t + 0.02, { freq: 2600 + k * 260, q: 2.6, gain: 0.055,
                                  dur: 0.16, type:"bandpass" });

        } else if (w === "foregone-reverse"){           // and it turns back
          /* THE ONE SOUND THAT HAS TO STATE THE MECHANIC. Everything in the
             laying phase RISES -- the charge, and twelve orbs stepping up a
             tone at a time. This falls, through the same interval, and it is
             the longest event this relic has: 0.6s of tearing arc, built in
             four overlapping stages so the envelope never sags.

             The sound of the ultimate is the sound of that climb played
             backwards, which is what the ultimate is. */
          this._burst(t, { freq: 7000, q: 0.7, gain: 0.20, dur: 0.045, type:"highpass" });
          [[0.00, 420, 0.20], [0.15, 300, 0.18], [0.30, 208, 0.16], [0.45, 146, 0.13]]
            .forEach(([d, f0, g0]) => {
              this._tone(t + d, { freq: f0, to: f0 * 0.62, gain: g0,
                                  dur: 0.26, type:"sawtooth" });
              this._tone(t + d, { freq: f0 * 1.5, to: f0 * 0.93, gain: g0 * 0.45,
                                  dur: 0.26, type:"sawtooth" });
            });
          [[0.02, 4600], [0.17, 3000], [0.32, 1900], [0.47, 1100]].forEach(
            ([d, fq]) => this._burst(t + d, { freq: fq, q: 2.0, gain: 0.10,
                                              dur: 0.24, type:"bandpass" }));

        } else if (w === "foregone-bloom"){             // a big wave lands
          /* THE LONG ZAP. Only a CONNECTING wave makes this -- measured, a
             cast lands one or two of its twelve blooms -- so unlike the mill
             this can afford to be half a second long and to be the loudest
             thing the relic does.

             Four parts and they are what an arc strike is made of: the
             STRIKE (broadband, 35ms, no ring-out), the BUZZ (a sawtooth pair
             a fifth apart, refreshed three times so it holds), the TEAR
             (sustained bandpass walking down the spectrum), and the BODY --
             a low sine under all of it, which is the weight the knockback
             gives the eye, stated in the dimension the ear reads faster. */
          const k = (p.n || 0) % 5;
          this._burst(t, { freq: 6500, q: 0.7, gain: 0.17, dur: 0.035, type:"highpass" });
          [[0.00, 172, 0.17], [0.13, 150, 0.14], [0.26, 128, 0.10]].forEach(
            ([d, f0, g0]) => {
              this._tone(t + d, { freq: f0 + k * 6, to: (f0 + k * 6) * 0.72,
                                  gain: g0, dur: 0.24, type:"sawtooth" });
              this._tone(t + d, { freq: (f0 + k * 6) * 1.5, to: (f0 + k * 6) * 1.08,
                                  gain: g0 * 0.45, dur: 0.24, type:"sawtooth" });
            });
          [[0.00, 3400], [0.14, 2400], [0.28, 1500]].forEach(
            ([d, fq]) => this._burst(t + d, { freq: fq + k * 180, q: 2.2,
                                              gain: 0.10, dur: 0.24, type:"bandpass" }));
          this._tone(t, { freq: 92, to: 44, gain: 0.13, dur: 0.30, type:"sine" });

        } else if (w === "gravemourn"){                 // a drop into the grave'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
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
    ap.add_argument("--src", default="../02-chain/sc-redflail.html")
    ap.add_argument("--out", default="../02-chain/sc-foregone.html")
    ap.add_argument("--dmg", type=float, default=TUNED_FG)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text()
    s = s0
    print(f"\nFOREGONE BUILD -- the runic scythe and the Converse")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if "_scConjured" not in s0:
        raise SystemExit("this source has no _scConjured -- wrong build")
    if '"retrace"' in s0:
        raise SystemExit("this source already has a retrace -- already built")

    subs = {"%ID%": RELIC_ID, "%NAME%": RELIC_NAME, "%ULT%": ULT_NAME,
            "%DMG%": f"{A.dmg:g}"}
    for k, v in ULT.items():
        subs["%" + k.upper() + "%"] = f"{v:g}"

    for label, old, new in EDITS:
        for k, v in subs.items():
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    out_p.write_text(s)
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print(f"\n  NEXT, and none of it is optional:")
    print(f"    python3 foregone_probe.py --game {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
