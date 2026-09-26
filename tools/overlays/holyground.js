// CONSECRATION, REDESIGNED (v78, Censer): every blow the hammer lands during the window consecrates the
// floor where it landed — a disc of radius groundR that lasts groundLife. A foe on holy ground takes smite +1
// and tickDmg every tickCd; the caster on holy ground gains blessing +1 every blessCd.
// arms: B = smite + damage only · C = + the heal · D = C with discs that also spawn at the CASTER every plantCd (it walks on holy ground)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const groundR = P.groundR ?? 90, groundLife = P.groundLife ?? 8, tickCd = P.tickCd ?? 0.5, tickDmg = P.tickDmg ?? 2, blessCd = P.blessCd ?? 1.0, plantCd = P.plantCd ?? 1.5;
  const heal = arm === "C" || arm === "D", selfPlant = arm === "D";
  let discs = [], cd = 0, bcd = 0, pcd = 0, hits = 0;
  const on = (f) => discs.some(d => Math.hypot(f.x - d.x, f.y - d.y) < groundR + H.R);
  return {
    onCast(t){ hits = me.hits; cd = 0; bcd = 0; pcd = 0; },
    onFrame(t, dt, open){
      discs = discs.filter(d => t - d.t < groundLife);
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      if (me.hits > hits){ hits = me.hits; discs.push({ x: foe.x, y: foe.y, t }); S.discs = (S.discs || 0) + 1; }
      pcd -= dt; if (selfPlant && pcd <= 0){ pcd = plantCd; discs.push({ x: me.x, y: me.y, t }); S.discs = (S.discs || 0) + 1; }
      cd -= dt; bcd -= dt;
      if (foe.alive && on(foe)){ S.foeOn = (S.foeOn || 0) + 1;
        if (cd <= 0){ cd = tickCd; foe.apply("smite", 1, me); S.dmg = (S.dmg || 0) + H.hurt(foe, tickDmg, me); S.ticks = (S.ticks || 0) + 1; } }
      if (heal && me.alive && on(me) && bcd <= 0){ bcd = blessCd; me.apply("blessing", 1, me); S.bless = (S.bless || 0) + 1; }
    },
    end(){ S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_foeOnPct = S.winFrames ? 100 * (S.foeOn || 0) / S.winFrames : 0; delete S.winFrames; delete S.foeStk; delete S.foeOn; },
  };
}
