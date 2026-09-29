#!/usr/bin/env python
"""REBUTTAL'S PROBE -- one check per sentence of v70 §1 / §5 and the brief's §0-§1,
read INSIDE the hooks.

    python lodestone_probe.py --game <link>        (stage 2 on: sc-lodestone-runes and after)

Wraps `tickRunes`, `resolveHit`, `fireUlt`, `tickCharge` and `step` on the Match
prototype and reads each event where it happens. Runs Lodestone against every
other relic, both sides, and prints N/N. The checks follow the link's own
numbers, so the same probe gates stages 2 and 3 (hurl 0 / 700) and stage 5.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [0] the numbers: the link's ult block not the design's (brief §0, design §5)
      -- charge 14 (the lab's 16 on the game's clock, v102 §0), dur 8, pad 1.5,
      cd 0.5, hex 1, hurl 0 (stage 2) or 700 -- so a mis-carried number fails
      the probe on its own after a carry, not only the builder's check
  [1] "for a duration": a window that is not `dur` long on the window clock
      (its frame count on a clock close is not the count that reaches dur by
      dt), that ticked on a frozen step, that outlived either death; any relic
      but Lodestone carrying `ultRunes` / `runeTally`. Closes on a death are
      counted apart: the CASTER's (a foe's side channel killed it before the
      runes ticked) and the FOE's (unreachable on this engine: Lodestone kills
      only with a blow, in `tickHits` after `tickRunes`, and that step's
      `checkEnd` ends the match). A kill in `tickHits` -- either hammer's --
      ends the match with `ultRunes` still set; the probe counts those fights
      and steps each 240 verdict steps further to show the field stays set
      (the stage-6 picture must gate on `!m.over`). Printed, not a failure:
      the simulation reads nothing after the verdict.
  [2] "every time the enemy's ball touches a wall": a touch with the foe's
      centre outside inset + R + pad of every side of the CURRENT hall, or a
      touch on a dead or pinned foe
  [3] "once per 0.5s": two touches of one window closer than `cd` on the window
      clock, or a frame with the foe on a wall, alive, unpinned and the
      cooldown clearly past, and no touch
  Both [1] and [3] read the PROBE'S OWN window clock -- its own sum of dt over
  the ticks it saw -- never the engine's `Z.t` or `Z.cd`, so an engine clock
  that runs fast or slow reads against the clock it should have kept.
  [4] "the rune ... hexes them": a touch that is not exactly one
      apply("hex", hex, <side letter>) on the foe, or whose `status.hex` is not
      that apply's own result (stacks, clock, source); any application, or any
      change to `status.hex`, on a frame with no touch
  [5] "and hurls them straight back at the hammer": at hurl > 0 a touch whose
      foe velocity is not EXACTLY hurl x unit(caster - foe) -- assigned, the
      old velocity discarded -- and not 700 +-1 in speed; any velocity change on
      a frame with no touch (the closing frame included), or at hurl 0
  [6] "The walls do no damage -- they hand the enemy back": a hurt, a
      resolveHit, a beat, a hit stop; ANY change to the foe's whole state but
      `vx`, `vy` ([5]) and `status.hex` ([4]) -- a deep snapshot of its own
      enumerable state before and after every rune tick (review round 3: a
      fixed field list let a drained charge and a flipped spin through); ANY
      change to the Match's whole state
  [7] "the caster's own touches do nothing": the tick changing ANYTHING on
      the caster -- its whole state, deep, but the window's own record
      (`ultRunes`, `runeTally`) -- counted on the window frames the caster is
      itself on a wall. Read on the frames the runes hurt nobody: a hurt
      already fails [6], and a ward it breaks bursts at its source, the
      caster -- [6]'s consequence, not a second failure.
  [8] "the hammer's own knock": a Lodestone blow whose damage is not the blade x
      dmgMul x jitter x dmgTaken, rounded, crit included -- rebuilt from the
      captured draws, in the window and out of it
  [9] "the next cast does not wait for anything": a cast while the walls are
      lit, or a tickCharge that leaves the charge at or over `ult.charge` with
      the caster alive (a cast held back)
  STAGE 6 (the picture and the voice, sc-lodestone-b205-fx). Each check runs
  only on a link that carries its half, read off the page itself:
  [10] THE VOICE (on when "lodestone-touch" is in AC.SFX.play.toString()): a
      Lodestone cast without exactly one `ult`/lodestone voice inside fireUlt,
      or a Lodestone voice inside any other relic's cast; a tickRunes call
      whose voices are not exactly its events', in order -- a touch: the
      `lodestone-touch` snap whose `n` is the count the foe carries after
      THAT touch's hex (read in the apply and again when the voice plays),
      then the school's `hex-snap` under it; a window that closes BY ITS CLOCK
      with both fighters alive: one `lodestone-close`; a window that closes on
      a death: nothing (v70 6.2's close is the clock's) -- and any other voice
      at all inside tickRunes (it hurts nobody, so no ward shatter's own crit
      voice can play there: [6] fails any hurt first); and every Lodestone
      voice of the run accounted for by those events (none plays anywhere
      else: not at the verdict, where a kill leaves the window lit)
  [11] THE PICTURE (on when the Match has `tickLode`): `tickLode`, the
      picture's one hook on the step, changing any sim field of either
      fighter or the match (bodies, statuses, window, tally; clock, stop,
      verdict, holds, hall, beats, shots) or drawing the RNG; the walls lit
      (lodeFade exactly 1) other than exactly while the window is open, the
      match not over and the caster alive; a touch without exactly one new
      record at the foe's spot at the touch, carrying the walls the touch
      test met (inset + R + pad, read at the touch) and its own count, clock
      and match time, or a record with no touch; a live touch without a HEX
      tag on the board reading the foe's count; a touch on the kill's step
      that draws a record or adds or recounts a hex tag (the shatter owns
      that frame); walls lit at `over` not dark 0.51s into the verdict; a
      touch the picture never saw; and on the DRAWN subset (the first seed,
      both sides, every foe, through the kill and the verdict) a drawn frame
      that throws, draws the match's RNG or changes any sim field
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=102001)
ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const AW = C.arena.w, AH = C.arena.h, critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickRunes, oResolve = P.resolveHit, oFire = P.fireUlt, oStep = P.step, oCharge = P.tickCharge;
  const lastTouch = new WeakMap(), win = new WeakMap();   // Z -> last touch t; Z -> {ticks, steps}
  const snap = (st, skip) => JSON.stringify(Object.keys(st).sort().filter(k => k !== skip).map(k => [k, st[k].stacks, st[k].t]));
  const onWall = (x, y, ins, e) => x <= ins + R + e || x >= AW - ins - R - e || y <= ins + R + e || y >= AH - ins - R - e;
  let ticked = false, per = null;
  /* the window's frame count on a clock close: Z.t starts at 0 and gains dt a
     tick; the tick on which it reaches dur is the close, not a frame */
  const closeTicks = (dur) => { let t = 0, k = 0; while (t < dur){ t += DT; k++; } return k; };

  /* THE WHOLE STATE (review round 3). [6] and [7] once compared a fixed list
     of fields, so a rune that drained the foe's charge or flipped its spin
     passed. Now every rune tick is read against a DEEP snapshot of both
     fighters' own enumerable state and the Match's, taken just before the
     tick and just after it: numbers, booleans, strings, null / undefined,
     and plain objects, arrays, typed arrays, Maps and Sets of those, walked
     to the bottom. A Fighter that is not one of the two (a Twinshade shade)
     is walked like one; the two fighters themselves, met inside another
     field, are recorded by identity (each has its own snapshot); any other
     class instance is recorded by identity and NAMED in the output (a blind
     spot is printed, never silent); a cycle is a marker. Skipped: the shared
     weapon `w` and the affinity `aff` (tables, not state), and exactly what
     the design lets a tick change -- on the foe `vx`, `vy` ([5] rebuilds
     them exactly on every frame) and `status.hex` ([4] rebuilds it exactly);
     on the caster `ultRunes` and `runeTally` (the window's own record, read
     by [1] and [3]); on the Match nothing (the fighters `a`, `b` have their
     own). Any other difference fails [6] (the foe or the Match) or [7] (the
     caster), naming the field. THE ONE LIMIT, for speed: an array longer
     than TAIL (16) -- the Match's growing logs, `beats`, `fx`, `motes`,
     `drains` -- is read as its length and its last TAIL entries, walked; an
     append is caught, a rewrite of an old entry is not. The fields it
     applies to are printed. Pure reads: `Object.keys` lists own
     enumerable properties, and the engine's class getters live on the
     prototypes, so the walk calls none of them. */
  const OB = Symbol("{"), CB = Symbol("}"), OA = Symbol("["), CA = Symbol("]");
  const ids = new WeakMap(); let nid = 0;
  const idOf = (o) => { let k = ids.get(o); if (k === undefined){ k = ++nid; ids.set(o, k); } return k; };
  const blind = new Set(), tailed = {}, TAIL = 16;
  let FP = null, M2 = null;                     // Fighter.prototype; the match's two fighters
  const walk = (v, out, seen, own, key) => {
    const t = typeof v;
    if (t === "function"){ out.push("<fn>"); return; }
    if (v === null || t !== "object"){ out.push(v); return; }
    if (seen.includes(v)){ out.push("<cycle>"); return; }
    if (Array.isArray(v)){
      seen.push(v); out.push(OA, v.length);
      let i0 = 0;
      if (v.length > TAIL){ i0 = v.length - TAIL; const wh = own + "." + key; if (!tailed[wh]) tailed[wh] = 1; }
      for (let i = i0; i < v.length; i++) walk(v[i], out, seen, own, key);
      out.push(CA); seen.pop(); return;
    }
    if (ArrayBuffer.isView(v)){ out.push(OA, v.length); for (let i = 0; i < v.length; i++) out.push(v[i]); out.push(CA); return; }
    if (v instanceof Map || v instanceof Set){
      seen.push(v); out.push(OA, v.size);
      for (const e of v) walk(e, out, seen, own, key);
      out.push(CA); seen.pop(); return;
    }
    const p = Object.getPrototypeOf(v);
    if (p === FP && M2 && (v === M2[0] || v === M2[1])){ out.push(v === M2[0] ? "<fighter a>" : "<fighter b>"); return; }
    if (p !== Object.prototype && p !== null && p !== FP){
      const nm = (p.constructor && p.constructor.name) || "?";
      out.push("<" + nm + "#" + idOf(v) + ">"); blind.add(own + "." + key + " : " + nm); return;
    }
    seen.push(v); out.push(OB);
    const ks = Object.keys(v);
    for (let i = 0; i < ks.length; i++){
      const k = ks[i];
      if (p === FP && (k === "w" || k === "aff")) continue;
      out.push(k); walk(v[k], out, seen, own, key);
    }
    out.push(CB); seen.pop();
  };
  /* a snapshot: the flat walk, and each top-level key's span in it */
  const snapTop = (o, skip, noHex, where) => {
    const out = [], seg = [], seen = [o];
    const ks = Object.keys(o);
    for (let i = 0; i < ks.length; i++){
      const k = ks[i];
      if (skip.has(k)) continue;
      const s0 = out.length;
      if (noHex && k === "status"){
        const st = o.status, sk = Object.keys(st); out.push(OB);
        for (let j = 0; j < sk.length; j++) if (sk[j] !== "hex"){ out.push(sk[j]); walk(st[sk[j]], out, seen, where, "status"); }
        out.push(CB);
      } else walk(o[k], out, seen, where, k);
      seg.push(k, s0, out.length);
    }
    return { out, seg };
  };
  /* the top-level keys whose state differs ([] when none does) */
  const changed = (A, B) => {
    if (A.out.length === B.out.length && A.seg.length === B.seg.length){
      let eq = true;
      for (let i = 0; i < A.out.length; i++) if (!Object.is(A.out[i], B.out[i])){ eq = false; break; }
      if (eq) return [];
    }
    const m = new Map(); for (let i = 0; i < A.seg.length; i += 3) m.set(A.seg[i], [A.seg[i + 1], A.seg[i + 2]]);
    const got = [];
    for (let i = 0; i < B.seg.length; i += 3){
      const k = B.seg[i], b0 = B.seg[i + 1], b1 = B.seg[i + 2], sa = m.get(k);
      if (!sa){ got.push("+" + k); continue; }
      m.delete(k);
      if (sa[1] - sa[0] !== b1 - b0){ got.push(k); continue; }
      for (let j = 0; j < b1 - b0; j++) if (!Object.is(A.out[sa[0] + j], B.out[b0 + j])){ got.push(k); break; }
    }
    for (const k of m.keys()) got.push("-" + k);
    return got;
  };
  const SKIP_FOE = new Set(["w", "aff", "vx", "vy"]), SKIP_CASTER = new Set(["w", "aff", "ultRunes", "runeTally"]);
  const SKIP_MATCH = new Set(["a", "b"]);
  const canon = (o) => o == null ? "null" : JSON.stringify(Object.keys(o).sort().map(k => [k, o[k]]));

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /lodestone-touch/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickLode === "function";
  const voices = [], lodeAll = {}, oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oLode = P.tickLode;
  let curM = null;
  const ldVoice = q => !!(q && typeof q.w === "string" && /^lodestone/.test(q.w));
  const vname = x => x[0] === "ult" && x[1] && x[1].w
    ? (x[1].w === "lodestone-touch" ? "lodestone-touch:" + x[1].n + "@" + x[2] : x[1].w) : x[0];
  /* every voice, with the count Lodestone's foe carries at the moment a touch's snap plays */
  if (stage6v) AC.SFX.play = function(kind, q){
    let atN = null;
    if (curM && kind === "ult" && q && q.w === "lodestone-touch"){
      const me = curM.a.w.id === "lodestone" ? curM.a : curM.b, foe = me === curM.a ? curM.b : curM.a;
      atN = foe.stacks("hex");
    }
    voices.push([kind, q ? Object.assign({}, q) : q, atN]);
    if (kind === "ult" && ldVoice(q)) lodeAll[q.w] = (lodeAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, statuses,
     window and tally, and the match's clock, stop, verdict, holds, hall, beats
     and shots. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "stunDR", "alive",
              "hits", "dealt", "crits", "spinDir", "hexClock", "pin", "burden"];
  const simSnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null,
               !!m.latch, !!m.splitHold, m.inset, m.beats ? m.beats.length : null,
               (m.shots || []).map(q => [q.x, q.y, q.vx, q.vy])];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t, f.status[k].src]));
      o.push(f.ultRunes ? [f.ultRunes.t, f.ultRunes.dur, f.ultRunes.cd] : null, f.runeTally ? JSON.stringify(f.runeTally) : null);
    }
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 30), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 30), i + 30)); };
  /* the touches tickRunes made that the picture has not seen yet, a caster's side: the foe's spot
     and the hall AT THE TOUCH TEST */
  const pendTouch = { a: [], b: [] };
  const wallsOf = (x, y, ins, e) => { const w = [];
    if (y <= ins + R + e) w.push(0); if (x >= AW - ins - R - e) w.push(1);
    if (y >= AH - ins - R - e) w.push(2); if (x <= ins + R + e) w.push(3); return w; };
  if (stage6p) P.tickLode = function(dt){
    const s0 = simSnap(this), oR = this.rng, oMR = Math.random;
    const pre = [this.a, this.b].map(f => ({ f, seen: f.lodeSeen, recs: (f.lodeFx || []).slice(),
                                             tags: this.tags.filter(g => g.key === "hex").map(g => [g, g.val]) }));
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oLode.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(11, `tickLode drew the RNG ${drew}x`);
    const s1 = simSnap(this);
    if (s1 !== s0) fail(11, "tickLode changed the sim: " + firstDiff(s0, s1)); else inc("lodeOk");
    for (const p of pre){
      const f = p.f, side = f === this.a ? "a" : "b", foe = f === this.a ? this.b : this.a, T = f.runeTally;
      /* THE WALLS ARE LIT EXACTLY WHILE THE WINDOW IS (and the match runs, and the caster stands) */
      const live = !!(f.ultRunes && !this.over && f.alive);
      if ((f.lodeFade === 1) !== live) fail(11, `lodeFade ${f.lodeFade} with the window ${live ? "live" : "not live"} (over ${this.over}, alive ${f.alive})`);
      else if (live) inc("wallsLit"); else if (f.lodeFade > 0) inc("wallsGoingDark");
      const fresh = f.lodeFx.filter(q => !p.recs.includes(q));
      if (!T){ if (fresh.length || f.lodeFade > 0) fail(11, "a picture with no runes"); continue; }
      const Q = pendTouch[side];
      if (f.lodeSeen !== T.touches) fail(11, `lodeSeen ${f.lodeSeen} after tickLode, the tally's touches ${T.touches}`);
      const rise = T.touches - p.seen;
      if (rise > 0){
        if (Q.length !== rise){ fail(11, `${rise} touch(es) by the tally, ${Q.length} seen in tickRunes`); Q.length = 0; continue; }
        const t = Q[Q.length - 1];
        if (this.over || !foe.alive){
          /* A TOUCH ON THE KILL'S STEP DRAWS NOTHING: no record, no hex tag added or recounted */
          const now = this.tags.filter(g => g.key === "hex");
          const added = now.filter(g => !p.tags.some(x => x[0] === g)).length;
          const recount = p.tags.filter(x => x[0].val !== x[1]).length;
          if (fresh.length || added || recount) fail(11, `a touch on the kill's step drew: ${fresh.length} record(s), ${added} tag(s) added, ${recount} recounted`);
          else inc("killTouchUndrawn");
        } else if (fresh.length !== 1) fail(11, `${fresh.length} new record(s) for ${rise} touch(es)`);
        else {
          /* ONE RECORD, AT THE FOE'S SPOT AT THE TOUCH, ON THE WALLS THE TOUCH TEST MET */
          const q = fresh[0], want = wallsOf(t.x, t.y, t.ins, t.pad);
          if (q.x !== t.x || q.y !== t.y) fail(11, `a flare at (${q.x}, ${q.y}); the touch at (${t.x}, ${t.y})`);
          else if (JSON.stringify(q.walls) !== JSON.stringify(want)) fail(11, `walls ${JSON.stringify(q.walls)}, the touch met ${JSON.stringify(want)}`);
          else if (q.k !== T.touches || q.t !== 0 || q.t0 !== this.t) fail(11, `a record's count ${q.k} (touches ${T.touches}), clock ${q.t}, match time ${q.t0} (now ${this.t})`);
          else { inc("recOk"); if (want.length > 1) inc("recCorner"); if (t.ins > 0) inc("recInset"); }
          /* THE HEX TAG PRINTS THE FOE'S COUNT */
          if (foe.hp > 0){
            const k = foe.stacks("hex");
            if (!this.tags.some(g => g.key === "hex" && g.val === k)) fail(11, `no hex tag reads the foe's ${k}`);
            else { inc("tagOk"); if (k < AC.STATUS.hex.maxStacks) inc("tagUnderCap"); }
          }
        }
        Q.length = 0;
      } else if (fresh.length) fail(11, `${fresh.length} record(s) with no touch`);
    }
    return r;
  };

  P.step = function(dt){
    if (this.over) return oStep.call(this, dt);   // the verdict: decay only, the runes never tick
    const fz = this.hitStop > 0 || !!this.latch || !!this.splitHold;
    const lit = [this.a, this.b].filter(f => f.ultRunes);
    for (const f of lit){ if (fz) inc("winFrozen"); else inc("winLive");
      const W = win.get(f.ultRunes); if (W) W.steps++; }
    ticked = false;
    const r = oStep.call(this, dt);
    if (fz && ticked) fail(1, "the runes ticked on a frozen step");
    return r;
  };
  P.fireUlt = function(f, foe){
    if (f.w.id === "lodestone"){
      if (f.ultRunes) fail(9, "cast while the walls are lit"); else inc("castOk");
    }
    const v0 = voices.length;
    const r = oFire.call(this, f, foe);
    /* [10] THE CAST: exactly one Lodestone voice inside a Lodestone fireUlt, the cast's own; none in any other */
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ldVoice(x[1]));
      if (f.w.id === "lodestone"){
        if (cv.length !== 1 || cv[0][1].w !== "lodestone") fail(10, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
        else inc("castVoice");
      } else if (cv.length) fail(10, `${f.w.id}'s cast played ${JSON.stringify(cv.map(vname))}`);
    }
    if (f.ultRunes && !win.has(f.ultRunes)) win.set(f.ultRunes, { ticks: 0, steps: 0, t: 0 });
    return r;
  };
  P.tickCharge = function(f, foe, dt){
    const r = oCharge.call(this, f, foe, dt);
    if (f.w && f.w.id === "lodestone" && f.alive && !this.over){
      if (f.charge >= f.w.ult.charge) fail(9, `the charge sits at ${f.charge.toFixed(3)} >= ${f.w.ult.charge}: a cast held back`);
      else inc("chargeOk");
    }
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!self.w || self.w.id !== "lodestone" || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultRunes, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
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
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(8, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    return r;
  };
  P.tickRunes = function(dt){
    ticked = true;
    const pre = [];
    FP = Object.getPrototypeOf(this.a); M2 = [this.a, this.b];
    let mS = null;
    for (const f of [this.a, this.b]){
      if ((f.ultRunes || f.runeTally) && f.w.id !== "lodestone") fail(1, `${f.w.id} carries ultRunes/runeTally`);
      const Z = f.ultRunes;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a, T = f.runeTally;
      /* THE PROBE'S OWN WINDOW CLOCK: its own sum of dt over the ticks it saw,
         never the engine's Z.t -- so a window or a cooldown that runs fast or
         slow in the engine reads against the clock it should have kept. */
      let W = win.get(Z); if (!W){ W = { ticks: 0, steps: 0, t: 0 }; win.set(Z, W); }
      pre.push({ f, foe, Z, W, t1: W.t + dt, fAlive: f.alive, foeAlive: foe.alive, ins: this.inset,
                 x: f.x, y: f.y, vx: f.vx, vy: f.vy, hp: f.hp, sh: f.shield, stun: f.stun, pin: f.pin, st: snap(f.status),
                 fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy, fhp: foe.hp, fsh: foe.shield, fstun: foe.stun,
                 fpin: foe.pin, fpinMax: foe.pinMax, fpinV: foe.pinV, fpinFree: foe.pinFree, fst: snap(foe.status, "hex"),
                 hex0: foe.stacks("hex"), touches: T.touches, hexes: T.hexes, hurls: T.hurls,
                 /* THE WHOLE STATE, before the tick and before the probe wraps anything */
                 cS: snapTop(f, SKIP_CASTER, false, "caster"), fS: snapTop(foe, SKIP_FOE, true, "foe"),
                 hexPre: foe.status.hex ? Object.assign({}, foe.status.hex) : null });
      if (!mS) mS = snapTop(this, SKIP_MATCH, false, "match");
    }
    const hs0 = this.hitStop, hurts = [], beats = [], applies = [];
    let rh = 0;
    const oHurt = this.hurt, oBeat = this.beat, oRH = this.resolveHit;
    this.hurt = function(t, d, s){ hurts.push([t, d]); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.resolveHit = function(){ rh++; return oRH.apply(this, arguments); };
    const wrapped = [];
    for (const p of pre) for (const who of [p.f, p.foe]) if (!wrapped.includes(who)){
      const o = who.apply; who.apply = function(k, nn, src){ const e = [who, k, nn, src]; applies.push(e); const rr = o.call(this, k, nn, src); e.push(who.stacks(k)); return rr; };
      wrapped.push(who);
    }
    const v0 = voices.length, vexp = [];
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; delete this.resolveHit; for (const w of wrapped) delete w.apply; }
    if (hurts.length) fail(6, `the runes hurt ${hurts.length}x`);
    if (beats.length) fail(6, `the runes filed ${beats.length} beat(s)`);
    if (rh) fail(6, `the runes called resolveHit ${rh}x`);
    if (this.hitStop !== hs0) fail(6, `hitStop ${hs0} -> ${this.hitStop}`);
    /* [6] THE MATCH'S WHOLE STATE: a rune tick changes nothing on the Match */
    if (mS){
      const dM = changed(mS, snapTop(this, SKIP_MATCH, false, "match"));
      if (dM.length) fail(6, `the tick changed the match's ${dM.join(", ")}`); else inc("wholeMatchOk");
    }
    const cap = AC.STATUS.hex.maxStacks, hexDur = AC.STATUS.hex.dur;
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult, T = f.runeTally, side = f === this.a ? "a" : "b";
      const W = p.W; W.ticks++; W.t = p.t1;
      const mine = applies.filter(x => x[0] === foe), selfA = applies.filter(x => x[0] === f);
      const dT = T.touches - p.touches;
      /* [7] THE CASTER IS UNTOUCHED ON EVERY FRAME -- its whole state but the
         window's own record -- read on the frames the runes hurt nobody: a
         hurt is [6]'s failure, and a ward that hurt breaks bursts at its
         SOURCE (`shatter(f, src)`: hp and a knock on the caster), which is
         [6]'s consequence, not a caster's touch. */
      const dC = changed(p.cS, snapTop(f, SKIP_CASTER, false, "caster"));
      if (hurts.length) inc("casterUnderHurt");
      else if (f.x !== p.x || f.y !== p.y || f.vx !== p.vx || f.vy !== p.vy || f.hp !== p.hp || f.shield !== p.sh ||
          f.stun !== p.stun || f.pin !== p.pin || snap(f.status) !== p.st || selfA.length || dC.length)
        fail(7, `the tick changed the caster (v ${foe.w.id})${dC.length ? ": " + dC.join(", ") : ""}`);
      else inc("casterOk");
      /* [6] THE FOE'S WHOLE STATE but vx, vy ([5]) and status.hex ([4]), on
         every frame of the window, the closing one included */
      const dF = changed(p.fS, snapTop(foe, SKIP_FOE, true, "foe"));
      if (dF.length) fail(6, `the tick changed the foe's ${dF.join(", ")} (${foe.w.id})`); else inc("wholeFoeOk");
      /* [4] the foe's hex, EXACTLY: apply("hex", hex, side)'s own result on a
         touch, untouched on every other frame */
      let hexWant = p.hexPre;
      if (dT === 1 && u.hex > 0){
        hexWant = Object.assign({}, p.hexPre || { stacks: 0, t: 0 });
        if (hexWant.stacks < cap) hexWant.stacks = Math.min(cap, hexWant.stacks + u.hex);
        hexWant.t = hexDur; hexWant.src = side;
      }
      const hexOk = canon(foe.status.hex) === canon(hexWant);
      if (p.t1 >= Z.dur || !p.fAlive || !p.foeAlive){
        /* THE CLOSE */
        vexp.push(p.fAlive && p.foeAlive ? { v: ["lodestone-close"], clock: true } : { v: [], death: true });
        if (f.ultRunes){ fail(1, "the window did not close"); continue; }
        if (p.fAlive && p.foeAlive && p.t1 < Z.dur - 1e-9) fail(1, "closed early");
        if (dT || mine.length) fail(3, "a touch on the closing frame");
        if (!dT && !hexOk) fail(4, "the foe's hex changed on the closing frame");
        if (!dT && (foe.vx !== p.fvx || foe.vy !== p.fvy)) fail(5, "a velocity change on the closing frame");
        inc("closes");
        if (p.fAlive && p.foeAlive){
          inc("clockCloses");
          const want = closeTicks(Z.dur);
          if (!W || W.ticks !== want) fail(1, `a clock close after ${W && W.ticks} ticks, want ${want}`);
          else { inc("clockOk"); inc("winSteps", W.steps); }
        } else { inc("deathCloses"); inc(!p.fAlive ? "casterDeathCloses" : "foeDeathCloses"); }
        continue;
      }
      /* A WINDOW FRAME */
      inc("frames");
      if (!f.ultRunes){ fail(1, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      inc("stkFrames", p.hex0);
      if (onWall(p.x, p.y, p.ins, u.pad)) inc("casterWallFrames");
      /* THE COOLDOWN ON THE PROBE'S CLOCK: the time since this window's last
         touch. `clear` = a touch is allowed; `due` = clearly past it, so a
         clear touching frame without a touch is a miss (the float edge at
         exactly cd is neither). */
      const lt = lastTouch.get(Z), since = lt === undefined ? Infinity : p.t1 - lt;
      const clear = since >= u.cd - 1e-9, due = since >= u.cd + 1e-9;
      const wall = onWall(p.fx, p.fy, p.ins, u.pad), pinned = p.fpin > 0;
      if (dT > 1) fail(3, `${dT} touches in one frame`);
      if (dT){
        inc("touches"); if (p.ins > 0) inc("insetTouches");
        /* [2] THE CONTACT */
        if (!wall) fail(2, `a touch off the wall: (${p.fx.toFixed(2)}, ${p.fy.toFixed(2)}) inset ${p.ins.toFixed(2)}`);
        else if (pinned) fail(2, "a touch on a pinned foe");
        else inc("wallOk");
        /* [3] THE CADENCE */
        if (!clear) fail(3, `touches ${since.toFixed(4)}s apart on the window clock`);
        else inc("cadenceOk");
        lastTouch.set(Z, p.t1);
        /* [4] THE HEX */
        if (u.hex > 0){
          if (mine.length !== 1 || mine[0][1] !== "hex" || mine[0][2] !== u.hex) fail(4, `applies ${JSON.stringify(mine.map(x => [x[1], x[2]]))}, want [["hex",${u.hex}]]`);
          else if (mine[0][3] !== side) fail(4, `source ${typeof mine[0][3] === "object" ? "a Fighter" : JSON.stringify(mine[0][3])}`);
          else if (T.hexes - p.hexes !== u.hex) fail(4, "the tally's hexes != touches x hex");
          else if (foe.stacks("hex") !== Math.min(AC.STATUS.hex.maxStacks, p.hex0 + u.hex)) fail(4, `hex ${p.hex0} -> ${foe.stacks("hex")}`);
          else if (!hexOk) fail(4, `status.hex ${canon(foe.status.hex)}, want apply's own ${canon(hexWant)}`);
          else inc("hexOk");
        } else if (mine.length || !hexOk) fail(4, "an application at hex 0");
        /* [10] the touch's voice (at the count its hex leaves), the hex-snap under it; [11] the touch, for the picture */
        if (u.hex > 0){ const k = mine.length === 1 ? mine[0][4] : "?"; vexp.push({ v: ["lodestone-touch:" + k + "@" + k, "hex-snap"], n: k }); }
        pendTouch[side].push({ x: p.fx, y: p.fy, ins: p.ins, pad: u.pad });
        /* [5] THE HURL */
        if (u.hurl > 0){
          const dx = p.x - p.fx, dy = p.y - p.fy, d = Math.hypot(dx, dy) || 1;
          const wx = dx / d * u.hurl, wy = dy / d * u.hurl, sp = Math.hypot(foe.vx, foe.vy);
          if (foe.vx !== wx || foe.vy !== wy) fail(5, `v (${foe.vx.toFixed(2)}, ${foe.vy.toFixed(2)}) want (${wx.toFixed(2)}, ${wy.toFixed(2)}) from (${p.fvx.toFixed(2)}, ${p.fvy.toFixed(2)})`);
          else if (Math.abs(sp - 700) > 1) fail(5, `a hurl at ${sp.toFixed(3)}, not 700 +-1`);
          else { inc("hurlOk"); if (sp < n.spMin || n.spMin === undefined) n.spMin = sp; if (sp > n.spMax || n.spMax === undefined) n.spMax = sp; }
          if (T.hurls - p.hurls !== 1) fail(5, "the tally's hurls != touches");
        } else if (foe.vx !== p.fvx || foe.vy !== p.fvy) fail(5, "a velocity change at hurl 0");
      } else {
        if (wall && due && !pinned && p.foeAlive) fail(3, `on the wall with the cooldown clear, and no touch (inset ${p.ins.toFixed(2)})`);
        if (wall && !clear) inc("wallCdFrames");
        if (mine.length) fail(4, "an application on a frame with no touch");
        else if (!hexOk) fail(4, "the foe's hex changed on a frame with no touch");
        if (foe.vx !== p.fvx || foe.vy !== p.fvy) fail(5, "a velocity change on a frame with no touch");
      }
      /* [6] NOTHING ELSE */
      if (foe.x !== p.fx || foe.y !== p.fy || foe.hp !== p.fhp || foe.shield !== p.fsh || foe.stun !== p.fstun ||
          foe.pin !== p.fpin || foe.pinMax !== p.fpinMax || foe.pinV !== p.fpinV || foe.pinFree !== p.fpinFree ||
          snap(foe.status, "hex") !== p.fst) fail(6, "the tick changed the foe's position, hp, shield, stun, pin or a status but hex");
      else inc("nothingElseOk");
    }
    /* [10] THE CALL'S VOICES: exactly its events', in order, and nothing else */
    if (stage6v){
      const got = voices.slice(v0).map(vname), want = [];
      for (const e of vexp) want.push(...e.v);
      if (JSON.stringify(got) !== JSON.stringify(want)) fail(10, `tickRunes voiced ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
      else for (const e of vexp){
        if (e.clock) inc("closeVoice"); else if (e.death) inc("deathCloseSilent");
        else { inc("touchVoice"); inc("touchN" + e.n); }
      }
    }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "lodestone");
  const T = { casts: 0, frames: 0, touches: 0, hexes: 0, hurls: 0, foeStk: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), through the kill and the verdict,
     with the sim read before and after each frame and the match's RNG
     watched. The post chain is off: this asks what a draw WRITES, not what
     it looks like (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.lodeFade > 0 || (q.lodeFx && q.lodeFx.length));
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    try { AC.__draw(m); } catch (e){ fail(11, "a drawn frame threw: " + String((e && e.message) || e)); }
    finally { m.rng = oR; }
    const s1 = simSnap(m);
    if (dr) fail(11, `a drawn frame drew the match's RNG ${dr}x`);
    else if (s1 !== s0) fail(11, "a drawn frame changed the sim: " + firstDiff(s0, s1));
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "lodestone", sd) : new AC.Match("lodestone", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    curM = m; voices.length = 0; pendTouch.a.length = 0; pendTouch.b.length = 0;
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.runeTally) for (const k in T) T[k] += me.runeTally[k];
    /* THE VERDICT (stage 6): 0.51s past `over`. Walls lit at `over` are dark
       in it; every touch has been seen by the picture. */
    if (stage6p && m.over){
      const upAtOver = me.lodeFade > 0;
      for (let k = 0; k < 61; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
      if (upAtOver){ if (me.lodeFade !== 0) fail(11, `walls lit at \`over\` still at ${me.lodeFade} 0.51s into the verdict`); else inc("darkAtVerdict"); }
      if (pendTouch.a.length || pendTouch.b.length) fail(11, `${pendTouch.a.length + pendTouch.b.length} touch(es) the picture never saw`);
    }
    /* THE VERDICT: a kill in tickHits ends the match before the runes see the
       death, so the field can outlive the fight. Counted, then stepped on. */
    if (m.over && me.ultRunes){
      inc("litAtVerdict"); inc(m.winner === me ? "litWin" : "litLoss");
      const Z0 = me.ultRunes, t0 = Z0.t;
      for (let k = 0; k < 240; k++) m.step(DT);
      if (me.ultRunes === Z0 && Z0.t === t0) inc("litThroughVerdict");
    }
  }
  P.tickRunes = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep; P.tickCharge = oCharge;
  curM = null;
  if (stage6v){
    if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
    /* EVERY LODESTONE VOICE OF THE RUN, ACCOUNTED FOR by its event (every fight, every verdict). */
    const want = { "lodestone": n.castVoice || 0, "lodestone-touch": n.touchVoice || 0, "lodestone-close": n.closeVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(lodeAll)]))
      if ((lodeAll[k] || 0) !== (want[k] || 0)) fail(10, `${lodeAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickLode = oLode;
  const u = AC.WEAPONS.find(w => w.id === "lodestone").ult;
  return { n, bad, T, fights, win: wins / decided, stage6v, stage6p, drawOn, lodeAll, blowsIn: bin / fights, blowsOut: bout / fights, blind: [...blind].sort(), tailed: Object.keys(tailed).sort(),
           closeTicks: closeTicks(u.dur),
           u: { charge: u.charge, dur: u.dur, pad: u.pad, cd: u.cd, hex: u.hex, hurl: u.hurl,
                dmg: AC.WEAPONS.find(w => w.id === "lodestone").dmg } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRunes === 'function'"):
        raise SystemExit("no tickRunes in this build -- not a Rebuttal link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, n.get("frames", 0))
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
cc = max(1, n.get("clockOk", 0))
print(f"\nREBUTTAL PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Lodestone both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Lodestone win {R['win']:.1%}")
print(f"  per cast: touches {T['touches']/casts:.2f}  hexes {T['hexes']/casts:.2f}  hurls {T['hurls']/casts:.2f}   "
      f"foe hex stacks on a window frame {T['foeStk']/max(1,T['frames']):.2f}   touches on a closed-in hall "
      f"{n.get('insetTouches',0)} of {n.get('touches',0)}")
print(f"  hurl speed {n.get('spMin',0):.6f} .. {n.get('spMax',0):.6f}   caster on a wall {n.get('casterWallFrames',0)} window frames "
      f"(its touches do nothing)   wall frames under the cooldown {n.get('wallCdFrames',0)}   "
      f"caster frames under a rune hurt {n.get('casterUnderHurt',0)}")
print(f"  closes on a death: the caster's {n.get('casterDeathCloses',0)}, the foe's {n.get('foeDeathCloses',0)} "
      f"(unreachable: Lodestone kills only in tickHits, after tickRunes)   fights ending with the walls STILL LIT "
      f"{n.get('litAtVerdict',0)} of {R['fights']} (Lodestone won {n.get('litWin',0)}, lost {n.get('litLoss',0)}); "
      f"still lit 240 verdict steps on {n.get('litThroughVerdict',0)}")
print(f"  window: {R['closeTicks']-1} window frames a clock close ({n.get('clockOk',0)} clock closes, {n.get('deathCloses',0)} on a death); "
      f"{n.get('winSteps',0)/cc/120:.2f}s of match time a clock-closed window   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  whole-state reads: the foe {n.get('wholeFoeOk',0)}, the caster {n.get('casterOk',0)}, the Match {n.get('wholeMatchOk',0)} "
      f"rune ticks unchanged; recorded by identity only (never walked): {R['blind'] or 'nothing'}; "
      f"arrays read as length + last 16: {', '.join(R['tailed']) or 'none'}")
NUM = {"charge": 14, "dur": 8, "pad": 1.5, "cd": 0.5, "hex": 1}
num_bad = [f"{k} {U[k]} (want {v})" for k, v in NUM.items() if U[k] != v]
if U["hurl"] not in (0, 700):
    num_bad.append(f"hurl {U['hurl']} (want 0 at stage 2, 700 after)")
n["x0"] = len(num_bad)
bad["0"] = num_bad
checks = [
    (0, "the numbers: charge 14 (16 converted), dur 8, pad 1.5, cd 0.5, hex 1, hurl 0 (stage 2) or 700",
        all(k in U for k in NUM)),
    (1, "the window is `dur` on the window clock (never ticks frozen), closes on the caster's death; only Lodestone carries it",
        n.get("clockOk", 0) > 0 and n.get("casterDeathCloses", 0) > 0 and n.get("frames", 0) > 0),
    (2, "a touch only with the foe's centre within inset + R + pad of a side of the CURRENT hall, alive, unpinned",
        n.get("wallOk", 0) > 0 and n.get("insetTouches", 0) > 0),
    (3, "once per `cd` on the window clock; never a missed clear touch", n.get("cadenceOk", 0) > 0 and n.get("wallCdFrames", 0) > 0),
    (4, "each touch: apply('hex', hex) on the foe once, by side letter; nothing on any other frame",
        n.get("hexOk", 0) > 0 if U["hex"] else n.get("touches", 0) > 0),
    (5, "the hurl: the foe's velocity ASSIGNED hurl x unit(caster - foe), 700 +-1; untouched otherwise (and at hurl 0)",
        n.get("hurlOk", 0) > 0 if U["hurl"] else n.get("touches", 0) > 0),
    (6, "no damage, no resolveHit, no beat, no hit stop; nothing else on the foe (its whole state but vx, vy, status.hex) or the Match",
        n.get("nothingElseOk", 0) > 0 and n.get("wholeFoeOk", 0) > 0 and n.get("wholeMatchOk", 0) > 0),
    (7, "the caster's own touches do nothing: the tick never changes the caster (its whole state but ultRunes, runeTally)",
        n.get("casterOk", 0) > 0 and n.get("casterWallFrames", 0) > 0),
    (8, "every blow the hammer's own, rebuilt exactly, in the window and out", n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
    (9, "no cast while the walls are lit; no cast held back", n.get("castOk", 0) > 0 and n.get("chargeOk", 0) > 0),
]
if R.get("stage6v"):
    ns = {k: n[k] for k in sorted(n, key=lambda k: (len(k), k)) if k.startswith("touchN")}
    print(f"  stage 6 voice: casts {n.get('castVoice',0)}  touch snaps + hex-snaps {n.get('touchVoice',0)} (n "
          f"{', '.join(f'{k[6:]}:{v}' for k, v in ns.items())})  close voices {n.get('closeVoice',0)} (clock closes, "
          f"both alive)  silent death closes {n.get('deathCloseSilent',0)}  windows lit at the verdict "
          f"{n.get('litAtVerdict',0)} (silent)   run totals {R['lodeAll']}")
    checks.append((10, "stage 6 voice: one cast voice a cast; a touch = its snap at the foe's count after its hex, then the "
                       "hex-snap, in order; a close voice only on a clock close with both alive, none on a death or at the "
                       "verdict; nothing else in tickRunes; every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "touchVoice", "closeVoice", "deathCloseSilent",
                                                 "litAtVerdict", "touchN1", "touchN5"))))
if R.get("stage6p"):
    print(f"  stage 6 picture: tickLode calls clean {n.get('lodeOk',0)}  walls lit {n.get('wallsLit',0)}, going dark "
          f"{n.get('wallsGoingDark',0)}  touch records at the touch {n.get('recOk',0)} ({n.get('recCorner',0)} at a corner, "
          f"{n.get('recInset',0)} in a closed-in hall)  the foe's count tagged {n.get('tagOk',0)} ({n.get('tagUnderCap',0)} "
          f"under the cap)  kill-step touches undrawn {n.get('killTouchUndrawn',0)}  dark in the verdict "
          f"{n.get('darkAtVerdict',0)}  drawn frames {n.get('drawOk',0)} ({n.get('drawPic',0)} with the picture up, "
          f"{n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawVerdict',0)} in the verdict)"
          + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((11, "stage 6 picture: tickLode writes no sim field and draws no RNG; the walls lit exactly while the window "
                       "is; one record a touch at its spot and walls; the foe's count tagged; a kill-step touch undrawn; dark "
                       "in the verdict; no drawn frame throws, draws the RNG or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("lodeOk", "wallsLit", "wallsGoingDark", "recOk", "recInset", "tagOk",
                                                 "tagUnderCap", "darkAtVerdict"))
                   and (n.get("drawPic", 0) > 0 and n.get("drawPicStop", 0) > 0 and n.get("drawVerdict", 0) > 0
                        if R.get("drawOn") else True)))
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
