"""THE GATES on real fights, on the DELIVERED bytes (ld-final.html = the base + the rows; or any page given). No
lab variant: a component is hidden by shadowing its renderer method on the instance from outside the page
(`r[name] = () => {}`), and the walls' own hex tags are held out by marking what `tickLode` adds or re-counts (a
wrapper on the match instance, harness-side). 540x960, chain on/off, shake zeroed, Math.random pinned per frame.
  bloom   -- the picture's share of the post chain's arena lift: (lift with the picture) - (lift with it all
             hidden), per frame; and the raw luma it adds.
  discs   -- caster and foe disc mean luma / clip with and without the picture, and the art alone (tags out).
  legib.  -- |dL| per component (hide one, diff; the pixels that move by > 0.02), in and out of a hit stop.
  controls that must FAIL -- drawn from outside in the EMISSIVE block (in the slot of `drawSunTop`, which draws
             nothing on a fight without Zenith): ctrl1 a white-hot lighter halo on the caster for the window;
             ctrl2 the walls as a 100-unit white lighter band round the whole hall for the window (reach: the
             Harrowing's class); ctrl3 a 200-unit white lighter radial flash at each touch for its flare.
usage: ld_measure.py page out.json [foe seed side]... SCRATCH."""
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
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  const me = m.a.w.id === "lodestone" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random, TAU = Math.PI * 2;
  const HAS = typeof m.tickLode === "function";
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const u2d = () => r.k * r.scale;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  /* the walls' own tags, marked harness-side: new ones, and the hammer's own re-counted in place */
  if (HAS){
    const tl = m.tickLode;
    m.tickLode = function(dt){
      const before = new Map(this.tags.map(g => [g, g.val]));
      tl.call(this, dt);
      for (const g of this.tags){
        if (!before.has(g)){ g.__qNew = 1; }
        else if (before.get(g) !== g.val && !g.__qNew && g.__q0 === undefined){ g.__q0 = before.get(g); }
      }
    };
  }
  const ALL = ["drawLode", "drawLodeTop", "_lodeHead"];
  const st0 = r.drawSunTop;
  const CTRL = {
    1: function(mm){ st0 && st0.call(this, mm);
         if (!(me.lodeFade > 0)) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const g = c.createRadialGradient(me.x, me.y, 0, me.x, me.y, R * 1.8);
         g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.6, "#DDEEFF"); g.addColorStop(1, "#DDEEFF00");
         c.globalAlpha = 0.9 * me.lodeFade; c.fillStyle = g;
         c.beginPath(); c.arc(me.x, me.y, R * 1.8, 0, TAU); c.fill(); c.restore(); },
    2: function(mm){ st0 && st0.call(this, mm);
         if (!(me.lodeFade > 0)) return;
         const c = this.ctx, n = mm.inset || 0; c.save(); c.globalCompositeOperation = "lighter";
         c.globalAlpha = me.lodeFade; c.strokeStyle = "#FFFFFF"; c.lineWidth = 100;
         c.strokeRect(n, n, A.w - 2 * n, A.h - 2 * n); c.restore(); },
    3: function(mm){ st0 && st0.call(this, mm);
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         for (const q of (me.lodeFx || [])){ const k = q.t / 0.3; if (k >= 1) continue;
           const g = c.createRadialGradient(q.x, q.y, 0, q.x, q.y, 200);
           g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.5, "#DDEEFF"); g.addColorStop(1, "#DDEEFF00");
           c.globalAlpha = 1 - k; c.fillStyle = g;
           c.beginPath(); c.arc(q.x, q.y, 200, 0, TAU); c.fill(); }
         c.restore(); },
  };
  function frame(chain, hide, tags, ctrl){
    const saved = [];
    for (const h of hide || []) if (typeof r[h] === "function"){ r[h] = function(){}; saved.push(h); }
    if (ctrl){ r.drawSunTop = CTRL[ctrl]; saved.push("drawSunTop"); }
    const G = m.tags;
    if (tags === false) m.tags = G.filter(g => !g.__qNew).map(g => g.__q0 !== undefined ? Object.assign({}, g, { val: g.__q0 }) : g);
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
    let sum = 0, n = 0, clip = 0;
    for (let y = Math.round(cy - rr); y < cy + rr; y++) for (let x = Math.round(cx - rr); x < cx + rr; x++){
      if (x < 0 || y < 0 || x >= w || y >= cv.height) continue;
      if ((x - cx) ** 2 + (y - cy) ** 2 > rr * rr) continue;
      const v = L(d, (y * w + x) * 4); sum += v; n++; if (v > 0.98) clip++; }
    return { mean: n ? sum / n : 0, clip: n ? clip / n : 0 };
  }
  function contour(d, f){
    const [cx, cy] = toDev(f.x, f.y), r0 = (R + 2) * u2d(), r1 = (R + 8) * u2d(), w = cv.width;
    let sum = 0, n = 0;
    for (let y = Math.round(cy - r1); y < cy + r1; y++) for (let x = Math.round(cx - r1); x < cx + r1; x++){
      if (x < 0 || y < 0 || x >= w || y >= cv.height) continue;
      const q = (x - cx) ** 2 + (y - cy) ** 2; if (q < r0 * r0 || q > r1 * r1) continue;
      sum += L(d, (y * w + x) * 4); n++; }
    return n ? sum / n : 0;
  }
  function comp(dw, dh){
    let n = 0, s = 0, pk = 0;
    for (let i = 0; i < dw.length; i += 4){
      const dl = L(dw, i) - L(dh, i); if (Math.abs(dl) < 0.02) continue;
      n++; s += Math.abs(dl); if (Math.abs(dl) > pk) pk = Math.abs(dl); }
    return { n, dL: n ? s / n : 0, peak: pk, areaU: n / (u2d() * u2d()) };
  }
  function measure(st){
    const Z = me.ultRunes;
    const out = { st, t: +m.t.toFixed(3), zt: Z ? +Z.t.toFixed(3) : null,
                  fade: +(me.lodeFade || 0).toFixed(3), age: +(me.lodeAge || 0).toFixed(3),
                  out: +(me.lodeOut || 0).toFixed(3), die: me.lodeDie, stop: m.hitStop > 0, foeHex: th.stacks("hex"),
                  fx: (me.lodeFx || []).map(q => +q.t.toFixed(3)), inset: +(m.inset || 0).toFixed(1),
                  foeAff: th.aff.key, over: m.over, dFoe: +Math.hypot(th.x - me.x, th.y - me.y).toFixed(1),
                  qtags: m.tags.filter(g => g.__qNew || g.__q0 !== undefined).length, meStun: me.stun > 0 };
    const onW = frame(true), offW = frame(false), onO = frame(true, ALL, false), offO = frame(false, ALL, false);
    const aW = arena(onW), aWo = arena(offW), aO = arena(onO), aOo = arena(offO);
    out.arena = { onW: aW.mean, offW: aWo.mean, onO: aO.mean, offO: aOo.mean, liftW: aW.mean - aWo.mean, liftO: aO.mean - aOo.mean,
                  dLift: (aW.mean - aWo.mean) - (aO.mean - aOo.mean), picOn: aW.mean - aO.mean, clipW: aW.clip, clipO: aO.clip };
    out.disc = { me: { W: disc(onW, me), O: disc(onO, me), cW: contour(onW, me), cO: contour(onO, me) },
                 foe: { W: disc(onW, th), O: disc(onO, th), cW: contour(onW, th), cO: contour(onO, th) } };
    out.all = comp(onW, onO);
    const comps = { ground: ["drawLode"], top: ["drawLodeTop"], head: ["_lodeHead"], walls: ["_lodeWalls"],
                    motes: ["_lodeMotes"], flare: ["_lodeFlare"], streak: ["_lodeStreak"], bolt: ["_lodeBolt"] };
    for (const [k, hs] of Object.entries(comps)){
      const h = frame(true, hs); out[k] = comp(onW, h);
      out[k].meDisc = disc(onW, me).mean - disc(h, me).mean; out[k].foeDisc = disc(onW, th).mean - disc(h, th).mean;
    }
    out.tag = comp(onW, frame(true, [], false));
    const dw = r.drawWeapon;
    r.drawWeapon = function(mm, f){ if (f !== me) return dw.call(this, mm, f); };
    let noWep, noWepO;
    try { noWep = frame(true); noWepO = frame(true, ALL, false); } finally { r.drawWeapon = dw; }
    out.weapon = comp(onW, noWep);
    out.weaponBase = comp(onO, noWepO);
    const artW = frame(true, [], false);
    out.artDisc = { me: disc(artW, me).mean - disc(onO, me).mean, foe: disc(artW, th).mean - disc(onO, th).mean,
                    meClip: disc(artW, me).clip, foeClip: disc(artW, th).clip };
    for (const c of [1, 2, 3]){
      const cW = frame(true, [], true, c), cWo = frame(false, [], true, c);
      const ac = arena(cW), aco = arena(cWo);
      out["ctrl" + c] = { dLift: (ac.mean - aco.mean) - (aO.mean - aOo.mean), picOn: ac.mean - aO.mean, clip: ac.clip,
                          me: disc(cW, me), foe: disc(cW, th), foeC: contour(cW, th) };
    }
    return out;
  }
  const out = { foe, seed, side, has: HAS, got: {}, missing: [] };
  const left = new Set(want);
  let step = 0, seenT = 0, touchAt = -1, overAt = -1, litAtOver = false, closeAt = -1, prevZ = null, casts = 0;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (step < 200 / DT && left.size){
    m.step(DT); step++;
    if (m.over){
      if (overAt < 0){ overAt = step; litAtOver = me.lodeFade > 0; }
      if (left.has("over") && litAtOver && step - overAt === 12){ left.delete("over"); out.got.over = measure("over"); }
      if (step - overAt > 60) break;
      continue;
    }
    const Z = me.ultRunes, T = me.runeTally;
    if (Z && !prevZ) casts++;
    if (T && T.touches > seenT){ seenT = T.touches; if (Z && th.alive) touchAt = step; }
    if (!Z && prevZ && me.alive && th.alive) closeAt = step;
    prevZ = Z;
    if (r.scrunchK && r.scrunchK(m) < 0.999) continue;
    const clean = m.hitStop <= 0 && !(me.flash > 0) && th.alive;
    const fxLive = (me.lodeFx || []).some(q => q.t < 0.8);
    let st = null;
    if (left.has("rest") && !Z && !(me.lodeFade > 0) && m.t > 3 && clean && inHall(me, 100) && !m.ultFx) st = "rest";
    else if (left.has("cast") && Z && me.lodeAge > 0.2 && me.lodeAge < 0.45 && casts >= 1) st = "cast";
    else if (left.has("lit") && Z && Z.t > 1.5 && clean && !fxLive && !(me.stun > 0)) st = "lit";
    else if (left.has("stop") && Z && m.hitStop > 0 && Z.t > 0.5 && !fxLive) st = "stop";
    else if (left.has("touch0") && touchAt === step) st = "touch0";
    else if (left.has("touch2") && touchAt >= 0 && step - touchAt === 2 && m.hitStop <= 0) st = "touch2";
    else if (left.has("touch10") && touchAt >= 0 && step - touchAt === 10 && m.hitStop <= 0) st = "touch10";
    else if (left.has("tstop") && m.hitStop > 0 && (me.lodeFx || []).some(q => q.t < 0.3)) st = "tstop";
    else if (left.has("close") && closeAt >= 0 && me.lodeOut > 0.25 && me.lodeOut < 0.55 && m.hitStop <= 0) st = "close";
    if (!st) continue;
    left.delete(st);
    out.got[st] = measure(st);
  }
  out.missing = Array.from(left);
  return out;
}"""

FIGHTS = [("dawnbringer", 99001, "a"), ("aureole", 4101, "b"),
          ("gravemourn", 99015, "a"), ("shroudmaul", 5150, "b"), ("twinshade", 99008, "a"),
          ("spellbreaker", 99015, "a"), ("grudgebearer", 31337, "b"), ("lastlight", 4242, "a"),
          ("widowmaker", 2207, "a")]
WANT = os.environ.get("LD_WANT", "rest,cast,lit,stop,touch0,touch2,touch10,tstop,close,over").split(",")
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
