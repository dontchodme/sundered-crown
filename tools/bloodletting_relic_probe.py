#!/usr/bin/env python3
"""BLOODLETTING, ASSERTED AGAINST THE BUILD — one check per sentence. Brief §4.

    python bloodletting_relic_probe.py --game ../02-chain/sc-bloodletting.html

  [1]  THE SPECTRE IS THROWN ON THE CAST AND ON NOTHING ELSE, never two at
       once from one cast, and its BEARING IS FIXED AT SPAWN — no homing
  [2]  IT STOPS WHERE IT STOPS, it never leaves the hall, and it is gone
       after `life`
  [3]  THE DISC IS `ballR + reach` AND A TICK LANDS IFF THE QUARRY'S CENTRE IS
       INSIDE IT — constructed both ways
  [4]  A TICK DEALS `dmg` SCALED BY `dmgTakenMul`, APPLIES `bleed`, AND KNOCKS
       `knock` ALONG ITS OWN BEARING — read off the engine, not recomputed
  [5]  THE CEILING IS SCOPED. A Marrowdraw match run in the same page session
       never sees a cap above 4, and the cap comes back down when a window
       merely EXPIRES rather than when the match ends
  [6]  THE BLADE FEEDS THE RAISED CEILING TOO — Rick's ruling
  [7]  THE CASTER IS NEVER TICKED, by its own copy or anybody's
  [8]  NO TICK ON A CORPSE, NONE AFTER `m.over`, NONE WHILE `m.hitStop > 0`
  [9]  PER-FIGHTER STATE — six other-relic matches run AFTER a Bloodmirror one
       are bit-identical to the same six run before it
  [10] IT IS NOT BUILT ON `shots`, so `bladeSegments` cannot parry it
  [11] THE BEAT. The cast files one, the LANDING files its own, the ticks file
       none — and a tick that KILLS files a FATAL one
  [12] TICKS A FIGHT IS 10.5-11.0. The scalar the whole design is priced on
  [13] EVERY VOICE RENDERS TO SOMETHING AUDIBLE in an OfflineAudioContext
  [P]  THE RENDER PATH IS CALLED against a real 2D context

## [P] IS NOT OPTIONAL AND v48 IS WHY

Two picture faults shipped through every headless check in this repo and died
on the first rendered frame: `_drawBeam` reached for a MATCH method from the
RENDERER, and `drawUltUnder` handed NaN to `createRadialGradient`. Both were
green across 27 probe checks, a 280-match `engine_ab`, `chain_audit` and
`post_identity` — and the probe's own check passed on the first one because it
was REGEXING the source for a call, and a string does not resolve a reference.
So this one CALLS `drawSpectre` against a live context, with a copy in the air,
a copy standing, and a copy dissolving.

## THE CHECKS RECONSTRUCT THE ENGINE'S RULE RATHER THAN ASSUMING THEIR OWN

`gravemourn_relic_probe` reported three defects that were not there, every one
because the probe had written down its own model of a rule and the engine
legitimately did something else. So `flight`, `speed`, `life`, `disc`, `tick`,
`dmg`, `bleed`, `cap` and `knock` are read off `w.ult` and never typed in.

**And [2] is the one that would have gone wrong.** "It stops where it stops"
is the design's sentence and the BUILD does not obey it literally: the hall
closes (`CONFIG.collapse` walks the inset 0 → 140 from t = 21s) and the wall
SHOVES a standing copy rather than killing it — brief §6.5, decided in
`tickSpectre` and written down there. So this check asserts that any movement
after landing is exactly a clamp against the CURRENT inset, which is a
different and stronger claim than "the position never changes".

## AND A CHECK THAT COUNTS FRAMES IS NOT COUNTING THE EVENT

Five times in one file in v60, and twice more in v56. [8] counts TRANSITIONS
and [11] counts beats attributed to the call that filed them; neither counts
frames in which something was possible.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "bloodmirror"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}"
          + (f"\n        {detail}" if detail else ""))


# ------------------------------------------------------------- the main run --
# ONE instrumented match per (foe, seed). Every hook forwards with `arguments`
# -- v44's warning, and it is that a wrapper with a FIXED ARITY silently
# measures the OLD build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const R = AC.CONFIG.physics.ballR;
  const HEM = AC.STATUS.hemorrhage;
  const M = AC.Match.prototype;
  const A = {
    fights: 0, casts: 0, spawns: 0, wrongN: 0, replaced: 0,
    bearingDrift: 0, flightBad: 0, speedBad: 0, fanBad: 0,
    landed: 0, movedAfterLand: 0, notDrift: 0, outOfHall: 0,
    lifeBad: 0, expires: 0,
    ticks: 0, tickOutside: 0, insideNoTick: 0, insideChecks: 0,
    dmgBad: 0, bleedBad: 0, knockBad: 0, dealtSum: 0,
    capOverBase: 0, capWhileFlying: 0, capAfterExpire: 0,
    bladePast4: 0, bladeInWindow: 0,
    selfTick: 0, shadeTick: 0,
    corpseTick: 0, overTick: 0, frozenTick: 0, frozenChecks: 0,
    inShots: 0, maxLive: 0, overlapTicks: 0,
    castBeats: 0, landBeats: 0, tickBeats: 0, tickFatalBeats: 0, tickKills: 0,
    ticksPerFight: [], castsPerFight: [], maxStack: 0, stackSum: 0, stackN: 0,
    flyTicks: 0,
  };
  const origHit = M.spectreHit, origBeat = M.beat;
  const origFire = M.fireUlt, origResolve = M.resolveHit;

  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      A.fights++;
      const me = m.a;                       // the relic is always side A here
      let step = 0, inTick = false, inCast = false;
      let fightTicks = 0, watchCap = 0;

      m.fireUlt = function (f, foe) {
        const had = f.ultSpectres.filter(S => !S.dead).length;
        inCast = (f === me);
        try { origFire.call(m, f, foe); } finally { inCast = false; }
        if (f !== me) return;
        A.casts++;
        const list = f.ultSpectres;
        A.spawns += list.length;
        if (list.length !== U.n) A.wrongN++;
        if (had) A.replaced++;
        /* [1] THE BEARINGS ARE RECORDED HERE AND COMPARED EVERY FRAME. A copy
           that steered would still land, still mill and still measure --
           "thrown at where the quarry is NOW" is the whole separation from an
           aimed shot, and nothing else in the fight would show it. */
        const a0 = Math.atan2(foe.y - f.y, foe.x - f.x);
        for (let i = 0; i < list.length; i++){
          const S = list[i];
          S.__x0 = S.x; S.__y0 = S.y;
          /* AND THE FAN IS RECONSTRUCTED FROM THE ENGINE'S OWN RULE rather
             than assumed: the i-th of N sits at `(i/(N-1) - 0.5) * 2 * spread`
             off the bearing to the quarry, and with N = 1 that term is
             identically zero. */
          const want = a0 + (list.length === 1 ? 0
                     : ((i / (list.length - 1)) - 0.5) * 2 * (U.spread || 0));
          let dA = Math.atan2(S.ay, S.ax) - want;
          while (dA >  Math.PI) dA -= 2 * Math.PI;
          while (dA < -Math.PI) dA += 2 * Math.PI;
          if (Math.abs(dA) > 1e-9) A.fanBad++;
        }
      };

      m.spectreHit = function (S, own, foe, d) {
        A.ticks++; fightTicks++;
        /* AND WHERE THE TICK CAME FROM. `hitFly` is a picture choice the design
           measured at +12.7 against +11.2 -- inside the noise -- but a copy
           that bites on the way out collects ticks the lab's centre arm did
           not, and [12] is a COUNT. Decomposed here so a number out of band can
           be attributed rather than argued about. */
        if (!S.landed) A.flyTicks++;
        /* [8] COUNTED HERE, WITH THE STATE AS IT WAS WHEN THE TICK HAPPENED.
           Both of these were frame samples in the first cut and both reported
           defects that were not there: a tick that KILLS leaves the foe dead
           and the match over on the same step, so a check reading `!alive` or
           `m.over` AFTER the step counts every killing tick as a violation. */
        if (!foe.alive) A.corpseTick++;
        if (m.over) A.overTick++;
        /* AND HOW OFTEN A QUARRY IS IN TWO DISCS AT ONCE. Not a defect -- each
           copy is its own hazard with its own cooldown and that is the plain
           reading of "three copies of itself" -- but it is the multiplier
           nobody priced, so it is COUNTED rather than argued about. */
        let inN = 0;
        for (const O of own.ultSpectres)
          if (!O.dead && (O.landed || U.hitFly)
              && Math.hypot(foe.x - O.x, foe.y - O.y) <= O.disc) inN++;
        if (inN > 1) A.overlapTicks++;
        /* [3] a tick that lands from OUTSIDE the disc is the check failing in
           the direction that matters -- a hit box bigger than the picture. */
        const dd = Math.hypot(foe.x - S.x, foe.y - S.y);
        if (dd > U.disc + 1e-6) A.tickOutside++;
        /* [7] the caster is never the target, and neither is a copy */
        if (own === foe) A.selfTick++;
        if (foe !== m.a && foe !== m.b) A.shadeTick++;
        /* [4] MEASURED EITHER SIDE OF THE CALL, off the engine's own state */
        const want = Math.round(U.dmg * foe.dmgTakenMul());
        const b4 = { dealt: own.dealt, hem: foe.stacks("hemorrhage"),
                     vx: foe.vx, vy: foe.vy, alive: foe.alive };
        const capNow = foe.bleedCap;
        inTick = true;
        try { origHit.call(m, S, own, foe, d); } finally { inTick = false; }
        if (own.dealt - b4.dealt !== want) A.dmgBad++;
        A.dealtSum += own.dealt - b4.dealt;
        const wantHem = b4.hem < capNow
                      ? Math.min(capNow, b4.hem + U.bleed) : b4.hem;
        if (foe.stacks("hemorrhage") !== wantHem) A.bleedBad++;
        if (b4.alive && foe.alive && U.knock > 0){
          const k = dd || 1;
          const ax = dd > 0.001 ? (foe.x - S.x) / k : S.ax;
          const ay = dd > 0.001 ? (foe.y - S.y) / k : S.ay;
          const ex = b4.vx + ax * U.knock, ey = b4.vy + ay * U.knock;
          if (Math.hypot(foe.vx - ex, foe.vy - ey) > 1e-6) A.knockBad++;
        }
        if (!foe.alive) A.tickKills++;
        A.maxStack = Math.max(A.maxStack, foe.stacks("hemorrhage"));
        A.stackSum += foe.stacks("hemorrhage"); A.stackN++;
      };

      /* [11] EVERY BEAT IS ATTRIBUTED TO THE CALL THAT FILED IT rather than
         counted and divided afterward. The cast, the landing and a fatal tick
         are three different claims and a total cannot separate them. */
      m.beat = function (o) {
        if (o && o.kind === "ult" && o.w === rid){
          if (inTick) A.tickBeats++;
          else if (inCast) A.castBeats++;
          else A.landBeats++;
        }
        if (o && o.fatal && inTick) A.tickFatalBeats++;
        origBeat.call(m, o);
      };

      /* [6] THE BLADE FEEDS THE RAISED CEILING. Sampled around `resolveHit` so
         it is the WEAPON's own application and not a copy's. */
      m.resolveHit = function (self, foe) {
        const inWin = foe.bleedCap > HEM.maxStacks;
        const b4 = foe.stacks("hemorrhage");
        const r = origResolve.apply(m, arguments);
        if (inWin){
          A.bladeInWindow++;
          if (foe.stacks("hemorrhage") > HEM.maxStacks
              && foe.stacks("hemorrhage") > b4) A.bladePast4++;
        }
        return r;
      };

      while (!m.over && step < secs / DT){
        const list = me.ultSpectres;
        A.maxLive = Math.max(A.maxLive, list.filter(S => !S.dead).length);
        const snap = list.map(S => ({ S: S, x: S.x, y: S.y, ax: S.ax, ay: S.ay,
                                      landed: S.landed, dead: S.dead,
                                      stand: S.stand, ticks: S.ticks,
                                      cd: S.cd, t: S.t }));
        const inset0 = m.inset;
        /* [8] NOTHING TICKS THROUGH A HIT STOP. Sampled where the engine's own
           freeze already is: `step()` returns through `decayImpactOnly` for as
           long as `hitStop` runs and `tickSpectre` sits below that return, so
           this is a check on the STRUCTURE and not on a guard. */
        /* AND WHETHER THIS STEP RAN AT ALL. `step()` returns through
           `decayImpactOnly` for as long as `hitStop` runs and `tickSpectre`
           sits below that return, so on a frozen frame a copy does not drift
           either -- and a check expecting it to would fire on one frame in
           five of a working build. That is what the first cut of [2] did:
           5501 "unexplained" frames, every one of them a hit stop. */
        const froze = m.hitStop > 0;
        const frozen = froze && snap.some(p => !p.dead);
        const t0 = frozen ? snap.map(p => p.stand + "|" + p.cd + "|" + p.ticks)
                              .join(";") : null;
        /* [3] THE OTHER DIRECTION: a quarry standing inside a landed disc with
           that copy's cooldown expired MUST be bitten. A check that only ever
           asks "did anything land from outside" cannot fail on a disc that
           never fires at all. */
        const owed = snap.filter(p => !p.dead && p.landed && p.cd <= 0
                       && m.b.alive && !m.over && m.hitStop <= 0
                       && Math.hypot(m.b.x - p.x, m.b.y - p.y) < U.disc - 1);
        const liveBefore = snap.filter(p => !p.dead && p.landed).length;

        m.step(DT); step++;

        if (frozen && t0 !== null){
          A.frozenChecks++;
          const now = snap.map(p => p.S.stand + "|" + p.S.cd + "|" + p.S.ticks)
                          .join(";");
          if (t0 !== now) A.frozenTick++;
        }
        for (const p of owed){
          A.insideChecks++;
          if (p.S.ticks === p.ticks) A.insideNoTick++;
        }

        for (const p of snap){
          const S = p.S;
          if (Math.abs(S.ax - p.ax) > 1e-12 || Math.abs(S.ay - p.ay) > 1e-12)
            A.bearingDrift++;
          if (p.dead) continue;
          if (!p.landed && S.landed){
            A.landed++;
            /* `S.t` AND NOT `m.t`. The first cut of this check compared the
               match clock either side of the throw and reported every landing
               "off the clock" -- because `step()` returns early for as long as
               `hitStop` runs, so a copy's own clock stops while the match's
               does not. Every impact in this engine opens with a freeze, so a
               probe that measures a duration against `m.t` measures the
               freezes. */
            if (Math.abs(S.t - U.flight) > DT * 1.5) A.flightBad++;
            const travelled = Math.hypot(S.x - S.__x0, S.y - S.__y0);
            /* the clamp can shorten a throw into a wall, so this is an upper
               bound and not an equality */
            if (travelled > (U.flight + DT) * U.speed + 1e-6) A.speedBad++;
          } else if (p.landed && !S.dead){
            /* [2] IT NO LONGER STOPS DEAD, AND THIS IS THE RULE IT OBEYS NOW.
               Rick asked for "a small amount of movement so they slowly
               continue to float in the direction they were fired", so a copy
               moves by exactly `drift * dt` along its OWN FIRED BEARING and
               then by whatever the closing wall added -- and by nothing else.
               A check that still asserted "the position never changes" would
               fire on every frame of a working build; a check that asserted
               nothing would not notice a copy that started chasing. */
            if (S.x !== p.x || S.y !== p.y) A.movedAfterLand++;
            const eff = froze ? 0 : DT;
            const dx = p.x + p.ax * (U.drift || 0) * eff;
            const dy = p.y + p.ay * (U.drift || 0) * eff;
            const cx = Math.min(Math.max(dx, m.inset + R),
                                AC.CONFIG.arena.w - m.inset - R);
            const cy = Math.min(Math.max(dy, m.inset + R),
                                AC.CONFIG.arena.h - m.inset - R);
            if (Math.abs(S.x - cx) > 1e-9 || Math.abs(S.y - cy) > 1e-9)
              A.notDrift++;
          }
          if (!S.dead
              && (S.x < m.inset - 1e-6
                  || S.x > AC.CONFIG.arena.w - m.inset + 1e-6
                  || S.y < m.inset - 1e-6
                  || S.y > AC.CONFIG.arena.h - m.inset + 1e-6)) A.outOfHall++;
          /* [10] IT IS NOT A SHOT. `spawnShot` shifts the oldest live entry out
             at `maxLive` 64 and `tickShots` lets `bladeSegments` PARRY. */
          if (m.shots && m.shots.some(sh => sh === S)) A.inShots++;
          if (!p.dead && S.dead && p.landed){
            A.expires++;
            if (Math.abs(p.stand + DT - U.life) > DT * 1.5) A.lifeBad++;
            watchCap = 2;
          }
        }
        if (list.some(S => !S.dead && !S.landed)
            && me.bleedCap !== HEM.maxStacks) A.capWhileFlying++;

        /* [5d] THE CAP COMES BACK DOWN ON A WINDOW MERELY EXPIRING, and that is
           the failure mode the design says a probe usually misses -- it is NOT
           the same event as the match ending. */
        if (watchCap && !me.ultSpectres.some(S => !S.dead && S.landed)){
          watchCap--;
          if (!m.over && m.b.bleedCap !== HEM.maxStacks) A.capAfterExpire++;
        }
        if (m.b.bleedCap > (U.cap || 8)) A.capOverBase++;
      }
      A.ticksPerFight.push(fightTicks);
      A.castsPerFight.push(me.ultsFired);
      m.fireUlt = origFire; m.spectreHit = origHit;
      m.beat = origBeat; m.resolveHit = origResolve;
    }
  }
  return A;
}"""


