#!/usr/bin/env python3
"""THE CHEAP FIX FOR THE DEAD ULTIMATES, MEASURED AGAINST THE EXPENSIVE ONE.

v49 §5: under 'drop the weakest', every ult-applied Curse stack is evicted by
the wielder's own blade before it ever pays. Two candidate rules for what an
ult stack remembers, both one line:

  blade   the wielder's own `w.dmg`      -- still smaller than a real blow,
                                            which lands at dmg x jitter x crit
  best    a copy of the pool's largest   -- survives displacement by construction

Baseline is `ult0` (remembers the ult's own dmg), which is what v49 measured.
Runtime injection only; nothing is written.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = r"""([donor, foes, seeds, secs, K, RATE, MODE]) => {
  const DT = AC.CONFIG.physics.dt, CU = AC.STATUS.curse;
  const oL = CU.maxHpLoss, oC = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  CU.maxHpLoss = 0; CU.maxStacks = K;
  const dw = AC.WEAPONS.find(x => x.id === donor);
  const ULTD = (dw.ult && (dw.ult.dmg || dw.ult.landDmg)) || 0;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const pool = []; let inR = false, hitD0 = 0;
    let echoDealt = 0, baseDealt = 0, hits = 0, ultKept = 0, ultApplied = 0;

    const origApply = th.apply.bind(th);
    th.apply = function(key, n){
      if (key === "curse"){
        let v;
        if (inR) v = me.dealt - hitD0;
        else {
          ultApplied += n;
          v = MODE === "blade" ? dw.dmg
            : MODE === "best"  ? (pool.length ? pool[0].v : dw.dmg)
            : ULTD;
        }
        if (v > 0){
          for (let i = 0; i < n; i++) pool.push({ v, ult: !inR });
          pool.sort((a, b) => b.v - a.v);
          while (pool.length > K) pool.pop();
        }
      }
      return origApply(key, n);
    };
    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      if (!(self === me && foe === th))
        return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      const d0 = self.dealt, h0 = self.hits;
      let s = 0; for (const p of pool) s += p.v;
      const echo = Math.round(s * RATE);
      inR = true; hitD0 = d0;
      origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      inR = false;
      if (self.hits === h0) return;
      hits++; baseDealt += self.dealt - d0;
      if (echo > 0 && foe.alive){ this.hurt(foe, echo, self); echoDealt += echo; }
    };
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    ultKept = pool.filter(p => p.ult).length;
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                echoDealt, baseDealt, hits, ultKept, ultApplied });
  }
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  return rows;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--K", type=int, default=3)
ap.add_argument("--rate", type=float, default=0.08)
a = ap.parse_args()
seeds = [3301 + 19 * i for i in range(a.seeds)]

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    print(f"\nWHAT AN ULT-APPLIED CURSE STACK REMEMBERS — K={a.K}, rate {a.rate:.0%}, "
          f"ults ON, {a.seeds} seeds x 25 foes\n")
    print(f"    {'donor':14}{'ult0 (v49)':>12}{'blade':>10}{'best':>10}"
          f"   |  kept in pool at the end: ult0 / blade / best")
    for donor in ["gravemourn", "nightfell", "twinshade"]:
        foes = [i for i in ids if i != donor]
        cells, kept = [], []
        for mode in ("ult0", "blade", "best"):
            rows = page.evaluate(JS, [donor, foes, seeds, a.secs, a.K, a.rate, mode])
            fin = [r for r in rows if r["win"] >= 0]
            cells.append(sum(r["win"] for r in fin) / len(fin))
            kept.append(statistics.mean([r["ultKept"] for r in rows]))
        print(f"    {donor:14}{cells[0]:>11.1%}{cells[1]:>10.1%}{cells[2]:>10.1%}"
              f"   |  {kept[0]:.1f} / {kept[1]:.1f} / {kept[2]:.1f}")
    assert not errors, errors[:3]
