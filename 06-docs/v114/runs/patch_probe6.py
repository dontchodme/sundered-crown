"""Extend tools/goreshard_probe.py with stage 6's checks [11] (the voices) and [12] (the picture's hook),
detected by their own presence; --stage 6; --drawn N. Every [1]-[10] line stays as it was."""
import pathlib, hashlib
p = pathlib.Path("C:/dev/sundered-crown/tools/goreshard_probe.py")
s = p.read_bytes().decode("utf-8")
assert "\r" not in s
if "[11]" in s:
    raise SystemExit("already extended")
reps = []

# ------------------------------------------------------------------ docstring
reps.append(('''      other attackers' blows that reached the damage line with her window
      open, and with it shut
"""''', '''      other attackers' blows that reached the damage line with her window
      open, and with it shut

STAGE 6 (the picture and the voice, the builder's readings 13-21), each check
run only where the link carries it -- the voices detected by their own
presence in `AC.SFX.play.toString()` (Goreshard's cast arm, `w ===
"oathwound"`, and the priced-blow branch, `kind === "hit" && p.price`), the
picture by `tickGore` on the Match -- so the same probe still gates stages 2
and 5 at 10/10, every line as before; `--stage 6` requires both. Once a fight
is over the probe steps 2 s more of the verdict (the step's `over` path: only
the presentation clock runs) for these two checks alone; [1]-[10] read none of
those steps, and every [1]-[10] number on the stage-6 link must be the stage-5
link's, line for line (the picture and the voice move no fight).
  [11] THE VOICES fire exactly on their events and nowhere else (v81 §4's
      sound). Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns), each call tagged with where it
      was made. Evidence: a cast of hers playing anything but exactly one `ult`
      voice with w "oathwound", inside fireUlt, or that voice anywhere else; a
      blow of hers whose hit voice (resolveHit's own line -- a ward's shatter
      plays its own crit hit voice inside hurt(), told apart by its caller and
      never priced) is not exactly one call, carrying `price` = the stacks the
      blow was priced on with its dmg and crit when the window is open and
      n > 0, and no `price` otherwise (x1 window blows and every shut-window
      blow keep the plain call); `price` on any other call (the foe's blows, a
      shade's, a shatter); ANY voice inside tickPrice -- the design's "close --
      nothing": a window closing by its clock or on a death plays nothing, and
      never a close voice on a death; a voice of hers in the picture's hook, a
      drawn frame or the verdict. Coverage: casts voiced one for one, priced
      blows voiced at n 2 and 4 one for one, x1 and shut-window blows plain,
      the foe's blows unpriced with her window open and shut, clock closes and
      death closes silent, a quiet verdict.
  [12] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S, AND IS THE
      PICTURE DECLARED. `tickGore` (tickPresentation: the picture's one call on
      the step path, through hit stops and in the verdict) is wrapped: evidence
      is any change across it to either fighter or a shade (every own number,
      flag and string but the picture's `gore*` fields, every array's length,
      every status, the window) or to the match (every own number, flag and
      string, every array's length), an RNG draw or a voice; the foe (not
      Goreshard) carrying any of the picture; the picture up before her first
      cast. And the picture REBUILT from what the simulation did, exactly, in
      the builder's own arithmetic (readings 13-16): the red up (`goreFade` 1)
      exactly while her window is open with the match on and both standing; its
      run clock the presentation clock since the cast, the cast found by
      `priceTally.casts` rising; a drain to 0 over DRAIN of its clock at any
      close (the clock, a death, the kill with the window still set); the glow
      eased (GLOWT) toward G0 + G1 x the foe's Hemorrhage -- v81's "0 -> 4 maps
      alpha 0.2 -> 0.8", pinned from the design; the motes shed at RATE a clock
      unit while the window is open and never while it is shut, each born within
      her reach, aged to DLIFE and capped at CAP; nothing up after 2 s of the
      verdict. THE FLOAT (reading 17): the damage float of every blow in her
      fights sized exactly clamp(22 + dmg x 0.62, 22, 62) x (crit ? 1.3 : 1) x
      (1 + FK x n) for a blow of hers priced on n, and the old size (x1) for
      every other (hers with the window shut or n 0, the foe's, a shade's).
      DRAIN, GLOWT, RATE, DLIFE, CAP and FK are read from the builder's S6
      table (Code's picks); 0.2 and 0.8 are v81's.
  --drawn N (default 0 = off): on the FIRST seed, both sides, every foe,
      each fight is also drawn through the renderer (`AC.__draw`, the post
      chain off, 270x480) every Nth step while the picture shows and every
      120th otherwise, through the kill and the verdict. [12] fails a drawn
      frame that throws, draws the match's RNG, plays a voice or changes the
      simulation or the picture's clocks. It runs on any link, so the stage-5
      link's draws are its control.
"""'''))

