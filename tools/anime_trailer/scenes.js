/* ANIME TRAILER — the cut list and the shared pieces.
   Time is in BEATS (144 bpm, 10 frames a beat) so the picture and the score
   are cut to the same grid. A scene draws itself from its local time only. */
"use strict";

const SCENES = [];
const CUES = [];                    // the score reads these: {t (s), kind, ...}
function scene(b0, b1, name, fn) { SCENES.push({ b0, b1, name, fn }); }
function cue(beat, kind, p = {}) { CUES.push(Object.assign({ t: +(beat * BEAT).toFixed(4), beat, kind }, p)); }
let TOTAL_BEATS = 102;

function renderAt(c, t) {
  const b = t / BEAT;
  const s = SCENES.find(s => b >= s.b0 - 1e-6 && b < s.b1 - 1e-6) || SCENES[SCENES.length - 1];
  c.save();
  s.fn(c, t - s.b0 * BEAT, b - s.b0, t);
  c.restore();
  c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = "source-over";
  vignette(c, 0.42);
  grain(c, t, 0.045);
}

/* Beat helpers for a scene: age since a beat, and whether we are in [a, b). */
const ageB = (lb, beat) => (lb - beat) * BEAT;
const inB = (lb, a, b) => lb >= a && lb < b;

/* The impact-frame pattern after a hit at beat `hb`: which ink mode, if any,
   this frame gets. Frame-exact, because the effect is two or three frames. */
function impactMode(lb, hb, pattern) {
  const f = Math.floor((lb - hb) * 10 + 1e-6);          // frames since the hit
  if (f < 0 || f >= pattern.length) return null;
  return pattern[f];
}
function applyImpact(c, mode) {
  if (!mode || mode === "-") return;
  if (mode === "i") impactFrame(c, "inv");
  else if (mode === "n") impactFrame(c, "norm");
  else if (mode === "r") impactFrame(c, "norm", "#ff2a3a");
  else if (mode === "R") impactFrame(c, "inv", "#ff2a3a");
  else if (mode === "g") impactFrame(c, "inv", "#7CFF5A");
  else if (mode === "p") impactFrame(c, "inv", "#C77DFF");
  else if (mode === "o") impactFrame(c, "norm", "#FF9A2A");
  else if (mode === "k") impactFrame(c, "inv", "#FF5FC8");
  else if (mode === "w") flash(c, "#ffffff", 1);
}

/* A callout: 奥義 over the ultimate's name, the anime special-move card. */
function callout(c, name, sc, age, y = 520, o = {}) {
  if (age < 0 || age > (o.dur || 1.6)) return;
  const P = PAL[sc];
  const out = (o.dur || 1.6) - 0.12;
  // a slash of colour behind the name
  const u = E.outExpo(Math.min(1, age / 0.12)), fade = age > out ? 1 - (age - out) / 0.12 : 1;
  c.save(); c.globalAlpha = fade;
  c.translate(W / 2, y); c.rotate(-0.06);
  c.fillStyle = INK; c.fillRect(-W * u, -92, W * 2 * u, 184);
  c.fillStyle = P.core; c.fillRect(-W * u, -78, W * 2 * u, 156);
  c.fillStyle = hexA("#ffffff", 0.35); c.fillRect(-W * u, -78, W * 2 * u, 18);
  c.restore();
  slam(c, "奥義", W / 2 - (o.jpx ?? 330), y - 128, 64, age - 0.02, { out, skew: 0, fill: P.core, ow: 0.2, iw: 0.08 });
  slam(c, name, W / 2, y + 4, o.size || 128, age - 0.03, { out, fill: "#ffffff", outer: INK, inner: P.dark, letter: 4, iw: 0.08 });
}

/* Ricochet in a box without state: unfold the straight line, fold it back.
   Returns position and how many walls it has touched — the Winnowing's kunai
   grow on every one, and so does everything that bounces here. */
