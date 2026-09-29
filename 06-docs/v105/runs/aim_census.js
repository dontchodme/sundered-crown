// THE CHARGE CENSUS (v105): overlays/aim.js (v75) UNCHANGED in what it does, plus a count of the lab's
// FROZEN steps. onFrame runs after every lab step, so the state it reads is the state the NEXT step
// starts from: a step is frozen when m.hitStop > 0 || m.latch || m.splitHold (step() takes the frozen
// path on any of the three). Counted on every fight of the arm, in total and inside windows
// (`open` as the harness passes it). f_steps / f_frozen / f_wst / f_wfz are per fight sums.
// The mechanism below the census lines is aim.js to the character.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, turn = P.turn ?? 6, hexExtra = P.hexExtra ?? 1, pinFor = P.pinFor ?? 0.25, lead = P.lead ?? 1;
  const hex = arm === "C", pin = arm === "D";
  let hits = 0;
  return {
    onCast(t){ hits = me.hits; },
    onFrame(t, dt, open){
      const fz = (m.hitStop > 0 || !!m.latch || !!m.splitHold);
      S.f_steps = (S.f_steps || 0) + 1; if (fz) S.f_frozen = (S.f_frozen || 0) + 1;
      if (open){ S.f_wst = (S.f_wst || 0) + 1; if (fz) S.f_wfz = (S.f_wfz || 0) + 1; }
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
