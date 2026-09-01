#!/usr/bin/env python3
"""DOES THE TORNADO COLLECT THE ECHO? Rick's reading, measured.

v62 s3-s10 asked only whether a tick ADDS to the curse pool, and answered no.
Rick asked the other direction: does a tick COLLECT from it? The engine says
every blow through `resolveHit` does --

    "PRICED ON THE TARGET AND NOT ON AN ASSUMED ATTACKER. There is no
     `self === owner` guard and there must never be one ... hit by any source."

-- but `hurt()` is a second damage path with no echo at all, and Sentinel's
beam, the closest precedent for a ticking ultimate, uses it (`beamHit` ->
`this.hurt(foe, dmg, f)`). So the tornado is worth very different amounts
depending on which path its ticks are written on, and that is a CHOICE.

Three arms, identical fights, two 10s windows a fight, 4.5 ticks a second.

    NONE    no tornado
    HURT    each tick deals its base damage only            (Sentinel's path)
    HIT     each tick deals base + the target's curse echo  (resolveHit's path)

CONTROL THAT CAN FAIL: with the pool emptied every tick, HIT must collapse onto
HURT. If it does not, the arms differ by something other than the echo.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=32)
ap.add_argument("--base", type=float, default=5.0)
ap.add_argument("--out", default="/tmp/echo_collect.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, base, mode, windows, rate]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let step = 0, nextTick = 0, ticks = 0, tornadoDmg = 0, echoSum = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (mode !== "NONE" && foe.alive && !m.over){
        const inWin = windows.some(([s, e]) => t >= s && t < e);
        if (inWin && t >= nextTick){
          if (mode === "DRAIN") foe.cursePool.length = 0;
          const echo = (mode === "HIT" || mode === "DRAIN") ? Math.round(foe.curseEcho()) : 0;
          const dmg = Math.round(base) + echo;
          m.hurt(foe, dmg, me);
          me.dealt += dmg; me.hits++;
          ticks++; tornadoDmg += dmg; echoSum += echo;
          nextTick = t + 1 / rate;
        }
      }
    }
    out.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               dealt: me.dealt, dur: step * DT, ticks, tornadoDmg, echoSum,
               pool: foe.cursePool.slice() });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=pathlib.Path(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [9901 + 37*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time(); arms = {}
    for mode in ("NONE", "HURT", "HIT", "DRAIN"):
        arms[mode] = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, a.base, mode, WIN, 4.5])
        assert not errors, errors[:3]
    n = len(arms["NONE"])
    print(f"\nDOES THE TORNADO COLLECT THE ECHO?  base tick {a.base:.0f} damage, "
          f"{n} fights an arm, 4.5 ticks/s in two 10s windows\n")
    print(f"    {'arm':<8}{'ticks':>8}{'tornado dmg':>14}{'of which echo':>15}"
          f"{'total dealt':>13}{'win rate':>10}{'vs NONE':>10}")
    base_wr = None
    for mode in ("NONE", "HURT", "HIT", "DRAIN"):
        rs = arms[mode]
        tk = statistics.mean([r["ticks"] for r in rs])
        td = statistics.mean([r["tornadoDmg"] for r in rs])
        es = statistics.mean([r["echoSum"] for r in rs])
        dl = statistics.mean([r["dealt"] for r in rs])
        wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
        if mode == "NONE": base_wr = wr
        print(f"    {mode:<8}{tk:>8.1f}{td:>14.1f}{es:>15.1f}{dl:>13.1f}"
              f"{wr:>10.1%}{wr-base_wr:>+10.1%}")
    hurt = statistics.mean([r["tornadoDmg"] for r in arms["HURT"]])
    hit  = statistics.mean([r["tornadoDmg"] for r in arms["HIT"]])
    drain= statistics.mean([r["tornadoDmg"] for r in arms["DRAIN"]])
    print(f"\n    THE ECHO IS WORTH {hit/max(hurt,1e-9):.2f}x THE TICK'S OWN DAMAGE "
          f"({hurt:.0f} -> {hit:.0f} per fight)")
    print(f"    CONTROL — pool emptied every tick (DRAIN) must collapse onto HURT: "
          f"{drain:.1f} vs {hurt:.1f}  "
          f"{'PASS' if abs(drain-hurt) < max(3.0, hurt*0.05) else 'FAIL'}")
    print(f"\n    {4*n} fights in {time.time()-t0:.0f}s   errors: {errors}")
    json.dump({k: v for k, v in arms.items()}, open(a.out, "w"))
