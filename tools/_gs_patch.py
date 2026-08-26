#!/usr/bin/env python3
"""School grammars for `greatsword` — the six schools the runic branch left flat.

The greatsword is the matrix contact sheet's worst cell ("almost pure
silhouette-plus-glow") and the most-watched weapon in the game: Dawnbringer and
Lightkeeper both carry it, and Dawnbringer is in nearly every judge render ever
pulled. It was still on two outlines.

Every grammar here calls `_gsBase` first and then adds or removes. Runic
already had its own branch and is untouched.
"""

GS_ANCHOR = '''    if ((p.key || aff) === "runic") return SHAPES._gsConjured(c, L, W, p);
    const bh = W * 0.19;                                       // blade half-height'''

GS_BODY = r'''    const key = p.key || aff;
    if (key === "runic")      return SHAPES._gsConjured(c, L, W, p);
    if (key === "verdant")    return SHAPES._gsGrown(c, L, W, p);
    if (key === "bloodsworn") return SHAPES._gsBarbed(c, L, W, p);
    if (key === "umbral")     return SHAPES._gsEaten(c, L, W, p);
    if (key === "sanctified") return SHAPES._gsRadiant(c, L, W, p);
    if (key === "dwarven")    return SHAPES._gsBuilt(c, L, W, p);
    if (key === "vigil")      return SHAPES._gsPlated(c, L, W, p);
    return SHAPES._gsBase(c, L, W, p);
  },

  /* the blade outline on its own -- every grammar clips to it, fills it or
     eats it, and three of them disagreeing about where the edge is would show */
  _gsBlade(c, L, W){
    const bh = W * 0.19;
    c.beginPath();
    c.moveTo(L*0.225, -bh);
    c.lineTo(L*0.795, -bh*0.90);
    c.lineTo(L,        0);
    c.lineTo(L*0.795,  bh*0.90);
    c.lineTo(L*0.225,  bh);
    c.closePath();
  },

  _gsBase(c, L, W, p){
    const bh = W * 0.19;                                       // blade half-height'''

