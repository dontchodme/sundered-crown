"""The clip's fight, headless: every stage-6 event of Aureole v Spellbreaker 110075 in match time (the HUD's
clock), from 43 s to the clip's end, and the fight's state there (cinema_clip's log gives its end time)."""
import pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
FX = pathlib.Path(__file__).resolve().parent.parent / "links" / "sc-aureole-b12.5-fx.html"
END = float(sys.argv[1]) if len(sys.argv) > 1 else 55.87
JS = r"""(END) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("aureole", "spellbreaker", 110075), me = m.a, th = m.b;
  const ev = [], V = []; const oPlay = AC.SFX.play;
  AC.SFX.play = function(k, q){ if (k === "ult" && q && /^aureole/.test(q.w)) V.push(q.w);
    else if (k === "ult" && q) V.push("ult " + q.w);
    else if (k === "spark" && q && q.collect) V.push("chime n" + q.n); else if (k === "death") V.push("death");
    return oPlay.call(this, k, q); };
  let steps = 0;
  try {
    while (!m.over && m.t < END){
      const T0 = me.haloTally ? Object.assign({}, me.haloTally) : null, Z0 = me.ultHalo, tags0 = new Set(m.tags), bn0 = m.banner;
      V.length = 0; m.step(DT); steps++;
      const T = me.haloTally, Z = me.ultHalo, out = [];
      if (m.t < 43) continue;
      if (!Z0 && Z) out.push("CAST (the halo rises)");
      if (Z0 && !Z) out.push("CLOSE " + (Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive ? "by the clock" : "by a death"));
      if (m.banner && m.banner !== bn0) out.push("BANNER " + m.banner.text);
      if (T && T0){
        if (T.frames > T0.frames){ const IN = T.inFrames > T0.inFrames; if (IN !== ev.lastIn){ out.push(IN ? "foe INSIDE" : "foe outside"); ev.lastIn = IN; } }
        if (T.smite > T0.smite) out.push("smite (foe smite " + th.stacks("smite") + ")");
        if (T.bless > T0.bless) out.push("blessing (Aureole " + me.stacks("blessing") + ")"); }
      if (!Z) ev.lastIn = undefined;
      for (const g of m.tags) if (!tags0.has(g)) out.push("TAG " + g.key.toUpperCase() + " " + g.val);
      if (V.length) out.push("voices: " + V.join(", "));
      if (out.length) ev.push([+m.t.toFixed(3), out.join("; ")]);
    }
  } finally { AC.SFX.play = oPlay; }
  return { ev: ev.slice(), end: { t: +m.t.toFixed(4), over: m.over, hp: [+me.hp.toFixed(2), +th.hp.toFixed(2)], clanks: m.clankCount } };
}"""
with game(game_path=FX) as (page, errors):
    R = page.evaluate(JS, END)
    assert not errors, errors
for t, e in R["ev"]:
    print(f"  {t:8.3f}  {e}")
print("end:", R["end"])
