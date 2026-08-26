"""The scrunch build, looked at. Draw and grab in ONE evaluate -- the page's own
rAF loop will otherwise redraw a normal frame in the gap and the shot is a lie
that looks plausible (learned on scrunch_mock)."""
import base64, io, pathlib, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
G = pathlib.Path("/home/claude/sc/sc/02-chain/sc-scrunch.html").resolve()
A,B,SEED = "ironhail","oathwound",1676955306

SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,seed>>>0); m.introT=0;
 AC.__inject(m); window.__m=m; return {auto:m.scrunchAuto};}"""
# step to a WALL time, drawing nothing, then draw+grab atomically
RUN="""([sec])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 const n=Math.round(sec/dt);
 for(let i=0;i<n && !window.__stop;i++){ m.step(dt); }
 AC.__draw(m);
 return {img:document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23),
         t:+m.t.toFixed(2), mode:m.scrunchMode, sT:+(m.scrunchT||0).toFixed(2),
         over:m.over};}"""
TOEND="""()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 let g=0; while(!m.over && g++<40000) m.step(dt);
 for(let i=0;i<Math.round(2.2/dt);i++) m.step(dt);
 AC.__draw(m);
 return {img:document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23),
         t:+m.t.toFixed(2), mode:m.scrunchMode, hp:m.winner?Math.ceil(m.winner.hp):null,
         win:m.winner?m.winner.w.name:null};}"""

shots=[]
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(G.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    print("  setup:", pg.evaluate(SETUP,[A,B,SEED]))
    for lab, at in [("t=1.5s  before the clank",1.5),
                    ("t=2.2s  scrunching in",0.7),
                    ("t=3.2s  tape held",1.0),
                    ("t=5.0s  tape held, late",1.8),
                    ("t=5.9s  expanding back",0.9),
                    ("t=7.0s  back to full",1.1)]:
        r=pg.evaluate(RUN,[at]); shots.append((f"{lab}", r.pop("img"))); print("  ",lab,r)
    r=pg.evaluate(TOEND); shots.append(("the verdict, in the panel", r.pop("img"))); print("  end:",r)
    print("  page errors:", errs[:3])
    br.close()

sc=0.29; w,h=int(1080*sc),int(1920*sc); pad,top=14,28
sheet=Image.new("RGB",(pad+len(shots)*(w+pad), top+h+pad),(16,16,18)); d=ImageDraw.Draw(sheet)
for i,(lab,b64) in enumerate(shots):
    im=Image.open(io.BytesIO(base64.b64decode(b64))).resize((w,h))
    x=pad+i*(w+pad); sheet.paste(im,(x,top)); d.text((x+2,top-16),lab,fill=(222,216,202))
sheet.save("/home/claude/tt/scrunch-shot.png"); print("  wrote /home/claude/tt/scrunch-shot.png", sheet.size)
