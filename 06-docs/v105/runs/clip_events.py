"""The pick's window events on the match clock (oracle v heartwood 105312), to choose the five checked frames."""
import sys, pathlib, json
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
L = pathlib.Path(__file__).resolve().parents[1] / "links/sc-oracle-fx.html"
JS = r"""() => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("oracle", "heartwood", 105312), me = m.a, th = m.b, ev = [];
  let st = 0, was = null;
  while (!m.over && m.t < 42){
    const T0 = me.sightTally ? Object.assign({}, me.sightTally) : null, Z0 = me.ultSight;
    m.step(DT); st++;
    const Z = me.ultSight, T = me.sightTally;
    if (Z && !Z0) ev.push(["cast", +m.t.toFixed(3)]);
    if (!Z && Z0) ev.push(["close", +m.t.toFixed(3), me.alive && th.alive ? "clock" : "death"]);
    if (T && T0 && T.hex > T0.hex) ev.push(["hex2", +m.t.toFixed(3), th.stacks("hex")]);
    if (T && T0 && T.arrows > T0.arrows && !(T.hex > T0.hex)) ev.push(["arrow-no-hex", +m.t.toFixed(3)]);
  }
  return { ev, t: m.t, hp: [me.hp, th.hp] };
}"""
with game(game_path=L) as (page, errors):
    R = page.evaluate(JS)
for e in R["ev"]:
    print(e, " video ~%.2f" % (e[1] - 29.18))
print("end", R["t"], R["hp"])
