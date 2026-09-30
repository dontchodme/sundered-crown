"""THE GATES on real fights, on the DELIVERED look (sb-final-fx.html = the base + the rows, SPECS.spellbreaker out of the
inlined fx.js as the carry takes it out; or any page given). No lab variant: a component is hidden by shadowing its
renderer method on the instance from outside the page (`r[name] = () => {}`; the grey by `_unmkGreyed` -> false), and the
+2 the picture writes on a tag is held out by putting the tag's `val` back to 0 for that frame (harness-side).
540x960, chain on/off, shake zeroed, Math.random pinned per frame.
  bloom   -- the picture's share of the post chain's arena lift: (lift with the picture) - (lift with it all hidden),
             per frame; and the raw luma it adds.
  discs   -- caster and foe disc mean luma / clip with and without the picture, and the art alone (tags out).
  legib.  -- |dL| per component (hide one, diff; the pixels whose luma OR chroma moves by > 0.02), with the chroma
             change |dC| beside it (the grey is a colour change), in and out of a hit stop.
  controls that must FAIL, each drawn from outside into the EMISSIVE pass (a wrapper on drawSunTop, which the
             base calls there, over both fighters): ctrl1 the grey as LIGHT -- a filled white `lighter` disc of the
             foe's reach at 0.35 over a greyed weapon (the Harrowing's class: reach, not alpha); ctrl2 the script as a
             white-hot `lighter` glow on the caster (Daybreak's class: light over a body); ctrl3 a white `lighter`
             disc over the foe's ball while greyed (erasing it).
usage: measure.py page out.json [foe seed side]... SCRATCH."""
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
  const m = side === "a" ? new AC.Match("spellbreaker", foe, seed) : new AC.Match(foe, "spellbreaker", seed);
  const me = m.a.w.id === "spellbreaker" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random, TAU = Math.PI * 2;
  const HAS = typeof m.tickUnmaking === "function";
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const u2d = () => r.k * r.scale;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const ALL = ["drawUnmaking", "_unmkScript", "_unmkGreyed"];
  const st_ = r.drawSunTop;
  const reachOf = (f) => f.w.reach * m.actMods.reach * f.reachMul + R;
  const CTRL = {
    1: function(mm){ st_.call(this, mm);
         if (!(th.unmkGrey > 0) || !th.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         c.globalAlpha = 0.35; c.fillStyle = "#FFFFFF";
         c.beginPath(); c.arc(th.x, th.y, reachOf(th), 0, TAU); c.fill(); c.restore(); },
    2: function(mm){ st_.call(this, mm);
         if (!(me.unmkFade > 0) || !me.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const g = c.createRadialGradient(me.x, me.y, 0, me.x, me.y, R * 1.8);
         g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.6, "#DDEEFF"); g.addColorStop(1, "#DDEEFF00");
         c.globalAlpha = 0.9 * me.unmkFade; c.fillStyle = g;
         c.beginPath(); c.arc(me.x, me.y, R * 1.8, 0, TAU); c.fill(); c.restore(); },
    3: function(mm){ st_.call(this, mm);
         if (!(th.unmkGrey > 0) || !th.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         c.globalAlpha = 0.8; c.fillStyle = "#FFFFFF";
         c.beginPath(); c.arc(th.x, th.y, R + 4, 0, TAU); c.fill(); c.restore(); },
  };
  const HIDEF = { _unmkGreyed: function(){ return false; } };
  function frame(chain, hide, tags, ctrl){
    const saved = [];
    for (const h of hide || []) if (typeof r[h] === "function"){ r[h] = HIDEF[h] || function(){}; saved.push(h); }
    if (ctrl){ r.drawSunTop = CTRL[ctrl]; saved.push("drawSunTop"); }
    const put = [];
    if (tags === false) for (const g of m.tags) if (g.unmk){ put.push([g, g.val]); g.val = 0; }
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    const was = AC.POSTFX.on; AC.POSTFX.on = chain;
    try { AC.__draw(m); }
    finally { AC.POSTFX.on = was; Math.random = realRandom; m.shake = ks; for (const [g, v] of put) g.val = v; for (const h of saved) delete r[h]; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data);
  }
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  const C = (d, i) => (Math.max(d[i], d[i+1], d[i+2]) - Math.min(d[i], d[i+1], d[i+2])) / 255;
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
    let n = 0, s = 0, pk = 0, sc = 0;
    for (let i = 0; i < dw.length; i += 4){
      const dl = L(dw, i) - L(dh, i), dc = C(dw, i) - C(dh, i);
      if (Math.abs(dl) < 0.02 && Math.abs(dc) < 0.02) continue;
      n++; s += Math.abs(dl); sc += Math.abs(dc); if (Math.abs(dl) > pk) pk = Math.abs(dl); }
    return { n, dL: n ? s / n : 0, dC: n ? sc / n : 0, peak: pk, areaU: n / (u2d() * u2d()) };
  }
  function measure(st){
    const tagN = m.tags.filter(g => g.unmk).length;
    const out = { st, t: +m.t.toFixed(3), zt: me.ultUnmake ? +me.ultUnmake.t.toFixed(3) : null,
                  fade: +(me.unmkFade || 0).toFixed(3), age: +(me.unmkAge || 0).toFixed(3), motes: me.unmkMotes ? me.unmkMotes.length : 0,
                  greyLeft: +(th.unmkGrey || 0).toFixed(4), stun: +th.stun.toFixed(4), d: +Math.hypot(th.x - me.x, th.y - me.y).toFixed(1),
                  stop: m.hitStop > 0, foeHex: th.stacks("hex"), foeAff: th.aff.key, foe: th.w.id,
                  over: m.over, meAlive: me.alive, foeAlive: th.alive, utags: tagN };
    const onW = frame(true), offW = frame(false), onO = frame(true, ALL, false), offO = frame(false, ALL, false);
    const aW = arena(onW), aWo = arena(offW), aO = arena(onO), aOo = arena(offO);
    out.arena = { onW: aW.mean, offW: aWo.mean, onO: aO.mean, offO: aOo.mean, liftW: aW.mean - aWo.mean, liftO: aO.mean - aOo.mean,
                  dLift: (aW.mean - aWo.mean) - (aO.mean - aOo.mean), picOn: aW.mean - aO.mean, clipW: aW.clip, clipO: aO.clip };
    out.disc = { me: { W: disc(onW, me), O: disc(onO, me), cW: contour(onW, me), cO: contour(onO, me) },
                 foe: { W: disc(onW, th), O: disc(onO, th), cW: contour(onW, th), cO: contour(onO, th) } };
    out.all = comp(onW, onO);
    const comps = { motes: ["drawUnmaking"], script: ["_unmkScript"], grey: ["_unmkGreyed"] };
    for (const [k, hs] of Object.entries(comps)){
      const h = frame(true, hs); out[k] = comp(onW, h);
      out[k].meDisc = disc(onW, me).mean - disc(h, me).mean; out[k].foeDisc = disc(onW, th).mean - disc(h, th).mean;
    }
    out.tag = comp(onW, frame(true, [], false));
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
  let step = 0, overAt = -1, liveAtOver = false, closeAt = -1, prevZ = null, casts = 0, x0 = 0, tagAt = -1;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (step < 200 / DT && left.size){
    m.step(DT); step++;
    if (m.over){
      if (overAt < 0){ overAt = step; liveAtOver = !!me.ultUnmake || (me.unmkFade > 0); }
      if (left.has("over") && liveAtOver && step - overAt === 12){ left.delete("over"); out.got.over = measure("over"); }
      if (step - overAt > 60) break;
      continue;
    }
    const Z = me.ultUnmake, T = me.unmakeTally;
    if (Z && !prevZ) casts++;
    if (!Z && prevZ && me.alive && th.alive) closeAt = step;
    prevZ = Z;
    if (T && T.extra > x0){ x0 = T.extra; tagAt = step; }
    if (r.scrunchK && r.scrunchK(m) < 0.999) continue;
    const clean = m.hitStop <= 0 && !(me.flash > 0) && !(th.flash > 0) && th.alive;
    let st = null;
    if (left.has("rest") && !Z && casts === 0 && m.t > 3 && clean && inHall(me, 90) && !m.ultFx) st = "rest";
    else if (left.has("cast") && Z && me.unmkAge > 0.08 && me.unmkAge < 0.2) st = "cast";
    else if (left.has("write") && Z && me.unmkAge > 0.3 && me.unmkAge < 0.45 && m.hitStop <= 0) st = "write";
    else if (left.has("open") && Z && Z.t > 1 && clean && !(th.unmkGrey > 0) && inHall(me, 90)) st = "open";
    else if (left.has("grey") && Z && th.unmkGrey > 0.12 && clean && inHall(th, 90)) st = "grey";
    else if (left.has("greystop") && th.unmkGrey > 0.1 && m.hitStop > 0) st = "greystop";
    else if (left.has("tag") && tagAt > 0 && step - tagAt === 2 && m.tags.some(g => g.unmk)) st = "tag";
    else if (left.has("stop") && Z && m.hitStop > 0 && Z.t > 0.5 && !(th.unmkGrey > 0)) st = "stop";
    else if (left.has("close") && closeAt >= 0 && step - closeAt >= 6 && step - closeAt <= 20 && m.hitStop <= 0 && me.unmkFade > 0) st = "close";
    if (!st) continue;
    left.delete(st);
    out.got[st] = measure(st);
  }
  out.missing = Array.from(left);
  return out;
}"""

FIGHTS = [("dawnbringer", 99001, "a"), ("lastlight", 4242, "b"), ("aureole", 4101, "a"), ("morningstar", 8888, "b"),
          ("gravemourn", 99015, "b"), ("nightfell", 5150, "a"), ("twinshade", 99008, "a"),
          ("grudgebearer", 31337, "a"), ("heartwood", 2207, "a"), ("censer", 4101, "b")]
WANT = os.environ.get("SB_WANT", "rest,cast,write,open,grey,greystop,tag,stop,close,over").split(",")
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
