#!/usr/bin/env python3
"""THE ONE KNOB -- CORONA's burn, per stack per second. v66, stage 5.

    python corona_sweep.py --game ../02-chain/sc-corona.html --only 0,1

`06-docs/v66/STARWARDEN-BUILD-BRIEF.md` stage 5. Everything else about this
relic is Rick's and does not move: the blade is 8.3 (his, from three priced
bodies), the window is 8s, the ring is 120 x 42, there are 16 stars, the burn
is uncapped and it feeds the shield. What the build owns is ONE NUMBER --
`STATUS.burn.dps` -- and the design says in as many words that its own ladder
cannot resolve it:

    0.10  +17.7      0.20  +34.9   <- the band, at n=192
    0.15  +20.3      0.25  +41.1
                     0.30  +51.0

A +15pp step for 0.05 at n=192 is not a curve, it is two samples. Scour's tick
damage had the same shape and turned out to be a cliff.

## THE INSTRUMENT, AND WHY IT IS NOT A BISECTION

v48 and v56, twice each: a bisection converges on the noise in its tail, and a
three-point confirmation is only as good as the ONE seed block it is drawn on.
Two n=702 readings of one arm have come back 4.3 points apart. WHAT SETTLES A
NUMBER ON THIS ROSTER IS A WIDE DIRECT MEASUREMENT AT n >= 1000 A POINT, ON
BOTH SIDES, REPEATED ON A SECOND BLOCK. So:

    pass 0   the curve, coarse and wide, to find the bracket rather than guess
             it -- v53's lesson, where a blade curve BENT DOWNWARD and a
             bisection started from a guessed bracket could not have seen it
    pass 1   the answer, three points around the crossing, n >= 1000 a point,
             BOTH SIDES, on TWO seed blocks
    pass 2   the shape at the answer -- what the relic is made of, which the
             win column cannot tell you

## BOTH SIDES, AND IT IS NOT A DETAIL HERE

`verify` pairs `i < j` over `WEAPONS`, so a newly appended relic is side B in
all of its pairings, while every sweep in `tools/` has historically run it as
side A. The asymmetry is small (-1.9pp to +2.6pp measured on three relics) and
it is a systematic difference between the instrument that TUNES a relic and the
instrument that PASSES it. This one runs both and prints the gap.
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

RID = "starwarden"


# ONE POINT ON THE CURVE. `dps` is mutated live on `AC.STATUS.burn` and put
# back in a `finally`, which is `umbral_sweep`'s shape -- a sweep that leaves
# the roster mutated poisons every later pass in the same page.
WIN_JS = r"""([id, dps, n, seed0, sides]) => {
  const B = AC.STATUS.burn;
  const d0 = B.dps;
  B.dps = dps;
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  const name = AC.WEAPONS.find(x => x.id === id).name;
  let s = seed0 >>> 0;
  const out = { A: { win: 0, games: 0 }, B: { win: 0, games: 0 },
                dur: 0, timeouts: 0, byFoe: {} };
  try {
    for (const foe of ids){
      let fw = 0, fg = 0;
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        /* THE SAME SEED IS PLAYED FROM BOTH SIDES, so the pair is the fight
           and not two fights -- the side gap is then a paired difference and
           not two independent samples of a roster. */
        for (const side of sides){
          const r = side === "A" ? AC.simulate(id, foe, s)
                                 : AC.simulate(foe, id, s);
          const w = r.winner === name ? 1 : 0;
          out[side].win += w; out[side].games++;
          fw += w; fg++;
          out.dur += r.duration;
          if (r.reason !== "slain") out.timeouts++;
        }
      }
      out.byFoe[foe] = fw / fg;
    }
  } finally { B.dps = d0; }
  const g = out.A.games + out.B.games;
  return { rate: (out.A.win + out.B.win) / g, games: g,
           rateA: out.A.games ? out.A.win / out.A.games : null,
           rateB: out.B.games ? out.B.win / out.B.games : null,
           dur: out.dur / g, timeouts: out.timeouts, byFoe: out.byFoe };
}"""


# WHAT THE RELIC IS MADE OF AT THE ANSWER. A relic that reaches the band
# because the ring is doing the work is not the same relic as one that reaches
# it out of the shower, and the win column cannot tell them apart -- the design
# says the shower should be about 60% of the fire and this is what checks it.
TEL_JS = r"""([id, dps, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, B = AC.STATUS.burn;
  const d0 = B.dps; B.dps = dps;
  const A = { fights: 0, casts: 0, ringStacks: 0, showerStacks: 0, stacks: 0,
              ringDmg: 0, burnDmg: 0, ward: 0, touched: 0, chained: 0,
              chainHit: 0, spawned: 0, pops: 0, peak: 0, dwell: 0,
              entries: 0 };
  try {
    for (const foeId of foes) for (const sd of seeds){
      const m = new AC.Match(id, foeId, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      A.fights++;
      let step = 0, last = null;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const C = me.ultCorona;
        if (C){
          if (!last) A.casts++;
          last = C;
        } else if (last){
          A.stacks += last.stacks; A.ringDmg += last.dmg;
          A.touched += last.touched; A.chained += last.chained;
          A.chainHit += last.chainHit; A.spawned += last.spawned;
          A.pops += last.pops; A.dwell += last.ringF / 120;
          A.entries += last.entries;
          /* THE SPLIT IS ARITHMETIC AND NOT AN ASSUMPTION: every stack the
             shower applies comes through `mineBurn`, so the shower's share is
             `touched + chainHit` times that, and the ring's is the rest. */
          const sh = (last.touched + last.chainHit) * me.w.ult.mineBurn;
          A.showerStacks += sh; A.ringStacks += last.stacks - sh;
          last = null;
        }
        const b = th.stacks("burn");
        if (b > A.peak) A.peak = b;
      }
      A.burnDmg += me.burnDealt || 0;
      A.ward += me.burnBanked || 0;
    }
  } finally { B.dps = d0; }
  return A;
}"""


def band(r, n):
    """One standard error on a roster win rate, and it is a LOWER BOUND.

    A roster win rate is 26-plus pairings of correlated fights, not n
    independent flips, so the binomial figure understates the real spread --
    two readings of one arm have come back 4.3 points apart at n=702. Printed
    so that nobody reads a 2pp difference as a result.
    """
    return (r * (1 - r) / max(1, n)) ** 0.5


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona.html")
    ap.add_argument("--only", default="0,1",
                    help="which passes to run: 0 the curve, 1 the answer, "
                         "2 the shape")
    ap.add_argument("--lo", type=float, default=0.06)
    ap.add_argument("--hi", type=float, default=0.34)
    ap.add_argument("--pts", type=int, default=8)
    ap.add_argument("--cn", type=int, default=6,
                    help="fights per foe per side on the curve")
    ap.add_argument("--wn", type=int, default=16,
                    help="fights per foe per side on the wide pass")
    ap.add_argument("--at", default="",
                    help="comma-separated dps values for pass 1 (default: "
                         "three around the curve's crossing)")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    only = [int(x) for x in a.only.split(",") if x != ""]
    out = {}

    with game(game_path=gp) as (page, errors):
        meta = page.evaluate(
            "() => ({ n: AC.WEAPONS.length,"
            " burn: JSON.parse(JSON.stringify(AC.STATUS.burn)),"
            " ult: JSON.parse(JSON.stringify("
            "   AC.WEAPONS.find(w => w.id === 'starwarden').ult)),"
            " dmg: AC.WEAPONS.find(w => w.id === 'starwarden').dmg })")
        B, U = meta["burn"], meta["ult"]
        print(f"\nCORONA -- the burn, per stack per second   {gp.name}")
        print(f"  {meta['n']} relics · blade {meta['dmg']:g} (Rick's) · "
              f"window {U['dur']:g}s every {U['charge']:g}s · "
              f"{U['stars']:g} stars · burn cap {B['maxStacks']:g}, "
              f"dur {B['dur']:g}s, shipped dps {B['dps']:g}")
        print("  the roster is the field WITH its ultimates live; both sides "
              "of every pairing\n")

        # ------------------------------------------------------- pass 0 ----
        if 0 in only:
            print("  PASS 0 -- THE CURVE. Wide and coarse, to FIND the bracket "
                  "rather than guess it")
            print("           (v53: a blade curve can bend downward and a "
                  "bisection started from a\n"
                  "            guessed bracket converges happily inside the "
                  "wrong one)\n")
            print(f"    {'dps':>6}{'win':>8}{'+/-':>7}{'side A':>9}"
                  f"{'side B':>9}{'dur':>8}{'games':>8}")
            curve = []
            t0 = time.time()
            for i in range(a.pts):
                d = a.lo + (a.hi - a.lo) * i / max(1, a.pts - 1)
                r = page.evaluate(WIN_JS, [RID, d, a.cn, 7000 + i * 17,
                                           ["A", "B"]])
                assert not errors, errors[:3]
                curve.append((d, r))
                print(f"    {d:>6.3f}{r['rate']:>8.1%}"
                      f"{band(r['rate'], r['games']):>7.1%}"
                      f"{r['rateA']:>9.1%}{r['rateB']:>9.1%}"
                      f"{r['dur']:>8.1f}{r['games']:>8}")
            print(f"    {time.time() - t0:.0f}s\n")
            out["curve"] = [(d, r) for d, r in curve]
            # the bracket: the last point under 50% and the first over it
            lo = hi = None
            for d, r in curve:
                if r["rate"] <= 0.50:
                    lo = d
                elif hi is None:
                    hi = d
            print(f"    bracket  {lo} .. {hi}"
                  + ("" if lo is not None and hi is not None
                     else "   <- THE CURVE DOES NOT CROSS 50% IN THIS RANGE"))
            out["bracket"] = [lo, hi]

        # ------------------------------------------------------- pass 1 ----
        if 1 in only:
            if a.at:
                pts = [float(x) for x in a.at.split(",")]
            elif out.get("bracket") and None not in out["bracket"]:
                lo, hi = out["bracket"]
                mid = (lo + hi) / 2
                pts = [round(lo, 4), round(mid, 4), round(hi, 4)]
            else:
                raise SystemExit("pass 1 needs --at, or a pass 0 that crossed")
            print("\n  PASS 1 -- THE ANSWER. Wide, direct, both sides, TWO "
                  "seed blocks")
            print("           (v48 and v56: a bisection converges on the noise "
                  "in its tail, and a\n"
                  "            three-point confirmation is only as good as the "
                  "one block it is on)\n")
            print(f"    {'dps':>6}{'block 1':>10}{'block 2':>10}"
                  f"{'pooled':>9}{'+/-':>7}{'A-B':>8}{'games':>8}")
            wide = {}
            for d in pts:
                rs = []
                for j, s0 in enumerate((21000, 55000)):
                    r = page.evaluate(WIN_JS, [RID, d, a.wn, s0, ["A", "B"]])
                    assert not errors, errors[:3]
                    rs.append(r)
                g = sum(r["games"] for r in rs)
                pooled = sum(r["rate"] * r["games"] for r in rs) / g
                gap = statistics.mean(r["rateA"] - r["rateB"] for r in rs)
                wide[d] = dict(pooled=pooled, games=g,
                               blocks=[r["rate"] for r in rs],
                               rateA=statistics.mean(r["rateA"] for r in rs),
                               rateB=statistics.mean(r["rateB"] for r in rs),
                               byFoe=rs[0]["byFoe"])
                print(f"    {d:>6.3f}{rs[0]['rate']:>10.1%}{rs[1]['rate']:>10.1%}"
                      f"{pooled:>9.1%}{band(pooled, g):>7.1%}{gap:>8.1%}{g:>8}")
            out["wide"] = {str(k): v for k, v in wide.items()}
            # THE ANSWER IS THE POINT NEAREST 50% AND THE HONEST PRECISION IS
            # THE INTERVAL, not the point -- Deadfall's confirmation was not
            # monotonic and the write-up said so rather than picking anyway.
            best = min(wide, key=lambda d: abs(wide[d]["pooled"] - 0.50))
            mono = all(wide[pts[i]]["pooled"] <= wide[pts[i + 1]]["pooled"]
                       for i in range(len(pts) - 1))
            print(f"\n    nearest 50%  dps {best:g} at "
                  f"{wide[best]['pooled']:.1%}")
            print(f"    monotonic    {'yes' if mono else 'NO -- the answer is '
                                     'the flat region, not the point'}")
            out["best"] = best

        # ------------------------------------------------------- pass 2 ----
        if 2 in only:
            d = out.get("best") or (float(a.at.split(",")[0]) if a.at
                                    else B["dps"])
            print(f"\n  PASS 2 -- THE SHAPE AT dps {d:g}. What the relic is "
                  "MADE of, which the win column\n"
                  "           cannot tell you -- the design says the shower is "
                  "~60% of the fire\n")
            ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
            foes = [i for i in ids if i != RID][::3]
            seeds = [4177 + 31 * i for i in range(4)]
            T = page.evaluate(TEL_JS, [RID, d, foes, seeds, 156.0])
            assert not errors, errors[:3]
            c = max(1, T["casts"])
            print(f"    {T['fights']} fights, {T['casts']} casts")
            print(f"      dwell         {T['dwell'] / c:6.2f}s   design 0.82")
            print(f"      crossings     {T['entries'] / c:6.2f}    design 5.6")
            print(f"      stars spawned {T['spawned'] / c:6.2f}    design 16")
            print(f"      touched       {T['touched'] / c:6.2f}    design 10.9")
            print(f"      chained       {T['chained'] / c:6.2f}    design 3.4")
            print(f"      chain hits    {T['chainHit'] / c:6.2f}    design 0.35")
            print(f"      stacks a cast {T['stacks'] / c:6.2f}    design 33.9")
            print(f"        from the ring   {T['ringStacks'] / c:6.2f}"
                  f"    design 12.0")
            print(f"        from the shower {T['showerStacks'] / c:6.2f}"
                  f"    design 21.9")
            print(f"      ring damage   {T['ringDmg'] / c:6.2f}    design 5.8")
            print(f"      burn damage   {T['burnDmg'] / c:6.2f}    design 20.5")
            print(f"      shield        {T['ward'] / c:6.2f}    design 11.2")
            print(f"      peak stacks   {T['peak']:6.0f}      design 49")
            share = T["showerStacks"] / max(1, T["stacks"])
            print(f"\n      the shower is {share:.0%} of the stacks applied "
                  "-- design ~65%")
            out["shape"] = T

        assert not errors, errors[:3]

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
