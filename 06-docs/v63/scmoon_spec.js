/* ------------------------------------------------------------------ UMBRAL --
   THE MOON. Rick's, 2026-09-02, from three references (`06-docs/v63/
   ref-scythe-1/2/3.jpg`) and a spread of four (`umbral-scythe-silhouette-
   v63.md`). Replaces `_scEaten`, which he rejected on sight the first time it
   was ever drawn ("this one is rough and should be redone").

   WHAT IT IS: a thin blade sweeping ~175 degrees, its tip curling back toward
   the shaft -- the blade is HALF the weapon's footprint, where `_scBase`'s
   crescent is a third. A faceted hub with a lit gem at the junction. A
   near-black jointed shaft with three segments and a hex gem at the butt.
   Near-black body, cold rim on the back, the honed edge lit twice.

   CONSTRUCTION, and why:
   * The honed edge is ONE cubic -- it carries the glow stroke, so it has to
     be a clean curve. The back edge is that cubic pushed out along its
     outward normal by a width profile w(t), so the blade's width is one
     function and cannot disagree with the edge it belongs to.
   * ONE closed path for the blade. v58's rule: a limb goes INTO the outline,
     never behind it.
   * The hub is drawn AFTER the blade and the blade's root sits inside it, so
     the join is hidden at every zoom.
   * The furthest point of the blade from the ball is 1.08 L (sim reach is
     1.00 L; the shipped crescent was 1.02 L). Printed by the lab, not judged.
   * Does not call `_scBase`, `_scCrescent` or `_scOuter`: the blade is a
     different curve, and the inverted-normal defect those carry (open item,
     `_scOuter`'s comment) is not inherited.
   * Nothing here touches the sim. `litWeapon` bakes it; no probe reads the
     path. engine_ab must come back identical.
*/
_scMoon(c, L, W, p){
  const TAU = Math.PI * 2;
  const S = SHAPES;

  /* ---- the shaft: near-black, a cold highlight line, three segments, a
          hex gem at the butt. The line is `_scBase`'s own quadratic, moved
          to meet the hub at (0.71L, 0.10W). ---- */
  const at = (u) => { const it = 1 - u;
    return { x: 2*it*u*(L*0.44) + u*u*(L*0.71), y: 2*it*u*(W*0.30) + u*u*(W*0.10),
             a: Math.atan2(2*it*(W*0.30) + 2*u*(W*0.10 - W*0.30),
                           2*it*(L*0.44) + 2*u*(L*0.71 - L*0.44)) }; };
  c.lineCap = "round";
  c.strokeStyle = S._ink(p.dark, 16); c.lineWidth = W*0.17;
  c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(L*0.44, W*0.30, L*0.71, W*0.10); c.stroke();
  c.strokeStyle = S._shade(p.steel, 0.55, 0.45); c.lineWidth = W*0.05;
  c.beginPath(); c.moveTo(L*0.05, -W*0.03); c.quadraticCurveTo(L*0.44, W*0.25, L*0.66, W*0.08); c.stroke();
  for (let i = 0; i < 3; i++){
    /* a SEGMENT of the rod, longer along the shaft than across it, so the
       shaft reads as jointed rather than beaded (ref 1) */
    const q = at(0.20 + 0.20*i);
    c.save(); c.translate(q.x, q.y); c.rotate(q.a);
    c.beginPath();
    c.moveTo(-W*0.20, 0); c.lineTo(-W*0.13, -W*0.13); c.lineTo(W*0.13, -W*0.13);
    c.lineTo( W*0.20, 0); c.lineTo( W*0.13,  W*0.13); c.lineTo(-W*0.13, W*0.13);
    c.closePath();
    c.fillStyle = S._ink(p.dark, 24); c.fill();
    c.strokeStyle = p.core + "BB"; c.lineWidth = Math.max(1, W*0.028); c.stroke();
    c.restore();
  }
  c.save(); c.rotate(at(0.02).a);                          // pommel gem
  c.beginPath();
  for (let i = 0; i < 6; i++){ const a = i*TAU/6, r = W*0.20;
    if (i === 0) c.moveTo(Math.cos(a)*r, Math.sin(a)*r); else c.lineTo(Math.cos(a)*r, Math.sin(a)*r); }
  c.closePath();
  c.fillStyle = S._ink(p.dark, 22); c.fill();
  c.strokeStyle = S._shade(p.steel, 1.0, 0.40); c.lineWidth = Math.max(1, W*0.03); c.stroke();
  c.save(); c.globalCompositeOperation = "lighter";
  { const g = c.createRadialGradient(0, 0, 0, 0, 0, W*0.30);
    g.addColorStop(0, p.glow); g.addColorStop(0.4, p.core + "AA"); g.addColorStop(1, p.core + "00");
    c.fillStyle = g; c.beginPath(); c.arc(0, 0, W*0.30, 0, TAU); c.fill(); }
  c.restore();
  c.fillStyle = p.glow; c.beginPath(); c.arc(0, 0, W*0.07, 0, TAU); c.fill();
  c.restore();

  /* ---- the blade ---- */
  const P = [[L*0.72, W*0.02], [L*1.05, -W*0.24], [L*0.99, -W*1.46], [L*0.48, -W*1.52]];
  const bez = (u) => {
    const it = 1 - u;
    const b  = (a,bq,cq,d) => it*it*it*a + 3*it*it*u*bq + 3*it*u*u*cq + u*u*u*d;
    const db = (a,bq,cq,d) => 3*it*it*(bq-a) + 6*it*u*(cq-bq) + 3*u*u*(d-cq);
    const x = b(P[0][0],P[1][0],P[2][0],P[3][0]), y = b(P[0][1],P[1][1],P[2][1],P[3][1]);
    let tx = db(P[0][0],P[1][0],P[2][0],P[3][0]), ty = db(P[0][1],P[1][1],P[2][1],P[3][1]);
    const m = Math.hypot(tx, ty) || 1; tx /= m; ty /= m;
    return { x, y, tx, ty };
  };
  /* outward = toward the control points, which sit on the convex side of a
     single-bend cubic; the sign is taken once at the midpoint */
  const M = [(P[1][0]+P[2][0])/2, (P[1][1]+P[2][1])/2], mid = bez(0.5);
  const sgn = (mid.ty*(M[0]-mid.x) - mid.tx*(M[1]-mid.y)) > 0 ? 1 : -1;
  const edge = (t) => { const q = bez(t); return { x:q.x, y:q.y, nx: sgn*q.ty, ny: -sgn*q.tx }; };
  const wAt = (t) => W*0.34 * Math.pow(1 - t, 0.62) * (t < 0.10 ? 0.75 + 2.5*t : 1);
  const N = 48;
  const blade = () => {
    c.beginPath();
    c.moveTo(P[0][0], P[0][1]);
    c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]);   // honed edge, root -> tip
    for (let i = N; i >= 0; i--){                                       // back edge, tip -> root
      const t = i / N, q = edge(t), w = wAt(t);
      c.lineTo(q.x + q.nx*w, q.y + q.ny*w);
    }
    c.closePath();
  };
  blade();
  { const g = c.createLinearGradient(P[0][0], P[0][1], P[3][0], P[3][1]);
    g.addColorStop(0, S._ink(p.dark, 30)); g.addColorStop(0.5, S._ink(p.dark, 18)); g.addColorStop(1, S._ink(p.dark, 26));
    c.fillStyle = g; c.fill(); }
  c.save(); c.shadowBlur = 0;                                  // the lit face, clipped
  { const wl = S._litN(c); c.globalAlpha = 0.55 * Math.abs(wl) + 0.25;
    blade(); c.clip();
    c.strokeStyle = S._shade(p.steel, 0.70, 0.30); c.lineWidth = Math.max(1, W*0.09);
    c.beginPath();
    for (let i = 0; i <= 40; i++){ const t = i/40, q = edge(t), w = wAt(t)*0.66;
      const x = q.x + q.nx*w, y = q.y + q.ny*w; if (i === 0) c.moveTo(x, y); else c.lineTo(x, y); }
    c.stroke(); }
  c.restore();
  c.strokeStyle = S._shade(p.steel, 1.15, 0.55); c.lineWidth = Math.max(1, W*0.035);   // cold rim
  blade(); c.stroke();
  const honed = () => { c.beginPath(); c.moveTo(P[0][0], P[0][1]);
    c.bezierCurveTo(P[1][0],P[1][1],P[2][0],P[2][1],P[3][0],P[3][1]); c.stroke(); };
  c.lineCap = "round";
  c.strokeStyle = p.core + "77"; c.lineWidth = Math.max(1, W*0.15); honed();          // wide and soft
  c.strokeStyle = p.glow;        c.lineWidth = Math.max(1, W*0.055); honed();         // tight and bright

  /* ---- the hub: a faceted plate over the blade's root, a lit gem, the
          school's mark (tarnish) on its face ---- */
  const hx = L*0.71, hy = W*0.10, r = W*0.30;
  c.save(); c.translate(hx, hy);
  c.beginPath();
  for (let i = 0; i < 6; i++){ const a = -Math.PI/2 + i*TAU/6;
    if (i === 0) c.moveTo(Math.cos(a)*r, Math.sin(a)*r); else c.lineTo(Math.cos(a)*r, Math.sin(a)*r); }
  c.closePath();
  c.fillStyle = S._ink(p.dark, 20); c.fill();
  c.strokeStyle = S._shade(p.steel, 1.05, 0.40); c.lineWidth = Math.max(1, W*0.035); c.stroke();
  c.beginPath();                                               // inner facet
  for (let i = 0; i < 6; i++){ const a = -Math.PI/2 + i*TAU/6 + Math.PI/6;
    if (i === 0) c.moveTo(Math.cos(a)*r*0.62, Math.sin(a)*r*0.62); else c.lineTo(Math.cos(a)*r*0.62, Math.sin(a)*r*0.62); }
  c.closePath();
  c.strokeStyle = p.core + "88"; c.lineWidth = Math.max(1, W*0.025); c.stroke();
  const gr = r*0.36;                                           // the gem
  c.save(); c.globalCompositeOperation = "lighter";
  { const g = c.createRadialGradient(0, 0, 0, 0, 0, gr*2.2);
    g.addColorStop(0, p.glow); g.addColorStop(0.35, p.core + "AA"); g.addColorStop(1, p.core + "00");
    c.fillStyle = g; c.beginPath(); c.arc(0, 0, gr*2.2, 0, TAU); c.fill(); }
  c.restore();
  c.fillStyle = p.glow; c.beginPath(); c.arc(0, 0, gr*0.55, 0, TAU); c.fill();
  c.restore();
  S._makerMark(c, hx + r*0.55, hy + r*0.45, W*0.10, W*0.62, p);
},
