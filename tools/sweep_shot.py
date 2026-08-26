"""How far can the art actually turn? Measure the ink, do not model it.

The geometry argument was already wrong once (the 250x148 band is a layout hint,
not a clip, and v3 crosses it), so headroom is measured from the rendered frame:
the ink bounding box of the header art, against the two things it must not hit --
the card's right border and the rule that closes the header. Sampled at the
extremes of each variant's motion, over the longest and the fastest relics.
"""
import base64, io, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

VARIANTS=[("CONTROL-v3",0,0,0),("TC60",0,0,0),("TC85",0,0,0)]
RELICS=[("axiom","nightfell"),("widowmaker","spellbreaker"),("grudgebearer","thornwake")]
PHASES=[round(0.02+i*0.16,2) for i in range(22)]   # dense: catch the worst angle, not a sample of it
# card A rests at y=118, header rule at +176, card spans x 40..1040
ART_REGION=(620,118,1040,118+176)      # right half of card A's header
LIMIT_R, LIMIT_B = 1040-4, 118+176-4

SHOT="""([a,b,e])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,4242);AC.__inject(m);
 m.introT=Math.max(0.0001,AC.CONFIG.intro.dur-e);AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23);}"""

def ink_bbox(png, thresh=110):
    im=Image.open(io.BytesIO(base64.b64decode(png))).convert("L")
    x0,y0,x1,y1=ART_REGION
    crop=im.crop(ART_REGION); px=crop.load(); w,h=crop.size
    R=B=None
    for x in range(w-1,-1,-1):
        if any(px[x,y]>thresh for y in range(h)): R=x0+x; break
    for y in range(h-1,-1,-1):
        if any(px[x,y]>thresh for x in range(0,w,2)): B=y0+y; break
    return R,B

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    print(f"  right border at {LIMIT_R}, header rule at {LIMIT_B}\n")
    print(f"  {'variant':<9}{'relic':<14}{'max right':>11}{'max bottom':>12}   verdict")
    for tag,sw,sy,sr in VARIANTS:
        f=pathlib.Path("/home/claude/sc/sc/02-chain/sc-ember.html" if tag.startswith("CONTROL")
                       else f"/home/claude/sc/sc/02-chain/sc-spin-{tag}.html").resolve()
        pg=br.new_page(); pg.goto(f.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
        for a,b in RELICS:
            mr=mb=0
            for e in PHASES:
                R,B=ink_bbox(pg.evaluate(SHOT,[a,b,e]))
                if R: mr=max(mr,R)
                if B: mb=max(mb,B)
            ok = mr<=LIMIT_R and mb<=LIMIT_B
            print(f"  {tag:<9}{a:<14}{mr:>11}{mb:>12}   {'ok' if ok else 'OVERRUNS'}")
        pg.close()
    br.close()
