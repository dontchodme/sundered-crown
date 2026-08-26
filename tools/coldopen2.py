"""Cold open, v2 -- [2] rebuilt after the first version failed for the wrong reason.

v1 compared whole card frames and set a floor of 3.0 by guesswork. Both were
wrong. The cards rest at y 118-678 and 1242-1802, so ~70% of the frame is card,
and the 80% scrim attenuates what is left: a live scene that moves 5.79 in the
bare frame shows up as 0.35 globally. The floor rejected a true hypothesis.

v2 fixes both ends. It measures only the rows the cards do NOT cover, and it
carries a CONTROL: the same comparison with the scene genuinely held at t=0,
which must read ~0. A discriminator with no negative case discriminates nothing.
"""
import base64, io, json, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("/home/claude/sc/sc/02-chain/sc-ember.html").resolve()
A,B,SEED,CUT = "grudgebearer","thornwake",1039818459,6.0
BANDS = [(0,112),(684,1236),(1808,1920)]   # rows the resting cards leave clear

SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 window.__m=new AC.Match(a,b,seed>>>0);window.__m.introT=0;AC.__inject(window.__m);
 AC.__draw(window.__m);return 1;}"""
STEP="([n])=>{for(let i=0;i<n;i++)window.__m.step(AC.CONFIG.physics.dt);AC.__draw(window.__m);return window.__m.t;}"
GRAB="()=>document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23)"

def band_diff(p1,p2):
    a=Image.open(io.BytesIO(base64.b64decode(p1))).convert("L")
    b=Image.open(io.BytesIO(base64.b64decode(p2))).convert("L")
    tot=n=0
    for y0,y1 in BANDS:
        ca=a.crop((0,y0,1080,y1)).tobytes(); cb=b.crop((0,y0,1080,y1)).tobytes()
        for i in range(0,len(ca),5): tot+=abs(ca[i]-cb[i]); n+=1
    return tot/n

fails=0
def check(ok,name,detail=""):
    global fails
    if not ok: fails+=1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}"+(f"  -- {detail}" if detail else ""))

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(GAME.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    dt=pg.evaluate("AC.CONFIG.physics.dt")
    control=json.loads(pg.evaluate("([a,b,s])=>JSON.stringify(AC.simulate(a,b,s>>>0))",[A,B,SEED]))

    def carded(at):
        pg.evaluate(SETUP,[A,B,SEED])
        if at: pg.evaluate(STEP,[int(round(at/dt))])
        bare=pg.evaluate(GRAB)
        pg.evaluate("()=>{window.__m.introT=AC.CONFIG.intro.dur;}")
        pg.evaluate(STEP,[int(round(1.8/dt))])
        return bare, pg.evaluate(GRAB)

    bare0,card0 = carded(0.0)
    bare0b,card0b = carded(0.0)          # the CONTROL: same state, twice
    bareC,cardC = carded(CUT)

    # finish the interrupted fight from the cut point
    guard=0
    while not pg.evaluate("()=>window.__m.over") and guard<20000:
        pg.evaluate(STEP,[30]); guard+=30
    late=json.loads(pg.evaluate("()=>JSON.stringify(window.__m.summary())"))
    after=pg.evaluate(GRAB)

    print(f"\n  seed {SEED}  {A} v {B}   card raised at t={CUT}s   (bands: {BANDS})\n")
    check(control==late,"[1] the sim is untouched by a late card",
          f"{control['winner']} {control['hp']}hp {control['duration']}s both ways")
    null = band_diff(card0,card0b)
    live = band_diff(card0,cardC)
    check(null<0.20,"[2a] CONTROL -- a card over a genuinely frozen t=0 scene reads ~0",
          f"mean |diff| {null:.3f}")
    check(live>2.0,"[2b] the scene behind a LATE card is the live fight",
          f"mean |diff| {live:.3f} vs control {null:.3f}, bare-frame reference 5.79")
    check(band_diff(bareC,bare0)>2.0,"[2c] the bands themselves carry signal",
          f"bare t=0 vs t={CUT}: {band_diff(bareC,bare0):.3f}")
    br.close()
print(f"\n  {'ALL PASS' if not fails else str(fails)+' FAILED'}")
sys.exit(1 if fails else 0)
