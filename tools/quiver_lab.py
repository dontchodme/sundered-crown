#!/usr/bin/env python3
"""WHAT DOES A BOW ACTUALLY LEAVE IN THE WALLS, AND WHAT WOULD IT BE WORTH BACK?

SUPERSEDED AS A DESIGN. KEPT AS A MEASUREMENT.
    The ultimate this lab prices was designed by Claude Code, which CLAUDE.md
    §3 rule 0 now forbids, and Rick chose GLOAMWIRE / CROSSWEAVE for this cell
    instead (`06-docs/v61/gloamwire-design-v61.md`). Section [1] is untouched by
    that ruling -- it injects nothing and observes the shipped build -- and it
    is the only description anyone has written of WHERE a bow's 82% actually
    goes. Section [2] prices a mechanic that is not being built.
    `06-docs/v61/quiver-design-v61-SUPERSEDED.md`.

    python quiver_lab.py --game ../02-chain/sc-garrote.html --sn 6

Rick, 2026-09-01, choosing the umbral bow's ultimate off a priced spread:
**THE MISSES COME BACK.** The window fires nothing new -- every ordinary arrow
that ends on a wall during it stays there, and then they all come back in.

`bow_survey` has said since v40 that **82% of every arrow in this game ends on
a wall** and that the wall is worth ten times anything else on this type. What
it has never said is anything about WHERE, WHEN or HOW MANY -- and every one of
those is a design decision this ultimate cannot be built without:

  [1] THE BANK, OBSERVED. No mechanic injected, nothing changed. Every arrow
      that dies on a wall is recorded with its position, its bearing and the
      second it landed. Then:

        - a real SLIDING WINDOW over the timeline, not a mean times a
          duration. "How many arrows would an 8s window have caught" is a
          distribution and the design is priced on its shape, because a
          window that banks 4 arrows a fifth of the time is a different
          ultimate from one that always banks 16.

        - WHICH WALL. `cindercleave` found the north wall takes 3.9% of its
          tears because gravity is real and a ball spends very little of a
          fight against the roof. An arrow has `grav: 0` and flies straight,
          but it is loosed from a BALL, and the balls are on the floor. If
          the bank is a floor bank, the release comes from below and the
          picture is decided here rather than in the renderer.

        - HOW CLUMPED. A release from sixteen points spread round the hall
          and a release from sixteen points inside one metre are two
          different set-pieces with the same number attached.

  [2] THE RELEASE, INJECTED, AND ITS AIM RULE IS THE DESIGN'S ONE REAL
      CHOICE. Back the way it came, straight out of the wall, or at the
      quarry. Each is a different weapon and only the third is homing -- and
      homing is Marrowdraw's, one cell along the same row.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


# ------------------------------------------------------------- [1] the bank --
# The classification is `bow_survey [2]`'s, deliberately: a shot that vanished
# inside tickShots is attributed by asking which of the branches could have
# taken it, in the engine's own order -- parried, hit, popped, expired, walled.
# The parry tag is an fx signature collected only while inside tickShots, so it
# cannot be borrowed by another system without this probe seeing an unmatched
# event. What is NEW here is that a wall death is not counted, it is RECORDED.

BANK_JS = r"""([shooter, foes, seeds, secs, noult, pinIds]) => {
  const DT = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena;

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { ch: x.ult ? x.ult.charge : null };
    if (noult && x.ult) x.ult.charge = 1e9;
  }

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      /* the hit tag, so a landed arrow is never miscounted as a wall arrow */
      const origResolve = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const s = m._cineShot;
        if (s) s._pHit = true;
        return origResolve.apply(m, arguments);
      };

      let inShots = false;
      const parryFx = [];
      const origFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, life, size, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) parryFx.push(x + "," + y);
        return origFx.apply(m, arguments);
      };

      const bank = [];          // every wall death, in order
      let fired = 0, hit = 0, parried = 0, walled = 0, other = 0, unknown = 0;
      const origSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, ang){ if (fg === me) fired++; return origSpawn.apply(m, arguments); };

      const origTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice();
        parryFx.length = 0;
        inShots = true;
        const r = origTick.apply(m, arguments);
        inShots = false;
        if (pre.length){
          const live = new Set(m.shots);
          const n = m.inset;
          const P = new Set(parryFx);
          for (const s of pre){
            if (live.has(s)) continue;
            const mine = s.own === (me === m.a ? "a" : "b");
            const onWall = s.x < n + s.r || s.x > A.w - n - s.r
                        || s.y < n + s.r || s.y > A.h - n - s.r;
            if (P.has(s.x + "," + s.y)){ if (mine) parried++; continue; }
            if (s._pHit){ if (mine) hit++; continue; }
            if (s.shard && s.life <= 0){ if (mine) other++; continue; }
            if (s.life <= 0){ if (mine) other++; continue; }
            if (onWall){
              if (mine){
                walled++;
                /* WHICH WALL is asked of the position, in the engine's own
                   order of tests, and the ambiguous corner is recorded as a
                   corner rather than silently assigned to whichever branch
                   ran first. */
                const w = [];
                if (s.x < n + s.r) w.push("W");
                if (s.x > A.w - n - s.r) w.push("E");
                if (s.y < n + s.r) w.push("N");
                if (s.y > A.h - n - s.r) w.push("S");
                bank.push({ t: m.t, x: s.x, y: s.y,
                            vx: s.vx, vy: s.vy,
                            side: w.length === 1 ? w[0] : "corner",
                            /* the separation at the moment it landed: a
                               release is only worth what it can reach */
                            sep: Math.hypot(th.x - s.x, th.y - s.y),
                            inset: n });
              }
              continue;
            }
            if (mine) unknown++;
          }
        }
        return r;
      };

      let steps = 0;
      while (!m.over && steps < secs / DT) { m.step(DT); steps++; }

      rows.push({ foe: f, seed: sd, dur: steps * DT, over: m.over,
                  fired, hit, parried, walled, other, unknown,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  bank });
    }
  }

  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return { rows, arena: { w: A.w, h: A.h } };
}"""


# --------------------------------------------------------- [2] the release --
# THE AIM RULE IS THE ONE REAL CHOICE IN THIS DESIGN and it is three different
# weapons, so it is measured as a PER-ARROW rate rather than as a win rate.
# `grab_lab`'s lesson one relic along: find the scalar the ultimate is made of
# and tune on that, because it is thirty times cheaper than the thing it adds
# up to and it is what the win rate is made OF.
#
#   back    the arrow returns along its own flight, reversed. It goes back
#           towards where the archer was STANDING when it was loosed, which is
#           not where anybody is now.
#   normal  straight out of the wall into the room. The hall becomes the
#           shooter and the volley converges from all four sides.
#   aimed   committed at the quarry's position at the instant of release, and
#           never revised -- Reprisal's rule, not Marrowdraw's. NOT homing:
#           homing is the bloodsworn bow, one cell along the same row.
#
# THE HALL CLOSES WHILE THE QUIVER FILLS, and that is not a detail. `collapse`
# runs at 4.2 units/s from 21s, so a wall travels 33.6 units across an 8s
# window against an arrow radius of 24: a quill banked at the top of a window
# is OUTSIDE the room by the time it is released. Released quills are pushed
# back inside the current wall line and the number that had to be is counted,
# because "the hall ate the quiver" is a mechanic if it is measured and a bug
# if it is not.

RELEASE_JS = r"""([shooter, foes, seeds, secs, arm, win, charge, dmgMul, pinIds, chan, fieldUlts]) => {
  const DT = AC.CONFIG.physics.dt;
  const A  = AC.CONFIG.arena;

  const saved = {};
  for (const pid of pinIds){
    const x = AC.WEAPONS.find(y => y.id === pid); if (!x) continue;
    saved[pid] = { ch: x.ult ? x.ult.charge : null,
                   onHit: x.onHit ? JSON.parse(JSON.stringify(x.onHit)) : null };
    /* TWO WORLDS, AND THEY ARE NOT THE SAME WORLD. `row_price` -- and every
       cell price in this project's history -- runs with EVERY ultimate off,
       which is where the +15.6 that chose this cell was measured. `ult_price`
       runs with every ultimate ON except the one it is deleting, which is
       where the field median of +20.4 was measured. A number from one is not
       a number from the other (v60 §3: the floors move 13-22 points), so this
       lab can stand in either and says which in its own header. The shooter's
       OWN ultimate is off in both: the injected window replaces it. */
    if (x.ult && (!fieldUlts || pid === shooter)) x.ult.charge = 1e9;
  }
  /* THE BODY IS THE CELL, not the donor. `row_price` prices umbral x bow as
     Ironhail carrying curse, and this has to be the same body or the arms
     below are not comparable with the price that chose the cell. */
  const SH = AC.WEAPONS.find(y => y.id === shooter);
  const shOnHit = SH.onHit ? JSON.parse(JSON.stringify(SH.onHit)) : null;
  if (chan){ SH.onHit = JSON.parse(chan); } else { delete SH.onHit; }

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(shooter, f, sd);
      const me = m.a.w.id === shooter ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const own = me === m.a ? "a" : "b";
      const S = me.w.shot;

      const origResolve = AC.Match.prototype.resolveHit;
      let qDmg = 0, qHits = 0;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const s = m._cineShot;
        if (s) s._pHit = true;
        const d0 = self.dealt;
        const r = origResolve.apply(m, arguments);
        if (s && s._quill && self === me){ qDmg += self.dealt - d0; qHits++; }
        return r;
      };

      let inShots = false;
      const parryFx = [];
      const origFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n, spd, life, size, dx, dy){
        if (inShots && col === "#FFF4D0" && n === 9 && spd === 240) parryFx.push(x + "," + y);
        return origFx.apply(m, arguments);
      };

      /* our own window, on our own clock. `f.charge` is the engine's and it is
         pure wall time; this mimics it exactly rather than reading it, so the
         floor arm and every release arm see the same fight up to the cast. */
      let cg = 0, open = 0, casts = 0, quiver = [];
      let banked = 0, released = 0, qParried = 0, qWalled = 0;
      /* HOW FAR THE WALL MOVED, not whether it moved. The first cut of this
         counted a boolean and reported 100% on every arm -- because a spent
         arrow's centre is already inside `n + r` by construction, so the
         release margin nudges every quill by a few units and the boolean
         could never read anything else. What the design actually wants to
         know is whether the COLLAPSE swallowed the quiver, which is a
         distance. */
      const push = [], creep = [];

      const origTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice();
        parryFx.length = 0;
        inShots = true;
        const r = origTick.apply(m, arguments);
        inShots = false;
        if (pre.length){
          const live = new Set(m.shots);
          const n = m.inset;
          const P = new Set(parryFx);
          for (const s of pre){
            if (live.has(s)) continue;
            const mine = s.own === own;
            const onWall = s.x < n + s.r || s.x > A.w - n - s.r
                        || s.y < n + s.r || s.y > A.h - n - s.r;
            if (P.has(s.x + "," + s.y)){ if (mine && s._quill) qParried++; continue; }
            if (s._pHit) continue;
            if (s.life <= 0) continue;
            if (onWall && mine){
              if (s._quill){ qWalled++; continue; }   // a quill is spent once
              if (open > 0 && arm !== "none"){
                const w = [];
                if (s.x < n + s.r) w.push(1, 0);
                else if (s.x > A.w - n - s.r) w.push(-1, 0);
                else w.push(0, 0);
                if (s.y < n + s.r) { w[1] = 1; }
                else if (s.y > A.h - n - s.r) { w[1] = -1; }
                const nl = Math.hypot(w[0], w[1]) || 1;
                quiver.push({ x: s.x, y: s.y, vx: s.vx, vy: s.vy,
                              nx: w[0] / nl, ny: w[1] / nl, n0: n });
                banked++;
              }
            }
          }
        }
        return r;
      };

      let steps = 0;
      while (!m.over && steps < secs / DT){
        /* the cast. Charge is wall time in this engine and it does NOT stop
           while a window runs -- 25 of 28 relics behave that way (open item
           30), so the lab behaves that way too. */
        if (me.alive) cg += DT;
        if (open <= 0 && cg >= charge){ cg = 0; open = win; casts++; quiver.length = 0; }
        else if (open > 0){
          open -= DT;
          if (open <= 0 && quiver.length){
            /* THE RELEASE. Every quill at once, from where it stuck. */
            const n = m.inset, R = AC.CONFIG.physics.ballR;
            for (const q of quiver){
              let px = q.x, py = q.y;
              const lo = n + S.r + 2;
              const cx = Math.min(Math.max(px, lo), A.w - lo);
              const cy = Math.min(Math.max(py, lo), A.h - lo);
              push.push(Math.hypot(cx - px, cy - py));
              /* THE COLLAPSE ALONE. How much wall arrived between the arrow
                 sticking and the quiver loosing, in units, per quill. */
              creep.push(n - q.n0);
              px = cx; py = cy;
              let ax;
              if (arm === "back")        ax = Math.atan2(-q.vy, -q.vx);
              else if (arm === "normal") ax = Math.atan2(q.ny, q.nx);
              else                       ax = Math.atan2(th.y - py, th.x - px);
              if (m.shots.length >= AC.CONFIG.shot.maxLive) m.shots.shift();
              m.shots.push({
                own, x: px, y: py, x0: px, y0: py, spd0: 0, t0: m.t,
                vx: Math.cos(ax) * S.speed, vy: Math.sin(ax) * S.speed,
                r: S.r, life: S.life, max: S.life, grav: 0,
                dmgMul: dmgMul, aff: me.aff, a: ax, _quill: true });
              released++;
            }
            quiver.length = 0;
          }
        }
        m.step(DT); steps++;
      }

      rows.push({ foe: f, seed: sd, dur: steps * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, banked, released,
                  /* THE LAST WINDOW. A fight that ends while a window is open
                     never reaches its own release, so its quiver is stranded
                     rather than lost. Reported, so `banked` balances. */
                  stranded: quiver.length,
                  push: push.reduce((x, y) => x + y, 0) / (push.length || 1),
                  pushMax: push.length ? Math.max.apply(null, push) : 0,
                  pushBig: push.filter(d => d > 6).length,
                  creep: creep.reduce((x, y) => x + y, 0) / (creep.length || 1),
                  creepMax: creep.length ? Math.max.apply(null, creep) : 0,
                  creepEat: creep.filter(d => d > 24).length,
                  qHits, qDmg, qParried, qWalled,
                  dealt: me.dealt, taken: th.dealt });
    }
  }

  if (shOnHit) SH.onHit = shOnHit; else delete SH.onHit;
  for (const pid of Object.keys(saved)){
    const x = AC.WEAPONS.find(y => y.id === pid);
    if (saved[pid].ch !== null) x.ult.charge = saved[pid].ch;
  }
  return rows;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-garrote.html")
    ap.add_argument("--shooter", default="ironhail")
    ap.add_argument("--sn", type=int, default=6, help="seeds per foe")
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--window", type=float, default=8.0, help="the candidate ult window")
    ap.add_argument("--charge", type=float, default=15.0)
    ap.add_argument("--dmg-mul", type=float, default=1.0)
    ap.add_argument("--arms", default="none,back,normal,aimed",
                    help="which release arms [2] runs; `none` is the floor")
    ap.add_argument("--field-ults", action="store_true",
                    help="leave the REST of the roster its ultimates -- "
                         "`ult_price`'s world, and the one the relic ships into")
    ap.add_argument("--dmgs", default="", help="sweep dmgMul on one aim rule")
    ap.add_argument("--aim", default="back", help="the aim rule --dmgs sweeps")
    ap.add_argument("--only", default="1,2", help="sections to run")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    only = set(a.only.split(","))
    arm_list = a.arms.split(",")
    # (label, aim rule, dmgMul). `--dmgs` turns the aim-rule sweep into a
    # WEIGHT sweep on one rule, so the floor is paid for once instead of once
    # per point -- the same fights, the same seeds, one arm varying.
    if a.dmgs:
        runs = [("none", "none", 1.0)] + [
            (f"{a.aim[:4]}@{d}", a.aim, float(d)) for d in a.dmgs.split(",")]
    else:
        runs = [(k, k, a.dmg_mul) for k in arm_list]
    arm_list = [r[0] for r in runs]

    gp = resolve_game(a.game)
    seeds = [3301 + 13 * i for i in range(a.sn)]

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id: w.id, shape: w.shape, aff: w.aff}))")
        foes = [w["id"] for w in W if w["shape"] != "bow"]
        pin_ids = [w["id"] for w in W]

        print(f"\nQUIVER LAB -- {gp.name}, shooter {a.shooter}, "
              f"{len(foes)} foes x {len(seeds)} seeds, ults suppressed\n")

        counts, sides, spreads, seps, arms = [], {}, [], [], {}

        # ------------------------------------------------------------ [1] --
        if "1" in only:
            out = page.evaluate(BANK_JS, [a.shooter, foes, seeds, a.secs, True, pin_ids])
            rows, arena = out["rows"], out["arena"]
            assert not errors, errors[:4]

            fired = sum(r["fired"] for r in rows)
            walled = sum(r["walled"] for r in rows)
            landed = sum(r["hit"] for r in rows)
            parried = sum(r["parried"] for r in rows)
            unknown = sum(r["unknown"] for r in rows)
            dur = sum(r["dur"] for r in rows)

            print(f"[1] THE BANK -- {len(rows)} fights, {dur:.0f}s of fighting, "
                  f"{fired} arrows loosed\n")
            print(f"    landed {landed / fired:6.1%}   parried {parried / fired:6.1%}   "
                  f"WALL {walled / fired:6.1%}   unclassified {unknown}")
            check("the ledger reproduces bow_survey -- the wall takes ~82%",
                  0.78 <= walled / fired <= 0.86 and unknown == 0,
                  f"{walled / fired:.1%} on the wall, {unknown} unclassified")

            # --- the sliding window. The design's headline number, as a shape.
            counts = []
            for r in rows:
                ts = [b["t"] for b in r["bank"]]
                if not ts:
                    counts.append(0)
                    continue
                # every window START that a cast could actually have, at 0.25s
                # resolution across the fight the archer was alive for
                k = 0
                step = 0.25
                t0 = 0.0
                while t0 + a.window <= r["dur"]:
                    k = sum(1 for t in ts if t0 <= t < t0 + a.window)
                    counts.append(k)
                    t0 += step
            counts.sort()

            def pct(p):
                return counts[min(len(counts) - 1, int(p * len(counts)))] if counts else 0

            print(f"\n    A {a.window:.0f}s WINDOW, over {len(counts)} window positions "
                  f"at 0.25s resolution:\n")
            print(f"    {'min':>6}{'p10':>6}{'p25':>6}{'median':>8}{'p75':>6}{'p90':>6}"
                  f"{'max':>6}{'mean':>8}")
            print(f"    {counts[0]:>6}{pct(.10):>6}{pct(.25):>6}{pct(.50):>8}"
                  f"{pct(.75):>6}{pct(.90):>6}{counts[-1]:>6}{mean(counts):>8.1f}")
            zero = sum(1 for c in counts if c == 0) / max(1, len(counts))
            print(f"\n    a window that banks NOTHING: {zero:.1%} of positions")

            # --- which wall
            sides = {}
            for r in rows:
                for b in r["bank"]:
                    sides[b["side"]] = sides.get(b["side"], 0) + 1
            tot = sum(sides.values()) or 1
            print(f"\n    WHICH WALL -- arena {arena['w']}x{arena['h']}, "
                  f"so N and S are the SHORT walls\n")
            for s in ["N", "S", "E", "W", "corner"]:
                n = sides.get(s, 0)
                name = {"N": "N (roof)", "S": "S (floor)", "E": "E", "W": "W",
                        "corner": "corner"}[s]
                print(f"    {name:<12}{n:>7}{n / tot:>9.1%}")

            # --- how clumped: pairwise distance between banked arrows inside one
            #     window, against the distance you would get from points spread
            #     evenly round the perimeter.
            per = 2 * (arena["w"] + arena["h"])
            spreads = []
            for r in rows:
                ts = [(b["t"], b["x"], b["y"]) for b in r["bank"]]
                t0 = 0.0
                while t0 + a.window <= r["dur"]:
                    grp = [(x, y) for (t, x, y) in ts if t0 <= t < t0 + a.window]
                    if len(grp) >= 4:
                        d = [math.hypot(grp[i][0] - grp[j][0], grp[i][1] - grp[j][1])
                             for i in range(len(grp)) for j in range(i + 1, len(grp))]
                        spreads.append(mean(d))
                    t0 += a.window          # non-overlapping, so windows are independent
            print(f"\n    HOW CLUMPED -- mean pairwise distance between the arrows "
                  f"banked in one window\n")
            if spreads:
                spreads.sort()
                print(f"    median {statistics.median(spreads):.0f} units over "
                      f"{len(spreads)} windows of 4+ arrows      "
                      f"p10 {spreads[int(.10 * len(spreads))]:.0f}   "
                      f"p90 {spreads[int(.90 * len(spreads))]:.0f}")
                print(f"    for scale: the hall is {arena['w']}x{arena['h']}, "
                      f"perimeter {per}, and its own diagonal is "
                      f"{math.hypot(arena['w'], arena['h']):.0f}")

            # --- how far the quarry was, when each arrow landed. A release is only
            #     worth what it can reach, and this is the number that decides
            #     whether the aim rule matters at all.
            seps = sorted(b["sep"] for r in rows for b in r["bank"])
            if seps:
                print(f"\n    HOW FAR THE QUARRY WAS from each banked arrow, at the "
                      f"moment it stuck:\n")
                print(f"    {'p10':>6}{'p25':>6}{'median':>8}{'p75':>6}{'p90':>6}")
                print(f"    {seps[int(.10*len(seps))]:>6.0f}"
                      f"{seps[int(.25*len(seps))]:>6.0f}"
                      f"{statistics.median(seps):>8.0f}"
                      f"{seps[int(.75*len(seps))]:>6.0f}"
                      f"{seps[int(.90*len(seps))]:>6.0f}")

            check("a window banks enough arrows to be an ultimate at all",
                  pct(.50) >= 6, f"median {pct(.50)} arrows in {a.window:.0f}s")
            check("the bank is not a corner case -- most windows carry a volley",
                  zero < 0.05, f"{zero:.1%} of windows bank nothing")

        # ------------------------------------------------------------ [2] --
        if "2" in only:
            print(f"\n[2] THE RELEASE -- {len(foes)} foes x {len(seeds)} seeds an arm, "
                  f"window {a.window:.0f}s, charge {a.charge:.0f}s, "
                  f"dmgMul {a.dmg_mul:g}\n"
                  f"    The body is {a.shooter} carrying CURSE -- the cell as "
                  f"`row_price` priced it, and\n"
                  f"    {'ONLY ITS OWN ultimate is off -- the field keeps theirs' if a.field_ults else 'every ultimate in the roster is off, its own included'},"
                  f" so the release is priced in "
                  f"{'ult_price' if a.field_ults else 'row_price'}'s world.")
            print("")
            print(f"    {'arm':<9}{'win%':>7}{'casts':>7}{'banked':>8}{'/cast':>7}"
                  f"{'rel':>6}{'strand':>7}{'hits':>7}{'HIT RATE':>10}"
                  f"{'parried':>9}{'quill dmg':>11}{'dealt':>8}")
            for label, arm, dmg in runs:
                rs = page.evaluate(RELEASE_JS,
                                   [a.shooter, foes, seeds, a.secs, arm, a.window,
                                    a.charge, dmg, pin_ids,
                                    json.dumps({"curse": 1}), a.field_ults])
                assert not errors, errors[:4]
                n = len(rs)
                wins = sum(1 for r in rs if r["win"] == 1)
                casts = sum(r["casts"] for r in rs)
                bk = sum(r["banked"] for r in rs)
                rel = sum(r["released"] for r in rs)
                st = sum(r["stranded"] for r in rs)
                pu = mean(r["push"] for r in rs if r["released"])
                pb = sum(r["pushBig"] for r in rs)
                cr = mean(r["creep"] for r in rs if r["released"])
                cx = max((r["creepMax"] for r in rs), default=0)
                ce = sum(r["creepEat"] for r in rs)
                hh = sum(r["qHits"] for r in rs)
                pp = sum(r["qParried"] for r in rs)
                dd = sum(r["qDmg"] for r in rs)
                dealt = mean(r["dealt"] for r in rs)
                arms[label] = {"n": n, "win": wins / n, "casts": casts, "banked": bk,
                             "released": rel, "stranded": st, "push": pu,
                             "pushBig": pb, "creep": cr, "creepMax": cx,
                             "creepEat": ce, "hits": hh,
                             "parried": pp, "qDmg": dd, "dealt": dealt}
                print(f"    {label:<9}{wins / n:>7.1%}{casts:>7}{bk:>8}"
                      f"{(bk / casts if casts else 0):>7.1f}{rel:>6}{st:>7}{hh:>7}"
                      f"{(hh / rel if rel else 0):>10.1%}"
                      f"{(pp / rel if rel else 0):>9.1%}{dd:>11.0f}{dealt:>8.0f}")

            print("")
            live = [k for k in arm_list if k != "none"]
            print(f"    THE COLLAPSE, and it is NOT the release margin. The wall "
                  f"arrives a mean")
            print(f"    {mean(arms[k]['creep'] for k in live):.1f} units between an "
                  f"arrow sticking and its quiver loosing, worst "
                  f"{max(arms[k]['creepMax'] for k in live):.0f} -- and "
                  f"{sum(arms[k]['creepEat'] for k in live)} of "
                  f"{sum(arms[k]['released'] for k in live)} quills "
                  f"({sum(arms[k]['creepEat'] for k in live) / max(1, sum(arms[k]['released'] for k in live)):.1%}) "
                  f"were swallowed")
            print(f"    outright -- the hall closed by more than an arrow radius "
                  f"on top of them. The release")
            print(f"    margin moves every quill {mean(arms[k]['push'] for k in live):.0f} "
                  f"units on average and that number is the PROBE, not the hall.")

            f0 = arms["none"]
            print(f"\n    THE FLOOR is the `none` arm: the same body, the same "
                  f"window opening and closing,\n"
                  f"    and nothing coming out of it. Every lift below is against "
                  f"{f0['win']:.1%}.\n")
            for arm in [k for k in arm_list if k != "none"]:
                r = arms[arm]
                print(f"    {arm:<9}{r['win'] - f0['win']:>+7.1%}   "
                      f"quill damage {r['qDmg'] / max(1, r['n']):.0f} a fight, "
                      f"{r['hits'] / max(1, r['casts']):.1f} quill hits a cast")

            check("the floor arm is inert -- the instrument banks and releases "
                  "nothing when the mechanic is off",
                  arms["none"]["banked"] == 0 and arms["none"]["released"] == 0
                  and arms["none"]["hits"] == 0,
                  f"banked {arms['none']['banked']}, released "
                  f"{arms['none']['released']}, hits {arms['none']['hits']}")
            check("every banked arrow is accounted for -- released, or stranded "
                  "in a window the fight ended inside",
                  all(arms[k]["banked"] == arms[k]["released"] + arms[k]["stranded"]
                      for k in arm_list if k != "none"),
                  "; ".join(f"{k} {arms[k]['banked']} = {arms[k]['released']}"
                            f"+{arms[k]['stranded']}"
                            for k in arm_list if k != "none"))
            check("a quill hits far harder than the arrow that banked it -- "
                  "otherwise this ultimate is a re-roll of a 8% shot",
                  min(arms[k]["hits"] / max(1, arms[k]["released"])
                      for k in arm_list if k != "none") > 0.084,
                  "; ".join(f"{k} {arms[k]['hits'] / max(1, arms[k]['released']):.1%}"
                            for k in arm_list if k != "none"))

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"window": a.window, "counts": counts, "sides": sides,
             "spreads": spreads, "seps": seps[::7], "arms": arms},
            indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
