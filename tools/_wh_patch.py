#!/usr/bin/env python3
"""Generates the warhammer school-grammar patch for silhouette_build.py.

Kept as its own file because the replacement is ~200 lines of canvas code and
inlining it into the builder's anchor table would make that table unreadable.
The builder imports WARHAMMER_ANCHOR / WARHAMMER_BODY from here.
"""

WARHAMMER_ANCHOR = '''  warhammer(c, L, W, p){
    const hh = W * 0.50;                                       // head half-height'''

WARHAMMER_BODY = r'''  /* ============================================================ WARHAMMER ==
     THE SCHOOL GRAMMARS, ON THE WORST ROW ON THE SHEET.

     `silhouette_probe.py` scored the shipped warhammer at **IoU 1.000 across
     all seven schools** -- pixel-identical outlines, seven relics, one weapon.
     It is the flattest row in the game and therefore the honest place to build
     the system rather than the flattering one.

     Rick, on what the system has to be:

       > *"i like having an overaching theme between schools that tie weapon
       >  models together. but they need to be distinct and unique in more ways
       >  than 'ones a sword and ones a dagger'"*
       > *"both really. they should share some characteristics but also bring
       >  their own unique flair"*

     So it is three layers, and they are the same three layers as the ultimate:

       TYPE    the form, the proportions, the hitbox. `_whBase` -- one hammer.
       SCHOOL  a GRAMMAR: a structural rule that deforms any type it is applied
               to. Learn "runic things are in pieces" once and it pays off on
               all eight types.
       CELL    the flair. What that grammar does SPECIFICALLY to a hammer, which
               is not what it does to a bow.

     Every grammar below except runic's calls `_whBase` first and then adds or
     removes -- literally sharing characteristics before bringing its own. Runic
     is the exception on purpose: its whole thesis is that nothing was made, so
     it must refuse the made object rather than decorate it. */
  warhammer(c, L, W, p, k, aff){
    const key = p.key || aff;
    if (key === "runic")      return SHAPES._whConjured(c, L, W, p);
    if (key === "verdant")    return SHAPES._whGrown(c, L, W, p);
    if (key === "bloodsworn") return SHAPES._whBarbed(c, L, W, p);
    if (key === "umbral")     return SHAPES._whEaten(c, L, W, p);
    if (key === "sanctified") return SHAPES._whRadiant(c, L, W, p);
    if (key === "dwarven")    return SHAPES._whBuilt(c, L, W, p);
    if (key === "vigil")      return SHAPES._whPlated(c, L, W, p);
    return SHAPES._whBase(c, L, W, p);
  },

  /* The type: the hammer every grammar starts from. Nothing wears it
     unmodified -- an outline shared by three schools was the whole complaint. */
  _whBase(c, L, W, p){
    const hh = W * 0.50;                                       // head half-height'''

# everything after the anchor in the original function is reused verbatim; the
# builder splices it in, then appends the four grammars below.