# ------------------------------------------------------------------ args and pins
reps.append(('''ap.add_argument("--stage", choices=["2", "5"], required=True,
                help="the stage this link is: pins the blade (2: the shipped 9.17; 5: the builder's TUNED)")''',
'''ap.add_argument("--stage", choices=["2", "5", "6"], required=True,
                help="the stage this link is: pins the blade (2: the shipped 9.17; 5 and 6: the builder's TUNED); "
                     "6 also requires the picture and the voice")'''))
reps.append(('''ap.add_argument("--json", default=None)
a = ap.parse_args()''', '''ap.add_argument("--json", default=None)
ap.add_argument("--drawn", type=int, default=0, help="draw the first seed's fights every Nth step (0 = off)")
a = ap.parse_args()'''))
reps.append(('''PIN = {"dur": GB.ULT["dur"], "charge": GB.ULT["charge"], "perStack": GB.ULT["perStack"],''',
'''# THE PICTURE'S NUMBERS: v81's glow map (alpha 0.2 at 0 stacks -> 0.8 at 4), and Code's picks read
# from the builder's S6 table (the tickGore row and the float's sim-path line), never from the page.
_tick = [new for label, _old, new in GB.S6 if label.startswith(GB.S6_TICK_ROW)]
assert len(_tick) == 1, "the builder has no single tickGore row"
_tick = _tick[0]


def _pin(rx, txt=None):
    m_ = re.search(rx, txt if txt is not None else _tick)
    assert m_, f"the builder's S6 no longer carries {rx}"
    return float(m_.group(1))


PIC = {"G0": 0.2, "G1": 0.15,           # v81: alpha 0.2 at 0 stacks, 0.8 at 4 (0.2 + 4 x 0.15)
       "GLOWT": _pin(r"Math\\.min\\(1, dt / ([\\d.]+)\\)"), "RATE": _pin(r"f\\.goreAcc \\+= dt \\* ([\\d.]+);"),
       "DRAIN": _pin(r"1 - f\\.goreOut / ([\\d.]+)\\)"), "DLIFE": _pin(r"f\\.goreDrops\\[i\\]\\.t >= ([\\d.]+)\\)"),
       "CAP": _pin(r"f\\.goreDrops\\.length > (\\d+)\\)"),
       "FK": _pin(r"\\(1 \\+ ([\\d.]+) \\* priceN\\)",
                  [v[0] for k, v in GB.S6_SIM_LINES.items() if "float" in k][0])}
assert abs(PIC["G0"] + 4 * PIC["G1"] - 0.8) < 1e-12
assert f"({PIC['G0']} + {PIC['G1']} * n - f.goreGlow)" in _tick, "the builder's glow is not v81's 0.2 -> 0.8"
PIN = {"dur": GB.ULT["dur"], "charge": GB.ULT["charge"], "perStack": GB.ULT["perStack"], "pic": PIC,'''))

