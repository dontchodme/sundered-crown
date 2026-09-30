"""Frames for the contact sheet's strips, off one real Goreshard fight (1080x1920, chain on, shake zeroed,
Math.random pinned): the cast (goreAge 0.02..1.0, half-seconds: the red's run from the guard to the point, the
first frames inside the cast's own stop), the GLOW LADDER (one settled window frame redrawn with goreGlow at
0.2 / 0.35 / 0.5 / 0.65 / 0.8, the design's alpha for 0..4 stacks) and the live window at the foe's 0 / 2 / 4
stacks, a priced blow (+0/+6/+14 steps: the larger float) and an unpriced one for scale, the drain (goreOut
0.05..0.65). Crops of 600 px round the blade's middle (the blows round the foe). And the HUD sigil (ULTSIG) at
charge 0 / 0.35 / 0.7 / 1.0, drawn alone at r 90 on its own canvas.
usage: gs_look.py page foe seed side tag [castN]. SCRATCH."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
FOE, SEED, SIDE, TAG = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
CASTN = int(sys.argv[6]) if len(sys.argv) > 6 else 1
OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
JS = r"""([foe, seed, side, castN]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const r = AC.renderer, DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv"), RB = AC.CONFIG.physics.ballR;
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const out = {};
  const mid = () => { const L = me.w.reach * m.actMods.reach * me.reachMul + 6, rr = RB - 6 + L * 0.55;
    return toDev(me.x + Math.cos(me.theta) * rr, me.y + Math.sin(me.theta) * rr); };
  const snap = (k, at, glow) => { if (out[k]) return; const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    const g0 = me.goreGlow; if (glow != null) me.goreGlow = glow;
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks; me.goreGlow = g0; }
    out[k] = { png: cv.toDataURL("image/png"), t: +m.t.toFixed(3), age: +(me.goreAge || 0).toFixed(3), out: +(me.goreOut || 0).toFixed(3),
               glow: glow != null ? glow : +(me.goreGlow || 0).toFixed(3), stop: +m.hitStop.toFixed(3), at: at || mid(),
               stk: th.stacks("hemorrhage"), drops: (me.goreDrops || []).length,
               floats: m.floats.map(f => [f.text, +f.size.toFixed(1)]), T: me.priceTally ? Object.assign({}, me.priceTally) : null }; };
  const AGES = [0.02, 0.06, 0.12, 0.2, 0.3, 0.45, 0.6, 1.0], OUTS = [0.05, 0.15, 0.28, 0.4, 0.52, 0.66];
  let step = 0, prev = null, casts = 0, sB = 0, sS = 0, blowAt = -1, blowN = 0, zeroAt = -1, closing = false, ladder = false;
  const PIC = typeof me.goreAge === "number";           // the base page: the sigil only
  while (PIC && step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultPrice, T = me.priceTally;
    if (Z && !prev) casts++;
    if (!Z && prev && me.alive && th.alive && casts === castN) closing = true;
    prev = Z;
    let nb = 0, ns = 0;
    if (T){ nb = T.blows - sB; ns = T.stk - sS; sB = T.blows; sS = T.stk; }
    if (casts === castN && Z) AGES.forEach((a, i) => { if (!out["cast" + i] && me.goreAge >= a) snap("cast" + i); });
    const sk = th.stacks("hemorrhage"), clean = m.hitStop <= 0 && th.alive;
    const d = Math.hypot(th.x - me.x, th.y - me.y);
    if (Z && Z.t > 1 && clean && !ladder && d > 190 && d < 330){
      ladder = true;
      [0.2, 0.35, 0.5, 0.65, 0.8].forEach((g, i) => snap("lad" + i, null, g));
    }
    if (Z && Z.t > 0.8 && clean && d < 330){
      if (sk === 0 && me.goreGlow < 0.21) snap("live0");
      if (sk === 2 && Math.abs(me.goreGlow - 0.5) < 0.01) snap("live2");
      if (sk >= 4 && me.goreGlow > 0.79) snap("live4");
    }
    if (nb > 0 && ns > 0 && blowAt < 0 && th.alive){ blowAt = step; blowN = ns; out.blowSpot = toDev(th.x, th.y); out.blowN = ns; }
    if (blowAt >= 0) [0, 6, 14].forEach((dd, i) => { if (step === blowAt + dd) snap("blow" + i, out.blowSpot); });
    if (nb > 0 && ns === 0 && Z && zeroAt < 0 && th.alive){ zeroAt = step; out.zeroSpot = toDev(th.x, th.y); }
    if (zeroAt >= 0 && step === zeroAt + 6) snap("zero1", out.zeroSpot);
    if (closing && !Z) OUTS.forEach((o, i) => { if (!out["drain" + i] && me.goreOut >= o) snap("drain" + i); });
    if (!Z && !(me.goreFade > 0)) closing = false;
    const need = ["cast7", "lad4", "live0", "live2", "live4", "blow2", "zero1", "drain5"];
    if (need.every(k => out[k]) || (m.t > 90 && ["cast7", "lad4", "blow2", "drain5"].every(k => out[k]))) break;
  }
  /* THE HUD SIGIL, alone: _ultSigil on its own canvas at r 90 */
  const sc = document.createElement("canvas"); sc.width = 820; sc.height = 220;
  const c2 = sc.getContext("2d"); c2.fillStyle = "#07050C"; c2.fillRect(0, 0, 820, 220);
  const oc = r.ctx; r.ctx = c2;
  try { [0, 0.35, 0.7, 1.0].forEach((cf, i) => r._ultSigil(m, me, 110 + i * 200, 110, 90, cf, cf >= 1)); }
  finally { r.ctx = oc; }
  out.sigil = { png: sc.toDataURL("image/png") };
  out.casts = casts; out.t = m.t;
  return out;
}"""
if __name__ == "__main__":
    with game(game_path=PAGE) as (page, errors):
        r = page.evaluate(JS, [FOE, SEED, SIDE, CASTN])
        assert not errors, errors[:5]
    meta = {}
    for k, v in r.items():
        if isinstance(v, dict) and "png" in v:
            im = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
            if k == "sigil":
                im.save(OUTD / f"look_{TAG}_sigil.png"); continue
            cx, cy = v["at"]
            W = 600
            box = (int(max(0, min(im.width - W, cx - W / 2))), int(max(0, min(im.height - W, cy - W / 2))))
            im.crop(box + (box[0] + W, box[1] + W)).save(OUTD / f"look_{TAG}_{k}.png")
            meta[k] = v
            print(k, json.dumps(v))
        else:
            print(k, v)
            meta[k] = v
    (OUTD / f"look_{TAG}.json").write_text(json.dumps(meta, indent=1))
