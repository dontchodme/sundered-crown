import sys, json, pathlib
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game
link, a, b, seed, t0, t1 = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
JS = r"""([a, b, seed, t0, t1]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(a, b, seed); const me = m.a.w.id === "widowmaker" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const ev = []; let pb = null, pu = [0, 0];
  while (!m.over && m.t < t1){
    m.step(DT);
    const u = [me.ultsFired, th.ultsFired];
    if (m.t >= t0 && (u[0] !== pu[0] || u[1] !== pu[1])) ev.push(["ultsFired", +m.t.toFixed(3), u]);
    pu = u;
    const bt = m.banner ? m.banner.text : null;
    if (m.t >= t0 && bt !== pb) ev.push(["banner", +m.t.toFixed(3), bt]);
    pb = bt;
  }
  return ev;
}"""
with game(game_path=pathlib.Path(link).resolve()) as (page, errors):
    R = page.evaluate(JS, [a, b, seed, t0, t1]); assert not errors, errors
for e in R: print(e)
