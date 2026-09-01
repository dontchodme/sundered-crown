#!/usr/bin/env python3
"""DOES A TICK-SIZED CURSE DO ANYTHING? A/B, PAIRED ON SEED AND OPPONENT.

Rick asked, fairly: "how is it not doing anything currently?" Asserting it a
third time is worth less than running it.

Three arms on identical fights. An umbral scythe (curse grafted on the scythe
donor). Two 10-second windows per fight standing in for the two casts, ticking
4.5 times a second -- the tornado's exact cadence:

    OFF     nothing injected
    TICK    every tick hands curse a memory of 8.5, the tornado's tick damage
    BIG     every tick hands curse a memory of 60 instead

POSITIVE CONTROL THAT MUST FAIL THE NULL: the BIG arm has to move. If pushing
60 changes nothing either, the injection is not reaching the fight and the TICK
result means nothing.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=12)
ap.add_argument("--out", default="/tmp/tick_ab.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, mem, windows, rate]) => {
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
    let step = 0, nextTick = 0, pushed = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (mem !== null){
        const inWin = windows.some(([s, e]) => t >= s && t < e);
        if (inWin && t >= nextTick){
          foe.pushCurse(mem, 1); foe.apply("curse", 1);
          pushed++; nextTick = t + 1 / rate;
        }
      }
    }
    out.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               dealt: me.dealt, foeHp: Math.max(0, foe.hp), dur: step * DT,
               pool: foe.cursePool.slice(), echo: foe.curseEcho(), pushed });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=pathlib.Path(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [9101 + 31*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time(); arms = {}
    for name, mem in (("OFF", None), ("TICK 8.5", 8.5), ("BIG 60", 60.0)):
        arms[name] = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, mem, WIN, 4.5])
        assert not errors, errors[:3]
    n = len(arms["OFF"])
    print(f"\nDOES A TICK-SIZED CURSE DO ANYTHING?  {n} fights an arm, paired on seed and foe")
    print(f"two 10s windows a fight, 4.5 ticks a second — the tornado's own cadence\n")
    print(f"    {'arm':<10}{'memories pushed':>17}{'final pool':>26}{'echo/blow':>11}"
          f"{'damage dealt':>14}{'win rate':>10}")
    base = None
    for name in ("OFF", "TICK 8.5", "BIG 60"):
        rs = arms[name]
        pools = [r["pool"] for r in rs if len(r["pool"]) == 3]
        mp = [statistics.mean([p[i] for p in pools]) for i in range(3)] if pools else [0,0,0]
        echo = statistics.mean([r["echo"] for r in rs])
        dealt = statistics.mean([r["dealt"] for r in rs])
        wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
        push = statistics.mean([r["pushed"] for r in rs])
        print(f"    {name:<10}{push:>17.0f}{str([round(x) for x in mp]):>26}"
              f"{echo:>11.2f}{dealt:>14.1f}{wr:>10.1%}")
        if name == "OFF": base = (echo, dealt, wr)
    print()
    for name in ("TICK 8.5", "BIG 60"):
        rs = arms[name]
        echo = statistics.mean([r["echo"] for r in rs])
        dealt = statistics.mean([r["dealt"] for r in rs])
        wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
        pairs = {(r["foe"], r["seed"]): r for r in arms["OFF"]}
        diffs = [r["dealt"] - pairs[(r["foe"], r["seed"])]["dealt"] for r in rs]
        ident = sum(1 for d in diffs if abs(d) < 1e-9)
        print(f"    {name:<10} vs OFF:  echo {echo-base[0]:+.2f}   damage {dealt-base[1]:+.1f}"
              f"   win {wr-base[2]:+.1%}   BYTE-IDENTICAL FIGHTS: {ident}/{len(diffs)}")
    print(f"\n    POSITIVE CONTROL: BIG 60 must move. "
          f"{'PASS' if abs(statistics.mean([r['echo'] for r in arms['BIG 60']]) - base[0]) > 1.0 else 'FAIL — injection is not reaching the fight'}")
    print(f"\n    {3*n} fights in {time.time()-t0:.0f}s   errors: {errors}")
    json.dump({k: [{kk: vv for kk, vv in r.items()} for r in v] for k, v in arms.items()},
              open(a.out, "w"))
