#!/usr/bin/env python3
"""WHY THE STAGE-2 GATE MISSED BY TEN POINTS. One question, four arms.

    python wire_channel.py --game ../02-chain/sc-wire.html --sn 26

`06-docs/v60/ravelbone-build-v60.md` §5a: the ring was registered at **+24 ± 3**
over Ravelbone's own no-ultimate floor and it measured **+14.3**, with every
contact number at or above the lab's. The brief's instruction on that gate
failing is that something is wrong with the ring.

**THERE IS A SECOND READING AND IT HAS TO BE ELIMINATED FIRST.**
`wire_lab.py` measured all 26 arms on *"Grudgebearer standing in as a bloodsworn
warhammer with its own Crucible suppressed"* -- and Grudgebearer's `onHit` is
`{sunder: 1}`, not `{hemorrhage: 2}`. Those are not interchangeable:

    sunder       the biggest damage-rate channel in the game, +13.6%, and it
                 costs -1.4pp of win rate           (open item 23)
    hemorrhage   costs this cell FIFTY blade damage a fight -- 303 against a
                 no-channel 353 -- while lifting it 22.1%, because the bleed
                 SHORTENS the fight so the blade delivers less of it
                 (`row_price --type warhammer --pin 0`, and open item 24)

So if the stand-in carried Sunder, every lift in `wirering-design-v60.md` is a
lift measured through a different channel, and +24 was never this relic's
number to miss.

**FOUR ARMS, AND THE ANSWER IS A DIFFERENCE OF DIFFERENCES:**

    hemorrhage, no ult    hemorrhage, GARROTE     -> the lift that shipped
    sunder,     no ult    sunder,     GARROTE     -> the lift the lab measured

If the sunder lift comes back near +24 and the hemorrhage lift near +14, the
gate was measuring the stand-in and the ring is fine. If BOTH come back near
+14, the channel is exonerated and something in the built ring really is worth
ten points less than the lab's.

THE ULTIMATE IS SWITCHED OFF THE WAY EVERY OTHER SWEEP IN THIS REPO DOES IT --
`charge = 1e9`, so the clock can never reach it and `fireUlt` never runs. The
channel is switched by rewriting `onHit` on the weapon object, which is the
same surface `row_price` uses.

n >= 700 A POINT IS A FLOOR AND NOT A GUARANTEE (CLAUDE.md: two readings of one
arm came back 4.3 points apart at n=702), so `--sn 26` over 29 foes is 754
fights an arm and the printed SE is the thing to read, not the point estimate.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "ravelbone"

ARMS_JS = r"""([rid, foes, seeds, secs, onHit, ultOn]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid);
  const keepOnHit = JSON.parse(JSON.stringify(W.onHit));
  const keepCharge = W.ult.charge;
  W.onHit = JSON.parse(onHit);
  /* THE SAME "OFF" EVERY SWEEP IN THIS REPO USES. The clock cannot reach it,
     so `fireUlt` never runs and the relic is a blade and a channel. */
  W.ult.charge = ultOn ? keepCharge : 1e9;
  let wins = 0, n = 0, dur = 0, dealt = 0, casts = 0;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, foeId, sd);
        const me = m.a;
        let i = 0;
        while (!m.over && i < secs / DT){ m.step(DT); i++; }
        n++; dur += m.t; dealt += me.dealt; casts += me.ultsFired;
        if (me.hp > (me === m.a ? m.b : m.a).hp) wins++;
      }
    }
  } finally {
    W.onHit = keepOnHit;
    W.ult.charge = keepCharge;
  }
  return { wins, n, dur, dealt, casts };
}"""


def se(p, n):
    return 100.0 * math.sqrt(max(p * (1 - p), 1e-9) / max(1, n))


# ---------------------------------------------------------- THE DECOMPOSITION
# The channel came back REFUTED IN THE WRONG DIRECTION -- sunder lifts LESS
# (+11.9) than hemorrhage (+16.2), so if the lab's stand-in carried sunder it
# should have measured under +24, not over. That eliminates the yardstick and
# leaves the ring.
#
# So this pass rebuilds `wirering-design-v60.md`'s OWN decomposition on the
# BUILT relic, arm for arm, because the design's single most load-bearing
# number is not the +24 at all -- it is §1.2's **"spin with no ring at all is
# +18.7"**. If the built spin is worth anything like that, the ring is worth
# almost nothing and the design's causal story is wrong. If the built spin is
# worth far less, the wind-up is not doing what the lab's did and THAT is the
# ten points.
#
# `spinMul` 1 is the "no wind-up" arm and it is the cleanest possible switch:
# `tickWeapon` multiplies by `f.w.ult.spinMul || 1`, so setting it to 1 leaves
# every other line of the ultimate running and removes only the rotation.
DECOMP_JS = r"""([rid, foes, seeds, secs, spinMul, ultOn, radius]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const keep = { spinMul: U.spinMul, charge: U.charge, radius: U.radius };
  U.spinMul = spinMul;
  U.radius = radius;
  U.charge = ultOn ? keep.charge : 1e9;
  let wins = 0, n = 0, casts = 0, spun = 0, blows = 0, foeBlows = 0;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, foeId, sd);
        const me = m.a, th = m.b;
        let i = 0;
        while (!m.over && i < secs / DT){
          m.step(DT); i++;
          if (me.ultWire) spun += DT;
        }
        n++; casts += me.ultsFired; blows += me.hits; foeBlows += th.hits;
        if (me.hp > th.hp) wins++;
      }
    }
  } finally { U.spinMul = keep.spinMul; U.charge = keep.charge;
             U.radius = keep.radius; }
  return { wins, n, casts, spun, blows, foeBlows };
}"""


def decompose(gp, seeds, a):
    """Rebuild the design's own arm table on the BUILT relic."""
    print(f"\nTHE DECOMPOSITION — the design's own arms, on the built relic")
    U0 = None
    rows = []
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        U0 = page.evaluate("(r) => JSON.parse(JSON.stringify("
                           "AC.WEAPONS.find(w=>w.id===r).ult))", RID)
        foes = [i for i in ids if i != RID]
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights an arm\n")
        arms = [
            ("the floor, no ultimate",   1.0,        False, U0["radius"]),
            ("the WIND-UP alone",        U0["spinMul"], True, 0.0),
            ("the ring, spin x1",        1.0,        True,  U0["radius"]),
            ("EVERYTHING, as shipped",   U0["spinMul"], True, U0["radius"]),
        ]
        print("  arm                        win      SE   casts  window  "
              "blows  foe blows")
        for label, sm, on, rad in arms:
            r = page.evaluate(DECOMP_JS,
                              [RID, foes, seeds, a.secs, sm, on, rad])
            p = r["wins"] / max(1, r["n"])
            rows.append((label, 100 * p, se(p, r["n"]), r))
            print(f"  {label:<26} {100*p:5.1f}%  {se(p, r['n']):5.2f}  "
                  f"{r['casts']/max(1,r['n']):5.2f}  "
                  f"{r['spun']/max(1,r['n']):5.2f}s  "
                  f"{r['blows']/max(1,r['n']):5.2f}  "
                  f"{r['foeBlows']/max(1,r['n']):8.2f}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))

    base = rows[0][1]
    print(f"\n  LIFT OVER THE FLOOR ({base:.1f}%):")
    for label, win, s, _ in rows[1:]:
        print(f"    {label:<26} {win - base:+5.1f}  +/- "
              f"{math.hypot(s, rows[0][2]):.1f}")
    print("\n  THE DESIGN'S OWN NUMBERS, for the same three arms:")
    print("    spin with no ring at all       +18.7     (design §1.2)")
    print("    the §1 as written              +27.8     (design §2)")
    print("    the SNAG arm                   +24.0     (design §3)")
    print("\n  AND THE ONE TO READ IS `foe blows`. The design's whole law is")
    print("  `lift = +8.2 + 8.25 x (blows the opponent did not land)`, r2 0.89,")
    print("  validated out of sample. If the built arms move the win rate")
    print("  WITHOUT moving that column, the law does not describe this build.")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"arms": [{"label": l, "win": w, "se": s, **r}
                      for l, w, s, r in rows], "ult": U0}, indent=1),
            encoding="utf-8")
        print(f"  wrote {a.json}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-wire.html")
    ap.add_argument("--sn", type=int, default=26, help="seeds a pairing")
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    ap.add_argument("--decompose", action="store_true",
                    help="rebuild the design's own arm table on "
                         "the BUILT relic instead")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [40009 + 617 * i for i in range(a.sn)]
    print(f"\nWHY THE GATE MISSED — the channel, or the ring — {gp.name}")

    if a.decompose:
        return decompose(gp, seeds, a)

    arms = [("hemorrhage", '{"hemorrhage":2}', False),
            ("hemorrhage", '{"hemorrhage":2}', True),
            ("sunder",     '{"sunder":1}',     False),
            ("sunder",     '{"sunder":1}',     True)]
    out = {}
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        foes = [i for i in ids if i != RID]
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights an arm, 4 arms\n")
        print("  channel      ult   win      SE    fights   dur    dealt  casts")
        for ch, oh, on in arms:
            r = page.evaluate(ARMS_JS, [RID, foes, seeds, a.secs, oh, on])
            p = r["wins"] / max(1, r["n"])
            out[f"{ch}-{'on' if on else 'off'}"] = dict(
                r, win=100 * p, se=se(p, r["n"]))
            print(f"  {ch:<12} {'ON ' if on else 'off'}  {100*p:5.1f}%  "
                  f"{se(p, r['n']):5.2f}  {r['n']:>6}  "
                  f"{r['dur']/max(1,r['n']):5.1f}s  "
                  f"{r['dealt']/max(1,r['n']):6.0f}  "
                  f"{r['casts']/max(1,r['n']):5.2f}")
        if errors:
            print("  ERRORS: " + "; ".join(errors[:3]))

    hl = out["hemorrhage-on"]["win"] - out["hemorrhage-off"]["win"]
    sl = out["sunder-on"]["win"] - out["sunder-off"]["win"]
    hse = math.hypot(out["hemorrhage-on"]["se"], out["hemorrhage-off"]["se"])
    sse = math.hypot(out["sunder-on"]["se"], out["sunder-off"]["se"])
    print(f"\n  THE LIFT, which is the quantity the gate is about:")
    print(f"    through hemorrhage (shipped)   {hl:+5.1f}  +/- {hse:.1f}")
    print(f"    through sunder     (the lab)   {sl:+5.1f}  +/- {sse:.1f}")
    print(f"    difference of differences      {sl - hl:+5.1f}  "
          f"+/- {math.hypot(hse, sse):.1f}")
    print("\n  REGISTERED: +24 +/- 3, from `wire_lab` on a Grudgebearer "
          "stand-in.")
    if sl - hl > math.hypot(hse, sse) * 2:
        print("  READ: the CHANNEL carries a real part of the gap. The lab's "
              "yardstick was\n        drawn on a relic with a different "
              "`onHit` and +24 was never this\n        relic's number to miss.")
    elif abs(sl - hl) < math.hypot(hse, sse):
        print("  READ: the channel is EXONERATED — both lifts agree inside one "
              "SE. Whatever\n        costs the ring ten points is in the RING, "
              "and the brief's instruction\n        on this gate stands.")
    else:
        print("  READ: inconclusive at this n. The channel moves the lift but "
              "not by enough\n        to close the gap on its own — raise "
              "`--sn` before concluding either way.")

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"arms": out, "liftHemorrhage": hl, "liftSunder": sl,
             "seHem": hse, "seSun": sse}, indent=1), encoding="utf-8")
        print(f"  wrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
