#!/usr/bin/env python
"""QUARRELSTORM'S PROBE (the hail, v83) -- one check per sentence of v83 §1 / §4,
read INSIDE the hooks.

    python ironhail_probe.py --game <sc-ironhail-hail.html | -sunder | -b<X>>

Wraps `tickHail`, `fireUlt`, `tickWeapon`, `tickFire`, `resolveHit` and `step`
on the Match prototype and reads each event where it happens. Runs Ironhail
against every other relic, both sides, and prints N/N. The checks follow the
link's own numbers, so the same probe gates stages 2, 3 and 5 (sunder 0 / 1).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration iron falls": a window whose clock does not advance by
      exactly dt a call, that closes before `dur` on the window clock or
      outlives it or either death; `tickHail` not asked exactly once on every
      unfrozen step, or asked on a frozen one (the step wrapper counts the
      calls: dt a call is only the window clock if the calls are one a step --
      the second v108 review's mutant ticked the hail twice a step, a 4.6s
      window, and passed the per-call checks); any relic but Ironhail
      carrying `ultHail` or a bolt in `m.hail`
  [2] "every 0.4s a bolt drops ... onto where the enemy is": a window frame
      whose drop is not exactly the rebuilt cooldown's (cd - dt <= 0, then cd
      = dropCd), a bolt not at the foe's (x, y) of that frame, no bolt on the
      cast frame, or a bolt from a closed window
  [3] "and lands a moment later": a bolt whose fall does not advance by dt a
      call, or that resolves on any call but the one its fall reaches fallT
      (after the window closed as before it). At 0.4 / 0.3 no bolt is ever in
      the air at a clock close, so a second pass (16 fights, in no tally)
      closes one window a fight by its clock on the frame after a drop and
      watches that bolt land ("drops in the air ... still land")
  [4] "an enemy still standing there when it lands is struck": a landing
      without a live foe within hitR + R of the spot, a live foe inside it
      that was not struck, or a strike that is not exactly one
      hurt(foe, dropDmg, the caster); a hail call whose hurts are not
      exactly its landings' [foe, dropDmg, caster], in order (a hurt on
      the caster or anybody else -- v83 6.3: the hail does not strike its
      caster); or any fighter's hp, ward or ward pool after the call that is
      not the one rebuilt from the call's landings with hurt()'s own
      arithmetic (the ward first, then hp; a ward that breaks bursts the
      caster, if alive, for Math.round(pool x STATUS.ward.shatter)). "hurt(foe,
      4, f) ... and nothing else" -- the third v108 review's mutants took
      a point more off the foe outside hurt(), and struck the caster, and
      passed a probe that read who was hurt but never anybody's hp
  [5] "and sundered": a landing without exactly one apply("sunder", sunder,
      side letter) on the foe (none at sunder 0), or any on a miss; a hail
      call whose sunder applications are not exactly its landings'
      [foe, sunder, side letter] (a sunder on the caster is a fail here, not
      an "other status")
  [6] "nothing else" (§4: no crit, no knock, no stop, no rng): a hail call
      that moves anybody, stops the world (a ward's own shatter aside),
      draws the rng, spawns a shot or applies any other status
  [7] a killing landing without exactly one fatal hit beat marked `hail`, or
      one that does not say the kill: kind "hit", the caster's side (0 for
      "a", 1 for "b"), the foe's (x, y) and dmg = dropDmg (the cinema finds
      the killing blow with `plan.find(c => c.fatal)` and cuts to its side and
      spot -- the second v108 review's note); or a beat from any other
      landing, miss or drop
  [8] "The bow keeps firing": Ironhail's facing not advancing by spin as ever,
      in the window and out; the bow's fire not asked exactly once on every
      unfrozen step (and never on a frozen one); a fire frame whose cadence is
      not the engine's, rebuilt from the captured state (fireCd - dt > 0: no
      shot and fireCd - dt; else exactly one ordinary shot and fireCd - dt +
      cadence x cm; a skipped frame -- stun, dead, over -- neither); any blow
      of Ironhail's (a shot or the blade) whose damage is not the bow's own,
      rebuilt exactly from the captured crit and jitter draws; no shots
      loosed in windows. (The fire rebuild is the v108 review's: a bow at half
      its cadence in the window passed the spin and blow checks.)
  [9] the nova is gone: a cast that spawns a shot, that does not open
      {t: 0, dur, cd: 0}, or that lands on an open window
  STAGE 6 (the picture and the voice, sc-ironhail-sunder-fx). Each check runs
  only on a link that carries its half, read off the page itself:
  [10] THE VOICE (on when "ironhail-land" is in AC.SFX.play.toString()): an
      Ironhail cast without exactly one `ult`/ironhail voice inside fireUlt; a
      tickHail call whose Ironhail voices are not exactly its resolved bolts'
      in order -- one landing thud per landed bolt whose `n` is the count the
      foe carries after THAT landing's sunder (read in the apply and again
      when the voice plays), one miss thud per missed bolt -- so a window
      that closes (on its clock or on a death) sounds nothing (v83 4: the
      close has no voice); any other voice inside tickHail but a ward's own
      shatter (shatter() plays its crit hit voice inside hurt(), once a
      break); and every Ironhail voice of the run accounted for by those
      events (none plays anywhere else, after `over` included)
  [11] THE PICTURE (on when the Match has `tickQuarrel`): `tickQuarrel`, the
      picture's one hook on the step, changing any sim field of either
      fighter or the match (the bolts in the air included) or drawing the
      RNG; the limbs up (quarrelFade exactly 1) other than exactly while the
      window is open, the match not over and the caster alive; a bolt that
      resolves without exactly one new puff at its own spot, hit or miss as
      tickHail resolved it, or a puff with no bolt resolved; a live landing
      without a sunder tag on the board reading the foe's count; a killing
      landing that adds or recounts a sunder tag (the shatter owns that
      frame); limbs up at `over` not cooled to 0 by 0.51s into the verdict;
      a resolved bolt the picture never showed; and on the DRAWN subset (the
      first seed, both sides, every foe, through the kill and the verdict) a
      drawn frame that throws, draws the match's RNG or changes any sim field
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=108001)
ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickHail, oFire = P.fireUlt, oWeap = P.tickWeapon, oLoose = P.tickFire,
        oResolve = P.resolveHit, oStep = P.step;
  let live = false, per = null, forceOnce = false, pass2 = false, fireCalls = 0, hailCalls = 0;
  const born = new WeakMap(), winMT = new WeakMap(), fallFr = {};

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /ironhail-land/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickQuarrel === "function";
  const voices = [], ihAll = {}, oPlay = AC.SFX.play, oQuarrel = P.tickQuarrel;
  let curM = null, postOver = false;
  const ihVoice = q => !!(q && typeof q.w === "string" && /^ironhail/.test(q.w));
  const vname = x => x[0] + (x[1] && x[1].w ? "/" + x[1].w : "") + (x[1] && x[1].crit ? "(crit)" : "");
  /* every voice, with the count the Ironhail's foe carries at the moment a landing thud plays */
  if (stage6v) AC.SFX.play = function(kind, q){
    let atN = null;
    if (curM && kind === "ult" && q && q.w === "ironhail-land"){
      const me = curM.a.w.id === "ironhail" ? curM.a : curM.b, foe = me === curM.a ? curM.b : curM.a;
      atN = foe.stacks("sunder");
    }
    voices.push([kind, q ? Object.assign({}, q) : q, atN]);
    if (kind === "ult" && ihVoice(q)) ihAll[q.w] = (ihAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, statuses,
     window and tally, and the match's clock, stop, verdict, holds, beats, shots
     and the bolts in the air. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "alive", "hits",
              "dealt", "crits", "spinDir", "fireCd", "burden"];
  const simSnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null,
               !!m.latch, !!m.splitHold, m.beats ? m.beats.length : null,
               m.shots.map(q => [q.x, q.y, q.vx, q.vy]), m.hail.map(d => [d.x, d.y, d.t, d.side])];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
      o.push(f.ultHail ? [f.ultHail.t, f.ultHail.dur, f.ultHail.cd] : null, f.hailTally ? JSON.stringify(f.hailTally) : null);
    }
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 30), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 30), i + 30)); };
  /* the bolts tickHail resolved that the picture has not shown yet, a side: {x, y, hit} */
  const pendRes = { a: [], b: [] };
  if (stage6p) P.tickQuarrel = function(dt){
    const s0 = simSnap(this), oR = this.rng, oMR = Math.random;
    const pre = [this.a, this.b].map(f => ({ f, seen: f.quarrelSeen.slice(),
                                             tags: this.tags.filter(g => g.key === "sunder").map(g => [g, g.val]) }));
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oQuarrel.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(11, `tickQuarrel drew the RNG ${drew}x`);
    const s1 = simSnap(this);
    if (s1 !== s0) fail(11, "tickQuarrel changed the sim: " + firstDiff(s0, s1)); else inc("quarrelOk");
    for (const p of pre){
      const f = p.f, side = f === this.a ? "a" : "b", foe = f === this.a ? this.b : this.a, T = f.hailTally;
      /* THE LIMBS ARE UP EXACTLY WHILE THE WINDOW IS (and the match runs, and the caster stands) */
      const live = !!(f.ultHail && !this.over && f.alive);
      if ((f.quarrelFade === 1) !== live) fail(11, `quarrelFade ${f.quarrelFade} with the window ${live ? "live" : "not live"} (over ${this.over}, alive ${f.alive})`);
      else if (live) inc("limbsUp"); else if (f.quarrelFade > 0) inc("limbsCool");
      if (!T){ if (f.quarrelFx.length) fail(11, "a puff with no hail"); continue; }
      /* EACH RESOLVED BOLT: one new puff at its own spot, hit or miss as tickHail resolved it */
      const rise = T.landed + T.missed - p.seen[0] - p.seen[1], Q = pendRes[side];
      const fresh = f.quarrelFx.filter(q => q.t === 0);
      if (rise > 0){
        if (fresh.length !== rise || Q.length !== rise) fail(11, `${rise} bolt(s) resolved by the tally, ${Q.length} seen resolving, ${fresh.length} new puff(s)`);
        else {
          let good = 0;
          for (let i = 0; i < rise; i++){
            const q = fresh[i], b = Q[i];
            if (q.x !== b.x || q.y !== b.y || q.hit !== b.hit) fail(11, `a puff at (${q.x}, ${q.y}) hit ${q.hit}; the bolt at (${b.x}, ${b.y}) ${b.hit ? "landed" : "missed"}`);
            else { good++; inc(b.hit ? "puffHit" : "puffMiss"); }
          }
          if (good === rise) inc("puffOk", rise);
        }
        const hits = Q.filter(b => b.hit).length;
        Q.length = 0;
        if (hits){
          if (foe.alive && foe.hp > 0){
            const k = foe.stacks("sunder");
            if (!this.tags.some(g => g.key === "sunder" && g.val === k)) fail(11, `no sunder tag reads the foe's ${k}`);
            else inc("landTagOk");
          } else {
            /* A KILLING LANDING TAGS NOTHING: no sunder tag added, none recounted */
            const now = this.tags.filter(g => g.key === "sunder");
            const added = now.filter(g => !p.tags.some(t => t[0] === g)).length;
            const recount = p.tags.filter(t => t[0].val !== t[1]).length;
            if (added || recount) fail(11, `a killing landing tagged: ${added} added, ${recount} recounted`);
            else inc("killNoTag");
          }
        }
      } else if (fresh.length) fail(11, `${fresh.length} puff(s) with no bolt resolved`);
    }
    return r;
  };

  P.step = function(dt){
    if (postOver) return oStep.call(this, dt);
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;
    const wasLive = live, me = this.a.w.id === "ironhail" ? this.a : this.b.w.id === "ironhail" ? this.b : null;
    if (!pass2) for (const f of [this.a, this.b]) if (f.ultHail){ if (live) inc("winLive"); else inc("winFrozen"); }
    for (const f of [this.a, this.b]) if (f.ultHail && winMT.has(f.ultHail)) winMT.get(f.ultHail).mt += dt;
    fireCalls = 0; hailCalls = 0;
    const r = oStep.call(this, dt);
    /* THE HAIL'S CLOCK IS THE STEP'S (the second v108 review): `tickHail` is asked exactly
       once on every unfrozen step and on no frozen one. Its per-call checks (the window and
       every fall advance dt a call) are the window clock only if the calls are one a step. */
    if (wasLive && hailCalls !== 1) fail(1, `${hailCalls} tickHail call(s) on an unfrozen step`);
    else if (!wasLive && hailCalls) fail(1, `${hailCalls} tickHail call(s) on a frozen step`);
    else if (wasLive) inc("hailStepOk");
    /* THE BOW IS ASKED TO FIRE ON EVERY UNFROZEN STEP, once, window or not (the fighter loop
       calls tickFire for both balls on every step that is not a latch, a split hold or a hit
       stop), and on no frozen one. */
    if (me){
      if (wasLive && fireCalls !== 1) fail(8, `${me.ultHail ? "IN" : "out of"} the window: ${fireCalls} tickFire call(s) on an unfrozen step`);
      else if (!wasLive && fireCalls) fail(8, `${fireCalls} tickFire call(s) on a frozen step`);
      else if (wasLive) inc("fireStepOk");
    }
    live = false;
    return r;
  };
  P.fireUlt = function(f, foe){
    if (f.w.id !== "ironhail") return oFire.call(this, f, foe);
    const open = !!f.ultHail, ns = this.shots.length, nh = this.hail.length, v0 = voices.length;
    const r = oFire.call(this, f, foe);
    /* [10] THE CAST: exactly one Ironhail voice inside fireUlt, the cast's own */
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ihVoice(x[1]));
      if (cv.length !== 1 || cv[0][1].w !== "ironhail") fail(10, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
      else inc("castVoice");
    }
    if (open) fail(9, "a cast on an open window");
    else if (this.shots.length !== ns) fail(9, `the cast spawned ${this.shots.length - ns} shot(s)`);
    else if (!f.ultHail || f.ultHail.t !== 0 || f.ultHail.cd !== 0 || f.ultHail.dur !== f.w.ult.dur) fail(9, `the cast opened ${JSON.stringify(f.ultHail)}`);
    else if (this.hail.length !== nh) fail(9, "the cast touched the bolts in the air");
    else { inc("castOk"); winMT.set(f.ultHail, { mt: 0 }); }
    return r;
  };
  P.tickWeapon = function(f, foe, dt){
    if (!f.w || f.w.id !== "ironhail") return oWeap.call(this, f, foe, dt);
    const th0 = f.theta, stun = f.stun, spin = f.w.spin * f.spinMul(this.actMods.spin), dir = f.spinDir, open = !!f.ultHail;
    const r = oWeap.call(this, f, foe, dt);
    const want = stun > 0 ? th0 : th0 + spin * dt * dir;
    if (f.theta !== want) fail(8, `${open ? "IN" : "out of"} the window: theta ${th0} -> ${f.theta}, want ${want}`);
    else inc(open ? "spinInOk" : "spinOutOk");
    return r;
  };
  /* THE BOW'S FIRE, REBUILT (v108 review): the engine's tickFire arithmetic on the
     captured state. A frame the engine skips (a dead or finished fight, no shot, a stun, an
     aimed draw) leaves `fireCd` alone and looses nothing. Otherwise want = fireCd - dt: above
     zero, nothing is loosed and fireCd is exactly want; at or under zero, exactly one ordinary
     shot is loosed (spawnShot(f) with no angle) and fireCd is exactly want + cadence x cm,
     cm the engine's `(f.ultBal || f.ultNet) && u.cadMul !== undefined ? u.cadMul : 1`.
     Shots are counted at spawnShot, not by `shots.length`, which `maxLive` can pin. */
  P.tickFire = function(f, foe, dt){
    if (!f.w || f.w.id !== "ironhail") return oLoose.call(this, f, foe, dt);
    if (f === this.a || f === this.b) fireCalls++;
    const S = f.w.shot, open = !!f.ultHail, cd0 = f.fireCd;
    const skip = (this.killFlight && f.hp <= 0) || !S || !f.alive || this.over || f.stun > 0 || !!f.ultDraw;
    const cm = (f.ultBal || f.ultNet) && f.w.ult.cadMul !== undefined ? f.w.ult.cadMul : 1;
    const cad = S ? S.cadence : 0, spawns = [], oSpawn = this.spawnShot;
    this.spawnShot = function(ff, ang){ if (ff === f) spawns.push(ang); return oSpawn.call(this, ff, ang); };
    let r;
    try { r = oLoose.call(this, f, foe, dt); }
    finally { delete this.spawnShot; }
    const where = open ? "IN" : "out of";
    if (skip){
      if (spawns.length || f.fireCd !== cd0) fail(8, `${where} the window: a skipped frame loosed ${spawns.length} and moved fireCd ${cd0} -> ${f.fireCd}`);
      else inc("fireSkipOk");
    } else {
      const want = cd0 - dt;
      if (want > 0){
        if (spawns.length || f.fireCd !== want) fail(8, `${where} the window: fireCd ${cd0} -> ${f.fireCd} and ${spawns.length} loosed, want ${want} and none`);
        else inc(open ? "fireInOk" : "fireOutOk");
      } else {
        const cd1 = want + cad * cm;
        if (spawns.length !== 1 || spawns[0] !== undefined || f.fireCd !== cd1)
          fail(8, `${where} the window: fireCd ${cd0} -> ${f.fireCd} and ${spawns.length} loosed (angle ${spawns[0]}), want ${cd1} and one ordinary shot`);
        else inc(open ? "fireInOk" : "fireOutOk");
      }
    }
    if (spawns.length) inc(open ? "shotsIn" : "shotsOut", spawns.length);
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!self.w || self.w.id !== "ironhail") return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultHail, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis,
                  echo: Math.round(foe.curseEcho()) };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    const D = self.dealt - d0, crit = self.crits > c0;
    const raw = self.w.dmg * (mul === undefined ? 1 : mul) * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw) + pre.echo;
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis) inc("blowExempt"); else fail(8, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want} (mul ${mul})`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    return r;
  };
  P.tickHail = function(dt){
    hailCalls++;
    if (!live) fail(1, "tickHail on a frozen step");
    const me = this.a.w.id === "ironhail" ? this.a : this.b.w.id === "ironhail" ? this.b : null;
    for (const f of [this.a, this.b]) if (f.ultHail && f.w.id !== "ironhail") fail(1, `${f.w.id} carries ultHail`);
    for (const d of this.hail) if (!me || this[d.side] !== me) fail(1, "a bolt that is not Ironhail's");
    const bolts = this.hail.map(d => ({ d, t: d.t, x: d.x, y: d.y, side: d.side, open: !!this[d.side].ultHail }));
    const wins = [];
    for (const f of [this.a, this.b]){
      const Z = f.ultHail;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      wins.push({ f, foe, Z, t0: Z.t, cd0: Z.cd, fx: foe.x, fy: foe.y });
    }
    const st = [this.a, this.b].map(f => ({ f, x: f.x, y: f.y, vx: f.vx, vy: f.vy, hp: f.hp, alive: f.alive,
                                            shield: f.shield, smax: f.shieldMax,
                                            stat: JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks])) }));
    const hs0 = this.hitStop, ns = this.shots.length, hurts = [], beats = [], applies = [];
    const oHurt = this.hurt, oBeat = this.beat, oRng = this.rng;
    let shattered = 0, draws = 0;
    this.hurt = function(t, d, s){ const s0 = t.shield; hurts.push([t, d, s]); const r = oHurt.call(this, t, d, s); if (s0 > 0 && t.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.rng = function(){ draws++; return oRng(); };
    const fs = [this.a, this.b];
    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ const e = [f, k, nn, src]; applies.push(e); const rr = o.call(this, k, nn, src); e.push(f.stacks(k)); return rr; }; }
    const v0 = voices.length;
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; }
    if (draws && !shattered) fail(6, `the hail drew the rng ${draws} time(s)`);   // a shatter's own burst draws
    if (this.shots.length !== ns) fail(6, "the hail spawned a shot");
    /* THE BOLTS IN THE AIR */
    let resolvedHere = 0;
    const land = [], expV = [];
    for (const b of bolts){
      const { d } = b, f = this[b.side], foe = f === this.a ? this.b : this.a, u = f.w.ult;
      const fp = st.find(s => s.f === foe);
      const t1 = b.t + dt, gone = !this.hail.includes(d);
      born.set(d, (born.get(d) || 0) + 1);
      const due = t1 >= u.fallT;
      if (!gone){
        if (due) fail(3, `a bolt still in the air at fall ${d.t}`);
        else if (d.t !== t1) fail(3, `fall ${b.t} -> ${d.t}, want ${t1}`);
        else inc("fallOk");
        continue;
      }
      /* a bolt that resolved off its frame fails [3] here, and its landing is still judged by [4]-[7] */
      if (!due) fail(3, `a bolt resolved at fall ${t1} of ${u.fallT}`);
      resolvedHere++;
      inc("resolved"); fallFr[born.get(d)] = (fallFr[born.get(d)] || 0) + 1;
      if (!b.open) inc("late");
      const want = fp.alive && Math.hypot(fp.x - b.x, fp.y - b.y) < u.hitR + R;
      const hs = hurts.filter(h => h[0] === foe), ap_ = applies.filter(x => x[0] === foe);
      if (want){
        inc("landed"); if (!b.open) inc("lateLanded");
        land.push({ foe, f, side: b.side, u });
        expV.push({ w: "ironhail-land", L: land.length - 1, kill: fp.hp > 0 && foe.hp <= 0 });
        pendRes[b.side].push({ x: b.x, y: b.y, hit: true });
        if (hs.length !== 1 || hs[0][1] !== u.dropDmg || hs[0][2] !== f) fail(4, `hurt ${JSON.stringify(hs.map(h => h[1]))} want [${u.dropDmg}] from the caster`);
        else inc("strikeOk");
        if (u.sunder > 0){
          if (ap_.length !== 1 || ap_[0][1] !== "sunder" || ap_[0][2] !== u.sunder) fail(5, `applies ${JSON.stringify(ap_.map(x => [x[1], x[2]]))}`);
          else if (ap_[0][3] !== b.side) fail(5, `source ${typeof ap_[0][3] === "object" ? "a Fighter" : JSON.stringify(ap_[0][3])}`);
          else inc("sunderOk");
        } else if (ap_.length) fail(5, "an application at sunder 0");
        const killed = fp.hp > 0 && foe.hp <= 0, fb = beats.filter(o => o.fatal && o.hail);
        if (killed){
          const B = fb[0], sd = b.side === "a" ? 0 : 1;
          if (fb.length !== 1 || beats.length !== 1) fail(7, `a killing landing filed ${fb.length} fatal hail beat(s) of ${beats.length}`);
          else if (B.kind !== "hit" || B.side !== sd || B.x !== fp.x || B.y !== fp.y || B.dmg !== u.dropDmg)
            fail(7, `the fatal beat says kind ${B.kind} side ${B.side} at (${B.x}, ${B.y}) dmg ${B.dmg}; want hit, side ${sd}, the foe's (${fp.x}, ${fp.y}), dmg ${u.dropDmg}`);
          else inc("fatalLanding");
        }
        else if (beats.length) fail(7, `a landing filed ${beats.length} beat(s)`);
        else inc("beatQuiet");
      } else {
        inc("missed");
        expV.push({ w: "ironhail-miss" });
        pendRes[b.side].push({ x: b.x, y: b.y, hit: false });
        if (hs.length) fail(4, "a miss that struck");
        if (ap_.length) fail(5, "a miss that sundered");
        if (beats.length) fail(7, "a miss that filed a beat");
      }
    }
    if (!resolvedHere){
      if (hurts.length) fail(4, "a hurt with no bolt landing");
      if (applies.length) fail(5, "an apply with no bolt landing");
      if (beats.length) fail(7, "a beat with no bolt landing");
    }
    /* WHO IS STRUCK, AND BY HOW MUCH (the third v108 review). The call's hurts are exactly its
       landings' [foe, dropDmg, caster], in order -- nobody else, the caster included (v83 6.3) --
       and every fighter's hp, ward and ward pool after the call are exactly the ones rebuilt from
       the landings with hurt()'s own arithmetic: the ward absorbs first (min(shield, dmg)); a ward
       that reaches zero shatters, zeroing shield and pool and bursting the hurt's source (the
       caster), if alive, for Math.round(pool x STATUS.ward.shatter); the rest comes off hp. The
       same operations in the same order, so the comparison is exact. */
    const nm = h => h && h.w ? h.w.id : String(h);
    const sameH = hurts.length === land.length &&
      hurts.every((h, i) => h[0] === land[i].foe && h[1] === land[i].u.dropDmg && h[2] === land[i].f);
    if (!sameH) fail(4, `the call's hurts ${JSON.stringify(hurts.map(h => [nm(h[0]), h[1], nm(h[2])]))}, want ${JSON.stringify(land.map(L => [nm(L.foe), L.u.dropDmg, nm(L.f)]))}`);
    else if (land.length) inc("hurtListOk");
    const E = new Map(st.map(s => [s.f, { hp: s.hp, shield: s.shield, smax: s.smax }]));
    let bursts = 0;
    for (const L of land){
      const e = E.get(L.foe), c = E.get(L.f);
      let dmg = L.u.dropDmg;
      if (e.shield > 0 && dmg > 0){
        const absorbed = Math.min(e.shield, dmg);
        e.shield -= absorbed; dmg -= absorbed;
        if (e.shield <= 0){
          const burst = Math.round((e.smax || 0) * AC.STATUS.ward.shatter);
          e.shield = 0; e.smax = 0;
          if (c.hp > 0 && burst > 0){ c.hp -= burst; bursts++; }
        }
      }
      if (dmg > 0) e.hp -= dmg;
    }
    let hpOk = true;
    for (const s of st){
      const f = s.f, e = E.get(f);
      if (f.hp !== e.hp || f.shield !== e.shield || (f.shieldMax || 0) !== (e.smax || 0)){
        hpOk = false;
        fail(4, `${f === this.a ? "a" : "b"} (${nm(f)}${me === f ? ", the caster" : ""}) hp ${s.hp} -> ${f.hp} ward ${s.shield} -> ${f.shield} pool ${s.smax} -> ${f.shieldMax}; rebuilt hp ${e.hp} ward ${e.shield} pool ${e.smax}`);
      }
    }
    if (hpOk){ inc("hpRebuiltOk"); if (land.length) inc("hpLandOk"); if (bursts) inc("burstOk", bursts); }
    const sund = applies.filter(x => x[1] === "sunder"), wantS = land.filter(L => L.u.sunder > 0);
    const sameS = sund.length === wantS.length &&
      sund.every((x, i) => x[0] === wantS[i].foe && x[2] === wantS[i].u.sunder && x[3] === wantS[i].side);
    if (!sameS) fail(5, `the call's sunders ${JSON.stringify(sund.map(x => [nm(x[0]), x[2], typeof x[3] === "object" ? "a Fighter" : x[3]]))}, want ${JSON.stringify(wantS.map(L => [nm(L.foe), L.u.sunder, L.side]))}`);
    /* THE WINDOWS */
    const newBolts = this.hail.filter(d => !bolts.some(b => b.d === d));
    let dropped = 0;
    for (const w of wins){
      const { f, foe, Z } = w, u = f.w.ult, t1 = w.t0 + dt, side = f === this.a ? "a" : "b";
      if (t1 >= Z.dur || !f.alive || !foe.alive){
        if (f.ultHail === Z){ fail(1, "the window did not close"); continue; }
        if (pass2) inc("pass2Closes");
        else if (f.alive && foe.alive){ inc("clockCloses"); const M = winMT.get(Z); if (M){ inc("winMT", M.mt); inc("winMTn"); } }
        else inc("deathCloses");
        continue;
      }
      if (f.ultHail !== Z){ fail(1, `closed at ${t1.toFixed(4)} of ${Z.dur}`); continue; }
      if (Z.t !== t1) fail(1, `window clock ${w.t0} -> ${Z.t}, want ${t1}`);
      inc("frames");
      const cd1 = w.cd0 - dt, mine = newBolts.filter(d => d.side === side);
      if (cd1 <= 0){
        dropped++;
        if (mine.length !== 1) fail(2, `${mine.length} bolts on a drop frame`);
        else if (mine[0].x !== w.fx || mine[0].y !== w.fy) fail(2, "a bolt not at the foe's spot");
        else if (mine[0].t !== 0) fail(2, "a bolt born falling");
        else if (Z.cd !== u.dropCd) fail(2, `cd ${Z.cd} after a drop`);
        else { inc("dropOk"); if (w.t0 === 0) inc("castFrameDrop"); }
      } else {
        if (mine.length) fail(2, "a bolt off the cadence");
        else if (Z.cd !== cd1) fail(2, `cd ${w.cd0} -> ${Z.cd}, want ${cd1}`);
        else inc("cadOk");
        if (w.t0 === 0) fail(2, "no bolt on the cast frame");
      }
    }
    if (newBolts.length !== dropped) fail(2, `${newBolts.length - dropped} bolt(s) from a closed window`);
    /* [10] THE CALL'S VOICES: exactly its resolved bolts', in order -- a landing's thud at the
       count its foe carries after that landing's sunder (in the apply, and when the voice plays),
       a miss's thud -- and nothing else but a ward's own shatter voice (shatter() plays
       SFX.play("hit", {crit: true}) inside hurt(), once a break). A close sounds nothing. */
    if (stage6v){
      const tv = voices.slice(v0);
      const iv = tv.filter(x => x[0] === "ult" && ihVoice(x[1])), ov = tv.filter(x => !(x[0] === "ult" && ihVoice(x[1])));
      const sund = applies.filter(x => x[1] === "sunder");
      const got = iv.map(x => x[1].w + (x[1].w === "ironhail-land" ? ":" + x[1].n + "@" + x[2] : ""));
      const want = expV.map(e => { if (e.w !== "ironhail-land") return e.w;
                                   const k = sund[e.L] ? sund[e.L][4] : "none"; return e.w + ":" + k + "@" + k; });
      const shV = ov.filter(x => x[0] === "hit" && x[1] && x[1].crit === true).length;
      const closed = wins.filter(w => w.f.ultHail !== w.Z);
      if (JSON.stringify(got) !== JSON.stringify(want)) fail(10, `tickHail voiced ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
      else if (ov.length !== shV || shV !== shattered) fail(10, `tickHail also played ${JSON.stringify(ov.map(vname))} with ${shattered} ward break(s)`);
      else {
        for (const e of expV){
          if (e.w === "ironhail-miss") inc("missVoice");
          else { inc("landVoice"); const k = sund[e.L][4]; inc("landN" + k); if (e.kill) inc("killLandVoice"); }
        }
        if (shV) inc("shatterVoiceOk", shV);
        for (const w of closed){ if (w.f.alive && w.foe.alive) inc("clockCloseSilent"); else inc("deathCloseSilent"); }
      }
    }
    /* NOTHING ELSE */
    for (const s of st){
      const f = s.f;
      if (f.x !== s.x || f.y !== s.y) fail(6, "the hail moved a ball");
      if (!shattered && (f.vx !== s.vx || f.vy !== s.vy)) fail(6, "the hail pushed a ball");
      const stat = JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks]));
      const other = applies.filter(x => x[0] === f && x[1] !== "sunder");
      if (other.length) fail(6, `the hail applied ${other[0][1]}`);
      if (stat !== s.stat && !applies.some(x => x[0] === f) && !shattered) fail(6, "a status moved with no apply");
    }
    if (!shattered && this.hitStop !== hs0) fail(6, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
    if (shattered) inc("wardBreaks", shattered);
    inc("calls");
    /* THE FORCED CLOSE (the second pass only): at 0.4 / 0.3 no bolt is ever in the air when a
       window closes on its clock (the last drops at 7.6s and lands at 7.9s), so the probe closes
       one window by its clock on the frame after a drop, and [3] watches that bolt land. */
    if (forceOnce) for (const w of wins){
      const side = w.f === this.a ? "a" : "b";
      if (w.f.ultHail === w.Z && newBolts.some(d => d.side === side)){ w.Z.t = w.Z.dur - dt / 2; forceOnce = false; inc("forcedCloses"); }
    }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "ironhail");
  const T = { casts: 0, frames: 0, drops: 0, landed: 0, missed: 0, dealt: 0, sunder: 0, late: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), through the kill and the verdict,
     with the sim read before and after each frame and the match's RNG
     watched. The post chain is off: this asks what a draw WRITES, not what
     it looks like (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = m.hail.length > 0 || [m.a, m.b].some(q => q.quarrelFade > 0 || q.quarrelFx.length);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    try { AC.__draw(m); } catch (e){ fail(11, "a drawn frame threw: " + String((e && e.message) || e)); }
    finally { m.rng = oR; }
    const s1 = simSnap(m);
    if (dr) fail(11, `a drawn frame drew the match's RNG ${dr}x`);
    else if (s1 !== s0) fail(11, "a drawn frame changed the sim: " + firstDiff(s0, s1));
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "ironhail", sd) : new AC.Match("ironhail", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    curM = m; voices.length = 0; pendRes.a.length = 0; pendRes.b.length = 0;
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.hailTally) for (const k in T) T[k] += me.hailTally[k];
    /* THE VERDICT (stage 6): 0.51s past `over`, the step hook passing straight
       through. Limbs up at `over` cool to 0 in it; every resolved bolt has
       been shown. */
    if (stage6p && m.over){
      const upAtOver = me.quarrelFade > 0;
      postOver = true;
      try { for (let k = 0; k < 61; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
      finally { postOver = false; }
      if (upAtOver){ if (me.quarrelFade !== 0) fail(11, `limbs up at \`over\` still at ${me.quarrelFade} 0.51s into the verdict`); else inc("coolAtVerdict"); }
      if (pendRes.a.length || pendRes.b.length) fail(11, `${pendRes.a.length + pendRes.b.length} resolved bolt(s) the picture never showed`);
    }
  }
  if (n.frames > 0 && !n.shotsIn) fail(8, "the bow loosed nothing in any window");
  /* THE SECOND PASS: one window a fight closed by its clock with a bolt in the air (above);
     these fights are not in any tally or the win rate. */
  pass2 = true;
  for (const fid of foes.slice(0, 16)){
    const m = new AC.Match("ironhail", fid, seeds[0]);
    per = null; forceOnce = true;
    curM = m; voices.length = 0; pendRes.a.length = 0; pendRes.b.length = 0;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    forceOnce = false;
  }
  P.tickHail = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.tickFire = oLoose; P.resolveHit = oResolve; P.step = oStep;
  curM = null;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY IRONHAIL VOICE OF THE RUN, ACCOUNTED FOR by its event (both passes and every verdict). */
    const want = { "ironhail": n.castVoice || 0, "ironhail-land": n.landVoice || 0, "ironhail-miss": n.missVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(ihAll)]))
      if ((ihAll[k] || 0) !== (want[k] || 0)) fail(10, `${ihAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickQuarrel = oQuarrel;
  const u = AC.WEAPONS.find(w => w.id === "ironhail").ult;
  const w = AC.WEAPONS.find(w => w.id === "ironhail");
  return { n, bad, T, fights, win: wins / decided, stage6v, stage6p, drawOn, ihAll, blowsIn: bin / fights, blowsOut: bout / fights, fallFr,
           u: { charge: u.charge, dur: u.dur, dropCd: u.dropCd, fallT: u.fallT, hitR: u.hitR, dropDmg: u.dropDmg, sunder: u.sunder, blade: w.dmg } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickHail === 'function'"):
        raise SystemExit("no tickHail in this build -- not a hail link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
print(f"\nQUARRELSTORM (HAIL) PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Ironhail both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"shots loosed: in windows {n.get('shotsIn',0)/R['fights']:.2f}, outside {n.get('shotsOut',0)/R['fights']:.2f} a fight   Ironhail win {R['win']:.1%}")
print(f"  per cast: drops {T['drops']/casts:.2f}  landed {T['landed']/casts:.2f}  dmg {T['dealt']/casts:.2f}  "
      f"sunder {T['sunder']/casts:.2f}   landed share {100*T['landed']/max(1,T['landed']+T['missed']):.1f}%   "
      f"bolts resolved after the close {T['late']/casts:.2f} a cast; forced closes {n.get('forcedCloses',0)}: "
      f"{n.get('late',0)} bolts resolved after them, {n.get('lateLanded',0)} landed")
print(f"  the bow's fire rebuilt: {n.get('fireInOk',0)} frames in windows, {n.get('fireOutOk',0)} outside, "
      f"{n.get('fireSkipOk',0)} skipped (stun / dead / over); asked once on {n.get('fireStepOk',0)} unfrozen steps")
print(f"  who is struck: {n.get('hurtListOk',0)} landing calls whose hurts are exactly [foe, dropDmg, caster]; "
      f"hp / ward / pool rebuilt exactly on {n.get('hpRebuiltOk',0)} hail calls ({n.get('hpLandOk',0)} with a landing, "
      f"{n.get('burstOk',0)} ward bursts on the caster)")
print(f"  the hail's clock: tickHail asked once on {n.get('hailStepOk',0)} unfrozen steps (none on a frozen one), "
      f"{n.get('frames',0)} open-window frames")
print(f"  fall on the window clock: {R['fallFr']} calls   killing landings {n.get('fatalLanding',0)}   "
      f"wards broken by the hail {n.get('wardBreaks',0)}   clock closes {n.get('clockCloses',0)}, death closes {n.get('deathCloses',0)}")
print(f"  FREEZE CENSUS {100*frozen:.1f}% of window steps frozen   a clock window lasts "
      f"{n.get('winMT',0)/max(1,n.get('winMTn',0)):.2f}s of match time ({U['dur']}s on the window clock)")
checks = [
    (1, "the window: dur on the window clock (tickHail once on every unfrozen step, never on a frozen one; dt a call), closes on either death; only Ironhail's",
        n.get("clockCloses", 0) > 0 and n.get("frames", 0) > 0 and n.get("hailStepOk", 0) > 0),
    (2, "a bolt every dropCd (cd - dt <= 0, then cd = dropCd) at the foe's (x, y), the first on the cast frame",
        n.get("dropOk", 0) > 0 and n.get("castFrameDrop", 0) > 0 and n.get("cadOk", 0) > 0),
    (3, "each bolt falls dt a call and resolves on the call its fall reaches fallT, the window open or closed",
        n.get("fallOk", 0) > 0 and n.get("resolved", 0) > 0 and n.get("late", 0) > 0),
    (4, "struck iff a live foe within hitR + R of the spot: hurt(foe, dropDmg, caster) once, nobody else hurt; every hp and ward rebuilt; a miss nothing",
        n.get("strikeOk", 0) > 0 and n.get("missed", 0) > 0 and n.get("hurtListOk", 0) > 0
        and n.get("hpLandOk", 0) > 0 and n.get("burstOk", 0) > 0),
    (5, "each landing sunders: apply('sunder', sunder, side letter) once, on the foe only; none on a miss (none at sunder 0)",
        (n.get("sunderOk", 0) > 0) if U["sunder"] else n.get("landed", 0) > 0),
    (6, "nothing else: no move, no push, no stop but a ward's own shatter, no rng, no shot, no other status",
        n.get("calls", 0) > 0),
    (7, "a killing landing files one fatal hail beat (hit, the caster's side, the foe's spot, dropDmg); nothing else files one",
        n.get("fatalLanding", 0) > 0 and n.get("beatQuiet", 0) > 0),
    (8, "the bow keeps firing: its spin, its fire (asked once a step; cadence rebuilt) and every blow its own, in the window and out",
        n.get("spinInOk", 0) > 0 and n.get("spinOutOk", 0) > 0 and n.get("blowInOk", 0) > 0
        and n.get("blowOutOk", 0) > 0 and n.get("shotsIn", 0) > 0 and n.get("fireInOk", 0) > 0
        and n.get("fireOutOk", 0) > 0 and n.get("fireStepOk", 0) > 0),
    (9, "the nova is gone: a cast spawns no shot, opens {t 0, dur, cd 0}, never on an open window", n.get("castOk", 0) > 0),
]
if R.get("stage6v"):
    ns = {k: n[k] for k in sorted(n, key=lambda k: (len(k), k)) if k.startswith("landN")}
    print(f"  stage 6 voice: casts {n.get('castVoice',0)}  landing thuds {n.get('landVoice',0)} (n "
          f"{', '.join(f'{k[5:]}:{v}' for k, v in ns.items())}; {n.get('killLandVoice',0)} on a killing landing)  "
          f"miss thuds {n.get('missVoice',0)}  ward shatters' own voice {n.get('shatterVoiceOk',0)}  silent closes: "
          f"{n.get('clockCloseSilent',0)} clock, {n.get('deathCloseSilent',0)} death   run totals {R['ihAll']}")
    checks.append((10, "stage 6 voice: one cast voice a cast; one landing thud a landed bolt at the foe's count after its sunder, "
                       "one miss thud a missed bolt, in order; nothing else in tickHail but a ward's own shatter; no close voice; "
                       "every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "landVoice", "missVoice", "killLandVoice", "shatterVoiceOk",
                                                 "clockCloseSilent", "deathCloseSilent"))))
if R.get("stage6p"):
    print(f"  stage 6 picture: tickQuarrel calls clean {n.get('quarrelOk',0)}  limbs up {n.get('limbsUp',0)}, cooling "
          f"{n.get('limbsCool',0)}  puffs at their bolts {n.get('puffOk',0)} ({n.get('puffHit',0)} landed, {n.get('puffMiss',0)} "
          f"missed)  the foe's count tagged {n.get('landTagOk',0)}  killing landings untagged {n.get('killNoTag',0)}  "
          f"cooled in the verdict {n.get('coolAtVerdict',0)}  drawn frames {n.get('drawOk',0)} ({n.get('drawPic',0)} with the "
          f"picture up, {n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawVerdict',0)} in the verdict)"
          + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((11, "stage 6 picture: tickQuarrel writes no sim field and draws no RNG; the limbs up exactly while the window is; "
                       "one puff a resolved bolt at its spot, hit or miss; the foe's count tagged, a kill untagged; cooled in the "
                       "verdict; no drawn frame throws, draws the RNG or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("quarrelOk", "limbsUp", "limbsCool", "puffHit", "puffMiss", "landTagOk",
                                                 "killNoTag", "coolAtVerdict"))
                   and (n.get("drawPic", 0) > 0 and n.get("drawPicStop", 0) > 0 and n.get("drawVerdict", 0) > 0
                        if R.get("drawOn") else True)))
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