# [5b] AND THE SCOPING, ACROSS RELICS AND ACROSS MATCHES IN ONE PAGE SESSION.
# The design names three silent failures and this is the first two: a
# Marrowdraw in the same session inheriting a window it never cast, and the cap
# surviving into the NEXT match. `bleedCap` is per-fighter and recomputed from
# scratch every frame, so neither is reachable -- which is a claim about the
# structure and therefore worth asserting rather than reasoning about.
SCOPE_JS = r"""([rid, secs]) => {
  const DT = AC.CONFIG.physics.dt, HEM = AC.STATUS.hemorrhage;
  const out = { base: HEM.maxStacks, globalMoved: 0,
                otherOverBase: 0, otherFights: 0, otherStackOver4: 0,
                mineOver4: 0, freshCapBad: 0 };
  const run = (a, b, sd, watch) => {
    const m = new AC.Match(a, b, sd);
    if (m.a.bleedCap !== HEM.maxStacks || m.b.bleedCap !== HEM.maxStacks)
      out.freshCapBad++;
    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      if (AC.STATUS.hemorrhage.maxStacks !== out.base) out.globalMoved++;
      if (watch){
        if (m.a.bleedCap > HEM.maxStacks || m.b.bleedCap > HEM.maxStacks)
          out.otherOverBase++;
        if (m.a.stacks("hemorrhage") > HEM.maxStacks
            || m.b.stacks("hemorrhage") > HEM.maxStacks) out.otherStackOver4++;
      } else {
        out.mineOver4 = Math.max(out.mineOver4, m.b.stacks("hemorrhage"));
      }
    }
  };
  /* the four bloodsworn relics that are NOT this one, before and after */
  const others = [["marrowdraw","axiom"], ["redflail","thornwake"],
                  ["oathwound","ironhail"], ["widowmaker","paradox"]];
  for (const [a, b] of others){ run(a, b, 7717, true); out.otherFights++; }
  run(rid, "thornwake", 4242, false);
  run(rid, "ironhail",  9001, false);
  for (const [a, b] of others){ run(a, b, 7717, true); out.otherFights++; }
  return out;
}"""


