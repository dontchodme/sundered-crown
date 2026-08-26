#!/usr/bin/env python3
"""FOREGONE'S THREE KNOBS, SWEPT — and which one the relic is made of.

    python3 foregone_sweep.py --game ../02-chain/sc-foregone.html

Three knobs, and they are not interchangeable:

    w.dmg           the blade. The type's own is Thornwake's 31.35 against
                    Lastlight's 17.5, and runic already carries the two lowest
                    blades in the game (Axiom 7.42, Spellbreaker 8.81) as the
                    price of hex.
    ult.bloomDmg    the reversal. Twelve of them inside a second, and the only
                    thing in the ultimate that applies the status.
    ult.orbDmg      the wait. Up to sixty rings over four seconds, and the
                    payload is QUADRATIC in `lay` -- a sigil laid at t=0 pulses
                    seven times and one laid at t=3.6 pulses once.

Sweeping only `dmg` would answer "how far down does the blade go", and that is
the wrong question. If the answer is "far below both other scythes", this is
not a scythe with an ultimate, it is an ultimate with a scythe attached — which
is a legitimate shape (Lastlight is exactly that, 17.5 against Thornwake's
31.35) but it has to be arrived at deliberately and paid for in the blade.

PINNED SEEDS. Every candidate sees the same fights, so a difference between two
rows is the candidate and not the draw.

THE RUNTIME OVERRIDE IS CHECKED AGAINST A REAL REBUILD (`--verify-override`).
v37 and v38 both did this and both found it sound; an instrument standing in
for another instrument is a guess with a table around it until it is compared.

Writes nothing.
"""
from __future__ import annotations

import argparse
import pathlib
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "foregone"

RUN_JS = """([id, dmg, bloom, orb, seeds]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const d0 = w.dmg, b0 = w.ult.bloomDmg, o0 = w.ult.orbDmg;
  if (dmg !== null) w.dmg = dmg;
  if (bloom !== null) w.ult.bloomDmg = bloom;
  if (orb !== null) w.ult.orbDmg = orb;
  const DT = AC.CONFIG.physics.dt;
  const foes = AC.WEAPONS.map(x => x.id).filter(x => x !== id);
  let wins = 0, games = 0, to = 0, ults = 0;
  const durs = [];
  for (const f of foes){
    for (const s of seeds){
      const m = new AC.Match(id, f, s);
      const me = m.a.w.id === id ? m.a : m.b;
      let n = 0;
      while (!m.over && n < 120 / DT){ m.step(DT); n++; }
      games++;
      if (!m.over) to++;
      durs.push(n * DT);
      ults += me.ultsFired;
      if (m.winner && m.winner.w.id === id) wins++;
    }
  }
  w.dmg = d0; w.ult.bloomDmg = b0; w.ult.orbDmg = o0;
  durs.sort((x, y) => x - y);
  return { win: wins / games, games, to, ults: ults / games,
           dur: durs.reduce((a, b) => a + b, 0) / durs.length,
           p50: durs[Math.floor(durs.length / 2)] };
}"""

