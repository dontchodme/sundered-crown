#!/usr/bin/env python3
"""RUNIC GLASS — Axiom's blade stops being a caterpillar.

    python3 glass_build.py --src ../02-chain/sc-cardspin.html \
                           --out ../02-chain/sc-glass.html

THE NOTE THIS ANSWERS
----------------------
Rick, 2026-08-16, on Axiom:

  > *"currently the shards held together to form the blade are a bit too
  >  uniform. im picturing more of a shards of runic glass held together with
  >  glowing magic."*

He is right, and "a bit too uniform" is understating it. Nobody had ever looked
at the fracture geometry itself, because the weapon ships at L=122 W=40 and is
on screen for a few frames at a time while spinning. `axiom_shot.py` draws it at
6x standing still, and at 6x it reads as a **caterpillar**.

THE UNIFORMITY IS FIVE UNIFORMITIES, and only fixing all five changes the read:

    1. every shard is the same LENGTH          u0 = i/N
    2. every gap is the same WIDTH             frac is a constant
    3. every cut is the same VERTICAL LINE     the clip is c.rect()
    4. every shard swings the same DISTANCE    only the phase varies by i
    5. every shard is one smooth GRADIENT      no flats, so no facets

Fix four and the fifth still says "manufactured". (3) is the loudest — six
parallel vertical cuts is a thing a machine does — and (4) is the one that
specifically says *caterpillar*, because equal amplitude on staggered phase is
exactly what an articulated mechanism looks like.

THE SECOND HALF OF THE NOTE IS THE PART THAT WAS NEVER DRAWN
-------------------------------------------------------------
*"held together with glowing magic."* `_conjure` has always put real daylight
between the pieces and left the daylight **empty**. The school's thesis is
"held by nothing" — but *nothing* was taken literally, so the honest read of the
shipped weapon is six shards that happen to be flying in formation, and
formation with no cause is a coincidence rather than a claim.

`bind` draws the cause: filaments across every break, gripping both faces.

THE ONE RULE THE NEW CUT KEEPS
-------------------------------
**Both faces of a break are the SAME fracture, drawn at two different x.** Pull
them together in your head and the pieces mate. That is the grammar's own law —
*"close the gaps and you get the type's outline back"* — and the shipped
vertical cuts satisfied it only by accident, because any two vertical lines
mate. Angled cuts that did not share a profile would quietly break it, and the
weapon would stop reading as one thing that was broken.

It is also what makes the filaments mean something: each one connects two points
that **were the same point** before the blade came apart.

SAFETY — WHY THIS CANNOT MOVE THE OTHER TWO RUNIC CELLS
--------------------------------------------------------
`_conjure` is shared by three callers: `_gsConjured` (n=6, Axiom),
`_whConjured` (n=3) and `_twinConjured` (n=5, a SHIPPED APPROVED silhouette
with a pixel-identity test). Every knob added here is **off at 0 and 0 is the
default**, and each is gated by an `if (jag)` / `if (o.facet)` branch that
leaves the original expressions untouched on the false path — not a
re-parameterisation that happens to evaluate the same. The one arithmetic
change on the shared path is `* av` and `* cv`, which are the literal `1` when
`jag` is 0, and `x * 1` is exact in IEEE754.

`twin_identity.py` is the proof and it is not optional:

    python3 twin_identity.py --a ../02-chain/sc-cardspin.html \
                             --b ../02-chain/sc-glass.html

`--shapes all` puts the same cut on the twinblade and the warhammer. It is for
LOOKING, not for shipping: it moves an approved silhouette by construction and
twin_identity will fail on it, correctly.

RENDER-ONLY
-----------
Deterministic in `SHAPES._t` and the shard index. No rng — `_h` is the standard
sine hash, a pure function of its arguments, so it is stable across frames,
across page loads, and across the two builds `engine_ab.py` compares.
`bladeSegments` still derives the hit segment from `f.theta`. Nothing here can
move a hitbox.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

PROTECTED = {"sundered-crown.html", "sc-playable.html"}

# ---------------------------------------------------------------- the hash --
HASH_ANCHOR = """  _conjure(c, L, W, p, o){
    const t = SHAPES._t || 0;"""

HASH_BODY = r"""  /* A DETERMINISTIC PER-SHARD HASH. There is no rng anywhere in SHAPES and
     there is not about to be: the drift is already a pure function of
     `SHAPES._t`, and a fracture that reshuffled itself every frame would read
     as STATIC -- television snow -- rather than as glass. A weapon has to be
     broken the same way every time you look at it.

     The standard sine hash, and the properties that matter here are that it is
     a pure function of its arguments and that it has no state: stable across
     frames, across page loads, and across the two builds `engine_ab.py`
     compares field for field. */
  _h(i, k){
    const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453;
    return s - Math.floor(s);
  },

  _conjure(c, L, W, p, o){
    const t = SHAPES._t || 0;"""

# ------------------------------------------------------------ the cut loop --
LOOP_ANCHOR = r"""    c.lineJoin = "miter"; c.lineCap = "butt";
    for (let i = 0; i < N; i++){
      const u0 = i / N, u1 = (i + (o.frac || 0.87)) / N;   // the daylight
      const x0 = sf + span * u0, x1 = sf + span * u1;
      const cx = (x0 + x1) / 2;
      const drift = Math.sin(t * 2.1 + i * 2.3) * W * o.drift;
      const cant  = Math.sin(t * 1.6 + i * 1.4) * o.cant;

      c.save();
      c.translate(cx, drift); c.rotate(cant); c.translate(-cx, -drift);
      c.beginPath();
      c.rect(x0, drift - bw * 2.2, x1 - x0, bw * 4.4);
      c.clip();"""

LOOP_BODY = r"""    /* ------------------------------------------------------------ THE CUT --
       Rick, 2026-08-16, on Axiom: *"the shards held together to form the blade
       are a bit too uniform. im picturing more of a shards of runic glass held
       together with glowing magic."*

       Drawn at 6x standing still (`axiom_shot.py`) the shipped cut is six
       pieces of the same LENGTH, separated by gaps of the same WIDTH, cut on
       the same VERTICAL line, swinging the same DISTANCE, out of one smooth
       GRADIENT. Four of those are geometry and the fifth is material, and
       fixing any four still leaves a manufactured object. `jag` is the
       geometry; `facet` is the material; `bind` and `pool` are the magic.

       ALL OF IT IS OFF AT 0 AND 0 IS THE DEFAULT. `_twinConjured` is a shipped,
       approved silhouette and `_whConjured` rides the same routine; every
       branch below leaves their expressions literally untouched rather than
       re-deriving them. `twin_identity.py` is the proof.

       THE RULE THE NEW CUT KEEPS: both faces of a break are the SAME fracture
       drawn at two different x. Pull them together and the pieces mate. That is
       the grammar's own law -- close the gaps and the type's outline comes back
       -- which the vertical cuts satisfied only by accident, since any two
       vertical lines mate. It is also what gives the filaments something to
       mean: each one joins two points that were the same point. */
    const frac = o.frac || 0.87;
    const jag  = o.jag  || 0;
    const H    = bw * 2.2;
    let seg = null, cut = null;
    if (jag){
      const sw = [], gw = [];
      let ss = 0, gs = 0;
      for (let i = 0; i < N; i++){
        sw.push(1 + (SHAPES._h(i, 11) - 0.5) * __LENVAR__ * jag); // shard lengths
        gw.push(1 + (SHAPES._h(i, 23) - 0.5) * __GAPVAR__ * jag); // daylight widths
        ss += sw[i]; gs += gw[i];
      }
      /* NORMALISED, and that is the whole difference between a re-CUT and a
         re-TUNE. The shards still own exactly `frac` of the window and the
         daylight still owns exactly 1-frac; only the division inside each
         changes. `frac` is a MEASURED value -- 0.74 on the greatsword, off an
         IoU sweep against its type-mates -- so widening the daylight here
         would move a tuned silhouette while claiming to be an art change. */
      seg = []; cut = [];
      let x = sf, minGap = Infinity;
      for (let i = 0; i < N; i++){
        const w = span * frac * sw[i] / ss;
        const g = span * (1 - frac) * gw[i] / gs;
        seg.push({ x0: x, x1: x + w, cx: x + w / 2, dr: 0, ct: 0 });
        if (i < N - 1) minGap = Math.min(minGap, g);
        x += w + g;
      }
      /* THE DAYLIGHT IS A HARD BUDGET, AND A LEANING CUT SPENDS IT.
         The two faces of a break are the SAME fracture, so a gap can only
         close one way: the two shards move differently. A face that leans by
         `s` on a neighbour that has drifted `d` further closes the gap by
         `s*d`, and a shard that cants by `ct` closes it by `ct*bw` at the
         blade's edge. Nothing else can.

         v1 picked the lean as a constant and the gaps shut on contact --
         0.73 of lean against 6.6 units of differential drift is 4.8 units of
         closure into a 4.2-unit gap, so the shards overlapped and the weapon
         went back to being solid. The screenshot is unambiguous.

         So the lean is NOT a number here. It is whatever the narrowest gap can
         afford, derived from the amplitudes actually in play, holding `open`
         of that gap in reserve. That scales itself onto any shape the grammar
         travels to, which a constant provably cannot -- the warhammer's `bw`
         is half again the greatsword's and its window is a third the length.

         The consequence is worth stating plainly rather than burying: AT A
         GIVEN `frac` THERE IS A HARD CEILING ON HOW ANGULAR THIS CAN LOOK.
         Wider daylight buys cut angle. That is the same knob `frac` always
         was -- the school's thesis turned up -- and it is a measured trade
         against `silhouette_probe.py`, not a taste one. */
      const dMax = W * o.drift, cMax = o.cant;    // av, cv are <= 1 by design
      const room = minGap * (1 - (o.open === undefined ? 0.25 : o.open))
                 - 2 * cMax * bw;
      const slope = Math.max(0, room) / (2 * dMax);
      /* Split 70/30 between the steady LEAN and the STEP. Both are fracture;
         the lean is the plane the break ran along and the step is where it
         jumped to a new one, and a break with only the first is a saw cut. */
      const lean0 = slope * 0.70;
      const kx0   = slope * 0.30 * (0.35 * H);
      /* N+1 fractures, one per boundary, SHARED by the two shards that face
         each other across it. `ky` is where the break steps. */
      for (let j = 0; j <= N; j++){
        cut.push({ lean: (SHAPES._h(j, 37) - 0.5) * 2 * lean0,
                   kx:   (SHAPES._h(j, 53) - 0.5) * 2 * kx0,
                   ky:   (SHAPES._h(j, 71) - 0.5) * 1.30 * H });
      }
    }
    /* The fracture's own x at height h -- a linear walk of the polyline, used
       both to trace the face and to land a filament ON the break rather than
       merely near it. */
    const fdx = (j, h) => {
      const f = cut[j];
      const d0 = f.lean * (-H), d1 = f.lean * f.ky + f.kx, d2 = f.lean * H;
      return h <= f.ky ? d0 + (d1 - d0) * (h + H) / (f.ky + H || 1)
                       : d1 + (d2 - d1) * (h - f.ky) / (H - f.ky || 1);
    };
    /* One fracture face traced -H to +H at x, with the shard's drift folded
       in. TWO SEGMENTS WITH A STEP: a straight lean is a saw cut at an angle,
       which is still a made thing. The step is what says it was broken. */
    const face = (j, x, dy, down) => {
      const f = cut[j];
      const q = [[x + f.lean * (-H),        dy - H],
                 [x + f.lean * f.ky + f.kx, dy + f.ky],
                 [x + f.lean * ( H),        dy + H]];
      return down ? q : [q[2], q[1], q[0]];
    };
    const trace = (q, move) => {
      if (move) c.moveTo(q[0][0], q[0][1]); else c.lineTo(q[0][0], q[0][1]);
      c.lineTo(q[1][0], q[1][1]); c.lineTo(q[2][0], q[2][1]);
    };

    c.lineJoin = "miter"; c.lineCap = "butt";
    for (let i = 0; i < N; i++){
      const u0 = i / N, u1 = (i + (o.frac || 0.87)) / N;   // the daylight
      const x0 = jag ? seg[i].x0 : sf + span * u0;
      const x1 = jag ? seg[i].x1 : sf + span * u1;
      const cx = (x0 + x1) / 2;
      /* PER-SHARD AMPLITUDE, not merely per-shard phase. The shipped version
         varies only the phase, so all six pieces swing through the same
         distance on staggered timing -- which is precisely what an articulated
         mechanism does, and is most of why the weapon reads as a caterpillar
         rather than as debris held in a field. Exactly 1 when jag is 0, and
         `x * 1` is exact in IEEE754, so the other two callers do not move.

         VARIED DOWNWARD ONLY, and that is deliberate: the drift and cant
         maxima are what close the daylight, so letting a shard swing FURTHER
         than shipped would spend gap budget the lean pass has already
         allocated -- and it would do it invisibly, at one phase of a 20*pi
         period, which is the kind of defect that ships. Below 1 the worst case
         is the shipped worst case, and the lockstep still breaks, because what
         killed the read was every piece moving the SAME distance, not every
         piece moving a large one. */
      const av = jag ? 0.42 + SHAPES._h(i, 91) * 0.58 : 1;
      const cv = jag ? 0.42 + SHAPES._h(i, 97) * 0.58 : 1;
      const drift = Math.sin(t * 2.1 + i * 2.3) * W * o.drift * av;
      const cant  = Math.sin(t * 1.6 + i * 1.4) * o.cant * cv;
      if (jag){ seg[i].dr = drift; seg[i].ct = cant; }

      c.save();
      c.translate(cx, drift); c.rotate(cant); c.translate(-cx, -drift);
      c.beginPath();
      if (jag){
        c.beginPath();
        trace(face(i, x0, drift, true), true);
        trace(face(i + 1, x1, drift, false), false);
        c.closePath();
      } else {
        c.rect(x0, drift - bw * 2.2, x1 - x0, bw * 4.4);
      }
      c.clip();"""

# ------------------------------------------------- facets and the cut faces --
FACE_ANCHOR = r"""      c.save();                                              // the cut faces
      prof(c); c.clip();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.055);
      c.beginPath();
      c.moveTo(x0, drift - bw * 2); c.lineTo(x0, drift + bw * 2);
      c.moveTo(x1, drift - bw * 2); c.lineTo(x1, drift + bw * 2);
      c.stroke();
      c.restore();

      prof(c);
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.045); c.stroke();
      c.restore();
    }"""

FACE_BODY = r"""      /* ------------------------------------------------------ RUNIC GLASS --
         TWO VALUE PLANES PER SHARD. The shipped fill is one smooth vertical
         gradient, which is an accurate description of a rounded metal bevel and
         a bad one of a broken solid. Glass has FLATS, and a flat is a region of
         near-constant value ending in a hard line. One internal facet per
         shard, at its own angle, with the far side a stop lighter: that single
         line is most of the distance between "painted segment" and "cut
         crystal", and it costs one fill and one hairline.

         ONE per shard, deliberately, not a lattice. This project has now
         learned three times that a viewer reads OBJECTS and cannot read a
         TEXTURE -- five ward plates over a continuous arc; discrete marks over
         a pattern; and the runic twinblade's own glyph notches, which were a
         texture pretending to be information. A mesh of facet lines on a 40px
         weapon that is spinning is a texture. */
      if (o.facet){
        c.save();
        prof(c); c.clip();
        const fl = (SHAPES._h(i, 131) - 0.5) * 1.30;         // the facet's lean
        const fy = (SHAPES._h(i, 137) - 0.5) * 1.05 * bw;    // where it crosses
        const ax = x0 - bw * 2, bx = x1 + bw * 2;
        const ay = drift + fy + fl * (ax - cx), by = drift + fy + fl * (bx - cx);
        /* BOTH SIDES, not one. Lightening the near plane alone buys `facet` of
           contrast; lightening one and darkening the other buys nearly twice
           that for the same alpha, and stays subtle enough to survive at 40px.
           A value BREAK is the thing being drawn -- the line is only where it
           happens. */
        c.beginPath();
        c.moveTo(ax, ay); c.lineTo(bx, by);
        c.lineTo(bx, drift - H); c.lineTo(ax, drift - H);
        c.closePath();
        c.fillStyle = p.steel; c.globalAlpha = o.facet; c.fill();
        c.beginPath();
        c.moveTo(ax, ay); c.lineTo(bx, by);
        c.lineTo(bx, drift + H); c.lineTo(ax, drift + H);
        c.closePath();
        c.fillStyle = p.dark; c.globalAlpha = o.facet * 0.85; c.fill();
        c.globalAlpha = Math.min(1, o.facet * 1.9);
        c.strokeStyle = p.glow; c.lineWidth = Math.max(0.5, W * 0.014);
        c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
        c.globalAlpha = 1;
        c.restore();
      }

      c.save();                                              // the cut faces
      prof(c); c.clip();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.055);
      c.beginPath();
      if (jag){
        trace(face(i, x0, drift, true), true);
        trace(face(i + 1, x1, drift, true), true);
      } else {
        c.moveTo(x0, drift - bw * 2); c.lineTo(x0, drift + bw * 2);
        c.moveTo(x1, drift - bw * 2); c.lineTo(x1, drift + bw * 2);
      }
      c.stroke();
      /* A WHITE CORE INSIDE THE FRACTURE RIM. A break in a transparent solid is
         a lens: it gathers light along the edge and throws it back white,
         brighter than anything happening on the face. One extra stroke at a
         third the width, on the path that is already there. It is the cheapest
         "this is glass and not painted metal" available, and it is on the CUT
         edges only -- the profile edge is where the blade always ended, and
         lighting that too would say the whole outline is a fracture. */
      if (o.facet){
        c.globalCompositeOperation = "lighter";
        c.strokeStyle = "#FFFFFF"; c.globalAlpha = 0.55;
        c.lineWidth = Math.max(0.5, W * 0.018); c.stroke();
        c.globalAlpha = 1;
      }
      c.restore();

      prof(c);
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.045); c.stroke();
      c.restore();
    }

    /* --------------------------------------------------- HELD BY SOMETHING --
       The half of the school that has never been drawn. `_conjure` has always
       put real daylight between the pieces and left the daylight EMPTY -- the
       thesis is "held by nothing" and *nothing* got taken literally. So the
       honest read of the shipped weapon is six shards that happen to be flying
       in formation, and formation with no cause is a coincidence rather than a
       claim. Rick asked for the cause.

       LIGHT POOLS IN THE BREAK FIRST, under the filaments, sized to its own
       gap -- so a wide break glows more than a narrow one and the daylight
       stops being a hole. Then the filaments: `bindN` per break, drawn between
       the two facing fracture faces, brightest where they GRIP the glass and
       thinner in the middle, bowed by their own phase so the binding reads as
       something under load.

       They run at t*5.3 against the drift's t*2.1, and that ratio is the whole
       characterisation: a fast binding on slow shards says the magic is working
       and the glass is heavy. Reverse it and the weapon reads as light debris
       in a lazy field, which is the opposite of a greatsword.

       Countable again, and for the same reason as the facet: two per break, not
       a web. A web is a texture.

       EACH FILAMENT JOINS TWO POINTS THAT WERE THE SAME POINT -- both ends read
       the same `fdx(j, h)`, at the shard positions either side of it. That is
       not decoration; it is the mating rule made visible. */
    if (jag && (o.bind || o.pool)){
      const rot = (px, py, ox, oy, a) => {
        const s = Math.sin(a), k = Math.cos(a);
        return [ox + (px - ox) * k - (py - oy) * s,
                oy + (px - ox) * s + (py - oy) * k];
      };
      /* A point ON shard `i`'s face `j`, after that shard's own drift and cant.
         The cant is a rotation about (cx, dr), so the filament has to be rotated
         with it or it will visibly miss the glass on the shards that are canted
         hardest -- which are exactly the ones the eye is drawn to. */
      const grip = (i, x, j, h) => {
        const S = seg[i];
        return rot(x + fdx(j, h), S.dr + h, S.cx, S.dr, S.ct);
      };
      const NB = o.bindN || 2;
      const tipX = L * (o.tipX || 1.02);
      c.save();
      c.globalCompositeOperation = "lighter";
      c.lineCap = "round";
      for (let i = 0; i < N; i++){
        const last = i === N - 1;
        const j = i + 1;
        const gapW = last ? Math.max(1e-3, tipX - seg[i].x1)
                          : seg[i + 1].x0 - seg[i].x1;
        if (o.pool){
          const A = grip(i, seg[i].x1, j, 0);
          const B = last ? [tipX, 0] : grip(i + 1, seg[i + 1].x0, j, 0);
          const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2;
          /* CLAMPED, because the last "gap" is not a gap. Between the final
             shard and the point lies the whole taper, which `frac` leaves
             empty by design -- on the greatsword that is four times the width
             of a real break, and an unclamped pool there put a bloom the size
             of the blade over the tip. It is one gap out of six and it was the
             only one anybody would have noticed. */
          const r  = Math.min(gapW * 0.85, bw * 0.75) + bw * 0.30;
          const gp = c.createRadialGradient(mx, my, 0, mx, my, r);
          gp.addColorStop(0,    p.core + "FF");
          gp.addColorStop(0.45, p.core + "55");
          gp.addColorStop(1,    p.core + "00");
          c.globalAlpha = o.pool * (0.75 + 0.25 * Math.sin(t * 3.7 + i * 1.9));
          c.fillStyle = gp;
          c.beginPath(); c.arc(mx, my, r, 0, TAU); c.fill();
          c.globalAlpha = 1;
        }
        if (!o.bind) continue;
        for (let q = 0; q < NB; q++){
          const h = ((q + 0.5) / NB - 0.5) * 2 * bw
                  * (0.62 + SHAPES._h(i * 7 + q, 149) * 0.46);
          const A = grip(i, seg[i].x1, j, h);
          const B = last ? [tipX, h * 0.22]
                         : grip(i + 1, seg[i + 1].x0, j, h);
          const bow = Math.sin(t * 5.3 + i * 2.1 + q * 1.7) * gapW * 0.30;
          const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2 + bow;
          const gr = c.createLinearGradient(A[0], A[1], B[0], B[1]);
          gr.addColorStop(0,   p.glow);
          gr.addColorStop(0.5, p.core + "99");
          gr.addColorStop(1,   p.glow);
          c.strokeStyle = gr;
          c.lineWidth = Math.max(0.5, W * 0.016);
          c.shadowColor = p.core; c.shadowBlur = 7;
          c.globalAlpha = o.bind * (0.55 + 0.45 * Math.sin(t * 5.3 + i * 2.1 + q * 1.7));
          c.beginPath();
          c.moveTo(A[0], A[1]); c.quadraticCurveTo(mx, my, B[0], B[1]);
          c.stroke();
        }
      }
      c.restore();
    }"""

# ----------------------------------------------------------- the gs callsite --
GS_ANCHOR = r"""    SHAPES._conjure(c, L, W, p, { n:6, gap, bw, prof, frac:0.74,
                                  beam:0.050, drift:0.055, cant:0.060,
                                  sigil:0.30 });"""

GS_BODY = r"""    /* v2, 2026-08-16 -- RUNIC GLASS. `jag`/`facet`/`bind`/`pool` are Rick's
       note on Axiom: the pieces were too uniform and nothing was visibly
       holding them. See glass_build.py for the five uniformities and which knob
       answers which. `frac` is untouched at 0.74 because it is a MEASURED
       value and this is a re-cut, not a re-tune. */
    SHAPES._conjure(c, L, W, p, { n:__N__, gap, bw, prof, frac:__FRAC__,
                                  beam:0.050, drift:0.055, cant:0.060,
                                  sigil:0.30,
                                  jag:__JAG__, facet:__FACET__, open:__OPEN__,
                                  bind:__BIND__, bindN:__BINDN__,
                                  pool:__POOL__ });"""

TB_ANCHOR = r"""    SHAPES._conjure(c, L, W, p, { n:5, gap, bw, prof, frac:0.87,
                                  beam:0.055, drift:0.065, cant:0.075,
                                  sigil:0.26, tipX:1.04, tipR:0.085,
                                  dark:"#040814" });"""

TB_BODY = r"""    SHAPES._conjure(c, L, W, p, { n:5, gap, bw, prof, frac:0.87,
                                  beam:0.055, drift:0.065, cant:0.075,
                                  sigil:0.26, tipX:1.04, tipR:0.085,
                                  dark:"#040814",
                                  jag:__JAG__, facet:__FACET__, open:__OPEN__,
                                  bind:__BIND__, bindN:__BINDN__,
                                  pool:__POOL__ });"""

WH_ANCHOR = r"""    SHAPES._conjure(c, L, W, p, { n:3, gap, bw:hh, prof, frac:0.76,
                                  sliceFrom:L*0.56, sliceTo:L*1.0,
                                  beam:0.040, drift:0.050, cant:0.045,
                                  sigil:0.26 });"""

WH_BODY = r"""    SHAPES._conjure(c, L, W, p, { n:3, gap, bw:hh, prof, frac:0.76,
                                  sliceFrom:L*0.56, sliceTo:L*1.0,
                                  beam:0.040, drift:0.050, cant:0.045,
                                  sigil:0.26,
                                  jag:__JAG__, facet:__FACET__, open:__OPEN__,
                                  bind:__BIND__, bindN:__BINDN__,
                                  pool:__POOL__ });"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="../02-chain/sc-cardspin.html")
    ap.add_argument("--out", default="../02-chain/sc-glass.html")
    ap.add_argument("--shapes", default="greatsword",
                    help="greatsword (Axiom only, the default) or 'all' — all "
                         "MOVES AN APPROVED SILHOUETTE and twin_identity.py "
                         "will fail on it, correctly. For looking, not shipping.")
    ap.add_argument("--n", type=int, default=6, help="shards")
    ap.add_argument("--frac", type=float, default=0.74,
                    help="share of the window the shards own. MEASURED off an "
                         "IoU sweep; moving it re-tunes the silhouette.")
    ap.add_argument("--jag", type=float, default=0.85,
                    help="fracture irregularity 0..1 — lengths, gaps, cut "
                         "angles, the step in each break, and per-shard swing")
    ap.add_argument("--facet", type=float, default=0.16,
                    help="alpha of the second value plane. 0 = one gradient")
    ap.add_argument("--bind", type=float, default=1.0,
                    help="filament strength across each break. 0 = nothing "
                         "visibly holds the blade together")
    ap.add_argument("--bind-n", type=int, default=2, help="filaments per break")
    ap.add_argument("--lenvar", type=float, default=1.15,
                    help="spread of shard LENGTHS, as a fraction either side "
                         "of equal. Free: a short shard costs no daylight.")
    ap.add_argument("--gapvar", type=float, default=0.90,
                    help="spread of DAYLIGHT widths. Not free: the narrowest "
                         "gap sets the cut-angle budget for every break, so "
                         "spread here is paid for in fracture angle everywhere.")
    ap.add_argument("--open", type=float, default=0.25,
                    help="share of the NARROWEST gap held in reserve when the "
                         "cut lean is derived. Higher = more daylight "
                         "guaranteed and a flatter, more vertical fracture. "
                         "This is the safety margin, not the look.")
    ap.add_argument("--pool", type=float, default=0.30,
                    help="light pooling in each break. Watch this one: the "
                         "silhouette probe flattens it to WHITE, so too much "
                         "fills the daylight and the grammar's IoU rises.")
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

    def sub(name: str, old: str, new: str) -> bool:
        nonlocal s
        n = s.count(old)
        if n != 1:
            print(f"! anchor '{name}' hit {n} times, wanted exactly 1. "
                  f"Diff before re-anchoring -- do not loosen it.", file=sys.stderr)
            return False
        s = s.replace(old, new, 1)
        return True

    def opts(body: str) -> str:
        return (body.replace("__JAG__", f"{A.jag:.3f}")
                    .replace("__FACET__", f"{A.facet:.3f}")
                    .replace("__BINDN__", str(A.bind_n))
                    .replace("__BIND__", f"{A.bind:.3f}")
                    .replace("__POOL__", f"{A.pool:.3f}")
                    .replace("__OPEN__", f"{A.open:.3f}")
                    .replace("__LENVAR__", f"{A.lenvar:.3f}")
                    .replace("__GAPVAR__", f"{A.gapvar:.3f}")
                    .replace("__FRAC__", f"{A.frac:.3f}")
                    .replace("__N__", str(A.n)))

    edits = [("_h hash helper", HASH_ANCHOR, HASH_BODY),
             ("the cut loop", LOOP_ANCHOR, opts(LOOP_BODY)),
             ("facets + cut faces + binding", FACE_ANCHOR, FACE_BODY),
             ("_gsConjured options", GS_ANCHOR, opts(GS_BODY))]
    if A.shapes == "all":
        edits += [("_twinConjured options", TB_ANCHOR, opts(TB_BODY)),
                  ("_whConjured options", WH_ANCHOR, opts(WH_BODY))]
    elif A.shapes != "greatsword":
        print(f"! --shapes must be 'greatsword' or 'all'", file=sys.stderr)
        return 4

    for name, old, new in edits:
        if not sub(name, old, new):
            return 3

    out.write_text(s, encoding="utf-8")
    print(f"  {A.src} -> {A.out}  ({len(edits)} anchors, {A.shapes})")
    print(f"    jag {A.jag}  facet {A.facet}  bind {A.bind}x{A.bind_n}  "
          f"pool {A.pool}  n {A.n}  frac {A.frac}")
    if A.shapes == "greatsword":
        print("    next: twin_identity.py must read 0 differing pixels, and "
              "silhouette_probe.py --types greatsword must stay in the band")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
