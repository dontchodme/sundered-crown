# SCRATCH CONTROL: the probe as it was before review round 2 (sha16 960863fbcb56a4c4): [1] counted tickDrain calls only; [5] read the foe's bleed ceiling back from the engine
#!/usr/bin/env python
"""EXSANGUINATE'S PROBE (v106) -- one check per sentence of v76 §1 / §4 / §5,
read INSIDE the hooks.

    python widowmaker_probe.py --game ../02-chain/sc-widowmaker-drain.html

Wraps `step`, `fireUlt`, `tickStatus`, `tickDrain` and `resolveHit` on the
Match prototype and reads each event where it happens. Runs Widowmaker against
every other relic, both sides, and prints N/N. The same probe gates every
stage from 2 on (the drain, the blade).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration": a window that is not `dur` long on the window clock
      (a clock close after exactly the steps whose dt sum first reaches
      `dur`), that outlives either death, or any relic but Widowmaker carrying
      `ultDrain`
  [2] "Every tick of Hemorrhage on the enemy heals her by the same amount": a
      hemorrhage tick on her opponent, inside her window, with both alive and
      her short of the cap by more than the tick, whose heal is not exactly d,
      where d = dps x stacks x dt x dmgTakenMul is REBUILT from the engine's
      own loop (the status keys in order, each expiry, every dps tick before
      it, the blessing, and the dmgTakenMul each tick actually read: the heal
      must pay back the tick as dealt)
  [3] "capped at maxHp": a drain tick that would carry her past maxHp leaving
      her anywhere but exactly maxHp, or her maxHp moving (the cap does not
      lift: v76 §6.3 leaves that out)
  [4] outside her window nothing drains: any change to her hp in a status
      tick of her foe's with the window shut, in a shade's status tick, or on
      a tick of a fighter already dead -- and the foe's own tick changed (the
      foe's hp rebuilt exactly in every status tick, each dps tick at Sunder's
      DEFINITION, 1 + taken x stacks, not the engine's dmgTakenMul)
  [5] "Her blades are unchanged": a Widowmaker blow whose damage is not the
      blade x dmgMul x jitter x dmgTaken, rounded, crit included, rebuilt from
      the captured draws, in the window and out of it; or whose onHit is not
      hemorrhage +2 to the cap, as ever. Every factor is REBUILT FROM ITS
      DEFINITION, never read back from the engine's methods: the blade from
      the row as loaded, the act's dmg and desperation (1.35 at or under 25%
      of her maxHp) for dmgMul, Sunder's 1 + taken x stacks for dmgTaken, the
      crit from its own draw against critChance (and the engine's crit count
      must agree), the jitter from its draw
  [6] "No damage change, no knock, no stun" at the cast: the cast changing the
      foe's hp, shield, velocity, stun, pin or any status, or her own hp; a stop
      other than the cast's common 0.08; a window that is not {t 0, dur}
  [7] "the drain files none", hp and nothing else: a status tick in which she
      drained that files any beat but the engine's own fatal-tick beat, stops
      the world, floats a number, or gives her any status (Blessing is not used)
  [8] a cast while her window is open
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
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
  /* the constants every multiplier is rebuilt from, read once before any fight */
  const ACTS = C.acts, DESP = C.desperation, SUNT = ST.sunder.taken;
  const BLADE = AC.WEAPONS.find(w => w.id === "widowmaker").dmg;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oStep = P.step, oFire = P.fireUlt, oStat = P.tickStatus, oDrain = P.tickDrain, oResolve = P.resolveHit;
  const isW = f => f && f.w && f.w.id === "widowmaker";
  const U = AC.WEAPONS.find(w => w.id === "widowmaker").ult;
  let nClock = 0; { let t = 0; while (t < U.dur){ t += DT; nClock++; } }
  const live = new WeakMap();       // window -> tickDrain increments (the window clock)
  const mt = new WeakMap();         // window -> steps of match time
  let per = null;

  P.step = function(dt){
    for (const f of [this.a, this.b]){
      if (f.ultDrain && !isW(f)) fail(1, `${f.w.id} carries ultDrain`);
      if (isW(f) && f.ultDrain){ inc("winSteps"); mt.set(f.ultDrain, (mt.get(f.ultDrain) || 0) + 1);
        if (this.hitStop > 0 || this.latch || this.splitHold) inc("winFrozen"); }
    }
    return oStep.call(this, dt);
  };

  P.fireUlt = function(f, foe){
    if (!isW(f)) return oFire.call(this, f, foe);
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
        inc("closes");
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
    let hp = f0, wh = W0, mi = 0, drains = 0, capped = 0, killBeat = false, bleedTicks = 0;
    for (const k of keys){
      const s = snap[k], def = ST[k];
      let t = s.t; if (!(k === "ward" && f.ultDraw)) t -= dt;
      if (t <= 0) continue;
      if (def.dps && k !== "blessing"){
        const hp0 = hp, d = def.dps * s.stacks * dt * muls[mi], dDef = def.dps * s.stacks * dt * defs[mi];
        mi++;
        hp -= dDef;
        if (hp0 > 0 && hp <= 0) killBeat = true;
        if (k === "hemorrhage"){
          bleedTicks++;
          if (open && Walive && hp0 > 0 && (!s.src || s.src === (W === this.a ? "a" : "b"))){
            if (wh + d > Wmax0){ capped++; wh = Wmax0; } else wh = wh + d;
            drains++;
          }
        }
      }
      if (k === "blessing") hp = Math.min(f.maxHp, hp + def.hps * s.stacks * dt);
    }
    hp = Math.min(hp, f.maxHp);
    if (W.maxHp !== Wmax0) fail(3, `her maxHp ${Wmax0} -> ${W.maxHp} in a status tick (the cap does not lift)`);
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
                  curse: foe.stacks("curse"), bl: foe.stacks("hemorrhage"), cap: foe.bleedCap };
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
    const bl = foe.stacks("hemorrhage"), wantBl = pre.bl < pre.cap ? Math.min(pre.cap, pre.bl + 2) : pre.bl;
    if (!foe.shade){ if (bl !== wantBl) fail(5, `onHit: hemorrhage ${pre.bl} -> ${bl}, want ${wantBl}`); else inc("onHitOk"); }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "widowmaker");
  const T = { casts: 0, frames: 0, foeStk: 0, ticks: 0, drained: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0; const lens = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "widowmaker", sd) : new AC.Match("widowmaker", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0, winLen: [] };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out; lens.push(...per.winLen);
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.drainTally) for (const k in T) T[k] += me.drainTally[k];
  }
  P.step = oStep; P.fireUlt = oFire; P.tickStatus = oStat; P.tickDrain = oDrain; P.resolveHit = oResolve;
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, nClock,
           u: { charge: U.charge, dur: U.dur, kind: U.kind }, blade: AC.WEAPONS.find(w => w.id === "widowmaker").dmg };
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
      f"(Widowmaker both sides x every foe x {a.seeds} seeds)   ult {U}  blade {R['blade']}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Widowmaker win {R['win']:.1%}")
print(f"  per cast: drained {T['drained']/casts:.2f} hp (the tally; hp deltas {n.get('drained',0)/casts:.2f})   "
      f"drain ticks {T['ticks']/casts:.0f}   foe stacks on a window frame {T['foeStk']/frames:.2f}   "
      f"ticks at the cap {100*n.get('cappedTicks',0)/max(1,n.get('drainTicks',0)):.1f}%")
print(f"  window: {R['nClock']} steps of the window clock ({R['nClock']/120:.3f}s); match time a window "
      f"{n.get('clockMatchSteps',0)/max(1,n.get('clockOk',0))/120:.2f}s (a clock close)   closes: {n.get('clockOk',0)} by the clock, {n.get('deathClose',0)} on a death   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  bleed ticks that drained nothing: {n.get('shutBleedOk',0)} window shut, {n.get('shadeBleedOk',0)} a shade's, "
      f"{n.get('deadBleedOk',0)} a dead foe's   blows exempt (aegis/curse) {n.get('blowExempt',0)}")
drain_cover = n.get("drainOk", 0) > 0
checks = [
    (1, "the window is `dur` on the window clock, closes on either death; only Widowmaker carries ultDrain",
        n.get("clockOk", 0) > 0 and n.get("deathClose", 0) > 0),
    (2, "every hemorrhage tick on her live foe in the window heals her by exactly d, rebuilt from the engine's loop",
        drain_cover and n.get("drainTicks", 0) > 0),
    (3, "capped at maxHp: a tick that would carry her past it leaves her exactly at maxHp", n.get("capOk", 0) > 0 and n.get("cappedTicks", 0) > 0),
    (4, "nothing drains with the window shut, from a shade or a corpse; the foe's own tick untouched",
        n.get("shutBleedOk", 0) > 0 and n.get("footTickOk", 0) > 0),
    (5, "every blow the twinblade's own, rebuilt exactly from the definitions, in the window and out; onHit hemorrhage +2",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("onHitOk", 0) > 0),
    (6, "the cast: no damage, knock, stun or status; the common 0.08 stop only; a window {t 0, dur}",
        n.get("castClean", 0) > 0),
    (7, "a drain tick: no beat but the fatal tick's own, no stop, no float, no status on her",
        n.get("nothingElseOk", 0) > 0),
    (8, "no cast while her window is open", n.get("castOk", 0) > 0),
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
