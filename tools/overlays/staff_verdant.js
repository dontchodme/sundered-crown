// THE VERDANT STAFF (v93). Bow body, spell instead of an arrow:
//   spell   THORNBURST — every cast is a FAN of `fan` thorns (spread `spread` rad about the facing), short-lived (life 0.8 at 440 = ~350 range),
//                        each at dmgMul `thornMul`, each landing entangle 2 (the channel)
//   ult     POLLEN     — a cloud (r `cloudR`) leaves the staff and drifts toward the foe at `drift` px/s for the window;
//                        a foe inside it is entangled +1 and bitten for `tick` every `every` s
// arms: S = spell only · U = spell + Pollen · W = plain bow shot + Pollen · X = spell + Pollen that does not drift (a fixed cloud where it was cast)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, side = me === m.a ? "a" : "b";
  const shot0 = JSON.parse(JSON.stringify(w.shot));
  const spell = arm !== "W";
  const fan = P.fan ?? 3, spread = P.spread ?? 0.28, thornMul = P.thornMul ?? 0.45;
  if (spell) Object.assign(w.shot, { cadence: P.cad ?? 0.42, speed: P.speed ?? 440, r: P.r ?? 16, life: P.life ?? 0.8, grav: 0, dmgMul: thornMul });
  const cloudR = P.cloudR ?? 110, drift = arm === "X" ? 0 : (P.drift ?? 90), tick = P.tick ?? 1.5, every = P.every ?? 0.4, stk = P.stk ?? 1;
  const ult = arm === "U" || arm === "W" || arm === "X";
  const seen = new WeakSet(); let cloud = null, nextTick = 0, hits = 0;
  function fresh(){ const o = []; for (const s of m.shots) if (s.own === side && !seen.has(s)){ seen.add(s); o.push(s); } return o; }
  return {
    onCast(t){ cloud = { x: me.x, y: me.y }; nextTick = t; hits = me.hits; },
    onFrame(t, dt, open){
      for (const s of fresh()){
        if (!spell || s.thorn) continue;
        s.thorn = true;
        // the engine's own thorn is the centre of the fan; the others sit at +/- spread, +/- 2 spread ...
        for (let k = 1; k < fan; k++){
          const off = spread * Math.ceil(k / 2) * (k % 2 ? -1 : 1);
          m.spawnShot(me, s.a + off);
          const q = m.shots[m.shots.length - 1]; q.thorn = true; seen.add(q);
          S.thorns = (S.thorns || 0) + 1;
        }
      }
      if (!ult || !open || !cloud) return;
      S.winFrames = (S.winFrames || 0) + 1; S.foeStk = (S.foeStk || 0) + foe.stacks("entangle");
      if (drift > 0 && foe.alive){ const dx = foe.x - cloud.x, dy = foe.y - cloud.y, l = Math.hypot(dx, dy) || 1; const st = Math.min(l, drift * dt); cloud.x += dx / l * st; cloud.y += dy / l * st; }
      const inside = foe.alive && Math.hypot(foe.x - cloud.x, foe.y - cloud.y) < cloudR + H.R;
      if (inside) S.inFrames = (S.inFrames || 0) + 1;
      if (inside && t >= nextTick){ nextTick = t + every; const d = H.hurt(foe, tick, me); foe.apply("entangle", stk, me); S.bite = (S.bite || 0) + d; S.ticks = (S.ticks || 0) + 1; }
      if (me.hits > hits){ S.hitsInWin = (S.hitsInWin || 0) + (me.hits - hits); hits = me.hits; }
    },
    onClose(t, reason){ cloud = null; },
    end(){ Object.assign(w.shot, shot0); S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_inShare = S.winFrames ? (S.inFrames || 0) / S.winFrames : 0; delete S.winFrames; delete S.foeStk; delete S.inFrames; },
  };
}
