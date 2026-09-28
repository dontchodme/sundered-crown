"""The clip's window, event by event (match time, and clip time = match - AT): the cast, each bolt's drop,
each landing with the foe's count after it, each miss, the close, and the fight still on at the end."""
import sys, pathlib, json
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
S = pathlib.Path(__file__).resolve().parent.parent
AT, END = 13.63, 13.63 + 11.57
JS = r"""([end]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("ironhail", "cindercleave", 108238), me = m.a, th = m.b, ev = [];
  while (!m.over && m.t < end){
    const Z0 = me.ultHail, T = me.hailTally, l0 = T ? T.landed : 0, x0 = T ? T.missed : 0, d0 = T ? T.drops : 0, hs = m.hitStop;
    m.step(DT);
    const T1 = me.hailTally;
    if (me.ultHail && !Z0) ev.push(["cast", m.t, th.stacks("sunder")]);
    if (T1 && T1.drops > d0) ev.push(["drop", m.t, th.stacks("sunder")]);
    if (T1 && T1.landed > l0) ev.push(["landing", m.t, th.stacks("sunder")]);
    if (T1 && T1.missed > x0) ev.push(["miss", m.t, th.stacks("sunder")]);
    if (Z0 && !me.ultHail) ev.push(["close", m.t, th.stacks("sunder"), me.alive && th.alive ? "clock" : "death"]);
  }
  ev.push(["end", m.t, th.stacks("sunder"), m.over ? "over" : "on", Math.round(me.hp), Math.round(th.hp)]);
  return ev;
}"""
with game(game_path=S / "links/sc-ironhail-sunder-fx.html") as (page, errors):
    ev = page.evaluate(JS, [END])
    assert not errors, errors
for e in ev:
    if e[0] == "drop": continue
    print(f"  {e[0]:<8} match {e[1]:7.3f}  clip {e[1] - AT:6.3f}  foe sunder {e[2]}" + ("  " + " ".join(map(str, e[3:])) if len(e) > 3 else ""))
print(f"  drops {sum(1 for e in ev if e[0] == 'drop')}, landings {sum(1 for e in ev if e[0] == 'landing')}, misses {sum(1 for e in ev if e[0] == 'miss')}")
json.dump(ev, open(S / "s6/clip_timeline.json", "w"))
