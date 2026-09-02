#!/usr/bin/env python
"""STATIC, PRICED ON THE BUILT RELIC -- the four-arm budget shape, gate 3.

    python arclight_price.py --game ../02-chain/sc-static.html --seeds 8

`storm_price.py` priced this ultimate as a SWARM RUN BESIDE the engine: bolts
that flew in a lab loop inside `m.step`, banking real ward and dealing damage
through `m.hurt`. This runs the same four arms on the ULTIMATE THAT WAS BUILT,
where the detonation goes through `resolveHit` and therefore collects crit,
damage jitter, the Sunder multiplier and the quarry's own ward, and where the
bolts bounce off `m.inset` rather than off the arena.

    A  the body, ward, no ultimate           the floor
    B  ward only        (dmg 0)              the feed
    C  detonation only  (ward 0)             the finale
    D  the whole of STATIC                   both

Paired on (foe, seed) exactly as v59's budget shape and the design's own table,
so every arm fights the same roster on the same seeds.

THE ARMS ARE THE BRIEF'S OWN TOGGLES -- "the toggles are `bank` -> 0 and `dmg`
-> 0" -- set on the shipped `ult` block and restored afterwards. Arm A is the
`charge:1e9` stub every stage-1 link in this project has used, so the floor is
measured on the same body the ultimate rides.
"""
from __future__ import annotations
import argparse, json, math, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

JS = r"""([rid, foes, seeds, secs, arms, blade]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid);
  const saved = { dmg: w.dmg, charge: w.ult.charge, ward: w.ult.ward,
                  bolt: w.ult.dmg };
  if (blade > 0) w.dmg = blade;
  const rows = [];
  for (const arm of arms){
    /* THE TOGGLES. Restored at the end of the run, and set from the SAVED
       values every time rather than from whatever the last arm left, so an arm
       list in any order measures the same four things. */
    w.ult.charge = arm === "A" ? 1e9 : saved.charge;
    w.ult.ward   = (arm === "B" || arm === "D") ? saved.ward : 0;
    w.ult.dmg    = (arm === "C" || arm === "D") ? saved.bolt : 0;
    for (const f of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, f, sd);
        const me = m.a.w.id === rid ? m.a : m.b;
        let step = 0;
        while (!m.over && step < secs / DT){ m.step(DT); step++; }
        rows.push({ arm, foe: f, seed: sd,
                    win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                    dur: +(step * DT).toFixed(1),
                    ults: me.ultsFired,
                    hp: +Math.max(0, me.hp).toFixed(1) });
      }
    }
  }
  w.dmg = saved.dmg; w.ult.charge = saved.charge;
  w.ult.ward = saved.ward; w.ult.dmg = saved.bolt;
  return rows;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-static.html")
    ap.add_argument("--relic", default="arclight")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--seed0", type=int, default=4401)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--arms", default="A,B,C,D")
    ap.add_argument("--blade", type=float, default=0.0,
                    help="override the blade for this run. The design's arms "
                         "were measured on a donor body at dmg 11.95; the "
                         "shipped relic starts at 8.3, and a floor read at one "
                         "is not the floor at the other.")
    ap.add_argument("--out", default="")
    A = ap.parse_args()
    seeds = [A.seed0 + 97 * i for i in range(A.seeds)]
    arms = A.arms.split(",")

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        ids = pg.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if A.relic not in ids:
            raise SystemExit(f"no `{A.relic}` in this build")
        foes = [i for i in ids if i != A.relic]
        blade = pg.evaluate("(r) => AC.WEAPONS.find(w => w.id === r).dmg",
                            A.relic)
        rows = pg.evaluate(JS, [A.relic, foes, seeds, A.secs, arms, A.blade])

    n = len(foes) * len(seeds)
    print(f"\nSTATIC, PRICED ON THE BUILT RELIC -- {len(foes)} foes x "
          f"{len(seeds)} seeds = {n} fights an arm")
    print(f"  {A.game}, blade {A.blade or blade:g}"
          + ("  (OVERRIDDEN for this run)" if A.blade else "  (as shipped)"))
    print("  the design's model, for reference: A 56.9%, B +16.1, C +25.0, "
          "D +33.1, on a donor body at dmg 11.95\n")

    def rate(arm):
        r = [x for x in rows if x["arm"] == arm and x["win"] >= 0]
        return (100.0 * sum(x["win"] for x in r) / len(r), len(r)) if r else (0.0, 0)

    def se(p, k):
        # A ROSTER WIN RATE IS NOT N INDEPENDENT FLIPS -- it is `len(foes)`
        # pairings of correlated fights, so this binomial figure is a FLOOR on
        # the error and the real precision is worse. v53: two measurements of
        # one arm at n=156 and n=208 came back 50.6% and 63.9%. Printed so the
        # tiers below are read as tiers.
        return 100.0 * math.sqrt(max(1e-9, (p / 100) * (1 - p / 100)) / max(1, k))

    base, kb = rate("A")
    print(f"    {'arm':<26} {'win':>7}  {'+/- SE':>7}  {'vs A':>7}   "
          f"{'ults/fight':>10}  {'dur':>6}")
    label = {"A": "A  the body, no ultimate", "B": "B  ward only (dmg 0)",
             "C": "C  detonation only (ward 0)", "D": "D  the whole of STATIC"}
    out = {}
    for arm in arms:
        p, k = rate(arm)
        r = [x for x in rows if x["arm"] == arm]
        u = sum(x["ults"] for x in r) / max(1, len(r))
        d = sum(x["dur"] for x in r) / max(1, len(r))
        out[arm] = p
        print(f"    {label.get(arm, arm):<26} {p:>6.1f}%  {se(p,k):>6.1f}   "
              + (f"{p-base:>+6.1f}" if arm != "A" else f"{'--':>7}")
              + f"   {u:>10.2f}  {d:>5.1f}s")

    print()
    tiers = {"B": (16.1, "the feed"), "C": (25.0, "the finale"),
             "D": (33.1, "the whole, on a body already spoken for")}
    ok = True
    for arm, (want, what) in tiers.items():
        if arm not in out or "A" not in out:
            continue
        got = out[arm] - base
        good = abs(got - want) <= 6.0
        ok = ok and good
        print(f"  {'in tier' if good else 'OUT OF TIER'}  {arm} - A = "
              f"{got:+.1f}pp against the design's {want:+.1f}  ({what})")
    if "D" in out:
        d = out["D"] - base
        if d > 45 or d < 20:
            print("\n  STOP. Brief gate 3: \"A D - A over +45 or under +20 is a "
                  "different relic -- stop and say what changed.\"")
    if A.out:
        pathlib.Path(A.out).write_text(json.dumps(rows), encoding="utf-8")
        print(f"\n  rows -> {A.out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
