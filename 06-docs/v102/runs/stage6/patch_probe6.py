"""Add stage 6's two checks ([10] the voice, [11] the picture) to tools/lodestone_probe.py.

Ironhail's / Bindweed's / Coldiron's pattern: each check switches itself on from the page (the voice's
arms in AC.SFX.play.toString(), the picture's hook on the Match), so the same probe still gates stages
2, 3 and 5 with 10 checks. Refuses to run twice.
"""
import pathlib, hashlib

p = pathlib.Path("C:/dev/sundered-crown/tools/lodestone_probe.py")
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "stage6v" in s:
    raise SystemExit("the probe already has stage 6")
assert hashlib.sha256(s.encode()).hexdigest()[:16] == "85b2d01e7897d0c7"

reps = [
# ---- the docstring
('''  [9] "the next cast does not wait for anything": a cast while the walls are
      lit, or a tickCharge that leaves the charge at or over `ult.charge` with
      the caster alive (a cast held back)
"""''',
'''  [9] "the next cast does not wait for anything": a cast while the walls are
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
"""'''),
# ---- the arguments
('''ap.add_argument("--json", default=None)
a = ap.parse_args()''',
'''ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()'''),
('JS = r"""([seeds]) => {', 'JS = r"""([seeds, drawEvery]) => {'),
# ---- the stage-6 setup and the tickLode hook
('''  const canon = (o) => o == null ? "null" : JSON.stringify(Object.keys(o).sort().map(k => [k, o[k]]));
''',
'''  const canon = (o) => o == null ? "null" : JSON.stringify(Object.keys(o).sort().map(k => [k, o[k]]));

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
'''),
# ---- fireUlt: the cast voice
('''    const r = oFire.call(this, f, foe);
    if (f.ultRunes && !win.has(f.ultRunes))''',
'''    const v0 = voices.length;
    const r = oFire.call(this, f, foe);
    /* [10] THE CAST: exactly one Lodestone voice inside a Lodestone fireUlt, the cast's own; none in any other */
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ldVoice(x[1]));
      if (f.w.id === "lodestone"){
        if (cv.length !== 1 || cv[0][1].w !== "lodestone") fail(10, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
        else inc("castVoice");
      } else if (cv.length) fail(10, `${f.w.id}'s cast played ${JSON.stringify(cv.map(vname))}`);
    }
    if (f.ultRunes && !win.has(f.ultRunes))'''),
# ---- tickRunes: the apply records the count it leaves; the call's voices
('''      const o = who.apply; who.apply = function(k, nn, src){ applies.push([who, k, nn, src]); return o.call(this, k, nn, src); };''',
'''      const o = who.apply; who.apply = function(k, nn, src){ const e = [who, k, nn, src]; applies.push(e); const rr = o.call(this, k, nn, src); e.push(who.stacks(k)); return rr; };'''),
('''    let r;
    try { r = oTick.call(this, dt); }''',
'''    const v0 = voices.length, vexp = [];
    let r;
    try { r = oTick.call(this, dt); }'''),
('''        /* THE CLOSE */
        if (f.ultRunes){ fail(1, "the window did not close"); continue; }''',
'''        /* THE CLOSE */
        vexp.push(p.fAlive && p.foeAlive ? { v: ["lodestone-close"], clock: true } : { v: [], death: true });
        if (f.ultRunes){ fail(1, "the window did not close"); continue; }'''),
('''        } else if (mine.length || !hexOk) fail(4, "an application at hex 0");
''',
'''        } else if (mine.length || !hexOk) fail(4, "an application at hex 0");
        /* [10] the touch's voice (at the count its hex leaves), the hex-snap under it; [11] the touch, for the picture */
        if (u.hex > 0){ const k = mine.length === 1 ? mine[0][4] : "?"; vexp.push({ v: ["lodestone-touch:" + k + "@" + k, "hex-snap"], n: k }); }
        pendTouch[side].push({ x: p.fx, y: p.fy, ins: p.ins, pad: u.pad });
'''),
('''      else inc("nothingElseOk");
    }
    return r;
  };
''',
'''      else inc("nothingElseOk");
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
'''),
# ---- the fight loop: the drawn subset, the verdict, the touch ledger
('''  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "lodestone", sd) : new AC.Match("lodestone", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.runeTally) for (const k in T) T[k] += me.runeTally[k];''',
'''  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
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
      if (upAtOver){ if (me.lodeFade !== 0) fail(11, `walls lit at \\`over\\` still at ${me.lodeFade} 0.51s into the verdict`); else inc("darkAtVerdict"); }
      if (pendTouch.a.length || pendTouch.b.length) fail(11, `${pendTouch.a.length + pendTouch.b.length} touch(es) the picture never saw`);
    }'''),
# ---- the run's end: the accounting
('''  P.tickRunes = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep; P.tickCharge = oCharge;''',
'''  P.tickRunes = oTick; P.resolveHit = oResolve; P.fireUlt = oFire; P.step = oStep; P.tickCharge = oCharge;
  curM = null;
  if (stage6v){
    if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
    /* EVERY LODESTONE VOICE OF THE RUN, ACCOUNTED FOR by its event (every fight, every verdict). */
    const want = { "lodestone": n.castVoice || 0, "lodestone-touch": n.touchVoice || 0, "lodestone-close": n.closeVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(lodeAll)]))
      if ((lodeAll[k] || 0) !== (want[k] || 0)) fail(10, `${lodeAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickLode = oLode;'''),
('''  return { n, bad, T, fights, win: wins / decided,''',
'''  return { n, bad, T, fights, win: wins / decided, stage6v, stage6p, drawOn, lodeAll,'''),
# ---- the Python side
('''    R = page.evaluate(JS, [seeds])''', '''    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])'''),
('''ok = 0
for k, text, cover in checks:''',
'''if R.get("stage6v"):
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
for k, text, cover in checks:'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("probe stage 6 written:", hashlib.sha256(s.encode()).hexdigest()[:16])
