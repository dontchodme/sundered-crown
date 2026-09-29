/* ANIME TRAILER — drawing library.
   Everything here is a pure function of its arguments (and of t). No state
   survives between frames, so any frame can be rendered alone, in any order,
   by any worker — the same property the game's SHAPES keeps. */
"use strict";

const W = 1080, H = 1920, FPS = 24, BPM = 144, BEAT = 60 / BPM;   // 10 frames a beat
const TAU = Math.PI * 2;
const INK = "#0a0610";

/* The schools, straight from the build of record (sc-nightglass-fx.html, PAL).
   `hot` is the trailer's own accent for fire/light effects, not a game value. */
const PAL = {
  sanctified: { name: "SANCTIFIED", core: "#FFF6E2", glow: "#FFFFFF", dark: "#5A4E30", steel: "#FFFFFF", hot: "#FFD66B" },
  bloodsworn: { name: "BLOODSWORN", core: "#E03A4E", glow: "#FF97A2", dark: "#450710", steel: "#EBD3D3", hot: "#FF2E4A" },
  dwarven:    { name: "DWARVEN",    core: "#9C6326", glow: "#E8A34E", dark: "#2E1B0A", steel: "#6A6E74", hot: "#FF7A1A" },
  verdant:    { name: "VERDANT",    core: "#4FD06B", glow: "#BCF7C7", dark: "#0D3A1A", steel: "#DCEBD8", hot: "#7CFF5A" },
  umbral:     { name: "UMBRAL",     core: "#A45CF0", glow: "#DDB8FF", dark: "#280A44", steel: "#B6A5C9", hot: "#C77DFF" },
  runic:      { name: "RUNIC",      core: "#4A9EFF", glow: "#BCDDFF", dark: "#08264F", steel: "#D4E4FF", hot: "#5FD0FF" },
  vigil:      { name: "VIGIL",      core: "#F06BB8", glow: "#FFD1EC", dark: "#4A0A31", steel: "#D8B9C9", hot: "#FF5FC8" },
};
const GOLD = "#FFC94A", GOLD_D = "#8A5A12", GOLD_L = "#FFF0B0";

/* ---------------------------------------------------------------- math */
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const inv = (a, b, x) => clamp((x - a) / (b - a));
const E = {
  outExpo: u => u >= 1 ? 1 : 1 - Math.pow(2, -10 * u),
  inExpo: u => u <= 0 ? 0 : Math.pow(2, 10 * u - 10),
  outCubic: u => 1 - Math.pow(1 - u, 3),
  inCubic: u => u * u * u,
  inOut: u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2,
  outBack: u => { const c = 2.2; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); },
};
function hash(n) { n = (n ^ 61) ^ (n >>> 16); n = n + (n << 3); n = n ^ (n >>> 4); n = Math.imul(n, 0x27d4eb2d); n = n ^ (n >>> 15); return (n >>> 0) / 4294967296; }
const h2 = (a, b) => hash((a * 73856093) ^ (b * 19349663));
const h3 = (a, b, c) => hash((a * 73856093) ^ (b * 19349663) ^ (c * 83492791));
function noise1(x, s = 0) { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(h2(i, s), h2(i + 1, s), u) * 2 - 1; }
/* ON TWOS. Anime holds a drawing for two frames; the characters step at 12
   drawings a second while the camera and the light run at 24. */
const twos = t => Math.floor(t * 12 + 1e-6) / 12;
const frameNo = t => Math.round(t * FPS);

function hexA(hex, a) {                  // "#RRGGBB" + alpha -> rgba()
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
}
function mix(h1, h2_, u) {
  const a = parseInt(h1.slice(1), 16), b = parseInt(h2_.slice(1), 16);
  const r = Math.round(lerp(a >> 16 & 255, b >> 16 & 255, u)), g = Math.round(lerp(a >> 8 & 255, b >> 8 & 255, u)), bl = Math.round(lerp(a & 255, b & 255, u));
  return "#" + ((1 << 24) | (r << 16) | (g << 8) | bl).toString(16).slice(1);
}

/* ---------------------------------------------------------------- glow sprites
   A radial falloff drawn once per colour and then stamped with 'lighter'.
   shadowBlur on a 1080x1920 canvas is the slow path; this is the fast one. */
const _glow = {};
function glowSprite(col) {
  if (_glow[col]) return _glow[col];
  const cv = document.createElement("canvas"); cv.width = cv.height = 256;
  const g = cv.getContext("2d"), gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, hexA(col, 1)); gr.addColorStop(0.25, hexA(col, 0.55));
  gr.addColorStop(0.6, hexA(col, 0.14)); gr.addColorStop(1, hexA(col, 0));
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  return (_glow[col] = cv);
}
function glow(c, x, y, r, col, a = 1) {
  if (a <= 0 || r <= 0) return;
  c.save(); c.globalCompositeOperation = "lighter"; c.globalAlpha = Math.min(1, a);
  c.drawImage(glowSprite(col), x - r, y - r, r * 2, r * 2); c.restore();
}

