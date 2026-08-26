#!/usr/bin/env python3
"""School grammars for `scythe` and `flailHead`.

The warhammer proved the three-layer system (type / school grammar / cell
flair) and Rick signed off on the row. These are the two types still flat on
`silhouette_probe.py` -- scythe 0.982, flailHead 1.000 -- and they are the real
test of the claim that applying a grammar is REPETITION rather than invention.

Each grammar answers the same question it answered on the hammer, in the
type's own terms:

    runic       what does "in pieces" mean for a curved blade / a ball?
    verdant     what does "grown" mean for a thing that already looks like a
                farm tool / a seed?
    bloodsworn  which way is BACKWARD on a weapon with no obvious front?
    umbral      what is the most alarming place to remove material?
    sanctified  where does the light get out?
    dwarven     what is carrying the load, and can you see it bolted?
    vigil       where do the plates go, and can you count them?
"""

SCYTHE_ANCHOR = '''  scythe(c, L, W, p){
    c.lineCap = "round";'''

SCYTHE_BODY = r'''  /* =============================================================== SCYTHE ==
     Same three layers as the warhammer. `_scBase` is the type; each grammar
     either calls it and modifies, or -- for runic -- refuses it. */
  scythe(c, L, W, p, k, aff){
    const key = p.key || aff;
    if (key === "runic")      return SHAPES._scConjured(c, L, W, p);
    if (key === "verdant")    return SHAPES._scGrown(c, L, W, p);
    if (key === "bloodsworn") return SHAPES._scBarbed(c, L, W, p);
    if (key === "umbral")     return SHAPES._scEaten(c, L, W, p);
    if (key === "sanctified") return SHAPES._scRadiant(c, L, W, p);
    if (key === "dwarven")    return SHAPES._scBuilt(c, L, W, p);
    if (key === "vigil")      return SHAPES._scPlated(c, L, W, p);
    return SHAPES._scBase(c, L, W, p);
  },

  /* The crescent, as a reusable path. Every grammar needs it -- to fill it, to
     clip to it, to stroke a plate along it -- so it is defined once. */
  _scCrescent(c, L, W){
    c.beginPath();
    c.moveTo(L*0.70, W*0.20);
    c.bezierCurveTo(L*1.02, -W*0.20, L*0.98, -W*0.95, L*0.56, -W*1.32);
    c.bezierCurveTo(L*0.88, -W*0.72, L*0.86, -W*0.10, L*0.66, W*0.30);
    c.closePath();
  },

  /* A point on the crescent's OUTER edge, and the outward normal there. The
     barbs, the plates and the bolts all ride this curve, and hand-placing them
     per grammar is how three grammars end up disagreeing about where the back
     of the blade is. */
  _scOuter(L, W, u){
    const p0 = [L*0.70, W*0.20], p1 = [L*1.02, -W*0.20],
          p2 = [L*0.98, -W*0.95], p3 = [L*0.56, -W*1.32];
    const it = 1 - u;
    const b = (a, bq, cq, d) => it*it*it*a + 3*it*it*u*bq + 3*it*u*u*cq + u*u*u*d;
    const db = (a, bq, cq, d) => 3*it*it*(bq-a) + 6*it*u*(cq-bq) + 3*u*u*(d-cq);
    const x = b(p0[0], p1[0], p2[0], p3[0]), y = b(p0[1], p1[1], p2[1], p3[1]);
    const tx = db(p0[0], p1[0], p2[0], p3[0]), ty = db(p0[1], p1[1], p2[1], p3[1]);
    const m = Math.hypot(tx, ty) || 1;
    return { x, y, nx: ty / m, ny: -tx / m, a: Math.atan2(ty, tx) };
  },

  _scBase(c, L, W, p){
    c.lineCap = "round";'''

