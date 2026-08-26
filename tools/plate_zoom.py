"""The plate at 1:1, through its whole life. Legibility is judged at the size
it ships at, not on a contact sheet."""
import base64, io, pathlib
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
G = pathlib.Path("/home/claude/sc/sc/02-chain/sc-nameplate.html").resolve()
SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 window.__m=new AC.Match(a,b,seed>>>0);window.__m.introT=0;
 AC.__inject&&AC.__inject(window.__m);return 1;}"""
STEP="([n])=>{const dt=AC.CONFIG.physics.dt;for(let i=0;i<n;i++)window.__m.step(dt);return window.__m.t;}"
DRAW="()=>{AC.__draw(window.__m);return document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23);}"
MARKS=[0.10,0.30,0.60,1.50,2.40,2.75,2.95]
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(G.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    dt=pg.evaluate("AC.CONFIG.physics.dt")
    pg.evaluate(SETUP,["ironhail","oathwound",1676955306])
    pg.evaluate(STEP,[int(round(2.03/dt))])
    pg.evaluate("()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
    ims=[]; last=0.0
    for mk in MARKS:
        n=int(round((mk-last)/dt)); last=mk
        if n>0: pg.evaluate(STEP,[n])
        ims.append((mk, Image.open(io.BytesIO(base64.b64decode(pg.evaluate(DRAW))))))
    br.close()
CROP=(0,0,1080,300)   # the whole plate, 1:1
w=CROP[2]-CROP[0]; h=CROP[3]-CROP[1]
sh=Image.new("RGB",(w+24,(h+30)*len(ims)+12),(16,16,18)); d=ImageDraw.Draw(sh)
for i,(mk,im) in enumerate(ims):
    y=12+i*(h+30)
    sh.paste(im.crop(CROP),(12,y))
    d.text((14,y-14),f"plate elapsed {mk:.2f}s of 3.00  (rise 0.28 · fall from 2.58)",fill=(200,196,184))
sh.save("/home/claude/tt/plate-zoom.png"); print("wrote /home/claude/tt/plate-zoom.png", sh.size)
