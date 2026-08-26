#!/usr/bin/env python3
"""SHATTER — the blade is broken in TWO dimensions, not sliced in one.

    python3 shatter_build.py --src ../02-chain/sc-cardspin.html \
                             --out ../02-chain/sc-shatter.html

THE NOTE THIS ANSWERS
----------------------
Rick, 2026-08-16, on the runic-glass patch:

  > *"better. shards are still purely horizontal. wouldnt glass shards be cut
  >  in every direction?"*

Yes, and this is the correction. `glass_build.py` varied the lengths, the gaps,
the cut angle and the swing — but it never touched the TOPOLOGY. `_conjure`
walks `i = 0..N` along one axis and every piece spans the blade's full height.
That is a **1-D partition**: a baguette sliced. Leaning each slice a few degrees
makes it a baguette sliced at an angle.

Glass does not break like that. A fracture network runs in every direction at
once and the pieces it leaves are wedges, triangles, long obliques — **some of
them only the top half of the plate, some only the bottom, some spanning.** The
tell that a viewer reads instantly is that *no two pieces are the same kind of
shape*, and no 1-D slicer can produce that, at any angle, ever.

HOW THE PARTITION IS BUILT
---------------------------
Recursive binary splitting. Start with one cell covering the blade; repeatedly
take the cell with the largest area and cut it with a straight line at a
hash-chosen angle through a jittered point near its centroid. `cuts` splits
leave `cuts + 1` pieces.

Three properties come free from doing it this way, and all three are things a
scatter of independent polygons could not give:

  - **THE PIECES TILE.** They are a partition, not a collection. Close the gaps
    and the blade comes back whole — the grammar's own law, which the 1-D
    slicer satisfied and a naive "draw some triangles" would not.
  - **EVERY BREAK MATES.** Both faces of a cut are the same straight line. Two
    pieces either side of it are exact complements.
  - **EVERY CELL IS CONVEX**, being an intersection of half-planes. That is what
    makes the daylight exact: see below.

THE DAYLIGHT IS AN INSET, AND IT IS EXACT
------------------------------------------
Generic polygon offsetting is fiddly and degenerate at sharp corners. It is not
needed. A cell here IS a list of half-planes, so pushing every plane inward by
`d` gives the true inset polygon in one line — and the gap between any two
neighbours is **exactly 2d, everywhere, in every direction**, because they share
the plane that separates them. The daylight is uniform by construction rather
than by tuning, and it runs in as many directions as there are cuts.

THE TOPOLOGY IS BUILT ONCE
---------------------------
The fracture depends only on the hashes and the geometry, never on the clock, so
it is computed once and cached on `SHAPES._fx`. Only the per-piece drift and
cant are evaluated per frame. This matters: the splitter does polygon clipping,
and the weapon is drawn twice a frame at 60fps.

WHAT IS DELIBERATELY NOT DONE
------------------------------
This does not touch `_conjure`. The 1-D grammar stays exactly as it shipped and
keeps its three callers, because `_twinConjured` is an approved silhouette and
`_whConjured` rides the same routine. `_gsConjured` is re-pointed at `_shatter`
and nothing else is. `twin_identity.py` proves it: 0 differing pixels on both.

`glass_build.py` is the previous proposal against the same base and is NOT an
ancestor of this one — they are alternatives, not a chain. Build either from
`sc-cardspin.html`.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

PROTECTED = {"sundered-crown.html", "sc-playable.html"}

ANCHOR = """  /* RUNIC GREATSWORD. The grammar's first trip to another type, and the"""

BODY = r"""  /* A DETERMINISTIC HASH. There is no rng anywhere in SHAPES and there is not
     about to be: a fracture that reshuffled itself every frame would read as
     television snow rather than as glass. A weapon has to be broken the same
     way every time you look at it. Pure function of its arguments, no state --
     stable across frames, across page loads, and across the two builds
     `engine_ab.py` compares field for field. */
  _h(i, k){
    const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453;
    return s - Math.floor(s);
  },

  /* ---- convex-polygon primitives. Sutherland-Hodgman and two sums. ------- */
  _clipHP(poly, nx, ny, d){                    // keep n.x <= d
    const out = [];
    for (let i = 0; i < poly.length; i++){
      const A = poly[i], B = poly[(i + 1) % poly.length];
      const da = nx * A[0] + ny * A[1] - d;
      const db = nx * B[0] + ny * B[1] - d;
      if (da <= 0) out.push(A);
      if ((da < 0 && db > 0) || (da > 0 && db < 0)){
        const s = da / (da - db);
        out.push([A[0] + (B[0] - A[0]) * s, A[1] + (B[1] - A[1]) * s]);
      }
    }
    return out;
  },
  _area(poly){
    let a = 0;
    for (let i = 0; i < poly.length; i++){
      const A = poly[i], B = poly[(i + 1) % poly.length];
      a += A[0] * B[1] - B[0] * A[1];
    }
    return Math.abs(a) / 2;
  },
  _centroid(poly){
    let a = 0, x = 0, y = 0;
    for (let i = 0; i < poly.length; i++){
      const A = poly[i], B = poly[(i + 1) % poly.length];
      const w = A[0] * B[1] - B[0] * A[1];
      a += w; x += (A[0] + B[0]) * w; y += (A[1] + B[1]) * w;
    }
    if (Math.abs(a) < 1e-9) return [0, 0];
    return [x / (3 * a), y / (3 * a)];
  },
  /* Inradius of a strip of the same area and perimeter -- a cheap, monotone
     "is this piece a sliver" test. A true inradius needs an LP; this does not,
     and the splitter only has to REJECT slivers, not measure them. */
  _thick(poly){
    let per = 0;
    for (let i = 0; i < poly.length; i++){
      const A = poly[i], B = poly[(i + 1) % poly.length];
      per += Math.hypot(B[0] - A[0], B[1] - A[1]);
    }
    return per < 1e-6 ? 0 : 2 * SHAPES._area(poly) / per;
  },

  /* THE FRACTURE NETWORK, built once and cached.

     Depends only on the hashes and the geometry -- never on the clock -- so
     rebuilding it per frame would be pure waste, and the weapon is drawn twice
     a frame. Keyed on everything that can change its shape.

     Largest-cell-first is what keeps the pieces comparable in size without any
     size term in the objective: cutting the biggest piece each time is a greedy
     balance, and it is why the result reads as one plate that broke rather than
     as a coarse half and a shattered half. The angle is uniform over pi (a line
     has no direction), so cross-cuts, lengthwise splits and obliques all occur
     -- on a 9:1 blade the lengthwise ones are what finally produce pieces that
     are only the TOP half, which is the whole of Rick's note. */
  _fracture(L, W, o){
    const key = [L, W, o.bw, o.gap, o.cuts, o.inset, o.sliceFrom, o.sliceTo].join(":");
    /* A MAP, NOT ONE SLOT. A single cached entry looks sufficient -- the arena
       draws this weapon at one size -- and it is not: the cold open paints the
       fight card OVER the live match, so `_artShape` at `reach * 0.86` and the
       arena at `reach + 6` are both drawn every frame for the length of the
       card. One slot would miss on every single call and rebuild the whole
       partition twice a frame, which is the exact opposite of caching it.
       Bounded the same way `_glowCache` is, and for the same reason. */
    if (!SHAPES._fxc) SHAPES._fxc = new Map();
    const hit = SHAPES._fxc.get(key);
    if (hit) return hit;
    const bw = o.bw;
    const sf = o.sliceFrom === undefined ? o.gap : o.sliceFrom;
    const st = o.sliceTo   === undefined ? L     : o.sliceTo;
    /* The seed rectangle is deliberately LARGER than the blade. Its own edges
       must never appear as a fracture face, and after the inset pushes them in
       they still have to sit outside the profile. */
    const M = bw * 3;
    const rect = [[sf - M, -bw - M], [st + M, -bw - M], [st + M, bw + M], [sf - M, bw + M]];
    const cells = [{ poly: rect, planes: [] }];
    const edges = [];
    const minA = (st - sf) * bw * 2 / (o.cuts + 1) * 0.16;
    const minT = bw * 0.34;
    for (let k = 0; k < o.cuts; k++){
      let bi = 0, ba = -1;
      for (let i = 0; i < cells.length; i++){
        /* Area measured on the cell CLIPPED TO THE BLADE BOX, not on the raw
           polygon. Otherwise the corner cells -- which are mostly the seed
           rectangle's overhang and contain almost no weapon -- look enormous
           and eat every cut, and the blade itself comes out in two pieces. */
        const a = SHAPES._area(SHAPES._clipBox(cells[i].poly, sf, st, bw));
        if (a > ba){ ba = a; bi = i; }
      }
      const C = cells[bi];
      const box = SHAPES._clipBox(C.poly, sf, st, bw);
      const ctr = SHAPES._centroid(box.length ? box : C.poly);
      let cut = null;
      for (let a = 0; a < 8 && !cut; a++){
        const ang = SHAPES._h(k * 17 + a, 3) * Math.PI;
        const nx = Math.cos(ang), ny = Math.sin(ang);
        const px = ctr[0] + (SHAPES._h(k * 17 + a, 5) - 0.5) * o.wander * (st - sf) / (o.cuts + 1);
        const py = ctr[1] + (SHAPES._h(k * 17 + a, 7) - 0.5) * o.wander * bw;
        const d = nx * px + ny * py;
        const A = SHAPES._clipHP(C.poly, nx, ny, d);
        const B = SHAPES._clipHP(C.poly, -nx, -ny, -d);
        if (A.length < 3 || B.length < 3) continue;
        /* Both children have to be real pieces of WEAPON. A cut that shaves a
           sliver, or that only divides the overhang, is rejected and the next
           angle is tried -- eight tries, then the cell is left whole. */
        const ab = SHAPES._clipBox(A, sf, st, bw), bb = SHAPES._clipBox(B, sf, st, bw);
        if (SHAPES._area(ab) < minA || SHAPES._area(bb) < minA) continue;
        if (SHAPES._thick(ab) < minT || SHAPES._thick(bb) < minT) continue;
        cut = { nx, ny, d, A, B };
      }
      if (!cut) continue;
      const pl = C.planes;
      const ca = { poly: cut.A, planes: pl.concat([[ cut.nx,  cut.ny,  cut.d]]) };
      const cb = { poly: cut.B, planes: pl.concat([[-cut.nx, -cut.ny, -cut.d]]) };
      cells[bi] = ca; cells.push(cb);
      /* The shared edge, taken from the child rather than re-derived: it is the
         one edge of A whose two ends both lie on the cutting line. This is what
         the filaments span, so it has to be the real segment and not the whole
         infinite line. */
      let seg = null;
      for (let i = 0; i < cut.A.length && !seg; i++){
        const P = cut.A[i], Q = cut.A[(i + 1) % cut.A.length];
        const dp = Math.abs(cut.nx * P[0] + cut.ny * P[1] - cut.d);
        const dq = Math.abs(cut.nx * Q[0] + cut.ny * Q[1] - cut.d);
        if (dp < 1e-6 && dq < 1e-6) seg = [P, Q];
      }
      if (seg) edges.push({ a: bi, b: cells.length - 1, nx: cut.nx, ny: cut.ny,
                            p: seg[0], q: seg[1] });
    }
    /* The inset polygon, and this is the payoff for keeping the half-planes.
       Pushing every plane in by `inset` is the exact offset of a convex cell --
       no offsetting algorithm, no corner degeneracies -- and two neighbours
       share the plane between them, so the daylight is EXACTLY 2*inset wide
       between every pair, in every direction the cuts happened to run. */
    for (const cell of cells){
      let q = rect;
      for (const pl of cell.planes) q = SHAPES._clipHP(q, pl[0], pl[1], pl[2] - o.inset);
      cell.in = q;
      cell.c  = SHAPES._centroid(q.length ? q : cell.poly);
    }
    if (SHAPES._fxc.size > 24) SHAPES._fxc.clear();
    const out = { key, cells, edges, sf, st };
    SHAPES._fxc.set(key, out);
    return out;
  },
  _clipBox(poly, sf, st, bw){
    let q = SHAPES._clipHP(poly, -1, 0, -sf);
    q = SHAPES._clipHP(q, 1, 0, st);
    q = SHAPES._clipHP(q, 0, -1, bw);
    q = SHAPES._clipHP(q, 0, 1, bw);
    return q;
  },

  /* ===================================================== SHATTER ==========
     Rick, 2026-08-16: *"shards are still purely horizontal. wouldnt glass
     shards be cut in every direction?"*

     `_conjure` walks one axis and every piece spans the full height. This does
     not. See shatter_build.py for the partition; what follows is only how the
     pieces are lit and what holds them apart.

     Deterministic in SHAPES._t and the piece index. No rng. `bladeSegments`
     still derives the hit segment from f.theta, so none of this can move a
     hitbox. */
  _shatter(c, L, W, p, o){
    const t = SHAPES._t || 0;
    const prof = o.prof, bw = o.bw, gap = o.gap;
    const F = SHAPES._fracture(L, W, o);
    const cells = F.cells;

    /* THE MOTION BUDGET. The daylight is 2*inset wide everywhere, and the only
       thing that can close it is two neighbours moving differently. So the
       amplitudes are derived FROM the inset rather than chosen next to it --
       the same discipline the 1-D version needed, but simpler here because the
       gap is uniform and known instead of being the narrowest of six.

       In 2-D the drift is a 2-D vector, so the worst case is both axes aligning
       against the same edge: hence the sqrt(2). */
    const rad = Math.hypot(F.st - F.sf, bw * 2) * 0.5;
    const budget = 2 * o.inset * (1 - o.open);
    const rotMax = Math.min(o.cant, budget * 0.30 / rad);
    const drMax  = Math.max(0, budget * 0.70 - rotMax * rad) / (2 * 1.4143);

    /* The hairline down the axis, drawn FIRST and kept thin: the light is what
       shows THROUGH the breaks, so it has to be narrower than the blade. */
    c.save();
    c.globalCompositeOperation = "lighter";
    const beam = c.createLinearGradient(gap, 0, L, 0);
    beam.addColorStop(0,    p.core + "00");
    beam.addColorStop(0.30, p.core + "CC");
    beam.addColorStop(1,    p.glow);
    c.strokeStyle = beam; c.lineCap = "round";
    c.lineWidth = W * o.beam;
    c.beginPath(); c.moveTo(gap, 0); c.lineTo(L, 0); c.stroke();
    c.restore();

    const pose = [];
    for (let i = 0; i < cells.length; i++){
      /* Amplitude varied DOWNWARD only. The maxima are what close the daylight,
         so a piece swinging further than the budget would spend gap that has
         already been allocated -- invisibly, at one phase of a long period,
         which is the kind of defect that ships. Varying below 1 still breaks
         the lockstep, and lockstep was the complaint. */
      const av = 0.40 + SHAPES._h(i, 91) * 0.60;
      const cvv = 0.40 + SHAPES._h(i, 97) * 0.60;
      const ph = SHAPES._h(i, 41) * 6.283;
      pose.push({ dx: Math.sin(t * 2.1 + ph) * drMax * av,
                  dy: Math.cos(t * 1.7 + ph * 1.31) * drMax * av,
                  rot: Math.sin(t * 1.6 + ph * 0.77) * rotMax * cvv });
    }

    c.lineJoin = "miter"; c.lineCap = "butt";
    for (let i = 0; i < cells.length; i++){
      const cell = cells[i], q = cell.in;
      if (!q || q.length < 3) continue;
      const P = pose[i], cx = cell.c[0], cy = cell.c[1];
      c.save();
      c.translate(cx + P.dx, cy + P.dy); c.rotate(P.rot); c.translate(-cx, -cy);
      c.beginPath();
      c.moveTo(q[0][0], q[0][1]);
      for (let k = 1; k < q.length; k++) c.lineTo(q[k][0], q[k][1]);
      c.closePath();
      c.clip();

      prof(c); c.fillStyle = p.dark; c.fill();                // silhouette
      const g = c.createLinearGradient(cx, -bw, cx, bw);      // lit from above
      g.addColorStop(0,    p.steel);
      g.addColorStop(0.52, p.core);
      g.addColorStop(1,    p.dark);
      prof(c); c.fillStyle = g; c.globalAlpha = 0.94; c.fill(); c.globalAlpha = 1;

      /* TWO VALUE PLANES PER PIECE. One smooth gradient describes a rounded
         metal bevel; glass has FLATS, and a flat is a region of near-constant
         value ending in a hard line. One facet per piece, at its own angle,
         lighter one side and darker the other -- twice the contrast of
         lightening alone, for the same alpha. ONE, not a lattice: a viewer
         reads objects and cannot read a texture. */
      if (o.facet){
        c.save();
        prof(c); c.clip();
        const fl = (SHAPES._h(i, 131) - 0.5) * 1.60;
        const fy = cy + (SHAPES._h(i, 137) - 0.5) * 1.20 * bw;
        const ax = cx - bw * 4, bx = cx + bw * 4;
        const ay = fy + fl * (ax - cx), by = fy + fl * (bx - cx);
        const H = bw * 4;
        c.beginPath();
        c.moveTo(ax, ay); c.lineTo(bx, by); c.lineTo(bx, cy - H); c.lineTo(ax, cy - H);
        c.closePath(); c.fillStyle = p.steel; c.globalAlpha = o.facet; c.fill();
        c.beginPath();
        c.moveTo(ax, ay); c.lineTo(bx, by); c.lineTo(bx, cy + H); c.lineTo(ax, cy + H);
        c.closePath(); c.fillStyle = p.dark; c.globalAlpha = o.facet * 0.85; c.fill();
        c.globalAlpha = Math.min(1, o.facet * 1.9);
        c.strokeStyle = p.glow; c.lineWidth = Math.max(0.5, W * 0.014);
        c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
        c.globalAlpha = 1;
        c.restore();
      }

      /* THE FRACTURE FACES CATCH THE LIGHT. Here every edge of the cell IS a
         fracture -- the seed rectangle's own edges are outside the profile and
         never show -- so the whole polygon is the rim, and the blade's own
         outline is stroked separately afterwards. That separation is exact
         rather than heuristic, which the 1-D version could not manage: it had
         to name x0 and x1 as "the cut edges" by hand. */
      c.save();
      prof(c); c.clip();
      c.beginPath();
      c.moveTo(q[0][0], q[0][1]);
      for (let k = 1; k < q.length; k++) c.lineTo(q[k][0], q[k][1]);
      c.closePath();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.055); c.stroke();
      /* A white core inside the rim. A break in a transparent solid is a lens:
         it gathers light along the edge and throws it back white, brighter than
         anything on the face. One extra stroke on the path already there. */
      if (o.facet){
        c.globalCompositeOperation = "lighter";
        c.strokeStyle = "#FFFFFF"; c.globalAlpha = 0.55;
        c.lineWidth = Math.max(0.5, W * 0.018); c.stroke();
        c.globalAlpha = 1;
      }
      c.restore();

      prof(c);                                                // the blade's own edge
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.045); c.stroke();
      c.restore();
    }

    /* --------------------------------------------------- HELD BY SOMETHING --
       `_conjure` always put real daylight between the pieces and left it EMPTY:
       the thesis is "held by nothing" and *nothing* got taken literally, so the
       honest read was pieces that happen to fly in formation. Formation with no
       cause is a coincidence.

       A filament across every break, spanning it PERPENDICULAR -- which is a
       thing only this version can do, because only here is there a break
       direction to be perpendicular to. Both ends grip the same cut line, so
       each filament joins two points that were the same point before the plate
       came apart. They run at t*5.3 against the drift's t*2.1: a fast binding
       on slow glass says the magic is working and the pieces are heavy. */
    if (o.bind){
      const rot = (P, px, py, cx, cy) => {
        const s = Math.sin(P.rot), k = Math.cos(P.rot);
        return [cx + (px - cx) * k - (py - cy) * s + P.dx,
                cy + (px - cx) * s + (py - cy) * k + P.dy];
      };
      c.save();
      /* CLIPPED TO THE BLADE, and this is not cosmetic. The seed rectangle is
         larger than the weapon, so some cuts divide pieces out in the overhang
         where there is no blade at all -- their shared edge is a real edge of a
         real cell and its filament was drawn faithfully in empty space, a
         scatter of little glowing commas around the weapon. The daylight is by
         definition INSIDE the profile, so clipping to it is exact rather than a
         patch: a filament that lands outside was never spanning anything. */
      prof(c); c.clip();
      c.globalCompositeOperation = "lighter";
      c.lineCap = "round";
      for (let e = 0; e < F.edges.length; e++){
        const E = F.edges[e], A = cells[E.a], B = cells[E.b];
        const PA = pose[E.a], PB = pose[E.b];
        for (let k = 0; k < o.bindN; k++){
          const u = (k + 0.5) / o.bindN + (SHAPES._h(e * 5 + k, 149) - 0.5) * 0.36;
          const uu = Math.min(0.92, Math.max(0.08, u));
          const mx = E.p[0] + (E.q[0] - E.p[0]) * uu;
          const my = E.p[1] + (E.q[1] - E.p[1]) * uu;
          /* Off the shared line by `inset` toward each side: that lands exactly
             on the two faces, because the inset is what pulled them apart. */
          const a0 = rot(PA, mx - E.nx * o.inset, my - E.ny * o.inset, A.c[0], A.c[1]);
          const b0 = rot(PB, mx + E.nx * o.inset, my + E.ny * o.inset, B.c[0], B.c[1]);
          const bow = Math.sin(t * 5.3 + e * 2.1 + k * 1.7) * o.inset * 0.55;
          const midx = (a0[0] + b0[0]) / 2 - E.ny * bow;
          const midy = (a0[1] + b0[1]) / 2 + E.nx * bow;
          const gr = c.createLinearGradient(a0[0], a0[1], b0[0], b0[1]);
          gr.addColorStop(0,   p.glow);
          gr.addColorStop(0.5, p.core + "99");
          gr.addColorStop(1,   p.glow);
          c.strokeStyle = gr;
          c.lineWidth = Math.max(0.5, W * 0.016);
          c.shadowColor = p.core; c.shadowBlur = 7;
          c.globalAlpha = o.bind * (0.55 + 0.45 * Math.sin(t * 5.3 + e * 2.1 + k * 1.7));
          c.beginPath();
          c.moveTo(a0[0], a0[1]); c.quadraticCurveTo(midx, midy, b0[0], b0[1]);
          c.stroke();
        }
      }
      c.restore();
    }

    /* The point is light, not steel: the weapon ends in the thing holding it
       together. */
    c.save();
    c.globalCompositeOperation = "lighter";
    c.fillStyle = "#FFFFFF"; c.shadowColor = p.core; c.shadowBlur = 18;
    c.beginPath(); c.arc(L * 1.02, 0, W * 0.075, 0, TAU); c.fill();
    c.restore();

    /* THE SIGIL, where a hand would be, turning BACKWARDS against the weapon.
       A thing that refuses to turn with what it is carrying cannot be read as a
       grip. The school's whole argument, in one moving object. */
    c.save();
    c.translate(gap * 0.50, 0);
    c.rotate(-t * 2.4);
    c.globalCompositeOperation = "lighter";
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.030);
    c.shadowColor = p.core; c.shadowBlur = 14;
    const rr = W * o.sigil;
    c.beginPath(); c.arc(0, 0, rr, 0, TAU); c.stroke();
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3;
      const x = Math.cos(a) * rr * 0.60, y = Math.sin(a) * rr * 0.60;
      if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
    }
    c.closePath(); c.stroke();
    c.lineWidth = Math.max(1, W * 0.020);
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3 + Math.PI / 3;
      c.beginPath();
      c.moveTo(Math.cos(a) * rr * 1.15, Math.sin(a) * rr * 1.15);
      c.lineTo(Math.cos(a) * rr * 1.55, Math.sin(a) * rr * 1.55);
      c.stroke();
    }
    c.restore();
  },

  /* RUNIC GREATSWORD. The grammar's first trip to another type, and the"""

GS_ANCHOR = r"""    SHAPES._conjure(c, L, W, p, { n:6, gap, bw, prof, frac:0.74,
                                  beam:0.050, drift:0.055, cant:0.060,
                                  sigil:0.30 });"""

GS_BODY = r"""    /* v3, 2026-08-16 -- SHATTERED, not sliced. `_conjure` is untouched and
       still carries the twinblade and the warhammer; this shape alone moves to
       the 2-D partition. See shatter_build.py. */
    SHAPES._shatter(c, L, W, p, { cuts:__CUTS__, gap, bw, prof,
                                  inset:__INSET__, wander:__WANDER__,
                                  open:__OPEN__, beam:0.050, cant:0.075,
                                  facet:__FACET__, bind:__BIND__,
                                  bindN:__BINDN__, sigil:0.30 });"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="../02-chain/sc-shatter.html")
    ap.add_argument("--cuts", type=int, default=9,
                    help="splits; pieces = cuts + 1. A viewer counts objects, so "
                         "this is a legibility knob, not a detail knob.")
    ap.add_argument("--inset", type=float, default=1.9,
                    help="half the daylight, in BLADE UNITS. The gap between any "
                         "two neighbours is exactly twice this, in every "
                         "direction, by construction.")
    ap.add_argument("--wander", type=float, default=0.85,
                    help="how far a cut may stray from the centroid of the piece "
                         "it divides. 0 halves everything down the middle.")
    ap.add_argument("--open", type=float, default=0.30,
                    help="share of the daylight held in reserve when the drift "
                         "and cant amplitudes are derived from it")
    ap.add_argument("--facet", type=float, default=0.16)
    ap.add_argument("--bind", type=float, default=1.0)
    ap.add_argument("--bind-n", type=int, default=1, help="filaments per break")
    A = ap.parse_args()

    out = pathlib.Path(A.out)
    if out.name in PROTECTED:
        print(f"REFUSED -- {out.name} is a shipped artifact.", file=sys.stderr)
        return 1
    src = pathlib.Path(A.src)
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr)
        return 2
    s = src.read_text(encoding="utf-8")

    gs = (GS_BODY.replace("__CUTS__", str(A.cuts))
                 .replace("__INSET__", f"{A.inset:.3f}")
                 .replace("__WANDER__", f"{A.wander:.3f}")
                 .replace("__OPEN__", f"{A.open:.3f}")
                 .replace("__FACET__", f"{A.facet:.3f}")
                 .replace("__BINDN__", str(A.bind_n))
                 .replace("__BIND__", f"{A.bind:.3f}"))

    for name, old, new in (("_shatter + primitives", ANCHOR, BODY),
                           ("_gsConjured -> _shatter", GS_ANCHOR, gs)):
        n = s.count(old)
        if n != 1:
            print(f"! anchor '{name}' hit {n} times, wanted exactly 1. "
                  f"Diff before re-anchoring -- do not loosen it.", file=sys.stderr)
            return 3
        s = s.replace(old, new, 1)

    out.write_text(s, encoding="utf-8")
    print(f"  {A.src} -> {A.out}  (2 anchors)")
    print(f"    {A.cuts + 1} pieces  inset {A.inset} (daylight {A.inset * 2})  "
          f"wander {A.wander}  open {A.open}  bind {A.bind}x{A.bind_n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
