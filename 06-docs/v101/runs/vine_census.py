#!/usr/bin/env python3
"""THE VINE, PRICED LIVE — v68, the verdant flail (the 35th cell).

The §1 in `06-docs/v68/verdant-flail-design-v68.md` run INSIDE `m.step`
against every relic in the build, ring_price's shape: an overlay that reads
the engine's own chain geometry each frame and pays through the engine's own
gates. Nothing is written to any build.

THE VINE is the chain: the segment from the haft's tip (`f.pivX/Y`) to the
head (`f.headX/Y`), `vineW` wide. While the foe's disc overlaps it, every
`biteCd` seconds it takes a BITE: `biteDmg` through `m.hurt` (the foe's ward
absorbs first; no crit / sunder / jitter / beat — DECLARED) and `bitePer`
stacks of entangle through `foe.apply`, the REAL status, so the slow it
carries is the engine's own. The head's blade blow is untouched and still
goes through `resolveHit` as ever.
GROWTH: every bite adds `grow` to the caster's `reachMul` (cap `growCap`) —
the field Revenant already grows the chain with, at all seven read sites —
and the window restores it to 1 on close, as Revenant does.
THE ROOT: when the window closes, the foe is pinned (`f.pin`, which
`tickStasis` turns into a weapon lock too) for `rootPer` seconds per entangle
stack it is carrying at that instant.

Arms, paired on (foe, seed):
  A  no ultimate            the body exactly as cell_ults_on prices it
  B  bites only             the live vine, no growth, no root
  C  bites + growth
  D  the whole §1           bites + growth + root
  R  root only              the root fed by the blade's own stacks (substitution control)

CONTROL THAT CAN FAIL: arm A must reproduce `cell_ults_on`'s ults-on body for
verdant:flail on the same seeds — 23/330 = 6.97% at seed0 2207 x 10 on
sc-trunk. It is the identical fight; anything else is the harness.

Bookkeeping asserted per fight: bites = stacks applied / bitePer.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, 'C:/dev/sundered-crown/tools')
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=10)
ap.add_argument("--seed0", type=int, default=2207)
ap.add_argument("--secs", type=float, default=160.0)
ap.add_argument("--blade", type=float, default=None)
ap.add_argument("--charge", type=float, default=16.0)
ap.add_argument("--dur", type=float, default=8.0)
ap.add_argument("--vine-w", type=float, default=8.0)
ap.add_argument("--bite-dmg", type=float, default=2.0)
ap.add_argument("--bite-cd", type=float, default=0.30)
ap.add_argument("--bite-per", type=int, default=1)
ap.add_argument("--grow", type=float, default=0.05)
ap.add_argument("--grow-cap", type=float, default=1.8)
ap.add_argument("--grow-time", type=float, default=0.0, help="reachMul gained per SECOND the window is open (growth by time, not by bite)")
ap.add_argument("--root-per", type=float, default=0.30)
ap.add_argument("--haft", type=int, default=0, help="1 = the haft (ball to pivot) is live too")
ap.add_argument("--seek", type=int, default=0, help="1 = while the window is open the facing is driven at the foe and the spin is zeroed: the vine REACHES")
ap.add_argument("--track", type=int, default=0, help="with --seek 2: 1 = the vine also draws back in when the foe comes closer")
ap.add_argument("--turn", type=float, default=0.0, help="max turn rate of the seeking facing, rad/s (0 = snaps to the foe)")
ap.add_argument("--noblade", type=int, default=0, help="1 = the head's own blade is off while the window is open (the vine is the weapon)")
ap.add_argument("--arms", default="A,B,C,D")
ap.add_argument("--foes", default=None, help="comma list; default every other relic")
ap.add_argument("--control", type=float, default=None, help="arm A must land within 0.05pp of this")
ap.add_argument("--out", default="/tmp/vine_price.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, P, arms]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg, spin: w.spin,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  // the cell, exactly as cell_ults_on builds it
  w.aff = "verdant"; delete w.onSelf; w.onHit = { entangle: 2 };
  if (P.blade) w.dmg = P.blade;
  if (w.ult) w.ult.charge = 1e9;
  // point-to-segment distance
  const segDist = (px, py, ax, ay, bx, by) => {
    const dx = bx - ax, dy = by - ay, l2 = dx*dx + dy*dy;
    let t = l2 > 0 ? ((px - ax)*dx + (py - ay)*dy) / l2 : 0;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (ax + t*dx), py - (ay + t*dy));
  };
  const rows = [];
  for (const arm of arms) for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    const ultOn = arm !== "A";
    let winOpen = false;
    if (P.noblade){ const orig = m.bladeSegments.bind(m); m.bladeSegments = (f) => (f === me && winOpen && ultOn) ? [] : orig(f); }
    const bitesOn = arm === "B" || arm === "C" || arm === "D";
    const growOn  = arm === "C" || arm === "D";
    const rootOn  = arm === "D" || arm === "R";
    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, cd = 0;
    const S = { casts: 0, bites: 0, stacks: 0, dmgBite: 0, touchFrames: 0, winFrames: 0,
                growPeak: 1, rootSec: 0, roots: 0, headBlowsIn: 0, headBlowsOut: 0,
                foeStacksIn: 0, castsHit: 0, fSteps: 0, fFrozen: 0, fWin: 0, fWinFrozen: 0 };
    let hitsAtOpen = 0, bitThisCast = false;
    while (!m.over && step < secs / DT){
      const hits0 = me.hits;
      { const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold, ow = castEnd >= 0 && t < castEnd;
        S.fSteps++; if (fz) S.fFrozen++; if (ow){ S.fWin++; if (fz) S.fWinFrozen++; } }
      m.step(DT); step++; t += DT;
      const open = castEnd >= 0 && t < castEnd;
      if (me.hits > hits0){ if (open) S.headBlowsIn += me.hits - hits0; else S.headBlowsOut += me.hits - hits0; }
      if (!ultOn) continue;
      if (castEnd < 0 && t >= nextCast && me.alive && foe.alive){
        castEnd = t + P.dur; nextCast += P.charge; S.casts++; cd = 0; bitThisCast = false;
        winOpen = true; if (P.seek) w.spin = 0;
      }
      if (castEnd >= 0 && t < castEnd){
        S.winFrames++;
        if (P.seek && foe.alive){
          const want = Math.atan2(foe.y - me.y, foe.x - me.x);
          if (P.turn > 0){
            let dlt = want - me.theta; dlt = Math.atan2(Math.sin(dlt), Math.cos(dlt));
            const mx = P.turn * DT; me.theta += Math.max(-mx, Math.min(mx, dlt));
          } else me.theta = want;
        }
        S.foeStacksIn += foe.stacks("entangle");
        if (growOn && P.growTime > 0){
          if (P.seek === 2){
            // GROWS UNTIL IT REACHES: the target is the foe's rim, in units of the type's own reach
            const dd = Math.hypot(foe.x - me.x, foe.y - me.y);
            const target = Math.max(1, Math.min(P.growCap, (dd - R) / (w.reach * m.actMods.reach)));
            if (target > me.reachMul) me.reachMul = Math.min(target, me.reachMul + P.growTime * DT);
            else if (P.track) me.reachMul = Math.max(target, me.reachMul - P.growTime * DT);
          } else me.reachMul = Math.min(P.growCap, me.reachMul + P.growTime * DT);
          S.growPeak = Math.max(S.growPeak, me.reachMul); }
        cd -= DT;
        if (foe.alive && me.alive){
          const ax = P.haft ? me.x : me.pivX, ay = P.haft ? me.y : me.pivY;
          const d = segDist(foe.x, foe.y, ax, ay, me.headX, me.headY);
          if (d < R + P.vineW){
            S.touchFrames++;
            if (bitesOn && cd <= 0){
              cd = P.biteCd; S.bites++; bitThisCast = true;
              if (P.biteDmg > 0){ const hp0 = foe.hp + foe.shield; m.hurt(foe, P.biteDmg, me); S.dmgBite += hp0 - (foe.hp + foe.shield); }
              foe.apply("entangle", P.bitePer, me); S.stacks += P.bitePer;
              if (growOn){ me.reachMul = Math.min(P.growCap, me.reachMul + P.grow); S.growPeak = Math.max(S.growPeak, me.reachMul); }
            }
          }
        }
      }
      if (castEnd >= 0 && t >= castEnd){
        castEnd = -1; winOpen = false; w.spin = saved.spin;
        if (bitThisCast) S.castsHit++;
        me.reachMul = 1;
        if (rootOn && foe.alive){
          const n = foe.stacks("entangle");
          if (n > 0){
            const hold = P.rootPer * n;
            if (!(foe.pin > hold)) foe.pinV = [foe.vx, foe.vy];
            foe.pin = Math.max(foe.pin, hold); foe.pinMax = Math.max(foe.pinMax, hold);
            S.roots++; S.rootSec += hold;
          }
        }
      }
    }
    if (castEnd >= 0) me.reachMul = 1;
    w.spin = saved.spin; winOpen = false;
    if (S.stacks !== S.bites * P.bitePer) throw new Error("bookkeeping: stacks != bites * bitePer");
    rows.push({ arm, foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: step * DT, ...S });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return rows;
}"""

