#!/usr/bin/env python3
"""LOOK AT A DRAIN. Six consecutive frames spanning one heal, cropped to hold
BOTH balls — the whole content of the effect is travel between two things, and
a crop centred on either one cannot show it."""
import base64, io, pathlib, sys
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foe, seed, n]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const cv = document.getElementById('cv');
  /* run to a real heal inside a real ultimate, not a forced one */
  let g = 0;
  while (g++ < DT_FPS * 200 && !m.over){
    m.step(DT);
    if (me.ultSplit && m.drains.length >= 10 && (th.drained || 0) > 0.5){
      /* let the burst DEVELOP: strands leave over 1.1s, so the first
         frame after the heal has almost nothing in flight */
      for (let k = 0; k < 34; k++) m.step(DT);
      break;
    }
  }
  if (!m.drains.length) return { error: "no drain found" };
  const out = [];
  for (let f = 0; f < n; f++){
    AC.__draw(m);
    const R = AC.renderer;
    const P = (x, y) => [Math.round((R.pad + x * R.scale) * R.k),
                         Math.round((R.arenaTop + y * R.scale) * R.k)];
    const pts = [P(me.x, me.y), P(th.x, th.y)];
    for (const s of m.shades) pts.push(P(s.x, s.y));
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    const pad = 150;
    let x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad;
    let y0 = Math.min(...ys) - pad, y1 = Math.max(...ys) + pad;
    const w = Math.max(x1 - x0, y1 - y0);
    x0 = Math.max(0, Math.min(cv.width - w, x0));
    y0 = Math.max(0, Math.min(cv.height - w, y0));
    const tmp = document.createElement('canvas');
    tmp.width = w; tmp.height = w;
    tmp.getContext('2d').drawImage(cv, x0, y0, w, w, 0, 0, w, w);
    out.push({ png: tmp.toDataURL('image/png'), motes: m.drains.length,
               drained: +(th.drained || 0).toFixed(2), hp: Math.round(me.hp) });
    for (let i = 0; i < 3; i++) m.step(DT);
  }
  return { frames: out };
}"""

with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    r = p.evaluate(JS, ["twinshade", "lightkeeper", 113967, 6])
    if e: print("PAGE ERRORS:", e[:3])
if r.get("error"): sys.exit(r["error"])
ims = [Image.open(io.BytesIO(base64.b64decode(f["png"].split(",",1)[1]))).convert("RGB")
       for f in r["frames"]]
S = 470
sheet = Image.new("RGB", (14 + 3*(S+14), 40 + 2*(S+40)), (11, 9, 16))
dr = ImageDraw.Draw(sheet)
dr.text((14, 8), "ONE DRAIN — six consecutive sim frames, 3 apart, cropped to hold every ball",
        fill=(201,162,39))
for i, (im, f) in enumerate(zip(ims, r["frames"])):
    x = 14 + (i % 3) * (S + 14); y = 40 + (i // 3) * (S + 40)
    sheet.paste(im.resize((S, S), Image.LANCZOS), (x, y + 18))
    dr.text((x, y + 2), f"motes {f['motes']}   drained {f['drained']}   hp {f['hp']}",
            fill=(214,200,170))
out = (HERE / "../05-reference/v37/drain.png").resolve()
sheet.save(out); print(f"{out.name}  {sheet.width}x{sheet.height}")