# ------------------------------------------------------------------ JS: the signature and stage-6 detection
reps.append(('''JS = r"""([seeds, PIN]) => {''', '''JS = r"""([seeds, PIN, drawEvery]) => {'''))
reps.append(('''  const isMe = f => isG(f) && !f.shade;
''', '''  const isMe = f => isG(f) && !f.shade;
  /* ---- STAGE 6, DETECTED BY ITS OWN PRESENCE: Goreshard's cast arm and the priced-blow branch in the
     synth [11], `tickGore` on the match [12]. A link without them runs [1]-[10] only. ---- */
  const playSrc = AC.SFX.play.toString();
  const hasArm = /w === "oathwound"/.test(playSrc), hasBr = /kind === "hit" && p\\.price/.test(playSrc);
  const S6V = hasArm && hasBr, S6P = typeof P.tickGore === "function", S6PART = hasArm !== hasBr;
  const PIC = PIN.pic, oGore = P.tickGore, oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  let FIGHT = null, vctx = "a step", vrec = null, tail = false;
  const isCastV = (kind, q) => kind === "ult" && !!q && q.w === "oathwound";
  const isPriced = (kind, q) => !!q && typeof q === "object" && Object.prototype.hasOwnProperty.call(q, "price");
  if (S6PART) fail(11, `only one of the two voice arms is on this link (cast arm ${hasArm}, priced branch ${hasBr})`);
  if (S6V !== S6P && (S6V || S6P)) fail(12, `half of stage 6 on this link (voices ${S6V}, picture ${S6P})`);
  if (S6V) AC.SFX.play = function(kind, q){
    if (FIGHT){
      if (vrec) vrec.push([kind, q && typeof q === "object" ? Object.assign({}, q) : q, vctx]);
      if (isCastV(kind, q) && vctx !== "her cast") fail(11, `her cast voice played in ${vctx}`);
      if (isPriced(kind, q) && vctx !== "her blow") fail(11, `a priced voice (price ${q.price}) played in ${vctx}`);
    }
    return oPlay.call(this, kind, q);
  };
  const GORE = new Set(["goreFade", "goreAge", "goreOut", "goreGlow", "goreSeen", "goreAcc", "goreDropN", "goreDrops",
                        "goreTh", "goreT", "goreW"]);
  const floatOld = (d, crit) => clampD(22 + d * 0.62, 22, 62) * (crit ? 1.3 : 1);
  /* a blow's damage float: the call at the blow's point whose text is its number (and "!" on a crit) */
  const dmgFloat = (fl, hx, hy) => { let r = null; for (const q of fl) if (q.x === hx && q.y === hy && /^\\d+!?$/.test(String(q.text))) r = q; return r; };
'''))

# ------------------------------------------------------------------ JS: the verdict bypasses [1]-[10]
reps.append(('''  P.step = function(dt){
    for (const f of [this.a, this.b]) if (f.ultPrice && !isMe(f)) fail(1,''',
'''  P.step = function(dt){
    if (tail) return oStep.call(this, dt);          /* the verdict: [11]-[12] only */
    for (const f of [this.a, this.b]) if (f.ultPrice && !isMe(f)) fail(1,'''))

# ------------------------------------------------------------------ JS: fireUlt
reps.append(('''    if (!isMe(f)) return oFire.call(this, f, foe);
    castStep++; if (per) per.casts++;''',
'''    if (!isMe(f)){ const vc = vctx; vctx = "another's cast"; try { return oFire.call(this, f, foe); } finally { vctx = vc; } }
    castStep++; if (per) per.casts++;'''))
reps.append(('''    try { r = oFire.call(this, f, foe); } finally { this.rng = oRng; }
''', '''    const vc0 = vctx, vr0 = vrec; vctx = "her cast"; vrec = [];
    let heardCast = null;
    try { r = oFire.call(this, f, foe); } finally { this.rng = oRng; heardCast = vrec; vctx = vc0; vrec = vr0; }
    /* [11] THE CAST'S VOICE: exactly one, inside fireUlt (the common `SFX.play("ult", { w: f.w.id })`) */
    if (S6V){
      const cv = heardCast.filter(c => isCastV(c[0], c[1]));
      if (cv.length !== 1) fail(11, `a cast of hers played ${cv.length} cast voices (${JSON.stringify(heardCast.map(c => c[0] + (c[1] && c[1].w ? "/" + c[1].w : "")))})`);
      else inc("v11CastOk");
    }
'''))

# ------------------------------------------------------------------ JS: tickPrice
reps.append(('''    try { r = oTick.call(this, dt); } finally { this.rng = oRng; }
''', '''    const vc0 = vctx, vr0 = vrec; vctx = "the price's ticker"; vrec = [];
    let heardT = null;
    try { r = oTick.call(this, dt); } finally { this.rng = oRng; heardT = vrec; vctx = vc0; vrec = vr0; }
    /* [11] "close -- nothing": the window's ticker plays no voice, by its clock or ON A DEATH */
    if (S6V && heardT.length) fail(11, `the window's ticker played ${JSON.stringify(heardT.map(c => c[0] + (c[1] && c[1].w ? "/" + c[1].w : "")))}${pre.some(q => !q.fa || !q.oa) ? " -- ON A DEATH" : ""}`);
'''))
reps.append(('''        inc("closes"); if (per) per.closes++;
''', '''        inc("closes"); if (per) per.closes++;
        if (S6V && !heardT.length) inc(death ? "v11CloseDeathQuiet" : "v11CloseClockQuiet");
'''))

