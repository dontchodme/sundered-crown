#!/usr/bin/env python3
"""GRAVEMOURN'S ULTIMATE -- THE CHAIN LENGTHENS AND THE HANDS COME OFF IT.

    python gravemourn_build.py --src ../02-chain/sc-curse.html \
                               --out ../02-chain/sc-gravemourn.html

STAGE 2 of three (`06-docs/v51/umbral-build-brief-v51.md` §3). Built on top of
the Curse rework, not beside it: every number here is priced against a pool
that remembers.

## RICK'S §1, VERBATIM

    when the ult fires for a duration the flails chain gains length and then
    each time it lands a hit an etheral purple hand flys off the hit. the hand
    soars around the arena briefly and then clenches into a fist as it dive
    bombs into the enemy fighter. on contact it applies curse and deals massive
    knockback.

## "THE CHAIN IS THE ULTIMATE AND THE HAND IS THE PAYLOAD" IS FALSE ON THE
## BUILT RELIC, AND IT WAS THE DESIGN'S HEADLINE CLAIM

`hand_lab.py` priced the chain ALONE, with no payload at all, at **+12.8
points** -- two thirds of a median ultimate -- and v51 concluded the chain was
about 75% of Grasp's whole value. **Measured on the build, removing the chain
buff ENTIRELY costs 3.8 points** (76.3% -> 72.4%, n=780 an arm):

    control (Grasp as built)              76.3%
    reachMul 1.0, no chain buff at all    72.4%   -3.8pp
    dur 3.0, a quarter of the window      64.1%  -12.2pp
    handMul 0.3, hands hit for a third    55.8%  -20.5pp
    charge 42, it fires rarely            52.6%  -23.7pp

**THE HANDS ARE THE ULTIMATE.** The lab measured a chain with nothing coming
off it; once the hands exist and carry pool entries as their damage, they
dominate and the chain's contribution is swamped.

THE MECHANISM THE DOC DESCRIBED IS STILL REAL -- it is only its SHARE that was
wrong. The chain is defensive exactly as priced: with `reachMul` at 1.0 the
foe's damage into this relic goes 203 -> 244. A flail on a longer chain sweeps
a wider circle and holds the quarry outside its own reach. It just is not what
wins the fight.

**And it has an optimum, which does still hold.** 1.30 and 1.45 are the same
within noise; 1.60 and 2.00 fall BACK. Past about 1.45 the head orbits so wide
that the shell it is protecting stops being covered.

## THE BLADE AND THE HANDS ARE THE SAME DAMAGE COUNTED TWICE

Which is why they trade almost exactly. A hand carries a curse pool entry as
its damage, and a pool entry IS a blade blow, so `dmg` and `handMul` are two
taps on one budget. Rick asked to "bring back the blade and do a weaker
grasp"; priced across the curve, n=676 an arm:

    blade 24.03  handMul 1.00   53.8%     <- SHIPPED
    blade 30.00  handMul 0.50   46.0%
    blade 34.00  handMul 0.30   47.2%
    blade 39.79  handMul 0.15   49.6%

Restoring the blade in full costs the hand six sevenths of its bite. Shown the
curve, **he chose to keep 24.03 and a full-strength Grasp** -- the row where
"a hand deals exactly the blow it remembers" survives, and the only one already
verified end to end.

## AND THE BLADE CURVE ALREADY BENDS ON THIS RELIC

v53 §3.5a: swept for stage 1b, Gravemourn reads 67.3% at dmg 47.2 and **60.6%
at 52.0**. More blade makes it worse, because a bigger blow throws the quarry
further out of reach of a weapon that lands 5.6 times a fight.

It was assumed the ULTIMATE'S KNOCKBACK SAT IN THAT SAME LOOP -- a hand
flinging the quarry away mid-window spawning fewer hands, "the design's one
self-inflicted wound" (v51 §4.3). **MEASURED, IT DOES NOT.** Across knock
150 / 400 / 700 / 1000, hands a fight run 3.36 / 3.27 / 3.44 / 3.41 and this
relic's own blows sit at 4.4 throughout -- no trend, over a range where the
force nearly sevenfolds. The homing is why: a hand takes the foe's LIVE
position as its endpoint, so shoving the quarry cannot make the next one miss.
The table is beside `knock` in ULT below.

The BLADE's curve is a different matter and still bends, so whoever runs stage
2b should sweep and plot rather than bisect blind.

## THE THING MOST LIKELY TO WASTE THIS BUILD

`w.reach` IS MODULE-LEVEL. `w` is shared by every match in a page session --
the live page runs hundreds against one roster -- so a window that writes
`w.reach` and misses one restore path does not lengthen one flail, it
**permanently rewrites the relic for every fight afterwards**, and the symptom
appears in a match that never cast anything.

So this build never touches `w.reach`. It adds a PER-FIGHTER `f.reachMul`,
default 1, and multiplies at **every** read site: five in the simulation
(`_initChain`, the chain physics, `bladeSegments`, and both projectile
origins) and two in the renderer (`drawWeapon`, `_stHex`). Miss a renderer one
and the picture disagrees with the hit box, which is the hardest class of bug
in this repo to see.

`hand_lab.py` swaps `w.reach` because it is a throwaway page. This is not.

## THE CHAIN GROWS BY ITSELF AND THAT IS NOT LUCK

`tickWeapon`'s chain branch recomputes `chainLen` from `reach` EVERY FRAME and
eases `headR` toward it through `C.extend`. So raising `reachMul` at the cast
makes the head swing wider over a few frames and settle back when the window
closes, with no animation code at all. The mechanic and the picture are the
same line.

## `handMul` > 1.0 COMPOUNDS WITHOUT BOUND

The hand deals `mem * M` and re-parks `mem * M`, so at M > 1 every memory grows
by M each time it is thrown. An 8-second window and 1.7 casts a fight HIDE it
-- two or three cycles is not enough for the exponent to show, and it reads as
a merely strong relic. A third cast, a longer window or a future duration buff
uncovers it. **M = 1.0 is a conservation law.** It is clamped, and the clamp
says why.

## WHAT IS A PLACEHOLDER

The window `dur` and the tip.

STAGE 2b IS HERE TOO: the blade re-swept WITH Grasp in place, 44.10 -> 39.79
(stage 1b) -> 24.03. §4.5 said the surface would be superlinear and it is
worse than that -- `dmg` moves FOUR channels on this relic, because the hands
carry pool entries as their damage. See TUNED_GM2.

`knock` is NO LONGER a placeholder: Rick took 700 off the three he was offered,
and it is priced. `handFly` is his too, at 1.8s. The hand ART is his, over two
rounds against rendered spreads -- a skeleton at 0.6x, and the reasoning is in
`gravemourn_hands.js` rather than here.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "gravemourn"

# --- the numbers, and every one of them is `hands-v51.md`'s ------------------
ULT = {
    "dur":       8.0,    # the window. 4s->16s is 19 points and it trades
                         # against the blade; 8s is what stage 2b prices
    "reachmul":  1.35,   # PER-FIGHTER. 1.30-1.45 is the plateau, 1.60 falls
                         # back, 2.00 is worse than 1.30
    "handfly":   1.8,    # RICK: "they need a little more flight time".
                         # 1.2 -> 1.8 and it costs nothing measurable:
                         # hands still in the air when the fight ends go
                         # 20.9% -> 20.4%, unchanged inside noise. It only
                         # starts costing past ~2.2s (28.8%) and 2.6s
                         # (31.4%), so the ceiling is named rather than
                         # guessed at.
    "handstag":  0.45,   # seconds between hands off the same blow
    "handmul":   1.0,    # NEVER above 1.0 -- see the header
    "knock":     700.0,  # RICK'S, off the three he was offered (150/400/700).
                         #
                         # AND THE LOOP IT WAS SUPPOSED TO SIT IN DOES NOT
                         # EXIST. v51 §4.3 registered the worry that a hand
                         # flinging the quarry away mid-window would spawn
                         # fewer hands -- "the design's one self-inflicted
                         # wound" -- and v53 §3.5a found the BLADE curve on
                         # this relic bending downward for exactly that
                         # reason, so it was a live concern and not a
                         # hypothetical.
                         #
                         # Measured across 150 / 400 / 700 / 1000, 64 fights
                         # an arm, and every column is FLAT:
                         #
                         #   knock  hands/fight  its blows  foe blows  dealt
                         #     150         3.36        4.4       10.2    381
                         #     400         3.27        4.4       10.6    384
                         #     700         3.44        4.4       10.1    377
                         #    1000         3.41        4.5       10.1    385
                         #
                         # No trend in any of them, over a range where the
                         # force nearly sevenfolds. The reason is the homing:
                         # a hand takes the foe's LIVE position as its Bezier
                         # endpoint, so shoving the quarry does not make the
                         # next hand miss, and the flail's own contact is
                         # reach-dominated rather than proximity-dominated --
                         # the 1.35x chain is already sweeping a wider circle
                         # than the knockback moves anything.
                         #
                         # So the dive can land as hard as it looks. If the
                         # window, the reach or the homing ever change, this
                         # table is the thing to re-run.
}
# RICK'S, off the five that were open to him (Dirge, The Tolling, Arrears,
# Exhumation, Grasp). DIRGE IS RETIRED WITH THE MECHANIC IT NAMED: a dirge is a
# lament and this ultimate is no longer a lament and no longer a pull -- it
# reaches out, takes hold and does not let go, which is what the word he picked
# says and what the hands do.
ULT_NAME = "Grasp"
ULT_TIP = "Lengthens the chain; every hit throws a cursed hand"   # 58/72

# --- STAGE 2b. THE BLADE, RE-SWEPT WITH THE ULTIMATE IN PLACE ---------------
# `umbral_sweep.py --relics gravemourn --lo 14 --hi 42`, 2730 fights.
#
#   44.10  what it shipped with, under the dead curse and a dead ultimate
#   39.79  stage 1b: the curse rework alone, still no real ultimate
#   24.03  HERE: with Grasp. It read 76.0% at 39.79 and failed verify's
#          30-70% band outright.
#
# THE BUILD BRIEF PREDICTED "~22-23" BEFORE ANY OF THIS EXISTED (v51 §3.2,
# "BISECTED, down from 44.10. Not optional"). Measured 24.03. That is the
# closest a registered prediction has come in this project and it is worth
# saying so, because the same document's OTHER prediction -- that knockback
# would eat its own window -- was struck outright. Predictions here are worth
# checking, not assuming, in both directions.
#
# THE CURVE BENDS AND §4.5 SAID IT WOULD. Pass 1, n=104 a point:
#
#   14.00  16.3%     26.00  63.5%     38.00  81.7%
#   18.00  40.4%     30.00  63.5%     42.00  76.0%
#   22.00  36.5%     34.00  69.2%
#
# 18 -> 22 goes DOWN and 38 -> 42 goes DOWN, both inside a 4.9pp standard
# error, so neither dip is signal on its own -- but a bisection started from a
# guessed bracket cannot tell the difference and would have converged happily
# inside one of them.
#
# WHAT THE CUT COSTS, AND IT IS THE RELIC'S OWN IDENTITY. `dmg` now moves FOUR
# channels: the blade, the pool the blade fills, the echo that pool pays, and
# the hands, which carry pool entries AS their damage. So a smaller blade is a
# smaller everything:
#
#              echo share   pool mean   pool peak
#   at 39.79        11.2%          111         303
#   at 24.03         6.0%           66         157
#
# Gravemourn was the biggest blade in the game at 44.10. At 24.03 it is a
# mid-weight flail whose ultimate is most of what it does. THAT IS A DESIGN
# CONSEQUENCE AND NOT A TUNING DETAIL: the alternative is a weaker Grasp --
# a shorter window or a smaller `reachMul` -- bought back as blade. It is
# Rick's, and it is named in the write-up rather than settled here.
TUNED_GM2 = 24.03


EDITS = [

# ------------------------------------------------- 1. the per-fighter field
("Fighter.reachMul", '''    this.burdenMass = 0;      // added FALL mass per blade. Never clank mass.''',
 '''    /* THE WINDOW'S REACH, AND IT LIVES ON THE FIGHTER BECAUSE `w` DOES NOT
       BELONG TO THE MATCH. `w` is module-level and shared by every match in a
       page session — the live page runs hundreds against one roster — so a
       window that writes `w.reach` and misses one restore path does not
       lengthen one flail, it permanently rewrites the relic for every fight
       afterwards, and the symptom shows up in a match that never cast
       anything. Default 1, multiplied at every read of `w.reach` in both the
       simulation and the renderer. Same shape as Nevermend's `blades` hazard,
       one field along. */
    this.reachMul = 1;
    this.burdenMass = 0;      // added FALL mass per blade. Never clank mass.'''),

# --------------------------------------- 2..6 THE FIVE SIMULATION READ SITES
("reach._initChain", '''    f.headR      = f.w.reach * (1 - C.hilt);
    f.pivX = f.x + Math.cos(f.theta) * f.w.reach * C.hilt;
    f.pivY = f.y + Math.sin(f.theta) * f.w.reach * C.hilt;''',
 '''    /* `f.reachMul` at every read — site 1 of 7. It is 1 here in practice
       because nothing has cast yet, and it is written anyway so the field
       means one thing everywhere. */
    f.headR      = f.w.reach * f.reachMul * (1 - C.hilt);
    f.pivX = f.x + Math.cos(f.theta) * f.w.reach * f.reachMul * C.hilt;
    f.pivY = f.y + Math.sin(f.theta) * f.w.reach * f.reachMul * C.hilt;'''),

("reach.chainPhysics", '''      const C = CONFIG.chain;
      const reach = f.w.reach * mods.reach;
      if (f.stun <= 0) f.theta += spin * dt * f.spinDir;''',
 '''      const C = CONFIG.chain;
      /* Site 2 of 7, AND THE ONE THAT MAKES THE PICTURE. `chainLen` below is
         recomputed from this every frame and `headR` is eased toward it, so
         raising `reachMul` at the cast swings the head wider over a few
         frames and settles it back when the window closes — the mechanic and
         the animation are the same line, and there is no second one. */
      const reach = f.w.reach * mods.reach * f.reachMul;
      if (f.stun <= 0) f.theta += spin * dt * f.spinDir;'''),

("reach.bladeSegments", '''    const mods = this.actMods;
    const R = CONFIG.physics.ballR;
    const reach = f.w.reach * mods.reach;
    if (f.w.mode === "chain"){''',
 '''    const mods = this.actMods;
    const R = CONFIG.physics.ballR;
    /* Site 3 of 7, AND THE ONE THAT MAKES IT REAL. This is what `tickHits`
       tests against, so the hit box and the drawn chain grow together. */
    const reach = f.w.reach * mods.reach * f.reachMul;
    if (f.w.mode === "chain"){'''),

("reach.shotOrigin", '''    const a = angle === undefined ? f.theta : angle;
    const ca = Math.cos(a), sa = Math.sin(a);
    const reach = f.w.reach * this.actMods.reach;
    this.shots.push({''',
 '''    const a = angle === undefined ? f.theta : angle;
    const ca = Math.cos(a), sa = Math.sin(a);
    /* Site 4 of 7. No flail shoots, so this is dead for THIS relic — written
       anyway, because a field that means "reach" in five places and nothing
       in a sixth is how the next window mechanic gets a silent hole. */
    const reach = f.w.reach * this.actMods.reach * f.reachMul;
    this.shots.push({'''),

("reach.aimedOrigin", '''    const R = CONFIG.physics.ballR;
    const reach = f.w.reach * this.actMods.reach;
    const ca = Math.cos(a), sa = Math.sin(a);''',
 '''    const R = CONFIG.physics.ballR;
    /* Site 5 of 7 — the SECOND projectile origin, and the one the first pass
       of this builder missed. There are two, not one; `w.reach` was grepped,
       six sites were edited, and this line sat there reading an unmultiplied
       reach. It is dead for a flail like every other shot path here, and it is
       written for the same reason: a field that means "reach" in six places
       and nothing in a seventh is how the next window mechanic gets a silent
       hole. */
    const reach = f.w.reach * this.actMods.reach * f.reachMul;
    const ca = Math.cos(a), sa = Math.sin(a);'''),

# ------------------------------------------ 7..8 THE TWO RENDERER READ SITES
("reach.drawWeapon", '''  drawWeapon(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR;
    const pal = f.aff;
    const reach = f.w.reach * m.actMods.reach;''',
 '''  drawWeapon(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR;
    const pal = f.aff;
    /* Site 6 of 7, AND MISSING IT IS THE HARDEST BUG IN THIS REPO TO SEE: the
       picture would disagree with the hit box, and both would be internally
       consistent. */
    const reach = f.w.reach * m.actMods.reach * f.reachMul;'''),

("reach.stHex", '''  _stHex(m, f, R, n){
    const c = this.ctx, N = Math.min(5, n);
    const reach = f.w.reach * m.actMods.reach;''',
 '''  _stHex(m, f, R, n){
    const c = this.ctx, N = Math.min(5, n);
    const reach = f.w.reach * m.actMods.reach * f.reachMul;   // site 7 of 7'''),

# ------------------------------------------------------ 9. the hands' home
("Match.hands", '''    this.shots = [];          // live projectiles, oldest first''',
 '''    this.shots = [];          // live projectiles, oldest first
    /* THE HANDS, AND THEY ARE PER-MATCH STATE ON THE MATCH. Not on `w`, which
       outlives the fight; not in `shots`, whose `maxLive` ceiling makes
       `spawnShot` SHIFT THE OLDEST LIVE ONE OUT — on a hand in flight that is
       a purple fist vanishing in mid-air with no error, no invariant broken
       and no win rate moved, which is this project's own defect class three
       times over. This list declines and counts instead. */
    this.hands = [];'''),

# ------------------------------------------------------ 10. the cast
("fireUlt.sling", '''    if (u.kind === "winnow"){''',
 '''    if (u.kind === "sling"){
      /* NOT `pull`. Pull-and-cash is the Crucible's verb and this relic is not
         allowed to be a second Crucible; the `pull` branch stays in the file
         and simply loses its only user.

         THE CAST DOES NOTHING BUT OPEN THE WINDOW. `u.dmg` is 0: no radius
         test, no nova, nothing resolves here. What the ultimate IS happens on
         the blows that land inside it, and three quarters of what it is worth
         is the chain being longer while they do. */
      f.ultSling = { t: 0, dur: u.dur, blows: 0, thrown: 0, landed: 0,
                     refused: 0, lost: 0 };
      /* THE ONE WRITE, and it is on the FIGHTER. See the field's own comment
         in the Fighter constructor for why `w.reach` is untouchable. */
      f.reachMul = u.reachMul;
      this.ultFx.life = (u.dur + 0.7) * 2;
      SFX.play("ult", { w: "gravemourn" });
      return;
    }

    if (u.kind === "winnow"){'''),

# ------------------------------- 11. the blows inside the window throw hands
("resolveHit.sling", '''      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);
    }''',
 '''      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);
    }

    /* ---- THE HANDS COME OFF THE BLOW. Rick: "each time it lands a hit an
       etheral purple hand flys off the hit."

       ONE HAND PER ENTRY IN THE FOE'S POOL, and each hand TAKES its entry as
       it peels off — so the pool empties on the blow and the hands carry it.
       That includes the memory this blow's own `onHit` just pushed, which is
       why this sits AFTER the loop above: the blow that throws the hands is
       one of the blows they remember.

       THE POOL IS RE-PARKED RATHER THAN SPENT. Each hand puts its memory back
       as a fresh curse stack when it lands, so the relic is not emptying its
       own engine every time it swings — measured as the strongest of three
       arms (79.5% against 77.0% for spend-and-empty and 74.5% for flat-damage
       hands), and it throws half a hand a fight more.

       `mul === undefined` is an ordinary melee connect and not a projectile,
       the same test Ironbloom's latch and the Crucible's strike use. */
    if (mul === undefined && self.ultSling && foe.alive && !foe.shade
        && !this.over && foe.cursePool.length){
      const S = self.ultSling, U = self.w.ult;
      S.blows++;
      const dx = hx - self.x, dy = hy - self.y;
      const base = Math.atan2(dy, dx);
      const mems = foe.cursePool.slice();
      foe.cursePool.length = 0;
      /* the stack count is DERIVED from the pool, so emptying it is the whole
         of taking the stacks — but the clock entry has to go with them */
      if (self === this.a || self === this.b) delete foe.status.curse;
      for (let i = 0; i < mems.length; i++){
        /* THE CEILING, DECLINED AND COUNTED. Never shift a live hand out. */
        if (this.hands.length >= 24){ S.refused++; continue; }
        this.hands.push({
          src: self === this.a ? "a" : "b",
          mem: mems[i],
          /* staggered off one blow, so three hands leave in sequence rather
             than as one object with three outlines */
          t: -i * U.handStag,
          dur: U.handFly,
          x: hx, y: hy, sx: hx, sy: hy,
          /* the soar bears AWAY from the blow, fanned so they do not overlap.
             No `rng()` here: a hand's whole path is a pure function of where
             the blow landed and which entry it carries, which keeps the
             ultimate reproducible without spending a draw. */
          ang: base + (i - (mems.length - 1) / 2) * 0.9,
          lx: hx, ly: hy, u: 0, gone: false,
        });
        S.thrown++;
      }
      SFX.play("ult", { w: "gravemourn-hand" });
    }'''),

# --------------------------------------------------- 12. the window and the flight
("tickSling", '''  tickWinnow(dt){''',
 '''  /* THE WINDOW, AND THE HANDS IN THE AIR OVER IT.

     The window and the flight are ticked together because they are not
     independent: the window is what makes hands, and a hand outlives the
     window that made it. A hand is a COMMITTED OBJECT — it was thrown, the
     viewer watched it go, and deleting it because a clock ran out would take
     away a hit already earned. The ballista's bolts, the Thicket's seeds and
     the Winnowing's kunai all outlive their windows for the same reason. */
  tickSling(dt){
    for (const f of [this.a, this.b]){
      const S = f.ultSling;
      if (!S) continue;
      S.t += dt;
      if (S.t >= S.dur || !f.alive){
        f.ultSling = null;
        /* THE RESTORE, AND IT IS THE WHOLE §4.1 HAZARD IN ONE LINE. There are
           exactly two ways out of this window — the clock and the corpse — and
           both are here. `reachMul` is per-fighter, so even a missed restore
           could not reach another match; this is belt and braces on the field
           that made that true. */
        f.reachMul = 1;
      }
    }

    for (let i = this.hands.length - 1; i >= 0; i--){
      const h = this.hands[i];
      const src = h.src === "a" ? this.a : this.b;
      const foe = h.src === "a" ? this.b : this.a;
      h.t += dt;
      if (h.t < 0) continue;                     // still peeling off
      const u = Math.min(1, h.t / h.dur);
      h.u = u;
      /* SOAR, THEN DIVE. A quadratic Bezier from where the blow landed,
         through a control point thrown out along `ang`, to the foe's LIVE
         position — so the hand curves away from the impact, comes round, and
         is still homing when it arrives. `s` is eased so the first two thirds
         drift and the last third accelerates: that is "soars around the arena
         briefly and then dive bombs", written as one curve rather than as two
         states with a seam between them. */
      const s = Math.pow(u, 1.7);
      const R = CONFIG.physics.ballR;
      const cx = h.sx + Math.cos(h.ang) * R * 5.2;
      const cy = h.sy + Math.sin(h.ang) * R * 5.2 - R * 2.4;
      const k = 1 - s;
      h.lx = h.x; h.ly = h.y;
      h.x = k * k * h.sx + 2 * k * s * cx + s * s * foe.x;
      h.y = k * k * h.sy + 2 * k * s * cy + s * s * foe.y;
      if (u < 1) continue;

      this.hands.splice(i, 1);
      /* A HAND MUST NOT RESOLVE ON A CORPSE OR AFTER THE FIGHT. `hand_lab`
         models this and it is 20-30% of hands spawned; counted rather than
         dropped silently, because "it landed" and "it was never allowed to"
         produce the same absence in every other instrument. */
      if (this.over || !foe.alive || !src.alive){
        if (src.ultSling) src.ultSling.lost++;
        continue;
      }

      /* IT DEALS EXACTLY WHAT IT CARRIES. `handMul` is clamped at 1.0 and the
         clamp is a CONSERVATION LAW, not a taste: the hand deals `mem * M` and
         re-parks `mem * M`, so at M > 1 every memory grows by M each time it
         is thrown. An 8-second window and 1.7 casts a fight hide the exponent
         for two or three cycles and it reads as merely strong; a third cast or
         a longer window uncovers it. */
      const M = Math.min(1, src.w.ult.handMul);
      const dmg = Math.round(h.mem * M * foe.dmgTakenMul());
      if (dmg > 0){
        this.hurt(foe, dmg, src);
        src.dealt += dmg;
        /* `hits` is deliberately NOT incremented: a hand does not go through
           `resolveHit`, and verify's "no pairing resolves on fewer than 6
           hits" floor is about BLOWS LANDED, which this is not. */
        foe.flash = 1; foe.ringFlash = 1;
        this.float(foe.x, foe.y - 40, dmg, AFFINITIES.umbral.glow, 34 + dmg * 0.5);
      }
      /* AND IT REMEMBERS WHAT IT JUST DEALT. A hand that lands is a hit, so
         the memory is PASSED ALONG rather than grown — which is the same
         `dmgBase`-not-`dmg` rule resolveHit obeys, arriving from the other
         side. */
      foe.pushCurse(dmg, 1);
      foe.apply("curse", 1);
      const first = !this.taught.curse && !!STATUS.curse.tip;
      if (first) this.taught.curse = true;
      this.statusTag(foe.x, foe.y, "curse", first, Math.round(foe.curseSum()));

      /* MASSIVE KNOCKBACK, along the line the fist came in on. */
      const kx = foe.x - h.lx, ky = foe.y - h.ly;
      const kl = Math.hypot(kx, ky) || 1;
      const power = src.w.ult.knock;
      foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;

      /* A FIST THAT ENDS THE FIGHT CARRIES THE FIGHT'S OWN WEIGHT. `resolveHit`
         swaps its hit-stop for `killStop` and arms `finisher` on a fatal blow;
         a hand landing outside that function has to do it itself or the
         killing blow of this ultimate is lighter than an ordinary swing. */
      const fatal = !foe.alive;
      if (fatal){
        this.hitStop = Math.max(this.hitStop, CONFIG.impact.killStop);
        this.finisher = 1.0;
      } else {
        this.hitStop = Math.max(this.hitStop, 0.05);
      }
      this.shake = Math.min(38, this.shake + (fatal ? 22 : 12));
      this.spawnFx(foe.x, foe.y, AFFINITIES.umbral.core, 26, 260, 0.6, 5);
      this.ring(foe.x, foe.y, AFFINITIES.umbral.glow, 6, 120, 0.4, 6);
      SFX.play("ult", { w: "gravemourn-fist" });
      /* RULE 3, SEVENTH RELIC RUNNING. The hands land through their own path,
         so nothing else in the frame knows the dive happened and `cinePlan`
         would score the best moment of this ultimate as empty air. */
      this.beat({ kind: "ult", side: src === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, w: src.w.id,
                  foeHpFrac: foe.hp / foe.maxHp });
      /* AND THE FATAL ONE IS FILED AS A HIT, WHICH IS A SECOND BEAT ON PURPOSE.
         `cinema_clip` finds the killing blow with `plan.find(c => c.fatal)`,
         and NOTHING on an `ult` beat carries that flag. Measured before this
         line existed: 30 of Gravemourn's 58 kills over 80 fights -- 51.7% --
         were landed by a hand, and ALL THIRTY produced a clip with no killing
         blow at all, falling back to "the last cut".

         That is open item 3's defect class (Dawnbringer 22.1% blind, the spark
         burn and `_traceHit`) and this would have been the worst instance of
         it in the game. It is also the Thicket's precedent applied exactly:
         `_cineVine` suppresses every lash beat AND KEEPS THE FATAL ONE,
         because "do not let small hits drive the camera" is a different claim
         from "do not film the finish".

         The shape is resolveHit's, so the director scores it against ordinary
         kills rather than against a special case. */
      if (fatal)
        this.beat({ kind: "hit", side: src === this.a ? 0 : 1,
                    x: foe.x, y: foe.y, dmg, crit: false, fatal: true,
                    hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                    selfHpFrac: src.hp / src.maxHp,
                    spd: src.speed, foeSpd: foe.speed,
                    close: Math.hypot(src.vx - foe.vx, src.vy - foe.vy) });
      if (src.ultSling) src.ultSling.landed++;
    }
  }

  tickWinnow(dt){'''),

("step.tickSling", '''    this.tickWinnow(dt);
    this.tickBallista(dt);''',
 '''    this.tickWinnow(dt);
    this.tickSling(dt);
    this.tickBallista(dt);'''),

# ---------------------------------------------------------- 13. the picture
# THE HAND ART LIVES IN ITS OWN .js FILE. It is Rick's pick off a rendered
# spread and it will be iterated on again; a builder that has to re-escape 180
# lines of canvas drawing every round is a builder that will escape it wrong.
# Read verbatim, inlined verbatim -- the same shape `fx_build.py` uses for
# `src/render/fx.js`, one directory along.
("drawHands", '''  drawShots(m){''',
 (HERE / "gravemourn_hands.js").read_text(encoding="utf-8")
 + "\n  drawShots(m){"),

("draw.dispatch", '''    this.drawShots(m);
    this.drawStuck(m);''',
 '''    this.drawShots(m);
    this.drawHands(m);
    this.drawStuck(m);'''),

# ------------------------------------------------------------ 14. the sound
("sfx.gravemourn", '''        } else if (w === "gravemourn"){                 // a drop into the grave
          this._tone (t, { freq: 420, to: 44, gain: 0.30, dur: 1.1, type:"sawtooth" });
          this._tone (t + 0.05, { freq: 300, to: 38, gain: 0.18, dur: 1.0, type:"sine" });
          this._burst(t, { freq: 420, q: 0.6, gain: 0.16, dur: 0.9, type:"lowpass" });''',
 '''        } else if (w === "gravemourn"){        // the chain paying out
          /* THE CAST IS A WINDOW OPENING, NOT A THING LANDING, and the old
             voice was a drop into the grave — a falling tone that ENDS. This
             one pays out: a low rising slide with links ticking over it, and
             it does not resolve, because nothing has happened yet. */
          this._tone (t, { freq: 58, to: 96, gain: 0.30, dur: 1.10, type:"sawtooth" });
          this._tone (t + 0.04, { freq: 116, to: 190, gain: 0.15, dur: 0.95, type:"sine" });
          [0, 0.11, 0.21, 0.30, 0.38].forEach((d, i) =>
            this._burst(t + d, { freq: 1500 + i * 260, q: 1.4,
                                 gain: 0.11 - i * 0.015, dur: 0.06,
                                 type:"bandpass" }));
          this._burst(t + 0.42, { freq: 520, q: 0.7, gain: 0.10, dur: 0.75, type:"lowpass" });
        } else if (w === "gravemourn-hand"){   // something leaves the blow
          /* Breathy and upward — it is a departure, and it has to be audible
             UNDER the blow that threw it without competing with the fist. */
          this._burst(t, { freq: 900, q: 0.9, gain: 0.13, dur: 0.22, type:"bandpass" });
          this._tone (t, { freq: 300, to: 720, gain: 0.11, dur: 0.30, type:"triangle" });
        } else if (w === "gravemourn-fist"){   // and it arrives
          /* THE HEAVIEST THING THIS RELIC HAS, because the knockback is the
             sentence: a hard low thud with a short bright crack on top so it
             cuts through a hit-stop. */
          this._burst(t, { freq: 220, q: 0.5, gain: 0.34, dur: 0.26, type:"lowpass" });
          this._tone (t, { freq: 150, to: 40, gain: 0.30, dur: 0.34, type:"sine" });
          this._burst(t + 0.02, { freq: 3200, q: 1.1, gain: 0.15, dur: 0.07, type:"bandpass" });
          this._tone (t + 0.05, { freq: 340, to: 96, gain: 0.13, dur: 0.42, type:"triangle" });'''),

# ------------------------------------------- 14b. STAGE 2b, the blade
("blade.2b", '''    blades:[0], reach:96, width:22, artW:52, dmg:39.79, spin:2.2, mode:"chain", mass:3.6,''',
 '''    /* dmg 39.79 -> %DMG% (stage 2b, `umbral_sweep.py`, 2730 fights). 39.79
       was stage 1b's answer for a relic with NO working ultimate; with Grasp
       it read 76.0% and failed verify's 30-70% band outright. The v51 brief
       predicted "~22-23" before any of this was built.

       THIS IS THE RELIC'S IDENTITY MOVING, not a tuning detail. `dmg` feeds
       FOUR channels here — the blade, the pool the blade fills, the echo that
       pool pays, and the hands, which carry pool entries as their damage — so
       the cut takes the echo's share from 11.2% to 6.0% and the pool's mean
       from 111 to 66. Gravemourn had the biggest blade in the game at 44.10.
       The alternative is a weaker Grasp bought back as blade, and that is
       Rick's. See curse_build.TUNED_GM and gravemourn_build.TUNED_GM2. */
    blades:[0], reach:96, width:22, artW:52, dmg:%DMG%, spin:2.2, mode:"chain", mass:3.6,'''),

# ------------------------------------------------------- 15. the relic's data
("ult.dirge", '''    /* `apply:{curse:3}` is GONE. Measured at -3.2 points against a field
       median of +20.4 (`ult_price.py`) — an ultimate whose payload was worth
       LESS than nothing, because a curse stack applied by an ultimate carries
       no memory to remember. Stage 2 replaces the payload; this stage only
       takes the dead one out. Name and tip are PLACEHOLDERS and are Rick's. */
    ult:{ name:"Dirge", charge:16, kind:"pull", radius:320, dmg:14, tip:"Pulls target in, dealing 14 damage" },''',
 '''    /* THE CHAIN IS THE ULTIMATE AND THE HAND IS THE PAYLOAD, which is the
       opposite of how §1 reads. `hand_lab.py` priced the chain with NO payload
       at all at +12.8 points — two thirds of a median ultimate — and it does
       not buy contact: this relic's own blows move 5.3 -> 5.6, six percent,
       nothing. IT BUYS DEFENCE. The foe lands 15.5 -> 14.0 blows and deals
       303 -> 273 damage, because a flail on a longer chain sweeps a wider
       circle and holds the quarry outside its own reach.

       `reachMul` HAS AN OPTIMUM AND IT IS NOT "LONGER". 1.30 and 1.45 are the
       same within noise; 1.60 and 2.00 fall BACK, and at 2.00 the foe's blows
       climb again — past about 1.45 the head orbits so wide that the shell it
       is protecting stops being covered.

       `dmg` 0: the cast opens the window and does nothing else. `kind` is
       "sling" and NOT "pull" — pull-and-cash is the Crucible's verb.

       NAME, TIP AND `knock` ARE PLACEHOLDERS AND ARE RICK'S. He was offered
       150 / 400 / 700 for the dive; the blade is stage 2b. */
    ult:{ name:"%ULT%", charge:16, kind:"sling", dmg:0,
          dur:%DUR%, reachMul:%REACHMUL%,
          handFly:%HANDFLY%, handStag:%HANDSTAG%, handMul:%HANDMUL%,
          knock:%KNOCK%, tip:"%TIP%" },'''),
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-curse.html")
    ap.add_argument("--out", default="../02-chain/sc-gravemourn.html")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=TUNED_GM2,
                    help="stage 2b: the blade, with Grasp in place")
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
    print("\nGRAVEMOURN -- the chain lengthens and the hands come off it")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    # THE CHAIN IS LINEAR AND STAGE 2 SITS ON STAGE 1. The hands take entries
    # out of the curse pool; without the rework there is no pool to take.
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the Curse rework "
                         "lands FIRST (brief §0). Build off sc-curse.html.")
    if '"sling"' in s0:
        raise SystemExit("this source already has a sling -- already built")

    # §4.2 IS A CONSERVATION LAW AND THE BUILDER ENFORCES IT, not just the
    # engine. A sweep is allowed to look under 1.0 and is not allowed over it.
    if A.handmul > 1.0:
        raise SystemExit(
            f"handMul {A.handmul:g} > 1.0. The hand deals mem * M and re-parks "
            f"mem * M, so every memory grows by M each time it is thrown and "
            f"the relic compounds without bound. Two or three cycles hide it "
            f"and it reads as merely strong. This is not a tuning range.")
    # AND THE REACH HAS A MEASURED CEILING, not just a measured optimum.
    if A.reachmul > 1.5:
        print(f"  WARN reachMul {A.reachmul:g} is past the measured plateau "
              f"(1.30-1.45). 1.60 and 2.00 both fall BACK -- the head orbits "
              f"wider than the shell it is protecting.")
    if len(A.tip) > 72:
        raise SystemExit(f"ULT TIP is {len(A.tip)} characters against 72:\n  {A.tip}")

    print(f"  ult {A.ult}   " + "  ".join(f"{k} {getattr(A, k):g}" for k in ULT))
    print(f"  tip {len(A.tip)}/72  {A.tip}")

    subs = {"%ULT%": A.ult, "%TIP%": A.tip, "%DMG%": f"{A.dmg:g}",
            "%DUR%": f"{A.dur:g}", "%REACHMUL%": f"{A.reachmul:g}",
            "%HANDFLY%": f"{A.handfly:g}", "%HANDSTAG%": f"{A.handstag:g}",
            "%HANDMUL%": f"{A.handmul:g}", "%KNOCK%": f"{A.knock:g}"}

    for label, old, new in EDITS:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # THE HAZARD, ASSERTED STATICALLY AND FOR FREE. §4.1 is the single most
    # likely way this build gets wasted, and "no assignment to w.reach" is a
    # property of the text.
    for bad in ("w.reach =", "w.reach=", ".reach = f.w.reach"):
        if bad in s:
            raise SystemExit(f"THE BUILD ASSIGNS TO w.reach ({bad!r}). `w` is "
                             f"module-level and shared by every match in a page "
                             f"session -- see §4.1.")
    # AND EVERY READ SITE CARRIES THE MULTIPLIER.
    # EVERY LIVE READ CARRIES THE MULTIPLIER, ASSERTED RATHER THAN COUNTED.
    # The first pass of this builder edited six sites and missed a seventh --
    # a second projectile origin -- and nothing said so, because a printed
    # count is something a person has to notice. These are the reads that are
    # NOT allowed to stand bare: `f.w.reach` and `m.actMods`-scaled renderer
    # reads. The card art (`w.reach` on a weapon with no fighter) legitimately
    # cannot take one, so it is excluded by name.
    bare = [ln.strip() for ln in s.splitlines()
            if "f.w.reach" in ln and "reachMul" not in ln]
    if bare:
        raise SystemExit(
            "THESE READS OF `f.w.reach` DO NOT CARRY `reachMul` (§4.1):\n  "
            + "\n  ".join(bare[:8]))
    print(f"  reach every `f.w.reach` read carries reachMul "
          f"({s.count('reachMul')} mentions)")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT, and item one is not optional (v43 §13, brief §0):")
    print(f"    python cinema_clip.py --game {A.out} --a gravemourn "
          f"--b emberedge --seed <seed> --full   # FILM IT FIRST")
    print(f"    python gravemourn_relic_probe.py --game {A.out}")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10   # the 24")
    print(f"    python verify.py --game {A.out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
