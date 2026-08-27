#!/usr/bin/env python3
"""TAKE THE CLOSING-WALL GLOW OFF THE FULL CANVAS.

    python3 wallglow_build.py --src sundered-crown.html --out sc-wall.html
    python3 wallglow_build.py --mode strips --out sc-wall-strips.html

WHY
---
One line in `drawArena` is 38% of the frame on an Adreno 660:

    c.shadowColor = "#E0433F"; c.shadowBlur = 30;
    c.strokeRect(n, n, W-n*2, H-n*2);

A Canvas2D shadow costs in proportion to the SURFACE it runs on. That is the
whole finding behind `worldlight_build.py` and `shadowbuf_build.py`, and both
of them cash it the same way: shrink the surface to fit the thing being blurred.

**That trick has nothing to shrink here.** The rect is the arena border, so its
bounding box IS the canvas, and a buffer sized to fit it is the canvas again.
NEXT-SESSION §3 recorded it as unfixable-by-buffer and proposed four gradient
strips as the replacement.

WHAT ACTUALLY WORKS, AND WHY IT IS NOT THE STRIPS
-------------------------------------------------
A Gaussian is scale-covariant. Blurring at 1/D scale with sigma/D and scaling
the result back up is the same Gaussian, to within the resampling error. So the
surface does shrink after all -- not by fitting the shape, but by dropping
resolution under the part of the draw that has no resolution in it.

    blur surface   2.07 Mpx  ->  0.13 Mpx at D=4      (16x less)
    added blur     resample ~D/2 device px, in quadrature against sigma 15:
                   sqrt(15^2 + 2^2) = 15.13           (0.9% wider)

The crisp 4px line never enters the buffer. `shadowOffsetX` pushes the source
rect clean off the buffer's left edge so ONLY its shadow lands, and the line is
then stroked at full resolution on top with no shadow at all. The sharp edge
stays sharp; the only thing that ever passes through the downscale is the soft
part, where a half pixel of extra blur has nothing to damage.

shadowBlur is in DEVICE pixels and is not touched by the CTM (HTML spec: "does
not correspond to a number of pixels and is not affected by the current
transformation matrix"). So the buffer wants `30 / D`, not `30`, and the ridge
amplitude comes out identical: the line is 4k device px against sigma 15 in the
main canvas and 4k/D against sigma 15/D in the buffer, and amplitude is
width/(sigma*sqrt(2pi)) either way.

--mode strips builds NEXT-SESSION's proposal instead, so the two can be diffed
against the truth rather than argued about. See `wallglow_probe.py`: the strips
are cheaper still and they are visibly wrong at the corners, which is exactly
what §3 predicted would need eyes.

WHAT THIS DOES NOT CHANGE
-------------------------
The glow only draws when `m.inset > 0`, so this is a collapse-phase change and
nothing else in the frame moves. `engine_ab` must stay identical field for
field: no simulation state is read or written here.
"""
from __future__ import annotations
import argparse, pathlib, sys

HERE = pathlib.Path(__file__).parent

