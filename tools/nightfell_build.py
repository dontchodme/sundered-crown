#!/usr/bin/env python3
"""NIGHTFELL'S ULTIMATE -- DEADFALL. SIGILS THAT ARM AND THEN WAIT.

    python nightfell_build.py --src ../02-chain/sc-gravemourn.html \
                              --out ../02-chain/sc-nightfell.html

STAGE 3 of three (`06-docs/v51/umbral-build-brief-v51.md` §8). Built ON TOP OF
Gravemourn's stage 2, not beside it: the figures read the curse pool, and the
pool only exists because of stage 1.

## RICK'S §1, VERBATIM

    nightfell crackles with purple electricity. for the duration of the ult
    when it lands a hit the hit leaves behind an echo bomb (thinking a
    pentagram imprinted on the battlefield but open to ideas here) the echos
    slowly begin to crackle with the same purple electricity and then explode.
    dealing damage, applying curse and knocking back enemy fighters in its
    area.

## TWO OF ITS CLAUSES CHANGED AND BOTH ARE MEASUREMENTS

**"then explode" became "then ARM."** A timer catches 8-38% of its bombs and
needs a blast covering half the hall to land at all; a landmine catches 69-86%
and lets the figure be small and dense. Rick, shown the catch rates: *"thats
not what i was picturing but now that youve mentioned it thats a much better
idea."* v52 §2 and §3c.

**"applying curse" is gone, and it is worth exactly +0.0%.** v52 §3e. A charge
deals `stamp / 5` -- about 3.6 damage -- against pool entries of ~20, so the
memory it would park is displaced by curse's own top-K rule the instant it
lands. The general law, now confirmed on three separate designs:

    AN ULTIMATE CANNOT MINT A MEMORY. The pool holds the blade's biggest
    blows, so anything an ultimate APPLIES is smaller than what is already in
    there -- unless it out-hits the blade, and a thing that out-hits the blade
    is the relic.

What an ultimate CAN do is take one and give it back, or read one and copy it:

    GRAVEMOURN   MOVES the memory. A hand takes an entry, deals it, re-parks
                 it. Conserved, and the pool empties on the blow.
    NIGHTFELL    READS the memory. The figure copies the pool's SUM onto the
                 floor and spends nothing. The pool is never written to.

That is what keeps the two umbral ultimates off each other's verb, and it is
why §8.3b of the brief is a hard rule rather than a preference.

## THE POSITION IS THE MECHANIC, AND IT COSTS 12 TO 19 POINTS

Both ultimates are now "a window; each blow inside it spawns a delayed
explosive". The only structural difference is that Gravemourn's hand FLIES TO
the foe and Nightfell's imprint STAYS WHERE THE BLOW LANDED -- and that is
worth **-12.5 to -19.0 points** against the same bomb homing (v52 §1). Even at
a nova-sized 240 radius the foe is gone 41% of the time. Nightfell's ultimate
is a bet on where the fight will be; Gravemourn's is a certainty.

## DENSITY IS THE CHAIN ENGINE AND KNOCKBACK IS THE BRAKE

Rick asked whether knockback could chain one bomb into the next. Measured, it
does the opposite at every density and every radius -- 7.16 chained hits at
zero shove down to 4.04 at 850 -- because **bombs are planted where blows
land, which is a CLUSTER**, so a push ejects the ball out of the field it is
standing in rather than sweeping it through more of it. v41's warhammer
finding wearing a different hat.

**His own picture is what solves it.** A pentagram has five points, so ONE
blow stamps ONE figure of five charges on a tight ring, and the density that
makes it chain comes from inside the sigil instead of from carpeting the hall.
A trigger then sets off 4.7 of 5 charges. Five figures a fight, not
twenty-six scattered dots -- and the bet on position survives, which
carpeting would have destroyed.

**And the shove stays, on legibility.** Rick: *"i think the only thing that
passes the legibility requirement is push."* A blast that SUCKS is the class of
thing `CONFIG.arena`'s no-seek comment already forbids. It costs 23% of the
chain (12.30 -> 9.51 chained hits at push 250) and it keeps the longest run at
4.67 of 5.

## WHAT WILL BITE, AND THE FIRST ONE IS INVISIBLE TO EVERY NUMBER

**THE CHAIN MUST SPAN FRAMES.** If the detonation handler loops over every
charge in range in one frame, the whole figure goes off at once, every number
in this file still comes out right, and **there is no chain to see**. That is
this project's own defect class -- v42's silent ultimate, v43's sticking hold
-- and it is the reason `tickDeadfall` fires AT MOST ONE CHARGE PER FRAME, the
nearest one, and lets the shove carry the ball into the next.

This is the one place the build deliberately departs from `bomb_lab.py`, which
loops. At dt = 1/120 a five-charge figure takes 42ms to come apart, so the
picture is still a crackle rather than a stutter, and every detonation now has
the previous one's shove already applied to the ball.

**FOE ONLY, and it is structural rather than a guard.** The charges are
planted where blows land, which is exactly where the caster is standing, so a
caster-triggering figure eats 48% of its own charges (v52 §3c) -- and these
balls cannot steer, so "do not walk into your own minefield" is not a thing a
fighter can do. `tickDeadfall`'s proximity test only ever reads the foe's
position; there is no `if` to get wrong.

**LIVE CHARGES ARE PER-MATCH STATE.** `m.sigils`, discarded with the match,
never on `w`. It declines at a ceiling and counts the refusal; it never shifts
a live one out, which is what `spawnShot` would have done.

**NOTHING EXPIRES.** A charge that is not walked into is not a miss, it is a
charge still waiting -- worth +6.4 points over a 2s life and, more to the
point, one sentence instead of a number and a fade. The hall accumulates: an
earlier cast's figures are still live when the next lands.

## NOTHING HERE IS A PLACEHOLDER ANY MORE

The art and the sound are Rick's, over three rounds of one rendered clip
each, and every round moved something no probe in this repo had a number for:

    round 1   "i can tell the difference between armed and arming pretty
               easily" -- so the four separations stay exactly as they are
    round 2   "my vision was the pentagram was 1 large mine not a cluster of
               small ones" -- the mechanic, and it cost the chain
    round 3   "lets make the explosion sound effect bigger", and "ive also
               seen some mines explode and then disappear and some explode
               and stick around" -- the blast, which was frozen on the floor
               96.2% of the time behind sixteen green checks

§8.4's check 10 -- can a viewer tell an ARMED sigil from an ARMING one -- was
never answerable here and never will be. It is a filmstrip question and a
person is the gate.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "nightfell"

# --- the numbers, and every one of them is `echoes-v52.md`'s -----------------
ULT = {
    "dur":       8.0,    # the window. 4s -> 16s is 16.4 points and it trades
                         # against the blade; 8s is what stage 3b prices
    "points":    5,      # A PENTAGRAM HAS FIVE POINTS. THIS IS A DRAWING
                         # NUMBER AND NOT A COUNT OF BOMBS -- one figure is
                         # one mine, `drawSigils` strokes the star through
                         # these, and the single hit test is the centre at
                         # `rad`. v52 §3b measured the five-point ring as the
                         # only arrangement that chains WITHIN a figure, and
                         # Rick took the legible explosion over that chain.
                         # What is left is figure-to-figure.
    "ring":      60.0,   # the figure's DRAWN radius -- about 120 units
                         # across, three and a half ball radii
    "rad":       110.0,  # THE MINE'S TRIGGER RADIUS, AND THE WHOLE FIGURE IS
                         # ONE MINE. Rick, off the first build: "my vision was
                         # the pentagram was 1 large mine not a cluster of
                         # small ones." It covers the drawn figure -- the
                         # points sit at `ring` -- and a little beyond, so the
                         # lit ground and the star agree. On the mine reading
                         # v52 §2 measured radius 60 to 240 all landing within
                         # noise on win rate, because the foe walks in
                         # eventually whatever the size: this is a PICTURE
                         # knob and it is set to fit the picture.
    "arm":       1.6,    # crackle, then live. The fuse was measured free at
                         # 0.8 / 1.6 / 2.6 -- the foe escapes within the
                         # shortest one tested or not at all -- so this is
                         # chosen for how it looks
    "stampmul":  0.3,    # THE COPY. The mine deals `poolSum * M`, ONCE, as
                         # one number. Under five charges each dealt a fifth
                         # of this, so a fully-consumed figure delivered the
                         # same total -- the starting point is unchanged and
                         # only the shape of the delivery moved. BISECT.
    "push":      250.0,  # RICK'S, on legibility. 0 chains best and cannot be
                         # read; 800 keeps half the chain; 250 keeps 77%
}
# RICK'S, from a second spread -- the first was four ecclesiastical-Latinate
# names (Interdict, Anathema, Fulmination, Malefice) and he rejected the
# register whole, as he did for Vesper. A deadfall is a trap rigged to drop on
# whatever disturbs it: it SPRINGS rather than fires, which is the
# timer-to-mine decision in one word. Gravemourn's is REVENANT -- one
# Anglo-Saxon, one Latinate, so the school's two ultimates do not read as a
# matched pair.
ULT_NAME = "Deadfall"
ULT_TIP = "Stamps sigils that arm, then take whatever walks in"   # 51/72

# --- STAGE 3b. THE BLADE, RE-SWEPT WITH DEADFALL IN PLACE -------------------
# `umbral_sweep.py --relics nightfell --lo 8 --hi 22`, 9750 fights, RUN TWICE:
# once on the five-charge build and again after Rick made the figure one mine.
#
#   15.83  what it shipped with, under the dead curse AND a dead Eclipse
#   12.79  five charges on a ring, each dealing a fifth of the stamp
#   12.27  HERE. ONE MINE at radius 110 rather than five at 70, which catches
#          91% of what is planted against 89% and covers more ground for it.
#          Half a damage point, and the shape of the delivery is the whole
#          reason the number moved.
#
# THE BUILD BRIEF PREDICTED "~13" BEFORE ANY OF THIS EXISTED (v51 §8.2), and
# both cuts landed inside half a point of it. That is the second registered
# prediction in two stages to come in — Gravemourn's "~22-23" measured 24.03.
#
# AND THIS CURVE DOES NOT BEND, WHICH IS NOT WHAT THE SCHOOL DID LAST TIME.
# Gravemourn reads 67.3% at 47.2 and 60.6% at 52.0 — more blade, worse relic,
# because a bigger blow throws the quarry out of reach of a weapon that lands
# 5.6 times a fight. Nightfell is monotone and steep over its whole range:
#
#    8.00  14.1%      14.00  61.1%      20.00  84.1%
#   10.00  33.9%      16.00  71.7%      22.00  89.0%
#   12.00  48.4%      18.00  76.9%
#
# A greatsword is reach-poor and contact-rich, so its knockback never gets far
# enough ahead of its own swing to cost it a blow. The sweep was still run
# wide first, because a bisection cannot tell you which of those two shapes
# you are standing on.
#
# THE CONFIRMATION IS MONOTONIC THIS TIME, AND IT WAS NOT BEFORE. Pass 3 at
# n=1040 a point reads 11.64 -> 44.3%, 12.14 -> 48.9%, 12.64 -> 53.1%, where
# the five-charge build gave 50.1 / 49.7 / 57.0 and the tool said out loud
# that it had landed in its own noise. One number a figure is a quieter
# instrument than five, which is worth knowing beyond this relic.
#
# WHAT THE CUT BUYS, and unlike Gravemourn's it does not gut the relic: at
# 12.27 the echo is 14.3% of everything Nightfell delivers, the pool means 48
# and peaks at 130, and it is UP 90% of the fight and FULL 68%. 477 of 915
# blows land on a pool with something in it — which is the number DEADFALL
# actually spends, because a figure stamped on an empty pool is a decoration.
BLADE_IN = 15.83      # what `sc-gravemourn.html` carries
TUNED_NF3 = 12.27


EDITS = [

# --------------------------------------------------- 1. the window's home
("Fighter.ultDeadfall", '''    this.ultWinnow = null;''',
 '''    this.ultWinnow = null;
    /* {t, dur, blows, figures, refused, sprung} while DEADFALL's
       window is open. null on every other relic and on this one outside its
       own window, which is the whole zero-burden argument: `tickDeadfall`
       returns after a two-iteration loop that does nothing and a length test
       on an empty array, and the one branch in `resolveHit` is a truthiness
       test on a field no other relic carries. */
    this.ultDeadfall = null;
    /* AND THE CRACKLE'S OWN FADE, because the window closing is not the same
       event as the picture of it ending. Same shape as `winnowFade`, one
       relic along. It is on the FIGHTER and not on `m.ultFx` for a measured
       reason -- see `drawCrackle`. */
    this.deadfallFade = 0;'''),

# ------------------------------------------------------ 2. the figures' home
("Match.sigils", '''    this.hands = [];''',
 '''    this.hands = [];
    /* THE SIGILS, AND THEY ARE PER-MATCH STATE ON THE MATCH. Not on `w`,
       which outlives the fight -- that is CLAUDE.md §4.1's hazard and the
       brief names it again at §8.3d -- and not in `shots`, whose `maxLive`
       ceiling makes `spawnShot` SHIFT THE OLDEST LIVE ONE OUT. A mine that
       vanishes off the floor with no error, no invariant broken and no win
       rate moved is this project's own defect class for the fourth time.
       This list declines at its ceiling and counts the refusal.

       NOTHING IN IT EVER EXPIRES. A mine that is not walked into is not a
       miss, it is a mine still waiting -- worth +6.4 points over a 2s life
       (v52 §3d) and, more to the point, ONE SENTENCE: the sigil stays until
       something sets it off. So the hall accumulates, and the floor gets more
       dangerous as the fight goes on, for free. */
    this.sigils = [];
    /* AND THE BLAST THEY LEAVE. Presentation only, beside `rings` and
       `floats`. A mine that simply vanished on the frame it fired was
       the whole of Rick's complaint about the first build, so a figure
       leaves by BECOMING the explosion. Nothing in the simulation
       reads it. */
    this.sigilFlash = [];'''),

# ------------------------------------------------------------- 3. the cast
("fireUlt.sigil", '''    if (u.kind === "sling"){''',
 '''    if (u.kind === "sigil"){
      /* NOTHING RESOLVES HERE, and `u.dmg` is 0. The cast opens a window and
         crackles; what the ultimate IS happens on the blows landed inside it
         and on the floor those blows leave behind.

         NOT `nova`. Eclipse was one -- 11 damage in a 250 ring -- and it is
         gone with the art that drew it: an occulted body over the caster is a
         picture of an eclipse and this relic no longer casts one. */
      f.ultDeadfall = { t: 0, dur: u.dur, blows: 0, figures: 0,
                        refused: 0, sprung: 0 };
      /* The fx clock runs at 2x sim time -- `decay()` calls
         `tickPresentation` once directly and once through `decayImpactOnly` --
         so every `life` in this engine is in half-seconds. The crackle has to
         still be on the caster for the whole window, the way Aegis, the
         Thicket, the ballista, the Stasis Field, the Winnowing and the
         Sentinel are; the map entry in the table above is the fallback if
         this line is ever missed. */
      this.ultFx.life = (u.dur + 0.7) * 2;
      return;
    }

    if (u.kind === "sling"){'''),

# ------------------------------- 4. the blows inside the window stamp a figure
("resolveHit.sigil", '''      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);
    }''',
 '''      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);
    }

    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit
       the hit leaves behind an echo bomb ... a pentagram imprinted on the
       battlefield."

       IT IS STAMPED WITH WHAT CURSE REMEMBERS AT THIS INSTANT, and that is
       the whole of why the ultimate is worth anything: a mine carrying a
       share of a 60-point pool is a mine worth walking round, and one dealing
       a flat 10 is not (v52 §3, +0.0% for the flat version).

       THIS SITS AFTER THE `onHit` LOOP ON PURPOSE, so the blow that stamps
       the figure is one of the blows the figure remembers -- the same reading
       Gravemourn's hands take, arriving from the other side.

       AND IT IS READ-ONLY ON THE POOL. `curseSum()` and nothing else: no
       push, no spend, no `apply`. Gravemourn MOVES a memory; this COPIES one.
       A build that re-applies curse from a mine recreates the dead clause
       v52 §3e deleted, and it would also hand this relic Gravemourn's verb. */
    if (mul === undefined && self.ultDeadfall && foe.alive && !foe.shade
        && !this.over && (self === this.a || self === this.b)){
      const D = self.ultDeadfall, U = self.w.ult;
      D.blows++;
      /* THE CEILING, DECLINED AND COUNTED. Never shift a live figure out. */
      if (this.sigils.length >= 24){ D.refused++; }
      else {
        const N = U.points | 0;
        const A2 = CONFIG.arena, ins = this.inset + 10;
        /* THE WHOLE FIGURE IS NUDGED TO FIT IN THE HALL. Blows land on the
           walls constantly, and half a pentagram off the edge of the frame is
           a picture fault with no number attached to it. The centre moves;
           the figure stays a figure. (Only at the stamp. The walls close
           during a fight, so a mine planted early can end up behind one, and
           that is the hall taking it rather than a bug.) */
        const cx = clamp(hx, ins + U.ring, A2.w - ins - U.ring);
        const cy = clamp(hy, ins + U.ring, A2.h - ins - U.ring);
        /* THE MINE'S WHOLE PAYLOAD, IN ONE NUMBER. The first build split
           this `stamp / points` five ways, and five three-damage numbers went
           up over the ball inside 42 milliseconds. Rick: "what isnt legible
           is the explosion itself ... my vision was the pentagram was 1 large
           mine not a cluster of small ones." A figure walked all the way
           through delivered exactly this much before; it just delivers it at
           once now, as one blast and one number. */
        const stamp = foe.curseSum() * U.stampMul;
        /* THE FIGURE'S ROTATION IS A PURE FUNCTION OF WHICH FIGURE IT IS. No
           `rng()` draw: a sigil's whole geometry follows from where the blow
           landed and how many have been stamped, which keeps the ultimate
           reproducible without spending from the fight's own stream. */
        const rot = (D.figures % N) * (TAU / (N * N));
        /* THE POINTS ARE A DRAWING AND NOT A LIST OF BOMBS. `drawSigils`
           strokes the star through them; nothing is ever tested against them.
           The one hit test in this relic is the CENTRE at `rad`. */
        const pts = [];
        for (let i = 0; i < N; i++){
          const a2 = rot - Math.PI / 2 + i * TAU / N;
          pts.push({ x: cx + Math.cos(a2) * U.ring,
                     y: cy + Math.sin(a2) * U.ring });
        }
        this.sigils.push({ src: self === this.a ? "a" : "b",
                           x: cx, y: cy, t: 0, arm: U.arm,
                           ring: U.ring, rad: U.rad, stamp, mem: stamp,
                           seed: D.figures + 1, pts });
        D.figures++;
        SFX.play("ult", { w: "nightfell-stamp" });
      }
    }'''),

# ------------------------------- 5b. THE BLAST IS ON THE PRESENTATION CLOCK
# RICK FOUND THIS BY WATCHING: "ive also seen some mines explode and then
# disappear and some explode and stick around."
#
# The blast was aged in `tickDeadfall`, which is on the normal step path -- and
# a detonation is an IMPACT. It sets `hitStop`, and `step()` returns through
# `decayImpactOnly` for as long as that runs, so the figure froze for exactly
# the frames a viewer is staring hardest at. `tickPresentation`'s own comment
# about status tags says this sentence already, one object along.
#
# The first cut was worse: it also sat below `if (!this.sigils.length)
# return;`, and a mine is spliced out of `sigils` the instant it fires, so when
# it was the last one on the floor the flash stopped dead until something
# stamped the next figure. Measured over 36 fights: 178 of 185 detonations --
# 96.2% -- left a figure frozen mid-expansion, worst 31.67 SECONDS against a
# 0.42s life.
#
# NOTHING IN THIS REPO COULD SEE IT. The sim is untouched, `engine_ab` is
# bit-identical, no win rate moves, and the relic probe's own check asked
# whether more than EIGHT flashes were held at the end of a fight -- a
# hoarding check, and this was one object standing still.
("flash.presentation", '''    if (this.wallCrack){
      this.wallCrack.t += dt;
      if (this.wallCrack.t > this.wallCrack.life) this.wallCrack = null;
    }''',
 '''    if (this.wallCrack){
      this.wallCrack.t += dt;
      if (this.wallCrack.t > this.wallCrack.life) this.wallCrack = null;
    }
    /* THE DEADFALL'S BLAST, HERE FOR EXACTLY THE REASON THE PARAGRAPH BELOW
       ALREADY GIVES FOR STATUS TAGS: it is spawned by an impact, and every
       impact begins with a hit stop that runs `decayImpactOnly`. Ticked on
       the normal path only, it freezes for the frames the viewer is staring
       hardest at — which is what Rick saw ("some explode and stick around")
       and what 96.2% of detonations were doing.

       `life` IS IN HALF-SECONDS, like every other `life` in this engine: this
       clock is called once directly and once through `decayImpactOnly`, so it
       runs at 2x sim time. */
    for (let i = this.sigilFlash.length - 1; i >= 0; i--){
      const b = this.sigilFlash[i];
      b.t += dt;
      if (b.t >= b.life) this.sigilFlash.splice(i, 1);
    }'''),

# ------------------------------------------- 5. the window, and the floor
("tickDeadfall", '''  tickSling(dt){''',
 '''  /* THE WINDOW, AND EVERY MINE STANDING ON THE FLOOR.

     They are ticked together because a figure outlives the window that
     stamped it -- permanently -- so this function is mostly about objects
     whose author's window closed long ago. Same shape as the ballista's
     bolts, the Thicket's seeds, the Winnowing's kunai and Grasp's hands: a
     COMMITTED OBJECT is not deleted because a clock ran out. */
  tickDeadfall(dt){
    for (const f of [this.a, this.b]){
      const D = f.ultDeadfall;
      if (!D) continue;
      D.t += dt;
      /* Two ways out and both are here: the clock and the corpse. Nothing is
         restored, because the window writes nothing -- unlike Grasp's, which
         has a `reachMul` to put back. */
      if (D.t >= D.dur || !f.alive) f.ultDeadfall = null;
    }
    /* THE PICTURE'S CLOCK, ON THE FIGHTER. Up instantly, down over 0.45s, so
       the electricity guts out rather than being cut. */
    for (const f of [this.a, this.b])
      f.deadfallFade = f.ultDeadfall ? 1
                     : Math.max(0, f.deadfallFade - dt / 0.45);

    /* THE BLAST IS NOT AGED HERE. It is presentation and it is spawned by
       an impact, so it belongs on the presentation clock -- `tickPresentation`
       carries it, and the reason is written out there. */
    if (!this.sigils.length) return;
    for (const g of this.sigils){
      const was = g.t;
      g.t += dt;
      /* THE SNAP. One sound per FIGURE at the instant it goes live, not one
         per mine — which is the same thing now that a figure is one mine,
         and was not when it was five: five simultaneous copies of one voice
         is a click, not a chord. The state change is a property of the
         figure, so the sound is too. */
      if (was < g.arm && g.t >= g.arm) SFX.play("ult", { w: "nightfell-arm" });
    }
    if (this.over) return;

    /* ---- AT MOST ONE MINE A FRAME, AND IT IS THE NEAREST ONE -----------

       §8.3a of the build brief. The chain that is left after Rick took the
       single large mine is FIGURE TO FIGURE -- the shove out of one blast
       carrying the ball into the next mine standing on the floor -- and it
       is a chain a viewer can actually follow, because every link is a
       whole explosion rather than a fifth of one.

       It only exists if the frames are separate. If this fired every
       figure in range in one step, the damage, the win rate, the chain
       counters and the beats would all still be right and THERE WOULD BE
       NO CHAIN TO SEE. v42 shipped a silent ultimate and v43 a hold that
       stuck to the ball it froze; both were caught by Rick watching, and
       both produced identical numbers either way. Firing one and
       returning means the shove below has landed before the next test
       runs, so the ball is genuinely carried from mine to mine.

       AND THE TEST ONLY EVER READS THE FOE. There is no caster branch to get
       wrong: a figure is planted where a blow landed, which is exactly where
       its own caster is standing, so a caster-triggering mine is not a
       tuning knob but 48% of the ultimate eating itself (v52 §3c) -- and
       these balls cannot steer, so nothing could avoid it. */
    let hitG = null, best = Infinity, at = -1;
    for (let i = 0; i < this.sigils.length; i++){
      const g2 = this.sigils[i];
      if (g2.t < g2.arm) continue;                  // still crackling
      const foe2 = g2.src === "a" ? this.b : this.a;
      if (!foe2.alive) continue;
      /* ONE TEST PER FIGURE, AT ITS CENTRE. The five points are a DRAWING --
         Rick, off the first build: "my vision was the pentagram was 1 large
         mine not a cluster of small ones." */
      const d = Math.hypot(foe2.x - g2.x, foe2.y - g2.y);
      if (d <= g2.rad && d < best){ best = d; hitG = g2; at = i; }
    }
    if (!hitG) return;

    const g = hitG;
    const own = g.src === "a" ? this.a : this.b;
    const foe = g.src === "a" ? this.b : this.a;
    this.sigils.splice(at, 1);
    /* AND IT LEAVES BY BECOMING THE EXPLOSION. The figure is handed to the
       renderer to expand, whiten and burn out; a mine that simply disappeared
       on the frame it fired is the thing Rick could not read. */
    this.sigilFlash.push({ x: g.x, y: g.y, ring: g.ring, rad: g.rad,
                           pts: g.pts, t: 0, life: 0.84 });   // 0.42s at 2x
    /* IT DEALS ITS SHARE OF WHAT THE FIGURE REMEMBERED, and it deals it as an
       integer, because every damage number in this engine is one and this one
       gets printed over a ball. */
    const dmg = Math.round(g.mem * foe.dmgTakenMul());
    if (dmg > 0){
      this.hurt(foe, dmg, own);
      own.dealt += dmg;
      /* `hits` is deliberately NOT incremented: a mine does not go through
         `resolveHit`, and verify's "no pairing resolves on fewer than 6 hits"
         floor is about BLOWS LANDED, which this is not. */
      foe.flash = 1; foe.ringFlash = 1;
      this.float(foe.x, foe.y - 40, dmg, AFFINITIES.umbral.glow, 34 + dmg * 0.5);
    }
    /* NO CURSE. v52 §3e's "1 charge, stamp x0.3" row is this configuration
       exactly — one payment a figure at a third of the pool — and it measured
       the clause at +0.4%, one standard error from nothing. The pool holds
       the blade's three biggest blows and curse's own top-K rule displaces
       anything smaller the instant it is parked. The figure READS the pool
       and never writes to it. */

    /* THE SHOVE, RADIALLY OUTWARD FROM THE MINE. Rick took push over pull
       on legibility -- a blast that SUCKS is the class of thing
       `CONFIG.arena`'s no-seek comment forbids, because the viewer cannot see
       the force and it reads as the physics lying. It costs 23% of the chain
       and it is what carries the ball into the next mine. */
    const dx = foe.x - g.x, dy = foe.y - g.y, dl = Math.hypot(dx, dy) || 1;
    const P = own.w.ult.push;
    foe.vx += (dx / dl) * P; foe.vy += (dy / dl) * P;

    const fatal = !foe.alive;
    if (fatal){
      /* A MINE THAT ENDS THE FIGHT CARRIES THE FIGHT'S OWN WEIGHT.
         `resolveHit` swaps its hit-stop for `killStop` and arms `finisher` on
         a fatal blow; anything landing outside that function has to do it
         itself or this ultimate's killing blow is lighter than a swing. */
      this.hitStop = Math.max(this.hitStop, CONFIG.impact.killStop);
      this.finisher = 1.0;
    } else {
      /* AND IT LANDS LIKE ONE THING, because it is one thing. The first build
         gave this 0.02 because five could fall inside 42ms and a hit-stop
         each would have frozen the hall for a quarter of a second. One mine
         a figure gets a real one. */
      this.hitStop = Math.max(this.hitStop, 0.05);
    }
    this.shake = Math.min(38, this.shake + (fatal ? 22 : 13));
    this.spawnFx(g.x, g.y, AFFINITIES.umbral.core, 34, 300, 0.7, 5);
    this.ring(g.x, g.y, AFFINITIES.umbral.glow, 7, g.rad, 0.42, 6);
    SFX.play("ult", { w: "nightfell-boom" });
    /* RULE 3, EIGHTH RELIC RUNNING. A mine goes off on the floor through
       its own path, so nothing else in the frame knows it happened and
       `cinePlan` would score the best moment of this ultimate as empty air. */
    this.beat({ kind: "ult", side: own === this.a ? 0 : 1,
                x: g.x, y: g.y, w: own.w.id,
                foeHpFrac: foe.hp / foe.maxHp });
    /* AND THE FATAL ONE IS FILED AS A HIT, WHICH IS A SECOND BEAT ON PURPOSE.
       `cinema_clip` finds the killing blow with `plan.find(c => c.fatal)` and
       NOTHING on an `ult` beat carries that flag. Measured on Gravemourn
       before the same line existed there: 30 of 58 kills were landed by a
       hand and ALL THIRTY rendered a clip with no killing blow. The brief
       registered this for these mines in advance (§8.3, open item 20) --
       they detonate outside `resolveHit` exactly as the hands do. */
    if (fatal)
      this.beat({ kind: "hit", side: own === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, dmg, crit: false, fatal: true,
                  hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                  selfHpFrac: own.hp / own.maxHp,
                  spd: own.speed, foeSpd: foe.speed,
                  close: Math.hypot(own.vx - foe.vx, own.vy - foe.vy) });
    if (own.ultDeadfall) own.ultDeadfall.sprung++;
  }

  tickSling(dt){'''),

("step.tickDeadfall", '''    this.tickWinnow(dt);
    this.tickSling(dt);''',
 '''    this.tickWinnow(dt);
    this.tickSling(dt);
    this.tickDeadfall(dt);'''),

# --------------------------------------------------------- 6. the picture
("drawSigils", '''  drawShots(m){''',
 (HERE / "nightfell_sigils.js").read_text(encoding="utf-8")
 + "  drawShots(m){"),

("draw.sigils", '''    this.drawMotes(m);
    this.drawUltUnder(m);''',
 '''    this.drawMotes(m);
    /* UNDER the set-pieces and under both balls: the sigils are ON THE FLOOR,
       and a figure drawn over the fighter standing in it would say the
       opposite of what the mechanic does. */
    this.drawSigils(m);
    this.drawCrackle(m, false);
    this.drawUltUnder(m);'''),

("draw.crackleOver", '''    this.drawSparks(m);''',
 '''    this.drawSparks(m);
    /* OVER both balls and under the HUD: the electricity is ON the shell. */
    this.drawCrackle(m, true);'''),

# ----------------------------------------- 7. the cast art, under and over
("art.under", '''    /* ---- Eclipse: the floor goes out, in a ring running outward ------------ */
    else if (u.w === "nightfell"){
      const ex = clamp(u.t / 0.44, 0, 1);
      const fade = 1 - clamp((u.t - 0.55) / 0.9, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      c.globalAlpha = 0.9 * fade;
      const g = c.createRadialGradient(u.x, u.y, R * 0.05, u.x, u.y, Math.max(1, R));
      g.addColorStop(0, "#05010AEE"); g.addColorStop(0.72, "#12042099");
      g.addColorStop(0.94, "#2A0A4066"); g.addColorStop(1, "#2A0A4000");
      c.fillStyle = g;
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.fill();
    }''',
 '''    /* ---- ECLIPSE'S FLOOR RING IS RETIRED WITH ECLIPSE, and DEADFALL'S
       window art does not live here.

       `ultFx` IS ONE SLOT ON THE MATCH, so the opponent casting anything
       overwrites it and that cast's own `life` then nulls it. Counting frames
       in which Nightfell's window was open, over four seeds an opponent:
       ironhail 0.0% still showed this relic's fx, bulwarden 20.8%, twinshade
       47.6%, grudgebearer 57.5%, axiom 97.9%, emberedge 99.1%. An eight-second
       window whose only signal is on `ultFx` is INVISIBLE for most of itself
       against half the roster -- and the sim is untouched, so no probe, no
       sweep and no win rate can see it.

       So the crackle and the ground under it are `drawCrackle`, off
       `f.ultDeadfall` and `f.deadfallFade`, which belong to the fighter.
       What still rides on `ultFx` is the one-shot particle burst at the cast,
       which is an EVENT and is allowed to be lost to a later one. */'''),

# ------------------------------- 7b. THE PARTICLE FIELD IS ON THE WRONG BALL
# CAUGHT ON THE FIRST RENDERED FRAME AND BY NOTHING ELSE, which is §4.1 again.
# `drawUltOver` ends with
#
#     const at = F.spec.mode === "burst" ? [u.tx, u.ty] : [u.x, u.y];
#
# so a `burst` field is drawn at the FOE'S position at the cast. That is right
# for the four novas that rule was written for -- they are cast AT somebody --
# and it put 1400 purple particles over the quarry on a cast that resolves
# NOTHING. The picture said the ultimate landed on them; the sim said nobody
# was touched. No probe, no sweep and no win rate can see that.
#
# The flag goes on the SPEC rather than a relic name in the glue, because
# "this field belongs to its caster" is a property of the field.
("fx.spec", '''    /* ECLIPSE, the one nova that should read as dark: slower and longer, and
       the school's own colours do the rest. */
    nightfell: { mode: 'burst', n: 1400, sp: [150, 480], grav: 60, drag: 2.3,
                 life: [0.45, 1.05], heavy: 0.02, size: [0.8, 2.4],
                 spawn: 0.08, up: 0 },''',
 '''    /* DEADFALL DISCHARGES, AND `atSelf` IS A FLAG NO OTHER SPEC CARRIES.
       A `burst` is drawn at the FOE -- right for the four novas above it,
       which are cast AT somebody, and wrong for a window that opens on its
       own caster. Eclipse was a nova and this entry was its dark, slow one;
       DEADFALL resolves nothing at the cast, so 1400 particles over the
       quarry would say the ultimate landed on them while nothing landed on
       anyone. It is now SPARKS COMING OFF THE BALL: fast out, almost no
       gravity, heavy drag and a short life, so they leave rather than fall,
       and they are gone before the first figure has finished arming. */
    nightfell: { mode: 'burst', n: 1100, sp: [200, 700], grav: 40, drag: 3.2,
                 life: [0.22, 0.60], heavy: 0.0, size: [0.6, 1.8],
                 spawn: 0.10, up: 0, atSelf: 1 },'''),

("fx.anchor", '''        const at = F.spec && F.spec.mode === "burst" ? [u.tx, u.ty]
                                                     : [u.x, u.y];''',
 '''        /* A BURST GOES WHERE IT WAS THROWN, AND `atSelf` SAYS WHO THREW IT.
           Four novas are cast AT somebody and their field belongs over the
           quarry. A window that opens on its own caster is not, and drawing
           its field on the foe says an ultimate landed on them when nothing
           resolved at all. */
        const at = F.spec && F.spec.mode === "burst" && !F.spec.atSelf
          ? [u.tx, u.ty] : [u.x, u.y];'''),

# ------------------------------------------------------------ 8. the sound
("sfx.nightfell", '''          this._tone (t + 0.05, { freq: 340, to: 96, gain: 0.13, dur: 0.42, type:"triangle" });
        } else {                                        // rune-crack''',
 '''          this._tone (t + 0.05, { freq: 340, to: 96, gain: 0.13, dur: 0.42, type:"triangle" });
        } else if (w === "nightfell"){          // the charge comes up
          /* THE CAST IS A WINDOW OPENING, so like Grasp's it does not
             resolve: a rising electrical whine with a body under it, and the
             sparks that answer it are the three voices below. */
          this._tone (t, { freq: 70, to: 150, gain: 0.26, dur: 0.95, type:"sawtooth" });
          this._tone (t + 0.03, { freq: 620, to: 1500, gain: 0.11, dur: 0.75, type:"square" });
          [0, 0.09, 0.17, 0.26, 0.36, 0.47].forEach((d, i) =>
            this._burst(t + d, { freq: 2600 + i * 420, q: 2.0,
                                 gain: 0.10 - i * 0.011, dur: 0.05,
                                 type:"bandpass" }));
        } else if (w === "nightfell-stamp"){    // a figure hits the floor
          /* SHORT AND LOW. It rides UNDER the blow that stamped it -- a blow
             already has a voice, and a second loud thing on the same frame
             just makes the first one muddy. */
          this._burst(t, { freq: 340, q: 0.7, gain: 0.15, dur: 0.16, type:"lowpass" });
          this._tone (t, { freq: 240, to: 70, gain: 0.12, dur: 0.22, type:"triangle" });
        } else if (w === "nightfell-arm"){      // and it goes live
          /* THE ONE SOUND THAT HAS A JOB. The armed state is invisible if the
             viewer is watching the balls instead of the floor, so this is the
             only cue that reaches them either way: a bright upward snap, one
             per figure, nothing like the stamp that preceded it and nothing
             like the detonation that follows it. */
          this._tone (t, { freq: 900, to: 1900, gain: 0.13, dur: 0.14, type:"square" });
          this._burst(t + 0.01, { freq: 4200, q: 1.6, gain: 0.11, dur: 0.07, type:"bandpass" });
        } else if (w === "nightfell-boom"){     // something walked in
          /* THE BIGGEST THING THIS RELIC DOES, and it took two cuts to get
             here. The first was a short bright CRACK on purpose: five charges
             could land inside 42 milliseconds and five thuds would have been
             mud. Rick took the single large mine and then asked for this --
             "lets make the explosion sound effect bigger" -- and the reason
             the crack existed went with the five charges.

             Built as a real blast in four parts: a SUB that drops away under
             everything, a BODY of low noise, a CRACK on top so it cuts
             through the hit-stop, and DEBRIS -- three short bandpassed hits
             under the tail, which is the pentagram coming apart.

             NO BURST IS LONGER THAN 0.6s. CLAUDE.md §4.5: `_burst` does not
             loop its 0.6s noise buffer, so anything longer plays silence for
             its tail, and this is exactly the voice that would want one. */
          this._tone (t, { freq: 190, to: 30, gain: 0.40, dur: 0.62, type:"sine" });
          this._burst(t, { freq: 150, q: 0.5, gain: 0.42, dur: 0.55, type:"lowpass" });
          this._burst(t, { freq: 5200, q: 0.9, gain: 0.26, dur: 0.09, type:"highpass" });
          this._tone (t + 0.01, { freq: 520, to: 70, gain: 0.26, dur: 0.34, type:"sawtooth" });
          [0.07, 0.15, 0.26].forEach((d, i) =>
            this._burst(t + d, { freq: 2600 - i * 700, q: 1.3,
                                 gain: 0.13 - i * 0.03, dur: 0.10,
                                 type:"bandpass" }));
          this._burst(t + 0.10, { freq: 320, q: 0.4, gain: 0.18, dur: 0.55, type:"lowpass" });
        } else {                                        // rune-crack'''),

# ------------------------------------------------------ 9. the relic's data
("ult.eclipse", '''    /* `apply:{curse:3}` is GONE, same reason as Dirge's and worth +7.2
       against a field median of +20.4. Stage 3 replaces the payload. Name and
       tip are PLACEHOLDERS and are Rick's. */
    ult:{ name:"Eclipse", charge:15, kind:"nova", radius:250, dmg:11,
          knock:150, tip:"Nova: deals 11 damage — knocks back" },''',
 '''    /* DEADFALL. The window is the ultimate and the FLOOR is the payload:
       every blow landed inside `dur` stamps ONE PENTAGRAM where the blow
       landed, carrying what Curse remembers about the quarry AT THAT INSTANT.
       It crackles for `arm` seconds, goes live, and then waits — permanently
       — for the foe to walk within `rad` of its CENTRE. Then it deals the
       whole of what it remembers, in one number.

       ONE FIGURE IS ONE MINE. `points` and `ring` are a DRAWING: five points
       because a pentagram has five, strokes through them in `drawSigils`, and
       nothing is ever tested against them. It shipped first as five separate
       charges on that ring — v52 §3b measured the ring as the only
       arrangement that chains — and Rick watched it: "what isnt legible is
       the explosion itself ... my vision was the pentagram was 1 large mine
       not a cluster of small ones." Five payments of `stamp/5` put five
       three-damage numbers over the ball inside 42ms, and every number in the
       build was right while it read as noise.

       IT IS A BET ON WHERE THE FIGHT WILL BE, and that is measured: the same
       bomb HOMING is worth 12.5 to 19.0 points more (v52 §1). That gap is
       what keeps this off Gravemourn's verb, whose hand is a certainty.

       `dmg` 0 and `kind` "sigil", NOT "nova": nothing resolves at the cast.
       Eclipse was a 250-radius nova for 11 and it is gone, art included.

       `apply` STAYS GONE, and the row it rests on is v52 §3e's "1 charge,
       stamp x0.3" — +0.4%, one standard error from nothing. That is now
       LITERALLY this configuration rather than an argument by analogy: one
       payment a figure at a third of the pool. (The five-charge build rested
       on the "5 charges, stamp x0.3" row, +0.0%. Both say the same thing for
       the same reason — curse's top-K rule displaces the memory as it lands
       — and the mine is the one the design actually measured.) The figure
       reads the pool and never writes to it.

       `rad` IS NOT NAMED `radius` ON PURPOSE. `fireUlt` reads `u.radius` for
       its in-range test and the particle field reads it for its extent; the
       mine's own trigger is neither of those, and putting it in that field
       would silently shrink the cast's own set-piece.

       THE BLADE IS 15.83 -> %DMG% (stage 3b, `umbral_sweep.py`, 9750
       fights, run twice — once on the five-charge figure and again on the
       single mine). 15.83 priced a relic whose ultimate was dead. Unlike
       Gravemourn's, this curve does NOT bend: it is monotone and steep from
       14.1% at dmg 8 to 89.0% at 22. And the cut does not gut the relic —
       the echo is still 14.3% of everything it delivers and the pool is up
       90% of the fight. See nightfell_build.TUNED_NF3. */
    ult:{ name:"%ULT%", charge:15, kind:"sigil", dmg:0,
          dur:%DUR%, points:%POINTS%, ring:%RING%, rad:%RAD%,
          arm:%ARM%, stampMul:%STAMPMUL%, push:%PUSH%,
          tip:"%TIP%" },'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
    if new.count("/*") != new.count("*/"):
        raise SystemExit(f"BLOCK {label}: {new.count('/*')} '/*' against "
                         f"{new.count('*/')} '*/'. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


# ---- ECLIPSE'S OVER-ART IS RETIRED WITH THE MECHANIC IT DREW ---------------
# An occulted body with a corona, held over the caster, explaining a 250-radius
# nova for 11 damage. DEADFALL does not nova, so keeping it would be the drift
# `docs/ARCHITECTURE.md` §1 exists to prevent, one layer down: the art saying
# one mechanic while the sim runs another. It is ~70 lines, so it is cut by
# BOUNDED EXCISION rather than by a literal anchor -- and the excision refuses
# on anything it does not recognise, which is the same promise `one()` makes.
ECL_HEAD = ("    /* ---- Eclipse: an OCCULTED BODY, and a shadow front that "
            "puts lights out -")
ECL_TAIL = "    /* ---- Corollary: the proof, stepped out and then concluded"


def cut_eclipse(src: str) -> str:
    if src.count(ECL_HEAD) != 1 or src.count(ECL_TAIL) != 1:
        raise SystemExit("ECLIPSE CUT: head or tail is not unique. The source "
                         "has moved under this builder.")
    i, j = src.index(ECL_HEAD), src.index(ECL_TAIL)
    span = src[i:j]
    if not (i < j and 1500 < len(span) < 4500):
        raise SystemExit(f"ECLIPSE CUT: the span is {len(span)} characters and "
                         f"nothing that size is the block this is meant to "
                         f"remove. Refusing.")
    for must in ('else if (u.w === "nightfell"){', "THE BODY: black",
                 "const BODY = 54;"):
        if must not in span:
            raise SystemExit(f"ECLIPSE CUT: the span does not contain "
                             f"{must!r}. Refusing.")
    if span.count("/*") != span.count("*/"):
        raise SystemExit("ECLIPSE CUT: the span's comments are unbalanced, so "
                         "the cut would take a `*/` the rest of the file needs.")
    print(f"  cut   Eclipse's over-art, {len(span)} characters "
          f"({span.count(chr(10))} lines)")
    return src[:i] + src[j:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-gravemourn.html")
    ap.add_argument("--out", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=TUNED_NF3,
                    help="stage 3b: the blade, with DEADFALL in place")
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
    print("\nNIGHTFELL -- DEADFALL: sigils that arm, then take whatever walks in")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    # THE CHAIN IS LINEAR AND STAGE 3 SITS ON STAGES 1 AND 2. The figures read
    # the curse pool; without the rework there is nothing to read.
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the Curse rework "
                         "lands FIRST (brief §0). Build off sc-gravemourn.html.")
    if '"sling"' not in s0:
        raise SystemExit("this source has no sling -- stage 2 lands before "
                         "stage 3 (brief §0). Build off sc-gravemourn.html.")
    if '"sigil"' in s0:
        raise SystemExit("this source already has a sigil -- already built")

    if int(A.points) < 3:
        raise SystemExit(f"points {A.points:g}: a figure of fewer than three "
                         f"charges is a dot, and the chain is the density "
                         f"INSIDE the figure (v52 §3b).")
    if len(A.tip) > 72:
        raise SystemExit(f"ULT TIP is {len(A.tip)} characters against 72:\n  {A.tip}")

    print(f"  ult {A.ult}   " + "  ".join(f"{k} {getattr(A, k):g}" for k in ULT))
    print(f"  tip {len(A.tip)}/72  {A.tip}")
    print(f"  blade {A.dmg:g}   (stage 3b, from {BLADE_IN:g})")

    subs = {"%ULT%": A.ult, "%TIP%": A.tip, "%DMG%": f"{A.dmg:g}",
            "%DUR%": f"{A.dur:g}", "%POINTS%": f"{int(A.points):d}",
            "%RING%": f"{A.ring:g}", "%RAD%": f"{A.rad:g}",
            "%ARM%": f"{A.arm:g}", "%STAMPMUL%": f"{A.stampmul:g}",
            "%PUSH%": f"{A.push:g}"}

    s = cut_eclipse(s)

    for label, old, new in EDITS:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    if abs(A.dmg - BLADE_IN) > 1e-9:
        # THE GREATSWORDS SHARE A STAT LINE, so the blade is found by walking
        # forward from the relic's own id and never by a global replace.
        old_blade = f"mass:3.0, dmg:{BLADE_IN:g},"
        i = s.index('id:"nightfell"')
        j = s.find(old_blade, i)
        if j < 0 or j - i > 400:
            raise SystemExit(f"cannot retune the blade: {old_blade!r} is not "
                             f"in Nightfell's own entry.")
        s = s[:j] + f"mass:3.0, dmg:{A.dmg:g}," + s[j + len(old_blade):]
        print(f"  blade dmg {BLADE_IN:g} -> {A.dmg:g}  (stage 3b)")

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # §8.3b IS A HARD RULE AND IT IS A PROPERTY OF THE TEXT. The figure READS
    # the pool. A build in which a charge pushes to it or applies curse has
    # recreated the +0.0 clause v52 §3e deleted, and has also handed this relic
    # Gravemourn's verb -- and both of those look FINE in every win rate,
    # because a memory that is displaced on arrival costs nothing either.
    #
    # COMMENTS ARE STRIPPED FIRST. `curse_build` refused to write on its own
    # explanation an hour after `curse_check` fired on one, and this file
    # explains itself in exactly the same way -- the paragraph above contains
    # every string being searched for.
    lo = s.index("tickDeadfall(dt){")
    hi = s.index("tickSling(dt){", lo)
    body = "\n".join(ln for ln in s[lo:hi].splitlines()
                     if "/*" not in ln and "*/" not in ln
                     and not ln.strip().startswith("*")
                     and "//" not in ln)
    for bad in ("pushCurse", 'apply("curse"', "cursePool"):
        if bad in body:
            raise SystemExit(
                f"`tickDeadfall` contains {bad!r}. THE FIGURE IS READ-ONLY ON "
                f"THE POOL (brief §8.3b): Gravemourn moves a memory, this one "
                f"copies it. A charge that writes to the pool is the +0.0 "
                f"clause v52 §3e deleted, coming back invisibly.")
    # AND THE CASTER MUST NOT BE ABLE TO SET ONE OFF (§8.3c). The proximity
    # test reads `foe` and nothing else; asserted rather than trusted, because
    # a self-triggering figure eats 48% of its own charges while every gate in
    # this repo stays green -- the cost tunes straight out of the blade.
    scan = body[body.index("let hitG = null"):body.index("if (!hitG) return;")]
    for bad in ("own.", "me.x", "this.a.x", "this.b.x"):
        if bad in scan:
            raise SystemExit(
                f"THE DETONATION SCAN READS {bad!r} (§8.3c). It may look at "
                f"the foe's position and nothing else: the charges are planted "
                f"where blows land, which is exactly where the caster is "
                f"standing, and a self-triggering figure eats 48% of them.")
    print("  rule  tickDeadfall never writes the pool, and only ever reads "
          "the foe's position")

    # THE INLINED MODULE AND THE FILE ON DISK MUST STAY THE SAME OBJECT.
    # `fx_build.py` inlines `src/render/fx.js` verbatim and stamps its sha256
    # into the page; this builder rewrites nightfell's spec in the inlined
    # copy. Written only there, the next rebuild through fx_build would
    # silently restore Eclipse's field -- a picture fault with no number
    # attached to it, which is the exact class this whole edit exists to fix.
    # So the same spec goes into `src/render/fx.js`, and this REFUSES TO WRITE
    # unless the two are byte-identical, then re-stamps.
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
    inlined = s[head.end():tm.start()].rstrip("\n")
    if inlined != mod.rstrip():
        raise SystemExit(
            "src/render/fx.js and the copy inlined in this build have "
            "DIVERGED.\n  The spec this builder writes into the page must "
            "also be in the file\n  fx_build.py inlines, or the next rebuild "
            "drops it.\n  inlined "
            f"{len(inlined)} bytes against {len(mod.rstrip())} on disk.")
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
    print(f"  fx    src/render/fx.js re-stamped {old_sha[:16]} -> "
          f"{new_sha[:16]}  (inlined copy verified byte-identical)")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT, and item one is not optional (v43 §13, brief §0):")
    print(f"    python cinema_clip.py --game {A.out} --a nightfell "
          f"--b emberedge --seed <seed> --full   # FILM IT FIRST")
    print(f"    python nightfell_relic_probe.py --game {A.out}")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10   # the 25")
    print(f"    python verify.py --game {A.out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
