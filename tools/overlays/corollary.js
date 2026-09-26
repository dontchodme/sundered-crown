// COROLLARY, REDESIGNED (v80, Axiom): every blow Axiom lands during the window is followed by its corollary —
// echoDelay later a rune-echo of the same blow strikes the foe wherever it is if within echoR of the caster:
// echoMul x the blow's damage (through hurt: ward first, no crit) and hexPer hex. arms: B = echo damage only · C = echo + hex
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const echoDelay = P.echoDelay ?? 0.5, echoMul = P.echoMul ?? 0.5, echoR = P.echoR ?? 200, hexPer = P.hexPer ?? 1;
  const hex = arm === "C";
  let hits = 0, dealt = 0, queue = [];
  return {
    onCast(t){ hits = me.hits; dealt = me.dealt; },
    onFrame(t, dt, open){
      if (open && me.hits > hits){ const n = me.hits - hits; const d = (me.dealt - dealt) / n; hits = me.hits; dealt = me.dealt;
        for (let i = 0; i < n; i++) queue.push({ at: t + echoDelay, dmg: d * echoMul }); }
      while (queue.length && queue[0].at <= t){ const q = queue.shift(); S.echoes = (S.echoes || 0) + 1;
        if (foe.alive && me.alive && Math.hypot(foe.x - me.x, foe.y - me.y) < echoR + H.R){ S.landed = (S.landed || 0) + 1; S.dmg = (S.dmg || 0) + H.hurt(foe, q.dmg, me);
          if (hex) { foe.apply("hex", hexPer, me); S.hex = (S.hex || 0) + hexPer; } } }
    },
    onClose(){ queue = []; },
  };
}
