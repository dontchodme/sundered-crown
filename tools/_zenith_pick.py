#!/usr/bin/env python3
"""A ZENITH WINDOW, TO FILM. v98.

    python _zenith_pick.py --game ../02-chain/sc-zenith-fx.html

`_dawn_pick.py`'s shape. What has to be ON SCREEN (and in the ear) is the whole
of v71 §6: the ring igniting out of the head, the sun riding the flail for the
full 8s -- so the window must close BY ITS CLOCK, which is also the only way to
see the ring contract and hear the close -- a foe lit and ticking for a good
share of it (sparks on the foe, the thread home, the blessing), and ideally the
foe walking in and out of the light more than once.

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "morningstar"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let step = 0, win = null, best = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultSun, t0 = me.sunTally ? me.sunTally.ticks : 0;
      m.step(DT); step++;
      const Z = me.ultSun;
      if (Z && !win) win = { t: m.t, ticks: 0, lit: 0, frames: 0, stretches: 0, was: false, clock: 0, end: m.t };
      if (win){
        if (me.sunTally) win.ticks += me.sunTally.ticks - t0;
        if (Z){
          const lit = th.alive && Math.hypot(th.x - me.headX, th.y - me.headY) < me.w.ult.r + R;
          win.frames++; if (lit) win.lit++;
          if (lit && !win.was) win.stretches++;
          win.was = lit;
        }
        win.end = m.t;
        if (!Z){
          win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive) ? 1 : 0;
          win.score = (win.clock ? 4 : 0) + Math.min(win.ticks, 12) * 0.5
                    + Math.min(win.stretches, 4) * 0.8 + (win.frames ? 3 * win.lit / win.frames : 0);
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
    ap.add_argument("--game", default="../02-chain/sc-zenith-fx.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=98101)
    ap.add_argument("--foes", type=int, default=10)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v98/zenith-window.mp4")
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
              f"{'ticks':>7}{'lit%':>7}{'in':>5}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}"
                  f"{r['clock']:>7}{r['ticks']:>7}{r['litPct']:>7.1f}{r['stretches']:>5}"
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
