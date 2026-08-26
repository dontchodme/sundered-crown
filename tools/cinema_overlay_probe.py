"""A/B the director's overlay layers one at a time, on a frozen frame.

The only way to catch a layer that reads as nothing, or as a blown exposure.
Both failures were found here and neither was visible in motion.
"""
import base64, pathlib
from scpage import game
from PIL import Image
import io
JS = r"""
([a,b,seed,tt,state]) => {
  const m = new AC.Match(a,b,seed); m.introT=0;
  const dt=AC.CONFIG.physics.dt; let g=0;
  while(!m.over && m.t<tt && g++<200000) m.step(dt);
  window.__frozen=true; CINE.on=true;
  Object.assign(CINE, state);
  CINE.fx = m.b.x; CINE.fy = m.b.y;
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/jpeg',0.9).slice(23);
}"""
states=[
 ("baseline",      dict(zoom=1,    bars=0,   wash=0,   flash=0,   streak=0)),
 ("zoom 1.9 only", dict(zoom=1.9,  bars=0,   wash=0,   flash=0,   streak=0)),
 ("+ bars",        dict(zoom=1.9,  bars=1,   wash=0,   flash=0,   streak=0)),
 ("+ wash .75",    dict(zoom=1.9,  bars=1,   wash=0.75,flash=0,   streak=0)),
 ("+ flash .72",   dict(zoom=1.9,  bars=1,   wash=0.75,flash=0.72,streak=0)),
 ("+ streak",      dict(zoom=1.9,  bars=1,   wash=0.75,flash=0.3, streak=1)),
]
ims=[]
with game(game_path=pathlib.Path("sc-cinema.html").resolve()) as (page,err):
    page.evaluate("AC.setResolution(540,960)")
    for name,st in states:
        d=page.evaluate(JS,["gravemourn","dawnbringer",2901315739,20.0,st])
        ims.append((name, Image.open(io.BytesIO(base64.b64decode(d)))))
    print("errors",err[:3])
w,h=ims[0][1].size; sc=0.5; tw,th=int(w*sc),int(h*sc)
sheet=Image.new("RGB",(tw*len(ims),th+22),(10,8,16))
from PIL import ImageDraw
d=ImageDraw.Draw(sheet)
for k,(name,im) in enumerate(ims):
    sheet.paste(im.resize((tw,th)),(k*tw,22)); d.text((k*tw+6,6),name,fill=(230,220,190))
sheet.save("/home/claude/work/cine-overlay-ab.png"); print("ok")
