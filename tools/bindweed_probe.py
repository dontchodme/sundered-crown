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
  STAGE 6 (the picture and the voice, sc-tendril-fx). Each check runs only on a
  link that carries its half, read off the page itself:
  [10] THE VOICE (on when "bindweed-bite" is in AC.SFX.play.toString()): a cast
       without exactly one `ult`/bindweed voice inside fireUlt; a bite without
       exactly one bite voice whose `n` is the foe's entangle stacks after the
       bite; a root without exactly one root voice; a clock close with both
       alive without exactly one wither voice; any Bindweed voice on any other
       frame -- the wither never on a death close; inside the vine's tick, any
       other voice but a ward shatter's own crit hit voice (hurt() plays it);
       and every Bindweed voice of the run accounted for by those events
  [11] THE PICTURE (on when the Match has `tickTwine`): `tickTwine`, the
       picture's one hook on the step, changing any sim field of either fighter
       or the match, or drawing the RNG; a root without exactly one write-only
       `ult` beat and no hit stop, or a beat on any other close; `twineHeld` not
       1 exactly while the root's pin holds its quarry; and on the DRAWN subset
       (the first seed, both sides, every foe) a drawn frame that throws or
       changes any sim field
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
  const clampf = (v, lo, hi) => v < lo ? lo : v > hi ? hi : v;
  const seg = (ax, ay, bx, by, px, py) => { const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    let t = l2 > 0 ? ((px - ax) * dx + (py - ay) * dy) / l2 : 0; t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (ax + t * dx), py - (ay + t * dy)); };
  const oTick = P.tickTendril, oWeap = P.tickWeapon, oResolve = P.resolveHit, oFire = P.fireUlt, oStep = P.step;
  const lastBite = new WeakMap();
  let per = null;

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /bindweed-bite/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickTwine === "function";
  const voices = [], bwAll = {}, oPlay = AC.SFX.play, oTwine = P.tickTwine;
  if (stage6v) AC.SFX.play = function(kind, q){
    voices.push([kind, q ? Object.assign({}, q) : q]);
    if (kind === "ult" && q && typeof q.w === "string" && /^bindweed/.test(q.w)) bwAll[q.w] = (bwAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, pins,
     statuses, chain, window and tally, and the match's clock and hit stop. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "alive", "pin", "pinMax",
              "pinFree", "reachMul", "vineWither", "headX", "headY", "headSpin", "headAng", "headAngVel", "headR",
              "pivX", "pivY", "clanks", "hits", "dealt", "crits", "spinDir", "burden"];
  const snap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(f.pinV ? [f.pinV[0], f.pinV[1]] : null, f.hitCd ? Array.from(f.hitCd) : null);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
      o.push(f.ultVine ? [f.ultVine.t, f.ultVine.cd, f.ultVine.dur] : null);
      o.push(f.vineTally ? JSON.stringify(f.vineTally) : null);
    }
    for (const s of (m.shades || [])) o.push([s.x, s.y, s.hp]);
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 30), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 30), i + 30)); };
  if (stage6p) P.tickTwine = function(dt){
    const s0 = snap(this), oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oTwine.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(11, `tickTwine drew the RNG ${drew}x`);
    const s1 = snap(this);
    if (s1 !== s0) fail(11, "tickTwine changed the sim: " + firstDiff(s0, s1)); else inc("twineOk");
    return r;
  };
  /* THE HELD BALL: the quarry of a root, while the pin holds it. */
  const heldBy = new Set(), rootsSeen = new WeakMap();

  P.step = function(dt){
    for (const f of [this.a, this.b]) if (f.ultVine){ if (this.hitStop > 0) inc("winFrozen"); else inc("winLive"); }
    const r = oStep.call(this, dt);
    if (stage6p){
      for (const f of [this.a, this.b]){
        if (f.w.id !== "bindweed" || !f.vineTally) continue;
        const foe = f === this.a ? this.b : this.a;
        if (f.vineTally.roots !== (rootsSeen.get(f) || 0)){
          rootsSeen.set(f, f.vineTally.roots);
          if (foe.alive && foe.pin > 0) heldBy.add(foe);
        }
      }
      for (const q of [this.a, this.b]){
        if (heldBy.has(q) && !(q.pin > 0 && q.alive)) heldBy.delete(q);
        const held = heldBy.has(q);
        if (held !== (q.twineHeld > 0)) fail(11, `twineHeld ${q.twineHeld} on ${q.w.id} while the root's pin ${held ? "holds" : "does not hold"} it (pin ${q.pin})`);
        else if (held) inc("heldOk");
      }
    }
    return r;
  };
  P.fireUlt = function(f, foe){
    if (f.w.id === "bindweed"){
      if (f.ultVine) fail(9, "cast while a vine hunts");
      else if (f.vineWither > 0) fail(9, `cast with ${f.vineWither.toFixed(3)}s of wither left`);
      else inc("castOk");
    }
    const v0 = voices.length;
    const r = oFire.call(this, f, foe);
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && x[1] && x[1].w === "bindweed").length;
      if (f.w.id === "bindweed"){ if (cv !== 1) fail(10, `a cast voiced ${cv}x`); else inc("castVoice"); }
      else if (cv) fail(10, `${f.w.id}'s cast played Bindweed's voice`);
    }
    return r;
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
    const v0 = voices.length;
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; for (const fo of wrapped) delete fo.apply; }
    /* THE VINE'S VOICES this tick. A ward the bite breaks plays the shatter's
       own crit hit voice inside hurt(); nothing else may sound here. */
    const tv = voices.slice(v0);
    const bwv = tv.filter(x => x[0] === "ult" && x[1] && typeof x[1].w === "string" && /^bindweed-/.test(x[1].w));
    const cnt = (w) => bwv.filter(x => x[1].w === w).length;
    if (stage6v){
      const other = tv.filter(x => !bwv.includes(x));
      const shv = other.filter(x => x[0] === "hit" && x[1] && x[1].crit === true).length;
      if (other.length !== shv || shv !== shattered) fail(10, `the vine's tick played ${JSON.stringify(other.map(x => x[0]))} with ${shattered} ward(s) broken`);
      else if (shv) inc("shatterVoice", shv);
      if (!pre.length && bwv.length) fail(10, `${bwv.length} Bindweed voice(s) with no vine`);
    }
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
        if (stage6v){
          const wv = cnt("bindweed-wither"), rv = cnt("bindweed-root");
          if (clock){ if (wv !== 1) fail(10, `a clock close voiced the wither ${wv}x`); else inc("witherVoice"); }
          else if (wv) fail(10, `a wither voice on a death close (caster ${p.fAlive ? "alive" : "dead"}, foe ${p.foeAlive ? "alive" : "dead"})`);
          else inc("deathSilent");
          if (rv !== dr) fail(10, `${rv} root voice(s) for ${dr} root(s)`); else if (dr) inc("rootVoice");
          if (cnt("bindweed-bite")) fail(10, "a bite voice on a close");
        }
        if (stage6p){
          const rb = beats.filter(b => b.kind === "ult" && b.w === "bindweed");
          if (dr){
            if (beats.length !== 1 || rb.length !== 1) fail(11, `a root filed ${beats.length} beat(s), ${rb.length} of them the root's`);
            else if (rb[0].side !== (f === this.a ? 0 : 1) || rb[0].x !== foe.x || rb[0].y !== foe.y) fail(11, "the root's beat is not at the quarry");
            else inc("rootBeat");
          } else if (beats.length) fail(11, `a close with no root filed ${beats.length} beat(s)`);
          if (this.hitStop !== hs0) fail(11, `the close moved the hit stop ${hs0} -> ${this.hitStop}`);
        }
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
      if (stage6v){
        const bv = bwv.filter(x => x[1].w === "bindweed-bite");
        if (bit){
          if (bv.length !== 1) fail(10, `a bite voiced ${bv.length}x`);
          else if (bv[0][1].n !== foe.stacks("entangle")) fail(10, `a bite voice at n ${bv[0][1].n}, the foe carries ${foe.stacks("entangle")}`);
          else { inc("biteVoice"); inc("biteN" + bv[0][1].n); if (foe.hp <= 0) inc("killBiteVoice"); }
        } else if (bv.length) fail(10, "a bite voice with no bite");
        if (cnt("bindweed-wither") || cnt("bindweed-root")) fail(10, "a wither or root voice on a window frame");
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
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), with the sim read before and after
     each frame. The post chain is off: this asks what a draw WRITES, not
     what it looks like (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "bindweed", sd) : new AC.Match("bindweed", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    voices.length = 0; heldBy.clear();
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){
      m.step(DT); steps++;
      if (drawn){
        const vis = [m.a, m.b].some(q => q.twineFade > 0 || q.twineRootFade > 0 || (q.twineMotes && q.twineMotes.length)
                                         || (q.twineBits && q.twineBits.length) || (q.twineFlash && q.twineFlash.length));
        if (vis ? steps % drawEvery === 0 : steps % 60 === 0){
          const s0 = snap(m);
          try { AC.__draw(m); } catch (e){ fail(11, "a drawn frame threw: " + String((e && e.message) || e)); }
          const s1 = snap(m);
          if (s1 !== s0) fail(11, "a drawn frame changed the sim: " + firstDiff(s0, s1));
          else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); }
        }
      }
    }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.vineTally) for (const k in T) T[k] += me.vineTally[k]; else T.peak += 1;
  }
  P.tickTendril = oTick; P.tickWeapon = oWeap; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY BINDWEED VOICE OF THE RUN, ACCOUNTED FOR by its event. */
    const want = { "bindweed": n.castVoice || 0, "bindweed-bite": n.biteVoice || 0,
                   "bindweed-root": n.rootVoice || 0, "bindweed-wither": n.witherVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(bwAll)]))
      if ((bwAll[k] || 0) !== (want[k] || 0)) fail(10, `${bwAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickTwine = oTwine;
  const u = AC.WEAPONS.find(w => w.id === "bindweed").ult;
  return { n, bad, T, fights, stage6v, stage6p, drawOn, bwAll, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           u: { charge: u.charge, turn: u.turn, grow: u.grow, growCap: u.growCap, biteDmg: u.biteDmg, bitePer: u.bitePer, rootPer: u.rootPer } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickTendril === 'function'"):
        raise SystemExit("no tickTendril in this build -- not a Tendril link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])
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
if R.get("stage6v"):
    ns = {k: n[k] for k in sorted(n) if k.startswith("biteN")}
    print(f"  stage 6 voice: casts {n.get('castVoice',0)}  bites {n.get('biteVoice',0)} (killing {n.get('killBiteVoice',0)}; "
          f"n {', '.join(f'{k[5:]}:{v}' for k, v in ns.items())})  roots {n.get('rootVoice',0)}  withers {n.get('witherVoice',0)} "
          f"on {n.get('clockCloses',0)} clock closes  silent death closes {n.get('deathSilent',0)}  "
          f"ward shatters voiced in the vine's tick {n.get('shatterVoice',0)}   run totals {R['bwAll']}")
    checks.append((10, "stage 6 voice: one cast voice a cast, one bite voice a bite at the foe's stacks, one root voice a root, "
                       "one wither voice a clock close and none on a death; nothing else sounds; every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "biteVoice", "rootVoice", "witherVoice", "deathSilent"))))
if R.get("stage6p"):
    print(f"  stage 6 picture: tickTwine calls clean {n.get('twineOk',0)}  root beats {n.get('rootBeat',0)}  "
          f"held steps {n.get('heldOk',0)}  drawn frames {n.get('drawOk',0)} ({n.get('drawPic',0)} with the picture up, "
          f"{n.get('drawPicStop',0)} of them in a hit stop)" + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((11, "stage 6 picture: tickTwine writes no sim field and draws no RNG; one write-only beat a root and none "
                       "on another close; twineHeld exactly while the root holds; no drawn frame throws or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("twineOk", "rootBeat", "heldOk"))
                   and (n.get("drawPic", 0) > 0 if R.get("drawOn") else True)))
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
