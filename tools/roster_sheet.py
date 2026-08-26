#!/usr/bin/env python3
"""Every relic, at four HP values, at 1:1 and at eye-resolution.

Open decision 6 of the health v4 note: the gauge has only ever been judged on
Axiom, a mid-value blue. The worst-contrast case in the roster is a near-white
shell -- Dawnbringer, Aureole, Censer -- and the second worst is a shell whose
own affinity is already warm. This is the instrument for that question.

    python3 roster_sheet.py --src ../02-chain/sc-health.html --out roster.png
"""
from __future__ import annotations
import argparse, base64, math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
from scpage import game

JS = r"""
([ida, idb, hps, t]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const mm = new AC.Match(ida, idb, 20260817);
  mm.introT = 0; AC.__inject(mm);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  while (mm.t < t) mm.step(AC.CONFIG.physics.dt);
  mm.shake = 0; mm.hitStop = 0; mm.banner = null;
  const f = mm.a;
  f.status = {}; f.ringFlash = 0; f.mend = 0; f.stun = 0; f.flash = 0;
  f.x = 150; f.y = 250; f.vx = 0; f.vy = 0;
  mm.b.status = {}; mm.b.x = 380; mm.b.y = 600; mm.b.vx = 0; mm.b.vy = 0;
  const r = AC.renderer, cv = document.getElementById('cv');
  const S = 250, out = [];
  const tile = document.createElement('canvas'); tile.width = S; tile.height = S;
  const tx = tile.getContext('2d');
  for (const hp of hps){
    f.hp = hp; f.hpGhost = hp;
    AC.__draw(mm);
    const dx = r.pad + f.x * r.scale, dy = r.arenaTop + f.y * r.scale;
    tx.clearRect(0,0,S,S);
    tx.drawImage(cv, Math.round(dx - S/2), Math.round(dy - S/2), S, S, 0, 0, S, S);
    out.push(tile.toDataURL('image/png').slice(22));
  }
  return { tiles: out, name: f.w.name, aff: f.aff.name };
}
"""

def acuity(img, frame_w=1080, phone_mm=65.1, dist_mm=350.0):
    arc = math.degrees(2*math.atan((phone_mm/2)/dist_mm))*60
    k = arc/frame_w
    w,h = img.size
    return img.resize((max(1,round(w*k)), max(1,round(h*k))), Image.LANCZOS)\
              .resize((w,h), Image.LANCZOS)

ap = argparse.ArgumentParser()
ap.add_argument("--src", default="../02-chain/sc-health.html")
ap.add_argument("--out", default="roster.png")
ap.add_argument("--hp", default="300,230,160,88,26")
ap.add_argument("--t", type=float, default=6.0)
ap.add_argument("--acuity", action="store_true")
g = ap.parse_args()
HPS = [float(v) for v in g.hp.split(",")]

src = pathlib.Path(g.src).resolve()
ids = []
import re
for mm in re.finditer(r'\{ *id:"([a-z]+)"', src.read_text(encoding="utf-8")):
    if mm.group(1) not in ids: ids.append(mm.group(1))
print(f"{len(ids)} relics x {len(HPS)} values")

rows = []
with game(game_path=src) as (pg, errs):
    for i, rid in enumerate(ids):
        foe = ids[(i+1) % len(ids)]
        r = pg.evaluate(JS, [rid, foe, HPS, g.t])
        ims = []
        for k, b64 in enumerate(r["tiles"]):
            pathlib.Path("_r.png").write_bytes(base64.b64decode(b64))
            im = Image.open("_r.png").convert("RGB")
            ims.append(acuity(im) if g.acuity else im)
        rows.append((r["name"], r["aff"], ims))
        print(f"  {r['name']:<14} {r['aff']}")
    if errs:
        print("PAGE ERRORS:", *errs[:6], sep="\n  "); sys.exit(1)

F = lambda s,b=False: ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""), s)
S = 250
COLS = 3                       # relics per block, side by side
blocks = [rows[i:i+COLS] for i in range(0, len(rows), COLS)]
BW = len(HPS)*S + 190
W = BW*COLS
H = 44 + max(len(b) for b in blocks)*(S+34)
sheet = Image.new("RGB", (W, H), (8,6,12)); d = ImageDraw.Draw(sheet)
for bi, block in enumerate(blocks):
    ox = bi*BW
    for j,v in enumerate(HPS):
        d.text((ox+186+j*S+S//2, 22), f"{int(v)}", font=F(20,True), fill=(210,200,182), anchor="mm")
    for ri,(name,aff,ims) in enumerate(block):
        y = 44 + ri*(S+34)
        d.text((ox+10, y+S//2-10), name.upper(), font=F(21,True), fill=(236,227,208))
        d.text((ox+10, y+S//2+14), aff.upper(), font=F(15), fill=(130,122,146))
        for j,im in enumerate(ims):
            sheet.paste(im, (ox+186+j*S, y))
sheet.save(g.out)
print(g.out, sheet.size)