/* ---------------------------------------------------------------- camera */
function camera(c, cam) {
  const sx = (cam.shake || 0) * noise1(cam.t * 38, 11), sy = (cam.shake || 0) * noise1(cam.t * 41, 23);
  const sr = (cam.shake || 0) * 0.0009 * noise1(cam.t * 29, 5);
  c.translate(W / 2 + sx, H / 2 + sy);
  c.rotate((cam.rot || 0) + sr);
  c.scale(cam.z || 1, cam.z || 1);
  c.translate(-(cam.x ?? W / 2), -(cam.y ?? H / 2));
}

/* ---------------------------------------------------------------- the relic
   The game's orb: dark glass above, the school's liquid below with a bright
   meniscus, a hard specular top-left. Here it is inked and cel-shaded — flat
   tones, hard shadow edges — which is the whole "anime" translation of it. */
function drawOrb(c, x, y, r, sc, o = {}) {
  const P = PAL[sc];
  const fill = o.fill ?? 0.55, tilt = o.tilt || 0, t = o.t || 0;
  c.save(); c.translate(x, y);
  if (o.squash) { c.rotate(o.sqAng || 0); c.scale(1 + o.squash, 1 - o.squash * 0.75); c.rotate(-(o.sqAng || 0)); }
  if (o.aura) drawAura(c, 0, 0, r, sc, t, o.aura);
  if (o.glow !== 0) glow(c, 0, 0, r * 2.4, P.core, o.glow ?? 0.55);
  // ink body
  c.beginPath(); c.arc(0, 0, r * 1.075, 0, TAU); c.fillStyle = INK; c.fill();
  c.save(); c.beginPath(); c.arc(0, 0, r, 0, TAU); c.clip();
  // glass: two flat tones, split on a hard diagonal (cel shadow)
  c.fillStyle = mix(P.dark, "#000000", 0.35); c.fillRect(-r, -r, 2 * r, 2 * r);
  c.fillStyle = mix(P.dark, "#1a1428", 0.2);
  c.beginPath(); c.arc(-r * 0.18, -r * 0.2, r * 0.92, 0, TAU); c.fill();
  // liquid
  c.save(); c.rotate(tilt);
  const lv = r * (1 - 2 * fill), wob = r * 0.06 * Math.sin(t * 9) * (o.slosh ?? 0.5);
  c.beginPath(); c.moveTo(-r * 1.2, lv + wob);
  c.quadraticCurveTo(0, lv - wob * 1.4, r * 1.2, lv - wob);
  c.lineTo(r * 1.2, r * 1.3); c.lineTo(-r * 1.2, r * 1.3); c.closePath();
  c.fillStyle = P.core; c.fill();
  c.save(); c.clip();
  c.fillStyle = mix(P.core, P.dark, 0.45);                   // hard cel shadow on the liquid
  c.beginPath(); c.arc(r * 0.35, r * 0.25, r * 0.95, 0, TAU); c.fill();
  c.fillStyle = mix(P.core, "#ffffff", 0.35);                 // lit band
  c.beginPath(); c.ellipse(-r * 0.45, lv + r * 0.28, r * 0.35, r * 0.12, -0.2, 0, TAU); c.fill();
  // bubbles
  for (let i = 0; i < 5; i++) {
    const bx = (h2(i, 3) - 0.5) * r * 1.3, by = r * 0.9 - ((t * 0.35 + h2(i, 7)) % 1) * (r * 0.9 - lv);
    c.beginPath(); c.arc(bx, by, r * (0.03 + 0.03 * h2(i, 9)), 0, TAU); c.fillStyle = hexA(P.glow, 0.8); c.fill();
  }
  c.restore();
  c.beginPath(); c.moveTo(-r * 1.2, lv + wob); c.quadraticCurveTo(0, lv - wob * 1.4, r * 1.2, lv - wob);
  c.strokeStyle = P.glow; c.lineWidth = r * 0.075; c.stroke();              // meniscus
  c.restore();
  // rim light (left) and core shadow (right) on the glass
  c.globalCompositeOperation = "source-over";
  c.beginPath(); c.arc(0, 0, r * 0.94, Math.PI * 0.62, Math.PI * 1.18);
  c.strokeStyle = hexA(P.glow, 0.85); c.lineWidth = r * 0.07; c.stroke();
  c.fillStyle = "rgba(0,0,0,0.28)";
  c.beginPath(); c.arc(0, 0, r, -0.9, 1.9); c.arc(-r * 0.25, -r * 0.1, r * 0.98, 1.9, -0.9, true); c.fill();
  c.restore();
  // specular — hard-edged, the anime tell
  c.fillStyle = "#ffffff";
  c.beginPath(); c.ellipse(-r * 0.4, -r * 0.46, r * 0.3, r * 0.14, -0.62, 0, TAU); c.fill();
  c.beginPath(); c.arc(-r * 0.08, -r * 0.66, r * 0.07, 0, TAU); c.fill();
  c.beginPath(); c.arc(0, 0, r * 1.02, 0, TAU); c.strokeStyle = INK; c.lineWidth = r * 0.07; c.stroke();
  c.restore();
}

