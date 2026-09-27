#!/usr/bin/env python
"""ONSLAUGHT'S PROBE -- one check per sentence of v72 §1 / §6 and the brief's §0-§1,
read INSIDE the hook.

    python portcullis_probe.py --game ../02-chain/sc-onslaught.html

Wraps `tickRam` on the Match prototype and reads each event where it happens.
Runs Portcullis against every other relic, both sides, and prints N/N. The
checks follow the link's own numbers, so the same probe gates stages 2-3
(bank 0 / 8).

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] a window frame whose charge is not exactly v + unit(foe) x accel x dt,
      clamped at speedMax -- or any charge on a pinned caster
  [2] a slam with the centres at or beyond 2R + pad, two slams closer than
      `cd` on the window clock, or a frame in range with the cooldown clear
      and no slam
  [3] a slam that did not hand `hurt` exactly share x (shield before), once
      (none at zero shield), with the caster as its source
  [4] a slam whose knock is not `knock` along caster -> foe (a live, unpinned
      foe), or a frame that moved the foe's position
  [5] a bank that is not min(cap, shield + bank) with shieldMax and the ward's
      clock restarted, or banks != slams (bank > 0); any shield change at bank 0
  [6] a slam without exactly one hit beat marked `ram` (fatal iff it killed),
      or a beat on a frame with no slam
  [7] a hit stop that is not a ward's own shatter
  [8] a window that is not `dur` long on the window clock
  [9] any relic but Portcullis carrying `ultRam`
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=100001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const VMAX = C.physics.speedMax, W = AC.STATUS.ward;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickRam;
  const lastSlam = new WeakMap();
  P.tickRam = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultRam && f.w.id !== "portcullis") fail(9, `${f.w.id} carries ultRam`);
      const Z = f.ultRam;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z, t1: Z.t + dt, cd1: Z.cd - dt, vx: f.vx, vy: f.vy, x: f.x, y: f.y, pin: f.pin,
                 sh: f.shield, shMax: f.shieldMax, fx: foe.x, fy: foe.y, fvx: foe.vx, fvy: foe.vy,
                 fAlive: f.alive, foeAlive: foe.alive, fhp: foe.hp, slams: f.ramTally.slams, banks: f.ramTally.banks });
    }
    const hs0 = this.hitStop, hurts = [], beats = [], oHurt = this.hurt, oBeat = this.beat;
    let shattered = 0;
    this.hurt = function(tgt, dmg, src){ const s0 = tgt.shield; hurts.push([tgt, dmg, src]);
      const r = oHurt.call(this, tgt, dmg, src); if (s0 > 0 && tgt.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; }
    for (const p of pre){
      const { f, foe, Z } = p, u = f.w.ult;
      if (p.t1 >= Z.dur || !p.fAlive){
        if (f.ultRam) fail(8, "window did not close at dur");
        else if (p.fAlive && p.t1 < Z.dur - 1e-9) fail(8, "closed early");
        else inc("closeOk");
        continue;
      }
      inc("frames");
      if (!p.foeAlive){ if (hurts.length || beats.length) fail(2, "a slam on a dead foe"); continue; }
      const slammed = f.ramTally.slams - p.slams;
      const dx = p.fx - p.x, dy = p.fy - p.y, d = Math.hypot(dx, dy) || 1;
      /* [1] THE CHARGE -- rebuilt from the frame's own inputs; a shatter
         knocks the caster (the ward's rule), so those frames are left out */
      if (!shattered){
        let wx = p.vx, wy = p.vy;
        if (p.pin <= 0){
          wx += dx / d * u.accel * dt; wy += dy / d * u.accel * dt;
          const v = Math.hypot(wx, wy); if (v > VMAX){ wx *= VMAX / v; wy *= VMAX / v; }
        }
        if (f.vx !== wx || f.vy !== wy) fail(1, `v ${f.vx},${f.vy} want ${wx},${wy} (pin ${p.pin})`);
        else inc(p.pin > 0 ? "pinnedOk" : "chargeOk");
      } else inc("shatterFrames");
      /* [2] THE CONTACT AND THE CADENCE */
      if (slammed > 1) fail(2, `${slammed} slams in one frame`);
      const inRange = d < 2 * R + u.pad;
      if (slammed){
        inc("slams");
        if (!inRange) fail(2, `slam at d ${d.toFixed(2)} (2R + pad ${2 * R + u.pad})`);
        if (p.cd1 > 1e-9) fail(2, `slam with the cooldown at ${p.cd1}`);
        const ls = lastSlam.get(Z);
        if (ls !== undefined && p.t1 - ls < u.cd - 1e-9) fail(2, `slams ${(p.t1 - ls).toFixed(3)}s apart`);
        lastSlam.set(Z, p.t1);
        inc("rangeOk");
        /* [3] THE DAMAGE */
        const want = u.share * p.sh, hs = hurts.filter(h => h[0] === foe);
        if (want > 0){
          if (hs.length !== 1 || hs[0][1] !== want || hs[0][2] !== f) fail(3, `hurt ${JSON.stringify(hs.map(h => h[1]))}, want [${want}] from the caster`);
          else inc("dmgOk");
        } else if (hs.length) fail(3, `hurt at zero shield: ${JSON.stringify(hs.map(h => h[1]))}`);
        else inc("zeroSlam");
        if (hurts.length !== hs.length) fail(3, "hurt on something that is not the foe");
        /* [4] THE KNOCK */
        const kx = dx / d * u.knock, ky = dy / d * u.knock;
        if (foe.alive && !(foe.pin > 0)){
          if (Math.abs(foe.vx - (p.fvx + kx)) > 1e-9 || Math.abs(foe.vy - (p.fvy + ky)) > 1e-9) {
            if (!shattered) fail(4, `foe v ${foe.vx},${foe.vy} want ${p.fvx + kx},${p.fvy + ky}`);
          } else inc("knockOk");
        }
        /* [5] THE BANK */
        const dB = f.ramTally.banks - p.banks;
        if (u.bank > 0){
          const wantSh = Math.min(W.cap, p.sh + u.bank);
          if (dB !== 1) fail(5, `${dB} banks on a slam`);
          else if (!shattered && f.shield !== wantSh) fail(5, `shield ${p.sh} -> ${f.shield}, want ${wantSh}`);
          else if (f.shieldMax < f.shield) fail(5, "shieldMax under the shield");
          else if (!f.status.ward || f.status.ward.t !== W.dur) fail(5, "the ward's clock was not restarted");
          else inc("bankOk");
        } else if (dB !== 0 || (!shattered && f.shield !== p.sh)) fail(5, "banked at bank 0");
        /* [6] THE BEAT */
        const rb = beats.filter(b => b.ram);
        const killed = p.fhp > 0 && foe.hp <= 0;
        if (rb.length !== 1) fail(6, `${rb.length} ram beats on a slam`);
        else if (!!rb[0].fatal !== killed) fail(6, `fatal ${rb[0].fatal}, killed ${killed}`);
        else { inc("beatOk"); if (killed) inc("fatalSlam"); }
      } else {
        if (hurts.length || beats.length) fail(6, "a hurt or beat on a frame with no slam");
        if (inRange && p.cd1 <= 1e-9) fail(2, "in range with the cooldown clear, and no slam");
        if (f.ramTally.banks !== p.banks) fail(5, "a bank with no slam");
      }
      if (foe.x !== p.fx || foe.y !== p.fy) fail(4, "a ram frame moved the foe's position");
      /* [7] NO STOP BUT A WARD'S OWN */
      if (!shattered && this.hitStop !== hs0) fail(7, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
    }
    if (shattered) inc("wardBreaks", shattered);
    return r;
  };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "portcullis");
  const T = { casts: 0, frames: 0, shieldSum: 0, slams: 0, dealt: 0, banks: 0, banked: 0 };
  let fights = 0, wins = 0, decided = 0, shieldFight = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "portcullis", sd) : new AC.Match("portcullis", fid, sd);
    const me = side ? m.b : m.a;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.ramTally){ for (const k in T) T[k] += me.ramTally[k];
      if (me.ramTally.frames) shieldFight += me.ramTally.shieldSum / me.ramTally.frames; }
  }
  P.tickRam = oTick;
  const u = AC.WEAPONS.find(w => w.id === "portcullis").ult;
  return { n, bad, T, fights, win: wins / decided, shieldFight: shieldFight / fights,
           u: { charge: u.charge, accel: u.accel, share: u.share, cd: u.cd, knock: u.knock, bank: u.bank } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickRam === 'function'"):
        raise SystemExit("no tickRam in this build -- not an Onslaught link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
casts = T["casts"] or 1
print(f"\nONSLAUGHT PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Portcullis both sides x every foe x {a.seeds} seeds)   ult {U}")
print(f"  per cast: slams {T['slams']/casts:.2f}  dmg {T['dealt']/casts:.2f}  banked {T['banked']/casts:.2f}   "
      f"shield on a window frame {T['shieldSum']/max(1,T['frames']):.2f} (per fight, windowless as 0: {R['shieldFight']:.2f})   "
      f"casts/fight {T['casts']/R['fights']:.2f}   Portcullis win {R['win']:.1%}")
print(f"  slams at zero shield {n.get('zeroSlam',0)}   killing slams {n.get('fatalSlam',0)}   "
      f"wards broken by a slam {n.get('wardBreaks',0)}   pinned frames {n.get('pinnedOk',0)}")
checks = [
    (1, "the charge: v + unit(foe) x accel x dt, clamped at speedMax; none while pinned", n.get("chargeOk", 0) > 0),
    (2, "a slam only inside 2R + pad, never closer than `cd`, never a missed clear contact", n.get("rangeOk", 0) > 0),
    (3, "each slam: hurt(foe, share x shield) once from the caster; none at zero shield", n.get("dmgOk", 0) > 0),
    (4, "the knock: `knock` along caster -> foe; the foe's position untouched", n.get("knockOk", 0) > 0),
    (5, "the bank: min(cap, shield + bank), shieldMax, the ward's clock; banks = slams (none at bank 0)",
        (n.get("bankOk", 0) > 0) if U["bank"] else n.get("slams", 0) > 0),
    (6, "one hit beat marked `ram` a slam, fatal iff it killed; none otherwise", n.get("beatOk", 0) > 0),
    (7, "no hit stop but a ward's own shatter", n.get("frames", 0) > 0),
    (8, "the window is `dur` long on the window clock", n.get("closeOk", 0) > 0),
    (9, "only Portcullis carries ultRam", True),
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
