#!/usr/bin/env python3
"""SOLVE SENTINEL. The blade first, then the thing the grid is actually
choosing: HOW MUCH OF THIS ULTIMATE IS THE TIP.

    python vesper_sweep.py --game ../02-chain/sc-vesper.html

THE FRAMING, AND IT IS THE POINT OF THIS FILE. `dmg` is bisected in every
cell, so no arm here is stronger than another -- the bisection compensates.
What the arms choose is not how hard this relic hits. It is WHAT SHARE OF A
CAST'S DAMAGE ARRIVES AT THE FAR END, against the share that arrives anywhere
along the shaft. A short beam that mostly pays at the tip, against a long one
that mostly pays in the middle. That is the number to put to Rick; a win rate
would be the bisection's own output read back as a finding, which is v43's
mistake and this project has now made it once.

    [1] THE BASELINE, so every share below has something to be a share of:
        the relic with the window suppressed (`charge` 1e9).
    [2] THE BLADE, bisected against all 26 opponents, WITH AN ESCALATING
        SAMPLE -- v43 §14.1's cheap win. Step one spends 52 fights on an
        interval sixteen damage wide; the last spends 312 on an interval of
        0.13, which is the one that matters. Same precision, a third of the
        fights.
    [3] range x tipMul. THE MAIN AXIS, and the one clean trade in the design
        (`beam_probe [4]`): range 180 -> 2.8 passes with 73% reaching the tip,
        300 -> 3.5 at 60%, 420 -> 3.8 at 45%. `dmg` re-bisected per cell, and
        reported as the share of the cast paid at the far end.
    [4] drink x dur. Whether the beam is self-sustaining. The measured ward
        income is ~2.0 points a second, so a drink under that is a beam that
        runs to `durCap` every cast and makes `dur` unreadable -- which is a
        thing to SEE in a table rather than to argue about.
    [5] half x turn. Thickness is the knob that buys contact where the turn
        rate must not, and `half` may not go below ballR/2 -- §1's own floor,
        which the builder refuses to write under.

WHAT IS DELIBERATELY NOT SWEPT: THE PUSH. `beam_probe [3]` moved the quarry
from 0.56 to 0.59 of the way down the beam at six times the force, because you
cannot push a thing along a line for 0.3 seconds. It is not in the build (see
`vesper_build.py`), so there is nothing here to sweep, and putting an axis on
a knob measured inert is how a project ends up with three of them.

INJECTION IS RUNTIME-ONLY. Nothing is written to any build; the chosen numbers
go back into `vesper_build.py`'s ULT dict by hand, which is the only place
this project keeps a tuned number (CLAUDE.md §4.9).
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "vesper"


# THE WIN RATE, over the WHOLE field. v41 open decision 2, closed the
# expensive way: Bulwarden's dmg was bisected on a five-foe subset that read
# 50% and the full 23-opponent field read 55.2% on the same number.
WIN_JS = r"""([id, dmg, ult, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0, timeouts = 0;
  const byFoe = {};
  for (const foe of ids){
    let fw = 0;
    for (let k = 0; k < n; k++){
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const r = AC.simulate(id, foe, s);
      if (r.winner === w.name){ win++; fw++; }
      games++; dur += r.duration;
      if (r.reason !== "slain") timeouts++;
    }
    byFoe[foe] = fw / n;
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return { win, games, rate: win / games, dur: dur / games, timeouts, byFoe };
}"""


# THE TELEMETRY, AND THE SPLIT IS THE WHOLE POINT: damage paid at the far end
# against damage paid anywhere else, plus what the BLADE did in the same
# fights. `beamHit` is wrapped rather than reimplemented, and it forwards with
# `arguments` -- v44's warning is that a wrapper with a fixed arity silently
# measures the old build the moment the build grows a parameter.
TEL_JS = r"""([id, dmg, ult, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];

  const P = AC.Match.prototype;
  let casts = 0, released = 0, broken = 0;
  let passes = 0, tips = 0, dTip = 0, dPass = 0, dBlade = 0;
  let windowT = [], drunk = 0, capped = 0, beamSecs = 0;

  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(id, foeId, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;

      const origHit = P.beamHit;
      m.beamHit = function(f, foe, g, mul, tip){
        const before = foe.hp;
        const r = origHit.apply(m, arguments);
        if (f === me){
          const paid = before - foe.hp;
          if (tip){ tips++; dTip += paid; } else { passes++; dPass += paid; }
        }
        return r;
      };
      /* THE BLADE, in the same fights, so the share has a denominator that is
         not a second experiment. `mul === undefined` is this engine's own
         test for "an ordinary melee blow" and it is what `resolveHit`'s
         banking gate uses. */
      const origRes = P.resolveHit;
      m.resolveHit = function(self, foe, hx, hy, seg, mul, over){
        const before = foe.hp;
        const r = origRes.apply(m, arguments);
        if (self === me && mul === undefined) dBlade += before - foe.hp;
        return r;
      };
      const origDrink = P.drinkWard;
      m.drinkWard = function(f, want){
        const got = origDrink.apply(m, arguments);
        if (f === me) drunk += got;
        return got;
      };

      let step = 0;
      while (!m.over && step < secs / DT){
        const B0 = me.ultBeam, p0 = B0 ? B0.phase : null;
        m.step(DT); step++;
        const B = me.ultBeam, p = B ? B.phase : null;
        if (p === "wind" && p0 !== "wind") casts++;
        if (p === "beam" && p0 === "wind") released++;
        if (p === "beam") beamSecs += DT;
        if (p0 === "beam" && p !== "beam"){
          windowT.push(B0.t);
          if (B0.dur >= w.ult.durCap - 1e-9) capped++;
        }
      }
      if (me.ultBeam && me.ultBeam.phase === "beam"){
        windowT.push(me.ultBeam.t);
        if (me.ultBeam.dur >= w.ult.durCap - 1e-9) capped++;
      }
      /* a wind-up that never released was taken off it */
      broken += 0;
    }
  }

  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];

  const mean = a => a.length ? a.reduce((s, v) => s + v, 0) / a.length : 0;
  const ult2 = dTip + dPass;
  return { casts, released, passes, tips,
           dTip, dPass, dBlade, ultShare: ult2 / Math.max(1e-9, ult2 + dBlade),
           tipShare: dTip / Math.max(1e-9, ult2),
           tipRate: tips / Math.max(1, passes),
           passesPerWindow: passes / Math.max(1, released),
           meanWindow: mean(windowT), capped, drunk, beamSecs,
           windows: windowT.length };
}"""


def bisect(page, ult, lo, hi, target=0.50, steps=7, base=2, top=12, seed0=7,
           label=""):
    """THE ESCALATING BISECTION. v43 §14.1, unclaimed through v47.

    A bisection spends the same number of fights on step one -- where the
    interval is sixteen damage wide and the answer is obvious -- as on step
    seven, where it is 0.13 and the answer is the point. The sample rises
    geometrically with the step, so the early calls are cheap and the last one
    is the widest sample in the run.
    """
    t0 = time.time()
    fights, hist = 0, []
    for i in range(steps):
        n = max(base, round(base * (top / base) ** (i / max(1, steps - 1))))
        mid = (lo + hi) / 2
        r = page.evaluate(WIN_JS, [RID, mid, ult, n, seed0 + i])
        fights += r["games"]
        hist.append((mid, r["rate"], r["games"], r["dur"]))
        if r["rate"] < target: lo = mid
        else: hi = mid
    out = (lo + hi) / 2
    print(f"    {label}bisect -> dmg {out:.2f}   "
          f"{fights} fights, {time.time() - t0:.0f}s")
    for d, rate, g, dur in hist:
        print(f"      {d:>7.2f}  {rate * 100:>5.1f}%  n={g:<5} mean {dur:.1f}s")
    return out, fights


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vesper.html")
    ap.add_argument("--lo", type=float, default=12.0)
    ap.add_argument("--hi", type=float, default=34.0)
    ap.add_argument("--steps", type=int, default=7)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--only", default="", help="1,2,3,4,5 — which sections")
    A = ap.parse_args()
    want = set(A.only.split(",")) if A.only else {"1", "2", "3"}
    path = resolve_game(A.game)
    seeds = [4000 + i * 811 for i in range(A.seeds)]
    # EIGHT FOES, ONE OF EVERY TYPE plus the two the ward is worth most and
    # least against (row_price: +34.0% against ranged, +2.9% against swing).
    FOES = ["emberedge", "ironhail", "lastlight", "gravemourn", "censer",
            "widowmaker", "thornshear", "farwarden"]
    spent = 0

    print(f"\nSENTINEL — the sweep, against {path.name}")

    with game(game_path=path) as (page, errors):
        u0 = page.evaluate("([id]) => JSON.parse(JSON.stringify("
                           "AC.WEAPONS.find(x => x.id === id).ult))", [RID])
        d0 = page.evaluate("([id]) => AC.WEAPONS.find(x => x.id === id).dmg",
                           [RID])
        print(f"  ships dmg {d0:g}   " + "  ".join(
            f"{k} {v:g}" for k, v in u0.items() if isinstance(v, (int, float))))

        # ------------------------------------------------------------ [1] --
        if "1" in want:
            print("\n[1] THE BASELINE — the relic with no window at all")
            off = dict(u0, charge=1e9)
            db, f = bisect(page, off, A.lo, A.hi, steps=A.steps, top=A.top,
                           label="no ult  ")
            spent += f
            t = page.evaluate(TEL_JS, [RID, db, off, FOES, seeds, A.secs])
            print(f"    blade alone: {t['dBlade']:.0f} damage over "
                  f"{len(FOES) * len(seeds)} fights, {t['casts']} casts")
            print(f"    SO THE BLADE ALONE IS WORTH dmg {db:.2f} at a 50% "
                  f"field win rate; everything below is what the window buys "
                  f"on top of that.")

        # ------------------------------------------------------------ [2] --
        if "2" in want:
            print("\n[2] THE BLADE, at the shipped ultimate — all 26 "
                  "opponents, escalating sample")
            dmg, f = bisect(page, u0, A.lo, A.hi, steps=A.steps, top=A.top,
                            label="shipped ")
            spent += f
            r = page.evaluate(WIN_JS, [RID, dmg, u0, A.top, 991])
            lo_ = min(r["byFoe"].items(), key=lambda kv: kv[1])
            hi_ = max(r["byFoe"].items(), key=lambda kv: kv[1])
            spent += r["games"]
            print(f"    at dmg {dmg:.2f}: {r['rate'] * 100:.1f}% over "
                  f"{r['games']} fights, mean {r['dur']:.1f}s, "
                  f"{r['timeouts']} timeouts")
            print(f"    worst matchup {lo_[0]} {lo_[1] * 100:.0f}%   "
                  f"best {hi_[0]} {hi_[1] * 100:.0f}%")
            print(f"    THE TYPE SHIPS 17.50 (Lastlight) .. 31.35 "
                  f"(Thornwake); this lands at {dmg:.2f}.")

        # ------------------------------------------------------------ [3] --
        if "3" in want:
            print("\n[3] range x tipMul — THE MAIN AXIS, and what it chooses "
                  "is the SHARE OF THE CAST PAID AT THE FAR END")
            print(f"    {'range':>6} {'tipMul':>7} {'dmg':>7} {'pass/win':>9} "
                  f"{'tip rate':>9} {'TIP SHARE':>10} {'ult share':>10} "
                  f"{'window':>8}")
            for rng in (180.0, 300.0, 420.0):
                for tm in (1.4, 1.8, 2.6):
                    ult = dict(u0, range=rng, tipMul=tm)
                    d, f = bisect(page, ult, A.lo, A.hi, steps=A.steps,
                                  top=A.top, seed0=13,
                                  label=f"r{rng:g} t{tm:g}  ")
                    spent += f
                    t = page.evaluate(TEL_JS, [RID, d, ult, FOES, seeds,
                                               A.secs])
                    print(f"    {rng:>6g} {tm:>7g} {d:>7.2f} "
                          f"{t['passesPerWindow']:>9.1f} "
                          f"{t['tipRate'] * 100:>8.0f}% "
                          f"{t['tipShare'] * 100:>9.0f}% "
                          f"{t['ultShare'] * 100:>9.0f}% "
                          f"{t['meanWindow']:>7.2f}s")
            print("\n    THE QUESTION FOR RICK IS THE 'TIP SHARE' COLUMN, not")
            print("    a win rate: the bisection compensates, so every row "
                  "above wins")
            print("    the same. A SHORT BEAM THAT MOSTLY PAYS AT THE FAR END "
                  "against")
            print("    A LONG ONE THAT MOSTLY PAYS IN THE MIDDLE.")

        # ------------------------------------------------------------ [4] --
        if "4" in want:
            print("\n[4] drink x dur — is the beam self-sustaining?")
            print(f"    {'drink':>6} {'dur':>5} {'dmg':>7} {'window':>8} "
                  f"{'capped':>7} {'drunk/win':>10} {'ult share':>10}")
            for dr in (2.0, 6.0, 14.0):
                for du in (3.0, 4.0, 6.0):
                    ult = dict(u0, drink=dr, dur=du)
                    d, f = bisect(page, ult, A.lo, A.hi, steps=A.steps,
                                  top=A.top, seed0=29,
                                  label=f"k{dr:g} d{du:g}  ")
                    spent += f
                    t = page.evaluate(TEL_JS, [RID, d, ult, FOES, seeds,
                                               A.secs])
                    print(f"    {dr:>6g} {du:>5g} {d:>7.2f} "
                          f"{t['meanWindow']:>7.2f}s "
                          f"{t['capped']:>3}/{t['windows']:<3} "
                          f"{t['drunk'] / max(1, t['windows']):>9.1f} "
                          f"{t['ultShare'] * 100:>9.0f}%")
            print("\n    THE MEASURED WARD INCOME IS ~2.0 POINTS A SECOND, so "
                  "a drink at or")
            print("    under that is a beam fed faster than it burns — it "
                  "runs to durCap")
            print("    every cast and `dur` stops being a knob at all. The "
                  "'capped' column")
            print("    is where to read that, not the win rate.")

        # ------------------------------------------------------------ [5] --
        if "5" in want:
            print("\n[5] half x turn — thickness buys contact where the turn "
                  "rate must not")
            print(f"    {'half':>5} {'turn':>5} {'dmg':>7} {'pass/win':>9} "
                  f"{'mean pass':>10} {'tip rate':>9} {'TIP SHARE':>10}")
            for h in (17.0, 22.0, 30.0):
                for tn in (0.8, 1.6, 3.2):
                    ult = dict(u0, half=h, turn=tn)
                    d, f = bisect(page, ult, A.lo, A.hi, steps=A.steps,
                                  top=A.top, seed0=41,
                                  label=f"h{h:g} n{tn:g}  ")
                    spent += f
                    t = page.evaluate(TEL_JS, [RID, d, ult, FOES, seeds,
                                               A.secs])
                    print(f"    {h:>5g} {tn:>5g} {d:>7.2f} "
                          f"{t['passesPerWindow']:>9.1f} "
                          f"{t['beamSecs'] / max(1, t['passes']):>9.2f}s "
                          f"{t['tipRate'] * 100:>8.0f}% "
                          f"{t['tipShare'] * 100:>9.0f}%")
            print("\n    `half` MAY NOT GO BELOW 17. §1 asks for a beam at "
                  "least half the")
            print("    thickness of an artifact, an artifact is 68 across, "
                  "and the builder")
            print("    refuses to write under it. 17 is the floor the "
                  "sentence sets.")
            print("    TURN IS RICK'S AND IS NOT UP FOR RE-DECIDING HERE — it "
                  "is in this")
            print("    table so the cost of his choice is visible, not so it "
                  "can be undone.")

        if errors:
            print(f"\n  !! {len(errors)} page error(s): {errors[0][:200]}")

    print(f"\n  {spent} fights spent.")
    print("  The chosen numbers go into vesper_build.py's ULT dict BY HAND — "
          "CLAUDE.md §4.9.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
