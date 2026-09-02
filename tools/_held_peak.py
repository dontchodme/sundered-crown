"""HOW MANY ARROWS ARE ACTUALLY ON THE BOARD NOW THAT VOLLEYS ARE HELD, AND FOR
HOW LONG IS ONE HELD?

The pre-build estimate said peak 23 against a cap of 64 and the built relic
evicts. That estimate was an INFERENCE from a build whose volleys shed arrows;
holding them changes the fights, so it under-predicted. This measures the thing
that was built.

Runtime only. NOTHING is written to any build.
"""
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const holds = [];
  let peak = 0, peakStuck = 0, atCap = 0, frames = 0;
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const own = me === m.a ? "a" : "b";
      const stuckAt = new Map();
      let i = 0;
      while (!m.over && i < secs / DT){
        m.step(DT); i++;
        let live = 0, st = 0;
        for (const s of m.shots){
          if (s.net && s.own === own){
            live++;
            if (s.stuck){
              st++;
              if (!stuckAt.has(s)) stuckAt.set(s, m.t);
            }
          }
        }
        peak = Math.max(peak, live); peakStuck = Math.max(peakStuck, st);
        if (m.shots.length >= AC.CONFIG.shot.maxLive) atCap++;
        frames++;
        for (const [s, t0] of stuckAt) if (m.shots.indexOf(s) < 0){
          holds.push(m.t - t0); stuckAt.delete(s);
        }
      }
    }
  }
  return { holds, peak, peakStuck, atCap, frames, cap: AC.CONFIG.shot.maxLive };
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
ap.add_argument("--sn", type=int, default=4)
a = ap.parse_args()
gp = resolve_game(a.game)
seeds = [4201 + 17 * i for i in range(a.sn)]
with game(game_path=gp) as (page, errors):
    W = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [w for w in W if w != "gloamwire"]
    r = page.evaluate(JS, ["gloamwire", foes, seeds, 120.0])
    assert not errors, errors[:4]
h = sorted(r["holds"])
def pct(p): return h[min(len(h)-1, int(p*len(h)))] if h else 0
print(f"\n  PEAK LIVE net arrows      {r['peak']}   against a cap of {r['cap']}")
print(f"  peak STUCK at once        {r['peakStuck']}")
print(f"  frames at the cap         {r['atCap']} of {r['frames']}"
      f"   {r['atCap']/max(1,r['frames']):.3%}")
print(f"\n  HOW LONG AN ARROW IS HELD ({len(h)} arrows)\n")
print(f"    {'p50':>7}{'p90':>7}{'p99':>7}{'max':>8}")
print(f"    {statistics.median(h):>7.2f}{pct(.90):>7.2f}{pct(.99):>7.2f}{h[-1]:>8.2f}   s")
