#!/usr/bin/env python3
"""TUNED DAMAGE AGAINST A FIXED REFERENCE FIELD — a cheap, uncoupled stand-in
for the closed-loop tuner, so the 3x3 factor test can be run on several rosters
inside one session.

WHY NOT JUST RUN tune.py
------------------------
`tune.py` moves twelve damages at once against each other; one run is ~10 min
here and the fixed point it lands on depends on the whole roster. To ask "does
the greatsword ratio survive matching the ultimates" I need the SAME statistic
on two rosters, and a coupled fixed point is the wrong instrument: it would let
a change to Dawnbringer's ultimate move Emberedge's number through the loop.

Instead, define per relic:

    d*(relic) = the dmg at which that relic wins 50% against a FIXED reference
                field of the six NON-block relics.

The six block relics never appear in each other's measurement, so each d* is an
independent 1-D root find. The reference field is byte-identical across arms, so
any change in d* is caused by the change to that relic.

THIS IS A DIFFERENT DEFINITION FROM THE PUBLISHED ONE and it is only worth
anything if it agrees with it. `--validate` measures the six block relics'
winrate against the field at their published tuned damage; if the definitions
coincide those are all ~50%. Run it before trusting anything else here.

Common random numbers throughout: every dmg point and every relic sees the same
seed list per opponent, so the comparison between points is far less noisy than
each point's absolute standard error.

    python3 gs_factor_probe.py --game sc-r15.html --validate
    python3 gs_factor_probe.py --game sc-r15.html --seed0 424242 --n 150
"""
from __future__ import annotations
import argparse, json, math, pathlib, sys, time
from scpage import game

# The six relics that are NOT in the 3x3 block. Fixed, never re-tuned, and
# identical across every arm — this is the ruler, not the thing measured.
FIELD = ["widowmaker", "thornwake", "gravemourn", "spellbreaker",
         "lightkeeper", "farwarden"]

# type -> (sanctified, dwarven)
BLOCK = {
    "greatsword": ("dawnbringer", "emberedge"),
    "bow":        ("aureole",     "ironhail"),
    "warhammer":  ("censer",      "grudgebearer"),
}
BLOCK_IDS = [w for pair in BLOCK.values() for w in pair]

# One evaluate() per relic: the whole dmg grid x field x seeds inside the page.
GRID_JS = r"""
([wid, dmgs, field, n, seed0]) => {
  const W = AC.WEAPONS.find(w => w.id === wid);
  if (!W) throw new Error('no relic ' + wid);
  const keep = W.dmg;
  // COMMON RANDOM NUMBERS: one seed list per opponent, reused at every dmg.
  const seeds = {};
  let s = seed0 >>> 0;
  for (const f of field) {
    const a = [];
    for (let k = 0; k < n; k++) { s = (Math.imul(s, 1103515245) + 12345) >>> 0; a.push(s); }
    seeds[f] = a;
  }
  const name = W.name;
  const out = [];
  for (const d of dmgs) {
    W.dmg = d;
    let win = 0, tot = 0, dur = 0, to = 0;
    const per = {};
    for (const f of field) {
      let fw = 0;
      for (const sd of seeds[f]) {
        const r = AC.simulate(wid, f, sd);
        if (r.winner === name) { fw++; win++; }
        if (r.reason !== 'slain') to++;
        dur += r.duration; tot++;
      }
      per[f] = fw / n;
    }
    out.push({ dmg: d, wr: win / tot, dur: dur / tot, timeout: to / tot, per });
  }
  W.dmg = keep;
  return out;
}
"""

VALIDATE_JS = r"""
([ids, field, n, seed0]) => {
  const res = {};
  let s = seed0 >>> 0;
  const seeds = {};
  for (const f of field) {
    const a = [];
    for (let k = 0; k < n; k++) { s = (Math.imul(s, 1103515245) + 12345) >>> 0; a.push(s); }
    seeds[f] = a;
  }
  for (const wid of ids) {
    const W = AC.WEAPONS.find(w => w.id === wid);
    let win = 0, tot = 0, dur = 0;
    for (const f of field) for (const sd of seeds[f]) {
      const r = AC.simulate(wid, f, sd);
      if (r.winner === W.name) win++;
      dur += r.duration; tot++;
    }
    res[wid] = { dmg: W.dmg, wr: win / tot, dur: dur / tot };
  }
  return res;
}
"""


