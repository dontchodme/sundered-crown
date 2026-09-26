// REBUTTAL (v70, runic x warhammer): for the window the walls are runed. Every time the foe's ball
// touches a wall it is FLUNG straight back at the caster at flingSpeed, hexed, and (optionally) bitten.
// arms: B = fling only · C = fling + hex · D = the whole (fling + hex + damage) · H = hex on wall touch only, no fling
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const flingSpeed = P.flingSpeed ?? 700, flingCd = P.flingCd ?? 0.5, hexPer = P.hexPer ?? 1, flingDmg = P.flingDmg ?? 4;
  const fling = arm === "B" || arm === "C" || arm === "D";
  const hex = arm === "C" || arm === "D" || arm === "H";
  const dmg = arm === "D";
  let cd = 0;
  return {
    onCast(t){ cd = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1;
      S.foeStk = (S.foeStk || 0) + foe.stacks("hex");
      cd -= dt;
      if (!foe.alive || foe.pin > 0 || cd > 0) return;
      const n = m.inset, R = H.R, e = 1.5;
      const onWall = foe.x <= n + R + e || foe.x >= H.W - n - R - e || foe.y <= n + R + e || foe.y >= H.Hh - n - R - e;
      if (!onWall) return;
      cd = flingCd; S.flings = (S.flings || 0) + 1;
      if (fling){
        const dx = me.x - foe.x, dy = me.y - foe.y, d = Math.hypot(dx, dy) || 1;
        foe.vx = dx / d * flingSpeed; foe.vy = dy / d * flingSpeed;
      }
      if (hex){ foe.apply("hex", hexPer, me); S.stacks = (S.stacks || 0) + hexPer; }
      if (dmg){ S.dmg = (S.dmg || 0) + H.hurt(foe, flingDmg, me); }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
