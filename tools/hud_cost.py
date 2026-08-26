#!/usr/bin/env python3
"""RELATIVE draw cost, shipped build vs the health build.

This container has no GPU and its rasterisers disagree by ~10x with real
hardware, so no number here is Rick's machine and none is a phone. What IS
transferable is the RATIO between two builds measured back to back through the
same harness in the same session -- which is the only question this patch has
to answer: did the new HUD make the frame materially more expensive?

Per RESUME-HERE §5: force the raster, and do N draws inside ONE rAF rather
than a getImageData every frame, which can demote an accelerated canvas to
software and turn the instrument into the result.
"""
import argparse, pathlib, statistics
from scpage import game

JS = r"""
([ida, idb, seed, warm, n]) => {
  AC.setResolution(1080, 1920);
  const m = new AC.Match(ida, idb, seed); m.introT = 0; AC.__inject(m);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const dt = AC.CONFIG.physics.dt;
  while (m.t < 22) m.step(dt);          // seals up, statuses live, cracks grown
  m.shake = 0;                           // Math.random() in the camera offset
  const cv = document.getElementById('cv'), ctx = cv.getContext('2d');
  for (let i = 0; i < warm; i++) AC.__draw(m);
  return new Promise(res => requestAnimationFrame(() => {
    const t0 = performance.now();
    for (let i = 0; i < n; i++) AC.__draw(m);
    ctx.getImageData(0, 0, 1, 1);        // force the raster, once, at the end
    res((performance.now() - t0) / n);
  }));
}
"""

ap = argparse.ArgumentParser()
ap.add_argument("--a", default="../02-chain/sc-cardspin.html")
ap.add_argument("--b", default="../02-chain/sc-health.html")
ap.add_argument("--pairs", default="ironhail:oathwound:1676955306,dawnbringer:censer:2503973695")
ap.add_argument("--n", type=int, default=120)
ap.add_argument("--reps", type=int, default=5)
g = ap.parse_args()

pairs = [p.split(":") for p in g.pairs.split(",")]
res = {}
for tag, path in (("shipped", g.a), ("health", g.b)):
    per = []
    with game(game_path=pathlib.Path(path).resolve()) as (pg, errs):
        for a, b, seed in pairs:
            runs = [pg.evaluate(JS, [a, b, int(seed), 12, g.n]) for _ in range(g.reps)]
            per.append((f"{a}/{b}", statistics.median(runs)))
        assert not errs, errs
    res[tag] = per
    print(f"{tag:<9} " + "  ".join(f"{k} {v:6.2f}ms" for k, v in per))

print()
for i, (k, _) in enumerate(res["shipped"]):
    s, h = res["shipped"][i][1], res["health"][i][1]
    print(f"  {k:<26} {s:6.2f} -> {h:6.2f} ms   {(h/s-1)*100:+5.1f}%")
sm = statistics.mean(v for _, v in res["shipped"])
hm = statistics.mean(v for _, v in res["health"])
print(f"\n  MEAN  {sm:.2f} -> {hm:.2f} ms   {(hm/sm-1)*100:+.1f}%   (ratio only; "
      f"this box has no GPU)")
