#!/usr/bin/env python3
"""A DAYBREAK WINDOW, TO FILM. v97.

    python _dawn_pick.py --game ../02-chain/sc-daybreak-fx.html

`_corollary_pick.py`'s shape. What has to be ON SCREEN (and in the ear) is the
whole of v86 §4: the line rising from the floor to the ceiling over the full 8s
-- so the window must close BY ITS CLOCK, which is also the only way to hear all
eight steps of the swell and the held top note -- a foe lit and ticking for a
good share of it, and ideally the foe crossing the line (lit, then not).

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "dawnbringer"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, H = AC.CONFIG.arena.h;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let step = 0, win = null, best = null;
    while (!m.over && step < secs / DT){
      const D0 = me.ultDawn, t0 = me.dawnTally ? me.dawnTally.ticks : 0;
      m.step(DT); step++;
      const D = me.ultDawn;
      if (D && !win) win = { t: m.t, ticks: 0, lit: 0, frames: 0, cross: 0, was: null, clock: 0, end: m.t };
      if (win){
        if (me.dawnTally) win.ticks += me.dawnTally.ticks - t0;
        if (D){
          const lineY = H - Math.min(1, D.t / D.dur) * H, lit = th.alive && th.y > lineY;
          win.frames++; if (lit) win.lit++;
          if (win.was !== null && lit !== win.was) win.cross++;
          win.was = lit;
        }
        win.end = m.t;
        if (!D){
          win.clock = (D0 && D0.t + DT >= D0.dur && me.alive) ? 1 : 0;
          win.score = (win.clock ? 4 : 0) + Math.min(win.ticks, 14) * 0.5
                    + Math.min(win.cross, 4) * 0.8 + (win.frames ? 3 * win.lit / win.frames : 0);
          win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
          win.litPct = win.frames ? 100 * win.lit / win.frames : 0;
          if (!best || win.score > best.score) best = win;
          win = null;
        }
      }
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-daybreak-fx.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=97101)
    ap.add_argument("--foes", type=int, default=10)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v97/daybreak-window.mp4")
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
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>7}"
              f"{'ticks':>7}{'lit%':>7}{'cross':>7}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}"
                  f"{r['clock']:>7}{r['ticks']:>7}{r['litPct']:>7.1f}{r['cross']:>7}"
                  f"{r['score']:>7.1f}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  FILM THE WINDOW AND NOT THE FIGHT:\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['t'] - lead):.2f} "
                  f"--window {b['dur'] + lead + 1.6:.2f} "
                  f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
