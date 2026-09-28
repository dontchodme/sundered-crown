#!/usr/bin/env python3
"""A QUARRELSTORM WINDOW, TO FILM. v108.

    python _ironhail_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape (by way of `_coldiron_pick.py`). What has to be ON
SCREEN (and in the ear) is the whole of v83 §4: the cast (the bellows huff; the
bow's limbs igniting forge-orange), bolts dropping -- each one's rune on the
foe's spot with its ring closing, and the streak falling onto it -- LANDINGS
(the iron thud, pitched by the foe's sunder count, so it steps up as the count
climbs; the splash, the dust, six sparks, the iron-spark motes and the SUNDER
tag on the foe ticking up), at least one MISS (the quieter thud and a splash
in dust), and the close BY ITS CLOCK: the limbs cooling, and no voice (the
design gives the close nothing). The counts the landings thud at are scored at
a point a count heard, so a window that climbs 1-2-3-4 beats one that starts
at the ceiling. A window that a death ends (or the match's end) shows none of
the cool, so it scores nothing. The fight must also run on for the clip's tail
(1.8s past the close), or the kill takes the picture.

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Ironhail plays side A, as `cinema_clip --a ironhail` films it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "ironhail"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a, th = m.b;
    let step = 0, win = null, best = null, pend = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultHail, h0 = me.hits, T0 = me.hailTally ? { l: me.hailTally.landed, x: me.hailTally.missed } : { l: 0, x: 0 };
      m.step(DT); step++;
      /* a clock-closed window waits for its tail: the fight must run on */
      if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; pend.score += 3; if (!best || pend.score > best.score) best = pend; pend = null; }
      const Z = me.ultHail, T = me.hailTally;
      if (Z && !win) win = { t: m.t, blows: 0, landed: 0, missed: 0, ns: {}, first: null, start: th.stacks("sunder"),
                            clock: 0, end: m.t, tailOk: 0 };
      if (!win) continue;
      if (T && T.landed > T0.l){
        const n = th.stacks("sunder");
        win.landed += T.landed - T0.l; win.ns[n] = (win.ns[n] || 0) + 1;
        if (win.first === null) win.first = m.t;
      }
      if (T && T.missed > T0.x) win.missed += T.missed - T0.x;
      if (Z){ win.blows += me.hits - h0; win.end = m.t; continue; }
      /* THE CLOSE: by the clock with both alive, the only close that cools in the picture */
      win.end = m.t;
      win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive && !m.over) ? 1 : 0;
      const kinds = Object.keys(win.ns).length;
      win.score = win.clock && win.landed > 0 && win.missed > 0
        ? (4 + Math.min(win.landed, 8) * 0.5 + Math.min(kinds, 6) * 1.0 + 1 + Math.min(win.missed, 4) * 0.2
           + Math.min(win.blows, 8) * 0.2 + (win.start <= 1 ? 0.5 : 0))
        : 0;
      win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
      win.nList = Object.keys(win.ns).map(Number).sort((p, q) => p - q).join(" ");
      if (win.score > 0) pend = win;
      win = null;
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=108201)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--also", default="spellbreaker:99015,dawnbringer:99001",
                    help="foe:seed pairs scored besides the grid (the picture lab's looks)")
    ap.add_argument("--out", default="../07-shorts/v108/quarrelstorm-window.mp4")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs, TAIL])
        for pair in [x for x in a.also.split(",") if x]:
            f, sd = pair.split(":")
            rows += page.evaluate(JS, [RID, [f], [int(sd)], a.secs, TAIL])
        rows.sort(key=lambda r: -r["score"])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds (+ {a.also})  ·  Ironhail side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'landed':>7}{'missed':>7}"
              f"{'counts heard':>16}{'start':>6}{'blows':>6}{'score':>7}")
        for r in rows[:14]:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['landed']:>7}"
                  f"{r['missed']:>7}{r['nList']:>16}{r['start']:>6}{r['blows']:>6}{r['score']:>7.2f}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  FILM THE WINDOW AND NOT THE FIGHT:\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['t'] - lead):.2f} "
                  f"--window {b['dur'] + lead + TAIL:.2f} --end-at-window "
                  f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
