#!/usr/bin/env python
"""DAYBREAK'S CIRCLE, IN PIXELS -- the stage-3 picture gates, legibility FIRST.

    python sunrise_sheet.py --game ../02-chain/sc-sunrise-fx.html \
        [--sheet ../05-reference/v99/sunrise-states.png] [--json out.json]

Everything is measured on REAL FIGHTS, 540x960, through the shipped renderer,
with the camera shake zeroed and Math.random pinned for every draw, from TWO
FRAMES THAT DIFFER ONLY IN THE MARK (the mark's draw call stubbed on the
renderer for the second one) -- v88 §6c's method. Dawnbringer against a runic
foe (Spellbreaker), the white Aureole and Grudgebearer, the brief's three.

LEGIBILITY (v99 brief stage 3), each able to fail:
  [L1] the wash: mean luma over the sun's disc minus the bare floor >= +0.15
       at the hold (the line measured +0.085 and failed Rick's eye)
  [L2] the rim: band luma >= 0.50, and the step from just inside it to just
       outside its halo >= 0.12, at every angle a wall, a ball, a blade, a shot
       or a word does not cover, on every hold frame with >= 6 such angles
       (fewer is not enough to judge, and is not counted either way). THE STEP IS THE SUN'S OWN LIGHT (the frame minus the same
       frame without the sun), because a real fight puts other things just
       outside the rim -- a foe's ultimate, arrows, a white ball's glow -- and
       raw luma there reads their light as the rim failing
  [L3] the rays: marks, not a disc -- mean |dL| over their footprint >= 0.05,
       and at radius 60-110 they cover under 60% of the circle
  [L4] the tick's number reads at least as well as Corollary's echo number
       (mean |dL| over the number's footprint, both drawn on the same frame
       over the same foe)
  [L5] the break's flash is gone by 0.3s of match time (frames counted)
  [L6] the armed edge-light draws on every armed frame and on no other -- a
       frame whose blade points into a wall, the tell's whole span past the
       hall's edge where nothing is drawn, is not a frame it could draw on
THE BLOOM (the old gates, measured after):
  [B1] the sun's share of the arena-mean bloom lift <= +0.02 with the sun fully
       up (180 frames: six foes, both sides, the hold)
  [B2] the sun never takes a ball's disc above 0.90 on any frame, the white
       Aureole standing on the core and the break's flash included. A disc over
       0.90 that is over 0.90 WITHOUT any of the sun's marks is the ball's own
       (a blow's hit flash, a ward) and is reported, not charged to the sun
  [B3] the wash does not touch a ball (max disc change 0.00) and is the same
       light with the chain off (none of it is bloom)
"""
from __future__ import annotations
import argparse, base64, io, json, pathlib, sys, time
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-sunrise-fx.html")
ap.add_argument("--sheet", default=None, help="write the filmstrip here")
ap.add_argument("--sheet-foe", default="grudgebearer")
ap.add_argument("--json", default=None)
ap.add_argument("--bloom-frames", type=int, default=15, help="per foe and side")
ap.add_argument("--only", default="leg,timing,bloom,core,sheet")
ap.add_argument("--rim-frames", type=int, default=6, help="hold frames a foe for the rim")
a = ap.parse_args()

LEG_FOES = ["spellbreaker", "aureole", "grudgebearer"]
BLOOM_FOES = ["spellbreaker", "aureole", "grudgebearer", "ironhail", "paradox", "heartwood"]

