#!/usr/bin/env python3
"""THE BLADE, AND THE THINGS IT IS NOT. Stage 3b of the v57 brief.

    python cindercleave_sweep.py --game ../02-chain/sc-breach.html --only 0,1,2

  [0] THE FLOOR — Cindercleave with its ultimate switched off. What the blade
      and the channel are worth alone, and it is the number the count is
      priced against.
  [1] THE CURVE, wide, printed. Cheap, and the only thing that can show a
      response that BENDS: Gravemourn reads 67.3% at dmg 47.2 and 60.6% at
      52.0, because a bigger blow throws the quarry out of reach of a weapon
      that lands 5.6 times a fight. A bisection started from a guessed bracket
      cannot see the shape it is standing on.
  [2] THE WIDE DIRECT MEASUREMENT, and it is the answer. **NOT A BISECTION.**
  [3] THE TYPE LADDER — which types this relic eats and which eat it. Open
      items 12 and 32 are the same question asked twice, and this is the
      instrument that can see it where `verify`'s per-relic band cannot.
  [4] THE TWO SCALARS at the answer, because Breach is hits-landed AND
      what-a-hit-is-worth and one number will not tune it.

## WHY THERE IS NO BISECTION IN THIS FILE

CLAUDE.md, twice, and the second time it cost a whole damage point:

    A bisection converges on the noise in its own tail, and a three-point
    confirmation is only as good as the ONE seed block it is drawn on. Two
    n=702 readings of the same number differed by 4.3 points.
    WHAT SETTLES A BLADE ON THIS ROSTER IS A WIDE DIRECT MEASUREMENT AT
    n >= 1000 A POINT, ON BOTH SIDES, REPEATED ON A SECOND BLOCK.

Shroudmaul's bisection returned 19.92 and the answer was 21.0. So pass 2 does
exactly what that sentence says and nothing else: five points across the
bracket pass 1 found, at n >= 1000 each, on two independent seed blocks, with
the relic run as side A and as side B.

## AND SIDE MATTERS BECAUSE OF WHERE A NEW RELIC SITS IN THE ARRAY

`verify` pairs `i < j`, so a relic APPENDED to `WEAPONS` is side B in all of
its pairings while every sweep in `tools/` runs it as side A. The asymmetry is
small (shroudmaul -1.9pp, grudgebearer +2.6pp) but it is a systematic
difference between the instrument that tunes a relic and the instrument that
passes it, and it is measured here so the question cannot arise.

Runtime only. NOTHING is written to any build; the answer goes into
`cindercleave_build.TUNED_CC` by hand.
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

RID = "cindercleave"


# THE WIN RATE OVER THE WHOLE FIELD. v41 open decision 2, closed the expensive
# way: a blade bisected on a five-foe subset read 50% and the full field read
# 55.2% on the same number.
#
# `side` IS AN ARGUMENT AND NOT AN ASSUMPTION. `AC.simulate(a, b, seed)` is not
# symmetric -- the two fighters start in different corners -- and every sweep
# in this repo has silently run the relic as side A.
WIN_JS = r"""([id, dmg, n, seed0, side, off]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, c0 = w.ult.charge;
  w.dmg = dmg;
  if (off) w.ult.charge = 1e9;          // [0] the floor: the clock never lands
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  const byFoe = {}, byType = {};
  try {
    for (const foe of ids){
      const ft = AC.WEAPONS.find(x => x.id === foe).shape;
      let fw = 0;
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = side === "b" ? AC.simulate(foe, id, s) : AC.simulate(id, foe, s);
        if (r.winner === w.name){ win++; fw++; }
        games++; dur += r.duration;
        if (r.reason !== "slain") timeouts++;
      }
      byFoe[foe] = fw / n;
      byType[ft] = byType[ft] || [0, 0];
      byType[ft][0] += fw; byType[ft][1] += n;
    }
  } finally { w.dmg = d0; w.ult.charge = c0; }
  const types = {};
  for (const k of Object.keys(byType)) types[k] = byType[k][0] / byType[k][1];
  return { win, games, rate: win / games, dur: dur / games, timeouts,
           byFoe, types };
}"""


# THE SHAPE AT THE ANSWER. A blade that reaches 50% by being a bigger blade is
# not the same relic as one that reaches it by opening more holes, and the win
# column cannot tell them apart.
TEL_JS = r"""([id, dmg, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg; w.dmg = dmg;
  const A = { fights: 0, casts: 0, tears: 0, fired: 0, hits: 0,
              jetDmg: 0, dealt: 0, stackSum: 0, stackN: 0, blows: 0 };
  const origTear = P.tearVent, origJet = P.jetHit;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(id, foeId, sd); A.fights++;
        const me = m.a, th = m.b;
        m.tearVent = function (f, Pp){
          const b = f.ultBreach ? f.ultBreach.tears : -1;
          origTear.call(m, f, Pp);
          const a2 = f.ultBreach ? f.ultBreach.tears : -1;
          if (a2 > b) A.tears++;
        };
        m.jetHit = function (v, own, foe){
          const hp = foe.hp;
          origJet.call(m, v, own, foe);
          A.hits++; A.jetDmg += (hp - foe.hp);
        };
        let step = 0, prevFired = [];
        while (!m.over && step < secs / DT){
          const before = m.vents.map(v => v.fired);
          m.step(DT); step++;
          for (let i = 0; i < m.vents.length && i < before.length; i++)
            if (m.vents[i].fired > before[i]) A.fired++;
          if (m.vents.length){ A.stackSum += th.stacks("sunder"); A.stackN++; }
        }
        A.casts += me.ultsFired; A.dealt += me.dealt; A.blows += me.hits;
      }
    }
  } finally { w.dmg = d0; P.tearVent = origTear; P.jetHit = origJet; }
  return A;
}"""


def run(page, dmg, n, seed0, side="a", off=False):
    return page.evaluate(WIN_JS, [RID, dmg, n, seed0, side, off])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-breach.html")
    ap.add_argument("--only", default="0,1,2,3,4")
    ap.add_argument("--lo", type=float, default=10.0)
    ap.add_argument("--hi", type=float, default=32.0)
    ap.add_argument("--pts", type=int, default=8)
    ap.add_argument("--sn", type=int, default=6, help="pass 1 seeds a pairing")
    ap.add_argument("--wn", type=int, default=40,
                    help="pass 2 seeds a pairing -- 40 x 28 foes = 1120 a point")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    only = {int(x) for x in a.only.split(",") if x.strip()}
    gp = resolve_game(a.game)
    out: dict = {}
    t0 = time.time()
    fights = 0

    print(f"\nCINDERCLEAVE — THE BLADE — {gp.name}")
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        d0 = page.evaluate("(r) => AC.WEAPONS.find(w=>w.id===r).dmg", RID)
        print(f"  {len(ids)} relics, shipped blade {d0:g}\n")

        if 0 in only:
            print("[0] THE FLOOR — the ultimate switched off at charge 1e9")
            r = run(page, d0, a.sn * 2, 700001, "a", True)
            fights += r["games"]
            print(f"      blade {d0:g}, NO ULTIMATE   {r['rate']*100:>5.1f}%  "
                  f"n={r['games']}  mean {r['dur']:.1f}s")
            r2 = run(page, d0, a.sn * 2, 700001, "a", False)
            fights += r2["games"]
            print(f"      blade {d0:g}, with BREACH   {r2['rate']*100:>5.1f}%  "
                  f"n={r2['games']}  mean {r2['dur']:.1f}s")
            print(f"      the ultimate is worth "
                  f"{(r2['rate']-r['rate'])*100:+.1f}pp on the same blade\n")
            out["floor"] = {"off": r["rate"], "on": r2["rate"], "n": r["games"]}

        curve = []
        if 1 in only:
            print(f"[1] THE CURVE — {a.pts} points, n={a.sn*(len(ids)-1)} each")
            for i in range(a.pts):
                d = a.lo + (a.hi - a.lo) * i / (a.pts - 1)
                r = run(page, d, a.sn, 810000 + i * 17)
                fights += r["games"]
                curve.append((d, r["rate"]))
                print(f"      {d:>7.2f}  {r['rate']*100:>5.1f}%  "
                      f"n={r['games']:<5} mean {r['dur']:.1f}s  "
                      f"timeouts {r['timeouts']}")
            # THE SHAPE, NAMED. A curve that bends is a finding and not a detail.
            mono = all(curve[i][1] <= curve[i + 1][1] + 1e-9
                       for i in range(len(curve) - 1))
            print("      monotonic: " + ("yes" if mono else
                  "NO — the response BENDS, which is a finding: a bisection "
                  "started\n                 from a guessed bracket cannot see "
                  "the shape it is standing on"))
            cross = [i for i in range(len(curve) - 1)
                     if (curve[i][1] - 0.5) * (curve[i + 1][1] - 0.5) <= 0]
            if cross:
                lo, hi = curve[cross[-1]][0], curve[cross[-1] + 1][0]
                print(f"      50% is bracketed by {lo:.2f} and {hi:.2f}"
                      + ("   (and it crosses %d times)" % len(cross)
                         if len(cross) > 1 else ""))
            out["curve"] = curve

        if 2 in only:
            # THE BRACKET comes from pass 1 when it ran, and from --lo/--hi
            # when it did not, so this pass can be re-run alone.
            if curve and cross:
                lo, hi = curve[cross[-1]][0], curve[cross[-1] + 1][0]
            else:
                lo, hi = a.lo, a.hi
            pts = [lo + (hi - lo) * i / 4 for i in range(5)]
            print(f"\n[2] THE WIDE DIRECT MEASUREMENT — n={a.wn*(len(ids)-1)} "
                  f"a point, TWO seed blocks, BOTH sides")
            print(f"      {'blade':>7}  {'A blk1':>7}{'A blk2':>8}"
                  f"{'B blk1':>8}{'pooled':>9}")
            rows = []
            for d in pts:
                cells = []
                for seed0, side in ((910001, "a"), (313377, "a"),
                                    (910001, "b")):
                    r = run(page, d, a.wn, seed0, side)
                    fights += r["games"]
                    cells.append(r["rate"])
                pooled = statistics.mean(cells)
                rows.append((d, cells, pooled))
                print(f"      {d:>7.2f}  {cells[0]*100:>6.1f}%"
                      f"{cells[1]*100:>7.1f}%{cells[2]*100:>7.1f}%"
                      f"{pooled*100:>8.1f}%")
            out["wide"] = [(d, c, p) for d, c, p in rows]
            # THE CROSSING, read off the pooled column by linear interpolation
            # between the two points that straddle it.
            ans = None
            for i in range(len(rows) - 1):
                x0, _, y0 = rows[i]
                x1, _, y1 = rows[i + 1]
                if (y0 - 0.5) * (y1 - 0.5) <= 0 and y1 != y0:
                    ans = x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0)
            mono = all(rows[i][2] <= rows[i + 1][2] + 1e-9
                       for i in range(len(rows) - 1))
            print(f"\n      pooled ordering is "
                  f"{'MONOTONIC' if mono else 'NOT monotonic — the answer is '
                     'the middle of a flat region and the honest precision is '
                     'the interval, not the number'}")
            if ans is None:
                print("      50% IS NOT INSIDE THIS BRACKET. Widen it.")
            else:
                print(f"      ANSWER  {ans:.2f}   "
                      f"(side asymmetry at the answer: "
                      f"{(rows[0][1][2]-rows[0][1][0])*100:+.1f}pp at "
                      f"{rows[0][0]:.2f})")
                out["answer"] = ans

        if 3 in only:
            print(f"\n[3] THE TYPE LADDER at the shipped blade "
                  f"— open items 12 and 32")
            r = run(page, d0, a.sn * 3, 660013)
            fights += r["games"]
            ts = sorted(r["types"].items(), key=lambda kv: -kv[1])
            for k, v in ts:
                print(f"      {k:<12}{v*100:>6.1f}%")
            spread = (ts[0][1] - ts[-1][1]) * 100
            print(f"      overall {r['rate']*100:.1f}%   TYPE SPREAD "
                  f"{spread:.1f}pp   (Thornshear 43.6, Shroudmaul 40.1)")
            print(f"      `verify`'s per-relic band cannot see this. It is the "
                  f"third instance\n      of the same open item and it is "
                  f"Rick's.")
            out["types"] = r["types"]
            out["typeSpread"] = spread

        if 4 in only:
            print(f"\n[4] THE TWO SCALARS at the shipped blade")
            foes = [i for i in ids if i != RID]
            seeds = [4242 + 37 * i for i in range(4)]
            T = page.evaluate(TEL_JS, [RID, d0, foes, seeds, a.secs])
            n_f = max(1, T["fights"])
            print(f"      casts a fight     {T['casts']/n_f:>7.2f}")
            print(f"      holes a cast      {T['tears']/max(1,T['casts']):>7.2f}")
            print(f"      jets fired        {T['fired']/n_f:>7.2f}")
            print(f"      HITS LANDED       {T['hits']/n_f:>7.2f}   <- one")
            print(f"      MEAN SUNDER       "
                  f"{T['stackSum']/max(1,T['stackN']):>7.2f}   <- two")
            print(f"      jet damage        {T['jetDmg']/n_f:>7.1f} a fight, "
                  f"{T['jetDmg']/max(1,T['dealt'])*100:.0f}% of everything "
                  f"delivered")
            print(f"      blade blows       {T['blows']/n_f:>7.2f} a fight")
            out["telemetry"] = T

        assert not errors, errors

    print(f"\n{fights} fights, {time.time()-t0:.0f}s")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