/* A flame aura around a relic powering up: tongues of the school's colour,
   stepped on twos so it flickers like drawn fire, not like a shader. */
function drawAura(c, x, y, r, sc, t, amt) {
  const P = PAL[sc], tq = twos(t), N = 22;
  for (let layer = 0; layer < 3; layer++) {
    const col = [P.dark, P.core, P.glow][layer], sz = [1.9, 1.62, 1.38][layer];
    c.beginPath();
    for (let i = 0; i <= N * 2; i++) {
      const a = (i / (N * 2)) * TAU, up = Math.max(0, -Math.sin(a)) * 0.9 + 0.25;
      const spike = i % 2 === 0 ? (0.55 + 0.6 * h3(i, Math.floor(tq * 12), layer)) * up : 0;
      const rr = r * (1.05 + (sz - 1.05) * amt * (0.4 + spike));
      const px = x + Math.cos(a) * rr, py = y + Math.sin(a) * rr - (i % 2 === 0 ? spike * r * 0.5 * amt : 0);
      i === 0 ? c.moveTo(px, py) : c.lineTo(px, py);
    }
    c.closePath(); c.globalAlpha = [0.85, 0.8, 0.9][layer] * Math.min(1, amt * 1.5);
    c.fillStyle = col; c.fill(); c.globalAlpha = 1;
  }
  glow(c, x, y, r * 3.2, P.core, 0.7 * amt);
}

/* ---------------------------------------------------------------- weapons
   Local frame: the relic's centre at the origin, the weapon pointing +x.
   Every piece is inked (a dark stroke under a flat fill) and cel-shaded (a
   darker lower half on a hard edge), so all seven read as the same hand. */
