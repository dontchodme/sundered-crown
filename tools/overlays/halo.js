// BENEDICTION, REDESIGNED (v82, Aureole): for the window a halo of radius haloR stands around Aureole.
// A foe inside it is smitten (+1 every tickCd) ; Aureole inside her own halo (always) is blessed +1 every blessCd
// WHILE A FOE IS IN IT (the halo blesses when it is tested). Arrows fired through the halo carry +1 smite.
// arms: B = smite inside · C = B + the blessing · D = C + blessed arrows
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const haloR = P.haloR ?? 150, tickCd = P.tickCd ?? 0.5, blessCd = P.blessCd ?? 0.8;
  const bless = arm === "C" || arm === "D", arrows = arm === "D";
  let cd = 0, bcd = 0, hits = 0;
  return {
    onCast(t){ cd = 0; bcd = 0; hits = me.hits; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      cd -= dt; bcd -= dt;
      const inside = foe.alive && Math.hypot(foe.x - me.x, foe.y - me.y) < haloR + H.R;
      if (inside){ S.foeIn = (S.foeIn || 0) + 1;
        if (cd <= 0){ cd = tickCd; foe.apply("smite", 1, me); S.smite = (S.smite || 0) + 1; }
        if (bless && bcd <= 0 && me.alive){ bcd = blessCd; me.apply("blessing", 1, me); S.bless = (S.bless || 0) + 1; } }
      if (arrows && me.hits > hits){ const n = me.hits - hits; hits = me.hits; if (foe.alive){ foe.apply("smite", n, me); S.arrowSmite = (S.arrowSmite || 0) + n; } }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_foeInPct = S.winFrames ? 100 * (S.foeIn || 0) / S.winFrames : 0; delete S.winFrames; delete S.foeStk; delete S.foeIn; },
  };
}