LIB = r"""
window.SUNLAB = (() => {
  const R = AC.renderer, cv = document.getElementById('cv'), ctx = cv.getContext('2d');
  const C = AC.CONFIG, BR = C.physics.ballR;
  const real = Math.random;
  const pin = () => { let s = 0x5EEDF00D | 0; Math.random = () => { s = (s + 0x6D2B79F5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  function draw(m, chain, stubs){
    const saved = {};
    for (const k of (stubs || [])){ saved[k] = true; R[k] = function(){}; }
    const was = AC.POSTFX.on;
    AC.POSTFX.on = !!chain;
    m.shake = 0; pin();
    try { AC.__draw(m); }
    finally { Math.random = real; AC.POSTFX.on = was; for (const k in saved) delete R[k]; }
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    const L = new Float32Array(cv.width * cv.height);
    for (let i = 0, j = 0; j < L.length; i += 4, j++)
      L[j] = (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 255;
    return L;
  }
  const W = () => cv.width, Hh = () => cv.height;
  const toDev = (x, y) => [R.k * (R.pad + R.scale * x), R.k * (R.arenaTop + R.scale * y)];
  const toArena = (px, py) => [(px / R.k - R.pad) / R.scale, (py / R.k - R.arenaTop) / R.scale];
  function disc(L, f){
    const [cx, cy] = toDev(f.x, f.y), rr = BR * R.scale * R.k * 0.92;
    let s = 0, n = 0;
    for (let y = Math.max(0, Math.floor(cy - rr)); y <= Math.min(Hh() - 1, Math.ceil(cy + rr)); y++)
      for (let x = Math.max(0, Math.floor(cx - rr)); x <= Math.min(W() - 1, Math.ceil(cx + rr)); x++){
        if (Math.hypot(x - cx, y - cy) > rr) continue;
        s += L[y * W() + x]; n++;
      }
    return n ? s / n : 0;
  }
  function arenaMean(L){
    const [x0, y0] = toDev(0, 0), [x1, y1] = toDev(C.arena.w, C.arena.h);
    let s = 0, n = 0;
    for (let y = Math.max(0, Math.round(y0)); y < Math.min(Hh(), Math.round(y1)); y++)
      for (let x = Math.max(0, Math.round(x0)); x < Math.min(W(), Math.round(x1)); x++){ s += L[y * W() + x]; n++; }
    return s / n;
  }
  /* pixels of the arena, with their arena coordinates, inside a live hall */
  function eachPx(m, fn){
    const n = m.inset || 0, A = C.arena;
    const [x0, y0] = toDev(n, n), [x1, y1] = toDev(A.w - n, A.h - n);
    for (let py = Math.max(0, Math.ceil(y0)); py < Math.min(Hh(), Math.floor(y1)); py++)
      for (let px = Math.max(0, Math.ceil(x0)); px < Math.min(W(), Math.floor(x1)); px++){
        const [x, y] = toArena(px + 0.5, py + 0.5);
        fn(py * W() + px, x, y);
      }
  }
  const SUNPARTS = ["_sunRays", "_sunEmbers", "_sunRim", "_sunCore"];
  /* the WASH (only the wash drawn) against the bare floor, over the disc
     minus the balls, the core and the rim band */
  function washLift(m, f){
    const S = f.ultSunrise, r = f.w.ult.r * Math.min(1, S.t / f.w.ult.grow);
    const Lw = draw(m, true, SUNPARTS), Lb = draw(m, true, ["drawSunrise", "drawSunriseBlade"]);
    const Lw0 = draw(m, false, SUNPARTS), Lb0 = draw(m, false, ["drawSunrise", "drawSunriseBlade"]);
    let s = 0, s0 = 0, n = 0;
    eachPx(m, (i, x, y) => {
      const d = Math.hypot(x - S.x, y - S.y);
      if (d > r - 8 || d < 20) return;
      for (const g of [m.a, m.b]) if (g.alive && Math.hypot(x - g.x, y - g.y) < BR + 10) return;
      s += Lw[i] - Lb[i]; s0 += Lw0[i] - Lb0[i]; n++;
    });
    return { on: n ? s / n : 0, off: n ? s0 / n : 0, n };
  }
  /* THE RIM at 72 angles: band luma, and the step from inside to outside */
  function rim(m, f, L, Lb){
    const S = f.ultSunrise, r = f.w.ult.r * Math.min(1, S.t / f.w.ult.grow);
    const bins = Array.from({ length: 72 }, () => ({ band: [0, 0], ins: [0, 0], out: [0, 0], bad: false }));
    const n = m.inset || 0, A = C.arena;
    /* a bin is unusable if any of its sample points sits outside the live
       hall, near a ball, or near a float/tag (text) */
    const words = m.floats.map(q => [q.x, q.y]).concat(m.tags.map(q => [q.x, q.y + 50]));
    /* and anything drawn OVER the sun at that angle: a blade (Dawnbringer's
       own greatsword lies across the rim, and the step there reads ~0 because
       the sun is covered, not because it is dim), a shot, a shade */
    const segs = [];
    for (const g of [m.a, m.b]) if (g.alive) for (const sg of m.bladeSegments(g)) segs.push(sg);
    const segD = (x, y, sg) => { const dx = sg.bx - sg.ax, dy = sg.by - sg.ay, l2 = dx * dx + dy * dy;
      let t = l2 ? ((x - sg.ax) * dx + (y - sg.ay) * dy) / l2 : 0; t = Math.max(0, Math.min(1, t));
      return Math.hypot(x - sg.ax - t * dx, y - sg.ay - t * dy); };
    const objs = (m.shots || []).map(q => [q.x, q.y]).concat((m.shades || []).map(q => [q.x, q.y]));
    for (let k = 0; k < 72; k++){
      const an = (k + 0.5) * Math.PI * 2 / 72;
      for (const rr of [r - 14, r - 8, r, r + 14, r + 21]){
        const x = S.x + Math.cos(an) * rr, y = S.y + Math.sin(an) * rr;
        if (x < n + 4 || x > A.w - n - 4 || y < n + 4 || y > A.h - n - 4) bins[k].bad = true;
        for (const g of [m.a, m.b]) if (g.alive && Math.hypot(x - g.x, y - g.y) < BR + 26) bins[k].bad = true;
        for (const [wx, wy] of words) if (Math.hypot(x - wx, y - wy) < 70) bins[k].bad = true;
        for (const sg of segs) if (segD(x, y, sg) < 24) bins[k].bad = true;
        for (const [ox, oy] of objs) if (Math.hypot(x - ox, y - oy) < BR + 20) bins[k].bad = true;
      }
    }
    eachPx(m, (i, x, y) => {
      const d = Math.hypot(x - S.x, y - S.y);
      let an = Math.atan2(y - S.y, x - S.x); if (an < 0) an += Math.PI * 2;
      const b = bins[Math.min(71, Math.floor(an / (Math.PI * 2) * 72))];
      const v = Lb ? L[i] - Lb[i] : L[i];
      if (Math.abs(d - r) <= 1.2){ b.band[0] += L[i]; b.band[1]++; }
      else if (d >= r - 14 && d <= r - 8){ b.ins[0] += v; b.ins[1]++; }
      else if (d >= r + 14 && d <= r + 20){ b.out[0] += v; b.out[1]++; }
    });
    const good = bins.filter(b => !b.bad && b.band[1] && b.ins[1] && b.out[1]);
    const lowSteps = good.map(b => b.ins[0] / b.ins[1] - b.out[0] / b.out[1]).filter(v => v < 0.12).length;
    const band = good.map(b => b.band[0] / b.band[1]);
    const step = good.map(b => b.ins[0] / b.ins[1] - b.out[0] / b.out[1]);
    return { used: good.length, low: lowSteps, bandMin: Math.min(...band), bandMed: band.sort((p, q) => p - q)[band.length >> 1],
             stepMin: Math.min(...step), stepMed: step.sort((p, q) => p - q)[step.length >> 1] };
  }
  /* THE RAYS: their footprint against the same frame without them, and how
     much of the circle at radius 60-110 they cover */
  function rays(m, f){
    const S = f.ultSunrise;
    const L1 = draw(m, true, []), L0 = draw(m, true, ["_sunRays"]);
    let s = 0, n = 0; const cov = new Array(180).fill(0), tot = new Array(180).fill(0);
    eachPx(m, (i, x, y) => {
      const d = L1[i] - L0[i];
      if (Math.abs(d) > 0.01){ s += Math.abs(d); n++; }
      const r = Math.hypot(x - S.x, y - S.y);
      if (r >= 60 && r <= 110){
        let an = Math.atan2(y - S.y, x - S.x); if (an < 0) an += Math.PI * 2;
        const k = Math.min(179, Math.floor(an / (Math.PI * 2) * 180));
        tot[k]++; if (d > 0.02) cov[k]++;
      }
    });
    let covered = 0, bins = 0;
    for (let k = 0; k < 180; k++) if (tot[k]){ bins++; if (cov[k] / tot[k] > 0.3) covered++; }
    return { dL: n ? s / n : 0, px: n, cover: bins ? covered / bins : 0 };
  }
  /* A NUMBER'S LEGIBILITY: mean |dL| over its footprint, on a frame, with
     and without it */
  function numberLeg(m, fl, exclude){
    const keep = m.floats.slice();
    m.floats.length = 0; for (const q of keep) if (q !== fl && q !== exclude) m.floats.push(q);
    const L0 = draw(m, true, []);
    m.floats.push(fl);
    const L1 = draw(m, true, []);
    m.floats.length = 0; for (const q of keep) m.floats.push(q);
    let s = 0, n = 0;
    for (let i = 0; i < L0.length; i++){ const d = Math.abs(L1[i] - L0[i]); if (d > 0.02){ s += d; n++; } }
    return { dL: n ? s / n : 0, px: n };
  }
  return { draw, disc, arenaMean, washLift, rim, rays, numberLeg, toDev, R };
})();
"""

