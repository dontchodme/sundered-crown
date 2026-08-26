#!/usr/bin/env python3
"""Pick fights for the VESSEL round: legible liquid AND watchable television.

The usual scorer (`pick.py`) optimises for a fight worth watching. This round
is also being asked to JUDGE AN INSTRUMENT -- the glass vessel and its liquid
level -- and those two goals disagree in one specific place:

    a fight the winner finishes at 80% says NOTHING about whether a falling
    level reads.

So `|hp - HPTARGET|` is a first-class term, not a tiebreak. HPTARGET defaults
to 55 of baseHP 300 (~18%), which is the criterion the v31 liquid clips were
picked on -- low enough that the winner's vessel is visibly near-empty while
the loser's has failed outright.

Every rejection is REPORTED, not silently dropped, because a scan that quietly
filters 95% of its seeds and prints a top-5 looks identical whether the bar is
right or the bar is broken.

    python3 vessel_pick.py --game ../02-chain/sc-liquid-scrunch.html --n 240
"""
from __future__ import annotations
import argparse, collections, pathlib, statistics, sys
from scpage import game

HERE = pathlib.Path(__file__).parent

# Pairings are derived from the build's own roster, never hardcoded -- the
# scrunch probe learned this the hard way when 01-live threw "Unknown relic id"
# on a chain-only relic.
ROSTER_JS = "()=>AC.WEAPONS.map(w=>w.id)"

SCAN_JS = r"""
([pairs, n, seed0, cap]) => {
  const out = [], dt = AC.CONFIG.physics.dt, CAP = Math.round(cap / dt);
  let s = seed0 >>> 0;
  for (const [a, b] of pairs) {
    for (let i = 0; i < n; i++) {
      s = (Math.imul(s, 1103515245) + 12345) >>> 0;
      const r = AC.simulate(a, b, s);
      if (!r || r.reason !== "slain") { out.push({a, b, seed: s, bad: "timeout"}); continue; }
      /* second pass, early-exit: WHEN the first contact lands is the most
         expensive number in a Short and summary() does not report it */
      const m = new AC.Match(a, b, s); m.introT = 0;
      let clank = null, hit = null;
      for (let k = 0; k < CAP && !m.over; k++) {
        const c0 = m.clankCount, ha = m.a.hp, hb = m.b.hp;
        m.step(dt);
        if (clank === null && m.clankCount > c0) clank = m.t;
        if (hit === null && (m.a.hp < ha || m.b.hp < hb)) hit = m.t;
        if (clank !== null && hit !== null) break;
      }
      const p = window.cinePlan(a, b, s);
      out.push({ a, b, seed: s, hp: r.hp, dur: r.duration, winner: r.winner,
                 clanks: r.clanks, tOpen: clank, tHit: hit,
                 cuts: (p && !p.err) ? p.cuts.length : 0,
                 kill: !!(p && !p.err && p.cuts.some(c => c.fatal)),
                 whys: (p && !p.err)
                   ? p.cuts.map(c => (c.why || []).join("/")).filter(Boolean) : [] });
    }
  }
  return out;
}
"""


