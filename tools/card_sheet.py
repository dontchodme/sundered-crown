"""The fight card, rendered. Rick caught Lightkeeper's missing status line by
LOOKING at it, while 13 automated checks stayed green. So look at it."""
import base64, pathlib, scpage, pathlib as _pl
scpage.GAME = _pl.Path(__file__).parent / "sundered-crown-vigil.html"
from scpage import game
from PIL import Image

JS = r"""([a, b]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const m = new AC.Match(a, b, 4242);
  m.introT = AC.CONFIG.intro.dur * 0.5;      // mid-card, fully faded in
  AC.__inject(m); AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  m.shake = 0; AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png').slice(22);
}"""

with game() as (pg, errs):
    png = pg.evaluate(JS, ["dawnbringer", "lightkeeper"])
    pathlib.Path("_c.png").write_bytes(base64.b64decode(png))
    assert not errs, errs
im = Image.open("_c.png").convert("RGB")
im.crop((0, 240, 1080, 1560)).save("card-sheet.png")
print("card-sheet.png")
