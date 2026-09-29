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
      outlives either death, or any relic but Oracle carrying `ultSight`
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
      (+cadence on a shot)
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
  [6] NOTHING ELSE: tickWeapon moving a ball; tickSight writing anything but
      the window and its tally
  [7] THE CAST ("nothing waits"): a frame whose charge reached `charge` with
      the bow alive and no cast, a cast below it, or a cast while a window runs
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
a = ap.parse_args()

JS = r"""([seeds]) => {
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
    const body = [f.x, f.y, f.vx, f.vy, foe.x, foe.y, foe.vx, foe.vy];
    const spinMul = f.spinMul(this.actMods.spin), spinDir = f.spinDir;
    const r = oWeap.call(this, f, foe, dt);
    const body1 = [f.x, f.y, f.vx, f.vy, foe.x, foe.y, foe.vx, foe.vy];
    if (body1.some((v, i) => v !== body[i])) fail(6, "tickWeapon moved a ball"); else inc("stillOk");
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
    const r = oFire.call(this, f, foe, dt);
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
    const r = oCharge.call(this, f, foe, dt);
    const cast = f.ultsFired - u0;
    if (live){
      const due = c0 + dt >= f.w.ult.charge;
      if (due && cast !== 1) fail(7, `charge ${c0 + dt} reached ${f.w.ult.charge} with no cast (window ${open})`);
      else if (!due && cast) fail(7, `a cast at charge ${c0 + dt}`);
      else if (cast){ if (f.charge !== 0) fail(7, "the charge not spent"); else inc("castDueOk"); }
      else inc("chargeOk");
    } else if (cast) fail(7, "a cast from a dead bow or an ended match");
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isO(f)) return oUlt.call(this, f, foe);
    if (f.ultSight) fail(7, "a cast under an open window");
    const c0 = f.sightTally ? f.sightTally.casts : 0;
    const r = oUlt.call(this, f, foe);
    const Z = f.ultSight;
    if (!Z || Z.t !== 0 || Z.dur !== f.w.ult.dur || Object.keys(Z).length !== 2 || f.sightTally.casts !== c0 + 1)
      fail(1, `the cast opened ${JSON.stringify(Z)}`);
    else inc("castOk");
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
    const oApply = foe.apply, M = this;
    foe.apply = function(k, nn, src){ const h = M.hitStop; applies.push([k, nn, src]); const rr = oApply.call(this, k, nn, src);
      if (M.hitStop !== h) fail(6, "an apply moved the hit stop"); return rr; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; delete this.beat; delete foe.apply; }
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
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "pin", "pinMax", "pinFree",
              "reachMul", "hits", "dealt", "crits", "spinDir", "fireCd", "ultsFired", "burden"];
  const snap = (m) => { const o = [m.t, m.hitStop, m.over, m.shots.length];
    for (const f of [m.a, m.b]){ for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t, f.status[k].src])); }
    return JSON.stringify(o); };
  P.tickSight = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultSight && !isO(f)) fail(1, `${f.w.id} carries ultSight`);
      if (!f.ultSight) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z: f.ultSight, t0: f.ultSight.t, fA: f.alive, oA: foe.alive, fr: f.sightTally.frames, fh: f.sightTally.foeHex,
                 stk: foe.stacks("hex"), T: JSON.stringify(Object.assign({}, f.sightTally, { frames: 0, foeHex: 0 })) });
    }
    const s0 = snap(this);
    const r = oSight.call(this, dt);
    if (snap(this) !== s0) fail(6, "tickSight changed the sim");
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
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "oracle");
  const T = { casts: 0, frames: 0, foeHex: 0, arrows: 0, hex: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, ain = 0, aout = 0, fStk = 0, time = 0, liveOut = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "oracle", sd) : new AC.Match("oracle", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0, ain: 0, aout: 0, wf: 0, wstk: 0 };
    let steps = 0, live = 0, liveWin = 0;
    while (!m.over && steps < 160 / DT){
      const froz = m.hitStop > 0 || !!m.latch || !!m.splitHold, open = !!me.ultSight;
      m.step(DT); steps++;
      if (!froz){ live++; if (open) liveWin++; }
    }
    fights++; bin += per.in; bout += per.out; ain += per.ain; aout += per.aout;
    fStk += per.wf ? per.wstk / per.wf : 0; time += steps * DT; liveOut += (live - liveWin) * DT;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.sightTally) for (const k in T) T[k] += me.sightTally[k];
  }
  P.step = oStep; P.tickWeapon = oWeap; P.tickFire = oFire; P.tickCharge = oCharge; P.fireUlt = oUlt;
  P.resolveHit = oResolve; P.tickSight = oSight;
  const u = AC.WEAPONS.find(w => w.id === "oracle");
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           arrowsIn: ain / fights, arrowsOut: aout / fights, fStk: fStk / fights, meanDur: time / fights, liveOut,
           u: { dmg: u.dmg, charge: u.ult.charge, dur: u.ult.dur, turn: u.ult.turn, hex: u.ult.hex } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickSight === 'function'"):
        raise SystemExit("no tickSight in this build -- not a Foresight link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
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
checks = [
    (1, "the window: dt a window-ticker frame, `dur` long, closes by its clock or either death; only Oracle carries ultSight",
        n.get("winOk", 0) > 0 and n.get("clockCloses", 0) > 0 and n.get("castOk", 0) > 0),
    (2, "the aim: each window frame (stunned or not) theta + clamp(shortest angle to the lead, +-turn x dt); none in a hit stop; spin as ever outside",
        n.get("aimOk", 0) > 0 and n.get("spinOk", 0) > 0 and n.get("aimStunned", 0) > 0),
    (3, "the stream: tickFire untouched -- one shot along f.theta when the cadence runs out, in the window and out; none stunned",
        n.get("shotsIn", 0) > 0 and n.get("shotsOut", 0) > 0 and n.get("holdOk", 0) > 0),
    (4, "the arrow as ever: every blow's damage rebuilt exactly, its own stop and one beat, in the window and out",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
    (5, "the double hex: an arrow landing in a window applies the channel's hex and +hex (side letter); nothing on a blade blow or outside",
        (n.get("hexOk", 0) > 0 if U["hex"] else n.get("hexZeroOk", 0) > 0) and n.get("outOk", 0) > 0),
    (6, "nothing else: tickWeapon moves no ball; tickSight writes only its window and tally; no apply moves the stop",
        n.get("stillOk", 0) > 0 and n.get("winOk", 0) > 0),
    (7, "the cast: on the frame the charge reaches `charge` (nothing waits), never under an open window",
        n.get("castDueOk", 0) > 0 and n.get("chargeOk", 0) > 0),
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
