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
  /* THE TICK IS MEASURED AROUND ITS OWN CALL, NOT AROUND THE FRAME IT LANDED
     ON. A frame can carry a tick AND a blade blow, and a blade blow legitimately
     raises hit stop, stun and the beat count -- so a frame-level check would
     report the BLADE as a defect in the tick. That is CLAUDE.md's most repeated
     probe fault in a new costume: a check that counts frames in which an event
     is possible is not counting the event.

     Wrapping `resolveHit` puts the before/after either side of the tick and
     nothing else. The wrapper is installed once and removed with the page. */
  if (!AC.Match.prototype.__scourWrapped){
    const orig = AC.Match.prototype.resolveHit;
    AC.Match.prototype.resolveHit = function(self, foe, hx, hy, seg, mul, over){
      const tick = !!(over && over.beat === false && over.stun === false
                      && over.knock === 0);
      if (!tick) return orig.call(this, self, foe, hx, hy, seg, mul, over);
      const W = window.__scour;
      const b = { hp: foe.hp, stun: foe.stun, stop: this.hitStop,
                  beats: this.beats.length, vx: foe.vx, vy: foe.vy,
                  pool: foe.cursePool.length, sum: foe.curseSum(),
                  latch: !!this.latch, heat: !!self.ultHeat,
                  wire: !!self.ultWire, mines: (this.mines||[]).length,
                  hands: (this.hands||[]).length, alive: foe.alive };
      const r = orig.call(this, self, foe, hx, hy, seg, mul, over);
      const dealt = b.hp - foe.hp;
      W.ticks++;
      W.dealt += dealt;
      /* THE ECHO IS THE RELIC. A tick landing on a NON-EMPTY pool must be
         worth more than one landing on an empty one -- that is the whole
         difference between the `resolveHit` path and the `hurt` path, and it
         is what the +59 rests on. Split rather than averaged, because an
         average over both populations hides it. */
      if (b.sum > 0){ W.withPool++; W.withPoolDmg += dealt; }
      else { W.noPool++; W.noPoolDmg += dealt; }
      if (dealt > W.maxTick) W.maxTick = dealt;
      if (this.hitStop > b.stop){
        W.raisedStop++;
        /* WHICH value, and whether the tick killed -- "hit stop rose" is a
           symptom and the VALUE names the site that raised it. */
        const k = this.hitStop.toFixed(3);
        W.stopVals[k] = (W.stopVals[k] || 0) + 1;
        if (b.alive && !foe.alive) W.stopFatal++;
      }
      if (foe.stun > b.stun) W.raisedStun++;
      /* THE FATAL TICK MUST FILE AND ONLY THE FATAL TICK MAY. */
      const filed = this.beats.length - b.beats;
      if (b.alive && !foe.alive){ W.fatal++; if (filed < 1) W.fatalNoBeat++; }
      else if (filed > 0) W.beatOnOrdinary += filed;
      /* VELOCITY. The tick passes knock 0, so the only thing that may move the
         quarry on this call is nothing at all -- the drag is applied in
         `tickScour`, OUTSIDE this call. */
      if (foe.vx !== b.vx || foe.vy !== b.vy) W.movedByTick++;
      /* NO OTHER `mul === undefined` MECHANIC MAY FIRE OFF A TICK. Every one
         of them tests that the hit is a melee connect, and the tick passes a
         defined `mul` -- this counts whether any of them fired anyway. */
      if ((!!this.latch) !== b.latch) W.latched++;
      if ((!!self.ultHeat) !== b.heat) W.heatChanged++;
      if ((this.mines||[]).length > b.mines) W.stamped++;
      if ((this.hands||[]).length > b.hands) W.slung++;
      /* THE INVARIANT `apply` DERIVES: the stack count IS the pool length. */
      if (foe.stacks("curse") !== foe.cursePool.length) W.poolMismatch++;
      return r;
    };
    AC.Match.prototype.__scourWrapped = 1;
  }
  window.__scour = { ticks:0, dealt:0, withPool:0, withPoolDmg:0,
                     noPool:0, noPoolDmg:0, maxTick:0, raisedStop:0,
                     raisedStun:0, fatal:0, fatalNoBeat:0, beatOnOrdinary:0,
                     movedByTick:0, latched:0, heatChanged:0, stamped:0,
                     slung:0, poolMismatch:0, stopVals:{}, stopFatal:0 };
  const out = { casts:0, frames:0, alive:0, samples:[], bounces:0,
                widths:{}, tops:{}, minCx: 1e9, maxCx:-1e9,
                movedFrozen:0, movedFree:0, outOfHall:0, dur:{lo:1e9,hi:-1e9},
                cutByMatch:0, ended:0, wall:{lo:1e9,hi:-1e9},
                caughtFrames:0, bandFrames:0,
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
        if (T && T.caught) out.caughtFrames++;
        if (T) out.bandFrames++;
        hpA = th.hp;
      }
      if (m.tornado) out.alive++;
    }
  }
  out.tick = window.__scour;
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-grind.html")
    ap.add_argument("--relic", default="duskreave")
    ap.add_argument("--foes", default="lastlight,ironhail,grudgebearer,axiom")
    ap.add_argument("--seeds", default="")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--base", type=float, default=5.0,
                    help="the tick's stated base damage, off "
                         "the ult block")
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

    t = r.get("tick") or {}
    if t.get("ticks"):
        print("\n  ---- STAGE 3: THE TICK ----\n")
        wp, np_ = t["withPool"], t["noPool"]
        wpd = t["withPoolDmg"] / wp if wp else 0.0
        npd = t["noPoolDmg"] / np_ if np_ else 0.0
        # THE HEADLINE CHECK. A tick that always deals round(base x jitter) is
        # collecting no echo and is on the `hurt` path -- which is a +17.8
        # ultimate rather than a +59 one, and every other number would still
        # look plausible.
        base = A.base
        chk(wp > 0 and wpd > base * 1.4,
            "the tick COLLECTS THE CURSE ECHO",
            f"{wpd:.2f} mean damage a tick against a stated base of {base:g} "
            f"-- the echo is {100*(wpd-base)/wpd:.0f}% of it. "
            f"({wp} ticks on a non-empty pool, {np_} on an empty one, "
            f"peak {t['maxTick']})")
        if np_ == 0:
            print("        NOTE: the empty-pool population is EMPTY, so this")
            print("              is measured against the STATED BASE and not")
            print("              against a control arm. The blade applies")
            print("              curse on every blow, so a tornado never")
            print("              catches a quarry whose pool is clean.")
        # A FATAL TICK KEEPS ITS `killStop` ON PURPOSE -- the kill is the shot
        # and no ultimate gets to take that away, so it is excluded here rather
        # than counted as a defect.
        nonfatal_stop = t["raisedStop"] - t["stopFatal"]
        chk(nonfatal_stop == 0 and t["raisedStun"] == 0,
            "a tick carries no weight and no stagger",
            f"{nonfatal_stop} non-fatal ticks raised hit stop "
            f"({t['stopFatal']} fatal ones did, which is `killStop` and is "
            f"correct), {t['raisedStun']} raised stun, over {t['ticks']} ticks"
            + (f"  values={t['stopVals']}" if nonfatal_stop else ""))
        chk(t["movedByTick"] == 0,
            "a tick does not knock; only the drag moves the quarry",
            f"{t['movedByTick']} ticks changed the foe's velocity inside "
            f"resolveHit")
        chk(t["beatOnOrdinary"] == 0 and t["fatalNoBeat"] == 0,
            "no beat except the first catch and the fatal",
            f"{t['beatOnOrdinary']} ordinary ticks filed one; "
            f"{t['fatal']} fatal ticks, {t['fatalNoBeat']} of them silent")
        chk(t["poolMismatch"] == 0,
            "stacks(curse) === cursePool.length after every tick",
            f"{t['poolMismatch']} mismatches over {t['ticks']} ticks")
        chk(t["latched"] == 0 and t["heatChanged"] == 0
            and t["stamped"] == 0 and t["slung"] == 0,
            "no `mul === undefined` mechanic fires off a tick",
            f"latch {t['latched']}, forge heat {t['heatChanged']}, "
            f"stamps {t['stamped']}, hands {t['slung']} -- all must be 0")
        held = (100.0 * r["caughtFrames"] / r["bandFrames"]) \
            if r["bandFrames"] else 0.0
        print(f"\n  the quarry was inside the band on {held:.1f}% of "
              f"band-frames")
        print(f"  {t['ticks']} ticks, {t['dealt']:.0f} damage, "
              f"{t['dealt']/max(1,t['ticks']):.2f} a tick")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:6], sep="\n    ")
    ok = sum(1 for c in checks if c)
    print(f"\n{ok}/{len(checks)} checks passed")
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