# [9] PER-FIGHTER STATE. `gravemourn_relic_probe [9d]`'s pattern: six
# other-relic matches run BEFORE a Bloodmirror one and the same six run AFTER
# it, compared field for field. A relic that leaked anything into module state
# -- a raised global cap being the obvious one -- shows up here and nowhere
# else.
LEAK_JS = r"""([rid, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const pairs = [["ironhail","axiom"], ["paradox","thornwake"],
                 ["twinshade","vesper"], ["lastlight","foregone"],
                 ["marrowdraw","oathwound"], ["shroudmaul","ravelbone"]];
  const run = (a, b, sd) => {
    const m = new AC.Match(a, b, sd);
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    return [m.t, m.a.hp, m.b.hp, m.a.hits, m.b.hits, m.a.dealt, m.b.dealt,
            m.a.ultsFired, m.b.ultsFired].map(v => +(+v).toFixed(6)).join("|");
  };
  const before = pairs.map(([a, b]) => run(a, b, 31337));
  const m = new AC.Match(rid, "thornwake", 4242);
  let step = 0;
  while (!m.over && step < secs / DT){ m.step(DT); step++; }
  const after = pairs.map(([a, b]) => run(a, b, 31337));
  let bad = 0;
  for (let i = 0; i < before.length; i++) if (before[i] !== after[i]) bad++;
  return { n: before.length, bad, cast: m.a.ultsFired };
}"""