def _logit(p, lo=0.02, hi=0.98):
    p = min(hi, max(lo, p))
    return math.log(p / (1 - p))


def solve_root(pts):
    """pts = [(dmg, wr)]. Weighted least squares of logit(wr) on ln(dmg),
    solved at wr = 0.5. Weight by binomial information so saturated points
    (wr near 0 or 1, where the logit clip bites) do not steer the fit."""
    xs = [math.log(d) for d, _ in pts]
    ys = [_logit(w) for _, w in pts]
    ws = [max(0.05, w * (1 - w)) for _, w in pts]
    sw = sum(ws)
    mx = sum(w * x for w, x in zip(ws, xs)) / sw
    my = sum(w * y for w, y in zip(ws, ys)) / sw
    sxy = sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys))
    sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs))
    if sxx <= 0 or sxy <= 0:
        return None, None
    slope = sxy / sxx                      # d logit / d ln(dmg)
    return math.exp(mx - my / slope), slope


def probe(pg, seed0, n, coarse_n, verbose=True, centers=None, only=None):
    """Two stage. Stage 1 brackets the 50% crossing on a wide coarse grid,
    stage 2 refits on a tight grid around it. Returns {wid: d*}."""
    ids = only or BLOCK_IDS
    base = pg.evaluate("Object.fromEntries(AC.WEAPONS.map(w=>[w.id,w.dmg]))")
    stage1 = {}
    if centers is None:
        COARSE = [0.45, 0.7, 1.0, 1.45, 2.1, 3.0]
        for wid in ids:
            grid = [round(base[wid] * m, 3) for m in COARSE]
            rows = pg.evaluate(GRID_JS, [wid, grid, FIELD, coarse_n, seed0 + 7919])
            d0, sl = solve_root([(r["dmg"], r["wr"]) for r in rows])
            if d0 is None:
                raise SystemExit(f"{wid}: coarse grid did not bracket 50% "
                                 f"({[round(r['wr'],3) for r in rows]})")
            d0 = min(max(d0, grid[0]), grid[-1])
            stage1[wid] = d0
            if verbose:
                print(f"    [coarse] {wid:<13} wr {[round(r['wr'],2) for r in rows]}"
                      f"  -> d* ~{d0:.2f}", flush=True)
    else:
        stage1 = dict(centers)

    FINE = [0.76, 0.87, 1.0, 1.15, 1.32]
    out, diag = {}, {}
    for wid in ids:
        grid = [round(stage1[wid] * m, 3) for m in FINE]
        rows = pg.evaluate(GRID_JS, [wid, grid, FIELD, n, seed0])
        d, sl = solve_root([(r["dmg"], r["wr"]) for r in rows])
        if d is None:
            raise SystemExit(f"{wid}: fine grid not monotone {[r['wr'] for r in rows]}")
        out[wid] = d
        diag[wid] = {"wr": [round(r["wr"], 3) for r in rows],
                     "grid": grid, "slope": sl,
                     "dur": round(sum(r["dur"] for r in rows) / len(rows), 1),
                     "timeout": round(max(r["timeout"] for r in rows), 3)}
        if verbose:
            print(f"    {wid:<13} d* {d:8.3f}   wr {diag[wid]['wr']}"
                  f"  slope {sl:5.2f}  dur {diag[wid]['dur']}s"
                  f"  to {diag[wid]['timeout']:.1%}", flush=True)
    return out, diag, stage1


def ratios(d):
    return {t: d[BLOCK[t][0]] / d[BLOCK[t][1]] for t in BLOCK}


