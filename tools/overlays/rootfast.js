// ROOTFAST, REDESIGNED (v85, Heartwood): for the window every blow the greatsword lands ROOTS the foe where
// it is hit — pinned rootFor (ball and weapon) — so the next swing finds it still there; a rooted foe takes
// entangle +extraEnt. arms: B = the root only · C = root + extra entangle
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const rootFor = P.rootFor ?? 0.45, extraEnt = P.extraEnt ?? 1;
  const ent = arm === "C";
  let hits = 0;
  return {
    onCast(t){ hits = me.hits; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foePinned = (S.foePinned || 0) + (foe.pin > 0 ? 1 : 0);
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; if (foe.alive){ H.pin(foe, rootFor); S.roots = (S.roots || 0) + n;
        if (ent){ foe.apply("entangle", extraEnt * n, me); S.ent = (S.ent || 0) + extraEnt * n; } } }
    },
    end(){ S.f_pinnedPct = S.winFrames ? 100 * (S.foePinned || 0) / S.winFrames : 0; delete S.winFrames; delete S.foePinned; },
  };
}
