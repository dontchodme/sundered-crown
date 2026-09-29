#!/usr/bin/env python
"""FORESIGHT'S PROBE -- one check per sentence of v75 §1 / §5 and the brief's §0-§1,
read INSIDE the hooks.

    python oracle_probe.py --game <link>            # stage 2 onward

Wraps `step`, `tickWeapon`, `tickFire`, `tickCharge`, `fireUlt`, `resolveHit`
and `tickSight` on the Match prototype and reads each event where it happens.
Runs Oracle against every other relic, both sides, and prints N/N. The checks
follow the link's own numbers, so the same probe gates stages 2-5 (hex 0 / 1,
the blade).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] THE WINDOW ("for a duration", 8s): a window whose clock does not advance
      exactly dt a window-ticker frame, that closes before `dur` with both
      alive or does not close on the first frame it reaches `dur`, that
      outlives either death, or any relic but Oracle carrying `ultSight`; and
      a window that is not, on entering tickSight, exactly what the cast or
      the last tickSight left (the same object, t and dur), so no writer
      anywhere else in the step can stretch or cut it unseen
  [2] THE AIM ("every arrow of the stream flies to it"; design §5): a window
      frame, stunned or not, whose facing is not exactly theta + clamp(the
      shortest angle to atan2(lead - f), +-turn x dt), lead = foe + v_foe x
      |foe - f| / shot.speed (theta held if either is dead); the facing moving
      in a hit stop; outside the window, a facing that did not advance by spin
      as ever (held while stunned)
  [3] THE STREAM ("tickFire is untouched"): a frame, in the window or out,
      where the bow fired when its cadence clock had not run out or did not
      fire when it had (alive, unstunned), fired other than one shot along
      f.theta at shot.speed, or moved the cadence clock other than -dt
      (+cadence on a shot); and a cadence clock that is not, on entering
      tickFire, what the last tickFire left (only tickFire writes fireCd in
      this engine: the constructor and tickFire's own two lines)
  [4] THE ARROW AS EVER: an Oracle blow (arrow or blade, in the window or out)
      whose damage is not the blade x mul x dmgMul x jitter x dmgTaken,
      rounded, crit included -- rebuilt from the captured draws -- or whose hit
      stop is not the blow's own (a ward's own shatter aside), or that filed
      other than its one hit beat
  [5] THE DOUBLE HEX ("an arrow that lands hexes twice"): an arrow landing in a
      window whose applications on the foe are not exactly the channel's hex 1
      and one more, +hex with a side letter (a live foe; at hex 0, the
      channel's alone); any second hex on a blade blow or outside a window;
      the tally's arrows or hex not matching
  [6] NOTHING ELSE: tickWeapon writing anything but the caster's facing. Every
      other field of both fighters (the balls, spinDir, fireCd, stun, hp, ...;
      the foe's facing too), both swing phases, both status maps, the tally,
      and the match's clock, stop and shots are snapshotted across it, in the
      window and out. (The caster's charge is [7]'s and its window [1]'s, so
      every field has one owner.) tickSight writing anything but the window
      and its tally; an apply moving the stop
  [7] THE CAST ("nothing waits"; "every 16s", 14 on the game's clock): a
      frame whose charge reached `charge` with the bow alive and no cast, a
      cast below it, or a cast while a window runs; a cast that files other
      than one `ult` beat (the brief's stage 6: "cast files `ult`"); a live frame with no cast
      whose charge did not fill by exactly dt, or a dead or ended one where it
      moved; and a charge that is not, on entering tickCharge, what the last
      tickCharge left (0 at the first). Only tickCharge writes the charge in
      this engine (the constructor and tickCharge's two lines), so any other
      writer is a faster or slower clock
  STAGE 6 (the picture and the voice, sc-oracle-fx; each check switches on by
  itself, off the page):
  [8] THE VOICE (on when "oracle-sigil" is in AC.SFX.play.toString()): a cast
      without exactly one `ult`/oracle voice inside fireUlt; a window frame
      whose sigil strike is not exactly one on the window's 1st, 9th, 17th ...
      frame (the frames counted here, not read off the build's clock) and none
      on the others; a second hex without exactly one `oracle-hex` snap whose
      `n` is the foe's hex count just after it; a clock close with both alive
      without exactly one `oracle-close`, and ANY close voice on a death close;
      any Oracle voice with a kind other than `ult`; and every Oracle voice of
      the run accounted for by those events (none anywhere else). A ward's
      shatter plays its own crit hit voice inside hurt(): that is the hit's
      voice and not one of these, so it is never counted against them
  [9] THE PICTURE (on when the Match has `tickForesight`): `tickForesight`,
      the picture's one hook on the step, changing any sim field of either
      fighter or the match (bodies, facing, charge, stun, statuses, window,
      tally, clock, stop, shots) or drawing the RNG; `foreFade` not 1 on every
      presentation tick of an open window (a live caster, the fight on), or
      rising outside one; any picture state on the other fighter; a flare
      record that is not exactly one on the tick a window arrow is first seen
      landing on a live foe (none on a killing arrow); a second hex on a live
      foe with no fresh HEX tag carrying the foe's count; and on the DRAWN
      subset (the first seed, both sides, every foe) a frame drawn through the
      renderer that throws or changes any sim field, or a drawn fight that
      ends anywhere but where the same fight ends undrawn
  Printed, comparable to the lab's columns (`overlays/aim.js`): casts a fight,
  blows in / out a fight, arrow hits a cast, the foe's hex on a window frame
  (pooled, and per fight as the lab's f_foeStk), second hexes a cast, the
  freeze census, and THE LOCK -- the share of window frames after the first
  half-second on which the facing already sat within turn x dt of the lead.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=105001)
ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR, I = C.impact;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const clampf = (v, lo, hi) => v < lo ? lo : v > hi ? hi : v;
  const isO = (f) => !!f && !!f.w && f.w.id === "oracle";
  const oStep = P.step, oWeap = P.tickWeapon, oFire = P.tickFire, oCharge = P.tickCharge, oUlt = P.fireUlt,
        oResolve = P.resolveHit, oSight = P.tickSight;
  let per = null;
  const lastV = new WeakMap();
  /* WHAT EACH OWNER LEFT: the charge as tickCharge left it ([7]), the cadence
     clock as tickFire left it ([3]), the window as the cast or tickSight left
     it ([1]). On the next entry each must be exactly that, or something else
     in the step wrote it. */
  const lastC = new WeakMap(), lastCd = new WeakMap(), lastZ = new WeakMap();
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "pin", "pinMax", "pinFree",
              "reachMul", "hits", "dealt", "crits", "spinDir", "fireCd", "ultsFired", "burden"];
  /* [6] across tickWeapon: every field but the caster's facing (it is [2]'s),
     its charge ([7]'s) and its window ([1]'s). */
  const WF = FF.filter(k => k !== "theta" && k !== "charge");
  const wsnap = (m, f, foe) => {
    const o = [m.t, m.hitStop, m.over, m.shots.length, !!m.latch, !!m.splitHold, f.swingPhase, foe.swingPhase, foe.ultSight];
    for (const k of WF) o.push(f[k]);
    for (const k of FF) o.push(foe[k]);
    for (const g of [f, foe]) for (const k of Object.keys(g.status).sort()){ const S = g.status[k]; o.push(k, S.stacks, S.t, S.src); }
    const T = f.sightTally;
    if (T) o.push(T.casts, T.frames, T.foeHex, T.arrows, T.hex);
    return o;
  };
  const wnames = (f, foe) => {
    const o = ["m.t", "m.hitStop", "m.over", "m.shots", "m.latch", "m.splitHold", "f.swingPhase", "foe.swingPhase", "foe.ultSight"];
    for (const k of WF) o.push("f." + k);
    for (const k of FF) o.push("foe." + k);
    for (const [g, s] of [[f, "f"], [foe, "foe"]]) for (const k of Object.keys(g.status).sort()) o.push(`${s}.${k}`, `${s}.${k}.stacks`, `${s}.${k}.t`, `${s}.${k}.src`);
    return o;
  };

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /oracle-sigil/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickForesight === "function";
  const voices = [], orAll = {}, oPlay = AC.SFX.play, oFore = P.tickForesight;
  const isOV = (q) => !!q && typeof q.w === "string" && /^oracle(-|$)/.test(q.w);
  if (stage6v) AC.SFX.play = function(kind, q){
    voices.push([kind, q ? Object.assign({}, q) : q]);
    if (isOV(q)){ orAll[q.w] = (orAll[q.w] || 0) + 1; if (kind !== "ult") fail(8, `an Oracle voice of kind ${kind}`); }
    return oPlay.call(this, kind, q);
  };
  const ovs = (v0) => voices.slice(v0).filter(x => isOV(x[1]));
  const winFrames = new WeakMap();        // a window -> its frames so far, counted here
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, facing,
     charge, stun, statuses, window and tally, and the match's clock, stop,
     verdict and shots in the air. */
  const psnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null, !!m.latch, !!m.splitHold];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(f.alive, f.swingPhase);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t, f.status[k].src]));
      o.push(f.ultSight ? [f.ultSight.t, f.ultSight.dur] : null, f.sightTally ? JSON.stringify(f.sightTally) : null);
    }
    for (const s of m.shots) o.push([s.own, s.x, s.y, s.vx, s.vy, s.life, !!s.stuck]);
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 40), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 40), i + 30)); };
  const seenA = new WeakMap(), seenH = new WeakMap();
  if (stage6p) P.tickForesight = function(dt){
    const pre = [this.a, this.b].map(f => ({ f, fade: f.foreFade, sa: seenA.get(f) || 0, sh: seenH.get(f) || 0 }));
    const s0 = psnap(this), oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oFore.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(9, `tickForesight drew the RNG ${drew}x`);
    const s1 = psnap(this);
    if (s1 !== s0) fail(9, "tickForesight changed the sim: " + firstDiff(s0, s1)); else inc("foreOk");
    for (const p of pre){
      const f = p.f, foe = f === this.a ? this.b : this.a;
      if (!isO(f)){
        if (f.foreFade !== 0 || f.foreFx.length || f.foreRune || f.foreLead) fail(9, `${f.w.id} carries Foresight's picture`);
        continue;
      }
      const open = !this.over && f.alive && !!f.ultSight;
      if (open){ if (f.foreFade !== 1) fail(9, `foreFade ${f.foreFade} in an open window`); else inc("fadeOpenOk"); }
      else if (f.foreFade > p.fade) fail(9, `the eye opened outside a window (${p.fade} -> ${f.foreFade})`);
      else if (p.fade > 0 && f.foreFade === 0) inc("eyeShut");
      const T = f.sightTally;
      if (!T) continue;
      const na = T.arrows - p.sa, nh = T.hex - p.sh;
      seenA.set(f, T.arrows); seenH.set(f, T.hex);
      const live = foe.alive && foe.hp > 0;
      const pushed = f.foreFx.filter(q => q.t === 0).length, want = na > 0 && live ? 1 : 0;
      if (pushed !== want) fail(9, `${pushed} flare records for ${na} window arrows first seen (foe ${live ? "live" : "down"})`);
      else if (want) inc("flareOk");
      else if (na > 0) inc("killNoFlare");
      if (nh > 0 && live){
        const k = foe.stacks("hex");
        const tg = this.tags.some(g => g.key === "hex" && g.val === k && g.life === g.max && Math.hypot(g.x - foe.x, g.y - foe.y) < R * 3);
        if (!tg) fail(9, `a second hex (the foe at ${k}) and no fresh HEX tag carrying the count`); else { inc("tagOk"); inc("tagN" + k); }
      }
    }
    return r;
  };

  /* THE FREEZE CENSUS, and no facing moves in a frozen step. */
  P.step = function(dt){
    const frozen = !this.over && (this.hitStop > 0 || !!this.latch || !!this.splitHold);
    const th = [this.a.theta, this.b.theta];
    for (const f of [this.a, this.b]) if (isO(f) && f.ultSight){ if (frozen) inc("winFrozen"); else inc("winLive"); }
    const r = oStep.call(this, dt);
    if (frozen){ [this.a, this.b].forEach((f, i) => { if (isO(f) && f.theta !== th[i]) fail(2, "the facing moved in a hit stop"); }); if (isO(this.a) || isO(this.b)) inc("frozenSteps"); }
    return r;
  };

  P.tickWeapon = function(f, foe, dt){
    if (!isO(f)) return oWeap.call(this, f, foe, dt);
    const V = f.ultSight, th0 = f.theta, stun = f.stun, fAlive = f.alive, foeAlive = foe.alive;
    const fx = foe.x, fy = foe.y, fvx = foe.vx, fvy = foe.vy, x = f.x, y = f.y;
    const w0 = wsnap(this, f, foe);
    const spinMul = f.spinMul(this.actMods.spin), spinDir = f.spinDir;
    const r = oWeap.call(this, f, foe, dt);
    /* [6] tickWeapon writes the facing and nothing else */
    const w1 = wsnap(this, f, foe);
    let wi = w0.length === w1.length ? -1 : Math.min(w0.length, w1.length);
    for (let i = 0; wi < 0 && i < w0.length; i++) if (!Object.is(w0[i], w1[i])) wi = i;
    if (wi >= 0) fail(6, `tickWeapon wrote ${wnames(f, foe)[wi] || "the status map"}: ${w0[wi]} -> ${w1[wi]} (${V ? "in" : "out of"} the window)`);
    else inc("stillOk");
    if (V){
      inc("aimFrames"); if (stun > 0) inc("aimStunned");
      let want = th0;
      if (fAlive && foeAlive){
        const S = f.w.shot, u = f.w.ult;
        const tof = Math.hypot(fx - x, fy - y) / S.speed;
        const tx = fx + fvx * tof, ty = fy + fvy * tof;
        const bear = Math.atan2(ty - y, tx - x);                 // grav 0: the build asserts it
        const dl = Math.atan2(Math.sin(bear - th0), Math.cos(bear - th0));
        const k = u.turn * dt;
        want = th0 + clampf(dl, -k, k);
        /* THE LOCK, measured: after the first half-second of the window. A
           jump in the foe's velocity (a bounce or a knock) of more than 150
           u/s since the last aimed frame arms a 0.6s mark. */
        const lv = lastV.get(f);
        const jt = lv && Math.hypot(fvx - lv[0], fvy - lv[1]) > 150 ? 0.6 : lv ? Math.max(0, lv[2] - dt) : 0;
        lastV.set(f, [fvx, fvy, jt]);
        if (V.t >= 0.5){
          inc("lockFrames");
          if (Math.abs(dl) <= k) inc("locked");
          else if (jt > 0) inc("unlockedAfterJump");
        }
      } else inc("aimHeld");
      if (f.theta !== want) fail(2, `window: theta ${th0} -> ${f.theta}, want ${want} (stun ${stun}, alive ${fAlive}/${foeAlive})`);
      else inc("aimOk");
    } else {
      lastV.delete(f);
      const want = stun <= 0 ? th0 + f.w.spin * spinMul * 1 * dt * spinDir : th0;
      if (f.theta !== want) fail(2, `out of the window: theta ${th0} -> ${f.theta}, want ${want}`); else inc("spinOk");
    }
    return r;
  };

  P.tickFire = function(f, foe, dt){
    if (!isO(f)) return oFire.call(this, f, foe, dt);
    const S = f.w.shot, V = !!f.ultSight, cd0 = f.fireCd, stun = f.stun;
    const live = !(this.killFlight && f.hp <= 0) && f.alive && !this.over;
    const last = this.shots[this.shots.length - 1], len0 = this.shots.length;
    if (lastCd.has(f)){
      if (lastCd.get(f) !== cd0) fail(3, `the cadence clock moved outside tickFire: ${lastCd.get(f)} -> ${cd0} (${V ? "in" : "out of"} the window)`);
      else inc("cdKeptOk");
    }
    const r = oFire.call(this, f, foe, dt);
    lastCd.set(f, f.fireCd);
    const nl = this.shots[this.shots.length - 1];
    const spawned = nl !== last ? 1 : 0;
    if (!live || stun > 0){
      if (spawned || f.fireCd !== cd0) fail(3, `fired or moved the cadence while ${live ? "stunned" : "down"}`); else inc("holdOk");
      if (live && V) inc("winStunFrames");
      return r;
    }
    const c1 = cd0 - dt, shoot = !(c1 > 0);
    if (shoot !== !!spawned) fail(3, `cadence ${cd0} -> shot ${spawned}, want ${shoot}`);
    else if (shoot){
      const want = c1 + S.cadence;
      if (f.fireCd !== want) fail(3, `cadence after a shot ${f.fireCd}, want ${want}`);
      else if (this.shots.length > len0 + 1) fail(3, "more than one shot");
      else if (nl.a !== f.theta || nl.vx !== Math.cos(f.theta) * S.speed || nl.vy !== Math.sin(f.theta) * S.speed)
        fail(3, "a shot not along the facing at the shot speed");
      else { inc("shotOk"); inc(V ? "shotsIn" : "shotsOut"); }
    } else if (f.fireCd !== c1) fail(3, `cadence ${cd0} -> ${f.fireCd}, want ${c1}`);
    else inc("cadOk");
    if (V) inc("winFireFrames"); else inc("outFireFrames");
    return r;
  };

  P.tickCharge = function(f, foe, dt){
    if (!isO(f)) return oCharge.call(this, f, foe, dt);
    const c0 = f.charge, u0 = f.ultsFired, live = f.alive && !this.over, open = !!f.ultSight;
    /* the charge is tickCharge's alone: on entry it is what the last one left */
    const cl = lastC.has(f) ? lastC.get(f) : 0;
    if (cl !== c0) fail(7, `the charge moved outside tickCharge: ${cl} -> ${c0} (${open ? "in" : "out of"} the window)`);
    else inc("chargeKeptOk");
    const r = oCharge.call(this, f, foe, dt);
    const cast = f.ultsFired - u0;
    if (live){
      const due = c0 + dt >= f.w.ult.charge;
      if (due && cast !== 1) fail(7, `charge ${c0 + dt} reached ${f.w.ult.charge} with no cast (window ${open})`);
      else if (!due && cast) fail(7, `a cast at charge ${c0 + dt}`);
      else if (cast){ if (f.charge !== 0) fail(7, "the charge not spent"); else inc("castDueOk"); }
      else if (f.charge !== c0 + dt) fail(7, `the charge filled ${c0} -> ${f.charge}, want +${dt}`);
      else inc("chargeOk");
    } else if (cast) fail(7, "a cast from a dead bow or an ended match");
    else if (f.charge !== c0) fail(7, `the charge moved on a dead bow or an ended match: ${c0} -> ${f.charge}`);
    lastC.set(f, f.charge);
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isO(f)) return oUlt.call(this, f, foe);
    if (f.ultSight) fail(7, "a cast under an open window");
    const c0 = f.sightTally ? f.sightTally.casts : 0, v0 = voices.length;
    /* the brief's stage 6: "Beats: cast files `ult`" -- one, and nothing else */
    const bts = [], oBeat = this.beat;
    this.beat = function(o){ bts.push(o); return oBeat.call(this, o); };
    let r;
    try { r = oUlt.call(this, f, foe); } finally { delete this.beat; }
    if (bts.length !== 1 || bts[0].kind !== "ult") fail(7, `a cast filed ${JSON.stringify(bts.map(b => b.kind))}`); else inc("castBeatOk");
    if (stage6v){
      const ov = ovs(v0);
      if (ov.length !== 1 || ov[0][0] !== "ult" || ov[0][1].w !== "oracle") fail(8, `a cast voiced ${JSON.stringify(ov.map(x => x[1].w))}`);
      else inc("castVoice");
    }
    const Z = f.ultSight;
    if (!Z || Z.t !== 0 || Z.dur !== f.w.ult.dur || Object.keys(Z).length !== 2 || f.sightTally.casts !== c0 + 1)
      fail(1, `the cast opened ${JSON.stringify(Z)}`);
    else inc("castOk");
    lastZ.set(f, Z ? [Z, Z.t, Z.dur] : null);
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isO(self)) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const V = !!self.ultSight, arrow = mul !== undefined, u = self.w.ult, side = self === this.a ? "a" : "b";
    const d0 = self.dealt, c0 = self.crits, h0 = self.hits, hs0 = this.hitStop, sh0 = foe.shield;
    const T = self.sightTally, ta0 = T ? T.arrows : 0, tx0 = T ? T.hex : 0;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis, curse: foe.stacks("curse") };
    const draws = [], oRng = this.rng, applies = [], beats = [], oBeat = this.beat;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    const oApply = foe.apply, M = this, afterX = [], v0 = voices.length;
    foe.apply = function(k, nn, src){ const h = M.hitStop; applies.push([k, nn, src]); const rr = oApply.call(this, k, nn, src);
      if (k === "hex" && src === side) afterX.push(foe.stacks("hex"));
      if (M.hitStop !== h) fail(6, "an apply moved the hit stop"); return rr; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; delete this.beat; delete foe.apply; }
    /* [8] one snap a second hex, at the count the foe carries just after it */
    if (stage6v){
      const ov = ovs(v0), hv = ov.filter(x => x[1].w === "oracle-hex");
      if (hv.length !== ov.length) fail(8, `an Oracle voice in resolveHit that is not the snap: ${JSON.stringify(ov.map(x => x[1].w))}`);
      if (hv.length !== afterX.length) fail(8, `${afterX.length} second hex(es), ${hv.length} snap(s) (${V ? "in" : "out of"} the window, ${arrow ? "arrow" : "blade"})`);
      else for (let i = 0; i < hv.length; i++){
        if (hv[i][1].n !== afterX[i]) fail(8, `a snap at n ${hv[i][1].n}, the foe carried ${afterX[i]}`);
        else { inc("hexVoice"); inc("snapN" + afterX[i]); }
      }
    }
    if (self.hits - h0 !== 1) return r;
    if (per){ if (V) per.in++; else per.out++; if (arrow){ if (V) per.ain++; else per.aout++; } }
    inc(arrow ? (V ? "arrowIn" : "arrowOut") : (V ? "bladeIn" : "bladeOut"));
    /* [4] the blow as ever */
    const D = self.dealt - d0, crit = self.crits > c0, fatal = foe.hp <= 0;
    const raw = self.w.dmg * (arrow ? mul : 1) * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (pre.aegis || pre.curse) inc("blowExempt");
    else if (Math.abs(D - want) > 1e-6) fail(4, `${V ? "IN" : "out of"} the window (${arrow ? "arrow" : "blade"}): dealt ${D}, want ${want}`);
    else {
      let stop = Math.min(I.stopMax, I.stopBase + D * I.stopPerDmg);
      if (crit) stop *= I.critStopMul;
      if (fatal) stop = I.killStop;
      let hsw = stop > 0 ? Math.max(hs0, stop) : hs0;
      const broke = sh0 > 0 && foe.shield <= 0;
      if (broke) hsw = Math.max(hsw, 0.10);
      if (this.hitStop !== hsw) fail(4, `hit stop ${hs0} -> ${this.hitStop}, want ${hsw} (${V ? "in" : "out of"} the window)`);
      else if (beats.length !== 1 || beats[0].kind !== "hit" || beats[0].fatal !== fatal) fail(4, `a blow filed ${beats.length} beats`);
      else inc(V ? "blowInOk" : "blowOutOk");
    }
    /* [5] the double hex */
    const chan = applies.filter(x => x[0] === "hex" && x[1] === 1 && x[2] === undefined);
    const extra = applies.filter(x => !(x[0] === "hex" && x[1] === 1 && x[2] === undefined));
    const wantExtra = arrow && V && u.hex > 0 && foe.alive && !foe.shade;
    if (chan.length !== 1) fail(5, `the channel applied ${chan.length}x`);
    else if (wantExtra){
      if (extra.length !== 1 || extra[0][0] !== "hex" || extra[0][1] !== u.hex || extra[0][2] !== side)
        fail(5, `an arrow in the window applied ${JSON.stringify(extra)}`);
      else if (T.hex - tx0 !== u.hex) fail(5, "the tally's hex does not match");
      else { inc("hexOk"); inc("hexApplied", 2); }
    } else if (extra.length) fail(5, `${arrow ? "an arrow" : "a blade blow"} ${V ? "in" : "out of"} the window applied ${JSON.stringify(extra)} (hex ${u.hex})`);
    else { inc(arrow && V ? (foe.alive ? "hexZeroOk" : "hexDeadOk") : (arrow ? "outOk" : "bladeOk")); if (arrow && V) inc("hexApplied", 1); }
    if (arrow && V && T.arrows - ta0 !== 1) fail(5, "the tally's arrows do not match");
    if ((!arrow || !V) && T && (T.arrows !== ta0 || T.hex !== tx0)) fail(5, "the tally moved on a blow it should not count");
    return r;
  };

  /* [1] THE WINDOW'S CLOCK, [6] nothing else */
  const snap = (m) => { const o = [m.t, m.hitStop, m.over, m.shots.length];
    for (const f of [m.a, m.b]){ for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t, f.status[k].src])); }
    return JSON.stringify(o); };
  P.tickSight = function(dt){
    const pre = [];
    /* [1] the window is what the cast or the last tickSight left: the same
       object, its t and dur untouched in between, and none opened or shut
       anywhere else */
    for (const f of [this.a, this.b]){
      if (!isO(f)) continue;
      const L = lastZ.get(f) || null, Z = f.ultSight || null;
      if (!L){ if (Z) fail(1, `a window opened outside the cast: ${JSON.stringify(Z)}`); }
      else if (Z !== L[0] || Z.t !== L[1] || Z.dur !== L[2] || Object.keys(Z).length !== 2)
        fail(1, `the window moved outside tickSight: t ${L[1]} dur ${L[2]} -> ${JSON.stringify(Z)}`);
      else inc("winKeptOk");
    }
    for (const f of [this.a, this.b]){
      if (f.ultSight && !isO(f)) fail(1, `${f.w.id} carries ultSight`);
      if (!f.ultSight) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z: f.ultSight, t0: f.ultSight.t, fA: f.alive, oA: foe.alive, fr: f.sightTally.frames, fh: f.sightTally.foeHex,
                 stk: foe.stacks("hex"), T: JSON.stringify(Object.assign({}, f.sightTally, { frames: 0, foeHex: 0 })) });
    }
    const s0 = snap(this), v0 = voices.length;
    const r = oSight.call(this, dt);
    if (snap(this) !== s0) fail(6, "tickSight changed the sim");
    /* [8] the sigil and the close, on the frames counted here */
    if (stage6v){
      let wantSig = 0, wantClose = 0, deathClose = 0;
      for (const p of pre){
        if (!isO(p.f)) continue;
        const t1 = p.t0 + dt;
        if (t1 >= p.Z.dur || !p.fA || !p.oA){ if (t1 >= p.Z.dur && p.fA && p.oA) wantClose++; else deathClose++; continue; }
        const k = (winFrames.get(p.Z) || 0) + 1;
        winFrames.set(p.Z, k);
        if (k % 8 === 1) wantSig++;
      }
      const ov = ovs(v0), sv = ov.filter(x => x[1].w === "oracle-sigil").length, cv = ov.filter(x => x[1].w === "oracle-close").length;
      if (sv + cv !== ov.length) fail(8, `another Oracle voice in tickSight: ${JSON.stringify(ov.map(x => x[1].w))}`);
      if (sv !== wantSig) fail(8, `${sv} sigil strike(s) where the window's frame count wants ${wantSig}`); else if (sv) inc("sigilVoice", sv);
      if (cv !== wantClose) fail(8, `${cv} close voice(s) on ${wantClose} clock close(s) and ${deathClose} death close(s)`);
      else { if (cv) inc("closeVoice", cv); if (deathClose) inc("deathCloseSilent", deathClose); }
    }
    for (const p of pre){
      const { f, Z } = p, t1 = p.t0 + dt;
      if (Z.t !== t1) fail(1, `the window clock ${p.t0} -> ${Z.t}`);
      const T = f.sightTally, Tn = JSON.stringify(Object.assign({}, T, { frames: 0, foeHex: 0 }));
      if (Tn !== p.T) fail(6, "tickSight moved the tally's other counts");
      if (t1 >= Z.dur || !p.fA || !p.oA){
        if (f.ultSight) fail(1, "the window did not close");
        else if (T.frames !== p.fr) fail(1, "a closing frame counted");
        else if (t1 >= Z.dur && p.fA && p.oA) inc("clockCloses");
        else inc("deathCloses");
        continue;
      }
      if (f.ultSight !== Z) fail(1, `closed at ${t1} of ${Z.dur}, both alive`);
      else if (T.frames !== p.fr + 1 || T.foeHex !== p.fh + p.stk) fail(1, "the tally's frame count");
      else { inc("winOk"); if (per){ per.wf++; per.wstk += p.stk; } }
    }
    for (const f of [this.a, this.b]) if (isO(f))
      lastZ.set(f, f.ultSight ? [f.ultSight, f.ultSight.t, f.ultSight.dur] : null);
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "oracle");
  const T = { casts: 0, frames: 0, foeHex: 0, arrows: 0, hex: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, ain = 0, aout = 0, fStk = 0, time = 0, liveOut = 0;
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), the sim read before and after each
     frame; each drawn fight's end is kept and replayed undrawn below. The
     post chain is off: this asks what a draw WRITES, not what it looks like
     (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0, drawnEnds = [];
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "oracle", sd) : new AC.Match("oracle", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0, ain: 0, aout: 0, wf: 0, wstk: 0 };
    voices.length = 0;
    const drawn = drawOn && sd === seeds[0];
    let steps = 0, live = 0, liveWin = 0;
    while (!m.over && steps < 160 / DT){
      const froz = m.hitStop > 0 || !!m.latch || !!m.splitHold, open = !!me.ultSight;
      m.step(DT); steps++;
      if (!froz){ live++; if (open) liveWin++; }
      if (drawn){
        const vis = [m.a, m.b].some(q => q.foreFade > 0 || (q.foreFx && q.foreFx.length));
        if (vis ? steps % drawEvery === 0 : steps % 60 === 0){
          const s0 = psnap(m);
          try { AC.__draw(m); } catch (e){ fail(9, "a drawn frame threw: " + String((e && e.message) || e)); }
          const s1 = psnap(m);
          if (s1 !== s0) fail(9, "a drawn frame changed the sim: " + firstDiff(s0, s1));
          else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && me.foreFade > 0 && me.foreFade < 1) inc("drawFade");
                 if (vis && m.hitStop > 0) inc("drawPicStop"); }
        }
      }
    }
    if (drawn) drawnEnds.push([side, fid, sd, steps, psnap(m)]);
    fights++; bin += per.in; bout += per.out; ain += per.ain; aout += per.aout;
    fStk += per.wf ? per.wstk / per.wf : 0; time += steps * DT; liveOut += (live - liveWin) * DT;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.sightTally) for (const k in T) T[k] += me.sightTally[k];
  }
  P.step = oStep; P.tickWeapon = oWeap; P.tickFire = oFire; P.tickCharge = oCharge; P.fireUlt = oUlt;
  P.resolveHit = oResolve; P.tickSight = oSight;
  if (stage6p) P.tickForesight = oFore;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY ORACLE VOICE OF THE RUN, ACCOUNTED FOR by its event */
    const want = { "oracle": n.castVoice || 0, "oracle-sigil": n.sigilVoice || 0, "oracle-hex": n.hexVoice || 0, "oracle-close": n.closeVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(orAll)]))
      if ((orAll[k] || 0) !== (want[k] || 0)) fail(8, `${orAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  /* each drawn fight, replayed UNDRAWN with every hook off: it must end where the drawn one did */
  for (const [side, fid, sd, steps0, end] of drawnEnds){
    const m = side ? new AC.Match(fid, "oracle", sd) : new AC.Match("oracle", fid, sd);
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    if (steps !== steps0 || psnap(m) !== end) fail(9, `a drawn fight (${side ? fid + " v oracle" : "oracle v " + fid} ${sd}) ends apart from its undrawn replay`);
    else inc("drawnEndOk");
  }
  const u = AC.WEAPONS.find(w => w.id === "oracle");
  return { n, bad, T, fights, stage6v, stage6p, drawOn, orAll, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           arrowsIn: ain / fights, arrowsOut: aout / fights, fStk: fStk / fights, meanDur: time / fights, liveOut,
           u: { dmg: u.dmg, charge: u.ult.charge, dur: u.ult.dur, turn: u.ult.turn, hex: u.ult.hex } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickSight === 'function'"):
        raise SystemExit("no tickSight in this build -- not a Foresight link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, T["frames"])
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
lockF = max(1, n.get("lockFrames", 0))
unl = lockF - n.get("locked", 0)
out_windows = R["liveOut"] / 8.0
print(f"\nFORESIGHT PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Oracle both sides x every foe x {a.seeds} seeds)   {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight in / out of windows {R['blowsIn']:.2f} / {R['blowsOut']:.2f}"
      f"   (arrows {R['arrowsIn']:.2f} / {R['arrowsOut']:.2f})   Oracle win {R['win']:.1%}   mean {R['meanDur']:.1f}s")
print(f"  per cast: arrow hits {T['arrows']/casts:.2f}   blade blows in windows {n.get('bladeIn',0)/casts:.2f}   "
      f"second hexes {T['hex']/casts:.2f}   hex applied by window arrows {n.get('hexApplied',0)} for {n.get('arrowIn',0)} arrows")
print(f"  outside: {n.get('arrowOut',0)} arrows in {R['liveOut']:.0f}s of live time = {n.get('arrowOut',0)/max(1e-9,out_windows):.2f} "
      f"a window-equivalent (8s)   foe hex on a window frame {T['foeHex']/frames:.2f} pooled, {R['fStk']:.2f} per fight (the lab's f_foeStk)")
print(f"  THE LOCK (after 0.5s): {100*n.get('locked',0)/lockF:.1f}% of {n.get('lockFrames',0)} window frames within turn x dt of the lead;"
      f" of the {unl} not, {100*n.get('unlockedAfterJump',0)/max(1,unl):.0f}% within 0.6s of a jump in the foe's velocity (a bounce or a knock)")
print(f"  aim frames {n.get('aimFrames',0)} (stunned {n.get('aimStunned',0)}, held {n.get('aimHeld',0)})   shots in / out "
      f"{n.get('shotsIn',0)} / {n.get('shotsOut',0)}   clock closes {n.get('clockCloses',0)}  death closes {n.get('deathCloses',0)}   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  OWNERS: the charge as tickCharge left it on {n.get('chargeKeptOk',0)} entries, the cadence as tickFire left it on "
      f"{n.get('cdKeptOk',0)}, the window as the cast / tickSight left it on {n.get('winKeptOk',0)}; tickWeapon wrote only the "
      f"facing on {n.get('stillOk',0)} frames; one `ult` beat on {n.get('castBeatOk',0)} casts")
checks = [
    (1, "the window: dt a window-ticker frame, `dur` long, closes by its clock or either death; only the cast and tickSight write it; only Oracle carries ultSight",
        n.get("winOk", 0) > 0 and n.get("clockCloses", 0) > 0 and n.get("castOk", 0) > 0 and n.get("winKeptOk", 0) > 0),
    (2, "the aim: each window frame (stunned or not) theta + clamp(shortest angle to the lead, +-turn x dt); none in a hit stop; spin as ever outside",
        n.get("aimOk", 0) > 0 and n.get("spinOk", 0) > 0 and n.get("aimStunned", 0) > 0),
    (3, "the stream: tickFire untouched -- one shot along f.theta when the cadence runs out, in the window and out; none stunned; only tickFire moves the cadence",
        n.get("shotsIn", 0) > 0 and n.get("shotsOut", 0) > 0 and n.get("holdOk", 0) > 0 and n.get("cdKeptOk", 0) > 0),
    (4, "the arrow as ever: every blow's damage rebuilt exactly, its own stop and one beat, in the window and out",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
    (5, "the double hex: an arrow landing in a window applies the channel's hex and +hex (side letter); nothing on a blade blow or outside",
        (n.get("hexOk", 0) > 0 if U["hex"] else n.get("hexZeroOk", 0) > 0) and n.get("outOk", 0) > 0),
    (6, "nothing else: tickWeapon writes only the facing (every other field snapshotted); tickSight only its window and tally; no apply moves the stop",
        n.get("stillOk", 0) > 0 and n.get("winOk", 0) > 0),
    (7, "the cast: on the frame the charge reaches `charge` (nothing waits), never under an open window, one `ult` beat; the charge fills by dt and only tickCharge writes it",
        n.get("castDueOk", 0) > 0 and n.get("chargeOk", 0) > 0 and n.get("chargeKeptOk", 0) > 0 and n.get("castBeatOk", 0) > 0),
]
if R.get("stage6v"):
    snaps = " ".join(f"{i}:{n.get(f'snapN{i}', 0)}" for i in range(1, 6))
    print(f"  STAGE 6 VOICE: cast voices {n.get('castVoice',0)} for {T['casts']} casts; sigil strikes {n.get('sigilVoice',0)} "
          f"(window frames {T['frames']}); snaps {n.get('hexVoice',0)} for {T['hex']} second hexes (n {snaps}); "
          f"close voices {n.get('closeVoice',0)} for {n.get('clockCloses',0)} clock closes, none on {n.get('deathCloseSilent',0)} death closes; "
          f"the run's Oracle voices {R.get('orAll')}")
    checks.append((8, "stage 6 voice: one cast voice a cast; the sigil on the window's 1st, 9th, 17th... frame and no other; one snap a second hex at the foe's count; "
                      "one close voice a clock close and none on a death; every Oracle voice accounted for",
                   n.get("castVoice", 0) > 0 and n.get("sigilVoice", 0) > 0 and n.get("hexVoice", 0) > 0
                   and n.get("closeVoice", 0) > 0 and n.get("deathCloseSilent", 0) > 0))
if R.get("stage6p"):
    tags = " ".join(f"{i}:{n.get(f'tagN{i}', 0)}" for i in range(1, 6))
    print(f"  STAGE 6 PICTURE: tickForesight calls with the sim untouched {n.get('foreOk',0)}; the eye at 1 on {n.get('fadeOpenOk',0)} open-window "
          f"ticks, shut after {n.get('eyeShut',0)} closes; flares {n.get('flareOk',0)} (killing arrows, no flare: {n.get('killNoFlare',0)}); "
          f"HEX tags carrying the count {n.get('tagOk',0)} ({tags})")
    print(f"    drawn subset: {n.get('drawOk',0)} frames through the renderer ({n.get('drawPic',0)} with the picture up, "
          f"{n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawFade',0)} with the eye opening or shutting); "
          f"drawn fights ending where their undrawn replay does: {n.get('drawnEndOk',0)}" + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((9, "stage 6 picture: tickForesight writes no sim field and draws no RNG; the eye at 1 through every open window and never rising outside; "
                      "one flare a landed window arrow on a live foe; a HEX tag carrying the count on each second hex; no drawn frame throws or writes the sim",
                   n.get("foreOk", 0) > 0 and n.get("fadeOpenOk", 0) > 0 and n.get("eyeShut", 0) > 0 and n.get("flareOk", 0) > 0
                   and n.get("tagOk", 0) > 0 and (n.get("drawPic", 0) > 0 and n.get("drawnEndOk", 0) > 0 if R.get("drawOn") else True)))
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
