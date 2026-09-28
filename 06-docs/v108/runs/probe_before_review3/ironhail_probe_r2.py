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
      hurt(foe, dropDmg, the caster)
  [5] "and sundered": a landing without exactly one apply("sunder", sunder,
      side letter) on the foe (none at sunder 0), or any on a miss
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
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickHail, oFire = P.fireUlt, oWeap = P.tickWeapon, oLoose = P.tickFire,
        oResolve = P.resolveHit, oStep = P.step;
  let live = false, per = null, forceOnce = false, pass2 = false, fireCalls = 0, hailCalls = 0;
  const born = new WeakMap(), winMT = new WeakMap(), fallFr = {};

  P.step = function(dt){
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
    const open = !!f.ultHail, ns = this.shots.length, nh = this.hail.length;
    const r = oFire.call(this, f, foe);
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
                                            stat: JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks])) }));
    const hs0 = this.hitStop, ns = this.shots.length, hurts = [], beats = [], applies = [];
    const oHurt = this.hurt, oBeat = this.beat, oRng = this.rng;
    let shattered = 0, draws = 0;
    this.hurt = function(t, d, s){ const s0 = t.shield; hurts.push([t, d, s]); const r = oHurt.call(this, t, d, s); if (s0 > 0 && t.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.rng = function(){ draws++; return oRng(); };
    const fs = [this.a, this.b];
    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ applies.push([f, k, nn, src]); return o.call(this, k, nn, src); }; }
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; }
    if (draws && !shattered) fail(6, `the hail drew the rng ${draws} time(s)`);   // a shatter's own burst draws
    if (this.shots.length !== ns) fail(6, "the hail spawned a shot");
    /* THE BOLTS IN THE AIR */
    let resolvedHere = 0;
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
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "ironhail", sd) : new AC.Match("ironhail", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.hailTally) for (const k in T) T[k] += me.hailTally[k];
  }
  if (n.frames > 0 && !n.shotsIn) fail(8, "the bow loosed nothing in any window");
  /* THE SECOND PASS: one window a fight closed by its clock with a bolt in the air (above);
     these fights are not in any tally or the win rate. */
  pass2 = true;
  for (const fid of foes.slice(0, 16)){
    const m = new AC.Match("ironhail", fid, seeds[0]);
    per = null; forceOnce = true;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    forceOnce = false;
  }
  P.tickHail = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.tickFire = oLoose; P.resolveHit = oResolve; P.step = oStep;
  const u = AC.WEAPONS.find(w => w.id === "ironhail").ult;
  const w = AC.WEAPONS.find(w => w.id === "ironhail");
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, fallFr,
           u: { charge: u.charge, dur: u.dur, dropCd: u.dropCd, fallT: u.fallT, hitR: u.hitR, dropDmg: u.dropDmg, sunder: u.sunder, blade: w.dmg } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickHail === 'function'"):
        raise SystemExit("no tickHail in this build -- not a hail link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
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
    (4, "struck iff a live foe within hitR + R of the spot: hurt(foe, dropDmg, caster) once; a miss nothing",
        n.get("strikeOk", 0) > 0 and n.get("missed", 0) > 0),
    (5, "each landing sunders: apply('sunder', sunder, side letter) once; none on a miss (none at sunder 0)",
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