GS_GRAMMARS = r'''
  /* ---------------------------------------------------------- SANCTIFIED --
     RADIANT AND PIERCED. THE CELL'S FLAIR: on a hammer the halo stood off
     behind the head; a sword has no behind, so the light goes into the GUARD.
     The crossguard becomes a pair of swept wings with a ring between them, and
     the fuller becomes a row of piercings -- so the one part of a greatsword
     that is already a horizontal bar becomes the part that radiates. */
  _gsRadiant(c, L, W, p){
    const bh = W * 0.19;
    c.save();
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.055);  // the ring
    c.beginPath(); c.arc(L*0.19, 0, W*0.60, 0, TAU); c.stroke();
    c.fillStyle = p.core;                                        // the wings
    for (const sg of [-1, 1]){
      c.beginPath();
      c.moveTo(L*0.155, sg * W*0.16);
      c.quadraticCurveTo(L*0.02, sg * W*1.10, L*0.29, sg * W*1.02);
      c.quadraticCurveTo(L*0.26, sg * W*0.52, L*0.225, sg * W*0.16);
      c.closePath(); c.fill();
    }
    c.restore();

    SHAPES._gsBase(c, L, W, p);

    c.save();                                                    // pierced fuller
    c.globalCompositeOperation = "destination-out";
    for (let i = 0; i < 5; i++){
      c.beginPath();
      c.arc(L*(0.32 + 0.10*i), 0, bh*(0.42 - 0.045*i), 0, TAU);
      c.fill();
    }
    c.restore();
  },

  /* ------------------------------------------------------------- DWARVEN --
     BUILT. THE CELL'S FLAIR: a sword is the hardest thing in the game to
     believe was ASSEMBLED, so this one is honest about it -- two cheek plates
     riveted to a central spine that runs out past them, and the point is a
     CHISEL rather than a taper, because a bolted blade cannot come to a forged
     edge. The tip is the tell and it is visible at any size. */
  _gsBuilt(c, L, W, p){
    const bh = W * 0.19;
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);

    c.fillStyle = SHAPES._shade(p.dark, 1.20, 0.30);             // grip
    c.fillRect(0, -W*0.085, L*0.135, W*0.17);
    c.fillStyle = p.core;
    c.beginPath(); c.arc(-L*0.012, 0, W*0.115, 0, TAU); c.fill();
    c.fillStyle = p.core;                                        // crossguard
    c.beginPath();
    c.moveTo(L*0.135, -W*0.50); c.lineTo(L*0.185, -W*0.40);
    c.lineTo(L*0.185,  W*0.40); c.lineTo(L*0.135,  W*0.50);
    c.closePath(); c.fill();

    c.fillStyle = iron;                                          // the spine
    c.fillRect(L*0.185, -bh*0.34, L*0.845, bh*0.68);
    c.beginPath();                                               // chisel point
    c.moveTo(L*1.03, -bh*0.34); c.lineTo(L*1.03, bh*0.34);
    c.lineTo(L*0.90, bh*0.34); c.lineTo(L*0.90, -bh*0.34);
    c.closePath(); c.fill();

    for (const sg of [-1, 1]){                                   // cheek plates
      c.beginPath();
      c.moveTo(L*0.235, sg * bh*0.18);
      c.lineTo(L*0.235, sg * bh);
      c.lineTo(L*0.86,  sg * bh*0.80);
      c.lineTo(L*0.86,  sg * bh*0.16);
      c.closePath();
      const g = c.createLinearGradient(0, sg*bh, 0, 0);
      g.addColorStop(0, SHAPES._shade(p.steel, 0.46, 0.45));
      g.addColorStop(1, p.steel);
      c.fillStyle = g; c.fill();
      c.strokeStyle = dark; c.lineWidth = Math.max(1, W*0.030); c.stroke();
    }
    c.fillStyle = dark;                                          // the rivets
    for (const rx of [0.30, 0.45, 0.60, 0.75]) for (const ry of [-0.62, 0.62]){
      c.beginPath(); c.arc(L*rx, bh*ry, W*0.045, 0, TAU); c.fill();
    }
    c.fillStyle = iron;                                          // and a collar
    c.fillRect(L*0.195, -bh*1.20, L*0.045, bh*2.40);
    c.strokeStyle = dark; c.lineWidth = Math.max(1, W*0.028);
    c.strokeRect(L*0.195, -bh*1.20, L*0.045, bh*2.40);
  },

  /* ---------------------------------------------------------- BLOODSWORN --
     BARBED BACKWARD. THE CELL'S FLAIR: a sword has a front and a back edge, so
     unlike the hammer or the ball there is no ambiguity -- the false edge grows
     four rearward hooks and the crossguard sweeps DOWN into two more, so the
     whole weapon rakes on the return. The cutting edge is left clean, which is
     what makes the barbs read as deliberate rather than as damage. */
  _gsBarbed(c, L, W, p){
    const bh = W * 0.19;
    SHAPES._gsBase(c, L, W, p);
    c.lineJoin = "miter";
    c.fillStyle = SHAPES._shade(p.steel, 0.74, 0.32);
    c.strokeStyle = SHAPES._shade(p.steel, 0.20, 0.52);
    c.lineWidth = Math.max(1, W*0.028);
    for (let i = 0; i < 4; i++){                                 // back-edge hooks
      const x = L * (0.34 + 0.14 * i);
      c.beginPath();
      c.moveTo(x,            bh*0.96);
      c.lineTo(x - L*0.075,  bh*2.10);
      c.lineTo(x + L*0.030,  bh*1.16);
      c.closePath(); c.fill(); c.stroke();
    }
    for (const sg of [-1, 1]){                                   // guard, swept down
      c.beginPath();
      c.moveTo(L*0.150, sg * W*0.30);
      c.quadraticCurveTo(L*0.075, sg * W*1.02, L*0.185, sg * W*0.96);
      c.quadraticCurveTo(L*0.175, sg * W*0.56, L*0.205, sg * W*0.26);
      c.closePath(); c.fill(); c.stroke();
    }
    c.fillStyle = p.core;                                        // a fed notch
    c.beginPath();
    c.moveTo(L*0.885, -bh*0.52); c.lineTo(L*0.955, -bh*0.10);
    c.lineTo(L*0.885, -bh*0.04);
    c.closePath(); c.fill();
  },

  /* ------------------------------------------------------------- VERDANT --
     GROWN. THE CELL'S FLAIR: a long straight blade is a LEAF, which is the one
     place this grammar gets an easier ride than anywhere else -- so it takes
     the harder version. The blade is a leaf with a serrated margin and a
     visible midrib, the guard is two curling shoots, and the grip is a length
     of stem that has not been stripped. */
  _gsGrown(c, L, W, p){
    const bh = W * 0.19;
    const wood = SHAPES._shade(p.dark, 1.28, 0.22);
    c.lineCap = "round"; c.lineJoin = "round";

    c.strokeStyle = wood; c.lineWidth = W*0.17;                  // the stem
    c.beginPath(); c.moveTo(-L*0.01, W*0.02); c.lineTo(L*0.20, 0); c.stroke();
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.042);  // two shoots
    for (const sg of [-1, 1]){
      c.beginPath();
      c.moveTo(L*0.175, sg * W*0.05);
      c.quadraticCurveTo(L*0.10, sg * W*0.72, L*0.27, sg * W*0.66);
      c.stroke();
    }

    c.beginPath();                                               // the leaf
    c.moveTo(L*0.20, 0);
    c.bezierCurveTo(L*0.34, -bh*1.55, L*0.72, -bh*1.45, L*1.00, 0);
    c.bezierCurveTo(L*0.72,  bh*1.45, L*0.34,  bh*1.55, L*0.20, 0);
    c.closePath();
    const g = c.createLinearGradient(0, -bh*1.5, 0, bh*1.5);
    g.addColorStop(0, p.glow); g.addColorStop(0.5, p.steel);
    g.addColorStop(1, SHAPES._shade(p.steel, 0.46, 0.38));
    c.fillStyle = g; c.fill();

    c.fillStyle = p.core;                                        // serrated margin
    for (let i = 1; i <= 7; i++){
      const u = i / 8;
      const x = L * (0.20 + 0.80 * u);
      const y = bh * 1.50 * Math.sin(Math.PI * u) * 0.96;
      for (const sg of [-1, 1]){
        c.beginPath();
        c.moveTo(x - L*0.035, sg * y * 0.94);
        c.lineTo(x + L*0.015, sg * (y + bh*0.55));
        c.lineTo(x + L*0.045, sg * y * 0.90);
        c.closePath(); c.fill();
      }
    }
    c.strokeStyle = SHAPES._shade(p.dark, 1.1, 0.12);            // the midrib
    c.lineWidth = Math.max(1, W*0.045);
    c.beginPath(); c.moveTo(L*0.22, 0); c.lineTo(L*0.98, 0); c.stroke();
    c.lineWidth = Math.max(1, W*0.024);                          // and its veins
    for (let i = 1; i <= 5; i++){
      const u = i / 6, x = L * (0.24 + 0.68 * u);
      const y = bh * 1.40 * Math.sin(Math.PI * u);
      for (const sg of [-1, 1]){
        c.beginPath();
        c.moveTo(x - L*0.05, 0); c.lineTo(x + L*0.03, sg * y * 0.72); c.stroke();
      }
    }
  },

  /* -------------------------------------------------------------- UMBRAL --
     EATEN. THE CELL'S FLAIR: the POINT is gone. On a hammer the bite went
     through the haft; on a sword the most alarming thing you can remove is the
     part that does the work, so this blade ends in a broken stump two thirds of
     the way along, with the rest of it eaten out of the edges. A greatsword's
     whole property is reach, and umbral's is that the damage is permanent. */
  _gsEaten(c, L, W, p){
    const bh = W * 0.19;
    c.save();
    SHAPES._gsBase(c, L, W, p);
    c.globalCompositeOperation = "destination-out";
    const bite = (bx, by, r, seed) => {
      c.beginPath();
      for (let i = 0; i < 10; i++){
        const a = i * TAU / 10;
        const rr = r * (0.58 + 0.50 * Math.abs(Math.sin(i * 1.9 + seed)));
        const px = bx + Math.cos(a) * rr, py = by + Math.sin(a) * rr;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.closePath(); c.fill();
    };
    /* the point, taken off with a ragged edge rather than a clean cut */
    c.beginPath();
    c.moveTo(L*0.70, -bh*1.6);
    c.lineTo(L*0.78, -bh*0.55); c.lineTo(L*0.72, -bh*0.05);
    c.lineTo(L*0.80,  bh*0.40); c.lineTo(L*0.74,  bh*1.6);
    c.lineTo(L*1.30,  bh*1.6);  c.lineTo(L*1.30, -bh*1.6);
    c.closePath(); c.fill();
    bite(L*0.36, -bh*0.92, bh*0.80, 0.4);                        // out of the edges
    bite(L*0.56,  bh*0.98, bh*0.66, 2.1);
    bite(L*0.16,  0,       bh*0.55, 1.3);                        // and the guard
    c.restore();

    c.save();                                                    // what leaks out
    c.globalAlpha = 0.5; c.fillStyle = p.core;
    c.beginPath();
    c.moveTo(L*0.76, -bh*0.30);
    c.quadraticCurveTo(L*1.02, -bh*1.30, L*1.12, -bh*0.10);
    c.quadraticCurveTo(L*0.94, -bh*0.42, L*0.78,  bh*0.26);
    c.closePath(); c.fill();
    c.globalAlpha = 1;
    c.restore();
  },

  /* --------------------------------------------------------------- VIGIL --
     PLATED. THE CELL'S FLAIR: on a bow the plates lie along the limbs, on a
     hammer they stack up the head. On a sword they run down the blade like the
     lames of a vambrace, each stepping proud of the one before, so the edge is
     a STAIRCASE rather than a line -- and the crossguard becomes a small shield
     with the same plate on it. Countable: five lames. */
  _gsPlated(c, L, W, p){
    const bh = W * 0.19;
    SHAPES._gsBase(c, L, W, p);

    c.fillStyle = p.dark;                                        // the guard shield
    c.beginPath();
    c.moveTo(L*0.130, -W*0.62); c.lineTo(L*0.215, -W*0.50);
    c.lineTo(L*0.215,  W*0.50); c.lineTo(L*0.130,  W*0.62);
    c.closePath(); c.fill();
    c.fillStyle = p.core;
    c.fillRect(L*0.148, -W*0.40, L*0.052, W*0.80);
    c.fillStyle = p.glow;
    c.fillRect(L*0.148, -W*0.40, L*0.052, W*0.20);

    for (let i = 0; i < 5; i++){                                 // five lames
      const x = L * (0.255 + 0.145 * i);
      const h = bh * (1.28 - 0.13 * i);
      c.fillStyle = p.dark;
      c.fillRect(x, -h, L*0.130, h*2);
      c.fillStyle = p.core;
      c.fillRect(x + L*0.012, -h*0.84, L*0.106, h*1.68);
      c.fillStyle = p.glow;
      c.fillRect(x + L*0.012, -h*0.84, L*0.106, h*0.26);
      c.fillStyle = p.dark;
      c.beginPath(); c.arc(x + L*0.065, 0, W*0.038, 0, TAU); c.fill();
    }
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.040);  // grip banding
    for (const gx of [0.035, 0.070, 0.105]){
      c.beginPath();
      c.moveTo(L*gx, -W*0.10); c.lineTo(L*gx, W*0.10); c.stroke();
    }
  },
'''
