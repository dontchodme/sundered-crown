#!/usr/bin/env python
"""THE UMBRAL SCYTHE, REDRAWN -- FOUR CANDIDATES AND THE SHIPPED ONE, AS A SPREAD.

    python umbral_scythe_lab.py --game ../02-chain/sc-duskreave.html

Rick, 2026-09-02, shown `_scEaten` on screen for the first time in the game's
history: "this one is rough and should be redone." Three reference images with
it. THE SILHOUETTE IS CODE'S TO DRAFT -- brief section 3, "the silhouette and
the tornado's look are Code's to draft against the reference and film for him"
-- so this is a spread to be chosen from, not a proposal.

WHAT THE THREE REFERENCES SHARE, read as SILHOUETTE and not as colour:

  * a THIN, deeply curved blade with a hot glowing cutting edge on a near-black
    body. Every one of the three. `_scBase` already strokes `p.glow` along the
    honed edge, so this is a weight-and-value change rather than a new shape.
  * a SECONDARY FANG hooking back under the head (refs 1 and 2) -- a small
    recurved hook below the main crescent, sharing its root.
  * SPINES ALONG THE BLADE'S BACK, growing toward the tip (ref 3).
  * a JOINTED SHAFT -- knuckles, nodes, a collar gem -- and a FINNED POMMEL at
    the butt (all three, and it is the feature nothing else on this row uses).

FOUR CANDIDATES, each a different answer to "which of those is the grammar":

    A  FANG      the crescent plus one recurved fang under the head. The blade
                 otherwise clean. Silhouette-heavy, surface-light.
    B  SPINED    the back edge itself becomes six swept spines, growing toward
                 the tip. Nothing added under the head.
    C  SHAFT     the blade stays clean and the grammar moves to the SNATH --
                 four knuckles and a finned pommel. The snath is ~60% of a
                 scythe's footprint (`_scConjured`'s own measurement) and no
                 other school touches it except runic, which breaks it.
    D  REAVER    fang and spines and the hot edge together -- the arm that
                 takes everything the references have in common.
    E  SHIPPED   `_scEaten`, unchanged, as the control. A spread with no
                 control cannot tell you that the new ones are better, only
                 that they are different.

EVERY CANDIDATE OBEYS v58'S ONE RULE, which is the rule that fixed the umbral
warhammer: **a grammar that adds a limb to a type must add it to the type's
OUTLINE, not behind it.** Rick, on the first cut of `_whGnawed`: "upclose the
spikes just look like triangles layered behind the hammer." So a fang or a spine
here is emitted into the SAME closed path as the crescent -- one path, one fill,
one stroke -- and cannot come apart from the blade at any zoom. `_scBarbed`,
`_scBuilt` and `_scPlated` are all built the older way and are open item 34.

EVERY CANDIDATE IS INJECTED OVER `SHAPES._scEaten` AT RUNTIME AND THE PAGE IS
THROWN AWAY. Nothing is written to any build. This is a LOOK.

AND EACH IS DRAWN TWICE -- at zoom and at the size it actually ships at. v56's
hand was approved at zoom and shipped at ~40px as a white scribble; v53's rule
is that shape questions go to a sheet and SCALE questions need the register the
thing is delivered in.
"""
from __future__ import annotations
import argparse, base64, io, math, pathlib, sys

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

L, W = 104, 46
ROT = -0.55

