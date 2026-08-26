#!/usr/bin/env python3
"""WHY IS THE DRAIN NOT LEGIBLE? Measure before changing anything."""
import pathlib, sys, statistics
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  const P = AC.Match.prototype;
  let heals = [], blocked = 0, hitsWhileLs = 0, spawnCalls = 0, motes = 0;
  const oh = P.resolveHit;
  P.resolveHit = function(self, foe){
    const ls = self.lifesteal || self.w.lifesteal;
    const before = self.hp, cap = self.maxHp;
    const r = oh.apply(this, arguments);
    if (ls){
      hitsWhileLs++;
      const got = Math.round(self.hp - before);
      if (got >= 1) heals.push(got);
      else blocked++;          // clamped at full hp, or rounded to nothing
    }
    return r;
  };
  const od = P.drain;
  P.drain = function(from, to, amount){ spawnCalls++; const n0 = this.drains.length;
    const rr = od.apply(this, arguments); motes += this.drains.length - n0; return rr; };

  let steps = 0, framesWithDrain = 0, framesWithSplit = 0, peak = 0;
  let framesWithTether = 0, framesWithAny = 0;
  let castFrames = 0;
  for (const f of foes) for (const s of seeds){
    const m = new AC.Match(id, f, s);
    m.introT = 0;
    let g = 0;
    while (!m.over && g++ < DT_FPS * 120){
      m.step(DT); steps++;
      const me = m.a.w.id === id ? m.a : m.b;
      if (me.ultSplit){
        framesWithSplit++;
        if (m.drains.length) framesWithDrain++;
        const th = me === m.a ? m.b : m.a;
        if ((th.drained || 0) > 0.02) framesWithTether++;
        if (m.drains.length || (th.drained || 0) > 0.02) framesWithAny++;
      }
      peak = Math.max(peak, m.drains.length);
    }
  }
  P.resolveHit = oh; P.drain = od;
  heals.sort((a,b)=>a-b);
  return { steps, framesWithSplit, framesWithDrain, peak,
           framesWithTether, framesWithAny,
           hitsWhileLs, healCount: heals.length, blocked, spawnCalls, motes,
           healMin: heals[0] || 0, healMed: heals[heals.length>>1] || 0,
           healMax: heals[heals.length-1] || 0,
           healMean: heals.length ? heals.reduce((a,b)=>a+b,0)/heals.length : 0 };
}"""

with game(game_path=(HERE / "../02-chain/sc-twinshade.html").resolve()) as (p, e):
    r = p.evaluate(JS, ["twinshade",
        ["thornwake","lightkeeper","emberedge","gravemourn","widowmaker","heartwood"],
        [90210 + i*7919 for i in range(10)]])
    if e: print("PAGE ERRORS:", e[:3])

fs, fd = r["framesWithSplit"], r["framesWithDrain"]
print(f"""
  HOW OFTEN IS A LIFESTEAL HEAL EVEN HAPPENING?

    hits landed while lifesteal was on   {r['hitsWhileLs']:>6}
    of those, healed >= 1 hp             {r['healCount']:>6}   ({100*r['healCount']/max(1,r['hitsWhileLs']):.0f}%)
    of those, healed NOTHING             {r['blocked']:>6}   ({100*r['blocked']/max(1,r['hitsWhileLs']):.0f}%)
       <- clamped at full hp, or rounded to 0

    hp per heal    min {r['healMin']}   median {r['healMed']}   mean {r['healMean']:.1f}   max {r['healMax']}
    motes spawned  {r['motes']} over {r['spawnCalls']} heals
                   = {r['motes']/max(1,r['spawnCalls']):.1f} per heal

  HOW MUCH OF THE ULTIMATE HAS A DRAIN ON SCREEN?

    frames with the split running        {fs:>6}
    of those, with a mote in flight      {fd:>6}   ({100*fd/max(1,fs):.0f}%)
    of those, with the tether lit        {r['framesWithTether']:>6}   ({100*r['framesWithTether']/max(1,fs):.0f}%)
    of those, with EITHER                {r['framesWithAny']:>6}   ({100*r['framesWithAny']/max(1,fs):.0f}%)
    peak motes in flight at once         {r['peak']:>6}
""")
