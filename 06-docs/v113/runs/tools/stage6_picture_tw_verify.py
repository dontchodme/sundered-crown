"""[1] SIM IDENTITY: every step of every fight hashed (positions, velocities, angles, hp, shield, statuses, charge,
pin / pinFree / pinV, hitCd, the flail head, Bramblesnare's window {t, dur}, brambleCd, brambleIn, its tally, every
bramble in m.brambles, m.brambleT, the shades, the shots, the beats' count), the BASE link
(links/sc-thornwake-b26.5.html) against tw-final.html (the rows applied: THE STAMP) and tw-final-fx.html (SPECS.thornwake
out, as shipped), undrawn AND drawn.
[2] WHOLE FIGHTS DRAWN on tw-final-fx through the kill and 3s of verdict, the post chain alternating on/off: nothing
may throw; after every step the picture's bramble records are exactly Thornwake's brambles in m.brambles (same
objects, none missing, none extra); THE HELD BALL against a harness-side model (held from the step
`brambleTally.snares` rises with the foe pinned, until its pin runs out or it dies); THE HEXAGON: on the first held
frame of each snare, `_drawField` on the held ball strokes nothing, and with `brierHeld` put to 0 for that one call
(the CONTROL) it strokes the hexagon; THE TAG RULE's invariants: every tag the picture prints is ENTANGLE with the
foe's count at the foe on a step whose bites rose, never over an ENTANGLE tag already up at the foe, and never the
count it printed last; the blade's green cools after a clock close, a death, or the verdict (timed), and the brambles
are gone within 0.35s of the verdict; the shared weapon row never written.
[3] THE CONTROL: tw-control.html is tw-final plus ONE sim write in tickBrier's tag branch (the foe's vx nudged by
1e-9) -- it must DIFFER on every Thornwake fight with a tagged bite, and match the fights without Thornwake."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-thornwake-b26.5.html").resolve()
PAIRS = [("thornwake", "aureole", 4101), ("gravemourn", "thornwake", 99015), ("thornwake", "grudgebearer", 31337),
         ("dawnbringer", "thornwake", 99001), ("thornwake", "nightfell", 5150), ("lastlight", "thornwake", 4242),
         ("thornwake", "morningstar", 8888), ("shroudmaul", "thornwake", 1234), ("thornwake", "paradox", 2317),
         ("censer", "thornwake", 2207), ("thornwake", "twinshade", 99008), ("bindweed", "thornwake", 2317),
         ("thornwake", "heartwood", 2207),
         ("axiom", "grudgebearer", 31337), ("morningstar", "lastlight", 4242)]

TRACE = r"""([a, b, seed, draw]) => {
  window.__frozen = true;
  AC.setResolution(270, 480);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const DT = AC.CONFIG.physics.dt, RB = AC.CONFIG.physics.ballR;
  const W0 = AC.WEAPONS.find(w => w.id === "thornwake");
  const w0 = JSON.stringify(W0);
  const m = new AC.Match(a, b, seed);
  const r = AC.renderer;
  const buf = new DataView(new ArrayBuffer(8));
  let h1 = 0x811c9dc5 | 0, h2 = 0x1234567 | 0;
  const mix = (v) => { buf.setFloat64(0, +v || 0);
    for (let i = 0; i < 8; i++){ const x = buf.getUint8(i);
      h1 = Math.imul(h1 ^ x, 16777619); h2 = Math.imul(h2 ^ (x + i), 2246822519); } };
  const fstate = (f) => { mix(f.x); mix(f.y); mix(f.vx); mix(f.vy); mix(f.hp); mix(f.shield); mix(f.shieldMax);
    mix(f.theta); mix(f.charge); mix(f.stun || 0); mix(f.alive ? 1 : 0); mix(f.pin || 0); mix(f.pinFree || 0);
    mix(f.pinMax || 0); if (f.pinV){ mix(f.pinV[0]); mix(f.pinV[1]); } else mix(-3);
    mix(f.reachMul); for (const c of f.hitCd) mix(c || 0); mix(f.tips.length); mix(f.clanks); mix(f.hits); mix(f.dealt);
    mix(f.headX || 0); mix(f.headY || 0); mix(f.headSpin || 0); mix(f.headAngVel || 0); mix(f.spinDir || 0);
    mix(f.fireCd || 0); mix(f.shotsFired || 0); mix(f.swingPhase || 0);
    for (const k of Object.keys(f.status).sort()){ const s = f.status[k]; mix(k.length); mix(s.stacks || 0); mix(s.t || 0); }
    const Z = f.ultBramble; if (Z){ mix(Z.t); mix(Z.dur); } else mix(-1);
    mix(f.brambleCd || 0); mix(f.brambleIn ? 1 : 0);
    const T = f.brambleTally; if (T){ for (const k of ["casts", "frames", "planted", "tested", "after", "foeIn", "entries", "snares", "ticks", "dealt", "ent", "kills"]) mix(T[k]); } else mix(-2); };
  const out = { draws: 0, thrown: null, picFrames: 0, stopPicFrames: 0, windows: 0, res: null,
                ticks: 0, snares: 0, tags: 0, tagBad: [], picBad: 0, heldBad: 0, heldFrames: 0, hexChecks: 0, hexBad: 0, hexCtl: 0,
                brambles: 0, closes: [], deaths: [], endAtOver: null, endZeroAfterOver: null, maxPic: 0, wWritten: false };
  const mes = [m.a, m.b].filter(f => f.w.id === "thornwake");
  if (draw && typeof m.tickBrier === "function"){
    const tq = m.tickBrier;
    m.tickBrier = function(dt){
      const before = new Set(this.tags);
      tq.call(this, dt);
      for (const g of this.tags) if (!before.has(g)) g.__brier = true;
    };
  }
  /* counts strokes a call makes on the renderer's context */
  const strokes = (fn) => { const c = r.ctx, s0 = c.stroke; let n = 0;
    c.stroke = function(){ n++; return s0.apply(this, arguments); };
    c.save(); try { fn(); } finally { c.restore(); c.stroke = s0; } return n; };
  const model = new Map();
  for (const f of mes) model.set(f, { snares: 0, ticks: 0, held: false, lastVal: null });
  let step = 0, over = -1;
  const prev = new Map(), closeStep = new Map();
  while (step < 200 / DT){
    const tagsBefore = new Set(m.tags);
    const near0 = new Map();
    for (const me of mes){ const th = me === m.a ? m.b : m.a;
      near0.set(me, m.tags.some(g => g.key === "entangle" && g.life > 0.35 && Math.hypot(g.x - th.x, g.y - th.y) < RB * 3)); }
    m.step(DT); step++;
    fstate(m.a); fstate(m.b); mix(m.t); mix(m.hitStop); mix(m.inset); mix(m.beats.length); mix(m.brambleT);
    mix(m.brambles.length);
    for (const bb of m.brambles){ mix(bb.x); mix(bb.y); mix(bb.t0); mix(bb.side === "a" ? 1 : 2); }
    for (const s of m.shots){ mix(s.x); mix(s.y); mix(s.vx); mix(s.vy); mix(s.life); mix(s.own === "a" ? 1 : 2); }
    for (const s of m.shades){ mix(s.x); mix(s.y); mix(s.hp); }
    for (const me of mes){
      const th = me === m.a ? m.b : m.a, T = me.brambleTally, side = me === m.a ? "a" : "b";
      const Z = me.ultBramble;
      if (Z && !prev.get(me)) out.windows++;
      if (!Z && prev.get(me) && !m.over) closeStep.set(me, [step, me.alive && th.alive]);
      prev.set(me, Z);
      if (!draw) continue;
      const G = m.brambles.filter(bb => bb.side === side), P = me.brierPic.map(p => p.b);
      if (G.length !== P.length || G.some(bb => P.indexOf(bb) < 0)) out.picBad++;
      out.maxPic = Math.max(out.maxPic, P.length);
      const M = model.get(me);
      if (T){
        const dS = T.snares - M.snares, dK = T.ticks - M.ticks;
        M.snares = T.snares; M.ticks = T.ticks; out.ticks += dK; out.snares += dS;
        if (M.held && !(th.pin > 0 && th.alive)) M.held = false;
        let fresh = false;
        if (dS > 0 && th.alive && th.pin > 0 && !th.pinFree){ fresh = !M.held; M.held = true; }
        if (M.held !== !!th.brierHeld) out.heldBad++;
        if (M.held) out.heldFrames++;
        /* the hexagon, on the first held frame of each snare */
        if (fresh && M.held && !th.ultField){
          out.hexChecks++;
          const n1 = strokes(() => r._drawField(m, th));
          const hv = th.brierHeld; th.brierHeld = 0;
          const n0 = strokes(() => r._drawField(m, th));
          th.brierHeld = hv;
          if (n1 !== 0) out.hexBad++;
          if (n0 > 0) out.hexCtl++;
        }
        const nt = m.tags.filter(g => !tagsBefore.has(g) && g.__brier);
        out.tags += nt.length;
        if (nt.length > 1) out.tagBad.push([+m.t.toFixed(3), "two tags", nt.length]);
        for (const g of nt){
          if (g.key !== "entangle") out.tagBad.push([+m.t.toFixed(3), "key", g.key]);
          if (!(dK > 0)) out.tagBad.push([+m.t.toFixed(3), "no bite"]);
          if (g.val !== th.stacks("entangle") || Math.hypot(g.x - th.x, g.y - th.y) > 1e-6) out.tagBad.push([+m.t.toFixed(3), "val/pos", g.val, th.stacks("entangle")]);
          if (near0.get(me)) out.tagBad.push([+m.t.toFixed(3), "over a tag already up"]);
          if (M.lastVal !== null && g.val === M.lastVal) out.tagBad.push([+m.t.toFixed(3), "same count", g.val]);
          M.lastVal = g.val;
        }
      }
      const cs = closeStep.get(me);
      if (cs && !(me.brierGreen > 0)){ (cs[1] ? out.closes : out.deaths).push(+((step - cs[0]) * DT).toFixed(4)); closeStep.delete(me); }
    }
    if (m.over && over < 0){ over = step; out.hashAtOver = [h1 >>> 0, h2 >>> 0]; out.stepsAtOver = step;
      out.res = Object.assign(m.summary(), { t: m.t, hpA: m.a.hp, hpB: m.b.hp });
      if (mes.length) out.endAtOver = mes.map(f => [f.brierGreen, f.brierPic ? f.brierPic.length : null, f.alive, !!f.ultBramble]); }
    if (draw){
      const vis = mes.some(f => f.brierGreen > 0 || f.brierPic.length || f.brierBite.length)
                  || [m.a, m.b].some(f => f.brierRootFade > 0);
      if (step % 24 === 0 || (vis && step % 3 === 0) || (over >= 0 && step % 6 === 0)){
        try { AC.POSTFX.on = (step % 2 === 0); AC.__draw(m); out.draws++;
              if (vis){ out.picFrames++; if (m.hitStop > 0) out.stopPicFrames++; } }
        catch (e){ out.thrown = String(e.stack || e); break; }
      }
      if (mes.length && over >= 0 && out.endZeroAfterOver === null){
        const gone = mes.every(f => !(f.brierGreen > 0) && (f.brierEnd >= 0.6 || !f.brierPic.length));
        if (gone) out.endZeroAfterOver = +((step - over) * DT).toFixed(4);
      }
    }
    if (over >= 0 && step - over > (draw ? 3 : 0) / DT) break;
  }
  out.brambles = mes.reduce((s, f) => s + (f.brambleTally ? f.brambleTally.planted : 0), 0);
  out.steps = step; out.hash = [h1 >>> 0, h2 >>> 0];
  out.wWritten = JSON.stringify(W0) !== w0;
  out.tagBad = out.tagBad.slice(0, 5);
  return out;
}"""


def make_control():
    s = (HERE / "tw-final.html").read_text(encoding="utf-8")
    old = "        f.brierTagN = n; f.brierTagT = "
    assert s.count(old) == 1
    s = s.replace(old, "        foe.vx += 1e-9;                          // CONTROL: a sim write\n" + old)
    (HERE / "tw-control.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    make_control()
    runs = {}
    for label, path, draw in (("base", BASE, False), ("final", HERE / "tw-final.html", False),
                              ("final-fx", HERE / "tw-final-fx.html", False),
                              ("final-fx drawn", HERE / "tw-final-fx.html", True),
                              ("CONTROL (must differ)", HERE / "tw-control.html", False)):
        with game(game_path=path) as (page, errors):
            for a, b, s in PAIRS:
                r = page.evaluate(TRACE, [a, b, s, draw])
                assert not errors, errors[:3]
                runs.setdefault((a, b, s), {})[label] = r
                if draw:
                    print(f"  [{label}] {a} v {b} {s}: draws {r['draws']} thrown {r['thrown']} windows {r['windows']} brambles {r['brambles']} "
                          f"(max {r['maxPic']} at once) pic!=sim {r['picBad']} | snares {r['snares']} held frames {r['heldFrames']} held!=model {r['heldBad']} "
                          f"| hexagon: {r['hexChecks']} snares checked, drawn on a held ball {r['hexBad']}, control drew it {r['hexCtl']} "
                          f"| bites {r['ticks']} tags {r['tags']} bad {r['tagBad']} | picture frames {r['picFrames']} (stop {r['stopPicFrames']}) "
                          f"close->0 {r['closes']} death->0 {r['deaths']} | at kill {r['endAtOver']} -> gone after {r['endZeroAfterOver']} s "
                          f"| w written {r['wWritten']}", flush=True)
    ok = True; ctrl_ok = True; draw_ok = True
    for k, v in runs.items():
        base = v["base"]
        dr = v["final-fx drawn"]
        draw_ok &= (dr["thrown"] is None and dr["picBad"] == 0 and dr["heldBad"] == 0 and not dr["tagBad"] and not dr["wWritten"]
                    and dr["hexBad"] == 0 and dr["hexCtl"] == dr["hexChecks"])
        for lab in ("final", "final-fx", "final-fx drawn", "CONTROL (must differ)"):
            o = v[lab]
            same = (o["res"] == base["res"]) and o["hashAtOver"] == base["hashAtOver"] and o["stepsAtOver"] == base["stepsAtOver"]
            if lab.startswith("CONTROL"):
                has = "thornwake" in (k[0], k[1])
                tagged = dr["tags"] > 0
                good = (not same) if (has and tagged) else same if not has else True
                ctrl_ok &= good
                print(f"{k}: {lab:22s} {'DIFFERS' if not same else 'IDENTICAL'}  tags {dr['tags']} (control {'bit' if good else 'DID NOT BITE'})")
                continue
            ok &= same
            print(f"{k}: {lab:14s} {'IDENTICAL' if same else 'DIFFERS'}  steps@kill {o['stepsAtOver']} hash@kill {o['hashAtOver']} "
                  f"winner {o['res']['winner']} t {o['res']['t']!r} windows {o['windows']}")
    print("SIM IDENTITY:", "PASS" if ok else "FAIL", "| DRAWN:", "PASS (nothing thrown, pic == sim, held == model, hexagon off / control on, tag invariants, row unwritten)" if draw_ok else "FAIL",
          "| CONTROL:", "BIT ON EVERY THORNWAKE FIGHT WITH A TAG" if ctrl_ok else "DID NOT BITE")
    (HERE / "verify.json").write_text(json.dumps({str(k): v for k, v in runs.items()}, indent=1, default=str))
