#!/usr/bin/env python
"""THE BALANCE SWEEP (v117) -- each named relic's blade walked to its point nearest 50%, BOTH SIDES.

    python balance_sweep.py --game <scratch>/staves-on-tip.html --relics ironhail,widowmaker,... \
        [--n 10] [--blocks 2207,2317] [--tol 1.0] [--max 4] [--parallel 4] --out sweep.json

Rick, 2026-09-29: "you pick the blades. do whatevers best for balance." Measured on the roster the
game will carry (the batch line's tip with yert's staves carried onto it), with `relic_rate.py`: the
same seeds from both sides, on two seed blocks, pooled. Per relic:

  1. its current blade (read from the page's own WEAPONS row), measured;
  2. if the pooled rate is within --tol points of 50, it stays;
  3. otherwise a first step from the roster's typical sensitivity (about 0.4 points of win rate per 1%
     of blade, clamped to +-25%), then secants through the two nearest measured points, each rounded
     to a quarter; at most --max measurements;
  4. the pick is the MEASURED blade whose pooled rate is nearest 50 (never an interpolated number).

`--set dmg=` is relic_rate's live mutation of the relic's own row, put back after each run, so one
page state is measured throughout. This tool only measures; the picks' home is balance_build.py.
"""
from __future__ import annotations
import argparse, json, pathlib, re, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent
PY = sys.executable
LOCK = threading.Lock()


def current_blade(html: str, relic: str) -> float:
    m = re.search(r'\{ id:"' + re.escape(relic) + r'",.*?\bdmg:([0-9.]+)', html, re.S)
    if not m:
        raise SystemExit(f"no dmg for {relic} in the page")
    return float(m.group(1))


def measure(game: str, relic: str, blade: float, n: int, blocks, tmp: pathlib.Path) -> dict:
    wins = games = 0
    per = []
    for s0 in blocks:
        out = tmp / f"{relic}_{blade}_{s0}.json"
        r = subprocess.run([PY, str(HERE / "relic_rate.py"), "--game", game, "--relic", relic, "--n", str(n),
                            "--seed0", str(s0), "--set", f"dmg={blade}", "--json", str(out)],
                           cwd=HERE, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            raise RuntimeError(f"relic_rate failed for {relic} @ {blade} block {s0}:\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
        j = json.loads(out.read_text())
        wins += j["rate"] * j["games"]
        games += j["games"]
        per.append({"seed0": s0, "rate": j["rate"], "rateA": j["rateA"], "rateB": j["rateB"], "games": j["games"]})
    return {"blade": blade, "rate": wins / games, "games": games, "blocks": per}


def q(x: float) -> float:
    return round(x * 4) / 4


def sweep(game: str, html: str, relic: str, a, tmp: pathlib.Path) -> dict:
    b0 = current_blade(html, relic)
    pts = [measure(game, relic, b0, a.n, a.blocks, tmp)]
    log = lambda m: print(f"  {relic:<13} blade {m['blade']:<7} {m['rate']:.1%}  ({m['games']} fights)", flush=True)
    with LOCK:
        log(pts[0])
    while abs(pts[-1]["rate"] - 0.5) * 100 > a.tol and len(pts) < a.max:
        near = sorted(pts, key=lambda m: abs(m["rate"] - 0.5))[:2]
        if len(near) < 2 or near[0]["blade"] == near[1]["blade"] or near[0]["rate"] == near[1]["rate"]:
            m0 = near[0]
            step = max(-25.0, min(25.0, (50 - m0["rate"] * 100) / 0.4)) / 100
            nb = q(m0["blade"] * (1 + step))
        else:
            (b1, r1), (b2, r2) = [(m["blade"], m["rate"]) for m in near]
            nb = q(b1 + (0.5 - r1) * (b2 - b1) / (r2 - r1))
        lo, hi = 0.5 * b0, 1.6 * b0
        nb = max(q(lo), min(q(hi), nb))
        if any(abs(m["blade"] - nb) < 1e-9 for m in pts):
            break
        m = measure(game, relic, nb, a.n, a.blocks, tmp)
        pts.append(m)
        with LOCK:
            log(m)
    pick = min(pts, key=lambda m: (abs(m["rate"] - 0.5), abs(m["blade"] - b0)))
    return {"relic": relic, "current": b0, "points": pts, "pick": pick["blade"], "pick_rate": pick["rate"],
            "moved": pick["blade"] != b0}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relics", required=True)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--blocks", default="2207,2317")
    ap.add_argument("--tol", type=float, default=1.0, help="points of win rate either side of 50 that stay")
    ap.add_argument("--max", type=int, default=4, help="measurements per relic at most")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    a.blocks = [int(x) for x in a.blocks.split(",")]
    game = str((HERE / a.game).resolve())
    html = pathlib.Path(game).read_text(encoding="utf-8")
    relics = [r for r in a.relics.split(",") if r]
    print(f"BALANCE SWEEP  {pathlib.Path(game).name}  {len(relics)} relics  n={a.n}  blocks {a.blocks}  tol {a.tol}", flush=True)
    t0 = time.time()
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(a.parallel) as ex:
        res = list(ex.map(lambda r: sweep(game, html, r, a, pathlib.Path(td)), relics))
    print(f"\n{'relic':<13} {'current':>8} {'rate':>7}   {'pick':>7} {'rate':>7}  moved")
    for r in res:
        c = r["points"][0]
        print(f"{r['relic']:<13} {r['current']:>8} {c['rate']:>7.1%}   {r['pick']:>7} {r['pick_rate']:>7.1%}  {'YES' if r['moved'] else ''}")
    pathlib.Path(a.out).write_text(json.dumps({"game": game, "n": a.n, "blocks": a.blocks, "tol": a.tol,
                                               "results": res, "seconds": time.time() - t0}, indent=1))
    print(f"\nwrote {a.out}  ({time.time()-t0:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
