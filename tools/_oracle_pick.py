#!/usr/bin/env python3
"""A FORESIGHT WINDOW, TO FILM. v105.

    python _oracle_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape, by way of `_bindweed_pick.py`. What has to be ON
SCREEN (and in the ear) is the whole of v75 §6: the cast's rune-eye opening
with its inhale-into-chime, the sigil's shimmer for the whole window, the rune
on the floor where the foe will be with its sight-line from the bow, the
window arrows' rune riding the shaft, landed arrows' flares with their snaps
and the HEX tag ticking by two -- and the close BY ITS CLOCK, the only close
the eye shuts to its reversed chime (a death close is silent, and a kill takes
the picture). So a window scores nothing unless it closes by its clock with
both alive, lands at least one window arrow that hexes twice, and the fight
runs on for the clip's tail (1.8s past the close).

Points then come from: the window arrows that land (0.35 each, to 12); the hex
counts heard (1.0 per distinct count the snaps carry, to 5 -- the snap steps a
semitone a count, so a window that climbs 2-3-4-5 beats one that sits at the
cap); the rune AT the lead (1.5 x the share of window frames whose lead is
inside the hall, so the rune is the prophecy and not its clamp at the wall);
and the lock (1.0 x the share of window frames the bow already sits within
turn x dt of the lead, so the sight-line is the arrows' path).

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Oracle plays side A, as `cinema_clip --a oracle` films it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "oracle"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a, th = m.b;
    let step = 0, win = null, best = null, pend = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultSight, zt0 = Z0 ? Z0.t : -1, T0 = me.sightTally ? Object.assign({}, me.sightTally) : null;
      m.step(DT); step++;
      /* a clock-closed window waits for its tail: the fight must run on */
      if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; if (!best || pend.score > best.score) best = pend; pend = null; }
      const Z = me.ultSight, T = me.sightTally;
      if (Z && !win) win = { t: m.t, arrows: 0, hexes: 0, ns: {}, frames: 0, inHall: 0, locked: 0, clock: 0, end: m.t, tailOk: 0,
                            hex0: th.stacks("hex") };
      if (!win) continue;
      if (Z){
        const live = !(Z === Z0 && Z.t === zt0);          // a hit stop does not tick the window
        if (live){
          win.frames++;
          const tof = Math.hypot(th.x - me.x, th.y - me.y) / me.w.shot.speed;
          const lx = th.x + th.vx * tof, ly = th.y + th.vy * tof, e = (m.inset || 0) + 16;
          if (lx >= e && lx <= A.w - e && ly >= e && ly <= A.h - e) win.inHall++;
          const b = Math.atan2(ly - me.y, lx - me.x), d = Math.atan2(Math.sin(b - me.theta), Math.cos(b - me.theta));
          if (Math.abs(d) <= me.w.ult.turn * DT) win.locked++;
        }
        const na = T.arrows - (T0 ? T0.arrows : 0), nh = T.hex - (T0 ? T0.hex : 0);
        win.arrows += na;
        if (nh > 0){ win.hexes += nh; const n = th.stacks("hex"); win.ns[n] = (win.ns[n] || 0) + 1; }
        win.end = m.t;
        continue;
      }
      /* THE CLOSE */
      win.end = m.t;
      win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive) ? 1 : 0;
      const kinds = Object.keys(win.ns).length;
      win.hallPct = win.frames ? 100 * win.inHall / win.frames : 0;
      win.lockPct = win.frames ? 100 * win.locked / win.frames : 0;
      win.score = (win.clock && win.hexes > 0) ? (4 + Math.min(win.arrows, 12) * 0.35 + Math.min(kinds, 5) * 1.0
                                                  + 1.5 * win.hallPct / 100 + 1.0 * win.lockPct / 100) : 0;
      win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
      win.nList = Object.keys(win.ns).sort().join("");
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
    ap.add_argument("--seed0", type=int, default=105201)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v105/foresight-window.mp4")
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
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds  ·  Oracle side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'arrows':>7}{'hexes':>6}"
              f"{'n':>7}{'hex0':>5}{'hall%':>7}{'lock%':>7}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['arrows']:>7}"
                  f"{r['hexes']:>6}{r['nList']:>7}{r['hex0']:>5}{r['hallPct']:>7.1f}{r['lockPct']:>7.1f}{r['score']:>7.2f}")
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