SCYTHE_GRAMMARS = r'''
  /* --------------------------------------------------------------- RUNIC --
     IN PIECES -- BUT IT IS THE SNATH THAT BREAKS, NOT THE BLADE.

     v1 did what the grammar does everywhere else: deleted the haft and
     fractured the blade. On a scythe that fails, and `silhouette_probe.py` said
     so at IoU 0.162 -- past the 0.303 floor where two different weapon TYPES
     sit. Rick's read of the sheet: a floating arc and a disconnected ball, two
     objects rather than a weapon.

     THE REASON IS PROPORTION. The snath is ~60% of a scythe's footprint, and
     the L -- a long pole with a hook at the far end -- IS the type. Delete it
     and what is left is a crescent, which is a different weapon. On a hammer
     the haft is thin and the head carries the identity, so deleting the haft
     costs nothing; the grammar transferred there and did not transfer here.

     So the flair for this cell inverts which part comes apart. The snath is
     six shards suspended along the line a snath would take -- held by nothing,
     twice as literally as anywhere else, because now the thing being held by
     nothing is the handle. The crescent stays nearly whole, in two pieces, so
     the hook still reads as a hook.

     GENERAL FORM, worth carrying to the remaining types: **runic fractures
     whatever part of the type carries its IDENTITY, which is not always the
     part that carries its mass.** */
  _scConjured(c, L, W, p){
    const t = SHAPES._t || 0;

    /* the line the snath takes, sampled -- the same quadratic _scBase strokes */
    const snath = (u) => {
      const it = 1 - u;
      return { x: 2*it*u*(L*0.44) + u*u*(L*0.70),
               y: 2*it*u*(W*0.30) + u*u*(W*0.16),
               a: Math.atan2(2*it*(W*0.30) + 2*u*(W*0.16 - W*0.30),
                             2*it*(L*0.44) + 2*u*(L*0.70 - L*0.44)) };
    };

    c.save();                                        // light along the whole L
    c.globalCompositeOperation = "lighter";
    /* WIDE. At W*0.045 this was a hairline and the six shards read as six
       objects; `silhouette_probe.py` put runic 0.10 below the cross-type floor
       and Rick's read of the sheet was "two objects rather than a weapon". At
       W*0.095 the light fills the daylight, so the snath reads as ONE thing
       that has come apart -- which is the grammar's actual claim. */
    c.strokeStyle = p.core + "99"; c.lineWidth = W*0.095; c.lineCap = "round";
    c.beginPath();
    c.moveTo(L*0.04, W*0.02);
    c.quadraticCurveTo(L*0.44, W*0.30, L*0.70, W*0.16);
    c.stroke();
    c.restore();

    const NS = 6;                                    // the snath, in pieces
    for (let i = 0; i < NS; i++){
      const u0 = 0.06 + (i / NS) * 0.94, u1 = 0.06 + ((i + 0.80) / NS) * 0.94;
      const q0 = snath(u0), q1 = snath(u1);
      const drift = Math.sin(t * 2.0 + i * 2.3) * W * 0.070;
      const cant  = Math.sin(t * 1.6 + i * 1.4) * 0.10;
      const half  = W * (0.115 - 0.02 * (i / NS));   // tapers toward the collar
      c.save();
      c.translate((q0.x + q1.x) / 2, (q0.y + q1.y) / 2 + drift);
      c.rotate(q0.a + cant);
      const len = Math.hypot(q1.x - q0.x, q1.y - q0.y);
      /* p.dark, not "#040814". A near-black literal is invisible against a
         white-on-black mask and reads as a BLACK BAR through the weapon once
         the matrix is pulled in colour -- the silhouette probe cannot see it
         because the probe flattens every colour to the same white. */
      c.fillStyle = p.dark;
      c.fillRect(-len/2 - W*0.012, -half - W*0.012, len + W*0.024, half*2 + W*0.024);
      const g = c.createLinearGradient(0, -half, 0, half);
      g.addColorStop(0, p.steel); g.addColorStop(0.52, p.core); g.addColorStop(1, p.dark);
      c.fillStyle = g; c.globalAlpha = 0.94;
      c.fillRect(-len/2, -half, len, half*2); c.globalAlpha = 1;
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.032);
      c.strokeRect(-len/2, -half, len, half*2);
      c.restore();
    }

    /* THE HOOK STAYS A HOOK, AND IT IS ONLY CRACKED.

       v2 sliced it into two wedge-clipped pieces and the crescent DID NOT
       RENDER AT ALL -- `_scOuter`'s normal points into the concave side of this
       curve, so the clip wedges were opening away from the blade. The sheet
       showed a sigil and a row of blocks and no hook, which is why the number
       would not move however the daylight was tuned. Caught by looking, not by
       measuring: the metric said 0.20 either way.

       So: draw the crescent whole and punch ONE crack through it. It cannot
       miss, and it is better art -- the fracture ESCALATES toward the hand. Six
       pieces at the grip, a single crack at the far end. The closer to the
       sigil that is holding it, the less of it there is. */
    SHAPES._scCrescent(c, L, W);
    c.fillStyle = p.dark; c.fill();
    const gg = c.createLinearGradient(L*0.55, -W, L*0.95, W*0.2);
    gg.addColorStop(0, p.glow); gg.addColorStop(0.55, p.core); gg.addColorStop(1, p.dark);
    SHAPES._scCrescent(c, L, W);
    c.fillStyle = gg; c.globalAlpha = 0.94; c.fill(); c.globalAlpha = 1;
    SHAPES._scCrescent(c, L, W);
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.045); c.stroke();

    /* A SEAM, NOT A HOLE. This was `destination-out` and it read as a hard
       black bar laid across the blade -- because punching through a shadowed
       draw removes the GLOW too, and on this shape the crack crosses the
       widest, brightest part of the crescent. Filling `p.dark` and lighting
       both faces says "broken" without taking the light out of the weapon, and
       it cannot erase anything. */
    c.save();
    SHAPES._scCrescent(c, L, W); c.clip();
    c.translate(L*0.86, -W*0.42);
    c.rotate(0.55 + Math.sin(t * 1.7) * 0.06);
    c.fillStyle = p.dark;
    c.fillRect(-W*0.62, -W*0.075, W*1.24, W*0.15);
    c.shadowColor = p.core; c.shadowBlur = 10;
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.038);
    c.beginPath();
    c.moveTo(-W*0.62, -W*0.075); c.lineTo(W*0.62, -W*0.075);
    c.moveTo(-W*0.62,  W*0.075); c.lineTo(W*0.62,  W*0.075);
    c.stroke();
    c.restore();

    c.save();                                        // the sigil, at the grip
    c.translate(L*0.03, W*0.01);
    c.rotate(-t * 2.4);
    c.globalCompositeOperation = "lighter";
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.030);
    c.shadowColor = p.core; c.shadowBlur = 14;
    const rr = W * 0.22;
    c.beginPath(); c.arc(0, 0, rr, 0, TAU); c.stroke();
    c.beginPath();
    for (let i = 0; i < 3; i++){
      const a = i * TAU / 3;
      const x = Math.cos(a) * rr * 0.60, y = Math.sin(a) * rr * 0.60;
      if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
    }
    c.closePath(); c.stroke();
    c.restore();
  },

  /* ------------------------------------------------------------- VERDANT --
     GROWN. A scythe is already the most agricultural object in the game, so
     the grammar has to work harder here than anywhere: the answer is that this
     one was never harvested WITH, it grew as a hook.

     THE CELL'S FLAIR: the snath is a runner that puts down two shoots, and the
     crescent is a single enormous THORN with the inner edge serrated into
     smaller thorns -- a bramble's grabbing hook at weapon scale. */
  _scGrown(c, L, W, p){
    const wood = SHAPES._shade(p.dark, 1.30, 0.22);
    c.lineCap = "round"; c.lineJoin = "round";

    c.strokeStyle = wood; c.lineWidth = W*0.15;                 // the runner
    c.beginPath();
    c.moveTo(0, -W*0.06);
    c.quadraticCurveTo(L*0.40, W*0.42, L*0.70, W*0.16);
    c.stroke();
    c.lineWidth = W*0.055;                                      // two shoots
    for (const [sx, sy, ex, ey] of [[0.20, 0.14, 0.30, -0.42],
                                    [0.44, 0.34, 0.56, 0.86]]){
      c.beginPath();
      c.moveTo(L*sx, W*sy);
      c.quadraticCurveTo(L*(sx+ex)*0.5, W*(sy+ey)*0.62, L*ex, W*ey);
      c.stroke();
      c.fillStyle = p.core;
      c.beginPath();
      c.ellipse(L*ex, W*ey, L*0.042, W*0.075, ey > 0 ? 0.7 : -0.7, 0, TAU);
      c.fill();
    }

    SHAPES._scCrescent(c, L, W);                                // the thorn
    const g = c.createLinearGradient(L*0.55, -W, L*0.95, W*0.2);
    g.addColorStop(0, p.glow); g.addColorStop(0.55, p.steel);
    g.addColorStop(1, SHAPES._shade(p.steel, 0.44, 0.38));
    c.fillStyle = g; c.fill();

    /* SMALL. v1 ran these to W*0.46 and turned the crescent inside out -- the
       thorn stopped reading as a blade at all. A grammar has to survive its
       type; see resume-here-v13 §4.2 on the band. */
    c.fillStyle = p.core;                                       // inner serration
    for (let i = 1; i <= 6; i++){
      const q = SHAPES._scOuter(L, W, i / 7);
      c.beginPath();
      c.moveTo(q.x - q.nx * W*0.04, q.y - q.ny * W*0.04);
      c.lineTo(q.x - q.nx * W*0.19 + Math.cos(q.a) * W*0.11,
               q.y - q.ny * W*0.19 + Math.sin(q.a) * W*0.11);
      c.lineTo(q.x - q.nx * W*0.05 + Math.cos(q.a) * W*0.13,
               q.y - q.ny * W*0.05 + Math.sin(q.a) * W*0.13);
      c.closePath(); c.fill();
    }
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);
    c.beginPath();
    c.moveTo(L*0.70, W*0.20);
    c.bezierCurveTo(L*1.02, -W*0.20, L*0.98, -W*0.95, L*0.56, -W*1.32);
    c.stroke();
  },

  /* ---------------------------------------------------------- BLOODSWORN --
     BARBED BACKWARD. On a hammer "backward" was the return stroke. On a scythe
     it is unambiguous: the blade cuts on the INSIDE of the curve, so the barbs
     go on the OUTSIDE, where they drag on the way out.

     THE CELL'S FLAIR: the barbs get longer toward the tip, so the far end of
     the sweep is the part that catches -- which is also the part travelling
     fastest. */
  _scBarbed(c, L, W, p){
    SHAPES._scBase(c, L, W, p);
    c.lineJoin = "miter";
    c.fillStyle = SHAPES._shade(p.steel, 0.74, 0.32);
    c.strokeStyle = SHAPES._shade(p.steel, 0.20, 0.55);
    c.lineWidth = Math.max(1, W*0.03);
    for (let i = 1; i <= 5; i++){
      const u = i / 6;
      const q = SHAPES._scOuter(L, W, u);
      const len = W * (0.19 + 0.30 * u);           // v1 ran to 0.56 and merged
      c.beginPath();
      c.moveTo(q.x, q.y);
      c.lineTo(q.x + q.nx * len - Math.cos(q.a) * len * 0.85,
               q.y + q.ny * len - Math.sin(q.a) * len * 0.85);
      c.lineTo(q.x + Math.cos(q.a) * W * 0.16, q.y + Math.sin(q.a) * W * 0.16);
      c.closePath(); c.fill(); c.stroke();
    }
    const tip = SHAPES._scOuter(L, W, 1.0);                     // and a tip hook
    c.beginPath();
    c.moveTo(tip.x, tip.y);
    c.lineTo(tip.x + W*0.10, tip.y - W*0.52);
    c.lineTo(tip.x + W*0.34, tip.y - W*0.10);
    c.closePath(); c.fill(); c.stroke();
  },

  /* ------------------------------------------------------------- UMBRAL --
     EATEN. THE CELL'S FLAIR: the bites are taken out of the CUTTING edge, so
     the blade has gaps exactly where it is supposed to work, and the snath is
     bitten through just below the collar -- the one joint the whole weapon
     hangs from. */
  _scEaten(c, L, W, p){
    c.save();
    SHAPES._scBase(c, L, W, p);
    c.globalCompositeOperation = "destination-out";
    /* shared path — see _whEaten: destination-out removes the glow too, so an
       un-rimmed bite is a hard black hole in the picture. */
    const bitePath = (bx, by, r, seed) => {
      c.beginPath();
      for (let i = 0; i < 10; i++){
        const a = i * TAU / 10;
        const rr = r * (0.60 + 0.48 * Math.abs(Math.sin(i * 1.9 + seed)));
        const px = bx + Math.cos(a) * rr, py = by + Math.sin(a) * rr;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.closePath();
    };
    const bite = (bx, by, r, seed) => { bitePath(bx, by, r, seed); c.fill(); };
    const RIMS = [];
    /* SMALL, and off the EDGE rather than through the middle. v1 used
       0.30/0.24 centred at W*0.16 inboard and left a sliver, which reads
       as broken rather than eaten. */
    for (const [u, r, s] of [[0.32, 0.17, 0.4], [0.66, 0.14, 2.1]]){
      const q = SHAPES._scOuter(L, W, u);
      RIMS.push([q.x + q.nx * W*0.02, q.y + q.ny * W*0.02, W*r, s]);
    }
    RIMS.push([L*0.685, W*0.155, W*0.13, 1.3]);                 // the joint
    for (const b of RIMS) bite(b[0], b[1], b[2], b[3]);
    c.restore();

    c.save();
    /* THE RIM CARRIES A SHADOW. `destination-out` removes the glow along
       with the metal, and the glow is 90%+ of the lit picture, so an
       un-lit rim still reads as a hard black hole. Giving the rim its own
       shadowBlur puts light back around the absence. */
    c.shadowColor = p.core; c.shadowBlur = 12;
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.040);
    for (const b of RIMS){ bitePath(b[0], b[1], b[2], b[3]); c.stroke(); }
    c.restore();

    c.save();                                                    // what leaks out
    c.globalAlpha = 0.5; c.fillStyle = p.core;
    for (const u of [0.30, 0.62]){
      const q = SHAPES._scOuter(L, W, u);
      c.beginPath();
      c.moveTo(q.x, q.y);
      c.quadraticCurveTo(q.x - q.nx * W*0.9, q.y - q.ny * W*0.9,
                         q.x - q.nx * W*0.5 - Math.cos(q.a) * W*0.5,
                         q.y - q.ny * W*0.5 - Math.sin(q.a) * W*0.5);
      c.quadraticCurveTo(q.x - q.nx * W*0.3, q.y - q.ny * W*0.3, q.x, q.y);
      c.closePath(); c.fill();
    }
    c.globalAlpha = 1;
    c.restore();
  },

  /* ---------------------------------------------------------- SANCTIFIED --
     RADIANT AND PIERCED. THE CELL'S FLAIR: the halo does not sit behind the
     blade the way it does behind a hammer head -- it follows the crescent, a
     second arc standing off the back, so the weapon reads as a sweep of light
     with a blade inside it. The piercings run along the blade's spine. */
  _scRadiant(c, L, W, p){
    c.save();                                                    // the outer arc
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.085);
    c.lineCap = "round";
    c.beginPath();
    c.moveTo(L*0.78, W*0.34);
    c.bezierCurveTo(L*1.26, -W*0.22, L*1.20, -W*1.20, L*0.52, -W*1.66);
    c.stroke();
    c.lineWidth = Math.max(1, W*0.045);                          // and its rays
    for (let i = 1; i <= 4; i++){
      const q = SHAPES._scOuter(L, W, i / 5);
      c.beginPath();
      c.moveTo(q.x + q.nx * W*0.10, q.y + q.ny * W*0.10);
      c.lineTo(q.x + q.nx * W*0.40, q.y + q.ny * W*0.40);
      c.stroke();
    }
    c.restore();

    SHAPES._scBase(c, L, W, p);

    c.save();                                                    // pierced spine
    c.globalCompositeOperation = "destination-out";
    for (let i = 1; i <= 4; i++){
      const q = SHAPES._scOuter(L, W, i / 5);
      c.beginPath();
      c.arc(q.x - q.nx * W*0.30 + Math.cos(q.a) * W*0.02,
            q.y - q.ny * W*0.30 + Math.sin(q.a) * W*0.02,
            W * 0.115, 0, TAU);
      c.fill();
    }
    c.restore();
  },

  /* ------------------------------------------------------------- DWARVEN --
     BUILT. THE CELL'S FLAIR: a scythe's weak point is the tang, where a long
     blade meets a long pole at an angle, so dwarven puts the whole apparatus
     there -- a bolted socket, a diagonal strut back to the snath, and a
     reinforcing spine strap bolted along the crescent's back. It looks like it
     was engineered by someone who did not trust the joint. */
  _scBuilt(c, L, W, p){
    SHAPES._scBase(c, L, W, p);
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);
    c.lineJoin = "round";

    c.strokeStyle = iron; c.lineWidth = W*0.13;                  // spine strap
    c.beginPath();
    const s0 = SHAPES._scOuter(L, W, 0.06);
    c.moveTo(s0.x + s0.nx * W*0.04, s0.y + s0.ny * W*0.04);
    for (let i = 1; i <= 8; i++){
      const q = SHAPES._scOuter(L, W, 0.06 + 0.88 * i / 8);
      c.lineTo(q.x + q.nx * W*0.04, q.y + q.ny * W*0.04);
    }
    c.stroke();
    c.fillStyle = dark;
    for (let i = 0; i <= 3; i++){
      const q = SHAPES._scOuter(L, W, 0.10 + 0.26 * i);
      c.beginPath(); c.arc(q.x + q.nx * W*0.04, q.y + q.ny * W*0.04,
                           W*0.055, 0, TAU); c.fill();
    }

    c.strokeStyle = iron; c.lineWidth = W*0.10;                  // the strut
    c.beginPath();
    c.moveTo(L*0.40, W*0.28); c.lineTo(L*0.70, -W*0.22);
    c.stroke();

    c.fillStyle = iron; c.strokeStyle = dark;                    // bolted socket
    c.lineWidth = Math.max(1, W*0.03);
    c.beginPath();
    c.moveTo(L*0.62, W*0.40); c.lineTo(L*0.80, W*0.30);
    c.lineTo(L*0.78, -W*0.16); c.lineTo(L*0.60, -W*0.06);
    c.closePath(); c.fill(); c.stroke();
    c.fillStyle = dark;
    for (const [bx, by] of [[0.655, 0.28], [0.745, 0.24],
                            [0.655, -0.02], [0.745, -0.06]]){
      c.beginPath(); c.arc(L*bx, W*by, W*0.05, 0, TAU); c.fill();
    }
  },

  /* --------------------------------------------------------------- VIGIL --
     PLATED. THE CELL'S FLAIR: five plates riding the OUTER edge, so the back
     of the blade is armoured and the cutting edge is bare -- the same argument
     the ward makes, that the thing which protects is the thing you present.
     Countable, because five plates read as five things. */
  _scPlated(c, L, W, p){
    SHAPES._scBase(c, L, W, p);
    for (let i = 0; i < 5; i++){
      const q = SHAPES._scOuter(L, W, 0.10 + 0.20 * i);
      c.save();
      c.translate(q.x + q.nx * W*0.10, q.y + q.ny * W*0.10);
      c.rotate(q.a);
      c.fillStyle = p.dark;   c.fillRect(-W*0.28, -W*0.30, W*0.56, W*0.46);
      c.fillStyle = p.core;   c.fillRect(-W*0.22, -W*0.24, W*0.44, W*0.34);
      c.fillStyle = p.glow;   c.fillRect(-W*0.22, -W*0.24, W*0.44, W*0.09);
      c.fillStyle = p.dark;
      c.beginPath(); c.arc(0, -W*0.06, W*0.05, 0, TAU); c.fill();
      c.restore();
    }
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.05);   // snath banding
    for (const gx of [0.16, 0.30, 0.44]){
      const gy = W * (0.30 * (gx / 0.70) * (1.4 - gx));
      c.beginPath();
      c.moveTo(L*gx, gy - W*0.13); c.lineTo(L*gx, gy + W*0.13); c.stroke();
    }
  },
'''