function inkFill(c, path, fillA, fillB, lw) {
  c.save(); path(); c.strokeStyle = INK; c.lineWidth = lw * 2.2; c.lineJoin = "round"; c.stroke();
  path(); c.fillStyle = fillA; c.fill();
  path(); c.clip(); c.fillStyle = fillB; c.fillRect(-4000, 0, 8000, 4000); c.restore();
}
function drawWeapon(c, type, sc, r, ang, o = {}) {
  const P = PAL[sc], lw = r * 0.06, t = o.t || 0;
  c.save(); c.rotate(ang);
  const steelA = mix(P.steel, "#ffffff", 0.25), steelB = mix(P.steel, P.dark, 0.55);
  const haft = (x0, x1, w) => inkFill(c, () => { c.beginPath(); c.rect(x0, -w / 2, x1 - x0, w); }, mix(P.dark, "#6b5a4a", 0.35), mix(P.dark, "#000", 0.4), lw);
  if (o.glow !== 0) glow(c, r * 2.2, 0, r * 2.2, P.core, (o.glow ?? 0.35));
  switch (type) {
    case "greatsword": {
      haft(r * 0.95, r * 1.6, r * 0.2);
      inkFill(c, () => { c.beginPath(); c.rect(r * 1.55, -r * 0.55, r * 0.2, r * 1.1); }, GOLD, GOLD_D, lw);   // guard
      inkFill(c, () => { c.beginPath(); c.moveTo(r * 1.75, -r * 0.32); c.lineTo(r * 4.6, -r * 0.26); c.lineTo(r * 5.2, 0); c.lineTo(r * 4.6, r * 0.26); c.lineTo(r * 1.75, r * 0.32); c.closePath(); }, steelA, steelB, lw);
      c.strokeStyle = hexA(P.core, 0.9); c.lineWidth = r * 0.07; c.beginPath(); c.moveTo(r * 1.9, 0); c.lineTo(r * 4.5, 0); c.stroke();
      break;
    }
    case "twinblade": {        // two slim curved blades, splayed
      for (const s of [-1, 1]) {
        c.save(); c.rotate(s * 0.16);
        haft(r * 0.95, r * 1.55, r * 0.16);
        inkFill(c, () => { c.beginPath(); c.moveTo(r * 1.5, -r * 0.13 * s); c.quadraticCurveTo(r * 2.8, -r * 0.5 * s, r * 3.9, -r * 0.05 * s); c.quadraticCurveTo(r * 2.8, r * 0.02 * s, r * 1.5, r * 0.12 * s); c.closePath(); }, steelA, steelB, lw * 0.8);
        c.restore();
      }
      break;
    }
    case "scythe": {
      haft(r * 0.9, r * 3.6, r * 0.16);
      const moon = o.moon;   // Duskreave's thin moon blade
      inkFill(c, () => {
        c.beginPath(); c.moveTo(r * 3.5, -r * 0.1);
        c.bezierCurveTo(r * 3.9, -r * 1.2, r * 2.6, -r * (moon ? 2.4 : 2.1), r * (moon ? 1.2 : 1.5), -r * (moon ? 2.0 : 2.2));
        c.bezierCurveTo(r * 2.3, -r * (moon ? 1.85 : 1.6), r * 3.3, -r * 1.1, r * 3.25, -r * 0.05); c.closePath();
      }, steelA, steelB, lw);
      c.strokeStyle = P.glow; c.lineWidth = r * 0.06;
      c.beginPath(); c.moveTo(r * 3.45, -r * 0.2); c.bezierCurveTo(r * 3.8, -r * 1.2, r * 2.6, -r * 2.05, r * 1.6, -r * 2.15); c.stroke();
      inkFill(c, () => { c.beginPath(); c.arc(r * 3.55, 0, r * 0.2, 0, TAU); }, P.core, P.dark, lw * 0.7);
      break;
    }
    case "warhammer": {
      haft(r * 0.9, r * 3.0, r * 0.18);
      const hx = r * 3.0, hw = r * 0.75, hh = r * 1.35;
      if (o.spikes) {        // Shroudmaul's lantern maul: bone spikes in the outline
        inkFill(c, () => {
          c.beginPath(); c.moveTo(hx - hw * 0.5, -hh * 0.5);
          for (let i = 0; i < 3; i++) { const x = hx - hw * 0.35 + i * hw * 0.35; c.lineTo(x - hw * 0.1, -hh * 0.5); c.lineTo(x, -hh * 0.5 - r * 0.45); c.lineTo(x + hw * 0.1, -hh * 0.5); }
          c.lineTo(hx + hw * 0.5, -hh * 0.5); c.lineTo(hx + hw * 0.5 + r * 0.55, 0); c.lineTo(hx + hw * 0.5, hh * 0.5);
          for (let i = 2; i >= 0; i--) { const x = hx - hw * 0.35 + i * hw * 0.35; c.lineTo(x + hw * 0.1, hh * 0.5); c.lineTo(x, hh * 0.5 + r * 0.45); c.lineTo(x - hw * 0.1, hh * 0.5); }
          c.lineTo(hx - hw * 0.5, hh * 0.5); c.lineTo(hx - hw * 0.5 - r * 0.3, 0); c.closePath();
        }, "#2a2433", "#0d0a12", lw);
        glow(c, hx, 0, r * 0.9, P.core, 0.9);
        c.fillStyle = P.glow; c.beginPath(); c.arc(hx, 0, r * 0.14, 0, TAU); c.fill();
      } else {
        inkFill(c, () => { c.beginPath(); c.rect(hx - hw / 2, -hh / 2, hw, hh); }, steelA, steelB, lw);
        c.fillStyle = P.core; c.fillRect(hx - hw * 0.12, -hh / 2 + lw, hw * 0.24, hh - lw * 2);
        if (o.barbs) {       // Ravelbone
          c.strokeStyle = INK; c.lineWidth = lw * 0.8;
          for (let i = 0; i < 6; i++) { const y = -hh / 2 + (i + 0.5) * hh / 6; c.beginPath(); c.moveTo(hx + hw / 2, y); c.lineTo(hx + hw / 2 + r * 0.22, y - r * 0.08); c.stroke(); }
        }
      }
      break;
    }
    case "bow": {
      c.save(); c.translate(r * 1.55, 0);
      inkFill(c, () => { c.beginPath(); c.moveTo(0, -r * 1.9); c.bezierCurveTo(r * 0.9, -r * 1.3, r * 0.9, r * 1.3, 0, r * 1.9); c.bezierCurveTo(r * 0.62, r * 1.2, r * 0.62, -r * 1.2, 0, -r * 1.9); c.closePath(); }, mix(P.core, P.dark, 0.2), P.dark, lw);
      c.strokeStyle = P.glow; c.lineWidth = r * 0.035; c.beginPath(); c.moveTo(0, -r * 1.85); c.lineTo(-r * (o.draw || 0.15), 0); c.lineTo(0, r * 1.85); c.stroke();
      c.restore();
      break;
    }
    case "staff": {          // long, out ONE side, head holding the school's light
      const L = r * 4.6;
      inkFill(c, () => { c.beginPath(); c.moveTo(r * 0.95, -r * 0.08); for (let i = 1; i <= 8; i++) { const x = r * 0.95 + (L - r * 0.95) * i / 8; c.lineTo(x, (i % 2 ? -1 : 1) * r * 0.05 - r * 0.09); } c.lineTo(L, r * 0.1); for (let i = 7; i >= 0; i--) { const x = r * 0.95 + (L - r * 0.95) * i / 8; c.lineTo(x, (i % 2 ? -1 : 1) * r * 0.05 + r * 0.09); } c.closePath(); }, "#5b4636", "#2a1c12", lw * 0.8);
      c.strokeStyle = INK; c.lineWidth = lw * 1.2;
      for (const s of [-1, 1]) { c.beginPath(); c.moveTo(L - r * 0.2, 0); c.quadraticCurveTo(L + r * 0.2, s * r * 0.8, L + r * 0.75, s * r * 0.15); c.stroke(); }
      glow(c, L + r * 0.45, 0, r * 1.6, P.core, 1);
      inkFill(c, () => { c.beginPath(); c.arc(L + r * 0.45, 0, r * 0.36, 0, TAU); }, P.glow, P.core, lw * 0.7);
      break;
    }
    case "flail": {
      haft(r * 0.95, r * 1.9, r * 0.2);
      const cx = r * 1.9, bx = r * 3.6, by = r * 0.6 * Math.sin(t * 5);
      c.strokeStyle = INK; c.lineWidth = lw * 1.4;
      for (let i = 0; i < 5; i++) { const u = (i + 0.5) / 5; c.beginPath(); c.ellipse(lerp(cx, bx - r * 0.5, u), by * u * u, r * 0.13, r * 0.08, 0, 0, TAU); c.stroke(); }
      inkFill(c, () => { c.beginPath(); for (let i = 0; i < 16; i++) { const a = i / 16 * TAU, rr = i % 2 ? r * 0.55 : r * 0.82; c.lineTo(bx + Math.cos(a) * rr, by + Math.sin(a) * rr); } c.closePath(); }, steelA, steelB, lw);
      c.fillStyle = P.core; c.beginPath(); c.arc(bx, by, r * 0.25, 0, TAU); c.fill();
      break;
    }
  }
  if (o.glint > 0) {       // the blade shine — a four-point star, hard-edged
    const gx = o.glintX ?? r * 3, gy = o.glintY ?? -r * 0.2, s = r * 1.3 * o.glint;
    c.fillStyle = "#fff"; c.beginPath();
    c.moveTo(gx, gy - s); c.lineTo(gx + s * 0.1, gy - s * 0.1); c.lineTo(gx + s, gy); c.lineTo(gx + s * 0.1, gy + s * 0.1);
    c.lineTo(gx, gy + s); c.lineTo(gx - s * 0.1, gy + s * 0.1); c.lineTo(gx - s, gy); c.lineTo(gx - s * 0.1, gy - s * 0.1); c.closePath(); c.fill();
    glow(c, gx, gy, s * 1.2, "#ffffff", 0.9 * o.glint);
  }
  c.restore();
}

