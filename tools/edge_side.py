"""Which edge? The entrance legitimately crosses top and bottom; the ART would
show up on the SIDES. introfit_probe excludes entrance/exit phases for this
reason and spin_shot.py did not, so resolve the 158 by side before believing it."""
import base64,io
from PIL import Image
from playwright.sync_api import sync_playwright
import pathlib
OUT=pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
SHOT="""([a,b,e])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,4242);AC.__inject(m);
 m.introT=Math.max(0.0001,AC.CONFIG.intro.dur-e);AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23);}"""
def sides(png,margin=6):
    im=Image.open(io.BytesIO(base64.b64decode(png))).convert("L"); w,h=im.size; px=im.load()
    L=max(px[x,y] for y in range(h) for x in range(margin))
    R=max(px[x,y] for y in range(h) for x in range(w-margin,w))
    T=max(px[x,y] for x in range(0,w,2) for y in range(margin))
    B=max(px[x,y] for x in range(0,w,2) for y in range(h-margin,h))
    return L,R,T,B
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(OUT.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    print(f"  {'phase':>6}  {'left':>5}{'right':>6}{'top':>6}{'bottom':>7}   (limit 150)")
    for e in (0.10,0.30,0.46,0.62,1.20,2.20,3.40):
        L,R,T,B=sides(pg.evaluate(SHOT,["grudgebearer","thornwake",e]))
        flag="  <- cards in flight" if e<0.62 else ""
        print(f"  {e:>6.2f}  {L:>5}{R:>6}{T:>6}{B:>7}{flag}")
    br.close()
