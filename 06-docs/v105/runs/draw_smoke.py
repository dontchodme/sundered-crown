"""Scratch: draw an Oracle link's fights through the renderer (AC.__draw) and
report throws and any sim write a draw makes. Presentation smoke test for
stages 1-5 (the relic has no picture of its own yet; kind "sight" must fall
through every renderer table without throwing)."""
import argparse, json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
ap = argparse.ArgumentParser(); ap.add_argument("--game", required=True)
ap.add_argument("--foes", default="ironhail,paradox,twinshade,bulwarden,farwarden,gravemourn")
ap.add_argument("--seed", type=int, default=105777); a = ap.parse_args()
JS = r"""([foes, seed]) => {
  window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false;
  const DT = AC.CONFIG.physics.dt; const out = { fights: 0, draws: 0, winDraws: 0, throws: [], writes: 0, casts: 0 };
  const snap = (m) => JSON.stringify([m.t, m.hitStop, m.over, m.a.x, m.a.y, m.a.vx, m.a.vy, m.a.hp, m.a.theta, m.a.charge,
                                      m.b.x, m.b.y, m.b.vx, m.b.vy, m.b.hp, m.b.theta, m.b.charge, m.shots.length]);
  for (const side of [0, 1]) for (const fid of foes){
    const m = side ? new AC.Match(fid, "oracle", seed) : new AC.Match("oracle", fid, seed);
    const me = side ? m.b : m.a; let steps = 0;
    while (!m.over && steps < 160 / DT){
      m.step(DT); steps++;
      const win = !!me.ultSight;
      if (win || steps % 30 === 0){
        const s0 = snap(m);
        try { AC.__draw(m); out.draws++; if (win) out.winDraws++; } catch (e){ out.throws.push(String(e && e.stack || e).slice(0, 300)); }
        if (snap(m) !== s0) out.writes++;
      }
    }
    out.fights++; out.casts += me.ultsFired;
  }
  return out;
}"""
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    r = page.evaluate(JS, [a.foes.split(","), a.seed])
    print(json.dumps(r)[:1500]); print("page errors:", errors[:3])
