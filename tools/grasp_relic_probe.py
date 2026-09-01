#!/usr/bin/env python3
"""GRASP, ASSERTED AGAINST THE BUILD -- one check per sentence of §5.

    python grasp_relic_probe.py --game ../02-chain/sc-grasp.html

Layer 2 of `06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md` (§5). Twelve checks, plus
the render path CALLED, which is v48's lesson and not one of the twelve.

  [1]  THE WINDOW opens on the charge and closes on `dur` or on the nth grab,
       never otherwise and never twice at once
  [2]  EXACTLY `n` GRABS TO A TRUE STUN, counted off the engine's own events
       rather than recomputed from the config
  [3]  A GRAB DOES NOT TOUCH `stunDR`, and `takeHitstun` is never called
  [4]  THE TRUE STUN CANCELS A WIND-UP AND AN ORDINARY GRAB DOES NOT
  [5]  NO GRAB DEALS DAMAGE AND NONE APPLIES CURSE
  [6]  FOE ONLY -- asserted in a Twinshade match
  [7]  NO GRAB RESOLVES AFTER `m.over` OR ON A CORPSE
  [8]  THE HAND IS PER-FIGHTER -- six other-relic matches after a cast are
       bit-identical to the same six before it
  [9]  `f.pin` IS NEVER WRITTEN BY THIS RELIC, in any match
  [10] THE ULT FILES A BEAT AND THE TRUE STUN FILES ITS OWN; the four
       ordinary grabs file none
  [11] `held` SECONDS A FIGHT IS 6.5-7.0 -- the scalar the whole design is
       priced on. REPORTED EVERY RUN.
  [12] EVERY VOICE RENDERS TO SOMETHING AUDIBLE in an OfflineAudioContext
  [P]  the render path is CALLED against a real 2D context

## [3] IS THE ONE THIS PROBE EXISTS FOR

`takeHitstun` caps at `stunMax` 0.26s and divides each application by
`1 + 0.55 x stunDR`. Route the grabs through it and the second grab onward is
eaten: five grabs become one grab and a rumour. **The mechanic still "works" by
every invariant in this repo** -- the window opens, the counter counts, the
crush lands, the beats are filed, and no probe fails. The only symptom is a
`held` column that does not move when the knobs do, and nothing in `tools/`
reads that column except [11].

## [11] IS THE ONE EVERYTHING ELSE IS TUNED AGAINST

`grab_lab.py`, fourteen arms at 702 fights each:

    lift = +3.1 + 2.62 x held seconds     r2 = 0.79
    residual sd 2.7pp against a per-arm SE of 5.3pp

The residuals are smaller than the measurement error, so window length,
cadence, grab hold, true-stun length, grab count and "then dissipates" are six
ways of writing one number. Tune on `held`; it is 30x cheaper to measure than a
win rate and it is what the win rate is made of.

## AND THE CHECKS RECONSTRUCT THE ENGINE'S RULE RATHER THAN ASSUMING THEIR OWN

Three checks in `gravemourn_relic_probe` reported defects that were not there,
all three because the probe had written down its own model of a rule and the
engine legitimately did something else. So `n`, `dur`, `radius`, `cadence`,
`grabStun` and `trueStun` are read off `w.ult` here and never typed in, and [4]
asks what `breakSpin` ACTUALLY does rather than what the brief says the three
wind-ups are -- Reprisal's draw is not a `breakSpin` target and never was, and
a probe that assumed the brief would have failed on the engine.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "shroudmaul"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


META_JS = r"""([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const P = AC.Match.prototype;
  /* THE BLOCK COMMENT IS REMOVED AS A BLOCK. This codebase teaches in its
     comments and every string below appears in the paragraph explaining it --
     `curse_check` fired on its own explanation once, and this builder refused
     to write on its §4.5 paragraph while it was being written. */
  const strip = f => f.toString().replace(/\/\*[\s\S]*?\*\//g, "")
                                 .replace(/\/\/[^\n]*/g, "");
  const tg = strip(P.tickGrasp);
  return {
    u: JSON.parse(JSON.stringify(w.ult)),
    dmg: w.dmg, aff: w.aff, shape: w.shape,
    onHit: JSON.parse(JSON.stringify(w.onHit || {})),
    relics: AC.WEAPONS.length,
    src: {
      /* THE CAST RESOLVES NOTHING. `u.dmg` is 0 and there is no `apply`. */
      castIsEmpty: w.ult.dmg === 0,
      kindIsGrip: w.ult.kind === "grip",
      noApply: !w.ult.apply,
      /* §4.1: the single easiest way to build this wrong */
      noHitstun: !/takeHitstun/.test(tg),
      /* §4.5, NARROWED. The squeeze pins and nothing longer does — Rick:
         "hitstun should freeze the enemy ball correct?" It does not, and that
         is why he could not see it. What must never come back is the FULL
         pin, measured at -3.3 points at identical held seconds. */
      pinIsSqueeze: /pin = Math\.max\(foe\.pin, u\.squeeze\)/.test(tg)
                    && !/pin = Math\.max\([^)]*(grabStun|trueStun|hold)\)/.test(tg),
      /* §8: no damage, no curse */
      noDamage: !/this\.hurt|pushCurse|apply\("curse"/.test(tg),
      /* §4.2: exactly ONE true-stun application site in this function */
      oneTrueSite: (tg.match(/breakSpin/g) || []).length === 1,
      /* the window is per-FIGHTER, never on the match and never in `shots` */
      perFighter: /ultGrasp/.test(tg) && !/this\.shots/.test(tg),
      /* and the art hangs off the fighter, which is v54 §2a */
      artOnFighter: /f\.ultGrasp|f\.graspFade/.test(strip(AC.renderer.constructor
                     .prototype.drawGrip)),
    },
  };
}"""


# ONE instrumented match per (foe, seed). EVERY HOOK FORWARDS WITH `arguments`
# -- v44's warning, which is that a wrapper with a FIXED ARITY silently
# measures the old build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const A = { fights: 0, casts: 0, closes: 0, badClose: 0, doubleOpen: 0,
              grabs: 0, crushes: 0, crushAtN: 0, multiGrab: 0,
              stunDrMoved: 0, hitstunCalls: 0, tickFrames: 0,
              hurtInTick: 0, poolMoved: 0, hpMoved: 0,
              pinMoved: 0, shadeStunned: 0, shadeFrames: 0,
              deadGrab: 0, overGrab: 0, outOfReach: 0,
              beatsInTick: 0, fatalInTick: 0, castBeats: 0,
              breakInTick: 0, breakTrue: 0,
              windForge: 0, windSpin: 0, windBeam: 0,
              windHeldOk: 0, windGrabTouched: 0,
              held: 0, heldFights: 0, maxLive: 0,
              graspSeen: 0, longestWindow: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      A.fights++;

      let inTick = false;
      const oTick = m.tickGrasp.bind(m);
      m.tickGrasp = function(){
        inTick = true;
        /* [3] AND [5] ARE MEASURED ACROSS `tickGrasp` AND NOTHING ELSE.
           A check that photographs a wider span than the claim it is making
           measures the rest of the engine and calls it a defect -- a blade
           blow landing on the same step legitimately moves `stunDR`, the
           pool and the foe's hp, and three checks in
           `gravemourn_relic_probe` failed exactly that way in one session. */
        /* [7]'s DISTANCE, AND THE FIRST CUT PHOTOGRAPHED THE WRONG INSTANT.
           It read the separation BEFORE `m.step`, and `move()` runs in the
           fighter loop ABOVE this tick -- so the quarry the window tests is
           one step further along than the one the probe measured, and 439 of
           738 grabs read as "outside radius". Every one of them was inside it
           when `tickGrasp` looked. Reconstruct the engine's rule; do not
           assume your own. */
        A.callD = Math.hypot(th.x - me.x, th.y - me.y);
        A.callAlive = th.alive && me.alive && !m.over;
        const dr0 = th.stunDR, hp0 = th.hp;
        const pool0 = th.cursePool.join(",") + "|" + me.cursePool.join(",");
        const pin0 = th.pin + "|" + me.pin;
        const shade0 = m.shades.map(s => s.stun).join(",");
        try { return oTick.apply(m, arguments); }
        finally {
          inTick = false;
          A.tickFrames++;
          if (th.stunDR !== dr0) A.stunDrMoved++;
          if (th.hp !== hp0) A.hpMoved++;
          if (th.cursePool.join(",") + "|" + me.cursePool.join(",") !== pool0)
            A.poolMoved++;
          if (th.pin + "|" + me.pin !== pin0) A.pinMoved++;
          if (m.shades.length){
            A.shadeFrames++;
            if (m.shades.map(s => s.stun).join(",") !== shade0) A.shadeStunned++;
          }
        }
      };
      const oHs = th.takeHitstun.bind(th);
      th.takeHitstun = function(){
        if (inTick) A.hitstunCalls++;          // [3]. §4.1, and it is silent
        return oHs.apply(th, arguments);
      };
      const oHurt = m.hurt.bind(m);
      m.hurt = function(){
        if (inTick) A.hurtInTick++;            // [5]
        return oHurt.apply(m, arguments);
      };
      const oBeat = m.beat.bind(m);
      m.beat = function(b){
        if (inTick && b && b.kind === "ult") A.beatsInTick++;
        if (inTick && b && b.fatal) A.fatalInTick++;
        return oBeat.apply(m, arguments);
      };
      const oBreak = m.breakSpin.bind(m);
      m.breakSpin = function(f, reason, trueFor){
        if (inTick){
          A.breakInTick++;
          if (trueFor !== undefined) A.breakTrue++;
          /* [4]. WHAT THE ENGINE ACTUALLY DOES, photographed at the call.
             `breakSpin` holds the Crucible, kills a WINDING Sentinel and
             kills a spike storm; it does NOT touch Reprisal's draw and never
             has. Reconstructing the rule beats asserting the brief's. */
          const hadForge = !!f.ultForge, hadSpin = !!f.ultSpin;
          const hadWind = !!(f.ultBeam && f.ultBeam.phase === "wind");
          const hold0 = f.forgeHold;
          const r = oBreak.apply(m, arguments);
          if (hadForge){ A.windForge++; if (f.forgeHold > hold0) A.windHeldOk++; }
          if (hadSpin){ A.windSpin++; if (!f.ultSpin) A.windHeldOk++; }
          if (hadWind){ A.windBeam++; if (!f.ultBeam) A.windHeldOk++; }
          return r;
        }
        return oBreak.apply(m, arguments);
      };
      const oFire = m.fireUlt.bind(m);
      m.fireUlt = function(f){
        const n0 = m.cine ? m.cine.length : 0;
        const r = oFire.apply(m, arguments);
        /* THE CAST COUNT IS THE ENGINE'S OWN EVENT AND NOT A TRANSITION THE
           PROBE RECONSTRUCTS. The first cut counted `null -> object` after
           each step and came back one short of the beats: a window that opens
           and CLOSES inside one step -- the quarry already in reach, the
           counter already at n on a re-cast -- is never null-to-object on the
           far side of `m.step`. `fireUlt` cannot miss one. */
        if (f === me){ A.castBeats++; A.casts++; }
        return r;
      };

      let step = 0, prevG = null, prevGrabs = 0, live = 0;
      while (!m.over && step < secs / DT){
        const G0 = me.ultGrasp;
        const t0 = G0 ? G0.t : 0, g0 = G0 ? G0.grabs : 0;
        const alive0 = th.alive, over0 = m.over;
        A.callD = Infinity; A.callAlive = true;
        m.step(DT); step++;
        const G1 = me.ultGrasp;

        if (!G0 && G1) A.graspSeen++;      // the transition, kept for the report
        if (G0 && G1 && G0 !== G1) A.doubleOpen++;    // [1]. never twice at once
        if (G0 && G1) A.longestWindow = Math.max(A.longestWindow, G1.t);
        if (G0 && !G1){
          /* [1]. THE THREE WAYS OUT, RECONSTRUCTED. The clock (within one
             step of `dur`), the counter (`grabs` reached `n`), or a corpse /
             the end of the match. Anything else is a window closing for a
             reason the design does not have. */
          A.closes++;
          const byClock = t0 + DT >= G0.dur - 1e-9;
          const byCount = g0 >= U.n || (G0.grabs >= U.n);
          const byEnd = !alive0 || !me.alive || m.over || !th.alive;
          if (!(byClock || byCount || byEnd)) A.badClose++;
        }
        if (G1 && G1.grabs > g0){
          const k = G1.grabs - g0;
          A.grabs += k;
          if (k > 1) A.multiGrab++;                   // one grab a frame
          /* [7]. A grab may not resolve on a corpse or after the match. */
          if (!A.callAlive) A.deadGrab++;
          if (m.over && !over0) A.overGrab++;
          /* THE REACH IS REAL: the grab happened, so the quarry was inside
             `radius` AT THE MOMENT `tickGrasp` LOOKED -- which is after
             `move()` has run, not before the step. */
          if (A.callD > U.radius + 1e-6) A.outOfReach++;
          if (G1.grabs >= U.n){ A.crushes++; A.crushAtN++; }
          A.held += G1.stunFor;
        }
        /* the crush ENDS the window, so the counter is read on the way out */
        if (G0 && !G1 && G0.grabs >= U.n && G0.crush){
          A.crushes++;
          A.crushAtN += (G0.grabs === U.n) ? 1 : 0;
          A.held += G0.stunFor;
        }
        if (G1) live = 1;
      }
      A.heldFights++;
    }
  }
  A.held = +A.held.toFixed(2);
  return A;
}"""


# [6]. FOE ONLY, AND TWINSHADE IS THE TEST -- three bodies on the floor for six
# seconds, and `tickShadeHits` is where v51 §4.3's bug lived. Run separately and
# for longer, because a shade has to be ON THE FLOOR while a grab lands for the
# check to have been exercised at all.
SHADE_JS = r"""([rid, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = { frames: 0, moved: 0, grabsWithShades: 0, grabs: 0 };
  for (const sd of seeds){
    const m = new AC.Match(rid, "twinshade", sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    let inTick = false;
    const oTick = m.tickGrasp.bind(m);
    m.tickGrasp = function(){
      const s0 = m.shades.map(s => s.stun + ":" + s.hp).join(",");
      const n = m.shades.length;
      const g0 = me.ultGrasp ? me.ultGrasp.grabs : 0;
      try { return oTick.apply(m, arguments); }
      finally {
        if (n){
          out.frames++;
          if (m.shades.map(s => s.stun + ":" + s.hp).join(",") !== s0) out.moved++;
          const g1 = me.ultGrasp ? me.ultGrasp.grabs : g0;
          if (g1 > g0) out.grabsWithShades++;
        }
        const g1 = me.ultGrasp ? me.ultGrasp.grabs : g0;
        if (g1 > g0) out.grabs++;
      }
    };
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
  }
  return out;
}"""


# [8]. THE HAND IS PER-FIGHTER. `gravemourn_relic_probe [9d]`'s pattern, and it
# is the check that would have caught the `w.reach` hazard: run six other-relic
# matches, then a Shroudmaul match that CASTS, then the same six again, and
# assert the summaries are identical field for field. Anything this ultimate
# leaves on `w`, on a prototype or in module state shows up here and nowhere
# else in the repo.
LEAK_JS = r"""([rid, pairs, seed]) => {
  const run = () => pairs.map(p => JSON.stringify(AC.simulate(p[0], p[1], seed)));
  const before = run();
  const DT = AC.CONFIG.physics.dt;
  let casts = 0;
  for (const foe of ["emberedge", "axiom", "grudgebearer"]){
    const m = new AC.Match(rid, foe, seed);
    const me = m.a.w.id === rid ? m.a : m.b;
    let step = 0, had = false;
    while (!m.over && step < 120 / DT){
      m.step(DT); step++;
      if (me.ultGrasp && !had){ casts++; had = true; }
      if (!me.ultGrasp) had = false;
    }
  }
  const after = run();
  let bad = 0;
  for (let i = 0; i < before.length; i++) if (before[i] !== after[i]) bad++;
  return { casts, bad, n: before.length };
}"""


# [P]. THE RENDER PATH IS CALLED. v48: TWO picture faults shipped through every
# headless check in this repo and died on the FIRST RENDERED FRAME -- a
# renderer reaching for a Match method, and a NaN handed to
# `createRadialGradient`. The probe that was supposed to catch the first one
# PASSED, because it was REGEXING the source for a name and a string does not
# resolve a reference. So this CALLS the functions against a real 2D context,
# in all three states.
DRAW_JS = r"""([rid, seed]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement("canvas");
  cv.width = 520; cv.height = 800;
  const ctx = cv.getContext("2d");
  const R = AC.renderer, saved = R.ctx;
  const seen = { reach: 0, squeeze: 0, crush: 0, fade: 0 };
  let threw = null, frames = 0;
  try {
    for (const foe of ["emberedge", "axiom"]){
      const m = new AC.Match(rid, foe, seed);
      const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < 120 / DT){
        m.step(DT); step++;
        if (!(me.graspFade > 0.01)) continue;
        /* THE THREE STATES, READ THE WAY `drawGrip` READS THEM. The crush is
           `graspCrush` and NOT `ultGrasp.crush`: the window is nulled on the
           frame the fifth grab lands -- that is "then dissipates" -- so the
           two seconds of the payoff live entirely on the presentation clock.
           The first cut of this classifier looked at `ultGrasp` and reported
           ZERO crush frames on a build that had none, which is how the
           missing picture was found. */
        const G = me.ultGrasp, C = me.graspCrush;
        if (C) seen.crush++;
        else if (!G) seen.fade++;
        /* THE SQUEEZE, NOT A HOLD. Rick's correction: the hand reaches out,
           squeezes, and LETS GO — `G.grip` is the fist and it is a quarter of
           the stun the grab wrote. A build that drew the stun instead held the
           hand on the quarry for 83% of the cadence and stretched with the
           ball, which says the BALL is held and it is not. */
        else if (G.grip > 0) seen.squeeze++;
        else seen.reach++;
        R.ctx = ctx;
        R.drawGrip(m, false);
        R.drawGrip(m, true);
        R.ctx = saved;
        frames++;
      }
    }
  } catch (e){ threw = String(e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-grasp.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    seeds = [4177 + 31 * i for i in range(a.seeds)]

    print(f"\nGRASP — asserted against {gp.name}\n")
    with game(game_path=gp) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        U = M["u"]
        print(f"  relic  {RID}  {M['aff']} x {M['shape']}  dmg {M['dmg']:g}  "
              f"onHit {M['onHit']}   roster {M['relics']}")
        print(f"  ult    {U['name']}  charge {U['charge']:g}  kind {U['kind']}  "
              f"dur {U['dur']:g}  radius {U['radius']:g}")
        print(f"         cadence {U['cadence']:g}  grabStun {U['grabStun']:g}  "
              f"n {U['n']}  trueStun {U['trueStun']:g}")
        print(f"  tip    {len(U['tip'])}/72  {U['tip']}\n")

        S = M["src"]
        check("[0] the cast resolves nothing — dmg 0, kind grip, no apply",
              S["castIsEmpty"] and S["kindIsGrip"] and S["noApply"])
        check("[3a] `tickGrasp` never mentions takeHitstun  (§4.1)",
              S["noHitstun"])
        check("[9a] the pin is the SQUEEZE's length and never the stun's  (§4.5)",
              S["pinIsSqueeze"])
        check("[5a] `tickGrasp` never hurts and never touches the pool  (§8)",
              S["noDamage"])
        check("[2a] exactly one true-stun application site in the window  (§4.2)",
              S["oneTrueSite"])
        check("[8a] the window is per-FIGHTER and never in `shots`",
              S["perFighter"])
        check("[Pa] the art is read off the fighter, not off `m.ultFx`  (v54 §2a)",
              S["artOnFighter"])

        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != RID]
        print(f"\n  running {len(foes)} foes x {a.seeds} seeds "
              f"= {len(foes) * a.seeds} fights\n")
        A = page.evaluate(RUN_JS, [RID, foes, seeds, a.secs])

        # ---------------------------------------------------------- [1] ----
        check("[1] the window closes on the clock, the counter or the corpse "
              "— never otherwise",
              A["badClose"] == 0 and A["doubleOpen"] == 0,
              f"{A['casts']} casts, {A['closes']} closes, "
              f"{A['badClose']} unexplained, {A['doubleOpen']} double-opens, "
              f"longest {A['longestWindow']:.2f}s against dur {U['dur']:g}")

        # ---------------------------------------------------------- [2] ----
        # COUNTED OFF THE ENGINE'S OWN EVENTS. `breakTrue` is the number of
        # times the crush called `breakSpin` WITH a duration, which is the
        # engine's own definition of a true stun; `crushAtN` is how many of
        # those landed on exactly the nth grab.
        check(f"[2] exactly n={U['n']} grabs to a true stun",
              A["breakTrue"] == A["crushes"] and A["crushAtN"] == A["crushes"]
              and A["crushes"] > 0 and A["multiGrab"] == 0,
              f"{A['grabs']} grabs, {A['crushes']} crushes, "
              f"{A['breakTrue']} true-stun calls, "
              f"{A['grabs'] / max(1, A['casts']):.2f} grabs a cast, "
              f"{A['multiGrab']} frames with more than one grab")

        # ---------------------------------------------------------- [3] ----
        check("[3] a grab does not touch `stunDR` and never calls takeHitstun",
              A["stunDrMoved"] == 0 and A["hitstunCalls"] == 0,
              f"{A['stunDrMoved']} stunDR moves and {A['hitstunCalls']} "
              f"takeHitstun calls across {A['tickFrames']} ticks")

        # ---------------------------------------------------------- [4] ----
        # WHAT THE ENGINE ACTUALLY DOES. Every `breakSpin` from this window
        # carries a duration (so it is a TRUE stun), and the ordinary grabs
        # never reach the hook at all -- `breakInTick == breakTrue == crushes`.
        wind = A["windForge"] + A["windSpin"] + A["windBeam"]
        check("[4] only the crush is a true stun, and it lands as one",
              A["breakInTick"] == A["crushes"] and A["breakTrue"] == A["crushes"]
              and A["windHeldOk"] == wind,
              f"{A['breakInTick']} calls for {A['crushes']} crushes; "
              f"caught {A['windForge']} forges / {A['windSpin']} storms / "
              f"{A['windBeam']} winding beams, all {A['windHeldOk']} taken"
              + ("" if wind else "  — NO WIND-UP WAS CAUGHT, so the second "
                                 "half is UNEXERCISED"))

        # ---------------------------------------------------------- [5] ----
        check("[5] no grab deals damage and none applies curse",
              A["hurtInTick"] == 0 and A["hpMoved"] == 0 and A["poolMoved"] == 0,
              f"{A['hurtInTick']} hurts, {A['hpMoved']} hp moves, "
              f"{A['poolMoved']} pool moves across {A['tickFrames']} ticks")

        # ---------------------------------------------------------- [7] ----
        check("[7] no grab resolves on a corpse or after the match",
              A["deadGrab"] == 0 and A["overGrab"] == 0 and A["outOfReach"] == 0,
              f"{A['deadGrab']} on a corpse, {A['overGrab']} after the end, "
              f"{A['outOfReach']} outside radius {U['radius']:g}")

        # ---------------------------------------------------------- [9] ----
        # [9] IS A BAND NOW, NOT A ZERO. The squeeze stops the ball and the
        # stun does not, so `pin` moves on exactly the frames a grab lands --
        # once per grab and never on a frame without one.
        check("[9] the ball is pinned once per grab and on no other frame",
              A["pinMoved"] == A["grabs"] + A["crushes"],
              f"{A['pinMoved']} pin moves against {A['grabs'] + A['crushes']} "
              f"grabs across {A['tickFrames']} ticks")

        # --------------------------------------------------------- [10] ----
        # THE CAST'S BEAT IS `fireUlt`'S OWN, which every relic in the game
        # gets; the crush files a SECOND one from inside the window. A grab
        # that filed a beat would hand the director a fight made of four
        # identical moments a cast -- `_cineVine`'s rule exactly.
        check("[10] the cast files a beat, the crush files its own, "
              "the ordinary grabs file none",
              A["castBeats"] == A["casts"] and A["beatsInTick"] == A["crushes"]
              and A["fatalInTick"] == 0,
              f"{A['castBeats']} cast beats for {A['casts']} casts, "
              f"{A['beatsInTick']} in-window beats for {A['crushes']} crushes, "
              f"{A['fatalInTick']} fatal (a zero-damage ultimate has none, ever)")

        # --------------------------------------------------------- [11] ----
        held = A["held"] / max(1, A["fights"])
        perCast = A["held"] / max(1, A["casts"])
        castRate = A["casts"] / max(1, A["fights"])
        # THE LAB'S OWN ROW, at n=5: 6.8s a fight over 1.84 casts = 3.70 s/cast.
        # THE MECHANIC IS THE PER-CAST NUMBER. `held` a fight is that times the
        # cast rate, and the cast rate is not this ultimate's -- see below.
        LAB_PER_CAST, LAB_HELD, LAB_CASTS = 3.70, 6.8, 1.84
        check("[11] held seconds A CAST matches the lab — the mechanic itself",
              abs(perCast - LAB_PER_CAST) < 0.30,
              f"{perCast:.2f}s a cast against grab_lab's {LAB_PER_CAST:.2f} "
              f"at n={U['n']}")
        band = 6.5 <= held <= 7.0
        print(f"  {'PASS' if band else 'NOTE'}  [11] held seconds A FIGHT — "
              f"THE SCALAR THE WHOLE DESIGN IS PRICED ON")
        print(f"        {held:.2f}s a fight over {A['fights']} fights against "
              f"the brief's registered 6.5-7.0")
        print(f"        lift = +3.1 + 2.62 x held  =>  "
              f"{3.1 + 2.62 * held:+.1f}% predicted over this relic's own floor")
        if not band:
            # AND THE REASON IS THE CAST RATE, NOT THE HOLD. `grab_lab` drives
            # its own window off match time and holds its charge clock WHILE
            # THE WINDOW RUNS; `tickCharge` does not, for 25 of 28 relics --
            # only the Crucible, Ironbloom and the bow window gate the rebuild
            # (v55b §1). So the built relic gets eight seconds of free charge a
            # cast that the lab never gave it, and every arm in the doc is
            # measured on a cast rate this build does not have.
            print(f"        AND IT IS THE CAST RATE, NOT THE HOLD: "
                  f"{castRate:.2f} casts a fight against the lab's "
                  f"{LAB_CASTS:.2f}, at {perCast:.2f}s a cast against "
                  f"{LAB_PER_CAST:.2f}.")
            print(f"        `grab_lab` holds its charge clock while its own "
                  f"window runs; `tickCharge` does not,")
            print(f"        for 25 of 28 relics (v55b §1). Eight seconds of "
                  f"free charge a cast the lab never gave it.")
        PASS.append(("[11] held a fight inside the brief's 6.5-7.0", band))

        # ---------------------------------------------------------- [6] ----
        SH = page.evaluate(SHADE_JS, [RID, seeds[:4], a.secs])
        check("[6] FOE ONLY — no shade is ever touched by the window",
              SH["moved"] == 0,
              f"{SH['moved']} shade states moved across {SH['frames']} ticks "
              f"with shades on the floor; {SH['grabsWithShades']} grabs landed "
              f"while shades were up"
              + ("" if SH["frames"] else "  — UNEXERCISED, no shade was ever up"))

        # ---------------------------------------------------------- [8] ----
        pairs = [["dawnbringer", "axiom"], ["ironhail", "bulwarden"],
                 ["paradox", "thornwake"], ["vesper", "redflail"],
                 ["twinshade", "emberedge"], ["gravemourn", "nightfell"]]
        LK = page.evaluate(LEAK_JS, [RID, pairs, 90210])
        check("[8] the hand is per-fighter — six other-relic matches are "
              "identical after a cast",
              LK["bad"] == 0 and LK["casts"] > 0,
              f"{LK['bad']} of {LK['n']} moved after {LK['casts']} casts")

        # ---------------------------------------------------------- [P] ----
        D = page.evaluate(DRAW_JS, [RID, 55196])
        s = D["seen"]
        check("[P] the render path is CALLED against a real 2D context, "
              "in every state",
              D["threw"] is None and D["frames"] > 0
              and s["reach"] > 0 and s["squeeze"] > 0 and s["crush"] > 0
              and s["fade"] > 0,
              f"{D['frames']} frames — reaching {s['reach']}, squeezing "
              f"{s['squeeze']}, crush {s['crush']}, fading {s['fade']}"
              + (f"   THREW {D['threw']}" if D["threw"] else ""))

        # --------------------------------------------------------- [12] ----
        # v42 SHIPPED A SILENT ULTIMATE THROUGH EVERY GREEN CHECK IN THIS REPO.
        # `SFX.play` returns on its first line headless and wraps its body in
        # try/catch, so a broken voice is invisible to every other tool here.
        print()
        voices = [("shroudmaul", "the hand growing", 2.4),
                  ("shroudmaul-grab", "a grab closing", 1.2),
                  ("shroudmaul-crush", "the crush", 2.4)]
        vok = True
        for w, what, secs in voices:
            r = page.evaluate(SFX_JS, ["ult", {"w": w}, secs])
            if r.get("skip"):
                print("  SKIP  [12] no OfflineAudioContext in this runtime")
                vok = False
                break
            ok = (r["threw"] is None and r["peak"] > 0.02
                  and r["audible"] > 0.05 and r["hp300"] > 0.05)
            vok = vok and ok
            print(f"  {'PASS' if ok else 'FAIL'}  [12] {w:<18} {what:<20} "
                  f"peak {r['peak']:.4f}  audible {r['audible']:.2f}s  "
                  f"<120Hz {r['low120']:.3f}  >300Hz {r['hp300']:.3f}"
                  + (f"   THREW {r['threw']}" if r["threw"] else ""))
        else:
            # AND THE TWO THAT MUST NOT BE CONFUSED. The crush has to be
            # bigger than a grab or a viewer cannot tell the payoff from the
            # rhythm -- Vesper's pass-against-tip pair is the precedent and it
            # is the same problem one relic along.
            g = page.evaluate(SFX_JS, ["ult", {"w": "shroudmaul-grab"}, 1.2])
            c = page.evaluate(SFX_JS, ["ult", {"w": "shroudmaul-crush"}, 2.4])
            # NOT `audible`. The first cut asked for 1.6x on it and got 1.27x
            # from two voices that are plainly different — because `audible`
            # measures the SIGNAL CHAIN'S tail, which both sounds fill, and it
            # saturates. What separates a clamp from a collapse is LEVEL and
            # WEIGHT: the crush is a body blow and the grab is a click.
            sep = (c["peak"] > g["peak"] * 1.6
                   and c["low120"] > g["low120"] + 0.08)
            vok = vok and sep
            print(f"  {'PASS' if sep else 'FAIL'}  [12] the crush is not a grab "
                  f"— peak {g['peak']:.4f} -> {c['peak']:.4f} "
                  f"({c['peak'] / max(1e-9, g['peak']):.2f}x), "
                  f"<120Hz {g['low120']:.3f} -> {c['low120']:.3f}")
        PASS.append(("[12] the three voices render and separate", vok))

        assert not errors, errors[:4]

    bad = [n for n, ok in PASS if not ok]
    print(f"\n  {len(PASS) - len(bad)}/{len(PASS)} checks pass")
    if bad:
        print("  FAILED: " + "; ".join(bad))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"pass": PASS, "run": A, "shade": SH, "leak": LK, "draw": D},
            indent=1))
        print(f"  wrote {a.json}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
