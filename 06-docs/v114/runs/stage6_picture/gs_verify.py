"""[1] SIM IDENTITY: every step of every fight hashed (positions, velocities, angles, hp, shield, statuses, charge,
hitCd, pin, the flail head, the price's window {t, dur}, its tally, every shot, the shades, the beats' and shots'
counts, the rng's own state), the BASE link (links/sc-goreshard-b10.25.html) against gs-final.html (the rows
applied: THE STAMP) and gs-final-fx.html (the same + SPECS.oathwound out), undrawn AND drawn.
[2] WHOLE FIGHTS DRAWN on gs-final-fx through the kill and 3s of verdict, the post chain alternating on/off:
nothing may throw; every cast starts the red's run on its step; the red is up exactly while the window is open
(ultPrice && !over && both alive) and drains after it (clock close, death, verdict); the glow sits at
0.2 + 0.15 x the foe's stacks once they have held 0.4s; every priced blow of hers files ONE float of exactly
clamp(22 + dmg x 0.62, 22, 62) x (crit ? 1.3 : 1) x (1 + 0.1 n) and every other blow's float is the old size;
no mote is shed with the window shut; the shared weapon row is never written; the picture's fields stay at rest
on the other relic. [3] THE CONTROL: gs-control.html is gs-final plus ONE sim write in tickGore's cast branch
(the foe's vx nudged by 1e-9) -- it must DIFFER on every Goreshard fight with a cast, and match the fights
without Goreshard. Resumable: verify_parts/<arm>.json keyed by the page's sha."""
import sys, json, pathlib, hashlib, os, time
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-goreshard-b10.25.html").resolve()
PAIRS = [("oathwound", "spellbreaker", 99015), ("dawnbringer", "oathwound", 99001), ("oathwound", "gravemourn", 99015),
         ("twinshade", "oathwound", 99008), ("oathwound", "grudgebearer", 31337), ("aureole", "oathwound", 4101),
         ("oathwound", "marrowdraw", 2207), ("farwarden", "oathwound", 31337), ("oathwound", "gloamwire", 5150),
         ("thornwake", "oathwound", 2427), ("widowmaker", "oathwound", 2317), ("oathwound", "lastlight", 4242),
         ("axiom", "grudgebearer", 31337), ("morningstar", "lastlight", 4242)]

