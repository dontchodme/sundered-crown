"""Add stage 6's two checks ([10] the voice, [11] the picture) to tools/ironhail_probe.py.

Bindweed's / Coldiron's pattern: each check switches itself on from the page (the voice's arms in
AC.SFX.play.toString(), the picture's hook on the Match), so the same probe still gates stages 2, 3
and 5 with 9 checks. Refuses to run twice.
"""
import pathlib, hashlib

p = pathlib.Path("C:/dev/sundered-crown/tools/ironhail_probe.py")
s = p.read_text(encoding="utf-8")
assert "\r\n" not in s
if "stage6v" in s:
    raise SystemExit("the probe already has stage 6")
assert hashlib.sha256(s.encode()).hexdigest()[:16] == "400e8424f60238c0"

reps = [
# ---- the docstring
('''  [9] the nova is gone: a cast that spawns a shot, that does not open
      {t: 0, dur, cd: 0}, or that lands on an open window
"""''',
'''  [9] the nova is gone: a cast that spawns a shot, that does not open
      {t: 0, dur, cd: 0}, or that lands on an open window
  STAGE 6 (the picture and the voice, sc-ironhail-sunder-fx). Each check runs
  only on a link that carries its half, read off the page itself:
  [10] THE VOICE (on when "ironhail-land" is in AC.SFX.play.toString()): an
      Ironhail cast without exactly one `ult`/ironhail voice inside fireUlt; a
      tickHail call whose Ironhail voices are not exactly its resolved bolts'
      in order -- one landing thud per landed bolt whose `n` is the count the
      foe carries after THAT landing's sunder (read in the apply and again
      when the voice plays), one miss thud per missed bolt -- so a window
      that closes (on its clock or on a death) sounds nothing (v83 4: the
      close has no voice); any other voice inside tickHail but a ward's own
      shatter (shatter() plays its crit hit voice inside hurt(), once a
      break); and every Ironhail voice of the run accounted for by those
      events (none plays anywhere else, after `over` included)
  [11] THE PICTURE (on when the Match has `tickQuarrel`): `tickQuarrel`, the
      picture's one hook on the step, changing any sim field of either
      fighter or the match (the bolts in the air included) or drawing the
      RNG; the limbs up (quarrelFade exactly 1) other than exactly while the
      window is open, the match not over and the caster alive; a bolt that
      resolves without exactly one new puff at its own spot, hit or miss as
      tickHail resolved it, or a puff with no bolt resolved; a live landing
      without a sunder tag on the board reading the foe's count; a killing
      landing that adds or recounts a sunder tag (the shatter owns that
      frame); limbs up at `over` not cooled to 0 by 0.51s into the verdict;
      a resolved bolt the picture never showed; and on the DRAWN subset (the
      first seed, both sides, every foe, through the kill and the verdict) a
      drawn frame that throws, draws the match's RNG or changes any sim field
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
# ---- the stage-6 setup and the tickQuarrel hook
('''  const born = new WeakMap(), winMT = new WeakMap(), fallFr = {};
''',
'''  const born = new WeakMap(), winMT = new WeakMap(), fallFr = {};

  /* STAGE 6, read off the page: the voice's arms are in SFX.play, the
     picture's hook is on the Match. */
  const stage6v = /ironhail-land/.test(AC.SFX.play.toString());
  const stage6p = typeof P.tickQuarrel === "function";
  const voices = [], ihAll = {}, oPlay = AC.SFX.play, oQuarrel = P.tickQuarrel;
  let curM = null, postOver = false;
  const ihVoice = q => !!(q && typeof q.w === "string" && /^ironhail/.test(q.w));
  const vname = x => x[0] + (x[1] && x[1].w ? "/" + x[1].w : "") + (x[1] && x[1].crit ? "(crit)" : "");
  /* every voice, with the count the Ironhail's foe carries at the moment a landing thud plays */
  if (stage6v) AC.SFX.play = function(kind, q){
    let atN = null;
    if (curM && kind === "ult" && q && q.w === "ironhail-land"){
      const me = curM.a.w.id === "ironhail" ? curM.a : curM.b, foe = me === curM.a ? curM.b : curM.a;
      atN = foe.stacks("sunder");
    }
    voices.push([kind, q ? Object.assign({}, q) : q, atN]);
    if (kind === "ult" && ihVoice(q)) ihAll[q.w] = (ihAll[q.w] || 0) + 1;
    return oPlay.call(this, kind, q);
  };
  /* THE SIM, as a picture hook could touch it: both fighters' bodies, statuses,
     window and tally, and the match's clock, stop, verdict, holds, beats, shots
     and the bolts in the air. */
  const FF = ["x", "y", "vx", "vy", "hp", "shield", "shieldMax", "theta", "charge", "stun", "alive", "hits",
              "dealt", "crits", "spinDir", "fireCd", "burden"];
  const simSnap = (m) => {
    const o = [m.t, m.hitStop, m.over, m.winner ? (m.winner === m.a ? "a" : "b") : null,
               !!m.latch, !!m.splitHold, m.beats ? m.beats.length : null,
               m.shots.map(q => [q.x, q.y, q.vx, q.vy]), m.hail.map(d => [d.x, d.y, d.t, d.side])];
    for (const f of [m.a, m.b]){
      for (const k of FF) o.push(f[k]);
      o.push(Object.keys(f.status).sort().map(k => [k, f.status[k].stacks, f.status[k].t]));
      o.push(f.ultHail ? [f.ultHail.t, f.ultHail.dur, f.ultHail.cd] : null, f.hailTally ? JSON.stringify(f.hailTally) : null);
    }
    return JSON.stringify(o);
  };
  const firstDiff = (s0, s1) => { let i = 0; while (i < s0.length && s0[i] === s1[i]) i++;
    return JSON.stringify(s0.slice(Math.max(0, i - 30), i + 30)) + " -> " + JSON.stringify(s1.slice(Math.max(0, i - 30), i + 30)); };
  /* the bolts tickHail resolved that the picture has not shown yet, a side: {x, y, hit} */
  const pendRes = { a: [], b: [] };
  if (stage6p) P.tickQuarrel = function(dt){
    const s0 = simSnap(this), oR = this.rng, oMR = Math.random;
    const pre = [this.a, this.b].map(f => ({ f, seen: f.quarrelSeen.slice(),
                                             tags: this.tags.filter(g => g.key === "sunder").map(g => [g, g.val]) }));
    let drew = 0, r;
    this.rng = function(){ drew++; return oR.apply(this, arguments); };
    Math.random = function(){ drew++; return oMR(); };
    try { r = oQuarrel.call(this, dt); }
    finally { this.rng = oR; Math.random = oMR; }
    if (drew) fail(11, `tickQuarrel drew the RNG ${drew}x`);
    const s1 = simSnap(this);
    if (s1 !== s0) fail(11, "tickQuarrel changed the sim: " + firstDiff(s0, s1)); else inc("quarrelOk");
    for (const p of pre){
      const f = p.f, side = f === this.a ? "a" : "b", foe = f === this.a ? this.b : this.a, T = f.hailTally;
      /* THE LIMBS ARE UP EXACTLY WHILE THE WINDOW IS (and the match runs, and the caster stands) */
      const live = !!(f.ultHail && !this.over && f.alive);
      if ((f.quarrelFade === 1) !== live) fail(11, `quarrelFade ${f.quarrelFade} with the window ${live ? "live" : "not live"} (over ${this.over}, alive ${f.alive})`);
      else if (live) inc("limbsUp"); else if (f.quarrelFade > 0) inc("limbsCool");
      if (!T){ if (f.quarrelFx.length) fail(11, "a puff with no hail"); continue; }
      /* EACH RESOLVED BOLT: one new puff at its own spot, hit or miss as tickHail resolved it */
      const rise = T.landed + T.missed - p.seen[0] - p.seen[1], Q = pendRes[side];
      const fresh = f.quarrelFx.filter(q => q.t === 0);
      if (rise > 0){
        if (fresh.length !== rise || Q.length !== rise) fail(11, `${rise} bolt(s) resolved by the tally, ${Q.length} seen resolving, ${fresh.length} new puff(s)`);
        else {
          let good = 0;
          for (let i = 0; i < rise; i++){
            const q = fresh[i], b = Q[i];
            if (q.x !== b.x || q.y !== b.y || q.hit !== b.hit) fail(11, `a puff at (${q.x}, ${q.y}) hit ${q.hit}; the bolt at (${b.x}, ${b.y}) ${b.hit ? "landed" : "missed"}`);
            else { good++; inc(b.hit ? "puffHit" : "puffMiss"); }
          }
          if (good === rise) inc("puffOk", rise);
        }
        const hits = Q.filter(b => b.hit).length;
        Q.length = 0;
        if (hits){
          if (foe.alive && foe.hp > 0){
            const k = foe.stacks("sunder");
            if (!this.tags.some(g => g.key === "sunder" && g.val === k)) fail(11, `no sunder tag reads the foe's ${k}`);
            else inc("landTagOk");
          } else {
            /* A KILLING LANDING TAGS NOTHING: no sunder tag added, none recounted */
            const now = this.tags.filter(g => g.key === "sunder");
            const added = now.filter(g => !p.tags.some(t => t[0] === g)).length;
            const recount = p.tags.filter(t => t[0].val !== t[1]).length;
            if (added || recount) fail(11, `a killing landing tagged: ${added} added, ${recount} recounted`);
            else inc("killNoTag");
          }
        }
      } else if (fresh.length) fail(11, `${fresh.length} puff(s) with no bolt resolved`);
    }
    return r;
  };
'''),
# ---- the step hook passes straight through in the verdict run
('''  P.step = function(dt){
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;''',
'''  P.step = function(dt){
    if (postOver) return oStep.call(this, dt);
    live = !(this.hitStop > 0 || this.latch || this.splitHold) && !this.over;'''),
# ---- fireUlt: the cast voice
('''    const open = !!f.ultHail, ns = this.shots.length, nh = this.hail.length;
    const r = oFire.call(this, f, foe);''',
'''    const open = !!f.ultHail, ns = this.shots.length, nh = this.hail.length, v0 = voices.length;
    const r = oFire.call(this, f, foe);
    /* [10] THE CAST: exactly one Ironhail voice inside fireUlt, the cast's own */
    if (stage6v){
      const cv = voices.slice(v0).filter(x => x[0] === "ult" && ihVoice(x[1]));
      if (cv.length !== 1 || cv[0][1].w !== "ironhail") fail(10, `a cast voiced ${JSON.stringify(cv.map(vname))}`);
      else inc("castVoice");
    }'''),
# ---- tickHail: the apply records the count it leaves
('''    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ applies.push([f, k, nn, src]); return o.call(this, k, nn, src); }; }
    let r;''',
'''    for (const f of fs){ const o = f.apply; f.apply = function(k, nn, src){ const e = [f, k, nn, src]; applies.push(e); const rr = o.call(this, k, nn, src); e.push(f.stacks(k)); return rr; }; }
    const v0 = voices.length;
    let r;'''),
('''    let resolvedHere = 0;
    const land = [];''',
'''    let resolvedHere = 0;
    const land = [], expV = [];'''),
('''        inc("landed"); if (!b.open) inc("lateLanded");
        land.push({ foe, f, side: b.side, u });''',
'''        inc("landed"); if (!b.open) inc("lateLanded");
        land.push({ foe, f, side: b.side, u });
        expV.push({ w: "ironhail-land", L: land.length - 1, kill: fp.hp > 0 && foe.hp <= 0 });
        pendRes[b.side].push({ x: b.x, y: b.y, hit: true });'''),
('''        inc("missed");
        if (hs.length) fail(4, "a miss that struck");''',
'''        inc("missed");
        expV.push({ w: "ironhail-miss" });
        pendRes[b.side].push({ x: b.x, y: b.y, hit: false });
        if (hs.length) fail(4, "a miss that struck");'''),
# ---- tickHail: the voices of the call, after the windows
('''    if (newBolts.length !== dropped) fail(2, `${newBolts.length - dropped} bolt(s) from a closed window`);
''',
'''    if (newBolts.length !== dropped) fail(2, `${newBolts.length - dropped} bolt(s) from a closed window`);
    /* [10] THE CALL'S VOICES: exactly its resolved bolts', in order -- a landing's thud at the
       count its foe carries after that landing's sunder (in the apply, and when the voice plays),
       a miss's thud -- and nothing else but a ward's own shatter voice (shatter() plays
       SFX.play("hit", {crit: true}) inside hurt(), once a break). A close sounds nothing. */
    if (stage6v){
      const tv = voices.slice(v0);
      const iv = tv.filter(x => x[0] === "ult" && ihVoice(x[1])), ov = tv.filter(x => !(x[0] === "ult" && ihVoice(x[1])));
      const sund = applies.filter(x => x[1] === "sunder");
      const got = iv.map(x => x[1].w + (x[1].w === "ironhail-land" ? ":" + x[1].n + "@" + x[2] : ""));
      const want = expV.map(e => { if (e.w !== "ironhail-land") return e.w;
                                   const k = sund[e.L] ? sund[e.L][4] : "none"; return e.w + ":" + k + "@" + k; });
      const shV = ov.filter(x => x[0] === "hit" && x[1] && x[1].crit === true).length;
      const closed = wins.filter(w => w.f.ultHail !== w.Z);
      if (JSON.stringify(got) !== JSON.stringify(want)) fail(10, `tickHail voiced ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
      else if (ov.length !== shV || shV !== shattered) fail(10, `tickHail also played ${JSON.stringify(ov.map(vname))} with ${shattered} ward break(s)`);
      else {
        for (const e of expV){
          if (e.w === "ironhail-miss") inc("missVoice");
          else { inc("landVoice"); const k = sund[e.L][4]; inc("landN" + k); if (e.kill) inc("killLandVoice"); }
        }
        if (shV) inc("shatterVoiceOk", shV);
        for (const w of closed){ if (w.f.alive && w.foe.alive) inc("clockCloseSilent"); else inc("deathCloseSilent"); }
      }
    }
'''),
# ---- the fight loop: the drawn subset, the verdict, and the resolved-bolt ledger
('''  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "ironhail", sd) : new AC.Match("ironhail", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.hailTally) for (const k in T) T[k] += me.hailTally[k];
  }''',
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
    const vis = m.hail.length > 0 || [m.a, m.b].some(q => q.quarrelFade > 0 || q.quarrelFx.length);
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
    const m = side ? new AC.Match(fid, "ironhail", sd) : new AC.Match("ironhail", fid, sd);
    const me = side ? m.b : m.a;
    per = { in: 0, out: 0 };
    curM = m; voices.length = 0; pendRes.a.length = 0; pendRes.b.length = 0;
    const drawn = drawOn && sd === seeds[0];
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); }
    fights++; bin += per.in; bout += per.out;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.hailTally) for (const k in T) T[k] += me.hailTally[k];
    /* THE VERDICT (stage 6): 0.51s past `over`, the step hook passing straight
       through. Limbs up at `over` cool to 0 in it; every resolved bolt has
       been shown. */
    if (stage6p && m.over){
      const upAtOver = me.quarrelFade > 0;
      postOver = true;
      try { for (let k = 0; k < 61; k++){ m.step(DT); steps++; if (drawn) drawFrame(m, steps); } }
      finally { postOver = false; }
      if (upAtOver){ if (me.quarrelFade !== 0) fail(11, `limbs up at \\`over\\` still at ${me.quarrelFade} 0.51s into the verdict`); else inc("coolAtVerdict"); }
      if (pendRes.a.length || pendRes.b.length) fail(11, `${pendRes.a.length + pendRes.b.length} resolved bolt(s) the picture never showed`);
    }
  }'''),
('''    const m = new AC.Match("ironhail", fid, seeds[0]);
    per = null; forceOnce = true;''',
'''    const m = new AC.Match("ironhail", fid, seeds[0]);
    per = null; forceOnce = true;
    curM = m; voices.length = 0; pendRes.a.length = 0; pendRes.b.length = 0;'''),
# ---- the run's end: the accounting
('''  P.tickHail = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.tickFire = oLoose; P.resolveHit = oResolve; P.step = oStep;''',
'''  P.tickHail = oTick; P.fireUlt = oFire; P.tickWeapon = oWeap; P.tickFire = oLoose; P.resolveHit = oResolve; P.step = oStep;
  curM = null;
  if (stage6v){
    AC.SFX.play = oPlay;
    /* EVERY IRONHAIL VOICE OF THE RUN, ACCOUNTED FOR by its event (both passes and every verdict). */
    const want = { "ironhail": n.castVoice || 0, "ironhail-land": n.landVoice || 0, "ironhail-miss": n.missVoice || 0 };
    for (const k of new Set([...Object.keys(want), ...Object.keys(ihAll)]))
      if ((ihAll[k] || 0) !== (want[k] || 0)) fail(10, `${ihAll[k] || 0} '${k}' voices in the run, ${want[k] || 0} accounted for`);
  }
  if (stage6p) P.tickQuarrel = oQuarrel;'''),
('''  return { n, bad, T, fights, win: wins / decided,''',
'''  return { n, bad, T, fights, win: wins / decided, stage6v, stage6p, drawOn, ihAll,'''),
# ---- the Python side
('''    R = page.evaluate(JS, [seeds])''', '''    R = page.evaluate(JS, [seeds, 0 if a.no_draw else a.draw_every])'''),
('''ok = 0
for k, text, cover in checks:''',
'''if R.get("stage6v"):
    ns = {k: n[k] for k in sorted(n, key=lambda k: (len(k), k)) if k.startswith("landN")}
    print(f"  stage 6 voice: casts {n.get('castVoice',0)}  landing thuds {n.get('landVoice',0)} (n "
          f"{', '.join(f'{k[5:]}:{v}' for k, v in ns.items())}; {n.get('killLandVoice',0)} on a killing landing)  "
          f"miss thuds {n.get('missVoice',0)}  ward shatters' own voice {n.get('shatterVoiceOk',0)}  silent closes: "
          f"{n.get('clockCloseSilent',0)} clock, {n.get('deathCloseSilent',0)} death   run totals {R['ihAll']}")
    checks.append((10, "stage 6 voice: one cast voice a cast; one landing thud a landed bolt at the foe's count after its sunder, "
                       "one miss thud a missed bolt, in order; nothing else in tickHail but a ward's own shatter; no close voice; "
                       "every voice accounted for",
                   all(n.get(k, 0) > 0 for k in ("castVoice", "landVoice", "missVoice", "killLandVoice", "shatterVoiceOk",
                                                 "clockCloseSilent", "deathCloseSilent"))))
if R.get("stage6p"):
    print(f"  stage 6 picture: tickQuarrel calls clean {n.get('quarrelOk',0)}  limbs up {n.get('limbsUp',0)}, cooling "
          f"{n.get('limbsCool',0)}  puffs at their bolts {n.get('puffOk',0)} ({n.get('puffHit',0)} landed, {n.get('puffMiss',0)} "
          f"missed)  the foe's count tagged {n.get('landTagOk',0)}  killing landings untagged {n.get('killNoTag',0)}  "
          f"cooled in the verdict {n.get('coolAtVerdict',0)}  drawn frames {n.get('drawOk',0)} ({n.get('drawPic',0)} with the "
          f"picture up, {n.get('drawPicStop',0)} of them in a hit stop, {n.get('drawVerdict',0)} in the verdict)"
          + ("" if R.get("drawOn") else "   (drawn subset OFF)"))
    checks.append((11, "stage 6 picture: tickQuarrel writes no sim field and draws no RNG; the limbs up exactly while the window is; "
                       "one puff a resolved bolt at its spot, hit or miss; the foe's count tagged, a kill untagged; cooled in the "
                       "verdict; no drawn frame throws, draws the RNG or writes the sim",
                   all(n.get(k, 0) > 0 for k in ("quarrelOk", "limbsUp", "limbsCool", "puffHit", "puffMiss", "landTagOk",
                                                 "killNoTag", "coolAtVerdict"))
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
