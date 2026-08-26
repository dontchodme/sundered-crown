#!/usr/bin/env python3
"""Photograph the STAGE CROSSING, which is the one thing a static hp value
cannot show. The flash is derived from hpGhost being above a threshold the real
hp has already fallen below, so the way to photograph it is to set exactly that
and draw -- no timers to wind forward, which is the point of holding no state."""
import base64, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
from scpage import game

JS = r"""
([hp, ghost]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const m = window.__m || (window.__m = (() => {
    const mm = new AC.Match('axiom','nightfell', 20260816);
    mm.introT = 0; AC.__inject(mm);
    AC.SFX.play=function(){}; AC.SFX.resume=function(){};
    while (mm.t < 7) mm.step(AC.CONFIG.physics.dt);
    return mm;
  })());
  m.shake = 0; m.hitStop = 0; m.banner = null;
  const f = m.a;
  f.status = {}; f.ringFlash = 0; f.mend = 0; f.stun = 0; f.flash = 0;
  f.x = 150; f.y = 250; f.vx = 0; f.vy = 0;
  f.hp = hp; f.hpGhost = ghost;
  m.b.status = {}; m.b.x = 372; m.b.y = 566; m.b.vx = 0; m.b.vy = 0;
  AC.__draw(m);
  const cv = document.getElementById('cv'), r = AC.renderer;
  return { png: cv.toDataURL('image/png').slice(22),
           x: Math.round(r.pad + f.x * r.scale),
           y: Math.round(r.arenaTop + f.y * r.scale) };
}
"""
# hp, ghost, label. Quarter boundaries: 225 / 150 / 75 HP; BRINK at 30.
CASES = [(240, 240, "before  240"),
         (222, 240, "CROSSING 3/4"),
         (165, 165, "after   165"),
         (144, 168, "CROSSING 1/2"),
         ( 69,  90, "CROSSING 1/4 = desperation"),
         ( 27,  44, "BRINK  0.10"),
         ( 22,  22, "one hit  22")]
tiles = []
with game(game_path=pathlib.Path("../02-chain/sc-health.html").resolve()) as (pg, errs):
    for hp, gh, lab in CASES:
        r = pg.evaluate(JS, [hp, gh])
        pathlib.Path("_s.png").write_bytes(base64.b64decode(r["png"]))
        tiles.append((lab, Image.open("_s.png").convert("RGB"), r["x"], r["y"]))
    if errs: print("PAGE ERRORS:", *errs[:5], sep="\n  "); sys.exit(1)

S, MAG = 250, 2
sheet = Image.new("RGB", (len(tiles)*(S*MAG+10), S*MAG+40), (8,6,12))
d = ImageDraw.Draw(sheet)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
for i,(lab,im,x,y) in enumerate(tiles):
    c = im.crop((x-S//2, y-S//2, x+S//2, y+S//2)).resize((S*MAG,S*MAG), Image.NEAREST)
    sheet.paste(c, (i*(S*MAG+10), 0))
    d.text((i*(S*MAG+10)+6, S*MAG+12), lab, font=fnt, fill=(226,216,196))
sheet.save("stage-sheet.png"); print("stage-sheet.png", sheet.size)
