#!/usr/bin/env python
"""THE UMBRAL SCYTHE, REDRAWN FROM RICK'S THREE REFERENCES -- Cowork, v63.

    python umbral_scythe_moon_lab.py --game ../02-chain/sc-duskreave.html

Rick, 2026-09-02: "lets redo umbral scythes silhouette. the current one is
really bad" -- with `06-docs/v63/ref-scythe-1/2/3.jpg`. Cowork owns this redraw
(CLAIMS.md, 03:58 UTC); Code's `umbral_scythe_lab.py` spread is superseded.

WHAT THE THREE REFERENCES SHARE, read as SILHOUETTE (this is the read Code's
spread missed -- every one of its arms kept `_scBase`'s short crescent and
varied what hung off it):

  * THE BLADE IS BIG. In all three the blade is roughly HALF the weapon's
    footprint -- a long band sweeping 150-180 degrees, not a short hook on a
    long pole. `_scBase`'s crescent sweeps ~90 degrees and is a third of the
    footprint.
  * A HUB AT THE JUNCTION. Ref 1 a faceted plate with a gem, ref 2 a ring
    with a hot core, ref 3 a bulb. Nothing on the scythe row has one; the type
    has a 5px collar.
  * A JOINTED SHAFT with a POMMEL. Knuckles on 1 and 2, a chain on 3; a gem or
    spike at the butt on all three.
  * A HOT EDGE ON A NEAR-BLACK BODY. All three. `_whGnawed` already took the
    umbral hammer near-black; this is the second umbral weapon to go there.

THE CANDIDATES vary the BLADE -- the one thing Rick asked about -- and hold
the hub, the shaft and the surface treatment fixed, so the sheet answers one
question:

    A  MOON     a thin band sweeping ~175 degrees, its tip curling back
                toward the shaft -- ref 1's crescent
    B  TALON    a longer, shallower blade tapering to a needle, with a RING
                hub and two prongs behind it -- ref 2
    C  REAPER   a broad blade with five spines grown out of its back -- ref 3
    D  WANE     the moon with a spur off the hub -- the read that takes what
                all three share and nothing one of them owns
    E  SHIPPED  `_scEaten`, the control

EVERY BLADE IS ONE CLOSED PATH -- honed edge out to the tip, back edge home,
spines and all -- and the hub is a second closed path that the blade's root
sits INSIDE, so nothing can come apart at any zoom. v58's rule.

THE BLADE'S REACH IS PRINTED, because the art is free to the sim (litWeapon
bakes it; nothing reads the path) but not free to the EYE: the sim's reach is
104 and a blade drawn past it says a hit that did not land. Each arm reports
its furthest point from the ball as a fraction of L.

Injected over `SHAPES._scEaten` at runtime; the page is thrown away. A LOOK.
"""
from __future__ import annotations
import argparse, base64, io, math, pathlib, sys

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

L, W = 104, 46
ROT = -0.55

