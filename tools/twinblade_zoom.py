#!/usr/bin/env python3
"""THE THREE TWINBLADES IN MOTION, AT 1:1, CROPPED TO THE BALL.

    python3 twinblade_zoom.py --game ../02-chain/sc-health18.html

`SHAPES.twinblade`'s own comment states the thing that makes a still sheet
insufficient:

    at spin 5.7 the pair reads as a spinning cross, and the thing a viewer
    actually sees is the OUTER TRACE of the two blades

So a single arm on a black field is not the object under test. This is: the
relic in the hall, drawn by the real renderer at 1080 wide (k = 1, so sim units
ARE pixels), cropped to a box around the fighter, several frames apart so the
trace is sampled at different phases.

Three columns, and the third is the question:

    Widowmaker    bloodsworn twinblade   _tbBarbed       ships
    Spellbreaker  runic twinblade        _twinConjured   ships
    <provisional> umbral twinblade       _tbEaten        unworn

Same foe, same seed, same frames for all three, so the only variable is the
branch. The crop is presented at 1:1 and again at 3x NEAREST — nearest, not
lanczos, because an interpolating upscale invents edges and the question is
whether the edges are there.

Writes one PNG. Touches no build.
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

DONOR = "axiom"
PROVISIONAL = {
    "id": DONOR, "name": "Provisional", "aff": "umbral", "shape": "twinblade",
    "blades": [0, 0.5], "reach": 62, "width": 8, "artW": 30,
    "dmg": 10.38, "spin": 5.7, "mode": "spin", "mass": 1.1,
    "onHit": {"curse": 1},
    "ult": {"name": "Placeholder", "charge": 14, "kind": "nova", "radius": 240,
            "dmg": 12, "apply": {"curse": 3}, "knock": 200,
            "tip": "PLACEHOLDER"},
    "blurb": "Provisional.",
}

INJECT_JS = """(relic) => {
  const w = AC.WEAPONS.find(x => x.id === relic.id);
  if (!w) return "donor missing: " + relic.id;
  for (const k of Object.keys(w)) delete w[k];
  Object.assign(w, relic);
  return "ok";
}"""

SHOT_JS = """([id, foe, seed, steps, frames, box, gap]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  for (let i = 0; i < steps; i++) m.step(1/60);
  const me = m.a.w.id === id ? m.a : m.b;
  const out = [];
  const cv = document.getElementById('cv');
  for (let f = 0; f < frames; f++){
    AC.__draw(m);
    /* WORLD -> SCREEN, taken from Renderer.draw rather than guessed:
       draw() scales by k, then translates by (pad, arenaTop), and the sim is
       CONFIG.arena.w wide with `scale = aw / arena.w`. Getting this wrong
       crops a plausible-looking piece of the WRONG part of the hall, which is
       the failure mode a picture cannot report. */
    const R = AC.renderer;
    const cx = Math.round((R.pad + me.x * R.scale) * R.k);
    const cy = Math.round((R.arenaTop + me.y * R.scale) * R.k);
    const sx = cx - box/2, sy = cy - box/2;
    const clipped = sx < 0 || sy < 0 || sx + box > cv.width || sy + box > cv.height;
    const tmp = document.createElement('canvas');
    tmp.width = box; tmp.height = box;
    tmp.getContext('2d').drawImage(cv, sx, sy, box, box, 0, 0, box, box);
    out.push({ png: tmp.toDataURL('image/png'),
               t: +m.t.toFixed(2), theta: +me.theta.toFixed(2),
               cx: cx, cy: cy, clipped: clipped,
               canvas: cv.width + "x" + cv.height });
    for (let i = 0; i < gap; i++) m.step(1/60);
  }
  return out;
}"""

GEOM_JS = """() => ({ k: AC.renderer.k, pad: AC.renderer.pad,
                     scale: AC.renderer.scale, arenaTop: AC.renderer.arenaTop,
                     cw: document.getElementById('cv').width,
                     ch: document.getElementById('cv').height })"""


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-health18.html")
    ap.add_argument("--foe", default="heartwood")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--steps", type=int, default=66)
    ap.add_argument("--frames", type=int, default=4)
    ap.add_argument("--gap", type=int, default=3, help="sim steps between frames")
    ap.add_argument("--box", type=int, default=190)
    ap.add_argument("--zoom", type=int, default=3)
    ap.add_argument("--out", default="../twinblade-motion.png")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")

    COLS = [("widowmaker", "Widowmaker - bloodsworn  _tbBarbed  (ships)"),
            ("spellbreaker", "Spellbreaker - runic  _twinConjured  (ships)"),
            (DONOR, "provisional - umbral  _tbEaten  (THE CELL)")]

    cols = []
    with game(game_path=g) as (page, errors):
        print(page.evaluate(INJECT_JS, PROVISIONAL), "- relic injected")
        print("renderer geometry:", page.evaluate(GEOM_JS))
        for rid, label in COLS:
            shots = page.evaluate(
                SHOT_JS, [rid, A.foe, A.seed, A.steps, A.frames, A.box, A.gap])
            cols.append((label, [png(s["png"]) for s in shots],
                         [s["t"] for s in shots]))
            clipped = [s for s in shots if s["clipped"]]
            print(f"  {rid:<14} frames at t = "
                  + ", ".join(f"{s['t']:.2f}" for s in shots)
                  + f"   centre {shots[0]['cx']},{shots[0]['cy']}"
                  + f"   canvas {shots[0]['canvas']}"
                  + (f"   <-- {len(clipped)}/{len(shots)} CLIPPED OFF-CANVAS"
                     if clipped else ""))
        if errors:
            print("PAGE ERRORS:", errors[:5])

    B, Z = A.box, A.zoom
    PAD, LBL = 18, 24
    cw = B + PAD + B * Z
    sheet = Image.new("RGB", (PAD + len(cols) * (cw + PAD),
                              PAD + LBL + A.frames * (B * Z + PAD)),
                      (11, 9, 16))
    dr = ImageDraw.Draw(sheet)
    dr.text((PAD, 5), f"TWINBLADE IN MOTION - 1:1 and {Z}x nearest - "
                      f"v {A.foe}, seed {A.seed}", fill=(201, 162, 39))
    for ci, (label, imgs, ts) in enumerate(cols):
        x = PAD + ci * (cw + PAD)
        dr.text((x, PAD + 8), label, fill=(214, 200, 170))
        for fi, im in enumerate(imgs):
            y = PAD + LBL + fi * (B * Z + PAD)
            sheet.paste(im, (x, y + (B * Z - B) // 2))
            sheet.paste(im.resize((B * Z, B * Z), Image.NEAREST), (x + B + PAD, y))
    out = (HERE / A.out).resolve()
    sheet.save(out)
    print(f"{out.name}  {sheet.width}x{sheet.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
