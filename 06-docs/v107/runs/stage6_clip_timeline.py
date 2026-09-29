"""The clip's fight, headless (the same Match the clip films: Lightkeeper side A v Redflail, seed 107201,
on the fx link): the MATCH time of every Bulwark event in the filmed span, to find its frame in the clip
by the HUD's clock. Casts, blocks, arrows, banks ("+N" floats), WARD tags, the close and its kind, the
fold (bulwarkFade reaching 0), and Lightkeeper voices through a wrapped SFX.play (a no-op headless)."""
import json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
G = sys.argv[1]
JS = r"""([a, b, seed, t0, t1]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match(a, b, seed), me = m.a, ev = [];
  const oP = AC.SFX.play;
  AC.SFX.play = function(k, q){ if (k === "ult" && q && /^lightkeeper/.test(q.w || "")) ev.push([+m.t.toFixed(3), "voice " + q.w + (q.k !== undefined ? ":" + q.k : "")]); return oP.apply(this, arguments); };
  let fade0 = 0, T0 = { b: 0, a: 0, k: 0 }, Z0 = null, nF = 0, nG = 0;
  try {
    while (!m.over && m.t < t1){
      const fl0 = m.floats.length, tg0 = m.tags.length;
      m.step(DT);
      if (m.t < t0) { Z0 = me.ultWall; fade0 = me.bulwarkFade; if (me.wallTally) T0 = { b: me.wallTally.blocks, a: me.wallTally.arrows, k: me.wallTally.banked }; continue; }
      const T = me.wallTally, Z = me.ultWall;
      if (Z && !Z0) ev.push([+m.t.toFixed(3), "CAST (window opens)"]);
      if (T){
        if (T.blocks > T0.b) ev.push([+m.t.toFixed(3), `block x${T.blocks - T0.b}`]);
        if (T.arrows > T0.a) ev.push([+m.t.toFixed(3), `arrow x${T.arrows - T0.a}`]);
        T0 = { b: T.blocks, a: T.arrows, k: T.banked };
      }
      for (const q of m.floats.slice(fl0)) if (/^\+\d/.test(q.text || "")) ev.push([+m.t.toFixed(3), `float ${q.text}`]);
      for (const g of m.tags.slice(tg0)) if (g.key === "ward") ev.push([+m.t.toFixed(3), `tag WARD`]);
      if (!Z && Z0) ev.push([+m.t.toFixed(3), `CLOSE (${me.alive && m.b.alive ? "clock" : "death"})`]);
      if (fade0 > 0 && !(me.bulwarkFade > 0)) ev.push([+m.t.toFixed(3), "fold done (bulwarkFade 0)"]);
      Z0 = Z; fade0 = me.bulwarkFade;
    }
  } finally { AC.SFX.play = oP; }
  return { ev, t: m.t, over: m.over, hp: [m.a.hp, m.b.hp] };
}"""
with game(game_path=pathlib.Path(G).resolve()) as (page, errors):
    R = page.evaluate(JS, ["lightkeeper", "redflail", 107201, 47.64, 60.87])
    assert not errors, errors
for t, e in R["ev"]:
    print(f"{t:8.3f}  {e}")
print("end", R["t"], "over", R["over"], "hp", R["hp"])
