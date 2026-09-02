#!/usr/bin/env python
"""DUSKREAVE'S BLADE, SWEPT AS A CURVE BEFORE ANYTHING IS CHOSEN.

    python duskreave_sweep.py --game ../02-chain/sc-lastthree.html

Rick, 2026-09-02, shown Duskreave at 96.2% on `verify`: *"lets drop the damage.
drop it to 1 if you have to."*

**A CURVE, NOT A BISECTION, AND THAT IS THE HOUSE RULE.** CLAUDE.md has the same
lesson from v48, v56 and v59: a bisection converges on the noise in its tail and
cannot see the shape of what it is walking down. v53 found a blade curve that
BENDS DOWNWARD -- Gravemourn reads 67.3% at dmg 47.2 and 60.6% at 52.0, because
bigger blows throw the quarry out of reach of a weapon that lands 5.6 times a
fight. "Sweep a curve first. Every time."

**AND THE QUESTION HERE IS NOT WHERE THE CROSSING IS. It is whether there is
one.** At `dmg` 21 this relic's blade is a minority of its damage -- 483 ticks
carried 4,306 damage in 16 fights, against a blade landing about seven blows --
so the honest thing to test first is the FLOOR: if `dmg 1` still leaves
Duskreave far above the band, the blade is not the lever and no amount of
cutting it will be, and that is a finding rather than a failure. It is why 1 is
in the sweep even though nothing would ever ship there.

`dmg` is injected at runtime and NOTHING IS WRITTEN. The chosen value goes into
`duskreave_build.py` by hand, the way every tuned number in this project does
(CLAUDE.md 4.9: twelve converged values were once written into an HTML and lost
on the next rebuild).
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

JS = r"""([rid, dmg, tick, foes, seeds, secs, side]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const was = w.dmg, wasT = w.ult.dmg;
  /* TWO AXES, BECAUSE THEY ARE TWO DIFFERENT RELICS' WORTH OF DAMAGE. `dmg` is
     the BLADE -- about seven blows a fight. `ult.dmg` is what ONE TICK deals
     before the curse echo is folded on, and there are 7 of those a second for
     up to ten seconds. Rick, 2026-09-02: "i ment drop the ults damage to 1 per
     tick if you have to." Passing null leaves either where it is. */
  if (dmg !== null) w.dmg = dmg;
  if (tick !== null) w.ult.dmg = tick;
  const DT = AC.CONFIG.physics.dt;
  let win = 0, n = 0, dur = 0;
  for (const f of foes) for (const sd of seeds){
    /* BOTH SIDES, and it is an argument the roster has already had. `verify`
       pairs `i < j`, so a newly appended relic runs as side B in every one of
       its pairings while every sweep in `tools/` runs it as side A -- measured
       elsewhere at about 1.3pp. A blade settled on one side is settled against
       a number the other instrument will not reproduce. */
    const m = side === 0 ? new AC.Match(rid, f, sd) : new AC.Match(f, rid, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    if (m.winner){ win += (m.winner === me ? 1 : 0); n++; dur += step * DT; }
  }
  w.dmg = was; w.ult.dmg = wasT;
  return { win: win, n: n, dur: n ? dur / n : 0 };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-lastthree.html")
    ap.add_argument("--relic", default="duskreave")
    ap.add_argument("--axis", default="tick", choices=("tick", "blade"),
                    help="which damage to sweep. `tick` is ult.dmg, what ONE "
                         "tick deals; `blade` is w.dmg")
    ap.add_argument("--blades", default="1,5,9,13,17,21")
    ap.add_argument("--ticks", default="1,2,3,4,5")
    ap.add_argument("--n", type=int, default=18,
                    help="seeds per foe per side. 18 x 32 foes x 2 sides = "
                         "1152 fights a point, which clears the n~700 floor")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--block", type=int, default=0,
                    help="seed block. Run it twice with different blocks -- "
                         "two readings of one arm have come back 4-6 points "
                         "apart above the floor")
    A = ap.parse_args()

    vals = ([float(x) for x in A.ticks.split(",")] if A.axis == "tick"
            else [float(x) for x in A.blades.split(",")])
    seeds = [7717 + A.block * 100003 + 23 * i for i in range(A.n)]

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        ids = pg.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != A.relic]
        print(f"\nDUSKREAVE'S BLADE -- a curve, block {A.block}, "
              f"{len(foes)} foes x {A.n} seeds x 2 sides = "
              f"{len(foes)*A.n*2} fights a point\n")
        print(f"    {A.axis:>6}{'side A':>9}{'side B':>9}{'POOLED':>9}"
              f"{'mean dur':>10}")
        rows = []
        for d in vals:
            dm = None if A.axis == "tick" else d
            tk = d if A.axis == "tick" else None
            a = pg.evaluate(JS, [A.relic, dm, tk, foes, seeds, A.secs, 0])
            b = pg.evaluate(JS, [A.relic, dm, tk, foes, seeds, A.secs, 1])
            wa = a["win"] / max(1, a["n"])
            wb = b["win"] / max(1, b["n"])
            pooled = (a["win"] + b["win"]) / max(1, a["n"] + b["n"])
            dur = (a["dur"] + b["dur"]) / 2
            rows.append((d, wa, wb, pooled))
            print(f"    {d:>6.2f}{wa:>8.1%}{wb:>9.1%}{pooled:>9.1%}"
                  f"{dur:>9.1f}s")
        if errs:
            print("\n  PAGE ERRORS:", *errs[:4], sep="\n    ")

    lo = min(r[3] for r in rows)
    print()
    if lo > 0.70:
        print("  THIS AXIS IS NOT THE LEVER, AND THAT IS THE FINDING.")
        print(f"  The floor of this curve is {lo:.1%} -- at dmg "
              f"{rows[[r[3] for r in rows].index(lo)][0]:g}, which is below")
        print("  anything that would ever ship. Duskreave does not get into")
        print("  band on this axis alone. What is left is the tick RATE, the")
        print("  window's duration, and the band's HEIGHT -- which was doubled")
        print("  for the picture and doubles the catch. All three are Rick's.")
    else:
        cross = None
        for i in range(len(rows) - 1):
            if (rows[i][3] - 0.5) * (rows[i+1][3] - 0.5) <= 0:
                x0, y0 = rows[i][0], rows[i][3]
                x1, y1 = rows[i+1][0], rows[i+1][3]
                cross = x0 + (0.5 - y0) * (x1 - x0) / max(1e-9, (y1 - y0))
        if cross is not None:
            print(f"  50% crosses near dmg {cross:.2f}. THAT IS A BRACKET AND "
                  f"NOT AN ANSWER --")
            print("  confirm it with a wide direct measurement at that value")
            print("  and its neighbours, on a SECOND seed block (--block 1).")
            print("  Two readings of one arm on this roster have come back 4-6")
            print("  points apart above the n~700 floor.")
        else:
            print("  no 50% crossing inside this range -- widen `--blades`.")
    print("\n  NOTHING WAS WRITTEN. The chosen value goes into "
          "`duskreave_build.py`\n  by hand (CLAUDE.md 4.9).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
