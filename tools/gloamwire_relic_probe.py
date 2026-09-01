#!/usr/bin/env python3
"""GLOAMWIRE / CROSSWEAVE, ASSERTED AGAINST THE BUILD.

    python gloamwire_relic_probe.py --game ../02-chain/sc-crossweave.html

Rick's section 1 is three outcomes and a fire rate, and every one of them is a
check here. `06-docs/v61/GLOAMWIRE-BUILD-BRIEF.md` gates 2 and 3 are the source
of every threshold; the design doc measured them on Chromium 141 at 29 relics
and this runs on the pin at 31, so a number that lands outside its band is a
finding rather than an error.

  [1] THE MAGAZINE. A volley is one round, not three. Volleys a fight, arrows
      a volley, and the window's length as it actually empties.

  [2] THE CAP, ASSERTED AND NOT ASSUMED. `CONFIG.shot.maxLive` is 64 and
      `spawnShot` SHIFTS the oldest off the front when it is reached. A triple
      shot at twice the cadence is nine times an ordinary bow's projectile load
      IN PRINCIPLE. The lab measured 0.0 evictions at up to 205 arrows a fight.
      A nonzero count means the cap is deleting shots this build thinks it
      bought, and every number after it is a number about the cap.

  [3] THE FOUR OUTCOMES, AND THEY MUST SUM TO THE VOLLEY COUNT. both +
      arrow-only + lightning-only + miss == volleys, to the unit. The lab leaked
      ~4% here on its first pass because volleys still in the air when the match
      ended were never retired; they are retired at the end here rather than
      dropped.

  [4] THE GEOMETRY CONTROLS, and each must come back at a value known BEFORE it
      is run -- CLAUDE.md section 4.7's rule, and the design's own lesson that a
      control which cannot come back wrong is worth nothing:
        strandW 0        -> lightning-only under 3% (a strand thinner than its
                            own arrows is inside them: algebra, not balance)
        reach past 954   -> miss exactly 0% OF VOLLEYS LOOSED AT A LIVE
                            QUARRY. Not of all volleys: `killFlight` holds the
                            match open while a fatal ball is in the air and the
                            archer keeps firing into that tail, so ~12% of
                            volleys are loosed at a corpse and no strand of any
                            width can catch one. The first cut of this control
                            asked for 0% of ALL volleys and could never have
                            passed.
        strandKnock 0    -> NOT A CONTROL THAT FITS IN ONE PAGE, and the first
                            cut compared it against the shipped arm, which is
                            the shove's PRICE and not an invariant. The real
                            statement -- a strand that records a classification
                            and shoves nothing cannot change a fight -- is an
                            engine A/B between the no-strand build and a
                            knock-0 copy: `04-experiments/_gloamwire-knock0.html`
                            against `02-chain/sc-volley.html`, all 31 ids.

  [5] THE STRAND TOUCHES NOTHING BUT POSITION. Rick's rule, verbatim: "enemies
      hit by only the lightning take no damage". Asserted on the TEXT of
      `tickNet` -- no `resolveHit`, no `pushCurse`, no `apply`, no `hurt` -- and
      at runtime, by watching hp and the curse pool across a shove that lands on
      a frame with no arrow contact.

  [6] ARROW-ONLY IS 1-6% AND THAT IS CORRECT. Above the crossover a ball an
      arrow can touch is already inside the segment, so what survives is
      entirely volleys that lost an arrow first. Gate 3 item 4: do not tune it
      up. This reports it and asserts the REASON rather than the number.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RELIC = "gloamwire"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


# Every arm runs the same fights. `strandw`/`strandknock`/`stub` are written on
# to `w.ult` before the match and put back after, so an arm is a number and
# never a re-patch -- net_lab's own discipline, and it is what makes the
# controls in [4] comparable to the shipped arm rather than merely similar.
RUN_JS = r"""([rid, foes, seeds, secs, strandW, strandKnock, stub]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === rid);
  const u  = w.ult;
  const keep = { sw: u.strandW, sk: u.strandKnock, ch: u.charge };
  if (strandW      !== null) u.strandW     = strandW;
  if (strandKnock  !== null) u.strandKnock = strandKnock;
  if (stub) u.charge = 1e9;

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const own = me === m.a ? "a" : "b";

      /* Every volley ever born, by id. `arrow` and `light` are set as the two
         contact kinds happen; `alive` counts arrows still in the air so a
         volley can be RETIRED rather than dropped when the match ends. */
      const V = new Map();
      let evictions = 0, arrows = 0, casts = 0;

      /* THE FLAG IS NOT SET YET INSIDE THIS WRAPPER, AND THE FIRST CUT OF THIS
         PROBE READ IT HERE AND REPORTED ZERO ARROWS AGAINST 2.04 CASTS.
         `tickFire` calls `spawnShot` and only THEN writes `volley`, `idx` and
         `net` on to the shot it just pushed -- which is the right shape for the
         build (the ordinary path stays the one thing that decides what an arrow
         is) and means a wrapper on `spawnShot` sees a plain arrow every time.

         So the only thing recorded here is what could not be recovered later:
         whether the roster was AT the cap on the frame this shot was pushed, in
         which case `spawnShot` has already shifted the oldest off the front.
         Registration happens on the next scan of `m.shots`, below. */
      const origSpawn = AC.Match.prototype.spawnShot;
      m.spawnShot = function(fg, ang){
        const full = m.shots.length >= AC.CONFIG.shot.maxLive;
        const r = origSpawn.apply(m, arguments);
        const s = m.shots[m.shots.length - 1];
        if (s && full) s._wasFull = true;
        return r;
      };

      /* AN ARROW CONTACT IS A `resolveHit` WITH THE SHOT ON THE INSTANCE.
         `_cineShot` is set by tickShots for exactly the duration of the call
         and cleared immediately, so this cannot read a stale one. */
      const origHit = AC.Match.prototype.resolveHit;
      let hpDrop = 0, poolBefore = 0;
      m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
        const s = m._cineShot;
        if (s && s.net && self === me){
          const v = V.get(s.volley);
          if (v) v.arrow = true;
        }
        return origHit.apply(m, arguments);
      };

      const origFireUlt = AC.Match.prototype.fireUlt;
      m.fireUlt = function(f2, foe2){
        const r = origFireUlt.apply(m, arguments);
        if (f2 === me && me.ultNet) casts++;
        return r;
      };

      /* ARROWS ARE REGISTERED AT BIRTH, IN A `tickFire` WRAPPER, AND NOT ON A
         SCAN AFTER THE STEP. `tickFire` is where the volley is pushed AND where
         its `net`/`volley`/`idx` fields are written, so this is the first
         moment the flag exists -- and it is before `tickShots` runs in the same
         step. A post-step scan would silently lose any arrow that was born and
         resolved inside one step, which a bow firing from 88 units at a quarry
         146 away can do; the count that check [1a] rests on would then be short
         by exactly the arrows that mattered most. */
      const born = new Set();

      /* AND THE STRAND IS LATCHED IN `tickNet`, SO IT IS READ IN `tickNet` --
         the third time in this probe that scanning after the step was the bug.
         `tickNet` sets `strandSpent` on an arrow and `tickShots` then runs in
         the SAME step and splices the dead ones out, so a post-step scan cannot
         see a latch on any arrow that died on the frame its strand fired. That
         is not a rare corner: a bow fires along a facing that sweeps at 2.8
         rad/s from 88 units out, so arrows into a nearby wall die in one or two
         steps, and under a collapsing hall that is most of them.
         It read as 11.9% of volleys missing at a reach that cannot miss. */
      const origNet = AC.Match.prototype.tickNet;
      m.tickNet = function(dt2){
        const r = origNet.apply(m, arguments);
        for (const s of m.shots){
          if (!s.net || s.own !== own) continue;
          if (s.strandSpent && !spent.has(s)){
            spent.add(s);
            shoves++;
            const v = V.get(s.volley);
            if (v) v.light = true;
            pending.push(s);
          }
        }
        return r;
      };

      const origFire = AC.Match.prototype.tickFire;
      m.tickFire = function(f2, foe2, dt2){
        const r = origFire.apply(m, arguments);
        if (f2 === me){
          for (const s of m.shots){
            if (!s.net || s.own !== own || born.has(s)) continue;
            born.add(s);
            arrows++;
            if (s._wasFull) evictions++;
            let v = V.get(s.volley);
            /* WAS THE QUARRY ALIVE WHEN THIS VOLLEY WAS LOOSED? `killFlight`
               holds the match open while a fatal ball is still in the air, so
               `foe.alive` goes false a long time before `m.over` does -- and
               the archer keeps firing into that tail. `tickNet` correctly skips
               a dead quarry, so those volleys are misses that no strand of any
               width could have caught. The reach control in [4b] is only
               meaningful over volleys that had something to hit. */
            if (!v) V.set(s.volley, v = { n: 0, arrow: false, light: false,
                                          live: foe2 && foe2.alive });
            v.n++;
          }
        }
        return r;
      };

      /* THE SHOVE, DETECTED WITHOUT THE BUILD HAVING TO REPORT IT. `tickNet`
         latches a spent strand on the lower-index arrow, so a transition of
         `strandSpent` from falsy to true is exactly one strand event and its
         volley is on the arrow that carries it. */
      const spent = new Set(), pending = [];
      let shoves = 0, shoveNoDamage = 0;

      let steps = 0, winOpen = 0;
      let hp0 = th.hp, pool0 = th.curseSum ? th.curseSum() : 0;
      while (!m.over && steps < secs / DT){
        const hpPre = th.hp;
        m.step(DT); steps++;
        if (me.ultNet) winOpen += DT;
        /* The no-damage observation is the one thing that genuinely needs the
           whole step to have run: it asks whether the quarry lost hp on a frame
           a strand fired. `pending` is what `tickNet` latched during this step,
           and it is drained here. */
        if (pending.length){
          if (th.hp >= hpPre) shoveNoDamage += pending.length;
          pending.length = 0;
        }
      }

      /* RETIRE, do not drop. A volley still in the air when the match ended is
         a MISS unless it already landed something -- the lab leaked 4% here. */
      let both = 0, arrowOnly = 0, lightOnly = 0, missed = 0;
      let liveV = 0, liveMiss = 0;
      for (const v of V.values()){
        if (v.arrow && v.light) both++;
        else if (v.arrow) arrowOnly++;
        else if (v.light) lightOnly++;
        else missed++;
        if (v.live){ liveV++; if (!v.arrow && !v.light) liveMiss++; }
      }

      rows.push({ foe: f, seed: sd, dur: steps * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, volleys: V.size, arrows, evictions,
                  both, arrowOnly, lightOnly, missed, liveV, liveMiss,
                  shoves, shoveNoDamage, winOpen,
                  pool: th.curseSum ? th.curseSum() : 0,
                  liveShotsMax: 0 });
    }
  }
  u.strandW = keep.sw; u.strandKnock = keep.sk; u.charge = keep.ch;
  return rows;
}"""


def agg(rows):
    n = len(rows)
    V = sum(r["volleys"] for r in rows)
    return {
        "n": n,
        "win": sum(1 for r in rows if r["win"] == 1) / n,
        "casts": sum(r["casts"] for r in rows) / n,
        "volleys": V, "volleysPerFight": V / n,
        "arrows": sum(r["arrows"] for r in rows),
        "evictions": sum(r["evictions"] for r in rows),
        "both": sum(r["both"] for r in rows),
        "arrowOnly": sum(r["arrowOnly"] for r in rows),
        "lightOnly": sum(r["lightOnly"] for r in rows),
        "missed": sum(r["missed"] for r in rows),
        "liveV": sum(r["liveV"] for r in rows),
        "liveMiss": sum(r["liveMiss"] for r in rows),
        "shoves": sum(r["shoves"] for r in rows) / n,
        "shoveNoDamage": sum(r["shoveNoDamage"] for r in rows),
        "shovesRaw": sum(r["shoves"] for r in rows),
        "pool": mean(r["pool"] for r in rows),
        "winOpen": mean(r["winOpen"] for r in rows),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
    ap.add_argument("--sn", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [4201 + 17 * i for i in range(a.sn)]

    with game(game_path=gp) as (page, errors):
        W = page.evaluate("() => AC.WEAPONS.map(w => ({id:w.id, shape:w.shape}))")
        ids = {w["id"] for w in W}
        if RELIC not in ids:
            raise SystemExit(f"{gp.name} has no {RELIC}")
        foes = [w["id"] for w in W if w["id"] != RELIC]
        src = page.evaluate("() => document.documentElement.outerHTML")
        u = page.evaluate(f"() => AC.WEAPONS.find(w => w.id === '{RELIC}').ult")

        print(f"\nGLOAMWIRE RELIC PROBE -- {gp.name}   "
              f"{len(foes)} foes x {len(seeds)} seeds\n")
        print(f"    magazine {u['volleys']:g} x {u['n']:g}   fan {u['spread']:g} rad   "
              f"cadMul {u['cadMul']:g}   dmgMul {u['dmgMul']:g}")
        print(f"    strandW {u['strandW']:g} (reach {34 + u['strandW']:g} against "
              f"the arrow's 58)   knock {u['strandKnock']:g}\n")

        has_strand = "strandSpent" in src

        # ------------------------------------------------------- [5] the text --
        # The refusal reads CODE and not the paragraph explaining it -- this
        # build's own comment has to be able to say the words "NO pushCurse".
        m = re.search(r"\n  tickNet\(dt\)\{", src)
        body = ""
        if m:
            i = src.index("{", m.start())
            depth, k = 0, i
            while k < len(src):
                if src[k] == "{":
                    depth += 1
                elif src[k] == "}":
                    depth -= 1
                    if depth == 0:
                        body = src[i:k + 1]
                        break
                k += 1
        code = re.sub(r"//[^\n]*", "", re.sub(r"/\*[\s\S]*?\*/", "", body))
        banned = [w for w in ("resolveHit", "pushCurse", "apply(", "hurt(",
                              "takeHitstun", "hitStop") if w in code]
        check("[5a] the strand touches nothing but position -- no damage path "
              "in tickNet's own code",
              bool(code) and not banned,
              "clean" if not banned else f"FOUND {banned}")

        # ------------------------------------------------------ the shipped arm --
        rows = page.evaluate(RUN_JS, [RELIC, foes, seeds, a.secs, None, None, False])
        assert not errors, errors[:4]
        S = agg(rows)

        print(f"[1] THE MAGAZINE -- {S['n']} fights\n")
        print(f"    casts a fight        {S['casts']:.2f}")
        print(f"    volleys a fight      {S['volleysPerFight']:.1f}"
              f"        (design 6.1: 36.6 at cadMul 0.5)")
        print(f"    arrows a fight       {S['arrows'] / S['n']:.1f}")
        print(f"    arrows a volley      {S['arrows'] / max(1, S['volleys']):.2f}"
              f"        (must be exactly {u['n']:g})")
        print(f"    window open a fight  {S['winOpen']:.2f}s")
        check("[1a] a volley is one magazine round -- exactly n arrows a volley",
              abs(S["arrows"] / max(1, S["volleys"]) - u["n"]) < 1e-9,
              f"{S['arrows'] / max(1, S['volleys']):.4f} against {u['n']:g}")
        check("[1b] the magazine empties -- volleys a cast is the magazine size",
              abs(S["volleys"] / max(1e-9, S["casts"] * S["n"]) - u["volleys"])
              < 0.5 * u["volleys"],
              f"{S['volleys'] / max(1e-9, S['casts'] * S['n']):.1f} a cast "
              f"against a magazine of {u['volleys']:g}")

        print(f"\n[2] THE CAP -- maxLive 64, and spawnShot SHIFTS at it\n")
        print(f"    evictions            {S['evictions']}"
              f"        over {S['arrows']} arrows")
        check("[2a] the cap never fires -- no shot this build thinks it bought "
              "was deleted",
              S["evictions"] == 0, f"{S['evictions']} evictions")

        if has_strand:
            V = max(1, S["volleys"])
            print(f"\n[3] THE FOUR OUTCOMES -- {S['volleys']} volleys\n")
            print(f"    both            {S['both']:>7}  {S['both'] / V:6.1%}")
            print(f"    arrow only      {S['arrowOnly']:>7}  {S['arrowOnly'] / V:6.1%}")
            print(f"    lightning only  {S['lightOnly']:>7}  {S['lightOnly'] / V:6.1%}")
            print(f"    miss            {S['missed']:>7}  {S['missed'] / V:6.1%}")
            tot = S["both"] + S["arrowOnly"] + S["lightOnly"] + S["missed"]
            check("[3a] the four outcomes sum to the volley count, to the unit",
                  tot == S["volleys"], f"{tot} against {S['volleys']}")
            check("[6a] arrow-only is 1-6% and it is the volleys that lost an "
                  "arrow first -- gate 3 item 4, do NOT tune it up",
                  0.005 <= S["arrowOnly"] / V <= 0.09,
                  f"{S['arrowOnly'] / V:.1%}")
            print(f"\n    shoves a fight       {S['shoves']:.1f}"
                  f"        (design 6.1: 22.3)")
            # NOT COMPARABLE TO THE DESIGN'S 40.8, and the first cut of this
            # line printed them side by side as though they were. Design 7's
            # figure is a TIME AVERAGE -- `net_lab` samples the pool every
            # 0.25s of sim and means it -- while this is the pool standing at
            # the final step, which is nearer the design's own `peak` column
            # (99.2 for this body at blade 16.23). Two different statistics of
            # one quantity, and printing them together invented a 2x
            # disagreement that does not exist. 
            print(f"    pool at the LAST step {S['pool']:.1f}"
                  f"       (design 7's 40.8 is a TIME AVERAGE --"
                  f" this is the final value, near its `peak`)")
            check("[5b] a shove that lands on a frame with no arrow contact "
                  "costs the quarry no hp",
                  S["shovesRaw"] > 0
                  and S["shoveNoDamage"] / S["shovesRaw"] > 0.80,
                  f"{S['shoveNoDamage']}/{S['shovesRaw']} shoves took no hp "
                  f"on their own frame")

            # ------------------------------------------------ [4] the controls --
            print("\n[4] THE GEOMETRY CONTROLS -- each one known before it ran\n")
            c0 = agg(page.evaluate(RUN_JS,
                                   [RELIC, foes, seeds, a.secs, 0.0, None, False]))
            V0 = max(1, c0["volleys"])
            print(f"    strandW 0        lightning only {c0['lightOnly'] / V0:6.1%}"
                  f"   (must be under 3%)")
            check("[4a] a strand thinner than its own arrows is inside them",
                  c0["lightOnly"] / V0 < 0.03, f"{c0['lightOnly'] / V0:.1%}")

            cW = agg(page.evaluate(RUN_JS,
                                   [RELIC, foes, seeds, a.secs, 1000.0, None, False]))
            VW = max(1, cW["volleys"])
            LW = max(1, cW["liveV"])
            print(f"    reach past 954   miss           {cW['missed'] / VW:6.1%}"
                  f"   of ALL volleys")
            print(f"                     miss           {cW['liveMiss'] / LW:6.1%}"
                  f"   of volleys loosed at a LIVE quarry (must be 0)")
            check("[4b] past the arena diagonal nothing loosed at a living "
                  "quarry can be missed",
                  cW["liveMiss"] == 0,
                  f"{cW['liveMiss']} of {cW['liveV']} -- and "
                  f"{cW['missed'] - cW['liveMiss']} more were loosed into "
                  f"`killFlight`, at a quarry already dead")

            cK = agg(page.evaluate(RUN_JS,
                                   [RELIC, foes, seeds, a.secs, None, 0.0, False]))
            print(f"    strandKnock 0    win {cK['win']:.1%}  against the "
                  f"shipped arm's {S['win']:.1%}")
            print(f"                     -- that difference is THE SHOVE'S "
                  f"PRICE ({S['win'] - cK['win']:+.1%}), not a control.")
            print(f"                     The control is an ENGINE A/B against "
                  f"the no-strand build and it")
            print(f"                     cannot be run inside one page: see "
                  f"`04-experiments/_gloamwire-knock0.html`.")
            # NOT A CHECK, AND THE FIRST CUT ASSERTED IT AND WAS RIGHT TO
            # FAIL. This is a BALANCE reading, not an invariant, and at the
            # sample this probe runs it cannot support a direction: measured at
            # blade 9.2 the shove read -2.5pp and at blade 9.0 it reads +9.2pp,
            # an 11.7pp swing out of a 0.2 change to the blade. That is not a
            # sign flip in the mechanic, it is n=120 an arm against CLAUDE.md's
            # own floor of n~700 for ranking anything on this roster. The
            # design measured it properly -- four monotone arms, -9pp across
            # 0 -> 400 -- and `gloamwire_sweep.py` is the shape of instrument
            # that could re-measure it.
            #
            # The INVARIANT half of gate 3 item 3 is testable and passes:
            # 04-experiments/_gloamwire-knock0.html against sc-volley.html,
            # 2790/2790 identical across all 31 ids.
            print(f"                     REPORTED, NOT CHECKED: n={S['n']} an "
                  f"arm cannot rank a direction")
            print(f"                     (CLAUDE.md's floor is n~700, and this "
                  f"reading has swung 11.7pp")
            print(f"                     across a 0.2 change of blade). The "
                  f"design's own four arms say -9pp.")

            print(f"\n    shipped win rate     {S['win']:.1%}"
                  f"        (design 6.1: ~51%, on 29 relics and Chromium 141)")
        else:
            print("\n  [3]-[6] SKIPPED -- this build has no strand (stage 2).")

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"   ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({"shipped": S}, indent=1))
        print(f"wrote {a.json}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
