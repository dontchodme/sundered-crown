"""Frames off one real Heartwood fight on a page, at the key states of Rootfast's picture:
rest (before the first cast), cast (the cast frame, in its hit stop), green (groveAge ~0.3 half-s: the front
mid-blade), grown (just after the greening), root (3 steps after a NEW hold: the shoots coming up), held (~0.25s
into a hold: clenched), wilt (a hold's last 0.2s), reroot (3 steps after a re-root of a held ball), window (a clean
frame mid-window with motes), stop (a hit stop inside the window), close1 (+0.1s after a clock close), close2
(+0.3s), over (+0.15s after a kill inside the window).
usage: hw_snap.py page foe seed side [WxH] [hide,comma]. SCRATCH. Saves crops + half frames to snaps/."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent

JS = r"""([foe, seed, side, res, hide, want]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(res[0], res[1]);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const r = AC.renderer, P = Object.getPrototypeOf(r);
  for (const h of hide) if (P[h]) r[h] = function(){};
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = side === "a" ? new AC.Match("heartwood", foe, seed) : new AC.Match(foe, "heartwood", seed);
  const me = m.a.w.id === "heartwood" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const out = {}; let step = 0, closeT = null, casts = 0, prev = null, pend = [], overT = null, liveAtOver = false;
  let seenR = 0, seenN = 0;
  const snap = (k, who) => { const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D); AC.__draw(m);
    Math.random = realRandom; m.shake = ks;
    const T = me.rootTally;
    out[k] = { png: cv.toDataURL("image/png"), who, t: +m.t.toFixed(3), zt: me.ultRoot ? +me.ultRoot.t.toFixed(3) : null,
               fade: +(me.groveFade || 0).toFixed(3), age: +(me.groveAge || 0).toFixed(3), out: +(me.groveOut || 0).toFixed(3),
               stop: +m.hitStop.toFixed(3), me: toDev(me.x, me.y), foe: toDev(th.x, th.y), k: r.k * r.scale,
               pin: +(th.pin || 0).toFixed(3), held: th.twineHeld || 0, rootFade: +(th.twineRootFade || 0).toFixed(3),
               heldAge: +(th.twineHeldAge || 0).toFixed(3), roots: T ? T.roots : 0, rooted: T ? T.rooted : 0,
               ent: th.stacks("entangle"), motes: me.groveMotes.length, bits: me.groveBits.length, over: m.over,
               tags: m.tags.filter(g => g.key === "entangle").map(g => [g.val, +g.life.toFixed(2), g.first]) }; };
  const need = new Set(want);
  while (step < 200 / DT && [...need].some(k => !out[k])){
    m.step(DT); step++;
    const Z = me.ultRoot, T = me.rootTally;
    if (m.over){
      if (overT === null){ overT = step; liveAtOver = me.groveFade > 0; }     // m.t stands once over: count steps
      if (liveAtOver && need.has("over") && !out.over && (step - overT) * DT > 0.15) snap("over", "me");
      if ((step - overT) * DT > 0.5) break;
      continue;
    }
    if (Z && !prev) casts++;
    if (!Z && prev && me.alive && th.alive) closeT = m.t;
    const castNow = Z && !prev;
    prev = Z;
    const nr = T ? T.roots - seenR : 0, nn = T ? T.rooted - seenN : 0;
    if (T){ seenR = T.roots; seenN = T.rooted; }
    for (const p of pend) p.n--;
    const due = pend.filter(p => p.n <= 0); pend = pend.filter(p => p.n > 0);
    for (const p of due) if (!out[p.k]) snap(p.k, p.who);
    const clean = m.hitStop <= 0;
    const W = (k) => need.has(k) && !out[k] && !pend.some(q => q.k === k);
    if (W("rest") && !Z && casts === 0 && m.t > 3 && clean) snap("rest", "me");
    if (W("cast") && castNow) snap("cast", "me");
    if (W("green") && Z && me.groveAge > 0.26 && me.groveAge < 0.36) snap("green", "me");
    if (W("grown") && Z && me.groveAge > 0.66 && me.groveAge < 0.8 && clean) snap("grown", "me");
    if (nr > 0 && th.alive && th.pin > 0 && W("root")) pend.push({ k: "root", n: 3, who: "foe" });
    if (nr > 0 && th.alive && th.pin > 0 && W("held") && out.root) pend.push({ k: "held", n: 30, who: "foe" });
    if (nr === 0 && nn > 0 && th.alive && W("reroot")) pend.push({ k: "reroot", n: 3, who: "foe" });
    if (W("wilt") && th.twineHeld && th.pin > 0.08 && th.pin < 0.2 && clean && Z) snap("wilt", "foe");
    if (W("window") && Z && Z.t > 3 && clean && me.groveMotes.length > 3 && Math.hypot(th.x - me.x, th.y - me.y) > 150) snap("window", "me");
    if (W("stop") && Z && m.hitStop > 0 && Z.t > 1) snap("stop", "me");
    if (W("close1") && !Z && closeT !== null && m.t - closeT > 0.09 && m.t - closeT < 0.12) snap("close1", "me");
    if (W("close2") && !Z && closeT !== null && m.t - closeT > 0.29 && m.t - closeT < 0.32) snap("close2", "me");
  }
  out.casts = casts; out.t = m.t; out.isOver = m.over;   // not `over`: that key is the kill's frame
  return out;
}"""
ALL = ["rest", "cast", "green", "grown", "root", "held", "wilt", "reroot", "window", "stop", "close1", "close2", "over"]


def run(page_path, foe, seed, side, res=(1080, 1920), hide=(), want=ALL):
    page_path = pathlib.Path(page_path); page_path = page_path if page_path.is_absolute() else HERE / page_path
    with game(game_path=page_path) as (page, errors):
        r = page.evaluate(JS, [foe, seed, side, list(res), list(hide), list(want)])
        assert not errors, errors[:5]
    ims = {}
    for k, v in list(r.items()):
        if isinstance(v, dict) and "png" in v:
            ims[k] = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
    return r, ims


def crop(im, v, size):
    cx, cy = v["me"] if v["who"] == "me" else v["foe"]
    return im.crop((int(max(0, min(im.width - size, cx - size / 2))), int(max(0, min(im.height - size, cy - size / 2))),
                    int(max(0, min(im.width - size, cx - size / 2))) + size, int(max(0, min(im.height - size, cy - size / 2))) + size))


if __name__ == "__main__":
    PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
    FOE, SEED, SIDE = sys.argv[2], int(sys.argv[3]), sys.argv[4]
    RES = [int(v) for v in sys.argv[5].split("x")] if len(sys.argv) > 5 else [1080, 1920]
    HIDE = [h for h in (sys.argv[6].split(",") if len(sys.argv) > 6 else []) if h]
    TAG = f"{PAGE.stem}_{FOE}_{SEED}{SIDE}_{RES[0]}" + ("_no-" + "-".join(HIDE) if HIDE else "")
    OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
    r, ims = run(PAGE, FOE, SEED, SIDE, RES, HIDE)
    S = RES[0] / 1080
    for k, im in ims.items():
        v = r[k]
        crop(im, v, int(560 * S)).save(OUTD / f"{TAG}_{k}.png")
        print(k, json.dumps(v))
    print("casts", r.get("casts"), "t", r.get("t"), "over", r.get("isOver"), "missing", [k for k in ALL if k not in ims])