function fold(u, a, b) { const L = b - a; let v = (u - a) % (2 * L); if (v < 0) v += 2 * L; const n = Math.floor((u - a) / L); return [v < L ? a + v : b - (v - L), Math.abs(n)]; }
function bounceAt(x0, y0, vx, vy, t, box, pad = 0) {
  const [x, nx] = fold(x0 + vx * t, box.x0 + pad, box.x1 - pad);
  const [y, ny] = fold(y0 + vy * t, box.y0 + pad, box.y1 - pad);
  return { x, y, n: nx + ny };
}

/* The leaf kunai — Thornshear's blades turned to leaves. */
function drawKunai(c, x, y, ang, s, sc = "verdant", heat = 0) {
  const P = PAL[sc];
  c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s);
  glow(c, 0, 0, 60, heat > 0.5 ? "#ffffff" : P.hot, 0.35 + 0.3 * heat);
  c.beginPath(); c.moveTo(34, 0); c.quadraticCurveTo(6, -15, -24, 0); c.quadraticCurveTo(6, 15, 34, 0); c.closePath();
  c.strokeStyle = INK; c.lineWidth = 7; c.stroke();
  c.fillStyle = mix(P.core, "#ffffff", heat * 0.6); c.fill();
  c.save(); c.clip(); c.fillStyle = mix(P.core, P.dark, 0.5); c.fillRect(-30, 0, 70, 20); c.restore();
  c.strokeStyle = P.glow; c.lineWidth = 2.5; c.beginPath(); c.moveTo(-22, 0); c.lineTo(30, 0); c.stroke();
  c.strokeStyle = INK; c.lineWidth = 5; c.beginPath(); c.moveTo(-24, 0); c.lineTo(-40, 0); c.stroke();
  c.restore();
}

