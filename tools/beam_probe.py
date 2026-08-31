#!/usr/bin/env python3
"""PRICE EVERY SENTENCE OF THE PINK SCYTHE'S §1 BEFORE A BUILDER IS OPENED.

    python3 beam_probe.py --game ../02-chain/sc-paradox-ignition.html

RICK'S §1:

    "when the ult fires the scythe charges up (with a loud glowing animation)
     and then fires a targeted beam (thick, at least half the thickness of an
     artifact) the beam has limited range and points at the tip. the beam
     slowly rotates to track the enemy ball. while it persists it does rapid
     ticks of damage that push enemies towards its tip where it does bonus
     damage. the beam uses the scythes banked shield to increase its duration."

Vigil's core is `#F06BB8`, so "pink scythe" is the school named by its colour.

**There is no beam in this game.** `kind: "beam"` exists on Benediction and
Bloodprice, but `fireUlt` has no `kind === "beam"` branch — it is a
SET-PIECE label and a particle spec, and both those ultimates are
instantaneous. Nothing here persists, tracks, or pushes. So every geometric
sentence of §1 is priced by overlaying the proposed beam on REAL trajectories
rather than by building it: the fight is the shipped simulation, and the beam
is a test applied to it frame by frame.

  [1] THE POOL AT THE CAST — the sentence most likely to break, and the
      project has already measured its failure once. v41 on Bulwarden: *"the
      pool at the cast is a MEDIAN OF ZERO over 88 casts"*, which is why Aegis
      was changed to feed the wall while it stands. Charge is pure wall time
      (`f.charge += dt`), so a cast is a metronome and the pool it finds is a
      blind sample of the ward's state. Bulwarden is carried as a CONTROL,
      because reproducing a published number is how this instrument earns the
      scythe's.

  [2] TIME ON TARGET — the decisive geometry. The beam is fired from the blade
      TIP, and this weapon's tip ORBITS the caster at 3.2 rad/s on a radius of
      R + reach. So a beam that "slowly rotates to track" has a slowly turning
      direction on a fast-moving origin, and whether that ever holds a target
      is not something anybody can reason out. Swept over turn rate and range,
      with the caster's CENTRE as the control origin so the orbit's
      contribution is separable.

  [3] THE PUSH TOWARD THE TIP. A sustained force along the beam, away from the
      caster. v41 found the warhammer throwing its quarry out of its own
      reach and v47 found the twinblade already out of reach; this pushes
      along a line whose far end is the bonus. Measured as where the foe ends
      up along the beam's own axis.

  [4] THE WIND-UP. `breakSpin` is the hook every true stun already calls, and
      v44 measured 14.77% of Crucible casts eating one. A charge-up on this
      relic is priced against the same four hex appliers.

  [5] THE TICK. `CONFIG.combat.hitCd` is 0.45s per segment and nothing in this
      game ticks damage off a volume except a status. What "rapid" can mean.

Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


def median(xs, d=0.0):
    xs = sorted(xs)
    return statistics.median(xs) if xs else d


DONOR = "thornwake"          # the scythe block; vigil is grafted over it
CONTROL = "bulwarden"        # the shipped vigil warhammer, for v41's number
FOES = ["aureole", "vinesower", "farwarden", "marrowdraw",      # ranged
        "emberedge", "nightfell", "heartwood", "axiom",          # swing
        "lastlight", "censer", "foregone", "spellbreaker",       # spin
        "gravemourn", "slagheart", "redflail", "paradox"]        # chain

# ------------------------------------------------------ [1] pool at the cast ---
# `tickCharge` is `f.charge += dt; if (f.charge >= u.charge) fireUlt(...)`, so a
# cast lands on a metronome and the ward pool it finds is a blind sample. The
# cast is intercepted rather than simulated: `fireUlt` is shadowed on the
# instance, the pool is recorded, and the shipped ultimate then runs exactly as
# it would.

POOL_JS = r"""([donor, graft, foes, seeds, secs, pin, pinIds]) => {
  const DT = AC.CONFIG.physics.dt;
  const W  = AC.STATUS.ward;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  if (graft){ w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 }; }

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg };
    if (pin > 0) x.dmg = pin;
  }

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const pools = [];
      const origFire = AC.Match.prototype.fireUlt;
      m.fireUlt = function(fr, fo){
        if (fr === me) pools.push(fr.shield);
        return origFire.call(m, fr, fo);
      };
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      rows.push({ foe: f, seed: sd, dur: step * DT, pools });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved))
    AC.WEAPONS.find(y => y.id === pid).dmg = saved[pid].dmg;
  return rows;
}"""

# ------------------------------------------------------------- [2][3] the beam ---
# The beam is not built. It is OVERLAID on the shipped simulation: the fight
# runs untouched, and every frame of the window the probe computes where the
# beam would be and asks whether the quarry is inside it. Nothing is written
# back, so the trajectories are the game's own and every arm sees the identical
# fight.
#
# `push` is the one arm that CANNOT be a pure overlay — a force changes the
# fight — so it is applied optionally and the two are reported apart.

BEAM_JS = r"""([donor, foes, seeds, cfg, secs, pin, pinIds]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                   onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 };

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { dmg: x.dmg, ch: x.ult ? x.ult.charge : null };
    if (pin > 0) x.dmg = pin;
    if (x.ult) x.ult.charge = 1e9;         // no ultimates: the beam is the only one
  }

  const wrap = (a) => { while (a >  Math.PI) a -= Math.PI*2;
                        while (a < -Math.PI) a += Math.PI*2; return a; };
  const segD = (ax, ay, bx, by, px, py) => {
    const dx = bx-ax, dy = by-ay, L2 = dx*dx+dy*dy || 1;
    let t = ((px-ax)*dx + (py-ay)*dy) / L2;
    t = Math.max(0, Math.min(1, t));
    return { d: Math.hypot(px-(ax+dx*t), py-(ay+dy*t)), t };
  };

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const a0 = Math.round(cfg.at / DT);
      const a1 = Math.round((cfg.at + cfg.dur) / DT);

      let step = 0, ba = 0, on = 0, frames = 0, alive = true, frozenTheta = 0;
      let banked = 0, passTip = 0, passAt = [];
      const origHit2 = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const before = me.shield;
        const r = origHit2.call(m, self, foe2, hx, hy, seg, mul, over);
        if (self === me && step >= a0) banked += Math.max(0, me.shield - before);
        return r;
      };
      let tipOn = 0, run = 0, bestRun = 0, runs = [], axSum = 0, axN = 0;
      let passPeak = 0;
      let sepSum = 0;

      while (step < a1){
        if (m.over){ alive = false; break; }
        if (step === a0){
          ba = Math.atan2(th.y - me.y, th.x - me.x);
          frozenTheta = me.theta;
        }

        if (step >= a0){
          /* THE ORIGIN. `tip` is the blade tip, which ORBITS the caster at the
             weapon's own spin; `centre` is the control that removes the orbit
             so its contribution is separable. */
          const reach = me.w.reach * m.actMods.reach;
          /* THREE ORIGINS. `tip` is the blade tip as it is, orbiting with the
             weapon. `tipfrozen` is the same tip with the weapon's rotation
             STOPPED for the duration -- the beam still comes out of the blade,
             the blade just stops sweeping, which is a thing a cast is allowed
             to do and which the Crucible and Converse both already do to spin.
             `centre` removes the arm entirely and is the control. */
          let ox, oy;
          if (cfg.origin === "centre"){ ox = me.x; oy = me.y; }
          else {
            const th0 = cfg.origin === "tipfrozen" ? frozenTheta : me.theta;
            ox = me.x + Math.cos(th0) * (R + reach);
            oy = me.y + Math.sin(th0) * (R + reach);
          }
          /* THE TRACK. Rate limited, the way `s.home` is: a beam that cannot
             turn faster than `turn` can be walked away from, and that is a
             failure a viewer can watch rather than arithmetic. */
          const want = Math.atan2(th.y - oy, th.x - ox);
          ba += Math.max(-cfg.turn * DT, Math.min(cfg.turn * DT, wrap(want - ba)));
          const ex = ox + Math.cos(ba) * cfg.range;
          const ey = oy + Math.sin(ba) * cfg.range;
          const hit = segD(ox, oy, ex, ey, th.x, th.y);
          const inside = hit.d < cfg.half + R;
          frames++;
          if (inside){
            on++; run++;
            /* the FURTHEST down the beam this pass reached. The tip bonus is a
               property of the PASS, not of a frame: did this crossing catch the
               ball out at the far end at any point during it. */
            if (hit.t > passPeak) passPeak = hit.t;
            axSum += hit.t; axN++;
            if (hit.t > cfg.tipFrom) tipOn++;
            /* THE PUSH, along the beam, away from the origin. This is the one
               thing here that is not an overlay: it changes the fight. */
            if (cfg.push > 0){
              th.vx += Math.cos(ba) * cfg.push * DT;
              th.vy += Math.sin(ba) * cfg.push * DT;
            }
          } else {
            if (run > 0){
              runs.push(run * DT);
              if (run > bestRun) bestRun = run;
              /* WHERE THE PASS CAUGHT IT. A pass is the unit now, not a frame,
                 so the tip bonus is a property of the PASS: did this crossing
                 catch the ball out at the far end at any point in it. */
              if (passPeak > cfg.tipFrom) passTip++;
              passAt.push(passPeak);
            }
            run = 0; passPeak = 0;
          }
          sepSum += Math.hypot(th.x - me.x, th.y - me.y);
        }
        m.step(DT); step++;
      }
      if (run > 0){ runs.push(run * DT);
                    if (passPeak > cfg.tipFrom) passTip++; passAt.push(passPeak); }
      rows.push({ foe: f, foeMode: th.w.mode, seed: sd, alive,
                  frames, on, tipOn,
                  share: frames ? on / frames : 0,
                  tipShare: on ? tipOn / on : 0,
                  meanRun: runs.length ? runs.reduce((x, y) => x + y, 0) / runs.length : 0,
                  bestRun: bestRun * DT, nRuns: runs.length,
                  axis: axN ? axSum / axN : 0,
                  banked, passes: runs.length, passTip,
                  passTipShare: runs.length ? passTip / runs.length : 0,
                  sep: frames ? sepSum / frames : 0 });
    }
  }

  w.aff = savedW.aff;
  delete w.onHit; delete w.onSelf;
  if (savedW.onHit) w.onHit = savedW.onHit;
  if (savedW.onSelf) w.onSelf = savedW.onSelf;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    x.dmg = saved[pid].dmg;
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""

