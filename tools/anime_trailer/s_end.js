/* ANIME TRAILER — the montage, the rematch, the crown. Beats 66-102. */
"use strict";

/* ============================================================ MONTAGE 66-74
   Eight more ultimates, one beat each — each drawn as the shipped verb. */
{
  const star = (c, x, y, r, rot, col) => {
    c.save(); c.translate(x, y); c.rotate(rot); c.beginPath();
    for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r; c.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); }
    c.closePath(); c.fillStyle = INK; c.lineWidth = r * 0.3; c.strokeStyle = INK; c.lineJoin = "round"; c.stroke(); c.fillStyle = col; c.fill(); c.restore();
  };
  const STA = -1.2;
  const foe = (c, x, y, sc, t, o = {}) => drawOrb(c, x, y, o.r || 80, sc, { t, fill: 0.45, glow: 0.3 });
  const SHOTS = [
    ["CORONA", "STARWARDEN", "vigil", "twinblade", (c, a, t, P) => {
      c.save(); c.translate(540, 860); c.rotate(-0.45);
      c.lineWidth = 34; c.strokeStyle = INK; c.beginPath(); c.ellipse(0, 0, 360, 95, 0, 0.35, TAU - 0.35); c.stroke();
      c.lineWidth = 18; c.strokeStyle = P.core; c.stroke(); c.lineWidth = 6; c.strokeStyle = "#fff"; c.stroke();
      glow(c, 0, 0, 420, P.core, 0.5);
      c.restore();
      const gx = 540 + Math.cos(-0.45) * 360, gy = 860 + Math.sin(-0.45) * 360;
      if (a < 0.16) star(c, gx, gy, 70 + 20 * Math.sin(a * 60), a * 4, "#FFF3B0");
      else for (let i = 0; i < 14; i++) { const q = i / 14 * TAU, d = 700 * (1 - Math.exp(-(a - 0.16) * 6)); star(c, gx + Math.cos(q) * d, gy + Math.sin(q) * d * 0.9, 26, q + a * 8, i % 2 ? "#FFF3B0" : P.glow); }
      if (a > 0.16) celBurst(c, gx, gy, 200, a - 0.16, 0.25, ["#ffffff", "#FFF3B0", P.core, P.dark], 3);
    }],
    ["CRUCIBLE", "GRUDGEBEARER", "dwarven", "warhammer", (c, a, t, P) => {
      const u = E.inExpo(clamp(a / 0.3)), fx = lerp(1000, 760, u), fy = lerp(420, 700, u);
      for (let k = 0; k < 4; k++) { const ph = (a * 3 + k / 4) % 1; c.strokeStyle = hexA(P.glow, 1 - ph); c.lineWidth = 10; c.beginPath(); c.arc(540, 860, 520 * (1 - ph) + 120, 0, TAU); c.stroke(); }
      smear(c, 1200, 250, fx, fy, 80, PAL.runic.core, 0.7);
      foe(c, fx, fy, "runic", t);
      if (a > 0.3) { celBurst(c, 700, 760, 260, a - 0.3, 0.2, ["#ffffff", "#FFD27A", "#FF7A1A", "#2a1606"], 9); sparks(c, 700, 760, a - 0.3, 10, 40, 1800, "#FFD27A", { life: 0.3 }); }
    }],
    ["RADIANCE", "CROZIER", "sanctified", "staff", (c, a, t, P) => {
      const hx = 540 + Math.cos(STA) * 150 * 5.05, hy = 860 + Math.sin(STA) * 150 * 5.05;
      const d = 2400 * a, w = lerp(16, 90, clamp(a / 0.3));
      c.save(); c.translate(hx, hy); c.rotate(2.9);
      glow(c, d * 0.5, 0, d * 0.6 + 100, "#FFD66B", 0.6);
      for (const [k, col] of [[1.15, INK], [1, "#FFD66B"], [0.55, "#FFF6E2"], [0.25, "#ffffff"]]) { c.beginPath(); c.moveTo(0, 0); c.lineTo(d - w * 2, -w * k); c.lineTo(d + w * 1.5, 0); c.lineTo(d - w * 2, w * k); c.closePath(); c.fillStyle = col; c.fill(); }
      c.restore();
    }],
    ["GYRE", "BLOODWICK", "bloodsworn", "staff", (c, a, t, P) => {
      const lunge = clamp((a - 0.22) / 0.18);
      for (let i = 0; i < 6; i++) {
        const q = i / 6 * TAU + a * 9, ox = 540 + Math.cos(q) * 230, oy = 860 + Math.sin(q) * 230;
        const x = lerp(ox, 980, E.inCubic(lunge)), y = lerp(oy, 250, E.inCubic(lunge));
        if (lunge > 0) smear(c, ox, oy, x, y, 40, P.core, 0.6);
        glow(c, x, y, 110, P.core, 0.8);
        c.beginPath(); c.arc(x, y, 44, 0, TAU); c.fillStyle = INK; c.fill(); c.beginPath(); c.arc(x, y, 37, 0, TAU); c.fillStyle = P.core; c.fill();
        c.fillStyle = "#fff"; c.beginPath(); c.arc(x - 12, y - 14, 9, 0, TAU); c.fill();
      }
    }],
    ["CONVERGENCE", "CIPHER", "runic", "staff", (c, a, t, P) => {
      foe(c, 280, 360, "sanctified", t, { r: 70 });
      [[60, 600], [1020, 1300], [60, 1500], [1020, 700], [400, 120], [700, 1700]].forEach(([sx, sy], i) => {
        const u = E.inCubic(clamp((a - i * 0.025) / 0.35)), x = lerp(sx, 280, u), y = lerp(sy, 360, u);
        smear(c, sx, sy, x, y, 34, P.core, 0.5);
        c.save(); c.translate(x, y); c.rotate(a * 5 + i); glow(c, 0, 0, 120, P.core, 0.9);
        c.scale(1.6, 1.6); c.strokeStyle = INK; c.lineWidth = 16; c.beginPath(); c.arc(0, 0, 44, 0, TAU); c.stroke();
        c.strokeStyle = P.glow; c.lineWidth = 7; c.stroke();
        c.beginPath(); for (let k = 0; k < 6; k++) { const q = k * TAU / 6; c.lineTo(Math.cos(q) * 30, Math.sin(q) * 30); } c.closePath(); c.stroke();
        c.beginPath(); c.moveTo(-20, 0); c.lineTo(20, 0); c.moveTo(0, -22); c.lineTo(0, 22); c.stroke();
        c.restore();
      });
      if (a > 0.35) celBurst(c, 280, 360, 240, a - 0.35, 0.2, ["#ffffff", P.glow, P.core, P.dark], 5);
    }],
    ["BLOOM", "BRIARWAND", "verdant", "staff", (c, a, t, P) => {
      const cx = 300 + 150 * a, cy = 430;
      foe(c, cx + 30, cy + 20, "vigil", t, { r: 70 });
      for (let i = 0; i < 22; i++) { const q = h2(i, 1) * TAU, d = 240 * Math.sqrt(h2(i, 2)) * (0.6 + 0.4 * clamp(a / 0.2)); c.fillStyle = hexA(i % 3 ? P.core : "#E8F57A", 0.35); c.beginPath(); c.arc(cx + Math.cos(q) * d, cy + Math.sin(q) * d * 0.7, 70 + 40 * h2(i, 3), 0, TAU); c.fill(); }
      for (let i = 0; i < 60; i++) { const q = h2(i, 4) * TAU + a * 2, d = 280 * Math.sqrt(h2(i, 5)); c.fillStyle = i % 2 ? "#F8FF9A" : "#ffffff"; c.beginPath(); c.arc(cx + Math.cos(q) * d, cy + Math.sin(q) * d * 0.7 - a * 60 * h2(i, 6), 5, 0, TAU); c.fill(); }
    }],
    ["BACKLASH", "NIGHTGLASS", "umbral", "staff", (c, a, t, P) => {
      c.save(); c.globalAlpha = 0.75; c.beginPath(); c.arc(540, 860, 300, 0, TAU); c.fillStyle = "#07020d"; c.fill(); c.restore();
      c.lineWidth = 16; c.strokeStyle = P.core; c.beginPath(); c.arc(540, 860, 300, 0, TAU); c.stroke(); glow(c, 540, 860, 380, P.core, 0.5);
      const hit = 0.12, u = a < hit ? a / hit : 0, back = a > hit ? a - hit : -1;
      if (a < hit) smear(c, 1100, 300, lerp(1100, 750, u), lerp(300, 620, u), 60, PAL.bloodsworn.core, 0.9);
      if (back >= 0) {
        celBurst(c, 750, 620, 200, back, 0.2, ["#ffffff", P.glow, P.core, P.dark], 7);
        const bx = lerp(750, 1150, E.outCubic(clamp(back / 0.25))), by = lerp(620, 250, E.outCubic(clamp(back / 0.25)));
        smear(c, 750, 620, bx, by, 50, P.core, 0.8);
        c.save(); c.translate(bx, by); c.rotate(-0.75); c.beginPath(); c.moveTo(60, 0); c.lineTo(-40, -24); c.lineTo(-20, 0); c.lineTo(-40, 24); c.closePath(); c.fillStyle = P.glow; c.fill(); c.strokeStyle = INK; c.lineWidth = 6; c.stroke(); c.restore();
      }
    }],
    ["BEACON", "WATCHLIGHT", "vigil", "staff", (c, a, t, P) => {
      const lx = 330, ly = 1060;
      glow(c, lx, ly - 40, 260, "#FFE9A8", 0.9);
      c.fillStyle = INK; c.fillRect(lx - 48, ly - 110, 96, 130); c.fillStyle = "#FFE9A8"; c.fillRect(lx - 36, ly - 98, 72, 106);
      c.fillStyle = INK; c.beginPath(); c.moveTo(lx - 60, ly - 110); c.lineTo(lx, ly - 160); c.lineTo(lx + 60, ly - 110); c.fill();
      [0.02, 0.2].forEach((b, i) => {
        const u = clamp((a - b) / 0.2); if (u <= 0) return;
        const x = lerp(lx, 900, u), y = lerp(ly - 50, 300, u);
        smear(c, lx, ly - 50, x, y, 26, P.glow, 0.8 * (1 - u * 0.5)); glow(c, x, y, 120, "#ffffff", 0.9);
        if (u >= 1) celBurst(c, 900, 300, 180, a - b - 0.2, 0.18, ["#ffffff", P.glow, P.core, P.dark], 11 + i);
      });
      foe(c, 920, 290, "dwarven", t, { r: 70 });
    }],
  ];
  function shot(c, k, age, lt) {
    const [ult, relic, sc, wpn, fx] = SHOTS[k], P = PAL[sc];
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = mix(P.dark, "#000", 0.3); c.fillRect(0, 0, W, H);
    speedLines(c, k % 2 ? 2.6 : -0.5, 80, P.core, 50 + k, 0.5, lt, 5000);
    halftone(c, k % 2 ? 150 : 930, k % 2 ? 1700 : 250, 700, hexA(P.core, 1), 26, 0.3);
    const z = 1 + 0.08 * age / BEAT;
    c.translate(540, 860); c.scale(z, z); c.translate(-540, -860);
    drawRelic(c, 540, 860, 150, sc, wpn, wpn === "staff" ? STA : -0.8, { t: lt, fill: 0.6, aura: 0.6, w: { t: lt } });
    fx(c, age, lt, P);
    c.restore();
    slam(c, ult, W / 2, 1330, 170, age - 0.02, { fill: P.glow, outer: INK, inner: "#fff", maxW: 960, letter: 3 });
    slam(c, relic, W / 2, 1450, 50, age - 0.05, { skew: 0, fill: "#fff", ow: 0.3, iw: 0, letter: 10, from: 1.4 });
  }
  scene(66, 74, "montage", (c, lt, lb, t) => {
    const k = Math.min(7, Math.floor(lb + 1e-6)), age = (lb - k) * BEAT;
    const u = E.outCubic(clamp(age / 0.1));
    if (k > 0 && u < 1) shot(c, k - 1, BEAT, lt);
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
    const edge = lerp(-600, W + 600, u), up = k % 2;
    c.beginPath();
    if (up) { c.moveTo(-100, H + 600); c.lineTo(W + 100, H + 600); c.lineTo(W + 100, lerp(H + 600, -800, u) - 200); c.lineTo(-100, lerp(H + 600, -800, u) + 200); }
    else { c.moveTo(-600, -100); c.lineTo(edge + 300, -100); c.lineTo(edge - 300, H + 100); c.lineTo(-600, H + 100); }
    c.closePath(); c.clip();
    shot(c, k, age, lt);
    c.restore();
    if (age < 0.05) flash(c, "#ffffff", 0.6 * (1 - age / 0.05));
  });
  for (let k = 0; k < 8; k++) cue(66 + k, "montage_hit", { k });
}

