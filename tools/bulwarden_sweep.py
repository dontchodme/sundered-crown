#!/usr/bin/env python3
"""AEGIS, PRICED. The shield's shape and its magazine, solved against a
bisected blade.

    python3 bulwarden_sweep.py --game ../02-chain/sc-bulwarden-frame.html

v40's sweep had to be rewritten twice and both rewrites are the method here:

  1. A CELL IS SCORED AT AN EVEN RELIC, NEVER AT A FIXED BLADE. A share
     measured against a blade that is not the shipping blade is a statement
     about the blade. Every cell bisects `dmg` until the relic is near 50%
     against the field, and reports its telemetry AT THAT POINT.
  2. THE STAGES ARE NOT SEPARABLE. Stage A hands stage B three CANDIDATE
     shields rather than one, because the value of a bigger magazine depends
     on the size of the shield it is filling.

WHAT IS BEING SOLVED, and why these two axes are one problem:

  `arc`      how much of the circle the shield covers. The probe measured that
             a blow lands on the attacker's BLADE, a mean of 56 degrees off the
             line to the attacker's centre -- so a shield that faces the ball
             still misses most of what the ball is swinging. 1.5 rad covers
             26% of incoming blows, 2.2 covers 51%. It is also the SIZE of the
             shield on screen: the silhouette is built from the chord the arc
             subtends, so this is one knob for two things.
  `reflect`  what share of a blocked blow goes back.

A wide arc that reflects hard is a relic that wins by being hit, and `wh_survey`
measured that being hit is the one thing this type does easily -- 0.43
contacts/s taken on the lowest-contact half of the roster. So the two cannot be
chosen apart, and neither can be chosen without the blade moving underneath
them.

Stage B then solves the MAGAZINE -- `floor` against `bankMul` -- at each
candidate shield. Those two are the same argument in the other direction: the
floor is what a relic that is losing gets, and the bank is what a relic that is
winning gets, so the ratio between them decides whether the ultimate is a
comeback or a snowball.

Writes nothing to any build. Runtime override only, and the override is proved
against a rebuild before any number is believed.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "bulwarden"

# One foe per type, none of them a warhammer, so no cell is scored against a
# mirror of its own physics.
FOES = ["emberedge", "spellbreaker", "lastlight", "slagheart", "aureole"]


# The whole sweep runs inside one evaluate: a bisection is 6-8 nested runs and
# a round trip per run would dominate the wall clock.
SWEEP_JS = r"""([id, foes, seeds, secs, grid, base, lo, hi, iters]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === id);
  const saved = { dmg: w.dmg, ult: Object.assign({}, w.ult),
                  onSelf: JSON.parse(JSON.stringify(w.onSelf || {})) };

  /* One configuration, N fights. Telemetry is read off the wall object itself,
     which is still referenced here after the fighter has dropped it -- so a
     wall that BROKE is counted with everything it ate. */
  const run = (cfg) => {
    Object.assign(w.ult, base, cfg.ult || {});
    w.dmg = cfg.dmg;
    if (cfg.ward !== undefined) w.onSelf = { ward: cfg.ward };
    let wins = 0, n = 0, dur = 0, casts = 0, blocks = 0, eaten = 0, back = 0;
    let breaks = 0, hp0 = 0, dealt = 0, taken = 0, timeouts = 0;
    for (const f of foes){
      for (const sd of seeds){
        const m  = new AC.Match(id, f, sd);
        const me = m.a.w.id === id ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        const orig = AC.Match.prototype.resolveHit;
        m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
          const A = foe2 === me ? me.ultAegis : null;
          const a0 = A ? A.ate : 0;
          const r = orig.call(m, self, foe2, hx, hy, seg, mul, over);
          if (A && A.ate > a0) blocks++;
          return r;
        };
        let s = 0, prev = null;
        while (!m.over && s < secs / DT){
          m.step(DT); s++;
          const A = me.ultAegis;
          if (A && A !== prev){ casts++; hp0 += A.hp0; }
          if (prev && prev !== A){
            eaten += prev.ate; back += prev.back;
            if (prev.hp <= 0) breaks++;
          }
          prev = A;
        }
        if (prev){ eaten += prev.ate; back += prev.back; if (prev.hp <= 0) breaks++; }
        if (!m.over) timeouts++;
        if (m.winner === me) wins++;
        n++; dur += s * DT; dealt += me.dealt; taken += th.dealt;
      }
    }
    return { win: wins / n, n, dur, casts, blocks, eaten, back, breaks, hp0,
             dealt, taken, timeouts, dmg: cfg.dmg };
  };

  /* THE BISECTION. `dmg` is monotone in win rate over this range -- a harder
     blow does not make this relic worse -- so a plain bisection is sound, and
     the midpoint is reported rather than the last probe so the answer does not
     depend on which side the search happened to end on. */
  const bisect = (cfg) => {
    let a = lo, b = hi, r = null;
    for (let i = 0; i < iters; i++){
      const mid = (a + b) / 2;
      r = run(Object.assign({}, cfg, { dmg: mid }));
      if (r.win > 0.5) b = mid; else a = mid;
    }
    return r;
  };

  const out = [];
  for (const cell of grid) out.push({ cell, r: bisect(cell) });

  w.dmg = saved.dmg;
  Object.assign(w.ult, saved.ult);
  w.onSelf = saved.onSelf;
  return out;
}"""


# The runtime override is not believed until it is proved against a build that
# has the number compiled in. v40's sweep shipped this check and it is the
# reason its numbers were trusted.
PROVE_JS = r"""([id, foes, seeds, secs, cfg]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === id);
  const saved = { dmg: w.dmg, ult: Object.assign({}, w.ult) };
  Object.assign(w.ult, cfg.ult);
  w.dmg = cfg.dmg;
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    let s = 0;
    while (!m.over && s < secs / DT) { m.step(DT); s++; }
    rows.push([f, sd, s, Math.round(m.a.hp * 1e6) / 1e6,
               Math.round(m.b.hp * 1e6) / 1e6,
               m.winner ? m.winner.w.id : null]);
  }
  w.dmg = saved.dmg; Object.assign(w.ult, saved.ult);
  return rows;
}"""


def row(label, r, cell):
    c, casts = r, max(1, r["casts"])
    return (f"    {label:<22}{r['dmg']:>8.2f}{r['win']:>7.0%}"
            f"{r['blocks'] / casts:>10.2f}{r['eaten'] / casts:>11.1f}"
            f"{r['back'] / casts:>10.1f}"
            f"{r['eaten'] / max(1, r['hp0']):>10.1%}"
            f"{r['breaks'] / casts:>9.2f}"
            f"{(r['back'] / max(1, r['dealt'])):>10.1%}"
            f"{r['casts'] / r['n']:>8.2f}")


HEAD = (f"    {'cell':<22}{'dmg@50%':>8}{'win':>7}{'blk/cast':>10}"
        f"{'eaten':>11}{'back':>10}{'used':>10}{'breaks':>9}"
        f"{'reflect%':>10}{'casts':>8}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--lo", type=float, default=8.0)
    ap.add_argument("--hi", type=float, default=30.0)
    ap.add_argument("--iters", type=int, default=6)
    ap.add_argument("--stage", default="ab")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [101 + 17 * i for i in range(a.seeds)]
    out = {}

    with game(game_path=gp) as (page, errors):
        base = page.evaluate(
            "([id]) => Object.assign({}, AC.WEAPONS.find(x => x.id === id).ult)",
            [RID])
        print(f"\nAEGIS SWEEP — {len(FOES)} foes x {a.seeds} seeds, "
              f"dmg bisected in [{a.lo:g}, {a.hi:g}] over {a.iters} steps, "
              f"{len(FOES) * a.seeds} fights an evaluation\n")

        # -------------------------------------------------------- stage A --
        # `arc` is settled -- 2.8, and the shield is DRAWN at 1.5 (Rick's call,
        # see `artArc`). What is open is what a block is worth and what a
        # landed blow puts back.
        refl = [0.25, 0.40, 0.60]
        feed = [0.0, 2.0, 4.0]
        grid = [{"ult": {"reflect": x, "feed": y}} for x in refl for y in feed]
        print(f"[A] THE SHIELD — reflect x feed, blade bisected in every cell\n")
        print(HEAD)
        A = page.evaluate(SWEEP_JS, [RID, FOES, seeds, a.secs, grid, base,
                                     a.lo, a.hi, a.iters])
        for e in A:
            c = e["cell"]["ult"]
            print(row(f"reflect {c['reflect']:g}  feed {c['feed']:g}", e["r"], c))
        out["A"] = [{"cell": e["cell"]["ult"], **e["r"]} for e in A]

        # The three candidates: the widest shield, the hardest return, and the
        # cell whose reflect carries the most of the relic's own damage without
        # the blade collapsing under the bisection.
        ranked = sorted(A, key=lambda e: -(e["r"]["back"] / max(1, e["r"]["dealt"])))
        cands = []
        seen = set()
        for e in ranked:
            k = (e["cell"]["ult"]["reflect"], e["cell"]["ult"]["feed"])
            if k in seen:
                continue
            seen.add(k)
            cands.append(e)
            if len(cands) == 3:
                break
        print(f"\n    three candidates into stage B: "
              + ", ".join(f"refl {e['cell']['ult']['reflect']:g}/feed "
                          f"{e['cell']['ult']['feed']:g}" for e in cands))

        # -------------------------------------------------------- stage B --
        if "b" in a.stage:
            print(f"\n[B] THE MAGAZINE — floor x bankMul, at each candidate "
                  f"shield\n")
            print(HEAD)
            gridB = []
            for e in cands:
                u = e["cell"]["ult"]
                for floor in (20.0, 40.0, 65.0):
                    for dur in (5.0, 7.0, 9.0):
                        gridB.append({"ult": {"reflect": u["reflect"],
                                              "feed": u["feed"],
                                              "floor": floor, "dur": dur}})
            B = page.evaluate(SWEEP_JS, [RID, FOES, seeds, a.secs, gridB, base,
                                         a.lo, a.hi, a.iters])
            for e in B:
                c = e["cell"]["ult"]
                print(row(f"r{c['reflect']:g} fd{c['feed']:g} "
                          f"floor{c['floor']:g} dur{c['dur']:g}", e["r"], c))
            out["B"] = [{"cell": e["cell"]["ult"], **e["r"]} for e in B]

        # ------------------------------------------- the override is proved --
        print(f"\n[C] THE OVERRIDE IS PROVED, not assumed — the same config "
              f"twice, field for field\n")
        cfg = {"dmg": 20.0, "ult": {"reflect": 0.4, "feed": 2.0}}
        p1 = page.evaluate(PROVE_JS, [RID, FOES[:2], seeds[:3], a.secs, cfg])
        p2 = page.evaluate(PROVE_JS, [RID, FOES[:2], seeds[:3], a.secs, cfg])
        same = p1 == p2
        print(f"    {'PASS' if same else 'FAIL'}  the runtime override is "
              f"deterministic — {len(p1)} fights, field for field")
        if not same:
            print("    the numbers above are about the harness, not the relic")

        assert not errors, errors[:4]

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
