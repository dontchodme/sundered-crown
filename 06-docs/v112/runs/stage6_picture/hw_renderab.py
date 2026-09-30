"""render_ab, the rows' way: the same fights drawn on a base and on its rows at fixed match times, 540x960, chain
on, shake zeroed, Math.random pinned per frame; pixels compared. Two pairs of pages: the stamp's (links/sc-heartwood-
b11.html against hw-final-fx.html) and the tip's (carry/hw-on-sc-tendril-fx.html against hw-tip-fx.html, the look as
it ships, with Tendril's root on it). The other relics' pairs must be pixel-identical -- the six other greatswords,
the other verdant relics (Bindweed's own root, which these rows reuse and must not move; Thornwake, whose freeze
shares the life map's note; Ironwood's canopy), Paradox (the hexagon); THE CONTROLS (Heartwood inside its window,
both sides) must not. SCRATCH."""
import sys, json, base64, io, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image, ImageChops
HERE = pathlib.Path(__file__).parent
GROUPS = {"stamp": ((HERE.parent / "links" / "sc-heartwood-b11.html").resolve(), (HERE / "hw-final-fx.html").resolve()),
          "tip": ((HERE / "carry" / "hw-on-sc-tendril-fx.html").resolve(), (HERE / "hw-tip-fx.html").resolve())}
PAIRS = [("lightkeeper", "grudgebearer", 31337), ("dawnbringer", "axiom", 4101), ("oathwound", "emberedge", 2207),
         ("nightfell", "spellbreaker", 1234), ("bindweed", "paradox", 2317), ("thornwake", "gravemourn", 99015),
         ("ironwood", "thornshear", 4242), ("vinesower", "lastlight", 5150), ("paradox", "twinshade", 90210)]
CTRL = [("heartwood", "spellbreaker", 2207), ("gravemourn", "heartwood", 99015)]
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
    out.push({ t: +m.t.toFixed(3), png: cv.toDataURL("image/png"), win: [m.a, m.b].some(f => f.ultRoot) });
  }
  return out;
}"""
total_ok = 0; total = 0; ctrl_ok = True
for g, (base, final) in GROUPS.items():
    res = {}
    for name, page in (("base", base), ("final", final)):
        with game(game_path=page) as (pg, errors):
            for a, b, s in PAIRS + CTRL:
                res[(name, a, b, s)] = pg.evaluate(JS, [a, b, s, TIMES])
                assert not errors, errors[:3]
    print(f"== {g}: {base.name} vs {final.name}")
    for a, b, s in PAIRS + CTRL:
        same = []
        for fb, ff in zip(res[("base", a, b, s)], res[("final", a, b, s)]):
            ib = Image.open(io.BytesIO(base64.b64decode(fb["png"].split(",", 1)[1]))).convert("RGB")
            iF = Image.open(io.BytesIO(base64.b64decode(ff["png"].split(",", 1)[1]))).convert("RGB")
            same.append(ImageChops.difference(ib, iF).getbbox() is None)
        ctrl = (a, b, s) in CTRL
        n = sum(same)
        if ctrl: ctrl_ok &= n < len(same)
        else: total_ok += n; total += len(same)
        print(f"  {'CONTROL ' if ctrl else ''}{a}:{b} {s}: {n}/{len(same)} pixel-identical  (window up at {[f['win'] for f in res[('final', a, b, s)]]})")
print(f"OTHER RELICS: {total_ok}/{total} pixel-identical; CONTROLS {'differ' if ctrl_ok else 'DID NOT DIFFER'}")
