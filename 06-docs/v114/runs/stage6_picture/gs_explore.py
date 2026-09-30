"""PICK THE BLADE'S RED AND THE GLOW'S SPRITE ON MEASUREMENT. On window frames of real fights (the first 6
clean window frames of cast 1 and 2, three fights: a white, a dark and an ordinary foe), the blade is redrawn
with each candidate (steel colour x glow sprite colour/blur), and measured at 540x960, chain on:
  weapon  -- |dL| of the caster's weapon against the frame without it (the blade off the floor)
  rest    -- the same for the REST blade on the same frames (the steel: the bar to keep near)
  ladder  -- |dL| between goreGlow 0.2 and 0.8 on the same frame (the stack readout), and its area
Variants are injected by replacing `_gorePal` / `_goreGlow` on the renderer instance from outside the page.
usage: gs_explore.py page. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
STEELS = ["#C41E36", "#D02A40"]
GLOWS = [("core", 20, "source-over"), ("glow", 20, "source-over"), ("glow", 20, "lighter"), ("glow", 26, "lighter"), ("glow", 32, "lighter")]
FIGHTS = [("aureole", 4101, "a"), ("gravemourn", 99015, "a"), ("spellbreaker", 99015, "a")]
JS = r"""([foe, seed, side, steels, glows]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  const comp = (dw, dh) => { let n = 0, s = 0; for (let i = 0; i < dw.length; i += 4){
      const dl = L(dw, i) - L(dh, i); if (Math.abs(dl) < 0.02) continue; n++; s += Math.abs(dl); }
    return { n, dL: n ? s / n : 0 }; };
  const P0 = Object.getPrototypeOf(r);
  const frame = (opt) => {
    const dw = r.drawWeapon;
    if (opt.noW) r.drawWeapon = function(mm, f){ if (f === me) return; return dw.call(this, mm, f); };
    if (opt.rest) r.drawGoreWeapon = function(){ return false; };
    if (opt.steel) r._gorePal = function(aff){ return Object.assign({}, aff, { steel: opt.steel }); };
    if (opt.glowC){
      r._goreGlow = function(c, f, Lw, Ww, al){
        const col = opt.glowC === "core" ? f.aff.core : opt.glowC === "glow" ? f.aff.glow : opt.glowC;
        const g = AC.__weaponGlow ? AC.__weaponGlow(f.w.shape, Lw, Ww, Object.assign({}, f.aff, { core: col }), f.drawK, opt.blur)
                                  : weaponGlowX(f.w.shape, Lw, Ww, Object.assign({}, f.aff, { core: col }), f.drawK, opt.blur);
        c.save(); c.globalCompositeOperation = opt.comp || "source-over"; c.globalAlpha = Math.max(0, Math.min(1, al)); c.drawImage(g.cv, g.ox, g.oy); c.restore(); };
    }
    const g0 = me.goreGlow; if (opt.glow != null) me.goreGlow = opt.glow;
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks; me.goreGlow = g0; r.drawWeapon = dw;
      delete r.drawGoreWeapon; delete r._gorePal; delete r._goreGlow; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data); };
  /* a local copy of weaponGlow's bake (the page's is a closure-scoped function) */
  const cache = new Map();
  function weaponGlowX(shape, Lw, Ww, pal, k, blur){
    const key = shape + "|" + Math.round(Lw) + "|" + pal.core + "|" + blur;
    if (cache.has(key)) return cache.get(key);
    const PAD = Math.ceil(blur * 1.5) + 4, w = Math.ceil(Lw * 1.15) + PAD * 2, h = Math.ceil(Ww * 3) + PAD * 2;
    const c2 = document.createElement("canvas"); c2.width = w; c2.height = h; const x = c2.getContext("2d");
    const OFF = w + 1000; x.translate(PAD, h / 2); x.shadowColor = pal.core; x.shadowBlur = blur; x.shadowOffsetX = OFF; x.translate(-OFF, 0);
    AC.SHAPES[shape](x, Lw, Ww, pal, k);
    const g = { cv: c2, ox: -PAD, oy: -h / 2 }; cache.set(key, g); return g; }
  const res = [];
  let step = 0, casts = 0, prev = null, got = 0;
  while (step < 200 / DT && got < 12){
    m.step(DT); step++;
    if (m.over) break;
    const Z = me.ultPrice; if (Z && !prev) casts++; prev = Z;
    if (!Z || Z.t < 0.8 || m.hitStop > 0 || !th.alive || step % 40) continue;
    if (Math.hypot(th.x - me.x, th.y - me.y) > 320) continue;
    got++;
    const noW = frame({ noW: 1 });
    const rest = comp(frame({ rest: 1 }), frame({ rest: 1, noW: 1 }));
    const row = { t: +m.t.toFixed(2), stk: th.stacks("hemorrhage"), rest, v: {} };
    for (const st of steels) for (const [gc, bl, cm] of glows){
      const o = { steel: st, glowC: gc, blur: bl, comp: cm };
      const w = comp(frame(o), noW);
      const d28 = comp(frame(Object.assign({ glow: 0.8 }, o)), frame(Object.assign({ glow: 0.2 }, o)));
      row.v[st + "|" + gc + "|" + bl + "|" + cm] = { w: w.dL, wn: w.n, lad: d28.dL, ladn: d28.n };
    }
    res.push(row);
  }
  return res;
}"""
if __name__ == "__main__":
    allr = []
    with game(game_path=PAGE) as (page, errors):
        for foe, seed, side in FIGHTS:
            r = page.evaluate(JS, [foe, seed, side, STEELS, GLOWS])
            assert not errors, errors[:3]
            allr += [dict(x, foe=foe) for x in r]
            print(foe, len(r), "frames", flush=True)
    (HERE / "explore.json").write_text(json.dumps(allr, indent=1))
    med = lambda a: sorted(a)[len(a) // 2]
    print(f"REST blade |dL| med {med([x['rest']['dL'] for x in allr]):.3f} over {len(allr)} frames")
    keys = list(allr[0]["v"].keys())
    for k in keys:
        w = [x["v"][k]["w"] for x in allr]; lad = [x["v"][k]["lad"] for x in allr]; ln = [x["v"][k]["ladn"] for x in allr]
        print(f"  {k:28s} weapon |dL| med {med(w):.3f} (min {min(w):.3f})   ladder 0.2->0.8 |dL| med {med(lad):.3f} px {med(ln)}")
