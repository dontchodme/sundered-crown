#!/usr/bin/env python3
"""WHICH FIGHT IS WORTH FILMING — scored on the DIRECTOR'S PLAN, not only on
   the relic's own telemetry.

    python3 marrowdraw_pick.py --game ../02-chain/sc-marrowdraw-frame.html

**THIS CLOSES v41 OPEN DECISION 6.** `bulwarden_pick` scored fights on what the
relic did and then handed the seed to `cinema_clip`, which planned the fight
independently -- and on seeds 9732 and 8430 the plan scored a killing blow
whose `why` read "the killing blow" and then did not cut to it, so the clip
tool fell back to the last cut and wrote a fight with no ending. That cost v41
two renders. A pick tool that never asks the director what it intends to do
cannot see it coming.

So every candidate here is run through `window.cinePlan` and **a seed with no
FATAL cut in its plan is rejected before it is ever offered**, however good the
fight was.

The relic's own criteria, because a hunting bolt is invisible in a fight where
the window never opens:

    two casts          the window is 8s and the charge is 15; one cast is an
                       anecdote
    bolts that LAND    the pierce is the moment, and a bolt that walls is the
                       thing this ultimate exists to stop doing
    a fork that CONNECTS   the second half of §1, and the half a viewer has to
                       be shown to believe
    a bolt BATTED      the counterplay on screen — "can be clanked, nullifying
                       the fork" is a sentence, and an unclanked window never
                       says it
    a close finish     under 22% of a bar between them
    30-50s             long enough to hold two windows

Writes nothing. Reports the shortlist and the seed.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "marrowdraw"

TEL_JS = r"""([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const side = me === m.a ? "a" : "b";
    let boltHits = 0, forkHits = 0, killedByBolt = 0, killedByFork = 0;
    const oRes = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
      const s = m._cineShot;
      const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
      if (s && self === me){
        if (s.fork){ forkHits++; if (!f2.alive) killedByFork++; }
        else if (s.bal){ boltHits++; if (!f2.alive) killedByBolt++; }
      }
      return r;
    };
    let inShots = false, batted = 0;
    const P = [];
    const oFx = AC.Match.prototype.spawnFx;
    m.spawnFx = function(x, y, c2, n2, spd, l, sz, dx, dy){
      if (inShots && c2 === "#FFF4D0" && n2 === 9 && spd === 240) P.push(x + "," + y);
      return oFx.call(m, x, y, c2, n2, spd, l, sz, dx, dy);
    };
    const oTick = AC.Match.prototype.tickShots;
    m.tickShots = function(dt){
      const pre = m.shots.slice(); P.length = 0; inShots = true;
      const r = oTick.call(m, dt); inShots = false;
      const live = new Set(m.shots), S = new Set(P);
      for (const s of pre)
        if (!live.has(s) && s.own === side && s.bal && S.has(s.x + "," + s.y)) batted++;
      return r;
    };
    let n = 0, casts = 0, wasUp = false, bolts = 0;
    while (!m.over && n < secs / DT){
      m.step(DT); n++;
      const B = me.ultBal;
      if (B && !wasUp) casts++;
      if (B) bolts = Math.max(bolts, B.bolts);
      wasUp = !!B;
    }
    out.push({ foe: f, seed: sd, dur: +(n * DT).toFixed(1),
               win: m.winner === me ? 1 : 0, casts, boltHits, forkHits,
               batted, killedByBolt, killedByFork,
               margin: +(Math.abs(me.hp - th.hp) / me.maxHp).toFixed(3),
               meHp: Math.round(Math.max(0, me.hp)),
               thHp: Math.round(Math.max(0, th.hp)) });
  }
  return out;
}"""

PLAN_JS = """([a, b, s]) => {
  const p = window.cinePlan(a, b, s);
  if (p.err) return { err: String(p.err) };
  const kill = p.cuts.find(c => c.fatal);
  return { dur: +p.dur.toFixed(1), cuts: p.cuts.length, kill: !!kill,
           killT: kill ? +kill.t.toFixed(1) : null,
           tiers: p.cuts.map(c => c.fatal ? "KILL" : "T" + c.tier).join(" "),
           why: kill ? (kill.why || []).join(", ") : "" };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw-frame.html")
    ap.add_argument("--foes", default="thornwake,dawnbringer,grudgebearer,"
                                      "gravemourn,twinshade,heartwood,foregone")
    ap.add_argument("--n", type=int, default=14)
    ap.add_argument("--seed0", type=int, default=6100)
    ap.add_argument("--secs", type=float, default=95.0)
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    foes = a.foes.split(",")
    seeds = [a.seed0 + i * 331 for i in range(a.n)]

    with game(game_path=gp) as (page, errors):
        rows = page.evaluate(TEL_JS, [RID, foes, seeds, a.secs])
        # THE PLAN IS ASKED FOR EVERY CANDIDATE THAT PASSES THE RELIC BAR --
        # not only for the winner, because "the best fight" and "a fight the
        # director will cut to the end of" are different sets and v41 learned
        # that the expensive way.
        cand = [r for r in rows
                if r["win"] and r["casts"] >= 2 and r["boltHits"] >= 2
                and r["forkHits"] >= 1 and r["batted"] >= 1
                and 30.0 <= r["dur"] <= 50.0]
        print(f"\n  {len(rows)} fights scanned, {len(cand)} clear the relic bar")
        for r in cand:
            p = page.evaluate(PLAN_JS, [RID, r["foe"], r["seed"]])
            r["plan"] = p
        assert not errors, errors[:3]

    ok = [r for r in cand if r["plan"].get("kill")]
    no = [r for r in cand if not r["plan"].get("kill")]
    print(f"  {len(ok)} of those carry a FATAL cut in the director's plan; "
          f"{len(no)} do NOT and are rejected here rather than after a render")
    if no:
        for r in no[:4]:
            print(f"      rejected  {r['foe']:<13} seed {r['seed']:<6} "
                  f"{r['dur']:>5.1f}s  {r['plan'].get('cuts', 0)} cuts, no KILL")

    ok.sort(key=lambda r: (-(r["killedByBolt"] + r["killedByFork"]),
                           r["margin"], -r["forkHits"]))
    print(f"\n  {'foe':<14}{'seed':>7}{'dur':>7}{'casts':>7}{'bolts':>7}"
          f"{'forks':>7}{'batted':>8}{'margin':>8}{'cuts':>6}{'kill@':>7}   why")
    for r in ok[:a.top]:
        p = r["plan"]
        endsOnUlt = "  <- the window lands the last blow" if (
            r["killedByBolt"] or r["killedByFork"]) else ""
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['dur']:>7.1f}{r['casts']:>7}"
              f"{r['boltHits']:>7}{r['forkHits']:>7}{r['batted']:>8}"
              f"{r['margin']:>8.2f}{p['cuts']:>6}{p['killT']:>7}   "
              f"{p['why'][:36]}{endsOnUlt}")
    if ok:
        b = ok[0]
        print(f"\n  PICK: --a {RID} --b {b['foe']} --seed {b['seed']}"
              f"   ({b['dur']:.1f}s, {b['casts']} casts, {b['boltHits']} bolts "
              f"landed, {b['forkHits']} forks connected, {b['batted']} batted, "
              f"{b['meHp']} v {b['thHp']})")
    else:
        print("\n  NOTHING QUALIFIES — widen --n or --foes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
