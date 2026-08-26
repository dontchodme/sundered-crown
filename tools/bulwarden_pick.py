#!/usr/bin/env python3
"""WHICH FIGHT IS WORTH FILMING. Aegis needs a specific kind of fight.

    python3 bulwarden_pick.py --game ../02-chain/sc-bulwarden-frame.html

A relic whose ultimate is a WALL is invisible in a fight where nothing arrives
at it. So this does not score on drama in general -- it scores on whether the
thing the relic does actually happened on screen:

    at least two casts        the 3.9s revolution and the tracking need time
    blocks on the wall        an unblocked cast is a shield nobody tested
    at least one BREAK        the wall failing is the only ending that makes a
                              noise, and a clip of walls timing out is a clip
                              of nothing ending
    a close finish            under 22% of a bar between them at the end
    35-50s                    long enough to hold a cast, short enough to post

Writes nothing. Reports the shortlist and the seed.
"""
from __future__ import annotations
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
RID = "bulwarden"

JS = r"""([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let blocks = 0;
    const orig = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
      const A = foe2 === me ? me.ultAegis : null;
      const a0 = A ? A.ate : 0;
      const r = orig.call(m, self, foe2, hx, hy, seg, mul, over);
      if (A && A.ate > a0) blocks++;
      return r;
    };
    let s = 0, prev = null, casts = 0, breaks = 0, eaten = 0, back = 0;
    while (!m.over && s < secs / DT){
      m.step(DT); s++;
      const A = me.ultAegis;
      if (A && A !== prev) casts++;
      if (prev && prev !== A){ eaten += prev.ate; back += prev.back; if (prev.hp <= 0) breaks++; }
      prev = A;
    }
    if (prev){ eaten += prev.ate; back += prev.back; if (prev.hp <= 0) breaks++; }
    out.push({ foe: f, seed: sd, dur: s * DT, win: m.winner === me ? 1 : 0,
               casts, blocks, breaks, eaten: Math.round(eaten),
               back: Math.round(back),
               margin: Math.abs(me.hp - th.hp) / me.maxHp,
               meHp: Math.round(me.hp), thHp: Math.round(th.hp),
               foeUlts: th.ultsCast || 0 });
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--foes", default="emberedge,redflail,foregone,twinshade,ironhail,nightfell")
    ap.add_argument("--n", type=int, default=90)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--top", type=int, default=12)
    a = ap.parse_args()
    foes = a.foes.split(",")
    seeds = [7717 + 31 * i for i in range(a.n)]
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        rows = page.evaluate(JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]

    def score(r):
        if not r["win"] or r["breaks"] < 1 or r["casts"] < 2:
            return -1
        if not (33 <= r["dur"] <= 52):
            return -1
        return (r["blocks"] * 2 + r["breaks"] * 3 + r["back"] / 12
                + max(0, 0.22 - r["margin"]) * 30)

    ranked = sorted(rows, key=score, reverse=True)

    # THE DIRECTOR HAS THE LAST WORD, and it does not always agree with the
    # simulation. `cinePlan` scores a killing blow and then does not always
    # promote it to a CUT -- and when it does not, `cinema_clip` falls back to
    # "the last cut", which on one seed this session was 1.7 seconds into a
    # 42-second fight. A clip with no ending is not a clip. So the shortlist is
    # re-checked against the PLAN before anything is rendered.
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        for r in ranked[:40]:
            if score(r) < 0:
                break
            pl = page.evaluate(
                "([a,b,s]) => { const p = cinePlan(a,b,s);"
                " return {cuts: p.cuts.length,"
                "         fatal: p.cuts.filter(c=>c.fatal).length}; }",
                [RID, r["foe"], r["seed"]])
            r["planCuts"] = pl["cuts"]
            r["planKill"] = pl["fatal"]
        assert not errors, errors[:3]
    ranked = [r for r in ranked if r.get("planKill")]
    print(f"\n{len(rows)} fights, {len(foes)} foes x {a.n} seeds\n")
    print(f"  {'foe':<14}{'seed':>8}{'dur':>7}{'casts':>7}{'blocks':>8}"
          f"{'breaks':>8}{'eaten':>7}{'back':>6}{'end':>12}{'cuts':>6}"
          f"{'score':>8}")
    for r in ranked[:a.top]:
        if score(r) < 0:
            break
        print(f"  {r['foe']:<14}{r['seed']:>8}{r['dur']:>7.1f}{r['casts']:>7}"
              f"{r['blocks']:>8}{r['breaks']:>8}{r['eaten']:>7}{r['back']:>6}"
              f"{str(r['meHp']) + ' v ' + str(r['thHp']):>12}"
              f"{r.get('planCuts', 0):>6}{score(r):>8.1f}")
    ok = [r for r in rows if score(r) > 0]
    print(f"\n  {len(ok)} of {len(rows)} fights qualify on the simulation "
          f"(won, 2+ casts, a break, 33-52s);\n  {len(ranked)} of the top 40 "
          f"also carry a KILL CUT in the director's own plan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
