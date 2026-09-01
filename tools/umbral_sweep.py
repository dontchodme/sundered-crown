#!/usr/bin/env python3
"""THREE BLADES, RE-SWEPT UNDER A CURSE THAT REMEMBERS.

    python umbral_sweep.py --game ../02-chain/sc-curse.html

STAGE 1b of the v51/52 build brief. All three umbral blades were tuned under
the OLD curse -- a permanent maximum-life drain that delivered ~3% of its
nominal -- and against ultimates carrying an `apply:{curse:3}` that is now
deleted. Every one of those numbers is stale:

    gravemourn 44.10      nightfell 15.83      twinshade 8.30

TWINSHADE IS THE ONE THAT GETS FORGOTTEN in a package named after the other
two. Nobody is touching Triplicate, but it is the ultimate the rework helps
most in the game (+36.0 worth) -- three bodies feeding and cashing one shared
pool -- and its 8.30 was tuned under the dead curse.

## WHY THIS IS NOT JUST A BISECTION

`dmg` now moves THREE channels at once: the blade, the pool (which is made of
blade damage), and the echo (which is a share of the pool). The response is
superlinear, and a bisection that assumes a monotonic linear response lands in
the wrong place. Brief §4.5 registered that before it was seen.

And a bisection converges on NOISE IN ITS TAIL. v48's escalating bisection
returned 16.04 with its last three steps reading 42.9 / 45.3 / 44.6% across
half a damage point -- an ordering that is sampling error, not signal. A
direct measurement at a wider sample put the crossing 0.76 higher.

So this runs THREE passes, and the third is the answer:

    1  A WIDE SWEEP, printed as a curve. Cheap, and it is the only thing that
       can show a non-monotonic response. It also brackets the crossing with
       two measured points instead of a guess.
    2  AN ESCALATING BISECTION inside that bracket, sample rising with the
       step so the last call is the widest.
    3  A WIDE DIRECT CONFIRMATION at the answer and at one point either side.
       If the ordering across those three is not monotonic, the bisection
       landed in noise and this SAYS SO rather than reporting a number.

Then the telemetry at the answer, because a blade that hits 50% for the wrong
reason is still wrong: what share of the relic's delivered damage is the echo,
how deep the pool gets, and how often it is full.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

UMBRAL = ["gravemourn", "nightfell", "twinshade", "shroudmaul"]

# The bracket to sweep, per relic. Wide on purpose -- the point of pass 1 is
# to SEE the curve, and a range that only just contains the answer cannot show
# that the response bends.
RANGE = {
    "gravemourn": (28.0, 52.0),
    "nightfell":  (9.0, 21.0),
    "twinshade":  (4.5, 12.0),
    # SHROUDMAUL, AND ITS SURFACE IS THE SIMPLE ONE. The warning at the top of
    # this file -- that `dmg` moves three channels at once and the response is
    # superlinear -- applies to the other three and NOT to this one. GRASP
    # carries no damage and reads nothing: it is a hold, and a hold is worth
    # the same whatever the blade is. So `dmg` here moves the blade and the
    # pool and stops, which is one channel fewer than any umbral relic tuned
    # so far.
    #
    # AND IT MAY NOT NEED TO MOVE AT ALL, which has not happened in this
    # chain before. `grab_lab` put the relic at 52.0% against a field of 50.0%
    # with the §1's placeholder numbers, so the bracket is deliberately
    # NARROWER than the other three -- but it is still a bracket and not a
    # point, because v53 measured Gravemourn's curve BENDING DOWNWARD past
    # 47.2 and a bisection cannot see the shape it is standing on.
    "shroudmaul": (16.0, 32.0),
}


# THE WIN RATE, OVER THE WHOLE FIELD. v41 open decision 2, closed the
# expensive way: a blade bisected on a five-foe subset read 50% and the full
# field read 55.2% on the same number.
WIN_JS = r"""([id, dmg, n, seed0, pins]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg;
  /* PINS. The three umbral blades are being retuned against a field that
     CONTAINS the other two, so tuning them one at a time and stopping is a
     fixed point nobody checked. Every pass here can pin the others at their
     current answers, and the last pass in main() pins all three at once. */
  const saved = {};
  for (const k of Object.keys(pins || {})){
    const x = AC.WEAPONS.find(y => y.id === k);
    if (x && k !== id){ saved[k] = x.dmg; x.dmg = pins[k]; }
  }
  w.dmg = dmg;
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  const byFoe = {};
  try {
    for (const foe of ids){
      let fw = 0;
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(id, foe, s);
        if (r.winner === w.name){ win++; fw++; }
        games++; dur += r.duration;
        if (r.reason !== "slain") timeouts++;
      }
      byFoe[foe] = fw / n;
    }
  } finally {
    w.dmg = d0;
    for (const k of Object.keys(saved)) AC.WEAPONS.find(y => y.id === k).dmg = saved[k];
  }
  return { win, games, rate: win / games, dur: dur / games, timeouts, byFoe };
}"""


# THE SHAPE AT THE ANSWER. A blade that reaches 50% by being a bigger blade is
# not the same relic as one that reaches it by remembering harder, and the win
# column cannot tell them apart.
TEL_JS = r"""([id, dmg, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg;
  w.dmg = dmg;
  let dealt = 0, echo = 0, blows = 0, echoBlows = 0, fights = 0;
  let poolSum = 0, poolFrames = 0, fullFrames = 0, anyFrames = 0, peak = 0;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(id, foeId, sd); fights++;
        const me = m.a.w.id === id ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        const origRH = P.resolveHit;
        m.resolveHit = function(self, foe){
          const e = Math.round(foe.curseEcho());
          blows++;
          if (e > 0){ echo += e; echoBlows++; }
          return origRH.apply(m, arguments);
        };
        let step = 0;
        while (!m.over && step < secs / DT){
          m.step(DT); step++;
          /* THE POOL ON THE QUARRY, sampled every frame -- what the relic has
             actually built up, not what it could in principle hold. */
          const n = th.cursePool.length;
          anyFrames++;
          if (n > 0){
            poolFrames++;
            const s = th.curseSum();
            poolSum += s;
            peak = Math.max(peak, s);
            if (n >= AC.STATUS.curse.maxStacks) fullFrames++;
          }
        }
        dealt += me.dealt;
      }
    }
  } finally { w.dmg = d0; }
  return { dealt, echo, blows, echoBlows, fights,
           poolMean: poolFrames ? poolSum / poolFrames : 0,
           poolUp: anyFrames ? poolFrames / anyFrames : 0,
           poolFull: anyFrames ? fullFrames / anyFrames : 0, peak };
}"""


def sweep(page, rid, lo, hi, pts, n, seed0, pins):
    """Pass 1 -- the curve. Returns [(dmg, rate, games, dur)]."""
    out = []
    for i in range(pts):
        d = lo + (hi - lo) * i / (pts - 1)
        r = page.evaluate(WIN_JS, [rid, d, n, seed0 + i * 17, pins])
        out.append((d, r["rate"], r["games"], r["dur"]))
        print(f"      {d:>7.2f}  {r['rate'] * 100:>5.1f}%  n={r['games']:<5} "
              f"mean {r['dur']:.1f}s  timeouts {r['timeouts']}")
    return out


def bracket(curve, target=0.50):
    """The two measured points that straddle the target, or None.

    A NON-MONOTONIC CURVE CAN STRADDLE THE TARGET MORE THAN ONCE, and that is
    exactly what §4.5 warns this surface can do. Take the LAST crossing and
    say how many there were -- a second crossing is a finding, not a detail.
    """
    xs = [c for c in curve]
    cross = []
    for i in range(len(xs) - 1):
        a, b = xs[i], xs[i + 1]
        if (a[1] - target) * (b[1] - target) <= 0 and a[1] != b[1]:
            cross.append((a[0], b[0]))
    return (cross[-1] if cross else None), len(cross)


def bisect(page, rid, lo, hi, target, steps, base, top, seed0, pins):
    """Pass 2 -- escalating sample, so the last call is the widest."""
    t0, fights, hist = time.time(), 0, []
    for i in range(steps):
        n = max(base, round(base * (top / base) ** (i / max(1, steps - 1))))
        mid = (lo + hi) / 2
        r = page.evaluate(WIN_JS, [rid, mid, n, seed0 + i, pins])
        fights += r["games"]
        hist.append((mid, r["rate"], r["games"], r["dur"]))
        print(f"      {mid:>7.2f}  {r['rate'] * 100:>5.1f}%  n={r['games']:<5} "
              f"mean {r['dur']:.1f}s")
        if r["rate"] < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2, fights, hist


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-curse.html")
    ap.add_argument("--relics", default=",".join(UMBRAL))
    # STAGE 2b MOVES THE BRACKET, because the relic moved. Gravemourn was
    # swept in 1b with no ultimate and read 76.0% once it had one, so the
    # 28..52 bracket in RANGE cannot contain the answer any more. Named on
    # the command line rather than edited into the constant: the constant
    # is the record of where these relics sit WITHOUT their new ultimates.
    ap.add_argument("--lo", type=float, default=0.0)
    ap.add_argument("--hi", type=float, default=0.0)
    ap.add_argument("--pts", type=int, default=6, help="pass 1 sweep points")
    ap.add_argument("--sn", type=int, default=4, help="pass 1 seeds per pairing")
    ap.add_argument("--steps", type=int, default=6, help="pass 2 bisection steps")
    ap.add_argument("--base", type=int, default=2)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--cn", type=int, default=14, help="pass 3 seeds per pairing")
    ap.add_argument("--jn", type=int, default=40,
                    help="seeds per pairing in the JOINT pass — high on "
                         "purpose, see the note beside it")
    ap.add_argument("--target", type=float, default=0.50)
    ap.add_argument("--secs", type=float, default=130.0)
    # RE-RUN THE JOINT PASS WITHOUT RE-SPENDING THE SWEEP. The three-pass
    # search costs ~7500 fights and the joint confirmation costs ~1100, so a
    # tool that can only do both together makes re-checking the fixed point
    # expensive enough to skip -- which is how a fixed point goes unchecked.
    ap.add_argument("--answers", default="",
                    help="e.g. gravemourn=39.79,nightfell=15.90 — skip the "
                         "search and run only the joint confirmation")
    A = ap.parse_args()

    path = resolve_game(A.game)
    print(f"\nTHE THREE UMBRAL BLADES, re-swept against {path.name}")
    spent = 0
    answers = {}

    with game(game_path=path) as (page, errors):
        C = page.evaluate("() => JSON.parse(JSON.stringify(AC.STATUS.curse))")
        print(f"  curse   maxStacks {C['maxStacks']}  echo {C.get('echo')}  "
              f"dur {C['dur']}")
        foes = page.evaluate("() => AC.WEAPONS.map(w => w.id)")

        # EACH RELIC IS SWEPT AGAINST THE OTHER TWO AT WHATEVER HAS BEEN
        # DECIDED SO FAR, so the third sweep is not run against two stale
        # blades. The joint pass at the end is what closes the loop.
        pins = {}
        if A.answers:
            for part in A.answers.split(","):
                k, _, v = part.partition("=")
                answers[k.strip()] = (float(v), float(v), [], True)
            print("  --answers given: skipping the search, confirming only")
        for rid in ([] if A.answers else A.relics.split(",")):
            lo, hi = RANGE[rid]
            if A.lo or A.hi:
                lo, hi = (A.lo or lo), (A.hi or hi)
            d0 = page.evaluate("([id]) => AC.WEAPONS.find(x => x.id === id).dmg",
                               [rid])
            print(f"\n  ---- {rid.upper()}   ships at dmg {d0:g}  "
                  f"(tuned under the dead curse) ----")

            print(f"    pass 1  the curve, {A.pts} points across {lo:g}..{hi:g}")
            curve = sweep(page, rid, lo, hi, A.pts, A.sn, 4000, pins)
            spent += sum(c[2] for c in curve)
            br, ncross = bracket(curve, A.target)
            if br is None:
                print(f"    NO CROSSING of {A.target * 100:.0f}% inside "
                      f"{lo:g}..{hi:g} -- widen RANGE[{rid!r}] and re-run. "
                      f"Reporting no answer rather than a bisection into a "
                      f"bracket that does not contain one.")
                continue
            if ncross > 1:
                print(f"    !! {ncross} crossings of {A.target * 100:.0f}% in "
                      f"this range. The response is NOT monotonic -- §4.5 said "
                      f"it might not be. Taking the last; read the curve.")
            print(f"    pass 2  bisecting inside {br[0]:.2f}..{br[1]:.2f}")
            ans, f2, hist = bisect(page, rid, br[0], br[1], A.target,
                                   A.steps, A.base, A.top, 7000, pins)
            spent += f2

            # PASS 3. The bisection's tail is where it converges on noise, so
            # the answer is confirmed against a WIDE sample at three points --
            # and the ordering across them is the check, not the middle value.
            step = max(0.25, (br[1] - br[0]) / 4)
            print(f"    pass 3  wide confirmation at {ans:.2f} +/- {step:.2f}, "
                  f"n={A.cn} a pairing")
            conf = []
            for j, d in enumerate((ans - step, ans, ans + step)):
                r = page.evaluate(WIN_JS, [rid, d, A.cn, 9000 + j, pins])
                conf.append((d, r["rate"], r["games"]))
                spent += r["games"]
                print(f"      {d:>7.2f}  {r['rate'] * 100:>5.1f}%  "
                      f"n={r['games']:<5} mean {r['dur']:.1f}s")
            mono = conf[0][1] <= conf[1][1] <= conf[2][1]
            if not mono:
                print("      !! NOT MONOTONIC across the confirmation. The "
                      "bisection landed in its own sampling noise; the answer "
                      "below is the WIDE middle point, and the interval is "
                      "the honest precision.")
            # the answer is the wide measurement, corrected toward the target
            # by linear interpolation across whichever confirmation pair
            # straddles it -- three wide points beat seven narrowing ones
            best = ans
            for j in range(2):
                a, b = conf[j], conf[j + 1]
                if (a[1] - A.target) * (b[1] - A.target) <= 0 and a[1] != b[1]:
                    best = a[0] + (b[0] - a[0]) * \
                        (A.target - a[1]) / (b[1] - a[1])
            answers[rid] = (best, ans, conf, mono)
            pins[rid] = best
            print(f"    ANSWER  dmg {best:.2f}   (bisection said {ans:.2f}; "
                  f"the wide confirmation moved it {best - ans:+.2f})")

            t = page.evaluate(TEL_JS, [rid, best,
                                       [f for f in foes if f != rid][:8],
                                       [5000 + i * 733 for i in range(5)],
                                       A.secs])
            share = t["echo"] / t["dealt"] if t["dealt"] else 0
            print(f"    shape   {share * 100:.1f}% of what it delivers is the "
                  f"echo   pool mean {t['poolMean']:.0f} peak {t['peak']:.0f}   "
                  f"up {t['poolUp'] * 100:.0f}% of the fight, full "
                  f"{t['poolFull'] * 100:.0f}%")
            print(f"            {t['echoBlows']} of {t['blows']} blows landed "
                  f"on a pool with something in it")

        # ---- THE JOINT PASS, AND IT IS THE ONE THAT CLOSES THE LOOP.
        # Each relic above was swept against a field CONTAINING the other two,
        # at whatever they happened to be worth at the time. Three relics
        # tuned one at a time and then all applied at once is a fixed point
        # nobody checked. This measures every answer with all three in place.
        # If a relic drifts off target here, the three interact and the honest
        # report is this table rather than the sweep's own number.
        #
        # AND IT NEEDS A BIGGER SAMPLE THAN THE SEARCH DOES, which is why it
        # takes its own. Measured: Nightfell at 15.96 read 50.3% and at 15.90
        # read 56.0% -- 0.06 of a damage point apart, 5.7pp apart, both at
        # n=364. A roster win rate is 26 pairings of correlated fights, not
        # 364 independent coin flips, so its real precision is far worse than
        # the binomial figure and a 3pp verdict at n=364 is a verdict about
        # seeds. `--jn` defaults high for that reason.
        if len(answers) > 1:
            pinned = {k: v[0] for k, v in answers.items()}
            print(f"\n  ---- ALL THREE AT ONCE, n={A.jn} a pairing ----")
            for rid, (best, _a, _c, _m) in answers.items():
                r = page.evaluate(WIN_JS, [rid, best, A.jn, 11000, pinned])
                drift = (r["rate"] - A.target) * 100
                print(f"    {rid:12s} dmg {best:6.2f}  {r['rate'] * 100:5.1f}%  "
                      f"n={r['games']:<5} mean {r['dur']:.1f}s  "
                      f"{drift:+.1f}pp off target"
                      + ("   <- outside 3pp, the three interact"
                         if abs(drift) > 3 else ""))
                spent += r["games"]

        if errors:
            print("\n  page errors:")
            for e in errors[:10]:
                print("   ", e)

    print(f"\n  {spent} fights spent\n")
    print("  THE NUMBERS TO WRITE INTO THE BUILDER (they do NOT go in the")
    print("  HTML -- CLAUDE.md §4.9, twelve values were lost that way once):")
    for rid, (best, ans, conf, mono) in answers.items():
        print(f"    {rid:12s} {best:.2f}" + ("" if mono else
              "   <- confirmation not monotonic, read the table"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
