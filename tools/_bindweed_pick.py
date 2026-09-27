#!/usr/bin/env python3
"""A TENDRIL WINDOW, TO FILM. v101.

    python _bindweed_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape. What has to be ON SCREEN (and in the ear) is the
whole of v68 §8: the cast's greening and its rustle, the vine hunting (growing
toward the foe, drawing back in), bites landing with their snaps and the
ENTANGLE count climbing, the leaf motes -- and the close BY ITS CLOCK, the only
close that roots and withers: the wither's rustle, the vine browning and
letting go, and the root's shoots clenching the held ball with the root's
creak-and-crack. The entangle count the bites climb through is scored at a
point a count heard (the bite's pitch steps a semitone a stack, and the tag
prints each step), so a window that climbs 1-2-3-4 beats one that starts at the
cap. A window that the caster's or the foe's death ends shows none
of the close, so it scores nothing. The fight must also run on for the clip's
tail (1.8s past the close), or the kill takes the picture.

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Bindweed plays side A, as `cinema_clip --a bindweed` films it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "bindweed"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a, th = m.b;
    let step = 0, win = null, best = null, pend = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultVine, h0 = me.hits, T0 = me.vineTally ? Object.assign({}, me.vineTally) : null;
      const rm0 = me.reachMul, zt0 = Z0 ? Z0.t : -1;
      m.step(DT); step++;
      /* a clock-closed window waits for its tail: the fight must run on */
      if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; pend.score += 3; if (!best || pend.score > best.score) best = pend; pend = null; }
      const Z = me.ultVine, T = me.vineTally;
      if (Z && !win) win = { t: m.t, blows: 0, bites: 0, ns: {}, touch: 0, frames: 0, stretches: 0, was: false,
                            peak: 1, back: 0, clock: 0, rooted: 0, hold: 0, end: m.t, tailOk: 0 };
      if (!win) continue;
      if (Z){
        if (!(Z === Z0 && Z.t === zt0)) win.frames++;
        win.blows += me.hits - h0;
        const b = T.bites - (T0 ? T0.bites : 0);
        if (b > 0){ win.bites += b; const n = th.stacks("entangle"); win.ns[n] = (win.ns[n] || 0) + 1; }
        /* a frozen step (a hit stop) does not tick the vine: it neither
           touches nor lets go */
        if (!(Z === Z0 && Z.t === zt0)){
          const touching = T.touchFrames > (T0 ? T0.touchFrames : 0);
          if (touching){ win.touch++; if (!win.was) win.stretches++; }
          win.was = touching;
        }
        win.peak = Math.max(win.peak, me.reachMul);
        if (me.reachMul < rm0) win.back += rm0 - me.reachMul;
        win.end = m.t;
        continue;
      }
      /* THE CLOSE */
      win.end = m.t;
      win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive) ? 1 : 0;
      win.rooted = T && T0 && T.roots > T0.roots ? 1 : 0;
      win.hold = win.rooted ? T.rootSec - T0.rootSec : 0;
      const kinds = Object.keys(win.ns).length;
      win.score = win.clock ? (4 + (win.rooted ? 3 : 0) + Math.min(win.hold, 1.2)
                               + Math.min(win.bites, 12) * 0.35 + Math.min(kinds, 4) * 1.0
                               + Math.min(win.stretches, 4) * 0.4 + Math.min(win.blows, 8) * 0.25
                               + (win.peak >= 1.6 ? 1 : 0) + (win.back >= 0.3 ? 0.5 : 0)) : 0;
      win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
      win.touchPct = win.frames ? 100 * win.touch / win.frames : 0;
      win.nList = Object.keys(win.ns).sort().join("");
      if (win.clock) pend = win;
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
    ap.add_argument("--seed0", type=int, default=101201)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v101/tendril-window.mp4")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs, TAIL])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds  ·  Bindweed side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'root':>5}{'hold':>6}"
              f"{'bites':>6}{'n':>6}{'in':>4}{'touch%':>7}{'peak':>6}{'blows':>6}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['rooted']:>5}"
                  f"{r['hold']:>6.2f}{r['bites']:>6}{r['nList']:>6}{r['stretches']:>4}{r['touchPct']:>7.1f}"
                  f"{r['peak']:>6.2f}{r['blows']:>6}{r['score']:>7.2f}")
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
