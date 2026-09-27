// COROLLARY, AS THE PROSE READS (v80 §4 + §6.3), for the build's gates -- a scratch copy of
// overlays/corollary.js with the two readings the build takes:
//   1. "A queued echo past the window still lands" -- the queue is NOT cleared at the close.
//   2. "no crit" / "(it does not)" -- a crit blow's echo has critMul taken back out.
// Everything else is the lab's: echoDelay 0.5, echoR 200 + R, hexPer 1, arm B = no hex, C = hex.
// echoMul defaults to 1.0 (the taken arm). The clock is the harness's (freezes included), as the lab's.
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const echoDelay = P.echoDelay ?? 0.5, echoMul = P.echoMul ?? 1.0, echoR = P.echoR ?? 200, hexPer = P.hexPer ?? 1;
  const critMul = AC.CONFIG.chaos.critMul;
  const hex = arm === "C";
  let hits = 0, dealt = 0, crits = 0, queue = [];
  return {
    onCast(t){ hits = me.hits; dealt = me.dealt; crits = me.crits; },
    onFrame(t, dt, open){
      if (open && me.hits > hits){
        const n = me.hits - hits, k = me.crits - crits, D = me.dealt - dealt;
        const base = D / (n + (critMul - 1) * k);       // per-blow damage with no crit
        hits = me.hits; dealt = me.dealt; crits = me.crits;
        for (let i = 0; i < n; i++) queue.push({ at: t + echoDelay, dmg: Math.round(base) * echoMul });
        S.blows = (S.blows || 0) + n; S.critBlows = (S.critBlows || 0) + k;
      } else if (!open){ hits = me.hits; dealt = me.dealt; crits = me.crits; }
      while (queue.length && queue[0].at <= t){ const q = queue.shift(); S.echoes = (S.echoes || 0) + 1;
        if (!open) S.late = (S.late || 0) + 1;
        if (foe.alive && me.alive && Math.hypot(foe.x - me.x, foe.y - me.y) < echoR + H.R){ S.landed = (S.landed || 0) + 1; S.dmg = (S.dmg || 0) + H.hurt(foe, q.dmg, me);
          if (hex) { foe.apply("hex", hexPer, me); S.hex = (S.hex || 0) + hexPer; } } }
    },
    onClose(){ /* the queue outlives the window */ },
  };
}
