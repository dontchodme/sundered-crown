"""THE GATES on real fights, on the DELIVERED bytes (hw-tip-fx.html = the real carry onto sc-tendril-fx + the
rows + SPECS.heartwood out of the inlined fx.js copy: the look as it ships; or any page given). No lab variant: a
component is hidden by shadowing its renderer method on the instance from outside the page (`r[name] = () => {}`),
and the tag's count is held out by marking what `tickGrove` re-counts (a wrapper on the match instance,
harness-side). 540x960, chain on/off, shake zeroed, Math.random pinned per frame.
  bloom   -- the picture's share of the post chain's arena lift: (lift with the picture) - (lift with it all
             hidden), per frame; and the raw luma it adds.
  discs   -- caster and foe disc mean luma / clip with and without the picture, and the art alone (tag count out).
  legib.  -- |dL| per component (hide one, diff; the pixels that move by > 0.02), in and out of a hit stop.
  controls that must FAIL -- drawn in the EMISSIVE pass (after drawSunTop) from outside: ctrl1 a white-hot lighter
             halo on the caster for the window; ctrl2 a 200-unit white lighter flash on the held foe for each root
             (the Harrowing's class: reach, not alpha); ctrl3 the sword's reach lit as a disc round the caster at
             0.35 lighter for the window (Bindweed's control).
The root's shoots are TENDRIL'S `_twineRoot` (reused): hidden as a component by shadowing it.
usage: hw_measure.py page out.json [foe seed side]... SCRATCH."""
import sys, json, pathlib, os
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent

SETUP = r"""([res]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(res[0], res[1]);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  return { chain: AC.POSTFX.on, k: AC.renderer.k, W: document.getElementById("cv").width };
}"""

