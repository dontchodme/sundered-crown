#!/usr/bin/env python3
"""GLOAMWIRE'S BLADE. A CURVE FIRST, THEN A WIDE DIRECT MEASUREMENT.

    python gloamwire_sweep.py --game ../02-chain/sc-crossweave.html --only 0
    python gloamwire_sweep.py --game ../02-chain/sc-crossweave.html --only 1

`dmg 9.2` is the design's PREDICTION, measured on Chromium 141 at 29 relics
(`06-docs/v61/gloamwire-design-v61.md` sections 6 and 6.1). This settles it on
the pin at 31.

**THERE IS NO BISECTION IN THIS FILE AND THAT IS DELIBERATE.** CLAUDE.md says it
twice, and the second time it cost a whole damage point:

    A bisection converges on the noise in its tail. WHAT SETTLES A BLADE ON THIS
    ROSTER IS A WIDE DIRECT MEASUREMENT AT n >= 1000 A POINT, ON BOTH SIDES,
    REPEATED ON A SECOND SEED BLOCK.

Shroudmaul's bisection returned 19.92 and the answer was 21.00 -- and its
three-point confirmation was monotonic while being wrong, because it was drawn
on one seed block. Cindercleave's cheap curve read 47.6% where three wide blocks
read 52.5%, and the first explanation offered for the gap (side asymmetry) was
itself refuted: it was sample size. Both are why section [0] is a CURVE and not
a bracket, and why section [1] pays for what it claims.

  [0] THE CURVE, wide and cheap. Not to find the answer -- to find the REGION,
      and to see whether this relic's curve BENDS. Gravemourn's reads 67.3% at
      dmg 47.2 and 60.6% at 52.0: more blade made it worse, because bigger blows
      threw the quarry out of reach. A bisection started inside the wrong
      bracket cannot see that and converges happily.

  [1] THE WIDE DIRECT MEASUREMENT. Three points around the region, n >= 1000 a
      point a side, BOTH SIDES, on TWO seed blocks. `verify` pairs `i < j` and
      an appended relic is side B in all of its pairings, while every sweep in
      `tools/` runs it as side A -- a systematic difference between the
      instrument that tunes a relic and the instrument that passes it, measured
      at about -1.3pp on Cindercleave and never written down before that.

Runtime only. NOTHING is written to any build -- the blade goes into
`gloamwire_build.TUNED_GW` and stage 4 writes it.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RELIC = "gloamwire"

# One pass, one blade, both sides if asked. The weapon's `dmg` is written before
# the fights and put back after, so an arm is a number and never a re-patch.
SWEEP_JS = r"""([rid, foes, seeds, secs, dmg, side]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const keep = w.dmg;
  w.dmg = dmg;
  let wins = 0, n = 0, dur = 0, timeouts = 0;
  for (const f of foes){
    for (const sd of seeds){
      /* SIDE IS THE ARGUMENT ORDER AND NOTHING ELSE. `new Match(a, b, seed)`
         puts the first id on side A, and the arena is not symmetric -- the two
         start positions differ and the seed drives both. */
      const m = side === "a" ? new AC.Match(rid, f, sd) : new AC.Match(f, rid, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      n++; dur += step * DT;
      if (!m.winner) timeouts++;
      else if (m.winner === me) wins++;
    }
  }
  w.dmg = keep;
  return { wins, n, dur: dur / n, timeouts };
}"""


def run(page, foes, seeds, secs, dmg, side):
    return page.evaluate(SWEEP_JS, [RELIC, foes, seeds, secs, dmg, side])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
    ap.add_argument("--only", default="0")
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--curve", default="5,7,9.2,11.5,14,16.23",
                    help="[0] the blades the curve is read at")
    ap.add_argument("--curve-sn", type=int, default=8)
    ap.add_argument("--points", default="",
                    help="[1] three blades around the region -- from [0]")
    ap.add_argument("--wide-sn", type=int, default=34,
                    help="seeds a foe a side; 34 x 30 foes = 1020 a point a side")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    only = set(a.only.split(","))
    gp = resolve_game(a.game)
    out = {}

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, dmg:w.dmg}))")
        ids = {w["id"] for w in W}
        if RELIC not in ids:
            raise SystemExit(f"{gp.name} has no {RELIC}")
        foes = [w["id"] for w in W if w["id"] != RELIC]
        shipped = next(w["dmg"] for w in W if w["id"] == RELIC)
        print(f"\nGLOAMWIRE BLADE -- {gp.name}   {len(foes)} foes   "
              f"shipped dmg {shipped:g}\n")

        # ------------------------------------------------------------ [0] --
        if "0" in only:
            seeds = [5501 + 13 * i for i in range(a.curve_sn)]
            n = len(foes) * len(seeds)
            print(f"[0] THE CURVE -- {n} fights a point, side A. Wide and cheap,")
            print("    and it is here to find the REGION and to see whether the")
            print("    curve bends. It is NOT the answer.\n")
            print(f"    {'dmg':>7}{'win':>8}{'dur':>8}{'timeouts':>10}")
            rows = []
            for d in [float(x) for x in a.curve.split(",")]:
                r = run(page, foes, seeds, a.secs, d, "a")
                assert not errors, errors[:4]
                w = r["wins"] / r["n"]
                rows.append({"dmg": d, "win": w, "dur": r["dur"],
                             "timeouts": r["timeouts"], "n": r["n"]})
                print(f"    {d:>7.2f}{w:>8.1%}{r['dur']:>8.1f}{r['timeouts']:>10}")
            out["curve"] = rows

            # DOES IT BEND? Gravemourn's did, and a bracket chosen from a
            # bending curve is chosen wrong.
            ws = [r["win"] for r in rows]
            mono = all(ws[i] <= ws[i + 1] + 1e-9 for i in range(len(ws) - 1))
            print(f"\n    monotone in the blade: {'YES' if mono else 'NO'}")
            if not mono:
                print("    ** THE CURVE BENDS. Read v51 section 4.3 before")
                print("       choosing a bracket -- more blade can be worse,")
                print("       because bigger blows throw the quarry out of reach.")
            band = [r for r in rows if 0.40 <= r["win"] <= 0.60]
            if band:
                print(f"    the 40-60% region is dmg "
                      f"{min(r['dmg'] for r in band):g} to "
                      f"{max(r['dmg'] for r in band):g}")
            print("\n    NEXT: --only 1 --points <lo>,<mid>,<hi> from the region "
                  "above.")

        # ------------------------------------------------------------ [1] --
        if "1" in only:
            if not a.points:
                raise SystemExit(
                    "--only 1 needs --points, and they come from [0]'s curve.\n"
                    "  Choosing a bracket without a curve is what CLAUDE.md "
                    "calls\n  'a bisection started from a guessed bracket', and "
                    "it cost v53 a\n  whole damage point.")
            pts = [float(x) for x in a.points.split(",")]
            blocks = {"A": [7001 + 13 * i for i in range(a.wide_sn)],
                      "B": [91001 + 17 * i for i in range(a.wide_sn)]}
            per = len(foes) * a.wide_sn
            print(f"[1] THE WIDE DIRECT MEASUREMENT -- {per} fights a point a "
                  f"side a block,")
            print(f"    {per * 2 * 2 * len(pts)} in total. Both sides, two seed "
                  f"blocks, no bisection.\n")
            print(f"    {'dmg':>7}{'A-side':>9}{'B-side':>9}{'blockA':>9}"
                  f"{'blockB':>9}{'POOLED':>9}")
            rows = []
            for d in pts:
                cell = {}
                for bn, seeds in blocks.items():
                    for side in ("a", "b"):
                        r = run(page, foes, seeds, a.secs, d, side)
                        assert not errors, errors[:4]
                        cell[(bn, side)] = r
                wins = sum(c["wins"] for c in cell.values())
                nn = sum(c["n"] for c in cell.values())
                sideA = (cell[("A", "a")]["wins"] + cell[("B", "a")]["wins"]) / \
                        (cell[("A", "a")]["n"] + cell[("B", "a")]["n"])
                sideB = (cell[("A", "b")]["wins"] + cell[("B", "b")]["wins"]) / \
                        (cell[("A", "b")]["n"] + cell[("B", "b")]["n"])
                blkA = (cell[("A", "a")]["wins"] + cell[("A", "b")]["wins"]) / \
                       (cell[("A", "a")]["n"] + cell[("A", "b")]["n"])
                blkB = (cell[("B", "a")]["wins"] + cell[("B", "b")]["wins"]) / \
                       (cell[("B", "a")]["n"] + cell[("B", "b")]["n"])
                pooled = wins / nn
                rows.append({"dmg": d, "sideA": sideA, "sideB": sideB,
                             "blockA": blkA, "blockB": blkB,
                             "pooled": pooled, "n": nn})
                print(f"    {d:>7.2f}{sideA:>9.1%}{sideB:>9.1%}"
                      f"{blkA:>9.1%}{blkB:>9.1%}{pooled:>9.1%}")
            out["wide"] = rows

            print(f"\n    SIDE ASYMMETRY   "
                  f"{statistics.mean(r['sideA'] - r['sideB'] for r in rows):+.1%}"
                  f"   (Cindercleave measured about -1.3pp, and `verify` runs an")
            print("                     appended relic as side B in all of its "
                  "pairings)")
            print(f"    BLOCK DISAGREEMENT "
                  f"{max(abs(r['blockA'] - r['blockB']) for r in rows):.1%}"
                  f" worst   (two n=702 readings of one number once")
            print("                       differed by 4.3 points -- n~700 is a "
                  "floor, not a guarantee)")
            ws = [r["pooled"] for r in rows]
            mono = all(ws[i] <= ws[i + 1] + 1e-9 for i in range(len(ws) - 1))
            print(f"    MONOTONE: {'yes' if mono else 'NO -- the honest '
                                   'precision is the interval, not a decimal'}")
            # the crossing, by linear interpolation between the two points that
            # bracket 50% -- and it is reported as an INTERVAL, never a decimal
            # dressed up as an answer.
            cross = None
            for i in range(len(rows) - 1):
                lo, hi = rows[i], rows[i + 1]
                if (lo["pooled"] - 0.5) * (hi["pooled"] - 0.5) <= 0:
                    t = (0.5 - lo["pooled"]) / (hi["pooled"] - lo["pooled"])
                    cross = lo["dmg"] + t * (hi["dmg"] - lo["dmg"])
                    print(f"\n    50% crosses between dmg {lo['dmg']:g} and "
                          f"{hi['dmg']:g}, at about {cross:.2f}")
            if cross is None:
                print("\n    50% IS NOT INSIDE THESE POINTS -- widen and re-run.")
            out["cross"] = cross

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
