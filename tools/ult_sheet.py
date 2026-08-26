#!/usr/bin/env python3
"""Every relic's ult block, at three charge levels. Rule 9 says each relic gets
its own; this is the instrument that proves seventeen distinct pictures exist
rather than one picture wearing seventeen palettes."""
import argparse, base64, pathlib, re, sys
from PIL import Image, ImageDraw, ImageFont
from scpage import game

JS = r"""
([ida, idb, fracs]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const mm = new AC.Match(ida, idb, 20260817);
  mm.introT = 0; AC.__inject(mm);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  while (mm.t < 5) mm.step(AC.CONFIG.physics.dt);
  mm.shake = 0; mm.hitStop = 0; mm.banner = null;
  const cv = document.getElementById('cv'), out = [];
  const W = 540, H = 104;
  const tile = document.createElement('canvas'); tile.width=W; tile.height=H;
  const tx = tile.getContext('2d');
  for (const fr of fracs){
    mm.a.charge = mm.a.w.ult.charge * fr;
    mm.b.charge = mm.b.w.ult.charge * 0.2;
    AC.__draw(mm);
    tx.clearRect(0,0,W,H); tx.drawImage(cv, 0, 0, W, H, 0, 0, W, H);
    out.push(tile.toDataURL('image/png').slice(22));
  }
  return { tiles: out, name: mm.a.w.name, ult: mm.a.w.ult.name };
}
"""

PREFLIGHT = r"""
() => {
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const P = AC.AFFINITIES.runic, bad = [];
  for (const id of Object.keys(ULTSIG))
    for (const cf of [0, 0.5, 1]){
      c.save(); c.translate(60, 60); c.scale(24, 24);
      try { ULTSIG[id](c, 3.7, cf, P); }
      catch (e){ bad.push(id + " cf=" + cf + " :: " + e.message); }
      c.restore();
    }
  return { n: Object.keys(ULTSIG).length, bad };
}
"""

ap = argparse.ArgumentParser()
ap.add_argument("--src", default="../02-chain/sc-health.html")
ap.add_argument("--out", default="ult-sheet.png")
ap.add_argument("--fracs", default="0.15,0.62,0.97")
g = ap.parse_args()
FR = [float(v) for v in g.fracs.split(",")]
src = pathlib.Path(g.src).resolve()
ids = []
for m in re.finditer(r'\{ id:"([a-z]+)"', src.read_text(encoding="utf-8")):
    if m.group(1) not in ids: ids.append(m.group(1))

rows = []
with game(game_path=src) as (pg, errs):
    # Exercise every sigil directly first. A sigil that throws otherwise
    # surfaces as a stack trace inside __draw with no relic name attached, and
    # the sheet stops at whichever fight happened to reach it.
    pf = pg.evaluate(PREFLIGHT)
    if pf["bad"]:
        print(f"! {len(pf['bad'])} sigil failures:", *pf["bad"], sep="\n    "); sys.exit(1)
    print(f"  preflight: {pf['n']} sigils, all draw at cf 0 / 0.5 / 1")
    for i, rid in enumerate(ids):
        r = pg.evaluate(JS, [rid, ids[(i+1) % len(ids)], FR])
        ims = []
        for b64 in r["tiles"]:
            pathlib.Path("_u.png").write_bytes(base64.b64decode(b64))
            ims.append(Image.open("_u.png").convert("RGB"))
        rows.append((r["name"], r["ult"], ims)); print(f"  {r['name']:<14} {r['ult']}")
    if errs: print("PAGE ERRORS:", *errs[:6], sep="\n  "); sys.exit(1)

F = lambda s,b=False: ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""), s)
W,H = 540,104
COLS = 2
blocks=[rows[i:i+ (len(rows)+COLS-1)//COLS] for i in range(0,len(rows),(len(rows)+COLS-1)//COLS)]
BW = len(FR)*W + 16
sheet = Image.new("RGB",(BW*COLS, 30+max(len(b) for b in blocks)*(H+30)),(8,6,12))
d = ImageDraw.Draw(sheet)
for bi,block in enumerate(blocks):
    ox = bi*BW
    for j,fr in enumerate(FR):
        d.text((ox+8+j*W+W//2, 14), f"charge {int(fr*100)}%", font=F(16,True), fill=(200,190,175), anchor="mm")
    for ri,(name,ult,ims) in enumerate(block):
        y = 30+ri*(H+30)
        for j,im in enumerate(ims): sheet.paste(im,(ox+8+j*W, y))
        d.text((ox+12, y+H+6), f"{name.upper()}  ·  {ult}", font=F(16,True), fill=(226,216,196))
sheet.save(g.out); print(g.out, sheet.size)
