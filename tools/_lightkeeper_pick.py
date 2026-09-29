#!/usr/bin/env python3
"""A BULWARK WINDOW, TO FILM. v107.

    python _lightkeeper_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape (by way of `_ironhail_pick.py`). What has to be ON
SCREEN (and in the ear) is the whole of v77 §5: the cast (the raise, a plate's
ring sliding up; the bar rising out of the ward ring), BLOCKS (the gong, the
bar flashing white, the foe bounced), ARROWS dying on the wall (the tink, the
scorch on the bar), THE BANK (a ward "+3" floating off the caster, and the
WARD tag once a window -- neither shows when the shield is already at its
cap), and the close BY ITS CLOCK (the fold, the slide reversed; the bar folding
back into the ring). A window that a death ends, or the match's end, shows no
fold and plays none, so it scores nothing; so does a window without a block,
an arrow or a bank. The fight must also run on for the clip's tail (1.8s past
the close), or the kill takes the picture. Past that the score counts the
blocks (to 8) and the arrows (to 6), a frame with two or more arrows (the
flam: the tinks heard one by one), the banks the viewer sees, and the blade's
blows in the window.

A window is scored on that, and the tool prints the `--at` and `--window` to
hand `cinema_clip`. RICK WATCHES THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
Lightkeeper plays side A, as `cinema_clip --a lightkeeper` films it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "lightkeeper"
TAIL = 1.8

JS = r"""([rid, foes, seeds, secs, tail]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a, th = m.b;
    let step = 0, win = null, best = null, pend = null;
    while (!m.over && step < secs / DT){
      const Z0 = me.ultWall, h0 = me.hits;
      const T0 = me.wallTally ? { b: me.wallTally.blocks, a: me.wallTally.arrows, k: me.wallTally.banked } : { b: 0, a: 0, k: 0 };
      m.step(DT); step++;
      /* a clock-closed window waits for its tail: the fight must run on */
      if (pend && m.t >= pend.end + tail){ pend.tailOk = 1; pend.score += 3; if (!best || pend.score > best.score) best = pend; pend = null; }
      const Z = me.ultWall, T = me.wallTally;
      if (Z && !win) win = { t: m.t, blows: 0, blocks: 0, arrows: 0, banked: 0, banks: 0, flam: 0, clock: 0, end: m.t, tailOk: 0,
                             shield0: me.shield };
      if (!win) continue;
      if (T){
        const dB = T.blocks - T0.b, dA = T.arrows - T0.a, dK = T.banked - T0.k;
        win.blocks += dB; win.arrows += dA;
        if (dK >= 1){ win.banked += dK; win.banks++; }
        if (dA >= 2) win.flam++;
      }
      if (Z){ win.blows += me.hits - h0; win.end = m.t; continue; }
      /* THE CLOSE: by the clock with both alive, the only close that folds and sounds */
      win.end = m.t;
      win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive && th.alive && !m.over) ? 1 : 0;
      win.score = win.clock && win.blocks > 0 && win.arrows > 0 && win.banks > 0
        ? (4 + Math.min(win.blocks, 8) * 0.5 + Math.min(win.arrows, 6) * 0.6 + (win.flam ? 0.5 : 0)
           + Math.min(win.banks, 6) * 0.2 + Math.min(win.blows, 8) * 0.2)
        : 0;
      win.foe = foe; win.seed = sd; win.dur = win.end - win.t;
      if (win.score > 0) pend = win;
      win = null;
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 16);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=107201)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--also", default="gloamwire:107602,aureole:4101,marrowdraw:2207,spellbreaker:99015",
                    help="foe:seed pairs scored besides the grid (the voice lab's real window, the picture lab's looks)")
    ap.add_argument("--out", default="../07-shorts/v107/bulwark-window.mp4")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != RID]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs, TAIL])
        for pair in [x for x in a.also.split(",") if x]:
            f, sd = pair.split(":")
            rows += page.evaluate(JS, [RID, [f], [int(sd)], a.secs, TAIL])
        rows.sort(key=lambda r: -r["score"])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  every foe ({len(foes)}) x {len(seeds)} seeds (+ {a.also})  ·  Lightkeeper side A\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>6}{'blocks':>7}{'arrows':>7}"
              f"{'flam':>5}{'banks':>6}{'banked':>7}{'blows':>6}{'score':>7}")
        for r in rows[:16]:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}{r['clock']:>6}{r['blocks']:>7}"
                  f"{r['arrows']:>7}{r['flam']:>5}{r['banks']:>6}{r['banked']:>7.0f}{r['blows']:>6}{r['score']:>7.2f}")
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
