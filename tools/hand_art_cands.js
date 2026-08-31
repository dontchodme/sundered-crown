/* ==========================================================================
   ROUND TWO. Rick, on candidate B in the build:

     "the hands are a bit large. they look a little comical. and the forearms
      look like they are just bone. thats got me thinking. what if the whole
      hand was bone?"

   BOTH NOTES ARE THE SAME DISCOVERY. The forearm was drawn as three glowing
   strands with dark gaps between them, and at this size that is exactly what
   a radius and an ulna look like. The art was already halfway to a skeleton
   and nobody had noticed, including whoever drew it.

   ## THE SIZE, MEASURED RATHER THAN EYEBALLED

   Candidate B's whole object -- arm plus hand -- spans about 100px on a 540
   frame and 200px on a 1080 phone frame, which is a fifth of the frame width
   for a thing there are three of at once. "A bit large" is right and the
   number says how much: the candidates below run at 0.68x and 0.80x, so the
   object lands at 68-80px on a 540 frame instead of 100.

   ## WHY BONE IS DRAWN THE OPPOSITE WAY ROUND FROM FLESH

   The flame hand is EDGE-LIT -- bright contour, dim interior -- because a
   flame is a volume. A skeleton is the inverse: bright PARTS with dark GAPS
   between them, and the gaps are the entire reading. Nothing else in this
   game is made of separated pieces, so a hand made of them survives a
   thumbnail that a solid silhouette does not.

   So bone is drawn:
     1  a dark stroke per bone, over-wide -- this is what makes the GAP
     2  a bright fill per bone at true width
   which is pass-for-pass the inverse of the flame body's two passes, and for
   the opposite reason.

   ## THE FOUR

     A  BONE HAND            full skeleton at 0.80x: radius and ulna, carpals,
                             four metacarpals, three phalanges a finger with
                             joint beads, an opposed thumb of two.
     B  BONE HAND, SMALLER   the same at 0.68x, for whether "comical" was the
                             size rather than the shape.
     C  BONE AND GHOST       the skeleton with a faint flesh-glow silhouette
                             around it -- "ethereal purple hand" with the bone
                             inside it rather than instead of it.
     D  FLAME HAND, SMALLER  what he picked last round, at 0.80x. The control:
                             if this reads fine small, the note was size only
                             and bone is a separate decision.
   ========================================================================== */
window.HAND = {};

/* ---- shared: capsules, and the two ways of painting them ---------------- */
function strokeCaps(c, parts, extra){
  for (const q of parts){
    c.lineWidth = Math.max(0.4, q.w + extra);
    c.beginPath();
    c.moveTo(q.x1, q.y1);
    c.lineTo(q.x2, q.y2);
    c.stroke();
  }
}

/* BONE: dark first (the gap), bright second (the bone) */
function paintBones(c, parts, R, pal, bold){
  c.save();
  c.lineCap = 'round';
  c.globalCompositeOperation = 'lighter';
  c.globalAlpha = 0.16;
  c.strokeStyle = pal.core;
  strokeCaps(c, parts, R * 0.55 * bold);
  c.restore();
  c.save();
  c.lineCap = 'round';
  c.globalCompositeOperation = 'source-over';
  c.globalAlpha = 1;
  c.strokeStyle = pal.dark;
  strokeCaps(c, parts, R * 0.075 * bold);
  c.globalAlpha = 0.96;
  c.strokeStyle = pal.glow;
  strokeCaps(c, parts, 0);
  c.restore();
}

