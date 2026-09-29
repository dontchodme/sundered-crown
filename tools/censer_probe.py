#!/usr/bin/env python
"""CONSECRATION'S PROBE -- one check per sentence of v78 §1 / §4, read INSIDE the hooks.

    python censer_probe.py --game <sc-censer-ground.html | -consecration... >

Wraps `step`, `tickHolyGround`, `fireUlt`, `tickCharge`, `tickWeapon`,
`tickHits`, `resolveHit` and `tickStatus` on the Match prototype, and puts an
accessor on Censer's `hp` for the length of each fight. Plays Censer against
every other relic from both sides and prints N/N. The design's numbers are
PINNED FROM THE BUILDER (`censer_build.ULT`), never read off the row under
test, so a row that drifts fails; the blessing is 0 on stage 2 and the
builder's on stage 3 on, and the blade is the shipped 28.77 or the builder's
stage-5 BLADE.

THE GROUND IS REBUILT, NOT READ. For every window frame the probe takes the
discs, both balls and both cooldowns as they stood when the ticker was called,
ages the discs on the ground's clock, and says which discs are left, whether
the foe must be smitten and whether the caster must be blessed. It then
compares that with what the ticker did.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration" -- THE WINDOW ON THE WINDOW CLOCK: a window that is not
      `dur` long on the window tickers' clock (a live step moves its clock by
      exactly dt; a frozen step -- hit stop, latch, split hold -- leaves the
      window, the ground and the ground's clock `holyT` exactly as they were),
      that outlives either death or closes early; the ticker not run exactly
      once on a live step or run on a frozen one; `holyT` not moved by
      exactly dt on a live step; a Censer cast under a standing window; any
      relic but Censer carrying `ultHoly` or `holyTally`
  [2] "every blow the hammer lands consecrates the ground where it landed":
      a Censer blow (its own blade, `mul` undefined) landed while the window
      is open that does not push exactly one disc {x, y, t0, side} at the
      struck ball's position at the hit, `t0` the ground's clock, `side` the
      caster's; a blow outside the window that pushes one; a disc that
      appears anywhere else
  [3] "a circle of holy ground that lasts" (8s; "does not move"; "the hall's
      close does not clip it"): a disc that moves or changes, that goes
      before `holyT - t0` reaches `groundLife` or outlives it, or that
      anything but its age removes
  [4] "An enemy standing on holy ground is smitten": on a window frame, the
      foe's centre within groundR + R of one of the caster's live discs and
      the cooldown clear, and no smite +`smite` exactly as apply("smite",
      smite, side) leaves it (stacks to the cap, t the status's dur, src the
      side letter); a smite with the foe off the ground or the cooldown
      running; the cooldown not `tickCd` after a smite, or not run down by
      dt on every window frame
  [5] "Censer standing on holy ground is healed": the caster's CENTRE within
      groundR of one of its live discs and its cooldown clear (bless > 0),
      and no blessing +`bless` exactly as apply("blessing", bless, side)
      leaves it; a blessing off the ground, under the cooldown or at bless 0;
      AND THE BLESSING IS THE HEAL: Censer's hp rising anywhere but in its
      own status tick (by at most hps x stacks x dt there) -- read by an
      accessor on its hp; the ticker's own frames are [6]'s
  [6] nothing else on a ground frame ("No damage, no knock, no beat"): a
      hurt, a beat, an rng draw or a hit stop in the ticker; A WHOLE-STATE
      DIFF of both fighters (every own field; the status table key by key),
      the match (every array by length, identity and content; a Twinshade
      shade field by field) and the shared tables STATUS, CONFIG and
      AFFINITIES, before and after the ticker. Only what another check
      rebuilds may move: the caster's ultHoly, holyTally and blessing ([1]
      [4] [5]), the foe's smite ([4]), the match's holyGround and holyT
      ([1] [3]). Once a fight: WEAPONS, SHAPES and the three against the
      run's start
  [7] "the nova is out": a Censer cast that does not open exactly {t 0, dur,
      cd 0, bcd 0}, or that writes ANYTHING ELSE after the engine's shared
      prologue (snapshotted when the prologue assigns `ultFx`, its last
      statement before the kind branches): only the caster's ultHoly and a
      holyTally whose casts went up by one may move
  [8] "the hammer swings as ever": Censer's turn on every live step (spin x
      spinMul x dt, locked while stunned), its blade segment and hit test in
      tickHits (the hit cooldown, the stun, R + width/2), and every blow it
      lands rebuilt from the captured crit and jitter draws: the damage, the
      knock, the foe's hitstun, the hit stop, the onHit smite -- in the
      window and out
  [9] the charge (Rick's batch ruling: the lab's 16 on the game's clock):
      Censer's charge not moving by exactly dt on each of its charge ticks,
      or a cast that does not come exactly when it reaches `charge`

COUNTED, NOT CHECKED: blows landed on a Twinshade shade in the window (their
disc is at the shade, reading 1); discs still alive when the next window
opens (reading 2); the freeze census of window steps.

STAGE 6 (the picture and the voice, the builder's readings 13-19), each check
run only where the link carries it -- the voices detected by the disc bell's
arm in `AC.SFX.play.toString()`, the picture by `tickConsecration` on the
Match -- so the same probe still gates stages 2-5 at 9/9, every line as
before. Once a fight is over the probe steps 2 s more of the verdict (the
step's `over` path: only the presentation clock runs) for these two checks
alone; [1]-[9] read none of those steps.
  [10] THE VOICES fire exactly on their events and nowhere else (design §4
      "Sound"). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Censer's two arms ("ult" with w "censer" / "censer-disc") and
      the heal chime ("spark" with collect) are read; a ward's shatter --
      which plays its own crit HIT voice inside hurt() -- is not one of them.
      Evidence: a Censer cast playing anything but exactly one cast voice (w
      "censer") inside fireUlt, or the cast voice anywhere else (a foe's
      cast included); a Censer blow that plants a disc and does not play
      exactly one disc bell, with n the caster's discs standing after the
      push, or a bell from any other blow or anywhere else; a ground ticker
      call that plays anything but one heal chime per blessing it laid, with
      n Censer's blessing after it -- so NO VOICE ON A CLOSE, by the clock or
      by a death (the design names no close voice) and nothing on a smite
      tick ("nothing new"); a heal chime anywhere but the ground's ticker and
      the two other relics' spark tickers (`tickSun`, `tickSparks`); any of
      them in the picture's hook or in the verdict. Every one of the run is
      accounted for: cast voices = casts, bells = discs, chimes = blessings.
  [11] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickConsecration`
      (tickPresentation, the picture's one call on the step path) is wrapped:
      evidence is any change across it to either fighter (every own number,
      flag and string but its `cons*` fields, every array's length, every
      status, the window, the tally, the blade cooldowns, the weapon row and
      its ult) or to the match (every own number, flag and string, every
      array's length but `tags`, every disc's x, y, t0 and side), an RNG draw
      or a voice. And the picture as declared (readings 13-15), REBUILT from
      the tally the way [4] rebuilds the smite: the head not lit (`consFade`
      1) in an open window (`ultHoly`, the match live, the caster alive), lit
      with none, or a close that is not a fade to 0 over exactly 0.6 of its
      clock (0.3 s) -- by the clock, on a death or AT THE KILL; the picture's
      discs not the caster's discs of `m.holyGround`, by identity and in
      order, or a disc's bloom clock not the presentation clock since it
      appeared; "on the ground" not `tickHolyGround`'s own answer (a step the
      window ticked is a foe-on step iff `foeOn` rose with it, a Censer-on
      step iff `selfOn` did; through a hit stop the last answer holds); a
      smite tick without its flash; a SMITE tag not exactly on the first
      smite of each on-ground stretch (at the foe, with its count), a
      BLESSING tag not exactly on the first blessing of each (on Censer,
      with its count), or any other tag; the foe carrying any of it; and the
      head lit or the ground drawn after 2 s of the verdict.
  --drawn N (default 6; 0 = off): on the FIRST seed, both sides, every foe,
      each fight is also drawn through the renderer (`AC.__draw`, the post
      chain off, 270x480) every Nth step while the picture shows and every
      60th otherwise, through the kill and the verdict. [11] fails a drawn
      frame that throws, draws the match's RNG or changes the simulation (the
      snapshot above); the renderer's own memos (an underscore key of SHAPES
      a draw writes) are taken into [6]'s once-a-fight table check, and
      every other write still fails it. It runs on any link, so the base's
      draws are its control.
"""
from __future__ import annotations
import argparse, importlib.util, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
_spec = importlib.util.spec_from_file_location("censer_build", HERE / "censer_build.py")
CB = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(CB)

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=109001)
ap.add_argument("--json", default=None)
# THE LAB'S FIELD, for a like-for-like mechanism column: --foes <the design's 33> --sides A
# --seed0 2207 --seeds 20 --seedstep 11 plays exactly the fights ult_overlay's arm SHIP plays.
ap.add_argument("--foes", default="", help="comma list; default every other relic")
ap.add_argument("--sides", default="AB", choices=["AB", "A", "B"])
ap.add_argument("--seedstep", type=int, default=13)
ap.add_argument("--drawn", type=int, default=6, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()

PIN = dict(CB.ULT)
PIN["blades"] = [28.77] + ([CB.BLADE] if CB.BLADE is not None else [])

JS = r"""([seeds, foeList, sides, PIN, drawEvery]) => {
  const ID = "censer";
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR, I = C.impact, CH = C.chaos;
  const ST = AC.STATUS, SM = ST.smite, BL = ST.blessing;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  /* the engine's segDist, character for character */
  const segd = (ax, ay, bx, by, px, py) => { const dx = bx - ax, dy = by - ay, len2 = dx*dx + dy*dy;
    let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2; t = t < 0 ? 0 : t > 1 ? 1 : t;
    const cx = ax + dx * t, cy = ay + dy * t; return { d: Math.hypot(px - cx, py - cy), x: cx, y: cy }; };
  /* THE PRICED STATUSES, pinned: the builder asserts these on the base */
  if (SM.maxStacks !== 4 || SM.dur !== 3.2 || BL.maxStacks !== 5 || BL.dur !== 6.0 || BL.hps !== 1.2)
    fail(4, "STATUS.smite / STATUS.blessing are not the ones the lab priced");
  /* Fighter.apply(key, k, src), rebuilt from the engine's own lines (smite
     and blessing: the global cap, no curse pool). */
  const applied = (s0, def, k, src) => { const c = Object.assign({}, s0 || { stacks: 0, t: 0 });
    if (c.stacks < def.maxStacks) c.stacks = Math.min(def.maxStacks, c.stacks + k);
    c.t = def.dur; if (src) c.src = src; return c; };
  /* N steps of dt, float-accumulated, to reach the charge */
  const oTick = P.tickHolyGround, oFire = P.fireUlt, oStep = P.step, oCharge = P.tickCharge,
        oWeapon = P.tickWeapon, oHits = P.tickHits, oResolve = P.resolveHit, oStatus = P.tickStatus;

  /* ---- THE WHOLE-STATE SNAPSHOT (v107's, the status table split key by key) ---- */
  let curM = null, FP = null;
  const TAGS = [[AC.Match.prototype, function(){ return "<match>"; }],
                [Map.prototype, function(){ return { "<Map>": [...this] }; }],
                [Set.prototype, function(){ return { "<Set>": [...this] }; }]];
  for (const [pr, fn] of TAGS){ if (Object.prototype.hasOwnProperty.call(pr, "toJSON")) throw new Error("toJSON already set"); pr.toJSON = fn; }
  const setM = m => { curM = m;
    if (m && !FP){ FP = Object.getPrototypeOf(m.a);
      if (Object.prototype.hasOwnProperty.call(FP, "toJSON")) throw new Error("Fighter toJSON already set");
      FP.toJSON = function(){ return !curM ? "<fighter ?>" : this === curM.a ? "<fighter a>" : this === curM.b ? "<fighter b>"
                                    : `<shade ${curM.shades ? curM.shades.indexOf(this) : -1}>`; };
      TAGS.push([FP, FP.toJSON]); } };
  const js = v => { if (v === undefined) return "undefined";
    try { return JSON.stringify(v); }
    catch (e) { fail(6, `the probe could not serialise a field (${e.message}) -- a field it cannot read is not a pass`); return "<unread>"; } };
  const SKIPF = new Set(["w", "aff", "status"]);
  const snapF = f => { const o = new Map();
    for (const k of Object.keys(f)){ if (SKIPF.has(k)) continue; const v = f[k];
      o.set(k, (v === null || typeof v !== "object") ? v : "J" + js(v)); }
    for (const k of Object.keys(f.status)) o.set("status." + k, "J" + js(f.status[k]));
    return o; };
  const snapM = m => { const o = new Map();
    for (const k of Object.keys(m)){ if (k === "a" || k === "b" || k === "rng") continue;
      const v = m[k];
      if (typeof v === "function") continue;
      if (Array.isArray(v)){
        o.set(k, v.slice());
        o.set(k + "=", "J" + js(v));
        for (let i = 0; i < v.length; i++){ const e = v[i];
          if (e !== null && typeof e === "object" && Object.getPrototypeOf(e) === FP)
            for (const [fk, fv] of snapF(e)) o.set(`${k}[${i}].${fk}`, fv); } }
      else o.set(k, (v === null || typeof v !== "object") ? v : "J" + js(v)); }
    return o; };
  /* SHAPES is read key by key (stage 6's drawn subset: a draw's own memo
     writes to an underscore key are taken into the check's start, and any
     other write still fails it) */
  const snapG = all => { const o = new Map([["STATUS", js(AC.STATUS)], ["CONFIG", js(AC.CONFIG)], ["AFFINITIES", js(AC.AFFINITIES)]]);
    if (all){ o.set("WEAPONS", js(AC.WEAPONS)); for (const k of Object.keys(AC.SHAPES)) o.set("SHAPES." + k, js(AC.SHAPES[k])); }
    return o; };
  const diffMap = (A, B) => { const out = [];
    for (const [k, v] of A){ if (!B.has(k)){ out.push(k); continue; } const w = B.get(k);
      if (Array.isArray(v)){ if (!Array.isArray(w) || w.length !== v.length || v.some((x, i) => x !== w[i])) out.push(k); }
      else if (!Object.is(v, w)) out.push(k); }
    for (const k of B.keys()) if (!A.has(k)) out.push(k);
    return out; };

  /* ---- PER-FIGHT STATE ---- */
  let F = null;          // { me, foe, m, model: [discs], planted: WeakMap disc -> {J, cast}, cast, stepsLive, ... }
  let ctx = null;        // "status" | "ticker" | null: where Censer's hp may rise
  let statusRise = 0;
  let tickCalls = 0, frozenNow = false, stepPushes = null;
  let WINLEN = null;

  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: the disc bell's arm in the
     synth [10], `tickConsecration` on the match [11]. A link without them
     runs [1]-[9] only. ---- */
  const S6V = /censer-disc/.test(AC.SFX.play.toString()), S6P = typeof P.tickConsecration === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oCons = P.tickConsecration, oSun = P.tickSun, oSparks = P.tickSparks;
  let vctx = "a step", vrec = null, tail = false;
  const isChime = (kind, q) => kind === "spark" && !!q && q.collect === true;
  const isOurs = (kind, q) => kind === "ult" && !!q && (q.w === "censer" || q.w === "censer-disc");
  if (S6V) AC.SFX.play = function(kind, q){
    if (F){
      if (vrec) vrec.push([kind, q ? Object.assign({}, q) : q]);
      const ours = isOurs(kind, q), chime = isChime(kind, q);
      if (ours || chime){
        const where = ours ? (q.w === "censer" ? "cast" : "blow") : null;
        const ok = ours ? vctx === where : (vctx === "ground" || vctx === "another relic's sparks");
        if (!ok) fail(10, `${ours ? "the " + q.w + " voice" : "the heal chime (spark collect)"} played in ${vctx}`);
        inc(ours ? "v_" + q.w : vctx === "ground" ? "v_chime" : "v_chimeOther");
      }
    }
    return oPlay.call(this, kind, q);
  };
  /* the two other relics' spark tickers may play the chime (theirs) */
  const ctxWrap = (fn, name) => function(){
    if (!F || F.m !== this) return fn.apply(this, arguments);
    const v0 = vctx; vctx = name;
    try { return fn.apply(this, arguments); } finally { vctx = v0; } };
  if (S6V && oSun) P.tickSun = ctxWrap(oSun, "another relic's sparks");
  if (S6V && oSparks) P.tickSparks = ctxWrap(oSparks, "another relic's sparks");
  /* [11] the simulation's state, as one array in a fixed key order: both
     fighters' own numbers, flags and strings (their `cons*` fields aside) and
     array lengths, statuses, the window, the tally, the cooldowns, the weapon
     row and its ult; the match's own numbers, flags and strings and every
     array's length (`tags` aside: the SMITE and BLESSING tags are the
     picture's to file), and every disc's x, y, t0 and side */
  const same = (x, y) => x === y || (x !== x && y !== y);
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 99 && k.startsWith("cons")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      for (const k in f.status){ const s = f.status[k]; o.push(k, s.stacks, s.t, s.src); }
      const Z = f.ultHoly;
      if (Z) o.push("Z", Z.t, Z.dur, Z.cd, Z.bcd); else o.push("Z-");
      const T = f.holyTally;
      if (T) for (const k of Object.keys(T)) o.push(k, T[k]); else o.push("T-");
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
    for (const d of m.holyGround) o.push(d.x, d.y, d.t0, d.side);
    return o;
  };
  const firstDiff = (s0, s1) => {
    if (s0.length !== s1.length) return `the shape ${s0.length} -> ${s1.length} fields`;
    for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i]))
      return `${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}`;
    return null; };
  let PM = null;   // the picture, rebuilt: per fight

  /* THE STEP: the window clock, the frozen steps, the ground's list between
     steps. */
  P.step = function(dt){
    if (!F || F.m !== this) return oStep.call(this, dt);
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [10]-[11] alone */
    if (tail) return oStep.call(this, dt);
    const frozen = !!(this.hitStop > 0 || this.latch || this.splitHold), over0 = this.over, live = !over0 && !frozen;
    const winJ = [this.a, this.b].map(f => [f.ultHoly, js(f.ultHoly)]);
    const G0 = this.holyGround.slice(), GJ0 = js(this.holyGround), hT0 = this.holyT;
    for (const f of [this.a, this.b]) if (f.ultHoly){ if (frozen && !over0) inc("winFrozen"); else if (live) inc("winLive"); }
    tickCalls = 0; frozenNow = frozen && !over0; stepPushes = [];
    const r = oStep.call(this, dt);
    frozenNow = false;
    if (live){
      if (tickCalls !== 1) fail(1, `the ground's ticker ran ${tickCalls} times on a live step`);
      else inc("liveTicks");
    } else if (!over0){
      if (tickCalls !== 0) fail(1, "the ground's ticker ran on a frozen step (the lab's clock, not the window's)");
      [this.a, this.b].forEach((f, i) => { if (f.ultHoly !== winJ[i][0] || js(f.ultHoly) !== winJ[i][1]) fail(1, "a window moved on a frozen step"); });
      if (this.holyT !== hT0 || js(this.holyGround) !== GJ0 || this.holyGround.length !== G0.length
          || this.holyGround.some((d, i) => d !== G0[i])) fail(1, "the ground or its clock moved on a frozen step");
      else inc("frozenOk");
    }
    /* THE GROUND'S LIST: the model (the ticker's purge, then the blows'
       plants, in order) against the engine's, by identity. */
    const E = this.holyGround, M = F.model;
    const extra = E.filter(d => !M.includes(d) && !F.planted.has(d)), gone = M.filter(d => !E.includes(d));
    if (extra.length) fail(2, `${extra.length} disc(s) appeared outside a blow`);
    if (gone.length) fail(3, `${gone.length} disc(s) removed by something other than their age`);
    if (!extra.length && !gone.length && E.length === M.length && E.some((d, i) => d !== M[i])) fail(3, "the ground was reordered");
    if (extra.length || gone.length || E.length !== M.length) F.model = E.slice();
    /* discs do not move, and do not change */
    for (const d of E){ const p = F.planted.get(d); if (p && js(d) !== p.J) { fail(3, "a disc moved or changed"); p.J = js(d); } }
    return r;
  };

  /* THE CHARGE [9]: exactly dt a charge tick, the cast exactly at `charge`. */
  P.tickCharge = function(f, foe, dt){
    if (!F || F.m !== this || f !== F.me) return oCharge.call(this, f, foe, dt);
    const c0 = f.charge, alive = f.alive && !this.over, casts0 = F.casts;
    const r = oCharge.call(this, f, foe, dt);
    if (!alive) return r;
    const want = c0 + dt, cast = F.casts > casts0;
    if (f.w.ult.charge !== PIN.charge) fail(9, `the row's charge is ${f.w.ult.charge}, the builder's ${PIN.charge}`);
    if (cast){
      if (!(want >= PIN.charge)) fail(9, `a cast at charge ${want}, want ${PIN.charge}`);
      else if (f.charge !== 0) fail(9, "the charge not spent at the cast");
      else inc("castOnCharge");
    } else if (want >= PIN.charge) fail(9, `charge ${want} reached ${PIN.charge} and no cast`);
    else if (f.charge !== want) fail(9, `charge ${c0} -> ${f.charge}, want +dt`);
    else inc("chargeOk");
    return r;
  };

  /* THE CAST [7] */
  P.fireUlt = function(f, foe){
    if (!F || F.m !== this || f !== F.me) return oFire.call(this, f, foe);
    if (f.ultHoly) fail(1, "a cast under a standing window");
    F.casts++;
    /* discs of this caster still alive at the cast: they act in this window (reading 2) */
    const side = f === this.a ? "a" : "b";
    const carried = this.holyGround.filter(d => d.side === side).length;
    if (carried){ inc("castsWithGround"); inc("discsCarried", carried); }
    setM(this);
    const M = this;
    let cur = this.ultFx, sets = 0, S0 = null;
    Object.defineProperty(this, "ultFx", { configurable: true, enumerable: true, get(){ return cur; },
      set(v){ cur = v; sets++;
              if (sets === 1) S0 = { a: snapF(M.a), b: snapF(M.b), m: snapM(M), g: snapG(false),
                                     tally: f.holyTally ? Object.assign({}, f.holyTally) : null }; } });
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "cast"; vrec = [];
    try { r = oFire.call(this, f, foe); }
    finally { Object.defineProperty(this, "ultFx", { value: cur, writable: true, enumerable: true, configurable: true });
              heard = vrec; vctx = vc0; vrec = vr0; }
    /* [10] THE CAST'S VOICE: exactly one, inside fireUlt (the prologue's `SFX.play("ult", { w: f.w.id })`) */
    if (S6V){
      const mine = heard.filter(c => isOurs(c[0], c[1]) || isChime(c[0], c[1]));
      if (mine.length !== 1 || mine[0][1].w !== "censer") fail(10, `a Censer cast played ${JSON.stringify(mine)}, want one cast voice`);
      else inc("castVoiceOk");
    }
    const Z = f.ultHoly, T0 = S0 && S0.tally, T1 = f.holyTally;
    const tallyOk = T1 && Object.keys(T1).every(k => T1[k] === (k === "casts" ? (T0 ? T0.casts : 0) + 1 : (T0 ? T0[k] : 0)));
    if (!S0 || sets !== 1) fail(7, `the cast's prologue assigned ultFx ${sets} times (read at the first)`);
    else if (!Z || js(Z) !== js({ t: 0, dur: f.w.ult.dur, cd: 0, bcd: 0 })) fail(7, `the cast opened ${JSON.stringify(Z)}`);
    else if (!tallyOk) fail(7, `the tally ${JSON.stringify(T0)} -> ${JSON.stringify(T1)}`);
    else {
      const bad2 = [], key = f === this.a ? "a" : "b";
      for (const k of ["a", "b"]){ const Fk = this[k];
        for (const d of diffMap(S0[k], snapF(Fk)))
          if (!(k === key && (d === "ultHoly" || d === "holyTally"))) bad2.push(`${k === key ? "the caster" : "the foe"}'s ${d}`); }
      for (const d of diffMap(S0.m, snapM(this))) bad2.push(`the match's ${d}`);
      for (const d of diffMap(S0.g, snapG(false))) bad2.push(`the shared table ${d}`);
      if (bad2.length) fail(7, `the cast also wrote ${bad2.join(", ")}`);
      else inc("castOk");
    }
    F.winStart = F.liveSteps;
    return r;
  };

  /* THE TURN [8]: spin x spinMul x dt, locked while stunned. */
  P.tickWeapon = function(f, foe, dt){
    if (!F || F.m !== this || f !== F.me) return oWeapon.call(this, f, foe, dt);
    const th0 = f.theta, stun0 = f.stun;
    const sm = Math.max(0.15, this.actMods.spin * (1 + ST.entangle.spin * f.stacks("entangle"))
                              * (f.desperate ? C.desperation.spin : 1));
    const r = oWeapon.call(this, f, foe, dt);
    const want = stun0 > 0 ? th0 : th0 + f.w.spin * sm * dt * f.spinDir;
    if (f.theta !== want) fail(8, `${f.ultHoly ? "IN" : "out of"} the window: theta ${th0} -> ${f.theta}, want ${want}`);
    else inc(f.ultHoly ? "turnInOk" : "turnOutOk");
    if (f.reachMul !== 1) fail(8, `reachMul ${f.reachMul}`);
    return r;
  };

  /* THE HIT TEST [8]: the blade segment, the cooldown, the stun, R + w/2. */
  let hitCalls = null;
  P.tickHits = function(self, foe, dt, cool){
    if (!F || F.m !== this || self !== F.me || foe !== F.foe) return oHits.call(this, self, foe, dt, cool);
    const early = (this.killFlight && self.hp <= 0) || !self.alive || !foe.alive;
    const reach = self.w.reach * this.actMods.reach * 1;
    const exp = [], cd0 = self.w.blades.map((_, i) => self.hitCd[i] || 0);
    if (!early) self.w.blades.forEach((off, i) => {
      const cd = Math.max(0, cd0[i] - (cool === false ? 0 : dt));
      if (cd > 0 || self.stun > 0) return;
      const a = self.theta + off * Math.PI * 2, ca = Math.cos(a), sa = Math.sin(a);
      const h = segd(self.x + ca * (R - 4), self.y + sa * (R - 4), self.x + ca * (R + reach), self.y + sa * (R + reach), foe.x, foe.y);
      if (h.d < R + self.w.width * 0.5) exp.push([h.x, h.y]); });
    hitCalls = [];
    const r = oHits.call(this, self, foe, dt, cool);
    const got = hitCalls; hitCalls = null;
    if (got.length !== exp.length || got.some((g, i) => g[0] !== exp[i][0] || g[1] !== exp[i][1]))
      fail(8, `the hit test: ${got.length} blow(s) at ${JSON.stringify(got)}, want ${JSON.stringify(exp)}`);
    else inc("hitTestOk");
    return r;
  };

  /* A BLOW [2] [8] */
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!F || F.m !== this || self !== F.me) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    if (hitCalls && mul === undefined) hitCalls.push([hx, hy]);
    const open = !!self.ultHoly, L0 = this.holyGround.length, fx = foe.x, fy = foe.y, T0 = self.holyTally ? self.holyTally.discs : 0;
    const d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    const pre = { dm: this.actMods.dmg * (self.desperate ? C.desperation.dmg : 1), dt: foe.dmgTakenMul(),
                  aegis: !!foe.ultAegis, echo: Math.round(foe.curseEcho()), sh: foe.shield,
                  vx: foe.vx, vy: foe.vy, kx: foe.x - self.x, ky: foe.y - self.y,
                  stun: foe.stun, stunDR: foe.stunDR, hs: this.hitStop, st: js(foe.status), stO: foe.status };
    const stBefore = JSON.parse(js(foe.status));
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "blow"; vrec = [];
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    /* [2] THE PLANT */
    const pushed = this.holyGround.slice(L0);
    /* [10] THE DISC'S BELL: one a disc planted, n the caster's discs standing
       after the push; none for any other blow. The blow's own voices (the
       hit, a ward shatter's crit hit inside hurt()) are not Censer's arms. */
    if (S6V){
      const bells = heard.filter(c => isOurs(c[0], c[1]) || isChime(c[0], c[1]));
      const side = self === this.a ? "a" : "b", standing = this.holyGround.filter(d => d.side === side).length;
      if (bells.length !== pushed.length || bells.some(c => c[1].w !== "censer-disc"))
        fail(10, `a blow that planted ${pushed.length} disc(s) played ${JSON.stringify(bells)}`);
      else if (bells.length && bells[0][1].n !== standing) fail(10, `the disc bell's n ${bells[0][1].n}, the caster's discs standing ${standing}`);
      else if (bells.length){ inc("bellOk"); inc("bellN" + Math.min(6, standing));
        if (!foe.alive || foe.hp <= 0) inc("bellOnKill"); }
      else inc("blowQuietOk");
    }
    if (self.hits - h0 === 1 && mul === undefined && open){
      const want = js({ x: fx, y: fy, t0: this.holyT, side: self === this.a ? "a" : "b" });
      if (pushed.length !== 1) fail(2, `a blow in the window pushed ${pushed.length} discs`);
      else if (js(pushed[0]) !== want) fail(2, `the disc ${js(pushed[0])}, want ${want}`);
      else if (!self.holyTally || self.holyTally.discs !== T0 + 1) fail(2, "the disc not counted");
      else {
        inc("plantOk"); if (foe !== F.foe) inc("shadeDiscs");
        F.model.push(pushed[0]); F.planted.set(pushed[0], { J: js(pushed[0]), cast: F.casts });
      }
    } else if (pushed.length) fail(2, `a blow ${open ? "that is not the hammer's own" : "outside the window"} pushed ${pushed.length} disc(s)`);
    else if (self.hits - h0 === 1 && mul === undefined) inc("noPlantOutOk");
    /* [8] THE BLOW, REBUILT */
    if (self.hits - h0 !== 1 || mul !== undefined) return r;
    if (open) F.bIn++; else F.bOut++;
    if (pre.aegis){ inc("blowExempt"); return r; }
    /* A BLOW'S DAMAGE IS AN INTEGER (rounded, plus the rounded echo), and
       `dealt` is a running float other paths add fractions to, so the
       difference is read to the nearest integer -- and a blow whose dealt
       is not within 1e-6 of one fails. (The first run read the raw
       difference and failed 2 of 4611 blows on a last-bit residue.) */
    const Draw = self.dealt - d0, D = Math.round(Draw), crit = self.crits > c0;
    if (Math.abs(Draw - D) > 1e-6) fail(8, `a blow dealt ${Draw}, not a whole number`);
    const raw = self.w.dmg * pre.dm * (1 + (draws[1] - 0.5) * CH.dmgJitter) * pre.dt;
    const wantD = Math.round(crit ? raw * CH.critMul : raw) + pre.echo;
    const fatal = foe.hp <= 0;
    const why = [];
    if (!PIN.blades.includes(self.w.dmg)) why.push(`blade ${self.w.dmg}`);
    if (draws.length < 2 || crit !== (draws[0] < CH.critChance)) why.push("the crit draw");
    if (Math.abs(D - wantD) > 1e-6) why.push(`dealt ${D}, want ${wantD}`);
    const kl = Math.hypot(pre.kx, pre.ky) || 1, power = C.combat.knock * (self.w.knockMul || 1) * (crit ? 1.5 : 1);
    if (foe.vx !== pre.vx + (pre.kx / kl) * power || foe.vy !== pre.vy + (pre.ky / kl) * power) why.push("the knock");
    if (!fatal){
      const rawS = Math.min(I.stunMax, I.stunBase + D * I.stunPerDmg), durS = rawS / (1 + I.stunDR * pre.stunDR);
      if (foe.stun !== Math.max(pre.stun, durS) || foe.stunDR !== pre.stunDR + 1) why.push("the hitstun");
    } else if (foe.stun !== pre.stun) why.push("hitstun on a kill");
    let stop = Math.min(I.stopMax, I.stopBase + D * I.stopPerDmg);
    if (crit) stop *= I.critStopMul;
    if (fatal) stop = I.killStop;
    const shattered = pre.sh > 0 && foe.shield <= 0;
    const wantHs = Math.max(pre.hs, shattered ? 0.10 : -Infinity, stop > 0 ? stop : -Infinity);
    if (this.hitStop !== wantHs) why.push(`hit stop ${this.hitStop}, want ${wantHs}`);
    const stWant = Object.assign({}, stBefore);
    if (shattered) delete stWant.ward;
    for (const [k, v] of Object.entries(self.w.onHit || {})) stWant[k] = applied(stWant[k], ST[k], v, undefined);
    if (js(foe.status) !== js(stWant)) why.push(`the foe's statuses ${js(foe.status)}, want ${js(stWant)}`);
    if (why.length) fail(8, `${open ? "IN" : "out of"} the window: ${why.join("; ")}`);
    else inc(open ? "blowInOk" : "blowOutOk");
    return r;
  };

  /* THE HEAL'S ONLY SOURCE [5]: Censer's status tick. */
  P.tickStatus = function(f, dt){
    if (!F || F.m !== this || f !== F.me) return oStatus.call(this, f, dt);
    const k0 = f.stacks("blessing"), prev = ctx;
    ctx = "status"; statusRise = 0;
    let r;
    try { r = oStatus.call(this, f, dt); } finally { ctx = prev; }
    if (statusRise > BL.hps * k0 * dt + 1e-9) fail(5, `the status tick healed ${statusRise}, the blessing's ${BL.hps * k0 * dt}`);
    else if (statusRise > 0) inc("blessHealOk");
    return r;
  };

  /* THE GROUND'S TICKER [1] [3] [4] [5] [6] */
  P.tickHolyGround = function(dt){
    if (!F || F.m !== this) return oTick.call(this, dt);
    tickCalls++;
    if (frozenNow) fail(1, "the ground's ticker ran on a frozen step (the lab's clock, not the window's)");
    F.liveSteps++;
    const hT0 = this.holyT, G0 = this.holyGround.slice();
    const pre = [];
    for (const f of [this.a, this.b]){
      if ((f.ultHoly || f.holyTally) && f.w.id !== ID) fail(1, `${f.w.id} carries the window`);
      const Z = f.ultHoly;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, side: f === this.a ? "a" : "b", t1: Z.t + dt, cd1: Z.cd - dt, bcd1: Z.bcd - dt,
                 x: f.x, y: f.y, fx: foe.x, fy: foe.y, fAlive: f.alive, foeAlive: foe.alive, u: f.w.ult,
                 T0: Object.assign({}, f.holyTally), sm0: foe.status.smite ? Object.assign({}, foe.status.smite) : null,
                 bl0: f.status.blessing ? Object.assign({}, f.status.blessing) : null,
                 smJ: js(foe.status.smite), blJ: js(f.status.blessing) });
    }
    setM(this);
    /* THE WHOLE STATE on a window frame; with no window open (the ground
       only ages) a compact read of both balls -- the ticker then has nothing
       to do but its clock and its purge, which [1] and [3] rebuild. */
    const full = pre.length > 0, st = {};
    const lite = f => js([f.x, f.y, f.vx, f.vy, f.hp, f.shield, f.shieldMax, f.stun, f.pin, f.charge, f.status, f.ultHoly, f.holyTally]);
    for (const k of ["a", "b"]) st[k] = { f: this[k], S: full ? snapF(this[k]) : lite(this[k]) };
    const M0 = full ? snapM(this) : null, GG0 = full ? snapG(false) : null, shJ = full ? null : js(this.shots);
    const hs0 = this.hitStop, calls = [], oHurt = this.hurt, oBeat = this.beat, oRng = this.rng;
    this.hurt = function(){ calls.push("hurt"); return oHurt.apply(this, arguments); };
    this.beat = function(){ calls.push("beat"); return oBeat.apply(this, arguments); };
    this.rng = function(){ calls.push("rng"); return oRng(); };
    const prev = ctx; ctx = "ticker";
    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "ground"; vrec = [];
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; ctx = prev; heard = vrec; vctx = vc0; vrec = vr0; }
    /* [10] THE GROUND'S VOICES: one heal chime a blessing laid (n Censer's
       blessing after it), and nothing else at all -- no voice on a close, by
       the clock or a death, and none on a smite tick */
    if (S6V){
      let want = 0, nWant = null, closing = null;
      for (const p of pre){ const d = p.f.holyTally.bless - p.T0.bless; want += d; if (d) nWant = p.f.stacks("blessing");
        if (!p.f.ultHoly) closing = (p.t1 >= p.Z.dur && p.fAlive && p.foeAlive) ? "clock" : "death"; }
      const chimes = heard.filter(c => isChime(c[0], c[1]));
      if (heard.length !== chimes.length || chimes.length !== want)
        fail(10, `the ground's ticker played ${JSON.stringify(heard)} for ${want} blessing(s)${closing ? " on a " + closing + " close" : ""}`);
      else if (want && chimes[0][1].n !== nWant) fail(10, `the heal chime's n ${chimes[0][1].n}, Censer's blessing ${nWant}`);
      else if (want){ inc("chimeOk"); inc("chimeN" + nWant); }
      else if (closing) inc(closing === "clock" ? "closeQuietClock" : "closeQuietDeath");
      if (!want && pre.some(p => p.f.holyTally.ticks > p.T0.ticks)) inc("tickQuiet");
    }
    /* [6] NOTHING ELSE */
    if (calls.length) fail(6, `the ground called ${calls.join(",")}`);
    if (this.hitStop !== hs0) fail(6, `hitStop ${hs0} -> ${this.hitStop}`);
    if (!full){
      const moved = ["a", "b"].filter(k => lite(this[k]) !== st[k].S).map(k => this[k].w.id);
      if (js(this.shots) !== shJ) moved.push("the shots");
      if (moved.length) fail(6, `with no window open the ground moved ${moved.join(", ")}`);
      else inc("liteOk");
    } else {
      const allow = { a: new Set(), b: new Set() };
      for (const p of pre){ const k = p.side, fk = k === "a" ? "b" : "a";
        for (const d of ["ultHoly", "holyTally", "status.blessing"]) allow[k].add(d);
        allow[fk].add("status.smite"); }
      const moved = [];
      for (const k of ["a", "b"]){ const f = st[k].f;
        for (const d of diffMap(st[k].S, snapF(f))) if (!allow[k].has(d)) moved.push(`${f.w.id}'s ${d}`); }
      for (const d of diffMap(M0, snapM(this))) if (!["holyGround", "holyGround=", "holyT"].includes(d)) moved.push(`the match's ${d}`);
      for (const d of diffMap(GG0, snapG(false))) moved.push(`the shared table ${d}`);
      if (moved.length) fail(6, `the ground also moved ${moved.join(", ")}`);
      else inc("stateOk");
    }
    /* [1] THE GROUND'S CLOCK */
    const hT1 = hT0 + dt;
    if (this.holyT !== hT1) fail(1, `holyT ${hT0} -> ${this.holyT}, want +dt`);
    /* [3] THE AGE: exactly the discs whose age reached groundLife go */
    const lifeOf = d => (d.side === "a" ? this.a : this.b).w.ult.groundLife;
    const keep = G0.filter(d => hT1 - d.t0 < lifeOf(d));
    const E = this.holyGround;
    if (E.length !== keep.length || E.some((d, i) => d !== keep[i])){
      const early = G0.filter(d => keep.includes(d) && !E.includes(d)).length, late = E.filter(d => !keep.includes(d)).length;
      fail(3, `the ground's purge: ${early} gone early, ${late} outlived groundLife`);
    } else { const k = G0.length - keep.length; if (k) inc("expiredOk", k); if (G0.length) inc("purgeOk"); }
    F.model = F.model.filter(d => hT1 - d.t0 < lifeOf(d));
    for (const f of [this.a, this.b]) if (f.w.id === ID && (f.w.ult.groundLife !== PIN.groundLife || f.w.ult.groundR !== PIN.groundR))
      fail(3, `the row's ground (r ${f.w.ult.groundR}, life ${f.w.ult.groundLife}) is not the builder's (${PIN.groundR}, ${PIN.groundLife})`);
    /* THE WINDOW FRAMES */
    for (const p of pre){
      const { f, foe, Z, u, side } = p, T = f.holyTally;
      if (p.t1 >= Z.dur || !p.fAlive || !p.foeAlive){
        if (f.ultHoly) fail(1, "the window did not close");
        else {
          if (p.fAlive && p.foeAlive && p.t1 < Z.dur - 1e-9) fail(1, "closed early");
          else { inc("closes"); if (p.t1 >= Z.dur && p.fAlive && p.foeAlive){ inc("clockCloses");
            const w = F.liveSteps - F.winStart; if (WINLEN !== null && w !== WINLEN) fail(1, `a window of ${w} live steps, the others ${WINLEN}`); WINLEN = w; }
            else inc("deathCloses"); }
          if (T.frames !== p.T0.frames || T.ticks !== p.T0.ticks || T.bless !== p.T0.bless) fail(1, "a closing frame did something");
          if (js(foe.status.smite) !== p.smJ) fail(4, "a closing frame smote");
          if (js(f.status.blessing) !== p.blJ) fail(5, "a closing frame blessed");
        }
        continue;
      }
      inc("frames");
      if (!f.ultHoly){ fail(1, `closed at ${p.t1.toFixed(4)} of ${Z.dur}`); continue; }
      if (f.ultHoly !== Z || Z.t !== p.t1){ fail(1, `the window's clock ${Z.t}, want ${p.t1}`); continue; }
      if (Z.dur !== PIN.dur) fail(1, `the window's dur ${Z.dur}, the builder's ${PIN.dur}`);
      if (T.frames !== p.T0.frames + 1) fail(1, "frames not counted");
      if (p.fx !== foe.x || p.x !== f.x) fail(6, "a ball moved in the ticker");
      /* [4] and [5] read the ground AS THE TICKER LEFT IT (its purge done):
         whether that purge was right is [3]'s alone, so a disc gone early or
         late fails [3] once and does not fail the smite and the heal after it.
         When [3] passes this is `keep`, disc for disc. */
      const mine = E.filter(d => d.side === side);
      const foeOn = mine.some(d => Math.hypot(p.fx - d.x, p.fy - d.y) < u.groundR + R);
      const selfOn = mine.some(d => Math.hypot(p.x - d.x, p.y - d.y) < u.groundR);
      if (mine.some(d => { const q = F.planted.get(d); return q && q.cast < F.casts; })) inc("framesWithOldDisc");
      /* [4] THE SMITE */
      const dT = T.ticks - p.T0.ticks, shouldTick = foeOn && p.cd1 <= 0;
      F.frames++; if (foeOn) F.foeOn++; F.foeStk += p.sm0 ? p.sm0.stacks : 0; if (selfOn) F.selfOn++;
      if (u.tickCd !== PIN.tickCd || u.smite !== PIN.smite) fail(4, `the row's smite (${u.smite} every ${u.tickCd}) is not the builder's`);
      if (u.blessCd !== PIN.blessCd) fail(5, `the row's blessCd ${u.blessCd} is not the builder's`);
      if (T.foeOn - p.T0.foeOn !== (foeOn ? 1 : 0)) fail(4, "foe-on-ground miscounted");
      if (dT > 1) fail(4, `${dT} smites in one frame`);
      if (shouldTick){
        const want = js(applied(p.sm0, SM, u.smite, side));
        if (dT !== 1) fail(4, `the foe on the ground (cd ${p.cd1}) and no smite`);
        else if (js(foe.status.smite) !== want) fail(4, `smite ${p.smJ} -> ${js(foe.status.smite)}, want ${want}`);
        else if (Z.cd !== u.tickCd) fail(4, `cd ${Z.cd} after a smite`);
        else inc("smiteOk");
      } else {
        if (dT) fail(4, `a smite with the foe ${foeOn ? "on" : "off"} the ground, cd ${p.cd1}`);
        else if (js(foe.status.smite) !== p.smJ) fail(4, "the foe's smite moved with no tick");
        else if (Z.cd !== p.cd1) fail(4, `cd ${p.cd1} -> ${Z.cd} with no smite`);
        else inc("noSmiteOk");
      }
      /* [5] THE BLESSING */
      const bless = u.bless;
      if (bless !== 0 && bless !== PIN.bless) fail(5, `the row's bless ${bless}, the builder's 0 / ${PIN.bless}`);
      const dB = T.bless - p.T0.bless, shouldBless = bless > 0 && selfOn && p.bcd1 <= 0;
      if (T.selfOn - p.T0.selfOn !== (selfOn ? 1 : 0)) fail(5, "caster-on-ground miscounted");
      if (shouldBless){
        const want = js(applied(p.bl0, BL, bless, side));
        if (dB !== 1) fail(5, `the caster's centre on the ground (bcd ${p.bcd1}) and no blessing`);
        else if (js(f.status.blessing) !== want) fail(5, `blessing ${p.blJ} -> ${js(f.status.blessing)}, want ${want}`);
        else if (Z.bcd !== u.blessCd) fail(5, `bcd ${Z.bcd} after a blessing`);
        else inc("blessOk");
      } else {
        if (dB) fail(5, `a blessing with the caster ${selfOn ? "on" : "off"} the ground, bcd ${p.bcd1}, bless ${bless}`);
        else if (js(f.status.blessing) !== p.blJ) fail(5, "the caster's blessing moved with no tick");
        else if (Z.bcd !== p.bcd1) fail(5, `bcd ${p.bcd1} -> ${Z.bcd} with no blessing`);
        else inc("noBlessOk");
      }
    }
    return r;
  };

  /* [11] THE PICTURE'S HOOK: `tickConsecration`, on the presentation clock
     (tickPresentation: through hit stops, twice a normal step, and in the
     verdict). The picture is REBUILT from the tally, as [4] rebuilds the
     smite (readings 13-15). */
  if (S6P) P.tickConsecration = function(dt){
    if (!F || F.m !== this) return oCons.call(this, dt);
    inc("consCalls");
    const me = F.me, foe = F.foe, side = me === this.a ? "a" : "b";
    const s0 = simSnap(this), tags0 = new Set(this.tags), fade0 = me.consFade;
    let draws = 0; const oRng = this.rng;
    this.rng = function(){ draws++; return oRng.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture"; vrec = [];
    let r, heard = null;
    try { r = oCons.call(this, dt); } finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = firstDiff(s0, simSnap(this));
    if (d) fail(11, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (draws) fail(11, `the picture drew the RNG ${draws} times`);
    else if (heard.length) fail(11, `the picture played ${JSON.stringify(heard)}`);
    else inc("consClean");
    /* the foe never carries any of it */
    if (foe.consFade !== 0 || foe.consPic.length || foe.consPulse !== 0 || foe.consFoeLit !== 0 || foe.consSelfLit !== 0
        || foe.consFoeOn || foe.consSelfOn) fail(11, `${foe.w.id}, which is not Censer, carries the picture`);
    const T = me.holyTally, G = this.holyGround;
    const fresh = this.tags.filter(g => !tags0.has(g));
    if (!T){
      if (me.consFade !== 0 || me.consPic.length) fail(11, "Censer carries the picture before its first cast");
      if (fresh.length) fail(11, `a tag before Censer's first cast: ${fresh.map(g => g.key)}`);
      return r;
    }
    if (!PM) PM = { seen: [0, 0, 0, 0, 0], on: false, self: false, tagS: false, tagB: false, closeDt: -1, prevZ: null, ages: new Map() };
    const Z = (this.over || !me.alive) ? null : me.ultHoly;
    /* THE HEAD: lit exactly while the window is open; a 0.3 s fade at any close */
    if (Z){
      if (me.consFade !== 1) fail(11, `the head not lit (${me.consFade}) in an open window`);
      else inc("upOk");
      if (PM.prevZ !== Z){ PM.on = false; PM.self = false; PM.tagS = false; PM.tagB = false; inc("picCasts"); }
      PM.closeDt = -1;
    } else if (fade0 > 0){
      if (PM.closeDt < 0){ PM.closeDt = 0;
        inc(this.over ? (me.ultHoly ? "picCloseOverOpen" : "picCloseOver") : !me.alive ? "picCloseDeath"
            : !foe.alive ? "picCloseFoeDeath" : "picCloseClock"); }
      PM.closeDt += dt;
      const want = Math.max(0, 1 - PM.closeDt / 0.6);
      if (Math.abs(me.consFade - want) > 1e-9) fail(11, `the head's close: ${me.consFade} at ${PM.closeDt.toFixed(4)} of its clock, want ${want}`);
      else if (me.consFade === 0) inc("picClosedOk");
    } else if (me.consFade !== 0) fail(11, `the head lit (${me.consFade}) with no window open`);
    PM.prevZ = Z;
    /* THE DISCS: the caster's discs of m.holyGround, by identity and in order;
       each record's bloom clock the presentation clock since it appeared */
    const mine = G.filter(q => q.side === side), recs = me.consPic;
    if (recs.length !== mine.length || recs.some((p, i) => p.d !== mine[i]))
      fail(11, `the picture's discs (${recs.length}) are not the caster's discs of the ground (${mine.length})`);
    else inc("discsMirrorOk");
    const ages = new Map();
    for (const p of recs){ const seen = PM.ages.has(p.d), a1 = (seen ? PM.ages.get(p.d) : 0) + dt;
      if (p.age !== a1) fail(11, `a disc's bloom clock ${p.age}, want ${a1}`);
      if (!seen) inc("discsSeen");
      ages.set(p.d, a1); }
    PM.ages = ages;
    /* ON THE GROUND, the flash and the tags, from the tally's rises */
    const S = PM.seen, dF = T.frames - S[0], dO = T.foeOn - S[1], dK = T.ticks - S[2], dS = T.selfOn - S[3], dB = T.bless - S[4];
    PM.seen = [T.frames, T.foeOn, T.ticks, T.selfOn, T.bless];
    if (!Z){ PM.on = false; PM.self = false; } else if (dF > 0){ PM.on = dO > 0; PM.self = dS > 0; }
    if (me.consFoeOn !== PM.on || me.consSelfOn !== PM.self)
      fail(11, `on the ground: the picture's foe ${me.consFoeOn} / Censer ${me.consSelfOn}, the ticker's ${PM.on} / ${PM.self}`);
    else if (Z) inc(PM.on ? "onFoeOk" : PM.self ? "onSelfOk" : "offOk");
    if (!PM.on) PM.tagS = false;
    if (!PM.self) PM.tagB = false;
    if (dK > 0){ if (me.consPulse !== 1) fail(11, "a smite tick without its flash"); else inc("pulseOk"); }
    let wantS = false, wantB = false;
    if (Z && foe.alive && foe.hp > 0){
      if (dK > 0 && !PM.tagS){ wantS = true; PM.tagS = true; }
      if (dB > 0 && !PM.tagB){ wantB = true; PM.tagB = true; }
    }
    const gS = fresh.filter(g => g.key === "smite"), gB = fresh.filter(g => g.key === "blessing");
    if (fresh.length !== gS.length + gB.length) fail(11, `the picture filed a tag that is not SMITE or BLESSING: ${fresh.map(g => g.key)}`);
    if (gS.length !== (wantS ? 1 : 0)) fail(11, `${gS.length} SMITE tag(s) on a call with ${dK} smite tick(s), want ${wantS ? 1 : 0}`);
    else if (wantS && (gS[0].x !== foe.x || gS[0].y !== foe.y || gS[0].val !== foe.stacks("smite"))) fail(11, "the SMITE tag not at the foe with its count");
    else if (wantS) inc("tagSOk");
    else if (dK > 0) inc("tickUntagged");
    if (gB.length !== (wantB ? 1 : 0)) fail(11, `${gB.length} BLESSING tag(s) on a call with ${dB} blessing(s), want ${wantB ? 1 : 0}`);
    else if (wantB && (gB[0].x !== me.x || gB[0].y !== me.y || gB[0].val !== me.stacks("blessing"))) fail(11, "the BLESSING tag not on Censer with its count");
    else if (wantB) inc("tagBOk");
    else if (dB > 0) inc("blessUntagged");
    return r;
  };

  /* THE DRAWN SUBSET [11]: a frame through the renderer, the simulation read
     before and after; a draw's own memo writes to an underscore key of SHAPES
     become [6]'s once-a-fight start for that key */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawMemo = new Set();
  const memoSnap = () => { const o = new Map();
    for (const k of Object.keys(AC.SHAPES)) if (k.charCodeAt(0) === 95) o.set(k, js(AC.SHAPES[k]));
    return o; };
  let G00 = null;
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.consFade > 0 || (q.consPic && q.consPic.length) || q.consFoeLit > 0 || q.consSelfLit > 0);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    setM(m);
    const s0 = simSnap(m), oR = m.rng, u0 = memoSnap(); let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx; vctx = "a drawn frame";
    let threw = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; vctx = vc0; }
    const u1 = memoSnap();
    for (const k of new Set([...u0.keys(), ...u1.keys()])) if (u0.get(k) !== u1.get(k)){
      drawMemo.add(k);
      if (u1.has(k)) G00.set("SHAPES." + k, u1.get(k)); else G00.delete("SHAPES." + k); }
    const d = firstDiff(s0, simSnap(m));
    if (threw) fail(11, "a drawn frame threw: " + threw);
    else if (dr) fail(11, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(11, "a drawn frame changed the simulation: " + d);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };

  /* THE HP ACCESSOR [5]: Censer's hp may rise only inside its own status
     tick (bounded there) or inside the ticker ([6] owns those frames). */
  const hook = (f) => { let v = f.hp;
    Object.defineProperty(f, "hp", { configurable: true, enumerable: true,
      get(){ return v; },
      /* checkEnd's `loser.hp = Math.max(0, loser.hp)` clamps a dead ball's
         hp up to 0: that is the death, not a heal */
      set(x){ if (x > v && !(v < 0 && x === 0)){ if (ctx === "status") statusRise += x - v;
                           else if (ctx !== "ticker") fail(5, `Censer healed ${x - v} outside the blessing (v ${F ? F.foe.w.id : "?"}, in ${String(new Error().stack).split(String.fromCharCode(10)).slice(2, 4).map(l => l.trim().split(" ")[1]).join(" < ")})`); }
              v = x; } }); };
  const unhook = (f) => { const v = f.hp; delete f.hp; f.hp = v; };

  const foes = foeList.length ? foeList : AC.WEAPONS.map(w => w.id).filter(i => i !== ID);
  const T = { casts: 0, frames: 0, discs: 0, foeOn: 0, ticks: 0, selfOn: 0, bless: 0, foeStk: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, pctOn = 0, stkF = 0, pctSelf = 0;
  setM(null);
  G00 = snapG(true);
  for (const side of sides) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, ID, sd) : new AC.Match(ID, fid, sd);
    const me = side ? m.b : m.a, foe = side ? m.a : m.b;
    F = { m, me, foe, model: [], planted: new WeakMap(), casts: 0, liveSteps: 0, winStart: 0,
          frames: 0, foeOn: 0, foeStk: 0, selfOn: 0, bIn: 0, bOut: 0 };
    PM = null;
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    hook(me);
    let steps = 0;
    try {
      while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
      /* [10]-[11] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
      if ((S6V || S6P) && m.over){
        const open = !!me.ultHoly, lit = me.consFade > 0, o0 = (n.x10 || 0);
        tail = true; vctx = "the verdict";
        try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
        finally { tail = false; vctx = "a step"; }
        if (S6V && (n.x10 || 0) === o0) inc(open ? "verdictQuietOpen" : "verdictQuiet");
        if (S6P){
          if (me.holyTally && (me.consFade !== 0 || (me.consPic.length && !(me.consEnd >= 0.6))))
            fail(11, `after 2 s of the verdict the head at ${me.consFade}, the ground's fade clock ${me.consEnd} with ${me.consPic.length} disc(s)${open ? " -- the window the sim left open" : ""}`);
          else if (me.holyTally) inc(lit ? (open ? "endGoneOpen" : "endGoneLit") : "endGoneOk");
        }
      }
    }
    finally { unhook(me); }
    fights++; bin += F.bIn; bout += F.bOut;
    if (F.frames){ pctOn += 100 * F.foeOn / F.frames; stkF += F.foeStk / F.frames; pctSelf += 100 * F.selfOn / F.frames; }
    setM(null);
    { const d = diffMap(G00, snapG(true));
      if (d.length) fail(6, `the shared table(s) ${d.join(", ")} written (${fid}, seed ${sd})`); else inc("rowOk"); }
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.holyTally) for (const k in T) T[k] += me.holyTally[k];
    F = null;
  }
  P.tickHolyGround = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep; P.tickCharge = oCharge;
  P.tickWeapon = oWeapon; P.tickHits = oHits; P.tickStatus = oStatus;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
            if (oSun) P.tickSun = oSun; if (oSparks) P.tickSparks = oSparks; }
  if (S6P) P.tickConsecration = oCons;
  for (const [pr] of TAGS) delete pr.toJSON;
  const w = AC.WEAPONS.find(x => x.id === ID), u = w.ult;
  n.winLen = WINLEN;
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           f_foeOnPct: pctOn / fights, f_foeStk: stkF / fights, f_selfOnPct: pctSelf / fights,
           s6v: S6V, s6p: S6P, drawMemo: [...drawMemo].sort(),
           u: { charge: u.charge, dur: u.dur, groundR: u.groundR, groundLife: u.groundLife, tickCd: u.tickCd,
                smite: u.smite, blessCd: u.blessCd, bless: u.bless }, dmg: w.dmg };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickHolyGround === 'function'"):
        raise SystemExit("no tickHolyGround in this build -- not a Consecration link (stage 2+)")
    seeds = [a.seed0 + a.seedstep * i for i in range(a.seeds)]
    foe_list = [x for x in a.foes.split(",") if x]
    R = page.evaluate(JS, [seeds, foe_list, [{"A": 0, "B": 1}[c] for c in a.sides], PIN, a.drawn])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
print(f"\nCONSECRATION PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Censer {'both sides' if a.sides == 'AB' else 'side ' + a.sides} x "
      f"{'every foe' if not a.foes else str(len(a.foes.split(','))) + ' foes'} x {a.seeds} seeds)   blade {R['dmg']}   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   per cast: discs {T['discs']/casts:.2f}  smites {T['ticks']/casts:.2f}  "
      f"blessings {T['bless']/casts:.2f}   foe on the ground {R['f_foeOnPct']:.2f}% of window frames (a fight's mean; "
      f"pooled {100*T['foeOn']/max(1,T['frames']):.2f}%)   foe smite stacks on a window frame {R['f_foeStk']:.2f}   "
      f"Censer win {R['win']:.1%}")
print(f"  blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   window frames a cast "
      f"{T['frames']/casts:.1f} (dur x 120 = {U['dur']*120:.0f})   caster's centre on the ground {R['f_selfOnPct']:.2f}% "
      f"of window frames   closes: clock {n.get('clockCloses',0)}, death {n.get('deathCloses',0)}")
print(f"  discs expired {n.get('expiredOk',0)}   casts with its own ground still standing {n.get('castsWithGround',0)} "
      f"({n.get('discsCarried',0)} discs; window frames with an older window's disc {n.get('framesWithOldDisc',0)})   "
      f"discs at a shade {n.get('shadeDiscs',0)}   FREEZE CENSUS {100*frozen:.1f}% of window steps frozen "
      f"(a window is ~{U['dur']/(1-frozen):.2f}s of match time)")
print(f"  whole-state diffs clean: {n.get('stateOk',0)} ground frames, {n.get('castOk',0)} casts, {n.get('rowOk',0)} fights' "
      f"shared tables   frozen steps unchanged {n.get('frozenOk',0)}   blows rebuilt {n.get('blowInOk',0)} in / "
      f"{n.get('blowOutOk',0)} out ({n.get('blowExempt',0)} into Bulwarden's wall exempt)   turns {n.get('turnInOk',0)} in / "
      f"{n.get('turnOutOk',0)} out   hit tests {n.get('hitTestOk',0)}   blessing heals {n.get('blessHealOk',0)}")
bless_on = U["bless"] > 0
checks = [
    (1, "the window: `dur` on the window clock (live +dt, frozen untouched, the ground and holyT too), closes on either death; no cast under a window; only Censer",
        n.get("closes", 0) > 0 and n.get("clockCloses", 0) > 0 and n.get("frozenOk", 0) > 0),
    (2, "every blow in the window plants exactly one disc {x, y, t0, side} at the struck ball; none outside; no other disc",
        n.get("plantOk", 0) > 0 and n.get("noPlantOutOk", 0) > 0),
    (3, "the ground lasts: discs do not move, go exactly at groundLife on holyT, nothing else removes one",
        n.get("expiredOk", 0) > 0 and n.get("purgeOk", 0) > 0),
    (4, "the smite: the foe within groundR + R of a live disc, cd clear -> apply(\"smite\", smite, side) exactly; cd tickCd; none else",
        n.get("smiteOk", 0) > 0 and n.get("noSmiteOk", 0) > 0),
    (5, "the heal: the caster's centre within groundR, bcd clear -> apply(\"blessing\", bless, side) exactly (none at bless 0); no other heal",
        (n.get("blessOk", 0) > 0 and n.get("blessHealOk", 0) > 0) if bless_on else n.get("noBlessOk", 0) > 0),
    (6, "nothing else on a ground frame: no hurt, beat, rng draw or hit stop; whole-state diff (fighters, match, shades, shared tables)",
        n.get("frames", 0) > 0 and n.get("stateOk", 0) > 0 and n.get("rowOk", 0) > 0),
    (7, "the nova is out: a cast opens exactly {t 0, dur, cd 0, bcd 0} and writes nothing else (from the prologue's end)",
        n.get("castOk", 0) > 0),
    (8, "the hammer swings as ever: the turn, the hit test, and every blow (damage, knock, hitstun, stop, onHit) rebuilt, in the window and out",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0 and n.get("turnInOk", 0) > 0 and n.get("hitTestOk", 0) > 0),
    (9, f"the charge: +dt a tick, a cast exactly at {PIN['charge']} (the lab's 16 on the game's clock)",
        n.get("castOnCharge", 0) > 0 and n.get("chargeOk", 0) > 0),
]
g = lambda k: n.get(k, 0)
if R["s6v"]:
    print(f"  stage 6 voices: {g('castVoiceOk')} casts each one cast voice (of {T['casts']}); {g('bellOk')} discs each one bell "
          f"(n 1-6: {'/'.join(str(g('bellN' + str(i))) for i in range(1, 7))}; {g('bellOnKill')} on a killing blow); "
          f"{g('blowQuietOk')} other blows silent; {g('chimeOk')} blessings each one heal chime (n 1-5: "
          f"{'/'.join(str(g('chimeN' + str(i))) for i in range(1, 6))}); {g('tickQuiet')} smite-tick frames silent; closes silent: "
          f"{g('closeQuietClock')} by the clock, {g('closeQuietDeath')} by a death; silent through 2 s of the verdict: "
          f"{g('verdictQuietOpen')} fights with the window open, {g('verdictQuiet')} with it shut; the run's own: "
          f"{g('v_censer')} cast voices, {g('v_censer-disc')} bells, {g('v_chime')} chimes in the ticker, {g('v_chimeOther')} "
          f"other relics' chimes in their spark tickers")
    checks.append((10, "stage 6 voices: one cast voice a cast (in fireUlt), one bell a disc planted (n = the caster's discs "
                       "standing), one heal chime a blessing (n = Censer's blessing); none on a close, by the clock or a "
                       "death, nor on a smite tick, a foe's cast, the picture or the verdict; every one accounted for",
                   g("castVoiceOk") == T["casts"] > 0 and g("bellOk") == T["discs"] > 0 and g("chimeOk") == T["bless"] > 0
                   and g("v_censer") == T["casts"] and g("v_censer-disc") == T["discs"] and g("v_chime") == T["bless"]
                   and g("closeQuietClock") > 0 and g("closeQuietDeath") > 0 and g("tickQuiet") > 0))
if R["s6p"]:
    print(f"  stage 6 picture: tickConsecration {g('consCalls')} calls, {g('consClean')} writing nothing of the simulation's, "
          f"drawing no RNG and playing nothing; the head lit on {g('upOk')} calls in an open window ({g('picCasts')} casts); "
          f"closes {g('picCloseClock')} by the clock, {g('picCloseDeath')} on Censer's death and {g('picCloseFoeDeath')} on the "
          f"foe's (in the kill flight), {g('picCloseOver') + g('picCloseOverOpen')} at `over` ({g('picCloseOverOpen')} of them "
          f"with the sim's window still open), {g('picClosedOk')} out in 0.6 of its clock (0.3 s); "
          f"the discs mirrored on {g('discsMirrorOk')} calls ({g('discsSeen')} discs, each bloom clock exact); on the ground: "
          f"foe {g('onFoeOk')}, Censer {g('onSelfOk')}, neither {g('offOk')} window calls; {g('pulseOk')} smite ticks flashed; "
          f"tags: SMITE {g('tagSOk')} (+{g('tickUntagged')} ticks inside a tagged stretch), BLESSING {g('tagBOk')} "
          f"(+{g('blessUntagged')}); after 2 s of the verdict the picture gone in {g('endGoneOk') + g('endGoneLit') + g('endGoneOpen')} "
          f"fights, {g('endGoneLit') + g('endGoneOpen')} of them lit at `over` ({g('endGoneOpen')} with the sim's window still open)")
    checks.append((11, "stage 6 picture: tickConsecration writes nothing of the simulation's, draws no RNG, plays nothing; the head "
                       "lit while the window is open and a 0.3 s close at any close; the discs the sim's; on the ground the "
                       "ticker's own answer; a flash a smite tick; SMITE / BLESSING on each stretch's first; gone after the "
                       "verdict" + ("; the drawn subset clean" if g("drawnFights") else ""),
                   g("consCalls") > 0 and g("consClean") == g("consCalls") and g("upOk") > 0 and g("picCloseClock") > 0
                   and g("picClosedOk") > 0 and g("discsSeen") > 0 and g("onFoeOk") > 0 and g("onSelfOk") > 0
                   and g("pulseOk") > 0 and g("tagSOk") > 0 and g("tagBOk") > 0 and g("tickUntagged") > 0
                   and g("endGoneOpen") > 0 and (g("drawOk") > 0 if g("drawnFights") else True)))
if g("drawnFights"):
    print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 60th "
          f"otherwise): {g('drawOk')} frames clean, {g('drawPic')} with the picture up ({g('drawPicStop')} in a hit stop), "
          f"{g('drawVerdict')} in the verdict; the renderer's memos taken into [6]'s start: {R['drawMemo']}")
    if not R["s6p"]:
        checks.append((11, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                           "the simulation", g("drawOk") > 0))
if not (R["s6v"] or R["s6p"]):
    print("  stage 6: not on this link (no disc bell in the synth, no tickConsecration) -- [10]-[11] not run")
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
