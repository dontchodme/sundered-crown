  /* ------------------------------------------------------------- UMBRAL --
     GNAWED TO THE BONE. Replaces `_whEaten`, on Rick's rejection of it:
     *"umbral hammers silhouette looks pretty bad ... the hammer with blocks
     attached to it idea just isnt working for me."*

     WHY THE OLD ONE FAILED, and it is a lesson about the grammar and not
     about that function. `_whEaten` was purely SUBTRACTIVE: it called
     `_whBase` and punched two blobs and a slot out of it with
     `destination-out`. Subtracting from a shape that is already rectilinear
     does not produce an absence, it produces SMALLER RECTANGLES -- the haft
     came apart into two bars with a gap, and the head into lumps -- which is
     exactly the "blocks attached to it" Rick saw. Every other grammar on this
     row ADDS a contour (halo, thorns, hooks, burl, plates, langets, floating
     cluster); umbral was the only one that removed one, and removal is the
     weakest silhouette operation there is because it takes area without
     giving the outline a new event.

     WHAT REPLACES IT. The school still says the iron is incomplete -- but
     what is missing is the SMOOTH BLOCK, and what the eating exposed is bone.
     Three bone spikes above, three below, a beak and a rear spur, all grown
     out of a near-black head with the school's light banked inside it.

     THE ONE RULE THAT MATTERS HERE: head, spikes, beak and spur are ONE
     CLOSED PATH -- one fill, one stroke, no internal edges anywhere. Drawn as
     separate stroked shapes behind the head they read as triangles layered
     behind a block (Rick, on the first cut: *"upclose the spikes just look
     like triangles layered behind the hammer"*). A spike that shares the
     head's outline cannot come apart from it at any zoom. Each spike's light
     then fades to nothing just INSIDE the iron, so it reads as seated in the
     head rather than glued to its edge.

     And there is no `destination-out` in this function at all -- see the note
     in the v58 doc about what the old bites did to whatever was behind them. */
  _whGnawed(c, L, W, p){
    const SPIKE = 0.64;          // spike length knob. tips land at
                                 // hy + hh*(0.28 + 0.50*SPIKE). Rick's, from a
                                 // ladder of four. The only knob in the shape
    const hh = W*0.50;
    const x0 = L*0.585, x1 = L*0.935, hy = hh*0.92;   // the head. LONGER than
    const ch = (x1-x0)*0.16, rw = L*0.043;            // `_whBase`'s 0.64L: in
    const tipY = hy + hh*(0.28 + 0.50*SPIKE);         // all three of Rick's
    const spur = L*(0.115 + 0.075*SPIKE);             // references the head is
    const beak = L - x1;                              // the mass and the rest
    const SX = [0.655, 0.760, 0.865].map(v => L*v);   // is trim
    const bone   = SHAPES._shade(p.glow, 1.06, 0.66); // desaturated toward its
    const boneDk = SHAPES._shade(p.glow, 0.46, 0.62); // own luminance: bone the
    const iron   = SHAPES._shade(p.dark, 0.92, 0.04); // palette still owns
    const ironLt = SHAPES._shade(p.dark, 1.85, 0.10);
    const rim    = SHAPES._shade(p.core, 0.62, 0.26);

    c.save();
    c.fillStyle = SHAPES._shade(p.dark, 1.30, 0.12);            // the haft
    c.fillRect(0, -W*0.074, x0 + L*0.03, W*0.148);
    c.fillStyle = p.core;
    for (const bx of [0.14, 0.22, 0.30]) c.fillRect(L*bx, -W*0.086, L*0.022, W*0.172);
    c.fillStyle = p.glow;
    c.fillRect(-L*0.015, -W*0.105, L*0.045, W*0.210);           // lit butt

    /* ONE outline, walked clockwise. Every spike is a detour along an edge the
       head already had -- not a new object laid over it. */
    const path = (cc) => {
      cc.beginPath();
      cc.moveTo(x0, -hy*0.80);
      cc.lineTo(x0 + ch*0.5, -hy);
      for (const sx of SX){
        cc.lineTo(sx - rw, -hy);
        cc.lineTo(sx - L*0.014, -tipY);
        cc.lineTo(sx + rw, -hy);
      }
      cc.lineTo(x1 - ch, -hy);
      cc.lineTo(x1, -hy*0.74);
      cc.lineTo(x1 + beak*0.30, -hy*0.44);
      cc.lineTo(L, 0);                                          // NEVER past L
      cc.lineTo(x1 + beak*0.30,  hy*0.44);
      cc.lineTo(x1,  hy*0.74);
      cc.lineTo(x1 - ch,  hy);
      for (let i = SX.length - 1; i >= 0; i--){
        const sx = SX[i];
        cc.lineTo(sx + rw, hy);
        cc.lineTo(sx - L*0.014, tipY);
        cc.lineTo(sx - rw, hy);
      }
      cc.lineTo(x0 + ch*0.5, hy);
      cc.lineTo(x0, hy*0.80);
      cc.lineTo(x0, hy*0.34);
      cc.lineTo(x0 - spur, 0);                                  // the rear spur
      cc.lineTo(x0, -hy*0.34);
      cc.closePath();
    };

    path(c);                                                    // ONE fill
    const g = c.createLinearGradient(0, -hy, 0, hy);
    g.addColorStop(0.00, ironLt);
    g.addColorStop(0.42, iron);
    g.addColorStop(1.00, SHAPES._shade(p.dark, 0.62, 0.04));
    c.fillStyle = g; c.fill();

    c.save(); path(c); c.clip();                                // the light
    for (const sx of SX) for (const sg of [-1, 1]){
      const rootY = sg*hy*0.86, tY = sg*tipY;                   // root is INSIDE
      const lg = c.createLinearGradient(0, rootY, 0, tY);        // the iron
      lg.addColorStop(0, boneDk + "00");
      lg.addColorStop(0.20, boneDk);
      lg.addColorStop(0.46, bone);
      lg.addColorStop(1, bone);
      c.fillStyle = lg;
      c.beginPath();
      c.moveTo(sx - rw*1.06, rootY);
      c.lineTo(sx - L*0.014, tY);
      c.lineTo(sx + rw*1.06, rootY);
      c.closePath(); c.fill();
    }
    for (const [ax, bx, hgt] of [[x1 - beak*0.16, L, 0.52],
                                 [x0 + spur*0.08, x0 - spur, 0.22]]){
      const lg = c.createLinearGradient(ax, 0, bx, 0);
      lg.addColorStop(0, boneDk + "00");
      lg.addColorStop(0.20, boneDk);
      lg.addColorStop(0.46, bone);
      lg.addColorStop(1, bone);
      c.fillStyle = lg;
      c.beginPath();
      c.moveTo(ax, -hy*hgt); c.lineTo(bx, 0); c.lineTo(ax, hy*hgt);
      c.closePath(); c.fill();
    }
    c.fillStyle = p.core;                                       // banked light
    c.beginPath(); c.ellipse(L*0.760, 0, hh*0.27, hh*0.42, 0, 0, TAU); c.fill();
    c.fillStyle = p.glow;
    c.beginPath(); c.ellipse(L*0.760, 0, hh*0.125, hh*0.19, 0, 0, TAU); c.fill();
    c.fillStyle = p.core;                                       // four studs
    for (const sg of [-1, 1]) for (const bx of [0.655, 0.865]){
      c.beginPath(); c.arc(L*bx, sg*hh*0.58, hh*0.13, 0, TAU); c.fill();
    }
    c.restore();

    path(c);                                                    // ONE stroke
    c.lineJoin = "round";
    c.strokeStyle = rim;
    c.lineWidth = Math.max(1, W*0.042);
    c.stroke();
    c.restore();
  },
