#!/usr/bin/env python3
"""WHICH FIGHT IS WORTH FILMING — for ANY pairing, scored on the DIRECTOR'S PLAN.

    python pick_fight.py --a paradox --b heartwood --n 400
    python pick_fight.py --a lastlight --b grudgebearer --n 600 --json out.json

paradox_pick.py answers this for one relic, and half of it is Paradox's own
telemetry -- casts, holds, blows landed on a held quarry. This is the other
half, the part that is true of every pairing, so the app can ask it about
whatever two relics are on screen.

WHY A TOOL AND NOT A PERSON CLICKING FIGHT. Clicking picks on what a fight
LOOKED like in the moment. This asks two things a person cannot see from the
window:

  1. DOES THE DIRECTOR HAVE A FATAL CUT IN ITS PLAN. v41 lost two renders to
     seeds whose plan carried none -- the fight ends and the camera was never
     told, so the payoff is filmed as ordinary air. `window.cinePlan` answers
     it before a render rather than after one, which is the rule v42 set.
  2. HOW CLOSE IT FINISHES. The winner's remaining hp against baseHP 300. A
     fight decided at 4hp and one decided at 210 look the same until the end.

HARD FILTERS, then a rank. The filters are the things that make a clip
unusable; the rank is preference among clips that are all usable:

  hard   a fatal cut in the plan · finished by a kill, not a timeout ·
         duration inside --secs
  rank   closeness first, then how much the director found to cut

WRITES NOTHING unless --json. Reports the shortlist and the seed.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

SCAN_JS = r"""([a, b, seeds]) => {
  const BASE = AC.CONFIG.combat.baseHP;
  const out = [];
  for (const sd of seeds){
    let s;
    try { s = AC.simulate(a, b, sd); } catch (e) { continue; }
    if (!s.winner) continue;                       // a draw is not a clip
    /* cinePlan replays the fight through the director. It is the expensive
       half, so it only runs on seeds that already finished on a kill. */
    let p = null;
    if (s.reason !== 'timeout') {
      try { p = window.cinePlan(a, b, sd); } catch (e) { p = null; }
    }
    const kill = p && !p.err ? (p.cuts || []).find(c => c.fatal) : null;
    out.push({
      seed: sd, dur: +s.duration.toFixed(2), winner: s.winner,
      hp: s.hp, margin: +(s.hp / BASE).toFixed(3),
      clanks: s.clanks, hits: s.hits.a + s.hits.b, reason: s.reason,
      cuts: p && !p.err ? p.cuts.length : 0,
      fatal: !!kill, killT: kill ? +kill.t.toFixed(2) : null,
      tiers: p && !p.err ? (p.cuts || []).map(c => c.fatal ? 'KILL' : 'T' + c.tier).join(' ') : '',
      why: kill ? (kill.why || []).join(', ') : '',
    });
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-paradox-arc.html")
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--n", type=int, default=300, help="seeds to scan")
    ap.add_argument("--seed0", type=int, default=1)
    ap.add_argument("--secs", default="18,55", help="min,max fight duration")
    ap.add_argument("--margin", type=float, default=0.35,
                    help="winner's remaining hp as a fraction of baseHP; lower "
                         "is a closer finish")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    lo, hi = (float(x) for x in A.secs.split(","))
    g = (HERE / A.game).resolve()
    if A.a == A.b:
        sys.exit("! a relic cannot fight itself")

    seeds = list(range(A.seed0, A.seed0 + A.n))
    with game(game_path=g) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        for r in (A.a, A.b):
            if r not in ids:
                sys.exit(f"! {r!r} is not a relic in {g.name}")
        rows = []
        for i in range(0, len(seeds), 100):
            rows += page.evaluate(SCAN_JS, [A.a, A.b, seeds[i:i + 100]])
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    usable = [r for r in rows
              if r["fatal"] and r["reason"] != "timeout" and lo <= r["dur"] <= hi]
    close = [r for r in usable if r["margin"] <= A.margin]
    # Closeness first, then how much the director found. Both are preferences
    # among clips that are already usable -- the filters did the excluding.
    close.sort(key=lambda r: (r["margin"], -r["cuts"]))

    print(f"  {len(rows)} seeds simulated · {len(usable)} finish on a kill with a "
          f"FATAL cut, in {lo:g}-{hi:g}s · {len(close)} inside margin {A.margin}")
    if not close:
        print("\n  NOTHING QUALIFIES — raise --n, widen --secs, or raise --margin.")
        if usable:
            print(f"  ({len(usable)} were usable but none finished closer than "
                  f"{min(r['margin'] for r in usable):.2f} of a bar)")
        return 1
    print(f"\n  {'seed':>10}{'dur':>7}{'winner':>14}{'hp':>5}{'margin':>8}"
          f"{'cuts':>6}{'kill@':>7}  tiers")
    for r in close[:A.top]:
        print(f"  {r['seed']:>10}{r['dur']:>7.1f}{r['winner']:>14}{r['hp']:>5}"
              f"{r['margin']:>8.2f}{r['cuts']:>6}{r['killT'] or 0:>7.1f}  {r['tiers']}")
    best = close[0]
    print(f"\n  PICK: --a {A.a} --b {A.b} --seed {best['seed']}   "
          f"({best['dur']:.1f}s, {best['winner']} by {best['hp']}hp, "
          f"{best['cuts']} cuts)")
    if A.json:
        pathlib.Path(A.json).write_text(
            json.dumps({"ok": True, "picks": close[:A.top]}, indent=1), encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
