// BASTION (v72, vigil x flail): for the window the flail's head is the caster's SHIELD — a ward disc of
// radius headR0 + bankR x shield. A foe blade that strikes the disc is PARRIED (weapon stun parryStun,
// the foe's ball shoved back) and every parry BANKS ward on the caster (bankPer). Arrows that touch the
// disc die. The head's own blow is unchanged.
// arms: B = parry only (no bank) · C = bank only (no parry effect) · D = the whole
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const headR0 = P.headR0 ?? 40, bankR = P.bankR ?? 0.5, parryStun = P.parryStun ?? 0.25, parryKnock = P.parryKnock ?? 250;
  const bankPer = P.bankPer ?? 8, parryCd = P.parryCd ?? 0.3, killShots = P.killShots ?? 1;
  const parry = arm === "B" || arm === "D", bank = arm === "C" || arm === "D";
  const Wd = AC.STATUS.ward;
  let cd = 0;
  return {
    onCast(t){ cd = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1;
      S.shieldSum = (S.shieldSum || 0) + me.shield;
      cd -= dt;
      const r = headR0 + bankR * me.shield;
      S._rk = Math.max(S._rk || 0, r);
      if (killShots) for (let i = m.shots.length - 1; i >= 0; i--){ const s = m.shots[i];
        if (s.stuck || s.own === (me === m.a ? "a" : "b")) continue;
        if (Math.hypot(s.x - me.headX, s.y - me.headY) < r + (s.r || 6)){ m.shots.splice(i, 1); S.arrows = (S.arrows || 0) + 1; } }
      if (!foe.alive || cd > 0 || foe.stun > 0) return;
      const segs = m.bladeSegments(foe);
      let hit = false;
      for (const sg of segs){ if (H.segDist(me.headX, me.headY, sg.ax, sg.ay, sg.bx, sg.by) < r){ hit = true; break; } }
      if (!hit) return;
      cd = parryCd; S.parries = (S.parries || 0) + 1;
      if (parry){ foe.stun = Math.max(foe.stun, parryStun); m.breakSpin(foe, "parried by the bastion", parryStun);
        H.knock(foe, foe.x - me.headX, foe.y - me.headY, parryKnock); }
      if (bank && me.alive){ const b0 = me.shield; me.shield = Math.min(Wd.cap, me.shield + bankPer); me.shieldMax = Math.max(me.shieldMax, me.shield);
        me.apply("ward", 1); S.banked = (S.banked || 0) + (me.shield - b0); }
    },
    onClose(){ if (S._rk){ S.rPeak = (S.rPeak || 0) + S._rk; delete S._rk; } },
    end(){ if (S._rk) delete S._rk; S.f_shield = S.winFrames ? S.shieldSum / S.winFrames : 0; delete S.winFrames; delete S.shieldSum; },
  };
}
