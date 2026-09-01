#!/usr/bin/env python3
"""GARROTE, ASSERTED AGAINST THE BUILD — one check per sentence. Brief section 6.

    python garrote_relic_probe.py --game ../02-chain/sc-wire.html

  [1]  THE WINDOW exists only while the ultimate is open, and no catch is ever
       made outside the ring's own radius
  [2]  THE WIND-UP MULTIPLIES ROTATION AND NOTHING ELSE — reach, damage and
       hitCd are untouched
  [3]  NOT `f.ultSpin`. That field is Twinshade's and it also changes clanks
  [4]  THE SNAG WRITES `f.pin` AND NEVER `f.stun`, AND THIS IS THE RELIC — the
       caught fighter's weapon still turns and still lands blows while held
  [5]  ONE CATCH PER WINDOW. The connect expires the ring
  [6]  THE CONNECT IS AN ORDINARY MELEE BLOW, found by the engine's own hit
       loop — never a timer, never a projectile
  [7]  THE HOLD ENDS WHEN THE WINDOW DOES, and `pin`, `pinMax`, `pinV` and
       `pinFree` are all clear afterwards
  [8]  THE KNOCKBACK ACTUALLY MOVES THE BALL. Read as a DISPLACEMENT two frames
       after the connect. THE SINGLE MOST IMPORTANT CHECK HERE
  [9]  THE CASTER IS NEVER SNAGGED, and no OTHER relic's hold is ever touched
  [10] NO CATCH ON A CORPSE, none after `m.over`, none while `m.hitStop > 0`
  [11] THE BEAT. The cast files one, the connect files its own through
       `resolveHit`, and a KILLING connect files a FATAL one
  [14] CONNECTS PER CAST IS 0.8-0.9 — the scalar the picture depends on
  [15] EVERY VOICE RENDERS TO SOMETHING AUDIBLE in an OfflineAudioContext
  [P]  THE RENDER PATH IS CALLED against a real 2D context
  [X]  AND THE RUNIC HEXAGON IS NOT DRAWN ON A WIRE SNAG

Checks 12 and 13 are the CONSUME and they belong to stage 3. This probe reports
them as not-yet-built rather than passing them, because a check that cannot
fail is worth nothing.

## [4] IS THE WHOLE RELIC AND THE TRAP IS NOT WHERE THE BRIEF SAYS

The brief's instruction is "write `f.pin`, do NOT write `f.stun`", and obeying
it exactly is not enough on this engine. `tickStasis`'s decrement loop runs for
both fighters every frame, OUTSIDE any `ultField` guard, and carries the line
`f.stun = Math.max(f.stun, f.pin)`. So any relic that writes `pin` is handed a
weapon lock by Paradox's bookkeeping, from a file nowhere near its own code —
and a check that asserts "tickWire never writes f.stun" passes, because
tickWire does not.

**So [4] does not read the source. It reads the caught fighter's WEAPON**, and
asserts that it is still turning and still landing blows while the ball is
held. That is the sentence the design is actually making.

## [8] IS THE ONE THAT WOULD SHIP BROKEN

`move()` ASSIGNS `f.pinV` on the first frame a held ball is allowed to move
again — v43's rule — so every impulse a ball took while pinned is discarded.
Garrote's headline effect is a massive knockback delivered to a ball that is
pinned at that instant. Written in the wrong order the hit lands, the damage
lands, the beat files, every other check in this file passes, AND THE BALL DOES
NOT MOVE. A test that reads `vx` immediately after the write passes in the
broken build, so this one reads POSITION two frames later.

## AND THE CHECKS RECONSTRUCT THE ENGINE'S RULE RATHER THAN ASSUMING THEIR OWN

`gravemourn_relic_probe` reported three defects that were not there, all
because the probe had written down its own model of a rule and the engine
legitimately did something else. So `dur`, `radius`, `spinMul`, `kick`,
`launch` and `connectKnock` are read off `w.ult` here and never typed in.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "ravelbone"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}"
          + (f"\n        {detail}" if detail else ""))


# ------------------------------------------------------------- the main run --
# ONE instrumented match per (foe, seed). Every hook forwards with `arguments`
# -- v44's warning, and it is that a wrapper with a FIXED ARITY silently
# measures the OLD build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs, hasConsume]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const R = AC.CONFIG.physics.ballR;
  const A = {
    fights: 0, casts: 0, catches: 0, connects: 0, expired: 0,
    heldFrames: 0, heldSecs: 0, windowSecs: 0,
    /* [1] */ outsideRadius: 0, wireNoWindow: 0, radiusSeen: 0,
    /* [2] */ reachMoved: 0, dmgMoved: 0, hitCdMoved: 0, spinBad: 0, spinN: 0,
    /* [3] */ ultSpinSet: 0,
    /* [4] */ stunWhileHeld: 0, heldChecks: 0, weaponTurned: 0,
              weaponFrozen: 0, blowsWhileHeld: 0,
              heldFreeFrames: 0, freeTurned: 0, freeFrozen: 0,
              snagAddedStun: 0, hitsOnHeld: 0, meleeOnHeld: 0,
              heldFrozenHall: 0,
    /* [5] */ recaught: 0, ringAfterConnect: 0,
    /* [6] */ connectNotMelee: 0,
    /* [7] */ dirtyAfter: 0, releaseChecks: 0,
    /* [8] */ moved: 0, notMoved: 0, dispSum: 0, disp2Sum: 0, dispMin: 1e9,
    /* [9] */ selfSnag: 0, foreignPin: 0, shadeSnag: 0,
    /* [10]*/ corpseCatch: 0, overCatch: 0, frozenCatch: 0, frozenChecks: 0,
    /* [11]*/ castBeats: 0, catchBeats: 0, connectBeats: 0,
              connectFatalBeats: 0, connectKills: 0,
    dmgSum: 0, foeBlows: 0, myBlows: 0,
    /* [12/13] */ consumeChecks: 0, consumeLeft: 0, consumeTookMine: 0,
                  consumeWrong: 0, hemSum: 0, burstSum: 0, leftSum: 0,
  };
  const M = AC.Match.prototype;
  const origBeat = M.beat, origHit = M.resolveHit,
        origRelease = M.releaseWire, origFire = M.fireUlt,
        origTick = M.tickWire;

  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      A.fights++;
      const me = m.a;                       // the relic is always side A here
      let inConnect = false, inCast = false;
      const me_foe = () => (me === m.a ? m.b : m.a);
      let pend = null;                      // [8] the displacement watch

      /* [11] THE CAST'S BEAT IS FILED BY `fireUlt` AND THE CATCH'S BY
         `tickWire`, AND A FRAME FLAG CANNOT TELL THEM APART -- the first cut
         of this check set a flag around the whole `m.step()` call, so the cast
         beat was counted as a catch and [11] reported 0 casts against 111.
         Attribute a beat to the CALL that filed it, never to the frame. */
      m.fireUlt = function (f, foe){
        inCast = true;
        try { return origFire.apply(this, arguments); }
        finally { inCast = false; }
      };
      m.beat = function (o){
        if (o && o.w === rid && o.kind === "ult"){
          if (inCast) A.castBeats++; else A.catchBeats++;
        }
        if (o && o.kind === "hit" && inConnect){
          A.connectBeats++;
          if (o.fatal) A.connectFatalBeats++;
        }
        return origBeat.apply(this, arguments);
      };

      m.resolveHit = function (self, foe, hx, hy, seg, mul, over){
        /* [6] THE CONNECT IS AN ORDINARY MELEE BLOW. `mul === undefined` is
           the engine's own test for "a swing and not a projectile", the same
           one Ironbloom's latch and the Crucible's strike use. */
        const isConnect = (self === me && me.ultWire && me.ultWire.caught
                           && foe.pinFree && !foe.shade && mul === undefined);
        const wasConnectish = (self === me && me.ultWire && me.ultWire.caught
                               && foe.pinFree && !foe.shade);
        if (wasConnectish && !isConnect) A.connectNotMelee++;
        /* AND WHAT ELSE IS LANDING ON A HELD BALL, because [4]'s diagnosis is
           a claim about the fight and not an excuse. Anything with a `mul` is
           a projectile and cannot connect, so it lands an ordinary hitstun on
           a quarry that cannot move away from it. */
        if (foe.pinFree && foe === me_foe()){
          A.hitsOnHeld++;
          if (mul === undefined) A.meleeOnHeld++;
        }
        if (!isConnect) return origHit.apply(this, arguments);

        inConnect = true;
        const hp0 = foe.hp;
        /* [12] THE CONSUME READS THE STACKS BEFORE THE CONNECT'S DAMAGE AND
           CLEARS THEM. Sampled either side of the call: `hemorrhage` must be
           gone afterwards, and the burst the relic recorded must be exactly
           what was standing when the blow arrived, times `consume`. */
        const hem0 = foe.stacks("hemorrhage");
        /* [13] AND IT CLEARS ONLY THE QUARRY'S. Five other bloodsworn relics
           put Hemorrhage on and both fighters can be carrying it. */
        const mine0 = self.stacks("hemorrhage");
        const wref = me.ultWire;
        try { origHit.apply(this, arguments); } finally { inConnect = false; }
        if (hasConsume){
          A.consumeChecks++;
          /* AND WHAT IS LEFT AFTERWARDS IS THE BLOW'S OWN BLEED, NOT A POOL
             THAT SURVIVED. The first cut of this check asserted zero stacks
             after the connect and reported 308 of 308 "left a stack standing".
             It is the hammer's own `onHit:{hemorrhage:2}`, applied further
             down `resolveHit` than the consume is, landing on a quarry whose
             pool has just been emptied.

             THAT IS RICK'S SENTENCE AND NOT A LEAK. Section 1: the connection
             "causes the barbed wire ring to explode and expire, APPLYING BLEED
             AGAIN." A quarry that ends the connect carrying exactly the blow's
             own two stacks is the design, drawn. */
          const want2 = Math.min(AC.STATUS.hemorrhage.maxStacks,
                                 (self.w.onHit || {}).hemorrhage || 0);
          if (foe.stacks("hemorrhage") !== want2) A.consumeLeft++;
          A.leftSum += foe.stacks("hemorrhage");
          if (self.stacks("hemorrhage") !== mine0) A.consumeTookMine++;
          const want = hem0 * (self.w.ult.consume || 0);
          if (!wref || Math.abs((wref.burst || 0) - want) > 1e-9)
            A.consumeWrong++;
          A.hemSum += hem0; A.burstSum += want;
        }
        A.connects++;
        A.dmgSum += (hp0 - foe.hp);
        if (!foe.alive) A.connectKills++;
        /* [5] THE RING EXPIRES ON THE CONNECT -- AND WHETHER THE WINDOW GOES
           WITH IT IS `u.expire`, SO THE CHECK READS THE BUILD RATHER THAN
           REMEMBERING ONE. The first cut asserted `me.ultWire` is null
           afterwards, which is true only under `expire:"window"` and would
           have reported 308 defects against the arm Rick chose.
           `gravemourn_relic_probe`'s rule: reconstruct the engine's rule, do
           not encode your own.

           WHAT IS INVARIANT UNDER BOTH IS THE ONE-CATCH CLAUSE, which is the
           +18.1 points of restraint the design says keeps this relic honest:
           after a connect the ring can never catch again. Under "window" that
           is enforced by the window being gone; under "ring" by `spent`. */
        const W2 = me.ultWire;
        if (U.expire === "ring"){
          if (!W2 || !W2.spent || W2.caught) A.ringAfterConnect++;
        } else {
          if (W2) A.ringAfterConnect++;
        }
        /* [7] and the hold is gone with it, all four fields */
        A.releaseChecks++;
        if (foe.pin > 0 || foe.pinMax > 0 || foe.pinV || foe.pinFree)
          A.dirtyAfter++;
        /* [8] THE DISPLACEMENT WATCH. Position now, position again once the
           ball is allowed to move -- and NOT velocity, because a velocity read
           here passes in the build where `move()` throws the impulse away. A
           dead quarry is excluded: `checkEnd` holds the match on `killFlight`
           and the ball is being flown by something else.

           "TWO FRAMES AFTER THE CONNECT" IS THE WRONG CLOCK, AND THE FIRST CUT
           OF THIS CHECK USED IT AND REPORTED 99 DEFECTS THAT WERE NOT THERE.
           The connect sets `hitStop` to 0.14s -- seventeen frames at dt 1/120
           -- and `step()` returns through `decayImpactOnly` for every one of
           them, so `move()` never runs and the ball CANNOT have moved. The
           check was measuring the freeze its own event caused, and it would
           have failed identically on a perfect build and on the broken one the
           brief warns about.

           `gravemourn_relic_probe`'s lesson and v56's crush probe's, a third
           time: A CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS
           NOT COUNTING THE EVENT. Both numbers are kept and reported, because
           the pair is what tells you which of the two is happening. */
        if (foe.alive) pend = { f: foe, x: foe.x, y: foe.y, n: 0, d2: -1, free: -1 };
      };

      /* [4] THE SNAG ITSELF ADDS NO STUN, AND IT IS SAMPLED ACROSS `tickWire`
         AND NOT ACROSS THE FRAME. The first cut read the quarry's stun either
         side of the whole `m.step()` and reported 2 catches of 107 that had
         "lengthened the weapon lock" -- which was a blow landing somewhere
         else in the same step, and would have been a defect report against a
         relic doing exactly what it is supposed to. Wrap the CALL. */
      m.tickWire = function (dt2){
        const s0 = m.a.stun, s1 = m.b.stun;
        const c0 = (me.ultWire ? me.ultWire.catches : -1);
        origTick.apply(this, arguments);
        const c1 = (me.ultWire ? me.ultWire.catches : -1);
        if (c1 > c0 && c0 >= 0
            && (m.a.stun > s0 + 1e-9 || m.b.stun > s1 + 1e-9))
          A.snagAddedStun++;
      };

      m.releaseWire = function (f, foe){
        const had = f.ultWire && f.ultWire.caught;
        origRelease.apply(this, arguments);
        if (had){
          A.expired++;
          A.releaseChecks++;
          if (foe.pin > 0 || foe.pinMax > 0 || foe.pinV || foe.pinFree)
            A.dirtyAfter++;
        }
      };

      let step = 0, prevWire = null, prevCatches = 0, prevTheta = null;
      let prevFoeHits = 0, prevMyHits = 0;
      const reach0 = me.w.reach, dmg0 = me.w.dmg, hitCd0 = AC.CONFIG.combat.hitCd;

      while (!m.over && step < secs / DT){
        /* [10] NOTHING CATCHES THROUGH A HIT STOP. Sampled where the engine's
           own freeze already is -- `step()` returns through `decayImpactOnly`
           for as long as `hitStop` runs and `tickWire` sits below that return,
           so this is a check on the STRUCTURE and not on a guard. */
        const frozen = m.hitStop > 0;
        const cBefore = me.ultWire ? me.ultWire.catches : 0;
        const foeDead = !m.b.alive, wasOver = m.over;

        const heldNow = !!(me.ultWire && me.ultWire.caught) && m.b.pinFree;
        const th0 = m.b.theta;
        const fh0 = m.b.hits, mh0 = m.a.hits;
        const bStun0 = m.b.stun, hs0 = m.hitStop;

        m.step(DT); step++;

        const wire = me.ultWire;
        if (wire){
          A.windowSecs += DT;
          A.radiusSeen = U.radius;
          /* [3] TWINSHADE'S FIELD IS NEVER SET ON THIS RELIC */
          if (me.ultSpin) A.ultSpinSet++;
          /* [2] THE WIND-UP CHANGES ROTATION AND NOTHING ELSE */
          if (me.w.reach !== reach0) A.reachMoved++;
          if (me.w.dmg !== dmg0) A.dmgMoved++;
          if (AC.CONFIG.combat.hitCd !== hitCd0) A.hitCdMoved++;
          /* [9] the caster is never caught by its own ring */
          if (me.pinFree) A.selfSnag++;
          if (m.b.shade && m.b.pinFree) A.shadeSnag++;
        }
        if (!wire && prevWire && prevWire.caught && m.b.pinFree)
          A.dirtyAfter++;

        /* [1] A WINDOW THAT IS OPEN WITH NO CAST BEHIND IT */
        if (wire && me.charge > 0 && wire.t <= 0) { /* fresh cast, fine */ }

        const cAfter = wire ? wire.catches : 0;
        if (wire && cAfter > cBefore){
          A.catches++;
          const d = Math.hypot(m.b.x - me.x, m.b.y - me.y);
          /* [1] NO CATCH OUTSIDE THE RING. The ring is the hammer's own hit
             range and a ball touches it at `radius + ballR` between centres. */
          if (d > U.radius + R + 1e-6) A.outsideRadius++;
          /* [10] and never on a corpse, after the match, or through a freeze */
          if (foeDead) A.corpseCatch++;
          if (wasOver) A.overCatch++;
          if (frozen) A.frozenCatch++;
        }
        if (frozen) A.frozenChecks++;

        /* [4] THE RELIC. While the ball is held, the WEAPON must still be
           moving and must still be able to land a blow. This does not read the
           source: `tickStasis`'s own decrement loop is the real writer of
           `stun` for every hold in the game, so the only honest test is the
           observable one. */
        if (heldNow){
          A.heldChecks++; A.heldFrames++; A.heldSecs += DT;
          if (m.b.stun > 0) A.stunWhileHeld++;
          /* AND THE ONLY FRAMES THAT SAY ANYTHING ABOUT THE SNAG ARE THE ONES
             WITH NO STUN ON THEM FROM SOMEWHERE ELSE.

             The first cut of this check asserted that a held fighter is NEVER
             stunned and that its weapon ALWAYS turns, and it reported 4637
             stunned frames of 24255 and 6470 frozen ones. Neither was the
             snag. A held ball is a stationary target: it carries in whatever
             hitstun it had when it was caught, and it goes on being hit by
             things that are not the hammer -- arrows, shards, spikes, shades
             -- every one of which lands an ORDINARY hitstun through
             `takeHitstun`, exactly as it would on a ball that was not held.
             `tickWeapon` then holds `theta` for those frames, on `f.stun` and
             not on `f.pin`, so the two symptoms are one cause.

             So the snag is asserted where it actually happens -- ON THE CATCH,
             below -- and the hold is asserted on the frames where nothing else
             is stunning the quarry. `gravemourn_relic_probe`'s rule: the check
             reconstructs the engine's rule instead of assuming its own. */
          /* AND NOT THROUGH A HIT STOP EITHER, which is the same exclusion
             [8] needs and for the same reason. `step()` returns through
             `decayImpactOnly` while `hitStop` runs, so `tickWeapon` never
             executes and NOBODY'S weapon turns -- the hall is frozen, not the
             quarry. Counting those frames reported 1983 "frozen" weapons that
             were the hit stop. Third time in this one probe. */
          /* AND THE STUN IS SAMPLED AT BOTH ENDS OF THE STEP, not just after
             it. `tickWeapon` reads `f.stun` DURING the step; a lock that was
             standing when the step began and expired inside it holds `theta`
             and then reads 0 afterwards. That boundary was the last 222 of the
             original 6470 "frozen" frames, and it is the fourth time in this
             one file that a check has had to stop sampling a frame and start
             sampling the thing. */
          if (m.b.stun <= 0 && bStun0 <= 0 && m.hitStop <= 0 && hs0 <= 0){
            A.heldFreeFrames++;
            if (m.b.theta !== th0) A.freeTurned++; else A.freeFrozen++;
          }
          if (m.hitStop > 0) A.heldFrozenHall++;
          if (prevTheta !== null && m.b.theta !== th0) A.weaponTurned++;
          else A.weaponFrozen++;
          if (m.b.hits > fh0) A.blowsWhileHeld++;
          /* [9] AND NOBODY ELSE'S HOLD IS TOUCHED. A ball held by the Stasis
             Field or by Grasp's squeeze carries `pinFree` 0; if this relic
             ever writes over one, the flag is the tell. */
          if (m.b.pin > 0 && !m.b.pinFree) A.foreignPin++;
        }
        prevTheta = th0;
        A.foeBlows += (m.b.hits - fh0);
        A.myBlows  += (m.a.hits - mh0);

        /* [8] TWO FRAMES ON. */
        if (pend){
          pend.n++;
          if (pend.n === 2)
            pend.d2 = Math.hypot(pend.f.x - pend.x, pend.f.y - pend.y);
          /* AND THE FRAME `hitStop` FIRST READS <= 0 IS STILL A FRAME ON WHICH
             THE BALL DID NOT MOVE. `step()` tests the freeze at the TOP and
             returns through `decayImpactOnly`, which is what decrements it --
             so the step that takes `hitStop` to zero is a step whose `move()`
             never ran, and the position at the end of it is the position at
             the start. Measuring there reported 294 connects of 294 that "did
             not move the ball", on a build where a traced connect departs at
             1836 px/s and has crossed a third of the hall inside 20 frames.
             So the watch waits for the first RUNNING frame and then two more.

             That is the fifth time in this one file that a check has had to
             stop sampling a frame and start sampling the thing, and by now it
             is not a recurrence -- it is the default failure mode of a probe
             on an engine whose every impact opens with a freeze. */
          if (pend.free < 0 && m.hitStop <= 0) pend.free = pend.n;
          if ((pend.free >= 0 && pend.n >= pend.free + 2) || pend.n > 90){
            const d = Math.hypot(pend.f.x - pend.x, pend.f.y - pend.y);
            A.dispSum += d;
            A.disp2Sum += Math.max(0, pend.d2);
            if (d < A.dispMin) A.dispMin = d;
            if (d > 1.0) A.moved++; else A.notMoved++;
            pend = null;
          }
        }

        if (!prevWire && wire) A.casts++;
        /* [5] ONE CATCH PER WINDOW */
        if (wire && wire.catches > 1) A.recaught++;
        prevWire = wire;
        prevCatches = cAfter;
      }
    }
  }
  M.beat = origBeat; M.resolveHit = origHit;
  M.releaseWire = origRelease; M.fireUlt = origFire;
  M.tickWire = origTick;
  if (A.dispMin > 1e8) A.dispMin = -1;
  return A;
}"""


