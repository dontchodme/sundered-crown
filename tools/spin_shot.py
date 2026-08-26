"""Card-spin v4b: engine A/B, then film the card and check its edges by pixels.

The geometric argument is spent -- the band is not a clip and v3 already
crosses it. So the containment question is answered the way introfit_probe
answers it: bright ink within 6px of the FRAME edge, sampled across the card's
phases, on the widest and the longest relics.
"""
import base64, io, json, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

SRC=pathlib.Path("/home/claude/sc/sc/02-chain/sc-ember.html").resolve()
OUT=pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PAIRS=[("axiom","nightfell"),("grudgebearer","thornwake"),("widowmaker","spellbreaker")]
PHASES=[0.10,0.30,0.46,0.62,1.20,2.20,3.40]

SIM="([p,n,s0])=>{const o=[];for(const[a,b]of p)for(let i=0;i<n;i++)o.push(AC.simulate(a,b,(s0+i*7919)>>>0));return JSON.stringify(o);}"
SHOT="""([a,b,e])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,4242);AC.__inject(m);
 m.introT=Math.max(0.0001,AC.CONFIG.intro.dur-e);AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23);}"""

def edge_ink(png, margin=6, thresh=150):
    im=Image.open(io.BytesIO(base64.b64decode(png))).convert("L")
    w,h=im.size; px=im.load(); worst=0
    for y in range(h):
        for x in list(range(margin))+list(range(w-margin,w)):
            worst=max(worst,px[x,y])
    for x in range(0,w,2):
        for y in list(range(margin))+list(range(h-margin,h)):
            worst=max(worst,px[x,y])
    return worst

fails=0
def check(ok,n,d=""):
    global fails
    if not ok: fails+=1
    print(f"  {'PASS' if ok else 'FAIL'}  {n}"+(f"  -- {d}" if d else ""))

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); sims={}; shots={}
    for f in (SRC,OUT):
        pg=br.new_page(); pg.goto(f.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
        sims[f.name]=pg.evaluate(SIM,[PAIRS,60,20260816])
        if f is OUT:
            for a,b in PAIRS:
                for e in PHASES: shots[(a,b,e)]=pg.evaluate(SHOT,[a,b,e])
        pg.close()
    br.close()

check(sims[SRC.name]==sims[OUT.name],"[1] engine A/B — 180 matches identical field for field")
worst={}
for k,v in shots.items(): worst[k]=edge_ink(v)
bad=[k for k,v in worst.items() if v>150]
check(not bad,"[2] no bright ink within 6px of the frame edge, all phases",
      f"worst luma {max(worst.values())} (limit 150)"+(f"; {bad}" if bad else ""))

out=pathlib.Path("/home/claude/out"); out.mkdir(exist_ok=True)
for (a,b),name in zip(PAIRS,["axiom","grudge","widow"]):
    ims=[Image.open(io.BytesIO(base64.b64decode(shots[(a,b,e)]))).resize((216,384)) for e in PHASES]
    sheet=Image.new("RGB",(216*len(ims),384))
    for i,im in enumerate(ims): sheet.paste(im,(i*216,0))
    sheet.save(out/f"spin-{name}.png")
print(f"    phases {PHASES}")
print(f"\n  {'ALL PASS' if not fails else str(fails)+' FAILED'}")
sys.exit(1 if fails else 0)
