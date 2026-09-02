#!/usr/bin/env python
"""THE BLADE, SWEPT AS A CURVE FIRST -- stage 4.

    python arclight_sweep.py --game ../02-chain/sc-static.html --blades 8.3,6,4,2,1 --seeds 10

CLAUDE.md's rule, learned three times and written down twice: **sweep a curve
first, every time**, and what settles a blade on this roster is a WIDE DIRECT
MEASUREMENT at n >= 1000 a point, on both sides, repeated on a second block --
never a bisection, which converges on the noise in its own tail.

THE QUESTION THIS TOOL EXISTS TO ANSWER IS NOT "WHICH BLADE" BUT "IS THERE
ONE". The four-arm price puts the whole of STATIC at 95.1% on the design's own
body (dmg 11.95) and at 95.5% on the shipped 8.3 -- a 3.65-point cut of the
blade, worth 27 points of win rate to the body with no ultimate, moved the
finished relic by 0.4. If that flatness holds down to a blade of 1 then the
blade cannot balance this relic and the answer is somewhere else, which is a
design decision and not this session's (CLAUDE.md section 3 rule 0).

`--side` runs the relic as A, as B, or both. Every sweep in `tools/` runs a new
relic as side A and `verify` runs it as side B in all of its pairings; the
asymmetry is small but it is real and it has never been written down for a
twinblade.
"""
from __future__ import annotations
import argparse, math, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