# ------------------------------------------------------------ legibility --
LEG_JS = r"""([foe, seed0, rimFrames]) => {
  window.__frozen = true;
  AC.setResolution(540, 960);
  AC.SFX.play = function(){};
  if (typeof CINE !== 'undefined') CINE.on = false;
  const L = window.SUNLAB, dt = AC.CONFIG.physics.dt;
  const out = { foe, seed: null, wash: null, rim: null, rays: null, num: null, echo: null,
                rims: [], sizes: null };
  for (let sd = seed0; sd < seed0 + 60 && (!out.wash || !out.num || out.rims.length < rimFrames); sd++){
    const m = new AC.Match("dawnbringer", foe, sd >>> 0);
    AC.__inject(m);
    if (typeof POSTFX !== 'undefined') POSTFX.reset();
    const me = m.a;
    let steps = 0, t0 = null, hold = null, ticks = 0, lastRim = -9;
    while (!m.over && steps < 160 / dt){
      m.step(dt); steps++;
      const S = me.ultSunrise;
      if (!S || !S.up) continue;
      /* THE HOLD: fully up, the foe anywhere, the first time past 2.3s */
      if (!out.wash && S.t > 2.3 && S.t < 7.5 && me.sunriseSeen){
        out.seed = sd; out.at = +m.t.toFixed(2); out.St = +S.t.toFixed(2);
        out.wash = L.washLift(m, me);
        const BARE = ["drawSunrise", "drawSunriseBlade", "drawSunriseFlash"];
        out.rim = L.rim(m, me, L.draw(m, true, []), L.draw(m, true, BARE));
        out.rim0 = L.rim(m, me, L.draw(m, false, []), L.draw(m, false, BARE));
        out.rays = L.rays(m, me);
      }
      /* THE RIM, over several hold frames and both breathing phases */
      if (out.rims.length < rimFrames && S.t > 2.3 && S.t < 7.8 && me.sunriseSeen && m.t - lastRim > 0.9){
        lastRim = m.t;
        const rr = L.rim(m, me, L.draw(m, true, []),
                         L.draw(m, true, ["drawSunrise", "drawSunriseBlade", "drawSunriseFlash"]));
        rr.breath = 0.03 * Math.sin(Math.PI * 2 * 0.8 * (m.t + (m.deathAge || 0)));
        out.rims.push(rr);
      }
      /* A TICK: the number just pushed, and Corollary's echo number drawn on
         the same frame over the same foe, its own formula (22 + dmg * 0.5,
         the runic glow; dmg 11.6, the mean echo -- v88 §6b) */
      const T = me.sunriseTally;
      if (T.ticks > ticks){
        ticks = T.ticks;
        const fl = m.floats[m.floats.length - 1];
        if (!out.num && fl && fl.c === "#FFD98A" && m.b.alive){
          out.num = L.numberLeg(m, fl);
          const echo = { x: fl.x, y: fl.y, text: 12, c: AC.AFFINITIES.runic.glow, life: fl.life, size: 22 + 11.6 * 0.5 };
          out.echo = L.numberLeg(m, echo, fl);
          out.sizes = {};
          for (const sz of [24, 26, 28, 30])
            out.sizes[sz] = L.numberLeg(m, Object.assign({}, fl, { size: sz }), fl).dL;
        }
      }
    }
  }
  return out;
}"""