/* ============================================================ THE REMATCH 74-86
   Back to the two from the open. Versus card; the line a first-time viewer
   needs (the liquid in the glass IS the life); the charge; one beat of
   silence; the clash. */
{
  const TS = "verdant", DR = "umbral";
  const DIV = [[0, 1180], [W, 740]];
  const divY = x => lerp(DIV[0][1], DIV[1][1], x / W);
  function half(c, sc, top, lt, seed) {
    const P = PAL[sc];
    c.save(); c.beginPath();
    if (top) { c.moveTo(0, 0); c.lineTo(W, 0); c.lineTo(W, DIV[1][1]); c.lineTo(0, DIV[0][1]); }
    else { c.moveTo(0, DIV[0][1]); c.lineTo(W, DIV[1][1]); c.lineTo(W, H); c.lineTo(0, H); }
    c.closePath(); c.clip();
    const g = c.createLinearGradient(0, top ? 0 : H, 0, top ? 1000 : 900); g.addColorStop(0, mix(P.core, "#000", 0.25)); g.addColorStop(1, mix(P.dark, "#000", 0.3));
    c.fillStyle = g; c.fillRect(0, 0, W, H);
    halftone(c, top ? 900 : 180, top ? 200 : 1700, 800, hexA(P.dark, 1), 26, 0.55);
    focusLines(c, top ? 360 : 720, top ? 520 : 1400, 100, 330, P.glow, seed + Math.floor(lt * 12), 0.45);
    c.restore();
  }
  scene(74, 86, "the rematch", (c, lt, lb, t) => {
    c.setTransform(1, 0, 0, 1, 0, 0);
    // ----------------------------------------- 0-4: versus
    if (lb < 4) {
      const e = E.outExpo(clamp(lb / 0.3));
      half(c, TS, true, lt, 90); half(c, DR, false, lt, 91);
      drawRelic(c, 360 - 700 * (1 - e), 520, 230, TS, "twinblade", -0.55, { t: lt, fill: 0.72, aura: 0.7, slosh: 1.5, w: { t: lt, glint: clamp(1 - Math.abs(lb - 0.5) / 0.2) } });
      drawRelic(c, 720 + 700 * (1 - e), 1400, 230, DR, "scythe", Math.PI + 0.9, { t: lt + 1, fill: 0.72, aura: 0.7, slosh: 1.5, w: { t: lt, moon: 1 } });
      c.save(); c.lineWidth = 40; c.strokeStyle = INK; c.beginPath(); c.moveTo(DIV[0][0], DIV[0][1]); c.lineTo(DIV[1][0], DIV[1][1]); c.stroke();
      c.lineWidth = 16; c.strokeStyle = "#fff"; c.stroke(); c.restore();
      slam(c, "THORNSHEAR", 745, 650, 84, ageB(lb, 0.2), { fill: PAL[TS].glow, maxW: 560 });
      slam(c, "DUSKREAVE", 335, 1290, 84, ageB(lb, 0.3), { fill: PAL[DR].glow, maxW: 560 });
      slam(c, "VS", W / 2, 960, 280, ageB(lb, 0.5), { out: 0.5, grad: ["#ffffff", GOLD_L, GOLD], shake: 5 });
      slam(c, "TO THE LAST DROP.", W / 2 - 30, 960, 118, ageB(lb, 2.0), { out: 0.7, fill: "#ffffff", maxW: 900, shake: 2 });
      if (lb < 0.1) flash(c, "#fff", 1 - lb / 0.1);
      return;
    }
    // ----------------------------------------- 4-7: the charge
    if (lb < 7) {
      const k = Math.floor(lb - 4), age = (lb - 4 - k) * BEAT;
      if (k < 2) {
        const sc = k === 0 ? TS : DR, P = PAL[sc], ang = k === 0 ? 0 : Math.PI;
        c.fillStyle = mix(P.dark, "#000", 0.2); c.fillRect(0, 0, W, H);
        speedLines(c, ang, 140, P.core, 60 + k, 0.8, lt, 9000);
        speedLines(c, ang, 40, "#ffffff", 70 + k, 0.6, lt, 12000);
        const x = 540 + (k ? 1 : -1) * 40 * Math.sin(age * 30), y = 900;
        smear(c, x + (k ? 1 : -1) * 900, y, x, y, 190, P.core, 0.7);
        drawRelic(c, x, y, 200, sc, k === 0 ? "twinblade" : "scythe", k === 0 ? -0.25 : Math.PI + 0.25, { t: lt, fill: 0.72, aura: 1, squash: 0.12, sqAng: 0, w: { t: lt, moon: 1 } });
      } else {
        const u = lb - 6;
        c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
        c.save(); c.beginPath(); c.rect(0, 0, W, H / 2 - 12); c.clip(); c.fillStyle = mix(PAL[TS].dark, "#000", 0.2); c.fillRect(0, 0, W, H); speedLines(c, 0, 100, PAL[TS].core, 80, 0.8, lt, 9000);
        drawRelic(c, lerp(-100, 380, u), 560, 190, TS, "twinblade", -0.2, { t: lt, fill: 0.72, aura: 1, w: { t: lt } }); c.restore();
        c.save(); c.beginPath(); c.rect(0, H / 2 + 12, W, H / 2); c.clip(); c.fillStyle = mix(PAL[DR].dark, "#000", 0.2); c.fillRect(0, 0, W, H); speedLines(c, Math.PI, 100, PAL[DR].core, 81, 0.8, lt, 9000);
        drawRelic(c, lerp(1180, 700, u), 1360, 190, DR, "scythe", Math.PI + 0.2, { t: lt, fill: 0.72, aura: 1, w: { t: lt, moon: 1 } }); c.restore();
        c.fillStyle = "#fff"; c.fillRect(0, H / 2 - 12, W, 24);
      }
      if (age < 0.06) flash(c, "#fff", 0.7);
      return;
    }
    // ----------------------------------------- 7-7.5: silence
    const CL = 7.5;
    if (lb < CL) {
      c.fillStyle = "#101010"; c.fillRect(0, 0, W, H);
      c.save(); c.filter = "grayscale(1) contrast(1.3)";
      drawRelic(c, 360, 1010, 200, TS, "twinblade", -0.35, { t: 0, fill: 0.72, aura: 0.6, w: { t: 0 } });
      drawRelic(c, 720, 910, 200, DR, "scythe", Math.PI - 0.35, { t: 0, fill: 0.72, aura: 0.6, w: { t: 0, moon: 1 } });
      c.restore();
      c.fillStyle = "#fff"; c.fillRect(535, 700, 10, 520);
      vignette(c, 0.9);
      return;
    }
    // ----------------------------------------- 7.5-12: the clash, and the white
    const ca = ageB(lb, CL);
    const cam = { x: 540, y: 960, z: 1 + 0.15 * clamp(ca), rot: 0.05, t: lt, shake: 120 * Math.exp(-ca * 1.8) };
    c.save(); camera(c, cam);
    c.fillStyle = "#05030a"; c.fillRect(-1000, -1000, W + 2000, H + 2000);
    focusLines(c, 540, 960, 200, 260, "#ffffff", 100 + Math.floor(lt * 12), 0.8);
    const R1 = 1500 * E.outExpo(ca / 2.2);
    for (let i = 0; i < 2; i++) {                     // the two schools, torn around each other
      const P = PAL[i ? DR : TS];
      c.save(); c.translate(540, 960); c.rotate(ca * (i ? -2 : 2) + i * Math.PI);
      c.beginPath(); c.moveTo(0, 0); for (let k = 0; k <= 30; k++) { const q = k / 30 * Math.PI, rr = R1 * (0.6 + 0.4 * h2(k, i + Math.floor(ca * 12))); c.lineTo(Math.cos(q) * rr, Math.sin(q) * rr); } c.closePath();
      c.fillStyle = P.core; c.fill(); c.restore();
    }
    celBurst(c, 540, 960, 760, ca, 2.4, ["#ffffff", "#ffffff", "#ffffff", "#ffffff"], 900);
    sparks(c, 540, 960, ca, 901, 160, 3600, "#ffffff", { life: 1.4, w: 12 });
    sparks(c, 540, 960, ca, 902, 80, 3000, PAL[TS].glow, { life: 1.2, w: 10 });
    sparks(c, 540, 960, ca, 903, 80, 3000, PAL[DR].glow, { life: 1.2, w: 10 });
    for (let k = 0; k < 3; k++) { const a = ca - k * 0.18; shockRing(c, 540, 960, 2000 * E.outExpo(a / 1.2), 80 * (1 - a / 1.2), "#ffffff", 1 - a / 1.2); }
    drawOrb(c, 540 - 130 * Math.exp(-ca * 3) - 40, 960, 150 * Math.exp(-ca * 1.5), TS, { t: lt, fill: 0.7, aura: 1 });
    drawOrb(c, 540 + 130 * Math.exp(-ca * 3) + 40, 960, 150 * Math.exp(-ca * 1.5), DR, { t: lt, fill: 0.7, aura: 1 });
    c.restore();
    const im = impactMode(lb, CL, ["i", "n", "R", "i", "g", "p", "i", "n", "i", "w"]);
    if (im) applyImpact(c, im);
    if (lb > CL + 0.1 && lb < CL + 2.5) screenCrack(c, 560, 930, 1300, 17, clamp((lb - CL - 0.1) / 0.3));
    flash(c, "#ffffff", E.inCubic(clamp((lb - 9.0) / 2.0)));
  });
  cue(74, "hit_big"); cue(74.5, "vs_slam"); cue(76, "slam_text");
  cue(78, "dash"); cue(79, "dash"); cue(80, "dash");
  cue(78, "riser", { dur: 3 * BEAT });
  cue(81, "silence", { dur: 0.5 * BEAT });
  cue(81.5, "clash_final");
  cue(81.6, "glass_crack");
  cue(83, "white_swell", { dur: 3 * BEAT });
}

