"""render_ab, the rows' way: the same fights drawn on the base link (sc-goreshard-b10.25.html) and on
gs-final-fx.html (the delivered look: the rows + SPECS.oathwound out) at fixed match times, 540x960, chain on,
shake zeroed, Math.random pinned per frame; pixels compared. The other relics' pairs must be pixel-identical --
the five other bloodsworn relics (the school's palette, Hemorrhage and its floats), the six other greatswords
(drawWeapon's hook), the last pictures on the chain (Bindweed, Ironwood, Morningstar, Portcullis) and
Twinshade's shades; THE CONTROLS (Goreshard inside its window, both sides) must not. SCRATCH."""
import sys, json, base64, io, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image, ImageChops
HERE = pathlib.Path(__file__).parent
PAGES = {"base": (HERE.parent / "links" / "sc-goreshard-b10.25.html").resolve(), "final": (HERE / "gs-final-fx.html").resolve()}
PAIRS = [("widowmaker", "redflail", 31337), ("marrowdraw", "ravelbone", 4101), ("bloodmirror", "dawnbringer", 2207),
         ("axiom", "lightkeeper", 7719), ("emberedge", "nightfell", 1234), ("heartwood", "bindweed", 90210),
         ("portcullis", "aureole", 4242), ("twinshade", "widowmaker", 5150), ("morningstar", "ironwood", 99001)]
CTRL = [("oathwound", "aureole", 4101), ("spellbreaker", "oathwound", 99015)]
TIMES = [6.0, 15.4, 17.0, 19.5, 21.0, 33.0]
JS = r"""([a, b, seed, times]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960); AC.SFX.play = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = new AC.Match(a, b, seed), out = [];
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  for (const T of times){
    while (m.t < T && !m.over) m.step(DT);
    const ks = m.shake; m.shake = 0; const rr = Math.random; Math.random = pin(0x5EEDF00D);
    AC.__draw(m); Math.random = rr; m.shake = ks;
    out.push({ t: +m.t.toFixed(3), png: cv.toDataURL("image/png"), wall: [m.a, m.b].some(f => f.ultPrice) });
  }
  return out;
}"""
res = {}
for name, page in PAGES.items():
    with game(game_path=page) as (pg, errors):
        for a, b, s in PAIRS + CTRL:
            res[(name, a, b, s)] = pg.evaluate(JS, [a, b, s, TIMES])
            assert not errors, errors[:3]
ok = 0; tot = 0
for a, b, s in PAIRS + CTRL:
    same = []
    for fb, ff in zip(res[("base", a, b, s)], res[("final", a, b, s)]):
        ib = Image.open(io.BytesIO(base64.b64decode(fb["png"].split(",", 1)[1]))).convert("RGB")
        iF = Image.open(io.BytesIO(base64.b64decode(ff["png"].split(",", 1)[1]))).convert("RGB")
        same.append(ImageChops.difference(ib, iF).getbbox() is None)
    ctrl = (a, b, s) in CTRL
    n = sum(same)
    if not ctrl: ok += n; tot += len(same)
    print(f"{'CONTROL ' if ctrl else ''}{a}:{b} {s}: {n}/{len(same)} pixel-identical  (window up at {[f['wall'] for f in res[('final', a, b, s)]]})")
print(f"OTHER RELICS: {ok}/{tot} pixel-identical")
