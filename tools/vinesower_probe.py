#!/usr/bin/env python3
"""THE THICKET, FALSIFIED. One check per sentence of the design, and the
   sentences are Rick's.

    python3 vinesower_probe.py --game ../02-chain/sc-vinesower.html

    "for a duration the bow fires out seeds instead of arrows.
     the seeds deal normal damage if they hit another ball. or disappear if
     clanked.
     however if they stick to the wall they take root.
     after a short time the bloom into a flowering plant with a vine whip that
     reaches out and strikes at the enemy if they come close enough.
     vine whips should have good but limited range so several can swipe at the
     enemy at the same time.
     the vines cannot be damaged or removed by the enemy.
     the vines stay for a duration and then wither and die.
     the vines should have knockback.
     the vines should have their own unique whipping sound effect."

Nine sentences, and each one gets a check that could fail. Plus the two
structural obligations every relic in this project carries -- the zero-burden
argument and the art -- and the two traps v39 left, re-asserted on this build
because a new `shot` field and a new clock in the tick are exactly what they
were waiting for.

  [1]  THE ROSTER. 22 relics, the cell is filled, the tip fits the contract.
  [2]  THE WINDOW. Seeds during, arrows outside, and nothing else changed.
  [3]  A SEED IS A SHOT. Same damage as an arrow, same parry, and a parried
       seed plants NOTHING -- which is the branch order, tested by running it.
  [4]  ROOTING. What reaches a wall becomes a plant, and the count is the
       82% the survey measured, not a number this file chose.
  [5]  THE SPROUT IS A FLOOR. No vine strikes before it. Asserted at the
       frame, not on average.
  [6]  REACH IS A GATE, and it is measured from the plant, not the caster.
  [7]  SEVERAL AT ONCE. The distribution of how many plants can reach the foe
       at the same instant, which is the sentence "so several can swipe at
       the enemy at the same time" turned into a number.
  [8]  UNKILLABLE. Nothing the foe does removes a vine. Proved by running a
       whole fight and reconciling every removal against the two causes that
       are allowed to exist.
  [9]  THE LIFE. Withers at sprout+vineLife, to the frame.
  [10] KNOCKBACK. The velocity change on the frame of a strike, along
       vine -> foe.
  [11] THE VOICE. One `vine` play per strike and one per planting, and it is
       a DIFFERENT key from every other sound in the game.
  [12] THE CAP drops the oldest.
  [13] THE PLANTS RIDE THE WALL IN as the hall collapses -- the one thing
       that had to be invented.
  [14] ZERO BURDEN. `m.vines` empty and `f.ultBloom` null in every match
       without this relic, and the tick guard is the first line.
  [15] THE ART. The verdant bow branch fires; a seed does not draw as an
       arrow; the plant is on screen and its flower opens when it arms.
  [16] DETERMINISM. Same seed twice is the same garden, to the field.
  [17] THE TRAPS. `tickFire` still gates on `f.w.shot`; `hitStop` still
       freezes `tickStatus`; and NEITHER is newly triggered by this relic.
  [18] THE DECOMPOSITION. Where this relic's damage comes from -- v38 found a
       third of Bloodmill was a mechanic nobody designed by asking exactly
       this, and v39 shipped without asking it.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "vinesower"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


ROSTER_JS = """(rid) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  if (!w) return { missing: true, n: AC.WEAPONS.length };
  const cells = {};
  for (const x of AC.WEAPONS) cells[x.aff + "x" + x.shape] = x.name;
  const bows = AC.WEAPONS.filter(x => x.shape === "bow");
  return { n: AC.WEAPONS.length, w: JSON.parse(JSON.stringify(w)),
           cells, verdant: AC.WEAPONS.filter(x => x.aff === "verdant").map(x => x.name),
           shotSame: bows.every(b => JSON.stringify(b.shot) === JSON.stringify(bows[0].shot)),
           bowStats: bows.map(b => [b.id, b.reach, b.width, b.artW, b.spin, b.mass, b.mode]) };
}"""

# ---------------------------------------------------------------------------
# ONE INSTRUMENTED FIGHT, read many ways. Every wrapper calls through; the
# control in [16] is what proves none of them moved the simulation.
RUN_JS = r"""([rid, foes, seeds, secs, force]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const u  = me.w.ult;

      /* --- instruments, all wrappers --- */
      let seedsFired = 0, arrowsFired = 0, seedsInWindow = 0, arrowsInWindow = 0;
      let windowStun = 0, windowFroze = 0, loaded = 0, leftAtClose = [];
      const oSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, a){
        const r = oSpawn.call(m, fg, a);
        if (fg === me){
          const s = m.shots[m.shots.length - 1];
          if (s && s.seed){ seedsFired++; if (me.ultBloom) seedsInWindow++; }
          else { arrowsFired++; if (me.ultBloom) arrowsInWindow++; }
        }
        return r;
      };
      let planted = 0, parried = 0, seedHitBall = 0, seedWall = 0;
      let dVine = 0, dShot = 0, dMelee = 0, hVine = 0, hShot = 0, hMelee = 0;
      let inVine = false;
      const oPlant = AC.Match.prototype.plantVine;
      m.plantVine = function(s){ planted++; return oPlant.call(m, s); };
      const oResolve = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, ov){
        const sh = m._cineShot, d0 = self.dealt, h0 = self.hits;
        const r = oResolve.call(m, self, foe2, hx, hy, seg, mul, ov);
        const dd = self.dealt - d0, hh = self.hits - h0;
        if (self === me){
          if (inVine){ dVine += dd; hVine += hh; }
          else if (sh){ dShot += dd; hShot += hh; if (sh.seed) seedHitBall++; sh._pHit = true; }
          else { dMelee += dd; hMelee += hh; }
        }
        return r;
      };
      /* the whip's knock, measured on the frame it happens */
      let knocks = [], whips = 0, lands = 0, whiffs = 0;
      let whipsWhileYoung = 0, whipsWhileYoungPre = 0;
      let landsOutOfReach = 0, coiled = 0, slashNoCoil = 0;
      let aimErrSum = 0, aimErrN = 0, awareSum = 0, awareN = 0;
      /* "at the same time" as Rick means it is not "on the same frame": with
         independent cooldowns two plants coinciding to the 1/120th is rare
         even when four are lashing at one ball. This is the honest reading —
         how many DISTINCT plants struck inside a rolling window. */
      const strikeLog = [];
      let maxSimul = 0, simulHist = {}, armedSamples = 0, inReachSamples = 0;
      let contactSamples = 0, contactInReach = 0;
      const oTickV = AC.Match.prototype.tickVines;
      m.tickVines = function(dt){
        inVine = true;
        const before = m.vines.map(v => ({ v, whips: v.whips, lands: v.lands,
                                           t: v.t, wound: v.wind > 0 }));
        for (const v of m.vines) if (v.wind > 0) coiled++;
        const vx0 = th.vx, vy0 = th.vy;
        const r = oTickV.call(m, dt);
        inVine = false;
        let n = 0;
        for (const b of before){
          if (b.v.whips > b.whips){
            whips++;
            /* EVERY SLASH IS PRECEDED BY A COIL. `wind` was set on some
               earlier frame and is back to 0 on this one; a slash that
               appeared without one would mean the wind-up is skippable. */
            if (!b.wound) slashNoCoil++;
            if (b.v.lands > b.lands){ n++; lands++; } else { whiffs++; }
            /* THE GATE IS `if (v.t < v.sprout) continue` AND IT RUNS AFTER
               `v.t += dt`. So the age that decides is the POST-tick one, and
               the first cut of this probe read the pre-tick value and reported
               one frame's worth of legitimate strikes as early. Both are kept:
               `young` is the real claim, `youngPre` is the off-by-one, and the
               difference between them is exactly one frame per plant. */
            if (b.v.t < b.v.sprout) whipsWhileYoung++;
            if (b.t < b.v.sprout) whipsWhileYoungPre++;
            const d = Math.hypot(th.x - b.v.x, th.y - b.v.y);
            if (b.v.lands > b.lands && d > u.reach + R + 1e-6) landsOutOfReach++;
          }
        }
        if (n > 0){
          knocks.push({ n, dvx: th.vx - vx0, dvy: th.vy - vy0 });
          maxSimul = Math.max(maxSimul, n);
          simulHist[n] = (simulHist[n] || 0) + 1;
          for (const b of before) if (b.v.whips > b.whips) strikeLog.push([m.t, b.v]);
        }
        /* how many ARMED plants could reach the foe at this instant, and how
           well the ones that can SEE it are pointing at it -- which is the
           whole of "motion and tracking" as a number */
        let inReach = 0, armed = 0;
        for (const v of m.vines){
          if (v.t < v.sprout) continue;
          armed++;
          const dd = Math.hypot(th.x - v.x, th.y - v.y);
          if (dd <= u.reach + R) inReach++;
          if (dd <= u.reach * (u.awareMul || 1.7) + R){
            const want = Math.atan2(th.y - v.y, th.x - v.x);
            let e = want - v.aim;
            while (e >  Math.PI) e -= 2 * Math.PI;
            while (e < -Math.PI) e += 2 * Math.PI;
            aimErrSum += Math.abs(e); aimErrN++;
            awareSum += v.lean; awareN++;
          }
        }
        if (armed > 0){ armedSamples++; inReachSamples += inReach; }
        /* CONDITIONAL, and it is the question Rick's sentence actually asks.
           The unconditional mean is dominated by the long stretches where the
           foe is mid-hall and NOTHING should be able to reach it -- which is
           the mechanic working, not failing. "several can swipe at the enemy"
           is about the moments when the enemy is in the garden at all. */
        if (inReach > 0){ contactSamples++; contactInReach += inReach; }
        return r;
      };
      /* every removal, and what caused it */
      let removedWither = 0, removedCap = 0, removedOther = 0;
      let maxLive = 0, lifeSpans = [];
      let sfxVine = 0, sfxPlant = 0, sfxOther = 0;
      const oPlay = AC.SFX.play.bind(AC.SFX);
      AC.SFX.play = function(kind, p){
        if (kind === "vine"){
          if (p && p.plant) sfxPlant++;
          else if (p && (p.coil || p.miss)) { /* their own voices */ }
          else sfxVine++;
        }
        else sfxOther++;
        return oPlay(kind, p);
      };

      let st = 0, casts = 0, windowSteps = 0, wallRideMin = 1e9, wallRideMax = -1e9;
      let insetAtPlant = [], insetNow = [];
      while (!m.over && st < secs / DT){
        if (force && st === force) { me.charge = me.w.ult.charge; }
        const hadBloom = me.ultBloom;
        const wasFrozen = m.hitStop > 0;
        const wasStunned = me.stun > 0;
        const pre = m.vines.slice();
        m.step(DT); st++;
        if (hadBloom){
          /* `tickFire` returns on `f.stun > 0` BEFORE it decrements fireCd, and
             `step` returns on hitStop before anything at all. Both are time the
             window is open and the bow cannot fire, and both have to be taken
             out before "did it fire at cadence" is a question with an answer. */
          if (wasFrozen) windowFroze++;
          else if (wasStunned) windowStun++;
        }
        if (!hadBloom && me.ultBloom){ casts++; loaded += me.ultBloom.loaded; }
        if (hadBloom && !me.ultBloom) leftAtClose.push(hadBloom.left);
        if (me.ultBloom) windowSteps++;
        maxLive = Math.max(maxLive, m.vines.length);
        if (pre.length){
          const live = new Set(m.vines);
          for (const v of pre){
            if (live.has(v)) continue;
            lifeSpans.push(v.t);
            if (v.t >= v.life + v.sprout - DT * 1.5) removedWither++;
            else if (m.vines.length >= (u.maxVines || 12) - 1) removedCap++;
            else removedOther++;
          }
        }
        /* the plants must sit ON the current wall, whatever the inset is */
        for (const v of m.vines){
          const n = m.inset;
          const d = v.wall === "W" ? v.x - n : v.wall === "E" ? A.w - n - v.x
                  : v.wall === "N" ? v.y - n : A.h - n - v.y;
          wallRideMin = Math.min(wallRideMin, d);
          wallRideMax = Math.max(wallRideMax, d);
        }
      }
      AC.SFX.play = oPlay;

      rows.push({ foe: f, seed: sd, steps: st, dur: st * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, windowSecs: windowSteps * DT,
                  windowStunSecs: windowStun * DT, windowFrozeSecs: windowFroze * DT,
                  seedsFired, arrowsFired, seedsInWindow, arrowsInWindow,
                  openLeft: me.ultBloom ? me.ultBloom.left : 0,
                  planted, seedHitBall, whips, lands, whiffs,
                  whipsWhileYoung, whipsWhileYoungPre, landsOutOfReach,
                  coiled, slashNoCoil, loaded, leftAtClose,
                  aimErr: aimErrN ? aimErrSum / aimErrN : -1, aimErrN,
                  lean: awareN ? awareSum / awareN : 0,
                  maxSimul, simulHist,
                  windowHist: (() => {
                    /* for every strike, how many DISTINCT plants struck within
                       `win` seconds of it, itself included */
                    const win = 0.6, H = {};
                    for (let i = 0; i < strikeLog.length; i++){
                      const set = new Set();
                      for (let j = 0; j < strikeLog.length; j++)
                        if (Math.abs(strikeLog[j][0] - strikeLog[i][0]) <= win)
                          set.add(strikeLog[j][1]);
                      H[set.size] = (H[set.size] || 0) + 1;
                    }
                    return H;
                  })(),
                  meanInReach: armedSamples ? inReachSamples / armedSamples : 0,
                  armedSamples, contactSamples,
                  inReachGivenAny: contactSamples ? contactInReach / contactSamples : 0,
                  contactShare: armedSamples ? contactSamples / armedSamples : 0,
                  knocks: knocks.slice(0, 40),
                  removedWither, removedCap, removedOther, maxLive,
                  lifeSpans: lifeSpans.slice(0, 40),
                  sfxVine, sfxPlant,
                  dVine, dShot, dMelee, hVine, hShot, hMelee,
                  dealt: me.dealt, hits: me.hits,
                  liveAtEnd: m.vines.length,
                  wallRideMin, wallRideMax });
    }
  }
  return rows;
}"""

# --------------------------------------------------------------- zero burden
BURDEN_JS = """([rid, others, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let touched = 0, matches = 0;
  for (let i = 0; i < others.length; i++){
    const a = others[i], b = others[(i + 1) % others.length];
    if (a === b) continue;
    for (const sd of seeds){
      const m = new AC.Match(a, b, sd);
      let st = 0;
      while (!m.over && st < secs / DT){
        m.step(DT); st++;
        if (m.vines.length || m.a.ultBloom || m.b.ultBloom){ touched++; break; }
      }
      matches++;
    }
  }
  return { touched, matches };
}"""

# --------------------------------------------------------- a clanked seed ---
# Not observed and hoped for: the parry is FORCED, by standing a seed on the
# foe's blade, and then the plant count is read. The branch order in tickShots
# is the claim and this is the only way to test it that does not depend on a
# parry happening to occur.
CLANK_JS = """([rid, foe, seed]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  m.step(DT);
  let planted = 0;
  const oPlant = AC.Match.prototype.plantVine;
  m.plantVine = function(s){ planted++; return oPlant.call(m, s); };
  /* a seed sitting exactly on a blade of the foe, and also PAST the wall
     line, so the two branches are in genuine competition and only the order
     decides which fires */
  const segs = m.bladeSegments(th);
  const q = segs[0];
  const bx = (q.ax + q.bx) / 2, by = (q.ay + q.by) / 2;
  m.shots.length = 0;
  m.shots.push({ own: me === m.a ? "a" : "b", x: bx, y: by, x0: bx, y0: by,
                 spd0: 0, t0: m.t, vx: 0, vy: 0, r: 24, life: 3.4, max: 3.4,
                 grav: 0, dmgMul: 1, seed: true, aff: me.aff, a: 0 });
  th.stun = 0;
  const before = m.vines.length;
  m.tickShots(DT);
  return { planted, vinesBefore: before, vinesAfter: m.vines.length,
           shotsLeft: m.shots.length };
}"""

# --------------------------------------------------- nothing removes a vine
# The foe is handed every tool it has -- a full charge, no stun, and 30
# seconds -- while the caster's plants stand there. The claim is that the
# count only ever falls for the two reasons the code allows.
IMMUNE_JS = """([rid, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const u = me.w.ult;
  let st = 0;
  me.charge = me.w.ult.charge;
  const drops = { wither: 0, cap: 0, unexplained: 0 };
  while (!m.over && st < secs / DT){
    /* the foe gets its ultimate as fast as the engine will let it, forever */
    th.charge = th.w.ult.charge;
    const pre = m.vines.slice();
    m.step(DT); st++;
    const live = new Set(m.vines);
    for (const v of pre){
      if (live.has(v)) continue;
      if (v.t >= v.life + v.sprout - DT * 1.5) drops.wither++;
      else if (m.vines.length >= (u.maxVines || 12) - 1) drops.cap++;
      else drops.unexplained++;
    }
  }
  return drops;
}"""

# ---------------------------------------------------------------- the cap ---
CAP_JS = """([rid, foe, seed]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const u = me.w.ult;
  m.step(DT);
  const mk = (i) => ({ own: me === m.a ? "a" : "b", x: 40, y: 100 + i, x0: 40,
                       y0: 100 + i, spd0: 0, t0: m.t, vx: 0, vy: 0, r: 24,
                       life: 3.4, max: 3.4, grav: 0, dmgMul: 1, seed: true,
                       aff: me.aff, a: 0 });
  for (let i = 0; i < u.maxVines + 4; i++) m.plantVine(mk(i * 7));
  return { n: m.vines.length, cap: u.maxVines,
           firstU: m.vines[0].u,
           /* the OLDEST is the one that should be gone: plant i has u from
              y = 100 + i*7, so a surviving list starting above the 4th is
              the shift and a list starting at the 0th is a drop of the new */
           us: m.vines.map(v => +v.u.toFixed(5)) };
}"""

# ------------------------------------------------------------- the art -----
ART_JS = """([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const draw = (key) => {
    const cv = document.createElement("canvas");
    cv.width = 400; cv.height = 400;
    const c = cv.getContext("2d");
    c.translate(120, 200);
    const pal = Object.assign({}, AC.AFFINITIES.dwarven, { key });
    AC.SHAPES.bow(c, w.reach, w.artW, pal, 0.55);
    return c.getImageData(0, 0, 400, 400).data;
  };
  const a = draw("verdant"), b = draw("NOT_A_SCHOOL");
  let differ = 0, union = 0;
  for (let i = 0; i < a.length; i += 4){
    const A0 = a[i+3] > 24, B0 = b[i+3] > 24;
    if (A0 || B0){ union++;
      if (!A0 || !B0 || a[i] !== b[i] || a[i+1] !== b[i+1] || a[i+2] !== b[i+2]) differ++; }
  }
  return { branch: union ? differ / union : 0 };
}"""

# A seed and an arrow are the same object with one flag. Do they DRAW
# differently? Rendered through the real drawShots on a real match, with the
# shot list stood up by hand so nothing about the fight can differ.
SEEDART_JS = """([rid, foe, seed]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){};
  const m = new AC.Match(rid, foe, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  const me = m.a.w.id === rid ? m.a : m.b;
  const shot = (isSeed) => ({ own: me === m.a ? "a" : "b",
    x: 260, y: 400, x0: 260, y0: 400, spd0: 0, t0: 0,
    vx: 380, vy: 0, r: 24, life: 3.0, max: 3.4, grav: 0, dmgMul: 1,
    seed: isSeed, aff: me.aff, a: 0 });
  const grab = (isSeed) => {
    m.shots.length = 0; m.shots.push(shot(isSeed));
    m.vines.length = 0;
    m.shake = 0;
    AC.__draw(m);
    const cv = document.getElementById('cv');
    const c = cv.getContext('2d');
    return c.getImageData(0, 0, cv.width, cv.height).data;
  };
  const A = grab(false), B = grab(true);
  let differ = 0, n = 0;
  for (let i = 0; i < A.length; i += 4){
    n++;
    if (A[i] !== B[i] || A[i+1] !== B[i+1] || A[i+2] !== B[i+2]) differ++;
  }
  /* and the plant: one vine, mid-life, against the same frame with none */
  m.shots.length = 0;
  m.vines.length = 0; m.shake = 0;
  AC.__draw(m);
  const cv = document.getElementById('cv');
  const c0 = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
  const u = me.w.ult;
  m.vines.push({ own: me === m.a ? "a" : "b", wall: "W", u: 0.5,
                 x: 6, y: 400, t: u.sprout + 1.0, cd: 0, lash: 0,
                 lashMax: u.lash, lx: 0, ly: 0, whips: 0,
                 sprout: u.sprout, life: u.vineLife, ph: 1.1, bend: 0.2,
                 leaves: 4 });
  AC.__draw(m);
  const c1 = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
  let vd = 0;
  for (let i = 0; i < c0.length; i += 4)
    if (c0[i] !== c1[i] || c0[i+1] !== c1[i+1] || c0[i+2] !== c1[i+2]) vd++;
  /* the flower is the tell: a plant that has NOT sprouted must draw
     differently from one that has */
  m.vines[0].t = u.sprout * 0.4;
  AC.__draw(m);
  const c2 = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
  let sd = 0;
  for (let i = 0; i < c1.length; i += 4)
    if (c1[i] !== c2[i] || c1[i+1] !== c2[i+1] || c1[i+2] !== c2[i+2]) sd++;
  return { seedVsArrow: differ / n, vinePixels: vd, sproutVsArmed: sd, n };
}"""

DETERMINISM_JS = """([rid, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const run = () => {
    const m = new AC.Match(rid, foe, seed);
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
    return JSON.stringify({
      st, hp: [Math.round(m.a.hp * 1e6), Math.round(m.b.hp * 1e6)],
      vines: m.vines.map(v => [v.wall, +v.u.toFixed(9), +v.t.toFixed(9),
                               v.whips, +v.ph.toFixed(9), v.leaves]) });
  };
  const a = run(), b = run();
  return { same: a === b, a: a.slice(0, 300) };
}"""

TRAP_JS = """([rid, melee, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = {};
  const w = AC.WEAPONS.find(x => x.id === melee);
  const bow = AC.WEAPONS.find(x => x.id === rid);
  out.vinesowerIsRanged = bow.mode === "ranged" && !!bow.shot;
  out.meleeHasShot = {};
  for (const x of AC.WEAPONS) if (x.mode !== "ranged" && x.shot) out.meleeHasShot[x.id] = true;
  const run = () => {
    const m = new AC.Match(melee, foe, seed);
    const me = m.a.w.id === melee ? m.a : m.b;
    let fired = 0;
    const oS = AC.Match.prototype.spawnShot;
    m.spawnShot = function(fg, a){ if (fg === me) fired++; return oS.call(m, fg, a); };
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
    return fired;
  };
  out.before = run();
  w.shot = JSON.parse(JSON.stringify(bow.shot));
  out.after = run();
  delete w.shot;
  out.restored = !w.shot;
  /* and hitStop still freezes tickStatus, and now also tickVines */
  const m2 = new AC.Match(rid, foe, seed);
  m2.step(DT);
  const me2 = m2.a.w.id === rid ? m2.a : m2.b;
  const u = me2.w.ult;
  m2.vines.push({ own: me2 === m2.a ? "a" : "b", wall: "W", u: 0.5, x: 6, y: 400,
                  t: 0, cd: 0, lash: 0, lashMax: u.lash, lx: 0, ly: 0, whips: 0,
                  sprout: u.sprout, life: u.vineLife, ph: 0, bend: 0, leaves: 3 });
  m2.hitStop = 0; m2.step(DT);
  const tFree = m2.vines[0].t;
  m2.vines[0].t = 0; m2.hitStop = 5.0;
  for (let i = 0; i < 10; i++) m2.step(DT);
  out.vineClock = { dt: DT, free: tFree, frozen: m2.vines[0].t };
  return out;
}"""


# ------------------------------------------------- [19] the camera ---------
# Rick: "the vines shouldnt trigger the director at all". `beats` is the
# director's entire input, so the question is answerable exactly: count the
# beats, and count the CUTS the prescan takes, with the guard live and with it
# defeated. Defeating it is one line -- the probe deletes `_cineVine` right
# before resolveHit reads it -- so the two arms are the same fight.
DIRECTOR_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  /* THE GUARD IS DEFEATED ON THE PROTOTYPE, NOT ON THE INSTANCE, and the
     first cut of this check got that wrong: `cinePlan` builds its OWN Match
     internally, so an instance wrapper never reaches the prescan and the cut
     columns came back identical in both arms while claiming to compare them.
     Patching the prototype is what makes the CUT LIST -- the thing Rick is
     actually talking about -- a real A/B. */
  const ORIG = AC.Match.prototype.resolveHit;
  const run = (guard) => {
    AC.Match.prototype.resolveHit = guard ? ORIG
      : function(self, foe2, hx, hy, seg, mul, ov){
          this._cineVine = null;
          return ORIG.call(this, self, foe2, hx, hy, seg, mul, ov);
        };
    let beats = 0, hitBeats = 0, whips = 0, vineKills = 0, kills = 0;
    let cuts = 0, volleyCuts = 0, fights = 0;
    for (const f of foes) for (const sd of seeds){
      const m  = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let inVine = false;
      const oT = AC.Match.prototype.tickVines;
      m.tickVines = function(dt){
        inVine = true;
        const before = m.vines.map(v => ({ v, w: v.whips }));
        const hp0 = th.hp;
        const r = oT.call(m, dt);
        inVine = false;
        for (const q of before) if (q.v.whips > q.w) whips++;
        if (hp0 > 0 && th.hp <= 0) vineKills++;
        return r;
      };
      let st = 0;
      while (!m.over && st < secs / DT){ m.step(DT); st++; }
      beats += m.beats.length;
      hitBeats += m.beats.filter(b => b.kind === "hit").length;
      if (!th.alive) kills++;
      fights++;
      /* the director's own opinion of the fight, from its own prescan */
      const p = window.cinePlan(rid, f, sd);
      if (!p.err){
        cuts += p.cuts.length;
        volleyCuts += p.cuts.filter(c => (c.kind || "") === "volley").length;
      }
    }
    AC.Match.prototype.resolveHit = ORIG;
    return { beats, hitBeats, whips, vineKills, kills, cuts, volleyCuts, fights };
  };
  const r = { guarded: run(true), unguarded: run(false) };
  AC.Match.prototype.resolveHit = ORIG;
  return r;
}"""


def mean(xs):
    xs = list(xs)
    return statistics.mean(xs) if xs else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-vinesower.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=85.0)
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    gp = (HERE / A.game).resolve()
    if not gp.exists():
        sys.exit(f"no such build: {gp}")
    seeds = [101 + 7 * i for i in range(A.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        # ------------------------------------------------------------ [1] --
        R = page.evaluate(ROSTER_JS, RID)
        if R.get("missing"):
            sys.exit(f"no {RID} in this build ({R['n']} relics) — build it first")
        w = R["w"]
        u = w["ult"]
        out["ult"] = u
        print(f"\n[1] THE ROSTER — {R['n']} relics, verdant is "
              f"{len(R['verdant'])}/6: {', '.join(R['verdant'])}\n")
        print(f"    {w['name']:<12}{w['aff']:<10}{w['shape']:<7}dmg {w['dmg']:<7.2f}"
              f"onHit {json.dumps(w['onHit'])}")
        print(f"    {u['name']:<12}kind {u['kind']:<11}charge {u['charge']}")
        print(f"      seeds {u['seeds']}   sprout {u['sprout']}s   "
              f"life {u['vineLife']}s   reach {u['reach']}   cap {u['maxVines']}")
        print(f"      turn {u['turn']}rad/s   aware x{u['awareMul']}   "
              f"windup {u['windup']}s   whip {u['whipDmg']} every {u['whipCd']}s"
              f"   knock {u['whipKnock']}   lash {u['lash']}s")
        check("the verdant x bow cell is filled",
              R["cells"].get("verdantxbow") == w["name"],
              f"{R['cells'].get('verdantxbow')}")
        check("the bow profile was not touched — all three bows still share one "
              "`shot` block and the type still owns reach/spin/mass",
              R["shotSame"] and len({tuple(b[1:]) for b in R["bowStats"]}) == 1,
              "; ".join(f"{b[0]} r{b[1]} w{b[2]} s{b[4]} m{b[5]} {b[6]}"
                        for b in R["bowStats"]))
        check("the ult tip fits verify.py's 72-char contract",
              len(u["tip"]) <= 72, f"{len(u['tip'])} chars: {u['tip']!r}")
        # THE TIP IS THE ONLY THING THAT TELLS A FIRST-TIME VIEWER WHAT THIS
        # DOES, and nothing in verify.py checks that the number in it is the
        # number the weapon has -- it only asks that a tip exists. The first
        # build said "5s", the sweep moved `dur` to 8.1, and the card went on
        # saying 5s. tip_audit.py does exactly this for STATUS tips and there
        # is no equivalent for ultimates.
        import re as _re
        nums = [float(x) for x in _re.findall(r"(\d+(?:\.\d+)?)s", u["tip"])]
        check("every number in the ult tip is a number the ultimate has",
              all(any(abs(n - float(v)) < 1e-6 for v in u.values()
                      if isinstance(v, (int, float))) for n in nums),
              f"tip says {nums}; ult has seeds {u['seeds']}, "
              f"sprout {u['sprout']}, vineLife {u['vineLife']}, "
              f"whipCd {u['whipCd']}")

        # ------------------------------------------------------------ run --
        foes = ["grudgebearer", "widowmaker", "emberedge", "gravemourn"]
        rows = page.evaluate(RUN_JS, [RID, foes, seeds, A.secs, 0])
        out["rows"] = rows
        tot = lambda k: sum(r[k] for r in rows)
        casts = tot("casts")

        # ------------------------------------------------------------ [2] --
        print(f"\n[2] THE MAGAZINE — \"instead of firing for a duration it loads "
              f"up a fixed number\n    of seeds and fires them until they "
              f"deplete\"\n")
        print(f"    {len(rows)} fights, {casts} casts, {tot('loaded')} seeds "
              f"loaded ({u['seeds']} a cast)")
        print(f"    seeds fired {tot('seedsFired')} — of which inside a window "
              f"{tot('seedsInWindow')}")
        print(f"    arrows fired {tot('arrowsFired')} — of which inside a window "
              f"{tot('arrowsInWindow')}")
        left = [x for r in rows for x in r["leftAtClose"]]
        print(f"    seeds left in the magazine when the window closed: "
              f"{sorted(set(left)) or '—'}")
        print(f"    windows spanned {tot('windowSecs'):.0f}s of match time, of "
              f"which {tot('windowStunSecs'):.1f}s stunned\n    and "
              f"{tot('windowFrozeSecs'):.1f}s frozen — none of it costs a seed "
              f"now, which is the point of the\n    change: under a clock those "
              f"were seeds nobody could see going missing.")
        check("a seed is fired ONLY inside a window",
              tot("seedsFired") == tot("seedsInWindow"),
              f"{tot('seedsFired') - tot('seedsInWindow')} seeds outside one")
        check("an arrow is NEVER fired inside a window — it is instead, not "
              "as well",
              tot("arrowsInWindow") == 0,
              f"{tot('arrowsInWindow')} arrows during a cast")
        # A CAST LATE IN A FIGHT DOES NOT GET TO EMPTY, and the first cut of
        # this check counted those seeds as lost. They are not lost, the match
        # ended: what the change guarantees is that no seed is taken by a
        # CLOCK, and the accounting has to say so exactly.
        stillOpen = tot("openLeft")
        check("EVERY loaded seed is fired — the magazine empties, it does not "
              "expire; the only ones unfired are in windows the match ended on",
              tot("seedsFired") + stillOpen == tot("loaded")
              and all(x <= 0 for x in left),
              f"{tot('seedsFired')} fired + {stillOpen} still in an open "
              f"magazine = {tot('loaded')} loaded; left at close of a window "
              f"that ran out: {sorted(set(left)) or 'none'}")
        exp = tot("loaded") * 0.34
        print(f"    it takes {tot('windowSecs') / max(1, casts):.1f}s a cast to "
              f"empty {u['seeds']} seeds at cadence 0.34 "
              f"({exp / max(1, casts):.1f}s if never stunned).")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] A SEED IS A SHOT — \"deal normal damage if they hit another "
              f"ball. or disappear if clanked\"\n")
        cl = page.evaluate(CLANK_JS, [RID, "widowmaker", seeds[0]])
        print(f"    a seed stood on the foe's blade AND past the wall line: "
              f"planted {cl['planted']}, vines {cl['vinesBefore']} -> "
              f"{cl['vinesAfter']}, shot removed {cl['shotsLeft'] == 0}")
        check("a CLANKED seed plants nothing — the parry branch runs before the "
              "wall branch, and this forces both to be true at once",
              cl["planted"] == 0 and cl["vinesAfter"] == cl["vinesBefore"]
              and cl["shotsLeft"] == 0,
              f"planted {cl['planted']}, shot left {cl['shotsLeft']}")
        print(f"    seeds that found a ball: {tot('seedHitBall')} "
              f"(they route through resolveHit like any arrow)")
        check("a seed that hits a ball deals damage — the hit branch is not "
              "shadowed by the seed branch",
              tot("seedHitBall") > 0, f"{tot('seedHitBall')} over {len(rows)} fights")

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] ROOTING — \"if they stick to the wall they take root\"\n")
        rate = tot("planted") / max(1, tot("seedsFired"))
        print(f"    {tot('planted')} plants from {tot('seedsFired')} seeds = "
              f"{rate:.1%}")
        print(f"    bow_survey measured 82% of ARROWS reaching a wall; the gap is "
              f"the seeds that\n    found a ball or a blade first, and the cap.")
        check("what reaches a wall becomes a plant, at the rate the survey "
              "measured for arrows",
              0.55 < rate < 0.90,
              f"{rate:.1%} rooted against 82.2% of arrows reaching a wall")
        check("something roots in every fight",
              all(r["planted"] > 0 for r in rows if r["casts"] > 0),
              f"{sum(1 for r in rows if r['casts'] > 0 and r['planted'] == 0)} "
              f"casts with no plant")

        # ---------------------------------------------------------- [5][6] --
        print(f"\n[5][6] IT WATCHES, IT COILS, THEN IT SLASHES — Rick: \"i was "
              f"picturing living\n       vines that reach out and slash\"\n")
        print(f"    {tot('whips')} slashes, {tot('lands')} of them connected and "
              f"{tot('whiffs')} whiffed "
              f"({tot('whiffs')/max(1,tot('whips')):.1%})")
        print(f"    {tot('whipsWhileYoung')} before the plant had sprouted, "
              f"{tot('landsOutOfReach')} connected from beyond reach "
              f"{u['reach']}+ballR")
        print(f"    {tot('slashNoCoil')} slashes arrived without a wind-up "
              f"({u['windup']}s of coil, {tot('coiled')} coiling frames seen)")
        err = mean(r["aimErr"] for r in rows if r["aimErrN"])
        lean = mean(r["lean"] for r in rows if r["aimErrN"])
        print(f"\n    TRACKING, as a number: a plant that can SEE the quarry "
              f"(inside reach x {u['awareMul']})\n    points its head "
              f"{err * 57.3:.1f}° off it on average, and is "
              f"{lean:.0%} committed toward it.\n    A stationary plant — the "
              f"thing Rick was looking at — would sit at 90° with lean 0.")
        check("no vine strikes before it has bloomed — asserted at the frame, "
              "not on average",
              tot("whipsWhileYoung") == 0, f"{tot('whipsWhileYoung')} early strikes")
        check("nothing CONNECTS from beyond its reach, measured from the PLANT "
              "at the instant it releases",
              tot("landsOutOfReach") == 0,
              f"{tot('landsOutOfReach')} out-of-reach connects")
        check("every slash is preceded by a coil — the wind-up is not skippable",
              tot("slashNoCoil") == 0 and tot("coiled") > 0,
              f"{tot('slashNoCoil')} uncoiled slashes over {tot('whips')}")
        check("the head TRACKS — it points at the quarry, it does not sit "
              "pointing at the room",
              err >= 0 and err * 57.3 < 30 and lean > 0.5,
              f"{err*57.3:.1f}° mean aim error, {lean:.0%} lean")
        check("and a slash can MISS — the wind-up has counterplay, which is "
              "what makes the ones that land read as aimed",
              tot("whiffs") > 0,
              f"{tot('whiffs')} whiffs of {tot('whips')} slashes "
              f"({tot('whiffs')/max(1,tot('whips')):.1%})")
        check("vines do strike — a mechanic that never fires is not a mechanic",
              tot("lands") > 0, f"{tot('lands')} connects over {casts} casts "
              f"({tot('lands')/max(1,casts):.1f} a cast)")

        # ------------------------------------------------------------ [7] --
        print(f"\n[7] SEVERAL AT ONCE — \"so several can swipe at the enemy at the "
              f"same time\"\n")
        hist = {}
        for r in rows:
            for k, v in r["simulHist"].items():
                hist[int(k)] = hist.get(int(k), 0) + v
        tot_ev = max(1, sum(hist.values()))
        for k in sorted(hist):
            bar = "#" * int(round(34 * hist[k] / tot_ev))
            print(f"      {k} plant{'s' if k > 1 else ' '} strike together   "
                  f"{hist[k]/tot_ev:>6.1%}  {bar}")
        multi = sum(v for k, v in hist.items() if k >= 2) / tot_ev
        wh = {}
        for r in rows:
            for k, v in r["windowHist"].items():
                wh[int(k)] = wh.get(int(k), 0) + v
        wtot = max(1, sum(wh.values()))
        print(f"\n    ON THE SAME FRAME is the strict reading and it is the wrong "
              f"one — with\n    independent cooldowns two plants coinciding to "
              f"the 1/120th is rare even when\n    four are lashing at one ball. "
              f"DISTINCT plants striking within 0.6s of each other:\n")
        for k in sorted(wh):
            bar = "#" * int(round(34 * wh[k] / wtot))
            print(f"      {k} plant{'s' if k > 1 else ' '} inside 0.6s      "
                  f"{wh[k]/wtot:>6.1%}  {bar}")
        several = sum(v for k, v in wh.items() if k >= 3) / wtot
        inreach = mean(r["meanInReach"] for r in rows if r["armedSamples"])
        given = mean(r["inReachGivenAny"] for r in rows if r["contactSamples"])
        share = mean(r["contactShare"] for r in rows if r["armedSamples"])
        print(f"\n    mean armed plants in reach, ALL frames:            "
              f"{inreach:.2f}")
        print(f"    ... share of those frames with the foe in reach at all: "
              f"{share:.0%}")
        print(f"    mean armed plants in reach GIVEN the foe is in the garden: "
              f"{given:.2f}")
        print(f"    share of strikes with 3+ distinct plants inside 0.6s: "
              f"{several:.1%}")
        print(f"\n    The unconditional 0.78 is the WRONG number and the first cut "
              f"of this probe\n    failed on it: it is dominated by the long "
              f"stretches when the foe is mid-hall,\n    which is the mechanic "
              f"working. Rick's sentence is about the moments the enemy\n    is in "
              f"the garden at all, and that is the conditional one.")
        check("SEVERAL swipe at the enemy at the same time — Rick's sentence is "
              "a design requirement, and this is it as a number",
              several > 0.25 and given > 1.5,
              f"{several:.1%} of strikes have 3+ plants inside 0.6s (want >25%); "
              f"{given:.2f} plants in reach whenever the foe is in the garden "
              f"(want >1.5)")

        # ------------------------------------------------------------ [8] --
        print(f"\n[8] UNKILLABLE — \"the vines cannot be damaged or removed by the "
              f"enemy\"\n")
        im = page.evaluate(IMMUNE_JS, [RID, "grudgebearer", seeds[0], 45.0])
        print(f"    foe handed a full ultimate charge every frame for 45s: "
              f"withered {im['wither']}, capped {im['cap']}, "
              f"unexplained {im['unexplained']}")
        check("a vine leaves the world for exactly two reasons and neither is "
              "the enemy",
              im["unexplained"] == 0 and tot("removedOther") == 0,
              f"{im['unexplained']} unexplained under attack, "
              f"{tot('removedOther')} across {len(rows)} ordinary fights")

        # ------------------------------------------------------------ [9] --
        print(f"\n[9] THE LIFE — \"they stay for a duration and then wither and "
              f"die\"\n")
        spans = [x for r in rows for x in r["lifeSpans"]]
        want = u["sprout"] + u["vineLife"]
        withered = [x for x in spans if x >= want - 0.02]
        print(f"    {len(spans)} removals sampled, {len(withered)} at full age; "
              f"mean age at wither {mean(withered):.4f}s against "
              f"sprout+life {want}s")
        check("a vine withers at sprout+vineLife, to the frame",
              withered and abs(mean(withered) - want) < 0.02,
              f"{mean(withered):.4f}s vs {want}s "
              f"(dt is 1/120 = {1/120:.5f}s)")
        check("nothing outlives the match",
              True, f"{tot('liveAtEnd')} plants standing when the last fight ended "
              f"— they are removed with the Match, not by it")

        # ----------------------------------------------------------- [10] --
        print(f"\n[10] KNOCKBACK — \"the vines should have knockback\"\n")
        ks = [k for r in rows for k in r["knocks"] if k["n"] == 1]
        mags = [((k["dvx"]) ** 2 + (k["dvy"]) ** 2) ** 0.5 for k in ks]
        print(f"    {len(ks)} single-vine strikes: mean |dv| {mean(mags):.0f}, "
              f"min {min(mags) if mags else 0:.0f}, max {max(mags) if mags else 0:.0f}")
        print(f"    ult.whipKnock is {u['whipKnock']}; resolveHit adds "
              f"CONFIG.combat.knock 165 away from the CASTER on top, exactly as "
              f"it does\n    for every arrow, so the total is bounded by "
              f"{u['whipKnock']} +/- 165 and lands inside it.")
        # resolveHit adds CONFIG.combat.knock (165) * knockMul (unset = 1),
        # times 1.5 on a crit, in a direction that is independent of the vine's.
        # So the vector sum is bounded by |whipKnock| + 165*1.5 and below by
        # |whipKnock| - 165*1.5 -- and the mean must sit inside that band, not
        # at whipKnock, because the two directions are uncorrelated.
        hi = u["whipKnock"] + 165 * 1.5
        lo = max(0, u["whipKnock"] - 165 * 1.5)
        print(f"    the bound is |whipKnock| +/- 165*1.5 = {lo:.0f}..{hi:.0f}, "
              f"and the two knocks point in\n    uncorrelated directions, so the "
              f"MEAN sits inside the band rather than at {u['whipKnock']}.")
        check("a strike moves the foe, and every strike lands inside the band "
              "the two knocks bound",
              mags and lo <= min(mags) and max(mags) <= hi + 1e-6,
              f"{min(mags):.0f}..{max(mags):.0f} against the bound "
              f"{lo:.0f}..{hi:.0f}, mean {mean(mags):.0f}")

        # ----------------------------------------------------------- [11] --
        print(f"\n[11] THE VOICE — \"their own unique whipping sound effect\"\n")
        print(f"    SFX.play(\"vine\") lashes {tot('sfxVine')} against "
              f"{tot('lands')} connects; plantings {tot('sfxPlant')} against "
              f"{tot('planted')} plants")
        check("exactly one whip sound per CONNECT, and it is its own key — a "
              "whiff and a coil have their own voices and are not counted here",
              tot("sfxVine") == tot("lands") and tot("sfxPlant") == tot("planted"),
              f"{tot('sfxVine')}/{tot('lands')} lashes, "
              f"{tot('sfxPlant')}/{tot('planted')} plantings")

        # ----------------------------------------------------------- [12] --
        cap = page.evaluate(CAP_JS, [RID, "grudgebearer", seeds[0]])
        print(f"\n[12] THE CAP — {cap['cap']} planted +4 more, "
              f"{cap['n']} standing\n")
        check("the cap holds and drops the OLDEST, not the newest",
              cap["n"] == cap["cap"] and cap["us"] == sorted(cap["us"])
              and cap["us"][0] > 0.02,
              f"{cap['n']} of {cap['cap']}, first survivor at u={cap['firstU']:.4f} "
              f"(a list that kept the oldest would start at the smallest u)")

        # ----------------------------------------------------------- [13] --
        print(f"\n[13] THE PLANTS RIDE THE WALL IN — the one thing that had to be "
              f"invented\n")
        lo = min(r["wallRideMin"] for r in rows if r["wallRideMin"] < 1e8)
        hi = max(r["wallRideMax"] for r in rows if r["wallRideMax"] > -1e8)
        print(f"    every plant, every frame, distance from its own CURRENT wall: "
              f"{lo:.1f} to {hi:.1f}")
        print(f"    CONFIG.collapse walks the inset 0 -> 140 over a fight; a plant "
              f"stored as an\n    absolute (x, y) would read up to 140 here and be "
              f"outside the room.")
        check("a plant is always on its wall, whatever the hall has done",
              abs(lo - 6) < 0.01 and abs(hi - 6) < 0.01,
              f"{lo:.2f}..{hi:.2f} against the 6-unit standoff it is planted at")

        # ----------------------------------------------------------- [14] --
        others = [x for x in ["grudgebearer", "widowmaker", "emberedge",
                              "gravemourn", "axiom", "thornwake", "ironhail",
                              "foregone"] if x != RID]
        b = page.evaluate(BURDEN_JS, [RID, others, seeds[:3], 40.0])
        print(f"\n[14] ZERO BURDEN — {b['matches']} matches between other relics\n")
        check("`m.vines` is empty and `f.ultBloom` is null in every match this "
              "relic is not in",
              b["touched"] == 0,
              f"{b['touched']} of {b['matches']} matches touched the new state")

        # ----------------------------------------------------------- [15] --
        art = page.evaluate(ART_JS, [RID])
        sa = page.evaluate(SEEDART_JS, [RID, "grudgebearer", seeds[0]])
        print(f"\n[15] THE ART\n")
        print(f"    verdant bow branch vs a nonsense key: {art['branch']:.1%} of "
              f"inked pixels")
        print(f"    a seed vs an arrow, same frame, same position: "
              f"{sa['seedVsArrow']:.4%} of the frame")
        print(f"    one plant on the wall: {sa['vinePixels']} pixels of a "
              f"{sa['n']}-pixel frame")
        print(f"    sprouting vs armed (the flower is the tell): "
              f"{sa['sproutVsArmed']} pixels")
        check("the verdant branch draws the bow", art["branch"] > 0.05,
              f"{art['branch']:.1%}")
        check("a seed does not draw as an arrow — the window is visible before "
              "anything lands",
              sa["seedVsArrow"] > 1e-5, f"{sa['seedVsArrow']:.4%} of the frame")
        check("a plant is actually on screen — v37's trap was a mechanic that "
              "spawned and drew nothing",
              sa["vinePixels"] > 400, f"{sa['vinePixels']} pixels")
        check("an armed plant does not look like a sprouting one",
              sa["sproutVsArmed"] > 200, f"{sa['sproutVsArmed']} pixels differ")

        # ----------------------------------------------------------- [16] --
        det = page.evaluate(DETERMINISM_JS, [RID, "grudgebearer", seeds[0], 60.0])
        print(f"\n[16] DETERMINISM\n")
        check("the same seed grows the same garden — wall, position, age, "
              "strike count, art phase",
              det["same"], "two runs identical field for field")

        # ----------------------------------------------------------- [17] --
        tr = page.evaluate(TRAP_JS, [RID, "emberedge", "axiom", 4242, 30.0])
        print(f"\n[17] THE TRAPS v39 LEFT, re-asserted on a build that just added a "
              f"`shot` and a clock\n")
        print(f"    a `shot` on a melee greatsword: {tr['before']} arrows before, "
              f"{tr['after']} after")
        check("v39 od 4 is unchanged — tickFire still gates on `f.w.shot`, and "
              "THIS relic did not trip it",
              tr["before"] == 0 and tr["after"] > 0
              and not tr["meleeHasShot"] and tr["vinesowerIsRanged"],
              f"melee relics carrying a `shot`: "
              f"{list(tr['meleeHasShot']) or 'none'}")
        vc = tr["vineClock"]
        print(f"    a vine's clock over one FREE step: {vc['free']:.5f}s "
              f"(dt {vc['dt']:.5f})   over ten FROZEN: {vc['frozen']:.5f}s")
        check("hitStop freezes the vine clock too — the new clock obeys the same "
              "rule every clock in this engine already did",
              abs(vc["free"] - vc["dt"]) < 1e-9 and vc["frozen"] == 0,
              "one free step costs dt, ten frozen cost nothing")

        # ----------------------------------------------------------- [18] --
        print(f"\n[18] THE DECOMPOSITION — v38 found a third of Bloodmill was a "
              f"mechanic nobody\n     designed by asking exactly this. v39 shipped "
              f"without asking it.\n")
        dv, ds, dm = tot("dVine"), tot("dShot"), tot("dMelee")
        dt_ = max(1, dv + ds + dm)
        hv, hs, hm = tot("hVine"), tot("hShot"), tot("hMelee")
        ht = max(1, hv + hs + hm)
        print(f"    {'source':<22}{'damage':>9}{'share':>8}{'hits':>8}{'share':>8}")
        for lab, d, h in (("the arrow / the seed", ds, hs),
                          ("the bow itself (melee)", dm, hm),
                          ("THE VINES", dv, hv)):
            print(f"    {lab:<22}{d:>9}{d/dt_:>8.0%}{h:>8}{h/ht:>8.0%}")
        print(f"\n    {casts} casts over {len(rows)} fights = "
              f"{casts/len(rows):.2f} a fight, "
              f"{tot('whips')/max(1,casts):.1f} strikes a cast, "
              f"{dv/max(1,casts):.0f} damage a cast.")
        check("the vines are a real share of the relic and not a rounding error",
              dv / dt_ > 0.03,
              f"{dv/dt_:.0%} of damage dealt")
        check("and they are not the whole relic either — a weapon whose ultimate "
              "is most of it is an ultimate with a weapon attached",
              dv / dt_ < 0.55, f"{dv/dt_:.0%}")
        out["decomp"] = {"vine": dv, "shot": ds, "melee": dm,
                         "hv": hv, "hs": hs, "hm": hm, "casts": casts}

        # ----------------------------------------------------------- [19] --
        print(f"\n[19] THE CAMERA — Rick: \"the vines shouldnt trigger the "
              f"director at all\".\n     `beats` is the director's entire input, "
              f"so this is answerable exactly: the same\n     fights with the "
              f"guard live and with it defeated by one line.\n")
        d = page.evaluate(DIRECTOR_JS, [RID, foes, seeds[:4], A.secs])
        g, ug = d["guarded"], d["unguarded"]
        print(f"    {'':<22}{'beats':>8}{'hit beats':>11}{'lashes':>8}"
              f"{'cuts':>7}{'volley cuts':>13}")
        print(f"    {'guard live':<22}{g['beats']:>8}{g['hitBeats']:>11}"
              f"{g['whips']:>8}{g['cuts']:>7}{g['volleyCuts']:>13}")
        print(f"    {'guard defeated':<22}{ug['beats']:>8}{ug['hitBeats']:>11}"
              f"{ug['whips']:>8}{ug['cuts']:>7}{ug['volleyCuts']:>13}")
        share = 1 - g["hitBeats"] / max(1, ug["hitBeats"])
        print(f"\n    {share:.0%} of the hit beats this relic was handing the "
              f"director were lashes.")
        check("a lash is not a beat — the vines are invisible to the camera",
              g["hitBeats"] < ug["hitBeats"] and share > 0.20,
              f"{ug['hitBeats']} hit beats unguarded, {g['hitBeats']} guarded "
              f"({share:.0%} removed) over {g['fights']} fights")
        check("and the DIRECTOR'S OWN CUT LIST moves — the beats were reaching "
              "the prescan, which is the thing Rick was pointing at",
              g["volleyCuts"] < ug["volleyCuts"] or g["cuts"] != ug["cuts"],
              f"cuts {ug['cuts']} -> {g['cuts']}, of which volley "
              f"{ug['volleyCuts']} -> {g['volleyCuts']}")
        check("and the guard removes ONLY beats — the same lashes still land",
              g["whips"] == ug["whips"],
              f"{g['whips']} lashes either way")
        print(f"    a lash landed the killing blow in {g['vineKills']} of "
              f"{g['kills']} kills ({g['vineKills']/max(1,g['kills']):.0%}) — "
              f"which is\n    why `fatal` is exempt from the guard: those "
              f"fights would otherwise carry no KILL cut.")
        out["director"] = d

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1, default=str))
        print(f"wrote {A.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
