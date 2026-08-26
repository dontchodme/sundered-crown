#!/usr/bin/env python3
"""WHAT DOES A LONGER CHAIN DO -- TO THE PICTURE AND TO THE BALANCE?

    python3 chain_len_sweep.py --game ../02-chain/sc-twinshade-scrunch.html

Rick: "can we also try making ALL flails have slightly longer chains? what does
that do to balance?"

**`CONFIG.chain.hilt` IS THE KNOB, AND IT IS THE RIGHT ONE.** The haft is
`reach * hilt` and the chain is `reach * (1 - hilt)`, so lowering `hilt`
lengthens the chain WITHOUT touching reach -- the head still cannot get further
from the ball than `reach`, which is the number every balance property in the
game is built on. Raising `reach` instead would be a different weapon, not a
longer chain.

Three things move when the chain gets longer, and they do not all point the
same way, which is why this is measured rather than reasoned:

  * `f.headR` clamps to `[chainLen*0.30, chainLen]`, so a longer chain lets the
    head swing FURTHER OUT at speed and FURTHER IN when stalled. More travel.
  * gravity's term is `gravity * C.sag / max(1, f.headR)` -- **divided by the
    live chain length**. A longer chain sags LESS per unit time. The build's own
    comment says so: "a chain swung out short whips faster than one hanging at
    full extension."
  * the pivot moves inward, so the same angular lag becomes a SMALLER positional
    error. Lag in angle, lag in space, and they trade against each other.

## The shortcut, and the control that proves it

Only `mode:"chain"` relics read `C.hilt`. So of 171 pairings, the 136 with no
flail in them are bit-identical at every hilt and re-running them six times
would be six times the runtime for the same numbers. This sweeps the 35 flail
pairings per candidate and composes them onto one full-grid baseline.

**That is an assumption, so it is tested.** `--control` re-runs three non-flail
pairings at the most extreme hilt and asserts the results are identical to the
baseline. If they are not, the shortcut is false and every number below is
wrong -- which is exactly the failure `contact_rate_probe` shipped for a
session because nothing checked its own premise.

Writes nothing.
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

# `AC.simulate` steps `CONFIG.physics.dt` internally -- 1/120 -- so this tool
# is correct by construction on the axis v37 caught six instruments getting
# wrong. Nothing here hand-rolls a step loop except GEO_JS, which reads dt.
GRID_JS = """([n, seed0, only]) => {
  const ids = AC.WEAPONS.map(w => w.id);
  const names = {}; for (const w of AC.WEAPONS) names[w.id] = w.name;
  const pairs = [];
  let s = seed0 >>> 0;
  for (let i = 0; i < ids.length; i++){
    for (let j = i + 1; j < ids.length; j++){
      const involves = only === null ||
                       only.indexOf(ids[i]) >= 0 || only.indexOf(ids[j]) >= 0;
      /* The seed stream is advanced for EVERY pair whether or not it is run,
         so pair (i,j) sees the same seeds in the filtered run as in the full
         one. Filtering by skipping the draw would silently reseed the sweep. */
      const seeds = [];
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0; seeds.push(s);
      }
      if (!involves) continue;
      let aw = 0, timeouts = 0;
      const durs = [], clanks = [], hits = [];
      for (const sd of seeds){
        const r = AC.simulate(ids[i], ids[j], sd);
        if (r.winner === names[ids[i]]) aw++;
        if (r.reason !== 'slain') timeouts++;
        durs.push(r.duration); clanks.push(r.clanks); hits.push(r.hits.a + r.hits.b);
      }
      const avg = x => x.reduce((p,v)=>p+v,0)/x.length;
      pairs.push({ a: ids[i], b: ids[j], n, aWins: aw, timeouts,
                   dur: avg(durs), clanks: avg(clanks), hits: avg(hits) });
    }
  }
  return pairs;
}"""

SET_JS = """(h) => { const was = AC.CONFIG.chain.hilt; AC.CONFIG.chain.hilt = h;
                     return was; }"""

# The PICTURE. Balance is half the question Rick asked; the other half is what
# a longer chain looks like, and that is head travel, not winrate.
GEO_JS = """([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const N = Math.round(secs / DT);
  let n = 0, sumD = 0, sumD2 = 0, maxD = 0, minD = 1e9, sumR = 0, sumUtil = 0;
  let sumLag = 0, maxLag = 0;
  const wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(id, f, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const chainLen = me.w.reach * (1 - AC.CONFIG.chain.hilt);
      for (let i = 0; i < N && !m.over; i++){
        m.step(DT);
        const d = Math.hypot(me.headX - me.x, me.headY - me.y);
        sumD += d; sumD2 += d * d; sumR += me.headR;
        sumUtil += me.headR / chainLen;
        maxD = Math.max(maxD, d); minD = Math.min(minD, d);
        const lg = Math.abs(wrap(me.headAng - me.theta));
        sumLag += lg; maxLag = Math.max(maxLag, lg);
        n++;
      }
    }
  }
  const mean = sumD / n;
  return { n, meanD: mean, sdD: Math.sqrt(Math.max(0, sumD2/n - mean*mean)),
           maxD, minD, meanR: sumR / n, meanUtil: sumUtil / n,
           meanLag: sumLag / n, maxLag };
}"""

FLAILS = ["gravemourn", "slagheart"]
GEO_FOES = ["thornwake", "censer", "ironhail", "heartwood"]


def wr_table(pairs, ids):
    tally = {i: [0, 0] for i in ids}
    for p in pairs:
        tally[p["a"]][0] += p["aWins"]; tally[p["a"]][1] += p["n"]
        tally[p["b"]][0] += p["n"] - p["aWins"]; tally[p["b"]][1] += p["n"]
    return {i: (t[0] / t[1] if t[1] else 0) for i, t in tally.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--hilts", default="0.50,0.46,0.42,0.38,0.34,0.30")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")
    hilts = [float(x) for x in A.hilts.split(",")]

    print(f"\nCHAIN LENGTH SWEEP -- CONFIG.chain.hilt")
    print(f"  build {g.name}   n={A.n} per pairing   seed {A.seed}")
    print(f"  chain length = reach * (1 - hilt); reach is UNCHANGED throughout\n")

    with game(game_path=g) as (page, errors):
        base_h = page.evaluate("() => AC.CONFIG.chain.hilt")
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        print(f"  shipped hilt {base_h}  ->  chain {96*(1-base_h):.1f} of reach 96,"
              f" haft {96*base_h:.1f}\n")

        print("  full grid once, at the shipped value ...")
        full = page.evaluate(GRID_JS, [A.n, A.seed, None])
        base_wr = wr_table(full, ids)
        flail_pairs = [p for p in full if p["a"] in FLAILS or p["b"] in FLAILS]
        other = [p for p in full if p not in flail_pairs]
        print(f"  {len(full)} pairings, {len(flail_pairs)} with a flail in them\n")

        # ---- the control on the shortcut -------------------------------
        page.evaluate(SET_JS, min(hilts))
        chk = page.evaluate(GRID_JS, [A.n, A.seed, ["dawnbringer"]])
        page.evaluate(SET_JS, base_h)
        keyed = {(p["a"], p["b"]): p for p in full}
        bad = [f"{p['a']}/{p['b']}" for p in chk
               if p["a"] not in FLAILS and p["b"] not in FLAILS
               and (keyed[(p["a"], p["b"])]["aWins"] != p["aWins"]
                    or abs(keyed[(p["a"], p["b"])]["dur"] - p["dur"]) > 1e-9)]
        n_chk = len([p for p in chk if p["a"] not in FLAILS and p["b"] not in FLAILS])
        print(f"  [{'PASS' if not bad else 'FAIL'}] CONTROL: {n_chk} non-flail pairings "
              f"are identical at hilt {min(hilts)}"
              + (f"   DIFFERED: {bad}" if bad else ""))
        if bad:
            sys.exit("the shortcut is false -- something other than a chain reads hilt")

        rows = []
        for h in hilts:
            page.evaluate(SET_JS, h)
            fp = page.evaluate(GRID_JS, [A.n, A.seed, FLAILS])
            geo = {f: page.evaluate(GEO_JS, [f, GEO_FOES, [11, 23, 37, 51], 20.0])
                   for f in FLAILS}
            wr = wr_table(other + fp, ids)
            rows.append((h, fp, wr, geo))
            print(f"  hilt {h:.2f}  chain {96*(1-h):5.1f}  done")
        page.evaluate(SET_JS, base_h)
        if errors:
            print("PAGE ERRORS:", errors[:4])

    print(f"\n  {'hilt':>5}{'chain':>7}{'GRAVE':>8}{'SLAG':>7}{'spread':>8}"
          f"{'dur':>7}{'clank':>7}{'hits':>7}{'t/o':>6}")
    print("  " + "-" * 62)
    for h, fp, wr, geo in rows:
        dur = statistics.mean(p["dur"] for p in fp)
        clk = statistics.mean(p["clanks"] for p in fp)
        hit = statistics.mean(p["hits"] for p in fp)
        to = sum(p["timeouts"] for p in fp)
        spread = (max(wr.values()) - min(wr.values())) * 100
        mark = "  <-- shipped" if abs(h - 0.46) < 1e-9 else ""
        print(f"  {h:>5.2f}{96*(1-h):>7.1f}{100*wr['gravemourn']:>7.1f}%"
              f"{100*wr['slagheart']:>6.1f}%{spread:>7.1f}pp"
              f"{dur:>7.1f}{clk:>7.1f}{hit:>7.1f}{to:>6}{mark}")

    print(f"\n  THE PICTURE -- head travel, sampled every frame of 20s x 4 foes x 4 seeds")
    print(f"  {'hilt':>5}{'chain':>7}   {'mean d':>8}{'sd':>7}{'min d':>7}{'max d':>7}"
          f"{'headR':>7}{'util':>7}{'lag':>7}")
    print("  " + "-" * 65)
    for h, fp, wr, geo in rows:
        g0 = geo["gravemourn"]
        print(f"  {h:>5.2f}{96*(1-h):>7.1f}   {g0['meanD']:>8.1f}{g0['sdD']:>7.1f}"
              f"{g0['minD']:>7.1f}{g0['maxD']:>7.1f}{g0['meanR']:>7.1f}"
              f"{100*g0['meanUtil']:>6.0f}%{g0['meanLag']:>7.2f}")
    print("\n  'd' is head-to-ball distance -- the reach a viewer actually sees.")
    print("  'util' is headR as a share of the chain: 100% means the chain is")
    print("  always thrown straight and a longer one is simply a longer weapon;")
    print("  well under 100% means the extra length is being spent on SLACK.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
