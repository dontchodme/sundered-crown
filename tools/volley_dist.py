#!/usr/bin/env python3
"""WHAT KIND OF CUT IS FIRING INSIDE THE WINDOW, AND WHY?

The score distributions are identical inside and out, and only 0.3 single hits
a fight clear the bar — yet 47 of 73 cuts land inside a Triplicate window. So
it is not hits. `cineVolleys` groups consecutive hits, and with 2.7x the beat
density a run of three forms far more readily. This measures that directly.
"""
import pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = { cuts: {}, vIn: [], vOut: [] };
  for (const foe of foes) for (const s of seeds){
    const m = new AC.Match(id, foe, s); m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b;
    const win = []; let open = null, g = 0;
    while (!m.over && g++ < 400000){
      m.step(DT);
      const live = !!me.ultSplit || !!m.splitHold;
      if (live && open === null) open = m.t;
      if (!live && open !== null){ win.push([open, m.t]); open = null; }
    }
    if (open !== null) win.push([open, m.t]);
    const isIn = (t) => win.some(w => t >= w[0] && t <= w[1]);
    const p = window.cinePlan(id, foe, s);
    for (const c of p.cuts){
      const k = (c.fatal ? "KILL" : c.kind) + (isIn(c.t) ? " [in]" : " [out]");
      out.cuts[k] = (out.cuts[k] || 0) + 1;
    }
    /* every volley the grouper found, qualifying or not */
    const vs = window.cineVolleysDebug
      ? window.cineVolleysDebug(p.scored)
      : null;
    if (vs) for (const v of vs) (isIn(v.t) ? out.vIn : out.vOut).push(
      { n: v.n, score: +v.score.toFixed(2), q: v.score >= CINE.floor });
  }
  return out;
}"""

FOES = ["emberedge", "axiom", "ironhail", "grudgebearer", "thornwake"]
SEEDS = [113967 + i * 7919 for i in range(10)]
with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    # expose the grouper so this can see every volley, not only the picked ones
    p.evaluate("() => { window.cineVolleysDebug = (sc) => cineVolleys(sc, CINE.volleyGap, CINE.volleyMin); }")
    r = p.evaluate(JS, ["twinshade", FOES, SEEDS])
    if e: print("PAGE ERRORS:", e[:3])

print("  WHAT THE DIRECTOR ACTUALLY CUT TO")
for k in sorted(r["cuts"], key=lambda k: -r["cuts"][k]):
    print(f"    {k:<18} {r['cuts'][k]}")
vi, vo = r["vIn"], r["vOut"]
if vi or vo:
    def sm(name, vs):
        if not vs: print(f"    {name:<10} none"); return
        q = [v for v in vs if v["q"]]
        print(f"    {name:<10} {len(vs):>4} volleys   median {statistics.median(v['n'] for v in vs):.0f} blows   "
              f"qualifying {len(q)} ({100*len(q)/len(vs):.0f}%)   "
              f"median blows of the qualifying: "
              f"{statistics.median([v['n'] for v in q]) if q else float('nan'):.0f}")
    print("\n  VOLLEYS FOUND BY THE GROUPER")
    sm("inside", vi); sm("outside", vo)
    print(f"\n  volley size, inside:  " + ", ".join(
        f"{n}:{sum(1 for v in vi if v['n']==n)}" for n in sorted({v['n'] for v in vi})))
    print(f"  volley size, outside: " + ", ".join(
        f"{n}:{sum(1 for v in vo if v['n']==n)}" for n in sorted({v['n'] for v in vo})))
