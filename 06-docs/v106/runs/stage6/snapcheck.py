import sys, json, pathlib
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game
link, a, b, seed, tend = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
JS = r"""([a, b, seed, tend]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const m = new AC.Match(a, b, seed); const me = m.a.w.id === "widowmaker" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const ev = []; let prevZ = null, prevSnap = null;
  while (!m.over && m.t < tend){
    const Z0 = me.ultDrain; m.step(DT);
    if (me.ultDrain && !Z0) ev.push(["cast", +m.t.toFixed(3)]);
    if (!me.ultDrain && Z0) ev.push(["close", +m.t.toFixed(3), "d now", +Math.hypot(me.x - th.x, me.y - th.y).toFixed(1)]);
    if (me.siphonSnap && me.siphonSnap !== prevSnap){ const S = me.siphonSnap; ev.push(["snap", +m.t.toFixed(3), "d at snap", +Math.hypot(S.sx - S.fx, S.sy - S.fy).toFixed(1), "gap", 2 * R + 10, "g", +S.g.toFixed(3)]); }
    prevSnap = me.siphonSnap;
  }
  return { ev, t: m.t, hp: [m.a.hp, m.b.hp], over: m.over };
}"""
with game(game_path=pathlib.Path(link).resolve()) as (page, errors):
    R = page.evaluate(JS, [a, b, seed, tend]); assert not errors, errors
print(json.dumps(R))