/* The crown. Gold, inked, cel-shaded, one gem per school on its band. */
const CROWN_GEMS = ["sanctified", "bloodsworn", "dwarven", "verdant", "umbral", "runic", "vigil"];
function crownPath(c) {
  c.beginPath();
  c.moveTo(-1, 0.55); c.lineTo(-1, -0.2);
  const pts = 5;
  for (let i = 0; i < pts; i++) {
    const x0 = -1 + i * 2 / pts, xm = x0 + 1 / pts, x1 = x0 + 2 / pts;
    const hgt = i === 2 ? -1.05 : (i === 1 || i === 3 ? -0.85 : -0.7);
    c.lineTo(x0 + 0.02, -0.2); c.lineTo(xm, hgt); c.lineTo(x1 - 0.02, -0.2);
  }
  c.lineTo(1, 0.55); c.closePath();
}
function drawCrown(c, x, y, s, t, o = {}) {
  c.save(); c.translate(x, y);
  const sx = o.flat ? 1 : 0.92 + 0.08 * Math.cos(t * 1.3);
  c.scale(s * sx, s);
  if (o.clip) o.clip(c);
  c.lineJoin = "miter";
  crownPath(c); c.strokeStyle = INK; c.lineWidth = 0.075; c.stroke();
  crownPath(c); c.fillStyle = GOLD; c.fill();
  c.save(); crownPath(c); c.clip();
  c.fillStyle = GOLD_D; c.beginPath(); c.moveTo(-1.2, 0.18); c.lineTo(1.2, 0.02); c.lineTo(1.2, 0.8); c.lineTo(-1.2, 0.8); c.fill();
  c.fillStyle = mix(GOLD, GOLD_D, 0.45); c.fillRect(-1.2, -0.2, 2.4, 0.1);
  c.fillStyle = GOLD_L;                                         // the hard highlight
  for (let i = 0; i < 5; i++) { const x0 = -1 + i * 0.4 + 0.07; c.beginPath(); c.moveTo(x0, -0.22); c.lineTo(x0 + 0.13, i === 2 ? -0.95 : -0.62); c.lineTo(x0 + 0.08, -0.22); c.fill(); }
  c.fillRect(-0.95, 0.02, 1.9, 0.05);
  c.restore();
  crownPath(c); c.strokeStyle = INK; c.lineWidth = 0.03; c.stroke();
  // band gems
  CROWN_GEMS.forEach((sc, i) => {
    const gx = -0.78 + i * 0.26, gy = 0.2, P = PAL[sc];
    if (o.gemGlow) glow(c, gx, gy, 0.35, P.core, o.gemGlow);
    c.beginPath(); c.moveTo(gx, gy - 0.12); c.lineTo(gx + 0.09, gy); c.lineTo(gx, gy + 0.12); c.lineTo(gx - 0.09, gy); c.closePath();
    c.fillStyle = P.core; c.fill(); c.strokeStyle = INK; c.lineWidth = 0.025; c.stroke();
    c.fillStyle = "#fff"; c.beginPath(); c.moveTo(gx - 0.03, gy - 0.06); c.lineTo(gx, gy - 0.09); c.lineTo(gx + 0.01, gy - 0.04); c.fill();
  });
  // tip pearls
  [[-0.8, -0.7], [-0.4, -0.85], [0, -1.05], [0.4, -0.85], [0.8, -0.7]].forEach(([px, py]) => {
    c.beginPath(); c.arc(px, py - 0.05, 0.07, 0, TAU); c.fillStyle = GOLD_L; c.fill(); c.strokeStyle = INK; c.lineWidth = 0.025; c.stroke();
  });
  c.restore();
}
/* The seven shard regions: vertical strips with jagged seams, in crown units. */
function shardClip(k) {
  const seam = (j) => { const pts = []; for (let i = 0; i <= 8; i++) { const y = -1.3 + i * 2.2 / 8; const x = -1 + j * 2 / 7 + (j === 0 || j === 7 ? (j === 0 ? -0.3 : 0.3) : (h2(j, i) - 0.5) * 0.16); pts.push([x, y]); } return pts; };
  return (c) => {
    const L = seam(k), R = seam(k + 1);
    c.beginPath(); L.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]));
    for (let i = R.length - 1; i >= 0; i--) c.lineTo(R[i][0], R[i][1]);
    c.closePath(); c.clip();
  };
}
/* God rays from above — wedges of light, gently swinging. */
function godRays(c, x, y, col, t, a = 0.3, n = 9) {
  c.save(); c.globalCompositeOperation = "lighter";
  for (let i = 0; i < n; i++) {
    const ang = Math.PI / 2 + (i - (n - 1) / 2) * 0.13 + 0.03 * Math.sin(t * 0.7 + i);
    const w = 0.025 + 0.03 * h2(i, 4);
    const g = c.createLinearGradient(x, y, x + Math.cos(ang) * 2200, y + Math.sin(ang) * 2200);
    g.addColorStop(0, hexA(col, a * (0.5 + 0.5 * h2(i, 5)))); g.addColorStop(1, hexA(col, 0));
    c.fillStyle = g; c.beginPath(); c.moveTo(x, y);
    c.lineTo(x + Math.cos(ang - w) * 2200, y + Math.sin(ang - w) * 2200);
    c.lineTo(x + Math.cos(ang + w) * 2200, y + Math.sin(ang + w) * 2200); c.closePath(); c.fill();
  }
  c.restore();
}
/* Afterimages: the smear of a fast relic — ghost copies behind it. */
function afterimages(c, pts, r, sc) {
  const P = PAL[sc];
  pts.forEach(([x, y], i) => {
    const k = (i + 1) / (pts.length + 1);
    c.save(); c.globalAlpha = 0.18 + 0.4 * k;
    c.beginPath(); c.arc(x, y, r * (0.8 + 0.2 * k), 0, TAU); c.fillStyle = i % 2 ? P.glow : P.core; c.fill();
    c.restore();
  });
}
/* A smear streak: a tapered ribbon along the motion, the drawn motion blur. */
function smear(c, x0, y0, x1, y1, r, col, a = 0.8) {
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy); if (L < 1) return;
  const nx = -dy / L * r, ny = dx / L * r;
  c.save(); c.globalAlpha = a;
  const g = c.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, hexA(col, 0)); g.addColorStop(1, hexA(col, 1));
  c.fillStyle = g; c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1 + nx, y1 + ny); c.lineTo(x1 - nx, y1 - ny); c.closePath(); c.fill();
  c.restore();
}
