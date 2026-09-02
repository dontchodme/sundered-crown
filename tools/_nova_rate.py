"""HOW OFTEN DO ALL THREE ARROWS OF A VOLLEY ACTUALLY LAND?

Rick: "how about when all 3 connect the arrows explode in a nova for more damage
and knockback?"

"Connect" has two readings and they are three orders of magnitude apart, so the
frequency is measured before the mechanic is written down:

  ALL THREE HIT THE QUARRY. A payoff you would wait for.
  ALL THREE RESOLVED (wall, parry or quarry). That is every volley, always.

Counted per volley: how many of its arrows landed ON THE ENEMY, and separately
how many resolved at all. Runtime only. NOTHING is written to any build.
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game

JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const hist = [0, 0, 0, 0];      // volleys with 0/1/2/3 arrows landed on the foe
  let volleys = 0, arrows = 0, landed = 0, strandHit = 0;
  let bothAndFull = 0;
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const own = me === m.a ? "a" : "b";
      const V = new Map(), seen = new Set(), spent = new Set();

      const origHit = AC.Match.prototype.resolveHit;
      m.resolveHit = function(self, foe2){
        const s = m._cineShot;
        if (s && s.net && self === me){
          const v = V.get(s.volley); if (v) v.hit++;
        }
        return origHit.apply(m, arguments);
      };
      const origFire = AC.Match.prototype.tickFire;
      m.tickFire = function(f2){
        const r = origFire.apply(m, arguments);
        if (f2 === me) for (const s of m.shots){
          if (!s.net || s.own !== own || seen.has(s)) continue;
          seen.add(s); arrows++;
          let v = V.get(s.volley);
          if (!v) V.set(s.volley, v = { hit: 0, n: 0, light: false });
          v.n++;
        }
        return r;
      };
      const origNet = AC.Match.prototype.tickNet;
      m.tickNet = function(){
        const r = origNet.apply(m, arguments);
        for (const s of m.shots){
          if (!s.net || s.own !== own) continue;
          if (s.strandSpent && !spent.has(s)){
            spent.add(s);
            const v = V.get(s.volley); if (v) v.light = true;
          }
        }
        return r;
      };
      let i = 0;
      while (!m.over && i < secs / DT){ m.step(DT); i++; }
      for (const v of V.values()){
        volleys++; landed += v.hit;
        hist[Math.min(3, v.hit)]++;
        if (v.light) strandHit++;
        if (v.hit === 3 && v.light) bothAndFull++;
      }
    }
  }
  return { volleys, arrows, landed, hist, strandHit, bothAndFull };
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-crossweave.html")
ap.add_argument("--sn", type=int, default=6)
a = ap.parse_args()
gp = resolve_game(a.game)
seeds = [4201 + 17 * i for i in range(a.sn)]
with game(game_path=gp) as (page, errors):
    W = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [w for w in W if w != "gloamwire"]
    r = page.evaluate(JS, ["gloamwire", foes, seeds, 120.0])
    assert not errors, errors[:4]
V = max(1, r["volleys"])
print(f"\n  {r['volleys']} volleys, {r['arrows']} arrows, {r['landed']} landed "
      f"on the quarry ({r['landed']/max(1,r['arrows']):.1%} an arrow)\n")
print("  ARROWS OF A VOLLEY THAT LANDED ON THE ENEMY\n")
for k in range(4):
    print(f"    {k} of 3 {r['hist'][k]:>8}   {r['hist'][k]/V:7.2%}"
          + ("   <- the nova, on the strict reading" if k == 3 else ""))
print(f"\n  volleys landing a STRAND    {r['strandHit']:>8}   {r['strandHit']/V:7.2%}")
print(f"  all 3 landed AND a strand   {r['bothAndFull']:>8}   {r['bothAndFull']/V:7.2%}")