# ---------------------------------------------- the flash, the armed blade --
TIMING_JS = r"""([foes, seeds]) => {
  window.__frozen = true;
  AC.setResolution(540, 960);
  AC.SFX.play = function(){};
  if (typeof CINE !== 'undefined') CINE.on = false;
  const L = window.SUNLAB, dt = AC.CONFIG.physics.dt;
  const res = { breaks: 0, flashLife: [], flashDisc: [], armedFrames: 0, armedDrawn: 0, armedInWall: 0,
                idleFrames: 0, idleDrawn: 0, fights: 0 };
  for (const foe of foes) for (const sd of seeds){
    const m = new AC.Match("dawnbringer", foe, sd >>> 0);
    AC.__inject(m);
    const me = m.a;
    let steps = 0, brk = null, lastUpX = null, k = 0;
    res.fights++;
    while (!m.over && steps < 160 / dt){
      m.step(dt); steps++;
      const S = me.ultSunrise, now = m.t + (m.deathAge || 0);
      /* a new break: the sun is up with an anchor not seen before */
      if (S && S.up && S.x !== lastUpX){ lastUpX = S.x; brk = { t: now, gone: null }; res.breaks++; }
      if (brk && brk.gone === null){
        if (!me.sunriseFlash) brk.gone = now - brk.t, res.flashLife.push(brk.gone);
        else if (res.flashDisc.length < 400 && steps % 3 === 0){
          const Lf = L.draw(m, true, []), L0 = L.draw(m, true, ["drawSunriseFlash"]);
          for (const g of [m.a, m.b]) if (g.alive){
            const d1 = L.disc(Lf, g), d0 = L.disc(L0, g);
            res.flashDisc.push([+d1.toFixed(4), +(d1 - d0).toFixed(4)]);
          }
        }
      }
      /* THE ARMED BLADE, every 20th step: drawn exactly while armed */
      if (steps % 20 === 0 && !m.over){
        const armed = !!(S && S.armed) && me.alive;
        /* where the tell is drawn: the blade's span 0.25..0.95 of its length.
           If none of it is inside the hall the blade points into a wall and
           nothing of it is on screen to draw on. */
        const Lb = me.w.reach * m.actMods.reach * me.reachMul + 6, BR = AC.CONFIG.physics.ballR;
        let inHall = false;
        for (const sg of m.bladeSegments(me)) for (let q = 0.25; q <= 0.951; q += 0.05){
          const d = BR - 6 + Lb * q, x = me.x + Math.cos(sg.a) * d, y = me.y + Math.sin(sg.a) * d;
          const n = m.inset || 0;
          if (x > n && x < AC.CONFIG.arena.w - n && y > n && y < AC.CONFIG.arena.h - n
              && !(m.b.alive && Math.hypot(x - m.b.x, y - m.b.y) < BR)) inHall = true;
        }
        const L1 = L.draw(m, false, []), L0 = L.draw(m, false, ["drawSunriseBlade"]);
        let diff = 0; for (let i = 0; i < L1.length; i++) if (L1[i] !== L0[i]) diff++;
        if (armed && !inHall) res.armedInWall++;
        else if (armed){ res.armedFrames++; if (diff > 0) res.armedDrawn++; }
        else { res.idleFrames++; if (diff > 0) res.idleDrawn++; }
      }
      k++;
    }
  }
  return res;
}"""

