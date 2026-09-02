#!/usr/bin/env python
"""SCOUR, ASSERTED AGAINST THE BUILD -- one check per sentence of stage 2.

    python scour_probe.py --game ../02-chain/sc-scour.html

Stage 2 is "the tornado exists and sweeps, and touches nobody", so every check
here is about EXISTENCE and MOTION, and the ones about damage are checks that
nothing happened. Stage 3 adds the catch and this file grows with it.

WRITTEN THE WAY `garrote_relic_probe` HAD TO BE REWRITTEN, and the reason is
CLAUDE.md's most repeated lesson: **a check that counts frames in which an
event is possible is not counting the event.** It has produced false defects
five times in one file (v60), five more in v59 and three in v61 -- always on
this engine, because every impact opens with a hit stop and a frozen frame
looks exactly like a mechanic that failed to fire. So the motion checks below
skip frozen frames explicitly and count TRANSITIONS rather than states.
"""
from __future__ import annotations
import argparse, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const out = { casts:0, frames:0, alive:0, samples:[], bounces:0,
                widths:{}, tops:{}, minCx: 1e9, maxCx:-1e9,
                movedFrozen:0, movedFree:0, outOfHall:0, dur:{lo:1e9,hi:-1e9},
                cutByMatch:0, ended:0, wall:{lo:1e9,hi:-1e9},
                hpMoved:0, ticks:0, err:null };
  for (const foe of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foe, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let prev = null, born = 0, lastDir = 0;
      let hpA = th.hp;
      let step = 0;
      while (!m.over && step < secs / DT){
        const before = m.tornado ? { cx:m.tornado.cx, dir:m.tornado.dir,
                                     t:m.tornado.t } : null;
        const frozen = m.hitStop > 0;
        const hpBefore = th.hp;
        m.step(DT); step++;
        const T = m.tornado;
        if (T && !before){ out.casts++; born = m.t; }
        if (!T && before){
          /* THE WINDOW'S OWN CLOCK, NOT THE MATCH'S. `T.t` advances only on
             live steps -- `step()` returns through `decayImpactOnly` while
             `hitStop` runs -- so wall-clock time is always LONGER than the
             window and measuring `m.t - born` reads a 10s window as 12.38s.
             That is the fault Bloodmirror's probe filed against 24 of 24
             landings, and it is on CLAUDE.md's list.

             `before.t` is the last value the window ever held: `t` is advanced
             inside the same step that deletes the object, so a sampler reading
             after the step sees nothing at all. */
          const d = +before.t.toFixed(2);
          const w = +(m.t - born).toFixed(2);
          if (!m.over){
            if (w < out.wall.lo) out.wall.lo = w;
            if (w > out.wall.hi) out.wall.hi = w;
          }
          /* AND A WINDOW THE MATCH ENDED IS NOT A SHORT WINDOW. The over-path
             nulls the tornado, so a cast landing seconds before the kill dies
             with the fight -- counted separately rather than dragging the
             minimum down to 0.22s. */
          if (m.over) out.cutByMatch++;
          else {
            if (d < out.dur.lo) out.dur.lo = d;
            if (d > out.dur.hi) out.dur.hi = d;
            out.ended++;
          }
        }
        if (T){
          out.frames++;
          out.widths[T.w] = 1; out.tops[T.top] = 1;
          if (T.cx < out.minCx) out.minCx = T.cx;
          if (T.cx > out.maxCx) out.maxCx = T.cx;
          const half = T.w * 0.5, n = m.inset;
          /* THE EDGE STAYS IN THE HALL. Not the centre -- the brief is explicit
             that the band's EDGE is what reaches the wall, and a check on the
             centre would pass on a band with half its width in the stone. */
          if (T.cx - half < n - 0.5 || T.cx + half > A.w - n + 0.5)
            out.outOfHall++;
          if (before){
            const moved = Math.abs(T.cx - before.cx) > 1e-9;
            /* SPLIT BY WHETHER THE WORLD WAS FROZEN. A band that does not move
               during a hit stop is CORRECT -- it is advanced by the ordinary
               step like everything else -- and a probe that did not split these
               would report the freeze as a stalled sweep. That is the exact
               false defect `garrote_relic_probe` filed 294 times. */
            if (frozen){ if (moved) out.movedFrozen++; }
            else if (moved) out.movedFree++;
            if (before.dir !== T.dir) out.bounces++;
          }
        }
        /* STAGE 2 TOUCHES NOBODY. Damage taken by the quarry while a band
           stands is not proof of anything on its own -- the blade is still
           swinging -- so what is counted is damage on a frame where the band
           exists AND the two are not in weapon contact. Kept coarse on
           purpose: any nonzero here is worth reading by hand. */
        if (T && th.hp < hpBefore) out.hpMoved++;
        hpA = th.hp;
      }
      if (m.tornado) out.alive++;
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-scour.html")
    ap.add_argument("--relic", default="duskreave")
    ap.add_argument("--foes", default="lastlight,ironhail,grudgebearer,axiom")
    ap.add_argument("--seeds", default="")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    A = ap.parse_args()
    seeds = ([int(x) for x in A.seeds.split(",")] if A.seeds
             else [11961 + i * 977 for i in range(A.n)])
    foes = A.foes.split(",")

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        r = pg.evaluate(RUN_JS, [A.relic, foes, seeds, A.secs])

    n_fights = len(foes) * len(seeds)
    print(f"\nSCOUR -- stage 2, {n_fights} fights "
          f"({len(foes)} foes x {len(seeds)} seeds)\n")
    checks = []

    def chk(ok, label, detail):
        checks.append(ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}\n        {detail}")

    chk(r["casts"] > 0, "the ultimate casts at all",
        f"{r['casts']} casts over {n_fights} fights "
        f"({r['casts']/n_fights:.2f} a fight; charge 15 predicts ~2)")
    # JS OBJECT KEYS ARE STRINGS. The first cut compared them against ints and
    # failed on a build that was carrying exactly the right numbers.
    widths = sorted(float(k) for k in r["widths"])
    tops = sorted(float(k) for k in r["tops"])
    chk(widths == [160.0] and tops == [600.0],
        "the band carries the brief's numbers, and only those",
        f"w {widths}, top {tops} -- one value each across every fight")
    chk(r["movedFree"] > 0 and r["movedFrozen"] == 0,
        "it sweeps on live frames and is frozen by hit stop",
        f"{r['movedFree']} live frames moved, {r['movedFrozen']} frozen frames "
        f"moved (must be 0 -- it is advanced by the ordinary step)")
    chk(r["bounces"] > 0, "it bounces off the walls",
        f"{r['bounces']} direction changes over {r['frames']} band-frames")
    chk(r["outOfHall"] == 0, "the band's EDGE never leaves the hall",
        f"{r['outOfHall']} frames with an edge in the stone "
        f"(cx ran {r['minCx']:.0f}..{r['maxCx']:.0f})")
    chk(r["alive"] == 0, "no band outlives its match",
        f"{r['alive']} matches ended with one standing")
    lo, hi = r["dur"]["lo"], r["dur"]["hi"]
    wlo, whi = r["wall"]["lo"], r["wall"]["hi"]
    chk(r["ended"] > 0 and abs(hi - 10.0) < 0.05 and abs(lo - 10.0) < 0.05,
        "the window runs its stated 10s on its OWN clock",
        f"{r['ended']} windows ran out: {lo:.2f}s .. {hi:.2f}s of window time, "
        f"{wlo:.2f}s .. {whi:.2f}s of WALL time "
        f"({r['cutByMatch']} more were ended by the match and are not counted)")

    print(f"\n  THE GAP BETWEEN THOSE TWO CLOCKS IS HIT STOP, and it is worth")
    print(f"  knowing before stage 3: a 10.00s window occupies up to "
          f"{whi:.2f}s of")
    print("  the fight, because `step()` returns through `decayImpactOnly`")
    print("  while a freeze runs and the window's own clock stops with it.")
    print("  A tick rate of 7/s is 70 ticks a window in WINDOW time, and the")
    print("  quarry is inside the band for rather longer than that in wall time.")

    print(f"\n  and for stage 3 to change: the quarry lost hp on "
          f"{r['hpMoved']} band-frames.")
    print("  STAGE 2 DOES NOT MAKE THAT ZERO -- the blade is still swinging.")
    print("  It is recorded so stage 3's ticks have a BEFORE to be read")
    print("  against, which is the only way to tell a tick from a blade blow.")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:6], sep="\n    ")
    ok = sum(1 for c in checks if c)
    print(f"\n{ok}/{len(checks)} checks passed")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
