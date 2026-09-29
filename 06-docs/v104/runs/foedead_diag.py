"""Scratch: where does tickRise see the foe dead with the caster alive and the match not over?"""
import sys, pathlib
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
JS = r"""([foes, seeds]) => {
  const P = AC.Match.prototype, oT = P.tickRise, out = [];
  P.tickRise = function(dt){
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a;
      if (f.w.id === "angelus" && f.ultRise && f.alive && !foe.alive && !this.over)
        out.push({foe: foe.w.id, status: Object.keys(foe.status).join("+"), seed: this.seed, t: +this.t.toFixed(3), kf: this.killFlight ? JSON.stringify(this.killFlight) : null, hp: foe.hp, lit: f.ultRise.lit});
    }
    return oT.call(this, dt);
  };
  let n = 0, over = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "angelus", sd) : new AC.Match("angelus", fid, sd);
    m.seed = sd;
    let k = 0; while (!m.over && k < 160 * 120){ m.step(1/120); k++; }
    n++;
  }
  P.tickRise = oT;
  return {n, out};
}"""
game_path = pathlib.Path(sys.argv[1])
foes = [w for w in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else None
with game(game_path=game_path) as (page, errors):
    if not foes:
        foes = page.evaluate("() => AC.WEAPONS.map(w => w.id).filter(i => i !== 'angelus')")
    seeds = [104001 + 13 * i for i in range(6)]
    R = page.evaluate(JS, [foes, seeds])
    print(R["n"], "fights;", len(R["out"]), "ticks with the foe dead, the caster alive, not over")
    for o in R["out"][:40]: print(" ", o)
    from collections import Counter
    print("foe statuses at those ticks:", Counter(o["status"] for o in R["out"]).most_common())
