#!/usr/bin/env python
"""EXSANGUINATE'S PROBE (v106) -- one check per sentence of v76 §1 / §2 / §4 /
§5 / §6.3, read INSIDE the hooks.

    python widowmaker_probe.py --game ../02-chain/sc-widowmaker-drain.html

Wraps `step`, `fireUlt`, `tickStatus`, `tickDrain` and `resolveHit` on the
Match prototype and reads each event where it happens. Runs Widowmaker against
every other relic, both sides, and prints N/N. The same probe gates every
stage from 2 on (the drain, the blade).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration", ON THE WINDOW TICKERS' CLOCK (the standing ruling:
      every window cadence runs on the clock that stops in a hit stop):
      - a FROZEN step (hitStop > 0, the latch or the split, read on entry)
        that moves the window at all: another object, opened or closed, or
        its clock `t` changed;
      - a LIVE step with the window open whose clock does not move by exactly
        dt (closing it or not; the cast's own step is [6]'s and [8]'s);
      - a clock close after any number of window steps but exactly the ones
        whose dt sum first reaches `dur`;
      - a death that `tickDrain` sees and does not close on;
      - a window unaccounted for: every cast is a clock close, a death close,
        or a window still set when the match ends (a kill landed after
        `tickDrain` in the last step -- `step` runs no ticker after `over` --
        or the timeout); those are counted, not failed;
      - any relic but Widowmaker carrying `ultDrain`
  [2] "Every tick of Hemorrhage on the enemy heals her by the same amount": a
      hemorrhage tick on her opponent, inside her window, with both alive and
      her short of the cap by more than the tick, whose heal is not exactly d,
      where d = dps x stacks x dt x dmgTakenMul is REBUILT from the engine's
      own loop (the status keys in order, each expiry, every dps tick before
      it, the blessing, and the dmgTakenMul each tick actually read: the heal
      must pay back the tick as dealt)
  [3] "capped at `maxHp`" (v76 §2: the drain "heals `hp` by it, capped at
      `maxHp`"; §4: `min(src.maxHp, ...)`): a drain tick that would carry her
      past maxHp leaving her anywhere but exactly maxHp, or her maxHp moving
      in a status tick
  [4] outside her window nothing drains: any change to her hp in a status
      tick of her foe's with the window shut, in a shade's status tick, or on
      a tick of a fighter already dead -- and the foe's own tick changed (the
      foe's hp rebuilt exactly in every status tick, each dps tick at Sunder's
      DEFINITION, 1 + taken x stacks, not the engine's dmgTakenMul)
  [5] "Her blades are unchanged": a Widowmaker blow whose damage is not the
      blade x dmgMul x jitter x dmgTaken, rounded, crit included, rebuilt from
      the captured draws, in the window and out of it; or, on a blow where the
      bleed ceiling cannot bind (stacks before + the row's onHit <= 4), an
      onHit that does not add exactly the row's hemorrhage 2 (where the
      ceiling binds, the stacks are [9]'s). Every factor is REBUILT FROM ITS
      DEFINITION, never read back from the engine's methods: the blade and the
      onHit from the row as loaded, the act's dmg and desperation (1.35 at or
      under 25% of her maxHp) for dmgMul, Sunder's 1 + taken x stacks for
      dmgTaken, the crit from its own draw against critChance (and the
      engine's crit count must agree), the jitter from its draw
  [6] "No damage change, no knock, no stun" at the cast: the cast changing the
      foe's hp, shield, velocity, stun, pin or any status, or her own hp; a stop
      other than the cast's common 0.08; a window that is not {t 0, dur}
  [7] "the drain files none", hp and nothing else: a status tick in which she
      drained that files any beat but the engine's own fatal-tick beat (at
      most one, and only when the foe's hp crossed 0 in that tick), stops the
      world, floats a number, or gives her any status (Blessing is not used)
  [8] a cast while her window is open
  [9] §6.3, "left out": the drain does NOT also lift "her own cap
      (Bloodletting's 8)" -- the hemorrhage STACK ceiling, the bleeding
      fighter's `bleedCap`. Rebuilt from its definition: her foe's ceiling is
      `STATUS.hemorrhage.maxStacks` (4) unless a Bloodletting spectre of HERS
      stands, and none can. Evidence: the foe's `bleedCap` anything else after
      any step or at any blow of hers, window open or shut; or a blow where the
      ceiling binds (stacks before + 2 > 4) leaving the foe anywhere but 4 (or
      where it was, at or above 4)
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")   # scratch copy of the round-2 probe (912e8e4f6bad3545), path fixed
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=101001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, ST = AC.STATUS;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, critCh = C.chaos.critChance, FP = Object.getPrototypeOf(new AC.Match("widowmaker", "axiom", 1).a);
  const oDTM = FP.dmgTakenMul;
  /* the constants every multiplier and ceiling is rebuilt from, read once before any fight */
  const ACTS = C.acts, DESP = C.desperation, SUNT = ST.sunder.taken;
  const ROW = AC.WEAPONS.find(w => w.id === "widowmaker");
  const BLADE = ROW.dmg, ONHIT = ROW.onHit.hemorrhage, HB = ST.hemorrhage.maxStacks;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oStep = P.step, oFire = P.fireUlt, oStat = P.tickStatus, oDrain = P.tickDrain, oResolve = P.resolveHit;
  const isW = f => f && f.w && f.w.id === "widowmaker";
  const U = ROW.ult;
  let nClock = 0; { let t = 0; while (t < U.dur){ t += DT; nClock++; } }
  const live = new WeakMap();       // window -> tickDrain increments (the window clock)
  const mt = new WeakMap();         // window -> steps of match time
  let per = null, castStep = 0;

  P.step = function(dt){
    for (const f of [this.a, this.b]) if (f.ultDrain && !isW(f)) fail(1, `${f.w.id} carries ultDrain`);
    const W = isW(this.a) ? this.a : isW(this.b) ? this.b : null;
    if (!W) return oStep.call(this, dt);
    const foe = W === this.a ? this.b : this.a;
    /* [1] THE WINDOW TICKERS' CLOCK: the step's path, and the window and its
       clock as they stood, read on entry (step() takes the latch, the split
       and the hit stop in that order, each returning before any ticker). */
    const frozen = !this.over && (this.hitStop > 0 || !!this.latch || !!this.splitHold);
    const liveStep = !this.over && !frozen;
    const z0 = W.ultDrain, zt0 = z0 ? z0.t : null;
    if (z0 && !this.over){ inc("winSteps"); mt.set(z0, (mt.get(z0) || 0) + 1); if (frozen) inc("winFrozen"); }
    castStep = 0;
    const r = oStep.call(this, dt);
    if (frozen){
      /* a frozen step leaves the window exactly as it was: the same object,
         the clock not moved, nothing opened or closed */
      if (W.ultDrain !== z0 || (z0 && z0.t !== zt0))
        fail(1, `a frozen step moved the window: t ${zt0} -> ${W.ultDrain ? W.ultDrain.t : null}${W.ultDrain !== z0 ? " (opened/closed)" : ""}`);
      else if (z0) inc("winHeldFrozen");
    } else if (liveStep && z0 && !castStep){
      /* a live step with the window open moves its clock by exactly dt */
      if (z0.t !== zt0 + dt) fail(1, `a live step moved the window's clock by ${z0.t - zt0}, want ${dt}`);
      else if (W.ultDrain === z0) inc("winLiveAdv");
      else if (W.ultDrain === null) inc("winLiveClose");
      else fail(1, "a live step replaced an open window");
    }
    /* [9] THE FOE'S BLEED CEILING, after every step: hemorrhage's own, which
       only a standing spectre of hers could raise, and she has none */
    if (foe.bleedCap !== HB) fail(9, `the foe's bleed ceiling is ${foe.bleedCap} after a step (her window ${W.ultDrain ? "open" : "shut"}), want hemorrhage's ${HB}`);
    else inc(W.ultDrain ? "ceilStepIn" : "ceilStepOut");
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isW(f)) return oFire.call(this, f, foe);
    castStep++; if (per) per.casts++;
    if (f.ultDrain) fail(8, `a cast with the window at ${f.ultDrain.t.toFixed(3)} of ${f.ultDrain.dur}`); else inc("castOk");
    const snap = x => ({ hp: x.hp, sh: x.shield, vx: x.vx, vy: x.vy, stun: x.stun, pin: x.pin,
                         st: JSON.stringify(Object.entries(x.status).map(([k, s]) => [k, s.stacks, s.t])) });
    const s0 = snap(foe), me0 = f.hp, hs0 = this.hitStop;
    const r = oFire.call(this, f, foe);
    const s1 = snap(foe);
    for (const k in s0) if (s0[k] !== s1[k]) fail(6, `the cast moved the foe's ${k}: ${s0[k]} -> ${s1[k]}`);
    if (f.hp !== me0) fail(6, "the cast moved her own hp");
    if (this.hitStop !== Math.max(hs0, 0.08)) fail(6, `hitStop ${hs0} -> ${this.hitStop}`);
    if (!f.ultDrain || f.ultDrain.t !== 0 || f.ultDrain.dur !== f.w.ult.dur) fail(6, "the cast did not open {t 0, dur}");
    else { inc("castClean"); live.set(f.ultDrain, 0); }
    return r;
  };

  P.tickDrain = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]) if (f.ultDrain){
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z: f.ultDrain, t1: f.ultDrain.t + dt, fa: f.alive, oa: foe.alive });
    }
    const r = oDrain.call(this, dt);
    for (const p of pre){
      const k = (live.get(p.Z) || 0) + 1; live.set(p.Z, k);
      const clock = p.t1 >= p.Z.dur, death = !p.fa || !p.oa;
      if (clock || death){
        if (p.f.ultDrain){ fail(1, "the window did not close"); continue; }
        inc("closes"); if (per) per.closes++;
        if (!death){ if (k !== nClock) fail(1, `a clock close after ${k} window steps, want ${nClock}`); else { inc("clockOk"); inc("clockMatchSteps", mt.get(p.Z) || 0); } }
        else inc("deathClose");
        if (per) per.winLen.push(k);
      } else {
        if (p.f.ultDrain !== p.Z){ fail(1, `closed at ${p.t1.toFixed(3)} of ${p.Z.dur} with both alive`); continue; }
        if (p.Z.t !== p.t1) fail(1, "the window clock is not t + dt");
        inc("winFrames");
      }
    }
    return r;
  };

  P.tickStatus = function(f, dt){
    const me = f === this.a ? this.b : f === this.b ? this.a : null;       // the drainer, if any
    const W = isW(this.a) ? this.a : isW(this.b) ? this.b : null;
    if (!W) return oStat.call(this, f, dt);
    const keys = Object.keys(f.status), snap = {};
    for (const k of keys) snap[k] = { stacks: f.status[k].stacks, t: f.status[k].t, src: f.status[k].src };
    const hasBleed = !!f.status.hemorrhage;
    const f0 = f.hp, W0 = W.hp, Wmax0 = W.maxHp, Wst0 = Object.keys(W.status).join(","), Wbless0 = W.status.blessing ? W.status.blessing.stacks : 0;
    const open = !!(me && me === W && W.ultDrain), Walive = W.hp > 0, hs0 = this.hitStop;
    const muls = [], defs = [], beats = [], floats = [], oBeat = this.beat, oFloat = this.float;
    /* each read of dmgTakenMul: the engine's value (the tick as dealt, which
       the drain must pay back) and Sunder's definition at the same instant
       (the tick as it must be: the foe's own hp is rebuilt from this one) */
    f.dmgTakenMul = function(){ const v = oDTM.call(this); muls.push(v);
      defs.push(1 + SUNT * (this.status.sunder ? this.status.sunder.stacks : 0)); return v; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.float = function(...x){ floats.push(x); return oFloat.apply(this, x); };
    let r;
    try { r = oStat.call(this, f, dt); }
    finally { delete f.dmgTakenMul; delete this.beat; delete this.float; }
    /* THE ENGINE'S LOOP, REBUILT: the keys in order, each expiry, every dps
       tick and the blessing. The foe's hp at Sunder's definition; the drain
       at the dmgTakenMul each dps tick actually read (the tick as dealt). */
    let hp = f0, hpD = f0, wh = W0, mi = 0, drains = 0, capped = 0, killBeat = false;
    for (const k of keys){
      const s = snap[k], def = ST[k];
      let t = s.t; if (!(k === "ward" && f.ultDraw)) t -= dt;
      if (t <= 0) continue;
      if (def.dps && k !== "blessing"){
        const hpD0 = hpD, d = def.dps * s.stacks * dt * muls[mi], dDef = def.dps * s.stacks * dt * defs[mi];
        mi++;
        hp -= dDef; hpD -= d;
        if (hpD0 > 0 && hpD <= 0) killBeat = true;
        if (k === "hemorrhage"){
          if (open && Walive && hpD0 > 0 && (!s.src || s.src === (W === this.a ? "a" : "b"))){
            if (wh + d > Wmax0){ capped++; wh = Wmax0; } else wh = wh + d;
            drains++;
          }
        }
      }
      if (k === "blessing"){ hp = Math.min(f.maxHp, hp + def.hps * s.stacks * dt); hpD = Math.min(f.maxHp, hpD + def.hps * s.stacks * dt); }
    }
    hp = Math.min(hp, f.maxHp);
    /* the engine's own fatal-tick beat is filed when the tick it dealt took the
       foe across 0 -- as rebuilt, or as it actually happened (a wrong tick is
       [4]'s, not a beat of the drain's) */
    if (f0 > 0 && f.hp <= 0) killBeat = true;
    if (W.maxHp !== Wmax0) fail(3, `her maxHp ${Wmax0} -> ${W.maxHp} in a status tick (the heal is capped at maxHp; nothing lifts it)`);
    if (mi !== muls.length) fail(4, `rebuilt ${mi} dps ticks, the engine read dmgTakenMul ${muls.length} times`);
    if (f.hp !== hp) fail(4, `the foe's tick: hp ${f0} -> ${f.hp}, rebuilt ${hp}`);
    else if (hasBleed) inc("footTickOk");
    if (drains){
      inc("drainTicks", drains); inc("drainCalls");
      if (capped){
        inc("cappedTicks", capped);
        if (W.hp !== Wmax0) fail(3, `a capped drain: her hp ${W0} -> ${W.hp}, maxHp ${Wmax0}`); else { inc("capOk"); inc("drained", W.hp - W0); }
      } else if (W.hp !== wh) fail(2, `drain: her hp ${W0} -> ${W.hp}, rebuilt ${wh}`); else { inc("drainOk"); inc("drained", W.hp - W0); }
      const others = beats.filter(b => !(b.fatal && b.tick && b.status));
      if (others.length) fail(7, `a drain tick filed ${others.length} beat(s)`);
      if (beats.length > 1) fail(7, `${beats.length} beats in one status tick`);
      if (beats.length && !killBeat) fail(7, "a beat with no killing tick");
      if (this.hitStop !== hs0) fail(7, `hitStop ${hs0} -> ${this.hitStop}`);
      if (floats.length) fail(7, `${floats.length} float(s) in a drain tick`);
      if (Object.keys(W.status).join(",") !== Wst0 || (W.status.blessing ? W.status.blessing.stacks : 0) !== Wbless0) fail(7, "her statuses changed in a drain tick");
      else inc("nothingElseOk");
    } else if (W !== f && W.hp !== W0){
      /* she was not drained on this call, so her hp must not move */
      fail(4, `her hp ${W0} -> ${W.hp} in ${me === W ? (open ? "an open window on a tick that owes nothing" : "a shut window") : "a shade's tick"}`);
    } else if (hasBleed && W !== f){
      if (me !== W) inc("shadeBleedOk"); else if (!open) inc("shutBleedOk"); else if (!(f0 > 0)) inc("deadBleedOk"); else inc("openNoTick");
    }
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isW(self) || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultDrain, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    /* THE MULTIPLIERS FROM THEIR DEFINITIONS, never from the engine's own
       methods (a change routed through `dmgMul`, `dmgTakenMul`, `desperate`
       or `actMods` would otherwise be read back as the truth): the act's dmg,
       desperation (alive and at or under `desperation.at` of her maxHp), and
       Sunder's `taken` per stack on the foe -- the constants read once, before
       any fight. */
    const desp = self.hp > 0 && self.hp / self.maxHp <= DESP.at;
    const pre = { dm: ACTS[this.act].dmg * (desp ? DESP.dmg : 1),
                  dt: 1 + SUNT * (foe.status.sunder ? foe.status.sunder.stacks : 0),
                  aegis: foe.w && foe.w.id === "bulwarden",
                  curse: foe.stacks("curse"), bl: foe.stacks("hemorrhage"), ceil: foe.bleedCap };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    const D = self.dealt - d0, crit = draws[0] < critCh;       // the crit from its draw, not the engine's count
    if (crit !== (self.crits > c0)) fail(5, `${open ? "IN" : "out of"} the window: the crit draw ${draws[0]} says ${crit}, the engine counted ${self.crits > c0}`);
    const raw = BLADE * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(5, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    if (!foe.shade){
      if (pre.ceil !== HB) fail(9, `her blow ${open ? "IN" : "out of"} the window: the foe's bleed ceiling ${pre.ceil}, want hemorrhage's ${HB}`);
      const bl = foe.stacks("hemorrhage");
      if (pre.bl + ONHIT <= HB){
        /* [5] the ceiling cannot bind: exactly the row's onHit */
        if (bl !== pre.bl + ONHIT) fail(5, `onHit: hemorrhage ${pre.bl} -> ${bl}, want +${ONHIT}`); else inc("onHitOk");
      } else {
        /* [9] the ceiling binds: hemorrhage's own, which the drain does not lift */
        const wantBl = pre.bl < HB ? HB : pre.bl;
        if (bl !== wantBl) fail(9, `onHit at the ceiling ${open ? "IN" : "out of"} the window: hemorrhage ${pre.bl} -> ${bl}, want ${wantBl}`);
        else inc(open ? "ceilBindIn" : "ceilBindOut");
      }
    }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "widowmaker");
  const T = { casts: 0, frames: 0, foeStk: 0, ticks: 0, drained: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0; const lens = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "widowmaker", sd) : new AC.Match("widowmaker", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0, winLen: [], casts: 0, closes: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out; lens.push(...per.winLen);
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.drainTally) for (const k in T) T[k] += me.drainTally[k];
    /* [1] EVERY WINDOW ACCOUNTED FOR: a clock close, a death close, or still set at the end */
    const still = me.ultDrain ? 1 : 0;
    if (per.casts !== per.closes + still) fail(1, `${per.casts} casts, ${per.closes} closes, ${still} still open at the end`);
    else inc("acctOk");
    if (still){
      if (m.over && m.reason === "slain") inc("openAtKill");
      else if (m.over) inc("openAtTimeout");
      else inc("openAtCap");
    }
  }
  P.step = oStep; P.fireUlt = oFire; P.tickStatus = oStat; P.tickDrain = oDrain; P.resolveHit = oResolve;
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, nClock, HB, ONHIT,
           u: { charge: U.charge, dur: U.dur, kind: U.kind }, blade: ROW.dmg };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickDrain === 'function'"):
        raise SystemExit("no tickDrain in this build -- not an Exsanguinate link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, T["frames"])
frozen = n.get("winFrozen", 0) / max(1, n.get("winSteps", 0))
print(f"\nEXSANGUINATE PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Widowmaker both sides x every foe x {a.seeds} seeds, seed0 {a.seed0})   ult {U}  blade {R['blade']}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Widowmaker win {R['win']:.1%}")
print(f"  per cast: drained {T['drained']/casts:.2f} hp (the tally; hp deltas {n.get('drained',0)/casts:.2f})   "
      f"drain ticks {T['ticks']/casts:.0f}   foe stacks on a window frame {T['foeStk']/frames:.2f}   "
      f"ticks at the cap {100*n.get('cappedTicks',0)/max(1,n.get('drainTicks',0)):.1f}%")
print(f"  window: {R['nClock']} steps of the window clock ({R['nClock']/120:.3f}s); match time a window "
      f"{n.get('clockMatchSteps',0)/max(1,n.get('clockOk',0))/120:.2f}s (a clock close)   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  the window clock: held on {n.get('winHeldFrozen',0)} frozen steps, moved by dt on "
      f"{n.get('winLiveAdv',0) + n.get('winLiveClose',0)} live steps ({n.get('winLiveClose',0)} of them closing)")
print(f"  {T['casts']} windows: {n.get('clockOk',0)} closed by the clock, {n.get('deathClose',0)} on a death tickDrain saw, "
      f"{n.get('openAtKill',0)} still set at `over` (a kill after tickDrain in the last step), "
      f"{n.get('openAtTimeout',0)} at the timeout, {n.get('openAtCap',0)} at the probe's cap")
print(f"  bleed ticks that drained nothing: {n.get('shutBleedOk',0)} window shut, {n.get('shadeBleedOk',0)} a shade's, "
      f"{n.get('deadBleedOk',0)} a dead foe's   blows exempt (aegis/curse) {n.get('blowExempt',0)}")
print(f"  the foe's bleed ceiling (hemorrhage's {R['HB']}): held after {n.get('ceilStepIn',0)} steps in windows and "
      f"{n.get('ceilStepOut',0)} outside; blows where it bound {n.get('ceilBindIn',0)} in windows, "
      f"{n.get('ceilBindOut',0)} outside; onHit +{R['ONHIT']} where it could not bind {n.get('onHitOk',0)}")
checks = [
    (1, "the window is `dur` on the window tickers' clock: held on every frozen step, dt on every live one; "
        "closes on a death tickDrain sees; every window accounted for; only Widowmaker carries ultDrain",
        n.get("clockOk", 0) > 0 and n.get("deathClose", 0) > 0 and n.get("winHeldFrozen", 0) > 0
        and n.get("winLiveAdv", 0) > 0 and n.get("winLiveClose", 0) > 0 and n.get("acctOk", 0) == R["fights"]),
    (2, "every hemorrhage tick on her live foe in the window heals her by exactly d, rebuilt from the engine's loop",
        n.get("drainOk", 0) > 0 and n.get("drainTicks", 0) > 0),
    (3, "capped at maxHp (§2): a tick that would carry her past it leaves her exactly at maxHp; maxHp never moves",
        n.get("capOk", 0) > 0 and n.get("cappedTicks", 0) > 0),
    (4, "nothing drains with the window shut, from a shade or a corpse; the foe's own tick untouched",
        n.get("shutBleedOk", 0) > 0 and n.get("footTickOk", 0) > 0),
    (5, "every blow the twinblade's own, rebuilt exactly from the definitions, in the window and out; onHit +2 where the ceiling cannot bind",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("onHitOk", 0) > 0),
    (6, "the cast: no damage, knock, stun or status; the common 0.08 stop only; a window {t 0, dur}",
        n.get("castClean", 0) > 0),
    (7, "a drain tick: no beat but the fatal tick's own, no stop, no float, no status on her",
        n.get("nothingElseOk", 0) > 0),
    (8, "no cast while her window is open", n.get("castOk", 0) > 0),
    (9, "the drain lifts no cap (§6.3): the foe's bleed ceiling is hemorrhage's own 4 after every step and at every blow, "
        "and a blow at the ceiling stops there",
        n.get("ceilStepIn", 0) > 0 and n.get("ceilStepOut", 0) > 0 and n.get("ceilBindIn", 0) > 0),
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
