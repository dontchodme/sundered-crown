#!/usr/bin/env python3
"""SHROUDMAUL, THE 28TH RELIC, AND ITS ULTIMATE GRASP. STAGES 2 AND 3.

    python shroudmaul_build.py --stage 2 --src ../02-chain/sc-revenant.html \
                               --out ../02-chain/sc-shroudmaul.html
    python shroudmaul_build.py --stage 3 --src ../02-chain/sc-shroudmaul.html \
                               --out ../02-chain/sc-grasp.html

`06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md`. STAGE 1 (`revenant_rename.py`) lands
first and has to be bit-identical before this file is opened, because it is the
only stage in the build that can be proven inert.

## RICK'S §1, VERBATIM

    for a duration the artifact grows an etherial skeletal hand that reaches
    out and grabs nearby enemies. the grab does no damage and doesn't apply
    curse but it does apply massive hit stun. if it grabs several times in one
    trigger (2-6 depending on balance) it true stuns for extra duration and
    then dissipates.

## THE WHOLE ULTIMATE IS ONE SCALAR, AND THAT IS THE MOST USEFUL THING KNOWN
## ABOUT IT

`grab_lab.py`, fourteen arms at 702 fights each, regressed on total seconds the
foe spends held:

    lift = +3.1 + 2.62 x held seconds      r2 = 0.79
    residual sd 2.7pp against a per-arm SE of 5.3pp

**The residuals are smaller than the measurement error.** Window length, grab
cadence, grab hold, true-stun length, grab count and whether the window
survives its own payoff are six ways of writing one number. Two consequences,
and both are load-bearing for anybody who touches this relic later:

    TUNE ON `held`, NOT ON WIN RATE.  30x cheaper and it is what the win rate
                                     is made of. `grasp_relic_probe [11]`.
    THE ARRANGEMENT IS FREE.         Any shape delivering 6.5-7.0 held seconds
                                     is worth the same, so every remaining
                                     choice is made for the picture.

The ONE knob that is not free is REACH, and it departs from the line in the
direction that says something: radius 140 costs 2.7 points and 300 costs 4.0 AT
THE SAME HELD SECONDS. **A hold is only worth what the hammer can reach.** At
300 the hand catches the quarry out at the far wall and holds it somewhere the
wielder then has to walk to -- the blows column falls while the grabs column
rises. 200 is about 2.6x the warhammer's own reach of 76.

## AND "THEN DISSIPATES" IS THE BALANCE KNOB, NOT A COST

    n=4  window ENDS on the true stun      +20.4%
    n=4  window RUNS ON, counter resets    +31.2%      the clause is 10.8 points

Without it the ultimate is sixth of twenty-eight and the blade would have to be
cut hard to pay for it. With it, the median. It is also a rule a viewer can
WATCH rather than read: the hand closes, it holds, it is gone.

## WHAT WILL BITE, AND THE FIRST ONE IS THE EASIEST WAY TO BUILD THIS WRONG

**`stunDR` MUST NOT BE IN THIS PATH.** `takeHitstun` caps at `stunMax` 0.26s
and divides each application by `1 + 0.55 x stunDR`. Route the grabs through it
and the second grab onward is eaten: five grabs become one grab and a rumour,
every invariant still holds, no probe fails, and the only symptom is a `held`
column that does not move when the knobs do. The grabs write `f.stun` directly,
exactly as `u.freeze` does -- which is also why "massive hit stun" in the §1 is
not `takeHitstun`. Nothing routed through that function can be massive.

**THE TRUE STUN IS AN APPLICATION SITE, NOT A DURATION.** Rick's own rule, in
the engine in his own words: *"Hitstun shouldnt stop the windup. but true stuns
from ults/abilities should."* There is no flag -- every source writes the same
`f.stun` -- so the distinction is drawn at the SITES, and there were exactly
three. This build makes it four, and **only the fifth grab joins the list**.
The four ordinary grabs delay a wind-up; they do not cancel it.

**THE ART HANGS OFF THE FIGHTER.** v54 §2a, now a chain-wide open item:
`m.ultFx` is ONE SLOT and the opponent casting anything overwrites it -- 0.0%
survival against Ironhail. Deadfall survived only by being rebuilt onto
`f.ultDeadfall`. This one starts there: `f.ultGrasp` and `f.graspFade`, drawn
by one function called twice, the shape of `drawVines(m, false/true)`.

**AND `atSelf` ON THE FX SPEC** (v54 §2b). `drawUltOver` puts a `burst` field
at `[u.tx, u.ty]` -- at the QUARRY -- which is right for the four novas it was
written for and wrong for a hand that grows out of the caster.

**DO NOT WRITE `f.pin`.** Measured at **-3.3 points against stun alone at
identical held seconds**, and consistent with the reach result: a pinned ball
cannot be knocked toward the wielder, and this relic needs the quarry to
arrive. `f.pin` is also written by exactly one relic in the game. The picture
follows the mechanic rather than fighting it -- **the hand grips the WEAPON,
not the ball**, which is what `f.stun` models and what the frame shows.

## THE ART IS THE ONLY EVIDENCE THE ULTIMATE HAPPENED

This ultimate deals no damage, so there is no number on screen, no hit-stop
scaled to it, no health bar moving. Rick, unprompted, in the §1: *"this ult
will need a unique animation for the hand, the reaching and grabbing, as well
as a unique animation for the true stun grab."*

    REVENANT   MANY hands, SMALL, AIRBORNE, thrown off blows, converging at
               2500px/s and closing into fists. On screen 1.8s per hand
    GRASP      ONE hand, LARGE, TETHERED -- it grows FROM the artifact and
               stays attached to it for the whole window. It reaches, opens,
               closes, HOLDS

One versus many, tethered versus airborne, reaching versus striking. **The
tether is the strongest of the four and it is free**: nothing else in the game
connects the wielder to the quarry with a limb, and it is on screen for eight
seconds rather than 1.8.

EVERYTHING BELOW IS A FIRST CUT AND NOBODY HAS WATCHED IT. v54 §2c is the
precedent and it nearly shipped broken -- Deadfall's ARMING state was drawn at
alpha 0.16 against a hall that already had a gold pentagram on its floor, and
photographed off a real match the two states did not separate at all. FILM IT
BEFORE TUNING ANYTHING.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "shroudmaul"

# --- THE RELIC. Every physical stat is the WARHAMMER'S, copied off the three
#     that already exist and not invented. Weapon-matrix decision 1: the TYPE
#     owns the physics, the SCHOOL owns status and palette. `_whEaten` already
#     exists and is already the umbral branch of `SHAPES.warhammer`, so the
#     silhouette is not new work -- it is 78.6% distinct from its nearest
#     sibling and 3rd most distinct of the fifteen open cells.
BLADE_IN = 23.5      # Grudgebearer's, as a start (brief §3.2)
TUNED_SM = 21.0      # STAGE 3b. See below -- and 19.92 is what the bisection
                     # said, before four wider measurements refuted it.

# --- STAGE 3b. THE BLADE WAS PREDICTED NOT TO MOVE MUCH, AND IT MOVED PAST THE
#     BOTTOM OF THE REGISTERED RANGE -------------------------------------------
#
# The brief registered: *"the blade bisects to somewhere in 21-23.5 rather than
# moving far."* Measured: **19.92**, and the reason is the same one that put
# `held` out of band -- the built relic casts more often than the lab's did.
#
#   `umbral_sweep.py --relics shroudmaul --lo 12 --hi 26`, 4617 fights
#
#     pass 1, the curve, n=162 a point
#       12.00   9.3%     18.00  32.1%     24.00  64.8%
#       14.00  24.7%     20.00  47.5%     26.00  66.0%
#       16.00  32.7%     22.00  53.1%
#
#     pass 3, the wide confirmation, n=702 a point, ONE SIDE
#       19.92  50.0%     20.42  50.4%     20.92  52.1%     -> 19.92
#
# AND 19.92 IS WRONG BY A DAMAGE POINT, WHICH FOUR WIDER MEASUREMENTS SAY AND
# THE SWEEP'S OWN CONFIRMATION COULD NOT. `umbral_sweep`'s three-point
# confirmation is n=702 a point with the relic always on SIDE A, and the seed
# block it happened to draw reads about four points high. Everything else
# disagrees with it:
#
#     umbral_sweep pass 3, side A, n=702        50.0%   at 19.92
#     shroudmaul_sweep type ladder, side A, n=702  45.2%
#     an independent side-A block, n=702        45.7%
#     verify --n 40, side B, n=1080             45.4%
#
# So it was re-measured DIRECTLY and WIDE, both sides, n=1080 a point, on two
# independent seed blocks:
#
#     block 1   19.92  45.4%   21.00  49.1%   22.00  54.1%   23.00  59.2%
#     block 2   20.68  47.9%   21.18  52.0%   21.68  52.6%
#
# Both monotonic, both crossing 50% at about 21.0, and block 1 reproduces
# `verify`'s 45.4% at 19.92 to the decimal.
#
# THE LESSON IS v48'S, AND THIS IS THE SECOND TIME. A bisection converges on
# the noise in its own tail, and a three-point confirmation is only as good as
# the ONE seed block it is drawn on. What settles a blade on this roster is a
# WIDE DIRECT MEASUREMENT AT n >= 1000 A POINT, ON BOTH SIDES, REPEATED ON A
# SECOND BLOCK -- and the difference between two n=702 readings of the same
# number here was 4.3 points.
#
# BOTH SIDES MATTERS BECAUSE OF WHERE THIS RELIC SITS IN THE ARRAY, AND NOT
# BECAUSE THE SIDES ARE VERY DIFFERENT. `verify` pairs `i < j`, so a relic
# appended to `WEAPONS` is side B in all 27 of its pairings while every sweep
# in `tools/` runs it as side A. Measured, the asymmetry is small -- shroudmaul
# -1.9pp, grudgebearer +2.6pp, nightfell -0.3pp -- so it is not the explanation
# here. It is measured both ways so that the question cannot arise.
#
# AND THIS CURVE DOES NOT BEND, which is worth stating because the school's
# does: Gravemourn reads 67.3% at 47.2 and 60.6% at 52.0, because a bigger blow
# throws the quarry out of reach of a weapon that lands 5.6 times a fight.
# Shroudmaul is monotone from 9.3% at 12 to 66.0% at 26. The sweep was still
# run WIDE FIRST, because a bisection cannot tell you which of those two shapes
# it is standing on -- CLAUDE.md, and the third build in a row to need it.
#
# THE HONEST PRECISION IS +/- HALF A DAMAGE POINT, which is why this ships as a
# round 21.0 and not as a hundredth.
#
# AND UNLIKE THE LAST THREE BUILDS THE SURFACE HERE IS SIMPLE. `dmg` moves the
# blade and the pool; it does NOT move the ultimate, because the ultimate
# carries no damage and reads nothing. v51 §4.5's superlinear warning does not
# apply, and the one knob that moves the ultimate is `n`.
#
# WHAT THE CUT BUYS, and it does not gut the relic: measured at 19.92 the echo
# is 16.6% of everything Shroudmaul delivers, the pool means 75 and peaks at
# 214, and it is UP 87% of the fight and FULL 63% -- the deepest pool in the
# school, which is the cell's whole argument (v55 §4) surviving the bisection.
# At 21.0 all five are slightly larger.

ULT = {
    "dur":      8.0,   # the window. On the held-seconds line like everything
                       # else, so it is free and it is chosen for the picture
    "radius":   200.0, # THE MEASURED OPTIMUM AND THE ONE NUMBER THAT IS NOT
                       # FREE. 140 costs 2.7 points and 300 costs 4.0 AT THE
                       # SAME HELD SECONDS -- a hold is only worth what the
                       # hammer can reach. ~2.6x the warhammer's own reach of
                       # 76, or three ball diameters.
                       #
                       # NAMED `radius` AND NOT `rad`, WHICH IS THE OPPOSITE
                       # CALL FROM DEADFALL'S AND IS RIGHT FOR THE OPPOSITE
                       # REASON. `fireUlt` reads `u.radius` for its in-range
                       # test and the particle field reads it for its extent.
                       # Deadfall's mine trigger was NEITHER of those, so
                       # putting it there would have shrunk its own set-piece.
                       # This one IS the ultimate's reach: the field should be
                       # that wide and the cast's own `hit` flag should mean
                       # what it says.
    "cadence":  2.0,   # THE COOLDOWN, AND IT IS RICK'S OFF THE SECOND CLIP:
                       # "its still pretty confusing what the ult is actually
                       # doing by just watching it. can we add a cooldown for
                       # how often it can grab but make the stun longer?"
                       #
                       # IT SHIPPED AT 0.6 AND THE WHOLE ULTIMATE RESOLVED IN
                       # 4.8 SECONDS OF ITS OWN EIGHT-SECOND WINDOW. Five
                       # near-identical half-second events a mean 1.13s apart,
                       # and then a dead back third. Nothing was on screen long
                       # enough to be read as a cause.
                       #
                       # AND THIS IS THE TRADE THE DESIGN GIVES AWAY FOR FREE.
                       # `grab_lab` fitted lift = +3.1 + 2.62 x held with
                       # residuals SMALLER than the measurement error, so
                       # cadence, grab hold, true-stun length, window and grab
                       # count are five ways of writing one number: any
                       # arrangement delivering the same held seconds is worth
                       # the same. No other ultimate in this game has that
                       # property and nothing had ever spent it.
                       #
                       # A LONGER COOLDOWN DOES NOT COST GRABS, WHICH IS WHY
                       # `n` HAD TO COME DOWN WITH IT. The timer sits expired
                       # between grabs and closes the instant the quarry is in
                       # reach, so slowing it SPACES the grabs without losing
                       # many -- and the longer stun then multiplies. Every arm
                       # in `grasp_rhythm_lab.py`'s first round came back
                       # 20-60% above the shipped `held` for exactly that
                       # reason.
    "grabStun": 1.0,   # per grab. Writes `f.stun` DIRECTLY -- never
                       # `takeHitstun`, whose ceiling is 0.26s and whose
                       # `stunDR` would eat the second grab onward
    "n":        3,     # GRABS TO THE TRUE STUN. It shipped at 5 and came
                       # down with the cooldown, because at cadence 2.0 five
                       # grabs deliver half again the held seconds the balance
                       # is priced on -- and the point of the change is that
                       # `held` must NOT move.
                       #
                       # WHAT IT BUYS IS THE WHOLE COMPLAINT: grabs a cast
                       # 4.84 -> 2.83, the gap between them 1.13s -> 2.62s, and
                       # the ultimate now occupies 70% of its window against
                       # 61%. Three beats two and a half seconds apart, each
                       # locking the quarry for a full second, and the third
                       # one is the crush.
                       #
                       # AND IT IS STILL RICK'S 2-TO-6. `grab_lab` priced the
                       # count monotone across that range at ONE cadence; this
                       # is the same total hold arranged differently, which the
                       # held-seconds law says is worth the same. Measured:
                       # held a fight 9.53 -> 10.06, half a second, which is
                       # 1.4 points of win rate against a per-arm SE of 5.3.
    "squeeze":  0.30,  # HOW LONG THE FIST IS SHUT, AND IT IS NOT HOW LONG THE
                       # FOE IS STUNNED. Rick, watching the first build: "the
                       # hand currently reaches out and latches on and
                       # stretches with the balls movement. it should reach
                       # out. squeeze. cause massive hitstun. let go."
                       #
                       # THE FIRST BUILD DREW THE STUN. It held the hand ON the
                       # quarry for `grabStun` — 0.5s of the 0.6s cadence — so
                       # the limb was attached 83% of the time and stretched
                       # with whatever the ball did. That is a LATCH, and a
                       # latch says the ball is being held, which is the one
                       # thing this ultimate deliberately does not do (`f.pin`
                       # is refused, §4.5). The hand grips the WEAPON.
                       #
                       # So the squeeze is a MOMENT and the hitstun OUTLIVES
                       # it: reach, close, let go, draw back, reach again — a
                       # pump on the cadence — while the foe stays locked for
                       # the whole 0.5s. PRESENTATION ONLY. Nothing in the
                       # simulation reads it, `engine_ab` is identical across
                       # this change, and the `held` column does not move.
    "trueStun": 2.2,   # AND IT IS A REGISTERED TRUE-STUN SITE. Worth nothing
                       # BEYOND its seconds -- "grabs only, no true stun at
                       # all" is +22.9% at 6.2s held and n=6 is +26.2% at 7.0s,
                       # both on the line. The escalation earns its place as a
                       # rhythm and as a picture, not as a payload, so DO NOT
                       # lengthen it to buy value.
}
# "then dissipates", and it is Rick's own clause doing the balancing. Worth
# -10.8 points at n=4 and -13.7 at n=3: without it the ultimate is sixth of
# twenty-eight and the blade pays for it. It is also a rule a viewer can SEE
# happen rather than read.
END_ON_TRUE = True

ULT_NAME = "Grasp"
ULT_TIP = "Grabs repeatedly; the third grab is a true stun, then it fades"  # 62/72
BLURB = ("Bone under the iron, and it did not start there. What it takes hold "
         "of does not get to swing back.")


# ============================================================ STAGE 2 =======
S2 = [

# --------------------------------------------------------- 1. the 28th relic
("relic", '''    blurb:"A watch kept with a light. It does not chase — it turns, and the room walks into it." },

];''',
 '''    blurb:"A watch kept with a light. It does not chase — it turns, and the room walks into it." },

  /* SHROUDMAUL — THE UMBRAL WARHAMMER, and the cell where the grid's two
     thinnest lines crossed. Umbral was on 3 of 6 types and the warhammer on 3
     of 7 schools; this puts both on 4.

     EVERY PHYSICAL STAT IS THE WARHAMMER'S, copied off Grudgebearer, Censer
     and Bulwarden and not invented — weapon-matrix decision 1, the TYPE owns
     the physics and the SCHOOL owns status and palette. `SHAPES.warhammer`
     already routes `umbral` to `_whEaten`, so the silhouette is not new work:
     it exists, it is 78.6% distinct from its nearest sibling and it was the
     3rd most distinct of the fifteen open cells.

     `onHit:{ curse:1 }`, matching the school's other three. AND THE CELL
     CANNOT BE ARGUED ON THAT CHANNEL: curse pays between 13.8% and 18.6% of a
     fighter's damage whatever it is bolted to (v55 §4), so the echo is very
     nearly type-invariant. What the warhammer buys is a POOL 77% bigger than
     Nightfell's and 20% bigger than Gravemourn's — the warhammer's entries
     match the flail's within noise (35.2 against 35.9) while it lands 28% more
     of them — and the pool is read by ultimates and by nothing else.

     WHICH THIS ULTIMATE THEN DELIBERATELY DOES NOT READ. Twinshade FILLS the
     pool, Gravemourn MOVES an entry out and back, Nightfell READS the sum onto
     the floor; this one has no relationship to it at all, and that is a
     decision rather than an oversight. v52 §5 registered the school's real
     risk as "umbral becomes a school where nothing works until Curse is
     stacked — a relic that loses its first exchange loses its ultimate as
     well". This is the only umbral ultimate that is worth full value in the
     first ten seconds of a fight.

     `dmg` is the tuned knob (shroudmaul_build.TUNED_SM) and it starts at
     Grudgebearer's own 23.5. */
  { id:"shroudmaul", name:"Shroudmaul", aff:"umbral", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:%DMG%, spin:1.6, mode:"spin", mass:5.0, knockMul:2.3,
    onHit:{ curse:1 },
    /* GRASP. STUBBED AT `charge:1e9` IN STAGE 2, which is the same "OFF" the
       charge sweep in v55b used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else. Stage 3 brings the charge down to %CHARGE% and builds the window.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed. */
    ult:{ name:"%ULT%", charge:1e9, kind:"grip", dmg:0,
          dur:%DUR%, radius:%RADIUS%, cadence:%CADENCE%,
          grabStun:%GRABSTUN%, n:%N%, trueStun:%TRUESTUN%,
          tip:"%TIP%" },
    blurb:"%BLURB%" },

];'''),
]


# ============================================================ STAGE 3 =======
S3 = [

# ------------------------------------------------------- 1. the hand's home
("Fighter.ultGrasp", '''    this.deadfallFade = 0;''',
 '''    this.deadfallFade = 0;
    /* {t, dur, grabs, cd, grip, stunFor, crush, held} while GRASP's window is
       open. `grip` is how long the FIST is still shut and `stunFor` is what
       the last grab wrote to `foe.stun`; they are different numbers and the
       first build conflated them into one — see `ult.grip`. null on every other relic and on this one outside its own window,
       which is the whole zero-burden argument: `tickGrasp` returns after a
       two-iteration loop that does nothing, `drawGrip` returns on its first
       line, and nothing anywhere else in the engine reads this field.

       ONE HAND, and it is OWNED BY A FIGHTER. Not `m.shots`, whose `maxLive`
       ceiling makes `spawnShot` SHIFT THE OLDEST LIVE ENTRY OUT — a hand that
       vanished with no error and no invariant broken is this project's own
       defect class. Not `m.hands` either: those are Revenant's, there are many
       of them, they are airborne and they outlive the window that threw them.
       This one is a limb, there is exactly one, and it belongs to the arm it
       grew out of. */
    this.ultGrasp = null;
    /* AND THE CRUSH OUTLIVES THE WINDOW, WHICH IS THE WHOLE OF "THEN
       DISSIPATES" AS A PICTURE. The fifth grab ENDS the window on the frame it
       lands — that clause is worth -10.8 points and it is not negotiable — so
       the sim's `ultGrasp` is null from that instant. Drawn off `ultGrasp`
       alone, the payoff of an eight-second window would therefore be a hand
       DISAPPEARING at the exact moment it closed, and the 2.0 seconds the
       quarry spends held would have nothing on screen at all.

       `grasp_relic_probe [P]` caught this on the first build: 2692 rendered
       frames, 1225 reaching, 1201 holding and **ZERO of the crush**. Nothing
       else could have — every number was right, the true stun landed, the beat
       was filed, the win rate did not move by a thousandth. That is this
       project's own defect class and Rick's §1 names it directly: "a unique
       animation for the true stun grab".

       PRESENTATION ONLY, and `life` is in HALF-SECONDS like every other
       presentation clock in this engine, because `tickPresentation` is called
       once directly and once through `decayImpactOnly`. It is ticked THERE and
       not in `tickGrasp`, and that is v54's lesson stated one relic along:
       ANYTHING PRESENTATION THAT IS SPAWNED BY AN IMPACT BELONGS IN
       `tickPresentation`. The crush sets `hitStop`, so a clock on the normal
       step path would freeze for exactly the frames the viewer is staring
       hardest at — which is what Deadfall's blast did, 96.2% of the time. */
    this.graspCrush = null;
    /* {t, hold, crush} — A STUN THAT HAS BEEN EARNED AND HAS NOT LANDED YET.
       Rick: "can we have the hand squeeze and let go before the stun starts so
       we can see the enemy fighter stunned out of its grasp?"

       The grab used to write `foe.stun` on the frame the fist CLOSED, so the
       quarry was already reeling while it was still being held and the two
       events could not be told apart. Now the squeeze schedules the stun and
       the stun lands `ult.squeeze` later, on the frame the fist OPENS: caught,
       crushed, let go, and THEN left reeling with its weapon dead.

       IT IS ON THE FIGHTER AND NOT ON `ultGrasp`, because the crush closes the
       window on the frame it lands — "then dissipates" — and its stun is still
       owed for another 0.3s after that. It is the only piece of this ultimate
       that outlives its own window, and nulling it on death or on `m.over` is
       the reason `tickGrasp` opens by ticking it before anything else.

       TOTAL HELD SECONDS ARE UNCHANGED: the stun is the same length, it simply
       starts a third of a second later. */
    this.graspPend = null;
    /* AND THE LIMB'S OWN FADE, because the window closing is not the same
       event as the picture of it ending. Same shape as `deadfallFade` and
       `winnowFade`, one relic along. It is on the FIGHTER and not on
       `m.ultFx` for a MEASURED reason — see `drawGrip`. It is driven in
       `tickPresentation` beside `graspCrush`, for the same reason. */
    this.graspFade = 0;'''),

# -------------------------------------------------------------- 2. the cast
("fireUlt.grip", '''    if (u.kind === "sigil"){''',
 '''    if (u.kind === "grip"){
      /* NOTHING RESOLVES HERE, and `u.dmg` is 0. The cast grows a hand and
         opens a window; what the ultimate IS happens on the grabs inside it.

         NOT `freeze`. The engine already says why, three lines from where a
         second hold would have gone: "The Crucible owns freeze; a second hold
         would make two of the sixteen the same relic." Every other hold in
         this game is a SINGLE EVENT ATTACHED TO DAMAGE — the Crucible pulls
         the foe in and cashes it, Bramblesnare and Rootfast root and hit,
         the Harrowing stuns on its burst. This is a WINDOW of repeated,
         zero-damage grabs whose payoff has to be EARNED inside it. Different
         verb, different rhythm, and a completely different value curve.

         `cd` STARTS AT 0, so the hand can close on the frame the window
         opens if the quarry is already in reach. That is `grab_lab`'s own
         arm and every number in `06-docs/v56/grab-v56.md` is measured on it. */
      f.ultGrasp = { t: 0, dur: u.dur, grabs: 0, cd: 0,
                     grip: 0, stunFor: 0, crush: false, held: 0 };
      return;
    }

    if (u.kind === "sigil"){'''),

# ------------------------------------------- 3. the set-piece's own lifetime
("ultFx.life", '''              aureole: 1.6, censer: 1.6,''',
 '''              /* SHROUDMAUL IS A BURST AND NOTHING MORE, which is the whole
                 point of the entry. Every other window ultimate in this map
                 sets `life` from `ult.dur` at its own cast site so its art
                 survives its window — and all seven of them are still wrong,
                 because `ultFx` is ONE SLOT and the opponent casting anything
                 erases it (v54 §2a, open item 25). GRASP's window art is on
                 `f.ultGrasp` where nobody else can reach it, so this field
                 carries only the particle burst of the hand GROWING, and 1.8
                 is how long that takes. */
              shroudmaul: 1.8,
              aureole: 1.6, censer: 1.6,'''),

# ------------------------------------------------------ 4. the window, ticked
("tick.call", '''    this.tickDeadfall(dt);''',
 '''    this.tickDeadfall(dt);
    this.tickGrasp(dt);'''),

# ------------------------------------------------------ 5. THE WINDOW ITSELF
("tickGrasp", '''  tickSling(dt){''',
 '''  /* GRASP — ONE HAND, TETHERED, AND THE FIRST PAYOFF IN THIS GAME THAT HAS
     TO BE EARNED INSIDE ITS OWN WINDOW.

     Rick's §1: "for a duration the artifact grows an etherial skeletal hand
     that reaches out and grabs nearby enemies. the grab does no damage and
     doesn't apply curse but it does apply massive hit stun. if it grabs
     several times in one trigger it true stuns for extra duration and then
     dissipates."

     ── IT NEVER RUNS DURING A HIT STOP, AND THAT IS STRUCTURAL ─────────────

     `step()` returns through `decayImpactOnly` for as long as `hitStop` runs,
     and every tick in this block sits below that return. So the hand is frozen
     with the rest of the world and there is no guard here to get wrong.
     `grab_lab` skipped its own hit-stop frames explicitly to model exactly
     this, which is why the numbers transfer.

     ── THE GRABS WRITE `f.stun` DIRECTLY, AND THAT IS THE WHOLE MECHANIC ───

     NEVER `takeHitstun`. That function caps at `stunMax` 0.26s and divides
     each application by `1 + stunDR * 0.55`, so routing five grabs through it
     turns them into one grab and a rumour — with every invariant intact, no
     probe failing, and the only symptom a `held` column that does not move
     when the knobs do. It is also why "massive hit stun" in the §1 could never
     have been `takeHitstun`: nothing routed through it can be massive.

     `u.freeze` is the precedent and this is written the same way it is.

     ── AND `f.pin` IS NEVER WRITTEN. MEASURED, NOT ASSUMED ─────────────────

     Holding the BALL as well as the weapon is **-3.3 points at identical held
     seconds**, consistent with the reach result: a pinned ball cannot be
     knocked toward the wielder, and this relic needs the quarry to arrive.
     `f.pin` is the Stasis Field's only exclusive verb in the whole game.

     So the hand grips the WEAPON and lets the ball drift — which is both the
     cheaper build and the better one, and it is what the frame shows.

     ── FOE ONLY, AND THE RULE IS STRUCTURAL RATHER THAN A GUARD ────────────

     "grabs nearby enemies" is plural in a 1v1 game — except against
     Triplicate, where there are three bodies for six seconds. THE HAND DOES
     NOT GRAB SHADES: the loop below reads `this.a` and `this.b` and nothing
     else, so there is no `if` to get wrong and `tickShadeHits` is never
     involved. The reason is that a grab spent on a copy that is about to
     expire is a grab spent on nothing — the shade cannot swing at the wielder
     after the window closes, and the counter toward the crush would be paid
     with it. This is also the arm `grab_lab` priced.

     ── THE COUNTER, AND "THEN DISSIPATES" ──────────────────────────────────

     Every grab is one closing of the hand. The `n`th is THE CRUSH: it holds
     for `trueStun` instead of `grabStun`, it is a REGISTERED TRUE-STUN SITE
     (see `breakSpin`), and the window ends on it. That last clause is worth
     -10.8 points and it is Rick's own sentence doing the balancing. */
  tickGrasp(dt){
    for (const f of [this.a, this.b]){
      const u = f.w.ult;
      const foe = f === this.a ? this.b : this.a;
      /* ---- THE STUN THAT WAS EARNED A THIRD OF A SECOND AGO --------------
         ABOVE the window guard, and that is load-bearing: the crush closes the
         window on the frame it lands and still owes its 2.2s. Rick's "squeeze
         and let go BEFORE the stun starts" is this whole block. */
      if (f.graspPend){
        const P = f.graspPend;
        P.t -= dt;
        if (P.t <= 0){
          f.graspPend = null;
          /* THE PAYOFF FIRES; ONLY THE STUN IS CONDITIONAL. The quarry can die
             to an ordinary hammer blow inside the third of a second between
             the fist closing and opening -- measured at 3 of 231 crushes -- and
             a true stun on a corpse is nonsense. But the crush HAPPENED: the
             fist closed, the art played, and a viewer watched it. The first cut
             of the delay guarded the whole block on `foe.alive` and silently
             dropped the beat and the biggest voice on the relic along with the
             stun, which is `cinePlan` being told the most distinctive moment in
             the fight did not occur. */
          if (!this.over && f.alive){
            if (foe.alive) foe.stun = Math.max(foe.stun, P.hold);
            if (P.crush){
              /* THE TRUE-STUN SITE IS STILL ONE AND STILL THE LAST GRAB —
                 it has moved to the frame the hand lets go, which is where a
                 viewer can see it happen. Guarded on the quarry being alive
                 for the same reason the stun above is. */
              if (foe.alive)
                this.breakSpin(foe, "the hand closes and it does not open",
                               u.trueStun);
              this.hitStop = Math.max(this.hitStop, 0.09);
              this.shake = Math.min(38, this.shake + 20);
              this.ring(foe.x, foe.y, AFFINITIES.umbral.glow, 7, 130, 0.45, 6);
              SFX.play("ult", { w: "shroudmaul-crush" });
              this.note(`${f.w.name} — the last grab`);
              /* RULE 3, NINTH RELIC RUNNING. See the cast's own note below:
                 a zero-damage ultimate can file nothing through `resolveHit`,
                 so this is one of exactly two beats it ever files. */
              this.beat({ kind: "ult", side: f === this.a ? 0 : 1,
                          x: foe.x, y: foe.y, w: f.w.id,
                          foeHpFrac: foe.hp / foe.maxHp });
            }
          }
        }
      }
      /* THE LIMB'S PICTURE IS NOT DRIVEN HERE. `graspCrush` and `graspFade`
         both live on the presentation clock — see `tickPresentation`, and see
         the field's own comment in the Fighter constructor for why. */
      const G = f.ultGrasp;
      if (!G) continue;
      G.t += dt;
      /* THE FIST, counted down for the picture, and it is NOT the stun. The
         stun is the foe's and is ticked by `tickStatus` like every other stun
         in the game; this is how long the hand is still shut, which is a
         quarter of it. Two clocks for one event is a drift hazard, so this
         one is deliberately presentation: nothing reads it but `drawGrip`. */
      G.grip = Math.max(0, G.grip - dt);

      /* THREE WAYS OUT AND ALL THREE ARE HERE: the clock, the corpse and the
         end of the match. Nothing is restored, because the window writes
         nothing to the fighter — unlike Revenant's, which has a `reachMul` to
         put back. A hand in flight at the end is not possible: there is only
         one, it is attached, and it goes with the window. */
      if (G.t >= G.dur || !f.alive || !foe.alive || this.over){
        f.ultGrasp = null;
        /* A STUN OWED TO A CORPSE IS NOT OWED. The pending block above refuses
           to write it anyway; this stops the object outliving the fight. */
        if (!f.alive || !foe.alive || this.over) f.graspPend = null;
        continue;
      }

      G.cd -= dt;
      if (G.cd > 0) continue;
      /* OUT OF REACH IS NOT A MISSED GRAB. The cadence timer is already
         expired and simply stays expired, so the hand closes the instant the
         quarry comes inside `radius` rather than on the next multiple of
         0.6s. That is `grab_lab`'s arm exactly and it is the difference
         between a hand that is WAITING and a hand on a metronome. */
      const d = Math.hypot(foe.x - f.x, foe.y - f.y);
      if (d > u.radius) continue;

      G.grabs++;
      G.cd = u.cadence;
      const crush = G.grabs >= u.n;
      const hold = crush ? u.trueStun : u.grabStun;
      /* THE ONE WRITE. `Math.max` and not assignment, so a grab can never
         SHORTEN a hold the foe is already under — the same shape `u.freeze`,
         hex and the Harrowing all use. NO DAMAGE, NO `apply`, NO `pushCurse`,
         NO `f.pin`: all four were considered and all four were ruled out, and
         the pool is measured to be unmoved by the whole ultimate (+1.2 blows
         and +5.4% of pool). */
      /* SCHEDULED, NOT APPLIED. `ult.squeeze` from now, which is the frame
         the fist opens — see `f.graspPend`. `Math.max` still guards the write
         itself when it lands, so a grab can never SHORTEN a hold the quarry is
         already under. */
      f.graspPend = { t: u.squeeze, hold, crush };
      /* ---- AND THE SQUEEZE STOPS THE BALL DEAD -------------------------

         Rick, watching the third build: "im not seeing the hand apply any
         hitstun at all?" and then "hitstun should freeze the enemy ball
         correct?"

         IT DOES NOT, AND THAT IS WHY HE COULD NOT SEE IT. `f.stun` locks the
         WEAPON -- `tickHits` skips, the head stops turning, the swing does not
         advance -- and the ball keeps moving: `moveMul` floors at 0.45 and
         `speedMin` is 250. Measured on the shipped relic, the quarry was
         stunned 54% of the open window and its ball was travelling **674 px/s
         while stunned against 599 free**, which is 12% FASTER. The most
         visually distinctive thing in the fight was landing on a target that
         then sailed away at speed.

         THE DESIGN PREDICTED THIS COMPLAINT AND BET AGAINST IT. `grab-v56.md`
         §5, in its own words: "a skeletal hand closing around a ball that then
         keeps drifting is not obviously legible. The answer is that the hand
         grips the WEAPON, not the ball." That was an argument, and a person
         watching refuted it.

         SO THE PIN IS THE SQUEEZE'S LENGTH AND NOT THE STUN'S, WHICH IS THE
         WHOLE OF THE COMPROMISE. `grab_lab` priced a FULL pin -- the ball held
         for the entire `grabStun` -- at **-3.3 points against stun alone at
         identical held seconds**, because a pinned ball cannot be knocked
         toward the wielder and this relic needs the quarry to arrive. It also
         held the ball for 39% of the window, which is the Stasis Field's verb
         and the thing the engine's own comment forbids a second relic from
         having ("a second hold would make two of the sixteen the same relic").

         `u.squeeze` is 0.30s and holds the ball for **13% of the window**, in
         three pulses. It is the frames the fist is actually shut and not one
         more: the hand closes, the ball stops, the hand opens, the ball goes
         on with its weapon still locked for the rest of the second. That is
         Rick's own sentence -- "reach out. squeeze. cause massive hitstun. let
         go." -- with the squeeze finally doing something a viewer can see.

         THE RESUME IS PARADOX'S, CHARACTER FOR CHARACTER. `move()` returns on
         `pin`, `pinV` is what it resumes with, and `pinrelease_build.py
         --mode clamp` then refuses to release a ball UPWARD, because a stored
         upward velocity goes stale the instant the hold starts. At 0.30s that
         clamp is a small distortion rather than Paradox's 2.3s one, but it is
         a REAL one and not just a picture: a ball caught rising comes out at
         rest. Named because it is the only part of this that is not
         presentation. */
      foe.pin = Math.max(foe.pin, u.squeeze);
      foe.pinMax = Math.max(foe.pinMax, u.squeeze);
      if (!(foe.pin > u.squeeze)) foe.pinV = [foe.vx, foe.vy];
      /* THE SQUEEZE IS A MOMENT AND THE HITSTUN OUTLIVES IT. `grip` is the
         fist; `stunFor` is what was written to the quarry, and it is four
         times longer. The crush squeezes twice as long and lets go the same
         way — Rick's "reach out. squeeze. cause massive hitstun. let go." */
      G.grip = crush ? u.squeeze * 2 : u.squeeze;
      G.stunFor = hold; G.crush = crush;
      G.held += hold;
      this.spawnFx(foe.x, foe.y, AFFINITIES.umbral.core,
                   crush ? 26 : 9, crush ? 260 : 150, crush ? 0.6 : 0.3, 4);
      if (!crush){
        /* AN ORDINARY GRAB FILES NO BEAT. "Do not let small hits drive the
           camera" — `_cineVine`'s rule exactly, and there are up to four of
           these a cast. It gets a shake and no hit stop: a freeze on a 0.6s
           cadence would stutter the fight rather than punctuate it. */
        this.shake = Math.min(38, this.shake + 6);
        SFX.play("ult", { w: "shroudmaul-grab" });
        continue;
      }

      /* ---- THE CRUSH -----------------------------------------------------

         A REGISTERED TRUE-STUN SITE, and the fourth in the game. `breakSpin`
         is the single hook all of them already call, and passing `trueFor`
         is what marks this one as a stun that CANCELS a wind-up rather than
         delaying it. The four ordinary grabs above deliberately do not call
         it. Rick's own rule: "Hitstun shouldnt stop the windup. but true
         stuns from ults/abilities should."

         IT LANDS LIKE SOMETHING. This ultimate deals no damage, so there is
         no number, no health bar moving and no hit stop scaled to a blow —
         which means the crush has to be given the weight a killing blow gets
         for free, or the payoff of an eight-second window is a ball going
         quiet. */
      /* THE CRUSH'S STUN, ITS BEAT AND ITS VOICE ALL LAND WHEN THE FIST
         OPENS, not here — see `f.graspPend` at the top of this function. What
         is left on this frame is the picture of the fist closing. */
      /* AND THE PICTURE OF IT OUTLIVES THE WINDOW. `ultGrasp` is nulled four
         lines down — that is "then dissipates" and it is the balance clause —
         so without this the hand would VANISH on the frame it closed and the
         squeeze that ended the window would have no frames at all.

         IT DOES NOT LAST `trueStun`, AND THAT IS RICK'S CORRECTION. The first
         build held the hand on the quarry for the whole 2.0s, which drew the
         STUN rather than the grip. This is the squeeze and the letting go —
         `squeeze * 2` shut, then `squeeze * 1.8` opening — and the quarry stays
         locked for the remaining second and a half with nothing on it but its
         own stopped weapon. Presentation only, in half-seconds. */
      f.graspCrush = { t: 0, grip: u.squeeze * 2 * 2,
                       life: (u.squeeze * 2 + u.squeeze * 1.8) * 2 };

      /* RULE 3, NINTH RELIC RUNNING, AND THIS ONE IS THE WORST PLACED YET.
         `cinePlan` scores an ultimate off the beats filed for it, and a
         zero-damage ultimate can file NOTHING through `resolveHit` — there
         is no blow. So the two beats this relic files are the cast (through
         `fireUlt`'s own generic beat, which every relic gets) and this one.

         AND THERE IS NO FATAL BEAT TO FILE, EVER. v53 §4 is the precedent —
         30 of Gravemourn's 58 kills rendered a clip with no killing blow
         because a hand filed `kind:"ult"` and `cinema_clip` finds the finish
         with `plan.find(c => c.fatal)`. That fix does not apply here and
         cannot: a grab deals no damage, so it can never be the killing blow.
         The relic's kills are all ordinary hammer blows through `resolveHit`,
         which already file fatal beats. `grasp_relic_probe [10]` asserts the
         beat, and [5] asserts there is nothing to be fatal about. */
      /* AND THEN IT DISSIPATES. Rick's own clause, and it is the balance knob
         rather than a cost: without it the ultimate is +31.2% instead of
         +20.4%, sixth of twenty-eight, and the blade would have to be cut
         hard to pay for it. It is also a rule a viewer can watch happen. */
      f.ultGrasp = null;
    }
  }

  tickSling(dt){'''),

# ------------------------------------- 6. the true-stun register grows to four
("truestun.list", '''     instead of by reading a timer, and there are exactly three of them:

         hex          STATUS.hex.stunFor      Spellbreaker, Axiom
         ult freeze   u.freeze                Thornwake, Rootfast
         the Harrowing's burst  u.stunBase    Lastlight

     Five relics of twenty, and the counter is therefore NAMEABLE -- a viewer
     can learn who shuts this down, which a stun budget could never have
     offered.''',
 '''     instead of by reading a timer, and there are exactly four of them:

         hex          STATUS.hex.stunFor      Spellbreaker, Axiom
         ult freeze   u.freeze                Thornwake, Rootfast
         the Harrowing's burst  u.stunBase    Lastlight
         GRASP'S LAST GRAB      u.trueStun    Shroudmaul

     Six relics of twenty-eight, and the counter is therefore NAMEABLE -- a
     viewer can learn who shuts this down, which a stun budget could never have
     offered.

     AND ONLY THE LAST GRAB IS ON THAT LIST. Shroudmaul closes its hand up to
     `n` times a window and every grab but the last DELAYS a wind-up exactly as
     ordinary hitstun does. The escalation is therefore legible in the one
     place a viewer can read it: grabs that hold, and a final one that takes
     the cast away. Adding the whole window to this list would have made every grab a
     cancellation and quietly turned a rhythm into a lockout.''')
,

# ---------------------------------- 6b. THE LIMB IS ON THE PRESENTATION CLOCK
# v54's lesson, stated one relic along: ANYTHING PRESENTATION THAT IS SPAWNED
# BY AN IMPACT BELONGS IN `tickPresentation`, NOT IN A TICK. The crush sets
# `hitStop`, and `step()` returns through `decayImpactOnly` for as long as that
# runs -- so a clock on the normal path freezes for exactly the frames the
# viewer is staring hardest at. Deadfall's blast did that 96.2% of the time,
# worst 31.67 SECONDS against a 0.42s life, and the engine had already written
# the warning three lines away.
("tickPresentation.grasp", '''  tickPresentation(dt){
    if (this.ultFx){''',
 '''  tickPresentation(dt){
    /* GRASP'S LIMB, AND BOTH HALVES OF IT ARE HERE FOR THE REASON THE
       PARAGRAPH BELOW ALREADY GIVES FOR STATUS TAGS AND THE DEADFALL'S BLAST:
       the crush is an IMPACT, every impact begins with a hit stop, and a hit
       stop runs `decayImpactOnly`.

       `life` IS IN HALF-SECONDS, like every other `life` in this engine: this
       clock is called once directly and once through `decayImpactOnly`, so it
       runs at 2x sim time. `graspCrush.life` is therefore `trueStun * 2` and
       the fade's 0.7 is 0.35 seconds.

       AND THE FADE IS DRIVEN OFF BOTH, which is what makes "then dissipates"
       read: the hand is solid while the window is open, still solid through
       the two seconds of the crush, and only then lets go. */
    for (const f of [this.a, this.b]){
      if (f.graspCrush){
        f.graspCrush.t += dt;
        if (f.graspCrush.t >= f.graspCrush.life) f.graspCrush = null;
      }
      f.graspFade = (f.ultGrasp || f.graspCrush) ? 1
                  : Math.max(0, f.graspFade - dt / 0.7);
    }
    if (this.ultFx){'''),

# ------------------------------------------------------------ 7. three voices
("sfx", '''        } else if (w === "nightfell-stamp"){    // a figure hits the floor''',
 '''        } else if (w === "shroudmaul"){         // an arm comes out of the iron
          /* THE CAST IS A WINDOW OPENING, so like Revenant's and Deadfall's it
             does not resolve — nothing has happened yet. This is a GROWTH: a
             low woody rise with the dry clatter of bone assembling over it,
             and it deliberately does not land on a beat, because the hand is
             still reaching when the sound ends. */
          this._tone (t, { freq: 52, to: 104, gain: 0.28, dur: 1.05, type:"sawtooth" });
          this._tone (t + 0.05, { freq: 138, to: 260, gain: 0.13, dur: 0.85, type:"triangle" });
          [0, 0.08, 0.15, 0.23, 0.32, 0.42].forEach((d, i) =>
            this._burst(t + d, { freq: 900 + i * 340, q: 2.2,
                                 gain: 0.10 - i * 0.012, dur: 0.05,
                                 type:"bandpass" }));
          this._burst(t + 0.30, { freq: 600, q: 0.6, gain: 0.09, dur: 0.55, type:"lowpass" });
        } else if (w === "shroudmaul-grab"){    // and it closes on something
          /* FOUR OF THESE A CAST, so it is quiet by design and short by
             design. A dry CLAMP — a wooden knock with a tight band over it —
             and it is deliberately much smaller than the crush, because the
             one thing a viewer has to learn from this ultimate is which of
             the two just happened. Vesper's pass-against-tip pair is the
             precedent and it is the same problem. */
          this._burst(t, { freq: 520, q: 1.4, gain: 0.15, dur: 0.07, type:"bandpass" });
          this._tone (t, { freq: 210, to: 120, gain: 0.13, dur: 0.11, type:"triangle" });
          this._burst(t + 0.02, { freq: 1900, q: 1.8, gain: 0.07, dur: 0.04, type:"bandpass" });
        } else if (w === "shroudmaul-crush"){   // the fifth, and it is the last
          /* THE PAYOFF, AND IT HAS TO CARRY THE WHOLE ULTIMATE. There is no
             damage number on screen, no health bar moving and no hit-stop
             scaled to a blow, so this voice IS the event — the same argument
             that made Deadfall's blast bigger, arriving from the other side.

             A bone crack on top of a low collapse, then the tether letting
             go. It is the only voice on this relic allowed to be big.

             NO BURST IS LONGER THAN 0.6s. CLAUDE.md §4.5: `_burst` does not
             loop its 0.6s noise buffer, so anything longer plays silence for
             its tail. */
          this._tone (t, { freq: 160, to: 34, gain: 0.38, dur: 0.58, type:"sine" });
          this._burst(t, { freq: 190, q: 0.5, gain: 0.34, dur: 0.50, type:"lowpass" });
          this._burst(t, { freq: 3400, q: 1.2, gain: 0.24, dur: 0.06, type:"bandpass" });
          this._tone (t + 0.01, { freq: 430, to: 90, gain: 0.20, dur: 0.30, type:"sawtooth" });
          [0.06, 0.13, 0.21].forEach((d, i) =>
            this._burst(t + d, { freq: 1500 - i * 380, q: 1.6,
                                 gain: 0.12 - i * 0.03, dur: 0.08,
                                 type:"bandpass" }));
          this._burst(t + 0.26, { freq: 380, q: 0.5, gain: 0.14, dur: 0.50, type:"lowpass" });
        } else if (w === "nightfell-stamp"){    // a figure hits the floor'''),

# ------------------------------------------------- 8. the limb, drawn twice
("draw.under", '''    this.drawCrackle(m, false);''',
 '''    this.drawCrackle(m, false);
    this.drawGrip(m, false);'''),

("draw.over", '''    this.drawCrackle(m, true);''',
 '''    this.drawCrackle(m, true);
    this.drawGrip(m, true);'''),

("drawGrip", '''  drawShots(m){''',
 '''  /* ==== GRASP: ONE HAND, LARGE, AND TETHERED TO THE ARTIFACT ============

     THIS ULTIMATE DEALS NO DAMAGE. There is no number over the ball, no health
     bar moving, no hit stop scaled to a blow. **If the hand does not read,
     nothing happened** — which makes this the one set-piece in the game whose
     art is not decoration on a mechanic but the only evidence of it.

     ── IT IS READ OFF THE FIGHTER, AND `m.ultFx` COULD NOT CARRY IT ────────

     v54 §2a, measured on Deadfall: `ultFx` is ONE SLOT on the match, the
     opponent casting anything at all overwrites it, and that cast's own
     shorter `life` then nulls it. Counting frames in which the window was
     open, Deadfall's art survived 0.0% of them against Ironhail and 20.8%
     against Bulwarden. Nothing in this repo can see that — the sim is
     untouched, every probe is green and the win rate does not move by a
     thousandth. So this hangs off `f.ultGrasp` and `f.graspFade`, which belong
     to the fighter.

     ONE FUNCTION, DRAWN TWICE. `over` false is the ground the hand is reaching
     across, under both balls; `over` true is the limb itself, above them. Same
     shape as `drawVines(m, false/true)` and `drawCrackle(m, false/true)`, and
     for the same reason: the two halves are one effect and splitting them into
     two methods is how they drift apart.

     ── THE COLLISION, NAMED BEFORE ANYTHING WAS DRAWN ─────────────────────

     Gravemourn's Revenant is ALREADY made of ethereal hands in this school and
     they are not placeholder art — Rick rejected the first cut ("the hands
     dont read as hands") and the shipped version is deliberately legible as a
     hand at 37px on a 540 frame. Two umbral relics whose signature object is a
     hand will read as the same ultimate on a phone unless the difference is
     STRUCTURAL. It is, four ways at once:

       REVENANT   MANY hands, SMALL, AIRBORNE, thrown off blows, converging at
                  2500px/s and closing into fists. 1.8s of flight each
       GRASP      ONE hand, LARGE, TETHERED — it grows FROM the artifact and
                  stays attached for the whole window. It reaches, opens,
                  closes, HOLDS

     THE TETHER IS THE STRONGEST OF THE FOUR AND IT IS FREE: nothing else in
     the game connects the wielder to the quarry with a limb, and it is on
     screen for eight seconds rather than 1.8. This is v52 §4's problem — two
     ultimates in one school marking the same ground — and it gets the same
     treatment: an art constraint written down before either is drawn again.

     THE BONES ARE SHARED AND THE SCALE IS NOT. `_boneParts`, `_boneStroke` and
     `_drawBones` are Revenant's, because a skeleton drawn twice by two
     functions is a skeleton that drifts. What is not shared is `GRIP_SCALE`:
     Rick settled Revenant's at 0.7 over three rounds, and every one of those
     rounds was about a hand that was one of THREE in flight. This is one, it
     is attached, and it is meant to be the largest object in the frame.

     ── THREE STATES, AND TWO OF THEM ARE ONE FRAME APART ──────────────────

       REACHING   open, extending, tether slack. Most of the eight seconds
       HOLDING    closed on the WEAPON, taut, tether drawn tight. 0.5s x 4
       THE CRUSH  the fifth. 2.0s, bigger, and the hand is gone after it

     v54 §2c is the precedent and it nearly shipped broken: Deadfall's ARMING
     and ARMED states were separated by alpha alone at 0.16, against a hall
     that ALREADY had a gold pentagram on its floor, and photographed off a
     real match they did not separate at all. So these three are separated
     FOUR ways — the clench, the scale, the tether's tension and the colour —
     because any one of them can be lost to a phone screen, to the bloom, or
     to a dark frame.

     ── AND THE COUNT IS ON THE TETHER, WHICH IS A DECISION ────────────────

     `u.n` pips are drawn along the arm and `G.grabs` of them are lit. A viewer
     should be able to tell the fourth grab from the fifth BEFORE the fifth
     lands, or the payoff arrives without having been promised. Nothing
     measures this and nothing can; it is Rick's, and it is open decision 3.

     ── WHAT IS DELIBERATELY NOT HERE ──────────────────────────────────────

     A wash, a disc, or anything with AREA. CLAUDE.md §4.1c: alpha is invisible
     to the bloom and REACH is not, and this school has already blown the chain
     out once. The reach ring under the hand is a thin stroke for exactly that
     reason, and the ground pool is DARK — it takes light out of the frame
     rather than adding it.

     EVERYTHING IS A PURE FUNCTION OF SIM STATE. No `rng()`: the renderer may
     not consume the simulation's randomness, and a field advanced by a
     per-frame delta would judder in the app and differ from the capture. */
  drawGrip(m, over){
    for (const f of [m.a, m.b]){
      const fade = f.graspFade;
      if (!(fade > 0.01)) continue;
      const c = this.ctx, A = f.aff, R = CONFIG.physics.ballR;
      const G = f.ultGrasp, u = f.w.ult;
      const foe = f === m.a ? m.b : m.a;

      /* ---- THE GEOMETRY, AND IT IS ALL DERIVED --------------------------
         The hand lies along the line to the quarry. HOLDING, it is ON the
         quarry — it has hold of the weapon, and the ball keeps drifting under
         it, which is `f.stun` and not `f.pin` showing up in the picture.
         REACHING, it is part way out, and it extends further as the cadence
         timer runs down: the hand WINDS UP toward its next grab, so the
         viewer is told a grab is coming before it lands. */
      const C = f.graspCrush;
      const crush = !!C;
      const dx = foe.x - f.x, dy = foe.y - f.y;
      const dist = Math.hypot(dx, dy) || 1;
      const ang = Math.atan2(dy, dx);

      /* ---- REACH, SQUEEZE, LET GO --------------------------------------
         Rick, watching the first build: "the hand currently reaches out and
         latches on and stretches with the balls movement. it should reach
         out. squeeze. cause massive hitstun. let go."

         THE FIRST BUILD DREW THE STUN INSTEAD OF THE GRIP. It put the hand on
         the quarry for `grabStun` — 0.5s of a 0.6s cadence — so the limb was
         attached 83% of the time and stretched with whatever the ball did.
         **A latch says the ball is being held**, and the ball is not: `f.pin`
         is refused on measurement (§4.5) and the hand grips the WEAPON. The
         picture was contradicting the one thing the mechanic is careful about.

         So the gesture is a PUMP on the cadence, and the hitstun outlives it:

           SQUEEZE   `G.grip` — the fist is shut, at the quarry, tether taut
           LET GO    it opens and withdraws over `squeeze * 0.9`
           REACH     it extends again as the cadence timer runs down

         `ext` is how far out along the line the hand is, 0 at the shell and 1
         at the quarry. `shut` is the clench — `_boneParts` curls the phalanges
         off that one number, so the fist is the same geometry as the open hand
         and cannot drift from it. */
      const sqT = u.squeeze, relT = u.squeeze * 0.9;
      let ext, shut;
      if (crush){
        /* THE CRUSH SQUEEZES TWICE AS LONG AND LETS GO THE SAME WAY. `C.t` is
           on the presentation clock, so `C.grip` and `C.life` are in
           half-seconds like every other `life` in this engine. */
        const k = C.t <= C.grip ? 0
                : clamp((C.t - C.grip) / Math.max(1e-6, C.life - C.grip), 0, 1);
        ext  = 1 - 0.70 * k;
        shut = 1 - 0.80 * k;
      } else if (G && G.grip > 0){
        ext = 1; shut = 1;
      } else {
        const since = G ? u.cadence - G.cd : 99;
        if (G && G.grabs > 0 && since >= sqT && since < sqT + relT){
          const k = (since - sqT) / relT;             // opening and pulling back
          ext  = 1 - 0.70 * k;
          shut = 1 - 0.82 * k;
        } else {
          /* REACHING. It extends as the next grab approaches, so the viewer is
             told a grab is coming before it lands — and out of range the
             cadence timer sits expired, which leaves the hand at full stretch
             casting about, which is exactly what it is doing. */
          const w = G ? 1 - clamp(G.cd / u.cadence, 0, 1) : 1;
          ext  = 0.30 + 0.62 * w;
          shut = 0.08 + 0.16 * w;
        }
      }
      const held = ext > 0.92;                    // the tether is taut
      const out = Math.min(dist, u.radius * 1.05) * ext;
      const hx = f.x + Math.cos(ang) * out;
      const hy = f.y + Math.sin(ang) * out;
      const HR = (13 + 5 * (1 - shut)) * GRIP_SCALE * (crush ? 1.22 : 1);
      /* AND THE FOURTH SEPARATION IS COLOUR, WHICH THE FIRST SHEET SAID WAS
         MISSING. The comment above claimed four ways of telling the crush from
         a hold and only three were built: clench, scale and tether tension.
         Photographed side by side, the crush and an ordinary hold were the
         same picture at a slightly different size.

         THE BONE GOES WHITE-HOT AND NOTHING ELSE CHANGES. §4.1c is the reason
         this is safe where it was not for Daybreak or the Harrowing: ALPHA is
         invisible to the bloom and REACH is not, so what blows the chain out
         is AREA. A skeleton is separated strokes -- the same argument that let
         Deadfall's crackle be the brightest thing on its caster. */
      const P = crush ? { core: A.glow, glow: "#FFF2FF", dark: A.dark }
                      : A;

      if (!over){
        /* THE GROUND. A DARK pool under the wielder — WHICH MATTERS MORE
           NOW THAN IT DID, because with the arm gone this and the reach ring
           are the only things on screen saying WHOSE hand that is — and a thin
           ring at `radius`,
           which is the one number in this ultimate that is not free. The ring
           teaches the mechanic — inside it you are caught — and it is a
           stroke rather than a fill for §4.1c's reason. */
        c.save();
        c.globalAlpha = 0.55 * fade;
        const g = c.createRadialGradient(f.x, f.y, R * 0.5, f.x, f.y, R * 2.6);
        g.addColorStop(0, "#1B0630AA"); g.addColorStop(1, "#1B063000");
        c.fillStyle = g;
        c.beginPath(); c.arc(f.x, f.y, R * 2.6, 0, TAU); c.fill();
        c.globalAlpha = fade * (held ? 0.30 : 0.17);
        c.strokeStyle = A.core;
        c.lineWidth = held ? 2.0 : 1.2;
        c.beginPath(); c.arc(f.x, f.y, u.radius, 0, TAU); c.stroke();
        c.restore();
        continue;
      }

      /* ---- NO ARM. THE HAND FLOATS. -------------------------------------
         Rick: "can we drop the arm and just have the hand float out and grab?"

         THE TETHER WAS THE DESIGN'S OWN STRONGEST ARGUMENT AND IT WAS WRONG.
         `grab-v56.md` §7b picked it out of four candidate separations from
         Revenant's hands — one against many, tethered against airborne, bone
         against smoke, reaching against striking — and called it "the
         strongest of the four and it is free: nothing else in the game
         connects the wielder to the quarry with a limb". Three of those four
         still hold. The fourth is gone, and the separation survives on the
         other three: ONE hand, LARGE, and it opens and closes rather than
         flying through and punching.

         What the arm actually cost was the read. A limb from the shell to the
         quarry draws a bright line straight through the middle of the fight,
         and at 2.8x scale it was the largest object on screen for the whole
         window — so the eye followed the LINE and not the hand at the end of
         it. Nothing measures that; Rick watched it. */


      /* ---- THE HAND -----------------------------------------------------
         `_boneParts` from the CARPALS on: the forearm it opens with is the
         tether's job here, and drawing it twice would put a second elbow in
         the middle of the limb. */
      const parts = this._boneParts(HR, shut).slice(2);
      c.save();
      c.globalAlpha = fade;
      c.translate(hx, hy);
      c.rotate(ang);
      this._handEmbers(c, HR, shut, P, crush ? 12 : 6, 2.2);
      this._drawBones(c, parts, HR, P, crush ? 1.6 : 1.0);
      /* ---- THE COUNT, AND IT RODE THE ARM UNTIL THERE WAS NO ARM ---------
         `u.n` marks, `G.grabs` of them lit, so the last grab is PROMISED
         rather than merely delivered (§7b). They were rungs across the tether;
         with the tether gone they are studs across the back of the hand, which
         is better placed anyway — they are now ON the object the eye is
         already following instead of on the line leading to it.

         HOT WHITE AGAINST THE BONE, and an unlit one is a DARK BAR rather than
         an absence. The first cut of the count drew lit dots in `pal.glow`,
         the colour the bone beside them is drawn in, and photographed off a
         real match they were invisible: a bright mark on a bright thing reads
         as a thicker thing. */
      c.lineCap = "round";
      for (let i = 0; i < u.n; i++){
        const lit = i < (G ? G.grabs : u.n);
        const y = (i - (u.n - 1) / 2) * HR * 0.31;
        c.globalCompositeOperation = lit ? "lighter" : "source-over";
        c.globalAlpha = fade * (lit ? 1 : 0.8);
        c.strokeStyle = lit ? "#FFF2FF" : A.dark;
        c.lineWidth = HR * (lit ? 0.11 : 0.085);
        c.shadowColor = A.core; c.shadowBlur = lit ? 12 : 0;
        c.beginPath();
        c.moveTo(-HR * 0.50, y); c.lineTo(-HR * 0.06, y);
        c.stroke();
      }
      c.restore();
    }
  }

  drawShots(m){'''),

# ------------------------------------------------------------ 9. the scale
("GRIP_SCALE", '''const WEAPON_BY_ID = Object.fromEntries(WEAPONS.map(w => [w.id, w]));''',
 '''/* GRASP'S HAND IS THE LARGEST OBJECT THIS GAME DRAWS, AND THAT IS THE POINT.

   Revenant's hands are `_handScale`, which Rick settled at 0.7 over three
   rounds — and every one of those rounds was about a hand that was one of
   THREE in flight at once ("the hands are a bit large. they look a little
   comical"). This is ONE hand, it is attached to the fighter that grew it, and
   it has to carry an ultimate that puts no number on the screen at all.

   1.35 WAS THE FIRST CUT AND IT WAS REFUTED BY THE FIRST SHEET. Photographed
   off a real match (`grasp_sheet.py`) the hand came out ~40px on a 540 frame
   and read as a white scribble on the ball -- which is Rick's own complaint
   about Revenant's first cut arriving from the other direction ("the hands
   dont read as hands. not detailed enough"). At that scale a phalanx is 2px
   wide against a 1.4px dark gap, so the two passes that MAKE a skeleton
   legible merge into one blob.

   2.8 puts the hand at ~110px, which is a fifth of the frame -- the number
   v53 measured as too large for one of THREE hands in flight, and about right
   for the only object of its kind on the screen.

   STILL A FIRST CUT. It is a SIZE question, and v53 settled that a size
   question cannot be answered off a sheet: the sheet shows the object still,
   and every size complaint in this project's history has been about an object
   in motion among others. FILM IT. */
const GRIP_SCALE = 2.8;

const WEAPON_BY_ID = Object.fromEntries(WEAPONS.map(w => [w.id, w]));'''),

# ------------------------------------------------------------ 10. the charge
("charge", '''    ult:{ name:"%ULT%", charge:1e9, kind:"grip", dmg:0,''',
 '''    /* CHARGE %CHARGE%, AND IT IS A POSITIVE CHOICE RATHER THAN A DEFAULT.
       v55b: charge was never derived for anybody — 27 relics span 13 to 18
       against ultimates worth -1.9% to +48.1%, correlation +0.17 — and 15 is
       the roster's mode. It is also the strongest single knob on the sheet, 3
       to 5 points of win rate a second in the 8-15 band.

       AND THIS RELIC IS THE ONE PLACE THE USUAL ARGUMENT DOES NOT APPLY. On
       every other umbral relic a longer charge makes the ultimate HIT HARDER,
       because charge is pure wall time and wall time fills the pool the
       ultimate spends (v55 §5: the warhammer's first cast arrives with 2.2x
       the pool behind it that Nightfell's does). GRASP reads the pool not at
       all. The hold scales with nothing that accumulates, so a longer charge
       here is only a cost. */
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"grip", dmg:0, squeeze:%SQUEEZE%,'''),
]


# ------------------------------------------------------- the fx field spec --
# v54 §2b. `drawUltOver`'s `mode === "burst" ? [u.tx, u.ty] : [u.x, u.y]` is
# right for the four novas it was written for and would put this field over the
# QUARRY on a cast that touches nobody. `atSelf` is a property of the FIELD,
# not a relic name in the glue.
FX_ANCHOR = """    gravemourn: { mode: 'implode', n: 1250, sp: [140, 420], grav: 0,
                  drag: 0.55, life: [0.40, 1.00], heavy: 0.03,
                  size: [0.7, 2.0], spawn: 0.55, up: 0 }"""

FX_NEW = """    gravemourn: { mode: 'implode', n: 1250, sp: [140, 420], grav: 0,
                  drag: 0.55, life: [0.40, 1.00], heavy: 0.03,
                  size: [0.7, 2.0], spawn: 0.55, up: 0 },
    /* GRASP GROWS AN ARM, AND `atSelf` IS WHY IT GROWS OUT OF THE RIGHT BALL.
       The second spec in the game to carry the flag: a `burst` is drawn at
       `[u.tx, u.ty]` — at the QUARRY — which is correct for the four novas the
       mode was written for and wrong for anything that resolves on its caster.
       Deadfall's field caught this on the first rendered frame and by nothing
       else.

       LOW AND HEAVY, and it is not Deadfall's discharge. `grav` is positive
       and `sp` is short, so the field falls back toward the shell instead of
       flying off it: what a viewer should read is material GATHERING into a
       limb, not a relic shedding. `n` is the lowest in the umbral school
       because this one is only the growth — the eight seconds after it are a
       drawn object, not a particle field. */
    shroudmaul: { mode: 'burst', n: 820, sp: [40, 260], grav: 210, drag: 2.6,
                  life: [0.35, 1.05], heavy: 0.10, size: [0.6, 2.2],
                  spawn: 0.14, up: 0, atSelf: 1 }"""


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
    fires on its own explanation." `curse_check` did, and `curse_build` refused
    to write on its own paragraph an hour later. Every refusal below greps a
    span of shipped source, and this file explains itself IN that source.

    AND THE LINE-BY-LINE VERSION IS NOT ENOUGH, which this builder found out by
    refusing to write on its own §4.5 paragraph. The earlier strippers in this
    repo drop lines containing `/*`, `*/`, `//` or a leading `*` -- and the
    INTERIOR of a block comment in this codebase is plain indented prose with
    none of those on it. `tickGrasp`'s own comment says "`f.pin` is the Stasis
    Field's only exclusive verb", and the `.pin` refusal fired on it. So the
    block comment is removed as a BLOCK, which is what the probes' own
    `strip` already does.
    """
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def ult_matches(s: str, A) -> None:
    """The shipped `ult` block must carry the numbers this run just printed.

    THE STAGE-3 BUILDER CANNOT RETUNE MOST OF THEM, AND IT REPORTED THAT IT
    HAD. `dur`, `radius`, `cadence`, `grabStun`, `n`, `trueStun` and the tip
    are written by the STAGE-2 insert and are baked into
    `sc-shroudmaul.html`; stage 3 rewrites only the line carrying `charge` and
    `squeeze`. So a stage-3 run with `--cadence 2.0` printed

        ult Grasp  charge 15  dur 8  radius 200  cadence 2  grabStun 1  n 3

    and shipped a relic still reading `cadence:0.6, grabStun:0.5, n:5`. Every
    gate downstream was measuring the OLD rhythm while the log said the new
    one, which is CLAUDE.md §4.9's lost-twelve-values in a different costume --
    and the only reason it was caught is that the probe printed `n=5` two
    minutes later.

    THE FIX IS TO REBUILD STAGE 2, NOT TO WIDEN STAGE 3. Stage 2 owns the
    relic's data and stage 3 owns its mechanism, which is the right split; what
    was missing is this assertion, so the split cannot be forgotten silently.
    """
    i = s.index('id:"%s"' % RELIC)
    j = s.index("blurb:", i)
    block = s[i:j]
    bad = []
    for k, v in (("dur", A.dur), ("radius", A.radius), ("cadence", A.cadence),
                 ("grabStun", A.grabstun), ("trueStun", A.truestun),
                 ("squeeze", A.squeeze), ("charge", A.charge)):
        if f"{k}:{v:g}" not in block:
            bad.append(f"{k} {v:g}")
    if f"n:{int(A.n):d}" not in block:
        bad.append(f"n {int(A.n):d}")
    if f'tip:"{A.tip}"' not in block:
        bad.append("the tip")
    if bad:
        raise SystemExit(
            "THE SHIPPED `ult` BLOCK DOES NOT CARRY: " + ", ".join(bad) + ".\n"
            "  Those fields are written by the STAGE-2 insert, not by this\n"
            "  stage, so the source you built from still has the old values\n"
            "  and this run would have SHIPPED THEM while printing the new\n"
            "  ones. Rebuild stage 2 first:\n"
            "    python shroudmaul_build.py --stage 2\n"
            "    python shroudmaul_build.py --stage 3")
    print("  rule  the shipped ult block carries every number this run printed")


