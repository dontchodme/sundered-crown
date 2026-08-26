#!/usr/bin/env python3
"""PRICE §1 BEFORE A BUILDER IS OPENED.

    python3 runic_flail_probe.py --game ../02-chain/sc-marrowdraw-frame.html

v41 built §1 literally and had it refuted inside an hour at the cost of a
build. v42 answered that by pricing every sentence of §1 on the PREVIOUS tip,
runtime-only, before anything was written. This is that, for v43.

§1, Rick's, verbatim:

    "blue flail gains a medium sized hexagonal shaped chain of lightning
     surrounding the flails ball. the flail gains extra hit stun. enemies that
     stay inside the hexagon (that is inside the beams of lightning with the
     flail head) for too long are true stunned. unable to move (ball and
     weapon) for 2ish seconds."

Four sentences, and each one is a question with a number behind it:

  [1] WHERE THE FOE ACTUALLY IS. "medium sized" has to be a number, and the
      number is only meaningful against the separation this game runs at. The
      head reaches 119 units from the shell (flail_survey §2), so §1's own
      parenthesis -- the head is INSIDE the beams -- puts a floor under it.

  [2] CAN A DWELL TIMER EVER FIRE? "stay inside for too long" is a CONTINUOUS
      residence, and nothing in this game steers: a ball is ballistic, bounces,
      and never travels slower than 250 units a second. Whether a foe is ever
      inside anything for two seconds is a measurement, not a design choice,
      and if the answer is no then §1's last sentence cannot be built as
      written.

  [3] IS THE HEXAGON LOAD-BEARING? A hexagon of circumradius R against a circle
      of the same R and against its own inscribed circle at 0.866R. v42 asked
      the identical question of "larger ballista shots" and the answer was that
      it was a look knob, which is a licence rather than a disappointment.

  [4] WHAT IS 2 SECONDS OF PIN WORTH? `foe.stun` locks a weapon and NOTHING in
      this game stops a ball -- `moveMul` floors at 0.45 and `speedMin` is 250.
      A pinned ball is a new state. Priced by forcing one and measuring, on the
      windowed A/B that flail_survey §3 calibrated.

  [5] WHAT DOES "EXTRA HIT STUN" BUY? `stunDR 0.55` with `stunDRDecay 0.75` is
      diminishing returns on repeat hitstun, and hitstun is deliberately NOT a
      true stun. Swept on the donor alone.

  [6] AND WHAT DOES IT COST HEX? Two overlapping locks are one lock -- `f.stun`
      is a `Math.max`. Every hex fire inside a 2s pin is a fire that bought
      nothing, and this cell's whole channel is that fire.

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

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return 0.0
    i = min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))
    return xs[i]


DONOR = "gravemourn"          # the type donor: a flail, re-schooled at runtime
FOES = ["emberedge", "spellbreaker", "lastlight", "aureole", "censer", "slagheart"]

# ------------------------------------------------------- [1][2][3] the zone --
# One pass collects everything geometric: the separation trace, and for every
# candidate radius and every shape, the CONTINUOUS residence episodes. An
# episode is a run of frames the foe's CENTRE is inside; it ends the frame it
# leaves. Episodes that are still open when the fight ends are dropped, because
# a censored episode is not evidence about how long a residence lasts.
#
# The hexagon is tested three ways -- static, turning with the weapon, and as
# the two circles that bracket it -- because §1 says "hexagonal" and the whole
# question is whether that word is a hitbox or a picture.

ZONE_JS = r"""([donor, foes, seeds, secs, radii, pinIds, noult, charges, chRad, hold]) => {
  const DT = AC.CONFIG.physics.dt;
  const R  = AC.CONFIG.physics.ballR;
  const C  = AC.CONFIG.chain;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null };
  w.aff = "runic"; delete w.onHit; w.onHit = { hex: 1 };

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { ch: x.ult ? x.ult.charge : null };
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const K = Math.cos(Math.PI / 6);           // apothem / circumradius
  const inHex = (dx, dy, rad, phi) => {
    const d = Math.hypot(dx, dy);
    if (d > rad) return false;               // outside the circumcircle
    if (d <= rad * K) return true;           // inside the incircle
    let a = (Math.atan2(dy, dx) - phi) % (Math.PI / 3);
    if (a < 0) a += Math.PI / 3;
    return d * Math.cos(a - Math.PI / 6) <= rad * K;
  };
  /* Four shapes per radius. `hexT` turns with the weapon, which is what a ring
     of lightning hung on a spinning relic would do. */
  const SHAPES = ["circ", "hex0", "hexT", "circIn"];
  const inside = (sh, dx, dy, rad, th) =>
      sh === "circ"   ? Math.hypot(dx, dy) <= rad
    : sh === "circIn" ? Math.hypot(dx, dy) <= rad * K
    : sh === "hex0"   ? inHex(dx, dy, rad, 0)
    :                   inHex(dx, dy, rad, th);

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(donor, f, sd);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const chainLen = me.w.reach * (1 - C.hilt);

      const acc = {};
      for (const rad of radii) for (const sh of SHAPES)
        acc[sh + ":" + rad] = { in: 0, run: 0, eps: [] };
      /* THE CUMULATIVE FORK. A continuous residence is one way to read "stay
         inside for too long"; a charge that fills inside and bleeds outside is
         the other, and it is the one that can actually fire in a hall where
         nothing steers. `lock` is the pin itself -- a foe already pinned is
         not accruing toward the next one. */
      const ch = charges.map(c => ({ need: c[0], drain: c[1], q: 0, lock: 0,
                                     fires: 0 }));

      let step = 0, sepSum = 0, sepMin = 1e9, sepMax = 0;
      const sepHist = new Array(24).fill(0);   // 0..1200 in 50s
      let headMax = 0, headSum = 0;

      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const dx = th.x - me.x, dy = th.y - me.y;
        const d = Math.hypot(dx, dy);
        sepSum += d; if (d < sepMin) sepMin = d; if (d > sepMax) sepMax = d;
        sepHist[Math.min(23, Math.floor(d / 50))]++;
        const hd = Math.hypot(me.headX - me.x, me.headY - me.y);
        headSum += hd; if (hd > headMax) headMax = hd;
        for (const rad of radii) for (const sh of SHAPES){
          const k = sh + ":" + rad, a = acc[k];
          if (inside(sh, dx, dy, rad, me.theta)){ a.in++; a.run++; }
          else { if (a.run > 0) a.eps.push(a.run * DT); a.run = 0; }
        }
        const insideCh = inside("hexT", dx, dy, chRad, me.theta);
        for (const c of ch){
          if (c.lock > 0){ c.lock -= DT; continue; }
          c.q = insideCh ? c.q + DT : Math.max(0, c.q - c.drain * DT);
          if (c.q >= c.need){ c.fires++; c.q = 0; c.lock = hold; }
        }
      }
      /* An episode still open when the fight ends is CENSORED and dropped --
         it is not evidence about how long a residence lasts. */
      const zones = {};
      for (const k of Object.keys(acc))
        zones[k] = { share: step ? acc[k].in / step : 0,
                     eps: acc[k].eps, open: acc[k].run > 0 ? 1 : 0 };

      rows.push({ foe: f, seed: sd, steps: step, dur: step * DT,
                  sep: step ? sepSum / step : 0, sepMin, sepMax, sepHist,
                  head: step ? headSum / step : 0, headMax, chainLen,
                  ballR: R, zones,
                  charges: ch.map(c => ({ need: c.need, drain: c.drain,
                                          fires: c.fires })) });
    }
  }

  w.aff = savedW.aff; delete w.onHit;
  if (savedW.onHit) w.onHit = savedW.onHit;
  for (const pid of Object.keys(saved))
    if (saved[pid].ch !== null) AC.WEAPONS.find(y => y.id === pid).ult.charge = saved[pid].ch;
  return rows;
}"""


# --------------------------------------------------------------- [4] the pin --
# A pinned ball does not exist in this engine. `foe.stun` locks a weapon;
# `moveMul` floors at 0.45 and `speedMin` is 250, so nothing stops a ball.
# The pin is therefore built here as the cheapest possible thing that could be
# built there -- `move` is not called for that fighter, and its weapon is
# stunned for the same span -- and priced on the windowed A/B flail_survey §3
# calibrated. Velocity is preserved across the hold, so release is a resume
# rather than a drop.

PIN_JS = r"""([donor, foes, seeds, ats, win, hold, secs, pinIds, noult, mode, rad]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null };
  w.aff = "runic"; delete w.onHit; w.onHit = { hex: 1 };

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { ch: x.ult ? x.ult.charge : null };
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const K = Math.cos(Math.PI / 6);
  const inHex = (dx, dy, r2, phi) => {
    const d = Math.hypot(dx, dy);
    if (d > r2) return false;
    if (d <= r2 * K) return true;
    let ang = (Math.atan2(dy, dx) - phi) % (Math.PI / 3);
    if (ang < 0) ang += Math.PI / 3;
    return d * Math.cos(ang - Math.PI / 6) <= r2 * K;
  };

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      for (const at of ats){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        /* THE PIN FIRES WHERE THE MECHANIC WOULD FIRE IT. The first cut of
           this section pinned at a fixed clock time regardless of where the
           foe was, and a foe frozen at the 254 units this game runs at is a
           foe a 115-unit head cannot reach. That is a true fact about a pin
           and a false one about THIS pin, which only ever triggers on a foe
           that is already inside the hexagon. `arm` is the first frame after
           `at` at which the trigger condition holds. */
        const armStep = Math.round(at / DT);
        let atStep = -1, endStep = -1, offStep = -1;

        let step = 0, alive = true;
        let hits = 0, dealt0 = 0, foeHits = 0, taken0 = 0;
        let hexFires = 0, hexFiresWin = 0, hexWasted = 0, prevClock = 0;

        const origHit = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
          if (step >= atStep && step < endStep && mul === undefined){
            if (self === me) hits++; else foeHits++;
          }
          return r;
        };
        const origMove = AC.Match.prototype.move;
        m.move = function(f2, foe2, dt){
          /* mode 0 = control, 1 = weapon only (what `foe.stun` already does),
             2 = weapon AND ball, which is what §1 asks for */
          if (mode === 2 && f2 === th && atStep >= 0
              && step >= atStep && step < offStep) return;
          return origMove.call(m, f2, foe2, dt);
        };

        let dA = 0, tA = 0, sepAt = 0;
        const cap = Math.round(secs / DT);
        while (step < cap){
          if (m.over){ alive = false; break; }
          if (atStep < 0 && step >= armStep
              && inHex(th.x - me.x, th.y - me.y, rad, me.theta)){
            atStep = step; offStep = step + Math.round(hold / DT);
            endStep = step + Math.round(win / DT);
            dA = me.dealt; tA = th.dealt;
            sepAt = Math.hypot(th.x - me.x, th.y - me.y);
          }
          if (atStep >= 0 && step >= endStep) break;
          if (mode > 0 && atStep >= 0 && step >= atStep && step < offStep)
            th.stun = Math.max(th.stun, DT * 2);
          m.step(DT); step++;
          const c = th.hexClock || 0;
          if (c < prevClock - 1e-9){
            hexFires++;
            if (atStep >= 0 && step >= atStep && step < endStep) hexFiresWin++;
            if (mode > 0 && atStep >= 0 && step >= atStep && step < offStep)
              hexWasted++;
          }
          prevClock = c;
        }
        rows.push({ foe: f, seed: sd, at, mode, alive: alive && atStep >= 0,
                    armed: atStep >= 0, sepAt,
                    firedAt: atStep >= 0 ? atStep * DT : -1,
                    hits, foeHits, hexFires, hexFiresWin, hexWasted,
                    dealt: atStep >= 0 ? me.dealt - dA : 0,
                    taken: atStep >= 0 ? th.dealt - tA : 0 });
      }
    }
  }

  w.aff = savedW.aff; delete w.onHit;
  if (savedW.onHit) w.onHit = savedW.onHit;
  for (const pid of Object.keys(saved))
    if (saved[pid].ch !== null) AC.WEAPONS.find(y => y.id === pid).ult.charge = saved[pid].ch;
  return rows;
}"""


# --------------------------------------------------------- [5] extra hitstun --
# `takeHitstun` is the only site, and it already carries diminishing returns:
# raw = min(stunMax, stunBase + dmg*stunPerDmg), dur = raw / (1 + stunDR*n).
# The knob §1 asks for is a multiplier on THIS RELIC'S blows only, so it is
# applied by wrapping resolveHit's call site rather than by moving a CONFIG
# constant every relic in the game reads.

HITSTUN_JS = r"""([donor, foes, seeds, secs, muls, pinIds, noult]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const savedW = { aff: w.aff,
                   onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null };
  w.aff = "runic"; delete w.onHit; w.onHit = { hex: 1 };

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { ch: x.ult ? x.ult.charge : null };
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const mul of muls){
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(donor, f, sd);
        const me = m.a.w.id === donor ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        const th0 = th.maxHp;

        let step = 0, lock = 0, stunSum = 0, nStun = 0;
        const origHit = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul2, over){
          const before = foe2.stun;
          const r = origHit.call(m, self, foe2, hx, hy, seg, mul2, over);
          if (self === me && mul2 === undefined && mul !== 1){
            /* the blow's OWN hitstun, extended -- read as the delta this call
               made, so a stun already running from another source is not
               multiplied twice */
            const gained = foe2.stun - before;
            if (gained > 0){
              foe2.stun = before + gained * mul;
              stunSum += gained * mul; nStun++;
            }
          } else if (self === me && mul2 === undefined){
            const gained = foe2.stun - before;
            if (gained > 0){ stunSum += gained; nStun++; }
          }
          return r;
        };

        while (!m.over && step < secs / DT){
          m.step(DT); step++;
          if (th.stun > 0) lock++;
        }
        rows.push({ mul, foe: f, seed: sd, steps: step, dur: step * DT,
                    win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                    hits: me.hits, foeHits: th.hits,
                    dealt: me.dealt, taken: th.dealt,
                    destroyed: th0 - th.hp,
                    lock, stunSum, nStun });
      }
    }
  }

  w.aff = savedW.aff; delete w.onHit;
  if (savedW.onHit) w.onHit = savedW.onHit;
  for (const pid of Object.keys(saved))
    if (saved[pid].ch !== null) AC.WEAPONS.find(y => y.id === pid).ult.charge = saved[pid].ch;
  return rows;
}"""


FACTS_JS = r"""() => {
  const mm = AC.Match.prototype.move.toString();
  const f = new AC.Match("gravemourn", "aureole", 1).a;
  return {
    moveMulSrc: f.constructor.prototype.moveMul.toString(),
    moveMulFloor: (f.constructor.prototype.moveMul.toString()
                    .match(/Math\.max\(([0-9.]+)/) || [])[1],
    speedMin: AC.CONFIG.physics.speedMin,
    speedMax: AC.CONFIG.physics.speedMax,
    cruise: AC.CONFIG.physics.cruise,
    impact: Object.assign({}, AC.CONFIG.impact),
    hex: Object.assign({}, AC.STATUS.hex),
    freezeRelics: AC.WEAPONS.filter(x => x.ult && x.ult.freeze)
                            .map(x => ({ id: x.id, name: x.ult.name,
                                         freeze: x.ult.freeze, radius: x.ult.radius })),
    /* the shipped "root" locks a weapon and does not touch the ball */
    freezeSrc: /foe\.stun = Math\.max\(foe\.stun, u\.freeze\)/.test(
                 AC.Match.prototype.fireUlt.toString()),
    windows: AC.WEAPONS.filter(x => x.ult && x.ult.dur)
                       .map(x => ({ name: x.ult.name, charge: x.ult.charge, dur: x.ult.dur })),
    arena: Object.assign({}, AC.CONFIG.arena),
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw-frame.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--hold", type=float, default=2.0)
    ap.add_argument("--ch-rad", type=float, default=160.0)
    ap.add_argument("--pin-win", type=float, default=3.0)
    ap.add_argument("--only", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    want = set(a.only.split(",")) if a.only else {"1", "2", "3", "4", "5", "6"}
    gp = (HERE / a.game).resolve()
    seeds = [4301 + 23 * i for i in range(a.seeds)]
    radii = [100, 130, 160, 200, 250, 320]
    out = {}

    with game(game_path=gp) as (page, errors):
        F = page.evaluate(FACTS_JS)
        pin_ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")

        # ---------------------------------------------------------- [0] --
        print("\n[0] WHAT THE ENGINE ALREADY HAS, AND WHAT §1 ASKS FOR THAT IT "
              "DOES NOT\n")
        print(f"    ball speed          min {F['speedMin']:g}  cruise "
              f"{F['cruise']:g}  max {F['speedMax']:g}   — a ball is never still")
        print(f"    moveMul floor       {F['moveMulFloor']}  — the only movement "
              f"knob in the game bottoms out at 45%")
        print(f"    hitstun             base {F['impact']['stunBase']:g} + "
              f"{F['impact']['stunPerDmg']:g}/dmg, capped {F['impact']['stunMax']:g}, "
              f"DR {F['impact']['stunDR']:g} decaying {F['impact']['stunDRDecay']:g}")
        print(f"    hex                 {F['hex']['stunFor']:g}s every "
              f"{F['hex']['stunEvery']:g}s per stack, cap {F['hex']['maxStacks']}, "
              f"dur {F['hex']['dur']:g}s")
        print("    the shipped 'root'  "
              + ", ".join(f"{r['name']} freeze {r['freeze']:g}s r{r['radius']}"
                          for r in F["freezeRelics"]))
        print("    window ultimates    "
              + ", ".join(f"{x['name']} {x['charge']:g}/{x['dur']:g}s"
                          for x in F["windows"]))
        print(f"    arena               {F['arena']['w']:g} x {F['arena']['h']:g}")

        check("`roots for 1.6 seconds` locks a WEAPON and does not touch the "
              "ball — §1's 'unable to move (ball and weapon)' is a state this "
              "engine does not have",
              F["freezeSrc"] and float(F["moveMulFloor"]) > 0,
              "fireUlt writes `foe.stun = Math.max(foe.stun, u.freeze)` and "
              f"nothing else; `moveMul` floors at {F['moveMulFloor']} and "
              f"`speedMin` is {F['speedMin']:g}. Bramblesnare and Rootfast both "
              "say 'roots' in a tip and mean 'weapon locked'")
        out["facts"] = F

        # ------------------------------------------------------- [1][2][3] --
        if "1" in want:
            charges = [[need, drain] for need in (0.6, 0.9, 1.2, 1.6)
                       for drain in (0.0, 0.5, 1.0, 2.0)]
            rows = page.evaluate(ZONE_JS, [DONOR, FOES, seeds, a.secs, radii,
                                           pin_ids, True, charges, a.ch_rad,
                                           a.hold])
            dur = sum(r["dur"] for r in rows)
            hist = [0] * 24
            for r in rows:
                for i, v in enumerate(r["sepHist"]):
                    hist[i] += v
            tot = sum(hist) or 1
            headMax = max(r["headMax"] for r in rows)
            print(f"\n[1] WHERE THE FOE ACTUALLY IS — centre to centre, "
                  f"{len(rows)} fights, {dur:.0f}s, ultimates suppressed\n")
            print(f"    mean separation {mean(r['sep'] for r in rows):.0f}, "
                  f"closest {min(r['sepMin'] for r in rows):.0f}, furthest "
                  f"{max(r['sepMax'] for r in rows):.0f}. The head reaches "
                  f"{headMax:.0f} from the shell.\n")
            cum = 0
            for i in range(24):
                if hist[i] == 0 and cum / tot > 0.995:
                    break
                cum += hist[i]
                bar = "#" * int(round(hist[i] / tot * 200))
                print(f"    {i*50:>4}-{i*50+49:<4}{hist[i]/tot:>7.1%}  "
                      f"{cum/tot:>6.1%}  {bar}")
            out["sepHist"] = hist

            floor_r = headMax
            check("§1's own parenthesis puts a floor under `medium sized` — the "
                  "head has to be INSIDE the beams",
                  floor_r > 100,
                  f"the head reaches {headMax:.0f} units from the shell, so a "
                  f"hexagon that contains it has a circumradius of at least "
                  f"{headMax:.0f} — `medium` is bounded below before anybody "
                  f"picks a number")

            # ------------------------------------------------------ [2] --
            print(f"\n[2] CAN A DWELL TIMER EVER FIRE — continuous residence, "
                  f"episodes that were still open at the end are DROPPED\n")
            print(f"    {'shape':<8}{'radius':>7}{'share':>8}{'episodes/min':>14}"
                  f"{'mean':>8}{'p50':>7}{'p90':>7}{'max':>7}"
                  f"{'>=1.0s':>9}{'>=2.0s':>9}")
            zones = {}
            for sh in ("circ", "hex0", "hexT", "circIn"):
                for rad in radii:
                    k = f"{sh}:{rad}"
                    eps, share, opn = [], [], 0
                    for r in rows:
                        z = r["zones"][k]
                        eps += z["eps"]
                        share.append(z["share"])
                        opn += z["open"]
                    q = {"share": mean(share), "n": len(eps),
                         "perMin": len(eps) / dur * 60,
                         "mean": mean(eps), "p50": pct(eps, 0.5),
                         "p90": pct(eps, 0.9), "max": max(eps) if eps else 0,
                         "ge1": sum(1 for e in eps if e >= 1.0) / max(1, len(eps)),
                         "ge2": sum(1 for e in eps if e >= 2.0) / max(1, len(eps)),
                         "open": opn}
                    zones[k] = q
                    if sh in ("circ", "hexT"):
                        print(f"    {sh:<8}{rad:>7}{q['share']:>8.1%}"
                              f"{q['perMin']:>14.1f}{q['mean']:>8.2f}"
                              f"{q['p50']:>7.2f}{q['p90']:>7.2f}{q['max']:>7.2f}"
                              f"{q['ge1']:>9.1%}{q['ge2']:>9.1%}")
            out["zones"] = zones

            r160 = zones["hexT:160"]
            big = zones[f"hexT:{radii[-1]}"]
            check("A CONTINUOUS TWO-SECOND RESIDENCE ESSENTIALLY DOES NOT "
                  "HAPPEN — nothing in this game steers, and a ball that never "
                  "travels slower than 250 does not loiter",
                  r160["ge2"] < 0.02,
                  f"at a circumradius of 160 the median residence is "
                  f"{r160['p50']:.2f}s, the 90th is {r160['p90']:.2f}s, the "
                  f"longest of {r160['n']} is {r160['max']:.2f}s, and "
                  f"{r160['ge2']:.1%} reach two seconds. Even at "
                  f"{radii[-1]} — a zone {2*radii[-1]/F['arena']['w']:.0%} of "
                  f"the hall's width — it is {big['ge2']:.1%}")
            check("so `for too long` has to be priced in TENTHS, and the "
                  "number that makes it fire is measurable rather than "
                  "arguable",
                  zones["hexT:160"]["p90"] > 0.3,
                  "at 160: "
                  + ", ".join(
                      f"{t:g}s → "
                      f"{sum(1 for r in rows for e in r['zones']['hexT:160']['eps'] if e >= t) / dur * 60:.1f}/min"
                      for t in (0.4, 0.6, 0.8, 1.0, 1.5, 2.0)))

            # ----------------------------------------------------- [2b] --
            print(f"\n[2b] THE FORK THAT MAKES THE SENTENCE BUILDABLE — a "
                  f"CHARGE that fills while the foe is inside and bleeds while "
                  f"it is out,\n     against a continuous residence that has to "
                  f"survive unbroken. Circumradius {a.ch_rad:g}, "
                  f"{a.hold:g}s of pin per trigger.\n")
            print(f"     {'':<10}" + "".join(f"{('drain ' + format(d, 'g') + '/s'):>14}"
                                             for d in (0.0, 0.5, 1.0, 2.0)))
            fires = {}
            for need in (0.6, 0.9, 1.2, 1.6):
                cells = []
                for drain in (0.0, 0.5, 1.0, 2.0):
                    n = sum(c["fires"] for r in rows for c in r["charges"]
                            if abs(c["need"] - need) < 1e-9
                            and abs(c["drain"] - drain) < 1e-9)
                    fires[(need, drain)] = n / dur * 60
                    cells.append(f"{n / dur * 60:>14.1f}")
                print(f"     need {need:<5g}" + "".join(cells))
            print(f"\n     PINS A MINUTE, over {dur:.0f}s of fights. What a "
                  f"window actually gets is that over its own length —\n"
                  f"     Aegis holds 9s and Bloodhunt 8, and a window that "
                  f"triggers less than once is a window that does nothing:\n")
            print(f"     {'':<10}" + "".join(f"{('drain ' + format(d, 'g') + '/s'):>14}"
                                             for d in (0.0, 0.5, 1.0, 2.0)))
            for need in (0.6, 0.9, 1.2, 1.6):
                print(f"     need {need:<5g}" + "".join(
                    f"{fires[(need, d)] / 60 * 8:>13.2f}x" for d in (0.0, 0.5, 1.0, 2.0)))
            print(f"     pins in an 8-second window. The pin itself is "
                  f"{a.hold:g}s and locks out while it runs, so four is the "
                  f"ceiling.")
            out["charges"] = {f"{k[0]}/{k[1]}": v for k, v in fires.items()}

            cont2 = zones[f"hexT:{a.ch_rad:g}"]["ge2"] if f"hexT:{a.ch_rad:g}" in zones else 0
            check("THE CUMULATIVE READING FIRES AND THE CONTINUOUS ONE DOES "
                  "NOT — same words, same zone, and the difference between an "
                  "ultimate that does something and one that never triggers",
                  fires[(0.9, 0.5)] > 2.0,
                  f"at need 0.9s and a 0.5/s bleed the pin lands "
                  f"{fires[(0.9, 0.5)]:.1f} times a minute; the same zone "
                  f"produces a two-second unbroken residence "
                  f"{fires[(2.0, 0.0)] if (2.0, 0.0) in fires else 0:.1f} times "
                  f"a minute by the continuous rule. The bleed rate is the "
                  f"counterplay knob: at 2/s it is "
                  f"{fires[(0.9, 2.0)]:.1f}/min, at 0 it is "
                  f"{fires[(0.9, 0.0)]:.1f}")

            # ------------------------------------------------------ [3] --
            print(f"\n[3] IS THE HEXAGON LOAD-BEARING — one circumradius, four "
                  f"shapes\n")
            print(f"    {'radius':>7}  {'circle R':>10}{'hex, static':>13}"
                  f"{'hex, turning':>14}{'circle 0.866R':>15}"
                  f"{'hex vs circle':>15}")
            for rad in radii:
                c = zones[f"circ:{rad}"]["share"]
                h0 = zones[f"hex0:{rad}"]["share"]
                ht = zones[f"hexT:{rad}"]["share"]
                ci = zones[f"circIn:{rad}"]["share"]
                print(f"    {rad:>7}  {c:>10.1%}{h0:>13.1%}{ht:>14.1%}"
                      f"{ci:>15.1%}{(ht / c - 1) if c else 0:>+15.1%}")
            mids = [r for r in radii if 100 <= r <= 250]
            spin_gap = max(abs(zones[f"hexT:{r}"]["share"]
                               - zones[f"hex0:{r}"]["share"]) for r in mids)
            hex_gap = mean(zones[f"hexT:{r}"]["share"] / zones[f"circ:{r}"]["share"]
                           for r in mids)
            check("the hexagon is a LOOK KNOB — it covers 83% of its own "
                  "circumcircle by area and that is exactly what it collects, "
                  "and whether it turns with the weapon makes no difference at "
                  "all",
                  spin_gap < 0.02 and 0.80 < hex_gap < 0.98,
                  f"turning against static differs by at most "
                  f"{spin_gap:.2%} of the fight; the hexagon collects "
                  f"{hex_gap:.0%} of what its circumcircle does against a "
                  f"{3 * math.sqrt(3) / 2 / math.pi:.0%} area ratio. Draw it at "
                  f"whatever size reads and nothing downstream is balanced on "
                  f"the corners")

        # ---------------------------------------------------------- [4] --
        if "4" in want:
            ats = [8.0, 14.0, 20.0, 26.0, 32.0]
            print(f"\n[4] WHAT {a.hold:g} SECONDS OF PIN IS WORTH — one pin per "
                  f"fight, three arms on the identical seeds, read over the "
                  f"{a.pin_win:g}s\n    from the moment it lands. Arm 1 is what "
                  f"`u.freeze` already does; arm 2 is what §1 asks for.\n")
            arms = [("control", 0), ("weapon only", 1), ("weapon AND ball", 2)]
            print(f"    {'arm':<18}{'my blows':>10}{'foe blows':>11}"
                  f"{'dealt':>9}{'taken':>9}{'hex fires':>11}{'wasted':>9}"
                  f"{'sep at trigger':>16}{'n':>5}")
            pin = {}
            for label, mode in arms:
                rows = page.evaluate(PIN_JS, [DONOR, FOES, seeds, ats,
                                              a.pin_win, a.hold, a.secs,
                                              pin_ids, True, mode, a.ch_rad])
                rows = [r for r in rows if r["alive"]]
                n = max(1, len(rows))
                q = {"n": len(rows),
                     "hits": sum(r["hits"] for r in rows) / n,
                     "foeHits": sum(r["foeHits"] for r in rows) / n,
                     "dealt": sum(r["dealt"] for r in rows) / n,
                     "taken": sum(r["taken"] for r in rows) / n,
                     "fires": sum(r["hexFiresWin"] for r in rows) / n,
                     "firesAll": sum(r["hexFires"] for r in rows) / n,
                     "wasted": sum(r["hexWasted"] for r in rows) / n,
                     "sepAt": mean(r["sepAt"] for r in rows)}
                pin[label] = q
                print(f"    {label:<18}{q['hits']:>10.3f}{q['foeHits']:>11.3f}"
                      f"{q['dealt']:>9.2f}{q['taken']:>9.2f}"
                      f"{q['fires']:>11.2f}{q['wasted']:>9.2f}"
                      f"{q['sepAt']:>16.0f}{q['n']:>5}")
            c, w1, w2 = pin["control"], pin["weapon only"], pin["weapon AND ball"]
            check("a locked weapon stops the foe hitting back, and that much "
                  "the engine already does",
                  w1["foeHits"] < c["foeHits"] * 0.7,
                  f"foe blows {c['foeHits']:.3f} → {w1['foeHits']:.3f} over "
                  f"{a.pin_win:g}s, and damage taken {c['taken']:.2f} → "
                  f"{w1['taken']:.2f}")
            check("PINNING THE BALL AS WELL IS WHAT MAKES THE FLAIL CONNECT — "
                  "a 13-unit head against a target that has stopped moving",
                  w2["hits"] > w1["hits"] and w2["dealt"] > w1["dealt"] * 1.15,
                  f"my blows {c['hits']:.3f} control → {w1['hits']:.3f} weapon "
                  f"only → {w2['hits']:.3f} weapon and ball "
                  f"({w2['hits'] / max(1e-9, w1['hits']) - 1:+.0%}), and damage "
                  f"{c['dealt']:.2f} → {w1['dealt']:.2f} → {w2['dealt']:.2f} "
                  f"({w2['dealt'] / max(1e-9, w1['dealt']) - 1:+.0%} on the "
                  f"lock alone, {w2['dealt'] / max(1e-9, c['dealt']) - 1:+.0%} "
                  f"on nothing). Damage is the column with the sample size — "
                  f"blows in a {a.pin_win:g}s window is a count of about half "
                  f"a blow")
            check("AND THE FIRST CUT OF THIS SECTION SAID THE OPPOSITE, WHICH "
                  "IS WORTH KEEPING. It pinned at a fixed clock time wherever "
                  "the foe happened to be, and read −12%",
                  c["sepAt"] < 200,
                  f"a foe frozen at the {259:.0f} units this game averages is "
                  f"a foe a {115:.0f}-unit head cannot reach — true of a pin, "
                  f"false of THIS pin, which only ever triggers on a foe "
                  f"already inside the hexagon. Measured separation at the "
                  f"trigger: {c['sepAt']:.0f}")
            check("AND THE PIN EATS THIS CELL'S OWN CHANNEL — `f.stun` is a "
                  "Math.max, so every hex fire inside the pin is a fire that "
                  "bought nothing",
                  w2["wasted"] > 0.5 * w2["fires"] * (a.hold / a.pin_win),
                  f"{w2['wasted']:.2f} hex fires land inside each pin, against "
                  f"{c['fires']:.2f} in the same {a.pin_win:g}s of the control "
                  f"— the pin covers {a.hold / a.pin_win:.0%} of that window "
                  f"and swallows {w2['wasted'] / max(1e-9, c['fires']):.0%} of "
                  f"its fires. Roughly {w2['wasted'] / 0.29:.1f} SECONDS of "
                  f"this cell's entire channel output, per pin, silently. v39 "
                  f"5.2 from a third direction, and an argument that the "
                  f"ultimate should not also be about stacking hex")
            out["pin"] = pin

        # ---------------------------------------------------------- [5] --
        if "5" in want:
            muls = [1.0, 1.5, 2.0, 3.0]
            print(f"\n[5] WHAT `EXTRA HIT STUN` BUYS — a multiplier on THIS "
                  f"relic's own hitstun only, shipped damage, ults suppressed\n")
            print(f"    {'x hitstun':>10}{'stun/blow':>11}{'foe locked':>12}"
                  f"{'my blows/s':>12}{'foe blows/s':>13}{'hp/s':>8}"
                  f"{'taken/s':>9}{'win':>7}")
            hs = {}
            for mul in muls:
                rows = page.evaluate(HITSTUN_JS, [DONOR, FOES, seeds, a.secs,
                                                  [mul], pin_ids, True])
                dur = sum(r["dur"] for r in rows)
                steps = sum(r["steps"] for r in rows)
                wins = [r["win"] for r in rows if r["win"] >= 0]
                nS = sum(r["nStun"] for r in rows)
                q = {"stun": sum(r["stunSum"] for r in rows) / max(1, nS),
                     "lock": sum(r["lock"] for r in rows) / steps,
                     "hps": sum(r["hits"] for r in rows) / dur,
                     "foeHps": sum(r["foeHits"] for r in rows) / dur,
                     "hp": sum(r["destroyed"] for r in rows) / dur,
                     "taken": sum(r["taken"] for r in rows) / dur,
                     "win": mean(wins), "n": len(rows)}
                hs[mul] = q
                print(f"    {mul:>10.1f}{q['stun']:>11.3f}{q['lock']:>12.1%}"
                      f"{q['hps']:>12.3f}{q['foeHps']:>13.3f}{q['hp']:>8.2f}"
                      f"{q['taken']:>9.2f}{q['win']:>7.0%}")
            b, t = hs[1.0], hs[3.0]
            check("the multiplier reaches the weapon — mean hitstun per blow "
                  "moves with it",
                  t["stun"] > b["stun"] * 2.0,
                  f"{b['stun']:.3f}s a blow at 1x → {t['stun']:.3f}s at 3x. "
                  f"`stunMax` caps the RAW value before DR, and this multiplies "
                  f"after it, so the cap does not eat the knob")
            check("BUT IT IS A THIN KNOB ON THIS TYPE, BECAUSE THE TYPE LANDS "
                  "SO LITTLE — tripling the hitstun of a blow that arrives "
                  "every six seconds moves the lock by a few points",
                  (t["lock"] - b["lock"]) < 0.12,
                  f"foe locked {b['lock']:.1%} → {t['lock']:.1%} at 3x, and "
                  f"damage taken {b['taken']:.2f} → {t['taken']:.2f}/s. "
                  f"Compare flail_survey §6: holding hex at its cap takes the "
                  f"same lock from 29% to 86%")
            out["hitstun"] = hs

    if errors:
        print("\n!! page errors:")
        for e in errors[:10]:
            print("   ", e)

    bad = [n for n, ok in PASS if not ok]
    print(f"\n{len(PASS) - len(bad)}/{len(PASS)} checks passed")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
