#!/usr/bin/env python3
"""DUSKREAVE AS RICK SETTLED IT. The shipping configuration, measured whole.

    blade      21          (Bloodmirror's weight, his call)
    tick rate  7 a second  (his call, once tick rate was shown to be a knob)
    base tick  5
    tornado    160 wide, top y=600, sweeps the floor at 200 px/s
    cast       10 seconds, ~2 a fight
    curse      SHIPPED RULE. Ticks are hits: they COLLECT the echo, and they
               APPLY curse as Rick's §1 says. Both, as written.

Every previous table in v62 measured one axis with the others at defaults --
the rate ladder ran on Thornwake's 31.35 blade, the blade sweep at 4.5 ticks.
This is the combination that ships and it had never been run.

CONTROL THAT CAN FAIL: the no-ult arm must land near the 29.4% blade_sweep
measured for a 21 blade. Different seeds, different code path; if it misses by
much, one of the two is wrong.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # v63: was a hardcoded Cowork container path; runs from tools/ on any machine now
from scpage import game, resolve_game

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="02-chain/sc-garrote.html")  # v63: repo-relative, resolved by scpage.resolve_game
ap.add_argument("--seeds", type=int, default=34)
ap.add_argument("--out", default="/tmp/duskreave_config.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, blade, base, on, apply_, windows, rate, width, top, speed]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.CONFIG.arena.w, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
                  onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  w.aff = "umbral"; w.dmg = blade; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const span = W - width, period = 2 * span / speed;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let step = 0, nextTick = 0, ticks = 0, baseSum = 0, echoSum = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (!on || !foe.alive || m.over) continue;
      if (!windows.some(([s, e]) => t >= s && t < e) || t < nextTick) continue;
      nextTick = t + 1 / rate;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
      const echo = Math.round(foe.curseEcho());
      const b = Math.round(base);
      m.hurt(foe, b + echo, me); me.dealt += b + echo; me.hits++;
      if (apply_){ foe.pushCurse(b, 1); foe.apply("curse", 1); }
      ticks++; baseSum += b; echoSum += echo;
    }
    out.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1, ticks,
               baseSum, echoSum, dur: step * DT, dealt: me.dealt, hits: me.hits });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=resolve_game(a.game)) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != "thornwake"]
    seeds = [16001 + 67*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time()
    print(f"\nDUSKREAVE / SCOUR — blade 21, 7 ticks/s, base 5, 160 wide, 10s casts")
    print(f"against all {len(foes)} other relics x {a.seeds} seeds = {len(foes)*a.seeds} fights an arm\n")
    res = {}
    for label, on, apply_ in (("no ultimate", False, False),
                              ("SCOUR, ticks apply curse", True, True),
                              ("SCOUR, ticks do not apply", True, False)):
        rs = page.evaluate(JS, ["thornwake", foes, seeds, 120.0, 21.0, 5.0, on, apply_,
                                WIN, 7.0, 160.0, 600.0, 200.0])
        assert not errors, errors[:3]
        res[label] = rs
        wr = statistics.mean([r["win"] for r in rs if r["win"] >= 0])
        tk = statistics.mean([r["ticks"] for r in rs])
        bs = statistics.mean([r["baseSum"] for r in rs])
        es = statistics.mean([r["echoSum"] for r in rs])
        print(f"    {label:<28}{wr:>8.1%}   ticks {tk:>5.1f}   "
              f"base {bs:>6.1f}   echo {es:>6.1f}   total {bs+es:>6.1f}   "
              f"per cast {(bs+es)/2:>6.1f}")
    off = statistics.mean([r["win"] for r in res["no ultimate"] if r["win"] >= 0])
    onA = statistics.mean([r["win"] for r in res["SCOUR, ticks apply curse"] if r["win"] >= 0])
    onB = statistics.mean([r["win"] for r in res["SCOUR, ticks do not apply"] if r["win"] >= 0])
    print(f"\n    SCOUR IS WORTH {(onA-off)*100:+.1f}pp   "
          f"(and {(onA-onB)*100:+.1f}pp of that is the apply clause — noise, as measured)")
    print(f"    CONTROL — blade_sweep put a 21 blade with no ult at 29.4%; "
          f"this run says {off:.1%}.  "
          f"{'PASS' if abs(off-0.294) < 0.08 else 'FAIL — the two disagree'}")
    print(f"\n    for scale: Crossweave +48.8pp, and v60 s2 puts the error bar at ~4.3pp")
    print(f"\n    {3*len(foes)*a.seeds} fights in {time.time()-t0:.0f}s   errors: {errors}")
    json.dump({k: v for k, v in res.items()}, open(a.out, "w"))