def refuse(s: str) -> None:
    """The four things §8 of the brief says not to do, asserted on the text.

    All four look FINE in every win rate this repo can produce, which is why
    they are checked here rather than left to a sweep.
    """
    lo = s.index("tickGrasp(dt){")
    hi = s.index("tickSling(dt){", lo)
    body = strip_comments(s[lo:hi])

    # §4.1. THE EASIEST WAY TO BUILD THIS WRONG. `takeHitstun` caps at 0.26s
    # and divides each application by `1 + 0.55 * stunDR`, so the second grab
    # onward is eaten -- and the mechanic still "works" by every invariant.
    if "takeHitstun" in body:
        raise SystemExit(
            "`tickGrasp` calls `takeHitstun` (brief §4.1). It caps at "
            "`stunMax` 0.26s\n  and each application shortens the next: five "
            "grabs become one grab and\n  a rumour, no probe fails, and the "
            "only symptom is a `held` column that\n  does not move when the "
            "knobs do. Write `f.stun` directly, as `u.freeze` does.")

    # §4.5 IS NOW A NARROWER RULE RATHER THAN A BAN, and the reason is Rick
    # watching: "hitstun should freeze the enemy ball correct?" It does not --
    # `f.stun` locks the weapon and the ball sails on at 674 px/s -- so the
    # squeeze pins, and ONLY for as long as the fist is shut.
    #
    # WHAT IS STILL FORBIDDEN IS THE FULL PIN. `grab_lab` measured the ball
    # held for the whole `grabStun` at -3.3 points at identical held seconds,
    # and at 39% of the window it is the Stasis Field's verb on a second relic.
    # So the assertion is not "never write pin", it is "write it for the
    # squeeze and for nothing longer" -- which a `grabStun` or `trueStun` in
    # any of the three pin lines would break silently, because a longer hold
    # looks FINE in every win rate and tunes straight out of the blade.
    pinls = [ln for ln in body.splitlines()
             if ".pin" in ln or "pinV" in ln or "pinMax" in ln]
    if len(pinls) != 3:
        raise SystemExit(
            f"`tickGrasp` has {len(pinls)} pin lines and there must be exactly "
            f"three:\n  `pin`, `pinMax` and `pinV`. §4.5 was relaxed to let the "
            f"SQUEEZE stop the\n  ball; it was not relaxed to let this relic "
            f"become a second Stasis Field.")
    for ln in pinls:
        if "grabStun" in ln or "trueStun" in ln or "hold" in ln:
            raise SystemExit(
                f"A pin in `tickGrasp` is written from the STUN and not from "
                f"`u.squeeze`:\n    {ln.strip()}\n  The ball is held for the "
                f"frames the fist is shut and NOT ONE MORE. A full pin\n  "
                f"measured -3.3 points at identical held seconds and holds the "
                f"ball for 39%\n  of the window, which is the Stasis Field's "
                f"only exclusive verb.")

    # §8. NO DAMAGE AND NO APPLICATION, ever. Both were considered and Rick
    # ruled them out, and the pool is measured unmoved by the whole ultimate.
    for bad in ("this.hurt", "pushCurse", 'apply("curse"', ".dealt"):
        if bad in body:
            raise SystemExit(
                f"`tickGrasp` contains {bad!r} (brief §8). The grab deals "
                f"nothing and\n  applies nothing -- that is Rick's §1 and it is "
                f"measured: the whole\n  ultimate moves the pool by +1.2 blows "
                f"and +5.4%.")

    # §4.6. FOE ONLY, and the rule is structural. A hand that grabs a shade
    # spends a grab on a copy that is about to expire, and the counter toward
    # the crush is paid with it. `tickShadeHits` is where v51 §4.3's bug lived.
    if "shades" in body or "shade" in body:
        raise SystemExit(
            "`tickGrasp` mentions a shade (brief §4.6). Foe only: the loop "
            "reads\n  `this.a` and `this.b` and nothing else, so there is no "
            "`if` to get wrong.\n  If that rule is being CHANGED, it is a "
            "decision and it belongs in the\n  comment as well as in the code.")

    # §4.2. AND ONLY THE LAST GRAB IS A REGISTERED TRUE STUN. `breakSpin` is
    # the hook every true stun calls; calling it once per grab would turn a
    # rhythm into a lockout and would be invisible in the `held` column.
    if body.count("breakSpin") != 1:
        raise SystemExit(
            f"`tickGrasp` calls `breakSpin` {body.count('breakSpin')} times "
            f"(brief §4.2). Exactly one:\n  the crush. The ordinary grabs "
            f"DELAY a wind-up and must not cancel it,\n  which is Rick's own "
            f"rule and the reason the true-stun register is nameable.")
    print("  rule  no takeHitstun, no damage, no curse, foe only, one "
          "true-stun site,\n        and the pin is the squeeze's length and "
          "never the stun's")


