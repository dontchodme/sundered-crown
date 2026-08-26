#!/usr/bin/env python3
"""LOOK AT THE FOUR OPEN BOW CELLS BEFORE CHOOSING ONE.

    python3 bow_survey.py --game ../02-chain/sc-foregone.html

v39's `cell_survey` looked at all 42 cells at once, which is the right
instrument for "which type" and the wrong one for "which school on THIS type".
Rick has picked the type. This is the same discipline pointed at one row.

The bow is not a sixth melee shape with a longer arm. It is the only
`mode:"ranged"` type in the game, it is the only type whose contacts can be
DESTROYED IN FLIGHT by the foe, and it is the type on which cell_survey
measured the HIGHEST contact rate in the game (0.352 hits/s against the
scythe's 0.196) off the SHORTEST reach in the game (54). None of that is
explained anywhere in the tree, and a design priced against the melee
intuition would be priced wrong.

  [1] THE GRID, and the four open bow cells. Read from AC.WEAPONS.

  [2] THE RANGED PATH, DECOMPOSED. v38 found a third of Bloodmill was a
      mechanic nobody designed, by decomposing. Nobody has decomposed a bow.
      Where does a bow's damage come from -- the arrow or the stick? What
      happens to the ~97% of arrows that do not land?

  [3] THE PARRY IS A PROPERTY OF THE FOE. `tickShots` bats a shot out of the
      air on any blade segment it touches, and `segs` is EMPTY while that
      fighter is stunned. So "hits from anywhere" is gated by the other
      weapon's geometry, and by whether the other weapon is running at all.

  [4] THE ART. Palette held, `p.key` varied -- v39's lesson, learned when an
      alpha mask reported the dwarven bow had no art and was flatly wrong.
      Plus the draw axis: the bow is the only shape whose art takes `k`.

  [5] THE FOUR CANDIDATE CLOCKS, as DELIVERED EFFECT. v39: occupancy is a
      proxy twice removed. Every one of these four statuses is a different
      KIND of thing, so each gets the readout its own mechanism deserves,
      and all four also get one model-free A/B: damage delivered with the
      channel, minus damage delivered with the channel deleted.

  [6] THE TWO FEEDBACK LOOPS, AND THEIR OWN NULL CONTROL. Entangle slows
      SPIN. Hex STUNS. Both of those are inputs to the parry, which is the
      thing standing between a bow and its damage. Curse and hemorrhage
      touch neither, so they are the control that makes the other two
      readable. Stacks are PINNED, not earned, so this is a controlled
      experiment and not an observation about who happened to win.

  [7] THE TRAPS v39 LEFT. Both are asserted, not assumed.

Injection is runtime-only. NOTHING is written to any build.
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

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


# --------------------------------------------------------------- [1] grid ---

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, width: w.width, artW: w.artW, dmg: w.dmg, spin: w.spin,
    mode: w.mode, mass: w.mass, arc: w.arc || null, blades: w.blades.length,
    shot: w.shot ? { cadence: w.shot.cadence, speed: w.shot.speed, r: w.shot.r,
                     life: w.shot.life, grav: w.shot.grav } : null,
    onHit: w.onHit ? Object.entries(w.onHit)[0] : null,
    onSelf: w.onSelf ? Object.entries(w.onSelf)[0] : null,
    ult: w.ult ? { name: w.ult.name, kind: w.ult.kind, charge: w.ult.charge } : null,
  }));
  const S = {};
  for (const [k, v] of Object.entries(AC.STATUS)) S[k] = Object.assign({}, v);
  return { weapons: W, status: S, affinities: Object.keys(AC.AFFINITIES),
           shotCfg: AC.CONFIG.shot, dt: AC.CONFIG.physics.dt,
           arena: AC.CONFIG.arena, ballR: AC.CONFIG.physics.ballR,
           shapeFns: Object.keys(AC.SHAPES).filter(n => typeof AC.SHAPES[n] === "function") };
}"""


# ------------------------------------------------- [2][3] ranged decomposed --
# Everything here is a WRAPPER around the shipped method. Nothing re-implements
# a predicate the game owns -- the one exception is the classification of a
# REMOVED shot, and that reads the shot's own final state, which the game has
# already finished mutating by the time the splice happens.
#
# The parry is tagged at its own effect call rather than inferred: it is the
# only `spawnFx(x, y, "#FFF4D0", 9, 240, ...)` in the file, it fires at the
# shot's exact position, and nothing moves the shot afterwards. Inferring it
# instead ("removed and not any of the others") would silently absorb every
# future sink somebody adds to tickShots.

RANGED_JS = r"""([shooter, foes, seeds, secs, pin, pinIds, noult, killStatus]) => {
  const DT = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena;

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null };
    if (pin > 0) x.dmg = pin;
    if (noult && x.ult) x.ult.charge = 1e9;
    if (killStatus){ delete x.onHit; delete x.onSelf; }
  }

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      let dShot = 0, dMelee = 0, hShot = 0, hMelee = 0, dTaken = 0;
      const origResolve = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const s = m._cineShot;
        const d0 = self.dealt, h0 = self.hits;
        const r = origResolve.call(m, self, foe2, hx, hy, seg, mul, over);
        const dd = self.dealt - d0, hh = self.hits - h0;
        if (self === me){
          if (s){ dShot += dd; hShot += hh; s._pHit = true; }
          else  { dMelee += dd; hMelee += hh; }
        } else { dTaken += dd; }
        return r;
      };

      let evicted = 0, fired = 0;
      const origSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, ang){
        if (m.shots.length >= AC.CONFIG.shot.maxLive) evicted++;
        fired++;
        return origSpawn.call(m, fg, ang);
      };

      /* Parry tag. Collected only while inside tickShots, so the identical
         signature could not be borrowed by another system later without this
         probe noticing it as an unmatched event. */
      let inShots = false;
      const parryFx = [];
      const origFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, life, size, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) parryFx.push(x + "," + y);
        return origFx.call(m, x, y, col, n, spd, life, size, dx, dy);
      };

      let hit = 0, parried = 0, walled = 0, expired = 0, popped = 0, ambig = 0, unknown = 0;
      const origTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice();
        parryFx.length = 0;
        inShots = true;
        const r = origTick.call(m, dt);
        inShots = false;
        if (pre.length){
          const live = new Set(m.shots);
          const n = m.inset;
          const P = new Set(parryFx);
          for (const s of pre){
            if (live.has(s)) continue;
            const spent = s.life <= 0 || s.x < n + s.r || s.x > A.w - n - s.r
                                      || s.y < n + s.r || s.y > A.h - n - s.r;
            if (P.has(s.x + "," + s.y)){ parried++; if (spent) ambig++; continue; }
            if (s._pHit){ hit++; continue; }
            if (s.shard && s.life <= 0){ popped++; continue; }
            if (s.life <= 0){ expired++; continue; }
            if (spent){ walled++; continue; }
            unknown++;
          }
        }
        return r;
      };

      /* Presence. How much of the fight the archer spends able to fire at
         all, and how much of it the FOE spends unable to parry. */
      let steps = 0, meStun = 0, thStun = 0, hstop = 0, liveShots = 0;
      let sepSum = 0, sepShotSum = 0, shotSamples = 0;
      const R = AC.CONFIG.physics.ballR;
      while (!m.over && steps < secs / DT){
        const hs = m.hitStop;
        m.step(DT); steps++;
        if (hs > 0) hstop++;
        if (me.stun > 0) meStun++;
        if (th.stun > 0) thStun++;
        liveShots += m.shots.length;
        const sep = Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
        sepSum += sep;
        for (const s of m.shots){ sepShotSum += Math.hypot(s.x - s.x0, s.y - s.y0); shotSamples++; }
      }

      rows.push({ foe: f, seed: sd, steps, dur: steps * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: me.dealt, taken: dTaken,
                  dShot, dMelee, hShot, hMelee,
                  fired, hit, parried, walled, expired, popped, evicted,
                  ambig, unknown, live: m.shots.length,
                  meStun: steps ? meStun / steps : 0,
                  thStun: steps ? thStun / steps : 0,
                  hstop:  steps ? hstop  / steps : 0,
                  meanLive: steps ? liveShots / steps : 0,
                  sep: steps ? sepSum / steps : 0,
                  flight: shotSamples ? sepShotSum / shotSamples : 0,
                  meHp: me.hp, thHp: th.hp, thMaxHp: th.maxHp });
    }
  }

  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
    delete x.onHit; delete x.onSelf;
    if (saved[pid].onHit) x.onHit = saved[pid].onHit;
    if (saved[pid].onSelf) x.onSelf = saved[pid].onSelf;
  }
  return rows;
}"""


# ------------------------------------------------------ [2] control: no-op --
# The instrument above shadows four prototype methods on one Match. If any of
# that perturbed the simulation, every number in [2] and [3] would be about
# the probe. Same seed, same matchup, instrumented and bare.