function drawRelic(c, x, y, r, sc, weapon, ang, o = {}) {
  drawOrb(c, x, y, r, sc, o);
  if (weapon) { c.save(); c.translate(x, y); drawWeapon(c, weapon, sc, r, ang, o.w || { t: o.t }); c.restore(); }
}

/* ---------------------------------------------------------------- effects */
/* 集中線 — focus lines: thin wedges from the frame edge toward a point. */
function focusLines(c, cx, cy, n, rIn, col, seed, a = 1, width = 1) {
  c.save(); c.fillStyle = col; c.globalAlpha = a;
  const R = 2400;
  for (let i = 0; i < n; i++) {
    const ang = h2(i, seed) * TAU, w = (0.004 + 0.012 * h2(i, seed + 1)) * width;
    const r0 = rIn * (0.8 + 0.7 * h2(i, seed + 2));
    c.beginPath();
    c.moveTo(cx + Math.cos(ang) * r0, cy + Math.sin(ang) * r0);
    c.lineTo(cx + Math.cos(ang - w) * R, cy + Math.sin(ang - w) * R);
    c.lineTo(cx + Math.cos(ang + w) * R, cy + Math.sin(ang + w) * R);
    c.closePath(); c.fill();
  }
  c.restore();
}
/* Speed lines along a direction — the background of every dash. */
function speedLines(c, ang, n, col, seed, a = 1, t = 0, speed = 3000) {
  c.save(); c.translate(W / 2, H / 2); c.rotate(ang); c.fillStyle = col; c.globalAlpha = a;
  for (let i = 0; i < n; i++) {
    const y = (h2(i, seed) - 0.5) * 2600, len = 300 + 900 * h2(i, seed + 1), th = 2 + 10 * Math.pow(h2(i, seed + 2), 3);
    const x = ((h2(i, seed + 3) * 5000 - t * speed * (0.6 + h2(i, seed + 4))) % 5000 + 5000) % 5000 - 2500;
    c.beginPath(); c.moveTo(x, y - th / 2); c.lineTo(x + len, y); c.lineTo(x, y + th / 2); c.closePath(); c.fill();
  }
  c.restore();
}
function shockRing(c, x, y, rad, th, col, a = 1, squash = 1) {
  if (a <= 0 || rad <= 0) return;
  c.save(); c.globalAlpha = a; c.strokeStyle = col; c.lineWidth = Math.max(1, th);
  c.beginPath(); c.ellipse(x, y, rad, rad * squash, 0, 0, TAU); c.stroke();
  c.globalAlpha = a * 0.6; c.lineWidth = Math.max(1, th * 0.25); c.strokeStyle = "#fff";
  c.beginPath(); c.ellipse(x, y, rad * 0.93, rad * 0.93 * squash, 0, 0, TAU); c.stroke(); c.restore();
}
/* Sparks: analytic particles — position is a function of age, so no state. */
function sparks(c, x, y, age, seed, n, spd, col, o = {}) {
  if (age < 0) return;
  const life = o.life || 0.6, drag = o.drag || 3.2, grav = o.grav || 0, len = o.len || 0.05;
  c.save(); c.lineCap = "round";
  for (let i = 0; i < n; i++) {
    const L = life * (0.5 + h2(i, seed + 9));
    if (age > L) continue;
    const a0 = (o.ang ?? 0) + (h2(i, seed) - 0.5) * (o.spread ?? TAU), v = spd * (0.35 + 0.9 * h2(i, seed + 1));
    const d = v * (1 - Math.exp(-drag * age)) / drag;
    const d2 = v * (1 - Math.exp(-drag * Math.max(0, age - len))) / drag;
    const px = x + Math.cos(a0) * d, py = y + Math.sin(a0) * d + grav * age * age;
    const qx = x + Math.cos(a0) * d2, qy = y + Math.sin(a0) * d2 + grav * Math.max(0, age - len) ** 2;
    const k = 1 - age / L;
    c.strokeStyle = h2(i, seed + 5) < 0.35 ? "#ffffff" : col; c.globalAlpha = Math.min(1, k * 1.4);
    c.lineWidth = (o.w || 6) * (0.4 + k);
    c.beginPath(); c.moveTo(qx, qy); c.lineTo(px, py); c.stroke();
  }
  c.restore();
}
/* A cel explosion: stacked jagged discs, white core to dark smoke, on twos. */
function celBurst(c, x, y, R, age, dur, cols, seed) {
  if (age < 0 || age > dur) return;
  const u = age / dur, tq = Math.floor(age * 12);
  const layers = [[cols[3] || "#1a1020", 1.0, 0.25], [cols[2], 0.86, 0.12], [cols[1], 0.68, 0.06], [cols[0], 0.44, 0]];
  for (let L = 0; L < layers.length; L++) {
    const [col, s, lag] = layers[L], uu = clamp((u - lag) / (1 - lag));
    const rr = R * s * E.outExpo(Math.min(1, uu * 2.2)) * (L === 3 ? (1 - uu) : 1) * (L === 0 ? 1 : (1 - uu * 0.6));
    if (rr <= 1) continue;
    c.beginPath();
    for (let i = 0; i < 20; i++) { const a = i / 20 * TAU, k = 0.78 + 0.34 * h3(i, tq, seed + L); c.lineTo(x + Math.cos(a) * rr * k, y + Math.sin(a) * rr * k - (L === 0 ? rr * 0.2 * uu : 0)); }
    c.closePath(); c.fillStyle = col; c.globalAlpha = L === 0 ? 0.85 * (1 - uu) : 1; c.fill();
  }
  c.globalAlpha = 1;
}
/* Screentone — the manga halftone. */
function halftone(c, cx, cy, R, col, sp = 26, a = 1, rot = 0.4) {
  c.save(); c.fillStyle = col; c.globalAlpha = a; c.translate(cx, cy); c.rotate(rot);
  const n = Math.ceil(R / sp);
  for (let i = -n; i <= n; i++) for (let j = -n; j <= n; j++) {
    const x = i * sp, y = j * sp, d = Math.hypot(x, y) / R;
    if (d > 1) continue;
    const rr = sp * 0.5 * (1 - d);
    if (rr < 0.8) continue;
    c.beginPath(); c.arc(x, y, rr, 0, TAU); c.fill();
  }
  c.restore();
}
function lightning(c, x0, y0, x1, y1, seed, col, w, jag = 0.18, a = 1) {
  const n = 10, dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  const pts = [];
  for (let i = 0; i <= n; i++) { const u = i / n, off = (i === 0 || i === n) ? 0 : (h2(i, seed) - 0.5) * 2 * jag * L * Math.sin(u * Math.PI); pts.push([x0 + dx * u + nx * off, y0 + dy * u + ny * off]); }
  c.save(); c.globalAlpha = a; c.lineJoin = "miter"; c.lineCap = "round";
  for (const [lwk, cc] of [[2.6, col], [1, "#ffffff"]]) {
    c.strokeStyle = cc; c.lineWidth = w * lwk; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke();
  }
  c.restore();
}

