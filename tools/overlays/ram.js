// RAM (v72, vigil x flail, third candidate): for the window the caster's BALL is the weapon — the ward
// hardens the shell and the ball charges the foe (accel toward the foe, capped at speedMax). A ball-to-ball
// contact is a RAM: ramDmg + ramShield x current shield to the foe, knock ramKnock, and banks ramBank ward.
// The head still swings. arms: B = ram on contact only (no charge) · C = charge + ram · D = charge + ram + bank
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const accel = P.accel ?? 600, ramDmg = P.ramDmg ?? 10, ramShield = P.ramShield ?? 0.25, ramKnock = P.ramKnock ?? 500, ramBank = P.ramBank ?? 8, ramCd = P.ramCd ?? 0.5;
  const charge = arm === "C" || arm === "D", bank = arm === "D";
  const Wd = AC.STATUS.ward, vmax = AC.CONFIG.physics.speedMax;
  let cd = 0;
  return {
    onCast(t){ cd = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.shieldSum = (S.shieldSum || 0) + me.shield;
      cd -= dt;
      if (!foe.alive || !me.alive) return;
      const dx = foe.x - me.x, dy = foe.y - me.y, d = Math.hypot(dx, dy) || 1;
      if (charge && me.pin <= 0){ me.vx += dx / d * accel * dt; me.vy += dy / d * accel * dt;
        const v = Math.hypot(me.vx, me.vy); if (v > vmax){ me.vx *= vmax / v; me.vy *= vmax / v; } }
      if (cd <= 0 && d < 2 * H.R + 3){
        cd = ramCd; S.rams = (S.rams || 0) + 1;
        S.dmg = (S.dmg || 0) + H.hurt(foe, ramDmg + ramShield * me.shield, me);
        H.knock(foe, dx, dy, ramKnock);
        if (bank){ const b0 = me.shield; me.shield = Math.min(Wd.cap, me.shield + ramBank); me.shieldMax = Math.max(me.shieldMax, me.shield); me.apply("ward", 1); S.banked = (S.banked || 0) + (me.shield - b0); }
      }
    },
    end(){ S.f_shield = S.winFrames ? S.shieldSum / S.winFrames : 0; delete S.winFrames; delete S.shieldSum; },
  };
}
