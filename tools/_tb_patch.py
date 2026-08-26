#!/usr/bin/env python3
"""School grammars for `twinblade` and `bow` — the last two flat types.

twinblade had runic only (IoU 0.403); bow had dwarven and vigil only (0.622).
Both already carried the branch MECHANISM, which is why they were the two rows
that were not pixel-identical to begin with — they just never got the other
five schools.

The bow is handled differently from every other type on purpose: its branch is
an `else if` chain *inside* the shared routine, between the limbs and the
string, rather than a dispatcher at the top. That structure was already there
and it is the better one for this shape — the limb curve, the string, the riser
and the bolt are what make a bow read as a bow at 54 units, and no grammar
should be able to lose them.
"""

# --------------------------------------------------------------- twinblade --

TB_ANCHOR = '''    const key = p.key || aff;
    if (key === "runic") return SHAPES._twinConjured(c, L, W, p);
    return SHAPES._twinDagger(c, L, W, p);'''

TB_BODY = '''    const key = p.key || aff;
    if (key === "runic")      return SHAPES._twinConjured(c, L, W, p);
    if (key === "verdant")    return SHAPES._tbGrown(c, L, W, p);
    if (key === "bloodsworn") return SHAPES._tbBarbed(c, L, W, p);
    if (key === "umbral")     return SHAPES._tbEaten(c, L, W, p);
    if (key === "sanctified") return SHAPES._tbRadiant(c, L, W, p);
    if (key === "dwarven")    return SHAPES._tbBuilt(c, L, W, p);
    if (key === "vigil")      return SHAPES._tbPlated(c, L, W, p);
    return SHAPES._twinDagger(c, L, W, p);'''

