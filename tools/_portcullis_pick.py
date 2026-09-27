#!/usr/bin/env python3
"""AN ONSLAUGHT WINDOW, TO FILM. v100.

    python _portcullis_pick.py --game <the stage-6 link>

`_ironwood_pick.py`'s shape. What has to be ON SCREEN (and in the ear) is the
whole of v72 §7: the cast (the ward's ring thickening into the plated shell,
the gate's clang), the charge (the speed-streak behind the ball), slams (the
plate flash, the glint and sparks, the number in vigil's glow, the WARD tag
ticking up, the thud and the latch of the bank), the fill brightening as the
pool grows -- and the close, so the window must close BY ITS CLOCK (the only
way to see the plates crack and fall and hear the three clinks).

A window is scored on that: a clock close 4; each slam 0.5 (to 8); each slam
that floats a number 0.4 (to 6); the pool it reaches, 2 x shield / cap; the
share of window frames the streak is lit, x2. AND A CLEAN FRAME FIRST: a
window with the foe's own ultimate up on the clip -- cast in the 8s before the
window opens, inside it, or in the 1.8s tail after its close -- ranks below
every clean one. A filter, not a weight, because two picks were filmed with a
1-point weight and the foe's set-piece took the frame both times: Twinshade's
Triplicate, cast 5s before the window, filled most of it with shades, and
Thornshear's Winnowing, cast on the close, took the tail and the falling
plates with it. Code's pick under
Rick's "you pick i overrule" -- the weights are the pick, stated.

THE FOES LEFT OUT, and why:
  - the vigil relics: the same school's pink on both balls, and the viewer has
    to tell the shell from the foe's ward ring;
  - the batch's redesigns still in flight (`IN_FLIGHT`, CLAIMS.md's BUILD
    rows): their ultimates change when they are carried onto the chain, and
    with them the fight this clip shows.

The tool prints the `--at` and `--window` to hand `cinema_clip`. RICK WATCHES
THE ULT'S WINDOW AND NOT THE WHOLE FIGHT.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "portcullis"
IN_FLIGHT = ("widowmaker", "lightkeeper", "censer", "spellbreaker", "oathwound",
             "aureole", "ironhail", "thornwake", "heartwood")

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, CAP = AC.STATUS.ward.cap;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a, side = me === m.a ? 0 : 1;
    let step = 0, win = null, best = null;
    const wins = [], foeUlts = [];
    while (!m.over && step < secs / DT){
      const Z0 = me.ultRam, sl0 = me.ramTally ? me.ramTally.slams : 0, uf0 = th.ultsFired;
      m.step(DT); step++;
      const Z = me.ultRam;
      if (th.ultsFired > uf0) foeUlts.push(m.t);
      if (Z && !win) win = { t: m.t, slams: 0, numbered: 0, peak: 0, frames: 0, lit: 0, foeCast: 0, clock: 0, end: m.t };
      if (win){
        if (Z){
          win.frames++;
          if (me.ramRun > 0.5) win.lit++;
          win.peak = Math.max(win.peak, me.shield);
          const ds = (me.ramTally ? me.ramTally.slams : 0) - sl0;
          if (ds > 0){
            win.slams += ds;
            for (let i = m.beats.length - 1, n = 0; i >= 0 && n < 32; i--, n++)
              if (m.beats[i].ram && m.beats[i].side === side){ if (Math.round(m.beats[i].dmg) >= 1) win.numbered++; break; }
          }
        }
        win.end = m.t;
        if (!Z){
          win.clock = (Z0 && Z0.t + DT >= Z0.dur && me.alive) ? 1 : 0;
          wins.push(win);
          win = null;
        }
      }
    }
    /* SCORED WHEN THE FIGHT IS DONE, so a foe cast in the tail is seen */
    for (const w of wins){
      w.foeCast = foeUlts.some(t => t >= w.t - 8 && t <= w.end + 1.8) ? 1 : 0;
      w.score = (w.clock ? 4 : 0) + Math.min(w.slams, 8) * 0.5 + Math.min(w.numbered, 6) * 0.4
              + 2 * Math.min(1, w.peak / CAP) + (w.frames ? 2 * w.lit / w.frames : 0);
      w.foe = foe; w.seed = sd; w.dur = w.end - w.t;
      w.litPct = w.frames ? 100 * w.lit / w.frames : 0;
      if (!best || w.foeCast < best.foeCast || (w.foeCast === best.foeCast && w.score > best.score)) best = w;
    }
    if (best) out.push(best);
  }
  out.sort((p, q) => (p.foeCast - q.foeCast) || (q.score - p.score));
  return out.slice(0, 12);
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=100101)
    ap.add_argument("--foes", type=int, default=12)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--out", default="../07-shorts/v100/onslaught-window.mp4")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => [w.id, typeof w.aff === 'string' ? w.aff : w.aff.key])")
        school = dict(ids)[RID]
        pool = [i for i, af in ids if i != RID and af != school and i not in IN_FLIGHT]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        seeds = [a.seed0 + 37 * i for i in range(a.seeds)]
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]
        print(f"\n  {gp.name}  ·  {len(foes)} foes x {len(seeds)} seeds  ({', '.join(foes)})\n")
        print(f"  {'foe':<14}{'seed':>7}{'cast at':>9}{'window':>8}{'clock':>7}"
              f"{'slams':>7}{'nums':>6}{'peak':>7}{'lit%':>7}{'foeUlt':>8}{'score':>7}")
        for r in rows:
            print(f"  {r['foe']:<14}{r['seed']:>7}{r['t']:>9.2f}{r['dur']:>8.2f}"
                  f"{r['clock']:>7}{r['slams']:>7}{r['numbered']:>6}{r['peak']:>7.1f}{r['litPct']:>7.1f}"
                  f"{r['foeCast']:>8}{r['score']:>7.1f}")
        if rows:
            b = rows[0]
            lead = 1.2
            print(f"\n  FILM THE WINDOW AND NOT THE FIGHT:\n")
            print(f"    python cinema_clip.py --game {a.game} "
                  f"--a {RID} --b {b['foe']} --seed {b['seed']} \\")
            print(f"      --at {max(0, b['t'] - lead):.2f} "
                  f"--window {b['dur'] + lead + 1.8:.2f} --end-at-window "
                  f"--fps 60 --w 540 --out {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
