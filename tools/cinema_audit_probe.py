"""Exercise the audit fixes directly: Force, late-fire, volley-swallow, reset."""
import pathlib
from scpage import game
JS = r"""
() => {
  const out = {};
  // 1. FORCE: begin() handed a raw beat must synthesize .beats, not crash.
  try {
    const m = new AC.Match("gravemourn","dawnbringer", 12345); m.introT = 0;
    const dt = AC.CONFIG.physics.dt;
    while (m.beats.length < 1 && m.t < 20) m.step(dt);
    CINE.on = true; CINE.reset(); CINE.plan = [];
    CINE.force = 1;
    for (let i = 0; i < 240; i++) CINE.pump(1/60, m, 1);   // run the whole cut
    out.force = { ok: true, phase: CINE.phase };
  } catch (e) { out.force = { ok: false, err: String(e) }; }

  // 2. LATE FIRE: a planned cut whose time is already past must be abandoned.
  try {
    const m = new AC.Match("gravemourn","dawnbringer", 777); m.introT = 0;
    const dt = AC.CONFIG.physics.dt;
    while (m.t < 10) m.step(dt);
    CINE.on = true; CINE.reset();
    CINE.plan = [{ t: 5.0, x: 100, y: 100, tier: 3, score: 9, kind: "hit",
                   beats: [{ t: 5.0, x: 100, y: 100 }] }];
    CINE.pump(1/60, m, 1);
    out.late = { fired: !!CINE.cut, done: CINE.plan[0]._done };
  } catch (e) { out.late = { err: String(e) }; }

  // 3. VOLLEY SWALLOW: across many seeds, no single-hit cut may sit inside a
  //    selected volley's span.
  let overlaps = 0, vols = 0, checked = 0, s = 0xA0D17 >>> 0;
  const ids = ["dawnbringer","widowmaker","grudgebearer","thornwake",
               "gravemourn","spellbreaker","ironhail","lightkeeper","farwarden"];
  for (let k = 0; k < 80; k++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const i = s % ids.length; let j = (s >>> 8) % ids.length;
    if (j === i) j = (j + 1) % ids.length;
    const p = window.cinePlan(ids[i], ids[j], s); if (p.err) continue;
    checked++;
    for (const v of p.cuts) if (v.kind === "volley") {
      vols++;
      for (const c of p.cuts)
        if (c !== v && c.kind !== "volley"
            && c.t >= v.t - 0.01 && c.t <= v.t + v.span + 0.01) overlaps++;
    }
  }
  out.swallow = { checked, volleys: vols, overlaps };

  // 4. RESET zeroes the accumulator.
  CINE.acc = 0.5; CINE.reset();
  out.reset = { acc: CINE.acc };
  return out;
}
"""
with game(game_path=pathlib.Path(__file__).parent.joinpath("sc-cinema.html").resolve()) as (page, err):
    page.evaluate("AC.setResolution(360,640)")
    r = page.evaluate(JS)
    print("1. force        ", r["force"])
    print("2. late-fire    ", r["late"], " (want fired: false, done: true)")
    print("3. volley-swallow", r["swallow"], " (want overlaps: 0)")
    print("4. reset acc    ", r["reset"], " (want acc: 0)")
    if err: print("page errors", err[:4])