TB_GRAMMARS = r'''
  /* ============================================== TWINBLADE, PER SCHOOL ==
     The type is the shortest and fastest in the game -- reach 62, spin 5.7,
     drawn TWICE at blade offsets 0 and 0.5. Two consequences that no other
     type has:

       - everything here is drawn twice, so every grammar costs double
       - at spin 5.7 the pair reads as a spinning cross, and the thing a viewer
         actually sees is the OUTER TRACE of the two blades. So a grammar that
         changes the tip or the back edge shows; one that changes the grip is
         almost invisible.

     Each therefore puts its structure at the far end. */

  /* SANCTIFIED. Pierced, and the guard becomes a ring -- the smallest possible
     version of the halo, because at this reach anything larger would be a
     wheel with a knife through it. */
  _tbRadiant(c, L, W, p){
    const bh = W * 0.17;
    c.save();
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.075);
    c.beginPath(); c.arc(L*0.33, 0, W*0.42, 0, TAU); c.stroke();
    c.restore();
    SHAPES._twinDagger(c, L, W, p);
    c.save();
    c.globalCompositeOperation = "destination-out";
    for (let i = 0; i < 3; i++){
      c.beginPath();
      c.arc(L*(0.50 + 0.13*i), 0, bh*(0.44 - 0.07*i), 0, TAU);
      c.fill();
    }
    c.restore();
  },

  /* DWARVEN. Bolted, and the point is a CHISEL -- the same tell as the dwarven
     greatsword, which is what makes the two read as one workshop. */
  _tbBuilt(c, L, W, p){
    const bh = W * 0.17;
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);
    SHAPES._twinDagger(c, L, W, p);
    c.fillStyle = iron; c.strokeStyle = dark;
    c.lineWidth = Math.max(1, W*0.030);
    c.beginPath();                                             // the chisel
    c.moveTo(L*0.86, -bh*0.62); c.lineTo(L*1.02, -bh*0.52);
    c.lineTo(L*1.02,  bh*0.52); c.lineTo(L*0.86,  bh*0.62);
    c.closePath(); c.fill(); c.stroke();
    c.fillRect(L*0.36, -bh*1.28, L*0.055, bh*2.56);            // a collar
    c.strokeRect(L*0.36, -bh*1.28, L*0.055, bh*2.56);
    c.fillStyle = dark;
    for (const rx of [0.50, 0.64, 0.78]){
      c.beginPath(); c.arc(L*rx, 0, W*0.048, 0, TAU); c.fill();
    }
  },

  /* BLOODSWORN. The dagger already has ONE notch at the base of the blade --
     the shape's own comment calls it "the one piece of real structure". This
     school gets three more, running back down the spine, so the notch stops
     being a detail and becomes the weapon's argument. */
  _tbBarbed(c, L, W, p){
    const bh = W * 0.17;
    SHAPES._twinDagger(c, L, W, p);
    c.lineJoin = "miter";
    c.fillStyle = SHAPES._shade(p.steel, 0.74, 0.32);
    c.strokeStyle = SHAPES._shade(p.steel, 0.20, 0.52);
    c.lineWidth = Math.max(1, W*0.030);
    for (let i = 0; i < 3; i++){
      const x = L * (0.52 + 0.13 * i);
      c.beginPath();
      c.moveTo(x,           bh*0.86);
      c.lineTo(x - L*0.085, bh*2.05);
      c.lineTo(x + L*0.035, bh*1.05);
      c.closePath(); c.fill(); c.stroke();
    }
    for (const sg of [-1, 1]){                                 // guard, hooked
      c.beginPath();
      c.moveTo(L*0.285, sg * W*0.30);
      c.quadraticCurveTo(L*0.20, sg * W*0.86, L*0.335, sg * W*0.80);
      c.quadraticCurveTo(L*0.325, sg * W*0.48, L*0.355, sg * W*0.26);
      c.closePath(); c.fill(); c.stroke();
    }
  },

  /* VERDANT. A thorn on a stem -- the smallest and most literal reading of the
     grammar in the game, and the right one: at this size a leaf with veins
     would be mush, and a thorn is exactly a short curved point. */
  _tbGrown(c, L, W, p){
    const bh = W * 0.17;
    const wood = SHAPES._shade(p.dark, 1.28, 0.22);
    c.lineCap = "round"; c.lineJoin = "round";
    c.strokeStyle = wood; c.lineWidth = W*0.20;                // the stem
    c.beginPath(); c.moveTo(-L*0.02, W*0.03); c.lineTo(L*0.34, 0); c.stroke();
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.055);
    for (const sg of [-1, 1]){                                 // two shoots
      c.beginPath();
      c.moveTo(L*0.30, sg * W*0.06);
      c.quadraticCurveTo(L*0.20, sg * W*0.62, L*0.42, sg * W*0.56);
      c.stroke();
    }
    c.beginPath();                                             // the thorn
    c.moveTo(L*0.34, -bh*0.90);
    c.quadraticCurveTo(L*0.74, -bh*1.05, L*1.02, -bh*0.05);
    c.quadraticCurveTo(L*0.72,  bh*0.60, L*0.34,  bh*0.95);
    c.closePath();
    const g = c.createLinearGradient(0, -bh, 0, bh);
    g.addColorStop(0, p.glow); g.addColorStop(0.5, p.steel);
    g.addColorStop(1, SHAPES._shade(p.steel, 0.46, 0.38));
    c.fillStyle = g; c.fill();
    c.strokeStyle = SHAPES._shade(p.dark, 1.1, 0.12);
    c.lineWidth = Math.max(1, W*0.038);
    c.beginPath(); c.moveTo(L*0.36, 0); c.lineTo(L*0.98, -bh*0.10); c.stroke();
  },

  /* UMBRAL. The point is gone, as on the greatsword -- and on a weapon whose
     entire job is to be the fastest thing on the floor, a blunt one is the
     most upsetting version available. */
  _tbEaten(c, L, W, p){
    const bh = W * 0.17;
    c.save();
    SHAPES._twinDagger(c, L, W, p);
    c.globalCompositeOperation = "destination-out";
    c.beginPath();
    c.moveTo(L*0.74, -bh*2.2);
    c.lineTo(L*0.82, -bh*0.55); c.lineTo(L*0.76, bh*0.10);
    c.lineTo(L*0.84,  bh*2.2);  c.lineTo(L*1.40, bh*2.2);
    c.lineTo(L*1.40, -bh*2.2);
    c.closePath(); c.fill();
    for (const [bx, by, r, s] of [[0.50, -0.95, 0.62, 0.4],
                                  [0.63,  1.00, 0.50, 2.1]]){
      c.beginPath();
      for (let i = 0; i < 10; i++){
        const a = i * TAU / 10;
        const rr = bh * r * (0.58 + 0.50 * Math.abs(Math.sin(i * 1.9 + s)));
        const px = L*bx + Math.cos(a) * rr, py = bh*by + Math.sin(a) * rr;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.closePath(); c.fill();
    }
    c.restore();
    c.save();
    c.globalAlpha = 0.5; c.fillStyle = p.core;
    c.beginPath();
    c.moveTo(L*0.80, -bh*0.30);
    c.quadraticCurveTo(L*1.04, -bh*1.20, L*1.14, -bh*0.05);
    c.quadraticCurveTo(L*0.96, -bh*0.40, L*0.82, bh*0.24);
    c.closePath(); c.fill();
    c.globalAlpha = 1;
    c.restore();
  },

  /* VIGIL. Three lames -- not five. The blade is 62 units long and drawn
     twice; five plates at this scale is a texture, and this build has learned
     that a viewer counts objects and cannot read a texture. */
  _tbPlated(c, L, W, p){
    const bh = W * 0.17;
    SHAPES._twinDagger(c, L, W, p);
    c.fillStyle = p.dark;                                      // guard shield
    c.beginPath();
    c.moveTo(L*0.275, -W*0.52); c.lineTo(L*0.375, -W*0.40);
    c.lineTo(L*0.375,  W*0.40); c.lineTo(L*0.275,  W*0.52);
    c.closePath(); c.fill();
    c.fillStyle = p.core; c.fillRect(L*0.295, -W*0.32, L*0.062, W*0.64);
    c.fillStyle = p.glow; c.fillRect(L*0.295, -W*0.32, L*0.062, W*0.18);
    for (let i = 0; i < 3; i++){
      const x = L * (0.41 + 0.155 * i);
      const h = bh * (1.24 - 0.18 * i);
      c.fillStyle = p.dark;  c.fillRect(x, -h, L*0.135, h*2);
      c.fillStyle = p.core;  c.fillRect(x + L*0.014, -h*0.82, L*0.107, h*1.64);
      c.fillStyle = p.glow;  c.fillRect(x + L*0.014, -h*0.82, L*0.107, h*0.28);
      c.fillStyle = p.dark;
      c.beginPath(); c.arc(x + L*0.068, 0, W*0.042, 0, TAU); c.fill();
    }
  },
'''

