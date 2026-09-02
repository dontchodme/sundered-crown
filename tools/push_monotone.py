#!/usr/bin/env python3
"""IS PUSHING CURSE EVER A LOSS? Rick: "how can it possibly do anything but
benefit the relic even with the rolling window?"

Run against the real Fighter.pushCurse in the build, and against the proposed
rolling-window replacement, on the same starting pools.
"""
import pathlib, sys, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # v63: was a hardcoded Cowork container path; runs from tools/ on any machine now
from scpage import game, resolve_game

JS = r"""(mode) => {
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
  const f = m0.a;
  const rows = [];
  for (const start of [[], [40], [40, 25], [35, 20, 10], [35, 5, 5], [50, 38, 31]])
    for (const v of [5, 50]){
      f.cursePool.length = 0;
      for (const x of start) f.cursePool.push(x);
      if (mode === "top3") f.cursePool.sort((a,b)=>b-a);
      const before = f.cursePool.slice();
      const s0 = before.reduce((a,b)=>a+b,0);
      f.pushCurse(v, 1);
      const after = f.cursePool.slice();
      const s1 = after.reduce((a,b)=>a+b,0);
      rows.push({ before, v, after, s0, s1, d: s1 - s0 });
    }
  P.pushCurse = P.__origPush;
  return rows;
}"""

G = resolve_game("02-chain/sc-garrote.html")  # v63: repo-relative
with game(game_path=G) as (page, errors):
    for mode, title in (("top3", "SHIPPED RULE — push, sort descending, truncate to 3"),
                        ("fifo", "ROLLING WINDOW — push, shift the oldest out")):
        rows = page.evaluate(JS, mode)
        print(f"\n{'='*72}\n{title}\n{'='*72}")
        print(f"  {'pool before':>18}{'push':>6}{'pool after':>18}{'sum before':>12}"
              f"{'sum after':>11}{'change':>9}")
        worst = 0
        for r in rows:
            worst = min(worst, r["d"])
            print(f"  {str(r['before']):>18}{r['v']:>6}{str(r['after']):>18}"
                  f"{r['s0']:>12}{r['s1']:>11}{r['d']:>+9}")
        print(f"\n  worst change: {worst:+}   "
              f"{'-> pushing can NEVER lower the pool' if worst >= 0 else '-> pushing CAN lower the pool'}")
    assert not errors, errors[:3]
