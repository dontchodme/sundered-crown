#!/usr/bin/env python3
"""THE RUNIC FLAIL. The twenty-fifth relic, and the first thing that stops a ball.

    python3 paradox_build.py --src ../02-chain/sc-marrowdraw.html \
                             --out ../02-chain/sc-paradox.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v43 design document:

    "blue flail gains a medium sized hexagonal shaped chain of lightning
     surrounding the flails ball. the flail gains extra hit stun. enemies that
     stay inside the hexagon (that is inside the beams of lightning with the
     flail head) for too long are true stunned. unable to move (ball and
     weapon) for 2ish seconds."

FOUR SENTENCES, ALL FOUR PRICED BEFORE THIS FILE WAS OPENED
(`runic_flail_probe.py`, 12/12, runtime-only on the v42 tip), and three of the
four came back needing a decision that measurement could make:

    THE SIZE     "medium sized" is bounded BELOW by §1's own parenthesis --
                 the head is inside the beams, and the head reaches 115 units
                 from the shell. Rick took 200: the foe is inside 32.3% of the
                 fight and crosses 46 times a minute.
    THE SHAPE    A LOOK KNOB, measured. A hexagon collects 81% of what its
                 circumcircle collects against an 83% area ratio, and turning
                 it with the weapon moves the share of the fight by 0.06%.
    THE DWELL    "FOR TOO LONG" COULD NOT BE TWO SECONDS. At radius 200 the
                 median continuous residence is 0.34s and the longest of 1058
                 was 1.95. Rick took the fork: a CHARGE that fills inside and
                 bleeds outside, which says the same thing on screen and fires
                 6.2 times a minute where the continuous rule fires 0.0.
    THE STUN     +42% damage over nothing and +21% over a weapon-only lock,
                 because a 13-unit head against a target that has stopped
                 moving is a different weapon. This is the half of §1 that
                 measured strongest and it is a state the engine has never had.

AND THE ONE SENTENCE THAT WAS REPLACED RATHER THAN BUILT. "The flail gains
extra hit stun" is measurably inert on this type: a 3x multiplier on this
relic's own hitstun moves the foe's lock from 20.6% to 23.1% and does not move
damage taken at all, because the weapon lands a blow every six seconds. Rick's
call, from three priced options: **a landed blow feeds the CHARGE instead.**
The sentence keeps its intent -- your blows shut them down harder -- and the
hardest blow in the game starts mattering to the mechanic rather than to a
stun ladder that cannot build.

## WHY THIS IS THE ANSWER TO WHAT THE SURVEY MEASURED

`flail_survey` §2: **the flail's live blade is 13.2 units** -- `width x 0.6`,
with its reach of 96 appearing nowhere in it -- against 61 to 128 for every
other type. It covers the most ground in the game and is live in the least of
it. §6: **its own contact interval is 5.94 seconds against a 2.6-second
status**, so 75% of every hex it applies lands on a foe with no stacks and the
ladder is re-lit from cold three times in four.

Both of those are the same problem: **this weapon cannot reliably touch
anything.** Stasis Field does not add reach, damage or contacts. It takes the
one thing that makes a 13-unit head miss -- that the target is moving -- and
removes it, on a foe that is by construction already inside the swing.

## What the engine gives free, and what had to be invented

`f.stun` IS THE WEAPON HALF, and it is already a TRUE stun in this school's
hands: hex is one of exactly three sources that break a wind-up
(`flail_survey` §7), so a hold that writes `f.stun` inherits that without a
special case. `breakSpin` is called for the same reason Bramblesnare calls it.

**THE BALL HALF DID NOT EXIST.** `moveMul` floors at 0.45, `speedMin` is 250,
and `fireUlt`'s `u.freeze` -- the thing two viewer-facing tips call "roots" --
writes `foe.stun` and touches the ball not at all. So `f.pin` is new, and it is
one line in one function: `move` returns on it. Nothing else in the engine
reads it.

## The zero-burden argument, kept structurally

    ALL STATE IS `f.ultField` AND `f.pin`, AND BOTH ARE null/0 ON EVERY
    OTHER RELIC AND ON THIS ONE OUTSIDE ITS OWN WINDOW.

`tickStasis` returns after a two-iteration loop that does nothing when no
fighter is held and neither carries a field. `_drawField` returns on its first
line. The `resolveHit` branch is one `if (self.ultField)`. `engine_ab` over the
twenty-four pre-existing ids is the proof, not this paragraph.

## Two known audio bugs are NOT fixed here, deliberately

`_burst` does not loop a 0.6s noise buffer, so every `_burst` longer than 0.6s
in this game has been playing silence for its tail (v42 §12). `_tone`'s
frequency automation is un-anchored (v42 3d), measured at 0.4-3.4 points of
band shift across four shipped voices.

Both bite exactly what a sustained electrical hum needs. **Fixing either is a
chain-wide change to shipped sound on twenty-four relics and is Rick's call,
not a slip-in** -- so this relic's voice is written INSIDE the safe envelope
instead: every `_burst` is under 0.6s, the sustain is carried by `_tone`, and
`paradox_relic_probe [10]` RENDERS the result in an OfflineAudioContext and
measures it rather than trusting this paragraph.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `charge`, `dur`, `need`, `bleed`, `blow` and `pin` are not in the design
and cannot be guessed. `need` and `bleed` are not independent -- they jointly
set how often the hold lands -- and `paradox_sweep.py` solves them together.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# PARADOX. Rick's, from four offered. A trap that folds in on itself, which is
# what a zone you can neither see the edge of nor choose to leave actually is,
# and it sits beside Axiom as the same kind of word without being it.
#
# STASIS FIELD. Rick's, and his own words rather than one of the twelve
# offered across three spreads -- two of which he rejected outright, which is
# the same "offer a spread, not a guess" lesson arriving from the other end:
# a spread is cheap and being wrong about the REGISTER is what costs.
# `hex-*` was ruled out BEFORE the first spread, the way `quarrel` was in v42:
# the school's status is literally called Hex and the hold measurably
# OVERWRITES 61% of its fires, so a hex- name would tell the viewer the
# ultimate is the status when it is the thing that eats it.
#
# THE ID MATCHES THE NAME. `oathwound`/Goreshard and `redflail`/Threshmaw are
# the two existing drifts in this roster and both are traps; a third is not
# worth the twenty minutes it takes to avoid.
RELIC_ID = "paradox"
RELIC_NAME = "Paradox"
ULT_NAME = "Stasis Field"

# A PLACEHOLDER, AND IT MUST BE BISECTED AGAINST THE WHOLE FIELD.
# The type ships 25.0 (Threshmaw) .. 44.1 (Gravemourn) and `flail_survey` §5
# measured hex as the second-strongest channel on the row by delivered effect
# (+12.1%) and the only one of four that cuts damage TAKEN -- so the
# expectation going in is that this lands BELOW the middle of the type. That
# expectation is written down here so the sweep can refute it.
#
# v41 open decision 2 is why "the whole field" is in this comment: Bulwarden's
# dmg was bisected on a five-foe subset that read 50% and the full 23-opponent
# field read 55.2% on the same number.
TUNED_PX = 35.0

# EVERY ONE OF THESE IS A PLACEHOLDER.
ULT = {
    # Runic ships 13 (Axiom, Spellbreaker) and 15 (Foregone). A NINE-SECOND
    # window that can hold the foe still three times should not be the
    # cheapest thing in its school.
    "charge":   16.0,
    # HOW LONG THE FIELD STANDS. Aegis is 9 and Bloodhunt is 8; this is the
    # longest in the game by a nose because the field does nothing on the
    # frame it is cast -- it has to be up long enough for the foe to wander
    # into it, and at radius 200 that is 46 crossings a minute.
    "dur":       9.0,
    # THE HEXAGON'S CIRCUMRADIUS. **RICK'S CALL, from four priced options.**
    # Bounded below at 115 by §1's own parenthesis -- the head is inside the
    # beams -- and at 200 the foe is inside 32.3% of the fight. The hall is
    # 520 across, so this is 400 of it.
    "rad":     200.0,
    # HOW MUCH ACCRUED DWELL THE HOLD COSTS, in seconds. NOT a continuous
    # residence: `runic_flail_probe [2]` measured the longest unbroken stay in
    # 1058 episodes at 1.95s and NONE at two, so the continuous reading of §1
    # fires 0.0 times a minute. This is the charge, and it fills at 1/s while
    # the foe is inside.
    "need":      0.6,
    # HOW FAST IT BLEEDS BACK, per second, while the foe is outside.
    # **THIS IS THE ONLY COUNTERPLAY KNOB THIS DESIGN CAN HAVE**, and that is
    # a measurement rather than a complaint: nothing in this game steers, so a
    # foe cannot choose to leave the field and "get out of it" is not advice.
    # At 0 the zone is a stopwatch that never resets and "get clear" stops
    # meaning anything; at 2 it is a trap that has to be sprung almost in one
    # pass. RICK'S CALL from four measured settings, and the framing that made
    # it decidable: the bisection compensates, so this pair does not choose how
    # hard the relic hits -- it chooses HOW MUCH OF THE RELIC IS THE FIELD.
    # At 0.6/0.5 the window is 24.7% of its damage and lands 1.54 holds a cast,
    # so every cast catches something and most catch twice.
    "bleed":     0.5,
    # WHAT A LANDED BLOW ADDS TO THE CHARGE, in seconds. §1's second sentence,
    # converted -- see the header. Rick's call from three priced options.
    "blow":      0.5,
    # HOW LONG THE HOLD LASTS. §1's "2ish seconds", and the number the +42%
    # was measured at.
    "pin":       2.0,
    # HOW MANY SIDES. **PURE LOOK, and that is measured rather than asserted**
    # -- `runic_flail_probe [3]` swept a hexagon against its own circumcircle,
    # its inscribed circle and a static copy of itself: the hexagon collects
    # 81% of the circumcircle against an 83% area ratio, and turning it with
    # the weapon changes the share of the fight by 0.06%. Draw it at whatever
    # reads; nothing downstream is balanced on the corners.
    "arcs":      6.0,
}


# --------------------------------------------------------------- the relic --

RELIC_NEW = r'''    blurb:"Hooked bone, strung on marrow. Nothing it looses is finished with you on the way past." },

  /* PARADOX -- the runic flail, and the first thing in this game that stops a
     BALL. Physics are Threshmaw's and Slagheart's and Gravemourn's exactly
     (the type owns them, field for field); the school owns Hex and the blue.

     THE CELL'S PROBLEM, measured before the design existed
     (`flail_survey.py`, and the survey that chose the cell):

       THE HEAD IS THE WEAPON AND IT IS 13.2 UNITS LONG. `bladeSegments`
       returns `width * 0.6` for a chain and `reach + shell` for everything
       else, so this type is live in 13 units where a greatsword is live in
       128 -- and its reach of 96 appears NOWHERE in its own hit test. It
       covers the most ground in the game and occupies the least of it. That
       is why it is paid 25-44 damage a blow.

       AND ITS OWN CLOCK IS SLOWER THAN ITS OWN STATUS. It lands a blow every
       5.94 seconds; hex expires in 2.6. So 75% of every hex this cell applies
       arrives on a foe with no stacks, and 71% of the gaps between its own
       blows outlast the status it carries. The ladder is not topping out low.
       It is being re-lit from cold three times in four.

     Both of those are one problem: THIS WEAPON CANNOT RELIABLY TOUCH
     ANYTHING. So the ultimate does not add reach, damage or contacts. It
     removes the reason a 13-unit head misses -- that the target is moving --
     on a foe that is already inside the swing by construction.

     `dmg` is a PLACEHOLDER (paradox_build.TUNED_PX) and MUST be swept. */
  { id:"%ID%", name:"%NAME%", aff:"runic", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:%DMG%, spin:2.2, mode:"chain", mass:3.6,
    onHit:{ hex:1 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"stasis",
          dur:%DUR%, rad:%RAD%,
          need:%NEED%, bleed:%BLEED%, blow:%BLOW%, pin:%PIN%,
          /* PURE LOOK. runic_flail_probe [3] swept the hexagon against its own
             circumcircle, its inscribed circle and a static copy of itself:
             it collects 81% of the circumcircle against an 83% area ratio,
             and turning it with the weapon moves the share of the fight by
             0.06%. The RADIUS is the mechanic; the corners are a picture. */
          arcs:%ARCS%,
          /* THE NUMBERS IN THIS LINE ARE SUBSTITUTED, not typed. v40 shipped
             a card reading "5s" after a sweep moved the number to 8.1 and
             nothing caught it, because verify.py only asks that a tip EXISTS.
             `paradox_relic_probe [1]` asserts every number here against a
             field the weapon actually has. */
          /* A PLACEHOLDER UNTIL RICK WORDS IT. His line is one of the seven
             things this project asks him for, and v42's card was his wording
             rather than one of the four offered. This one also has a HARD
             LIMIT nobody had hit before: `verify.py` fails an ult tip over 72
             characters, and the first cut of this line was 73. */
          tip:"For %DUR%s, rings itself in lightning — linger inside and freeze for %PIN%s" },
    blurb:"A pit chain swung inside its own storm. Stand in it long enough and the argument is over." },

];'''


# ------------------------------------------------------------ fighter state --

FIGHTER_STATE_NEW = r'''    this.ultAegis = null;
    /* {t, dur, q, in, pins} while the Stasis Field stands. null on every
       other relic and on this one outside its own window, which is the whole
       zero-burden argument: `tickStasis` returns after a two-iteration loop
       that does nothing, `_drawField` returns on its first line, and the
       branch in resolveHit is one `if (self.ultField)`. */
    this.ultField = null;
    /* HELD. §1: "unable to move (ball and weapon) for 2ish seconds."
       THE WEAPON HALF ALREADY EXISTED -- `f.stun` -- and it is already a TRUE
       stun in this school's hands, because hex is one of exactly three
       sources that break a wind-up. THE BALL HALF DID NOT: `moveMul` floors
       at 0.45, `speedMin` is 250, and `u.freeze` -- the thing two shipped
       tips call "roots" -- writes `foe.stun` and touches the ball not at all.
       So this is new, and it is one line in one function: `move` returns on
       it. Nothing else in the engine reads it. Velocity is preserved across
       the hold, so release is a resume rather than a drop, and
       `ballCollision` is deliberately NOT gated -- a held ball can still be
       shouldered out of the way, which is what the probe measured. */
    this.pin = 0;
    this.pinMax = 0;          // presentation only: what the hold was, for the fade
    /* THE VELOCITY IT WAS CAPTURED WITH. null on every other relic and on this
       one outside a hold; `move` restores it and drops it on the frame the
       hold lifts, which is what "resume, with no banked knockback and no loss
       of momentum" is in two lines. */
    this.pinV = null;'''


# ---------------------------------------------------------------- the cast --

FIRE_ULT_NEW = r'''    if (u.kind === "stasis"){
      /* The field does NOTHING on the frame it is cast, which is the one
         thing that makes `dur` load-bearing: it has to stand long enough for
         the foe to wander into it, and at radius 200 that is 46 crossings a
         minute. Nothing else here -- no damage, no knock, no application.
         §1 asks for a ring and a hold, and a cast that also hit would be
         paying the ultimate twice. */
      f.ultField = { t: 0, dur: u.dur, q: 0, in: false, pins: 0 };
      /* NORMAL path: the fx clock runs at 2x sim time, and this set-piece has
         to still be on screen for the whole window the way Aegis's is -- the
         map entry in the table above is only the fallback if this is missed. */
      this.ultFx.life = (u.dur + 0.5) * 2;
      return;
    }

    if (u.kind === "ballista"){'''


# ---------------------------------------------------------------- the hold --

MOVE_NEW = r'''  move(f, foe, dt){
    /* HELD. The whole of §1's "unable to move (ball)", in one line.
       `f.pin` is 0 on every other relic and on this one outside a hold, so
       this is a comparison against zero on a field nothing else writes.
       Deliberately BEFORE gravity: a held ball does not accumulate fall
       either, so what it resumes with is what it arrived with. */
    if (f.pin > 0) return;
    /* AND THE FRAME IT LIFTS. Rick: "ball should just resume when the stun
       ends. no banked knockback and no loss of momentum after the stun."

       A ball that cannot move can still be PUSHED -- knockback from every blow
       it eats while it is held, a bind it loses, a shade shouldering it -- and
       none of that can be spent while `pin` holds. The first build let it all
       accumulate and the ball launched on release at up to 165 units/s per
       blow banked. Measured, named, and refused: everything that happened to
       its velocity while it could not use it is discarded HERE, on the first
       frame it is allowed to move again, and the vector it resumes with is
       byte-for-byte the one it was captured with.

       This line and not the capture site, because the capture site is
       `tickStasis`, which runs BEFORE `tickHits` -- restoring there would
       leave one frame of blows unspent-but-not-discarded. `move` is the first
       thing that reads velocity after a hold and it is the last chance to be
       exactly right. */
    if (f.pinV){ f.vx = f.pinV[0]; f.vy = f.pinV[1]; f.pinV = null; }
    const P = CONFIG.physics, R = P.ballR;'''


# --------------------------------------------------------------- the field --

TICK_STASIS_NEW = r'''  /* THE STASIS FIELD. A hexagon of lightning hung on the caster; a charge that
     fills while the quarry is inside it and bleeds while it is out; and a hold
     when the charge fills.

     WHY A CHARGE AND NOT A RESIDENCE. §1 says "enemies that stay inside the
     hexagon for too long", and the literal reading -- an unbroken two-second
     stay -- was measured on the previous tip and fires ZERO times a minute.
     At this radius the median unbroken stay is 0.34s and the longest of 1058
     was 1.95. Nothing in this game steers: a ball is ballistic, bounces, and
     never travels slower than 250 units a second, so it does not loiter, it
     crosses -- 46 times a minute. The charge says the same sentence on screen
     and is the version that can happen.

     `bleed` IS THE COUNTERPLAY AND IT IS THE ONLY ONE THERE IS. That is a
     measurement, not a shrug: every other relic's counterplay is a thing the
     foe's weapon does -- a bolt can be batted, a wall can be gone round -- and
     a foe cannot choose to leave a zone in a game with no steering. So the
     one lever on how forgiving this is, is how fast the charge comes back
     when the quarry gets clear by luck.

     ORDER. Called after the fighter loop -- so `move` has already run and the
     positions are current -- and before `tickHits`, so a hold lands on the
     same frame the hit loop reads it. Exactly where `tickAegis` sits, and for
     the same reason. */
  tickStasis(dt){
    /* THE HOLD OUTLIVES THE WINDOW. A field that fills its charge at 8.9s of
       a 9s window still holds for the full two, so this clock is deliberately
       outside the `ultField` guard below. `f.stun` is REFRESHED rather than
       set once: tickStatus takes dt off it every frame, and a weapon that
       came unlocked halfway through a hold would be a ball frozen in the air
       swinging. */
    for (const f of [this.a, this.b]){
      if (f.pin <= 0) continue;
      /* A KILL FLIGHT IS NOT A HOLD, and `pinV` goes with it -- the launch
         `resolveHit` wrote into a dying ball's velocity must not be restored
         away by a hold that is already over. */
      if (!f.alive){ f.pin = 0; f.pinV = null; continue; }
      f.pin = Math.max(0, f.pin - dt);
      f.stun = Math.max(f.stun, f.pin);
    }
    if (!this.a.ultField && !this.b.ultField) return;

    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const F = f.ultField;
      if (!F) continue;
      const u = f.w.ult;
      F.t += dt;
      if (F.t >= F.dur || !f.alive){ f.ultField = null; continue; }
      /* A QUARRY ALREADY HELD IS NOT ACCRUING TOWARD THE NEXT HOLD. Without
         this the charge would keep filling through a hold it caused -- the
         foe is pinned inside the hexagon by construction -- and the field
         would chain holds back to back for the rest of the window. */
      if (foe.pin > 0 || !foe.alive){ F.in = false; continue; }

      F.in = this.inField(f, foe.x, foe.y, u);
      F.q = F.in ? F.q + dt : Math.max(0, F.q - u.bleed * dt);
      if (F.q < u.need) continue;

      F.q = 0; F.pins++;
      foe.pin = u.pin;
      foe.pinMax = u.pin;
      foe.pinV = [foe.vx, foe.vy];    // what it resumes with, exactly
      foe.stun = Math.max(foe.stun, u.pin);
      /* A TRUE STUN, and it says so the same way hex does. `breakSpin` is
         what separates the three stuns that cancel a wind-up from the two
         that only delay it, and a hold that left Bloodmill winding would be
         teaching the viewer that the rule is decorative. */
      this.breakSpin(foe, "held in the field");
      /* THE DIRECTOR HAS TO BE TOLD. Rule 3, fifth relic running: this is a
         control event with no damage and no contact, so nothing else in the
         frame would file anything and `cinePlan` would score the most
         legible moment of the ultimate as empty air. Written to a list the
         simulation never reads -- `engine_ab` is the proof of that, not this
         comment. */
      this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                  w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
      this.hitStop = Math.max(this.hitStop, 0.06);
      this.shake = Math.max(this.shake, 20);
      this.ring(foe.x, foe.y, f.aff.core, 10, 150, 0.45, 6);
      this.ring(foe.x, foe.y, f.aff.glow, 4, 96, 0.30, 4);
      this.spawnFx(foe.x, foe.y, f.aff.glow, 18, 240, 0.45, 3);
      SFX.play("ult", { w: "paradox-pin" });
      this.note(`${f.w.name} — held`);
    }
  }

  /* ONE definition of "inside", called by the simulation and by nothing else.
     A regular `arcs`-gon of circumradius `u.rad`, turning with the weapon --
     which is a picture rather than a mechanic (the probe measured the
     difference at 0.06% of the fight) but costs nothing to honour, and means
     the drawn beams and the tested boundary are the same object.

     Two cheap exits before the trigonometry: outside the circumcircle is out,
     inside the incircle is in, and only the corners need the angle. */
  inField(f, x, y, u){
    const dx = x - f.x, dy = y - f.y;
    const d = Math.hypot(dx, dy);
    if (d > u.rad) return false;
    const n = u.arcs, K = Math.cos(Math.PI / n);
    if (d <= u.rad * K) return true;
    const seg = TAU / n;
    let a = (Math.atan2(dy, dx) - f.theta) % seg;
    if (a < 0) a += seg;
    return d * Math.cos(a - Math.PI / n) <= u.rad * K;
  }

  tickHits(self, foe, dt, cool){'''

TICK_CALL_NEW = r'''    this.tickStasis(dt);
    this.tickAegis(dt);'''


# ------------------------------------------------------ the blow feeds it --

HITSTUN_NEW = r'''                shotSpd0: _cs ? (_cs.spd0 || 0) : 0 });
    if (!fatal) foe.takeHitstun(dmg);
    /* THE BLOW FEEDS THE FIELD. §1's second sentence is "the flail gains extra
       hit stun", and that was measured on the previous tip and is inert on
       this type: a 3x multiplier on this relic's own hitstun moves the foe's
       lock from 20.6% to 23.1% and does not move damage taken at all, because
       the weapon lands a blow every six seconds. Tripling the stagger of a
       blow that rare is tripling almost nothing.

       Rick's call, from three priced options: the blow feeds the CHARGE
       instead. Same sentence -- your blows shut them down harder -- with the
       hardest hit in the game pushed at the mechanic rather than at a ladder
       that cannot build.

       `mul === undefined` is an ordinary melee connect and not a projectile,
       the same test Ironbloom's latch and the Crucible's strike use. The
       `foe.pin` guard is the same one tickStasis has: a hold does not feed
       the hold that caused it.

       `!foe.shade` is the third clause and it is not decoration: `me` can
       land an ordinary melee blow on a COPY of the quarry -- Triplicate walks
       three of them -- and a blow on a copy fed the charge while the real
       quarry was already held, which is the one thing the `foe.pin` guard
       exists to stop. Reading `f.shade` is how every branch in this build asks
       whether a body is a relic or a picture of one. Found by a probe check
       that reported ONE frame in six thousand and was right.

       `foe.alive` is the fourth clause and it is the same guard `tickStasis`
       already carries: a charge exists to hold a LIVING quarry, and the
       killing blow feeding one is state with nowhere to go. Two frames in
       seven thousand, found by a check that asserts the field stops asking
       when the quarry is dead. */
    if (mul === undefined && self.ultField && !foe.shade
        && foe.alive && foe.pin <= 0)
      self.ultField.q += self.w.ult.blow;'''


# ------------------------------------------------------------------- art --

DRAW_FIELD_NEW = r'''  /* THE FIELD, AND THE THING HELD IN IT. Two pictures, one method, and it
     returns on its first line for every relic that is not casting and every
     fighter that is not held. */
  _drawField(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR;
    const F = f.ultField;
    if (F){
      const u = f.w.ult, P = f.aff, n = u.arcs;
      /* THE CHARGE IS THE PICTURE. There is no bar and no number: the beams
         brighten, thicken and go jagged as the charge fills, and settle back
         when the quarry gets clear. A viewer who has read nothing can see the
         pressure building and can see it bleed off.

         This ultimate spends most of its nine seconds doing nothing that
         lands, which is the exact case rule 1 exists for -- if the window
         does not say what it is doing, it reads as a window in which nothing
         happened, three times out of four. */
      const load = clamp(F.q / u.need, 0, 1);
      const fade = clamp(Math.min(F.t / 0.30, (F.dur - F.t) / 0.45), 0, 1);
      /* The floor is 0.45 and not 0.30: the first cut left a cold field
         almost invisible in the hall, and a window that cannot be seen
         standing is a window the viewer thinks did nothing. */
      const heat = 0.45 + 0.55 * load;
      const seg = TAU / n;
      /* Deterministic off `m.t`, the way SHAPES._t is. An ACCUMULATED phase
         would strobe against the frame interpolator -- v42's eyes learned
         that, and lightning is the worst possible thing to learn it on.

         THREE FREQUENCIES AND A WINDOW. One sine is a wobble and reads as a
         hand-drawn polygon, which is what the first cut looked like: the
         difference between a wobble and an arc is high-frequency detail on
         top of a low-frequency wander. The `sin(pi*t)` window pins both ends
         to the vertex exactly, so the corners stay corners. */
      const jag = (i, t2) => {
        const p2 = t2 * 3.7 + i * 2.13;
        return (Math.sin(p2 * 17.3 + m.t * 13.0) * 0.28
              + Math.sin(p2 *  6.1 + m.t *  9.0) * 0.42
              + Math.sin(p2 *  2.3 + m.t *  4.1) * 0.55)
             * Math.sin(Math.PI * t2);
      };
      const pts = [];
      for (let i = 0; i < n; i++){
        const a = f.theta + i * seg;
        pts.push([f.x + Math.cos(a) * u.rad, f.y + Math.sin(a) * u.rad]);
      }
      const STEPS = 14;
      const stroke = (w, col, alpha, amp) => {
        c.globalAlpha = alpha * fade;
        c.strokeStyle = col; c.lineWidth = w;
        c.beginPath();
        for (let i = 0; i < n; i++){
          const p0 = pts[i], p1 = pts[(i + 1) % n];
          const nx = -(p1[1] - p0[1]), ny = (p1[0] - p0[0]);
          const nl = Math.hypot(nx, ny) || 1;
          c.moveTo(p0[0], p0[1]);
          for (let s = 1; s <= STEPS; s++){
            const t2 = s / STEPS;
            const o = jag(i, t2) * amp;
            c.lineTo(p0[0] + (p1[0] - p0[0]) * t2 + (nx / nl) * o,
                     p0[1] + (p1[1] - p0[1]) * t2 + (ny / nl) * o);
          }
        }
        c.stroke();
      };
      c.save();
      c.lineCap = "round"; c.lineJoin = "round";
      const amp = 5 + 13 * load;
      /* Four passes, widest and dimmest first: a bloom, the school's blue, a
         near-white core, and a SECOND core on a different phase of the same
         jag, which is what stops a single stroke reading as a drawn line.
         Light is many strokes; a line is one. */
      stroke(13,  P.glow,     0.12 * heat, amp);
      stroke(6,   P.core,     0.34 * heat, amp);
      stroke(2.0, "#EAF4FF",  0.70 * heat, amp);
      stroke(1.1, "#FFFFFF",  0.34 * heat, amp * 1.35);
      /* THE SPOKES. Rick, on the first cut: "how about we add lightning lines
         that connect from the hexagons edges to the center?" -- and he is
         right about what was wrong. A ring hung in the hall with nothing
         joining it to the relic reads as a thing the hall is doing; the same
         ring wired back to the shell reads as a thing the RELIC is doing, and
         this is the caster's ultimate.

         THEY FLICKER, AND THAT IS THE POINT. Six permanent spokes are a wheel
         -- a drawn diagram, static and mechanical. An arc is intermittent, so
         each spoke is gated on its own phase and three or four of the six are
         lit at any moment. The gate is a function of `m.t` and the spoke
         index and nothing else, so it is deterministic and does not strobe
         against the frame interpolator.

         They start at the shell rather than at the centre: a line drawn to
         `f.x, f.y` passes through the ball and reads as impaling it. */
      const spokeAmp = 3 + 7 * load;
      for (let i = 0; i < n; i++){
        const lit = Math.sin(m.t * (5.1 + i * 0.83) + i * 2.2)
                  + Math.sin(m.t * (2.3 + i * 0.41) + i * 5.1) * 0.7;
        /* The gate is deliberately generous: at the first cut it lit about a
           fifth of the spokes at nearly zero alpha, which photographed as a
           ring with nothing joining it -- the exact thing this was added to
           fix. Four or five of six, and a lit spoke is properly lit. */
        const thr = -0.55 - load * 0.75;
        if (lit < thr) continue;
        const g = clamp(0.45 + (lit - thr) * 0.85, 0, 1);
        const p1 = pts[i];
        const ux = (p1[0] - f.x), uy = (p1[1] - f.y);
        const ul = Math.hypot(ux, uy) || 1;
        const x0 = f.x + (ux / ul) * (R + 3), y0 = f.y + (uy / ul) * (R + 3);
        const nx = -(p1[1] - y0), ny = (p1[0] - x0);
        const nl = Math.hypot(nx, ny) || 1;
        const path = (w2, col, alpha, amp2) => {
          c.globalAlpha = alpha * fade * g;
          c.strokeStyle = col; c.lineWidth = w2;
          c.beginPath(); c.moveTo(x0, y0);
          for (let s2 = 1; s2 <= 10; s2++){
            const t2 = s2 / 10, o = jag(i + 7, t2) * amp2;
            c.lineTo(x0 + (p1[0] - x0) * t2 + (nx / nl) * o,
                     y0 + (p1[1] - y0) * t2 + (ny / nl) * o);
          }
          c.stroke();
        };
        path(9,   P.glow,    0.11 * heat, spokeAmp);
        path(4,   P.core,    0.32 * heat, spokeAmp);
        path(1.5, "#EAF4FF", 0.62 * heat, spokeAmp);
      }
      /* THE NODES. A hexagon with its corners lit reads as six beams joined
         rather than as one ring, which is the object §1 named -- and now they
         are where the spokes land, so the corners are junctions. */
      c.globalAlpha = (0.45 + 0.55 * load) * fade;
      c.fillStyle = "#EAF4FF";
      for (let i = 0; i < n; i++){
        const r2 = 3.2 + 2.8 * load + Math.abs(jag(i, 0.5)) * 1.3;
        c.beginPath(); c.arc(pts[i][0], pts[i][1], r2, 0, TAU); c.fill();
      }
      c.restore();
    }

    if (f.pin > 0){
      /* HELD. Deliberately NOT the stagger ring: a stagger is a weapon that
         stopped and this is a BALL that stopped, and the picture has to be
         able to tell a viewer which one it is looking at. A hexagon closes on
         the shell and tightens as the hold runs out -- the same shape that
         caught it, arriving -- with the arcs that put it there still crawling
         over the ball. */
      const P = AFFINITIES.runic;
      const left = clamp(f.pin / Math.max(0.01, f.pinMax || 1), 0, 1);
      const n = 6, seg = TAU / n;
      const rr = R * (1.14 + 0.62 * left);
      c.save();
      c.globalAlpha = Math.min(1, f.pin * 5) * 0.92;
      c.lineJoin = "round";
      c.beginPath();
      for (let i = 0; i <= n; i++){
        const a = i * seg + m.t * 0.55;
        const x = f.x + Math.cos(a) * rr, y = f.y + Math.sin(a) * rr;
        if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
      }
      c.strokeStyle = P.core;  c.lineWidth = 3.6; c.stroke();
      c.strokeStyle = "#EAF4FF"; c.lineWidth = 1.3; c.stroke();
      c.strokeStyle = P.glow; c.lineWidth = 2.1;
      for (let i = 0; i < 3; i++){
        const a = m.t * (5.5 + i * 2.1) + i * TAU / 3;
        c.beginPath(); c.arc(f.x, f.y, R * 1.04, a, a + 0.55); c.stroke();
      }
      c.restore();
    }
  }

  _drawAegis(m, f){'''

DRAW_CALL_NEW = r'''    this._drawBalWindow(m, f);
    this._drawField(m, f);'''


# ----------------------------------------------------------------- sound --

SFX_ULT_VOICE_NEW = r'''        } else if (w === "paradox"){               // a field switching on
          /* NOT a blast. Something is SWITCHED ON and then stands there: a
             capacitive snap, a fast down-glide, and then a mains-shaped hum
             that holds for most of a second and a half with crackle over it.
             Every other cast in this game is an event; this one is a state,
             and it is the only voice in the roster that has to still be
             telling the viewer something a second after it started.

             RULE 3f: this is an impact plus a rough band plus steady tones --
             the class this toolkit is five-for-five on -- and deliberately
             NOT a voice, breath or creature vocalisation, which it is
             nought-for-four on.

             AND IT IS WRITTEN INSIDE THE ENVELOPE OF TWO KNOWN BUGS RATHER
             THAN FIXING THEM. `_burst` does not loop its 0.6s noise buffer,
             so every burst here is under 0.6s and the sustain is carried by
             `_tone`; fixing either helper is a chain-wide change to shipped
             sound on twenty-four relics and is not a thing a relic build gets
             to slip in. `paradox_relic_probe [10]` RENDERS this and measures
             it rather than trusting the paragraph. */
          this._burst(t, { freq: 5400, q: 0.9, gain: 0.30, dur: 0.05, type:"highpass" });
          this._tone (t, { freq: 1500, to: 190, gain: 0.20, dur: 0.15, type:"square" });
          this._burst(t + 0.02, { freq: 900, q: 0.8, gain: 0.14, dur: 0.28, type:"bandpass" });
          /* The hum. 108 / 162 / 324 is a fundamental, its fifth and its
             octave-and-a-fifth -- a harmonic stack rather than a cluster, so
             it reads as ELECTRICAL rather than as the drone Rick rejected for
             the score. The 324 is what survives a laptop: v42 measured 39% of
             the iron clamp sitting in 200-600 Hz and that is why it worked
             where a 30 Hz sine did not. `to` is a hair below `freq` on all
             three so the ramp is anchored and the field sags rather than
             sitting perfectly still. */
          /* AND IT IS RE-STRUCK RATHER THAN HELD, WHICH IS A MEASUREMENT AND
             NOT A STYLE. `_tone` ends on `exponentialRampToValueAtTime(0.0001)`
             over its whole `dur`, so a "sustained" 1.35s tone is an
             exponential decay that is 1% of its own level by 0.85s in -- v42
             said this in one line ("an exponential release spends its last
             third under the audible floor") and it is why `_growl` had to be a
             new builder. A relic build does not get to add one, so the field
             PULSES instead: four strikes at an irregular 0.36-0.39s, which is
             a 2.7 Hz buzz and reads as an arc rather than as a drone. Rick
             rejected a drone for the score for exactly the reason it would be
             wrong here -- "odd and unnatural", a sustained cluster with no
             motion in it. */
          [[0.05, 0.165], [0.41, 0.150], [0.80, 0.128], [1.14, 0.104]].forEach(
            ([d, g]) => {
              this._tone(t + d,        { freq: 108, to: 104, gain: g,        dur: 0.50, type:"sawtooth" });
              this._tone(t + d + 0.004,{ freq: 162, to: 158, gain: g * 0.55, dur: 0.46, type:"triangle" });
              this._tone(t + d + 0.008,{ freq: 324, to: 316, gain: g * 0.34, dur: 0.40, type:"triangle" });
            });
          /* Crackle, between the strikes rather than on them, and none of them
             longer than the 0.6s noise buffer `_burst` does not loop. */
          [[0.22, 4200], [0.58, 2800], [0.95, 3600], [1.30, 2400]].forEach(
            ([d, hz]) => this._burst(t + d,
              { freq: hz, q: 1.6, gain: 0.075, dur: 0.06, type:"bandpass" }));
        } else if (w === "paradox-pin"){            // the hold landing
          /* ONE EVENT, AND IT STOPS DEAD. A bright top, a short body, a drop,
             and then nothing -- no ring, no tail. The iron clamp in v42 rings
             for two seconds because struck metal rings; this is the opposite
             sound and it is the opposite for a reason a viewer can hear: the
             whole content of the moment is that something STOPPED. */
          this._burst(t, { freq: 4400, q: 1.2, gain: 0.32, dur: 0.035, type:"bandpass" });
          this._burst(t, { freq: 560,  q: 0.8, gain: 0.28, dur: 0.10,  type:"lowpass" });
          this._burst(t + 0.01, { freq: 3000, q: 2.0, gain: 0.10, dur: 0.12, type:"bandpass" });
          this._tone (t, { freq: 320, to: 74, gain: 0.34, dur: 0.18, type:"square" });
          this._tone (t + 0.02, { freq: 92, to: 88, gain: 0.20, dur: 0.30, type:"sine" });
        } else if (w === "bulwarden"){'''


ULTFX_LIFE_NEW = r'''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
              /* THE STASIS FIELD is set from `ult.dur` at the cast site, the
                 way Aegis and the Thicket are. This entry is the fallback if
                 that is ever missed. */
              paradox: 9.5,'''


# ------------------------------------------------------- an immovable ball --

BALLPAIR_NEW = r'''  _ballPair(a, b){
    const R = CONFIG.physics.ballR;
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.hypot(dx, dy);
    if (d >= R * 2 || d === 0) return;
    const nx = dx / d, ny = dy / d, overlap = R * 2 - d;
    /* A HELD BALL IS AN IMMOVABLE OBJECT. §1 says "unable to move (ball and
       weapon)", and a held ball that could still be shouldered across the hall
       would be a hold the viewer can watch being broken by the thing that cast
       it. So both halves of the separation and the whole of the impulse go to
       the other ball -- the equal-mass exchange with one mass sent to
       infinity, which is what an immovable object is.

       BYTE-IDENTICAL WHEN NOBODY IS HELD. `pin` is 0 on every other relic and
       on this one outside a hold, so `wa` and `wb` are both exactly 0.5, the
       impulse factor is exactly 1, and `overlap * 0.5` is the same IEEE754
       value as `overlap / 2`. `engine_ab` over the twenty-four is the proof of
       that, not this comment. */
    const pa = a.pin > 0, pb = b.pin > 0;
    const wa = pa ? 0 : (pb ? 1 : 0.5), wb = pb ? 0 : (pa ? 1 : 0.5);
    const ka = pb ? 2 : 1,              kb = pa ? 2 : 1;
    a.x -= nx * overlap * wa; a.y -= ny * overlap * wa;
    b.x += nx * overlap * wb; b.y += ny * overlap * wb;
    /* A HELD BALL'S VELOCITY IS A MEMORY, NOT A MOTION, AND THE EXCHANGE HAS
       TO READ IT AS ZERO. `pinV` keeps the vector the quarry was captured with
       so it can resume on exactly that -- but it is not TRAVELLING on it, and
       the first build fed it straight into the relative-velocity term here.
       The result was visible and Rick found it in the clip: with the held
       ball's stored vector pointing away from the caster, `p` came out near
       zero or the wrong sign and the caster did not bounce off at all. It
       STUCK to the thing it had just frozen and slid along it.

       Zero when held, untouched otherwise, so this is byte-identical in every
       match without a hold in it. */
    const avx = pa ? 0 : a.vx, avy = pa ? 0 : a.vy;
    const bvx = pb ? 0 : b.vx, bvy = pb ? 0 : b.vy;
    const p0 = (avx - bvx) * nx + (avy - bvy) * ny;
    /* AND ONLY WHEN THEY ARE ACTUALLY APPROACHING. The equal-mass branch
       EXCHANGES normal components whatever the sign, which is its own quirk
       and is left exactly alone -- but doubling that quirk against an
       immovable object drives the caster back INTO the thing it is bouncing
       off, one frame after the other. `p` is `p0` untouched when nobody is
       held, so this is byte-identical in every match without a hold. */
    const p = (pa || pb) ? Math.max(0, p0) : p0;
    if (!pa){ a.vx -= p * nx * ka; a.vy -= p * ny * ka; }
    if (!pb){ b.vx += p * nx * kb; b.vy += p * ny * kb; }'''


EDITS = [
    ("the relic",
     '''    blurb:"Hooked bone, strung on marrow. Nothing it looses is finished with you on the way past." },

];''',
     RELIC_NEW),

    ("fighter state",
     '''    this.ultAegis = null;''',
     FIGHTER_STATE_NEW),

    ("the cast",
     '''    if (u.kind === "ballista"){''',
     FIRE_ULT_NEW),

    ("the hold",
     '''  move(f, foe, dt){
    const P = CONFIG.physics, R = P.ballR;''',
     MOVE_NEW),

    ("tickStasis",
     '''  tickHits(self, foe, dt, cool){''',
     TICK_STASIS_NEW),

    ("the tick call",
     '''    this.tickAegis(dt);''',
     TICK_CALL_NEW),

    ("the blow feeds it",
     '''                shotSpd0: _cs ? (_cs.spd0 || 0) : 0 });
    if (!fatal) foe.takeHitstun(dmg);''',
     HITSTUN_NEW),

    ("the field art",
     '''  _drawAegis(m, f){''',
     DRAW_FIELD_NEW),

    ("the draw call",
     '''    this._drawBalWindow(m, f);''',
     DRAW_CALL_NEW),

    ("the ult voice",
     '''        } else if (w === "bulwarden"){''',
     SFX_ULT_VOICE_NEW),

    ("an immovable ball",
     '''  _ballPair(a, b){
    const R = CONFIG.physics.ballR;
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.hypot(dx, dy);
    if (d >= R * 2 || d === 0) return;
    const nx = dx / d, ny = dy / d, overlap = R * 2 - d;
    a.x -= nx * overlap / 2; a.y -= ny * overlap / 2;
    b.x += nx * overlap / 2; b.y += ny * overlap / 2;
    const p = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny;
    a.vx -= p * nx; a.vy -= p * ny;
    b.vx += p * nx; b.vy += p * ny;''',
     BALLPAIR_NEW),

    ("the fx clock",
     '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,''',
     ULTFX_LIFE_NEW),
]


def one(src: str, old: str, new: str, label: str) -> str:
    # A BUILDER THAT WRITES BROKEN JAVASCRIPT SHOULD SAY SO, NOT HAND IT TO A
    # PROBE THAT TIMES OUT AFTER TWENTY SECONDS WITH A PLAYWRIGHT STACK TRACE.
    # This build shipped an unbalanced `*/` once -- a comment paragraph appended
    # after the block it belonged inside -- and the only signal was the page
    # failing to load. These blocks are almost all prose; the cheapest thing
    # that catches it is counting the delimiters.
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
    ap.add_argument("--src", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--out", default="../02-chain/sc-paradox.html")
    ap.add_argument("--id", default=RELIC_ID)
    ap.add_argument("--name", default=RELIC_NAME)
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--dmg", type=float, default=TUNED_PX)
    for k, v in ULT.items():
        ap.add_argument(f"--{k.lower()}", type=float, default=v)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nRUNIC FLAIL BUILD -- the stasis field")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if '"ballista"' not in s0:
        raise SystemExit("this source has no ballista -- build off sc-marrowdraw or later")
    if '"stasis"' in s0:
        raise SystemExit("this source already has a stasis field -- already built")

    # BUILDERS ECHO WHAT THEY ARE ABOUT TO WRITE, AND SOMEBODY READS IT.
    # v42 rule 6: a `dmgMul` edit was silently eaten by a stale anchor and a
    # 4600-fight bisection ran at the wrong value. The only thing that caught
    # it was this block.
    print(f"  id  {A.id} / {A.name} / {A.ult}     dmg {A.dmg:g}")
    print("  ult " + "  ".join(f"{k} {getattr(A, k.lower()):g}" for k in ULT))

    subs = {"%ID%": A.id, "%NAME%": A.name, "%ULT%": A.ult,
            "%DMG%": f"{A.dmg:g}"}
    for k in ULT:
        subs["%" + k.upper() + "%"] = f"{getattr(A, k.lower()):g}"

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
    print("\n  NEXT, and none of it is optional:")
    print(f"    python3 paradox_relic_probe.py --relic {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40")
    print("    python3 paradox_sweep.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
