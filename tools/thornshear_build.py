#!/usr/bin/env python3
"""THORNSHEAR. The verdant twinblade, and THE WINNOWING -- the first thing in
this game that gets STRONGER the longer it stays in the air.

    python thornshear_build.py --src ../02-chain/sc-paradox-ignition.html \
                               --out ../02-chain/sc-thornshear.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in `06-docs/v47/kunai-design-v47.md`:

    "green twinblade forgoes its blades for leaf kunai. the kunai shoot off in
     both directions rapidly as a projectile. the kunai ricochet off walls and
     clanks and turn to try to hit again. kunai grow and empower after they
     ricochet and gain bonus damage and high knockback."

    "the kunai ricochet shouldnt be steering. natural and predictable ricochet
     physics"

    "instead of 2 kunai. lets do a fan of kunai and really turn the number of
     projectiles up so the ricochet shots have a better chance of connecting"

FOUR SENTENCES, ALL FOUR PRICED BEFORE THIS FILE WAS OPENED
(`kunai_probe.py`, re-run at this tip 2026-08-30, 12/12) and the design and
the survey are in `06-docs/v47/`. What the measurement decided:

    THE BILL      Forgoing the blades costs 4.46 dmg/s -- 2.76 of output it
                  stops dealing PLUS 1.70 of damage it starts taking, because
                  a bind this type LOSES still costs the foe a swing.
    THE FAN       A LOOK KNOB. A nine-fold range of fan width lands within
                  x1.13 of itself: the coverage comes from the weapon's own
                  6.47 rad/s, not from the fan. Rick picks it from a render.
    THE BOUNCE    THE MECHANIC. 69.8% of every landed kunai has bounced at
                  least once, and the same fan with no bounce budget lands
                  1359 against 2479. The growth is what the ultimate DOES.
    THE KNOCK     260, Rick's, from a priced spread of five -- and priced on
                  its own condition rather than on a clock, which is v43 §7.

## THE ONE THING THE BUILD BRIEF ASKED FOR AND THIS FILE DOES DIFFERENTLY

The brief's §7 says "do not build the fan as new machinery -- `spawnShot(f,
angle)` already takes the angle", and it is right that the fan is a loop. But
`spawnShot` reads `f.w.shot`, and a `shot` block on this relic is a twinblade
that fires ALL FIGHT: `tickFire` gates on `f.w.shot` and nothing else, so the
block would have to be defeated by a guard inside a function all five bows
live in. `spawnSpike` is the precedent and its own comment is the argument --
"deliberately NOT `spawnShot`: that function needs `f.w.shot`, and this relic
has none". So `spawnKunai` is twelve lines beside it, and:

    THE ENGINE'S SHARED RANGED PATH IS UNTOUCHED. `tickFire`, `spawnShot`,
    `relicShot`, `fireCd` -- not one character. The kunai fly, parry, bounce
    and land through `tickShots`, which is the part that had to be shared.

AND THE SPAWN GEOMETRY IS THE MEASUREMENT'S. `kunai_probe` looses from the
shell edge (`R + 6`), not from the blade tip (`R + reach`), and every number
in the design doc is that geometry. Using `spawnShot`'s would have made this
build's census a different experiment from the one that priced it.

## §3.3 OF THE BRIEF IS HALF RIGHT, AND THE HALF THAT IS WRONG IS WORTH SAYING

    "shot.life and the w.shot mode gate are both waking up here."

The MODE GATE does not wake up: this relic has no `shot`, so v39 open
decision 4 is exactly as inert as it was. `shot.life: 3.4` also stays dead
config on all five bows -- the kunai carry `ult.life`, not `shot.life`.

What DOES wake up is the branch those knobs were pointing at. `tickShots`'
`s.life <= 0` arm has never fired in this game -- bow_survey §4: "a shot
travels 1292 units in its life and the longest wall is 800" -- and it is now
the modal death of a kunai at 33.3%. Treat that branch as untested code,
because until this relic it was.

## THE FOUR PICTURE FAULTS THIS BUILD IS BUILT AGAINST

    THE CEILING       `spawnShot` honours `maxLive` by DELETING THE OLDEST
                      LIVE SHOT. On a bouncing kunai that is one vanishing in
                      mid-air -- v42's silent ultimate and v43's stuck hold, a
                      third time and foreseen. `spawnKunai` DECLINES, by whole
                      volleys, and counts the refusals.
    THE SATURATION    And the count is a design check, not a log: at fan 5 /
                      cadence 0.25 the probe refused 9090 of 11050 looses. A
                      fan permanently at the ceiling is a fan whose cadence is
                      set by a constant in CONFIG. THE SHIPPING PAIR IS THE
                      ONE ARM THAT REFUSED NOTHING (fan 5, cadence 0.60,
                      spread 1.6: 0 refused, peak 61 of 64, 2257 landed --
                      within 9% of the best arm on the board).
    THE STALE RIBBON  `f.tips` is fed from `bladeSegments`, which is empty for
                      the window -- so the swing-arc ribbons would hang in the
                      hall, unmoving, for four seconds. Cleared at the cast.
    THE GHOST BLADE   A blade drawn where no blade is live is the same class
                      of fault pointing the other way. `winnowFade` snaps to 1
                      AT THE CAST -- no frames of a drawn blade that cannot
                      hit -- and eases back over 0.25s after the window, while
                      the blades are already live.

## EVERY NUMBER BELOW IS A PLACEHOLDER AND IS MARKED AS ONE

`dmg` must be bisected against all 25 opponents (v43 §6: bisect BEFORE reading
a cell's telemetry, or the grid compares relics of different strength and
reports it as a mechanic). The growth schedule -- `growR`, `growDmg`,
`growKnock` -- is unmeasured: `kunai_probe` flew CONSTANT kunai, so every
number in the design doc is the growth's floor, not its value.
`thornshear_sweep.py` solves them, and the question to put to Rick is not a
win rate: it is WHAT SHARE OF A CAST IS CARRIED BY GROWN KUNAI.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# THORNSHEAR / THE WINNOWING. Both Rick's, from four offered each. The id
# matches the name, as it does on all 25 -- `oathwound`/Goreshard and
# `redflail`/Threshmaw are the two existing drifts and both are traps.
#
# ONE COLLISION, FLAGGED BEFORE HE CHOSE AND TAKEN ANYWAY: Lastlight's ult is
# the Harrowing. Settled, not open, and not to be relitigated here -- but the
# card and the callout lean on what the Winnowing DOES rather than on the
# word, because the word is doing less work than usual.
RELIC_ID = "thornshear"
RELIC_NAME = "Thornshear"
ULT_NAME = "The Winnowing"

# THE CARD, AND IT IS RICK'S OWN WORDING. 2026-08-30, unprompted, off the
# first-look clip: "lets also change the wording on the intro card for the ult
# 'fires a fan of kunai that ricochet. ricochets deal bonus damage'". Verbatim
# except for the two capitals every other tip in the roster carries.
#
# It is also the better line, for a reason worth keeping: the first cut said
# "For 4s the blades fly as kunai", which spends a third of a 72-character
# budget on the DURATION -- a number the viewer cannot act on and can watch for
# themselves -- and never says what the mechanic is. His says the mechanic
# twice: the fan, and then the thing that makes the fan matter.
ULT_TIP = "Fires a fan of kunai that ricochet. Ricochets deal bonus damage"

# A PLACEHOLDER, AND IT MUST BE BISECTED AGAINST THE WHOLE FIELD.
# The type ships 8.81 (Spellbreaker) .. 11.95 (Widowmaker) and it is the lowest
# damage ceiling in the game. `twinblade_survey` re-run at this tip prices
# verdant's channel on this type at +19.8% delivered against dwarven's +20.3%
# -- which is NOT what the design doc says (it reported +7.6% and called
# entangle the weakest of the three). See §0 of the build write-up. The
# expectation going in is therefore that this lands near the middle of the
# type rather than at the top of it, and that expectation is written here so
# the sweep can refute it.
#
# v41 open decision 2 is why "the whole field" is in this comment: Bulwarden's
# dmg was bisected on a five-foe subset that read 50% and the full 23-opponent
# field read 55.2% on the same number.
TUNED_TS = 10.0

# EVERY ONE OF THESE IS A PLACEHOLDER.
ULT = {
    # The roster band is 13..18. A four-second window that fills the hall
    # should not be the cheapest thing in its school.
    "charge":     16.0,
    # HOW LONG THE FAN LOOSES. The blades are gone for exactly this long and
    # the bill is 4.46 dmg/s, so this number is what the ultimate has to beat.
    "dur":         4.0,
    # SECONDS BETWEEN VOLLEYS. **NOT a look knob, and this is the one number
    # the ceiling decides.** `fan` x 2 bearings x `life` / `cadence` is the
    # steady-state population, and it must sit clear of `CONFIG.shot.maxLive`
    # (64) with the FOE's own arrows sharing the same list. At 5/0.60/3.0 that
    # is 50, and the probe measured peak 61 and zero refusals across sixteen
    # foes including all five bows.
    "cadence":     0.60,
    # KUNAI PER BEARING PER VOLLEY. **A LOOK KNOB -- Rick's, from a render.**
    # A nine-fold range lands within x1.13 of itself. He is choosing along the
    # curve `fan / cadence ~= 8.3`, not choosing freely: fan 3 / 0.36, fan 5 /
    # 0.60, fan 9 / 1.10 all cost the same population.
    "fan":         5.0,
    # HOW WIDE A VOLLEY IS, radians, tip to tip. A LOOK KNOB likewise -- the
    # weapon turns 1.6 radians between two volleys at this cadence, so the
    # SPIN is what sprays them and the fan only widens a volley that was
    # already sweeping.
    "spread":      1.6,
    # A kunai's launch speed. 260 cost 4% of connections and 4% of the bounce
    # distribution; sweep it lightly.
    "speed":     420.0,
    # THE FRESH KUNAI. Both grow -- see growR/growDmg below.
    "r":          10.0,
    "dmgMul":      0.15,
    # THE BINDING CONSTRAINT, AND IT IS NOT `bounce`. Each bounce costs 12% of
    # speed (`s.vx *= 0.88`), so at life 3.0 NOTHING reaches a fourth: bounce 6
    # and bounce 3 return identical numbers, digit for digit. Three rungs
    # unless this goes up, and raising it is a PICTURE decision as much as a
    # balance one (kunai visibly stay in the hall longer). Both arms are in
    # the sweep. At 6.0 the landed count rises 2479 -> 2764.
    "life":        3.0,
    "bounce":      3.0,
    # RICK'S, flat, from a spread of 0 / 120 / 260 / 420 / 700 -- and priced on
    # its own condition (every landed kunai, along the kunai's travel) rather
    # than as one synthetic shove on a clock, which measured NOTHING and is
    # v43 §7's trap arriving on a second weapon. It is the ULTIMATE that pays:
    # landed 2479 -> 2242, and the dead time before the blades reconnect after
    # the cast goes 1.40s -> 2.56s.
    "knock":     260.0,
    # THE GROWTH, PER RUNG, AND THE THREE OF THEM ARE THE ONLY NUMBERS IN THIS
    # BLOCK NOTHING HAS MEASURED. `kunai_probe` flew CONSTANT kunai, so every
    # census number in the design doc is this schedule at 1.0/1.0/1.0. At the
    # measured mean of 1.59 bounces a landed kunai carries x1.5^1.59 = x1.9 of
    # its fresh damage, and at the top rung x3.4.
    "growr":       1.25,
    "growdmg":     1.50,
    "growknock":   1.30,
    # HOW LONG A KUNAI CANNOT BE PARRIED AGAIN FOR after a blade bats it.
    # Not a design knob: without it a kunai sits inside the parry radius of the
    # blade that just hit it and racks a rung every frame. `arm` is the field
    # `tickShots` already gates both hit branches on, so this costs no new
    # state and no new branch.
    "parryarm":    0.06,
    # THE DIRECTOR'S DENSITY. `beat()`'s own comment: "anything that puts extra
    # CUTS on the floor belongs in this loop", and this window puts ~19 landed
    # projectiles on the floor in four seconds -- more than the spike storm,
    # which is the relic that forced `crowdMul` to exist. 10 is the storm's
    # value and it is a placeholder here: it wants the same measurement the
    # storm got (`beat_dist.py`, cut preference inside the window against out).
    "crowdmul":   10.0,
}


# --------------------------------------------------------------- the relic --

RELIC_NEW = r'''    blurb:"A pit chain swung inside its own storm. Stand in it long enough and the argument is over." },

  /* THORNSHEAR -- the verdant twinblade, and the twenty-sixth relic. Physics
     are Widowmaker's and Spellbreaker's and Twinshade's exactly (the type owns
     them, field for field); the school owns Entangle and the green, and
     SHAPES._tbGrown has drawn this weapon since before it existed.

     THE CELL, measured before the design existed (`twinblade_survey.py`):

       139.6 UNITS OF LIVE EDGE ON THE SHORTEST REACH IN THE GAME. Two opposed
       70-unit segments, each with its own 0.45s `hitCd`, and both of them
       land -- 278 blows against 263, so the weaker blade carries 48.6% of the
       type's contacts. That is MORE live edge than a greatsword's 127.5.

       AND IT IS THE LEAST EFFICIENT MELEE WEAPON IN THE GAME PER RADIAN.
       0.0422 contacts a radian against a warhammer's 0.1068: it turns 3.4x as
       fast to land 1.34x the blows. It is paid 8.3-11.9 a hit for it, the
       lowest ceiling in the game.

       AND IT LOSES EVERY BIND IT TAKES. 100% lost against every other type,
       and the only bind it does not lose is the mirror, which is 213/213
       deadlocks. The sharpest version of the mass ladder anywhere.

     So the weapon's problem is not that it cannot touch anything -- it is that
     everything it touches costs more than it earns. THE WINNOWING STOPS
     TOUCHING. For four seconds the blades are gone (no hits, no binds, no
     parry, and a measured bill of 4.46 damage a second) and the hall does the
     work instead: a fan out of both bearings, and every wall and every blade
     in it makes what comes off it BIGGER.

     `dmg` is a PLACEHOLDER (thornshear_build.TUNED_TS) and MUST be bisected. */
  { id:"%ID%", name:"%NAME%", aff:"verdant", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:%DMG%, spin:5.7, mode:"spin", mass:1.1,
    onHit:{ entangle:2 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"winnow",
          dur:%DUR%, cadence:%CADENCE%, fan:%FAN%, spread:%SPREAD%,
          speed:%SPEED%, r:%R%, dmgMul:%DMGMUL%, life:%LIFE%, bounce:%BOUNCE%,
          knock:%KNOCK%,
          /* THE GROWTH. §1's fourth sentence, and the only sentence in it
             that nothing else in this game owns: Ironbloom's shards are
             constant across their three bounces, the Harrowing's scythes are
             constant, and Bloodhunt's forks get WEAKER (forkDmg 0.5). The
             only precedent for a projectile changing after it resolves once
             is one that decays. UNMEASURED -- see the builder. */
          growR:%GROWR%, growDmg:%GROWDMG%, growKnock:%GROWKNOCK%,
          parryArm:%PARRYARM%,
          /* THE DIRECTOR'S DENSITY, not a balance number. See `beat()`. */
          crowdMul:%CROWDMUL%,
          /* THE NUMBER IN THIS LINE IS SUBSTITUTED, not typed. v40 shipped a
             card reading "5s" after a sweep moved the number to 8.1 and
             nothing caught it, because verify.py only asks that a tip EXISTS.
             And verify.py fails an ult tip over 72 characters, which v43 hit
             for the first time in the project.

             A PLACEHOLDER UNTIL RICK WORDS IT -- the scrunch card is one of
             the seven things this project asks him for. It leans on what the
             ultimate DOES rather than on its name, because "the Winnowing"
             collides with "the Harrowing" and the word is carrying less than
             usual. */
          tip:"%TIP%" },
    blurb:"A hedge-blade that lets go of its edges. What it throws comes back off the wall bigger than it left." },

];'''


# ------------------------------------------------------------ fighter state --

FIGHTER_STATE_NEW = r'''    this.pinV = null;
    /* {t, dur, cd, volleys, loosed, refused, rungs} while the Winnowing is
       loosing. null on every other relic and on this one outside its own
       window, which is the whole zero-burden argument: `tickWinnow` returns
       after a two-iteration loop that does nothing, `bladeSegments`' first
       line is a comparison against null, and the two branches in `tickShots`
       are `if (s.kunai)` on a field no other projectile carries. */
    this.ultWinnow = null;
    /* PRESENTATION ONLY: 1 while the blades are gone, easing back to 0 over
       0.25s after the window closes. It SNAPS to 1 at the cast rather than
       easing in, and the asymmetry is the point -- a blade drawn while it
       cannot hit is a picture fault of exactly the class §4.1 exists for, and
       a blade drawn small while it CAN hit is only a weapon re-forming. */
    this.winnowFade = 0;'''


# ---------------------------------------------------------------- the cast --

FIRE_ULT_NEW = r'''    if (u.kind === "winnow"){
      /* NOTHING RESOLVES HERE. This ultimate does not deal damage at the cast;
         it changes what the weapon IS for a window, the same shape as the
         Thicket, the ballista and Bloodmill. The first volley leaves on this
         frame -- `cd` starts at 0 -- so the blades are not replaced by a
         pause, they are replaced by kunai.

         THE RIBBONS ARE CLEARED, and that is not tidiness. `f.tips` is fed
         from `bladeSegments`, which returns nothing for the whole window, so
         two swing-arc ribbons would hang motionless in the hall for four
         seconds -- a picture fault with no number attached to it, which is
         this project's own defect class. They grow back from empty when the
         blades do. */
      f.ultWinnow = { t: 0, dur: u.dur, cd: 0, volleys: 0, loosed: 0,
                      refused: 0, rungs: 0 };
      f.winnowFade = 1;
      for (const tp of f.tips) tp.length = 0;
      /* The fx clock runs at 2x sim time -- `decay()` calls `tickPresentation`
         once directly and once through `decayImpactOnly` -- so every `life` in
         this engine is in half-seconds. The map entry in the table above is
         only the fallback if this is missed. */
      this.ultFx.life = (u.dur + 0.7) * 2;
      return;
    }

    if (u.kind === "ballista"){'''


# ------------------------------------------------------- forgoing the blades --

BLADE_SEGMENTS_NEW = r'''  bladeSegments(f){
    /* FORGOING THE BLADES, and it is ONE mutation reaching all four consumers.
       §1's first sentence means exactly this in this engine: `tickHits` lands
       nothing, `_clankPair` finds no crossing, `tickShots`' parry has no
       segment to bat with, and `tickWeapon` has no tip to record. Suppressing
       those four separately would be four chances to disagree, which is why
       `kunai_probe` priced the sentence by emptying `blades` and why this is
       the line that implements it.

       IT IS ALSO THE ULTIMATE'S ENTIRE BILL, MEASURED: 2.76 dmg/s of output
       it stops dealing plus 1.70 dmg/s it starts taking = 4.46 dmg/s. The
       second half was a refutation -- twenty binds a minute that this type
       LOSES 100% of were still worth more as interruption than they cost as
       stagger, because a bind the twinblade loses still costs the foe a swing.

       `ultWinnow` is null on every other relic and on this one outside its
       own window, so this is a comparison against null on a field nothing
       else writes. */
    if (f.ultWinnow) return [];
    const mods = this.actMods;'''


# --------------------------------------------------------------- the window --

TICK_WINNOW_NEW = r'''      if (A.t >= A.dur) f.ultAegis = null;
    }
  }

  /* ------------------------------------------------------------- WINNOW --
     THE WINNOWING. The blades come off, and for four seconds a fan of leaf
     kunai looses out of both bearings and the HALL does the work: every wall
     and every blade a kunai comes off makes it bigger, harder and heavier.

     THIS IS THE ONLY THING IN THE GAME THAT GETS STRONGER FOR STAYING IN THE
     AIR, and that is not a claim, it is the roster: Ironbloom's nine shards
     are constant across their three bounces, the Harrowing's twelve scythes
     are constant, and Bloodhunt's forks are explicitly WEAKER than the bolt
     that made them. The measurement that says the growth is a mechanic rather
     than decoration is `kunai_probe [4]`: 69.8% of every landed kunai arrives
     having bounced at least once, and the same fan with the budget set to
     zero lands 1359 against 2479.

     WHY THE FAN IS NOT SWEPT. `kunai_probe [4]` flew fan 1, 3, 5 and 9 and
     every one landed within x1.13 of every other, because a twinblade turns
     6.47 rad/s -- the fastest weapon in the game by 66% -- and between two
     volleys 0.6s apart it has turned nearly four radians. THE SPIN IS WHAT
     SPRAYS THEM; the fan only widens a volley that was already sweeping. So
     the fan and the spread are LOOK KNOBS and they are Rick's, off a render.
     That is v43 §4.2 arriving in a different costume: the hexagon was a
     picture and the radius was the mechanic; here the fan is a picture and
     the BOUNCE is the mechanic.

     RETURNS ON ITS FIRST LINE for every relic that is not casting -- past a
     two-iteration loop that does nothing when nobody is inside a window and
     nobody has a fade left to run down. */
  tickWinnow(dt){
    for (const f of [this.a, this.b]){
      /* PRESENTATION ONLY, and it is deliberately outside the window guard:
         the fade has to keep running for a quarter second AFTER the window
         closes. Nothing in the simulation reads it. */
      if (!f.ultWinnow && f.winnowFade > 0)
        f.winnowFade = Math.max(0, f.winnowFade - dt / 0.25);
      const W = f.ultWinnow;
      if (!W) continue;
      W.t += dt;
      /* THE WINDOW ENDS AND THE KUNAI IN THE AIR STAY IN THE AIR -- and with
         them their bounce budgets, so the last volley is still growing for a
         second and a half after the blades are back. A kunai is a committed
         object: it was loosed, the viewer watched it go, and deleting it
         because a clock ran out would take away a hit already earned. The
         ballista's bolts and the Thicket's seeds outlive their windows for
         the same reason. */
      if (W.t >= W.dur || !f.alive){ f.ultWinnow = null; continue; }

      W.cd -= dt;
      if (W.cd > 0) continue;
      W.cd += f.w.ult.cadence;

      const u = f.w.ult, n = u.fan | 0;
      /* THE TWO BEARINGS ARE THE WEAPON'S OWN, read out of `w.blades` rather
         than written here as 0 and pi. §1 says the kunai leave "in both
         directions", and both directions is what this weapon already IS --
         two opposed segments at offsets 0 and 0.5. A second copy of that pair
         in this function would be a second source of truth for the one
         property the type is defined by. */
      const per = n * f.w.blades.length;
      /* THE CEILING, DECLINED. `CONFIG.shot.maxLive` is 64 and `spawnShot`
         honours it by SHIFTING THE OLDEST LIVE SHOT OUT -- which on a bouncing
         kunai is one vanishing in mid-air: no error, no invariant broken, no
         win rate moved, and only a person watching can see it. That is v42's
         silent ultimate and v43's stuck hold a third time, and unlike both of
         those it was foreseen. The Bloodhunt fork branch already refuses to
         spawn instead and says why; so does this.

         BY WHOLE VOLLEYS, not by kunai. Half a fan is its own picture fault --
         an asymmetric spray with no cause the viewer can see -- and the count
         is a design check rather than a log: at fan 5 / cadence 0.25 the probe
         refused 9090 of 11050 looses, which is a design whose cadence is
         decided by a constant in CONFIG. The shipping pair refuses none.

         THE FOE'S ARROWS SHARE THIS LIST, which is why the test is against
         the live length and not against this relic's own count. */
      if (this.shots.length + per > CONFIG.shot.maxLive){ W.refused += per; continue; }

      for (const off of f.w.blades){
        for (let k = 0; k < n; k++){
          const sp = n === 1 ? 0 : -u.spread / 2 + u.spread * (k / (n - 1));
          this.spawnKunai(f, f.theta + off * TAU + sp);
          W.loosed++;
        }
      }
      W.volleys++;
      /* ONE SOUND PER VOLLEY, not one per kunai. Ten kunai leaving on the same
         frame are one event; ten copies of a loose would be a transient
         stacked ten deep and would read as a single loud click. */
      SFX.play("loose", { leaf: true });
    }
  }

  /* A KUNAI LEAVES THE SHELL, travelling along the bearing it was handed.

     Deliberately NOT `spawnShot`, and `spawnSpike` is the precedent with the
     argument already written in it: `spawnShot` reads `f.w.shot`, and a `shot`
     block on this relic is a twinblade that fires ALL FIGHT -- `tickFire`
     gates on `f.w.shot` and on nothing else. Reusing it would mean defeating
     it with a guard inside a function all five bows live in, to borrow twelve
     lines. The engine's shared ranged path is untouched by this relic.

     AND THE SPAWN POINT IS THE SHELL EDGE, NOT THE BLADE TIP. `R + 6` is what
     `kunai_probe` loosed from and every number in the design doc is that
     geometry; `spawnShot`'s `R + reach` would have put the census 62 units
     further out and made this build a different experiment from the one that
     priced it. It is also the picture §1 asks for: the blades are GONE, so
     there is no tip for anything to leave from.

     `dmgMul` prices the kunai against the WEAPON's damage the way Ironbloom's
     pop and the flail's spike do, so the sweep can move `dmg` without moving
     what a kunai means. Everything else -- crit, jitter, the Sunder
     multiplier, Entangle, hit stop, hitstun and `self.hits++` for verify.py's
     six-hit floor -- comes free from `resolveHit`, which the shot path
     already routes through. */
  spawnKunai(f, a){
    const u = f.w.ult, R = CONFIG.physics.ballR;
    const ca = Math.cos(a), sa = Math.sin(a);
    this.shots.push({
      own: f === this.a ? "a" : "b",
      x: f.x + ca * (R + 6), y: f.y + sa * (R + 6),
      /* CINEMA (demo): where it was loosed from and how fast the caster was
         moving. Dead data as far as the sim is concerned. */
      x0: f.x, y0: f.y, spd0: f.speed, t0: this.t,
      vx: ca * u.speed, vy: sa * u.speed,
      r: u.r, life: u.life, max: u.life, grav: 0,
      dmgMul: u.dmgMul, knock: u.knock, arm: 0,
      bounce: u.bounce | 0,
      /* THE RUNG. One counter, read by the growth, by the art and by nothing
         else. `kunai` is the flag every branch this build adds tests, and it
         is false on every projectile any other relic fires -- and on this
         one, which fires nothing else. */
      kunai: true, rung: 0,
      /* NO `home`, AND THAT IS THE DESIGN. Rick amended §1 unprompted: "the
         kunai ricochet shouldnt be steering. natural and predictable ricochet
         physics." `s.home` exists and works -- Bloodhunt steers on it -- and
         leaving it undefined is the decision, not an omission. */
      aff: f.aff, a,
    });
    f.shotsFired++;
  }

  /* WHAT A RICOCHET DOES TO A KUNAI. §1's fourth sentence, and the one thing
     in it nothing else in this game owns.

     ONE definition, called from both reflection paths -- the wall and the
     parry -- because "grow and empower after they ricochet" does not
     distinguish between them and neither should the code. A second copy would
     be a second growth schedule the day somebody tunes one of them.

     THE SPEED LOSS IS NOT HERE. The wall branch's `*= 0.88` is the shipped
     splinter rule and it stays exactly where it is; the parry path applies it
     itself. It is also the reason the growth has three rungs and not six:
     twelve percent a bounce means nothing reaches a fourth inside `life 3.0`,
     measured, digit for digit, at bounce 3 and bounce 6. */
  kunaiRung(s, src){
    const u = src.w.ult;
    s.rung++;
    s.r *= u.growR;
    s.dmgMul *= u.growDmg;
    s.knock *= u.growKnock;
    /* AND THE THING IT JUST GREW OUT OF HAS TO BE GIVEN BACK. This is the
       first projectile in this game whose RADIUS changes after it has been
       placed, and every wall test in `tickShots` is written against the
       radius at the moment it runs:

         the bounce branch clamps `s.x = n + s.r` -- with the OLD r --
         the spent branch then asks `s.x < n + s.r` -- with the NEW one --

       so a kunai that grew on the wall it just bounced off was one pixel
       outside itself and was spent on the same frame it ricocheted. MEASURED,
       and it is why this line exists rather than a paragraph arguing for it:
       89% of every kunai died on a wall at a median age of 0.33 seconds, the
       rung histogram was 500 at one and 33 at three, and the peak in flight
       was 20 against a predicted 50. Every one of those numbers is the same
       missing clamp.

       It is not only the wall path. A parry inside `s.r * growR` of a wall
       puts a grown kunai outside the hall with nothing having touched it, so
       the clamp belongs HERE -- in the one function both reflections call --
       rather than in the branch that happened to find it. */
    const AR = CONFIG.arena, ins = this.inset;
    s.x = clamp(s.x, ins + s.r, AR.w - ins - s.r);
    s.y = clamp(s.y, ins + s.r, AR.h - ins - s.r);
    /* THE INTERPOLATOR MUST NOT TWEEN THROUGH THE THING IT CAME OFF. The wall
       branch sets this and says so; every reflection path this build adds sets
       it too.

       AND IT IS CURRENTLY INERT, WHICH IS WORTH KNOWING RATHER THAN
       DISCOVERING. Nothing reads `s.snap`: `LERP_FIELDS.shot` is ["x","y"]
       and `CINE.snapObj` only copies numbers, so a boolean is invisible to it.
       What actually saves the picture is that both reflection paths reflect
       VELOCITY and leave POSITION where the step put it, so the previous and
       current positions are both on the legal side of the surface and there
       is nothing to tween through. `thornshear_relic_probe [7]` asserts the
       flag is set AND states that it is decorative until something reads it. */
    s.snap = true;
    this.spawnFx(s.x, s.y, src.aff.glow, 4 + s.rung * 2, 140, 0.26, 2.4);
    /* THE TOP RUNG IS AN EVENT AND THE ONES BEFORE IT ARE NOT.
       19.1% of every kunai reaches the budget, which is ~13 a cast; the other
       two rungs happen ~110 times a cast. A sound and a beat on every rung
       would be a wash of noise and would evict the fight's own beats -- the
       list is capped at 600 and SHIFTS.

       So the payoff frame is the one that speaks: a fully grown kunai, and it
       is the moment §1's fourth sentence completes. */
    if (s.rung < (src.w.ult.bounce | 0)) return;
    this.ring(s.x, s.y, src.aff.core, 2, 34, 0.22, 3);
    /* ONE GATE FOR THE SOUND AND THE BEAT, and the number behind it moved
       once already. `kunai_probe` measured 19.1% of kunai reaching the third
       bounce -- but it flew CONSTANT kunai, and a growing one is fatter every
       time it comes off something and gets parried more. Measured on this
       build: 55% arrive fully grown, which is 38 a cast and not 13. A chime
       ten times a second is a wash, and a beat that often would evict the
       fight's own -- `beats` is capped at 600 and SHIFTS. */
    /* RULE 3, SIXTH RELIC RUNNING. The kunai land through `resolveHit`, so
       ordinary hits file their own beats -- but nothing in the frame knows a
       kunai just finished growing, and that is the legible moment of this
       ultimate. Rate limited to 0.4s: the director wants the moment, not a
       hundred and thirteen of them. Written to a list the simulation never
       reads; `engine_ab` is the proof of that, not this comment. */
    if (this._winnowBeat !== undefined && this.t - this._winnowBeat < 0.4) return;
    this._winnowBeat = this.t;
    SFX.play("ult", { w: "thornshear-rung", n: s.rung });
    const foe = src === this.a ? this.b : this.a;
    this.beat({ kind: "ult", side: src === this.a ? 0 : 1, x: s.x, y: s.y,
                w: src.w.id, foeHpFrac: foe.hp / foe.maxHp });
  }'''

TICK_CALL_NEW = r'''    this.tickWinnow(dt);
    this.tickBallista(dt);'''


# ------------------------------------------------------------- the ricochet --

PARRY_NEW = r'''      for (const q of segs){
        const d = segDist(q.ax, q.ay, q.bx, q.by, s.x, s.y).d;
        if (d < s.r + foe.w.width * 0.5 + CONFIG.shot.pad){
          /* A KUNAI IS BATTED BACK, NOT OUT OF THE AIR. §1: "the kunai
             ricochet off walls and clanks." RICK TOOK THE LITERAL READING
             FROM THREE PRICED OPTIONS -- deflect-only, deflect-AND-empower,
             and parry-kills-it -- and he took the boldest: the only
             counterplay to this ultimate FEEDS it.

             IT HAS A MEASURED COST AND IT POINTS THE SAME WAY THE SCHOOL DOES.
             Parry rate by the foe's mode: swing 29.1%, spin 18.9%, ranged
             14.9%, chain 12.1%. A greatsword bats away nearly a third of every
             kunai loosed at it -- and entangle is worth -36.2% against a
             swinging foe and -3.3% against a bow. Seven greatswords, five
             bows. THE REGISTERED PREDICTION this build exists to falsify is
             that this relic's win-rate spread will be the widest in the game;
             if the finished spread sits inside the existing band, the
             prediction was wrong and the concentration argument gets struck
             rather than explained away.

             THE BUDGET IS SHARED WITH THE WALL and that is deliberate: it is
             one number for "how many times can this come off something", so a
             kunai that has spent it dies on the next blade exactly as an arrow
             does. The counterplay is not removed, it is delayed by three.

             `s.arm > 0` IS NOT A KILL. A kunai that has just been batted is
             still inside the blade's radius on the next frame or two, and
             without this it would rack a rung every frame against a blade it
             is passing. It breaks out of the parry loop still alive, and both
             hit branches below are already gated on the same field. */
          if (s.kunai){
            if (s.arm > 0) break;
            if (s.bounce > 0){
              const bl = Math.hypot(s.vx, s.vy) || 1;
              /* MIRRORED IN THE BLADE, which is the reflection a viewer can
                 predict from the picture: the component along the edge is
                 kept and the component into it is reversed. Nothing here
                 reads the blade's rotation -- a spinning edge that also
                 imparted its own speed would be the steering Rick's amendment
                 refused, arriving through the back door. */
              const bx = Math.cos(q.a), by = Math.sin(q.a);
              const dp = s.vx * bx + s.vy * by;
              s.vx = (2 * dp * bx - s.vx) * 0.88;
              s.vy = (2 * dp * by - s.vy) * 0.88;
              s.a = Math.atan2(s.vy, s.vx);
              s.bounce--;
              s.arm = src.w.ult.parryArm;
              this.spawnFx(s.x, s.y, "#FFF4D0", 7, 210, 0.30, 3.0);
              this.shake = Math.min(38, this.shake + 3);
              SFX.play("clank");
              this.kunaiRung(s, src);
              break;
            }
          }
          this.spawnFx(s.x, s.y, "#FFF4D0", 9, 240, 0.34, 3.2);
          this.ring(s.x, s.y, foe.aff.glow, 3, 46, 0.22, 3);
          this.shake = Math.min(38, this.shake + 4);
          SFX.play("clank");
          dead = true; break;
        }
      }'''

WALL_NEW = r'''        if (hitWall){
          s.bounce--;
          s.vx *= 0.88; s.vy *= 0.88;
          s.a = Math.atan2(s.vy, s.vx);
          s.snap = true;          // the interpolator must not tween through a wall
          this.spawnFx(s.x, s.y, s.aff.glow, 5, 130, 0.24, 2.4);
          SFX.play("wall");
          /* AND THE WALL IS THE OTHER HALF OF §1's THIRD SENTENCE. v40
             measured 82% of every arrow in this game spent on a wall; a
             bouncing kunai spends 0.1%, because the modal fate of every
             projectile here has been turned into the mechanic. */
          if (s.kunai) this.kunaiRung(s, src);
        }'''

SPENT_NEW = r'''      if (!dead && (s.life <= 0
          || s.x < n + s.r || s.x > A.w - n - s.r
          || s.y < n + s.r || s.y > A.h - n - s.r)){
        /* A KUNAI SPENDS ITSELF RATHER THAN BLINKING OUT, and this branch is
           why it needs to. EXPIRY IS THE MODAL DEATH OF A KUNAI at 33.3% --
           this arm of `tickShots` has never fired in this game before this
           relic (bow_survey §4: "a shot travels 1292 units in its life and the
           longest wall is 800"), so it is untested code carrying a third of
           the population. A grown kunai reaching the end of its life with no
           picture attached is the same silent fault as one deleted at the
           ceiling; it comes apart into leaf instead, larger the more it grew. */
        if (s.kunai)
          this.spawnFx(s.x, s.y, s.aff.glow, 5 + (s.rung || 0) * 3,
                       70 + (s.rung || 0) * 30, 0.42, 2.2);
        else
          this.spawnFx(s.x, s.y, s.aff.core, 4, 110, 0.26, 2.2);
        dead = true;
      }'''


# ------------------------------------------------------------ the director --

CROWD_NEW = r'''      if (f.ultTrace){
        o.crowd = true;
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);
      }
      /* v47: AND THE WINNOWING, WHICH IS THE DENSEST OF THE THREE. Triplicate
         crowds with BODIES, the spike storm with PROJECTILES and the Converse
         with contacts at four times the closing speed -- this window puts
         seventy projectiles and ~19 landed hits on the floor in four seconds,
         which is the spike storm's problem with a bigger number.

         The comment above generalised the rule to "anything that puts extra
         CUTS on the floor belongs in this loop", and this is the first relic
         built after that sentence rather than before it. `crowdMul` is a
         PLACEHOLDER at the storm's own 10 and wants the same measurement the
         storm got: cut preference inside the window against outside. */
      if (f.ultWinnow){
        o.crowd = true;
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);
      }'''


# ------------------------------------------------------------------- art --

KUNAI_ART_NEW = r'''      /* A LEAF KUNAI. Not an arrow -- an arrow reads by its 9:1 aspect ratio
         and anything borrowing it says "this is archery", which is the one
         thing this window is not -- and not a splinter, a seed or a scythe
         either. It is a leaf with a point on it: a blade the hedge grew.

         IT POINTS WHERE IT IS GOING, and that is legibility rather than
         style. This is the only projectile in the game whose direction the
         viewer has to be able to predict, because the whole mechanic is that
         it is about to come off something and arrive from somewhere else.
         So the tumble every other projectile here uses is replaced by a
         FLUTTER: a small deterministic wobble about the heading, derived from
         elapsed life (`s.max - s.life`) rather than accumulated, so it steps
         with the 120Hz sim instead of strobing against the interpolator --
         the same construction rule the splinter's tumble and the Harrowing's
         spin use, and for the same reason.

         AND IT GROWS. `s.r` is the simulation's own number, tripled across
         three rungs by `kunaiRung`, so the thing the viewer sees getting
         bigger IS the thing that is hitting harder. The rung adds a hot edge
         and a wider halo on top of that -- light, not size, because the size
         is already true. */
      if (s.kunai){
        const rg = s.rung || 0;
        const age = s.max - s.life;
        const ang = s.a + Math.sin(age * 16 + s.a * 3.1) * 0.20;
        const dim = clamp(s.life / 0.35, 0, 1);
        const hot = clamp(rg / 3, 0, 1);
        /* THE KUNAI, and the proportions ARE the read. Rick, watching the
           first-look clip: "the blades dont look like kunai" — and then the
           brief, in five words: "kunai first, leaf second." What shipped was a
           pointed ellipse with a midrib, so the verdant flavour was carrying
           the whole silhouette and the weapon was carrying none of it.

           THREE THINGS SAY KUNAI AT THIRTY-SEVEN PIXELS, in this order:

             THE TANG      the object is longer than its blade and the back
                           half is dark and narrow. A blade with no handle is
                           a leaf, whatever shape it is.
             THE RING      the one feature nothing else in this game has. Four
                           pixels across on a fresh kunai and it still reads,
                           because it is a HOLE and nothing else on screen is.
             THE SHOULDER  a kunai's blade widens ABRUPTLY and then tapers. A
                           leaf's widest point is halfway along and its edges
                           are convex — that single difference is most of what
                           separates the two.

           So the furniture is a kunai's and the BLADE is the leaf: convex
           edges between shoulder and nose, a bright midrib, two veins. Rick's
           pick from four rendered candidates (`kunai_art_lab.py`,
           `05-reference/v47/kunai-shapes.png` and `kunai-in-hall.png`) — the
           spread ran from a steel kunai with leaves trailing off the ring to
           a kunai grown out of a woody stem, and the sheet with fourteen of
           them at once is why it was a spread: a silhouette that reads alone
           can still turn to soup in a crowd of fifty. */
        const L = s.r * 1.85, W = s.r * 0.52, TW = s.r * 0.17;
        const NOSE = L, SHO = L * 0.30, HILT = -L * 0.06;
        const BUTT = -L * 0.74, RING = -L * 0.86, RINGR = L * 0.13;
        c.globalCompositeOperation = "lighter";
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * (1.6 + 0.9 * hot));
        gh.addColorStop(0, s.aff.glow + (rg ? "AA" : "77"));
        gh.addColorStop(1, s.aff.glow + "00");
        c.globalAlpha = (0.45 + 0.35 * hot) * dim; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * (1.6 + 0.9 * hot), 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.save();
        c.translate(s.x, s.y); c.rotate(ang);
        c.globalAlpha = dim;
        /* THE TANG AND THE RING, drawn first so the blade sits over the
           shoulder of the tang. Inked off the SCHOOL's own dark rather than a
           hard-coded near-black: `_twinDagger`'s own note is the record of
           "#00000055" being one black at 33% for all 48 cells, which is a
           shadow the palette cannot reach. */
        c.strokeStyle = SHAPES._ink(s.aff.dark, 9.71);
        c.lineWidth = TW * 2;
        c.beginPath(); c.moveTo(HILT, 0); c.lineTo(BUTT, 0); c.stroke();
        c.lineWidth = Math.max(1, s.r * 0.13);
        c.beginPath(); c.arc(RING, 0, RINGR, 0, TAU); c.stroke();
        /* THE BLADE: a kunai's shoulder, a leaf's edges between shoulder and
           nose. One closed path, so at phone size it is a shape and not a
           collection of strokes. */
        const blade = (k) => {
          c.beginPath();
          c.moveTo(NOSE * k, 0);
          c.quadraticCurveTo(SHO * k, -W * 1.30 * k, HILT * k, -W * 0.36 * k);
          c.lineTo(HILT * k, W * 0.36 * k);
          c.quadraticCurveTo(SHO * k,  W * 1.30 * k, NOSE * k, 0);
          c.closePath();
        };
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.71);
        blade(1.10); c.fill();
        c.fillStyle = s.aff.core;
        blade(1.0); c.fill();
        /* the midrib, and the two veins — the only leaf detail that survives
           to thirty-seven pixels. The rib goes WHITE the moment a kunai has
           grown, so the rung is legible on a single object rather than only
           by comparison with a fresh one beside it. */
        c.strokeStyle = rg ? "#FFFFFF" : s.aff.glow;
        c.lineWidth = Math.max(0.8, s.r * (0.10 + 0.06 * hot));
        c.beginPath();
        c.moveTo(HILT, 0); c.lineTo(NOSE * 0.92, 0); c.stroke();
        c.lineWidth = Math.max(0.6, s.r * 0.05);
        c.globalAlpha = dim * 0.6;
        for (let v = -1; v <= 1; v += 2){
          c.beginPath();
          c.moveTo(SHO * 0.2, 0); c.lineTo(SHO * 1.15, v * W * 0.70); c.stroke();
        }
        c.globalAlpha = dim;
        if (rg){
          c.globalAlpha = dim * (0.35 + 0.45 * hot);
          c.strokeStyle = "#EAFBE4"; c.lineWidth = Math.max(0.8, s.r * 0.09);
          blade(1.0); c.stroke();
        }
        c.restore();
        c.globalAlpha = 1;
        continue;
      }
      if (s.seed){'''

BLADE_DRAW_NEW = r'''    for (const off of f.w.blades){
      const a = f.theta + off * TAU;
      c.save();
      /* THE BLADES ARE GONE. §1's first sentence, in the picture: for the
         whole of the Winnowing `bladeSegments` returns nothing, so a blade
         drawn here would be a weapon the viewer can see and the hall cannot
         touch -- v42's silent ultimate and v43's stuck hold are both exactly
         this shape, a picture and a simulation disagreeing with no number
         between them to notice.

         `winnowFade` SNAPS to 1 at the cast and eases back over 0.25s after
         the window, so the disagreement can only ever run the safe way round:
         never a blade drawn that cannot hit, only a blade drawn small that
         can. Zero on every other relic, so this is a comparison against zero
         on a field nothing else writes. */
      const wk = 1 - (f.winnowFade || 0);
      if (wk < 0.02){ c.restore(); continue; }
      c.globalAlpha = dim * wk;
      c.translate(f.x, f.y);
      c.rotate(a);
      c.translate(R - 6, 0);
      if (wk < 1) c.scale(wk, wk);'''

DRAW_UNDER_NEW = r'''    /* ---- THE WINNOWING, under ------------------------------------------
       Deliberately SMALL, and for the same reason the Thicket's and the
       Harrowing's are: everything a viewer needs in order to read this
       ultimate is already a simulation object -- the blades gone, seventy
       leaves in the air, each one visibly bigger every time it comes off
       something. A set-piece competing with that would be light drawn on top
       of light.

       WHAT IS HERE IS THE ONE THING THE SIM CANNOT SAY BY ITSELF: THE WALLS
       ARE THE WEAPON. A bouncing kunai spends 0.1% of itself on a wall where
       an arrow spends 82%, and the reason the ultimate works is that the four
       walls are feeding it. So the hall lights at the cast and gutters out as
       the window closes -- and the corners are brightest, because a corner is
       two ricochets.

       AND THE BLADES LEAVING. Two arcs sweeping out along the bearings the
       first volley left on, for a third of a second, so the swap from weapon
       to projectile is an event rather than a cut. */
    if (u.w === "%ID%"){
      const dur = Math.max(0.01, u.life - 0.7);
      const k2 = clamp(u.t / dur, 0, 1);
      const A2 = CONFIG.arena, ins = m.inset;
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = (1 - k2) * 0.26 + 0.05;
      c.strokeStyle = u.aff.glow;
      c.lineWidth = 3 + 6 * (1 - k2);
      c.shadowColor = u.aff.core; c.shadowBlur = 18;
      c.strokeRect(ins + 3, ins + 3, A2.w - 2 * ins - 6, A2.h - 2 * ins - 6);
      c.shadowBlur = 0;
      /* the corners, where two walls meet and a kunai gets two rungs */
      c.globalAlpha = (1 - k2) * 0.40 + 0.06;
      c.lineWidth = 4 + 7 * (1 - k2);
      const cl = 58;
      for (const [cx, cy, sx, sy] of [[ins + 3, ins + 3, 1, 1],
                                      [A2.w - ins - 3, ins + 3, -1, 1],
                                      [ins + 3, A2.h - ins - 3, 1, -1],
                                      [A2.w - ins - 3, A2.h - ins - 3, -1, -1]]){
        c.beginPath();
        c.moveTo(cx + sx * cl, cy); c.lineTo(cx, cy); c.lineTo(cx, cy + sy * cl);
        c.stroke();
      }
      /* the blades coming off, along the two bearings */
      const ex = clamp(u.t / 0.34, 0, 1);
      if (ex < 1 && src){
        c.globalAlpha = (1 - ex) * 0.60;
        c.strokeStyle = u.aff.glow;
        c.lineWidth = 5 * (1 - ex) + 1;
        const rr = 30 + 150 * (1 - Math.pow(1 - ex, 2.4));
        for (const off of [0, 0.5]){
          const a2 = src.theta + off * TAU;
          c.beginPath();
          c.arc(src.x, src.y, rr, a2 - 0.55, a2 + 0.55);
          c.stroke();
        }
      }
      c.globalAlpha = 1;
      c.globalCompositeOperation = "source-over";
    }

    if (u.w === "vinesower"){'''


# ----------------------------------------------------------------- sound --

SFX_NEW = r'''        } else if (w === "%ID%"){                   // the blades coming apart
          /* THE CAST IS A SHEAR, NOT A BLAST. Something that was one object
             becomes seventy, and the sound has to say COMING APART rather
             than GOING OFF -- which is the same distinction the fork sound
             is built on ("a wet split ... so it reads as something COMING
             APART rather than as a second impact"), one size up.

             Three parts: a metal shear at the top, a body that falls away
             under it, and then the STREAM -- the window is four seconds long
             and this is the only cast in the game whose sound has to hand
             over to an ongoing thing rather than end.

             RULE 3f: an impact plus a rough band plus tones, which is the
             class this toolkit is five-for-five on, and deliberately NOT a
             voice or a creature vocalisation, which it is nought-for-four on.

             AND IT IS WRITTEN INSIDE THE ENVELOPE OF TWO KNOWN BUGS RATHER
             THAN FIXING THEM. `_burst` does not loop its 0.6s noise buffer,
             so every burst here is under 0.6s; `_tone` ends on an exponential
             ramp over its whole length, so the stream is RE-STRUCK rather
             than held. Both bugs are live on twenty-five shipped voices and
             fixing either is chain-wide and Rick's, not a thing a relic build
             gets to slip in. `thornshear_relic_probe [10]` RENDERS this in an
             OfflineAudioContext and measures it rather than trusting the
             paragraph -- v42 shipped a SILENT ultimate through fourteen
             checks, twenty-nine checks, a full sweep and a 13/13 verify. */
          this._burst(t, { freq: 3400, q: 1.4, gain: 0.26, dur: 0.055, type:"bandpass" });
          this._tone (t, { freq: 1250, to: 240, gain: 0.20, dur: 0.16, type:"sawtooth" });
          this._burst(t + 0.015, { freq: 1500, q: 0.7, gain: 0.15, dur: 0.30, type:"bandpass" });
          /* THE STREAM. Four airy re-strikes at an irregular 0.30-0.34s, which
             is roughly the volley cadence and reads as a hall filling rather
             than as a drone -- Rick rejected a sustained cluster for the score
             for exactly the reason it would be wrong here. The band is high
             and thin because leaves are, and because 200-600 Hz is where the
             impacts live and this must not compete with them. */
          [[0.10, 0.085], [0.42, 0.075], [0.75, 0.062], [1.06, 0.048]].forEach(
            ([d, g]) => {
              this._burst(t + d, { freq: 2600, q: 0.9, gain: g, dur: 0.24, type:"bandpass" });
              this._tone (t + d, { freq: 620, to: 470, gain: g * 0.55, dur: 0.26, type:"triangle" });
            });
        } else if (w === "%ID%-rung"){              // a kunai finishes growing
          /* THE TOP RUNG, AND ONLY THE TOP RUNG. Two of the three rungs happen
             about a hundred and ten times a cast and already have the wall's
             own voice under them; this is the ~13 that arrive fully grown, and
             it is the sound of §1's fourth sentence completing.

             A RISING CHIME, pitched off the rung so a viewer who has heard it
             twice knows what the third one means. Quiet by design and short by
             design: it lands in a window that is already busy, and an event
             that fires thirteen times cannot be loud thirteen times. */
          const f0 = 640 * Math.pow(1.26, (p.n || 1));
          this._tone (t, { freq: f0, to: f0 * 0.86, gain: 0.055, dur: 0.13, type:"triangle" });
          this._burst(t, { freq: f0 * 2.4, q: 2.2, gain: 0.035, dur: 0.045, type:"bandpass" });
        } else if (w === "bulwarden"){'''

SFX_LOOSE_NEW = r'''        if (p.bal){
          this._burst(t, { freq: 168, q: 1.3, gain: 0.10, dur: 0.16, type:"bandpass" });
          this._tone (t, { freq: 128, to: 58, gain: 0.10, dur: 0.20, type:"sawtooth" });
        } else if (p.leaf){
          /* A VOLLEY OF LEAVES IS NOT A BOWSTRING. One call per volley, not
             one per kunai -- ten transients on the same frame stack into a
             single loud click and tell the viewer nothing. Airy, short, and
             under everything: the volley leaving must not compete with the
             volley landing. */
          this._burst(t, { freq: 2100, q: 0.8, gain: 0.05, dur: 0.075, type:"bandpass" });
          this._tone (t, { freq: 380, to: 250, gain: 0.035, dur: 0.09, type:"triangle" });
        } else {'''


ULTFX_LIFE_NEW = r'''              marrowdraw: 8.6,
              /* THE WINNOWING is set from `ult.dur` at the cast site, the way
                 Aegis, the Thicket, the ballista and the Stasis Field are.
                 This entry is the fallback if that is ever missed. */
              thornshear: 9.4,'''


# ---------------------------------------------------------- the particles --
# THE TWENTY-SIXTH SPEC. `src/render/fx.js` carries twenty-five and every one
# of the shipped ultimates has a field; a relic with no entry is not an error
# (`ULTFX.sync` returns on `!spec`) which is exactly why it would ship missing.
# Written into the INLINED copy here and into `src/render/fx.js` by hand in the
# same commit, so a rebuild through `fx_build.py` cannot lose it.
FX_SPEC_NEW = r'''    /* THE WINNOWING. A FALL, not a burst: the one set-piece in the game whose
       objects are already doing the throwing, so the field must not compete
       with seventy kunai for the same read. Leaves come DOWN through the hall
       behind them -- slow, long-lived, barely any speed of their own, and the
       widest spawn band of any fall because the whole hall is in play rather
       than one point in it. */
    thornshear: { mode: 'fall', n: 1150, sp: [20, 110], grav: 70, drag: 1.1,
                  life: [0.90, 2.00], heavy: 0.03, size: [0.7, 2.0],
                  spawn: 0.90, up: 0 },
    /* ---- IMPLOSION: a burst run backwards ---------------------------- */'''

FX_SPEC_OLD = r'''    /* ---- IMPLOSION: a burst run backwards ---------------------------- */'''


EDITS = [
    ("the relic",
     '''    blurb:"A pit chain swung inside its own storm. Stand in it long enough and the argument is over." },

];''',
     RELIC_NEW),

    ("fighter state",
     '''    this.pinV = null;''',
     FIGHTER_STATE_NEW),

    ("the cast",
     '''    if (u.kind === "ballista"){''',
     FIRE_ULT_NEW),

    ("forgoing the blades",
     '''  bladeSegments(f){
    const mods = this.actMods;''',
     BLADE_SEGMENTS_NEW),

    ("the window",
     '''      if (A.t >= A.dur) f.ultAegis = null;
    }
  }''',
     TICK_WINNOW_NEW),

    ("the tick call",
     '''    this.tickBallista(dt);''',
     TICK_CALL_NEW),

    ("the parry",
     '''      for (const q of segs){
        const d = segDist(q.ax, q.ay, q.bx, q.by, s.x, s.y).d;
        if (d < s.r + foe.w.width * 0.5 + CONFIG.shot.pad){
          this.spawnFx(s.x, s.y, "#FFF4D0", 9, 240, 0.34, 3.2);
          this.ring(s.x, s.y, foe.aff.glow, 3, 46, 0.22, 3);
          this.shake = Math.min(38, this.shake + 4);
          SFX.play("clank");
          dead = true; break;
        }
      }''',
     PARRY_NEW),

    ("the wall",
     '''        if (hitWall){
          s.bounce--;
          s.vx *= 0.88; s.vy *= 0.88;
          s.a = Math.atan2(s.vy, s.vx);
          s.snap = true;          // the interpolator must not tween through a wall
          this.spawnFx(s.x, s.y, s.aff.glow, 5, 130, 0.24, 2.4);
          SFX.play("wall");
        }''',
     WALL_NEW),

    ("spent",
     '''      if (!dead && (s.life <= 0
          || s.x < n + s.r || s.x > A.w - n - s.r
          || s.y < n + s.r || s.y > A.h - n - s.r)){
        this.spawnFx(s.x, s.y, s.aff.core, 4, 110, 0.26, 2.2);
        dead = true;
      }''',
     SPENT_NEW),

    ("the director",
     '''      if (f.ultTrace){
        o.crowd = true;
        o.crowdMul = Math.max(o.crowdMul, f.w.ult.crowdMul || 0);
      }''',
     CROWD_NEW),

    ("the kunai",
     '''      if (s.seed){''',
     KUNAI_ART_NEW),

    ("the blades, drawn",
     '''    for (const off of f.w.blades){
      const a = f.theta + off * TAU;
      c.save();
      c.globalAlpha = dim;
      c.translate(f.x, f.y);
      c.rotate(a);
      c.translate(R - 6, 0);''',
     BLADE_DRAW_NEW),

    ("the set-piece",
     '''    if (u.w === "vinesower"){''',
     DRAW_UNDER_NEW),

    ("the ult voice",
     '''        } else if (w === "bulwarden"){''',
     SFX_NEW),

    ("the loose",
     '''        if (p.bal){
          this._burst(t, { freq: 168, q: 1.3, gain: 0.10, dur: 0.16, type:"bandpass" });
          this._tone (t, { freq: 128, to: 58, gain: 0.10, dur: 0.20, type:"sawtooth" });
        } else {''',
     SFX_LOOSE_NEW),

    ("the fx clock",
     '''              marrowdraw: 8.6,''',
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
    ap.add_argument("--src", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--out", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--id", default=RELIC_ID)
    ap.add_argument("--name", default=RELIC_NAME)
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=TUNED_TS)
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
    print("\nVERDANT TWINBLADE BUILD -- the Winnowing")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if '"stasis"' not in s0:
        raise SystemExit("this source has no stasis field -- build off "
                         "sc-paradox-ignition or later")
    if '"winnow"' in s0:
        raise SystemExit("this source already has a winnow -- already built")

    # BUILDERS ECHO WHAT THEY ARE ABOUT TO WRITE, AND SOMEBODY READS IT.
    # v42 rule 6: a `dmgMul` edit was silently eaten by a stale anchor and a
    # 4600-fight bisection ran at the wrong value. The only thing that caught
    # it was this block.
    print(f"  id  {A.id} / {A.name} / {A.ult}     dmg {A.dmg:g}")
    print("  ult " + "  ".join(f"{k} {getattr(A, k):g}" for k in ULT))

    # THE CEILING, ARITHMETIC, BEFORE ANY FIGHT RUNS. `fan` x 2 bearings x
    # `life` / `cadence` is the steady-state population of this relic's own
    # kunai, and CONFIG.shot.maxLive is 64 and SHARED with the foe's arrows.
    # A design permanently at the ceiling is a design whose cadence is decided
    # by a constant in CONFIG -- so the builder refuses to write one, rather
    # than leaving it for a probe to find after a sweep has run on it.
    pop = A.fan * 2 * A.life / max(1e-9, A.cadence)
    print(f"  pop {pop:.0f} kunai in steady flight against a 64 ceiling "
          f"shared with the foe's shots")
    if pop > 56:
        raise SystemExit(
            f"CEILING: fan {A.fan:g} at cadence {A.cadence:g} with life "
            f"{A.life:g} holds {pop:.0f} kunai in the air. maxLive is 64 and "
            f"the foe's arrows share it -- this build would spend the window "
            f"refusing volleys. Move along the curve fan/cadence ~= 8.3.")

    subs = {"%ID%": A.id, "%NAME%": A.name, "%ULT%": A.ult,
            "%TIP%": A.tip, "%DMG%": f"{A.dmg:g}"}
    for k in ULT:
        subs["%" + k.upper() + "%"] = f"{getattr(A, k):g}"

    for label, old, new in EDITS:
        for k, v in subs.items():
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # THE TIP HAS A HARD LIMIT AND verify.py IS WHERE IT IS ENFORCED -- which
    # is 12000 fights too late to find out. v43 hit 73 characters on its first
    # cut of the same line.
    # THE TIP THIS BUILDER WROTE, and not some other relic's. An earlier cut
    # of this check searched the whole page for `tip:"(For [^"]*)"` and matched
    # AUREOLE's, forty relics up the file, reporting 68/72 for a line this
    # builder never wrote. It is substituted now, so the string is known and
    # the only question is whether the page carries exactly one of it.
    if len(A.tip) > 72:
        raise SystemExit(f"ULT TIP is {len(A.tip)} characters against "
                         f"verify.py's limit of 72:\n  {A.tip}")
    if s.count(f'tip:"{A.tip}"') != 1:
        raise SystemExit("the ult tip did not land exactly once")
    print(f"  tip {len(A.tip)}/72  {A.tip}")

    # THE INLINED MODULE AND THE FILE ON DISK MUST STAY THE SAME OBJECT.
    # `fx_build.py` inlines `src/render/fx.js` verbatim and STAMPS ITS SHA256
    # into the page twice, and this builder writes a twenty-sixth spec into the
    # inlined copy. Written only there, the next rebuild through fx_build would
    # silently drop the field -- an ultimate with no particles among
    # twenty-five that have them, which is a picture fault with no number
    # attached to it. So the same spec goes into `src/render/fx.js` in the same
    # commit, and this block REFUSES TO WRITE unless the two are byte
    # identical, then re-stamps the sha so nothing downstream is reading the
    # hash of a file that has moved.
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
    print("\n  NEXT, and item one is not optional:")
    print(f"    python cinema_clip.py --game {A.out} --a thornshear "
          f"--b emberedge --seed <seed> --full   # FILM IT FIRST (v43 §13)")
    print(f"    python thornshear_relic_probe.py --relic {A.out}")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python verify.py --game {A.out} --n 40")
    print("    python thornshear_sweep.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
