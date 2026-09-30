"""[1] SIM IDENTITY: every step of every fight hashed (positions, velocities, angles, hp, shield, statuses, charge,
stun, stunDR, hexClock, hexStunMul, reachMul, hitCd, the flail head, the Unmaking's window {t, dur}, its tally
{casts, frames, blows, extra, foeHex}, every shot, every shade, the beats' count), the BASE link
(links/sc-spellbreaker-b7.5.html) against sb-final.html (the rows applied: THE STAMP) and sb-final-fx.html (and
SPECS.spellbreaker out of the inlined fx.js, as the carry does), undrawn AND drawn.
[2] WHOLE FIGHTS DRAWN on sb-final-fx through the kill and 3s of verdict, the post chain alternating on/off: nothing may
throw, and the picture must be the mechanism's, rebuilt harness-side from inside the hooks:
  THE GREY -- every hex proc captured inside tickStatus (its own breakSpin call, with the hexStunMul it read): a proc at
    x2 starts a grey on that step, a proc at x1 never does, nothing else starts one; the grey stands only while that
    fighter's stun does; and an uninterrupted grey lasts exactly as many unfrozen steps as the doubled stun it draws
    (the stun's own countdown, measured beside it) -- the "longer grey";
  THE TAG -- every step her unmakeTally.extra rises by k prints exactly k `HEX +2` (hex tags pushed that step,
    relabelled), and no other tag is relabelled; a killing blow's tag stays plain;
  THE SCRIPT -- unmkFade is 1 on every step the window is open (not over, she alive) and 0 before her first cast; it
    reaches 0 within the unwrite after a clock close, a death, or the kill; the motes are born only in an open window;
  the cast record's life is 1.5 (the bolt's 1.4 retired); the banner lands on her, not the foe; the shared weapon row
  is never written.
[3] THE CONTROL: sb-control.html is sb-final-fx plus ONE sim write in tickUnmaking's tag branch (her vx nudged by 1e-9
at each relabel) -- it must DIFFER on every Spellbreaker fight with a +2 tag, and match the fights without her."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-spellbreaker-b7.5.html").resolve()
PAIRS = [("spellbreaker", "grudgebearer", 31337), ("dawnbringer", "spellbreaker", 99001), ("spellbreaker", "gravemourn", 99015),
         ("twinshade", "spellbreaker", 99008), ("spellbreaker", "nightfell", 5150), ("farwarden", "spellbreaker", 4101),
         ("spellbreaker", "ironhail", 99001), ("ironwood", "spellbreaker", 1234), ("spellbreaker", "bindweed", 2317),
         ("morningstar", "spellbreaker", 8888), ("spellbreaker", "portcullis", 5150), ("lastlight", "spellbreaker", 4242),
         ("spellbreaker", "heartwood", 2207), ("paradox", "spellbreaker", 4242), ("spellbreaker", "axiom", 777),
         ("spellbreaker", "twinshade", 2207),
         ("axiom", "grudgebearer", 31337), ("morningstar", "lastlight", 4242)]

TRACE = r"""([a, b, seed, draw]) => {
  window.__frozen = true;
  AC.setResolution(270, 480);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const DT = AC.CONFIG.physics.dt;
  const W0 = AC.WEAPONS.find(w => w.id === "spellbreaker");
  const w0 = JSON.stringify(W0);
  const m = new AC.Match(a, b, seed);
  const buf = new DataView(new ArrayBuffer(8));
  let h1 = 0x811c9dc5 | 0, h2 = 0x1234567 | 0;
  const mix = (v) => { buf.setFloat64(0, +v || 0);
    for (let i = 0; i < 8; i++){ const x = buf.getUint8(i);
      h1 = Math.imul(h1 ^ x, 16777619); h2 = Math.imul(h2 ^ (x + i), 2246822519); } };
  const fstate = (f) => { mix(f.x); mix(f.y); mix(f.vx); mix(f.vy); mix(f.hp); mix(f.shield); mix(f.shieldMax);
    mix(f.theta); mix(f.charge); mix(f.stun || 0); mix(f.stunDR || 0); mix(f.alive ? 1 : 0); mix(f.pin || 0); mix(f.pinFree || 0);
    mix(f.reachMul); mix(f.hexClock || 0); mix(f.hexStunMul); for (const c of f.hitCd) mix(c || 0); mix(f.tips.length); mix(f.clanks); mix(f.hits); mix(f.dealt);
    mix(f.headX || 0); mix(f.headY || 0); mix(f.headSpin || 0); mix(f.headAngVel || 0); mix(f.spinDir || 0);
    mix(f.fireCd || 0); mix(f.shotsFired || 0); mix(f.swingPhase || 0); mix(f.ultsFired || 0);
    for (const k of Object.keys(f.status).sort()){ const s = f.status[k]; mix(k.length); mix(s.stacks || 0); mix(s.t || 0); }
    const Z = f.ultUnmake; if (Z){ mix(Z.t); mix(Z.dur); } else mix(-1);
    const T = f.unmakeTally; if (T){ for (const k of ["casts", "frames", "blows", "extra", "foeHex"]) mix(T[k]); } else mix(-2); };
  const out = { draws: 0, thrown: null, picFrames: 0, stopPicFrames: 0, windows: 0, res: null,
                procs1: 0, procs2: 0, procs2NoStun: 0, greyStarts: 0, greyBad: [], greyNoStun: 0, greyLen: {}, stunLen: {}, lenBad: [],
                extra: 0, plus2: 0, tagBad: [], tagOther: [], runsOther: 0,
                fadeBad: [], closes: [], deaths: [], moteBad: 0, lifeAtCast: [], bannerOnHer: 0, bannerOnFoe: 0,
                fadeAtOver: null, fadeZeroAfterOver: null, wWritten: false };
  const mes = [m.a, m.b].filter(f => f.w.id === "spellbreaker");
  const me = mes[0] || null, th = me ? (me === m.a ? m.b : m.a) : null;
  /* the hex procs, captured inside tickStatus through its own breakSpin call (the probe's way) */
  const procs = [];
  let step = 0;
  if (draw && me){
    const ots = m.tickStatus;
    m.tickStatus = function(f, dt){
      const oBS = this.breakSpin;
      this.breakSpin = function(ff, reason, trueFor){
        if (ff === f && reason === "the hex takes the wind out of it" && (f === this.a || f === this.b))
          procs.push({ f, mul: ff.hexStunMul, step: step + 1 });
        return oBS.call(this, ff, reason, trueFor);
      };
      try { return ots.call(this, f, dt); } finally { delete this.breakSpin; }
    };
    const ost = m.statusTag;
    m.statusTag = function(x, y, key, first, val){
      const n0 = this.tags.length; const r = ost.call(this, x, y, key, first, val);
      if (this.tags.length) { const g = this.tags[this.tags.length - 1]; if (g && g.__s === undefined) g.__s = step + 1; }
      return r;
    };
  }
  let over = -1, prevZ = null, prevG = th ? 0 : 0, closeStep = null, cast0 = false, x0 = 0, mn0 = 0;
  const run = new Map();   // per greyed fighter: { unfrozen steps the grey stood, the stun it came with }
  while (step < 200 / DT){
    const frozen = !!(m.hitStop > 0 || m.latch || m.splitHold) || m.over;
    procs.length = 0;
    const ext0 = me && me.unmakeTally ? me.unmakeTally.extra : 0;
    const g0 = th ? th.unmkGrey : 0, ultFx0 = m.ultFx;
    m.step(DT); step++;
    fstate(m.a); fstate(m.b); mix(m.t); mix(m.hitStop); mix(m.inset); mix(m.beats.length); mix(m.shots.length);
    for (const s of m.shots){ mix(s.x); mix(s.y); mix(s.vx); mix(s.vy); mix(s.life); mix(s.own === "a" ? 1 : 2); }
    for (const s of m.shades){ mix(s.x); mix(s.y); mix(s.hp); mix(s.stun || 0); mix(s.hexClock || 0);
      for (const k of Object.keys(s.status).sort()){ mix(s.status[k].stacks || 0); mix(s.status[k].t || 0); } }
    if (me){
      const Z = me.ultUnmake;
      if (Z && !prevZ){ out.windows++;
        const u = m.ultFx; if (u && u.w === "spellbreaker") out.lifeAtCast.push(u.life);
        const B = m.banner; if (B && B.w === "spellbreaker"){
          if (Math.hypot(B.bx - me.x, B.by - me.y) < Math.hypot(B.bx - th.x, B.by - th.y)) out.bannerOnHer++; else out.bannerOnFoe++; } }
      if (!Z && prevZ && !m.over) closeStep = [step, me.alive && th.alive];
      prevZ = Z;
    }
    if (draw && me){
      /* THE SCRIPT */
      const open = !!me.ultUnmake && !m.over && me.alive;
      if (open && me.unmkFade !== 1) out.fadeBad.push([+m.t.toFixed(3), "open", me.unmkFade]);
      if (!me.unmakeTally && me.unmkFade !== 0) out.fadeBad.push([+m.t.toFixed(3), "before", me.unmkFade]);
      if (me.unmkMoteN > mn0 && !open) out.moteBad++;
      mn0 = me.unmkMoteN;
      if (closeStep && !(me.unmkFade > 0)){ (closeStep[1] ? out.closes : out.deaths).push(+((step - closeStep[0]) * DT).toFixed(4)); closeStep = null; }
      /* THE TAG */
      const dX = (me.unmakeTally ? me.unmakeTally.extra : 0) - ext0;
      const fresh = m.tags.filter(g => g.__s === step);
      const rel = fresh.filter(g => g.unmk);
      out.extra += dX; out.plus2 += rel.length;
      if (rel.length !== dX || rel.some(g => g.key !== "hex" || g.val !== "+2")) out.tagBad.push([+m.t.toFixed(3), dX, rel.map(g => [g.key, g.val])]);
      const other = m.tags.filter(g => g.unmk && !g.__ok && g.__s !== step);
      if (other.length) out.tagOther.push([+m.t.toFixed(3), other.length]);
      for (const g of rel) g.__ok = true;
      /* THE GREY, on the foe (the only fighter the Unmaking can double) and never on her */
      if (me.unmkGrey > 0) out.greyBad.push([+m.t.toFixed(3), "on her"]);
      const P2 = procs.filter(p => p.f === th && p.mul > 1), P1 = procs.filter(p => p.f === th && !(p.mul > 1));
      out.procs2 += P2.length; out.procs1 += P1.length;
      const g1 = th.unmkGrey;
      const started = g1 > 0 && (g1 > g0 + 1e-9 || P2.length > 0) && P2.length > 0;
      if (P2.length && !(g1 > 0) && th.alive && th.stun > 0) out.greyBad.push([+m.t.toFixed(3), "x2 proc, no grey", th.stun]);
      if (P2.length && !(g1 > 0) && !(th.stun > 0)) out.procs2NoStun++;
      if (g1 > g0 + 1e-9 && !P2.length) out.greyBad.push([+m.t.toFixed(3), "grey rose with no x2 proc", g0, g1, P1.length]);
      if (g1 > 0 && !(th.stun > 0)) out.greyNoStun++;
      if (started){ out.greyStarts++;
        const R0 = run.get(th); if (R0 && !R0.done) R0.cut = true;
        run.set(th, { g: 0, s: 0, cut: false, done: false, stun0: th.stun, prev: th.stun, raised: false }); }
      const R = run.get(th);
      if (R && !R.done && !started){ if (th.stun > R.prev + 1e-12) R.raised = true; R.prev = th.stun; }
      if (R && !R.done){
        if (!frozen || started){ if (g1 > 0) R.g++; if (th.stun > 0) R.s++; }
        if (!(g1 > 0) && !(th.stun > 0)){ R.done = true;
          if (!R.cut && !R.raised && R.stun0 <= 0.4){ out.greyLen[R.g] = (out.greyLen[R.g] || 0) + 1; out.stunLen[R.s] = (out.stunLen[R.s] || 0) + 1;
            if (R.g !== R.s) out.lenBad.push([+m.t.toFixed(3), R.g, R.s]); }
          else out.runsOther = (out.runsOther || 0) + 1; }
        else if (!(g1 > 0) && th.stun > 0 && !R.gEnd){ R.gEnd = true; }
      }
    }
    if (m.over && over < 0){ over = step; out.hashAtOver = [h1 >>> 0, h2 >>> 0]; out.stepsAtOver = step;
      out.res = Object.assign(m.summary(), { t: m.t, hpA: m.a.hp, hpB: m.b.hp });
      if (me) out.fadeAtOver = [me.unmkFade, me.alive, !!me.ultUnmake]; }
    if (draw){
      const vis = me && (me.unmkFade > 0 || (me.unmkMotes && me.unmkMotes.length) || (th && th.unmkGrey > 0));
      if (step % 24 === 0 || (vis && step % 3 === 0) || (over >= 0 && step % 6 === 0)){
        try { AC.POSTFX.on = (step % 2 === 0); AC.__draw(m); out.draws++;
              if (vis){ out.picFrames++; if (m.hitStop > 0) out.stopPicFrames++; } }
        catch (e){ out.thrown = String(e.stack || e); break; }
      }
      if (me && over >= 0 && out.fadeZeroAfterOver === null && !(me.unmkFade > 0))
        out.fadeZeroAfterOver = +((step - over) * DT).toFixed(4);
    }
    if (over >= 0 && step - over > (draw ? 3 : 0) / DT) break;
  }
  out.steps = step; out.hash = [h1 >>> 0, h2 >>> 0];
  out.wWritten = W0 ? JSON.stringify(W0) !== w0 : false;
  for (const k of ["greyBad", "tagBad", "tagOther", "fadeBad", "lenBad"]) out[k] = out[k].slice(0, 6);
  return out;
}"""


def make_control():
    s = (HERE / "sb-final-fx.html").read_text(encoding="utf-8")
    old = "          g.val = val; g.unmk = true; k--;\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "          f.vx += 1e-9;                          // CONTROL: a sim write\n")
    (HERE / "sb-control.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    import os
    ONLY = os.environ.get("VERIFY_ONLY", "")
    make_control()
    runs = {}
    for label, path, draw in (("base", BASE, False), ("final", HERE / "sb-final.html", False),
                              ("final-fx", HERE / "sb-final-fx.html", False),
                              ("final-fx drawn", HERE / "sb-final-fx.html", True),
                              ("CONTROL (must differ)", HERE / "sb-control.html", False)):
        if ONLY == "drawn" and not draw: continue
        with game(game_path=path) as (page, errors):
            for a, b, s in PAIRS:
                r = page.evaluate(TRACE, [a, b, s, draw])
                assert not errors, errors[:3]
                runs.setdefault((a, b, s), {})[label] = r
                if draw:
                    print(f"  [{label}] {a} v {b} {s}: draws {r['draws']} thrown {r['thrown']} windows {r['windows']} | "
                          f"procs x2 {r['procs2']} (stun zeroed at once {r['procs2NoStun']}) x1 {r['procs1']} grey starts {r['greyStarts']} bad {r['greyBad']} grey-without-stun {r['greyNoStun']} "
                          f"grey len {r['greyLen']} stun len {r['stunLen']} len-mismatch {r['lenBad']} (runs cut/raised/long {r['runsOther']}) | extra {r['extra']} +2 tags {r['plus2']} "
                          f"bad {r['tagBad']} other {r['tagOther']} | fade bad {r['fadeBad']} motes out of window {r['moteBad']} | "
                          f"life at cast {sorted(set(r['lifeAtCast']))} banner her/foe {r['bannerOnHer']}/{r['bannerOnFoe']} | "
                          f"pic frames {r['picFrames']} (stop {r['stopPicFrames']}) close->0 {r['closes']} death->0 {r['deaths']} "
                          f"| at kill {r['fadeAtOver']} -> 0 after {r['fadeZeroAfterOver']} s | w written {r['wWritten']}", flush=True)
    if ONLY == "drawn":
        (HERE / "verify_drawn.json").write_text(json.dumps({str(k): v for k, v in runs.items()}, indent=1, default=str)); raise SystemExit(0)
    ok = True; ctrl_ok = True
    for k, v in runs.items():
        base = v["base"]
        for lab in ("final", "final-fx", "final-fx drawn", "CONTROL (must differ)"):
            o = v[lab]
            same = (o["res"] == base["res"]) and o["hashAtOver"] == base["hashAtOver"] and o["stepsAtOver"] == base["stepsAtOver"]
            if lab.startswith("CONTROL"):
                has = "spellbreaker" in (k[0], k[1])
                tagged = v["final-fx drawn"]["plus2"] > 0
                good = (not same) if (has and tagged) else same if not has else True
                ctrl_ok &= good
                print(f"{k}: {lab:22s} {'DIFFERS' if not same else 'IDENTICAL'}  +2 tags {v['final-fx drawn']['plus2']} (control {'bit' if good else 'DID NOT BITE'})")
                continue
            ok &= same
            print(f"{k}: {lab:15s} {'IDENTICAL' if same else 'DIFFERS'}  steps@kill {o['stepsAtOver']} hash@kill {o['hashAtOver']} "
                  f"winner {o['res']['winner']} t {o['res']['t']!r} windows {o['windows']}")
    print("SIM IDENTITY:", "PASS" if ok else "FAIL", "| CONTROL:", "BIT ON EVERY SPELLBREAKER FIGHT WITH A +2 TAG" if ctrl_ok else "DID NOT BITE")
    (HERE / "verify.json").write_text(json.dumps({str(k): v for k, v in runs.items()}, indent=1, default=str))
