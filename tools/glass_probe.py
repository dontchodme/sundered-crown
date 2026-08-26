#!/usr/bin/env python3
""""TOO UNIFORM" AS A NUMBER — and does the daylight ever close?

    python3 glass_probe.py --a ../02-chain/sc-cardspin.html \
                           --b ../02-chain/sc-glass-nb.html

WHY THIS EXISTS
---------------
Rick's note on Axiom was *"the shards ... are a bit too uniform."* That is a
judgement, and this project's habit is to turn a judgement into an instrument
before spending a session on it — otherwise the only test of the fix is the
same pair of eyes that asked for it, and the next person to touch `_conjure`
has nothing to regress against.

Uniformity is measurable directly. Walk the blade axis column by column and ask
of each column: is there shard here, or is there daylight? That gives the run
lengths — every shard and every gap, in pixels — and:

    CV = stdev / mean            of the shard x-extents, and of the gaps
                                 between consecutive shards

**CV 0.000 is a machine.** The shipped build scores exactly that, by
construction: `u0 = i/N` cuts equal pieces and a constant `frac` leaves equal
gaps. Any number above 0 is a claim that the pieces differ, and how far above 0
is how much.

THE FAILURE THIS IS REALLY HUNTING
-----------------------------------
`glass_build.py` derives the cut angle from a **budget**: the lean a break may
carry is whatever the narrowest gap can afford once the drift and cant
differentials are paid for. That derivation is arithmetic done at the desk, and
arithmetic done at the desk is precisely the kind of thing that is wrong at one
phase of a 20*pi period and right everywhere else. v1's constant lean shut the
gaps outright and it took a screenshot to notice.

So [1] is the check that matters: **at every sampled `_t`, there are still N
shards with N-1 gaps between them, and no gap is thinner than `--min-gap`.**
A gap that closes merges two shards, the run count drops, and the weapon is
quietly solid again at that phase.

WHY THIS COUNTS REGIONS AND NOT COLUMNS
----------------------------------------
v1 of this probe walked the axis column by column and called a column "gap" if
no pixel in it was lit. That is a correct test for the SHIPPED weapon and a
wrong one for the candidate, and the difference is the whole point of the
patch.

A column projection cannot tell a closed gap from a SLANTED one. Two faces that
lean the same way — which they must, being the same fracture — leave a
constant-width diagonal band of daylight, plainly open to the eye, whose
projection onto the x axis is empty as soon as the lean exceeds
`gap / (2 x band height)`. v1 duly reported every leaning build as "the gap
closes", including builds whose screenshots show daylight all the way through.
It was measuring the projection of the daylight, not the daylight.

So: label the CONNECTED REGIONS of shard ink. Two shards that touch are one
region; two shards separated by any path of background are two, at any angle.
That is the property the art actually has to hold.

The separation is then measured by DILATION rather than by geometry: grow every
region by k pixels and find the smallest k at which the count drops. The gap
that closed first was `2k` wide, whatever direction it ran in.

THE BEAM IS DELETED, NOT AVOIDED
---------------------------------
The axial beam runs down the middle of the weapon and bridges every gap by
design — it is the light showing THROUGH them. Flattened to white it would join
all six shards into one region. Sampling two bands either side of it and
stacking them is the obvious dodge and it is wrong twice: it invents an
adjacency across the axis, and near the tapered tip it splits a shard whose two
halves do not both reach the band. It scored the SHIPPED weapon at seven shards
at some phases, which is how it was caught.

Instead the beam is opened away — eroded by a vertical element taller than its
2 blade units and dilated back. A 27-unit shard survives that untouched, at any
drift or cant, and the bar does not.

`--b` SHOULD BE A `--bind 0 --pool 0` BUILD
--------------------------------------------
The filaments and the gap pool are drawn ACROSS the daylight on purpose, and
under the flattened palette they are white, so they bridge the runs exactly the
way the beam does. Neither touches `seg` or `cut`, so a bind-free build has
**identical geometry** — it is the honest control for a geometric question, not
a different weapon. The tool warns if `--b` looks like it has them on.
"""
from __future__ import annotations

import argparse
import base64
import io
import math
import pathlib
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

from scpage import game

HERE = pathlib.Path(__file__).parent

# The greatsword at shipping size, drawn at a scale where one blade unit is
# several pixels -- a gap 1 unit wide has to be countable, not rounded away.
L, W, S = 122, 40, 8.0

SHOT = """([shape, aff, L, W, S, t]) => {
  const cv = document.createElement('canvas');
  cv.width  = Math.round(L * S * 1.30);
  cv.height = Math.round(W * S * 3.2);
  const c = cv.getContext('2d');
  c.fillStyle = '#000000'; c.fillRect(0, 0, cv.width, cv.height);
  /* The same flattening silhouette_probe.py uses: every palette field to one
     white, so nothing the shape does with COLOUR can register and the only
     thing left in the image is where it put ink. */
  const p = Object.assign({}, AC.AFFINITIES[aff]);
  p.core = p.glow = p.steel = p.dark = '#FFFFFF';
  AC.SHAPES._t = t;
  c.save();
  c.translate(W * S * 0.55, cv.height / 2);
  c.scale(S, S);
  AC.SHAPES[shape](c, L, W, p, 0.5, aff);
  c.restore();
  AC.SHAPES._t = 0;
  return [cv.toDataURL('image/png').slice(22), W * S * 0.55, cv.height / 2];
}"""


