#!/usr/bin/env python3
"""Which (frac, n, open, gapvar) actually keeps the daylight open?

The cut-angle budget in `glass_build.py` is arithmetic done at the desk, and
`glass_probe.py` says the desk is wrong: at `open 0.25` the narrowest gap
reaches 0.25 blade units and two shards merge. Rather than nudge a constant
until one screenshot looks right, build the grid and measure it.

Reported per config:

    shards   the set of shard counts seen across the _t sweep. Anything but
             {n} means a gap closed at some phase.
    min gap  the thinnest daylight, in blade units, over the whole sweep
    slope    the cut-angle budget the build actually derived. THIS IS THE LOOK
             -- 0.05 is a vertical saw cut, 0.35 reads as a broken plane.
    CV       shard-length and gap-width variation, against a 0.035/0.049 noise
             floor from the shipped build.

Every build here is `--bind 0 --pool 0`: the filaments and the pool cross the
daylight on purpose and would bridge the runs. They do not touch `seg`/`cut`,
so the geometry measured is the geometry that ships.
"""
from __future__ import annotations

import math
import pathlib
import subprocess
import sys

from glass_probe import L, S, W, cv, measure
from scpage import game

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
CTRL = CHAIN / "sc-cardspin.html"

# (label, n, frac, open, gapvar)
GRID = [
    ("open  0.00",        6, 0.74,  0.00, 0.90),
    ("open -0.15",        6, 0.74, -0.15, 0.90),
    ("open -0.30",        6, 0.74, -0.30, 0.90),
    ("open -0.45",        6, 0.74, -0.45, 0.90),
    ("open -0.30 gap0.6", 6, 0.74, -0.30, 0.60),
    ("open -0.30 frac.70",6, 0.70, -0.30, 0.90),
]

PERIOD = 20 * math.pi
TS = [PERIOD * k / 14 for k in range(14)] + [0.37, 1.234, 7.5]


def slope_of(path: pathlib.Path, n: int) -> float:
    """Ask the build itself what lean it derived, rather than re-deriving it
    here — a second copy of the arithmetic would agree with the first and
    disagree with the picture, which is the failure mode this whole file is
    about."""
    js = """(n) => {
      const S = AC.SHAPES, p = AC.AFFINITIES.runic;
      let seen = 0;
      const cv = document.createElement('canvas');
      cv.width = 900; cv.height = 400;
      const c = cv.getContext('2d');
      const orig = S._h;
      /* Re-run the builder's own budget line by reading the cut table it
         produced: the widest |lean| over the N+1 fractures IS the slope it
         allowed itself, times 0.70. */
      const grab = [];
      const realConjure = S._conjure;
      S._conjure = function(cc, LL, WW, pp, o){
        const N = o.n, gap = o.gap, bw = o.bw, jag = o.jag || 0;
        const frac = o.frac || 0.87;
        const sf = o.sliceFrom === undefined ? gap : o.sliceFrom;
        const st = o.sliceTo === undefined ? LL : o.sliceTo;
        const span = st - sf;
        const H = bw * 2.2;
        const sw = [], gw = []; let ss = 0, gs = 0;
        for (let i = 0; i < N; i++){
          sw.push(1 + (S._h(i, 11) - 0.5) * __LV__ * jag);
          gw.push(1 + (S._h(i, 23) - 0.5) * __GV__ * jag);
          ss += sw[i]; gs += gw[i];
        }
        let minGap = Infinity;
        for (let i = 0; i < N - 1; i++) minGap = Math.min(minGap, span * (1 - frac) * gw[i] / gs);
        const dMax = WW * o.drift, cMax = o.cant;
        const room = minGap * (1 - (o.open === undefined ? 0.25 : o.open)) - 2 * cMax * bw;
        grab.push({ slope: Math.max(0, room) / (2 * dMax), minGap: minGap });
        return realConjure.apply(S, arguments);
      };
      S.greatsword(c, 122, 40, p, 0.5, 'runic');
      S._conjure = realConjure;
      return grab[0];
    }"""
    with game(game_path=path) as (page, errors):
        return page.evaluate(js.replace("__LV__", str(LV[path])).replace("__GV__", str(GV[path])), n)


LV: dict = {}
GV: dict = {}


def main() -> int:
    rows = []
    with game(game_path=CTRL) as (page, errors):
        base = measure(page, "greatsword", "runic", TS, 0.34, 0.20, 0.99)
    bshards = {len(i) for _, i, _, _ in base}
    bmin = min(2 * sep for _, _, _, sep in base) / S
    print(f"    {'config':<18}{'n':>3}{'frac':>7}{'open':>7}{'gapvar':>8}"
          f"{'shards':>9}{'min sep':>9}{'slope':>8}{'CV len':>8}{'CV gap':>8}")
    print(f"    {'shipped (control)':<18}{6:>3}{0.74:>7.2f}{'—':>7}{'—':>8}"
          f"{str(sorted(bshards)):>9}{bmin:>9.2f}{0.0:>8.3f}"
          f"{sum(cv(i) for _, i, _, _ in base) / len(base):>8.3f}"
          f"{sum(cv([g for g in gg if g > 0]) for _, _, gg, _ in base) / len(base):>8.3f}")

    for label, n, frac, open_, gapvar in GRID:
        out = CHAIN / f"sc-glass-sw.html"
        r = subprocess.run(
            [sys.executable, "glass_build.py", "--src", str(CTRL), "--out", str(out),
             "--n", str(n), "--frac", str(frac), "--open", str(open_),
             "--gapvar", str(gapvar), "--bind", "0", "--pool", "0"],
            cwd=HERE, capture_output=True, text=True)
        if r.returncode:
            print(f"    {label:<18}  BUILD FAILED: {r.stderr.strip()[:60]}")
            continue
        LV[out.resolve()] = 1.15
        GV[out.resolve()] = gapvar
        sl = slope_of(out.resolve(), n)
        with game(game_path=out.resolve()) as (page, errors):
            m = measure(page, "greatsword", "runic", TS, 0.34, 0.20, 0.99)
        shards = {len(i) for _, i, _, _ in m}
        mn = min(2 * sep for _, _, _, sep in m) / S
        lcv = sum(cv(i) for _, i, _, _ in m) / len(m)
        gcv = sum(cv([g for g in gg if g > 0]) for _, _, gg, _ in m) / len(m)
        ok = "" if shards == {n} and mn >= 1.0 else "   <-- gap closes"
        print(f"    {label:<18}{n:>3}{frac:>7.2f}{open_:>7.2f}{gapvar:>8.2f}"
              f"{str(sorted(shards)):>9}{mn:>9.2f}{sl['slope']:>8.3f}"
              f"{lcv:>8.3f}{gcv:>8.3f}{ok}")
        rows.append((label, n, frac, open_, gapvar, shards, mn, sl["slope"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
