// TENDRIL (v68) as an ult_overlay module — the harness's own reproduction control.
// Must read what tools/vine_price.py reads at the same P: arm D, blade 19, turn 4 -> 54.4% (seed0 2207 x 20).
// arms: B = seek + bites, no growth, no root · C = seek + growth + bites · D = the whole · R = seek + root only
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, spin0 = w.spin;
  const turn = P.turn ?? 4, growRate = P.growRate ?? 0.3, growCap = P.growCap ?? 3.0;
  const vineW = P.vineW ?? 8, biteDmg = P.biteDmg ?? 2, biteCd = P.biteCd ?? 0.30, rootPer = P.rootPer ?? 0.30;
  const bites = arm === "B" || arm === "C" || arm === "D";
  const grow  = arm === "C" || arm === "D";
  const root  = arm === "D" || arm === "R";
  let cd = 0, winOpen = false;
  return {
    onCast(t){ winOpen = true; cd = 0; w.spin = 0; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1;
      S.foeStk = (S.foeStk || 0) + foe.stacks("entangle");
      if (!foe.alive) return;
      // the seek: the facing turns toward the foe
      const want = Math.atan2(foe.y - me.y, foe.x - me.x);
      if (turn > 0){ const d = H.angTo(me.theta, want); const mx = turn * dt; me.theta += Math.max(-mx, Math.min(mx, d)); }
      else me.theta = want;
      // the growth: toward the foe's rim, both directions
      if (grow){
        const dd = Math.hypot(foe.x - me.x, foe.y - me.y);
        const target = Math.max(1, Math.min(growCap, (dd - H.R) / (w.reach * m.actMods.reach)));
        if (target > me.reachMul) me.reachMul = Math.min(target, me.reachMul + growRate * dt);
        else me.reachMul = Math.max(target, me.reachMul - growRate * dt);
        S.growPeakSum = (S.growPeakSum || 0); // per-cast peak tracked below
        S._pk = Math.max(S._pk || 1, me.reachMul);
      }
      // the bite
      cd -= dt;
      const d = H.segDist(foe.x, foe.y, me.pivX, me.pivY, me.headX, me.headY);
      if (d < H.R + vineW){
        S.touch = (S.touch || 0) + 1;
        if (bites && cd <= 0){ cd = biteCd; S.bites = (S.bites || 0) + 1; S.dmg = (S.dmg || 0) + H.hurt(foe, biteDmg, me); foe.apply("entangle", 1, me); }
      }
    },
    onClose(t, reason){
      winOpen = false; w.spin = spin0; me.reachMul = 1;
      if (root && reason === "clock" && foe.alive){ const n = foe.stacks("entangle"); if (n > 0){ H.pin(foe, rootPer * n); S.rootS = (S.rootS || 0) + rootPer * n; S.roots = (S.roots || 0) + 1; } }
      if (S._pk){ S.growPeakSum += S._pk; delete S._pk; }
    },
    end(){ w.spin = spin0; if (S._pk) delete S._pk; S.touchPct = S.winFrames ? 100 * (S.touch || 0) / S.winFrames : 0; S.foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; delete S.winFrames; delete S.touch;
      // touchPct and foeStk are per-fight ratios: mark them f_
      S.f_touchPct = S.touchPct; S.f_foeStk = S.foeStk; delete S.touchPct; delete S.foeStk; },
  };
}
