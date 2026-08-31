#!/usr/bin/env python3
"""v49 §5 CORRECTION. The first pass guarded the echo on `self === donor`, so
every blow landed by a Twinshade SHADE was invisible to it: shades are real
Fighter objects carrying the relic's own `onHit:{curse:1}`, resolved on the
shade and credited to the caster afterwards (`tickShadeHits`). They neither
fed the pool nor cashed it, and Twinshade's -5.3pp was that bug, not the
design.

Corrected rule, which is also PoE's: the echo is priced on the TARGET, and any
blow landing on a cursed target pays it and remembers its own damage.

Runtime injection only; nothing is written.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent
UMBRAL = ["gravemourn", "nightfell", "twinshade"]

JS = r"""([donor, foes, seeds, secs, arm, K, RATE]) => {
  const DT = AC.CONFIG.physics.dt, CU = AC.STATUS.curse;
  const oL = CU.maxHpLoss, oC = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  if (arm !== "shipped") CU.maxHpLoss = 0;
  if (arm === "echo") CU.maxStacks = K;
  const dw = AC.WEAPONS.find(x => x.id === donor);
  const ULTD = (dw.ult && (dw.ult.dmg || dw.ult.landDmg)) || 0;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const pool = [];
    let inR = false, hitSrc = null, hitD0 = 0;
    let echoDealt = 0, baseDealt = 0, hits = 0, shadeHits = 0, ultStacks = 0;

    const origApply = th.apply.bind(th);
    th.apply = function(key, n){
      if (key === "curse" && arm === "echo"){
        const v = inR ? (hitSrc.dealt - hitD0) : ULTD;
        if (!inR) ultStacks += n;
        if (v > 0){
          for (let i = 0; i < n; i++) pool.push(v);
          pool.sort((a, b) => b - a);
          while (pool.length > K) pool.pop();
        }
      }
      return origApply(key, n);
    };

    if (arm === "echo"){
      /* PRICED ON THE TARGET. Any blow landing on the cursed fighter pays the
         echo and remembers its own damage -- a shade's swing is a blow. */
      m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
        if (foe !== th) return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
        const d0 = self.dealt, h0 = self.hits;
        let s = 0; for (const v of pool) s += v;
        const echo = Math.round(s * RATE);
        inR = true; hitSrc = self; hitD0 = d0;
        origResolve.call(this, self, foe, hx, hy, seg, mul, over);
        inR = false;
        if (self.hits === h0) return;
        hits++; if (self.shade) shadeHits++;
        baseDealt += self.dealt - d0;
        if (echo > 0 && foe.alive){ this.hurt(foe, echo, self); echoDealt += echo; }
      };
    }

    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                echoDealt, baseDealt, hits, shadeHits, ultStacks });
  }
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  return rows;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--secs", type=float, default=120.0)
a = ap.parse_args()
seeds = [3301 + 19 * i for i in range(a.seeds)]
arms = [("none", 0, 0.0), ("shipped", 0, 0.0),
        ("echo", 3, 0.08), ("echo", 3, 0.15), ("echo", 5, 0.08)]

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    print(f"\nCORRECTED ARMS — echo priced on the TARGET, shade blows counted")
    print(f"    shipped damage, ults ON, {a.seeds} seeds x 25 foes = {25*a.seeds} fights an arm\n")
    print(f"    {'donor':14}" + "".join(
        f"{(n if n!='echo' else 'K%d r%.0f%%'%(k,r*100)):>12}" for n, k, r in arms))
    det = {}
    for donor in UMBRAL:
        foes = [i for i in ids if i != donor]
        cells = []
        for n, k, r in arms:
            rows = page.evaluate(JS, [donor, foes, seeds, a.secs, n, k, r])
            fin = [x for x in rows if x["win"] >= 0]
            cells.append(sum(x["win"] for x in fin) / len(fin))
            det[(donor, n, k, r)] = rows
        print(f"    {donor:14}" + "".join(f"{c:>11.1%}" for c in cells))
    print(f"\n    {'donor':14}{'arm':>10}{'blows':>8}{'of which shade':>16}"
          f"{'base dmg':>10}{'echo dmg':>10}{'uplift':>9}")
    for donor in UMBRAL:
        for n, k, r in arms:
            if n != "echo": continue
            rows = det[(donor, n, k, r)]
            mm = lambda key: statistics.mean([x[key] for x in rows])
            up = mm("echoDealt") / mm("baseDealt") if mm("baseDealt") else 0
            print(f"    {donor:14}{'K%d r%.0f%%'%(k,r*100):>10}{mm('hits'):>8.1f}"
                  f"{mm('shadeHits'):>16.1f}{mm('baseDealt'):>10.0f}"
                  f"{mm('echoDealt'):>10.0f}{up:>8.0%}")
    assert not errors, errors[:3]
