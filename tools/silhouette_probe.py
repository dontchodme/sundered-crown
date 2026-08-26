#!/usr/bin/env python3
"""IS IT A DIFFERENT WEAPON, OR THE SAME ONE PAINTED? — outline only.

    python3 silhouette_probe.py --game sundered-crown-next.html

WHY THIS AND NOT THE COLOUR PROBES
-----------------------------------
Rick, 2026-08-12:

  > *"while i like the idea of animations on every weapon. what i really ment
  >  was unique models/silhouettes for each weapon. animations are great. but
  >  whats important is that they are visually distinct"*

`school_probe.py` measures colour distance and `palette_probe.py` measures who
owns the pixels. Both are surface: they describe what happens INSIDE an outline
that never changes. This measures the outline.

It is also the honest instrument for the matrix doc's central finding — *"every
row is one silhouette in six colours"* — which has been quoted for three
sessions without a number attached, because the only sheet ever pulled for it
was in full colour, where the glow does the separating and hides the fact that
the shape does not.

METHOD
------
Every palette field is forced to the same flat white and the renderer's glow is
switched off, so what comes back is a **mask**: the weapon's footprint and
nothing else. Two masks are compared by **intersection over union**.

    IoU 1.00   pixel-identical outline. Two relics, one weapon.
    IoU 0.90   a detail moved. Visible on a sheet, invisible in motion.
    IoU < 0.7  genuinely different objects.

Masks are compared at a FIXED FACING, which is the generous case — two shapes
that share an outline standing still also share it turning. A pair that fails
here cannot be rescued downstream.

THE CALIBRATION IS INSIDE THE BUILD
------------------------------------
There is no universal threshold for "reads as a different weapon", so this does
not invent one. `twinblade` already branches per school: `_twinDagger` is a
forged dagger and `_twinConjured` is five floating shards. Rick has seen both
and kept both. **Whatever IoU that pair scores is what "distinct enough" means
in this game**, and every other pair is read against it. Same discipline as
`anim_sheet.py` calibrating against the shards.

  python3 silhouette_probe.py --types warhammer,scythe
"""
from __future__ import annotations

import argparse
import base64
import io
import itertools
import pathlib

import numpy as np
from PIL import Image, ImageDraw

from scpage import game

SCHOOLS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral", "runic", "vigil"]
DIM = {
    "greatsword": (116, 40), "warhammer": (76, 54), "scythe": (104, 46),
    "twinblade": (62, 30), "bow": (54, 44), "flailHead": (96, 52),
}

JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  if (!window.__AFF0){
    window.__AFF0 = {};
    for (const k in AC.AFFINITIES) window.__AFF0[k] = Object.assign({}, AC.AFFINITIES[k]);
  }
  for (const k in AC.AFFINITIES) Object.assign(AC.AFFINITIES[k], window.__AFF0[k]);
  /* FLATTEN THE PALETTE. Every field becomes the same white, so nothing the
     shape does with colour can register and the only thing left in the image is
     where it put ink. `key` is preserved -- it is what the per-school structural
     branches switch on, and flattening it would delete the very thing this tool
     exists to find. */
  const p = Object.assign({}, AC.AFFINITIES[cfg.aff]);
  p.core = p.glow = p.steel = p.dark = "#FFFFFF";
  AC.SHAPES._t = 0;
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.shadowBlur = 0; c.shadowColor = 'transparent';
  c.fillStyle = "#000000"; c.fillRect(0,0,1080,1920);

  /* --footprint: THE TRUE FOOTPRINT.
     The flatten above only reaches PALETTE FIELDS. Ink drawn with a hardcoded
     literal is not flattened, and if that literal is near-black it is also
     below the greyscale threshold -- so it is invisible to the mask twice over,
     silently, and the row reads as a plausible number for a smaller object.
     Measured 2026-08-13: the bow is 35-59% invisible this way and its IoU is
     0.350/0.476 published against 0.448/0.668 true. Every other shape <= 10%.
     `sundered-crown-blind-ink.md`.

     This forces every colour the shape asks for to white, ALPHA PRESERVED --
     alpha is kept because destination-out sites take their strength from the
     source alpha (depth_build --erase), so flattening it would change the
     footprint rather than reveal it.

     NOTE: this is NOT fixed by giving those literals to the palette. A helper
     that holds luminance returns near-black from a white input too. The
     instrument and the art are two jobs. */
  let undo = [];
  if (cfg.footprint){
    const proto = Object.getPrototypeOf(c);
    const wh = (v) => {
      if (typeof v !== 'string') return v;
      if (v[0] === '#'){
        if (v.length === 9) return '#FFFFFF' + v.slice(7);
        if (v.length === 5) return '#FFFF' + v[4] + v[4];
        return '#FFFFFF';
      }
      const m = v.match(/^rgba?\(([^)]*)\)/);
      if (m){ const q = m[1].split(',').map(x=>x.trim());
              return 'rgba(255,255,255,' + (q.length>3 ? q[3] : '1') + ')'; }
      return '#FFFFFF';
    };
    for (const k of ['fillStyle','strokeStyle','shadowColor']){
      const d = Object.getOwnPropertyDescriptor(proto, k);
      Object.defineProperty(c, k, { configurable:true,
        get(){ return d.get.call(c); }, set(v){ d.set.call(c, wh(v)); } });
      undo.push(k);
    }
    for (const g of ['createLinearGradient','createRadialGradient']){
      const orig = proto[g];
      c[g] = function(){ const gr = orig.apply(c, arguments);
        const acs = gr.addColorStop.bind(gr);
        gr.addColorStop = (o, col) => acs(o, wh(col));
        return gr; };
    }
  }
  c.save();
  c.translate(cfg.ox, cfg.oy);
  c.scale(s, s);
  const fn = AC.SHAPES[cfg.shape];
  if (!fn) return null;
  if (cfg.shape === 'flailHead') fn(c, cfg.W, p, 0.5);
  else fn(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  const out = cv.toDataURL('image/png').slice(22);
  if (cfg.footprint){
    for (const k of undo) delete c[k];
    delete c.createLinearGradient; delete c.createRadialGradient;
  }
  return out;
}"""


def mask(pg, shape, aff, ox, oy, scale, footprint=False, thresh=40):
    L, W = DIM[shape]
    png = pg.evaluate(JS, {"shape": shape, "aff": aff, "L": L, "W": W,
                           "ox": ox, "oy": oy, "footprint": footprint})
    im = Image.open(io.BytesIO(base64.b64decode(png))).convert("L")
    r = L * scale * 1.5 + 40
    im = im.crop((int(ox - r), int(oy - r), int(ox + r), int(oy + r)))
    return np.asarray(im, dtype=np.int16) > thresh


def pad_to(a, b):
    """Masks are cropped per type, so cross-type pairs arrive different sizes.
    Centre both in a common frame rather than resizing — resizing would rescale
    a weapon and make a long thin blade look like a short thick one."""
    h = max(a.shape[0], b.shape[0])
    w = max(a.shape[1], b.shape[1])
    out = []
    for m in (a, b):
        z = np.zeros((h, w), dtype=bool)
        y0, x0 = (h - m.shape[0]) // 2, (w - m.shape[1]) // 2
        z[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m
        out.append(z)
    return out


def iou(a, b):
    if a.shape != b.shape:
        a, b = pad_to(a, b)
    u = int((a | b).sum())
    return float((a & b).sum()) / u if u else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="sundered-crown-next.html")
    ap.add_argument("--types", default="greatsword,warhammer,scythe,twinblade,bow,flailHead")
    ap.add_argument("--sheet", default="",
                    help="also write the masks themselves. The table says HOW "
                         "identical; only the sheet says what you are looking at.")
    ap.add_argument("--footprint", action="store_true",
                    help="mask the TRUE footprint: force every colour the shape "
                         "asks for to white, not just the palette fields. Use this "
                         "on any build with near-black literals. See "
                         "sundered-crown-blind-ink.md.")
    a = ap.parse_args()
    here = pathlib.Path(__file__).parent
    types = [t.strip() for t in a.types.split(",") if t.strip()]
    ox, oy = 700, 900

    print(f"=== silhouette, colour stripped — {a.game}"
          f"{'  [--footprint: TRUE, literals included]' if a.footprint else ''} ===\n")
    print("WITHIN A TYPE: do the seven schools differ in OUTLINE?")
    print(f"{'type':<12}{'variants':>10}{'min IoU':>10}{'mean IoU':>10}   the split")
    within = {}
    per_type_masks = {}
    with game(game_path=(here / a.game).resolve()) as (pg, errs):
        scale = pg.evaluate("()=>{AC.setResolution(1080,1920);return AC.renderer.scale;}")
        for ty in types:
            ms = {s: mask(pg, ty, s, ox, oy, scale, a.footprint)
                  for s in SCHOOLS}
            per_type_masks[ty] = ms
            pairs = [(iou(ms[x], ms[y]), x, y)
                     for x, y in itertools.combinations(SCHOOLS, 2)]
            lo = min(pairs)
            mean = sum(p[0] for p in pairs) / len(pairs)
            # count distinct outlines: group schools whose masks are >0.995 alike
            groups = []
            for s in SCHOOLS:
                for g in groups:
                    if iou(ms[s], ms[g[0]]) > 0.995:
                        g.append(s)
                        break
                else:
                    groups.append([s])
            split = " | ".join("+".join(x[:4] for x in g) for g in groups)
            within[ty] = (len(groups), lo[0], mean)
            print(f"{ty:<12}{len(groups):>10}{lo[0]:>10.3f}{mean:>10.3f}   {split}")
        if a.sheet:
            CW = max(m.shape[1] for ms in per_type_masks.values()
                     for m in ms.values())
            CH = max(m.shape[0] for ms in per_type_masks.values()
                     for m in ms.values())
            CW, CH = min(CW, 380), min(CH, 380)
            GUT, TOP = 120, 30
            sh = Image.new("RGB", (GUT + CW * len(SCHOOLS), TOP + CH * len(types)),
                           (0, 0, 0))
            dr = ImageDraw.Draw(sh)
            dr.text((8, 8), f"SILHOUETTE ONLY — {a.game} — every palette field "
                            f"flattened to one white. If two cells look the same, "
                            f"they ARE the same.", fill=(210, 200, 185))
            for ci, s in enumerate(SCHOOLS):
                dr.text((GUT + ci * CW + 6, 20), s.upper(), fill=(150, 145, 135))
            for ri, ty in enumerate(types):
                dr.text((8, TOP + ri * CH + CH // 2), ty, fill=(150, 145, 135))
                for ci, s in enumerate(SCHOOLS):
                    m = per_type_masks[ty][s]
                    im = Image.fromarray((m * 255).astype(np.uint8)).convert("RGB")
                    x0 = max(0, (im.width - CW) // 2)
                    y0 = max(0, (im.height - CH) // 2)
                    im = im.crop((x0, y0, x0 + CW, y0 + CH))
                    sh.paste(im, (GUT + ci * CW, TOP + ri * CH))
            sh.save(here / a.sheet)
            print(f"\n{a.sheet}  {sh.size}")

        if errs:
            raise SystemExit("PAGE ERRORS:\n" + "\n".join(errs))

        print("\nACROSS TYPES (sanctified), for scale — this is what different looks like")
        cross = [(iou(per_type_masks[x]["sanctified"], per_type_masks[y]["sanctified"]),
                  x, y) for x, y in itertools.combinations(types, 2)]
        for v, x, y in sorted(cross, reverse=True)[:4]:
            print(f"   {x:<12}/{y:<12} {v:.3f}")

    tw = within.get("twinblade")
    print()
    if tw:
        print(f"CALIBRATION. `twinblade` is the one type that already branches per\n"
              f"school -- a forged dagger for six schools, five floating shards for\n"
              f"runic -- and Rick has seen both and kept both. It scores **IoU "
              f"{tw[1]:.3f}**.\nThat is what 'a different weapon' measures in this "
              f"game.")
    flat = [t for t, (n, _, _) in within.items() if n == 1]
    if flat:
        print(f"\n{len(flat)} of {len(types)} types have ONE outline for all seven "
              f"schools:\n   {', '.join(flat)}")
        print("At N=48 that is 8 silhouettes wearing 48 names, which is the matrix\n"
              "doc's §3 finding with a number on it at last.")


if __name__ == "__main__":
    main()
