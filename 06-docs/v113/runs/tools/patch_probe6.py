"""Extend tools/thornwake_probe.py with stage 6's checks [9] (the voices) and [10] (the picture's hook),
the verdict tail, --drawn and --stage 6. Exact-once replacements; refuses a probe that already has them."""
import hashlib, pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/thornwake_probe.py")
s = p.read_bytes().decode("utf-8")
assert "\r" not in s
if "S6V" in s:
    raise SystemExit("the probe already carries stage 6")
before = hashlib.sha256(s.encode()).hexdigest()[:16]
R = []

# ---- 1. the docstring -------------------------------------------------------------------------------------
R.append(('''    python thornwake_probe.py --game <link> --stage 2|3|5
''', '''    python thornwake_probe.py --game <link> --stage 2|3|5|6 [--drawn N]
'''))
R.append(('''  [8] "the charge (the lab's 16 on the game's clock), the window 8": a cast
      not on the frame the live charge clock reaches the builder's charge, or
      a cast while a window is open; the row's charge, window, radius, life,
      cadence, entangle, bite, snare or blade not the pinned stage's
"""''', '''  [8] "the charge (the lab's 16 on the game's clock), the window 8": a cast
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
"""'''))

# ---- 2. the arguments --------------------------------------------------------------------------------------
R.append(('''ap.add_argument("--stage", required=True, choices=["2", "3", "5"],
                help="the stage the link is: 2 the brambles, 3 the snare, 5 the blade (the final)")''',
          '''ap.add_argument("--stage", required=True, choices=["2", "3", "5", "6"],
                help="the stage the link is: 2 the brambles, 3 the snare, 5 the blade (the final), "
                     "6 the picture and the voice (stage 5's numbers)")'''))
R.append(('''ap.add_argument("--json", default=None)
a = ap.parse_args()''', '''ap.add_argument("--json", default=None)
ap.add_argument("--drawn", type=int, default=0, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()'''))

# ---- 3. the JS: signature, and stage 6's machinery after diffSnap ------------------------------------------
R.append(('''JS = r"""([seeds, PIN]) => {''', '''JS = r"""([seeds, PIN, drawEvery]) => {'''))
R.append(('''  const diffSnap = (s0, s1) => {
    if (s0.length !== s1.length) return `the set of fields (${s0.length} -> ${s1.length})`;
    for (let i = 0; i < s0.length; i++)
      if (s0[i][0] !== s1[i][0] || s0[i][1] !== s1[i][1])
        return `${s1[i][0]}: ${s0[i][1].slice(0, 90)} -> ${s1[i][1].slice(0, 90)}`;
    return null;
  };
''', '''  const diffSnap = (s0, s1) => {
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
'''))

# ---- 4. the step wrapper: the verdict tail, and the snared set ---------------------------------------------
R.append(('''  P.step = function(dt){
    const frozen = this.over || !!this.latch || !!this.splitHold || this.hitStop > 0;''',
          '''  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [9]-[10] alone */
    if (tail) return oStep.call(this, dt);
    const frozen = this.over || !!this.latch || !!this.splitHold || this.hitStop > 0;'''))
R.append(('''    for (const q of [...heldBy]) if (!(q.pin > 0) || !q.alive) heldBy.delete(q);
    return r;
  };
''', '''    for (const q of [...heldBy]) if (!(q.pin > 0) || !q.alive) heldBy.delete(q);
    for (const q of [...snared]) if (!(q.pin > 0) || !q.alive) snared.delete(q);
    return r;
  };
'''))

# ---- 5. the tickBramble wrapper: its voices ----------------------------------------------------------------
R.append(('''    const wrapped = [];
    for (const g of [this.a, this.b]){ const o = g.apply; g.apply = function(k, nn, src){ applies.push([g, k, nn, src]); seq.push("apply"); return o.call(this, k, nn, src); }; wrapped.push(g); }
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oR; Math.random = oMR; for (const g of wrapped) delete g.apply; }''',
          '''    const wrapped = [];
    for (const g of [this.a, this.b]){ const o = g.apply; g.apply = function(k, nn, src){ applies.push([g, k, nn, src]); seq.push("apply"); return o.call(this, k, nn, src); }; wrapped.push(g); }
    const vc0 = vctx, vr0 = vrec; vctx = "tickBramble"; vrec = [];
    let heardTick = null;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; this.rng = oR; Math.random = oMR; for (const g of wrapped) delete g.apply;
              heardTick = vrec; vctx = vc0; vrec = vr0; }
    const wantV = [];                     /* [9] the voices this call owes: its snares, then its bites, a caster at a time */
    let closeClock = 0, closeDeath = 0, killV = 0;'''))
