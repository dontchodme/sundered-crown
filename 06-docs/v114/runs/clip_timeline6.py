"""v114 scratch: the clip's fight, headless, event by event inside [t0, t1] of match time -- what the clip shows
and plays, read where it happens (the voices through AC.SFX.play, a no-op headless; the picture's fields after
each step; the float sizes through the match's float()). Nothing here moves the fight.
    python clip_timeline6.py <link> <foe> <seed> <t0> <t1>"""
import json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

link, foe, seed, t0, t1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
JS = r"""([foe, seed, t0, t1]) => {
  const DT = AC.CONFIG.physics.dt, m = new AC.Match("oathwound", foe, seed), me = m.a, th = m.b;
  const ev = []; let V = [], F = [];
  const oPlay = AC.SFX.play, own = Object.prototype.hasOwnProperty.call(AC.SFX, "play");
  AC.SFX.play = function(kind, q){ V.push([kind, q ? Object.assign({}, q) : q]); return oPlay.call(this, kind, q); };
  const oFloat = m.float; m.float = function(x, y, text, c, size){ F.push([String(text), size]); return oFloat.call(this, x, y, text, c, size); };
  let prevZ = null, prevFade = 0, lv = {}, frames = 0, stops = 0, drops = 0;
  try {
    while (!m.over && m.t < t1 + 3){
      V = []; F = [];
      const h0 = me.hits, T0 = me.priceTally ? me.priceTally.stk : 0, d0 = me.dealt, Z0 = me.ultPrice;
      m.step(DT);
      const inClip = m.t >= t0 && m.t <= t1;
      const Z = me.ultPrice;
      if (inClip){
        for (const [k, q] of V){
          if (k === "ult" && q && q.w === "oathwound") ev.push([m.t, "CAST voice (ult/oathwound)"]);
          else if (k === "hit" && q && "price" in q) ev.push([m.t, `PRICED blow voice: price ${q.price}, dmg ${q.dmg}${q.crit ? " crit" : ""}`]);
          else if (k === "hit" && me.hits > h0) ev.push([m.t, `her plain blow voice: dmg ${q.dmg}${q.crit ? " crit" : ""}${Z ? " (window open, n 0)" : ""}`]);
          else if (k === "ult") ev.push([m.t, `other ult voice ${q && q.w}`]);
          else if (k === "death") ev.push([m.t, "death voice"]);
        }
        for (const [t, s] of F) if (me.hits > h0) ev.push([m.t, `  float "${t}" at ${s.toFixed(2)} px`]);
        if (!Z0 && Z) ev.push([m.t, "WINDOW OPENS"]);
        if (Z0 && !Z) ev.push([m.t, `WINDOW CLOSES ${Z0.t + DT >= Z0.dur - 1e-9 && me.alive && th.alive ? "by the clock" : "on a death"}`]);
        if (Z){ frames++; const n = Math.min(4, th.stacks("hemorrhage")); lv[n] = (lv[n] || 0) + 1; if (m.hitStop > 0) stops++; }
        if (prevFade > 0 && me.goreFade === 0) ev.push([m.t, "the red DRAINED (goreFade 0)"]);
        drops = Math.max(drops, me.goreDrops ? me.goreDrops.length : 0);
      }
      prevFade = me.goreFade; prevZ = Z;
    }
  } finally { if (own) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  return { ev, over: m.over ? m.t : null, winner: m.winner ? m.winner.w.name : null, frames, lv, stops, drops };
}"""
with game(game_path=pathlib.Path(link).resolve()) as (page, errors):
    R = page.evaluate(JS, [foe, seed, t0, t1])
    assert not errors, errors[:3]
print(f"Goreshard (side A) v {foe}, seed {seed}, match time {t0:.3f}-{t1:.3f}  ({pathlib.Path(link).name})")
for t, e in R["ev"]:
    print(f"  {t:8.3f}  {e}")
tot = max(1, R["frames"])
print(f"window steps in the clip {R['frames']}: the foe's Hemorrhage 0/2/4 on "
      f"{', '.join(f'{k}: {100*v/tot:.0f}%' for k, v in sorted(R['lv'].items(), key=lambda kv: int(kv[0])))}; "
      f"{R['stops']} in a hit stop; at most {R['drops']} motes in flight")
print(f"the match ends at {R['over']} ({R['winner']})")
