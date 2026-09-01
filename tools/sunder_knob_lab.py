#!/usr/bin/env python3
"""WHAT THE TWO SUNDER KNOBS ARE WORTH ON A SCYTHE, before a §1 exists.

    python3 sunder_knob_lab.py --game ../02-chain/sc-nightfell.html

`sunder_survey` established that sunder's 5.0s duration cuts the roster in
half at the blow interval, and that the scythe sits just over the line: 5.24s
between blows, 1.23 stacks at the moment of a blow, cap reached in 21% of
fights against 78-89% for the three fast types.

There are exactly two ways an ultimate can move a relic back across that line,
and this prices both BEFORE anything is designed around either:

  APPLY MORE   onHit sunder:n. Donor only — clean, no confound.
  HOLD LONGER  STATUS.sunder.dur. GLOBAL, so the four dwarven foes get it too;
               this arm therefore UNDERSTATES the relic-only value and its
               numbers are a floor, not an estimate. dur 99 is the ceiling
               arm: a stack that never decays at all.

Both are arms of a lab, not proposals. Injection is runtime-only. NOTHING is
written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


ARM_JS = r"""([donor, foes, seeds, secs, n, dur]) => {
  const DT = AC.CONFIG.physics.dt;
  const W  = AC.WEAPONS;
  const w  = W.find(x => x.id === donor);
  const saved = { aff: w.aff,
                  onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
                  onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  const savedDur = AC.STATUS.sunder.dur;
  w.aff = "dwarven";
  delete w.onHit; delete w.onSelf;
  if (n > 0) w.onHit = { sunder: n };
  if (dur !== null) AC.STATUS.sunder.dur = dur;

  const savedUlt = {};
  for (const x of W) if (x.ult) { savedUlt[x.id] = x.ult.charge; x.ult.charge = 1e9; }

  const probe = new AC.Match(donor, foes[0], 1);
  const F = Object.getPrototypeOf(probe.a);
  const origMul = F.dmgTakenMul;
  let LOG = null;
  F.dmgTakenMul = function () {
    const v = origMul.call(this);
    if (LOG && this.side === LOG.foeSide) { LOG.mul.push(v); LOG.stk.push(this.stacks("sunder")); }
    return v;
  };

  const rows = [];
  try {
    for (const f of foes) for (const s of seeds) {
      const m  = new AC.Match(donor, f, s);
      const me = m.a.w.id === donor ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      LOG = { foeSide: th.side, mul: [], stk: [] };
      let steps = 0;
      while (!m.over && steps < secs / DT) { m.step(DT); steps++; }
      const cap = AC.STATUS.sunder.maxStacks;
      rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  dealt: me.dealt, dur: steps * DT, events: LOG.mul.length,
                  meanMul: LOG.mul.length ? LOG.mul.reduce((a,b)=>a+b,0)/LOG.mul.length : 1,
                  stk: LOG.stk.length ? LOG.stk.reduce((a,b)=>a+b,0)/LOG.stk.length : 0,
                  zero: LOG.stk.length ? LOG.stk.filter(x=>x===0).length/LOG.stk.length : 0,
                  capS: LOG.stk.length ? LOG.stk.filter(x=>x>=cap).length/LOG.stk.length : 0 });
    }
  } finally {
    F.dmgTakenMul = origMul;
    AC.STATUS.sunder.dur = savedDur;
    w.aff = saved.aff;
    delete w.onHit; delete w.onSelf;
    if (saved.onHit)  w.onHit  = saved.onHit;
    if (saved.onSelf) w.onSelf = saved.onSelf;
    for (const x of W) if (x.ult && savedUlt[x.id] !== undefined) x.ult.charge = savedUlt[x.id];
  }
  return rows;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--donor", default="thornwake")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [2207 + 11 * i for i in range(a.seeds)]

    arms = [("no channel at all", 0, None),
            ("apply 1  (shipped)", 1, None),
            ("apply 2  (Slagheart's)", 2, None),
            ("apply 3", 3, None),
            ("hold 7.0s", 1, 7.0),
            ("hold 10.0s", 1, 10.0),
            ("hold forever (ceiling)", 1, 99.0)]

    out = {}
    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != a.donor]
        print(f"\nDONOR {a.donor} — {len(foes)} foes x {len(seeds)} seeds "
              f"= {len(foes)*len(seeds)} fights an arm, ultimates suppressed\n")
        print(f"    {'arm':<26}{'blows':>7}{'stk@blow':>10}{'0 stk':>7}"
              f"{'6 stk':>7}{'meanMul':>9}{'dealt':>8}{'win':>8}{'lift':>8}")
        base = None
        for name, n, dur in arms:
            rows = page.evaluate(ARM_JS, [a.donor, foes, seeds, a.secs, n, dur])
            fin = [r for r in rows if r["win"] >= 0]
            rec = {"blows": mean(r["events"] for r in rows),
                   "stk": mean(r["stk"] for r in rows),
                   "zero": mean(r["zero"] for r in rows),
                   "cap": mean(r["capS"] for r in rows),
                   "mul": mean(r["meanMul"] for r in rows),
                   "dealt": mean(r["dealt"] for r in rows),
                   "win": mean(r["win"] for r in fin)}
            if base is None:
                base = rec["win"]
            rec["lift"] = rec["win"] - base
            out[name] = rec
            print(f"    {name:<26}{rec['blows']:>7.1f}{rec['stk']:>10.2f}"
                  f"{rec['zero']:>7.0%}{rec['cap']:>7.0%}{rec['mul']:>9.3f}"
                  f"{rec['dealt']:>8.0f}{rec['win']:>8.1%}{rec['lift']:>+8.1%}")

        a1 = out["apply 1  (shipped)"]
        check("applying more stacks moves the stack count",
              out["apply 3"]["stk"] > a1["stk"] * 1.3,
              f"1 -> {a1['stk']:.2f}, 3 -> {out['apply 3']['stk']:.2f}")
        check("holding the stack moves it further than applying more does",
              out["hold forever (ceiling)"]["stk"] > out["apply 3"]["stk"],
              f"apply 3 -> {out['apply 3']['stk']:.2f}, "
              f"hold forever -> {out['hold forever (ceiling)']['stk']:.2f}")
        check("a scythe carrying an undecaying stack reaches the cap the way "
              "a fast type does",
              out["hold forever (ceiling)"]["cap"] > 0.5,
              f"{out['hold forever (ceiling)']['cap']:.0%} of blows at 6 stacks "
              f"(shipped scythe: {a1['cap']:.0%}; fast types: 15-26%)")
        check("no JS errors or page exceptions", not errors, "; ".join(errors[:3]))

    n_ok = sum(1 for _, ok in PASS if ok)
    print(f"\n{n_ok}/{len(PASS)} checks passed"
          + ("" if n_ok == len(PASS) else f"  ({len(PASS)-n_ok} FAILED)"))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
