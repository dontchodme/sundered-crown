#!/usr/bin/env python3
"""SOLVE THE WINNOWING. The blade first, then the thing the pair is actually
choosing: HOW MUCH OF THIS RELIC IS THE GROWTH.

    python thornshear_sweep.py --game ../02-chain/sc-thornshear.html

THE FRAMING, AND IT IS THE POINT OF THIS FILE. `dmg` is bisected in every
cell, so no arm here is stronger than another -- the bisection compensates.
What the arms choose is not how hard this relic hits. It is WHAT SHARE OF A
CAST'S DAMAGE IS CARRIED BY KUNAI THAT HAVE GROWN, against the share carried
by fresh ones. That is the number to put to Rick; a win rate would be the
bisection's own output read back as a finding.

    [1] THE BASELINE, so every share below has something to be a share of:
        the relic with the window suppressed (`charge` 1e9).
    [2] THE BLADE, bisected against all 25 opponents, WITH AN ESCALATING
        SAMPLE -- v43 §14.1's cheap win, unclaimed for four sessions. Step
        one spends 50 fights on an interval twelve damage wide; step seven
        spends 750 on an interval of 0.1, which is the one that matters.
        Same precision, a third of the fights.
    [3] THE GROWTH SCHEDULE. `growDmg` against `life`, dmg re-bisected per
        cell, reported as the share of the cast carried by each rung.
    [4] bounce x life. `bounce` above 3 is INERT at life 3.0 -- measured,
        digit for digit -- so this is really one knob, and it is a PICTURE
        decision as much as a balance one: kunai visibly stay in the hall
        longer.

WHAT IS DELIBERATELY NOT SWEPT: the fan and the spread. `kunai_probe [4]`
flew fan 1, 3, 5 and 9 and every one landed within x1.13 of every other,
because the coverage comes from the weapon's own 6.47 rad/s. They are LOOK
KNOBS and they are Rick's, off a render -- but they are not free, and the
constraint is arithmetic rather than balance: `fan x 2 x life / cadence` is
the steady-state population and `CONFIG.shot.maxLive` is 64, SHARED with the
foe's own arrows. Rick is choosing along `fan / cadence ~= 8.3`.

INJECTION IS RUNTIME-ONLY. Nothing is written to any build; the chosen numbers
go back into `thornshear_build.py`'s ULT dict by hand, which is the only place
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

RID = "thornshear"


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


# THE TELEMETRY. Damage split BY RUNG, which is the only split that answers
# the question this sweep exists to ask.
TEL_JS = r"""([id, dmg, ult, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = JSON.parse(JSON.stringify(w.ult));
  w.dmg = dmg;
  for (const k of Object.keys(ult)) w.ult[k] = ult[k];

  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m  = new AC.Match(id, f, sd);
      const me = m.a.w.id === id ? m.a : m.b;

      /* SPLIT AT THE SOURCE. `_cineShot` is the projectile the engine hands
         resolveHit for the duration of the call, so a kunai's damage is
         attributable exactly and a blade's is what is left. */
      const byRung = [0, 0, 0, 0, 0, 0];
      const nRung  = [0, 0, 0, 0, 0, 0];
      let blade = 0, kunai = 0, taken = 0;
      const oRes = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
        const cs = m._cineShot, before = f2.hp;
        const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
        const dd = before - f2.hp;
        if (self === me && !f2.shade){
          if (cs && cs.kunai){
            kunai += dd;
            byRung[Math.min(5, cs.rung)] += dd;
            nRung[Math.min(5, cs.rung)]++;
          } else blade += dd;
        } else if (f2 === me) taken += dd;
        return r;
      };

      let steps = 0, casts = 0, up = 0, wasUp = false, refused = 0, loosed = 0;
      let peak = 0;
      while (!m.over && steps < secs / DT){
        m.step(DT); steps++;
        const W = me.ultWinnow;
        if (W){ up++; if (!wasUp) casts++; refused = W.refused; }
        if (W) loosed = Math.max(loosed, W.loosed);
        wasUp = !!W;
        if (m.shots.length > peak) peak = m.shots.length;
      }
      rows.push({ foe: f, seed: sd, dur: steps * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  casts, up, blade, kunai, taken, byRung, nRung,
                  refused, peak });
    }
  }
  w.dmg = d0;
  for (const k of Object.keys(w.ult)) delete w.ult[k];
  for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  return rows;
}"""


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


def bisect(page, ult, lo, hi, target=0.50, steps=7, base=2, top=12, seed0=7,
           label=""):
    """THE ESCALATING BISECTION. v43 §14.1, and the reason it is here.

    A bisection spends the same number of fights on step one -- where the
    interval is twelve damage wide and the answer is obvious -- as on step
    seven, where it is 0.1 and the answer is the point. The sample rises
    geometrically with the step, so the early calls are cheap and the last
    one is the widest sample in the run.
    """
    t0 = time.time()
    fights = 0
    hist = []
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
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--lo", type=float, default=4.0)
    ap.add_argument("--hi", type=float, default=16.0)
    ap.add_argument("--steps", type=int, default=7)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--only", default="", help="1,2,3,4 — which sections")
    A = ap.parse_args()
    want = set(A.only.split(",")) if A.only else {"1", "2", "3", "4"}
    path = resolve_game(A.game)
    seeds = [4000 + i * 811 for i in range(A.seeds)]
    FOES = ["emberedge", "ironhail", "lastlight", "gravemourn", "grudgebearer",
            "spellbreaker", "heartwood", "farwarden"]
    spent = 0

    print(f"\nTHE WINNOWING — the sweep, against {path.name}")

    with game(game_path=path) as (page, errors):
        u0 = page.evaluate("([id]) => JSON.parse(JSON.stringify("
                           "AC.WEAPONS.find(x => x.id === id).ult))", [RID])
        d0 = page.evaluate("([id]) => AC.WEAPONS.find(x => x.id === id).dmg",
                           [RID])
        print(f"  shipping placeholders: dmg {d0:g}  " +
              "  ".join(f"{k} {v:g}" for k, v in u0.items()
                        if isinstance(v, (int, float))))

        # ------------------------------------------------------------ [1] --
        if "1" in want:
            print("\n[1] THE BASELINE — the blade alone, with the window "
                  "suppressed\n")
            off = {"charge": 1e9}
            d_off, n = bisect(page, off, A.lo, A.hi, steps=A.steps, top=A.top,
                              label="no ultimate  ")
            spent += n
            r = page.evaluate(TEL_JS, [RID, d_off, off, FOES, seeds, A.secs])
            print(f"    at dmg {d_off:.2f} with no window: "
                  f"{mean(x['blade'] for x in r):.0f} damage a fight from the "
                  f"blades, {mean(x['dur'] for x in r):.1f}s mean")
            print("\n    THE ULTIMATE HAS TO PAY FOR ITSELF TWICE OVER: "
                  "`kunai_probe [1]` measured\n    the bill at 4.46 dmg/s — "
                  "2.76 of output it stops dealing plus 1.70 of\n    damage it "
                  "starts taking, because a bind this type LOSES still costs "
                  "the\n    foe a swing.")

        # ------------------------------------------------------------ [2] --
        if "2" in want:
            print("\n[2] THE BLADE, at the shipping ultimate — bisected "
                  "against all 25\n")
            d_on, n = bisect(page, {}, A.lo, A.hi, steps=A.steps, top=A.top,
                             label="shipping     ")
            spent += n
            rows = page.evaluate(TEL_JS, [RID, d_on, {}, FOES, seeds, A.secs])
            share(rows, u0, f"at dmg {d_on:.2f}")
            # THE CEILING, IN THE SWEEP AS WELL AS IN THE PROBE. A design that
            # saturates is a design whose cadence is CONFIG's.
            ref = sum(x["refused"] for x in rows)
            pk = max(x["peak"] for x in rows)
            print(f"    ceiling: {ref} volleys refused, peak {pk} in flight")

        # ------------------------------------------------------------ [3] --
        if "3" in want:
            print("\n[3] THE GROWTH SCHEDULE — and this is the arm that is "
                  "actually being chosen\n")
            for gd in (1.0, 1.25, 1.5, 1.85):
                arm = {"growDmg": gd}
                d, n = bisect(page, arm, A.lo, A.hi, steps=A.steps,
                              top=A.top, label=f"growDmg {gd:<4g} ")
                spent += n
                rows = page.evaluate(TEL_JS, [RID, d, arm, FOES, seeds, A.secs])
                share(rows, dict(u0, growDmg=gd), f"growDmg {gd:g}, dmg {d:.2f}")

        # ------------------------------------------------------------ [4] --
        if "4" in want:
            print("\n[4] bounce x life — the three-rung ceiling, and whether "
                  "it should be four\n")
            for bo, lf in ((3, 3.0), (4, 4.5), (6, 6.0)):
                arm = {"bounce": bo, "life": lf}
                d, n = bisect(page, arm, A.lo, A.hi, steps=A.steps,
                              top=A.top, label=f"bounce {bo} life {lf:<4g} ")
                spent += n
                rows = page.evaluate(TEL_JS, [RID, d, arm, FOES, seeds, A.secs])
                share(rows, dict(u0, bounce=bo, life=lf),
                      f"bounce {bo} life {lf:g}, dmg {d:.2f}")
                print(f"    ceiling: {sum(x['refused'] for x in rows)} volleys "
                      f"refused, peak {max(x['peak'] for x in rows)} in flight "
                      f"— fan x 2 x life / cadence = "
                      f"{u0['fan'] * 2 * lf / u0['cadence']:.0f}")

        if errors:
            print("\n  ! page errors:", errors[:3])

    print(f"\n{spent} fights in the bisections, plus the telemetry passes.")
    print("The chosen numbers go into thornshear_build.py's ULT dict BY HAND. "
          "A tuned\nnumber written into the HTML is lost on the next rebuild "
          "(CLAUDE.md §4.9).")
    return 0


def share(rows, u, label):
    """WHAT SHARE OF A CAST IS THE GROWTH. The framing, printed."""
    k = mean(x["kunai"] for x in rows)
    b = mean(x["blade"] for x in rows)
    casts = mean(x["casts"] for x in rows)
    tot = max(1e-9, k + b)
    rung = [mean(x["byRung"][i] for x in rows) for i in range(5)]
    nr = [mean(x["nRung"][i] for x in rows) for i in range(5)]
    grown = sum(rung[1:])
    print(f"    {label}:  {mean(x['dur'] for x in rows):.1f}s, {casts:.1f} "
          f"casts, {100 * k / tot:.0f}% of damage from kunai "
          f"({k / max(0.01, casts):.0f} a cast)")
    print(f"      {'rung':>6}{'hits':>8}{'damage':>9}{'of the ult':>12}"
          f"{'of the fight':>14}")
    for i in range(5):
        if nr[i] < 0.05 and rung[i] < 0.05: continue
        print(f"      {i:>6}{nr[i]:>8.1f}{rung[i]:>9.1f}"
              f"{100 * rung[i] / max(1e-9, k):>11.0f}%"
              f"{100 * rung[i] / tot:>13.0f}%")
    print(f"      GROWN KUNAI CARRY {100 * grown / max(1e-9, k):.0f}% OF THE "
          f"ULTIMATE and {100 * grown / tot:.0f}% of the fight")


if __name__ == "__main__":
    sys.exit(main())