# The whole roster at a candidate, so the relic is priced against the field
# rather than against a handful of foes -- and so the SPREAD is visible, which
# is the number verify.py's band check actually reads.
FIELD_JS = """([seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const ids = AC.WEAPONS.map(x => x.id);
  const w = {}, g = {};
  for (const i of ids){ w[i] = 0; g[i] = 0; }
  let to = 0, n = 0, sum = 0;
  for (let a = 0; a < ids.length; a++)
    for (let b = a + 1; b < ids.length; b++)
      for (const s of seeds){
        const m = new AC.Match(ids[a], ids[b], s);
        let k = 0;
        while (!m.over && k < 120 / DT){ m.step(DT); k++; }
        if (!m.over) to++;
        n++; sum += k * DT;
        g[ids[a]]++; g[ids[b]]++;
        if (m.winner) w[m.winner.w.id]++;
      }
  const out = {};
  for (const i of ids) out[i] = g[i] ? w[i] / g[i] : 0;
  return { win: out, to, n, meanDur: sum / n };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-foregone.html")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--dmg", default="31.35,26,22,18,17.5,15,14,12")
    ap.add_argument("--bloom", default="9")
    ap.add_argument("--orb", default="2")
    ap.add_argument("--field", type=float, default=None,
                    help="dmg to run the whole 21-relic roster at")
    ap.add_argument("--verify-override", type=float, default=None,
                    help="rebuild at this dmg and compare to the override")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [7001 + 13 * i for i in range(a.n)]
    dmgs = [float(x) for x in a.dmg.split(",")] if a.dmg else [None]
    blooms = [float(x) for x in a.bloom.split(",")] if a.bloom else [None]
    orbs = [float(x) for x in a.orb.split(",")] if a.orb else [None]

    with game(game_path=gp) as (page, errors):
        base = page.evaluate(
            "() => { const w = AC.WEAPONS.find(x => x.id === '%s'); "
            "return { dmg: w.dmg, bloom: w.ult.bloomDmg, orb: w.ult.orbDmg }; }"
            % RID)
        n_foes = page.evaluate("() => AC.WEAPONS.length") - 1
        print(f"\nFOREGONE SWEEP — {n_foes} foes x {a.n} pinned seeds = "
              f"{n_foes * a.n} matches a candidate")
        print(f"  build carries dmg {base['dmg']}  bloomDmg {base['bloom']}  "
              f"orbDmg {base['orb']}\n")

        if a.field is not None:
            f = page.evaluate(RUN_JS, [RID, a.field, None, None, seeds[:1]])
            r = page.evaluate(FIELD_JS, [seeds[:max(1, a.n // 4)]])
            ws = sorted(r["win"].items(), key=lambda kv: kv[1])
            print(f"  WHOLE ROSTER at dmg {a.field}, {r['n']} matches, "
                  f"{r['to']} timeouts, mean {r['meanDur']:.1f}s")
            print(f"    spread {(ws[-1][1] - ws[0][1]) * 100:.1f}pp   "
                  f"{ws[0][0]} {ws[0][1]:.1%} .. {ws[-1][0]} {ws[-1][1]:.1%}")
            print(f"    {RID} {r['win'][RID]:.1%}")
            return 0

        print(f"  {'dmg':>7}{'bloom':>7}{'orb':>6}{'win':>8}{'ults':>7}"
              f"{'mean':>8}{'p50':>7}{'t/o':>5}")
        rows = []
        for o in orbs:
            for b in blooms:
                for d in dmgs:
                    r = page.evaluate(RUN_JS, [RID, d, b, o, seeds])
                    rows.append((d, b, o, r))
                    print(f"  {d:>7}{b:>7}{o:>6}{r['win']:>8.1%}"
                          f"{r['ults']:>7.2f}{r['dur']:>8.1f}s"
                          f"{r['p50']:>6.1f}s{r['to']:>5}")
        se = (0.25 / (n_foes * a.n)) ** 0.5
        print(f"\n  SE on a winrate here is about {se * 100:.1f}pp, so two rows "
              f"inside {se * 200:.1f}pp are one row.")
        near = [x for x in rows if abs(x[3]["win"] - 0.5) < 0.06]
        if near:
            print(f"  inside 44-56%: "
                  + ", ".join(f"dmg {x[0]:g}/bloom {x[1]:g} "
                              f"({x[3]['win']:.1%})" for x in near))
        print("\n  A column that only reaches 50% far below both other scythes")
        print("  is not a tuned scythe, it is an ultimate with a scythe")
        print("  attached. Lastlight IS that and pays 17.5 against 31.35 — the")
        print("  shape is legitimate, but it has to be chosen, not defaulted.")
        assert not errors, errors[:4]

    if a.verify_override is not None:
        d = a.verify_override
        out = HERE / f"../02-chain/_sweepcheck-{d:g}.html"
        print(f"\n  REBUILD CHECK at dmg {d:g} — an override standing in for a")
        print( "  build is a guess with a table around it until it is compared.")
        subprocess.run([sys.executable, "foregone_build.py",
                        "--out", str(out), "--dmg", str(d)],
                       cwd=HERE, check=True, capture_output=True)
        with game(game_path=out.resolve()) as (p2, e2):
            real = p2.evaluate(RUN_JS, [RID, None, None, None, seeds])
            assert not e2, e2[:3]
        with game(game_path=gp) as (p3, e3):
            over = p3.evaluate(RUN_JS, [RID, d, None, None, seeds])
            assert not e3, e3[:3]
        same = (abs(real["win"] - over["win"]) < 1e-12
                and abs(real["dur"] - over["dur"]) < 1e-9
                and real["games"] == over["games"])
        print(f"    rebuilt  {real['win']:.4%}  mean {real['dur']:.4f}s "
              f"({real['games']} matches)")
        print(f"    override {over['win']:.4%}  mean {over['dur']:.4f}s")
        print(f"    {'PASS' if same else 'FAIL'} — "
              f"{'identical' if same else 'THE OVERRIDE IS NOT THE BUILD'}")
        out.unlink(missing_ok=True)
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