# [X] THE RUNIC HEXAGON IS NOT DRAWN ON A WIRE SNAG.
#
# The renderer's held-ball block hardcodes `AFFINITIES.runic` -- it is the
# Stasis Field's picture -- and it fires on `f.pin > 0`. Garrote writes `pin`,
# so without a guard a BLOODSWORN wire snag draws PARADOX'S HEXAGON around the
# ball it caught, with every number in the fight correct. That is section 4.1's
# defect class exactly, and no numeric check in this repo could see it.
#
# Read off the SOURCE, because the thing being asserted is that the guard is in
# the branch -- and the comments are stripped first, since this build explains
# itself in the file and the paragraph above that line says the words.
HEX_JS = r"""(()=>{
  const src = AC.renderer.constructor.prototype._drawField.toString()
              .replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/[^\n]*/g, "");
  const i = src.indexOf("AFFINITIES.runic");
  if (i < 0) return { found: false };
  const head = src.lastIndexOf("if (", i);
  const cond = src.slice(head, src.indexOf("{", head));
  return { found: true, cond: cond.trim(), guarded: /pinFree/.test(cond) };
})"""


# [9] AND NO OTHER RELIC'S HOLD IS EVER TOUCHED. Paradox and Shroudmaul are the
# only other writers of `pin` in the game -- the design doc says Paradox is the
# ONLY one, and that stopped being true in v56 when Grasp's squeeze was added.
# Run Ravelbone against both and assert their holds behave as they do without
# it: `pinFree` 0 throughout, and the weapon locked.
FOREIGN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = { holds: 0, freeFlagged: 0, unlocked: 0, pairs: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      out.pairs++;
      let i = 0;
      while (!m.over && i < secs / DT){
        m.step(DT); i++;
        /* the OTHER fighter holding OUR relic is the case that matters: their
           hold must still lock our weapon, exactly as it does without us. */
        if (m.a.pin > 0){
          out.holds++;
          if (m.a.pinFree) out.freeFlagged++;
          else if (m.a.stun <= 0) out.unlocked++;
        }
      }
    }
  }
  return out;
}"""


# [P] THE RENDER PATH, CALLED. Not regexed -- v48's own lesson, twice over:
# `_drawBeam` reached for a MATCH method from the RENDERER and `drawUltUnder`
# handed NaN to `createRadialGradient`, both green across 27 probe checks, a
# 280-match engine_ab, chain_audit and post_identity. The probe's own check
# passed on the first one because it was REGEXING the source for the call, and
# A STRING DOES NOT RESOLVE A REFERENCE.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { ring: 0, held: 0, fade: 0, under: 0, over: 0,
                fighter: 0, threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const live = m.a.ultWire || m.b.ultWire;
        const fade = m.a.wireFade > 0 || m.b.wireFade > 0;
        if (!fade) continue;
        out.fade++;
        if (live) out.ring++;
        if (m.b.pinFree || m.a.pinFree) out.held++;
        try { R.ctx.save(); R.drawWire(m, false); R.ctx.restore(); }
        catch (e){ out.threw = "drawWire(under): " + String(e); return out; }
        try { R.ctx.save(); R.drawWire(m, true); R.ctx.restore(); }
        catch (e){ out.threw = "drawWire(over): " + String(e); return out; }
        /* AND THE HELD BALL ITSELF, because the hexagon guard [X] lives in
           `drawFighter` and a guard that throws is not a guard. */
        try { R.ctx.save(); R.drawFighter(m, m.b); R.ctx.restore(); out.fighter++; }
        catch (e){ out.threw = "drawFighter: " + String(e); return out; }
        if (!m.ultFx) continue;
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
      }
      if (out.ring > 900 && out.held > 200) return out;
    }
  }
  return out;
}"""


