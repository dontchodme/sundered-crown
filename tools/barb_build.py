#!/usr/bin/env python3
"""RED RAZOR POINTS on the bloodsworn flail head.

    python3 barb_build.py --src ../02-chain/sc-twinshade-scrunch.html \
                          --out ../02-chain/sc-redbarb.html

Rick: "the tips of the flail are red dots. can we change those to red razor
sharp points? fits the bloody theme better imo" ... "flail head looks good but
lets shorten those spikes a bit."

WHAT WAS THERE, and it is worse than "a dot": the barb ALREADY terminates at a
true vertex -- its outer edge runs to `P1 = dir(a+0.86)*r*1.94` and its inner
edge leaves from the same point. The tip was a filled circle of radius 0.13r
centred 0.08r INSIDE that vertex, spanning 1.73r to 1.99r. **The dot was not
decorating the point, it was capping a point that already existed.**

PRESENTATION ONLY. Nothing in the simulation reads shape art, so `engine_ab`
must come back bit-identical on all nineteen ids. That is the check that says
this is what it claims to be, and `barb_probe.py --built` re-runs the dispatch
assertions against the written file rather than against a runtime injection.

`_needle` is factored out rather than inlined because THE SPIKES THIS RELIC'S
ULTIMATE THROWS ARE THE BARBS IT WEARS, and the projectile will call it too. A
barb's tip is cut from the barb's own Bezier and a thrown spike is not, so what
is shared is the LOOK and not the construction -- which is exactly as much as
they have in common.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# Rick's ladder pick, at 1:1. 0.42 was what he first saw; below 0.24 the red
# stops being a spike and becomes a cap, which is the shipped dot's failure
# with extra steps.
POINT_LEN = 0.30
CONC      = 0.18      # edge concavity. convex reads as a thorn, straight as a
                      # triangle, concave as honed.
BACK      = 0.72      # where the base sits on the barb's leading edge
FRONT     = 0.30      # ... and on the trailing edge
GLOW_A    = 0.85
GLOW_W    = 0.34

NEEDLE = '''  /* A NEEDLE: two concave edges meeting at a TRUE VERTEX, plus the light on
     the leading edge drawn as a second needle SHARING that vertex.

     Never a stroke. A stroke has a cap and a cap is a blunt end at any width --
     v37 section 8.3 learned this on the flame tongues ("drawn as strokes with
     round caps: noodles ... the taper is most of what makes it read") and it is
     the same lesson here. An outline stroked round the whole thing would round
     off the point exactly the way the red dot used to.

     Callers hand in their own three points. A barb's tip is cut from the barb's
     own Bezier; a thrown spike is not. What these share is the LOOK, which is
     all they have in common, so that is all that is factored. */
  _needle(c, B1, AP, B2, conc, core, glow, ga, gw){
    const lp = (u, v, t) => [u[0] + (v[0] - u[0]) * t, u[1] + (v[1] - u[1]) * t];
    const k1 = lp(lp(B1, AP, 0.5), B2, conc);
    const k2 = lp(lp(AP, B2, 0.5), B1, conc);
    c.fillStyle = core;
    c.beginPath();
    c.moveTo(B1[0], B1[1]);
    c.quadraticCurveTo(k1[0], k1[1], AP[0], AP[1]);
    c.quadraticCurveTo(k2[0], k2[1], B2[0], B2[1]);
    c.closePath(); c.fill();
    if (!(ga > 0)) return;
    const G2 = lp(B1, B2, gw);
    const g1 = lp(lp(B1, AP, 0.5), G2, conc);
    const g2 = lp(lp(AP, G2, 0.5), B1, conc);
    c.globalAlpha = ga; c.fillStyle = glow;
    c.beginPath();
    c.moveTo(B1[0], B1[1]);
    c.quadraticCurveTo(g1[0], g1[1], AP[0], AP[1]);
    c.quadraticCurveTo(g2[0], g2[1], G2[0], G2[1]);
    c.closePath(); c.fill();
    c.globalAlpha = 1;
  },

'''

OLD_TIPS = '''    SHAPES._fhBall(c, D, p);
    c.fillStyle = p.core;
    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU + 0.86;
      c.beginPath();
      c.arc(Math.cos(a) * r * 1.86, Math.sin(a) * r * 1.86, r * 0.13, 0, TAU);
      c.fill();
    }
    c.restore();'''

NEW_TIPS = '''    SHAPES._fhBall(c, D, p);
    /* THE TIPS, HONED. They were filled circles of radius 0.13r centred 0.08r
       INSIDE the barb's own vertex -- spanning 1.73r to 1.99r against a barb
       that terminates at 1.94r -- so the dot was capping a point that already
       existed. The point now CONTINUES the barb's own tangent at that vertex,
       `P1 - C1` for a quadratic, which is 1.07 rad off radial because these
       barbs hook hard. A point drawn radially would read as a spike glued onto
       a hook rather than as a hook that has been sharpened.
       Rick: "red razor sharp points ... fits the bloody theme better imo",
       then "lets shorten those spikes a bit" -- laddered at 1:1 and taken
       at %LEN%r. */
    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU;
      const d = (ang, k) => [Math.cos(ang) * r * k, Math.sin(ang) * r * k];
      const q = (A, C, B, t) => { const u = 1 - t;
        return [u*u*A[0] + 2*u*t*C[0] + t*t*B[0],
                u*u*A[1] + 2*u*t*C[1] + t*t*B[1]]; };
      /* the barb's own control net, restated. if these ever drift from the
         loop above, the point detaches from the barb -- which is the one way
         this can fail while still drawing something plausible. */
      const P0 = d(a - 0.22, 0.92), C1 = d(a + 0.34, 1.70),
            P1 = d(a + 0.86, 1.94), C2 = d(a + 0.34, 1.24),
            P2 = d(a + 0.24, 0.92);
      const B1 = q(P0, C1, P1, %BACK%), B2 = q(P1, C2, P2, %FRONT%);
      const tx = P1[0] - C1[0], ty = P1[1] - C1[1];
      const tl = Math.hypot(tx, ty) || 1;
      const AP = [P1[0] + tx / tl * r * %LEN%, P1[1] + ty / tl * r * %LEN%];
      SHAPES._needle(c, B1, AP, B2, %CONC%, p.core, p.glow, %GA%, %GW%);
    }
    c.restore();'''

ANCHOR_BARBED = "  _fhBarbed(c, D, p, spin){"


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly once, or refuse.

    A build that silently applied zero or two of its patches and then reported
    a hash is the failure mode every builder in this tree is arranged around.
    v37's `liquid_build.replace_span` discarded silently and ate the drain
    clock; this refuses instead.
    """
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--out", default="../02-chain/sc-redbarb.html")
    ap.add_argument("--len", type=float, default=POINT_LEN)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s = src_p.read_text(encoding="utf-8")
    print(f"\nBARB BUILD -- red razor points, len {A.len}r")
    print(f"  src {src_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}")

    tips = (NEW_TIPS.replace("%LEN%", f"{A.len:g}")
                    .replace("%CONC%", f"{CONC:g}")
                    .replace("%BACK%", f"{BACK:g}")
                    .replace("%FRONT%", f"{FRONT:g}")
                    .replace("%GA%", f"{GLOW_A:g}")
                    .replace("%GW%", f"{GLOW_W:g}"))

    s = one(s, ANCHOR_BARBED, NEEDLE + ANCHOR_BARBED, "1 _needle inserted")
    s = one(s, OLD_TIPS, tips, "2 _fhBarbed tips -> razor points")

    # The dot is gone, not merely unused. A dead branch left in place is how a
    # later reader concludes the tip is still a circle.
    if "r * 1.86, Math.sin(a) * r * 1.86, r * 0.13" in s:
        raise SystemExit("the old dot geometry is still in the file")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(src_p.read_text(encoding="utf-8")):+d} bytes)")
    print(f"\n  NEXT, and none of it is optional:")
    print(f"    python3 barb_probe.py --game {A.out} --built")
    print(f"    python3 engine_ab.py  --a {A.src} --b {A.out} --n 10")
    print(f"    python3 chain_audit.py\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
