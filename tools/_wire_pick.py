"""Pick a seed to FILM. Brief stage F: film it before you tune it.

Not a probe and not a gate -- a search for one fight in which a viewer can
actually see the three beats: the ring standing, the catch holding, and the
head arriving. Scores an early cast (so the ring is on screen before the
viewer has stopped watching), a hold long enough to read, and a connect that
lands rather than a window that times out.
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, M = AC.Match.prototype;
  const origHit = M.resolveHit;
  const out = [];
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a;
      let firstCast = -1, catches = 0, connects = 0, held = 0, firstHold = -1;
      m.resolveHit = function (self, foe, hx, hy, seg, mul, over){
        if (self === me && me.ultWire && me.ultWire.caught && foe.pinFree
            && !foe.shade && mul === undefined) connects++;
        return origHit.apply(this, arguments);
      };
      let i = 0, hadWire = false;
      while (!m.over && i < secs / DT){
        m.step(DT); i++;
        if (me.ultWire){
          if (!hadWire){ hadWire = true; if (firstCast < 0) firstCast = m.t; }
          if (me.ultWire.caught){
            held += DT;
            if (firstHold < 0) firstHold = m.t;
          }
          catches = Math.max(catches, me.ultWire.catches);
        } else hadWire = false;
      }
      m.resolveHit = origHit;
      out.push({ foe: foeId, seed: sd, t: +m.t.toFixed(1), win: m.a.hp > m.b.hp,
                 firstCast: +firstCast.toFixed(1), held: +held.toFixed(1),
                 connects, firstHold: +firstHold.toFixed(1) });
    }
  }
  M.resolveHit = origHit;
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-garrote.html")
ap.add_argument("--n", type=int, default=14)
a = ap.parse_args()
gp = resolve_game(a.game)
seeds = [10007 + 977 * i for i in range(a.n)]
with game(game_path=gp) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = ["axiom", "emberedge", "censer", "oathwound", "twinshade",
            "grudgebearer", "ironhail"]
    rows = page.evaluate(JS, ["ravelbone", foes, seeds, 130.0])
# EARLY cast, a hold that reads, and a connect that actually lands.
rows = [r for r in rows if r["connects"] > 0 and 0 < r["firstCast"] <= 26
        and r["held"] >= 2.0 and 25 <= r["t"] <= 70]
rows.sort(key=lambda r: (-r["connects"], r["firstCast"], -r["held"]))
print(f"\n{len(rows)} filmable of {a.n * len(foes)}\n")
print("  foe            seed    len  1st cast  1st hold   held  connects  win")
for r in rows[:14]:
    print(f"  {r['foe']:<13} {r['seed']:>6} {r['t']:>6.1f} {r['firstCast']:>9.1f}"
          f" {r['firstHold']:>9.1f} {r['held']:>6.1f} {r['connects']:>9}"
          f"   {'A' if r['win'] else 'B'}")
