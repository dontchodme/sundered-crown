/* ------------------------------------------------------------------ STAFF --
   THE STAFF ROW'S ART — CONCEPTS (v89). Cowork, 2026-09-27. Rick: "we are
   also going to art for the weapons. how about you do concepts and code
   builds them?" — and on the first sheet: "those all look like wands at
   best ... wanting a clear wizards staff." So: SECOND CUT. This file is the
   CONCEPT SPEC, three candidates a school (A/B/C) on ONE pole, drawn with the
   engine's own SHAPES helpers on the engine's own frame, rendered to
   `05-reference/v89/staff-sheet*.png` by `tools/staff_art_lab.py`. Rick
   picks one letter a school; Code pastes THIS function as `SHAPES.staff`,
   sets `STAFF.pick` to the seven letters, and deletes the losers. Nothing
   here touches the sim.

   WHAT MAKES IT A WIZARD'S STAFF AND NOT A WAND (the first cut's failure):
   * IT IS LONG. The pole runs THROUGH the ball — held at its middle — from a
     shod butt sticking out the far side to the head on the reach side: ~2.5
     ball diameters end to end. `drawFighter` draws the weapon UNDER the
     shell, so the middle is hidden and the two ends show; the first cut
     started at the ball's edge and could only ever be a stub.
   * IT IS GNARLED. The pole is a closed path with a wobbling width and a
     slight bend, not a tapered rectangle; a wrapped grip where the hand
     would be; an iron shoe at the butt.
   * THE HEAD IS BIG — half the ball across — and it HOLDS something: a claw
     of wood holding an orb, a crook, a cage, a bell. The thing it holds is
     the school's light and is where the spell leaves from (~0.95 L).

   THE FRAME (drawWeapon): translated to the ball's edge (R - 6 from centre),
   rotated to the facing, local +x OUT along the weapon. `litWeapon` calls
   `fn(c, L, W, p, k)` with L = reach + 6 = 60 and W = artW = 44. The ball
   is R = 34; everything left of x = -(2R - 6) = -62 is past the far edge.

   THE GRAMMAR (the bow's, v40; the moon's, v63): three passes (near-black
   silhouette first and widest, the school's `dark`, one `steel` line); one
   structural detail a school, in the head; a limb goes INTO the outline
   (v58); `core`/`glow` only on the thing the head holds. The art's reach is
   printed by the lab (the moon ships at 1.08 L).
*/
const STAFF = {
  pick: { bloodsworn:"A", umbral:"A", vigil:"A", verdant:"A", runic:"A", sanctified:"A", dwarven:"A" },
  TAU: Math.PI * 2,

  /* ---- THE POLE, shared. From the butt (past the ball's far side) to
          `end` L. Gnarled: the half-width is `hw` modulated by two sines and
          the centreline bends by `bend`; the whole thing is ONE closed path
          drawn three times. `grip` wraps the pole just outside the ball on
          the head side. `shoe` is the iron at the butt. ---- */
  pole(c, L, W, p, o){
    const S = SHAPES;
    /* CUT 3 (Rick: "staffs should be longer and not stick through the whole
       artifact"): the pole starts at the ball's edge and goes OUT, long. No
       butt on the far side. L here is already 1.7x the sim reach (the
       dispatcher), so a pole to 0.7 L is 1.2 reaches and a head at 0.8-1.0 L
       sits at 1.4-1.7 reaches: the staff is the longest weapon on the ball. */
    const xb = -L*0.05, xe = L*(o.end ?? 0.70);
    const hw = W*(o.hw ?? 0.09), gn = o.gnarl ?? 0.26, bend = W*(o.bend ?? 0.08);
    const N = 28, top = [], bot = [];
    for (let i = 0; i <= N; i++){
      const t = i/N, x = xb + (xe - xb)*t;
      const cy = bend*Math.sin(t*Math.PI*1.3 + 0.4);                       // the bend
      const w = hw*(1 + gn*Math.sin(t*19 + 1.1)*0.6 + gn*Math.sin(t*7.3)*0.4) * (0.82 + 0.18*(1 - t));  // gnarl + a taper toward the head
      top.push([x, cy - w]); bot.push([x, cy + w]);
    }
    const path = (g) => { c.beginPath();
      top.forEach(([x, y], i) => i ? c.lineTo(x, y - g) : c.moveTo(x, y - g));
      for (let i = bot.length - 1; i >= 0; i--) c.lineTo(bot[i][0], bot[i][1] + g);
      c.closePath(); };
    c.lineJoin = "round";
    path(W*0.05); c.fillStyle = S._ink(p.dark, 9.7); c.fill();               // silhouette
    path(0); c.fillStyle = o.body || S._shade(p.dark, 1.15, 0.05); c.fill();  // body
    c.strokeStyle = S._shade(p.steel, 0.7, 0.4); c.lineWidth = Math.max(1, W*0.03); c.lineCap = "round";
    c.beginPath(); top.forEach(([x, y], i) => { const yy = y + hw*0.45; i ? c.lineTo(x, yy) : c.moveTo(x, yy); }); c.stroke();  // one lit line
    // the grip: wraps just outside the ball on the head side
    if (o.grip !== false){
      c.strokeStyle = S._ink(p.dark, 18); c.lineWidth = Math.max(1, W*0.045);
      for (let i = 0; i < 4; i++){ const x = L*(0.03 + 0.045*i); c.beginPath(); c.moveTo(x - W*0.03, -hw*1.15); c.lineTo(x + W*0.03, hw*1.15); c.stroke(); }
    }
    return { xe, hw };
  },
  /* a gem/orb: dark bezel, lit core, soft falloff (v63's socket) */
  orb(c, x, y, r, p, hue){
    const S = SHAPES, TAU = STAFF.TAU;
    c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.arc(x, y, r*1.22, 0, TAU); c.fill();
    const g = c.createRadialGradient(x - r*0.3, y - r*0.3, 0, x, y, r);
    g.addColorStop(0, hue || p.glow); g.addColorStop(0.45, p.core); g.addColorStop(1, S._shade(p.core, 0.45, 0.2));
    c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    c.fillStyle = "rgba(255,255,255,0.35)"; c.beginPath(); c.ellipse(x - r*0.35, y - r*0.4, r*0.28, r*0.16, -0.6, 0, TAU); c.fill();
  },
  /* a CLAW of wood: `n` gnarled fingers growing from x0 and curling to hold
     something centred at (cx, 0) of radius r. Each finger is one closed
     path (v58). */
  claw(c, x0, cx, r, n, W, p, col){
    const S = SHAPES;
    for (let i = 0; i < n; i++){
      const a = (n === 1) ? 0 : (-0.9 + 1.8*i/(n - 1));
      const ex = cx + Math.cos(a)*r*1.05, ey = Math.sin(a)*r*1.05;          // fingertip, on the thing held
      const mx = x0 + (ex - x0)*0.5, my = ey*1.9;                             // bows outward, then in
      const fin = (g, colr) => { c.fillStyle = colr; c.beginPath();
        c.moveTo(x0, -W*0.10 - g); c.quadraticCurveTo(mx, my - W*0.14 - g, ex + g*0.5, ey - W*0.03 - g*0.6);
        c.lineTo(ex + g*0.5, ey + W*0.03 + g*0.6); c.quadraticCurveTo(mx, my + W*0.14 + g, x0, W*0.10 + g); c.closePath(); c.fill(); };
      fin(W*0.045, S._ink(p.dark, 9.7)); fin(0, col || S._shade(p.dark, 1.15, 0.05));
      c.strokeStyle = S._shade(p.steel, 0.7, 0.4); c.lineWidth = 1; c.beginPath(); c.moveTo(x0, -W*0.06); c.quadraticCurveTo(mx, my - W*0.08, ex, ey - W*0.02); c.stroke();  // one lit line per finger, so it reads on a dark ball
    }
  },

  /* ================================================================ HEADS = */

  /* BLOODSWORN — BLOODWICK. The staff is a candle of blood.
     A: a CLAW holding a blood-glass orb with a flame standing off it.
     B: a CHALICE — a wide cup at the head, the flame tall out of it.
     C: TWO HORNS — the pole forks into two curling horns, the flame burning
        between them (the wick is the gap). */
  bloodsworn(c, L, W, p, v){
    const S = SHAPES;
    const flame = (fx, fl, fh) => {
      c.fillStyle = p.core; c.beginPath(); c.moveTo(fx, -fh); c.quadraticCurveTo(fx + fl*0.55, -fh*1.1, fx + fl, 0); c.quadraticCurveTo(fx + fl*0.55, fh*1.1, fx, fh); c.closePath(); c.fill();
      c.fillStyle = p.glow; c.beginPath(); c.moveTo(fx, -fh*0.45); c.quadraticCurveTo(fx + fl*0.4, -fh*0.5, fx + fl*0.6, 0); c.quadraticCurveTo(fx + fl*0.4, fh*0.5, fx, fh*0.45); c.closePath(); c.fill(); };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.56 });
      const cx = L*0.80, r = W*0.26;
      STAFF.claw(c, L*0.52, cx, r, 3, W, p);
      STAFF.orb(c, cx, 0, r, p);
      flame(cx + r*0.9, L*0.18, W*0.16);
    } else if (v === "B"){
      /* the THISTLE (Rick's ref 1): a calyx of dark spikes and a bloom of blood standing out of it */
      STAFF.pole(c, L, W, p, { end: 0.60, gnarl: 0.34 });
      const cx = L*0.60, cw = L*0.24, ch = W*0.30;
      const calyx = (g, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(cx - g, -W*0.08 - g);
        for (let i = 0; i < 5; i++){ const t = i/4; const x = cx + cw*(0.35 + 0.65*t) + g, y = -ch*(0.5 + 0.5*t) - g; c.lineTo(x - cw*0.10, y*0.55); c.lineTo(x, y); }
        for (let i = 4; i >= 0; i--){ const t = i/4; const x = cx + cw*(0.35 + 0.65*t) + g, y = ch*(0.5 + 0.5*t) + g; c.lineTo(x, y); c.lineTo(x - cw*0.10, y*0.55); }
        c.lineTo(cx - g, W*0.08 + g); c.closePath(); c.fill(); };
      calyx(W*0.045, S._ink(p.dark, 9.7)); calyx(0, S._ink(p.dark, 22));
      c.strokeStyle = S._shade(p.steel, 0.6, 0.4); c.lineWidth = 1; c.beginPath(); c.moveTo(cx + cw*0.3, -ch*0.3); c.lineTo(cx + cw*0.9, -ch*0.75); c.stroke();
      // the bloom: a burst of petals, core and glow, leaning out along +x
      for (let i = 0; i < 9; i++){ const a = -0.9 + 1.8*i/8, len = L*(0.20 + 0.06*Math.cos(a*2.2)); c.save(); c.translate(cx + cw*0.95, 0); c.rotate(a);
        c.fillStyle = i % 2 ? p.glow : p.core; c.beginPath(); c.moveTo(0, -W*0.035); c.quadraticCurveTo(len*0.6, -W*0.06, len, 0); c.quadraticCurveTo(len*0.6, W*0.06, 0, W*0.035); c.closePath(); c.fill(); c.restore(); }
      c.fillStyle = p.core; c.beginPath(); c.arc(cx + cw*0.95, 0, W*0.08, 0, STAFF.TAU); c.fill();
    } else {
      STAFF.pole(c, L, W, p, { end: 0.58 });
      for (const sg of [-1, 1]){                                              // two horns curling out and back
        const horn = (g, col) => { c.strokeStyle = col; c.lineWidth = Math.max(1, W*(0.11 + g)); c.lineCap = "round"; c.beginPath();
          c.moveTo(L*0.56, 0); c.quadraticCurveTo(L*0.80, sg*W*0.05, L*0.86, sg*W*0.34); c.quadraticCurveTo(L*0.88, sg*W*0.50, L*0.76, sg*W*0.48); c.stroke(); };
        horn(0.06, S._ink(p.dark, 9.7)); horn(0, S._shade(p.dark, 1.15, 0.05));
      }
      flame(L*0.74, L*0.24, W*0.22);
    }
  },

  /* UMBRAL — NIGHTGLASS. Black glass that reflects.
     A: a CLAW holding a black mirror-orb, one violet glint in it.
     B: a CRESCENT of dark wood (the moon, v63's own sign) cradling a shard.
     C: a jointed pole (three segments, the moon's shaft) ending in a black
        PRISM. */
  umbral(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU;
    const glass = (x, y, r) => { c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.arc(x, y, r*1.2, 0, TAU); c.fill();
      c.fillStyle = S._ink(p.dark, 4); c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
      c.strokeStyle = p.core + "CC"; c.lineWidth = Math.max(1, W*0.04); c.beginPath(); c.arc(x, y, r*0.66, Math.PI*1.1, Math.PI*1.7); c.stroke();
      c.fillStyle = p.glow; c.beginPath(); c.arc(x + r*0.3, y + r*0.25, r*0.12, 0, TAU); c.fill(); };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.54, body: S._ink(p.dark, 22) });
      const cx = L*0.80, r = W*0.27;
      STAFF.claw(c, L*0.50, cx, r, 3, W, p, S._ink(p.dark, 30));
      glass(cx, 0, r);
    } else if (v === "B"){
      /* the COIL (Rick's ref 4): a scaled serpent winds up the pole and wraps the glass, its head over the top of it */
      STAFF.pole(c, L, W, p, { end: 0.62, body: S._ink(p.dark, 22) });
      const cx = L*0.82, r = W*0.27;
      const coil = (wd, col) => { c.strokeStyle = col; c.lineWidth = Math.max(1, W*wd); c.lineCap = "round"; c.beginPath();
        c.moveTo(L*0.20, W*0.08); c.quadraticCurveTo(L*0.36, -W*0.16, L*0.50, W*0.02); c.quadraticCurveTo(L*0.62, W*0.20, L*0.68, -W*0.30);
        c.arc(cx, 0, r*1.35, -Math.PI*0.95, Math.PI*0.75); c.stroke(); };
      coil(0.20, S._ink(p.dark, 9.7)); coil(0.12, S._shade(p.steel, 0.5, 0.3));
      c.strokeStyle = S._ink(p.dark, 14); c.lineWidth = 1;                                     // scales: short ticks across the coil
      for (let i = 0; i < 9; i++){ const a = -Math.PI*0.9 + i*0.42; const x = cx + Math.cos(a)*r*1.35, y = Math.sin(a)*r*1.35; c.beginPath(); c.moveTo(x - Math.sin(a)*W*0.05, y + Math.cos(a)*W*0.05); c.lineTo(x + Math.sin(a)*W*0.05, y - Math.cos(a)*W*0.05); c.stroke(); }
      glass(cx, 0, r);
      const hx = cx + Math.cos(Math.PI*0.75)*r*1.35, hy = Math.sin(Math.PI*0.75)*r*1.35;   // the head, a wedge over the orb's edge
      const head = (g, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(hx - W*0.02 - g, hy - W*0.10 - g); c.lineTo(hx + W*0.22 + g, hy - W*0.02); c.lineTo(hx - W*0.02 - g, hy + W*0.10 + g); c.closePath(); c.fill(); };
      head(W*0.04, S._ink(p.dark, 9.7)); head(0, S._shade(p.steel, 0.5, 0.3));
      c.fillStyle = p.core; c.beginPath(); c.arc(hx + W*0.05, hy - W*0.02, W*0.025, 0, TAU); c.fill();
    } else {
      STAFF.pole(c, L, W, p, { end: 0.58, gnarl: 0.05, body: S._ink(p.dark, 22) });
      for (const x of [L*0.10, L*0.30, L*0.50]){                                 // the moon's jointed segments
        c.fillStyle = S._ink(p.dark, 26); c.beginPath();
        c.moveTo(x - W*0.11, 0); c.lineTo(x - W*0.06, -W*0.16); c.lineTo(x + W*0.06, -W*0.16); c.lineTo(x + W*0.11, 0); c.lineTo(x + W*0.06, W*0.16); c.lineTo(x - W*0.06, W*0.16); c.closePath(); c.fill();
        c.strokeStyle = p.core + "AA"; c.lineWidth = Math.max(1, W*0.03); c.stroke();
      }
      const cx = L*0.80, r = W*0.30;
      const hex = (g, col) => { c.fillStyle = col; c.beginPath();
        for (let i = 0; i < 6; i++){ const a = i*TAU/6; const rr = r + g; c.lineTo(cx + Math.cos(a)*rr*(i === 0 ? 1.2 : i === 3 ? 0.9 : 1), Math.sin(a)*rr*0.9); }
        c.closePath(); c.fill(); };
      hex(W*0.05, S._ink(p.dark, 9.7)); hex(0, S._ink(p.dark, 4));
      c.strokeStyle = S._shade(p.steel, 0.8, 0.3); c.lineWidth = Math.max(1, W*0.03); c.beginPath(); c.moveTo(cx - r*0.5, -r*0.78); c.lineTo(cx + r*0.5, -r*0.78); c.stroke();
      c.strokeStyle = p.core + "CC"; c.lineWidth = Math.max(1, W*0.04); c.beginPath(); c.moveTo(cx - r*0.4, r*0.1); c.lineTo(cx + r*0.5, r*0.1); c.stroke();
      c.fillStyle = p.glow; c.beginPath(); c.arc(cx + r*0.2, -r*0.2, W*0.04, 0, TAU); c.fill();
    }
  },

  /* VIGIL — WATCHLIGHT. The staff is a lamp-post.
     A: a CAGE lantern hung from a bracket, warm core inside, three bars.
     B: a HOODED lamp — a half-shell open toward +x, so the light has a
        direction (the beacon looks where it fires).
     C: PLATES down the pole (the ward's own material, the bow's grammar)
        and a round lamp in a claw at the tip. */
  vigil(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU;
    const light = (x, y, r) => { const g = c.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, p.glow); g.addColorStop(0.5, p.core); g.addColorStop(1, p.core + "00"); c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.56 });
      // the bracket: a hook off the pole's end, the lantern hangs under it
      c.strokeStyle = S._ink(p.dark, 9.7); c.lineWidth = Math.max(1, W*0.15); c.lineCap = "round"; c.beginPath(); c.moveTo(L*0.54, 0); c.quadraticCurveTo(L*0.80, -W*0.02, L*0.84, -W*0.34); c.stroke();
      c.strokeStyle = p.dark; c.lineWidth = Math.max(1, W*0.08); c.beginPath(); c.moveTo(L*0.54, 0); c.quadraticCurveTo(L*0.80, -W*0.02, L*0.84, -W*0.34); c.stroke();
      const x0 = L*0.66, x1 = L*1.00, y0 = -W*0.30, y1 = W*0.36;                 // the cage, hung below the hook
      c.fillStyle = S._ink(p.dark, 9.7); c.fillRect(x0 - W*0.05, y0 - W*0.05, x1 - x0 + W*0.10, y1 - y0 + W*0.10);
      c.fillStyle = p.dark; c.fillRect(x0, y0, x1 - x0, y1 - y0);
      light((x0 + x1)/2, (y0 + y1)/2, (y1 - y0)*0.55);
      c.fillStyle = S._ink(p.dark, 9.7);
      for (const u of [0.34, 0.67]) c.fillRect(x0 + (x1 - x0)*u - W*0.025, y0, W*0.05, y1 - y0);
      c.fillRect(x0 - W*0.03, y0 - W*0.02, x1 - x0 + W*0.06, W*0.07); c.fillRect(x0 - W*0.03, y1 - W*0.05, x1 - x0 + W*0.06, W*0.07);
      c.strokeStyle = S._shade(p.steel, 0.75, 0.35); c.lineWidth = Math.max(1, W*0.03); c.beginPath(); c.moveTo(x0 + W*0.02, y0 + W*0.015); c.lineTo(x1 - W*0.02, y0 + W*0.015); c.stroke();
    } else if (v === "B"){
      STAFF.pole(c, L, W, p, { end: 0.62 });
      const cx = L*0.76, r = W*0.34;
      const hood = (g, col) => { c.fillStyle = col; c.beginPath(); c.arc(cx, 0, r + g, Math.PI*0.5, Math.PI*1.5); c.lineTo(cx + W*0.10 + g, -r - g); c.lineTo(cx + W*0.10 + g, r + g); c.closePath(); c.fill(); };
      hood(W*0.05, S._ink(p.dark, 9.7)); hood(0, p.dark);
      light(cx + r*0.25, 0, r*0.95);
      c.strokeStyle = S._shade(p.steel, 0.75, 0.35); c.lineWidth = Math.max(1, W*0.035); c.beginPath(); c.arc(cx, 0, r*0.86, Math.PI*0.62, Math.PI*1.38); c.stroke();
      c.fillStyle = S._ink(p.dark, 9.7); c.fillRect(cx + W*0.06, -r - W*0.02, W*0.05, r*2 + W*0.04);   // the lip of the hood
    } else {
      STAFF.pole(c, L, W, p, { end: 0.60, grip: false });
      for (let i = 0; i < 4; i++){                                                   // the plates
        const x = L*(0.06 + 0.13*i);
        c.fillStyle = S._ink(p.dark, 10.4); c.fillRect(x - W*0.05, -W*0.20, W*0.10, W*0.40);
        c.fillStyle = p.core; c.fillRect(x - W*0.035, -W*0.15, W*0.07, W*0.30);
        c.fillStyle = p.glow; c.fillRect(x - W*0.035, -W*0.15, W*0.07, W*0.06);
      }
      const cx = L*0.82, r = W*0.24;
      STAFF.claw(c, L*0.56, cx, r, 3, W, p, p.dark);
      c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.arc(cx, 0, r*1.15, 0, TAU); c.fill();
      c.fillStyle = p.dark; c.beginPath(); c.arc(cx, 0, r, 0, TAU); c.fill();
      light(cx, 0, r*0.9);
    }
  },

  /* VERDANT — BRIARWAND. The staff is a living branch.
     A: the pole FORKS into a gnarled claw holding a green orb, thorns on
        the fork (the fan's three thorns are in the wood).
     B: a TENDRIL coils once round the head and grips an orb; leaves.
     C: an OPEN FLOWER: five petals about a lit heart, thorns down the pole. */
  verdant(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU, wood = S._shade(p.dark, 1.25, 0.0);
    const thorn = (x, y, a, len, g, col) => { c.save(); c.translate(x, y); c.rotate(a);
      c.fillStyle = col; c.beginPath(); c.moveTo(-W*0.06 - g, -W*0.07 - g); c.lineTo(len + g, 0); c.lineTo(-W*0.06 - g, W*0.07 + g); c.closePath(); c.fill(); c.restore(); };
    const thorns = (list) => { for (const [x, a, len] of list){ thorn(x, 0, a, len, W*0.035, S._ink(p.dark, 9.7)); thorn(x, 0, a, len, 0, wood); } };
    const leaf = (x, y, a, len) => { c.save(); c.translate(x, y); c.rotate(a);
      c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(len*0.5, -len*0.42, len*1.06, 0); c.quadraticCurveTo(len*0.5, len*0.42, 0, 0); c.fill();
      c.fillStyle = S._shade(p.core, 0.55, 0.1); c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(len*0.5, -len*0.34, len, 0); c.quadraticCurveTo(len*0.5, len*0.34, 0, 0); c.fill();
      c.strokeStyle = p.glow + "88"; c.lineWidth = 1; c.beginPath(); c.moveTo(0, 0); c.lineTo(len*0.9, 0); c.stroke(); c.restore(); };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.54, body: wood, gnarl: 0.3 });
      thorns([[L*0.14, -1.0, W*0.16], [L*0.26, 1.0, W*0.18], [L*0.38, -0.9, W*0.16]]);
      const cx = L*0.80, r = W*0.25;
      STAFF.claw(c, L*0.50, cx, r, 3, W, p, wood);
      thorns([[L*0.66, -0.55, W*0.16], [L*0.66, 0.55, W*0.16], [L*0.62, -1.3, W*0.14]]);
      STAFF.orb(c, cx, 0, r, p);
    } else if (v === "B"){
      STAFF.pole(c, L, W, p, { end: 0.60, body: wood, gnarl: 0.3 });
      leaf(L*0.26, -W*0.06, -1.1, W*0.28); leaf(L*0.40, W*0.06, 1.15, W*0.24);
      const cx = L*0.80, r = W*0.24;
      const coil = (g, col) => { c.strokeStyle = col; c.lineWidth = Math.max(1, W*(0.10 + g)); c.lineCap = "round"; c.beginPath();
        c.moveTo(L*0.58, 0); c.quadraticCurveTo(L*0.66, -W*0.34, cx, -W*0.40); c.arc(cx, 0, r*1.55, -Math.PI*0.5, Math.PI*0.95); c.stroke(); };
      coil(0.06, S._ink(p.dark, 9.7)); coil(0, wood);
      STAFF.orb(c, cx, 0, r, p);
      thorn(cx + Math.cos(Math.PI*0.95)*r*1.55, Math.sin(Math.PI*0.95)*r*1.55, 2.4, W*0.16, W*0.03, S._ink(p.dark, 9.7));
      thorn(cx + Math.cos(Math.PI*0.95)*r*1.55, Math.sin(Math.PI*0.95)*r*1.55, 2.4, W*0.16, 0, wood);
    } else {
      STAFF.pole(c, L, W, p, { end: 0.62, body: wood, gnarl: 0.3 });
      thorns([[L*0.16, -1.0, W*0.16], [L*0.30, 1.0, W*0.16], [L*0.44, -0.95, W*0.16]]);
      const cx = L*0.82, pr = W*0.32;
      for (let i = 0; i < 5; i++){
        const a = i*TAU/5;
        c.save(); c.translate(cx, 0); c.rotate(a);
        const pet = (g, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(pr*0.55, -pr*0.42 - g, pr + g, 0); c.quadraticCurveTo(pr*0.55, pr*0.42 + g, 0, 0); c.closePath(); c.fill(); };
        pet(W*0.045, S._ink(p.dark, 9.7)); pet(0, S._shade(p.dark, 1.7, 0.0));
        c.strokeStyle = p.core + "77"; c.lineWidth = 1; c.beginPath(); c.moveTo(pr*0.15, 0); c.lineTo(pr*0.85, 0); c.stroke();
        c.restore();
      }
      STAFF.orb(c, cx, 0, W*0.12, p);
    }
  },

  /* RUNIC — CIPHER. Runes cut down the pole; the head is a frame the bolt
     is born inside. A: an open RING holding an orb (Rick's ref 3), the glyph in the orb. B: a BROKEN
     CIRCLE, two arcs, the gap toward +x (the bolt leaves through it).
     C: a TRIANGLE frame, a rune-stone at each corner, the glyph inside. */
  runic(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU;
    const runes = () => { c.strokeStyle = p.core + "CC"; c.lineWidth = Math.max(1, W*0.03); c.lineCap = "round";
      const xs = [L*0.06, L*0.14, L*0.22, L*0.30, L*0.38, L*0.46];
      xs.forEach((x, i) => { c.beginPath(); c.moveTo(x, -W*0.07); c.lineTo(x + W*0.04, W*0.07); if (i % 2){ c.moveTo(x - W*0.02, 0); c.lineTo(x + W*0.06, 0); } else { c.moveTo(x + W*0.04, -W*0.07); c.lineTo(x + W*0.07, -W*0.02); } c.stroke(); }); };
    const glyph = (x, r) => { c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.04); c.lineCap = "round";
      c.beginPath(); c.moveTo(x - r, -r); c.lineTo(x + r, r); c.moveTo(x + r*0.2, -r); c.lineTo(x - r*0.2, r); c.moveTo(x - r*0.9, r*0.1); c.lineTo(x + r*0.9, r*0.1); c.stroke();
      c.fillStyle = p.glow; c.beginPath(); c.arc(x, r*0.1, W*0.03, 0, TAU); c.fill(); };
    const stone = (x, y, r) => { c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.arc(x, y, r*1.3, 0, TAU); c.fill(); c.fillStyle = S._shade(p.dark, 1.5, 0.1); c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); c.fillStyle = p.core; c.beginPath(); c.arc(x, y, r*0.45, 0, TAU); c.fill(); };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.52 }); runes();
      const cx = L*0.80, r = W*0.33;
      STAFF.claw(c, L*0.50, cx, r, 2, W, p);
      c.strokeStyle = S._ink(p.dark, 9.7); c.lineWidth = Math.max(1, W*0.16); c.beginPath(); c.arc(cx, 0, r, 0, TAU); c.stroke();
      c.strokeStyle = S._shade(p.dark, 1.3, 0.1); c.lineWidth = Math.max(1, W*0.09); c.beginPath(); c.arc(cx, 0, r, 0, TAU); c.stroke();
      c.strokeStyle = S._shade(p.steel, 0.8, 0.3); c.lineWidth = Math.max(1, W*0.025); c.beginPath(); c.arc(cx, 0, r*0.8, Math.PI*1.1, Math.PI*1.9); c.stroke();
      STAFF.orb(c, cx - r*0.05, 0, r*0.52, p);
      c.globalAlpha = 0.55; glyph(cx - r*0.05, r*0.28); c.globalAlpha = 1;
    } else if (v === "B"){
      STAFF.pole(c, L, W, p, { end: 0.60 }); runes();
      const cx = L*0.74;
      for (const [r, wd, a0, a1] of [[W*0.36, 0.14, 0.6, TAU - 0.6], [W*0.21, 0.11, 1.0, TAU - 1.0]]){
        c.strokeStyle = S._ink(p.dark, 9.7); c.lineWidth = Math.max(1, W*(wd + 0.07)); c.lineCap = "round"; c.beginPath(); c.arc(cx, 0, r, a0, a1); c.stroke();
        c.strokeStyle = S._shade(p.dark, 1.3, 0.1); c.lineWidth = Math.max(1, W*wd); c.beginPath(); c.arc(cx, 0, r, a0, a1); c.stroke();
      }
      c.strokeStyle = p.core + "CC"; c.lineWidth = Math.max(1, W*0.035); c.beginPath(); c.arc(cx, 0, W*0.36, 2.3, 4.0); c.stroke();
      stone(cx, 0, W*0.09);
    } else {
      STAFF.pole(c, L, W, p, { end: 0.56 }); runes();
      const cx = L*0.82, r = W*0.34;
      const P = [[cx + r, 0], [cx - r*0.5, -r*0.87], [cx - r*0.5, r*0.87]];
      const tri = (g, col) => { c.strokeStyle = col; c.lineWidth = Math.max(1, W*(0.09 + g)); c.lineJoin = "round"; c.beginPath(); c.moveTo(P[0][0], P[0][1]); c.lineTo(P[1][0], P[1][1]); c.lineTo(P[2][0], P[2][1]); c.closePath(); c.stroke(); };
      tri(0.07, S._ink(p.dark, 9.7)); tri(0, S._shade(p.dark, 1.3, 0.1));
      for (const [x, y] of P) stone(x, y, W*0.07);
      glyph(cx - r*0.08, r*0.36);
    }
  },

  /* SANCTIFIED — CROZIER. Gilt wood. A: the CROOK — the pole curls over
     into a spiral, a bead of light in the curl. B: a SUNBURST on a tall
     finial. C: a HALO — an open, pierced ring standing at the tip, held by
     two prongs (the bow's monstrance grammar). */
  sanctified(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU, gilt = S._shade(p.dark, 2.0, 0.1);
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.60, body: gilt, gnarl: 0.08 });
      const cx = L*0.70, r0 = W*0.38;
      const spiral = (wd, col) => { c.strokeStyle = col; c.lineWidth = Math.max(1, wd); c.lineCap = "round"; c.beginPath();
        for (let i = 0; i <= 48; i++){ const t = i/48, a = Math.PI*0.5 - t*Math.PI*2.75, r = r0*(1 - 0.66*t); const x = cx + r0*0.08 + Math.cos(a)*r, y = -r0*0.12 + Math.sin(a)*r*0.95; if (i) c.lineTo(x, y); else c.moveTo(x, y); }
        c.stroke(); };
      spiral(W*0.20, S._ink(p.dark, 9.7)); spiral(W*0.12, gilt); spiral(W*0.035, p.steel + "AA");
      STAFF.orb(c, cx + r0*0.14, -r0*0.02, W*0.09, p);
    } else if (v === "B"){
      STAFF.pole(c, L, W, p, { end: 0.66, body: gilt, gnarl: 0.08 });
      const cx = L*0.78, r = W*0.14;
      for (const [wd, col] of [[0.09, S._ink(p.dark, 9.7)], [0.045, gilt]]){
        c.strokeStyle = col; c.lineWidth = Math.max(1, W*wd); c.lineCap = "round";
        for (let i = 0; i < 12; i++){ const a = i*TAU/12; const len = i % 3 === 0 ? 3.0 : i % 3 === 1 ? 2.2 : 2.5; c.beginPath(); c.moveTo(cx + Math.cos(a)*r*1.1, Math.sin(a)*r*1.1); c.lineTo(cx + Math.cos(a)*r*len, Math.sin(a)*r*len); c.stroke(); }
      }
      c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.arc(cx, 0, r*1.3, 0, TAU); c.fill();
      c.fillStyle = gilt; c.beginPath(); c.arc(cx, 0, r*1.05, 0, TAU); c.fill();
      STAFF.orb(c, cx, 0, r*0.7, p);
    } else {
      STAFF.pole(c, L, W, p, { end: 0.56, body: gilt, gnarl: 0.08 });
      const cx = L*0.80, r = W*0.36;
      STAFF.claw(c, L*0.52, cx, r, 2, W, p, gilt);
      c.strokeStyle = S._ink(p.dark, 9.7); c.lineWidth = Math.max(1, W*0.14); c.beginPath(); c.arc(cx, 0, r, 0, TAU); c.stroke();
      c.strokeStyle = gilt; c.lineWidth = Math.max(1, W*0.075); c.beginPath(); c.arc(cx, 0, r, 0, TAU); c.stroke();
      c.save(); c.globalCompositeOperation = "destination-out";
      for (let i = 0; i < 8; i++){ const a = i*TAU/8 + 0.4; c.beginPath(); c.arc(cx + Math.cos(a)*r, Math.sin(a)*r, W*0.03, 0, TAU); c.fill(); }
      c.restore();
      c.strokeStyle = p.core + "AA"; c.lineWidth = Math.max(1, W*0.035);
      for (let i = 0; i < 8; i++){ const a = i*TAU/8 + 0.4 + Math.PI/8; c.beginPath(); c.moveTo(cx + Math.cos(a)*r*0.45, Math.sin(a)*r*0.45); c.lineTo(cx + Math.cos(a)*r*0.84, Math.sin(a)*r*0.84); c.stroke(); }
      STAFF.orb(c, cx, 0, W*0.10, p);
    }
  },

  /* DWARVEN — CULVERIN. Iron on wood: the head is a gun. A: a BELL muzzle
     flaring off a banded barrel, an ember in the bore. B: a MORTAR — a
     short fat tube strapped to the pole, the bore facing +x. C: a
     HAMMER-BORE — the school's square iron head with the bore drilled
     through it, the maker's chevron on the cheek. */
  dwarven(c, L, W, p, v){
    const S = SHAPES, TAU = STAFF.TAU, iron = S._shade(p.steel, 0.6, 0.2);
    const bore = (x, ry) => { c.fillStyle = S._ink(p.dark, 9.7); c.beginPath(); c.ellipse(x, 0, ry*0.36, ry*1.12, 0, 0, TAU); c.fill();
      c.fillStyle = S._ink(p.dark, 3); c.beginPath(); c.ellipse(x, 0, ry*0.30, ry, 0, 0, TAU); c.fill();
      const g = c.createRadialGradient(x, 0, 0, x, 0, ry*0.6); g.addColorStop(0, p.glow); g.addColorStop(0.5, p.core); g.addColorStop(1, p.core + "00"); c.fillStyle = g; c.beginPath(); c.ellipse(x, 0, ry*0.24, ry*0.6, 0, 0, TAU); c.fill(); };
    const bands = (xs, h) => { for (const x of xs){ c.fillStyle = S._ink(p.dark, 9.7); c.fillRect(x - W*0.045, -h - 1, W*0.09, 2*h + 2); c.fillStyle = iron; c.fillRect(x - W*0.03, -h, W*0.06, 2*h); c.fillStyle = p.core + "66"; c.fillRect(x - W*0.03, -h, W*0.06, h*0.3); } };
    if (v === "A"){
      STAFF.pole(c, L, W, p, { end: 0.50, hw: 0.13, gnarl: 0.08 });
      const barrel = (g, col) => { c.fillStyle = col; c.beginPath();
        c.moveTo(L*0.46, -W*0.14 - g); c.lineTo(L*0.80, -W*0.15 - g); c.quadraticCurveTo(L*0.92, -W*0.16 - g, L*1.00 + g, -W*0.40 - g);
        c.lineTo(L*1.00 + g, W*0.40 + g); c.quadraticCurveTo(L*0.92, W*0.16 + g, L*0.80, W*0.15 + g); c.lineTo(L*0.46, W*0.14 + g); c.closePath(); c.fill(); };
      barrel(W*0.05, S._ink(p.dark, 9.7)); barrel(0, S._ink(p.dark, 20));
      c.strokeStyle = iron; c.lineWidth = Math.max(1, W*0.035); c.beginPath(); c.moveTo(L*0.48, -W*0.11); c.lineTo(L*0.80, -W*0.12); c.quadraticCurveTo(L*0.92, -W*0.13, L*0.98, -W*0.36); c.stroke();
      bands([L*0.52, L*0.68], W*0.17);
      bore(L*0.99, W*0.36);
    } else if (v === "B"){
      STAFF.pole(c, L, W, p, { end: 0.60, hw: 0.13, gnarl: 0.08 });
      const x0 = L*0.44, x1 = L*1.00, h = W*0.36;
      c.fillStyle = S._ink(p.dark, 9.7); c.fillRect(x0 - W*0.05, -h - W*0.05, x1 - x0 + W*0.10, 2*h + W*0.10);
      c.fillStyle = S._ink(p.dark, 20); c.fillRect(x0, -h, x1 - x0, 2*h);
      c.fillStyle = iron; c.fillRect(x0, -h, x1 - x0, W*0.05);
      bands([x0 + W*0.12, x0 + (x1 - x0)*0.5, x1 - W*0.12], h);
      bore(L*0.98, h*0.82);
    } else {
      STAFF.pole(c, L, W, p, { end: 0.60, hw: 0.13, gnarl: 0.08 });
      const x0 = L*0.56, x1 = L*1.00, h = W*0.42;
      const head = (g, col) => { c.fillStyle = col; c.beginPath();
        c.moveTo(x0 - g, -h*0.5 - g); c.lineTo(x0 + (x1 - x0)*0.22, -h - g); c.lineTo(x1 + g, -h - g); c.lineTo(x1 + g, h + g); c.lineTo(x0 + (x1 - x0)*0.22, h + g); c.lineTo(x0 - g, h*0.5 + g); c.closePath(); c.fill(); };
      head(W*0.05, S._ink(p.dark, 9.7)); head(0, S._ink(p.dark, 20));
      c.strokeStyle = iron; c.lineWidth = Math.max(1, W*0.035); c.beginPath(); c.moveTo(x0 + (x1 - x0)*0.26, -h*0.84); c.lineTo(x1 - W*0.04, -h*0.84); c.stroke();
      c.strokeStyle = p.core + "99"; c.lineWidth = Math.max(1, W*0.04); c.lineJoin = "round";
      c.beginPath(); c.moveTo(x0 + (x1 - x0)*0.40, -h*0.45); c.lineTo(x0 + (x1 - x0)*0.60, 0); c.lineTo(x0 + (x1 - x0)*0.40, h*0.45); c.stroke();
      bands([x0 - W*0.05], W*0.20);
      bore(L*0.98, h*0.66);
    }
  },

  /* the dispatcher: `SHAPES.staff` */
  staff(c, L, W, p, k){
    /* W at 1.3x: Rick's references (06-docs/v89/ref-staff-1..6) all carry a
       head four to five pole-widths across on a THIN pole. The pole's own
       half-width is 0.09 of this W (~7.7 px on the bow's artW), the heads
       span up to 0.4 W either side of it. */
    /* L at 1.7x: the staff is LONG -- that is what separates it from the
       wand (short, no head to speak of) and the sceptre (short, a heavy
       ornate head held close) that may follow it as types. Its head sits at
       1.4-1.7 sim reaches from the ball's edge. Open decision: whether the
       type's sim reach should grow to match (art doc, open item 2). */
    const v = STAFF.pick[p.key] || "A", Wq = W * 1.3, Lq = L * 1.7;
    const fn = STAFF[p.key];
    if (fn) return fn(c, Lq, Wq, p, v);
    STAFF.pole(c, Lq, Wq, p, {});
  },
};
