#!/usr/bin/env python3
"""A TEMPER WINDOW, TO FILM. v103.

    python _coldiron_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape (by way of `_bindweed_pick.py`). What has to be ON
SCREEN (and in the ear) is the whole of v73 §6: the cast's quench (the blades
flash forge-orange and cool to black iron, thickening; the quench hiss into the
iron ring), binds WON in the iron -- each one the anvil ring and the forge
sparks off the blades, the anvil strike stepping up a semitone with the foe's
sunder count, and the SUNDER tag on the foe ticking up -- the count going PAST
6 (the tag printing in the forge's glow, the ball spalling hot), and the close
BY ITS CLOCK: the blades cooling back to steel and the ring dying. The counts
the anvils strike at are scored at a point a count heard, so a window that
climbs 2-4-6-8-9 beats one that starts at the ceiling. A window that a death
ends (or the match's end) shows none of the close, so it scores nothing. The
fight must also run on for the clip's tail (1.8s past the close), or the kill
takes the picture.

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Coldiron plays side A, as `cinema_clip --a coldiron` films it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "coldiron"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt, CAP0 = AC.STATUS.sunder.maxStacks;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a, th = m.b;
    let step = 0, win = null, best = null, pend = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultTemper, h0 = me.hits, won0 = me.temperTally ? me.temperTally.won : 0;
      m.step(DT); step++;
      /* a clock-closed window waits for its tail: the fight must run on */
      if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; pend.score += 3; if (!best || pend.score > best.score) best = pend; pend = null; }
      const Z = me.ultTemper, T = me.temperTally;
      if (Z && !win) win = { t: m.t, blows: 0, won: 0, ns: {}, pastAt: null, peak: th.stacks("sunder"),
                            start: th.stacks("sunder"), clock: 0, end: m.t, tailOk: 0 };
      if (!win) continue;
      if (T && T.won > won0){
        const n = th.stacks("sunder");
        win.won += T.won - won0; win.ns[n] = (win.ns[n] || 0) + 1;
      }
      if (Z){
        win.blows += me.hits - h0;
        const k = th.stacks("sunder");
        win.peak = Math.max(win.peak, k);
        if (k > CAP0 && win.pastAt === null) win.pastAt = m.t;
        win.end = m.t;
        continue;
      }
      /* THE CLOSE: by the clock with both alive, the only close that cools and rings out */
      win.end = m.t;
      win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive && !m.over) ? 1 : 0;
      const kinds = Object.keys(win.ns).length;
      win.score = win.clock && win.won > 0 && win.pastAt !== null
        ? (4 + Math.min(win.won, 8) * 0.5 + Math.min(kinds, 8) * 1.0 + 2
           + (win.peak >= 9 ? 0.5 : 0) + Math.min(win.blows, 8) * 0.2 + (win.start <= 2 ? 0.5 : 0))
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
    ap.add_argument("--seed0", type=int, default=103201)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--also", default="spellbreaker:99015",
                    help="foe:seed pairs scored besides the grid (the window v103 §5 named)")
    ap.add_argument("--out", default="../07-shorts/v103/temper-window.mp4")
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
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds (+ {a.also})  ·  Coldiron side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'won':>5}"
              f"{'counts heard':>22}{'past 6 at':>10}{'peak':>5}{'blows':>6}{'score':>7}")
        for r in rows[:14]:
            past = f"{r['pastAt']:.2f}" if r["pastAt"] is not None else "-"
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['won']:>5}"
                  f"{r['nList']:>22}{past:>10}{r['peak']:>5}{r['blows']:>6}{r['score']:>7.2f}")
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
