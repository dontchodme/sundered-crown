// EXSANGUINATE, REDESIGNED (v76, Widowmaker): for the window the foe's bleed DRAINS INTO Widowmaker — every
// hemorrhage tick on the foe heals her by drainMul x the tick — and her blows carry lifesteal (the engine's
// own field). arms: B = the drain only · C = lifesteal only · D = both · SHIP = the nova as shipped · A = nothing
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const drainMul = P.drainMul ?? 1.0, steal = P.steal ?? 0.35, ls0 = me.lifesteal;
  const drain = arm === "B" || arm === "D", lifesteal = arm === "C" || arm === "D";
  const Hm = AC.STATUS.hemorrhage;
  return {
    onCast(t){ if (lifesteal) me.lifesteal = steal; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hemorrhage");
      if (drain && me.alive && foe.alive){ const st = foe.stacks("hemorrhage");
        if (st > 0){ const tick = Hm.dps * st * dt * foe.dmgTakenMul() * drainMul; const hp0 = me.hp; me.hp = Math.min(me.maxHp || me.hp + tick, me.hp + tick); S.drained = (S.drained || 0) + (me.hp - hp0); } }
    },
    onClose(){ me.lifesteal = ls0; },
    end(){ me.lifesteal = ls0; S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
