#!/usr/bin/env python3
"""A WINDOW WHERE THE POP LANDS ON THE CAST'S HEELS. v66.

    python _corona_tight.py --game ../02-chain/sc-corona-fx.html

The pop is a median 1.31s after the cast (`corona_star_probe [4]`), and the
cast voice SWEEP runs 1.15s. So in the typical window THE TWO OVERLAP, and
whether they fuse into one long noise is the only question about the pop voice
that a spread cannot answer -- `sentinel_hum_audition` exists because a spread
was the wrong instrument for exactly this shape of question.

THE WINDOW THE POP CANDIDATES WERE FIRST AUDITIONED IN HAS A 3.35s GAP, which
is nearly three times the median and hears the two voices as separate events by
construction. That is not a rigged test, it is an unlucky one -- and it is the
kind of thing that ships a cue nobody can pick out.

So this finds the opposite: a cast whose pop lands INSIDE the cast voice's own
tail, and prints the `cinema_clip` line for it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"

JS = r"""([rid, foes, seeds, secs, want]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    let step = 0, cast = null;
    while (!m.over && step < secs / DT){
      const had = !!me.ultCorona;
      const wasPop = had && me.ultCorona.popped;
      m.step(DT); step++;
      const C = me.ultCorona;
      if (C && !had) cast = { t: m.t, gap: -1, touched: 0, chained: 0 };
      if (C && cast && C.popped && !wasPop) cast.gap = m.t - cast.t;
      if (C && cast){ cast.touched = C.touched; cast.chained = C.chained; }
      if (!C && cast){
        if (cast.gap > 0)
          out.push({ foe, seed: sd, t: cast.t, gap: cast.gap,
                     touched: cast.touched, chained: cast.chained,
                     miss: Math.abs(cast.gap - want) });
        cast = null;
      }
    }
  }
  /* NEAREST THE TARGET GAP, and among those the one with the fullest shower --
     a tight window with two stars touched would answer the timing question and
     show nothing else. */
  out.sort((p, q) => (p.miss - q.miss) || (q.touched - p.touched));
  return out.slice(0, 10);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--want", type=float, default=1.31,
                    help="the gap to hunt for -- the measured median")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--seed0", type=int, default=51001)
    ap.add_argument("--foes", type=int, default=8)
    ap.add_argument("--secs", type=float, default=156.0)
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 41 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs, a.want])
        assert not errors, errors[:3]
        print(f"\n  hunting a cast-to-pop gap of {a.want:g}s  "
              f"({len(foes)} foes x {len(seeds)} seeds)\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'gap':>7}"
              f"{'touch':>7}{'chain':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}"
                  f"{r['gap']:>7.2f}{r['touched']:>7}{r['chained']:>7}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  TIGHTEST: pop {b['gap']:.2f}s after the cast -- "
                  f"SWEEP is still ringing\n")
            print(f"    python cinema_clip.py --game {a.game} \\")
            print(f"      --a {RID} --b {b['foe']} --seed {b['seed']} "
                  f"--at {max(0, b['t'] - lead):.2f} --window 13.30 \\")
            print(f"      --fps 60 --w 540 --out "
                  f"../07-shorts/v66/corona-tight.mp4")
            print(f"\n    then: python corona_voice_audition.py --event pop "
                  f"--b {b['foe']} \\")
            print(f"      --seed {b['seed']} --at {max(0, b['t'] - lead):.2f} "
                  f"--video ../07-shorts/v66/corona-tight.mp4 \\")
            print(f"      --out ../05-reference/v66/corona-pop-tight")
    return 0


if __name__ == "__main__":
    sys.exit(main())
