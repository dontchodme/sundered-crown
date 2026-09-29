#!/usr/bin/env python
"""ASCENSION'S PROBE -- one check per sentence of v74 §1 / §5 and the brief's §0-§1,
read INSIDE the hooks.

    python angelus_probe.py --game <link>  [--seeds 6] [--seed0 104001] [--json out.json]

Wraps `tickRise`, `tickWeapon`, `resolveHit`, `tickStatus`, `fireUlt` and `step`
on the Match prototype (and each fighter's `apply`) and reads each event where it
happens. Runs Angelus against every other relic, both sides, and prints N/N. The
checks follow the link's own numbers, so the same probe gates stages 2-5
(healPer 0 / 1).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "rises and hangs in the air": a cast whose record is not {t 0, x0/y0 the
      caster's position, lit 0, hits the ledger}; a rise frame whose position is
      not x0 + (hang - x0) x smoothstep(t / rise); a lit frame that does not
      end at (W/2, max(hangY, inset + R + 6)); or the caster off the hang point
      by more than 1 unit at the end of more than 1% of lit steps
  [2] "pinned there, re-armed; immovable, takes hits, takes no knock": a cast
      that does not pin (pin dur, pinFree 1, pinV [0,0]); a window frame that
      does not end with pin = pinMax = dur and pinFree 1; the hung caster moved
      between two frames by anything (counted); no foe blow ever landing on the
      risen caster (the design's point: it is reachable).
      THE RE-ARM IS EXERCISED, NOT ASSUMED (review r2, finding 1). Nothing on
      this roster clears the hold inside a window -- "pinFree found cleared"
      counts it and reads 0 -- so a build that forgot to re-arm `pinFree` (or
      `pinMax`) would pass on natural fights alone. Every FORCE-th window frame
      (--force, default 50) the probe clears the three fields the re-arm owns
      (pin, pinMax, pinFree) JUST BEFORE the tick: `tickStasis` has already
      run this step and nothing reads them between here and the tick, so on a
      correct build the tick restores them and no fight changes (the win and
      every count equal a --force 0 run); a build that does not re-arm one of
      them ends that frame un-held and fails [2]. Coverage requires >= 1
      forced frame re-armed.
  [3] "released to rest on close": a live caster left with velocity, pin, pinMax,
      pinV or pinFree; a dead one whose kill flight the close touched
  [4] "reachMul 10 on both blades ... reaching the floor": reachMul not `shaft`
      on every lit frame, or not 1 during the rise and after the close; a blade
      segment whose tip is not R + reach x mods.reach x reachMul from the centre
      (both blades, lit or not)
  [5] "spin x 0.5": a turn that is not w.spin x (shaftSpin lit, 1 otherwise) x
      spinMul x dt x spinDir, rebuilt exactly (none while stunned)
  [6] "a shaft through the enemy is a light hit": a blow whose damage is not the
      blade x (winDmg lit, 1 otherwise) x dmgMul x jitter x dmgTaken, rounded,
      crit included -- rebuilt from the captured crit and jitter draws; and any
      shaft hit at full damage, named
  [7] "every hit heals the one above": a tick whose blessing is not exactly
      healPer x (the hits delta since the last tick, while lit), once, with the
      side letter; a blessing with no shaft hit, during the rise, or at healPer
      0; the shaft tally not the delta; and a blessing-only tickStatus whose heal
      is not min(maxHp, hp + hps x stacks x dt)
  [8] "nothing else": the rise's tick hurting, filing a beat, moving the hit
      stop, touching the foe or applying anything to it; the cast filing any
      beat but its one `ult`
  [9] a window that is not `dur` long on the window clock, or that outlives the
      caster: its clock moving through a frozen step (hit stop, latch, split
      hold) or by anything but dt through a live one, or the arrival later than
      the first tick at or after `rise`; any relic but Angelus carrying `ultRise`.
      NOT on the foe's death (the builder's reading 10): a tick that finds the
      foe dead and the caster alive must leave the window open ("closed early"
      otherwise); such ticks are counted, and so are the windows still open
      when the match ends (the sim never closes them -- `step()` returns at
      `over` before any ticker; stage 6's picture closes them)
  [10] a cast while the rise is open (the design has no wait; none may be needed)

COUNTS FOR THE READINGS (not checks): shaft hits on Twinshade's shades (they
heal, reading 11); windows open at the match's end, by winner, lit and reason;
ticks with the foe dead and the caster alive.

STAGE 6 (the picture and the voice, the builder's readings 12-18), each check
run only where the link carries it -- the voices detected by the tap's arm in
`AC.SFX.play.toString()`, the picture by `tickAscend` on the Match -- so the
same probe still gates stages 2-5 at 10/10, every line as before. Once a fight
is over the probe runs 2 s more of the verdict (the step's `over` path: only
the presentation clock runs) for these two checks alone; [1]-[10] read none of
those steps.
  [11] THE VOICES fire exactly on their events and nowhere else (v74 §6.2).
      Read through `AC.SFX.play` (a no-op headless: the call is recorded before
      its first line returns); only Angelus's four `ult` arms are read, so a
      ward's shatter -- which plays its own crit HIT voice inside hurt() -- is
      not one of them. Evidence: Angelus's cast playing anything but exactly
      one cast voice (w "angelus"), or another relic's cast playing one; a
      tickRise tick playing anything but one tap (w "angelus-shaft") when it
      heals a shaft hit (its n the caster's blessing stacks after the heal)
      and one close chord (w "angelus-close") when the window closes BY ITS
      CLOCK with both alive -- none on a death close, none when the foe is
      dead; a landing thud (w "angelus-land") anywhere but `move`, or other
      than exactly on the caster's first floor contact after such a close (a
      bounce that plays the wall tick, at the floor, the caster alive) -- every
      chord accounted for: a thud, a fight that ended before the ball landed, or
      a ball the next cast hung again in mid-air (it never landed); any of
      the four in a step anywhere else, in the picture's hook or in the
      verdict.
  [12] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickAscend`
      (tickPresentation, the picture's one call on the step path) is wrapped:
      evidence is any change across it to either fighter (every own number,
      flag and string but its `ascend*` fields, every status, the window, the
      tally, the pin's rest, the blade cooldowns, the shared weapon row and its
      ult) or to the match (every own number, flag and string, every array's
      length but `tags`), or an RNG draw. And the picture as declared
      (readings 12-13): not up (`ascendFade` 1) in an open window (`ultRise`,
      the match live, the caster alive); up with no window; a close that is
      not a fade to 0 over exactly 0.6 of its clock (0.3 s) -- by the clock,
      on the caster's death, or AT THE KILL, where the sim leaves the window
      open (reading 10); a heal (`riseTally.bless` rising, the caster alive,
      the match live) without the halo's flare and a BLESSING tag with the
      caster's count on the caster, or a flare after a death or the verdict;
      a thread with no shaft blow seen while lit, or more threads than blows;
      a fighter that never cast carrying any of it; and the picture still up
      after 2 s of the verdict.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=104001)
ap.add_argument("--json", default=None)
ap.add_argument("--foes", default="", help="comma list (default: every other relic)")
ap.add_argument("--sides", default="AB", help="AB, A or B (A = Angelus as side A, the lab's)")
ap.add_argument("--seed-step", type=int, default=13, help="11 = ult_overlay's seeds, for a run on the lab's fights")
ap.add_argument("--force", type=int, default=50, help="clear pin/pinMax/pinFree before every Nth window tick ([2]); 0 = never")
a = ap.parse_args()

JS = r"""([seeds, foeList, sides, FORCE]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR, AW = C.arena.w;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, BL = AC.STATUS.blessing;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const isMe = f => !!(f && f.w && f.w.id === "angelus");
  const oTick = P.tickRise, oWeap = P.tickWeapon, oResolve = P.resolveHit, oFire = P.fireUlt,
        oStep = P.step, oStatus = P.tickStatus;
  let per = null, inRise = false, wf = 0;   // wf: Angelus's window ticks seen, for the forced clears
  const applyLog = [];
  const last = new WeakMap();     // Z -> {x, y} at the end of its previous lit frame

  /* STAGE 6, DETECTED BY ITS OWN PRESENCE: the tap's arm in the synth [11],
     `tickAscend` on the match [12]. A link without them runs [1]-[10] only. */
  const S6V = /angelus-shaft/.test(AC.SFX.play.toString()), S6P = typeof P.tickAscend === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oMove = P.move, oAscend = P.tickAscend;
  const OURS = { "angelus": "cast", "angelus-shaft": "tap", "angelus-close": "close", "angelus-land": "land" };
  const WHERE = { cast: "cast", tap: "rise", close: "rise", land: "move" };
  let vctx = "a step", tail = false, vOurs = 0, vWall = 0;
  const vlog = [], pend = new WeakMap();     // pend: a clock close's chord played, its landing not yet
  if (S6V) AC.SFX.play = function(kind, q){
    if (kind === "ult" && q && OURS[q.w]){
      const ty = OURS[q.w];
      vOurs++;
      if (vctx !== WHERE[ty]) fail(11, `the ${ty} voice (${q.w}) played in ${vctx}`);
      vlog.push([ty, q.n]);
    } else if (kind === "wall" && vctx === "move") vWall++;
    return oPlay.call(this, kind, q);
  };
  /* [12] the simulation's state, as one array in a fixed key order: both
     fighters' own numbers, flags and strings (their `ascend*` fields aside)
     and array lengths, statuses, the window, the tally, the pin's rest, the
     cooldowns, the weapon row and its ult; the match's own numbers, flags and
     strings and every array's length (`tags` aside: the BLESSING tag is the
     picture's to file) */
  const same = (x, y) => x === y || (x !== x && y !== y);
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 97 && k.startsWith("ascend")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      for (const k in f.status){ const s = f.status[k]; o.push(k, s.stacks, s.t, s.src); }
      const Z = f.ultRise;
      if (Z) o.push(Z.t, Z.dur, Z.x0, Z.y0, Z.lit, Z.hits); else o.push("-");
      const T = f.riseTally;
      if (T) for (const k of Object.keys(T)) o.push(k, T[k]); else o.push("-");
      if (f.pinV) o.push(f.pinV[0], f.pinV[1]);
      if (f.hitCd) o.push(...f.hitCd);
      for (const k of Object.keys(f.w)){ const v = f.w[k]; if (v === null || typeof v !== "object") o.push(k, v); }
      if (f.w.ult) for (const k of Object.keys(f.w.ult)){ const v = f.w.ult[k]; if (v === null || typeof v !== "object") o.push(k, v); }
    }
    for (const k of Object.keys(m)){
      if (k === "tags") continue;
      const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    return o;
  };
  const aseen = new WeakMap();    // f -> the picture's inputs as last seen: {hits, bless, closeDt}

  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [11]-[12] alone */
    if (tail) return oStep.call(this, dt);
    vctx = "a step"; vlog.length = 0;
    const frozen = this.hitStop > 0 || !!this.latch || !!this.splitHold, over0 = this.over;
    for (const f of [this.a, this.b]) if (f.ultRise){ if (frozen) inc("winFrozen"); else inc("winLive"); }
    /* [9] THE WINDOW CLOCK: a window open at the top of a step does not advance
       through a frozen step (hit stop, latch, split hold) and advances by
       exactly dt through a live one -- the window tickers' clock. */
    const open = [];
    for (const f of [this.a, this.b]) if (isMe(f) && f.ultRise && !over0) open.push([f, f.ultRise, f.ultRise.t]);
    const r = oStep.call(this, dt);
    for (const [f, Z, t0] of open){
      if (frozen){
        if (f.ultRise !== Z || Z.t !== t0) fail(9, `the window clock ran through a frozen step: t ${t0} -> ${Z.t}${f.ultRise !== Z ? " (closed)" : ""}`);
        else inc("clockHeldOk");
      } else if (f.ultRise === Z){
        if (Z.t !== t0 + dt) fail(9, `a live step advanced the window by ${Z.t - t0}, not dt`);
        else inc("clockLiveOk");
      }
    }
    for (const f of [this.a, this.b]){
      if (!isMe(f) || !f.ultRise) continue;
      const foe = f === this.a ? this.b : this.a;
      if (per){ per.winSteps++; per.foeStk += foe.stacks("smite"); }
      if (f.ultRise.lit && !this.over){
        const ty = Math.max(f.w.ult.hangY, this.inset + R + 6);
        inc("litSteps");
        if (Math.abs(f.y - ty) <= 1 && Math.abs(f.x - AW / 2) <= 1) inc("heldOk"); else inc("heldOff");
      }
    }
    return r;
  };

  P.fireUlt = function(f, foe){
    const me = isMe(f);
    if (me){ if (f.ultRise) fail(10, "cast while the rise is open"); else inc("castOk"); }
    const b0 = this.beats.length, x = f.x, y = f.y, h = f.hits;
    const vc0 = vctx, v0 = vlog.length;
    vctx = me ? "cast" : "a foe's cast";
    let r;
    try { r = oFire.call(this, f, foe); } finally { vctx = vc0; }
    if (S6V){
      /* [11] Angelus's cast plays exactly one cast voice; another relic's cast none of ours */
      const got = vlog.slice(v0);
      if (me){ if (got.length !== 1 || got[0][0] !== "cast") fail(11, `the cast played ${JSON.stringify(got)}`); else inc("castVoiceOk"); }
      else if (got.length) fail(11, `a foe's cast played ${JSON.stringify(got)}`);
      /* a clock close whose ball is still in the air at the next cast never lands: the cast hangs it
         again, and the thud waits for the landing after a later clock close */
      if (me && pend.get(f)){ inc("landRecast"); pend.set(f, false); }
    }
    if (me){
      const Z = f.ultRise, u = f.w.ult, nb = this.beats.length - b0;
      const ub = this.beats.slice(b0).filter(b => b.kind === "ult");
      if (!Z || Z.t !== 0 || Z.x0 !== x || Z.y0 !== y || Z.lit !== 0 || Z.hits !== h || Z.dur !== u.dur) fail(1, `the cast's record ${JSON.stringify(Z)}`);
      else inc("castRecOk");
      if (f.pin !== u.dur || f.pinMax !== u.dur || f.pinFree !== 1 || !f.pinV || f.pinV[0] !== 0 || f.pinV[1] !== 0) fail(2, `the cast's hold pin ${f.pin} pinFree ${f.pinFree} pinV ${JSON.stringify(f.pinV)}`);
      else inc("castPinOk");
      if (nb !== 1 || ub.length !== 1) fail(8, `the cast filed ${nb} beat(s), ${ub.length} of them ult`); else inc("castBeatOk");
    }
    return r;
  };

  P.tickWeapon = function(f, foe, dt){
    if (!isMe(f)) return oWeap.call(this, f, foe, dt);
    const Z = f.ultRise, lit = !!(Z && Z.lit), th0 = f.theta, stun = f.stun, dir = f.spinDir;
    const k = lit ? f.w.ult.shaftSpin : 1;
    const spin = f.w.spin * k * f.spinMul(this.actMods.spin) * 1;
    const r = oWeap.call(this, f, foe, dt);
    const want = stun > 0 ? th0 : th0 + spin * dt * dir;
    if (f.theta !== want) fail(5, `theta ${th0} -> ${f.theta}, want ${want} (lit ${lit}, stun ${stun})`);
    else inc(lit ? "spinLitOk" : "spinOk");
    /* [4] THE SHAFTS' GEOMETRY: both blades, from the centre, R + reach */
    const segs = this.bladeSegments(f), reach = f.w.reach * this.actMods.reach * f.reachMul;
    if (segs.length !== f.w.blades.length) fail(4, `${segs.length} segments`);
    else {
      let ok = true;
      for (const s of segs) if (Math.abs(Math.hypot(s.bx - f.x, s.by - f.y) - (R + reach)) > 1e-6) ok = false;
      if (!ok) fail(4, `a blade tip off R + reach (reachMul ${f.reachMul})`);
      else inc(lit ? "geomLitOk" : "geomOk");
      if (lit) inc("tipLen", R + reach);
    }
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    if (!isMe(self) || mul !== undefined){
      if (isMe(foe) && foe.ultRise){
        const h0 = self.hits, lit = foe.ultRise.lit;
        const r = oResolve.call(this, self, foe, hx, hy, seg, mul, over);
        if (self.hits > h0) inc(lit ? "takenLit" : "takenRise");
        return r;
      }
      return oResolve.call(this, self, foe, hx, hy, seg, mul, over);
    }
    const Z = self.ultRise, lit = !!(Z && Z.lit), u = self.w.ult;
    const d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(),
                  aegis: !!(foe.w && foe.w.id === "bulwarden"), curse: foe.stacks("curse") };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg, mul, over); }
    finally { this.rng = oRng; }
    if (self.hits - h0 !== 1) return r;
    if (Z){ inc("blowsIn"); if (per) per.in++; } else { inc("blowsOut"); if (per) per.out++; }
    if (lit) inc("shaftSeen"); else if (Z) inc("riseBlows");
    if (lit && foe.shade) inc("shadeLit");     // reading 11: a shaft hit on a shade heals too
    const D = self.dealt - d0, crit = self.crits > c0;
    const jit = 1 + (draws[1] - 0.5) * jitK;
    const raw = (lit ? self.w.dmg * u.winDmg : self.w.dmg) * 1 * pre.dm * jit * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){
      if (pre.aegis || pre.curse) inc("blowExempt");
      else {
        const full = Math.round((crit ? critMul : 1) * self.w.dmg * pre.dm * jit * pre.dt);
        fail(6, `${lit ? "a SHAFT" : Z ? "a rise" : "an ordinary"} blow: dealt ${D}, want ${want}${lit && Math.abs(D - full) < 1e-6 ? " -- FULL DAMAGE" : ""}`);
      }
    } else inc(lit ? "dmgLitOk" : "dmgOk");
    return r;
  };

  P.tickStatus = function(f, dt){
    if (!isMe(f) || !f.status.blessing) return oStatus.call(this, f, dt);
    const st = f.status.blessing, s = st.stacks, t0 = st.t, hp0 = f.hp, only = Object.keys(f.status).length === 1;
    const r = oStatus.call(this, f, dt);
    const lives = t0 - dt > 0;
    const heal = lives ? Math.min(BL.hps * s * dt, Math.max(0, f.maxHp - hp0)) : 0;
    inc("healHp", heal);
    if (only && f.alive){
      const want = lives ? Math.min(f.maxHp, hp0 + BL.hps * s * dt) : hp0;
      if (f.hp !== Math.min(want, f.maxHp)) fail(7, `blessing-only tickStatus: hp ${hp0} -> ${f.hp}, want ${want} (${s} stacks)`);
      else inc("statusHealOk");
    }
    return r;
  };

  P.tickRise = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultRise && !isMe(f)) fail(9, `${f.w.id} carries ultRise`);
      const Z = f.ultRise;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t0: Z.t, t1: Z.t + dt, lit: Z.lit, x: f.x, y: f.y, vx: f.vx, vy: f.vy, alive: f.alive,
                 pinFree: f.pinFree, hits: f.hits, zh: Z.hits, inset: this.inset,
                 fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy, fhp: foe.hp, fsh: foe.shield,
                 shaft0: f.riseTally.shaftHits, bless0: f.riseTally.bless, forced: false });
      if (isMe(f) && f.alive && !foe.alive && !this.over) inc("foeDeadTicks");
    }
    /* [2] THE RE-ARM, EXERCISED: every FORCE-th window tick, clear the three
       fields the re-arm owns just before the tick. `pre` has already recorded
       the natural pinFree (the "found cleared" count stays the engine's). */
    if (FORCE > 0) for (const p of pre){
      if (!isMe(p.f)) continue;
      if (++wf % FORCE === 0){ p.forced = true; p.f.pin = 0; p.f.pinMax = 0; p.f.pinFree = 0; inc("forcedClears"); }
    }
    const hurts = [], beats = [], oHurt = this.hurt, oBeat = this.beat, a0 = applyLog.length;
    const hs0 = this.hitStop, shk0 = this.shake;
    this.hurt = function(t, d, s){ hurts.push([t, d, s]); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    inRise = true;
    const vc0 = vctx, v0 = vlog.length;
    vctx = "rise";
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; inRise = false; vctx = vc0; }
    if (S6V){
      /* [11] THE TICK'S VOICES: one tap for a tick that heals a shaft hit (n =
         the caster's blessing stacks after it), one close chord for a close BY
         THE CLOCK with both alive; nothing else */
      const got = vlog.slice(v0), taps = got.filter(x => x[0] === "tap"), chords = got.filter(x => x[0] === "close");
      let wantTap = 0, wantChord = 0, nWant = null, death = false;
      for (const p of pre){
        if (!isMe(p.f)) continue;
        const nh = p.hits - p.zh;
        if (nh > 0 && p.lit && p.f.w.ult.healPer > 0 && p.alive){
          wantTap++; nWant = p.f.stacks("blessing");
          if (nh > 1) inc("tapMulti");
        }
        if (p.t1 >= p.Z.dur || !p.alive){
          if (p.t1 >= p.Z.dur && p.alive && p.foe.alive){ wantChord++; pend.set(p.f, true); }
          else if (!p.alive){ death = true; inc("chordQuietDeath"); }
          else inc("chordQuietFoeDead");
        }
      }
      if (taps.length !== wantTap) fail(11, `the tick played ${taps.length} tap(s) for ${wantTap} heal(s)`);
      else if (wantTap){
        if (taps[0][1] !== nWant) fail(11, `a tap at n ${taps[0][1]}, the caster's blessing ${nWant}`);
        else { inc("tapOk"); inc("tapN" + nWant); }
      }
      if (chords.length !== wantChord) fail(11, wantChord ? "no close chord on a clock close with both alive"
                                               : `a close chord ${death ? "on the caster's death" : "with no clock close (both alive)"}`);
      else if (wantChord) inc("chordOk");
    }
    const applies = applyLog.slice(a0);
    if (hurts.length) fail(8, `the rise's tick hurt ${hurts.length}x`);
    if (beats.length) fail(8, `the rise's tick filed ${beats.length} beat(s)`);
    if (this.hitStop !== hs0) fail(8, `the rise's tick moved the hit stop ${hs0} -> ${this.hitStop}`);
    if (this.shake !== shk0) fail(8, "the rise's tick shook the hall");
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult, T = f.riseTally, side = f === this.a ? "a" : "b";
      /* [7] THE HEAL -- the hits delta at the top of the tick, whatever the frame */
      const nh = p.hits - p.zh;
      const mine = applies.filter(x => x[0] === f), onFoe = applies.filter(x => x[0] === foe);
      if (onFoe.length) fail(8, `applied ${JSON.stringify(onFoe.map(x => [x[1], x[2]]))} to the foe`);
      if (Z.hits !== p.hits) fail(7, `the ledger ${Z.hits}, the caster's hits ${p.hits}`);
      if (nh > 0 && p.lit){
        if (T.shaftHits - p.shaft0 !== nh) fail(7, `shaft tally +${T.shaftHits - p.shaft0} for ${nh} hits`);
        if (u.healPer > 0 && p.alive){
          if (mine.length !== 1 || mine[0][1] !== "blessing" || mine[0][2] !== u.healPer * nh) fail(7, `applies ${JSON.stringify(mine.map(x => [x[1], x[2]]))} for ${nh} shaft hit(s)`);
          else if (mine[0][3] !== side) fail(7, `source ${typeof mine[0][3] === "object" ? "a Fighter" : JSON.stringify(mine[0][3])}`);
          else { inc("healOk"); inc("blessN", u.healPer * nh); if (nh > 1) inc("healMulti"); }
          if (T.bless - p.bless0 !== u.healPer * nh) fail(7, "the bless tally");
        } else if (mine.length) fail(7, `a blessing at healPer ${u.healPer} (alive ${p.alive})`);
        else inc("noHealOk");
      } else {
        if (mine.length) fail(7, `a blessing with ${nh} hit(s), lit ${p.lit}`);
        if (nh > 0) inc("riseHitsSeen", nh);
      }
      if (p.t1 >= Z.dur || !p.alive){
        /* THE CLOSE */
        if (f.ultRise){ fail(9, "the window did not close at dur / on the caster's death"); continue; }
        if (p.alive && p.t1 < Z.dur - 1e-9) fail(9, "closed early");
        inc("closes");
        if (f.reachMul !== 1) fail(4, `reachMul ${f.reachMul} after the close`);
        if (p.alive){
          inc("clockCloses");
          if (f.vx !== 0 || f.vy !== 0 || f.pin !== 0 || f.pinMax !== 0 || f.pinV !== null || f.pinFree !== 0)
            fail(3, `released with v ${f.vx},${f.vy} pin ${f.pin}/${f.pinMax} pinV ${JSON.stringify(f.pinV)} pinFree ${f.pinFree}`);
          else inc("restOk");
        } else {
          if (f.vx !== p.vx || f.vy !== p.vy) fail(3, "the close touched a dead caster's kill flight");
          else inc("deadCloseOk");
        }
        continue;
      }
      /* A WINDOW FRAME */
      inc("frames");
      if (!f.ultRise){ fail(9, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      if (f.pin !== Z.dur || f.pinMax !== Z.dur || f.pinFree !== 1) fail(2, `a window frame ended with pin ${f.pin}/${f.pinMax} pinFree ${f.pinFree}${p.forced ? " (the probe cleared the hold before this tick)" : ""}`);
      else { inc("holdOk"); if (p.forced) inc("forcedRearmOk"); }
      if (p.pinFree !== 1) inc("pinFreeCleared");
      const tx = AW / 2, ty = Math.max(u.hangY, p.inset + R + 6);
      if (ty !== u.hangY) inc("clampBound");
      if (!p.lit && p.t1 < u.rise){
        const k = p.t1 / u.rise, e = k * k * (3 - 2 * k);
        const wx = Z.x0 + (tx - Z.x0) * e, wy = Z.y0 + (ty - Z.y0) * e;
        if (f.x !== wx || f.y !== wy) fail(1, `rise at ${p.t1.toFixed(4)}: (${f.x}, ${f.y}), want (${wx}, ${wy})`);
        else inc("easeOk");
        if (f.reachMul !== 1 || Z.lit) fail(4, "lit during the rise"); else inc("riseDarkOk");
        continue;
      }
      if (!p.lit){
        /* the first tick at or after `rise` ON THE WINDOW CLOCK; a window clock
           that ran elsewhere shows up here as a late arrival, so it is [9]'s */
        if (!(p.t0 < u.rise)) fail(9, `arrived late: t ${p.t0} -> ${p.t1}`);
        else inc("arrivals");
        if (T.arrivals < 1) fail(1, "no arrival tallied");
      } else {
        const L = last.get(Z);
        if (L){ inc("hungPairs"); if (p.x !== L.x || p.y !== L.y) inc("hungMoved"); }
      }
      if (!Z.lit || f.reachMul !== u.shaft) fail(4, `a lit frame with reachMul ${f.reachMul}, lit ${Z.lit}`); else inc("litOk");
      if (f.x !== tx || f.y !== ty) fail(1, `hung at (${f.x}, ${f.y}), want (${tx}, ${ty})`); else inc("hangOk");
      last.set(Z, { x: f.x, y: f.y });
      /* [8] NOTHING ELSE: the foe untouched by the tick */
      if (foe.x !== p.fx || foe.y !== p.fy || foe.vx !== p.fvx || foe.vy !== p.fvy || foe.hp !== p.fhp || foe.shield !== p.fsh)
        fail(8, "the rise's tick moved or hurt the foe");
    }
    return r;
  };

  /* [11] THE LANDING: `move` is the one place the thud may play, exactly on
     the caster's first floor contact after a clock close's chord -- a bounce
     (it plays the wall tick) that leaves it on the floor, the caster alive */
  if (S6V) P.move = function(f, foe, dt){
    const me = isMe(f) && !f.shade, vc0 = vctx, v0 = vlog.length, w0 = vWall;
    vctx = me ? "move" : "a foe's move";
    let r;
    try { r = oMove.call(this, f, foe, dt); } finally { vctx = vc0; }
    if (!me) return r;
    const lands = vlog.slice(v0).filter(x => x[0] === "land").length;
    const hiY = C.arena.h - this.inset - R;
    const want = pend.get(f) && vWall > w0 && f.alive && f.y >= hiY ? 1 : 0;
    if (lands !== want) fail(11, want ? "no landing thud on the first floor contact after a clock close"
                                      : `a landing thud ${pend.get(f) ? "off the floor" : "with no clock close before it"}`);
    else if (want){ inc("landOk"); pend.set(f, false); }
    return r;
  };

  /* [12] THE PICTURE'S HOOK: `tickAscend`, on the presentation clock inside the step */
  if (S6P) P.tickAscend = function(dt){
    inc("ascendCalls");
    const F = [this.a, this.b], pre = F.map(f => ({ fade: f.ascendFade }));
    const s0 = simSnap(this);
    let draws = 0; const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    const vc0 = vctx; vctx = "the picture (tickAscend)";
    let r;
    try { r = oAscend.call(this, dt); } finally { this.rng = oRng; vctx = vc0; }
    const s1 = simSnap(this);
    let clean = s0.length === s1.length;
    if (!clean) fail(12, `the picture changed the simulation's shape: ${s0.length} -> ${s1.length} fields`);
    else for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i])){
      clean = false;
      fail(12, `the picture wrote the simulation: ${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}${this.over ? " (after over)" : ""}`);
      break;
    }
    if (draws){ clean = false; fail(12, `the picture drew the RNG ${draws} times`); }
    if (clean) inc("ascendClean");
    for (let i = 0; i < 2; i++){
      const f = F[i], p = pre[i], T = f.riseTally;
      if (!T){
        if (f.ascendFade !== 0 || f.ascendFx.length) fail(12, `${f.w.id}, which never cast, carries the picture`);
        continue;
      }
      let S = aseen.get(f);
      if (!S){ S = { hits: 0, bless: 0, closeDt: -1 }; aseen.set(f, S); }
      const open = !!f.ultRise && !this.over && f.alive;
      const nh = f.hits - S.hits, nb = T.bless - S.bless;
      S.hits = f.hits; S.bless = T.bless;
      /* the window's picture: up while open; the close a fade to 0 over exactly
         0.6 of this clock (0.3 s) -- by the clock, on a death, or at the kill */
      if (open){
        if (f.ascendFade !== 1) fail(12, `the picture is not up (${f.ascendFade}) in an open window`);
        else inc("upOk");
        S.closeDt = -1;
      } else if (p.fade > 0){
        if (S.closeDt < 0){
          S.closeDt = 0;
          inc(this.over ? (f.ultRise ? "picCloseKillOpen" : "picCloseOver") : !f.alive ? "picCloseDeath" : "picCloseClock");
        }
        S.closeDt += dt;
        if (f.ascendFade === 0){
          if (S.closeDt < 0.6 - 1e-9) fail(12, `the picture gone ${S.closeDt.toFixed(4)} into its close (0.6 of this clock is 0.3 s)`);
          else inc("picClosedOk");
        } else if (S.closeDt > 0.6 + 1e-9) fail(12, `the picture still up ${S.closeDt.toFixed(4)} into its close (fade ${f.ascendFade})`);
        else if (!(f.ascendFade < p.fade)) fail(12, `the close is not a fade: ${p.fade} -> ${f.ascendFade} at ${S.closeDt.toFixed(4)}`);
      } else if (f.ascendFade !== 0) fail(12, `the picture came up (${f.ascendFade}) with no window open`);
      /* a heal: the halo's flare and BLESSING n on the caster */
      if (nb > 0){
        if (f.alive && !this.over){
          const k = f.stacks("blessing");
          if (f.ascendHeal !== 0) fail(12, "a heal landed without the halo's flare");
          else if (!this.tags.some(g => g.key === "blessing" && g.val === k && Math.hypot(g.x - f.x, g.y - f.y) < R * 3))
            fail(12, `a heal landed with no BLESSING ${k} on the caster`);
          else inc("flareOk");
        } else if (f.ascendHeal === 0) fail(12, "a flare after the caster's death or the verdict");
      }
      /* a shaft blow: its thread, only for a blow seen while lit, never more than the blows */
      const nt = f.ascendFx.filter(x => x.t === 0).length, lit = open && !!f.ultRise.lit;
      if (nt > 0 && !(lit && nh > 0)) fail(12, `${nt} thread(s) with no shaft blow seen while lit`);
      else if (nt > nh) fail(12, `${nt} threads for ${nh} blow(s)`);
      if (lit && nh > 0){ inc("litBlowsSeen", nh); inc("threads", nt); }
    }
    return r;
  };

  const foes = foeList.length ? foeList : AC.WEAPONS.map(w => w.id).filter(i => i !== "angelus");
  const T = { casts: 0, frames: 0, litFrames: 0, arrivals: 0, shaftHits: 0, bless: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, foeStkF = 0, blessOther = 0;
  for (const side of sides) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "angelus", sd) : new AC.Match("angelus", fid, sd);
    const me = side ? m.b : m.a;
    for (const q of [m.a, m.b]){
      const o = q.apply;
      q.apply = function(k, nn, src){
        applyLog.push([q, k, nn, src]);
        if (q === me && k === "blessing" && !inRise) blessOther += nn;
        return o.call(this, k, nn, src);
      };
    }
    per = { in: 0, out: 0, winSteps: 0, foeStk: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; applyLog.length = 0; }
    /* READING 10: a window open when the match ends stays open (step() returns
       at `over` before any ticker); stage 6's picture has to close it. */
    if (m.over && me.ultRise){
      inc("openAtEnd"); inc(m.winner === me ? "openWin" : "openLoss");
      if (me.ultRise.lit) inc("openLit");
      if (m.reason !== "slain") inc("openNotSlain");
    }
    if (S6V && pend.get(me)){ inc("landUnlanded"); pend.set(me, false); }   // the fight ended before the ball landed
    /* [11]-[12] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
    if ((S6V || S6P) && m.over){
      const o0 = vOurs, open = !!me.ultRise;
      tail = true; vctx = "the verdict (a step after over)";
      try { for (let i = 0; i < 2 / DT; i++) m.step(DT); } finally { tail = false; vctx = "a step"; }
      if (S6V && vOurs === o0) inc(open ? "verdictQuietOpen" : "verdictQuiet");
      if (S6P){
        if (me.ascendFade !== 0 || me.ascendFx.length)
          fail(12, `the picture still up after 2 s of the verdict (fade ${me.ascendFade}, ${me.ascendFx.length} threads)${open ? " -- the window the sim left open" : ""}`);
        else inc(open ? "endClosedOpen" : "endClosedOk");
      }
    }
    fights++; bin += per.in; bout += per.out;
    foeStkF += per.winSteps ? per.foeStk / per.winSteps : 0;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.riseTally) for (const k in T) T[k] += me.riseTally[k];
  }
  P.tickRise = oTick; P.tickWeapon = oWeap; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep; P.tickStatus = oStatus;
  if (S6V){ P.move = oMove; if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  if (S6P) P.tickAscend = oAscend;
  const u = AC.WEAPONS.find(w => w.id === "angelus");
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           foeStk: foeStkF / fights, blessOther, s6v: S6V, s6p: S6P,
           u: { dmg: u.dmg, charge: u.ult.charge, dur: u.ult.dur, rise: u.ult.rise, hangY: u.ult.hangY, shaft: u.ult.shaft,
                shaftSpin: u.ult.shaftSpin, winDmg: u.ult.winDmg, healPer: u.ult.healPer } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRise === 'function'"):
        raise SystemExit("no tickRise in this build -- not an Ascension link (stage 2+)")
    seeds = [a.seed0 + a.seed_step * i for i in range(a.seeds)]
    sides = [{"A": 0, "B": 1}[c] for c in a.sides]
    R = page.evaluate(JS, [seeds, [f for f in a.foes.split(",") if f], sides, a.force])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frames = max(1, n.get("frames", 0))
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
held = n.get("heldOk", 0) / max(1, n.get("litSteps", 0))
print(f"\nASCENSION PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Angelus sides {a.sides} x {len(a.foes.split(',')) if a.foes else 'every'} foe(s) x {a.seeds} seeds from {a.seed0} step {a.seed_step})   relic {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Angelus win {R['win']:.1%}")
print(f"  per cast: shaft hits {T['shaftHits']/casts:.2f}  blessing {T['bless']/casts:.2f}  healed {n.get('healHp',0)/casts:.1f} hp "
      f"(tickStatus)  blows in the rise {n.get('riseBlows',0)/casts:.2f}  foe blows taken lit {n.get('takenLit',0)/casts:.2f} "
      f"/ rising {n.get('takenRise',0)/casts:.2f}")
print(f"  foe smite stacks on an average window frame (per fight, the lab's f_foeStk) {R['foeStk']:.2f}   "
      f"blessing from elsewhere {R['blessOther']}   ward/curse-exempt blows {n.get('blowExempt',0)}")
print(f"  hold: at the hang point on {100*held:.2f}% of lit steps ({n.get('heldOff',0)} off of {n.get('litSteps',0)})   "
      f"hung ball moved between frames {n.get('hungMoved',0)} of {n.get('hungPairs',0)}   pinFree found cleared "
      f"{n.get('pinFreeCleared',0)}   clamp bound {n.get('clampBound',0)}   shaft tip {n.get('tipLen',0)/max(1,n.get('geomLitOk',0)):.1f} units")
print(f"  closes {n.get('closes',0)} (clock {n.get('clockCloses',0)}, dead caster {n.get('deadCloseOk',0)})   "
      f"multi-hit heals {n.get('healMulti',0)}   window clock: held {n.get('clockHeldOk',0)} frozen steps, +dt {n.get('clockLiveOk',0)} live   FREEZE CENSUS {100*frozen:.1f}% of window steps frozen "
      f"({n.get('winFrozen',0)} of {n.get('winFrozen',0)+n.get('winLive',0)})")
print(f"  [2] re-arm exercised: the probe cleared pin/pinMax/pinFree before {n.get('forcedClears',0)} window ticks "
      f"(every {a.force}th), re-armed {n.get('forcedRearmOk',0)} (the rest were closes)")
print(f"  reading 10: windows still open at the match's end {n.get('openAtEnd',0)} of {R['fights']} fights "
      f"(Angelus won {n.get('openWin',0)}, lost {n.get('openLoss',0)}; lit {n.get('openLit',0)}; not slain {n.get('openNotSlain',0)})   "
      f"ticks with the foe dead and the caster alive {n.get('foeDeadTicks',0)}   reading 11: shaft hits on shades {n.get('shadeLit',0)}")
heal_on = U["healPer"] > 0
checks = [
    (1, "the rise: the cast's record, the smoothstep ease on the window clock, the arrival at `rise`, the hang point held (>= 99% of lit steps within 1)",
        n.get("castRecOk", 0) > 0 and n.get("easeOk", 0) > 0 and n.get("arrivals", 0) > 0 and n.get("hangOk", 0) > 0 and held >= 0.99),
    (2, "the hold: pin dur / pinFree 1 / pinV [0,0] at the cast, re-armed every frame (exercised: the probe's cleared frames re-arm); the hung ball never moved; foe blows land on it",
        n.get("castPinOk", 0) > 0 and n.get("holdOk", 0) > 0 and n.get("hungMoved", 0) == 0 and n.get("takenLit", 0) > 0
        and (a.force == 0 or n.get("forcedRearmOk", 0) > 0)),
    (3, "released on close: a live caster to rest; a dead one's kill flight untouched", n.get("restOk", 0) > 0),
    (4, "the shafts: reachMul `shaft` on every lit frame, 1 in the rise and after; both blade tips at R + reach x reachMul",
        n.get("litOk", 0) > 0 and n.get("riseDarkOk", 0) > 0 and n.get("geomLitOk", 0) > 0 and n.get("geomOk", 0) > 0),
    (5, "the turn: w.spin x (shaftSpin lit) x spinMul x dt, rebuilt exactly", n.get("spinLitOk", 0) > 0 and n.get("spinOk", 0) > 0),
    (6, "every blow: the blade x (winDmg lit), crit and jitter rebuilt exactly; no shaft hit at full damage",
        n.get("dmgLitOk", 0) > 0 and n.get("dmgOk", 0) > 0),
    (7, "the heal: blessing healPer x each lit hit, once, by side letter, and tickStatus heals it; nothing else" if heal_on
        else "the heal: none at healPer 0",
        (n.get("healOk", 0) > 0 and n.get("statusHealOk", 0) > 0) if heal_on else n.get("noHealOk", 0) > 0),
    (8, "nothing else: the tick hurts nobody, files no beat, moves no stop, leaves the foe; the cast files its one ult beat",
        n.get("frames", 0) > 0 and n.get("castBeatOk", 0) > 0),
    (9, "the window is `dur` long on the window clock (held through every frozen step, +dt a live one), closes on the caster's death, not the foe's (reading 10); only Angelus carries ultRise",
        n.get("closes", 0) > 0 and n.get("clockHeldOk", 0) > 0 and n.get("clockLiveOk", 0) > 0),
    (10, "no cast while the rise is open (the design has no wait)", n.get("castOk", 0) > 0),
]
g = lambda k: n.get(k, 0)
if R["s6v"]:
    print(f"  stage 6 voices: {g('castVoiceOk')} casts each one cast voice (of {T['casts']}); {g('tapOk')} healing ticks each one tap "
          f"(n 1-5: {'/'.join(str(g('tapN' + str(i))) for i in range(1, 6))}; {g('tapMulti')} tick(s) healing two hits at once, one tap); "
          f"{g('chordOk')} clock closes with both alive each one chord; quiet on {g('chordQuietDeath')} death closes and "
          f"{g('chordQuietFoeDead')} clock closes with the foe dead; {g('landOk')} landings each one thud ({g('landUnlanded')} fights "
          f"ended before the ball landed, {g('landRecast')} balls hung again by the next cast before they landed: "
          f"{g('landOk') + g('landUnlanded') + g('landRecast')} = the {g('chordOk')} chords); silent through 2 s of the verdict: {g('verdictQuietOpen')} fights with the window open, "
          f"{g('verdictQuiet')} with it shut")
    checks.append((11, "stage 6 voices: one cast voice a cast, one tap a healing tick (n = the caster's blessing), one chord a clock "
                       "close with both alive and one thud on its landing; none anywhere else -- not on a death, a foe's cast, "
                       "the picture or the verdict",
                   g("castVoiceOk") == T["casts"] > 0 and g("tapOk") > 0 and g("chordOk") > 0 and g("chordQuietDeath") > 0
                   and g("landOk") > 0 and g("verdictQuietOpen") > 0
                   and g("landOk") + g("landUnlanded") + g("landRecast") == g("chordOk")))
if R["s6p"]:
    print(f"  stage 6 picture: tickAscend {g('ascendCalls')} calls, {g('ascendClean')} writing nothing of the simulation's and "
          f"drawing no RNG; up on {g('upOk')} calls in an open window; closes {g('picCloseClock')} by the clock, "
          f"{g('picCloseDeath')} on the caster's death, {g('picCloseKillOpen')} AT THE KILL with the sim's window open "
          f"(+{g('picCloseOver')} at `over` with it shut), {g('picClosedOk')} gone in 0.6 of its clock (0.3 s); "
          f"{g('flareOk')} heals each flared and tagged; {g('threads')} threads for {g('litBlowsSeen')} shaft blows seen lit; "
          f"after 2 s of the verdict the picture down in {g('endClosedOpen')} fights the sim left open and {g('endClosedOk')} others")
    checks.append((12, "stage 6 picture: tickAscend writes nothing of the simulation's and draws no RNG; up while the window is "
                       "open, a 0.3 s close by the clock, on a death and AT THE KILL (reading 10); a flare and a BLESSING tag a "
                       "heal; threads only for shaft blows; down after the verdict",
                   g("ascendCalls") > 0 and g("ascendClean") == g("ascendCalls") and g("upOk") > 0 and g("picCloseClock") > 0
                   and g("picCloseKillOpen") > 0 and g("picClosedOk") > 0 and g("flareOk") > 0 and g("threads") > 0
                   and g("endClosedOpen") > 0))
if not (R["s6v"] or R["s6p"]):
    print("  stage 6: not on this link (no tap arm in the synth, no tickAscend) -- [11]-[12] not run")
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