P = dict(blade=a.blade, charge=a.charge, dur=a.dur, vineW=a.vine_w, biteDmg=a.bite_dmg,
         biteCd=a.bite_cd, bitePer=a.bite_per, grow=a.grow, growCap=a.grow_cap,
         rootPer=a.root_per, haft=a.haft, growTime=a.grow_time, seek=a.seek, noblade=a.noblade, track=a.track, turn=a.turn)
arms = a.arms.split(",")
seeds = [a.seed0 + 11 * i for i in range(a.seeds)]

def wr(rs):
    d = [r for r in rs if r["win"] >= 0]
    return sum(r["win"] for r in d) / len(d) if d else float("nan")

def mean(rs, k, per="casts"):
    tot = sum(r[k] for r in rs); n = sum(r[per] for r in rs) if per else len(rs)
    return tot / n if n else 0.0

t0 = time.time()
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    donor = "gravemourn"
    foes = a.foes.split(",") if a.foes else [i for i in ids if i != donor]
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    print(f"{len(ids)} relics · Chromium {ver} · donor {donor} as verdant x flail · "
          f"{len(foes)} foes x {len(seeds)} seeds = {len(foes)*len(seeds)} fights an arm")
    print("  " + " ".join(f"{k}={v}" for k, v in P.items()))
    rows = page.evaluate(JS, [donor, foes, seeds, a.secs, P, arms])
    assert not errors, errors
