"""Where does the cold open end? Measure, do not pick.

The card's own opening beat is a CLANK at 0.46s -- two cards flying in and
colliding. If the card is raised at the moment two relics actually collide in
the hall, the fight's impact runs straight into the card's impact. That makes
the anchor a measured quantity, not a taste call: how long until the first
clank, and until the first landed hit, across the roster.
"""
import json, pathlib, statistics as st
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PAIRS = [("grudgebearer","thornwake"),("dawnbringer","widowmaker"),
         ("slagheart","lightkeeper"),("emberedge","gravemourn"),
         ("axiom","heartwood"),("nightfell","censer")]
N, SEED0 = 24, 20260816

JS = """([pairs,n,seed0])=>{
  window.__frozen=true; AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const dt=AC.CONFIG.physics.dt, out=[];
  for(const [a,b] of pairs) for(let i=0;i<n;i++){
    const m=new AC.Match(a,b,(seed0+i*7919)>>>0); m.introT=0;
    let clank=null, hit=null, hp0=300;
    for(let k=0;k<Math.round(20/dt) && !m.over;k++){
      const c0=m.clankCount, ha=m.a.hp, hb=m.b.hp;
      m.step(dt);
      if(clank===null && m.clankCount>c0) clank=m.t;
      if(hit===null && (m.a.hp<ha || m.b.hp<hb)) hit=m.t;
      if(clank!==null && hit!==null) break;
    }
    out.push({a,b,seed:(seed0+i*7919)>>>0,clank,hit});
  }
  return JSON.stringify(out);
}"""

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(GAME.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    rows=json.loads(pg.evaluate(JS,[PAIRS,N,SEED0])); br.close()

def q(v,f): 
    v=sorted(v); return v[min(len(v)-1,int(f*len(v)))]
cl=[r["clank"] for r in rows if r["clank"] is not None]
hi=[r["hit"]   for r in rows if r["hit"]   is not None]
print(f"  {len(rows)} matches, {len(PAIRS)} pairings x {N} seeds\n")
for nm,v,tot in (("first CLANK",cl,len(rows)),("first landed HIT",hi,len(rows))):
    print(f"  {nm:17s} n={len(v)}/{tot}  min {min(v):5.2f}  p25 {q(v,.25):5.2f}  "
          f"median {st.median(v):5.2f}  p75 {q(v,.75):5.2f}  p90 {q(v,.90):5.2f}  max {max(v):5.2f}")
print()
for lim in (1.5,2.0,2.5,3.0,4.0):
    print(f"  a clank has landed by {lim:3.1f}s in {100*sum(1 for x in cl if x<=lim)/len(rows):5.1f}% of matches"
          f"   |  a HIT has landed by {lim:3.1f}s in {100*sum(1 for x in hi if x<=lim)/len(rows):5.1f}%")
