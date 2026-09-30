"""Scratch: what happened on the step verify flagged (spellbreaker v twinshade 2207, t 24.483)."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
JS = r"""() => {
  AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("spellbreaker", "twinshade", 2207), me = m.a, th = m.b;
  const log = [];
  const ost = m.statusTag, orh = m.resolveHit;
  let step = 0, cur = [];
  m.statusTag = function(x, y, key, first, val){ cur.push(["tag", key, first, +x.toFixed(2), +y.toFixed(2), this.tags.length]); const r = ost.call(this, x, y, key, first, val); const g = this.tags[this.tags.length - 1]; if (g) g.__s = step + 1; return r; };
  m.resolveHit = function(self, foe, hx, hy, seg, mul, over){ cur.push(["hit", self.w.id + (self.shade ? "(shade)" : ""), foe.w.id + (foe.shade ? "(shade)" : ""), foe.alive, !!self.ultUnmake, mul, over ? Object.keys(over) : null]);
    const r = orh.call(this, self, foe, hx, hy, seg, mul, over); cur.push(["after", foe.alive]); return r; };
  while (!m.over && step < 200 / DT){
    cur = [];
    const x0 = me.unmakeTally ? me.unmakeTally.extra : 0;
    m.step(DT); step++;
    const dx = (me.unmakeTally ? me.unmakeTally.extra : 0) - x0;
    if (m.t > 24.3 && m.t < 24.7 && (dx || cur.length))
      log.push({ t: +m.t.toFixed(3), step, dx, cur, stop: m.hitStop, fresh: m.tags.filter(g => g.__s === step).map(g => [g.key, g.val, g.first, g.life, g.max, g.unmk || false]),
                 shades: m.shades.length });
    if (m.t > 24.8) break;
  }
  return log;
}"""
with game(game_path=HERE / "sb-final-fx.html") as (page, errors):
    for e in page.evaluate(JS): print(json.dumps(e))
    assert not errors, errors[:3]
