/* ANIME TRAILER — the open: the clash, the crown, the seven. Beats 0-24. */
"use strict";

/* ============================================================ COLD OPEN 0-8
   Frame one is already moving: two relics rushing at each other on speed
   lines. The channel's own measurement says second one is where a fifth of
   every audience leaves — so there is no black, no logo, no wait. */
{
  const TS = "verdant", DR = "umbral", R = 120;
  const CT = [430, 1010], CD = [650, 910];            // where they meet
  const dir = Math.atan2(CD[1] - CT[1], CD[0] - CT[0]);
  const ux = Math.cos(dir), uy = Math.sin(dir);

  scene(0, 8, "cold open", (c, lt, lb, t) => {
    const lq = Math.floor(lb * 5 + 1e-6) / 5;         // on twos, in beats
    let cam = { x: 540, y: 960, z: 1, rot: 0.1, t: lt, shake: 0 };
    let tsP, drP, tsA = dir + 0.35, drA = dir + Math.PI - 0.35, aura = 0;

    if (lb < 1) {                                     // --- the rush
      const d = 330 * Math.pow(1 - lq, 1.3);
      tsP = [CT[0] - ux * d, CT[1] - uy * d]; drP = [CD[0] + ux * d, CD[1] + uy * d];
      cam.z = 1.15 + 0.1 * lb;
      // split plate: green lower-left, violet upper-right
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
      c.fillStyle = "#07030d"; c.fillRect(0, 0, W, H);
      c.save(); c.beginPath(); c.moveTo(0, 0); c.lineTo(W, 0); c.lineTo(W, 700); c.lineTo(0, 1300); c.closePath(); c.clip();
      c.fillStyle = mix(PAL[DR].dark, "#000", 0.3); c.fillRect(0, 0, W, H); speedLines(c, dir + Math.PI, 70, PAL[DR].core, 3, 0.55, lt, 6000); c.restore();
      c.save(); c.beginPath(); c.moveTo(0, 1300); c.lineTo(W, 700); c.lineTo(W, H); c.lineTo(0, H); c.closePath(); c.clip();
      c.fillStyle = mix(PAL[TS].dark, "#000", 0.3); c.fillRect(0, 0, W, H); speedLines(c, dir, 70, PAL[TS].core, 4, 0.55, lt, 6000); c.restore();
      c.restore();
      c.save(); camera(c, cam);
      smear(c, tsP[0] - ux * 700, tsP[1] - uy * 700, tsP[0], tsP[1], R, PAL[TS].core, 0.7);
      smear(c, drP[0] + ux * 700, drP[1] + uy * 700, drP[0], drP[1], R, PAL[DR].core, 0.7);
      drawRelic(c, tsP[0], tsP[1], R, TS, "twinblade", tsA, { t: lt, fill: 0.62, squash: 0.18, sqAng: dir, w: { t: lt } });
      drawRelic(c, drP[0], drP[1], R, DR, "scythe", drA, { t: lt, fill: 0.62, squash: 0.18, sqAng: dir, w: { t: lt, moon: 1 } });
      c.restore();
      return;
    }

    if (lb < 4) {                                     // --- the clash and the grind
      const g = lb - 1, gq = lq - 1;
      const push = 14 * Math.sin(gq * 5.1) + 6 * Math.sin(gq * 13.3);
      tsP = [CT[0] + ux * push, CT[1] + uy * push]; drP = [CD[0] + ux * push, CD[1] + uy * push];
      tsP[1] -= 40; drP[1] -= 40;
      cam.z = 1.05 + 0.2 * E.inOut(g / 3); cam.rot = 0.1 + 0.05 * g / 3; cam.shake = 60 * Math.exp(-g * 2.5) + 5;
      aura = 0.6 + 0.3 * Math.sin(g * 3);
      // plate: the two schools pushing against each other, split at the contact
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
      const split = 960 + 30 * Math.sin(gq * 5.1);
      c.fillStyle = mix(PAL[DR].core, "#000", 0.55); c.fillRect(0, 0, W, H);
      c.save(); c.beginPath(); c.moveTo(0, split + 340); c.lineTo(W, split - 340); c.lineTo(W, H); c.lineTo(0, H); c.closePath(); c.clip();
      c.fillStyle = mix(PAL[TS].core, "#000", 0.5); c.fillRect(0, 0, W, H);
      halftone(c, 200, 1600, 800, hexA(PAL[TS].dark, 1), 28, 0.5); c.restore();
      halftone(c, 900, 300, 800, hexA(PAL[DR].dark, 1), 28, 0.5);
      focusLines(c, 540, 900, 160, 330, "#ffffff", 7 + Math.floor(lt * 12), 0.7);
      c.restore();
      c.save(); camera(c, cam);
      const kx = 540, ky = 890;                       // where the blades cross
      glow(c, kx, ky, 700, "#ffffff", 0.5 * Math.exp(-g * 1.5) + 0.25);
      drawRelic(c, tsP[0], tsP[1], R, TS, "twinblade", -0.95, { t: lt, fill: 0.62, aura, w: { t: lt, glint: g < 0.3 ? 1 - g / 0.3 : 0 } });
      drawRelic(c, drP[0], drP[1], R, DR, "scythe", Math.PI + 0.55, { t: lt, fill: 0.62, aura, w: { t: lt, moon: 1 } });
      sparks(c, kx, ky, ageB(lb, 1), 11, 90, 3200, "#fff4b0", { life: 0.9, w: 9 });
      for (let k = 0; k < 30; k++) { const a0 = ageB(lb, 1.2 + k * 0.1); sparks(c, kx, ky, a0, 100 + k, 7, 1500, k % 2 ? PAL[TS].glow : PAL[DR].glow, { life: 0.45, w: 6, ang: -Math.PI / 2 + (k % 2 ? -0.9 : 0.9), spread: 1.6 }); }
      const sa = ageB(lb, 1);
      shockRing(c, kx, ky, 1500 * E.outExpo(sa / 0.6), 70 * (1 - sa / 0.6), "#ffffff", 1 - sa / 0.6);
      c.restore();
      vText(c, "決戦", 150, 440, 120, "#ffffff", clamp(ageB(lb, 2) / 0.1), { stroke: INK });
      const im = impactMode(lb, 1, ["i", "R", "i", "n"]);
      if (im) applyImpact(c, im); else if (g < 0.6) flash(c, "#ffffff", 0.7 * (1 - g / 0.6));
      return;
    }

    // --- blasted apart; they hit the walls; they wait
    const u = clamp((lb - 4) / 0.75), uq = clamp((lq - 4) / 0.75);
    const e = E.outCubic(uq);
    tsP = [lerp(CT[0], 250, e), lerp(CT[1] - 40, 1420, e)];
    drP = [lerp(CD[0], 830, e), lerp(CD[1] - 40, 480, e)];
    const hov = lb - 4.75;
    if (hov > 0) { tsP[1] += 12 * Math.sin(hov * 3); drP[1] += 12 * Math.sin(hov * 3 + 1); }
    cam.z = lerp(1.25, 0.94, E.outCubic(u)) + 0.04 * clamp(hov / 3.25); cam.rot = lerp(0.15, 0.0, E.outCubic(u));
    cam.shake = 50 * Math.exp(-Math.max(0, hov) * 3) * (hov > 0 ? 1 : 0.4);
    c.save(); camera(c, cam);
    drawArena(c, DR, lt);
    if (u < 1) {
      smear(c, CT[0], CT[1], tsP[0], tsP[1], R * 0.9, PAL[TS].core, 0.6);
      smear(c, CD[0], CD[1], drP[0], drP[1], R * 0.9, PAL[DR].core, 0.6);
    }
    const wa = ageB(lb, 4.75);
    celBurst(c, 150, 1500, 260, wa, 0.6, ["#ffffff", PAL[TS].glow, PAL[TS].core, "#12240f"], 21);
    celBurst(c, 930, 400, 260, wa, 0.6, ["#ffffff", PAL[DR].glow, PAL[DR].core, "#1a0b2a"], 22);
    sparks(c, 150, 1500, wa, 31, 40, 1600, PAL[TS].glow, { life: 0.6 });
    sparks(c, 930, 400, wa, 32, 40, 1600, PAL[DR].glow, { life: 0.6 });
    aura = hov > 0 ? clamp(hov / 1.5) * (0.8 + 0.2 * Math.sin(hov * 7)) : 0;
    drawRelic(c, tsP[0], tsP[1], R * 0.9, TS, "twinblade", -0.9, { t: lt, fill: 0.62, aura, w: { t: lt } });
    drawRelic(c, drP[0], drP[1], R * 0.9, DR, "scythe", Math.PI - 0.9 + 0.3, { t: lt, fill: 0.62, aura, w: { t: lt, moon: 1 } });
    c.restore();
    slam(c, "ONE CROWN.", W / 2, 960, 170, ageB(lb, 5.5), { out: 1.75, grad: [GOLD_L, GOLD, GOLD_D], inner: "#fff", shake: 3, maxW: 900 });
    applyImpact(c, impactMode(lb, 4, ["n", "i"]));
    if (lb > 7.4) flash(c, "#ffffff", E.inCubic(clamp((lb - 7.4) / 0.6)));
  });
  cue(0, "whoosh_in", { dur: BEAT });
  cue(1, "clash_big");
  cue(1.05, "grind", { dur: 3 * BEAT });
  cue(2, "taiko_hit");
  cue(4, "hit_big");
  cue(4.75, "wallslam");
  cue(5.5, "slam_text");
  cue(7.2, "reverse_whoosh", { dur: 0.8 * BEAT });
}

