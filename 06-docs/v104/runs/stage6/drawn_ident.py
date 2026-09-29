"""v104 stage 6, scratch: DRAWN SIM IDENTITY on the stage-6 link itself (the picture lab's drawn arms ran on
its own page, without the voice rows; the voice lab's on its own, without the picture's). v106's
drawn_ident.py, for Angelus. Each fight is run three times in one page: undrawn (m.step only), drawn the way
the app draws it (AC.__inject, AC.__draw every second step at 540x960, the synth left as it is), and drawn
with a control write -- through the kill and 2 s of the verdict. The state at the kill -- steps, t, the
winner, both fighters' hp, x, y, vx, vy, and Angelus's rise tally -- must be identical drawn. CONTROL: a 1e-9
write to the foe's vx after every draw while the picture is up (ascendFade > 0) must DIFFER.

    python drawn_ident.py <link> [i,j,...]   (optional: only these fights, 0-based, to resume a cut-off run)
"""
import json, pathlib, sys
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
from scpage import game

FIGHTS = [("angelus", "grudgebearer", 2213), ("dawnbringer", "angelus", 4242), ("angelus", "nightfell", 2211),
          ("spellbreaker", "angelus", 99015), ("angelus", "twinshade", 104001), ("ravelbone", "angelus", 5150)]

JS = r"""([a, b, sd]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;            // the page's own loop steps nothing (render_ab's switch)
  AC.setResolution(540, 960);
  const state = (m, steps) => { const me = m.a.w.id === "angelus" ? m.a : m.b, T = me.riseTally;
    return JSON.stringify([steps, m.t, m.winner ? m.winner.w.id : null, m.reason,
      m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, m.a.vx, m.a.vy, m.b.vx, m.b.vy,
      T ? [T.casts, T.shaftHits, T.bless, T.arrivals] : null, !!me.ultRise]); };
  const run = (a, b, sd, mode) => {
    const m = new AC.Match(a, b, sd >>> 0);
    m.introT = 0;
    const me = m.a.w.id === "angelus" ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    if (mode !== "undrawn") AC.__inject(m);
    let steps = 0, draws = 0, thrown = 0, atKill = null, picDraws = 0;
    while (steps < 170 / DT){
      m.step(DT); steps++;
      if (mode !== "undrawn" && steps % 2 === 0){
        m.shake = 0;
        try { AC.__draw(m); draws++; } catch (e){ thrown++; }
        if (me.ascendFade > 0) picDraws++;
        if (mode === "control" && me.ascendFade > 0) foe.vx += 1e-9;
      }
      if (m.over && !atKill) atKill = state(m, steps);
      if (m.over && steps > 0 && (m.deathAge || 0) >= 2) break;
    }
    return { atKill, draws, thrown, picDraws };
  };
  const u = run(a, b, sd, "undrawn"), d = run(a, b, sd, "drawn"), c = run(a, b, sd, "control");
  return { a, b, sd, same: u.atKill === d.atKill, ctlDiffers: u.atKill !== c.atKill, draws: d.draws,
           picDraws: d.picDraws, thrown: d.thrown + c.thrown, kill: u.atKill };
}"""

link = pathlib.Path(sys.argv[1]).resolve()
if len(sys.argv) > 2:                               # resume: run only these fight indices (0-based)
    FIGHTS = [FIGHTS[int(i)] for i in sys.argv[2].split(",")]
R, ok = [], True
print(f"DRAWN SIM IDENTITY on {link.name}: {len(FIGHTS)} fights, each run undrawn, drawn and drawn+control in one page", flush=True)
with game(game_path=link) as (page, errors):
    for fa, fb, fs in FIGHTS:                      # one fight per call, printed as it lands
        r = page.evaluate(JS, [fa, fb, fs]); R.append(r)
        k = json.loads(r["kill"])
        print(f"  {r['a']:>12} v {r['b']:<12} {r['sd']:>7}  drawn {'IDENTICAL' if r['same'] else 'DIFFERS'}  "
              f"({r['draws']} draws, {r['picDraws']} with the picture up, {r['thrown']} thrown)   "
              f"control {'DIFFERS' if r['ctlDiffers'] else 'IDENTICAL (blind!)'}   "
              f"kill at step {k[0]}, winner {k[2]}, rise tally [casts, shaftHits, bless, arrivals] {k[14]}, "
              f"window open at the kill {k[15]}", flush=True)
        ok &= r["same"] and r["ctlDiffers"] and r["thrown"] == 0
    assert not errors, errors[:3]
print(f"\nDRAWN SIM IDENTITY {'PASS' if ok else 'FAIL'}: {sum(r['same'] for r in R)}/{len(R)} identical drawn, "
      f"control differs on {sum(r['ctlDiffers'] for r in R)}/{len(R)}; {sum(r['draws'] for r in R)} draws, "
      f"{sum(r['picDraws'] for r in R)} with the picture up  ({link.name})")
sys.exit(0 if ok else 1)
