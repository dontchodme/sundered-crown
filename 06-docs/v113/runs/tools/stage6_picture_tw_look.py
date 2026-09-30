"""Strips for the contact sheet off one real Thornwake fight (tw-final-fx.html unless given), 1080x1920, chain on:
  rest       the resting scythe before the first cast (crop: the caster)
  cast0..5   the blade greening: brierAge (half-seconds) past 0.02 / 0.12 / 0.24 / 0.36 / 0.48 / 0.62 (crop: the caster)
  plant0..5  the window's first bramble growing out of the blow: its picture age past 0.02 / 0.12 / 0.24 / 0.36 / 0.48 /
             0.62 (crop: the bramble)
  snare0..5  the window's first snare: 2 steps before it, then +1 / +8 / +20 / +50 / +84 steps (the shoots grow,
             clench, hold, dry, and wilt after the 0.6s pin) (crop: the foe)
  bite0..3   a bite with the foe in a bramble (not in a snare's first frames): 1 step before, then +1 / +4 / +9 steps
             (the thorn flash, 0.12s; ENTANGLE n) (crop: the foe)
  close0..5  the close: brierOut past 0.02 / 0.12 / 0.24 / 0.36 / 0.48 / 0.58 (the green goes) (crop: the caster, wide)
  brown0..4  a bramble's last second: its sim age past 4.8 / 5.2 / 5.5 / 5.8 / 5.95 of 6 (crop: the bramble)
  sig0..3    the HUD charge rune (ULTSIG.thornwake, kept) at charge 0.1 / 0.4 / 0.75 / 1.0 (hot), 4x its HUD size
usage: tw_look.py foe seed side [page] [castN]. Writes snaps/look_<foe>_*.png and snaps/look_<foe>.json. SCRATCH."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
FOE, SEED, SIDE = sys.argv[1], int(sys.argv[2]), sys.argv[3]
PAGE = pathlib.Path(sys.argv[4]) if len(sys.argv) > 4 else HERE / "tw-final-fx.html"
PAGE = PAGE if PAGE.is_absolute() else HERE / PAGE
CASTN = int(sys.argv[5]) if len(sys.argv) > 5 else 1
OUTD = HERE / "snaps"; OUTD.mkdir(exist_ok=True)
JS = r"""([foe, seed, side, castN]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const r = AC.renderer, DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const mk = () => side === "a" ? new AC.Match("thornwake", foe, seed) : new AC.Match(foe, "thornwake", seed);
  const m = mk();
  const me = m.a.w.id === "thornwake" ? m.a : m.b, th = me === m.a ? m.b : m.a, mySide = me === m.a ? "a" : "b";
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const out = {};
  const draw = (mm) => { const ks = mm.shake; mm.shake = 0; Math.random = pin(0x5EEDF00D); AC.__draw(mm); Math.random = realRandom; mm.shake = ks; };
  const snap = (k, focus, extra) => { draw(m);
    out[k] = Object.assign({ png: cv.toDataURL("image/png"), t: +m.t.toFixed(3), zt: me.ultBramble ? +me.ultBramble.t.toFixed(3) : null,
               stop: m.hitStop > 0, focus: toDev(focus[0], focus[1]), k: r.k * r.scale,
               age: +me.brierAge.toFixed(3), outT: +me.brierOut.toFixed(3), green: +me.brierGreen.toFixed(3),
               held: th.brierHeld, heldAge: +th.brierHeldAge.toFixed(3), root: +th.brierRootFade.toFixed(3), pin: +(th.pin || 0).toFixed(3),
               ent: th.stacks("entangle"), inside: me.brambleIn,
               tags: m.tags.map(g => [g.key, g.val]) }, extra || {}); };
  const CA = [0.02, 0.12, 0.24, 0.36, 0.48, 0.62], CO = [0.02, 0.12, 0.24, 0.36, 0.48, 0.58], BR = [4.8, 5.2, 5.5, 5.8, 5.95];
  const SN = [1, 8, 20, 50, 84], BI = [1, 4, 9];
  let step = 0, casts = 0, prev = null, ci = 0, pi = 0, oi = 0, bi = 0, closed = false, pd = null, bd = null, rested = false;
  let snareAt = -1, lastSn = 0, biteAt = -1, lastTk = 0;
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultBramble, T = me.brambleTally;
    if (Z && !prev) casts++;
    const clockClose = !Z && prev && me.alive && th.alive;
    prev = Z;
    if (!rested && !Z && casts === 0 && m.t > 3 && m.hitStop <= 0 && !(me.flash > 0)){ snap("rest", [me.x, me.y]); rested = true; }
    if (casts < castN) continue;
    const mine = casts === castN;
    if (mine && Z && ci < CA.length && me.brierAge >= CA[ci]){ snap("cast" + ci, [me.x, me.y]); ci++; }
    if (mine && !pd && me.brierPic.length){ const p = me.brierPic.find(q => q.age < 0.05); if (p) pd = p; }
    if (pd && pi < CA.length && pd.age >= CA[pi]){ snap("plant" + pi, [pd.b.x, pd.b.y], { pAge: +pd.age.toFixed(3) }); pi++; }
    if (mine && T && T.snares > lastSn && snareAt < 0 && th.brierHeld) snareAt = step;
    if (T) lastSn = T.snares;
    if (snareAt > 0){ const j = SN.indexOf(step - snareAt); if (j >= 0) snap("snare" + (j + 1), [th.x, th.y]); }
    if (mine && T && T.ticks > lastTk && biteAt < 0 && Z && Z.t > 0.8 && m.hitStop <= 0 && !(th.brierRootFade > 0) && th.alive) biteAt = step;
    if (T) lastTk = T.ticks;
    if (biteAt > 0){ const j = BI.indexOf(step - biteAt); if (j >= 0) snap("bite" + (j + 1), [th.x, th.y]); }
    if (mine && clockClose) closed = true;
    if (closed && me.brierGreen > 0 && oi < CO.length && me.brierOut >= CO[oi]){ snap("close" + oi, [me.x, me.y]); oi++; }
    if (mine && !bd){ const G = m.brambles.filter(b => b.side === mySide); if (G.length) bd = G[0]; }
    if (bd && bi < BR.length && m.brambles.indexOf(bd) >= 0 && m.brambleT - bd.t0 >= BR[bi]){ snap("brown" + bi, [bd.x, bd.y], { bAge: +(m.brambleT - bd.t0).toFixed(3) }); bi++; }
    if (closed && bi >= BR.length && oi >= CO.length && (snareAt < 0 || step > snareAt + 90) && (biteAt < 0 || step > biteAt + 12)) break;
    if (closed && bd && m.brambles.indexOf(bd) < 0 && oi >= CO.length && (snareAt < 0 || step > snareAt + 90)) break;
  }
  const replay = (at, key) => {
    const m2 = mk(); for (let s = 0; s < at; s++) m2.step(DT);
    const me2 = m2.a.w.id === "thornwake" ? m2.a : m2.b, th2 = me2 === m2.a ? m2.b : m2.a;
    draw(m2);
    out[key] = { png: cv.toDataURL("image/png"), t: +m2.t.toFixed(3), focus: toDev(th2.x, th2.y), k: r.k * r.scale,
                 held: th2.brierHeld, stop: m2.hitStop > 0, ent: th2.stacks("entangle") };
  };
  if (snareAt > 0) replay(snareAt - 2, "snare0");
  if (biteAt > 0) replay(biteAt - 1, "bite0");
  const c = cv.getContext("2d");
  [0.1, 0.4, 0.75, 1.0].forEach((cf, i) => {
    c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = "#08070B"; c.fillRect(0, 0, 240, 240);
    r._ultSigil(m, me, 120, 120, 100, cf, cf >= 1);
    out["sig" + i] = { png: cv.toDataURL("image/png"), cf, sigBox: [0, 0, 240, 240] };
  });
  out.casts = casts; out.snareAt = snareAt; out.biteAt = biteAt;
  return out;
}"""
with game(game_path=PAGE) as (page, errors):
    r = page.evaluate(JS, [FOE, SEED, SIDE, CASTN])
    assert not errors, errors[:5]
meta = {}
for k, v in r.items():
    if isinstance(v, dict) and "png" in v:
        im = Image.open(io.BytesIO(base64.b64decode(v.pop("png").split(",", 1)[1]))).convert("RGB")
        if k.startswith("sig"):
            im = im.crop(tuple(v["sigBox"]))
        else:
            K = v["k"]
            half = int((200 if k.startswith("close") else 120 if (k.startswith("plant") or k.startswith("brown")) else
                        100 if k.startswith("snare") or k.startswith("bite") else 150) * K)
            cx, cy = v["focus"]
            W = 2 * half
            box = (int(max(0, min(im.width - W, cx - half))), int(max(0, min(im.height - W, cy - half))))
            im = im.crop(box + (box[0] + W, box[1] + W))
        im.save(OUTD / f"look_{FOE}_{k}.png")
        meta[k] = v
    else:
        meta[k] = v
(OUTD / f"look_{FOE}.json").write_text(json.dumps(meta, indent=1))
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("t", "zt", "age", "outT", "green", "held", "heldAge", "root", "pin", "stop", "ent", "tags", "cf", "pAge", "bAge")} if isinstance(v, dict) else v for k, v in meta.items()}, indent=0)[:5000])