PRELUDE = r"""() => {
  const S = AC.SHAPES, TAU = Math.PI * 2;
  const U = window.__UMB = {};

  const bez = (P, u) => {
    const it = 1 - u;
    const b  = (a,bq,cq,d) => it*it*it*a + 3*it*it*u*bq + 3*it*u*u*cq + u*u*u*d;
    const db = (a,bq,cq,d) => 3*it*it*(bq-a) + 6*it*u*(cq-bq) + 3*u*u*(d-cq);
    const x = b(P[0][0],P[1][0],P[2][0],P[3][0]), y = b(P[0][1],P[1][1],P[2][1],P[3][1]);
    let tx = db(P[0][0],P[1][0],P[2][0],P[3][0]), ty = db(P[0][1],P[1][1],P[2][1],P[3][1]);
    const m = Math.hypot(tx,ty) || 1; tx/=m; ty/=m;
    return { x, y, tx, ty };
  };

  /* THE BLADE. `spine` is the HONED edge as a cubic (it is what gets the glow
     stroke, so it has to be a clean curve). The back edge is the honed edge
     pushed out along the OUTWARD normal by `w(t)` -- so the blade's width is a
     profile, not a second hand-placed curve that can disagree with the first.
     Outward = toward the control points, which sit on the convex side of any
     single-bend cubic. */
  U.bladePath = (c, o) => {
    const P = o.spine, N = 48;
    const M = [(P[1][0]+P[2][0])/2, (P[1][1]+P[2][1])/2];
    const mid = bez(P, 0.5);
    let sgn = ((mid.ty)*(M[0]-mid.x) + (-mid.tx)*(M[1]-mid.y)) > 0 ? 1 : -1;
    const at = (t) => { const q = bez(P, t); return { x:q.x, y:q.y, nx: sgn*q.ty, ny: -sgn*q.tx, tx:q.tx, ty:q.ty }; };
    U._at = at;
    c.beginPath();
    const r0 = at(0);
    c.moveTo(r0.x, r0.y);
    c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]);   // honed edge, root -> tip
    /* back edge, tip -> root, with spines lifted off it if asked */
    const sp = o.spines || [];
    let si = sp.length - 1;
    for (let i = N; i >= 0; i--){
      const t = i / N, q = at(t), w = o.w(t);
      const bx = q.x + q.nx * w, by = q.y + q.ny * w;
      if (si >= 0 && t <= sp[si].t){
        /* a spine: leave the back edge, climb to a point swept toward the
           tip, come back down further along -- three vertices, all on or
           above the outline, one path. */
        const s = sp[si--];
        const a = at(s.t + s.base), b2 = at(s.t + s.base*0.35), r = at(s.t - s.base*0.55);
        const wa = o.w(s.t + s.base), wr = o.w(s.t - s.base*0.55);
        c.lineTo(a.x + a.nx*wa, a.y + a.ny*wa);
        c.lineTo(b2.x + b2.nx*(o.w(s.t)+s.h) + b2.tx*s.h*0.55,
                 b2.y + b2.ny*(o.w(s.t)+s.h) + b2.ty*s.h*0.55);
        c.lineTo(r.x + r.nx*wr, r.y + r.ny*wr);
        i = Math.floor((s.t - s.base*0.55) * N);
        continue;
      }
      c.lineTo(bx, by);
    }
    c.closePath();
  };

  /* THE HUB: a faceted plate at the junction, drawn AFTER the blade so the
     blade's root disappears into it. `spur` grows one point of the plate out
     into a hook behind the blade (arm D); `ring` draws it as ref 2's ring
     instead (arm B). */
  U.hub = (c, Lq, Wq, p, o) => {
    const hx = Lq*0.71, hy = Wq*0.10, r = Wq*(o.hubR || 0.30);
    c.save(); c.translate(hx, hy);
    if (o.ring){
      c.lineWidth = Math.max(1.2, Wq*0.075);
      c.strokeStyle = S._shade(p.steel, 0.95, 0.30);
      c.beginPath(); c.arc(0, 0, r, 0, TAU); c.stroke();
      c.strokeStyle = p.core + "99"; c.lineWidth = Math.max(1, Wq*0.03);
      c.beginPath(); c.arc(0, 0, r*0.72, 0, TAU); c.stroke();
      if (o.prongs){
        /* two prongs off the ring's back, the way ref 2 carries them --
           each is a closed path whose base is INSIDE the ring band. */
        for (const a of [Math.PI*0.72, Math.PI*1.05]){
          c.save(); c.rotate(a);
          c.beginPath();
          c.moveTo(r*0.80, -Wq*0.085); c.lineTo(r*1.95, -Wq*0.02);
          c.lineTo(r*2.05,  Wq*0.03); c.lineTo(r*0.80,  Wq*0.085);
          c.closePath();
          c.fillStyle = S._ink(p.dark, 22); c.fill();
          c.strokeStyle = S._shade(p.steel, 1.05, 0.40); c.lineWidth = Math.max(1, Wq*0.03); c.stroke();
          c.restore();
        }
      }
    } else {
      c.beginPath();
      const n = 6;
      for (let i = 0; i < n; i++){
        const a = -Math.PI/2 + i * TAU / n;
        let rr = r;
        if (o.spur && i === 3) rr = r * 2.6;             // the point that grows into a hook
        const px = Math.cos(a)*rr, py = Math.sin(a)*rr;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
        if (o.spur && i === 3){                          // recurve it: come back under
          c.lineTo(Math.cos(a+0.55)*r*1.35, Math.sin(a+0.55)*r*1.35);
        }
      }
      c.closePath();
      c.fillStyle = S._ink(p.dark, 20); c.fill();
      c.strokeStyle = S._shade(p.steel, 1.05, 0.40); c.lineWidth = Math.max(1, Wq*0.035); c.stroke();
      c.beginPath();                                     // inner facet
      for (let i = 0; i < n; i++){
        const a = -Math.PI/2 + i * TAU / n + Math.PI/n;
        const px = Math.cos(a)*r*0.62, py = Math.sin(a)*r*0.62;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.closePath();
      c.strokeStyle = p.core + "88"; c.lineWidth = Math.max(1, Wq*0.025); c.stroke();
    }
    /* the gem core -- every reference has a lit stone here */
    const gr = r * (o.ring ? 0.42 : 0.36);
    c.save(); c.globalCompositeOperation = "lighter";
    const g = c.createRadialGradient(0, 0, 0, 0, 0, gr*2.2);
    g.addColorStop(0, p.glow); g.addColorStop(0.35, p.core + "AA"); g.addColorStop(1, p.core + "00");
    c.fillStyle = g; c.beginPath(); c.arc(0, 0, gr*2.2, 0, TAU); c.fill();
    c.restore();
    c.fillStyle = p.glow; c.beginPath(); c.arc(0, 0, gr*0.55, 0, TAU); c.fill();
    c.restore();
    /* the school's mark stays on the hub -- tarnish eating the plate's face */
    S._makerMark(c, hx + r*0.55, hy + r*0.45, Wq*0.10, Wq*0.62, p);
  };

  /* THE SHAFT: near-black, three knuckles, a pommel gem. Refs 1 and 2. The
     line it takes is `_scBase`'s own quadratic so the hand and the hub land
     where the type puts them. */
  U.shaft = (c, Lq, Wq, p, o) => {
    const at = (u) => { const it = 1-u;
      return { x: 2*it*u*(Lq*0.44) + u*u*(Lq*0.71), y: 2*it*u*(Wq*0.30) + u*u*(Wq*0.10),
               a: Math.atan2(2*it*(Wq*0.30) + 2*u*(Wq*0.10-Wq*0.30), 2*it*(Lq*0.44) + 2*u*(Lq*0.71-Lq*0.44)) }; };
    c.lineCap = "round";
    c.strokeStyle = S._ink(p.dark, 16); c.lineWidth = Wq*0.17;
    c.beginPath(); c.moveTo(0,0); c.quadraticCurveTo(Lq*0.44, Wq*0.30, Lq*0.71, Wq*0.10); c.stroke();
    c.strokeStyle = S._shade(p.steel, 0.55, 0.45); c.lineWidth = Wq*0.05;   // a cold highlight line
    c.beginPath(); c.moveTo(Lq*0.05,-Wq*0.03); c.quadraticCurveTo(Lq*0.44, Wq*0.25, Lq*0.66, Wq*0.08); c.stroke();
    if (o.chain){
      /* ref 3's chain: links as short dashes crossing the shaft */
      c.strokeStyle = S._shade(p.steel, 0.80, 0.35); c.lineWidth = Math.max(1, Wq*0.035);
      for (let i = 0; i < 9; i++){
        const q = at(0.14 + 0.06*i); c.save(); c.translate(q.x,q.y); c.rotate(q.a + 0.9);
        c.beginPath(); c.ellipse(0, 0, Wq*0.06, Wq*0.11, 0, 0, TAU); c.stroke(); c.restore();
      }
    }
    for (let i = 0; i < 3; i++){
      const q = at(0.20 + 0.20*i);
      c.save(); c.translate(q.x, q.y); c.rotate(q.a);
      c.beginPath();
      /* a SEGMENT of the rod, not a bead on it: longer along the shaft than
         across it, so the shaft reads as jointed (ref 1) */
      c.moveTo(-Wq*0.20, 0); c.lineTo(-Wq*0.13,-Wq*0.13); c.lineTo(Wq*0.13,-Wq*0.13);
      c.lineTo(Wq*0.20, 0);  c.lineTo(Wq*0.13, Wq*0.13);  c.lineTo(-Wq*0.13, Wq*0.13);
      c.closePath();
      c.fillStyle = S._ink(p.dark, 24); c.fill();
      c.strokeStyle = p.core + "BB"; c.lineWidth = Math.max(1, Wq*0.028); c.stroke();
      c.restore();
    }
    /* pommel: a hexagonal gem at the butt, ref 1 */
    c.save(); c.rotate(at(0.02).a);
    c.beginPath();
    for (let i = 0; i < 6; i++){ const a = i*TAU/6; const r = Wq*0.20;
      if (i===0) c.moveTo(Math.cos(a)*r, Math.sin(a)*r); else c.lineTo(Math.cos(a)*r, Math.sin(a)*r); }
    c.closePath();
    c.fillStyle = S._ink(p.dark, 22); c.fill();
    c.strokeStyle = S._shade(p.steel, 1.0, 0.40); c.lineWidth = Math.max(1, Wq*0.03); c.stroke();
    c.save(); c.globalCompositeOperation = "lighter";
    const g = c.createRadialGradient(0,0,0,0,0,Wq*0.30);
    g.addColorStop(0, p.glow); g.addColorStop(0.4, p.core+"AA"); g.addColorStop(1, p.core+"00");
    c.fillStyle = g; c.beginPath(); c.arc(0,0,Wq*0.30,0,TAU); c.fill(); c.restore();
    c.fillStyle = p.glow; c.beginPath(); c.arc(0,0,Wq*0.07,0,TAU); c.fill();
    c.restore();
  };

  /* THE BLADE'S SURFACE: near-black body, a cold rim on the back, the honed
     edge lit twice -- once wide and soft, once tight. Same for every arm. */
  U.paint = (c, Lq, Wq, p, o) => {
    const path = () => U.bladePath(c, o);
    path();
    const P = o.spine;
    const g = c.createLinearGradient(P[0][0], P[0][1], P[3][0], P[3][1]);
    g.addColorStop(0, S._ink(p.dark, 30)); g.addColorStop(0.5, S._ink(p.dark, 18)); g.addColorStop(1, S._ink(p.dark, 26));
    c.fillStyle = g; c.fill();
    /* the lit face: a lighter band inboard of the back edge, clipped */
    c.save(); c.shadowBlur = 0;
    const wl = S._litN(c); c.globalAlpha = 0.55 * Math.abs(wl) + 0.25;
    path(); c.clip();
    c.strokeStyle = S._shade(p.steel, 0.70, 0.30); c.lineWidth = Math.max(1, Wq*0.09);
    c.beginPath();
    for (let i = 0; i <= 40; i++){ const t = i/40, q = U._at(t), w = o.w(t)*0.66;
      const x = q.x + q.nx*w, y = q.y + q.ny*w; if (i===0) c.moveTo(x,y); else c.lineTo(x,y); }
    c.stroke();
    c.restore();
    /* cold rim on the back */
    c.strokeStyle = S._shade(p.steel, 1.15, 0.55); c.lineWidth = Math.max(1, Wq*0.035);
    path(); c.stroke();
    /* the honed edge, twice */
    const honed = () => { c.beginPath(); c.moveTo(P[0][0],P[0][1]);
      c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]); c.stroke(); };
    c.lineCap = "round";
    c.strokeStyle = p.core + "77"; c.lineWidth = Math.max(1, Wq*0.15); honed();
    c.strokeStyle = p.glow;        c.lineWidth = Math.max(1, Wq*0.055); honed();
  };

  /* the profiles, in the type's own L and W */
  const L = 104, W = 46;
  const taper = (wb, k) => (t) => wb * Math.pow(1 - t, k) * (t < 0.10 ? 0.75 + 2.5*t : 1);

  const MOON = {
    spine: [[L*0.72, W*0.02],[L*1.05, -W*0.24],[L*0.99, -W*1.46],[L*0.48, -W*1.52]],
    w: taper(W*0.34, 0.62)
  };
  const TALON = {
    spine: [[L*0.72, W*0.02],[L*1.04, -W*0.20],[L*0.97, -W*1.02],[L*0.60, -W*1.56]],
    w: taper(W*0.38, 0.85)
  };
  const REAPER = {
    spine: [[L*0.72, W*0.04],[L*1.04, -W*0.28],[L*0.95, -W*1.28],[L*0.50, -W*1.44]],
    w: taper(W*0.50, 0.70),
    spines: [{t:0.18,h:W*0.20,base:0.05},{t:0.30,h:W*0.26,base:0.055},{t:0.43,h:W*0.30,base:0.06},{t:0.56,h:W*0.26,base:0.055},{t:0.68,h:W*0.18,base:0.05}]
  };

  U.ARMS = {
    A: (c,Lq,Wq,p) => { U.shaft(c,Lq,Wq,p,{}); U.paint(c,Lq,Wq,p,MOON);   U.hub(c,Lq,Wq,p,{}); },
    B: (c,Lq,Wq,p) => { U.shaft(c,Lq,Wq,p,{}); U.paint(c,Lq,Wq,p,TALON);  U.hub(c,Lq,Wq,p,{ring:true, prongs:true, hubR:0.34}); },
    C: (c,Lq,Wq,p) => { U.shaft(c,Lq,Wq,p,{chain:true}); U.paint(c,Lq,Wq,p,REAPER); U.hub(c,Lq,Wq,p,{hubR:0.28}); },
    D: (c,Lq,Wq,p) => { U.shaft(c,Lq,Wq,p,{}); U.paint(c,Lq,Wq,p,MOON);   U.hub(c,Lq,Wq,p,{spur:true}); },
  };
  U.PROFILES = { A: MOON, B: TALON, C: REAPER, D: MOON };
  U.SHIPPED = S._scEaten;

  /* furthest point of the blade from the ball, as a fraction of L */
  U.reach = (arm) => {
    const o = U.PROFILES[arm]; if (!o) return null;
    const cv = document.createElement('canvas'); const c = cv.getContext('2d');
    U.bladePath(c, o);
    let m = 0;
    for (let i = 0; i <= 60; i++){ const t = i/60, q = U._at(t), w = o.w(t);
      m = Math.max(m, Math.hypot(q.x, q.y), Math.hypot(q.x+q.nx*w, q.y+q.ny*w)); }
    return m / L;
  };
  return Object.keys(U.ARMS).length;
}"""

