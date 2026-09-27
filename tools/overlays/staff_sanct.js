// THE SANCTIFIED STAFF (v95). Bow body, spell instead of an arrow:
//   spell   LANCE   — a needle of light, the fastest shot in the game (speed 560, r 16, life 2.5) that CANNOT BE PARRIED: it passes the foe's blade
//                     and lands only on the ball (the overlay owns the ball test; the engine sees a shot of r 1 that is armed, so neither its blade test nor its ball test reaches it)
//   ult     SANCTUM — for the window a ring of holy ground (r `R`) travels with the caster: a foe inside it is REPELLED (accel `push` px/s^2 outward),
//                     smitten +1 and burned for `tick` every `every` s, and while a foe stands in it the caster is blessed +1 every `blessEvery` s
// arms: Z = spell + RADIANCE — for the window every lance GROWS as it flies: r `gR0`->`gR1` and dmgMul 1->`gMul` over `gT` s of flight (a needle that blooms into a shaft the farther it goes); no ground, no heal
// arms: S = spell only · U = spell + Sanctum · W = plain bow shot + Sanctum · X = spell + Sanctum with no push (the ground alone) · Y = spell + Sanctum with no heal
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.34, speed: P.speed ?? 560, r: P.r ?? 16, life: P.life ?? 2.5, grav: 0, dmgMul: 1.0 });
  const R = P.R ?? 170, push = arm === "X" ? 0 : (P.push ?? 600), tick = P.tick ?? 1.5, every = P.every ?? 0.4, blessEvery = P.blessEvery ?? 0.5, heal = arm !== "Y";
  const ult = arm === "U" || arm === "W" || arm === "X" || arm === "Y";
  const grow = arm === "Z", gR0 = P.gR0 ?? 16, gR1 = P.gR1 ?? 60, gMul = P.gMul ?? 2.5, gT = P.gT ?? 1.0;
  const seen = new WeakSet(); let nextTick = 0, nextBless = 0, hits = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ nextTick = t; nextBless = t; hits = me.hits; },
    onFrame(t, dt, open){
      for (const s of fresh()){ if (spell){ s.arm = 99; s.lance = true; s.lr = s.r; s.r = 1; if (grow && open){ s.grow = true; s.born = t; S.grown = (S.grown || 0) + 1; } } }  // r 1 for the engine: the blade test cannot reach it; the ball test below uses the true radius
      if (spell) for (let i = m.shots.length - 1; i >= 0; i--){
        const s = m.shots[i];
        if (s.own !== side || !s.lance) continue;
        if (s.grow){ const k = Math.min(1, (t - s.born) / gT); s.lr = gR0 + (gR1 - gR0) * k; s.dmgMul = 1 + (gMul - 1) * k; }
        if (foe.alive && me.alive && Math.hypot(s.x - foe.x, s.y - foe.y) < H.R + s.lr){
          const bl = Math.hypot(s.vx, s.vy) || 1;
          const seg = { ax: s.x - s.vx / bl * 10, ay: s.y - s.vy / bl * 10, bx: s.x + s.vx / bl * 10, by: s.y + s.vy / bl * 10, a: s.a };
          m.shotHits++; m._cineShot = s; m.resolveHit(me, foe, s.x, s.y, seg, s.dmgMul, s.over); m._cineShot = null;
          m.shots.splice(i, 1); S.lanceHits = (S.lanceHits || 0) + 1;
        }
      }
      if (!ult || !open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      const dx = foe.x - me.x, dy = foe.y - me.y, d = Math.hypot(dx, dy) || 1;
      const inside = foe.alive && d < R + H.R;
      if (inside){
        S.inFrames = (S.inFrames || 0) + 1;
        if (push > 0 && !(foe.pin > 0)){ foe.vx += dx / d * push * dt; foe.vy += dy / d * push * dt; }
        if (t >= nextTick){ nextTick = t + every; const dd = H.hurt(foe, tick, me); foe.apply("smite", 1, me); S.burn = (S.burn || 0) + dd; }
        if (heal && t >= nextBless){ nextBless = t + blessEvery; me.apply("blessing", 1, me); S.bless = (S.bless || 0) + 1; }
      }
      if (me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){},
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_inShare = S.winFrames ? (S.inFrames || 0) / S.winFrames : 0; delete S.winFrames; delete S.foeStk; delete S.inFrames; },
  };
}
