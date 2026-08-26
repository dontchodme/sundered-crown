"""When does the first impact land in the SHIPPED cold opens, and what is on
screen before it?

v28 records the seed of every week-1 short, so this is not a simulation of
something like the videos -- it is the videos. Axiom v Nightfell predates the
v28 slate and its seed is not recorded, so it is absent rather than guessed.
"""
import base64, json, pathlib, sys
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
SHIPPED = [   # short, a, b, seed, measured r(1), r(2) from TikTok
    ("short-10", "ironhail",    "oathwound", 1676955306, 0.85, 0.68),
    ("short-09", "emberedge",   "thornwake", 1270498896, 0.80, 0.65),
    ("short-08", "dawnbringer", "censer",    2503973695, 0.81, 0.65),
    ("short-11", "gravemourn",  "heartwood",  939176749, None, None),  # posted today
    ("short-12", "widowmaker",  "aureole",   3435875439, None, None),  # not yet posted
]

JS = """([a,b,seed])=>{
  window.__frozen=true; AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const dt=AC.CONFIG.physics.dt;
  const m=new AC.Match(a,b,seed>>>0); m.introT=0;
  let clank=null, hit=null, sep0=null;
  const dist=()=>Math.hypot(m.a.x-m.b.x, m.a.y-m.b.y);
  sep0=dist();
  const seps=[];
  for(let k=0;k<Math.round(20/dt) && !m.over;k++){
    const c0=m.clankCount, ha=m.a.hp, hb=m.b.hp;
    m.step(dt);
    if(Math.abs(m.t-Math.round(m.t))<dt/2 && m.t<6) seps.push([+m.t.toFixed(1), +dist().toFixed(0)]);
    if(clank===null && m.clankCount>c0) clank=m.t;
    if(hit===null && (m.a.hp<ha || m.b.hp<hb)) hit=m.t;
    if(clank!==null && hit!==null && m.t>5) break;
  }
  return JSON.stringify({clank, hit, sep0:+sep0.toFixed(0), seps});
}"""

GRAB = """([a,b,seed,at])=>{
  window.__frozen=true; AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  AC.setResolution(540,960);
  const dt=AC.CONFIG.physics.dt;
  const m=new AC.Match(a,b,seed>>>0); m.introT=0; AC.__inject&&AC.__inject(m);
  for(let k=0;k<Math.round(at/dt);k++) m.step(dt);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/jpeg',0.9).slice(23);
}"""

out = pathlib.Path("/home/claude/tt/frames"); out.mkdir(parents=True, exist_ok=True)
rows = []
with sync_playwright() as p:
    br = p.chromium.launch(args=["--no-sandbox"]); pg = br.new_page()
    pg.goto(GAME.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    for tag, a, b, seed, r1, r2 in SHIPPED:
        r = json.loads(pg.evaluate(JS, [a, b, seed]))
        rows.append((tag, a, b, r, r1, r2))
        for at in (0.0, 1.0, 2.0):
            img = pg.evaluate(GRAB, [a, b, seed, at])
            (out / f"{tag}_{at:.0f}s.jpg").write_bytes(base64.b64decode(img))
    br.close()

print("WHEN DOES ANYTHING HAPPEN IN THE SHIPPED VIDEOS?\n")
print(f"  {'short':9s} {'fight':26s} {'1st clank':>10s} {'1st hit':>9s} | {'r(1)':>6s} {'r(2)':>6s}")
for tag,a,b,r,r1,r2 in rows:
    c = f"{r['clank']:.2f}s" if r['clank'] is not None else "  none"
    h = f"{r['hit']:.2f}s"   if r['hit']   is not None else "  none"
    print(f"  {tag:9s} {a+' v '+b:26s} {c:>10s} {h:>9s} | "
          f"{(f'{r1:.2f}' if r1 else '   --'):>6s} {(f'{r2:.2f}' if r2 else '   --'):>6s}")

print("\nSEPARATION between the two relics, second by second (sim units):")
for tag,a,b,r,r1,r2 in rows:
    print(f"  {tag:9s} " + "  ".join(f"{t:.0f}s:{d}" for t,d in r["seps"][:6]))
print("\nFrames written to /home/claude/tt/frames — the actual opening second, looked at.")
