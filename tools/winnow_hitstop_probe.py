#!/usr/bin/env python3
"""THE WINNOWING'S FREEZE, COUNTED -- gate 2 of the v67 brief. v67.

    python winnow_hitstop_probe.py --game ../02-chain/sc-trunk.html

`06-docs/v67/WINNOWING-HITSTOP-BRIEF-v67.md` §3 gate 2, and it is a STOP
CONDITION before it is a gate:

    "Publish the BEFORE number from the unpatched tip first -- if it is not
     several hundred ms a cast the diagnosis above is wrong and the build
     stops."

Rick watched Thornshear and said the hit stop *"reads as lag even though its
probably not."* The brief's diagnosis is that every landed kunai buys the
DEFAULT freeze -- `spawnKunai` passes no `over`, so a 1.8-damage leaf holds the
whole picture for ~49ms, sixty-odd times, at irregular moments across five or
six seconds. This measures that claim before anything is built to fix it.

WHAT IS COUNTED, AND HOW

  FROZEN TIME is counted as STEPS THAT TOOK THE FREEZE BRANCH, not as a sum of
  the stops written. `step()` opens with `if (this.hitStop > 0){ hitStop -= dt;
  t += dt; decayImpactOnly(dt); return; }` -- so the wall-time a viewer loses
  is exactly `dt` per step entered with the clock positive. Summing the WRITES
  would over-count every overlap, because `hitStop = max(hitStop, stop)` means
  two hits inside one freeze do not add.

  A FREEZE IS ATTRIBUTED BY THE VALUE THE ENGINE ACTUALLY WROTE. `resolveHit`
  is wrapped and the clock read either side of it; when it rises, the applied
  stop is the new value. Nothing is recomputed from `stopBase` here -- three
  probes in this repo have reported defects that were the probe writing down
  its own model of a rule (`gravemourn_relic_probe`), and this one is measuring
  the rule itself.

  THE WINDOW IS THE CAST UNTIL THE LAST KUNAI IS GONE, which is longer than
  `ult.dur`: the fan keeps flying and bouncing after the window that loosed it
  has closed, and the brief's complaint is about the whole spray.

  A KUNAI HIT IS IDENTIFIED BY `mul`, NOT GUESSED. The shot path passes
  `s.dmgMul` and the blade path passes `undefined`, so a defined `mul` on a
  Thornshear resolve is a kunai. The RUNG is not inferred before the patch --
  it cannot be, because `s.over` does not exist yet. After the patch it is read
  straight off `over.stop`, which is `0.02 * rung` by construction.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "thornshear"


RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const A = { fights: 0, casts: 0, winF: 0, frozenF: 0, winFrozenF: 0,
              kunaiHits: 0, bladeHits: 0, freezes: 0, winFreezes: 0,
              killFreezes: 0, bySize: {}, byRung: {}, killByRung: {}, overSeen: 0,
              perCast: [], shareCast: [], longestWin: 0 };
  for (const foeId of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foeId, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    A.fights++;
    /* THE WINDOW IS OPEN WHILE THE ULT IS UP **OR** A KUNAI OF ITS OWN IS
       STILL IN THE AIR. `ult.dur` is 4s and the spray outlives it. */
    const mine = () => m.shots.some(s => s.kunai && s.own === (me === m.a ? "a" : "b"));
    const open = () => !!me.ultWinnow || mine();

    let inWin = false, winFrozen = 0, winSteps = 0, casts = 0;
    const oRes = m.resolveHit.bind(m);
    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      const before = m.hitStop;
      const r = oRes.apply(m, arguments);
      const after = m.hitStop;
      if (self === me && after > before){
        A.freezes++;
        if (inWin) A.winFreezes++;
        /* THE APPLIED STOP IS WHAT THE CLOCK NOW READS, because the write is
           `max(hitStop, stop)` and it only rose if this hit won it. */
        const k = after.toFixed(3);
        A.bySize[k] = (A.bySize[k] || 0) + 1;
        const kill = after >= AC.CONFIG.impact.killStop - 1e-9;
        if (kill) A.killFreezes++;
        if (mul !== undefined) A.kunaiHits++; else A.bladeHits++;
        if (over && over.stop !== undefined){
          A.overSeen++;
          /* A FATAL KUNAI IS NOT A RUNG-0 FREEZE, AND THE FIRST CUT OF THIS
             COUNTED ONE AS EXACTLY THAT. `resolveHit` guards `!fatal` BEFORE
             it honours an override, so a killing kunai keeps `killStop` 0.55
             while still CARRYING `over.stop = 0.02 * rung` -- which is the
             brief's ruling working, not a leak. Bucketing on the field the
             shot carries rather than on the value the engine wrote reported
             `rung 0 x1` on a build where no rung-0 hit froze anything, and 14
             rung buckets that no size bucket could account for. COUNT THE
             WRITE, NOT THE INTENT. */
          if (kill) A.killByRung[Math.round(over.stop / 0.02)] =
            (A.killByRung[Math.round(over.stop / 0.02)] || 0) + 1;
          else {
            const rung = Math.round(over.stop / 0.02);
            A.byRung[rung] = (A.byRung[rung] || 0) + 1;
          }
        }
      }
      return r;
    };
    /* AND A ZERO OVERRIDE WRITES NOTHING, so a rung-0 kunai after the patch
       never reaches the branch above. Counted separately or it looks like the
       hits stopped happening. */
    let zeroOver = 0;
    const oRes2 = m.resolveHit;
    m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      if (self === me && over && over.stop === 0) zeroOver++;
      return oRes2.apply(m, arguments);
    };

    let step = 0;
    while (!m.over && step < secs / DT){
      const wasOpen = open();
      if (wasOpen && !inWin){ inWin = true; casts++; winFrozen = 0; winSteps = 0; }
      /* A STEP IS FROZEN IF THE CLOCK WAS POSITIVE WHEN IT STARTED -- that is
         exactly the branch `step()` takes. */
      const frozen = m.hitStop > 0;
      m.step(DT); step++;
      if (frozen) A.frozenF++;
      if (inWin){
        winSteps++;
        if (frozen){ winFrozen++; A.winFrozenF++; }
        A.winF++;
      }
      if (inWin && !open()){
        inWin = false;
        A.perCast.push(winFrozen * DT);
        A.shareCast.push(winSteps ? winFrozen / winSteps : 0);
        A.longestWin = Math.max(A.longestWin, winSteps * DT);
      }
    }
    if (inWin){ A.perCast.push(winFrozen * DT);
                A.shareCast.push(winSteps ? winFrozen / winSteps : 0); }
    A.casts += casts;
    A.zeroOver = (A.zeroOver || 0) + zeroOver;
  }
  return A;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-trunk.html")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--seed0", type=int, default=7717)
    ap.add_argument("--foes", type=int, default=8)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    gp = resolve_game(a.game)

    with game(game_path=gp) as (page, errors):
        I = page.evaluate("() => JSON.parse(JSON.stringify(AC.CONFIG.impact))")
        U = page.evaluate("([r]) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(w => w.id === r).ult))", [RID])
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 29 * i for i in range(a.seeds)]
        print(f"\nTHE WINNOWING'S FREEZE -- {gp.name}")
        print(f"  stopBase {I['stopBase']}  stopPerDmg {I['stopPerDmg']}  "
              f"stopMax {I['stopMax']}  critStopMul {I['critStopMul']}  "
              f"killStop {I['killStop']}")
        print(f"  ult dur {U['dur']}  cadence {U['cadence']}  fan {U['fan']}  "
              f"dmgMul {U['dmgMul']}  bounce {U['bounce']}")
        print(f"  {len(foes)} foes x {len(seeds)} seeds\n")
        A = page.evaluate(RUN_JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]

    casts = max(1, A["casts"])
    per = A["perCast"] or [0.0]
    share = A["shareCast"] or [0.0]
    print(f"  {A['fights']} fights, {A['casts']} windows "
          f"(cast -> last kunai gone)\n")
    print(f"  FROZEN SECONDS A CAST       {statistics.mean(per):6.3f}s"
          f"   median {statistics.median(per):.3f}   max {max(per):.3f}")
    print(f"  FROZEN SHARE OF THE WINDOW  {statistics.mean(share):6.1%}")
    print(f"  window length               {A['longestWin']:6.2f}s longest")
    print(f"  frozen share of the WHOLE fight "
          f"{A['frozenF'] / max(1, A['frozenF'] + 1):.1%} of frozen frames "
          f"are... (see counts below)")
    print()
    print(f"  freezes this relic caused   {A['freezes']}  "
          f"({A['winFreezes']} inside a window)")
    print(f"    of them, kunai hits       {A['kunaiHits']}")
    print(f"    of them, blade hits       {A['bladeHits']}")
    print(f"    of them, kills            {A['killFreezes']}")
    print(f"  hits that wrote NOTHING (a zero override)  {A.get('zeroOver', 0)}")
    print()
    print("  by the size the engine actually wrote:")
    for kk in sorted(A["bySize"], key=float):
        print(f"    {float(kk):6.3f}s   x{A['bySize'][kk]}")
    if A["overSeen"]:
        print("\n  by rung (read off `over.stop`, which is 0.02 x rung):")
        for r in sorted(A["byRung"], key=int):
            print(f"    rung {r}   x{A['byRung'][r]}")
    else:
        print("\n  no `over.stop` on any kunai -- this is the UNPATCHED build")

    # THE STOP CONDITION, AND IT IS THE POINT OF THE WHOLE RUN.
    ms = statistics.mean(per) * 1000
    print()
    if not A["overSeen"]:
        if ms < 150:
            print(f"  STOP -- {ms:.0f}ms a cast is not 'several hundred'. The "
                  "brief's diagnosis\n         does not hold on this build and "
                  "the build does not proceed (§3 gate 2).")
            return 1
        print(f"  DIAGNOSIS HOLDS -- {ms:.0f}ms of frozen picture a cast, "
              f"{statistics.mean(share):.0%} of the window.")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(A, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
