#!/usr/bin/env python3
"""REBUILDING DIRGE AND ECLIPSE ON THE ECHO POOL.

Base curse for every arm is the v49 recommendation: K=3, echo 8%, permanent,
displacement kept, priced on the TARGET so shade blows count.

`strip` is the CONTROL: the ultimate keeps its damage, its knock and its
picture, and loses only its worthless `apply:{curse:3}`. Every other arm is
`strip` plus one new payload, so the column reads as what the REBUILD is
worth, not what the relic is worth -- the blade gets re-swept afterwards and
will absorb the level.

  detonate M   read the pool, EMPTY it, then deal M x pool. Consumed then
               priced, per Slagburst: a spend that is also multiplied by what
               it just ate pays itself twice.
  keepbest M   detonate M, but the largest entry survives the spend
  deepen  +n   the foe's Curse cap rises by n, permanently, this fight
  amplify N/s  the echo rate is multiplied by N for s seconds
  mirror       every slot is overwritten with a copy of the pool's largest

BOTH shapes are run on BOTH relics on purpose. The design claim is that
Gravemourn wants the lump sum (biggest pool, fewest blows) and Nightfell wants
the deeper pool (2.6x the blows). If that is wrong, this table says so.

Runtime injection only; nothing is written.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = r"""([donor, foes, seeds, secs, K0, RATE, MODE, P1, P2]) => {
  const DT = AC.CONFIG.physics.dt, CU = AC.STATUS.curse;
  const oL = CU.maxHpLoss, oC = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  const origFire = AC.Match.prototype.fireUlt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const savedApply = w.ult.apply;
  delete w.ult.apply;                       // the broken payload, gone in every arm
  CU.maxHpLoss = 0; CU.maxStacks = K0;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const pool = [];
    let K = K0, ampUntil = -1;
    let inR = false, hitSrc = null, hitD0 = 0;
    let echoDealt = 0, spendDealt = 0, baseDealt = 0, hits = 0, casts = 0;
    let spendPool = 0, biggest = 0;

    const trim = () => { pool.sort((a,b)=>b-a); while (pool.length > K) pool.pop(); };
    const origApply = th.apply.bind(th);
    th.apply = function(key, n){
      if (key === "curse"){
        const v = inR ? (hitSrc.dealt - hitD0) : 0;
        if (v > 0){ for (let i=0;i<n;i++) pool.push(v); trim(); }
      }
      return origApply(key, n);
    };

    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      if (foe !== th) return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      const d0 = self.dealt, h0 = self.hits;
      let s = 0; for (const v of pool) s += v;
      const rate = (ampUntil > this.t) ? RATE * P1 : RATE;
      const echo = Math.round(s * (MODE === "amplify" ? rate : RATE));
      inR = true; hitSrc = self; hitD0 = d0;
      origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      inR = false;
      if (self.hits === h0) return;
      hits++; baseDealt += self.dealt - d0;
      if (echo > 0 && foe.alive){ this.hurt(foe, echo, self); echoDealt += echo; }
    };

    m.fireUlt = function(fr, foe){
      const r = origFire.call(this, fr, foe);
      if (fr !== me || foe !== th) return r;
      casts++;
      if (MODE === "detonate" || MODE === "keepbest"){
        /* READ, EMPTY, THEN DEAL. */
        let s = 0; for (const v of pool) s += v;
        const best = pool.length ? pool[0] : 0;
        pool.length = 0;
        if (MODE === "keepbest" && best > 0) pool.push(best);
        const d = Math.round(s * P1);
        spendPool += s; if (s > biggest) biggest = s;
        if (d > 0 && foe.alive){ this.hurt(foe, d, fr); fr.dealt += d; spendDealt += d; }
      } else if (MODE === "deepen"){
        K += P1; CU.maxStacks = K;
      } else if (MODE === "amplify"){
        ampUntil = this.t + P2;
      } else if (MODE === "mirror"){
        const mx = pool.length ? pool[0] : 0;
        if (mx > 0){ pool.length = 0; for (let i=0;i<K;i++) pool.push(mx); }
      }
      return r;
    };

    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    CU.maxStacks = K0;
    rows.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                echoDealt, spendDealt, baseDealt, hits, casts,
                spendPool: casts ? spendPool / casts : 0, biggest });
  }
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  if (savedApply) w.ult.apply = savedApply;
  return rows;
}"""

ARMS = [("strip", 0, 0), ("detonate", 0.6, 0), ("detonate", 1.0, 0), ("detonate", 1.5, 0),
        ("keepbest", 1.0, 0), ("deepen", 2, 0), ("deepen", 3, 0),
        ("amplify", 2.0, 8.0), ("mirror", 0, 0)]

def label(mode, p1, p2):
    return {"strip": "strip", "detonate": f"det x{p1}", "keepbest": f"keep x{p1}",
            "deepen": f"deepen +{int(p1)}", "amplify": f"amp x{p1}/{int(p2)}s",
            "mirror": "mirror"}[mode]

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
    print(f"\nREBUILDING THE TWO UMBRAL ULTIMATES — curse K={a.K}, echo {a.rate:.0%}")
    print(f"    {a.seeds} seeds x 25 foes = {25*a.seeds} fights an arm, ults ON\n")
    for donor in ["gravemourn", "nightfell"]:
        foes = [i for i in ids if i != donor]
        base = None
        print(f"  {donor.upper()}")
        print(f"    {'arm':14}{'win':>8}{'worth':>8}{'casts':>7}{'pool at cast':>14}"
              f"{'spend dmg':>11}{'echo dmg':>10}{'blade dmg':>11}")
        for mode, p1, p2 in ARMS:
            rows = page.evaluate(JS, [donor, foes, seeds, a.secs, a.K, a.rate, mode, p1, p2])
            fin = [r for r in rows if r["win"] >= 0]
            wr = sum(r["win"] for r in fin) / len(fin)
            if base is None: base = wr
            mm = lambda k: statistics.mean([r[k] for r in rows])
            print(f"    {label(mode,p1,p2):14}{wr:>8.1%}{wr-base:>+8.1%}{mm('casts'):>7.2f}"
                  f"{mm('spendPool'):>14.0f}{mm('spendDealt'):>11.0f}"
                  f"{mm('echoDealt'):>10.0f}{mm('baseDealt'):>11.0f}")
        print()
    assert not errors, errors[:3]