# ------------------------------------------------------------------ JS: another attacker's blow
reps.append(('''    const outer = herWatch; herWatch = [];
    let r, seen;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally {
      seen = herWatch; herWatch = outer;
''', '''    const outer = herWatch; herWatch = [];
    const vc0 = vctx, vr0 = vrec; vctx = "another's blow"; vrec = [];
    const fl = [], hadF = Object.prototype.hasOwnProperty.call(this, "float"), oF = this.float;
    this.float = function(x, y, text, color, size){ fl.push({ x, y, text, size }); return oF.call(this, x, y, text, color, size); };
    let r, seen, heardO;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally {
      seen = herWatch; herWatch = outer;
      heardO = vrec; vctx = vc0; vrec = vr0;
      if (hadF) this.float = oF; else delete this.float;
'''))
reps.append(('''    else if (pastDmg) inc((self.shade ? "othShade" : "oth") + (open ? "In" : "Out"));
    return r;
  };
''', '''    else if (pastDmg) inc((self.shade ? "othShade" : "oth") + (open ? "In" : "Out"));
    /* [11] another's blow is never priced (the wrapper fails a priced call by where it was made) */
    if (S6V && pastDmg && !heardO.some(c => isPriced(c[0], c[1]))) inc(open ? "v11OthIn" : "v11OthOut");
    /* [12] and its damage float is the old size */
    if (S6P && pastDmg){
      const q = dmgFloat(fl, hx, hy);
      if (q){
        const t = String(q.text), d = parseInt(t, 10), cr = t.endsWith("!");
        if (q.size !== floatOld(d, cr)) fail(12, `${where}: its damage float ${q.size}, want the old size ${floatOld(d, cr)}`);
        else inc("f12Oth");
      }
    }
    return r;
  };
'''))