R.append(('''      const dSn = T ? T.snares - (p.T ? p.T.snares : 0) : 0;''',
          '''      const dSn = T ? T.snares - (p.T ? p.T.snares : 0) : 0;
      const dTk0 = T ? T.ticks - (p.T ? p.T.ticks : 0) : 0;
      for (let i = 0; i < dSn; i++) wantV.push("thornwake-snare");
      for (let i = 0; i < dTk0; i++) wantV.push("thornwake-bite");
      if (p.closing){ if (p.fAlive && p.foeAlive) closeClock++; else closeDeath++; }
      if (dTk0 && p.hp > 0 && foe.hp <= 0) killV++;
      if (dSn > 0 && foe.pin > 0 && !foe.pinFree && foe.alive){ snared.add(foe); pendSnare.add(foe); }'''))
R.append(('''    if (!shattered){
      if (this.hitStop !== hs0) fail(6, `the hit stop ${hs0} -> ${this.hitStop} with no ward broken`);''',
          '''    if (S6V){
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
      if (this.hitStop !== hs0) fail(6, `the hit stop ${hs0} -> ${this.hitStop} with no ward broken`);'''))

# ---- 6. plantBramble: the crackle --------------------------------------------------------------------------
R.append(('''    try { r = oPlant.call(this, f, q); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(6, `plantBramble drew the RNG ${drew}x`);''',
          '''    const vc0 = vctx, vr0 = vrec; vctx = "plantBramble"; vrec = [];
    let heard = null;
    try { r = oPlant.call(this, f, q); }
    finally { this.rng = oR; Math.random = oMR; heard = vrec; vctx = vc0; vrec = vr0; }
    if (S6V){ const o = oursIn(heard); if (o.length !== 1 || o[0] !== "thornwake-crackle") fail(9, `plantBramble played ${JSON.stringify(o)}, want exactly ["thornwake-crackle"]`); else inc("crackleOk"); }
    if (drew) fail(6, `plantBramble drew the RNG ${drew}x`);'''))

# ---- 7. fireUlt: the cast voice ----------------------------------------------------------------------------
R.append(('''    const r = oFire.call(this, f, foe);
    if (!isTW(this, f) && f.ultBramble) fail(1, `${f.w.id}'s cast opened a bramble window`);''',
          '''    const vc0 = vctx, vr0 = vrec; vctx = isTW(this, f) ? "Thornwake's fireUlt" : "another relic's cast"; vrec = [];
    let r, heard = null;
    try { r = oFire.call(this, f, foe); } finally { heard = vrec; vctx = vc0; vrec = vr0; }
    if (S6V && isTW(this, f)){ const o = oursIn(heard); if (o.length !== 1 || o[0] !== "thornwake") fail(9, `a cast played ${JSON.stringify(o)}, want exactly ["thornwake"]`); else inc("castVoiceOk"); }
    if (!isTW(this, f) && f.ultBramble) fail(1, `${f.w.id}'s cast opened a bramble window`);'''))

# ---- 8. the picture's hook, the drawn subset, and the fight loop -------------------------------------------
R.append(('''  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== TW);
  const W = AC.WEAPONS.find(w => w.id === TW), row = W.ult;''',
          '''  /* [10] THE PICTURE'S HOOK: `tickBrier`, on the presentation clock (tickPresentation: through hit
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
  const W = AC.WEAPONS.find(w => w.id === TW), row = W.ult;'''))
R.append(('''    per = { casts: 0, bin: 0, bout: 0, winSteps: 0, winFrozen: 0 };
    heldBy.clear(); pendingHeld.clear();
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    S.fights++;''', '''    per = { casts: 0, bin: 0, bout: 0, winSteps: 0, winFrozen: 0 };
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
    S.fights++;'''))
R.append(('''  P.step = oStep; P.tickBramble = oTick; P.plantBramble = oPlant; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  const u = {}; for (const k of ROWK) u[k] = row[k];
  u.kind = row.kind; u.blade = W.dmg;
  return { n, bad, S, wantCalls, u };''', '''  P.step = oStep; P.tickBramble = oTick; P.plantBramble = oPlant; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.fireUlt = oFire; P.move = oMove; P.tickHits = oHits;
  if (S6P) P.tickBrier = oBrier;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  const u = {}; for (const k of ROWK) u[k] = row[k];
  u.kind = row.kind; u.blade = W.dmg;
  return { n, bad, S, wantCalls, u, S6V, S6P };'''))

# ---- 9. python: pins, the call, the checks -------------------------------------------------------------------
R.append(('''    PIN["blade"] = float(TB.BLADE if a.stage == "5" else TB.SHIPPED_DMG)
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN])''', '''    PIN["blade"] = float(TB.BLADE if a.stage in ("5", "6") else TB.SHIPPED_DMG)
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN, a.drawn])'''))
R.append(('''print(f"\\n  {ok}/{len(checks)}")''', '''S6V, S6P = R.get("S6V"), R.get("S6P")
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
print(f"\\n  {ok}/{len(checks)}")'''))

for a_, b_ in R:
    c = s.count(a_)
    if c != 1:
        raise SystemExit(f"anchor found {c}x:\n{a_[:200]}")
    s = s.replace(a_, b_, 1)
p.write_bytes(s.encode("utf-8"))
print("probe", before, "->", hashlib.sha256(s.encode()).hexdigest()[:16])
