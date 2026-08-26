#!/usr/bin/env python3
"""WHAT BLADE DOES LASTLIGHT WANT? One relic, swept, against the whole field.

    python3 lastlight_sweep.py --blades 31.35,24,20,17 --n 40

`verify.py --n 60` put the placeholder blade at 71.0% — 21pp clear of the
field, which is far outside its 1.7pp standard error, so the DIRECTION is
unambiguous even though that tool cannot rank a flat field. This narrows the
number without paying for a 9180-match verify per candidate: it plays
Lastlight against all seventeen foes at PINNED seeds and reports one winrate.

WHY PINNED SEEDS AND NOT `batch()`. The engine's own `batch` draws its seeds
from `Math.random()`, so two candidate blades would be measured on two
different populations and a 2pp difference between them would be unreadable.
Every candidate here sees the SAME seed set, so the comparison is paired and
the difference is the blade.

WHAT THIS CANNOT DO. It measures Lastlight against the field. It cannot see
what Lastlight does to the SHAPE of the field — whether lowering the blade
pushes some third relic around — and only a full `verify.py` answers that.
Narrow here, confirm there.
"""
from __future__ import annotations
import argparse, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

SWEEP_JS = """([id, foes, seeds]) => {
  const rows = [];
  let wins = 0, total = 0, durs = [], casts = 0, blades = 0;
  for (const foe of foes){
    let w = 0;
    for (const s of seeds){
      const m = new AC.Match(id, foe, s);
      const dt = AC.CONFIG.physics.dt;
      let g = 0;
      while (!m.over && g++ < 200000) m.step(dt);
      const me = m.a.w.id === id ? m.a : m.b;
      if (m.winner === me) w++;
      durs.push(m.t);
      casts += me.ultsFired;
    }
    rows.push({ foe, w, n: seeds.length });
    wins += w; total += seeds.length;
  }
  durs.sort((x, y) => x - y);
  return { wins, total, rows,
           medDur: +durs[durs.length >> 1].toFixed(1), casts };
}"""


def measure(path, foes, seeds):
    with game(game_path=path.resolve()) as (page, errs):
        r = page.evaluate(SWEEP_JS, ["lastlight", foes, seeds])
        if errs:
            sys.exit(f"page errors: {errs[:2]}")
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--blades", default="31.35,24,20,17")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--keep", default=None, help="rebuild this blade at the end")
    a = ap.parse_args()

    foes = ["dawnbringer", "widowmaker", "grudgebearer", "thornwake",
            "gravemourn", "slagheart", "spellbreaker", "ironhail",
            "lightkeeper", "farwarden", "aureole", "censer", "emberedge",
            "oathwound", "heartwood", "nightfell", "axiom"]
    seeds = [7_000_003 + i * 104729 for i in range(a.n)]
    tmp = HERE.parent / "02-chain" / "sc-llsweep.html"

    print(f"=== Lastlight blade sweep — {len(foes)} foes x {a.n} pinned seeds "
          f"= {len(foes)*a.n} matches per candidate ===\n")
    print(f"{'blade':>8}{'winrate':>10}{'median dur':>12}{'ults':>7}   worst / best matchup")
    best = None
    for b in [float(x) for x in a.blades.split(",")]:
        tmp.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(HERE / "lastlight_build.py"),
                        "--src", a.src, "--out", "sc-llsweep.html",
                        "--blade", str(b)], check=True,
                       stdout=subprocess.DEVNULL)
        r = measure(tmp, foes, seeds)
        wr = r["wins"] / r["total"]
        rows = sorted(r["rows"], key=lambda x: x["w"])
        print(f"{b:>8.2f}{wr*100:>9.1f}%{r['medDur']:>11.1f}s"
              f"{r['casts']:>7}   {rows[0]['foe']} {rows[0]['w']}/{a.n}"
              f"  ·  {rows[-1]['foe']} {rows[-1]['w']}/{a.n}")
        if best is None or abs(wr - 0.50) < abs(best[1] - 0.50):
            best = (b, wr)
    tmp.unlink(missing_ok=True)
    print(f"\nclosest to 50%: blade {best[0]} at {best[1]*100:.1f}%")
    print("NOTE: this measures Lastlight against the field, not the field's "
          "own shape. Confirm with verify.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
