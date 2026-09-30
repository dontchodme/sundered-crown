"""render_ab, the rows' way: the same fights drawn on the base link (sc-thornwake-b26.5.html, the freeze's picture and
its SPECS field still in) and on tw-final-fx.html (the delivered look) at fixed match times, 540x960, chain on, shake
zeroed, Math.random pinned per frame; pixels compared. The other relics' pairs must be pixel-identical -- the other
scythes (drawWeapon's new hook is one comparison for them), the other verdant relics (the ENTANGLE tags), Heartwood
(the other freeze, on the ultFx life line the rows cut a token from), Emberedge (on the onTarget line the rows cut a
token from), Vinesower (the SPECS entry above the one the carry cuts), the pinners whose held ball draws Paradox's
hexagon (Paradox, Gloamwire, Ravelbone: `_drawField` gains a return for a ball Bramblesnare holds), the pictures
already on this base (Canopy, Zenith, Daybreak, Corollary) and a shade-maker; THE CONTROLS (Thornwake inside its
window, both sides) must not. SCRATCH."""
import sys, json, base64, io, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
from scpage import game
from PIL import Image, ImageChops
HERE = pathlib.Path(__file__).parent
PAGES = {"base": (HERE.parent / "links" / "sc-thornwake-b26.5.html").resolve(), "final": (HERE / "tw-final-fx.html").resolve()}
PAIRS = [("lastlight", "foregone", 7719), ("bloodmirror", "duskreave", 4242), ("vesper", "cindercleave", 2317),
         ("heartwood", "paradox", 2207), ("emberedge", "axiom", 4101), ("vinesower", "ironwood", 1234),
         ("gloamwire", "thornshear", 99015), ("ravelbone", "bindweed", 5150), ("morningstar", "dawnbringer", 99001),
         ("twinshade", "grudgebearer", 5150), ("spellbreaker", "heartwood", 31337), ("portcullis", "paradox", 8888)]
CTRL = [("thornwake", "aureole", 4101), ("gravemourn", "thornwake", 99015)]
TIMES = [6.0, 15.4, 16.2, 17.0, 19.5, 21.0, 33.0]
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
    out.push({ t: +m.t.toFixed(3), png: cv.toDataURL("image/png"), win: [m.a, m.b].some(f => f.ultBramble), brambles: m.brambles.length,
               pinned: [m.a, m.b].map(f => +(f.pin || 0).toFixed(2)),
               fx: m.ultFx ? m.ultFx.w + ":" + m.ultFx.t.toFixed(2) + "/" + m.ultFx.life : null });
  }
  return out;
}"""
res = {}
for name, page in PAGES.items():
    with game(game_path=page) as (pg, errors):
        for a, b, s in PAIRS + CTRL:
            res[(name, a, b, s)] = pg.evaluate(JS, [a, b, s, TIMES])
            assert not errors, errors[:3]
ok = 0; tot = 0; cok = True
for a, b, s in PAIRS + CTRL:
    same = []
    for fb, ff in zip(res[("base", a, b, s)], res[("final", a, b, s)]):
        ib = Image.open(io.BytesIO(base64.b64decode(fb["png"].split(",", 1)[1]))).convert("RGB")
        iF = Image.open(io.BytesIO(base64.b64decode(ff["png"].split(",", 1)[1]))).convert("RGB")
        same.append(ImageChops.difference(ib, iF).getbbox() is None)
    ctrl = (a, b, s) in CTRL
    n = sum(same)
    if not ctrl: ok += n; tot += len(same)
    else: cok &= n < len(same)
    fin = res[("final", a, b, s)]
    print(f"{'CONTROL ' if ctrl else ''}{a}:{b} {s}: {n}/{len(same)} pixel-identical  (window up {[f['win'] for f in fin]}; "
          f"brambles {[f['brambles'] for f in fin]}; pins {[f['pinned'] for f in fin]}; ultFx {[f['fx'] for f in fin]})")
print(f"OTHER RELICS: {ok}/{tot} pixel-identical; CONTROLS {'differ' if cok else 'DID NOT DIFFER'}")