CONTROL_JS = r"""([shooter, foe, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const run = (instrument) => {
    const out = [];
    for (const sd of seeds){
      const m = new AC.Match(shooter, foe, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      if (instrument){
        const oR = AC.Match.prototype.resolveHit;
        m.resolveHit = function(...a){ const s = m._cineShot; if (s) s._pHit = true; return oR.call(m, ...a); };
        const oS = AC.Match.prototype.spawnShot;
        m.spawnShot = function(...a){ return oS.call(m, ...a); };
        const oF = AC.Match.prototype.spawnFx;
        m.spawnFx = function(...a){ return oF.call(m, ...a); };
        const oT = AC.Match.prototype.tickShots;
        m.tickShots = function(dt){ const pre = m.shots.slice(); const r = oT.call(m, dt);
                                    const live = new Set(m.shots); for (const s of pre) live.has(s); return r; };
      }
      let steps = 0;
      while (!m.over && steps < secs / DT){ m.step(DT); steps++; }
      out.push([steps, Math.round(me.hp * 1e6) / 1e6, Math.round(th.hp * 1e6) / 1e6,
                me.hits, th.hits, m.shotHits]);
    }
    return out;
  };
  return { bare: run(false), inst: run(true) };
}"""


# ------------------------------------------------------------- [4] the art --
# Lifted from cell_survey's INK_JS. ONE palette, N keys: every field comes
# from one school so no branch can trip over a field this probe forgot to
# fake, and `key` is the only thing that varies -- so a differing pixel is
# the DISPATCH and nothing else.

INK_JS = r"""([keys, D, artW, zoom, S, cx, k]) => {
  const draw = (palKey) => {
    const cv = document.createElement("canvas");
    cv.width = S * zoom; cv.height = S * zoom;
    const c = cv.getContext("2d");
    c.scale(zoom, zoom);
    c.translate(S * cx, S / 2);
    const pal = Object.assign({}, AC.AFFINITIES.dwarven,
                              { key: palKey === null ? "NOT_A_SCHOOL" : palKey });
    AC.SHAPES.bow(c, D, artW, pal, k);
    const d = c.getImageData(0, 0, cv.width, cv.height).data;
    const n = cv.width * cv.height;
    const px = new Int32Array(n);
    let x0 = cv.width, y0 = cv.height, x1 = -1, y1 = -1, ink = 0;
    for (let p = 0; p < n; p++){
      const i = p << 2;
      if (d[i+3] > 24){
        px[p] = 1 + ((d[i] << 16) | (d[i+1] << 8) | d[i+2]);
        ink++;
        const yy = (p / cv.width) | 0, xx = p % cv.width;
        if (xx < x0) x0 = xx; if (xx > x1) x1 = xx;
        if (yy < y0) y0 = yy; if (yy > y1) y1 = yy;
      }
    }
    return { px, ink, box: [x0, y0, x1, y1], w: cv.width, h: cv.height };
  };
  const shots = {};
  for (const kk of keys) shots[kk === null ? "NEG" : kk] = draw(kk);
  const rerun = draw(keys.find(kk => kk !== null));
  const cmp = (X, Y) => {
    let union = 0, differ = 0, inter = 0;
    const a = X.px, b = Y.px, n = a.length;
    for (let p = 0; p < n; p++){
      const x = a[p], y = b[p];
      if (x || y){ union++; if (x !== y) differ++; if (x && y) inter++; }
    }
    return { diff: union ? differ / union : 0, iou: union ? inter / union : 1 };
  };
  const names = keys.map(kk => kk === null ? "NEG" : kk);
  const M = {};
  for (let i = 0; i < names.length; i++)
    for (let j = i + 1; j < names.length; j++)
      M[names[i] + "|" + names[j]] = cmp(shots[names[i]], shots[names[j]]);
  const first = names.find(n => n !== "NEG");
  const boxes = {}, inks = {};
  for (const n of names){ boxes[n] = shots[n].box; inks[n] = shots[n].ink; }
  return { m: M, rerun: cmp(shots[first], rerun).diff, boxes, inks,
           w: shots[first].w, h: shots[first].h };
}"""


# ----------------------------------------------- [5] the clock, DELIVERED --
# cell_survey reported occupancy. v39 §5.2: occupancy is a proxy twice
# removed, because these four statuses are four different KINDS of object --
# hemorrhage is a damage rate, curse is a permanent subtraction, hex is a
# lock RATE, entangle is a pair of multipliers. Each gets its own readout,
# and all four get the same model-free A/B on top: hp removed from the foe
# with the channel, minus hp removed with the channel deleted.

