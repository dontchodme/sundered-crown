#!/usr/bin/env python3
"""DOES `_scOuter`'s NORMAL POINT WHERE THE CALLERS THINK IT DOES?

    python3 scouter_check.py                 # check the shipped artifact
    python3 scouter_check.py --selftest      # prove every check can go both ways
    python3 scouter_check.py --consequence   # what the wrong sign actually costs
    python3 scouter_check.py --sheet out.png # before/after render, all 7 schools

WHY
---
`SHAPES._scOuter(L, W, u)` returns a point on the scythe crescent's outer
bezier and a normal `(nx, ny)`. Six scythe grammars ride that normal: the
serrations, the barbs, the halo rays, the piercings, the bolted spine strap,
the plates. The sign has never been checked by anything but an eye, and the
in-file comment at the crescent-crack site claims it "points into the concave
side" -- which is the OPPOSITE of what most call sites assume when they write
`q.x + q.nx * W*0.10` for a feature they describe as riding the OUTER edge.
One of the two is wrong.

WHAT COUNTS AS FAILURE -- stated before the numbers, so it cannot be
retrofitted to whatever came back:

  C1  UNIT      FAIL if any sample has | ‖n‖ - 1 | > 1e-9.
  C2  PERPENDICULAR
                FAIL if any interior sample has |n . t_fd| > 2e-3, where t_fd
                is the unit tangent from a CENTRAL FINITE DIFFERENCE of
                `_scOuter`'s own returned position. The normal must be normal
                to the curve the function actually traces, not to a derivative
                transcribed into this file.
  C3  NO FLIP   FAIL if sign(cross(t_fd, n)) is not the SAME at every interior
                sample. A curve whose normal changes handedness partway along
                cannot be offset consistently by anything.
  C4  SIDE      The call sites are the specification (see CALLERS): their
                consensus is that `+n` points OUT OF the blade, off the back.
                Measured by stepping a hairline eps along +n and asking the
                SHIPPED `_scCrescent` path, via isPointInPath, whether that
                landed in the blade. FAIL if `q + n*eps` is inside for any
                interior sample.
  C5  CALL SITES
                For each site, the offset DIRECTION is compared with the
                locally-measured outward direction at that same u. FAIL if any
                site moves toward the side its own comment says it does not.
                Direction, not membership: `+n * 0.34W` on a blade 0.3W thick
                exits the far side, and "outside past the cutting edge" is not
                "outside on the back" however the membership test scores it.

C4/C5 use the shipped `_scCrescent` path, and the inside-test is itself
validated against a known-inside and a known-outside point before any side
verdict is reported.

CAN THIS CHECK FAIL?
--------------------
`--selftest` runs the real file and four patched copies and requires EVERY
check to be observed taking both values. This matters more than usual here,
because the real file is already RED on C4/C5: a red that is stuck red proves
nothing, so the discriminating demonstration is the sign-flipped copy turning
C4/C5 GREEN while C1-C3 stay green.

    --patch scale   ‖n‖ doubled                   -> C1 red
    --patch skew    normal rotated 30 deg         -> C2 red
    --patch half    sign flipped only for u > 0.5 -> C3 red
    --patch flip    sign flipped everywhere       -> C4, C5 green

`flip` is also the candidate FIX. It is not applied by this tool: it moves a
shipped, approved silhouette, and `--sheet` exists to show by how much.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys
import tempfile

from PIL import Image, ImageDraw

from scpage import game

HERE = pathlib.Path(__file__).parent


def resolve(name: str) -> pathlib.Path:
    """The html sits beside tools/ in this checkout and inside it in others."""
    for cand in (pathlib.Path(name), HERE / name, HERE.parent / name):
        if cand.exists():
            return cand.resolve()
    raise SystemExit(f"cannot find {name}")


GAME = "sundered-crown.html"

# The scythe's real art dimensions, from silhouette_probe.DIM.
L_DEF, W_DEF = 104.0, 46.0

SCHOOLS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral",
           "runic", "vigil"]
SC_FN = {"sanctified": "_scRadiant", "bloodsworn": "_scBarbed",
         "dwarven": "_scBuilt", "verdant": "_scGrown", "umbral": "_scEaten",
         "runic": "_scConjured", "vigil": "_scPlated"}

ORIG = "return { x, y, nx: ty / m, ny: -tx / m, a: Math.atan2(ty, tx) };"
PATCH = {
    "flip":  "return { x, y, nx: -ty / m, ny: tx / m, a: Math.atan2(ty, tx) };",
    "half":  ("const _sg = u > 0.5 ? -1 : 1; "
              "return { x, y, nx: _sg*ty / m, ny: -_sg*tx / m, "
              "a: Math.atan2(ty, tx) };"),
    "scale": "return { x, y, nx: 2*ty / m, ny: -2*tx / m, a: Math.atan2(ty, tx) };",
    "skew":  ("const _C=Math.cos(0.5235987756), _S=Math.sin(0.5235987756); "
              "return { x, y, nx: (ty*_C - (-tx)*_S)/m, ny: ((-tx)*_C + ty*_S)/m, "
              "a: Math.atan2(ty, tx) };"),
}

# The sanctified piercings, for --consequence. Turning the loop off must change
# the render if the holes remove anything.
PIERCE_ON = '''    c.globalCompositeOperation = "destination-out";
    for (let i = 1; i <= 4; i++){
      const q = SHAPES._scOuter(L, W, i / 5);'''
PIERCE_OFF = '''    c.globalCompositeOperation = "destination-out";
    for (let i = 1; i <= 0; i++){
      const q = SHAPES._scOuter(L, W, i / 5);'''

# ---------------------------------------------------------------- CALL SITES --
# Read off the source, 2026-08-14. `side` is what the call site's OWN comment
# says the offset is for -- not what this tool would like to be true. Sites
# whose comment does not commit to a side get side=None: they are reported but
# not scored, because scoring them would be inventing a spec.
#
#   sign  the sign the code multiplies nx/ny by
#   d     the offset distance, in units of W
CALLERS = [
    # _scGrown, "inner serration" -- teeth cut into the blade.
    dict(fn="_scGrown  serration", us=[i / 7 for i in range(1, 7)],
         sign=-1, d=0.19, side="in", note='"inner serration"'),
    # _scBarbed: "the blade cuts on the INSIDE of the curve, so the barbs go on
    # the OUTSIDE, where they drag on the way out".
    dict(fn="_scBarbed barbs", us=[i / 6 for i in range(1, 6)],
         sign=+1, d=0.34, side="out", note='"the barbs go on the OUTSIDE"'),
    # _scRadiant: rays reaching from the blade out to the halo standing off the
    # back.
    dict(fn="_scRadiant rays", us=[i / 5 for i in range(1, 5)],
         sign=+1, d=0.40, side="out",
         note='"a second arc standing off the back"'),
    # _scRadiant: "pierced spine" -- destination-out holes THROUGH the blade.
    dict(fn="_scRadiant pierce", us=[i / 5 for i in range(1, 5)],
         sign=-1, d=0.30, side="in", note='"pierced spine", destination-out'),
    # _scBuilt: "a reinforcing spine strap bolted along the crescent's back".
    dict(fn="_scBuilt  strap", us=[0.06] + [0.06 + 0.88 * i / 8 for i in range(1, 9)],
         sign=+1, d=0.04, side="out",
         note='"bolted along the crescent\'s back"'),
    dict(fn="_scBuilt  bolts", us=[0.10 + 0.26 * i for i in range(4)],
         sign=+1, d=0.04, side="out", note="rides the strap"),
    # _scPlated: "five plates riding the OUTER edge, so the back of the blade is
    # armoured and the cutting edge is bare".
    dict(fn="_scPlated plates", us=[0.10 + 0.20 * i for i in range(5)],
         sign=+1, d=0.10, side="out", note='"riding the OUTER edge"'),
    # _scEaten. Its comment says the bites come out of the CUTTING edge, but it
    # places them on the OUTER curve nudged by a hairline 0.02W -- comment and
    # code already disagree about which edge, so this site names no side.
    dict(fn="_scEaten  bites", us=[0.32, 0.66],
         sign=+1, d=0.02, side=None,
         note="hairline 0.02W; comment names the inner edge"),
    dict(fn="_scEaten  leaks", us=[0.30, 0.62],
         sign=-1, d=0.90, side=None, note="no side named in comment"),
]

JS = r"""(cfg) => {
  const S = AC.SHAPES, L = cfg.L, W = cfg.W, N = cfg.n, h = cfg.h;
  const OX = cfg.ox, OY = cfg.oy;
  const cv = document.createElement('canvas');
  cv.width = 640; cv.height = 480;
  const c = cv.getContext('2d');

  /* The inside-test uses the SHIPPED crescent path. Build it under a
     translation so every query point sits at positive canvas coordinates,
     then query in canvas space (isPointInPath ignores the CTM). */
  const inside = (x, y) => {
    c.setTransform(1,0,0,1,OX,OY);
    S._scCrescent(c, L, W);
    c.setTransform(1,0,0,1,0,0);
    return c.isPointInPath(x + OX, y + OY);
  };
  const at = (u) => S._scOuter(L, W, u);

  /* VALIDATE THE INSTRUMENT BEFORE TRUSTING IT. The midpoint between the outer
     curve and the inner curve must read inside; a point a mile off the back
     must read outside. Both come from the shipped control points, so this goes
     loud if isPointInPath is not doing what this tool thinks it is. */
  const bez = (a,b,cc,d,u) => { const it=1-u;
    return it*it*it*a + 3*it*it*u*b + 3*it*u*u*cc + u*u*u*d; };
  const innerX = (u) => bez(L*0.56, L*0.88, L*0.86, L*0.66, u);
  const innerY = (u) => bez(-W*1.32, -W*0.72, -W*0.10, W*0.30, u);
  const probe = [];
  for (const u of [0.3, 0.5, 0.7]){
    const q = at(u), ix = innerX(1-u), iy = innerY(1-u);
    probe.push({ mid: inside((q.x+ix)/2, (q.y+iy)/2),
                 far: inside(q.x + 500, q.y) });
  }

  /* Local outward direction, MEASURED, not assumed: step a hairline each way
     along n and ask the path which step left the blade. */
  const orient = (q) => {
    const p = inside(q.x + q.nx*cfg.eps, q.y + q.ny*cfg.eps);
    const m = inside(q.x - q.nx*cfg.eps, q.y - q.ny*cfg.eps);
    if (p && !m) return -1;      // -n is outward
    if (m && !p) return +1;      // +n is outward
    return 0;                    // degenerate: both in, or both out (a cusp)
  };

  const rows = [];
  for (let i = 0; i <= N; i++){
    const u = i / N;
    const q = at(u);
    const ua = Math.max(0, u - h), ub = Math.min(1, u + h);
    const qa = at(ua), qb = at(ub);
    const dx = qb.x - qa.x, dy = qb.y - qa.y;
    const dm = Math.hypot(dx, dy);
    rows.push({ u, x:q.x, y:q.y, nx:q.nx, ny:q.ny,
                tx: dm ? dx/dm : 0, ty: dm ? dy/dm : 0,
                speed: dm / (ub - ua),
                inPlus:  inside(q.x + q.nx*cfg.eps, q.y + q.ny*cfg.eps),
                inMinus: inside(q.x - q.nx*cfg.eps, q.y - q.ny*cfg.eps),
                orient: orient(q) });
  }

  const sites = [];
  for (const s of cfg.callers){
    for (const u of s.us){
      const q = at(u);
      const px = q.x + s.sign * q.nx * W * s.d;
      const py = q.y + s.sign * q.ny * W * s.d;
      const o = orient(q);
      /* Which side did the offset MOVE toward? o is the sign of n that points
         out of the blade, so moving along sign*n goes outward iff they agree. */
      const dir = o === 0 ? "?" : (s.sign === o ? "out" : "in");
      sites.push({ fn: s.fn, u, side: s.side, sign: s.sign, d: s.d,
                   dir, orient: o, inside: inside(px, py) });
    }
  }
  return { rows, sites, probe };
}"""

RENDER_JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  const p = Object.assign({}, AC.AFFINITIES[cfg.aff]);
  AC.SHAPES._t = 0;
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  c.fillStyle = "#000000"; c.fillRect(0,0,1080,1920);
  c.save();
  c.translate(cfg.ox, cfg.oy); c.scale(s, s);
  AC.SHAPES.scythe(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  return { png: cv.toDataURL('image/png').slice(22), s };
}"""


