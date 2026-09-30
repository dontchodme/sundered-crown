"""[1] SIM IDENTITY: every step of every fight hashed (positions, velocities, angles, hp, shield, statuses, charge,
stun, pin, pinV, pinMax, pinFree, hitCd, reachMul, the window {t, dur}, its tally, the beats' count, the shades),
the BASE against the rows, undrawn AND drawn, on two pairs: the stamp's (links/sc-heartwood-b11.html against
hw-final.html = b11 + the rows = THE STAMP, and hw-final-fx.html) and the tip's (carry/hw-on-sc-tendril-fx.html
against hw-tip.html and hw-tip-fx.html, the look as it ships). [2] WHOLE FIGHTS DRAWN on hw-tip-fx through the kill
and 3s of verdict, the post chain alternating on/off: nothing may throw; every root on a live foe marks the held
ball for Tendril's root (twineHeld 1, twineRootFade 1; a new hold's shoots from the floor, heldAge 0) and the blow's
own ENTANGLE tag carries the count the root leaves (or is the first-ever panel); every Heartwood-held ball carries
twineHeld exactly while pinned (so `_drawField` leaves the hexagon off); the green stands exactly while the window
does; the wither timed (clock close, the caster's death, the kill); motes capped; the shared weapon row never
written. [3] THE CONTROL: hw-control.html is hw-final plus ONE sim write in tickGrove's root branch (the foe's vx
nudged by 1e-9) -- it must DIFFER on every Heartwood fight with a root, and match the fights without Heartwood."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-heartwood-b11.html").resolve()
TIP0 = HERE / "carry" / "hw-on-sc-tendril-fx.html"
PAIRS = [("heartwood", "spellbreaker", 2207), ("dawnbringer", "heartwood", 99001), ("heartwood", "gravemourn", 99015),
         ("twinshade", "heartwood", 99008), ("heartwood", "grudgebearer", 31337), ("lastlight", "heartwood", 4242),
         ("heartwood", "bindweed", 2317), ("paradox", "heartwood", 1234), ("heartwood", "thornwake", 777),
         ("heartwood", "widowmaker", 99001), ("ironwood", "heartwood", 5150), ("axiom", "grudgebearer", 31337),
         ("morningstar", "lastlight", 4242)]

TRACE = r"""([a, b, seed, draw]) => {
  window.__frozen = true;
  AC.setResolution(270, 480);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const DT = AC.CONFIG.physics.dt, RB = AC.CONFIG.physics.ballR;
  const W0 = AC.WEAPONS.find(w => w.id === "heartwood");
  const w0 = JSON.stringify(W0);
  const m = new AC.Match(a, b, seed);
  const buf = new DataView(new ArrayBuffer(8));
  let h1 = 0x811c9dc5 | 0, h2 = 0x1234567 | 0;
  const mix = (v) => { buf.setFloat64(0, +v || 0);
    for (let i = 0; i < 8; i++){ const x = buf.getUint8(i);
      h1 = Math.imul(h1 ^ x, 16777619); h2 = Math.imul(h2 ^ (x + i), 2246822519); } };
  const fstate = (f) => { mix(f.x); mix(f.y); mix(f.vx); mix(f.vy); mix(f.hp); mix(f.shield); mix(f.shieldMax);
    mix(f.theta); mix(f.charge); mix(f.stun || 0); mix(f.alive ? 1 : 0); mix(f.pin || 0); mix(f.pinFree || 0);
    mix(f.pinMax || 0); if (f.pinV){ mix(f.pinV[0]); mix(f.pinV[1]); } else mix(-3);
    mix(f.reachMul); for (const c of f.hitCd) mix(c || 0); mix(f.tips.length); mix(f.clanks); mix(f.hits); mix(f.dealt);
    mix(f.headX || 0); mix(f.headY || 0); mix(f.spinDir || 0); mix(f.ultsFired || 0);
    for (const k of Object.keys(f.status).sort()){ const s = f.status[k]; mix(k.length); mix(s.stacks || 0); mix(s.t || 0); }
    const Z = f.ultRoot; if (Z){ mix(Z.t); mix(Z.dur); } else mix(-1);
    const T = f.rootTally; if (T){ for (const k of ["casts", "frames", "blows", "rooted", "roots", "ent"]) mix(T[k]); } else mix(-2); };
  const out = { draws: 0, thrown: null, pictureFrames: 0, stopFrames: 0, windows: 0, res: null,
                rootEv: 0, holdEv: 0, marked: 0, markBad: [], newAge0: 0, selfOK: 0, selfBad: [], letGo: 0, tagOK: 0, tagFirst: 0, tagNone: 0, tagBad: [],
                heldPinned: 0, heldBad: [], clearedBad: 0, greenBad: [], closes: [], deaths: [], fadeAtOver: null,
                fadeZeroAfterOver: null, maxMotes: 0, nanBad: 0, wWritten: false };
  const mes = [m.a, m.b].filter(f => f.w.id === "heartwood");
  const HAS = typeof m.tickGrove === "function", TW = typeof m.tickTwine === "function";
  let step = 0, over = -1;
  const prev = new Map(), closeStep = new Map(), seen = new Map(mes.map(f => [f, [0, 0]]));
  const byMe = new Set();          // balls a Heartwood root holds right now
  while (step < 200 / DT){
    m.step(DT); step++;
    fstate(m.a); fstate(m.b); mix(m.t); mix(m.hitStop); mix(m.inset); mix(m.beats.length); mix(m.shots.length);
    for (const s of m.shades){ mix(s.x); mix(s.y); mix(s.hp); }
    for (const me of mes){
      const th = me === m.a ? m.b : m.a, T = me.rootTally, Z = me.ultRoot;
      if (Z && !prev.get(me)) out.windows++;
      if (!Z && prev.get(me) && !m.over) closeStep.set(me, [step, me.alive]);
      prev.set(me, Z);
      if (!T) continue;
      const [sr, sn] = seen.get(me);
      if (T.rooted !== sn){
        const hold = T.roots !== sr;
        out.rootEv++; if (hold) out.holdEv++;
        seen.set(me, [T.roots, T.rooted]);
        if (draw && HAS && th.alive && th.pin > 0 && th.pinFree){
          /* a ball that holds itself (Canopy): its own picture's -- nothing marked */
          if (th.twineHeld > 0) out.selfBad.push([+m.t.toFixed(3), th.pin]); else out.selfOK++;
        }
        if (draw && HAS && th.alive && th.pin > 0){
          if (!th.pinFree){
            byMe.add(th);
            if (th.twineHeld === 1 && th.twineRootFade === 1) out.marked++;
            else out.markBad.push([+m.t.toFixed(3), th.twineHeld, th.twineRootFade]);
            if (hold && th.twineHeldAge <= DT * 2 + 1e-9) out.newAge0++;
          }
          const n = th.stacks("entangle");
          const near = m.tags.filter(g => g.key === "entangle" && g.max - g.life <= 0.1 && Math.hypot(g.x - th.x, g.y - th.y) < RB * 3);
          const g = near[near.length - 1];
          if (!g) out.tagNone++;
          else if (g.first) out.tagFirst++;
          else if (g.val === n) out.tagOK++;
          else out.tagBad.push([+m.t.toFixed(3), n, g.val]);
        }
      }
      if (draw && HAS){
        const live = !!(Z && !m.over && me.alive);
        if (live !== (me.groveFade === 1) && !(!live && me.groveFade > 0 && me.groveFade < 1))
          out.greenBad.push([+m.t.toFixed(3), live, me.groveFade]);
        const cs = closeStep.get(me);
        if (cs && !(me.groveFade > 0)){ (cs[1] ? out.closes : out.deaths).push(+((step - cs[0]) * DT).toFixed(4)); closeStep.delete(me); }
        out.maxMotes = Math.max(out.maxMotes, me.groveMotes.length);
        for (const q of me.groveMotes) if (!isFinite(q.x) || !isFinite(q.y)) out.nanBad++;
        for (const q of me.groveBits) if (!isFinite(q.x) || !isFinite(q.y)) out.nanBad++;
      }
    }
    if (draw && HAS && TW){
      for (const q of Array.from(byMe)){
        if (q.pin > 0 && q.alive && !q.pinFree){ if (q.twineHeld > 0) out.heldPinned++; else out.heldBad.push([+m.t.toFixed(3), q.pin]); }
        else { if (q.twineHeld && !m.over) out.clearedBad++; if (q.pinFree && q.pin > 0) out.letGo++; byMe.delete(q); }
      }
    }
    if (m.over && over < 0){ over = step; out.hashAtOver = [h1 >>> 0, h2 >>> 0]; out.stepsAtOver = step;
      out.res = Object.assign(m.summary(), { t: m.t, hpA: m.a.hp, hpB: m.b.hp });
      if (mes.length && HAS) out.fadeAtOver = mes.map(f => [f.groveFade, f.alive, !!f.ultRoot]); }
    if (draw){
      const vis = mes.some(f => f.groveFade > 0 || f.groveMotes.length || f.groveBits.length) || [m.a, m.b].some(f => f.twineRootFade > 0);
      if (step % 24 === 0 || (vis && step % 3 === 0) || (over >= 0 && step % 6 === 0)){
        try { AC.POSTFX.on = (step % 2 === 0); AC.__draw(m); out.draws++;
              if (vis){ out.pictureFrames++; if (m.hitStop > 0) out.stopFrames++; } }
        catch (e){ out.thrown = String(e.stack || e); break; }
      }
      if (mes.length && HAS && over >= 0 && out.fadeZeroAfterOver === null && mes.every(f => !(f.groveFade > 0)))
        out.fadeZeroAfterOver = +((step - over) * DT).toFixed(4);
    }
    if (over >= 0 && step - over > (draw ? 3 : 0) / DT) break;
  }
  out.steps = step; out.hash = [h1 >>> 0, h2 >>> 0];
  out.wWritten = JSON.stringify(W0) !== w0;
  for (const k of ["markBad", "tagBad", "heldBad", "greenBad", "selfBad"]) { out[k + "N"] = out[k].length; out[k] = out[k].slice(0, 4); }
  return out;
}"""


def make_control():
    s = (HERE / "hw-final.html").read_text(encoding="utf-8")
    old = "            foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldOut = 0;\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "            foe.vx += 1e-9;                   // CONTROL: a sim write\n")
    (HERE / "hw-control.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    if "stamp" in (sys.argv[1:] or ["stamp"]): make_control()
    runs = {}
    groups = [("stamp", BASE, [("final", HERE / "hw-final.html", False), ("final-fx", HERE / "hw-final-fx.html", False),
                               ("final drawn", HERE / "hw-final.html", True), ("CONTROL (must differ)", HERE / "hw-control.html", False)]),
              ("tip", TIP0, [("tip", HERE / "hw-tip.html", False), ("tip-fx", HERE / "hw-tip-fx.html", False),
                             ("tip-fx drawn", HERE / "hw-tip-fx.html", True)])]
    want = sys.argv[1:] or ["stamp", "tip"]
    groups = [g for g in groups if g[0] in want]
    ok = True; ctrl_ok = True
    for gname, base, arms in groups:
        for label, path, draw in [("base", base, False)] + arms:
            with game(game_path=path) as (page, errors):
                for a, b, s in PAIRS:
                    r = page.evaluate(TRACE, [a, b, s, draw])
                    assert not errors, errors[:3]
                    runs.setdefault((gname, a, b, s), {})[label] = r
                    if draw:
                        print(f"  [{gname}/{label}] {a} v {b} {s}: draws {r['draws']} thrown {r['thrown']} windows {r['windows']} "
                              f"roots {r['rootEv']} (holds {r['holdEv']}) marked {r['marked']} bad {r['markBadN']} {r['markBad']} newAge0 {r['newAge0']} "
                              f"| tag ok {r['tagOK']} first {r['tagFirst']} none {r['tagNone']} bad {r['tagBadN']} {r['tagBad']} "
                              f"| held&pinned {r['heldPinned']} bad {r['heldBadN']} cleared-bad {r['clearedBad']} "
                              f"| self-held: unmarked {r['selfOK']} bad {r['selfBadN']} let go {r['letGo']} "
                              f"| green bad {r['greenBadN']} {r['greenBad']} | close->0 {r['closes']} death->0 {r['deaths']} "
                              f"| at kill {r['fadeAtOver']} -> 0 after {r['fadeZeroAfterOver']}s | motes max {r['maxMotes']} nan {r['nanBad']} "
                              f"| pic frames {r['pictureFrames']} (stop {r['stopFrames']}) | w written {r['wWritten']}", flush=True)
        for k, v in runs.items():
            if k[0] != gname: continue
            b0 = v["base"]
            for label, _, _ in arms:
                o = v[label]
                same = (o["res"] == b0["res"]) and o["hashAtOver"] == b0["hashAtOver"] and o["stepsAtOver"] == b0["stepsAtOver"]
                if label.startswith("CONTROL"):
                    has = "heartwood" in (k[1], k[2])
                    good = (not same) if (has and b0["rootEv"] > 0) else (same if not has else True)
                    ctrl_ok &= good
                    print(f"{k}: {label:22s} {'DIFFERS' if not same else 'IDENTICAL'}  roots {b0['rootEv']} (control {'bit' if good else 'DID NOT BITE'})")
                    continue
                ok &= same
                print(f"{k}: {label:14s} {'IDENTICAL' if same else 'DIFFERS'}  steps@kill {o['stepsAtOver']} hash@kill {o['hashAtOver']} "
                      f"winner {o['res']['winner']} t {o['res']['t']!r} roots {o['rootEv']}", flush=True)
    print("SIM IDENTITY:", "PASS" if ok else "FAIL", "| CONTROL:", "BIT ON EVERY HEARTWOOD FIGHT WITH A ROOT" if ctrl_ok else "DID NOT BITE")
    (HERE / ("verify_" + "_".join(want) + ".json")).write_text(json.dumps({str(k): v for k, v in runs.items()}, indent=1, default=str))
