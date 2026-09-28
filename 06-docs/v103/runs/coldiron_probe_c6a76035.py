#!/usr/bin/env python
"""TEMPER'S PROBE -- one check per sentence of v73 §1 / §5 and the brief's §0-§1,
read INSIDE the hooks.

    python coldiron_probe.py --game <a Temper link, stage 2+>

Wraps `step`, `move`, `resolveClank`, `resolveHit`, `fireUlt`, `tickTemper`
and the liquid's `SLOSH.step`, and reads each event where it happens, rebuilding
the engine's arithmetic exactly where it can. Runs Coldiron against every
other relic, both sides, and prints N/N. The checks follow the link's own
numbers, so the same probe gates stages 2-5 (bind 0 / 2, cap 6 / 9).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration": a window that is not `dur` long on the window clock
      (the ticks of a clock-closed window counted), that outlives a death while
      the match still runs (a kill flight), a clock that does not advance by
      exactly dt on a live step, a clock that moves (or a window that opens or
      closes) on a FROZEN step -- a hit stop, the latch, the split: the window
      tickers' clock stops there, the standing ruling -- a cast under an open
      window, or any relic but Coldiron carrying `ultTemper`. (On an ordinary
      kill the window is still set at `over`: `checkEnd` follows `tickTemper`
      in the killing step and nothing ticks after `over`. Counted and printed.)
  [2] "as heavy as a warhammer, so every bind the twinblade takes, it wins --
      the enemy's weapon is thrown back instead of its own": `massMul` not
      exactly ult.mass / w.mass on the window (w.mass x massMul not exactly
      ult.mass at the cast) or not 1 on every fighter (shades included) outside
      it; a clank whose stuns and knocks are not the engine's rule rebuilt
      from w.mass x massMul (mass^1.7 shares, the streak's growth and falloff)
  [3] "each bind it wins sunders the enemy": a bind won decisively by the open
      window (the outcome read off the knock the engine actually gave) without
      exactly one apply("sunder", bind, the winner's side letter) on the loser,
      the loser's stacks not the ceiling rule's, or any apply on any other bind
  [4] "While the iron holds, sunder stacks past its limit": a fighter's
      `sunderCap` not `cap` while the other's window is open and 6 otherwise,
      after every step and every tick; a stack above max(6, cap) ever; a
      fighter rising above 6 outside a window; stacks above 6 trimmed (they
      only run out, to 0, on sunder's own clock)
  [5] the blades are still the blades: a blow of Coldiron's whose damage is not
      the blade x dmgMul x jitter x dmgTaken (sunder included), rounded, crit
      included -- rebuilt from the captured draws, in the window and out
  [6] the declared gravity consequence (design §5): move's gravity, the hit
      stop's gravity or the liquid's not (w.mass x massMul + burden) / massRef
      to the massWeight, exactly, on every fighter
  [7] nothing else: a cast that damages, applies, moves anybody or stops the
      world beyond the engine's generic cast stop; a tickTemper frame that
      moves anybody, draws the RNG, hurts, applies, stops the world or files a
      beat; a clank that files anything but its own one beat and its own stop
  STAGE 6 (the picture and the voice, sc-coldiron-temper-fx). Each check runs
  only on a link that carries its half, read off the page itself:
  [8] THE VOICE (on when "coldiron-anvil" is in AC.SFX.play.toString()): a
      Coldiron cast without exactly one `ult`/coldiron voice inside fireUlt; a
      won bind without exactly one anvil voice inside resolveClank whose `n` is
      the loser's sunder count after the bind's sunder, or an anvil on any
      other clank; a clank without exactly its own one clank voice (nothing
      else sounds there); a clock close with both alive without exactly one
      close voice, a close voice on a death close, or anything else sounding
      inside tickTemper; and every Coldiron voice of the run accounted for by
      those events -- so none plays after `over` (a window still set there
      closes silently: the death voice's)
  [9] THE PICTURE (on when the Match has `tickIron`): `tickIron`, the
      picture's one hook on the step, changing any sim field of either
      fighter, a shade or the match, or drawing the RNG; the iron up (ironFade
      exactly 1) other than exactly while the window is open, the match not
      over and the caster alive; a won bind without exactly one new anvil ring
      at that bind's contact (the resolveClank call's own hx, hy), or, the foe
      alive, without a sunder tag on the board reading the foe's count; a
      sunder tag past 6 not in dwarven's glow, or one at 6 or under in it; a
      window still set at `over` whose blades are not cooled to 0 by 0.5s into
      the verdict; and on the DRAWN subset (the first seed, both sides, every
      foe, through the kill and 0.5s of verdict) a drawn frame that throws,
      draws the match's RNG or changes any sim field
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=103001)
ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, HP = C.physics, DT = HP.dt, CL = C.clank;
  const CAP0 = AC.STATUS.sunder.maxStacks, critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const ID = "coldiron", U = AC.WEAPONS.find(w => w.id === ID).ult, TOP = Math.max(CAP0, U.cap);
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const isC = f => !!(f && f.w && f.w.id === ID);
  const mmWant = f => (f.ultTemper ? f.w.ult.mass / f.w.mass : 1);
  const gTerm = (f, mm) => HP.gravity * Math.pow((f.w.mass * mm + f.burden * f.burdenMass) / HP.massRef, HP.massWeight);
  const side = (m, f) => f === m.a ? "a" : "b";
  const snap = f => ({ x: f.x, y: f.y, vx: f.vx, vy: f.vy, stun: f.stun, hp: f.hp, sh: f.shield });
  /* how many clock ticks a window of `dur` takes, the engine's own accumulation */
  let TICKS = 0; { let t = 0; while (!(t >= U.dur)){ t += DT; TICKS++; } }
  const oStep = P.step, oMove = P.move, oClank = P.resolveClank, oHit = P.resolveHit, oFire = P.fireUlt, oTick = P.tickTemper;
  const hasSlosh = typeof SLOSH !== "undefined" && typeof SLOSH.step === "function";
  const oSlosh = hasSlosh ? SLOSH.step : null;
  let curM = null, per = null, postOver = false;

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /coldiron-anvil/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickIron === "function";
  const voices = [], ciAll = {}, oPlay = AC.SFX.play, oIron = P.tickIron;
  const ciVoice = q => !!(q && typeof q.w === "string" && /^coldiron/.test(q.w));
  if (stage6v) AC.SFX.play = function(kind, q){
    voices.push([kind, q ? Object.assign({}, q) : q]);
    if (kind === "ult" && ciVoice(q)) ciAll[q.w] = (ciAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  const vname = x => x[0] + (x[1] && x[1].w ? "/" + x[1].w : "");
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, statuses,
     window, mass, ceiling and tally, the shades, and the match's clock, stop,
     verdict, streak, holds and beats. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "alive", "pin", "pinMax",
              "pinFree", "reachMul", "clanks", "hits", "dealt", "crits", "spinDir", "burden", "massMul", "sunderCap"];
  const simSnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null, m.clankStreak,
               !!m.latch, !!m.splitHold, m.beats ? m.beats.length : null];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
      o.push(f.ultTemper ? [f.ultTemper.t, f.ultTemper.dur] : null, f.temperTally ? JSON.stringify(f.temperTally) : null);
    }
    for (const q of (m.shades || [])) o.push([q.x, q.y, q.vx, q.vy, q.hp]);
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 30), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 30), i + 30)); };
  const DW = AC.AFFINITIES.dwarven;
  /* a won bind's contact, as resolveClank was handed it (the winner's latest) */
  const wonAt = new Map();
  const cooledSeen = new WeakSet(), tagSeen = new WeakSet(), tagPast = new WeakSet();
  if (stage6p) P.tickIron = function(dt){
    const s0 = simSnap(this), oR = this.rng, oMR = Math.random;
    const pend = [this.a, this.b].map(f => ({ f, won: f.temperTally ? f.temperTally.won : 0, seen: f.ironSeen }));
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oIron.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(9, `tickIron drew the RNG ${drew}x`);
    const s1 = simSnap(this);
    if (s1 !== s0) fail(9, "tickIron changed the sim: " + firstDiff(s0, s1)); else inc("ironOk");
    for (const p of pend){
      const f = p.f, foe = f === this.a ? this.b : this.a;
      /* THE IRON IS UP EXACTLY WHILE THE WINDOW IS (and the match runs, and the caster stands) */
      const live = !!(f.ultTemper && !this.over && f.alive);
      if ((f.ironFade === 1) !== live) fail(9, `ironFade ${f.ironFade} with the window ${live ? "live" : "not live"} (over ${this.over}, alive ${f.alive})`);
      else if (live) inc("ironUp"); else if (f.ironFade > 0) inc("ironCool");
      if (f.ultTemper && this.over && f.ironFade < 1 && !cooledSeen.has(f.ultTemper)){ cooledSeen.add(f.ultTemper); inc("coolAtOver"); }
      /* A WON BIND: one ring at its own contact, and the foe's count on the board */
      if (p.won > p.seen){
        inc("wonSeen", p.won - p.seen);
        const fresh = f.ironRings.filter(q => q.t === 0), at = wonAt.get(f);
        if (f.ironSeen !== p.won) fail(9, `ironSeen ${f.ironSeen}, the tally ${p.won}`);
        else if (fresh.length !== 1) fail(9, `a won bind rang ${fresh.length} new rings`);
        else if (!at || fresh[0].x !== at.x || fresh[0].y !== at.y) fail(9, `the ring at ${fresh[0].x},${fresh[0].y}, the bind at ${at ? at.x + "," + at.y : "?"}`);
        else inc("ringOk");
        if (foe.alive && foe.hp > 0){
          const k = foe.stacks("sunder");
          if (!this.tags.some(g => g.key === "sunder" && g.val === k)) fail(9, `no sunder tag reads the foe's ${k}`);
          else { inc("bindTagOk"); if (k > CAP0) inc("bindTagPast6"); }
        }
      } else if (f.ironRings.some(q => q.t === 0)) fail(9, "a ring with no won bind");
    }
    /* PAST THE CAP IS A COLOUR: every sunder tag on the board */
    for (const g of this.tags){
      if (g.key !== "sunder") continue;
      const past = (g.val || 0) > CAP0, want = past ? DW.glow : DW.core;
      if (g.c !== want){ fail(9, `a sunder tag at ${g.val} in ${g.c}, want ${want}`); continue; }
      /* counted once a tag, and once more the first time it reads past 6 */
      if (!tagSeen.has(g)){ tagSeen.add(g); inc("tagOk"); }
      if (past && !tagPast.has(g)){ tagPast.add(g); inc("tagPastOk"); }
    }
    return r;
  };

  P.step = function(dt){
    const me = isC(this.a) ? this.a : isC(this.b) ? this.b : null;
    if (!me || postOver) return oStep.call(this, dt);
    const other = me === this.a ? this.b : this.a;
    const prevM = curM; curM = this;
    const frozenPath = !this.over && !this.latch && !this.splitHold && this.hitStop > 0;
    const frozen = !this.over && (this.hitStop > 0 || !!this.latch || !!this.splitHold);
    const openBefore = !!me.ultTemper, live = !this.over && !frozen;
    /* [1] THE WINDOW TICKERS' CLOCK: the window and its clock as they stood before the step */
    const z0 = me.ultTemper, zt0 = z0 ? z0.t : null;
    if (openBefore && !this.over){ inc(frozen ? "winFrozen" : "winLive"); per.winSteps++; }
    const pre = [this.a, this.b].map(f => ({ f, vy: f.vy, pin: f.pin, s: f.stacks("sunder"), so: f.status.sunder,
                                             win: !!(f === me ? other : me).ultTemper }));
    let r;
    try { r = oStep.call(this, dt); } finally { curM = prevM; }
    /* [1] THE WINDOW RUNS ON THE WINDOW TICKERS' CLOCK (the standing ruling; v99 §4).
       A FROZEN step (a hit stop, the latch, the split) leaves the window exactly as
       it was: the same object, the clock not moved, nothing opened or closed. A LIVE
       step with the window open moves its clock by exactly dt, closing it or not.
       (The review's r1 -- the window ticking through a hit stop, the lab's clock --
       made 960 ticks a window and passed the tick count alone.) */
    if (frozen){
      if (me.ultTemper !== z0 || (z0 && z0.t !== zt0))
        fail(1, `a frozen step moved the window: ${zt0} -> ${me.ultTemper ? me.ultTemper.t : null}${me.ultTemper !== z0 ? " (opened/closed)" : ""}`);
      else if (z0) inc("winHeldFrozen");
    } else if (live && z0){
      if (z0.t !== zt0 + dt) fail(1, `a live step moved the window's clock ${z0.t - zt0}, want ${dt}`);
      else if (me.ultTemper === z0) inc("winLiveAdv");
      else if (me.ultTemper === null) inc("winLiveClose");
      else fail(1, "a live step replaced an open window");
    }
    /* [6] THE HIT STOP'S GRAVITY -- the only velocity change on the frozen path */
    if (frozenPath) for (const p of pre){
      const f = p.f; if (p.pin > 0) continue;
      const want = p.vy + gTerm(f, mmWant(f)) * dt;
      if (f.vy !== want) fail(6, `hit-stop gravity: vy ${p.vy} -> ${f.vy}, want ${want} (massMul ${f.massMul})`);
      else inc(isC(f) && f.ultTemper ? "frozenGravIn" : "frozenGravOut");
    }
    /* [4] THE CEILING, THE LIFT AND THE CLOCK, after every step */
    for (const p of pre){
      const f = p.f, o = f === this.a ? this.b : this.a, s1 = f.stacks("sunder");
      const capWant = o.ultTemper ? o.w.ult.cap : CAP0;
      if (f.sunderCap !== capWant) fail(4, `sunderCap ${f.sunderCap}, want ${capWant} after a step`);
      if (s1 > TOP) fail(4, `${s1} stacks, above ${TOP}`);
      const inWin = p.win || !!o.ultTemper;
      if (s1 > CAP0){
        if (inWin) inc("over6In");
        else { inc("over6Out"); if (s1 > p.s) fail(4, `rose ${p.s} -> ${s1} outside a window`); else inc("over6Held"); }
      }
      /* a status that ran out and was re-applied in the same step is a new object */
      if (p.s > CAP0 && s1 > 0 && s1 < p.s && f.status.sunder === p.so) fail(4, `trimmed ${p.s} -> ${s1}`);
    }
    /* THE LAB'S COLUMNS, read after the step as the lab read them */
    if (me.ultTemper){
      per.winFrames++; const k = other.stacks("sunder"); per.foeStk += k; per.pk = Math.max(per.pk, k);
    }
    if (openBefore && !me.ultTemper){
      per.peaks.push(per.pk); per.pk = 0;
      per.winLen.push(per.winSteps * dt); per.winSteps = 0;
      if (other.stacks("sunder") > CAP0) per.over6At = this.t;
    }
    /* HOW LONG STACKS ABOVE 6 OUTLIVE A WINDOW: from the close to the frame they
       run out (every sunder application refreshes the 5s clock, the engine's
       rule), censored at the next cast or the match's end */
    if (per.over6At !== null){
      if (other.stacks("sunder") <= CAP0){ per.over6Secs.push(this.t - per.over6At); per.over6At = null; }
      else if (me.ultTemper || this.over){ per.over6Cens.push(this.t - per.over6At); per.over6At = null; }
    }
    return r;
  };

  P.move = function(f, foe, dt){
    if (!curM || !(isC(curM.a) || isC(curM.b))) return oMove.call(this, f, foe, dt);
    const calls = [], oPow = Math.pow, pin = f.pin;
    Math.pow = function(b, e){ if (e === HP.massWeight) calls.push(b); return oPow(b, e); };
    let r;
    try { r = oMove.call(this, f, foe, dt); } finally { Math.pow = oPow; }
    if (pin > 0){ if (calls.length) fail(6, "a held ball felt gravity"); return r; }
    const want = (f.w.mass * mmWant(f) + f.burden * f.burdenMass) / HP.massRef;
    if (calls.length !== 1 || calls[0] !== want) fail(6, `move's gravity base ${JSON.stringify(calls)}, want ${want}`);
    else { inc(isC(f) && f.ultTemper ? "moveGravIn" : "moveGravOut");
           if (isC(f)) { if (f.ultTemper) { per.gIn += oPow(want, HP.massWeight); per.gInN++; } else { per.gOut += oPow(want, HP.massWeight); per.gOutN++; } } }
    return r;
  };

  if (hasSlosh) SLOSH.step = function(f, dt, g){
    if (curM && (isC(curM.a) || isC(curM.b)) && (f === curM.a || f === curM.b)){
      const want = gTerm(f, mmWant(f));
      if (g !== want) fail(6, `the liquid's gravity ${g}, want ${want}`);
      else inc(isC(f) && f.ultTemper ? "sloshIn" : "sloshOut");
    }
    return oSlosh.call(this, f, dt, g);
  };

  P.resolveClank = function(A, B, hx, hy){
    const me = isC(A) ? A : isC(B) ? B : null;
    if (!me) return oClank.call(this, A, B, hx, hy);
    const pA = snap(A), pB = snap(B), hs0 = this.hitStop, open = !!me.ultTemper, v0 = voices.length;
    if (A.massMul !== mmWant(A) || B.massMul !== mmWant(B)) fail(2, `massMul ${A.massMul} / ${B.massMul} at a clank, want ${mmWant(A)} / ${mmWant(B)}`);
    const applies = [], beats = [], oBeat = this.beat;
    const wrap = f => { const o = f.apply; f.apply = function(k, nn, src){ applies.push({ f, k, nn, src, s0: f.stacks(k), cap: f.sunderCap }); return o.call(this, k, nn, src); }; };
    wrap(A); wrap(B);
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    let r;
    try { r = oClank.call(this, A, B, hx, hy); }
    finally { delete A.apply; delete B.apply; delete this.beat; }
    /* [2] THE ENGINE'S RULE, REBUILT FROM w.mass x massMul */
    const st = this.clankStreak, knockMul = 1 + CL.knockGrowth * st, stunMul = 1 / (1 + CL.stunFalloff * st);
    const mA = A.w.mass * mmWant(A), mB = B.w.mass * mmWant(B);
    const wA = Math.pow(mA, 1.7), wB = Math.pow(mB, 1.7), tot = wA + wB, shareA = wB / tot, shareB = wA / tot;
    const dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy) || 1, nx = dx / d, ny = dy / d;
    const want = { avx: pA.vx - nx * CL.knock * shareA * 2 * knockMul, avy: pA.vy - ny * CL.knock * shareA * 2 * knockMul,
                   bvx: pB.vx + nx * CL.knock * shareB * 2 * knockMul, bvy: pB.vy + ny * CL.knock * shareB * 2 * knockMul,
                   ast: Math.max(pA.stun, CL.stun * shareA * 2 * stunMul), bst: Math.max(pB.stun, CL.stun * shareB * 2 * stunMul) };
    if (A.vx !== want.avx || A.vy !== want.avy || B.vx !== want.bvx || B.vy !== want.bvy || A.stun !== want.ast || B.stun !== want.bst)
      fail(2, `${open ? "IN" : "out of"} the window, ${A.w.id} (${mA}) v ${B.w.id} (${mB}): knock/stun not the mass rule`);
    else inc(open ? "clankIn" : "clankOut");
    /* [3] THE OUTCOME THE ENGINE ACTUALLY GAVE, read off A's knock */
    const kx = nx * CL.knock * 2 * knockMul, ky = ny * CL.knock * 2 * knockMul;
    const shA = Math.abs(kx) >= Math.abs(ky) ? (pA.vx - A.vx) / kx : (pA.vy - A.vy) / ky;
    const decO = Math.abs(1 - 2 * shA) > 0.16, W = shA < 0.5 ? A : B, L = W === A ? B : A;
    const iron = decO && !!W.ultTemper, meWon = decO && W === me;
    if (open){ per.binds++; if (meWon) per.won++; else if (!decO) per.dead++; else per.lost++;
               if (!decO && L.w.shape !== "warhammer" && W.w.shape !== "warhammer") inc("deadNonHammer"); }
    else { per.bindsOut++; if (meWon) per.wonOut++; }
    if (iron && U.bind > 0){
      const mine = applies.filter(x => x.f === L);
      if (applies.length !== 1 || mine.length !== 1 || mine[0].k !== "sunder" || mine[0].nn !== W.w.ult.bind)
        fail(3, `a won bind applied ${JSON.stringify(applies.map(x => [x.f.w.id, x.k, x.nn]))}, want [[${L.w.id}, sunder, ${W.w.ult.bind}]]`);
      else if (mine[0].src !== side(this, W)) fail(3, `source ${typeof mine[0].src === "object" ? "a Fighter" : JSON.stringify(mine[0].src)}`);
      else {
        const x = mine[0], s1 = L.stacks("sunder"), sw = x.s0 < x.cap ? Math.min(x.cap, x.s0 + x.nn) : x.s0;
        if (s1 !== sw) fail(3, `the loser's stacks ${x.s0} -> ${s1}, want ${sw} (ceiling ${x.cap})`);
        else { inc("bindSunderOk"); per.applied += x.nn; if (sw > CAP0) inc("bindPast6"); }
      }
    } else if (applies.length) fail(3, `an apply on a bind the iron did not win: ${JSON.stringify(applies.map(x => [x.f.w.id, x.k, x.nn]))}`);
    else inc(open ? "noSunderOk" : "noSunderOut");
    if (iron) wonAt.set(W, { x: hx, y: hy });
    /* [8] THE CLANK'S VOICE, AND THE ANVIL OVER IT ON A BIND THE IRON WINS */
    if (stage6v){
      const tv = voices.slice(v0), an = tv.filter(x => x[0] === "ult" && x[1] && x[1].w === "coldiron-anvil");
      const cl = tv.filter(x => x[0] === "clank");
      if (cl.length !== 1 || tv.length !== cl.length + an.length) fail(8, `a clank played ${JSON.stringify(tv.map(vname))}`);
      else if (iron && U.bind > 0){
        if (an.length !== 1) fail(8, `a won bind struck the anvil ${an.length}x`);
        else if (an[0][1].n !== L.stacks("sunder")) fail(8, `an anvil at n ${an[0][1].n}, the loser carries ${L.stacks("sunder")}`);
        else { inc("anvilVoice"); inc("anvilN" + an[0][1].n); }
      } else if (an.length) fail(8, "an anvil on a bind the iron did not win");
      else inc("clankVoiceOk");
    }
    /* [7] THE CLANK'S OWN BEAT AND ITS OWN STOP, NOTHING MORE */
    if (beats.length !== 1 || beats[0].kind !== "clank") fail(7, `a clank filed ${JSON.stringify(beats.map(b => b.kind))}`);
    else if (this.hitStop !== Math.max(hs0, CL.stop)) fail(7, `a clank's stop ${hs0} -> ${this.hitStop}`);
    else inc("clankBeatOk");
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isC(self) || mul !== undefined) return oHit.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultTemper, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: foe.w && foe.w.id === "bulwarden",
                  curse: foe.stacks("curse"), stk: foe.stacks("sunder") };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oHit.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (open) per.in++; else per.out++;
    const D = self.dealt - d0, crit = self.crits > c0;
    const raw = self.w.dmg * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(5, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want} (${pre.stk} sunder)`); }
    else { inc(open ? "blowInOk" : "blowOutOk"); if (pre.stk > CAP0) inc("blowPast6"); }
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isC(f)) return oFire.call(this, f, foe);
    if (f.ultTemper) fail(1, "a cast under an open window"); else inc("castOk");
    const pf = snap(foe), pm = snap(f), hs0 = this.hitStop, fst = JSON.stringify(foe.status), mst = JSON.stringify(f.status);
    const v0 = voices.length;
    const r = oFire.call(this, f, foe);
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ciVoice(x[1]));
      if (cv.length !== 1 || cv[0][1].w !== "coldiron") fail(8, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
      else inc("castVoice");
    }
    const Z = f.ultTemper;
    if (!Z || Z.t !== 0 || Z.dur !== f.w.ult.dur) fail(1, `the cast opened ${JSON.stringify(Z)}`);
    if (f.massMul !== f.w.ult.mass / f.w.mass || f.w.mass * f.massMul !== f.w.ult.mass) fail(2, `massMul ${f.massMul} at the cast (w.mass x massMul ${f.w.mass * f.massMul})`);
    else inc("castMassOk");
    const same = (p, g) => p.x === g.x && p.y === g.y && p.vx === g.vx && p.vy === g.vy && p.hp === g.hp && p.sh === g.sh && p.stun === g.stun;
    if (!same(pf, snap(foe)) || !same(pm, snap(f)) || JSON.stringify(foe.status) !== fst || JSON.stringify(f.status) !== mst)
      fail(7, "the cast moved, hurt or applied");
    else if (this.hitStop !== Math.max(hs0, 0.08)) fail(7, `the cast's stop ${hs0} -> ${this.hitStop}`);
    else inc("castNothingOk");
    return r;
  };

  P.tickTemper = function(dt){
    const pre = [], both = [this.a, this.b], sn = both.map(snap), hs0 = this.hitStop;
    for (const f of both){
      if (f.ultTemper && !isC(f)) fail(1, `${f.w.id} carries ultTemper`);
      if (f.massMul !== mmWant(f)) fail(2, `massMul ${f.massMul} on ${f.w.id} (window ${!!f.ultTemper})`);
      else inc(f.ultTemper ? "mmIn" : "mmOut");
      const Z = f.ultTemper;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t0: Z.t, t1: Z.t + dt, fAlive: f.alive, foeAlive: foe.alive });
    }
    let draws = 0; const oRng = this.rng, hurts = [], beats = [], applies = [];
    this.rng = () => { draws++; return oRng(); };
    const oHurt = this.hurt, oBeat = this.beat;
    this.hurt = function(t, d, s){ hurts.push(d); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    for (const f of both){ const o = f.apply; f.apply = function(k, nn, src){ applies.push(k); return o.call(this, k, nn, src); }; }
    const v0 = voices.length;
    let r;
    try { r = oTick.call(this, dt); }
    finally { this.rng = oRng; delete this.hurt; delete this.beat; for (const f of both) delete f.apply; }
    /* [8] THE CLOSE: one voice a clock close with both alive, none on a death, nothing else here */
    if (stage6v){
      const tv = voices.slice(v0), cc = tv.filter(x => x[0] === "ult" && x[1] && x[1].w === "coldiron-close").length;
      const clockN = pre.filter(p => p.fAlive && p.foeAlive && p.t1 >= p.Z.dur).length;
      const deathN = pre.filter(p => !(p.fAlive && p.foeAlive)).length;
      if (tv.length !== cc) fail(8, `tickTemper played ${JSON.stringify(tv.map(vname))}`);
      else if (cc !== clockN) fail(8, `${cc} close voice(s) on a tick with ${clockN} clock close(s) and ${deathN} death close(s)`);
      else { if (clockN) inc("closeVoice", clockN); if (deathN) inc("deathSilent", deathN); }
    }
    /* [7] NOTHING ELSE */
    const moved = both.some((f, i) => f.x !== sn[i].x || f.y !== sn[i].y || f.vx !== sn[i].vx || f.vy !== sn[i].vy || f.hp !== sn[i].hp || f.shield !== sn[i].sh || f.stun !== sn[i].stun);
    if (moved || draws || hurts.length || beats.length || applies.length || this.hitStop !== hs0)
      fail(7, `tickTemper: moved ${moved}, rng ${draws}, hurts ${hurts.length}, beats ${beats.length}, applies ${applies.length}, stop ${hs0} -> ${this.hitStop}`);
    else if (pre.length) inc("tickNothingOk");
    /* [1] THE WINDOW ON THE WINDOW CLOCK */
    for (const p of pre){
      const { f, Z } = p;
      if (!p.fAlive || !p.foeAlive || p.t1 >= Z.dur){
        if (f.ultTemper){ fail(1, "the window did not close"); continue; }
        if (f.massMul !== 1) fail(2, "massMul not 1 after the close");
        inc("closes");
        if (p.fAlive && p.foeAlive){
          const ticks = per.ticks.get(Z) + 1;
          if (ticks !== TICKS) fail(1, `a clock close after ${ticks} ticks, want ${TICKS}`); else inc("clockCloseOk");
        } else inc("deathCloseOk");
        continue;
      }
      if (!f.ultTemper){ fail(1, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      if (Z.t !== p.t1) fail(1, `the clock moved ${Z.t - p.t0}, want ${dt}`);
      per.ticks.set(Z, (per.ticks.get(Z) || 0) + 1);
      inc("winTicks");
    }
    /* [4] THE CEILING, BOTH FIGHTERS, EVERY TICK */
    for (const f of both){
      const o = f === this.a ? this.b : this.a, want = o.ultTemper ? o.w.ult.cap : CAP0;
      if (f.sunderCap !== want) fail(4, `sunderCap ${f.sunderCap} on ${f.w.id}, want ${want}`);
      else inc(o.ultTemper ? "capUpOk" : "capDownOk");
    }
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ID);
  const T = { casts: 0, frames: 0, won: 0, applied: 0 };
  const S = { binds: 0, won: 0, dead: 0, lost: 0, bindsOut: 0, wonOut: 0, applied: 0, winFrames: 0, foeStk: 0,
              in: 0, out: 0, gIn: 0, gInN: 0, gOut: 0, gOutN: 0, winSteps: 0, fFoeStk: 0 };
  const peaks = [], winLen = [], over6Secs = [], over6Cens = [];
  let fights = 0, wins = 0, decided = 0;
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), through the kill and 0.5s of the
     verdict, with the sim read before and after each frame and the match's
     RNG watched. The post chain is off: this asks what a draw WRITES, not
     what it looks like (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.ironFade > 0 || q.ironRings.length || q.ironSparks.length || q.stacks("sunder") > CAP0);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    try { AC.__draw(m); } catch (e){ fail(9, "a drawn frame threw: " + String((e && e.message) || e)); }
    finally { m.rng = oR; }
    const s1 = simSnap(m);
    if (dr) fail(9, `a drawn frame drew the match's RNG ${dr}x`);
    else if (s1 !== s0) fail(9, "a drawn frame changed the sim: " + firstDiff(s0, s1));
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };
  for (const sd0 of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = sd0 ? new AC.Match(fid, ID, sd) : new AC.Match(ID, fid, sd);
    const me = sd0 ? m.b : m.a;
    per = { binds: 0, won: 0, dead: 0, lost: 0, bindsOut: 0, wonOut: 0, applied: 0, winFrames: 0, foeStk: 0, pk: 0,
            peaks: [], in: 0, out: 0, gIn: 0, gInN: 0, gOut: 0, gOutN: 0, winSteps: 0, winLen: [], over6At: null, over6Secs: [], over6Cens: [],
            ticks: new Map() };
    let steps = 0;
    voices.length = 0; wonAt.clear();
    const drawn = drawOn && sd === seeds[0];
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++;
    /* A WINDOW STILL SET WHEN THE MATCH ENDS: the killing step runs tickTemper
       before checkEnd, and nothing ticks after `over` (only a kill flight leaves
       live frames after a death, where the death close runs). Counted, not failed:
       no fight can change after `over`; stage 6's picture has to know. */
    if (me.ultTemper){ if (m.over) inc("openAtOver"); else inc("openAtLimit"); }
    /* THE VERDICT (stage 6): 0.5s past `over`, the step hook passing straight
       through. A window still set at `over` cools its blades to 0 in it. */
    if (stage6p && m.over){
      const setAtOver = !!me.ultTemper;
      postOver = true;
      try { for (let k = 0; k < 60; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
      finally { postOver = false; }
      if (setAtOver){ if (me.ironFade !== 0) fail(9, `a window set at \`over\` still shows iron ${me.ironFade} 0.5s into the verdict`); else inc("verdictCoolOk"); }
    }
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.temperTally) for (const k in T) T[k] += me.temperTally[k];
    for (const k in S) if (k in per) S[k] += per[k];
    S.fFoeStk += per.winFrames ? per.foeStk / per.winFrames : 0;
    if (per.over6At !== null) per.over6Cens.push(m.t - per.over6At);
    peaks.push(...per.peaks); winLen.push(...per.winLen); over6Secs.push(...per.over6Secs); over6Cens.push(...per.over6Cens);
  }
  P.step = oStep; P.move = oMove; P.resolveClank = oClank; P.resolveHit = oHit; P.fireUlt = oFire; P.tickTemper = oTick;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY COLDIRON VOICE OF THE RUN, ACCOUNTED FOR by its event. */
    const want = { "coldiron": n.castVoice || 0, "coldiron-anvil": n.anvilVoice || 0, "coldiron-close": n.closeVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(ciAll)]))
      if ((ciAll[k] || 0) !== (want[k] || 0)) fail(8, `${ciAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickIron = oIron;
  if (hasSlosh) SLOSH.step = oSlosh;
  const mean = xs => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0;
  return { n, bad, T, S, fights, win: wins / decided, TICKS, hasSlosh, stage6v, stage6p, drawOn, ciAll,
           peak: mean(peaks), winLen: mean(winLen), over6Secs: mean(over6Secs), over6N: over6Secs.length,
           over6Cens: mean(over6Cens), over6CensN: over6Cens.length,
           u: { charge: U.charge, dur: U.dur, mass: U.mass, bind: U.bind, cap: U.cap },
           gCfg: HP.gravity };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickTemper === 'function'"):
        raise SystemExit("no tickTemper in this build -- not a Temper link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])
    assert not errors, errors

n, bad, T, S, U = R["n"], R["bad"], R["T"], R["S"], R["u"]
F = R["fights"]
casts = T["casts"] or 1
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
gIn = S["gIn"] / max(1, S["gInN"]); gOut = S["gOut"] / max(1, S["gOutN"])
print(f"\nTEMPER PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {F} fights "
      f"(Coldiron both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  casts/fight {T['casts']/F:.2f}   blows a fight: in windows {S['in']/F:.2f}, outside {S['out']/F:.2f}   "
      f"Coldiron win {R['win']:.1%}")
print(f"  per cast: binds {S['binds']/casts:.2f}  won {S['won']/casts:.2f}  deadlocked {S['dead']/casts:.2f}  "
      f"lost {S['lost']/casts:.2f}   sunder from binds {S['applied']/casts:.2f}   foe stack peak {R['peak']:.2f}")
print(f"  foe stacks on a window frame {S['foeStk']/max(1,S['winFrames']):.2f} (the lab's per-fight mean f_foeStk "
      f"{S['fFoeStk']/F:.2f})   the control, outside windows: {S['bindsOut']/F:.2f} binds a fight, "
      f"{S['wonOut']} won")
print(f"  gravity x{gIn:.3f} of the config's in the window, x{gOut:.3f} outside (x{gIn/max(gOut,1e-9):.2f}); "
      f"design: (5/2.68)^0.5 = {(5/2.68)**0.5:.3f}")
print(f"  a window: {R['TICKS']} ticks on the window clock, {R['winLen']:.2f}s of match time (mean, clock and death "
      f"closes)   FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  the window clock: held on {n.get('winHeldFrozen',0)} frozen steps, dt on {n.get('winLiveAdv',0) + n.get('winLiveClose',0)} "
      f"live ones   {T['casts']} casts: {n.get('clockCloseOk',0)} closed on the clock, {n.get('deathCloseOk',0)} on a death "
      f"(a kill flight), {n.get('openAtOver',0)} still set at `over` (an ordinary kill), {n.get('openAtLimit',0)} at the 160s limit")
print(f"  above 6: {n.get('over6In',0)} fighter-steps in a window, {n.get('over6Out',0)} outside (held, never rising); "
      f"{R['over6N'] + R['over6CensN']} closes left the foe above 6: {R['over6N']} ran out after {R['over6Secs']:.2f}s on average, "
      f"{R['over6CensN']} still above 6 at the next cast or the end ({R['over6Cens']:.2f}s)   "
      f"blows at >6 stacks {n.get('blowPast6',0)}   deadlocks against a non-hammer {n.get('deadNonHammer',0)}   "
      f"liquid hooked {R['hasSlosh']}")
on_bind = bool(U["bind"])
checks = [
    (1, "the window is `dur` on the window clock (held through every freeze, dt a live step), closes on a death while the match runs; only Coldiron carries ultTemper; no cast under a window",
        n.get("clockCloseOk", 0) > 0 and n.get("castOk", 0) > 0 and n.get("winTicks", 0) > 0
        and n.get("winHeldFrozen", 0) > 0 and n.get("winLiveAdv", 0) > 0),
    (2, "massMul = mass / w.mass on the window and 1 everywhere else; every clank the mass rule from w.mass x massMul",
        n.get("castMassOk", 0) > 0 and n.get("clankIn", 0) > 0 and n.get("clankOut", 0) > 0 and n.get("mmIn", 0) > 0),
    (3, "a bind the iron wins: apply(sunder, bind, side letter) on the loser, the ceiling's rule; nothing on any other bind",
        (n.get("bindSunderOk", 0) > 0) if on_bind else n.get("noSunderOk", 0) > 0),
    (4, "sunderCap = cap on the foe of an open window, 6 otherwise; never above the cap; above 6 only by the clock, never trimmed",
        n.get("capUpOk", 0) > 0 and n.get("capDownOk", 0) > 0 and (n.get("over6In", 0) > 0 if U["cap"] > 6 else True)),
    (5, "every blow the twinblade's own, rebuilt exactly, in the window and out (sunder included)",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
    (6, "gravity from w.mass x massMul: move, the hit stop and the liquid, exactly, on every fighter",
        n.get("moveGravIn", 0) > 0 and n.get("frozenGravIn", 0) > 0 and (n.get("sloshIn", 0) > 0 or not R["hasSlosh"])),
    (7, "nothing else: the cast resolves nothing; tickTemper moves, draws, hurts, applies, stops and files nothing; a clank its own beat",
        n.get("castNothingOk", 0) > 0 and n.get("tickNothingOk", 0) > 0 and n.get("clankBeatOk", 0) > 0),
]
if R.get("stage6v"):
    ns = {k: n[k] for k in sorted(n, key=lambda k: (len(k), k)) if k.startswith("anvilN")}
    print(f"  stage 6 voice: casts {n.get('castVoice',0)}  anvils {n.get('anvilVoice',0)} on won binds (n "
          f"{', '.join(f'{k[6:]}:{v}' for k, v in ns.items())})  plain clanks {n.get('clankVoiceOk',0)}  "
          f"closes {n.get('closeVoice',0)} on {n.get('clockCloseOk',0)} clock closes  silent: {n.get('deathSilent',0)} death "
          f"closes, {n.get('openAtOver',0)} windows set at `over`   run totals {R['ciAll']}")
    checks.append((8, "stage 6 voice: one cast voice a cast; one anvil a won bind at the loser's count, none on another clank, "
                      "the clank's own voice always; one close a clock close, none on a death; nothing else sounds; every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "anvilVoice", "clankVoiceOk", "closeVoice", "deathSilent"))))
if R.get("stage6p"):
    print(f"  stage 6 picture: tickIron calls clean {n.get('ironOk',0)}  iron up {n.get('ironUp',0)}, cooling {n.get('ironCool',0)}  "
          f"won binds seen {n.get('wonSeen',0)}: rings at the contact {n.get('ringOk',0)}, the foe's count on a tag "
          f"{n.get('bindTagOk',0)} ({n.get('bindTagPast6',0)} past 6)  sunder tags coloured right {n.get('tagOk',0)} "
          f"({n.get('tagPastOk',0)} past 6)  windows cooled at the verdict {n.get('coolAtOver',0)} (to 0 by 0.5s: "
          f"{n.get('verdictCoolOk',0)})  drawn frames {n.get('drawOk',0)} ({n.get('drawPic',0)} with the picture up, "
          f"{n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawVerdict',0)} in the verdict)"
          + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((9, "stage 6 picture: tickIron writes no sim field and draws no RNG; the iron up exactly while the window is; "
                      "one ring a won bind at its contact and the foe's count tagged; past 6 in the glow; cooled at the verdict; "
                      "no drawn frame throws, draws the RNG or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("ironOk", "ironUp", "ironCool", "ringOk", "bindTagOk", "tagPastOk",
                                                 "coolAtOver", "verdictCoolOk"))
                   and (n.get("drawPic", 0) > 0 and n.get("drawVerdict", 0) > 0 if R.get("drawOn") else True)))
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
