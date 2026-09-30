#!/usr/bin/env python
"""ROOTFAST'S PROBE -- one check per sentence of v85 §1 / §4 / §5, read INSIDE the hooks.

    python heartwood_probe.py --game <link> --stage 2|3|5|6 [--draw-every 6 | --no-draw]

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
every Heartwood `fireUlt` call, and every 16th `tickRootfast` call with a
window open and every call that closes one, every own field of both fighters
and of every shade (the shared weapon row included, to depth 4) and every
field of the match is snapshotted, and only the fields the sentence writes may
differ -- and those are checked against their exact expected values where the
engine's arithmetic can be rebuilt (the opponent's status after a root, the
cast's window, tally, hit stop, shake, banner, beat and note).

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
  [3] "roots ... for a second": after a blow that rooted (the tally's rooted
      rose; [2] reads whether it SHOULD have) the opponent's pin is not
      max(pin before, rootFor), pinMax likewise, or pinV is not captured iff
      the hold standing was not longer -- and then EXACTLY the vector the ball
      was hit with, the engine's knock rebuilt from the blow's crit ("the
      knock is applied and then frozen by the pin", §4); after a blow that
      rooted nobody, the pin untouched
  [4] "ball and weapon": the root touches pinFree; a living ball the root
      holds (pin > 0, pinFree 0) moved by move(), or landing a blow, or
      entering its hit loop with its weapon free (stun 0)
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
      no stun, no charge, no reach) -- and the opponent's status EXACTLY the
      record before with the root's own apply() calls folded in by
      Fighter.apply's arithmetic (stacks min(cap, s + n) under the cap, the
      clock the status's dur, the source the side letter): WHICH applications
      is [5]'s, so a status written by hand past apply() fails here and only
      here; `tickRootfast` drawing the RNG or changing anything but the window
      record and the tally's frames
  [7] "Charge 15 (on the game's clock) / window 8": a cast not on the frame
      the live charge clock reaches the builder's charge, or a cast while a
      window is open; the row's charge, window, root length, entangle or
      blade not the pinned stage's
  [8] "freeze out" (brief stage 1) and "No damage change" at the cast: the
      row's ult block carrying any key but {name, charge, kind, dur, rootFor,
      extraEnt, tip} (the freeze's radius / dmg / apply / freeze back in), its
      name, kind or card not the design's; a Heartwood `fireUlt` drawing the
      RNG, or changing any field of either fighter, a shade or the match but
      the caster's ultsFired (+1), ultRoot (EXACTLY {t: 0, dur}) and rootTally
      (casts +1, or made at 1 with every counter 0) and the generic cast's
      presentation (hitStop max'd to 0.08, shake 32, the banner "Rootfast" on
      Heartwood, one "ult" beat, one note, the ultFx record of kind
      "rootfast") -- so the cast hurts, stuns, pins, entangles and moves
      nobody
  STAGE 6 (the picture and the voice, sc-heartwood-b11-fx; v112 §6). Each check
  runs on a link that carries its half, read off the page itself, and `--stage
  6` REQUIRES both (a stage-6 link without them fails as "not on this link"):
  [9] THE VOICE (on when "heartwood-root" is in AC.SFX.play.toString()): a
      Heartwood cast without exactly one `ult` / heartwood voice inside fireUlt
      (and no root voice there); any other relic's cast playing a Heartwood
      voice; a blow that ROOTED (the tally's rooted rose) without exactly one
      voice inside rootBlow, `ult` with opts exactly {w: "heartwood-root"};
      any voice inside rootBlow on a blow that rooted nobody (a killing blow);
      any voice inside tickRootfast -- the design has no close voice, so none
      at a clock close and none at a death; and every Heartwood voice of the
      run accounted for by those events (a voice played anywhere else fails).
      rootBlow hurts nobody, so no ward's shatter (whose own crit hit voice
      plays inside hurt()) can sound inside it: NOTHING else may.
  [10] THE PICTURE (on when the Match has `tickGrove`): `tickGrove`, the
      picture's one hook on the step (tickPresentation), drawing the RNG or
      changing the simulation -- both fighters' bodies, pins, statuses,
      charge, window and tally and the match's clock, every call; and on every
      call that marks a root and every 64th with the picture up, EVERY field of
      both fighters, the shades and the match but the picture's own
      (`grove*`), the held ball's `twine*` markers and a tag's printed count;
      a root on a living ball held without pinFree not marked (twineHeld 1,
      twineRootFade 1, twineHeldOut 0, the shoots' age 0 on a new hold), or a
      ball that holds itself (pinFree) marked; the blow's ENTANGLE tag not
      printing the count the root leaves; `groveFade` not 1 while the window
      stands, or the green outliving its caster; any other relic carrying the
      grove; and on the DRAWN subset (the first seed, both sides, every foe) a
      drawn frame that throws or writes the simulation or the picture's state
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import heartwood_build as HB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--stage", required=True, choices=["2", "3", "5", "6"],
                help="the stage the link is: 2 the root, 3 the entangle, 5 the blade, 6 the picture and the voice (the final)")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=112001)
ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, PIN, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const HW = "heartwood";
  /* THE GENERIC CAST'S PRESENTATION ON THE MATCH ([8] checks each exactly below) */
  const CAST_M = new Set(["banner", "shake", "hitStop", "beats", "events", "ultFx"]);
  const oStep = P.step, oTick = P.tickRootfast, oRoot = P.rootBlow, oResolve = P.resolveHit,
        oCharge = P.tickCharge, oFire = P.fireUlt, oMove = P.move, oHits = P.tickHits;
  /* STAGE 6, read off the page: the voices' arms are in SFX.play, the
     picture's hook is on the Match. SFX.play is a no-op headless (no audio
     context): each call is recorded here before its first line returns, and
     nothing the probe keeps is the page's. */
  const RV = "heartwood-root";
  const stage6v = new RegExp(RV).test(AC.SFX.play.toString());
  const stage6p = typeof P.tickGrove === "function";
  const voices = [], hwAll = {}, oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oGrove = P.tickGrove;
  if (stage6v) AC.SFX.play = function(kind, q){
    voices.push([kind, q === undefined ? "u" : JSON.stringify(q), q && q.w]);
    if (kind === "ult" && q && (q.w === HW || q.w === RV)) hwAll[q.w] = (hwAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  const hwIn = (vs) => vs.filter(v => v[0] === "ult" && (v[2] === HW || v[2] === RV));
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
        /* the opponent's status is checked EXACTLY in the rootBlow wrapper: the record before, with the
           calls to apply() the root made folded in by Fighter.apply's own arithmetic, and nothing else */
        if (mode === "root" && g === q && k === "status") continue;
        /* the cast's own writes on the caster, each checked exactly in the fireUlt wrapper ([8]) */
        if (mode === "cast" && g === f && (k === "ultsFired" || k === "ultRoot" || k === "rootTally")) continue;
        if (k === "rootTally" && v && isHW(m, g)){
          v = Object.assign({}, v);
          if (mode === "root" && g === f){ delete v.blows; delete v.rooted; delete v.roots; delete v.ent; }
          if (mode === "tick") delete v.frames;
        }
        if (mode === "tick" && k === "ultRoot" && isHW(m, g)) continue;
        /* the picture's own fields and the held ball's markers (read by Tendril's root picture only) */
        if (mode === "grove" && /^(grove|twine)/.test(k)) continue;
        out.push([lab + "." + k, JSON.stringify(ser(m, v, 1, new Set()))]);
      }
    }
    for (const k of Object.keys(m).sort()){
      const v = m[k];
      if (k === "rng" || k === "shades" || isF(m, v)) continue;
      if (mode === "cast" && CAST_M.has(k)) continue;
      if (mode === "grove" && k === "tags") continue;     // [10] reads the tags apart: only a count may move
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
    const v0 = voices.length;
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
    /* [9] THE CLOSE IS SILENT (the design has none), and so is every tick */
    const tv = voices.slice(v0);
    if (stage6v && tv.length) fail(9, `tickRootfast played ${tv.map(v => v[2] || v[0]).join(", ")}${closing ? " at a close" : ""}`);
    for (const p of pre){
      const k = (winCalls.get(p.Z) || 0) + 1; winCalls.set(p.Z, k);
      if (stage6v && !tv.length && (p.t1 >= PIN.dur || !p.fAlive || !p.foeAlive))
        inc(p.fAlive && p.foeAlive ? "clockSilent" : "deathSilent");
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
    const st0 = {};
    for (const k of Object.keys(q.status)) st0[k] = q.status[k] && typeof q.status[k] === "object" ? Object.assign({}, q.status[k]) : q.status[k];
    /* the root's calls to apply() on the opponent, captured and passed through (to [5]'s capture
       inside resolveHit when there is one) */
    const calls = [], hadOwn = Object.prototype.hasOwnProperty.call(q, "apply"), prevApply = q.apply;
    q.apply = function(k, nn, src){ calls.push([k, nn, src]); return prevApply.call(this, k, nn, src); };
    let drew = 0, r;
    const v0 = voices.length, rd0 = f.rootTally ? f.rootTally.rooted : 0;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oRoot.call(this, f); }
    finally { this.rng = oR; Math.random = oMR; if (hadOwn) q.apply = prevApply; else delete q.apply; }
    if (drew) fail(6, `rootBlow drew the RNG ${drew}x`);
    /* [9] A ROOT IS VOICED ONCE, INSIDE rootBlow, AND NOTHING ELSE SOUNDS THERE; A KILLING BLOW IS SILENT */
    if (stage6v){
      const rv = voices.slice(v0), rooted1 = (f.rootTally ? f.rootTally.rooted : 0) - rd0;
      if (rooted1 === 1){
        if (rv.length !== 1 || rv[0][0] !== "ult" || rv[0][1] !== JSON.stringify({ w: RV }))
          fail(9, `a root voiced ${JSON.stringify(rv.map(v => [v[0], v[1]]))}, want one ult ${JSON.stringify({ w: RV })}`);
        else inc("rootVoice");
      } else if (rv.length) fail(9, `a blow that rooted nobody (opponent alive ${q.alive}) voiced ${JSON.stringify(rv.map(v => [v[0], v[1]]))}`);
      else inc("killSilent");
    }
    const dd = diffSnap(s0, snapAll(this, "root", q, f));
    if (dd) fail(6, "rootBlow changed " + dd); else inc("rootClean");
    /* THE OPPONENT'S STATUS, EXACTLY: the record before with the root's own apply() calls folded
       in by Fighter.apply's arithmetic (stacks min(cap, s + n) under the cap -- hemorrhage's cap
       the fighter's bleedCap, curse's stacks its pool -- the clock the status's dur, the source if
       given) and nothing else. WHICH applications the root makes is [5]'s sentence; this is "the
       record is what those applications make of it", so a status written by hand fails here. */
    const want = {};
    for (const k of Object.keys(st0)) want[k] = st0[k] && typeof st0[k] === "object" ? Object.assign({}, st0[k]) : st0[k];
    for (const [k, nn, src] of calls){
      const def = AC.STATUS[k];
      if (!def) continue;
      const cur = want[k] || { stacks: 0, t: 0 };
      const cap = k === "hemorrhage" ? q.bleedCap : def.maxStacks;
      if (cur.stacks < cap) cur.stacks = Math.min(cap, cur.stacks + nn);
      cur.t = def.dur;
      if (src) cur.src = src;
      if (k === "curse") cur.stacks = Math.min(def.maxStacks, q.cursePool.length);
      want[k] = cur;
    }
    const j1 = JSON.stringify(ser(this, q.status, 1, new Set())), jW = JSON.stringify(ser(this, want, 1, new Set()));
    if (j1 !== jW) fail(6, `rootBlow changed ${q === this.a ? "A" : "B"}.status beyond its applications: ${JSON.stringify(st0).slice(0, 80)} -> ${j1.slice(0, 80)}, want ${jW.slice(0, 80)}`);
    else { inc("entRecOk"); if (calls.some(c => c[0] === "entangle")) inc("entRecApplied"); }
    return r;
  };
  /* [8] THE CAST RESOLVES NOTHING: snapshotted whole, and each field the generic cast and the
     rootfast branch write checked against its exact value. */
  P.fireUlt = function(f, foe){
    if (!isHW(this, f)){
      const v0 = voices.length, r0 = oFire.call(this, f, foe);
      if (stage6v && hwIn(voices.slice(v0)).length) fail(9, `${f.w.id}'s cast played a Heartwood voice`);
      return r0;
    }
    castNow++;
    if (f.ultRoot) fail(7, "a cast while the window is open"); else inc("castOk");
    per.casts++;
    const s0 = snapAll(this, "cast", foe, f);
    const pre = { fired: f.ultsFired, tally: f.rootTally ? Object.assign({}, f.rootTally) : null,
                  hitStop: this.hitStop, nBeats: this.beats.length, nEvents: this.events.length };
    const oR = this.rng, oMR = Math.random, v0 = voices.length;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oFire.call(this, f, foe); }
    finally { this.rng = oR; Math.random = oMR; }
    /* [9] THE CAST'S OWN VOICE: fireUlt's prologue plays `w: f.w.id`, now Heartwood's arm */
    if (stage6v){
      const cv = voices.slice(v0), n1 = cv.filter(v => v[0] === "ult" && v[2] === HW).length, n2 = cv.filter(v => v[2] === RV).length;
      if (n1 !== 1 || n2) fail(9, `a cast voiced ${n1} cast voice(s) and ${n2} root voice(s)`); else inc("castVoice");
    }
    const u = f.w.ult, side = f === this.a ? 0 : 1, why = [];
    if (drew) why.push(`drew the RNG ${drew}x`);
    const dd = diffSnap(s0, snapAll(this, "cast", foe, f));
    if (dd) why.push("changed " + dd);
    if (f.ultsFired !== pre.fired + 1) why.push(`ultsFired ${pre.fired} -> ${f.ultsFired}`);
    if (JSON.stringify(ser(this, f.ultRoot, 1, new Set())) !== JSON.stringify({ dur: PIN.dur, t: 0 }))
      why.push(`ultRoot ${JSON.stringify(f.ultRoot)}, want {t: 0, dur: ${PIN.dur}}`);
    const tWant = pre.tally ? Object.assign({}, pre.tally, { casts: pre.tally.casts + 1 })
                            : { casts: 1, frames: 0, blows: 0, rooted: 0, roots: 0, ent: 0 };
    if (JSON.stringify(ser(this, f.rootTally, 1, new Set())) !== JSON.stringify(ser(this, tWant, 1, new Set())))
      why.push(`rootTally ${JSON.stringify(f.rootTally)}, want ${JSON.stringify(tWant)}`);
    if (this.hitStop !== Math.max(pre.hitStop, 0.08)) why.push(`hitStop ${pre.hitStop} -> ${this.hitStop}, want the cast's 0.08`);
    if (this.shake !== 32) why.push(`shake ${this.shake}`);
    const b = this.banner;
    if (!b || b.text !== u.name || b.w !== HW || b.bx !== f.x || b.by !== f.y)
      why.push(`banner ${JSON.stringify(b && { text: b.text, w: b.w })}`);
    const lb = this.beats[this.beats.length - 1];
    const grew = this.beats.length === pre.nBeats + 1 || (pre.nBeats >= 600 && this.beats.length === pre.nBeats);
    if (!grew || !lb || lb.kind !== "ult" || lb.w !== HW || lb.side !== side)
      why.push(`the cast beat ${JSON.stringify(lb && { kind: lb.kind, w: lb.w, side: lb.side })} (${pre.nBeats} -> ${this.beats.length})`);
    const le = this.events[this.events.length - 1];
    if (this.events.length !== pre.nEvents + 1 || !le || le.text !== `${f.w.name} — ${u.name}`)
      why.push(`the cast note (${pre.nEvents} -> ${this.events.length})`);
    const X = this.ultFx;
    if (!X || X.w !== HW || X.kind !== "rootfast" || X.hit !== true)
      why.push(`ultFx ${JSON.stringify(X && { w: X.w, kind: X.kind, hit: X.hit })}`);
    if (why.length) fail(8, "the cast " + why.join("; ")); else inc("castClean");
    return r;
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
  /* [4] reads the LIVING balls a root holds: a dead ball's weapon decides nothing, and a root
     on a dead ball is [2]'s sentence ("a killing blow roots nobody"). */
  P.move = function(f, foe, dt){
    if (!heldBy.has(f) || !(f.pin > 0) || f.pinFree || !f.alive) return oMove.call(this, f, foe, dt);
    const x0 = f.x, y0 = f.y;
    const r = oMove.call(this, f, foe, dt);
    if (f.x !== x0 || f.y !== y0) fail(4, `a held ${f.w.id} moved`); else inc("heldStill");
    return r;
  };
  P.tickHits = function(self, foe, dt, cool){
    if (!heldBy.has(self) || !(self.pin > 0) || self.pinFree || !self.alive) return oHits.call(this, self, foe, dt, cool);
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
    /* [3] and [5] read the blows that ROOTED (the tally's rooted rose by one); whether a blow
       SHOULD have rooted -- in the window, on a living opponent -- is [2]'s. */
    const rooted = dr === 1;
    if (rooted){
      const hold = PIN.rootFor;
      if (q.pin !== Math.max(pre.pin, hold) || q.pinMax !== Math.max(pre.pinMax, hold)) fail(3, `pin ${pre.pin} -> ${q.pin}, pinMax ${pre.pinMax} -> ${q.pinMax}, want ${Math.max(pre.pin, hold)}`);
      else if (!(pre.pin > hold) && (!q.pinV || q.pinV[0] !== vxK || q.pinV[1] !== vyK)) fail(3, `pinV ${JSON.stringify(q.pinV)}, want the knocked [${vxK}, ${vyK}]`);
      else if ((pre.pin > hold) && q.pinV !== pre.pinV) fail(3, "pinV recaptured under a longer hold");
      else { inc("pinOk"); if (pre.pin > 0) inc("rerootOk"); if (pre.pin > hold) inc("longerHold"); }
      if (q.pinFree !== pre.pinFree) fail(4, `the root wrote pinFree ${pre.pinFree} -> ${q.pinFree}`); else inc("pinFreeOk");
      if (q.pin > 0 && !q.pinFree && q.alive) heldBy.add(q);
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

  /* [10] THE PICTURE'S HOOK. The sim, cheap, on every call: both fighters'
     bodies, pins, statuses, charge, window and tally, the shades, the match's
     clock. The whole state (snapAll "grove": everything but the picture's own
     fields and the markers; the tags apart, only a count may move) on every
     call that marks a root and every 64th with the picture up. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "theta", "charge", "stun", "pin", "pinMax", "pinFree",
              "reachMul", "hits", "dealt", "crits", "ultsFired", "spinDir", "burden", "alive"];
  const simSnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(f.pinV ? [f.pinV[0], f.pinV[1]] : null);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t, f.status[k].src]));
      o.push(f.ultRoot ? [f.ultRoot.t, f.ultRoot.dur] : null, f.rootTally ? JSON.stringify(f.rootTally) : null);
    }
    for (const s of (m.shades || [])) o.push([s.x, s.y, s.hp]);
    return JSON.stringify(o);
  };
  const picSnap = (m) => JSON.stringify([m.a, m.b].map(f => Object.keys(f).filter(k => /^(grove|twine)/.test(k)).sort()
                                         .map(k => [k, ser(m, f[k], 1, new Set())])));
  const tagSnap = (m) => JSON.stringify((m.tags || []).map(g => { const o = {}; for (const k of Object.keys(g).sort()) if (k !== "val") o[k] = g[k]; return o; }));
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return s0.slice(Math.max(0, i - 40), i + 40) + " -> " + s1.slice(Math.max(0, i - 40), i + 40); };
  const seenRooted = new WeakMap(), seenRoots = new WeakMap();
  let groveCalls = 0;
  if (stage6p) P.tickGrove = function(dt){
    groveCalls++;
    const marks = [];
    for (const f of [this.a, this.b]){
      if (!isHW(this, f) || !f.rootTally) continue;
      const T = f.rootTally, sr = seenRooted.get(f) || 0, so = seenRoots.get(f) || 0;
      if (T.rooted !== sr){ marks.push({ f, foe: opp(this, f), hold: T.roots !== so }); seenRooted.set(f, T.rooted); seenRoots.set(f, T.roots); }
    }
    const up = [this.a, this.b].some(q => q.groveFade > 0 || q.groveMotes.length || q.groveBits.length);
    const whole = marks.length > 0 || (up && groveCalls % 64 === 0);
    const c0 = simSnap(this), g0 = whole ? snapAll(this, "grove") : null, t0 = whole ? tagSnap(this) : null;
    const oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oGrove.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(10, `tickGrove drew the RNG ${drew}x`);
    const c1 = simSnap(this);
    if (c1 !== c0) fail(10, "tickGrove changed the sim: " + firstDiff(c0, c1));
    else if (whole){
      const dd = diffSnap(g0, snapAll(this, "grove"));
      if (dd) fail(10, "tickGrove changed " + dd);
      else if (tagSnap(this) !== t0) fail(10, "tickGrove changed a tag beyond its printed count");
      else inc("groveWhole");
    } else inc("groveOk");
    /* THE ROOT, MARKED FOR TENDRIL'S PICTURE, AND THE TAG'S COUNT */
    for (const { f, foe, hold } of marks){
      if (!(foe.alive && foe.pin > 0)) continue;
      if (foe.pinFree){ if (foe.twineHeld) fail(10, "a ball that holds itself (pinFree) marked as rooted"); else inc("selfHeld"); }
      else if (foe.twineHeld !== 1 || foe.twineRootFade !== 1 || foe.twineHeldOut !== 0 || (hold && foe.twineHeldAge !== 0))
        fail(10, `a root not marked: twineHeld ${foe.twineHeld}, fade ${foe.twineRootFade}, out ${foe.twineHeldOut}, age ${foe.twineHeldAge} (new hold ${hold})`);
      else inc(hold ? "markHold" : "markReroot");
      const R0 = C.physics.ballR, nE = foe.stacks("entangle");
      for (let i = this.tags.length - 1; i >= 0; i--){
        const g = this.tags[i];
        if (g.key !== "entangle" || g.max - g.life > 0.1 || Math.hypot(g.x - foe.x, g.y - foe.y) >= R0 * 3) continue;
        if (g.first) inc("tagFirst"); else if (g.val !== nE) fail(10, `the ENTANGLE tag prints ${g.val}, the foe carries ${nE}`); else inc("tagOk");
        break;
      }
    }
    for (const f of [this.a, this.b]){
      if (!isHW(this, f)){ if (f.groveFade > 0 || f.groveMotes.length || f.groveBits.length) fail(10, `${f.w.id} carries the grove`); continue; }
      if (f.ultRoot && !this.over && f.alive){ if (f.groveFade !== 1) fail(10, `groveFade ${f.groveFade} while the window stands`); else inc("fadeOk"); }
      else if (!f.alive && f.groveFade !== 0) fail(10, `the green outlives its caster (groveFade ${f.groveFade})`);
      else if (f.groveFade > 0) inc("witherOk");
    }
    return r;
  };
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== HW);
  const row = AC.WEAPONS.find(w => w.id === HW).ult;
  for (const [k, v] of [["charge", PIN.charge], ["dur", PIN.dur], ["rootFor", PIN.rootFor], ["extraEnt", PIN.extraEnt]])
    if (row[k] !== v) fail(7, `the row's ${k} is ${row[k]}, the stage's ${v}`); else inc("rowOk");
  const blade = AC.WEAPONS.find(w => w.id === HW).dmg;
  if (blade !== PIN.blade) fail(7, `the blade is ${blade}, the stage's ${PIN.blade}`); else inc("rowOk");
  /* [8] THE FREEZE IS OUT OF THE ROW: the ult block is the design's keys and nothing else */
  const ROWKEYS = ["charge", "dur", "extraEnt", "kind", "name", "rootFor", "tip"];
  const keys = Object.keys(row).sort();
  if (JSON.stringify(keys) !== JSON.stringify(ROWKEYS)) fail(8, `the ult block's keys ${keys.join(",")}, want ${ROWKEYS.join(",")} (the freeze out)`);
  else inc("rowKeysOk");
  if (row.kind !== "rootfast" || row.name !== "Rootfast" || row.tip !== PIN.tip) fail(8, `the ult block is ${row.name} / ${row.kind} / ${row.tip}`);
  else inc("rowKeysOk");
  const S = { fights: 0, wins: 0, decided: 0, casts: 0, bin: 0, bout: 0, binOpp: 0, winSteps: 0, winFrozen: 0,
              labFrames: 0, labPinned: 0, entIn: 0, entUlt: 0, blows: 0, rooted: 0, roots: 0, ent: 0, frames: 0 };
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, HW, sd) : new AC.Match(HW, fid, sd);
    const me = side ? m.b : m.a;
    per = { casts: 0, bin: 0, bout: 0, binOpp: 0, winSteps: 0, winFrozen: 0, labFrames: 0, labPinned: 0, entIn: 0, entUlt: 0 };
    heldBy.clear(); voices.length = 0;
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){
      m.step(DT); steps++;
      if (drawn){
        const vis = [m.a, m.b].some(q => q.groveFade > 0 || q.groveMotes.length || q.groveBits.length);
        if (vis ? steps % drawEvery === 0 : steps % 60 === 0){
          const s0 = simSnap(m), p0 = picSnap(m);
          try { AC.__draw(m); } catch (e){ fail(10, "a drawn frame threw: " + String((e && e.message) || e)); }
          const s1 = simSnap(m), p1 = picSnap(m);
          if (s1 !== s0) fail(10, "a drawn frame changed the sim: " + firstDiff(s0, s1));
          else if (p1 !== p0) fail(10, "a drawn frame changed the picture's state: " + firstDiff(p0, p1));
          else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); }
        }
      }
    }
    S.fights++;
    if (m.winner){ S.decided++; if (m.winner === me) S.wins++; }
    for (const k in per) S[k] += per[k];
    if (me.rootTally) for (const k of ["blows", "rooted", "roots", "ent", "frames"]) S[k] += me.rootTally[k];
  }
  P.step = oStep; P.tickRootfast = oTick; P.rootBlow = oRoot; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  if (stage6p) P.tickGrove = oGrove;
  if (stage6v){
    if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
    /* EVERY HEARTWOOD VOICE OF THE RUN, ACCOUNTED FOR by its event */
    const want = { [HW]: n.castVoice || 0, [RV]: n.rootVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(hwAll)]))
      if ((hwAll[k] || 0) !== (want[k] || 0)) fail(9, `${hwAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  return { n, bad, S, wantCalls, stage6v, stage6p, drawOn, hwAll, groveCalls,
           u: { charge: row.charge, dur: row.dur, rootFor: row.rootFor, extraEnt: row.extraEnt, blade } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRootfast === 'function'"):
        raise SystemExit("no tickRootfast in this build -- not a Rootfast link (stage 2+)")
    # EVERY NUMBER PINNED BY THE STAGE, from the builder -- never read off the link under test.
    PIN = {"charge": HB.ULT["charge"], "dur": HB.ULT["dur"], "rootFor": HB.ULT["rootFor"],
           "extraEnt": 0 if a.stage == "2" else HB.ULT["extraEnt"],
           "blade": float(HB.BLADE if a.stage in ("5", "6") else HB.SHIPPED_DMG), "tip": HB.TIP}
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN, 0 if a.no_draw else a.draw_every])
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
print(f"  nothing else: {n.get('rootClean', 0)} root calls, {n.get('tickClean', 0)} ticker calls and "
      f"{n.get('castClean', 0)} casts snapshotted whole (both fighters, the shades, the match), clean; "
      f"the opponent's status exactly its applications after {n.get('entRecOk', 0)} root calls ({n.get('entRecApplied', 0)} with an entangle)")
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
        "(every field of both fighters, the shades and the match; the opponent's status exactly its applications), no RNG",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("rootClean", 0) > 0
        and n.get("tickClean", 0) > 0 and n.get("entRecOk", 0) > 0),
    (7, "a cast exactly when the live clock reaches the builder's charge, never with the window open; the row "
        "(charge, window, root, entangle, blade) is the stage's",
        n.get("castOk", 0) > 0 and n.get("chargeOk", 0) > 0 and n.get("rowOk", 0) == 5),
    (8, "the freeze out: the ult block is the design's keys only; the cast opens the window and resolves nothing "
        "(snapshotted whole, no RNG; only the window, the tally, ultsFired and the generic cast's picture)",
        n.get("castClean", 0) > 0 and n.get("rowKeysOk", 0) == 2),
]
S6 = a.stage == "6"
if R.get("stage6v") or S6:
    print(f"  stage 6 voice{'' if R.get('stage6v') else ' -- NOT ON THIS LINK'}: casts voiced {n.get('castVoice', 0)}  "
          f"roots voiced {n.get('rootVoice', 0)}  killing blows silent {n.get('killSilent', 0)}  closes silent: "
          f"clock {n.get('clockSilent', 0)}, death {n.get('deathSilent', 0)}   run totals {R.get('hwAll')}")
    checks.append((9, "stage 6 voice: one cast voice a cast, inside fireUlt; one root voice a rooted blow, inside rootBlow, "
                      "and nothing else there; none on a killing blow; none at a close, by the clock or a death; every "
                      "Heartwood voice of the run accounted for",
                   bool(R.get("stage6v")) and all(n.get(k, 0) > 0 for k in ("castVoice", "rootVoice", "killSilent",
                                                                           "clockSilent", "deathSilent"))))
if R.get("stage6p") or S6:
    print(f"  stage 6 picture{'' if R.get('stage6p') else ' -- NOT ON THIS LINK'}: tickGrove calls {R.get('groveCalls', 0)} "
          f"(sim clean {n.get('groveOk', 0)}, whole-state clean {n.get('groveWhole', 0)})  roots marked: new holds "
          f"{n.get('markHold', 0)}, re-roots {n.get('markReroot', 0)}, self-held left alone {n.get('selfHeld', 0)}  "
          f"tags counted {n.get('tagOk', 0)} (teaching panels {n.get('tagFirst', 0)})  green in the window {n.get('fadeOk', 0)}  "
          f"wither frames {n.get('witherOk', 0)}  drawn frames {n.get('drawOk', 0)} ({n.get('drawPic', 0)} with the "
          f"picture up, {n.get('drawPicStop', 0)} in a hit stop)" + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((10, "stage 6 picture: tickGrove draws no RNG and writes nothing but its own fields, the held ball's "
                       "markers and a tag's count; every root on a held ball marked, a self-held ball left alone; the tag "
                       "prints the count; green exactly while the window stands; no drawn frame throws or writes",
                   bool(R.get("stage6p")) and all(n.get(k, 0) > 0 for k in ("groveOk", "groveWhole", "markHold",
                                                                           "markReroot", "tagOk", "fadeOk", "witherOk"))
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