/* ---- the skeleton, as a parts list -------------------------------------- */
function boneParts(R, shut){
  const p = [], s = shut;
  /* THE FOREARM IS TWO BONES. This is the thing Rick saw. */
  p.push({ x1: -3.00 * R, y1: -0.20 * R, x2: -0.90 * R, y2: -0.22 * R,
           w: 0.20 * R });
  p.push({ x1: -3.00 * R, y1:  0.22 * R, x2: -0.90 * R, y2:  0.18 * R,
           w: 0.17 * R });
  /* the carpals -- two short beads, so the wrist is a joint and not a weld */
  p.push({ x1: -0.78 * R, y1: -0.12 * R, x2: -0.66 * R, y2: -0.12 * R,
           w: 0.22 * R });
  p.push({ x1: -0.78 * R, y1:  0.12 * R, x2: -0.66 * R, y2:  0.12 * R,
           w: 0.22 * R });
  /* the metacarpals -- four bones fanning across the back of the hand */
  for (let k = 0; k < 4; k++){
    const y = (-0.46 + k * 0.31) * R;
    p.push({ x1: -0.58 * R, y1: y * 0.42, x2: 0.24 * R, y2: y,
             w: 0.135 * R });
  }
  /* the phalanges -- three a finger, WITH GAPS, curling on the clench */
  for (let k = 0; k < 4; k++){
    const y = (-0.46 + k * 0.31) * R;
    const taper = (k === 3 ? 0.80 : 1) * (k === 0 ? 0.90 : 1);
    let x = 0.30 * R, yy = y, a = s * 0.62;
    for (let seg = 0; seg < 3; seg++){
      const L = R * (0.54 - seg * 0.085) * taper * (1 - 0.20 * s);
      const nx = x + Math.cos(a) * L, ny = yy + Math.sin(a) * L * 0.5;
      p.push({ x1: x, y1: yy, x2: nx, y2: ny,
               w: (0.125 - seg * 0.018) * R * taper });
      /* the GAP is the point -- the next bone starts short of this one's end */
      x = nx + Math.cos(a) * R * 0.075;
      yy = ny + Math.sin(a) * R * 0.075;
      a += s * 0.52;
    }
  }
  /* the thumb: a metacarpal and two phalanges, opposed */
  let tx = -0.34 * R, ty = 0.34 * R, ta = 0.72 - s * 0.30;
  for (let seg = 0; seg < 3; seg++){
    const L = R * (0.40 - seg * 0.07);
    const nx = tx + Math.cos(ta) * L, ny = ty + Math.sin(ta) * L * 0.62;
    p.push({ x1: tx, y1: ty, x2: nx, y2: ny, w: (0.15 - seg * 0.02) * R });
    tx = nx + Math.cos(ta) * R * 0.05;
    ty = ny + Math.sin(ta) * R * 0.05;
    ta -= 0.42 + s * 0.30;
  }
  return p;
}

/* the joint beads, drawn after the bones so they sit on top */
function boneJoints(c, parts, R, pal, bold){
  c.save();
  c.globalCompositeOperation = 'source-over';
  for (let i = 6; i < parts.length; i++){
    const q = parts[i];
    c.fillStyle = pal.dark;
    c.beginPath(); c.arc(q.x2, q.y2, q.w * 0.62 + R * 0.028 * bold, 0,
                         Math.PI * 2); c.fill();
    c.fillStyle = pal.glow;
    c.beginPath(); c.arc(q.x2, q.y2, q.w * 0.48, 0, Math.PI * 2); c.fill();
  }
  c.restore();
}

function embers(c, R, shut, pal, n, spread){
  c.save();
  c.globalCompositeOperation = 'lighter';
  c.fillStyle = pal.glow;
  for (let i = 0; i < n; i++){
    const h1 = ((i * 2654435761) % 1000) / 1000;
    const h2 = ((i * 1597334677) % 1000) / 1000;
    const front = i % 3 === 0;
    const x = front ? R * (0.9 + h1 * 1.4) : -R * (0.6 + h1 * spread);
    const y = (h2 - 0.5) * R * (front ? 2.6 : 1.8);
    c.globalAlpha = (front ? 0.80 * (0.4 + shut * 0.6) : 0.45)
                    * (0.4 + h1 * 0.6);
    c.beginPath();
    c.arc(x, y, R * (0.05 + h2 * 0.05), 0, Math.PI * 2);
    c.fill();
  }
  c.restore();
}

/* ---- the flame hand, kept as the control -------------------------------- */
function flameParts(R, shut){
  const p = [], s = shut;
  p.push({ x1: -0.28 * R, y1: 0, x2: 0.18 * R, y2: 0, w: 1.24 * R });
  for (let k = 0; k < 4; k++){
    const y = (-0.46 + k * 0.305) * R;
    const taper = (k === 3 ? 0.80 : 1) * (k === 0 ? 0.92 : 1);
    const len = R * (1.12 * (1 - s) + 0.46 * s) * taper;
    const x0 = R * (0.36 + 0.16 * s);
    p.push({ x1: x0, y1: y * (1 - 0.06 * s),
             x2: x0 + len, y2: y * (1 - 0.06 * s) + 0.08 * R * s,
             w: R * (0.30 - 0.02 * k) * (1 + 0.30 * s) });
  }
  p.push({ x1: -0.10 * R, y1: 0.42 * R,
           x2: R * (0.66 - 0.10 * s), y2: R * (0.62 - 0.20 * s),
           w: R * (0.40 + 0.06 * s) });
  p.push({ x1: -0.30 * R, y1: 0, x2: -0.86 * R, y2: 0, w: 0.66 * R });
  return p;
}

