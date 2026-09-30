#!/usr/bin/env python
"""UNMAKING'S PROBE (Spellbreaker, redesigned, v79) -- one check per sentence of
v79 §1 / §4 and the brief's §5, read INSIDE the hooks.

    python spellbreaker_probe.py --game <sc-spellbreaker-stun.html | -unmaking | -b<X> | -b7.5-fx> [--stage 2|3|5] [--drawn N]

Wraps `tickUnmake`, `fireUlt`, `tickStatus` (and, inside it, `breakSpin`),
`tickWeapon`, `resolveHit` and `step` on the Match prototype and reads each
event where it happens. Runs Spellbreaker against every other relic, both
sides, and prints N/N. `--sides A --seedstep 11 --foes <33> --seeds 20 --seed0
2207` plays the lab's own fights.

THE STAGE IS PINNED, NOT READ OFF THE LINK (v111's review): what the probe
EXPECTS comes from `--stage` and the builder's numbers, never from the link's
own ult block, so a link that has lost a design number fails. Stage 2 (the
brief's stage 1) expects no second hex; stages 3 and 5 expect the design's
`hexExtra` 1 and every blow in a window on a live body to apply exactly TWO hex.
With no `--stage`, the probe infers it from the BLADE -- a blade that is not the
shipped 8.81 is stage 5 -- and, at the shipped blade only, from `hexExtra`
(0: stage 2, else 3), and says so; the carried link (the final, at its stage-5
blade) therefore needs no flag.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration": a window whose clock does not advance by exactly dt a
      call, that closes before `dur` on the window clock or outlives it or
      either death; `tickUnmake` not asked exactly once on every unfrozen step,
      or asked on a frozen one; any relic but Spellbreaker carrying `ultUnmake`;
      a `dur` that is not the design's 8
  [2] "every stun a hex lands on the enemy's weapon lasts twice as long": a
      hex proc (tickStatus's `breakSpin(f, "the hex takes the wind out of
      it", len)`) whose length is not exactly STATUS.hex.stunFor x the
      fighter's own `hexStunMul`, or whose weapon stun is not max(the stun
      before, len); no proc at x2 on the foe inside a window, or none at x1
      outside. AND THE CADENCE IS THE ENGINE'S (only the LENGTH moves): in
      every tickStatus call the hex clock goes from c0 to c0 + dt x stacks,
      and a proc happens exactly when that reaches stunEvery (1.15), when the
      clock goes to 0 -- rebuilt call by call. The REALISED stun (the proc
      until the weapon's stun reaches 0, counted in tickStatus calls, i.e. on
      the window clock) is the brief's gate: 0.40 +- 0.01 inside windows and
      0.20 outside, over at least 200 clean runs each
  [3] "the build reads it through the FOE's f.hexStunMul (1 default; 2 while
      the caster's window is open -- recomputed each frame, Bloodletting's
      rule) so a runic foe's hexes on Spellbreaker are untouched" (§4): after
      every tickUnmake call, a fighter's field not exactly the OTHER
      fighter's `stunMul` while the other's window is open and 1 otherwise
      (Spellbreaker's own field therefore 1 always); a shade's field not 1; a
      fresh Match not at 1; the field moving anywhere but in tickUnmake; a
      `stunMul` that is not the design's 2
  [4] "every hit Spellbreaker lands hexes twice": a blow of Spellbreaker's
      whose statuses on the body it struck are not exactly the channel's
      apply("hex", 1) and then, while the window is open and the blow left the
      body alive (the lab's guard), apply("hex", the STAGE's hexExtra, side
      letter) -- in that order, nothing else, the stacks (min(5, ...)) and
      the clock (2.6) the engine's; outside the window, or on the killing
      blow, the channel's hex 1 alone; hex applied by her blows on a live
      body in windows, divided by those blows, not exactly 1 + hexExtra (2
      from stage 3); a link whose `hexExtra` is not the stage's; or a blow
      whose damage is not the blade's own (rebuilt from the captured crit and
      jitter draws), in the window and out
  [5] nothing else, read as EVERY OWN FIELD of both fighters, every shade and
      the match (a primitive by value, an object by its JSON, an array of the
      match's by its length): a tickUnmake call that moves any field but
      `ultUnmake`, `unmakeTally` and `hexStunMul` -- a hex clock, a reach, a
      stun, a charge, a position, an hp, a status, anything -- or the match's
      clock, hit stop, shots, beats or end; the second-hex insert (bracketed
      from its own `self.ultUnmake` read to Deadfall's `self.ultDeadfall` read
      right after it) moving any field but the caster's `unmakeTally` (blows +1,
      extra + hexExtra when it hexes) and, through an apply() that [4] audits,
      the struck body's statuses; either one hurting, filing a beat, drawing the
      rng or spawning a shot; and a fighter's hex clock moving anywhere between
      two of its tickStatus calls
  [6] the bolt is out: a cast that spawns a shot, hurts anybody, applies any
      status, moves an hp or a ward, that does not open {t: 0, dur}, that
      lands on an open window, or that moves any field of either fighter, a
      shade or the match beyond fireUlt's shared prologue (the caster's
      `ultsFired` +1; the match's banner, events, shake, hit stop, beats and
      ultFx record) and the window it opens (`ultUnmake`, `unmakeTally`); an
      ult block that is not the design's (kind "unmake", charge 14 -- the
      builder's), or that still carries the bolt's dmg / apply; a blade that is
      not the stage's (the shipped 8.81 at stages 2-3; one of the builder's
      stage-5 blades at stage 5: 7.5 the carry, 8.30 / 7.7 Rick's others)

STAGE 6 (the picture and the voice, the builder's readings 13-20), each check
run only where the link carries it -- the voices detected by the stun's arm
(`spellbreaker-stun`) in `AC.SFX.play.toString()`, the picture by
`tickUnmaking` on the Match -- so the same probe still gates stages 2-5 at 6/6,
every line as before. Once a fight is over the probe steps 2 s more of the
verdict (the step's `over` path: only the presentation clock runs) for these
two checks alone; [1]-[6] read none of those steps.
  [7] THE VOICES fire exactly on their events and nowhere else (v79 §4's
      sound). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Spellbreaker's three arms ("ult" with w "spellbreaker",
      "spellbreaker-stun", "spellbreaker-close") are read; a ward's shatter --
      which plays its own crit HIT voice inside hurt() -- is not one of them,
      nor is any other relic's cast. Evidence: a Spellbreaker cast playing
      anything but exactly one cast voice (w "spellbreaker") inside fireUlt, or
      the cast voice anywhere else; a tickStatus call whose voices are not
      EXACTLY one stun voice for each hex proc [2] saw at more than x1 (the
      proc's own hexStunMul) and none for a proc at x1, on any body; a
      tickUnmake call whose voices are not exactly the close voice for each
      window closing BY ITS CLOCK with both alive, and NEVER ON A CLOSE BY A
      DEATH; any of them in the picture's hook, a drawn frame or the verdict.
      Every one of the run is accounted for: cast voices = casts, stun voices =
      the x2 procs, close voices = clock closes; and x1 procs and death closes
      must each have been seen silent (NOT EXERCISED otherwise).
  [8] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickUnmaking`
      (tickPresentation, the picture's one call on the step path) is wrapped:
      evidence is any change across it to either fighter or a shade (every own
      number, flag and string but its `unmk*` fields, every array's length,
      every status, the window, the tally, the weapon row and its ult) or to
      the match (every own number, flag and string, every array's length, every
      shot's x, y, vx, vy and life; the tags by membership, each tag's `val`
      and `unmk` read below), an RNG draw or a voice. And the picture as
      declared, REBUILT from what the simulation did, the way [2] rebuilds the
      cadence (readings 13-15): the script not up (`unmkFade` 1) in an open
      window (`ultUnmake`, the match live, the caster alive) or its write clock
      not the presentation clock since the cast, up with none, or a close that
      is not a fade to 0 over exactly 0.4 of its clock (0.2 s) -- by the
      clock, on a death or AT THE KILL; a mote born outside a window, off her
      blades, or not at the rebuilt shedding rate (8 a clock unit a blade);
      THE TAG: every HEX tag pushed by a blow of hers that laid the second hex
      (read in resolveHit) relabelled `+2` at the next call, and no other tag
      ever relabelled (the match's first hex tag, a teaching panel, kept);
      THE GREY: on each fighter, rebuilt from the hex procs tickStatus ran --
      a proc at more than x1 (the sim's own factor) starts it at stunFor x mul,
      clamped to the fighter's stun; it counts down with the stun, never
      rises but at such a proc, and is 0 whenever the stun is -- so an x1
      proc never greys a weapon; the foe carrying the script or the motes; and
      the script up or a mote alive after 2 s of the verdict.
  --drawn N (default 6; 0 = off): on the FIRST seed, both sides, every foe,
      each fight is also drawn through the renderer (`AC.__draw`, the post
      chain off, 270x480) every Nth step while the picture shows and every
      60th otherwise, through the kill and the verdict. [8] fails a drawn
      frame that throws, draws the match's RNG or changes the simulation (the
      snapshot above). It runs on any link, so the base's draws are its
      control.

Printed besides, not checked: every number BY SIDE (A: Spellbreaker is the
Match's a), so a side gap in the win rate can be read against the mechanism
on each side; and in the json a digest of every fight (won / lost, steps), so
a mutant's changed fights can be counted against the link's.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import spellbreaker_build as SB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--stage", choices=["2", "3", "5"], default=None,
                help="the builder stage this link is (default: inferred from the blade, then hexExtra)")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=111001)
ap.add_argument("--json", default=None)
ap.add_argument("--foes", default="", help="comma list of foes (default: every other relic)")
ap.add_argument("--sides", default="AB", help="AB (both sides, the default) or A (the lab's side)")
ap.add_argument("--seedstep", type=int, default=13, help="seeds are seed0 + seedstep x i (the lab's is 11)")
ap.add_argument("--drawn", type=int, default=6, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()

BLOCK = r"""() => { const w = AC.WEAPONS.find(x => x.id === "spellbreaker"), u = w.ult;
  return { charge: u.charge, dur: u.dur, stunMul: u.stunMul, hexExtra: u.hexExtra, kind: u.kind,
           dmg: u.dmg, apply: u.apply, blade: w.dmg }; }"""

JS = r"""([seeds, foeList, sides, wantExtra, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, ST = AC.STATUS, HX = ST.hex;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickUnmake, oFire = P.fireUlt, oWeap = P.tickWeapon, oResolve = P.resolveHit,
        oStep = P.step, oStatus = P.tickStatus;
  let live = false, per = null, calls = 0;
  const winMT = new WeakMap();
  const isMe = f => !!(f && f.w && f.w.id === "spellbreaker");
  const nm = h => h && h.w ? (h.shade ? "shade:" : "") + h.w.id : String(h);
  const srcName = s => typeof s === "object" && s ? "a Fighter" : JSON.stringify(s);
  const stat = f => JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
  /* ---- THE WORLD, FIELD BY FIELD ([5], [6]). Every own enumerable field of both fighters and every
     shade: a primitive by value, a function by identity, an object by its JSON (a shade's `{ owner }`
     with the Fighter by identity, so the owner is not serialised whole), an array by its JSON when it is
     short and, when it is a long history (a trail, a blade tip's path), by its length and its first and
     last entries. THE THREE SHARED TABLES A FIGHTER POINTS AT -- `w` (the WEAPONS row), `aff` (the
     AFFINITIES entry) and `slM` (the school's spring constants) -- by identity on every call, and by their
     JSON at every fight's start and end (the builder refuses any write to them; nothing in the base
     writes them). The match: every own field but the two fighters, a primitive by value, an array by
     its length, an object by identity. */
  const ids = new WeakMap(); let nid = 0;
  const idOf = o => { if (!ids.has(o)) ids.set(o, ++nid); return ids.get(o); };
  let FC = null, snapping = false;
  const rep = (k, v) => (k !== "" && v && typeof v === "object" && ((FC && v instanceof FC) || v instanceof AC.Match)) ? "@" + idOf(v) : v;
  const js = v => { try { return JSON.stringify(v, rep); } catch (e) { return "ref@" + idOf(v); } };
  const jsPlain = v => { try { return JSON.stringify(v); } catch (e) { return "ref@" + idOf(v); } };
  const arr = (v, d) => v.length <= 16 && !(v.length && Array.isArray(v[0])) ? "a" + js(v)
                      : Array.isArray(v[0]) && d < 1 ? "A" + v.length + "[" + v.map(x => arr(x, d + 1)).join(",") + "]"
                      : "A" + v.length + ":" + js(v[0]) + ":" + js(v[v.length - 1]);
  const SHARED = new Set(["w", "aff", "slM"]);
  const val = (k, v) => v === null || (typeof v !== "object" && typeof v !== "function") ? v
                 : typeof v === "function" ? "fn@" + idOf(v)
                 : SHARED.has(k) ? "ref@" + idOf(v)
                 : Array.isArray(v) ? arr(v, 0)
                 : "j" + js(v);
  const snapF = f => { const keys = Object.keys(f), vals = new Array(keys.length);
    for (let i = 0; i < keys.length; i++) vals[i] = val(keys[i], f[keys[i]]); return { keys, vals }; };
  const snapM = m => { const keys = Object.keys(m).filter(k => k !== "a" && k !== "b"), vals = keys.map(k => { const v = m[k];
    return v === null || (typeof v !== "object" && typeof v !== "function") ? v : typeof v === "function" ? "fn@" + idOf(v)
             : Array.isArray(v) ? "len" + v.length : "ref@" + idOf(v); }); return { keys, vals }; };
  const world = m => { snapping = true; try { const fs = [m.a, m.b, ...(m.shades || [])];
    return { m: snapM(m), fs: fs.map(f => [f, snapF(f)]) }; } finally { snapping = false; } };
  const dmap = (A, B, allow) => { const out = [];
    if (A.keys.length === B.keys.length && A.keys.every((k, i) => k === B.keys[i])){
      for (let i = 0; i < A.keys.length; i++) if (!Object.is(A.vals[i], B.vals[i]) && !(allow && allow.has(A.keys[i]))) out.push(A.keys[i]);
      return out; }
    const a = new Map(A.keys.map((k, i) => [k, A.vals[i]])), b = new Map(B.keys.map((k, i) => [k, B.vals[i]]));
    for (const k of new Set([...a.keys(), ...b.keys()])){
      if (allow && allow.has(k)) continue; if (!a.has(k) || !b.has(k) || !Object.is(a.get(k), b.get(k))) out.push(k); } return out; };
  /* the shared tables' JSON: `slM` is resolved on first use (null before), so it is compared only once set */
  const sharedJSON = m => [m.a, m.b].map(f => jsPlain(f.w) + jsPlain(f.aff)).join("|");
  const slmJSON = m => [m.a, m.b].map(f => f.slM ? jsPlain(f.slM) : "").join("|");
  /* the moved fields, as "who.field", beyond what `allowF(f)` / `allowM` let move */
  const wdiff = (W0, W1, allowF, allowM) => { const out = [];
    const f0 = W0.fs.map(x => x[0]), f1 = W1.fs.map(x => x[0]);
    if (f0.length !== f1.length || f0.some((f, i) => f !== f1[i])) out.push("the bodies on the floor");
    for (const k of dmap(W0.m, W1.m, allowM)) out.push("match." + k);
    for (const [f, s0] of W0.fs){ const e = W1.fs.find(x => x[0] === f); if (!e) continue;
      for (const k of dmap(s0, e[1], allowF(f))) out.push(nm(f) + "." + k); }
    return out; };
  const TICK_OK = new Set(["ultUnmake", "unmakeTally", "hexStunMul"]), NONE = new Set();
  const CAST_M = new Set(["banner", "events", "shake", "hitStop", "beats", "ultFx"]);
  /* the field as last written by tickUnmake, per fighter: [3] asserts nothing else moves it */
  const lastField = new WeakMap();
  /* the hex clock at the end of each fighter's last tickStatus: [5] asserts nothing else moves it */
  const lastHC = new WeakMap();
  /* a clean stun run per fighter: { mul, len, calls, prev } */
  const run = new WeakMap();

  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: the stun's arm in the synth [7], `tickUnmaking` on the
     match [8]. A link without them runs [1]-[6] only. ---- */
  const S6V = /spellbreaker-stun/.test(AC.SFX.play.toString()), S6P = typeof P.tickUnmaking === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oUnmk = P.tickUnmaking;
  let F = null, vctx = "a step", vrec = null, tail = false;
  const OURS = { "spellbreaker": "the cast", "spellbreaker-stun": "the hex proc", "spellbreaker-close": "the Unmaking's ticker" };
  const isOurs = (kind, q) => kind === "ult" && !!q && Object.prototype.hasOwnProperty.call(OURS, q.w);
  const oursIn = rec => rec.filter(c => isOurs(c[0], c[1])).map(c => c[1].w);
  if (S6V) AC.SFX.play = function(kind, q){
    if (F){
      if (vrec) vrec.push([kind, q ? Object.assign({}, q) : q]);
      if (isOurs(kind, q)){
        if (vctx !== OURS[q.w]) fail(7, `the ${q.w} voice played in ${vctx}`);
        inc("v_" + q.w);
      }
    }
    return oPlay.call(this, kind, q);
  };
  /* [8] the simulation's state, as one array in a fixed key order: both fighters' and every shade's own
     numbers, flags and strings (their `unmk*` fields aside) and array lengths, statuses, the window, the
     tally, the weapon row and its ult; the match's own numbers, flags and strings and every array's length,
     and every shot's x, y, vx, vy and life. The tags are read apart (by membership, `val` and `unmk`). */
  const same = (x, y) => x === y || (x !== x && y !== y);
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b, ...(m.shades || [])]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 117 && k.startsWith("unmk")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      for (const k in f.status){ const st = f.status[k]; o.push(k, st.stacks, st.t, st.src); }
      const Z = f.ultUnmake;
      if (Z) o.push("Z", Z.t, Z.dur); else o.push("Z-");
      const T = f.unmakeTally;
      if (T) for (const k of Object.keys(T)) o.push(k, T[k]); else o.push("T-");
      if (f.w){ for (const k of Object.keys(f.w)){ const v = f.w[k]; if (v === null || typeof v !== "object") o.push(k, v); }
        if (f.w.ult) for (const k of Object.keys(f.w.ult)){ const v = f.w.ult[k]; if (v === null || typeof v !== "object") o.push(k, v); } }
    }
    for (const k of Object.keys(m)){
      const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    for (const sh of m.shots) o.push(sh.x, sh.y, sh.vx, sh.vy, sh.life);
    return o;
  };
  const firstDiff = (s0, s1) => {
    if (s0.length !== s1.length) return `the shape ${s0.length} -> ${s1.length} fields`;
    for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i]))
      return `${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}`;
    return null; };
  let PM = null;                       // [8] the script and the motes, rebuilt: per fight
  const PG = new Map();                // [8] the grey, rebuilt: per fighter, per fight
  const pend = new Map();              // [8] the hex proc tickStatus ran on a fighter since the last picture call
  const relabel = new Map();           // [8] the HEX tags a second-hex blow pushed, awaiting the next picture call

  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [7]-[8] alone */
    if (tail) return oStep.call(this, dt);
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;
    const wasLive = live;
    for (const f of [this.a, this.b]) if (f.ultUnmake){ if (live) inc("winLive"); else inc("winFrozen"); }
    for (const f of [this.a, this.b]) if (f.ultUnmake && winMT.has(f.ultUnmake)) winMT.get(f.ultUnmake).mt += dt;
    for (const f of [this.a, this.b])
      if (lastField.has(f) && f.hexStunMul !== lastField.get(f)) fail(3, `${nm(f)}'s hexStunMul moved outside tickUnmake: ${lastField.get(f)} -> ${f.hexStunMul}`);
    calls = 0;
    const r = oStep.call(this, dt);
    if (wasLive && calls !== 1) fail(1, `${calls} tickUnmake call(s) on an unfrozen step`);
    else if (!wasLive && calls) fail(1, `${calls} tickUnmake call(s) on a frozen step`);
    else if (wasLive) inc("tickStepOk");
    for (const f of [this.a, this.b])
      if (lastField.has(f) && f.hexStunMul !== lastField.get(f)) fail(3, `${nm(f)}'s hexStunMul moved outside tickUnmake: ${lastField.get(f)} -> ${f.hexStunMul}`);
    live = false;
    return r;
  };

  /* [2] THE HEX PROC AND ITS CADENCE, read inside tickStatus through its own breakSpin call */
  P.tickStatus = function(f, dt){
    const stun0 = f.stun, hc0 = f.hexClock, oBS = this.breakSpin, procs = [];
    /* [5] the hex clock moves in tickStatus and nowhere else */
    if (lastHC.has(f)){ if (!Object.is(hc0, lastHC.get(f))) fail(5, `${nm(f)}'s hex clock moved between tickStatus calls: ${lastHC.get(f)} -> ${hc0}`); else inc("hcContOk"); }
    this.breakSpin = function(ff, reason, trueFor){
      if (ff === f && reason === "the hex takes the wind out of it") procs.push({ trueFor, stun: ff.stun, mul: ff.hexStunMul });
      return oBS.call(this, ff, reason, trueFor);
    };
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "the hex proc"; vrec = [];
    try { r = oStatus.call(this, f, dt); } finally { delete this.breakSpin; heard = vrec; vctx = vc0; vrec = vr0; }
    lastHC.set(f, f.hexClock);
    const real = f === this.a || f === this.b, foe = real ? (f === this.a ? this.b : this.a) : null;
    const where = f.shade ? "shade" : isMe(f) ? "me" : (foe && foe.ultUnmake) ? "in" : "out";
    if (procs.length > 1) fail(2, `${procs.length} hex procs in one tickStatus`);
    /* [7] THE STUN VOICE: one for each proc at more than x1 (the proc's own factor), none at x1, any body */
    if (S6V && F && F.m === this){
      const mine = oursIn(heard), want = procs.filter(p => p.mul > 1).map(() => "spellbreaker-stun");
      if (JSON.stringify(mine) !== JSON.stringify(want))
        fail(7, `a tickStatus on ${nm(f)} (${where}) played ${JSON.stringify(mine)}, want ${JSON.stringify(want)} (procs at x${JSON.stringify(procs.map(p => p.mul))})`);
      else if (want.length) inc(`stunVoiceOk_${where}`);
      else if (procs.length) inc(`procQuietOk_${where}`);
    }
    /* [8] the proc, for the grey's rebuild at the next picture call */
    if (procs.length && real) pend.set(f, procs[procs.length - 1]);
    /* THE CADENCE, rebuilt: c = c0 + dt x stacks; a proc (and the clock to 0) exactly when c >= stunEvery */
    const hx = f.stacks("hex");
    let wantHC = hc0, wantP = 0;
    if (hx > 0){ const c = hc0 + dt * hx; if (c >= HX.stunEvery){ wantHC = 0; wantP = 1; } else wantHC = c; }
    if (!Object.is(f.hexClock, wantHC) || procs.length !== wantP)
      fail(2, `${nm(f)} (${where}): hex clock ${hc0} -> ${f.hexClock} at ${hx} stacks with ${procs.length} proc(s); the engine's cadence says ${wantHC} and ${wantP}`);
    else { inc("cadenceOk"); if (wantP) inc(`cadenceProc_${where}`); }
    /* the clean run in progress, if any */
    const R0 = run.get(f);
    if (R0 && !procs.length){
      if (stun0 !== R0.prev){ run.delete(f); inc("runDirty"); }
      else {
        R0.calls++;
        if (f.stun <= 0){ run.delete(f); const L = R0.calls * dt; inc(`runN_${R0.tag}`); inc(`runL_${R0.tag}`, L);
          const lo = `runMin_${R0.tag}`, hi = `runMax_${R0.tag}`;
          if (n[lo] === undefined || L < n[lo]) n[lo] = L; if (n[hi] === undefined || L > n[hi]) n[hi] = L; }
        else R0.prev = f.stun;
      }
    }
    for (const p of procs){
      const want = HX.stunFor * p.mul;
      if (p.trueFor !== want) fail(2, `a hex proc on ${nm(f)} (${where}) ran ${p.trueFor}s, want stunFor x hexStunMul = ${want}`);
      else if (p.stun !== Math.max(stun0, want)) fail(2, `a hex proc on ${nm(f)} (${where}) left the weapon's stun ${p.stun}, want max(${stun0}, ${want})`);
      else inc(`proc_${where}_x${p.mul}`);
      if (R0) { run.delete(f); if (!(stun0 === R0.prev)) inc("runDirty"); else inc("runCut"); }
      if (stun0 === 0 && !f.shade) run.set(f, { tag: `${where}_x${p.mul}`, calls: 1, prev: f.stun });
      else if (!f.shade) inc("procOnStun");
    }
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isMe(f)) return oFire.call(this, f, foe);
    const open = !!f.ultUnmake, ns = this.shots.length, W0 = world(this), fired0 = f.ultsFired;
    const st = [f, foe].map(x => ({ x, hp: x.hp, shield: x.shield, stat: stat(x) }));
    const oHurt = this.hurt, hurts = [], applies = [];
    this.hurt = function(t, d, s){ hurts.push([t, d, s]); return oHurt.call(this, t, d, s); };
    for (const x of [f, foe]){ const o = x.apply; x.apply = function(k, nn, src){ applies.push([x, k, nn]); return o.call(this, k, nn, src); }; }
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "the cast"; vrec = [];
    try { r = oFire.call(this, f, foe); }
    finally { delete this.hurt; delete f.apply; delete foe.apply; heard = vrec; vctx = vc0; vrec = vr0; }
    /* [7] THE CAST'S VOICE: exactly one, inside fireUlt (the prologue's `SFX.play("ult", { w: f.w.id })`) */
    if (S6V && F && F.m === this){
      const mine = oursIn(heard);
      if (mine.length !== 1 || mine[0] !== "spellbreaker") fail(7, `a Spellbreaker cast played ${JSON.stringify(mine)}, want one cast voice`);
      else inc("castVoiceOk");
    }
    const W1 = world(this);
    const moved = wdiff(W0, W1, x => x === f ? new Set(["ultsFired", "ultUnmake", "unmakeTally"]) : NONE, CAST_M);
    const u = f.w.ult;
    if (open) fail(6, "a cast on an open window");
    else if (this.shots.length !== ns) fail(6, `the cast spawned ${this.shots.length - ns} shot(s)`);
    else if (hurts.length || applies.length) fail(6, `the cast hurt ${hurts.length} and applied ${JSON.stringify(applies.map(x => [nm(x[0]), x[1], x[2]]))}`);
    else if (st.some(s => s.x.hp !== s.hp || s.x.shield !== s.shield)) fail(6, `the cast moved an hp or a ward: ${JSON.stringify(st.map(s => [nm(s.x), s.hp, s.x.hp, s.shield, s.x.shield]))}`);
    else if (st.some(s => stat(s.x) !== s.stat)) fail(6, "the cast moved a status");
    else if (moved.length) fail(6, `the cast moved ${moved.join(", ")}`);
    else if (f.ultsFired !== fired0 + 1) fail(6, `ultsFired ${fired0} -> ${f.ultsFired}`);
    else if (!f.ultUnmake || f.ultUnmake.t !== 0 || f.ultUnmake.dur !== u.dur || Object.keys(f.ultUnmake).length !== 2) fail(6, `the cast opened ${JSON.stringify(f.ultUnmake)}`);
    else { inc("castOk"); winMT.set(f.ultUnmake, { mt: 0 }); }
    return r;
  };

  /* the foe's weapon, stunned or free, on the frames of a window and outside one */
  P.tickWeapon = function(f, foe, dt){
    if ((f === this.a || f === this.b) && !isMe(f) && foe && isMe(foe) && foe.unmakeTally){
      const k = foe.ultUnmake ? "In" : "Out", sd = foe === this.a ? "A" : "B";
      inc("foeWeap" + k); if (f.stun > 0) inc("foeStun" + k);
      inc("foeWeap" + k + sd); if (f.stun > 0) inc("foeStun" + k + sd);
    }
    return oWeap.call(this, f, foe, dt);
  };

  let inRH = 0;
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isMe(self) || inRH) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const M = this, open = !!self.ultUnmake, d0 = self.dealt, c0 = self.crits, h0 = self.hits, side = self === this.a ? "a" : "b";
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis,
                  echo: Math.round(foe.curseEcho()), hex: foe.stacks("hex") };
    const draws = [], oRng = this.rng, applies = [], oAp = foe.apply;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    foe.apply = function(k, nn, src){ const e = [k, nn, src, M._brk]; applies.push(e); const rr = oAp.call(this, k, nn, src);
      e.push(foe.stacks(k), foe.status[k] ? foe.status[k].t : null); return rr; };
    /* [5] THE SECOND-HEX INSERT, BRACKETED: its head is the one read of `self.ultUnmake` in resolveHit (the
       insert's own `if`), its tail the read of `self.ultDeadfall` that follows it (Deadfall's `if`). */
    const hold = { u: self.ultUnmake, d: self.ultDeadfall };
    let head = null, tail = null, aliveHead = null, tally0 = null;
    M._brk = 0;
    Object.defineProperty(self, "ultUnmake", { configurable: true, enumerable: true,
      get(){ if (!snapping && !head){ head = world(M); aliveHead = foe.alive; tally0 = self.unmakeTally ? Object.assign({}, self.unmakeTally) : null; M._brk = 1; } return hold.u; },
      set(v){ if (!snapping) fail(5, "ultUnmake written inside resolveHit"); hold.u = v; } });
    Object.defineProperty(self, "ultDeadfall", { configurable: true, enumerable: true,
      get(){ if (!snapping && head && !tail){ M._brk = 0; tail = world(M); } return hold.d; },
      set(v){ hold.d = v; } });
    let r;
    const tg0 = this.tags.length;
    inRH++;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { inRH--; this.rng = oRng; delete foe.apply; delete M._brk;
      Object.defineProperty(self, "ultUnmake", { value: hold.u, writable: true, enumerable: true, configurable: true });
      Object.defineProperty(self, "ultDeadfall", { value: hold.d, writable: true, enumerable: true, configurable: true }); }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    const where = open ? "IN" : "out of";
    /* [5] the insert moved nothing but her tally and, through apply(), the struck body's statuses */
    const inIns = applies.filter(x => x[3] === 1);
    /* [8] THE TAG: the HEX tag(s) a blow that laid the second hex pushed must read +2 at the next picture call */
    if (S6P && F && F.m === this && open && inIns.length){
      const fresh = this.tags.slice(tg0).filter(g => g.key === "hex");
      if (!fresh.length) inc("secondHexNoTag");
      for (const g of fresh) relabel.set(g, { first: !!g.first });
    }
    if (head && tail){
      const moved = wdiff(head, tail, x => x === self ? new Set(["unmakeTally"]) : (x === foe && inIns.length) ? new Set(["status"]) : NONE, NONE)
                    .filter(k => !(k === "match._brk"));
      const t1 = self.unmakeTally;
      const wantT = tally0 && open ? Object.assign({}, tally0, { blows: tally0.blows + 1,
                      extra: tally0.extra + inIns.reduce((q, x) => q + x[1], 0) }) : tally0;
      if (moved.length) fail(5, `the second-hex insert moved ${moved.join(", ")}`);
      else if (JSON.stringify(t1) !== JSON.stringify(wantT)) fail(5, `the insert's tally ${JSON.stringify(tally0)} -> ${JSON.stringify(t1)}, want ${JSON.stringify(wantT)}`);
      else inc(open ? "insertInOk" : "insertOutOk");
    } else inc(head ? "insertOpenEnded" : "insertUnread");
    /* the blade's own damage */
    const D = self.dealt - d0, crit = self.crits > c0;
    const raw = self.w.dmg * (mul === undefined ? 1 : mul) * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw) + pre.echo;
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis) inc("blowExempt"); else fail(4, `${where} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    /* the blow's statuses on the body it struck: the channel's, then (in the window, on a body the blow left
       alive) the STAGE's second hex -- never the link's own number */
    const aliveI = head ? aliveHead : foe.alive;
    const ex = open && wantExtra > 0 && aliveI;
    const wantAp = ex ? [["hex", 1, undefined], ["hex", wantExtra, side]] : [["hex", 1, undefined]];
    const got = applies.map(x => [x[0], x[1], x[2]]);
    if (JSON.stringify(got.map(g => [g[0], g[1], srcName(g[2])])) !== JSON.stringify(wantAp.map(g => [g[0], g[1], srcName(g[2])]))){
      if (pre.aegis && !applies.length) inc("blowExempt");
      else fail(4, `${where} the window${open && !aliveI ? " (the killing blow)" : ""}: a blow on ${nm(foe)} applied ${JSON.stringify(got.map(g => [g[0], g[1], srcName(g[2])]))}, want ${JSON.stringify(wantAp.map(g => [g[0], g[1], srcName(g[2])]))}`);
    } else {
      let s = pre.hex, okS = true;
      for (const x of applies){ s = s < HX.maxStacks ? Math.min(HX.maxStacks, s + x[1]) : s; if (x[4] !== s || x[5] !== HX.dur) okS = false; }
      if (!okS) fail(4, `${where} the window: hex ${pre.hex} -> ${JSON.stringify(applies.map(x => [x[4], x[5]]))}, the engine's arithmetic says ${s}`);
      else { inc(open ? "chanInOk" : "chanOutOk");
        if (open){ const q = applies.reduce((z, x) => z + x[1], 0);
          if (aliveI){ inc("hexAppliedInLive", q); inc("blowsInLive"); } else { inc("hexAppliedKill", q); inc("blowsInKill"); }
          if (foe.shade) inc("blowOnShadeIn"); } }
    }
    return r;
  };

  P.tickUnmake = function(dt){
    calls++;
    if (!live) fail(1, "tickUnmake on a frozen step");
    for (const f of [this.a, this.b]) if (f.ultUnmake && !isMe(f)) fail(1, `${f.w.id} carries ultUnmake`);
    const wins = [];
    for (const f of [this.a, this.b]){
      const Z = f.ultUnmake;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      wins.push({ f, foe, Z, t0: Z.t, fAlive: f.alive, foeAlive: foe.alive });
    }
    const W0 = world(this);
    const ns = this.shots.length, hurts = [], beats = [], applies = [];
    const oHurt = this.hurt, oB = this.beat, oRng = this.rng;
    let draws = 0;
    this.hurt = function(t, d, s){ hurts.push([t, d, s]); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oB.call(this, o); };
    this.rng = function(){ draws++; return oRng(); };
    const fs = [this.a, this.b, ...(this.shades || [])];
    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ applies.push([f, k, nn, src]); return o.call(this, k, nn, src); }; }
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "the Unmaking's ticker"; vrec = [];
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; heard = vrec; vctx = vc0; vrec = vr0; }
    /* [7] THE CLOSE VOICE: one for each window closing BY ITS CLOCK with both alive, none on a death's close */
    if (S6V && F && F.m === this){
      const want = [], vk = [];
      for (const w of wins){
        if (!(w.t0 + dt >= w.Z.dur || !w.fAlive || !w.foeAlive)) continue;
        if (w.fAlive && w.foeAlive){ want.push("spellbreaker-close"); vk.push("closeVoiceOk"); }
        else vk.push("closeDeathQuiet");
      }
      const mine = oursIn(heard);
      if (JSON.stringify(mine) !== JSON.stringify(want)) fail(7, `the Unmaking's ticker played ${JSON.stringify(mine)}, want ${JSON.stringify(want)}`);
      else for (const k of vk) inc(k);
    }
    /* [5] NOTHING ELSE: every own field of both fighters, every shade and the match */
    const moved = wdiff(W0, world(this), x => (x === this.a || x === this.b) ? TICK_OK : NONE, NONE);
    if (hurts.length) fail(5, `the Unmaking hurt ${JSON.stringify(hurts.map(h => [nm(h[0]), h[1]]))}`);
    if (beats.length) fail(5, `the Unmaking filed ${beats.length} beat(s)`);
    if (draws) fail(5, `the Unmaking drew the rng ${draws} time(s)`);
    if (applies.length) fail(5, `the Unmaking's tick applied ${JSON.stringify(applies.map(x => [nm(x[0]), x[1], x[2]]))}`);
    if (this.shots.length !== ns) fail(5, "the Unmaking spawned a shot");
    if (moved.length) fail(5, `the Unmaking's tick moved ${moved.join(", ")}`);
    else inc("tickWorldOk");
    inc("calls");
    /* [1] THE WINDOWS */
    for (const w of wins){
      const { f, foe, Z } = w, t1 = w.t0 + dt;
      if (t1 >= Z.dur || !w.fAlive || !w.foeAlive){
        if (f.ultUnmake === Z){ fail(1, "the window did not close"); continue; }
        if (f.ultUnmake) fail(1, "a new window at the close");
        if (w.fAlive && w.foeAlive){ inc("clockCloses"); const M = winMT.get(Z); if (M){ inc("winMT", M.mt); inc("winMTn"); } }
        else inc("deathCloses");
        continue;
      }
      if (f.ultUnmake !== Z){ fail(1, `closed at ${t1.toFixed(4)} of ${Z.dur}`); continue; }
      if (Z.t !== t1) fail(1, `window clock ${w.t0} -> ${Z.t}, want ${t1}`);
      else inc("frames");
    }
    /* [3] THE FIELD, RECOMPUTED FOR BOTH FIGHTERS: the OTHER fighter's stunMul while its window is open */
    for (const f of [this.a, this.b]){
      const o = f === this.a ? this.b : this.a;
      const want = o.ultUnmake ? o.w.ult.stunMul : 1;
      if (f.hexStunMul !== want) fail(3, `${nm(f)}'s hexStunMul ${f.hexStunMul}, want ${want} (other's window ${o.ultUnmake ? "open" : "shut"})`);
      else inc(want === 1 ? (isMe(f) ? "fieldMeOk" : "fieldFoeOutOk") : "fieldFoeInOk");
      if (o.ultUnmake && o.w.ult.stunMul !== 2) fail(3, `stunMul ${o.w.ult.stunMul}, the design's is 2`);
      lastField.set(f, f.hexStunMul);
    }
    for (const s of (this.shades || [])){ if (s.hexStunMul !== 1) fail(3, `a shade's hexStunMul is ${s.hexStunMul}`); else inc("fieldShadeOk"); }
    return r;
  };

  /* [8] THE PICTURE'S HOOK: `tickUnmaking`, on the presentation clock (tickPresentation: through hit
     stops, twice a normal step, and in the verdict). The picture is REBUILT from what the simulation did:
     the window, the procs tickStatus ran, the blows that laid the second hex (readings 13-15). */
  if (S6P) P.tickUnmaking = function(dt){
    if (!F || F.m !== this) return oUnmk.call(this, dt);
    inc("unmkCalls");
    const me = F.me, foe = F.foe;
    const s0 = simSnap(this), tg0 = this.tags.slice(), tv0 = tg0.map(g => [g.val, g.unmk]);
    const fade0 = me.unmkFade, moteN0 = me.unmkMoteN;
    let draws = 0; const oRng = this.rng;
    this.rng = function(){ draws++; return oRng.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture"; vrec = [];
    let r, heard = null;
    try { r = oUnmk.call(this, dt); } finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = firstDiff(s0, simSnap(this));
    if (d) fail(8, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (draws) fail(8, `the picture drew the RNG ${draws} times`);
    else if (heard.length) fail(8, `the picture played ${JSON.stringify(heard)}`);
    else if (this.tags.length !== tg0.length || this.tags.some((g, i) => g !== tg0[i])) fail(8, "the picture added, removed or moved a tag");
    else inc("unmkClean");
    /* the foe never carries the script or the motes */
    if (foe.unmkFade !== 0 || foe.unmkAge !== 0 || foe.unmkOut !== 0 || foe.unmkMotes.length || foe.unmkMoteN !== 0
        || foe.unmkSeenX !== 0) fail(8, `${foe.w.id}, which is not Spellbreaker, carries the script or the motes`);
    const busy = !!(this.a.unmakeTally || this.b.unmakeTally);
    /* THE TAG: every HEX tag a second-hex blow pushed reads +(1 + hexExtra) now; no other tag relabelled */
    for (let i = 0; i < tg0.length; i++){
      const g = tg0[i], [v0, u0] = tv0[i], want = relabel.get(g);
      if (want){
        relabel.delete(g);
        if (want.first){ if (g.val !== v0 || g.unmk !== u0) fail(8, "the match's first HEX tag (its teaching panel) relabelled"); else inc("tagFirstKept"); }
        else if (g.val !== "+" + (1 + wantExtra) || g.unmk !== true) fail(8, `a second hex's HEX tag reads ${JSON.stringify(g.val)} (unmk ${g.unmk}), want "+${1 + wantExtra}"`);
        else inc("tagOk");
      } else if (g.val !== v0 || g.unmk !== u0) fail(8, `a ${g.key} tag relabelled ${JSON.stringify(v0)} -> ${JSON.stringify(g.val)} that no second hex pushed`);
    }
    if (relabel.size) for (const g of [...relabel.keys()]) if (!this.tags.includes(g)){ relabel.delete(g); fail(8, "a second hex's HEX tag gone before a picture call"); }
    /* THE GREY, on each fighter, rebuilt from the procs tickStatus ran (the sim's own factor) */
    for (const f of [this.a, this.b]){
      const p = pend.get(f); pend.delete(f);
      if (!busy) continue;                                   // the picture's zero-burden return: nothing moves
      const G = PG.get(f) || { grey: 0, stun: 0 };
      const st = f.stun;
      let g;
      if (p && p.mul > 1){ g = HX.stunFor * p.mul; inc("greyStart"); }
      else if (st < G.stun) g = G.grey - (G.stun - st);
      else g = G.grey;
      g = Math.min(g, st);
      if (!(g > 1e-9)) g = 0;
      if (f.unmkGrey !== g) fail(8, `${nm(f)}'s grey ${f.unmkGrey}, the procs and its stun rebuild ${g} (stun ${st}${p ? ", a proc at x" + p.mul : ""})`);
      else if (g > 0) inc(this.hitStop > 0 ? "greyOnStop" : "greyOn");
      else inc(p ? "greyNoneOnX1" : "greyOffOk");
      if (p && p.mul > 1 && st === 0 && g === 0) inc("greyStartNoStun");
      if (g > G.grey) { if (!(p && p.mul > 1)) fail(8, `${nm(f)}'s grey rose with no proc at x2`); }
      G.grey = g; G.stun = st; PG.set(f, G);
    }
    const T = me.unmakeTally;
    if (!T){
      if (me.unmkFade !== 0 || me.unmkMotes.length || me.unmkMoteN !== 0) fail(8, "Spellbreaker carries the picture before her first cast");
      return r;
    }
    if (!PM) PM = { prevZ: null, age: 0, closeDt: -1, acc: 0, moteN: 0 };
    const Z = (this.over || !me.alive) ? null : me.ultUnmake;
    /* THE SCRIPT: up exactly while the window is open, its write clock the presentation clock since the
       cast; a 0.2 s unwrite (0.4 of the clock) at any close */
    if (Z){
      if (PM.prevZ !== Z){ PM.age = 0; inc("picCasts"); }
      PM.age += dt;
      if (me.unmkFade !== 1) fail(8, `the script not up (${me.unmkFade}) in an open window`);
      else if (me.unmkAge !== PM.age) fail(8, `the script's write clock ${me.unmkAge}, want ${PM.age}`);
      else inc(PM.age < 0.6 ? "scriptWriting" : "scriptUpOk");
      PM.closeDt = -1;
    } else if (fade0 > 0){
      if (PM.closeDt < 0){ PM.closeDt = 0;
        inc(this.over ? (me.ultUnmake ? "picCloseOverOpen" : "picCloseOver") : !me.alive ? "picCloseDeath"
            : !foe.alive ? "picCloseFoeDeath" : "picCloseClock"); }
      PM.closeDt += dt;
      const want = Math.max(0, 1 - PM.closeDt / 0.4);
      if (Math.abs(me.unmkFade - want) > 1e-9) fail(8, `the script's unwrite: ${me.unmkFade} at ${PM.closeDt.toFixed(4)} of its clock, want ${want}`);
      else if (me.unmkFade === 0) inc("scriptGoneOk"); else inc("scriptUnwriting");
    } else if (me.unmkFade !== 0) fail(8, `the script up (${me.unmkFade}) with no window open`);
    PM.prevZ = Z;
    /* THE MOTES: born only in an open window, at 8 a clock unit a blade, off her blades; none older than 1.1 */
    let births = 0;
    if (Z){ PM.acc += dt * 8; const nb = (me.bladeSet || me.w.blades).length; while (PM.acc >= 1){ PM.acc -= 1; births += nb; } }
    PM.moteN += births;
    if (me.unmkMoteN !== PM.moteN) fail(8, `motes born ${me.unmkMoteN - moteN0} on this call, the shedding clock says ${births}${Z ? "" : " (no window open)"}`);
    else if (births) inc("motesBorn", births);
    const M = me.unmkMotes, Rb = C.physics.ballR, Lr = me.w.reach * this.actMods.reach * me.reachMul + 6 + me.w.artW;
    if (M.length > 48 || M.some(o => !(o.t < 1.1) || !Number.isFinite(o.x) || !Number.isFinite(o.y))) fail(8, "a mote past its life, past the cap of 48, or off the page");
    for (const o of M) if (o.t === 0){ if (Math.hypot(o.x - me.x, o.y - me.y) > Rb + Lr) fail(8, "a mote born off her blades"); else inc("moteOnBlade"); }
    if (!Z && M.length) inc("motesOutlive");
    return r;
  };

  /* THE DRAWN SUBSET [8]: a frame through the renderer, the simulation read before and after */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.unmkFade > 0 || (q.unmkMotes && q.unmkMotes.length) || q.unmkGrey > 0);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), tg0 = m.tags.map(g => g.val), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx; vctx = "a drawn frame";
    let threw = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; vctx = vc0; }
    const d = firstDiff(s0, simSnap(m));
    if (threw) fail(8, "a drawn frame threw: " + threw);
    else if (dr) fail(8, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(8, "a drawn frame changed the simulation: " + d);
    else if (m.tags.length !== tg0.length || m.tags.some((g, i) => g.val !== tg0[i])) fail(8, "a drawn frame changed a tag");
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict");
           if ([m.a, m.b].some(q => q.unmkGrey > 0)) inc("drawGrey"); }
  };

  const foes = foeList.length ? foeList : AC.WEAPONS.map(w => w.id).filter(i => i !== "spellbreaker");
  const T = { casts: 0, frames: 0, blows: 0, extra: 0, foeHex: 0 };
  /* BY SIDE (A = Spellbreaker is m.a): the same tallies, so a side gap in the win rate can be read
     against the mechanism on each side. DIGEST: every fight's outcome (Spellbreaker won 1 / lost 0 /
     undecided -1) and its length in steps, so a mutant's changed fights can be counted. */
  const TS = [0, 1].map(() => ({ casts: 0, frames: 0, blows: 0, extra: 0, foeHex: 0, fights: 0, wins: 0, decided: 0, bin: 0 }));
  const digest = [];
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  const t0 = Date.now();
  for (const side of sides) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "spellbreaker", sd) : new AC.Match("spellbreaker", fid, sd);
    if (!FC) FC = m.a.constructor;
    const me = side ? m.b : m.a;
    for (const f of [m.a, m.b]){ if (f.hexStunMul !== 1) fail(3, `a fresh Match's ${nm(f)} carries hexStunMul ${f.hexStunMul}`); else inc("freshOk"); }
    per = { in: 0, out: 0 };
    let steps = 0;
    const sh0 = sharedJSON(m);
    let slm0 = null;
    if (S6P) for (const f of [m.a, m.b]){
      if (f.unmkFade !== 0 || f.unmkAge !== 0 || f.unmkOut !== 0 || !Array.isArray(f.unmkMotes) || f.unmkMotes.length
          || f.unmkMoteN !== 0 || f.unmkSeenX !== 0 || f.unmkGrey !== 0 || f.unmkMul !== 1) fail(8, `a fresh Match's ${nm(f)} carries a picture`);
      else inc("picFreshOk");
    }
    F = { m, me, foe: side ? m.a : m.b };
    PM = null; PG.clear(); pend.clear(); relabel.clear();
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    try {
      while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (slm0 === null && m.a.slM && m.b.slM) slm0 = slmJSON(m); if (drawn) drawFrame(m, steps); }
      /* [7]-[8] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
      if ((S6V || S6P) && m.over){
        const open = !!me.ultUnmake, up = me.unmkFade > 0, o7 = (n.x7 || 0);
        tail = true; vctx = "the verdict";
        try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); if (drawn) drawFrame(m, steps + i + 1); } }
        finally { tail = false; vctx = "a step"; }
        if (S6V && (n.x7 || 0) === o7) inc(open ? "verdictQuietOpen" : "verdictQuiet");
        if (S6P && me.unmakeTally){
          if (me.unmkFade !== 0 || me.unmkMotes.length)
            fail(8, `after 2 s of the verdict the script at ${me.unmkFade}, ${me.unmkMotes.length} motes${open ? " -- the window the sim left open" : ""}`);
          else inc(up ? (open ? "endGoneOpen" : "endGoneUp") : "endGoneOk");
          if ([m.a, m.b].some(q => q.unmkGrey > 0)) inc("greyAtVerdict");
        }
      }
    } finally { F = null; }
    if (sharedJSON(m) !== sh0 || (slm0 !== null && slmJSON(m) !== slm0))
      fail(5, `a shared table (the WEAPONS row, the AFFINITIES entry or the springs) moved during ${fid} ${sd}`);
    else inc("sharedOk");
    fights++; bin += per.in; bout += per.out;
    const S_ = TS[side]; S_.fights++; S_.bin += per.in;
    if (m.winner){ decided++; S_.decided++; if (m.winner === me){ wins++; S_.wins++; } }
    if (me.unmakeTally) for (const k in T){ T[k] += me.unmakeTally[k]; S_[k] += me.unmakeTally[k]; }
    digest.push([side, fid, sd, m.winner ? (m.winner === me ? 1 : 0) : -1, steps]);
  }
  P.tickUnmake = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.resolveHit = oResolve;
  P.step = oStep; P.tickStatus = oStatus;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  if (S6P) P.tickUnmaking = oUnmk;
  const w = AC.WEAPONS.find(x => x.id === "spellbreaker"), u = w.ult;
  const blk = { charge: u.charge, dur: u.dur, stunMul: u.stunMul, hexExtra: u.hexExtra, kind: u.kind,
                dmg: u.dmg, apply: u.apply, blade: w.dmg };
  return { n, bad, T, TS, digest, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, u: blk, secs: (Date.now() - t0) / 1000,
           s6v: S6V, s6p: S6P };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickUnmake === 'function'"):
        raise SystemExit("no tickUnmake in this build -- not an Unmaking link (stage 2+)")
    U0 = page.evaluate(BLOCK)
    # THE STAGE: pinned by --stage, else inferred from the blade (not the shipped 8.81: stage 5) and, at the
    # shipped blade only, from hexExtra. What the probe EXPECTS then comes from the stage and the builder.
    if a.stage:
        stage, how = a.stage, "pinned by --stage"
    elif U0["blade"] != float(SB.SHIPPED_DMG):
        stage, how = "5", f"inferred: blade {U0['blade']} is not the shipped {SB.SHIPPED_DMG}"
    else:
        stage, how = ("2" if U0.get("hexExtra") == 0 else "3"), f"inferred at the shipped blade from hexExtra {U0.get('hexExtra')}"
    want_extra = 0 if stage == "2" else SB.ULT["hexExtra"]
    seeds = [a.seed0 + a.seedstep * i for i in range(a.seeds)]
    foes = [f for f in a.foes.split(",") if f]
    R = page.evaluate(JS, [seeds, foes, [0, 1] if a.sides == "AB" else [0], want_extra, a.drawn])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
fights = R["fights"]
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
def runs(tag):
    k = n.get(f"runN_{tag}", 0)
    if not k:
        return f"{tag}: none"
    return (f"{tag}: {n[f'runL_{tag}']/k:.4f}s mean over {k} clean runs "
            f"({n[f'runMin_{tag}']:.4f}..{n[f'runMax_{tag}']:.4f})")
print(f"\nUNMAKING PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {fights} fights "
      f"(Spellbreaker {'both sides' if a.sides == 'AB' else 'side A'} x {len(foes) or 'every'} foe(s) x {a.seeds} seeds, "
      f"seed0 {a.seed0} step {a.seedstep})   ult {U}")
print(f"  STAGE {stage} ({how}): expects hexExtra {want_extra}, blade "
      f"{SB.SHIPPED_DMG if stage != '5' else ' / '.join((SB.BLADE, SB.ALTROW_BLADE, SB.ALT50_BLADE))}")
print(f"  casts/fight {T['casts']/fights:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Spellbreaker win {R['win']:.1%}")
live_ratio = n.get("hexAppliedInLive", 0) / max(1, n.get("blowsInLive", 0))
print(f"  per cast (the lab's columns): unmade (blows in the window) {T['blows']/casts:.2f}   hex (the second hex) {T['extra']/casts:.2f}"
      f"   hex applied by her blows in windows on a live body / those blows {live_ratio:.3f} ({n.get('blowsInLive',0)} blows)"
      f"   killing blows in windows {n.get('blowsInKill',0)} (hex {n.get('hexAppliedKill',0)})   ({n.get('blowOnShadeIn',0)} blows on a shade)")
print(f"  the foe on a window frame: hex stacks {T['foeHex']/max(1,T['frames']):.2f}   its weapon stunned "
      f"{100*n.get('foeStunIn',0)/max(1,n.get('foeWeapIn',0)):.1f}% of window frames "
      f"(outside windows {100*n.get('foeStunOut',0)/max(1,n.get('foeWeapOut',0)):.1f}%)")
print(f"  hex procs: on the foe in windows at x2 {n.get('proc_in_x2',0)} ({n.get('proc_in_x2',0)/casts:.2f} a cast), "
      f"in windows at x1 {n.get('proc_in_x1',0)} (the cast's own step, before the recompute), outside {n.get('proc_out_x1',0)}; "
      f"on Spellbreaker {n.get('proc_me_x1',0)} (x2: {n.get('proc_me_x2',0)}); on shades {sum(v for k, v in n.items() if k.startswith('proc_shade'))}")
print(f"  the cadence: {n.get('cadenceOk',0)} tickStatus calls rebuilt (c0 + dt x stacks, a proc and 0 at {1.15}), "
      f"{n.get('cadenceProc_in',0)} procs on the foe in windows, {n.get('cadenceProc_out',0)} outside; "
      f"hex clock unmoved between tickStatus calls {n.get('hcContOk',0)} times")
print(f"  REALISED STUN (window clock): {runs('in_x2')}   |   {runs('out_x1')}   |   {runs('me_x1')}")
print(f"    runs cut by another proc {n.get('runCut',0)}, dirtied by another stun {n.get('runDirty',0)}, procs onto a running stun {n.get('procOnStun',0)}")
print(f"  the field: foe x2 on {n.get('fieldFoeInOk',0)} ticker frames, foe x1 {n.get('fieldFoeOutOk',0)}, Spellbreaker x1 {n.get('fieldMeOk',0)}, "
      f"shades x1 {n.get('fieldShadeOk',0)}")
print(f"  nothing else: {n.get('tickWorldOk',0)} tickUnmake calls moved no field beyond the three; the second-hex insert bracketed "
      f"{n.get('insertInOk',0)} times in a window and {n.get('insertOutOk',0)} outside (open-ended {n.get('insertOpenEnded',0)}, "
      f"never read {n.get('insertUnread',0)}); {n.get('castOk',0)} casts moved nothing beyond the prologue and the window")
print(f"  the window's clock: tickUnmake asked once on {n.get('tickStepOk',0)} unfrozen steps (none on a frozen one), "
      f"{n.get('frames',0)} open-window frames; clock closes {n.get('clockCloses',0)}, death closes {n.get('deathCloses',0)}")
print(f"  FREEZE CENSUS {100*frozen:.1f}% of window steps frozen   a clock window lasts "
      f"{n.get('winMT',0)/max(1,n.get('winMTn',0)):.2f}s of match time ({U['dur']}s on the window clock)")
for i, sd in ((0, "A"), (1, "B")):
    s_ = R["TS"][i]
    if not s_["fights"]:
        continue
    print(f"  SIDE {sd} ({s_['fights']} fights): win {s_['wins']/max(1,s_['decided']):.1%}   casts/fight {s_['casts']/s_['fights']:.2f}   "
          f"blows in windows a cast {s_['blows']/max(1,s_['casts']):.2f} (a fight {s_['bin']/s_['fights']:.2f})   second hex a cast {s_['extra']/max(1,s_['casts']):.2f}   "
          f"foe hex on a window frame {s_['foeHex']/max(1,s_['frames']):.2f}   foe's weapon stunned "
          f"{100*n.get('foeStunIn'+sd,0)/max(1,n.get('foeWeapIn'+sd,0)):.1f}% of window frames "
          f"({100*n.get('foeStunOut'+sd,0)/max(1,n.get('foeWeapOut'+sd,0)):.1f}% outside)")
# THE DESIGN'S NUMBERS, each held by the check of its own sentence, against the builder's and the STAGE's:
dur_ok = U["dur"] == 8 == SB.ULT["dur"]                                                    # [1]
mul_ok = U["stunMul"] == 2 == SB.ULT["stunMul"]                                            # [3]
extra_ok = U["hexExtra"] == want_extra and SB.ULT["hexExtra"] == 1                         # [4]
ratio_ok = n.get("blowsInLive", 0) > 0 and n.get("hexAppliedInLive", 0) == (1 + want_extra) * n.get("blowsInLive", 0)
blades = {float(SB.SHIPPED_DMG)} if stage != "5" else {float(SB.BLADE), float(SB.ALTROW_BLADE), float(SB.ALT50_BLADE)}
block_ok = (U["kind"] == "unmake" and U["charge"] == 14 == SB.ULT["charge"] and U.get("dmg") is None
            and U.get("apply") is None and U["blade"] in blades)                           # [6]
for k, ok_, msg in ((1, dur_ok, f"dur {U['dur']}, the design's is 8"),
                    (3, mul_ok, f"stunMul {U['stunMul']}, the design's is 2"),
                    (4, extra_ok, f"hexExtra {U['hexExtra']}, stage {stage}'s is {want_extra}"),
                    (4, ratio_ok or not n.get("blowsInLive", 0),
                     f"hex applied by her blows on a live body in windows {n.get('hexAppliedInLive', 0)} over "
                     f"{n.get('blowsInLive', 0)} blows = {live_ratio:.4f}, stage {stage}'s is {1 + want_extra}"),
                    (6, block_ok, f"the ult block {U} is not the design's / stage {stage}'s")):
    if not ok_:
        bad.setdefault(str(k), []).append(msg)
        n[f"x{k}"] = n.get(f"x{k}", 0) + 1
FLOOR = 200
inx2 = n.get("runN_in_x2", 0)
outx1 = n.get("runN_out_x1", 0)
gate = (inx2 >= FLOOR and outx1 >= FLOOR
        and abs(n["runL_in_x2"] / inx2 - 0.40) <= 0.01 and abs(n["runL_out_x1"] / outx1 - 0.20) <= 0.01)
print(f"  THE BRIEF'S STUN GATE (0.40 +- 0.01 inside, 0.20 outside, at least {FLOOR} clean runs each): {'MET' if gate else 'NOT MET'}")
checks = [
    (1, "the window: dur 8 on the window clock (tickUnmake once on every unfrozen step, never on a frozen one; dt a call), closes on its clock or either death; only Spellbreaker's",
        n.get("clockCloses", 0) > 0 and n.get("deathCloses", 0) > 0 and n.get("frames", 0) > 0 and n.get("tickStepOk", 0) > 0),
    (2, "every hex proc: stunFor x the fighter's own hexStunMul, both reads; x2 on the foe in windows, x1 outside; the engine's cadence, rebuilt every call; realised 0.40 / 0.20 +- 0.01 over >= 200 runs each",
        n.get("proc_in_x2", 0) > 0 and n.get("proc_out_x1", 0) > 0 and n.get("proc_me_x1", 0) > 0 and gate
        and n.get("cadenceProc_in", 0) > 0 and n.get("cadenceProc_out", 0) > 0),
    (3, "the field: the OTHER fighter's stunMul (the design's 2) while its window is open, else 1, recomputed on every ticker frame for both (Spellbreaker's own 1: a runic foe's hexes untouched); shades 1; moved nowhere else",
        all(n.get(k, 0) > 0 for k in ("fieldFoeInOk", "fieldFoeOutOk", "fieldMeOk", "freshOk"))),
    (4, f"every blow: the channel's hex 1, then in the window on a live body hex {want_extra} (stage {stage}) by side letter on the body struck -- {1 + want_extra} hex a blow, exactly; the killing blow the channel's alone; stacks and clock the engine's; the blade's own damage, in and out",
        all(n.get(k, 0) > 0 for k in ("chanInOk", "chanOutOk", "blowInOk", "blowOutOk", "blowsInLive"))),
    (5, "nothing else: every own field of both fighters, every shade and the match unmoved by the ticker but its three, and by the second-hex insert but her tally and the audited hex; the hex clock moves only in tickStatus; no hurt, beat, rng or shot",
        n.get("calls", 0) > 0 and n.get("tickWorldOk", 0) > 0 and n.get("insertInOk", 0) > 0 and n.get("insertOutOk", 0) > 0
        and n.get("hcContOk", 0) > 0),
    (6, "the bolt is out: a cast spawns no shot, hurts or applies nothing, moves nothing beyond the prologue and opens {t 0, dur}, never on an open window; the block (kind, charge 14, no dmg / apply) and the stage's blade",
        n.get("castOk", 0) > 0),
]
g = lambda k: n.get(k, 0)
x2procs = sum(v for k, v in n.items() if k.startswith("proc_") and not k.endswith("_x1"))
if R["s6v"]:
    stunv = sum(v for k, v in n.items() if k.startswith("stunVoiceOk_"))
    quiet = sum(v for k, v in n.items() if k.startswith("procQuietOk_"))
    print(f"  stage 6 voices: {g('castVoiceOk')} casts each one cast voice (of {T['casts']}); {stunv} hex procs at x2 each one "
          f"stun voice (of {x2procs}: {', '.join(k[12:] + ' ' + str(v) for k, v in sorted(n.items()) if k.startswith('stunVoiceOk_'))}), "
          f"{quiet} procs at x1 silent ({', '.join(k[12:] + ' ' + str(v) for k, v in sorted(n.items()) if k.startswith('procQuietOk_'))}); "
          f"closes: {g('closeVoiceOk')} by the clock voiced (of {g('clockCloses')}), {g('closeDeathQuiet')} by a death silent; "
          f"silent through 2 s of the verdict: {g('verdictQuietOpen')} fights with the window open, {g('verdictQuiet')} with it shut; "
          f"the run's own: {g('v_spellbreaker')} cast voices, {g('v_spellbreaker-stun')} stun voices, {g('v_spellbreaker-close')} close voices")
    checks.append((7, "stage 6 voices: one cast voice a cast (in fireUlt); one stun voice for each hex proc at more than x1 "
                      "(the proc's own factor), none at x1, on any body; the close voice on a clock close with both alive "
                      "and never on a death; none in the picture, a drawn frame or the verdict; every one accounted for",
                   g("castVoiceOk") == T["casts"] > 0 and g("v_spellbreaker") == T["casts"]
                   and stunv == x2procs > 0 and g("v_spellbreaker-stun") == stunv and quiet > 0
                   and g("closeVoiceOk") == g("clockCloses") > 0 and g("v_spellbreaker-close") == g("closeVoiceOk")
                   and g("closeDeathQuiet") > 0 and g("verdictQuiet") + g("verdictQuietOpen") > 0))
if R["s6p"]:
    print(f"  stage 6 picture: tickUnmaking {g('unmkCalls')} calls, {g('unmkClean')} writing nothing of the simulation's, "
          f"drawing no RNG, playing nothing and leaving the tags where they were; fresh matches {g('picFreshOk')} fighters clean; "
          f"the script up on {g('scriptWriting') + g('scriptUpOk')} calls in an open window ({g('picCasts')} casts; "
          f"{g('scriptWriting')} of them writing, the first 0.3 s), its clock exact; closes {g('picCloseClock')} by the clock, "
          f"{g('picCloseDeath')} on Spellbreaker's death, {g('picCloseFoeDeath')} on the foe's, "
          f"{g('picCloseOver') + g('picCloseOverOpen')} at `over` ({g('picCloseOverOpen')} with the sim's window still open), "
          f"{g('scriptGoneOk')} out in 0.4 of its clock (0.2 s; {g('scriptUnwriting')} calls unwriting); motes: {g('motesBorn')} "
          f"born at the rebuilt rate, {g('moteOnBlade')} checked on her blades, {g('motesOutlive')} calls with motes alive after a "
          f"close; tags: {g('tagOk')} second hexes' HEX tags relabelled +{1 + want_extra}, {g('tagFirstKept')} teaching panels "
          f"kept, {g('secondHexNoTag')} second hexes with no tag; the grey: {g('greyStart')} starts at an x2 proc "
          f"({g('greyStartNoStun')} whose stun was already 0), on {g('greyOn')} calls (+{g('greyOnStop')} in a hit stop), off "
          f"{g('greyOffOk')}, {g('greyNoneOnX1')} calls after an x1 proc with no grey; after 2 s of the verdict the picture gone "
          f"in {g('endGoneOk') + g('endGoneUp') + g('endGoneOpen')} fights, {g('endGoneUp') + g('endGoneOpen')} of them up at "
          f"`over` ({g('endGoneOpen')} with the sim's window still open); {g('greyAtVerdict')} fights ending with a doubled stun "
          f"(its grey frozen with it)")
    checks.append((8, "stage 6 picture: tickUnmaking writes nothing of the simulation's, draws no RNG, plays nothing; the "
                      "script up while the window is open and a 0.2 s unwrite at any close; motes only in a window, at the "
                      "rebuilt rate, off her blades; HEX +2 on exactly the second hexes' tags; the grey rebuilt from the "
                      "sim's own procs; gone after the verdict"
                      + ("; the drawn subset clean" if g("drawnFights") else ""),
                   g("unmkCalls") > 0 and g("unmkClean") == g("unmkCalls") and g("scriptUpOk") > 0 and g("scriptWriting") > 0
                   and g("picCloseClock") > 0 and g("scriptGoneOk") > 0 and g("motesBorn") > 0 and g("moteOnBlade") > 0
                   and g("tagOk") > 0 and g("greyStart") > 0 and g("greyOn") > 0 and g("greyNoneOnX1") > 0
                   and g("endGoneUp") + g("endGoneOpen") > 0 and g("picFreshOk") > 0
                   and (g("drawOk") > 0 if g("drawnFights") else True)))
if g("drawnFights"):
    print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 60th "
          f"otherwise): {g('drawOk')} frames clean, {g('drawPic')} with the picture up ({g('drawPicStop')} in a hit stop, "
          f"{g('drawGrey')} with a weapon greyed), {g('drawVerdict')} in the verdict")
    if not R["s6p"]:
        checks.append((8, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                          "the simulation", g("drawOk") > 0))
if not (R["s6v"] or R["s6p"]):
    print("  stage 6: not on this link (no stun arm in the synth, no tickUnmaking) -- [7]-[8] not run")
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}   ({R['secs']:.0f}s in the page)")
if a.json:
    R["stage"], R["stageHow"], R["wantExtra"] = stage, how, want_extra
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