FLAIL_ANCHOR = '''  flailHead(c, D, p, spin){
    const r = D * 0.34;'''

FLAIL_BODY = r'''  /* ============================================================ FLAILHEAD ==
     The only shape with no `aff` argument -- it is called `(c, D, p, spin)` --
     so the grammar dispatches on `p.key` alone. It is also the shape the matrix
     doc calls "genuinely school-neutral", which turned out to mean nobody had
     tried: it scored IoU 1.000, the flattest cell in the game. */
  flailHead(c, D, p, spin){
    const key = p.key;
    if (key === "runic")      return SHAPES._fhConjured(c, D, p, spin);
    if (key === "verdant")    return SHAPES._fhGrown(c, D, p, spin);
    if (key === "bloodsworn") return SHAPES._fhBarbed(c, D, p, spin);
    if (key === "umbral")     return SHAPES._fhEaten(c, D, p, spin);
    if (key === "sanctified") return SHAPES._fhRadiant(c, D, p, spin);
    if (key === "dwarven")    return SHAPES._fhBuilt(c, D, p, spin);
    if (key === "vigil")      return SHAPES._fhPlated(c, D, p, spin);
    return SHAPES._fhBase(c, D, p, spin);
  },

  /* the ball, without its spikes -- every grammar wants a different set */
  _fhBall(c, D, p){
    const r = D * 0.34;
    const g = c.createRadialGradient(-r*0.35, -r*0.35, r*0.08, 0, 0, r);
    g.addColorStop(0, p.steel);
    g.addColorStop(0.6, SHAPES._shade(p.steel, 0.38, 0.42));
    g.addColorStop(1, p.dark);
    c.fillStyle = g;
    c.beginPath(); c.arc(0, 0, r, 0, TAU); c.fill();
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, D*0.028);
    c.beginPath(); c.arc(0, 0, r*0.52, 0, TAU); c.stroke();
    c.beginPath(); c.arc(0, 0, r*0.52, 1.1, 2.4);
    c.lineWidth = Math.max(1, D*0.05); c.stroke();
  },

  _fhBase(c, D, p, spin){
    const r = D * 0.34;'''

