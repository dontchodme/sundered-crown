#!/usr/bin/env python
"""BENEDICTION'S PROBE (the halo, v82) -- one check per sentence of v82 §1 / §4,
read INSIDE the hooks.

    python aureole_probe.py --game <sc-aureole-halo.html | -bless | -b<X>>

Wraps `tickHalo`, `fireUlt`, `tickWeapon`, `tickFire`, `resolveHit`,
`tickStatus` and `step` on the Match prototype and reads each event where it
happens. Runs Aureole against every other relic, both sides, and prints N/N.
The checks follow the link's own numbers, so the same probe gates stages 2, 3
and 5 (bless 0 / 1); [7] holds those numbers to the design's.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration a halo of light stands around Aureole": a window whose
      clock does not advance by exactly dt a call, that closes before `dur`
      on the window clock or outlives it or either death; `tickHalo` not asked
      exactly once on every unfrozen step, or asked on a frozen one (the step
      wrapper counts the calls: dt a call is the window clock only if the
      calls are one a step -- the v108 review's lesson); any relic but
      Aureole carrying `ultHalo`
  [2] "wide enough to reach half the hall ... an enemy inside the halo":
      a window frame whose inside flag (the engine's `haloTally.inFrames`
      rising) is not the rebuilt test, the foe's centre strictly within
      haloR + R of the caster's centre on that frame (v82 §4; the lab's `<`)
  [3] "is smitten for as long as it stays there": a window frame whose smite
      is not exactly the rebuilt cooldown's -- cd - dt <= 0 on an inside
      frame: exactly one apply("smite", smite, side letter) ON THE FOE and cd
      = tickCd; otherwise none and cd - dt -- or whose stacks after the apply
      are not the engine's (min(4, before + smite), the clock 3.2); a smite on
      an outside frame or on anybody but the foe
  [4] "and for as long as an enemy is inside it, Aureole is blessed": the
      same for the blessing on its own cooldown -- bcd - dt <= 0 on an inside
      frame: exactly one apply("blessing", bless, side letter) ON THE CASTER
      and bcd = blessCd; otherwise none and bcd - dt; none at bless 0; none
      on the foe; none on an outside frame. And the blessing is her ONLY heal
      now: every tickStatus of hers heals by exactly her blessing's
      hps x stacks x dt (the engine's arithmetic, rebuilt) and nothing else
  [5] "No damage, no knock, no beat" (§4): a tickHalo call that hurts
      anybody, moves or pushes a ball, stops the world, files a beat, draws
      the rng, spawns a shot, applies any other status or changes any
      fighter's hp, ward or ward pool
  [6] no arrows through the halo (§6.3, arm D not taken): Aureole's facing
      not advancing by spin as ever, in the window and out; the bow's fire not
      asked exactly once on every unfrozen step, or a fire frame whose cadence
      is not the engine's, rebuilt from the captured state; any blow of hers
      whose damage is not the bow's own (rebuilt from the captured crit and
      jitter draws), or whose statuses on the foe are not exactly the
      channel's `smite 1` -- in the window and out
  [7] the beam is out: a cast that spawns a shot, hurts or heals anybody,
      applies any status, that does not open {t: 0, dur, cd: 0, bcd: 0}, or
      that lands on an open window; an ult block whose numbers are not the
      design's (dur 8, haloR 150, tickCd 0.5, smite 1, blessCd 0.8, bless 0 or
      1) or that still carries the beam's dmg / heal
  [8] a smite tick that kills files its fatal beat for HER side (reading 6:
      the side letter; the lab's Fighter would credit side b every time)

STAGE 6 (the picture and the voice, the builder's readings 14-20), each check
run only where the link carries it -- the voices detected by the entry's arm
(`aureole-enter`) in `AC.SFX.play.toString()`, the picture by `tickBenediction`
on the Match -- so the same probe still gates stages 2-5 at 8/8, every line as
before. Once a fight is over the probe steps 2 s more of the verdict (the
step's `over` path: only the presentation clock runs) for these two checks
alone; [1]-[8] read none of those steps.
  [9] THE VOICES fire exactly on their events and nowhere else (v82 §4's
      sound). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Aureole's three arms ("ult" with w "aureole", "aureole-enter",
      "aureole-close") and the heal chime ("spark" with collect) are read; a
      ward's shatter -- which plays its own crit HIT voice inside hurt() -- is
      not one of them, nor is any other relic's cast. Evidence: an Aureole
      cast playing anything but exactly one cast voice (w "aureole") inside
      fireUlt, or the cast voice anywhere else; a tickHalo call whose voices
      are not EXACTLY, in order, the rebuilt ones -- the entry on an inside
      tick that follows an outside tick of the same window (never on the
      window's first tick: a foe already inside when the halo rises is no
      entry), one heal chime a blessing laid (n her blessing after it), and
      the close voice on a close BY THE CLOCK with both alive and NEVER ON A
      CLOSE BY A DEATH; a heal chime anywhere but the halo and the other
      relics' spark tickers (`tickSun`, `tickSparks`, `tickHolyGround`); any
      of them in the picture's hook, a drawn frame or the verdict. Every one
      of the run is accounted for: cast voices = casts, chimes = blessings,
      close voices = clock closes.
  [10] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickBenediction`
      (tickPresentation, the picture's one call on the step path) is wrapped:
      evidence is any change across it to either fighter (every own number,
      flag and string but its `bene*` fields, every array's length, every
      status, the window and its `voiceIn`, the tally, the weapon row and its
      ult) or to the match (every own number, flag and string, every array's
      length but `tags`, every shot's x, y, vx, vy and life), an RNG draw or a
      voice. And the picture as declared (readings 14-15), REBUILT from the
      tally the way [3] rebuilds the smite: the ring not up (`beneFade` 1) in
      an open window (`ultHalo`, the match live, the caster alive) or its
      growth clock not the presentation clock since the cast, up with none,
      or a close that is not a fade to 0 over exactly 0.6 of its clock (0.3
      s) -- by the clock, on a death or AT THE KILL; "inside" not
      `tickHalo`'s own answer (a step the window ticked is an inside step iff
      `inFrames` rose with it; through a hit stop the last answer holds); the
      brightening not 0.2 / 0.5 of its clock up and down; a SMITE tag not
      exactly on the first smite of each inside stretch (at the foe, with its
      count), a BLESSING tag not exactly on the first blessing of each (on
      her, with her count), or any other tag; the foe carrying any of it; and
      the ring up or lit after 2 s of the verdict.
  --drawn N (default 6; 0 = off): on the FIRST seed, both sides, every foe,
      each fight is also drawn through the renderer (`AC.__draw`, the post
      chain off, 270x480) every Nth step while the picture shows and every
      60th otherwise, through the kill and the verdict. [10] fails a drawn
      frame that throws, draws the match's RNG or changes the simulation (the
      snapshot above). It runs on any link, so the base's draws are its
      control.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=110001)
ap.add_argument("--json", default=None)
ap.add_argument("--foes", default="", help="comma list of foes (default: every other relic)")
ap.add_argument("--sides", default="AB", help="AB (both sides, the default) or A (the lab's side)")
ap.add_argument("--seedstep", type=int, default=13, help="seeds are seed0 + seedstep x i (the lab's is 11)")
ap.add_argument("--drawn", type=int, default=6, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()

JS = r"""([seeds, foeList, sides, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, ST = AC.STATUS;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickHalo, oFire = P.fireUlt, oWeap = P.tickWeapon, oLoose = P.tickFire,
        oResolve = P.resolveHit, oStep = P.step, oStatus = P.tickStatus, oBeat = P.beat;
  let live = false, per = null, fireCalls = 0, haloCalls = 0, inStatus = null;
  const winMT = new WeakMap();
  const isMe = f => !!(f && f.w && f.w.id === "aureole");
  const nm = h => h && h.w ? h.w.id : String(h);
  const srcName = s => typeof s === "object" && s ? "a Fighter" : JSON.stringify(s);

  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: the entry's arm in the synth
     [9], `tickBenediction` on the match [10]. A link without them runs
     [1]-[8] only. ---- */
  const S6V = /aureole-enter/.test(AC.SFX.play.toString()), S6P = typeof P.tickBenediction === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oBene = P.tickBenediction;
  const OTHER = ["tickSun", "tickSparks", "tickHolyGround"].filter(k => typeof P[k] === "function"), oOther = {};
  let F = null, vctx = "a step", vrec = null, tail = false;
  const OURS = { "aureole": "cast", "aureole-enter": "halo", "aureole-close": "halo" };
  const isChime = (kind, q) => kind === "spark" && !!q && q.collect === true;
  const isOurs = (kind, q) => kind === "ult" && !!q && Object.prototype.hasOwnProperty.call(OURS, q.w);
  const vKey = c => isChime(c[0], c[1]) ? ["chime", c[1].n] : [c[0], c[1] && c[1].w];
  if (S6V) AC.SFX.play = function(kind, q){
    if (F){
      if (vrec) vrec.push([kind, q ? Object.assign({}, q) : q]);
      const ours = isOurs(kind, q), chime = isChime(kind, q);
      if (ours || chime){
        const ok = ours ? vctx === OURS[q.w] : (vctx === "halo" || vctx === "another relic's sparks");
        if (!ok) fail(9, `${ours ? "the " + q.w + " voice" : "the heal chime (spark collect)"} played in ${vctx}`);
        inc(ours ? "v_" + q.w : vctx === "halo" ? "v_chime" : "v_chimeOther");
      }
    }
    return oPlay.call(this, kind, q);
  };
  /* the other relics' spark tickers may play the chime (theirs) */
  const ctxWrap = (fn, name) => function(){
    if (!F || F.m !== this) return fn.apply(this, arguments);
    const v0 = vctx; vctx = name;
    try { return fn.apply(this, arguments); } finally { vctx = v0; } };
  if (S6V) for (const k of OTHER){ oOther[k] = P[k]; P[k] = ctxWrap(P[k], "another relic's sparks"); }
  const prevIn = new WeakMap();   // [9] the last inside answer of each window, rebuilt
  /* [10] the simulation's state, as one array in a fixed key order: both
     fighters' own numbers, flags and strings (their `bene*` fields aside) and
     array lengths, statuses, the window with its `voiceIn`, the tally, the
     weapon row and its ult; the match's own numbers, flags and strings and
     every array's length (`tags` aside: the SMITE and BLESSING tags are the
     picture's to file), and every shot's x, y, vx, vy and life */
  const same = (x, y) => x === y || (x !== x && y !== y);
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 98 && k.startsWith("bene")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      for (const k in f.status){ const st = f.status[k]; o.push(k, st.stacks, st.t, st.src); }
      const Z = f.ultHalo;
      if (Z) o.push("Z", Z.t, Z.dur, Z.cd, Z.bcd, Z.voiceIn); else o.push("Z-");
      const T = f.haloTally;
      if (T) for (const k of Object.keys(T)) o.push(k, T[k]); else o.push("T-");
      for (const k of Object.keys(f.w)){ const v = f.w[k]; if (v === null || typeof v !== "object") o.push(k, v); }
      if (f.w.ult) for (const k of Object.keys(f.w.ult)){ const v = f.w.ult[k]; if (v === null || typeof v !== "object") o.push(k, v); }
    }
    for (const k of Object.keys(m)){
      if (k === "tags") continue;
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
  let PM = null;   // the picture, rebuilt: per fight

  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [9]-[10] alone */
    if (tail) return oStep.call(this, dt);
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;
    const wasLive = live, me = isMe(this.a) ? this.a : isMe(this.b) ? this.b : null;
    for (const f of [this.a, this.b]) if (f.ultHalo){ if (live) inc("winLive"); else inc("winFrozen"); }
    for (const f of [this.a, this.b]) if (f.ultHalo && winMT.has(f.ultHalo)) winMT.get(f.ultHalo).mt += dt;
    fireCalls = 0; haloCalls = 0;
    const r = oStep.call(this, dt);
    /* THE HALO'S CLOCK IS THE STEP'S: tickHalo once on every unfrozen step, none on a frozen one */
    if (wasLive && haloCalls !== 1) fail(1, `${haloCalls} tickHalo call(s) on an unfrozen step`);
    else if (!wasLive && haloCalls) fail(1, `${haloCalls} tickHalo call(s) on a frozen step`);
    else if (wasLive) inc("haloStepOk");
    if (me){
      if (wasLive && fireCalls !== 1) fail(6, `${me.ultHalo ? "IN" : "out of"} the window: ${fireCalls} tickFire call(s) on an unfrozen step`);
      else if (!wasLive && fireCalls) fail(6, `${fireCalls} tickFire call(s) on a frozen step`);
      else if (wasLive) inc("fireStepOk");
    }
    live = false;
    return r;
  };

  /* [8] A FATAL SMITE TICK ON HER FOE credits her side (tickStatus files the beat) */
  P.beat = function(o){
    if (inStatus && o && o.fatal && o.tick && o.status === "smite"){
      const { f, me } = inStatus;
      if (me && f !== me){
        const sd = me === this.a ? 0 : 1;
        if (o.side !== sd) fail(8, `a fatal smite tick on her foe credited side ${o.side}, want ${sd}`);
        else inc("fatalSmiteOk");
      }
    }
    return oBeat.call(this, o);
  };
  /* [4] HER ONLY HEAL IS THE BLESSING: rebuild her hp through tickStatus when nothing else touches it */
  P.tickStatus = function(f, dt){
    const me = isMe(this.a) ? this.a : isMe(this.b) ? this.b : null;
    inStatus = { f, me };
    const hp0 = f.hp, bl = f.status.blessing ? { s: f.status.blessing.stacks, t: f.status.blessing.t } : null;
    const others = Object.keys(f.status).filter(k => k !== "blessing" && ST[k] && ST[k].dps);
    let r;
    try { r = oStatus.call(this, f, dt); } finally { inStatus = null; }
    if (f === me && !others.length && hp0 > 0){
      let want = hp0;
      if (bl && bl.t - dt > 0) want = Math.min(f.maxHp, hp0 + ST.blessing.hps * bl.s * dt);
      want = Math.min(want, f.maxHp);
      if (f.hp !== want) fail(4, `her hp ${hp0} -> ${f.hp} in tickStatus, the blessing (${bl ? bl.s : 0} stacks) rebuilds ${want}`);
      else if (bl && bl.t - dt > 0 && want > hp0) inc("blessHealOk"); else inc("statusQuietOk");
    }
    return r;
  };

  P.fireUlt = function(f, foe){
    if (!isMe(f)) return oFire.call(this, f, foe);
    const open = !!f.ultHalo, ns = this.shots.length;
    const st = [f, foe].map(x => ({ x, hp: x.hp, shield: x.shield, stat: JSON.stringify(Object.keys(x.status).sort().map(k => [k, x.status[k].stacks, x.status[k].t])) }));
    const oHurt = this.hurt, hurts = [], applies = [];
    this.hurt = function(t, d, s){ hurts.push([t, d, s]); return oHurt.call(this, t, d, s); };
    for (const x of [f, foe]){ const o = x.apply; x.apply = function(k, nn, src){ applies.push([x, k, nn]); return o.call(this, k, nn, src); }; }
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "cast"; vrec = [];
    try { r = oFire.call(this, f, foe); }
    finally { delete this.hurt; delete f.apply; delete foe.apply; heard = vrec; vctx = vc0; vrec = vr0; }
    /* [9] THE CAST'S VOICE: exactly one, inside fireUlt (the prologue's `SFX.play("ult", { w: f.w.id })`) */
    if (S6V){
      const mine = heard.filter(c => isOurs(c[0], c[1]) || isChime(c[0], c[1]));
      if (mine.length !== 1 || mine[0][1].w !== "aureole") fail(9, `an Aureole cast played ${JSON.stringify(mine)}, want one cast voice`);
      else inc("castVoiceOk");
    }
    const u = f.w.ult;
    if (open) fail(7, "a cast on an open window");
    else if (this.shots.length !== ns) fail(7, `the cast spawned ${this.shots.length - ns} shot(s)`);
    else if (hurts.length || applies.length) fail(7, `the cast hurt ${hurts.length} and applied ${JSON.stringify(applies.map(x => [nm(x[0]), x[1], x[2]]))}`);
    else if (st.some(s => s.x.hp !== s.hp || s.x.shield !== s.shield)) fail(7, `the cast moved an hp or a ward: ${JSON.stringify(st.map(s => [nm(s.x), s.hp, s.x.hp, s.shield, s.x.shield]))}`);
    else if (st.some(s => JSON.stringify(Object.keys(s.x.status).sort().map(k => [k, s.x.status[k].stacks, s.x.status[k].t])) !== s.stat)) fail(7, "the cast moved a status");
    else if (!f.ultHalo || f.ultHalo.t !== 0 || f.ultHalo.cd !== 0 || f.ultHalo.bcd !== 0 || f.ultHalo.dur !== u.dur) fail(7, `the cast opened ${JSON.stringify(f.ultHalo)}`);
    else { inc("castOk"); winMT.set(f.ultHalo, { mt: 0 }); }
    return r;
  };

  P.tickWeapon = function(f, foe, dt){
    if (!isMe(f)) return oWeap.call(this, f, foe, dt);
    const th0 = f.theta, stun = f.stun, spin = f.w.spin * f.spinMul(this.actMods.spin), dir = f.spinDir, open = !!f.ultHalo;
    const r = oWeap.call(this, f, foe, dt);
    const want = stun > 0 ? th0 : th0 + spin * dt * dir;
    if (f.theta !== want) fail(6, `${open ? "IN" : "out of"} the window: theta ${th0} -> ${f.theta}, want ${want}`);
    else inc(open ? "spinInOk" : "spinOutOk");
    return r;
  };
  /* THE BOW'S FIRE, REBUILT (the v108 review's): the engine's tickFire arithmetic on the captured state */
  P.tickFire = function(f, foe, dt){
    if (!isMe(f)) return oLoose.call(this, f, foe, dt);
    if (f === this.a || f === this.b) fireCalls++;
    const S = f.w.shot, open = !!f.ultHalo, cd0 = f.fireCd;
    const skip = (this.killFlight && f.hp <= 0) || !S || !f.alive || this.over || f.stun > 0 || !!f.ultDraw;
    const cm = (f.ultBal || f.ultNet) && f.w.ult.cadMul !== undefined ? f.w.ult.cadMul : 1;
    const cad = S ? S.cadence : 0, spawns = [], oSpawn = this.spawnShot;
    this.spawnShot = function(ff, ang){ if (ff === f) spawns.push(ang); return oSpawn.call(this, ff, ang); };
    let r;
    try { r = oLoose.call(this, f, foe, dt); }
    finally { delete this.spawnShot; }
    const where = open ? "IN" : "out of";
    if (skip){
      if (spawns.length || f.fireCd !== cd0) fail(6, `${where} the window: a skipped frame loosed ${spawns.length} and moved fireCd ${cd0} -> ${f.fireCd}`);
      else inc("fireSkipOk");
    } else {
      const want = cd0 - dt;
      if (want > 0){
        if (spawns.length || f.fireCd !== want) fail(6, `${where} the window: fireCd ${cd0} -> ${f.fireCd} and ${spawns.length} loosed, want ${want} and none`);
        else inc(open ? "fireInOk" : "fireOutOk");
      } else {
        const cd1 = want + cad * cm;
        if (spawns.length !== 1 || spawns[0] !== undefined || f.fireCd !== cd1)
          fail(6, `${where} the window: fireCd ${cd0} -> ${f.fireCd} and ${spawns.length} loosed (angle ${spawns[0]}), want ${cd1} and one ordinary shot`);
        else inc(open ? "fireInOk" : "fireOutOk");
      }
    }
    if (spawns.length) inc(open ? "shotsIn" : "shotsOut", spawns.length);
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isMe(self)) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultHalo, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul(), aegis: !!foe.ultAegis,
                  echo: Math.round(foe.curseEcho()) };
    const draws = [], oRng = this.rng, applies = [], oAp = foe.apply;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    foe.apply = function(k, nn, src){ applies.push([k, nn]); return oAp.call(this, k, nn, src); };
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; delete foe.apply; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    const D = self.dealt - d0, crit = self.crits > c0;
    const raw = self.w.dmg * (mul === undefined ? 1 : mul) * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw) + pre.echo;
    if (Math.abs(D - want) > 1e-6){ if (pre.aegis) inc("blowExempt"); else fail(6, `${open ? "IN" : "out of"} the window: dealt ${D}, want ${want} (mul ${mul})`); }
    else inc(open ? "blowInOk" : "blowOutOk");
    /* THE BLOW'S STATUSES: the channel's smite 1 and nothing else, in the window and out */
    if (JSON.stringify(applies) !== JSON.stringify([["smite", 1]])){ if (pre.aegis && !applies.length) inc("blowExempt"); else fail(6, `${open ? "IN" : "out of"} the window: a blow applied ${JSON.stringify(applies)}, want [["smite",1]]`); }
    else inc(open ? "chanInOk" : "chanOutOk");
    return r;
  };

  P.tickHalo = function(dt){
    haloCalls++;
    if (!live) fail(1, "tickHalo on a frozen step");
    for (const f of [this.a, this.b]) if (f.ultHalo && !isMe(f)) fail(1, `${f.w.id} carries ultHalo`);
    const wins = [];
    for (const f of [this.a, this.b]){
      const Z = f.ultHalo;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      wins.push({ f, foe, Z, t0: Z.t, cd0: Z.cd, bcd0: Z.bcd, fAlive: f.alive, foeAlive: foe.alive,
                  d: Math.hypot(foe.x - f.x, foe.y - f.y), in0: f.haloTally.inFrames,
                  sm: foe.stacks("smite"), bl: f.stacks("blessing") });
    }
    const st = [this.a, this.b].map(f => ({ f, x: f.x, y: f.y, vx: f.vx, vy: f.vy, hp: f.hp, alive: f.alive,
                                            shield: f.shield, smax: f.shieldMax, theta: f.theta, stun: f.stun, pin: f.pin,
                                            stat: JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t])) }));
    const hs0 = this.hitStop, ns = this.shots.length, hurts = [], beats = [], applies = [];
    const oHurt = this.hurt, oB = this.beat, oRng = this.rng;
    let draws = 0;
    this.hurt = function(t, d, s){ hurts.push([t, d, s]); return oHurt.call(this, t, d, s); };
    this.beat = function(o){ beats.push(o); return oB.call(this, o); };
    this.rng = function(){ draws++; return oRng(); };
    const fs = [this.a, this.b];
    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ const e = [f, k, nn, src]; applies.push(e); const rr = o.call(this, k, nn, src); e.push(f.stacks(k), f.status[k] ? f.status[k].t : null); return rr; }; }
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "halo"; vrec = [];
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; heard = vrec; vctx = vc0; vrec = vr0; }
    const wantV = [], vk = [];   // [9] the voices this call must play, rebuilt, and what passing counts
    /* [5] NOTHING ELSE: no hurt, no beat, no rng, no shot, no stop, no move, no hp or ward change */
    if (hurts.length) fail(5, `the halo hurt ${JSON.stringify(hurts.map(h => [nm(h[0]), h[1]]))}`);
    if (beats.length) fail(5, `the halo filed ${beats.length} beat(s)`);
    if (draws) fail(5, `the halo drew the rng ${draws} time(s)`);
    if (this.shots.length !== ns) fail(5, "the halo spawned a shot");
    if (this.hitStop !== hs0) fail(5, `hitStop ${hs0} -> ${this.hitStop}`);
    for (const s of st){
      const f = s.f;
      if (f.x !== s.x || f.y !== s.y || f.vx !== s.vx || f.vy !== s.vy) fail(5, "the halo moved or pushed a ball");
      if (f.hp !== s.hp || f.shield !== s.shield || f.shieldMax !== s.smax) fail(5, `the halo moved ${nm(f)}'s hp ${s.hp} -> ${f.hp} or ward ${s.shield} -> ${f.shield}`);
      if (f.theta !== s.theta || f.stun !== s.stun || f.pin !== s.pin) fail(5, "the halo turned, stunned or pinned a ball");
      const stat = JSON.stringify(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
      if (stat !== s.stat && !applies.some(x => x[0] === f)) fail(5, "a status moved with no apply");
    }
    /* THE WINDOWS: [1] the clock, [2] the inside test, [3] the smite, [4] the blessing */
    const expect = [];
    for (const w of wins){
      const { f, foe, Z } = w, u = f.w.ult, t1 = w.t0 + dt, side = f === this.a ? "a" : "b";
      if (t1 >= Z.dur || !w.fAlive || !w.foeAlive){
        if (f.ultHalo === Z){ fail(1, "the window did not close"); continue; }
        if (w.fAlive && w.foeAlive){ inc("clockCloses"); const M = winMT.get(Z); if (M){ inc("winMT", M.mt); inc("winMTn"); }
          wantV.push(["ult", "aureole-close"]); vk.push("closeClockOk"); }
        else { inc("deathCloses"); vk.push("closeDeathQuiet"); }
        if (f.haloTally.inFrames !== w.in0) fail(2, "a closed window counted an inside frame");
        continue;
      }
      if (f.ultHalo !== Z){ fail(1, `closed at ${t1.toFixed(4)} of ${Z.dur}`); continue; }
      if (Z.t !== t1) fail(1, `window clock ${w.t0} -> ${Z.t}, want ${t1}`);
      else inc("frames");
      /* [2] the inside flag, the engine's, against the rebuilt geometry */
      const inside = w.d < u.haloR + R, flag = f.haloTally.inFrames - w.in0;
      if (flag !== (inside ? 1 : 0)) fail(2, `inside flag ${flag} at d ${w.d.toFixed(3)} against haloR + R ${u.haloR + R}`);
      else inc(inside ? "inOk" : "outOk");
      if (inside && w.d > u.haloR) inc("inRim");     // the + R: inside by the rim, not the centre
      const IN = flag === 1;
      /* [9] THE ENTRY: an inside tick after an outside tick of the same window */
      const pIn = prevIn.get(Z);
      if (IN && pIn === false){ wantV.push(["ult", "aureole-enter"]); vk.push("enterOk"); }
      else if (IN) vk.push(pIn === undefined ? "firstInQuiet" : "stayQuiet");
      else vk.push("outQuiet");
      prevIn.set(Z, IN);
      /* [3] the smite's cooldown, rebuilt; the smite judged on the engine's inside flag */
      const cd1 = w.cd0 - dt, smiteNow = IN && cd1 <= 0;
      if (smiteNow){
        if (Z.cd !== u.tickCd) fail(3, `cd ${w.cd0} -> ${Z.cd} on a smite frame, want ${u.tickCd}`);
        else inc("smiteCdOk");
        expect.push({ who: foe, k: "smite", nn: u.smite, side, before: w.sm, cap: ST.smite.maxStacks, dur: ST.smite.dur, chk: 3 });
      } else if (Z.cd !== cd1) fail(3, `cd ${w.cd0} -> ${Z.cd}, want ${cd1}`);
      else inc(IN ? "smiteWaitOk" : "smiteOutOk");
      /* [4] the blessing's cooldown, rebuilt */
      const bcd1 = w.bcd0 - dt, blessNow = u.bless > 0 && IN && bcd1 <= 0;
      if (blessNow){
        if (Z.bcd !== u.blessCd) fail(4, `bcd ${w.bcd0} -> ${Z.bcd} on a blessing frame, want ${u.blessCd}`);
        else inc("blessCdOk");
        expect.push({ who: f, k: "blessing", nn: u.bless, side, before: w.bl, cap: ST.blessing.maxStacks, dur: ST.blessing.dur, chk: 4 });
        wantV.push(["chime", f.stacks("blessing")]); vk.push("chimeOk");
      } else if (Z.bcd !== bcd1) fail(4, `bcd ${w.bcd0} -> ${Z.bcd}, want ${bcd1}`);
      else inc(u.bless > 0 ? (IN ? "blessWaitOk" : "blessOutOk") : "bless0Ok");
    }
    /* THE CALL'S APPLIES ARE EXACTLY THE EXPECTED ONES, IN ORDER */
    const got = applies.map(x => [nm(x[0]), x[1], x[2], srcName(x[3])]);
    const want = expect.map(e => [nm(e.who), e.k, e.nn, JSON.stringify(e.side)]);
    if (JSON.stringify(got) !== JSON.stringify(want)){
      const k = expect.some(e => e.chk === 4) || applies.some(x => x[1] === "blessing") ? 4 : 3;
      const smG = got.filter(g => g[1] === "smite"), smW = want.filter(g => g[1] === "smite");
      const blG = got.filter(g => g[1] === "blessing"), blW = want.filter(g => g[1] === "blessing");
      const oth = got.filter(g => g[1] !== "smite" && g[1] !== "blessing");
      if (JSON.stringify(smG) !== JSON.stringify(smW)) fail(3, `the call's smites ${JSON.stringify(smG)}, want ${JSON.stringify(smW)}`);
      if (JSON.stringify(blG) !== JSON.stringify(blW)) fail(4, `the call's blessings ${JSON.stringify(blG)}, want ${JSON.stringify(blW)}`);
      if (oth.length) fail(5, `the halo applied ${JSON.stringify(oth)}`);
    } else {
      for (let i = 0; i < expect.length; i++){
        const e = expect[i], x = applies[i];
        const s1 = e.before < e.cap ? Math.min(e.cap, e.before + e.nn) : e.before;
        if (x[4] !== s1 || x[5] !== e.dur) fail(e.chk, `${e.k} stacks ${e.before} -> ${x[4]} clock ${x[5]}, want ${s1} and ${e.dur}`);
        else inc(e.k === "smite" ? "smiteOk" : "blessOk");
      }
    }
    /* [9] THE HALO'S VOICES: exactly the rebuilt ones, in order, and nothing else */
    if (S6V){
      const got = JSON.stringify(heard.map(vKey)), want = JSON.stringify(wantV);
      if (got !== want) fail(9, `the halo played ${got}, want ${want}`);
      else for (const k of vk) inc(k);
    }
    inc("calls");
    return r;
  };

  /* [10] THE PICTURE'S HOOK: `tickBenediction`, on the presentation clock
     (tickPresentation: through hit stops, twice a normal step, and in the
     verdict). The picture is REBUILT from the tally, as [3] rebuilds the
     smite (readings 14-15). */
  if (S6P) P.tickBenediction = function(dt){
    if (!F || F.m !== this) return oBene.call(this, dt);
    inc("beneCalls");
    const me = F.me, foe = F.foe;
    const s0 = simSnap(this), tags0 = new Set(this.tags), fade0 = me.beneFade;
    let draws = 0; const oRng = this.rng;
    this.rng = function(){ draws++; return oRng.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture"; vrec = [];
    let r, heard = null;
    try { r = oBene.call(this, dt); } finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = firstDiff(s0, simSnap(this));
    if (d) fail(10, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (draws) fail(10, `the picture drew the RNG ${draws} times`);
    else if (heard.length) fail(10, `the picture played ${JSON.stringify(heard)}`);
    else inc("beneClean");
    /* the foe never carries any of it */
    if (foe.beneFade !== 0 || foe.beneLit !== 0 || foe.beneIn || foe.beneAge !== 0 || foe.beneOut !== 0
        || foe.beneTagS || foe.beneTagB) fail(10, `${foe.w.id}, which is not Aureole, carries the picture`);
    const T = me.haloTally;
    const fresh = this.tags.filter(g => !tags0.has(g));
    if (!T){
      if (me.beneFade !== 0 || me.beneLit !== 0) fail(10, "Aureole carries the picture before her first cast");
      if (fresh.length) fail(10, `a tag before Aureole's first cast: ${fresh.map(g => g.key)}`);
      return r;
    }
    if (!PM) PM = { seen: [0, 0, 0, 0], in: false, lit: 0, age: 0, tagS: false, tagB: false, closeDt: -1, prevZ: null };
    const Z = (this.over || !me.alive) ? null : me.ultHalo;
    /* THE RING: up exactly while the window is open, its growth clock the
       presentation clock since the cast; a 0.3 s contraction at any close */
    if (Z){
      if (PM.prevZ !== Z){ PM.in = false; PM.lit = 0; PM.age = 0; PM.tagS = false; PM.tagB = false; inc("picCasts"); }
      PM.age += dt;
      if (me.beneFade !== 1) fail(10, `the ring not up (${me.beneFade}) in an open window`);
      else if (me.beneAge !== PM.age) fail(10, `the ring's growth clock ${me.beneAge}, want ${PM.age}`);
      else inc("upOk");
      PM.closeDt = -1;
    } else if (fade0 > 0){
      if (PM.closeDt < 0){ PM.closeDt = 0;
        inc(this.over ? (me.ultHalo ? "picCloseOverOpen" : "picCloseOver") : !me.alive ? "picCloseDeath"
            : !foe.alive ? "picCloseFoeDeath" : "picCloseClock"); }
      PM.closeDt += dt;
      const want = Math.max(0, 1 - PM.closeDt / 0.6);
      if (Math.abs(me.beneFade - want) > 1e-9) fail(10, `the ring's close: ${me.beneFade} at ${PM.closeDt.toFixed(4)} of its clock, want ${want}`);
      else if (me.beneFade === 0) inc("picClosedOk");
    } else if (me.beneFade !== 0) fail(10, `the ring up (${me.beneFade}) with no window open`);
    PM.prevZ = Z;
    /* INSIDE, the brightening and the tags, from the tally's rises */
    const S = PM.seen, dF = T.frames - S[0], dI = T.inFrames - S[1], dS = T.smite - S[2], dB = T.bless - S[3];
    PM.seen = [T.frames, T.inFrames, T.smite, T.bless];
    if (!Z) PM.in = false; else if (dF > 0) PM.in = dI > 0;
    if (me.beneIn !== PM.in) fail(10, `inside: the picture's ${me.beneIn}, the ticker's ${PM.in}`);
    else if (Z) inc(PM.in ? (dF > 0 ? "picInOk" : "picInHeldOk") : "picOutOk");
    if (Z && dF === 0 && this.hitStop > 0) inc(PM.in ? "heldStopIn" : "heldStopOut");
    if (PM.in || PM.lit > 0) PM.lit = PM.in ? Math.min(1, PM.lit + dt / 0.2) : Math.max(0, PM.lit - dt / 0.5);
    if (me.beneLit !== PM.lit) fail(10, `the ring's brightening ${me.beneLit}, want ${PM.lit}`);
    else if (PM.lit === 1) inc("litFull"); else if (PM.lit > 0) inc(PM.in ? "litUp" : "litDown");
    if (!PM.in){ PM.tagS = false; PM.tagB = false; }
    let wantS = false, wantB = false;
    if (Z && foe.alive && foe.hp > 0){
      if (dS > 0 && !PM.tagS){ wantS = true; PM.tagS = true; }
      if (dB > 0 && !PM.tagB){ wantB = true; PM.tagB = true; }
    }
    const gS = fresh.filter(g => g.key === "smite"), gB = fresh.filter(g => g.key === "blessing");
    if (fresh.length !== gS.length + gB.length) fail(10, `the picture filed a tag that is not SMITE or BLESSING: ${fresh.map(g => g.key)}`);
    if (gS.length !== (wantS ? 1 : 0)) fail(10, `${gS.length} SMITE tag(s) on a call with ${dS} smite(s), want ${wantS ? 1 : 0}`);
    else if (wantS && (gS[0].x !== foe.x || gS[0].y !== foe.y || gS[0].val !== foe.stacks("smite"))) fail(10, "the SMITE tag not at the foe with its count");
    else if (wantS) inc("tagSOk");
    else if (dS > 0) inc("smiteUntagged");
    if (gB.length !== (wantB ? 1 : 0)) fail(10, `${gB.length} BLESSING tag(s) on a call with ${dB} blessing(s), want ${wantB ? 1 : 0}`);
    else if (wantB && (gB[0].x !== me.x || gB[0].y !== me.y || gB[0].val !== me.stacks("blessing"))) fail(10, "the BLESSING tag not on Aureole with her count");
    else if (wantB) inc("tagBOk");
    else if (dB > 0) inc("blessUntagged");
    return r;
  };

  /* THE DRAWN SUBSET [10]: a frame through the renderer, the simulation read
     before and after */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.beneFade > 0 || q.beneLit > 0);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    const s0 = simSnap(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx; vctx = "a drawn frame";
    let threw = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; vctx = vc0; }
    const d = firstDiff(s0, simSnap(m));
    if (threw) fail(10, "a drawn frame threw: " + threw);
    else if (dr) fail(10, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(10, "a drawn frame changed the simulation: " + d);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };

  const foes = foeList.length ? foeList : AC.WEAPONS.map(w => w.id).filter(i => i !== "aureole");
  const T = { casts: 0, frames: 0, inFrames: 0, smite: 0, bless: 0, foeStk: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, casts = 0;
  for (const side of sides) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "aureole", sd) : new AC.Match("aureole", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    F = { m, me, foe: side ? m.a : m.b };
    PM = null;
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    try {
      while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
      /* [9]-[10] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
      if ((S6V || S6P) && m.over){
        const open = !!me.ultHalo, lit = me.beneFade > 0, o9 = (n.x9 || 0);
        tail = true; vctx = "the verdict";
        try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); if (drawn) drawFrame(m, steps + i + 1); } }
        finally { tail = false; vctx = "a step"; }
        if (S6V && (n.x9 || 0) === o9) inc(open ? "verdictQuietOpen" : "verdictQuiet");
        if (S6P && me.haloTally){
          if (me.beneFade !== 0 || me.beneLit !== 0)
            fail(10, `after 2 s of the verdict the ring at ${me.beneFade}, lit ${me.beneLit}${open ? " -- the window the sim left open" : ""}`);
          else inc(lit ? (open ? "endGoneOpen" : "endGoneLit") : "endGoneOk");
        }
      }
    } finally { F = null; }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.haloTally) for (const k in T) T[k] += me.haloTally[k];
  }
  P.tickHalo = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.tickFire = oLoose; P.resolveHit = oResolve;
  P.step = oStep; P.tickStatus = oStatus; P.beat = oBeat;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
            for (const k of OTHER) P[k] = oOther[k]; }
  if (S6P) P.tickBenediction = oBene;
  const w = AC.WEAPONS.find(x => x.id === "aureole"), u = w.ult;
  const blk = { charge: u.charge, dur: u.dur, haloR: u.haloR, tickCd: u.tickCd, smite: u.smite, blessCd: u.blessCd,
                bless: u.bless, kind: u.kind, dmg: u.dmg, heal: u.heal, blade: w.dmg };
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, u: blk,
           s6v: S6V, s6p: S6P, other: OTHER };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickHalo === 'function'"):
        raise SystemExit("no tickHalo in this build -- not a halo link (stage 2+)")
    seeds = [a.seed0 + a.seedstep * i for i in range(a.seeds)]
    foes = [f for f in a.foes.split(",") if f]
    R = page.evaluate(JS, [seeds, foes, [0, 1] if a.sides == "AB" else [0], a.drawn])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
print(f"\nBENEDICTION (HALO) PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Aureole {'both sides' if a.sides == 'AB' else 'side A'} x {len(foes) or 'every'} foe(s) x {a.seeds} seeds, "
      f"seed0 {a.seed0} step {a.seedstep})   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"shots loosed: in windows {n.get('shotsIn',0)/R['fights']:.2f}, outside {n.get('shotsOut',0)/R['fights']:.2f} a fight   "
      f"Aureole win {R['win']:.1%}")
print(f"  per cast: smite {T['smite']/casts:.2f}  bless {T['bless']/casts:.2f}   foe inside {100*T['inFrames']/max(1,T['frames']):.1f}% "
      f"of window frames ({n.get('inRim',0)} inside frames by the rim only)   foe smite stacks on a window frame "
      f"{T['foeStk']/max(1,T['frames']):.2f}")
print(f"  the bow's fire rebuilt: {n.get('fireInOk',0)} frames in windows, {n.get('fireOutOk',0)} outside, "
      f"{n.get('fireSkipOk',0)} skipped; asked once on {n.get('fireStepOk',0)} unfrozen steps; the channel's smite 1 on "
      f"{n.get('chanInOk',0)} blows in windows, {n.get('chanOutOk',0)} outside")
print(f"  the halo's clock: tickHalo asked once on {n.get('haloStepOk',0)} unfrozen steps (none on a frozen one), "
      f"{n.get('frames',0)} open-window frames; clock closes {n.get('clockCloses',0)}, death closes {n.get('deathCloses',0)}")
print(f"  her heal: {n.get('blessHealOk',0)} blessed tickStatus frames rebuilt exactly, {n.get('statusQuietOk',0)} unblessed "
      f"frames with no heal; fatal smite ticks on her foe credited to her side: {n.get('fatalSmiteOk',0)}")
print(f"  FREEZE CENSUS {100*frozen:.1f}% of window steps frozen   a clock window lasts "
      f"{n.get('winMT',0)/max(1,n.get('winMTn',0)):.2f}s of match time ({U['dur']}s on the window clock)")
design = (U["dur"] == 8 and U["haloR"] == 150 and U["tickCd"] == 0.5 and U["smite"] == 1 and U["blessCd"] == 0.8
          and U["bless"] in (0, 1) and U["kind"] == "halo" and U.get("dmg") is None and U.get("heal") is None)
checks = [
    (1, "the window: dur on the window clock (tickHalo once on every unfrozen step, never on a frozen one; dt a call), closes on its clock or either death; only Aureole's",
        n.get("clockCloses", 0) > 0 and n.get("deathCloses", 0) > 0 and n.get("frames", 0) > 0 and n.get("haloStepOk", 0) > 0),
    (2, "inside iff the foe's centre is strictly within haloR + R of hers, rebuilt on every window frame",
        n.get("inOk", 0) > 0 and n.get("outOk", 0) > 0 and n.get("inRim", 0) > 0),
    (3, "the smite: every tickCd while inside (cd rebuilt, through the whole window): apply('smite', smite, side letter) on the foe only, stacks and clock the engine's",
        n.get("smiteOk", 0) > 0 and n.get("smiteCdOk", 0) > 0 and n.get("smiteWaitOk", 0) > 0 and n.get("smiteOutOk", 0) > 0),
    (4, "the blessing: every blessCd while a foe is inside (bcd rebuilt): apply('blessing', bless, side letter) on her only (none at bless 0); her only heal",
        ((n.get("blessOk", 0) > 0 and n.get("blessCdOk", 0) > 0 and n.get("blessWaitOk", 0) > 0 and n.get("blessOutOk", 0) > 0
          and n.get("blessHealOk", 0) > 0) if U["bless"] else n.get("bless0Ok", 0) > 0)
        and n.get("statusQuietOk", 0) > 0),
    (5, "nothing else: no hurt, no hp or ward change, no move, no push, no stop, no beat, no rng, no shot, no other status",
        n.get("calls", 0) > 0),
    (6, "no arrows through the halo: the bow's spin, its fire (asked once a step; cadence rebuilt), every blow's damage and its channel smite 1, in the window and out",
        all(n.get(k, 0) > 0 for k in ("spinInOk", "spinOutOk", "blowInOk", "blowOutOk", "chanInOk", "chanOutOk",
                                      "shotsIn", "fireInOk", "fireOutOk", "fireStepOk"))),
    (7, "the beam is out: a cast spawns no shot, hurts, heals or applies nothing, opens {t 0, dur, cd 0, bcd 0}, never on an open window; the block is the design's",
        n.get("castOk", 0) > 0 and design),
    (8, "a smite tick that kills her foe files its fatal beat for her side (the side letter)",
        n.get("fatalSmiteOk", 0) > 0),
]
g = lambda k: n.get(k, 0)
if R["s6v"]:
    print(f"  stage 6 voices: {g('castVoiceOk')} casts each one cast voice (of {T['casts']}); entries: {g('enterOk')} voiced "
          f"(an inside tick after an outside one), {g('firstInQuiet')} windows opened with the foe inside and no entry, "
          f"{g('stayQuiet')} inside ticks after inside ticks silent, {g('outQuiet')} outside ticks silent; {g('chimeOk')} "
          f"blessings each one heal chime (of {T['bless']}); closes: {g('closeClockOk')} by the clock voiced (of "
          f"{g('clockCloses')}), {g('closeDeathQuiet')} by a death silent; silent through 2 s of the verdict: "
          f"{g('verdictQuietOpen')} fights with the window open, {g('verdictQuiet')} with it shut; the run's own: "
          f"{g('v_aureole')} cast voices, {g('v_aureole-enter')} entries, {g('v_aureole-close')} close voices, {g('v_chime')} "
          f"chimes in the halo, {g('v_chimeOther')} other relics' chimes in their tickers ({', '.join(R['other'])})")
    checks.append((9, "stage 6 voices: one cast voice a cast (in fireUlt); the entry on an inside tick after an outside tick "
                      "of the same window and never on a window's first; one heal chime a blessing (n = her blessing); the "
                      "close voice on a clock close with both alive and never on a death; none in the picture, a drawn frame "
                      "or the verdict; every one accounted for",
                   g("castVoiceOk") == T["casts"] > 0 and g("enterOk") > 0 and g("v_aureole-enter") == g("enterOk")
                   and g("chimeOk") == T["bless"] > 0 and g("v_chime") == T["bless"] and g("v_aureole") == T["casts"]
                   and g("closeClockOk") == g("clockCloses") > 0 and g("v_aureole-close") == g("closeClockOk")
                   and g("closeDeathQuiet") > 0 and g("firstInQuiet") > 0 and g("stayQuiet") > 0))
if R["s6p"]:
    print(f"  stage 6 picture: tickBenediction {g('beneCalls')} calls, {g('beneClean')} writing nothing of the simulation's, "
          f"drawing no RNG and playing nothing; the ring up on {g('upOk')} calls in an open window ({g('picCasts')} casts), "
          f"its growth clock exact; closes {g('picCloseClock')} by the clock, {g('picCloseDeath')} on Aureole's death and "
          f"{g('picCloseFoeDeath')} on the foe's (in the kill flight), {g('picCloseOver') + g('picCloseOverOpen')} at `over` "
          f"({g('picCloseOverOpen')} of them with the sim's window still open), {g('picClosedOk')} out in 0.6 of its clock "
          f"(0.3 s); inside: {g('picInOk')} ticked inside, {g('picInHeldOk')} held inside between ticks, {g('picOutOk')} outside "
          f"window calls ({g('heldStopIn')} held inside and {g('heldStopOut')} outside through a hit stop); brightening: "
          f"{g('litUp')} rising, {g('litFull')} full, {g('litDown')} falling; tags: SMITE {g('tagSOk')} (+{g('smiteUntagged')} "
          f"smites inside a tagged stretch), BLESSING {g('tagBOk')} (+{g('blessUntagged')}); after 2 s of the verdict the "
          f"picture gone in {g('endGoneOk') + g('endGoneLit') + g('endGoneOpen')} fights, {g('endGoneLit') + g('endGoneOpen')} "
          f"of them lit at `over` ({g('endGoneOpen')} with the sim's window still open)")
    checks.append((10, "stage 6 picture: tickBenediction writes nothing of the simulation's, draws no RNG, plays nothing; the "
                       "ring up while the window is open and a 0.3 s close at any close; inside the ticker's own answer; "
                       "the brightening rebuilt; SMITE / BLESSING on each stretch's first; gone after the verdict"
                       + ("; the drawn subset clean" if g("drawnFights") else ""),
                   g("beneCalls") > 0 and g("beneClean") == g("beneCalls") and g("upOk") > 0 and g("picCloseClock") > 0
                   and g("picClosedOk") > 0 and g("picInOk") > 0 and g("picOutOk") > 0 and g("heldStopIn") > 0
                   and g("litUp") > 0 and g("litFull") > 0 and g("litDown") > 0 and g("tagSOk") > 0 and g("tagBOk") > 0
                   and g("smiteUntagged") > 0 and g("endGoneOpen") + g("endGoneLit") > 0
                   and (g("drawOk") > 0 if g("drawnFights") else True)))
if g("drawnFights"):
    print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 60th "
          f"otherwise): {g('drawOk')} frames clean, {g('drawPic')} with the picture up ({g('drawPicStop')} in a hit stop), "
          f"{g('drawVerdict')} in the verdict")
    if not R["s6p"]:
        checks.append((10, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                           "the simulation", g("drawOk") > 0))
if not (R["s6v"] or R["s6p"]):
    print("  stage 6: not on this link (no entry arm in the synth, no tickBenediction) -- [9]-[10] not run")
if not design:
    bad.setdefault("7", []).append(f"the ult block {U} is not the design's")
    n["x7"] = n.get("x7", 0) + 1
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
