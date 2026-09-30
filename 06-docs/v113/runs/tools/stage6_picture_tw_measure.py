"""THE GATES on real fights, on the DELIVERED look (tw-final-fx.html = the base + the rows, SPECS.thornwake out of
the inlined fx.js as the carry takes it out; or any page given). No lab variant: a component is hidden by shadowing
its renderer method on the instance from outside the page (`r[name] = () => {}`), and the tags the picture prints are
held out by marking what `tickBrier` pushes (a wrapper on the match instance, harness-side).
540x960, chain on/off, shake zeroed, Math.random pinned per frame.
  bloom   -- the picture's share of the post chain's arena lift: (lift with the picture) - (lift with it all hidden),
             per frame; the FLOOR's share alone (drawBrier hidden vs shown); and the raw luma the picture adds.
  discs   -- caster and foe disc mean luma / clip with and without the picture, and the art alone (tags out).
  legib.  -- |dL| per component (hide one, diff; the pixels that move by > 0.02), in and out of a hit stop.
  controls that must FAIL, each drawn from outside into the EMISSIVE pass (a wrapper on drawSunTop, which the base
             calls there, over both fighters):
             ctrl1 (TW_C1, default "wash") a white `lighter` radial wash r 300 at every bramble -- the Harrowing's class,
                   reach and not alpha. The two weaker forms are kept as data: "disc", every bramble a filled white disc
                   at 0.9 at its test radius (m1 at 0.35 r 80: +0.014; m2: +0.012 -- a large flat white raises the frame
                   mean and the bloom's adaptation damps it, CLAUDE.md 4.1d), and "tangle", the picture's own canes
                   stroked white in the emissive pass (+0.004: thin strokes, little area);
             ctrl2 the blade's green as a white-hot `lighter` glow over the caster (Daybreak's class: light over a
                   body);
             ctrl3 the snare as a filled white `lighter` disc over the held foe.
usage: tw_measure.py page out.json [foe seed side]... SCRATCH."""
import sys, json, pathlib, os
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
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

