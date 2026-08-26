"""WHERE should the name plate sit? Measure, do not pick.

The plate is up from the first clank for ~3s. In that window the relics are
somewhere specific -- they have just collided -- and the honest place for a
temporary overlay is the horizontal band they occupy LEAST. Sampling the real
simulation across the roster answers that; taste does not.

Arena geometry, read from the build rather than assumed:
  W 1080  H 1920  pad 12  hud 152  arenaTop 176
  sim arena 520 x 800, scale = (1080-24)/520 = 2.0308  ->  ah = 1624.6
  so the hall occupies screen y 176 .. 1800.6
"""
import json, pathlib, statistics as st
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PAIRS = [("ironhail","oathwound"),("emberedge","thornwake"),("dawnbringer","censer"),
         ("gravemourn","heartwood"),("widowmaker","aureole"),("axiom","nightfell"),
         ("grudgebearer","thornwake"),("slagheart","lightkeeper")]
N, SEED0, PLATE = 16, 20260819, 3.0

JS = """([pairs,n,seed0,plate])=>{
  window.__frozen=true; AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const dt=AC.CONFIG.physics.dt, H=800, out=[];
  for(const [a,b] of pairs) for(let i=0;i<n;i++){
    const m=new AC.Match(a,b,(seed0+i*7919)>>>0); m.introT=0;
    let clank=null, ys=[];
    for(let k=0;k<Math.round(30/dt) && !m.over;k++){
      const c0=m.clankCount;
      m.step(dt);
      if(clank===null && m.clankCount>c0) clank=m.t;
      if(clank!==null && m.t>=clank && m.t<=clank+plate){
        // sample the ball CENTRES and the reach of each weapon, in sim y
        ys.push([m.a.y, m.b.y]);
      }
      if(clank!==null && m.t>clank+plate) break;
    }
    if(ys.length) out.push({a,b,clank,ys});
  }
  return JSON.stringify(out);
}"""

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"]); pg=br.new_page()
    pg.goto(GAME.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
    rows=json.loads(pg.evaluate(JS,[PAIRS,N,SEED0,PLATE])); br.close()

BANDS = 16                      # 800 sim units / 16 = 50 units per band = ~101 screen px
occ = [0]*BANDS; tot = 0
for r in rows:
    for ya, yb in r["ys"]:
        for y in (ya, yb):
            occ[min(BANDS-1, max(0, int(y/800*BANDS)))] += 1
            tot += 1

print(f"  {len(rows)} matches, {tot} relic-samples inside the {PLATE:.1f}s plate window\n")
print(f"  {'sim y':>12s} {'screen y':>15s}   share of relic-time   ")
for i,c in enumerate(occ):
    y0,y1 = i*800/BANDS, (i+1)*800/BANDS
    s0,s1 = 176+y0*2.0308, 176+y1*2.0308
    pct = 100*c/tot
    print(f"  {y0:5.0f}-{y1:3.0f} {s0:7.0f}-{s1:4.0f}   {pct:5.1f}%  " + "#"*int(pct*2.2))

# best contiguous 2-band (100 sim units ~= 203 screen px) window
best = min(range(BANDS-1), key=lambda i: occ[i]+occ[i+1])
b0,b1 = best*800/BANDS, (best+2)*800/BANDS
print(f"\n  quietest 2-band window: sim y {b0:.0f}-{b1:.0f}"
      f"  = screen y {176+b0*2.0308:.0f}-{176+b1*2.0308:.0f}"
      f"   ({100*(occ[best]+occ[best+1])/tot:.1f}% of relic-time)")
worst = max(range(BANDS-1), key=lambda i: occ[i]+occ[i+1])
print(f"  busiest 2-band window : sim y {worst*800/BANDS:.0f}-{(worst+2)*800/BANDS:.0f}"
      f"   ({100*(occ[worst]+occ[worst+1])/tot:.1f}%)  -- {(occ[worst]+occ[worst+1])/max(1,occ[best]+occ[best+1]):.1f}x the quietest")
print(f"\n  clank times: median {st.median([r['clank'] for r in rows]):.2f}s")
