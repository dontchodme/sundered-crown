#!/usr/bin/env python
# SCRATCH COPY: tools/heartwood_probe.py as it stood BEFORE the Spellbreaker review lessons (sha 89f2ba3adb843bb8), kept to show what it missed.
"""ROOTFAST'S PROBE -- one check per sentence of v85 §1 / §4 / §5, read INSIDE the hooks.

    python heartwood_probe.py --game <link>

Wraps `step`, `tickRootfast`, `rootBlow`, `resolveHit`, `tickCharge`,
`fireUlt`, `move` and `tickHits` on the Match prototype and reads each event
where it happens. Runs Heartwood against every other relic, both sides, and
prints N/N. The window, the charge and the root's length are PINNED from the
builder (`heartwood_build.ULT`), never read off the row under test; the
entangle is 0 on stage 2's link and the builder's on stage 3's and after.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "for a duration": the window not `dur` on the window clock -- a
      `tickRootfast` call on a frozen step (a hit stop, the latch, the split
      hold, the verdict), not exactly one on every unfrozen step, `t` not
      advancing by dt a call, a clock window not exactly as many calls as the
      clock takes to reach `dur` -- a window outliving either death, or any
      relic but Heartwood carrying `ultRoot`
  [2] "every blow the sword lands roots the enemy": a blow Heartwood lands
      inside its window, the opponent alive after it, that does not root
      exactly once (a blow on a Twinshade shade roots Twinshade); a root from
      a blow outside the window; a killing blow that roots
  [3] "roots ... for a second": after a rooting blow the opponent's pin is not
      max(pin before, rootFor), pinMax likewise, or pinV is not captured iff
      the hold standing was not longer -- and then EXACTLY the vector the ball
      was hit with, the engine's knock rebuilt from the blow's crit ("the
      knock is applied and then frozen by the pin", §4); otherwise untouched
  [4] "ball and weapon": the root touches pinFree; a ball the root holds
      (pin > 0, pinFree 0) moved by move(), or landing a blow, or entering
      its hit loop with its weapon free (stun 0)
  [5] "and entangles it" (§4 "+1 on top of the channel's 2"): a rooted blow
      whose applications on the opponent are not the channel's own and then
      entangle +extraEnt by side letter; any other application; a root
      that entangles at extraEnt 0
  [6] "No damage change": a blow of Heartwood's whose damage is not the blade
      x dmgMul x jitter x dmgTaken, rounded, crit included -- rebuilt from the
      captured draws, in the window and out; and NOTHING ELSE: `rootBlow`
      hurting, moving, beating, touching the hit stop, drawing the RNG or
      writing any field but the opponent's pin, pinMax, pinV, entangle and
      the tally
  [7] "Charge / window 8": a cast not on the frame the live charge clock
      reaches the builder's charge, or a cast while a window is open; the
      row's charge, window, root length or entangle not the builder's
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, 'C:/dev/sundered-crown/tools')
from scpage import game
import heartwood_build as HB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=112001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds, PIN]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const HW = "heartwood";
  const oStep = P.step, oTick = P.tickRootfast, oRoot = P.rootBlow, oResolve = P.resolveHit,
        oCharge = P.tickCharge, oFire = P.fireUlt, oMove = P.move, oHits = P.tickHits;
  const isHW = (m, f) => f && f.w && f.w.id === HW && (f === m.a || f === m.b);
  const opp = (m, f) => f === m.a ? m.b : m.a;
  /* THE WINDOW'S LENGTH ON THE WINDOW CLOCK: the calls it takes the clock,
     accumulated as the engine accumulates it, to reach `dur`. */
  let wantCalls = 0; { let t = 0; while (!(t >= PIN.dur)) { t += DT; wantCalls++; } }
  let per = null;                         // this fight's counters
  let tickCalls = 0, rootCalls = 0, castNow = 0;
  const winCalls = new WeakMap();         // window record -> calls so far
  const heldBy = new Set();               // balls a Heartwood root holds (pin > 0 since a root)

  P.step = function(dt){
    const frozen = this.over || !!this.latch || !!this.splitHold || this.hitStop > 0;
    const c0 = tickCalls;
    for (const f of [this.a, this.b]) if (isHW(this, f) && f.ultRoot){ per.winSteps++; if (frozen) per.winFrozen++; }
    const r = oStep.call(this, dt);
    const calls = tickCalls - c0;
    if (frozen){ if (calls) fail(1, `tickRootfast ran ${calls}x on a frozen step`); else inc("frozenOk"); }
    else if (calls !== 1) fail(1, `tickRootfast ran ${calls}x on an unfrozen step`); else inc("liveOk");
    /* THE LAB'S COLUMN: the foe pinned on a window frame, read after the step. */
    for (const f of [this.a, this.b]) if (isHW(this, f) && f.ultRoot){
      per.labFrames++; if (opp(this, f).pin > 0) per.labPinned++;
    }
    for (const q of [...heldBy]) if (!(q.pin > 0)) heldBy.delete(q);
    return r;
  };
  P.tickRootfast = function(dt){
    tickCalls++;
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultRoot && !isHW(this, f)) fail(1, `${f.w.id} carries ultRoot`);
      if (!f.ultRoot) continue;
      const foe = opp(this, f);
      pre.push({ f, Z: f.ultRoot, t1: f.ultRoot.t + dt, fAlive: f.alive, foeAlive: foe.alive });
    }
    const r = oTick.call(this, dt);
    for (const p of pre){
      const k = (winCalls.get(p.Z) || 0) + 1; winCalls.set(p.Z, k);
      if (p.t1 >= PIN.dur || !p.fAlive || !p.foeAlive){
        if (p.f.ultRoot){ fail(1, "the window did not close"); continue; }
        if (p.fAlive && p.foeAlive){
          if (k !== wantCalls) fail(1, `a clock window of ${k} calls, want ${wantCalls}`); else inc("clockClose");
        } else inc("deathClose");
      } else {
        if (p.f.ultRoot !== p.Z) fail(1, `closed at ${p.t1.toFixed(4)} of ${PIN.dur}`);
        else if (p.Z.t !== p.t1) fail(1, `t ${p.Z.t}, want ${p.t1}`);
        else inc("winOk");
      }
    }
    return r;
  };
  /* THE ROOT ITSELF: nothing but the opponent's pin, pinMax, pinV and
     entangle and the tally may change, and no RNG. (The opponent's pinFree
     is [4]'s, so a pinFree write fails [4] and only [4].) */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "alive",
              "reachMul", "hits", "dealt", "crits", "spinDir", "burden", "launch", "flash"];
  const snap = (m, q, f) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? 1 : 0, (m.beats || []).length, m.shake];
    for (const g of [m.a, m.b]){
      for (const k of FF) o.push(g[k]);
      if (g !== q){ o.push(g.pin, g.pinMax, g.pinV ? [g.pinV[0], g.pinV[1]] : null, g.pinFree); }
      o.push(Object.keys(g.status).sort().filter(k => !(g === q && k === "entangle"))
               .map(k => [k, g.status[k].stacks, g.status[k].t, typeof g.status[k].src === "object" ? "F" : g.status[k].src]));
      o.push(g.ultRoot ? [g.ultRoot.t, g.ultRoot.dur] : null);
    }
    for (const s of (m.shades || [])) o.push([s.x, s.y, s.vx, s.vy, s.hp, s.pin]);
    return JSON.stringify(o);
  };
  P.rootBlow = function(f){
    rootCalls++;
    const q = opp(this, f), s0 = snap(this, q, f), oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oRoot.call(this, f); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(6, `rootBlow drew the RNG ${drew}x`);
    const s1 = snap(this, q, f);
    if (s1 !== s0) fail(6, "rootBlow changed something else: " + s0.slice(0, 200) + " -> " + s1.slice(0, 200));
    else inc("rootClean");
    return r;
  };
  P.fireUlt = function(f, foe){
    if (isHW(this, f)){
      castNow++;
      if (f.ultRoot) fail(7, "a cast while the window is open"); else inc("castOk");
      per.casts++;
    }
    return oFire.call(this, f, foe);
  };
  P.tickCharge = function(f, foe, dt){
    if (!isHW(this, f)) return oCharge.call(this, f, foe, dt);
    const c0 = f.charge, live = f.alive && !this.over, k0 = castNow;
    const r = oCharge.call(this, f, foe, dt);
    const cast = castNow - k0;
    if (live){
      const c1 = c0 + dt;
      if (c1 >= PIN.charge){ if (cast !== 1 || f.charge !== 0) fail(7, `the clock at ${c1.toFixed(4)} of ${PIN.charge}: ${cast} cast(s)`); else inc("chargeOk"); }
      else if (cast || f.charge !== c1) fail(7, `a cast at ${c1.toFixed(4)} of ${PIN.charge}`);
    } else if (cast) fail(7, "a cast from a dead caster or a finished match");
    return r;
  };
  P.move = function(f, foe, dt){
    if (!heldBy.has(f) || !(f.pin > 0) || f.pinFree) return oMove.call(this, f, foe, dt);
    const x0 = f.x, y0 = f.y;
    const r = oMove.call(this, f, foe, dt);
    if (f.x !== x0 || f.y !== y0) fail(4, `a held ${f.w.id} moved`); else inc("heldStill");
    return r;
  };
  P.tickHits = function(self, foe, dt, cool){
    if (!heldBy.has(self) || !(self.pin > 0) || self.pinFree) return oHits.call(this, self, foe, dt, cool);
    /* The weapon is locked: tickStasis re-arms stun >= pin every step, and on
       the root's own step the blow's hitstun already holds it. */
    if (!(self.stun > 0)) fail(4, `a held ${self.w.id} with its weapon free (stun ${self.stun}, pin ${self.pin})`);
    const h0 = self.hits;
    const r = oHits.call(this, self, foe, dt, cool);
    if (self.hits !== h0) fail(4, `a held ${self.w.id} landed a blow`); else inc("heldQuiet");
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isHW(this, self) || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const q = opp(this, self), open = !!self.ultRoot, T = self.rootTally;
    const h0 = self.hits, d0 = self.dealt, c0 = self.crits, rc0 = rootCalls, rooted0 = T ? T.rooted : 0;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis, curse: foe.stacks("curse"),
                  pin: q.pin, pinMax: q.pinMax, pinV: q.pinV, pinFree: q.pinFree, vx: q.vx, vy: q.vy, qx: q.x, qy: q.y,
                  sx: self.x, sy: self.y, ent: q.stacks("entangle") };
    const draws = [], oRng = this.rng, applies = [];
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    const targets = foe === q ? [q] : [q, foe];
    for (const t of targets){ const o = t.apply; t.apply = function(k, nn, src){ applies.push([t, k, nn, src]); return o.call(this, k, nn, src); }; }
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; for (const t of targets) delete t.apply; }
    if (self.hits - h0 !== 1) return r;
    const crit = self.crits > c0;
    /* [6] THE BLOW IS THE SWORD'S OWN */
    if (open) per.bin++; else per.bout++;
    const D = self.dealt - d0;
    const raw = self.w.dmg * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(6, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    /* [2] EVERY BLOW IN THE WINDOW ROOTS, NONE OUTSIDE, NOT A KILLING ONE */
    const calls = rootCalls - rc0, dr = (self.rootTally ? self.rootTally.rooted : 0) - rooted0;
    const expect = open && q.alive;
    if (open && calls !== 1) fail(2, `a blow in the window called the root ${calls}x`);
    else if (!open && calls) fail(2, "a root from a blow outside the window");
    else if (dr !== (expect ? 1 : 0)) fail(2, `${dr} roots from a blow (in the window ${open}, opponent alive ${q.alive})`);
    else { inc(expect ? "rootOk" : open ? "killNoRoot" : "outNoRoot"); if (expect && foe !== q) inc("shadeRoot"); }
    /* [3] THE PIN: GRASP'S WRITE, ON THE KNOCKED VECTOR */
    let vxK = pre.vx, vyK = pre.vy;
    if (foe === q){
      const kx = pre.qx - pre.sx, ky = pre.qy - pre.sy, kl = Math.hypot(kx, ky) || 1;
      const power = C.combat.knock * (self.w.knockMul || 1) * (crit ? 1.5 : 1) * 1;
      vxK = pre.vx + (kx / kl) * power; vyK = pre.vy + (ky / kl) * power;
    }
    if (expect){
      const hold = PIN.rootFor;
      if (q.pin !== Math.max(pre.pin, hold) || q.pinMax !== Math.max(pre.pinMax, hold)) fail(3, `pin ${pre.pin} -> ${q.pin}, pinMax ${pre.pinMax} -> ${q.pinMax}, want ${Math.max(pre.pin, hold)}`);
      else if (!(pre.pin > hold) && (!q.pinV || q.pinV[0] !== vxK || q.pinV[1] !== vyK)) fail(3, `pinV ${JSON.stringify(q.pinV)}, want the knocked [${vxK}, ${vyK}]`);
      else if ((pre.pin > hold) && q.pinV !== pre.pinV) fail(3, "pinV recaptured under a longer hold");
      else { inc("pinOk"); if (pre.pin > 0) inc("rerootOk"); if (pre.pin > hold) inc("longerHold"); }
      if (q.pinFree !== pre.pinFree) fail(4, `the root wrote pinFree ${pre.pinFree} -> ${q.pinFree}`); else inc("pinFreeOk");
      if (q.pin > 0 && !q.pinFree) heldBy.add(q);
    } else if (q.pin !== pre.pin || q.pinMax !== pre.pinMax || q.pinV !== pre.pinV) fail(3, "a blow that roots nobody moved the opponent's pin");
    /* [5] THE CHANNEL'S OWN, THEN +extraEnt BY SIDE LETTER */
    const side = self === this.a ? "a" : "b", ch = (self.w.onHit || {});
    const onQ = applies.filter(x => x[0] === q), onFoe = applies.filter(x => x[0] === foe);
    const chanWant = Object.entries(ch).map(([k, v]) => [k, v, undefined]);
    const got = onQ.map(x => [x[1], x[2], x[3]]);
    const want5 = (foe === q ? chanWant : []).concat(expect && PIN.extraEnt > 0 ? [["entangle", PIN.extraEnt, side]] : []);
    if (JSON.stringify(got) !== JSON.stringify(want5)) fail(5, `applications on the opponent ${JSON.stringify(got)}, want ${JSON.stringify(want5)}`);
    else if (foe !== q && JSON.stringify(onFoe.map(x => [x[1], x[2], x[3]])) !== JSON.stringify(chanWant)) fail(5, "the shade's own applications moved");
    else if (expect){ inc("entOk"); per.entIn += (foe === q ? 2 : 0) + PIN.extraEnt; per.entUlt += PIN.extraEnt; }
    if (open && foe === q) per.binOpp++;
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== HW);
  const row = AC.WEAPONS.find(w => w.id === HW).ult;
  for (const [k, v] of [["charge", PIN.charge], ["dur", PIN.dur], ["rootFor", PIN.rootFor], ["extraEnt", PIN.extraEnt]])
    if (row[k] !== v) fail(7, `the row's ${k} is ${row[k]}, the builder's ${v}`); else inc("rowOk");
  const S = { fights: 0, wins: 0, decided: 0, casts: 0, bin: 0, bout: 0, binOpp: 0, winSteps: 0, winFrozen: 0,
              labFrames: 0, labPinned: 0, entIn: 0, entUlt: 0, blows: 0, rooted: 0, roots: 0, ent: 0, frames: 0 };
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, HW, sd) : new AC.Match(HW, fid, sd);
    const me = side ? m.b : m.a;
    per = { casts: 0, bin: 0, bout: 0, binOpp: 0, winSteps: 0, winFrozen: 0, labFrames: 0, labPinned: 0, entIn: 0, entUlt: 0 };
    heldBy.clear();
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    S.fights++;
    if (m.winner){ S.decided++; if (m.winner === me) S.wins++; }
    for (const k in per) S[k] += per[k];
    if (me.rootTally) for (const k of ["blows", "rooted", "roots", "ent", "frames"]) S[k] += me.rootTally[k];
  }
  P.step = oStep; P.tickRootfast = oTick; P.rootBlow = oRoot; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  return { n, bad, S, wantCalls, u: { charge: row.charge, dur: row.dur, rootFor: row.rootFor, extraEnt: row.extraEnt } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRootfast === 'function'"):
        raise SystemExit("no tickRootfast in this build -- not a Rootfast link (stage 2+)")
    ext = page.evaluate("() => AC.WEAPONS.find(w => w.id === 'heartwood').ult.extraEnt")
    PIN = {"charge": HB.ULT["charge"], "dur": HB.ULT["dur"], "rootFor": HB.ULT["rootFor"],
           # the entangle is stage 3's: 0 on stage 2's link, the builder's after
           "extraEnt": HB.ULT["extraEnt"] if ext else 0}
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN])
    assert not errors, errors

n, bad, S, U = R["n"], R["bad"], R["S"], R["u"]
F = max(1, S["fights"]); casts = max(1, S["casts"])
print(f"\nROOTFAST PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {S['fights']} fights "
      f"(Heartwood both sides x every foe x {a.seeds} seeds)   ult {U}   pinned {PIN}")
print(f"  casts/fight {S['casts']/F:.2f}   blows a fight: in windows {S['bin']/F:.2f} (on the opponent {S['binOpp']/F:.2f}), "
      f"outside {S['bout']/F:.2f}   Heartwood win {S['wins']/max(1,S['decided']):.1%}")
print(f"  per cast: blows rooted {S['rooted']/casts:.2f}   roots as transitions {S['roots']/casts:.2f}   "
      f"extra entangle {S['ent']/casts:.2f}   foe pinned {100*S['labPinned']/max(1,S['labFrames']):.1f}% of window frames (the lab's read)")
print(f"  entangle applied by rooted blows in windows {S['entIn']}  = {S['entIn']/max(1,S['rooted']):.2f} x blows rooted "
      f"(the brief's gate: 3 x at stage 3)   killing blows unrooted {n.get('killNoRoot',0)}   shade blows rooting Twinshade {n.get('shadeRoot',0)}")
print(f"  re-roots on a held ball {n.get('rerootOk',0)} (under a longer hold {n.get('longerHold',0)})   held steps still {n.get('heldStill',0)}   "
      f"held hit loops quiet {n.get('heldQuiet',0)}   FREEZE CENSUS {100*S['winFrozen']/max(1,S['winSteps']):.1f}% of window steps frozen   "
      f"clock window {R['wantCalls']} calls")
has_ent = PIN["extraEnt"] > 0
checks = [
    (1, "the window: dur on the window clock (one tick an unfrozen step, none frozen), closes on either death; only Heartwood's",
        n.get("clockClose", 0) > 0 and n.get("liveOk", 0) > 0 and n.get("frozenOk", 0) > 0),
    (2, "every blow in the window roots the opponent once (a shade's too); none outside; a killing blow roots nobody",
        n.get("rootOk", 0) > 0 and n.get("outNoRoot", 0) > 0),
    (3, "the pin: max(pin, rootFor), pinMax likewise, pinV = the knocked vector iff no longer hold stands",
        n.get("pinOk", 0) > 0 and n.get("rerootOk", 0) > 0),
    (4, "ball and weapon: pinFree untouched; a held ball neither moves nor lands a blow, its weapon locked",
        n.get("pinFreeOk", 0) > 0 and n.get("heldStill", 0) > 0 and n.get("heldQuiet", 0) > 0),
    (5, "the channel's own, then entangle +extraEnt by side letter on every rooted blow; nothing else" +
        ("" if has_ent else "  (extraEnt 0 at this stage: none)"),
        n.get("entOk", 0) > 0),
    (6, "no damage change (every blow rebuilt exactly, in and out); the root writes nothing else, no RNG",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("rootClean", 0) > 0),
    (7, "a cast exactly when the live clock reaches the builder's charge, never with the window open; the row is the builder's",
        n.get("castOk", 0) > 0 and n.get("chargeOk", 0) > 0 and n.get("rowOk", 0) == 4),
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
