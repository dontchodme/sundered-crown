"""render_ab, the rows' way: the same fights drawn on the base link (sc-lodestone-b205.html) and on ld-final.html
(the rows) at fixed match times, 540x960, chain on, shake zeroed, Math.random pinned per frame; pixels compared.
The other relics' pairs must be pixel-identical -- the six other warhammers (Grudgebearer, Censer, Bulwarden,
Shroudmaul, Ravelbone, Ironwood: the head's route is runic's alone), the four other runic relics (Spellbreaker,
Axiom, Foregone, Paradox: they hex, and the wall tags are Lodestone's alone), the last pictures on the chain
(Bindweed, Portcullis, Morningstar, Dawnbringer) among them; THE CONTROLS (Lodestone inside its window, both
sides) must not. SCRATCH."""
import sys, json, base64, io, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image, ImageChops
HERE = pathlib.Path(__file__).parent
PAGES = {"base": (HERE.parent / "links" / "sc-lodestone-b205.html").resolve(), "final": (HERE / "ld-final.html").resolve()}
PAIRS = [("grudgebearer", "spellbreaker", 31337), ("censer", "axiom", 4101), ("bulwarden", "foregone", 2207),
         ("shroudmaul", "paradox", 7719), ("ravelbone", "ironwood", 1234), ("paradox", "heartwood", 90210),
         ("bindweed", "spellbreaker", 4242), ("portcullis", "axiom", 5150), ("morningstar", "dawnbringer", 99001)]
CTRL = [("lodestone", "spellbreaker", 99015), ("gravemourn", "lodestone", 5150)]
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
    out.push({ t: +m.t.toFixed(3), png: cv.toDataURL("image/png"), lit: [m.a, m.b].some(f => f.ultRunes) });
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
    print(f"{'CONTROL ' if ctrl else ''}{a}:{b} {s}: {n}/{len(same)} pixel-identical  (walls lit at {[f['lit'] for f in res[('final', a, b, s)]]})")
print(f"OTHER RELICS: {ok}/{tot} pixel-identical")
