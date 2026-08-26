"""Card vs scrunch, side by side, as video -- the opening beat and the verdict.

Two clips because the two beats are 30 seconds apart and the middle is the same
fight in both builds. Each build runs its OWN timeline: the card's is 4s longer
by construction, which is the point.
"""
import base64, io, pathlib, subprocess, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright

CARD    = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
SCRUNCH = pathlib.Path("/home/claude/sc/sc/02-chain/sc-scrunch.html").resolve()
A, B, SEED, FPS = "ironhail", "oathwound", 1676955306, 24
OPEN_S, END_S = 9.0, 6.0

SETUP = """([a,b,seed,auto])=>{window.__frozen=true;AC.setResolution(540,960);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,seed>>>0); m.introT=0;
 AC.__inject(m); m.scrunchAuto=!!auto; window.__m=m; window.__raised=false; return 1;}"""
# one video frame: advance, maybe raise the card, draw and grab -- all atomic
TICK = """([n,cut,isCard])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 if(isCard && !window.__raised && m.t>=cut){ m.introT=AC.CONFIG.intro.dur; window.__raised=true; }
 for(let i=0;i<n;i++) m.step(dt);
 AC.__draw(m);
 return document.getElementById('cv').toDataURL('image/jpeg',0.86).slice(23);}"""
RUNTO = """([sec])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 let g=0; while(m.t<sec && !m.over && g++<200000) m.step(dt); return +m.t.toFixed(2);}"""
TOKILL = """()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 let g=0; while(!m.over && g++<200000) m.step(dt); return +m.t.toFixed(2);}"""
CLANK = """([a,b,seed])=>{const dt=AC.CONFIG.physics.dt;const m=new AC.Match(a,b,seed>>>0);m.introT=0;
 for(let k=0;k<Math.round(20/dt)&&!m.over;k++){const c0=m.clankCount;m.step(dt);if(m.clankCount>c0)return m.t;}return 2;}"""

def frames(page, isCard, cut, dt, secs, skip_to_kill=False, lead=0.0):
    page.evaluate(SETUP, [A, B, SEED, not isCard])
    n = max(1, int(round((1.0/FPS)/dt)))
    if skip_to_kill:
        # Run to the kill without capturing, then film the verdict. __raised is
        # forced true afterwards: the capture loop arms the card on `m.t >= cut`
        # and by the kill m.t is 33s, so without this the CARD build raises its
        # INTRO card over its own verdict -- which made the baseline look far
        # worse than it is. A comparison that flatters the new thing is worthless.
        page.evaluate(TOKILL)
        page.evaluate("()=>{window.__raised = true;}")
    out = []
    for _ in range(int(secs*FPS)):
        out.append(page.evaluate(TICK, [n, cut, isCard]))
    return out

with sync_playwright() as p:
    br = p.chromium.launch(args=["--no-sandbox"])
    pc, ps = br.new_page(), br.new_page()
    pc.goto(CARD.as_uri());    pc.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    ps.goto(SCRUNCH.as_uri()); ps.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    dt = ps.evaluate("AC.CONFIG.physics.dt"); cut = ps.evaluate(CLANK, [A, B, SEED])
    print(f"  first clank {cut:.2f}s")
    print("  filming the opening beat ...")
    oc, os_ = frames(pc, True, cut, dt, OPEN_S), frames(ps, False, cut, dt, OPEN_S)
    print("  filming the verdict ...")
    ec = frames(pc, True, cut, dt, END_S, skip_to_kill=True)
    es = frames(ps, False, cut, dt, END_S, skip_to_kill=True)
    br.close()

tmp = pathlib.Path(tempfile.mkdtemp()); i = 0
for L, R in list(zip(oc, os_)) + list(zip(ec, es)):
    a_ = Image.open(io.BytesIO(base64.b64decode(L)))
    b_ = Image.open(io.BytesIO(base64.b64decode(R)))
    sh = Image.new("RGB", (1096, 960), (10,10,12)); sh.paste(a_, (0,0)); sh.paste(b_, (556,0))
    sh.save(tmp/f"f{i:05d}.jpg", quality=88); i += 1
out = "/home/claude/tt/card-vs-scrunch.mp4"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),
  "-i",str(tmp/"f%05d.jpg"),
  "-vf","drawtext=text='CARD — fight frozen 4.0s':x=14:y=922:fontsize=20:fontcolor=0xE2DCCD:box=1:boxcolor=0x000000AA:boxborderw=6,"
        "drawtext=text='SCRUNCH — hall makes room':x=570:y=922:fontsize=20:fontcolor=0xE2DCCD:box=1:boxcolor=0x000000AA:boxborderw=6",
  "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
  "-movflags","+faststart",out],check=True)
print(f"  wrote {out}  {pathlib.Path(out).stat().st_size/1024/1024:.2f} MB  ({i} frames)")