def patched(src: pathlib.Path, mode: str) -> pathlib.Path:
    text = src.read_text()
    if text.count(ORIG) != 1:
        raise SystemExit(f"expected exactly 1 `_scOuter` return, found "
                         f"{text.count(ORIG)} -- the patch anchor moved")
    out = pathlib.Path(tempfile.mkdtemp()) / src.name
    out.write_text(text.replace(ORIG, PATCH[mode]))
    return out


def pierce_off(src: pathlib.Path) -> pathlib.Path:
    text = src.read_text()
    if text.count(PIERCE_ON) != 1:
        raise SystemExit(f"pierce anchor found {text.count(PIERCE_ON)} times")
    out = pathlib.Path(tempfile.mkdtemp()) / src.name
    out.write_text(text.replace(PIERCE_ON, PIERCE_OFF))
    return out


def run(game_path, n, h, eps):
    with game(game_path=game_path) as (pg, errors):
        res = pg.evaluate(JS, {
            "L": L_DEF, "W": W_DEF, "n": n, "h": h, "eps": eps,
            "ox": 60.0, "oy": 260.0,
            "callers": [{k: v for k, v in c.items()
                         if k in ("fn", "us", "sign", "d", "side")}
                        for c in CALLERS]})
        if errors:
            raise SystemExit("page errors: " + "; ".join(errors))
    res["eps"] = eps
    return res