_ap = argparse.ArgumentParser(description=__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("--src", default="sundered-crown.html")
_ap.add_argument("--out", default="sc-wall.html")
_ap.add_argument("--mode", choices=["buf", "strips"], default="buf",
                 help="buf = downscaled shadow buffer (default). "
                      "strips = NEXT-SESSION §3's four gradient strips.")
_ap.add_argument("--down", type=int, default=4,
                 help="buf mode: downscale factor D. Measured, not assumed — "
                      "wallglow_probe.py --sweep prints error vs D.")
_A = _ap.parse_args()

SRC = (HERE / _A.src)
if not SRC.exists():
    sys.exit(f"no such source: {SRC}")
s = SRC.read_text(encoding="utf-8")

# NO REFUSAL ON A GENERATED INPUT. This builder used to reject one, and that
# was overreach that broke the documented chain: `silhouette_build ->
# depth_build -> worldlight_build -> shadowbuf_build` is four builders each
# consuming the last one's output, and composing the branches needs
# `roster15_build -> cinema_build -> wallglow_build` to do the same.
#
# The rule in SEED.md is narrower than it reads: a generated file is not a
# place to STORE A NUMBER, which is why `tune.py --apply` refuses one. Nothing
# is stored here — this is a code transform with an asserted anchor, and if the
# anchor is gone it fails loudly two lines below.


def rep(src, old, new, label, expect=1):
    n = src.count(old)
    if n != expect:
        sys.exit(f"anchor {label}: found {n}, expected {expect}\n  {old[:120]}")
    return src.replace(old, new)


# --- the anchor: the one block being replaced --------------------------------
OLD = """      c.strokeStyle = "#E0433F"; c.lineWidth = 4;
      c.shadowColor = "#E0433F"; c.shadowBlur = 30;
      c.strokeRect(n, n, W-n*2, H-n*2);
      c.shadowBlur = 0;"""

NEW = """      this._wallGlow(c, W, H, n);"""

s = rep(s, OLD, NEW, "wall glow block")

# --- the replacement method, inserted just above drawArena -------------------
METHOD_BUF = """  /* THE CLOSING-WALL GLOW, OFF THE FULL CANVAS.

     `strokeRect` under `shadowBlur = 30` was 38%% of the frame on an Adreno
     660. The shadowbuf trick -- shrink the surface to fit the blurred thing --
     does not apply, because the thing is the arena border and its bounding box
     IS the canvas.

     A Gaussian is scale-covariant, so the surface shrinks a different way:
     blur at 1/D scale with sigma/D, scale back up. Same Gaussian, 1/D^2 of the
     pixels. The resample adds about D/2 device px of blur, which lands in
     quadrature against sigma 15 and vanishes (15 -> 15.13 at D=4).

     Only the SOFT part goes through the buffer. `shadowOffsetX` pushes the
     source rect off the buffer's left edge so the buffer receives its shadow
     and nothing else, and the 4px line is stroked at full resolution on top.
     Sharp stays sharp.

     shadowBlur is in device pixels and the CTM does not touch it, so the
     buffer wants 30/D. Amplitude is width/(sigma*sqrt(2pi)) on both sides and
     comes out equal: 4k against sigma 15 here, 4k/D against sigma 15/D there.

     Draws nothing when the walls are open. Reads no simulation state. */
  _wallGlow(c, W, H, n){
    const D = %(D)d;
    const t = c.getTransform();
    const k = Math.hypot(t.a, t.b) || 1;             /* device px per arena unit */
    const bw = Math.max(1, Math.ceil(W * k / D)), bh = Math.max(1, Math.ceil(H * k / D));

    if (!this._gbuf) this._gbuf = document.createElement("canvas");
    const b = this._gbuf;
    if (b.width !== bw || b.height !== bh){ b.width = bw; b.height = bh; }
    const bx = b.getContext("2d");
    bx.setTransform(1, 0, 0, 1, 0, 0);
    bx.globalCompositeOperation = "source-over";
    bx.globalAlpha = 1;
    bx.clearRect(0, 0, bw, bh);

    bx.save();
    bx.scale(k / D, k / D);
    /* The source rect is drawn one full arena-width to the left of where it
       belongs and the shadow is offset back by exactly that, in device px,
       because shadowOffset is device space too. What lands on the buffer is
       the shadow alone -- the rect itself is off the edge and clipped away. */
    const OFF = W + 64;
    bx.shadowColor = "#E0433F";
    bx.shadowBlur = 30 / D;
    bx.shadowOffsetX = OFF * k / D;
    bx.strokeStyle = "#E0433F"; bx.lineWidth = 4;
    bx.strokeRect(n - OFF, n, W - n*2, H - n*2);
    bx.restore();

    c.drawImage(b, 0, 0, bw, bh, 0, 0, W, H);        /* the soft part, upscaled */

    c.strokeStyle = "#E0433F"; c.lineWidth = 4;      /* the hard part, at full res */
    c.strokeRect(n, n, W - n*2, H - n*2);
  }

"""

METHOD_STRIPS = """  /* THE CLOSING-WALL GLOW as NEXT-SESSION §3 proposed it: four gradient
     strips, no blur anywhere. Cheapest of the three and the least faithful --
     a real blur wraps the corner radially and four axis-aligned strips cannot,
     so the diagonal outside each corner goes dark. Kept buildable so the
     comparison is a measurement instead of an argument. wallglow_probe.py. */
  _wallGlow(c, W, H, n){
    const R = 45;                                    /* 3 sigma at sigma = 15 */
    const stops = [[0.000,"00"],[0.167,"03"],[0.333,"0A"],[0.500,"1B"],
                   [0.667,"0A"],[0.833,"03"],[1.000,"00"]];
    const band = (x0,y0,x1,y1) => {
      const g = c.createLinearGradient(x0,y0,x1,y1);
      for (const [p,a] of stops) g.addColorStop(p, "#E0433F" + a);
      return g;
    };
    const L = n, T = n, Rt = W - n, B = H - n;
    c.fillStyle = band(0, T-R, 0, T+R); c.fillRect(L, T-R, Rt-L, 2*R);
    c.fillStyle = band(0, B-R, 0, B+R); c.fillRect(L, B-R, Rt-L, 2*R);
    c.fillStyle = band(L-R, 0, L+R, 0); c.fillRect(L-R, T, 2*R, B-T);
    c.fillStyle = band(Rt-R, 0, Rt+R, 0); c.fillRect(Rt-R, T, 2*R, B-T);

    c.strokeStyle = "#E0433F"; c.lineWidth = 4;
    c.strokeRect(n, n, W - n*2, H - n*2);
  }

"""

METHOD = (METHOD_BUF % {"D": _A.down}) if _A.mode == "buf" else METHOD_STRIPS

s = rep(s, "  /* ------------------------------------------------------------- arena --- */\n  drawArena(m){",
        "  /* ------------------------------------------------------------- arena --- */\n"
        + METHOD + "  drawArena(m){",
        "drawArena head")

# The stamp goes AFTER the doctype, where roster15_build.py puts its own.
#
# CORRECTED 2026-08-14: this comment previously claimed a comment ahead of
# `<!DOCTYPE html>` drops the browser into quirks mode. **That is false and was
# measured false** — `document.compatMode` reads `CSS1Compat` on builds stamped
# either way. An HTML5 parser takes a comment token in the "initial" insertion
# mode and stays there; only a missing or malformed doctype triggers quirks.
# (It was true of IE9 and earlier, which is where the belief comes from.)
#
# So this placement is a CONVENTION, matching roster15_build.py, not a fix.
# `introcard_build.py` stamps before the doctype and is not wrong to.
# Chained builds accumulate stamps, so the head of the file reads as the
# provenance of the build.
STAMP = (f"<!-- GENERATED by wallglow_build.py --mode {_A.mode}"
         + (f" --down {_A.down}" if _A.mode == "buf" else "")
         + f" --src {_A.src} — do not hand-edit or tune in place -->")
_DOC = "<!DOCTYPE html>\n"
if not s.startswith(_DOC):
    sys.exit("source does not begin with a doctype — refusing to guess where the stamp goes")
s = _DOC + STAMP + "\n" + s[len(_DOC):]

out = HERE / _A.out
out.write_text(s, encoding="utf-8", newline="\n")
import hashlib
print(f"{_A.out}  {hashlib.sha256(s.encode()).hexdigest()[:16]}  mode={_A.mode}"
      + (f" D={_A.down}" if _A.mode == "buf" else ""))