SEEK = r"""([foe, seed, side, want]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("heartwood", foe, seed) : new AC.Match(foe, "heartwood", seed);
  const me = m.a.w.id === "heartwood" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random, TAU = Math.PI * 2;
  const HAS = typeof m.tickGrove === "function";
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const u2d = () => r.k * r.scale;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  /* the root's re-counted tags, marked harness-side */
  if (HAS){
    const tg = m.tickGrove;
    m.tickGrove = function(dt){
      const before = new Map(this.tags.map(g => [g, g.val]));
      tg.call(this, dt);
      for (const g of this.tags) if (before.has(g) && before.get(g) !== g.val && g.__g0 === undefined) g.__g0 = before.get(g);
    };
  }
  const ALL = ["_groveBlade", "drawGrove", "_twineRoot"];
  const st0 = r.drawSunTop;
  const ctrlOn = { 1: () => me.groveFade > 0 && me.alive, 2: () => true, 3: () => me.groveFade > 0 && me.alive };
  let rootFlash = [];
  const CTRL = {
    1: function(mm){ st0.call(this, mm);
         if (!ctrlOn[1]()) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const g = c.createRadialGradient(me.x, me.y, 0, me.x, me.y, R * 1.8);
         g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.6, "#F4FFF0"); g.addColorStop(1, "#F4FFF000");
         c.globalAlpha = 0.9; c.fillStyle = g;
         c.beginPath(); c.arc(me.x, me.y, R * 1.8, 0, TAU); c.fill(); c.restore(); },
    2: function(mm){ st0.call(this, mm);
         if (!(th.twineRootFade > 0) || !th.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const g = c.createRadialGradient(th.x, th.y, 0, th.x, th.y, 200);
         g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.5, "#F4FFF0"); g.addColorStop(1, "#F4FFF000");
         c.globalAlpha = th.twineRootFade; c.fillStyle = g;
         c.beginPath(); c.arc(th.x, th.y, 200, 0, TAU); c.fill(); c.restore(); },
    3: function(mm){ st0.call(this, mm);
         if (!ctrlOn[3]()) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter"; c.globalAlpha = 0.35;
         c.fillStyle = me.aff.glow; const rc = R + me.w.reach * mm.actMods.reach * me.reachMul;
         c.beginPath(); c.arc(me.x, me.y, rc, 0, TAU); c.fill(); c.restore(); },
  };
  function frame(chain, hide, tags, ctrl){
    const saved = [];
    for (const h of hide || []) if (typeof r[h] === "function"){ r[h] = function(){}; saved.push(h); }
    if (ctrl){ r.drawSunTop = CTRL[ctrl]; saved.push("drawSunTop"); }
    const G = m.tags;
    if (tags === false) m.tags = G.map(g => g.__g0 !== undefined ? Object.assign({}, g, { val: g.__g0 }) : g);
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    const was = AC.POSTFX.on; AC.POSTFX.on = chain;
    try { AC.__draw(m); }
    finally { AC.POSTFX.on = was; Math.random = realRandom; m.shake = ks; m.tags = G; for (const h of saved) delete r[h]; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data);
  }
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  function arena(d){
    const x0 = Math.round(r.pad * r.k), y0 = Math.round(r.arenaTop * r.k);
    const w = Math.round(r.aw * r.k), h = Math.round(r.ah * r.k), cw = cv.width;
    let sum = 0, n98 = 0, n = 0;
    for (let y = y0; y < y0 + h; y++) for (let x = x0; x < x0 + w; x++){
      const v = L(d, (y * cw + x) * 4); sum += v; n++; if (v > 0.98) n98++; }
    return { mean: sum / n, clip: n98 / n };
  }
  function disc(d, f){
    const [cx, cy] = toDev(f.x, f.y), rr = R * 0.97 * u2d(), w = cv.width;
    let sum = 0, n = 0, clip = 0, p90 = 0;
    for (let y = Math.round(cy - rr); y < cy + rr; y++) for (let x = Math.round(cx - rr); x < cx + rr; x++){
      if (x < 0 || y < 0 || x >= w || y >= cv.height) continue;
      if ((x - cx) ** 2 + (y - cy) ** 2 > rr * rr) continue;
      const v = L(d, (y * w + x) * 4); sum += v; n++; if (v > 0.98) clip++; if (v > 0.90) p90++; }
    return { mean: n ? sum / n : 0, clip: n ? clip / n : 0, over90: n ? p90 / n : 0 };
  }
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lab = (d, i) => { const R_ = lin(d[i]), G = lin(d[i+1]), B = lin(d[i+2]);
    const X = (0.4124 * R_ + 0.3576 * G + 0.1805 * B) / 0.95047, Y = 0.2126 * R_ + 0.7152 * G + 0.0722 * B, Z = (0.0193 * R_ + 0.1192 * G + 0.9505 * B) / 1.08883;
    const f = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))]; };
  /* the pixels a component moves: |dL| > 0.02 OR CIE76 dE > 2.3 (a hue change is a change); |dL| and dE of those */
  function comp(dw, dh){
    let n = 0, s = 0, pk = 0, e = 0, nL = 0, sL = 0;
    for (let i = 0; i < dw.length; i += 4){
      if (dw[i] === dh[i] && dw[i+1] === dh[i+1] && dw[i+2] === dh[i+2]) continue;
      const dl = Math.abs(L(dw, i) - L(dh, i)), a = lab(dw, i), b = lab(dh, i);
      const de = Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
      if (dl < 0.02 && de < 2.3) continue;
      n++; s += dl; e += de; if (dl > pk) pk = dl; if (dl >= 0.02){ nL++; sL += dl; } }
    return { n, dL: n ? s / n : 0, dE: n ? e / n : 0, peak: pk, nL, dLonly: nL ? sL / nL : 0, areaU: n / (u2d() * u2d()) };
  }
  function measure(st){
    const T = me.rootTally;
    const out = { st, t: +m.t.toFixed(3), zt: me.ultRoot ? +me.ultRoot.t.toFixed(3) : null,
                  fade: +(me.groveFade || 0).toFixed(3), age: +(me.groveAge || 0).toFixed(3), out: +(me.groveOut || 0).toFixed(3),
                  stop: m.hitStop > 0, foeEnt: th.stacks("entangle"), foeAff: th.aff.key, over: m.over,
                  pin: +(th.pin || 0).toFixed(3), held: th.twineHeld || 0, heldAge: +(th.twineHeldAge || 0).toFixed(3),
                  motes: me.groveMotes.length, bits: me.groveBits.length,
                  dFoe: +Math.hypot(th.x - me.x, th.y - me.y).toFixed(1), gtags: m.tags.filter(g => g.__g0 !== undefined).length };
    const onW = frame(true), offW = frame(false), onO = frame(true, ALL, false), offO = frame(false, ALL, false);
    const aW = arena(onW), aWo = arena(offW), aO = arena(onO), aOo = arena(offO);
    out.arena = { onW: aW.mean, offW: aWo.mean, onO: aO.mean, offO: aOo.mean, liftW: aW.mean - aWo.mean, liftO: aO.mean - aOo.mean,
                  dLift: (aW.mean - aWo.mean) - (aO.mean - aOo.mean), picOn: aW.mean - aO.mean, clipW: aW.clip, clipO: aO.clip };
    out.disc = { me: { W: disc(onW, me), O: disc(onO, me) }, foe: { W: disc(onW, th), O: disc(onO, th) } };
    out.all = comp(onW, onO);
    const comps = { blade: ["_groveBlade"], ground: ["drawGrove"], green: ["_groveGreen"], scale: ["_groveScale"],
                    front: ["_groveFront"], motes: ["_groveMotes"], bits: ["_groveBits"], root: ["_twineRoot"] };
    for (const [k, hs] of Object.entries(comps)){
      const h = frame(true, hs); out[k] = comp(onW, h);
      out[k].meDisc = disc(onW, me).mean - disc(h, me).mean; out[k].foeDisc = disc(onW, th).mean - disc(h, th).mean;
    }
    out.tag = comp(onW, frame(true, [], false));
    /* the ART on the discs, the tag's count held out */
    const artW = frame(true, [], false);
    out.artDisc = { me: disc(artW, me).mean - disc(onO, me).mean, foe: disc(artW, th).mean - disc(onO, th).mean,
                    meClip: disc(artW, me).clip, foeClip: disc(artW, th).clip, me90: disc(artW, me).over90, foe90: disc(artW, th).over90 };
    for (const c of [1, 2, 3]){
      const cW = frame(true, [], true, c), cWo = frame(false, [], true, c);
      const ac = arena(cW), aco = arena(cWo);
      out["ctrl" + c] = { dLift: (ac.mean - aco.mean) - (aO.mean - aOo.mean), picOn: ac.mean - aO.mean, clip: ac.clip,
                          me: disc(cW, me), foe: disc(cW, th) };
    }
    return out;
  }
  const out = { foe, seed, side, has: HAS, got: {}, missing: [] };
  const left = new Set(want);
  let step = 0, seenR = 0, seenN = 0, overAt = -1, liveAtOver = false, closeAt = -1, prevZ = null, pend = [], casts = 0;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (step < 200 / DT && left.size){
    m.step(DT); step++;
    if (m.over){
      if (overAt < 0){ overAt = step; liveAtOver = me.groveFade > 0 && me.alive; }
      if (left.has("over") && liveAtOver && step - overAt === 18){ left.delete("over"); out.got.over = measure("over"); }
      if (step - overAt > 60) break;
      continue;
    }
    const Z = me.ultRoot, T = me.rootTally;
    if (Z && !prevZ) casts++;
    const castNow = Z && !prevZ;
    if (!Z && prevZ && me.alive && th.alive) closeAt = step;
    prevZ = Z;
    const nr = T ? T.roots - seenR : 0, nn = T ? T.rooted - seenN : 0;
    if (T){ seenR = T.roots; seenN = T.rooted; }
    for (const p of pend) p.n--;
    const due = pend.filter(p => p.n <= 0); pend = pend.filter(p => p.n > 0);
    for (const p of due) if (left.has(p.k) && th.alive){ left.delete(p.k); out.got[p.k] = measure(p.k); }
    if (r.scrunchK && r.scrunchK(m) < 0.999) continue;
    const clean = m.hitStop <= 0 && th.alive;
    const W = (k) => left.has(k) && !pend.some(q => q.k === k);
    let st = null;
    if (W("rest") && !Z && casts === 0 && m.t > 3 && clean && inHall(me, 100)) st = "rest";
    else if (W("cast") && castNow) st = "cast";
    else if (W("caststop") && Z && m.hitStop > 0 && m.hitStop <= DT * 1.5 && me.groveAge < 0.2) st = "caststop";
    else if (W("green") && Z && me.groveAge > 0.26 && me.groveAge < 0.36) st = "green";
    else if (W("sprout") && Z && me.groveAge > 0.5 && me.groveAge < 0.62 && m.hitStop <= 0) st = "sprout";
    else if (W("window") && Z && Z.t > 2 && clean && me.groveMotes.length > 2 && !(th.pin > 0)) st = "window";
    else if (W("stop") && Z && m.hitStop > 0 && Z.t > 1) st = "stop";
    else if (W("held") && Z && th.twineHeld && th.twineHeldAge > 0.5 && th.twineHeldAge < 0.7 && clean) st = "held";
    else if (W("wilt") && Z && th.twineHeld && th.pin > 0.08 && th.pin < 0.2 && clean) st = "wilt";
    else if (W("close") && closeAt >= 0 && step - closeAt >= 14 && step - closeAt <= 40 && m.hitStop <= 0) st = "close";
    if (nr > 0 && th.alive && th.pin > 0 && W("root")) pend.push({ k: "root", n: 3 });
    if (nr === 0 && nn > 0 && th.alive && W("reroot")) pend.push({ k: "reroot", n: 3 });
    if (!st) continue;
    left.delete(st);
    out.got[st] = measure(st);
  }
  out.missing = Array.from(left);
  return out;
}"""