def shot(pg, aff, ox=700, oy=900):
    r = pg.evaluate(RENDER_JS, {"aff": aff, "L": L_DEF, "W": W_DEF,
                                "ox": ox, "oy": oy})
    im = Image.open(io.BytesIO(base64.b64decode(r["png"]))).convert("RGB")
    s = r["s"]
    box = (int(ox - L_DEF * s * 0.35), int(oy - W_DEF * s * 2.6),
           int(ox + L_DEF * s * 1.35), int(oy + W_DEF * s * 1.4))
    return im.crop(box)


def analyse(res, *, quiet=False, table=True):
    rows, sites, probe = res["rows"], res["sites"], res["probe"]

    bad = [p for p in probe if not p["mid"] or p["far"]]
    if bad:
        raise SystemExit(f"INSIDE-TEST IS BROKEN: {bad} -- refusing to report a "
                         "side verdict from an instrument that cannot tell the "
                         "blade from empty space")

    interior = [r for r in rows if 0.02 <= r["u"] <= 0.98]

    worst_unit = max(abs((r["nx"] ** 2 + r["ny"] ** 2) ** 0.5 - 1) for r in rows)
    c1 = worst_unit <= 1e-9

    worst_dot = max(abs(r["nx"] * r["tx"] + r["ny"] * r["ty"]) for r in interior)
    c2 = worst_dot <= 2e-3

    signs = [1 if (r["tx"] * r["ny"] - r["ty"] * r["nx"]) > 0 else -1
             for r in interior]
    npos, nneg = signs.count(1), signs.count(-1)
    c3 = npos == 0 or nneg == 0
    flips = [interior[i]["u"] for i in range(1, len(signs))
             if signs[i] != signs[i - 1]]

    n_plus_in = sum(1 for r in interior if r["inPlus"])
    n_minus_in = sum(1 for r in interior if r["inMinus"])
    degen = [r["u"] for r in interior if r["orient"] == 0]
    c4 = n_plus_in == 0                      # callers' consensus: +n is OUT

    scored = [s for s in sites if s["side"]]
    wrong = [s for s in scored if s["dir"] != s["side"]]
    c5 = not wrong

    if not quiet:
        print(f"  samples {len(rows)}  (interior {len(interior)})   "
              f"L={L_DEF:g} W={W_DEF:g}   eps={res.get('eps', '')}")
        print(f"  C1 ‖n‖ = 1              worst |‖n‖-1| = {worst_unit:.3e}"
              f"        {'PASS' if c1 else 'FAIL'}")
        print(f"  C2 n . t_fd = 0         worst |dot|   = {worst_dot:.3e}"
              f"        {'PASS' if c2 else 'FAIL'}")
        print(f"  C3 handedness           cross>0: {npos:5d}   cross<0: {nneg:5d}"
              f"   {'PASS' if c3 else 'FAIL'}")
        if flips:
            print("       flips at u = "
                  + ", ".join(f"{u:.4f}" for u in flips[:8])
                  + (" ..." if len(flips) > 8 else ""))
        print(f"  C4 which side is blade  +n*eps inside: {n_plus_in:5d}/{len(interior)}"
              f"   -n*eps inside: {n_minus_in:5d}/{len(interior)}"
              f"  {'PASS' if c4 else 'FAIL'}")
        print("     (callers' consensus, from their own comments: +n is OUTSIDE)")
        if degen:
            print(f"     {len(degen)} degenerate samples (both/neither side in): "
                  f"u = {degen[0]:.3f} .. {degen[-1]:.3f}")
        print(f"  C5 call sites           {len(scored) - len(wrong)}/{len(scored)}"
              f" move toward the side their comment names   "
              f"{'PASS' if c5 else 'FAIL'}")
        print(f"  fyi min |dP/du| = {min(r['speed'] for r in rows):.2f} "
              f"(0 would be a cusp, where the normal is undefined)")
        if table:
            print()
            print("  call site                 u      offset     moves   lands"
                  "        comment says")
            print("  " + "-" * 76)
            for s in sites:
                sgn = "+" if s["sign"] > 0 else "-"
                off = f"{sgn}n*{s['d']:.2f}W"
                lands = "in blade" if s["inside"] else (
                    "off back" if s["dir"] == "out" else "past edge")
                want = s["side"] or "--"
                mark = "" if not s["side"] else (
                    "  ok" if s["dir"] == s["side"] else "  <-- WRONG")
                print(f"  {s['fn']:<22} {s['u']:.3f}  {off:>9}   {s['dir']:>5}"
                      f"   {lands:>9}   {want:>4}{mark}")

    ok = c1 and c2 and c3 and c4 and c5
    return ok, dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5,
                    worst_unit=worst_unit, worst_dot=worst_dot,
                    npos=npos, nneg=nneg, flips=flips,
                    n_plus_in=n_plus_in, n_minus_in=n_minus_in,
                    n_interior=len(interior), n_wrong=len(wrong),
                    n_scored=len(scored))


