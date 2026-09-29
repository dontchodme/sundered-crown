#!/usr/bin/env python
"""BULWARK'S PROBE -- one check per sentence of v77 §1 / §5, read INSIDE the hooks.

    python lightkeeper_probe.py --game <sc-lightkeeper-wall.html | -bulwark...>

Wraps `tickLightwall`, `fireUlt`, `resolveHit` and `step` on the Match
prototype and reads each event where it happens. Runs Lightkeeper against every
other relic, both sides, and prints N/N. The checks follow the link's own
numbers, so the same probe gates stages 2-5 (bank 0 / 3).

THE WALL IS REBUILT, NOT READ. For every window frame the probe takes the
frame's own theta and position and every shot in the hall as they stood when
the ticker was called, rebuilds the wall (centre `ahead` along theta,
half-length `half`, perpendicular) with the engine's own segment distance, and
says which arrows must die and whether the foe must be turned back. It then
compares that with what the ticker did.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "for a duration": a window that is not `dur` long on the window clock,
      that outlives either death, a Lightkeeper cast under a standing wall, or
      any relic but Lightkeeper carrying `ultWall`; THE WINDOW CLOCK: the
      wall's ticker running on a frozen step (hit stop, latch, split hold), or
      not exactly once on a live one (added on the resume: the lab-clock
      control, ticked through freezes, now fails here)
  [2] "the nova is out": a Lightkeeper cast that does not open the wall
      {t 0, dur, cd 0} exactly, or that writes ANYTHING ELSE. Read at the
      point the lightwall branch starts: the engine's shared cast prologue
      (ultsFired, the banner, the note, the shake, the cast's 0.08 hit stop,
      the "ult" beat, the ultFx record) is every relic's and not the design's,
      so the probe snapshots both fighters (every field: stun, stunDR, pin,
      pinV, pinMax, burden, the whole `status` table, shield, shieldMax, ...)
      and the match when the prologue assigns `ultFx` -- its last statement
      before the kind branches -- and after the cast allows only the caster's
      `ultWall` and a `wallTally` whose casts went up by one (added in the
      second review round: a cast that stunned, pinned or hexed passed before)
  [3] "arrows die on it": a live shot within (r || 6) + shotPad of the rebuilt
      wall that survives, a shot outside it that dies, a net arrow killed
      without tickShots' endpoint write (stuck, still, life 1e9) or a non-net
      one not spliced, a stuck arrow touched, or arrows counted != killed
  [4] "an enemy that runs into it": a block without the foe's centre inside
      R + ballPad of the rebuilt wall, the foe pinned or the cooldown not clear;
      a clear, unpinned contact with no block; two blocks closer than `cd` on
      the window clock; the cooldown not `cd` after a block
  [5] "bounces off and cannot pass": a block whose shove is not exactly `shove`
      along the wall's normal to the side the foe stands on (the lab's H.knock
      arithmetic), or a velocity change on a frame with no block
  [6] "every arrow ... and every time it turns the enemy back, the shield
      grows": the caster's shield not min(cap, shield + bankShot) per arrow
      then + bankBall per block, in that order, from the blocks that happened;
      shieldMax not following; the ward not exactly apply("ward", 1) once a
      bank (stacks to the cap, t = the ward's dur, src untouched) or moved on
      a frame with no bank; banks != blocks + arrows; any change at bank 0
  [7] nothing else: a hurt, a beat, an rng draw or a hit stop on a wall frame;
      and, from the second review round, A WHOLE-STATE DIFF: every field of
      both fighters (stun, stunDR, pin, pinV, pinMax, burden, the `status`
      table key by key with stacks, t and src, the foe's shield and shieldMax,
      position, hp, ...), every field of the match, and every field of every
      shot that is not dying, before and after the ticker. The only changes
      allowed are the ones another check rebuilds exactly: the caster's
      ultWall and wallTally ([1] [3] [4] [6]), shield, shieldMax and ward
      ([6]); the foe's vx and vy ([5]); the dying arrows ([3]). (A block that
      stunned the foe for 0.3s -- the reviewer's r5-stun, Lightkeeper 43.9% ->
      76.1% -- passed the first form of this check.)
      THIRD REVIEW ROUND (v5). "Every field of the match" now means it: each
      match array by its length, each element by identity AND by content --
      a Fighter inside an array (Twinshade's shades) gets the fighters' own
      field-by-field snapshot, keyed `shades[i].<field>`, and every other
      element (the cast's shots included) its JSON. And the SHARED MODULE
      TABLES: STATUS, CONFIG and AFFINITIES before and after every wall
      frame and every cast; those three plus WEAPONS and SHAPES once a fight
      against their values when the run began. (A block that shoved a shade,
      the reviewer's v3-shade, and one that wrote STATUS.ward.cap = 120, v4-
      global, passed v4 8/8 while changing fights.) The JSON is the native
      one (the engine itself never serialises anything) with four tags set
      for the run and removed after it: a fighter, a shade and the match
      write as tags (no cycle, no deep copy), a Map or a Set writes its
      entries (JSON would write {}). A value the probe cannot serialise FAILS
      [7] (a field it cannot read is not a pass). What JSON still cannot tell
      apart, nested inside a record: NaN / Infinity / null, and one function
      for another (top-level fields of a fighter are compared by value, so
      there they are seen). [6] rebuilds the cap from the live STATUS.ward,
      the engine's own; [7] is what holds that table to its start.
  [8] "the sword swings as ever": a Lightkeeper blow whose damage is not the
      greatsword's own (blade x dmgMul x jitter x dmgTaken, crit, rounded),
      rebuilt from the captured draws, in the window and out

COUNTED, NOT CHECKED (the builder's reading 2): the Crossweave volleys the
wall leaves with every arrow stuck. tickShots releases such a volley in the
same pass as its own endpoint write; the wall copies the write and not the
release, so the volley detonates at the next tickShots -- a frame later, or
after the whole freeze if a blow in tickHits starts one that frame.

STAGE 6 (the picture and the voice, sc-lightkeeper-bulwark-b9.5-fx; this is
the probe's v6). Each check runs only on a link that carries its half, read
off the page itself, so the same probe still reads [1]-[8] alone on a link
without stage 6. (v6 also reads SHAPES key by key in the once-a-fight table
check, and takes into that check's start what a DRAW writes to SHAPES'
underscore memos, as the draw writes it: the renderer keeps `_t`,
`_shadeCache`, `_facetCache`, `_inkCache` and `_fxc` there, on the base link
alike, and a headless fight never draws. Anything else a draw writes in
SHAPES, and anything written to those memos outside a draw, still fails [7].
v6's first form left four named memos out and missed `_fxc`, which a drawn
Axiom fight creates: v107 §5d.)
  [9] THE VOICE (on when "lightkeeper-gong" is in AC.SFX.play.toString()): a
      Lightkeeper cast without exactly one `ult`/lightkeeper voice (the raise)
      inside fireUlt; a tickLightwall call whose Lightkeeper voices are not
      exactly, in order, a tink per arrow its wall stopped (k = the arrow's
      index among the call's kills, 0 up) then a gong per block, and on a
      closing frame the fold IF AND ONLY IF the close is by the clock with
      both alive -- a close by a death sounds nothing; any other voice inside
      tickLightwall (the wall hurts nobody, so not even a ward's shatter,
      which plays its own crit hit voice inside hurt(), can sound there); and
      every Lightkeeper voice of the run accounted for by those events (none
      plays anywhere else: at `over`, in the verdict, on a draw)
  [10] THE PICTURE (on when the Match has `tickBulwark`): `tickBulwark`, the
      picture's one hook on the step, changing anything but its own
      `bulwark*` fields, the floats, the tags and `taught` -- read on EVERY
      call as every own primitive field of both fighters, their status,
      window and tally, the match's primitives, every shot and every shade;
      and on every call where the picture has something to do (a cast, a
      block, an arrow, a fold) as the v5 whole-state diff of both fighters,
      the match and the shared tables -- or drawing the RNG; the bar up
      (bulwarkFade exactly 1) other than exactly while `ultWall && alive &&
      !over`, or rising again with no cast; a block and an arrow the picture
      does not see on the call after the ticker made them (each call's rise
      in the tally is exactly the ticker's count since the last call); a
      block without its two-frame flash (0.066 on the presentation clock);
      arrows without exactly min(n, 8) new scorches, each on the bar; a bank
      without exactly one "+N" float of the banked amount at the caster's
      seat, or a float with no bank; the WARD tag not exactly once a window,
      on its first bank; a bar up at `over` not folded to 0 by 0.51s into the
      verdict; an event the picture never showed; and on the DRAWN subset
      (the first seed, both sides, every foe, through the kill and the
      verdict, the post chain off) a drawn frame that throws, draws the
      match's RNG or changes a sim field
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=107001)
ap.add_argument("--json", default=None)
# THE LAB'S FIELD, for a like-for-like mechanism column: --foes <the design's 33> --sides A
# --seed0 2207 --seeds 20 --seedstep 11 plays exactly the fights ult_overlay's arm SHIP plays.
ap.add_argument("--foes", default="", help="comma list; default every other relic")
ap.add_argument("--sides", default="AB", choices=["AB", "A", "B"])
ap.add_argument("--seedstep", type=int, default=13)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()

JS = r"""([seeds, foeList, sides, drawEvery]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, W = AC.STATUS.ward;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  /* the engine's segDist, character for character */
  const segd = (ax, ay, bx, by, px, py) => { const dx = bx - ax, dy = by - ay, len2 = dx*dx + dy*dy;
    let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2; t = t < 0 ? 0 : t > 1 ? 1 : t;
    const cx = ax + dx * t, cy = ay + dy * t; return Math.hypot(px - cx, py - cy); };
  const wallOf = (th, x, y, u) => { const ux = Math.cos(th), uy = Math.sin(th);
    const cx = x + ux * u.ahead, cy = y + uy * u.ahead, px = -uy, py = ux;
    return { ux, uy, cx, cy, ax: cx - px * u.half, ay: cy - py * u.half, bx: cx + px * u.half, by: cy + py * u.half }; };
  const oTick = P.tickLightwall, oResolve = P.resolveHit, oFire = P.fireUlt, oStep = P.step;
  const lastBlock = new WeakMap();
  let per = null;

  /* THE WHOLE-STATE SNAPSHOT ([2] and [7]). Every own field of a fighter:
     primitives by value (Object.is), everything else as JSON with the
     fighters, the shades and the match written as tags (TAGS below). The
     status table is split so the caster's ward -- [6]'s, rebuilt exactly --
     is its own key: "status" is the table WITHOUT the ward, "status.ward"
     the ward alone. `w` and `aff` are the shared rows, checked once a fight
     on the whole table. The match: primitives by value; every array by its
     length and element identity AND by content (the whole array's JSON; a
     Fighter element -- a Twinshade shade -- also through snapF, key by key);
     records as JSON. The fighters a and b, the rng and (on a wall frame,
     where [3] owns them) the shots are left to their own checks. */
  let curM = null, FP = null;
  /* the tags, for the run only (removed at the end): native JSON, no replacer */
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
    catch (e) { fail(7, `the probe could not serialise a field (${e.message}) -- a field it cannot read is not a pass`); return "<unread>"; } };
  const SKIPF = new Set(["w", "aff", "status"]);
  const snapF = f => { const o = new Map();
    for (const k of Object.keys(f)){ if (SKIPF.has(k)) continue; const v = f[k];
      o.set(k, (v === null || typeof v !== "object") ? v : "J" + js(v)); }
    o.set("status", "J" + js(Object.assign({}, f.status, { ward: undefined })));
    o.set("status.ward", "J" + js(f.status.ward));
    return o; };
  const snapM = (m, withShots) => { const o = new Map();
    for (const k of Object.keys(m)){ if (k === "a" || k === "b" || k === "rng" || (!withShots && k === "shots")) continue;
      const v = m[k];
      if (typeof v === "function") continue;
      if (Array.isArray(v)){
        o.set(k, v.slice());                                         // length and element identity
        o.set(k + "=", "J" + js(v));                                 // content
        for (let i = 0; i < v.length; i++){ const e = v[i];           // a shade, field by field
          if (e !== null && typeof e === "object" && Object.getPrototypeOf(e) === FP)
            for (const [fk, fv] of snapF(e)) o.set(`${k}[${i}].${fk}`, fv); } }
      else o.set(k, (v === null || typeof v !== "object") ? v : "J" + js(v)); }
    return o; };
  /* THE SHARED MODULE TABLES (third review round). STATUS, CONFIG and
     AFFINITIES around every wall frame and cast; with WEAPONS and SHAPES,
     once a fight against the run's start. */
  /* SHAPES, KEY BY KEY, AND THE RENDERER'S MEMOS (stage 6's drawn subset).
     Any draw, on the base link alike, writes memo entries into SHAPES under
     underscore keys -- `_t`, the `_shadeCache`, `_facetCache` and
     `_inkCache` colour memos, and `_fxc`, which a drawn Axiom fight creates
     (measured over every foe drawn, both links: v107 §5d). Headless fights
     never draw, so they never move. The once-a-fight check reads every key
     of SHAPES; `drawFrame` takes what each DRAW writes to an underscore key
     into the check's start as the draw writes it (`memoSnap` before and
     after the draw), so a sim write to any key, a memo included, and a
     draw's write to any other key still fail [7]. */
  const memoSnap = () => { const o = new Map();
    for (const k of Object.keys(AC.SHAPES)) if (k.startsWith("_")) o.set(k, js(AC.SHAPES[k]));
    return o; };
  const drawMemo = new Set();
  const snapG = all => { const o = new Map([["STATUS", js(AC.STATUS)], ["CONFIG", js(AC.CONFIG)], ["AFFINITIES", js(AC.AFFINITIES)]]);
    if (all){ o.set("WEAPONS", js(AC.WEAPONS));
              for (const k of Object.keys(AC.SHAPES)) o.set("SHAPES." + k, js(AC.SHAPES[k])); }
    return o; };
  /* Fighter.apply("ward", 1) with no source, `n` times, rebuilt from the
     engine's own lines: the stacks rise to the cap unless already at it, the
     clock is set to the ward's dur, the src is left as it was. */
  const wardAfter = (w0, n) => { const c = Object.assign({}, w0 || { stacks: 0, t: 0 });
    for (let i = 0; i < n; i++){ if (c.stacks < W.maxStacks) c.stacks = Math.min(W.maxStacks, c.stacks + 1); c.t = W.dur; }
    return c; };
  const diffMap = (A, B) => { const out = [];
    for (const [k, v] of A){ if (!B.has(k)){ out.push(k); continue; } const w = B.get(k);
      if (Array.isArray(v)){ if (!Array.isArray(w) || w.length !== v.length || v.some((x, i) => x !== w[i])) out.push(k); }
      else if (!Object.is(v, w)) out.push(k); }
    for (const k of B.keys()) if (!A.has(k)) out.push(k);
    return out; };

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /lightkeeper-gong/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickBulwark === "function";
  const voices = [], lkAll = {}, oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  const oBulwark = P.tickBulwark;
  let postOver = false;
  const lkV = q => !!(q && typeof q.w === "string" && /^lightkeeper/.test(q.w));
  const vname = x => x[0] + (x[1] && x[1].w ? "/" + x[1].w : "") + (x[1] && x[1].k !== undefined ? ":" + x[1].k : "")
                   + (x[1] && x[1].crit ? "(crit)" : "");
  if (stage6v) AC.SFX.play = function(kind, q){
    voices.push([kind, q && typeof q === "object" ? Object.assign({}, q) : q]);
    if (kind === "ult" && lkV(q)) lkAll[q.w] = (lkAll[q.w] || 0) + 1;
    return oPlay.apply(this, arguments);
  };
  /* THE PICTURE'S EVENTS, as the ticker made them, a side: arrows and blocks
     since the picture's last call, and where each arrow died (for the scorch
     placement, measured and printed, not gated: the picture places it from
     its own prediction). */
  const pend = { a: { A: 0, B: 0, at: [] }, b: { A: 0, B: 0, at: [] } };
  const scorchD = { seen: [], unseen: [] };
  /* THE SIM AS A PICTURE HOOK COULD TOUCH IT, cheap enough for every call:
     every own primitive field of both fighters but the picture's own
     `bulwark*`, their status, window and tally; every own primitive field of
     the match; every shot; every shade's body. (The floats, the tags and
     `taught` are the picture's to write; the whole-state diff below reads
     everything else on the calls where the picture does something.) */
  const PIC = k => k.startsWith("bulwark");
  const simLite = m => { const o = [];
    for (const f of [m.a, m.b]){
      for (const k of Object.keys(f)){ if (PIC(k)) continue; const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v); }
      o.push(js(f.status), js(f.ultWall), js(f.wallTally), f.pin, f.stun);
    }
    for (const k of Object.keys(m)){ const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v); }
    o.push(js(m.shots));
    for (const s of (m.shades || [])) o.push(s.x, s.y, s.vx, s.vy, s.hp, s.alive);
    return o; };
  const firstDiffA = (A, B) => { if (A.length !== B.length) return `length ${A.length} -> ${B.length}`;
    for (let i = 0; i < A.length; i++) if (!Object.is(A[i], B[i])) return `[${i}] ${String(A[i - 1] !== undefined && typeof A[i - 1] === "string" ? A[i - 1] + " " : "")}${String(A[i]).slice(0, 80)} -> ${String(B[i]).slice(0, 80)}`;
    return null; };
  /* THE SIM FOR A DRAWN FRAME (the renderer keeps its own caches): the bodies,
     the statuses, the window and tally, the clock, the stop, the verdict, the
     holds, the beats, the shots and the shades. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "stunDR", "pin", "burden",
              "alive", "hits", "dealt", "crits", "spinDir", "swingPhase", "fireCd"];
  const simDraw = m => { const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null,
                                    !!m.latch, !!m.splitHold, m.beats ? m.beats.length : null, js(m.shots)];
    for (const f of [m.a, m.b]){ for (const k of FF) o.push(f[k]); o.push(js(f.status), js(f.ultWall), js(f.wallTally)); }
    for (const s of (m.shades || [])) o.push(s.x, s.y, s.vx, s.vy, s.hp, s.alive);
    return o; };
  if (stage6p) P.tickBulwark = function(dt){
    setM(this);
    const M = this, L0 = simLite(this), oR = this.rng, oMR = Math.random;
    const pre = [this.a, this.b].map(f => {
      const T = f.wallTally, live = !!(f.ultWall && !M.over && f.alive);
      return { f, T, side: f === M.a ? "a" : "b", fade0: f.bulwarkFade, out0: f.bulwarkOut, flash0: f.bulwarkFlash,
               tagged0: f.bulwarkTagged, seen0: f.bulwarkSeen.slice(), live,
               castEdge: live && (!(f.bulwarkFade > 0) || f.bulwarkOut > 0),
               rise: T ? (T.blocks - f.bulwarkSeen[0]) + (T.arrows - f.bulwarkSeen[1]) : 0 }; });
    const event = pre.some(p => p.T && (p.rise > 0 || p.castEdge || (p.fade0 > 0 && !p.live) || p.f.bulwarkScorch.length || p.flash0 > 0));
    const W0 = event ? { a: snapF(this.a), b: snapF(this.b), m: snapM(this, true), g: snapG(false) } : null;
    const floats0 = new Set(this.floats), tags0 = new Set(this.tags);
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oBulwark.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(10, `tickBulwark drew the RNG ${drew}x`);
    const dL = firstDiffA(L0, simLite(this));
    if (dL) fail(10, "tickBulwark changed the sim: " + dL); else inc("bulwarkOk");
    if (W0){
      const moved = [];
      for (const k of ["a", "b"]) for (const d of diffMap(W0[k], snapF(this[k]))) if (!PIC(d)) moved.push(`${k}'s ${d}`);
      for (const d of diffMap(W0.m, snapM(this, true)))
        if (!["floats", "floats=", "tags", "tags=", "taught"].includes(d)) moved.push(`the match's ${d}`);
      for (const d of diffMap(W0.g, snapG(false))) moved.push(`the shared table ${d}`);
      if (moved.length) fail(10, `tickBulwark wrote ${moved.join(", ")}`); else inc("bulwarkFullOk");
    }
    const newFloats = this.floats.filter(q => !floats0.has(q)), newTags = this.tags.filter(g => !tags0.has(g));
    const wantFloats = [], wantTags = [];
    for (const p of pre){
      const f = p.f, T = p.T, Q = pend[p.side];
      if (!T){ if (f.bulwarkFade > 0 || f.bulwarkScorch.length) fail(10, "a bar or a scorch with no wall ever cast"); continue; }
      /* THE BAR IS UP EXACTLY WHILE THE WINDOW IS (and the match runs, and the caster stands) */
      if ((f.bulwarkFade === 1) !== p.live) fail(10, `bulwarkFade ${f.bulwarkFade} with the window ${p.live ? "live" : "not live"} (over ${this.over}, alive ${f.alive})`);
      else if (p.live) inc("barUp");
      else if (f.bulwarkFade > p.fade0) fail(10, `the bar rose (${p.fade0} -> ${f.bulwarkFade}) with no window`);
      else if (f.bulwarkFade > 0) inc("barFolding");
      else if (p.fade0 > 0) inc("foldDone");
      if (p.castEdge) inc("barCast");
      /* EACH CALL SEES EXACTLY THE TICKER'S EVENTS SINCE THE LAST ONE */
      const nB = T.blocks - p.seen0[0], nA = T.arrows - p.seen0[1], got = Math.round(T.banked - p.seen0[2]);
      if (nB !== Q.B || nA !== Q.A) fail(10, `the picture saw ${nB} block(s) and ${nA} arrow(s); the ticker made ${Q.B} and ${Q.A}`);
      if (f.bulwarkSeen[0] !== T.blocks || f.bulwarkSeen[1] !== T.arrows || f.bulwarkSeen[2] !== T.banked) fail(10, "the picture did not take the tally in");
      /* A BLOCK FLASHES THE BAR WHITE (0.066 = two frames on the presentation clock) */
      if (nB > 0){ if (f.bulwarkFlash !== 0.066) fail(10, `a block and the flash at ${f.bulwarkFlash}`); else inc("flashOk", nB); }
      else if (f.bulwarkFlash !== (p.flash0 > 0 ? Math.max(0, p.flash0 - dt) : p.flash0)) fail(10, `the flash ${p.flash0} -> ${f.bulwarkFlash} with no block`);
      /* AN ARROW LEAVES A SCORCH ON THE BAR (min(n, 8) new, each on the bar) */
      const fresh = f.bulwarkScorch.filter(q => q.t === 0);
      if (fresh.length !== Math.min(nA, 8)) fail(10, `${nA} arrow(s) and ${fresh.length} new scorch(es)`);
      else if (fresh.some(q => !(Math.abs(q.s) <= f.w.ult.half) || (q.side !== 1 && q.side !== -1) || q.life !== 0.6)) fail(10, "a scorch off the bar");
      else if (nA) {
        inc("scorchOk", nA);
        /* where it lands on the bar against where the arrow died, along the bar (measured) */
        const u = f.w.ult, ux = Math.cos(f.theta), uy = Math.sin(f.theta), px = -uy, py = ux;
        const cx = f.x + ux * u.ahead, cy = f.y + uy * u.ahead;
        const trueS = Q.at.map(([x, y]) => Math.max(-u.half, Math.min(u.half, (x - cx) * px + (y - cy) * py)));
        for (const q of fresh) if (trueS.length) (q.seen ? scorchD.seen : scorchD.unseen).push(Math.min(...trueS.map(s => Math.abs(s - q.s))));
      }
      Q.A = 0; Q.B = 0; Q.at.length = 0;
      /* THE BANK ON THE CASTER: one "+N" float at its seat, and the WARD tag on the window's first bank */
      if ((nA > 0 || nB > 0) && got >= 1 && f.alive){
        wantFloats.push(["+" + got, f.x, f.y - 44]);
        if (!(p.castEdge ? false : p.tagged0)) wantTags.push("ward");
      }
    }
    const gotFloats = newFloats.map(q => [q.text, q.x, q.y]);
    if (js(gotFloats) !== js(wantFloats)) fail(10, `floats ${js(gotFloats)}, want ${js(wantFloats)}`);
    else if (wantFloats.length) inc("floatOk", wantFloats.length);
    const gotTags = newTags.map(g => g.key);
    if (js(gotTags) !== js(wantTags)) fail(10, `tags ${js(gotTags)}, want ${js(wantTags)}`);
    else if (wantTags.length) inc("tagOk", wantTags.length);
    return r;
  };

  /* THE WINDOW CLOCK. The engine's early returns (over, the latch, the split
     hold, a hit stop) come before every window ticker, so the wall's clock is
     the window tickers' clock only if its ticker runs exactly once on every
     live step and never on a frozen one. Read from the step, not assumed. */
  let lwCalls = 0, lwFrozen = false;
  P.step = function(dt){
    if (postOver) return oStep.call(this, dt);
    const frozen =!!(this.hitStop > 0 || this.latch || this.splitHold), live = !this.over && !frozen;
    for (const f of [this.a, this.b]) if (f.ultWall){ if (frozen) inc("winFrozen"); else inc("winLive"); }
    lwCalls = 0; lwFrozen = frozen && !this.over;
    const r = oStep.call(this, dt);
    if (live && lwCalls !== 1) fail(1, `the wall's ticker ran ${lwCalls} times on a live step`);
    else if (live) inc("liveTicks");
    lwFrozen = false;
    return r;
  };
  P.fireUlt = function(f, foe){
    if (f.w.id !== "lightkeeper") return oFire.call(this, f, foe);
    if (f.ultWall) fail(1, "a cast under a standing wall");
    /* The snapshot is taken INSIDE the cast, when the shared prologue assigns
       `ultFx` (its last statement before the kind branches, which only test
       u.kind until "lightwall"): an accessor on this match for the length of
       the call, put back as the plain field it was, in the same key order. */
    setM(this);
    const M = this, key = f === this.a ? "a" : "b";
    let cur = this.ultFx, sets = 0, S0 = null;
    Object.defineProperty(this, "ultFx", { configurable: true, enumerable: true, get(){ return cur; },
      set(v){ cur = v; sets++;
              if (sets === 1) S0 = { a: snapF(M.a), b: snapF(M.b), m: snapM(M, true), g: snapG(false),
                                     tally: f.wallTally ? Object.assign({}, f.wallTally) : null }; } });
    let r;
    const v0 = voices.length;
    try { r = oFire.call(this, f, foe); }
    finally { Object.defineProperty(this, "ultFx", { value: cur, writable: true, enumerable: true, configurable: true }); }
    /* [9] THE RAISE: exactly one Lightkeeper voice inside the cast, the cast's own */
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && lkV(x[1]));
      if (cv.length !== 1 || cv[0][1].w !== "lightkeeper") fail(9, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
      else inc("castVoice");
    }
    const Z = f.ultWall, u = f.w.ult;
    const T0 = S0 && S0.tally, T1 = f.wallTally;
    const tallyOk = T1 && Object.keys(T1).every(k => T1[k] === (k === "casts" ? (T0 ? T0.casts : 0) + 1 : (T0 ? T0[k] : 0)));
    if (!S0 || sets !== 1) fail(2, `the cast's prologue assigned ultFx ${sets} times (read at the first)`);
    else if (!Z || js(Z) !== js({ t: 0, dur: u.dur, cd: 0 })) fail(2, `the cast opened ${JSON.stringify(Z)}`);
    else if (!tallyOk) fail(2, `the tally ${JSON.stringify(T0)} -> ${JSON.stringify(T1)}`);
    else {
      const bad2 = [];
      for (const k of ["a", "b"]){ const F = this[k];
        for (const d of diffMap(S0[k], snapF(F)))
          if (!(k === key && (d === "ultWall" || d === "wallTally"))) bad2.push(`${k === key ? "the caster" : "the foe"}'s ${d}`); }
      for (const d of diffMap(S0.m, snapM(this, true))) bad2.push(`the match's ${d}`);
      for (const d of diffMap(S0.g, snapG(false))) bad2.push(`the shared table ${d}`);
      if (bad2.length) fail(2, `the cast also wrote ${bad2.join(", ")}`);
      else inc("castOk");
    }
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!self.w || self.w.id !== "lightkeeper" || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultWall, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
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
  P.tickLightwall = function(dt){
    lwCalls++;
    if (lwFrozen) fail(1, "the wall's ticker ran on a frozen step (the lab's clock, not the window's)");
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultWall && f.w.id !== "lightkeeper") fail(1, `${f.w.id} carries ultWall`);
      const Z = f.ultWall;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, u: f.w.ult, t1: Z.t + dt, cd1: Z.cd - dt, th: f.theta, x: f.x, y: f.y,
                 sh: f.shield, shMax: f.shieldMax, fAlive: f.alive, foeAlive: foe.alive,
                 fx: foe.x, fy: foe.y, fpin: foe.pin, T0: Object.assign({}, f.wallTally),
                 ward0: f.status.ward ? Object.assign({}, f.status.ward) : null, wardJ: js(f.status.ward) });
    }
    if (!pre.length) return oTick.call(this, dt);
    setM(this);
    if (this.shades && this.shades.length) inc("shadeFrames");
    const shots0 = this.shots.map(s => ({ s, x: s.x, y: s.y, r: s.r, stuck: !!s.stuck, net: !!s.net, vx: s.vx, vy: s.vy, life: s.life, J: js(s) }));
    const st = {};
    for (const f of [this.a, this.b]) st[f === this.a ? "a" : "b"] = { f, x: f.x, y: f.y, vx: f.vx, vy: f.vy, hp: f.hp, sh: f.shield, shMax: f.shieldMax, S: snapF(f) };
    const M0 = snapM(this, false), G0 = snapG(false);
    const hs0 = this.hitStop, calls = [], oHurt = this.hurt, oBeat = this.beat, oRng = this.rng;
    this.hurt = function(){ calls.push("hurt"); return oHurt.apply(this, arguments); };
    this.beat = function(){ calls.push("beat"); return oBeat.apply(this, arguments); };
    this.rng = function(){ calls.push("rng"); return oRng(); };
    let r;
    const v0 = voices.length;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; }
    /* [7] NOTHING ELSE */
    if (calls.length) fail(7, `the wall called ${calls.join(",")}`);
    if (this.hitStop !== hs0) fail(7, `hitStop ${hs0} -> ${this.hitStop}`);
    for (const k of ["a", "b"]){ const o = st[k], f = o.f;
      if (f.x !== o.x || f.y !== o.y) fail(7, `${f.w.id}'s position moved`);
      if (f.hp !== o.hp) fail(7, `${f.w.id}'s hp moved`); }
    /* [7] THE WHOLE-STATE DIFF: only what another check rebuilds may move */
    {
      const allow = { a: new Set(), b: new Set() };
      for (const p of pre){ const k = p.f === this.a ? "a" : "b", fk = k === "a" ? "b" : "a";
        for (const d of ["ultWall", "wallTally", "shield", "shieldMax", "status.ward"]) allow[k].add(d);   // [1] [3] [4] [6]
        allow[fk].add("vx"); allow[fk].add("vy"); }                                                        // [5]
      const moved = [];
      for (const k of ["a", "b"]){ const f = st[k].f;
        for (const d of diffMap(st[k].S, snapF(f))) if (!allow[k].has(d)) moved.push(`${f.w.id}'s ${d}`); }
      for (const d of diffMap(M0, snapM(this, false))) moved.push(`the match's ${d}`);
      for (const d of diffMap(G0, snapG(false))) moved.push(`the shared table ${d}`);
      if (moved.length) fail(7, `the wall also moved ${moved.join(", ")}`);
      else inc("stateOk");
    }
    /* THE MODEL: which arrows must die, whether the foe must be turned back */
    const alive = shots0.filter(o => true);
    const expectDead = new Set(), expectVel = { a: [st.a.vx, st.a.vy], b: [st.b.vx, st.b.vy] };
    let open = 0;
    for (const p of pre){
      const { f, foe, Z, u } = p, T = f.wallTally, k = f === this.a ? "a" : "b", fk = k === "a" ? "b" : "a";
      if (p.t1 >= Z.dur || !p.fAlive || !p.foeAlive){
        /* [1] THE CLOSE. A window that should have closed and did not is [1]'s
           failure alone: the frame is then judged as the wall frame it was, so
           one broken sentence does not read as four. */
        if (f.ultWall) fail(1, "the window did not close");
        else {
          if (p.fAlive && p.foeAlive && p.t1 < Z.dur - 1e-9) fail(1, "closed early");
          else { inc("closes"); inc(p.t1 >= Z.dur && p.fAlive && p.foeAlive ? "clockCloses" : "deathCloses"); }
          if (T.frames !== p.T0.frames || T.blocks !== p.T0.blocks || T.arrows !== p.T0.arrows) fail(1, "a closing frame did something");
          if (f.shield !== p.sh || f.shieldMax !== p.shMax || js(f.status.ward) !== p.wardJ) fail(6, "a closing frame banked");
          continue;
        }
      }
      open++;
      inc("frames");
      if (!f.ultWall){ fail(1, `closed at ${p.t1.toFixed(3)} of ${Z.dur}`); continue; }
      if (f.ultWall !== Z || Z.t !== p.t1){ fail(1, `the window's clock ${Z.t}, want ${p.t1}`); continue; }
      if (T.frames !== p.T0.frames + 1) fail(1, "frames not counted");
      const Wl = wallOf(p.th, p.x, p.y, u);
      /* [3] ARROWS */
      let want = 0;
      for (let i = alive.length - 1; i >= 0; i--){
        const o = alive[i];
        if (o.stuck || expectDead.has(o)) continue;
        if (segd(Wl.ax, Wl.ay, Wl.bx, Wl.by, o.x, o.y) < (o.r || 6) + u.shotPad){ expectDead.add(o); want++; }
      }
      const dA = T.arrows - p.T0.arrows;
      /* [4] THE CONTACT AND THE CADENCE */
      const dB = T.blocks - p.T0.blocks;
      const dd = segd(Wl.ax, Wl.ay, Wl.bx, Wl.by, p.fx, p.fy), inRange = dd < R + u.ballPad;
      const shouldBlock = p.cd1 <= 0 && !(p.fpin > 0) && inRange;
      if (inRange && p.cd1 <= 0 && p.fpin > 0) inc("pinnedContact");
      if (dB > 1) fail(4, `${dB} blocks in one frame`);
      if (dB === 1){
        inc("blocks");
        if (!shouldBlock) fail(4, `a block with d ${dd.toFixed(3)} (pad ${R + u.ballPad}), cd ${p.cd1}, pin ${p.fpin}`);
        const lb = lastBlock.get(Z);
        if (lb !== undefined && p.t1 - lb < u.cd - 1e-9) fail(4, `blocks ${(p.t1 - lb).toFixed(3)}s apart`);
        lastBlock.set(Z, p.t1);
        if (Z.cd !== u.cd) fail(4, `cd ${Z.cd} after a block`);
        else inc("blockOk");
        /* [5] THE SHOVE, from the frame's own wall and the foe where it stood */
        const side = ((p.fx - Wl.cx) * Wl.ux + (p.fy - Wl.cy) * Wl.uy) >= 0 ? 1 : -1;
        const kx = Wl.ux * side, ky = Wl.uy * side, kl = Math.hypot(kx, ky) || 1;
        expectVel[fk] = [expectVel[fk][0] + kx / kl * u.shove, expectVel[fk][1] + ky / kl * u.shove];
        inc(side > 0 ? "blockAhead" : "blockBehind");
      } else {
        if (shouldBlock) fail(4, "a clear, unpinned contact and no block");
        if (Z.cd !== p.cd1) fail(4, `cd ${p.cd1} -> ${Z.cd} with no block`);
      }
      /* [6] THE BANK, from the blocks that happened, in the engine's order */
      let sh = p.sh, banks = 0;
      if (u.bankShot > 0) for (let i = 0; i < dA; i++){ sh = Math.min(W.cap, sh + u.bankShot); banks++; }
      if (u.bankBall > 0 && dB === 1){ sh = Math.min(W.cap, sh + u.bankBall); banks++; }
      const dK = T.banks - p.T0.banks;
      if (f.shield !== sh) fail(6, `shield ${p.sh} -> ${f.shield}, want ${sh} (${dA} arrows, ${dB} blocks)`);
      else if (dK !== banks) fail(6, `${dK} banks, want ${banks}`);
      else if (banks && f.shieldMax !== Math.max(p.shMax, sh)) fail(6, `shieldMax ${f.shieldMax}, want ${Math.max(p.shMax, sh)}`);
      else if (!banks && f.shieldMax !== p.shMax) fail(6, "shieldMax moved with no bank");
      else if (js(f.status.ward) !== (banks ? js(wardAfter(p.ward0, banks)) : p.wardJ))
        fail(6, banks ? `the ward ${p.wardJ} -> ${js(f.status.ward)}, want ${js(wardAfter(p.ward0, banks))} (apply("ward", 1) x ${banks})`
                      : `the ward moved with no bank: ${p.wardJ} -> ${js(f.status.ward)}`);
      else if (Math.abs((T.banked - p.T0.banked) - (sh - p.sh)) > 1e-9) fail(6, "banked miscounted");
      else { inc("bankFrameOk"); if (banks) inc("bankOk", banks); }
      p.dA = dA; p.dB = dB; p.want = want;
    }
    /* [9] THE CALL'S VOICES: exactly its events', in order -- a tink an arrow
       (k its index among the call's kills), then a gong a block; on a closing
       frame the fold iff the close is by the clock with both alive -- and
       nothing else (the wall hurts nobody: no shatter voice can sound here). */
    if (stage6v){
      const tv = voices.slice(v0), got = [], other = [], want = [];
      for (const x of tv){ if (x[0] === "ult" && lkV(x[1])) got.push(x[1].w + (x[1].w === "lightkeeper-tink" ? ":" + x[1].k : "")); else other.push(vname(x)); }
      let K = 0, closes = [];
      for (const p of pre){
        if (p.dA === undefined){                                   // a closing frame
          const byClock = p.t1 >= p.Z.dur && p.fAlive && p.foeAlive;
          if (byClock) want.push("lightkeeper-fold");
          closes.push(byClock); continue; }
        for (let i = 0; i < p.dA; i++) want.push("lightkeeper-tink:" + (K++));
        if (p.dB === 1) want.push("lightkeeper-gong");
      }
      if (JSON.stringify(got) !== JSON.stringify(want)) fail(9, `tickLightwall voiced ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
      else if (other.length) fail(9, `tickLightwall also played ${JSON.stringify(other)}`);
      else {
        for (const w of want){ if (w === "lightkeeper-fold") inc("foldVoice"); else if (w === "lightkeeper-gong") inc("gongVoice"); else inc("tinkVoice"); }
        if (K > 1) inc("tinkFlamFrames");
        for (const c of closes) inc(c ? "clockCloseFold" : "deathCloseSilent");
      }
    }
    /* THE PICTURE'S EVENTS: counted for the picture's next call (see tickBulwark) */
    if (stage6p) for (const p of pre){
      if (p.dA === undefined) continue;
      const Q = pend[p.f === this.a ? "a" : "b"];
      Q.A += p.dA; Q.B += p.dB;
      if (p.dA) for (const o of shots0) if (expectDead.has(o)) Q.at.push([o.x, o.y]);
    }
    /* [3] THE ARROWS THAT DIED, against the model */
    const now = new Set(this.shots);
    let killed = 0, arrowsCounted = 0;
    for (const p of pre) if (p.dA !== undefined) arrowsCounted += p.dA;
    for (const o of shots0){
      const s = o.s, gone = !now.has(s), nowStuck = !!s.stuck && !o.stuck;
      const died = gone || nowStuck;
      if (died) killed++;
      /* every field of every shot, not just its motion (second review round) */
      if (o.stuck){ if (gone || js(s) !== o.J) fail(3, "a stuck arrow was touched"); continue; }
      if (expectDead.has(o)){
        const endpoint = () => js(Object.assign(JSON.parse(o.J), { stuck: true, vx: 0, vy: 0, life: 1e9 }));
        if (!died) fail(3, `an arrow inside the wall survived (r ${o.r}, net ${o.net})`);
        else if (o.net && (gone || js(s) !== endpoint())) fail(3, "a net arrow killed without exactly the endpoint write");
        else if (!o.net && !gone) fail(3, "a non-net arrow not spliced");
        else inc(o.net ? "netStuck" : "arrowOk");
      } else if (died) fail(3, `an arrow outside the wall died (r ${o.r})`);
      else if (js(s) !== o.J) fail(3, "a live arrow outside the wall was changed");
    }
    /* COUNTED, NOT CHECKED: a Crossweave volley the wall left with every
       arrow stuck. tickShots would have released it in the same pass; here
       it waits for the next tickShots (the builder's reading 2). */
    { const vs = new Set();
      for (const o of shots0) if (o.net && expectDead.has(o) && now.has(o.s)) vs.add(o.s.volley);
      for (const v of vs) if (this.shots.every(s => !s.net || s.volley !== v || s.stuck)) inc("volleysHeld"); }
    for (const s of this.shots) if (!shots0.some(o => o.s === s)) fail(3, "the wall made a shot");
    if (killed !== arrowsCounted) fail(3, `${killed} arrows died, ${arrowsCounted} counted`);
    if (killed) inc("arrowsKilled", killed);
    /* [5] VELOCITIES: only the shoves */
    for (const k of ["a", "b"]){ const f = st[k].f, e = expectVel[k];
      if (f.vx !== e[0] || f.vy !== e[1]) fail(5, `${f.w.id} v ${f.vx},${f.vy} want ${e[0]},${e[1]}`);
      else if (e[0] !== st[k].vx || e[1] !== st[k].vy) inc("shoveOk"); }
    /* a fighter without a wall: its shield untouched */
    for (const k of ["a", "b"]){ const f = st[k].f;
      if (!pre.some(p => p.f === f) && (f.shield !== st[k].sh || f.shieldMax !== st[k].shMax)) fail(6, "the wall banked on the foe"); }
    return r;
  };

  const foes = foeList.length ? foeList : AC.WEAPONS.map(w => w.id).filter(i => i !== "lightkeeper");
  const T = { casts: 0, frames: 0, shieldSum: 0, blocks: 0, arrows: 0, banks: 0, banked: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0, shieldFight = 0;
  setM(null);
  const G00 = snapG(true);   // [7] the shared module tables: no build may write them
  /* THE DRAWN SUBSET (stage 6's picture): the first seed, both sides, every
     foe, drawn through the renderer every `drawEvery` steps while any of the
     picture shows (every 60th otherwise), through the kill and the verdict,
     the sim read before and after each frame and the match's RNG watched.
     The post chain is off: this asks what a draw WRITES, not what it looks
     like (render_ab and the picture lab answer that). */
  const drawOn = stage6p && drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.bulwarkFade > 0 || q.bulwarkScorch.length);
    if (!(vis ? steps % drawEvery === 0 : steps % 60 === 0)) return;
    setM(m);
    const s0 = simDraw(m), oR = m.rng, u0 = memoSnap(); let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    try { AC.__draw(m); } catch (e){ fail(10, "a drawn frame threw: " + String((e && e.message) || e)); }
    finally { m.rng = oR; }
    /* the renderer's own memos: what this draw wrote to an underscore key of
       SHAPES becomes [7]'s start for it (see memoSnap) */
    const u1 = memoSnap();
    for (const k of new Set([...u0.keys(), ...u1.keys()])) if (u0.get(k) !== u1.get(k)){
      drawMemo.add(k);
      if (u1.has(k)) G00.set("SHAPES." + k, u1.get(k)); else G00.delete("SHAPES." + k); }
    const d = firstDiffA(s0, simDraw(m));
    if (dr) fail(10, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(10, "a drawn frame changed the sim: " + d);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };
  for (const side of sides) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "lightkeeper", sd) : new AC.Match("lightkeeper", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    voices.length = 0;
    for (const k of ["a", "b"]){ pend[k].A = 0; pend[k].B = 0; pend[k].at.length = 0; }
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++; bin += per.in; bout += per.out;
    /* THE VERDICT (stage 6): 0.51s past `over`, the step hook passing straight
       through. A bar up at `over` folds to 0 in it; every event has been shown;
       and no Lightkeeper voice sounds in it (the run's accounting below). */
    if (stage6p && m.over){
      const upAtOver = me.bulwarkFade > 0;
      postOver = true;
      try { for (let k = 0; k < 61; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
      finally { postOver = false; }
      if (upAtOver){ if (me.bulwarkFade !== 0) fail(10, `a bar up at \`over\` still at ${me.bulwarkFade} 0.51s into the verdict`); else inc("foldAtVerdict"); }
      if (pend.a.A || pend.a.B || pend.b.A || pend.b.B) fail(10, "a block or an arrow the picture never showed");
    }
    setM(null);
    { const d = diffMap(G00, snapG(true));
      if (d.length) fail(7, `the shared table(s) ${d.join(", ")} written (${fid}, seed ${sd})`); else inc("rowOk"); }
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.wallTally){ for (const k in T) T[k] += me.wallTally[k];
      if (me.wallTally.frames) shieldFight += me.wallTally.shieldSum / me.wallTally.frames; }
  }
  P.tickLightwall = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep;
  if (stage6p) P.tickBulwark = oBulwark;
  if (stage6v){
    if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
    /* EVERY LIGHTKEEPER VOICE OF THE RUN, ACCOUNTED FOR by its event (the verdicts included) */
    const want = { "lightkeeper": n.castVoice || 0, "lightkeeper-gong": n.gongVoice || 0,
                   "lightkeeper-tink": n.tinkVoice || 0, "lightkeeper-fold": n.foldVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(lkAll)]))
      if ((lkAll[k] || 0) !== (want[k] || 0)) fail(9, `${lkAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  for (const [pr] of TAGS) delete pr.toJSON;
  const q = (v, p) => { if (!v.length) return null; const s = v.slice().sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
  const scorch = { seen: [scorchD.seen.length, q(scorchD.seen, 0.5), q(scorchD.seen, 0.95), scorchD.seen.length ? Math.max(...scorchD.seen) : null],
                   unseen: [scorchD.unseen.length, q(scorchD.unseen, 0.5), q(scorchD.unseen, 0.95), scorchD.unseen.length ? Math.max(...scorchD.unseen) : null] };
  const u = AC.WEAPONS.find(w => w.id === "lightkeeper").ult;
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights,
           shieldFight: shieldFight / fights, stage6v, stage6p, drawOn, lkAll, scorch, drawMemo: [...drawMemo].sort(),
           u: { charge: u.charge, dur: u.dur, ahead: u.ahead, half: u.half, shotPad: u.shotPad, ballPad: u.ballPad,
                cd: u.cd, shove: u.shove, bankBall: u.bankBall, bankShot: u.bankShot },
           dmg: AC.WEAPONS.find(w => w.id === "lightkeeper").dmg };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickLightwall === 'function'"):
        raise SystemExit("no tickLightwall in this build -- not a Bulwark link (stage 2+)")
    seeds = [a.seed0 + a.seedstep * i for i in range(a.seeds)]
    foe_list = [x for x in a.foes.split(",") if x]
    R = page.evaluate(JS, [seeds, foe_list, [{"A": 0, "B": 1}[c] for c in a.sides], 0 if a.no_draw else a.draw_every])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
frozen = n.get("winFrozen", 0) / max(1, n.get("winFrozen", 0) + n.get("winLive", 0))
bank_on = U["bankBall"] or U["bankShot"]
print(f"\nBULWARK PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Lightkeeper {'both sides' if a.sides == 'AB' else 'side ' + a.sides} x "
      f"{'every foe' if not a.foes else str(len(a.foes.split(','))) + ' foes'} x {a.seeds} seeds)   blade {R['dmg']}   ult {U}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   per cast: blocks {T['blocks']/casts:.2f}  arrows {T['arrows']/casts:.2f}  "
      f"banked {T['banked']/casts:.2f}   shield on a window frame {T['shieldSum']/max(1,T['frames']):.2f} "
      f"(per fight, windowless as 0: {R['shieldFight']:.2f})   Lightkeeper win {R['win']:.1%}")
print(f"  blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   window frames a cast "
      f"{T['frames']/casts:.1f} (dur x 120 = {U['dur']*120:.0f})   blocks ahead / behind the wall "
      f"{n.get('blockAhead',0)} / {n.get('blockBehind',0)}   pinned contacts passed over {n.get('pinnedContact',0)}")
print(f"  net arrows stuck {n.get('netStuck',0)}   other arrows spliced {n.get('arrowOk',0)}   "
      f"closes: clock {n.get('clockCloses',0)}, death {n.get('deathCloses',0)}   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen (a window is ~{U['dur']/(1-frozen):.2f}s of match time)")
print(f"  whole-state diffs clean: {n.get('stateOk',0)} wall frames ({n.get('shadeFrames',0)} with a shade in the hall), "
      f"{n.get('castOk',0)} casts, {n.get('rowOk',0)} fights' shared tables (WEAPONS STATUS CONFIG AFFINITIES SHAPES)   "
      f"Crossweave volleys the wall left fully stuck (released at the next tickShots, reading 2): {n.get('volleysHeld',0)}")
checks = [
    (1, "the window is `dur` on the window clock, closes on either death; no cast under a wall; only Lightkeeper carries ultWall",
        n.get("closes", 0) > 0 and n.get("clockCloses", 0) > 0),
    (2, "the nova is out: a cast opens exactly {t 0, dur, cd 0} and writes nothing else (whole state and shared tables, from the prologue's end)",
        n.get("castOk", 0) > 0),
    (3, "arrows within (r || 6) + shotPad of the rebuilt wall die (net: exactly the endpoint write; else spliced), no other shot is touched",
        n.get("arrowsKilled", 0) > 0),
    (4, "a block exactly when the foe is inside R + ballPad, unpinned, the cooldown clear; never closer than cd",
        n.get("blockOk", 0) > 0),
    (5, "the shove: exactly `shove` along the normal to the foe's side of the wall; no other velocity", n.get("shoveOk", 0) > 0),
    (6, "the bank: min(cap, shield + bankShot) an arrow, + bankBall a block, shieldMax, apply(\"ward\", 1) exactly (none at bank 0)",
        (n.get("bankOk", 0) > 0) if bank_on else n.get("bankFrameOk", 0) > 0),
    (7, "nothing else: no hurt, beat, rng draw or hit stop; a whole-state diff of both fighters, the match (shades too) and the shared tables",
        n.get("frames", 0) > 0 and n.get("stateOk", 0) > 0 and n.get("rowOk", 0) > 0),
    (8, "the sword swings as ever: every blow the greatsword's own, rebuilt exactly, in the window and out",
        n.get("blowInOk", 0) > 0 and n.get("blowOutOk", 0) > 0),
]
if R.get("stage6v"):
    print(f"  stage 6 voice: raises {n.get('castVoice',0)}  tinks {n.get('tinkVoice',0)} ({n.get('tinkFlamFrames',0)} calls with "
          f"two or more, flammed by k)  gongs {n.get('gongVoice',0)}  folds {n.get('foldVoice',0)} (= clock closes both alive "
          f"{n.get('clockCloseFold',0)})  death closes silent {n.get('deathCloseSilent',0)}   run totals {R['lkAll']}")
    checks.append((9, "stage 6 voice: one raise a cast; a tink an arrow (k its index in the call) then a gong a block, in order; "
                      "the fold on a clock close with both alive and never on a death; nothing else in the ticker; every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "tinkVoice", "gongVoice", "foldVoice", "clockCloseFold",
                                                 "deathCloseSilent", "tinkFlamFrames"))))
if R.get("stage6p"):
    sc = R["scorch"]
    fmt = lambda v: "-" if v is None else f"{v:.1f}"
    print(f"  stage 6 picture: tickBulwark calls clean {n.get('bulwarkOk',0)} (whole-state on {n.get('bulwarkFullOk',0)} event calls)  "
          f"bar up {n.get('barUp',0)}, casts {n.get('barCast',0)}, folding {n.get('barFolding',0)}, folds done {n.get('foldDone',0)} "
          f"({n.get('foldAtVerdict',0)} in the verdict)  flashes {n.get('flashOk',0)}  scorches {n.get('scorchOk',0)}  "
          f"'+N' floats {n.get('floatOk',0)}  WARD tags {n.get('tagOk',0)}")
    print(f"  scorch along the bar vs where the arrow died (units; measured, not gated): seen n {sc['seen'][0]} "
          f"p50 {fmt(sc['seen'][1])} p95 {fmt(sc['seen'][2])} max {fmt(sc['seen'][3])}   never seen n {sc['unseen'][0]} "
          f"p50 {fmt(sc['unseen'][1])} p95 {fmt(sc['unseen'][2])} max {fmt(sc['unseen'][3])}   drawn frames {n.get('drawOk',0)} "
          f"({n.get('drawPic',0)} with the picture up, {n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawVerdict',0)} in the verdict)"
          + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    if R.get("drawOn"):
        print(f"  SHAPES keys the renderer wrote on drawn frames, taken into [7]'s start as each draw wrote them: "
              f"{', '.join(R['drawMemo']) or 'none'}")
    checks.append((10, "stage 6 picture: tickBulwark writes no sim field (every call; whole state on event calls) and draws no RNG; "
                       "the bar up exactly while the window is; every block flashed, every arrow scorched, every bank one '+N', "
                       "WARD once a window; folded in the verdict; no drawn frame throws, draws the RNG or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("bulwarkOk", "bulwarkFullOk", "barUp", "barCast", "barFolding", "foldDone",
                                                 "foldAtVerdict", "flashOk", "scorchOk", "floatOk", "tagOk"))
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
