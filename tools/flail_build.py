#!/usr/bin/env python3
"""THE BLOODSWORN FLAIL, and the SPIKE STORM. The twentieth relic.

    python3 flail_build.py --src ../02-chain/sc-redbarb.html \
                           --out ../02-chain/sc-redflail.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v38 design document.
Everything here implements those words plus four interview answers:

    the caster KEEPS FIGHTING throughout -- both phases, contact damage and all
    the wind-up is broken by a STUN BUDGET
    40 spikes a second
    the sweep follows the HEAD'S REAL SPEED

## What is genuinely new, and what is free

FREE, and it is the larger half. "the spikes dont bounce but expire when they
hit anything" is `tickShots`' DEFAULT: `s.bounce` undefined means the bounce
branch is skipped and the spent branch kills the shot on any wall. Spinning
weapons already parry shots and the build already argues why -- "an ultimate
that cheated the rules its own weapon lives under would teach the viewer that
the rules are decorative". Nothing about the projectile had to be written.

NEW: a two-phase ultimate whose release condition is a PHYSICAL STATE of the
weapon rather than a clock, and a continuous emitter. Every volley in the game
today is a single burst.

## The zero-burden argument, kept structurally

    ALL STATE LIVES IN `f.ultSpin`, WHICH IS `null` ON EVERY OTHER RELIC.

`tickSpinStorm` returns on its first line when neither fighter has one, so in
every match without this relic -- and in every match with it before the bar
fills -- it costs one null check a frame. The one edit NOT behind that guard is
the chain drive multiplier, and it is an exact identity at rest:

    (f.ultDraw || f.ultForge || f.ultSpin ? (u.spinMul || 1) : 1)

three nulls -> 1, which is the expression that was already there.

`engine_ab` on the nineteen pre-existing ids is the proof, not this paragraph.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `spikeDmg` and above all `budget` are unset in the design and cannot be
guessed. The budget especially: stun stops the drive, so being stunned
LENGTHENS the wind-up, which exposes it to more stun. That is a feedback loop
and its dud rate has to be measured on this build, not modelled from the stun
trace. `flail_relic_probe.py` is that instrument and it is the next thing.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC_ID   = "redflail"
RELIC_NAME = "Threshmaw"
# A flail is a THRESHING tool -- the word is the weapon's own etymology, and
# threshing is violence done to a body until parts come off it, which is the
# bloodsworn argument in one verb. `-maw` for the seven hooks, and because the
# blurb's promise is that it throws its own teeth. On the register of
# Gravemourn / Slagheart / Goreshard rather than of Dawnbringer / Lightkeeper,
# which is where a bloodsworn heavy belongs.
ULT_NAME   = "Bloodmill"
# Rick's pick, over Winnowing, and it is the better one: a mill is a thing that
# TURNS without stopping, so the name points at the wind-up rather than at the
# spray -- and the wind-up is the half a viewer actually watches arrive. The
# spray is the consequence. Winnowing named the consequence and left the
# telegraph unnamed.
TUNED_RF   = 25.0   # SWEPT, 40 pinned seeds x 19 foes = 760 matches a candidate.
                    # 30 -> 58.4% . 28 -> 56.7% . 26 -> 53.3% . 25 -> 48.9%
                    # 24 -> 50.4% . 22 -> 47.0%   (SE about 1.8pp, so 25/24 are
                    # one point, not two). Whole roster at 25: Threshmaw 48.2%,
                    # spread 15.0pp, mean duration 38.2s, 0 timeouts of 7600.
                    #
                    # 25 AGAINST THE TYPE'S 43.3 IS NOT AN ANOMALY, IT IS A
                    # SHAPE THIS ROSTER ALREADY HAS. Lastlight carries 17.5 on
                    # the scythe profile where Thornwake carries 31.35 -- 56%.
                    # This is 58%. Both are relics whose ultimate is most of
                    # what they are, and both pay for it in the blade.
ULT = dict(
    charge   = 16,
    spinMul  = 6.9,    # drive at FULL wind. base spin 2.2 -> 15.18, just over
                       # maxAngVel 15, so the head saturates rather than
                       # overshooting and the release is a real ceiling.
    stormMul = 6.9,    # drive once the spray is running. SEPARATE FROM spinMul
                       # because they are separate claims. Rick's words describe
                       # the head WINDING UP; they say nothing about the arm
                       # still being swung seven times faster for the five
                       # seconds afterwards. That speed-up came free with the
                       # existing spinMul hook and `decomp.py` priced it at
                       # +7.6pp of winrate -- a third of everything the
                       # ultimate is worth, from a mechanic nobody designed.
                       # Defaults equal to spinMul so it is inert until swept.
    ramp     = 0.9,    # PLACEHOLDER, and the most important number here.
                       # seconds for the drive to climb from 1x to spinMul.
                       # WITHOUT IT the wind-up measured 0.21s median -- 25
                       # frames, no telegraph at all -- because C.spring (26)
                       # is five times C.follow (5.2) and drags the head onto
                       # a new drive almost immediately. The ramp is what makes
                       # "begins to spin ... then when it reaches full speed"
                       # a thing you watch rather than a thing you miss.
    at       = 0.97,   # release at this share of CONFIG.chain.maxAngVel
    windCap  = 4.0,    # a wind-up that cannot finish must not hang the match.
    dur      = 5.0,
    rate     = 40,     # spikes a second -- Rick's answer, off the rate ladder
    spikeDmg = 3.0,    # PLACEHOLDER
    spikeSpd = 300,    # slower than the basic shot (380): they must LIVE long
                       # enough to fill the hall or the sweep is invisible
    spikeR   = 7,
    spikeLife= 2.4,
    crowdMul = 10,     # SWEPT. The director fired 15.53x more often inside a
                       # Bloodmill window than outside one -- against
                       # Triplicate's 4.59x, which Rick had already called too
                       # much. Excluding the kill (exempt by design):
                       #   5 -> 5.18x . 7 -> 3.45x . 9 -> 2.59x
                       #   10 -> 2.16x  <- taken . 11 -> 0.86x
                       # 10 is the last value above parity: the storm can still
                       # win a cut and no longer out-bids the fight. Triplicate,
                       # which declares no crowdMul, measures 1.69x either side
                       # of this change -- v37's published number to the digit.
    chuff    = 0.23,   # seconds between the mill's wet beats. Deliberately NOT
                       # a multiple of 1/rate: phase-locked to the spikes the
                       # two would fuse into one buzz instead of reading as a
                       # turning thing throwing a spraying thing.
)

# --------------------------------------------------------------- the relic --
RELIC = '''
  /* THE BLOODSWORN FLAIL -- and the SPIKE STORM.

     The twentieth relic, the school's first heavy and its first non-blade.
     Physics are Gravemourn's and Slagheart's EXACTLY (weapon-matrix decision 1:
     type owns the physics, school owns status and palette) -- `flail_probe.py`
     measured all three at 0.151 / 0.150 / 0.152 hits/s with damage pinned and
     ultimates suppressed, which is that rule showing up as a measurement.

     hemorrhage:2, matching the school's other two. The look-first probe is why
     this needed a decision rather than a copy: hemorrhage DECAYS at dur 3.2 and
     this type contacts once every ~6.6 seconds, so the foe holds two stacks or
     more for only 41% of a fight against 52% on the twinblade and 59% on the
     greatsword. The control says it is the CLOCK and not the chain -- same
     chain, sunder at dur 5.0 holds 51% and curse at dur 99 holds 58%.

     THE ULTIMATE IS THE ANSWER TO THAT, and it was designed before the numbers
     existed. Hemorrhage caps at 4, so a spike storm does not buy DEPTH -- it
     buys UPTIME AT THE CAP, which is the one thing a chain cannot produce.

     `dmg` is a PLACEHOLDER (flail_build.TUNED_RF) and MUST be swept. */
  { id:"%ID%", name:"%NAME%", aff:"bloodsworn", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:%DMG%, spin:2.2, mode:"chain", mass:3.6,
    onHit:{ hemorrhage:2 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"spinstorm",
          spinMul:%SPINMUL%, stormMul:%STORMMUL%, ramp:%RAMP%,
          at:%AT%, windCap:%WINDCAP%,
          dur:%DUR%, rate:%RATE%,
          spikeDmg:%SPIKEDMG%, spikeSpd:%SPIKESPD%, spikeR:%SPIKER%,
          spikeLife:%SPIKELIFE%, chuff:%CHUFF%, crowdMul:%CSP%,
          tip:"Winds the head up, then throws bleeding spikes for %DUR% seconds" },
    blurb:"Pit chain and a fistful of hooks. Wind it up far enough and it throws its own teeth." },

'''

# ------------------------------------------------------------ the fire path --
FIRE = '''    /* THE SPIKE STORM does not happen here. `fireUlt` STARTS it, and what it
       starts is a wind-up whose end is a physical state of the weapon rather
       than a clock -- Reprisal's precedent ("the bow fires when its facing
       comes round"), and the reason the telegraph is free: the head visibly
       spinning up IS the charge meter, the same virtue Ward's plate brightness
       has. No second HUD element exists or is needed. */
    if (u.kind === "spinstorm"){
      f.ultSpin = { phase: "wind", t: 0, stun: 0, acc: 0, n: 0, peak: 0, chuff: 0 };
    }
'''

# ------------------------------------------------------------------ the tick --
TICK = '''
  /* ================================================== THE SPIKE STORM ==
     Two phases on one state object.

     WIND-UP. The drive multiplier is applied in tickWeapon (the chain branch
     already had the hook for Reprisal and the Crucible); all this does is
     watch. Release when the head ACTUALLY reaches `at` of CONFIG.chain
     .maxAngVel -- not when a timer says it should have.

     WHAT BREAKS IT. Rick: "Hitstun shouldnt stop the windup. but true stuns
     from ults/abilities should." That distinction is not in `f.stun` -- every
     source writes the same field -- so it is drawn at the APPLICATION SITES
     instead of by reading a timer, and there are exactly three of them:

         hex          STATUS.hex.stunFor      Spellbreaker, Axiom
         ult freeze   u.freeze                Thornwake, Rootfast
         the Harrowing's burst  u.stunBase    Lastlight

     Five relics of twenty, and the counter is therefore NAMEABLE -- a viewer
     can learn who shuts this down, which a stun budget could never have
     offered. Ordinary hitstun and the clank stun are deliberately NOT in that
     list: they still zero the chain drive, so being beaten on DELAYS the
     wind-up, and enough of it runs out `windCap`. Delay is not cancellation.

     Marking the sites rather than adding a second timer is deliberate. A
     parallel `hardStun` clock would be a second source of truth about being
     stunned and the two would drift the first time somebody added a stun.

     `windCap` is not a design knob, it is a hang guard: a cast that can never
     reach the ceiling -- stun-locked, or a future value of spinMul below the
     threshold -- must end rather than sit there for the rest of the match.

     STORM. `acc` carries the fractional remainder so the rate is exact at any
     dt and does not drift with the timestep. The emission angle is `f.headAng`
     itself, which is why the sweep can never run backwards out of the spin:
     it IS the spin. A fixed screen direction would have been wrong in half of
     all matches (`spinDir` is +1 as fighter a and -1 as fighter b) and would
     have reversed mid-fight (`spinDir` flips on clank outcomes). */
  tickSpinStorm(dt){
    if (!this.a.ultSpin && !this.b.ultSpin) return;
    const MAXV = CONFIG.chain.maxAngVel;
    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const S = f.ultSpin;
      if (!S) continue;
      const u = f.w.ult;
      S.t += dt;
      S.peak = Math.max(S.peak, Math.abs(f.headAngVel));

      if (S.phase === "wind"){
        if (f.stun > 0) S.stun += dt;        // reported, not a break condition
        /* THE HANG GUARD, and it is also a real outcome. Hitstun zeroes the
           chain drive (that behaviour predates this relic), so a caster being
           beaten on winds up slowly -- and if it is beaten on hard enough the
           head never reaches the ceiling at all. That is a legitimate way to
           lose the cast and it is announced like any other. */
        if (S.t > u.windCap){ this.breakSpin(f, "it never gets up to speed"); continue; }
        if (Math.abs(f.headAngVel) >= MAXV * u.at){
          S.phase = "storm"; S.wind = S.t; S.t = 0;
          this.shake = Math.min(38, this.shake + 10);
          SFX.play("ult", { w: "redflail-release" });
        }
        continue;
      }

      /* STORM. */
      S.acc += u.rate * dt;
      while (S.acc >= 1){
        S.acc -= 1;
        this.spawnSpike(f);
        S.n++;
      }
      /* THE MILL'S RHYTHM. Forty spikes a second cannot each have a voice --
         that is a machine gun, not a mill. One wet beat every `chuff` seconds
         is what a turning thing sounds like, and `chuff` is deliberately not a
         multiple of 1/rate: phase-locked, the two would fuse into a single
         buzz instead of reading as a turning thing throwing a spraying one. */
      S.chuff -= dt;
      if (S.chuff <= 0){
        S.chuff += u.chuff || 0.23;
        SFX.play("ult", { w: "redflail-mill", n: S.n });
      }
      if (S.t >= u.dur) f.ultSpin = null;
    }
  }

  /* THE DRIVE, RAMPED. Reprisal's `spinMul` is a step change and that is right
     for a bow, whose telegraph is the BANNER sitting on a committed point. A
     flail's telegraph is the head itself, so the head has to be seen arriving.

     Measured before this existed: with the multiplier applied as a step, the
     wind-up ran a MEDIAN OF 0.21 SECONDS -- twenty-five frames -- because
     `CONFIG.chain.spring` is 26 against `follow` 5.2, and the spring drags the
     head onto a new drive almost at once. The release condition was fine; there
     was simply nothing to watch. `ramp` is the fix and it keeps the condition
     physical rather than replacing it with a timer: the head still fires when
     it ACTUALLY reaches the ceiling, it just now takes a while to get there.

     Read from `S.t` rather than accumulated on the state, so it cannot depend
     on whether tickWeapon runs before or after tickSpinStorm in a frame. */
  ultSpinMul(f){
    const S = f.ultSpin, u = f.w.ult;
    const full = u.spinMul || 1;
    /* THE STORM IS ITS OWN NUMBER. The wind-up must reach the ceiling or the
       ultimate never fires, so `spinMul` is load-bearing there; the storm has
       no such constraint and the arm speeding up through it is a side effect
       of the hook rather than a design. `stormMul` defaults to `spinMul`, so
       omitting it reproduces the behaviour this comment is describing. */
    if (!S) return full;
    if (S.phase === "storm") return u.stormMul === undefined ? full : u.stormMul;
    return 1 + (full - 1) * Math.min(1, S.t / (u.ramp || 1));
  }

  /* THE CAST IS LOST. Called from the three true-stun sites and from the
     wind-up's own cap. The bar is already spent -- `tickCharge` zeroed it
     before `fireUlt` ran -- so this relic gets nothing for it, which is the
     whole point of a counter.

     ANNOUNCED, never silent. The Harrowing shipped with an 11.5% dud rate that
     nobody could see, and the fix that mattered was not the rate. `reason` is
     carried into the note so the two ways to lose a cast do not read as one. */
  breakSpin(f, reason){
    if (!f.ultSpin) return;
    f.ultSpin = null;
    f.ultBroke = 0.9;                       // presentation only
    this.spawnFx(f.headX, f.headY, f.aff.core, 16, 210, 0.55, 3.2);
    SFX.play("ult", { w: "redflail-break" });
    this.note(`${f.w.name} — ${reason}`);
  }

  /* A spike leaves the HEAD, travelling along the head's own bearing -- flung
     off the end of the chain, which is the picture, and radial rather than
     tangential because that is the one Rick signed off on the schematic of.

     Deliberately NOT `spawnShot`: that function needs `f.w.shot`, and this
     relic has none. A `shot` block would also make `relicShot()` advertise on
     the fight card that this weapon shoots, and it does not -- its ultimate
     does. The card must not learn to lie for the sake of reusing a function.

     `dmgMul` prices the spike against the WEAPON's damage, the same conversion
     Ironbloom's pop uses (`s.pop / Math.max(0.01, src.w.dmg)`), so `spikeDmg`
     means what it says no matter what the tuner does to `dmg`. Everything else
     -- crit, jitter, the sunder multiplier, hemorrhage, hit stop, hitstun and
     `self.hits++` for verify.py's floor -- comes free from resolveHit, which
     is what the shot path already routes through. */
  spawnSpike(f){
    const u = f.w.ult;
    if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();
    const a = f.headAng;
    const ca = Math.cos(a), sa = Math.sin(a);
    const off = (f.w.artW || 40) * 0.42;
    this.shots.push({
      own: f === this.a ? "a" : "b",
      x: f.headX + ca * off, y: f.headY + sa * off,
      x0: f.headX, y0: f.headY, spd0: f.speed, t0: this.t,
      vx: ca * u.spikeSpd, vy: sa * u.spikeSpd,
      r: u.spikeR, life: u.spikeLife, max: u.spikeLife, grav: 0,
      dmgMul: u.spikeDmg / Math.max(0.01, f.w.dmg),
      aff: f.aff, a, spike: true,
    });
  }
'''

CALL = '''    /* THE SPIKE STORM. Deliberately AFTER the charge loop that can start it
       and BEFORE tickShots, so a spike moves and resolves on the frame it is
       born exactly as an arrow does. */
    this.tickSpinStorm(dt);
'''

TEARDOWN = '''    /* The spike storm cannot outlive the match either, and for the same
       reason the shades could not: `step()` returns from the `over` branch
       before tickSpinStorm is reached, so a storm left running would sit
       frozen mid-spray through the entire verdict beat. */
    if (this.over && (this.a.ultSpin || this.b.ultSpin)){
      this.a.ultSpin = null; this.b.ultSpin = null;
    }
'''

DRAW = '''      if (s.spike){
        /* THE SPIKE IS THE BARB. Drawn through the same `_needle` the flail
           head's tips are, because this relic throws the teeth it wears --
           one LOOK, two constructions, and a viewer is meant to recognise the
           second from the first. A barb's tip is cut from the barb's own
           Bezier and a thrown spike is not, so the construction is not shared
           and should not be.

           `dim` fades the last 0.35s so a spike that runs out its life does
           not simply vanish; one that hits something is removed by tickShots
           and never reaches this. */
        const dim = clamp(s.life / 0.35, 0, 1);
        const L = s.r * 2.9, W = s.r * 0.46;
        const ca = Math.cos(s.a), sa = Math.sin(s.a);
        const AP = [s.x + ca * L, s.y + sa * L];
        const B1 = [s.x - sa * W, s.y + ca * W];
        const B2 = [s.x + sa * W, s.y - ca * W];
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 2.0);
        gh.addColorStop(0, s.aff.core + "77");
        gh.addColorStop(1, s.aff.core + "00");
        c.globalAlpha = 0.5 * dim; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * 2.0, 0, TAU); c.fill();
        c.globalAlpha = dim;
        SHAPES._needle(c, B1, AP, B2, 0.18, s.aff.core, s.aff.glow, 0.85 * dim, 0.34);
        c.globalAlpha = 1;
        continue;
      }
'''

ANCHOR_GRAVE = '        } else if (w === "gravemourn"){                 // a drop into the grave'

# --------------------------------------------------------------- the voice --
# Held as a module-level literal, like every other block in this file, because
# the first attempt built it inline through repr() and put a LITERAL backslash-n
# into the JavaScript. The page then failed to parse, `window.AC` never existed,
# and scpage's wait_for_function timed out -- which is the guard working, but a
# build should not need a guard to catch its own quoting.
SOUND = '''        } else if (w === "redflail"){                   // the mill takes hold
          /* BLOODMILL, in four voices. Rick: "something guttural and bloody".

             Guttural is not simply LOW -- a low sine is a heartbeat. What makes
             a sound guttural is BEATING: two detuned sawtooths a few hertz
             apart, whose difference frequency the ear hears as a growl rather
             than as two notes. The detune here is PROPORTIONAL, so the beat
             rate climbs with the pitch and the growl tightens into a whine as
             the head comes up to speed. That is the wind-up stated in the one
             dimension the ear reads better than the eye.

             Three stages rather than one long ramp, because `_tone`'s gain only
             ever DECAYS -- a swell has to be built out of overlapping events
             that each start louder than the last. Timed to `ult.ramp` (0.9s) so
             the sound and the picture arrive together rather than merely
             overlapping. */
          [[0.00, 46, 0.16], [0.30, 68, 0.22], [0.60, 96, 0.28]].forEach(
            ([d, f0, g0]) => {
              this._tone(t + d, { freq: f0,         to: f0 * 1.55, gain: g0,
                                  dur: 0.42, type:"sawtooth" });
              this._tone(t + d, { freq: f0 * 1.045, to: f0 * 1.62, gain: g0 * 0.85,
                                  dur: 0.42, type:"sawtooth" });
            });
          /* the wet under it. Noise through a low filter is breath and slop,
             and it is what stops the growl reading as an engine. */
          this._burst(t,        { freq: 260, q: 0.5, gain: 0.15, dur: 0.55, type:"lowpass" });
          this._burst(t + 0.48, { freq: 380, q: 0.6, gain: 0.17, dur: 0.50, type:"lowpass" });

        } else if (w === "redflail-release"){           // and it lets go
          /* The barbs tearing loose: a short wet snap high, a body under it,
             and no ring-out. This is the moment the sound stops climbing, and
             anything sustained here would blur into the mill that follows. */
          this._burst(t,        { freq: 1500, q: 2.2, gain: 0.26, dur: 0.11, type:"bandpass" });
          this._tone (t,        { freq: 150,  to: 42, gain: 0.30, dur: 0.26, type:"sawtooth" });
          this._burst(t + 0.03, { freq: 5200, q: 0.9, gain: 0.13, dur: 0.20, type:"highpass" });

        } else if (w === "redflail-mill"){              // it keeps turning
          /* Roughly four a second for five seconds, so it has to be QUIET and
             it must not be identical each time -- a repeated identical grain
             reads as a loop artefact inside about three repeats. `p.n` is the
             spike count, a real number out of the sim rather than a random one,
             so the variation is deterministic and a render is reproducible.
             `Math.random()` in a frame is a standing open decision in this
             project precisely because it blocks that.

             GAINS SET FROM THE RENDER, not from taste. At 0.085/0.075 the first
             cut normalised to the wind-up's peak and the mill was inaudible
             underneath it -- twenty-two events that may as well not have been
             written. 0.135/0.105 puts the rhythm where it can be heard without
             out-shouting the release it follows. */
          const k = (p.n || 0) % 5;
          this._burst(t, { freq: 300 + k * 46, q: 0.7, gain: 0.135,
                           dur: 0.11, type:"lowpass" });
          this._tone (t, { freq: 86 + k * 5,  to: 62, gain: 0.105,
                           dur: 0.12, type:"sawtooth" });

        } else if (w === "redflail-break"){             // the wind goes out
          /* The wind-up run backwards, and audibly so: the pitch FALLS where it
             rose, the beating slows instead of tightening, and it ends wet and
             short. A cast that died must not sound like a cast that landed
             quietly -- it should sound like something stopping. */
          this._tone (t,        { freq: 140, to: 38, gain: 0.26, dur: 0.40, type:"sawtooth" });
          this._tone (t,        { freq: 134, to: 36, gain: 0.20, dur: 0.40, type:"sawtooth" });
          this._burst(t,        { freq: 420, q: 0.5, gain: 0.16, dur: 0.36, type:"lowpass" });
          this._burst(t + 0.16, { freq: 180, q: 0.4, gain: 0.10, dur: 0.24, type:"lowpass" });

'''

EDITS = [
 ("1 ultSpin on the fighter",
  "    this.ultSplit = null;",
  "    this.ultSplit = null;\n"
  "    /* {phase,t,stun,acc,n,peak} while the head winds up and then sprays.\n"
  "       null on every other relic, which is the whole zero-burden argument. */\n"
  "    this.ultSpin = null;"),

 ("2 the chain drive hook",
  "              * (f.ultDraw || f.ultForge ? (f.w.ult.spinMul || 1) : 1);",
  "              * (f.ultDraw || f.ultForge ? (f.w.ult.spinMul || 1)\n"
  "                 : f.ultSpin ? this.ultSpinMul(f) : 1);"),

 ("3 the relic",
  '    blurb:"Two daggers, and then six. What walks out of it wears your face and keeps what it takes." },',
  '    blurb:"Two daggers, and then six. What walks out of it wears your face and keeps what it takes." },\n'
  + RELIC.rstrip("\n")),

 ("4 fireUlt starts the wind-up",
  '    if (u.kind === "volley" && f.w.shot){',
  FIRE + '    if (u.kind === "volley" && f.w.shot){'),

 ("5 tickSpinStorm + spawnSpike",
  "  fireUlt(f, foe){",
  TICK.strip("\n") + "\n\n  fireUlt(f, foe){"),

 ("6 the tick call",
  "      this.tickCharge(self, foe, dt);\n    }",
  "      this.tickCharge(self, foe, dt);\n    }\n" + CALL.rstrip("\n")),

 ("7 teardown on the over path",
  "      if (this.a.ultSplit) this.a.ultSplit = null;\n"
  "      if (this.b.ultSplit) this.b.ultSplit = null;\n"
  "      this.a.lifesteal = 0; this.b.lifesteal = 0;\n"
  "    }",
  "      if (this.a.ultSplit) this.a.ultSplit = null;\n"
  "      if (this.b.ultSplit) this.b.ultSplit = null;\n"
  "      this.a.lifesteal = 0; this.b.lifesteal = 0;\n"
  "    }\n" + TEARDOWN.rstrip("\n")),

 ("8 the spike draw",
  "      if (s.sc){",
  DRAW.rstrip("\n") + "\n      if (s.sc){"),
 ("9 true stun: hex",
  "        f.stun = Math.max(f.stun, STATUS.hex.stunFor);",
  "        f.stun = Math.max(f.stun, STATUS.hex.stunFor);\n"
  "        /* A TRUE STUN. Hex is the status whose entire job is shutting a\n"
  "           weapon down, so it is the one that should stop a weapon being\n"
  "           wound up. No-op on every relic but one. */\n"
  "        this.breakSpin(f, \"the hex takes the wind out of it\");"),

 ("10 true stun: ult freeze",
  "    if (u.freeze && inRange) foe.stun = Math.max(foe.stun, u.freeze);",
  "    if (u.freeze && inRange){\n"
  "      foe.stun = Math.max(foe.stun, u.freeze);\n"
  "      this.breakSpin(foe, \"rooted mid-wind-up\");   // a TRUE stun\n"
  "    }"),

 ("11 true stun: the Harrowing's burst",
  "      foe.takeHitstun(dmg);\n"
  "      foe.stun = Math.max(foe.stun, u.stunBase + u.stunPer * n);",
  "      foe.takeHitstun(dmg);\n"
  "      foe.stun = Math.max(foe.stun, u.stunBase + u.stunPer * n);\n"
  "      /* The burst's stun is a TRUE stun and scales with how many blades\n"
  "         were buried; the takeHitstun on the line above is NOT and is\n"
  "         deliberately left alone. */\n"
  "      this.breakSpin(foe, \"the blades burst and the wind goes out of it\");"),

 ("12 Bloodmill's voice", ANCHOR_GRAVE, SOUND + ANCHOR_GRAVE),
 ("13 the crowd flag learns about storms",
  '    o.crowd = this.shades.length > 0;',
  '    /* v38: A SPIKE STORM CROWDS THE FLOOR AND HAS NO SHADES. The line above\n       used to read `this.shades.length > 0` and its own comment said it would\n       be "False in every match without a summon in it, which until this relic\n       was all of them" -- this is the relic that comment was waiting for.\n\n       A storm is not more BODIES, it is more CONTACTS, and the director cannot\n       tell the difference: measured at 15.53x preference for the inside of a\n       Bloodmill window against Triplicate\'s 4.59x before that was fixed, with\n       78% of every cut in a fight landing inside 19% of its seconds.\n\n       `crowdVolleyMin` was swept at 8, 14, 20, 28 and 40 first and returned\n       15.53x AT EVERY VALUE, to the digit -- the same signature v37 got, and\n       the same lesson: a knob that moves nothing is not a knob that needs a\n       bigger number, it is a knob that is not connected.\n\n       ANYTHING THAT PUTS EXTRA HITS ON THE FLOOR BELONGS IN THIS LOOP.\n\n       ONE CINE-WIDE NUMBER CANNOT SERVE TWO ULTIMATES, which is v37 open\n       decision 3 coming due: \"crowdVolleyMin is a CINE-wide setting, not a\n       per-relic one ... if one arrives with a different density the sweep has\n       to be redone.\" Swept on one shared knob, the value that brings a storm\n       from 13.37x to 2.35x drags Triplicate to 1.17x -- below the 1.69x v37\n       argued for on the grounds that an ultimate SHOULD put more spectacle on\n       the floor. So `crowd` is no longer a boolean: it carries the strength\n       the crowding ultimate asks for, and each ult declares its own.\n\n       TWO FIELDS, NOT ONE. `crowd` stays a boolean because\n       `crowdVolleyMin` reads it, and folding the strength into it set\n       Triplicate\'s to 0 -- which silently reverted v37\'s fix and put it\n       back at 4.59x. A relic can want the volley rule and not the score\n       bar, and Triplicate is exactly that relic. */\n    o.crowd = false; o.crowdMul = 0;\n    /* v37 condition, verbatim. The first cut of this said\n       `shades[0].owner === f` inside the fighter loop, which looked tidier\n       and put Triplicate back to 4.59x -- its PRE-FIX number. Do not tighten\n       a condition that another relic depends on without measuring that relic. */\n    if (this.shades.length > 0){\n      o.crowd = true;\n      const ow = this.shades[0].owner;\n      o.crowdMul = Math.max(o.crowdMul, (ow && ow.w.ult.crowdMul) || 0);\n    }\n    for (const f of [this.a, this.b]){\n      if (f.ultSpin){\n        o.crowd = true;                                   // the volley rule\n        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);  // the score bar\n      }\n    }'),
 ("14 Bloodmill does not turn round", '    if (!decisive || !aWins) A.spinDir *= -1;\n    if (!decisive ||  aWins) B.spinDir *= -1;',
  '    /* BLOODMILL DOES NOT TURN ROUND. A clank flips the loser\'s spinDir --\n       and both, when it is not decisive -- so a flip mid-cast would reverse\n       the spray inside a single ultimate: the head throwing spikes one way and\n       then the other. That is the same incoherence that made a fixed screen\n       direction impossible to build against in the first place.\n       Rick: "grant immunity to losing clanks so it never reverses direction\n       while its casting".\n       IT BUYS DIRECTION, NOT SAFETY. The stun on the two lines below is\n       untouched, so losing a bind during a cast still costs exactly what it\n       costs any other relic. */\n    const spinLockA = !!A.ultSpin, spinLockB = !!B.ultSpin;\n    if ((!decisive || !aWins) && !spinLockA) A.spinDir *= -1;\n    if ((!decisive ||  aWins) && !spinLockB) B.spinDir *= -1;'),

 ("15 the crowd score floor", '  const volleys = cineVolleys(scored, CINE.volleyGap, CINE.volleyMin,\n                              CINE.crowdVolleyMin);',
  '  /* THE CROWD FLOOR -- and it is the tool v37 TRIED AND CORRECTLY ABANDONED.\n\n     Rick: "directior will probably always see this ult as a big exchange and\n     we need to tell it to only highlight big exchanges relitive to how many\n     hits this ult usually produces."\n\n     v37 built exactly this for Triplicate and it measured NOTHING, twice,\n     because a Triplicate\'s beats score IDENTICALLY to ordinary ones and are\n     merely 2.7x more frequent -- "no level can thin a population that differs\n     only in rate". A spike storm is the other case, and the difference is the\n     whole reason this line exists rather than a second copy of `crowdVolleyMin`:\n\n         crowded    mean 0.68  med 0.50  p95 2.07  | >= floor 6.29%  2.57 beats/s\n         ordinary   mean 0.53  med 0.46  p95 1.29  | >= floor 0.65%  0.80 beats/s\n\n     The storm\'s beats DO score higher and nearly TEN TIMES as many of them\n     clear the bar, so a percentile taken against the storm\'s own distribution\n     is the right instrument here and was the wrong one there. It is also why\n     `crowdVolleyMin` plateaued at 11.90x no matter how high it went: 12 of the\n     23 non-kill in-window cuts are single hits, and a grouping rule cannot\n     touch a single hit.\n\n     The kill is exempt, as it is from `crowdVolleyMin`, and for the same\n     reason -- a finish is a cut whatever else was happening. */\n  /* A MEDIAN AND A MULTIPLIER, not a percentile, and the reason is sample\n     size. A storm contributes about FOURTEEN crowded beats to a match, so a\n     p90 is the twelfth of fourteen and moves in whole-sample steps -- swept\n     as a percentile it went 13.37x -> 12.08x and stopped. A median is stable\n     at n=14 and `mul` is a smooth knob on top of it. It is also the more\n     faithful reading of the ask: \"relative to how many hits this ult usually\n     produces\" is a statement about the CENTRE of the storm\'s distribution,\n     not about its tail. */\n  const cSc = scored.filter(b => b.crowd).map(b => b.score).sort((x, y) => x - y);\n  const cMed = cSc.length ? cSc[cSc.length >> 1] : 0;\n  const crowdOK = cSc.length >= 6;\n  const volleys = cineVolleys(scored, CINE.volleyGap, CINE.volleyMin,\n                              CINE.crowdVolleyMin);'),

 ("16 the pool filter reads it", '                     .filter(x => x.score >= CINE.floor\n                               || (x.ranged && x.range >= 320\n                                   && x.score >= CINE.floor * 0.62))',
  "                     .filter(x => {\n                       /* a crowded beat clears the crowd's own bar; everything\n                          else, and every kill, clears the global floor. */\n                       /* the bar is the beat's OWN strength times the\n                          crowd's median, so two ultimates that crowd the\n                          floor differently are judged differently. */\n                       const f = (x.crowdMul && !x.fatal && crowdOK)\n                               ? Math.max(CINE.floor, cMed * x.crowdMul)\n                               : CINE.floor;\n                       return x.score >= f\n                           || (x.ranged && x.range >= 320 && x.score >= f * 0.62);\n                     })"),

 ("17 CINE.crowdScoreMul", '  crowdVolleyMin: 8,',
  '  crowdVolleyMin: 8,\n\n  /* A CROWDED beat must clear this multiple of the crowd\'s own MEDIAN\n     score. 0 disables. See cinePlan for why this exists here and did not\n     work for Triplicate. SWEPT in v38 -- the target is not 1.00x: v37 settled\n     Triplicate at 1.69x on the argument that "the ultimate does put more real\n     spectacle on the floor. What it no longer does is out-bid the rest of the\n     fight three to one." */\n  crowdScoreMul: %CSP%,'),
 ("18 a volley carries its crowd strength",
  '          crowd: run.some(b => b.crowd),',
  '          crowd: run.some(b => b.crowd),\n'
  '          /* v38: and HOW crowded. Without this a volley inside a storm\n'
  '             reaches the filter with `crowd === true`, the bar is computed\n'
  '             as median x 1 instead of median x the strength that ult asked for, and the\n'
  '             exception silently does nothing for exactly the beats it was\n'
  '             built for. */\n'
  '          crowdMul: run.reduce((a, b) => Math.max(a, b.crowdMul || 0), 0),'),
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
    ap.add_argument("--src", default="../02-chain/sc-redbarb.html")
    ap.add_argument("--out", default="../02-chain/sc-redflail.html")
    ap.add_argument("--dmg", type=float, default=TUNED_RF)
    ap.add_argument("--csp", type=float, default=10,
                    help="CINE.crowdScoreMul -- multiple of the crowd's median")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nFLAIL BUILD -- the bloodsworn flail and the spike storm")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if "_needle" not in s0:
        raise SystemExit("this source has no _needle -- run barb_build.py first")

    subs = {"%ID%": RELIC_ID, "%NAME%": RELIC_NAME, "%ULT%": ULT_NAME,
            "%DMG%": f"{A.dmg:g}", "%CSP%": f"{A.csp:g}"}
    for k, v in ULT.items():
        subs["%" + k.upper() + "%"] = f"{v:g}"

    for label, old, new in EDITS:
        for k, v in subs.items():
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print(f"\n  NEXT, and none of it is optional:")
    print(f"    python3 flail_relic_probe.py --game {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --ids <the 19>  --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
