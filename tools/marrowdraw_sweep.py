#!/usr/bin/env python3
"""SOLVE THE BALLISTA WINDOW. cadence against damage, then the forks.

    python3 marrowdraw_sweep.py --game ../02-chain/sc-marrowdraw.html

THE PAIR IS NOT SEPARABLE and that is the whole reason this file exists.
`cadMul` 3.0 fires a third as many shots, so `dmgMul` 2.2 is a THIRTY PERCENT
DPS CUT bought back by the landed rate -- and the landed rate is itself a
function of how long each bolt is in the air. Sweeping either alone measures
the other one's setting.

EVERY CELL BISECTS `dmg` FIRST. v40's rule: a share measured against a blade
that is not the shipping blade is a statement about the blade. A window that
looks like 40% of a relic's damage at dmg 15 may be 25% of it at the dmg that
makes the relic even, and the second number is the one that means something.

AND THE BISECTION IS AGAINST THE WHOLE FIELD. v41 open decision 2, closed the
expensive way: Bulwarden's dmg was bisected on a five-foe subset that read 50%
and the full 253 pairings read 55.2% on the same number -- five points, three
full passes to find. Every win rate here is all 23 opponents.

  [1] THE BASELINE. The relic with the window suppressed, so every share
      below has something to be a share OF.
  [2] cadMul x dmgMul, dmg bisected per cell. The grid the design lives in.
  [3] THE FORKS, at the chosen pair: forkHome, forkDmg, forkBleed.
  [4] THE FINAL BISECTION, at the chosen numbers, wider.

INJECTION IS RUNTIME-ONLY. Nothing is written to any build; the chosen numbers
go back into `marrowdraw_build.py`'s ULT dict by hand, which is the only place
this project keeps a tuned number.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "marrowdraw"

# The relic's own win rate is every pairing it is in. There is no subset here
# and there is not going to be one.
WIN_JS = r"""([id, dmg, ult, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  for (const foe of ids){
    for (let k = 0; k < n; k++){
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const r = AC.simulate(id, foe, s);
      if (r.winner === w.name) win++;
      games++; dur += r.duration;
      if (r.reason !== "slain") timeouts++;
    }
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return { win, games, rate: win / games, dur: dur / games, timeouts };
}"""

# Telemetry. Wrappers on the match instance, `bow_survey`'s parry tag, and the
# window's own counters, which the build already keeps.
TEL_JS = r"""([id, dmg, ult, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(id, f, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const side = me === m.a ? "a" : "b";

      /* Damage is split at the SOURCE, because "what is the window worth" is
         the only question this file asks and an ultimate that changes what
         the ORDINARY shot does cannot be priced by counting casts. */
      let dBolt = 0, dFork = 0, dArrow = 0, dMelee = 0, dAll = 0;
      let hBolt = 0, hFork = 0;
      const oRes = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
        const s = m._cineShot, d0b = self.dealt;
        const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
        const dd = self.dealt - d0b;
        if (self === me){
          dAll += dd;
          if (s && s.fork){ dFork += dd; hFork++; }
          else if (s && s.bal){ dBolt += dd; hBolt++; }
          else if (s){ dArrow += dd; }
          else dMelee += dd;
          if (s) s._ph = true;
        }
        return r;
      };

      let fired = 0, boltsFired = 0;
      const oSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, ang){
        const r = oSpawn.call(m, fg, ang);
        if (fg === me){ fired++;
          const s = m.shots[m.shots.length - 1];
          if (s && s.bal) boltsFired++; }
        return r;
      };

      let inShots = false;
      const parryFx = [];
      const oFx = AC.Match.prototype.spawnFx;
      m.spawnFx = function(x, y, col, n2, spd, life, size, dx, dy){
        if (inShots && col === "#FFF4D0" && n2 === 9 && spd === 240)
          parryFx.push(x + "," + y);
        return oFx.call(m, x, y, col, n2, spd, life, size, dx, dy);
      };

      const T = { bParried:0, bWall:0, fParried:0, fWall:0, aParried:0, aWall:0 };
      const oTick = AC.Match.prototype.tickShots;
      m.tickShots = function(dt){
        const pre = m.shots.slice();
        parryFx.length = 0; inShots = true;
        const r = oTick.call(m, dt);
        inShots = false;
        if (pre.length){
          const live = new Set(m.shots), n2 = m.inset, P = new Set(parryFx);
          for (const s of pre){
            if (live.has(s) || s.own !== side || s._ph) continue;
            const parried = P.has(s.x + "," + s.y);
            const spent = s.life <= 0 || s.x < n2 + s.r || s.x > A.w - n2 - s.r
                                      || s.y < n2 + s.r || s.y > A.h - n2 - s.r;
            const k = s.fork ? "f" : s.bal ? "b" : "a";
            if (parried) T[k + "Parried"]++;
            else if (spent) T[k + "Wall"]++;
          }
        }
        return r;
      };

      let steps = 0, casts = 0, up = 0, wasUp = false, forks = 0;
      while (!m.over && steps < secs / DT){
        m.step(DT); steps++;
        const B = me.ultBal;
        if (B){ up++; if (!wasUp) casts++; forks = Math.max(forks, B.forks); }
        wasUp = !!B;
      }
      rows.push({ foe: f, seed: sd, dur: steps * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, upFrac: steps ? up / steps : 0,
                  fired, boltsFired, hBolt, hFork,
                  dBolt, dFork, dArrow, dMelee, dAll,
                  ultsFired: me.ultsFired, ...T });
    }
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return rows;
}"""

ROSTER_JS = """() => JSON.stringify(AC.WEAPONS.map(w => ({
  id: w.id, dmg: w.dmg, ult: w.ult || null })))"""


def bisect(page, ult, n, lo, hi, steps, seed=20260821, target=0.50, quiet=False):
    """Find the `dmg` at which the relic is even against the WHOLE field."""
    best = None
    for i in range(steps):
        mid = (lo + hi) / 2
        r = page.evaluate(WIN_JS, [RID, mid, ult, n, seed + i])
        if not quiet:
            print(f"      dmg {mid:6.2f}  ->  {r['rate']:6.1%}  "
                  f"({r['win']}/{r['games']}, mean {r['dur']:.1f}s, "
                  f"{r['timeouts']} timeouts)")
        if best is None or abs(r["rate"] - target) < abs(best[1] - target):
            best = (mid, r["rate"], r)
        if r["rate"] > target:
            hi = mid
        else:
            lo = mid
    return best


def agg(rows):
    n = len(rows)
    tot = lambda k: sum(r[k] for r in rows)          # noqa: E731
    dAll = tot("dAll") or 1
    bf = tot("boltsFired") or 1
    return dict(
        casts=tot("casts") / n,
        boltsPerCast=bf / max(1, tot("casts")),
        boltLanded=tot("hBolt") / bf,
        boltParried=tot("bParried") / bf,
        boltWall=tot("bWall") / bf,
        forkPerBolt=tot("hFork") / max(1, tot("hBolt")),
        windowShare=(tot("dBolt") + tot("dFork")) / dAll,
        boltShare=tot("dBolt") / dAll,
        forkShare=tot("dFork") / dAll,
        arrowShare=tot("dArrow") / dAll,
        meleeShare=tot("dMelee") / dAll,
        dur=statistics.mean(r["dur"] for r in rows),
        win=statistics.mean(r["win"] for r in rows),
        upFrac=statistics.mean(r["upFrac"] for r in rows),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--n", type=int, default=14, help="seeds per pairing, bisection")
    ap.add_argument("--nfinal", type=int, default=40)
    ap.add_argument("--steps", type=int, default=6)
    ap.add_argument("--seeds", type=int, default=5, help="seeds per foe, telemetry")
    ap.add_argument("--secs", type=float, default=90.0)
    ap.add_argument("--phase", default="1,2,3,4")
    ap.add_argument("--json", default="../05-reference/v42/marrowdraw-sweep.json")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [7717 + i * 613 for i in range(a.seeds)]
    phases = set(a.phase.split(","))
    out = {}

    with game(game_path=gp) as (page, errors):
        before = json.loads(page.evaluate(ROSTER_JS))
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, shape:w.shape}))")
        assert any(w["id"] == RID for w in W), f"{RID} is not in this build"
        base_ult = page.evaluate(
            f"() => JSON.parse(JSON.stringify(AC.WEAPONS.find(w=>w.id==='{RID}').ult))")
        base_dmg = page.evaluate(
            f"() => AC.WEAPONS.find(w=>w.id==='{RID}').dmg")
        by_shape = {}
        for w in W:
            if w["id"] != RID:
                by_shape.setdefault(w["shape"], []).append(w["id"])
        foes = [ids[0] for ids in by_shape.values()]

        print(f"\nMARROWDRAW SWEEP — {len(W)} relics, {len(W)-1} opponents\n"
              f"  bisection {a.n} seeds x {len(W)-1} pairings = "
              f"{a.n*(len(W)-1)} fights a step, {a.steps} steps\n"
              f"  telemetry {len(foes)} foes x {len(seeds)} seeds  "
              f"({', '.join(foes)})\n"
              f"  shipping placeholder: dmg {base_dmg}  cadMul "
              f"{base_ult['cadMul']}  dmgMul {base_ult['dmgMul']}")

        # ------------------------------------------------------------ [1] --
        if "1" in phases:
            print("\n[1] THE BASELINE — the window suppressed, so the shares below "
                  "have something to be shares OF\n")
            off = dict(base_ult); off["charge"] = 1e9
            d, rate, _ = bisect(page, off, a.n, 8.0, 26.0, a.steps)
            rows = page.evaluate(TEL_JS, [RID, d, off, foes, seeds, a.secs])
            g = agg(rows)
            print(f"\n    with NO ultimate the relic is even at dmg {d:.2f} "
                  f"({rate:.1%})")
            print(f"    arrow {g['arrowShare']:.1%} of its damage, "
                  f"melee {g['meleeShare']:.1%}, mean fight {g['dur']:.1f}s")
            out["baseline"] = {"dmg": d, "rate": rate, **g}

        # ------------------------------------------------------------ [2] --
        if "2" in phases:
            print("\n[2] cadMul x dmgMul — `dmg` BISECTED IN EVERY CELL against all "
                  f"{len(W)-1} opponents\n")
            print(f"    {'cadMul':>7}{'dmgMul':>8}{'dmg':>7}{'win':>8}"
                  f"{'bolts/cast':>12}{'landed':>8}{'parried':>9}{'wall':>7}"
                  f"{'forks/hit':>11}{'window':>8}{'ttk':>7}")
            grid = {}
            for cad in [2.0, 3.0, 4.0]:
                for dm in [1.6, 2.2, 3.0, 4.0]:
                    u = dict(base_ult); u["cadMul"] = cad; u["dmgMul"] = dm
                    d, rate, _ = bisect(page, u, a.n, 8.0, 26.0, a.steps, quiet=True)
                    rows = page.evaluate(TEL_JS, [RID, d, u, foes, seeds, a.secs])
                    g = agg(rows)
                    grid[f"{cad}|{dm}"] = {"dmg": d, "rate": rate, **g}
                    print(f"    {cad:>7.1f}{dm:>8.1f}{d:>7.2f}{rate:>8.1%}"
                          f"{g['boltsPerCast']:>12.1f}{g['boltLanded']:>8.1%}"
                          f"{g['boltParried']:>9.1%}{g['boltWall']:>7.1%}"
                          f"{g['forkPerBolt']:>11.2f}{g['windowShare']:>8.1%}"
                          f"{g['dur']:>7.1f}")
            out["grid"] = grid

        # ------------------------------------------------------------ [3] --
        if "3" in phases:
            print("\n[3] THE FORKS — at the shipping pair, `dmg` bisected per cell\n")
            print(f"    {'forkHome':>9}{'forkDmg':>9}{'fork bl':>9}"
                  f"{'bolt bl':>9}{'dmg':>7}"
                  f"{'win':>8}{'forks/hit':>11}{'fork share':>12}"
                  f"{'window':>8}{'ttk':>7}")
            fk = {}
            for fh, fd, fb, bb in [(2.0, 0.5, 2, 2), (4.0, 0.5, 2, 2),
                                   (6.0, 0.5, 2, 2),
                                   (4.0, 0.3, 2, 2), (4.0, 0.8, 2, 2),
                                   # THE BLEED PAIR. forkBleed alone is inert
                                   # -- hemorrhage caps at 4 and the weapon's
                                   # own onHit 2 fills it in the same call --
                                   # so the row that matters is what happens
                                   # when the BOLT stops carrying it.
                                   (4.0, 0.5, 0, 2), (4.0, 0.5, 3, 2),
                                   (4.0, 0.5, 2, 0), (4.0, 0.5, 3, 0),
                                   (4.0, 0.5, 0, 0)]:
                u = dict(base_ult)
                u["forkHome"] = fh; u["forkDmg"] = fd
                u["forkBleed"] = fb; u["boltBleed"] = bb
                d, rate, _ = bisect(page, u, a.n, 8.0, 26.0, a.steps, quiet=True)
                rows = page.evaluate(TEL_JS, [RID, d, u, foes, seeds, a.secs])
                g = agg(rows)
                fk[f"{fh}|{fd}|{fb}|{bb}"] = {"dmg": d, "rate": rate, **g}
                print(f"    {fh:>9.1f}{fd:>9.2f}{fb:>9}{bb:>9}{d:>7.2f}"
                      f"{rate:>8.1%}{g['forkPerBolt']:>11.2f}"
                      f"{g['forkShare']:>12.1%}{g['windowShare']:>8.1%}"
                      f"{g['dur']:>7.1f}")
            out["forks"] = fk

        # ------------------------------------------------------------ [4] --
        if "4" in phases:
            print(f"\n[4] THE FINAL BISECTION at the shipping numbers, "
                  f"{a.nfinal} seeds x {len(W)-1} pairings\n")
            d, rate, r = bisect(page, base_ult, a.nfinal, 10.0, 22.0, 5)
            print(f"\n    dmg {d:.2f} -> {rate:.1%} over {r['games']} fights")
            out["final"] = {"dmg": d, "rate": rate, "games": r["games"]}

        after = json.loads(page.evaluate(ROSTER_JS))
        assert after == before, "THE ROSTER WAS LEFT MUTATED"
        print("\n  the roster is put back — 24 relics identical field for field")
        assert not errors, errors[:3]

    if a.json:
        p = (HERE / a.json).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1))
        print(f"  wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