TRACE = r"""([a, b, seed, draw]) => {
  window.__frozen = true;
  AC.setResolution(270, 480);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const DT = AC.CONFIG.physics.dt, RB = AC.CONFIG.physics.ballR;
  const W0 = AC.WEAPONS.find(w => w.id === "oathwound");
  const w0 = JSON.stringify(W0);
  const m = new AC.Match(a, b, seed);
  const buf = new DataView(new ArrayBuffer(8));
  let h1 = 0x811c9dc5 | 0, h2 = 0x1234567 | 0;
  const mix = (v) => { buf.setFloat64(0, +v || 0);
    for (let i = 0; i < 8; i++){ const x = buf.getUint8(i);
      h1 = Math.imul(h1 ^ x, 16777619); h2 = Math.imul(h2 ^ (x + i), 2246822519); } };
  const fstate = (f) => { mix(f.x); mix(f.y); mix(f.vx); mix(f.vy); mix(f.hp); mix(f.shield); mix(f.shieldMax);
    mix(f.theta); mix(f.charge); mix(f.stun || 0); mix(f.alive ? 1 : 0); mix(f.pin || 0); mix(f.pinFree || 0);
    mix(f.reachMul); for (const c of f.hitCd) mix(c || 0); mix(f.tips.length); mix(f.clanks); mix(f.hits); mix(f.dealt);
    mix(f.headX || 0); mix(f.headY || 0); mix(f.headSpin || 0); mix(f.headAngVel || 0); mix(f.spinDir || 0);
    mix(f.fireCd || 0); mix(f.swingPhase || 0);
    for (const k of Object.keys(f.status).sort()){ const s = f.status[k]; mix(k.length); mix(s.stacks || 0); mix(s.t || 0); }
    const Z = f.ultPrice; if (Z){ mix(Z.t); mix(Z.dur); } else mix(-1);
    const T = f.priceTally; if (T){ for (const k of ["casts", "frames", "foeStk", "blows", "stk"]) mix(T[k]); } else mix(-2); };
  const out = { draws: 0, thrown: null, redFrames: 0, stopRedFrames: 0, windows: 0, res: null,
                casts: 0, runOK: 0, runBad: [], upShut: 0, downOpen: 0, drainAfter: [], deathDrain: [], overDrain: null,
                glowChk: 0, glowBad: [], pricedBlows: 0, floatOK: 0, floatBad: [], otherFloats: 0, otherBad: [],
                shedShut: 0, maxDrops: 0, wWritten: false, otherTouched: false, fadeAtOver: null };
  const mes = [m.a, m.b].filter(f => f.w.id === "oathwound");
  const others = [m.a, m.b].filter(f => f.w.id !== "oathwound");
  /* TRUTH, harness-side and read-only: each blow's float, and whether the price scaled it */
  const blows = [];
  if (draw){
    const rh = m.resolveHit;
    m.resolveHit = function(self, foe, ...rest){
      const F0 = new Set(this.floats), T = self.priceTally, s0 = T ? T.stk : 0, b0 = T ? T.blows : 0, hp0 = foe.hp;
      const r0 = rh.call(this, self, foe, ...rest);
      const T2 = self.priceTally, nf = this.floats.filter(x => !F0.has(x));
      const priced = !!(T2 && T2.blows > b0), n = priced ? T2.stk - s0 : 0;
      blows.push({ self, n, priced, nf });
      return r0;
    };
  }
  let step = 0, over = -1;
  const prevZ = new Map(), closeStep = new Map(), held = new Map();
  while (step < 200 / DT){
    const pre = mes.map(f => ({ casts: f.priceTally ? f.priceTally.casts : 0, dropN: f.goreDropN }));
    blows.length = 0;
    m.step(DT); step++;
    fstate(m.a); fstate(m.b); mix(m.t); mix(m.hitStop); mix(m.inset); mix(m.beats.length); mix(m.shots.length);
    for (const s of m.shots){ mix(s.x); mix(s.y); mix(s.vx); mix(s.vy); mix(s.stuck ? 1 : 0); }
    for (const s of m.shades){ mix(s.x); mix(s.y); mix(s.hp); }
    if (typeof m.rngState === "number") mix(m.rngState);
    mes.forEach((me, j) => {
      const th = me === m.a ? m.b : m.a, T = me.priceTally, Z = me.ultPrice;
      if (Z && !prevZ.get(me)) out.windows++;
      if (!Z && prevZ.get(me) && !m.over) closeStep.set(me, [step, me.alive && th.alive]);
      prevZ.set(me, Z);
      if (!draw) return;
      const open = !!Z && !m.over && me.alive && th.alive;
      if (T && T.casts > pre[j].casts){
        out.casts++;
        if (open && me.goreFade === 1 && me.goreOut === 0 && me.goreAge < 0.02) out.runOK++;
        else if (open) out.runBad.push([+m.t.toFixed(3), me.goreFade, me.goreOut, me.goreAge]);
      }
      if (me.goreFade === 1 && me.goreOut === 0 && !open) out.upShut++;
      if (open && !(me.goreFade === 1 && me.goreOut === 0)) out.downOpen++;
      if (!open && me.goreDropN > pre[j].dropN) out.shedShut++;
      out.maxDrops = Math.max(out.maxDrops, me.goreDrops.length);
      /* the glow, once the foe's stacks have held 0.4s of match time */
      if (open){
        const n = Math.min(4, th.stacks("hemorrhage")), h = held.get(me);
        if (!h || h[0] !== n) held.set(me, [n, m.t]);
        else if (m.t - h[1] > 0.4 && me.goreAge > 0.7){
          out.glowChk++;
          if (Math.abs(me.goreGlow - (0.2 + 0.15 * n)) > 0.01) out.glowBad.push([+m.t.toFixed(3), n, +me.goreGlow.toFixed(4)]);
        }
      } else held.delete(me);
      const cs = closeStep.get(me);
      if (cs && !(me.goreFade > 0)){ (cs[1] ? out.drainAfter : out.deathDrain).push(+((step - cs[0]) * DT).toFixed(4)); closeStep.delete(me); }
    });
    if (draw){
      for (const B of blows){
        const size = (x, n) => { const dmg = parseFloat(x.text), crit = x.text.endsWith("!");
          return Math.min(62, Math.max(22, 22 + dmg * 0.62)) * (crit ? 1.3 : 1) * (1 + 0.1 * n); };
        /* the blow's own float is resolveHit's damage line: its text is a STRING (dmg + "" or "!"); a vigil
           burst or return filed inside the same call carries a NUMBER (L14288, L14543), and is not this float */
        const dmgF = B.nf.filter(x => typeof x.text === "string" && /^[0-9]+!?$/.test(x.text));
        if (mes.indexOf(B.self) >= 0 && B.priced && B.n > 0){
          out.pricedBlows++;
          if (dmgF.length === 1 && Math.abs(dmgF[0].size - size(dmgF[0], B.n)) < 1e-9) out.floatOK++;
          else out.floatBad.push([+m.t.toFixed(3), B.n, dmgF.map(x => [x.text, x.size])]);
        } else {
          for (const x of dmgF){ out.otherFloats++; if (Math.abs(x.size - size(x, 0)) > 1e-9) out.otherBad.push([+m.t.toFixed(3), x.text, x.size]); }
        }
      }
    }
    for (const f of others) if (f.goreFade || f.goreAge || f.goreOut || (f.goreDrops && f.goreDrops.length) || f.goreSeen || f.goreDropN) out.otherTouched = true;
    if (m.over && over < 0){ over = step; out.hashAtOver = [h1 >>> 0, h2 >>> 0]; out.stepsAtOver = step;
      out.res = Object.assign(m.summary(), { t: m.t, hpA: m.a.hp, hpB: m.b.hp });
      if (mes.length) out.fadeAtOver = mes.map(f => [f.goreFade, f.alive, !!f.ultPrice]); }
    if (draw){
      const vis = mes.some(f => f.goreFade > 0 || f.goreDrops.length);
      if (step % 24 === 0 || (vis && step % 3 === 0) || (over >= 0 && step % 6 === 0)){
        try { AC.POSTFX.on = (step % 2 === 0); AC.__draw(m); out.draws++;
              if (vis){ out.redFrames++; if (m.hitStop > 0) out.stopRedFrames++; } }
        catch (e){ out.thrown = String(e.stack || e); break; }
      }
      if (mes.length && over >= 0 && out.overDrain === null && mes.every(f => !(f.goreFade > 0)))
        out.overDrain = +((step - over) * DT).toFixed(4);
    }
    if (over >= 0 && step - over > (draw ? 3 : 0) / DT) break;
  }
  out.steps = step; out.hash = [h1 >>> 0, h2 >>> 0];
  out.wWritten = JSON.stringify(W0) !== w0;
  for (const k of ["runBad", "glowBad", "floatBad", "otherBad"]) out[k] = out[k].slice(0, 5);
  return out;
}"""


