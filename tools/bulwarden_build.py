#!/usr/bin/env python3
"""BULWARDEN and AEGIS. The vigil warhammer, and the twenty-third relic.

    python3 bulwarden_build.py --src ../02-chain/sc-vinesower.html \
                               --out ../02-chain/sc-bulwarden.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v41 design document:

    "Bulwark: The ult conjures a shield in front of the ball. the shield
     rotates with the weapon and blocks incoming damage. it also reflects a
     portion of the damage it blocked back to its attacker"

Three forks it left open, all three settled by him:

    NAME     Bulwark is already Lightkeeper's ultimate. He left Lightkeeper
             alone; the ult is AEGIS and the relic is BULWARDEN.
    HP       the shield is made of the BANKED WARD, plus a floor so a cast is
             never dead.
    ARC      it rides the head's side -- the literal reading of "in front of
             the ball" and "rotates with the weapon".

## WHY THIS IS THE ANSWER TO WHAT THE SURVEY MEASURED

`wh_survey.py` found the warhammer's own thesis and it is a problem:
**the 2.3x knockback throws the quarry +22 units off a 76 reach**, costing 12%
of its contacts and 16 points of win rate -- unless the ultimate takes the
shove back. Grudgebearer's Crucible pulls and is paid +7% for carrying it.
Censer's Consecration knocks and is still down 17%. Same type, same shove,
opposite ultimates, opposite sign.

Aegis is a third answer and it is neither: **it does not fix the reach, it
stops needing it.** For a duration the relic has a damage channel that pays out
when the foe comes to IT -- a blow arriving on the arc is damage the hammer
never had to reach for.

## What the engine gives free

`spendWard()` already exists and is already not `shatter()` with a flag -- it
consumes the pool and returns it, and Reprisal already spends it as damage on
one shot. Aegis spends the same pool as a WALL. `f.spendFx` and `f.spendA`
already animate the plates leaving the shell along a bearing, so the wall is
visibly made of the armour that was on the ball a frame earlier.

Every projectile in the game resolves through `resolveHit`, so "blocks incoming
damage" catches a bow's arrow and a hammer's swing with one branch. Four bow
relics exist and none of them needed a special case.

## The one thing that had to be invented

**A DIRECTION.** Every existing defence in this game is a POOL -- ward, and
nothing else -- and a pool does not care where the blow came from. Aegis is
decided at the CONTACT POINT: the angle from the victim's centre to `(hx, hy)`
against the victim's own `theta`, which is the same quantity `bladeSegments`
builds its segments from. `resolveHit` is the only place in the engine that
knows where a blow landed, which is why the branch is there and not in
`hurt()`.

## The zero-burden argument, kept structurally

    ALL STATE IS `f.ultAegis`, WHICH IS null ON EVERY OTHER RELIC.

`tickAegis` returns on its first line when neither fighter has one, the branch
in `resolveHit` is one `if (foe.ultAegis)`, and `_drawAegis` returns on its
first line. `engine_ab` over the twenty-two pre-existing ids is the proof, not
this paragraph.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `dur`, `floor`, `bankMul`, `arc`, `r` and `reflect` are unset in the
design and cannot be guessed. `arc` and `reflect` are not independent: a wide
arc that reflects hard is a relic that wins by being hit, and being hit is the
one thing this type does easily. `bulwarden_sweep.py` solves them jointly and
is the next thing after the probe.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC_ID = "bulwarden"
# BULWARDEN. Rick's, from four offered. Bulwark and warden: the wall, and the
# one who keeps it -- and it keeps the word he reached for first in §1 without
# taking it off Lightkeeper, which is a chain-wide rename touching 01-live.
# It lands in the -en/-er agent register the roster runs on and, specifically,
# in the register vigil already owns (Lightkeeper, Farwarden).
#
# THE ID MATCHES THE NAME. `oathwound`/Goreshard and `redflail`/Threshmaw are
# the two existing drifts in this roster and both are traps; a third was not
# worth the twenty minutes it takes to avoid.
RELIC_NAME = "Bulwarden"
ULT_NAME = "Aegis"

# PLACEHOLDER. The type ships 27.93 (Grudgebearer) and 28.77 (Censer), and
# wh_survey measured the vigil channel on this type at 77% win against a 52%
# control -- so this number comes DOWN and it is bisected by the sweep, never
# chosen here.
TUNED_BW = 20.1

# EVERY ONE OF THESE IS A PLACEHOLDER.
ULT = {
    # Grudgebearer 18, Censer 15. A defensive ultimate that does not resolve
    # into damage should not be the cheapest thing on the type.
    "charge":  16.0,
    # How long the wall stands. Long enough that the 3.9s revolution of this
    # weapon happens at least twice under it, or "it rotates with the weapon"
    # is a sentence the viewer never gets to see.
    "dur":      9.0,
    # The guaranteed hp, so a cast on an empty plate is never dead. wh_survey:
    # the pool sits at a mean of 14.3 and reaches its 90 cap 0.6% of the time.
    "floor":   40.0,
    # What a banked point is worth as wall.
    "bankMul":  1.0,
    # THE WHOLE FEEL OF THE RELIC IS IN THIS NUMBER. 1.5 rad is 86 degrees --
    # a quarter of the circle, swept in 0.94s at spin 1.6.
    "arc":      2.8,
    # How far in front of the shell it rides, as an offset on ballR (34). The
    # ward's own plates are at R+17; this sits just outside them, and inside
    # the radius a contact lands at (R + width*0.5 = R+13) plus a margin, so
    # the blow it stops and the thing that stops it are in the same place.
    "r":       26.0,
    # The share handed back. 0.40 is STATUS.ward.shatter's own number, which
    # is a rhyme rather than an argument -- sweep it.
    "reflect":  0.6,
    # HOW FAR THE SHIELD IS BENT AROUND THE BALL. 0 is a flat kite, 1 wraps
    # it onto the circle it is defending.
    #
    # THIS IS A REAL TRADE AND IT CANNOT BE ARGUED AWAY. A FLAT shape of arc
    # length La at radius rr subtends 2*atan(La/2/rr) -- at rr 60 a 110-unit
    # kite covers about 85 degrees and no more, however long it is drawn. So a
    # flat kite is unmistakably a kite and cannot honestly cover a wide arc;
    # a fully bent one covers exactly `arc` by construction and reads as a
    # curved barrier rather than a kite. Anything between draws a picture
    # narrower than the hitbox it belongs to.
    "bend":     0.0,
    # THE ANGULAR WIDTH OF THE DRAWN SHIELD, which is DELIBERATELY NARROWER
    # than `arc`. Rick's call, made against the picture, with the cost stated:
    # a flat kite at this radius cannot subtend more than about 85 degrees
    # however long it is drawn, and he wanted the kite AND the coverage. So the
    # shield draws at `artArc` and blocks at `arc`, and blows that visibly miss
    # it are stopped by it. It is the one place in this build where the picture
    # is not the mechanic, and it is recorded here rather than discovered
    # later. bulwarden_probe [4] asserts the gap is the size it is supposed to
    # be, so it can never drift unnoticed.
    "artArc":   1.5,
    # WHAT A LANDED BLOW PUTS BACK INTO THE WALL, as a multiplier on the ward
    # bank. Rick, after the sweep found the magazine was mostly floor: "feed
    # the wall while it stands."
    #
    # THE MEASUREMENT THAT FORCED IT: over 88 casts the plate held a MEDIAN OF
    # ZERO at the moment of the cast -- mean 8.4 of a 90 cap -- because
    # `STATUS.ward.dur` is 5s and the plate expires four times a fight while
    # the ultimate fires on a charge timer that knows nothing about it. The
    # relic banks real armour (peak 44 a fight) and simply never happens to be
    # holding any when it casts. So the bank goes into the WALL while the wall
    # is up, the 5s clock stops mattering, and the ultimate rewards the one
    # thing wh_survey says this type is worst at: landing contacts.
    "feed":     2.0,
    # HOW FAST THE WALL COMES ROUND, rad/s. Rick, after the probe refuted the
    # first geometry: "the shield tracks the enemy ball and always tries to
    # face them." TRIES is the load-bearing word -- the turn is RATE LIMITED,
    # so a quarry moving faster than this gets round the edge and the
    # counterplay is something a viewer can see rather than arithmetic. The
    # weapon itself turns at 1.6.
    #
    # WHY TRACKING AND NOT `theta`. §1's first geometry rode the weapon.
    # Measured over 531 incoming blows and six foes: blows arrive a mean of
    # 1.98 rad from where the weapon points, because a weapon pointing AT the
    # attacker CLANKS instead of being hit -- and this type wins 734 of 734
    # binds. A 1.5 rad arc on the head's side caught 6.0% of incoming blows
    # against 23.9% for a randomly pointed one: the hammer was guarding the
    # one side it already guards. bulwarden_probe.py [7].
    "turn":     3.0,
}


# ---------------------------------------------------------------- THE RELIC --

RELIC_NEW = '''    blurb:"A branch bent living and never let go. What it misses with takes root where it lands." },

  /* BULWARDEN -- the vigil warhammer, and the twenty-third relic. The cell is
     the double gap: vigil was the thinnest school at 2 of 6 and the warhammer
     the thinnest type at 2 of 6, and wh_survey.py priced all five open cells
     on the row before this one was chosen.

     Physics are Grudgebearer's and Censer's exactly -- all three warhammers
     now share one block byte for byte and the TYPE owns it. The school owns
     Ward and the rose, and SHAPES.warhammer's vigil branch has drawn this
     relic since before it existed.

     `dmg` and every number under `ult` are PLACEHOLDERS -- bulwarden_build's
     TUNED_BW and ULT -- and MUST be swept. `onSelf.ward`'s value is a per-relic
     BANK MULTIPLIER, and on this relic it is also the ultimate's magazine. */
  { id:"%ID%", name:"%NAME%", aff:"vigil", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:%DMG%, spin:1.6, mode:"spin", mass:5.0, knockMul:2.3,
    onSelf:{ ward:1 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"aegis",
          dur:%DUR%, floor:%FLOOR%, bankMul:%BANKMUL%,
          arc:%ARC%, r:%R%, reflect:%REFLECT%, turn:%TURN%, feed:%FEED%,
          bend:%BEND%, artArc:%ARTARC%,
          /* THE NUMBER IN THE TIP IS SUBSTITUTED, not typed -- v40 shipped a
             card reading "5s" after the sweep moved the number to 8.1 and
             nothing caught it, because verify.py only asks that a tip EXISTS. */
          /* RICK'S LINE, VERBATIM. Asked for the first time in twenty-three
             relics -- the v40 handoff's rule 2 names the scrunch wording and
             it had never once been put to him. It carries NO NUMBER, which is
             his call and not an oversight: bulwarden_probe [1] asserts that
             IF a percentage appears in an ult tip it must equal the weapon's
             own field, so this line is guarded and so is any later edit that
             puts a number back into it. */
          tip:"Raises a shield that reflects damage blocked" },
    blurb:"Every plate it banks it can raise as a wall. What the wall stops, it hands back." },

];'''


# ------------------------------------------------------------- THE STATE --

FIGHTER_STATE_NEW = '''    /* {t, dur, hp, hp0, flash} while Aegis stands. null on every other relic,
       which is the whole zero-burden argument: tickAegis returns on its first
       line, _drawAegis returns on its first line, and the branch in
       resolveHit is one `if (foe.ultAegis)`. */
    this.ultAegis = null;
    this.ultSlag = null;      // {t, fuse, split} while a Slagburst fuse burns'''


# --------------------------------------------------------------- THE CAST --

FIRE_ULT_NEW = '''    if (u.kind === "spinstorm"){
      f.ultSpin = { phase: "wind", t: 0, stun: 0, acc: 0, n: 0, peak: 0, chuff: 0 };
    }

    /* AEGIS RAISES A WALL AND RESOLVES NOTHING. Rick: "The ult conjures a
       shield in front of the ball."

       THE WALL IS MADE OF THE PLATE. `spendWard` is the ward's third ending
       and the only one the relic chooses -- it consumes the pool and hands the
       number back without bursting it at the holder or flinging anybody, which
       is exactly what is wanted here and is why Reprisal's precedent is worth
       having. `f.spendFx` and `f.spendA` are the animation that already
       exists: the plates detach as a ring, accelerate along a bearing and
       tighten as they go. Fired along `f.theta`, they arrive exactly where the
       wall is about to stand. The viewer sees the armour leave the ball and
       become the shield, with nothing to caption.

       THE FLOOR IS NOT A KINDNESS, it is the difference between an ultimate
       and a downward spiral. A relic that is not landing blows has banked
       nothing, and a relic that has banked nothing would get an empty cast
       exactly when it most needs the wall. */
    if (u.kind === "aegis"){
      const pool = this.spendWard ? this.spendWard(f) : 0;
      if (pool > 0){ f.spendFx = 1; f.spendA = f.theta; }
      const hp = Math.round(u.floor + pool * u.bankMul);
      /* IT ARRIVES ALREADY FACING. A wall conjured pointing the wrong way and
         then swinging round would spend its first half second being useless
         for a reason the viewer cannot see. `ang` is the shield's OWN angle
         from here on -- the weapon's `theta` is not read by this mechanic
         again. */
      f.ultAegis = { t: 0, dur: u.dur, hp, hp0: hp, flash: 0, mend: 0,
                     ate: 0, back: 0, fed: 0,
                     ang: Math.atan2(foe.y - f.y, foe.x - f.x) };
      /* NORMAL path: the fx clock runs at 2x sim time, and this set-piece has
         to still be on screen for the whole window the way the Thicket's does
         -- the map entry below is only the fallback if this line is missed. */
      this.ultFx.life = (u.dur + 0.5) * 2;
      this.note(`${f.w.name} — ${u.name} raises ${hp}`);
      return;
    }'''

TICK_CALL_NEW = '''    this.tickVines(dt);
    /* BEFORE the hit loops and after everything that moves: the wall's clock
       has to be current on the frame a blow arrives at it, and the wall's
       ANGLE is read live off `theta` at the contact rather than stored here,
       so there is nothing to keep in sync. */
    this.tickAegis(dt);
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);'''

TICK_AEGIS_NEW = '''  /* ---------------------------------------------------------------- AEGIS --
     The clock and nothing else. The wall has no position of its own: it is an
     ARC ON `theta`, recomputed at the point of contact and at the point of
     draw, so a stunned fighter's wall stops where its weapon stopped and a
     spinning one's sweeps -- both for free, and neither as a special case.

     Returns on its first line in every match that does not contain this
     relic. */
  tickAegis(dt){
    if (!this.a.ultAegis && !this.b.ultAegis) return;
    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const A = f.ultAegis;
      if (!A) continue;
      A.t += dt;
      if (A.flash > 0) A.flash = Math.max(0, A.flash - dt * 4.5);
      if (A.mend  > 0) A.mend  = Math.max(0, A.mend  - dt * 3.0);
      /* THE TRACKING. Rick: "the shield tracks the enemy ball and always tries
         to face them." Rate limited, and the rate is the entire counterplay:
         at `turn` the wall covers a quarry that closes and holds, and loses
         the edge of its arc to one that crosses fast. A quarry that has just
         been thrown 483 units by a shatter is moving fast. */
      const want = Math.atan2(foe.y - f.y, foe.x - f.x);
      const d = angDiff(A.ang, want), step = f.w.ult.turn * dt;
      A.ang += Math.abs(d) <= step ? d : Math.sign(d) * step;
      /* EXPIRY IS NOT A BREAK, and the distinction is the ward's own -- see
         STATUS.ward's note. A wall that runs out has held; a wall that is
         broken through has failed. Only one of them makes a noise. */
      if (A.t >= A.dur) f.ultAegis = null;
    }
  }

  tickHits(self, foe, dt, cool){'''


# ---------------------------------------------------------------- THE BLOCK --

BLOCK_NEW = '''    dmg = Math.round(dmg);

    /* ---- AEGIS. THE FIRST DEFENCE IN THIS GAME WITH A DIRECTION.
       Rick: "the shield rotates with the weapon and blocks incoming damage.
       it also reflects a portion of the damage it blocked back to its
       attacker."

       WHY IT IS HERE AND NOT IN hurt(). A pool does not care where a blow came
       from and `hurt` is handed a number, not a place. `resolveHit` is the only
       function in the engine that knows where a blow LANDED, and every
       projectile in the game routes through it -- so an arrow and a swing are
       stopped by the same four lines and the four bow relics needed no special
       case.

       THE TEST is the angle from the victim's own centre to the contact point,
       against the victim's own `theta`. That is the same quantity
       bladeSegments builds its segments from, so the wall and the weapon can
       never disagree about which way this relic is facing.

       WHAT IT DOES NOT STOP: status. The plate has always let `onHit` through
       -- `hurt` gates damage and nothing else -- and a wall that also stripped
       hemorrhage would be a second rule for the same school. Damage-over-time
       goes under both, by design. */
    if (foe.ultAegis && dmg > 0){
      const A = foe.ultAegis, U = foe.w.ult;
      const rel = Math.abs(angDiff(Math.atan2(hy - foe.y, hx - foe.x), A.ang));
      if (rel <= U.arc * 0.5){
        const eaten = Math.min(A.hp, dmg);
        A.hp -= eaten; dmg -= eaten;
        A.flash = 1; A.ate += eaten;
        /* THE RETURN. Handed back through hurt() so it respects whatever the
           attacker is standing behind -- a vigil mirror is a real fight and
           not a special case. It is a RETURN, NOT A BLOW: no crit roll, no
           onHit, no knockback, no hit-stun, and it cannot trigger a latch or a
           forge, because none of those are reached from here. */
        const back = Math.round(eaten * U.reflect);
        if (back > 0){
          A.back += back;
          const wasUp = self.hp > 0;
          this.hurt(self, back, foe);
          self.flash = 1; self.ringFlash = 1;
          this.float(self.x, self.y - 46, back, AFFINITIES.vigil.glow,
                     26 + back * 0.6);
          /* A FATAL RETURN FILES A BEAT, and nothing else here does.

             This is the Thicket's rule and it is here for the same reason,
             found the same way -- off a clip that had no ending. `hurt` files
             no beat, so a fight decided by the shield handing a blow back was
             invisible to the director: `cinePlan` returned a cut list with no
             KILL in it and cinema_clip fell back to "the last cut", which on
             one seed was 1.7 seconds into a 42-second fight.

             The ORDINARY return stays silent on purpose. It is two events a
             cast, and it is not a blow this relic struck -- filing it would
             have the camera cut to a moment where the caster did nothing. The
             FATAL one is the fight ending, and "do not let a side-channel
             drive the camera" is a different claim from "do not film the
             finish". How often it decides a fight is measured in
             bulwarden_probe [6] rather than assumed here. */
          if (wasUp && self.hp <= 0)
            this.beat({ kind: "hit", side: foe === this.a ? 0 : 1,
                        x: self.x, y: self.y, dmg: back, crit: false,
                        fatal: true, hpAfter: 0,
                        hpFrac: 0, maxHp: self.maxHp,
                        selfHpFrac: foe.hp / foe.maxHp,
                        spd: self.speed, foeSpd: foe.speed,
                        close: Math.hypot(self.vx - foe.vx, self.vy - foe.vy),
                        ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                        shotSpd0: 0 });
        }
        this.ring(hx, hy, AFFINITIES.vigil.glow, 5, 116, 0.34, 6);
        this.spawnFx(hx, hy, AFFINITIES.vigil.core, 14, 260, 0.42, 4);
        this.hitStop = Math.max(this.hitStop, 0.05);
        this.shake = Math.min(38, this.shake + 8);
        SFX.play("aegis", { n: eaten, back });
        if (A.hp <= 0){
          foe.ultAegis = null;
          this.ring(foe.x, foe.y, AFFINITIES.vigil.core, 7, 210, 0.52, 7);
          this.spawnFx(foe.x, foe.y, AFFINITIES.vigil.glow, 34, 380, 0.7, 5);
          SFX.play("aegis", { broke: true });
          this.note(`${foe.w.name} — the wall gives`);
        }
      }
    }

    this.hurt(foe, dmg, self);'''


# ----------------------------------------------------------------- THE ART --

DRAW_AEGIS_NEW = '''  /* THE SHIELD. Rick, on the first pass: "we are way off base here art wise.
     Id like to see an actual shield. a floating pink kiteshield."

     The first cut drew the ward's own five plates, off the shell and out in
     front, and the argument for it was continuity. That is an argument about
     where the wall CAME FROM and it cost the thing the wall IS: an object,
     conjured, floating, and it should look like one.

     THE SHIELD IS CURVED, AND THAT IS FORCED RATHER THAN CHOSEN. A FLAT shape
     of length L sitting at radius `rr` subtends 2*atan(L/2/rr) -- at rr 60 a
     110-unit kite covers about 85 degrees and no more, however long it is
     drawn. The block test covers `arc`, and at 2.8 rad that is 160 degrees.
     A flat kite cannot honestly cover it, so the kite is BENT around the
     circle it is defending: the path is built in (angle, depth) and mapped out
     to polar, which makes the silhouette and the hitbox the same object by
     construction rather than by eye. Real kite shields were bowed anyway.

     THE READS, three things a viewer takes at a glance with no number on
     screen:

       IT IS A SHIELD      the kite. A flat top with two corners, straight
                           shoulders, a taper, a point. A boss and two rivets.
       WHICH WAY           the point trails, so the shape states the bearing.
       HOW MUCH IS LEFT    the face DRAINS FROM THE TOP -- a wedge clipped to
                           the shield, retreating toward the point. The glass
                           vessel's own grammar, one object over.

     It floats: a slow bob on the radius and a slower rock on the angle, both
     off `m.t`, neither read by anything. A conjured thing that sat perfectly
     still would read as bolted on. */
  _drawAegis(m, f){
    const A = f.ultAegis;
    if (!A) return;
    const c = this.ctx, R = CONFIG.physics.ballR, P = AFFINITIES.vigil;
    const U = f.w.ult;
    const frac = clamp(A.hp / Math.max(1, A.hp0), 0, 1);
    const fade = clamp((A.dur - A.t) / 0.5, 0, 1);
    const bob  = Math.sin(m.t * 2.6) * 2.2;
    const rock = Math.sin(m.t * 1.7 + 1.1) * 0.045;
    const rr = R + U.r + bob;
    const EDGE = "#1A0512";
    const N = 30;

    /* `s` runs 0 at the top edge to 1 at the point; `d` is radial depth. The
       taper is flat for the first third and then runs into the point, which is
       the profile that separates a kite from a leaf. */
    const prof = (s) => {
      /* the corners come off the top edge, and the taper starts late -- a
         point that starts at a third of the way down is a spearhead, and the
         difference between a shield and a spearhead is where the shoulders
         end */
      const top  = s < 0.07 ? 0.90 + 0.10 * (s / 0.07) : 1;
      const body = s <= 0.46 ? 1 : Math.pow(1 - (s - 0.46) / 0.54, 0.9);
      return Math.min(top, body);
    };
    /* THE DRAWN WIDTH IS NOT THE BLOCKED WIDTH. See `artArc` in the
       builder: a flat kite cannot subtend `arc`, and the kite is what was
       asked for. Everything below is in `AA`. */
    const AA = U.artArc || U.arc;
    const ang0 = -AA / 2;
    const bend = U.bend === undefined ? 1 : U.bend;
    /* LENGTH AND DEPTH BOTH MOVE WITH THE BEND, because a kite and a barrier
       are not the same object at different curvatures -- they are different
       proportions. Flat, the shield is the CHORD its arc subtends and 1.6:1,
       which is a kite. Wrapped, it is the ARC LENGTH and much shallower,
       because a 1.6:1 shape bent through 160 degrees would reach from inside
       the ball to twice its own radius. */
    const Lflat = 2 * rr * Math.sin(AA / 2);
    const Lwrap = rr * AA;
    const La = Lflat + (Lwrap - Lflat) * bend;
    const Dflat = Lflat * 0.62;
    const Dwrap = Math.min(rr * 0.55, Lwrap * 0.34);
    const D = Dflat + (Dwrap - Dflat) * bend;
    /* ONE KNOB BETWEEN TWO HONEST PICTURES. At bend 1 the point is placed in
       polar and the silhouette subtends `arc` exactly; at bend 0 the same
       profile is laid out flat and subtends 2*atan(La/2/rr), which is less.
       The two are LERPED rather than branched so there is one path to read and
       one shape to debug. */
    const pt = (s, d) => {
      const phi = ang0 + s * AA, rad = rr + d;
      const cx = Math.cos(phi) * rad, cy = Math.sin(phi) * rad;
      const fx = rr + d,              fy = (s - 0.5) * La;
      return [fx + (cx - fx) * bend, fy + (cy - fy) * bend];
    };
    const kite = (k) => {
      const h = D * 0.5 * k;
      c.beginPath();
      let q = pt(0, h * prof(0)); c.moveTo(q[0], q[1]);
      for (let i = 1; i <= N; i++){ const s = i / N; q = pt(s,  h * prof(s)); c.lineTo(q[0], q[1]); }
      for (let i = N - 1; i >= 0; i--){ const s = i / N; q = pt(s, -h * prof(s)); c.lineTo(q[0], q[1]); }
      c.closePath();
    };

    c.save();
    c.globalAlpha = fade;
    c.translate(f.x, f.y);
    c.rotate(A.ang + rock);

    c.shadowBlur = 0;
    kite(1); c.fillStyle = EDGE; c.fill();
    c.lineWidth = 5; c.strokeStyle = EDGE; c.stroke();
    kite(1); c.fillStyle = P.dark; c.fill();

    /* WHAT IS LEFT. A wedge retreating toward the point, clipped INSIDE the
       rim rather than to the whole outline -- the shield keeps a border of
       `dark` at every level and never becomes one flat pink shape. The first
       cut filled edge to edge and read as an eye. */
    if (frac > 0){
      c.save(); kite(0.86); c.clip();
      /* the surviving part, walked in the SAME mapped space as the outline, so
         the fill follows the shield whether it is flat or bent */
      const s0 = 1 - frac;
      c.beginPath();
      let q = pt(s0, -D); c.moveTo(q[0], q[1]);
      q = pt(s0, D); c.lineTo(q[0], q[1]);
      for (let i = 1; i <= N; i++){
        const s = s0 + (1 - s0) * (i / N);
        q = pt(s, D); c.lineTo(q[0], q[1]);
      }
      for (let i = N; i >= 0; i--){
        const s = s0 + (1 - s0) * (i / N);
        q = pt(s, -D); c.lineTo(q[0], q[1]);
      }
      c.closePath();
      c.fillStyle = P.core; c.fill();
      c.restore();
    }

    /* THE STRAPS. Two lines from the shoulders into the point. They are what
       stop a silhouette this simple reading as a petal: a shield is a made
       object and it should look built. */
    c.lineWidth = 1.8;
    c.strokeStyle = SHAPES._shade(P.dark, 0.58, 0.06);
    for (const sg of [-1, 1]){
      c.beginPath();
      let q = pt(0.10, sg * D * 0.30); c.moveTo(q[0], q[1]);
      for (let i = 1; i <= 12; i++){
        const s = 0.10 + (0.78 * i / 12);
        q = pt(s, sg * D * 0.30 * (1 - i / 12));
        c.lineTo(q[0], q[1]);
      }
      c.stroke();
    }

    /* the rim */
    kite(1);
    c.lineWidth = 2.6; c.strokeStyle = P.glow;
    c.shadowColor = P.core; c.shadowBlur = 13; c.stroke();
    c.shadowBlur = 0;
    /* the bevel: the same outline drawn in, which is what turns a flat fill
       into a face with an edge on it */
    kite(0.80);
    c.lineWidth = 1.4; c.strokeStyle = SHAPES._shade(P.dark, 0.62, 0.08); c.stroke();

    /* THE BOSS, and it does not drain -- it is the shield being HELD, and it
       goes out only when the shield does. Two rivets at the top corners so the
       flat edge has something for the eye to catch at 1:1. */
    let b = pt(0.24, 0);
    c.beginPath(); c.arc(b[0], b[1], D * 0.20, 0, TAU);
    c.fillStyle = EDGE; c.fill();
    c.beginPath(); c.arc(b[0], b[1], D * 0.148, 0, TAU);
    c.fillStyle = P.glow; c.fill();
    for (const sg of [-1, 1]){
      const q = pt(0.055, sg * D * 0.31);
      c.beginPath(); c.arc(q[0], q[1], D * 0.062, 0, TAU);
      c.fillStyle = EDGE; c.fill();
    }

    /* THE MEND. The rim runs bright for a moment when a landed blow puts
       something back -- the opposite motion to a block, and on the RIM rather
       than the face so the two can never be confused at a glance. */
    if (A.mend > 0){
      c.globalAlpha = fade * A.mend * 0.8;
      kite(1);
      c.lineWidth = 4.5; c.strokeStyle = P.glow;
      c.shadowColor = P.glow; c.shadowBlur = 22; c.stroke();
      c.shadowBlur = 0; c.globalAlpha = fade;
    }

    /* THE BLOCK. The whole face lights, not the spot that was hit: what the
       viewer needs is "that was stopped", and a local flash on an object this
       size at 1:1 is two pixels of information. */
    if (A.flash > 0){
      c.globalAlpha = fade * A.flash * 0.9;
      c.globalCompositeOperation = "lighter";
      kite(1); c.fillStyle = "#FFFFFF"; c.fill();
      c.lineWidth = 6; c.strokeStyle = P.glow;
      c.shadowColor = P.glow; c.shadowBlur = 30; c.stroke();
    }
    c.restore();
  }

  drawStatus(m, f){'''


DRAW_CALL_NEW = '''    this.drawStatus(m, f);
    /* OVER the status plates and over the shell: the wall is in front of the
       ball, and a wall drawn under the armour it was made of is a wall the
       viewer reads as being inside the ball. */
    this._drawAegis(m, f);'''


# ---------------------------------------------------------------- THE SOUND --

SFX_AEGIS_NEW = '''      else if (kind === "aegis"){
        /* A STOPPED BLOW IS NOT A HIT AND MUST NOT SOUND LIKE ONE. The whole
           point of this relic is that a thing which would have hurt did not,
           so the sound is a dead stop rather than a strike: a hard short
           transient with the ring taken OFF it, on a body that is bright and
           metallic instead of woody. `clank` is the nearest neighbour in the
           game and is deliberately avoided -- a clank is two weapons agreeing,
           this is one of them being refused.

           The RETURN is the second half and it is a rising tail, because the
           damage is going the other way. It scales with what came back, so a
           big block and a scratch are not the same event. */
        if (p && p.broke){
          /* the wall failing: the same plates as a shatter, but nobody is
             flung, so it is a collapse rather than a burst -- pitched DOWN */
          this._burst(t, { freq: 2600, q: 0.8, gain: 0.20, dur: 0.09, type:"highpass" });
          this._tone (t, { freq: 520, to: 96, gain: 0.20, dur: 0.42, type:"square" });
          this._tone (t + 0.05, { freq: 300, to: 62, gain: 0.13, dur: 0.40, type:"sawtooth" });
          this._burst(t + 0.02, { freq: 420, q: 0.6, gain: 0.14, dur: 0.44, type:"lowpass" });
        } else {
          const n = Math.min(60, (p && p.n) || 1);
          const bk = Math.min(40, (p && p.back) || 0);
          this._burst(t, { freq: 3200 + n * 12, q: 1.4, gain: 0.16, dur: 0.030, type:"bandpass" });
          this._tone (t, { freq: 880 + n * 4, to: 660, gain: 0.13, dur: 0.055, type:"square" });
          this._tone (t, { freq: 132, to: 108, gain: 0.11, dur: 0.09, type:"sine" });
          if (bk > 0){
            this._tone (t + 0.05, { freq: 330, to: 330 + bk * 14, gain: 0.06 + bk * 0.002,
                                    dur: 0.20, type:"triangle" });
            this._burst(t + 0.05, { freq: 1800 + bk * 40, q: 1.8, gain: 0.05, dur: 0.20, type:"bandpass" });
          }
        }
      }
      else if (kind === "vine"){'''

SFX_ULT_VOICE_NEW = '''        } else if (w === "%ID%"){              // a hall door closing
          /* Not a blast and not a chime. Something heavy is set down between
             the caster and the fight: a low fall with a metal plate landing on
             top of it, then a long ring that does NOT rise -- the wall is up
             and it stays up, and a rising tail would promise something about
             to happen. The plates leaving the shell are the picture; this is
             the weight of them arriving. */
          this._tone (t, { freq: 140, to: 62, gain: 0.26, dur: 0.42, type:"sine" });
          this._burst(t, { freq: 300, q: 0.7, gain: 0.20, dur: 0.30, type:"lowpass" });
          this._burst(t + 0.07, { freq: 2200, q: 1.1, gain: 0.16, dur: 0.10, type:"bandpass" });
          this._tone (t + 0.07, { freq: 392, to: 392, gain: 0.13, dur: 0.75, type:"triangle" });
          this._tone (t + 0.09, { freq: 588, to: 588, gain: 0.07, dur: 0.70, type:"triangle" });
          this._burst(t + 0.30, { freq: 900, q: 0.8, gain: 0.05, dur: 0.60, type:"lowpass" });
        } else if (w === "vinesower"){         // a bowstring, then a field of it'''

ULTFX_LIFE_NEW = '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
              /* AEGIS is set from `ult.dur` at the cast site, the way the
                 Thicket is. This entry is the fallback if that is ever
                 missed. */
              %ID%: %FXLIFE%,'''


FEED_NEW = '''    for (const [k, n] of Object.entries(self.w.onSelf || {})){
      if (k !== "ward"){ self.apply(k, n); continue; }
      const W = STATUS.ward;
      /* THE WALL IS FED WHILE IT STANDS. Rick: "feed the wall while it
         stands." Same channel, same 0.55 share of what was just dealt, a
         different destination -- and the plate gets NOTHING while the wall is
         up, which is the cost: a relic comes out of its own ultimate with no
         armour on the shell.

         WHY IT HAD TO EXIST. `STATUS.ward.dur` is 5 seconds and the plate
         expires four times a fight, so a charge timer that knows nothing about
         the plate casts on an empty one more often than not: measured, the
         pool at the cast is a MEDIAN OF ZERO over 88 casts. "Made of what you
         banked" was 80% floor. This makes the bank continuous instead of
         instantaneous, and the 5s clock stops being able to erase it.

         REPAIR, NOT GROWTH. Capped at what the wall was raised at, because the
         face draws its fill against `hp0` -- a wall that could exceed its own
         gauge would show full while it grew and the viewer would lose the one
         read that matters. */
      if (self.ultAegis){
        const A = self.ultAegis, u = self.w.ult;
        const was = A.hp;
        /* `=== undefined` and not `|| 1`: a feed of ZERO is a legitimate
           setting and the sweep has to be able to ask for it. The first cut
           wrote `u.feed || 1` and every control run in the sweep silently
           measured a feed of 1 instead of none -- two configurations came back
           byte-identical across 100 fights, which is what caught it. */
        const fd = u.feed === undefined ? 1 : u.feed;
        A.hp = Math.min(A.hp0, A.hp + dmg * W.bank * n * fd);
        const got = Math.round(A.hp - was);
        if (got >= 1){
          A.mend = 1;
          this.float(self.x, self.y - 52, "+" + got, AFFINITIES.vigil.glow,
                     20 + got * 0.5);
        }
        continue;
      }
      const before = self.shield;'''


SETPIECE_NEW = '''    /* ---- AEGIS, over ---------------------------------------------------
       Rick: "give it a proper set-piece." The first cut had none -- the ward's
       existing spend animation threw the plates forward and the shield was
       simply there -- and understatement is the wrong instinct for the one
       moment in a defensive ultimate that is an EVENT.

       What it says, in order, and it is the mechanic rather than a flourish:

         THE CALL      a ring leaves the shell. The armour is being spent.
         THE PLATES    five of them, the ward's own count, spiralling out of
                       the ball and converging on the bearing to the quarry.
                       They arrive where the shield stands, so the viewer sees
                       the shield being MADE OF the plate rather than replacing
                       it.
         THE LOCK      a hard white ring at the shield's own position on the
                       last fifth. The wall is up.

       Drawn from the LIVE fighter and its live `ultAegis.ang`, not from the
       frozen cast record: the ball moves and the wall tracks, and a set-piece
       drawn from a copy describes a fight that has moved on -- the same reason
       `_retraceField` reads `f.ultTrace`. Gated on `u.t` and not on `k`,
       because this fx block deliberately outlives the conjure by the whole
       nine-second window. */
    if (u.w === "%ID%"){
      const CONJ = 1.7;                    // fx seconds; the fx clock runs 2x
      const t = u.t;
      if (t < CONJ && src && src.alive){
        const P = AFFINITIES.vigil, R0 = CONFIG.physics.ballR;
        const A2 = src.ultAegis;
        const ang = A2 ? A2.ang : Math.atan2(u.ty - u.y, u.tx - u.x);
        const kk = clamp(t / CONJ, 0, 1);
        const sx = src.x, sy = src.y, rr = R0 + (src.w.ult.r || 22);
        c.globalCompositeOperation = "lighter";

        c.globalAlpha = (1 - kk) * 0.7;
        c.strokeStyle = P.glow; c.lineWidth = 6 * (1 - kk) + 1;
        c.shadowColor = P.core; c.shadowBlur = 22 * (1 - kk);
        c.beginPath(); c.arc(sx, sy, R0 * 1.1 + kk * 190, 0, TAU); c.stroke();

        c.shadowBlur = 0;
        for (let i = 0; i < 5; i++){
          const ph = clamp((t - i * 0.085) / (CONJ * 0.72), 0, 1);
          if (ph <= 0) continue;
          const a2 = ang + (i / 4 - 0.5) * 1.5 * (1 - ph) + (1 - ph) * 1.25;
          const rad = R0 + (rr - R0 + 26) * ph + (1 - ph) * 66;
          const px = sx + Math.cos(a2) * rad, py = sy + Math.sin(a2) * rad;
          c.globalAlpha = Math.min(1, ph * 1.7) * (1 - Math.pow(ph, 6)) * 0.9;
          c.fillStyle = P.core;
          c.save(); c.translate(px, py); c.rotate(a2 + Math.PI / 2);
          c.fillRect(-11 * ph - 3, -3.5, 22 * ph + 6, 7);
          c.restore();
        }

        if (t > CONJ * 0.78){
          const lk = clamp((t - CONJ * 0.78) / (CONJ * 0.22), 0, 1);
          const lx = sx + Math.cos(ang) * rr, ly = sy + Math.sin(ang) * rr;
          c.globalAlpha = (1 - lk) * 0.9;
          c.strokeStyle = "#FFFFFF"; c.lineWidth = 5 * (1 - lk) + 1;
          c.shadowColor = P.glow; c.shadowBlur = 26 * (1 - lk);
          c.beginPath(); c.arc(lx, ly, 12 + lk * 96, 0, TAU); c.stroke();
        }
        c.globalCompositeOperation = "source-over";
        c.shadowBlur = 0; c.globalAlpha = 1;
      }
    }

    /* ---- THE HARROWING, over -------------------------------------------'''


EDITS = [
    ("the relic",
     '''    blurb:"A branch bent living and never let go. What it misses with takes root where it lands." },

];''',
     RELIC_NEW),

    ("fighter state",
     '''    this.ultSlag = null;      // {t, fuse, split} while a Slagburst fuse burns''',
     FIGHTER_STATE_NEW),

    ("the cast",
     '''    if (u.kind === "spinstorm"){
      f.ultSpin = { phase: "wind", t: 0, stun: 0, acc: 0, n: 0, peak: 0, chuff: 0 };
    }''',
     FIRE_ULT_NEW),

    ("the tick call",
     '''    this.tickVines(dt);
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);''',
     TICK_CALL_NEW),

    ("tickAegis",
     '''  tickHits(self, foe, dt, cool){''',
     TICK_AEGIS_NEW),

    ("the block",
     '''    dmg = Math.round(dmg);

    this.hurt(foe, dmg, self);''',
     BLOCK_NEW),

    ("the art",
     '''  drawStatus(m, f){''',
     DRAW_AEGIS_NEW),

    ("the draw call",
     '''    this.drawStatus(m, f);''',
     DRAW_CALL_NEW),

    ("the block sound",
     '''      else if (kind === "vine"){''',
     SFX_AEGIS_NEW),

    ("the ult voice",
     '''        } else if (w === "vinesower"){         // a bowstring, then a field of it''',
     SFX_ULT_VOICE_NEW),

    ("the feed",
     """    for (const [k, n] of Object.entries(self.w.onSelf || {})){
      if (k !== "ward"){ self.apply(k, n); continue; }
      const W = STATUS.ward;
      const before = self.shield;""",
     FEED_NEW),

    ("the set-piece",
     """    /* ---- THE HARROWING, over -------------------------------------------""",
     SETPIECE_NEW),

    ("the fx clock",
     '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,''',
     ULTFX_LIFE_NEW),
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
    ap.add_argument("--src", default="../02-chain/sc-vinesower.html")
    ap.add_argument("--out", default="../02-chain/sc-bulwarden.html")
    ap.add_argument("--dmg", type=float, default=TUNED_BW)
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
    print(f"\nBULWARDEN BUILD -- the vigil warhammer and Aegis")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if '"seedfall"' not in s0:
        raise SystemExit("this source has no seedfall -- build off sc-vinesower or later")
    if '"aegis"' in s0:
        raise SystemExit("this source already has an aegis -- already built")

    subs = {"%ID%": RELIC_ID, "%NAME%": RELIC_NAME, "%ULT%": ULT_NAME,
            "%DMG%": f"{A.dmg:g}"}
    for k in ULT:
        subs["%" + k.upper() + "%"] = f"{getattr(A, k.lower()):g}"
    subs["%REFLECTPCT%"] = f"{round(A.reflect * 100):g}"
    # the fallback only -- the cast site sets the real one off `dur`
    subs["%FXLIFE%"] = f"{A.dur + 0.5:g}"

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
    print(f"    python3 bulwarden_probe.py --game {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40")
    print(f"    python3 frame_build.py --src {A.out} --out ../02-chain/sc-bulwarden-frame.html")
    print(f"    python3 chain_audit.py --relic {A.out} --tip ../02-chain/sc-bulwarden-frame.html\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
