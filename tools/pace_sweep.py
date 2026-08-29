#!/usr/bin/env python3
"""HOW LONG IS A FIGHT, AND WHAT MAKES IT THAT LONG?

    python pace_sweep.py                          the coarse grid
    python pace_sweep.py --scales 1.0,1.3 --hp 1.0,1.4 --n 40
    python pace_sweep.py --apply-check 1.35 1.30  one cell, big sample

Rick, 2026-08-29: *"lets try something simple. get rid of the timeout win, let
fights go to their full conclusion. increase the time it takes for the arena to
shrink and increase fighter hp across the board to achieve desired fight
length."* Target: 45-60s, against a measured 37.3s today.

## Two knobs, and the second is the one that is easy to get wrong

    H   CONFIG.combat.baseHP multiplier                   300 -> 300*H
    S   the CLOCK scale: CONFIG.acts[].t, collapse.startT
        and timeout, all multiplied together

**HP ALONE DOES NOT MAKE A LONGER FIGHT OF THE SAME SHAPE.** Damage escalates
on a wall clock:

    t=0    dmg 1.00
    t=15   SECOND SEAL   dmg 1.35, spin 1.20   <- the hall starts closing here
    t=35   THIRD SEAL    dmg 1.85, spin 1.42

So raising HP without moving the seals spends the extra health inside the Third
Seal at 1.85x damage: duration rises much less than linearly, and the fight
that results is a different fight -- most of it at the escalated damage rather
than proportionally more of each act. Stretching the clock with the HP keeps
the SHAPE and changes the length, which is what "longer fights" should mean.

**AND collapse.startT IS NOT FREE TO MOVE ON ITS OWN.** The build says why:

  > Starts on the Second Seal, not at an arbitrary clock time: the seal breaks
  > and the hall begins to close. [...] a wall that starts closing at an
  > unexplained clock time is exactly the invisible correction this project
  > deleted `seek` over.

So this sweep moves `collapse.startT` WITH `acts[1].t` and never independently.
Rick asked for the arena to shrink later; that is what delivers it, and it
keeps the reason the viewer can see.

## What is measured, and why not just duration

  dur      mean seconds, the target
  p90      because a mean of 50 built from 30s and 90s is not the ask
  timeout  fights ending on the clock rather than on a death. Rick wants this
           at ZERO -- "let fights go to their full conclusion"
  spread   winrate range across the sampled relics. verify.py fails outside
           30-70%, and a longer fight favours anything that banks or heals HP,
           so this moves whether or not anyone intends it to
  ults     casts per fight. Ult charge is PURE WALL TIME (13-18s), so a longer
           fight buys more set-pieces automatically -- and since every one of
           the twenty-five now emits a particle field, that is a change to the
           film's rhythm that should be a number rather than a surprise

## Cost

`CLAUDE.md` §6: tuning found one number for 24,700 fights, and names
"bisections should escalate their sample" as a cheap win nobody has taken. So
the grid runs SMALL and only the chosen cell is re-run large. Nothing is
applied here -- this tool writes no build.
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
BUILD = REPO / "02-chain" / "sc-paradox-arc.html"

# Ten pairings across schools rather than one. Duration is a property of a
# MATCHUP as much as of the config -- verify.py's own range is 22.5s to 59.2s
# across pairings -- so a grid measured on one pair would tune the config to
# that pair. Same reasoning as CLAUDE.md §4.8.
PAIRS = ["paradox:heartwood", "emberedge:bulwarden", "lastlight:dawnbringer",
         "widowmaker:ironhail", "aureole:spellbreaker", "grudgebearer:thornwake",
         "foregone:marrowdraw", "redflail:censer", "axiom:vinesower",
         "nightfell:farwarden"]

SWEEP_JS = r"""([pairs, seeds, H, S, noTimeout]) => {
  const C = AC.CONFIG;
  /* Snapshot every number this tool touches, so one page can run the whole
     grid without a reload and cell N+1 cannot inherit cell N. */
  const keep = {
    hp: C.combat.baseHP,
    acts: C.acts.map(a => a.t),
    startT: C.collapse.startT,
    timeout: C.timeout,
  };
  C.combat.baseHP = Math.round(keep.hp * H);
  for (let i = 0; i < C.acts.length; i++) C.acts[i].t = keep.acts[i] * S;
  /* WITH acts[1], never independently -- the hall closes because the seal
     breaks, and that is the thing the viewer can see. */
  C.collapse.startT = C.acts[1].t;
  C.timeout = noTimeout ? 100000 : keep.timeout * S;

  const wasOn = AC.SFX.on; AC.SFX.on = false;
  const dt = C.physics.dt;
  const out = [];
  try {
    for (const p of pairs){
      const [a, b] = p.split(":");
      for (const seed of seeds){
        const m = new AC.Match(a, b, seed);
        let g = 0, casts = 0, prev = null;
        while (!m.over && g++ < 400000){
          m.step(dt);
          const u = m.ultFx;
          const k = u ? (u.w + "|" + u.src) : null;
          if (k && k !== prev) casts++;
          prev = k;
        }
        out.push({ a: a, b: b, seed: seed, t: +m.t.toFixed(2),
                   over: !!m.over, reason: m.reason || null,
                   win: m.winner ? m.winner.w.id : null,
                   casts: casts });
      }
    }
  } finally {
    AC.SFX.on = wasOn;
    C.combat.baseHP = keep.hp;
    for (let i = 0; i < C.acts.length; i++) C.acts[i].t = keep.acts[i];
    C.collapse.startT = keep.startT;
    C.timeout = keep.timeout;
  }
  return out;
}"""

BASE_JS = """() => ({
  hp: AC.CONFIG.combat.baseHP,
  acts: AC.CONFIG.acts.map(a => a.t),
  startT: AC.CONFIG.collapse.startT,
  timeout: AC.CONFIG.timeout,
})"""


def summarise(rows):
    dur = [r["t"] for r in rows]
    dur.sort()
    n = len(rows)
    wins, seen = {}, {}
    for r in rows:
        for side in (r["a"], r["b"]):
            seen[side] = seen.get(side, 0) + 1
        if r["win"]:
            wins[r["win"]] = wins.get(r["win"], 0) + 1
    rates = [100 * wins.get(k, 0) / v for k, v in seen.items() if v >= 4]
    return {
        "n": n,
        "dur": statistics.mean(dur) if dur else 0,
        "p90": dur[int(0.9 * (len(dur) - 1))] if dur else 0,
        "timeout": 100 * sum(1 for r in rows if r["reason"] == "timeout") / n,
        "unresolved": sum(1 for r in rows if not r["over"]),
        "lo": min(rates) if rates else 0,
        "hi": max(rates) if rates else 0,
        "casts": statistics.mean([r["casts"] for r in rows]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--scales", default="1.0,1.2,1.4,1.6",
                    help="clock scale S: acts, collapse.startT and timeout")
    ap.add_argument("--hp", default="1.0,1.2,1.4",
                    help="baseHP multiplier H")
    ap.add_argument("--n", type=int, default=10, help="seeds per pairing")
    ap.add_argument("--seed0", type=int, default=25064)
    ap.add_argument("--keep-timeout", action="store_true",
                    help="leave the timeout win in. Off by default because "
                         "Rick asked for it gone")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2
    scales = [float(x) for x in args.scales.split(",") if x.strip()]
    hps = [float(x) for x in args.hp.split(",") if x.strip()]
    seeds = [(args.seed0 + i * 7919) & 0xFFFFFFFF for i in range(args.n)]
    total = len(scales) * len(hps) * len(PAIRS) * len(seeds)

    print(f"PACE SWEEP  {len(PAIRS)} pairings x {len(seeds)} seeds = "
          f"{len(PAIRS)*len(seeds)} fights per cell, {total:,} total")
    print(f"  timeout win: {'KEPT' if args.keep_timeout else 'REMOVED'}   "
          f"target 45-60s   today 37.3s\n")
    print(f"  {'S':>5}{'H':>6}{'baseHP':>8}{'seal2':>7}{'seal3':>7}"
          f"{'dur':>8}{'p90':>7}{'t/out':>7}{'unres':>7}"
          f"{'winrate':>13}{'ults':>6}")

    grid = []
    with game(game_path=path) as (page, errors):
        # THE SOURCE'S OWN NUMBERS, so the label cannot lie. An earlier version
        # printed 300*H and 15*S, which is right only if the build is stock --
        # run against a build pace_build.py had already paced, it reported
        # "baseHP 300, seals 15/35" over a build carrying 400 and 21/49.
        base = page.evaluate(BASE_JS)
        seals = "/".join(str(round(t)) for t in base["acts"][1:])
        print(f"  source: baseHP {base['hp']}  seals {seals}  "
              f"collapse {round(base['startT'])}  timeout {base['timeout']}\n")
        for S in scales:
            for H in hps:
                rows = page.evaluate(SWEEP_JS, [PAIRS, seeds, H, S,
                                                not args.keep_timeout])
                s = summarise(rows)
                s.update({"S": S, "H": H})
                grid.append(s)
                mark = "  <-" if 45 <= s["dur"] <= 60 and s["timeout"] == 0 \
                    and s["lo"] >= 30 and s["hi"] <= 70 else ""
                print(f"  {S:>5.2f}{H:>6.2f}{round(base['hp']*H):>8}"
                      f"{base['acts'][1]*S:>7.1f}{base['acts'][2]*S:>7.1f}"
                      f"{s['dur']:>8.1f}{s['p90']:>7.1f}"
                      f"{s['timeout']:>6.0f}%{s['unresolved']:>7}"
                      f"{s['lo']:>6.0f}-{s['hi']:<6.0f}{s['casts']:>6.1f}{mark}")
        if errors:
            print("\n! page errors:")
            for e in errors[:6]:
                print("   ", e)
            return 1

    ok = [g for g in grid if 45 <= g["dur"] <= 60 and g["timeout"] == 0
          and g["unresolved"] == 0]
    print(f"\n  {len(ok)} of {len(grid)} cells land in 45-60s with no timeouts "
          f"and nothing unresolved.")
    print("\n  THE WINRATE COLUMN IS REPORTED AND NOT GATED, and it is not "
          "verify.py's number.\n  With 10 pairings each relic faces exactly "
          "ONE opponent here, so that is a\n  MATCHUP rate -- 80% means it "
          "beats its single opponent, not the roster.\n  verify.py --n 40 "
          "over 300 pairings is the balance gate; this tool is for\n  "
          "duration. Run it on the built config before believing any of this.")
    if ok:
        best = min(ok, key=lambda g: abs(g["dur"] - 52))
        print(f"\n  closest to the middle of the band: S={best['S']:.2f} "
              f"H={best['H']:.2f}  ->  {best['dur']:.1f}s, "
              f"{best['casts']:.1f} ults/fight")
        print(f"    baseHP {round(base['hp']*best['H'])}   "
              f"SECOND SEAL t={base['acts'][1]*best['S']:.0f}   "
              f"THIRD SEAL t={base['acts'][2]*best['S']:.0f}   "
              f"collapse.startT {base['acts'][1]*best['S']:.0f}")
        print("\n  THE SAMPLE IS SMALL. Re-run that cell alone at a high --n "
              "before building it;\n  a winrate off 10 fights per relic is not "
              "a winrate. CLAUDE.md §6.")
    else:
        print("\n  Nothing qualified. Widen --scales / --hp rather than "
              "relaxing the bands.")

    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(grid, indent=1))
        print(f"\n  wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