def make_control():
    s = (HERE / "gs-final.html").read_text(encoding="utf-8")
    old = "        if (open){ f.goreAge = 0; f.goreOut = 0; f.goreGlow = 1; }   // a cast\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "        if (open) foe.vx += 1e-9;                    // CONTROL: a sim write\n")
    (HERE / "gs-control.html").write_text(s, encoding="utf-8")


def sha16(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]


if __name__ == "__main__":
    make_control()
    PARTS = HERE / "verify_parts"; PARTS.mkdir(exist_ok=True)
    only = os.environ.get("GV_ARMS")
    arms = [("base", BASE, False, PAIRS), ("final", HERE / "gs-final.html", False, PAIRS),
            ("final-fx", HERE / "gs-final-fx.html", False, PAIRS),
            ("final-fx drawn", HERE / "gs-final-fx.html", True, PAIRS),
            ("final drawn", HERE / "gs-final.html", True, PAIRS[:8]),
            ("CONTROL (must differ)", HERE / "gs-control.html", False, PAIRS)]
    runs = {}
    for label, path, draw, pairs in arms:
        pf = PARTS / (label.split(" (")[0].replace(" ", "_") + ".json")
        key = sha16(path)
        got = json.loads(pf.read_text()) if pf.exists() else {}
        if got.get("sha") != key: got = {"sha": key, "fights": {}}
        todo = [p for p in pairs if f"{p[0]}|{p[1]}|{p[2]}" not in got["fights"]]
        if todo and (not only or label in only.split(",")):
            with game(game_path=path) as (page, errors):
                for a, b, s in todo:
                    r = page.evaluate(TRACE, [a, b, s, draw])
                    assert not errors, errors[:3]
                    got["fights"][f"{a}|{b}|{s}"] = r
                    pf.write_text(json.dumps(got, default=str))
                    if draw:
                        print(f"  [{label}] {a} v {b} {s}: draws {r['draws']} thrown {r['thrown']} windows {r['windows']} casts {r['casts']} "
                              f"run ok {r['runOK']} bad {r['runBad']} | up-while-shut {r['upShut']} down-while-open {r['downOpen']} | "
                              f"glow checks {r['glowChk']} bad {r['glowBad']} | priced blows {r['pricedBlows']} float ok {r['floatOK']} "
                              f"bad {r['floatBad']} | other floats {r['otherFloats']} bad {r['otherBad']} | shed-while-shut {r['shedShut']} "
                              f"max drops {r['maxDrops']} | drain after close {r['drainAfter']} death {r['deathDrain']} | at kill "
                              f"{r['fadeAtOver']} -> 0 after {r['overDrain']} s | red frames {r['redFrames']} (stop {r['stopRedFrames']}) | "
                              f"w written {r['wWritten']} | other relic touched {r['otherTouched']}", flush=True)
                    time.sleep(0.3)
        for k, r in got["fights"].items():
            runs.setdefault(k, {})[label] = r
    ok = True; ctrl_ok = True
    for k, v in runs.items():
        base = v.get("base")
        if not base: continue
        for lab in ("final", "final-fx", "final-fx drawn", "final drawn", "CONTROL (must differ)"):
            if lab not in v: continue
            o = v[lab]
            same = (o["res"] == base["res"]) and o["hashAtOver"] == base["hashAtOver"] and o["stepsAtOver"] == base["stepsAtOver"]
            if lab.startswith("CONTROL"):
                has = "oathwound" in k.split("|")[:2]
                casts = v.get("final-fx drawn", {}).get("casts", None)
                good = (not same) if (has and (casts or 0) > 0) else same if not has else True
                ctrl_ok &= good
                print(f"{k}: {lab:22s} {'DIFFERS' if not same else 'IDENTICAL'}  casts {casts} (control {'bit' if good else 'DID NOT BITE'})")
                continue
            ok &= same
            print(f"{k}: {lab:14s} {'IDENTICAL' if same else 'DIFFERS'}  steps@kill {o['stepsAtOver']} hash@kill {o['hashAtOver']} "
                  f"winner {o['res']['winner']} t {o['res']['t']!r}")
    print("SIM IDENTITY:", "PASS" if ok else "FAIL", "| CONTROL:", "BIT ON EVERY GORESHARD FIGHT WITH A CAST" if ctrl_ok else "DID NOT BITE")
    (HERE / "verify.json").write_text(json.dumps(runs, indent=1, default=str))
