#!/usr/bin/env python3
"""TICK RATE IS NOT A FREE KNOB. v62 s9a SAID IT WAS AND THAT IS WITHDRAWN.

Rick: "the ticks hit faster than the blades hit. much faster. which means more
activations of curses extra damage."

s9a called tick rate "pure feel, no balance". That was written while this
document still believed the ticks fed the pool and were paid once on release.
On the `resolveHit` path EVERY TICK COLLECTS THE ECHO, so the tick rate is a
direct multiplier on the ultimate's damage. Rick is right and the earlier
ruling was wrong.

Two ladders, because they separate two different claims:

  [A] FIXED BASE PER TICK (5). More ticks = more base damage AND more echo
      activations. The naive reading.
  [B] FIXED TOTAL BASE DAMAGE (100 a cast, so base = 100/expected ticks).
      The tick's own damage is held constant and ONLY the number of echo
      activations changes. This isolates Rick's claim exactly.

CONTROL THAT CAN FAIL: in ladder [B] the tornado's non-echo damage must stay
flat across the whole ladder. If base damage drifts, [B] is not isolating
anything.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, "/mnt/user-data/uploads/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="/mnt/user-data/uploads/sundered-crown/02-chain/sc-garrote.html")
ap.add_argument("--seeds", type=int, default=32)
ap.add_argument("--out", default="/tmp/rate_ladder.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, base, windows, rate, width, top, speed]) => {
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
    let step = 0, nextTick = 0, ticks = 0, baseSum = 0, echoSum = 0, bladeHits0 = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (!foe.alive || m.over) continue;
      if (!windows.some(([s, e]) => t >= s && t < e) || t < nextTick) continue;
      nextTick = t + 1 / rate;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
      const echo = Math.round(foe.curseEcho());
      const b = Math.max(1, Math.round(base));
      m.hurt(foe, b + echo, me); me.dealt += b + echo; me.hits++;
      ticks++; baseSum += b; echoSum += echo;
    }
    out.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               ticks, baseSum, echoSum });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=pathlib.Path(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [14009 + 59*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    RATES = [1.5, 3.0, 4.5, 7.0, 10.0, 15.0]
    t0 = time.time(); res = {"A": [], "B": []}
    # baseline with no tornado
    none = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, 0.0, [[999,999]],
                              4.5, 160.0, 600.0, 200.0])
    base_wr = statistics.mean([r["win"] for r in none if r["win"] >= 0])
    print(f"\nno tornado at all: {base_wr:.1%} win rate\n")
    for lad, label in (("A", "[A] FIXED BASE PER TICK — 5 damage a tick, whatever the rate"),
                       ("B", "[B] FIXED TOTAL BASE — ~100 base damage a cast at every rate")):
        print(f"{label}\n")
        print(f"    {'ticks/s':>9}{'base/tick':>11}{'ticks/fight':>13}{'base dmg':>10}"
              f"{'echo dmg':>10}{'total':>8}{'echo share':>12}{'win':>8}{'vs none':>9}")
        for rate in RATES:
            if lad == "A":
                base = 5.0
            else:
                exp = 0.26 * 20.0 * rate          # contact x cast seconds x rate
                base = max(1.0, 200.0 / max(exp, 1e-9))   # 100 a cast x 2 casts
            rs = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, base, WIN,
                                    rate, 160.0, 600.0, 200.0])
            assert not errors, errors[:3]
            tk = statistics.mean([r["ticks"] for r in rs])
            bs = statistics.mean([r["baseSum"] for r in rs])
            es = statistics.mean([r["echoSum"] for r in rs])
            wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
            res[lad].append({"rate": rate, "base": base, "ticks": tk, "baseSum": bs,
                             "echo": es, "win": wr})
            print(f"    {rate:>9.1f}{base:>11.1f}{tk:>13.1f}{bs:>10.1f}{es:>10.1f}"
                  f"{bs+es:>8.1f}{es/max(bs+es,1e-9):>11.0%}{wr:>8.1%}{(wr-base_wr)*100:>+8.1f}")
        print()
    bs = [r["baseSum"] for r in res["B"]]
    print(f"    CONTROL — ladder [B] base damage must stay flat: "
          f"{min(bs):.0f} to {max(bs):.0f}  "
          f"{'PASS' if max(bs)/max(min(bs),1e-9) < 1.35 else 'FAIL — base is drifting'}")
    lo, hi = res["B"][0], res["B"][-1]
    print(f"\n    RICK'S CLAIM, ISOLATED: at the SAME base damage, "
          f"{lo['rate']:.1f} -> {hi['rate']:.1f} ticks/s moves echo "
          f"{lo['echo']:.0f} -> {hi['echo']:.0f} ({hi['echo']/max(lo['echo'],1e-9):.1f}x) "
          f"and win {(lo['win']-base_wr)*100:+.1f} -> {(hi['win']-base_wr)*100:+.1f} points")
    json.dump(res, open(a.out, "w"), indent=1)
    print(f"\n    done in {time.time()-t0:.0f}s   errors: {errors}")
