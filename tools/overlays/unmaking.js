// UNMAKING, REDESIGNED (v79, Spellbreaker): for the window every hit Spellbreaker lands UNMAKES the foe's
// weapon — its reach shrinks by shrinkPer (of its own) per hit down to shrinkMin, restored when the window closes.
// arms: B = the shrink only · C = the shrink + an extra hex per hit
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const shrinkPer = P.shrinkPer ?? 0.12, shrinkMin = P.shrinkMin ?? 0.4, hexExtra = P.hexExtra ?? 1, stunMul = P.stunMul ?? 1;
  const Hx = AC.STATUS.hex, stun0 = Hx.stunFor;
  const hex = arm === "C" || arm === "D", shrink = arm !== "D";
  let hits = 0;
  return {
    onCast(t){ hits = me.hits; Hx.stunFor = stun0 * stunMul; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeReach = (S.foeReach || 0) + foe.reachMul;
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.unmade = (S.unmade || 0) + n;
        if (shrink) foe.reachMul = Math.max(shrinkMin, foe.reachMul - shrinkPer * n);
        if (hex && foe.alive){ foe.apply("hex", hexExtra * n, me); S.hex = (S.hex || 0) + hexExtra * n; } }
    },
    onClose(){ foe.reachMul = 1; Hx.stunFor = stun0; },
    end(){ foe.reachMul = 1; Hx.stunFor = stun0; S.f_foeReach = S.winFrames ? S.foeReach / S.winFrames : 1; delete S.winFrames; delete S.foeReach; },
  };
}
