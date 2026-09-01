#!/usr/bin/env python3
"""ONE CAST, TICK BY TICK, UNDER BOTH RULES. Rick: "how can it possibly be -52"

Prints the foe's curse pool and the echo collected at every single tick of one
cast, in one fight, under the shipped top-3-by-size rule and under the proposed
rolling window. Same fight, same seed, same opponent, same contact.
"""
from __future__ import annotations
import pathlib, sys, json
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

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

JS = r"""([donor, foe_, seed, base, push, win, rate, width, top, speed]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.CONFIG.arena.w, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const span = W - width, period = 2 * span / speed;
  const m = new AC.Match(donor, foe_, seed);
  const me = m.a.w.id === donor ? m.a : m.b;
  const foe = (me === m.a) ? m.b : m.a;
  let step = 0, nextTick = 0; const rows = [];
  while (!m.over && step < 120 / DT){
    m.step(DT); step++;
    const t = step * DT;
    if (!foe.alive || m.over) continue;
    if (t < win[0] || t >= win[1] || t < nextTick) continue;
    nextTick = t + 1 / rate;
    const ph = ((t - win[0]) % period) * speed;
    const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
    if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
    const before = foe.cursePool.slice();
    const echo = Math.round(foe.curseEcho());
    m.hurt(foe, Math.round(base) + echo, me); me.dealt += base + echo; me.hits++;
    if (push){ foe.pushCurse(Math.round(base), 1); foe.apply("curse", 1); }
    rows.push({ t: +t.toFixed(2), before, echo, after: foe.cursePool.slice(),
                dealt: Math.round(base) + echo });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return rows;
}"""

G = pathlib.Path("/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
with game(game_path=G) as (page, errors):
    for mode in ("top3", "fifo"):
        page.evaluate(INSTALL, mode)
        rows = page.evaluate(JS, ["thornwake", "dawnbringer", 13001, 5.0, True,
                                  [12, 22], 4.5, 160.0, 600.0, 200.0])
        assert not errors, errors[:3]
        label = ("SHIPPED RULE — keep the three BIGGEST, forever"
                 if mode == "top3" else
                 "ROLLING WINDOW — keep the three MOST RECENT")
        print(f"\n{'='*74}\n{label}\n{'='*74}")
        print(f"  {'tick':>5}{'t':>7}{'pool before':>22}{'echo':>7}{'tick deals':>12}"
              f"{'pool after the push of 5':>28}")
        tot = 0
        for i, r in enumerate(rows, 1):
            tot += r["dealt"]
            print(f"  {i:>5}{r['t']:>7.2f}{str([round(x) for x in r['before']]):>22}"
                  f"{r['echo']:>7}{r['dealt']:>12}{str([round(x) for x in r['after']]):>28}")
        echo = sum(r["echo"] for r in rows)
        print(f"\n  ONE CAST: {len(rows)} ticks, {tot} damage, of which {echo} is echo "
              f"({echo/max(tot,1):.0%})")
    page.evaluate(INSTALL, "top3")
