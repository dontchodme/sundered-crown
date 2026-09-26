// THE SUN (v71, sanctified x flail): for the window the flail's HEAD is a sun. Its light is a disc of
// radius sunR around the head; a foe inside it takes smite (+1 stack every tickCd) and tickDmg; the
// caster gains blessing stacks while the light burns (blessPer every blessCd), i.e. is healed by its own light.
// TRAIL variant: the light is the head's PATH over the last trailLife seconds (discs of trailR), not a disc on the head.
// arms: B = smite only · C = smite + damage · D = the whole (smite + damage + blessing) · T = trail (smite + damage + blessing)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const sunR = P.sunR ?? 70, tickCd = P.tickCd ?? 0.4, tickDmg = P.tickDmg ?? 3, smitePer = P.smitePer ?? 1;
  const blessCd = P.blessCd ?? 1.0, blessPer = P.blessPer ?? 1, blessOnTick = P.blessOnTick ?? 0;
  const trailLife = P.trailLife ?? 1.5, trailR = P.trailR ?? 30, trailEvery = P.trailEvery ?? 0.05;
  const smite = true, dmg = arm !== "B", bless = arm === "D" || arm === "T", trail = arm === "T";
  let cd = 0, bcd = 0, pts = [], tAcc = 0;
  return {
    onCast(t){ cd = 0; bcd = 0; pts = []; tAcc = 0; },
    onFrame(t, dt, open){
      if (!open){ pts = []; return; }
      S.winFrames = (S.winFrames || 0) + 1;
      S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      cd -= dt; bcd -= dt;
      let lit = false;
      if (trail){
        tAcc += dt; if (tAcc >= trailEvery){ tAcc = 0; pts.push({ x: me.headX, y: me.headY, t }); }
        while (pts.length && t - pts[0].t > trailLife) pts.shift();
        if (foe.alive) for (const p of pts){ if (Math.hypot(foe.x - p.x, foe.y - p.y) < trailR + H.R){ lit = true; break; } }
      } else if (foe.alive){
        lit = Math.hypot(foe.x - me.headX, foe.y - me.headY) < sunR + H.R;
      }
      if (lit){
        S.lit = (S.lit || 0) + 1;
        if (cd <= 0){ cd = tickCd; S.ticks = (S.ticks || 0) + 1;
          if (smite){ foe.apply("smite", smitePer, me); S.stacks = (S.stacks || 0) + smitePer; }
          if (dmg){ S.dmg = (S.dmg || 0) + H.hurt(foe, tickDmg, me); }
          if (bless && blessOnTick && me.alive){ me.apply("blessing", blessPer, me); S.bless = (S.bless || 0) + blessPer; } }
      }
      if (bless && !blessOnTick && me.alive && bcd <= 0){ bcd = blessCd; me.apply("blessing", blessPer, me); S.bless = (S.bless || 0) + blessPer; }
    },
    onClose(){ pts = []; },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_litPct = S.winFrames ? 100 * (S.lit || 0) / S.winFrames : 0;
      delete S.winFrames; delete S.foeStk; delete S.lit; },
  };
}