# ----------------------------------------------------------------- bloom --
BLOOM_JS = r"""([foe, side, seed0, want]) => {
  window.__frozen = true;
  AC.setResolution(540, 960);
  AC.SFX.play = function(){};
  if (typeof CINE !== 'undefined') CINE.on = false;
  const L = window.SUNLAB, dt = AC.CONFIG.physics.dt;
  const rows = [];
  for (let sd = seed0; sd < seed0 + 80 && rows.length < want; sd++){
    const m = side ? new AC.Match(foe, "dawnbringer", sd >>> 0) : new AC.Match("dawnbringer", foe, sd >>> 0);
    AC.__inject(m);
    const me = side ? m.b : m.a, oth = side ? m.a : m.b;
    let steps = 0, lastT = -9;
    while (!m.over && steps < 160 / dt && rows.length < want){
      m.step(dt); steps++;
      const S = me.ultSunrise;
      if (!S || !S.up || S.t < 2.3 || S.t > 7.8 || !me.sunriseSeen) continue;
      if (m.t - lastT < 0.33) continue;                 /* spread across the hold */
      lastT = m.t;
      const on = L.draw(m, true, []), off = L.draw(m, false, []);
      const onX = L.draw(m, true, ["drawSunrise"]), offX = L.draw(m, false, ["drawSunrise"]);
      const onN = L.draw(m, true, ["drawSunrise", "drawSunriseBlade", "drawSunriseFlash"]);
      const lift = L.arenaMean(on) - L.arenaMean(off), liftX = L.arenaMean(onX) - L.arenaMean(offX);
      const d = [me, oth].filter(g => g.alive);
      rows.push({ seed: sd, t: +m.t.toFixed(2), lift, share: lift - liftX,
                  disc: Math.max(...d.map(g => L.disc(on, g))),
                  sunOver: Math.max(...d.map(g => { const w = L.disc(on, g), n = L.disc(onN, g);
                                                     return w > 0.90 && w - n > 0.005 ? w : 0; })),
                  dDisc: Math.max(...d.map(g => Math.abs(L.disc(on, g) - L.disc(onX, g)))),
                  dDisc0: Math.max(...d.map(g => Math.abs(L.disc(off, g) - L.disc(offX, g)))) });
    }
  }
  return rows;
}"""

