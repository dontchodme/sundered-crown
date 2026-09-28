"""The clip's window, event by event (match time and clip time = match - 30.85): the cast, each won
bind and the loser's count, the first frame past 6, the close, and the fight still on at the end."""
import sys, pathlib
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
S = pathlib.Path(__file__).resolve().parent.parent
AT = 30.85
JS = r"""() => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("coldiron", "vinesower", 103349), me = m.a, th = m.b, ev = [];
  let past = false;
  while (!m.over && m.t < 44){
    const Z0 = me.ultTemper, w0 = me.temperTally ? me.temperTally.won : 0, h0 = me.hits;
    m.step(DT);
    if (me.ultTemper && !Z0) ev.push(["cast", m.t, th.stacks("sunder")]);
    if (me.temperTally && me.temperTally.won > w0) ev.push(["won bind", m.t, th.stacks("sunder")]);
    if (me.ultTemper && me.hits > h0) ev.push(["blow", m.t, th.stacks("sunder")]);
    if (!past && th.stacks("sunder") > 6){ past = true; ev.push(["past 6", m.t, th.stacks("sunder")]); }
    if (Z0 && !me.ultTemper) ev.push(["close", m.t, th.stacks("sunder"), me.alive && th.alive ? "clock" : "death"]);
  }
  ev.push(["end", m.t, th.stacks("sunder"), m.over ? "over" : "on", me.hp, th.hp]);
  return ev;
}"""
with game(game_path=S / "links/sc-coldiron-temper-fx.html") as (page, errors):
    ev = page.evaluate(JS)
    assert not errors, errors
for e in ev:
    print(f"  {e[0]:<9} match {e[1]:7.3f}  clip {e[1] - AT:6.3f}  foe sunder {e[2]}" + ("  " + " ".join(map(str, e[3:])) if len(e) > 3 else ""))
