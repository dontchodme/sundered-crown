#!/usr/bin/env python3
"""Pick a fight that SHOWS this ultimate.

Not a general picker — the criteria are specific to what has to be on screen:
two casts (so the split, the burn, the drain and the reunion all land twice),
the first one early enough to be inside a short, and real contact during the
window or the drain has nothing to draw.

Foes are chosen for COLOUR first. The relic is a purple ball with hot pink-red
flames and a green drain, so an umbral foe is the v28 smudge at its worst and a
bloodsworn one puts red on red. Dwarven amber and runic blue are the two that
separate cleanly.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  const rows = [];
  for (const foe of foes) for (const s of seeds){
    const m = new AC.Match(id, foe, s);
    m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let g = 0, casts = [], holds = 0, shadeHits = 0, drainFrames = 0;
    let prevSplit = false;
    const oh = AC.Match.prototype.resolveHit;
    while (!m.over && g++ < DT_FPS * 120){
      m.step(DT);
      if (me.ultSplit && !prevSplit) casts.push(+m.t.toFixed(1));
      prevSplit = !!me.ultSplit;
      if (m.drains.length) drainFrames++;
    }
    rows.push({ foe, seed: s, dur: +m.t.toFixed(1), casts: casts.length,
                first: casts[0] === undefined ? null : casts[0],
                last: casts[casts.length-1] === undefined ? null : casts[casts.length-1],
                drainFrames, hits: me.hits, clanks: m.clankCount,
                win: !!(m.winner && m.winner.w.id === id),
                winnerHp: m.winner ? Math.round(m.winner.hp) : 0 });
  }
  return rows;
}"""

FOES = ["emberedge", "slagheart", "axiom", "ironhail", "grudgebearer"]
SEEDS = [113967 + i * 7919 for i in range(14)]
with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    rows = p.evaluate(JS, ["twinshade", FOES, SEEDS])
    if e: print("PAGE ERRORS:", e[:3])

def score(r):
    if r["casts"] < 2 or r["first"] is None: return -1
    if not (26 <= r["dur"] <= 52): return -1
    if r["last"] > r["dur"] - 6: return -1        # the last cast must complete
    return (r["drainFrames"] * 0.02 + r["clanks"] * 0.6
            - abs(r["first"] - 17) * 1.2 - abs(r["dur"] - 40) * 0.5)

rows = [r for r in rows if score(r) > 0]
rows.sort(key=score, reverse=True)
print(f"  {'foe':<14} {'seed':>9} {'dur':>6} {'casts':>6} {'1st':>6} "
      f"{'last':>6} {'drainF':>7} {'hits':>5} {'clanks':>7}  winner")
for r in rows[:10]:
    print(f"  {r['foe']:<14} {r['seed']:>9} {r['dur']:>6.1f} {r['casts']:>6} "
          f"{r['first']:>6.1f} {r['last']:>6.1f} {r['drainFrames']:>7} "
          f"{r['hits']:>5} {r['clanks']:>7}  "
          f"{'TWINSHADE' if r['win'] else r['foe']} @{r['winnerHp']}")
print(f"\n  {len(rows)} of {len(FOES)*len(SEEDS)} qualify")
