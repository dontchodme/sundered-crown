#!/usr/bin/env python3
"""HOW WRONG IS THE REPLACEMENT GLOW, AND HOW MUCH DOES IT SAVE?

    python3 wallglow_probe.py --builds sundered-crown.html sc-wall.html sc-wall-strips.html
    python3 wallglow_probe.py --sweep                 # error vs downscale factor D

Two numbers per build, both taken on the SAME pinned frame:

  fidelity    the glow's own pixels, differenced against the shipped shadow.
              Reported as max and mean channel error over the arena, and again
              over the CORNERS alone, because that is where the strips were
              predicted to fail and a whole-frame mean would bury it.

  blur surface  every draw made while `shadowBlur > 0`, charged the area of the
              canvas it ran on. This is the metric that called the A->B->C
              chain correctly in-container (31.22 -> 26.48 -> 11.48 Mpx) when
              three different direct timings disagreed, and it is deterministic
              — no GPU, no thermals, no fight-to-fight variation.

WHAT WOULD COUNT AS FAILURE
---------------------------
The replacement is rejected if the glow's max channel error exceeds 8/255
anywhere, or if the corner mean exceeds 2/255. The scale those sit on is the
SOFT ridge's own peak, printed each run — the crisp 4px line and the wall fill
are in the same differenced image and are an order of magnitude brighter, so
quoting either as "the glow's peak" would flatter any candidate.

THE MEASUREMENT IS DIFFERENTIAL, WHICH IS THE ONLY REASON IT IS CLEAN
--------------------------------------------------------------------
Each build is rendered twice on one pinned match: once with `m.inset` at the
test value, once with `m.inset = 0`. The difference is the walls plus the glow
and NOTHING else — same seed, same fighters, same frame, same sigil rotation.
Differencing before comparing means a build that changed some unrelated pixel
cannot flatter or damn the glow.

`m.inset` is set directly rather than stepped to, so no build can reach the
test state by a different path than another.
"""
from __future__ import annotations
import argparse, base64, io, json, pathlib, sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

# The instrument. Wraps every draw that can carry a shadow and charges it the
# area of the surface it ran on. Installed before any frame is drawn, and it
# counts on BUFFER contexts too -- which is the entire point, since the fix
# moves the blur onto one.
INSTRUMENT = r"""
() => {
  const P = CanvasRenderingContext2D.prototype;
  window.__blur = { px: 0, calls: 0, sites: {} };
  const names = ["stroke","fill","strokeRect","fillRect","strokeText","fillText",
                 "drawImage","arc","ellipse","putImageData"];
  for (const nm of names){
    const orig = P[nm];
    if (typeof orig !== "function") continue;
    P[nm] = function(...a){
      if (this.shadowBlur > 0 && this.shadowColor !== "transparent"
          && this.shadowColor !== "rgba(0, 0, 0, 0)"){
        const cv = this.canvas;
        const area = (cv.width * cv.height) || 0;
        window.__blur.px += area;
        window.__blur.calls += 1;
        const key = nm + "@" + cv.width + "x" + cv.height;
        window.__blur.sites[key] = (window.__blur.sites[key] || 0) + 1;
      }
      return orig.apply(this, a);
    };
  }
  return true;
}
"""

FRAME = r"""
([a, b, seed, inset, w, h]) => {
  AC.setResolution(w, h);
  const m = new AC.Match(a, b, seed);
  m.inset = inset;
  window.__blur.px = 0; window.__blur.calls = 0; window.__blur.sites = {};
  AC.__draw(m);
  const blur = JSON.parse(JSON.stringify(window.__blur));
  return { png: document.querySelector("canvas").toDataURL("image/png"), blur };
}
"""


def frame(page, a, b, seed, inset, w, h):
    r = page.evaluate(FRAME, [a, b, seed, inset, w, h])
    im = Image.open(io.BytesIO(base64.b64decode(r["png"].split(",", 1)[1]))).convert("RGB")
    return np.asarray(im).astype(np.int16), r["blur"]