function flameArm(c, R, pal, n, len, bold){
  c.save();
  c.globalCompositeOperation = 'lighter';
  c.lineCap = 'round';
  for (let i = 0; i < n; i++){
    const off = (i - (n - 1) / 2) / Math.max(1, n - 1);
    c.beginPath();
    c.moveTo(-R * 0.80, off * R * 0.26);
    for (let s = 1; s <= 6; s++){
      const t = s / 6;
      c.lineTo(-R * (0.80 + len * t),
               off * R * 0.26 * (1 - t * 0.3)
               + Math.sin(t * 3.1 + i * 1.7) * R * 0.32 * t);
    }
    c.globalAlpha = 0.22;
    c.strokeStyle = pal.core;
    c.lineWidth = R * 0.44 * bold * (1 - 0.1 * i);
    c.stroke();
    c.globalAlpha = 0.50;
    c.strokeStyle = pal.glow;
    c.lineWidth = R * 0.10 * bold;
    c.stroke();
  }
  c.restore();
}

function flameBody(c, R, shut, pal, bold, core){
  const parts = flameParts(R, shut);
  c.save();
  c.lineCap = 'round'; c.lineJoin = 'round';
  c.save();
  c.globalCompositeOperation = 'lighter';
  c.globalAlpha = 0.20;
  c.strokeStyle = pal.core;
  strokeCaps(c, parts, R * 0.62 * bold);
  c.restore();
  c.globalCompositeOperation = 'source-over';
  c.globalAlpha = 0.95;
  c.strokeStyle = pal.glow;
  strokeCaps(c, parts, R * 0.20 * bold);
  c.globalAlpha = 1;
  c.strokeStyle = pal.dark;
  strokeCaps(c, parts, 0);
  c.save();
  c.globalCompositeOperation = 'lighter';
  if (core > 0 && shut > 0.3){
    const k = (shut - 0.3) / 0.7;
    const g = c.createRadialGradient(R * 0.05, 0, 0, R * 0.05, 0, R * 0.70);
    g.addColorStop(0, '#FFFFFF');
    g.addColorStop(0.35, pal.glow);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    c.globalAlpha = 0.60 * k * core;
    c.fillStyle = g;
    c.beginPath(); c.arc(R * 0.05, 0, R * 0.70, 0, Math.PI * 2); c.fill();
  }
  c.restore();
  c.restore();
}

/* ---------------------------------------------------------------- SHIPPED */
/* candidate B as it stands in the build right now, full size */
window.HAND.SHIPPED = function(c, R, shut, pal){
  const S = R * 1.15;
  flameArm(c, S, pal, 3, 2.4, 1.5);
  embers(c, S, shut, pal, 7, 2.4);
  flameBody(c, S, shut, pal, 1.5, 1.0);
};

/* ------------------------------------------------------------ A BONE HAND */
window.HAND.A = function(c, R, shut, pal){
  const S = R * 0.80;
  const parts = boneParts(S, shut);
  embers(c, S, shut, pal, 6, 2.6);
  paintBones(c, parts, S, pal, 1.0);
  boneJoints(c, parts, S, pal, 1.0);
};

/* -------------------------------------------------- B BONE HAND, SMALLER */
window.HAND.B = function(c, R, shut, pal){
  const S = R * 0.68;
  const parts = boneParts(S, shut);
  embers(c, S, shut, pal, 5, 2.6);
  paintBones(c, parts, S, pal, 1.15);
  boneJoints(c, parts, S, pal, 1.15);
};

/* -------------------------------------------------------- C BONE AND GHOST */
/* the skeleton INSIDE a faint flesh-glow, so §1's "etheral purple hand" is
   still literally true and the bone is what you read first */
window.HAND.C = function(c, R, shut, pal){
  const S = R * 0.80;
  const ghost = flameParts(S * 1.02, shut);
  c.save();
  c.lineCap = 'round';
  c.globalCompositeOperation = 'lighter';
  c.globalAlpha = 0.13;
  c.strokeStyle = pal.core;
  strokeCaps(c, ghost, S * 0.50);
  c.globalAlpha = 0.22;
  c.strokeStyle = pal.core;
  strokeCaps(c, ghost, S * 0.06);
  c.restore();
  const parts = boneParts(S, shut);
  embers(c, S, shut, pal, 6, 2.6);
  paintBones(c, parts, S, pal, 1.0);
  boneJoints(c, parts, S, pal, 1.0);
};

/* -------------------------------------------------- D FLAME HAND, SMALLER */
/* THE CONTROL. If this reads fine at 0.80x then "comical" was the size and
   bone is a separate decision, not the fix. */
window.HAND.D = function(c, R, shut, pal){
  const S = R * 0.80;
  flameArm(c, S, pal, 3, 2.4, 1.5);
  embers(c, S, shut, pal, 7, 2.4);
  flameBody(c, S, shut, pal, 1.5, 1.0);
};
