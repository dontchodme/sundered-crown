"""Scrunch alone vs scrunch + the health rework, same fight, same moments."""
import base64, io, pathlib, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
BUILDS = [("SCRUNCH only", "/home/claude/sc/sc/02-chain/sc-scrunch.html"),
          ("SCRUNCH + HEALTH", "/home/claude/sc/sc/02-chain/sc-healthscrunch.html")]
A,B,SEED = "ironhail","oathwound",1676955306
MARKS = [("1.5s  before",1.5),("3.2s  panel held",1.7),("5.0s  panel, late",1.8),
         ("7.0s  back to full",2.0),("18s  mid-fight",11.0)]
SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,seed>>>0);m.introT=0;AC.__inject(m);window.__m=m;return 1;}"""
RUN="""([sec])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 for(let i=0;i<Math.round(sec/dt);i++) m.step(dt); AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23);}"""
END="""()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;let g=0;
 while(!m.over&&g++<40000)m.step(dt); for(let i=0;i<Math.round(2.2/dt);i++)m.step(dt);
 AC.__draw(m); return document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23);}"""
rows=[]
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    for label, path in BUILDS:
        pg=br.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(pathlib.Path(path).resolve().as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
        pg.evaluate(SETUP,[A,B,SEED])
        shots=[(n, pg.evaluate(RUN,[d])) for n,d in MARKS]
        pg.evaluate(SETUP,[A,B,SEED]); shots.append(("the verdict", pg.evaluate(END)))
        rows.append((label, shots)); print(f"  {label}: {len(shots)} frames, errors {errs[:1]}")
        pg.close()
    br.close()
sc=0.235; w,h=int(1080*sc),int(1920*sc); pad,top,lead=12,26,152
sheet=Image.new("RGB",(lead+len(rows[0][1])*(w+pad), top+2*(h+top)+8),(16,16,18))
d=ImageDraw.Draw(sheet)
for r,(label,shots) in enumerate(rows):
    y=top+r*(h+top); d.text((8,y+h//2-6), label, fill=(230,224,210))
    for i,(n,b64) in enumerate(shots):
        im=Image.open(io.BytesIO(base64.b64decode(b64))).resize((w,h))
        x=lead+i*(w+pad); sheet.paste(im,(x,y))
        if r==0: d.text((x+2,y-15), n, fill=(170,166,156))
sheet.save("/home/claude/tt/health-scrunch.png"); print("  wrote /home/claude/tt/health-scrunch.png", sheet.size)
