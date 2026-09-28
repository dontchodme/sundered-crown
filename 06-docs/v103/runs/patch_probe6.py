"""Add stage 6's two checks ([8] the voice, [9] the picture) to tools/coldiron_probe.py.

Bindweed's [10]/[11] pattern: each check switches itself on from the page (the voice's arms in
AC.SFX.play.toString(), the picture's hook on the Match), so the same probe still gates stages
2-5 with 7 checks. Refuses to run twice.
"""
import pathlib, hashlib

p = pathlib.Path("C:/dev/sundered-crown/tools/coldiron_probe.py")
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "stage6v" in s:
    raise SystemExit("the probe already has stage 6")
assert hashlib.sha256(s.encode()).hexdigest()[:16] == "bc34ecee5ad1ab30"

reps = [
# ---- the docstring
('''      beat; a clank that files anything but its own one beat and its own stop
"""''',
'''      beat; a clank that files anything but its own one beat and its own stop
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
# ---- the stage-6 setup and the tickIron hook
('''  let curM = null, per = null;
''',
'''  let curM = null, per = null, postOver = false;

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
'''),
# ---- the step hook passes straight through after `over` (the verdict run)
('''    if (!me) return oStep.call(this, dt);
    const other = me === this.a ? this.b : this.a;''',
'''    if (!me || postOver) return oStep.call(this, dt);
    const other = me === this.a ? this.b : this.a;'''),
# ---- resolveClank: the anvil voice, and the won bind's contact
('''    const pA = snap(A), pB = snap(B), hs0 = this.hitStop, open = !!me.ultTemper;''',
'''    const pA = snap(A), pB = snap(B), hs0 = this.hitStop, open = !!me.ultTemper, v0 = voices.length;'''),
('''    /* [7] THE CLANK'S OWN BEAT AND ITS OWN STOP, NOTHING MORE */''',
'''    if (iron) wonAt.set(W, { x: hx, y: hy });
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
    /* [7] THE CLANK'S OWN BEAT AND ITS OWN STOP, NOTHING MORE */'''),
# ---- fireUlt: the cast voice
('''    const r = oFire.call(this, f, foe);
    const Z = f.ultTemper;''',
'''    const v0 = voices.length;
    const r = oFire.call(this, f, foe);
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ciVoice(x[1]));
      if (cv.length !== 1 || cv[0][1].w !== "coldiron") fail(8, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
      else inc("castVoice");
    }
    const Z = f.ultTemper;'''),
# ---- tickTemper: the close voice
('''    let r;
    try { r = oTick.call(this, dt); }
    finally { this.rng = oRng; delete this.hurt; delete this.beat; for (const f of both) delete f.apply; }''',
'''    const v0 = voices.length;
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
    }'''),
# ---- the fight loop: the drawn subset and the verdict
('''  let fights = 0, wins = 0, decided = 0;
  for (const sd0 of [0, 1]) for (const fid of foes) for (const sd of seeds){''',
'''  let fights = 0, wins = 0, decided = 0;
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
  for (const sd0 of [0, 1]) for (const fid of foes) for (const sd of seeds){'''),
('''    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++;''',
'''    let steps = 0;
    voices.length = 0; wonAt.clear();
    const drawn = drawOn && sd === seeds[0];
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++;'''),
('''    if (me.ultTemper){ if (m.over) inc("openAtOver"); else inc("openAtLimit"); }''',
'''    if (me.ultTemper){ if (m.over) inc("openAtOver"); else inc("openAtLimit"); }
    /* THE VERDICT (stage 6): 0.5s past `over`, the step hook passing straight
       through. A window still set at `over` cools its blades to 0 in it. */
    if (stage6p && m.over){
      const setAtOver = !!me.ultTemper;
      postOver = true;
      try { for (let k = 0; k < 60; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
      finally { postOver = false; }
      if (setAtOver){ if (me.ironFade !== 0) fail(9, `a window set at \\`over\\` still shows iron ${me.ironFade} 0.5s into the verdict`); else inc("verdictCoolOk"); }
    }'''),
# ---- the run's end: the accounting
('''  P.step = oStep; P.move = oMove; P.resolveClank = oClank; P.resolveHit = oHit; P.fireUlt = oFire; P.tickTemper = oTick;''',
'''  P.step = oStep; P.move = oMove; P.resolveClank = oClank; P.resolveHit = oHit; P.fireUlt = oFire; P.tickTemper = oTick;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY COLDIRON VOICE OF THE RUN, ACCOUNTED FOR by its event. */
    const want = { "coldiron": n.castVoice || 0, "coldiron-anvil": n.anvilVoice || 0, "coldiron-close": n.closeVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(ciAll)]))
      if ((ciAll[k] || 0) !== (want[k] || 0)) fail(8, `${ciAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickIron = oIron;'''),
('''  return { n, bad, T, S, fights, win: wins / decided, TICKS, hasSlosh,''',
'''  return { n, bad, T, S, fights, win: wins / decided, TICKS, hasSlosh, stage6v, stage6p, drawOn, ciAll,'''),
# ---- the Python side
('''    R = page.evaluate(JS, [seeds])''', '''    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])'''),
('''ok = 0
for k, text, cover in checks:''',
'''if R.get("stage6v"):
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
for k, text, cover in checks:'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("probe stage 6 written:", hashlib.sha256(s.encode()).hexdigest()[:16])