out = {"P": P, "arms": {}}
base = None
print(f"\n  {'arm':<22}{'win':>7}{'casts':>7}{'bites':>7}{'stk':>6}{'dmg':>6}{'touch%':>8}{'foeStk':>7}{'grow':>6}{'root s':>7}{'hits in/out':>12}{'castsHit':>9}")
for arm in arms:
    rs = [r for r in rows if r["arm"] == arm]
    W = wr(rs)
    if arm == "A": base = W
    casts = sum(r["casts"] for r in rs)
    touch = sum(r["touchFrames"] for r in rs) / max(1, sum(r["winFrames"] for r in rs))
    foeStk = sum(r["foeStacksIn"] for r in rs) / max(1, sum(r["winFrames"] for r in rs))
    growPk = statistics.mean(r["growPeak"] for r in rs)
    label = {"A": "A no ultimate", "B": "B bites only", "C": "C bites + growth",
             "D": "D the whole §1", "R": "R root only"}[arm]
    print(f"  {label:<22}{W:>7.1%}{casts/len(rs):>7.2f}{mean(rs,'bites'):>7.2f}{mean(rs,'stacks'):>6.1f}"
          f"{mean(rs,'dmgBite'):>6.1f}{touch:>8.1%}{foeStk:>7.2f}{growPk:>6.2f}{mean(rs,'rootSec'):>7.2f}"
          f"{mean(rs,'headBlowsIn',None):>6.2f}/{mean(rs,'headBlowsOut',None):<5.2f}"
          f"{mean(rs,'castsHit'):>9.0%}")
    byFoe = {}
    for r in rs:
        if r["win"] >= 0: byFoe.setdefault(r["foe"], []).append(r["win"])
    out["arms"][arm] = dict(byFoe={k: sum(v)/len(v) for k, v in byFoe.items()}, win=W, n=len(rs), casts=casts, bitesPerCast=mean(rs, "bites"),
                            stacksPerCast=mean(rs, "stacks"), dmgPerCast=mean(rs, "dmgBite"),
                            touch=touch, foeStk=foeStk, growPeak=growPk, rootSec=mean(rs, "rootSec"),
                            hitsIn=mean(rs, "headBlowsIn", None), hitsOut=mean(rs, "headBlowsOut", None),
                            census={k: sum(r[k] for r in rs) for k in ("fSteps", "fFrozen", "fWin", "fWinFrozen")})
    _c = out["arms"][arm]["census"]
    print(f"      census: frozen {_c['fFrozen']/max(1,_c['fSteps']):.4f} of lab steps, {_c['fWinFrozen']/max(1,_c['fWin']):.4f} in windows; lab 16 -> engine {16*(1-_c['fFrozen']/max(1,_c['fSteps'])):.2f}")
if base is not None:
    print("\n  lifts over A: " + "  ".join(f"{arm} {100*(out['arms'][arm]['win']-base):+.1f}" for arm in arms if arm != "A"))
if a.control is not None:
    ok = abs(base - a.control) < 0.0005
    print(f"  CONTROL arm A {base:.2%} against {a.control:.2%}: {'PASS' if ok else 'FAIL'}")
    if not ok: sys.exit(2)
print(f"\n  {len(rows)} fights in {time.time()-t0:.0f}s   errors: {errors}")
pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
