// THE BLOODSWORN STAFF (v90). The staff is a bow body whose basic attack is a SPELL:
//   spell   SEEKER — a globule of blood that homes on the foe (speed 300, home 2.2 rad/s, r 22, life 3.0)
//   ult     GYRE   — for the window the seekers do not leave: they orbit the caster (r 95, 4 rad/s, up to 6);
//                    when the foe comes inside lungeR they all lunge (speed 520, home 8). At close, the orbit is loosed.
// arms: S = spell only · U = spell + Gyre · V = spell + Gyre with no lunge (orbit only: a moat) · W = plain bow shot + Gyre (the ult on the bow, for the decomposition)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.34, speed: P.speed ?? 300, r: P.r ?? 22, life: P.life ?? 3.0, grav: 0, dmgMul: 1.0 });
  const home = P.home ?? 2.2, oR = P.orbitR ?? 95, oW = P.orbitW ?? 4.0, maxOrb = P.maxOrb ?? 6;
  const lungeR = P.lungeR ?? 230, lungeV = P.lungeV ?? 520, lungeHome = P.lungeHome ?? 8;
  const ult = arm === "U" || arm === "V" || arm === "W", lunge = arm !== "V";
  const seen = new WeakSet(); let orb = [], phase = 0, hits = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ hits = me.hits; },
    onFrame(t, dt, open){
      for (const s of fresh()){
        if (spell) s.home = home;
        if (ult && open && orb.length < maxOrb){ s.orb = true; s.home = 0; s.ph = phase + orb.length * (2 * Math.PI / maxOrb); orb.push(s); S.orbited = (S.orbited || 0) + 1; }
      }
      if (!ult) return;
      orb = orb.filter(s => m.shots.includes(s));
      phase += oW * dt;
      if (open){
        S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("hemorrhage");
        const d = Math.hypot(foe.x - me.x, foe.y - me.y);
        if (lunge && orb.length && d < lungeR && foe.alive){
          for (const s of orb){ const ang = Math.atan2(foe.y - s.y, foe.x - s.x); s.vx = Math.cos(ang) * lungeV; s.vy = Math.sin(ang) * lungeV; s.a = ang; s.home = lungeHome; s.orb = false; s.life = 2.0; S.lunged = (S.lunged || 0) + 1; }
          orb = [];
        }
      }
      for (let i = 0; i < orb.length; i++){
        const s = orb[i], a = phase + i * (2 * Math.PI / Math.max(1, orb.length));
        s.x = me.x + Math.cos(a) * oR; s.y = me.y + Math.sin(a) * oR;
        s.vx = -Math.sin(a) * oR * oW; s.vy = Math.cos(a) * oR * oW; s.a = a + Math.PI / 2; s.life = 3.0;
      }
      if (open && me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){ for (const s of orb){ s.orb = false; s.home = home; const ang = Math.atan2(foe.y - s.y, foe.x - s.x); s.vx = Math.cos(ang) * (w.shot.speed); s.vy = Math.sin(ang) * w.shot.speed; s.a = ang; } orb = []; },
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
