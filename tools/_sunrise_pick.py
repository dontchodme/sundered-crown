#!/usr/bin/env python3
"""A DAYBREAK SUN, TO FILM. v99.

    python _sunrise_pick.py --game ../02-chain/sc-sunrise-fx.html

`_dawn_pick.py`'s shape, on the brief's whole sentence (v99 stage 4): a SHORT
arming, the break in frame, the foe crossing the rim at least twice, and a
CLOCK sunset -- so the clip has every one of the four things a viewer must be
able to say with the card off: he swung; where the sword hit, the sun came up;
a circle of sunlight spread from there; the other ball burned whenever it was
inside it (and not when it was out).

A sun is scored on that, from the cast that armed it to 0.7s past its set, and
the tool prints the `--at` and `--window` to hand `cinema_clip`. RICK WATCHES
THE ULTIMATE'S WINDOW AND NOT THE WHOLE FIGHT -- and he watches it with the
card hidden.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "dawnbringer"

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let step = 0, cast = null, sun = null, best = null, lastUp = -99;
    while (!m.over && step < secs / DT){
      const t0 = me.sunriseTally ? me.sunriseTally.ticks : 0;
      const up0 = !!(me.ultSunrise && me.ultSunrise.up), x0 = me.ultSunrise && me.ultSunrise.x;
      m.step(DT); step++;
      const S = me.ultSunrise;
      /* A CLEAN OPENING: a sun whose lead-in still has an earlier sun on
         screen (up, or setting: 0.65s) opens the clip on the wrong dawn */
      if (S && S.armed && !S.up && cast === null && !sun) cast = m.t;
      /* a sun breaks: the one being scored is the first after this cast */
      if (!sun && cast !== null && S && S.up && (!up0 || S.x !== x0))
        sun = { cast, brk: m.t, ticks: 0, ins: 0, frames: 0, cross: 0, was: null, clock: 0, end: m.t,
                clean: cast - lastUp > 1.0 + 0.65 + 0.2 };
      if (sun){
        if (me.sunriseTally) sun.ticks += me.sunriseTally.ticks - t0;
        if (S && S.up && S.x === sun.x0 || S && S.up && sun.x0 === undefined){
          sun.x0 = S.x;
          const r = me.w.ult.r * Math.min(1, S.t / me.w.ult.grow);
          const inn = th.alive && Math.hypot(th.x - S.x, th.y - S.y) < r + R;
          sun.frames++; if (inn) sun.ins++;
          if (sun.was !== null && inn !== sun.was) sun.cross++;
          sun.was = inn;
          sun.end = m.t;
        } else {
          sun.clock = (!S || !S.up) && me.alive && !m.over ? 1 : 0;   // not replaced, not a death
          const arm = sun.brk - sun.cast;
          /* a short arming is a clip that gets to the point; one longer than
             3s is mostly waiting */
          sun.score = (sun.clock ? 4 : 0) + Math.min(sun.cross, 5) * 1.0
                    + Math.min(sun.ticks, 14) * 0.4 + (sun.frames ? 2 * sun.ins / sun.frames : 0)
                    - Math.max(0, arm - 1.5) * 1.2;
          sun.foe = foe; sun.seed = sd; sun.arm = arm;
          sun.inPct = sun.frames ? 100 * sun.ins / sun.frames : 0;
          if (sun.cross >= 2 && sun.clock && sun.clean && (!best || sun.score > best.score)) best = sun;
          sun = null; cast = null;
        }
      }
      if (S && S.up) lastUp = m.t;          /* after this frame's tests */
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => q.score - p.score);
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-sunrise-fx.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=99101)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v99/daybreak-sun.mp4")
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
        print(f"  {'foe':<14}{'seed':>7}{'cast':>8}{'arming':>8}{'break':>8}{'set':>8}"
              f"{'ticks':>7}{'in%':>7}{'cross':>7}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['cast']:>8.2f}{r['arm']:>8.2f}{r['brk']:>8.2f}"
                  f"{r['end']:>8.2f}{r['ticks']:>7}{r['inPct']:>7.1f}{r['cross']:>7}{r['score']:>7.1f}")
        if rows:
            b = rows[0]
            lead = 1.0
            print(f"\n  FILM THE SUN AND NOT THE FIGHT (the cast, the break, the sun, the set):\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['cast'] - lead):.2f} "
                  f"--window {b['end'] - b['cast'] + lead + 1.4:.2f} "
                  f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