WARHAMMER_GRAMMARS = r'''
  /* -------------------------------------------------------------- RUNIC --
     IN PIECES, HELD BY NOTHING. The grammar's second type. There is no haft at
     all and no head -- three blocks hang in a head-shaped cluster with real
     daylight between them, light bleeds down the axis where a shaft would be,
     and the sigil turns backwards where a hand would be.

     THE CELL'S FLAIR: a hammer's whole argument is that its mass is out at the
     end, so the chunks get BIGGER toward the striking face instead of tapering
     like a blade. The twinblade's shards narrow to a point; these grow into
     one. Same grammar, opposite gesture, because the type is different. */
  _whConjured(c, L, W, p){
    const hh = W * 0.50, gap = L * 0.34;
    const prof = (cc) => {
      cc.beginPath();
      cc.moveTo(L*0.56, -hh*0.42);
      cc.lineTo(L*0.93, -hh);
      cc.lineTo(L,      -hh*0.66);
      cc.lineTo(L,       hh*0.66);
      cc.lineTo(L*0.93,  hh);
      cc.lineTo(L*0.56,  hh*0.42);
      cc.closePath();
    };
    SHAPES._conjure(c, L, W, p, { n:3, gap, bw:hh, prof, frac:0.76,
                                  sliceFrom:L*0.56, sliceTo:L*1.0,
                                  beam:0.040, drift:0.050, cant:0.045,
                                  sigil:0.26 });
  },

  /* ------------------------------------------------------------ VERDANT --
     GROWN, NOT MADE. Nothing here was struck on an anvil: the haft is a living
     branch that forks, and the head is a burl -- the swollen knot a tree makes
     around an injury, which is the only naturally occurring object shaped like
     a hammer head and is genuinely what verdant would swing.

     THE CELL'S FLAIR: three thorns out of the striking face. On a scythe this
     grammar would be a curl of new growth along the inside of the crescent; on
     a hammer it is the part that hits, so the growth is armed. */
  _whGrown(c, L, W, p){
    const hh = W * 0.50;
    const wood = SHAPES._shade(p.dark, 1.30, 0.22);
    c.lineCap = "round"; c.lineJoin = "round";

    c.strokeStyle = wood; c.lineWidth = W*0.15;                // the branch
    c.beginPath();
    c.moveTo(0, W*0.04);
    c.quadraticCurveTo(L*0.34, -W*0.13, L*0.62, W*0.02);
    c.stroke();
    c.lineWidth = W*0.075;                                     // the fork
    c.beginPath();
    c.moveTo(L*0.40, -W*0.055);
    c.quadraticCurveTo(L*0.56, -W*0.30, L*0.70, -hh*0.52);
    c.stroke();
    c.beginPath();
    c.moveTo(L*0.44, W*0.05);
    c.quadraticCurveTo(L*0.60, W*0.30, L*0.72, hh*0.50);
    c.stroke();

    for (const [tx, ty, r] of [[0.22,-1,1], [0.33,1,-1]]){      // leaves, out
      c.save();
      c.translate(L*tx, ty * W*0.10);
      c.rotate(ty * 0.85);
      c.fillStyle = p.core;
      c.beginPath();
      c.moveTo(0, 0);
      c.quadraticCurveTo(L*0.10, -W*0.14*r, L*0.22, 0);
      c.quadraticCurveTo(L*0.10,  W*0.14*r, 0, 0);
      c.closePath(); c.fill();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.022);
      c.beginPath(); c.moveTo(0,0); c.lineTo(L*0.21, 0); c.stroke();
      c.restore();
    }

    c.beginPath();                                              // the burl
    c.moveTo(L*0.62, -hh*0.30);
    c.bezierCurveTo(L*0.68, -hh*1.16, L*0.96, -hh*1.02, L*1.00, -hh*0.34);
    c.bezierCurveTo(L*1.04,  hh*0.28, L*0.92,  hh*1.12, L*0.74,  hh*0.94);
    c.bezierCurveTo(L*0.64,  hh*0.84, L*0.60,  hh*0.30, L*0.62, -hh*0.30);
    c.closePath();
    const g = c.createLinearGradient(0, -hh, 0, hh);
    g.addColorStop(0, p.steel);
    g.addColorStop(0.5, SHAPES._shade(p.steel, 0.60, 0.45));
    g.addColorStop(1,   SHAPES._shade(p.steel, 0.32, 0.45));
    c.fillStyle = g; c.fill();
    c.strokeStyle = SHAPES._shade(p.dark, 1.0, 0.10);
    c.lineWidth = Math.max(1, W*0.05); c.stroke();

    c.strokeStyle = p.core + "99";                              // grain rings
    c.lineWidth = Math.max(1, W*0.030);
    for (const rr of [0.30, 0.52]){
      c.beginPath(); c.ellipse(L*0.82, 0, hh*rr*0.72, hh*rr, 0, 0, TAU); c.stroke();
    }

    c.fillStyle = p.glow;                                       // three thorns
    for (const ty of [-0.58, 0, 0.58]){
      c.beginPath();
      c.moveTo(L*0.98, hh*ty - hh*0.13);
      c.lineTo(L*1.16, hh*ty * 1.22);
      c.lineTo(L*0.98, hh*ty + hh*0.13);
      c.closePath(); c.fill();
    }
  },

  /* --------------------------------------------------------- BLOODSWORN --
     BARBED, AND EVERY BARB POINTS BACKWARD. The grammar is that the weapon is
     built to keep what it catches: the outline is serrated against the
     direction of travel, so it reads as a thing that goes in easily and does
     not come out. Same argument as hemorrhage, in the silhouette.

     THE CELL'S FLAIR: a hammer cannot cut, so its barbs are on the RETURN --
     a long rearward spur off the back of the head that arrives after the face
     does. It shares `_whBase` entirely; everything here is added. */
  _whBarbed(c, L, W, p){
    const hh = W * 0.50;
    SHAPES._whBase(c, L, W, p);
    c.lineJoin = "miter";
    c.fillStyle = SHAPES._shade(p.steel, 0.72, 0.35);
    c.strokeStyle = SHAPES._shade(p.steel, 0.20, 0.55);
    c.lineWidth = Math.max(1, W*0.035);

    for (const sg of [-1, 1]){                                  // hooks, top+bottom
      for (const hx of [0.70, 0.82, 0.94]){
        c.beginPath();
        c.moveTo(L*hx,          sg * hh*0.98);
        c.lineTo(L*(hx-0.09),   sg * hh*1.62);
        c.lineTo(L*(hx+0.035),  sg * hh*1.06);
        c.closePath(); c.fill(); c.stroke();
      }
    }
    c.beginPath();                                              // the return spur
    c.moveTo(L*0.66, -hh*0.34);
    c.lineTo(L*0.40, -hh*1.02);
    c.lineTo(L*0.52, -hh*0.10);
    c.lineTo(L*0.66,  hh*0.20);
    c.closePath(); c.fill(); c.stroke();

    c.fillStyle = p.core;                                       // and it is fed
    c.beginPath();
    c.moveTo(L*0.455, -hh*0.86); c.lineTo(L*0.425, -hh*0.98);
    c.lineTo(L*0.50,  -hh*0.62);
    c.closePath(); c.fill();
  },

  /* ------------------------------------------------------------- UMBRAL --
     EATEN. The grammar is ABSENCE: an umbral weapon is not decorated, it is
     incomplete, and the missing parts are the point. Curse is the only status
     in the game that never expires, and this is that -- damage already done,
     permanently.

     Implemented with `destination-out`, so the bites are real holes in the
     silhouette rather than dark paint on it. That distinction is the entire
     difference between this and a maker's mark: `silhouette_probe.py` scores
     the marks at 0.917-1.000 because paint does not move an outline.

     THE CELL'S FLAIR: the HAFT is bitten through as well, so the head is only
     tenuously attached -- which on the heaviest weapon in the game is the most
     alarming place to put a gap. On a bow the same grammar would eat the limb
     tips; on a hammer it eats the thing holding five kilos of iron. */
  _whEaten(c, L, W, p){
    const hh = W * 0.50;
    c.save();
    SHAPES._whBase(c, L, W, p);
    c.globalCompositeOperation = "destination-out";
    /* THE PATH IS SHARED so the hole and the rim cannot drift apart. The rim
       is why this is needed at all: `drawWeapon` sets a shadowBlur before it
       calls the shape, so `destination-out` removes the GLOW as well as the
       metal and leaves a hard-edged black void -- invisible on a white-on-black
       silhouette sheet, and obviously broken the moment the matrix was pulled
       in colour. An eaten thing has a lit edge where the material stops. */
    const bitePath = (cx, cy, r, seed) => {
      c.beginPath();
      for (let i = 0; i < 10; i++){
        const a = i * TAU / 10;
        const rr = r * (0.62 + 0.46 * Math.abs(Math.sin(i * 1.9 + seed)));
        const px = cx + Math.cos(a) * rr, py = cy + Math.sin(a) * rr;
        if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.closePath();
    };
    const bite = (cx, cy, r, seed) => { bitePath(cx, cy, r, seed); c.fill(); };
    const BITES = [[L*0.72, -hh*0.86, hh*0.62, 0.4],            // out of the head
                   [L*0.99,  hh*0.52, hh*0.50, 2.1],            // out of the face
                   [L*0.342, 0,       W*0.155, 3.4]];           // through the haft
    for (const b of BITES) bite(b[0], b[1], b[2], b[3]);
    c.restore();

    c.save();                                                   // the lit edges
    /* THE RIM CARRIES A SHADOW. `destination-out` removes the glow along
       with the metal, and the glow is 90%+ of the lit picture, so an
       un-lit rim still reads as a hard black hole. Giving the rim its own
       shadowBlur puts light back around the absence. */
    c.shadowColor = p.core; c.shadowBlur = 12;
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.045);
    for (const b of BITES){ bitePath(b[0], b[1], b[2], b[3]); c.stroke(); }
    c.restore();

    /* what is left behind: the void does not read as a hole unless something
       is leaking out of it. Two wisps, drawn AFTER the restore so they are not
       themselves eaten. */
    c.save();
    c.globalAlpha = 0.55;
    c.fillStyle = p.core;
    for (const [bx, by, s] of [[0.72, -0.86, 1], [0.99, 0.52, -1]]){
      c.beginPath();
      c.moveTo(L*bx, hh*by);
      c.quadraticCurveTo(L*(bx-0.16), hh*(by + s*0.9),
                         L*(bx-0.30), hh*(by + s*0.4));
      c.quadraticCurveTo(L*(bx-0.14), hh*(by + s*0.2), L*bx, hh*by);
      c.closePath(); c.fill();
    }
    c.globalAlpha = 1;
    c.restore();
  },

  /* --------------------------------------------------------- SANCTIFIED --
     RADIANT, AND PIERCED. The grammar: a sanctified weapon is not solid, it is
     a lantern -- light is meant to come THROUGH it, so the metal is cut away in
     a rosette and a halo stands off behind the working end. Both change the
     outline; the halo especially, because it is the only round thing on a
     rectilinear weapon.

     THE CELL'S FLAIR: the halo sits BEHIND the head rather than around it, so
     the hammer reads as a thing being swung out of the light. Four spurs off
     the ring, at the diagonals, so it cannot be mistaken for a wheel. */
  _whRadiant(c, L, W, p){
    const hh = W * 0.50;
    c.save();
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.055);  // the halo
    c.beginPath(); c.arc(L*0.70, 0, hh*1.34, 0, TAU); c.stroke();
    c.lineWidth = Math.max(1, W*0.040);
    for (let i = 0; i < 4; i++){
      const a = Math.PI/4 + i * Math.PI/2;
      c.beginPath();
      c.moveTo(L*0.70 + Math.cos(a)*hh*1.34, Math.sin(a)*hh*1.34);
      c.lineTo(L*0.70 + Math.cos(a)*hh*1.86, Math.sin(a)*hh*1.86);
      c.stroke();
    }
    c.restore();

    SHAPES._whBase(c, L, W, p);

    c.save();                                                    // and pierced
    c.globalCompositeOperation = "destination-out";
    for (const [px, py, r] of [[0.755, 0, 0.30], [0.755, -0.62, 0.19],
                               [0.755, 0.62, 0.19], [0.875, -0.36, 0.15],
                               [0.875, 0.36, 0.15]]){
      c.beginPath(); c.arc(L*px, hh*py, hh*r, 0, TAU); c.fill();
    }
    c.restore();
  },

  /* ------------------------------------------------------------ DWARVEN --
     BUILT, NOT FORGED. The grammar is visible assembly: a dwarven weapon is
     several parts BOLTED TOGETHER, and the fasteners stand proud of the
     surface so you can see it was made by someone. The bow already does this
     with its riveted riser -- this is the same idea on a hammer, and the point
     of putting it here is that the two should look like the same workshop.

     THE CELL'S FLAIR: a hammer is the one weapon where the join has to carry
     the whole load, so the head is strapped to the haft with two long langets
     running back down the shaft, and the bolt bosses project out past the
     head's own edge. The assembly is doing visible work. */
  _whBuilt(c, L, W, p){
    const hh = W * 0.50;
    SHAPES._whBase(c, L, W, p);
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);

    c.fillStyle = iron; c.strokeStyle = dark;
    c.lineWidth = Math.max(1, W*0.030);
    for (const sg of [-1, 1]){                                   // langets
      c.beginPath();
      c.moveTo(L*0.66, sg * W*0.075);
      c.lineTo(L*0.66, sg * W*0.235);
      c.lineTo(L*0.34, sg * W*0.150);
      c.lineTo(L*0.34, sg * W*0.075);
      c.closePath(); c.fill(); c.stroke();
    }
    for (const sg of [-1, 1]){                                   // bolt bosses
      for (const bx of [0.70, 0.90]){
        c.beginPath();
        c.arc(L*bx, sg * hh*1.14, W*0.105, 0, TAU);
        c.fillStyle = iron; c.fill(); c.stroke();
        c.beginPath();
        c.arc(L*bx, sg * hh*1.14, W*0.042, 0, TAU);
        c.fillStyle = dark; c.fill();
      }
    }
    c.fillStyle = iron; c.strokeStyle = dark;                    // a wedge, driven
    c.beginPath();
    c.moveTo(L*0.60, -W*0.30); c.lineTo(L*0.665, -W*0.075);
    c.lineTo(L*0.665, W*0.075); c.lineTo(L*0.60, W*0.30);
    c.closePath(); c.fill(); c.stroke();
  },

  /* -------------------------------------------------------------- VIGIL --
     PLATED. The grammar already exists on the bow -- discrete, countable
     armour segments with a hard value break under each -- and it is the same
     material the ward puts on the shell, so the weapon and the status are
     visibly the same substance. Countable is the whole point: five plates read
     as five things, a smooth casing reads as nothing.

     THE CELL'S FLAIR: on a bow the plates lie along the limbs. On a hammer
     they stack UP the head like a pauldron, each one stepping proud of the one
     beneath, so the striking face is the last and largest plate. The thing
     that shields is also the thing that hits. */
  _whPlated(c, L, W, p){
    const hh = W * 0.50;
    SHAPES._whBase(c, L, W, p);
    c.lineJoin = "round";
    for (let i = 0; i < 4; i++){                                 // stacked plates
      const u = i / 4;
      const x = L * (0.62 + 0.10 * i);
      const h = hh * (0.92 + 0.30 * u);
      c.fillStyle = p.dark;
      c.fillRect(x, -h, L*0.115, h*2);
      c.fillStyle = p.core;
      c.fillRect(x + L*0.012, -h*0.86, L*0.091, h*1.72);
      c.fillStyle = p.glow;
      c.fillRect(x + L*0.012, -h*0.86, L*0.091, h*0.24);
    }
    c.fillStyle = p.dark;                                        // plate studs
    for (let i = 0; i < 4; i++){
      const x = L * (0.62 + 0.10 * i) + L*0.057;
      c.beginPath(); c.arc(x, 0, W*0.038, 0, TAU); c.fill();
    }
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, W*0.045);   // haft banding
    for (const gx of [0.22, 0.34, 0.46]){
      c.beginPath();
      c.moveTo(L*gx, -W*0.145); c.lineTo(L*gx, W*0.145); c.stroke();
    }
  },
'''
