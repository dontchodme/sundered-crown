#!/usr/bin/env python
"""ZENITH'S PROBE -- one check per sentence of v71 §5 / the brief's §0, read INSIDE the hook.

    python morningstar_probe.py --game ../02-chain/sc-zenith.html

Wraps `tickSun` on the Match prototype and reads each event where it happens.
Runs Morningstar against every other relic, both sides, and prints N/N. The
checks follow the link's own numbers, so the same probe gates stages 2-4
(tickDmg 0 / 3, bless 0 / 1).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] a tick on a foe whose centre was NOT within r + R of the flail head
  [2] two ticks closer than `tick`, or a lit frame with the cooldown clear that
      did not tick (the lab's cadence)
  [3] a tick that did not hand `hurt` exactly tickDmg once, and add smite
      `smite` (to its cap)
  [4] a tick that moved the foe or froze the world (a ward's own shatter aside)
  [5] a blessing not applied on a tick (when bless > 0), or applied when 0;
      blessing applications != ticks
  [6] a beat from a tick that did not kill, or a killing tick without its own
      fatal beat
  [7] a window that is not `dur` long on the window clock
  [8] smite or blessing applied with a source that is not "a" / "b"
  [9] any relic but Morningstar carrying `ultSun`
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=98001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickSun;
  const lastTick = new WeakMap();
  P.tickSun = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultSun && f.w.id !== "morningstar") fail(9, `${f.w.id} carries ultSun`);
      const Z = f.ultSun;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t1: Z.t + dt, cd1: Z.cd - dt, x: foe.x, y: foe.y, vx: foe.vx, vy: foe.vy,
                 hx: f.headX, hy: f.headY, smite: foe.stacks("smite"), bless: f.stacks("blessing"),
                 fhp: foe.hp, alive: foe.alive, fAlive: f.alive, ticks: f.sunTally.ticks, blessN: f.sunTally.bless });
    }
    const hs0 = this.hitStop, hurts = [], beats = [], oHurt = this.hurt, oBeat = this.beat;
    let shattered = 0;
    this.hurt = function(tgt, dmg, src){ const s0 = tgt.shield; hurts.push([tgt, dmg]);
      const r = oHurt.call(this, tgt, dmg, src); if (s0 > 0 && tgt.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    const r = oTick.call(this, dt);
    delete this.hurt; delete this.beat;
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult;
      if (p.t1 >= Z.dur || !p.fAlive){
        if (f.ultSun) fail(7, "window did not close at dur");
        else inc("closeOk");
        continue;
      }
      const d = Math.hypot(p.x - p.hx, p.y - p.hy), lit = p.alive && d < u.r + R;
      const ticked = f.sunTally.ticks - p.ticks;
      if (ticked > 1) fail(2, `${ticked} ticks in one frame`);
      if (ticked){
        inc("ticks");
        if (!lit) fail(1, `ticked at ${d.toFixed(1)} from the head (r+R ${u.r + R})`); else inc("litOk");
        const lt = lastTick.get(f);
        if (lt && lt.Z === Z && p.t1 - lt.t < u.tick - 1e-9) fail(2, `ticks ${(p.t1 - lt.t).toFixed(3)}s apart`);
        lastTick.set(f, { Z, t: p.t1 });
        if (p.cd1 > 1e-9) fail(2, `ticked with the cooldown at ${p.cd1}`);
        const hs = hurts.filter(h => h[0] === foe);
        if (hs.length !== 1 || hs[0][1] !== u.tickDmg) fail(3, `hurt calls ${JSON.stringify(hs.map(h => h[1]))}, want [${u.tickDmg}]`); else inc("dmgOk");
        if (foe.stacks("smite") < Math.min(p.smite + u.smite, 4)) fail(3, `smite ${p.smite} -> ${foe.stacks("smite")}`);
        const ssrc = foe.status.smite ? foe.status.smite.src : undefined, side = f === this.a ? "a" : "b";
        if (ssrc !== side) fail(8, `smite src ${typeof ssrc === "object" ? "a Fighter" : JSON.stringify(ssrc)}`); else inc("srcOk");
        const dB = f.sunTally.bless - p.blessN;
        if (u.bless > 0){
          if (dB !== u.bless) fail(5, `blessing +${dB} on a tick, want ${u.bless}`);
          else if (f.stacks("blessing") < Math.min(p.bless + u.bless, 5)) fail(5, "blessing stacks did not rise");
          else { inc("blessOk"); const bs = f.status.blessing ? f.status.blessing.src : undefined;
                 if (bs !== side) fail(8, `blessing src ${typeof bs === "object" ? "a Fighter" : JSON.stringify(bs)}`); }
        } else if (dB !== 0 || f.stacks("blessing") > p.bless) fail(5, "blessed with bless 0");
        if (foe.x !== p.x || foe.y !== p.y || foe.vx !== p.vx || foe.vy !== p.vy) fail(4, "a tick moved the foe");
        if (!shattered && this.hitStop !== hs0) fail(4, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
        if (shattered) inc("wardBreaks", shattered);
        const killed = p.fhp > 0 && foe.hp <= 0, fb = beats.filter(b => b.fatal && b.sun);
        if (killed){ if (fb.length !== 1) fail(6, `killing tick filed ${fb.length} fatal beats`); else inc("fatalBeat"); }
        else if (beats.length) fail(6, `a non-killing tick filed ${beats.length} beat(s)`);
      } else {
        if (lit && p.cd1 <= 1e-9) fail(2, "lit with the cooldown clear, and no tick");
        if (beats.length) fail(6, "a frame with no tick filed a beat");
      }
      inc("frames"); if (lit) inc("litFrames");
    }
    return r;
  };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "morningstar");
  const T = { casts: 0, ticks: 0, dealt: 0, bless: 0, litFrames: 0, frames: 0 };
  let fights = 0, wins = 0, decided = 0, healed = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "morningstar", sd) : new AC.Match("morningstar", fid, sd);
    const me = side ? m.b : m.a;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.sunTally) for (const k in T) T[k] += me.sunTally[k];
  }
  P.tickSun = oTick;
  const u = AC.WEAPONS.find(w => w.id === "morningstar").ult;
  return { n, bad, T, fights, win: wins / decided, u: { charge: u.charge, tickDmg: u.tickDmg, bless: u.bless, r: u.r, tick: u.tick } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickSun === 'function'"):
        raise SystemExit("no tickSun in this build -- not a Zenith link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
print(f"\nZENITH PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Morningstar both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  per cast: ticks {T['ticks']/casts:.2f}  dmg {T['dealt']/casts:.2f}  bless {T['bless']/casts:.2f}  "
      f"foe lit {100*T['litFrames']/max(1,T['frames']):.1f}% of the window   casts/fight {T['casts']/R['fights']:.2f}   "
      f"Morningstar win {R['win']:.1%}")
print(f"  killing ticks {n.get('fatalBeat',0)}   wards broken by a tick {n.get('wardBreaks',0)}")
checks = [
    (1, "every tick lands on a foe within r + R of the flail head", n.get("litOk", 0) > 0),
    (2, "the lab's cadence: never closer than `tick`, never a missed clear lit frame", n.get("ticks", 0) > 0),
    (3, "each tick: hurt(foe, tickDmg) once, smite +smite (to its cap)", n.get("dmgOk", 0) > 0),
    (4, "nothing else: no move, no stop but a ward's own", n.get("ticks", 0) > 0),
    (5, "blessing +bless on every tick (none at bless 0)", (n.get("blessOk", 0) > 0) if U["bless"] else n.get("ticks", 0) > 0),
    (6, "no beat, except the killing tick's own fatal beat", (n.get("fatalBeat", 0) > 0) if U["tickDmg"] else n.get("ticks", 0) > 0),
    (7, "the window is `dur` long on the window clock", n.get("closeOk", 0) > 0),
    (8, "smite's (and blessing's) source is a side letter", n.get("srcOk", 0) > 0),
    (9, "only Morningstar carries ultSun", True),
]
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