# ---------------------------------------------------------------------------
# THE SHARED SKELETON. Every candidate calls `SC.blade(...)` with a list of
# limbs, and the limbs are emitted INTO the crescent's own path between the two
# beziers -- which is what makes them part of the outline instead of objects
# sitting behind it.
# ---------------------------------------------------------------------------
PRELUDE = r"""() => {
  const S = AC.SHAPES, TAU = Math.PI * 2;
  window.__SC = {};
  const SC = window.__SC;

  /* The two beziers `_scBase` draws, as samplers. `edge` is the honed one --
     the curve `_scBase` strokes in `p.glow` -- and `back` is the other. Both
     return a point and the unit normal there. */
  const bez = (P, u) => {
    const it = 1 - u;
    const b = (a,bq,cq,d) => it*it*it*a + 3*it*it*u*bq + 3*it*u*u*cq + u*u*u*d;
    const db = (a,bq,cq,d) => 3*it*it*(bq-a) + 6*it*u*(cq-bq) + 3*u*u*(d-cq);
    const x  = b(P[0][0],P[1][0],P[2][0],P[3][0]);
    const y  = b(P[0][1],P[1][1],P[2][1],P[3][1]);
    const tx = db(P[0][0],P[1][0],P[2][0],P[3][0]);
    const ty = db(P[0][1],P[1][1],P[2][1],P[3][1]);
    const m = Math.hypot(tx,ty) || 1;
    return { x, y, tx: tx/m, ty: ty/m, nx: ty/m, ny: -tx/m };
  };
  SC.pts = (Lq, Wq) => ({
    edge: [[Lq*0.70, Wq*0.20],[Lq*1.02,-Wq*0.20],[Lq*0.98,-Wq*0.95],[Lq*0.56,-Wq*1.32]],
    back: [[Lq*0.56,-Wq*1.32],[Lq*0.88,-Wq*0.72],[Lq*0.86,-Wq*0.10],[Lq*0.66, Wq*0.30]]
  });
  SC.edge = (Lq,Wq,u) => bez(SC.pts(Lq,Wq).edge, u);
  SC.back = (Lq,Wq,u) => bez(SC.pts(Lq,Wq).back, u);

  /* ONE CLOSED PATH: the honed edge, then the back -- with the back either
     smooth or broken into spines -- then optionally a fang hooked under the
     root before it closes. Nothing here strokes or fills; the caller does that
     ONCE, which is the whole point. */
  SC.blade = (c, Lq, Wq, o) => {
    const P = SC.pts(Lq, Wq);
    if (o.thin){
      /* THINNED. The back curve is pulled toward the honed edge by `thin`, so
         the blade narrows while its TIP, its ROOT and its reach stay exactly
         where the type puts them -- this is a school grammar, not a new weapon.
         `_scConjured` is the precedent for a school departing from `_scBase`
         (runic refuses it outright), so a narrower umbral blade is inside what
         this row already does. */
      const rev = [P.edge[3], P.edge[2], P.edge[1], P.edge[0]];
      P.back = P.back.map((q, i) => [
        q[0] + (rev[i][0] - q[0]) * o.thin,
        q[1] + (rev[i][1] - q[1]) * o.thin ]);
    }
    c.beginPath();
    c.moveTo(P.edge[0][0], P.edge[0][1]);
    c.bezierCurveTo(P.edge[1][0],P.edge[1][1],P.edge[2][0],P.edge[2][1],
                    P.edge[3][0],P.edge[3][1]);
    if (!o.spines){
      c.bezierCurveTo(P.back[1][0],P.back[1][1],P.back[2][0],P.back[2][1],
                      P.back[3][0],P.back[3][1]);
    } else {
      /* THE SPINES ARE THE BACK EDGE, not triangles laid on it. The curve is
         walked from the tip toward the root and every step lifts off the
         surface and comes back down to it, so the outline itself is serrated
         and there is no seam anywhere for a zoom to find. They GROW toward the
         tip: `u` runs 0 at the tip, so the height falls away as it goes. */
      const n = o.spines, h = o.spineH === undefined ? 0.30 : o.spineH;
      for (let i = 0; i <= n; i++){
        const u0 = i / n, u1 = (i + 0.5) / n;
        const a = SC.back(Lq,Wq,u0);
        if (i) c.lineTo(a.x, a.y);
        if (i === n) break;
        const b2 = SC.back(Lq,Wq,u1);
        const k = h * Wq * (1 - u1 * 0.72);          // taller near the tip
        c.lineTo(b2.x - b2.nx * k, b2.y - b2.ny * k);
      }
      c.lineTo(P.back[3][0], P.back[3][1]);
    }
    if (o.fang){
      /* THE FANG, hooked back under the root -- refs 1 and 2. It is a DETOUR
         ON THE CLOSING SEGMENT: the back curve ends at (0.66L, 0.30W) and the
         path has to reach (0.70L, 0.20W) to close, so the fang goes the long
         way round. BOTH ENDS LAND ON THE OUTLINE, which is the whole point --
         the first cut returned to the point it left from, so the lobe hung off
         the blade by a single vertex and read as a dark shape laid behind it.
         That is v58's rejection ("triangles layered behind the hammer")
         reproduced exactly, in a lab, before Rick had to see it again.

         Recurved: the leading edge bows away and the trailing edge cuts back
         under, which is what separates a fang from a triangle. */
      const f = o.fang;
      c.bezierCurveTo(Lq*0.76,          Wq*(0.30+f*0.62),
                      Lq*0.80,          Wq*(0.30+f*1.05),
                      Lq*0.90,          Wq*(0.30+f*1.34));
      c.bezierCurveTo(Lq*0.80,          Wq*(0.30+f*0.72),
                      Lq*0.755,         Wq*(0.30+f*0.30),
                      Lq*0.70,          Wq*0.20);
    }
    c.closePath();
  };

  /* The snath, and the only place a candidate is allowed to differ from
     `_scBase` on it. `knuckles` and `pommel` are candidate C's grammar. */
  SC.snath = (c, Lq, Wq, p, o) => {
    c.lineCap = "round";
    c.strokeStyle = S._shade(p.dark, 1.30, 0.28); c.lineWidth = Wq*0.15;
    c.beginPath();
    c.moveTo(0,0); c.quadraticCurveTo(Lq*0.44, Wq*0.30, Lq*0.70, Wq*0.16);
    c.stroke();
    c.strokeStyle = p.core + "66"; c.lineWidth = Wq*0.05;
    c.beginPath();
    c.moveTo(Lq*0.06,0); c.quadraticCurveTo(Lq*0.44, Wq*0.26, Lq*0.68, Wq*0.14);
    c.stroke();
    const at = (u) => {
      const it = 1-u;
      return { x: 2*it*u*(Lq*0.44) + u*u*(Lq*0.70),
               y: 2*it*u*(Wq*0.30) + u*u*(Wq*0.16),
               a: Math.atan2(2*it*(Wq*0.30) + 2*u*(Wq*0.16-Wq*0.30),
                             2*it*(Lq*0.44) + 2*u*(Lq*0.70-Lq*0.44)) };
    };
    if (o && o.knuckles){
      /* KNUCKLES ON THE HAFT -- refs 1, 2 and 3 all have them and nothing on
         this row does. Each is one closed path around the haft's own line, so
         it reads as the haft THICKENING rather than as a bead threaded on it. */
      for (let i = 0; i < o.knuckles; i++){
        const u = 0.16 + 0.66 * i / (o.knuckles - 1);
        const q = at(u);
        c.save(); c.translate(q.x, q.y); c.rotate(q.a);
        c.beginPath();
        c.moveTo(-Wq*0.13, 0);
        c.lineTo(-Wq*0.05,-Wq*0.155); c.lineTo(Wq*0.06,-Wq*0.145);
        c.lineTo( Wq*0.13, 0);
        c.lineTo( Wq*0.06, Wq*0.145); c.lineTo(-Wq*0.05, Wq*0.155);
        c.closePath();
        c.fillStyle = S._shade(p.dark, 1.55, 0.30); c.fill();
        c.strokeStyle = p.core + "CC"; c.lineWidth = Math.max(1, Wq*0.028);
        c.stroke();
        c.restore();
      }
    }
    if (o && o.pommel){
      /* THE FINNED POMMEL -- refs 2 and 3. One closed path: three fins off a
         core, at the butt, where the type has nothing at all today. */
      c.save(); c.translate(0,0); c.rotate(at(0.02).a);
      c.beginPath();
      c.moveTo( Wq*0.10, 0);
      c.lineTo(-Wq*0.02,-Wq*0.30); c.lineTo(-Wq*0.14,-Wq*0.12);
      c.lineTo(-Wq*0.30, 0);
      c.lineTo(-Wq*0.14, Wq*0.12); c.lineTo(-Wq*0.02, Wq*0.30);
      c.closePath();
      c.fillStyle = S._shade(p.dark, 1.45, 0.26); c.fill();
      c.strokeStyle = p.core; c.lineWidth = Math.max(1, Wq*0.03); c.stroke();
      c.restore();
    }
    c.fillStyle = p.dark;
    c.beginPath(); c.arc(Lq*0.70, Wq*0.14, Wq*0.12, 0, TAU); c.fill();
    S._makerMark(c, Lq*0.70, Wq*0.14, Wq*0.115, Wq*0.62, p);
  };

  /* THE BLADE'S BODY, filled and lit the way `_scBase` does it -- the same
     gradient, the same back-of-the-wedge shading, the same honed stroke. A
     candidate that redrew the lighting as well would be answering two
     questions at once, and only one of them is Rick's. `hot` darkens the body
     and lifts the edge, which is the references' single most consistent
     feature. */
  SC.paint = (c, Lq, Wq, p, o) => {
    const path = () => SC.blade(c, Lq, Wq, o);
    path();
    const g = c.createLinearGradient(Lq*0.55, -Wq, Lq*0.95, Wq*0.2);
    if (o.hot){
      g.addColorStop(0, p.glow);
      g.addColorStop(0.30, S._shade(p.steel, 0.78, 0.18));
      g.addColorStop(0.62, S._shade(p.steel, 0.40, 0.34));
      g.addColorStop(1, S._shade(p.dark, 1.20, 0.10));
    } else {
      g.addColorStop(0, p.glow);
      g.addColorStop(0.55, p.steel);
      g.addColorStop(1, S._shade(p.steel, 0.44, 0.38));
    }
    c.fillStyle = g; c.fill();
    c.save(); c.shadowBlur = 0;
    const wl = S._litN(c); c.globalAlpha = Math.abs(wl);
    path(); c.clip();
    c.fillStyle = S._facet(p.steel, p.dark, o.hot ? 0.82 : 0.68);
    c.fillRect(Lq*0.40, -Wq*1.60, Lq*0.90, Wq*2.20);
    c.translate(-Wq*0.10, Wq*0.115 * (wl < 0 ? -1 : 1));
    path(); c.fillStyle = g; c.fill();
    c.restore();
    /* THE HONED EDGE. One stroke, and on the `hot` arms it is heavier and
       carries the glow twice -- once wide and soft, once tight -- which is how
       the references read as LIT rather than as outlined. */
    const P = SC.pts(Lq, Wq);
    const honed = () => {
      c.beginPath();
      c.moveTo(P.edge[0][0], P.edge[0][1]);
      c.bezierCurveTo(P.edge[1][0],P.edge[1][1],P.edge[2][0],P.edge[2][1],
                      P.edge[3][0],P.edge[3][1]);
      c.stroke();
    };
    if (o.hot){
      c.strokeStyle = p.core + "77"; c.lineWidth = Math.max(1, Wq*0.16); honed();
      c.strokeStyle = p.glow;        c.lineWidth = Math.max(1, Wq*0.055); honed();
    } else {
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, Wq*0.05); honed();
    }
  };

  /* THE FIVE ARMS. Each is a whole `_scEaten` replacement. */
  SC.ARMS = {
    A: (c,Lq,Wq,p) => { SC.snath(c,Lq,Wq,p,{});
                        SC.paint(c,Lq,Wq,p,{ fang:1, hot:true }); },
    B: (c,Lq,Wq,p) => { SC.snath(c,Lq,Wq,p,{});
                        SC.paint(c,Lq,Wq,p,{ spines:6, hot:true }); },
    C: (c,Lq,Wq,p) => { SC.snath(c,Lq,Wq,p,{ knuckles:4, pommel:true });
                        SC.paint(c,Lq,Wq,p,{ hot:true }); },
    D: (c,Lq,Wq,p) => { SC.snath(c,Lq,Wq,p,{ knuckles:4, pommel:true });
                        SC.paint(c,Lq,Wq,p,{ fang:1, spines:6, spineH:0.24,
                                             hot:true }); },
    F: (c,Lq,Wq,p) => { SC.snath(c,Lq,Wq,p,{ knuckles:4, pommel:true });
                        SC.paint(c,Lq,Wq,p,{ thin:0.46, fang:0.72,
                                             hot:true }); }
  };
  SC.SHIPPED = S._scEaten;
  return Object.keys(SC.ARMS).length;
}"""