# ------------------------------------------------------------------ JS: her blow
reps.append(('''    let hurtD = null; const oHurt = this.hurt;
    this.hurt = function(t, d, s){ if (t === foe && hurtD === null) hurtD = d; return oHurt.call(this, t, d, s); };
''', '''    let hurtD = null; const oHurt = this.hurt;
    this.hurt = function(t, d, s){
      if (t === foe && hurtD === null) hurtD = d;
      const vh = vctx; vctx = "hurt() in her blow";
      try { return oHurt.call(this, t, d, s); } finally { vctx = vh; }
    };
    const flH = [], oFl = this.float;
    this.float = function(x, y, text, color, size){ flH.push({ x, y, text, size }); return oFl.call(this, x, y, text, color, size); };
'''))
reps.append(('''    const watch0 = herWatch; herWatch = null;       /* [10] her own blow is not another's */
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { herWatch = watch0; this.rng = oRng; delete this.hurt; delete foe.stacks; delete self.dmgMul; }
''', '''    const watch0 = herWatch; herWatch = null;       /* [10] her own blow is not another's */
    const vcB = vctx, vrB = vrec; vctx = "her blow"; vrec = [];
    let heardB = null;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { herWatch = watch0; this.rng = oRng; delete this.hurt; delete this.float; delete foe.stacks; delete self.dmgMul;
              heardB = vrec; vctx = vcB; vrec = vrB; }
'''))
reps.append(('''      else inc(open ? "ceilBindIn" : "ceilBindOut");
    }
    return r;
  };
''', '''      else inc(open ? "ceilBindIn" : "ceilBindOut");
    }
    /* [11] HER BLOW'S VOICE: resolveHit's own hit line, priced exactly when the window is open and n > 0 */
    if (S6V){
      const own = heardB.filter(c => c[2] === "her blow" && c[0] === "hit");
      const nPaid = open ? pre.bl : 0;
      if (own.length !== 1) fail(11, `a blow of hers played ${own.length} hit voices from its own line (${JSON.stringify(own.map(c => c[1]))})`);
      else {
        const q = own[0][1] || {};
        if (nPaid > 0){
          if (!isPriced("hit", q) || q.price !== nPaid || q.dmg !== D || q.crit !== crit)
            fail(11, `a blow of hers priced on n ${nPaid} voiced ${JSON.stringify(q)}, want price ${nPaid}, dmg ${D}, crit ${crit}`);
          else inc("v11Priced" + nPaid);
        } else if (isPriced("hit", q)) fail(11, `a ${open ? "x1 window" : "shut-window"} blow of hers voiced price ${q.price}`);
        else if (q.dmg !== D || q.crit !== crit) fail(11, `a blow of hers voiced dmg ${q.dmg} crit ${q.crit}, dealt ${D} crit ${crit}`);
        else inc(open ? "v11PlainX1" : "v11PlainShut");
      }
      if (heardB.some(c => c[2] === "hurt() in her blow" && c[0] === "hit")) inc("v11Shatter");
    }
    /* [12] HER BLOW'S FLOAT: x(1 + FK x n) on a priced blow, the old size otherwise */
    if (S6P){
      const nPaid = open ? pre.bl : 0, q = dmgFloat(flH, hx, hy);
      const want = floatOld(D, crit) * (1 + PIC.FK * nPaid);
      if (!q) fail(12, `a blow of hers (dealt ${D}) drew no damage float at its point`);
      else if (String(q.text) !== String(D) + (crit ? "!" : "")) fail(12, `her blow's float reads ${q.text}, dealt ${D}${crit ? " (crit)" : ""}`);
      else if (q.size !== want) fail(12, `her blow ${open ? "IN" : "out of"} the window (n ${nPaid}): its float ${q.size}, want ${want}`);
      else inc(nPaid > 0 ? "f12Priced" : open ? "f12X1" : "f12Shut");
    }
    return r;
  };

  /* [12] THE PICTURE'S HOOK: `tickGore`, on the presentation clock, REBUILT from what the simulation did */
  if (S6P) P.tickGore = function(dt){
    if (!FIGHT || FIGHT.m !== this) return oGore.call(this, dt);
    inc("g12Calls");
    const me = FIGHT.me, foe = FIGHT.foe;
    const s0 = simSnap(this, GORE);
    const pre = { fade: me.goreFade, age: me.goreAge, out: me.goreOut, glow: me.goreGlow, seen: me.goreSeen,
                  acc: me.goreAcc, dropN: me.goreDropN, drops: me.goreDrops.map(q => [q.t, q.n]) };
    const open = !!me.ultPrice && !this.over && me.alive && foe.alive;
    const nS = Math.min(4, foe.stacks("hemorrhage"));
    let draws = 0; const oRng = this.rng;
    this.rng = function(){ draws++; return oRng.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "the picture's hook"; vrec = [];
    let r, heard = null;
    try { r = oGore.call(this, dt); } finally { this.rng = oRng; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = diffAt(s0, simSnap(this, GORE));
    if (d) fail(12, `the picture wrote the simulation: ${d}${this.over ? " (after over)" : ""}`);
    else if (draws) fail(12, `the picture drew the RNG ${draws} times`);
    else if (heard.length) fail(12, `the picture played ${JSON.stringify(heard.map(c => c[0]))}`);
    else inc("g12Clean");
    if (foe.goreFade !== 0 || foe.goreAge !== 0 || foe.goreOut !== 0 || foe.goreGlow !== 1 || foe.goreSeen !== 0
        || foe.goreAcc !== 0 || foe.goreDropN !== 0 || foe.goreDrops.length)
      fail(12, `${foe.w.id}, which is not Goreshard, carries the picture`);
    const T = me.priceTally;
    if (!T){
      if (me.goreFade !== 0 || me.goreDrops.length || me.goreDropN !== 0 || me.goreSeen !== 0) fail(12, "the picture up before her first cast");
      else inc("g12Idle");
      return r;
    }
    /* THE REBUILD, in the builder's own arithmetic and order */
    let seen = pre.seen, age = pre.age, out = pre.out, glow = pre.glow, fade = pre.fade, acc = pre.acc, sheds = 0, cast = false;
    if (T.casts !== seen){ seen = T.casts; if (open){ age = 0; out = 0; glow = 1; cast = true; } }
    if (open){
      fade = 1; out = 0; age += dt;
      glow += (PIC.G0 + PIC.G1 * nS - glow) * Math.min(1, dt / PIC.GLOWT);
      acc += dt * PIC.RATE;
      while (acc >= 1){ acc -= 1; sheds++; }
    } else if (fade > 0){ out += dt; fade = Math.max(0, 1 - out / PIC.DRAIN); }
    const want = { goreFade: fade, goreAge: age, goreOut: out, goreGlow: glow, goreSeen: seen, goreAcc: acc, goreDropN: pre.dropN + sheds };
    const off = Object.keys(want).filter(k => me[k] !== want[k]);
    if (off.length) fail(12, `the picture ${open ? "IN an open window" : pre.fade > 0 ? "draining" : "down"}: ${off.map(k => `${k} ${me[k]} (want ${want[k]})`).join(", ")}`);
    else {
      if (cast) inc("g12Cast");
      if (open){ inc("g12Open"); inc("g12GlowN" + nS); }
      else if (pre.fade > 0){
        if (pre.fade === 1) inc(this.over ? (me.ultPrice ? "g12CloseKillOpen" : "g12CloseOver") : "g12CloseClock");
        inc(fade === 0 ? "g12Gone" : "g12Drain");
      } else inc("g12Down");
    }
    /* the motes: the old ones aged, the new ones born at t 0 and aged with them, none past DLIFE, capped */
    let M = pre.drops.map(q => q.slice());
    for (let i = 0; i < sheds; i++){ M.push([0, pre.dropN + i]); if (M.length > PIC.CAP) M.shift(); }
    for (const q of M) q[0] += dt;
    M = M.filter(q => !(q[0] >= PIC.DLIFE));
    const got = me.goreDrops.map(q => [q.t, q.n]);
    if (got.length !== M.length || got.some((q, i) => q[0] !== M[i][0] || q[1] !== M[i][1]))
      fail(12, `the motes: ${got.length} in flight, the shedding clock says ${M.length}${open ? "" : " (the window shut)"}`);
    else if (sheds){
      inc("g12Shed", sheds);
      const Lr = C.physics.ballR + me.w.reach * this.actMods.reach * me.reachMul + 6 + me.w.artW;
      for (const q of me.goreDrops) if (q.n >= pre.dropN){
        if (!(Math.hypot(q.x - me.x, q.y - me.y) <= Lr)) fail(12, `a mote born ${Math.hypot(q.x - me.x, q.y - me.y).toFixed(1)} from her centre, past her reach ${Lr.toFixed(1)}`);
        else inc("g12MoteOnBlade");
      }
    } else if (!open && got.length) inc("g12MotesFalling");
    return r;
  };

  /* THE DRAWN SUBSET [12]: a frame through the renderer, the simulation and the picture's clocks read before and after */
  const drawOn = drawEvery > 0;
  if (drawOn){ window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false; }
  const goreClocks = m => [m.a, m.b].map(q => [q.goreFade, q.goreAge, q.goreOut, q.goreGlow, q.goreSeen, q.goreAcc, q.goreDropN,
                                               q.goreDrops ? q.goreDrops.map(o => o.t).join(":") : "-"].join()).join("|");
  const drawFrame = (m, steps) => {
    const vis = [m.a, m.b].some(q => q.goreFade > 0 || (q.goreDrops && q.goreDrops.length));
    if (!(vis ? steps % drawEvery === 0 : steps % 120 === 0)) return;
    const s0 = simSnap(m, null), g0 = goreClocks(m), oR = m.rng; let dr = 0;
    m.rng = function(){ dr++; return oR.apply(this, arguments); };
    const vc0 = vctx, vr0 = vrec; vctx = "a drawn frame"; vrec = [];
    let threw = null, heard = null;
    try { AC.__draw(m); } catch (e){ threw = String((e && e.message) || e); }
    finally { m.rng = oR; heard = vrec; vctx = vc0; vrec = vr0; }
    const d = diffAt(s0, simSnap(m, null));
    if (threw) fail(12, "a drawn frame threw: " + threw);
    else if (dr) fail(12, `a drawn frame drew the match's RNG ${dr}x`);
    else if (d) fail(12, "a drawn frame changed the simulation: " + d);
    else if (goreClocks(m) !== g0) fail(12, "a drawn frame changed the picture's clocks");
    else if (heard.length) fail(12, `a drawn frame played ${JSON.stringify(heard.map(c => c[0]))}`);
    else { inc("drawOk"); if (vis) inc("drawPic"); if (vis && m.hitStop > 0) inc("drawPicStop"); if (m.over) inc("drawVerdict"); }
  };
'''))

