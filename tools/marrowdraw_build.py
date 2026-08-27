#!/usr/bin/env python3
"""THE BLOODSWORN BOW. The twenty-fourth relic, and the first homing shot.

    python3 marrowdraw_build.py --src ../02-chain/sc-bulwarden.html \
                            --out ../02-chain/sc-marrowdraw.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v42 design document:

    "red bow slows down its shots drastically for a duration and begins
     shooting larger balista shots. The shots gain a homing effect that will
     seek out its opponent. when the shots hit they pierce the enemy ball fly
     through and fork into 2 shots which turn around and try to home in and
     hit again. the forks apply bleed
     the balista shot can be clanked nullifying the fork and destroying the
     bolt"

Three forks it left open, all three settled by him, and all three PRICED
BEFORE they were put (`marrowdraw_probe.py`, 14/14, runtime-only):

    HOMING   IT HUNTS -- 3-4 rad/s. At 4 the landed rate is 35.8% against a
             7.1% baseline and the wall falls from 82.9% to 35.4%. Above that
             only a blade stops a bolt and the ultimate's outcome becomes a
             property of the foe's weapon geometry.
    BLEED    THE FORKS BLEED EXTRA. The bolt carries the weapon's own
             hemorrhage 2 through resolveHit like any hit; each fork carries
             `forkBleed` on top, the way Exsanguinate applies 3.
    FORKS    THEY CAN BE BATTED. The Harrowing's precedent, and its comment is
             the argument: "an ultimate that cheated the rules its own weapon
             lives under would teach the viewer that the rules are decorative."

## WHY THIS IS THE ANSWER TO WHAT THE SURVEY MEASURED

`bow_survey` §2: **a bow lands 8.3% of what it fires and 81% of every arrow
ends on a wall.** v40 closed on that number -- "the wall is the type's
constraint and no relic addresses it" -- and Vinesower's Thicket then addressed
it by MONETISING the misses. This one attacks the same 81% from the other end:
**it stops missing.** Measured, at turn 4 rad/s, the wall goes 82.9% -> 35.4%.

And the cell needed none of it. Bloodsworn is already the strongest channel on
the bow at +53±23 in a paired 20s window (+52%) against sanctified's +38 and
umbral's +0. **This is the first relic in the chain whose ultimate is not being
asked to fix its own cell** -- so the ultimate is free to be about the TYPE.

## What the engine gives free, and it is nearly all of it

`arm` IS THE PIERCE. `tickShots` already gates both hit branches on
`!(s.arm > 0)`, for the Harrowing's blades. A fork is born inside the ball it
just came through and may not hit anything for `forkArm` seconds, which is
exactly "pierce the enemy ball, fly through" -- expressed in a field the engine
already has rather than in a new one.

`s.a` IS ALREADY INTERPOLATED. `LERP_FIELDS.shotAng` carries `a` with
shortest-path interpolation, so a bolt that turns every step draws a smooth
curve and does not strobe against the frame interpolator or spin the wrong way
round at pi. Homing writes `s.a` and gets that for nothing.

**"THE BALISTA SHOT CAN BE CLANKED, NULLIFYING THE FORK" IS ALREADY THE RULE.**
`tickShots` resolves in the order the viewer would -- parried, then landed,
then spent on a wall -- and a batted bolt sets `dead` in the parry branch and
never reaches the branch a fork hangs off. §1's last sentence costs zero lines.
`marrowdraw_probe [1]` asserts it structurally AND behaviourally: 111 bolts batted,
0 forks; 106 landed on a live foe, exactly 212 forks.

## The one thing that had to be invented

**STEERING.** `tickFire`'s own comment is the thing this breaks: "No aim, no
steering, no homing: the shot leaves along f.theta ... Everything that makes
ranged strong is positional luck rather than intent." Four bows have shipped
under that sentence and Reprisal's whole design is built on honouring it.

So the break is DECLARED and it is bounded: steering exists only while
`s.home` is a number, `s.home` is set only on shots loosed inside this relic's
own window, and it is RATE LIMITED -- "seek out its opponent" is a TRY, the
way Aegis's `turn` makes "tries to face them" a sentence with a failure mode
in it. A quarry that out-turns the bolt gets round it, and the viewer can see
that happen.

## The zero-burden argument, kept structurally

    ALL STATE IS `f.ultBal` AND THE PER-SHOT `s.home`/`s.bal`/`s.fork`,
    AND ALL OF IT IS null OR undefined ON EVERY OTHER RELIC.

The homing loop is `for (const s of this.shots) if (s.home)`, the fork is one
`if (s.bal ...)` inside a branch that already exists, and the cadence is one
multiplier that reads 1 when the window is down. `engine_ab` over the
twenty-three pre-existing ids is the proof, not this paragraph.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `dur`, `cadMul`, `dmgMul`, `home`, `forkHome`, `forkDmg` and
`forkBleed` are not in the design and cannot be guessed. `cadMul` and `dmgMul`
are not independent -- a window that fires a third as often for twice the
damage is a NERF -- and `marrowdraw_sweep.py` solves them jointly.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# MARROWDRAW. Rick's, from four offered. The draw of a bow, and marrow for the
# bone the bolt is turned from -- and `draw` is the one archery word the roster
# had not spent: Farwarden's Reprisal HOLDS a draw and never says so, which is
# the closest thing to a collision and is not one.
#
# BLOODHUNT. Rick's, from four offered. "It hunts" was his own word for the
# homing when he chose it, and blood- is the school's existing ultimate family
# (Bloodmill, Bloodprice). `quarrel` was ruled out before the four were offered
# because Ironhail's Quarrelstorm already owns it -- the same trap Bulwark was
# for Aegis, caught a step earlier this time.
#
# THE ID MATCHES THE NAME. `oathwound`/Goreshard and `redflail`/Threshmaw are
# the two existing drifts in this roster and both are traps; a third is not
# worth the twenty minutes it takes to avoid.
RELIC_ID = "marrowdraw"
RELIC_NAME = "Marrowdraw"
ULT_NAME = "Bloodhunt"

# BISECTED, not chosen. The type ships 12.73 (Farwarden) .. 16.23 (Ironhail),
# and bow_survey measured bloodsworn as the strongest channel on the row at
# +52%, so the expectation going in was that this number would come DOWN off
# the middle of the type. It did not have to: at cadMul 4 / dmgMul 1.6 the
# window is only about a third of the relic, and 15.25 sits comfortably inside
# the type's own range.
#
# AGAINST THE WHOLE FIELD, ALL 23 OPPONENTS, 920 FIGHTS. v41 open decision 2 is
# why that clause is in this comment: Bulwarden's dmg was bisected on a
# five-foe subset that read 50% and the full field read 55.2% on the same
# number -- five points, and three full passes to find.
#
#   dmg 16.00 -> 54.3%    dmg 14.50 -> 46.0%
#   dmg 15.62 -> 51.0%    dmg 13.00 -> 40.8%
#   dmg 15.25 -> 49.6%    <- ships
TUNED_RB = 15.25

# EVERY ONE OF THESE IS A PLACEHOLDER.
ULT = {
    # Bows ship 14 (Aureole), 15 (Ironhail, Vinesower), 16 (Farwarden). A
    # window that converts the type's own worst number should not be the
    # cheapest thing on the row.
    "charge":   15.0,
    # HOW LONG THE WINDOW STANDS. At cadMul 3 a 8s window is seven or eight
    # bolts -- few enough to count, which is the point of "drastically".
    "dur":       8.0,
    # HOW MUCH SLOWER THE STRING IS. §1's "slows down its shots drastically".
    # The type's cadence is 0.34, so 4.0 is a bolt every 1.36 seconds and
    # about four a window -- few enough to count, which is what "drastically"
    # has to mean if the viewer is to notice it happening.
    "cadMul":    4.0,
    # WHAT ONE BOLT IS WORTH, as a multiplier on the weapon's own damage.
    #
    # NOT INDEPENDENT OF cadMul, which is why marrowdraw_sweep solves the pair
    # and not either half: at cadMul 4 the window fires a quarter as many
    # shots, so anything under 4.0 here is a DPS cut bought back by the landed
    # rate -- and the landed rate is itself a function of how long each bolt
    # is in the air.
    #
    # RICK'S CALL, AND THE FRAMING THAT MADE IT DECIDABLE: across the whole
    # grid a bolt lands for 24-26 damage whatever the pair is, because the
    # blade bisects to compensate. So the pair does not choose how hard a bolt
    # hits -- it chooses HOW STRONG THE RELIC IS BETWEEN CASTS. At 4/1.6 the
    # blade lands inside the type's own 12.73-16.23, so Marrowdraw is a real
    # bow that gets a hunting window rather than a relic that is barely a bow
    # between them, and the window is about a third of its damage.
    "dmgMul":    1.6,
    # HOW BIG THE BOLT IS. **A LOOK KNOB, NOT A BALANCE KNOB**, and that is
    # measured rather than asserted: marrowdraw_probe [3] swept r from 24 to 60
    # and the parried-per-landed ratio is flat (1.31 -> 1.28) because `r` is
    # on BOTH sides of the engine's ledger -- the hit test is
    # `dist < R + s.r` and the parry test is `dist < s.r + width/2 + pad`.
    # Both sides grow together. So this is drawn at whatever size reads as a
    # ballista bolt in the hall, and nothing downstream is balanced on it.
    "r":        44.0,
    # HOW FAST THE BOLT TRAVELS. The type's own shot is 380. **THIS is the
    # knob the clank clause lives on**, and it is the one §1 named: a slow
    # bolt is longer in the air, which is more time for a blade to find it AND
    # more time for the homing to work, and between 380 and 220 the blade
    # wins. Parried per landed, at home 2.0: 0.81 at 380, 1.06 at 300, 1.17 at
    # 220, 0.97 at 150 -- an interior maximum, because past 220 the homing
    # catches back up. marrowdraw_probe [4].
    "speed":   220.0,
    # HOW HARD THE BOLT HUNTS, rad/s. **Rick's call from three priced
    # options: "it hunts".** At 4 rad/s the landed rate is 35.8% against a
    # 7.1% baseline and a third of bolts still end on a wall, so the miss
    # stays on screen. Above ~8 only a blade stops a bolt and the outcome
    # becomes a property of the foe's weapon shape.
    "home":      3.0,
    # HOW LONG A BOLT LIVES. Longer than the type's 3.4 because it is slower:
    # 220 x 5.0 = 1100 units, still further than any wall, so `life` never
    # fires and the bolt always ends on something the viewer watched.
    "life":      5.0,
    # HOW MANY EYES OPEN ABOVE THE BALL while the window stands. Rick: "can we
    # also give the ball itself an animation when its bloodhunting? maybe
    # piercing red hunters eyes floating above it?" Pure look; nothing reads
    # it but the renderer.
    "artEyes":   3.0,
    # HOW MANY FORKS. §1 says two.
    "fork":      2.0,
    # THE ANGLE THEY DIVERGE BY, about the bolt's own heading. Wide enough
    # that two objects leave rather than one, narrow enough that both are
    # still pointing away from the ball they just came through.
    "forkSpread": 0.9,
    # THE FORK'S SIZE, as a share of the bolt's. It is a piece of the bolt.
    "forkRMul":  0.55,
    # HOW HARD A FORK HUNTS. Higher than the bolt's on purpose: a fork has to
    # come back, and it cannot turn inside a radius of v/w -- 55 units at 4
    # rad/s, which is smaller than the ball. marrowdraw_probe [6]: 51.9% of forks
    # connect at 4 and NO fork ends on a wall above it.
    "forkHome":  4.0,
    # HOW LONG A FORK CHASES. "TRY to home in and hit again" -- the life is
    # what makes it a try.
    "forkLife":  2.2,
    # THE PIERCE. Seconds after birth in which a fork may not hit anything,
    # which is "fly through the enemy ball" expressed in the engine's own
    # `arm` field. At 220 u/s this is 40 units, past a ball of radius 34.
    "forkArm":   0.18,
    # WHAT A FORK IS WORTH, as a multiplier on the weapon's damage.
    "forkDmg":   0.5,
    # ---- THE BOLT'S PROPORTIONS. Rick, on the first cut: "the balista shots
    # look a little cartooney. can we go for a longer slimmer and more
    # realistic look?" So the silhouette is numbers rather than literals, and
    # it is judged from `marrowdraw_bolt_zoom.py` rather than from a filmstrip at
    # 30%. ALL THREE ARE PURE LOOK -- marrowdraw_probe [3] measured `r` as
    # balance-free and these do not touch `r`.
    #
    # TOTAL LENGTH, in units of `r`. 2.0 was the dart; 3.4 was the rocket.
    "artLen":    3.2,
    # SHAFT HALF-WIDTH, in units of `r`. **THIS is the number the look lives
    # on.** 0.30 was the cartoon and 0.085 was still a rocket body; at 0.048
    # the aspect is about 33:1, which is what the reference is.
    "artW":      0.048,
    # HEAD LENGTH, in units of `r`. SMALL. The cartoon's head was a bright
    # white nose cone a third the length of the object, which is most of why
    # it read as a rocket -- a real broadhead is a short dark leaf barely
    # wider than the shaft it is socketed onto.
    "artHead":   0.34,
    # HOW MUCH OF THE TAIL IS FEATHER, as a share of total length.
    "artFletch": 0.26,
    # WHETHER THE BOLT ITSELF CARRIES THE SCHOOL. **Rick's call: it does
    # not.** 0 hands `over.onHit` an empty object, which `resolveHit` already
    # honours for Ironbloom's splinter ("a splinter sunders ONCE, where the
    # head that threw it sunders twice"), so the bolt lands as pure damage and
    # the FORKS carry the bleed -- which is §1's sentence, made true.
    #
    # THERE IS NO `forkBleed`, AND THAT IS A FINDING RATHER THAN AN OMISSION.
    # §1 says "the forks apply bleed" and the first build read that as an EXTRA
    # application on top of the weapon's own `onHit`. It swept BYTE-IDENTICAL
    # at 0, 1, 2 and 3 -- v41's wall-feed signature exactly -- because
    # `STATUS.hemorrhage.maxStacks` is 4, `onHit` is 2, and `resolveHit` fills
    # the ladder in the same call: 86% of fork hits arrive with the quarry
    # ALREADY AT CAP and `apply` clamps the rest away with Math.min.
    #
    # A dead knob is worse than no knob -- `shot.life: 3.4` has been dead
    # config on four bows since v40 and is still an open decision -- so it is
    # not shipped. The forks bleed because everything that lands bleeds, and
    # they are now the only part of this ultimate that does.
    "boltBleed": 0.0,
}


# ---------------------------------------------------------------- THE RELIC --

RELIC_NEW = '''    blurb:"Every plate it banks it can raise as a wall. What the wall stops, it hands back." },

  /* THE BLOODSWORN BOW -- the twenty-fourth relic, and the first shot in this
     game that steers.

     THE CELL WAS NOT CHOSEN ON A GAP. For the first time in the project the
     grid had none to offer: five schools at 3 of 6, two at 4, four types tied
     at 3. It was chosen on the design job, and the job is the TYPE's, because
     the school does not need one -- bow_survey §5 measures bloodsworn as the
     strongest channel on this row at +53±23 in a paired 20s window (+52%),
     against sanctified's +38 and umbral's +0.

     THE JOB IS THE 81%. bow_survey §2: a bow lands 8.3% of what it fires and
     81% of every arrow ever loosed ends on a wall. Thicket spends that number;
     this one refuses it.

     Physics are Ironhail's, Aureole's, Farwarden's and Vinesower's exactly --
     all five bows share one `shot` block byte for byte and the TYPE owns it.
     The school owns hemorrhage and the red; SHAPES' bow branch has drawn the
     barbed recurve with the tip-hooks since before this relic existed.

     `dmg` and every number under `ult` are PLACEHOLDERS -- marrowdraw_build's
     TUNED_RB and ULT -- and MUST be swept. `cadMul` and `dmgMul` are not
     independent and the sweep solves them jointly. */
  { id:"%ID%", name:"%NAME%", aff:"bloodsworn", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:%DMG%, spin:2.8, mode:"ranged", mass:1.6,
    shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" },
    onHit:{ hemorrhage:2 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"ballista",
          dur:%DUR%, cadMul:%CADMUL%, dmgMul:%DMGMUL%,
          r:%R%, speed:%SPEED%, home:%HOME%, life:%LIFE%,
          fork:%FORK%, forkSpread:%FORKSPREAD%, forkRMul:%FORKRMUL%,
          forkHome:%FORKHOME%, forkLife:%FORKLIFE%, forkArm:%FORKARM%,
          forkDmg:%FORKDMG%, boltBleed:%BOLTBLEED%,
          /* PURE LOOK. marrowdraw_probe [3] measured `r` as
             balance-free and these do not touch `r`. */
          artLen:%ARTLEN%, artW:%ARTW%, artHead:%ARTHEAD%,
          artFletch:%ARTFLETCH%,
          /* THE NUMBERS IN THE TIP ARE SUBSTITUTED, not typed -- v40 shipped a
             card reading "5s" after the sweep moved the number to 8.1 and
             nothing caught it, because verify.py only asks that a tip EXISTS.
             `marrowdraw_probe` asserts every number in this line against the
             weapon's own fields. */
          /* RICK'S LINE, VERBATIM, with the number SUBSTITUTED rather than
             typed. v40 shipped a card reading "5s" after the sweep moved the
             number to 8.1 and nothing caught it, because verify.py only asks
             that a tip EXISTS; marrowdraw_relic_probe [1] asserts every number
             in this line against a field the weapon actually has. */
          tip:"For %DUR%s, fires homing bolts that pierce and fork" },
    blurb:"Hooked bone, strung on marrow. Nothing it looses is finished with you on the way past." },

];'''


# ------------------------------------------------------------- THE STATE --

FIGHTER_STATE_NEW = '''    /* {t, dur, bolts, hits, forks} while the ballista window stands. null on
       every other relic, and null on this one outside its own window, which
       is the whole zero-burden argument: the cadence multiplier reads 1, the
       shot upgrade in spawnShot does not run, and no shot ever gets a `home`
       so the steering loop in tickShots iterates over nothing. */
    this.ultBal = null;
    this.ultAegis = null;'''


# --------------------------------------------------------------- THE CAST --

FIRE_ULT_NEW = '''    /* THE STRING SLOWS AND THE BOLTS GET BIG. Rick: "red bow slows down its
       shots drastically for a duration and begins shooting larger balista
       shots."

       NOTHING RESOLVES HERE. This ultimate does not deal damage at the cast;
       it changes what the weapon has been doing all fight, for a window. That
       is the same shape as Bloodmill and the Thicket, and it is the reason
       the set-piece's life is taken from `ult.dur` below rather than from the
       fallback map.

       THE WINDOW DOES NOT REFILL THE CLOCK. `f.fireCd` is left exactly as it
       is, so the first bolt arrives when the next arrow would have -- the
       viewer sees the stream they were already watching become something
       else, rather than a pause and then a bolt. */
    if (u.kind === "ballista"){
      f.ultBal = { t: 0, dur: u.dur, bolts: 0, hits: 0, forks: 0 };
      this.ultFx.life = u.dur + 0.6;
    }

    if (u.kind === "aegis"){'''


# ------------------------------------------------------------- THE WINDOW --

TICK_BAL_NEW = '''  /* ------------------------------------------------------------- BALLISTA --
     The window, and nothing else. The bolts are made in spawnShot, steered in
     tickShots and forked in tickShots; this only decides when it is over.

     RETURNS ON ITS FIRST LINE on every relic that is not inside a window,
     which is every relic in the roster except this one and this one for most
     of a fight. */
  tickBallista(dt){
    for (const f of [this.a, this.b]){
      const B = f.ultBal;
      if (!B) continue;
      B.t += dt;
      /* THE WINDOW ENDS AND THE BOLTS IN THE AIR STAY IN THE AIR. A bolt is
         a committed object -- it was loosed, the viewer watched it go, and
         deleting it because a clock ran out would take away a hit that had
         already been earned. The Thicket's seeds live past their window for
         the same reason. */
      if (B.t >= B.dur) f.ultBal = null;
    }
  }

  tickHits(self, foe, dt, cool){'''

TICK_CALL_NEW = '''    this.tickBallista(dt);
    this.tickAegis(dt);'''


# ------------------------------------------------------------- THE CADENCE --

CADENCE_NEW = '''    f.fireCd -= dt;
    if (f.fireCd > 0) return;
    /* DRASTICALLY SLOWER, and it is one multiplier that reads 1 when the
       window is down. `=== undefined` and not `|| 1`: v41's wall-feed read
       `u.feed || 1` and every "feed off" control in that sweep silently
       measured a feed of ONE, which was caught only because two configurations
       came back byte-identical across 100 fights. A sweep is allowed to set
       cadMul to 0 and must be able to. */
    const cm = f.ultBal && f.w.ult.cadMul !== undefined ? f.w.ult.cadMul : 1;
    f.fireCd += S.cadence * cm;
    this.spawnShot(f);'''


# ---------------------------------------------------------------- THE BOLT --

SPAWN_NEW = '''      seed: f.ultBloom ? (f.ultBloom.left--, true) : false,
      aff: f.aff, a,
    });
    /* THE BOLT. The shot is spawned by the shipped path first and then
       upgraded in place, so everything the type owns -- where it leaves from,
       that it inherits none of the ball's velocity, that it points along the
       facing -- is still decided by one piece of code for all five bows.

       `speed` is applied as a RESCALE of the velocity the type already set
       rather than as a fresh vector, so a bolt cannot end up travelling
       somewhere the arrow would not have. */
    if (f.ultBal){
      const u = f.w.ult, s = this.shots[this.shots.length - 1];
      const sp = Math.hypot(s.vx, s.vy) || 1, k = u.speed / sp;
      s.vx *= k; s.vy *= k;
      s.r = u.r; s.life = u.life; s.max = u.life;
      s.dmgMul = s.dmgMul * u.dmgMul;
      s.bal = true; s.home = u.home;
      /* `over.onHit` lets one call site state its own statuses without giving
         the weapon a second field -- resolveHit's own comment, written for
         Ironbloom's splinter. `=== 0` and not `!u.boltBleed`: a sweep is
         allowed to set this to zero and must be able to, which is v41's
         `u.feed || 1` lesson in the one place it would bite again. */
      if (u.boltBleed === 0) s.over = { onHit: {} };
      /* The silhouette travels with the shot so drawShots needs no handle on
         the weapon. Three numbers, and a fork inherits them scaled. */
      s.bL = u.artLen; s.bW = u.artW; s.bH = u.artHead; s.bF = u.artFletch;
      f.ultBal.bolts++;
    }
    f.shotsFired++;
    SFX.play("loose", { bal: !!f.ultBal });'''


# --------------------------------------------------------------- THE HOMING --

HOME_NEW = '''      const s = this.shots[i];
      /* --- THE HOMING. `tickFire`'s own comment is what this breaks: "No aim,
         no steering, no homing: the shot leaves along f.theta." Four bows
         shipped under that sentence and Reprisal's entire design honours it,
         so the break is BOUNDED: it runs only where `s.home` is a number, and
         `s.home` is set only on shots loosed inside one relic's own window.

         RATE LIMITED, because "seek out its opponent" is a TRY. A bolt cannot
         turn inside a radius of `speed / home` -- 73 units at 220 and 3 rad/s
         -- so a quarry that out-turns it gets round the outside, and that is
         a failure the viewer can watch rather than arithmetic.

         `s.a` is written as well as the velocity: it is in LERP_FIELDS.shotAng
         with shortest-path interpolation, so the art turns with the bolt and
         does not spin the wrong way round at pi. */
      if (s.home){
        const tg = s.own === "a" ? this.b : this.a;
        if (tg.alive){
          const cur = Math.atan2(s.vy, s.vx);
          let d = Math.atan2(tg.y - s.y, tg.x - s.x) - cur;
          while (d >  Math.PI) d -= TAU;
          while (d < -Math.PI) d += TAU;
          const na = cur + clamp(d, -s.home * dt, s.home * dt);
          const sp = Math.hypot(s.vx, s.vy);
          s.vx = Math.cos(na) * sp; s.vy = Math.sin(na) * sp;
          s.a = na;
        }
        /* THE TRAIL IS WHERE IT ACTUALLY WENT. A streak laid along the
           CURRENT heading is a straight line behind a curving object, which
           draws the one thing this ultimate is not. This is a short ring
           buffer of real positions, so the arc in the air is the arc the bolt
           flew. Presentation only -- nothing reads it, it is not in
           LERP_FIELDS, and it exists only on shots that steer. */
        (s.trail || (s.trail = [])).push(s.x, s.y);
        if (s.trail.length > 24) s.trail.splice(0, 2);
      }
      s.vy += s.grav * dt;'''


# ---------------------------------------------------------------- THE FORK --

FORK_NEW = '''        if (s.knock){
          const kl = Math.hypot(s.vx, s.vy) || 1;
          foe.vx += (s.vx / kl) * s.knock; foe.vy += (s.vy / kl) * s.knock;
        }
        /* --- THE FORK. Rick: "when the shots hit they pierce the enemy ball
           fly through and fork into 2 shots which turn around and try to home
           in and hit again."

           THIS BRANCH IS THE WHOLE OF "CAN BE CLANKED, NULLIFYING THE FORK".
           tickShots resolves parried, then landed, then spent on a wall, and
           a batted bolt sets `dead` in the parry branch above and never
           arrives here. The counterplay is the engine's existing order and
           costs nothing to keep.

           A LETHAL BOLT DOES NOT FORK. `foe.alive` is tested after resolveHit
           has run, so a bolt that killed produces nothing -- a blade does not
           stick into a corpse and a fork should not chase one.

           `arm` IS THE PIERCE. The forks are born inside the ball the bolt
           just went through and may not hit anything for `forkArm`, which is
           the pass-through, written in the field tickShots already gates both
           hit branches on. */
        if (s.bal && foe.alive && src.alive){
          const u = src.w.ult, base = Math.atan2(s.vy, s.vx);
          /* THE BOLT COMES APART, AND IT MAKES A NOISE. Rick, asked whether
             the sound was finished: "give the fork its own sound." He is
             right and the reason is structural rather than aesthetic -- the
             pierce and the split were SILENT, so the half of this ultimate
             that happens after the hit was carried entirely by the picture,
             and a viewer who blinked heard an ordinary arrow land.

             ONE CALL PER PIERCE, not one per fork. Two forks are one event;
             firing it twice would double the transient and read as two
             separate impacts a frame apart. */
          SFX.play("fork");
          /* The bolt came apart. Sparks along the line of travel, so the
             viewer reads a pass-THROUGH rather than a stop. */
          this.spawnFx(s.x, s.y, src.aff.glow, 10, 260, 0.30, 3.0,
                       s.vx / (Math.hypot(s.vx, s.vy) || 1) * 90,
                       s.vy / (Math.hypot(s.vx, s.vy) || 1) * 90);
          this.ring(s.x, s.y, src.aff.core, 3, 52, 0.24, 3);
          const n = u.fork | 0;
          const sp2 = Math.hypot(s.vx, s.vy);
          for (let k = 0; k < n; k++){
            /* maxLive is a ceiling on objects in flight and spawnShot honours
               it by shifting the oldest out. THIS path must not: a shift
               inside the loop tickShots is running would move every index
               under the iterator. It declines to spawn instead, which is the
               same protection without the corruption. */
            if (this.shots.length >= CONFIG.shot.maxLive) break;
            const off = n === 1 ? 0
                      : -u.forkSpread / 2 + u.forkSpread * (k / (n - 1));
            const a2 = base + off;
            this.shots.push({
              own: s.own, x: s.x, y: s.y, x0: s.x, y0: s.y,
              spd0: 0, t0: this.t,                        // CINEMA (demo)
              vx: Math.cos(a2) * sp2, vy: Math.sin(a2) * sp2,
              r: Math.max(5, u.r * u.forkRMul),
              life: u.forkLife, max: u.forkLife, grav: 0,
              dmgMul: u.forkDmg, arm: u.forkArm, home: u.forkHome,
              fork: true, aff: s.aff, a: a2,
              /* A fork is a PIECE of the bolt: the same slenderness, a
                 shorter shaft, the same head. Not a small bolt -- a broken
                 one. */
              bL: u.artLen * 0.62, bW: u.artW * 1.30, bH: u.artHead * 0.90,
              bF: u.artFletch * 1.15,
            });
            if (src.ultBal) src.ultBal.forks++;
          }
        }
        dead = true;
      }'''


# ------------------------------------------------------------------ THE ART --

DRAW_BOLT_NEW = '''      /* A BALLISTA BOLT, third cut, drawn from a reference Rick supplied.

         CUT ONE was a dart: a 3:1 shaft with a fat triangular head and two
         vanes nearly as wide as the bolt was long. "the balista shots look a
         little cartooney. can we go for a longer slimmer and more realistic
         look?"

         CUT TWO was 20:1 and still wrong, and the diagnosis is worth keeping
         because it is not about length: "they look like cartoony rockets."
         A big BRIGHT WHITE nose cone plus two solid saturated fins is a
         rocket, at any aspect ratio. Slimming a rocket makes a slimmer rocket.

         WHAT THE REFERENCE ACTUALLY IS, and every one of these fights the
         rocket read:
           * the shaft is nearly all of the object -- about 33:1 -- and it is
             pale bone with a TWIST cut down its length;
           * the head is SMALL and DARK, a short leaf barely wider than the
             shaft, not a bright cone;
           * the fletching is FEATHER: three dark vanes with visible barbs,
             leaf-shaped and splayed, set right at the nock -- not two solid
             flares halfway up the body;
           * the only bright metal is a small nock cap at the very end.

         So the value structure is inverted from cut two. The shaft is the
         light thing and the ENDS are dark, which is also why it reads at
         arena scale: two dark tips at a known separation on a pale line is a
         length cue, where a bright point on a pale line was just a longer
         bright thing.

         THE SIZE IS FREE, and that is measured rather than assumed:
         marrowdraw_probe [3] swept `r` from 24 to 60 and the parried-per-landed
         ratio did not move (1.31 -> 1.28), because `r` is on both sides of the
         engine's ledger -- the hit test is `dist < R + s.r` and the parry test
         is `dist < s.r + width/2 + pad`. So the bolt is drawn at whatever
         reads and the balance is untouched. This is the opposite of v41's
         shield, where the picture and the hitbox had to be argued apart; here
         they agree because nothing forced them not to.

         THE TRAIL IS THE MECHANIC. A polyline through positions the bolt
         really occupied, so a bolt that curved draws a curve. A streak along
         the current heading -- which is what every other projectile in this
         game draws, correctly, because every other projectile flies straight
         -- would draw a straight line behind a turning object. */
      if (s.bal || s.fork){
        const dim = s.arm > 0 ? 0.5 : 1;
        const L  = s.r * (s.bL || 3.2);          /* total length */
        const W  = s.r * (s.bW || 0.048);        /* shaft half-width */
        const HD = s.r * (s.bH || 0.34);         /* head length */
        const FL = L * (s.bF || 0.26);           /* feathered tail */
        const nose = L * 0.42, tail = -L * 0.58; /* the hit point leads */
        const T = s.trail;
        /* the flown path. It ends at the NOCK, not at `s.x` -- the hit point
           is 42% back from the nose, so a trail terminating at the shot's own
           coordinate stops halfway up the shaft and reads as a separate
           object floating beside the bolt. */
        const tux = Math.cos(s.a), tuy = Math.sin(s.a);
        if (T && T.length >= 4){
          c.globalCompositeOperation = "lighter";
          for (let pass = 0; pass < 2; pass++){
            c.strokeStyle = pass ? s.aff.glow : s.aff.core;
            /* THIN. The first cut was 0.20r under `lighter`, which
               double-exposes itself and drew a pink rope thicker than the
               bolt it was trailing. */
            c.lineWidth = Math.max(1, s.r * (pass ? 0.04 : 0.10));
            c.globalAlpha = (pass ? 0.55 : 0.20) * dim;
            c.lineJoin = "round"; c.lineCap = "round";
            c.beginPath();
            c.moveTo(T[0], T[1]);
            for (let k = 2; k < T.length; k += 2) c.lineTo(T[k], T[k + 1]);
            c.lineTo(s.x + tux * tail, s.y + tuy * tail);
            c.stroke();
          }
          c.lineCap = "butt";
        }
        /* A LOW GLOW, and smaller than the object. The Harrowing's first cut
           put a 2.3r halo around a 1.0r crescent and the contact sheet showed
           twelve white blobs -- the shape was inside its own bloom. A 33:1
           bolt disappears into one even faster. */
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 0.62);
        gh.addColorStop(0, s.aff.glow + "4A");
        gh.addColorStop(1, s.aff.glow + "00");
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 0.5 * dim; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.fill();

        c.globalCompositeOperation = "source-over";
        c.globalAlpha = dim;
        c.save(); c.translate(s.x, s.y); c.rotate(s.a);

        /* THE SHAFT. Bone, tapering a little toward the head the way a turned
           shaft does. */
        c.fillStyle = s.aff.steel;
        c.beginPath();
        c.moveTo(tail + L * 0.02, -W * 1.05);
        c.lineTo(nose - HD * 0.55, -W * 0.72);
        c.lineTo(nose - HD * 0.55,  W * 0.72);
        c.lineTo(tail + L * 0.02,   W * 1.05);
        c.closePath(); c.fill();

        /* THE TWIST. Short diagonal ticks down the length, which is the one
           detail in the reference that says "turned wood" rather than "line".
           Stepped in world units off the bolt's own length so a fork -- a
           shorter object -- gets the same pitch rather than the same COUNT,
           and the two read as the same material. */
        c.strokeStyle = s.aff.dark;
        c.globalAlpha = 0.34 * dim;
        c.lineWidth = Math.max(0.6, W * 0.42);
        const pitch = Math.max(4, s.r * 0.15);
        for (let x = tail + L * 0.06; x < nose - HD * 0.7; x += pitch){
          c.beginPath();
          c.moveTo(x, -W * 0.9);
          c.lineTo(x + pitch * 0.55, W * 0.9);
          c.stroke();
        }
        c.globalAlpha = dim;

        /* THE FEATHERS. Three, dark, leaf-shaped, splayed, set at the nock,
           with barbs. Two are drawn as full vanes above and below; the third
           is the foreshortened one on the centreline, which is what the top
           feather of a three-fletch looks like from the side and is the
           cheapest honest cue that this is a round shaft and not a decal. */
        const fx0 = tail + L * 0.03, fx1 = fx0 + FL;
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.71);
        for (const sgn of [-1, 1]){
          c.beginPath();
          c.moveTo(fx1, sgn * W * 0.6);
          c.quadraticCurveTo(fx0 + FL * 0.42, sgn * W * 4.6,
                             fx0 + FL * 0.06, sgn * W * 3.4);
          c.quadraticCurveTo(fx0 + FL * 0.30, sgn * W * 1.4, fx0, sgn * W * 0.7);
          c.closePath(); c.fill();
          /* the barbs */
          c.strokeStyle = s.aff.core;
          c.globalAlpha = 0.42 * dim;
          c.lineWidth = Math.max(0.5, W * 0.30);
          for (let k = 1; k <= 4; k++){
            const t = k / 5;
            const bx = fx0 + FL * (0.10 + t * 0.72);
            c.beginPath();
            c.moveTo(bx, sgn * W * 0.8);
            c.lineTo(bx - FL * 0.10, sgn * W * (1.0 + 2.6 * (1 - Math.abs(t - 0.45) * 1.5)));
            c.stroke();
          }
          c.globalAlpha = dim;
        }
        c.fillStyle = s.aff.dark;
        c.globalAlpha = 0.72 * dim;
        c.beginPath();
        c.moveTo(fx1, -W * 0.5); c.lineTo(fx0 + FL * 0.12, -W * 1.5);
        c.lineTo(fx0 + FL * 0.12, W * 1.5); c.lineTo(fx1, W * 0.5);
        c.closePath(); c.fill();
        c.globalAlpha = dim;

        /* THE NOCK. The one piece of bright metal on the object, and it is at
           the BACK -- so the eye reads the tail, and direction of travel comes
           free from which end is glowing. */
        c.fillStyle = s.aff.core;
        c.fillRect(tail, -W * 1.25, L * 0.035, W * 2.5);

        /* THE HEAD. A short dark leaf, barely wider than the shaft, with one
           pale edge where the light catches the bevel. Small on purpose: the
           bright cone was most of the rocket. */
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.71);
        c.beginPath();
        c.moveTo(nose, 0);
        c.quadraticCurveTo(nose - HD * 0.45, -W * 2.1, nose - HD, -W * 0.55);
        c.lineTo(nose - HD,  W * 0.55);
        c.quadraticCurveTo(nose - HD * 0.45,  W * 2.1, nose, 0);
        c.closePath(); c.fill();
        c.strokeStyle = s.aff.glow;
        c.globalAlpha = 0.85 * dim;
        c.lineWidth = Math.max(0.6, W * 0.42);
        c.beginPath();
        c.moveTo(nose, 0);
        c.quadraticCurveTo(nose - HD * 0.45, -W * 2.1, nose - HD, -W * 0.55);
        c.stroke();
        c.globalAlpha = dim;
        /* the socket band */
        c.fillStyle = s.aff.core;
        c.fillRect(nose - HD - W * 0.9, -W * 1.0, W * 1.4, W * 2.0);

        c.restore();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 1;
        continue;
      }
      const sp = Math.hypot(s.vx, s.vy) || 1;'''


# -------------------------------------------------------------- THE ARCHER --

DRAW_DRAW_NEW = '''  /* THE HUNTER'S EYES. Rick: "can we also give the ball itself an animation
     when its bloodhunting? maybe piercing red hunters eyes floating above it?"

     WHY THE BALL NEEDED ONE AT ALL. Every other window ultimate in this game
     puts something on the CASTER that the viewer can point at -- Bloodmill
     spins the head, Aegis stands a wall in front of it, the Thicket roots the
     hall. Bloodhunt's whole expression was out in the air on objects that are
     only there half the time: between bolts the relic looked exactly like a
     bow having a quiet moment, and the window is eight seconds long.

     THEY LOOK AT THE QUARRY, and that is the point rather than a flourish.
     The pupils track the foe, so the picture on the caster says the same
     thing the bolts say -- this weapon has stopped firing at a DIRECTION and
     started firing at a FIGHTER. It is the homing, stated on the ball, a
     second before the first bolt proves it.

     BLINKING IS NOT DECORATION EITHER. A row of steady lights reads as a
     status icon; a row that blinks, at slightly different times, reads as
     something alive looking at you. The phase offset per eye is what stops
     them reading as one object with three lamps on it.

     Deterministic off `m.t`, the way SHAPES._t is: `life` is not in
     LERP_FIELDS, and an accumulated phase would strobe against the frame
     interpolator. Returns on its first line on every relic in the roster. */
  _drawBalWindow(m, f){
    const B = f.ultBal;
    if (!B) return;
    const c = this.ctx;
    const R = CONFIG.physics.ballR;
    const foe = f === m.a ? m.b : m.a;
    const u = f.w.ult;
    const N = Math.max(1, Math.round(u.artEyes === undefined ? 3 : u.artEyes));

    /* IN FAST, OUT SLOW. They snap open on the cast -- it is a trigger and
       should read as one -- and fade as the window runs down, so the end of
       it is legible before the last bolt rather than after it. */
    const A = clamp(B.t / 0.18, 0, 1) * clamp((B.dur - B.t) / 0.55, 0, 1);
    if (A <= 0.01) return;

    const bob = Math.sin(m.t * 2.15) * 2.4;
    /* HIGH ENOUGH TO CLEAR THE WEAPON. The first cut sat them at R+25 and
       the bow's own barbs swept through them twice a second -- the eyes are
       drawn before the relic, so the weapon wins every overlap. R+36 puts
       them above the arc a 54-reach bow sweeps and they stop being occluded
       by the thing they belong to. */
    const cy = f.y - R - 36 + bob;
    const sp = R * 0.60;
    const eyeR = R * 0.34;

    c.save();
    for (let i = 0; i < N; i++){
      const ex = f.x + (i - (N - 1) / 2) * sp;
      /* The row arcs: the outer eyes sit a little higher, so three of them
         read as a brow rather than as a line of pips. */
      const ey = cy - Math.abs(i - (N - 1) / 2) * eyeR * 0.42;

      /* THE BLINK. A short, hard close roughly every 2.4s, phase-shifted per
         eye by an irrational-ish step so the row never syncs up. */
      const ph = (m.t * 0.42 + i * 0.37) % 1;
      const blink = ph > 0.955 ? Math.abs(Math.cos((ph - 0.955) / 0.045 * Math.PI)) : 1;
      const open = eyeR * (0.62 * blink);

      /* the glow it sits in */
      c.globalCompositeOperation = "lighter";
      const gh = c.createRadialGradient(ex, ey, 1, ex, ey, eyeR * 2.6);
      gh.addColorStop(0, f.aff.core + "88");
      gh.addColorStop(0.45, f.aff.core + "33");
      gh.addColorStop(1, f.aff.glow + "00");
      c.globalAlpha = 0.75 * A;
      c.fillStyle = gh;
      c.beginPath(); c.arc(ex, ey, eyeR * 2.6, 0, TAU); c.fill();

      if (blink < 0.06){                    /* shut: a lid, and nothing else */
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 0.85 * A;
        c.strokeStyle = SHAPES._ink(f.aff.dark, 9.71);
        c.lineWidth = Math.max(1, eyeR * 0.22);
        c.beginPath();
        c.moveTo(ex - eyeR, ey); c.quadraticCurveTo(ex, ey + eyeR * 0.22, ex + eyeR, ey);
        c.stroke();
        continue;
      }

      /* THE ALMOND. Two quadratics, pinched at the corners -- a circle reads
         as a lamp and a slit reads as a scar; the pinch is what makes it an
         eye. */
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = A;
      c.fillStyle = SHAPES._ink(f.aff.dark, 9.71);
      c.beginPath();
      c.moveTo(ex - eyeR, ey);
      c.quadraticCurveTo(ex, ey - open * 1.65, ex + eyeR, ey);
      c.quadraticCurveTo(ex, ey + open * 1.65, ex - eyeR, ey);
      c.closePath(); c.fill();

      /* THE IRIS, LOOKING AT THE QUARRY. Offset toward it and clamped inside
         the almond, so a foe directly overhead does not push the pupil out
         through the lid. */
      const dx = foe.x - ex, dy = foe.y - ey;
      const dl = Math.hypot(dx, dy) || 1;
      const px = ex + (dx / dl) * eyeR * 0.34;
      const py = ey + (dy / dl) * Math.min(open * 0.34, eyeR * 0.34);
      const ir = eyeR * 0.46;
      c.globalCompositeOperation = "lighter";
      c.fillStyle = f.aff.core;
      c.beginPath(); c.ellipse(px, py, ir, Math.min(ir, open * 0.95), 0, 0, TAU); c.fill();
      c.fillStyle = f.aff.glow;
      c.globalAlpha = 0.9 * A;
      c.beginPath(); c.ellipse(px, py, ir * 0.55, Math.min(ir * 0.55, open * 0.7), 0, 0, TAU); c.fill();

      /* THE SLIT. Vertical, thin, and dark -- this is the "piercing" in
         Rick's sentence, and it is the only part of the eye that is not
         additive. A round pupil would read as an owl. */
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = A;
      c.fillStyle = SHAPES._ink(f.aff.dark, 9.71);
      c.beginPath();
      c.ellipse(px, py, Math.max(0.7, ir * 0.20), Math.min(ir * 1.05, open * 0.92),
                0, 0, TAU);
      c.fill();
    }
    c.restore();
    c.globalAlpha = 1;
    c.globalCompositeOperation = "source-over";
  }

  drawStatus(m, f){'''


DRAW_CALL_NEW = '''    this._drawBalWindow(m, f);
    this.drawStatus(m, f);'''


# -------------------------------------------------------------- THE SOUND --

# The EXISTING branch is rewritten, not a new one inserted beside it. The first
# cut anchored on `kind === "vine"` and put a second `else if (kind ===
# "loose")` into the same if/else chain BELOW the real one -- unreachable, and
# nothing at runtime would ever have said so, because a sound that does not
# play looks exactly like a sound that plays quietly.
SFX_LOOSE_NEW = '''      else if (kind === "loose"){
        /* Woody body, no top end. It sits UNDER the impacts rather than
           competing with them, so a shot landing still reads louder than
           a shot leaving. */
        /* THE BALLISTA STRING is the SAME EVENT -- one string, one relic --
           so it is this sound transposed down with a longer body and a little
           windlass creak under it, rather than a new sound that would read as
           a second weapon. */
        if (p.bal){
          this._burst(t, { freq: 168, q: 1.3, gain: 0.10, dur: 0.16, type:"bandpass" });
          this._tone (t, { freq: 128, to: 58, gain: 0.10, dur: 0.20, type:"sawtooth" });
        } else {
          this._burst(t, { freq: 380, q: 1.1, gain: 0.055, dur: 0.055, type:"bandpass" });
        }
      }
      else if (kind === "fork"){
        /* A WET SPLIT. Bright and short so it cuts through the hit that fired
           it -- they land on the same frame -- with a falling body underneath
           so it reads as something COMING APART rather than as a second
           impact. Deliberately quieter than `hit`: the blow is the event and
           this is what the event did. */
        this._burst(t,         { freq: 1650, q: 0.9,  gain: 0.075, dur: 0.045, type:"bandpass" });
        this._tone (t,         { freq: 430, to: 140,  gain: 0.085, dur: 0.14,  type:"sawtooth" });
        this._burst(t + 0.022, { freq: 640,  q: 1.7,  gain: 0.055, dur: 0.09,  type:"bandpass" });
      }'''

# THE FIRST CUT OF THIS CALLED `this.tone()` AND `this.noise()`, NEITHER OF
# WHICH EXISTS. The helpers are `_tone(t, {...})` and `_burst(t, {...})`. It
# threw a TypeError on the first cast and NOTHING ANYWHERE COULD SAY SO:
# `SFX.play` wraps its whole body in a try/catch, and every probe in this repo
# runs headless where `SFX.ok` is false and `play` returns on its first line.
#
# So the ultimate shipped SILENT and it took Rick asking for "a sound effect to
# signify it triggering" to surface it. `marrowdraw_relic_probe [10]` builds a
# real AudioContext and plays every sound this relic makes, which is the check
# that had to exist and did not.
SFX_ULT_VOICE_NEW = '''        } else if (w === "%ID%"){
          /* AN IRON CLAMP CLOSING. Rick's pick from six candidates, then his
             pick from three depths of it, then "lower and louder".

             HOW IT WAS CHOSEN, AND THAT IS THE POINT. The cast voice took four
             cuts as a creature growl -- each one a round trip through a
             25-second render because the only instrument for judging it was
             Rick listening. `cast_lab.py` replaced that with a SPREAD: six
             characters in one file, then three depths of the winner. Two round
             trips instead of four, and both landed.

             ONE EVENT, AND THE CHARACTER IS ALL IN THE RING. A clack is easy;
             what makes it iron rather than a box is four INHARMONIC partials
             -- 139, 209, 302, 443 -- whose ratios are 1 : 1.51 : 2.18 : 3.19.
             Integer ratios would be a musical note. Real struck metal is not.

             THE 4.4kHz TICK IS BARELY SCALED DOWN while everything else drops
             by a third. It is the metal-on-metal contact, and dropping it with
             the rest is what would turn a lower clamp into a cardboard box.
             That is also the guard against the failure that killed the growl:
             39% of this sits in 200-600 Hz, so it survives a laptop. */
          this._burst(t, { freq: 4400, q: 0.7, gain: 0.40, dur: 0.030, type:"highpass" });
          this._burst(t, { freq: 594,  q: 1.2, gain: 0.40, dur: 0.13,  type:"bandpass" });
          this._tone (t, { freq: 92, to: 38,   gain: 0.46, dur: 0.55,  type:"sine" });
          [[139, 0.114, 2.3], [209, 0.087, 2.1],
           [302, 0.060, 1.8], [443, 0.038, 1.4]].forEach(
            ([f, g, d]) => this._tone(t + 0.008,
              { freq: f, to: f * 0.985, gain: g, dur: d, type:"triangle" }));
        } else if (w === "bulwarden"){'''

ULTFX_LIFE_NEW = '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
              /* THE BALLISTA WINDOW is set from `ult.dur` at the cast site,
                 the way the Thicket and Aegis are. This entry is the fallback
                 if that is ever missed. */
              %ID%: 8.6,'''


# ------------------------------------------------------- THE FATAL TICK --
# NOT A MARROWDRAW MECHANIC. Found while probing this relic and fixed here
# because this relic is the one that has to film, but it belongs to SEVEN.

FATAL_TICK_NEW = '''      if (def.dps && key !== "blessing"){
        const hp0 = f.hp;
        f.hp -= def.dps * st.stacks * dt * f.dmgTakenMul();
        if (this.rng() < dt * 8){
          const aff = Object.values(AFFINITIES).find(a => a.status === key);
          this.spawnFx(f.x, f.y, aff ? aff.glow : "#fff", 1, 60, 0.5, 3);
        }
        /* A FATAL TICK FILES A BEAT, AND AN ORDINARY ONE DOES NOT.

           THE SAME RULE, FOR THE FOURTH TIME, FROM A FOURTH DIRECTION.
           Triplicate needed it, the Thicket needed it (`_cineVine` above --
           "a lash is not a beat ... THE FATAL ONE IS KEPT"), Aegis needed it
           in v41 when 21% of Bulwarden's wins were landed by a reflection the
           director could not see. This is the same hole in `tickStatus`, and
           it is the biggest one: it belongs to every relic carrying a status
           with a `dps`, which is bloodsworn and sanctified -- SEVEN of the
           twenty-four.

           MEASURED, with a control that separates cleanly:

             Dawnbringer  44.1% of its wins   Ironhail    0.0%
             Widowmaker   31.1%               Axiom       0.0%
             Threshmaw    26.2%               Nightfell   0.0%
             Lastlight    25.7%               Bulwarden   0.0%
             Marrowdraw   23.8%
             Goreshard    20.9%
             Aureole      19.4%

           Every school with a `dps` status is between a fifth and nearly half.
           Every school without one is EXACTLY zero. Dawnbringer has been in
           01-live since v37 ending nearly half its fights on a blow the camera
           was never told about, and `cinema_clip` has been falling back to
           "the last cut" and writing clips with no ending for all of it.

           ORDINARY TICKS STILL FILE NOTHING, which is the whole distinction:
           a bleed ticks 120 times a second and filing those would hand the
           director a fight made entirely of the loser standing still.

           THE ATTRIBUTION IS THE OTHER FIGHTER, and that is sound rather than
           lazy: a status does not record who applied it, and the only statuses
           with a `dps` are hemorrhage and smite, which only bloodsworn and
           sanctified weapons carry, and neither school has a summon. The day a
           third party can apply a bleed, this needs a source on the status --
           `marrowdraw_relic_probe` asserts the precondition rather than
           trusting this comment. */
        if (hp0 > 0 && f.hp <= 0){
          const src = f === this.a ? this.b : this.a;
          this.beat({ kind: "hit", side: src === this.a ? 0 : 1,
                      x: f.x, y: f.y, dmg: def.dps * st.stacks,
                      crit: false, fatal: true, hpAfter: 0, hpFrac: 0,
                      maxHp: f.maxHp, selfHpFrac: src.hp / src.maxHp,
                      spd: src.speed, foeSpd: f.speed,
                      close: Math.hypot(src.vx - f.vx, src.vy - f.vy),
                      ranged: false, range: 0,
                      loosT: 0, lx: 0, ly: 0, shotSpd0: 0,
                      status: key, tick: true });
        }
      }'''


# THE GROWL IS GONE, AND THAT IS A DECISION RATHER THAN A RETREAT FROM ONE.
#
# Four cuts, four different wrong sounds -- "a fart", then 97.7% sub-60Hz and
# inaudible, then "rolling thunder", then a version matching Rick's reference
# recording to 6.4 points across six bands and 0.1 Hz of modulation rate that
# he still called "really far off".
#
# THAT LAST ONE IS THE INFORMATIVE FAILURE. A spectrum match that close, still
# wrong, means band shares and an AM rate do not capture what makes a growl a
# growl -- the missing thing is cycle-to-cycle JITTER and subharmonic chaos,
# which is what separates a biological voice from an oscillator, and none of
# the four attempts had any. It was a gameable metric one level up from the
# two gameable metrics that preceded it.
#
# Offered: embed his recording as PCM (guaranteed, 37.5KB, but it breaks the
# build's synth-only rule and carries a licensing question), one more synth
# attempt at the jitter, or scrap it. Rick scrapped it. The cast is a siege
# engine now, which is what short percussive synthesis is actually good at --
# every such sound this session landed on the first try.
#
# `_growl` is deleted rather than left unused. `shot.life: 3.4` has been dead
# config on five bows since v40 and is still an open decision; this build is
# not adding a sixty-line dead synth to that list.


EDITS = [
    ("the relic",
     '''    blurb:"Every plate it banks it can raise as a wall. What the wall stops, it hands back." },

];''',
     RELIC_NEW),

    ("fighter state",
     '''    this.ultAegis = null;''',
     FIGHTER_STATE_NEW),

    ("the cast",
     '''    if (u.kind === "aegis"){''',
     FIRE_ULT_NEW),

    ("tickBallista",
     '''  tickHits(self, foe, dt, cool){''',
     TICK_BAL_NEW),

    ("the tick call",
     '''    this.tickAegis(dt);''',
     TICK_CALL_NEW),

    ("the cadence",
     '''    f.fireCd -= dt;
    if (f.fireCd > 0) return;
    f.fireCd += S.cadence;
    this.spawnShot(f);''',
     CADENCE_NEW),

    ("the bolt",
     '''      seed: f.ultBloom ? (f.ultBloom.left--, true) : false,
      aff: f.aff, a,
    });
    f.shotsFired++;
    SFX.play("loose");''',
     SPAWN_NEW),

    ("the homing",
     '''      const s = this.shots[i];
      s.vy += s.grav * dt;''',
     HOME_NEW),

    ("the fork",
     '''        if (s.knock){
          const kl = Math.hypot(s.vx, s.vy) || 1;
          foe.vx += (s.vx / kl) * s.knock; foe.vy += (s.vy / kl) * s.knock;
        }
        dead = true;
      }''',
     FORK_NEW),

    ("the art",
     '''      const sp = Math.hypot(s.vx, s.vy) || 1;
      const tl = Math.min(88, sp * 0.105);''',
     DRAW_BOLT_NEW + '''
      const tl = Math.min(88, sp * 0.105);'''),

    ("the window art",
     '''  drawStatus(m, f){''',
     DRAW_DRAW_NEW),

    ("the draw call",
     '''    this.drawStatus(m, f);''',
     DRAW_CALL_NEW),

    ("the loose sound",
     '''      else if (kind === "loose"){
        /* Woody body, no top end. It sits UNDER the impacts rather than
           competing with them, so a shot landing still reads louder than
           a shot leaving. */
        this._burst(t, { freq: 380, q: 1.1, gain: 0.055, dur: 0.055, type:"bandpass" });
      }''',
     SFX_LOOSE_NEW),

    ("the ult voice",
     '''        } else if (w === "bulwarden"){''',
     SFX_ULT_VOICE_NEW),

    ("the fatal tick",
     '''      if (def.dps && key !== "blessing"){
        f.hp -= def.dps * st.stacks * dt * f.dmgTakenMul();
        if (this.rng() < dt * 8){
          const aff = Object.values(AFFINITIES).find(a => a.status === key);
          this.spawnFx(f.x, f.y, aff ? aff.glow : "#fff", 1, 60, 0.5, 3);
        }
      }''',
     FATAL_TICK_NEW),

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
    ap.add_argument("--src", default="../02-chain/sc-bulwarden.html")
    ap.add_argument("--out", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--id", default=RELIC_ID)
    ap.add_argument("--name", default=RELIC_NAME)
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--dmg", type=float, default=TUNED_RB)
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
    print("\nBLOODSWORN BOW BUILD -- the ballista window")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if '"aegis"' not in s0:
        raise SystemExit("this source has no aegis -- build off sc-bulwarden or later")
    if '"ballista"' in s0:
        raise SystemExit("this source already has a ballista -- already built")

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
    print(f"    python3 marrowdraw_probe.py --relic {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40")
    print("    python3 marrowdraw_sweep.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
