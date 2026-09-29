#!/usr/bin/env python
"""v104 stage 6, scratch: DO THE STAGE-6 MUTANTS MOVE FIGHTS? The probe's own fights (Angelus both sides x
every other relic x N seeds from 104001 step 13, as `angelus_probe.py --seeds N`) played plainly on the
stage-6 link and on each mutant, one page per link, and compared record for record: the winner, the steps,
both fighters' hits, dealt, crits, clanks, final hp and position, and Angelus's rise tally.

    python mut_fights.py <fx link> <mutant> [<mutant> ...] [--seeds 2]
"""
import argparse, hashlib, json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("links", nargs="+")
ap.add_argument("--seeds", type=int, default=2)
a = ap.parse_args()
seeds = [104001 + 13 * i for i in range(a.seeds)]

JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "angelus");
  const out = [];
  for (const side of ["A", "B"]) for (const fid of ids) for (const sd of seeds){
    const m = side === "A" ? new AC.Match("angelus", fid, sd) : new AC.Match(fid, "angelus", sd);
    let st = 0;
    while (!m.over && st < 170 / DT){ m.step(DT); st++; }
    const me = m.a.w.id === "angelus" ? m.a : m.b, fo = me === m.a ? m.b : m.a, T = me.riseTally;
    out.push([side, fid, sd, m.winner ? (m.winner === me ? 1 : 0) : -1, st, me.hits, me.dealt, me.crits, me.clanks,
              fo.hits, fo.dealt, fo.crits, fo.clanks, me.hp, fo.hp, me.x, me.y, fo.x, fo.y,
              T ? [T.casts, T.shaftHits, T.bless, T.arrivals] : null]);
  }
  return out;
}"""

R = {}
for p in a.links:
    pp = pathlib.Path(p).resolve()
    with game(game_path=pp) as (page, errors):
        R[pp.name] = page.evaluate(JS, [seeds])
        assert not errors, errors[:3]
    print(f"  {pp.name}  {hashlib.sha256(pp.read_bytes()).hexdigest()[:16]}  {len(R[pp.name])} fights played", flush=True)
names = list(R)
ref = R[names[0]]
win = lambda rows: 100 * sum(1 for x in rows if x[3] == 1) / len(rows)
print(f"\nFIGHT FOR FIGHT against {names[0]} ({len(ref)} fights: Angelus both sides x {len(ref) // 2 // len(seeds)} foes x "
      f"{len(seeds)} seeds from 104001 step 13; win {win(ref):.1f}%)")
for n in names[1:]:
    ch = sum(1 for x, y in zip(ref, R[n]) if x != y)
    print(f"  {n:<36} {ch:>4} of {len(ref)} fights changed   win {win(R[n]):.1f}%")
