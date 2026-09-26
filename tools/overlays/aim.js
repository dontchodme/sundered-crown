// AUGURY (v75, runic x bow): for the window the bow AIMS — its facing is driven (at turn rad/s) to the lead
// point where the foe will be when the arrow arrives, so every arrow of the ordinary stream flies true.
// arms: B = aim only · C = aim + an extra hex on every arrow hit · D = aim + the foe PINNED 0.25s on every arrow hit (stasis on the arrow)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, turn = P.turn ?? 6, hexExtra = P.hexExtra ?? 1, pinFor = P.pinFor ?? 0.25, lead = P.lead ?? 1;
  const hex = arm === "C", pin = arm === "D";
  let hits = 0;
  return {
    onCast(t){ hits = me.hits; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hex");
      if (foe.alive && me.alive){
        const v = w.shot.speed;
        const d0 = Math.hypot(foe.x - me.x, foe.y - me.y), tof = lead ? d0 / v : 0;
        const tx = foe.x + foe.vx * tof, ty = foe.y + foe.vy * tof;
        const want = Math.atan2(ty - me.y, tx - me.x);
        if (turn > 0){ const d = H.angTo(me.theta, want); const mx = turn * dt; me.theta += Math.max(-mx, Math.min(mx, d)); }
        else me.theta = want;
      }
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.arrowHits = (S.arrowHits || 0) + n;
        if (hex && foe.alive){ foe.apply("hex", hexExtra * n, me); S.hex = (S.hex || 0) + hexExtra * n; }
        if (pin && foe.alive){ H.pin(foe, pinFor); S.pinS = (S.pinS || 0) + pinFor; } }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
