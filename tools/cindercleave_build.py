#!/usr/bin/env python3
"""CINDERCLEAVE, THE 29TH RELIC, AND ITS ULTIMATE BREACH. STAGES 1, 2 AND 3.

    python cindercleave_build.py --stage 1 --src ../02-chain/sc-gnawed.html \
                                 --out ../02-chain/sc-cindercleave.html
    python cindercleave_build.py --stage 2 --src ../02-chain/sc-cindercleave.html \
                                 --out ../02-chain/sc-thepass.html
    python cindercleave_build.py --stage 3 --src ../02-chain/sc-thepass.html \
                                 --out ../02-chain/sc-breach.html

`06-docs/v57/cindercleave-build-brief-v57.md`, and the design and the pricing
behind it are in `06-docs/v57/cindercleave-design-v57.md`.

## TWO DEPARTURES FROM THE BRIEF, BOTH BOOKKEEPING, BOTH DECLARED HERE

**IT IS THE TWENTY-NINTH RELIC AND THE BRIEF SAYS THIRTIETH.** `WEAPONS` holds
28 on `sc-gnawed.html`; counted, Cindercleave is 29 and every `engine_ab` run
in the gates is over 28 others rather than 29. Nothing in the design moves.

**AND IT IS BUILT OFF `sc-gnawed.html`, NOT `sc-grasp.html`.** The brief was
written before v58, which redrew the umbral warhammer on top of Grasp and is
the build of record. `sc-grasp.html` is one link behind it. Building off the
tip is the whole point of a linear chain, and `_whGnawed` is render-only
(`engine_ab` 3024/3024), so nothing this relic is priced against moved.

## RICK'S §1, VERBATIM

    for a duration the scythe can collide with the walls of the arena. When it
    does it tears open a hole where lava/heat beams periodically spew out and
    damage enemy fighters caught in their blast.

    The vents should be able to be torn in all directions. some flowing
    parallel or perpendicular to the battlefield. but also some torn in
    diagonals.

plus, on top of it: *"can we come up with a way for the size of the vents to
vary? so a graze to the wall makes a small one but a full slash makes a larger
one?"* and *"can we achieve better balance by only letting it open a set number
of vents? so instead of a duration it can open 3-5 and then its done?"*

## THE LARGEST NUMBER IN THE DESIGN IS NOT THE LAVA

    beams apply 1 Sunder      71.9%   +28.5%
    beams apply NOTHING       61.9%   +18.5%      <- and it lands MORE beams

The no-sunder arm lands 7.3 hits a fight against 6.3 and is **ten points
worse**. The beams' damage is worth +1.9pp over the floor; the sunder they
apply is worth +10.0pp on top of the same beams.

**BREACH IS NOT A DAMAGE ULTIMATE. It is a second contact rate running
underneath a slow weapon.** `sunder_survey` put the six types either side of a
threshold at the status's own 5.0s duration -- `gap / dur` reads 0.66, 0.67,
0.69 and then 1.02, 1.05, 1.26, with nothing between -- and the scythe misses
the line by 0.24 seconds. The lava is what it looks like. Filling the gaps
between a scythe's slow blows is what it does.

## AND UNLIKE GRASP, IT DOES NOT COLLAPSE ONTO ONE SCALAR

Shroudmaul's whole ultimate fitted `lift = +3.1 + 2.62 x held` at r2 0.79 with
residuals smaller than the measurement error, so its arrangement was free.
Beam hits landed gets r2 **0.33** here, and the arms furthest off the line are
the ones that change what a hit *does*. **Breach is TWO numbers -- hits landed,
and what a hit is worth -- and both have to be tuned.** Four knobs each move it
about eleven points (design §3.7).

## WHAT WILL BITE

**THE BLADE IS ALREADY THROUGH THE WALL.** `bladeSegments` runs from `R - 4` to
`R + reach` and `move()` clamps the ball's centre at `n + R`, so a scythe
against a wall has up to 104 units of blade inside the stone on most of every
rotation. "The scythe can collide with the walls" is not a new collision -- it
is a test nobody was running, and the design's real question is never *whether*
it tears but *how often it is allowed to*.

**SO THE TEAR RESOLVES AT THE END OF THE PASS AND NOT THE START.** Tearing on
the frame the blade first crosses the plane samples the SHALLOWEST moment of
the cut -- the size mechanic would have almost no range -- and it needs an
arbitrary cooldown to stop a pinned ball tearing one a frame. A pass opens on a
crossing, keeps the deepest one, and resolves when the blade leaves. **One
pass is one vent and the weapon's own rotation is the spacing rule.**

**A VENT IS `{wall, u}` AND NEVER AN `(x, y)`.** v40 §3.3: `CONFIG.collapse`
walks the inset 0 -> 140 from t=21s, so an absolute position torn early is
buried in the wall by the end of the fight. `tickVines` is the pattern and it
is forty lines away from the new code.

**THE HOLES OUTLIVE THE LICENCE, SO THEY CANNOT LIVE ON IT.** They keep their
own 9s clock and go on firing after the window has closed -- and they must not
hang off `m.ultFx` either (v54 §2a: one slot, the opponent overwrites it,
measured at 0.0% survival against Ironhail). The licence is `f.ultBreach`; the
holes are `m.vents`.

**DO NOT BUILD THE JET ON `shots`.** `spawnShot` shifts the oldest live entry
out at `maxLive` 64 and -- the real hazard -- `tickShots` lets `bladeSegments`
PARRY a shot, with melee's defence winning ties. A jet of heat a scythe can
parry is a different mechanic and nobody has decided it is this one.

**AND THE FRONT IS THE MECHANIC, NOT THE DECORATION.** Resolving the whole line
at once is +4.2pp stronger and it is the version Rick already rejected once, on
a different relic: v40's Thicket, *"the vines look stationary and damage the
enemy ball when it happens to run into them"*. A strike with no duration reads
as a hazard you walked into.

EVERYTHING DRAWN HERE IS A FIRST CUT AND NOBODY HAS WATCHED IT. Five holes,
four states each, and a jet that has to read against a hall that already
blooms. FILM IT BEFORE TUNING ANYTHING -- v43 §13, and v54 §2c is why it is not
optional.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "cindercleave"

# --- THE RELIC. Every physical stat is the SCYTHE'S, copied off Thornwake,
#     Lastlight, Foregone and Vesper -- all four already share this line byte
#     for byte. Weapon-matrix decision 1: the TYPE owns the physics, the SCHOOL
#     owns status and palette.
BLADE_IN = 21.0      # THE BISECTION START, not a shipped number. Design §3.6:
                     # 20 reads 48.5% and 22 reads 53.1%, so the answer is
                     # expected in 20-22 -- and the curve is steep below 22 and
                     # flat-to-noisy above it, which is its own finding.
TUNED_CC = 20.25     # STAGE 3b, RE-MEASURED WITH THE SHOVE IN. Blade and
                     # knockback are not separable: `cindercleave_sweep
                     # --only 2`, n=1008 a point on TWO seed blocks and BOTH
                     # sides, at `jetKnock` 260:
                     #
                     #     blade   A blk1  A blk2  B blk1   pooled
                     #     19.00    47.4%   46.0%   45.8%    46.4%
                     #     19.38    47.9%   44.8%   48.8%    47.2%
                     #     19.75    47.5%   47.0%   48.0%    47.5%
                     #     20.12    48.8%   49.2%   50.6%    49.5%
                     #     20.50    49.8%   53.0%   51.1%    51.3%
                     #
                     # Monotonic pooled, crossing interpolated at 20.22, and
                     # 20.25 is the round quarter-point inside the half-damage
                     # band the honest precision allows (v56's own call, which
                     # shipped "a round 21.0" against a bisected 19.92).
                     #
                     # AND THE SHOVE COSTS 2.3 POINTS, WHICH THE LADDER THAT
                     # PRICED IT COULD NOT SEE. `--only 5` swept `jetKnock`
                     # across 0 / 130 / 260 / 420 / 600 at n=672 a point and
                     # every arm landed inside one SE of every other -- read as
                     # "the shove is free, so choose it for the picture". The
                     # wide measurement then put blade 19.75 at 49.8% with no
                     # shove and 47.5% with it: **-2.3pp, on the same seeds, at
                     # n=3024 each.** A knob that measures free at n=672 and
                     # costs a fifth of a damage point at n=3024 is the third
                     # instance in this one build of CLAUDE.md's n~700 floor,
                     # after the curve that chose the wrong bracket and the
                     # per-relic reading that disagreed with `verify`.
                     #
                     # WHAT THE SHOVE BUYS BACK is contact, and it is why the
                     # cost is only 2.3 and not more: jet hits a fight rise
                     # 7.41 -> 8.04 and the mean Sunder on the quarry 3.87 ->
                     # 4.02, because five holes fire along five different
                     # bearings and a quarry thrown off one wall is as likely
                     # to be pushed INTO another jet as out of it. What it
                     # spends is the BLADE: 7.47 blows a fight -> ~7.25.
                     # v51 §4.3's "knockback eating its own window", small.

ULT = {
    "n":        5,     # HOLES TO A CAST, AND THE WINDOW ENDS ON THE FIFTH.
                       # Rick's, from three offered, and it is the structural
                       # fix rather than a balance knob: the clock version's
                       # worth was CONTACT RATE, and contact rate is the
                       # noisiest thing in the game -- a cast spent near a wall
                       # tore twice what a cast spent mid-arena tore, so two
                       # casts of the same ultimate in one fight were not the
                       # same ultimate. A count deletes that entirely.
                       #
                       # More holes is stronger at a fixed blade, monotonically
                       # (2.97 / 3.77 / 4.59 / 5.37 holes a cast for n=3..6),
                       # but the blade is bisected afterward either way, so
                       # what `n` decides is what the relic is MADE OF: three
                       # holes and a blade near 24-25 is a heavy scythe with an
                       # accent, five holes and a blade near 21 is a moderate
                       # scythe that lives on its ultimate.
    "cap":      14.0,  # A GUARD RAIL, NOT A MECHANIC. A count with no clock
                       # behind it never ends if the ball never reaches a wall,
                       # and the window would carry into the next cast and out
                       # of the fight. Measured, 14s ended the window in 0.01
                       # fights out of one. DO NOT TUNE IT AND DO NOT PUT IT IN
                       # THE TIP.
    "passMax":  1.2,   # the pass guard, for a ball that is genuinely pinned.
                       # It is not a tear cooldown -- THE PASS IS THE COOLDOWN
    "kMin":     0.5,   # k = lerp(kMin, kMax, pen01), and it drives WIDTH and
    "kMax":     1.5,   # LIFE and nothing else. Driving all four of width, life,
                       # damage and period is +6.1pp stronger and is four knobs
                       # riding one scalar, which leaves the bisection nothing
                       # to grab (design §3.2)
    "maxVents": 8,     # holes alive at once, across both fighters. 5 costs
                       # 6.2 points against 8 and this is the design centre
    "warm":     0.35,  # the hole glows before its first firing
    "period":   1.1,   # per hole
    "life":     9.0,   # x k
    "half":     14.0,  # x k -- the beam's half-width at full bloom
    "jetDmg":   9.0,   # FLAT. Not scaled by k, and not the point: see the
                       # header. Doubling the sunder application is worth
                       # +1.1pp and doubling this is worth much less than the
                       # sunder is
    "speed":    1100., # units a second -- 0.9s across the hall. FREE:
                       # everything from 650 to 1800 is inside one SE of
                       # everything else in that range, so it is chosen for the
                       # look. Only the instantaneous bar and the 350 arm
                       # separate at all
    "taperTo":  0.55,  # the taper reaches full width at this fraction of the
                       # hall's diagonal, from 0.25 of `half` at the wall
    "sunderN":  1,     # per hit, FOE ONLY. NOT A KNOB -- 2 stacks a hit is
                       # worth +1.1pp over 1
    "jetKnock": 260.,  # RICK'S, off the first cut: "lets give the beams some
                       # knockback." It is applied ALONG THE JET'S OWN BEARING,
                       # which is off the wall and into the room -- the
                       # Thicket's `whipKnock` is the precedent and its comment
                       # gives the reason: `resolveHit`'s built-in knock fires
                       # away from the CASTER, and a hazard that is not the
                       # caster needs its own direction or the shove reads as
                       # coming from the wrong place.
                       #
                       # AND IT IS THE ONE THING IN THIS DESIGN THAT CAN EAT
                       # ITSELF. v51 §4.3, and Gravemourn's blade curve BENDING
                       # DOWNWARD is the measured instance: a shove that throws
                       # the quarry out of the caster's reach costs the blade
                       # more than the jet gains. Five holes firing along five
                       # different bearings can also shove the quarry OUT of
                       # another jet's path or INTO it, so this number is swept
                       # rather than chosen -- `cindercleave_sweep --only 5`.
}

ULT_NAME = "Breach"
# THE NUMBER IN THE TIP IS SUBSTITUTED, NOT TYPED. v40 shipped a card reading
# "5s" after a sweep moved the number to 8.1 and nothing caught it, because
# `verify.py` only asks that a tip EXISTS. It is a WORD here rather than a
# digit, which is the same hazard wearing a hat.
ULT_TIP = "Cuts the walls open — %NWORD% vents that spit heat and Sunder"
NWORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
BLURB = ("Forged for a harvest and handed a hall. What it opens in the stone "
         "stays open, and the mountain does the rest.")


# ============================================================ STAGE 1 =======
S1 = [

# --------------------------------------------------------- 1. the 29th relic
("relic", '''    blurb:"Bone under the iron, and it did not start there. What it takes hold of does not get to swing back." },

];''',
 '''    blurb:"Bone under the iron, and it did not start there. What it takes hold of does not get to swing back." },

  /* CINDERCLEAVE — THE DWARVEN SCYTHE, and the twenty-ninth relic. Dwarven
     was on 4 of 6 types and the scythe on 4 of 7 schools; this puts both on 5.

     EVERY PHYSICAL STAT IS THE SCYTHE'S, copied off Thornwake, Lastlight,
     Foregone and Vesper — all four already carry this line byte for byte and
     the TYPE owns it. `SHAPES.scythe` routes `dwarven` to `_scBuilt`, which
     has drawn this cell since before there was a relic in it.

     AND THE CELL CANNOT BE ARGUED ON THE CHANNEL, WHICH IS THE FINDING THAT
     NAMED THE ULTIMATE. `sunder_survey` measured dwarven's channel on all six
     types at their own shipped damage and the roster splits in half at the
     status's OWN duration: `gap / dur` reads 0.66, 0.67, 0.69 — and then 1.02,
     1.05, 1.26, with nothing at all between 0.69 and 1.02. A weapon that
     swings faster than Sunder decays compounds toward the cap in 78-89% of
     fights; a weapon slower than it starts from zero on 40-50% of its blows.
     **The scythe misses that line by 0.24 seconds** — 5.24s between blows
     against a 5.0s status — and sits at 1.23 stacks when it lands one.

     SO THE ULTIMATE FILLS THE GAPS. Dwarven's other four all treat the stack
     as something to SPEND or make more of — the Crucible consumes it,
     Slagburst detonates it, Ironbloom's shrapnel applies more, Quarrelstorm
     ignores it. Nothing in the school HOLDS it, and holding it is what this
     body needs; Breach does the third thing and adds a second contact rate
     underneath the blade. Measured, that is the whole ultimate: the same beams
     with no Sunder on them land MORE hits and are ten points worse.

     `dmg` is the tuned knob (cindercleave_build.TUNED_CC) and it starts at 21,
     which is a bisection START and not a shipped number. */
  { id:"cindercleave", name:"Cindercleave", aff:"dwarven", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:%DMG%, spin:3.2, mode:"spin", mass:2.4,
    onHit:{ sunder:1 },
    /* BREACH. STUBBED AT `charge:1e9` IN STAGE 1, which is the same "OFF" the
       charge sweep in v55b used and the same one Shroudmaul's stage 2 used:
       the clock can never reach it, `fireUlt` never runs, and the relic is
       measured as a blade and a channel and nothing else. Stage 2 brings the
       charge down to %CHARGE% and opens the licence; stage 3 lights the jets.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       CHARGE 15 IS A POSITIVE CHOICE AND THIS RELIC IS SENSITIVE TO IT, which
       is the opposite of Shroudmaul one build ago: 18 costs 10.8 points here,
       because charge is pure wall time and every second of it is a second the
       holes are not open. 15 is also the roster's mode (v55b: nobody's charge
       was ever derived). */
    ult:{ name:"%ULT%", charge:1e9, kind:"breach",
          n:%N%, cap:%CAP%, passMax:%PASSMAX%,
          kMin:%KMIN%, kMax:%KMAX%, maxVents:%MAXVENTS%,
          warm:%WARM%, period:%PERIOD%, life:%LIFE%, half:%HALF%,
          jetDmg:%JETDMG%, speed:%SPEED%, taperTo:%TAPERTO%, sunderN:%SUNDERN%,
          jetKnock:%JETKNOCK%,
          tip:"%TIP%" },
    blurb:"%BLURB%" },

];'''),
]


# ============================================================ STAGE 2 =======
# THE PASS AND THE TEAR. Holes open, they are sized, they are drawn -- and they
# do not fire. This stage exists as its own link for one reason: design §3.2's
# depth distribution is a PUBLISHED PREDICTION made before the build existed,
# and it is the only part of this design that can be falsified without a single
# beam being drawn.
S2 = [

# ------------------------------------------------------ 1. the licence's home
("Fighter.ultBreach", '''    this.graspFade = 0;''',
 '''    this.graspFade = 0;
    /* THE LICENCE. `{t, cap, n, tears, pass, byCap}` while BREACH's window is
       open, and null on every other relic and on this one outside its own
       window — which is the whole zero-burden argument: `tickBreach` returns
       after a two-iteration loop that does nothing, `drawVents` returns on its
       first line, and nothing else in the engine reads this field.

       IT IS A LICENCE AND NOT A CLOCK. Rick: "can we achieve better balance by
       only letting it open a set number of vents? so instead of a duration it
       can open 3-5 and then its done?" `cap` is a guard rail behind the count
       — a count with no clock never ends if the ball never reaches a wall, and
       the window would carry into the next cast and out of the fight.

       `pass` IS THE CUT IN PROGRESS and it lives HERE rather than on the
       fighter, because a pass that is not inside a licence is not a pass — it
       is a scythe doing what a scythe does against a wall on most of every
       rotation, which is the thing §4.1 of the design doc is about. */
    this.ultBreach = null;
    /* AND THE LICENCE'S OWN FADE, because the window closing is not the same
       event as the picture of it ending. Same shape as `graspFade`,
       `deadfallFade` and `winnowFade`. It is on the FIGHTER and not on
       `m.ultFx` for the measured reason v54 §2a gives, and it is driven in
       `tickPresentation` so it does not freeze through a hit stop. */
    this.breachFade = 0;'''),

# ------------------------------------------------------- 2. the holes' home
("Match.vents", '''    this.vines = [];
    this.vineSeq = 0;         // deterministic per-plant art variation''',
 '''    this.vines = [];
    this.vineSeq = 0;         // deterministic per-plant art variation
    /* THE VENTS, AND THEY ARE PER-MATCH STATE ON THE MATCH. In the same family
       as `vines`, `sigils`, `sparks` and `shades`: SIM objects that only one
       relic can ever create, so every loop over them runs zero times in any
       match without it. `tickBreach` returns on its first line when this is
       empty and `drawVents` on its own.

       THEY CANNOT LIVE ON THE LICENCE. A hole keeps its own nine-second clock
       and goes on firing after the window that tore it has closed — that is
       the sentence, and it is what makes the last third of a fight against
       this relic different from the first. So it outlives `f.ultBreach`, it
       outlives its own caster, and it is discarded only when the match ends.
       Not on `m.ultFx` either, which is ONE SLOT the opponent overwrites the
       instant they cast anything (v54 §2a, chain-wide open item 25).

       A VENT IS A WALL AND A FRACTION ALONG IT. `m.inset` walks 0 -> 140 as
       the hall collapses, so an absolute (x, y) torn early is outside the room
       later — buried in the stone, venting off-screen. Storing {wall, u} and
       recomputing the position each frame is two lines and makes the collapse
       part of the mechanic. v40 §3.3, and `tickVines` is forty lines away. */
    this.vents = [];
    this.ventSeq = 0;         // deterministic per-vent bearing'''),

# ------------------------------------------------------------ 3. the tick
("step.tickBreach", '''    this.tickGrasp(dt);
    this.tickBallista(dt);''',
 '''    this.tickGrasp(dt);
    /* AFTER the fighter loop that moved the blade and BEFORE the hit loops,
       for the reason `tickWinnow` gives one line up: the wall's state has to
       be current on the frame a blade arrives at it. A vent is torn from
       `bladeSegments`, which is recomputed from `theta` — so there is nothing
       stored here to keep in sync. */
    this.tickBreach(dt);
    this.tickBallista(dt);'''),

# ---------------------------------------------------------- 4. the licence
("tickBreach", '''  tickDeadfall(dt){''',
 '''  /* BREACH — A LICENCE TO CUT THE WALLS, AND THE HALL KEEPS WHAT IT IS GIVEN.

     Rick's §1: "for a duration the scythe can collide with the walls of the
     arena. When it does it tears open a hole where lava/heat beams
     periodically spew out and damage enemy fighters caught in their blast."

     ── THE BLADE IS ALREADY THROUGH THE WALL ──────────────────────────────

     `bladeSegments` runs from `R - 4` out to `R + reach` and `move()` clamps
     the ball's centre at `n + R`, so a scythe standing against a wall has up
     to 104 units of blade INSIDE the stone on most of every rotation. There is
     no new collision here. There is a test nobody was running, and a rule
     about how often it is allowed to fire — which is the whole of what this
     ultimate had to invent.

     ── IT NEVER RUNS DURING A HIT STOP, AND THAT IS STRUCTURAL ─────────────

     `step()` returns through `decayImpactOnly` for as long as `hitStop` runs
     and this tick sits below that return, so the hall is frozen with the rest
     of the world and there is no guard here to get wrong. Every lab that
     priced this skipped its own hit-stop frames explicitly to model exactly
     that, which is why the numbers transfer.

     ── AND THE TEAR RESOLVES AT THE END OF THE PASS ────────────────────────

     Tearing on the frame the blade first crosses the plane samples the
     SHALLOWEST moment of the cut, which would leave Rick's size mechanic with
     almost no range at all — and it needs an arbitrary cooldown to stop a
     pinned ball tearing one a frame. So:

       a pass OPENS       when any blade end crosses a wall plane
       a pass ACCUMULATES the deepest crossing and the dwell, per frame
       a pass RESOLVES    when no blade end is beyond the plane — or at
                          `passMax`, the guard for a ball that is truly pinned

     ONE PASS IS ONE VENT AND THE WEAPON'S OWN ROTATION IS THE SPACING RULE.
     Measured in the lab at exactly `10.7 passes, 10.7 vents`. A pass that
     changes wall closes and a new one opens, so a corner is two passes and
     that is deliberate. */
  tickBreach(dt){
    const A = CONFIG.arena, R = CONFIG.physics.ballR, n = this.inset;

    for (const f of [this.a, this.b]){
      const V = f.ultBreach;
      if (!V) continue;
      V.t += dt;
      /* THE TWO WAYS OUT IN THIS STAGE, AND THE COUNT IS NOT ONE OF THEM YET.
         "The FIFTH cut ends it" lands in stage 3 with the jets, so every pass
         that closes here tears — which is what the distribution gate wants,
         because a licence that stopped at five would throw away most of the
         passes it is supposed to be measured over. */
      const done = V.t >= V.cap || !f.alive;

      /* THE DEEPEST CROSSING THIS FRAME, over every blade. `pen` is measured
         past the wall FACE and normalised in `tearVent` by the weapon's own
         reach, so the scalar is "how much of this blade went in" rather than a
         number of pixels that stops meaning anything the day reach changes.

         `f.stun <= 0` because a locked weapon cannot cut. It is the same rule
         `tickHits`, `tickWeapon` and `tickFire` already live under, and it is
         what makes a true stun a real answer to this relic with no special
         case written anywhere. */
      let wall = null, pen = 0, hx = 0, hy = 0;
      if (!done && f.stun <= 0){
        for (const s of this.bladeSegments(f)){
          const cand = [["W", n - s.bx, n, s.by],
                        ["E", s.bx - (A.w - n), A.w - n, s.by],
                        ["N", n - s.by, s.bx, n],
                        ["S", s.by - (A.h - n), s.bx, A.h - n]];
          for (const [wl, p, cx, cy] of cand)
            if (p > pen){ pen = p; wall = wl; hx = cx; hy = cy; }
        }
      }

      if (wall){
        if (!V.pass || V.pass.wall !== wall){
          if (V.pass) this.tearVent(f, V.pass);
          /* `lo`/`hi` ARE THE SWEPT EXTENT and `cx`/`cy` are where the blade is
             RIGHT NOW, and both exist for the picture rather than for the
             mechanic. Rick, off the first cut: "the scythe should also have an
             animation showing it tear open the arena not just placing the
             breaches on the wall." A cut that is invisible until it resolves
             leaves the hall placing holes by itself, which is the opposite of
             what §1 says is happening — so `drawVents` draws the SCAR the
             blade is opening, and the tear then opens along exactly the stretch
             of wall the viewer just watched it cross. Nothing in the simulation
             reads any of the four. */
          V.pass = { wall, maxPen: 0, dwell: 0, hx, hy,
                     lo: Infinity, hi: -Infinity, cx: hx, cy: hy };
        }
        const P = V.pass;
        P.dwell += dt;
        P.cx = hx; P.cy = hy;
        const along = (wall === "N" || wall === "S") ? hx : hy;
        if (along < P.lo) P.lo = along;
        if (along > P.hi) P.hi = along;
        if (pen > P.maxPen){ P.maxPen = pen; P.hx = hx; P.hy = hy; }
        if (P.dwell >= (f.w.ult.passMax || 1.2)){
          this.tearVent(f, P); V.pass = null;
        }
      } else if (V.pass){
        this.tearVent(f, V.pass); V.pass = null;
      }

      if (done){
        /* A CUT IN PROGRESS WHEN THE WINDOW ENDS STILL LANDS. `tearVent` is
           the single gate on whether a tear is allowed at all, so this line
           cannot outrun the count — which it otherwise could, on the one path
           where the last tear came from a wall CHANGE and opened a fresh pass
           on the same frame. */
        if (V.pass) this.tearVent(f, V.pass);
        f.ultBreach = null;
      }
    }

    if (!this.vents.length) return;         // <- the zero-burden guard
    for (let i = this.vents.length - 1; i >= 0; i--){
      const v = this.vents[i];
      v.t += dt;
      if (v.t >= v.life){ this.vents.splice(i, 1); continue; }

      /* THE HOLE RIDES THE WALL IN. Recomputed every frame from the CURRENT
         inset, which is the whole reason a vent is stored as {wall, u}. */
      if (v.wall === "N" || v.wall === "S"){
        v.x = n + v.u * Math.max(1, A.w - 2 * n);
        v.y = v.wall === "N" ? n : A.h - n;
      } else {
        v.x = v.wall === "W" ? n : A.w - n;
        v.y = n + v.u * Math.max(1, A.h - 2 * n);
      }
      /* ---- THE JETS. STUBBED IN STAGE 2, and that is the point of the stage:
         the pass, the tear and the size are the half of this design that can
         be falsified against a published distribution before a single beam is
         drawn. Stage 3 replaces this block. ---- */
    }
  }

  /* ONE PASS, ONE VENT — and this is where Rick's two additions to the §1 both
     land: the SIZE the cut earned, and the count it spends. */
  tearVent(f, P){
    const V = f.ultBreach;
    /* A TEAR WITHOUT A LICENCE IS A SCYTHE DOING WHAT A SCYTHE DOES, which is
       standing in a wall on most of every rotation. The count joins this
       guard in stage 3. */
    if (!V) return;
    const A = CONFIG.arena, n = this.inset, u = f.w.ult;

    /* THE SIZE, AND IT IS RICK'S: "a graze to the wall makes a small one but a
       full slash makes a larger one". The prior question was whether the
       physics makes the distinction at all, and it does — 2,780 passes, median
       0.63 of the blade, quartiles 0.30 / 0.63 / 0.92, and a fat spike of
       27.4% at full burial. A quarter of passes are the whole blade and a
       quarter are under a third of it.

       NORMALISED BY REACH AND NOT BY PIXELS, or the scalar stops meaning
       anything the day reach changes — and `f.reachMul` is in it because
       Revenant's window is a per-fighter multiplier on exactly this number.

       `k` DRIVES WIDTH AND LIFE AND NOTHING ELSE. Damage and period stay flat.
       Driving all four is +6.1pp stronger and is four knobs riding one scalar,
       which leaves the bisection nothing to grab — width is what a viewer
       reads as size, life is what makes a deep cut still matter a minute
       later, and those are the two that say something. */
    const pen01 = clamp(P.maxPen / Math.max(1, f.w.reach * f.reachMul), 0, 1);
    const k = (u.kMin || 0.5) + ((u.kMax || 1.5) - (u.kMin || 0.5)) * pen01;

    const nx = P.wall === "W" ? 1 : P.wall === "E" ? -1 : 0;
    const ny = P.wall === "N" ? 1 : P.wall === "S" ? -1 : 0;

    /* THE BEARING — RICK'S RULE, AND IT IS THE BEST ARM MEASURED AS WELL AS
       THE ONE HE ASKED FOR: "everything should shoot into the room. but all 8
       directions are possible."

       It resolves with no special case. Of the eight compass bearings, keep
       those with an inward component: that is the perpendicular and the two
       diagonals that lean into the hall, and it drops exactly the two that run
       ALONG the wall the hole was torn from. Three bearings a wall, four
       walls, and all eight compass directions present in the game while no
       single hole ever fires into empty stone.

         into the room, 3 a wall   7.0 hits   81.9%   <- his
         even eight, parallels     5.1        71.9%
         straight across only      8.2        80.0%

       Ten points over the even eight, and it beats perpendicular-only, which
       is the arm the numbers alone would have chosen.

       DRAWN FROM `shellHash` AND NOT `this.rng()` — the house rule since
       Ironbloom's splinters: a relic that is not in the match must not be able
       to perturb the draw order of one that is, and a probe that pins a seed
       must get the same hall twice. */
    const idx = this.ventSeq = (this.ventSeq || 0) + 1;
    const pick = VENT_DIRS.filter(d => d[0] * nx + d[1] * ny > 0.01);
    const d = pick[Math.floor(shellHash(7717, idx) * pick.length) % pick.length];

    /* THE CAP DROPS THE OLDEST, not the newest. A cast that is still cutting
       should always be able to tear, and the hole that has had the most of its
       life is the one with the least left to lose. Same rule `shots`, `sparks`
       and the Thicket's vines all follow. */
    if (this.vents.length >= (u.maxVents || 8)) this.vents.shift();
    this.vents.push({
      own: f === this.a ? "a" : "b", wall: P.wall,
      u: (P.wall === "N" || P.wall === "S")
         ? clamp((P.hx - n) / Math.max(1, A.w - 2 * n), 0.02, 0.98)
         : clamp((P.hy - n) / Math.max(1, A.h - 2 * n), 0.02, 0.98),
      x: P.hx, y: P.hy, nx, ny, ax: d[0], ay: d[1],
      k, half: (u.half || 14) * k, life: (u.life || 9) * k,
      /* HOW LONG THE GASH IS, AS A FRACTION OF THE WALL, and it is stored the
         same way the position is and for the same reason: the inset walks
         0 -> 140, so a length in pixels stops describing the same stretch of
         wall by the end of the fight. Capped at a third of a wall — a blade
         that swept most of one is a pinned ball, not a cut. Presentation only:
         `drawVents` reads it and nothing else does. */
      span: clamp((P.hi - P.lo) / ((P.wall === "N" || P.wall === "S")
                                   ? Math.max(1, A.w - 2 * n)
                                   : Math.max(1, A.h - 2 * n)), 0, 0.34),
      t: 0, next: u.warm === undefined ? 0.35 : u.warm,
      fired: 0, front: null, spent: false, seq: idx,
    });
    V.tears++;

    this.spawnFx(P.hx + nx * 6, P.hy + ny * 6, AFFINITIES.dwarven.glow,
                 8 + ((k * 8) | 0), 190, 0.42, 2.6, nx, ny);
    this.ring(P.hx, P.hy, "#FF6A1A", 4, 34 + 26 * k, 0.34, 4);
    this.shake = Math.min(38, this.shake + 5);
    SFX.play("ult", { w: "cindercleave-tear" });
    /* RULE 3, ELEVENTH RELIC RUNNING. A hole opens on a wall through its own
       path, so nothing else in the frame knows it happened and `cinePlan`
       would score the best moments of this ultimate as empty air. The CAST
       files one and each TEAR files its own; the firings do not, which is the
       Thicket's `_cineVine` rule — five holes firing every 1.1s for nine
       seconds would be sixty beats and the director would see nothing else. */
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1,
                x: P.hx, y: P.hy, w: f.w.id,
                foeHpFrac: (f === this.a ? this.b : this.a).hp
                           / (f === this.a ? this.b : this.a).maxHp });
  }

  tickDeadfall(dt){'''),

# ------------------------------------------------------------ 5. the bearings
("VENT_DIRS", '''function shellHash(a, b){''',
 '''/* THE EIGHT COMPASS BEARINGS, and `tearVent` keeps the three that lean into
   the room. Module-level because the array is the same on every tear and a
   fresh one per tear would be eight allocations five times a cast for nothing.
   Read in exactly one place. */
const VENT_DIRS = [[1, 0], [0, 1], [-1, 0], [0, -1],
                   [0.7071, 0.7071], [0.7071, -0.7071],
                   [-0.7071, 0.7071], [-0.7071, -0.7071]];

function shellHash(a, b){'''),

# --------------------------------------------------------------- 6. the cast
("fireUlt.breach", '''    if (u.kind === "sigil"){''',
 '''    if (u.kind === "breach"){
      /* NOTHING RESOLVES HERE. The cast opens a LICENCE — for up to `cap`
         seconds the scythe tears the stone it is already inside — and what the
         ultimate IS happens on the cuts made inside it and on the holes those
         cuts leave behind. There is no radius test, no nova and no damage on
         this frame.

         NOT `seedfall`. The Thicket also puts things on these walls and waits,
         and the separations are structural rather than cosmetic: a vine
         REACHES INTO THE ROOM at a quarry that comes close and tracks it,
         where a vent fires a FIXED bearing across the whole hall whether or
         not anyone is near it. A vine is a limb; a vent is a hole. And the
         Thicket is SOWN — eight seeds leave the bow — where these are CUT, by
         a blade the viewer is already watching swing.

         `pass` STARTS NULL, so the first tear cannot land before the blade has
         been through the stone once. A licence that opened mid-cut would tear
         a hole out of a pass that began before the ultimate did. */
      f.ultBreach = { t: 0, cap: u.cap, n: u.n, tears: 0, pass: null };
      return;
    }

    if (u.kind === "sigil"){'''),

# --------------------------------------------------------- 7. the fx's length
("ultFx.life", '''              shroudmaul: 1.8,''',
 '''              shroudmaul: 1.8,
              /* CINDERCLEAVE IS THE BLADE LIGHTING, AND NOTHING MORE, for the
                 same reason Shroudmaul's entry is a burst: `m.ultFx` is ONE
                 SLOT and the opponent casting anything erases it (v54 §2a,
                 open item 25), so a fourteen-second licence hung there would
                 be art with a measured 0.0% chance of surviving an Ironhail.
                 The window lives on `f.ultBreach` and `f.breachFade`, the
                 holes live on `m.vents`, and both are drawn by `drawVents`
                 where nobody else can reach them. This field carries the
                 ignition and 1.6 is how long that takes. */
              cindercleave: 1.6,'''),

# ------------------------------------------------------- 8. the licence fades
("tickPresentation.breachFade", '''      f.graspFade = (f.ultGrasp || f.graspCrush) ? 1
                  : Math.max(0, f.graspFade - dt / 0.7);
    }''',
 '''      f.graspFade = (f.ultGrasp || f.graspCrush) ? 1
                  : Math.max(0, f.graspFade - dt / 0.7);
      /* AND THE LICENCE'S. Up instantly, down over 0.45s, so the blade cools
         rather than being switched off. HERE and not in `tickBreach` for
         v54's reason stated one relic along: a tear sets `hitStop`, and a
         presentation clock on the normal path freezes for exactly the frames
         the viewer is staring hardest at. */
      f.breachFade = f.ultBreach ? 1
                   : Math.max(0, f.breachFade - dt / 0.45);
    }'''),

# ----------------------------------------------------------- 9. the match ends
("decay.vents", '''    if (this.over && (this.a.ultBeam || this.b.ultBeam)){
      this.a.ultBeam = null; this.b.ultBeam = null;
    }''',
 '''    if (this.over && (this.a.ultBeam || this.b.ultBeam)){
      this.a.ultBeam = null; this.b.ultBeam = null;
    }
    /* AND THE HALL STOPS VENTING WHEN THE MATCH DOES, for the fourth time
       verbatim: `step()` returns from the `over` branch before `tickBreach` is
       reached, so holes left in the list would sit frozen on the walls — one
       of them mid-jet, a molten bar laid across the room — for the whole 2.4s
       the verdict panel is up, over the most legible moment in the match.

       THE HOLES OUTLIVE THE LICENCE AND THEY OUTLIVE THEIR CASTER. They do not
       outlive the match, and the asymmetry is the design's (§4.5): a hall still
       venting after the kill is a strong final image, and the verdict panel is
       not the place to put it. */
    if (this.over && this.vents.length){
      for (const v of this.vents)
        this.spawnFx(v.x + v.nx * 6, v.y + v.ny * 6, AFFINITIES.dwarven.core,
                     7, 150, 0.5, 3, v.nx, v.ny);
      this.vents.length = 0;
      this.a.ultBreach = null; this.b.ultBreach = null;
    }'''),

# ------------------------------------------------------ 10. the art, under
("draw.vents.under", '''    if (__emit) this.drawVines(m, false);''',
 '''    if (__emit) this.drawVines(m, false);
    /* the holes are IN the wall and the balls are in front of them */
    if (__emit) this.drawVents(m, false);'''),

# ------------------------------------------------------- 11. the art, over
("draw.vents.over", '''    this.drawVines(m, true);''',
 '''    this.drawVines(m, true);
    /* and a jet crosses the room, so it goes over what it crosses */
    this.drawVents(m, true);'''),

# ------------------------------------------------------------ 12. drawVents
("drawVents", '''  drawVines(m, over){''',
 '''  /* THE HALL IS THE WEAPON — four states, and one of them is the mechanic.

       THE CUT     the blade sweeps through the stone. This is where the SIZE
                   is decided, so the licence lights the blade: what a viewer
                   has to understand is that THIS weapon can do this now
       THE TEAR    the wall opens behind the blade as it leaves. Sized
       THE HOLE    dormant between firings, glowing, aimed — and brightening as
                   its next firing comes due, so the jet is PROMISED before it
                   arrives rather than appearing. v40's Thicket finding is the
                   precedent in Rick's own words
       THE JET     the front crosses the hall in 0.9s

     THE COUNT IS THE FIFTH THING THE ART HAS TO CARRY. A viewer should be able
     to tell the fourth tear from the fifth BEFORE the fifth lands, or the
     ultimate ends without ever having promised it — Grasp's four-knuckles
     problem, one relic on. Five chips ride the caster's shell and go out one
     per tear, which is a thing that can be watched rather than counted.

     THE WHITE IS THE FRONT AND NOT THE LENGTH, which is the one thing in this
     palette that can be got wrong permanently. Dwarven and sanctified were the
     closest pair in the game at CIEDE2000 8.05 and were separated on VALUE
     rather than hue to reach 21.19 — "a forge is not a treasury" — and
     sanctified is `#FFF6E2` on `#FFFFFF`. A white-hot jet body walks that
     straight back. So the body is carried in the Crucible's own `#FFB347` and
     `#FF6A1A`, which is dwarven-coded, shipped and measured, and the hot core
     is kept to a thin crescent at the head.

     Split `false`/`true` exactly as `drawVines` is, and for the same reason:
     the hall is BEHIND the two balls that own the health bars, and a jet is a
     strike and belongs over them. */
  drawVents(m, over){
    const lic = (m.a.ultBreach || m.a.breachFade > 0 ||
                 m.b.ultBreach || m.b.breachFade > 0);
    if (!(m.vents && m.vents.length) && !lic) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, R = CONFIG.physics.ballR;
    const L = Math.hypot(A.w, A.h);
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";

    /* ---- THE CUT, WHICH IS THE THING THE FIRST BUILD DID NOT HAVE.

       Rick: "the scythe should also have an animation showing it tear open the
       arena not just placing the breaches on the wall."

       He is right about what was on screen and about why it was wrong. A tear
       resolves at the END of a pass — that is the mechanic and it is not
       negotiable, because tearing on the first crossing frame samples the
       shallowest moment of the cut and leaves Rick's own size mechanic with no
       range. But nothing was DRAWN for the up-to-1.2 seconds a pass runs, so
       what a viewer saw was a hole appearing on a wall while a scythe happened
       to be near it. **The hall was placing the holes and the weapon was not.**

       So while a pass is open the wall carries a molten SCAR over exactly the
       stretch the blade has swept, brightening with how deep it has gone — and
       the tear then opens along that same stretch, because `v.span` is the
       same measurement. The cut and the hole are one event with two frames of
       it drawn instead of one.

       ON THE WALL AND THEREFORE UNDER BOTH BALLS, like the tear it becomes.
       Everything is derived from `P` and `m.t` and NOTHING is accumulated, so
       it steps with the 120Hz sim and does not strobe against the frame
       interpolator — and the sparks are drawn rather than spawned, because
       `spawnFx` draws from `this.rng()` and a picture must not move the
       simulation. */
    if (!over) for (const f of [m.a, m.b]){
      const V = f.ultBreach;
      if (!V || !V.pass) continue;
      const P = V.pass;
      if (!(P.hi > P.lo)) continue;
      const u2 = f.w.ult;
      const nx2 = P.wall === "W" ? 1 : P.wall === "E" ? -1 : 0;
      const ny2 = P.wall === "N" ? 1 : P.wall === "S" ? -1 : 0;
      const horiz = (P.wall === "N" || P.wall === "S");
      const wy = P.wall === "N" ? m.inset
               : P.wall === "S" ? A.h - m.inset : 0;
      const wx = P.wall === "W" ? m.inset
               : P.wall === "E" ? A.w - m.inset : 0;
      const ax2 = horiz ? P.lo : wx, ay2 = horiz ? wy : P.lo;
      const bx2 = horiz ? P.hi : wx, by2 = horiz ? wy : P.hi;
      /* HOW HOT THE SCAR IS, and it is the SAME scalar the tear will be sized
         by — so what the viewer watches getting brighter is what they then
         watch open. */
      const deep = clamp(P.maxPen / Math.max(1, f.w.reach * f.reachMul), 0, 1);
      const wid = 1.6 + 6.0 * deep;
      /* HOTTEST WHERE THE BLADE IS, COOLING BACK ALONG THE SWEEP. Drawn as two
         gradients meeting at the contact point rather than as one even bar —
         which is what the first cut was, and an even bar of amber laid on a
         wall reads as lava that is already there. The stone the blade left
         half a second ago has had half a second to cool, and saying so is the
         difference between "this weapon is cutting" and "this wall is lit".
         It is also what points at the contact: a viewer's eye goes to the
         bright end. */
      c.globalCompositeOperation = "lighter";
      c.shadowColor = "#FF6A1A"; c.shadowBlur = 9 * deep;
      for (const [ex, ey] of [[ax2, ay2], [bx2, by2]]){
        const gs = c.createLinearGradient(ex, ey, P.cx, P.cy);
        gs.addColorStop(0.00, "#FF6A1A00");
        gs.addColorStop(1.00, "#FF6A1A");
        c.globalAlpha = 0.24 + 0.42 * deep;
        c.strokeStyle = gs; c.lineWidth = wid;
        c.beginPath(); c.moveTo(ex, ey); c.lineTo(P.cx, P.cy); c.stroke();
        const gh = c.createLinearGradient(ex, ey, P.cx, P.cy);
        gh.addColorStop(0.00, "#FFB34700");
        gh.addColorStop(0.72, "#FFB34700");
        gh.addColorStop(1.00, "#FFB347");
        c.globalAlpha = 0.45 + 0.35 * deep;
        c.strokeStyle = gh; c.lineWidth = Math.max(1, wid * 0.40);
        c.beginPath(); c.moveTo(ex, ey); c.lineTo(P.cx, P.cy); c.stroke();
      }
      c.shadowBlur = 0;
      /* THE CONTACT POINT, where the blade is in the stone right now — the
         brightest thing in the cut, and the only white in it. */
      c.globalAlpha = 0.85;
      c.fillStyle = "#FFEFC9";
      c.beginPath();
      c.arc(P.cx + nx2 * 2, P.cy + ny2 * 2, 2.5 + 4.5 * deep, 0, TAU);
      c.fill();
      /* AND THE STONE COMING OFF IT. Drawn, not spawned: eight sparks whose
         phase is hashed and whose age is read off `m.t`, so they cost the
         simulation nothing and are identical on every replay. */
      for (let k3 = 0; k3 < 8; k3++){
        const ph = shellHash(6151, k3 + ((P.lo * 8) | 0));
        const age = (m.t * 2.4 + ph) % 1;
        const sp = 90 + 150 * shellHash(6163, k3);
        const spread = (shellHash(6173, k3) - 0.5) * 1.7;
        const dx2 = nx2 * Math.cos(spread) - ny2 * Math.sin(spread);
        const dy2 = nx2 * Math.sin(spread) + ny2 * Math.cos(spread);
        const r2 = age * sp * 0.30;
        c.globalAlpha = (1 - age) * 0.75 * (0.35 + 0.65 * deep);
        c.fillStyle = age < 0.4 ? "#FFEFC9" : "#FF8A2A";
        c.beginPath();
        c.arc(P.cx + dx2 * r2, P.cy + dy2 * r2 + age * age * 26,
              (1 - age) * 2.2 + 0.5, 0, TAU);
        c.fill();
      }
      c.globalAlpha = 1;
    }

    if (m.vents) for (const v of m.vents){
      const own = m[v.own];
      const per = Math.max(0.01, (own.w.ult.period || 1.1));
      const born = clamp(v.t / 0.20, 0, 1);
      const age  = clamp(v.t / Math.max(0.01, v.life), 0, 1);
      const cool = clamp((age - 0.78) / 0.22, 0, 1);
      const tx = -v.ny, ty = v.nx;                     // along the wall
      /* THE CHARGE. `next` runs down to the firing, so this runs UP to it. */
      const due = clamp(1 - v.next / per, 0, 1);

      if (!over){
        /* ---- THE TEAR, AND IT IS A BREAK IN THE WALL RATHER THAN A LAMP ON
           IT. Rick, off the first build: "they read as buttons and not as
           tears in the arena itself."

           He is describing what the first cut was: a filled ELLIPSE with a
           radial gradient in it, laid on top of the arena's own border. Every
           property of that shape says button — a smooth closed curve, a
           symmetric highlight, and an outline that does not disturb the line
           it is sitting on. What says TEAR is the opposite of all three:

             A JAGGED MOUTH        no two vents the same, and the roughness
                                   lives on the edge rather than in the fill
             THE WALL LINE BREAKS  the gash is painted in the hall's own
                                   background over the border stroke, so the
                                   boundary is visibly INTERRUPTED. A hole that
                                   does not break the line it is in is a decal
             IT RUNS ALONG THE CUT the length is the stretch of wall the blade
                                   actually swept (`v.span`), not a radius —
                                   so a long drag opens a long gash
             CRACKS                the stone fails past the ends of the tear,
                                   which is what makes it read as broken rather
                                   than as cut out

           Every jitter is `shellHash` off the vent's own sequence number, so a
           given tear is the same tear on every replay and on every machine —
           the house rule since Ironbloom's splinters, and the reason a probe
           that pins a seed gets the same hall twice. */
        const wlen = (v.wall === "N" || v.wall === "S")
                   ? Math.max(1, A.w - 2 * m.inset)
                   : Math.max(1, A.h - 2 * m.inset);
        /* THE LENGTH IS THE CUT, COMPRESSED. A scythe dragging along a wall
           can genuinely sweep a third of it, and a gash that long is not a
           tear — it is a missing wall section, which is what the first cut
           drew. So the swept extent still LENGTHENS the gash, and does so at a
           fifth of its true rate and against a hard ceiling: a long drag reads
           as a long tear without eating the hall. */
        const spanPx = (v.span || 0) * wlen;
        const hw = Math.min(v.half * 3.0, v.half * 0.90 + spanPx * 0.18)
                 * born * (1 - 0.26 * cool);
        const dpp = v.half * 0.66 * born * (1 - 0.30 * cool);
        c.save();
        c.translate(v.x, v.y);
        /* +x RUNS ALONG THE WALL AND +y RUNS INTO THE STONE, on all four
           walls and with no per-wall case: `tx = -ny` and `ty = nx`, so a
           rotation by `atan2(ty, tx)` maps local (0, 1) to (-ty, tx), which is
           exactly `-n`. The first cut multiplied a handedness term on top of
           that — and the term is CONSTANT at -1, so every tear was flipped
           inside out and the mouth bulged into the room. */
        c.rotate(Math.atan2(ty, tx));

        const NJ = 10;
        const room = [], deep = [];
        for (let i = 0; i <= NJ; i++){
          const q = i / NJ, xx = -hw + 2 * hw * q;
          /* THE MOUTH CLOSES TO A POINT AT BOTH ENDS. A gash with square ends
             is a slot; the taper is most of what makes it read as torn. */
          const e = Math.sin(Math.PI * q);
          const j1 = shellHash(4441, v.seq * 37 + i) - 0.5;
          const j2 = shellHash(4451, v.seq * 37 + i) - 0.5;
          room.push([xx, -dpp * (0.30 + 0.70 * e) * (1 + j1 * 1.1)]);
          deep.push([xx,  dpp * (0.55 + 1.00 * e) * (1 + j2 * 1.1)]);
        }
        const mouth = () => {
          c.beginPath();
          c.moveTo(room[0][0], room[0][1]);
          for (let i = 1; i <= NJ; i++) c.lineTo(room[i][0], room[i][1]);
          for (let i = NJ; i >= 0; i--) c.lineTo(deep[i][0], deep[i][1]);
          c.closePath();
        };

        /* 1. THE LINE BREAKS. The hall's own background, painted over the
              border stroke, so the boundary has a bite out of it. */
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 1;
        c.fillStyle = "#0E0A08";
        mouth(); c.fill();

        /* 2. THE BROKEN LIP, in stone rather than in light: a hard rim on the
              room side only, because that is the edge the viewer is looking
              at across the hall. */
        c.globalAlpha = 0.85 * (1 - 0.4 * cool);
        c.strokeStyle = SHAPES._shade(AFFINITIES.dwarven.dark, 1.7, 0.06);
        c.lineWidth = 2.0; c.lineJoin = "miter";
        c.beginPath();
        c.moveTo(room[0][0], room[0][1]);
        for (let i = 1; i <= NJ; i++) c.lineTo(room[i][0], room[i][1]);
        c.stroke();
        c.lineJoin = "round";

        /* 3. THE HEAT INSIDE IT, CLIPPED TO THE MOUTH so the glow cannot spill
              past the break and turn the tear back into a lamp. It sits DEEP —
              the light is coming from inside the mountain, not off the face. */
        c.save();
        mouth(); c.clip();
        c.globalCompositeOperation = "lighter";
        /* ACROSS THE DEPTH AND NOT OUT FROM A CENTRE. A radial of radius `hw`
           over a mouth three times as long as it is deep fills the whole thing
           with amber, and under `lighter` that buries the dark cavity the heat
           is supposed to be glowing INSIDE. The gradient runs from the room
           lip (nothing) to the deep edge (hot), so what the viewer sees is a
           break in the stone with fire a long way down it. */
        const g = c.createLinearGradient(0, -dpp * 0.9, 0, dpp * 1.5);
        g.addColorStop(0.00, "#FF6A1A00");
        g.addColorStop(0.42, "#FF6A1A");
        g.addColorStop(0.78, "#FFB347");
        g.addColorStop(1.00, "#FFEFC9");
        c.globalAlpha = (0.62 + 0.34 * due * due) * (1 - cool);
        c.fillStyle = g;
        c.fillRect(-hw * 1.2, -dpp * 2.2, hw * 2.4, dpp * 4.4);
        /* AND A SEAM ALONG THE DEEPEST LINE, so a long gash has a thread of
           molten rock running its length rather than an even wash. */
        c.globalAlpha = (0.72 + 0.28 * due) * (1 - cool);
        c.strokeStyle = "#FFB347";
        c.shadowColor = "#FF6A1A"; c.shadowBlur = 10;
        c.lineWidth = Math.max(1.4, dpp * 0.34);
        c.beginPath();
        for (let i = 0; i <= NJ; i++){
          const q = i / NJ, e = Math.sin(Math.PI * q);
          const yy = dpp * (0.30 + 0.60 * e)
                   * (1 + (shellHash(4457, v.seq * 41 + i) - 0.5) * 0.5);
          if (i === 0) c.moveTo(room[i][0], yy); else c.lineTo(room[i][0], yy);
        }
        c.stroke();
        c.shadowBlur = 0;
        c.restore();

        /* AND IT LIGHTS THE ROOM IT OPENED INTO. A soft wash just inside the
           mouth, unclipped and deliberately small: a break with fire behind it
           throws light, and a tear that is dark on the room side reads as
           damage rather than as a vent. It is the one thing here drawn OUTSIDE
           the clip, so it is kept low — the point is that the wall around the
           gash is warm, not that the gash is a lamp again. */
        c.globalCompositeOperation = "lighter";
        const gw = c.createRadialGradient(0, 0, 0, 0, 0, Math.max(6, hw * 0.9));
        gw.addColorStop(0.00, "#FF6A1A");
        gw.addColorStop(1.00, "#FF6A1A00");
        c.globalAlpha = (0.20 + 0.22 * due) * (1 - cool) * born;
        c.fillStyle = gw;
        c.beginPath();
        c.ellipse(0, -dpp * 0.15, hw * 0.95, dpp * 1.5, 0, 0, TAU);
        c.fill();

        /* 4. THE STONE FAILS PAST BOTH ENDS. Short jagged cracks running along
              the wall, dim, and they are what separate "torn" from "cut out".
              They do not glow: a crack is an absence. */
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 0.55 * born * (1 - 0.5 * cool);
        c.strokeStyle = "#0E0A08";
        c.lineWidth = 1.6;
        for (let sgn = -1; sgn <= 1; sgn += 2){
          for (let k2 = 0; k2 < 3; k2++){
            const h1 = shellHash(4463, v.seq * 53 + sgn * 7 + k2);
            const h2 = shellHash(4481, v.seq * 53 + sgn * 7 + k2);
            const len = hw * (0.35 + 0.75 * h1);
            c.beginPath();
            c.moveTo(sgn * hw * 0.92, (h2 - 0.5) * dpp * 0.5);
            c.lineTo(sgn * (hw * 0.92 + len * 0.55),
                     (h1 - 0.5) * dpp * 1.1);
            c.lineTo(sgn * (hw * 0.92 + len), (h2 - 0.5) * dpp * 1.6);
            c.stroke();
          }
        }
        c.restore();

        /* 5. AND WHICH WAY IT IS POINTED, which is the only thing about a
              dormant hole a viewer can act on. A stub of heat along the
              bearing, growing as the firing comes due, so the jet is PROMISED
              before it arrives rather than appearing. */
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = (0.14 + 0.36 * due * due) * (1 - cool) * born;
        c.strokeStyle = "#FF6A1A";
        c.lineWidth = Math.max(1.5, v.half * 0.34);
        c.shadowColor = "#FF6A1A"; c.shadowBlur = 10 * due;
        c.beginPath();
        c.moveTo(v.x, v.y);
        c.lineTo(v.x + v.ax * (10 + 26 * due), v.y + v.ay * (10 + 26 * due));
        c.stroke();
        c.shadowBlur = 0;
        continue;
      }

      /* ---- THE JET, ACROSS THE ROOM -------------------------------------
         Drawn from the hole to the front, with the half-width at every point
         EXACTLY the width the hit test uses — so the picture is a promise the
         simulation keeps rather than an illustration of it. What carries the
         "leaving" is alpha down the tail, not a narrower body.

         Rick's reference frame: a jet that tapers to nothing at its origin,
         swells along its length, and carries a bright crescent FRONT at the
         head. The taper pays for itself twice — it is his frame, and it means
         the HOLE can be small while the BEAM is wide, so the vent's size shows
         where the camera is looking instead of on a wall it often is not. */
      if (v.front === null || v.front === undefined) continue;
      /* IT IS ANCHORED WHILE IT ERUPTS AND THEN IT WITHDRAWS. Rick's frame is
         a jet that tapers to nothing AT ITS ORIGIN, which means the thing is
         attached to the hole — so while the front is still inside the hall the
         body runs from the wall to the head. Once the head is through the far
         side the tail follows it off, which is what stops a spent jet sitting
         across the room as a bar. A fixed-length slug does neither: early it
         reads as a projectile rather than an eruption. */
      const head = Math.min(v.front, L);
      const tail = Math.max(0, v.front - L);
      if (head <= tail) continue;
      const px = -v.ay, py = v.ax;
      /* THE HIT BOX. `tickBreach` calls this same expression. */
      const halfAt = (s2) => v.half
                          * (0.25 + 0.75 * clamp(s2 / (L * (own.w.ult.taperTo || 0.55)), 0, 1));

      /* ---- THE JET, MEASURED OFF RICK'S REFERENCE FRAME RATHER THAN GUESSED
         AT. Four cuts were spent inventing shapes and being told they were
         wrong, so this one is proportions taken off the photograph. In units
         of the body's half-width where it is widest, and running tail to head:

           0.00 - 0.45   a THREAD. Near-constant, about a sixth of the head's
                         width, and it barely grows. "It stays thin until the
                         end" is the whole first half of the picture
           0.45 - 0.88   the flare, and it is a SPEARHEAD: the sides open out
                         steadily and the white spine brightens inside them
           0.88 - 1.00   it comes back to a POINT. This is the part four cuts
                         got wrong — a shaft that ends in a rounded bulb is not
                         what the reference has and is not what anyone wants
                         on screen
           the ARC       radius about 2.4 of the head half-width, struck from
                         the head itself, spanning ~205 degrees and opening
                         BACKWARD. Its arms end roughly level with the white
                         core; they do not wrap round behind it
           inside it     DIM ORANGE and not black. The arc is a rim on a body
                         of flame, not a hoop in empty space

         THE TRAIL BEING THIN IS HONEST, which is the fact that makes the
         profile free. `half` is the hit box and everywhere else in this relic
         the drawing may not exceed it — but the resolution condition is
         `proj >= prev && proj <= front`, so THE ONLY WIDTH EVER TESTED IS THE
         ONE AT THE HEAD. A quarry behind the front has already been swept or
         already been missed. The head is drawn at the tested width; the trail
         behind it is decoration.

         THE LICKS ARE HASHED OFF `v.front`, so they crawl as the jet travels
         with no renderer-side clock — identical on every replay and every
         machine, the property `drawVines` gets from deriving off `v.t`. */
      const N = 26;
      const bucket = Math.floor(v.front / 24);
      const lick = (i2) => (shellHash(7727, v.seq * 131 + i2 * 17 + bucket)
                            - 0.5);
      const pt = [];
      for (let i2 = 0; i2 <= N; i2++){
        const q = i2 / N;
        const s2 = tail + (head - tail) * q;
        /* A MODEST CONE, WHICH IS WHAT THE SECOND REFERENCE HAS. Its jet
           leaves a hole in stone -- our own case, where the first reference
           was a flamethrower crossing frame -- and the shaft widens steadily
           from the wall to the head rather than running as a thread. What
           stops that reading as a shaft with a bulb on the end is that the
           HEAD is three times the shaft, and lobed. */
        let w = 0.20 + 0.80 * Math.pow(q, 1.5);
        /* and eased back over the last tenth so the billow is not sitting on
           a squared-off stump */
        w *= 1 - 0.30 * Math.pow(clamp((q - 0.90) / 0.10, 0, 1), 1.5);
        /* AND IT REACHES INTO THE BILLOW. The frill is struck from the head,
           so a shaft that stops at the head leaves a dark socket in the middle
           of it — which is what the first lobed cut drew. The reference has
           the shaft's fire meeting the frill from inside. */
        pt.push([v.x + v.ax * s2, v.y + v.ay * s2, halfAt(s2), q, w,
                 lick(i2)]);
      }

      const ribbon = (wf, col, al, blur) => {
        c.beginPath();
        for (let i2 = 0; i2 <= N; i2++){
          const q = pt[i2], w2 = wf(q, false);
          if (i2 === 0) c.moveTo(q[0] + px * w2, q[1] + py * w2);
          else c.lineTo(q[0] + px * w2, q[1] + py * w2);
        }
        for (let i2 = N; i2 >= 0; i2--){
          const q = pt[i2], w2 = wf(q, true);
          c.lineTo(q[0] - px * w2, q[1] - py * w2);
        }
        c.closePath();
        const gg = c.createLinearGradient(pt[0][0], pt[0][1],
                                          pt[N][0], pt[N][1]);
        gg.addColorStop(0.00, col + "00");
        gg.addColorStop(0.30, col + "66");
        gg.addColorStop(1.00, col);
        c.globalAlpha = al;
        c.shadowColor = col; c.shadowBlur = blur;
        c.fillStyle = gg;
        c.fill();
        c.shadowBlur = 0;
      };

      const hx2 = pt[N][0], hy2 = pt[N][1];
      /* THE HEAD'S WIDTH IS TAKEN WHERE THE BODY IS WIDEST, not at the tip —
         the tip is a point, and sizing the arc off a point makes it vanish. */
      const hw = halfAt(tail + (head - tail) * 0.90);
      const ang = Math.atan2(v.ay, v.ax);
      const hr = Math.max(19, hw * 3.20);

      c.globalCompositeOperation = "lighter";

      /* 1. THE DIM INTERIOR, first and underneath everything: the arc is a rim
            on a body of flame and not a hoop in empty space. */
      c.save();
      c.translate(hx2 - v.ax * hr * 0.12, hy2 - v.ay * hr * 0.12);
      const gi = c.createRadialGradient(0, 0, 0, 0, 0, hr);
      gi.addColorStop(0.00, "#FF6A1A");
      gi.addColorStop(0.55, "#FF6A1A55");
      gi.addColorStop(1.00, "#FF6A1A00");
      c.globalAlpha = 0.30;
      c.fillStyle = gi;
      c.beginPath(); c.arc(0, 0, hr, 0, TAU); c.fill();
      c.restore();

      /* 2. THE ENVELOPE — soft, ragged, the one layer allowed outside the hit
            box because it is flame fringe with no hard edge in it. */
      ribbon((q, b) => q[2] * q[4] * 1.30 * (1 + (b ? -q[5] : q[5]) * 0.50)
                     + (b ? -q[5] : q[5]) * 2.0,
             "#FF6A1A", 0.44, 15);
      /* 3. THE BODY. */
      ribbon((q, b) => q[2] * q[4] * 0.80 * (1 + (b ? -q[5] : q[5]) * 0.28)
                     + (b ? -q[5] : q[5]) * 1.2,
             "#FFB347", 0.60, 8);
      /* 4. THE SPINE, and it is LONG and THIN rather than a blob at the nose —
            the reference runs white from about the halfway point forward. §7a
            holds: the white is the front, and the length is amber. */
      ribbon((q, b) => q[2] * q[4] * 0.36
                     * clamp((q[3] - 0.34) / 0.66, 0, 1)
                     * (1 + (b ? -q[5] : q[5]) * 0.22),
             "#FFE3B4", 0.62, 7);

      /* 5. THE FILAMENTS. Fire is fibrous and a filled ribbon is not; six
            streaks trailing back off the head at hashed offsets are most of
            what separates flame from an airbrush. */
      c.strokeStyle = "#FFB347";
      c.lineCap = "round";
      for (let f2 = 0; f2 < 6; f2++){
        const off = (shellHash(7741, v.seq * 53 + f2 + bucket * 3) - 0.5) * 2;
        const a0 = 0.50 + 0.30 * shellHash(7753, v.seq * 53 + f2);
        c.globalAlpha = 0.40 * (0.4 + 0.6 * Math.abs(off));
        c.lineWidth = Math.max(0.8, hw * 0.13);
        c.beginPath();
        for (let i2 = Math.floor(N * a0); i2 <= N; i2++){
          const q = pt[i2];
          const o2 = off * q[2] * q[4] * 0.95;
          const xx = q[0] + px * o2, yy = q[1] + py * o2;
          if (i2 === Math.floor(N * a0)) c.moveTo(xx, yy); else c.lineTo(xx, yy);
        }
        c.stroke();
      }

      /* 6. THE BILLOW, AND IT IS SCALLOPED RATHER THAN SMOOTH.

         Rick's second reference is the one that settles this: a jet erupting
         from a hole in a stone wall, which is our own case rather than an
         analogy. Its head is not an arc — it is a ring of ROUNDED LOBES, six
         to nine of them, overlapping like the frill of a mushroom, and that
         internal structure is the entire difference between fire that is
         ROLLING and a bright curve that is sitting still. Five previous cuts
         drew a stroked arc of one width or another and every one of them read
         as a lens flare, because a stroked arc has no inside.

         So the crescent is built as overlapping filled lobes on an arc, each
         one a soft radial that falls off to nothing, smaller toward the tips.
         `lighter` does the rest: where two lobes overlap they brighten, which
         is what gives the frill its seams for free.

         AND THE PALETTE COMES BACK TOWARD AMBER. The reference is gold almost
         throughout with white only in the very hottest part of the head — §7a
         was right and the last three cuts had drifted whiter than it. */
      const LOB = 9;
      const SPAN = 3.30;
      c.save();
      c.translate(hx2 - v.ax * hr * 0.10, hy2 - v.ay * hr * 0.10);
      c.rotate(ang);
      for (let i2 = 0; i2 < LOB; i2++){
        const q2 = LOB === 1 ? 0.5 : i2 / (LOB - 1);
        const a2 = -SPAN / 2 + SPAN * q2;
        const hsh = shellHash(7789, v.seq * 97 + i2 + bucket);
        /* the lobes sit on the arc, and the ones at the tips are smaller —
           the frill thins into its own ends */
        const hs2 = shellHash(7793, v.seq * 97 + i2 * 3 + bucket);
        /* THE SPACING JITTERS TOO. Lobes on even angular centres at one radius
           are a croissant; the reference's frill is uneven in both. */
        const aj = a2 + (hs2 - 0.5) * (SPAN / LOB) * 0.55;
        const ring = hr * (0.70 + 0.20 * hsh)
                   * (0.62 + 0.38 * Math.sin(Math.PI * q2));
        const lx = Math.cos(aj) * ring, ly = Math.sin(aj) * ring;
        const lr = hr * (0.26 + 0.24 * hs2)
                 * (0.55 + 0.45 * Math.sin(Math.PI * q2));
        /* THREE FLAT DISCS AND NOT A GRADIENT. `createRadialGradient` is
           the one performance trap this file has already been bitten by, and
           the engine's own grain cache carries the note: nine of them per
           relic per frame "was the single cause of the stutter Rick
           reported". Nine lobes across up to eight live vents is SEVENTY-TWO
           gradient objects a frame. Under `lighter` three concentric solid
           discs build the same falloff for none of the cost. */
        c.globalAlpha = 0.22;
        c.fillStyle = "#FF6A1A";
        c.beginPath(); c.arc(lx, ly, lr, 0, TAU); c.fill();
        c.globalAlpha = 0.26;
        c.fillStyle = "#FFB347";
        c.beginPath(); c.arc(lx, ly, lr * 0.70, 0, TAU); c.fill();
        c.globalAlpha = 0.30;
        c.fillStyle = "#FFD79A";
        c.beginPath(); c.arc(lx, ly, lr * 0.38, 0, TAU); c.fill();
      }
      /* AND A RIM ON THE OUTSIDE OF THE FRILL, thin, so the billow has an edge
         the eye can follow round. It scallops with the lobes because it is
         struck on the same radii. */
      c.globalAlpha = 0.30;
      c.strokeStyle = "#FFC978";
      c.shadowColor = "#FFB347"; c.shadowBlur = 8;
      c.lineCap = "round";
      c.lineWidth = Math.max(0.8, hw * 0.15);
      const M2 = 40;
      c.beginPath();
      for (let i2 = 0; i2 <= M2; i2++){
        const q2 = i2 / M2;
        const a2 = -SPAN / 2 + SPAN * q2;
        const lobe = q2 * (LOB - 1);
        const hsh = shellHash(7789, v.seq * 97 + Math.round(lobe) + bucket);
        const rr = hr * (0.74 + 0.10 * hsh)
                 * (0.62 + 0.38 * Math.sin(Math.PI * q2))
                 + hr * (0.30 + 0.14 * hsh)
                 * (0.55 + 0.45 * Math.sin(Math.PI * q2)) * 0.72;
        const xx = Math.cos(a2) * rr, yy = Math.sin(a2) * rr;
        if (i2 === 0) c.moveTo(xx, yy); else c.lineTo(xx, yy);
      }
      c.stroke();
      c.shadowBlur = 0;
      c.restore();

      /* 7. THE SPARKS, AND THEY ARE THE THING THE STILL COULD NOT SHOW.

         Rick's second reference is eight seconds of a jet playing on a stone
         wall, and what the photograph leaves out is that most of what a viewer
         reads as FIRE is not the ribbon — it is the cloud of point sparks
         spraying off it, arcing out and falling. The ribbon on its own is a
         lit shape; the sparks are what make it burn.

         EVERY ONE IS DERIVED AND NONE IS SPAWNED. A spark is born where the
         FRONT passed, so its age is `(head - birth) / speed` — no stored
         state, no per-frame integration, nothing in `m.fx`, and above all no
         `this.rng()`, which would move the simulation and re-invalidate the
         blade for the third time. Hashed off the vent's own sequence number,
         so a given jet throws the same sparks on every replay and on every
         machine.

         THEY FALL. `+ 300 * age * age` is the only place in this drawing that
         knows which way is down, and it is what stops the spray reading as a
         starburst. */
      const spd2 = Math.max(1, own.w.ult.speed || 1100);
      for (let k3 = 0; k3 < 52; k3++){
        const h1 = shellHash(7757, v.seq * 211 + k3);
        const h2 = shellHash(7761, v.seq * 211 + k3);
        const h3 = shellHash(7769, v.seq * 211 + k3);
        /* born along the part the front has already crossed, biased hard
           toward the head — which is where the reference throws most of them */
        const bs = head * (0.30 + 0.70 * Math.pow(h1, 0.55));
        const age = (head - bs) / spd2 + h3 * 0.05;
        if (age > 0.55) continue;
        /* FORWARD-BIASED. The first cut had the lateral term four times the
           forward one, so every spark left the jet at ninety degrees and the
           spray read as tally marks down the shaft. The reference throws them
           ahead and out. */
        const lat = (h2 - 0.5) * 300;
        const fwd = 150 + 420 * h3;
        const ex = v.x + v.ax * (bs + fwd * age) + px * lat * age;
        const ey = v.y + v.ay * (bs + fwd * age) + py * lat * age
                 + 300 * age * age;
        const fade = 1 - age / 0.55;
        /* a STREAK and not a dot: a spark moving at a few hundred units a
           second is a line at 60fps, and drawing it as a point is the same
           mistake as drawing a jet with no duration */
        const sx2 = v.ax * fwd + px * lat;
        const sy2 = v.ay * fwd + py * lat + 600 * age;
        const sl = Math.hypot(sx2, sy2) || 1;
        /* AN EMBER AND NOT A TALLY MARK. Uniform white dashes read as
           hatching; the reference's sparks are warm, uneven, and each one
           carries a little of its own light. Length varies with the spark's
           own hash so the spray is not a comb. */
        const len2 = (1.2 + 6 * fade * (0.45 + 0.9 * h2)) * v.k;
        c.globalAlpha = fade * 0.9;
        c.strokeStyle = fade > 0.68 ? "#FFF0CC"
                      : fade > 0.34 ? "#FFB347" : "#FF7A18";
        c.lineWidth = Math.max(0.6, 1.3 * fade * v.k);
        /* NO SHADOW ON A SPARK. `shadowBlur` is the most expensive thing a 2D
           context does and there are up to sixty-four of these per vent; at
           arena scale a two-pixel ember's halo is invisible and the capture
           was paying eight times over for it. */
        c.beginPath();
        c.moveTo(ex, ey);
        c.lineTo(ex - (sx2 / sl) * len2, ey - (sy2 / sl) * len2);
        c.stroke();
      }
      c.shadowBlur = 0;
    }

    /* ---- THE LICENCE, ON THE CASTER --------------------------------------
       Only in the `over` pass: the blade is drawn over the ball that swings
       it, so heat laid under it would be behind the thing it is heating. */
    if (over) for (const f of [m.a, m.b]){
      const fade = f.breachFade || 0;
      if (fade <= 0) continue;
      const V = f.ultBreach;
      const N2 = V ? V.n : (f.w.ult ? f.w.ult.n : 5) || 5;
      const left = V ? Math.max(0, V.n - V.tears) : 0;
      c.globalCompositeOperation = "lighter";
      /* THE BLADE IS MOLTEN, which is the sentence the ultimate is made of:
         this weapon can cut the walls NOW. Drawn off `m.bladeSegments`, so it
         is exactly the segment the tear is tested against — and it returns
         nothing while the Winnowing is running, which is another relic's
         window and correct here by construction. */
      for (const s of m.bladeSegments(f)){
        const gb = c.createLinearGradient(s.ax, s.ay, s.bx, s.by);
        gb.addColorStop(0.00, "#FF6A1A00");
        gb.addColorStop(0.55, "#FF6A1A");
        gb.addColorStop(1.00, "#FFB347");
        c.strokeStyle = gb;
        c.lineWidth = 8 * fade;
        c.globalAlpha = 0.50 * fade;
        c.shadowColor = "#FF6A1A"; c.shadowBlur = 18 * fade;
        c.beginPath(); c.moveTo(s.ax, s.ay); c.lineTo(s.bx, s.by); c.stroke();
      }
      c.shadowBlur = 0;
      /* THE COUNT. Five chips on the shell, one going dark per tear, so the
         fifth is visible as the last one BEFORE it lands. */
      for (let i = 0; i < N2; i++){
        const a2 = -Math.PI / 2 + (i - (N2 - 1) / 2) * 0.34;
        const rx = f.x + Math.cos(a2) * (R + 12);
        const ry = f.y + Math.sin(a2) * (R + 12);
        const on = i < left;
        c.save();
        c.translate(rx, ry);
        c.rotate(a2 + Math.PI / 2);
        c.globalAlpha = fade * (on ? 0.95 : 0.30);
        c.fillStyle = on ? "#FFB347" : "#5A3A1C";
        if (on){ c.shadowColor = "#FF6A1A"; c.shadowBlur = 9; }
        c.beginPath();
        c.moveTo(0, -4.4); c.lineTo(2.1, 0); c.lineTo(0, 4.4); c.lineTo(-2.1, 0);
        c.closePath(); c.fill();
        c.restore();
      }
      c.shadowBlur = 0;
    }
    c.globalAlpha = 1;
    c.globalCompositeOperation = "source-over";
    c.restore();
  }

  drawVines(m, over){'''),

# ------------------------------------------------------- 13. the charge lands
("charge", '''    ult:{ name:"%ULT%", charge:1e9, kind:"breach",''',
 '''    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"breach",'''),
]


# ============================================================ STAGE 3 =======
# THE JETS. The front, the taper, the sunder — and the count of five closing
# the window, which is the clause the tip promises and the balance rests on.
S3 = [

# ------------------------------------------------------------- 1. the jets
("jets", '''      /* ---- THE JETS. STUBBED IN STAGE 2, and that is the point of the stage:
         the pass, the tear and the size are the half of this design that can
         be falsified against a published distribution before a single beam is
         drawn. Stage 3 replaces this block. ---- */''',
 '''      const own = v.own === "a" ? this.a : this.b;
      const foe = v.own === "a" ? this.b : this.a;
      const u = own.w.ult;
      const L = Math.hypot(A.w, A.h);

      /* THE FRONT, AND IT IS THE MECHANIC AND NOT THE DECORATION.

         `front` is null between firings; a firing sets it to 0 and it walks
         out along the bearing at `speed`. The quarry is caught when the front
         SWEEPS PAST its projection — the interval [previous front, this front]
         — so a fast front cannot step over a ball between frames, and a slow
         one can genuinely be left behind.

         Resolving the whole line at once instead is +4.2pp stronger and it is
         the version Rick already rejected on a different relic: v40's Thicket,
         "the vines look stationary and damage the enemy ball when it happens
         to run into them". A strike with no duration reads as a hazard you
         walked into. 1100 units a second crosses the hall in about 0.9s and
         EVERY speed from 650 to 1800 measures the same, so this number is
         chosen for the look and nothing else.

         `spent` IS PER FIRING, not per hole: one payment a jet, and the next
         jet out of the same hole is a fresh one. */
      if (v.front !== null){
        const prev = v.front;
        v.front += u.speed * dt;
        if (v.front > L + 380){ v.front = null; }
        else if (foe.alive && !v.spent && !this.over){
          const px = foe.x - v.x, py = foe.y - v.y;
          const proj = px * v.ax + py * v.ay;
          /* THE TAPER, AND THE TESTED VOLUME IS THE DRAWN ONE. `drawVents`
             calls the same expression, so a jet that looks like it missed
             did. It pays for itself twice: it is Rick's reference frame, and
             it lets the HOLE be small while the beam is wide, so the vent's
             size shows where the camera is looking. */
          const wid = v.half * (0.25 + 0.75
                    * clamp(proj / (L * (u.taperTo || 0.55)), 0, 1));
          if (proj >= prev && proj <= v.front &&
              Math.abs(px * v.ay - py * v.ax) <= wid + R){
            v.spent = true;
            this.jetHit(v, own, foe);
          }
        }
      }

      v.next -= dt;
      if (v.next > 0) continue;
      v.next = u.period;
      v.fired++;
      v.front = 0; v.spent = false;
      this.spawnFx(v.x + v.nx * 5, v.y + v.ny * 5, "#FFB347",
                   6 + ((v.k * 5) | 0), 260, 0.30, 2.2, v.ax, v.ay);
      SFX.play("ult", { w: "cindercleave-jet" });''' ),

# ------------------------------------------------------------ 2. what it does
("jetHit", '''  tickDeadfall(dt){''',
 '''  /* WHAT A JET IS WORTH, AND THE DAMAGE IS THE SMALLER HALF OF IT.

       beams apply 1 Sunder      71.9%   +28.5%
       beams apply NOTHING       61.9%   +18.5%      and land MORE hits

     The no-sunder arm lands 7.3 hits a fight against 6.3 and is ten points
     worse. The beams' damage is worth +1.9pp over the floor; the Sunder they
     apply is worth +10.0pp on top of the same beams. BREACH IS NOT A DAMAGE
     ULTIMATE — it is a second contact rate running underneath a slow weapon,
     and it carries the relic across `sunder_survey`'s 5.0s line for as long as
     the holes are open.

     Which is why the application is NOT scaled by size or by damage: 2 stacks
     a hit is worth +1.1pp over 1, flat, and it is not a knob.

     FOE ONLY, and it is a decision rather than an accident. Measured, beams
     that burn their caster too take the relic from +28.5% to +3.8%, because a
     scythe has to fight near walls to tear anything and therefore stands in
     its own fire. That is a different relic, not a balance term.

     AND THERE IS NO `self === owner` GUARD, ever. The side is decided by
     CONSTRUCTION rather than by a test: `v.own` is the caster's side and `foe`
     is read off it, so there is no comparison here to get backwards. v51 §4.3
     is why that matters — a caster guard written the obvious way made 9.3
     blows a fight invisible on a different relic.

     ── AND A JET DOES NOT CATCH A SHADE. THAT IS A DECISION ────────────────

     Design §4.8 asked for a rule and offered "yes, like any other body" as its
     placeholder. This is the other answer, for two reasons and not for
     convenience.

     THE PRECEDENT SAYS QUARRY ONLY. Every payload in this game that resolves
     outside `resolveHit` reads the real fighter and nothing else — the
     Deadfall's mines test `g.src === "a" ? this.b : this.a` and no shade has
     ever set one off. `tickShadeHits` exists precisely because the ordinary
     hit loop does not offer a copy as a target, and nothing has been added to
     it since.

     AND NOTHING PRICED IT. Every number in `06-docs/v57/` is measured against
     the real quarry; `spent` is ONE payment per firing, so a jet that swept
     three bodies would either pay once into whichever it met first — which
     makes a Twinshade window a shield — or pay three times, which is a
     damage multiplier nobody measured. Both are knobs, and picking one from
     a comment is how a relic acquires an unpriced clause.

     `breach_relic_probe [6]` asserts it either way, so the day Rick wants the
     other answer the check moves with the code. */
  jetHit(v, own, foe){
    const u = own.w.ult;
    /* ROUNDED, because every damage number in this engine is an integer and
       this one gets printed over a ball. `dmgTakenMul` is the quarry's own
       Sunder — including whatever this relic's earlier jets put there, which
       is the compounding the design is built on. */
    const dmg = Math.round((u.jetDmg || 9) * foe.dmgTakenMul());
    if (dmg > 0){
      this.hurt(foe, dmg, own);
      own.dealt += dmg;
      /* `hits` is deliberately NOT incremented: a jet does not go through
         `resolveHit`, and verify's "no pairing resolves on fewer than 6 hits"
         floor is about BLOWS LANDED, which this is not. Same call as the
         Deadfall's mines, one relic along. */
      foe.flash = 1; foe.ringFlash = 1;
      this.float(foe.x, foe.y - 40, dmg, AFFINITIES.dwarven.glow,
                 30 + dmg * 0.6);
    }
    /* THE SUNDER LANDS AFTER THE DAMAGE, so a jet does not amplify itself. */
    const firstTeach = !this.taught.sunder
                     && !!(STATUS.sunder && STATUS.sunder.tip);
    if (firstTeach) this.taught.sunder = true;
    foe.apply("sunder", u.sunderN || 1);
    this.statusTag(foe.x, foe.y, "sunder", firstTeach);

    /* THE SHOVE, ALONG THE JET'S OWN BEARING — off the wall and into the
       room. Rick's, and the direction is the Thicket's rule rather than a
       choice: `resolveHit`'s built-in knock fires away from the CASTER, and
       this hazard is not the caster, so a shove borrowed from that function
       would push the quarry along a line nothing on screen is drawn on.

       AFTER the damage and BEFORE the fatal test, so a killing jet still
       throws the corpse — `killFlight` is what carries a slain ball into the
       wall it shatters against, and a kill that landed with no push would end
       the fight on a ball standing still. */
    if (foe.alive && (u.jetKnock || 0) > 0){
      foe.vx += v.ax * u.jetKnock;
      foe.vy += v.ay * u.jetKnock;
    }

    const fatal = !foe.alive;
    if (fatal){
      /* A JET THAT ENDS THE FIGHT CARRIES THE FIGHT'S OWN WEIGHT. `resolveHit`
         swaps its hit-stop for `killStop` and arms `finisher` on a fatal blow;
         anything landing outside that function has to do it itself or this
         ultimate's killing blow is lighter than a swing. */
      this.hitStop = Math.max(this.hitStop, CONFIG.impact.killStop);
      this.finisher = 1.0;
    } else {
      /* SMALL ON PURPOSE. Five holes at 1.1s can put several of these inside
         a second, and a full hit-stop each would freeze the hall solid — the
         Deadfall's first build made exactly that mistake in reverse. */
      this.hitStop = Math.max(this.hitStop, 0.04);
    }
    this.shake = Math.min(38, this.shake + (fatal ? 20 : 8));
    this.spawnFx(foe.x, foe.y, "#FFB347", 14, 240, 0.45, 3,
                 v.ax, v.ay);
    SFX.play("ult", { w: "cindercleave-burn" });
    /* THE FIRINGS DO NOT FILE A BEAT — the Thicket's `_cineVine` rule, and
       sixty of them a cast would drown every other beat in the fight.

       AND THE FATAL ONE DOES, WHICH IS THE WHOLE OF v53 §4. `cinema_clip`
       finds the killing blow with `plan.find(c => c.fatal)` and NOTHING on an
       `ult` beat carries that flag. Measured on Gravemourn before this line
       existed there: 30 of 58 kills were landed by a hand and ALL THIRTY
       rendered a clip with no killing blow. Unlike Grasp, this ultimate deals
       damage and therefore CAN kill, so it must file one. */
    if (fatal)
      this.beat({ kind: "hit", side: own === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, dmg, crit: false, fatal: true,
                  hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                  selfHpFrac: own.hp / own.maxHp,
                  spd: own.speed, foeSpd: foe.speed,
                  close: Math.hypot(own.vx - foe.vx, own.vy - foe.vy) });
  }

  tickDeadfall(dt){'''),

# ---------------------------------------------------------- 3. the four voices
("sfx", '''        } else if (w === "nightfell-stamp"){''',
 '''        } else if (w === "cindercleave"){       // the blade is licensed
          /* THE CAST IS A WINDOW OPENING, so like Deadfall's and Grasp's it
             does not resolve — nothing has happened yet. This is IGNITION: a
             low forge rush with the blade coming up to heat over it, and it
             deliberately does not land on a beat, because the first cut has
             not been made when the sound ends. */
          this._tone (t, { freq: 58, to: 128, gain: 0.27, dur: 1.00, type:"sawtooth" });
          this._burst(t, { freq: 400, q: 0.5, gain: 0.24, dur: 0.55, type:"lowpass" });
          this._tone (t + 0.06, { freq: 180, to: 520, gain: 0.12, dur: 0.80, type:"triangle" });
          this._burst(t + 0.10, { freq: 3200, q: 1.1, gain: 0.09, dur: 0.45, type:"highpass" });
        } else if (w === "cindercleave-tear"){  // stone opens behind the blade
          /* FIVE OF THESE A CAST, so it is short by design — but it is the
             loudest of the three small voices, because the tear is the event
             the count is made of and a viewer has to be able to hear the
             fifth one arrive. Rock giving way, then heat behind it. */
          this._burst(t, { freq: 900, q: 0.8, gain: 0.22, dur: 0.13, type:"bandpass" });
          this._tone (t, { freq: 300, to: 88, gain: 0.18, dur: 0.24, type:"sawtooth" });
          this._burst(t + 0.05, { freq: 260, q: 0.5, gain: 0.16, dur: 0.34, type:"lowpass" });
        } else if (w === "cindercleave-jet"){   // a hole spits
          /* QUIET AND SHORT, and it is the one that fires most — up to five
             holes every 1.1 seconds for nine seconds. A gas ignition: a click
             of pressure and a rush behind it, nothing like the tear that made
             the hole and nothing like the burn that lands. Vesper's
             pass-against-tip pair is the precedent and it is the same
             problem. */
          this._burst(t, { freq: 1700, q: 1.6, gain: 0.09, dur: 0.05, type:"bandpass" });
          this._burst(t + 0.01, { freq: 700, q: 0.6, gain: 0.11, dur: 0.30, type:"lowpass" });
          this._tone (t, { freq: 420, to: 900, gain: 0.07, dur: 0.20, type:"triangle" });
        } else if (w === "cindercleave-burn"){  // and something was in it
          /* THE PAYMENT. It has to cut through a 0.04s hit-stop and it has to
             be distinguishable from the jet that carried it, because the ONE
             thing a viewer has to learn from this ultimate is which jets
             connected. A hiss with a low body under it and a bright crack on
             top.

             NO BURST IS LONGER THAN 0.6s. CLAUDE.md §4.5: `_burst` does not
             loop its 0.6s noise buffer, so anything longer plays silence for
             its tail. */
          this._burst(t, { freq: 3600, q: 0.9, gain: 0.20, dur: 0.18, type:"highpass" });
          this._tone (t, { freq: 210, to: 62, gain: 0.22, dur: 0.30, type:"sine" });
          this._burst(t + 0.01, { freq: 240, q: 0.5, gain: 0.20, dur: 0.34, type:"lowpass" });
          this._tone (t + 0.02, { freq: 640, to: 150, gain: 0.12, dur: 0.22, type:"sawtooth" });
        } else if (w === "nightfell-stamp"){'''),

# ------------------------------------------------------- 4. the count closes it
("count", '''      /* THE TWO WAYS OUT IN THIS STAGE, AND THE COUNT IS NOT ONE OF THEM YET.
         "The FIFTH cut ends it" lands in stage 3 with the jets, so every pass
         that closes here tears — which is what the distribution gate wants,
         because a licence that stopped at five would throw away most of the
         passes it is supposed to be measured over. */
      const done = V.t >= V.cap || !f.alive;''',
 '''      /* THE FIFTH TEAR ENDS IT, AND THAT CLAUSE IS THE BALANCE. Rick's own
         count, and what it buys is a relic whose every cast is worth exactly
         the same thing: the clock version's worth was CONTACT RATE, so a cast
         spent near a wall tore twice what a cast spent mid-arena tore, and two
         casts of the same ultimate in one fight were not the same ultimate. It
         also gives the thing a number a viewer can hold, which is what the
         chips on the shell are for. GRASP's third grab is the precedent and it
         is one build old.

         THE CAP IS A GUARD RAIL BEHIND IT AND IT IS NOT COUNTED HERE.
         `breach_relic_probe [2]` has to report how often the cap was the thing
         that ended a window — if it is more than one in fifty, `n` is not
         reachable and the DESIGN changes rather than the number — and the
         first cut of this line kept a `byCap` tally on the licence for it to
         read. Nothing in the engine ever read that field: the licence is
         nulled on the same frame it is incremented, so the only reader
         possible is a probe that snapshots the object anyway, which is what
         the probe does. A counter written and never read is open item 13's
         `s.snap` in a new costume, and this is one relic too soon to add a
         second instance of it. */
      const spent = V.tears >= V.n;
      const done = spent || V.t >= V.cap || !f.alive;'''),

# ------------------------------------------------------- 5. and it is exact
("count.guard", '''    /* A TEAR WITHOUT A LICENCE IS A SCYTHE DOING WHAT A SCYTHE DOES, which is
       standing in a wall on most of every rotation. The count joins this
       guard in stage 3. */
    if (!V) return;''',
 '''    /* A TEAR WITHOUT A LICENCE IS A SCYTHE DOING WHAT A SCYTHE DOES, which is
       standing in a wall on most of every rotation.

       AND THE COUNT IS AN INVARIANT RATHER THAN A RUNNING TOTAL. The tip says
       five and means it; `breach_relic_probe [1]` counts the tears off events
       instead of recomputing them, and this line is what makes that check
       about the mechanic rather than about arithmetic. Without it there is
       exactly one path to a sixth hole: the fifth tear coming from a wall
       CHANGE, which closes one pass and opens another on the same frame, and
       the window then ending on the next frame with that new pass in hand. */
    if (!V || V.tears >= V.n) return;'''),
]


# THE FX SPEC. The inlined copy and `src/render/fx.js` must stay one object.
FX_ANCHOR = """    shroudmaul: { mode: 'burst', n: 820, sp: [40, 260], grav: 210, drag: 2.6,
                  life: [0.35, 1.05], heavy: 0.10, size: [0.6, 2.2],
                  spawn: 0.14, up: 0, atSelf: 1 }"""

FX_NEW = """    shroudmaul: { mode: 'burst', n: 820, sp: [40, 260], grav: 210, drag: 2.6,
                  life: [0.35, 1.05], heavy: 0.10, size: [0.6, 2.2],
                  spawn: 0.14, up: 0, atSelf: 1 },
    /* BREACH IGNITES A BLADE, AND `atSelf` IS WHY IT IGNITES THE RIGHT ONE.
       The third spec in the game to carry the flag: a `burst` is drawn at
       `[u.tx, u.ty]` — at the QUARRY — which is right for the four novas the
       mode was written for and wrong for anything that resolves on its caster.
       Deadfall's field caught this on the first rendered frame and by nothing
       else, and this ultimate touches nobody on the frame it is cast.

       IT RISES. `grav` is negative and `up` is set, because what a viewer
       should read is heat coming OFF a weapon rather than a shell shedding
       material — and it is short, because the fourteen seconds after it are
       five drawn holes and a jet, not a particle field. */
    cindercleave: { mode: 'burst', n: 900, sp: [70, 330], grav: -240,
                    drag: 2.2, life: [0.30, 0.95], heavy: 0.06,
                    size: [0.5, 2.0], spawn: 0.12, up: 40, atSelf: 1 }"""


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
    source and this file explains itself IN that source -- `tearVent`'s own
    comment says the words "do not build the jet on shots".
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


def refuse(s: str) -> None:
    """The build's own §8, asserted on the text it is about to write.

    Every one of these is a "WHAT NOT TO DO" from the brief that would leave
    every number right and the relic wrong -- which is this project's own
    defect class and the reason a builder refuses instead of printing.
    """
    tick = strip_comments(span(s, "  tickBreach(dt){", "tickBreach"))
    tear = strip_comments(span(s, "  tearVent(f, P){", "tearVent"))
    hit = strip_comments(span(s, "  jetHit(v, own, foe){", "jetHit"))
    both = tick + tear + hit

    # §8. DO NOT BUILD THE JET ON `shots`. `spawnShot` shifts the oldest live
    # entry out at maxLive 64 and `tickShots` lets `bladeSegments` PARRY a
    # shot, with melee's defence winning ties. A jet of heat a scythe can parry
    # is a different mechanic and nobody has decided it is this one.
    for bad in ("spawnShot", "this.shots"):
        if bad in both:
            raise SystemExit(
                f"BREACH touches `{bad}` (brief §4). The jet is not a shot:\n"
                f"  `spawnShot` shifts the oldest live entry out at maxLive 64,"
                f" and\n  `tickShots` lets a blade PARRY one.")

    # §8. DO NOT HANG THE HOLES ON `m.ultFx`. One slot, the opponent overwrites
    # it, and Deadfall measured 0.0% survival against Ironhail.
    if "ultFx" in both:
        raise SystemExit(
            "BREACH's tick reads or writes `ultFx` (v54 §2a, open item 25).\n"
            "  It is ONE SLOT and the opponent casting anything erases it. The"
            " licence\n  lives on `f.ultBreach` and the holes on `m.vents`.")

    # §8. DO NOT LET `k` DRIVE DAMAGE OR PERIOD. Four knobs riding one scalar
    # is how a relic becomes untunable -- the bisection has nothing to grab.
    m = re.search(r"k,\s*half:.*?life:.*?\n", tear, re.S)
    if not m:
        raise SystemExit("cannot find the vent record's size line in tearVent")
    tail = tear[tear.index("k, half:"):]
    tail = tail[:tail.index("});")]
    for f in ("jetDmg", "period", "dmg:", "sunderN"):
        if f in tail and "* k" in tail.split(f)[1][:40]:
            raise SystemExit(
                f"`k` drives `{f}` (brief §3.2). It drives WIDTH and LIFE and\n"
                f"  nothing else: everything-at-once is +6.1pp stronger and is"
                f" four knobs\n  riding one scalar, which leaves the bisection"
                f" nothing to grab.")

    # §8. DO NOT MAKE THE JETS BURN THE CASTER. +28.5% -> +3.8%, and it is a
    # different relic rather than a balance term.
    if "jetHit(v, own, own)" in tick or re.search(r"jetHit\(\s*v\s*,\s*foe\s*,",
                                                  tick):
        raise SystemExit("a jet is resolving on its own caster (design §4.7): "
                         "+28.5% -> +3.8%.")

    # §4.3 of the design doc, and it is v40 §3.3 restated: a vent is {wall, u}
    # in ARENA space. An absolute (x, y) torn early is buried in the wall by
    # the end of the fight, because the inset walks 0 -> 140 from t=21s.
    if "v.wall" not in tick or "this.inset" not in tick:
        raise SystemExit("the vent loop does not recompute its position from "
                         "the CURRENT inset\n  (design §4.3). A hole stored as "
                         "an (x, y) is outside the hall by t=60.")

    # THE PASS IS THE COOLDOWN. A tear cooldown would be an arbitrary spacing
    # rule bolted on top of one the weapon's own rotation already provides.
    if re.search(r"\btearCd\b|\bcutCd\b", both):
        raise SystemExit("BREACH has a tear cooldown (brief §8). THE PASS IS "
                         "THE COOLDOWN.")

    # AND THE BEARING IS NOT DRAWN FROM `this.rng()`. The house rule since
    # Ironbloom's splinters: a relic not in the match must not be able to
    # perturb the draw order of one that is.
    if "this.rng()" in tear:
        raise SystemExit("the bearing is drawn from `this.rng()` (brief §3.4). "
                         "Use `shellHash`:\n  a relic not in the match must not "
                         "perturb the draw order of one that is.")

    print("  rule  not a shot, not on ultFx, k drives width and life only, foe"
          "\n        only, {wall,u} in arena space, the pass is the cooldown, "
          "and the\n        bearing is hashed")


def ult_matches(s: str, A) -> None:
    """The shipped `ult` block carries every number this run printed.

    v56's own failure, verbatim: the stage-2 insert writes the whole `ult`
    block and stage 3 rewrote only the line carrying `charge`, so
    `--stage 3 --cadence 2.0` LOGGED the new rhythm and SHIPPED the old one --
    and every gate downstream measured a relic the log was not describing. It
    was caught by a probe printing `n=5` two minutes later.
    """
    i = s.index(f'id:"{RELIC}"')
    # THE PROSE IS STRIPPED FIRST, and it is not a nicety: this relic's own
    # comment says "STUBBED AT `charge:1e9` IN STAGE 1", so the first thing
    # this check ever did was read the HISTORY of the build instead of the
    # build. CLAUDE.md, third time in three sessions -- a check that cannot
    # tell code from the comment explaining it fires on its own explanation.
    blk = strip_comments(s[i:s.index("blurb:", i)])
    want = {k: getattr(A, k.lower()) for k in ULT}
    want["charge"] = A.charge
    bad = []
    for k, v in want.items():
        m = re.search(rf"\b{k}:\s*([0-9.e+]+)", blk)
        if not m or abs(float(m.group(1)) - float(v)) > 1e-9:
            bad.append(f"{k}: shipped {m.group(1) if m else '(absent)'}, "
                       f"printed {v:g}")
    if bad:
        raise SystemExit("the shipped ult block does not carry what this run "
                         "printed:\n  " + "\n  ".join(bad))
    print(f"  ult   every number in the shipped block matches this run")


def sync_fx(s: str) -> str:
    """The inlined copy and the file on disk must stay the same object.

    `fx_build.py` inlines `src/render/fx.js` verbatim and stamps its sha256
    into the page. A spec written only into the page is a spec the next
    `fx_build` run silently drops -- and `ULTFX.sync` RETURNS on a missing
    spec, which is not an error, which is exactly why it would ship.
    """
    fx_js = HERE.parent / "src" / "render" / "fx.js"
    mod = fx_js.read_text(encoding="utf-8")

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
    ap.add_argument("--stage", type=int, required=True, choices=(1, 2, 3))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--charge", type=float, default=15.0)
    # THE BLADE BELONGS TO WHICHEVER STAGE IS RUNNING, and stage 3b has to be
    # asked for. v56: defaulting every stage to the tuned value made stage 2
    # write it and stage 3 then fail looking for the starting value.
    ap.add_argument("--dmg", type=float, default=None,
                    help="stages 1-3: the starting blade (default %.2f). "
                         "stage 3b: the tuned one, and it has no default"
                         % BLADE_IN)
    for k, v in ULT.items():
        ap.add_argument(f"--{k.lower()}", type=float, default=v)
    A = ap.parse_args()
    # THE BLADE BELONGS TO WHICHEVER STAGE IS RUNNING, and this line is the
    # one v56 got wrong. Stages 1 and 2 ship the STARTING blade, which is what
    # the floor gate and the distribution gate are measured against; stage 3b
    # is the only place the tuned value lands. Defaulting every stage to
    # TUNED_CC made stage 1 write 19.75 and stage 3 then refuse, looking for
    # the 21 it was supposed to replace -- a loud failure, and only because
    # the retune asserts.
    if A.dmg is None:
        A.dmg = TUNED_CC if (A.stage == 3 and TUNED_CC is not None) else BLADE_IN

    src = A.src or {1: "../02-chain/sc-gnawed.html",
                    2: "../02-chain/sc-cindercleave.html",
                    3: "../02-chain/sc-thepass.html"}[A.stage]
    out = A.out or {1: "../02-chain/sc-cindercleave.html",
                    2: "../02-chain/sc-thepass.html",
                    3: "../02-chain/sc-breach.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nCINDERCLEAVE -- STAGE {A.stage}: "
          + {1: "the 29th relic, its ultimate stubbed",
             2: "THE PASS AND THE TEAR -- holes open, and they do not fire",
             3: "BREACH -- the jets, the front, and the count of five"}[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the curse rework is "
                         "upstream of this whole chain")
    if "_whGnawed" not in s0:
        raise SystemExit("this source is not the v58 tip -- `_whGnawed` is "
                         "absent.\n  Build off `sc-gnawed.html`, not "
                         "`sc-grasp.html` (see this file's header).")

    tip = A.tip.replace("%NWORD%", NWORDS.get(int(A.n), str(int(A.n))))
    if len(tip) > 72:
        raise SystemExit(f"ULT TIP is {len(tip)} characters against 72:\n  {tip}")
    # AND THE NUMBER IN IT IS THE WEAPON'S OWN. `bulwarden_probe [1]` made this
    # a rule after v40 shipped a card reading "5s" for a window of 8.1.
    if int(A.n) not in NWORDS:
        raise SystemExit(f"n {A.n:g} has no word in NWORDS, so the tip cannot "
                         f"be written truthfully.")
    if int(A.n) < 2:
        raise SystemExit("a licence that ends on its first tear is not a count, "
                         "it is a nova with\n  a wind-up. Rick's own range is "
                         "3-5.")

    subs = {"%ULT%": A.ult, "%TIP%": tip, "%BLURB%": BLURB,
            "%DMG%": f"{A.dmg:g}", "%CHARGE%": f"{A.charge:g}",
            "%N%": f"{int(A.n):d}", "%CAP%": f"{A.cap:g}",
            "%PASSMAX%": f"{A.passmax:g}", "%KMIN%": f"{A.kmin:g}",
            "%KMAX%": f"{A.kmax:g}", "%MAXVENTS%": f"{int(A.maxvents):d}",
            "%WARM%": f"{A.warm:g}", "%PERIOD%": f"{A.period:g}",
            "%LIFE%": f"{A.life:g}", "%HALF%": f"{A.half:g}",
            "%JETDMG%": f"{A.jetdmg:g}", "%SPEED%": f"{A.speed:g}",
            "%TAPERTO%": f"{A.taperto:g}", "%SUNDERN%": f"{int(A.sundern):d}",
            "%JETKNOCK%": f"{A.jetknock:g}"}

    if A.stage == 1:
        if f'id:"{RELIC}"' in s0:
            raise SystemExit("this source already has Cindercleave -- built")
        edits = S1
        print(f"  ult {A.ult}  STUBBED at charge 1e9")
        print(f"  tip {len(tip)}/72  {tip}")
        print(f"  blade {A.dmg:g}   (the bisection START, not a shipped number)")
    elif A.stage == 2:
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("this source has no Cindercleave -- stage 1 first")
        if "tickBreach" in s0:
            raise SystemExit("this source already has tickBreach -- built")
        edits = S2
        print(f"  ult {A.ult}  charge {A.charge:g}   "
              + "  ".join(f"{k} {getattr(A, k.lower()):g}"
                          for k in ("n", "cap", "passMax", "kMin", "kMax",
                                    "maxVents")))
        print("  gate  the depth distribution is a PUBLISHED PREDICTION: "
              "median 0.63,\n        sd 0.32, 27% above 0.9. If it does not "
              "reproduce, STOP AT THIS\n        STAGE -- the size mechanic is "
              "what is being falsified, not the tuning.")
    else:
        if "tickBreach" not in s0:
            raise SystemExit("this source has no tickBreach -- stage 2 first")
        if "jetHit" in s0:
            raise SystemExit("this source already has jetHit -- built")
        edits = S3
        print(f"  ult {A.ult}  "
              + "  ".join(f"{k} {getattr(A, k.lower()):g}"
                          for k in ("warm", "period", "life", "half", "jetDmg",
                                    "speed", "taperTo", "sunderN", "jetKnock")))
        print(f"  pred  registered: 48-53% against the field at these numbers,"
              f"\n        and the cap ends fewer than 1 window in 50")

    for label, old, new in edits:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    if A.stage == 3:
        if TUNED_CC is not None and abs(A.dmg - BLADE_IN) > 1e-9:
            # THE FOUR SCYTHES SHARE A STAT LINE, so the blade is found by
            # walking forward from this relic's own id and never by a global
            # replace.
            i = s.index(f'id:"{RELIC}"')
            j = s.find(f"dmg:{BLADE_IN:g},", i)
            if j < 0 or j - i > 400:
                raise SystemExit(f"cannot retune: dmg:{BLADE_IN:g} is not in "
                                 f"Cindercleave's own entry.")
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

    if A.stage == 1:
        print("\n  NEXT:")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40      # 29 relics")
        print("      the floor: Cindercleave with no ultimate, well under 43.5%")
    elif A.stage == 2:
        print("\n  NEXT, and item one is the stage gate:")
        print(f"    python pass_probe.py --game {out}")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
    else:
        print("\n  NEXT, and item one is not optional (v43 §13, brief §0):")
        print(f"    python cinema_clip.py --game {out} --a cindercleave "
              f"--b emberedge --seed <seed> --full   # FILM IT FIRST")
        print(f"    python breach_relic_probe.py --game {out}")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
