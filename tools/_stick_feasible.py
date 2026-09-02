"""IF A VOLLEY'S ARROWS PERSISTED UNTIL THE LAST OF THE THREE RESOLVED, WHAT
WOULD IT COST THE ENGINE?

Rick: "what if the arrows stuck until all 3 had a chance to collide? that way
their trio is always alive together."

Two facts decide whether that is buildable at all, and neither is a matter of
taste:

  THE CAP. `CONFIG.shot.maxLive` is 64 and `spawnShot` SHIFTS the oldest off
  the front when it is reached -- silently. Today the relic runs about ten live
  shots and 0 evictions over 15,990 arrows. Holding every arrow until its
  slowest sibling resolves raises that, and if it crosses 64 the engine starts
  deleting the very arrows this mechanic exists to keep.

  THE HOLD. How long the last arrow of a volley takes to resolve after the
  first one does IS the duration a stuck arrow has to sit there. If it is a
  tenth of a second nobody sees it; if it is two seconds the wall grows a
  hedge of arrows.

Runtime only. NOTHING is written to any build. This measures the CURRENT build
and infers what the change would cost -- it does not implement it.
"""
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const spans = [];        // seconds from FIRST death to LAST death, per volley
  const firstLife = [];    // how long the first arrow of a volley survived
  let peakReal = 0, peakHeld = 0, evict = 0;
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const own = me === m.a ? "a" : "b";
      /* born[volley] = {t0, alive:Set, deaths:[t...]}  */
      const V = new Map(), seen = new Set();
      let i = 0;
      while (!m.over && i < secs / DT){
        const pre = new Set();
        for (const s of m.shots) if (s.net && s.own === own) pre.add(s);
        m.step(DT); i++;
        const now = new Set();
        let liveNet = 0;
        for (const s of m.shots){
          if (!s.net || s.own !== own) continue;
          now.add(s); liveNet++;
          if (!seen.has(s)){
            seen.add(s);
            let v = V.get(s.volley);
            if (!v) V.set(s.volley, v = { t0: m.t, deaths: [], n: 0 });
            v.n++;
          }
        }
        for (const s of pre) if (!now.has(s)){
          const v = V.get(s.volley); if (v) v.deaths.push(m.t);
        }
        peakReal = Math.max(peakReal, liveNet);
        /* WHAT THE HELD COUNT WOULD HAVE BEEN: every arrow of every volley
           whose LAST arrow has not yet resolved is still on the board. */
        let held = 0;
        for (const v of V.values()) if (v.deaths.length < v.n) held += v.n;
        peakHeld = Math.max(peakHeld, held);
      }
      for (const v of V.values()){
        if (v.deaths.length >= 2){
          v.deaths.sort((a, b) => a - b);
          spans.push(v.deaths[v.deaths.length - 1] - v.deaths[0]);
          firstLife.push(v.deaths[0] - v.t0);
        }
      }
    }
  }
  return { spans, firstLife, peakReal, peakHeld, maxLive: AC.CONFIG.shot.maxLive };
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
ap.add_argument("--sn", type=int, default=3)
a = ap.parse_args()
gp = resolve_game(a.game)
seeds = [4201 + 17 * i for i in range(a.sn)]
with game(game_path=gp) as (page, errors):
    W = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [w for w in W if w != "gloamwire"]
    r = page.evaluate(JS, ["gloamwire", foes, seeds, 120.0])
    assert not errors, errors[:4]

sp = sorted(r["spans"]); fl = sorted(r["firstLife"])
def pct(xs, p): return xs[min(len(xs)-1, int(p*len(xs)))]
print(f"\n  volleys measured {len(sp)}\n")
print("  HOW LONG A STUCK ARROW WOULD HAVE TO SIT")
print("  (first arrow of the volley dies -> last one resolves)\n")
print(f"    {'p50':>7}{'p75':>7}{'p90':>7}{'p99':>7}{'max':>8}")
print(f"    {statistics.median(sp):>7.2f}{pct(sp,.75):>7.2f}{pct(sp,.90):>7.2f}"
      f"{pct(sp,.99):>7.2f}{sp[-1]:>8.2f}   seconds")
print(f"\n  and the first arrow dies {statistics.median(fl):.2f}s after the "
      f"volley is loosed (p90 {pct(fl,.90):.2f}s)")
print(f"\n  THE CAP -- maxLive {r['maxLive']}\n")
print(f"    live net arrows now, peak          {r['peakReal']}")
print(f"    live if the trio were HELD, peak   {r['peakHeld']}"
      f"   {'<- PAST THE CAP' if r['peakHeld'] >= r['maxLive'] else 'still under it'}")
