#!/usr/bin/env python
"""ROOTFAST'S PROBE -- one check per sentence of v85 §1 / §4 / §5, read INSIDE the hooks.

    python heartwood_probe.py --game <link> --stage 2|3|5

Wraps `step`, `tickRootfast`, `rootBlow`, `resolveHit`, `tickCharge`,
`fireUlt`, `move` and `tickHits` on the Match prototype and reads each event
where it happens. Runs Heartwood against every other relic, both sides, and
prints N/N. EVERY NUMBER IS PINNED BY THE STAGE, from the builder
(`heartwood_build`), never read off the link under test: the window, the
charge and the root's length; the entangle (0 at stage 2, the builder's from
stage 3); the blade (the shipped 12.65 at stages 2 and 3, the builder's
`BLADE` at stage 5, the final). A link that lost a number fails the check that
reads it, and [7] reads the row itself.

"NOTHING ELSE" IS GENERIC, not a list of fields: around every `rootBlow` call,
and around every 16th `tickRootfast` call with a window open and every call
that closes one, every own field of both fighters and of every shade (the
shared weapon row included, to depth 4) and every field of the match is
snapshotted, and only the fields the sentence writes may differ.

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
  [3] "roots ... for a second": after a blow that rooted ([2] reads whether a
      blow in the window rooted at all) the opponent's pin is not
      max(pin before, rootFor), pinMax likewise, or pinV is not captured iff
      the hold standing was not longer -- and then EXACTLY the vector the ball
      was hit with, the engine's knock rebuilt from the blow's crit ("the
      knock is applied and then frozen by the pin", §4); otherwise untouched
  [4] "ball and weapon": the root touches pinFree; a ball the root holds
      (pin > 0, pinFree 0) moved by move(), or landing a blow, or entering
      its hit loop with its weapon free (stun 0)
  [5] "and entangles it" (§4 "+1 on top of the channel's 2"): a blow that rooted
      whose applications on the opponent are not the channel's own and then
      entangle +extraEnt by side letter; any other application; a root
      that entangles at extraEnt 0
  [6] "No damage change": a blow of Heartwood's whose damage is not the blade
      x dmgMul x jitter x dmgTaken, rounded, crit included -- rebuilt from the
      captured draws, in the window and out; and NOTHING ELSE: `rootBlow`
      drawing the RNG or changing any field of either fighter, a shade or the
      match but the opponent's pin, pinMax, pinV and entangle and the tally's
      blows / rooted / roots / ent (so no hurt, no move, no beat, no hit stop,
      no stun, no charge, no reach); `tickRootfast` drawing the RNG or changing
      anything but the window record and the tally's frames
  [7] "Charge 15 (on the game's clock) / window 8": a cast not on the frame
      the live charge clock reaches the builder's charge, or a cast while a
      window is open; the row's charge, window, root length, entangle or
      blade not the pinned stage's
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")   # scratch copy of the 7-check probe, c27d97940d22dbd7
from scpage import game
import heartwood_build as HB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--stage", required=True, choices=["2", "3", "5"],
                help="the stage the link is: 2 the root, 3 the entangle, 5 the blade (the final)")
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
  /* "NOTHING ELSE", GENERIC: every own field of both fighters and of every
     shade (the shared weapon row included) and every field of the match, to
     depth 4, as [path, json] pairs. `mode` names the sentence being watched
     and leaves out only the fields that sentence writes. A long array on the
     match (beats, floats, sparks) is its length and its last two entries. */
  const isF = (m, v) => v === m.a || v === m.b || (m.shades || []).includes(v);
  const ser = (m, v, d, seen) => {
    if (v === undefined) return "u";
    if (v === null) return null;
    const t = typeof v;
    if (t === "function") return "fn";
    if (t === "number") return Number.isNaN(v) ? "NaN" : v;
    if (t !== "object") return v;
    if (isF(m, v)) return v === m.a ? "<A>" : v === m.b ? "<B>" : "<shade>";
    if (seen.has(v)) return "<cyc>";
    if (d > 4) return "<deep>";
    seen.add(v);
    let o;
    if (Array.isArray(v)) o = v.map(x => ser(m, x, d + 1, seen));
    else { o = {}; for (const k of Object.keys(v).sort()) o[k] = ser(m, v[k], d + 1, seen); }
    seen.delete(v);
    return o;
  };
  const snapAll = (m, mode, q, f) => {
    const out = [];
    const bodies = [["A", m.a], ["B", m.b]].concat((m.shades || []).map((s, i) => ["S" + i, s]));
    for (const [lab, g] of bodies){
      for (const k of Object.keys(g).sort()){
        let v = g[k];
        /* the root's own writes; `pinFree` is [4]'s sentence ("ball AND weapon"),
           so a pinFree write fails [4], and [6] leaves it to [4] */
        if (mode === "root" && g === q && (k === "pin" || k === "pinMax" || k === "pinV" || k === "pinFree")) continue;
        if (mode === "root" && g === q && k === "status" && v){ v = Object.assign({}, v); delete v.entangle; }
        if (k === "rootTally" && v && isHW(m, g)){
          v = Object.assign({}, v);
          if (mode === "root" && g === f){ delete v.blows; delete v.rooted; delete v.roots; delete v.ent; }
          if (mode === "tick") delete v.frames;
        }
        if (mode === "tick" && k === "ultRoot" && isHW(m, g)) continue;
        out.push([lab + "." + k, JSON.stringify(ser(m, v, 1, new Set()))]);
      }
    }
    for (const k of Object.keys(m).sort()){
      const v = m[k];
      if (k === "rng" || k === "shades" || isF(m, v)) continue;
      if (Array.isArray(v) && v.length > 8) out.push(["m." + k, JSON.stringify([v.length, ser(m, v.slice(-2), 1, new Set())])]);
      else out.push(["m." + k, JSON.stringify(ser(m, v, 1, new Set()))]);
    }
    return out;
  };
  const diffSnap = (s0, s1) => {
    if (s0.length !== s1.length) return `the set of fields (${s0.length} -> ${s1.length})`;
    for (let i = 0; i < s0.length; i++)
      if (s0[i][0] !== s1[i][0] || s0[i][1] !== s1[i][1])
        return `${s1[i][0]}: ${s0[i][1].slice(0, 90)} -> ${s1[i][1].slice(0, 90)}`;
    return null;
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
    /* [6] THE TICKER WRITES NOTHING ELSE: every 16th call with a window open
       and every call that closes one, snapshotted whole. */
    const closing = pre.some(p => p.t1 >= PIN.dur || !p.fAlive || !p.foeAlive);
    const watch = pre.length > 0 && (closing || tickCalls % 16 === 0);
    const oR = this.rng, oMR = Math.random;
    let s0 = null, drew = 0, r;
    if (watch){
      s0 = snapAll(this, "tick");
      this.rng = function(){ drew++; return oR.apply(this, arguments); };
      Math.random = function(){ drew++; return oMR(); };
    }
    try { r = oTick.call(this, dt); }
    finally { if (watch){ this.rng = oR; Math.random = oMR; } }
    if (watch){
      if (drew) fail(6, `tickRootfast drew the RNG ${drew}x`);
      const dd = diffSnap(s0, snapAll(this, "tick"));
      if (dd) fail(6, "tickRootfast changed " + dd); else inc("tickClean");
    }
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
     entangle and the tally's blows / rooted / roots / ent may change -- in
     either fighter, a shade or the match -- and no RNG. (The opponent's
     pinFree is [4]'s sentence, so a pinFree write fails [4] and only [4].) */
  P.rootBlow = function(f){
    rootCalls++;
    const q = opp(this, f), s0 = snapAll(this, "root", q, f), oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oRoot.call(this, f); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(6, `rootBlow drew the RNG ${drew}x`);
    const dd = diffSnap(s0, snapAll(this, "root", q, f));
    if (dd) fail(6, "rootBlow changed " + dd); else inc("rootClean");
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
    /* [3] and [5] read the blows that ROOTED (dr 1); whether a blow in the window rooted is [2]'s. */
    const rooted = expect && dr === 1;
    if (rooted){
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
    const want5 = (foe === q ? chanWant : []).concat(rooted && PIN.extraEnt > 0 ? [["entangle", PIN.extraEnt, side]] : []);
    if (JSON.stringify(got) !== JSON.stringify(want5)) fail(5, `applications on the opponent ${JSON.stringify(got)}, want ${JSON.stringify(want5)}`);
    else if (foe !== q && JSON.stringify(onFoe.map(x => [x[1], x[2], x[3]])) !== JSON.stringify(chanWant)) fail(5, "the shade's own applications moved");
    else if (rooted){ inc("entOk"); per.entIn += (foe === q ? 2 : 0) + PIN.extraEnt; per.entUlt += PIN.extraEnt; }
    if (open && foe === q) per.binOpp++;
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== HW);
  const row = AC.WEAPONS.find(w => w.id === HW).ult;
  for (const [k, v] of [["charge", PIN.charge], ["dur", PIN.dur], ["rootFor", PIN.rootFor], ["extraEnt", PIN.extraEnt]])
    if (row[k] !== v) fail(7, `the row's ${k} is ${row[k]}, the stage's ${v}`); else inc("rowOk");
  const blade = AC.WEAPONS.find(w => w.id === HW).dmg;
  if (blade !== PIN.blade) fail(7, `the blade is ${blade}, the stage's ${PIN.blade}`); else inc("rowOk");
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
  return { n, bad, S, wantCalls, u: { charge: row.charge, dur: row.dur, rootFor: row.rootFor, extraEnt: row.extraEnt, blade } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRootfast === 'function'"):
        raise SystemExit("no tickRootfast in this build -- not a Rootfast link (stage 2+)")
    # EVERY NUMBER PINNED BY THE STAGE, from the builder -- never read off the link under test.
    PIN = {"charge": HB.ULT["charge"], "dur": HB.ULT["dur"], "rootFor": HB.ULT["rootFor"],
           "extraEnt": 0 if a.stage == "2" else HB.ULT["extraEnt"],
           "blade": float(HB.BLADE if a.stage == "5" else HB.SHIPPED_DMG)}
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN])
    assert not errors, errors

n, bad, S, U = R["n"], R["bad"], R["S"], R["u"]
F = max(1, S["fights"]); casts = max(1, S["casts"])
print(f"\nROOTFAST PROBE  {pathlib.Path(a.game).name}  stage {a.stage}  Chromium {ver}  {S['fights']} fights "
      f"(Heartwood both sides x every foe x {a.seeds} seeds)   the row {U}   pinned {PIN}")
print(f"  casts/fight {S['casts']/F:.2f}   blows a fight: in windows {S['bin']/F:.2f} (on the opponent {S['binOpp']/F:.2f}), "
      f"outside {S['bout']/F:.2f}   Heartwood win {S['wins']/max(1,S['decided']):.1%}")
print(f"  per cast: blows rooted {S['rooted']/casts:.2f}   roots as transitions {S['roots']/casts:.2f}   "
      f"extra entangle {S['ent']/casts:.2f}   foe pinned {100*S['labPinned']/max(1,S['labFrames']):.1f}% of window frames (the lab's read)")
print(f"  entangle applied by rooted blows in windows {S['entIn']}  = {S['entIn']/max(1,S['rooted']):.2f} x blows rooted "
      f"(the brief's gate: 3 x at stage 3)   killing blows unrooted {n.get('killNoRoot',0)}   shade blows rooting Twinshade {n.get('shadeRoot',0)}")
print(f"  re-roots on a held ball {n.get('rerootOk',0)} (under a longer hold {n.get('longerHold',0)})   held steps still {n.get('heldStill',0)}   "
      f"held hit loops quiet {n.get('heldQuiet',0)}   FREEZE CENSUS {100*S['winFrozen']/max(1,S['winSteps']):.1f}% of window steps frozen   "
      f"clock window {R['wantCalls']} calls")
print(f"  nothing else: {n.get('rootClean', 0)} root calls and {n.get('tickClean', 0)} ticker calls "
      f"snapshotted whole (both fighters, the shades, the match), clean")
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
    (6, "no damage change (every blow rebuilt exactly, in and out); the root and the ticker write nothing else "
        "(every field of both fighters, the shades and the match), no RNG",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("rootClean", 0) > 0
        and n.get("tickClean", 0) > 0),
    (7, "a cast exactly when the live clock reaches the builder's charge, never with the window open; the row "
        "(charge, window, root, entangle, blade) is the stage's",
        n.get("castOk", 0) > 0 and n.get("chargeOk", 0) > 0 and n.get("rowOk", 0) == 5),
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