FLAIL_GRAMMARS = r'''
  /* --------------------------------------------------------------- RUNIC --
     IN PIECES. THE CELL'S FLAIR: a ball has no length to break along, so it
     breaks the only way a sphere can -- into a shell that has come APART, five
     curved plates orbiting the gap where the mass should be. The spikes are
     gone; what is left is the light that was inside it. */
  _fhConjured(c, D, p, spin){
    const r = D * 0.34, t = SHAPES._t || 0;
    c.save();
    c.rotate(spin);
    c.save();
    c.globalCompositeOperation = "lighter";
    c.fillStyle = p.glow; c.shadowColor = p.core; c.shadowBlur = 20;
    c.beginPath(); c.arc(0, 0, r*0.34, 0, TAU); c.fill();
    c.restore();
    for (let i = 0; i < 5; i++){
      const a = (i / 5) * TAU;
      const out = r * (1.02 + 0.20 * Math.sin(t * 2.0 + i * 1.7));
      const cant = Math.sin(t * 1.5 + i * 2.1) * 0.22;
      c.save();
      c.rotate(a + cant);
      c.translate(out, 0);
      c.fillStyle = p.dark;
      c.beginPath();
      c.moveTo(-r*0.30, -r*0.62); c.lineTo(r*0.34, -r*0.40);
      c.lineTo(r*0.34,  r*0.40);  c.lineTo(-r*0.30,  r*0.62);
      c.closePath(); c.fill();
      const g = c.createLinearGradient(-r*0.30, 0, r*0.34, 0);
      g.addColorStop(0, p.core); g.addColorStop(1, p.steel);
      c.fillStyle = g; c.globalAlpha = 0.94;
      c.beginPath();
      c.moveTo(-r*0.24, -r*0.54); c.lineTo(r*0.28, -r*0.34);
      c.lineTo(r*0.28,  r*0.34);  c.lineTo(-r*0.24,  r*0.54);
      c.closePath(); c.fill(); c.globalAlpha = 1;
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, D*0.022); c.stroke();
      c.restore();
    }
    c.restore();
  },

  /* ------------------------------------------------------------- VERDANT --
     GROWN. THE CELL'S FLAIR: a spiked ball on a chain is a BURR -- the seed
     head that evolved precisely to be spiky and to catch on things. So the
     grammar barely has to reach: the spikes become hooked bristles of uneven
     length, and the ball becomes a seed case with a split down it. */
  _fhGrown(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.strokeStyle = SHAPES._shade(p.steel, 0.66, 0.30);
    c.lineCap = "round"; c.lineJoin = "round";
    for (let i = 0; i < 11; i++){
      const a = (i / 11) * TAU;
      const len = r * (1.55 + 0.55 * Math.abs(Math.sin(i * 2.3)));
      c.lineWidth = Math.max(1, D * 0.030);
      c.beginPath();
      c.moveTo(Math.cos(a) * r * 0.80, Math.sin(a) * r * 0.80);
      c.quadraticCurveTo(Math.cos(a) * len, Math.sin(a) * len,
                         Math.cos(a + 0.30) * len * 0.94,
                         Math.sin(a + 0.30) * len * 0.94);
      c.stroke();
    }
    SHAPES._fhBall(c, D, p);
    c.strokeStyle = SHAPES._shade(p.dark, 1.1, 0.10);            // the split
    c.lineWidth = Math.max(1, D*0.035);
    c.beginPath();
    c.moveTo(-r*0.80, -r*0.30);
    c.quadraticCurveTo(0, r*0.10, r*0.80, -r*0.24);
    c.stroke();
    c.fillStyle = p.glow;                                        // seeds in the split
    for (const sx of [-0.42, 0, 0.42]){
      c.beginPath(); c.arc(r*sx, r*(0.02 - 0.10*Math.abs(sx)), r*0.10, 0, TAU);
      c.fill();
    }
    c.restore();
  },

  /* ---------------------------------------------------------- BLOODSWORN --
     BARBED BACKWARD. THE CELL'S FLAIR: on a ball that spins there is no
     "backward" until you pick one -- so every spike hooks the SAME way round,
     which turns the whole head into a ratchet and states the direction of
     rotation in the silhouette. Nothing else in the game says which way a
     weapon is turning while it is turning. */
  _fhBarbed(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);
    c.strokeStyle = SHAPES._shade(p.steel, 0.20, 0.52);
    c.lineWidth = Math.max(1, D*0.018);
    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.22) * r * 0.92, Math.sin(a - 0.22) * r * 0.92);
      c.quadraticCurveTo(Math.cos(a + 0.34) * r * 1.70,
                         Math.sin(a + 0.34) * r * 1.70,
                         Math.cos(a + 0.86) * r * 1.94,
                         Math.sin(a + 0.86) * r * 1.94);
      c.quadraticCurveTo(Math.cos(a + 0.34) * r * 1.24,
                         Math.sin(a + 0.34) * r * 1.24,
                         Math.cos(a + 0.24) * r * 0.92,
                         Math.sin(a + 0.24) * r * 0.92);
      c.closePath(); c.fill(); c.stroke();
    }
    SHAPES._fhBall(c, D, p);
    c.fillStyle = p.core;
    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU + 0.86;
      c.beginPath();
      c.arc(Math.cos(a) * r * 1.86, Math.sin(a) * r * 1.86, r * 0.13, 0, TAU);
      c.fill();
    }
    c.restore();
  },

  /* ------------------------------------------------------------- UMBRAL --
     EATEN. THE CELL'S FLAIR: half the spikes are simply MISSING, and the ball
     has a crescent bitten out of one side, so the head is visibly lighter on
     one side than the other -- an unbalanced flail, which is the most
     unsettling thing this particular weapon could be. */
  _fhEaten(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.save();
    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);
    for (const i of [0, 1, 3, 6]){                               // four of eight
      const a = (i / 8) * TAU;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.20) * r * 0.92, Math.sin(a - 0.20) * r * 0.92);
      c.lineTo(Math.cos(a + 0.20) * r * 0.92, Math.sin(a + 0.20) * r * 0.92);
      c.lineTo(Math.cos(a) * r * 1.95,        Math.sin(a) * r * 1.95);
      c.closePath(); c.fill();
    }
    c.fillStyle = p.core;
    for (const i of [0, 1, 3, 6]){
      const a = (i / 8) * TAU;
      c.beginPath();
      c.arc(Math.cos(a) * r * 1.80, Math.sin(a) * r * 1.80, r * 0.16, 0, TAU);
      c.fill();
    }
    SHAPES._fhBall(c, D, p);
    c.globalCompositeOperation = "destination-out";              // the bite
    c.beginPath();
    for (let i = 0; i < 12; i++){
      const a = -0.9 + i * (2.2 / 11);
      const rr = r * (1.02 + 0.26 * Math.abs(Math.sin(i * 1.7)));
      const px = r * 0.92 + Math.cos(a) * rr * 0.66;
      const py = -r * 0.70 + Math.sin(a) * rr * 0.66;
      if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
    }
    c.closePath(); c.fill();
    c.restore();

    c.globalAlpha = 0.5; c.fillStyle = p.core;                   // the leak
    c.beginPath();
    c.moveTo(r*0.50, -r*0.56);
    c.quadraticCurveTo(r*1.50, -r*1.30, r*1.90, -r*0.42);
    c.quadraticCurveTo(r*1.20, -r*0.62, r*0.72, -r*0.10);
    c.closePath(); c.fill();
    c.globalAlpha = 1;
    c.restore();
  },

  /* ---------------------------------------------------------- SANCTIFIED --
     RADIANT AND PIERCED. THE CELL'S FLAIR: a spiked ball with holes in it and
     light coming out is a CENSER, which is both the correct liturgical object
     and the only version of this weapon that has ever been swung in a church.
     The halo is a ring around the equator rather than behind the head, because
     a sphere has no behind. */
  _fhRadiant(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, D*0.030);  // the ring
    c.beginPath(); c.ellipse(0, 0, r*2.05, r*0.62, 0, 0, TAU); c.stroke();

    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);            // finials
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.16) * r * 0.94, Math.sin(a - 0.16) * r * 0.94);
      c.lineTo(Math.cos(a + 0.16) * r * 0.94, Math.sin(a + 0.16) * r * 0.94);
      c.lineTo(Math.cos(a) * r * 1.52,        Math.sin(a) * r * 1.52);
      c.closePath(); c.fill();
      c.fillStyle = p.glow;
      c.beginPath();
      c.arc(Math.cos(a) * r * 1.66, Math.sin(a) * r * 1.66, r * 0.16, 0, TAU);
      c.fill();
      c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);
    }
    SHAPES._fhBall(c, D, p);
    c.save();                                                     // pierced
    c.globalCompositeOperation = "destination-out";
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU + 0.5;
      c.beginPath();
      c.arc(Math.cos(a) * r * 0.52, Math.sin(a) * r * 0.52, r * 0.19, 0, TAU);
      c.fill();
    }
    c.restore();
    c.save();                                                     // light inside
    c.globalCompositeOperation = "lighter";
    c.fillStyle = p.glow; c.globalAlpha = 0.55;
    c.beginPath(); c.arc(0, 0, r*0.34, 0, TAU); c.fill();
    c.restore();
    c.restore();
  },

  /* ------------------------------------------------------------- DWARVEN --
     BUILT. THE CELL'S FLAIR: the head is two hemispheres BOLTED TOGETHER along
     a visible equatorial band, and the spikes are separate square studs screwed
     into it rather than forged out of it -- so the silhouette is stepped where
     every other flail's is smooth. */
  _fhBuilt(c, D, p, spin){
    const r = D * 0.34;
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);
    c.save();
    c.rotate(spin);
    c.fillStyle = iron; c.strokeStyle = dark;
    c.lineWidth = Math.max(1, D*0.018);
    for (let i = 0; i < 8; i++){                                  // studs
      const a = (i / 8) * TAU;
      c.save();
      c.translate(Math.cos(a) * r * 1.32, Math.sin(a) * r * 1.32);
      c.rotate(a);
      c.fillRect(-r*0.46, -r*0.30, r*0.92, r*0.60);
      c.strokeRect(-r*0.46, -r*0.30, r*0.92, r*0.60);
      c.fillStyle = dark;
      c.fillRect(r*0.20, -r*0.30, r*0.26, r*0.60);
      c.fillStyle = iron;
      c.restore();
    }
    SHAPES._fhBall(c, D, p);
    c.fillStyle = iron; c.strokeStyle = dark;                     // equator band
    c.fillRect(-r*1.02, -r*0.20, r*2.04, r*0.40);
    c.strokeRect(-r*1.02, -r*0.20, r*2.04, r*0.40);
    c.fillStyle = dark;
    for (const bx of [-0.66, -0.22, 0.22, 0.66]){
      c.beginPath(); c.arc(r*bx, 0, r*0.10, 0, TAU); c.fill();
    }
    c.restore();
  },

  /* --------------------------------------------------------------- VIGIL --
     PLATED. THE CELL'S FLAIR: six plates laid over the sphere like the gores
     of a helmet, each stepping proud of the last, so the ball reads as
     ARMOURED rather than spiked -- and the spikes shorten to studs, because a
     vigil weapon's argument is that it survives the exchange, not that it wins
     the exchange. */
  _fhPlated(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);             // short studs
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU + 0.5;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.20) * r * 0.94, Math.sin(a - 0.20) * r * 0.94);
      c.lineTo(Math.cos(a + 0.20) * r * 0.94, Math.sin(a + 0.20) * r * 0.94);
      c.lineTo(Math.cos(a) * r * 1.34,        Math.sin(a) * r * 1.34);
      c.closePath(); c.fill();
    }
    SHAPES._fhBall(c, D, p);
    for (let i = 0; i < 6; i++){                                   // the gores
      const a = (i / 6) * TAU;
      c.save();
      c.rotate(a);
      c.fillStyle = p.dark;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 1.06, -0.50, 0.02);
      c.closePath(); c.fill();
      c.fillStyle = p.core;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 0.94, -0.44, -0.04);
      c.closePath(); c.fill();
      c.fillStyle = p.glow;
      c.beginPath();
      c.moveTo(0, 0);
      c.arc(0, 0, r * 0.94, -0.44, -0.36);
      c.closePath(); c.fill();
      c.restore();
    }
    c.fillStyle = p.dark;                                          // the boss
    c.beginPath(); c.arc(0, 0, r*0.30, 0, TAU); c.fill();
    c.fillStyle = p.glow;
    c.beginPath(); c.arc(0, 0, r*0.17, 0, TAU); c.fill();
    c.restore();
  },
'''
