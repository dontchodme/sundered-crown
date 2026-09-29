// CONTROL COPY of tools/overlays/drain.js (v76), for v106 §2's clock attribution. drain_freeze.js (the census
// copy) with ONE change, P.liveOnly: when 1 the drain is paid only after a LIVE lab step -- a step the engine's
// world, and so its bleed, would have run -- as the engine's tickStatus pays it. With --P dur=9.30 the lab's window
// is then the engine's in match time (8 / (1 - 0.1396), the census's frozen share inside windows) and its drain
// is the engine's tick for tick: the lab put onto the engine's clock.
// CENSUS COPY of tools/overlays/drain.js (v76, Widowmaker / Exsanguinate), for v106's charge conversion.
// THE MECHANIC IS drain.js's, LINE FOR LINE. What it adds reads and never writes: it wraps THIS match's
// `m.step` and counts, BEFORE each lab step, whether that step is frozen (m.hitStop > 0 || m.latch ||
// m.splitHold -- the three branches of Match.step that return before the fighter loop, so the engine's
// charge and window clocks do not advance), over the whole fight and inside windows (the window as the
// harness last reported it, which is the window the coming step runs in). All counts per FIGHT (f_ keys).
// Stated precedents: 06-docs/v99/runs/ironwood/tree_freeze.js, 06-docs/v100/runs/ram_freeze.js
// (those counted after the step; this counts before it, as the v106 method asks). `drainFz` is the part of
// the drain the lab paid on a frozen step, where the engine's bleed does not tick at all.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const drainMul = P.drainMul ?? 1.0, steal = P.steal ?? 0.35, ls0 = me.lifesteal;
  const drain = arm === "B" || arm === "D", lifesteal = arm === "C" || arm === "D";
  const Hm = AC.STATUS.hemorrhage;
  let open0 = false, lastFz = false;
  const oStep = m.step;
  m.step = function(dt){
    const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold; lastFz = fz;
    S.f_steps = (S.f_steps || 0) + 1; if (fz) S.f_frozen = (S.f_frozen || 0) + 1;
    if (open0){ S.f_wst = (S.f_wst || 0) + 1; if (fz) S.f_wfz = (S.f_wfz || 0) + 1; }
    return oStep.call(this, dt);
  };
  return {
    onCast(t){ if (lifesteal) me.lifesteal = steal; },
    onFrame(t, dt, open){
      open0 = open;
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hemorrhage");
      if (drain && me.alive && foe.alive && !(P.liveOnly && lastFz)){ const st = foe.stacks("hemorrhage");
        if (st > 0){ const tick = Hm.dps * st * dt * foe.dmgTakenMul() * drainMul; const hp0 = me.hp; me.hp = Math.min(me.maxHp || me.hp + tick, me.hp + tick); S.drained = (S.drained || 0) + (me.hp - hp0); if (lastFz) S.drainFz = (S.drainFz || 0) + (me.hp - hp0); } }
    },
    onClose(){ me.lifesteal = ls0; },
    end(){ me.lifesteal = ls0; S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