def regions(mask: np.ndarray, ox: float, oy: float, bw_px: float,
            xa: float, xb: float, beam_px: int):
    """Connected regions of shard ink inside the slice window.

    THE BEAM IS REMOVED MORPHOLOGICALLY, not by sampling a band away from it.
    v2 of this probe took two horizontal bands either side of the axis and
    stacked them, which bridges y=-0.25bw to y=+0.25bw with a seam that does
    not exist and, near the tapered tip, splits one shard into two regions
    whenever only one of its halves reaches the band. It reported the SHIPPED
    weapon as seven shards at some phases, which is how it was caught: the
    control is known to be six.

    A vertical opening is exact instead of approximate. The axial beam is a
    horizontal bar `W * o.beam` tall — 2 blade units — and every shard is
    `2 * bw` tall, 27. Eroding by a vertical element taller than the beam and
    dilating back deletes the bar and returns the shards whole, still joined
    through their own middles, at any drift or cant.

    The x window matters as much. The SIGIL turns backwards at `gap * 0.50`
    with a radius of `W * 0.30` and spokes out to `1.55x` that: it is not a
    shard, and counting it merges it with the first piece and poisons every
    statistic downstream. The TIP is a light ball past `L`.
    """
    m = mask > 96
    m = ndimage.binary_opening(m, structure=np.ones((beam_px, 1), dtype=bool))
    w = np.zeros_like(m)
    w[:, int(xa):int(xb)] = m[:, int(xa):int(xb)]
    lab, n = ndimage.label(w, structure=np.ones((3, 3), dtype=int))
    spans = []
    for i in range(1, n + 1):
        xs = np.nonzero(lab == i)[1]
        if xs.size < 40:          # specks from an antialiased corner
            continue
        spans.append((int(xs.min()), int(xs.max())))
    spans.sort()
    return w, spans


def min_separation(w: np.ndarray, target: int, kmax: int = 40) -> int:
    """Smallest dilation, in pixels, that merges two regions. The daylight that
    closed first was about `2k` wide -- measured in whatever direction it
    actually ran, which is the point of doing it this way."""
    for k in range(1, kmax + 1):
        d = ndimage.binary_dilation(w, structure=np.ones((3, 3), dtype=bool),
                                    iterations=k)
        lab, n = ndimage.label(d, structure=np.ones((3, 3), dtype=int))
        big = sum(1 for i in range(1, n + 1) if (lab == i).sum() >= 12)
        if big < target:
            return k
    return kmax + 1


def measure(page, shape: str, aff: str, ts: list[float], bw: float,
            fa: float, fb: float, beam: int = 26):
    """Per-`_t`: the interior shard runs and the gaps between them.

    `bw` arrives as a FRACTION of W, the way the callers of `_conjure` write it.
    It becomes pixels here and nowhere else -- passing it through as 0.34 put
    the sample band at |y| in [0.7, 3.0] PIXELS, which is directly on the axial
    beam, so every gap bridged and the control read as one shard. The check
    that caught it was [5], asking the instrument to agree the control is
    uniform before believing anything it says about the candidate."""
    rows = []
    for t in ts:
        b64, ox, oy = page.evaluate(SHOT, [shape, aff, L, W, S, t])
        im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("L")
        m = np.asarray(im, dtype=np.uint8)
        w, spans = regions(m, ox, oy, bw * W * S,
                           ox + fa * L * S, ox + fb * L * S, beam)
        ink = [b - a for a, b in spans]
        gap = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
        sep = min_separation(w, len(spans)) if len(spans) > 1 else 0
        rows.append((t, ink, gap, sep))
    return rows