/* ---------------------------------------------------------------- text
   The slam: arrives huge and hard, overshoots, settles, then shivers. Heavy
   italic (a skew), a white keyline inside a black one — the anime title card. */
/* Noto Sans CJK JP Black is what the committed render used (Latin and
   Japanese in one heavy face). The fallbacks keep a Windows render legible
   if Noto is not installed there — but it will not match; install Noto. */
const FONT = '"Noto Sans CJK JP", "Yu Gothic UI", "Meiryo", "Arial Black", sans-serif';
function slam(c, str, x, y, size, age, o = {}) {
  if (age < 0) return;
  const inT = o.inT ?? 0.14, out = o.out ?? 99, outT = o.outT ?? 0.12;
  if (age > out + outT) return;
  let s = age < inT ? lerp(o.from ?? 2.6, 1, E.outCubic(age / inT)) : 1 + 0.05 * Math.exp(-(age - inT) * 14) * Math.sin((age - inT) * 60);
  let a = age > out ? 1 - (age - out) / outT : 1;
  if (age > out) s *= 1 + 0.4 * (age - out) / outT;
  c.save(); c.translate(x + (o.shake ? o.shake * noise1(age * 40, 3) : 0), y); c.scale(s, s);
  c.transform(1, 0, o.skew ?? -0.18, 1, 0, 0);
  c.font = `${o.weight || 900} ${size}px ${o.font || FONT}`; c.textAlign = o.align || "center"; c.textBaseline = "middle";
  c.globalAlpha = a * (o.alpha ?? 1);
  if (o.letter) c.letterSpacing = o.letter + "px";
  if (o.maxW) { const w = c.measureText(str).width; if (w > o.maxW) c.scale(o.maxW / w, o.maxW / w); }
  c.lineJoin = "round";
  if (o.stroke !== false) {
    c.strokeStyle = o.outer || INK; c.lineWidth = size * (o.ow ?? 0.24); c.strokeText(str, 0, 0);
    c.strokeStyle = o.inner || "#ffffff"; c.lineWidth = size * (o.iw ?? 0.11); c.strokeText(str, 0, 0);
  }
  if (o.grad) { const g = c.createLinearGradient(0, -size / 2, 0, size / 2); o.grad.forEach((cc, i) => g.addColorStop(i / (o.grad.length - 1), cc)); c.fillStyle = g; }
  else c.fillStyle = o.fill || "#ffffff";
  c.fillText(str, 0, 0);
  c.restore();
}
/* A vertical line of Japanese, the way a title card sets it. */
function vText(c, str, x, y, size, col, a = 1, o = {}) {
  if (a <= 0) return;
  c.save(); c.font = `${o.weight || 900} ${size}px ${FONT}`; c.textAlign = "center"; c.textBaseline = "middle"; c.globalAlpha = a;
  [...str].forEach((ch, i) => {
    const yy = y + i * size * 1.05;
    if (o.stroke) { c.strokeStyle = o.stroke; c.lineWidth = size * 0.18; c.lineJoin = "round"; c.strokeText(ch, x, yy); }
    c.fillStyle = col; c.fillText(ch, x, yy);
  });
  c.restore();
}