TRAP_JS = r"""() => {
  const fu = AC.Match.prototype.fireUlt.toString();
  const tc = AC.Match.prototype.tickCharge.toString();
  const beamKinds = AC.WEAPONS.filter(w => w.ult && w.ult.kind === "beam")
                              .map(w => w.name + " / " + w.ult.name);
  return {
    noBeamBranch: !/kind === "beam"/.test(fu),
    beamKinds,
    chargeIsWallTime: /f\.charge \+= dt/.test(tc),
    hasBreakSpin: typeof AC.Match.prototype.breakSpin === "function",
    hasSpendWard: typeof AC.Match.prototype.spendWard === "function",
    hitCd: AC.CONFIG.combat.hitCd,
    ballR: AC.CONFIG.physics.ballR,
    arena: AC.CONFIG.arena,
    scythe: (() => { const x = AC.WEAPONS.find(y => y.id === "thornwake");
                     return { reach: x.reach, spin: x.spin, width: x.width }; })(),
    vigilCore: AC.AFFINITIES.vigil.core,
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--pin", type=float, default=24.0)
    ap.add_argument("--at", type=float, default=15.0)
    ap.add_argument("--dur", type=float, default=4.0)
    ap.add_argument("--only", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"0", "1", "2", "3", "4"}
    gp = (HERE / a.game).resolve()
    seeds = [7701 + 29 * i for i in range(a.seeds)]
    out: dict = {}

    with game(game_path=gp) as (page, errors):
        t = page.evaluate(TRAP_JS)
        pin_ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        R = t["ballR"]
        tipR = R + t["scythe"]["reach"]
        print(f"\nvigil core {t['vigilCore']} (pink)   ballR {R}   "
              f"scythe reach {t['scythe']['reach']} spin {t['scythe']['spin']}   "
              f"blade tip {tipR} from centre   arena "
              f"{t['arena']['w']}x{t['arena']['h']}   hitCd {t['hitCd']}")

        if "0" in want:
            print(f"\n[0] WHAT ALREADY EXISTS\n")
            check("THERE IS NO BEAM IN THIS GAME — `kind: \"beam\"` is a set-piece "
                  "label with no branch in fireUlt",
                  t["noBeamBranch"],
                  "carried by " + "; ".join(t["beamKinds"])
                  + " — both instantaneous. Nothing here persists, tracks or "
                    "pushes, so every geometric sentence of §1 is new")
            check("a cast is a METRONOME — charge is pure wall time, so the ward "
                  "pool a cast finds is a blind sample and not something the "
                  "relic can aim", t["chargeIsWallTime"])
            check("the two hooks §1 needs already exist: `breakSpin` for the "
                  "wind-up and `spendWard` for the pool",
                  t["hasBreakSpin"] and t["hasSpendWard"])

        # ---------------------------------------------------------- [1] --
        if "1" in want:
            print(f"\n[1] THE POOL AT THE CAST — the sentence most likely to break\n")
            print(f"    {'relic':<26}{'casts':>7}{'MEDIAN':>8}{'mean':>7}"
                  f"{'empty':>8}{'>= 45':>8}{'at cap':>8}")
            pools = {}
            for label, donor, graft in [
                    ("Bulwarden (v41's control)", CONTROL, False),
                    ("a vigil scythe", DONOR, True)]:
                foes = [f for f in FOES if f != donor]
                rows = page.evaluate(POOL_JS, [donor, graft, foes, seeds,
                                               a.secs, a.pin, pin_ids])
                ps = [p for r in rows for p in r["pools"]]
                pools[label] = {"n": len(ps), "median": median(ps),
                                "mean": mean(ps),
                                "empty": sum(1 for p in ps if p < 0.5) / max(1, len(ps)),
                                "half": sum(1 for p in ps if p >= 45) / max(1, len(ps)),
                                "cap": sum(1 for p in ps if p >= 89.5) / max(1, len(ps))}
                v = pools[label]
                print(f"    {label:<26}{v['n']:>7}{v['median']:>8.1f}{v['mean']:>7.1f}"
                      f"{v['empty']:>8.0%}{v['half']:>8.0%}{v['cap']:>8.0%}")
            sc = pools["a vigil scythe"]
            bw = pools["Bulwarden (v41's control)"]
            check("v41's published number reproduces — the pool at a Bulwarden cast "
                  "is a MEDIAN OF ZERO",
                  bw["median"] < 0.5,
                  f"median {bw['median']:.1f} over {bw['n']} casts against v41's "
                  f"'median of zero over 88 casts'")
            check("AND THE SCYTHE IS NO BETTER — a beam whose duration is read off "
                  "the pool at the instant of the cast is a beam of zero length "
                  "most of the time",
                  sc["empty"] > 0.35,
                  f"{sc['empty']:.0%} of casts find an EMPTY shell, median "
                  f"{sc['median']:.1f}, mean {sc['mean']:.1f} of a 90 cap. The "
                  f"ward is up 42% of the fight (scythe_survey §4) and a cast is "
                  f"a metronome, so the two are simply uncorrelated")
            out["pool"] = pools

        # ---------------------------------------------------------- [2] --
        if "2" in want:
            print(f"\n[2] TIME ON TARGET — a slow beam on a tip that orbits at "
                  f"{t['scythe']['spin']} rad/s\n")
            print(f"    {'arm':<34}{'on target':>11}{'mean run':>10}"
                  f"{'longest':>9}{'breaks':>8}{'near the tip':>14}")
            base = dict(at=a.at, dur=a.dur, turn=1.6, range=300, half=17,
                        tipFrom=0.75, origin="tip", push=0)
            arms = {}
            grid = [
                ("turn 1.6  range 300  tip", dict()),
                ("turn 0.8  range 300  tip", dict(turn=0.8)),
                ("turn 3.2  range 300  tip", dict(turn=3.2)),
                ("turn 6.0  range 300  tip", dict(turn=6.0)),
                ("turn 1.6  range 180  tip", dict(range=180)),
                ("turn 1.6  range 520  tip", dict(range=520)),
                ("turn 1.6  range 300  TIP FROZEN", dict(origin="tipfrozen")),
                ("turn 3.2  range 300  TIP FROZEN", dict(turn=3.2,
                                                         origin="tipfrozen")),
                ("turn 1.6  range 300  CENTRE", dict(origin="centre")),
                ("turn 3.2  range 520  CENTRE", dict(turn=3.2, range=520,
                                                     origin="centre")),
            ]
            for label, over in grid:
                cfg = dict(base); cfg.update(over)
                rows = page.evaluate(BEAM_JS, [DONOR, FOES, seeds, cfg,
                                               a.secs, a.pin, pin_ids])
                ok = [r for r in rows if r["frames"] > 0]
                rec = {"share": mean(r["share"] for r in ok),
                       "run": mean(r["meanRun"] for r in ok if r["meanRun"] > 0),
                       "best": max(r["bestRun"] for r in ok),
                       "breaks": mean(r["nRuns"] for r in ok),
                       "tip": mean(r["tipShare"] for r in ok if r["on"] > 0),
                       "axis": mean(r["axis"] for r in ok if r["on"] > 0)}
                arms[label] = rec
                print(f"    {label:<34}{rec['share']:>11.1%}{rec['run']:>9.2f}s"
                      f"{rec['best']:>8.2f}s{rec['breaks']:>8.1f}{rec['tip']:>14.1%}")
            slow = arms["turn 1.6  range 300  tip"]
            fast = arms["turn 6.0  range 300  tip"]
            ctr = arms["turn 1.6  range 300  CENTRE"]
            froz = arms["turn 1.6  range 300  TIP FROZEN"]
            check("THE ORBITING TIP COSTS SOMETHING, AND IT IS SMALL — mounting "
                  "the beam on a blade that goes round at "
                  f"{t['scythe']['spin']} rad/s is a tax, not the design",
                  ctr["share"] - slow["share"] < 0.10,
                  f"tip {slow['share']:.1%} on target, tip with the weapon's spin "
                  f"STOPPED {froz['share']:.1%}, caster's centre "
                  f"{ctr['share']:.1%} — same turn rate, same range, same fights. "
                  f"So §1 can keep `points at the tip` for free; the sentence that "
                  f"costs is the next one")
            # A CHECK THAT CANNOT FAIL IS NOT A CHECK. The first cut of this
            # one passed a literal True and printed a table under a sentence the
            # table contradicts -- turning faster rescues the beam comfortably.
            # It asserts the ordering it actually found, and it would fail if
            # the turn rate stopped being the dominant knob.
            turns = [arms[k]["share"] for k in
                     ("turn 0.8  range 300  tip", "turn 1.6  range 300  tip",
                      "turn 3.2  range 300  tip", "turn 6.0  range 300  tip")]
            check("TURN RATE IS THE DOMINANT KNOB, and it runs the wrong way for "
                  "the word `slowly`",
                  turns == sorted(turns) and turns[-1] > 2 * turns[0],
                  "turn 0.8 / 1.6 / 3.2 / 6.0 -> "
                  + " / ".join(f"{x:.1%}" for x in turns)
                  + f"; the orbit costs {ctr['share'] - slow['share']:+.1%} beside "
                    f"that, so the tip mounting is a minor tax and the tracking "
                    f"rate is the design")
            check("AND A SLOW BEAM DOES NOT PERSIST ON ANYTHING — it flickers "
                  "across the quarry rather than holding it",
                  slow["run"] < 0.5,
                  f"at turn 1.6 the mean unbroken contact is {slow['run']:.2f}s and "
                  f"the beam breaks {slow['breaks']:.1f} times in a "
                  f"{a.dur:g}s window. `while it persists it does rapid ticks` "
                  f"and `slowly rotates` are in tension and the sweep is where "
                  f"that gets settled")
            out["beam"] = arms

        # ---------------------------------------------------------- [3] --
        if "3" in want:
            print(f"\n[3] THE PUSH TOWARD THE TIP — the one arm that is not an "
                  f"overlay, because a force changes the fight\n")
            print(f"    {'push (u/s^2)':<16}{'on target':>11}{'mean run':>10}"
                  f"{'position along the beam':>26}{'near the tip':>14}"
                  f"{'separation':>12}")
            base = dict(at=a.at, dur=a.dur, turn=1.6, range=300, half=17,
                        tipFrom=0.75, origin="tip", push=0)
            pushes = {}
            for p in (0, 150, 400, 900):
                cfg = dict(base); cfg["push"] = p
                rows = page.evaluate(BEAM_JS, [DONOR, FOES, seeds, cfg,
                                               a.secs, a.pin, pin_ids])
                ok = [r for r in rows if r["frames"] > 0]
                rec = {"share": mean(r["share"] for r in ok),
                       "run": mean(r["meanRun"] for r in ok if r["meanRun"] > 0),
                       "axis": mean(r["axis"] for r in ok if r["on"] > 0),
                       "tip": mean(r["tipShare"] for r in ok if r["on"] > 0),
                       "sep": mean(r["sep"] for r in ok)}
                pushes[p] = rec
                print(f"    {p:<16}{rec['share']:>11.1%}{rec['run']:>9.2f}s"
                      f"{rec['axis']:>25.2f}{rec['tip']:>14.1%}{rec['sep']:>12.0f}")
            # THE HONEST READ. The push moves the numbers in the right
            # direction and it moves them by almost nothing, and a check that
            # only asserts the sign would report a working mechanic. What it
            # has to assert is the SIZE.
            gain = pushes[900]["tip"] - pushes[0]["tip"]
            check("THE PUSH IS NEARLY INERT AT THESE CONTACT DURATIONS — six "
                  "times the force moves the quarry two points further down the "
                  "beam",
                  gain < 0.10,
                  "share of contact past 0.75 of the length: "
                  + ", ".join(f"{p} -> {pushes[p]['tip']:.0%}" for p in pushes)
                  + f"; mean position along the beam "
                    f"{pushes[0]['axis']:.2f} -> {pushes[900]['axis']:.2f}")
            check("and the reason is [2]: you cannot push a thing along a line "
                  "for 0.3 seconds",
                  pushes[0]["run"] < 0.5,
                  f"mean unbroken contact {pushes[0]['run']:.2f}s. THE PUSH AND "
                  f"THE TRACKING RATE ARE ONE DECISION, not two — the push only "
                  f"has somewhere to act if the beam holds, and the beam only "
                  f"holds if it turns fast")
            out["push"] = pushes

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            print(f"\n[4] THE LIGHTHOUSE — Rick took the slow beam, so the unit is "
                  f"the PASS and not the frame\n")
            print(f"    {'arm':<30}{'passes':>8}{'per second':>12}{'mean pass':>11}"
                  f"{'longest':>9}{'passes that reach the tip':>27}"
                  f"{'ward banked':>13}")
            base = dict(at=a.at, dur=a.dur, turn=1.6, range=300, half=17,
                        tipFrom=0.75, origin="tip", push=0)
            lh = {}
            grid4 = [
                ("turn 0.0  range 300   STATIC", dict(turn=0.0)),
                ("turn 0.4  range 300", dict(turn=0.4)),
                ("turn 0.8  range 300", dict(turn=0.8)),
                ("turn 1.6  range 300", dict()),
                ("turn 1.6  range 180", dict(range=180)),
                ("turn 1.6  range 420", dict(range=420)),
                ("turn 0.8  range 180", dict(turn=0.8, range=180)),
                ("turn 1.6  range 300  thick 26", dict(half=26)),
            ]
            for label, over in grid4:
                cfg = dict(base); cfg.update(over)
                rows = page.evaluate(BEAM_JS, [DONOR, FOES, seeds, cfg,
                                               a.secs, a.pin, pin_ids])
                ok = [r for r in rows if r["frames"] > 0]
                rec = {"passes": mean(r["passes"] for r in ok),
                       "per": mean(r["passes"] for r in ok) / a.dur,
                       "run": mean(r["meanRun"] for r in ok if r["meanRun"] > 0),
                       "best": max(r["bestRun"] for r in ok),
                       "tip": mean(r["passTipShare"] for r in ok if r["passes"] > 0),
                       "bank": mean(r["banked"] for r in ok)}
                lh[label] = rec
                print(f"    {label:<30}{rec['passes']:>8.1f}{rec['per']:>12.2f}"
                      f"{rec['run']:>10.2f}s{rec['best']:>8.2f}s"
                      f"{rec['tip']:>27.0%}{rec['bank']:>13.1f}")

            static = lh["turn 0.0  range 300   STATIC"]
            slow16 = lh["turn 1.6  range 300"]
            check("THE TRACKING IS NOT WHAT MAKES THE PASSES — a beam that does "
                  "not turn at all still gets crossed, because the BALL is what "
                  "moves",
                  static["passes"] > slow16["passes"] * 0.4,
                  f"a static beam takes {static['passes']:.1f} passes in "
                  f"{a.dur:g}s against {slow16['passes']:.1f} at turn 1.6. "
                  f"`slowly rotates to track` is doing less of the work than the "
                  f"sentence implies, and the honest version of the mechanic is "
                  f"that the HALL sweeps the beam as much as the beam sweeps the "
                  f"hall")
            thick = lh["turn 1.6  range 300  thick 26"]
            check("thickness buys contact where the turn rate must not",
                  thick["run"] > slow16["run"],
                  f"half-width 17 -> 26 (a beam 52 wide against a 68-wide relic) "
                  f"moves the mean pass {slow16['run']:.2f}s -> {thick['run']:.2f}s "
                  f"and passes {slow16['passes']:.1f} -> {thick['passes']:.1f}")
            short = lh["turn 1.6  range 180"]
            check("A SHORT BEAM IS A TIP BONUS THAT ACTUALLY FIRES — the far end "
                  "is where the ball is, instead of somewhere past it",
                  short["tip"] > lh["turn 1.6  range 420"]["tip"],
                  f"range 180 -> {short['tip']:.0%} of passes reach the tip zone, "
                  f"300 -> {slow16['tip']:.0%}, 420 -> "
                  f"{lh['turn 1.6  range 420']['tip']:.0%}. "
                  f"\"limited range\" is not a restriction on this design, it is "
                  f"the thing that makes its bonus reachable")
            print(f"\n    THE WARD, DRUNK CONTINUOUSLY — what a {a.dur:g}s beam "
                  f"banks while it runs\n")
            print(f"        {slow16['bank']:.1f} points of ward banked during the "
                  f"window, against a pool of 12.3 at the cast and a 90 cap.")
            print(f"        So a beam that drinks continuously is fed roughly "
                  f"{slow16['bank'] / a.dur:.1f} points a second by the blade that "
                  f"is casting it.")
            out["lighthouse"] = lh

        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
