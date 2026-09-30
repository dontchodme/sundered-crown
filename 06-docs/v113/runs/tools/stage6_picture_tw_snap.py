"""Frames off one real Thornwake fight on a page, at key states of Bramblesnare's picture:
rest (before the first cast), cast (the cast frame, in its hit stop), green (brierAge ~0.3 half-s: the blade green),
plant (a bramble mid-growth), bramble (brambles standing, the foe out of them, no stop), snare (the held ball, its
shoots clenched), bite (+2 steps after a bite: the thorn flash), stop (a hit stop in the window with a bramble up),
close1 (+0.1s after a clock close), close2 (+0.2s), after (window closed >= 0.6s, a bramble standing), brown (a
bramble in its last 0.6s), over (+0.12s after the kill). A crop round the focus of 2 x 230 units, and the frame.
usage: tw_snap.py page foe seed side [WxH] [hide,comma] [castN]. SCRATCH."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
FOE, SEED, SIDE = sys.argv[2], int(sys.argv[3]), sys.argv[4]
RES = [int(v) for v in sys.argv[5].split("x")] if len(sys.argv) > 5 else [1080, 1920]
HIDE = [h for h in (sys.argv[6].split(",") if len(sys.argv) > 6 else []) if h]
CASTN = int(sys.argv[7]) if len(sys.argv) > 7 else 1
TAG = f"{PAGE.stem}_{FOE}_{SEED}{SIDE}_{RES[0]}" + ("_no-" + "-".join(HIDE) if HIDE else "") + (f"_c{CASTN}" if CASTN != 1 else "")
OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
JS = r"""([foe, seed, side, res, hide, castN]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(res[0], res[1]);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const r = AC.renderer, P = Object.getPrototypeOf(r);
  for (const h of hide) if (P[h]) r[h] = function(){};
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = side === "a" ? new AC.Match("thornwake", foe, seed) : new AC.Match(foe, "thornwake", seed);
  const me = m.a.w.id === "thornwake" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const mySide = me === m.a ? "a" : "b";
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const R = AC.CONFIG.physics.ballR, PR = me.w.ult.patchR, PL = me.w.ult.patchLife;
  const mine = () => m.brambles.filter(b => b.side === mySide);
  const newest = () => { const G = mine(); return G.length ? G[G.length - 1] : null; };
  const out = {}; let step = 0, closeT = null, casts = 0, prev = null, overT = null, tick0 = -1, lastTicks = 0;
  const snap = (k, focus) => { const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D); AC.__draw(m);
    Math.random = realRandom; m.shake = ks;
    const Z = me.ultBramble, T = me.brambleTally, F = focus || [me.x, me.y];
    out[k] = { png: cv.toDataURL("image/png"), t: +m.t.toFixed(3), zt: Z ? +Z.t.toFixed(3) : null,
               stop: +m.hitStop.toFixed(3), me: toDev(me.x, me.y), foe: toDev(th.x, th.y), focus: toDev(F[0], F[1]), k: r.k * r.scale,
               green: me.brierGreen === undefined ? null : +me.brierGreen.toFixed(3),
               age: me.brierAge === undefined ? null : +me.brierAge.toFixed(3),
               held: th.brierHeld === undefined ? null : th.brierHeld, heldAge: th.brierHeldAge === undefined ? null : +th.brierHeldAge.toFixed(3),
               pin: +(th.pin || 0).toFixed(3), inside: me.brambleIn,
               brambles: mine().map(b => [+(m.brambleT - b.t0).toFixed(2), Math.round(b.x), Math.round(b.y)]),
               pic: me.brierPic ? me.brierPic.map(p => +p.age.toFixed(2)) : null,
               ent: th.stacks("entangle"),
               tally: T ? Object.assign({}, T) : null, over: m.over,
               tags: m.tags.map(g => [g.key, g.val, +g.life.toFixed(2)]) }; };
  const want = ["rest", "cast", "green", "plant", "bramble", "snare", "bite", "stop", "close1", "close2", "after", "brown", "over"];
  while (step < 200 / DT && want.some(k => !out[k])){
    m.step(DT); step++;
    const Z = me.ultBramble, T = me.brambleTally;
    if (m.over){
      if (overT === null) overT = m.t;
      if (!out.over && m.t - overT > 0.12 && (casts >= castN)) snap("over", newest() ? [newest().x, newest().y] : null);
      if (m.t - overT > 0.5) break;
      continue;
    }
    if (Z && !prev) casts++;
    if (!Z && prev && me.alive && th.alive) closeT = m.t;
    const castNow = Z && !prev;
    prev = Z;
    const clean = m.hitStop <= 0 && !(me.flash > 0) && !(th.flash > 0);
    if (!out.rest && !Z && casts === 0 && m.t > 3 && clean) snap("rest");
    if (casts < castN) continue;
    const nb = newest(), bAge = nb ? m.brambleT - nb.t0 : -1;
    const pn = me.brierPic && me.brierPic.length ? me.brierPic[me.brierPic.length - 1] : null;
    if (T && T.ticks > lastTicks){ tick0 = step; lastTicks = T.ticks; }
    if (casts === castN){
      if (!out.cast && castNow) snap("cast");
      if (!out.green && Z && me.brierAge > 0.28 && me.brierAge < 0.4) snap("green");
      if (!out.plant && pn && pn.age > 0.25 && pn.age < 0.4) snap("plant", [pn.b.x, pn.b.y]);
      if (!out.bramble && Z && nb && bAge > 0.6 && clean && !me.brambleIn && Z.t > 1) snap("bramble", [nb.x, nb.y]);
      if (!out.snare && th.brierHeld && th.brierHeldAge > 0.5 && th.brierHeldAge < 0.7 && th.alive) snap("snare", [th.x, th.y]);
      if (!out.bite && tick0 > 0 && step - tick0 === 2 && th.alive) snap("bite", [th.x, th.y]);
      if (!out.stop && Z && m.hitStop > 0 && Z.t > 0.5 && mine().length) snap("stop", nb ? [nb.x, nb.y] : null);
      if (!out.close1 && !Z && closeT !== null && m.t - closeT > 0.09 && m.t - closeT < 0.12) snap("close1");
      if (!out.close2 && !Z && closeT !== null && m.t - closeT > 0.19 && m.t - closeT < 0.22) snap("close2");
    }
    if (!out.after && !Z && closeT !== null && m.t - closeT > 0.6 && nb && clean) snap("after", [nb.x, nb.y]);
    if (!out.brown && nb && PL - bAge < 0.6 && PL - bAge > 0.35 && clean) snap("brown", [nb.x, nb.y]);
  }
  out.casts = casts; out.t = m.t; out.over = m.over;
  return out;
}"""
if __name__ == "__main__":
    with game(game_path=PAGE) as (page, errors):
        r = page.evaluate(JS, [FOE, SEED, SIDE, RES, HIDE, CASTN])
        assert not errors, errors[:5]
    for k, v in r.items():
        if isinstance(v, dict) and "png" in v:
            im = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
            K = v["k"]
            half = int(int(__import__("os").environ.get("TW_HALF", "230")) * K)
            cx, cy = v["focus"]
            W = 2 * half
            box = (int(max(0, min(im.width - W, cx - half))), int(max(0, min(im.height - W, cy - half))))
            im.crop(box + (box[0] + W, box[1] + W)).save(OUTD / f"{TAG}_{k}.png")
            im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(OUTD / f"{TAG}_{k}_frame.png")
            print(k, json.dumps(v))
        else:
            print(k, v)