# ------------------------------------------------------------------ JS: the fight loop
reps.append(('''    herWatch = null;
    per = { in: 0, out: 0, casts: 0, closes: 0 };
    chargeLive = 0; hitLog = null;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
''', '''    herWatch = null;
    per = { in: 0, out: 0, casts: 0, closes: 0 };
    chargeLive = 0; hitLog = null;
    let steps = 0;
    if (S6P) for (const f of [m.a, m.b]){
      if (f.goreFade !== 0 || f.goreAge !== 0 || f.goreOut !== 0 || f.goreGlow !== 1 || f.goreSeen !== 0 || f.goreAcc !== 0
          || f.goreDropN !== 0 || !Array.isArray(f.goreDrops) || f.goreDrops.length) fail(12, `a fresh Match's ${f.w.id} carries a picture`);
      else inc("g12Fresh");
    }
    FIGHT = (S6V || S6P || drawOn) ? { m, me, foe: side ? m.a : m.b } : null;
    const drawn = drawOn && sd === seeds[0];
    if (drawn) inc("drawnFights");
    try {
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
'''))
reps.append(('''    if (rowSnap() !== ROW0) fail(8, "the shared weapon row moved during a fight");
  }
''', '''    if (rowSnap() !== ROW0) fail(8, "the shared weapon row moved during a fight");
    /* [11]-[12] THE VERDICT: 2 s of the step's `over` path (the presentation clock only), read by them alone */
    if ((S6V || S6P || drawn) && m.over){
      const openAt = !!me.ultPrice, up = me.goreFade > 0, x11 = n.x11 || 0;
      tail = true; vctx = "the verdict"; vrec = [];
      let heardV = null;
      try { for (let i = 0; i < 2 / DT; i++){ m.step(DT); if (drawn) drawFrame(m, steps + i + 1); } }
      finally { tail = false; vctx = "a step"; heardV = vrec; vrec = null; }
      if (S6V){
        if (heardV.some(c => isCastV(c[0], c[1]) || isPriced(c[0], c[1]))) fail(11, "a voice of hers in the verdict");
        else if ((n.x11 || 0) === x11) inc(openAt ? "v11VerdictQuietOpen" : "v11VerdictQuiet");
      }
      if (S6P && me.priceTally){
        if (me.goreFade !== 0 || me.goreDrops.length)
          fail(12, `after 2 s of the verdict the red at ${me.goreFade}, ${me.goreDrops.length} motes${openAt ? " -- the window the sim left set" : ""}`);
        else inc(up ? (openAt ? "g12EndGoneOpen" : "g12EndGoneUp") : "g12EndGoneOk");
      }
    }
    } finally { FIGHT = null; }
  }
'''))
reps.append(('''  P.tickCharge = oCharge; P.tickWeapon = oWeap; P.bladeSegments = oSegs; P.tickHits = oHits; P.resolveClank = oClank; P.checkEnd = oEnd;
''', '''  P.tickCharge = oCharge; P.tickWeapon = oWeap; P.bladeSegments = oSegs; P.tickHits = oHits; P.resolveClank = oClank; P.checkEnd = oEnd;
  if (S6P) P.tickGore = oGore;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
'''))
reps.append(('''           u: { charge: U.charge, dur: U.dur, kind: U.kind, perStack: U.perStack }, blade: ROW.dmg, pin: PIN };''',
'''           u: { charge: U.charge, dur: U.dur, kind: U.kind, perStack: U.perStack }, blade: ROW.dmg, pin: PIN,
           s6: { v: S6V, p: S6P, part: S6PART } };'''))