/* ============================================================ THE CROWN 86-102 */
{
  const CX = 540, CY = 720, S = 250;
  const lockB = k => 1.0 + k * 0.28;
  scene(86, 102, "title", (c, lt, lb, t) => {
    c.setTransform(1, 0, 0, 1, 0, 0);
    const bg = c.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, "#1c1006"); bg.addColorStop(0.55, "#08050c"); bg.addColorStop(1, "#000");
    c.fillStyle = bg; c.fillRect(0, 0, W, H);
    const whole = lb >= 3.5, wa = ageB(lb, 3.5);
    godRays(c, CX, -300, GOLD, lt, whole ? 0.36 : 0.12, 11);
    glow(c, CX, CY, 1000, GOLD, whole ? 0.32 : 0.12);
    for (let i = 0; i < 90; i++) {                      // embers rising
      const x = (h2(i, 11) * W + 30 * Math.sin(lt + i)) % W, y = H - ((h2(i, 12) * H + lt * (60 + 90 * h2(i, 13))) % (H + 100));
      c.fillStyle = hexA(i % 7 === 0 ? PAL[CROWN_GEMS[i % 7]].core : GOLD_L, 0.25 + 0.5 * h2(i, 14));
      c.beginPath(); c.arc(x, y, 1.5 + 3 * h2(i, 15), 0, TAU); c.fill();
    }
    const cam = { x: 540, y: 960, z: 1 + 0.03 * Math.sin(lt * 0.6), t: lt, shake: wa > 0 ? 40 * Math.exp(-wa * 4) : 0 };
    c.save(); camera(c, cam);
    const bob = 8 * Math.sin(lt * 1.4);
    if (!whole) {
      for (let k = 0; k < 7; k++) {                    // the seven come home
        const P = PAL[CROWN_GEMS[k]], a = ageB(lb, lockB(k)), u = a >= 0 ? 1 : E.inCubic(clamp(1 + a / (1.4 * BEAT)));
        const ang = -Math.PI / 2 + (k - 3) * 0.55 + Math.PI;
        const d = 1600 * (1 - u);
        const px = CX + Math.cos(ang) * d, py = CY + Math.sin(ang) * d;
        if (u < 1 && u > 0) smear(c, CX + Math.cos(ang) * (d + 700), CY + Math.sin(ang) * (d + 700), px, py, 50, P.core, 0.7);
        if (u <= 0) continue;
        glow(c, px, py, 220, P.core, a >= 0 ? 0.5 * Math.exp(-a * 3) + 0.2 : 0.7);
        c.save(); c.translate(px - CX, py - CY + bob);
        drawCrown(c, CX, CY, S, 0, { clip: shardClip(k), flat: true, gemGlow: 0.6 });
        if (a < 0.3) { c.translate(CX, CY); c.scale(S, S); shardClip(k)(c); crownPath(c); c.globalCompositeOperation = "source-atop"; c.fillStyle = hexA(P.core, a < 0 ? 0.6 : 0.6 * (1 - a / 0.3)); c.fill(); }
        c.restore();
        if (a >= 0 && a < 0.25) sparks(c, px, py, a, 950 + k, 20, 1200, P.glow, { life: 0.3 });
      }
    } else {
      drawCrown(c, CX, CY + bob, S, lt * 0.4, { gemGlow: 0.6 + 0.3 * Math.sin(lt * 3) });
      shockRing(c, CX, CY, 1600 * E.outExpo(wa / 0.9), 60 * (1 - wa / 0.9), GOLD_L, 1 - wa / 0.9);
      sparks(c, CX, CY, wa, 960, 90, 2400, GOLD_L, { life: 1.0, w: 8 });
      const gl = [8.0, 12.5].map(b => ageB(lb, b)).find(a => a > 0 && a < 0.35);
      if (gl !== undefined) { const s = 90 * Math.sin(gl / 0.35 * Math.PI); c.fillStyle = "#fff"; c.save(); c.translate(CX + 120, CY - 150 + bob); c.beginPath(); c.moveTo(0, -s); c.lineTo(s * 0.12, -s * 0.12); c.lineTo(s, 0); c.lineTo(s * 0.12, s * 0.12); c.lineTo(0, s); c.lineTo(-s * 0.12, s * 0.12); c.lineTo(-s, 0); c.lineTo(-s * 0.12, -s * 0.12); c.closePath(); c.fill(); glow(c, 0, 0, s * 1.5, "#fff", 0.8); c.restore(); }
    }
    c.restore();
    if (wa > 0 && wa < 0.35) flash(c, "#fff", 0.9 * (1 - wa / 0.35));
    if (lb < 1) flash(c, "#fff", 1 - E.outCubic(lb));
    slam(c, "SUPER WEAPON BALL", W / 2, 1040, 58, ageB(lb, 4.0), { skew: 0, fill: GOLD_L, ow: 0.3, iw: 0, letter: 12, from: 1.6 });
    slam(c, "THE SUNDERED", W / 2 - 20, 1140, 116, ageB(lb, 4.0), { fill: "#ffffff", maxW: 820, letter: 4 });
    slam(c, "CROWN", W / 2 - 20, 1290, 215, ageB(lb, 4.25), { grad: [GOLD_L, GOLD, GOLD_D], inner: "#fff", letter: 8, shake: 2 });
    vText(c, "砕かれた王冠", 118, 470, 66, "#ffffff", clamp(ageB(lb, 5) / 0.3), { stroke: "#7a0e18" });
    slam(c, "WHO TAKES THE CROWN?", W / 2, 300, 84, ageB(lb, 8), { fill: "#ffffff", maxW: 960 });
    slam(c, "FOLLOW TO FIND OUT", W / 2, 1450, 60, ageB(lb, 10), { skew: 0, fill: GOLD_L, ow: 0.3, iw: 0, letter: 8, from: 1.5 });
  });
  for (let k = 0; k < 7; k++) cue(86 + lockB(k), "shard_lock", { k });
  cue(89.5, "crown_whole");
  cue(90, "title_slam"); cue(90.25, "title_slam");
  cue(94, "slam_text"); cue(96, "slam_soft");
  cue(94, "glint"); cue(98.5, "glint");
}
