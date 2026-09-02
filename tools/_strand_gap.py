"""WHY IS AN ARROW FLYING WITH NO LIGHTNING ON IT?

Rick, watching the app: "seeing some of the arrows fire without their lightning
chains." Two causes are possible and they want opposite fixes, so this counts
them apart instead of guessing.

  A DEAD SIBLING. The brief's rule: a strand joins ADJACENT live arrows, and a
  dead arrow breaks its links and does not re-form them. A volley that loses
  its middle arrow leaves idx 0 and idx 2 with no strand between them -- two
  arrows flying naked, and CORRECT.

  A NAKED VOLLEY AT BIRTH. All three alive, adjacent, and still no strand.
  That would be a real fault in `drawStrands` or in the fields it reads.

Runtime only. NOTHING is written to any build.
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let frames = 0, netArrows = 0, naked = 0;
  let nakedDeadSib = 0, nakedFullVolley = 0, nakedEdge = 0;
  let volleysSeen = 0, volleysFullAtBirth = 0;
  const born = new Set();
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const own = me === m.a ? "a" : "b";
      let i = 0;
      while (!m.over && i < secs / DT){
        m.step(DT); i++;
        const by = new Map();
        for (const s of m.shots){
          if (!s.net || s.own !== own) continue;
          let g = by.get(s.volley); if (!g) by.set(s.volley, g = []);
          g.push(s);
        }
        if (!by.size) continue;
        frames++;
        for (const g of by.values()){
          g.sort((p, q) => p.idx - q.idx);
          if (!born.has(g[0].volley)){
            born.add(g[0].volley); volleysSeen++;
            if (g.length === 3) volleysFullAtBirth++;
          }
          const idxs = new Set(g.map(s => s.idx));
          for (const s of g){
            netArrows++;
            /* an arrow is CLOTHED if it has a live neighbour at idx-1 or idx+1 */
            const has = idxs.has(s.idx - 1) || idxs.has(s.idx + 1);
            if (has) continue;
            naked++;
            if (g.length === 1) nakedDeadSib++;
            else if (g.length === 3) nakedFullVolley++;
            else nakedEdge++;
          }
        }
      }
    }
  }
  return { frames, netArrows, naked, nakedDeadSib, nakedFullVolley, nakedEdge,
           volleysSeen, volleysFullAtBirth };
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
n = max(1, r["netArrows"])
print(f"\n  arrow-frames with a volley alive   {r['netArrows']}")
print(f"  NAKED (no live adjacent neighbour) {r['naked']}   {r['naked']/n:.1%}\n")
print(f"    last one left of its volley      {r['nakedDeadSib']:>8}"
      f"   {r['nakedDeadSib']/n:6.1%}   correct — the sibling died")
print(f"    2 of 3 left, non-adjacent        {r['nakedEdge']:>8}"
      f"   {r['nakedEdge']/n:6.1%}   correct — the MIDDLE died")
print(f"    all 3 alive and still no strand  {r['nakedFullVolley']:>8}"
      f"   {r['nakedFullVolley']/n:6.1%}   <- A FAULT IF NONZERO")
print(f"\n  volleys seen {r['volleysSeen']}, of which full at first sight "
      f"{r['volleysFullAtBirth']} ({r['volleysFullAtBirth']/max(1,r['volleysSeen']):.1%})")
