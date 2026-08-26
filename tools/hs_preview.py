"""Scrunch + health, single build, full frame. Three segments: the opening beat,
a mid-fight stretch where the health readouts are the only thing doing work, and
the verdict."""
import base64, io, pathlib, subprocess, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright
G = pathlib.Path("/home/claude/sc/sc/02-chain/sc-healthscrunch.html").resolve()
A,B,SEED,FPS = "ironhail","oathwound",1676955306,24
SETUP="""([a,b,seed])=>{window.__frozen=true;AC.setResolution(540,960);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,seed>>>0);m.introT=0;AC.__inject(m);window.__m=m;return 1;}"""
TICK="""([n])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 for(let i=0;i<n;i++) m.step(dt); AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.86).slice(23);}"""
SKIP="""([sec])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 let g=0; while(m.t<sec && !m.over && g++<200000) m.step(dt); return +m.t.toFixed(2);}"""
KILL="""()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 let g=0; while(!m.over && g++<200000) m.step(dt); return +m.t.toFixed(2);}"""
with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(G.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    dt=pg.evaluate("AC.CONFIG.physics.dt"); n=max(1,int(round((1.0/FPS)/dt)))
    frames=[]
    print("  opening beat ..."); pg.evaluate(SETUP,[A,B,SEED])
    for _ in range(int(9.0*FPS)): frames.append(pg.evaluate(TICK,[n]))
    print("  mid-fight ...");     pg.evaluate(SKIP,[19.0])
    for _ in range(int(5.0*FPS)): frames.append(pg.evaluate(TICK,[n]))
    print("  verdict ...");       pg.evaluate(KILL)
    for _ in range(int(6.0*FPS)): frames.append(pg.evaluate(TICK,[n]))
    br.close()
tmp=pathlib.Path(tempfile.mkdtemp())
for i,b64 in enumerate(frames):
    Image.open(io.BytesIO(base64.b64decode(b64))).save(tmp/f"f{i:05d}.jpg", quality=90)
out="/home/claude/tt/scrunch-plus-health.mp4"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),
 "-i",str(tmp/"f%05d.jpg"),"-c:v","libx264","-preset","veryfast","-crf","20",
 "-pix_fmt","yuv420p","-movflags","+faststart",out],check=True)
print(f"  wrote {out}  {pathlib.Path(out).stat().st_size/1024/1024:.2f} MB  ({len(frames)} frames)")
