#!/usr/bin/env python
"""STAGE 1 == ARM A, FIGHT FOR FIGHT (v104, scratch).

Plays every (foe, seed) of ult_overlay's blocks twice: on the BASE with the donor
mutated exactly as ult_overlay's arm A does (widowmaker as sanctified x twinblade,
onHit smite 1, its own ultimate at 1e9), and on the stage-1 LINK as `angelus`.
Each fight's record is compared: winner, steps, both hits/dealt/crits/clanks and
both final hp. The control plays the base's donor UNMUTATED (bloodsworn, its ult
still off) and must differ.
"""
import argparse, json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--link", required=True)
ap.add_argument("--foes", required=True)
ap.add_argument("--seed0", type=int, nargs="+", default=[2207, 2317])
ap.add_argument("--seeds", type=int, default=20)
ap.add_argument("--out", required=True)
a = ap.parse_args()
foes = a.foes.split(",")
seeds = [s0 + 11 * i for s0 in a.seed0 for i in range(a.seeds)]

JS = r"""([rid, mutate, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = { aff: w.aff, onHit: w.onHit, onSelf: w.onSelf, charge: w.ult.charge };
  if (mutate === "cell"){ w.aff = "sanctified"; delete w.onHit; delete w.onSelf; w.onHit = { smite: 1 }; }
  w.ult.charge = 1e9;
  const out = [];
  try {
    for (const fid of foes) for (const sd of seeds){
      const m = new AC.Match(rid, fid, sd);
      let st = 0;
      while (!m.over && st < 160 / DT){ m.step(DT); st++; }
      const me = m.a, fo = m.b;
      out.push([fid, sd, m.winner ? (m.winner === me ? 1 : 0) : -1, st, me.hits, me.dealt, me.crits, me.clanks,
                fo.hits, fo.dealt, fo.crits, fo.clanks, me.hp, fo.hp]);
    }
  } finally { w.aff = saved.aff; delete w.onHit; delete w.onSelf;
              if (saved.onHit) w.onHit = saved.onHit; if (saved.onSelf) w.onSelf = saved.onSelf; w.ult.charge = saved.charge; }
  return out;
}"""

def run(path, rid, mutate):
    with game(game_path=pathlib.Path(path).resolve()) as (page, errors):
        r = page.evaluate(JS, [rid, mutate, foes, seeds])
        assert not errors, errors
    return r

lab = run(a.base, "widowmaker", "cell")
built = run(a.link, "angelus", "none")
ctl = run(a.base, "widowmaker", "none")
same = sum(1 for x, y in zip(lab, built) if x == y)
cdiff = sum(1 for x, y in zip(lab, ctl) if x != y)
wl = sum(1 for x in lab if x[2] == 1) / sum(1 for x in lab if x[2] >= 0)
wb = sum(1 for x in built if x[2] == 1) / sum(1 for x in built if x[2] >= 0)
first = next(((x, y) for x, y in zip(lab, built) if x != y), None)
lines = [f"STAGE 1 vs ARM A, fight for fight: {len(foes)} foes x {len(seeds)} seeds (blocks {a.seed0}) = {len(lab)} fights",
         f"  identical records (winner, steps, both hits/dealt/crits/clanks, both hp): {same}/{len(lab)}",
         f"  win: lab arm A {wl:.2%}   built stage 1 {wb:.2%}",
         f"  CONTROL (the donor unmutated, bloodsworn): {cdiff}/{len(lab)} records differ from arm A -- the comparison can fail",
         f"  first difference: {first}"]
print("\n".join(lines))
pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
sys.exit(0 if same == len(lab) and cdiff > 0 else 1)
