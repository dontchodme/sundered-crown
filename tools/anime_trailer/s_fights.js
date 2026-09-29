/* ANIME TRAILER — four fights, each an ultimate as the game has it, drawn
   loud. Beats 24-66. Nothing here is a new mechanic: every move below is the
   shipped ultimate's own verb (see the tips quoted beside each). */
"use strict";

function inArena(c, sc, cam, lt, fn, o) {
  c.save(); camera(c, cam); drawArena(c, sc, lt, o); fn(); c.restore();
}
const keyPos = (keys, b) => {                // piecewise-eased path through [beat, x, y]
  if (b <= keys[0][0]) return [keys[0][1], keys[0][2]];
  for (let i = 1; i < keys.length; i++) if (b <= keys[i][0]) {
    const [b0, x0, y0] = keys[i - 1], [b1, x1, y1] = keys[i], u = E.outCubic((b - b0) / (b1 - b0));
    return [lerp(x0, x1, u), lerp(y0, y1, u)];
  }
  const k = keys[keys.length - 1]; return [k[1], k[2]];
};

/* ============================================================ THE WINNOWING 24-36
   "Fires a fan of kunai that ricochet. Ricochets deal bonus damage."
   Rick's §1: the twinblade forgoes its blades for leaf kunai; a fan fires in
   both directions; they ricochet off walls and grow on every ricochet; no
   homing — natural, predictable ricochet. */
{
  const TS = "verdant", GW = "umbral", R = 68;
  const tsHome = [380, 1200], gwHome = [720, 600];
  const aim = Math.atan2(tsHome[1] - gwHome[1], tsHome[0] - gwHome[0]);
  const KUNAI = [];
  for (let i = 0; i < 14; i++) {
    const side = i < 7 ? 0 : 1, j = i % 7;
    const a = (side ? Math.PI - 0.95 : -0.95) + (j - 3) * 0.16;
    KUNAI.push({ a, v: 1150 + 60 * h2(i, 5) });
  }
  const FIRE = 4.5;
  const kunaiAt = (k, age) => bounceAt(tsHome[0], tsHome[1], Math.cos(k.a) * k.v, Math.sin(k.a) * k.v, age, ARENA, 18);
  const finals = [[8.2, -2.6], [8.5, 0.4], [8.8, -1.2], [9.1, 2.3], [9.35, -0.2]];   // the last legs in: [beat, from-angle]

  scene(24, 36, "the winnowing", (c, lt, lb, t) => {
    const lq = Math.floor(lb * 5 + 1e-6) / 5;
    // --------------------------------------------------- 0-3: Crossweave, and the dodge
    if (lb < 3) {
      const release = 1.0, ra = ageB(lb, release);
      const camP = lb < release ? gwHome : [lerp(gwHome[0], 470, E.inOut(clamp(ra / 0.7))), lerp(gwHome[1], 1080, E.inOut(clamp(ra / 0.7)))];
      const cam = { x: camP[0], y: camP[1], z: lb < release ? 1.75 - 0.1 * lb : lerp(1.65, 1.3, clamp(ra / 0.7)), rot: -0.06, t: lt, shake: ra > 0 && ra < 0.2 ? 18 : 0 };
      const dodge = 1.85, da = ageB(lb, dodge);
      const tsP = da < 0 ? tsHome : [lerp(tsHome[0], 225, E.outExpo(clamp(da / 0.25))), lerp(tsHome[1], 1060, E.outExpo(clamp(da / 0.25)))];
      inArena(c, TS, cam, lt, () => {
        // the bow, drawn and loosed
        const draw = lb < release ? 0.1 + 0.55 * E.outCubic(clamp(lb / 0.8)) : 0.1;
        drawRelic(c, gwHome[0], gwHome[1], R, GW, "bow", aim, { t: lt, fill: 0.5, aura: lb < release ? 0.4 : 0, w: { t: lt, draw, glint: clamp(1 - Math.abs(lb - 0.8) / 0.15) } });
        if (ra > 0) {
          const arrows = [-0.16, 0, 0.16].map(o => {
            const a = aim + o * (1 + ra), d = 120 + 1500 * ra;
            return [gwHome[0] + Math.cos(a) * d, gwHome[1] + Math.sin(a) * d, a];
          });
          for (let i = 0; i < 2; i++) lightning(c, arrows[i][0], arrows[i][1], arrows[i + 1][0], arrows[i + 1][1], 7 + i + Math.floor(lt * 12) * 3, PAL[GW].core, 14, 0.14);
          arrows.forEach(([x, y, a]) => {
            c.save(); c.translate(x, y); c.rotate(a); glow(c, 0, 0, 90, PAL[GW].core, 0.8);
            c.fillStyle = INK; c.fillRect(-70, -6, 70, 12); c.fillStyle = PAL[GW].glow; c.fillRect(-66, -3, 62, 6);
            c.beginPath(); c.moveTo(26, 0); c.lineTo(-6, -15); c.lineTo(-6, 15); c.closePath(); c.fillStyle = PAL[GW].core; c.fill(); c.strokeStyle = INK; c.lineWidth = 5; c.stroke();
            c.restore();
          });
          sparks(c, gwHome[0] + Math.cos(aim) * 100, gwHome[1] + Math.sin(aim) * 100, ra, 51, 30, 1400, PAL[GW].glow, { ang: aim, spread: 1.2, life: 0.4 });
        }
        if (da > 0 && da < 0.3) { afterimages(c, [0.2, 0.45, 0.7].map(u => [lerp(tsHome[0], tsP[0], u), lerp(tsHome[1], tsP[1], u)]), R, TS); smear(c, tsHome[0], tsHome[1], tsP[0], tsP[1], R, PAL[TS].glow, 0.6); }
        drawRelic(c, tsP[0], tsP[1], R, TS, "twinblade", -0.6, { t: lt, fill: 0.7, w: { t: lt } });
      });
      if (lb < release) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); focusLines(c, W / 2, H / 2, 90, 520, "#ffffff", 12 + Math.floor(lt * 12), 0.35); c.restore(); }
      return;
    }
    // --------------------------------------------------- 3-4.5: the cut-in
    if (lb < FIRE) {
      const age = ageB(lb, 3);
      cutInPlate(c, TS, lt, 60, { fx: 540, fy: 880, fr: 360 });
      const dissolve = clamp((lb - 4.0) / 0.5);
      const s = 1 + 0.06 * age;
      c.save(); c.translate(540, 880); c.scale(s, s); c.translate(-540, -880);
      drawOrb(c, 540, 880, 250, TS, { t: lt, fill: 0.7, aura: 0.8 });
      c.save(); c.globalAlpha = 1 - dissolve; c.translate(540, 880); drawWeapon(c, "twinblade", TS, 250, -0.85, { t: lt, glint: clamp(1 - Math.abs(age - 0.3) / 0.12) }); c.restore();
      for (let i = 0; i < 22 * dissolve; i++) {        // the blades coming apart into leaves
        const u = (i + 1) / 22, a = -0.85 + (h2(i, 2) - 0.5) * 0.5, d = 250 * (1.3 + 2.3 * u);
        const px = 540 + Math.cos(a) * d + (dissolve * 300 + 60) * (h2(i, 3) - 0.3), py = 880 + Math.sin(a) * d - dissolve * 200 * h2(i, 4);
        drawKunai(c, px, py, a + dissolve * 3 * (h2(i, 6) - 0.5), 1.4, TS, 0);
      }
      c.restore();
      callout(c, "THE WINNOWING", TS, age - 0.05, 1400, { size: 112, dur: 1.5 });
      if (age < 0.08) flash(c, "#ffffff", 1 - age / 0.08);
      return;
    }
    // --------------------------------------------------- 4.5-8: the fan, ricocheting
    if (lb < 8) {
      const age = ageB(lb, FIRE);
      const cam = { x: 540, y: 1030, z: 0.97 + 0.04 * (lb - FIRE) / 3.5, rot: 0.03 * Math.sin(lb), t: lt, shake: age < 0.25 ? 20 : 3 };
      inArena(c, TS, cam, lt, () => {
        drawRelic(c, gwHome[0] + 25 * Math.sin(lt * 2), gwHome[1], R, GW, "bow", aim, { t: lt, fill: 0.5, w: { t: lt } });
        drawRelic(c, tsHome[0], tsHome[1], R, TS, null, 0, { t: lt, fill: 0.7, aura: 0.5 * Math.exp(-age) + 0.2 });
        sparks(c, tsHome[0], tsHome[1], age, 81, 40, 1500, PAL[TS].glow, { life: 0.5 });
        shockRing(c, tsHome[0], tsHome[1], 600 * E.outExpo(age / 0.5), 30 * (1 - age / 0.5), PAL[TS].glow, 1 - age / 0.5);
        KUNAI.forEach((k, i) => {
          const tq = twos(age);
          const p = kunaiAt(k, tq), n = p.n, s = 1.2 + 0.34 * Math.min(n, 6), heat = Math.min(1, n * 0.22);
          // trail
          c.save(); c.lineCap = "round";
          for (let j = 1; j <= 5; j++) {
            const q0 = kunaiAt(k, Math.max(0, tq - (j - 1) * 0.025)), q1 = kunaiAt(k, Math.max(0, tq - j * 0.025));
            if (Math.hypot(q0.x - q1.x, q0.y - q1.y) > 120) continue;
            c.strokeStyle = hexA(heat > 0.5 ? "#ffffff" : PAL[TS].glow, 0.55 * (1 - j / 6)); c.lineWidth = 16 * s * (1 - j / 7);
            c.beginPath(); c.moveTo(q0.x, q0.y); c.lineTo(q1.x, q1.y); c.stroke();
          }
          c.restore();
          const q = kunaiAt(k, Math.max(0, tq - 0.01));
          drawKunai(c, p.x, p.y, Math.atan2(p.y - q.y, p.x - q.x), s, TS, heat);
          // a flash on every wall it touches
          for (let f = 0; f < 4; f++) {
            const a1 = kunaiAt(k, Math.max(0, age - f / FPS)), a0 = kunaiAt(k, Math.max(0, age - (f + 1) / FPS));
            if (a1.n > a0.n) { const fa = f / FPS; celBurst(c, a1.x, a1.y, 70 + 18 * a1.n, fa, 0.2, ["#ffffff", PAL[TS].glow, PAL[TS].core, PAL[TS].dark], i * 7 + a1.n); sparks(c, a1.x, a1.y, fa, i * 13 + a1.n, 10, 900, "#ffffff", { life: 0.25, w: 5 }); }
          }
        });
      });
      return;
    }
    // --------------------------------------------------- 8-10: the last legs in, and the big one
    if (lb < 10) {
      const BIG = 9.5, ba = ageB(lb, BIG);
      let gwP = [...gwHome];
      finals.forEach(([hb, fa]) => { const a = ageB(lb, hb); if (a > 0) { const k = 16 * Math.exp(-a * 10); gwP[0] -= Math.cos(fa) * k; gwP[1] -= Math.sin(fa) * k; } });
      let launched = null;
      if (ba > 0) {
        const u = E.outCubic(clamp(ba / 0.4 * 2.5 / 2.5));
        launched = [lerp(gwHome[0], 925, u), lerp(gwHome[1], 375, u)];
        gwP = launched;
      }
      const cam = { x: ba > 0 ? lerp(gwHome[0], 840, E.outCubic(clamp(ba / 0.4))) : gwHome[0], y: ba > 0 ? lerp(gwHome[1], 470, E.outCubic(clamp(ba / 0.4))) : gwHome[1], z: ba > 0 ? lerp(2.0, 1.55, clamp(ba / 0.4)) : 2.0 + 0.1 * (lb - 8), rot: 0.08, t: lt, shake: 0 };
      finals.forEach(([hb]) => { const a = ageB(lb, hb); if (a > 0 && a < 0.12) cam.shake = 26; });
      const wa = ageB(lb, BIG + 0.95);
      if (ba > 0) cam.shake = Math.max(cam.shake, 70 * Math.exp(-ba * 3));
      if (wa > 0) cam.shake = 90 * Math.exp(-wa * 3);
      inArena(c, TS, cam, lt, () => {
        if (wa > 0) {                          // the crater: the wall itself breaks
          c.save(); c.strokeStyle = "#ffffff"; c.lineWidth = 5;
          for (let i = 0; i < 9; i++) { const a = Math.PI * (0.05 + 0.9 * h2(i, 3)) - Math.PI; c.beginPath(); c.moveTo(930, 340); let x = 930, y = 340; for (let s = 0; s < 4; s++) { x += Math.cos(a + (h2(i, s) - 0.5)) * 50; y += Math.sin(a + (h2(i, s) - 0.5)) * 50 * -1; c.lineTo(x, y); } c.strokeStyle = INK; c.lineWidth = 10; c.stroke(); c.strokeStyle = PAL[TS].glow; c.lineWidth = 4; c.stroke(); }
          c.restore();
          celBurst(c, 930, 360, 300, wa, 0.7, ["#ffffff", PAL[GW].glow, PAL[GW].core, "#1a0b2a"], 44);
          sparks(c, 930, 360, wa, 45, 50, 2000, "#ffffff", { life: 0.7, ang: Math.PI * 0.75, spread: 2.2 });
        }
        if (launched && ba < 0.5) smear(c, gwHome[0], gwHome[1], gwP[0], gwP[1], R, PAL[GW].core, 0.7);
        drawRelic(c, gwP[0], gwP[1], R, GW, "bow", aim + (ba > 0 ? ba * 8 : 0), { t: lt, fill: 0.5 - 0.05 * finals.filter(f => lb > f[0]).length - (ba > 0 ? 0.12 : 0), w: { t: lt } });
        finals.forEach(([hb, fa], i) => {
          const a = ageB(lb, hb);
          if (a < -0.22 || a > 0.35) return;
          if (a < 0) {                            // incoming, a straight last leg
            const d = -a * 2600, s = 1.5 + i * 0.35;
            const px = gwHome[0] + Math.cos(fa) * d, py = gwHome[1] + Math.sin(fa) * d;
            c.save(); c.strokeStyle = hexA("#ffffff", 0.6); c.lineWidth = 18 * s; c.lineCap = "round"; c.beginPath(); c.moveTo(px, py); c.lineTo(px + Math.cos(fa) * 200, py + Math.sin(fa) * 200); c.stroke(); c.restore();
            drawKunai(c, px, py, fa + Math.PI, s, TS, 1);
          } else {
            celBurst(c, gwHome[0] + Math.cos(fa) * 40, gwHome[1] + Math.sin(fa) * 40, 150 + 30 * i, a, 0.28, ["#ffffff", PAL[TS].glow, PAL[TS].core, PAL[TS].dark], i + 90);
            sparks(c, gwHome[0], gwHome[1], a, 200 + i, 24, 1500, PAL[TS].glow, { ang: fa + Math.PI, spread: 1.4, life: 0.35 });
          }
        });
        if (ba > -0.25 && ba < 0) {              // the big one, grown on every wall
          const d = -ba * 3000, fa = 2.5;
          drawKunai(c, gwHome[0] + Math.cos(fa) * d, gwHome[1] + Math.sin(fa) * d, fa + Math.PI, 4.2, TS, 1);
        }
        if (ba > 0) { celBurst(c, gwHome[0], gwHome[1], 420, ba, 0.5, ["#ffffff", PAL[TS].glow, PAL[TS].core, "#0a1f0c"], 91); shockRing(c, gwHome[0], gwHome[1], 900 * E.outExpo(ba / 0.5), 50 * (1 - ba / 0.5), "#ffffff", 1 - ba / 0.5); }
      });
      if (ba > -0.2 && ba < 0) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); focusLines(c, W / 2, H / 2, 140, 300, "#ffffff", 5 + Math.floor(lt * 12), 0.8); c.restore(); }
      const im = impactMode(lb, BIG, ["g", "i", "n", "i"]) || impactMode(lb, BIG + 0.95, ["n"]);
      if (im) applyImpact(c, im);
      return;
    }
    // --------------------------------------------------- 10-12: Thornshear, and the leaves coming down
    const age = ageB(lb, 10);
    const cam = { x: 470, y: 1020, z: 1.55 - 0.08 * age, rot: -0.05, t: lt, shake: 0 };
    inArena(c, TS, cam, lt, () => {
      drawRelic(c, 930, 375, R, GW, "bow", 2.2, { t: lt, fill: 0.3, glow: 0.2, w: { t: lt } });
      const re = clamp(age / 0.5);
      drawOrb(c, tsHome[0] + 40, tsHome[1] - 120, R * 1.25, TS, { t: lt, fill: 0.7, aura: 0.3 });
      c.save(); c.globalAlpha = re; c.translate(tsHome[0] + 40, tsHome[1] - 120); drawWeapon(c, "twinblade", TS, R * 1.25, -0.7, { t: lt, glint: clamp(1 - Math.abs(age - 0.55) / 0.1) }); c.restore();
    });
    for (let i = 0; i < 26; i++) {           // leaves falling past the lens, big and soft
      const x = (h2(i, 1) * 1300 - 110 + 60 * Math.sin(lt * 2 + i)), y = ((h2(i, 2) * 2400 + lt * (260 + 200 * h2(i, 3))) % 2400) - 240;
      c.save(); c.globalAlpha = 0.85; drawKunai(c, x, y, lt * (1 + h2(i, 4)) * 2 + i, 1.2 + 1.8 * h2(i, 5), TS, 0); c.restore();
    }
    if (lb > 11.5) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); speedLines(c, 0, 90, "#ffffff", 9, clamp((lb - 11.5) / 0.5), lt, 7000); c.restore(); }
  });
  cue(24, "bow_draw", { dur: BEAT });
  cue(25, "crossweave"); cue(25.05, "zap", { dur: 0.6 });
  cue(25.85, "dodge");
  cue(27, "cutin"); cue(27.05, "callout");
  cue(28, "leaves", { dur: 0.5 * BEAT });
  cue(28.5, "kunai_fan");
  for (let i = 0; i < 14; i++) {             // a tink for every ricochet, computed from the same law
    const k = KUNAI[i];
    let prev = 0;
    for (let f = 1; f <= Math.round(3.5 * BEAT * FPS); f++) {
      const n = bounceAt(tsHome[0], tsHome[1], Math.cos(k.a) * k.v, Math.sin(k.a) * k.v, f / FPS, ARENA, 18).n;
      if (n > prev) { cue(28.5 + f / FPS / BEAT, "ricochet", { n, gain: 0.35 }); prev = n; }
    }
  }
  finals.forEach(([hb]) => cue(24 + hb, "kunai_hit"));
  cue(24 + 9.5, "hit_huge"); cue(24 + 10.45, "wallslam");
  cue(35.5, "whoosh_out", { dur: 0.5 * BEAT });
}

