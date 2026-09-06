#!/usr/bin/env python3
"""A FIGHT WITH CORONA IN IT, TO FILM. v66.

    python _corona_pick.py --game ../02-chain/sc-corona-fx.html

`_wire_pick.py` and `_storm_pick.py`'s shape. CLAUDE.md 4.0: film before you
tune if the ultimate is a picture -- and what has to be ON SCREEN here is not
"a cast" but the whole sentence: the ring standing, an enemy crossing it, the
STAR POPPING on a body contact, sixteen stars in the room, and the chain going
off top to bottom when the window shuts.

So a candidate is scored on all five, and the tool prints the `--at` and
`--window` to hand `cinema_clip` rather than a seed and a shrug.

RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT, which is why this
returns a moment and a length.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let step = 0, cast = null, best = null;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      const C = me.ultCorona;
      if (C && !cast) cast = { t: m.t, pops: 0, touched: 0, chained: 0,
                               entries: 0, live: 0, end: 0, hp: th.hp,
                               peak: 0 };
      if (C && cast){
        cast.pops = C.pops; cast.touched = C.touched; cast.chained = C.chained;
        cast.entries = C.entries; cast.end = m.t;
        cast.live = Math.max(cast.live, C.stars.length);
        cast.peak = Math.max(cast.peak, th.stacks("burn"));
      }
      if (!C && cast){
        /* SCORED ON THE WHOLE SENTENCE. A cast with no pop is a ring nobody
           walked into, which is a real ninth of all casts and is exactly the
           thing not to film first. */
        cast.score = (cast.pops ? 3 : 0) + Math.min(cast.entries, 6)
                   + Math.min(cast.touched, 12) * 0.5
                   + Math.min(cast.chained, 6) * 0.7
                   + (cast.peak > 30 ? 2 : 0);
        cast.foe = foe; cast.seed = sd; cast.dur = cast.end - cast.t;
        if (!best || cast.score > best.score) best = cast;
        cast = null;
      }
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=33101)
    ap.add_argument("--foes", type=int, default=8)
    ap.add_argument("--secs", type=float, default=156.0)
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}"
              f"{'cross':>7}{'pop':>5}{'touch':>7}{'chain':>7}{'live':>6}"
              f"{'peak':>6}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}"
                  f"{r['dur']:>8.2f}{r['entries']:>7}{r['pops']:>5}"
                  f"{r['touched']:>7}{r['chained']:>7}{r['live']:>6}"
                  f"{r['peak']:>6}{r['score']:>7.1f}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  FILM THE WINDOW AND NOT THE FIGHT:\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['t'] - lead):.2f} "
                  f"--window {b['dur'] + lead + 1.6:.2f} "
                  f"--fps 60 --w 540 --out ../07-shorts/v66/corona-cast.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
