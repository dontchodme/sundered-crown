#!/usr/bin/env python
"""CULVERIN, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v96.

    python culverin_probe.py --game ../02-chain/sc-slug.html [--seeds 2]

Plays Culverin against every relic in the build, from BOTH sides, stepping the
engine itself, and asserts what `CULVERIN-BUILD-BRIEF.md` §2 says each stage
must be true of. Every check is a count of EVENTS, not of frames on which an
event was possible (CLAUDE.md, five times: a check that counts frames in which
an event is possible is not counting the event).

STAGE 2 -- THE SPELL:
  [1] every slug leaves with the slug's numbers (r, grav, dmgMul, speed, life)
  [2] the cadence is 0.55 EXACTLY: on every step that looses a slug, `fireCd`
      moves by `cadence - dt` and nothing else
  [3] every live slug's vy grows by exactly grav*dt on every step the world
      moves, and not at all on a frozen one; vx never changes
  [4] a slug that reaches a wall is spent -- no slug bounces
  [5] slugs are clankable: some are batted out of the air, over the run
  [6] blows a fight: the brief's ~14, at 1.6 (slugs and blade together)
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const foes = AC.WEAPONS.map(x => x.id).filter(x => x !== rid);
  const T = { fights: 0, wins: 0, spawned: 0, badSpawn: [], cadSteps: 0, badCad: [],
              gravSteps: 0, frozenSteps: 0, badGrav: [], bounced: 0,
              slugHits: 0, blows: 0, hitsRemoved: 0, wallRemoved: 0, otherRemoved: 0,
              dur: 0 };
  for (const foeId of foes) for (const sd of seeds) for (const side of ['A', 'B']){
    const m = side === 'A' ? new AC.Match(rid, foeId, sd) : new AC.Match(foeId, rid, sd);
    m.slLive = false;
    const me = m.a.w.id === rid ? m.a : m.b, own = me === m.a ? 'a' : 'b';
    const landed = new Set();
    const orig = m.resolveHit;
    m.resolveHit = function(self, tgt, x, y, seg, mul, over){
      if (self === me && this._cineShot && !this._cineShot.shell){ T.slugHits++; landed.add(this._cineShot); }
      return orig.call(this, self, tgt, x, y, seg, mul, over);
    };
    let step = 0;
    while (!m.over && step < secs / DT){
      const frozen = m.over || m.latch || m.splitHold || m.hitStop > 0;
      const mine = new Map();
      for (const s of m.shots) if (s.own === own && !s.shell) mine.set(s, [s.vx, s.vy]);
      const fc0 = me.fireCd, f0 = me.shotsFired;
      m.step(DT); step++;
      // [1] [2] the loose
      if (me.shotsFired > f0){
        const d = me.fireCd - fc0;
        T.cadSteps++;
        if (Math.abs(d - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push({ t: m.t, d });
        for (const s of m.shots){
          if (s.own !== own || s.shell || mine.has(s)) continue;
          T.spawned++;
          /* SEEN AFTER ONE TICK, ALWAYS. `tickFire` looses the slug and
             `tickShots` moves it in the SAME step (the fighter loop runs
             first), so the probe meets it with one step of gravity in its vy
             and one step off its life. Undo exactly that and nothing else. */
          const sp = Math.hypot(s.vx, s.vy - s.grav * DT);
          const ok = s.r === S.r && s.grav === S.grav && s.dmgMul === S.dmgMul
                  && Math.abs(sp - S.speed) < 1e-6 && s.life === S.life - DT && !(s.bounce > 0);
          if (!ok && T.badSpawn.length < 5) T.badSpawn.push({ r: s.r, grav: s.grav, dmgMul: s.dmgMul, sp, life: s.life });
        }
      }
      // [3] [4] the fall, and what became of every slug that left the hall
      const live = new Set(m.shots);
      for (const [s, v0] of mine){
        if (!live.has(s)){
          if (landed.has(s)) T.hitsRemoved++;
          else {
            const A = AC.CONFIG.arena, n = m.inset;
            if (s.x < n + s.r + 1 || s.x > A.w - n - s.r - 1 || s.y < n + s.r + 1 || s.y > A.h - n - s.r - 1) T.wallRemoved++;
            else T.otherRemoved++;
          }
          continue;
        }
        if (frozen){
          T.frozenSteps++;
          if ((s.vy !== v0[1] || s.vx !== v0[0]) && T.badGrav.length < 5) T.badGrav.push({ frozen: true, dvy: s.vy - v0[1] });
        } else {
          T.gravSteps++;
          if (s.vx !== v0[0]){ T.bounced++; continue; }
          if (Math.abs((s.vy - v0[1]) - s.grav * DT) > 1e-9 && T.badGrav.length < 5)
            T.badGrav.push({ dvy: s.vy - v0[1], want: s.grav * DT });
        }
      }
    }
    T.fights++; T.dur += m.t; T.blows += me.hits;
    if (m.winner === me) T.wins++;
  }
  return T;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="culverin")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--secs", type=float, default=200.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    t0 = time.time()
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        T = page.evaluate(JS, [a.relic, seeds, a.secs])
        assert not errors, errors
    F = T["fights"]
    print(f"CULVERIN PROBE -- {a.game}   {F} fights (every foe x {a.seeds} seeds x both sides)"
          f"   {time.time()-t0:.0f}s")
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["spawned"] > 20 * F and not T["badSpawn"], "[1] every slug leaves with the slug's numbers",
          f"{T['spawned']} slugs seen alive after their first step, of {T['cadSteps']} loosed"
          f" -- the rest were spent on the step they left (a slug loosed into the floor)"
          + (f"  BAD {T['badSpawn']}" if T["badSpawn"] else ""))
    check(T["cadSteps"] > 0 and not T["badCad"], "[2] the cadence is exact",
          f"{T['cadSteps']} looses, fireCd moved by cadence - dt on every one" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["gravSteps"] > 1000 and T["frozenSteps"] > 0 and not T["badGrav"],
          "[3] vy grows by grav*dt on every moving step and not on a frozen one",
          f"{T['gravSteps']} moving slug-steps, {T['frozenSteps']} frozen" + (f"  BAD {T['badGrav']}" if T["badGrav"] else ""))
    check(T["bounced"] == 0 and T["wallRemoved"] > 0, "[4] no slug bounces; a slug at a wall is spent",
          f"{T['wallRemoved']} spent on a wall, {T['bounced']} changed vx in flight")
    check(T["otherRemoved"] > 0, "[5] slugs are clankable",
          f"{T['otherRemoved']} gone mid-hall without landing (batted, or eaten by Scour's band)")
    bl = T["blows"] / F
    check(11 <= bl <= 17, "[6] blows a fight, the brief's ~14",
          f"{bl:.2f} blows a fight, {T['slugHits']/F:.2f} of them slugs; {T['hitsRemoved']} slugs landed")
    print(f"\n  win {T['wins']/F:.1%} over the probe's {F} fights (a probe, not a measurement)   "
          f"mean {T['dur']/F:.1f}s")
    print(f"  {sum(res)}/{len(res)}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(T, indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
