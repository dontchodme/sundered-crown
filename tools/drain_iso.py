#!/usr/bin/env python3
"""ONE DRAIN, ISOLATED. No fight, no flames, no damage numbers.

Judging a new effect inside a frame that already has three balls, a set of
flames and four floating numbers in it is judging a composite. This places two
balls on a quiet stage, calls `drain()` once, and photographs the presentation
clock advancing. What is on this sheet is the effect and nothing else.
"""
import base64, io, pathlib, sys
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foe, amount, times]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, 4242);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const A = AC.CONFIG.arena;
  /* a quiet stage: two balls, well apart, nothing else running */
  me.x = A.w * 0.28; me.y = A.h * 0.34; me.vx = 0; me.vy = 0;
  th.x = A.w * 0.74; th.y = A.h * 0.62; th.vx = 0; th.vy = 0;
  me.lifesteal = 0.35;
  m.drain(th, me, amount, false);
  const out = [];
  let t = 0, next = 0;
  const cv = document.getElementById('cv');
  for (let f = 0; f < 400 && next < times.length; f++){
    if (t >= times[next]){
      AC.__draw(m);
      out.push({ t: +t.toFixed(2), n: m.drains.length,
                 png: cv.toDataURL('image/png') });
      next++;
    }
    m.tickPresentation(DT);
    t += DT;
  }
  return { frames: out };
}"""

with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    r = p.evaluate(JS, ["twinshade", "lightkeeper", 12,
                        [0.10, 0.30, 0.55, 0.80, 1.10, 1.45]])
    if e: print("PAGE ERRORS:", e[:3])
ims = [Image.open(io.BytesIO(base64.b64decode(f["png"].split(",",1)[1]))).convert("RGB")
       for f in r["frames"]]
# crop to the band the two balls live in
box = (60, 380, 1020, 1340)
S = 460
sheet = Image.new("RGB", (14 + 3*(S+14), 40 + 2*(int(S*(box[3]-box[1])/(box[2]-box[0]))+40)),
                  (11, 9, 16))
dr = ImageDraw.Draw(sheet)
dr.text((14, 8), "ONE DRAIN, ISOLATED — quiet stage, drain(12hp) called once",
        fill=(201,162,39))
h = int(S*(box[3]-box[1])/(box[2]-box[0]))
for i, (im, f) in enumerate(zip(ims, r["frames"])):
    x = 14 + (i % 3) * (S + 14); y = 40 + (i // 3) * (h + 40)
    sheet.paste(im.crop(box).resize((S, h), Image.LANCZOS), (x, y + 18))
    dr.text((x, y + 2), f"t {f['t']}s   strands alive {f['n']}", fill=(214,200,170))
out = (HERE / "../05-reference/v37/drain-iso.png").resolve()
sheet.save(out); print(f"{out.name}  {sheet.width}x{sheet.height}")
