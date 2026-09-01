#!/usr/bin/env python3
"""WOULD THE TORNADO BENEFIT FROM CURSE? Rick's question, under both rules.

The tornado's ticks are hits, so they do two things to curse: they COLLECT the
echo (read before the blow's own onHit runs) and they PUSH a memory of their
own tick damage. Under the shipped top-3-by-size rule the push is discarded and
the collect is free. Under Rick's proposed rolling-window rule the push
DISPLACES the blade's memories, so the tornado floods the pool with its own
tick-sized numbers and stops paying itself.

Four arms, the tornado at its real geometry (160 wide, y>=600, two 10s casts,
4.5 ticks/s, base 5), 320 fights an arm:

    top3 / push     shipped rule, ticks apply curse as Rick's §1 says
    top3 / nopush   shipped rule, ticks collect but never apply
    fifo / push     rolling window, ticks apply curse
    fifo / nopush   rolling window, ticks collect but never apply

CONTROL THAT CAN FAIL: top3/push and top3/nopush must be the same within noise
-- under a top-3-by-size rule a memory of 5 is discarded, so pushing it can
change nothing. If those two arms differ, the push is doing something the rule
says it cannot.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=32)
ap.add_argument("--out", default="/tmp/tornado_fifo.json")
a = ap.parse_args()

INSTALL = r"""(mode) => {
  const m0 = new AC.Match(AC.WEAPONS[0].id, AC.WEAPONS[1].id, 1);
  const P = Object.getPrototypeOf(m0.a);
  if (!P.__origPush) P.__origPush = P.pushCurse;
  const MAX = AC.STATUS.curse.maxStacks;
  if (mode === "fifo"){
    P.pushCurse = function(v, n){
      for (let i = 0; i < n; i++) this.cursePool.push(v);
      while (this.cursePool.length > MAX) this.cursePool.shift();
    };
  } else { P.pushCurse = P.__origPush; }
  return mode;
}"""

JS = r"""([donor, foes, seeds, secs, base, push, windows, rate, width, top, speed]) => {
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
    let step = 0, nextTick = 0, ticks = 0, dmgSum = 0, echoSum = 0, firstEcho = -1, lastEcho = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (!foe.alive || m.over) continue;
      const inWin = windows.some(([s, e]) => t >= s && t < e);
      if (!inWin || t < nextTick) continue;
      nextTick = t + 1 / rate;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
      /* resolveHit's order: the echo is read BEFORE this blow's own onHit runs */
      const echo = Math.round(foe.curseEcho());
      const dmg = Math.round(base) + echo;
      m.hurt(foe, dmg, me); me.dealt += dmg; me.hits++;
      if (push){ foe.pushCurse(Math.round(base), 1); foe.apply("curse", 1); }
      ticks++; dmgSum += dmg; echoSum += echo;
      if (firstEcho < 0) firstEcho = echo;
      lastEcho = echo;
    }
    out.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1, ticks, dmgSum, echoSum,
               firstEcho, lastEcho, dealt: me.dealt });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=pathlib.Path(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [13001 + 53*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time(); arms = {}
    print(f"\nWOULD THE TORNADO BENEFIT FROM CURSE? — 160 wide, two 10s casts, "
          f"base tick 5, {len(panel)*a.seeds} fights an arm\n")
    print(f"    {'rule':<6}{'ticks apply?':<14}{'ticks':>8}{'echo/fight':>12}"
          f"{'tornado dmg':>13}{'echo 1st tick':>15}{'echo last tick':>16}{'win rate':>10}")
    for mode in ("top3", "fifo"):
        for push in (True, False):
            page.evaluate(INSTALL, mode)
            rs = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, 5.0, push,
                                    WIN, 4.5, 160.0, 600.0, 200.0])
            assert not errors, errors[:3]
            k = f"{mode}/{'push' if push else 'nopush'}"
            arms[k] = rs
            tk = statistics.mean([r["ticks"] for r in rs])
            es = statistics.mean([r["echoSum"] for r in rs])
            td = statistics.mean([r["dmgSum"] for r in rs])
            fe = statistics.mean([r["firstEcho"] for r in rs if r["firstEcho"] >= 0])
            le = statistics.mean([r["lastEcho"] for r in rs if r["ticks"] > 0])
            wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
            print(f"    {mode:<6}{('yes' if push else 'no'):<14}{tk:>8.1f}{es:>12.1f}"
                  f"{td:>13.1f}{fe:>15.1f}{le:>16.1f}{wr:>10.1%}")
    page.evaluate(INSTALL, "top3")
    d = lambda k, f: statistics.mean([r[f] for r in arms[k]])
    print(f"\n    CONTROL — under top-3 a memory of 5 is discarded, so push and nopush")
    print(f"    must agree: tornado damage {d('top3/push','dmgSum'):.1f} vs "
          f"{d('top3/nopush','dmgSum'):.1f}  "
          f"{'PASS' if abs(d('top3/push','dmgSum')-d('top3/nopush','dmgSum')) < 8 else 'FAIL'}")
    print(f"\n    THE ANSWER:")
    print(f"      top-3 rule, ticks apply curse   echo {d('top3/push','echoSum'):>6.0f} a fight   "
          f"win {statistics.mean([r['win'] for r in arms['top3/push'] if r['win']>=0]):.1%}")
    print(f"      FIFO rule,  ticks apply curse   echo {d('fifo/push','echoSum'):>6.0f} a fight   "
          f"win {statistics.mean([r['win'] for r in arms['fifo/push'] if r['win']>=0]):.1%}")
    print(f"      FIFO rule,  ticks do NOT apply  echo {d('fifo/nopush','echoSum'):>6.0f} a fight   "
          f"win {statistics.mean([r['win'] for r in arms['fifo/nopush'] if r['win']>=0]):.1%}")
    json.dump({k: v for k, v in arms.items()}, open(a.out, "w"))
    print(f"\n    {4*len(panel)*a.seeds} fights in {time.time()-t0:.0f}s   errors: {errors}")
