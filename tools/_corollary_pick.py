#!/usr/bin/env python3
"""A COROLLARY WINDOW, TO FILM. v88.

    python _corollary_pick.py --game ../02-chain/sc-corollary.html

`_corona_pick.py`'s shape. CLAUDE.md 4.0: film before you tune if the
ultimate is a picture -- and what has to be ON SCREEN is not "a cast" but the
whole sentence of v80 §4: blows landing in the window, their corollaries
striking half a second later and hexing, at least one that finds the foe OUT
of reach (the picture has to say "missed", not "broke"), and one that lands
AFTER the window has closed ("it was earned").

So a window is scored on all of it, and the tool prints the `--at` and
`--window` to hand `cinema_clip` rather than a seed and a shrug. A window is
the span `me.ultEcho` exists: the cast until the last queued echo resolves.

RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT, which is why this
returns a moment and a length.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "axiom"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    let step = 0, win = null, best = null;
    while (!m.over && step < secs / DT){
      const E0 = me.ultEcho, T0 = me.echoTally ? Object.assign({}, me.echoTally) : null;
      m.step(DT); step++;
      const E = me.ultEcho, T = me.echoTally;
      if (E && !win) win = { t: m.t, blows: 0, echoes: 0, landed: 0, miss: 0,
                              late: 0, hex: 0, kill: 0, end: m.t };
      if (win && T && T0){
        const dl = T.landed - T0.landed, de = T.echoes - T0.echoes;
        win.blows += T.blows - T0.blows; win.echoes += de; win.landed += dl;
        win.hex += T.hex - T0.hex;
        /* an echo that resolved without landing, with both alive, missed */
        if (de > dl && me.alive && (me === m.a ? m.b : m.a).alive) win.miss += de - dl;
        if (dl > 0 && E0 && E0.t >= E0.dur) win.late += dl;
        if (m.over && m.winner === me && dl > 0) win.kill = 1;
        win.end = m.t;
      }
      if (win && (!E || m.over)){
        win.score = Math.min(win.landed, 5) * 2 + (win.miss ? 1.5 : 0)
                  + (win.late ? 1.5 : 0) + (win.kill ? 3 : 0);
        win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
        if (!best || win.score > best.score) best = win;
        win = null;
      }
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corollary.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=88101)
    ap.add_argument("--foes", type=int, default=10)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v88/corollary-window.mp4")
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
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'blows':>7}"
              f"{'echo':>6}{'land':>6}{'miss':>6}{'late':>6}{'hex':>5}{'kill':>6}"
              f"{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}"
                  f"{r['blows']:>7}{r['echoes']:>6}{r['landed']:>6}{r['miss']:>6}"
                  f"{r['late']:>6}{r['hex']:>5}{r['kill']:>6}{r['score']:>7.1f}")
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