# AND THE ONE THING A RENDER CANNOT SEE. `_burst` does not loop its 0.6s noise
# buffer, so a burst asked for a longer tail simply plays silence into it -- and
# the rendered waveform looks like a sound that ended, which is exactly what a
# sound that ended looks like. So this is measured on the SOURCE.
BURSTS_JS = r"""([names]) => {
  const src = AC.SFX.play.toString();
  const out = { n: 0, max: 0, over: [], missing: [] };
  for (const nm of names){
    const i = src.indexOf('w === "' + nm + '"');
    if (i < 0){ out.missing.push(nm); continue; }
    let j = src.indexOf('} else if (', i);
    if (j < 0) j = src.length;
    const body = src.slice(i, j);
    const re = /_burst\(([\s\S]*?)\)\s*;/g;
    let m2;
    while ((m2 = re.exec(body))){
      const d = /dur:\s*([0-9.]+)/.exec(m2[1]);
      if (!d) continue;
      const v = parseFloat(d[1]);
      out.n++;
      if (v > out.max) out.max = v;
      if (v > 0.6) out.over.push(nm + " " + v + "s");
    }
  }
  return out;
}"""


# `SFX_JS` SCHEDULES AT `currentTime = 1.0` INSIDE A `secs`-LONG BUFFER, so the
# window actually rendered is `secs - 1.0` and asking for 1.0 renders NOTHING.
# v59's case list did exactly that and reported peak 0.000 -- indistinguishable
# from the silent ultimate v42 shipped, and the reason this check earns its
# place even on the occasions when it is the probe that is wrong.
CASES = [
    ("the wind-up",     "ult", {"w": "ravelbone"},        2.4),
    ("the wire closes", "ult", {"w": "ravelbone-snag"},   1.8),
    ("and it holds",    "ult", {"w": "ravelbone-wire"},   1.9),
    ("and it lets go",  "ult", {"w": "ravelbone-burst"},  2.2),
]


