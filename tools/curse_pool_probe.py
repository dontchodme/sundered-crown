#!/usr/bin/env python3
"""DOES THE CURSE POOL KEEP IMPROVING, OR DOES IT FILL AND FREEZE?

The reworked curse is a MEMORY: three slots, each holding the damage of the
blow that filled it, a new blow displacing the weakest. So the pool is only a
live mechanic if the wielder's later blows are BIGGER than its earlier ones.
On a weapon whose every blow is the same size the pool fills in three hits and
never moves again — it is a constant with extra steps.

Grafts curse onto each type's donor at umbral's own weight, deletes the donor's
own channel and its ultimate, and records the foe's curseSum every 0.25s.

Reports, per type: the final pool, the time to 90% of it, and the share of the
fight spent at the final value. Runtime only; nothing is written to any build.
"""
import argparse, pathlib, statistics, sys, time
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=8); ap.add_argument("--secs", type=float, default=120.0)
a = ap.parse_args()
sys.path.insert(0, str(pathlib.Path(a.repo) / "tools"))
from scpage import game

DONOR = {"greatsword":"dawnbringer","twinblade":"widowmaker","warhammer":"grudgebearer",
         "scythe":"thornwake","flail":"gravemourn","bow":"ironhail"}

JS = r"""([donor, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff:w.aff, onHit:w.onHit?JSON.parse(JSON.stringify(w.onHit)):null,
                  onSelf:w.onSelf?JSON.parse(JSON.stringify(w.onSelf)):null };
  const charges = new Map();
  for (const x of AC.WEAPONS) if (x.ult) charges.set(x.id, x.ult.charge);
  for (const x of AC.WEAPONS) if (x.ult) x.ult.charge = 1e9;
  w.aff = "umbral"; delete w.onHit; delete w.onSelf; w.onHit = { curse: 1 };
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let step = 0, acc = 0; const trace = [];
    while (!m.over && step < secs/DT){
      m.step(DT); step++; acc += DT;
      if (acc >= 0.25){ acc = 0; trace.push(+th.curseSum().toFixed(4)); }
    }
    out.push({ trace, dur: step*DT, pool: th.cursePool.slice(), hits: me.hits });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  for (const x of AC.WEAPONS) if (x.ult) x.ult.charge = charges.get(x.id);
  return out;
}"""

seeds = [2207 + 11*i for i in range(a.seeds)]
t0 = time.time()
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    print(f"curse grafted onto every type's donor, {a.seeds} seeds x {len(ids)-1} foes\n")
    print(f"  {'type':<12}{'final pool':>11}{'blade dmg':>11}{'t to 90%':>10}"
          f"{'share of fight AT final':>25}{'hits':>7}")
    for typ, d in DONOR.items():
        foes = [i for i in ids if i != d]
        rows = page.evaluate(JS, [d, foes, seeds, a.secs])
        assert not errors, errors
        fin, t90, frac = [], [], []
        for r in rows:
            tr = r["trace"]
            if not tr or tr[-1] <= 0: continue
            F = max(tr)
            fin.append(F)
            k = next(i for i, v in enumerate(tr) if v >= 0.90*F)
            t90.append((k+1)*0.25)
            frac.append(sum(1 for v in tr if v >= F-1e-9)/len(tr))
        dmg = page.evaluate("(d)=>AC.WEAPONS.find(x=>x.id===d).dmg", d)
        print(f"  {typ:<12}{statistics.mean(fin):>11.1f}{dmg:>11.1f}"
              f"{statistics.mean(t90):>10.2f}s{statistics.mean(frac):>24.0%}"
              f"{statistics.mean(r['hits'] for r in rows):>7.1f}", flush=True)
    print(f"\n  done in {time.time()-t0:.0f}s   errors: {errors}")
