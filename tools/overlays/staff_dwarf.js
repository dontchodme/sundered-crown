// THE DWARVEN STAFF (v96). Bow body, spell instead of an arrow:
//   spell   SLUG     — a heavy iron slug lobbed along the facing: it FALLS (grav `grav`), slow to reload (cadence 0.55), big (r 28), hits at dmgMul 1.6
//   ult     IRONFALL — for the window the staff also fires a SHELL every `every` s, lobbed high to land on the foe's LEAD point `T` s later;
//                      a shell bursts where it lands (r `popR`, `popDmg` absolute, sundering — the engine's own shard pop), or on the foe if it strikes it in flight
// arms: S = spell only · U = spell + Ironfall · W = plain bow shot + Ironfall · X = spell + Ironfall aimed at where the foe IS (no lead) · Y = spell + Ironfall with no burst (a shell that must strike)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.55, speed: P.speed ?? 470, r: P.r ?? 28, life: P.life ?? 3.0, grav: P.grav ?? 700, dmgMul: P.slugMul ?? 1.6 });
  const every = P.every ?? 0.7, T = P.T ?? 0.85, g = P.g ?? 1000, sR = P.sR ?? 26, sMul = P.sMul ?? 1.6, popR = P.popR ?? 60, popDmg = P.popDmg ?? 8;
  const ult = arm === "U" || arm === "W" || arm === "X" || arm === "Y", lead = arm !== "X", burst = arm !== "Y";
  const seen = new WeakSet(); let next = 0, hits = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ next = t; hits = me.hits; },
    onFrame(t, dt, open){
      fresh();
      if (!ult || !open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("sunder");
      if (t >= next && foe.alive && me.alive && m.shots.length < AC.CONFIG.shot.maxLive){
        next += every;
        const tx = foe.x + (lead ? foe.vx * T : 0), ty = foe.y + (lead ? foe.vy * T : 0);
        const vx = (tx - me.x) / T, vy = (ty - me.y) / T - 0.5 * g * T;
        const a = Math.atan2(vy, vx);
        const s = { own: side, x: me.x, y: me.y, x0: me.x, y0: me.y, spd0: 0, t0: m.t, vx, vy, r: sR, life: T, max: T, grav: g, dmgMul: sMul,
          seed: false, aff: me.aff, a, shell: true };
        if (burst){ s.shard = true; s.pop = popDmg; s.popR = popR; }
        seen.add(s); m.shots.push(s); S.shells = (S.shells || 0) + 1;
      }
      if (me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){},
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.foeStk; },
  };
}
