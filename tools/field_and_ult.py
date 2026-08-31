#!/usr/bin/env python3
"""[3] THE FIELD — the yardstick any donor number has to be read against.
   [4] THE ULT-STACK AUDIT — under 'drop the weakest', what happens to the
       three ultimates whose entire payload is Curse (Dirge 3, Eclipse 3,
       Interment 8)?  Runtime only; nothing is written."""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

FIELD_JS = r"""([ids, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = {}, n = {};
  for (const id of ids){ w[id] = 0; n[id] = 0; }
  for (let i = 0; i < ids.length; i++)
   for (let j = i + 1; j < ids.length; j++)
    for (const sd of seeds){
      const m = new AC.Match(ids[i], ids[j], sd);
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      if (!m.winner) continue;
      n[ids[i]]++; n[ids[j]]++;
      if (m.winner === m.a) w[m.a.w.id]++; else w[m.b.w.id]++;
    }
  return ids.map(id => ({ id, win: n[id] ? w[id] / n[id] : null, n: n[id] }));
}"""

ULT_JS = r"""([donor, foes, seeds, secs, K, RATE]) => {
  const DT = AC.CONFIG.physics.dt;
  const CU = AC.STATUS.curse;
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
    let pool = [];                       // [{v, ult}]
    let inR = false, hitD0 = 0;
    let ultApplied = 0, ultDisplaced = 0, ultPaid = 0, blaPaid = 0, hits = 0;
    let ultEverPaid = 0, ultLife = 0;    // payouts an ult stack survived to see

    const origApply = th.apply.bind(th);
    th.apply = function(key, n){
      if (key === "curse"){
        const isUlt = !inR;
        const v = inR ? (me.dealt - hitD0) : ULTD;
        if (isUlt) ultApplied += n;
        if (v > 0){
          for (let i = 0; i < n; i++) pool.push({ v, ult: isUlt, paid: 0 });
          pool.sort((a, b) => b.v - a.v);
          while (pool.length > K){
            const drop = pool.pop();
            if (drop.ult){ ultDisplaced++; ultLife += drop.paid; if (drop.paid) ultEverPaid++; }
          }
        } else if (isUlt) { ultApplied += 0; }
      }
      return origApply(key, n);
    };

    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      if (!(self === me && foe === th))
        return origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      const d0 = self.dealt, h0 = self.hits;
      let s = 0, su = 0;
      for (const p of pool){ s += p.v; if (p.ult) su += p.v; }
      const echo = Math.round(s * RATE);
      inR = true; hitD0 = d0;
      origResolve.call(this, self, foe, hx, hy, seg, mul, over);
      inR = false;
      if (self.hits === h0) return;
      hits++;
      if (echo > 0 && foe.alive){
        this.hurt(foe, echo, self);
        const share = s > 0 ? su / s : 0;
        ultPaid += echo * share; blaPaid += echo * (1 - share);
        for (const p of pool) p.paid++;
      }
    };

    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    for (const p of pool) if (p.ult){ ultLife += p.paid; if (p.paid) ultEverPaid++; }
    const ultLeft = pool.filter(p => p.ult).length;
    rows.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                hits, ultApplied, ultDisplaced, ultLeft, ultEverPaid,
                ultPaid, blaPaid, ultD: ULTD });
  }
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  return rows;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--rate", type=float, default=0.08)
    ap.add_argument("--skip-field", action="store_true")
    a = ap.parse_args()
    gp = (HERE / a.game).resolve()
    seeds = [3301 + 19 * i for i in range(a.seeds)]

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, aff:w.aff, shape:w.shape, dmg:w.dmg}))")
        ids = [w["id"] for w in W]
        byid = {w["id"]: w for w in W}

        if not a.skip_field:
            print(f"\n[3] THE FIELD — every pairing, shipped damage, ults ON, {a.seeds} seeds")
            fr = page.evaluate(FIELD_JS, [ids, seeds, a.secs])
            fr = [r for r in fr if r["win"] is not None]
            ws = sorted(fr, key=lambda r: -r["win"])
            print(f"    {'relic':14}{'aff':12}{'shape':12}{'win':>7}{'n':>6}")
            for r in ws:
                w = byid[r["id"]]
                mark = "   <-- umbral" if w["aff"] == "umbral" else ""
                print(f"    {r['id']:14}{w['aff']:12}{w['shape']:12}{r['win']:>6.1%}{r['n']:>6}{mark}")
            xs = [r["win"] for r in ws]
            print(f"\n    field mean {statistics.mean(xs):.1%}   sd {statistics.pstdev(xs):.1%}   "
                  f"range {min(xs):.1%}..{max(xs):.1%}   (n {ws[0]['n']} a relic, "
                  f"binomial SE {(0.25/ws[0]['n'])**0.5:.1%})")

        print(f"\n[4] THE ULT-STACK AUDIT — K={a.K}, rate {a.rate:.0%}, ults ON")
        print("    Dirge, Eclipse and Interment exist to apply Curse. Under "
              "'drop the weakest'\n    a stack that remembers a small number is "
              "displaced by the wielder's own blade.\n")
        print(f"    {'donor':14}{'ult remembers':>14}{'stacks/fight':>13}"
              f"{'displaced':>10}{'ever paid':>10}{'echo from ult':>14}{'from blade':>12}")
        for donor in ["gravemourn", "nightfell", "twinshade"]:
            foes = [i for i in ids if i != donor]
            rows = page.evaluate(ULT_JS, [donor, foes, seeds, a.secs, a.K, a.rate])
            m = lambda k: statistics.mean([r[k] for r in rows])
            ap_ = m("ultApplied")
            print(f"    {donor:14}{rows[0]['ultD']:>14.0f}{ap_:>13.1f}"
                  f"{m('ultDisplaced'):>10.1f}{m('ultEverPaid'):>10.1f}"
                  f"{m('ultPaid'):>14.0f}{m('blaPaid'):>12.0f}")
        assert not errors, errors[:3]


main()
