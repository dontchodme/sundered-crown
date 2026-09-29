"""[1] SIM IDENTITY: every step of every fight hashed (positions, velocities, angles, hp, shield, statuses,
charge, stun, pin, hitCd, the flail head, the runes' window {t, dur, cd}, its tally, the beats' count, shots,
shades), the BASE link (links/sc-lodestone-b205.html) against ld-final.html (the rows applied: THE STAMP),
undrawn AND drawn. [2] WHOLE FIGHTS DRAWN on ld-final through the kill and 3s of verdict, the post chain
alternating on/off: nothing may throw; every touch (captured INSIDE tickRunes by a harness-side wrapper on the
match instance, which only reads) is found exactly once by the picture -- one lodeFx record, its spot the foe's
own position at the touch test, its walls the test's own sides -- except on the kill's step; every touch on a
live foe shows the foe's hex count on a hex tag within 3R of it; the bar is drawn on exactly ONE frame of a
60 fps render (both phases of the 2-step cadence counted); the walls' go-dark timed (clock close, the caster's
death, the verdict); the shared weapon row never written. [3] THE CONTROL: ld-control.html is ld-final plus
ONE sim write in tickLode's touch branch (the foe's vx nudged by 1e-9) -- it must DIFFER on every Lodestone
fight with a touch, and match the fights without Lodestone."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-lodestone-b205.html").resolve()
PAIRS = [("lodestone", "spellbreaker", 99015), ("dawnbringer", "lodestone", 99001), ("lodestone", "gravemourn", 99015),
         ("twinshade", "lodestone", 99008), ("lodestone", "grudgebearer", 31337), ("aureole", "lodestone", 4101),
         ("lodestone", "shroudmaul", 2207), ("ironwood", "lodestone", 1234), ("lodestone", "bindweed", 2317),
         ("morningstar", "lodestone", 8888), ("lodestone", "paradox", 5150), ("gloamwire", "lodestone", 4242),
         ("axiom", "grudgebearer", 31337), ("morningstar", "lastlight", 4242)]

TRACE = r"""([a, b, seed, draw]) => {
  window.__frozen = true;
  AC.setResolution(270, 480);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const DT = AC.CONFIG.physics.dt, RB = AC.CONFIG.physics.ballR, AR = AC.CONFIG.arena, BOLT = 0.0125;
  const W0 = AC.WEAPONS.find(w => w.id === "lodestone");
  const w0 = JSON.stringify(W0);
  const m = new AC.Match(a, b, seed);
  const r = AC.renderer;
  const HAS = typeof m.tickLode === "function";
  let step = 0;
  /* THE TOUCHES, read inside tickRunes (harness-side, on this instance; it reads and writes nothing) */
  const touches = [];
  const tr = m.tickRunes;
  m.tickRunes = function(dt){
    const pre = [this.a, this.b].map(f => f.runeTally ? f.runeTally.touches : 0);
    const pos = [[this.b.x, this.b.y], [this.a.x, this.a.y]];
    tr.call(this, dt);
    [this.a, this.b].forEach((f, j) => { const T = f.runeTally;
      if (T && T.touches > pre[j]) touches.push({ step: step + 1, j, k: T.touches, x: pos[j][0], y: pos[j][1],
                                                   n: this.inset || 0, pad: f.w.ult.pad }); });
  };
  const buf = new DataView(new ArrayBuffer(8));
  let h1 = 0x811c9dc5 | 0, h2 = 0x1234567 | 0;
  const mix = (v) => { buf.setFloat64(0, +v || 0);
    for (let i = 0; i < 8; i++){ const x = buf.getUint8(i);
      h1 = Math.imul(h1 ^ x, 16777619); h2 = Math.imul(h2 ^ (x + i), 2246822519); } };
  const fstate = (f) => { mix(f.x); mix(f.y); mix(f.vx); mix(f.vy); mix(f.hp); mix(f.shield); mix(f.shieldMax);
    mix(f.theta); mix(f.charge); mix(f.stun || 0); mix(f.alive ? 1 : 0); mix(f.pin || 0); mix(f.pinFree || 0);
    mix(f.reachMul); for (const c of f.hitCd) mix(c || 0); mix(f.tips.length); mix(f.clanks); mix(f.hits); mix(f.dealt);
    mix(f.headX || 0); mix(f.headY || 0); mix(f.headSpin || 0); mix(f.headAngVel || 0); mix(f.spinDir || 0);
    mix(f.fireCd || 0); mix(f.stunDR || 0);
    for (const k of Object.keys(f.status).sort()){ const s = f.status[k]; mix(k.length); mix(s.stacks || 0); mix(s.t || 0); }
    const Z = f.ultRunes; if (Z){ mix(Z.t); mix(Z.dur); mix(Z.cd); } else mix(-1);
    const T = f.runeTally; if (T){ for (const k of ["casts", "frames", "touches", "hexes", "hurls", "foeStk"]) mix(T[k]); } else mix(-2); };
  const out = { draws: 0, thrown: null, lodeFrames: 0, stopLodeFrames: 0, windows: 0, res: null,
                touches: 0, killStep: 0, found: 0, foundBad: [], spotOK: 0, spotBad: [], wallOK: 0, wallBad: [], corners: 0,
                tagOK: 0, tagBad: [], bolt0: {}, bolt1: {}, boltDrawn: {}, closes: [], deaths: [], fadeAtOver: null,
                fadeZeroAfterOver: null, maxFx: 0, wWritten: false, hasPic: HAS };
  const mes = [m.a, m.b].filter(f => f.w.id === "lodestone");
  if (Object.prototype.hasOwnProperty.call(r, "_lodeBolt")) delete r._lodeBolt;   // a previous fight's wrapper
  if (draw && HAS){
    const lb = r._lodeBolt;
    r._lodeBolt = function(mm, f, G, P){
      const foe = f === mm.a ? mm.b : mm.a;
      for (const q of f.lodeFx) if (!mm.over && mm.t - q.t0 < BOLT && foe.alive){ const key = (f === mm.a ? "a" : "b") + q.k; out.boltDrawn[key] = (out.boltDrawn[key] || 0) + 1; }
      return lb.call(this, mm, f, G, P);
    };
  }
  let over = -1, tSeen = 0;
  const prev = new Map(), closeStep = new Map();
  while (step < 200 / DT){
    m.step(DT); step++;
    fstate(m.a); fstate(m.b); mix(m.t); mix(m.hitStop); mix(m.inset); mix(m.beats.length); mix(m.shots.length);
    for (const s of m.shades){ mix(s.x); mix(s.y); mix(s.hp); }
    /* the touches this step, against the picture's records */
    for (; tSeen < touches.length; tSeen++){
      const t = touches[tSeen], f = t.j ? m.b : m.a, foe = t.j ? m.a : m.b;
      out.touches++;
      if (!HAS) continue;
      if (m.over || !foe.alive){ out.killStep++; continue; }
      const recs = f.lodeFx.filter(q => q.k === t.k);
      if (recs.length === 1) out.found++; else { out.foundBad.push([+m.t.toFixed(3), recs.length]); continue; }
      const q = recs[0];
      if (q.x === t.x && q.y === t.y) out.spotOK++; else out.spotBad.push([+m.t.toFixed(3), q.x, q.y, t.x, t.y]);
      const R = RB, e = t.pad, n = t.n, want = [];
      if (t.y <= n + R + e) want.push(0);
      if (t.x >= AR.w - n - R - e) want.push(1);
      if (t.y >= AR.h - n - R - e) want.push(2);
      if (t.x <= n + R + e) want.push(3);
      if (JSON.stringify(want) === JSON.stringify(q.walls) && want.length) out.wallOK++; else out.wallBad.push([+m.t.toFixed(3), want, q.walls]);
      if (want.length > 1) out.corners++;
      if (foe.hp > 0){
        const k = foe.stacks("hex");
        const g = m.tags.find(g2 => g2.key === "hex" && g2.val === k && Math.hypot(g2.x - foe.x, g2.y - foe.y) < RB * 3.01);
        if (g) out.tagOK++; else out.tagBad.push([+m.t.toFixed(3), k, m.tags.filter(g2 => g2.key === "hex").map(g2 => [g2.val, g2.first])]);
      }
    }
    mes.forEach((me) => {
      const Z = me.ultRunes, sd = me === m.a ? "a" : "b";
      if (Z && !prev.get(me)) out.windows++;
      if (!Z && prev.get(me) && !m.over) closeStep.set(me, [step, me.alive]);
      prev.set(me, Z);
      if (HAS){
        /* the bar at a 60 fps cadence, both phases */
        for (const q of me.lodeFx){ if (!m.over && m.t - q.t0 < BOLT){ const o = step % 2 ? out.bolt1 : out.bolt0; o[sd + q.k] = (o[sd + q.k] || 0) + 1; } }
        const cs = closeStep.get(me);
        if (cs && !(me.lodeFade > 0)){ (cs[1] ? out.closes : out.deaths).push(+((step - cs[0]) * DT).toFixed(4)); closeStep.delete(me); }
        out.maxFx = Math.max(out.maxFx, me.lodeFx.length);
      }
    });
    if (m.over && over < 0){ over = step; out.hashAtOver = [h1 >>> 0, h2 >>> 0]; out.stepsAtOver = step;
      out.res = Object.assign(m.summary(), { t: m.t, hpA: m.a.hp, hpB: m.b.hp });
      if (mes.length) out.fadeAtOver = mes.map(f => [f.lodeFade, f.alive, !!f.ultRunes]); }
    if (draw){
      const vis = HAS && mes.some(f => f.lodeFade > 0 || f.lodeFx.length);
      const near = HAS && mes.some(f => f.lodeFx.some(q => q.t < 0.1));
      /* a 60 fps cadence (every 2nd step) while a touch is fresh, so the bar's frame count is a real render's */
      if (near ? step % 2 === 0 : (step % 24 === 0 || (vis && step % 3 === 0) || (over >= 0 && step % 6 === 0))){
        try { AC.POSTFX.on = (step % 4 < 2); AC.__draw(m); out.draws++;
              if (vis){ out.lodeFrames++; if (m.hitStop > 0) out.stopLodeFrames++; } }
        catch (e){ out.thrown = String(e.stack || e); break; }
      }
      if (HAS && mes.length && over >= 0 && out.fadeZeroAfterOver === null && mes.every(f => !(f.lodeFade > 0)))
        out.fadeZeroAfterOver = +((step - over) * DT).toFixed(4);
    }
    if (over >= 0 && step - over > (draw ? 3 : 0) / DT) break;
  }
  if (Object.prototype.hasOwnProperty.call(r, "_lodeBolt")) delete r._lodeBolt;
  out.steps = step; out.hash = [h1 >>> 0, h2 >>> 0];
  out.wWritten = JSON.stringify(W0) !== w0;
  /* the bar: frames per touch at each phase of a 60 fps cadence */
  const cnt = (o) => { const h = {}; for (const v of Object.values(o)) h[v] = (h[v] || 0) + 1; return h; };
  out.boltHist0 = cnt(out.bolt0); out.boltHist1 = cnt(out.bolt1); out.boltDrawnHist = cnt(out.boltDrawn);
  delete out.bolt0; delete out.bolt1; delete out.boltDrawn;
  for (const k of ["foundBad", "spotBad", "wallBad", "tagBad"]) out[k] = out[k].slice(0, 5);
  return out;
}"""


def make_control():
    s = (HERE / "ld-final.html").read_text(encoding="utf-8")
    old = "        if (f.lodeFx.length > 6) f.lodeFx.shift();\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "        foe.vx += 1e-9;                          // CONTROL: a sim write\n")
    (HERE / "ld-control.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    make_control()
    runs = {}
    for label, path, draw in (("base", BASE, False), ("final", HERE / "ld-final.html", False),
                              ("final drawn", HERE / "ld-final.html", True),
                              ("CONTROL (must differ)", HERE / "ld-control.html", False)):
        with game(game_path=path) as (page, errors):
            for a, b, s in PAIRS:
                r = page.evaluate(TRACE, [a, b, s, draw])
                assert not errors, errors[:3]
                runs.setdefault((a, b, s), {})[label] = r
                if draw:
                    print(f"  [{label}] {a} v {b} {s}: draws {r['draws']} thrown {r['thrown']} windows {r['windows']} touches {r['touches']} "
                          f"(kill step {r['killStep']}) found {r['found']} bad {r['foundBad']} spot {r['spotOK']} bad {r['spotBad']} "
                          f"walls {r['wallOK']} bad {r['wallBad']} (corners {r['corners']}) tag {r['tagOK']} bad {r['tagBad']} | "
                          f"bar frames/touch @60fps phase0 {r['boltHist0']} phase1 {r['boltHist1']} drawn {r['boltDrawnHist']} | "
                          f"lode frames {r['lodeFrames']} (stop {r['stopLodeFrames']}) close->0 {r['closes']} death->0 {r['deaths']} "
                          f"| at kill {r['fadeAtOver']} -> 0 after {r['fadeZeroAfterOver']} s | max records {r['maxFx']} | w written {r['wWritten']}", flush=True)
    ok = True; ctrl_ok = True
    for k, v in runs.items():
        base = v["base"]
        for lab in ("final", "final drawn", "CONTROL (must differ)"):
            o = v[lab]
            same = (o["res"] == base["res"]) and o["hashAtOver"] == base["hashAtOver"] and o["stepsAtOver"] == base["stepsAtOver"]
            if lab.startswith("CONTROL"):
                has = "lodestone" in (k[0], k[1])
                good = (not same) if (has and base["touches"] > 0) else same if not has else True
                ctrl_ok &= good
                print(f"{k}: {lab:22s} {'DIFFERS' if not same else 'IDENTICAL'}  touches {base['touches']} (control {'bit' if good else 'DID NOT BITE'})")
                continue
            ok &= same
            print(f"{k}: {lab:14s} {'IDENTICAL' if same else 'DIFFERS'}  steps@kill {o['stepsAtOver']} hash@kill {o['hashAtOver']} "
                  f"winner {o['res']['winner']} t {o['res']['t']!r} touches {o['touches']}")
    print("SIM IDENTITY:", "PASS" if ok else "FAIL", "| CONTROL:", "BIT ON EVERY LODESTONE FIGHT WITH A TOUCH" if ctrl_ok else "DID NOT BITE")
    (HERE / "verify.json").write_text(json.dumps({str(k): v for k, v in runs.items()}, indent=1, default=str))
