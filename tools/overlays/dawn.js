// DAYBREAK, REDESIGNED (v86, Dawnbringer): the sun rises — a line of light climbs the hall from the floor to
// the top over the window. Everything BELOW the line is in the light: a foe there is smitten +1 and takes
// tickDmg every tickCd; Dawnbringer there is blessed +1 every blessCd. arms: B = smite + damage · C = B + the blessing
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const tickCd = P.tickCd ?? 0.5, tickDmg = P.tickDmg ?? 2, blessCd = P.blessCd ?? 1.0, riseFrom = P.riseFrom ?? 0.0, riseTo = P.riseTo ?? 1.0;
  const bless = arm === "C", blessIfLit = P.blessIfLit ?? 0;
  let t0 = 0, cd = 0, bcd = 0;
  return {
    onCast(t){ t0 = t; cd = 0; bcd = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      const k = Math.min(1, (t - t0) / P.dur);
      const lineY = H.Hh - (riseFrom + (riseTo - riseFrom) * k) * H.Hh;   // y grows downward; the line rises
      cd -= dt; bcd -= dt;
      if (foe.alive && foe.y > lineY){ S.foeLit = (S.foeLit || 0) + 1;
        if (cd <= 0){ cd = tickCd; foe.apply("smite", 1, me); S.dmg = (S.dmg || 0) + H.hurt(foe, tickDmg, me); S.ticks = (S.ticks || 0) + 1; } }
      const foeLitNow = foe.alive && foe.y > lineY;
      if (bless && me.alive && me.y > lineY && (!blessIfLit || foeLitNow) && bcd <= 0){ bcd = blessCd; me.apply("blessing", 1, me); S.bless = (S.bless || 0) + 1; }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_foeLitPct = S.winFrames ? 100 * (S.foeLit || 0) / S.winFrames : 0; delete S.winFrames; delete S.foeStk; delete S.foeLit; },
  };
}
