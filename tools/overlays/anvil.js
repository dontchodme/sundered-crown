// ANVIL (v73, dwarven x twinblade): for the window the blades are forged iron — mass 1.1 -> winMass, so the
// twinblade WINS the binds it always lost; a bind it wins sunders the foe (bindSunder). Optionally the sunder
// cap is lifted to winCap for the window (the fast blade stacks past 6).
// arms: B = mass only · C = mass + sunder on a won bind · D = C + the cap lifted · S = sunder on bind only (no mass; a control)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, mass0 = w.mass, winMass = P.winMass ?? 5.0, bindSunder = P.bindSunder ?? 2, winCap = P.winCap ?? 12;
  const Sd = AC.STATUS.sunder, cap0 = Sd.maxStacks;
  const mass = arm === "B" || arm === "C" || arm === "D", sunder = arm === "C" || arm === "D" || arm === "S", lift = arm === "D";
  let clanks = 0;
  return {
    onCast(t){ clanks = me.clanks; if (mass) w.mass = winMass; if (lift) Sd.maxStacks = winCap; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("sunder");
      if (me.clanks > clanks){
        clanks = me.clanks; S.binds = (S.binds || 0) + 1;
        // who won: the engine's own rule, mass^1.7 shares, decisive past 0.16
        const wA = Math.pow(w.mass, 1.7), wB = Math.pow(foe.w.mass, 1.7), tot = wA + wB;
        const shareMe = wB / tot, shareFoe = wA / tot;
        const won = Math.abs(shareMe - shareFoe) > 0.16 && shareMe < shareFoe;
        if (won){ S.won = (S.won || 0) + 1; if (sunder && foe.alive){ foe.apply("sunder", bindSunder, me); S.stacks = (S.stacks || 0) + bindSunder; } }
      }
      S._pk = Math.max(S._pk || 0, foe.stacks("sunder"));
    },
    onClose(){ w.mass = mass0; Sd.maxStacks = cap0; if (S._pk !== undefined){ S.stkPeak = (S.stkPeak || 0) + S._pk; delete S._pk; } },
    end(){ w.mass = mass0; Sd.maxStacks = cap0; if (S._pk !== undefined) delete S._pk;
      S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