SEEK = r"""([foe, seed, side, want, C1]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("thornwake", foe, seed) : new AC.Match(foe, "thornwake", seed);
  const me = m.a.w.id === "thornwake" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const mySide = me === m.a ? "a" : "b";
  const realRandom = Math.random, TAU = Math.PI * 2;
  const HAS = typeof m.tickBrier === "function";
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const u2d = () => r.k * r.scale;
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  /* the tags the picture prints, marked harness-side */
  if (HAS){
    const tq = m.tickBrier;
    m.tickBrier = function(dt){
      const before = new Set(this.tags);
      tq.call(this, dt);
      for (const g of this.tags) if (!before.has(g)) g.__brier = true;
    };
  }
  const ALL = ["drawBrier", "drawBrierTop", "_brierBlade"];
  const st_ = r.drawSunTop;
  const PR = me.w.ult.patchR, PL = me.w.ult.patchLife;
  const mine = () => m.brambles.filter(b => b.side === mySide);
  const CTRL = {
    1: function(mm){ st_.call(this, mm);
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         if (C1 === "tangle"){
           for (const p of me.brierPic) this._brierTangle(c, { x: p.b.x, y: p.b.y, R: PR, k: 1, A: 2, g: p.g, dk: "#FFFFFF", sm: "#FFFFFF" });
         } else if (C1 === "wash"){
           for (const b of mine()){ const g = c.createRadialGradient(b.x, b.y, 0, b.x, b.y, 300);
             g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.35, "#FFFFFFAA"); g.addColorStop(1, "#FFFFFF00");
             c.globalAlpha = 1; c.fillStyle = g; c.beginPath(); c.arc(b.x, b.y, 300, 0, TAU); c.fill(); }
         } else {
           c.globalAlpha = 0.9; c.fillStyle = "#FFFFFF";
           for (const b of mine()){ c.beginPath(); c.arc(b.x, b.y, PR + R, 0, TAU); c.fill(); }
         }
         c.restore(); },
    2: function(mm){ st_.call(this, mm);
         if (!(me.brierGreen > 0) || !me.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         const g = c.createRadialGradient(me.x, me.y, 0, me.x, me.y, R * 1.8);
         g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.6, "#F2FFF4"); g.addColorStop(1, "#F2FFF400");
         c.globalAlpha = 0.9 * me.brierGreen; c.fillStyle = g;
         c.beginPath(); c.arc(me.x, me.y, R * 1.8, 0, TAU); c.fill(); c.restore(); },
    3: function(mm){ st_.call(this, mm);
         if (!(th.brierRootFade > 0) || !th.alive) return;
         const c = this.ctx; c.save(); c.globalCompositeOperation = "lighter";
         c.globalAlpha = th.brierRootFade; c.fillStyle = "#FFFFFF";
         c.beginPath(); c.arc(th.x, th.y, R + 7, 0, TAU); c.fill(); c.restore(); },
  };
  function frame(chain, hide, tags, ctrl){
    const saved = [];
    for (const h of hide || []) if (typeof r[h] === "function"){ r[h] = function(){}; saved.push(h); }
    if (ctrl){ r.drawSunTop = CTRL[ctrl]; saved.push("drawSunTop"); }
    const G = m.tags;
    if (tags === false) m.tags = G.filter(g => !g.__brier);
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
    const G = mine();
    const out = { st, t: +m.t.toFixed(3), zt: me.ultBramble ? +me.ultBramble.t.toFixed(3) : null,
                  green: +(me.brierGreen || 0).toFixed(3), age: +(me.brierAge || 0).toFixed(3),
                  held: th.brierHeld || 0, heldAge: +(th.brierHeldAge || 0).toFixed(3), rootFade: +(th.brierRootFade || 0).toFixed(3),
                  bites: (me.brierBite || []).length, brambles: G.length, inside: !!me.brambleIn,
                  bAge: G.map(b => +(m.brambleT - b.t0).toFixed(2)), pic: (me.brierPic || []).map(p => +p.age.toFixed(2)),
                  stop: m.hitStop > 0, foeEnt: th.stacks("entangle"), foeAff: th.aff.key, foe: th.w.id, meAff: me.aff.key,
                  over: m.over, meAlive: me.alive, foeAlive: th.alive,
                  btags: m.tags.filter(g => g.__brier).length };
    const onW = frame(true), offW = frame(false), onO = frame(true, ALL, false), offO = frame(false, ALL, false);
    const aW = arena(onW), aWo = arena(offW), aO = arena(onO), aOo = arena(offO);
    const onG = frame(true, ["drawBrier"]), offG = frame(false, ["drawBrier"]);
    const aG = arena(onG), aGo = arena(offG);
    out.arena = { onW: aW.mean, offW: aWo.mean, onO: aO.mean, offO: aOo.mean, liftW: aW.mean - aWo.mean, liftO: aO.mean - aOo.mean,
                  dLift: (aW.mean - aWo.mean) - (aO.mean - aOo.mean), picOn: aW.mean - aO.mean, clipW: aW.clip, clipO: aO.clip,
                  floorLift: (aW.mean - aWo.mean) - (aG.mean - aGo.mean), floorRaw: aWo.mean - aGo.mean };
    out.disc = { me: { W: disc(onW, me), O: disc(onO, me), cW: contour(onW, me), cO: contour(onO, me) },
                 foe: { W: disc(onW, th), O: disc(onO, th), cW: contour(onW, th), cO: contour(onO, th) } };
    out.all = comp(onW, onO);
    const comps = { floor: ["drawBrier"], shade: ["_brierShade"], tangle: ["_brierTangle"], motes: ["_brierMotes"],
                    root: ["_brierRoot"], top: ["drawBrierTop"], bite: ["_brierBite"], blade: ["_brierBlade"] };
    for (const [k, hs] of Object.entries(comps)){
      const h = frame(true, hs); out[k] = comp(onW, h);
      out[k].meDisc = disc(onW, me).mean - disc(h, me).mean; out[k].foeDisc = disc(onW, th).mean - disc(h, th).mean;
    }
    out.tag = comp(onW, frame(true, [], false));
    const artW = frame(true, [], false);
    out.artDisc = { me: disc(artW, me).mean - disc(onO, me).mean, foe: disc(artW, th).mean - disc(onO, th).mean,
                    meClip: disc(artW, me).clip, foeClip: disc(artW, th).clip, meO: disc(onO, me).mean, foeO: disc(onO, th).mean };
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
  let step = 0, overAt = -1, liveAtOver = false, closeAt = -1, prevZ = null, casts = 0, tickAt = -1, lastTicks = 0;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (step < 200 / DT && left.size){
    m.step(DT); step++;
    if (m.over){
      if (overAt < 0){ overAt = step; liveAtOver = mine().length > 0 || (me.brierGreen > 0); }
      if (left.has("over") && liveAtOver && step - overAt === 12){ left.delete("over"); out.got.over = measure("over"); }
      if (step - overAt > 60) break;
      continue;
    }
    const Z = me.ultBramble, T = me.brambleTally;
    if (Z && !prevZ) casts++;
    if (!Z && prevZ && me.alive && th.alive) closeAt = step;
    prevZ = Z;
    if (T && T.ticks > lastTicks){ tickAt = step; lastTicks = T.ticks; }
    if (r.scrunchK && r.scrunchK(m) < 0.999) continue;
    const G = mine();
    const pn = me.brierPic && me.brierPic.length ? me.brierPic[me.brierPic.length - 1] : null;
    const clean = m.hitStop <= 0 && !(me.flash > 0) && !(th.flash > 0) && th.alive;
    const young = G.some(b => m.brambleT - b.t0 > PL - 1.2);
    let st = null;
    if (left.has("rest") && !Z && casts === 0 && m.t > 3 && clean && inHall(me, 100) && !m.ultFx) st = "rest";
    else if (left.has("cast") && Z && me.brierAge > 0.08 && me.brierAge < 0.2) st = "cast";
    else if (left.has("green") && Z && me.brierAge > 0.3 && me.brierAge < 0.45 && m.hitStop <= 0) st = "green";
    else if (left.has("plant") && pn && pn.age > 0.2 && pn.age < 0.45) st = "plant";
    else if (left.has("off") && Z && Z.t > 1 && clean && G.length && !me.brambleIn && !(th.brierRootFade > 0) && !young) st = "off";
    else if (left.has("in") && Z && Z.t > 1 && clean && me.brambleIn && !(th.brierRootFade > 0) && !(me.brierBite.length)) st = "in";
    else if (left.has("snare") && th.brierHeld && th.brierHeldAge > 0.5 && th.brierHeldAge < 0.7 && m.hitStop <= 0) st = "snare";
    else if (left.has("bite") && tickAt > 0 && step - tickAt === 2 && m.hitStop <= 0 && th.alive) st = "bite";
    else if (left.has("stop") && Z && m.hitStop > 0 && Z.t > 0.5 && G.length && me.brambleIn) st = "stop";
    else if (left.has("stopoff") && Z && m.hitStop > 0 && Z.t > 0.5 && G.length && !me.brambleIn) st = "stopoff";
    else if (left.has("close") && closeAt >= 0 && step - closeAt >= 12 && step - closeAt <= 30 && m.hitStop <= 0 && me.brierGreen > 0) st = "close";
    else if (left.has("after") && !Z && closeAt >= 0 && step - closeAt > 90 && G.length && clean) st = "after";
    else if (left.has("brown") && G.some(b => PL - (m.brambleT - b.t0) < 0.6 && PL - (m.brambleT - b.t0) > 0.3) && clean) st = "brown";
    if (!st) continue;
    left.delete(st);
    out.got[st] = measure(st);
  }
  out.missing = Array.from(left);
  return out;
}"""

