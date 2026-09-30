"""The clip's fight, headless: every stage-6 event of Thornwake (side A) v FOE, SEED, in match time (the HUD's
clock), from FROM to END, and the fight's state at END (cinema_clip's log gives its end time).
    python clip_timeline6.py <game> <foe> <seed> <from> <end>"""
import pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
GAME, FOE, SEED, FROM, END = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
JS = r"""([FOE, SEED, FROM, END]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("thornwake", FOE, SEED), me = m.a, th = m.b;
  const ev = [], V = []; const oPlay = AC.SFX.play;
  AC.SFX.play = function(k, q){ if (k === "ult" && q) V.push(q.w); else if (k === "death") V.push("death");
    return oPlay.call(this, k, q); };
  let steps = 0, heldWas = false, greenWas = 0;
  try {
    while (!m.over && m.t < END){
      const Z0 = me.ultBramble, tags0 = new Set(m.tags), bn0 = m.banner, T0 = me.brambleTally ? Object.assign({}, me.brambleTally) : null;
      const tv0 = new Map(m.tags.map(g => [g, g.val])), nb0 = m.brambles.length;
      V.length = 0; m.step(DT); steps++;
      const Z = me.ultBramble, out = [], T = me.brambleTally;
      if (m.t < FROM) { heldWas = th.brierHeld > 0; greenWas = me.brierGreen; continue; }
      if (!Z0 && Z) out.push("CAST (the blade greens)");
      if (Z0 && !Z) out.push("CLOSE " + (Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive ? "by the clock" : "by a death"));
      if (m.banner && m.banner !== bn0) out.push("BANNER " + m.banner.text + " at " + (Math.hypot(m.banner.bx - me.x, m.banner.by - me.y) < 1 ? "the caster" : "the foe"));
      if (T && T0 && T.planted > T0.planted) out.push("BRAMBLE planted x" + (T.planted - T0.planted) + " (" + m.brambles.length + " standing)");
      else if (T && !T0 && T.planted) out.push("BRAMBLE planted x" + T.planted);
      if (m.brambles.length < nb0 && !(T && T0 && T.planted > T0.planted)) out.push("a bramble goes (" + m.brambles.length + " standing)");
      if (T && T0 && T.snares > T0.snares) out.push("SNARE (pin " + th.pin.toFixed(2) + ")");
      if (T && T0 && T.ticks > T0.ticks) out.push("BITE x" + (T.ticks - T0.ticks) + " (hp " + th.hp.toFixed(1) + ")");
      const held = th.brierHeld > 0;
      if (held && !heldWas) out.push("foe HELD (the shoots)");
      if (!held && heldWas) out.push("hold off");
      heldWas = held;
      if (greenWas > 0 && me.brierGreen === 0) out.push("the green gone");
      greenWas = me.brierGreen;
      for (const g of m.tags) if (!tags0.has(g)) out.push("TAG " + g.key.toUpperCase() + " " + g.val + (g.first ? " (panel)" : ""));
      for (const g of m.tags) if (tags0.has(g) && tv0.get(g) !== g.val) out.push("TAG counts " + g.key.toUpperCase() + " " + g.val);
      if (V.length) out.push("voices: " + V.join(", "));
      if (out.length) ev.push([+m.t.toFixed(3), out.join("; ")]);
    }
  } finally { AC.SFX.play = oPlay; }
  return { ev, end: { t: +m.t.toFixed(4), over: m.over, hp: [+me.hp.toFixed(2), +th.hp.toFixed(2)], clanks: m.clankCount,
                      brambles: m.brambles.length, green: +me.brierGreen.toFixed(3), held: th.brierHeld } };
}"""
with game(game_path=GAME) as (page, errors):
    R = page.evaluate(JS, [FOE, SEED, FROM, END])
    assert not errors, errors
print(f"Thornwake v {FOE}, seed {SEED}, {GAME.name}: every stage-6 event from {FROM} to {END} (match time)")
for t, e in R["ev"]:
    print(f"  {t:8.3f}  {e}")
print("end:", R["end"])
