"""Extend tools/heartwood_probe.py with stage 6's checks [9] (the voices) and [10] (the picture's hook). SCRATCH."""
import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_probe.py")
s = p.read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b, 1)


# ---- docstring
rep('''    python heartwood_probe.py --game <link> --stage 2|3|5
''', '''    python heartwood_probe.py --game <link> --stage 2|3|5|6 [--draw-every 6 | --no-draw]
''')
rep('''      "rootfast") -- so the cast hurts, stuns, pins, entangles and moves
      nobody
"""''', '''      "rootfast") -- so the cast hurts, stuns, pins, entangles and moves
      nobody
  STAGE 6 (the picture and the voice, sc-heartwood-b11-fx; v112 §7). Each check
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
"""''')
rep('''ap.add_argument("--stage", required=True, choices=["2", "3", "5"],
                help="the stage the link is: 2 the root, 3 the entangle, 5 the blade (the final)")''',
    '''ap.add_argument("--stage", required=True, choices=["2", "3", "5", "6"],
                help="the stage the link is: 2 the root, 3 the entangle, 5 the blade, 6 the picture and the voice (the final)")''')
rep('''ap.add_argument("--json", default=None)
a = ap.parse_args()''', '''ap.add_argument("--json", default=None)
ap.add_argument("--draw-every", type=int, default=6,
                help="stage 6: on the drawn subset, draw every Nth step while the picture shows")
ap.add_argument("--no-draw", action="store_true", help="stage 6: skip the drawn subset")
a = ap.parse_args()''')

# ---- JS: signature and the stage-6 machinery
rep('''JS = r"""([seeds, PIN]) => {''', '''JS = r"""([seeds, PIN, drawEvery]) => {''')
rep('''  const oStep = P.step, oTick = P.tickRootfast, oRoot = P.rootBlow, oResolve = P.resolveHit,
        oCharge = P.tickCharge, oFire = P.fireUlt, oMove = P.move, oHits = P.tickHits;''',
    '''  const oStep = P.step, oTick = P.tickRootfast, oRoot = P.rootBlow, oResolve = P.resolveHit,
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
  const hwIn = (vs) => vs.filter(v => v[0] === "ult" && (v[2] === HW || v[2] === RV));''')

# ---- snapAll: the picture's own mode
rep('''        if (mode === "tick" && k === "ultRoot" && isHW(m, g)) continue;
        out.push([lab + "." + k, JSON.stringify(ser(m, v, 1, new Set()))]);''',
    '''        if (mode === "tick" && k === "ultRoot" && isHW(m, g)) continue;
        /* the picture's own fields and the held ball's markers (read by Tendril's root picture only) */
        if (mode === "grove" && /^(grove|twine)/.test(k)) continue;
        out.push([lab + "." + k, JSON.stringify(ser(m, v, 1, new Set()))]);''')
rep('''      if (mode === "cast" && CAST_M.has(k)) continue;''',
    '''      if (mode === "cast" && CAST_M.has(k)) continue;
      if (mode === "grove" && k === "tags") continue;     // [10] reads the tags apart: only a count may move''')

# ---- tickRootfast: no voice, at a close or anywhere
rep('''    let s0 = null, drew = 0, r;
    if (watch){
      s0 = snapAll(this, "tick");''', '''    let s0 = null, drew = 0, r;
    const v0 = voices.length;
    if (watch){
      s0 = snapAll(this, "tick");''')
rep('''    for (const p of pre){
      const k = (winCalls.get(p.Z) || 0) + 1; winCalls.set(p.Z, k);''',
    '''    /* [9] THE CLOSE IS SILENT (the design has none), and so is every tick */
    const tv = voices.slice(v0);
    if (stage6v && tv.length) fail(9, `tickRootfast played ${tv.map(v => v[2] || v[0]).join(", ")}${closing ? " at a close" : ""}`);
    for (const p of pre){
      const k = (winCalls.get(p.Z) || 0) + 1; winCalls.set(p.Z, k);
      if (stage6v && !tv.length && (p.t1 >= PIN.dur || !p.fAlive || !p.foeAlive))
        inc(p.fAlive && p.foeAlive ? "clockSilent" : "deathSilent");''')

# ---- rootBlow: one voice a root, none on a killing blow
rep('''    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oRoot.call(this, f); }''', '''    let drew = 0, r;
    const v0 = voices.length, rd0 = f.rootTally ? f.rootTally.rooted : 0;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oRoot.call(this, f); }''')
rep('''    if (drew) fail(6, `rootBlow drew the RNG ${drew}x`);
    const dd = diffSnap(s0, snapAll(this, "root", q, f));''', '''    if (drew) fail(6, `rootBlow drew the RNG ${drew}x`);
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
    const dd = diffSnap(s0, snapAll(this, "root", q, f));''')

# ---- fireUlt: one cast voice a Heartwood cast; none from another relic's
rep('''  P.fireUlt = function(f, foe){
    if (!isHW(this, f)) return oFire.call(this, f, foe);''', '''  P.fireUlt = function(f, foe){
    if (!isHW(this, f)){
      const v0 = voices.length, r0 = oFire.call(this, f, foe);
      if (stage6v && hwIn(voices.slice(v0)).length) fail(9, `${f.w.id}'s cast played a Heartwood voice`);
      return r0;
    }''')
rep('''    const oR = this.rng, oMR = Math.random;
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oFire.call(this, f, foe); }
    finally { this.rng = oR; Math.random = oMR; }
    const u = f.w.ult, side = f === this.a ? 0 : 1, why = [];''', '''    const oR = this.rng, oMR = Math.random, v0 = voices.length;
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
    const u = f.w.ult, side = f === this.a ? 0 : 1, why = [];''')

# ---- tickGrove wrapper, before the fight loop
rep('''  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== HW);
  const row = AC.WEAPONS.find(w => w.id === HW).ult;''', '''  /* [10] THE PICTURE'S HOOK. The sim, cheap, on every call: both fighters'
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
  const row = AC.WEAPONS.find(w => w.id === HW).ult;''')

# ---- the fight loop: voices reset a fight; the drawn subset
rep('''    heldBy.clear();
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }''', '''    heldBy.clear(); voices.length = 0;
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
    }''')
rep('''  P.step = oStep; P.tickRootfast = oTick; P.rootBlow = oRoot; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  return { n, bad, S, wantCalls, u: { charge: row.charge, dur: row.dur, rootFor: row.rootFor, extraEnt: row.extraEnt, blade } };''',
    '''  P.step = oStep; P.tickRootfast = oTick; P.rootBlow = oRoot; P.resolveHit = oResolve;
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
           u: { charge: row.charge, dur: row.dur, rootFor: row.rootFor, extraEnt: row.extraEnt, blade } };''')

# ---- python side
rep('''           "blade": float(HB.BLADE if a.stage == "5" else HB.SHIPPED_DMG), "tip": HB.TIP}
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN])''', '''           "blade": float(HB.BLADE if a.stage in ("5", "6") else HB.SHIPPED_DMG), "tip": HB.TIP}
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN, 0 if a.no_draw else a.draw_every])''')
rep('''ok = 0
for k, text, cover in checks:''', '''S6 = a.stage == "6"
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
for k, text, cover in checks:''')
p.write_text(s, encoding="utf-8", newline="\n")
print("probe patched")
