"""The clip's window, event by event (match time, and clip time = match - AT): the cast (its voice), each
touch (the snap's n as played, the walls its record carries, the hex-snap under it), the close (its voice,
clock or death), and the fight still on at the end. Voices READ off SFX.play (a no-op headless)."""
import sys, pathlib, json
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
S = pathlib.Path(__file__).resolve().parent.parent
AT, WIN = 46.62, 12.61
END = AT + WIN
JS = r"""([end]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("lodestone", "heartwood", 102238), me = m.a, th = m.b, ev = [];
  let heard = [];
  const oPlay = AC.SFX.play;
  AC.SFX.play = function(kind, q){ heard.push([kind, q && q.w, q && q.n]); return oPlay.call(this, kind, q); };
  const WN = ["top", "right", "floor", "left"];
  while (!m.over && m.t < end){
    const Z0 = me.ultRunes, r0 = me.lodeFx.slice();
    heard = [];
    m.step(DT);
    for (const x of heard){
      if (x[0] === "ult" && x[1] === "lodestone") ev.push(["cast", m.t, th.stacks("hex")]);
      else if (x[0] === "ult" && x[1] === "lodestone-touch"){
        const q = me.lodeFx.find(r => !r0.includes(r));
        ev.push(["touch", m.t, x[2], q ? q.walls.map(w => WN[w]).join("+") : "-", heard.some(y => y[0] === "hex-snap") ? "hex-snap" : "NO hex-snap", Math.round(m.inset)]);
      } else if (x[0] === "ult" && x[1] === "lodestone-close") ev.push(["close-voice", m.t, th.stacks("hex")]);
    }
    if (Z0 && !me.ultRunes) ev.push(["close", m.t, th.stacks("hex"), me.alive && th.alive ? "clock" : "death"]);
  }
  ev.push(["end", m.t, th.stacks("hex"), m.over ? "over" : "on", Math.round(me.hp), Math.round(th.hp)]);
  delete AC.SFX.play;
  return ev;
}"""
with game(game_path=S / "links/sc-lodestone-b205-fx.html") as (page, errors):
    ev = page.evaluate(JS, [END])
    assert not errors, errors
n_before = sum(1 for e in ev if e[1] < AT and e[0] == "touch")
ev = [e for e in ev if e[1] >= AT]          # the clip's own events (the match's two earlier windows are off-clip)
print(f"(the match's two earlier windows, {n_before} touches, are before the clip and not listed)")
print(f"lodestone v heartwood 102238, the clip from match {AT} for {WIN}s")
for e in ev:
    extra = ""
    if e[0] == "touch": extra = f"  snap n {e[2]}  walls {e[3]}  {e[4]}  inset {e[5]}"
    elif e[0] in ("close", "end"): extra = "  " + " ".join(map(str, e[3:]))
    print(f"  {e[0]:<12} match {e[1]:7.3f}  clip {e[1] - AT:6.3f}" + (f"  foe hex {e[2]}" if e[0] != "touch" else "") + extra)
print(f"  touches {sum(1 for e in ev if e[0] == 'touch')}")
json.dump(ev, open(S / "s6/clip_timeline.json", "w"))
