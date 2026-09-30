"""The clip's fight, headless: every stage-6 event of Spellbreaker (side A) v FOE, SEED, in match time (the HUD's
clock), from FROM to END, and the fight's state at END (cinema_clip's log gives its end time).
    python clip_timeline6.py <game> <foe> <seed> <from> <end>"""
import pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
GAME, FOE, SEED, FROM, END = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
JS = r"""([FOE, SEED, FROM, END]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("spellbreaker", FOE, SEED), me = m.a, th = m.b;
  const ev = [], V = []; const oPlay = AC.SFX.play;
  AC.SFX.play = function(k, q){ if (k === "ult" && q) V.push(q.w); else if (k === "death") V.push("death");
    return oPlay.call(this, k, q); };
  let steps = 0, greyWas = false;
  try {
    while (!m.over && m.t < END){
      const x0 = me.unmakeTally ? me.unmakeTally.extra : 0, Z0 = me.ultUnmake, tags0 = new Set(m.tags), bn0 = m.banner;
      const tv0 = new Map(m.tags.map(g => [g, g.val]));
      V.length = 0; m.step(DT); steps++;
      const Z = me.ultUnmake, out = [];
      if (m.t < FROM) { greyWas = th.unmkGrey > 0; continue; }
      if (!Z0 && Z) out.push("CAST (the script writes)");
      if (Z0 && !Z) out.push("CLOSE " + (Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive ? "by the clock" : "by a death"));
      if (m.banner && m.banner !== bn0) out.push("BANNER " + m.banner.text + (m.banner.onTarget ? " (on the foe)" : ""));
      const x1 = me.unmakeTally ? me.unmakeTally.extra : 0;
      if (x1 > x0) out.push("second hex x" + (x1 - x0));
      const grey = th.unmkGrey > 0;
      if (grey && !greyWas) out.push("foe's weapon GREY (stun " + th.stun.toFixed(3) + ")");
      if (!grey && greyWas) out.push("grey off");
      greyWas = grey;
      for (const g of m.tags) if (!tags0.has(g)) out.push("TAG " + g.key.toUpperCase() + " " + g.val + (g.first ? " (panel)" : ""));
      for (const g of m.tags) if (tags0.has(g) && tv0.get(g) !== g.val) out.push("TAG relabelled " + g.key.toUpperCase() + " " + g.val);
      if (V.length) out.push("voices: " + V.join(", "));
      if (out.length) ev.push([+m.t.toFixed(3), out.join("; ")]);
    }
  } finally { AC.SFX.play = oPlay; }
  return { ev, end: { t: +m.t.toFixed(4), over: m.over, hp: [+me.hp.toFixed(2), +th.hp.toFixed(2)], clanks: m.clankCount,
                      script: +me.unmkFade.toFixed(3), motes: me.unmkMotes.length } };
}"""
with game(game_path=GAME) as (page, errors):
    R = page.evaluate(JS, [FOE, SEED, FROM, END])
    assert not errors, errors
print(f"Spellbreaker v {FOE}, seed {SEED}, {GAME.name}: every stage-6 event from {FROM} to {END} (match time)")
for t, e in R["ev"]:
    print(f"  {t:8.3f}  {e}")
print("end:", R["end"])
