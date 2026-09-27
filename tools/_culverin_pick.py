#!/usr/bin/env python
"""AN IRONFALL WINDOW, TO FILM. v96.

    python _culverin_pick.py --game ../02-chain/sc-ironfall.html

`_corollary_pick.py`'s shape. CLAUDE.md §4.0: film before you tune if the
ultimate is a picture, and the brief's stage-3 gate is "FILM the landing ring
and the burst". So a window is scored on what has to be ON SCREEN: shells that
strike the foe in flight, a burst that LANDS (rare -- a shell that reaches its
mark has usually missed), bursts at all, and slugs in the air between them --
and marked down for shells that die on a wall, because a window of wall-splats
says nothing about where the foe was going to be.

A window is the span `me.ultIronfall` exists, plus the last shell's 0.85s.
Prints the `--at` and `--window` to hand `cinema_clip` (Rick watches the ult's
window and not the whole fight).
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match(rid, foe, sd);
    m.slLive = false;
    const me = m.a.w.id === rid ? m.a : m.b, own = me === m.a ? 'a' : 'b';
    let inShots = false, W = null;
    const oRH = m.resolveHit;
    m.resolveHit = function(self, tgt, x, y, seg, mul, over){
      if (W && self === me){
        const cs = this._cineShot;
        if (cs && cs.shell) W.hit++; else if (!cs && inShots) W.popHit++;
      }
      return oRH.call(this, self, tgt, x, y, seg, mul, over);
    };
    const oTS = m.tickShots;
    m.tickShots = function(dt){ inShots = true; try { return oTS.call(this, dt); } finally { inShots = false; } };
    let step = 0;
    while (!m.over && step < secs / DT){
      const mine = new Map();
      if (W) for (const s of m.shots) if (s.own === own && s.shell) mine.set(s, s.life);
      m.step(DT); step++;
      if (me.ultIronfall && !W) W = { t0: m.t, hit: 0, popHit: 0, pops: 0, wall: 0, shells: 0, end: null, slugs: 0 };
      if (W){
        const alive = new Set(m.shots);
        for (const [s, l0] of mine) if (!alive.has(s)){ if (s.life <= 0) W.pops++; else W.wall++; }
        for (const s of m.shots) if (s.own === own && s.spell === 'slug') W.slugs++;
        if (!me.ultIronfall && W.end === null) W.end = m.t;
        if (W.end !== null && m.t > W.end + 0.9){
          W.score = W.hit * 3 + W.popHit * 6 + W.pops * 1.0 - W.wall * 0.3;
          out.push(Object.assign({ foe, seed: sd, alive: me.alive && (m.a.alive && m.b.alive) }, W));
          W = null;
        }
      }
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-ironfall.html")
    ap.add_argument("--relic", default="culverin")
    ap.add_argument("--foes", default="emberedge,axiom,farwarden,gravemourn,thornshear,vinesower,heartwood,oathwound")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed0", type=int, default=3301)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [a.relic, a.foes.split(","), seeds, 200.0])
        assert not errors, errors
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} Ironfall windows over {len(a.foes.split(','))} foes x {a.seeds} seeds")
    print(f"  {'score':>6}  {'foe':<12}{'seed':>6}  {'t0':>6}  hit  popHit  pops  wall   film")
    for r in rows[:a.top]:
        at = max(0.0, r["t0"] - 0.6)
        win = (r["end"] - r["t0"]) + 1.6
        print(f"  {r['score']:>6.1f}  {r['foe']:<12}{r['seed']:>6}  {r['t0']:>6.1f}  {r['hit']:>3}  {r['popHit']:>6}  "
              f"{r['pops']:>4}  {r['wall']:>4}   --a {a.relic} --b {r['foe']} --seed {r['seed']} --at {at:.1f} --window {win:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