/* ---------------------------------------------------------------- post */
let _tmp = null;
function tmpCanvas() { if (!_tmp) { _tmp = document.createElement("canvas"); _tmp.width = W; _tmp.height = H; } return _tmp; }
/* THE IMPACT FRAME: the picture thresholded to ink — black/white, inverted or
   not, optionally with the white turned to a colour. Two to four frames of it
   is the loudest thing anime can do without sound. */
function impactFrame(c, mode, col) {
  const cv = c.canvas, tmp = tmpCanvas(), g = tmp.getContext("2d");
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = "copy"; g.filter = "none"; g.drawImage(cv, 0, 0); g.globalCompositeOperation = "source-over";
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
  c.filter = mode === "inv" ? "grayscale(1) brightness(1.1) contrast(30) invert(1)" : "grayscale(1) brightness(1.4) contrast(30)";
  c.drawImage(tmp, 0, 0); c.filter = "none";
  if (col) { c.globalCompositeOperation = "multiply"; c.fillStyle = col; c.fillRect(0, 0, W, H); }
  c.restore();
}
function flash(c, col, a) { if (a <= 0) return; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = Math.min(1, a); c.fillStyle = col; c.fillRect(0, 0, W, H); c.restore(); }
function vignette(c, a = 0.7) {
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
  const g = c.createRadialGradient(W / 2, H / 2, H * 0.28, W / 2, H / 2, H * 0.75);
  g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, `rgba(0,0,0,${a})`);
  c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore();
}
function grain(c, t, a = 0.05) {       // film grain, on twos
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = a; const s = Math.floor(t * 12);
  for (let i = 0; i < 900; i++) { c.fillStyle = h2(i, s) > 0.5 ? "#fff" : "#000"; c.fillRect(h3(i, s, 1) * W, h3(i, s, 2) * H, 2, 2); }
  c.restore();
}
/* Screen crack: jagged radial fractures from a point, drawn over the picture. */
function screenCrack(c, x, y, R, seed, u) {
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.lineJoin = "miter";
  for (let i = 0; i < 14; i++) {
    const a0 = h2(i, seed) * TAU, len = R * (0.4 + 0.8 * h2(i, seed + 1)) * E.outExpo(u);
    let px = x, py = y; c.beginPath(); c.moveTo(px, py);
    for (let k = 1; k <= 6; k++) { const a = a0 + (h2(i * 7 + k, seed + 2) - 0.5) * 0.7; px = x + Math.cos(a) * len * k / 6; py = y + Math.sin(a) * len * k / 6; c.lineTo(px, py); }
    c.strokeStyle = "#000"; c.lineWidth = 9; c.stroke(); c.strokeStyle = "#fff"; c.lineWidth = 3; c.stroke();
  }
  c.restore();
}

