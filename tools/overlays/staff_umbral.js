// THE UMBRAL STAFF (v91). Bow body, spell instead of an arrow:
//   spell   SHADEBOLT — a bolt of shadow that ricochets off the walls (bounce 2, speed 380, r 22, life 4.0)
//   ult     BACKLASH  — for the window the caster is shrouded: every blow it TAKES is remembered and thrown back —
//                       `refl` of the damage dealt to the foe at once, and the reflected blow curses (its memory is the blow)
// arms: S = spell only · U = spell + Backlash · W = plain bow shot + Backlash · X = spell + Backlash at refl 1.0
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.34, speed: P.speed ?? 380, r: P.r ?? 22, life: P.life ?? 4.0, grav: 0, dmgMul: 1.0 });
  const bounce = P.bounce ?? 2, refl = arm === "X" ? 1.0 : (P.refl ?? 0.5);
  const ult = arm === "U" || arm === "W" || arm === "X";
  const seen = new WeakSet(); let pool = 0, hits = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ pool = me.hp + me.shield; hits = me.hits; },
    onFrame(t, dt, open){
      for (const s of fresh()){ if (spell){ s.bounce = bounce; s.b0 = bounce; } }
      if (spell) for (const s of m.shots) if (s.own === side && s.b0 !== undefined && s.bounce < s.b0){ S.bounces = (S.bounces || 0) + (s.b0 - s.bounce); s.b0 = s.bounce; }
      if (!ult || !open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("curse");
      const now = me.hp + me.shield;
      if (now < pool && foe.alive && me.alive){
        const taken = pool - now, back = Math.round(taken * refl);
        if (back > 0){ const dealt = H.hurt(foe, back, me); foe.pushCurse(back, 1); foe.apply("curse", 1, me); S.back = (S.back || 0) + dealt; S.taken = (S.taken || 0) + taken; }
      }
      pool = now;
      if (me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){},
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