def misfit(d):
    """rms |log| residual of dmg[school][type] = base[type] x mod[school] on the
    2x3 block, fitted in logs (which is exactly a two-way ANOVA on log dmg)."""
    rows, cols = ["sanctified", "dwarven"], list(BLOCK)
    L = {(s, t): math.log(d[BLOCK[t][0 if s == "sanctified" else 1]])
         for s in rows for t in cols}
    gm = sum(L.values()) / len(L)
    rm = {s: sum(L[(s, t)] for t in cols) / len(cols) for s in rows}
    cm = {t: sum(L[(s, t)] for s in rows) / len(rows) for t in cols}
    res = [L[(s, t)] - rm[s] - cm[t] + gm for s in rows for t in cols]
    return math.sqrt(sum(r * r for r in res) / len(res)), res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sc-r15.html")
    ap.add_argument("--n", type=int, default=150)
    ap.add_argument("--coarse-n", type=int, default=50)
    ap.add_argument("--seed0", type=int, action="append", default=None)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--only", default=None,
                    help="comma-separated relic ids; skips the ratio/misfit block")
    a = ap.parse_args()
    only = [s.strip() for s in a.only.split(",")] if a.only else None
    path = pathlib.Path(a.game)
    if not path.is_absolute():
        path = pathlib.Path(__file__).parent / path
    seeds = a.seed0 or [424242, 987654]

    t0 = time.time()
    with game(game_path=path) as (pg, errs):
        if a.validate:
            r = pg.evaluate(VALIDATE_JS, [BLOCK_IDS, FIELD, a.n, 424242])
            print(f"=== {path.name}: block relics at their shipped dmg, "
                  f"vs the fixed {len(FIELD)}-relic field, "
                  f"{a.n} seeds x {len(FIELD)} = {a.n*len(FIELD)} matches each ===")
            for wid in BLOCK_IDS:
                v = r[wid]
                print(f"  {wid:<13} dmg {v['dmg']:7.2f}   winrate "
                      f"{v['wr']*100:5.1f}%   mean {v['dur']:.1f}s")
            if errs:
                print("! PAGE ERRORS:", errs[:3], file=sys.stderr); return 1
            return 0

        runs, centers = {}, None
        for sd in seeds:
            print(f"\n=== {path.name}  seed0 {sd}  n {a.n} x {len(FIELD)} opponents"
                  f" x 5 dmg points ===", flush=True)
            d, diag, centers = probe(pg, sd, a.n, a.coarse_n, centers=centers,
                                     only=only)
            runs[sd] = d
            if only: continue
            rr = ratios(d)
            rms, _ = misfit(d)
            print(f"  ratios sanct/dwarv:  " +
                  "   ".join(f"{t} {rr[t]:.3f}" for t in BLOCK))
            print(f"  factor-model misfit rms|log| {rms:.4f}", flush=True)
        if errs:
            print("! PAGE ERRORS:", errs[:3], file=sys.stderr); return 1

    print(f"\n=== {path.name}: SUMMARY  ({time.time()-t0:.0f}s) ===")
    if only:
        for w in only:
            vals = [runs[s][w] for s in seeds]
            print(f"  {w:<13} d* " + "  ".join(f"{v:8.3f}" for v in vals)
                  + f"   mean {sum(vals)/len(vals):8.3f}")
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(
                {"game": path.name, "n": a.n,
                 "runs": {str(k): v for k, v in runs.items()}}, indent=1))
        return 0
    hdr = "  " + "".join(f"{t:>13}" for t in BLOCK)
    print(hdr)
    for lbl, sc in (("sanctified", 0), ("dwarven", 1)):
        cells = []
        for t in BLOCK:
            vals = [runs[s][BLOCK[t][sc]] for s in seeds]
            cells.append(f"{sum(vals)/len(vals):13.2f}")
        print(f"  {lbl:<10}" + "".join(cells))
    print("  " + "-" * 42)
    ids_done = list(runs[seeds[0]])
    mean_d = {w: sum(runs[s][w] for s in seeds) / len(seeds) for w in ids_done}
    rr = ratios(mean_d)
    print("  ratio     " + "".join(f"{rr[t]:13.3f}" for t in BLOCK))

    if len(seeds) >= 2:
        diffs = [math.log(runs[seeds[0]][w] / runs[seeds[1]][w]) for w in ids_done]
        noise = math.sqrt(sum(d * d for d in diffs) / len(diffs))
        # difference of two independent estimates -> per-run sd is /sqrt(2)
        print(f"\n  SEED-STREAM REPRODUCIBILITY (the noise floor)")
        print(f"    rms|log| between the two runs' d*   {noise:.4f}"
              f"   (max {max(abs(x) for x in diffs):.4f})")
        print(f"    implied per-run sd                  {noise/math.sqrt(2):.4f}")
        for s in seeds:
            r2 = ratios(runs[s])
            print(f"    seed {s}: " + "  ".join(f"{t} {r2[t]:.3f}" for t in BLOCK))
    rms, res = misfit(mean_d)
    print(f"\n  FACTOR-MODEL MISFIT rms|log| {rms:.4f}")

    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(
            {"game": path.name, "n": a.n, "runs": {str(k): v for k, v in runs.items()},
             "mean": mean_d, "ratios": rr, "misfit": rms}, indent=1))
        print(f"  wrote {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