/* ============================================================ BREACH / SENTINEL 36-48
   Breach: "Cuts the walls open — five vents that spit heat and Sunder."
   Sentinel: "Sweeps a slow beam. Its far end deals bonus damage." */
{
  const CC = "dwarven", VS = "vigil", R = 64;
  const VENTS = [          // [x, y, facing, size, open beat]
    [110, 760, -0.25, 1.15, 0.5], [560, 1570, -Math.PI / 2 - 0.35, 0.85, 1.5], [970, 1150, Math.PI + 0.2, 1.1, 2.5],
  ];
  const JETS = [[0, 3.0], [1, 3.4], [2, 3.8], [0, 5.0], [1, 5.4], [2, 10.3]];
  const ccKeys = [[0, 500, 950], [0.45, 175, 770], [0.6, 200, 820], [1.45, 560, 1500], [1.6, 600, 1470], [2.45, 905, 1150], [2.7, 860, 1150]];
  const vsKeys = [[0, 700, 700], [3.2, 700, 700], [3.5, 610, 560], [4.0, 760, 500], [4.6, 600, 600], [5.0, 560, 520]];
  const vsHome = [560, 520];
  const beamAng = b => 1.05 + 0.5 * E.inOut(clamp((b - 6.5) / 3.5)) - 0.25;

  function drawVent(c, v, open) {
    const [x, y, face, sz] = v; if (open <= 0) return;
    const o = E.outBack(clamp(open / 0.25)), wall = (x === 110 || x === 970) ? Math.PI / 2 : 0;
    c.save(); c.translate(x, y); c.rotate(wall);
    glow(c, 0, 0, 220 * sz * o, "#FF7A1A", 0.9);
    c.beginPath();
    for (let i = 0; i < 16; i++) { const a = i / 16 * TAU, rr = (i % 2 ? 0.7 : 1) * (0.9 + 0.2 * h2(i, x)); c.lineTo(Math.cos(a) * 95 * sz * o * rr, Math.sin(a) * 34 * sz * o * rr); }
    c.closePath(); c.fillStyle = INK; c.fill();
    c.beginPath(); c.ellipse(0, 0, 70 * sz * o, 20 * sz * o, 0, 0, TAU); c.fillStyle = "#FF7A1A"; c.fill();
    c.beginPath(); c.ellipse(0, 0, 44 * sz * o, 10 * sz * o, 0, 0, TAU); c.fillStyle = "#FFF1C1"; c.fill();
    c.restore();
  }
  function drawJet(c, v, age) {       // a tapering jet with a bright crescent front, orange to white-hot
    const [x, y, face, sz] = v, dur = 0.95; if (age < 0 || age > dur) return;
    const len = Math.min(720, 2200 * age) * sz, fade = age > dur - 0.3 ? (dur - age) / 0.3 : 1, w0 = 95 * sz;
    c.save(); c.translate(x, y); c.rotate(face); c.globalAlpha = fade;
    glow(c, len * 0.5, 0, len * 0.7, "#FF7A1A", 0.6);
    const body = (w, col) => { c.beginPath(); c.moveTo(0, -w); c.quadraticCurveTo(len * 0.6, -w * 0.55, len, -w * 0.25); c.lineTo(len, w * 0.25); c.quadraticCurveTo(len * 0.6, w * 0.55, 0, w); c.closePath(); c.fillStyle = col; c.fill(); };
    body(w0 * 1.1, INK); body(w0, "#E2361A"); body(w0 * 0.72, "#FF7A1A"); body(w0 * 0.42, "#FFD27A"); body(w0 * 0.18, "#FFFBEA");
    for (let i = 0; i < 6; i++) { const u = ((age * 3 + i / 6) % 1); c.fillStyle = hexA("#FFF1C1", 0.7); c.beginPath(); c.ellipse(len * u, (h2(i, 3) - 0.5) * w0 * 0.6 * (1 - u), 40 * (1 - u) + 10, 6, 0, 0, TAU); c.fill(); }
    // the crescent front
    c.lineCap = "round";
    c.strokeStyle = INK; c.lineWidth = 26 * sz; c.beginPath(); c.arc(len - 40 * sz, 0, 70 * sz, -1.0, 1.0); c.stroke();
    c.strokeStyle = "#FFFBEA"; c.lineWidth = 15 * sz; c.beginPath(); c.arc(len - 40 * sz, 0, 70 * sz, -1.0, 1.0); c.stroke();
    glow(c, len, 0, 160 * sz, "#FFF1C1", 0.8);
    c.restore();
  }
  function drawBeam(c, x, y, a, len, w, t) {
    c.save(); c.translate(x, y); c.rotate(a);
    glow(c, len * 0.5, 0, len * 0.65, PAL[VS].core, 0.7);
    const edge = (k) => w * (1 + 0.06 * Math.sin(t * 60 + k));
    const band = (ww, col) => { c.beginPath(); c.moveTo(0, -ww * 0.6); for (let i = 0; i <= 12; i++) c.lineTo(len * i / 12, -ww * (1 + 0.05 * Math.sin(t * 70 + i * 2))); c.arc(len, 0, ww, -Math.PI / 2, Math.PI / 2); for (let i = 12; i >= 0; i--) c.lineTo(len * i / 12, ww * (1 + 0.05 * Math.sin(t * 70 + i * 2 + 1))); c.lineTo(0, ww * 0.6); c.closePath(); c.fillStyle = col; c.fill(); };
    band(edge(0) * 1.12, INK); band(edge(1), PAL[VS].core); band(edge(2) * 0.66, PAL[VS].glow); band(edge(3) * 0.36, "#ffffff");
    c.strokeStyle = hexA("#ffffff", 0.8); c.lineWidth = 5;               // flow lines running outward
    for (let i = 0; i < 8; i++) { const u = (t * 2.2 + i / 8) % 1, yy = (h2(i, 4) - 0.5) * w * 1.3; c.beginPath(); c.moveTo(len * u, yy); c.lineTo(len * u + 120, yy); c.stroke(); }
    c.restore();
  }

  scene(36, 48, "breach / sentinel", (c, lt, lb, t) => {
    const lq = Math.floor(lb * 5 + 1e-6) / 5;
    const ccP = keyPos(ccKeys, lq);
    // ---------------------------------------------- 5-6.5: Vesper charges
    if (lb >= 5 && lb < 6.5) {
      const age = ageB(lb, 5), u = clamp(age / (1.5 * BEAT));
      const aimA = beamAng(6.5);
      const cam = { x: vsHome[0], y: vsHome[1] + 60, z: 1.9 + 0.3 * u, rot: -0.1 * u, t: lt, shake: 8 * u };
      c.save(); camera(c, cam); drawArena(c, VS, lt);
      VENTS.forEach(v => drawVent(c, v, 9));
      c.restore();
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
      const g = c.createRadialGradient(W / 2, H / 2 - 100, 200, W / 2, H / 2, 1100); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, `rgba(0,0,0,${0.85 * u})`);
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      focusLines(c, W / 2, H / 2, 150, 420, PAL[VS].glow, 30 + Math.floor(lt * 12), 0.5 * u);
      c.restore();
      c.save(); camera(c, cam);
      const tipX = vsHome[0] + Math.cos(aimA) * R * 3.4, tipY = vsHome[1] + Math.sin(aimA) * R * 3.4;
      drawRelic(c, vsHome[0], vsHome[1], R, VS, "scythe", aimA - 0.3, { t: lt, fill: 0.65, aura: 0.4 + 0.6 * u, w: { t: lt } });
      for (let i = 0; i < 40; i++) {                  // the light drawn in to the point
        const ph = (age * 1.6 + h2(i, 1)) % 1, a = h2(i, 2) * TAU, d = 380 * (1 - ph);
        c.strokeStyle = hexA(i % 3 ? PAL[VS].glow : "#ffffff", ph); c.lineWidth = 4 + 5 * ph;
        c.beginPath(); c.moveTo(tipX + Math.cos(a) * d, tipY + Math.sin(a) * d); c.lineTo(tipX + Math.cos(a) * (d + 60), tipY + Math.sin(a) * (d + 60)); c.stroke();
      }
      for (let k = 0; k < 3; k++) { const ph = (age * 2 + k / 3) % 1; shockRing(c, tipX, tipY, 260 * (1 - ph), 10 * ph, PAL[VS].glow, ph); }
      glow(c, tipX, tipY, 160 + 180 * u, "#ffffff", 0.6 + 0.4 * u);
      c.restore();
      callout(c, "SENTINEL", VS, age - 0.05, 1400, { size: 132, dur: 1.4, jpx: 270 });
      return;
    }
    // ---------------------------------------------- the arena: the slashes, the vents, the beam
    let cam;
    if (lb < 3) cam = { x: lerp(540, ccP[0], 0.55), y: lerp(960, ccP[1], 0.55), z: 1.25, rot: 0.05, t: lt, shake: 0 };
    else if (lb < 5) cam = { x: 600, y: 1000, z: 1.02, rot: 0, t: lt, shake: 4 };
    else cam = { x: 590, y: 1060, z: 0.93, rot: 0.02, t: lt, shake: lb < 10 ? 16 : 4 };
    VENTS.forEach(v => { const a = ageB(lb, v[4]); if (a > 0 && a < 0.2) cam.shake = 40; });
    JETS.forEach(([i, b]) => { const a = ageB(lb, b); if (a > 0 && a < 0.15) cam.shake = Math.max(cam.shake, 22); });
    const TIP = 9.0, ta = ageB(lb, TIP);
    if (ta > 0) cam.shake = Math.max(cam.shake, 90 * Math.exp(-ta * 3));
    inArena(c, lb < 5 ? CC : VS, cam, lt, () => {
      VENTS.forEach(v => drawVent(c, v, ageB(lb, v[4])));
      JETS.forEach(([i, b]) => drawJet(c, VENTS[i], ageB(lb, b)));
      // Cindercleave: three slashes that open the walls
      let ccDraw = ccP;
      if (lb >= 6.5) {                                          // riding the beam out to its far end
        const a = beamAng(Math.min(lb, TIP)), s = lerp(620, 900, E.inCubic(clamp((lb - 7.3) / (TIP - 7.3))));
        ccDraw = lb < TIP ? [vsHome[0] + Math.cos(a) * s, vsHome[1] + Math.sin(a) * s] : null;
      }
      if (ccDraw) {
        const sw = VENTS.map(v => ageB(lb, v[4])).find(a => a > -0.15 && a < 0.2);
        const ang = sw !== undefined ? -2.2 + 5 * E.outExpo(clamp((sw + 0.15) / 0.3)) : -0.8;
        drawRelic(c, ccDraw[0], ccDraw[1], R, CC, "scythe", ang, { t: lt, fill: lb >= 6.5 ? 0.45 - 0.2 * clamp((lb - 7.3) / 1.7) : 0.6, w: { t: lt } });
        if (sw !== undefined && sw > -0.05 && sw < 0.2) {       // the slash arc
          c.save(); c.translate(ccDraw[0], ccDraw[1]); c.globalAlpha = 1 - sw / 0.2;
          c.strokeStyle = "#FFF1C1"; c.lineWidth = 30; c.lineCap = "round"; c.beginPath(); c.arc(0, 0, R * 3.3, ang - 1.8, ang); c.stroke();
          c.strokeStyle = "#FF7A1A"; c.lineWidth = 12; c.beginPath(); c.arc(0, 0, R * 3.6, ang - 1.6, ang); c.stroke(); c.restore();
        }
      }
      VENTS.forEach(v => { const a = ageB(lb, v[4]); sparks(c, v[0], v[1], a, v[0] + v[1], 50, 2100, "#FFD27A", { life: 0.6, ang: v[2], spread: 2.4, grav: 900 }); });
      // Vesper
      const vsP = lb < 5 ? keyPos(vsKeys, lq) : vsHome;
      if (lb < 5 && lb > 3.1) { const p2 = keyPos(vsKeys, lq - 0.2); smear(c, p2[0], p2[1], vsP[0], vsP[1], R * 0.9, PAL[VS].core, 0.5); }
      const bA = beamAng(lb);
      drawRelic(c, vsP[0], vsP[1], R, VS, "scythe", lb >= 6.5 ? bA - 0.3 : -0.9, { t: lt, fill: 0.65, aura: lb >= 6.5 && lb < 10 ? 0.8 : 0, w: { t: lt } });
      if (lb >= 6.5 && lb < 10.2) {
        const on = clamp((lb - 6.5) / 0.15), off = lb > 9.6 ? 1 - clamp((lb - 9.6) / 0.6) : 1;
        const bx = vsHome[0] + Math.cos(bA) * R * 3.3, by = vsHome[1] + Math.sin(bA) * R * 3.3;
        drawBeam(c, bx, by, bA, 900 * on, 62 * off * (1 + 0.4 * Math.exp(-ageB(lb, 6.5) * 6)), lt);
        if (lb < TIP && lb > 7.3) {                             // it drinks the foe down the beam
          sparks(c, ccDraw[0], ccDraw[1], ((lb - 7.3) * BEAT) % 0.2, Math.floor((lb - 7.3) * 12), 12, 1100, PAL[VS].glow, { life: 0.25, w: 5 });
        }
      }
      if (ta > 0) {
        const a = beamAng(TIP), ex = vsHome[0] + Math.cos(a) * 900, ey = vsHome[1] + Math.sin(a) * 900;
        celBurst(c, ex, ey, 520, ta, 1.1, ["#ffffff", PAL[VS].glow, PAL[VS].core, "#2a0a1e"], 77);
        shockRing(c, ex, ey, 1300 * E.outExpo(ta / 0.8), 70 * (1 - ta / 0.8), "#ffffff", 1 - ta / 0.8);
        sparks(c, ex, ey, ta, 78, 90, 2600, "#FFD1EC", { life: 1.1, w: 9 });
        if (ta < 0.5) { const u = ta / 0.5; smear(c, ex, ey, ex + 500 * u, ey + 700 * u, R, PAL[CC].glow, 0.8 * (1 - u)); }
      }
    });
    if (lb < 3) callout(c, "BREACH", CC, ageB(lb, 0.6), 520, { size: 150, dur: 1.5, jpx: 240 });
    const im = impactMode(lb, TIP, ["k", "i", "n", "i"]) || impactMode(lb, 6.5, ["n"]);
    if (im) applyImpact(c, im);
    if (lb > 11.5) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); speedLines(c, Math.PI / 2, 90, "#ffffff", 19, clamp((lb - 11.5) / 0.5), lt, 7000); c.restore(); }
  });
  VENTS.forEach(v => { cue(36 + v[4] - 0.12, "scythe_swing"); cue(36 + v[4], "wall_tear", { size: v[3] }); });
  cue(36.6, "callout");
  JETS.forEach(([i, b]) => cue(36 + b, "heat_jet", { size: VENTS[i][3] }));
  cue(41, "charge", { dur: 1.5 * BEAT });
  cue(41.05, "callout");
  cue(42.5, "beam_fire", { dur: 3.4 * BEAT });
  cue(45, "hit_huge"); cue(45.02, "explosion");
  cue(47.5, "whoosh_out", { dur: 0.5 * BEAT });
}

