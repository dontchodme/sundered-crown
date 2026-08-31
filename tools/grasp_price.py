#!/usr/bin/env python3
"""FOUR WAYS TO WEAKEN GRASP, PRICED AT A RESTORED BLADE.

    python grasp_price.py --game ../02-chain/sc-gravemourn.html --blade 39.79

Rick, on stage 2b's answer (blade 44.10 -> 39.79 -> 24.03 to hold 50%):

    "bring back the blade and lets do a weaker grasp"

He chose the DIRECTION. The knob is a second decision and it is not
interchangeable, because the four levers take the ultimate apart in four
different places:

    dur       THE SET-PIECE'S LENGTH. Fewer seconds means fewer blows inside
              the window, so fewer hands -- it makes the ultimate SHORTER, and
              a shorter set-piece is less to watch as well as less to survive.
    reachMul  THE CHAIN. `hand_lab` priced this as 75% of the whole ultimate's
              value and showed it is DEFENSIVE -- the foe lands 10% fewer
              blows. Cutting it removes the half of §1 that reads as staging
              and is actually the half that wins.
    handMul   WHAT A HAND HITS FOR. The one lever that leaves the picture
              completely intact: the same number of hands fly the same arcs
              and land the same fists, they just take less. Clamped at 1.0
              from above (compounding, §4.2); nothing stops it going down.
    charge    HOW OFTEN IT HAPPENS AT ALL. The brief says charge is NOT a
              balance lever here -- at 42 it fires in a quarter of fights and
              the relic still wins 61.5% -- so it is carried to be RULED OUT
              with a number rather than left as a claim.

THE POINT OF THE TABLE IS THAT SEVERAL OF THESE REACH 50% AND THEY ARE NOT THE
SAME RELIC AFTERWARDS. `handMul` keeps every frame of the set-piece and makes
it cosmetic; `dur` and `reachMul` make it genuinely smaller. That is Rick's
call and this tool exists so it is made on numbers rather than on feel.

Runtime injection only. Nothing is written to any build.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "gravemourn"

# Each arm is (knob, value). `None` is the control -- the shipped ultimate at
# the restored blade, which is the number the weakening has to move.
ARMS = [
    ("control", None),
    ("dur", 6.0), ("dur", 4.5), ("dur", 3.0), ("dur", 2.0),
    ("reachMul", 1.25), ("reachMul", 1.15), ("reachMul", 1.05), ("reachMul", 1.0),
    ("handMul", 0.70), ("handMul", 0.50), ("handMul", 0.30), ("handMul", 0.10),
    ("charge", 24), ("charge", 32), ("charge", 42),
]


WIN_JS = r"""([id, blade, knob, val, n, seed0]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, u0 = {};
  for (const k of Object.keys(w.ult)) u0[k] = w.ult[k];
  w.dmg = blade;
  if (knob) w.ult[knob] = val;
  const ids = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let s = seed0 >>> 0, win = 0, games = 0, dur = 0;
  let casts = 0, hands = 0, dealt = 0, taken = 0, secs = 0;
  const DT = AC.CONFIG.physics.dt;
  try {
    for (const foe of ids){
      for (let k = 0; k < n; k++){
        s = (Math.imul(s, 1103515245) + 12345) >>> 0;
        const r = AC.simulate(id, foe, s);
        if (r.winner === w.name) win++;
        games++; dur += r.duration;
      }
    }
    /* THE TELEMETRY IS A SEPARATE, SMALLER PASS, because `simulate` returns a
       result and not a match -- and what this table is FOR is how much
       set-piece is left, which a win rate cannot say. */
    const tf = ids.slice(0, 6), ts = [7, 331, 655, 979];
    for (const foe of tf) for (const sd of ts){
      const m = new AC.Match(id, foe, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let step = 0, prev = 0;
      while (!m.over && step < 130 / DT){
        m.step(DT); step++;
        if (m.hands.length > prev) hands += m.hands.length - prev;
        prev = m.hands.length;
      }
      casts += me.ultsFired; dealt += me.dealt; taken += th.dealt;
      secs += m.t;
    }
    const nf = tf.length * ts.length;
    return { rate: win / games, games, dur: dur / games,
             casts: casts / nf, hands: hands / nf,
             dealt: dealt / nf, taken: taken / nf, secs: secs / nf };
  } finally {
    w.dmg = d0;
    for (const k of Object.keys(w.ult)) delete w.ult[k];
    for (const k of Object.keys(u0)) w.ult[k] = u0[k];
  }
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-gravemourn.html")
    ap.add_argument("--blade", type=float, default=39.79,
                    help="the RESTORED blade every arm is priced at")
    ap.add_argument("--n", type=int, default=6, help="seeds per pairing")
    A = ap.parse_args()

    path = resolve_game(A.game)
    print(f"\nWEAKENING GRASP at a restored blade of {A.blade:g}   ({path.name})")
    print(f"  every arm is the whole 26-relic field, {A.n} seeds a pairing "
          f"= {26 * A.n} fights\n")
    print(f"  {'arm':<18}{'win':>7}{'casts':>7}{'hands':>7}{'dealt':>7}"
          f"{'taken':>7}{'secs':>7}   what it costs the picture")
    spent = 0
    rows = []
    with game(game_path=path) as (page, errors):
        for i, (knob, val) in enumerate(ARMS):
            r = page.evaluate(WIN_JS, [RID, A.blade,
                                       None if val is None else knob,
                                       val, A.n, 5000 + i * 97])
            spent += r["games"]
            label = "control" if val is None else f"{knob} {val:g}"
            note = {
                "control": "the shipped ultimate",
                "dur": "a SHORTER set-piece — fewer hands, less to watch",
                "reachMul": "the CHAIN, which is 75% of its value and defensive",
                "handMul": "cosmetic — every hand still flies, it just takes less",
                "charge": "it happens less often; each one is unchanged",
            }["control" if val is None else knob]
            rows.append((label, r, note))
            print(f"  {label:<18}{r['rate'] * 100:>6.1f}%{r['casts']:>7.1f}"
                  f"{r['hands']:>7.1f}{r['dealt']:>7.0f}{r['taken']:>7.0f}"
                  f"{r['secs']:>7.1f}   {note}")
        if errors:
            print("\n  page errors:", errors[:3])

    print(f"\n  {spent} fights spent")
    near = [(l, r) for l, r, _ in rows if abs(r["rate"] - 0.50) <= 0.05]
    print(f"\n  WITHIN 5 POINTS OF 50%: "
          + (", ".join(f"{l} ({r['rate'] * 100:.1f}%)" for l, r in near)
             if near else "none — widen the arms"))
    print("  These are not the same relic afterwards. That is the decision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
