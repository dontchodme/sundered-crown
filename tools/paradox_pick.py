#!/usr/bin/env python3
"""WHICH FIGHT IS WORTH FILMING — scored on the DIRECTOR'S PLAN, not only on
   the relic's own telemetry.

    python3 paradox_pick.py --game ../02-chain/sc-paradox-pace.html

v41 lost two renders to seeds whose plan carried no FATAL cut, and v42 closed
that by asking `window.cinePlan` before offering a seed rather than after a
render. Same rule here, and this relic needs it more than either of them: the
Stasis Field deals NO DAMAGE. Nothing about a hold is a hit, so a fight can be
a perfect demonstration of the mechanic and still end on something the camera
was never told about.

The relic's own criteria, because a hold is invisible in a fight where the
window never opens:

    two casts          the window is 9s and the charge is 16; one cast is an
                       anecdote
    two holds          one hold is luck. The charge fills at 1/s inside a
                       hexagon the quarry crosses 46 times a minute, and the
                       whole design question was whether that ever fires
    blows ON a hold    the entire mechanical claim. A hold nobody capitalises
                       on is a two-second pause, and the reason this relic
                       exists is that its live blade is 13 units long
    a close finish     under 22% of a bar between them
    30-55s             long enough to hold two windows and their holds

Writes nothing. Reports the shortlist and the seed.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "paradox"

TEL_JS = r"""([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;

    let hitsHeld = 0, dHeld = 0, killedHeld = 0;
    const oRes = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
      const held = f2.pin > 0, before = self.dealt;
      const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
      if (self === me && held && !f2.shade){
        hitsHeld++; dHeld += self.dealt - before;
        if (!f2.alive) killedHeld++;
      }
      return r;
    };

    let n = 0, casts = 0, wasUp = false, holds = 0, p0 = 0, heldFrames = 0;
    let lastHold = -1;
    while (!m.over && n < secs / DT){
      m.step(DT); n++;
      const F = me.ultField;
      if (F && !wasUp) casts++;
      wasUp = !!F;
      if (th.pin > 0){ heldFrames++; if (p0 <= 0){ holds++; lastHold = n; } }
      p0 = th.pin;
    }
    out.push({ foe: f, seed: sd, dur: +(n * DT).toFixed(1),
               win: m.winner === me ? 1 : 0, casts, holds,
               hitsHeld, dHeld: Math.round(dHeld), killedHeld,
               heldFrac: +(heldFrames / Math.max(1, n)).toFixed(3),
               lastHoldT: lastHold > 0 ? +(lastHold * DT).toFixed(1) : -1,
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
    ap.add_argument("--game", default="../02-chain/sc-paradox-pace.html")
    ap.add_argument("--foes", default="heartwood,grudgebearer,twinshade,"
                                      "lastlight,widowmaker,slagheart,"
                                      "dawnbringer,marrowdraw")
    ap.add_argument("--n", type=int, default=14)
    ap.add_argument("--seed0", type=int, default=7300)
    ap.add_argument("--secs", type=float, default=95.0)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-holds", type=int, default=2)
    ap.add_argument("--margin", type=float, default=0.30)
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    foes = a.foes.split(",")
    seeds = [a.seed0 + i * 331 for i in range(a.n)]

    with game(game_path=gp) as (page, errors):
        rows = page.evaluate(TEL_JS, [RID, foes, seeds, a.secs])
        cand = [r for r in rows
                if r["win"] and r["casts"] >= 2 and r["holds"] >= a.min_holds
                and r["hitsHeld"] >= 2 and r["margin"] <= a.margin
                and 28.0 <= r["dur"] <= 58.0]
        print(f"\n  {len(rows)} fights scanned, {len(cand)} clear the relic bar")
        # A FATAL CUT IS RARE FOR EVERY MELEE RELIC IN THIS GAME, AND THAT IS
        # MEASURED RATHER THAN ASSUMED. Over 48 fights each, on the same foes
        # and seeds: axiom 23%, gravemourn 23%, redflail 19%, PARADOX 12%,
        # thornwake 10%, foregone 8%. So a shortlist of ten is a shortlist of
        # about one, and the widening below is not laziness -- it is the rate.
        for r in cand:
            r["plan"] = page.evaluate(PLAN_JS, [RID, r["foe"], r["seed"]])
        assert not errors, errors[:3]

    ok = [r for r in cand if r["plan"].get("kill")]
    no = [r for r in cand if not r["plan"].get("kill")]
    print(f"  {len(ok)} of those carry a FATAL cut in the director's plan; "
          f"{len(no)} do NOT and are rejected here rather than after a render")
    for r in no[:4]:
        print(f"      rejected  {r['foe']:<13} seed {r['seed']:<6} "
              f"{r['dur']:>5.1f}s  {r['plan'].get('cuts', 0)} cuts, no KILL")

    # A HOLD LATE IN THE FIGHT IS WORTH MORE THAN A HOLD EARLY, because the
    # director's own tiers already weight the end and a clip that shows the
    # mechanic and then runs three quiet windows reads as a fight the ultimate
    # was not in.
    ok.sort(key=lambda r: (-r["killedHeld"], -(r["dHeld"]),
                           -(r["lastHoldT"] / max(1, r["dur"])), r["margin"]))
    print(f"\n  {'foe':<14}{'seed':>7}{'dur':>7}{'casts':>7}{'holds':>7}"
          f"{'hits held':>11}{'dmg':>7}{'held':>7}{'last':>7}{'margin':>8}"
          f"{'cuts':>6}{'kill@':>7}   why")
    for r in ok[:a.top]:
        p = r["plan"]
        tail = "  <- the hold lands the last blow" if r["killedHeld"] else ""
        print(f"  {r['foe']:<14}{r['seed']:>7}{r['dur']:>7.1f}{r['casts']:>7}"
              f"{r['holds']:>7}{r['hitsHeld']:>11}{r['dHeld']:>7}"
              f"{r['heldFrac']:>7.1%}{r['lastHoldT']:>7.1f}{r['margin']:>8.2f}"
              f"{p['cuts']:>6}{p['killT']:>7}   {p['why'][:30]}{tail}")
    if ok:
        b = ok[0]
        print(f"\n  PICK: --a {RID} --b {b['foe']} --seed {b['seed']}"
              f"   ({b['dur']:.1f}s, {b['casts']} casts, {b['holds']} holds, "
              f"{b['hitsHeld']} blows landed on a held quarry for "
              f"{b['dHeld']}, {b['meHp']} v {b['thHp']})")
    else:
        print("\n  NOTHING QUALIFIES — widen --n or --foes, or lower --min-holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
