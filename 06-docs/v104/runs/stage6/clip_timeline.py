"""v104 stage 6, scratch: THE CLIP'S FIGHT, HEADLESS -- the match times of the window's events and the state at
the clip's end, to set against what cinema_clip printed (v106's snapcheck.py, for Angelus).

    python clip_timeline.py <link> <a> <b> <seed> <t_end>
"""
import json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

link, a, b, seed, tend = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
JS = r"""([a, b, seed, tend]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(a, b, seed);
  const me = m.a.w.id === "angelus" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const ev = []; let V = [];
  const oPlay = AC.SFX.play;
  AC.SFX.play = function(kind, q){ if (kind === "ult" && q && typeof q.w === "string" && q.w.startsWith("angelus")) V.push(q.n ? q.w + " " + q.n : q.w); return oPlay.call(this, kind, q); };
  let stopOn = false;
  try {
    while (!m.over && m.t < tend){
      const Z0 = me.ultRise, h0 = me.hits, th0 = th.hits, a0 = me.riseTally ? me.riseTally.arrivals : 0;
      V = [];
      m.step(DT);
      const T = m.t.toFixed(3), Z = me.ultRise;
      for (const v of V) ev.push([T, "voice", v]);
      if (Z && !Z0) ev.push([T, "cast", `at (${me.x.toFixed(0)}, ${me.y.toFixed(0)})`]);
      if (me.riseTally && me.riseTally.arrivals > a0) ev.push([T, "arrival: the shafts light", `(${me.x.toFixed(0)}, ${me.y.toFixed(0)})`]);
      if (Z0 && Z0.lit && me.hits > h0) ev.push([T, "shaft blow", `foe hp ${th.hp.toFixed(2)}`]);
      if (Z && th.hits > th0) ev.push([T, "the foe's blow on the hung ball", `hp ${me.hp.toFixed(2)}`]);
      const st = m.hitStop > 0 && !!Z && !!Z.lit;
      if (st && !stopOn) ev.push([T, "hit stop (lit) begins", ""]);
      stopOn = st;
      if (!Z && Z0) ev.push([T, "close", `window clock ${Z0.t.toFixed(3)} of ${Z0.dur}; hp ${me.hp.toFixed(2)} / ${th.hp.toFixed(2)}`]);
    }
  } finally { AC.SFX.play = oPlay; }
  return { ev, t: m.t, over: m.over, hp: [m.a.hp, m.b.hp], pos: [[m.a.x, m.a.y], [m.b.x, m.b.y]] };
}"""
with game(game_path=pathlib.Path(link).resolve()) as (page, errors):
    R = page.evaluate(JS, [a, b, seed, tend]); assert not errors, errors[:3]
print(f"CLIP TIMELINE {pathlib.Path(link).name}  {a} v {b} {seed}, headless to match time {tend}")
for e in R["ev"]:
    print(f"  {e[0]:>9}  {e[1]:<34} {e[2]}")
print(f"  end: t {R['t']:.4f}  over {R['over']}  hp {R['hp']}  positions {json.dumps([[round(v, 2) for v in p] for p in R['pos']])}")
