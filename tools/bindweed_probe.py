#!/usr/bin/env python
"""TENDRIL'S PROBE -- one check per sentence of v68 §1 / §4-§7 and the brief's §0-§1,
read INSIDE the hooks.

    python bindweed_probe.py --game ../02-chain/sc-tendril.html

Wraps `tickWeapon`, `tickTendril`, `resolveHit`, `fireUlt` and `step` on the
Match prototype and reads each event where it happens. Runs Bindweed against
every other relic, both sides, and prints N/N. The checks follow the link's
own numbers, so the same probe gates stages 2-4 (bites 0 / on, root 0 / 0.3).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] a window that is not `dur` long on the window clock, that outlives
      either death, or any relic but Bindweed carrying `ultVine`
  [2] "it turns toward the enemy": a window frame whose facing is not exactly
      theta + clamp(shortest angle to the foe, +-turn x dt), stunned or not, or
      whose drive is not 0 (the head's tumble rebuilt with drive 0); outside the
      window, a facing that did not advance by spin as ever
  [3] "grows until it reaches them ... draws back in": reachMul not moving
      exactly `grow` x dt toward clamp((d - R) / (reach x mods.reach), 1, cap),
      never past it; not 1 after the close
  [4] "still a flail head, still hitting like one": a blow of Bindweed's whose
      damage is not the blade x dmgMul x jitter x dmgTaken, rounded, crit
      included -- rebuilt from the captured draws, in the window and out of it
  [5] "anywhere the vine touches them it bites, over and over": a bite without
      the foe's centre inside R + vineW of the pivot -> head segment, two bites
      closer than biteCd, or a clear touching frame without a bite
  [6] "a small hit that leaves entangle": not exactly hurt(foe, biteDmg, the
      caster) once and entangle +bitePer with a side letter; applications !=
      bites; a bite that moved the foe or stopped the world (a ward's own
      shatter aside)
  [7] a killing bite without exactly one fatal beat, or a beat from any other
      bite or frame
  [8] "the thorns take root": at a clock close with both alive and stacks n,
      not pin = max(pin, rootPer x n), pinMax likewise, pinV captured iff the
      hold was not already longer, pinFree untouched; any root at a death close
  [9] a cast while a vine hunts or withers; a close that does not leave `wither`
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=101001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const clampf = (v, lo, hi) => v < lo ? lo : v > hi ? hi : v;
  const seg = (ax, ay, bx, by, px, py) => { const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    let t = l2 > 0 ? ((px - ax) * dx + (py - ay) * dy) / l2 : 0; t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (ax + t * dx), py - (ay + t * dy)); };
  const oTick = P.tickTendril, oWeap = P.tickWeapon, oResolve = P.resolveHit, oFire = P.fireUlt, oStep = P.step;
  const lastBite = new WeakMap();
  let per = null;

  P.step = function(dt){
    for (const f of [this.a, this.b]) if (f.ultVine){ if (this.hitStop > 0) inc("winFrozen"); else inc("winLive"); }
    return oStep.call(this, dt);
  };
  P.fireUlt = function(f, foe){
    if (f.w.id === "bindweed"){
      if (f.ultVine) fail(9, "cast while a vine hunts");
      else if (f.vineWither > 0) fail(9, `cast with ${f.vineWither.toFixed(3)}s of wither left`);
      else inc("castOk");
    }
    return oFire.call(this, f, foe);
  };
  P.tickWeapon = function(f, foe, dt){
    if (!f.w || f.w.id !== "bindweed") return oWeap.call(this, f, foe, dt);
    const V = f.ultVine, th0 = f.theta, stun = f.stun, fx = foe.x, fy = foe.y, fAlive = foe.alive, hs0 = f.headSpin;
    const spinMul = f.spinMul(this.actMods.spin), spinDir = f.spinDir;
    const r = oWeap.call(this, f, foe, dt);
    if (V){
      inc("seekFrames"); if (stun > 0) inc("seekStunned");
      let want = th0;
      if (fAlive){
        const w = Math.atan2(fy - f.y, fx - f.x);
        const dl = Math.atan2(Math.sin(w - th0), Math.cos(w - th0));
        const k = f.w.ult.turn * dt;
        want = th0 + clampf(dl, -k, k);
      }
      if (f.theta !== want) fail(2, `theta ${th0} -> ${f.theta}, want ${want} (stun ${stun})`); else inc("turnOk");
      const tumble = hs0 + (f.headAngVel * 1.7 + 0 * 0.5) * dt;
      if (f.headSpin !== tumble) fail(2, "the head's tumble says the drive was not 0"); else inc("driveOk");
    } else {
      const want = stun <= 0 ? th0 + f.w.spin * spinMul * dt * spinDir : th0;
      if (Math.abs(f.theta - want) > 1e-12) fail(2, `out of the window: theta ${th0} -> ${f.theta}, want ${want}`); else inc("spinOk");
    }
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!self.w || self.w.id !== "bindweed" || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultVine, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: foe.w && foe.w.id === "bulwarden", curse: foe.stacks("curse") };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    const D = self.dealt - d0, crit = self.crits > c0;
    const raw = self.w.dmg * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(4, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    return r;
  };
  P.tickTendril = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultVine && f.w.id !== "bindweed") fail(1, `${f.w.id} carries ultVine`);
      const Z = f.ultVine;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t1: Z.t + dt, cd1: Z.cd - dt, rm: f.reachMul, fAlive: f.alive, foeAlive: foe.alive,
                 x: f.x, y: f.y, px: f.pivX, py: f.pivY, hx: f.headX, hy: f.headY, fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy,
                 fhp: foe.hp, stk: foe.stacks("entangle"), pin: foe.pin, pinMax: foe.pinMax, pinV: foe.pinV, pinFree: foe.pinFree,
                 bites: f.vineTally.bites, stacks: f.vineTally.stacks, roots: f.vineTally.roots });
    }
    const hs0 = this.hitStop, hurts = [], beats = [], applies = [], oHurt = this.hurt, oBeat = this.beat;
    let shattered = 0;
    this.hurt = function(t, d, s){ const s0 = t.shield; hurts.push([t, d, s]); const r = oHurt.call(this, t, d, s); if (s0 > 0 && t.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    const wrapped = pre.map(p => { const o = p.foe.apply; p.foe.apply = function(k, nn, src){ applies.push([p.foe, k, nn, src]); return o.call(this, k, nn, src); }; return p.foe; });
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; for (const fo of wrapped) delete fo.apply; }
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult, T = f.vineTally, side = f === this.a ? "a" : "b";
      if (p.t1 >= Z.dur || !p.fAlive || !p.foeAlive){
        /* THE CLOSE */
        if (f.ultVine){ fail(1, "the window did not close"); continue; }
        if (p.fAlive && p.foeAlive && p.t1 < Z.dur - 1e-9) fail(1, "closed early");
        inc("closes");
        if (f.reachMul !== 1) fail(3, `reachMul ${f.reachMul} after the close`);
        if (f.vineWither !== u.wither) fail(9, `wither ${f.vineWither} at the close`);
        const clock = p.t1 >= Z.dur && p.fAlive && p.foeAlive, dr = T.roots - p.roots;
        if (clock){
          inc("clockCloses");
          const nst = p.stk, hold = u.rootPer * nst;
          if (u.rootPer > 0 && nst > 0){
            if (dr !== 1) fail(8, `${dr} roots at a clock close with ${nst} stacks`);
            else if (foe.pin !== Math.max(p.pin, hold) || foe.pinMax !== Math.max(p.pinMax, hold)) fail(8, `pin ${p.pin} -> ${foe.pin}, want ${Math.max(p.pin, hold)}`);
            else if (foe.pinFree !== p.pinFree) fail(8, "the root touched pinFree");
            else if (!(p.pin > hold) && (!foe.pinV || foe.pinV[0] !== p.fvx || foe.pinV[1] !== p.fvy)) fail(8, "pinV not captured");
            else if ((p.pin > hold) && foe.pinV !== p.pinV) fail(8, "pinV recaptured under a longer hold");
            else { inc("rootOk"); inc("rootSec", hold); }
          } else if (dr) fail(8, "a root with no stacks or rootPer 0");
          else inc("noRootOk");
        } else if (dr) fail(8, "a root at a death close");
        else inc("deathCloseOk");
        continue;
      }
      /* A WINDOW FRAME */
      inc("frames");
      if (!f.ultVine){ fail(1, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      const dd = Math.hypot(p.fx - p.x, p.fy - p.y);
      const tgt = clampf((dd - R) / (f.w.reach * this.actMods.reach), 1, u.growCap);
      const wantR = p.rm < tgt ? Math.min(tgt, p.rm + u.grow * dt) : p.rm > tgt ? Math.max(tgt, p.rm - u.grow * dt) : p.rm;
      if (f.reachMul !== wantR) fail(3, `reachMul ${p.rm} -> ${f.reachMul}, want ${wantR} (target ${tgt})`); else inc("growOk");
      const touching = seg(p.px, p.py, p.hx, p.hy, p.fx, p.fy) < R + u.vineW;
      if (touching) inc("touchFrames");
      inc("stkFrames", foe.stacks("entangle"));
      const bit = T.bites - p.bites, on = u.biteDmg > 0 || u.bitePer > 0;
      const mine = applies.filter(x => x[0] === foe), hs = hurts.filter(h => h[0] === foe);
      if (bit > 1) fail(5, `${bit} bites in one frame`);
      if (bit){
        inc("bites");
        if (!touching) fail(5, "a bite without contact");
        if (p.cd1 > 1e-9) fail(5, `a bite with the cooldown at ${p.cd1}`);
        const lb = lastBite.get(Z);
        if (lb !== undefined && p.t1 - lb < u.biteCd - 1e-9) fail(5, `bites ${(p.t1 - lb).toFixed(3)}s apart`);
        lastBite.set(Z, p.t1);
        inc("touchOk");
        if (u.biteDmg > 0){
          if (hs.length !== 1 || hs[0][1] !== u.biteDmg || hs[0][2] !== f) fail(6, `hurt ${JSON.stringify(hs.map(h => h[1]))} want [${u.biteDmg}] from the caster`);
          else inc("dmgOk");
        } else if (hs.length) fail(6, "hurt at biteDmg 0");
        if (u.bitePer > 0){
          if (mine.length !== 1 || mine[0][1] !== "entangle" || mine[0][2] !== u.bitePer) fail(6, `applies ${JSON.stringify(mine.map(x => [x[1], x[2]]))}`);
          else if (mine[0][3] !== side) fail(6, `source ${typeof mine[0][3] === "object" ? "a Fighter" : JSON.stringify(mine[0][3])}`);
          else inc("applyOk");
        } else if (mine.length) fail(6, "an application at bitePer 0");
        if (T.stacks - p.stacks !== u.bitePer) fail(6, "applications != bites x bitePer");
        const killed = p.fhp > 0 && foe.hp <= 0, fb = beats.filter(b => b.fatal && b.tendril);
        if (killed){ if (fb.length !== 1) fail(7, `a killing bite filed ${fb.length} fatal beats`); else inc("fatalBite"); }
        else if (beats.length) fail(7, `a bite filed ${beats.length} beat(s)`);
      } else {
        if (touching && on && p.cd1 <= 1e-9) fail(5, "touching with the cooldown clear, and no bite");
        if (hs.length || mine.length || beats.length) fail(6, "a hurt, apply or beat on a frame with no bite");
      }
      if (foe.x !== p.fx || foe.y !== p.fy || (!shattered && (foe.vx !== p.fvx || foe.vy !== p.fvy))) fail(6, "a vine frame moved the foe");
      if (!shattered && this.hitStop !== hs0) fail(6, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
    }
    if (shattered) inc("wardBreaks", shattered);
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "bindweed");
  const T = { casts: 0, frames: 0, touchFrames: 0, bites: 0, dealt: 0, stacks: 0, foeStk: 0, peak: 0, roots: 0, rootSec: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "bindweed", sd) : new AC.Match("bindweed", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.vineTally) for (const k in T) T[k] += me.vineTally[k]; else T.peak += 1;
  }
  P.tickTendril = oTick; P.tickWeapon = oWeap; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep;
  const u = AC.WEAPONS.find(w => w.id === "bindweed").ult;
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           u: { charge: u.charge, turn: u.turn, grow: u.grow, growCap: u.growCap, biteDmg: u.biteDmg, bitePer: u.bitePer, rootPer: u.rootPer } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickTendril === 'function'"):
        raise SystemExit("no tickTendril in this build -- not a Tendril link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, n.get("frames", 0))
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
cc = max(1, n.get("clockCloses", 0))
print(f"\nTENDRIL PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Bindweed both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"growth peak {T['peak']/R['fights']:.2f} (per fight)   Bindweed win {R['win']:.1%}")
print(f"  per cast: bites {T['bites']/casts:.2f}  dmg {T['dealt']/casts:.2f}  root {T['rootSec']/casts:.2f}s   "
      f"touch {100*n.get('touchFrames',0)/frames:.1f}% of window frames   foe stacks on a window frame "
      f"{n.get('stkFrames',0)/frames:.2f}   clock closes rooting {100*n.get('rootOk',0)/cc:.0f}%")
print(f"  seek frames stunned {n.get('seekStunned',0)} of {n.get('seekFrames',0)}   killing bites {n.get('fatalBite',0)}   "
      f"wards broken by a bite {n.get('wardBreaks',0)}   FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
checks = [
    (1, "the window is `dur` on the window clock, closes on either death; only Bindweed carries ultVine", n.get("closes", 0) > 0),
    (2, "the seek: theta + clamp(shortest angle, +-turn x dt), stunned or not, drive 0; spin as ever outside",
        n.get("turnOk", 0) > 0 and n.get("driveOk", 0) > 0 and n.get("spinOk", 0) > 0),
    (3, "the growth: `grow` x dt toward clamp((d - R)/(reach x mods.reach), 1, cap), both ways; 1 after", n.get("growOk", 0) > 0),
    (4, "every blow the flail's own, rebuilt exactly, in the window and out", n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
    (5, "a bite only in contact, never closer than biteCd, never a missed clear contact",
        (n.get("touchOk", 0) > 0) if (U["biteDmg"] or U["bitePer"]) else n.get("frames", 0) > 0),
    (6, "each bite: hurt(foe, biteDmg, caster) once, entangle +bitePer by side letter; nothing else",
        (n.get("dmgOk", 0) > 0 and n.get("applyOk", 0) > 0) if (U["biteDmg"] or U["bitePer"]) else n.get("frames", 0) > 0),
    (7, "a killing bite files one fatal beat; nothing else files one",
        (n.get("fatalBite", 0) > 0) if U["biteDmg"] else n.get("frames", 0) > 0),
    (8, "the root: pin max(pin, rootPer x stacks) at a clock close, Grasp's write, pinFree untouched; none at a death",
        (n.get("rootOk", 0) > 0) if U["rootPer"] else n.get("noRootOk", 0) > 0),
    (9, "no cast while a vine hunts or withers; every close leaves `wither`", n.get("castOk", 0) > 0),
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