# --------------------------------------------------------------------- bow --
# The bow's branch is an else-if chain INSIDE the shared routine, between the
# limbs and the string. Appending to it keeps the limb curve, the string, the
# riser and the bolt in every school, which is what makes a 54-unit shape still
# read as a bow.

BOW_ANCHOR = '''    } else if (p.key === "dwarven"){'''

BOW_BODY = r'''    } else if (p.key === "sanctified"){
      /* SANCTIFIED: the bow is a MONSTRANCE. A ring stands in the mouth of the
         recurve with rays out of it, so the thing the arrow leaves through is
         a halo. Pierced limbs, because the light has to get out. */
      c.save();
      c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.055);
      c.beginPath(); c.arc(rx + L*0.14, 0, lh*0.52, 0, TAU); c.stroke();
      c.lineWidth = Math.max(1, W*0.035);
      for (let i = 0; i < 6; i++){
        const a = i * TAU / 6 + 0.3;
        c.beginPath();
        c.moveTo(rx + L*0.14 + Math.cos(a)*lh*0.52, Math.sin(a)*lh*0.52);
        c.lineTo(rx + L*0.14 + Math.cos(a)*lh*0.80, Math.sin(a)*lh*0.80);
        c.stroke();
      }
      c.restore();
      c.save();
      c.globalCompositeOperation = "destination-out";
      for (const sg of [-1, 1]) for (let i = 0; i < 3; i++){
        const q = onLimb(sg, 0.24 + i * 0.26);
        c.beginPath(); c.arc(q.x, q.y, W*0.052, 0, TAU); c.fill();
      }
      c.restore();

    } else if (p.key === "bloodsworn"){
      /* BLOODSWORN: barbs on the OUTSIDE of both limbs, pointing back along the
         draw, and a hook off each tip. A bow that catches is a strange object
         and that is the point -- this school's weapons are built to keep what
         they touch, even the one that never touches anything. */
      c.fillStyle = SHAPES._shade(p.steel, 0.74, 0.32);
      c.strokeStyle = "#0D0907"; c.lineWidth = Math.max(1, W*0.022);
      for (const sg of [-1, 1]){
        for (let i = 0; i < 3; i++){
          const q = onLimb(sg, 0.22 + i * 0.28);
          c.save();
          c.translate(q.x, q.y); c.rotate(q.a);
          c.beginPath();
          c.moveTo(0, sg * W*0.05);
          c.lineTo(-W*0.30, sg * W*0.44);
          c.lineTo(W*0.10,  sg * W*0.14);
          c.closePath(); c.fill(); c.stroke();
          c.restore();
        }
        const t2 = onLimb(sg, 0.02);                 // and a tip hook
        c.beginPath();
        c.moveTo(t2.x, t2.y);
        c.lineTo(t2.x - W*0.16, t2.y + sg * W*0.46);
        c.lineTo(t2.x + W*0.20, t2.y + sg * W*0.12);
        c.closePath(); c.fill(); c.stroke();
      }

    } else if (p.key === "verdant"){
      /* VERDANT: the limbs are a living branch that has been bent and left
         bent, so it leafs along its length and the string is a vine. This is
         the only school for which "a bow" is not a stretch -- a bow IS a bent
         piece of wood, and every other school has to explain why theirs is
         not one. */
      c.lineCap = "round";
      for (const sg of [-1, 1]){
        for (let i = 0; i < 3; i++){
          const q = onLimb(sg, 0.20 + i * 0.28);
          c.save();
          c.translate(q.x, q.y);
          c.rotate(q.a + sg * 0.95);
          c.fillStyle = p.core;
          c.beginPath();
          c.moveTo(0, 0);
          c.quadraticCurveTo(W*0.20, -W*0.16, W*0.44, 0);
          c.quadraticCurveTo(W*0.20,  W*0.16, 0, 0);
          c.closePath(); c.fill();
          c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.020);
          c.beginPath(); c.moveTo(0,0); c.lineTo(W*0.42, 0); c.stroke();
          c.restore();
        }
      }
      c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.030);
      for (const sg of [-1, 1]){                    // a tendril off each tip
        const q = onLimb(sg, 0.02);
        c.beginPath();
        c.moveTo(q.x, q.y);
        c.quadraticCurveTo(q.x - W*0.36, q.y + sg*W*0.30,
                           q.x - W*0.10, q.y + sg*W*0.52);
        c.stroke();
      }

    } else if (p.key === "umbral"){
      /* UMBRAL: both limb TIPS are eaten off, which on a bow is the one place
         where absence is also a mechanical claim -- the tips are what the
         string is anchored to. It should not be able to fire, and it does. */
      c.save();
      c.globalCompositeOperation = "destination-out";
      for (const sg of [-1, 1]){
        const q = onLimb(sg, 0.10);
        c.beginPath();
        for (let i = 0; i < 10; i++){
          const a = i * TAU / 10;
          const rr = W * 0.30 * (0.58 + 0.50 * Math.abs(Math.sin(i * 1.9 + sg)));
          const px = q.x + Math.cos(a) * rr, py = q.y + Math.sin(a) * rr;
          if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
        }
        c.closePath(); c.fill();
      }
      const mid = onLimb(1, 0.55);                  // and a gap in one limb
      c.beginPath(); c.arc(mid.x, mid.y, W*0.19, 0, TAU); c.fill();
      c.restore();
      c.save();
      c.globalAlpha = 0.5; c.fillStyle = p.core;
      for (const sg of [-1, 1]){
        const q = onLimb(sg, 0.10);
        c.beginPath();
        c.moveTo(q.x, q.y);
        c.quadraticCurveTo(q.x - W*0.60, q.y + sg*W*0.50,
                           q.x - W*0.20, q.y + sg*W*0.70);
        c.quadraticCurveTo(q.x - W*0.20, q.y + sg*W*0.28, q.x, q.y);
        c.closePath(); c.fill();
      }
      c.globalAlpha = 1;
      c.restore();

    } else if (p.key === "runic"){
      /* RUNIC: the limbs are in pieces and the STRING is what holds them in
         formation -- which is the grammar's best joke and its most honest
         reading on this type. Everywhere else runic deletes the part that does
         the holding; here it cannot, because the string is the only thing left
         that could. Five segments a limb, cut out of the limb that is already
         drawn, so the recurve still reads. */
      c.save();
      c.globalCompositeOperation = "destination-out";
      for (const sg of [-1, 1]){
        for (let i = 0; i < 4; i++){
          const q = onLimb(sg, 0.16 + i * 0.21);
          c.save();
          c.translate(q.x, q.y); c.rotate(q.a);
          c.fillRect(-W*0.055, -W*0.34, W*0.11, W*0.68);
          c.restore();
        }
      }
      c.restore();
      c.save();                                     // the sigil, at the grip
      c.globalCompositeOperation = "lighter";
      c.translate(rx + L*0.13, 0);
      c.rotate(-(SHAPES._t || 0) * 2.4);
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.028);
      c.shadowColor = p.core; c.shadowBlur = 12;
      const rr2 = W * 0.24;
      c.beginPath(); c.arc(0, 0, rr2, 0, TAU); c.stroke();
      c.beginPath();
      for (let i = 0; i < 3; i++){
        const a = i * TAU / 3;
        const x = Math.cos(a) * rr2 * 0.60, y = Math.sin(a) * rr2 * 0.60;
        if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
      }
      c.closePath(); c.stroke();
      c.restore();

    } else if (p.key === "dwarven"){'''
