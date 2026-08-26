#!/usr/bin/env python3
"""Scan seeds for a matchup and rank them by how watchable the fight is.

The seed is recorded on every match precisely so this is possible: sim a few
hundred coin flips, then publish the one worth watching. Scoring is explicit
and tunable rather than a vibe, so it can be argued with.

  python3 pick.py gravemourn dawnbringer --n 300 --top 5
"""
from __future__ import annotations

import argparse
import pathlib
import json

from scpage import game

SCAN_JS = r"""
([a, b, n, s0]) => {
  const out = [], dt = AC.CONFIG.physics.dt, CAP = Math.round(22 / dt);
  let s = s0 >>> 0;
  for (let i = 0; i < n; i++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const r = AC.simulate(a, b, s);
    /* Second pass, early-exit: AC.simulate does not report WHEN contact
       happened, and with a cold open that is the most expensive number in the
       video. Stepping only to the first clank costs a fraction of a full
       match, and the summary above is left exactly as it was so the existing
       ranking cannot move except through the new term. */
    const m = new AC.Match(a, b, s); m.introT = 0;
    let clank = null, hit = null;
    for (let k = 0; k < CAP && !m.over; k++) {
      const c0 = m.clankCount, ha = m.a.hp, hb = m.b.hp;
      m.step(dt);
      if (clank === null && m.clankCount > c0) clank = m.t;
      if (hit === null && (m.a.hp < ha || m.b.hp < hb)) hit = m.t;
      if (clank !== null && hit !== null) break;
    }
    r.tOpen = clank; r.tHit = hit;
    out.push(r);
  }
  return out;
}
"""


def score(r, lo=28.0, hi=44.0, max_open=6.0):
    """Higher is more watchable. Every term is a stated opinion about Shorts."""
    if r["reason"] != "slain":
        return -1e9, "timeout"                       # a timeout is not an ending

    # Time to first contact. With a cold open this is dead air at the front of
    # the video, where a Short is decided -- so a late opener is REJECTED
    # outright rather than merely penalised. p90 across the roster is 7.78s and
    # the worst seed measured 18.18s; those are not films, they are wallpaper.
    t_open = r.get("tOpen")
    if t_open is None or t_open > max_open:
        return -1e9, f"cold open {t_open if t_open is None else round(t_open, 1)}s"

    d = r["duration"]
    why = []
    s = 0.0

    # inside p25 (1.78s) is a fight that starts before the viewer can leave
    if t_open <= 1.8:
        s += 14.0; why.append("fast open")
    elif t_open <= 3.2:                              # inside the median
        s += 6.0

    # length: inside the band is free, outside costs fast
    if d < lo:
        s -= (lo - d) * 3.0; why.append("short")
    elif d > hi:
        s -= (d - hi) * 3.5; why.append("long")
    else:
        s += 12.0

    # a close finish is the whole point — comebacks matter more than balance
    hp = r["hp"] or 0
    s += max(0.0, 40.0 - hp * 0.30)
    if hp <= 60:
        s += 18.0; why.append("close")

    # binds are the signature mechanic; some is good, a lockfest is not
    c = r["clanks"]
    s += min(c, 16) * 1.6 - max(0, c - 22) * 2.5
    if c >= 12:
        why.append("clanky")

    # both sides must land — a one-sided beating reads as a bug
    ha, hb = r["hits"]["a"], r["hits"]["b"]
    lo_h, hi_h = min(ha, hb), max(ha, hb)
    if lo_h == 0:
        s -= 60.0; why.append("one-sided")
    else:
        s += 10.0 * (lo_h / hi_h)

    if r["crits"]["a"] + r["crits"]["b"] > 0:
        s += 4.0
    return s, ",".join(why) or "plain"


def scan(a, b, n=300, seed0=12345, lo=28.0, hi=44.0, top=5, game_path=None,
         max_open=6.0):
    with game(game_path=game_path) as (page, errors):
        rows = page.evaluate(SCAN_JS, [a, b, n, seed0])
        if errors:
            raise SystemExit("page errors:\n  " + "\n  ".join(errors))
    scored = []
    for r in rows:
        sc, why = score(r, lo, hi, max_open)
        scored.append({"score": round(sc, 1), "why": why, **r})
    scored.sort(key=lambda r: -r["score"])
    return scored[:top], rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--lo", type=float, default=28.0)
    ap.add_argument("--hi", type=float, default=44.0)
    ap.add_argument("--max-open", type=float, default=6.0,
                    help="reject seeds whose first clank is later than this "
                         "(seconds). Roster p75 is 4.58s, p90 is 7.78s.")
    # Variants are how this project makes broken things safely: the shipped
    # artifact is never edited, an experiment is generated beside it (see
    # vigil_build.py), and every tool that can judge the game has to be able
    # to point at either. verify.py grew this first; a change is not judged
    # until it has been WATCHED, so pick and render need it too.
    ap.add_argument("--game", default=None,
                    help="scan a variant HTML instead of sundered-crown.html")
    a = ap.parse_args()
    best, allr = scan(a.a, a.b, a.n, top=a.top, lo=a.lo, hi=a.hi,
                      max_open=a.max_open,
                      game_path=pathlib.Path(a.game).resolve() if a.game else None)
    kills = sum(1 for r in allr if r["reason"] == "slain")
    cold = sum(1 for r in allr
               if r["reason"] == "slain"
               and (r.get("tOpen") is None or r["tOpen"] > a.max_open))
    print(f"# {a.a} vs {a.b}: {a.n} seeds, {kills} ended in a kill, "
          f"{cold} rejected for opening later than {a.max_open}s")
    for r in best:
        print(f"  seed {r['seed']:>10}  score {r['score']:>6}  {r['duration']:>5}s  "
              f"winner {r['winner']:<13} hp {r['hp']:<4} clanks {r['clanks']:<3} "
              f"hits {r['hits']['a']}/{r['hits']['b']}  [{r['why']}]")
    print(json.dumps(best[0], indent=1))


if __name__ == "__main__":
    main()
