// RAMPART (v72, vigil x flail, second candidate): for the window every blow the flail lands banks its
// FULL damage as ward (bankMul, over the school's 0.55) and the cap is lifted to winCap; when the window
// closes the whole pool DETONATES — burstMul x pool damage to a foe within burstR, knock burstKnock — and
// the shield is spent. arms: B = the swell only (no burst; pool decays as ward does) · C = the burst only
// (normal banking) · D = the whole
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const bankMul = P.bankMul ?? 1.0, winCap = P.winCap ?? 200, burstMul = P.burstMul ?? 0.6, burstR = P.burstR ?? 150, burstKnock = P.burstKnock ?? 500;
  const swell = arm === "B" || arm === "D", burst = arm === "C" || arm === "D";
  const Wd = AC.STATUS.ward, cap0 = Wd.cap;
  let lastHits = 0, lastDealt = 0;
  return {
    onCast(t){ lastHits = me.hits; lastDealt = me.dealt || 0; if (swell) Wd.cap = winCap; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.shieldSum = (S.shieldSum || 0) + me.shield;
      if (swell && me.hits > lastHits){
        // top up the bank so a blow banks bankMul of its damage instead of 0.55: dealt is tracked by the engine per fighter
        const dealt = (me.dealt || 0) - lastDealt; lastDealt = me.dealt || 0; lastHits = me.hits;
        if (dealt > 0){ const extra = dealt * (bankMul - Wd.bank); const b0 = me.shield;
          me.shield = Math.min(Wd.cap, me.shield + extra); me.shieldMax = Math.max(me.shieldMax, me.shield); me.apply("ward", 1);
          S.extra = (S.extra || 0) + (me.shield - b0); }
      }
      S._pk = Math.max(S._pk || 0, me.shield);
    },
    onClose(t, reason){
      Wd.cap = cap0;
      if (S._pk !== undefined){ S.poolPeak = (S.poolPeak || 0) + S._pk; delete S._pk; }
      if (burst && reason === "clock" && me.alive && me.shield > 0){
        const pool = me.shield; S.bursts = (S.bursts || 0) + 1; S.poolSpent = (S.poolSpent || 0) + pool;
        if (foe.alive && Math.hypot(foe.x - me.x, foe.y - me.y) < burstR + H.R){
          S.dmg = (S.dmg || 0) + H.hurt(foe, pool * burstMul, me); H.knock(foe, foe.x - me.x, foe.y - me.y, burstKnock); S.landed = (S.landed || 0) + 1; }
        me.shield = 0; me.shieldMax = 0; delete me.status.ward;
      }
      if (me.shield > cap0) me.shield = cap0;
    },
    end(){ Wd.cap = cap0; if (S._pk !== undefined) delete S._pk; S.f_shield = S.winFrames ? S.shieldSum / S.winFrames : 0; delete S.winFrames; delete S.shieldSum; },
  };
}
