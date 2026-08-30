#!/usr/bin/env python3
"""HOW OFTEN IS THE CRUCIBLE LIT WHILE A TRUE STUN LANDS?

    python forgestun_probe.py --game ../02-chain/sc-paradox-arc.html --n 40

Rick, 2026-08-29: *"currently when its true stunned it black hole effect still
happens. a true stun should turn it off."*

Before changing an ult mechanic, price it. `breakSpin` is this engine's marker
for a TRUE stun -- the three application sites the v39 comment names, plus the
Stasis hold -- so wrapping it counts every true stun in the game exactly, with
no second source of truth and no change to the sim.

The forge's own `f.stun = 0` erases the stun one step later, so `f.stun` cannot
be read for this. The marker can.

Reports, per opponent: Crucible casts, how many ate a true stun while lit,
how far into the 4.0s window the stun landed, and what the cast went on to do.
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

JS = r"""
([foeIds, n, seed0, dt]) => {
  const out = [];
  let s = seed0 >>> 0;
  const orig = AC.Match.prototype.breakSpin;
  for (const foe of foeIds) {
    let casts = 0, stunned = 0, strikes = 0, fizzles = 0, unresolved = 0;
    const ats = [], perCast = [];
    for (let k = 0; k < n; k++) {
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const m = new AC.Match('grudgebearer', foe, s);
      const g = m.a.w.id === 'grudgebearer' ? m.a : m.b;
      let hits = [];
      /* FORWARD EVERYTHING. `breakSpin` grew a third argument -- the true
         stun's duration, which is what holds a lit Crucible -- and a wrapper
         with a fixed arity would silently drop it, leaving the probe measuring
         the build BEFORE the change while claiming to measure the one after.
         It did exactly that once. */
      AC.Match.prototype.breakSpin = function (f, ...rest) {
        if (f === g && g.ultForge) hits.push(g.ultForge.t);
        return orig.call(this, f, ...rest);
      };
      let lit = false, litT = 0, tookOne = false, nHits = 0;
      for (let i = 0; i < 120 * 130 && !m.over; i++) {
        const before = !!g.ultForge;
        m.step(dt);
        const after = !!g.ultForge;
        if (!before && after) { lit = true; tookOne = false; nHits = 0; hits = []; }
        if (before && !after) {
          casts++;
          nHits = hits.length;
          if (nHits) { stunned++; for (const a of hits) ats.push(a); }
          perCast.push(nHits);
          const fx = m.ultFx;
          if (fx && fx.w === 'grudgebearer' && fx.kind === 'forge') {
            if (fx.phase === 'strike') strikes++;
            else if (fx.phase === 'fizzle') fizzles++;
            else unresolved++;
          } else unresolved++;
          hits = [];
        }
      }
      AC.Match.prototype.breakSpin = orig;
    }
    out.push({ foe, casts, stunned, strikes, fizzles, unresolved, ats, perCast });
  }
  AC.Match.prototype.breakSpin = orig;
  return out;
};
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox-arc.html")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--foes", default="")
    A = ap.parse_args()

    gp = (HERE / A.game).resolve()
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = (A.foes.split(",") if A.foes
                else [i for i in ids if i != "grudgebearer"])
        dt = page.evaluate("() => AC.CONFIG.physics.dt")
        rows = page.evaluate(JS, [foes, A.n, A.seed, dt])
        if errors:
            print("\n".join(errors[:5]))
            return 2

    print(f"grudgebearer vs {len(foes)} relics, {A.n} seeds each "
          f"({A.n * len(foes)} fights)\n")
    print(f"  {'foe':<14}{'casts':>6}{'stunned':>9}{'rate':>8}"
          f"{'mean t':>9}{'strike':>8}{'fizzle':>8}")
    tc = ts = 0
    allats = []
    for r in sorted(rows, key=lambda r: -(r["stunned"] / max(1, r["casts"]))):
        tc += r["casts"]; ts += r["stunned"]; allats += r["ats"]
        rate = r["stunned"] / max(1, r["casts"])
        mt = statistics.mean(r["ats"]) if r["ats"] else float("nan")
        if r["stunned"] == 0:
            continue
        print(f"  {r['foe']:<14}{r['casts']:>6}{r['stunned']:>9}{rate:>7.1%}"
              f"{mt:>9.2f}{r['strikes']:>8}{r['fizzles']:>8}")
    zeros = [r["foe"] for r in rows if r["stunned"] == 0]
    print(f"\n  {len(zeros)} relics never true-stun a lit Crucible: "
          + ", ".join(zeros))
    print(f"\n  overall  {ts}/{tc} casts eat a true stun  "
          f"({ts / max(1, tc):.2%})")
    if allats:
        allats.sort()
        print(f"  when     mean {statistics.mean(allats):.2f}s of a 4.00s "
              f"window, median {statistics.median(allats):.2f}s, "
              f"min {allats[0]:.2f}s, max {allats[-1]:.2f}s")
        past = sum(1 for a in allats if a >= 1.05)
        print(f"  {past}/{len(allats)} land after minT 1.05s "
              f"(the strike is already armed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
