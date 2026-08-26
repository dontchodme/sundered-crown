#!/usr/bin/env python3
"""Full frames of the band with both relics near their ultimate, which is the
only state that proves the two blocks do not collide."""
import base64, pathlib, sys
from PIL import Image
from scpage import game
JS = r"""
([ida, idb, ca, cb]) => {
  window.__frozen = true; AC.setResolution(1080, 1920);
  const mm = new AC.Match(ida, idb, 20260817); mm.introT = 0; AC.__inject(mm);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  while (mm.t < 6) mm.step(AC.CONFIG.physics.dt);
  mm.shake=0; mm.hitStop=0; mm.banner=null;
  mm.a.charge = mm.a.w.ult.charge * ca; mm.b.charge = mm.b.w.ult.charge * cb;
  AC.__draw(mm);
  return document.getElementById('cv').toDataURL('image/png').slice(22);
}
"""
CASES = [("dawnbringer","censer",0.97,0.93,"both-imminent-sanctified"),
         ("grudgebearer","gravemourn",0.78,0.98,"crucible-v-dirge"),
         ("ironhail","oathwound",0.99,0.35,"quarrelstorm-now")]
out=[]
with game(game_path=pathlib.Path("../02-chain/sc-health.html").resolve()) as (pg,errs):
    for a,b,ca,cb,tag in CASES:
        pathlib.Path("_f.png").write_bytes(base64.b64decode(pg.evaluate(JS,[a,b,ca,cb])))
        out.append((tag, Image.open("_f.png").convert("RGB").crop((0,0,1080,215))))
    if errs: print("PAGE ERRORS:",*errs[:5],sep="\n  "); sys.exit(1)
sheet=Image.new("RGB",(1080,len(out)*235),(8,6,12))
for i,(tag,im) in enumerate(out): sheet.paste(im,(0,i*235))
sheet.save("ult-band.png"); print("ult-band.png", sheet.size)
