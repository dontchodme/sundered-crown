"""Card vs plate, side by side, as video. Nothing here is proven until it is
watched -- every number in the probe is a measurement, and this is the judgement."""
import base64, io, pathlib, subprocess, sys, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright

CARD  = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PLATE = pathlib.Path("/home/claude/sc/sc/02-chain/sc-nameplate.html").resolve()
A, B, SEED, SECS, FPS = "ironhail", "oathwound", 1676955306, 10.0, 24

SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(540,960);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 window.__m=new AC.Match(a,b,seed>>>0);window.__m.introT=0;
 AC.__inject&&AC.__inject(window.__m);return 1;}"""
STEP="([n])=>{const dt=AC.CONFIG.physics.dt;for(let i=0;i<n;i++)window.__m.step(dt);return window.__m.t;}"
DRAW="()=>{AC.__draw(window.__m);return document.getElementById('cv').toDataURL('image/jpeg',0.85).slice(23);}"
CLANK="""([a,b,seed])=>{const dt=AC.CONFIG.physics.dt;const m=new AC.Match(a,b,seed>>>0);m.introT=0;
 for(let k=0;k<Math.round(20/dt)&&!m.over;k++){const c0=m.clankCount;m.step(dt);if(m.clankCount>c0)return m.t;}return 2.0;}"""

def run(page, mode, cut, dt):
    page.evaluate(SETUP,[A,B,SEED])
    n = max(1, int(round((1.0/FPS)/dt)))
    frames, raised, v = [], False, 0.0
    for i in range(int(SECS*FPS)):
        if not raised and v >= cut:
            page.evaluate("()=>{window.__m.introT=AC.CONFIG.intro.dur;}" if mode=="card"
                          else "()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
            raised = True
        frames.append(page.evaluate(DRAW))
        page.evaluate(STEP,[n]); v += n*dt
    return frames

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    pc,pp=br.new_page(),br.new_page()
    pc.goto(CARD.as_uri());  pc.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    pp.goto(PLATE.as_uri()); pp.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    dt=pp.evaluate("AC.CONFIG.physics.dt"); cut=pp.evaluate(CLANK,[A,B,SEED])
    print(f"  first clank {cut:.2f}s; rendering {SECS:.0f}s x {FPS}fps x 2 builds")
    fc=run(pc,"card",cut,dt); fp=run(pp,"plate",cut,dt)
    br.close()

tmp=pathlib.Path(tempfile.mkdtemp())
for i,(a_,b_) in enumerate(zip(fc,fp)):
    ia=Image.open(io.BytesIO(base64.b64decode(a_)))
    ib=Image.open(io.BytesIO(base64.b64decode(b_)))
    sh=Image.new("RGB",(1096,960),(10,10,12)); sh.paste(ia,(0,0)); sh.paste(ib,(556,0))
    sh.save(tmp/f"f{i:05d}.jpg", quality=88)
out="/home/claude/tt/card-vs-plate.mp4"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),
  "-i",str(tmp/"f%05d.jpg"),
  "-vf","drawtext=text='CARD — fight frozen 4.0s':x=14:y=922:fontsize=20:fontcolor=0xE2DCCD:box=1:boxcolor=0x000000AA:boxborderw=6,"
        "drawtext=text='PLATE — fight never stops':x=570:y=922:fontsize=20:fontcolor=0xE2DCCD:box=1:boxcolor=0x000000AA:boxborderw=6",
  "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
  "-movflags","+faststart",out],check=True)
print(f"  wrote {out}  {pathlib.Path(out).stat().st_size/1024/1024:.2f} MB")
