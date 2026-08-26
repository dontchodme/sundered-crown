#!/usr/bin/env python3
"""THE THREEFOLD, PHOTOGRAPHED BY STEPPING THE SIMULATION.

    python3 twinshade_strip.py --game ../02-chain/sc-twinshade.html

`ult_filmstrip.py` CANNOT PHOTOGRAPH THIS and neither could it photograph
Interment (v36 §6a): it hand-constructs `m.ultFx`, never calls `fireUlt` and
never steps, which is right for six drawn set-pieces and useless for an
ultimate whose whole content is three bodies moving. It produced seven
identical frames of nothing happening and reported no error.

This steps a real match and captures at real times, so what is on the sheet is
what the sim did. Two sheets:

  --- the strip ---  full frames across the window: before the cast, the split
                     itself, the middle of it, the gutter, and after.
  --- the zoom  ---  the caster at 1:1 and 3x nearest, because the fire is
                     ~34px of ball and a downscaled strip cannot say whether
                     it reads as fire or as a purple smear.

Writes PNGs. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
ID = "twinshade"
W, H = 1080, 1920

SHOT_JS = """([id, foe, seed, box]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const cv = document.getElementById('cv');
  const out = [];
  const grab = (label, extra) => {
    const R = AC.renderer;
    const cx = Math.round((R.pad + me.x * R.scale) * R.k);
    const cy = Math.round((R.arenaTop + me.y * R.scale) * R.k);
    AC.__draw(m);
    const sx = cx - box/2, sy = cy - box/2;
    const tmp = document.createElement('canvas');
    tmp.width = box; tmp.height = box;
    tmp.getContext('2d').drawImage(cv, sx, sy, box, box, 0, 0, box, box);
    out.push({ label, shades: m.shades.length, drains: m.drains.length,
               k: me.ultSplit ? +(me.ultSplit.k || 0).toFixed(2) : 0,
               hold: m.splitHold ? (m.splitHold.rejoin ? "rejoin" : "split") : "-",
               hp: Math.round(me.hp), t: +m.t.toFixed(2), extra: extra || "",
               full: cv.toDataURL('image/png'), zoom: tmp.toDataURL('image/png') });
  };
  /* WAIT FOR A NATURAL CAST. Forcing one photographs a hall that frame one
     arranged rather than one that eighteen seconds of fighting did, and the
     whole question here is what this looks like in a real fight. */
  let g = 0;
  while (!m.splitHold && !m.over && g++ < DT_FPS * 100) m.step(DT);
  if (!m.splitHold) return { error: "no natural cast in 100s" };
  /* every loop below gets its OWN budget */
  const spin = (test, cap) => { let n = 0; while (test() && n++ < cap) m.step(DT); };
  grab("the cast");
  const hold = m.splitHold, hdur = hold.dur;
  for (const frac of [0.30, 0.60, 0.88]){
    spin(() => m.splitHold && m.splitHold.t < hdur * frac, 400);
    grab("dividing " + Math.round(frac * 100) + "%");
  }
  spin(() => !!m.splitHold, 400);
  grab("released");
  /* a burning frame WITH A DRAIN IN FLIGHT, because the drain is the note and
     an average frame does not happen to have one */
  spin(() => !m.over && m.shades.length && m.drains.length === 0, DT_FPS * 8);
  grab("burning", m.drains.length ? "drain x" + m.drains.length : "no drain");
  /* run to the reunion — it has to arrive on its own */
  spin(() => !m.over && !(m.splitHold && m.splitHold.rejoin), DT_FPS * 90);
  if (m.splitHold && m.splitHold.rejoin){
    const rd = m.splitHold.dur;
    for (const frac of [0.35, 0.80]){
      spin(() => m.splitHold && m.splitHold.t < rd * frac, 400);
      grab("rejoining " + Math.round(frac * 100) + "%");
    }
    spin(() => !!m.splitHold, 400);
  }
  grab("after");
  return { frames: out, dur: 0, foeHp: Math.round(th.hp), endWall: 0 };
}"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def sheet(tiles, labels, out, scale, title, nearest=False, cols=None):
    n = len(tiles)
    cols = cols or n
    rows = (n + cols - 1) // cols
    tw = int(tiles[0].width * scale)
    th = int(tiles[0].height * scale)
    PAD, LBL = 14, 30
    im = Image.new("RGB", (PAD + cols * (tw + PAD), PAD + LBL + rows * (th + PAD + LBL)),
                   (11, 9, 16))
    dr = ImageDraw.Draw(im)
    dr.text((PAD, 6), title, fill=(201, 162, 39))
    r = Image.NEAREST if nearest else Image.LANCZOS
    for i, (t, lab) in enumerate(zip(tiles, labels)):
        cx, cy = i % cols, i // cols
        x = PAD + cx * (tw + PAD)
        y = PAD + LBL + cy * (th + PAD + LBL)
        im.paste(t.resize((tw, th), r), (x, y + LBL))
        dr.text((x + 2, y + 2), lab, fill=(214, 200, 170))
    im.save(out)
    print(f"  {out.name}  {im.width}x{im.height}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--foe", default="lightkeeper")
    ap.add_argument("--seed", type=int, default=113967)
    ap.add_argument("--box", type=int, default=430)
    ap.add_argument("--zoom", type=int, default=3)
    ap.add_argument("--scale", type=float, default=0.30)
    ap.add_argument("--outdir", default="../05-reference/v37")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    outdir = (HERE / A.outdir).resolve(); outdir.mkdir(parents=True, exist_ok=True)

    with game(game_path=g) as (page, errors):
        r = page.evaluate(SHOT_JS, [ID, A.foe, A.seed, A.box])
        if r.get("error"):
            sys.exit(r["error"])
        if errors:
            print("PAGE ERRORS:", errors[:4])

    fr = r["frames"]
    print(f"natural cast · {len(fr)} frames, keyed off the two HOLDS rather "
          f"than off the hall clock")
    labs = [f"{f['label']}  [{f['hold']}]  shades {f['shades']}  "
            f"fire {f['k']}  drains {f['drains']}  hp {f['hp']}  {f['extra']}"
            for f in fr]
    for f, l in zip(fr, labs):
        print(f"    {l}")

    sheet([png(f["full"]) for f in fr], labs,
          outdir / "threefold-strip.png", A.scale,
          f"TRIPLICATE — stepped, natural cast — v {A.foe}, seed {A.seed}",
          cols=4)
    sheet([png(f["zoom"]) for f in fr], labs,
          outdir / "threefold-fire.png", A.zoom,
          f"THE FIRE — the caster at {A.zoom}x NEAREST "
          f"(an interpolating upscale invents edges)", nearest=True, cols=4)
    return 0


if __name__ == "__main__":
    sys.exit(main())