def glow_of(path, a, b, seed, inset, w, h):
    """Return (isolated glow+walls image, blur stats at inset, blur stats at 0).

    THE WARM-UP IS NOT A TIDY-UP. The weapon light is cached per relic, so the
    first frame a page ever draws pays for building it — 71 blurred draws that
    never happen again. Measured cold-then-warm, the wall glow appeared to cost
    4.74 Mpx, and every one of those Mpx was the cache. Both frames are drawn
    warm here, and the counter is reset after the warm-up rather than before.
    """
    with game(game_path=path) as (page, errors):
        page.evaluate(INSTRUMENT)
        frame(page, a, b, seed, inset, w, h)      # warm: caches, not measured
        frame(page, a, b, seed, 0.0, w, h)
        lit, blur_on = frame(page, a, b, seed, inset, w, h)
        dark, blur_off = frame(page, a, b, seed, 0.0, w, h)
        if errors:
            sys.exit(f"{path.name}: page errors: {errors[:3]}")
    return lit - dark, blur_on, blur_off, lit


def corner_mask(w, h, rows, cols, pad):
    """The four corner squares of the inner rect, where axis-aligned strips
    cannot reproduce a radial falloff. Sized to 3 sigma so it is the region the
    effect actually occupies, not a region chosen to make a number look good."""
    m = np.zeros((h, w), bool)
    for cy in rows:
        for cx in cols:
            y0, y1 = max(0, cy - pad), min(h, cy + pad)
            x0, x1 = max(0, cx - pad), min(w, cx + pad)
            m[y0:y1, x0:x1] = True
    return m