DRAW_JS = r"""(cfg)=>{
  const S = AC.SHAPES, U = window.__UMB;
  S._scEaten = (cfg.arm === "E") ? U.SHIPPED : U.ARMS[cfg.arm];
  AC.setResolution(cfg.res, cfg.res * 16 / 9 | 0);
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const s = AC.renderer.scale * cfg.zoom;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation='source-over'; c.globalAlpha=1;
  c.shadowBlur=0; c.shadowColor='transparent';
  c.fillStyle = cfg.bg; c.fillRect(0, 0, cv.width, cv.height);
  const p = Object.assign({}, AC.AFFINITIES.umbral);
  S._t = 0;
  c.save();
  c.translate(cfg.ox, cfg.oy); c.rotate(cfg.rot); c.scale(s, s);
  AC.litWeapon(c, 'scythe', cfg.L, cfg.W, p, 0.5, cfg.rot);
  c.restore();
  return { png: cv.toDataURL('image/png').slice(22),
           scale: AC.renderer.scale, w: cv.width, h: cv.height };
}"""

ARENA_JS = r"""([arm, rid, foe, sd, secs, wantT])=>{
  const S = AC.SHAPES, U = window.__UMB;
  S._scEaten = (arm === "E") ? U.SHIPPED : U.ARMS[arm];
  if (S._litCache) S._litCache = {};
  window.__frozen = true;
  const pan = document.getElementById("cinePanel");
  if (pan) pan.style.display = "none";
  AC.setResolution(540, 960);
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, foe, sd);
  const me = m.a.w.id === rid ? m.a : m.b;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    if (m.t < wantT || m.hitStop > 0) continue;
    const th = Math.abs(Math.sin(me.theta));
    if (th < 0.86) continue;
    /* world -> canvas: the renderer lays the arena at (pad, arenaTop) in a
       1080x1920 space and draws it at k = 0.5 into the 540x960 canvas */
    const rr = AC.renderer, sc = rr.scale * rr.k;
    const px = (rr.pad + me.x * rr.scale) * rr.k, py = (rr.arenaTop + me.y * rr.scale) * rr.k;
    /* and not against a wall, so the crop can be centred on the relic */
    const R = 130 * sc;
    if (px < R || px > 540 - R || py < R || py > 960 - R) continue;
    AC.__draw(m);
    return { t: +m.t.toFixed(2), theta: +me.theta.toFixed(2),
             sx: px, sy: py, sc: sc,
             png: document.getElementById("cv").toDataURL("image/png").split(",",1)[0].length ? document.getElementById("cv").toDataURL("image/png").split(",")[1] : "" };
  }
  return null;
}"""

