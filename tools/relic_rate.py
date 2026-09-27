#!/usr/bin/env python
"""ONE RELIC'S WIN RATE ON A BUILT LINK -- both sides, a seed block, live knobs.

    python relic_rate.py --game ../02-chain/sc-culverin.html --relic culverin \
        --n 10 --seed0 2207 [--sides AB] [--set dmg=13.2 ult.charge=14] \
        [--foes -ironhail] [--json out.json]

What settles a number on this roster is a wide direct measurement, BOTH SIDES,
repeated on a second seed block (v48/v56/v66; `corona_sweep`'s docstring has
the argument). This is that measurement lifted out of the per-relic sweeps so
the staff row's seven builds do not each rewrite it:

  * THE SAME SEED IS PLAYED FROM BOTH SIDES, so a side gap is a paired
    difference and not two samples of a roster. `verify` pairs `i < j` over
    WEAPONS, so an appended relic is side B in every one of its pairings;
    `ult_overlay` and the lab run it as side A. Both are printed.
  * `--set` mutates fields of the relic's own WEAPONS entry live (dotted paths:
    `dmg`, `ult.charge`, `shot.cadence`) and puts every one back in a
    `finally` -- a sweep that leaves the roster mutated poisons every later
    pass in the same page. A path that does not already exist is refused, so
    a typo cannot measure the unmodified relic under a new label.
  * `--foes -a,-b` drops foes (the lab that priced a staff used Ironhail as
    its donor, so its field is the 33 without Ironhail); `--foes a,b` keeps
    only those.

Seeds come from an LCG inside the page, `corona_sweep`'s, so two runs of one
block are the same fights. n is seeds per foe PER SIDE.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([id, n, seed0, sides, sets, foeSpec]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  if (!w) return { err: 'no relic ' + id };
  const undo = [];
  const at = (path) => { const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++){ o = o[ks[i]]; if (o == null) return null; }
    return [o, ks[ks.length - 1]]; };
  try {
    for (const [path, v] of sets){
      const r = at(path);
      if (!r || !(r[1] in r[0])) return { err: 'no field ' + path + ' on ' + id };
      undo.push([r[0], r[1], r[0][r[1]]]); r[0][r[1]] = v;
    }
    let ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
    const drop = foeSpec.filter(f => f.startsWith('-')).map(f => f.slice(1));
    const keep = foeSpec.filter(f => !f.startsWith('-'));
    if (keep.length) ids = ids.filter(x => keep.includes(x));
    ids = ids.filter(x => !drop.includes(x));
    const shape = Object.fromEntries(AC.WEAPONS.map(x => [x.id, x.shape]));
    const name = w.name;
    const out = { A: [0, 0], B: [0, 0], dur: 0, timeouts: 0, byFoe: {}, byType: {}, foes: ids.length };
    let s = seed0 >>> 0;
    for (const foe of ids){
      let fw = 0, fg = 0;
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        for (const side of sides){
          const r = side === 'A' ? AC.simulate(id, foe, s) : AC.simulate(foe, id, s);
          const win = r.winner === name ? 1 : 0;
          out[side][0] += win; out[side][1]++; fw += win; fg++;
          out.dur += r.duration; if (r.reason !== 'slain') out.timeouts++;
        }
      }
      out.byFoe[foe] = fw / fg;
      const t = out.byType[shape[foe]] || (out.byType[shape[foe]] = [0, 0]);
      t[0] += fw; t[1] += fg;
    }
    return out;
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; }
}"""


def parse(v):
    try: return json.loads(v)
    except Exception: return v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", required=True)
    ap.add_argument("--n", type=int, default=10, help="seeds per foe per side")
    ap.add_argument("--seed0", type=int, default=2207)
    ap.add_argument("--sides", default="AB")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--foes", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    sets = [(kv.split("=", 1)[0], parse(kv.split("=", 1)[1])) for kv in a.set]
    foes = [f for f in a.foes.split(",") if f]
    t0 = time.time()
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        r = page.evaluate(JS, [a.relic, a.n, a.seed0, list(a.sides), sets, foes])
        assert not errors, errors
    if "err" in r:
        raise SystemExit(r["err"])
    g = r["A"][1] + r["B"][1]
    rate = (r["A"][0] + r["B"][0]) / g
    rA = r["A"][0] / r["A"][1] if r["A"][1] else float("nan")
    rB = r["B"][0] / r["B"][1] if r["B"][1] else float("nan")
    print(f"{a.relic} on {pathlib.Path(a.game).name} · Chromium {ver} · {r['foes']} foes x {a.n} seeds"
          f" x sides {a.sides} = {g} fights · seed0 {a.seed0}"
          + (f" · set {' '.join(a.set)}" if a.set else "") + (f" · {a.label}" if a.label else ""))
    print(f"  win {rate:.1%}   side A {rA:.1%}   side B {rB:.1%}   "
          f"mean {r['dur']/g:.1f}s   timeouts {r['timeouts']}")
    print("  by type  " + "  ".join(f"{t} {v[0]/v[1]:.0%}" for t, v in
                                     sorted(r["byType"].items(), key=lambda kv: -kv[1][0]/kv[1][1])))
    worst = sorted(r["byFoe"].items(), key=lambda kv: kv[1])[:3]
    print("  worst    " + "  ".join(f"{k} {v:.0%}" for k, v in worst)
          + f"   ({g} fights in {time.time()-t0:.0f}s)")
    if a.json:
        out = dict(relic=a.relic, game=a.game, n=a.n, seed0=a.seed0, sides=a.sides, set=a.set,
                   foes=a.foes, rate=rate, rateA=rA, rateB=rB, games=g, dur=r["dur"] / g,
                   timeouts=r["timeouts"], byType={k: v[0] / v[1] for k, v in r["byType"].items()},
                   byFoe=r["byFoe"], chromium=ver)
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