FIGHTS = [("dawnbringer", 99001, "a"), ("lastlight", 4242, "b"), ("morningstar", 8888, "a"),
          ("gravemourn", 99015, "a"), ("twinshade", 99008, "b"), ("nightfell", 5150, "a"),
          ("spellbreaker", 2207, "a"), ("grudgebearer", 31337, "b"), ("paradox", 1234, "a"),
          ("bindweed", 2317, "b"), ("thornwake", 777, "a"), ("widowmaker", 99001, "b")]
WANT = os.environ.get("HW_WANT", "rest,cast,caststop,green,sprout,window,stop,root,held,wilt,reroot,close,over").split(",")
if __name__ == "__main__":
    page_ = pathlib.Path(sys.argv[1]); page_ = page_ if page_.is_absolute() else HERE / page_
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "m1.json"
    out = out if out.is_absolute() else HERE / out
    fights = FIGHTS if len(sys.argv) <= 3 else [(sys.argv[i], int(sys.argv[i + 1]), sys.argv[i + 2]) for i in range(3, len(sys.argv), 3)]
    res = []
    with game(game_path=page_) as (page, errors):
        page.evaluate(SETUP, [[540, 960]])
        for foe, seed, side in fights:
            r = page.evaluate(SEEK, [foe, seed, side, WANT])
            assert not errors, errors[:3]
            res.append(r)
            print(foe, seed, side, "got", list(r["got"]), "missing", r["missing"], flush=True)
            out.write_text(json.dumps(res, indent=1))