ARMS = [
    ("A", "MOON - a thin band sweeping ~175 deg, tip curling back to the shaft (ref 1)"),
    ("B", "TALON - longer, shallower, needle tip; ring hub with two prongs (ref 2)"),
    ("C", "REAPER - broad blade, five spines grown from its back; chained shaft (ref 3)"),
    ("D", "WANE - the moon plus a hooked spur off the hub (what all three share)"),
    ("E", "SHIPPED _scEaten - the control Rick rejected"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-duskreave.html")
    ap.add_argument("--zoom", type=float, default=3.2)
    ap.add_argument("--out", default="../05-reference/v63")
    ap.add_argument("--name", default="umbral-scythe-moon-candidates.png")
    ap.add_argument("--only", default="")
    ap.add_argument("--relic", default="duskreave")
    ap.add_argument("--foe", default="lastlight")
    ap.add_argument("--seed", type=int, default=33581)
    ap.add_argument("--secs", type=float, default=60.0)
    ap.add_argument("--at", type=float, default=6.0)
    A = ap.parse_args()
    out = HERE / A.out
    out.mkdir(parents=True, exist_ok=True)
    arms = [a for a in ARMS if not A.only or a[0] in A.only]

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        n = pg.evaluate(PRELUDE)
        print(f"  {n} arms injected over SHAPES._scEaten")
        for arm, _ in arms:
            r = pg.evaluate("(a)=>window.__UMB.reach(a)", arm)
            if r is not None:
                print(f"  reach {arm}: {r:.3f} L  (sim reach 1.00 L; shipped crescent 1.02 L)")

        rows = []
        for arm, label in arms:
            # ZOOM PANEL, cropped to the bbox of what was drawn.
            res, zoom = 1080, A.zoom
            ox, oy = res // 2, int(res * 16 / 9) // 2
            got = pg.evaluate(DRAW_JS, {
                "arm": arm, "L": L, "W": W, "zoom": zoom, "res": res,
                "ox": ox, "oy": oy, "rot": ROT, "bg": "#0B0710"})
            im = Image.open(io.BytesIO(base64.b64decode(got["png"]))).convert("RGB")
            from PIL import ImageChops
            bg = Image.new("RGB", im.size, (0x0B, 0x07, 0x10))
            x0, y0, x1, y1 = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 6 else 0).getbbox()
            side = max(x1 - x0, y1 - y0) + 2 * int(18 * zoom)
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            zoomed = im.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2))
            # THE SHIP-SIZE PANEL IS A REAL FIGHT FRAME at 540x960 -- the same
            # frame for every arm, because the art cannot move the sim -- cropped
            # around the relic and shown at 2x nearest. Not a scaled zoom.
            shot = pg.evaluate(ARENA_JS, [arm, A.relic, A.foe, A.seed, A.secs, A.at])
            if shot:
                fr = Image.open(io.BytesIO(base64.b64decode(shot["png"]))).convert("RGB")
                w, h = fr.size
                # The frame comes back at 540x960 -- the size a short is
                # delivered at (printed, so a pinned 1080 canvas would show).
                # Crop around the relic, then 2x NEAREST so the delivered
                # pixels are visible. No zoom is added anywhere.
                assert (w, h) == (540, 960), (w, h)
                r = int(130 * shot["sc"])
                fx = min(max(int(shot["sx"]), r), w - r); fy = min(max(int(shot["sy"]), r), h - r)
                native = fr.crop((fx - r, fy - r, fx + r, fy + r))
                native = native.resize((native.width * 2, native.height * 2), Image.NEAREST)
                print(f"  {arm}: arena frame {w}x{h} t={shot['t']}s theta={shot['theta']}; crop {2*r}px shown 2x")
            else:
                native = Image.new("RGB", (300, 300), (30, 0, 0)); print(f"  {arm}: NO ARENA FRAME")
            rows.append((arm, label, zoomed, native))

        cell = 330
        rw = max(r[3].width for r in rows)
        sh = Image.new("RGB", (cell + 24 + rw, (cell + 34) * len(rows) + 30), (8, 6, 12))
        d = ImageDraw.Draw(sh)
        d.text((8, 8), "THE UMBRAL SCYTHE, FROM RICK'S REFERENCES - four blades on one hub/shaft, and the shipped one (E). "
                       "Left: zoom. Right: the SAME fight frame at the size a short ships at (540-wide), 2x pixels.", fill=(210, 200, 230))
        for i, (arm, label, zoomed, native) in enumerate(rows):
            y = 30 + i * (cell + 34)
            d.text((8, y + 4), f"{arm}   {label}", fill=(232, 214, 255))
            sh.paste(zoomed.resize((cell, cell)), (8, y + 22))
            sh.paste(native, (8 + cell + 8, y + 22 + max(0, (cell - native.height) // 2)))
        p = out / A.name
        sh.save(p)
        print(f"  {p}  {sh.size}")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:6], sep="\n    ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
