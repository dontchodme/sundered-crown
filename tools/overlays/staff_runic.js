// THE RUNIC STAFF (v94). Bow body, spell instead of an arrow:
//   spell   GLYPH    — a rune bolt (speed 380, r 22) that, when it reaches a wall, STOPS there and hangs as a SIGIL for `sigilLife` s;
//                      a foe that touches a sigil takes the blow and is hexed `sigilHex` (a bolt that lands in flight hexes 1, the channel)
//   ult     SEQUENCE — at cast every sigil on the walls detonates in the order it was laid, `gap` s apart (r `popR`, `popDmg`, hex `popHex`);
//                      for the window every NEW sigil detonates `fuse` s after it is laid
// arms: Y = spell + CONVERGENCE (the sigils fly at the foe instead of detonating; in-window sigils launch after `fuse`) · Z = Y with cHome 6
// arms: S = spell only · U = spell + Sequence · W = plain bow shot + a nova on cast (the pop with no sigils: r popR at the caster, for the decomposition) · X = spell + Sequence with popR 220
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.34, speed: P.speed ?? 380, r: P.r ?? 22, life: P.life ?? 3.4, grav: 0, dmgMul: 1.0 });
  const sigilLife = P.sigilLife ?? 4.0, sigilHex = P.sigilHex ?? 2, sigilR = P.sigilR ?? 22;
  const gap = P.gap ?? 0.25, popR = arm === "X" ? 220 : (P.popR ?? 150), popDmg = P.popDmg ?? 6, popHex = P.popHex ?? 2, fuse = P.fuse ?? 0.5;
  const ult = arm === "U" || arm === "X" || arm === "W" || arm === "Y" || arm === "Z";
  const seen = new WeakSet(); let queue = [], hits = 0, open_ = false;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  function pop(x, y){
    S.pops = (S.pops || 0) + 1;
    if (foe.alive && Math.hypot(foe.x - x, foe.y - y) < popR + H.R){ const d = H.hurt(foe, popDmg, me); foe.apply("hex", popHex, me); S.popDmg = (S.popDmg || 0) + d; S.popHits = (S.popHits || 0) + 1; }
  }
  // CONVERGENCE (arms Y, Z): the sigil leaves the wall and flies at the foe — homing `cHome` at `cV`, life `cLife`; its hit is the sigil's (hex sigilHex)
  const cHome = arm === "Z" ? 6 : (P.cHome ?? 3), cV = P.cV ?? 380, cLife = P.cLife ?? 3.0, converge = arm === "Y" || arm === "Z";
  function launch(s){ if (!foe.alive) return; const a = Math.atan2(foe.y - s.y, foe.x - s.x); s.vx = Math.cos(a) * cV; s.vy = Math.sin(a) * cV; s.a = a; s.home = cHome; s.life = cLife; s.max = cLife; s.sigil = false; s.flown = true; delete s.fuse; S.launched = (S.launched || 0) + 1; }
  return {
    onCast(t){
      hits = me.hits; open_ = true;
      if (arm === "W"){ pop(me.x, me.y); return; }
      let k = 0;
      for (const s of m.shots) if (s.own === side && s.sigil && !s.fuse){ s.fuse = t + gap * (k++); }
      S.sigilsAtCast = (S.sigilsAtCast || 0) + k;
    },
    onFrame(t, dt, open){
      for (const s of fresh()){ if (spell){ s.bounce = 1; s.glyph = true; } }
      if (spell) for (const s of m.shots){
        if (s.own !== side || !s.glyph || s.sigil || s.flown) continue;
        if (s.bounce === 0){ s.sigil = true; s.vx = 0; s.vy = 0; s.grav = 0; s.life = sigilLife; s.max = sigilLife; s.r = sigilR; s.over = { onHit: { hex: sigilHex } }; s.laid = t; S.sigils = (S.sigils || 0) + 1; if (ult && open) s.fuse = t + fuse; }
      }
      if (!ult) return;
      if (open){ S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hex"); }
      for (let i = m.shots.length - 1; i >= 0; i--){ const s = m.shots[i]; if (s.own === side && s.sigil && s.fuse && t >= s.fuse){ if (converge) launch(s); else { pop(s.x, s.y); m.shots.splice(i, 1); } } }
      if (open && me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){ open_ = false; },
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
