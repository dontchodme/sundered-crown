#!/usr/bin/env python3
"""HOW OFTEN DOES THE DIRECTOR FIRE INSIDE AN ULTIMATE'S WINDOW?

Written for Triplicate; generalised in v38 for Bloodmill, which is the case
v37 open decision 3 predicted: "crowdVolleyMin is a CINE-wide setting, not a
per-relic one. It is correct for any future summon and there are none. If one
arrives with a different density the sweep has to be redone."

A spike storm is not a summon -- `o.crowd` reads `this.shades.length > 0` and a
storm has no shades -- so the exception built for Triplicate DOES NOT APPLY to
it, while forty spikes a second is a far denser stream of contacts than two
copies ever were. Whether that matters is a measurement, not a deduction.

The original brief:

Rick: "the director currently seems to go off the majority of the time
triplicate is active... its too much and a little distracting."

Measured as a RATE, not a count, because the windows are only ~10s of a ~45s
fight and a raw count would flatter whichever side of the comparison had more
seconds in it. The number that matters is cuts per second inside the window
against cuts per second outside it: at parity the director is indifferent to
the ultimate, and anything above 1.0 is it preferring the crowded window.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foes, seeds, cmin]) => {
  if (cmin !== null && typeof CINE !== "undefined"){
    if (Array.isArray(cmin)){ if (cmin[0] !== null) CINE.crowdVolleyMin = cmin[0];
                              if (cmin[1] !== null) CINE.crowdScoreMul = cmin[1]; }
    else CINE.crowdVolleyMin = cmin; }
  const DT = AC.CONFIG.physics.dt;
  const rows = [];
  for (const foe of foes) for (const s of seeds){
    /* the windows: every interval in which a split is running, holds included */
    const m = new AC.Match(id, foe, s);
    m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b;
    const win = [];
    let open = null, g = 0;
    while (!m.over && g++ < 400000){
      m.step(DT);
      /* v39: `ultTrace` joins the list. The tool has now been generalised
         twice (Triplicate -> the spike storm -> the Converse) and each time
         the window predicate was the thing that had to change, because an
         ultimate's "window" is whatever state object it happens to hang its
         duration on. There is no shared field to read. */
      const live = !!me.ultSplit || !!m.splitHold || !!me.ultSpin
                || !!me.ultTrace;
      if (live && open === null) open = m.t;
      if (!live && open !== null){ win.push([open, m.t]); open = null; }
    }
    if (open !== null) win.push([open, m.t]);
    const dur = m.t;
    const inWin = win.reduce((a, w) => a + (w[1] - w[0]), 0);
    const p = window.cinePlan(id, foe, s);
    const cuts = p.cuts || [];
    const isIn = (t) => win.some(w => t >= w[0] && t <= w[1]);
    const inside = cuts.filter(c => isIn(c.t));
    rows.push({ foe, seed: s, dur: +dur.toFixed(1),
                winS: +inWin.toFixed(1), windows: win.length,
                cuts: cuts.length, inside: inside.length,
                cutsNK: cuts.filter(c => !c.fatal).length,
                insideNK: inside.filter(c => !c.fatal).length,
                insideKinds: inside.map(c => c.fatal ? "KILL" : c.kind),
                floorUsed: (typeof CINE !== "undefined" ? CINE.floor : null),
                crowdMin: (typeof CINE !== "undefined" ? CINE.crowdVolleyMin : null) });
  }
  return rows;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-redflail.html")
ap.add_argument("--a", default=None, help="the relic under test")
ap.add_argument("--csp", type=float, default=None, help="CINE.crowdScoreMul")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--min", type=int, default=None,
                help="override CINE.crowdVolleyMin at runtime")
A = ap.parse_args()
FOES = ["emberedge", "axiom", "ironhail", "grudgebearer", "thornwake"]
SEEDS = [113967 + i * 7919 for i in range(A.n)]
with game(game_path=(HERE / A.game).resolve()) as (p, e):
    rows = p.evaluate(JS, [A.a or "twinshade", FOES, SEEDS,
                           [A.min, A.csp] if (A.min is not None or A.csp is not None) else None])
    if e: print("PAGE ERRORS:", e[:3])

tot_dur = sum(r["dur"] for r in rows)
tot_win = sum(r["winS"] for r in rows)
tot_cut = sum(r["cuts"] for r in rows)
tot_in  = sum(r["inside"] for r in rows)
out_cut, out_dur = tot_cut - tot_in, tot_dur - tot_win
rin  = tot_in / max(0.01, tot_win)
rout = out_cut / max(0.01, out_dur)
print(f"  crowdVolleyMin = {rows[0]['crowdMin']}   volleyMin = 3\n")
print(f"  {len(rows)} matches, {tot_dur:.0f}s of fight, {tot_win:.0f}s of it "
      f"inside a Triplicate window ({100*tot_win/tot_dur:.0f}%)\n")
print(f"  cuts total                    {tot_cut}")
print(f"  cuts INSIDE the window        {tot_in}   ({100*tot_in/max(1,tot_cut):.0f}% of all cuts)")
print(f"  cuts outside                  {out_cut}\n")
print(f"  cut rate inside   {rin*60:>6.2f} per minute of window")
print(f"  cut rate outside  {rout*60:>6.2f} per minute of fight")
print(f"  PREFERENCE        {rin/max(1e-9,rout):>6.2f}x   "
      f"(1.00 = the director does not care that the ultimate is running)")
# THE KILL IS EXEMPT BY DESIGN, so it is not a number this exception can move —
# and 18 of the in-window cuts are kills, because this ultimate is often what
# finishes the fight. Excluding them is the only honest read of the knob.
tin_nk = sum(r["insideNK"] for r in rows)
tot_nk = sum(r["cutsNK"] for r in rows)
out_nk = tot_nk - tin_nk
rin_nk = tin_nk / max(0.01, tot_win)
rout_nk = out_nk / max(0.01, out_dur)
print(f"\n  EXCLUDING THE KILL (exempt by design; {tot_cut-tot_nk} of the cuts are kills,"
      f" {tot_in-tin_nk} of them inside)")
print(f"    inside {tin_nk:>3}  outside {out_nk:>3}   "
      f"{rin_nk*60:>5.2f}/min vs {rout_nk*60:>5.2f}/min   "
      f"PREFERENCE {rin_nk/max(1e-9,rout_nk):>5.2f}x")
share = [r for r in rows if r["winS"] > 1]
if share:
    print(f"\n  per match, inside the window: "
          f"median {statistics.median(r['inside'] for r in share):.1f} cuts in "
          f"{statistics.median(r['winS'] for r in share):.1f}s")