# THE WHITE AUREOLE STANDING ON THE CORE: a real hold, the foe moved onto the
# sun's contact point for one frame (drawn only; nothing is stepped after).
CORE_JS = r"""([seed0]) => {
  window.__frozen = true;
  AC.setResolution(540, 960);
  AC.SFX.play = function(){};
  if (typeof CINE !== 'undefined') CINE.on = false;
  const L = window.SUNLAB, dt = AC.CONFIG.physics.dt;
  for (let sd = seed0; sd < seed0 + 60; sd++){
    const m = new AC.Match("dawnbringer", "aureole", sd >>> 0);
    AC.__inject(m);
    let steps = 0;
    while (!m.over && steps < 160 / dt){
      m.step(dt); steps++;
      const S = m.a.ultSunrise;
      if (!S || !S.up || S.t < 2.3 || !m.a.sunriseSeen || !m.b.alive) continue;
      const bx = m.b.x, by = m.b.y;
      m.b.x = S.x; m.b.y = S.y;
      const on = L.draw(m, true, []), onX = L.draw(m, true, ["drawSunrise"]);
      const off = L.draw(m, false, []), offX = L.draw(m, false, ["drawSunrise"]);
      const r = { seed: sd, disc: L.disc(on, m.b), bare: L.disc(onX, m.b),
                  disc0: L.disc(off, m.b), bare0: L.disc(offX, m.b) };
      m.b.x = bx; m.b.y = by;
      return r;
    }
  }
  return null;
}"""

# ------------------------------------------------------------- the sheet --
SHEET_JS = r"""([foe, seed0]) => {
  window.__frozen = true;
  AC.setResolution(540, 960);
  AC.SFX.play = function(){};
  if (typeof CINE !== 'undefined') CINE.on = false;
  const L = window.SUNLAB, dt = AC.CONFIG.physics.dt, cv = document.getElementById('cv');
  /* the fight: an arming of at least 0.8s, the foe inside AND outside the sun
     at some point, and the sun setting on its clock with both still alive */
  for (let sd = seed0; sd < seed0 + 200; sd++){
    const m = new AC.Match("dawnbringer", foe, sd >>> 0);
    const me = m.a;
    let steps = 0, castT = null, armed = 0, brk = null, ins = 0, outs = 0, set = null, prevIn = null, cross = 0;
    while (!m.over && steps < 160 / dt){
      m.step(dt); steps++;
      const S = me.ultSunrise;
      if (!brk && S && S.armed && !S.up && castT === null) castT = m.t;
      if (!brk && S && S.up && castT !== null){ brk = m.t; armed = brk - castT; }
      if (brk && !set && S && S.up){ const i = me.sunriseIn; if (prevIn !== null && i !== prevIn) cross++; prevIn = i; }
      if (brk && !set && (!S || !S.up)){ set = m.t; break; }
    }
    if (!(armed >= 0.8 && cross >= 2 && set && set - brk > 7.9 && !m.over)) continue;
    /* replay it and photograph the six moments -- with the HUD's ult card
       HIDDEN, as the clip is: Rick judges whether the picture alone says what
       the ultimate does, and the HUD prints the card for the five seconds
       before a cast */
    if (typeof ULTBAR !== 'undefined') ULTBAR.tip = false;
    const m2 = new AC.Match("dawnbringer", foe, sd >>> 0);
    AC.__inject(m2);
    if (typeof POSTFX !== 'undefined') POSTFX.reset();
    const shots = [];
    const at = [[castT + armed * 0.6, "ARMED - the sun is in the blade"], [brk + 0.08, "THE BREAK - where the sword hit"],
                [brk + 0.5, "+0.5s - the rim leaves the point"], [brk + 2.2, "+2s - the sun is up"],
                [brk + 5.0, "+5s - inside it burns, outside not"], [set + 0.25, "SUNSET - it goes down"]];
    let k = 0; steps = 0;
    while (!m2.over && k < at.length && steps < 160 / dt){
      m2.step(dt); steps++;
      if (m2.t >= at[k][0]){
        L.draw(m2, true, []);
        shots.push([at[k][1], cv.toDataURL("image/png"), +m2.t.toFixed(2)]);
        k++;
      }
    }
    return { seed: sd, armed, brk, set, cross, shots };
  }
  return null;
}"""


