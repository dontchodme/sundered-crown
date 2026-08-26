#!/usr/bin/env python3
"""How much of the ACTION leaves the frame during wall-adjacent set-pieces?

The earlier bottom-clip fix kept the FOCUS POINT in frame and its probe checked
exactly that -- which is why it passed while play kept showing cut-off action.
The action is not a point: a relic has a radius that the zoom magnifies, and
the letterbox bars eat the frame edges on top of that. This probe runs real
cuts whose contact sits near a wall, through the REAL path (CINE.pump), and at
every frame measures how far each relic's magnified body extends past the
usable frame (viewport minus the current letterbox). Positive = pixels of
relic body the viewer cannot see.

  python3 cinema_edge_probe.py
"""
from __future__ import annotations
import pathlib, sys
from scpage import game

HERE = pathlib.Path(__file__).parent
JS = r"""
([ids, nseeds, seed0, wallFrac]) => {
  const A = AC.CONFIG.arena, R = AC.CONFIG.relic ? AC.CONFIG.relic.r : 34;
  const rr = (AC.CONFIG.fighter && AC.CONFIG.fighter.r) || R || 34;
  let s = seed0 >>> 0;
  const rows = [];
  for (let k = 0; k < nseeds && rows.length < 8; k++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const i = s % ids.length; let j = (s >>> 8) % ids.length;
    if (j === i) j = (j + 1) % ids.length;
    const p = window.cinePlan(ids[i], ids[j], s); if (p.err) continue;
    const cut = p.cuts.find(c =>
      (c.y > A.h * wallFrac || c.y < A.h * (1 - wallFrac) * 0.2 ||
       c.x > A.w * wallFrac || c.x < A.w * (1 - wallFrac) * 0.2));
    if (!cut) continue;

    CINE.on = true; CINE.interp = true; CINE.reset();
    CINE.plan = p.cuts.slice(); CINE.acc = 0;
    const m = new AC.Match(ids[i], ids[j], s); m.introT = 0;
    const dt = AC.CONFIG.physics.dt, raw = 1 / 60;
    const startAt = (cut.loose ? cut.loose.t : cut.t) - 0.6;
    while (!m.over && m.t < startAt) m.step(dt);

    let worst = { over: -1e9, nearOver: -1e9, farOver: -1e9 };
    let frames = 0, active = false;
    while (!m.over && frames < 3000) {
      const alpha = CINE.pump(raw, m, 1);
      if (CINE.cut) { active = true; } else if (active) break;
      if (!CINE.cut) { frames++; continue; }
      if (alpha > 0) CINE.drawLerped(AC.renderer, m, alpha);
      else AC.__draw(m);
      const rd = AC.renderer, cam = rd._cineCam;
      if (cam) {
        const [px, py, z] = cam;
        const barH = rd.ah * 0.115 * (CINE.bars || 0);
        /* The pass criterion is the NEAR relic -- the action. The far relic is
           reported but tolerated: when both cannot fit at this zoom the design
           abandons the distant one on purpose (the archer the shot just panned
           away from), and flagging that as failure is how the first version of
           this probe sent the fix chasing the wrong relic. */
        for (const f of [m.a, m.b]) {
          const sx = px + (f.x * rd.scale - px) * z;
          const sy = py + (f.y * rd.scale - py) * z;
          const rp = rr * rd.scale * z;
          const over = Math.max(
            (sy + rp) - (rd.ah - barH),      // past the bottom usable edge
            (barH) - (sy - rp),              // past the top usable edge
            (sx + rp) - rd.aw,
            -(sx - rp));
          const dF = Math.hypot(f.x - CINE.fx, f.y - CINE.fy);
          const key = dF <= 220 ? "nearOver" : "farOver";
          if (over > (worst[key] || -1e9)) worst[key] = Math.round(over);
          if (over > (worst.over || -1e9))
            worst = Object.assign(worst, { over: Math.round(over), phase: CINE.phase,
                      z: +z.toFixed(2), bars: +(CINE.bars || 0).toFixed(2),
                      relic: f === m.a ? ids[i] : ids[j],
                      dFocus: Math.round(dF),
                      ranged: !!(CINE.cut && CINE.cut.ranged) });
        }
      }
      frames++;
    }
    rows.push({ a: ids[i], b: ids[j], seed: s,
                cy: Math.round(cut.y), ch: Math.round(A.h), worst });
  }
  return rows;
}
"""

def main() -> int:
    ids = ("dawnbringer,widowmaker,grudgebearer,thornwake,gravemourn,"
           "spellbreaker,ironhail,lightkeeper,farwarden").split(",")
    with game(game_path=(HERE / "sc-cinema.html").resolve()) as (page, err):
        page.evaluate("AC.setResolution(540, 960)")
        rows = page.evaluate(JS, [ids, 160, 0xED6E, 0.78])
        if err: print("page errors", err[:3])
    if not rows:
        print("no wall-adjacent cuts found"); return 1
    print("wall-adjacent set-pieces, relic-body overflow past the USABLE frame")
    print("(viewport minus letterbox; positive px = body the viewer cannot see)\n")
    bad = 0
    for r in rows:
        w = r["worst"]
        # 12px, not 2: the probe measures against restored (un-lerped)
        # positions while the camera was clamped for the lerped positions the
        # frame actually drew -- up to one sim step of skew, ~6px at this
        # resolution. Below that is the probe's own error bar, not a clip.
        flag = "  ACTION CLIPPED" if w.get("nearOver", -9999) > 12 else ""
        print(f"  {r['a']} v {r['b']} seed {r['seed']}: contact y={r['cy']}/{r['ch']}"
              f"  worst {w['over']:+4}px in {w['phase']} (z {w['z']}, bars {w['bars']},"
              f" relic {w['relic']} {w['dFocus']}su from focus,"
              f" {'ranged' if w.get('ranged') else 'melee'})"
              f"  near {w.get('nearOver',-9999):+}px / far {w.get('farOver',-9999):+}px{flag}")
        if w.get("nearOver", -9999) > 12: bad += 1
    print(f"\n  {bad}/{len(rows)} wall cuts clip the ACTION (near-relic body)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
