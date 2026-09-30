// SCRATCH COPY of tools/overlays/unmaking.js (v79) for v111 §2 -- THE LAB'S MECHANISM UNCHANGED, plus
// counters that read it: on every window frame, the foe's hex stacks and whether its weapon is stunned,
// split by whether the step that made the frame was FROZEN (the state after the previous frame:
// m.hitStop > 0 || m.latch || m.splitHold). All counters are f_ (per fight) sums, so pooled ratios are
// ratios of the printed means. Nothing here writes the match: its arms must read the lab's to the fight.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const shrinkPer = P.shrinkPer ?? 0.12, shrinkMin = P.shrinkMin ?? 0.4, hexExtra = P.hexExtra ?? 1, stunMul = P.stunMul ?? 1;
  const Hx = AC.STATUS.hex, stun0 = Hx.stunFor;
  const hex = arm === "C" || arm === "D", shrink = arm !== "D";
  let hits = 0, fzPrev = false;
  const add = (k, v) => { S[k] = (S[k] || 0) + v; };
  return {
    onCast(t){ hits = me.hits; Hx.stunFor = stun0 * stunMul; },
    onFrame(t, dt, open){
      const fz = fzPrev;
      fzPrev = m.hitStop > 0 || !!m.latch || !!m.splitHold;
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeReach = (S.foeReach || 0) + foe.reachMul;
      /* THE COUNTERS (read only) */
      const hx = foe.stacks("hex"), stn = foe.stun > 0 ? 1 : 0;
      add("f_wf", 1); add("f_hexSum", hx); add("f_stunSum", stn);
      if (fz){ add("f_wfFz", 1); add("f_hexFz", hx); add("f_stunFz", stn); }
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.unmade = (S.unmade || 0) + n;
        if (shrink) foe.reachMul = Math.max(shrinkMin, foe.reachMul - shrinkPer * n);
        if (hex && foe.alive){ foe.apply("hex", hexExtra * n, me); S.hex = (S.hex || 0) + hexExtra * n; } }
    },
    onClose(){ foe.reachMul = 1; Hx.stunFor = stun0; },
    end(){ foe.reachMul = 1; Hx.stunFor = stun0; S.f_foeReach = S.winFrames ? S.foeReach / S.winFrames : 1; delete S.winFrames; delete S.foeReach; },
  };
}