CLOCK_JS = r"""([donor, aff, key, per, foes, seeds, pin, pinIds, secs, live]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = aff;
  delete w.onSelf; delete w.onHit;
  if (live){ w.onHit = {}; w.onHit[key] = per; }

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  const DEF = AC.STATUS[key];
  for (const f of foes){
    for (const s of seeds){
      const m  = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const hp0 = th.hp, maxHp0 = th.maxHp, meHp0 = me.hp;

      /* The hex fire is counted at its own site. `breakSpin` is called with a
         reason string that exists nowhere else, so this is the event and not
         a reconstruction of it from the stun trace -- which would have been
         wrong anyway, because hitstun writes the same field. */
      let fires = 0;
      const oBreak = AC.Match.prototype.breakSpin;
      m.breakSpin = function(fg, why){
        if (why === "the hex takes the wind out of it") fires++;
        return oBreak.call(m, fg, why);
      };
      let parried = 0, fired = 0;
      let inShots = false; const pfx = [];
      const oFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, l, sz, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) pfx.push(x + "," + y);
        return oFx.call(m, x, y, col, n, spd, l, sz, dx, dy);
      };
      const oSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, a){ fired++; return oSpawn.call(m, fg, a); };
      const oTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice(); pfx.length = 0; inShots = true;
        const r = oTick.call(m, dt); inShots = false;
        if (pre.length){ const P = new Set(pfx), L = new Set(m.shots);
          for (const q of pre) if (!L.has(q) && P.has(q.x + "," + q.y)) parried++; }
        return r;
      };

      let steps = 0, unfrozen = 0, sum = 0, ge2 = 0, geMax = 0, apps = 0, prevT = 0;
      let lock = 0, dot = 0, entSpin = 0, entMove = 0, capAt = -1, meLock = 0;
      const cap = DEF.maxStacks;
      /* FIXED WINDOWS. hp-per-second over a whole fight is confounded by how
         long the fight was, and every one of these channels changes that. The
         window is the same length in both arms of the A/B whatever happens
         after it, so it is the only column here that compares like with like. */
      const CK = [10, 20, 30], ckHp = [0, 0, 0], ckHit = [0, 0, 0], ckMe = [0, 0, 0];
      const ckThHit = [0, 0, 0], ckThDesp = [0, 0, 0], ckMeDesp = [0, 0, 0];
      const ckSep = [0, 0, 0], ckFroz = [0, 0, 0], ckThStun = [0, 0, 0];
      let thDesp = 0, meDesp = 0, sepSum = 0, frozen = 0;
      const BR = AC.CONFIG.physics.ballR;
      let ttk = -1, hitsPrev = 0, ckI = 0;
      while (!m.over && steps < secs / DT){
        const froze = m.hitStop > 0;
        m.step(DT); steps++;
        if (!froze) unfrozen++;
        const st = th.status[key];
        const t = st ? st.t : 0, n = st ? st.stacks : 0;
        if (t > prevT + 1e-9) apps++;
        prevT = t;
        sum += n;
        if (n >= 2) ge2++;
        if (n >= cap){ geMax++; if (capAt < 0) capAt = steps * DT; }
        if (th.stun > 0) lock++;
        if (me.stun > 0) meLock++;
        if (th.desperate) thDesp++;
        if (me.desperate) meDesp++;
        if (froze) frozen++;
        sepSum += Math.hypot(me.x - th.x, me.y - th.y) - 2 * BR;
        if (DEF.dps) dot += DEF.dps * n * DT * th.dmgTakenMul();
        if (DEF.spin){ entSpin += -DEF.spin * n; entMove += -DEF.move * n; }
        while (ckI < CK.length && steps * DT >= CK[ckI]){
          ckHp[ckI] = hp0 - th.hp; ckHit[ckI] = me.hits;
          ckMe[ckI] = meHp0 - me.hp;
          ckThHit[ckI] = th.hits;
          ckThDesp[ckI] = thDesp / steps; ckMeDesp[ckI] = meDesp / steps;
          ckSep[ckI] = sepSum / steps; ckFroz[ckI] = frozen / steps;
          ckThStun[ckI] = lock / steps;
          ckI++;
        }
        if (!th.alive && ttk < 0) ttk = steps * DT;
      }
      for (let i = ckI; i < CK.length; i++){ ckHp[i] = -1; ckHit[i] = -1; ckMe[i] = -1;
        ckThHit[i] = -1; ckThDesp[i] = -1; ckMeDesp[i] = -1;
        ckSep[i] = -1; ckFroz[i] = -1; ckThStun[i] = -1; }
      rows.push({ foe: f, seed: s, steps, dur: steps * DT, over: m.over,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: me.dealt,
                  hpOut: (hp0 - th.hp) + (maxHp0 - th.maxHp) * 0,
                  hpLost: hp0 - th.hp, maxHpEaten: maxHp0 - th.maxHp,
                  meanStacks: steps ? sum / steps : 0,
                  p2: steps ? ge2 / steps : 0, pMax: steps ? geMax / steps : 0,
                  apps, fires, capAt,
                  lock: steps ? lock / steps : 0,
                  meLock: steps ? meLock / steps : 0,
                  dot, entSpin: steps ? entSpin / steps : 0,
                  entMove: steps ? entMove / steps : 0,
                  frozen: steps ? 1 - unfrozen / steps : 0,
                  fired, parried, parryRate: fired ? parried / fired : 0,
                  ckHp, ckHit, ttk, hp0,
                  meTaken: meHp0 - me.hp, meHp0, ckMe, ckThHit, ckThDesp, ckMeDesp,
                  ckSep, ckFroz, ckThStun,
                  thHpEnd: th.hp, thMaxEnd: th.maxHp });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


# --------------------------------------------- [6] the loop, stacks PINNED --
# The status is written onto the foe every frame at a fixed level rather than
# earned, so contact rate cannot confound the answer: at every level the
# archer is the same archer and the only thing that moves is the foe.
#
# Curse and hemorrhage are in this table as the NULL: neither touches spin,
# move or stun, so if the parry rate slides with them too, the instrument is
# measuring something else and the entangle and hex rows mean nothing.

LOOP_JS = r"""([shooter, foes, seeds, secs, pin, pinIds, key, levels]) => {
  const DT = AC.CONFIG.physics.dt;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
    delete x.onHit; delete x.onSelf;      // NO channel: the pin is the only source
  }
  const A = AC.CONFIG.arena;
  const out = [];
  for (const lv of levels){
    let fired = 0, parried = 0, hit = 0, walled = 0, expired = 0;
    let steps = 0, thStun = 0, sep = 0, dealt = 0, meStun = 0;
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(shooter, f, sd);
        const me = m.a.w.id === shooter ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        let inShots = false; const pfx = [];
        const oFx = AC.Match.prototype.spawnFx;
        m.spawnFx = function(x, y, col, n, spd, l, sz, dx, dy){
          if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) pfx.push(x + "," + y);
          return oFx.call(m, x, y, col, n, spd, l, sz, dx, dy);
        };
        const oR = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const s = m._cineShot;
          const r = oR.call(m, self, foe2, hx, hy, seg, mul, over);
          if (s) s._pHit = true;
          return r;
        };
        const oSpawn = AC.Match.prototype.spawnShot;
        m.spawnShot = function(fg, a){ if (fg === me) fired++; return oSpawn.call(m, fg, a); };
        const oTick = AC.Match.prototype.tickShots;
        m.tickShots = function(dt){
          const pre = m.shots.slice(); pfx.length = 0; inShots = true;
          const r = oTick.call(m, dt); inShots = false;
          if (pre.length){
            const P = new Set(pfx), L = new Set(m.shots), n = m.inset;
            for (const q of pre){
              if (L.has(q) || q.own !== (me === m.a ? "a" : "b")) continue;
              if (P.has(q.x + "," + q.y)){ parried++; continue; }
              if (q._pHit){ hit++; continue; }
              if (q.life <= 0){ expired++; continue; }
              walled++;
            }
          }
          return r;
        };
        const R = AC.CONFIG.physics.ballR;
        let st2 = 0;
        while (!m.over && st2 < secs / DT){
          /* PINNED BEFORE THE STEP, so the step sees it. Written straight onto
             the status object rather than through apply(): apply() would re-pay
             curse's max-hp cost every frame, and this table is about the PARRY,
             not about damage. */
          if (lv > 0) th.status[key] = { stacks: lv, t: 999 };
          else delete th.status[key];
          m.step(DT); st2++; steps++;
          if (th.stun > 0) thStun++;
          if (me.stun > 0) meStun++;
          sep += Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
        }
        dealt += me.dealt;
      }
    }
    out.push({ level: lv, fired, parried, hit, walled, expired,
               parryRate: fired ? parried / fired : 0,
               hitRate: fired ? hit / fired : 0,
               thStun: steps ? thStun / steps : 0,
               meStun: steps ? meStun / steps : 0,
               sep: steps ? sep / steps : 0, steps, dealt });
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
    delete x.onHit; delete x.onSelf;
    if (saved[pid].onHit) x.onHit = saved[pid].onHit;
    if (saved[pid].onSelf) x.onSelf = saved[pid].onSelf;
  }
  return out;
}"""


# --------------------------------------------------------- [7] the traps ---

TRAP_JS = r"""([melee, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = {};

  /* (a) v39 open decision 4. `relicShot()` gates on mode; `tickFire` reads
     `f.w.shot` and never calls it. Asserted by DOING it: hang a shot block on
     a melee weapon and count what leaves the barrel. */
  const w = AC.WEAPONS.find(x => x.id === melee);
  const bow = AC.WEAPONS.find(x => x.mode === "ranged" && x.shot);
  out.melee = { id: w.id, mode: w.mode, hadShot: !!w.shot };
  const run = () => {
    const m = new AC.Match(melee, foe, seed);
    const me = m.a.w.id === melee ? m.a : m.b;
    let fired = 0;
    const oS = AC.Match.prototype.spawnShot;
    m.spawnShot = function(fg, a){ if (fg === me) fired++; return oS.call(m, fg, a); };
    let st = 0;
    while (!m.over && st < secs / DT){ m.step(DT); st++; }
    return { fired, dur: st * DT };
  };
  out.before = run();
  w.shot = JSON.parse(JSON.stringify(bow.shot));
  out.after = run();
  out.relicShotSays = null;
  delete w.shot;
  out.restored = !w.shot;

  /* (b) v39 §5.3. `step()` returns on hitStop BEFORE tickStatus, so every
     clock in tickStatus is frozen for the duration of the freeze. Asserted
     directly: hold a status, force the freeze, step, and read the clock. */
  const m2 = new AC.Match(melee, foe, seed);
  m2.step(DT);
  const t0 = 3.2;
  m2.b.status.smite = { stacks: 1, t: t0 };
  m2.hitStop = 0;
  m2.step(DT);
  const tFree = m2.b.status.smite.t;
  m2.b.status.smite.t = t0;
  m2.hitStop = 5.0;
  for (let i = 0; i < 10; i++) m2.step(DT);
  const tFrozen = m2.b.status.smite ? m2.b.status.smite.t : 0;
  out.clock = { dt: DT, afterOneFreeStep: t0 - tFree, afterTenFrozenSteps: t0 - tFrozen };
  return out;
}"""


# ------------------------------------------------ [2c] the arc, falsified --
# Ironhail's own comment states the type's thesis: "hits from anywhere, dies
# up close" -- "and the collapsing hall turns that into an arc for free."
# CONFIG.collapse starts at 15s and closes the walls in by up to 140. Nobody
# has ever checked whether the arc is real. Binned by time, and a bin only
# counts matches that were STILL RUNNING at the end of it, so the fights the
# archer was already winning cannot draw the curve on their own.

ARC_JS = r"""([shooter, foes, seeds, secs, pin, pinIds, binW]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena, R = AC.CONFIG.physics.ballR;
  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null,
                   onSelf: x.onSelf ? JSON.parse(JSON.stringify(x.onSelf)) : null };
    x.dmg = pin; if (x.ult) x.ult.charge = 1e9;
    delete x.onHit; delete x.onSelf;
  }
  const nb = Math.ceil(secs / binW);
  const B = Array.from({ length: nb }, () => ({
    fired: 0, hit: 0, parried: 0, walled: 0, melee: 0, dmgShot: 0, dmgMelee: 0,
    sep: 0, inset: 0, steps: 0, matches: 0, dealtBy: 0, taken: 0 }));

  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let bin = 0;
      let inShots = false; const pfx = [];
      const oFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, l, sz, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) pfx.push(x + "," + y);
        return oFx.call(m, x, y, col, n, spd, l, sz, dx, dy);
      };
      const oR = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const sh = m._cineShot, d0 = self.dealt;
        const r = oR.call(m, self, foe2, hx, hy, seg, mul, over);
        const dd = self.dealt - d0;
        if (self === me){
          if (sh){ sh._pHit = true; B[bin].dmgShot += dd; }
          else { B[bin].melee++; B[bin].dmgMelee += dd; }
        } else B[bin].taken += dd;
        return r;
      };
      const oSp = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, a){ if (fg === me) B[bin].fired++; return oSp.call(m, fg, a); };
      const oTk = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice(); pfx.length = 0; inShots = true;
        const r = oTk.call(m, dt); inShots = false;
        if (pre.length){
          const P = new Set(pfx), L = new Set(m.shots);
          const own = me === m.a ? "a" : "b";
          for (const q of pre){
            if (L.has(q) || q.own !== own) continue;
            if (P.has(q.x + "," + q.y)) B[bin].parried++;
            else if (q._pHit) B[bin].hit++;
            else B[bin].walled++;
          }
        }
        return r;
      };
      let steps = 0;
      const seen = new Set();
      while (!m.over && steps < secs / DT){
        bin = Math.min(nb - 1, Math.floor((steps * DT) / binW));
        if (!seen.has(bin)){ seen.add(bin); B[bin].matches++; }
        m.step(DT); steps++;
        B[bin].steps++;
        B[bin].sep += Math.hypot(me.x - th.x, me.y - th.y) - 2 * R;
        B[bin].inset += m.inset;
      }
    }
  }
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg; if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
    delete x.onHit; delete x.onSelf;
    if (saved[pid].onHit) x.onHit = saved[pid].onHit;
    if (saved[pid].onSelf) x.onSelf = saved[pid].onSelf;
  }
  return B;
}"""


# ------------------------------------- [5b] the pin that breaks one column --
# Every comparable number in this project pins damage so a harder-hitting
# relic cannot buy stacks by ending the fight sooner. Curse is the one status
# for which the pin IS the variable: `apply` subtracts `maxHpLoss` per
# APPLICATION, and hp only follows when maxHp is driven below it, so what
# curse delivers is decided by 13-per-hit against the weapon's own damage per
# hit. Pin the damage and you have pinned the answer.

CURSEPIN_JS = r"""([shooter, foes, seeds, secs, pins, pinIds]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === shooter);
  const savedW = { aff: w.aff, onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  const savedAll = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid);
    savedAll[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
  }
  const out = [];
  for (const pin of pins){
    for (const live of [true, false]){
      for (const pid of pinIds){
        const x = AC.WEAPONS.find(y => y.id === pid);
        x.dmg = pin > 0 ? pin : savedAll[pid].dmg;
        if (x.ult) x.ult.charge = 1e9;
      }
      w.aff = "umbral"; delete w.onHit; delete w.onSelf;
      if (live) w.onHit = { curse: 1 };
      let ttk = [], eaten = [], hp20 = [], hits = 0, dur = 0, n = 0;
      for (const f of foes) for (const sd of seeds){
        const m = new AC.Match(shooter, f, sd);
        const me = m.a.w.id === shooter ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        const hp0 = th.hp, mx0 = th.maxHp;
        let st = 0, k20 = -1;
        while (!m.over && st < secs / DT){
          m.step(DT); st++;
          if (k20 < 0 && st * DT >= 20) k20 = hp0 - th.hp;
        }
        if (!th.alive) ttk.push(st * DT);
        eaten.push(mx0 - th.maxHp); if (k20 >= 0) hp20.push(k20);
        hits += me.hits; dur += st * DT; n++;
      }
      out.push({ pin, live, n,
                 dmgPerHit: pin > 0 ? pin : w.dmg,
                 ttk: ttk.length ? ttk.reduce((a, b) => a + b, 0) / ttk.length : null,
                 killed: ttk.length / n,
                 eaten: eaten.reduce((a, b) => a + b, 0) / eaten.length,
                 hp20: hp20.length ? hp20.reduce((a, b) => a + b, 0) / hp20.length : null,
                 hps: hits / dur });
    }
  }
  w.aff = savedW.aff; delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(savedAll)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = savedAll[pid].dmg;
    if (savedAll[pid].ch !== null) x.ult.charge = savedAll[pid].ch;
  }
  return out;
}"""



def paired(live, dead, key, idx=None):
    """Paired per-(foe,seed) differences, mean and 95% half-width.

    The two arms share seeds and foes, so the row-wise difference is the
    statistic and its spread is the error bar. Reporting a mean without one is
    how this section's first cut turned RNG divergence into five findings.
    """
    d = []
    for l, x in zip(live, dead):
        a = l[key][idx] if idx is not None else l[key]
        b = x[key][idx] if idx is not None else x[key]
        if idx is not None and (a < 0 or b < 0):
            continue
        d.append(a - b)
    if not d:
        return 0.0, 0.0, 0
    m = statistics.mean(d)
    if len(d) < 2:
        return m, 0.0, len(d)
    return m, 1.96 * statistics.stdev(d) / (len(d) ** 0.5), len(d)


def mean(xs):
    xs = list(xs)
    return statistics.mean(xs) if xs else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=90.0)
    ap.add_argument("--pin", type=float, default=14.0)
    ap.add_argument("--zoom", type=int, default=6)
    ap.add_argument("--roster-seeds", type=int, default=3)
    ap.add_argument("--skip", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    skip = set(a.skip.split(",")) if a.skip else set()

    gp = (HERE / a.game).resolve()
    seeds = [101 + 7 * i for i in range(a.seeds)]
    rseeds = [101 + 7 * i for i in range(a.roster_seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        g = page.evaluate(GRID_JS)
        W, ST = g["weapons"], g["status"]
        by_id = {w["id"]: w for w in W}
        schools = sorted(set({w["aff"] for w in W}) | set(g["affinities"]))
        shapes = sorted({w["shape"] for w in W})
        filled = {(w["aff"], w["shape"]): w["name"] for w in W}
        bows = [w for w in W if w["shape"] == "bow"]
        open_bow = [s for s in schools if (s, "bow") not in filled]
        pin_ids = [w["id"] for w in W]

        # ------------------------------------------------------------ [1] --
        print(f"\n[1] THE BOW ROW — {len(W)} relics, {len(open_bow)} open bow cells\n")
        print(f"    {'':<12}" + "".join(f"{t[:10]:>12}" for t in shapes) + "    school")
        for s in schools:
            row = "".join(f"{filled.get((s,t),'·')[:11]:>12}" for t in shapes)
            print(f"    {s:<12}{row}    {sum(1 for t in shapes if (s,t) in filled)}/{len(shapes)}")
        print(f"    {'type':<12}" + "".join(
            f"{sum(1 for s in schools if (s,t) in filled):>12}" for t in shapes))
        print(f"\n    {'the three that exist':<24}{'aff':<12}{'dmg':>7}{'onHit/onSelf':>18}"
              f"{'cadence':>9}{'ult':>14}")
        for w in bows:
            ch = (f"{w['onHit'][0]}:{w['onHit'][1]}" if w["onHit"]
                  else f"self {w['onSelf'][0]}:{w['onSelf'][1]}" if w["onSelf"] else "—")
            print(f"    {w['name']:<24}{w['aff']:<12}{w['dmg']:>7.2f}{ch:>18}"
                  f"{w['shot']['cadence'] if w['shot'] else 0:>9.2f}"
                  f"{w['ult']['kind']:>14}")
        print(f"\n    OPEN: {', '.join(s + ' x bow' for s in open_bow)}")

        check("every bow shares one shot block — the shot is a property of the TYPE",
              len({json.dumps(w["shot"], sort_keys=True) for w in bows}) == 1,
              f"{len(bows)} bows, {len({json.dumps(w['shot'], sort_keys=True) for w in bows})} distinct shot blocks")
        check("the bow is the only ranged mode in the game",
              {w["shape"] for w in W if w["mode"] == "ranged"} == {"bow"},
              f"ranged: {sorted({w['id'] for w in W if w['mode'] == 'ranged'})}")
        check("the bow has the shortest reach in the game",
              min(w["reach"] for w in W) == bows[0]["reach"],
              f"bow {bows[0]['reach']}, next {sorted({w['reach'] for w in W})[:3]}")

        # ------------------------------------------------------- [2] control --
        if "control" not in skip:
            print("\n[2a] CONTROL — does the instrument move the simulation?\n")
            ctlFoe = next(w["id"] for w in W if w["shape"] == "greatsword")
            ctl = page.evaluate(CONTROL_JS, ["ironhail", ctlFoe, seeds[:4], 40.0])
            same = ctl["bare"] == ctl["inst"]
            check("wrapping resolveHit/spawnShot/spawnFx/tickShots changes nothing",
                  same,
                  "4 seeds, steps+hp+hits+shotHits field for field"
                  if same else f"bare {ctl['bare']}  inst {ctl['inst']}")

        # ------------------------------------------------------------ [2] --
        ranged = {}
        if "ranged" not in skip:
            print(f"\n[2] THE RANGED PATH, DECOMPOSED — ults suppressed, damage NOT pinned "
                  f"(this is what the three bows really do), {a.secs:.0f}s cap\n")
            mfoes = [w["id"] for w in W if w["shape"] != "bow"]
            print(f"    {'bow':<12}{'hits/s':>8}{'arrow':>8}{'stick':>8}"
                  f"{'dmg arrow':>11}{'landed':>8}{'parried':>9}{'wall':>7}"
                  f"{'spent':>7}{'live':>6}{'sep':>7}{'flight':>8}")
            for w in bows:
                rows = page.evaluate(RANGED_JS, [w["id"], mfoes, seeds, a.secs,
                                                 0, pin_ids, True, False])
                dur = sum(r["dur"] for r in rows)
                fired = sum(r["fired"] for r in rows)
                hs, hm = sum(r["hShot"] for r in rows), sum(r["hMelee"] for r in rows)
                ds, dm = sum(r["dShot"] for r in rows), sum(r["dMelee"] for r in rows)
                pa, wa = sum(r["parried"] for r in rows), sum(r["walled"] for r in rows)
                ex, ev = sum(r["expired"] for r in rows), sum(r["evicted"] for r in rows)
                hit = sum(r["hit"] for r in rows)
                unk = sum(r["unknown"] for r in rows)
                amb = sum(r["ambig"] for r in rows)
                lv = sum(r["live"] for r in rows)
                ranged[w["id"]] = dict(
                    n=len(rows), dur=dur, fired=fired, hit=hit, parried=pa, walled=wa,
                    expired=ex, evicted=ev, unknown=unk, ambig=amb, live=lv,
                    hShot=hs, hMelee=hm, dShot=ds, dMelee=dm,
                    hps=(hs + hm) / dur, meanLive=mean(r["meanLive"] for r in rows),
                    sep=mean(r["sep"] for r in rows), flight=mean(r["flight"] for r in rows),
                    hstop=mean(r["hstop"] for r in rows),
                    win=mean(r["win"] for r in rows if r["win"] >= 0),
                    over=sum(1 for r in rows if r["over"]) / len(rows))
                R = ranged[w["id"]]
                print(f"    {w['name']:<12}{R['hps']:>8.3f}{hs/(hs+hm):>8.0%}"
                      f"{hm/(hs+hm):>8.0%}{ds/(ds+dm):>11.0%}"
                      f"{hit/fired:>8.1%}{pa/fired:>9.1%}{wa/fired:>7.1%}"
                      f"{ex/fired:>7.1%}{R['meanLive']:>6.1f}"
                      f"{R['sep']:>7.0f}{R['flight']:>8.0f}")
            tot = {k: sum(R[k] for R in ranged.values())
                   for k in ("fired", "hit", "parried", "walled", "expired",
                             "evicted", "unknown", "live")}
            check("every arrow is accounted for — fired = landed + parried + wall "
                  "+ spent + evicted + still in flight",
                  tot["fired"] == (tot["hit"] + tot["parried"] + tot["walled"]
                                   + tot["expired"] + tot["evicted"] + tot["live"]),
                  f"{tot['fired']} fired, "
                  f"{tot['fired'] - (tot['hit']+tot['parried']+tot['walled']+tot['expired']+tot['evicted']+tot['live'])} unexplained")
            check("no arrow is classified by a sink this probe does not know about",
                  tot["unknown"] == 0, f"{tot['unknown']} unknown")
            amb = sum(R["ambig"] for R in ranged.values())
            # This is the justification for tagging the parry at its own effect
            # call instead of inferring it from "removed and not otherwise
            # explained": these are arrows batted out of the air ON or PAST the
            # wall line, which an inference would have filed as wall hits.
            check("the parry tag is worth having — inference would misfile some "
                  "parries as wall hits, and does not silently absorb new sinks",
                  amb / max(1, tot["parried"]) < 0.02,
                  f"{amb} of {tot['parried']} parries ({amb/max(1,tot['parried']):.1%}) "
                  f"were also past the wall line on the frame they were batted")

        # ------------------------------------------------------------ [3] --
        parry = {}
        if "parry" not in skip:
            print(f"\n[3] THE PARRY IS A PROPERTY OF THE FOE — one bow (Ironhail), "
                  f"every non-bow foe, {len(rseeds)} seeds.\n    Damage pinned "
                  f"{a.pin} and EVERY channel deleted, so the only thing that varies "
                  f"down this table is the foe's geometry.\n")
            mfoes = [w["id"] for w in W if w["shape"] != "bow"]
            rows = page.evaluate(RANGED_JS, ["ironhail", mfoes, rseeds, a.secs,
                                             a.pin, pin_ids, True, True])
            print(f"    {'foe':<14}{'shape':<12}{'reach':>6}{'width':>6}{'spin':>6}"
                  f"{'blades':>7}{'sweep':>8}   {'parried':>8}{'landed':>8}{'wall':>7}")
            agg = {}
            for r in rows:
                agg.setdefault(r["foe"], []).append(r)
            for fid, rs in sorted(agg.items(),
                                  key=lambda kv: -sum(r["parried"] for r in kv[1])
                                  / max(1, sum(r["fired"] for r in kv[1]))):
                fw = by_id[fid]
                fired = sum(r["fired"] for r in rs)
                pa = sum(r["parried"] for r in rs)
                hi = sum(r["hit"] for r in rs)
                wa = sum(r["walled"] for r in rs)
                # the area a spinning weapon sweeps per second, in blade-lengths
                sweep = fw["reach"] * fw["width"] * fw["spin"] * fw["blades"]
                parry[fid] = {"parry": pa / fired, "hit": hi / fired, "fired": fired,
                              "sweep": sweep, "shape": fw["shape"]}
                print(f"    {fw['name']:<14}{fw['shape']:<12}{fw['reach']:>6}"
                      f"{fw['width']:>6}{fw['spin']:>6.1f}{fw['blades']:>7}"
                      f"{sweep:>8.0f}   {pa/fired:>8.1%}{hi/fired:>8.1%}{wa/fired:>7.1%}")
            ps = [v["parry"] for v in parry.values()]
            print(f"\n    parry rate spread: {min(ps):.1%} — {max(ps):.1%} "
                  f"({max(ps)/max(1e-9,min(ps)):.1f}x)")
            check("the parry rate is not a constant of the type — the foe's weapon "
                  "decides it", max(ps) - min(ps) > 0.05,
                  f"{min(ps):.1%} to {max(ps):.1%} across {len(parry)} foes")
            # Damage is pinned and every channel deleted in this pass, so two
            # relics of the same shape are the SAME WEAPON. Identical rows are
            # therefore the correct answer and a difference would be a per-relic
            # field reaching the shot path that nothing in the tree documents.
            byshape = {}
            for fid, v in parry.items():
                byshape.setdefault(v["shape"], set()).add(round(v["parry"], 9))
            dup = {k: v for k, v in byshape.items() if len(v) > 1}
            check("with damage pinned and every channel deleted, two relics of one "
                  "shape parry IDENTICALLY — nothing per-relic reaches the shot path",
                  not dup,
                  ", ".join(f"{k}: {sorted(v)}" for k, v in dup.items())
                  or f"{len(byshape)} shapes, one rate each")

        # ----------------------------------------------------------- [3b] --
        arc = []
        if "arc" not in skip:
            print(f"\n[3b] THE ARC — the type's own thesis, tested. Ironhail's comment: "
                  f"\"hits from\n     anywhere, dies up close ... the collapsing hall "
                  f"turns that into an arc for free.\"\n     Collapse starts at "
                  f"{g['arena'] and 15}s. Damage pinned, channels deleted, 10s bins; a bin "
                  f"counts\n     only matches still running at the end of it.\n")
            afoes = [w["id"] for w in W if w["shape"] != "bow"]
            arc = page.evaluate(ARC_JS, ["ironhail", afoes, rseeds, a.secs,
                                         a.pin, pin_ids, 10.0])
            print(f"    {'bin':<10}{'matches':>8}{'fired':>7}{'landed':>8}{'parried':>9}"
                  f"{'wall':>7}{'melee/s':>9}{'shot dmg':>10}{'sep':>7}{'inset':>7}")
            for i, b in enumerate(arc):
                if not b["steps"]:
                    continue
                f_ = max(1, b["fired"])
                dtot = max(1e-9, b["dmgShot"] + b["dmgMelee"])
                secsb = b["steps"] * g["dt"]
                print(f"    {f'{i*10}-{i*10+10}s':<10}{b['matches']:>8}{b['fired']:>7}"
                      f"{b['hit']/f_:>8.1%}{b['parried']/f_:>9.1%}{b['walled']/f_:>7.1%}"
                      f"{b['melee']/secsb:>9.3f}{b['dmgShot']/dtot:>10.0%}"
                      f"{b['sep']/b['steps']:>7.0f}{b['inset']/b['steps']:>7.0f}")
            live = [b for b in arc if b["steps"] and b["fired"] > 200]
            if len(live) >= 3:
                first, last = live[0], live[-1]
                lr0 = first["hit"] / first["fired"]
                lr1 = last["hit"] / last["fired"]
                sh0 = first["dmgShot"] / max(1e-9, first["dmgShot"] + first["dmgMelee"])
                sh1 = last["dmgShot"] / max(1e-9, last["dmgShot"] + last["dmgMelee"])
                print(f"\n    landed rate {lr0:.1%} -> {lr1:.1%}   "
                      f"arrow's share of damage {sh0:.0%} -> {sh1:.0%}   "
                      f"separation {first['sep']/first['steps']:.0f} -> "
                      f"{last['sep']/last['steps']:.0f}")
                verdict = "REAL" if sh1 < sh0 - 0.05 else "REFUTED"
                print(f"\n    VERDICT ON THE TYPE'S OWN THESIS: {verdict}. The arrow "
                      f"carries {sh0:.0%} of the damage\n    in the opening bin and "
                      f"{sh1:.0%} in the last, with the walls in "
                      f"{last['inset']/last['steps']:.0f}.")
                check("the arc measurement has the resolution to see an arc if there "
                      "were one — every bin carries enough arrows to separate 5%",
                      min(b["fired"] for b in live) > 200,
                      f"smallest bin {min(b['fired'] for b in live)} arrows over "
                      f"{len(live)} bins")

        # ------------------------------------------------------------ [4] --
        art = {}
        if "art" not in skip:
            print("\n[4] THE ART — palette HELD, only p.key varies, so a differing "
                  "pixel is the dispatch\n")
            rep = bows[0]
            D, aw = rep["reach"], rep["artW"]
            keys = schools + [None]

            def pair(M, x, y):
                return M.get(f"{x}|{y}") or M[f"{y}|{x}"]

            for kdraw, label in ((0.55, "drawn 0.55"), (0.0, "undrawn")):
                S, cx, tries, clipped = int(D * 1.6), 0.5, 0, True
                while True:
                    r = page.evaluate(INK_JS, [keys, D, aw, a.zoom, S, cx, kdraw])
                    bx = list(r["boxes"].values())
                    clipped = any(b[0] <= 0 or b[1] <= 0 or b[2] >= r["w"] - 1
                                  or b[3] >= r["h"] - 1 for b in bx)
                    if not clipped or tries >= 4:
                        break
                    if any(b[0] <= 0 for b in bx):
                        cx = min(0.82, cx + 0.13)
                    S = int(S * 1.45); tries += 1
                M = r["m"]
                pairs = [(x, y, pair(M, x, y)["diff"], pair(M, x, y)["iou"])
                         for i, x in enumerate(schools) for y in schools[i + 1:]]
                vsneg = {s: pair(M, s, "NEG")["diff"] for s in schools}
                art[label] = {"pairs": pairs, "vsNeg": vsneg, "det": r["rerun"],
                              "fit": not clipped, "S": S, "cx": cx,
                              "inks": r["inks"], "w": r["w"], "h": r["h"]}
                print(f"    {label:<12}  {S}px canvas, fit={'y' if not clipped else 'N'}"
                      f"   rerun={r['rerun']:.0e}   pair diff mean "
                      f"{mean(d for _, _, d, _ in pairs):.1%}"
                      f"   min {min(d for _, _, d, _ in pairs):.1%}")

            check("the render is deterministic — same key twice is the same pixels",
                  all(v["det"] < 1e-9 for v in art.values()),
                  f"max {max(v['det'] for v in art.values()):.1e}")
            check("no bow is measured clipped — `_artBox` lies about a bow and "
                  "v39 measured a cropped one",
                  all(v["fit"] for v in art.values()),
                  ", ".join(k for k, v in art.items() if not v["fit"]) or "both draw states")
            check("the comparator is sensitive — a nonsense key differs from every "
                  "real school",
                  all(min(v["vsNeg"].values()) > 0.002 for v in art.values()),
                  f"smallest {min(min(v['vsNeg'].values()) for v in art.values()):.1%}")

            base = art["drawn 0.55"]
            print(f"\n    {'open cell':<18}{'nearest sibling':<16}{'diff':>7}{'inkIoU':>8}"
                  f"{'ink px':>9}   rank on the type")
            allp = sorted(d for _, _, d, _ in base["pairs"])
            for s in open_bow:
                sibs = [(o, d, i) for x, y, d, i in base["pairs"]
                        for o in ([y] if x == s else [x] if y == s else [])]
                near = min(sibs, key=lambda q: q[1])
                rank = sum(1 for v in allp if v < near[1]) + 1
                art.setdefault("cells", {})[s] = {"near": near[0], "diff": near[1],
                                                  "iou": near[2], "rank": rank}
                print(f"    {s + ' x bow':<18}{near[0]:<16}{near[1]:>7.1%}"
                      f"{near[2]:>8.3f}{base['inks'][s]:>9}   "
                      f"closest pair #{rank} of {len(allp)}")
            check("every open bow cell has art that differs from every sibling",
                  all(art["cells"][s]["diff"] > 0.05 for s in open_bow),
                  f"min {min(art['cells'][s]['diff'] for s in open_bow):.1%}")
            print("\n    NOTE: every one of those four is nearest to DWARVEN, and that "
                  "is not\n    four coincidences — the dwarven branch is the smallest "
                  "ornament on the\n    shape (v39: 0.12% of coverage), so it sits "
                  "closest to the bare recurve\n    that all seven share. This column "
                  "reads HOW MUCH the branch adds. It is\n    not a confusability "
                  "score: at arena size two relics collide by PALETTE,\n    and that "
                  "is a count, not a render —\n")
            print(f"    {'open cell':<18}{'same-school relics it would stand beside':<44}"
                  f"{'mirror pairs':>13}")
            for s in open_bow:
                sibs = [w["name"] for w in W if w["aff"] == s]
                print(f"    {s + ' x bow':<18}{(', '.join(sibs) or '—'):<44}"
                      f"{len(sibs):>13}")

        # ------------------------------------------------------------ [5] --
        clock = {}
        if "clock" not in skip:
            print(f"\n[5] THE CLOCK ON THE BOW — each school's channel carried on "
                  f"Ironhail's body, damage pinned {a.pin}, ults suppressed\n")
            cfoes = [w["id"] for w in W if w["shape"] != "bow"][:5]
            chan = {}
            for s in schools:
                rel = [w for w in W if w["aff"] == s]
                hits = [w["onHit"] for w in rel if w["onHit"]]
                chan[s] = hits[0] if hits else None
            order = open_bow + [s for s in schools if (s, "bow") in filled]
            print(f"    {'':<3}{'school x bow':<20}{'status':<11}{'hits/s':>8}"
                  f"{'mean':>6}{'>=2':>6}{'cap':>6}{'capAt':>7}"
                  f"{'hp@20s':>8}{'net (95%)':>11}{'net%':>7}{'ttk':>7}{'dTtk':>7}")
            deadArms = {}
            for s in order:
                if not chan[s]:
                    print(f"    {'':<3}{s + ' x bow':<20}{'— no onHit channel —':<11}")
                    continue
                k, per = chan[s]
                use = [f for f in cfoes if f != "ironhail"]
                live = page.evaluate(CLOCK_JS, ["ironhail", s, k, per, use, seeds,
                                                a.pin, pin_ids, a.secs, True])
                dead = page.evaluate(CLOCK_JS, ["ironhail", s, k, per, use, seeds,
                                                a.pin, pin_ids, a.secs, False])
                durL = sum(r["dur"] for r in live)
                durD = sum(r["dur"] for r in dead)
                deadArms[s] = [(r["foe"], r["seed"], round(r["dur"], 9),
                                round(r["hpLost"], 6), r["hits"]) for r in dead]
                # FIXED WINDOW: only rows where BOTH arms were still running at
                # 20s, paired by (foe, seed). hp/s over a whole fight rewards a
                # channel for ending the fight, which is the confound below.
                pairs20 = [(l["ckHp"][1], d["ckHp"][1])
                           for l, d in zip(live, dead)
                           if l["ckHp"][1] >= 0 and d["ckHp"][1] >= 0]
                w20L = mean(x for x, _ in pairs20) if pairs20 else 0
                w20D = mean(y for _, y in pairs20) if pairs20 else 0
                ttkL = [r["ttk"] for r in live if r["ttk"] > 0]
                ttkD = [r["ttk"] for r in dead if r["ttk"] > 0]
                hpsL = sum(r["hpLost"] for r in live) / durL
                hpsD = sum(r["hpLost"] for r in dead) / durD
                capAt = [r["capAt"] for r in live if r["capAt"] > 0]
                mark = "->" if (s, "bow") not in filled else "  "
                clock[s] = dict(
                    status=k, per=per, n=len(live),
                    hps=sum(r["hits"] for r in live) / durL,
                    mean=mean(r["meanStacks"] for r in live),
                    p2=mean(r["p2"] for r in live), pMax=mean(r["pMax"] for r in live),
                    capAt=mean(capAt) if capAt else None,
                    capReached=len(capAt) / len(live),
                    hpsLive=hpsL, hpsDead=hpsD,
                    w20=w20L, w20base=w20D, n20=len(pairs20),
                    net=w20L - w20D, netPct=(w20L - w20D) / w20D if w20D else 0,
                    netCI=paired(live, dead, "ckHp", 1)[1],
                    takeCI=paired(live, dead, "ckMe", 1)[1],
                    thHitCI=paired(live, dead, "ckThHit", 1)[1],
                    ttk=mean(ttkL) if ttkL else None, ttkBase=mean(ttkD) if ttkD else None,
                    killed=len(ttkL) / len(live), killedBase=len(ttkD) / len(dead),
                    lockLive=mean(r["lock"] for r in live),
                    lockDead=mean(r["lock"] for r in dead),
                    fires=sum(r["fires"] for r in live) / durL,
                    dot=sum(r["dot"] for r in live) / durL,
                    maxHpEaten=mean(r["maxHpEaten"] for r in live),
                    entSpin=mean(r["entSpin"] for r in live),
                    entMove=mean(r["entMove"] for r in live),
                    take=mean(l["ckMe"][1] for l, d in zip(live, dead)
                              if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    takeBase=mean(d["ckMe"][1] for l, d in zip(live, dead)
                                  if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    thHit=mean(l["ckThHit"][1] for l, d in zip(live, dead)
                               if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    thHitBase=mean(d["ckThHit"][1] for l, d in zip(live, dead)
                                   if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    thDesp=mean(l["ckThDesp"][1] for l, d in zip(live, dead)
                                if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    thDespBase=mean(d["ckThDesp"][1] for l, d in zip(live, dead)
                                    if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0),
                    **{f"w{n2}{arm}": mean(r[f"ck{n2}"][1] for l, d in zip(live, dead)
                                           if l["ckMe"][1] >= 0 and d["ckMe"][1] >= 0
                                           for r in [l if arm == "L" else d])
                       for n2 in ("Hit", "Sep", "Froz", "ThStun") for arm in ("L", "D")},
                    ramp=[mean(d["ckHit"][i] for d in dead if d["ckHit"][i] >= 0)
                          for i in range(3)],
                    parryLive=mean(r["parryRate"] for r in live),
                    parryDead=mean(r["parryRate"] for r in dead),
                    frozen=mean(r["frozen"] for r in live),
                    winLive=mean(r["win"] for r in live if r["win"] >= 0),
                    winDead=mean(r["win"] for r in dead if r["win"] >= 0),
                    overLive=sum(1 for r in live if r["over"]) / len(live))
                C = clock[s]
                capTxt = f"{C['capAt']:.0f}s" if C["capAt"] else "—"
                ttkTxt = f"{C['ttk']:.0f}s" if C["ttk"] else "—"
                dTtk = (f"{C['ttk'] - C['ttkBase']:+.0f}s"
                        if C["ttk"] and C["ttkBase"] else "—")
                netTxt = f"{C['net']:+.0f}±{C['netCI']:.0f}"
                print(f"    {mark:<3}{s + ' x bow':<20}{k:<11}{C['hps']:>8.3f}"
                      f"{C['mean']:>6.2f}{C['p2']:>6.0%}{C['pMax']:>6.0%}"
                      f"{capTxt:>7}"
                      f"{C['w20']:>8.0f}{netTxt:>11}{C['netPct']:>7.0%}"
                      f"{ttkTxt:>7}{dTtk:>7}")
            ident = len({json.dumps(v) for v in deadArms.values()}) == 1
            check("the A/B baseline is one weapon — with the channel deleted, the "
                  "school string is cosmetic and every arm is identical",
                  ident,
                  f"{len(deadArms)} channel-deleted arms, "
                  f"{len({json.dumps(v) for v in deadArms.values()})} distinct")

            print(f"\n    the delivered effect — one readout per KIND of status, "
                  f"because they are not the same kind of object\n")
            for s in order:
                if s not in clock:
                    continue
                C = clock[s]
                k = C["status"]
                if k in ("hemorrhage", "smite"):
                    what = (f"dot {C['dot']:.2f} hp/s of the {C['net']:.2f} net "
                            f"({C['dot']/max(1e-9,C['net']):.0%} of it)")
                elif k == "hex":
                    what = (f"{C['fires']:.2f} locks/s, foe weapon shut "
                            f"{C['lockLive']:.1%} vs {C['lockDead']:.1%} without "
                            f"= {C['lockLive']-C['lockDead']:+.1%}")
                elif k == "curse":
                    what = (f"{C['maxHpEaten']:.0f} max hp eaten a fight, cap "
                            f"reached in {C['capReached']:.0%} of them")
                elif k == "entangle":
                    what = (f"foe spin -{C['entSpin']:.1%}, move -{C['entMove']:.1%} "
                            f"time-weighted; foe parries {C['parryLive']:.1%} vs "
                            f"{C['parryDead']:.1%} without = "
                            f"{C['parryLive']-C['parryDead']:+.1%}")
                elif k == "sunder":
                    what = f"damage taken x{1 + ST['sunder']['taken']*C['mean']:.2f} mean"
                else:
                    what = "—"
                print(f"    {'->' if (s,'bow') not in filled else '  '} "
                      f"{s + ' x bow':<20}{k:<11}{what}")

            print(f"\n    THE OTHER HALF OF THE LEDGER — the same 20s window, "
                  f"measured on the ARCHER\n")
            print(f"    {'':<3}{'school x bow':<20}{'took@20s':>9}{'base':>7}"
                  f"{'extra (95%)':>13}{'foe hits':>10}{'base':>7}{'foe <25%':>10}")
            for s2 in order:
                if s2 not in clock:
                    continue
                C = clock[s2]
                ex = C["take"] - C["takeBase"]
                real = abs(ex) > C["takeCI"]
                exTxt = f"{ex:+.0f}±{C['takeCI']:.0f}"
                note = "" if real else "inside the error bar"
                print(f"    {'->' if (s2,'bow') not in filled else '  ':<3}"
                      f"{s2 + ' x bow':<20}{C['take']:>9.0f}{C['takeBase']:>7.0f}"
                      f"{exTxt:>13}"
                      f"{C['thHit']:>10.1f}{C['thHitBase']:>7.1f}"
                      f"{C['thDesp']:>10.0%}   {note}")
            print(f"\n    ONLY THE TWO DOT CHANNELS COST THE ARCHER ANYTHING, and "
                  f"finding that out cost\n    this section a retraction. At 5 seeds "
                  f"ALL FIVE live arms took 12-23 more and it\n    read as a law about "
                  f"offensive channels on a bow. At 20 it is hemorrhage and\n    smite "
                  f"alone; hex, entangle and sunder fall inside the error bar. The "
                  f"error bar\n    is now printed for exactly that reason.\n\n"
                  f"    DESPERATION IS NOT THE REASON EITHER: it fires at 25% and the "
                  f"foe is under it\n    for 0-2% of the window in every arm. The "
                  f"contact columns:\n")
            print(f"    {'':<3}{'school x bow':<20}{'archer hits':>12}{'base':>7}"
                  f"{'foe hits':>10}{'base':>7}{'sep':>7}{'base':>7}"
                  f"{'frozen':>8}{'base':>7}")
            for s2 in order:
                if s2 not in clock:
                    continue
                C = clock[s2]
                print(f"    {'->' if (s2,'bow') not in filled else '  ':<3}"
                      f"{s2 + ' x bow':<20}{C['wHitL']:>12.1f}{C['wHitD']:>7.1f}"
                      f"{C['thHit']:>10.1f}{C['thHitBase']:>7.1f}"
                      f"{C['wSepL']:>7.0f}{C['wSepD']:>7.0f}"
                      f"{C['wFrozL']:>8.1%}{C['wFrozD']:>7.1%}")
            print(f"\n    CURSE IS THE CONTROL THAT MAKES THIS READABLE. At this pin it "
                  f"changes nothing\n    inside 20s — every column above is base to the "
                  f"digit — so the movement in the\n    other four rows is the channel "
                  f"and not the seed. WHAT the channels do to\n    contact is NOT "
                  f"established here and should not be asserted: it is an open\n    "
                  f"question, and it is worth one, because it is a tax on every "
                  f"offensive\n    channel a bow could carry.")
            worse = [(s2, clock[s2]) for s2 in order if s2 in clock
                     and clock[s2]["takeBase"] - clock[s2]["take"] < -5]
            check("desperation is REFUTED as the explanation — the foe is barely ever "
                  "under 25% inside the window",
                  all(C["thDesp"] < 0.05 for _, C in worse),
                  "; ".join(f"{s2}: foe desperate {C['thDesp']:.0%} of the window, "
                            f"took {C['take']-C['takeBase']:+.0f}" for s2, C in worse))
            cz = clock.get("umbral")
            if cz:
                check("curse is the null control it needs to be — at this pin it moves "
                      "no column inside the window",
                      abs(cz["take"] - cz["takeBase"]) < 0.51
                      and abs(cz["thHit"] - cz["thHitBase"]) < 0.05,
                      f"took {cz['take']:.1f} vs {cz['takeBase']:.1f}, "
                      f"foe hits {cz['thHit']:.2f} vs {cz['thHitBase']:.2f}")

            rmp = clock[order[0]]["ramp"]
            if all(x > 0 for x in rmp):
                print(f"\n    WHY THE WINDOW AND NOT hp/s. A REFUTED GUESS FIRST: the "
                      f"first cut of this\n    section assumed contact was BACK-LOADED "
                      f"(the hall collapses from 15s, so the\n    archer should hit "
                      f"more late). It does not. Channel-deleted baseline:\n")
                print(f"      hits  0-10s {rmp[0]:.1f}   10-20s {rmp[1]-rmp[0]:.1f}   "
                      f"20-30s {rmp[2]-rmp[1]:.1f}   — flat, and the guess is dead")
                print(f"\n    The real reason is a CEILING. Over a whole fight the "
                      f"foe's pool is fixed, so\n    hp/s is very nearly hp0/ttk, and "
                      f"once a channel is strong enough to kill,\n    everything extra "
                      f"shows up only as a shorter fight — which compresses it:")
                for s3 in order:
                    if s3 not in clock:
                        continue
                    C3 = clock[s3]
                    wf = (C3["hpsLive"] - C3["hpsDead"]) / max(1e-9, C3["hpsDead"])
                    print(f"      {s3 + ' x bow':<20}{'window':>8} {C3['netPct']:>+6.0%}"
                          f"    {'whole fight':>12} {wf:>+6.0%}")
                comp = [(clock[x]["netPct"],
                         (clock[x]["hpsLive"] - clock[x]["hpsDead"]) / max(1e-9, clock[x]["hpsDead"]))
                        for x in order if x in clock and clock[x]["netPct"] > 0.10]
                check("whole-fight hp/s compresses a strong channel and a fixed window "
                      "does not — this is why every net above is windowed",
                      all(abs(wf) < abs(w2) for w2, wf in comp) and len(comp) >= 2,
                      "; ".join(f"{w2:+.0%} windowed vs {wf:+.0%} whole-fight"
                                for w2, wf in comp))

            if "cursepin" not in skip:
                print(f"\n[5b] THE PIN THAT BREAKS ONE COLUMN. `apply` subtracts 13 max "
                      f"hp per\n     APPLICATION of curse, and hp only follows when maxHp "
                      f"is driven under it. So\n     what curse delivers is 13 against "
                      f"the weapon's OWN damage per hit — and the\n     pin that makes "
                      f"every other row comparable is the one number curse's row is\n"
                      f"     entirely about.\n")
                cfo = [w["id"] for w in W if w["shape"] != "bow"][:5]
                cp = page.evaluate(CURSEPIN_JS, ["ironhail", cfo, seeds, a.secs,
                                                 [8, 14, 20, 28, 0], pin_ids])
                out["cursepin"] = cp
                print(f"    {'dmg/hit':>9}{'13 : dmg':>10}{'maxhp eaten':>13}"
                      f"{'hp@20s':>9}{'base':>7}{'net':>7}{'ttk':>7}{'base':>7}{'dTtk':>7}")
                for i in range(0, len(cp), 2):
                    L, D = cp[i], cp[i + 1]
                    lab = f"{L['dmgPerHit']:.1f}" + ("*" if L["pin"] == 0 else "")
                    dt_ = (f"{L['ttk'] - D['ttk']:+.0f}s" if L["ttk"] and D["ttk"] else "—")
                    tL = f"{L['ttk']:.0f}s" if L["ttk"] else "—"
                    tD = f"{D['ttk']:.0f}s" if D["ttk"] else "—"
                    print(f"    {lab:>9}{13/max(1e-9,L['dmgPerHit']):>10.2f}"
                          f"{L['eaten']:>13.0f}"
                          f"{(L['hp20'] or 0):>9.0f}{(D['hp20'] or 0):>7.0f}"
                          f"{(L['hp20'] or 0)-(D['hp20'] or 0):>7.0f}"
                          f"{tL:>7}{tD:>7}{dt_:>7}")
                print(f"    * unpinned — the real roster damage")
                gains = [((cp[i]['hp20'] or 0) - (cp[i+1]['hp20'] or 0))
                         for i in range(0, len(cp), 2)]
                check("curse's whole value is decided by the damage pin, so its row in "
                      "any pinned table is a statement about the pin",
                      max(gains) - min(gains) > 15,
                      "net hp at 20s across the pins: "
                      + ", ".join(f"{x:+.0f}" for x in gains))

            bowhex = clock.get("runic", {})
            if bowhex:
                print(f"\n    cross-check against v39 cell_survey's hex x bow row "
                      f"(0.352 hits/s, 35% >=2, lock 31.1%, net +17.7%):")
                print(f"      here: {bowhex['hps']:.3f} hits/s, "
                      f"{bowhex['p2']:.0%} >=2, lock {bowhex['lockLive']:.1%}, "
                      f"net {bowhex['netPct']:+.1%}")
                check("this instrument agrees with v39's on the one row they share",
                      abs(bowhex["p2"] - 0.35) < 0.10 and abs(bowhex["hps"] - 0.352) < 0.12,
                      f"{bowhex['hps']:.3f} vs 0.352 hits/s, {bowhex['p2']:.0%} vs 35%"
                      " — different foe set and secs, so agreement is the point, "
                      "not identity")

        # ------------------------------------------------------------ [6] --
        loop = {}
        if "loop" not in skip:
            print(f"\n[6] THE FEEDBACK LOOP — stacks PINNED on the foe, not earned. "
                  f"Ironhail shoots, the foe carries N stacks of one status.\n")
            lfoes = [w["id"] for w in W if w["shape"] != "bow"][:5]
            for k, why in (("entangle", "slows spin 13%/stack — spin is what parries"),
                           ("hex", "stuns — a stunned fighter has NO blade segments"),
                           ("curse", "NULL CONTROL: touches neither spin nor stun"),
                           ("hemorrhage", "NULL CONTROL: pure damage rate")):
                lv = list(range(0, ST[k]["maxStacks"] + 1))
                rows = page.evaluate(LOOP_JS, ["ironhail", lfoes, rseeds, a.secs,
                                               a.pin, pin_ids, k, lv])
                loop[k] = rows
                base = rows[0]
                print(f"    {k} — {why}")
                print(f"      {'stacks':>7}{'fired':>8}{'parried':>9}{'landed':>8}"
                      f"{'wall':>7}{'foe stun':>9}{'sep':>7}   vs 0 stacks")
                for r in rows:
                    dp = r["parryRate"] - base["parryRate"]
                    dh = r["hitRate"] - base["hitRate"]
                    print(f"      {r['level']:>7}{r['fired']:>8}{r['parryRate']:>9.1%}"
                          f"{r['hitRate']:>8.1%}{r['walled']/max(1,r['fired']):>7.1%}"
                          f"{r['thStun']:>9.1%}{r['sep']:>7.0f}   "
                          f"parry {dp:+.1%}  landed {dh:+.1%}")
                print()

            def slope(k):
                r = loop[k]
                return r[-1]["parryRate"] - r[0]["parryRate"]

            # THE CHECKS TEST THE INSTRUMENT. The hypotheses are reported as
            # verdicts underneath, because a probe that fails when a guess is
            # wrong is a probe nobody will run twice.
            check("the loop table has a working POSITIVE control — hex, which really "
                  "does empty the foe's blade list, moves the parry",
                  slope("hex") < -0.02,
                  f"parry {loop['hex'][0]['parryRate']:.1%} -> "
                  f"{loop['hex'][-1]['parryRate']:.1%} ({slope('hex'):+.1%}) "
                  f"as foe stun goes {loop['hex'][0]['thStun']:.0%} -> "
                  f"{loop['hex'][-1]['thStun']:.0%}")
            check("the loop table has working NULL controls — curse and hemorrhage "
                  "touch neither spin nor stun and do not move the parry",
                  abs(slope("curse")) < 0.02 and abs(slope("hemorrhage")) < 0.02,
                  f"curse {slope('curse'):+.1%}, hemorrhage {slope('hemorrhage'):+.1%}")
            print("    THE TWO VERDICTS THIS TABLE WAS BUILT TO REACH\n")
            ent, hx = slope("entangle"), slope("hex")
            entL, hxL = loop["entangle"][-1], loop["hex"][-1]
            e0, h0 = loop["entangle"][0], loop["hex"][0]
            print(f"      ENTANGLE -> PARRY: {'REAL' if ent < -0.02 else 'REFUTED'}. "
                  f"A full {entL['level']} stacks is a 52% cut to the foe's spin and "
                  f"moves\n        the parry {ent:+.1%} and the landed rate "
                  f"{entL['hitRate']-e0['hitRate']:+.1%}. The parry is not "
                  f"spin-limited:\n        the blade OCCUPIES the space whether it is "
                  f"turning fast or slow, and an arrow\n        crossing that space is "
                  f"caught either way.")
            print(f"      HEX -> PARRY: {'REAL' if hx < -0.02 else 'REFUTED'}. "
                  f"{hxL['level']} stacks holds the foe stunned "
                  f"{hxL['thStun']:.0%} of the fight and the parry\n        falls "
                  f"{h0['parryRate']:.1%} -> {hxL['parryRate']:.1%}. But the landed "
                  f"rate only moves {hxL['hitRate']-h0['hitRate']:+.1%}:\n        an "
                  f"arrow that is not batted down mostly goes on to hit the WALL. "
                  f"Suppressing\n        the parry is worth about a tenth of what "
                  f"suppressing the wall would be.\n")

        # ------------------------------------------------------------ [7] --
        if "traps" not in skip:
            print("\n[7] THE TRAPS v39 LEFT — asserted, not assumed\n")
            gs = [w["id"] for w in W if w["shape"] == "greatsword"]
            tr = page.evaluate(TRAP_JS, [gs[0], gs[1], 4242, 30.0])
            print(f"    (a) a `shot` block on a MELEE weapon: "
                  f"{tr['before']['fired']} arrows before, "
                  f"{tr['after']['fired']} after, over {tr['after']['dur']:.0f}s")
            check("v39 open decision 4 is still open — tickFire gates on `f.w.shot`, "
                  "not on mode",
                  tr["before"]["fired"] == 0 and tr["after"]["fired"] > 0,
                  f"a melee greatsword fired {tr['after']['fired']} arrows")
            check("the trap probe put the roster back",
                  tr["restored"], "no `shot` left on the melee weapon")
            c = tr["clock"]
            print(f"    (b) a status clock over one FREE step: "
                  f"-{c['afterOneFreeStep']:.5f}s (dt={c['dt']:.5f})   "
                  f"over ten FROZEN steps: -{c['afterTenFrozenSteps']:.5f}s")
            check("v39 §5.3 confirmed — hitStop freezes every clock in tickStatus",
                  abs(c["afterOneFreeStep"] - c["dt"]) < 1e-9
                  and c["afterTenFrozenSteps"] == 0,
                  "one free step costs exactly dt, ten frozen steps cost nothing")
            if ranged:
                hs = mean(R["hstop"] for R in ranged.values())
                print(f"    ... and a bow fight is frozen {hs:.1%} of its steps, "
                      f"so that much of every clock above is bought and not spent")

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))

    out = {"openBow": open_bow, "ranged": ranged, "parry": parry,
           "art": {k: v for k, v in art.items() if k == "cells"},
           "clock": clock,
           "loop": {k: [dict(r) for r in v] for k, v in loop.items()}}
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1, default=str))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