# ------------------------------------------------------------------ Python: the call and the checks
reps.append(('''    R = page.evaluate(JS, [seeds, PIN])''', '''    R = page.evaluate(JS, [seeds, PIN, a.drawn])'''))
reps.append(('''ok = 0
for k, text, cover in checks:''', '''S6 = R["s6"]
if S6["v"] or S6["p"] or a.stage == "6":
    pc = PIN["pic"]
    priced = {k: g(f"v11Priced{k}") for k in range(1, 5)}
    nlog = {int(k): v[0] for k, v in R["log"].items()}
    print(f"  STAGE 6 on this link: voices {S6['v']}, picture {S6['p']}   picture pins: glow {pc['G0']:g} + {pc['G1']:g} x n "
          f"(v81: 0.2 -> 0.8), ease {pc['GLOWT']:g}, drain {pc['DRAIN']:g}, motes {pc['RATE']:g} a clock unit living "
          f"{pc['DLIFE']:g} (cap {pc['CAP']:g}), float x(1 + {pc['FK']:g} n)   (clock units: half-seconds)")
    print(f"  [11] casts voiced {g('v11CastOk')} of {T['casts']}; priced blows voiced by n {priced} (the log's n > 0: "
          f"{ {k: v for k, v in nlog.items() if k > 0} }); plain: {g('v11PlainX1')} x1 window blows, {g('v11PlainShut')} "
          f"shut-window; {g('v11Shatter')} ward shatters' own voices unpriced; the foe's blows unpriced {g('v11OthIn')} open / "
          f"{g('v11OthOut')} shut; closes silent: {g('v11CloseClockQuiet')} by the clock, {g('v11CloseDeathQuiet')} ON A DEATH; "
          f"verdicts quiet {g('v11VerdictQuiet')} (+{g('v11VerdictQuietOpen')} with the window left set)")
    print(f"  [12] tickGore clean on {g('g12Clean')} of {g('g12Calls')} calls ({g('g12Idle')} before a first cast); rebuilt: "
          f"{g('g12Cast')} casts found, {g('g12Open')} open calls (glow at n 0/2/4: {g('g12GlowN0')}/{g('g12GlowN2')}/"
          f"{g('g12GlowN4')}), closes {g('g12CloseClock')} by the clock / {g('g12CloseKillOpen')} at a kill with the "
          f"window set / {g('g12CloseOver')} at over after a death close, {g('g12Drain')} draining calls, {g('g12Gone')} "
          f"gone; motes {g('g12Shed')} shed ({g('g12MoteOnBlade')} born on her blade), {g('g12MotesFalling')} calls with "
          f"motes falling after a close; after the verdict {g('g12EndGoneOk') + g('g12EndGoneUp') + g('g12EndGoneOpen')} "
          f"clean ({g('g12EndGoneOpen')} with the window left set); fresh fighters {g('g12Fresh')}")
    print(f"       floats: {g('f12Priced')} priced x(1 + {pc['FK']:g} n), {g('f12X1')} x1 window and {g('f12Shut')} "
          f"shut-window blows of hers the old size, {g('f12Oth')} of other attackers' the old size")
    if a.drawn:
        print(f"  drawn subset: {g('drawnFights')} fights drawn every {a.drawn}th step while the picture shows (every 120th "
              f"otherwise): {g('drawOk')} frames clean ({g('drawPic')} with the picture up, {g('drawPicStop')} in a hit stop, "
              f"{g('drawVerdict')} in the verdict)")
    both = S6["v"] and S6["p"] and not S6["part"]
    checks.append((11, "the voices fire exactly on their events: one cast voice a cast, in fireUlt; a blow priced on "
                       "n > 0 voiced with price n (its dmg and crit), every other blow plain; the close silent, by the "
                       "clock and ON A DEATH; none in the picture, a drawn frame or the verdict",
                   both and g("v11CastOk") == T["casts"] and priced[2] > 0 and priced[4] > 0
                   and sum(priced.values()) == sum(v for k, v in nlog.items() if k > 0)
                   and g("v11PlainX1") > 0 and g("v11PlainShut") > 0 and g("v11OthIn") > 0 and g("v11OthOut") > 0
                   and g("v11CloseClockQuiet") > 0 and g("v11CloseDeathQuiet") > 0
                   and g("v11VerdictQuiet") + g("v11VerdictQuietOpen") > 0))
    checks.append((12, "the picture's hook writes nothing of the simulation's and is the picture declared: the red "
                       "exactly while the window is open, its run and drain, the glow toward 0.2 + 0.15 n, the motes "
                       "while open only; the float x(1 + 0.1 n) on a priced blow and the old size on every other"
                       + ("; the drawn subset clean" if a.drawn else ""),
                   both and g("g12Clean") == g("g12Calls") and g("g12Cast") > 0 and g("g12Open") > 0
                   and all(g(f"g12GlowN{k}") > 0 for k in (0, 2, 4)) and g("g12CloseClock") > 0
                   and g("g12CloseKillOpen") > 0 and g("g12Drain") > 0 and g("g12Gone") > 0 and g("g12Shed") > 0
                   and g("g12MoteOnBlade") > 0 and g("g12EndGoneOk") + g("g12EndGoneUp") + g("g12EndGoneOpen") > 0
                   and g("f12Priced") > 0 and g("f12X1") > 0 and g("f12Shut") > 0 and g("f12Oth") > 0
                   and g("g12Fresh") == 2 * R["fights"] and (g("drawOk") > 0 if a.drawn else True)))
elif a.drawn:
    print(f"  stage 6: not on this link -- [11] not run; the drawn subset alone: {g('drawnFights')} fights, {g('drawOk')} "
          f"frames clean")
    checks.append((12, "the drawn subset only (no picture on this link): no drawn frame throws, draws the RNG or changes "
                       "the simulation", g("drawOk") > 0))
else:
    print("  stage 6: not on this link (no cast arm or priced branch in the synth, no tickGore) -- [11]-[12] not run")
ok = 0
for k, text, cover in checks:'''))

for a_, b_ in reps:
    assert s.count(a_) == 1, (s.count(a_), a_[:100])
    s = s.replace(a_, b_, 1)
p.write_bytes(s.encode("utf-8"))
print("probe extended; sha16", hashlib.sha256(s.encode()).hexdigest()[:16])