def main() -> int:
    t0 = time.time()
    game = (HERE / a.game).resolve() if not pathlib.Path(a.game).is_absolute() else pathlib.Path(a.game)
    R = {"game": game.name}
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox"])
        pg = br.new_page(viewport={"width": 620, "height": 1000})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(game.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS && window.__fontsReady !== false", timeout=30000)
        ver = pg.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        R["chromium"] = ver
        pg.evaluate(LIB)
        only = set(a.only.split(","))
        R["leg"] = [pg.evaluate(LEG_JS, [f, 5100, a.rim_frames]) for f in LEG_FOES] if "leg" in only else []
        R["timing"] = pg.evaluate(TIMING_JS, [LEG_FOES, [5200, 5201, 5202]]) if "timing" in only else None
        R["bloom"] = []
        for f in (BLOOM_FOES if "bloom" in only else []):
            for side in (0, 1):
                rows = pg.evaluate(BLOOM_JS, [f, side, 5300, a.bloom_frames])
                for r in rows:
                    r["foe"], r["side"] = f, side
                R["bloom"] += rows
        R["core"] = pg.evaluate(CORE_JS, [5400]) if "core" in only else None
        if a.sheet and "sheet" in only:
            R["sheet"] = pg.evaluate(SHEET_JS, [a.sheet_foe, 5500])
        br.close()
    if errs:
        print("PAGE ERRORS:", errs[:5])
        return 2

    print(f"\nDAYBREAK'S CIRCLE -- THE PICTURE  {R['game']}  Chromium {R['chromium']}  540x960")
    checks = []
    print("\n  LEGIBILITY (first)")
    for L in R["leg"]:
        w, rm, ry, rm0 = L["wash"], L["rim"], L["rays"], L.get("rim0")
        if L.get("rims"):
            rs = L["rims"]
            print(f"   {L['foe']:<13} THE RIM over {len(rs)} hold frames: " + "  ".join(
                f"[{r['stepMin']:.3f}/{r['stepMed']:.3f} low {r['low']}/{r['used']} br {r['breath']:+.3f}]" for r in rs))
        if not w:
            print(f"   {L['foe']:<13} NO HOLD FOUND")
            checks.append((f"L1-3 {L['foe']}", False)); continue
        print(f"   {L['foe']:<13} seed {L['seed']} at {L['at']}s (sun t {L['St']})")
        print(f"     wash    +{w['on']:.3f} over the bare floor (chain off +{w['off']:.3f})   n {w['n']}")
        print(f"     rim     band min {rm['bandMin']:.3f} med {rm['bandMed']:.3f}   step min {rm['stepMin']:.3f} "
              f"med {rm['stepMed']:.3f}   ({rm['used']}/72 angles usable)   chain off: band min "
              f"{rm0['bandMin']:.3f} step min {rm0['stepMin']:.3f}")
        print(f"     rays    |dL| {ry['dL']:.3f} over {ry['px']} px, covering {100 * ry['cover']:.0f}% of the circle at r 60-110")
        n, e = L["num"], L["echo"]
        if n and e:
            print(f"     number  the tick's |dL| {n['dL']:.3f} ({n['px']} px)   the echo's {e['dL']:.3f} ({e['px']} px)"
                  + ("   by size: " + "  ".join(f"{k} {v:.3f}" for k, v in L["sizes"].items()) if L.get("sizes") else ""))
        allr = [rm] + L.get("rims", [])
        checks += [(f"L1 wash >= +0.15 ({L['foe']})", w["on"] >= 0.15),
                   (f"L2 rim band >= 0.50 and step >= 0.12 at every usable angle, "
                    f"{sum(1 for r in allr if r['used'] >= 6)} judged frames ({L['foe']})",
                    sum(1 for r in allr if r["used"] >= 6) >= 3
                    and all(r["bandMin"] >= 0.50 and r["stepMin"] >= 0.12 for r in allr if r["used"] >= 6)),
                   (f"L3 rays are marks, not a disc ({L['foe']})", ry["dL"] >= 0.05 and ry["cover"] < 0.6),
                   (f"L4 the tick's number reads >= the echo's ({L['foe']})",
                    bool(n and e) and n["dL"] >= e["dL"])]
    T = R["timing"]
    FD = []
    if T:
        fl = T["flashLife"]
        FD = T["flashDisc"]
        print(f"\n   the break's flash: {T['breaks']} breaks, gone after {min(fl):.3f}-{max(fl):.3f}s of match time; "
              f"it adds at most {max([x[1] for x in FD] or [0]):+.4f} to a disc; discs over 0.90 it raised: "
              f"{sum(1 for x in FD if x[0] > 0.90 and x[1] > 0.005)} of {len(FD)} ball-frames")
        print(f"   the armed blade: drawn on {T['armedDrawn']}/{T['armedFrames']} armed frames, "
              f"{T['idleDrawn']}/{T['idleFrames']} others ({T['armedInWall']} armed frames with the blade in a wall)")
        checks += [("L5 the flash is gone by 0.3s", bool(fl) and max(fl) <= 0.3 + 1 / 120 + 1e-9),
                   ("L6 the armed edge-light on every armed frame it can be seen on, and no other",
                    T["armedFrames"] > 0 and T["armedDrawn"] == T["armedFrames"] and T["idleDrawn"] == 0)]
    print("\n  THE BLOOM (after)")
    B = R["bloom"]
    if B:
        sh = [r["share"] for r in B]; lf = [r["lift"] for r in B]
        print(f"   {len(B)} frames at the hold ({len(BLOOM_FOES)} foes x 2 sides): arena lift mean {sum(lf)/len(lf):+.4f} "
              f"max {max(lf):+.4f}; the sun's share mean {sum(sh)/len(sh):+.5f} max {max(sh):+.5f}")
        print(f"   max disc {max(r['disc'] for r in B):.3f} (a ball's own, over 0.90 without the sun too: "
              f"{sum(1 for r in B if r['disc'] > 0.90)} frames; the sun took one over: "
              f"{sum(1 for r in B if r['sunOver'] > 0)})   max disc change from the sun: chain on "
              f"{max(r['dDisc'] for r in B):.4f}, off {max(r['dDisc0'] for r in B):.4f}")
    Cr = R["core"]
    if Cr:
        print(f"   the white Aureole ON the core: disc {Cr['disc']:.3f} (bare {Cr['bare']:.3f}); chain off "
              f"{Cr['disc0']:.3f} (bare {Cr['bare0']:.3f})")
    wash_same = all(abs(L["wash"]["on"] - L["wash"]["off"]) <= 0.01 for L in R["leg"] if L["wash"])
    if B:
        checks += [("B1 the sun's share of the bloom <= +0.02 (180 frames)", max(r["share"] for r in B) <= 0.02),
                   ("B2 the sun never takes a disc over 0.90: the hold, the Aureole on the core, the flash",
                    all(r["sunOver"] == 0 for r in B) and bool(Cr) and Cr["disc"] <= 0.90
                    and not any(x[0] > 0.90 and x[1] > 0.005 for x in FD)),
                   ("B3 the sun never paints a ball (disc change 0.00) and is the same light chain off",
                    max(r["dDisc"] for r in B) < 0.005 and max(r["dDisc0"] for r in B) < 0.005
                    and bool(Cr) and abs(Cr["disc"] - Cr["bare"]) < 0.005 and wash_same)]
    ok = 0
    print()
    for text, c in checks:
        ok += bool(c)
        print(f"  {'PASS' if c else 'FAIL'}  {text}")
    print(f"\n  {ok}/{len(checks)}   ({time.time() - t0:.0f}s)")

    if a.sheet and R.get("sheet"):
        from PIL import Image, ImageDraw, ImageFont
        S = R["sheet"]
        ims = []
        for label, url, tt in S["shots"]:
            im = Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).convert("RGB")
            d = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype("arialbd.ttf", 17)
            except Exception:
                font = ImageFont.load_default()
            d.rectangle([0, im.height - 40, im.width, im.height], fill=(0, 0, 0))
            d.text((10, im.height - 32), f"{label}   ({tt:.2f}s)", font=font, fill=(235, 225, 205))
            ims.append(im)
        Wd, Hd = ims[0].size
        sheet = Image.new("RGB", (Wd * len(ims) + 6 * (len(ims) - 1), Hd), (20, 16, 26))
        for i, im in enumerate(ims):
            sheet.paste(im, (i * (Wd + 6), 0))
        out = pathlib.Path(a.sheet)
        if not out.is_absolute():
            out = (HERE / out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out)
        print(f"  sheet {out}  dawnbringer v {a.sheet_foe} seed {S['seed']}: armed {S['armed']:.2f}s, "
              f"{S['cross']} crossings, set at {S['set']:.2f}")
        R["sheet"] = {k: v for k, v in S.items() if k != "shots"}
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
