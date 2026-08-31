  /* ==== THE HANDS, AND THEY ARE BONE ======================================
     Rick's, over two rounds against rendered spreads (`hand_art_lab.py`,
     `05-reference/v53/hand-shapes.png`).

     ROUND 1 he said "the hands dont read as hands. not detailed enough", and
     sent `Mage_hand_flying_and_fist.mp4` as reference. ROUND 2, on the flame
     hand that came out of it: "the hands are a bit large. they look a little
     comical. and the forearms look like they are just bone. thats got me
     thinking. what if the whole hand was bone?"

     BOTH NOTES WERE ONE DISCOVERY. The flame arm was three glowing strands
     with dark gaps between them, and at this size that is exactly what a
     radius and an ulna look like. The art was already halfway to a skeleton
     and nobody had noticed, including whoever drew it.

     ## WHAT WAS WRONG WAS NEVER THE SIZE, AND THEN IT WAS

     Measured before anything was redrawn: the FIRST hand was 37px across on a
     540 frame and 75px on a phone, on screen for 78 frames, moving 0.65x its
     own width per frame. Large, slow, well lit -- and a filled disc with four
     spokes, which is an asterisk. That was a SHAPE problem.

     The flame hand that replaced it fixed the shape and overshot the scale:
     arm plus hand spanned ~100px on a 540 frame, a fifth of the frame width
     for a thing there are three of at once. THAT was a size problem. Rick
     picked 0.6x off a spread at 0.80 and 0.68.

     ## BONE IS DRAWN THE EXACT INVERSE OF FLESH

     A flame is a volume, so it is EDGE-LIT: bright contour, dim interior. A
     skeleton is bright PARTS with dark GAPS, and the gaps are the entire
     reading -- nothing else in this game is made of separated pieces, so it
     survives a thumbnail that a solid silhouette does not. Two passes, the
     same trick pointed the other way:

       1  a dark stroke per bone, over-wide -- this is what MAKES the gap
       2  a bright fill per bone at true width

     THE GAP MUST NOT SWALLOW THE BONE. The first cut used a 0.13R dark stroke
     against a 0.40R phalanx, the halos merged, and every finger read as a
     string of beads rather than as a finger. 0.075R against 0.54R.

     EVERYTHING IS A PURE FUNCTION OF (hand index, u, contact point). No
     `rng()`: the renderer may not consume the simulation's randomness. */

  /* THE SCALE, AND IT TOOK THREE GOES. Rick's, off rendered spreads:
     the flame hand at 1.15 read "a little comical", 0.6 was his first cut at
     the correction and then "i may have also been heavy handed with the size
     reduction. lets do .7". So 0.7 — and the interesting part is that the
     whole argument was about a number nobody could have picked off a sheet,
     because the sheet shows the object STILL and the complaint was about it
     in motion among two others. */
  _handScale(shut){ return (13 + 5 * (1 - shut)) * 0.7; }

  _boneParts(R, shut){
    const p = [], s = shut;
    /* THE FOREARM IS TWO BONES, and it is the thing that started this. */
    p.push({ x1: -3.00 * R, y1: -0.20 * R, x2: -0.90 * R, y2: -0.22 * R,
             w: 0.20 * R });
    p.push({ x1: -3.00 * R, y1:  0.22 * R, x2: -0.90 * R, y2:  0.18 * R,
             w: 0.17 * R });
    /* the carpals, so the wrist is a joint and not a weld */
    p.push({ x1: -0.78 * R, y1: -0.12 * R, x2: -0.66 * R, y2: -0.12 * R,
             w: 0.22 * R });
    p.push({ x1: -0.78 * R, y1:  0.12 * R, x2: -0.66 * R, y2:  0.12 * R,
             w: 0.22 * R });
    /* four metacarpals, fanning across the back of the hand */
    for (let k = 0; k < 4; k++){
      const y = (-0.46 + k * 0.31) * R;
      p.push({ x1: -0.58 * R, y1: y * 0.42, x2: 0.24 * R, y2: y,
               w: 0.135 * R });
    }
    /* three phalanges a finger, WITH GAPS, curling on the clench */
    for (let k = 0; k < 4; k++){
      const y = (-0.46 + k * 0.31) * R;
      const taper = (k === 3 ? 0.80 : 1) * (k === 0 ? 0.90 : 1);
      let x = 0.30 * R, yy = y, a = s * 0.62;
      for (let seg = 0; seg < 3; seg++){
        const L = R * (0.54 - seg * 0.085) * taper * (1 - 0.20 * s);
        const nx = x + Math.cos(a) * L, ny = yy + Math.sin(a) * L * 0.5;
        p.push({ x1: x, y1: yy, x2: nx, y2: ny,
                 w: (0.125 - seg * 0.018) * R * taper });
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

  _boneStroke(c, parts, extra){
    for (const q of parts){
      c.lineWidth = Math.max(0.4, q.w + extra);
      c.beginPath();
      c.moveTo(q.x1, q.y1);
      c.lineTo(q.x2, q.y2);
      c.stroke();
    }
  }

  _drawBones(c, parts, R, pal, bold){
    /* the halo, so the skeleton sits IN light rather than on top of the hall */
    c.save();
    c.lineCap = "round";
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = 0.16;
    c.strokeStyle = pal.core;
    this._boneStroke(c, parts, R * 0.55 * bold);
    c.restore();
    /* PASS 1 the gap, PASS 2 the bone */
    c.save();
    c.lineCap = "round";
    c.globalCompositeOperation = "source-over";
    c.globalAlpha = 1;
    c.strokeStyle = pal.dark;
    this._boneStroke(c, parts, R * 0.075 * bold);
    c.globalAlpha = 0.96;
    c.strokeStyle = pal.glow;
    this._boneStroke(c, parts, 0);
    /* the joints, on top -- from index 6, so the forearm and carpals are
       skipped and only the hand has knuckles */
    for (let i = 6; i < parts.length; i++){
      const q = parts[i];
      c.fillStyle = pal.dark;
      c.beginPath();
      c.arc(q.x2, q.y2, q.w * 0.62 + R * 0.028 * bold, 0, TAU);
      c.fill();
      c.fillStyle = pal.glow;
      c.beginPath(); c.arc(q.x2, q.y2, q.w * 0.48, 0, TAU); c.fill();
    }
    c.restore();
  }

  _handEmbers(c, R, shut, pal, n, spread){
    c.save();
    c.globalCompositeOperation = "lighter";
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
      c.arc(x, y, R * (0.05 + h2 * 0.05), 0, TAU);
      c.fill();
    }
    c.restore();
  }

  /* Drawn in the EMISSIVE pass so the bloom reaches them, and over the
     fighters, because a hand diving at a ball is in front of it. */
  drawHands(m){
    if (!m.hands.length) return;
    const c = this.ctx, U = AFFINITIES.umbral;
    for (const h of m.hands){
      if (h.t < 0) continue;
      /* THE CLENCH IS LATE, so the soar is most of the flight and the fist is
         the arrival. `handFly` is 1.8s and the last 30% of it is the dive. */
      const shut = clamp((h.u - 0.62) / 0.30, 0, 1);
      const ang = Math.atan2(h.y - h.ly, h.x - h.lx);
      const R = this._handScale(shut);
      const parts = this._boneParts(R, shut);
      c.save();
      c.translate(h.x, h.y);
      c.rotate(ang);
      this._handEmbers(c, R, shut, U, 6, 2.6);
      this._drawBones(c, parts, R, U, 1.0);
      c.restore();
    }
  }