/* ---------------------------------------------------------------- the arena
   The game's hall, redrawn as an anime background plate: the school-tinted
   dark, the floor sigil, the glowing walls, dust in the light. */
const ARENA = { x0: 110, y0: 330, x1: 970, y1: 1570 };
function drawArena(c, sc, t, o = {}) {
  const P = PAL[sc], A = ARENA;
  const g = c.createLinearGradient(0, -400, 0, H + 400);
  g.addColorStop(0, mix(P.dark, "#000", 0.55)); g.addColorStop(0.5, mix(P.dark, "#05030a", 0.25)); g.addColorStop(1, "#030207");
  c.fillStyle = g; c.fillRect(-1200, -1200, W + 2400, H + 2400);
  // painted light pool
  glow(c, W / 2, H * 0.45, 900, P.core, 0.22);
  // floor sigil (the game's pentagram floor)
  c.save(); c.translate(W / 2, (A.y0 + A.y1) / 2); c.rotate(t * 0.05);
  c.strokeStyle = hexA(P.glow, 0.13); c.lineWidth = 3;
  c.beginPath(); c.arc(0, 0, 400, 0, TAU); c.stroke(); c.beginPath(); c.arc(0, 0, 330, 0, TAU); c.stroke();
  c.beginPath(); for (let i = 0; i <= 5; i++) { const a = -Math.PI / 2 + i * 2 * TAU / 5; c.lineTo(Math.cos(a) * 400, Math.sin(a) * 400); } c.stroke();
  c.restore();
  // walls
  c.save(); c.lineJoin = "miter";
  c.strokeStyle = INK; c.lineWidth = 30; c.strokeRect(A.x0, A.y0, A.x1 - A.x0, A.y1 - A.y0);
  c.strokeStyle = o.wallCol || P.core; c.lineWidth = 9; c.strokeRect(A.x0, A.y0, A.x1 - A.x0, A.y1 - A.y0);
  c.strokeStyle = "#fff"; c.globalAlpha = 0.6; c.lineWidth = 2.5; c.strokeRect(A.x0, A.y0, A.x1 - A.x0, A.y1 - A.y0);
  c.restore();
  // dust motes drifting through the light
  for (let i = 0; i < 70; i++) {
    const x = (h2(i, 91) * (W + 400) + t * 20 * (h2(i, 92) - 0.3)) % (W + 400) - 200, y = (h2(i, 93) * (H + 400) - t * 30 * h2(i, 94) + H + 400) % (H + 400) - 200;
    c.fillStyle = hexA(P.glow, 0.25 + 0.4 * h2(i, 95)); c.beginPath(); c.arc(x, y, 1.5 + 3 * h2(i, 96), 0, TAU); c.fill();
  }
}

/* Paint a flat colour field with focus lines and tone — the cut-in plate. */
function cutInPlate(c, sc, t, seed, o = {}) {
  const P = PAL[sc];
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
  const g = c.createLinearGradient(0, 0, W, H); g.addColorStop(0, mix(P.core, "#fff", 0.1)); g.addColorStop(1, mix(P.dark, "#000", 0.2));
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  halftone(c, o.hx ?? W * 0.8, o.hy ?? H * 0.25, 900, hexA(P.dark, 1), 30, 0.35);
  focusLines(c, o.fx ?? W / 2, o.fy ?? H / 2, 140, o.fr ?? 380, "#ffffff", seed + Math.floor(t * 12), 0.55);
  c.restore();
}
