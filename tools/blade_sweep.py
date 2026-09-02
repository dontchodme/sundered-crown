#!/usr/bin/env python3
"""THE BLADE AND THE ULTIMATE ARE COUPLED ON THIS RELIC. HOW TIGHTLY?

v62 s11: the tornado's ticks collect the target's curse echo, and the echo is
8% of the three biggest blows the SCYTHE landed. So a heavier blade makes
bigger memories, and bigger memories make every tick hit harder. No other relic
in the game has this loop.

Sweeps the blade across the scythe row's real range (Vesper 17.25 -> Thornwake
31.35) and measures, at each: the relic with no ultimate, and the relic with
the tornado on the resolveHit path.

CONTROL THAT CAN FAIL: the no-ult arm must rise monotonically with the blade.
If a heavier blade does not win more fights without an ultimate, the injection
is not reaching the weapon.
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
ap.add_argument("--out", default="/tmp/blade_sweep.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, blade, base, on, windows, rate, width, top, speed]) => {
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
    let step = 0, nextTick = 0, ticks = 0, dmgSum = 0, echoSum = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const t = step * DT;
      if (!on || !foe.alive || m.over) continue;
      const inWin = windows.some(([s, e]) => t >= s && t < e);
      if (!inWin || t < nextTick) continue;
      nextTick = t + 1 / rate;
      const ph = ((t - windows[0][0]) % period) * speed;
      const cx = (ph <= span ? ph : 2 * span - ph) + width / 2;
      if (!((foe.y + R >= top) && (Math.abs(foe.x - cx) <= width / 2 + R))) continue;
      const echo = Math.round(foe.curseEcho());
      const dmg = Math.round(base) + echo;
      m.hurt(foe, dmg, me); me.dealt += dmg; me.hits++;
      ticks++; dmgSum += dmg; echoSum += echo;
    }
    out.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               ticks, dmgSum, echoSum, pool: foe.cursePool.slice() });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  return out;
}"""

with game(game_path=resolve_game(a.game)) as (page, errors):
    panel = ["dawnbringer","widowmaker","grudgebearer","gravemourn","ironhail",
             "axiom","censer","bulwarden","foregone","heartwood"]
    seeds = [11101 + 43*i for i in range(a.seeds)]
    WIN = [[12, 22], [30, 40]]
    t0 = time.time(); rows = []
    print(f"\nBLADE x ULTIMATE — base tick {a.base:.0f}, 160 wide, two 10s casts, "
          f"{len(panel)*a.seeds} fights an arm\n")
    print(f"    {'blade':>7}{'no ult':>10}{'with tornado':>15}{'the ult is worth':>19}"
          f"{'echo/fight':>13}{'tornado dmg':>14}{'pool sum':>11}")
    for blade in (17.25, 21.0, 24.0, 27.0, 31.35):
        off = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, blade, a.base, False,
                                 WIN, 4.5, 160.0, 600.0, 200.0])
        on = page.evaluate(JS, ["thornwake", panel, seeds, 120.0, blade, a.base, True,
                                WIN, 4.5, 160.0, 600.0, 200.0])
        assert not errors, errors[:3]
        wo = statistics.mean([r["win"] for r in off if r["win"] >= 0])
        wn = statistics.mean([r["win"] for r in on if r["win"] >= 0])
        es = statistics.mean([r["echoSum"] for r in on])
        td = statistics.mean([r["dmgSum"] for r in on])
        pools = [sum(r["pool"]) for r in on if r["pool"]]
        ps = statistics.mean(pools) if pools else 0.0
        rows.append({"blade": blade, "off": wo, "on": wn, "lift": (wn-wo)*100,
                     "echo": es, "td": td, "pool": ps})
        print(f"    {blade:>7.2f}{wo:>10.1%}{wn:>15.1%}{(wn-wo)*100:>+18.1f}pp"
              f"{es:>13.1f}{td:>14.1f}{ps:>11.1f}")
    mono = all(rows[i]["off"] <= rows[i+1]["off"] + 0.03 for i in range(len(rows)-1))
    print(f"\n    CONTROL — no-ult win rate must rise with the blade: "
          f"{'PASS' if mono else 'FAIL — blade injection is not reaching the weapon'}")
    lo, hi = rows[0], rows[-1]
    print(f"    THE COUPLING: blade {lo['blade']:.2f} -> {hi['blade']:.2f} moves the "
          f"tornado's own damage {lo['td']:.0f} -> {hi['td']:.0f} "
          f"({(hi['td']/max(lo['td'],1e-9)-1):+.0%}) with NO change to the ultimate")
    print(f"\n    {2*5*len(panel)*a.seeds} fights in {time.time()-t0:.0f}s   errors: {errors}")
    json.dump(rows, open(a.out, "w"), indent=1)
