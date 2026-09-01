#!/usr/bin/env python3
"""RAVELBONE, THE 30TH RELIC, AND ITS ULTIMATE GARROTE. STAGES 1, 2, 3 AND 4.

    python ravelbone_build.py --stage 1 --src ../02-chain/sc-breach.html \
                              --out ../02-chain/sc-ravelbone.html
    python ravelbone_build.py --stage 2 --src ../02-chain/sc-ravelbone.html \
                              --out ../02-chain/sc-wire.html
    python ravelbone_build.py --stage 3 --src ../02-chain/sc-wire.html \
                              --out ../02-chain/sc-garrote.html

`06-docs/v60/ravelbone-build-brief-v60.md` is the brief, and the design and the
pricing behind it are `06-docs/v60/wirering-design-v60.md` -- 26 arms at 702
fights each, `tools/wire_lab.py`.

## THREE DEPARTURES FROM THE BRIEF, ALL DECLARED HERE

**IT IS THE THIRTIETH RELIC AND THE BRIEF SAYS THIRTY-FIRST.** The brief was
written expecting BLOODMIRROR to land first; Bloodmirror is neither built nor
in this repo -- its brief lives in the Cowork project only. `WEAPONS` holds 29
on `sc-breach.html`, so counted, Ravelbone is 30 and every `engine_ab` in the
gates runs over 29 others rather than 30.

**AND IT IS NOT BLOODSWORN'S LAST OPEN CELL.** Counted on the tip, bloodsworn
holds twinblade, greatsword, flail and bow; this puts it on 5 of 6 and leaves
**bloodsworn x scythe open**, which is the cell Bloodmirror is designed into.
The brief's sentence is true only once Bloodmirror exists. What does not move:
the warhammer goes to 5 of 7 schools, and `row_price --type warhammer --pin 0`
picks this cell on both its columns (+22.1%, 65% at >=2 stacks).

**AND THE CONNECT IS NOT A BARE `knock x2`. IT IS RICK'S MERGE, 2026-09-01.**
Two v60 designs were written for this cell in parallel by two sessions that
could not see each other; `06-docs/v60/CONFLICT-READ-FIRST-v60.md` has the
whole of it and Rick's ruling. He took RAVELBONE ALONE **with the red hammer's
kick folded into the connect**, and the reason is that document's section 3:

> GARROTE's headline effect is *"the connection deals massive knockback"*, and
> the red hammer measured exactly that verb and REFUTED it. The impulse is real
> and exactly `CONFIG.combat.knock x knockMul` -- `|dv|` comes back at 379.5 to
> the decimal -- but most of it is spent CANCELLING the incoming velocity,
> because the quarry was travelling toward the hammer, which is why they
> touched. And `move()` governs speed rather than conserving it: it clamps to
> [250, 1300] every step and relaxes toward an energy-derived target at 0.62.
> Whatever survives washes out inside the 0.41s median flight to a wall.

So the connect delivers the normal blow's knock **plus a separate impulse of
`kick` 800 under `launch` 1.2s**. `launch` is a PERMISSION and not a push -- it
raises the vmax clamp and adds no velocity, which is why below about kick 500
it changes nothing at all, and it is why the Crucible pairs it with an impulse
and why this must too.

**AND 800 IS MEASURED, WHERE 2400 WOULD HAVE BEEN COPIED.** The red hammer
swept it: at kick 2400 -- the Crucible's own number for the same verb on the
same weapon type -- arrivals pile against `vmax` 2795 and the arrival spread
COLLAPSES from 3.65 to 1.70. It is the single worst value in the sweep for a
mechanic that pays per event rather than once at the end of a charge. **The
shipped build was already clipping and nobody knew**: p90 arrival at kick 0 is
exactly 1300, which is `speedMax`.

This costs nothing in value. `wirering-design-v60.md` section 5b measured the
knock at x1 +25.2, x2 +30.1, x5 +29.8 -- **+4.9 for the first doubling and
nothing after it** -- so a louder connect is free and is bought for the picture.

> **IT DOES CHANGE THE CONDITIONS OF THE REGISTERED PREDICTION.** Brief section
> 11 names "knock 2x". The value should be unchanged by 5b's own flatness, so
> the +30 claim still stands as a test -- but it is no longer a clean test of
> the connect as specified, and this paragraph exists so nobody reads a pass as
> confirming a number nobody shipped.

## AND THE SNAG IS WHY THE KICK WORKS BETTER HERE THAN IT DID THERE

The red hammer's whole problem is an impulse spent reversing a quarry that was
moving toward the hammer. **A snagged ball has no incoming velocity to cancel**
-- `f.pin` holds it still -- so a connect delivered to a pinned foe is the one
case in this game where the full impulse goes into departure.

## RICK'S SECTION 1, VERBATIM

    the hammer gains massive rotational speed. It also gets a barbed wire ring
    around it that matches its hit range. enemies caught in the barbed wire are
    stunned, gain a bleed stack, and are held until the hammer comes around and
    connects. the connection deals massive knockback and causes the barbed wire
    ring to explode and expire, applying bleed again.

plus two rulings that arrived after it and that look contradictory until they
are put together -- *the wire SNAGS rather than stuns*, and *the ball is
FROZEN* -- and combine into a verb nothing in this game uses:

> **The ball is held. The weapon is not.** You are caught in the wire, you
> cannot leave, and you can still fight back.

    CRUCIBLE        ball pulled   weapon LOCKED   cannot act
    GRASP           ball free     weapon LOCKED   cannot act
    STASIS FIELD    ball HELD     weapon LOCKED   cannot act
    GARROTE         ball HELD     weapon free     CAN act -- it just cannot leave

## THE ULTIMATE IS ONE SCALAR AND IT IS NOT THE ONE THE DESIGN PREDICTED

Regressed across 22 tuning arms, and then validated on four the line never saw:

    predictor                       r       r2
    FOE BLOWS NOT LANDED        +0.942   0.89     the whole thing
    catches                     +0.684   0.47
    connects                    +0.606   0.37
    held seconds                +0.514   0.26     v56's currency. Not this one's
    OWN blows                   -0.088   0.01     the fast spin is worth NOTHING

    lift = +8.2 + 8.25 x (blows the opponent did not land)

**"Massive rotational speed" earns its place as a picture and as the clock that
sets the hold -- not as damage.** And the hold's length is not a field at all:
it is however long the head takes to come around, so winding faster SHORTENS it
and buys the payoff sooner. The weapon is its own timer.

## WHAT WILL BITE, AND THE FIRST ONE IS SILENT

**`move()` DISCARDS EVERY IMPULSE A BALL TOOK WHILE IT WAS PINNED.** It ASSIGNS
`f.pinV` on the first frame the ball is allowed to move again -- v43's rule, a
measured and named fix. Garrote's headline effect is a massive knockback
delivered to a ball that is pinned at that instant. Apply the impulse before
clearing the pin and the hit lands, the damage lands, the beat files, every
probe passes, **and the ball does not move.**

    THE ORDER, AND IT IS NOT NEGOTIABLE
      1. f.pin = 0; f.pinMax = 0; f.pinV = null;    release FIRST
      2. then the impulse
      3. then the consume, the damage, the beat

Assert it as a DISPLACEMENT and never as a velocity write: a test that reads
`vx` immediately after the write passes in the broken build.

**BOTH HALVES OF THE BLEED SENTENCE ARE INERT.** `hemorrhage` is
`{maxStacks: 4, dur: 3.2, dps: 1.5}` and the hammer's own `onHit` already puts
on 2 a blow, so the bar is full before the ultimate casts: applying 1 stack on
the explosion and applying 4 returned **64.5% and 64.5%, identical to the
decimal**. The repair is stage 3 -- the explosion CONSUMES the pool.

**`f.ultSpin` IS TWINSHADE'S AND IT ALSO CHANGES CLANKS.** `resolveClank` reads
`spinLockA = !!A.ultSpin` and grants immunity from having your spin reversed by
a lost bind. Ravelbone probably WANTS that immunity -- a hammer at 6x whose
direction flips stops coming around and the snag never pays off -- but it must
be granted from its own field with a comment, not inherited by accident.

**`m.ultFx` IS ONE SLOT.** A ring on screen for eight seconds cannot live in a
field the other fighter clears by casting anything. Deadfall measured 0.0%
survival against Ironhail.

**AND THE RING IS NOT A SHOT.** `spawnShot` shifts the oldest live entry out at
`maxLive` 64 and `tickShots` lets a blade PARRY one. A parryable ring is not a
ring.

EVERYTHING DRAWN HERE IS A FIRST CUT AND NOBODY HAS WATCHED IT. A held ball
with a MOVING weapon is a picture this game has never drawn, and if it reads as
a frozen one the whole separation above is invisible. FILM IT BEFORE TUNING
ANYTHING -- v43 section 13, and v54 section 2c is why it is not optional.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "ravelbone"

# --- THE RELIC. Every physical stat is the WARHAMMER'S, and it is copied off
#     Grudgebearer, Censer, Bulwarden and Shroudmaul -- all four already carry
#     this line byte for byte and the TYPE owns it. There is no fifth set to
#     invent. `SHAPES.warhammer` already routes `bloodsworn` to `_whBarbed`,
#     which has drawn this cell since before there was a relic in it.
BLADE_IN = 23.5      # THE BISECTION START, and it is the type's own. Design
                     # section 2 says the answer is BELOW it: the section 1 as
                     # ruled lands at +30.3% over its own no-ultimate floor,
                     # against a field of 27 built ultimates whose mean is
                     # +20.1 and whose Q3 is +25.5. The lab's floor arm sits at
                     # 36.8%, so there is room to give back.
TUNED_RB = None      # STAGE 4. Not measured yet -- and it must not be guessed.
                     # v56 defaulted every stage to a tuned value and stage 2
                     # then wrote it, so stage 3 refused looking for a starting
                     # value that was already gone.

ULT = {
    # THE WINDOW, if nothing is ever caught. 4s is +19.1 and 12s is +30.9, so
    # this is a real knob and 8 is where Rick's section 1 sits.
    "dur": 8.0,
    # THE RING. 110 is Rick's, from two, and it is the happy number: the head
    # sits at `reach` 76 from the ball centre and the foe's ball is `ballR` 34,
    # so a blow lands at about 110 between centres. "Matches its hit range"
    # reads as 110 and not as 76 -- and at 76 the ring is +6.7 STRONGER and
    # fewer than half its catches ever get the hammer, because the caught ball
    # drifts out of the head's path and the ring just holds until the window
    # runs out. That is worth a lot and it looks like a bug.
    "radius": 110.0,
    # THE WIND-UP. FLAT TO NOISE across x2 -> x12 (8.1pp spread against a 2.7pp
    # SE), so it is PICKED FOR THE PICTURE -- and 6 is what the registered
    # prediction in brief section 11 names, which is the only reason it is 6
    # and not 9. Do NOT set 3.4: that is Crucible's exact number on this type.
    "spinMul": 6.0,
    # THE CONNECT'S OWN KNOCK, as a multiple of a normal blow's. 1 means the
    # engine's ordinary `knock x knockMul` and nothing added -- the loudness is
    # bought with `kick` below, which is the half of it that survives `move()`.
    # IT IS NOT CALLED `knockMul`. The WEAPON carries a `knockMul` of 2.3 four
    # lines above this in the same entry, and the first thing the collision did
    # was make `ult_matches` read the weapon's value and refuse. A relic-level
    # name and an ult-level name that differ in meaning must differ in spelling.
    "connectKnock": 1.0,
    # THE KICK, and it is the merge. `06-docs/v60/CONFLICT-READ-FIRST-v60.md`.
    # Measured across 0 / 250 / 500 / 800 / 1200 / 1800 / 2400: 800 clears the
    # arrival-speed gate at +35.7%, holds the widest spread of any arm at 3.65,
    # and is the last value before the arrivals start piling against `vmax`.
    # 2400 -- the Crucible's -- collapses that spread to 1.70.
    "kick": 800.0,
    # THE PERMISSION. `launch` raises the vmax clamp for this long and the
    # relax term spends it back; it adds no velocity by itself.
    "launch": 1.2,
    # HOW LONG THE WIRE WILL HOLD SOMETHING THE HEAD NEVER REACHES. Rick, on
    # the shipped clip: "the hold needs to expire if the hammer doesn't hit in
    # time." Chosen off `hold_lab.py`'s distribution rather than guessed: a
    # catch that connects holds a median 1.03s and a p90 of 3.82s, and one that
    # never connects holds a median 7.33s -- the whole window. 2.5s is about
    # FOUR revolutions of the head at `spin` 1.6 x `spinMul` 6, so a hold that
    # reaches it has had four chances and taken none.
    "holdMax": 2.5,
    # AND HOW LONG BEFORE THE RING MAY CATCH AGAIN. Not decoration: the quarry
    # was caught on the frame it ENTERED the ring, so released without a delay
    # it is still inside and is re-caught on the next frame -- the same
    # infinite hold with a stutter drawn over it.
    "reArm": 1.0,
    # THE CONSUME, stage 3. 8 damage a stack -- about 56 on the connect on top
    # of a 23.5 blade, the hardest single blow in the game and still under a
    # quarter of a fighter's health. Linear at +0.73 win points per point, so
    # it is the LAST thing that should move: settle it after the bisection,
    # because `dmg` moves the blade AND the Hemorrhage the consume later eats.
    "consume": 8.0,
}

# WHAT THE CONNECT ENDS, and it is a STRING rather than a number so it is not
# swept by accident. `06-docs/v60/ravelbone-build-v60.md` sections 5c-5f.
#
# "window"  the connect ends the ring AND the wind-up. THE SHIPPED ARM.
# "ring"    the ring blows apart and the hammer keeps turning out the rest of
#           its window without being able to catch again.
#
# RICK RULED TWICE AND THE SECOND RULING IS THE ONE THAT COUNTS, because the
# first was made on a table and the second was made on a rendered fight.
#
#   1. Shown +32.9 against +18.2, he took "ring" -- it reproduces the design's
#      own registered +29.9 where "window" misses it by 3.2 sigma.
#   2. Shown the CLIP: *"the extra wind up speed should stop after it lands a
#      hit."*
#
# THE SECOND OVERRULES THE FIRST AND COSTS 14.7 MEASURED POINTS, and it is
# section 4.1 working exactly as this project intends: the numbers said the arm
# was free and a person watching said the picture was not. What he saw is open
# item 45 -- after the connect the payoff has visibly happened, the ring is
# gone, and the hammer is still turning at 6x with nothing in the arena saying
# the window is open. `05-reference/v60/garrote-states-tail.png` is that frame.
#
# AND "LANDS A HIT" IS "THE CONNECT", WHICH IS CHECKED RATHER THAN ASSUMED. The
# ring sits at `radius` 110 and a blow lands at about 144 between centres, so
# the quarry cannot be struck without having been caught first. The only bodies
# that can be hit un-caught are a SHADE and a quarry already pinned by Paradox,
# and neither is the case his sentence is about.
EXPIRE = "window"

ULT_NAME = "Garrote"
# MECHANIC-FIRST, <=72 characters, and it is a FIRST CUT -- brief open decision
# 3, and the tip is one of the seven things that are Rick's. What has to get in
# is that the wire holds you where you stand and the hammer is coming.
# AND `tip_audit` MEASURES IT IN PIXELS. The scrunch panel is 536px on one line
# at 25px, and a 48-character string has overflowed it before now.
ULT_TIP = "Wire ring holds the foe where it stands; the hammer comes around"
# AND STAGE 3'S, because by then the relic does a third thing. "consumes" is
# the house word -- the Crucible's own tip says "consumes Sunder" -- and using
# it here is the THIRD collision with that relic on this weapon type, after the
# spin-up and the hold. It is deliberate rather than unnoticed: inventing a
# different verb for the same mechanic would be worse. Rick's, and it is his
# card wording rule.
ULT_TIP3 = "Holds the foe where it stands, then throws it and consumes Hemorrhage"
BLURB = ("Wire off a pit fence, wound round a head that was already heavy. "
         "What it catches does not get to walk away from the swing.")


# ============================================================ STAGE 1 =======
# THE 30TH RELIC EXISTS AND ITS ULTIMATE IS STUBBED. What this stage measures
# is a blade and a channel and nothing else, and the gate is that it lands near
# 37% at blade 23.5 -- the lab's floor arm, Grudgebearer standing in as a
# bloodsworn warhammer with its own Crucible suppressed, read 36.8%.
S1 = [

# --------------------------------------------------------- 1. the 30th relic
("relic", '''    blurb:"Forged for a harvest and handed a hall. What it opens in the stone stays open, and the mountain does the rest." },

];''',
 '''    blurb:"Forged for a harvest and handed a hall. What it opens in the stone stays open, and the mountain does the rest." },

  /* RAVELBONE -- THE BLOODSWORN WARHAMMER, and the thirtieth relic. Bloodsworn
     was on 4 of 6 types and the warhammer on 4 of 7 schools; this puts the
     school on 5 and the type on 5. It does NOT close bloodsworn -- the scythe
     cell is still open and is the one Bloodmirror is designed into.

     EVERY PHYSICAL STAT IS THE WARHAMMER'S, copied off Grudgebearer, Censer,
     Bulwarden and Shroudmaul -- all four already carry this line byte for byte
     and the TYPE owns it. `SHAPES.warhammer` routes `bloodsworn` to
     `_whBarbed`, which has drawn this cell since before there was a relic in
     it, and Rick has ruled on that silhouette with its number in front of him:
     nearest sibling dwarven at 50.8% ink diff, inkIoU 0.762, the closest pair
     of 21 on this type, and he took "leave it, it's fine". Open item 34's
     first instance is a DECISION now. Do not re-raise it.

     AND THE CELL WAS CHOSEN ON ITS CHANNEL, NOT ON ITS OCCUPANCY.
     `row_price --type warhammer --pin 0` picks it on both columns -- 56.1%,
     +22.1%, 65% of fights at two stacks or more, against runic's +10.4% and
     verdant's +6.8% -- and two things in that run are worth more than the
     ranking. It is THE ONLY CHANNEL ON THE ROW THAT IS POSITIVE AGAINST
     RANGED (+10.0%, against runic -6.0% and verdant -10.0%), which is the
     opposite sign to open items 12 and 32 on the same axis. And hemorrhage
     costs this cell FIFTY BLADE DAMAGE A FIGHT -- 303 against a no-channel
     353 -- while lifting it 22.1%, because the bleed shortens the fight so the
     blade delivers less of it. That is open item 24 visible on the cell rather
     than argued about: ANYTHING TUNED OFF RAW `dealt` HERE READS BACKWARDS.

     `dmg` is the tuned knob (ravelbone_build.TUNED_RB) and it starts at 23.5,
     which is the type's own value and a bisection START. Design section 2 says
     the answer is below it. */
  { id:"ravelbone", name:"Ravelbone", aff:"bloodsworn", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:%DMG%, spin:1.6, mode:"spin", mass:5.0, knockMul:2.3,
    onHit:{ hemorrhage:2 },
    /* GARROTE. STUBBED AT `charge:1e9` IN STAGE 1, which is the same "OFF" the
       charge sweep in v55b used and the same one Cindercleave's stage 1 and
       Shroudmaul's stage 2 used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else. Stage 2 brings the charge down to %CHARGE% and builds the ring;
       stage 3 makes the explosion consume Hemorrhage.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       CHARGE 16 IS THE ROSTER MODE AND IT WAS NEVER SWEPT -- v55b, and nobody
       else's was ever derived either. Unlike Grasp this ultimate DOES scale
       with cast count, so it is a real open knob and it is brief open decision
       4. It has not been measured and this comment is not claiming it has.

       `kind:"wire"` IS ITS OWN AND IT IS NOT `"forge"`. Crucible is the
       dwarven warhammer and this is the third warhammer whose ultimate stops
       the other fighter moving. What separates it is real and it is worth
       writing down where the numbers live: Crucible's hold is a freeze with a
       cash-out, Grasp's is a counter that has to be earned, and THIS one's
       length is set by the weapon's own rotation and ends with the weapon
       ARRIVING. It is the only hold in the game that resolves itself with a
       hit rather than with a timer, and the only ultimate whose area is
       exactly the weapon's own reach, drawn. */
    ult:{ name:"%ULT%", charge:1e9, kind:"wire",
          dur:%DUR%, radius:%RADIUS%, spinMul:%SPINMUL%,
          connectKnock:%CONNECTKNOCK%, kick:%KICK%, launch:%LAUNCH%,
          holdMax:%HOLDMAX%, reArm:%REARM%,
          consume:%CONSUME%, expire:"%EXPIRE%",
          tip:"%TIP%" },
    blurb:"%BLURB%" },

];'''),
]


# ============================================================ STAGE 2 =======
# THE RING. Snag, hold, connect, throw -- and NO consume yet. This stage stops
# short of the consume on purpose: the consume is a clean linear knob (+0.73
# win points per point of per-stack damage) and it is the last thing that
# should move. A stage-2 build landing near +24% over its own stage-1 floor is
# the gate; if it does not, the consume papers over whatever is wrong with the
# ring and nobody finds it until the bisection misbehaves.
S2 = [

# ------------------------------------------------------ 0. the clock reaches
#     THE WHOLE `ult` BLOCK IS REWRITTEN AND NOT JUST THE LINE CARRYING
#     `charge`, AND THAT IS v56'S OWN FAILURE AVOIDED RATHER THAN DESCRIBED.
#     There, the stage that opened the window wrote every knob and the stage
#     after it rewrote only `charge` -- so `--stage 3 --cadence 2.0` LOGGED the
#     new rhythm and SHIPPED the old one, and every gate downstream measured a
#     relic the log was not describing. It was caught by a probe printing n=5
#     two minutes later.
#
#     `%D_*%` is what stage 1 WROTE (this module's defaults) and `%*%` is what
#     THIS run was asked for, so passing a knob here changes the build. If
#     stage 1 was run with non-default knobs the anchor does not match and this
#     refuses -- which is right: the chain is linear and the fix is to re-run
#     stage 1, not to let two links disagree about what the relic is.
("ult.charge", '''    ult:{ name:"%ULT%", charge:1e9, kind:"wire",
          dur:%D_DUR%, radius:%D_RADIUS%, spinMul:%D_SPINMUL%,
          connectKnock:%D_CONNECTKNOCK%, kick:%D_KICK%, launch:%D_LAUNCH%,
          holdMax:%D_HOLDMAX%, reArm:%D_REARM%,
          consume:%D_CONSUME%, expire:"%D_EXPIRE%",''',
 '''    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"wire",
          dur:%DUR%, radius:%RADIUS%, spinMul:%SPINMUL%,
          connectKnock:%CONNECTKNOCK%, kick:%KICK%, launch:%LAUNCH%,
          holdMax:%HOLDMAX%, reArm:%REARM%,
          consume:%CONSUME%, expire:"%EXPIRE%",'''),

# --------------------------------------------------- 1. whether a hold locks
#     the weapon. THIS FIELD EXISTS BECAUSE THE BRIEF'S CENTRAL INSTRUCTION --
#     "write `f.pin`, do NOT write `f.stun`" -- IS NOT SUFFICIENT ON THIS
#     ENGINE, and nothing in the brief says so.
("Fighter.pinFree", '''    this.pinV = null;''',
 '''    this.pinV = null;
    /* AND WHETHER THIS HOLD LOCKS THE WEAPON. 0 for every hold in the game
       before GARROTE, which is why `engine_ab` is the proof that adding it
       moved nothing.

       THE BRIEF SAYS "WRITE `f.pin`, DO NOT WRITE `f.stun`" AND THAT IS NOT
       ENOUGH ON THIS ENGINE. `tickStasis`'s decrement loop -- which runs for
       BOTH fighters on every frame, outside any `ultField` guard -- carries
       the line `f.stun = Math.max(f.stun, f.pin)`. So any relic that writes
       `pin` is handed a weapon lock by Paradox's bookkeeping, from a file
       nowhere near its own code. Garrote would have locked the weapon it was
       built to leave free, the whole separation in the design would have been
       invisible, and a probe asserting "tickWire never writes f.stun" would
       have passed -- because tickWire does not. THE WRITE IS SOMEWHERE ELSE.

       So the field says what KIND of hold this is, and the two readers that
       care about the difference ask it: the stun refresh above, and the runic
       hexagon the renderer draws on a held ball. Nothing else in the engine
       reads it, and no other relic sets it. */
    this.pinFree = 0;'''),

# ------------------------------------------------------------- 2. the window
("Fighter.ultWire", '''    this.breachFade = 0;''',
 '''    this.breachFade = 0;
    /* THE RING. `{t, dur, caught, catches, connects, held, hum}` while
       GARROTE's window is open, and null on every other relic and on this one
       outside its own window -- which is the whole zero-burden argument:
       `tickWire` returns on its first line, `drawWire` returns on its first
       line, and the two new clauses in `tickWeapon` and `resolveClank` are
       comparisons against null on a field nothing else writes.

       IT IS ON THE FIGHTER AND NOT ON `m.ultFx`, and that is v54 section 2a
       and open item 25: `ultFx` is ONE SLOT and the opponent casting anything
       overwrites it, measured at 0.0% survival against Ironhail. A ring that
       is on screen for eight seconds cannot live in a field the other fighter
       can clear.

       THE HOLD'S LENGTH IS NOT IN HERE AND THERE IS NO FIELD FOR IT. Every
       other hold in this roster is a duration -- Bramblesnare's 1.6s,
       Rootfast's 1.3s, Grasp's two timers, the Crucible's freeze. This one
       falls out of the rotation: the wire holds until the head comes around,
       so winding the hammer faster SHORTENS the hold and buys the payoff
       sooner. `foe.pin` is REFRESHED frame by frame while the catch stands,
       which is how a hold with no duration is written down. */
    this.ultWire = null;
    /* AND THE RING'S OWN FADE, because the window closing is not the same
       event as the picture of it ending. Same shape as `graspFade`,
       `breachFade`, `deadfallFade` and `winnowFade`, and driven in
       `tickPresentation` for the reason they all give: the connect sets
       `hitStop`, and a presentation clock on the normal path freezes for
       exactly the frames the viewer is staring hardest at. */
    this.wireFade = 0;'''),

# --------------------------------------- 3. the stun refresh asks what kind
("tickStasis.pinFree", '''      if (!f.alive){ f.pin = 0; f.pinV = null; continue; }
      f.pin = Math.max(0, f.pin - dt);
      f.stun = Math.max(f.stun, f.pin);''',
 '''      if (!f.alive){ f.pin = 0; f.pinV = null; f.pinFree = 0; continue; }
      f.pin = Math.max(0, f.pin - dt);
      /* AND ONLY IF THE HOLD IS ONE THAT LOCKS THE WEAPON. This loop runs for
         both fighters on every frame and it is OUTSIDE the `ultField` guard
         below, so it is the real writer of `stun` for every hold in the game
         -- the Stasis Field's, Grasp's squeeze, and now Garrote's. The first
         two want it. GARROTE IS THE WHOLE POINT OF NOT WANTING IT: the ball
         is held and the weapon is not, the quarry can still fight back, and
         it is the one verb nothing else in this game uses.

         `pinFree` is 0 on both existing writers, so this line is unchanged
         for them and `engine_ab` is the proof rather than this comment. */
      if (!f.pinFree) f.stun = Math.max(f.stun, f.pin);'''),

# ------------------------------- 4. and the picture asks the same question
("draw.pinFree", '''    if (f.pin > 0){
      /* HELD. Deliberately NOT the stagger ring: a stagger is a weapon that''',
 '''    if (f.pin > 0 && !f.pinFree){
      /* HELD BY THE STASIS FIELD. `pinFree` is the guard and it is not
         defensive: this block hardcodes `AFFINITIES.runic`, so without it a
         bloodsworn wire snag draws PARADOX'S HEXAGON around the ball it
         caught -- a picture fault with every number in the fight correct,
         which is section 4.1's own defect class.

         Deliberately NOT the stagger ring: a stagger is a weapon that''')
,

# ------------------------------------------------------------ 5. the wind-up
("tickWeapon.spin", '''    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);''',
 '''    /* GARROTE JOINS THE FIRST BRANCH AND NOT `ultSpin`'S. `f.ultSpin` is
       TWINSHADE'S -- it is declared "{t, dur} while the shades walk", it is
       driven by `tickSpinStorm`, and `resolveClank` reads it to grant immunity
       from having your spin direction reversed by a lost bind. Reusing it here
       would collide with Twinshade and would hand Ravelbone that immunity by
       accident. It is granted deliberately instead, from this relic's own
       field, three hundred lines down in `resolveClank`.

       The multiplier is `ult.spinMul` and the sweep across x2 -> x12 is FLAT
       TO NOISE (8.1pp spread against a 2.7pp standard error), so 6 is a
       PICTURE choice and not a tuned one. It is also the clock: the hold ends
       when the head comes around, so this number sets how long a catch is
       held and nothing else does. */
    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge || f.ultWire ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);'''),

# ------------------------------------------------- 6. and it keeps its footing
("resolveClank.spinLock", '''    const spinLockA = !!A.ultSpin, spinLockB = !!B.ultSpin;''',
 '''    /* AND GARROTE KEEPS ITS DIRECTION THROUGH A LOST BIND, DELIBERATELY.
       A hammer at 6x whose spin reverses mid-window stops coming around, and
       the catch it is holding then pays off nothing at all -- the hold ends
       when the window does, the connect never happens, and eight seconds
       resolve into a foe standing still. Rick already ruled the same way for
       Twinshade: "grant immunity to losing clanks so it never reverses
       direction while its casting."

       IT IS GRANTED FROM `ultWire` AND NOT INHERITED FROM `ultSpin`, which is
       the same field for the same effect and belongs to another relic. Two
       relics reading one field is how the next change to Twinshade silently
       becomes a change to this one. */
    const spinLockA = !!A.ultSpin || !!A.ultWire;
    const spinLockB = !!B.ultSpin || !!B.ultWire;'''),

# --------------------------------------------------------------- 7. the cast
("fireUlt.wire", '''      f.ultBreach = { t: 0, cap: u.cap, n: u.n, tears: 0, pass: null };
      return;
    }''',
 '''      f.ultBreach = { t: 0, cap: u.cap, n: u.n, tears: 0, pass: null };
      return;
    }

    if (u.kind === "wire"){
      /* NOTHING RESOLVES HERE, and there is no `u.dmg`. The cast winds the
         head up and stands a ring of barbed wire at the hammer's own hit
         range; what the ultimate IS happens on the catch inside it and on the
         blow that ends it. There is no radius test on this frame and nobody
         is touched by it.

         NOT `forge`, and the collision is worth writing down where the code
         is rather than in a document. Crucible is the DWARVEN warhammer, it
         also multiplies spin, it also stops the other fighter, and it also
         consumes a status -- three collisions with one relic on one weapon
         type. What actually separates them: Crucible's hold is a freeze with
         a cash-out and it PULLS the quarry in, Grasp's is a counter that has
         to be earned, and this one's length is set by the weapon's own
         rotation and ends with the weapon ARRIVING. It is the only hold in
         the game that resolves itself with a hit rather than with a timer,
         and the only ultimate whose area is exactly the weapon's own reach,
         drawn.

         `caught` STARTS FALSE and there is no cooldown on the catch: the ring
         closes on the frame the quarry is inside it, which may be the frame
         the window opens. The ring is a place it is unsafe to be, not a
         metronome. */
      f.ultWire = { t: 0, dur: u.dur, caught: false, catches: 0,
                    connects: 0, held: 0, hum: 0, spent: false,
                    holdT: 0, cd: 0, slips: 0 };
      return;
    }'''),

# ------------------------------------------------- 8. the set-piece's length
("ultFx.life", '''              cindercleave: 1.6,''',
 '''              cindercleave: 1.6,
              /* THE RING IS NOT IN HERE. This is the CAST's flash and its
                 particle field only; the ring itself is on `f.ultWire` and
                 `f.wireFade` for v54 section 2a's measured reason, so this
                 number is short on purpose and does not track `ult.dur`. */
              ravelbone: 1.5,'''),

# ------------------------------------------------------------- 9. the tick
("step.tickWire", '''    this.tickBallista(dt);
    this.tickStasis(dt);''',
 '''    this.tickBallista(dt);
    /* BEFORE `tickStasis`, because the hold has no duration of its own and is
       REFRESHED here every frame the catch stands -- so the refresh has to be
       written before the loop that decrements it. And before `tickHits`,
       because the connect is an ordinary melee blow resolved by the engine's
       own hit loop, and it has to be able to see that the quarry is caught. */
    this.tickWire(dt);
    this.tickStasis(dt);'''),

# ---------------------------------------------------------- 10. the ring
("tickWire", '''  tickStasis(dt){
    /* THE HOLD OUTLIVES THE WINDOW.''',
 '''  /* ---------------------------------------------------------- GARROTE --
     THE RING, AND THE ONE THING IN IT THAT NOTHING ELSE IN THE GAME DOES.

     The ball is held and the weapon is not. You are caught in the wire, you
     cannot leave, and you can still fight back:

       CRUCIBLE        ball pulled   weapon LOCKED   cannot act
       GRASP           ball free     weapon LOCKED   cannot act
       STASIS FIELD    ball HELD     weapon LOCKED   cannot act
       GARROTE         ball HELD     weapon free     CAN act

     Measured at 702 fights an arm: a ring that only cuts is +19.6% (the field
     median exactly), the SNAG is +24.0%, and the stun version is +27.8%. The
     snag costs 3.8 points and buys the whole identity -- and it also raises
     connects from 1.17 to 1.38 a fight, because a pinned ball cannot drift
     out of the head's path, so the promised payoff lands MORE often.

     NOTHING RESOLVES IN HERE. The catch deals no damage and the connect is an
     ordinary melee blow found by the engine's own `tickHits` and priced in
     `resolveHit` -- which is why it inherits `hitCd` 0.45, the head's width,
     the crit roll, hit-stop weight and, the part that matters, THE FATAL BEAT.
     v53's Gravemourn filed `kind:"ult"` for a killing hand and 30 of 58 kills
     rendered with no killing blow; a payload that resolves outside
     `resolveHit` has that hole and this one deliberately does not.

     ORDER. Called after the fighter loop -- so `move` has already run and the
     positions are current -- and before `tickStasis` and `tickHits`. All three
     matter and the reasons are in `step`.

     THE RING IS NOT A SHOT. `spawnShot` shifts the oldest live entry out at
     `maxLive` 64 and `tickShots` lets `bladeSegments` PARRY one. A ring a
     greatsword can parry is not a ring, and nobody decided it should be. */
  tickWire(dt){
    if (!this.a.ultWire && !this.b.ultWire) return;   // <- the zero-burden guard
    const R = CONFIG.physics.ballR;
    for (const [f, foe] of [[this.a, this.b], [this.b, this.a]]){
      const W = f.ultWire;
      if (!W) continue;
      const u = f.w.ult;
      W.t += dt;

      /* THE WINDOW ENDS, and a catch it is still holding is let go. A caster
         that dies takes its own ring with it -- wire is not a thing that
         outlives the arm swinging it, and a hold with nobody coming for it is
         the Stasis Field with extra steps. */
      if (W.t >= W.dur || !f.alive){ this.releaseWire(f, foe); continue; }

      if (W.caught){
        /* THE QUARRY DIED OR STOPPED BEING A LEGAL TARGET WHILE HELD. */
        if (!foe.alive || this.over){ this.releaseWire(f, foe); continue; }
        W.held += dt;
        W.holdT += dt;
        /* AND THE WIRE LETS GO IF THE HEAD NEVER ARRIVES. Rick, on the shipped
           clip: "the hold needs to expire if the hammer doesn't hit in time."

           THE DISTRIBUTION MAKES THE NUMBER CHOOSABLE RATHER THAN GUESSABLE,
           and it is startlingly bimodal (`hold_lab.py`, 453 catches). A catch
           that CONNECTS holds a median 1.03s and a p90 of 3.82s; a catch that
           NEVER connects holds a median 7.33s and a p90 of 8.52s -- it runs
           the whole window. The head comes round every 0.65s at `spin` 1.6 x
           `spinMul` 6, so a hold past a couple of seconds means the hammer has
           swung through four times and MISSED, which happens because the
           quarry is pinned at up to 144 units between centres while the head
           reaches about 110 and the wielder has to drift in. When it does not
           drift in, the wire used to just hold, for the rest of the eight
           seconds. 45 catches of 453 did that, for 260 seconds of dead hold.

           SO IT LETS GO AND RE-ARMS, RATHER THAN LETTING GO AND BEING SPENT,
           and that is the one part of this Rick's sentence did not settle. A
           spent ring would leave the rest of the window as a fast hammer with
           a dead ring at its reach -- which is the tail he had just rejected
           on `expire:"ring"`, arriving by another road. A ring that can try
           again keeps the window meaning something.

           `reArm` IS NOT DECORATION EITHER. The quarry was caught on the frame
           it ENTERED the ring, so its stored velocity points inward; released
           without a delay it is still inside and is re-caught on the very next
           frame, which is the same infinite hold with a stutter drawn over it. */
        if (u.holdMax && W.holdT >= u.holdMax){
          if (foe.pinFree){
            foe.pin = 0; foe.pinMax = 0; foe.pinV = null; foe.pinFree = 0;
          }
          W.caught = false; W.holdT = 0; W.cd = u.reArm || 0; W.slips++;
          SFX.play("ult", { w: "ravelbone-slip" });
          this.note(`${f.w.name} — the wire slips`);
          continue;
        }
        /* THE HOLD, REFRESHED. There is no duration field for how long a
           SUCCESSFUL hold runs and that is the design: the wire holds until
           the head comes around, and `holdMax` above is a guard rail behind
           that rather than the clock itself. The refresh is comfortably longer
           than a frame so the hold does not flicker, and it is torn down
           explicitly at the connect and at the window's end rather than being
           allowed to run out on its own -- a residual hold after the payoff
           would be the wire still gripping something the hammer has thrown. */
        foe.pin = Math.max(foe.pin, 0.20);
        foe.pinFree = 1;
        /* THE WIRE UNDER TENSION. `_tone` ends on an exponential ramp over
           its whole length, so a HELD note does not exist in this toolkit
           (section 4.5) -- anything that must last is re-struck. */
        W.hum -= dt;
        if (W.hum <= 0){ W.hum = 0.45; SFX.play("ult", { w: "ravelbone-wire" }); }
        continue;
      }

      /* THE CATCH. No cooldown, no timer: the ring is a place it is unsafe to
         be, and it closes on the first frame the quarry is inside it.

         `foe.pin <= 0` IS NOT DECORATION. A ball already held by the Stasis
         Field or by Grasp's squeeze carries a `pinV` that is the vector IT was
         captured with, and catching it again would overwrite that with the
         zero-ish velocity of a ball that is already standing still -- so the
         other relic's quarry would resume from rest and v43's rule would be
         broken from outside the relic that owns it.

         `!foe.shade` IS THE SHADE RULE AND IT IS A DECISION. Triplicate walks
         three bodies and a ring at hit range reaches whichever is nearest;
         this ultimate gets exactly ONE catch, so spending it on a copy that
         is about to expire is a wasted window. The ring snags the real quarry
         only, and `breach_relic_probe`'s precedent applies -- assert whatever
         the code does, over measured opportunities, so reversing it is one
         line and the check moves with it.

         AND THE CASTER IS NEVER SNAGGED by its own ring or by anyone else's:
         `foe` is the other fighter by construction of this loop, and there is
         no second ring in the game to be caught by. */
      /* AND A SPENT RING NEVER CATCHES AGAIN. Under `expire:"ring"` the
         window outlives its own ring, so this is the line that keeps the
         one-catch rule -- and with it the 18.1-point restraint clause the
         design measured. Under the default `expire:"window"` the window is
         already null here and `spent` is never set. */
      if (W.spent) continue;
      /* AND THE RE-ARM AFTER A SLIP. See the note in the caught branch: a
         quarry released inside the ring is still inside it, so without this
         the catch fires again on the next frame. */
      if (W.cd > 0){ W.cd = Math.max(0, W.cd - dt); continue; }
      if (!foe.alive || foe.shade || foe.pin > 0 || this.over) continue;
      const dx = foe.x - f.x, dy = foe.y - f.y;
      if (Math.hypot(dx, dy) > u.radius + R) continue;

      W.caught = true; W.catches++; W.holdT = 0;
      foe.pin = 0.20;
      foe.pinMax = 0.20;
      foe.pinV = [foe.vx, foe.vy];    // what it resumes with, exactly
      foe.pinFree = 1;                // ball held, weapon free. The relic
      /* RICK'S SENTENCE SAYS THE CATCH BLEEDS, AND IT IS MEASURED INERT.
         `hemorrhage` caps at 4 and this hammer's own `onHit` puts on 2 a
         blow, so the bar is full before the ultimate casts -- applying one
         stack on the ring and applying four returned 64.5% and 64.5%,
         identical to the decimal. It is kept because it is his sentence, it
         costs nothing, and the status tag is the only thing on screen that
         says the wire is barbed. The repair for the inertness is stage 3 and
         it is the CONSUME, not a bigger number here. */
      foe.apply("hemorrhage", 1);
      /* THE DIRECTOR HAS TO BE TOLD. Rule 3: this is a control event with no
         damage and no contact, so nothing else in the frame files anything
         and `cinePlan` would score the most legible moment of the ultimate as
         empty air. The CONNECT files its own through `resolveHit`, fatal flag
         included. */
      this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                  w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
      this.hitStop = Math.max(this.hitStop, 0.05);
      this.shake = Math.max(this.shake, 16);
      this.ring(foe.x, foe.y, f.aff.core, 8, 132, 0.40, 5);
      this.ring(foe.x, foe.y, f.aff.glow, 3, 84, 0.28, 3);
      this.spawnFx(foe.x, foe.y, f.aff.glow, 16, 210, 0.40, 3);
      SFX.play("ult", { w: "ravelbone-snag" });
      this.note(`${f.w.name} — caught in the wire`);
    }
  }

  /* THE WINDOW LETS GO. Called when the window runs out, when the caster
     dies, and when the quarry does -- never on the connect, which tears the
     hold down itself in `resolveHit` so the impulse can be delivered to a ball
     that is already free.

     THE `pinFree` GUARD IS LOAD-BEARING. Without it a Garrote window ending
     while PARADOX had the same quarry held would clear the Stasis Field's
     hold, discard its stored vector and release a ball two relics along. */
  releaseWire(f, foe){
    const W = f.ultWire;
    if (W && W.caught && foe && foe.pinFree){
      foe.pin = 0; foe.pinMax = 0; foe.pinV = null; foe.pinFree = 0;
    }
    f.ultWire = null;
  }

  tickStasis(dt){
    /* THE HOLD OUTLIVES THE WINDOW.'''),

# ------------------------------------------------------------ 11. the connect
("resolveHit.wire", '''    const kx = foe.x - self.x, ky = foe.y - self.y, kl = Math.hypot(kx, ky) || 1;
    const power = CONFIG.combat.knock * (self.w.knockMul || 1) * (crit ? 1.5 : 1);
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;

    if (forge){''',
 '''    /* ---- GARROTE'S CONNECT, AND THE RELEASE COMES FIRST.

       `move()` DISCARDS EVERY IMPULSE A BALL TOOK WHILE IT WAS PINNED. It
       ASSIGNS `f.pinV` on the first frame the ball is allowed to move again --
       v43's rule, Rick's own sentence, a measured and named fix. This
       ultimate's headline effect is a massive knockback delivered to a ball
       that is pinned at that exact instant, so applying the impulse before
       clearing the hold means the hit lands, the damage lands, the beat files,
       every probe in the repo passes -- AND THE BALL DOES NOT MOVE.

       So the hold is torn down HERE, above the ordinary knock three lines
       down, rather than in the payload block below it. Written the other way
       round it would still work today, because nulling `pinV` is what actually
       saves the impulse -- and it would break silently the first time anyone
       reordered these two blocks. The order is the guarantee.

       `mul === undefined` is an ordinary melee connect and not a projectile,
       the same test Ironbloom's latch and the Crucible's strike use. */
    const wire = (mul === undefined && self.ultWire && self.ultWire.caught
                  && foe.pinFree && !foe.shade) ? self.ultWire : null;
    if (wire){
      foe.pin = 0; foe.pinMax = 0; foe.pinV = null; foe.pinFree = 0;
    }

    const kx = foe.x - self.x, ky = foe.y - self.y, kl = Math.hypot(kx, ky) || 1;
    const power = CONFIG.combat.knock * (self.w.knockMul || 1) * (crit ? 1.5 : 1);
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;

    if (wire){
      const u = self.w.ult;
      wire.connects++;
      /* THE THROW, AND IT IS NOT THE BRIEF'S BARE `knock x2`. Rick's merge of
         the two v60 designs, 2026-09-01 --
         `06-docs/v60/CONFLICT-READ-FIRST-v60.md`.

         The wire lab priced this as a multiple of a normal blow: x1 +25.2,
         x2 +30.1, x5 +29.8. **+4.9 for the first doubling and nothing after
         it.** It measured the knockback for VALUE and never for whether it
         READS -- and the red hammer measured exactly that and refuted it. The
         impulse is real and exactly `knock x knockMul`, but most of it is
         spent CANCELLING the incoming velocity, because the quarry was
         travelling toward the hammer, which is why they touched. And speed is
         governed rather than conserved: `move()` clamps to [250, 1300] every
         step and relaxes toward an energy-derived target, so whatever survives
         washes out inside the 0.41s median flight to a wall.

         THE SNAG IS WHY THIS ONE LANDS WHERE THAT ONE DID NOT. A ball that has
         just been released from a hold has no incoming velocity to cancel, so
         this is the one case in the game where the whole impulse goes into
         departure.

         `launch` IS A PERMISSION AND NOT A PUSH. It raises the vmax clamp and
         the relax term spends the next second paying it back; it adds no
         velocity at all, which is why below about kick 500 it changes nothing.
         800 is the measured optimum -- widest arrival spread of any arm at
         3.65 and the last value before the arrivals start piling against
         `vmax`. THE CRUCIBLE'S OWN 2400 IS THE WORST VALUE IN THAT SWEEP for a
         mechanic that pays per event rather than once at the end of a charge:
         the spread collapses to 1.70. Copying the game's own constant for the
         same verb on the same weapon type would have reproduced a clipping
         defect one ceiling higher. */
      const extra = power * ((u.connectKnock || 1) - 1) + (u.kick || 0);
      foe.vx += (kx / kl) * extra; foe.vy += (ky / kl) * extra;
      foe.launch = Math.max(foe.launch || 0, u.launch || 0);
      /* AND THE RING EXPIRES. Rick's own sentence -- "causes the barbed wire
         ring to explode and expire" -- and it is the balance clause: letting
         the window run on and the ring RE-ARM is +45.9% against +27.8%, so the
         reward truncating its own reward is worth 18.1 points and is what
         keeps this relic honest.

         BUT `expire` DECIDES WHETHER THE WIND-UP GOES WITH IT, AND THAT WAS
         NEVER A DESIGN DECISION -- it was a build one, made by the ring and
         the window being the same field. Measured on the built relic, the
         wind-up ALONE is +24.3 and the ring alone is +5.3, and the two
         together are +16.2: the connect ends the window after about a third of
         its 8 seconds, so the ring spends two thirds of the thing that is
         actually paying. `expire:"window"` is that behaviour and it is the
         default because it is what shipped; `expire:"ring"` is the arm Rick's
         sentence literally describes -- the RING blows apart, the hammer keeps
         turning for the rest of its window, and it still cannot catch again,
         so the restraint clause the design priced at 18.1 points is kept. */
      if ((u.expire || "window") === "window") self.ultWire = null;
      else { wire.caught = false; wire.spent = true; }
      this.hitStop = Math.max(this.hitStop, 0.14);
      this.shake = 52;
      this.banner = { text: u.name, life: 2.1, max: 2.1, color: self.aff.core,
                      glow: self.aff.glow, w: self.w.id, bx: foe.x, by: foe.y };
      this.ultFx = { w: self.w.id, kind: "wire", phase: "burst",
                     src: self === this.a ? "a" : "b",
                     tgt: self === this.a ? "b" : "a",
                     x: hx, y: hy, tx: foe.x, ty: foe.y, hit: true,
                     radius: u.radius || 110, aff: self.aff, t: 0, life: 1.4 };
      SFX.play("ult", { w: "ravelbone-burst" });
      this.note(`${self.w.name} — ${u.name}`);
      /* THE KILL DOES NOT LAND HERE, and this is the Crucible's own comment
         one relic along: the match holds its breath while the ball flies,
         `checkEnd` waits on `killFlight`, and `move()` clears it at the first
         wall, where the death actually happens. NOT FOR A SHADE -- `tgt` is an
         "a"/"b" key and a copy is neither -- and a wire connect cannot land on
         one anyway, because the ring refuses to catch one. */
      if (fatal && !foe.shade)
        this.killFlight = { tgt: foe === this.a ? "a" : "b", t: 0 };
    }

    if (forge){'''),

# ---------------------------------------------------------- 12. and it fades
("tickPresentation.wireFade", '''      f.breachFade = f.ultBreach ? 1
                   : Math.max(0, f.breachFade - dt / 0.45);''',
 '''      f.breachFade = f.ultBreach ? 1
                   : Math.max(0, f.breachFade - dt / 0.45);
      /* AND THE RING'S. Up instantly, down over 0.35s, so the wire snaps
         rather than being switched off -- the window usually ends ON the
         connect, which sets `hitStop`, and a presentation clock on the normal
         path freezes for exactly the frames the viewer is staring hardest at.
         v54's lesson, fourth relic running. */
      f.wireFade = f.ultWire ? 1
                 : Math.max(0, f.wireFade - dt / 0.35);'''),

# ------------------------------------------------------- 13. the three voices
("SFX.ravelbone", '''        } else if (w === "shroudmaul"){         // an arm comes out of the iron''',
 '''        } else if (w === "ravelbone"){          // the head winds up
          /* THE CAST IS A WINDOW OPENING, so like Revenant's, Deadfall's and
             Shroudmaul's it does not resolve -- nothing has been hit. It is a
             SPIN-UP, and it is the telegraph: the only warning the other
             fighter gets that the ring is now standing at the hammer's reach.

             The chuffs ACCELERATE, because that is what a head going to six
             times its own rate sounds like, and because a fixed cadence would
             say "a thing started" where this has to say "a thing is getting
             faster". They are the four voices' only shared idea with
             Bloodmill's wind-up, which is the other bloodsworn relic that
             spins up -- deliberately, since the school owns the gesture. */
          this._tone (t, { freq: 44, to: 132, gain: 0.30, dur: 1.15, type:"sawtooth" });
          this._tone (t + 0.04, { freq: 128, to: 384, gain: 0.13, dur: 0.95, type:"triangle" });
          [0, 0.20, 0.37, 0.51, 0.62, 0.71, 0.78, 0.84].forEach((d, i) =>
            this._burst(t + d, { freq: 1600 + i * 190, q: 2.8,
                                 gain: 0.085 + i * 0.006, dur: 0.045,
                                 type:"bandpass" }));
          this._burst(t + 0.30, { freq: 520, q: 0.6, gain: 0.10, dur: 0.58, type:"lowpass" });
        } else if (w === "ravelbone-snag"){     // the wire closes on something
          /* THE CATCH. A short metallic SEIZE — a bright band snapping shut
             with a scrape under it — and deliberately not a thud: nothing has
             been hit, something has been CAUGHT, and the difference has to be
             audible or the ultimate sounds like it dealt damage it did not. */
          this._burst(t, { freq: 2400, q: 2.6, gain: 0.16, dur: 0.06, type:"bandpass" });
          this._tone (t, { freq: 420, to: 160, gain: 0.15, dur: 0.20, type:"sawtooth" });
          this._burst(t + 0.03, { freq: 1150, q: 1.5, gain: 0.11, dur: 0.16, type:"bandpass" });
        } else if (w === "ravelbone-wire"){     // and it holds, under tension
          /* THE HARD ONE, and it is section 4.5 rather than a preference.
             `_tone` ends on an exponential ramp over its whole length, so a
             HELD note does not exist in this toolkit -- anything that must
             last is RE-STRUCK. `tickWire` re-strikes this every 0.45s while
             the catch stands, so the number of times it sounds is the number
             of times the wire was still holding.

             Quiet by design: it runs for seconds under a hammer at 6x and
             everything else in the fight, and a sustain that competes is a
             wash rather than a tension. */
          this._tone (t, { freq: 96, to: 88, gain: 0.075, dur: 0.42, type:"sawtooth" });
          this._burst(t + 0.02, { freq: 3100, q: 3.4, gain: 0.045, dur: 0.10, type:"bandpass" });
        } else if (w === "ravelbone-slip"){     // and sometimes it lets go
          /* THE FAILURE, AND IT HAS TO SOUND LIKE ONE. The head never arrived
             and the wire opens on its own -- so this is the snag played
             backwards in shape: a scrape that FALLS instead of a band that
             snaps shut, and quieter than the catch was, because nothing has
             happened. If it sounded like an event a viewer would look for the
             payoff that is not coming. */
          this._tone (t, { freq: 260, to: 90, gain: 0.11, dur: 0.26, type:"sawtooth" });
          this._burst(t + 0.01, { freq: 900, q: 1.8, gain: 0.075, dur: 0.14, type:"bandpass" });
        } else if (w === "ravelbone-burst"){    // and the ring comes apart
          /* THE LOUDEST THING THIS RELIC DOES, because the connect is the
             payoff for an eight-second window and it ends it. A low body for
             the hammer, a wire-parting crack over it, and a spray of barbs.
             Under 0.6s of burst on any one voice — section 4.5, `_burst` does
             not loop its noise buffer and plays silence past that. */
          this._burst(t, { freq: 190, q: 0.5, gain: 0.36, dur: 0.28, type:"lowpass" });
          this._tone (t, { freq: 140, to: 38, gain: 0.30, dur: 0.38, type:"sine" });
          this._burst(t + 0.02, { freq: 3600, q: 1.0, gain: 0.17, dur: 0.08, type:"bandpass" });
          [0, 0.05, 0.10, 0.16, 0.23, 0.31].forEach((d, i) =>
            this._burst(t + d, { freq: 2100 + i * 380, q: 2.4,
                                 gain: 0.12 - i * 0.014, dur: 0.05,
                                 type:"bandpass" }));
          this._tone (t + 0.06, { freq: 300, to: 84, gain: 0.13, dur: 0.46, type:"triangle" });
        } else if (w === "shroudmaul"){         // an arm comes out of the iron'''),

# ------------------------------------------------------------- 14. the art
("draw.wire.calls", '''    this.drawCrackle(m, false);
    this.drawGrip(m, false);''',
 '''    this.drawCrackle(m, false);
    this.drawGrip(m, false);
    /* the ring is a place in the hall and the balls are inside it */
    this.drawWire(m, false);'''),

("draw.wire.calls.over", '''    this.drawCrackle(m, true);
    this.drawGrip(m, true);''',
 '''    this.drawCrackle(m, true);
    this.drawGrip(m, true);
    /* and the wire on a caught ball is ON the shell, so it goes over it */
    this.drawWire(m, true);'''),

("drawWire", '''  drawGrip(m, over){''',
 '''  /* ---------------------------------------------------------- GARROTE --
     THE RING, THE CATCH, AND THE ONE PICTURE THIS GAME HAS NEVER DRAWN.

     Brief section 9: "THE SNAG — the foe stops moving AND KEEPS SWINGING. If
     this does not read, the ultimate looks like a stun and the whole
     separation is invisible." The weapon half is free — `f.stun` is never
     written, so the caught fighter's blade goes on turning through the normal
     renderer with no code here at all. What has to be drawn is the other half:
     the ball is not stopped, it is HELD, and something is holding it.

     THREE SEPARATIONS FROM EVERY OTHER HOLD IN THE GAME, because any one of
     them can be lost to a phone screen or to the bloom:
       the SHAPE   barbed wire cinched round the shell, not a closed polygon
       the COLOUR  bloodsworn, where the Stasis Field's hold is runic
       the LINE    a wire runs from the ring to the ball, so the eye can see
                   what is doing the holding and where it came from

     AND THE RING IS THE HAMMER'S OWN HIT RANGE, DRAWN. It is the first object
     in this game whose area IS the weapon's reach: a viewer who sees the ring
     knows precisely where it is unsafe to be, and the hold that follows is the
     rule being enforced rather than a thing that happened.

     NOTHING HERE DRAWS FROM `this.rng()`. The wobble and the barbs are
     functions of their own index, so a relic not in the match cannot perturb
     the draw order of one that is — the house rule since Ironbloom's
     splinters, and the reason the blade does not have to be re-measured every
     time this art is re-cut.

     Split `false`/`true` exactly as `drawGrip` and `drawVines` are, and for
     the same reason: the ring is a place in the hall and belongs under the two
     balls that own the health bars, while the wire biting a caught shell is ON
     that shell and belongs over it. */
  drawWire(m, over){
    const A = m.a, B = m.b;
    if (!(A.ultWire || A.wireFade > 0 || B.ultWire || B.wireFade > 0)) return;
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const [f, foe] of [[A, B], [B, A]]){
      const fade = f.wireFade || 0;
      if (fade <= 0) continue;
      const W = f.ultWire;
      const u = f.w.ult;
      const rad = (u && u.radius) || 110;
      const P = f.aff;
      /* THE WIND-UP IS THE TELEGRAPH and it is the only warning the other
         fighter gets, so the ring arrives fast and leaves slowly: `wireFade`
         is 1 the instant the window opens and eases out over 0.35s after it
         closes. `t` drives the crawl, and it is the MATCH clock rather than
         the window's, so the wire does not restart its texture on a re-cast. */
      const t = m.t;

      /* A SPENT RING IS NOT DRAWN. Under `expire:"ring"` the window runs on
         with the hammer still turning and nothing at its reach -- and a ring
         still on screen after it has visibly blown apart would be the picture
         contradicting the mechanic, which is what v56's latch did. */
      if (W && W.spent) continue;
      if (!over){
        c.save();
        c.lineCap = "round"; c.lineJoin = "round";
        /* ---- THE RING. A closed strand with a wobble on it, because a true
           circle reads as a UI element and the one thing this must not read as
           is a range indicator. Two passes: a dark core so it is legible
           against the hall's own glow, and a hot strand over it. */
        const N = 96, seg = TAU / N;
        /* AND IT STROKES. The first cut of this built the path and returned
           without stroking it, so the STRAND WAS NEVER ON SCREEN -- the only
           thing drawn was the 34 barb spurs, which read as a dashed circle and
           therefore as a range indicator, which is the one thing brief section
           9 says this object must not be. Nothing threw, the probe's render
           check called `drawWire` on 989 frames and passed, and it took a
           photograph of a real match to see it. Section 4.1's defect class:
           wrong and right produce identical numbers. */
        const strand = (phase, amp) => {
          c.beginPath();
          for (let i = 0; i <= N; i++){
            const a = i * seg;
            const wob = Math.sin(a * 7 + phase) * 0.55
                      + Math.sin(a * 13 - phase * 1.7) * 0.30
                      + Math.sin(a * 3 + phase * 0.6) * 0.15;
            const rr = rad + wob * amp;
            const x = f.x + Math.cos(a) * rr, y = f.y + Math.sin(a) * rr;
            if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
          }
          c.closePath();
          c.stroke();
        };
        c.globalAlpha = fade * 0.85;
        c.strokeStyle = "#160406"; c.lineWidth = 5.2; strand(t * 1.6, 5.5);
        c.strokeStyle = P.core;    c.lineWidth = 2.4; strand(t * 1.6, 5.5);
        c.globalAlpha = fade * 0.55;
        c.strokeStyle = P.glow;    c.lineWidth = 1.2; strand(t * 1.6 + 2.1, 7.5);

        /* ---- THE BARBS. Short spurs at a slight angle, alternating in and
           out, and they are what makes a strand read as BARBED rather than as
           a hoop. Spaced by index so they crawl with the strand. */
        c.globalAlpha = fade * 0.9;
        c.strokeStyle = P.core; c.lineWidth = 2.0;
        const NB = 34, bseg = TAU / NB;
        c.beginPath();
        for (let i = 0; i < NB; i++){
          const a = i * bseg + t * 0.22;
          const wob = Math.sin(a * 7 + t * 1.6) * 0.55
                    + Math.sin(a * 13 - t * 2.7) * 0.30;
          const rr = rad + wob * 5.5;
          const cx = f.x + Math.cos(a) * rr, cy = f.y + Math.sin(a) * rr;
          const sgn = (i % 2) ? 1 : -1;
          const lean = a + sgn * 0.85;
          const L = 6.5 + 2.2 * Math.sin(i * 2.4);
          c.moveTo(cx, cy);
          c.lineTo(cx + Math.cos(lean) * L * sgn, cy + Math.sin(lean) * L * sgn);
        }
        c.stroke();

        /* ---- AND THE LINE TO WHAT IT CAUGHT. Drawn UNDER the balls so it
           reads as running behind the shell rather than across it, with the
           cinch over the top in the `over` pass. Without this the ring and the
           held ball are two separate facts and the viewer has to infer the
           one that matters. */
        if (W && W.caught && foe.alive){
          const dx = foe.x - f.x, dy = foe.y - f.y;
          const dl = Math.hypot(dx, dy) || 1;
          const ux = dx / dl, uy = dy / dl;
          const x0 = f.x + ux * rad, y0 = f.y + uy * rad;
          const x1 = foe.x - ux * R * 0.9, y1 = foe.y - uy * R * 0.9;
          c.globalAlpha = fade * 0.9;
          c.strokeStyle = "#160406"; c.lineWidth = 4.4;
          this._wireLine(x0, y0, x1, y1, t);
          c.strokeStyle = P.core; c.lineWidth = 2.0;
          this._wireLine(x0, y0, x1, y1, t);
        }
        c.restore();
        continue;
      }

      /* ---- THE CINCH, over the shell. THIS IS THE PICTURE THE WHOLE DESIGN
         RESTS ON: a ball that is held, with a weapon that is still turning.
         Two loops of wire pulled tight round the shell with the barbs biting
         inward — deliberately NOT a closed ring and deliberately NOT the
         stagger tell, because a stagger is a weapon that stopped and this is a
         BALL that stopped, and the picture has to be able to tell a viewer
         which one it is looking at. */
      if (!(W && W.caught && foe.alive)) continue;
      c.save();
      c.lineCap = "round"; c.lineJoin = "round";
      const rr = R * 1.06;
      for (let k = 0; k < 2; k++){
        const tilt = (k ? -1 : 1) * 0.42 + Math.sin(t * 0.9 + k) * 0.06;
        c.beginPath();
        for (let i = 0; i <= 40; i++){
          const a = -TAU * 0.5 + (i / 40) * TAU;
          const x = foe.x + Math.cos(a) * rr;
          const y = foe.y + Math.sin(a) * rr * 0.34;
          const cs = Math.cos(tilt), sn = Math.sin(tilt);
          const px = foe.x + (x - foe.x) * cs - (y - foe.y) * sn;
          const py = foe.y + (x - foe.x) * sn + (y - foe.y) * cs;
          if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
        }
        c.globalAlpha = fade * 0.95;
        c.strokeStyle = "#160406"; c.lineWidth = 4.0; c.stroke();
        c.strokeStyle = P.core;    c.lineWidth = 1.9; c.stroke();
      }
      /* the barbs that are in it */
      c.globalAlpha = fade;
      c.strokeStyle = P.glow; c.lineWidth = 1.7;
      c.beginPath();
      for (let i = 0; i < 10; i++){
        const a = i * (TAU / 10) + t * 0.5;
        const x = foe.x + Math.cos(a) * rr * 0.96;
        const y = foe.y + Math.sin(a) * rr * 0.96;
        c.moveTo(x, y);
        c.lineTo(x + Math.cos(a) * 5.0, y + Math.sin(a) * 5.0);
      }
      c.stroke();
      c.restore();
    }
  }

  /* One strand, with the same wobble the ring carries so the two read as the
     same material. Deterministic in its own arguments and nothing else. */
  _wireLine(x0, y0, x1, y1, t){
    const c = this.ctx;
    const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1;
    const nx = -dy / L, ny = dx / L;
    c.beginPath();
    for (let i = 0; i <= 24; i++){
      const s = i / 24;
      const w = (Math.sin(s * 14 + t * 3.1) * 0.6
               + Math.sin(s * 27 - t * 4.4) * 0.3) * 3.4 * Math.sin(s * Math.PI);
      c.lineTo(x0 + dx * s + nx * w, y0 + dy * s + ny * w);
    }
    c.stroke();
  }

  drawGrip(m, over){'''),
]


# ============================================================ STAGE 3 =======
# THE CONSUME, AND IT IS THE REPAIR FOR A SENTENCE THAT MEASURED INERT.
# Rick's section 1 says the catch bleeds and the explosion bleeds again.
# `hemorrhage` is `{maxStacks: 4, dur: 3.2, dps: 1.5}` and this hammer's own
# `onHit` puts on 2 a blow, so the bar is full before the ultimate casts:
# applying ONE stack on the explosion and applying FOUR returned 64.5% and
# 64.5%, identical to the decimal. Two repairs were priced and the obvious one
# -- Bloodmirror's ceiling trick, 4 -> 8 while the ring stands -- transfers
# NOTHING here (+0.0), because Bloodletting mills at 0.22s and needs headroom
# where this hammer lands 8.6 blows a fight and cannot fill 4, let alone 8.
S3 = [

# ------------------------------------------------------- 1. what it consumes
("resolveHit.consume", '''    const curseEcho = Math.round(foe.curseEcho());
    const dmgBase = dmg;
    dmg += curseEcho;''',
 '''    /* ---- GARROTE CONSUMES THE BLEED, AND IT IS FOLDED INTO `dmg` FOR THE
       REASON THE ECHO ABOVE IS: a burst dealt BESIDE the blow is a second
       number over the ball that a wall does not eat, a ward does not absorb,
       hit stop does not scale with and knockback does not carry. Added here,
       above the aegis block, it is part of the hit.

       READ BEFORE IT IS PAID, which is the same rule the echo two lines up
       follows and the same one the Crucible's forge follows for Sunder. The
       stacks are counted first and the status is deleted in the same act, so
       the pool cannot pay twice.

       THE QUARRY'S ONLY, and never the caster's. Five other bloodsworn relics
       put Hemorrhage on and both fighters can be carrying it; `foe` is the
       thing the wire caught.

       AND IT IS A DAMAGE KNOB WEARING AN INTERACTION'S CLOTHES, which is worth
       saying where the code is. `connect dmg x2` -- plain extra damage, no
       bleed involved -- is +33.6, and consume-at-14 is +36.6. They are the
       same curve. What the consume buys is LEGIBILITY, not strength: the
       payoff scales with the fight the hammer has actually had, so a long
       grind pays a bigger burst than an early cast does. Linear at +0.73 win
       points per point of per-stack damage, which makes it the LAST thing that
       should move -- it and the blade trade directly and the blade is the
       coarser instrument. */
    let wireBurst = 0;
    if (wire){
      wireBurst = foe.stacks("hemorrhage") * (self.w.ult.consume || 0);
      delete foe.status.hemorrhage;
      wire.burst = wireBurst;
    }

    const curseEcho = Math.round(foe.curseEcho());
    const dmgBase = dmg;
    dmg += curseEcho + wireBurst;'''),

# ---------------------------- 2. and the detection has to be above the damage
("resolveHit.hoist", '''    const wire = (mul === undefined && self.ultWire && self.ultWire.caught
                  && foe.pinFree && !foe.shade) ? self.ultWire : null;
    if (wire){
      foe.pin = 0; foe.pinMax = 0; foe.pinV = null; foe.pinFree = 0;
    }

    const kx = foe.x - self.x''',
 '''    if (wire){
      foe.pin = 0; foe.pinMax = 0; foe.pinV = null; foe.pinFree = 0;
    }

    const kx = foe.x - self.x'''),

("resolveHit.detect", '''    const crit = this.rng() < (forge''',
 '''    /* GARROTE'S CONNECT IS DETECTED HERE, ABOVE THE DAMAGE, because stage 3
       folds the consume into `dmg` and a detection below it would be reading
       the quarry's Hemorrhage after the blow had already been priced. The
       RELEASE still happens further down, immediately above the ordinary
       knock -- see the paragraph there, and do not move it.

       `mul === undefined` is an ordinary melee connect and not a projectile,
       the same test Ironbloom's latch and the Crucible's strike use. */
    const wire = (mul === undefined && self.ultWire && self.ultWire.caught
                  && foe.pinFree && !foe.shade) ? self.ultWire : null;

    const crit = this.rng() < (forge'''),

# ---------------------------------------------------- 3. and the card says so
("ult.tip", '''          tip:"%TIP%" },''',
 '''          tip:"%TIP3%" },'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
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
    """Code with the prose taken out.

    CLAUDE.md: "a check that cannot tell code from the comment explaining it
    fires on its own explanation." Every refusal below greps a span of shipped
    source and this file explains itself IN that source -- `tickWire`'s own
    comment has to say the words "do not write f.stun".
    """
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def span(s: str, head: str, label: str) -> str:
    """The body of one method, by brace matching from its signature."""
    i = s.find(head)
    if i < 0:
        raise SystemExit(f"cannot find `{label}` in the build")
    j = s.index("{", i)
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return s[j:k + 1]
        k += 1
    raise SystemExit(f"unbalanced braces in `{label}`")


def ult_matches(s: str, A, stage: int) -> None:
    """The shipped `ult` block carries every number this run printed.

    v56's own failure, verbatim: the stage-2 insert wrote the whole `ult` block
    and stage 3 rewrote only the line carrying `charge`, so `--stage 3
    --cadence 2.0` LOGGED the new rhythm and SHIPPED the old one -- and every
    gate downstream measured a relic the log was not describing. It was caught
    by a probe printing `n=5` two minutes later.
    """
    i = s.index(f'id:"{RELIC}"')
    # THE PROSE IS STRIPPED FIRST, and it is not a nicety: this relic's own
    # comment says "STUBBED AT `charge:1e9` IN STAGE 1", so without this the
    # check reads the HISTORY of the build instead of the build.
    blk = strip_comments(s[i:s.index("blurb:", i)])
    want = {k: getattr(A, k.lower()) for k in ULT}
    # STAGE 1 SHIPS THE STUB, and 1e9 is what it is FOR: the clock can never
    # reach it, so `fireUlt` never runs and the relic is measured as a blade
    # and a channel. Expecting `--charge` here would fire on the stub this
    # stage was told to write.
    want["charge"] = 1e9 if stage == 1 else A.charge
    # AND THE ONE KNOB THAT IS A STRING. It is checked here for exactly v56's
    # reason and it has already caught itself once: `--expire ring` passed to
    # STAGE 3 printed the variant and shipped the default, because `expire` is
    # written by the stage-2 `ult` block. A knob that silently does not apply
    # is the failure this whole function exists to stop, and a number is not
    # the only shape it comes in.
    m = re.search(r'expire:\s*"([a-z]+)"', blk)
    got = m.group(1) if m else "(absent)"
    if got != A.expire:
        raise SystemExit(
            f"the shipped ult block says expire:{got!r} and this run printed "
            f"{A.expire!r}."
            f"\n  `expire` is written by the STAGE-2 ult block -- pass it "
            f"there, not to stage 3.")
    bad = []
    for k, v in want.items():
        m = re.search(rf"\b{k}:\s*([0-9.e+]+)", blk)
        if not m or abs(float(m.group(1)) - float(v)) > 1e-9:
            bad.append(f"{k}: shipped {m.group(1) if m else '(absent)'}, "
                       f"printed {v:g}")
    if bad:
        raise SystemExit("the shipped ult block does not carry what this run "
                         "printed:\n  " + "\n  ".join(bad))
    print("  ult   every number in the shipped block matches this run")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True, choices=(1, 2, 3, 4))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--tip3", default=ULT_TIP3)
    ap.add_argument("--expire", default=EXPIRE,
                    choices=("window", "ring"),
                    help="what the connect ends. See sections "
                         "5c/5d of the write-up -- this is the "
                         "difference between +16.2 and the "
                         "wind-up's own +24.3")
    ap.add_argument("--charge", type=float, default=16.0)
    # THE BLADE BELONGS TO WHICHEVER STAGE IS RUNNING. v56 defaulted every
    # stage to the tuned value, which made stage 2 write it and stage 3 then
    # fail looking for the starting value it was supposed to replace.
    ap.add_argument("--dmg", type=float, default=None,
                    help="stages 1-3: the starting blade (default %.2f). "
                         "stage 4: the bisected one, and it has no default"
                         % BLADE_IN)
    for k, v in ULT.items():
        ap.add_argument(f"--{k.lower()}", type=float, default=v)
    A = ap.parse_args()
    if A.dmg is None:
        A.dmg = TUNED_RB if (A.stage == 3 and TUNED_RB is not None) else BLADE_IN

    src = A.src or {1: "../02-chain/sc-breach.html",
                    2: "../02-chain/sc-ravelbone.html",
                    3: "../02-chain/sc-wire.html",
                    4: "../02-chain/sc-garrote.html"}[A.stage]
    out = A.out or {1: "../02-chain/sc-ravelbone.html",
                    2: "../02-chain/sc-wire.html",
                    3: "../02-chain/sc-garrote.html",
                    4: "../02-chain/sc-garrote.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nRAVELBONE -- STAGE {A.stage}: "
          + {1: "the 30th relic, its ultimate stubbed",
             2: "THE RING -- snag, hold, connect, throw. No consume yet",
             3: "GARROTE -- the explosion consumes Hemorrhage",
             4: "THE BLADE, and it is the only number this stage moves"
             }[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the curse rework is "
                         "upstream of this whole chain")
    if "tickBreach" not in s0:
        raise SystemExit("this source is not the v59 tip -- `tickBreach` is "
                         "absent.\n  Build off `sc-breach.html`.")
    if "_whBarbed" not in s0:
        raise SystemExit("this source has no `_whBarbed`, so bloodsworn x "
                         "warhammer has nothing to draw with.")

    tip = A.tip
    if len(tip) > 72:
        raise SystemExit(f"ULT TIP is {len(tip)} characters against 72:\n  {tip}")
    # THE RING IS THE HAMMER'S OWN REACH, DRAWN, and that is the only thing it
    # means. Widening it past 110 to buy strength stops it meaning anything --
    # 150 is -5.2 points and 220 is -6.0, so it would not even buy the strength.
    if A.radius > 110.0 + 1e-9:
        raise SystemExit(
            f"radius {A.radius:g} is wider than the hammer's own hit range "
            f"(brief section 10).\n  reach 76 + ballR 34 = 110 is where a blow "
            f"actually lands, and it is\n  the only thing the ring means.")
    # DO NOT USE CRUCIBLE'S NUMBER ON CRUCIBLE'S OWN WEAPON TYPE. The sweep is
    # flat to noise across x2 -> x12, so there is no cost to avoiding it.
    if abs(A.spinmul - 3.4) < 1e-9:
        raise SystemExit("spinMul 3.4 is Crucible's exact number on this same "
                         "weapon type (brief section 10).\n  The sweep is flat "
                         "to noise from x2 to x12 -- pick anything else.")

    subs = {"%ULT%": A.ult, "%TIP%": tip, "%TIP3%": A.tip3, "%BLURB%": BLURB,
            "%DMG%": f"{A.dmg:g}", "%CHARGE%": f"{A.charge:g}",
            "%DUR%": f"{A.dur:g}", "%RADIUS%": f"{A.radius:g}",
            "%SPINMUL%": f"{A.spinmul:g}", "%CONNECTKNOCK%": f"{A.connectknock:g}",
            "%KICK%": f"{A.kick:g}", "%LAUNCH%": f"{A.launch:g}",
            "%CONSUME%": f"{A.consume:g}", "%EXPIRE%": A.expire,
            "%HOLDMAX%": f"{A.holdmax:g}", "%REARM%": f"{A.rearm:g}",
            "%D_EXPIRE%": EXPIRE}
    # WHAT STAGE 1 WROTE, which is this module's defaults and never this run's
    # arguments. Only the stage-2 `ult` block reads these, and only on the OLD
    # side of the edit -- see the note there.
    subs.update({f"%D_{k.upper()}%": f"{v:g}" for k, v in ULT.items()})

    if A.stage == 1:
        if f'id:"{RELIC}"' in s0:
            raise SystemExit("this source already has Ravelbone -- built")
        edits = S1
        print(f"  ult {A.ult}  STUBBED at charge 1e9")
        print(f"  tip {len(tip)}/72  {tip}")
        print(f"  blade {A.dmg:g}   (the type's own, and a bisection START)")
    elif A.stage == 2:
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("this source has no Ravelbone -- stage 1 first")
        if "tickWire" in s0:
            raise SystemExit("this source already has tickWire -- built")
        if not S2:
            raise SystemExit("stage 2 is not written yet")
        edits = S2
    elif A.stage == 3:
        if "tickWire" not in s0:
            raise SystemExit("this source has no tickWire -- stage 2 first")
        if not S3:
            raise SystemExit("stage 3 is not written yet")
        edits = S3
    else:
        # STAGE 4. ONE NUMBER, IN PLACE, AND NOTHING ELSE.
        #
        # AND IT REFUSES UNTIL THE STAGE-2 GATE IS UNDERSTOOD. The ring was
        # registered at +24 +/- 3 over this relic's own no-ultimate floor and
        # measured +16.2 +/- 2.5 -- about 2.1 sigma, which is a real
        # discrepancy and not a broken relic. The brief's own instruction is
        # that a stage-2 miss means something is wrong with the RING, and that
        # "the consume will paper over whatever is wrong ... until the
        # bisection misbehaves". A bisection run over an unexplained ring is
        # the exact failure that sentence describes, so this refuses to run
        # until somebody sets TUNED_RB deliberately.
        if "hemorrhage" not in strip_comments(span(s0, "  resolveHit(self, foe,"
                                                   " hx, hy, seg, mul, over){",
                                                   "resolveHit")):
            raise SystemExit("this source has no consume -- stage 3 first")
        if TUNED_RB is None:
            raise SystemExit("\n".join((
                "TUNED_RB is None and stage 4 has no default (v56's lesson).",
                "  Measure it FIRST -- and read"
                " `06-docs/v60/ravelbone-build-v60.md` section 5a",
                "  before you do, because the stage-2 gate has not been"
                " explained, and a blade",
                "  bisected over an unexplained ring is exactly what that gate"
                " exists to stop.",
                "  WHAT SETTLES A BLADE ON THIS ROSTER IS A WIDE DIRECT"
                " MEASUREMENT AT",
                "  n >= 1000 A POINT, ON BOTH SIDES, REPEATED ON A SECOND"
                " BLOCK -- never a",
                "  bisection (CLAUDE.md, twice, and the second time it cost a"
                " whole damage point).")))
        edits = []

    for label, old, new in edits:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    if A.stage == 4:
        # THE FIVE WARHAMMERS SHARE A STAT LINE, so the blade is found by
        # walking forward from this relic's own id and never by a global
        # replace -- `dmg:23.5` is Grudgebearer's value too.
        i = s.index(f'id:"{RELIC}"')
        j = s.find(f"dmg:{BLADE_IN:g},", i)
        if j < 0 or j - i > 400:
            raise SystemExit(f"cannot retune: dmg:{BLADE_IN:g} is not in "
                             f"Ravelbone's own entry. Already tuned?")
        s = s[:j] + f"dmg:{A.dmg:g}," + s[j + len(f"dmg:{BLADE_IN:g},"):]
        print(f"  blade dmg {BLADE_IN:g} -> {A.dmg:g}")

    ult_matches(s, A, A.stage)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")

    if A.stage == 1:
        print("\n  NEXT:")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40      # 30 relics")
        print("      the floor: Ravelbone with no ultimate, near 37% at "
              "blade 23.5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