/* ============================================================ SCOUR 48-60
   Rick's §1: a purple tornado crackling with electricity; it paths along the
   bottom of the arena, sucks up enemy projectiles, and a foe caught in it is
   dragged into rapid ticks of damage. His reference: a neon-purple
   cel-shaded funnel of stacked glowing bands, a halo ring, dark debris, a
   bright floor glow. */
{
  const DR = "umbral", CV = "dwarven", R = 66;
  const drHome = [770, 720], cvHome = [300, 1380];
  const SHELLS = [[0.2, [720, 760]], [0.55, [820, 690]], [0.9, [700, 650]], [3.3, [760, 720]], [3.6, [720, 700]], [3.9, [800, 740]], [4.2, [740, 700]]];
  const SUCK = 3.0;                                   // shells after this are eaten
  const baseX = b => lerp(880, 300, E.inOut(clamp((b - 3) / 3.2)));
  const BASE_Y = 1545, TOPH = 640;
  const caught = b => b >= 6.0 && b < 9.0;

  function funnel(c, cx, t, grow, alpha = 1) {
    const P = PAL[DR], hh = TOPH * grow;
    c.save(); c.globalAlpha = alpha;
    glow(c, cx, BASE_Y, 360, P.core, 0.9);                               // bright floor glow
    c.beginPath(); c.ellipse(cx, BASE_Y, 170 * grow, 40 * grow, 0, 0, TAU); c.fillStyle = hexA(P.glow, 0.7); c.fill();
    const N = 26, wob = f => 38 * Math.sin(f * 5 - t * 4) * f;
    const rx = f => lerp(55, 270, Math.pow(f, 1.25)) * (0.4 + 0.6 * grow);
    // the body: a dark violet silhouette, inked
    c.beginPath();
    for (let i = 0; i <= N; i++) { const f = i / N; c.lineTo(cx + wob(f) - rx(f), BASE_Y - f * hh); }
    for (let i = N; i >= 0; i--) { const f = i / N; c.lineTo(cx + wob(f) + rx(f), BASE_Y - f * hh); }
    c.closePath(); c.fillStyle = INK; c.fill();
    c.save(); c.clip();
    c.fillStyle = "#2a0c46"; c.fillRect(cx - 600, BASE_Y - hh - 100, 1200, hh + 200);
    // stacked glowing bands scrolling up
    for (let i = 0; i < N; i++) {
      const f = ((i / N) + t * 0.55) % 1, y = BASE_Y - f * hh, r0 = rx(f), band = i % 3;
      c.strokeStyle = band === 0 ? "#ffffff" : band === 1 ? P.glow : P.core;
      c.lineWidth = band === 0 ? 5 : 12; c.globalAlpha = 0.9 * alpha;
      c.beginPath(); c.ellipse(cx + wob(f), y, r0, r0 * 0.2, 0, 0.1, Math.PI - 0.1); c.stroke();
    }
    c.fillStyle = "rgba(0,0,0,0.3)"; c.fillRect(cx + 40, BASE_Y - hh - 100, 600, hh + 200);   // cel shadow side
    c.restore();
    // halo ring at the crown
    const ty = BASE_Y - hh, tr = rx(1);
    c.lineWidth = 16; c.strokeStyle = INK; c.beginPath(); c.ellipse(cx + wob(1), ty, tr * 1.15, tr * 0.26, 0, 0, TAU); c.stroke();
    c.lineWidth = 8; c.strokeStyle = P.glow; c.stroke(); glow(c, cx + wob(1), ty, tr * 1.3, P.core, 0.7);
    // debris, orbiting
    for (let i = 0; i < 18; i++) {
      const f = 0.15 + 0.8 * h2(i, 3), a = t * (5 + 3 * h2(i, 4)) + i, y = BASE_Y - f * hh + Math.sin(a) * rx(f) * 0.2;
      const x = cx + wob(f) + Math.cos(a) * rx(f) * 1.1, s = 8 + 14 * h2(i, 5);
      c.fillStyle = Math.sin(a) > 0 ? "#120618" : "#3a1a52"; c.beginPath(); c.moveTo(x - s, y); c.lineTo(x, y - s * 0.7); c.lineTo(x + s * 0.8, y + s * 0.2); c.lineTo(x - s * 0.2, y + s * 0.6); c.closePath(); c.fill();
    }
    // electricity, re-struck every other frame
    const tq = Math.floor(t * 12);
    for (let k = 0; k < 4; k++) {
      const f0 = h3(k, tq, 1), f1 = clamp(f0 + 0.2 * (h3(k, tq, 2) - 0.2));
      const x0 = cx + wob(f0) + (h3(k, tq, 3) - 0.5) * 2 * rx(f0), x1 = cx + wob(f1) + (h3(k, tq, 4) - 0.5) * 2 * rx(f1);
      lightning(c, x0, BASE_Y - f0 * hh, x1, BASE_Y - f1 * hh, tq * 7 + k, P.core, 6, 0.3);
    }
    c.restore();
  }
  function shell(c, x, y, h, t) {
    c.save(); c.globalAlpha = 0.45; c.fillStyle = "#000"; c.beginPath(); c.ellipse(x, y + 10, 30, 12, 0, 0, TAU); c.fill(); c.restore();
    const s = 1 + h / 500, py = y - h * 0.9;
    c.save(); c.translate(x, py); c.scale(s, s);
    glow(c, 0, 0, 80, "#FF7A1A", 0.5);
    c.beginPath(); c.arc(0, 0, 26, 0, TAU); c.fillStyle = INK; c.fill();
    c.beginPath(); c.arc(0, 0, 21, 0, TAU); c.fillStyle = "#5a5e66"; c.fill();
    c.fillStyle = "#2c2e33"; c.beginPath(); c.arc(4, 4, 18, 0, TAU); c.fill();
    c.fillStyle = "#FF7A1A"; c.fillRect(-21, -4, 42, 8);
    c.fillStyle = "#fff"; c.beginPath(); c.arc(-8, -9, 5, 0, TAU); c.fill();
    c.fillStyle = h2(Math.floor(t * 24), 3) > 0.5 ? "#FFF1C1" : "#FF7A1A"; c.beginPath(); c.arc(0, -28, 7, 0, TAU); c.fill();
    c.restore();
  }

  scene(48, 60, "scour", (c, lt, lb, t) => {
    const lq = Math.floor(lb * 5 + 1e-6) / 5;
    // ---------------------------------------------- 2-3: the cut-in
    if (lb >= 2 && lb < 3) {
      const age = ageB(lb, 2);
      cutInPlate(c, DR, lt, 70, { fx: 540, fy: 860, fr: 360 });
      const s = 1 + 0.08 * age;
      c.save(); c.translate(540, 860); c.scale(s, s); c.translate(-540, -860);
      drawRelic(c, 560, 860, 240, DR, "scythe", -2.2 + 0.3 * age, { t: lt, fill: 0.55, aura: 0.9, w: { t: lt, moon: 1, glint: clamp(1 - Math.abs(age - 0.25) / 0.1), glintX: 240 * 1.5, glintY: -240 * 2.1 } });
      c.restore();
      callout(c, "SCOUR", DR, age - 0.03, 1400, { size: 160, dur: 1.0, jpx: 220 });
      if (age < 0.08) flash(c, "#ffffff", 1 - age / 0.08);
      return;
    }
    const tb = lb >= 3 ? baseX(lb) : 880, grow = lb >= 3 ? E.outBack(clamp((lb - 3) / 0.6)) : 0;
    const col = ageB(lb, 9);                           // the collapse
    let cam;
    if (lb < 2) cam = { x: 540, y: 1060, z: 1.3, rot: -0.04, t: lt, shake: 0 };
    else if (lb < 6) cam = { x: lerp(620, 420, clamp((lb - 3) / 3)), y: 1180, z: 1.05, rot: 0.03, t: lt, shake: 18 * grow };
    else if (lb < 9) cam = { x: 360, y: 1200, z: 1.55 + 0.1 * (lb - 6), rot: -0.08, t: lt, shake: 22 };
    else cam = { x: lerp(360, 560, E.outCubic(clamp(col / 1.2))), y: lerp(1200, 1000, E.outCubic(clamp(col / 1.2))), z: lerp(1.85, 1.0, E.outCubic(clamp(col / 1.2))), rot: 0, t: lt, shake: 80 * Math.exp(-col * 3) };
    inArena(c, DR, cam, lt, () => {
      // Duskreave, at its post
      drawRelic(c, drHome[0], drHome[1], R, DR, "scythe", lb >= 3 ? 1.9 : -0.5, { t: lt, fill: 0.6, aura: lb >= 3 && lb < 9 ? 0.5 : 0, w: { t: lt, moon: 1 } });
      // Culverin: lobbing, then caught, then thrown
      let cvP = cvHome, cvA = -0.7;
      if (caught(lb)) {
        const u = clamp((lb - 6) / 0.6), a = lt * 9;
        cvP = [tb + Math.cos(a) * 110 * u, lerp(cvHome[1], 1130, E.outCubic(u)) + Math.sin(a) * 25 * u]; cvA = lt * 14;
      } else if (lb >= 9) {
        const u = E.outCubic(clamp(col / 0.5)); cvP = [lerp(tb, 150, u), lerp(1130, 700, u)]; cvA = col * 30;
      }
      if (lb >= 9 && col < 0.5) smear(c, tb, 1130, cvP[0], cvP[1], R, PAL[CV].glow, 0.7);
      const behind = caught(lb) && Math.sin(lt * 9) < 0;
      if (behind) drawRelic(c, cvP[0], cvP[1], R, CV, "staff", cvA, { t: lt, fill: 0.55 - 0.3 * clamp((lb - 6) / 3), w: { t: lt } });
      if (lb >= 3 && lb < 9.5) funnel(c, tb, lt, grow, lb < 9 ? 1 : 1 - clamp(col / 0.25));
      if (!behind) drawRelic(c, cvP[0], cvP[1], R, CV, "staff", cvA, { t: lt, fill: lb >= 6 ? 0.55 - 0.3 * clamp((lb - 6) / 3) : 0.7, w: { t: lt } });
      if (caught(lb)) {                                   // the ticks: seven a second
        const n = Math.floor((lb - 6.2) * BEAT * 7);
        for (let k = Math.max(0, n - 2); k <= n; k++) {
          const a = (lb - 6.2) * BEAT - k / 7; if (a < 0 || a > 0.25) continue;
          const hx = cvP[0] + (h2(k, 1) - 0.5) * 80, hy = cvP[1] + (h2(k, 2) - 0.5) * 80;
          celBurst(c, hx, hy, 80, a, 0.16, ["#ffffff", PAL[DR].glow, PAL[DR].core, PAL[DR].dark], k);
          slam(c, "5", hx + 40, hy - 60 - a * 200, 54, a, { out: 0.18, fill: PAL[DR].glow, skew: -0.1, from: 1.8 });
        }
        lightning(c, tb, 1000, cvP[0], cvP[1], Math.floor(lt * 12), PAL[DR].core, 8, 0.2);
      }
      // the shells: lobbed at Duskreave; after the tornado rises they are eaten
      SHELLS.forEach(([lbS, tgt], i) => {
        const a = ageB(lb, lbS); if (a < 0) return;
        const src = [cvHome[0] + 230, cvHome[1] - 120], fl = 1.0;
        if (lbS < SUCK) {
          if (a < fl) { const u = a / fl; shell(c, lerp(src[0], tgt[0], u), lerp(src[1], tgt[1], u), 4 * 260 * u * (1 - u), lt); }
          else { celBurst(c, tgt[0], tgt[1], 170, a - fl, 0.4, ["#ffffff", "#FFD27A", "#FF7A1A", "#2a1606"], i + 300); sparks(c, tgt[0], tgt[1], a - fl, i + 310, 26, 1400, "#FFD27A", { life: 0.4 }); }
        } else {
          const cap = 0.3;
          if (a < cap) { const u = a / fl; shell(c, lerp(src[0], tgt[0], u), lerp(src[1], tgt[1], u), 4 * 260 * u * (1 - u), lt); }
          else if (a < 1.1) {
            const u0 = cap / fl, p0 = [lerp(src[0], tgt[0], u0), lerp(src[1], tgt[1], u0)], h0 = 4 * 260 * u0 * (1 - u0);
            const k = E.inOut(clamp((a - cap) / 0.8)), ang = lt * 10 + i, rr = 150 * (1 - k * 0.5);
            const sx = lerp(p0[0], tb + Math.cos(ang) * rr, k), sy = lerp(p0[1], BASE_Y - 150 - k * 380, k);
            shell(c, sx, sy, lerp(h0, 0, k), lt);
          } else if (a < 1.4) { const pa = a - 1.1, px = tb, py = BASE_Y - 560; celBurst(c, px, py, 90, pa, 0.25, ["#ffffff", PAL[DR].glow, PAL[DR].core, PAL[DR].dark], i + 400); }
        }
      });
      if (col > 0) {
        celBurst(c, tb, 1250, 620, col, 1.0, ["#ffffff", PAL[DR].glow, PAL[DR].core, "#16061f"], 500);
        shockRing(c, tb, 1350, 1200 * E.outExpo(col / 0.8), 60 * (1 - col / 0.8), PAL[DR].glow, 1 - col / 0.8, 0.5);
        sparks(c, tb, 1250, col, 501, 90, 2400, PAL[DR].glow, { life: 1.0, w: 8 });
      }
      if (lb >= 3 && lb < 3.6) { const a = ageB(lb, 3); sparks(c, 880, BASE_Y, a, 600, 60, 1800, PAL[DR].glow, { ang: -Math.PI / 2, spread: 2.0, life: 0.6 }); }
    });
    const im = impactMode(lb, 9, ["p", "i", "n"]) || impactMode(lb, 3, ["i"]);
    if (im) applyImpact(c, im);
    if (lb > 11.5) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); speedLines(c, Math.PI, 90, "#ffffff", 29, clamp((lb - 11.5) / 0.5), lt, 7000); c.restore(); }
  });
  SHELLS.forEach(([b], i) => { cue(48 + b, "shell_lob"); if (b < SUCK) cue(48 + b + 1.0 / BEAT, "shell_burst"); else cue(48 + b + 1.1 / BEAT, "pop"); });
  cue(50, "cutin"); cue(50.03, "callout");
  cue(51, "tornado", { dur: 6.4 * BEAT });
  for (let k = 0; k < Math.floor(2.8 * BEAT * 7); k++) cue(48 + 6.2 + k / 7 / BEAT, "tick", { k });
  cue(57, "hit_huge"); cue(57.02, "explosion");
  cue(59.5, "whoosh_out", { dur: 0.5 * BEAT });
}