/* ============================================================ THE CROWN 8-16 */
{
  const CX = 540, CY = 860, S = 270;
  const cracks = [   // in crown units: each a jagged line
    [[-0.1, -0.9], [-0.05, -0.5], [-0.18, -0.1], [-0.08, 0.3], [-0.2, 0.55]],
    [[0.55, -0.7], [0.42, -0.35], [0.5, 0.05], [0.36, 0.55]],
    [[-0.62, -0.62], [-0.5, -0.2], [-0.6, 0.2], [-0.45, 0.55]],
  ];
  const crackAt = [1, 2, 2.5];
  const SH = 3;      // shatter beat (local)

  scene(8, 16, "crown", (c, lt, lb, t) => {
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
    const bg = c.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, "#1a0f05"); bg.addColorStop(0.6, "#07040a"); bg.addColorStop(1, "#000");
    c.fillStyle = bg; c.fillRect(0, 0, W, H);
    godRays(c, CX, -300, GOLD, lt, lb < SH ? 0.32 : 0.32 * Math.exp(-(lb - SH) * 1.2), 11);
    glow(c, CX, CY, 900, GOLD, lb < SH ? 0.35 : 0.35 * Math.exp(-(lb - SH)));
    for (let i = 0; i < 80; i++) {                    // gold dust
      const x = (h2(i, 3) * W + lt * 15 * (h2(i, 4) - 0.5)) % W, y = (h2(i, 5) * H - lt * 40 * h2(i, 6) + H * 3) % H;
      c.fillStyle = hexA(GOLD_L, 0.2 + 0.5 * h2(i, 7)); c.beginPath(); c.arc(x, y, 1 + 3 * h2(i, 8), 0, TAU); c.fill();
    }
    const cam = { x: 540, y: 960, z: 1 + 0.06 * Math.min(lb, SH) / SH, t: lt, shake: 0 };
    const sa = ageB(lb, SH);
    if (sa > 0) cam.shake = 40 * Math.exp(-sa * 4);
    camera(c, cam);
    const bob = 10 * Math.sin(lt * 1.6);
    if (lb < SH) {
      drawCrown(c, CX, CY + bob, S, lt, { gemGlow: 0.5 });
      // cracks: white-hot, growing over three frames each
      c.save(); c.translate(CX, CY + bob); c.scale(S * (0.92 + 0.08 * Math.cos(lt * 1.3)), S);
      cracks.forEach((cr, k) => {
        const a = ageB(lb, crackAt[k]); if (a < 0) return;
        const n = Math.min(cr.length, 1 + Math.floor(a / 0.04));
        c.lineJoin = "miter";
        for (const [lw, col] of [[0.05, GOLD_L], [0.018, "#ffffff"]]) {
          c.beginPath(); for (let i = 0; i < n; i++) i ? c.lineTo(cr[i][0], cr[i][1]) : c.moveTo(cr[i][0], cr[i][1]);
          c.strokeStyle = col; c.lineWidth = lw; c.stroke();
        }
        glow(c, cr[0][0], cr[0][1], 0.5, "#ffffff", 0.8 * Math.exp(-a * 5));
      });
      c.restore();
      const ca = Math.min(...crackAt.map(b => { const a = ageB(lb, b); return a < 0 ? 9 : a; }));
      if (ca < 0.12) cam.shake = 25;
    } else {
      // the seven shards fly apart, each taking its school's colour
      const fly = lb > 11 - 8 + 3 ? 0 : 0;   // (kept simple: one motion law)
      for (let k = 0; k < 7; k++) {
        const P = PAL[CROWN_GEMS[k]];
        const ang = -Math.PI / 2 + (k - 3) * 0.5 + (k % 2 ? 0.12 : -0.12);
        const d = 520 * (1 - Math.exp(-2.4 * sa)) + (lb > 6 ? 900 * E.inCubic(clamp((lb - 6) / 2)) : 0);
        const px = CX + Math.cos(ang) * d * 1.05, py = CY + bob + Math.sin(ang) * d * 0.9 + 140 * (k === 3 ? -0.2 : 0.4) * (1 - Math.exp(-sa));
        const sc = 1 + (lb > 6 ? 3 * E.inCubic(clamp((lb - 6) / 2)) : 0);
        smear(c, CX, CY, px, py, 50 * sc, P.core, 0.5 * Math.exp(-sa * 0.8));
        glow(c, px, py, 260 * sc, P.core, 0.7);
        c.save(); c.translate(px - CX, py - CY); c.translate(CX, CY); c.rotate((k - 3) * 0.25 * sa); c.scale(sc, sc); c.translate(-CX, -CY);
        drawCrown(c, CX, CY, S, 0, { clip: shardClip(k), flat: true, gemGlow: 0.8 });
        c.save(); c.translate(CX, CY); c.scale(S, S); shardClip(k)(c); crownPath(c); c.globalCompositeOperation = "source-atop";
        c.fillStyle = hexA(P.core, clamp(sa * 1.2) * 0.55); c.fill(); c.restore();
        c.restore();
      }
      sparks(c, CX, CY, sa, 71, 120, 3000, GOLD_L, { life: 1.0, w: 8 });
      shockRing(c, CX, CY, 1600 * E.outExpo(sa / 0.8), 90 * (1 - sa / 0.8), GOLD_L, 1 - sa / 0.8);
    }
    c.setTransform(1, 0, 0, 1, 0, 0);
    slam(c, "SHATTERED", W / 2, 1300, 150, ageB(lb, 4), { out: 2.6, fill: "#ffffff", shake: 2 });
    slam(c, "INTO SEVEN.", W / 2, 1450, 150, ageB(lb, 4.5), { out: 2.1, grad: [GOLD_L, GOLD, GOLD_D], shake: 2 });
    const im = impactMode(lb, SH, ["i", "n", "i"]);
    if (im) applyImpact(c, im); else if (sa > 0 && sa < 0.45) flash(c, "#ffffff", 0.8 * (1 - sa / 0.45));
    if (lb > 7.5) flash(c, "#ffffff", E.inCubic(clamp((lb - 7.5) / 0.5)) * 0.9);
  });
  cue(8, "crown_hum", { dur: 3 * BEAT });
  cue(9, "crack"); cue(10, "crack"); cue(10.5, "crack");
  cue(11, "shatter");
  cue(12, "slam_text"); cue(12.5, "slam_text");
  cue(14, "whoosh_out", { dur: 2 * BEAT });
}

