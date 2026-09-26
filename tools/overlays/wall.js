// BULWARK, REDESIGNED (v77, Lightkeeper), second candidate: the ward becomes a WALL — a barrier of light
// perpendicular to the facing, `ahead` units in front of the ball, half-length `half`. Arrows that cross it die;
// a foe ball that touches it is shoved back along the wall's normal (shove) and cannot pass; every block
// banks ward (bankShot for an arrow, bankBall for a ball). The sword swings as ever.
// arms: B = the wall (blocks + shoves, no bank) · C = the wall + the bank
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const ahead = P.ahead ?? 50, half = P.half ?? 110, shove = P.shove ?? 500, bankShot = P.bankShot ?? 5, bankBall = P.bankBall ?? 10, cdBall = P.cdBall ?? 0.4;
  const bank = arm === "C";
  const Wd = AC.STATUS.ward;
  let cd = 0;
  const doBank = (n) => { if (!bank || !me.alive || n <= 0) return 0; const b0 = me.shield; me.shield = Math.min(Wd.cap, me.shield + n); me.shieldMax = Math.max(me.shieldMax, me.shield); me.apply("ward", 1); return me.shield - b0; };
  return {
    onCast(t){ cd = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.shieldSum = (S.shieldSum || 0) + me.shield;
      const ux = Math.cos(me.theta), uy = Math.sin(me.theta);          // the facing (the greatsword aims)
      const cx = me.x + ux * ahead, cy = me.y + uy * ahead;             // wall centre
      const px = -uy, py = ux;                                          // along the wall
      const ax = cx - px * half, ay = cy - py * half, bx = cx + px * half, by = cy + py * half;
      for (let i = m.shots.length - 1; i >= 0; i--){ const s = m.shots[i]; if (s.stuck) continue;
        if (H.segDist(s.x, s.y, ax, ay, bx, by) < (s.r || 6) + 6){ m.shots.splice(i, 1); S.arrows = (S.arrows || 0) + 1; S.banked = (S.banked || 0) + doBank(bankShot); } }
      cd -= dt;
      if (foe.alive && cd <= 0 && foe.pin <= 0 && H.segDist(foe.x, foe.y, ax, ay, bx, by) < H.R + 8){
        cd = cdBall; S.blocks = (S.blocks || 0) + 1;
        // shove along the wall's normal, away from the caster's side
        const side = ((foe.x - cx) * ux + (foe.y - cy) * uy) >= 0 ? 1 : -1;
        H.knock(foe, ux * side, uy * side, shove);
        S.banked = (S.banked || 0) + doBank(bankBall);
      }
    },
    end(){ S.f_shield = S.winFrames ? S.shieldSum / S.winFrames : 0; delete S.winFrames; delete S.shieldSum; },
  };
}
