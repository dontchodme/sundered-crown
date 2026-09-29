// v110 §2's mechanism control: tools/overlays/halo.js UNCHANGED in what it does, plus counters that
// split the lab's window frames by whether the lab step that produced them was FROZEN (m.hitStop > 0
// || m.latch || m.splitHold before the step -- the steps the engine's window clock does not count).
// Its arms must read the lab's to the fight (the counters draw nothing and write nothing).
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const haloR = P.haloR ?? 150, tickCd = P.tickCd ?? 0.5, blessCd = P.blessCd ?? 0.8;
  const bless = arm === "C" || arm === "D", arrows = arm === "D";
  let cd = 0, bcd = 0, hits = 0, prevFz = false;
  return {
    onCast(t){ cd = 0; bcd = 0; hits = me.hits; },
    onFrame(t, dt, open){
      const fz = prevFz;                                   // was the step that just ran frozen?
      prevFz = m.hitStop > 0 || !!m.latch || !!m.splitHold;  // the state before the next step
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      cd -= dt; bcd -= dt;
      const inside = foe.alive && Math.hypot(foe.x - me.x, foe.y - me.y) < haloR + H.R;
      if (fz){ S.fzWin = (S.fzWin || 0) + 1; if (inside) S.fzIn = (S.fzIn || 0) + 1; }
      else { S.unWin = (S.unWin || 0) + 1; if (inside) S.unIn = (S.unIn || 0) + 1; }
      if (inside){ S.foeIn = (S.foeIn || 0) + 1;
        if (cd <= 0){ cd = tickCd; foe.apply("smite", 1, me); S.smite = (S.smite || 0) + 1; if (fz) S.smiteFz = (S.smiteFz || 0) + 1; }
        if (bless && bcd <= 0 && me.alive){ bcd = blessCd; me.apply("blessing", 1, me); S.bless = (S.bless || 0) + 1; if (fz) S.blessFz = (S.blessFz || 0) + 1; } }
      if (arrows && me.hits > hits){ const n = me.hits - hits; hits = me.hits; if (foe.alive){ foe.apply("smite", n, me); S.arrowSmite = (S.arrowSmite || 0) + n; } }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_foeInPct = S.winFrames ? 100 * (S.foeIn || 0) / S.winFrames : 0;
      S.f_fzWinPct = S.winFrames ? 100 * (S.fzWin || 0) / S.winFrames : 0;
      S.f_inUnfzPct = S.unWin ? 100 * (S.unIn || 0) / S.unWin : 0;
      S.f_inFzPct = S.fzWin ? 100 * (S.fzIn || 0) / S.fzWin : 0;
      for (const k of ["winFrames", "foeStk", "foeIn", "fzWin", "fzIn", "unWin", "unIn"]) delete S[k]; },
  };
}