def do_consequence(src, out_png):
    """Does the wrong sign actually cost anything? Two renders answer it.

    A: the sanctified scythe as shipped.
    B: the same file with the `pierced spine` destination-out loop turned OFF.

    If the piercings remove ink, A != B. If A == B to the pixel, the holes are
    landing off the blade and the pierced spine does not exist in the picture.
    """
    import numpy as np
    print("== CONSEQUENCE: the sanctified 'pierced spine' ==")
    with game(game_path=src) as (pg, e):
        a = shot(pg, "sanctified")
        if e:
            raise SystemExit("page errors: " + "; ".join(e))
    off = pierce_off(src)
    with game(game_path=off) as (pg, e):
        b = shot(pg, "sanctified")
        if e:
            raise SystemExit("page errors: " + "; ".join(e))
    fix = patched(src, "flip")
    with game(game_path=fix) as (pg, e):
        cimg = shot(pg, "sanctified")
        if e:
            raise SystemExit("page errors: " + "; ".join(e))
    A = np.asarray(a, dtype=np.int16)
    B = np.asarray(b, dtype=np.int16)
    C = np.asarray(cimg, dtype=np.int16)
    d_ab = np.abs(A - B)
    d_ac = np.abs(A - C)
    print(f"  shipped  vs  piercings switched OFF : "
          f"{int((d_ab.max(axis=2) > 0).sum()):6d} px differ, "
          f"max channel delta {int(d_ab.max())}")
    print(f"  shipped  vs  sign flipped           : "
          f"{int((d_ac.max(axis=2) > 0).sum()):6d} px differ, "
          f"max channel delta {int(d_ac.max())}")
    print("  => the piercings are centred 0.30W off the BACK of the blade, which")
    print("     is empty space -- except that the halo arc lives there. What the")
    print("     'pierced spine' removes in the shipped render is the HALO. Look")
    print("     at the sheet: the outer arc is chopped into segments, and the")
    print("     spine has no holes in it at all.")
    if out_png:
        w, h = a.size
        sheet = Image.new("RGB", (w * 3 + 40, h + 26), (12, 12, 16))
        for i, (im, lab) in enumerate([(a, "shipped"), (b, "pierce loop OFF"),
                                       (cimg, "sign flipped")]):
            sheet.paste(im, (i * (w + 20), 22))
            ImageDraw.Draw(sheet).text((i * (w + 20) + 4, 6), lab,
                                       fill=(210, 210, 220))
        sheet.save(out_png)
        print(f"  wrote {out_png}")


