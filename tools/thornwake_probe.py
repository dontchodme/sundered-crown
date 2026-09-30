#!/usr/bin/env python
"""BRAMBLESNARE'S PROBE -- one check per sentence of v84 §1 / §4 / §5, read INSIDE the hooks.

    python thornwake_probe.py --game <link> --stage 2|3|5|6 [--drawn N]

Wraps `step`, `tickBramble`, `plantBramble`, `resolveHit`, `tickCharge`,
`fireUlt`, `move` and `tickHits` on the Match prototype and reads each event
where it happens. Runs Thornwake against every other relic, both sides, and
prints N/N. EVERY NUMBER IS PINNED BY THE STAGE, from the builder
(`thornwake_build`), never read off the link under test: the window, the
charge, the bramble's radius and life, the thorns' cadence, entangle and bite;
the snare (0 at stage 2, the builder's from stage 3); the blade (the shipped
31.35 at stages 2 and 3, the builder's `BLADE` at stage 5, the final). A link
that lost a number fails the check that reads it, and [8] reads the row itself.

"NOTHING ELSE" IS GENERIC, not a list of fields: around every `plantBramble`
call, and around every `tickBramble` call on which the probe's own geometry
expects a snare or a bite, every call that closes a window and every 16th live
call, every own field of both fighters and of every shade (the shared weapon
row included, to depth 4) and every field of the match is snapshotted, and
only the fields the sentence writes may differ. A call on which a bite breaks
a ward is left to the ward: `shatter` bursts the pool at Thornwake, flings it,
draws the RNG for its sparks and stops the world, as every ward break does
(counted, and the foe must still not move).

The checks read the ENGINE's own answers where one sentence feeds another, so
each fails alone: [3] rebuilds the brambles and the foe's INSIDE from the
geometry; [4] and [5] take INSIDE from the engine (`brambleIn`) and check what
follows from it.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "for a duration": the window not `dur` on the window clock -- a
      `tickBramble` call on a frozen step (a hit stop, the latch, the split
      hold, the verdict), not exactly one on every unfrozen step, `t` not
      advancing by dt a call, a clock window not exactly as many calls as the
      clock takes to reach `dur` -- a window outliving either death, or any
      relic but Thornwake carrying `ultBramble`
  [2] "every blow the scythe lands leaves a bramble on the floor where it
      landed": a blow Thornwake lands inside its window that does not plant
      exactly one bramble {x, y} = the struck ball's centre, t0 = the
      brambles' clock, side = the caster's; a bramble from a blow outside the
      window; a bramble from anything but `plantBramble`; a bramble on any
      side but Thornwake's
  [3] "a patch r 80 ... life 6s ... outlives the window; the hall's close does
      not clip it": the brambles after a tick not exactly those whose age on
      the brambles' clock is under `patchLife` (none moved, none removed
      early, none kept late); the thorns not tested exactly while the window
      is open or one of the caster's brambles lives; INSIDE not exactly "the
      foe alive and its centre within patchR + R of one of the caster's
      brambles"
  [4] "an enemy that steps into a bramble is snared -- rooted for a moment
      (ball and weapon)": on an ENTRY (inside now, not on the last tested
      frame) at rootFor > 0, the foe's pin not max(pin, rootFor), pinMax
      likewise, pinV not captured iff no longer hold stood, or pinFree
      touched; a pin write on any other frame, or at all at rootFor 0; a
      ball the snare holds (pin > 0, pinFree 0) moved by move(), landing a
      blow, or entering its hit loop with its weapon free (stun 0)
  [5] "while it stays in one it is entangled and bitten by the thorns" (§4:
      "entangle +1 and hurt 2 every 0.5s inside"): the cooldown not run down
      by dt on every tested frame; a bite not exactly when inside with the
      cooldown clear; a bite that is not exactly entangle +tickEnt by side
      letter, then hurt(foe, tickDmg, Thornwake) once, the cooldown then
      `tickCd`; any other application or hurt from the thorns
  [6] "no knock, no hit stop, no beat" and nothing else: a blow of
      Thornwake's whose damage is not the blade x dmgMul x jitter x dmgTaken,
      rounded, crit included -- rebuilt from the captured draws, in the window
      and out; `plantBramble` or `tickBramble` drawing the RNG, moving the
      foe, stopping the world, or changing any field of either fighter, a
      shade or the match but the sentence's own (a ward the bite breaks
      aside)
  [7] a bite that kills without exactly one fatal hit beat at the foe
      (`bramble: true`); a beat from any other bite or frame of the thorns
  [8] "the charge (the lab's 16 on the game's clock), the window 8": a cast
      not on the frame the live charge clock reaches the builder's charge, or
      a cast while a window is open; the row's charge, window, radius, life,
      cadence, entangle, bite, snare or blade not the pinned stage's

STAGE 6 (the picture and the voice, the builder's readings 17-22), each check
run only where the link carries it -- the voices detected by the crackle's arm
(`thornwake-crackle`) in `AC.SFX.play.toString()`, the picture by `tickBrier`
on the Match -- so the same probe still gates stages 2-5 at 8/8, every line as
before. `--stage 6` pins stage 5's numbers and demands both. Once a fight is
over the probe steps 2 s more of the verdict (the step's `over` path: only the
presentation clock runs) for these two checks alone; [1]-[8] read none of
those steps.
  [9] THE VOICES fire exactly on their events and nowhere else (v84 §4's
      sound). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Bramblesnare's four voices ("ult" with w "thornwake",
      "thornwake-crackle", "thornwake-snare", "thornwake-bite") are read; a
      ward's shatter -- which plays its own crit HIT voice inside hurt() -- is
      not one of them, nor is any other relic's cast. Evidence: a Thornwake
      cast playing anything but exactly one cast voice inside fireUlt, or the
      cast voice anywhere else; a plantBramble call whose voices are not
      exactly one crackle; a tickBramble call whose voices are not EXACTLY the
      snares it wrote and the bites it bit, in the order it did them (a snare,
      then its bite); a Thornwake voice no design names; any of them in the
      picture's hook, a drawn frame, the verdict, another relic's cast or any
      other part of a step. THERE IS NO CLOSE VOICE: a window closing BY ITS
      CLOCK or BY A DEATH must play nothing beyond that call's snares and
      bites (each seen, or NOT EXERCISED). Every voice of the run is accounted
      for: cast voices = casts, crackles = brambles planted, snare voices =
      snares, bite voices = bites (a killing bite's among them).
 [10] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickBrier`
      (tickPresentation: through hit stops, twice a normal step, and in the
      verdict) is wrapped: evidence is any change across it to either fighter
      or a shade (every own number, flag and string but its `brier*` fields,
      every array's length, every status, the pin's velocity, the window, the
      tally) or to the match (every own number, flag and string, every array's
      length, every bramble, every shot) -- and, on every 8th busy call and
      every call where the tally's snares or bites rose, a whole-state
      snapshot to depth 4 (the one [6] uses) with only `brier*`, the tags and
      the teaching flags left out -- an RNG draw or a voice. THE TAGS: the old
      ones kept in order (the oldest may go: statusTag keeps ten), each
      unchanged but an ENTANGLE tag's count; new ones ENTANGLE tags only; the
      teaching flag only entangle's, only turned on. And the picture as
      declared (reading 20), REBUILT: the blade's green 1 exactly while the
      window is open (the match live, the caster alive) and 1 - t/0.6 of the
      presentation clock after it; the caster's picture records exactly the
      simulation's brambles of its side, by identity; the foe carrying none of
      the caster's picture; `brierHeld` (the one picture field another method
      reads) only on a ball a Bramblesnare snare pinned and only while its pin
      holds, and on at the first picture call after the snare; everything the
      picture shows gone after 2 s of the verdict; every field at rest in a
      fresh Match.
  --drawn N (default 0 = off): on the FIRST seed, both sides, every foe, each
      fight is also drawn through the renderer (`AC.__draw`, the post chain
      off, 270x480) every Nth step while the picture shows and every 60th
      otherwise, through the kill and the verdict. [10] fails a drawn frame
      that throws, draws the match's RNG, changes the simulation (the
      per-call snapshot above) or a tag, or plays a Thornwake voice. It runs
      on any link, so the base's draws are its control.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import thornwake_build as TB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--stage", required=True, choices=["2", "3", "5", "6"],
                help="the stage the link is: 2 the brambles, 3 the snare, 5 the blade (the final), "
                     "6 the picture and the voice (stage 5's numbers)")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=113001)
ap.add_argument("--json", default=None)
ap.add_argument("--drawn", type=int, default=0, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()

JS = r"""([seeds, PIN, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const TW = "thornwake";
  const oStep = P.step, oTick = P.tickBramble, oPlant = P.plantBramble, oResolve = P.resolveHit,
        oCharge = P.tickCharge, oFire = P.fireUlt, oMove = P.move, oHits = P.tickHits;
  const isTW = (m, f) => f && f.w && f.w.id === TW && (f === m.a || f === m.b);
  const opp = (m, f) => f === m.a ? m.b : m.a;
  /* THE WINDOW'S LENGTH ON THE WINDOW CLOCK: the calls it takes the clock,
     accumulated as the engine accumulates it, to reach `dur`. */
  let wantCalls = 0; { let t = 0; while (!(t >= PIN.dur)) { t += DT; wantCalls++; } }
  let per = null;                         // this fight's counters
  let tickCalls = 0, plantCalls = 0, castNow = 0, removedNow = 0;
  const winCalls = new WeakMap();         // window record -> calls so far
  const born = new WeakMap();             // bramble -> tick calls it has lived
  const heldBy = new Set(), pendingHeld = new Set();   // balls a snare holds (from the step after it)
  /* A ball snared THIS step: `tickStasis` ran before the snare, so its weapon
     lock starts next step (the lab's timing too: it pinned after the whole
     step). A re-snare on a ball whose old hold ran out on this very step is
     the same case. */
  const snaredNow = new Set();

  /* "NOTHING ELSE", GENERIC: every own field of both fighters and of every
     shade (the shared weapon row included) and every field of the match, to
     depth 4, as [path, json] pairs. `drop` names the fields the sentence
     writes. A long array on the match is its length and its last two entries. */
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
  const snapAll = (m, drop) => {
    const out = [];
    const bodies = [["A", m.a], ["B", m.b]].concat((m.shades || []).map((s, i) => ["S" + i, s]));
    for (const [lab, g] of bodies){
      for (const k of Object.keys(g).sort()){
        let v = g[k];
        if (drop(g, k)) continue;
        if (k === "status" && v && drop(g, "status.entangle")){ v = Object.assign({}, v); delete v.entangle; }
        out.push([lab + "." + k, JSON.stringify(ser(m, v, 1, new Set()))]);
      }
    }
    for (const k of Object.keys(m).sort()){
      const v = m[k];
      if (k === "rng" || k === "shades" || isF(m, v) || drop(m, k)) continue;
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

  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: the crackle's arm in the synth [9], `tickBrier` on the
     match [10]. A link without them runs [1]-[8] only. ---- */
  const S6V = /thornwake-crackle/.test(AC.SFX.play.toString()), S6P = typeof P.tickBrier === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play"), oBrier = P.tickBrier;
  const OURS = { "thornwake": "Thornwake's fireUlt", "thornwake-crackle": "plantBramble",
                 "thornwake-snare": "tickBramble", "thornwake-bite": "tickBramble" };
  const isOurs = (kind, q) => kind === "ult" && !!q && typeof q.w === "string" && q.w.startsWith("thornwake");
  const oursIn = rec => rec.filter(c => isOurs(c[0], c[1])).map(c => c[1].w);
  let vctx = "a step", vrec = null, tail = false;
  if (S6V) AC.SFX.play = function(kind, q){
    if (vrec) vrec.push([kind, q ? Object.assign({}, q) : q]);
    if (isOurs(kind, q)){
      inc("v_" + q.w);
      if (!Object.prototype.hasOwnProperty.call(OURS, q.w)) fail(9, `a Thornwake voice no design names: ${q.w}`);
      else if (vctx !== OURS[q.w]) fail(9, `the ${q.w} voice played in ${vctx}`);
    }
    return oPlay.call(this, kind, q);
  };
  /* [10] the simulation's state, as one array in a fixed key order: both fighters' and every shade's own
     numbers, flags and strings (their `brier*` fields aside) and array lengths, statuses, the pin's
     velocity, the window and the tally; the match's own numbers, flags and strings and every array's
     length (the tags read apart), every bramble and every shot. */
  const same = (x, y) => x === y || (x !== x && y !== y);
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b, ...(m.shades || [])]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 98 && k.startsWith("brier")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      if (f.status) for (const k in f.status){ const st = f.status[k]; o.push(k, st && typeof st === "object" ? st.stacks : st, st && typeof st === "object" ? st.t : 0); }
      if (Array.isArray(f.pinV)) o.push("pinV", f.pinV[0], f.pinV[1]);
      const Z = f.ultBramble; if (Z) o.push("Z", Z.t, Z.dur); else o.push("Z-");
      const T = f.brambleTally; if (T) for (const k of Object.keys(T)) o.push(k, T[k]); else o.push("T-");
    }
    for (const k of Object.keys(m)){
      if (k === "tags") continue;
      const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    for (const b of m.brambles) o.push(b.x, b.y, b.t0, b.side);
    for (const sh of (m.shots || [])) o.push(sh.x, sh.y, sh.vx, sh.vy, sh.life);
    return o;
  };
  const firstDiff = (s0, s1) => {
    if (s0.length !== s1.length) return `the shape ${s0.length} -> ${s1.length} fields`;
    for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i]))
      return `${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}`;
    return null; };
  let PMod = null;                       // [10] the green, rebuilt: per fight { off, ever }
  const snared = new Set(), pendSnare = new Set();   // [10] balls a Bramblesnare snare pinned; not yet seen by the picture
  let brierN = 0;

  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [9]-[10] alone */
    if (tail) return oStep.call(this, dt);
    const frozen = this.over || !!this.latch || !!this.splitHold || this.hitStop > 0;
    const c0 = tickCalls, p0 = plantCalls, nb0 = this.brambles.length;
    removedNow = 0;
    snaredNow.clear();
    for (const f of [this.a, this.b]) if (isTW(this, f) && f.ultBramble){ per.winSteps++; if (frozen) per.winFrozen++; }
    const r = oStep.call(this, dt);
    const calls = tickCalls - c0;
    if (frozen){ if (calls) fail(1, `tickBramble ran ${calls}x on a frozen step`); else inc("frozenOk"); }
    else if (calls !== 1) fail(1, `tickBramble ran ${calls}x on an unfrozen step`); else inc("liveOk");
    /* [2] NOTHING BUT plantBramble ADDS A BRAMBLE */
    if (this.brambles.length !== nb0 - removedNow + (plantCalls - p0))
      fail(2, `the brambles went ${nb0} -> ${this.brambles.length} with ${plantCalls - p0} plant(s) and ${removedNow} expiry(ies)`);
    for (const q of pendingHeld) heldBy.add(q);
    pendingHeld.clear();
    for (const q of [...heldBy]) if (!(q.pin > 0) || !q.alive) heldBy.delete(q);
    for (const q of [...snared]) if (!(q.pin > 0) || !q.alive) snared.delete(q);
    return r;
  };

  P.tickBramble = function(dt){
    tickCalls++;
    const G0 = this.brambles.slice(), G0v = G0.map(b => [b.x, b.y, b.t0, b.side]), T0 = this.brambleT, T1 = T0 + dt;
    const survive = G0.filter(b => !(T1 - b.t0 >= PIN.patchLife));
    const pre = [];
    let expect = false;
    for (const f of [this.a, this.b]){
      if (f.ultBramble && !isTW(this, f)) fail(1, `${f.w.id} carries ultBramble`);
      const foe = opp(this, f), side = f === this.a ? "a" : "b";
      if (!isTW(this, f)){ if (G0.some(b => b.side === side)) fail(2, `${f.w.id}'s side carries a bramble`); continue; }
      const Z = f.ultBramble;
      const closing = !!Z && (Z.t + dt >= PIN.dur || !f.alive || !foe.alive);
      const openAfter = !!Z && !closing;
      const tested = openAfter || survive.some(b => b.side === side);
      const inGeo = tested && foe.alive && survive.some(b => b.side === side && Math.hypot(foe.x - b.x, foe.y - b.y) < PIN.patchR + R);
      const p = { f, foe, side, Z, t1: Z ? Z.t + dt : null, closing, openAfter, tested, inGeo,
                  fAlive: f.alive, foeAlive: foe.alive, cd: f.brambleCd, wasIn: f.brambleIn,
                  T: f.brambleTally ? Object.assign({}, f.brambleTally) : null,
                  fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy, pin: foe.pin, pinMax: foe.pinMax, pinV: foe.pinV,
                  pinFree: foe.pinFree, hp: foe.hp, shield: foe.shield, cx: f.x, cy: f.y, cvx: f.vx, cvy: f.vy };
      if (closing || (inGeo && (!p.wasIn || p.cd - dt <= 0))) expect = true;
      pre.push(p);
    }
    const live = pre.some(p => p.tested || p.Z);
    const watch = expect || (live && tickCalls % 16 === 0);
    const hs0 = this.hitStop;
    const s0 = watch ? snapAll(this, () => false) : null;
    /* THE CALL, with every hurt, application, beat and RNG draw inside it recorded */
    const hurts = [], applies = [], beats = [], seq = [];
    let shattered = 0, drew = 0, r;
    const oHurt = this.hurt, oBeat = this.beat, oR = this.rng, oMR = Math.random;
    this.hurt = function(t, d, s){ const sh = t.shield; hurts.push([t, d, s]); seq.push("hurt"); const q = oHurt.call(this, t, d, s); if (sh > 0 && t.shield <= 0) shattered++; return q; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    const wrapped = [];
    for (const g of [this.a, this.b]){ const o = g.apply; g.apply = function(k, nn, src){ applies.push([g, k, nn, src]); seq.push("apply"); return o.call(this, k, nn, src); }; wrapped.push(g); }
    const vc0 = vctx, vr0 = vrec; vctx = "tickBramble"; vrec = [];
    let heardTick = null;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oR; Math.random = oMR; for (const g of wrapped) delete g.apply;
              heardTick = vrec; vctx = vc0; vrec = vr0; }
    const wantV = [];                     /* [9] the voices this call owes: its snares, then its bites, a caster at a time */
    let closeClock = 0, closeDeath = 0, killV = 0;
    if (shattered) inc("wardBreaks", shattered);

    /* [3] THE BRAMBLES: exactly the survivors, unmoved, in order, on their clock */
    if (this.brambleT !== T1) fail(3, `brambleT ${T0} -> ${this.brambleT}, want ${T1}`);
    const G1 = this.brambles;
    removedNow += G0.length - G1.length;      /* the ticker's own count; [2] reads the step's, [3] which ones */
    if (G1.length !== survive.length || G1.some((b, i) => b !== survive[i])) fail(3, `the brambles after the tick: ${G1.length}, want ${survive.length} survivors of ${G0.length}`);
    else {
      let moved = false;
      for (let i = 0; i < G0.length; i++){ const b = G0[i], v = G0v[i]; if (b.x !== v[0] || b.y !== v[1] || b.t0 !== v[2] || b.side !== v[3]) moved = true; }
      if (moved) fail(3, "a bramble moved"); else inc("survOk");
      for (const b of G0){
        const k = (born.get(b) || 0) + 1;
        if (survive.includes(b)) born.set(b, k);
        else { inc("expired"); n.lifeMin = Math.min(n.lifeMin ?? 1e9, k - 1); n.lifeMax = Math.max(n.lifeMax ?? 0, k - 1); }
      }
    }

    for (const p of pre){
      const { f, foe, side } = p, T = f.brambleTally;
      /* [1] THE WINDOW */
      if (p.Z){
        const k = (winCalls.get(p.Z) || 0) + 1; winCalls.set(p.Z, k);
        if (p.closing){
          if (f.ultBramble){ fail(1, "the window did not close"); }
          else if (p.fAlive && p.foeAlive){
            if (k !== wantCalls) fail(1, `a clock window of ${k} calls, want ${wantCalls}`); else inc("clockClose");
          } else inc("deathClose");
        } else if (f.ultBramble !== p.Z) fail(1, `closed at ${p.t1.toFixed(4)} of ${PIN.dur}`);
        else if (p.Z.t !== p.t1) fail(1, `t ${p.Z.t}, want ${p.t1}`);
        else inc("winOk");
      } else if (f.ultBramble) fail(1, "a window opened inside the thorns' tick");
      /* [3] WHEN THE THORNS ARE TESTED, AND INSIDE */
      const dTested = T ? T.tested - (p.T ? p.T.tested : 0) : 0;
      if (dTested !== (p.tested ? 1 : 0)) fail(3, `tested ${dTested}, want ${p.tested ? 1 : 0} (window open ${p.openAfter})`);
      /* [4] and [5] read the ENGINE's answers -- whether it tested (the tally) and INSIDE (brambleIn) -- so a
         broken bramble list or test fails [3] and only [3] */
      const engTested = dTested === 1;
      const engIn = engTested ? f.brambleIn : false;
      if (p.tested){
        if (f.brambleIn !== p.inGeo) fail(3, `inside ${f.brambleIn}, the geometry says ${p.inGeo}`);
        else { inc("insideOk"); if (p.inGeo) inc("insideYes"); if (p.inGeo && !p.openAfter) inc("afterIn"); }
      } else if (f.brambleIn !== p.wasIn) fail(3, "brambleIn written on an untested frame");
      /* [4] THE SNARE ON ENTRY, per the engine's own inside */
      const entry = engTested && engIn === true && !p.wasIn;
      const dEnt = T ? T.entries - (p.T ? p.T.entries : 0) : 0;
      if (dEnt !== (entry ? 1 : 0)) fail(4, `${dEnt} entries counted, want ${entry ? 1 : 0}`);
      const dSn = T ? T.snares - (p.T ? p.T.snares : 0) : 0;
      const dTk0 = T ? T.ticks - (p.T ? p.T.ticks : 0) : 0;
      for (let i = 0; i < dSn; i++) wantV.push("thornwake-snare");
      for (let i = 0; i < dTk0; i++) wantV.push("thornwake-bite");
      if (p.closing){ if (p.fAlive && p.foeAlive) closeClock++; else closeDeath++; }
      if (dTk0 && p.hp > 0 && foe.hp <= 0) killV++;
      if (dSn > 0 && foe.pin > 0 && !foe.pinFree && foe.alive){ snared.add(foe); pendSnare.add(foe); }
      if (entry && PIN.rootFor > 0){
        const hold = PIN.rootFor;
        if (dSn !== 1) fail(4, `an entry counted ${dSn} snares`);
        else if (foe.pin !== Math.max(p.pin, hold) || foe.pinMax !== Math.max(p.pinMax, hold)) fail(4, `pin ${p.pin} -> ${foe.pin}, pinMax ${p.pinMax} -> ${foe.pinMax}, want ${Math.max(p.pin, hold)}`);
        else if (!(p.pin > hold) && (!foe.pinV || foe.pinV === p.pinV || foe.pinV[0] !== p.fvx || foe.pinV[1] !== p.fvy)) fail(4, `pinV ${JSON.stringify(foe.pinV)}, want a fresh [${p.fvx}, ${p.fvy}]`);
        else if ((p.pin > hold) && foe.pinV !== p.pinV) fail(4, "pinV recaptured under a longer hold");
        else if (foe.pinFree !== p.pinFree) fail(4, `the snare wrote pinFree ${p.pinFree} -> ${foe.pinFree}`);
        else { inc("snareOk"); if (p.pin > 0) inc("resnare"); if (p.pin > hold) inc("longerHold"); if (!p.openAfter) inc("snareAfter"); }
        if (foe.pin > 0 && !foe.pinFree){ pendingHeld.add(foe); snaredNow.add(foe); }
      } else {
        if (dSn) fail(4, `${dSn} snare(s) with ${entry ? "rootFor 0" : "no entry"}`);
        if (foe.pin !== p.pin || foe.pinMax !== p.pinMax || foe.pinV !== p.pinV) fail(4, `the pin moved with no snare (entry ${entry}, rootFor ${PIN.rootFor})`);
        else if (entry) inc("noSnareOk");
      }
      /* [5] THE THORNS: the cooldown, the bite, its order and its terms, per the engine's own inside */
      const cdRun = p.cd - dt;
      const bite = engTested && engIn === true && cdRun <= 0;
      const dTk = T ? T.ticks - (p.T ? p.T.ticks : 0) : 0;
      const mine = applies.filter(x => x[0] === foe), hs = hurts.filter(h => h[0] === foe);
      if (!engTested){ if (f.brambleCd !== p.cd) fail(5, `the cooldown moved on an untested frame (${p.cd} -> ${f.brambleCd})`); }
      else if (bite){ if (f.brambleCd !== PIN.tickCd) fail(5, `the cooldown ${f.brambleCd} after a bite, want ${PIN.tickCd}`); }
      else if (f.brambleCd !== cdRun) fail(5, `the cooldown ${p.cd} -> ${f.brambleCd}, want ${cdRun}`);
      if (bite){
        if (dTk !== 1) fail(5, `a bite counted ${dTk} ticks`);
        else if (mine.length !== 1 || mine[0][1] !== "entangle" || mine[0][2] !== PIN.tickEnt) fail(5, `applications ${JSON.stringify(mine.map(x => [x[1], x[2]]))}, want [["entangle", ${PIN.tickEnt}]]`);
        else if (mine[0][3] !== side) fail(5, `the entangle's source ${typeof mine[0][3] === "object" ? "a Fighter" : JSON.stringify(mine[0][3])}, want "${side}"`);
        else if (hs.length !== 1 || hs[0][1] !== PIN.tickDmg || hs[0][2] !== f) fail(5, `hurt ${JSON.stringify(hs.map(h => h[1]))} from ${hs.length && hs[0][2] === f ? "the caster" : "?"}, want [${PIN.tickDmg}] from the caster`);
        else if (JSON.stringify(seq.filter(x => x === "apply" || x === "hurt").slice(0, 2)) !== '["apply","hurt"]') fail(5, `the order ${JSON.stringify(seq)}, want entangle then the bite`);
        else if (Math.abs((p.hp + p.shield) - (foe.hp + foe.shield) - PIN.tickDmg) > 1e-9) fail(5, `the bite took ${(p.hp + p.shield) - (foe.hp + foe.shield)}, want ${PIN.tickDmg}`);
        else { inc("tickOk"); if (!p.openAfter) inc("tickAfter"); if (!p.fAlive) inc("deadCasterBite"); }
      } else if (dTk || mine.length || hs.length) fail(5, `${dTk} tick(s), ${mine.length} application(s), ${hs.length} hurt(s) with no bite due`);
      if (applies.some(x => x[0] !== foe) || hurts.some(h => h[0] !== foe)) fail(5, "the thorns touched a body that is not the opponent");
      /* [7] A KILLING BITE FILES ONE FATAL BEAT; NOTHING ELSE FILES ONE */
      const killed = bite && p.hp > 0 && foe.hp <= 0;
      const fb = beats.filter(b => b.kind === "hit" && b.fatal === true && b.bramble === true);
      if (killed){
        if (beats.length !== 1 || fb.length !== 1) fail(7, `a killing bite filed ${beats.length} beat(s), ${fb.length} fatal`);
        else if (fb[0].x !== foe.x || fb[0].y !== foe.y || fb[0].side !== (f === this.a ? 0 : 1) || fb[0].dmg !== PIN.tickDmg) fail(7, "the fatal beat is not at the foe, from the caster, for the bite");
        else inc("fatalTick");
      } else if (beats.length) fail(7, `a thorns' frame with no kill filed ${beats.length} beat(s)`);
      /* [6] NO KNOCK, NO HIT STOP: the foe does not move (a ward's shatter flings the CASTER) */
      if (foe.x !== p.fx || foe.y !== p.fy || foe.vx !== p.fvx || foe.vy !== p.fvy) fail(6, "the thorns moved the foe");
      if (!shattered && (f.x !== p.cx || f.y !== p.cy || f.vx !== p.cvx || f.vy !== p.cvy)) fail(6, "the thorns moved the caster");
    }
    if (S6V){
      const o = oursIn(heardTick);
      if (JSON.stringify(o) !== JSON.stringify(wantV)) fail(9, `tickBramble played ${JSON.stringify(o)}, its snares and bites want ${JSON.stringify(wantV)}`);
      else {
        inc("tickVoiceOk");
        if (closeClock) inc("clockCloseSilent", closeClock);
        if (closeDeath) inc("deathCloseSilent", closeDeath);
        if (killV) inc("killBiteVoiced", killV);
        if (wantV.length > 1 && wantV[0] === "thornwake-snare" && wantV.includes("thornwake-bite")) inc("snareThenBite");
      }
    }
    if (!shattered){
      if (this.hitStop !== hs0) fail(6, `the hit stop ${hs0} -> ${this.hitStop} with no ward broken`);
      if (drew) fail(6, `tickBramble drew the RNG ${drew}x with no ward broken`);
    }
    /* [6] NOTHING ELSE, around the watched calls: only the sentence's own fields */
    if (watch && !shattered){
      const lab = (g) => g === this.a ? "A" : g === this.b ? "B" : "?";
      const bit = pre.some(p => p.f.brambleTally && p.T && p.f.brambleTally.ticks !== p.T.ticks);
      const sn = pre.some(p => p.f.brambleTally && p.T && p.f.brambleTally.snares !== p.T.snares);
      const dropP = new Set(["m.brambles", "m.brambleT"]), entP = new Set();
      if (bit) dropP.add("m.floats");            // hurt()'s own float when a ward absorbs the bite
      if (beats.length) dropP.add("m.beats");    // [7]'s
      for (const p of pre){
        const L = lab(p.f), Fo = lab(p.foe);
        for (const k of ["ultBramble", "brambleCd", "brambleIn", "brambleTally"]) dropP.add(L + "." + k);
        dropP.add(Fo + ".pinFree");              // [4]'s sentence
        if (sn) for (const k of ["pin", "pinMax", "pinV"]) dropP.add(Fo + "." + k);
        if (bit){ dropP.add(Fo + ".hp"); dropP.add(Fo + ".shield"); entP.add(Fo + ".status"); }
      }
      const filt = (snap) => snap.filter(x => !dropP.has(x[0])).map(x => {
        if (!entP.has(x[0])) return x;
        const o = JSON.parse(x[1]); if (o && typeof o === "object") delete o.entangle;
        return [x[0], JSON.stringify(o)];
      });
      const dd = diffSnap(filt(s0), filt(snapAll(this, () => false)));
      if (dd) fail(6, "tickBramble changed " + dd); else inc("tickClean");
    }
    return r;
  };

  /* THE PLANT: nothing but one bramble more and the tally's `planted`, and no RNG */
  P.plantBramble = function(f, q){
    plantCalls++;
    const drop = (g, k) => (g === this && k === "brambles") || (g === f && k === "brambleTally");
    const s0 = snapAll(this, drop), oR = this.rng, oMR = Math.random, nb = this.brambles.length, pl0 = f.brambleTally.planted;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    const vc0 = vctx, vr0 = vrec; vctx = "plantBramble"; vrec = [];
    let heard = null;
    try { r = oPlant.call(this, f, q); }
    finally { this.rng = oR; Math.random = oMR; heard = vrec; vctx = vc0; vrec = vr0; }
    if (S6V){ const o = oursIn(heard); if (o.length !== 1 || o[0] !== "thornwake-crackle") fail(9, `plantBramble played ${JSON.stringify(o)}, want exactly ["thornwake-crackle"]`); else inc("crackleOk"); }
    if (drew) fail(6, `plantBramble drew the RNG ${drew}x`);
    const dd = diffSnap(s0, snapAll(this, drop));
    if (dd) fail(6, "plantBramble changed " + dd);
    else if (this.brambles.length !== nb + 1 || f.brambleTally.planted !== pl0 + 1) fail(6, "plantBramble did not add exactly one bramble and one count");
    else inc("plantClean");
    return r;
  };
  P.fireUlt = function(f, foe){
    if (isTW(this, f)){
      castNow++;
      if (f.ultBramble) fail(8, "a cast while the window is open"); else inc("castOk");
      per.casts++;
    }
    const vc0 = vctx, vr0 = vrec; vctx = isTW(this, f) ? "Thornwake's fireUlt" : "another relic's cast"; vrec = [];
    let r, heard = null;
    try { r = oFire.call(this, f, foe); } finally { heard = vrec; vctx = vc0; vrec = vr0; }
    if (S6V && isTW(this, f)){ const o = oursIn(heard); if (o.length !== 1 || o[0] !== "thornwake") fail(9, `a cast played ${JSON.stringify(o)}, want exactly ["thornwake"]`); else inc("castVoiceOk"); }
    if (!isTW(this, f) && f.ultBramble) fail(1, `${f.w.id}'s cast opened a bramble window`);
    if (isTW(this, f) && (!f.ultBramble || f.ultBramble.t !== 0 || f.ultBramble.dur !== PIN.dur || f.brambleCd !== 0))
      fail(1, "the cast did not open a fresh window with the thorns' cooldown clear");
    return r;
  };
  P.tickCharge = function(f, foe, dt){
    if (!isTW(this, f)) return oCharge.call(this, f, foe, dt);
    const c0 = f.charge, live = f.alive && !this.over, k0 = castNow;
    const r = oCharge.call(this, f, foe, dt);
    const cast = castNow - k0;
    if (live){
      const c1 = c0 + dt;
      if (c1 >= PIN.charge){ if (cast !== 1 || f.charge !== 0) fail(8, `the clock at ${c1.toFixed(4)} of ${PIN.charge}: ${cast} cast(s)`); else inc("chargeOk"); }
      else if (cast || f.charge !== c1) fail(8, `a cast at ${c1.toFixed(4)} of ${PIN.charge}`);
    } else if (cast) fail(8, "a cast from a dead caster or a finished match");
    return r;
  };
  P.move = function(f, foe, dt){
    if (!heldBy.has(f) || !(f.pin > 0) || f.pinFree) return oMove.call(this, f, foe, dt);
    const x0 = f.x, y0 = f.y;
    const r = oMove.call(this, f, foe, dt);
    if (f.x !== x0 || f.y !== y0) fail(4, `a snared ${f.w.id} moved`); else inc("heldStill");
    return r;
  };
  P.tickHits = function(self, foe, dt, cool){
    if (!heldBy.has(self) || !(self.pin > 0) || self.pinFree) return oHits.call(this, self, foe, dt, cool);
    /* the snare's own step: the lock and the stillness of the weapon begin next step (tickStasis's timing) */
    if (snaredNow.has(self)){ inc("lockNextStep"); return oHits.call(this, self, foe, dt, cool); }
    if (!(self.stun > 0)) fail(4, `a snared ${self.w.id} with its weapon free (stun ${self.stun}, pin ${self.pin})`);
    const h0 = self.hits;
    const r = oHits.call(this, self, foe, dt, cool);
    if (self.hits !== h0) fail(4, `a snared ${self.w.id} landed a blow`); else inc("heldQuiet");
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isTW(this, self) || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const q = opp(this, self), open = !!self.ultBramble;
    const h0 = self.hits, d0 = self.dealt, c0 = self.crits, pc0 = plantCalls, nb0 = this.brambles.length;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis, curse: foe.stacks("curse"),
                  x: foe.x, y: foe.y, T: this.brambleT };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; }
    const landed = self.hits - h0 === 1;
    const pc = plantCalls - pc0;
    if (!landed){ if (pc) fail(2, "a bramble from a call that landed no blow"); return r; }
    /* [6] THE BLOW IS THE SCYTHE'S OWN */
    if (open) per.bin++; else per.bout++;
    const crit = self.crits > c0, D = self.dealt - d0;
    const raw = self.w.dmg * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis || pre.curse) inc("blowExempt"); else fail(6, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want}`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    /* [2] A BLOW IN THE WINDOW PLANTS ONE BRAMBLE WHERE IT LANDED; NONE OUTSIDE */
    if (open){
      const b = this.brambles[this.brambles.length - 1];
      if (pc !== 1 || this.brambles.length !== nb0 + 1) fail(2, `a blow in the window planted ${pc}x (${nb0} -> ${this.brambles.length})`);
      else if (b.x !== pre.x || b.y !== pre.y || b.t0 !== pre.T || b.side !== (self === this.a ? "a" : "b")) fail(2, `the bramble ${JSON.stringify(b)} is not {x ${pre.x}, y ${pre.y}, t0 ${pre.T}} at the struck ball`);
      else { inc("plantOk"); if (foe !== q) inc("shadePlant"); }
    } else if (pc || this.brambles.length !== nb0) fail(2, "a bramble from a blow outside the window");
    else inc("outNoPlant");
    return r;
  };

  /* [10] THE PICTURE'S HOOK: `tickBrier`, on the presentation clock (tickPresentation: through hit
     stops, twice a normal step, and in the verdict). */
  if (S6P) P.tickBrier = function(dt){
    inc("brierCalls"); brierN++;
    const s0 = simSnap(this), tg0 = this.tags.slice(), tj0 = tg0.map(g => [g.val, JSON.stringify(Object.assign({}, g, { val: 0 }))]);
    const taught0 = JSON.stringify(this.taught);
    const busy = [this.a, this.b].some(q => q.brambleTally || q.brierGreen > 0 || q.brierPic.length || q.brierRootFade > 0);
    const rose = [this.a, this.b].some(q => q.brambleTally && (q.brambleTally.snares !== q.brierSeen[0] || q.brambleTally.ticks !== q.brierSeen[1]));
    const deep = busy && (rose || brierN % 8 === 0);
    const dropB = (g, k) => (typeof k === "string" && k.startsWith("brier")) || (g === this && (k === "tags" || k === "taught"));
    const d0 = deep ? snapAll(this, dropB) : null;
    let draws = 0; const oR = this.rng, oMR = Math.random;
    this.rng = function(){ draws++; return oR.apply(this, arguments); };
    Math.random = function(){ draws++; return oMR(); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture"; vrec = [];
    let r, heard = null;
    try { r = oBrier.call(this, dt); } finally { this.rng = oR; Math.random = oMR; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = firstDiff(s0, simSnap(this));
    const dd = deep ? diffSnap(d0, snapAll(this, dropB)) : null;
    if (d) fail(10, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (dd) fail(10, `the picture wrote the simulation (whole state): ${dd}`);
    else if (draws) fail(10, `the picture drew the RNG ${draws}x`);
    else if (heard.length) fail(10, `the picture played ${JSON.stringify(heard.map(h => [h[0], h[1] && h[1].w]))}`);
    else { inc("brierClean"); if (deep) inc("brierDeep"); if (busy && this.hitStop > 0) inc("brierInStop"); if (this.over) inc("brierVerdict"); }
    /* THE TAGS: the old ones kept in order (the oldest may go), each unchanged but an ENTANGLE tag's count;
       new ones ENTANGLE tags only; the teaching flag only entangle's, only on */
    const T1 = this.tags, kept = tg0.filter(g => T1.includes(g)), gone = tg0.length - kept.length;
    const added = T1.filter(g => !tg0.includes(g));
    if (!(T1.slice(0, kept.length).every((g, i) => g === kept[i]) && kept.every((g, i) => g === tg0[gone + i])) || gone > added.length)
      fail(10, "the picture removed or moved a tag");
    else if (added.some(g => g.key !== "entangle")) fail(10, `the picture pushed a ${added.find(g => g.key !== "entangle").key} tag`);
    else {
      for (let i = 0; i < tg0.length; i++){
        const g = tg0[i]; if (!T1.includes(g)) continue;
        if (tj0[i][1] !== JSON.stringify(Object.assign({}, g, { val: 0 }))) fail(10, `the picture changed a ${g.key} tag beyond its count`);
        else if (g.val !== tj0[i][0]){ if (g.key !== "entangle") fail(10, `the picture relabelled a ${g.key} tag`); else inc("tagCounted"); }
      }
      if (added.length) inc("tagPushed", added.length);
    }
    const taught1 = JSON.stringify(this.taught);
    if (taught1 !== taught0){
      const t0 = JSON.parse(taught0), t1 = this.taught, ks = Object.keys(t1).filter(k => t1[k] !== t0[k]).concat(Object.keys(t0).filter(k => !(k in t1)));
      if (ks.length !== 1 || ks[0] !== "entangle" || t1.entangle !== true) fail(10, `the picture changed the teaching flags ${JSON.stringify(ks)}`);
      else inc("taughtEntangle");
    }
    if (!PMod) return r;
    for (const g of [this.a, this.b]){
      if (!isTW(this, g)){
        if (g.brierGreen !== 0 || g.brierPic.length || g.brierBite.length || g.brierAge !== 0 || g.brierOut !== 0 || g.brierEnd !== 0)
          fail(10, `${g.w.id}, which is not Thornwake, carries the caster's picture`);
        continue;
      }
      /* THE GREEN: 1 while the window is open (the match live, the caster alive); after it 1 - t/0.6 */
      const Z = (this.over || !g.alive) ? null : g.ultBramble;
      if (Z){ PMod.off = 0; PMod.ever = true; }
      else if (PMod.ever) PMod.off += dt;
      const want = Z ? 1 : PMod.ever ? Math.max(0, 1 - PMod.off / 0.6) : 0;
      if (Math.abs(g.brierGreen - want) > 1e-9)
        fail(10, `the blade's green ${g.brierGreen}, want ${want} (${Z ? "the window open" : PMod.ever ? PMod.off.toFixed(4) + " of the clock since the close" : "before the first cast"})`);
      else inc(Z ? "greenOn" : want > 0 ? "greenFading" : "greenOff");
      /* THE BRAMBLES: the picture's records are exactly the simulation's of this side, by identity */
      const side = g === this.a ? "a" : "b", mine = this.brambles.filter(b => b.side === side), pic = g.brierPic.map(q => q.b);
      if (pic.length !== mine.length || mine.some(b => !pic.includes(b))) fail(10, `the picture shows ${pic.length} brambles, the simulation has ${mine.length}`);
      else if (mine.length) inc("picMirrorOk");
    }
    /* THE HELD BALL: brierHeld only on a ball a Bramblesnare snare pinned and only while its pin holds;
       on at the first picture call after the snare */
    for (const g of [this.a, this.b]){
      if (g.brierHeld && !(g.pin > 0 && g.alive && snared.has(g)))
        fail(10, `${g.w.id} carries brierHeld with ${!(g.pin > 0) ? "no pin" : !g.alive ? "no life" : "no Bramblesnare snare"}`);
      if (pendSnare.has(g)){
        pendSnare.delete(g);
        if (g.pin > 0 && g.alive && !g.pinFree){ if (g.brierHeld !== 1) fail(10, `a snared ${g.w.id} with brierHeld ${g.brierHeld}`); else inc("heldOn"); }
      }
      if (g.brierHeld) inc("heldCalls");
    }
    return r;
  };

  /* THE DRAWN SUBSET [10]: a frame through the renderer, the simulation read before and after */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.brierGreen > 0 || (q.brierPic && q.brierPic.length) || q.brierRootFade > 0 || (q.brierBite && q.brierBite.length));
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), tg0 = m.tags.map(g => g.val), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "a drawn frame"; vrec = [];
    let threw = null, heard = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = firstDiff(s0, simSnap(m));
    if (threw) fail(10, "a drawn frame threw: " + threw);
    else if (dr) fail(10, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(10, "a drawn frame changed the simulation: " + d);
    else if (m.tags.length !== tg0.length || m.tags.some((g, i) => g.val !== tg0[i])) fail(10, "a drawn frame changed a tag");
    else if (oursIn(heard).length) fail(10, `a drawn frame played ${JSON.stringify(oursIn(heard))}`);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict");
           if ([m.a, m.b].some(q => q.brierHeld > 0)) inc("drawHeld"); }
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== TW);
  const W = AC.WEAPONS.find(w => w.id === TW), row = W.ult;
  const ROWK = ["charge", "dur", "patchR", "patchLife", "tickCd", "tickEnt", "tickDmg", "rootFor"];
  for (const k of ROWK)
    if (row[k] !== PIN[k]) fail(8, `the row's ${k} is ${row[k]}, the stage's ${PIN[k]}`); else inc("rowOk");
  if (row.kind !== "bramble") fail(8, `the row's kind is ${row.kind}`); else inc("rowOk");
  if (W.dmg !== PIN.blade) fail(8, `the blade is ${W.dmg}, the stage's ${PIN.blade}`); else inc("rowOk");
  const S = { fights: 0, wins: 0, decided: 0, casts: 0, bin: 0, bout: 0, winSteps: 0, winFrozen: 0,
              frames: 0, planted: 0, tested: 0, after: 0, foeIn: 0, entries: 0, snares: 0, ticks: 0, dealt: 0, ent: 0, kills: 0 };
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, TW, sd) : new AC.Match(TW, fid, sd);
    const me = side ? m.b : m.a;
    per = { casts: 0, bin: 0, bout: 0, winSteps: 0, winFrozen: 0 };
    heldBy.clear(); pendingHeld.clear();
    snared.clear(); pendSnare.clear(); PMod = S6P ? { off: 0, ever: false } : null;
    if (S6P) for (const g of [m.a, m.b]){
      if (g.brierGreen !== 0 || g.brierAge !== 0 || g.brierOut !== 0 || g.brierEnd !== 0 || !Array.isArray(g.brierPic) || g.brierPic.length
          || JSON.stringify(g.brierSeen) !== "[0,0]" || g.brierTagN !== 0 || g.brierTagT !== 0 || !Array.isArray(g.brierBite) || g.brierBite.length
          || g.brierHeld !== 0 || g.brierRootFade !== 0 || g.brierHeldAge !== 0 || g.brierHeldOut !== 0) fail(10, `a fresh Match's ${g.w.id} carries a picture`);
      else inc("picFreshOk");
    }
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    /* [9]-[10] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
    if ((S6V || S6P) && m.over){
      const o9 = n.x9 || 0;
      tail = true; vctx = "the verdict";
      try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); if (drawn) drawFrame(m, steps + i + 1); } }
      finally { tail = false; vctx = "a step"; }
      if (S6V && (n.x9 || 0) === o9) inc("verdictQuiet");
      if (S6P) for (const g of [m.a, m.b]){
        if (g.brierGreen !== 0 || g.brierRootFade !== 0 || g.brierBite.length || (g.brierPic.length && !(g.brierEnd >= 0.6)))
          fail(10, `after 2 s of the verdict ${g.w.id}'s picture still shows (green ${g.brierGreen}, shoots ${g.brierRootFade}, bites ${g.brierBite.length}, brambles ${g.brierPic.length} at ${g.brierEnd})`);
        else inc("endGoneOk");
      }
    }
    S.fights++;
    if (m.winner){ S.decided++; if (m.winner === me) S.wins++; }
    for (const k in per) S[k] += per[k];
    if (me.brambleTally) for (const k of ["frames", "planted", "tested", "after", "foeIn", "entries", "snares", "ticks", "dealt", "ent", "kills"]) S[k] += me.brambleTally[k];
  }
  P.step = oStep; P.tickBramble = oTick; P.plantBramble = oPlant; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  if (S6P) P.tickBrier = oBrier;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  const u = {}; for (const k of ROWK) u[k] = row[k];
  u.kind = row.kind; u.blade = W.dmg;
  return { n, bad, S, wantCalls, u, S6V, S6P };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickBramble === 'function'"):
        raise SystemExit("no tickBramble in this build -- not a Bramblesnare link (stage 2+)")
    # EVERY NUMBER PINNED BY THE STAGE, from the builder -- never read off the link under test.
    PIN = {k: TB.ULT[k] for k in ("charge", "dur", "patchR", "patchLife", "tickCd", "tickEnt", "tickDmg")}
    PIN["rootFor"] = 0 if a.stage == "2" else TB.ULT["rootFor"]
    PIN["blade"] = float(TB.BLADE if a.stage in ("5", "6") else TB.SHIPPED_DMG)
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN, a.drawn])
    assert not errors, errors

n, bad, S, U = R["n"], R["bad"], R["S"], R["u"]
F = max(1, S["fights"]); casts = max(1, S["casts"])
print(f"\nBRAMBLESNARE PROBE  {pathlib.Path(a.game).name}  stage {a.stage}  Chromium {ver}  {S['fights']} fights "
      f"(Thornwake both sides x every foe x {a.seeds} seeds)")
print(f"  the row {U}")
print(f"  pinned  {PIN}")
print(f"  casts/fight {S['casts']/F:.2f}   blows a fight: in windows {S['bin']/F:.2f}, outside {S['bout']/F:.2f}   "
      f"Thornwake win {S['wins']/max(1,S['decided']):.1%}")
print(f"  per cast (the lab's columns): brambles {S['planted']/casts:.2f}   bites {S['ticks']/casts:.2f}   "
      f"dmg {S['dealt']/casts:.2f}   snares {S['snares']/casts:.2f}   entries {S['entries']/casts:.2f}   "
      f"foe inside {S['foeIn']/casts:.1f} tested frames (live steps)   entangle {S['ent']/casts:.2f}")
print(f"  the brambles outlive the window: {S['after']/casts:.1f} tested frames a cast after the close, "
      f"{n.get('afterIn',0)} of them with the foe inside; bites after the close {n.get('tickAfter',0)} of {n.get('tickOk',0)}, "
      f"snares after {n.get('snareAfter',0)} of {n.get('snareOk',0)}")
print(f"  brambles expired {n.get('expired',0)}, each after {n.get('lifeMin','-')}..{n.get('lifeMax','-')} ticks of the "
      f"brambles' clock   shade blows planting at the shade {n.get('shadePlant',0)}   re-snares on a held ball "
      f"{n.get('resnare',0)} (under a longer hold {n.get('longerHold',0)})   killing bites {n.get('fatalTick',0)}   "
      f"bites from a slain caster's brambles (its kill flight) {n.get('deadCasterBite',0)}   "
      f"wards broken by a bite {n.get('wardBreaks',0)}")
print(f"  held steps still {n.get('heldStill',0)}   held hit loops quiet {n.get('heldQuiet',0)} (re-snared on the step "
      f"the old hold ran out, the weapon locked from the next: {n.get('lockNextStep',0)})   "
      f"FREEZE CENSUS {100*S['winFrozen']/max(1,S['winSteps']):.1f}% of window steps frozen   clock window {R['wantCalls']} calls")
print(f"  nothing else: {n.get('plantClean',0)} plant calls and {n.get('tickClean',0)} ticker calls snapshotted whole "
      f"(both fighters, the shades, the match), clean")
snare_on = PIN["rootFor"] > 0
checks = [
    (1, "the window: dur on the window clock (one tick an unfrozen step, none frozen), closes on either death; only Thornwake's",
        n.get("clockClose", 0) > 0 and n.get("liveOk", 0) > 0 and n.get("frozenOk", 0) > 0 and n.get("winOk", 0) > 0),
    (2, "every blow in the window plants one bramble at the struck ball, on the brambles' clock; none outside; none from anything else",
        n.get("plantOk", 0) > 0 and n.get("outNoPlant", 0) > 0),
    (3, "the brambles live patchLife on their clock, unmoved, and outlive the window; tested while the window or a bramble "
        "lives; inside = the foe's centre within patchR + R",
        n.get("survOk", 0) > 0 and n.get("expired", 0) > 0 and n.get("insideYes", 0) > 0 and n.get("afterIn", 0) > 0),
    (4, "the snare on entry: max(pin, rootFor), pinMax, pinV iff no longer hold, pinFree untouched; nowhere else; the held "
        "ball still and its weapon locked" + ("" if snare_on else "  (rootFor 0 at this stage: entries, no pin)"),
        (n.get("snareOk", 0) > 0 and n.get("heldStill", 0) > 0 and n.get("heldQuiet", 0) > 0) if snare_on
        else n.get("noSnareOk", 0) > 0),
    (5, "the thorns: the cooldown runs on tested frames; inside and clear -> entangle +tickEnt (side letter), then "
        "hurt(foe, tickDmg, Thornwake), the cooldown tickCd; nothing else",
        n.get("tickOk", 0) > 0),                      # bites AFTER the window are [3]'s coverage (afterIn), not [5]'s
    (6, "the blow is the scythe's own (rebuilt exactly, in and out); the plant and the thorns write nothing else, "
        "draw no RNG, move nothing and stop nothing (a ward's own break aside)",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("plantClean", 0) > 0
        and n.get("tickClean", 0) > 0),
    (7, "a killing bite files one fatal hit beat at the foe; no other frame of the thorns files one",
        n.get("fatalTick", 0) > 0),
    (8, "a cast exactly when the live clock reaches the builder's charge, never with a window open; the row (charge, "
        "window, radius, life, cadence, entangle, bite, snare, kind, blade) is the stage's",
        n.get("castOk", 0) > 0 and n.get("chargeOk", 0) > 0 and n.get("rowOk", 0) == 10),
]
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
S6V, S6P = R.get("S6V"), R.get("S6P")
g = lambda k: n.get(k, 0)
if S6V:
    acc = (g("v_thornwake") == S["casts"] and g("v_thornwake-crackle") == S["planted"]
           and g("v_thornwake-snare") == S["snares"] and g("v_thornwake-bite") == S["ticks"])
    print(f"  stage 6 voices: {g('castVoiceOk')} casts each one cast voice (of {S['casts']}); {g('crackleOk')} plants each one "
          f"crackle (of {S['planted']}); {g('tickVoiceOk')} ticker calls voiced exactly their snares and bites -- "
          f"{g('v_thornwake-snare')} snare voices for {S['snares']} snares, {g('v_thornwake-bite')} bite voices for "
          f"{S['ticks']} bites ({g('killBiteVoiced')} killing), a snare then its bite on {g('snareThenBite')} calls; "
          f"closes silent: {g('clockCloseSilent')} by the clock, {g('deathCloseSilent')} by a death; "
          f"{g('verdictQuiet')} verdicts quiet")
    checks.append((9, "stage 6 voices: one cast voice a cast (in fireUlt), one crackle a bramble (in plantBramble), the snares' "
                      "and the bites' voices exactly as tickBramble wrote them, in order; no close voice (clock or death); none "
                      "in the picture, a drawn frame, the verdict or anywhere else; every one accounted for",
                   acc and g("castVoiceOk") > 0 and g("crackleOk") > 0 and g("tickVoiceOk") > 0
                   and g("v_thornwake-snare") > 0 and g("v_thornwake-bite") > 0 and g("killBiteVoiced") > 0
                   and g("clockCloseSilent") > 0 and g("deathCloseSilent") > 0 and g("verdictQuiet") > 0))
if S6P:
    print(f"  stage 6 picture: tickBrier {g('brierCalls')} calls, {g('brierClean')} writing nothing of the simulation's "
          f"({g('brierDeep')} whole-state, {g('brierInStop')} in a hit stop, {g('brierVerdict')} in the verdict); tags pushed "
          f"{g('tagPushed')}, counts updated {g('tagCounted')}, taught {g('taughtEntangle')}; green on {g('greenOn')}, fading "
          f"{g('greenFading')}, off {g('greenOff')}; brambles mirrored {g('picMirrorOk')}; held on at the snare {g('heldOn')} "
          f"(held calls {g('heldCalls')}); gone after the verdict {g('endGoneOk')}; fresh {g('picFreshOk')}")
    checks.append((10, "stage 6 picture: tickBrier writes nothing of the simulation's, draws no RNG, plays nothing, keeps the "
                       "tags' rule; the green, the brambles and the held ball as declared; gone after the verdict"
                       + ("; the drawn subset clean" if g("drawnFights") else ""),
                   g("brierClean") > 0 and g("brierDeep") > 0 and g("greenOn") > 0 and g("greenFading") > 0
                   and g("picMirrorOk") > 0 and g("heldOn") > 0 and g("tagPushed") + g("tagCounted") > 0
                   and g("endGoneOk") > 0 and g("picFreshOk") > 0
                   and ((g("drawOk") > 0 and g("drawPic") > 0) if g("drawnFights") else True)))
if g("drawnFights"):
    print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 60th "
          f"otherwise): {g('drawOk')} frames clean ({g('drawPic')} with the picture up, {g('drawPicStop')} in a hit stop, "
          f"{g('drawHeld')} with a held ball, {g('drawVerdict')} in the verdict)")
    if not S6P:
        checks.append((10, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                           "the simulation", g("drawOk") > 0))
if not (S6V or S6P):
    print("  stage 6: not on this link (no crackle arm in the synth, no tickBrier) -- [9]-[10] not run")
if a.stage == "6" and not (S6V and S6P):
    checks.append((10, "--stage 6 asks for the voices and the picture, and this link lacks "
                       + ("both" if not (S6V or S6P) else "the voices" if not S6V else "the picture"), False))
ok = 0
for k, text, cover in checks[8:]:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
ok += sum(1 for k, text, cover in checks[:8] if n.get(f"x{k}", 0) == 0 and cover)
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