def report(name, diff, ref, cmask, blur_on, blur_off):
    err = np.abs(diff - ref)
    dpx = int((err.max(axis=2) > 0).sum())
    row = {
        "build": name,
        "max_err": int(err.max()),
        "mean_err": float(err.mean()),
        "corner_max": int(err[cmask].max()),
        "corner_mean": float(err[cmask].mean()),
        "diff_px": dpx,
        "blur_mpx_inset": blur_on["px"] / 1e6,
        "blur_calls_inset": blur_on["calls"],
        "blur_mpx_open": blur_off["px"] / 1e6,
        "sites": blur_on["sites"],
    }
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default="sundered-crown.html",
                    help="the build whose glow is the truth")
    ap.add_argument("--builds", nargs="*", default=["sc-wall.html", "sc-wall-strips.html"])
    ap.add_argument("--a", default="dawnbringer")
    ap.add_argument("--b", default="grudgebearer")
    ap.add_argument("--seed", type=int, default=424242)
    ap.add_argument("--inset", type=float, default=64.0)
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--sweep", action="store_true",
                    help="build and score D = 2,3,4,6,8 instead of --builds")
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    ref_path = HERE / A.ref
    ref_diff, ref_on, ref_off, ref_lit = glow_of(ref_path, A.a, A.b, A.seed,
                                                 A.inset, A.w, A.h)
    h, w, _ = ref_diff.shape

    # The inset is in arena units; the drawn wall is `m.inset * renderer.scale`.
    # Locate the glow empirically instead of recomputing that scale here.
    #
    # MEAN across the other axis, not max. The left and right wall lines are
    # equally bright in EVERY row, so a per-row max is that same value at every
    # y and argmax lands wherever the noise falls — it returned y=900 on a wall
    # sitting at y=305, which silently aimed the corner mask at open floor. The
    # corner columns were then reporting mid-arena error under a corner heading.
    # A full-width horizontal line moves the row MEAN; one vertical line barely
    # does. The x offset is NOT the y offset either: the arena is inset by `pad`
    # horizontally and `arenaTop` vertically, so both are found separately.
    # All FOUR edges are found separately. The arena is not centred in the
    # canvas — the HUD is above it and the footer below — so the bottom wall is
    # not at `h - top`, and mirroring the top edge left the bottom crisp line
    # standing inside the "soft" mask and reported the line's own 209/255 as the
    # glow's amplitude.
    rprof = np.abs(ref_diff).mean(axis=(1, 2))
    cprof = np.abs(ref_diff).mean(axis=(0, 2))
    top = int(np.argmax(rprof[: h // 2]))
    bot = int(np.argmax(rprof[h // 2:])) + h // 2
    left = int(np.argmax(cprof[: w // 2]))
    right = int(np.argmax(cprof[w // 2:])) + w // 2
    cmask = corner_mask(w, h, (top, bot), (left, right), 60)

    # The isolated diff is walls + line + glow. The crisp 4px line saturates at
    # the stroke colour and the wall fill is a flat slab, and neither is the
    # thing under test — quoting either as "the glow's peak" would inflate the
    # scale the error is judged against. Mask a band around the edge and take
    # the peak of what is left: that is the SOFT ridge, which is what the
    # replacement has to reproduce.
    # The vertical edges do NOT sit at the same offset as the horizontal ones:
    # the arena is inset by `pad` in x and `arenaTop` in y, so masking columns
    # at the row index leaves the left and right lines standing and the "soft
    # peak" comes back as the crisp line again. Find the column the same
    # empirical way the row was found.
    soft = np.abs(ref_diff).copy()
    band = 8
    for lo in (top, bot):
        soft[max(0, lo - band):lo + band, :, :] = 0
    for lo in (left, right):
        soft[:, max(0, lo - band):lo + band, :] = 0
    peak_soft = int(soft.max())
    peak = int(np.abs(ref_diff).max())
    print(f"reference   {A.ref}")
    print(f"  crisp line + wall fill peak  {peak}/255"
          f"   (inner rect x {left}..{right}, y {top}..{bot})")
    print(f"  the SOFT glow's own peak     {peak_soft}/255"
          f"   <- the scale the error is judged against")
    print(f"  blur surface, walls closing   {ref_on['px']/1e6:.2f} Mpx"
          f"   {ref_on['calls']} blurred draws")
    print(f"  blur surface, walls open      {ref_off['px']/1e6:.2f} Mpx"
          f"   {ref_off['calls']} blurred draws")
    print(f"  the wall glow alone           "
          f"{(ref_on['px']-ref_off['px'])/1e6:.2f} Mpx")
    print()

    builds = list(A.builds)
    if A.sweep:
        import subprocess
        builds = []
        for D in (2, 3, 4, 6, 8):
            out = f"sc-wall-D{D}.html"
            subprocess.run([sys.executable, str(HERE / "wallglow_build.py"),
                            "--src", A.ref, "--out", out, "--mode", "buf",
                            "--down", str(D)], check=True, cwd=HERE)
            builds.append(out)

    rows = []
    hdr = (f"{'build':<26}{'maxErr':>7}{'meanErr':>9}{'cnrMax':>8}"
           f"{'cnrMean':>9}{'blurMpx':>9}{'verdict':>10}")
    print(hdr)
    print("-" * len(hdr))
    for bname in builds:
        p = HERE / bname
        if not p.exists():
            print(f"{bname:<26}  MISSING")
            continue
        d, on, off, _ = glow_of(p, A.a, A.b, A.seed, A.inset, A.w, A.h)
        r = report(bname, d, ref_diff, cmask, on, off)
        ok = r["max_err"] <= 8 and r["corner_mean"] <= 2.0
        r["pass"] = ok
        rows.append(r)
        print(f"{bname:<26}{r['max_err']:>7}{r['mean_err']:>9.3f}"
              f"{r['corner_max']:>8}{r['corner_mean']:>9.3f}"
              f"{r['blur_mpx_inset']:>9.2f}{'PASS' if ok else 'FAIL':>10}")

    print()
    print("thresholds: max channel error <= 8/255 anywhere, corner mean <= 2.0/255")
    print(f"            (the soft ridge's own peak is {peak_soft}/255)")

    if A.json:
        (HERE / A.json).write_text(json.dumps(
            {"ref": {"peak": peak, "blur_mpx": ref_on["px"] / 1e6,
                     "blur_open_mpx": ref_off["px"] / 1e6},
             "builds": rows}, indent=2))
        print(f"\nwrote {A.json}")


if __name__ == "__main__":
    main()
