// THE VIGIL STAFF (v92). Bow body, spell instead of an arrow:
//   spell   WARDBOLT — a heavy bolt of light that SHOVES: knock 220 on the foe it lands on (speed 400, r 26, life 3.4); the staff banks ward at 2.5 like Farwarden's bow
//   ult     BEACON   — a lantern is set down where the caster stands; for the window it fires an AIMED wardbolt at the foe every `every` s
//                      (speed 420, r 22, dmgMul, knock), and every lantern hit banks ward to the caster (resolveHit's own onSelf)
// arms: S = spell only · U = spell + Beacon · W = plain bow shot (ward 2.5) + Beacon · X = spell + Beacon with LEAD aim (foe + v x tof) · B = plain bow body at ward 2.5 (no spell, no ult)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot)), self0 = w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null;
  const spell = arm !== "W" && arm !== "B";
  w.onSelf = { ward: P.ward ?? 2.5 };
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.34, speed: P.speed ?? 400, r: P.r ?? 26, life: P.life ?? 3.4, grav: 0, dmgMul: 1.0 });
  const knock = P.knock ?? 220, every = P.every ?? 0.5, bV = P.bV ?? 420, bR = P.bR ?? 22, bMul = P.bMul ?? 0.7, bKnock = P.bKnock ?? 150, bLife = P.bLife ?? 3.0;
  const ult = arm === "U" || arm === "W" || arm === "X", lead = arm === "X";
  const seen = new WeakSet(); let lamp = null, next = 0, hits = 0, shield0 = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ lamp = { x: me.x, y: me.y }; next = t; hits = me.hits; shield0 = me.shield; },
    onFrame(t, dt, open){
      for (const s of fresh()){ if (spell && !s.lamp) s.knock = knock; }
      if (!ult || !open || !lamp) return;
      S.winFrames = (S.winFrames || 0) + 1; S.shield = (S.shield || 0) + me.shield;
      if (t >= next && foe.alive && me.alive && m.shots.length < AC.CONFIG.shot.maxLive){
        next += every;
        let tx = foe.x, ty = foe.y;
        if (lead){ const d0 = Math.hypot(foe.x - lamp.x, foe.y - lamp.y), tof = d0 / bV; tx += foe.vx * tof; ty += foe.vy * tof; }
        const a = Math.atan2(ty - lamp.y, tx - lamp.x);
        const s = { own: side, x: lamp.x, y: lamp.y, x0: lamp.x, y0: lamp.y, spd0: 0, t0: m.t,
          vx: Math.cos(a) * bV, vy: Math.sin(a) * bV, r: bR, life: bLife, max: bLife, grav: 0, dmgMul: bMul,
          seed: false, aff: me.aff, a, knock: bKnock, lamp: true };
        seen.add(s); m.shots.push(s); S.lampShots = (S.lampShots || 0) + 1;
      }
      if (me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){ lamp = null; },
    end(){ Object.assign(w.shot, shot0); if (self0) w.onSelf = self0; else delete w.onSelf; S.f_shield = S.winFrames ? S.shield / S.winFrames : 0; delete S.winFrames; delete S.shield; },
  };
}