JS = r"""([rid, foes, seeds, secs, blades, side, knob, vals, combos]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = w.dmg, savedK = knob ? w.ult[knob] : null;
  const savedW = w.ult.ward, savedB = w.ult.dmg;
  const rows = [];
  /* CANDIDATE BUILDS, NOT A GRID. Three numbers move this relic and a grid of
     them is hundreds of arms; these are whole settings, each one a thing
     somebody could ship, priced side by side. Which one ships is a design
     decision (rule 0) -- this only says what each costs. */
  if (combos && combos.length){
    for (const c of combos){
      w.dmg = c[0]; w.ult.ward = c[1]; w.ult.dmg = c[2];
      const tag = c[0] + "/" + c[1] + "/" + c[2];
      for (const f of foes) for (const sd of seeds)
        for (const s of (side === "both" ? ["a", "b"] : [side])){
          const m = s === "a" ? new AC.Match(rid, f, sd)
                              : new AC.Match(f, rid, sd);
          const me = m.a.w.id === rid ? m.a : m.b;
          let step = 0;
          while (!m.over && step < secs / DT){ m.step(DT); step++; }
          rows.push({ bl: tag, foe: f, seed: sd, side: s,
                      win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                      dur: +(step * DT).toFixed(1), ults: me.ultsFired });
        }
    }
    w.dmg = saved; w.ult.ward = savedW; w.ult.dmg = savedB;
    return rows;
  }
  /* ONE AXIS AT A TIME. `--knob` sweeps a number inside the ULTIMATE at a
     fixed blade; without it the blade itself is the axis. Two axes in one run
     would be a grid nobody asked for and four times the fights. */
  const axis = knob ? vals : blades;
  for (const v of axis){
    if (knob){ w.ult[knob] = v; w.dmg = blades[0]; }
    else w.dmg = v;
    const bl = v;
    for (const f of foes){
      for (const sd of seeds){
        for (const s of (side === "both" ? ["a", "b"] : [side])){
          /* SIDE IS A REAL VARIABLE. `new AC.Match(x, y, seed)` puts x on side
             A, and a fight is not symmetric in it -- the spawn offsets differ.
             Every sweep in tools/ runs a new relic as A and `verify` runs it as
             B in all 33 of its pairings, so a blade chosen on one and passed on
             the other is being read by two instruments that disagree. */
          const m = s === "a" ? new AC.Match(rid, f, sd)
                              : new AC.Match(f, rid, sd);
          const me = m.a.w.id === rid ? m.a : m.b;
          let step = 0;
          while (!m.over && step < secs / DT){ m.step(DT); step++; }
          rows.push({ bl, foe: f, seed: sd, side: s,
                      win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                      dur: +(step * DT).toFixed(1), ults: me.ultsFired });
        }
      }
    }
  }
  w.dmg = saved;
  if (knob) w.ult[knob] = savedK;
  return rows;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-static.html")
    ap.add_argument("--relic", default="arclight")
    ap.add_argument("--blades", default="8.3,6,4,2,1")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--seed0", type=int, default=7717)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--side", default="a", choices=("a", "b", "both"))
    ap.add_argument("--knob", default="",
                    help="sweep a number inside the `ult` block instead of the "
                         "blade -- `dmg` (the 15 a bolt, which design open "
                         "decision 3 names as THE knob) or `ward` (the 2 a "
                         "bolt). The blade is held at the first --blades value.")
    ap.add_argument("--vals", default="",
                    help="the values for --knob")
    ap.add_argument("--combos", default="",
                    help="whole candidate settings, `blade:ward:boltdmg` "
                         "separated by commas -- e.g. 4:1:6,4:1:3,2:1:3. "
                         "Priced side by side, because three numbers move this "
                         "relic and a grid of them is hundreds of arms.")
    ap.add_argument("--noult", action="store_true",
                    help="stub the ultimate (charge 1e9) -- the FLOOR curve, "
                         "which is what says how much of this relic the blade "
                         "is even attached to")
    A = ap.parse_args()
    seeds = [A.seed0 + 97 * i for i in range(A.seeds)]
    blades = [float(x) for x in A.blades.split(",")]

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        ids = pg.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if A.relic not in ids:
            raise SystemExit(f"no `{A.relic}` in this build")
        foes = [i for i in ids if i != A.relic]
        if A.noult:
            pg.evaluate("(r) => { AC.WEAPONS.find(w => w.id === r).ult.charge "
                        "= 1e9; }", A.relic)
        vals = [float(x) for x in A.vals.split(",")] if A.vals else []
        if A.knob and not vals:
            raise SystemExit("--knob needs --vals")
        combos = [[float(y) for y in c.split(":")]
                  for c in A.combos.split(",")] if A.combos else []
        rows = pg.evaluate(JS, [A.relic, foes, seeds, A.secs, blades, A.side,
                                A.knob or None, vals, combos])

    per = len(foes) * len(seeds) * (2 if A.side == "both" else 1)
    print("\nARCLIGHT -- "
          + ("CANDIDATE SETTINGS, PRICED SIDE BY SIDE" if A.combos
             else f"ult.{A.knob} AS A CURVE, blade held at {blades[0]:g}"
             if A.knob else "THE BLADE AS A CURVE")
          + ("  (ULTIMATE STUBBED)" if A.noult else ""))
    print(f"  {A.game}, {len(foes)} foes x {len(seeds)} seeds"
          f"{' x 2 sides' if A.side == 'both' else f', side {A.side.upper()}'}"
          f" = {per} fights a point\n")
    head = ("blade/ward/bolt" if A.combos
            else ("ult." + A.knob if A.knob else "dmg"))
    print(f"    {head:>10}  {'win':>7}  {'+/- SE':>7}  {'ults/fight':>10}  "
          f"{'dur':>6}")
    out = []
    axis = ([f"{c[0]:g}/{c[1]:g}/{c[2]:g}"
             for c in ([[float(y) for y in c.split(":")]
                        for c in A.combos.split(",")])] if A.combos
            else (vals if A.knob else blades))
    for bl in axis:
        r = [x for x in rows if x["bl"] == bl and x["win"] >= 0]
        if not r:
            continue
        p = 100.0 * sum(x["win"] for x in r) / len(r)
        # A ROSTER WIN RATE IS NOT N INDEPENDENT FLIPS. This binomial figure is
        # a FLOOR on the error; two readings of one arm have come back 4-6
        # points apart above n=700. Read the curve, not the decimals.
        se = 100.0 * math.sqrt(max(1e-9, (p/100) * (1 - p/100)) / len(r))
        u = sum(x["ults"] for x in r) / len(r)
        d = sum(x["dur"] for x in r) / len(r)
        out.append((bl, p))
        lbl = f"{bl:>10.2f}" if isinstance(bl, float) else f"{bl:>10}"
        print(f"    {lbl}  {p:>6.1f}%  {se:>6.1f}   {u:>10.2f}  {d:>5.1f}s")

    if A.combos:
        print()
        for bl, p in out:
            band = "IN BAND" if 30 <= p <= 70 else ("high" if p > 70 else "low")
            print(f"    {bl:<16} {p:>6.1f}%   {band}")
        return 0
    cross = [i for i in range(1, len(out))
             if (out[i-1][1] - 50) * (out[i][1] - 50) <= 0]
    print()
    if cross:
        i = cross[0]
        (b0, p0), (b1, p1) = out[i-1], out[i]
        bx = b0 + (b1 - b0) * (50 - p0) / (p1 - p0) if p1 != p0 else b0
        print(f"  50% is crossed between {min(b0,b1):g} and "
              f"{max(b0,b1):g} -- linear interpolation says {bx:.2f}")
        print("  THAT IS A BRACKET AND NOT AN ANSWER. Confirm it with a wide")
        print("  direct measurement at n >= 1000 a point, both sides, on a")
        print("  second seed block (CLAUDE.md, v48 and v56).")
    else:
        lo, hi = min(p for _, p in out), max(p for _, p in out)
        print(f"  NO CROSSING IN THIS RANGE -- the curve runs {lo:.1f}% to "
              f"{hi:.1f}%.")
        if lo > 50:
            axis = f"`ult.{A.knob}`" if A.knob else "THE BLADE"
            print(f"  {axis} CANNOT BALANCE THIS RELIC ON ITS OWN, at the")
            print(f"  {'blade' if A.knob else 'ultimate'} this run held fixed.")
            print("  Stop and say so: what comes down next is a design")
            print("  decision (CLAUDE.md section 3 rule 0). The design names")
            print("  its own first knob -- open decision 3, 'the 15-a-bolt is")
            print("  the knob, not the radius'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
