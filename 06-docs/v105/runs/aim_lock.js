// THE LAB'S MECHANISM, COUNTED (v105): overlays/aim.js (v75) UNCHANGED in what it does, plus counts the
// build's probe prints, read the lab's way: arrows and blade blows landed inside windows (an instance
// wrapper on m.resolveHit: `mul !== undefined` is a projectile, the engine's own test), the LOCK (window
// frames >= 0.5s after the cast on which the facing already sat within turn x dt of the lead, before the
// overlay's turn), and the window's frozen steps. Nothing here writes the fight.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, turn = P.turn ?? 6, hexExtra = P.hexExtra ?? 1, pinFor = P.pinFor ?? 0.25, lead = P.lead ?? 1;
  const hex = arm === "C", pin = arm === "D";
  let hits = 0, castT = -1, isOpen = false;
  const oR = m.resolveHit;
  m.resolveHit = function(self, fo, hx, hy, seg, mul, over){
    const h0 = me.hits, r = oR.call(this, self, fo, hx, hy, seg, mul, over);
    if (self === me && me.hits > h0 && isOpen){ if (mul !== undefined) S.l_arrows = (S.l_arrows || 0) + 1; else S.l_blades = (S.l_blades || 0) + 1; }
    return r;
  };
  return {
    onCast(t){ hits = me.hits; castT = t; isOpen = true; },
    onClose(t){ isOpen = false; },
    onFrame(t, dt, open){
      isOpen = open;
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hex");
      if (m.hitStop > 0 || m.latch || m.splitHold) S.f_wfz = (S.f_wfz || 0) + 1;
      if (foe.alive && me.alive){
        const v = w.shot.speed;
        const d0 = Math.hypot(foe.x - me.x, foe.y - me.y), tof = lead ? d0 / v : 0;
        const tx = foe.x + foe.vx * tof, ty = foe.y + foe.vy * tof;
        const want = Math.atan2(ty - me.y, tx - me.x);
        if (t - castT >= 0.5){ S.f_lockF = (S.f_lockF || 0) + 1; if (Math.abs(H.angTo(me.theta, want)) <= turn * dt) S.f_lock = (S.f_lock || 0) + 1; }
        if (turn > 0){ const d = H.angTo(me.theta, want); const mx = turn * dt; me.theta += Math.max(-mx, Math.min(mx, d)); }
        else me.theta = want;
      }
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.arrowHits = (S.arrowHits || 0) + n;
        if (hex && foe.alive){ foe.apply("hex", hexExtra * n, me); S.hex = (S.hex || 0) + hexExtra * n; }
        if (pin && foe.alive){ H.pin(foe, pinFor); S.pinS = (S.pinS || 0) + pinFor; } }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_wst = S.winFrames || 0; delete S.winFrames; delete S.foeStk; m.resolveHit = oR; },
  };
}
