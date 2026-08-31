#!/usr/bin/env python3
"""WHAT IS EVERY ULTIMATE IN THE GAME WORTH? A/B against its own deletion.

The general form of v47's complaint -- nothing in the repo has ever asked
whether an ultimate delivers anything. One relic at a time: 25 foes x N seeds
with every ult live, then the SAME fights with only this relic's charge set to
1e9. Paired on seed and opponent, so the difference is the ultimate.

Runtime injection only; nothing is written.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = r"""([id, foes, seeds, secs, off]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const ch = w.ult ? w.ult.charge : null;
  if (off && w.ult) w.ult.charge = 1e9;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    out.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
               casts: me.ultsUsed || me.ultCount || 0, dur: step * DT });
  }
  if (ch !== null) w.ult.charge = ch;
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
ap.add_argument("--seeds", type=int, default=5)
ap.add_argument("--secs", type=float, default=120.0)
a = ap.parse_args()
seeds = [3301 + 19 * i for i in range(a.seeds)]

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    W = page.evaluate("""() => AC.WEAPONS.map(w => ({id:w.id, aff:w.aff, shape:w.shape,
        ult:(w.ult&&w.ult.name)||null, kind:(w.ult&&w.ult.kind)||null,
        charge:(w.ult&&w.ult.charge)||null, tip:(w.ult&&w.ult.tip)||null}))""")
    ids = [x["id"] for x in W]
    byid = {x["id"]: x for x in W}
    print(f"\nWHAT EVERY ULTIMATE IS WORTH — paired A/B against its own deletion")
    print(f"    {a.seeds} seeds x 25 foes = {25*a.seeds} fights an arm, "
          f"{2*26*25*a.seeds} fights total\n")
    res = []
    for id_ in ids:
        foes = [i for i in ids if i != id_]
        on = page.evaluate(JS, [id_, foes, seeds, a.secs, False])
        off = page.evaluate(JS, [id_, foes, seeds, a.secs, True])
        pair = {(r["foe"], r["seed"]): r for r in off}
        d = [(r, pair[(r["foe"], r["seed"])]) for r in on if (r["foe"], r["seed"]) in pair]
        d = [(x, y) for x, y in d if x["win"] >= 0 and y["win"] >= 0]
        wo = statistics.mean([x["win"] for x, y in d])
        wf = statistics.mean([y["win"] for x, y in d])
        flip = sum(1 for x, y in d if x["win"] != y["win"])
        res.append({"id": id_, "on": wo, "off": wf, "d": wo - wf, "n": len(d), "flip": flip})
    res.sort(key=lambda r: r["d"])
    print(f"    {'relic':14}{'ultimate':14}{'kind':9}{'chg':>5}"
          f"{'with':>7}{'without':>9}{'worth':>8}{'flips':>7}   tip")
    for r in res:
        w = byid[r["id"]]
        print(f"    {r['id']:14}{(w['ult'] or '-'):14}{(w['kind'] or '-'):9}"
              f"{(w['charge'] or 0):>5.0f}{r['on']:>7.1%}{r['off']:>9.1%}"
              f"{r['d']:>+8.1%}{r['flip']:>7}   {(w['tip'] or '')[:44]}")
    xs = [r["d"] for r in res]
    print(f"\n    mean worth {statistics.mean(xs):+.1%}   median {statistics.median(xs):+.1%}"
          f"   paired SE on a single relic is roughly "
          f"{(statistics.mean([r['flip'] for r in res])**0.5)/res[0]['n']:.1%}")
    assert not errors, errors[:3]
