"""The clip's fight, headless: every stage-6 event of Censer v Slagheart 109149 in match time (the HUD's clock),
from 29 s to 43 s, and the fight's state at the clip's end (42.8167 in cinema_clip's log)."""
import pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
FX = pathlib.Path(__file__).resolve().parent.parent / "links" / "sc-censer-consecration-b25.5-fx.html"
JS = r"""() => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("censer", "slagheart", 109149), me = m.a, th = m.b;
  const ev = [], V = []; const oPlay = AC.SFX.play;
  AC.SFX.play = function(k, q){ if (k === "ult" && q && (q.w === "censer" || q.w === "censer-disc")) V.push(q.w + (q.n ? " n" + q.n : ""));
    else if (k === "spark" && q && q.collect) V.push("chime n" + q.n); else if (k === "death") V.push("death");
    return oPlay.call(this, k, q); };
  let steps = 0, s0 = 0;
  try {
    while (!m.over && m.t < 42.82){
      const T0 = me.holyTally ? Object.assign({}, me.holyTally) : null, Z0 = me.ultHoly, tags0 = new Set(m.tags);
      V.length = 0; m.step(DT); steps++;
      const T = me.holyTally, Z = me.ultHoly, out = [];
      if (m.t < 29) continue;
      if (!Z0 && Z) out.push("CAST (window opens)");
      if (Z0 && !Z) out.push("CLOSE " + (Z0.t + DT >= Z0.dur - 1e-9 ? "by the clock" : "by a death") + ", discs standing " + m.holyGround.filter(d => d.side === "a").length);
      if (T && T0){ if (T.discs > T0.discs) out.push("disc #" + T.discs + " planted (standing " + m.holyGround.filter(d => d.side === "a").length + ")");
        if (T.ticks > T0.ticks) out.push("smite tick (foe smite " + th.stacks("smite") + ")");
        if (T.bless > T0.bless) out.push("blessing (Censer " + me.stacks("blessing") + ")"); }
      for (const g of m.tags) if (!tags0.has(g)) out.push("TAG " + g.key.toUpperCase() + " " + g.val);
      if (V.length) out.push("voices: " + V.join(", "));
      if (m.hitStop > 0 && !s0){ s0 = 1; } if (m.hitStop <= 0) s0 = 0;
      if (out.length) ev.push([+m.t.toFixed(3), out.join("; ")]);
    }
  } finally { AC.SFX.play = oPlay; }
  return { ev, end: { t: +m.t.toFixed(4), over: m.over, hp: [+me.hp.toFixed(2), +th.hp.toFixed(2)], clanks: m.clankCount,
                      discs: m.holyGround.length } };
}"""
with game(game_path=FX) as (page, errors):
    R = page.evaluate(JS)
    assert not errors, errors
for t, e in R["ev"]:
    print(f"  {t:8.3f}  {e}")
print("end:", R["end"])
