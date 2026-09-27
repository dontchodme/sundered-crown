#!/usr/bin/env python3
"""THE STAFF ROW'S ART — THE CONCEPT SHEET (v89).

    python staff_art_lab.py --game ../02-chain/sc-leaf.html --spec ../06-docs/v89/staff_spec.js --out ../05-reference/v89

Injects `06-docs/v89/staff_spec.js` (Cowork's concepts: three heads a school,
A/B/C, one shared rod) over a throwaway page of the build and draws every
candidate with the engine's own `litWeapon`, on the engine's own frame, on a
ball of the school's palette — at zoom (the shape question) and at the size
it ships at on a 1080-wide phone (the scale question; v53's rule). Nothing
is written to any build. Rick picks one letter a school; Code pastes the
spec as `SHAPES.staff` with `STAFF.pick` set to his seven letters.

Prints, per candidate, the furthest point of the drawn head from the ball's
edge as a fraction of L (the reach rule: <= 1.02 L), read off the alpha
channel rather than judged.
"""
from __future__ import annotations
import argparse, base64, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--spec", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--zoom", type=float, default=4.5)
ap.add_argument("--ship", type=float, default=1080/620)
ap.add_argument("--rot", type=float, default=-0.35, help="facing, radians; the engine lights by world orientation, so a tilt shows the lit face and the dark underside the way play does")
a = ap.parse_args()

SCHOOLS = ["bloodsworn", "umbral", "vigil", "verdant", "runic", "sanctified", "dwarven"]
NAMES = {"bloodsworn":"BLOODWICK", "umbral":"NIGHTGLASS", "vigil":"WATCHLIGHT", "verdant":"BRIARWAND",
         "runic":"CIPHER", "sanctified":"CROZIER", "dwarven":"CULVERIN"}
SPEC = pathlib.Path(a.spec).read_text()

INJECT = r"""(src) => {
  const cv = document.createElement('canvas'); cv.id = '__staffcv'; document.body.appendChild(cv);
  window.__STAFF = eval('(() => { ' + src + '; return STAFF; })()');
  SHAPES.staff = window.__STAFF.staff;
  return Object.keys(window.__STAFF.pick).length;
}"""

DRAW = r"""(cfg) => {
  const ST = window.__STAFF; ST.pick[cfg.key] = cfg.v;
  const cv = document.getElementById('__staffcv'), c = cv.getContext('2d');
  const L = 60, W = 44, R = CONFIG.physics.ballR, z = cfg.zoom;
  const butt = 4;
  cv.width = Math.ceil((butt + R*2 + L*2.2) * z) + 24; cv.height = Math.ceil((W*2.4 + L*1.2*Math.abs(Math.sin(cfg.rot)))*z) + 24;
  c.setTransform(1,0,0,1,0,0); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  c.fillStyle = cfg.bg; c.fillRect(0, 0, cv.width, cv.height);
  const p = Object.assign({}, AFFINITIES[cfg.key]);
  const ox = 12 + (butt + R)*z, oy = cv.height/2;
  // the weapon FIRST, exactly as drawWeapon places it (at the ball's edge, along the facing) -- drawFighter draws the shell over it
  c.save(); c.translate(ox, oy); c.scale(z, z); c.rotate(cfg.rot); c.translate(R - 6, 0);
  if (!litWeapon(c, 'staff', L, W, p, 0.5, cfg.rot)) SHAPES.staff(c, L, W, p, 0.5);
  c.restore();
  // then the ball: the school's dark with a lit rim, the way the shell reads in the arena
  c.save(); c.translate(ox, oy); c.scale(z, z);
  const g = c.createRadialGradient(-R*0.3, -R*0.3, R*0.1, 0, 0, R);
  g.addColorStop(0, SHAPES._shade(p.dark, 1.9, 0.2)); g.addColorStop(1, SHAPES._ink(p.dark, 6));
  c.fillStyle = g; c.beginPath(); c.arc(0, 0, R, 0, Math.PI*2); c.fill();
  c.strokeStyle = p.core + '99'; c.lineWidth = 1.6; c.beginPath(); c.arc(0, 0, R - 1, 0, Math.PI*2); c.stroke();
  c.restore();
  // reach: the furthest opaque pixel right of the ball's edge, in L
  const id = c.getImageData(0, 0, cv.width, cv.height).data; let maxx = 0;
  const edge = ox + R*z;
  for (let y = 0; y < cv.height; y++) for (let x = Math.floor(edge); x < cv.width; x++){
    const i = (y*cv.width + x)*4; if (Math.abs(id[i]-cfg.bgc[0]) + Math.abs(id[i+1]-cfg.bgc[1]) + Math.abs(id[i+2]-cfg.bgc[2]) > 24) if (x > maxx) maxx = x; }
  const reach = (maxx - (ox + (R - 6)*z)) / (L*z*Math.cos(cfg.rot));   // in SIM reaches (L = 60), not in the art's own 1.7 L
  return { png: cv.toDataURL('image/png').slice(22), reach };
}"""

out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
BG = "#0B0B12"; BGC = [11, 11, 18]
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    n = page.evaluate(INJECT, SPEC)
    print(f"spec injected: {n} schools")
    cells = {}
    for key in SCHOOLS:
        for v in "ABC":
            big = page.evaluate(DRAW, {"key": key, "v": v, "zoom": a.zoom, "bg": BG, "bgc": BGC, "rot": a.rot})
            small = page.evaluate(DRAW, {"key": key, "v": v, "zoom": a.ship, "bg": BG, "bgc": BGC, "rot": a.rot})
            cells[(key, v)] = (big, small)
            print(f"  {key:<11} {v}  reach {big['reach']:.2f} L")
    assert not errors, errors

def img(b64):
    import io; return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGBA")

try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22); fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except Exception: font = ImageFont.load_default(); fs = font

# one sheet for the row (7 x 3) and one per school (1 x 3), each cell: big + ship-size inset
b0 = img(cells[("bloodsworn", "A")][0]["png"]); cw, ch = b0.width + 20, b0.height + 70
def sheet(keys, path, title):
    S = Image.new("RGBA", (cw*3 + 40, ch*len(keys) + 80), (11, 11, 18, 255)); d = ImageDraw.Draw(S)
    d.text((20, 18), title, fill=(230, 230, 240), font=font)
    for r, key in enumerate(keys):
        for cidx, v in enumerate("ABC"):
            big, small = cells[(key, v)]; bi, si = img(big["png"]), img(small["png"])
            x, y = 20 + cidx*cw, 70 + r*ch
            S.paste(bi, (x, y + 40)); S.paste(si, (x + bi.width - si.width - 4, y + 40 + bi.height - si.height - 4))
            d.text((x, y + 8), f"{NAMES[key]}  {v}", fill=(235, 235, 245), font=font)
            d.text((x + 230, y + 12), f"{key} · reach {big['reach']:.2f} L · inset = ship size", fill=(150, 150, 165), font=fs)
    S.save(path); print("wrote", path, S.size)
sheet(SCHOOLS, out / "staff-sheet.png", "THE STAFF ROW — concepts A/B/C a school (v89). Rick picks one letter a school. Inset: the size it ships at.")
for key in SCHOOLS: sheet([key], out / f"staff-{key}.png", f"{NAMES[key]} — the {key} staff, three heads on one rod")