def score(r, a):
    """Higher is better. Every term is a stated opinion; none is a vibe."""
    if r.get("bad"):
        return None, r["bad"]
    t = r["tOpen"]
    if t is None or t > a.max_open:
        return None, f"slow open {'none' if t is None else round(t,1)}s"
    if not (a.lo <= r["dur"] <= a.hi):
        return None, f"duration {r['dur']}s outside {a.lo}-{a.hi}"
    if r["cuts"] < a.min_cuts:
        return None, f"{r['cuts']} cuts < {a.min_cuts}"

    s, why = 0.0, []
    # 1. VESSEL LEGIBILITY -- the reason this round exists.
    d = abs(r["hp"] - a.hp_target)
    s += max(0.0, 40.0 - 1.6 * d)
    if d <= 10:
        why.append(f"vessel {r['hp']}hp={round(100*r['hp']/300)}%")
    # 2. the front of the video
    if t <= 1.8:   s += 14.0; why.append("fast open")
    elif t <= 2.6: s += 6.0
    # 3. television: more cuts, and DIFFERENT cuts
    s += 5.0 * min(r["cuts"], 4)
    kinds = len(set(r["whys"]))
    s += 6.0 * (kinds - 1)
    if kinds >= 3: why.append(f"{kinds} distinct cuts")
    # 4. the kill itself earning a cut is the best single beat in the format
    if r["kill"]: s += 12.0; why.append("kill is a cut")
    # 5. shorter is safer against the 60s cap
    s += (a.hi - r["dur"]) * 0.35
    return s, ", ".join(why)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-liquid-scrunch.html")
    ap.add_argument("--n", type=int, default=240, help="seeds per pairing")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--lo", type=float, default=30.0)
    ap.add_argument("--hi", type=float, default=45.0)
    ap.add_argument("--max-open", type=float, default=2.6)
    ap.add_argument("--min-cuts", type=int, default=2)
    ap.add_argument("--hp-target", type=float, default=55.0)
    ap.add_argument("--seed0", type=int, default=20260819)
    ap.add_argument("--pairs", default=None,
                    help="comma list of a:b; default = a spread over the roster")
    a = ap.parse_args()

    path = pathlib.Path(a.game).resolve()
    with game(game_path=path) as (page, errs):
        roster = page.evaluate(ROSTER_JS)
        if a.pairs:
            pairs = [p.split(":") for p in a.pairs.split(",")]
        else:
            # a spread, not a clique: each relic appears at most twice, and the
            # two chain-only relics (lastlight, slagheart) are included on
            # purpose -- they have never been filmed.
            pairs = [[roster[i], roster[(i + 5) % len(roster)]]
                     for i in range(0, len(roster), 2)]
        unknown = [x for p in pairs for x in p if x not in roster]
        if unknown:
            sys.exit(f"not in this build's roster: {unknown}")
        print(f"  build   {path.name}")
        print(f"  roster  {len(roster)} relics")
        print(f"  pairs   {len(pairs)}: " + ", ".join(f'{x} v {y}' for x, y in pairs))
        print(f"  scan    {a.n} seeds each = {a.n*len(pairs)} matches\n")
        rows = page.evaluate(SCAN_JS, [pairs, a.n, a.seed0, 25.0])
        if errs:
            sys.exit(f"page errors: {errs[:3]}")

    kept, rej = [], collections.Counter()
    for r in rows:
        sc, why = score(r, a)
        if sc is None:
            rej[why.split()[0] + " " + why.split()[1] if len(why.split()) > 1 else why] += 1
        else:
            r["score"], r["why"] = sc, why
            kept.append(r)

    print(f"  {len(rows)} scanned -> {len(kept)} qualify ({100*len(kept)/max(1,len(rows)):.1f}%)")
    print("  rejected: " + ", ".join(f"{k} x{v}" for k, v in rej.most_common(6)) + "\n")
    if not kept:
        sys.exit("  nothing qualified -- SCAN for a fight, do not lower the bar")

    hps = [r["hp"] for r in kept]
    print(f"  qualifying winner HP: min {min(hps)} med {statistics.median(hps):.0f} max {max(hps)}\n")
    kept.sort(key=lambda r: -r["score"])
    print(f"  {'#':>2}  {'fight':34} {'seed':>11} {'dur':>6} {'open':>5} {'winHP':>6} {'cuts':>4}  why")
    for i, r in enumerate(kept[:a.top], 1):
        f = f"{r['a']} v {r['b']}"
        print(f"  {i:2}  {f:34} {r['seed']:>11} {r['dur']:6.1f} {r['tOpen']:5.2f} "
              f"{r['hp']:4}/300 {r['cuts']:4}  {r['why']}")


if __name__ == "__main__":
    main()
