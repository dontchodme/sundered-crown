"""THE GATES on real fights, on the DELIVERED bytes (gs-final-fx.html = the rows + SPECS.oathwound out of
the inlined fx.js copy, the look as it ships; or any page given). No lab variant: a component is hidden by
shadowing its renderer method on the instance from outside the page (`r[name] = () => {}`; a hidden
`drawGoreWeapon` returns undefined, so drawWeapon falls through to the REST blade, which is exactly the
picture-off baseline), and the picture's own readout (the priced blow's larger float) is held out by
restoring the float's size (a wrapper on resolveHit marks the floats it files and their base size,
harness-side). 540x960, chain on/off, shake zeroed, Math.random pinned per frame.
  bloom   -- the picture's share of the post chain's arena lift: (lift with the picture) - (lift with it all
             hidden), per frame; and the raw luma it adds.
  discs   -- caster and foe disc mean luma / clip with and without the picture, and the art alone (readout out).
  legib.  -- |dL| per component (hide one, diff; the pixels that move by > 0.02), in and out of a hit stop.
  ladder  -- the glow's stack readout: the same frame with goreGlow forced to 0.2 / 0.5 / 0.8, diffed.
  controls that must FAIL -- drawn from outside in the EMISSIVE pass (a wrapper on drawSunTop, which runs
             there, over both fighters): ctrl1 the blade as LIGHT -- the same line from the guard to the point,
             60 wide, white, `lighter`, not clipped (light painted over the balls, CLAUDE.md 4.1b's class); ctrl2 a
             200-unit white radial wash on the blade's middle, `lighter` (the Harrowing's class, 4.1c: reach).
usage: gs_measure.py page out.json [foe seed side]... SCRATCH."""
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
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random, TAU = Math.PI * 2;
  const HAS = typeof r.drawGoreWeapon === "function";
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const u2d = () => r.k * r.scale;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  /* the priced blow's float, marked harness-side with the size it would have had */
  const rh = m.resolveHit;
  m.resolveHit = function(...args){
    const F0 = new Set(this.floats), T = me.priceTally, s0 = T ? T.stk : 0, b0 = T ? T.blows : 0;
    const out = rh.apply(this, args);
    const T2 = me.priceTally;
    if (T2 && T2.blows > b0 && T2.stk > s0){
      const n = T2.stk - s0;
      for (const x of this.floats) if (!F0.has(x) && args[0] === me){ x.__gs = x.size / (1 + 0.1 * n); x.__n = n; }
    }
    return out;
  };
  const ALL = ["drawGoreWeapon", "drawGoreDrops"];
  const blade = () => { const reach = me.w.reach * m.actMods.reach * me.reachMul, L = reach + 6;
    const a = me.theta + (me.bladeSet || me.w.blades)[0] * TAU, ca = Math.cos(a), sa = Math.sin(a);
    const x0 = me.x + ca * (R - 6 + L * 0.2), y0 = me.y + sa * (R - 6 + L * 0.2);
    const x1 = me.x + ca * (R - 6 + L), y1 = me.y + sa * (R - 6 + L);
    return { x0, y0, x1, y1, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 }; };
  const st0 = r.drawSunTop;
  const CTRL = {
    1: function(mm){ st0.call(this, mm);
         if (!(me.goreFade > 0)) return;
         const g = blade(), c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         c.strokeStyle = "#FFFFFF"; c.lineCap = "round"; c.lineWidth = 60; c.globalAlpha = 0.9;
         c.beginPath(); c.moveTo(g.x0, g.y0); c.lineTo(g.x1, g.y1); c.stroke();
         c.restore(); },
    2: function(mm){ st0.call(this, mm);
         if (!(me.goreFade > 0)) return;
         const g = blade(), c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const gr = c.createRadialGradient(g.cx, g.cy, 0, g.cx, g.cy, 200);
         gr.addColorStop(0, "#FFFFFF"); gr.addColorStop(0.5, "#FFF4D0"); gr.addColorStop(1, "#FFF4D000");
         c.globalAlpha = 0.9; c.fillStyle = gr;
         c.beginPath(); c.arc(g.cx, g.cy, 200, 0, TAU); c.fill(); c.restore(); },
  };
  /* one frame: `hide` = renderer method names shadowed; `reads` false = the priced float at its old size;
     `ctrl` = a control drawn in the emissive pass; `glow` = goreGlow forced */
  function frame(chain, hide, reads, ctrl, glow){
    const saved = [];
    for (const h of hide || []) if (typeof r[h] === "function"){ r[h] = function(){}; saved.push(h); }
    if (ctrl){ r.drawSunTop = CTRL[ctrl]; saved.push("drawSunTop"); }
    const sizes = [];
    if (reads === false) for (const x of m.floats) if (x.__gs){ sizes.push([x, x.size]); x.size = x.__gs; }
    const g0 = me.goreGlow;
    if (glow != null) me.goreGlow = glow;
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    const was = AC.POSTFX.on; AC.POSTFX.on = chain;
    try { AC.__draw(m); }
    finally { AC.POSTFX.on = was; Math.random = realRandom; m.shake = ks; me.goreGlow = g0;
              for (const [x, s] of sizes) x.size = s; for (const h of saved) delete r[h]; }
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
  function measure(st, extra){
    const out = Object.assign({ st, t: +m.t.toFixed(3), zt: me.ultPrice ? +me.ultPrice.t.toFixed(3) : null,
                  fade: +(me.goreFade || 0).toFixed(3), age: +(me.goreAge || 0).toFixed(3),
                  out: +(me.goreOut || 0).toFixed(3), glow: +(me.goreGlow || 0).toFixed(3),
                  stop: m.hitStop > 0, drops: (me.goreDrops || []).length, foeAff: th.aff.key, foeId: th.w.id, over: m.over,
                  stk: th.stacks("hemorrhage"), dFoe: +Math.hypot(th.x - me.x, th.y - me.y).toFixed(1),
                  reads: m.floats.filter(x => x.__gs).length }, extra || {});
    const onW = frame(true), offW = frame(false), onO = frame(true, ALL, false), offO = frame(false, ALL, false);
    const aW = arena(onW), aWo = arena(offW), aO = arena(onO), aOo = arena(offO);
    out.arena = { onW: aW.mean, offW: aWo.mean, onO: aO.mean, offO: aOo.mean, liftW: aW.mean - aWo.mean, liftO: aO.mean - aOo.mean,
                  dLift: (aW.mean - aWo.mean) - (aO.mean - aOo.mean), picOn: aW.mean - aO.mean, clipW: aW.clip, clipO: aO.clip };
    out.disc = { me: { W: disc(onW, me), O: disc(onO, me), cW: contour(onW, me), cO: contour(onO, me) },
                 foe: { W: disc(onW, th), O: disc(onO, th), cW: contour(onW, th), cO: contour(onO, th) } };
    out.all = comp(onW, onO);
    const comps = { pic: ["drawGoreWeapon"], glow: ["_goreGlow"], steel: ["_goreSteel"], front: ["_goreFront"],
                    drops: ["drawGoreDrops"] };
    for (const [k, hs] of Object.entries(comps)){
      const h = frame(true, hs); out[k] = comp(onW, h);
      out[k].meDisc = disc(onW, me).mean - disc(h, me).mean; out[k].foeDisc = disc(onW, th).mean - disc(h, th).mean;
    }
    out.reads = comp(onW, frame(true, [], false));
    /* the caster's weapon against the floor, with the picture and with it all hidden */
    const dw = r.drawWeapon;
    r.drawWeapon = function(mm, f){ if (f !== me) return dw.call(this, mm, f); };
    let noWep, noWepO;
    try { noWep = frame(true); noWepO = frame(true, ALL, false); } finally { r.drawWeapon = dw; }
    out.weapon = comp(onW, noWep);
    out.weaponBase = comp(onO, noWepO);
    /* the glow's ladder: what the stacks change, on this frame (the window up) */
    if (me.goreFade > 0 && !(me.goreOut > 0)){
      const g2 = frame(true, [], true, 0, 0.2), g5 = frame(true, [], true, 0, 0.5), g8 = frame(true, [], true, 0, 0.8);
      out.ladder = { d28: comp(g8, g2), d25: comp(g5, g2), d58: comp(g8, g5) };
    }
    /* the ART on the discs, the picture's readout held out */
    const artW = frame(true, [], false);
    out.artDisc = { me: disc(artW, me).mean - disc(onO, me).mean, foe: disc(artW, th).mean - disc(onO, th).mean,
                    meClip: disc(artW, me).clip, foeClip: disc(artW, th).clip };
    for (const c of [1, 2]){
      const cW = frame(true, [], true, c), cWo = frame(false, [], true, c);
      const ac = arena(cW), aco = arena(cWo);
      out["ctrl" + c] = { dLift: (ac.mean - aco.mean) - (aO.mean - aOo.mean), picOn: ac.mean - aO.mean, clip: ac.clip,
                          me: disc(cW, me), foe: disc(cW, th), foeC: contour(cW, th) };
    }
    return out;
  }
  const out = { foe, seed, side, has: HAS, got: {}, missing: [] };
  const left = new Set(want);
  let step = 0, overAt = -1, upAtOver = false, closeAt = -1, prevZ = null, seenBl = 0, seenStk = 0, blowAt = -1, blowN = 0;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (step < 200 / DT && left.size){
    m.step(DT); step++;
    if (m.over){
      if (overAt < 0){ overAt = step; upAtOver = me.goreFade > 0; }
      if (left.has("over") && upAtOver && step - overAt === 12){ left.delete("over"); out.got.over = measure("over"); }
      if (step - overAt > 60) break;
      continue;
    }
    const Z = me.ultPrice, T = me.priceTally;
    if (T){ if (T.blows > seenBl && T.stk > seenStk){ blowAt = step; blowN = T.stk - seenStk; } seenBl = T.blows; seenStk = T.stk; }
    if (!Z && prevZ && me.alive && th.alive) closeAt = step;
    prevZ = Z;
    if (r.scrunchK && r.scrunchK(m) < 0.999) continue;
    const clean = m.hitStop <= 0 && !(me.flash > 0) && th.alive;
    const near = Math.hypot(th.x - me.x, th.y - me.y) < 300;
    const sk = th.stacks("hemorrhage");
    let st = null, extra = null;
    if (left.has("rest") && !Z && m.t > 3 && clean && inHall(me, 120) && !(me.goreFade > 0) && !m.ultFx) st = "rest";
    else if (left.has("cast") && Z && me.goreAge > 0.02 && me.goreAge < 0.08 && m.hitStop > 0) st = "cast";
    else if (left.has("run") && Z && me.goreAge > 0.3 && me.goreAge < 0.42) st = "run";
    else if (left.has("win0") && Z && Z.t > 0.8 && clean && near && sk === 0 && me.goreGlow < 0.22) st = "win0";
    else if (left.has("win2") && Z && Z.t > 0.8 && clean && near && sk === 2 && Math.abs(me.goreGlow - 0.5) < 0.02) st = "win2";
    else if (left.has("win4") && Z && Z.t > 0.8 && clean && near && sk >= 4 && me.goreGlow > 0.78) st = "win4";
    else if (left.has("stop") && Z && m.hitStop > 0 && Z.t > 0.5 && blowAt !== step) st = "stop";
    else if (left.has("blow") && blowAt === step && th.alive){ st = "blow"; extra = { n: blowN }; }
    else if (left.has("blow2") && blowAt >= 0 && step - blowAt === 10 && th.alive){ st = "blow2"; extra = { n: blowN }; }
    else if (left.has("close") && closeAt >= 0 && step - closeAt === 12) st = "close";
    if (!st) continue;
    left.delete(st);
    out.got[st] = measure(st, extra);
  }
  out.missing = Array.from(left);
  return out;
}"""

FIGHTS = [("aureole", 4101, "a"), ("dawnbringer", 99001, "a"), ("gravemourn", 99015, "a"), ("twinshade", 99008, "a"),
          ("gloamwire", 5150, "b"), ("spellbreaker", 99015, "a"), ("marrowdraw", 2207, "a"), ("farwarden", 31337, "b"),
          ("grudgebearer", 31337, "a")]
WANT = os.environ.get("GS_WANT", "rest,cast,run,win0,win2,win4,stop,blow,blow2,close,over").split(",")
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
