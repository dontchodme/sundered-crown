"""THE BLADE'S GREEN, picked on measurements (Rick: "you pick i overrule"). On real window frames (clean, the
caster in the hall, no hit stop), per gradient variant of `_groveGreen`'s fill (installed on the renderer from
outside; the rest of the method is the delivered one):
  change -- the blade against the resting steel blade (the picture hidden): |dL| and CIE76 dE of the pixels
            that move (|dL| > 0.02 or dE > 2.3)
  floor  -- the caster's weapon against the floor under it (weapon hidden): |dL| of the weapon's pixels,
            with this variant and with the shipped steel blade.
usage: pick_green.py page. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "hw-tip-fx.html"
PAGE = PAGE if PAGE.is_absolute() else HERE / PAGE
VARIANTS = {
    "V0 light (core-glow / core / core-dark .6)": [[0, "mix(P.core, P.glow, 0.35)"], [0.45, "P.core"], [1, "mix(P.core, P.dark, 0.6)"]],
    "V1 deep (core / core-dark .35 / dark)": [[0, "P.core"], [0.45, "mix(P.core, P.dark, 0.35)"], [1, "P.dark"]],
    "V2 lit edge, deep body": [[0, "mix(P.core, P.glow, 0.25)"], [0.3, "P.core"], [0.6, "mix(P.core, P.dark, 0.5)"], [1, "P.dark"]],
    "V3 mid (core / core-dark .2 / core-dark .7)": [[0, "mix(P.core, P.glow, 0.15)"], [0.45, "mix(P.core, P.dark, 0.2)"], [1, "mix(P.core, P.dark, 0.7)"]],
}
JS = r"""([foe, seed, side, variants]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960); AC.SFX.play = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("heartwood", foe, seed) : new AC.Match(foe, "heartwood", seed);
  const me = m.a.w.id === "heartwood" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const mix = AC.mix || window.mix;
  const src = r._groveGreen.toString();
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const realRandom = Math.random;
  function frame(hide, green){
    const saved = [];
    for (const h of hide) { r[h] = function(){}; saved.push(h); }
    if (green){ r._groveGreen = green; saved.push("_groveGreen"); }
    const dw = r.drawWeapon;
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks; for (const h of saved) delete r[h]; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data);
  }
  function noWeapon(green){
    const dw = r.drawWeapon; r.drawWeapon = function(mm, f){ if (f !== me) return dw.call(this, mm, f); };
    try { return frame([], green); } finally { r.drawWeapon = dw; }
  }
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lab = (d, i) => { const R_ = lin(d[i]), G = lin(d[i+1]), B = lin(d[i+2]);
    let X = (0.4124 * R_ + 0.3576 * G + 0.1805 * B) / 0.95047, Y = 0.2126 * R_ + 0.7152 * G + 0.0722 * B, Z = (0.0193 * R_ + 0.1192 * G + 0.9505 * B) / 1.08883;
    const f = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))]; };
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  function comp(a, b){
    let n = 0, s = 0, e = 0;
    for (let i = 0; i < a.length; i += 4){
      if (a[i] === b[i] && a[i+1] === b[i+1] && a[i+2] === b[i+2]) continue;
      const dl = Math.abs(L(a, i) - L(b, i)), la = lab(a, i), lb = lab(b, i);
      const de = Math.hypot(la[0] - lb[0], la[1] - lb[1], la[2] - lb[2]);
      if (dl < 0.02 && de < 2.3) continue;
      n++; s += dl; e += de; }
    return { n, dL: n ? s / n : 0, dE: n ? e / n : 0 };
  }
  const mk = (stops) => { const body = src.replace(/gr\.addColorStop\(0, mix\(P\.core, P\.glow, 0\.35\)\); gr\.addColorStop\(0\.45, P\.core\);\s*gr\.addColorStop\(1, mix\(P\.core, P\.dark, 0\.6\)\);/,
      stops.map(([o, c]) => `gr.addColorStop(${o}, ${c});`).join(" "));
    if (body === src) throw new Error("gradient not found in _groveGreen");
    return eval("(function " + body.replace(/^_groveGreen/, "") + ")"); };
  const out = []; let step = 0, n = 0;
  while (step < 200 / DT && !m.over && n < 3){
    m.step(DT); step++;
    const Z = me.ultRoot;
    if (!(Z && Z.t > 1.5 + n * 2 && m.hitStop <= 0 && me.x > 120 && me.x < A.w - 120 && me.y > 120 && me.y < A.h - 120
          && Math.hypot(th.x - me.x, th.y - me.y) > 260 && !(me.stun > 0))) continue;
    n++;
    const base = frame(["_groveBlade", "drawGrove", "_twineRoot"]), baseNW = noWeapon(null);
    const rec = { t: +m.t.toFixed(2), baseFloor: comp(base, baseNW), v: {} };
    for (const [name, stops] of Object.entries(variants)){
      const g = mk(stops);
      const on = frame([], g), nw = noWeapon(g);
      rec.v[name] = { change: comp(on, base), floor: comp(on, nw) };
    }
    out.push(rec);
  }
  return out;
}"""
FIGHTS = [("grudgebearer", 31337, "b"), ("spellbreaker", 2207, "a"), ("dawnbringer", 99001, "a"), ("gravemourn", 99015, "a")]
if __name__ == "__main__":
    allr = []
    with game(game_path=PAGE) as (page, errors):
        for foe, seed, side in FIGHTS:
            r = page.evaluate(JS, [foe, seed, side, VARIANTS])
            assert not errors, errors[:3]
            allr += r
            print(foe, seed, side, len(r), "frames", flush=True)
    (HERE / "pick_green.json").write_text(json.dumps(allr, indent=1))
    med = lambda xs: sorted(xs)[len(xs) // 2]
    print(f"\n{len(allr)} window frames. The shipped steel blade against the floor: |dL| med {med([x['baseFloor']['dL'] for x in allr]):.3f} "
          f"(n med {med([x['baseFloor']['n'] for x in allr])})")
    for name in VARIANTS:
        ch = [x["v"][name]["change"] for x in allr]; fl = [x["v"][name]["floor"] for x in allr]
        print(f"  {name:44s} change |dL| med {med([c['dL'] for c in ch]):.3f} dE med {med([c['dE'] for c in ch]):5.1f} (n med {med([c['n'] for c in ch])}) "
              f"| blade vs floor |dL| med {med([c['dL'] for c in fl]):.3f} dE med {med([c['dE'] for c in fl]):5.1f}")