def cv(xs: list[int]) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    if m == 0:
        return 0.0
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs)) / m


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", default="../02-chain/sc-cardspin.html",
                    help="control — the build being complained about")
    ap.add_argument("--b", default="../02-chain/sc-glass-nb.html",
                    help="candidate. Should be built --bind 0 --pool 0; see the "
                         "docstring for why that is the honest control and not "
                         "a different weapon.")
    ap.add_argument("--shape", default="greatsword")
    ap.add_argument("--aff", default="runic")
    ap.add_argument("--bw", type=float, default=0.34,
                    help="the caller's bw as a fraction of W (greatsword 0.34)")
    ap.add_argument("--n", type=int, default=6, help="shards expected")
    ap.add_argument("--nt", type=int, default=12, help="values of _t")
    ap.add_argument("--window-from", type=float, default=0.20,
                    help="start of the slice window as a fraction of L — the "
                         "caller's `gap`. Below it lies the SIGIL, which is in "
                         "the band and is not a shard.")
    ap.add_argument("--window-to", type=float, default=0.99,
                    help="end of the window as a fraction of L, short of the "
                         "tip ball")
    ap.add_argument("--beam-px", type=int, default=26,
                    help="height of the vertical opening that deletes the axial "
                         "beam. Must exceed the beam (W*o.beam, 16px here) and "
                         "stay under the thinnest shard (~58px at the tip).")
    ap.add_argument("--dump", action="store_true",
                    help="print every run in blade units, per _t")
    ap.add_argument("--min-gap", type=float, default=1.0,
                    help="thinnest daylight allowed, in BLADE UNITS. Below this "
                         "the gap is a hairline at shipping size and the pieces "
                         "have effectively rejoined.")
    A = ap.parse_args()

    # 20*pi is the common period of the 2.1 and 1.6 phases; a single frame
    # proves nothing, so sample across it and add values off the grid.
    period = 20 * math.pi
    ts = [period * k / A.nt for k in range(A.nt)] + [0.37, 1.234, 7.5]

    def resolve(n):
        for c in (pathlib.Path(n), HERE / n, HERE.parent / n):
            if c.exists():
                return c.resolve()
        print(f"! cannot find {n}", file=sys.stderr)
        raise SystemExit(2)

    pa, pb = resolve(A.a), resolve(A.b)
    src_b = pb.read_text(encoding="utf-8")
    if "bind:0.000" not in src_b or "pool:0.000" not in src_b:
        print("  ! --b does not look like a --bind 0 --pool 0 build. The "
              "filaments and the pool bridge the daylight by design and this "
              "measures the daylight. Numbers below may be meaningless.\n")

    out = {}
    for label, path in (("A control", pa), ("B candidate", pb)):
        with game(game_path=path) as (page, errors):
            out[label] = measure(page, A.shape, A.aff, ts, A.bw,
                                 A.window_from, A.window_to, A.beam_px)
        if errors:
            print(f"  ! page errors on {path.name}: {errors[:2]}", file=sys.stderr)
            return 2

    fails = 0

    def check(ok: bool, name: str, detail: str = "") -> None:
        nonlocal fails
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))

    px_per_unit = S
    print(f"=== {pa.name}  vs  {pb.name} ===")
    print(f"    {A.shape}/{A.aff} at L={L} W={W}, {len(ts)} values of _t, "
          f"{px_per_unit:.0f}px per blade unit\n")

    hdr = f"    {'build':<14}{'shards':>8}{'gaps':>7}{'min sep':>10}{'shard CV':>11}{'gap CV':>9}"
    print(hdr)
    stats = {}
    for label in ("A control", "B candidate"):
        rows = out[label]
        counts = {len(ink) for _, ink, _, _ in rows}
        mins = min(2 * sep for _, _, _, sep in rows) / px_per_unit
        scv = sum(cv(ink) for _, ink, _, _ in rows) / len(rows)
        gcv = sum(cv([g for g in gaps if g > 0]) for _, _, gaps, _ in rows) / len(rows)
        stats[label] = (counts, mins, scv, gcv)
        cs = str(sorted(counts)) if len(counts) > 1 else str(next(iter(counts)))
        print(f"    {label:<14}{cs:>8}{len(rows[0][2]):>7}{mins:>10.2f}"
              f"{scv:>11.3f}{gcv:>9.3f}")
    print()

    if A.dump:
        for label in ("A control", "B candidate"):
            print(f"    -- {label}")
            for t, ink, gap, sep in out[label]:
                print(f"       _t {t:8.3f}  ink {[round(v / px_per_unit, 1) for v in ink]}")
                print(f"                  gap {[round(v / px_per_unit, 1) for v in gap]}")
        print()

    ca, ma, sa, ga = stats["A control"]
    cb, mb, sb, gb = stats["B candidate"]

    check(cb == {A.n},
          f"[1] {A.n} shards at EVERY sampled _t — no gap ever closes",
          f"saw {sorted(cb)}")
    check(mb >= A.min_gap,
          f"[2] thinnest daylight >= {A.min_gap} blade units, in any direction",
          f"{mb:.2f} units ({mb * px_per_unit:.0f}px at this scale)")
    check(sb > 0.10,
          "[3] shard lengths are not uniform",
          f"CV {sb:.3f} against the control's {sa:.3f}")
    check(gb > 0.10,
          "[4] daylight widths are not uniform",
          f"CV {gb:.3f} against the control's {ga:.3f}")
    check(len(ca) == 1 and sa < 0.07 and ga < 0.07,
          "[5] the instrument agrees the control IS uniform",
          f"control {sorted(ca)} shards (its own count, NOT --n, which "
          f"describes the candidate), CV {sa:.3f}/{ga:.3f} — this is the "
          f"NOISE FLOOR, not zero: the profile stroke and the canted clip both "
          f"widen a shard by ~1 unit in world x, so equal pieces measure "
          f"unequal by a few percent. A candidate has to clear it to mean "
          f"anything. If this check fails the measurement is wrong, not the art.")

    print(f"\n  {'ALL PASS' if not fails else str(fails) + ' FAILED'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
