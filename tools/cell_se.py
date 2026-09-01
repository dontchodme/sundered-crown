#!/usr/bin/env python3
"""HOW BIG IS THE ERROR BAR ON A CELL PRICE, REALLY?

Every cell number in this project is quoted against "a per-cell SE of ~4pp",
which is sqrt(0.25/270) x sqrt(2) — the SE you get if 270 fights are 270
independent draws. They are not. A cell is 27 foes x 10 SEEDS, and the seed
sets the whole match's initial conditions, so the 27 fights sharing a seed are
correlated. The independent unit is the SEED, and there are ten of them.

This computes both: the naive binomial SE, and the seed-clustered SE — the
lift computed per seed, then the SE of the mean over seeds. Runtime only.
"""
import argparse, math, pathlib, statistics, sys
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--game", required=True)
ap.add_argument("--cell", required=True); ap.add_argument("--seeds", type=int, default=20)
ap.add_argument("--secs", type=float, default=120.0)
a = ap.parse_args()
sys.path.insert(0, str(pathlib.Path(a.repo) / "tools"))
from scpage import game
TYPE_DONOR = {"greatsword":"dawnbringer","twinblade":"widowmaker","warhammer":"grudgebearer",
              "scythe":"thornwake","flail":"gravemourn","bow":"ironhail"}
CHAN = {"bloodsworn":("onHit","hemorrhage",2),"dwarven":("onHit","sunder",1),
        "runic":("onHit","hex",1),"sanctified":("onHit","smite",1),
        "umbral":("onHit","curse",1),"verdant":("onHit","entangle",2),"vigil":("onSelf","ward",1)}
JS = r"""([donor, aff, slot, key, per, on, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff:w.aff, onHit:w.onHit?JSON.parse(JSON.stringify(w.onHit)):null,
                  onSelf:w.onSelf?JSON.parse(JSON.stringify(w.onSelf)):null };
  const charges = new Map();
  for (const x of AC.WEAPONS) if (x.ult) charges.set(x.id, x.ult.charge);
  for (const x of AC.WEAPONS) if (x.ult) x.ult.charge = 1e9;
  w.aff = aff; delete w.onHit; delete w.onSelf;
  if (on) { const o = {}; o[key] = per; w[slot] = o; }
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    let step = 0;
    while (!m.over && step < secs/DT){ m.step(DT); step++; }
    rows.push([f, sd, m.winner ? (m.winner === me ? 1 : 0) : -1]);
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  for (const x of AC.WEAPONS) if (x.ult) x.ult.charge = charges.get(x.id);
  return rows;
}"""
aff, typ = a.cell.split(":"); donor = TYPE_DONOR[typ]; slot, key, per = CHAN[aff]
seeds = [2207 + 11*i for i in range(a.seeds)]
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != donor]
    arms = {}
    for on in (False, True):
        arms[on] = page.evaluate(JS, [donor, aff, slot, key, per, on, foes, seeds, a.secs])
        assert not errors, errors
    n = len(foes)*len(seeds)
    print(f"{a.cell} on {donor} — {len(foes)} foes x {len(seeds)} seeds = {n} fights an arm\n")
    def rate(rows, pred=lambda r: True):
        d = [r for r in rows if r[2] >= 0 and pred(r)]
        return sum(r[2] for r in d)/len(d) if d else float("nan")
    off, on_ = rate(arms[False]), rate(arms[True])
    print(f"  floor {off:.1%}   channel {on_:.1%}   lift {(on_-off)*100:+.1f}pp\n")
    naive = math.sqrt(2*0.25/n)*100
    per_seed = [(rate(arms[True], lambda r,s=s: r[1]==s) - rate(arms[False], lambda r,s=s: r[1]==s))*100
                for s in seeds]
    per_foe  = [(rate(arms[True], lambda r,f=f: r[0]==f) - rate(arms[False], lambda r,f=f: r[0]==f))*100
                for f in foes]
    clust_seed = statistics.stdev(per_seed)/math.sqrt(len(seeds))
    clust_foe  = statistics.stdev(per_foe)/math.sqrt(len(foes))
    print(f"  naive binomial SE, 270 independent fights   {naive:>6.1f}pp   <- what the docs quote")
    print(f"  clustered on SEED  ({len(seeds)} clusters)              {clust_seed:>6.1f}pp")
    print(f"  clustered on FOE   ({len(foes)} clusters)              {clust_foe:>6.1f}pp")
    print(f"\n  per-seed lift spread  min {min(per_seed):+.1f}  max {max(per_seed):+.1f}"
          f"  sd {statistics.stdev(per_seed):.1f}")
    print(f"  per-foe  lift spread  min {min(per_foe):+.1f}  max {max(per_foe):+.1f}"
          f"  sd {statistics.stdev(per_foe):.1f}")
    print(f"\n  errors: {errors}")
