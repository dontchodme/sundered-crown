#!/usr/bin/env python3
"""GRASP'S RHYTHM — fewer, slower, longer grabs, priced at CONSTANT BALANCE.

    python grasp_rhythm_lab.py --game ../02-chain/sc-grasp.html

Rick, watching the second build: *"its still pretty confusing what the ult is
actually doing by just watching it. can we add a cooldown for how often it can
grab but make the stun longer?"*

## THIS IS THE ONE TRADE THIS ULTIMATE GIVES AWAY FOR FREE, AND IT HAS NEVER
## BEEN SPENT

`06-docs/v56/grab-v56.md`, fourteen arms at 702 fights each:

    lift = +3.1 + 2.62 x held seconds     r2 0.79, residual sd 2.7pp against a
                                          per-arm SE of 5.3pp

The residuals are smaller than the measurement error, so **window length, grab
cadence, grab hold, true-stun length and grab count are five ways of writing
one number.** Which means the ARRANGEMENT is free: any shape delivering the
same held seconds is worth the same, and every remaining choice can be made for
the picture.

No other ultimate in this game has had that property, and until now nothing had
used it. This is what it is for.

## WHAT IS ACTUALLY WRONG WITH THE SHIPPED RHYTHM, MEASURED

    cadence 0.6   grabStun 0.5   n 5   window 8.0

    the whole ultimate resolves in 4.79s — 60% of its own window
    five grabs a mean 1.11s apart
    the quarry is locked 45% of that, in half-second pieces

**Five near-identical half-second events inside five seconds.** Nothing is on
screen long enough to be read as a cause, and the window's back 40% is empty.
The escalation to the fifth is the only structure in it and it goes by in the
time it takes to notice the first.

## WHAT THIS MEASURES

Every arm is judged on TWO axes that have nothing to do with each other:

    BALANCE     `held` seconds a fight. Must land on the shipped 9.66 or the
                blade moves and stage 3b has to be re-run.
    LEGIBILITY  grabs a cast (fewer is clearer), seconds between them (longer
                is clearer), how much of the 8s window the ultimate occupies
                (more is better — an empty back half is a dead set-piece), and
                the share of the window the quarry is actually locked for.

The last one has a CEILING, not a maximum: at 100% the quarry never moves
between grabs and the ultimate reads as one long freeze, which is the
Crucible's verb and the thing this relic is not allowed to be. Somewhere near
two thirds is a hold with visible releases in it.

Injection is runtime-only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "shroudmaul"

# THE WIN RATE, BOTH SIDES. §5a of the build write-up: `verify` runs a newly
# appended relic as side B in all 27 of its pairings while every sweep in
# `tools/` runs it as side A, and the blade was a whole damage point wrong for
# a related reason. Measure both and the question cannot arise.
WIN_JS = r"""([rid, over, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = {};
  for (const k of Object.keys(over || {})){ saved[k] = w.ult[k]; w.ult[k] = over[k]; }
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== rid);
  let s = seed0 >>> 0, win = 0, g = 0, dur = 0;
  try {
    for (const foe of ids) for (let k = 0; k < n; k++){
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const ra = AC.simulate(rid, foe, s); if (ra.winner === w.name) win++; g++; dur += ra.duration;
      const rb = AC.simulate(foe, rid, s); if (rb.winner === w.name) win++; g++; dur += rb.duration;
    }
  } finally {
    for (const k of Object.keys(saved)) w.ult[k] = saved[k];
  }
  return { rate: win / g, n: g, dur: dur / g };
}"""

# HELD, AND THE FOUR LEGIBILITY COLUMNS. Stepped rather than `simulate`d,
# because none of this is in `summary()` and never will be -- every one of them
# is a property of an object that is nulled the moment it matters.
RHY_JS = r"""([rid, over, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = {};
  for (const k of Object.keys(over || {})){ saved[k] = w.ult[k]; w.ult[k] = over[k]; }
  const U = w.ult;
  let fights = 0, casts = 0, crushes = 0, held = 0, grabs = 0;
  let fill = 0, fillN = 0, gap = 0, gapN = 0, lockIn = 0, winIn = 0;
  try {
    for (const foeId of foes) for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      fights++;
      let step = 0, castT = null, lastGrab = null, lastCastGrabs = 0;
      while (!m.over && step < secs / DT){
        const G0 = me.ultGrasp, g0 = G0 ? G0.grabs : 0, had = !!G0;
        m.step(DT); step++;
        const G = me.ultGrasp, t = step * DT;
        if (!had && G){ casts++; castT = t; lastGrab = null; }
        /* THE SHARE OF THE WINDOW THE QUARRY IS ACTUALLY LOCKED FOR, sampled
           per step while a window is open. `th.stun` is the real thing -- not
           the grab count, not the hand -- because it is what the mechanic
           writes and what a viewer sees stop. */
        if (G){ winIn += DT; if (th.stun > 0) lockIn += DT; }
        const g1 = G ? G.grabs : g0;
        if (g1 > g0){
          grabs += g1 - g0;
          held += G.stunFor;
          if (lastGrab !== null){ gap += t - lastGrab; gapN++; }
          lastGrab = t;
        }
        if (had && !G && me.graspCrush){
          crushes++; grabs++; held += G0.stunFor;
          if (lastGrab !== null){ gap += t - lastGrab; gapN++; }
          fill += t - castT; fillN++;
        }
      }
    }
  } finally {
    for (const k of Object.keys(saved)) w.ult[k] = saved[k];
  }
  return { fights, casts: casts / fights, crushes: crushes / fights,
           held: held / fights, heldCast: held / Math.max(1, casts),
           grabsCast: grabs / Math.max(1, casts),
           reach: crushes / Math.max(1, casts),
           fill: fillN ? fill / fillN : 0,
           fillPct: fillN ? (fill / fillN) / U.dur : 0,
           gap: gapN ? gap / gapN : 0,
           lock: winIn ? lockIn / winIn : 0 };
}"""

# THE ARMS. Every one is a guess at the SAME held seconds by a different route,
# which is the whole point: if the law holds they are worth the same and the
# choice is Rick's on the picture alone.
ARMS = [
    ("as shipped",              {}),
    # ---- ROUND 2. Round 1 asked "what does a slower, longer rhythm look
    # like" and every arm came back 20-60% ABOVE the shipped `held` -- because
    # a longer cooldown does NOT cost grabs. The timer sits expired between
    # them and closes the instant the quarry is in reach, so slowing it SPACES
    # the grabs without losing many, and the longer stun then multiplies. The
    # whole overshoot has to come out of `n`.
    ("H  cad 1.8, stun 0.9, n 3",
     {"cadence": 1.8, "grabStun": 0.9, "n": 3}),
    ("I  cad 2.0, stun 1.0, n 3, true 2.2",
     {"cadence": 2.0, "grabStun": 1.0, "n": 3, "trueStun": 2.2}),
    ("J  cad 1.5, stun 0.8, n 4",
     {"cadence": 1.5, "grabStun": 0.8, "n": 4}),
    ("K  cad 2.2, stun 1.2, n 2, true 2.5",
     {"cadence": 2.2, "grabStun": 1.2, "n": 2, "trueStun": 2.5}),
    ("L  cad 2.5, stun 1.4, n 2, true 2.8",
     {"cadence": 2.5, "grabStun": 1.4, "n": 2, "trueStun": 2.8}),
    ("M  cad 2.0, stun 1.1, n 3, true 2.0, dur 10",
     {"cadence": 2.0, "grabStun": 1.1, "n": 3, "dur": 10.0}),
    ("N  cad 1.6, stun 0.8, n 3, true 2.4",
     {"cadence": 1.6, "grabStun": 0.8, "n": 3, "trueStun": 2.4}),
]



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-grasp.html")
    ap.add_argument("--hn", type=int, default=6, help="seeds a pairing for held")
    ap.add_argument("--wn", type=int, default=0,
                    help="seeds a pairing for a WIN RATE, both sides. 0 skips "
                         "it — the held column is the balance and it is 30x "
                         "cheaper. Use 20+ to confirm the law on the arm chosen")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    A = ap.parse_args()
    gp = resolve_game(A.game)
    t0 = time.time()

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        U = page.evaluate("([r]) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(x => x.id === r).ult))", [RID])
        foes = [i for i in ids if i != RID]
        seeds = [7717 + 23 * i for i in range(A.hn)]
        print(f"\nGRASP'S RHYTHM — {len(foes)} foes x {A.hn} seeds "
              f"= {len(foes) * A.hn} fights an arm, {gp.name}")
        print(f"  shipped: cadence {U['cadence']:g}  grabStun {U['grabStun']:g}  "
              f"n {U['n']}  trueStun {U['trueStun']:g}  window {U['dur']:g}\n")
        print("  BALANCE is the `held` column and nothing else. LEGIBILITY is "
              "the four to its right.\n")
        print(f"    {'arm':<38}{'held':>7}{'/cast':>7}{'grabs':>7}"
              f"{'gap':>7}{'fill':>7}{'lock':>7}{'crush':>7}"
              + (f"{'win':>8}" if A.wn else ""))

        base = None
        out = {}
        for lab, over in ARMS:
            r = page.evaluate(RHY_JS, [RID, over, foes, seeds, A.secs])
            if base is None:
                base = r
            row = (f"    {lab:<38}{r['held']:>7.2f}{r['heldCast']:>7.2f}"
                   f"{r['grabsCast']:>7.2f}{r['gap']:>7.2f}"
                   f"{r['fillPct']:>6.0%}{r['lock']:>7.0%}"
                   f"{r['reach']:>7.0%}")
            if A.wn:
                w = page.evaluate(WIN_JS, [RID, over, A.wn, 88117])
                row += f"{w['rate']:>8.1%}"
                r["win"] = w["rate"]
            print(row)
            out[lab] = r

        print(f"\n    held   seconds the quarry is locked, a fight. THE BALANCE."
              f"  Shipped is {base['held']:.2f}")
        print(f"    /cast  the same, per cast   grabs  grabs a cast")
        print(f"    gap    mean seconds BETWEEN grabs — the cooldown as felt")
        print(f"    fill   how much of the {U['dur']:g}s window the ultimate "
              f"occupies before it ends")
        print(f"    lock   share of the open window the quarry is stunned for. "
              f"A CEILING, not a\n           maximum: at 100% it never moves "
              f"and the ultimate is a freeze, which is\n           the "
              f"Crucible's verb and the one thing this relic may not be")
        print(f"    crush  share of casts that reach the fifth grab")
        assert not errors, errors[:4]

    print(f"\n  {time.time() - t0:.0f}s")
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1))
        print(f"  wrote {A.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
