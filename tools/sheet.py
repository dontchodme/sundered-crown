"""Contact sheet at 1:1. Rule 7: you cannot judge legibility from a statistic.

Statuses are applied through f.apply() — the real API — at the ball's real
position after a real match has been stepped. Nothing is teleported and no
clock is set by hand, which is what the harness traps in the resume doc are
about."""
import base64, pathlib
from scpage import game
from PIL import Image

JS = r"""([key, n]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const m = window.__sheetM || (window.__sheetM = (() => {
    const mm = new AC.Match('grudgebearer','thornwake', 4242);
    mm.introT = 0; AC.__inject(mm);
    AC.SFX.play=function(){}; AC.SFX.resume=function(){};
    const dt = AC.CONFIG.physics.dt;
    while (mm.t < 9) mm.step(dt);
    mm.shake = 0;
    return mm;
  })());
  const f = m.a;
  f.status = {};                       // clear whatever the fight applied
  if (key) f.apply(key, n);
  m.shake = 0;
  AC.__draw(m);
  const cv = document.getElementById('cv');
  const r = AC.renderer;
  // device coords of the ball
  const dx = r.pad + f.x * r.scale, dy = r.arenaTop + f.y * r.scale;
  return { png: cv.toDataURL('image/png').slice(22), x: Math.round(dx), y: Math.round(dy) };
}"""

CASES = [("none", 0), ("smite", 3), ("hemorrhage", 4), ("sunder", 4),
         ("entangle", 3), ("curse", 5), ("hex", 3)]
S = 440
tiles = []
with game() as (pg, errs):
    for key, n in CASES:
        r = pg.evaluate(JS, [key or None, n])
        pathlib.Path("_t.png").write_bytes(base64.b64decode(r["png"]))
        im = Image.open("_t.png").convert("RGB")
        x, y = r["x"], r["y"]
        box = (max(0, x-S//2), max(0, y-S//2), min(1080, x+S//2), min(1920, y+S//2))
        tiles.append((key, im.crop(box).resize((S, S))))
    assert not errs, errs

from PIL import ImageDraw
cols, rows = 4, 2
sheet = Image.new("RGB", (cols*S, rows*(S+30)), (10, 8, 14))
d = ImageDraw.Draw(sheet)
for i, (name, t) in enumerate(tiles):
    cx, cy = (i % cols) * S, (i // cols) * (S + 30)
    sheet.paste(t, (cx, cy))
    d.text((cx + 8, cy + S + 8), name.upper(), fill=(233, 213, 168))
sheet.save("status-sheet.png")
print("status-sheet.png", sheet.size)
