// ASCENSION (v74, sanctified x twinblade): for the window the caster RISES to the top of the hall and hangs
// there (pinned, weapon free); its two blades become two shafts of light reaching the floor (reachMul -> shaft),
// turning at spinMul x its spin, hitting through resolveHit at dmg x winDmg. Every shaft hit that lands heals
// the caster (blessing +healPer). arms: B = ascend + shafts only · C = + blessing on hit · D = + smite 2 a hit (extra +1)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, spin0 = w.spin, dmg0 = w.dmg;
  const shaft = P.shaft ?? 10, spinMul = P.spinMul ?? 0.5, winDmg = P.winDmg ?? 0.4, healPer = P.healPer ?? 1, smiteExtra = P.smiteExtra ?? 1;
  const heal = arm === "C" || arm === "D", smite = arm === "D";
  let hits = 0, y0 = 0, x0 = 0;
  const release = () => { me.pin = 0; me.pinMax = 0; me.pinV = null; me.pinFree = 0; me.vx = 0; me.vy = 0; };
  return {
    onCast(t){
      hits = me.hits; w.spin = spin0 * spinMul; w.dmg = dmg0 * winDmg;
      x0 = H.W / 2; y0 = P.hangY ?? (m.inset + H.R + 6);
      me.x = x0; me.y = y0; me.pinV = [0, 0]; me.pin = P.dur + 1; me.pinMax = P.dur + 1; me.pinFree = 1;
      me.reachMul = shaft; while (me.tips.length < 2) me.tips.push([]);
    },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("smite");
      if (me.alive){ me.pin = P.dur + 1; me.x = x0; me.y = Math.max(y0, m.inset + H.R + 6); }
      S.foeHits = (S.foeHits || 0);
      if (me.hits > hits){ const n = me.hits - hits; hits = me.hits; S.shaftHits = (S.shaftHits || 0) + n;
        if (heal){ me.apply("blessing", healPer * n, me); S.bless = (S.bless || 0) + healPer * n; }
        if (smite && foe.alive){ foe.apply("smite", smiteExtra * n, me); S.smite = (S.smite || 0) + smiteExtra * n; } }
    },
    onClose(){ w.spin = spin0; w.dmg = dmg0; me.reachMul = 1; release(); },
    end(){ w.spin = spin0; w.dmg = dmg0; if (me.pinFree) release(); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