FIGHTS = [("aureole", 4101, "a"), ("gravemourn", 99015, "a"), ("grudgebearer", 31337, "b"), ("dawnbringer", 99001, "a"),
          ("nightfell", 5150, "b"), ("lastlight", 4242, "b"), ("morningstar", 8888, "a"), ("shroudmaul", 1234, "b"),
          ("paradox", 2317, "b"), ("censer", 2207, "b")]
WANT = os.environ.get("TW_WANT", "rest,cast,green,plant,off,in,snare,bite,stop,stopoff,close,after,brown,over").split(",")
if __name__ == "__main__":
    page_ = pathlib.Path(sys.argv[1]); page_ = page_ if page_.is_absolute() else HERE / page_
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "m1.json"
    out = out if out.is_absolute() else HERE / out
    fights = FIGHTS if len(sys.argv) <= 3 else [(sys.argv[i], int(sys.argv[i + 1]), sys.argv[i + 2]) for i in range(3, len(sys.argv), 3)]
    res = []
    with game(game_path=page_) as (page, errors):
        page.evaluate(SETUP, [[540, 960]])
        for foe, seed, side in fights:
            r = page.evaluate(SEEK, [foe, seed, side, WANT, os.environ.get("TW_C1", "wash")])
            assert not errors, errors[:3]
            res.append(r)
            print(foe, seed, side, "got", list(r["got"]), "missing", r["missing"], flush=True)
            out.write_text(json.dumps(res, indent=1))
