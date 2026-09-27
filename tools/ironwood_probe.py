#!/usr/bin/env python
"""CANOPY'S PROBE -- one check per sentence of v69 §1 / §6 and the brief's §1,
read INSIDE the hooks.

    python ironwood_probe.py --game ../02-chain/sc-canopy.html

Wraps `tickTree`, `resolveHit`, `fireUlt` and `step` on the Match prototype
and reads each event where it happens. Runs Ironwood against every other
relic, both sides, and prints N/N. The checks follow the link's own numbers,
so the same probe gates stages 2-4 (boughs 1 / 3, winDmg 1 / 0.35,
canopy 0 / 1).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] the rooted ball moving between two frames of one window on more than 1%
      of window frames, or a window frame that ends without pin and pinFree
  [2] a live caster released with any velocity, pin or pinV left; a dead one
      whose kill-flight velocity the close touched
  [3] the root locking the weapon: pinFree 0 at the start of a window frame
      (counted; Ravelbone's wire is the only writer), or 0 at its end
  [4] reachMul not rising exactly grow x dt to reachCap on the window clock, or
      not 1 after the close
  [5] a blade set before `sprout`, not [0, 1/3, 2/3] from the first frame at
      or after it (with boughs 3), a new bough without a ribbon or with a
      cooldown not clear, or a blade set or an extra ribbon after the close
  [6] an Ironwood blow whose damage is not the hammer's blade x (winDmg while
      the tree stands, 1 otherwise) x dmgMul x jitter x dmgTaken, rounded,
      crit included -- rebuilt from the captured crit and jitter draws
  [7] an entangle applied outside reach x mods.reach x reachMul + R, closer
      than canopyCd, with a source that is not "a"/"b", with n != canopy, a
      clear lit frame that did not apply, or any application at canopy 0; a
      canopy frame that hurt, moved the foe or filed a beat
  [8] a cast while a tree stands or withers; a close without `wither` seconds
  [9] a window that is not `dur` long on the window clock
  [10] any relic but Ironwood carrying `ultTree` or `bladeSet`
  STAGE 6 (the voice, sc-canopy-fx):
  [11] a sprout without exactly one sprout voice, a clock close without exactly
       one wither voice, either voice on any other frame (a death included), or
       a blow whose hit voice does not carry `bough` exactly while the tree stands
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=99001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickTree, oResolve = P.resolveHit, oFire = P.fireUlt, oStep = P.step;
  const stage6 = /ironwood-sprout/.test(AC.SFX.play.toString());
  const voices = [], oPlay = AC.SFX.play;
  if (stage6) AC.SFX.play = function(kind, q){ voices.push([kind, q]); return oPlay.call(this, kind, q); };
  const last = new WeakMap();     // Z -> {x, y, t} of its previous window frame
  const lastApply = new WeakMap();
  const peaks = [];
  let per = null;                 // per-fight counters for Ironwood

  P.step = function(dt){
    for (const f of [this.a, this.b]) if (f.ultTree){
      if (this.hitStop > 0) inc("winFrozen"); else inc("winLive");
    }
    return oStep.call(this, dt);
  };

  P.fireUlt = function(f, foe){
    if (f.w.id === "ironwood"){
      if (f.ultTree) fail(8, "cast while a tree stands");
      else if (f.treeWither > 0) fail(8, `cast with ${f.treeWither.toFixed(3)}s of wither left`);
      else inc("castOk");
    }
    return oFire.call(this, f, foe);
  };

  P.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    if (!self.w || self.w.id !== "ironwood" || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg, mul, over);
    const stands = !!self.ultTree, u = self.w.ult;
    const d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: foe.w && foe.w.id === "bulwarden", curse: foe.stacks("curse") };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    const v0 = voices.length, sh0 = foe.shield;
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (stands) { inc("blowsIn"); if (per) per.in++; } else { inc("blowsOut"); if (per) per.out++; }
    if (stage6){
      /* THE BLOW'S OWN VOICE IS THE LAST: a blow that breaks the foe's ward
         plays the shatter's hit voice first, inside `hurt` (the ward's rule). */
      const hv = voices.slice(v0).filter(x => x[0] === "hit"), broke = sh0 > 0 && foe.shield <= 0;
      const own = hv[hv.length - 1];
      if (hv.length !== (broke ? 2 : 1)) fail(11, `${hv.length} hit voices on a blow (ward broken ${broke})`);
      else if (broke && !(hv[0][1].crit === true && hv[0][1].bough === undefined)) fail(11, "the shatter's voice is not the ward's own");
      else if (stands ? own[1].bough !== u.winDmg : own[1].bough !== undefined) fail(11, `bough ${own[1].bough} on a blow (tree ${stands})`);
      else inc(stands ? "boughVoice" : "hammerVoice");
    }
    const D = self.dealt - d0, crit = self.crits > c0;
    const jit = 1 + (draws[1] - 0.5) * jitK;
    const raw = (stands ? self.w.dmg * u.winDmg : self.w.dmg) * pre.dm * jit * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){
      if (pre.aegis || pre.curse) inc("blowExempt");
      else {
        const full = Math.round((crit ? critMul : 1) * self.w.dmg * pre.dm * jit * pre.dt);
        fail(6, `${stands ? "IN" : "out of"} the window: dealt ${D}, want ${want}${stands && Math.abs(D - full) < 1e-6 ? " -- FULL DAMAGE" : ""}`);
      }
    } else inc(stands ? "dmgInOk" : "dmgOutOk");
    return r;
  };

  P.tickTree = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if ((f.ultTree || f.bladeSet) && f.w.id !== "ironwood") fail(10, `${f.w.id} carries ultTree/bladeSet`);
      const Z = f.ultTree;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t1: Z.t + dt, cd1: Z.cd - dt, x: f.x, y: f.y, vx: f.vx, vy: f.vy, alive: f.alive,
                 pinFree: f.pinFree, rm: f.reachMul, set: f.bladeSet, fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy,
                 fAlive: foe.alive, stk: foe.stacks("entangle") });
    }
    const applies = [], hurts = [], beats = [];
    const oHurt = this.hurt, oBeat = this.beat;
    const oApply = pre.map(p => { const o = p.foe.apply; p.foe.apply = function(k, nn, src){ applies.push([p.foe, k, nn, src]); return o.call(this, k, nn, src); }; return [p.foe, o]; });
    this.hurt = function(t, d, s){ hurts.push(d); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    const v0 = voices.length;
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; for (const [fo] of oApply) delete fo.apply; }
    const tv = voices.slice(v0).filter(x => x[0] === "ult" && x[1] && /^ironwood-(sprout|wither)$/.test(x[1].w));
    if (hurts.length) fail(7, `the tree's tick hurt ${hurts.length}x`);
    if (beats.length) fail(7, `the tree's tick filed ${beats.length} beat(s)`);
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult, side = f === this.a ? "a" : "b";
      const mine = applies.filter(x => x[0] === foe);
      if (p.t1 >= Z.dur || !p.alive){
        /* THE CLOSE */
        if (f.ultTree) { fail(9, "the window did not close at dur / on death"); continue; }
        if (p.alive && p.t1 < Z.dur - 1e-9) fail(9, "closed early");
        inc("closes");
        if (p.alive){
          if (f.vx !== 0 || f.vy !== 0 || f.pin !== 0 || f.pinV !== null || f.pinFree !== 0) fail(2, `released with v ${f.vx},${f.vy} pin ${f.pin} pinV ${JSON.stringify(f.pinV)} pinFree ${f.pinFree}`);
          else inc("restOk");
        } else {
          if (f.vx !== p.vx || f.vy !== p.vy) fail(2, "the close touched a dead caster's kill flight");
          else inc("deadCloseOk");
        }
        if (f.reachMul !== 1) fail(4, `reachMul ${f.reachMul} after the close`);
        if (f.bladeSet !== null || f.tips.length !== f.w.blades.length) fail(5, `after the close: bladeSet ${JSON.stringify(f.bladeSet)}, ${f.tips.length} ribbons`);
        if (f.treeWither !== u.wither) fail(8, `wither ${f.treeWither} at the close`);
        if (mine.length) fail(7, "an application on the closing frame");
        const pk = last.get(Z); if (pk) peaks.push(pk.peak);
        if (stage6){
          const wv = tv.filter(x => x[1].w === "ironwood-wither").length;
          if (p.alive && p.t1 >= Z.dur){ if (wv !== 1) fail(11, `clock close voiced ${wv}x`); else inc("witherVoice"); }
          else if (wv) fail(11, "a wither voice on a death");
          if (tv.some(x => x[1].w === "ironwood-sprout")) fail(11, "a sprout voice on a close");
        }
        continue;
      }
      /* A WINDOW FRAME */
      inc("frames");
      if (!f.ultTree) { fail(9, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      const L = last.get(Z);
      if (L){
        inc("pairs");
        if (p.x !== L.x || p.y !== L.y) inc("moved");
      }
      if (f.pin <= 0 || f.pinFree !== 1) fail(1, `a window frame ended with pin ${f.pin} pinFree ${f.pinFree}`);
      if (p.pinFree !== 1) inc("pinFreeCleared");
      const want = Math.min(u.reachCap, p.rm + u.grow * dt);
      if (f.reachMul !== want) fail(4, `reachMul ${p.rm} -> ${f.reachMul}, want ${want}`); else inc("growOk");
      last.set(Z, { x: f.x, y: f.y, peak: Math.max(L ? L.peak : 1, f.reachMul) });
      /* the sprout */
      if (stage6){
        const sv = tv.filter(x => x[1].w === "ironwood-sprout").length, sprouted = u.boughs > 1 && !p.set && f.bladeSet;
        if (sprouted){ if (sv !== 1) fail(11, `a sprout voiced ${sv}x`); else inc("sproutVoice"); }
        else if (sv) fail(11, "a sprout voice with no sprout");
        if (tv.some(x => x[1].w === "ironwood-wither")) fail(11, "a wither voice on a window frame");
      }
      if (u.boughs > 1 && p.t1 >= u.sprout){
        const s = f.bladeSet;
        const ok = s && s.length === u.boughs && s.every((v, i) => v === i / u.boughs);
        if (!ok) fail(5, `at ${p.t1.toFixed(3)}s the blade set is ${JSON.stringify(s)}`);
        else if (f.tips.length < u.boughs) fail(5, `${f.tips.length} ribbons for ${u.boughs} boughs`);
        else if (!p.set){
          let clear = true; for (let i = 1; i < u.boughs; i++) if (f.hitCd[i] !== 0) clear = false;
          if (!clear) fail(5, `new boughs' cooldowns ${JSON.stringify(f.hitCd)}`); else inc("sproutOk");
          if (p.t1 - dt >= u.sprout) fail(5, "sprouted late");
        }
      } else if (f.bladeSet) fail(5, `a blade set at ${p.t1.toFixed(3)}s (sprout ${u.sprout}, boughs ${u.boughs})`);
      else inc("noSetOk");
      /* the canopy */
      inc("stkFrames", p.stk);
      const reach = f.w.reach * this.actMods.reach * f.reachMul;
      const under = p.fAlive && Math.hypot(p.fx - f.x, p.fy - f.y) < reach + R;
      if (under) inc("underFrames");
      if (foe.x !== p.fx || foe.y !== p.fy || foe.vx !== p.fvx || foe.vy !== p.fvy) fail(7, "a tree frame moved the foe");
      if (u.canopy <= 0){
        if (mine.length) fail(7, `applied ${mine.length} at canopy 0`);
        continue;
      }
      if (mine.length > 1) fail(7, `${mine.length} applications in one frame`);
      if (mine.length){
        const [, k, nn, src] = mine[0];
        inc("applies");
        if (!under) fail(7, "entangle applied outside the canopy");
        if (k !== "entangle" || nn !== u.canopy) fail(7, `applied ${k} ${nn}`);
        if (src !== side) fail(7, `source ${typeof src === "object" ? "a Fighter" : JSON.stringify(src)}`); else inc("srcOk");
        const la = lastApply.get(Z);
        if (la !== undefined && p.t1 - la < u.canopyCd - 1e-9) fail(7, `applications ${(p.t1 - la).toFixed(3)}s apart`);
        lastApply.set(Z, p.t1);
        if (p.cd1 > 1e-9) fail(7, `applied with the cooldown at ${p.cd1}`); else inc("canopyOk");
      } else if (under && p.cd1 <= 1e-9) fail(7, "under the canopy with the cooldown clear, and no application");
    }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "ironwood");
  const T = { casts: 0, frames: 0, canopyFrames: 0, stacks: 0, sprouts: 0 };
  let fights = 0, wins = 0, decided = 0, blowsIn = 0, blowsOut = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "ironwood", sd) : new AC.Match("ironwood", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; blowsIn += per.in; blowsOut += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.treeTally) for (const k in T) T[k] += me.treeTally[k];
  }
  P.tickTree = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep;
  const u = AC.WEAPONS.find(w => w.id === "ironwood").ult;
  const pk = peaks.length ? peaks.reduce((s, v) => s + v, 0) / peaks.length : 0;
  if (stage6) AC.SFX.play = oPlay;
  return { n, bad, T, fights, win: wins / decided, stage6, blowsIn: blowsIn / fights, blowsOut: blowsOut / fights, peak: pk,
           u: { charge: u.charge, boughs: u.boughs, winDmg: u.winDmg, canopy: u.canopy, reachCap: u.reachCap, sprout: u.sprout } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickTree === 'function'"):
        raise SystemExit("no tickTree in this build -- not a Canopy link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, n.get("frames", 0))
moved = n.get("moved", 0) / max(1, n.get("pairs", 0))
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
print(f"\nCANOPY PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Ironwood both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}"
      f"   growth peak {R['peak']:.3f} a cast   Ironwood win {R['win']:.1%}")
print(f"  canopy: foe under it {100*n.get('underFrames',0)/frames:.1f}% of window frames   applications a cast "
      f"{n.get('applies',0)/casts:.2f}   entangle stacks on an average window frame {n.get('stkFrames',0)/frames:.2f}")
print(f"  root: moved on {100*moved:.2f}% of window frame pairs   pinFree found cleared {n.get('pinFreeCleared',0)}x   "
      f"sprouts {T['sprouts']}")
print(f"  FREEZE CENSUS: {100*frozen:.1f}% of window steps frozen ({n.get('winFrozen',0)} of "
      f"{n.get('winFrozen',0)+n.get('winLive',0)})   blows exempt (an Aegis or a curse on the foe) {n.get('blowExempt',0)}")
checks = [
    (1, "the rooted ball does not move (>= 99% of window frames); pin and pinFree every frame", n.get("pairs", 0) > 0 and moved <= 0.01),
    (2, "released on close: a live caster to rest, a dead one's kill flight untouched", n.get("restOk", 0) > 0),
    (3, "the root never locks the weapon (pinFree cleared only by a wire, <= 1% of frames)", n.get("frames", 0) > 0 and n.get("pinFreeCleared", 0) <= 0.01 * frames),
    (4, "reachMul rises grow x dt to reachCap on the window clock, and is 1 after", n.get("growOk", 0) > 0),
    (5, "the boughs sprout at `sprout` as [0, 1/3, 2/3] with ribbons and clear cooldowns, and go on close",
        (n.get("sproutOk", 0) > 0) if U["boughs"] > 1 else n.get("noSetOk", 0) > 0),
    (6, "every blow: the hammer's blade x (winDmg while the tree stands), crit and jitter rebuilt exactly",
        n.get("dmgInOk", 0) > 0 and n.get("dmgOutOk", 0) > 0),
    (7, "the canopy: entangle `canopy` inside the reach, the cadence, a side letter; nothing else",
        (n.get("canopyOk", 0) > 0 and n.get("srcOk", 0) > 0) if U["canopy"] else n.get("frames", 0) > 0),
    (8, "no cast while a tree stands or withers; every close leaves `wither`", n.get("castOk", 0) > 0 and n.get("closes", 0) > 0),
    (9, "the window is `dur` long on the window clock", n.get("closes", 0) > 0),
    (10, "only Ironwood carries ultTree / bladeSet", True),
]
if R.get("stage6"):
    print(f"  stage 6 voices: sprouts {n.get('sproutVoice',0)}, clock closes {n.get('witherVoice',0)}, "
          f"bough blows {n.get('boughVoice',0)}, hammer blows {n.get('hammerVoice',0)}")
    checks.append((11, "stage 6: one sprout voice a sprout, one wither voice a clock close (none on a death), `bough` on the hit voice exactly while the tree stands",
                   n.get("sproutVoice", 0) > 0 and n.get("witherVoice", 0) > 0 and n.get("boughVoice", 0) > 0 and n.get("hammerVoice", 0) > 0))
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED / OUT OF BOUND -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
