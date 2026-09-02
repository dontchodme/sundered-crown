#!/usr/bin/env python3
"""THE TORNADO, WITH ITS REAL GEOMETRY AND BOTH DAMAGE PATHS.

Joins the two halves this session measured separately:
  - `tornado_lab.py`  -- a 160-wide band sweeping the floor catches the foe
                         ~26% of the time (v62 s8).
  - `echo_collect.py` -- a tick on `resolveHit`'s path collects the target's
                         curse echo; a tick on `hurt()`'s path does not (v62 s11).

Here the tornado only ticks WHEN IT IS ACTUALLY TOUCHING THE FOE, sweeping in
the sim's own coordinates, for two 10-second casts a fight.

    HURT   tick deals base only                      (Sentinel's beamHit path)
    HIT    tick deals base + target's curse echo     (resolveHit's path)

CONTROLS THAT CAN FAIL:
  1. contact -- measured ticks / possible ticks must land near the 26% that
     `tornado_lab` predicted from position tracks alone.
  2. DRAIN -- emptying the pool before reading the echo must collapse HIT onto
     HURT, or the two arms differ by something that is not the echo.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # v63: was a hardcoded Cowork container path; runs from tools/ on any machine now
from scpage import game, resolve_game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="02-chain/sc-garrote.html")  # v63: repo-relative, resolved by scpage.resolve_game
ap.add_argument("--seeds", type=int, default=32)
ap.add_argument("--base", type=float, default=5.0)
ap.add_argument("--width", type=float, default=160.0)
ap.add_argument("--top", type=float, default=600.0)
ap.add_argument("--speed", type=float, default=200.0)
ap.add_argument("--out", default="/tmp/tornado_full.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, base, mode, windows, rate, width, top, speed]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.CONFIG.arena.w, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const span = W - width, period = 2 * span / speed;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let step = 0, nextTick = 0, ticks = 0, possible = 0, dmgSum = 0, echoSum = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (mode === "NONE" || !foe.alive || m.over) continue;
      const inWin = windows.some(([s, e]) => t >= s && t < e);
      if (!inWin || t < nextTick) continue;
      nextTick = t + 1 / rate; possible++;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      const touching = (foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R);
      if (!touching) continue;
      if (mode === "DRAIN") foe.cursePool.length = 0;
      const echo = (mode === "HIT" || mode === "DRAIN") ? Math.round(foe.curseEcho()) : 0;
      const dmg = Math.round(base) + echo;
      m.hurt(foe, dmg, me); me.dealt += dmg; me.hits++;
      ticks++; dmgSum += dmg; echoSum += echo;
    }
    out.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               dealt: me.dealt, dur: step * DT, ticks, possible, dmgSum, echoSum });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=resolve_game(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [10301 + 41*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time(); arms = {}
    for mode in ("NONE", "HURT", "HIT", "DRAIN"):
        arms[mode] = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, a.base, mode,
                                        WIN, 4.5, a.width, a.top, a.speed])
        assert not errors, errors[:3]
    n = len(arms["NONE"])
    print(f"\nTHE TORNADO AT ITS REAL SIZE — {a.width:.0f} wide, top y={a.top:.0f}, "
          f"{a.speed:.0f} px/s, base tick {a.base:.0f}")
    print(f"two 10s casts a fight, 4.5 ticks/s, {n} fights an arm\n")
    print(f"    {'arm':<8}{'ticks/fight':>13}{'contact':>10}{'tornado dmg':>14}"
          f"{'of which echo':>15}{'per cast':>10}{'win rate':>10}{'vs NONE':>10}")
    base_wr = None
    for mode in ("NONE", "HURT", "HIT", "DRAIN"):
        rs = arms[mode]
        tk = statistics.mean([r["ticks"] for r in rs])
        po = statistics.mean([r["possible"] for r in rs]) or 1
        td = statistics.mean([r["dmgSum"] for r in rs])
        es = statistics.mean([r["echoSum"] for r in rs])
        wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
        if mode == "NONE": base_wr = wr
        print(f"    {mode:<8}{tk:>13.1f}{tk/po:>9.1%}{td:>14.1f}{es:>15.1f}"
              f"{td/2:>10.1f}{wr:>10.1%}{wr-base_wr:>+10.1%}")
    hurt = statistics.mean([r["dmgSum"] for r in arms["HURT"]])
    hit  = statistics.mean([r["dmgSum"] for r in arms["HIT"]])
    drain= statistics.mean([r["dmgSum"] for r in arms["DRAIN"]])
    ctk  = statistics.mean([r["ticks"] for r in arms["HURT"]])
    cpo  = statistics.mean([r["possible"] for r in arms["HURT"]])
    print(f"\n    CONTROL 1 — contact {ctk/cpo:.1%}, tornado_lab predicted 26.0% from "
          f"position tracks alone.  {'PASS' if abs(ctk/cpo - 0.26) < 0.07 else 'FAIL'}")
    print(f"    CONTROL 2 — DRAIN must collapse onto HURT: {drain:.1f} vs {hurt:.1f}  "
          f"{'PASS' if abs(drain-hurt) < max(4.0, hurt*0.08) else 'FAIL'}")
    print(f"\n    THE ECHO IS {hit-hurt:+.0f} DAMAGE A FIGHT, "
          f"{(hit-hurt)/max(hurt,1e-9):+.0%} on top of the tick's own")
    print(f"\n    {4*n} fights in {time.time()-t0:.0f}s   errors: {errors}")
    json.dump({k: v for k, v in arms.items()}, open(a.out, "w"))
