#!/usr/bin/env python3
"""What does the LAST N seconds of a fight hold? For picking short-cut clips.

    python finish_probe.py --game ../02-chain/sc-nightglass-fx.html --pairs vesper:culverin --seeds 1001-1080
    python finish_probe.py --game ../02-chain/sc-nightglass-fx.html --all-unposted posted.txt --seeds 777001,784920 --json out.json

Per fight: length, winner, winner HP %, both sides' HP % when the final window
opens ("was the result still open?"), ult casts inside the window, and hits +
clanks inside it. A short cut filmed with the app's "seconds before the finish"
shows exactly that window, so these are the numbers the viewer gets.

Written 2026-09-29 for 08-analytics/short-cut-test-2026-09-29.md. Picks there
were measured on HeadlessChrome 141 in Cowork's container, NOT the pinned
runtime -- a seed can play differently in the app. The app's Replay is the check.
"""
from __future__ import annotations

import argparse
import itertools
import json
import statistics
import sys

from scpage import game, resolve_game

JS = r"""([pairs, seeds, win]) => {
  const dt = AC.CONFIG.physics.dt;
  const wasOn = AC.SFX.on; AC.SFX.on = false;
  const out = [];
  try {
    for (const p of pairs) { const [a, b] = p.split(':');
      for (const seed of seeds) {
        const m = new AC.Match(a, b, seed);
        let g = 0, prev = null, nextSnap = 0; const casts = [], snap = [];
        while (!m.over && g++ < 400000) {
          m.step(dt);
          const u = m.ultFx; const k = u ? (u.w + '|' + u.src) : null;
          if (k && k !== prev) casts.push(m.t);
          prev = k;
          if (m.t >= nextSnap) { snap.push([m.t, m.a.hits + m.b.hits + m.a.clanks + m.b.clanks, m.a.hp, m.b.hp]); nextSnap += 0.5; }
        }
        const T = m.t, t0 = T - win; let base = snap[0];
        for (const s of snap) { if (s[0] <= t0) base = s; else break; }
        const W = m.winner;
        out.push({ a, b, seed, t: +T.toFixed(2), reason: m.reason || null, win: W ? W.w.id : null,
          winHpPct: W ? +(100 * W.hp / W.maxHp).toFixed(1) : null,
          castsInWin: casts.filter(c => c >= t0).length,
          actInWin: m.a.hits + m.b.hits + m.a.clanks + m.b.clanks - base[1],
          hpAtWin: [Math.round(100 * base[2] / m.a.maxHp), Math.round(100 * base[3] / m.b.maxHp)] });
      } }
  } finally { AC.SFX.on = wasOn; }
  return out;
}"""


def seeds_arg(s: str) -> list[int]:
    if "-" in s and "," not in s:
        lo, hi = (int(x) for x in s.split("-"))
        return list(range(lo, hi + 1))
    return [int(x) for x in s.split(",")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", required=True)
    ap.add_argument("--pairs", help="a:b,c:d")
    ap.add_argument("--all-unposted", metavar="FILE", help="every pairing on the build except a:b lines in FILE")
    ap.add_argument("--seeds", required=True, help="1001-1080 or 5,9,12")
    ap.add_argument("--win", type=float, default=15.0, help="seconds before the finish")
    ap.add_argument("--json")
    A = ap.parse_args()
    seeds = seeds_arg(A.seeds)
    rows = []
    with game(game_path=resolve_game(A.game)) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if A.pairs:
            pairs = A.pairs.split(",")
        elif A.all_unposted:
            skip = {frozenset(l.strip().split(":")) for l in open(A.all_unposted) if ":" in l}
            pairs = [f"{a}:{b}" for a, b in itertools.combinations(ids, 2) if frozenset((a, b)) not in skip]
        else:
            ap.error("--pairs or --all-unposted")
        print(page.evaluate("() => navigator.userAgent"))
        for i in range(0, len(pairs), 20):
            rows += page.evaluate(JS, [pairs[i:i + 20], seeds, A.win])
            print(f"  {min(i + 20, len(pairs))}/{len(pairs)} pairings", flush=True)
        if errors:
            print("! page errors:", *errors[:5], sep="\n  ")
            return 1
    by: dict[str, list] = {}
    for r in rows:
        by.setdefault(f"{r['a']}:{r['b']}", []).append(r)
    for p, L in by.items():
        a, _ = p.split(":")
        n = len(L)
        print(f"{p:32s} n={n:3d}  {a} wins {100 * sum(r['win'] == a for r in L) / n:4.0f}%  "
              f"median {statistics.median(r['t'] for r in L):4.0f}s  "
              f"open at window {100 * sum(min(r['hpAtWin']) >= 35 for r in L) / n:4.0f}%  "
              f"ult in window {100 * sum(r['castsInWin'] > 0 for r in L) / n:4.0f}%  "
              f"winner HP {statistics.median(r['winHpPct'] for r in L):4.0f}%")
    if A.json:
        json.dump(rows, open(A.json, "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