def do_sheet(src, out_png):
    """Before/after render: every scythe school, shipped vs sign flipped."""
    import numpy as np
    print("== SHEET: shipped vs sign-flipped, all seven scythe schools ==")
    ims = {}
    with game(game_path=src) as (pg, e):
        for s in SCHOOLS:
            ims[("a", s)] = shot(pg, s)
        if e:
            raise SystemExit("page errors: " + "; ".join(e))
    fix = patched(src, "flip")
    with game(game_path=fix) as (pg, e):
        for s in SCHOOLS:
            ims[("b", s)] = shot(pg, s)
        if e:
            raise SystemExit("page errors: " + "; ".join(e))
    print(f"  {'school':<12}{'fn':<13}{'px differ':>11}{'% of frame':>12}"
          f"{'max delta':>11}")
    for s in SCHOOLS:
        A = np.asarray(ims[("a", s)], dtype=np.int16)
        B = np.asarray(ims[("b", s)], dtype=np.int16)
        d = np.abs(A - B)
        n = int((d.max(axis=2) > 0).sum())
        tot = A.shape[0] * A.shape[1]
        print(f"  {s:<12}{SC_FN[s]:<13}{n:>11d}{100 * n / tot:>11.2f}%"
              f"{int(d.max()):>11d}")
    w, h = ims[("a", SCHOOLS[0])].size
    sheet = Image.new("RGB", (w * len(SCHOOLS) + 8, h * 2 + 46), (12, 12, 16))
    dr = ImageDraw.Draw(sheet)
    for i, s in enumerate(SCHOOLS):
        sheet.paste(ims[("a", s)], (i * w + 4, 20))
        sheet.paste(ims[("b", s)], (i * w + 4, h + 40))
        dr.text((i * w + 8, 6), f"{s} / {SC_FN[s]}", fill=(210, 210, 220))
    dr.text((6, h + 26), "SIGN FLIPPED (candidate fix, NOT applied)",
            fill=(255, 170, 120))
    dr.text((6, h + 6), "", fill=(200, 200, 200))
    sheet.save(out_png)
    print(f"  wrote {out_png}  (top row shipped, bottom row sign flipped)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=GAME)
    ap.add_argument("--n", type=int, default=2000, help="samples of u")
    ap.add_argument("--h", type=float, default=1e-4, help="finite-diff step in u")
    ap.add_argument("--eps", type=float, default=0.25,
                    help="side-test offset, local units (W=46, so 0.25 ~ 0.005W)")
    ap.add_argument("--patch", choices=sorted(PATCH), default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--consequence", nargs="?", const="", default=None,
                    metavar="PNG")
    ap.add_argument("--sheet", default=None, metavar="PNG")
    a = ap.parse_args()

    src = resolve(a.game)

    def one(path, label, table=True):
        print(f"== {label} ==  {path.name}")
        ok, v = analyse(run(path, a.n, a.h, a.eps), table=table)
        print(f"  VERDICT: {'PASS' if ok else 'FAIL'}\n")
        return ok, v

    if a.consequence is not None:
        do_consequence(src, a.consequence or None)
        return 0
    if a.sheet:
        do_sheet(src, a.sheet)
        return 0

    if a.selftest:
        ok_real, v = one(src, "REAL FILE")
        vs = {}
        for m in ("scale", "skew", "half", "flip"):
            _, vs[m] = one(patched(src, m), f"PATCH {m}", table=False)
        print("SELFTEST -- is every check able to take BOTH values?")
        rules = [
            ("C1", v["c1"], not vs["scale"]["c1"], "scale"),
            ("C2", v["c2"], not vs["skew"]["c2"], "skew"),
            ("C3", v["c3"], not vs["half"]["c3"], "half"),
            ("C4", vs["flip"]["c4"], not v["c4"], "flip"),
            ("C5", vs["flip"]["c5"], not v["c5"], "flip"),
        ]
        allok = True
        for name, green, red, via in rules:
            good = green and red
            allok &= good
            print(f"  {name}: seen PASS {'yes' if green else 'NO '}   "
                  f"seen FAIL {'yes' if red else 'NO '}   (via --patch {via})"
                  f"   {'ok' if good else '<-- CHECK IS STUCK'}")
        if not allok:
            print("  SELFTEST FAILED -- a check that cannot change its answer "
                  "is not measuring anything.")
            return 2
        print("  selftest OK: all five checks discriminate.\n")
        return 0 if ok_real else 1

    path = patched(src, a.patch) if a.patch else src
    ok, _ = one(path, a.patch or "REAL FILE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