/* ============================================================ THE SEVEN 16-24
   One relic a beat, one of every school AND one of every weapon — the roster
   happens to cover both axes with seven fighters, which is the point. */
{
  const CAST = [
    ["DAWNBRINGER", "sanctified", "greatsword", {}],
    ["RAVELBONE", "bloodsworn", "warhammer", { barbs: 1 }],
    ["CINDERCLEAVE", "dwarven", "scythe", {}],
    ["THORNSHEAR", "verdant", "twinblade", {}],
    ["GLOAMWIRE", "umbral", "bow", {}],
    ["PARADOX", "runic", "flail", {}],
    ["WATCHLIGHT", "vigil", "staff", {}],
  ];
  function panel(c, k, age, lt) {
    const [name, sc, wpn, wo] = CAST[k], P = PAL[sc];
    cutInPlate(c, sc, lt, 40 + k, { fx: 540, fy: 820, fr: 300, hx: k % 2 ? 200 : 880, hy: k % 2 ? 1500 : 300 });
    // a big pale numeral behind, like an episode card
    c.save(); c.font = `900 700px ${FONT}`; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = hexA("#ffffff", 0.1);
    c.fillText(String(k + 1), 540 + (k % 2 ? -260 : 260), 820); c.restore();
    const e = E.outExpo(clamp(age / 0.22));
    const x = 540 + (k % 2 ? -1 : 1) * 800 * (1 - e), y = 820;
    const r = 175;
    const ang = wpn === "bow" ? -0.25 : wpn === "staff" ? -0.55 : -0.75;
    smear(c, x + (k % 2 ? -1 : 1) * 600 * (1 - e) + (k % 2 ? -1 : 1) * 200, y, x, y, r * (1 - e * 0.6), P.core, 0.6 * (1 - e));
    drawRelic(c, x, y, r, sc, wpn, ang, { t: lt, fill: 0.6, aura: 0.35, w: Object.assign({ t: lt, glint: clamp(1 - Math.abs(age - 0.24) / 0.1) }, wo) });
    slam(c, name, W / 2, 1255, 150, age - 0.04, { fill: "#ffffff", outer: INK, inner: P.core, maxW: 940, letter: 2 });
    slam(c, `${P.name}  ·  ${wpn.toUpperCase()}`, W / 2, 1375, 46, age - 0.08, { skew: 0, fill: P.core === "#FFF6E2" ? "#FFD66B" : P.glow, ow: 0.3, iw: 0, letter: 8, from: 1.4 });
  }
  scene(16, 24, "the seven", (c, lt, lb, t) => {
    c.setTransform(1, 0, 0, 1, 0, 0);
    if (lb < 7) {
      const k = Math.floor(lb + 1e-6), age = (lb - k) * BEAT;
      // the wipe: the new panel cuts in on a diagonal over three frames
      const u = E.outCubic(clamp(age / 0.125));
      if (k > 0 && u < 1) { c.save(); panel(c, k - 1, BEAT, lt); c.restore(); }
      c.save();
      const edge = lerp(-500, W + 500, u);
      c.beginPath(); c.moveTo(-600, -100); c.lineTo(edge + 300, -100); c.lineTo(edge - 300, H + 100); c.lineTo(-600, H + 100); c.closePath(); c.clip();
      panel(c, k, age, lt);
      c.restore();
      if (u < 1 && k > 0) {        // the slash line itself
        c.save(); c.strokeStyle = "#fff"; c.lineWidth = 26; c.beginPath(); c.moveTo(edge + 300, -100); c.lineTo(edge - 300, H + 100); c.stroke(); c.restore();
      }
      if (k === 0 && age < 0.12) flash(c, "#ffffff", 1 - age / 0.12);
      return;
    }
    // beat 7: all seven at once, in slanted bands
    const age = (lb - 7) * BEAT;
    c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
    for (let i = 0; i < 7; i++) {
      const [name, sc, wpn, wo] = CAST[i], P = PAL[sc], bw = W / 7, x0 = i * bw;
      const drop = 1 - E.outExpo(clamp((age - i * 0.018) / 0.16));
      c.save(); c.translate(0, (i % 2 ? -1 : 1) * 1400 * drop);
      c.beginPath(); c.moveTo(x0 + 120, 0); c.lineTo(x0 + bw + 124, 0); c.lineTo(x0 + bw - 124, H); c.lineTo(x0 - 120, H); c.closePath();
      c.fillStyle = P.core; c.fill(); c.strokeStyle = INK; c.lineWidth = 10; c.stroke();
      c.clip(); halftone(c, x0 + bw / 2, 960, 900, hexA(P.dark, 1), 22, 0.4);
      drawOrb(c, x0 + bw / 2, 700 + (i % 2) * 180, 62, sc, { t: lt, fill: 0.6 });
      c.restore();
    }
    slam(c, "SEVEN SCHOOLS.", W / 2, 1300, 140, age - 0.05, { fill: "#ffffff", maxW: 980 });
  });
  for (let k = 0; k < 7; k++) cue(16 + k, "panel_hit", { k });
  cue(23, "hit_big"); cue(23, "slam_text");
  cue(23.6, "whoosh_out", { dur: 0.4 * BEAT });
}