# [P] THE RENDER PATH, CALLED. Not regexed -- v48's own lesson, twice over.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { flying: 0, standing: 0, fading: 0, under: 0, over: 0,
                threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const S = (m.a.ultSpectres[0] || m.b.ultSpectres[0]);
        const nLive = m.a.ultSpectres.length + m.b.ultSpectres.length;
        if (!nLive) continue;
        const all = m.a.ultSpectres.concat(m.b.ultSpectres);
        if (all.some(S => !S.dead && !S.landed)) out.flying++;
        if (all.some(S => !S.dead && S.landed)) out.standing++;
        if (all.some(S => S.dead)) out.fading++;
        try { R.ctx.save(); R.drawSpectre(m); R.ctx.restore(); }
        catch (e){ out.threw = "drawSpectre: " + String(e); return out; }
        if (!m.ultFx) continue;
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
      }
      if (out.flying > 200 && out.standing > 900 && out.fading > 100)
        return out;
    }
  }
  return out;
}"""


# AND THE ONE THING A RENDER CANNOT SEE. `_burst` does not loop its 0.6s noise
# buffer, so a burst asked for a longer tail plays silence into it -- and the
# rendered waveform looks exactly like a sound that ended.
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
# v59 did exactly that for the jet and reported peak 0.000 -- which is
# indistinguishable from the silent ultimate v42 shipped, and is why this check
# earns its place even on the occasions when it is the probe that is wrong.
CASES = [
    ("the throw",     "ult", {"w": "bloodmirror"},        2.4),
    ("it sticks",     "ult", {"w": "bloodmirror-stick"},  2.0),
    ("the mill",      "ult", {"w": "bloodmirror-mill"},   2.2),
    ("a tick lands",  "ult", {"w": "bloodmirror-tick"},   1.7),
    ("and it closes", "ult", {"w": "bloodmirror-close"},  2.2),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bloodletting.html")
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--foes", default="thornwake,ironhail,twinshade,paradox,"
                                      "axiom,lastlight,grudgebearer,vesper")
    ap.add_argument("--seeds", default="4242,9001,15503,20260901,7717,33581")
    A = ap.parse_args()

    g = resolve_game(A.game)
    foes = A.foes.split(",")
    seeds = [int(x) for x in A.seeds.split(",")]

    print(f"\nBLOODLETTING — §4, asserted against {pathlib.Path(g).name}")
    print(f"  {len(foes)} foes x {len(seeds)} seeds\n")

    with game(game_path=g) as (page, errors):
        U = page.evaluate(
            "(rid) => AC.WEAPONS.find(w => w.id === rid).ult", RID)
        base = page.evaluate("() => AC.STATUS.hemorrhage.maxStacks")
        R = page.evaluate("() => AC.CONFIG.physics.ballR")
        reach = page.evaluate(
            "(rid) => AC.WEAPONS.find(w => w.id === rid).reach", RID)
        print(f"  the ult, as shipped: flight {U['flight']}s at {U['speed']}, "
              f"life {U['life']}s, disc {U['disc']}")
        print(f"                       tick {U['tick']}s for {U['dmg']} and "
              f"{U['bleed']} Hemorrhage, knock {U['knock']}")
        print(f"                       ceiling {base} -> {U['cap']} while it "
              f"stands\n")

        a = page.evaluate(RUN_JS, [RID, foes, seeds, A.secs])
        if errors:
            print(f"  page errors: {errors[:3]}")

        n = a["fights"]
        check(f"[1] {U['n']:g} copies a cast, in a fan, and only on a cast",
              a["spawns"] == a["casts"] * U["n"] and a["wrongN"] == 0
              and a["fanBad"] == 0,
              f"{a['casts']} casts, {a['spawns']} copies "
              f"({a['spawns'] / max(1, a['casts']):.2f} a cast), "
              f"{a['wrongN']} casts spawned the wrong number, "
              f"{a['fanBad']} off the fan; peak live {a['maxLive']}. "
              f"{a['replaced']} casts landed on top of a live set")
        check("[1b] the bearing is fixed at spawn — NO HOMING",
              a["bearingDrift"] == 0,
              f"{a['bearingDrift']} frames on which ax/ay moved after the throw")
        check("[1c] flight is `flight` seconds and no further than "
              "`flight x speed`",
              a["flightBad"] == 0 and a["speedBad"] == 0,
              f"{a['landed']} landings, {a['flightBad']} off the clock, "
              f"{a['speedBad']} past the reach of the throw")

        check(f"[2] after landing it moves by `drift` {U['drift']:g} px/s along "
              f"its OWN bearing and by nothing else",
              a["notDrift"] == 0,
              f"{a['movedAfterLand']} frames of movement after landing, "
              f"{a['notDrift']} of them not the drift plus the closing wall. "
              f"RICK CHANGED HIS OWN §1 HERE — it said \"sticks in place\", "
              f"and this check moved with the build rather than the build "
              f"being held to a sentence nobody is standing behind any more.")
        check("[2b] it never leaves the hall", a["outOfHall"] == 0,
              f"{a['outOfHall']} frames outside the inset")
        check("[2c] and each is gone after `life`",
              a["lifeBad"] == 0 and a["expires"] > 0,
              f"{a['expires']} copies expired on the clock, "
              f"{a['lifeBad']} at the wrong length")

        check("[3] a tick lands IFF the quarry's centre is inside the disc",
              a["tickOutside"] == 0 and a["insideNoTick"] == 0,
              f"{a['ticks']} ticks, {a['tickOutside']} from outside {U['disc']}; "
              f"{a['insideChecks']} frames owed a tick, "
              f"{a['insideNoTick']} of them missed"
              + ("   <-- WEAKLY EXERCISED: a copy that is due and in range "
                 "fires in the same step, so this arm only ever sees the "
                 "frames where one did not. It DID fire once, on the "
                 "same-frame hit-stop ordering bug, and it is worth keeping "
                 "for that reason alone." if a["insideChecks"] < 5 else ""))
        check("[3b] and the disc is the copy's own sweep",
              abs((R + reach) - U["disc"]) < 1e-6,
              f"ballR {R} + reach {reach} = {R + reach}, disc {U['disc']}")

        check("[4] every tick deals, bleeds and shoves exactly what the "
              "block says",
              a["dmgBad"] == 0 and a["bleedBad"] == 0 and a["knockBad"] == 0,
              f"{a['dmgBad']} wrong damage, {a['bleedBad']} wrong bleed, "
              f"{a['knockBad']} wrong shove, over {a['ticks']} ticks "
              f"({a['dealtSum']} damage total)")

        sc = page.evaluate(SCOPE_JS, [RID, A.secs])
        check("[5] the global `maxStacks` never moves",
              sc["globalMoved"] == 0,
              f"{sc['globalMoved']} frames with STATUS.hemorrhage.maxStacks "
              f"off {sc['base']}")
        check("[5b] no other bloodsworn relic ever sees a raised ceiling",
              sc["otherOverBase"] == 0 and sc["otherStackOver4"] == 0,
              f"{sc['otherFights']} matches of the other four, "
              f"{sc['otherOverBase']} frames with a cap over {sc['base']}, "
              f"{sc['otherStackOver4']} with a stack over it — "
              f"run BEFORE and AFTER two Bloodmirror matches")
        check("[5c] a fresh match starts at the status's own ceiling",
              sc["freshCapBad"] == 0,
              f"{sc['freshCapBad']} fighters born with a cap that was not "
              f"{sc['base']}")
        check("[5d] and it comes back down when a window merely EXPIRES",
              a["capAfterExpire"] == 0 and a["capWhileFlying"] == 0,
              f"{a['expires']} expiries, {a['capAfterExpire']} left the cap up "
              f"with the match still running; {a['capWhileFlying']} frames "
              f"raised while every copy was still in the air")
        check("[5e] and nothing ever exceeds the ultimate's own cap",
              a["capOverBase"] == 0, f"{a['capOverBase']} frames over "
              f"{U['cap']}")

        check("[6] the BLADE feeds the raised ceiling too — Rick's ruling",
              a["bladePast4"] > 0,
              f"{a['bladeInWindow']} blade blows landed inside a window, "
              f"{a['bladePast4']} of them carried the quarry past {base}. "
              f"Peak stack seen: {a['maxStack']}")

        check("[7] the caster is never ticked, and neither is a copy",
              a["selfTick"] == 0 and a["shadeTick"] == 0,
              f"{a['selfTick']} self, {a['shadeTick']} shades — and milling "
              f"both balls measures -16.5pp at z -6.02, BELOW this relic's "
              f"own no-ultimate floor")

        check("[8] no tick on a corpse, after `m.over`, or through a freeze",
              a["corpseTick"] == 0 and a["overTick"] == 0
              and a["frozenTick"] == 0,
              f"{a['corpseTick']} on a corpse, {a['overTick']} after over, "
              f"{a['frozenTick']} of {a['frozenChecks']} frozen frames "
              f"advanced the clock")

        lk = page.evaluate(LEAK_JS, [RID, A.secs])
        check("[9] per-fighter — nothing leaks into the next match",
              lk["bad"] == 0,
              f"{lk['n']} other-relic matches, {lk['bad']} differed after a "
              f"Bloodmirror match that cast {lk['cast']} times")

        check("[10] it is not built on `shots`", a["inShots"] == 0,
              f"{a['inShots']} frames with the spectre in m.shots — "
              f"`spawnShot` shifts the oldest live entry out at maxLive 64, "
              f"and `bladeSegments` can parry a shot")

        check("[11] the cast files a beat, the VOLLEY'S LANDING files ONE, "
              "the ticks file none",
              a["castBeats"] == a["casts"] and a["tickBeats"] == 0
              and a["landBeats"] * U["n"] >= a["landed"] - 2
              and a["landBeats"] <= a["landed"],
              f"{a['castBeats']} cast beats for {a['casts']} casts, "
              f"{a['landBeats']} landing beats for {a['landed']} landings of "
              f"{U['n']:g} copies each — ONE A VOLLEY, not one a copy, because "
              f"three share a `flight` and land on the same frame; "
              f"{a['tickBeats']} from ticks")
        killed = a["tickKills"]
        check("[11b] and a tick that KILLS files a FATAL beat",
              a["tickFatalBeats"] == killed,
              f"{killed} kills by a tick, {a['tickFatalBeats']} fatal beats. "
              + ("WEAKLY EXERCISED — a tick is 3 damage, so it lands the "
                 "finish rarely." if killed < 5 else "")
              + " v53 §4: 30 of 58 Gravemourn kills rendered with no killing "
                "blow because a hand filed `kind:\"ult\"`.")

        tpf = a["ticksPerFight"]
        mean = sum(tpf) / max(1, len(tpf))
        check("[12] TICKS A FIGHT IS 10.5-11.0 — the scalar the design is "
              "priced on",
              10.5 <= mean <= 11.0,
              f"{mean:.2f} over {len(tpf)} fights "
              f"(min {min(tpf) if tpf else 0}, max {max(tpf) if tpf else 0}). "
              f"REGISTERED PREDICTION, brief §9. Mean stack while ticking "
              f"{a['stackSum'] / max(1, a['stackN']):.2f}, peak "
              f"{a['maxStack']}.")
        print(f"        AND THE OVERLAP: {a['overlapTicks']} of {a['ticks']} "
              f"ticks ({100 * a['overlapTicks'] / max(1, a['ticks']):.1f}%) "
              f"landed on a quarry standing in more than one disc. Each copy "
              f"carries its own cooldown, so those frames are paid more than "
              f"once — the plain reading of \"three copies of itself\", and "
              f"the multiplier nobody has priced.")
        cpf = a["castsPerFight"]
        cmean = sum(cpf) / max(1, len(cpf))
        print(f"        AND WHAT IT MEANS: {a['dealtSum'] / max(1, n):.1f} "
              f"spectre damage a fight against the design's ~32 target. The "
              f"one-scalar law is lift = +5.6 + 0.245 x spectre damage, so a "
              f"count {100 * (mean / 10.75 - 1):+.0f}% off the band is about "
              f"{0.245 * (a['dealtSum'] / max(1, n) - 32):+.1f}pp of lift the "
              f"blade has to absorb at 3b.")
        print(f"        DECOMPOSED: {cmean:.2f} casts a fight, "
              f"{mean / max(1e-9, cmean):.2f} ticks a cast; "
              f"{a['flyTicks']} of {a['ticks']} ticks "
              f"({100 * a['flyTicks'] / max(1, a['ticks']):.1f}%) landed while "
              f"the copy was still IN THE AIR (`hitFly`, a picture choice the "
              f"design measured inside the noise)")

        print("\n[13] THE FOUR VOICES, RENDERED")
        print(f"      {'':<16}{'peak':>7}{'audible':>8}")
        sfx = {}
        for name, kind, pp, secs in CASES:
            gg = page.evaluate(SFX_JS, [kind, pp, secs])
            sfx[name] = gg
            print(f"      {name:<16}{gg['peak']:>7}{gg['audible']:>8}s"
                  + (f"   THREW {gg['threw']}" if gg.get("threw") else ""))
        quiet = [k for k, v in sfx.items() if v.get("peak", 0) < 0.002]
        threw = [k for k, v in sfx.items() if v.get("threw")]
        check("[13] every voice renders to something audible",
              not quiet and not threw,
              f"{len(sfx)} voices; silent: {quiet or 'none'}; "
              f"threw: {threw or 'none'}")

        bu = page.evaluate(BURSTS_JS, [[c[2]["w"] for c in CASES]])
        check("[13b] no `_burst` longer than 0.6s (§4.5 — it does not loop)",
              not bu["over"] and not bu["missing"],
              f"{bu['n']} bursts, longest {bu['max']}s"
              + (f", OVER: {bu['over']}" if bu["over"] else "")
              + (f", MISSING: {bu['missing']}" if bu["missing"] else ""))

        print("\n[P] THE RENDER PATH IS CALLED")
        dr = page.evaluate(DRAW_JS, [RID, foes[:4], seeds[:3], A.secs])
        if dr.get("skip"):
            check("[P] the render path is called", False, dr["skip"])
        else:
            check("[P] drawSpectre survives flying, standing AND dissolving",
                  not dr["threw"] and dr["flying"] > 0 and dr["standing"] > 0
                  and dr["fading"] > 0,
                  f"{dr['flying']} frames in the air, {dr['standing']} "
                  f"standing, {dr['fading']} dissolving; "
                  f"drawUltUnder {dr['under']}, drawUltOver {dr['over']}"
                  + (f"; THREW {dr['threw']}" if dr["threw"] else ""))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n{ok}/{len(PASS)} checks passed"
          + ("" if ok == len(PASS) else f"  ({len(PASS) - ok} FAILED)"))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