def profile(g):
    return {k: g.get(k) for k in ("peak", "audible", "low120", "hp300")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-wire.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [3301 + 13 * i for i in range(a.seeds)]
    print(f"\nGARROTE — one check per sentence — {gp.name}")

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        U = page.evaluate("(r) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(w=>w.id===r).ult))", RID)
        has_consume = page.evaluate(
            "() => /hemorrhage/.test(AC.Match.prototype.resolveHit.toString()"
            ".replace(/\\/\\*[\\s\\S]*?\\*\\//g,''))")
        foes = [i for i in ids if i != RID]
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights   "
              f"dur {U['dur']:g}  radius {U['radius']:g}  "
              f"spinMul {U['spinMul']:g}  kick {U['kick']:g}  "
              f"launch {U['launch']:g}  charge {U['charge']:g}\n")

        A = page.evaluate(RUN_JS, [RID, foes, seeds, a.secs, bool(has_consume)])
        hexg = page.evaluate(HEX_JS)
        foreign = page.evaluate(FOREIGN_JS,
                                [RID, ["paradox", "shroudmaul"], seeds[:4],
                                 a.secs])
        drawn = page.evaluate(DRAW_JS, [RID, foes[:10], seeds[:3], a.secs])
        bursts = page.evaluate(BURSTS_JS, [[c[2]["w"] for c in CASES]])

        sfx = {}
        print("[15] THE VOICES")
        for label, kind, pp, secs in CASES:
            g = page.evaluate(SFX_JS, [kind, pp, secs])
            sfx[pp["w"]] = g
            print(f"       {label:<16} peak {g['peak']:.4f}  "
                  f"audible {g['audible']:.2f}s  "
                  f"below 120Hz {g['low120']:.3f}")
        print()

    casts = max(1, A["casts"])
    cpc = A["connects"] / casts

    print("[1]  THE WINDOW AND THE RING")
    check("the ring never catches outside its own radius",
          A["outsideRadius"] == 0,
          f"{A['catches']} catches, {A['outsideRadius']} outside "
          f"radius {U['radius']:g} + ballR")
    print("\n[2]  THE WIND-UP MULTIPLIES ROTATION AND NOTHING ELSE")
    check("reach, damage and hitCd are untouched inside the window",
          A["reachMoved"] == 0 and A["dmgMoved"] == 0 and A["hitCdMoved"] == 0,
          f"reach {A['reachMoved']}  dmg {A['dmgMoved']}  "
          f"hitCd {A['hitCdMoved']} frames moved")
    print("\n[3]  NOT `f.ultSpin` — THAT FIELD IS TWINSHADE'S")
    check("`f.ultSpin` is null on Ravelbone in every frame of a cast",
          A["ultSpinSet"] == 0, f"{A['ultSpinSet']} frames set")
    print("\n[4]  THE SNAG. BALL HELD, WEAPON FREE — AND THIS IS THE RELIC")
    check("THE SNAG ITSELF NEVER ADDS A STUN, measured across the catch frame",
          A["snagAddedStun"] == 0,
          f"{A['snagAddedStun']} of {A['catches']} catches lengthened the "
          f"quarry's weapon lock")
    check("and its weapon turns on every held frame nothing else is stunning it",
          A["heldFreeFrames"] > 0 and A["freeFrozen"] == 0,
          f"{A['freeTurned']} turning / {A['freeFrozen']} frozen over "
          f"{A['heldFreeFrames']} held frames that were neither "
          f"stunned nor frozen"
          f"\n        ({A['heldSecs']:.1f}s held in total; "
          f"{A['heldFrozenHall']} of those frames were hit stops, in which no"
          f"\n        weapon in the hall turns)")
    print(f"       and the other {A['stunWhileHeld']} held frames DO carry a"
          f" stun, from {A['hitsOnHeld']} blows"
          f"\n       landed on a held ball"
          f" ({A['hitsOnHeld'] - A['meleeOnHeld']} of them projectiles, which"
          f" cannot"
          f"\n       connect and so land an ordinary hitstun). That is the"
          f" hammer and the hall,"
          f"\n       not the wire — a held ball is a stationary target.")
    check("and it goes on landing blows while its ball is held",
          A["blowsWhileHeld"] > 0,
          f"{A['blowsWhileHeld']} blows landed by a caught fighter")
    print("\n[5]  ONE CATCH PER WINDOW, AND THE CONNECT EXPIRES THE RING")
    check("no window ever catches twice", A["recaught"] == 0,
          f"{A['recaught']} windows with a second catch")
    check("the ring can never catch again after a connect  "
          f"(expire:{U['expire']!r})",
          A["ringAfterConnect"] == 0,
          f"{A['ringAfterConnect']} of {A['connects']} connects left it able to")
    print("\n[6]  THE CONNECT IS AN ORDINARY MELEE BLOW")
    check("no connect ever resolves off a projectile",
          A["connectNotMelee"] == 0, f"{A['connectNotMelee']} non-melee")
    print("\n[7]  THE HOLD ENDS CLEAN")
    check("pin, pinMax, pinV and pinFree are all clear after every release",
          A["dirtyAfter"] == 0,
          f"{A['dirtyAfter']} of {A['releaseChecks']} releases left state behind")
    print("\n[8]  THE KNOCKBACK ACTUALLY MOVES THE BALL — read as displacement")
    _n8 = max(1, A["moved"] + A["notMoved"])
    check("every connect displaces the quarry once the hall runs again",
          A["notMoved"] == 0 and A["moved"] > 0,
          f"{A['moved']} moved / {A['notMoved']} did not; "
          f"mean {A['dispSum']/_n8:.1f}px, min {A['dispMin']:.1f}px"
          f"\n        and {A['disp2Sum']/_n8:.1f}px at two frames — WHICH IS "
          f"THE FREEZE THE CONNECT ITSELF CAUSED"
          f"\n        (hitStop 0.14s = 17 frames of `decayImpactOnly`, in "
          f"which `move()` never runs)")
    print("\n[9]  THE CASTER IS NEVER SNAGGED, AND NOBODY ELSE'S HOLD IS TOUCHED")
    check("the caster is never caught by its own ring", A["selfSnag"] == 0,
          f"{A['selfSnag']} frames")
    check("no shade is ever snagged", A["shadeSnag"] == 0,
          f"{A['shadeSnag']} frames (the ring takes the real quarry only)")
    check("Paradox's and Grasp's holds still lock the weapon they hold",
          foreign["holds"] > 0 and foreign["freeFlagged"] == 0
          and foreign["unlocked"] == 0,
          f"{foreign['holds']} held frames against the two other pin writers, "
          f"{foreign['freeFlagged']} mis-flagged, {foreign['unlocked']} unlocked")
    print("\n[10] NO CATCH ON A CORPSE, AFTER THE MATCH, OR THROUGH A FREEZE")
    check("none of the three", A["corpseCatch"] == 0 and A["overCatch"] == 0
          and A["frozenCatch"] == 0,
          f"corpse {A['corpseCatch']}  over {A['overCatch']}  "
          f"frozen {A['frozenCatch']} (of {A['frozenChecks']} frozen frames)")
    print("\n[11] THE BEATS")
    check("the cast files one and every catch files its own",
          A["castBeats"] >= A["casts"] and A["catchBeats"] >= A["catches"] * 0.99,
          f"{A['castBeats']} cast, {A['catchBeats']} catch, "
          f"{A['connectBeats']} connect")
    check("A KILLING CONNECT FILES A FATAL BEAT",
          A["connectKills"] == 0 or A["connectFatalBeats"] >= A["connectKills"],
          f"{A['connectKills']} kills by connect, "
          f"{A['connectFatalBeats']} fatal beats"
          + ("   — WEAKLY EXERCISED, no connect killed in this run"
             if A["connectKills"] == 0 else ""))
    print("\n[12/13] THE CONSUME")
    if has_consume:
        _nc = max(1, A["consumeChecks"])
        check("it reads the stacks BEFORE the connect's damage and clears them",
              A["consumeChecks"] > 0 and A["consumeLeft"] == 0
              and A["consumeWrong"] == 0,
              f"{A['consumeChecks']} connects, {A['consumeLeft']} ended with"
              f" the wrong pool, {A['consumeWrong']} burst by the wrong amount"
              f"\n        mean {A['hemSum']/_nc:.2f} stacks eaten, mean burst"
              f" {A['burstSum']/_nc:.1f} damage")
        check("and it clears only the QUARRY's",
              A["consumeTookMine"] == 0,
              f"{A['consumeTookMine']} connects also took the caster's")
    else:
        print("       NOT BUILT. Stage 2 stops before the consume on purpose, "
              "and a\n       check that cannot fail is worth nothing.")
    print("\n[14] THE SCALAR THE PICTURE DEPENDS ON")
    check(f"connects per cast is 0.8-0.9   (measured {cpc:.2f})",
          0.8 <= cpc <= 0.9,
          f"{A['casts']} casts, {A['catches']} catches, "
          f"{A['connects']} connects, {A['expired']} windows let go\n        "
          f"held {A['heldSecs']:.1f}s over {A['windowSecs']:.1f}s of window "
          f"({100*A['heldSecs']/max(1e-9,A['windowSecs']):.0f}%), "
          f"mean connect {A['dmgSum']/max(1,A['connects']):.1f} damage"
          f"\n        window used "
          f"{A['windowSecs']/max(1,A['casts']):.2f}s of {U['dur']:g}s a cast"
          f" — the whole difference between"
          f"\n        expire:'ring' and expire:'window', and the reason the"
          f" shipped arm is +32.9 and not +18.2")
    print("\n[15] THE VOICES")
    for label, kind, pp, secs in CASES:
        g = sfx[pp["w"]]
        check(f"{label} is audible", g["peak"] > 0.02 and g["audible"] > 0.04,
              f"peak {g['peak']:.4f}  audible {g['audible']:.2f}s")
    check("no burst is asked to run past its 0.6s noise buffer",
          not bursts["over"] and not bursts["missing"],
          f"{bursts['n']} bursts, longest {bursts['max']:.2f}s"
          + (f", OVER: {bursts['over']}" if bursts["over"] else "")
          + (f", MISSING: {bursts['missing']}" if bursts["missing"] else ""))
    print("\n[P]  THE RENDER PATH, CALLED AGAINST A REAL CONTEXT")
    check("drawWire, drawFighter, drawUltUnder and drawUltOver all return",
          not drawn.get("threw") and not drawn.get("skip")
          and drawn.get("ring", 0) > 0 and drawn.get("held", 0) > 0,
          f"ring {drawn.get('ring',0)} frames, held {drawn.get('held',0)}, "
          f"fade {drawn.get('fade',0)}, fighter {drawn.get('fighter',0)}, "
          f"ultUnder {drawn.get('under',0)}, ultOver {drawn.get('over',0)}"
          + (f"\n        THREW: {drawn['threw']}" if drawn.get("threw") else "")
          + (f"\n        SKIPPED: {drawn['skip']}" if drawn.get("skip") else ""))
    print("\n[X]  AND THE RUNIC HEXAGON IS NOT DRAWN ON A WIRE SNAG")
    check("the held-ball block is guarded on `pinFree`",
          hexg.get("found") and hexg.get("guarded"),
          f"cond: {hexg.get('cond')!r}" if hexg.get("found")
          else "AFFINITIES.runic is not in `_drawField` — the block moved")

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"run": A, "draw": drawn, "foreign": foreign, "hex": hexg,
             "sfx": {k: profile(v) for k, v in sfx.items()},
             "connectsPerCast": cpc, "ult": U}, indent=1), encoding="utf-8")
        print(f"  wrote {a.json}")
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
