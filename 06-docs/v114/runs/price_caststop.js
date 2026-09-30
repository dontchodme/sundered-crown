// SCRATCH CONTROL COPY of tools/overlays/bloodprice.js (v114 §2): the mechanic line for line, plus fireUlt's common
// cast stop (m.hitStop = max(hitStop, P.castStop)) at each cast, which the lab never had and every built cast carries.
// BLOODPRICE, REDESIGNED (v81, Goreshard): for the window the foe pays in blood — Goreshard's blows deal
// +perStack x (foe's hemorrhage stacks) of their damage, and its hits apply hemorrhage extraBleed more.
// arms: B = the scaling only · C = scaling + extra bleed on hit
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, dmg0 = w.dmg, perStack = P.perStack ?? 0.12, extraBleed = P.extraBleed ?? 1;
  const extra = arm === "C";
  let hits = 0;
  return {
    onCast(t){ hits = me.hits; if (P.castStop) m.hitStop = Math.max(m.hitStop, P.castStop); },   // SCRATCH CONTROL: fireUlt's common 0.08 stop at the cast
    onFrame(t, dt, open){
      if (!open){ w.dmg = dmg0; return; }
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hemorrhage");
      w.dmg = dmg0 * (1 + perStack * foe.stacks("hemorrhage"));   // read before the next blow resolves
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.blows = (S.blows || 0) + n;
        if (extra && foe.alive){ foe.apply("hemorrhage", extraBleed * n, me); S.bleed = (S.bleed || 0) + extraBleed * n; } }
    },
    onClose(){ w.dmg = dmg0; },
    end(){ w.dmg = dmg0; S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
