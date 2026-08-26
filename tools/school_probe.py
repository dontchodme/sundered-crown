#!/usr/bin/env python3
"""DO TWO SCHOOLS SEPARATE? — pairwise colour distance, measured, per shape.

WHY THIS EXISTS
---------------
Three documents now assert the same thing without a number behind it:

    matrix §3.2   "Sanctified gold and dwarven orange are the closest pair in
                   the set and I do not believe they separate in a moving frame."
    night-plan §1.3  "On the scythe, the bow and the flail head they are nearly
                   the same weapon. Second-closest: vigil against bloodsworn."

Both readings came from an eye on a contact sheet. An eye is the right court of
final appeal — rule 7 — but it cannot tell you whether a proposed fix moved the
problem by a lot or a little, and it cannot rank seven schools against each
other on six shapes without drifting. That is 21 pairs x 6 shapes = 126
judgements, which is exactly the kind of thing an instrument should do first so
the eye only has to check the answer.

WHAT IT MEASURES
----------------
Every school rendered on every shape at 1:1, through the real SHAPES functions,
with the shadowBlur the live renderer puts on a weapon — because §1.2's finding
is that the school reads through the GLOW, so a measurement without the glow is
measuring something the viewer never sees.

Distance is **CIEDE2000**, not RGB and not dE76. That matters specifically here:
dE76 badly overstates distance in the yellow-orange region, which is the exact
region the sanctified/dwarven question lives in. Using it would have flattered
the palette and hidden the failure the eye already found.

Two statistics per pair, and they disagree usefully:

    mean   how different the two weapons are on average
    p10    the 10th percentile — how similar their MOST similar 10% of pixels
           are. A pair can have a healthy mean and still collide in the bulk,
           which is what "same weapon, different trim" looks like numerically.

WHAT COUNTS AS SEPARATED
------------------------
There is no absolute threshold for "two game assets read as different", so the
scale is calibrated from inside the build rather than invented: the pairs Rick
and the sheets have already accepted as distinct set the floor, and the pair
they rejected sets the ceiling. Run it once on the shipped palette and the
ranking IS the calibration.

  python3 school_probe.py --game sundered-crown-next.html
  python3 school_probe.py --override dwarven:core=#C8641E,dwarven:glow=#FFB067
  python3 school_probe.py --shapes scythe --pairs sanctified:dwarven
"""
from __future__ import annotations

import argparse
import base64
import io
import itertools
import pathlib

import numpy as np
from PIL import Image

from scpage import game

SCHOOLS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral", "runic", "vigil"]
DIM = {
    "greatsword": (116, 40), "warhammer": (76, 54), "scythe": (104, 46),
    "twinblade": (62, 30), "bow": (54, 44), "flailHead": (96, 52),
}
BG = np.array([11, 9, 16], dtype=np.float64)

JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  /* AFFINITIES is a live object on the page and an override MUTATES it. Without
     this, column 3's override is still in force when the next row draws column
     1, and the "before" column silently becomes an "after" column from row two
     onward -- the first sheet showed a white sanctified in every NOW cell but
     the top one. Snapshot once, restore before every draw. This is v12's "do
     not compare builds on a field that is not the field you think it is",
     wearing a different hat. */
  if (!window.__AFF0){
    window.__AFF0 = {};
    for (const k in AC.AFFINITIES) window.__AFF0[k] = Object.assign({}, AC.AFFINITIES[k]);
  }
  for (const k in AC.AFFINITIES) Object.assign(AC.AFFINITIES[k], window.__AFF0[k]);
  for (const ov of cfg.overrides){
    if (AC.AFFINITIES[ov[0]]) AC.AFFINITIES[ov[0]][ov[1]] = ov[2];
  }
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;
  const p  = AC.AFFINITIES[cfg.aff];
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  c.fillStyle = "#0B0910"; c.fillRect(0,0,1080,1920);
  c.save();
  c.translate(cfg.ox, cfg.oy);
  c.scale(s, s);
  if (cfg.glow){ c.shadowColor = p.core; c.shadowBlur = 20; }
  const fn = AC.SHAPES[cfg.shape];
  if (!fn) return null;
  if (cfg.shape === 'flailHead') fn(c, cfg.W, p, 0.5);
  else fn(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  return cv.toDataURL('image/png').slice(22);
}"""


# ---------------------------------------------------------------- colour ----
def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """rgb uint8-ish float array (...,3) in 0..255 -> CIE L*a*b*, D65."""
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T
    white = np.array([0.95047, 1.00000, 1.08883])
    t = xyz / white
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(np.clip(t, 1e-12, None)),
                 t / (3 * d * d) + 4.0 / 29.0)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def ciede2000(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    """Full CIEDE2000. Vectorised over the leading axes."""
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cb = (C1 + C2) / 2.0
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25.0 ** 7 + 1e-30)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360.0
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360.0
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, np.where(dhp < -180, dhp + 360, dhp))
    dhp = np.where((C1p * C2p) == 0, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2.0))
    Lbp = (L1 + L2) / 2.0
    Cbp = (C1p + C2p) / 2.0
    hsum = h1p + h2p
    hdiff = np.abs(h1p - h2p)
    hbp = np.where(C1p * C2p == 0, hsum,
                   np.where(hdiff <= 180, hsum / 2.0,
                            np.where(hsum < 360, (hsum + 360) / 2.0,
                                     (hsum - 360) / 2.0)))
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30))
         + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6))
         - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dTh = 30 * np.exp(-(((hbp - 275) / 25.0) ** 2))
    Rc = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7 + 1e-30))
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dTh)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                   + Rt * (dCp / Sc) * (dHp / Sh))


# ------------------------------------------------------------------ main ----
def shot(pg, **cfg) -> np.ndarray:
    png = pg.evaluate(JS, cfg)
    if png is None:
        raise SystemExit(f"SHAPES.{cfg['shape']} missing")
    im = Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB")
    # Crop in CANVAS pixels. The renderer draws at AC.renderer.scale (~2.03), so
    # a box sized in shape units clips every weapon at half its length.
    ox, oy, pad = cfg["ox"], cfg["oy"], 30
    r = cfg["L"] * cfg["scale"] * 1.45 + pad
    im = im.crop((int(ox - r), int(oy - r), int(ox + r), int(oy + r)))
    return np.asarray(im, dtype=np.float64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sundered-crown-next.html")
    ap.add_argument("--shapes", default="greatsword,warhammer,scythe,twinblade,bow,flailHead")
    ap.add_argument("--schools", default=",".join(SCHOOLS))
    ap.add_argument("--pairs", default="", help="a:b,c:d — restrict to these pairs")
    ap.add_argument("--override", default="",
                    help="school:field=hex,... applied at runtime, nothing written")
    ap.add_argument("--no-glow", action="store_true")
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args()

    here = pathlib.Path(__file__).parent
    shapes = [s.strip() for s in a.shapes.split(",") if s.strip()]
    schools = [s.strip() for s in a.schools.split(",") if s.strip()]
    overrides = []
    for tok in filter(None, (t.strip() for t in a.override.split(","))):
        lhs, hexv = tok.split("=")
        sch, fld = lhs.split(":")
        overrides.append([sch, fld, hexv])
    want = None
    if a.pairs:
        want = {frozenset(t.split(":")) for t in a.pairs.split(",") if t}

    glow = not a.no_glow
    ox, oy = 700, 900
    if overrides:
        print("runtime overrides: " + ", ".join(f"{s}.{f}={v}" for s, f, v in overrides))
    print(f"=== school separation, CIEDE2000 — {a.game}, "
          f"{'with renderer glow' if glow else 'shape ink only'} ===\n")

    per_pair = {}
    with game(game_path=(here / a.game).resolve()) as (pg, errs):
        scale = pg.evaluate("()=>{AC.setResolution(1080,1920);return AC.renderer.scale;}")
        for shape in shapes:
            L, W = DIM[shape]
            imgs = {s: shot(pg, shape=shape, aff=s, L=L, W=W, ox=ox, oy=oy,
                            glow=glow, overrides=overrides, scale=scale)
                    for s in schools}
            labs = {s: srgb_to_lab(v) for s, v in imgs.items()}
            inks = {s: (np.abs(v - BG).max(axis=-1) > 8) for s, v in imgs.items()}
            rows = []
            for s1, s2 in itertools.combinations(schools, 2):
                if want is not None and frozenset((s1, s2)) not in want:
                    continue
                mask = inks[s1] | inks[s2]
                if mask.sum() == 0:
                    continue
                d = ciede2000(labs[s1][mask], labs[s2][mask])
                mean, p10 = float(d.mean()), float(np.percentile(d, 10))
                rows.append((mean, p10, s1, s2))
                per_pair.setdefault((s1, s2), []).append(mean)
            rows.sort()
            print(f"-- {shape} --   (closest {min(a.top, len(rows))} pairs)")
            for mean, p10, s1, s2 in rows[:a.top]:
                bar = "#" * int(min(40, mean * 1.1))
                print(f"   {s1[:10]:<11}/{s2[:10]:<11} mean {mean:6.2f}  "
                      f"p10 {p10:6.2f}  {bar}")
            print()
        if errs:
            raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

    print("=== worst pairs across all shapes (mean of per-shape means) ===")
    agg = sorted(((sum(v) / len(v), k) for k, v in per_pair.items()))
    for m, (s1, s2) in agg[:a.top]:
        print(f"   {s1:<11}/{s2:<11} {m:6.2f}")
    print(f"\n   best in set: {agg[-1][1][0]}/{agg[-1][1][1]} {agg[-1][0]:.2f}")


if __name__ == "__main__":
    main()
