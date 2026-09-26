// BRAMBLESNARE, REDESIGNED (v84, Thornwake): every blow the scythe lands during the window leaves a BRAMBLE
// where it landed — a patch of radius patchR for patchLife. A foe in a bramble is entangled +1 every tickCd and
// takes tickDmg; a foe that ENTERS one is rooted (pinned) rootFor. arms: B = entangle + bite · C = B + the root on entry
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const patchR = P.patchR ?? 80, patchLife = P.patchLife ?? 6, tickCd = P.tickCd ?? 0.5, tickDmg = P.tickDmg ?? 2, rootFor = P.rootFor ?? 0.6;
  const root = arm === "C";
  let patches = [], cd = 0, hits = 0, wasIn = false;
  return {
    onCast(t){ hits = me.hits; cd = 0; },
    onFrame(t, dt, open){
      patches = patches.filter(p => t - p.t < patchLife);
      if (open && me.hits > hits){ hits = me.hits; patches.push({ x: foe.x, y: foe.y, t }); S.patches = (S.patches || 0) + 1; }
      if (!open && !patches.length) return;
      cd -= dt;
      const inside = foe.alive && patches.some(p => Math.hypot(foe.x - p.x, foe.y - p.y) < patchR + H.R);
      if (inside){ S.foeIn = (S.foeIn || 0) + 1;
        if (!wasIn && root){ H.pin(foe, rootFor); S.roots = (S.roots || 0) + 1; }
        if (cd <= 0){ cd = tickCd; foe.apply("entangle", 1, me); S.dmg = (S.dmg || 0) + H.hurt(foe, tickDmg, me); S.ticks = (S.ticks || 0) + 1; } }
      wasIn = inside;
    },
  };
}
