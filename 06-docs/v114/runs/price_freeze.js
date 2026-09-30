// CENSUS COPY of tools/overlays/bloodprice.js (v81, Goreshard / Bloodprice), for v114's charge conversion.
// THE MECHANIC IS bloodprice.js's, LINE FOR LINE. What it adds reads and never writes: it wraps THIS match's
// `m.step` and counts, BEFORE each lab step, whether that step is frozen (m.hitStop > 0 || m.latch ||
// m.splitHold -- the three branches of Match.step that return before the fighter loop, so the engine's
// charge and window clocks do not advance), over the whole fight and inside windows (the window as the
// harness last reported it, which is the window the coming step runs in). All counts per FIGHT (f_ keys).
// Precedent: 06-docs/v106/runs/drain_freeze.js (counts before the step), 06-docs/v99/runs/ironwood/tree_freeze.js.
// It also records, per cast, the stacks each window blow was priced on (`stkAtBlow`, the count the lab's
// w.dmg was last set from) and the blows that landed on a frozen-free step inside windows, for the probe's
// comparable columns. None of it writes the match.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, dmg0 = w.dmg, perStack = P.perStack ?? 0.12, extraBleed = P.extraBleed ?? 1;
  const extra = arm === "C";
  let hits = 0;
  let open0 = false, stkSet = 0;
  const oStep = m.step;
  m.step = function(dt){
    const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold;
    S.f_steps = (S.f_steps || 0) + 1; if (fz) S.f_frozen = (S.f_frozen || 0) + 1;
    if (open0){ S.f_wst = (S.f_wst || 0) + 1; if (fz) S.f_wfz = (S.f_wfz || 0) + 1; }
    return oStep.call(this, dt);
  };
  return {
    onCast(t){ hits = me.hits; },
    onFrame(t, dt, open){
      open0 = open;
      if (!open){ w.dmg = dmg0; stkSet = 0; return; }
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hemorrhage");
      if (me.hits > hits){ S.stkAtBlow = (S.stkAtBlow || 0) + stkSet * (me.hits - hits); }
      w.dmg = dmg0 * (1 + perStack * foe.stacks("hemorrhage"));   // read before the next blow resolves
      stkSet = foe.stacks("hemorrhage");
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.blows = (S.blows || 0) + n;
        if (extra && foe.alive){ foe.apply("hemorrhage", extraBleed * n, me); S.bleed = (S.bleed || 0) + extraBleed * n; } }
    },
    onClose(){ w.dmg = dmg0; stkSet = 0; open0 = false; },
    end(){ w.dmg = dmg0; S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