DRAW_JS = r"""(cfg)=>{
  const S = AC.SHAPES, SC = window.__SC;
  S._scEaten = (cfg.arm === "E") ? SC.SHIPPED : SC.ARMS[cfg.arm];
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

CRAFT_JS = r"""() => {
  const S = AC.SHAPES, TAU = Math.PI * 2, SC = window.__SC;

  /* THE SILHOUETTE IS HELD FIXED AND ONLY THE TREATMENT MOVES. Rick, shown six
     silhouettes: "none of these", and asked which gap to close first, he named
     the DETAIL AND CRAFT LEVEL. So this spread varies exactly one thing. Shape
     stays open and gets asked again after -- a spread that moves two variables
     cannot say which half worked, and that is how v42 lost four rounds.

     The base is arm F -- thinned blade, fang, knuckled shaft -- because
     proportion is the gap he did NOT name. */
  /* AND THE BASE IS THE TYPE'S OWN CRESCENT, NOT THE THINNED ONE. The first
     cut of this spread held arm F fixed -- and a thin blade has no INTERIOR,
     so facets, plates and rim lights had nowhere to be and four arms rendered
     as the same picture. Holding fixed the one variable that destroys the
     variable being tested is a broken experiment, not a null result. */
  const BASE = { thin:0.06, fang:0.72, hot:true };
  const SNATH = { knuckles:4, pommel:true };

  /* A GEM SOCKET. The references' most distinctive surface feature, and the one
     thing on them that is not metal: a bright inset with a hot halo sitting IN
     the metal rather than on it. Drawn as a dark bezel, a lit core and a
     falloff -- which is what separates an inset stone from a dot of paint. */
  const socket = (c, x, y, r, p, hue) => {
    c.save();
    c.fillStyle = S._shade(p.dark, 0.85, 0.10);
    c.beginPath(); c.arc(x, y, r * 1.42, 0, TAU); c.fill();
    c.globalCompositeOperation = "lighter";
    const g = c.createRadialGradient(x, y, 0, x, y, r * 1.30);
    g.addColorStop(0, hue || p.glow);
    g.addColorStop(0.45, (hue || p.core) + "CC");
    g.addColorStop(1, (hue || p.core) + "00");
    c.fillStyle = g;
    c.beginPath(); c.arc(x, y, r * 1.30, 0, TAU); c.fill();
    c.restore();
    c.fillStyle = hue || p.glow;
    c.beginPath(); c.arc(x, y, r * 0.42, 0, TAU); c.fill();
  };

  /* THE BLADE, BUILT IN LAYERS. `_scBase` already does three -- a gradient, a
     clipped back-of-the-wedge pass and a honed stroke -- and the references do
     five or six. THAT DIFFERENCE IS THE CRAFT GAP. Every flag below adds one
     layer, and every one is clipped to the blade's own path, so no amount of
     surface work can escape the outline. */
  const paint = (c, Lq, Wq, p, cf) => {
    const path = () => SC.blade(c, Lq, Wq, BASE);
    const cx = Lq * 0.80, cy = -Wq * 0.45;

    path();
    const g = c.createLinearGradient(Lq*0.55, -Wq, Lq*0.95, Wq*0.2);
    g.addColorStop(0, S._shade(p.steel, 0.42, 0.30));
    g.addColorStop(0.38, S._ink(p.dark, 26));
    g.addColorStop(1, S._ink(p.dark, 13));
    c.fillStyle = g; c.fill();

    c.save(); c.shadowBlur = 0;
    const wl = S._litN(c);
    path(); c.clip();

    /* FACETS -- distinct planes with a hard fold between them, not a gradient.
       A gradient reads as a coloured region; a fold reads as METAL. Three
       values, and the fold runs along the blade's own spine so the planes
       belong to the curve instead of being laid across it. */
    if (cf.facet){
      c.globalAlpha = Math.abs(wl);
      c.fillStyle = S._facet(p.steel, p.dark, 0.18);
      c.beginPath();
      c.moveTo(Lq*0.52, -Wq*1.45);
      c.lineTo(Lq*1.12, -Wq*0.55);
      c.lineTo(Lq*1.12,  Wq*0.60);
      c.lineTo(Lq*0.52,  Wq*0.60);
      c.closePath(); c.fill();
      c.fillStyle = S._facet(p.steel, p.dark, 0.72);
      c.beginPath();
      c.moveTo(Lq*0.52, -Wq*1.45);
      c.lineTo(Lq*1.12, -Wq*0.55);
      c.lineTo(Lq*1.12, -Wq*1.70);
      c.closePath(); c.fill();
      c.globalAlpha = 1;
      c.strokeStyle = S._shade(p.steel, 1.15, 0.45);
      c.lineWidth = Math.max(1, Wq*0.040);
      c.beginPath();
      c.moveTo(Lq*0.52, -Wq*1.45); c.lineTo(Lq*1.12, -Wq*0.55); c.stroke();
    }

    /* AN INSET PLATE -- the blade's own outline shrunk about its centre and
       laid back down lighter, so the dark body survives as a RIM the whole way
       round and the weapon reads as two layers of metal. Refs 1 and 2 both do
       this and it is most of why they look machined rather than drawn. */
    if (cf.plate){
      c.save();
      c.translate(cx, cy); c.scale(0.56, 0.56); c.translate(-cx, -cy);
      path();
      c.fillStyle = S._shade(p.steel, 1.02, 0.22);
      c.fill();
      c.strokeStyle = p.glow + "CC"; c.lineWidth = Math.max(1, Wq*0.030);
      c.stroke();
      c.restore();
    }
    c.restore();

    /* THE HONED EDGE, TWICE -- once wide and soft, once tight and bright. One
       stroke reads as an outline. Two read as light coming off an edge, and
       every one of the three references has the second one. */
    const P = SC.pts(Lq, Wq);
    const honed = () => {
      c.beginPath();
      c.moveTo(P.edge[0][0], P.edge[0][1]);
      c.bezierCurveTo(P.edge[1][0],P.edge[1][1],P.edge[2][0],P.edge[2][1],
                      P.edge[3][0],P.edge[3][1]);
      c.stroke();
    };
    c.strokeStyle = p.core + "66"; c.lineWidth = Math.max(1, Wq*0.11); honed();
    c.strokeStyle = p.glow;        c.lineWidth = Math.max(1, Wq*0.055); honed();

    /* A COLD RIM ON THE BACK. The edge opposite the honed one catches a thin
       light line, which is what stops a dark body reading as a hole in the
       picture. */
    if (cf.rim){
      c.save();
      c.strokeStyle = S._shade(p.steel, 1.25, 0.60);
      c.lineWidth = Math.max(1, Wq*0.045);
      const Pb = SC.pts(Lq, Wq);
      const rev = [Pb.edge[3], Pb.edge[2], Pb.edge[1], Pb.edge[0]];
      const b2 = Pb.back.map(function(q, i){
        return [ q[0] + (rev[i][0]-q[0])*BASE.thin,
                 q[1] + (rev[i][1]-q[1])*BASE.thin ]; });
      c.beginPath();
      c.moveTo(b2[0][0], b2[0][1]);
      c.bezierCurveTo(b2[1][0],b2[1][1],b2[2][0],b2[2][1],b2[3][0],b2[3][1]);
      c.stroke();
      c.restore();
    }

    if (cf.socket){
      socket(c, Lq*0.705, Wq*0.145, Wq*0.115, p, null);   // the collar hub
      socket(c, Lq*0.87, -Wq*0.66,  Wq*0.070, p, null);   // mid-blade
    }
  };

  SC.CRAFT = {
    G: function(c,Lq,Wq,p){ SC.snath(c,Lq,Wq,p,SNATH);
                            paint(c,Lq,Wq,p,{ facet:true }); },
    H: function(c,Lq,Wq,p){ SC.snath(c,Lq,Wq,p,SNATH);
                            paint(c,Lq,Wq,p,{ plate:true, rim:true }); },
    I: function(c,Lq,Wq,p){ SC.snath(c,Lq,Wq,p,SNATH);
                            paint(c,Lq,Wq,p,{ plate:true, rim:true,
                                              socket:true }); },
    J: function(c,Lq,Wq,p){ SC.snath(c,Lq,Wq,p,SNATH);
                            paint(c,Lq,Wq,p,{ facet:true, plate:true,
                                              rim:true, socket:true }); }
  };
  Object.assign(SC.ARMS, SC.CRAFT);
  return Object.keys(SC.CRAFT).length;
}"""

CRAFT_ARMS = [
    ("G", "FACETED - the blade as folded planes with a hard spine fold"),
    ("H", "PLATED - a lighter inset plate over a dark body, cold rim light"),
    ("I", "SOCKETED - plated, plus lit gem insets at the hub and mid-blade"),
    ("J", "FULL - facets, plate, rim light and sockets together"),
    ("F", "FLAT - the same silhouette, last round's treatment (the control)"),
]

ARMS = [
    ("A", "FANG — one recurved hook under the head, blade otherwise clean"),
    ("B", "SPINED — the back edge IS six swept spines, growing to the tip"),
    ("C", "SHAFT — clean blade, four knuckles and a finned pommel"),
    ("D", "REAVER — fang, spines and the hot edge together"),
    ("F", "THIN — a narrowed, deeply hooked blade, fang, knuckled shaft"),
    ("E", "SHIPPED _scEaten — the control Rick rejected"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-duskreave.html")
    ap.add_argument("--zoom", type=float, default=3.2)
    ap.add_argument("--craft", action="store_true",
                    help="vary the TREATMENT on one fixed "
                         "silhouette -- the gap Rick named after "
                         "rejecting all six shapes")
    ap.add_argument("--out", default="../05-reference/v63")
    A = ap.parse_args()
    out = HERE / A.out
    out.mkdir(parents=True, exist_ok=True)

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        n = pg.evaluate(PRELUDE)
        print(f"  {n} silhouette arms injected over SHAPES._scEaten")
        arms, name = ARMS, "umbral-scythe-candidates.png"
        if A.craft:
            k = pg.evaluate(CRAFT_JS)
            print(f"  {k} CRAFT arms, all on ONE fixed silhouette (arm F)")
            arms, name = CRAFT_ARMS, "umbral-scythe-craft.png"

        rows = []
        for arm, label in arms:
            panels = []
            # 1080 for the zoom panel; 540 for the other, because 540 is what
            # `cinema_clip` actually captures a short at.
            # ONE PANEL, AT ZOOM. The second column tried to show the delivery
            # register and could not be made honest: cropped at the zoom radius
            # it overflowed the cell, cropped at its own it framed the handle,
            # and sized off the renderer's scale it came out LARGER than the
            # zoom panel beside it. A shape question belongs at zoom (v53), and
            # the scale question is answered by a real arena frame at 540 --
            # `duskreave_sheet.py --arena` -- once an arm is chosen. A column
            # that cannot be trusted is worse than no column.
            for zoom, tag, res in ((A.zoom, "zoom", 1080),):
                ox, oy = res // 2, int(res * 16 / 9) // 2
                got = pg.evaluate(DRAW_JS, {
                    "arm": arm, "L": L, "W": W, "zoom": zoom, "res": res,
                    "ox": ox, "oy": oy, "rot": ROT, "bg": "#0B0710"})
                im = Image.open(io.BytesIO(base64.b64decode(
                    got["png"]))).convert("RGB")
                # THE WEAPON IS DRAWN FROM ITS BUTT, so the origin is one END
                # of it rather than its middle, and the crop has to be centred
                # half a length along the rotation. The radius comes off the
                # renderer's OWN scale instead of a guess: at 540 the guessed
                # one framed the handle and cut the blade off entirely, which
                # made the ships-at column a picture of a stick.
                px = L * zoom * got["scale"]
                r = int(px * 0.95)
                cx = min(max(int(ox + math.cos(ROT) * px * 0.55), r),
                         got["w"] - r)
                cy = min(max(int(oy + math.sin(ROT) * px * 0.55), r),
                         got["h"] - r)
                panels.append((im.crop((cx-r, cy-r, cx+r, cy+r)), tag, zoom))
            rows.append((arm, label, panels))

        # ONE SHEET. A candidate judged on its own page is judged against
        # memory; judged in a row it is judged against its siblings, which is
        # the comparison that is actually being made.
        cell = 330
        sh = Image.new("RGB", (cell + 16, (cell + 34) * len(rows) + 30),
                       (8, 6, 12))
        d = ImageDraw.Draw(sh)
        d.text((8, 8), ("THE UMBRAL SCYTHE - CRAFT, ON ONE FIXED "
                        "SILHOUETTE. Only the treatment moves."
                        if A.craft else
                        "THE UMBRAL SCYTHE - FIVE CANDIDATES AND THE "
                        "SHIPPED ONE (E), at zoom."),
               fill=(210, 200, 230))
        for i, (arm, label, panels) in enumerate(rows):
            y = 30 + i * (cell + 34)
            d.text((8, y + 4), f"{arm}   {label}", fill=(232, 214, 255))
            for j, (im, tag, zoom) in enumerate(panels):
                if zoom == A.zoom:
                    sh.paste(im.resize((cell, cell)), (8, y + 22))
                else:
                    # NATIVE PIXELS, no resize, centred in the cell -- this is
                    # the register the weapon is actually delivered in. The
                    # first cut resized BOTH panels into the same cell, so the
                    # ships-at column was the zoom column upscaled and the two
                    # were the same picture. v56's hand was approved at zoom
                    # and shipped at ~40px as a white scribble; a sheet that
                    # cannot show the delivery register is the instrument that
                    # let that happen.
                    sh.paste(im, (8 + cell + 8 + (cell - im.width) // 2,
                                  y + 22 + (cell - im.height) // 2))
        p = out / name
        sh.save(p)
        print(f"  {p}  {sh.size}")

    if errs:
        print("\n  PAGE ERRORS:", *errs[:6], sep="\n    ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