/* ============================================================ GARROTE 60-66
   "Holds the foe where it stands, then throws it and consumes Hemorrhage."
   Rick's §1: the hammer gains massive rotational speed and grows a barbed
   wire ring matching its hit range; a foe caught in the wire is held until
   the hammer comes around and connects — massive knockback, and the ring
   explodes. The foe coming in is Shroudmaul, reaching with its Grasp. */
{
  const RB = "bloodsworn", SM = "umbral", R = 70;
  const rbP = [540, 1080], RW = 275;
  const inAng = -2.35, smHold = [rbP[0] + Math.cos(inAng) * (RW + 40), rbP[1] + Math.sin(inAng) * (RW + 40)];
  const CONNECT = 3.5, SNAG = 2.0;
  /* The hammer's angle: accelerating, then the slow-motion wind before it
     comes around onto the held foe at CONNECT, then a long spin-down. */
  function hammerAng(lb) {
    const s = lb * BEAT;
    if (lb < SNAG) return 2 * Math.PI * (0.4 * s + 1.1 * s * s);
    const a0 = hammerAng(SNAG - 1e-4), target = inAng + 2 * Math.PI * Math.ceil((a0 - inAng) / (2 * Math.PI) + 1);
    if (lb < CONNECT) { const u = (lb - SNAG) / (CONNECT - SNAG); return lerp(a0, target, 0.35 * u + 0.65 * Math.pow(u, 5)); }
    return target + 3.2 * (1 - Math.exp(-(lb - CONNECT) * BEAT * 2.2));
  }
  function wire(c, x, y, r, t, a) {
    c.save(); c.globalAlpha = a; c.translate(x, y); c.rotate(t * 0.8);
    for (const [lw, col] of [[12, INK], [5, "#b9b3bf"]]) for (let s = 0; s < 2; s++) {
      c.beginPath(); for (let i = 0; i <= 120; i++) { const q = i / 120 * TAU, rr = r + 5 * Math.sin(q * 30 + s * Math.PI); c.lineTo(Math.cos(q) * rr, Math.sin(q) * rr); } c.strokeStyle = col; c.lineWidth = lw; c.stroke();
    }
    for (let i = 0; i < 28; i++) {              // barbs
      const q = i / 28 * TAU, bx = Math.cos(q) * r, by = Math.sin(q) * r;
      c.strokeStyle = INK; c.lineWidth = 7; c.beginPath(); c.moveTo(bx - 12, by - 12); c.lineTo(bx + 12, by + 12); c.moveTo(bx + 12, by - 12); c.lineTo(bx - 12, by + 12); c.stroke();
      c.strokeStyle = i % 4 ? "#d8d2dc" : PAL[RB].core; c.lineWidth = 3; c.stroke();
    }
    glow(c, 0, 0, r * 1.3, PAL[RB].core, 0.25);
    c.restore();
  }
  function ghostHand(c, x, y, ang, s, a, t) {
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s); c.globalAlpha = a;
    glow(c, 60, 0, 190, PAL[SM].core, 0.8);
    c.lineCap = "round"; c.lineJoin = "round";
    const bone = (pts, w) => { for (const [lw, col] of [[w + 10, hexA("#1a0830", 0.9)], [w, PAL[SM].glow], [w * 0.35, "#ffffff"]]) { c.strokeStyle = col; c.lineWidth = lw; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke(); } };
    const curl = 0.5 + 0.5 * Math.sin(t * 6);
    bone([[-40, 0], [40, 0]], 26);
    [-36, -12, 12, 36].forEach((yy, i) => bone([[40, yy * 0.6], [90, yy], [130, yy + curl * 10 * Math.sign(yy || 1)], [160, yy + curl * 25 * Math.sign(yy || 1)]], 14));
    bone([[20, 20], [50, 60], [80, 75]], 14);
    c.restore();
  }

  scene(60, 66, "garrote", (c, lt, lb, t) => {
    const ha = hammerAng(lb), ca = ageB(lb, CONNECT), sn = ageB(lb, SNAG);
    const ring = lb < CONNECT ? E.outBack(clamp((lb - 0.2) / 0.6)) : 0;
    let cam = { x: rbP[0], y: rbP[1] - 80, z: 1.15, rot: 0.05, t: lt, shake: 6 };
    if (lb >= SNAG && lb < CONNECT) { const u = E.inOut(clamp((lb - SNAG) / 0.8)); cam = { x: lerp(rbP[0], (rbP[0] + smHold[0]) / 2, u), y: lerp(rbP[1] - 80, (rbP[1] + smHold[1]) / 2, u), z: lerp(1.15, 1.75, u), rot: lerp(0.05, -0.12, u), t: lt, shake: sn < 0.15 ? 40 : 3 }; }
    if (ca > 0) cam = { x: lerp((rbP[0] + smHold[0]) / 2, 400, E.outCubic(clamp(ca / 1))), y: lerp((rbP[1] + smHold[1]) / 2, 820, E.outCubic(clamp(ca / 1))), z: lerp(1.75, 0.95, E.outCubic(clamp(ca / 0.8))), rot: -0.12 + 0.2 * E.outCubic(clamp(ca / 1)), t: lt, shake: 110 * Math.exp(-ca * 2.6) };
    inArena(c, RB, cam, lt, () => {
      // Shroudmaul comes in with its hand out
      let smP, handA = 0;
      if (lb < 1.0) smP = null;
      else if (lb < SNAG) { const u = E.inCubic(clamp((lb - 1) / (SNAG - 1))); smP = [lerp(-150, smHold[0], u), lerp(420, smHold[1], u)]; }
      else if (lb < CONNECT) smP = [smHold[0] + 4 * noise1(lt * 40, 1), smHold[1] + 4 * noise1(lt * 40, 2)];
      else { const u = E.outCubic(clamp(ca / 0.55)); smP = [lerp(smHold[0], -500, u), lerp(smHold[1], -300, u)]; }
      if (smP) {
        const toRB = Math.atan2(rbP[1] - smP[1], rbP[0] - smP[0]);
        if (lb < CONNECT) {
          const reach = lb < SNAG ? 1 : 1 - clamp((lb - SNAG) / 0.4);
          ghostHand(c, smP[0] + Math.cos(toRB) * 90, smP[1] + Math.sin(toRB) * 90, toRB, 1.0 * reach + 0.01, 0.9 * reach, lt);
          if (lb < SNAG) smear(c, smP[0] - Math.cos(toRB) * 500, smP[1] - Math.sin(toRB) * 500, smP[0], smP[1], R, PAL[SM].core, 0.5);
        }
        if (ca > 0 && ca < 0.6) smear(c, smHold[0], smHold[1], smP[0], smP[1], R * 1.1, PAL[RB].core, 0.9 * (1 - ca / 0.6));
        drawRelic(c, smP[0], smP[1], R, SM, "warhammer", toRB + 0.6, { t: lt, fill: lb < CONNECT ? 0.6 : 0.3, w: { t: lt, spikes: 1 } });
        if (lb >= SNAG && lb < CONNECT) {      // held in the wire, bleeding
          c.save(); c.strokeStyle = "#d8d2dc"; c.lineWidth = 5;
          for (let k = -1; k <= 1; k++) { c.beginPath(); c.arc(rbP[0], rbP[1], RW + k * 14, inAng - 0.45, inAng + 0.45); c.stroke(); }
          c.restore();
          for (let k = 0; k < 5; k++) { const a = ((lb - SNAG) * BEAT + k * 0.13) % 0.65; const dx = smP[0] + (h2(k, 1) - 0.5) * 70, dy = smP[1] + 30 + a * 300; c.fillStyle = PAL[RB].core; c.beginPath(); c.arc(dx, dy, 9 * (1 - a), 0, TAU); c.fill(); }
          sparks(c, smP[0], smP[1], sn, 700, 40, 1400, PAL[RB].glow, { life: 0.5 });
        }
      }
      // the hammer, spinning, with the drawn motion arc behind its head
      const spin = lb < SNAG ? clamp(lb / 1.4) : lb < CONNECT - 0.15 ? 0.25 : 1;
      if (lb < CONNECT + 1.5) {
        c.save(); c.translate(rbP[0], rbP[1]);
        const arcLen = 1.9 * spin;
        c.globalAlpha = 0.55; c.fillStyle = PAL[RB].core;
        c.beginPath(); c.arc(0, 0, R * 3.9, ha - arcLen, ha); c.arc(0, 0, R * 2.4, ha, ha - arcLen, true); c.closePath(); c.fill();
        c.globalAlpha = 0.9; c.strokeStyle = "#ffffff"; c.lineWidth = 6; c.beginPath(); c.arc(0, 0, R * 3.7, ha - arcLen * 0.7, ha); c.stroke();
        c.restore();
      }
      if (ring > 0) wire(c, rbP[0], rbP[1], RW * ring, lt, 1);
      drawRelic(c, rbP[0], rbP[1], R, RB, "warhammer", ha, { t: lt, fill: 0.6, aura: lb < CONNECT ? 0.35 + 0.3 * spin : 0.2, w: { t: lt, barbs: 1 } });
      if (ca > 0) {                              // the ring goes up
        celBurst(c, smHold[0], smHold[1], 480, ca, 0.9, ["#ffffff", PAL[RB].glow, PAL[RB].core, "#2a0409"], 800);
        shockRing(c, rbP[0], rbP[1], RW + 1400 * E.outExpo(ca / 0.9), 60 * (1 - ca / 0.9), PAL[RB].glow, 1 - ca / 0.9);
        for (let i = 0; i < 36; i++) {           // wire shrapnel
          const q = i / 36 * TAU, d = RW + 1300 * (1 - Math.exp(-ca * 3)) * (0.6 + 0.6 * h2(i, 9));
          const x = rbP[0] + Math.cos(q) * d, y = rbP[1] + Math.sin(q) * d, rot = q + ca * 12 * (h2(i, 3) - 0.5);
          c.save(); c.globalAlpha = clamp(1 - ca / 1.2); c.translate(x, y); c.rotate(rot); c.strokeStyle = INK; c.lineWidth = 10; c.beginPath(); c.moveTo(-26, 0); c.lineTo(26, 0); c.stroke(); c.strokeStyle = i % 3 ? "#d8d2dc" : PAL[RB].core; c.lineWidth = 4; c.stroke(); c.restore();
        }
        sparks(c, smHold[0], smHold[1], ca, 801, 100, 2800, PAL[RB].glow, { life: 1.0, w: 9 });
      }
    });
    callout(c, "GARROTE", RB, ageB(lb, 0.3), 470, { size: 140, dur: 1.6, jpx: 250 });
    if (lb >= CONNECT - 0.9 && lb < CONNECT) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); focusLines(c, W / 2, H / 2, 160, 380, "#ffffff", 40 + Math.floor(lt * 12), 0.75); c.restore(); }
    const im = impactMode(lb, CONNECT, ["R", "i", "r", "n", "i"]) || impactMode(lb, SNAG, ["r"]);
    if (im) applyImpact(c, im);
    if (lb > 5.5) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); speedLines(c, -0.4, 90, "#ffffff", 39, clamp((lb - 5.5) / 0.5), lt, 7000); c.restore(); }
  });
  cue(60, "spin_up", { dur: 2 * BEAT });
  cue(60.25, "wire_ring"); cue(60.3, "callout");
  cue(61, "grasp_reach", { dur: BEAT });
  cue(62, "snag");
  cue(62.2, "tension", { dur: 1.3 * BEAT });
  cue(63.35, "whoosh_in", { dur: 0.15 * BEAT });
  cue(63.5, "hit_huge"); cue(63.52, "explosion");
  cue(65.5, "whoosh_out", { dur: 0.5 * BEAT });
}
