#!/usr/bin/env python3
"""SHROUDMAUL, SWEPT -- the floor, the one knob that moves the ultimate, the
held-seconds law re-measured ON THE BUILT RELIC, the one knob that is not free,
and the type ladder.

    python shroudmaul_sweep.py --game ../02-chain/sc-grasp.html --only 0,1

    [0] THE FLOOR — the relic with `charge` at 1e9, which is the same OFF the
        v55b charge sweep used. The brief's stage-2 gate: ~27%.
    [1] THE GRAB COUNT — 2 to 6, Rick's own range, and the WHOLE balance
        decision. Open decision 1 is 4 against 5.
    [2] THE HELD-SECONDS LAW, RE-MEASURED. `grab_lab` fitted
        `lift = +3.1 + 2.62 x held` at r2 0.79 on Grudgebearer standing in.
        This asks whether it still holds on the relic that was actually built,
        which is the brief's registered prediction and its own falsifier.
    [3] REACH — the one number in this ultimate that is NOT free. 140 cost 2.7
        points and 300 cost 4.0 AT THE SAME HELD SECONDS, because a hold is
        only worth what the hammer can reach.
    [4] THE TYPE LADDER — the foe's TYPE, not the foe. Open item 12: Thornshear
        loses four fights in five to every bow and wins 62% against greatswords
        at an overall 47.0%, so NO per-relic band in this repo can see it. A
        relic that stops the other fighter moving is exactly the shape that
        could be lopsided by type, and nobody has looked.

THE BLADE IS NOT HERE. It goes through `umbral_sweep.py`, which already runs
the wide-curve / escalating-bisection / wide-confirmation pass this project
settled on and has now been extended to four relics:

    python umbral_sweep.py --game ../02-chain/sc-grasp.html --relics shroudmaul

Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "shroudmaul"

# THE WIN RATE OVER THE WHOLE FIELD. v41 open decision 2, closed the expensive
# way: a blade bisected on a five-foe subset read 50% and the full field read
# 55.2% on the same number. And v53 §3.1: nothing below n~700 ranks anything on
# this roster -- two measurements of the SAME arm at n=156 and n=208 came back
# 50.6% and 63.9%, because a roster win rate is 27 pairings of CORRELATED
# fights and not N independent flips.
WIN_JS = r"""([rid, over, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = {};
  for (const k of Object.keys(over || {})){ saved[k] = w.ult[k]; w.ult[k] = over[k]; }
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== rid);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  const byFoe = {};
  try {
    for (const foe of ids){
      let fw = 0;
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(rid, foe, s);
        if (r.winner === w.name){ win++; fw++; }
        games++; dur += r.duration;
        if (r.reason !== "slain") timeouts++;
      }
      byFoe[foe] = fw / n;
    }
  } finally {
    for (const k of Object.keys(saved)) w.ult[k] = saved[k];
  }
  return { rate: win / games, games, dur: dur / games, timeouts, byFoe };
}"""


# HELD SECONDS, WHICH IS 30x CHEAPER TO MEASURE THAN A WIN RATE AND IS WHAT THE
# WIN RATE IS MADE OF. Stepped rather than `simulate`d, because the scalar the
# design is priced on is not in `summary()` and never will be -- it is a
# property of an object that is nulled the moment it matters.
HELD_JS = r"""([rid, over, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = {};
  for (const k of Object.keys(over || {})){ saved[k] = w.ult[k]; w.ult[k] = over[k]; }
  let held = 0, grabs = 0, crushes = 0, casts = 0, fights = 0, dur = 0;
  let blows = 0, foeBlows = 0, pool = 0, poolFrames = 0;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, foeId, sd);
        const me = m.a.w.id === rid ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        fights++;
        const oFire = m.fireUlt.bind(m);
        m.fireUlt = function(f){ if (f === me) casts++; return oFire.apply(m, arguments); };
        let step = 0;
        while (!m.over && step < secs / DT){
          const G0 = me.ultGrasp, g0 = G0 ? G0.grabs : 0;
          m.step(DT); step++;
          const G1 = me.ultGrasp;
          /* AN ORDINARY GRAB is visible on the far side of the step; THE CRUSH
             IS NOT, because it nulls the window on the frame it lands. Both
             are counted, and the second one is why this cannot be a one-liner. */
          if (G1 && G1.grabs > g0){ grabs += G1.grabs - g0; held += G1.holdMax; }
          else if (G0 && !G1 && me.graspCrush){ grabs++; crushes++; held += G0.holdMax; }
          poolFrames++; pool += th.curseSum();
        }
        dur += step * DT;
        blows += me.hits; foeBlows += th.hits;
      }
    }
  } finally {
    for (const k of Object.keys(saved)) w.ult[k] = saved[k];
  }
  return { held: held / fights, grabs: grabs / fights, crushes: crushes / fights,
           casts: casts / fights, dur: dur / fights, fights,
           blows: blows / fights, foeBlows: foeBlows / fights,
           pool: poolFrames ? pool / poolFrames : 0 };
}"""

TYPES = {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-grasp.html")
    ap.add_argument("--only", default="")
    ap.add_argument("--n", type=int, default=20,
                    help="seeds a pairing for a win rate (27 foes x n fights)")
    ap.add_argument("--hn", type=int, default=6,
                    help="seeds a pairing for a HELD measurement")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    A = ap.parse_args()
    gp = resolve_game(A.game)
    want = set(A.only.split(",")) if A.only else None
    out, t0 = {}, time.time()

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        shapes = page.evaluate("() => Object.fromEntries("
                               "AC.WEAPONS.map(w => [w.id, w.shape]))")
        U = page.evaluate("([r]) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(x => x.id === r).ult))", [RID])
        foes = [i for i in ids if i != RID]
        seeds = [7717 + 23 * i for i in range(A.hn)]
        print(f"\nSHROUDMAUL — swept against {len(foes)} foes, {gp.name}")
        print(f"  shipped: n {U['n']}  radius {U['radius']:g}  dur {U['dur']:g}  "
              f"cadence {U['cadence']:g}  grab {U['grabStun']:g}  "
              f"true {U['trueStun']:g}  charge {U['charge']:g}")
        print(f"  win rates are {len(foes)} x {A.n} = {len(foes) * A.n} fights; "
              f"held is {len(foes)} x {A.hn} = {len(foes) * A.hn}\n")

        def win(lab, over, seed0):
            r = page.evaluate(WIN_JS, [RID, over, A.n, seed0])
            print(f"    {lab:<24}{r['rate']:>7.1%}  n={r['games']:<5} "
                  f"mean {r['dur']:>5.1f}s  timeouts {r['timeouts']}")
            return r

        def held(lab, over):
            r = page.evaluate(HELD_JS, [RID, over, foes, seeds, A.secs])
            print(f"    {lab:<24}{r['held']:>7.2f}s{r['casts']:>7.2f}"
                  f"{r['grabs']:>7.1f}{r['crushes']:>7.2f}{r['blows']:>7.1f}"
                  f"{r['foeBlows']:>6.1f}{r['pool']:>7.1f}{r['dur']:>7.1f}s")
            return r

        HHDR = (f"    {'arm':<24}{'held':>8}{'casts':>7}{'grabs':>7}"
                f"{'crush':>7}{'blows':>7}{'foe':>6}{'pool':>7}{'fight':>8}")

        # ------------------------------------------------------------- [0] --
        # THE FLOOR. `charge` 1e9 is the same OFF the v55b charge sweep used:
        # the clock can never reach it, `fireUlt` never runs, and the relic is
        # a blade and a channel and nothing else.
        floor = None
        if not want or "0" in want:
            print("[0] THE FLOOR — the relic with no ultimate at all "
                  "(charge 1e9), against grab_lab's 27.1%\n")
            floor = win("no ultimate", {"charge": 1e9}, 5501)
            base = win("as shipped", {}, 5501)
            print(f"\n    the ultimate is worth "
                  f"{base['rate'] - floor['rate']:+.1%} over this relic's own "
                  f"floor, against a field median of +21.8%")
            out["floor"] = floor["rate"]
            out["shipped"] = base["rate"]

        # ------------------------------------------------------------- [1] --
        if not want or "1" in want:
            print("\n[1] THE GRAB COUNT — Rick's own 2 to 6, and the WHOLE "
                  "balance decision.\n    Nothing else has to move with it. "
                  "OPEN DECISION 1 is 4 against 5.\n")
            if floor is None:
                floor = win("no ultimate", {"charge": 1e9}, 5501)
                print()
            rows = {}
            for nn in [2, 3, 4, 5, 6]:
                r = win(f"n = {nn}" + ("   <- shipped" if nn == U["n"] else ""),
                        {"n": nn}, 6100 + nn)
                rows[nn] = r["rate"]
            print(f"\n    lift over the floor:  " + "  ".join(
                f"n{k} {v - floor['rate']:+.1%}" for k, v in rows.items()))
            out["grabCount"] = rows

        # ------------------------------------------------------------- [2] --
        if not want or "2" in want:
            print("\n[2] THE HELD-SECONDS LAW, RE-MEASURED ON THE BUILT RELIC."
                  "\n    grab_lab: lift = +3.1 + 2.62 x held, r2 0.79, "
                  "residual sd 2.7pp.\n    If this does not hold here, the law "
                  "was an artefact of one relic and every\n    knob has to be "
                  "re-priced separately (brief §6).\n")
            print(HHDR)
            arms = [("n = 2", {"n": 2}), ("n = 3", {"n": 3}), ("n = 4", {"n": 4}),
                    ("n = 5  <- shipped", {}), ("n = 6", {"n": 6}),
                    ("window 4s", {"dur": 4.0}), ("window 12s", {"dur": 12.0}),
                    ("grab hold 0.8s", {"grabStun": 0.8}),
                    ("true stun 4.0s", {"trueStun": 4.0})]
            hs, ls = [], []
            if floor is None:
                floor = win("no ultimate", {"charge": 1e9}, 5501)
            for lab, over in arms:
                h = held(lab, over)
                w2 = page.evaluate(WIN_JS, [RID, over, A.n, 7300])
                hs.append(h["held"]); ls.append((w2["rate"] - floor["rate"]) * 100)
                print(f"    {'':<24}{'':>8}  win {w2['rate']:.1%}  "
                      f"lift {w2['rate'] - floor['rate']:+.1%}  "
                      f"law says {3.1 + 2.62 * h['held']:+.1f}%  "
                      f"resid {(w2['rate'] - floor['rate']) * 100 - (3.1 + 2.62 * h['held']):+.1f}pp")
            if len(hs) > 2:
                mh, ml = statistics.mean(hs), statistics.mean(ls)
                sxy = sum((x - mh) * (y - ml) for x, y in zip(hs, ls))
                sxx = sum((x - mh) ** 2 for x in hs)
                syy = sum((y - ml) ** 2 for y in ls)
                b = sxy / sxx if sxx else 0
                r = sxy / (sxx * syy) ** 0.5 if sxx and syy else 0
                res = [y - (ml - b * mh + b * x) for x, y in zip(hs, ls)]
                sd = statistics.pstdev(res)
                print(f"\n    REFIT ON THE BUILT RELIC: "
                      f"lift = {ml - b * mh:+.1f} + {b:.2f} x held   "
                      f"r {r:+.3f}  r2 {r * r:.2f}  residual sd {sd:.1f}pp")
                print(f"    grab_lab said              "
                      f"lift = +3.1 + 2.62 x held   r +0.889  r2 0.79  "
                      f"residual sd 2.7pp")
                out["law"] = {"a": ml - b * mh, "b": b, "r2": r * r, "sd": sd}

        # ------------------------------------------------------------- [3] --
        if not want or "3" in want:
            print("\n[3] REACH — the ONE number in this ultimate that is not "
                  "free.\n    grab_lab: 140 costs 2.7 points and 300 costs 4.0 "
                  "AT THE SAME HELD SECONDS,\n    because a hold is only worth "
                  "what the hammer can reach.\n")
            print(HHDR)
            for rr in [140.0, 200.0, 260.0, 320.0]:
                h = held(f"radius {rr:g}" + ("  <- shipped"
                                             if rr == U["radius"] else ""),
                         {"radius": rr})
                w2 = page.evaluate(WIN_JS, [RID, {"radius": rr}, A.n, 7900])
                print(f"    {'':<24}{'':>8}  win {w2['rate']:.1%}  "
                      f"law says {3.1 + 2.62 * h['held']:+.1f}% over the floor")

        # ------------------------------------------------------------- [4] --
        if not want or "4" in want:
            print("\n[4] THE TYPE LADDER — by the foe's TYPE, not by the foe."
                  "\n    OPEN ITEM 12: Thornshear reads 47.0% overall and "
                  "18.6% against the five bows,\n    so no per-relic band in "
                  "this repo can see it. A relic whose ultimate STOPS the\n"
                  "    other fighter moving is exactly the shape that could be "
                  "lopsided by type.\n")
            r = win("as shipped", {}, 8800)
            byType = {}
            for foe, rate in r["byFoe"].items():
                byType.setdefault(shapes[foe], []).append((foe, rate))
            print()
            for t in sorted(byType, key=lambda k: -statistics.mean(
                    [x[1] for x in byType[k]])):
                rows = sorted(byType[t], key=lambda x: x[1])
                m = statistics.mean([x[1] for x in rows])
                print(f"    {t:<12}{m:>7.1%}  n={len(rows)}   "
                      f"worst {rows[0][0]} {rows[0][1]:.0%}   "
                      f"best {rows[-1][0]} {rows[-1][1]:.0%}")
            spread = (max(statistics.mean([x[1] for x in v]) for v in byType.values())
                      - min(statistics.mean([x[1] for x in v]) for v in byType.values()))
            print(f"\n    overall {r['rate']:.1%}, type spread "
                  f"{spread * 100:.1f}pp   (Thornshear's is 43.6pp)")
            out["byType"] = {k: statistics.mean([x[1] for x in v])
                             for k, v in byType.items()}

        assert not errors, errors[:4]

    print(f"\n  {time.time() - t0:.0f}s")
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1))
        print(f"  wrote {A.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
