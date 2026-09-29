"""Extend tools/aureole_probe.py with stage 6's [9] voices and [10] picture hook (+ --drawn N).
Exactly-once text edits on the probe as it stood (afa389b746f9c12b); refuses otherwise."""
import hashlib, pathlib
P = pathlib.Path("C:/dev/sundered-crown/tools/aureole_probe.py")
s = P.read_text(encoding="utf-8")
assert hashlib.sha256(s.encode()).hexdigest()[:16] == "afa389b746f9c12b", "the probe moved"

DOC = '''  [8] a smite tick that kills files its fatal beat for HER side (reading 6:
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
'''
reps = [
 ('''  [8] a smite tick that kills files its fatal beat for HER side (reading 6:
      the side letter; the lab's Fighter would credit side b every time)
''', DOC),
 ('''ap.add_argument("--seedstep", type=int, default=13, help="seeds are seed0 + seedstep x i (the lab's is 11)")
''',
  '''ap.add_argument("--seedstep", type=int, default=13, help="seeds are seed0 + seedstep x i (the lab's is 11)")
ap.add_argument("--drawn", type=int, default=6, help="draw the first seed's fights every Nth step (0 = off)")
'''),
 ('''JS = r"""([seeds, foeList, sides]) => {''', '''JS = r"""([seeds, foeList, sides, drawEvery]) => {'''),
 # the stage-6 machinery, after the probe's own declarations
 ('''  const srcName = s => typeof s === "object" && s ? "a Fighter" : JSON.stringify(s);
''',
  '''  const srcName = s => typeof s === "object" && s ? "a Fighter" : JSON.stringify(s);

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
'''),
 # the verdict passes straight through the step wrapper
 ('''  P.step = function(dt){
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;
''',
  '''  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [9]-[10] alone */
    if (tail) return oStep.call(this, dt);
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;
'''),
 # fireUlt: the cast's voice
 ('''    for (const x of [f, foe]){ const o = x.apply; x.apply = function(k, nn, src){ applies.push([x, k, nn]); return o.call(this, k, nn, src); }; }
    let r;
    try { r = oFire.call(this, f, foe); }
    finally { delete this.hurt; delete f.apply; delete foe.apply; }
''',
  '''    for (const x of [f, foe]){ const o = x.apply; x.apply = function(k, nn, src){ applies.push([x, k, nn]); return o.call(this, k, nn, src); }; }
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
'''),
 # tickHalo: the voices heard in the call
 ('''    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; }
''',
  '''    let r, heard = null;
    const vc0 = vctx, vr0 = vrec; vctx = "halo"; vrec = [];
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oRng; for (const f of fs) delete f.apply; heard = vrec; vctx = vc0; vrec = vr0; }
    const wantV = [], vk = [];   // [9] the voices this call must play, rebuilt, and what passing counts
'''),
 ('''        if (w.fAlive && w.foeAlive){ inc("clockCloses"); const M = winMT.get(Z); if (M){ inc("winMT", M.mt); inc("winMTn"); } }
        else inc("deathCloses");
''',
  '''        if (w.fAlive && w.foeAlive){ inc("clockCloses"); const M = winMT.get(Z); if (M){ inc("winMT", M.mt); inc("winMTn"); }
          wantV.push(["ult", "aureole-close"]); vk.push("closeClockOk"); }
        else { inc("deathCloses"); vk.push("closeDeathQuiet"); }
'''),
 ('''      if (inside && w.d > u.haloR) inc("inRim");     // the + R: inside by the rim, not the centre
      const IN = flag === 1;
''',
  '''      if (inside && w.d > u.haloR) inc("inRim");     // the + R: inside by the rim, not the centre
      const IN = flag === 1;
      /* [9] THE ENTRY: an inside tick after an outside tick of the same window */
      const pIn = prevIn.get(Z);
      if (IN && pIn === false){ wantV.push(["ult", "aureole-enter"]); vk.push("enterOk"); }
      else if (IN) vk.push(pIn === undefined ? "firstInQuiet" : "stayQuiet");
      else vk.push("outQuiet");
      prevIn.set(Z, IN);
'''),
 ('''        expect.push({ who: f, k: "blessing", nn: u.bless, side, before: w.bl, cap: ST.blessing.maxStacks, dur: ST.blessing.dur, chk: 4 });
''',
  '''        expect.push({ who: f, k: "blessing", nn: u.bless, side, before: w.bl, cap: ST.blessing.maxStacks, dur: ST.blessing.dur, chk: 4 });
        wantV.push(["chime", f.stacks("blessing")]); vk.push("chimeOk");
'''),
 ('''    inc("calls");
    return r;
  };
''',
  '''    /* [9] THE HALO'S VOICES: exactly the rebuilt ones, in order, and nothing else */
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
'''),
 # the fight loop: the fight record, the drawn subset, the verdict
 ('''    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
''',
  '''    const me = side ? m.b : m.a;
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
'''),
 ('''  P.step = oStep; P.tickStatus = oStatus; P.beat = oBeat;
''',
  '''  P.step = oStep; P.tickStatus = oStatus; P.beat = oBeat;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play;
            for (const k of OTHER) P[k] = oOther[k]; }
  if (S6P) P.tickBenediction = oBene;
'''),
 ('''  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, u: blk };''',
  '''  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, u: blk,
           s6v: S6V, s6p: S6P, other: OTHER };'''),
 ('''    R = page.evaluate(JS, [seeds, foes, [0, 1] if a.sides == "AB" else [0]])''',
  '''    R = page.evaluate(JS, [seeds, foes, [0, 1] if a.sides == "AB" else [0], a.drawn])'''),
 # the report and the two checks
 ('''if not design:
    bad.setdefault("7", []).append(f"the ult block {U} is not the design's")
''',
  '''g = lambda k: n.get(k, 0)
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
'''),
]
for a_, b_ in reps:
    assert s.count(a_) == 1, (s.count(a_), a_[:90])
    s = s.replace(a_, b_, 1)
P.write_text(s, encoding="utf-8", newline="\n")
print("probe patched:", hashlib.sha256(s.encode()).hexdigest()[:16])
