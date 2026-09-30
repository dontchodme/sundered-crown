"""Frames off one real Goreshard fight on a page, at the key states of Bloodprice's picture:
rest (before the first cast), cast0..cast3 (the cast frame and goreAge ~0.1/0.2/0.3s: the red's run),
win0 / win2 / win4 (the window up, clean, the foe at 0 / 2 / 4 Hemorrhage), blow (the step of a priced blow,
n > 0), blow2 (+8 steps: the float up), stop (a hit stop with the window up), close1..close3 (the drain
+0.05/+0.15/+0.3s after a clock close), over (+0.1s after a kill with the window up).
usage: gs_snap.py page foe seed side [WxH] [hide,comma] [castIndex]. SCRATCH. Saves crops + half frames to snaps/."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
FOE, SEED, SIDE = sys.argv[2], int(sys.argv[3]), sys.argv[4]
RES = [int(v) for v in sys.argv[5].split("x")] if len(sys.argv) > 5 else [1080, 1920]
HIDE = [h for h in (sys.argv[6].split(",") if len(sys.argv) > 6 else []) if h]
CAST = int(sys.argv[7]) if len(sys.argv) > 7 else 1
TAG = f"{PAGE.stem}_{FOE}_{SEED}{SIDE}_{RES[0]}" + ("_no-" + "-".join(HIDE) if HIDE else "") + (f"_c{CAST}" if CAST != 1 else "")
OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
JS = r"""([foe, seed, side, res, hide, castIx]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(res[0], res[1]);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const r = AC.renderer, P = Object.getPrototypeOf(r);
  for (const h of hide) if (P[h]) r[h] = function(){};
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const out = {}; let step = 0, closeT = null, casts = 0, prev = null, pend = [], overT = null, upAtOver = false;
  let seenBl = 0, seenStk = 0;
  const snap = (k, spot, extra) => { const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D); AC.__draw(m);
    Math.random = realRandom; m.shake = ks;
    out[k] = Object.assign({ png: cv.toDataURL("image/png"), t: +m.t.toFixed(3), zt: me.ultPrice ? +me.ultPrice.t.toFixed(3) : null,
               fade: +(me.goreFade || 0).toFixed(3), age: +(me.goreAge || 0).toFixed(3),
               out: +(me.goreOut || 0).toFixed(3), glow: +(me.goreGlow || 0).toFixed(3), drops: (me.goreDrops || []).length,
               stk: th.stacks("hemorrhage"), stop: +m.hitStop.toFixed(3), me: toDev(me.x, me.y), foe: toDev(th.x, th.y), k: r.k * r.scale,
               spot: spot ? toDev(spot[0], spot[1]) : null,
               T: me.priceTally ? Object.assign({}, me.priceTally) : null,
               floats: m.floats.map(f => [f.text, +f.size.toFixed(1)]), over: m.over }, extra || {}); };
  while (step < 200 / DT){
    m.step(DT); step++;
    const Z = me.ultPrice, T = me.priceTally;
    if (m.over){
      if (overT === null){ overT = m.t; upAtOver = me.goreFade > 0; }
      if (upAtOver && !out.over && m.t - overT > 0.1) snap("over");
      if (upAtOver && !out.over2 && m.t - overT > 0.3) snap("over2");
      if (m.t - overT > 0.6) break;
      continue;
    }
    if (Z && !prev) casts++;
    if (!Z && prev && me.alive && th.alive) closeT = m.t;
    const castNow = Z && !prev;
    prev = Z;
    const nb = T ? T.blows - seenBl : 0, ns = T ? T.stk - seenStk : 0;
    if (T){ seenBl = T.blows; seenStk = T.stk; }
    for (const p of pend) p.n--;
    const due = pend.filter(p => p.n <= 0); pend = pend.filter(p => p.n > 0);
    for (const p of due) if (!out[p.k]) snap(p.k, p.spot, p.extra);
    const clean = m.hitStop <= 0;
    const near = Math.hypot(th.x - me.x, th.y - me.y) < 260;
    if (!out.rest && !Z && casts === 0 && m.t > 3 && clean && near) snap("rest");
    if (casts === castIx){
      if (!out.cast0 && castNow) snap("cast0");
      if (!out.cast1 && Z && me.goreAge > 0.18 && me.goreAge < 0.24) snap("cast1");
      if (!out.cast2 && Z && me.goreAge > 0.38 && me.goreAge < 0.44) snap("cast2");
      if (!out.cast3 && Z && me.goreAge > 0.62 && me.goreAge < 0.7) snap("cast3");
    }
    const sk = th.stacks("hemorrhage");
    if (Z && Z.t > 0.6 && clean && near){
      if (!out.win0 && sk === 0) snap("win0");
      if (!out.win2 && sk === 2 && Math.abs(me.goreGlow - 0.5) < 0.03) snap("win2");
      if (!out.win4 && sk >= 4 && me.goreGlow > 0.77) snap("win4");
    }
    if (nb > 0 && ns > 0 && !out.blow){ snap("blow", [th.x, th.y], { n: ns }); pend.push({ k: "blow2", n: 8, spot: [th.x, th.y], extra: { n: ns } }); }
    if (nb > 0 && ns === 0 && !out.blow0 && Z){ snap("blow0", [th.x, th.y], { n: 0 }); pend.push({ k: "blow0b", n: 8, spot: [th.x, th.y], extra: { n: 0 } }); }
    if (!out.stop && Z && m.hitStop > 0 && Z.t > 0.5) snap("stop");
    if (!out.close1 && !Z && closeT !== null && m.t - closeT > 0.04 && m.t - closeT < 0.06) snap("close1");
    if (!out.close2 && !Z && closeT !== null && m.t - closeT > 0.14 && m.t - closeT < 0.16) snap("close2");
    if (!out.close3 && !Z && closeT !== null && m.t - closeT > 0.29 && m.t - closeT < 0.31) snap("close3");
  }
  out.casts = casts; out.t = m.t; out.over = m.over; out.T = me.priceTally;
  return out;
}"""
if __name__ == "__main__":
    with game(game_path=PAGE) as (page, errors):
        r = page.evaluate(JS, [FOE, SEED, SIDE, RES, HIDE, CAST])
        assert not errors, errors[:5]
    S = RES[0] / 1080
    for k, v in r.items():
        if isinstance(v, dict) and "png" in v:
            im = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
            cx, cy = v["me"]
            W = int(640 * S)
            box = (int(max(0, min(im.width - W, cx - W / 2))), int(max(0, min(im.height - W, cy - W / 2))))
            im.crop(box + (box[0] + W, box[1] + W)).save(OUTD / f"{TAG}_{k}.png")
            im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(OUTD / f"{TAG}_{k}_frame.png")
            print(k, json.dumps(v))
        else:
            print(k, v)
