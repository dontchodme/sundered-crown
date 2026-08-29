#!/usr/bin/env python3
"""HOW OFTEN DOES AN ULTIMATE ACTUALLY GET A SHOT? — FX-RUNTIME-BRIEF.md §3.4.

    python ult_camera_probe.py                       the default pairings
    python ult_camera_probe.py --pairs paradox:heartwood --n 60
    python ult_camera_probe.py --window 1.2

§3.4 argues that an ultimate should own the camera, and prices the argument off
`cinema_rate_probe.py`'s number: **41% of matches contain zero cuts.** That is
the right shape and it is not the question. A match with no cuts might have had
no ultimate in it; a match with three cuts might have spent all three on
ordinary exchanges while its ultimate played wide and unremarked.

THE QUESTION IS PER-CAST, NOT PER-MATCH: when a relic spends the one thing it
owns alone, does the director point the camera at it? Nothing in this repo has
measured that, and every argument in §3.4 rests on it.

HOW A CAST IS DETECTED, and why not off the beats. `m.ultFx` is built in one
place and is presentation-only, so a cast is the frame where `ultFx` appears or
its `w` changes. That reads the engine's own event rather than inferring one
from the beat stream -- which matters, because Rule 3 exists precisely BECAUSE
some ultimates file no beat the director can see. Detecting casts through
beats would therefore be blind to exactly the relics the section is about.

A cast COUNTS AS FILMED if any cut in the plan opens within `--window` seconds
of it. That is generous on purpose: a cut whose drop begins a second before the
cast still has the ultimate on screen inside the shot. A tighter window would
flatter the argument, so the loose one is used and reported.

Costs one simulated match per seed and runs cinePlan on the same seed, so
roughly two matches of work per row. CLAUDE.md §6 on what a session's fights go
on.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-frame.html"

# Six pairings across schools rather than one, because "does the ult get a
# shot" could easily be a property of how HITTY a particular relic is -- a
# crowded ult files beats the director already loves, a quiet one files none.
DEFAULT_PAIRS = ["paradox:heartwood", "lastlight:dawnbringer",
                 "aureole:spellbreaker", "widowmaker:ironhail",
                 "slagheart:bulwarden", "foregone:marrowdraw"]

SCAN_JS = r"""([idA, idB, seed]) => {
  const wasOn = AC.SFX.on;
  AC.SFX.on = false;
  const dt = AC.CONFIG.physics.dt;
  const casts = [];
  let m, guard = 0, prev = null;
  try {
    m = new AC.Match(idA, idB, seed);
    while (!m.over && guard++ < 200000) {
      m.step(dt);
      /* A CAST IS AN EDGE, not a state. ultFx persists for `life` seconds and
         is advanced by the decay paths, so testing truthiness every step would
         count one cast a few hundred times. The edge is null->set, or the
         owner changing when the two relics ult close together. */
      const u = m.ultFx;
      const key = u ? (u.w + "|" + (u.src || "")) : null;
      if (key && key !== prev)
        casts.push({ w: u.w, src: u.src, t: +m.t.toFixed(3),
                     life: u.life || null, hit: !!u.hit });
      prev = key;
    }
  } catch (e) {
    AC.SFX.on = wasOn;
    return { err: String(e && e.message || e) };
  }
  AC.SFX.on = wasOn;

  const plan = cinePlan(idA, idB, seed);
  return {
    dur: +m.t.toFixed(2), over: m.over,
    casts: casts,
    cuts: (plan.cuts || []).map(c => ({
      t: +c.t.toFixed(3), tier: c.tier || null, fatal: !!c.fatal,
      score: +(c.score || 0).toFixed(3), kind: c.kind || null,
      span: +(c.span || 0).toFixed(3),
    })),
    err: plan.err || null,
  };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--pairs", default=",".join(DEFAULT_PAIRS))
    ap.add_argument("--n", type=int, default=24, help="seeds per pairing")
    ap.add_argument("--seed0", type=int, default=25064)
    ap.add_argument("--window", type=float, default=1.0,
                    help="a cast counts as filmed if a cut opens within this "
                         "many seconds of it, either side")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2
    pairs = [p.strip().split(":") for p in args.pairs.split(",") if p.strip()]

    rows, allc = [], []
    with game(game_path=path) as (page, errors):
        for a, b in pairs:
            casts = filmed = 0
            gaps, cutn, matches, no_cut = [], [], 0, 0
            for i in range(args.n):
                seed = (args.seed0 + i * 7919) & 0xFFFFFFFF
                r = page.evaluate(SCAN_JS, [a, b, seed])
                if r.get("err"):
                    print(f"! {a} v {b} seed {seed}: {r['err']}")
                    continue
                matches += 1
                cutn.append(len(r["cuts"]))
                if not r["cuts"]:
                    no_cut += 1
                for c in r["casts"]:
                    casts += 1
                    near = [abs(x["t"] - c["t"]) for x in r["cuts"]]
                    d = min(near) if near else None
                    if d is not None:
                        gaps.append(d)
                    if d is not None and d <= args.window:
                        filmed += 1
                    allc.append({"pair": f"{a}:{b}", "seed": seed,
                                 "w": c["w"], "src": c.get("src"),
                                 "hit": bool(c.get("hit")),
                                 "t": c["t"], "gap": d,
                                 "dur": r["dur"],
                                 "cuts": len(r["cuts"])})
            rows.append({"pair": f"{a} v {b}", "matches": matches,
                         "casts": casts, "filmed": filmed,
                         "cuts_mean": statistics.mean(cutn) if cutn else 0,
                         "no_cut_pct": 100 * no_cut / matches if matches else 0,
                         "gap_med": statistics.median(gaps) if gaps else None})
        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    print(f"\nDOES THE ULTIMATE GET A SHOT?   {args.n} seeds per pairing, "
          f"a cast counts as filmed\nif a cut opens within {args.window:.1f}s "
          f"of it\n")
    print(f"  {'pairing':<26}{'matches':>8}{'casts':>7}{'filmed':>8}{'':>3}"
          f"{'cuts/match':>11}{'no cuts':>9}{'med gap':>9}")
    for r in rows:
        pct = 100 * r["filmed"] / r["casts"] if r["casts"] else 0
        g = f"{r['gap_med']:.2f}s" if r["gap_med"] is not None else "-"
        print(f"  {r['pair']:<26}{r['matches']:>8}{r['casts']:>7}"
              f"{r['filmed']:>8}{pct:>7.0f}%{r['cuts_mean']:>11.2f}"
              f"{r['no_cut_pct']:>8.0f}%{g:>9}")

    C = sum(r["casts"] for r in rows)
    F = sum(r["filmed"] for r in rows)
    M = sum(r["matches"] for r in rows)
    print(f"\n  {'ALL':<26}{M:>8}{C:>7}{F:>8}"
          f"{(100*F/C if C else 0):>7.0f}%")

    if C:
        print(f"\n  {C - F} of {C} ultimate casts ({100*(C-F)/C:.0f}%) have no "
              f"cut within {args.window:.1f}s.")
        print("  An ultimate is the one thing a relic owns alone "
              "(sundered-crown-ult-model.md §2)\n  and it currently competes "
              "for the camera on the same bar as an ordinary\n  exchange -- "
              "`cinePlan` filters every beat through CINE.floor and an ult's "
              "beat\n  is just another beat in that pool.")
    # ---- WHAT WOULD IT COST TO FILM THEM? ----
    #
    # "Give the ultimate the camera" is not one proposal, it is a family, and
    # they differ by a factor of three in how much they change the PACING.
    # cinema_rate_probe.py's own numbers -- none 41%, one 37%, two 16%, 3+ 7%,
    # mean 0.90 cuts/match -- are what a change here is measured against, so
    # each policy is priced in the same unit.
    by_match = {}
    for c in allc:
        by_match.setdefault((c["pair"], c["seed"]), []).append(c)
    base = statistics.mean([v[0]["cuts"] for v in by_match.values()])         if by_match else 0

    def cost(keep):
        add = [len([c for c in v if keep(v, c)]) for v in by_match.values()]
        tot = [v[0]["cuts"] + n for v, n in zip(by_match.values(), add)]
        zero = 100 * sum(1 for t in tot if t == 0) / len(tot)
        return statistics.mean(add), statistics.mean(tot), zero

    def first_per_relic(v, c):
        return c is min([x for x in v if x["src"] == c["src"]],
                        key=lambda x: x["t"])

    print(f"\n  WHAT EACH POLICY WOULD COST, in cuts per match "
          f"(today: {base:.2f})\n")
    print(f"  {'policy':<34}{'ult cuts':>10}{'total':>8}{'no cuts':>9}")
    def first_in_match(v, c):
        return c is min(v, key=lambda x: x["t"])

    def last_in_match(v, c):
        return c is max(v, key=lambda x: x["t"])

    def finisher(v, c):
        # THE ULT THAT ENDS IT. The last cast of the match, and only when it
        # is close enough to the end to plausibly be what ended it. This is
        # the only policy that treats an ultimate as the rare thing §3.4
        # assumes it is -- at 3.7 casts a match it is not rare, and a policy
        # that fires on all of them is arguing with the game's own pacing.
        return last_in_match(v, c) and (c["dur"] - c["t"]) <= 3.0

    for name, keep in (
            ("every cast", lambda v, c: True),
            ("only casts that CONNECT", lambda v, c: c["hit"]),
            ("first cast per relic", first_per_relic),
            ("first cast per relic, if it hits",
             lambda v, c: c["hit"] and first_per_relic(v, c)),
            ("ONE per match: the first cast", first_in_match),
            ("ONE per match: the last cast", last_in_match),
            ("ONLY the ult that finishes it", finisher)):
        a_, t_, z_ = cost(keep)
        print(f"  {name:<34}{a_:>10.2f}{t_:>8.2f}{z_:>8.0f}%")
    print("\n  Today 41% of matches have no cut at all (CLAUDE.md). Any of "
          "these puts an\n  ultimate on screen properly; they differ in "
          "whether the film becomes busy.\n  THIS IS RICK'S CALL and the "
          "numbers are the spread, not a recommendation.")

    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"rows": rows, "casts": allc,
                                 "window": args.window}, indent=1))
        print(f"\n  wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
