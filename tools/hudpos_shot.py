#!/usr/bin/env python3
"""The band at the top and at the bottom, same fight, same frame, one artifact.
HUDPOS is a live flag, so this flips it between draws rather than rebuilding."""
import base64, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
from scpage import game
JS = r"""
([a, b, seed, ca, cb, hpa, hpb, pos]) => {
  window.__frozen = true; AC.setResolution(1080, 1920);
  BAND.pos = pos;
  const mm = new AC.Match(a, b, seed); mm.introT = 0; AC.__inject(mm);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  while (mm.t < 24) mm.step(AC.CONFIG.physics.dt);
  mm.shake=0; mm.hitStop=0; mm.banner=null;
  
  mm.a.charge = mm.a.w.ult.charge*ca; mm.b.charge = mm.b.w.ult.charge*cb;
  mm.a.hp = hpa; mm.a.hpGhost = hpa; mm.b.hp = hpb; mm.b.hpGhost = hpb;
  AC.__draw(mm);
  return document.getElementById('cv').toDataURL('image/png').slice(22);
}
"""
CASE = ("ironhail","oathwound",1676955306,0.97,0.55,168.0,96.0)
ims = {}
with game(game_path=pathlib.Path("../02-chain/sc-health.html").resolve()) as (pg,errs):
    for pos in ("top","bottom"):
        pathlib.Path("_h.png").write_bytes(base64.b64decode(pg.evaluate(JS, list(CASE)+[pos])))
        ims[pos] = Image.open("_h.png").convert("RGB")
    if errs: print("PAGE ERRORS:",*errs[:5],sep="\n  "); sys.exit(1)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
o = Image.new("RGB",(1080*2+30,1920+56),(8,6,12)); d = ImageDraw.Draw(o)
for i,pos in enumerate(("top","bottom")):
    o.paste(ims[pos],(i*(1080+30),56)); d.text((i*(1080+30)+8,12), "HUDPOS = "+pos.upper(), font=F, fill=(236,226,206))
o.resize((o.width//2,o.height//2),Image.LANCZOS).save("hudpos.png")
print("hudpos.png", o.size)
