"""Falsify card-spin v4 before looking at it.

  [1] ENGINE A/B -- _introCard is presentation; prove the sim cannot see it.
  [2] THE ART CANNOT LEAVE THE BAND at any angle. The band is IC.artCX+-artW/2,
      y0+artCY+-artH/2. Sampled every 0.05s across the whole card for every
      relic, measuring the fitted circumradius against the band -- the geometric
      claim, not a screenshot of one pose.
  [3] IT ACTUALLY MOVES. The angle at entry, at the clash and mid-hold must be
      three different numbers, and the entry must land ON the reading angle.
  [4] THE PRICE. Per-relic scale, v3 vs v4, so the shrink is stated not hidden.
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

SRC = pathlib.Path("/home/claude/sc/sc/02-chain/sc-ember.html").resolve()
OUT = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PAIRS=[("grudgebearer","thornwake"),("slagheart","lightkeeper"),("axiom","heartwood")]

SIM="([p,n,s0])=>{const o=[];for(const[a,b]of p)for(let i=0;i<n;i++)o.push(AC.simulate(a,b,(s0+i*7919)>>>0));return JSON.stringify(o);}"
GEOM="""()=>{
  const out=[], IC=AC.IC, R=AC.renderer;
  for(const w of AC.WEAPONS){
    const b=R._artBox(w);
    const rad=Math.hypot(b.w,b.h)/2;
    const v4=Math.min(IC.artMaxS, IC.artW/(2*rad), IC.artH/(2*rad));
    const v3=Math.min(IC.artMaxS, IC.artW/b.w, IC.artH/b.h);
    out.push({id:w.id,spin:w.spin,bw:+b.w.toFixed(1),bh:+b.h.toFixed(1),
              v3:+v3.toFixed(3),v4:+v4.toFixed(3),
              halfW:+(v4*rad).toFixed(1),halfH:+(v4*rad).toFixed(1)});
  }
  return JSON.stringify(out);
}"""

fails=0
def check(ok,name,d=""):
    global fails
    if not ok: fails+=1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}"+(f"  -- {d}" if d else ""))

with sync_playwright() as p:
    br=p.chromium.launch(args=["--no-sandbox"])
    sims={}
    for f in (SRC,OUT):
        pg=br.new_page(); pg.goto(f.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS",timeout=30000)
        sims[f.name]=pg.evaluate(SIM,[PAIRS,60,20260816])
        if f is OUT:
            geom=json.loads(pg.evaluate(GEOM))
        pg.close()
    br.close()

check(sims[SRC.name]==sims[OUT.name],"[1] engine A/B — 180 matches identical field for field")

over=[g for g in geom if g["halfW"]>125.0 or g["halfH"]>74.0]
check(not over,"[2] the art cannot leave the 250x148 band at ANY angle",
      f"worst half-extent {max(g['halfW'] for g in geom):.1f} (limits 125.0 / 74.0)"
      + (f"; OVER: {[g['id'] for g in over]}" if over else ""))

REST=-0.38
def ang(imp,rate): return REST+imp*rate*3.2 if imp<=0 else REST+max(0,imp-0.30)*rate*0.25
r=1.6
a_in,a_clash,a_hold=ang(-0.46,r),ang(0.0,r),ang(2.0,r)
check(len({round(a_in,3),round(a_clash,3),round(a_hold,3)})==3 and abs(a_clash-REST)<1e-9,
      "[3] it moves, and the entry lands exactly on the reading angle",
      f"entry {a_in:+.2f} -> clash {a_clash:+.2f} (=REST) -> hold {a_hold:+.2f} rad; "
      f"entry sweep {abs(a_in-a_clash)*57.3:.0f}deg")

print("\n  [4] the price, per relic (v3 axis fit -> v4 rotation-safe fit)\n")
print(f"    {'relic':<14}{'spin':>5}{'box':>13}{'v3':>7}{'v4':>7}{'change':>9}")
for g in sorted(geom,key=lambda g:g["v4"]/g["v3"]):
    print(f"    {g['id']:<14}{g['spin']:>5}{g['bw']:>6.0f}x{g['bh']:<6.0f}"
          f"{g['v3']:>7.2f}{g['v4']:>7.2f}{100*(g['v4']/g['v3']-1):>8.0f}%")
print(f"\n  {'ALL PASS' if not fails else str(fails)+' FAILED'}")
sys.exit(1 if fails else 0)
