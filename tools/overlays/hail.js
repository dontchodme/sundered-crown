// QUARRELSTORM, REDESIGNED (v83, Ironhail): for the window iron falls — every dropCd a bolt drops from the top
// of the hall onto the foe's position at that instant and lands fallT later; if the foe is within hitR of the
// spot it takes dropDmg and sunder +1. arms: B = the hail (damage only) · C = the hail + sunder
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const dropCd = P.dropCd ?? 0.4, fallT = P.fallT ?? 0.55, hitR = P.hitR ?? 40, dropDmg = P.dropDmg ?? 5;
  const sunder = arm === "C";
  let cd = 0, drops = [];
  return {
    onCast(t){ cd = 0; },
    onFrame(t, dt, open){
      if (open){ cd -= dt; if (cd <= 0 && foe.alive){ cd = dropCd; drops.push({ x: foe.x, y: foe.y, at: t + fallT }); S.drops = (S.drops || 0) + 1; } }
      while (drops.length && drops[0].at <= t){ const d = drops.shift();
        if (foe.alive && Math.hypot(foe.x - d.x, foe.y - d.y) < hitR + H.R){ S.landed = (S.landed || 0) + 1; S.dmg = (S.dmg || 0) + H.hurt(foe, dropDmg, me); if (sunder){ foe.apply("sunder", 1, me); S.sunder = (S.sunder || 0) + 1; } } }
    },
    onClose(){ /* drops in the air still land */ },
  };
}