def sync_fx(s: str) -> str:
    """The inlined copy and the file on disk must stay the same object.

    `fx_build.py` inlines `src/render/fx.js` verbatim and stamps its sha256
    into the page. A spec written only into the page is a spec the next
    `fx_build` run silently drops -- and `ULTFX.sync` RETURNS on a missing
    spec, which is not an error, which is exactly why it would ship. An
    ultimate with no field among twenty-seven that have one is a picture fault
    with no number attached to it.
    """
    fx_js = HERE.parent / "src" / "render" / "fx.js"
    mod = fx_js.read_text(encoding="utf-8")

    # A STAGE-3 REBUILD AFTER THE SPEC HAS BEEN COMMITTED IS THE NORMAL CASE,
    # AND THE FIRST CUT OF THIS COULD NOT DO IT. Once the spec is in
    # `src/render/fx.js` on disk, that file no longer matches the copy inlined
    # in stage 2's output -- which is correct and expected, because stage 2
    # predates the spec -- and the divergence check fired on it. Rebuilding
    # stage 3 to change one line of ART then required hand-editing a tracked
    # file first, which is exactly the kind of manual carry step this repo
    # keeps getting wrong (CLAUDE.md, `app/main.js`'s GAME line).
    #
    # So this builder's own spec is REMOVED first if it is already there, and
    # the identity check below then compares the two PRE-SPEC modules, which is
    # the thing it was always trying to assert.
    if FX_NEW in mod:
        mod = mod.replace(FX_NEW, FX_ANCHOR, 1)
        print("  fx    stripping this builder's own spec from src/render/fx.js "
              "first — a rebuild, not a first build")

    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    if not tm:
        raise SystemExit("no ULT FIELDS glue after the inlined fx.js")
    inlined = s[head.end():tm.start()].rstrip("\n")
    if inlined != mod.rstrip():
        raise SystemExit(
            "src/render/fx.js and the copy inlined in this build have "
            "DIVERGED before\n  this builder wrote anything. Fix that first.")

    if FX_ANCHOR not in mod or FX_ANCHOR not in s:
        raise SystemExit("the fx spec anchor is not in both copies")

    mod2 = mod.replace(FX_ANCHOR, FX_NEW, 1)
    s = s.replace(FX_ANCHOR, FX_NEW, 1)
    fx_js.write_text(mod2, encoding="utf-8", newline="\n")

    old_sha = head.group(1)
    new_sha = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])

    # AND THE TWO ARE COMPARED AGAIN AFTER THE WRITE, because "I wrote both"
    # is a promise and this is the assertion. `thornshear_build` established
    # the refusal; this is it re-stated on the output rather than the input.
    head2 = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                      r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm2 = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head2.end())
    if s[head2.end():tm2.start()].rstrip("\n") != mod2.rstrip():
        raise SystemExit("the inlined copy and src/render/fx.js DIVERGED "
                         "across this builder's own write")
    print(f"  fx    src/render/fx.js + inlined copy carry the spec, "
          f"re-stamped {old_sha[:16]} -> {new_sha[:16]}")
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True, choices=(2, 3))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--charge", type=float, default=15.0)
    # THE BLADE BELONGS TO WHICHEVER STAGE IS RUNNING. Stage 2 ships the relic
    # at Grudgebearer's 23.5, which is what its own floor gate is measured
    # against; stage 3b is where it is bisected. Defaulting both to the tuned
    # value made stage 2 write 21.0 and stage 3 then fail looking for 23.5 to
    # replace -- a loud failure, but only because the retune asserts.
    ap.add_argument("--dmg", type=float, default=None,
                    help="stage 2: the starting blade (default 23.5). "
                         "stage 3b: the tuned one (default %.2f)" % TUNED_SM)
    for k, v in ULT.items():
        ap.add_argument(f"--{k.lower()}", type=float, default=v)
    A = ap.parse_args()
    if A.dmg is None:
        A.dmg = BLADE_IN if A.stage == 2 else TUNED_SM

    src = A.src or ("../02-chain/sc-revenant.html" if A.stage == 2
                    else "../02-chain/sc-shroudmaul.html")
    out = A.out or ("../02-chain/sc-shroudmaul.html" if A.stage == 2
                    else "../02-chain/sc-grasp.html")
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nSHROUDMAUL -- STAGE {A.stage}: "
          + ("the 28th relic, its ultimate stubbed"
             if A.stage == 2 else "GRASP -- one hand, tethered, and it waits"))
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR AND STAGE 1 IS NOT OPTIONAL. `Grasp` is the new
    # relic's ultimate; if Gravemourn still owns the word, two relics in one
    # school share a verb and every comment naming it is ambiguous.
    if 'name:"Revenant"' not in s0:
        raise SystemExit("this source has no Revenant -- STAGE 1 lands FIRST "
                         "(brief §0). Run revenant_rename.py.")
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the curse rework is "
                         "upstream of this whole chain")

    if len(A.tip) > 72:
        raise SystemExit(f"ULT TIP is {len(A.tip)} characters against 72:\n  {A.tip}")
    if int(A.n) < 2:
        raise SystemExit(f"n {A.n:g}: a hand that crushes on its first grab is "
                         f"not an escalation, it is a nova with a wind-up. "
                         f"Rick's own range is 2-6.")

    subs = {"%ULT%": A.ult, "%TIP%": A.tip, "%BLURB%": BLURB,
            "%DMG%": f"{A.dmg:g}", "%CHARGE%": f"{A.charge:g}",
            "%DUR%": f"{A.dur:g}", "%RADIUS%": f"{A.radius:g}",
            "%CADENCE%": f"{A.cadence:g}", "%GRABSTUN%": f"{A.grabstun:g}",
            "%N%": f"{int(A.n):d}", "%TRUESTUN%": f"{A.truestun:g}",
            "%SQUEEZE%": f"{A.squeeze:g}"}

    if A.stage == 2:
        if f'id:"{RELIC}"' in s0:
            raise SystemExit("this source already has Shroudmaul -- already built")
        edits = S2
        print(f"  ult {A.ult}  STUBBED at charge 1e9   "
              + "  ".join(f"{k} {getattr(A, k.lower()):g}" for k in ULT))
        print(f"  tip {len(A.tip)}/72  {A.tip}")
        print(f"  blade {A.dmg:g}   (Grudgebearer's, as a start)")
    else:
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("this source has no Shroudmaul -- stage 2 lands "
                             "before stage 3 (brief §0)")
        if '"grip"' not in s0:
            raise SystemExit("this source has no grip ult -- stage 2 first")
        if "tickGrasp" in s0:
            raise SystemExit("this source already has tickGrasp -- already built")
        edits = S3
        print(f"  ult {A.ult}  charge {A.charge:g}   "
              + "  ".join(f"{k} {getattr(A, k.lower()):g}" for k in ULT))
        print(f"  held  predicted 6.5-7.0 s a fight at these numbers "
              f"(brief §6, registered)")

    for label, old, new in edits:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    if A.stage == 3:
        if abs(A.dmg - BLADE_IN) > 1e-9:
            # THE WARHAMMERS SHARE A STAT LINE, so the blade is found by
            # walking forward from the relic's own id and never by a global
            # replace: Grudgebearer ships at exactly 23.50 too.
            old_blade = f"mass:5.0, knockMul:2.3,"
            i = s.index(f'id:"{RELIC}"')
            j = s.find(f"dmg:{BLADE_IN:g},", i)
            if j < 0 or j - i > 400:
                raise SystemExit(f"cannot retune the blade: dmg:{BLADE_IN:g} "
                                 f"is not in Shroudmaul's own entry.")
            s = s[:j] + f"dmg:{A.dmg:g}," + s[j + len(f'dmg:{BLADE_IN:g},'):]
            print(f"  blade dmg {BLADE_IN:g} -> {A.dmg:g}  (stage 3b)")
        refuse(s)
        ult_matches(s, A)
        s = sync_fx(s)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")

    if A.stage == 2:
        print("\n  NEXT:")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40      # 28 relics")
        print(f"    python shroudmaul_sweep.py --game {out} --only 0")
        print("      the floor: Shroudmaul with no ultimate should land ~27%")
    else:
        print("\n  NEXT, and item one is not optional (v43 §13, brief §0):")
        print(f"    python cinema_clip.py --game {out} --a shroudmaul "
              f"--b emberedge --seed <seed> --full   # FILM IT FIRST")
        print(f"    python grasp_relic_probe.py --game {out}")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
