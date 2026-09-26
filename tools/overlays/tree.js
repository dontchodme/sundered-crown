// THE TREE (v69, verdant x warhammer): the caster ROOTS ITSELF (ball held, weapon free -- Garrote's
// verb on the self), the haft grows into a bough (reachMul eases toward growCap at growRate), and
// anyone inside the bough's reach is in the canopy: entangle every canopyCd while inside.
// arms: G = growth only (no root, no canopy) · B = root + canopy · C = root + growth · D = the whole
//       T = growth + canopy, no self-root (what the root costs)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w;
  const growRate = P.growRate ?? 0.35, growCap = P.growCap ?? 3.0;
  const canopyCd = P.canopyCd ?? 0.5, canopyPer = P.canopyPer ?? 1, canopyMul = P.canopyMul ?? 1.0;
  const spinMul = P.spinMul ?? 1.0, spin0 = w.spin, blades0 = w.blades.slice();
  const boughs = P.boughs ?? 1, winDmg = P.winDmg ?? 1.0, dmg0 = w.dmg;
  const selfRoot = arm === "B" || arm === "C" || arm === "D";
  const grow = arm === "G" || arm === "C" || arm === "D" || arm === "T";
  const canopy = arm === "B" || arm === "D" || arm === "T";
  let cd = 0;
  const release = () => { me.pin = 0; me.pinMax = 0; me.pinV = null; me.pinFree = 0; me.vx = 0; me.vy = 0; };
  return {
    onCast(t){
      cd = 0; w.spin = spin0 * spinMul; if (grow) w.dmg = dmg0 * winDmg;
      if (grow && boughs > 1){ w.blades = Array.from({length: boughs}, (_, i) => i / boughs); while (me.tips.length < boughs) me.tips.push([]); while (me.hitCd.length < boughs) me.hitCd.push(0); }
      if (selfRoot){ me.pinV = [0, 0]; me.pin = P.dur + 1; me.pinMax = P.dur + 1; me.pinFree = 1; }
    },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1;
      S.foeStk = (S.foeStk || 0) + foe.stacks("entangle");
      if (selfRoot && me.alive){ me.pin = P.dur + 1; }   // held for the whole window; released on close
      if (grow){ me.reachMul = Math.min(growCap, me.reachMul + growRate * dt); S._pk = Math.max(S._pk || 1, me.reachMul); }
      cd -= dt;
      if (canopy && foe.alive){
        const reach = w.reach * m.actMods.reach * me.reachMul * canopyMul;
        const d = Math.hypot(foe.x - me.x, foe.y - me.y);
        if (d < reach + H.R){ S.inCanopy = (S.inCanopy || 0) + 1;
          if (cd <= 0){ cd = canopyCd; foe.apply("entangle", canopyPer, me); S.stacks = (S.stacks || 0) + canopyPer; } }
      }
    },
    onClose(t, reason){
      w.spin = spin0; me.reachMul = 1; w.blades = blades0; w.dmg = dmg0;
      if (selfRoot) release();
      if (S._pk){ S.growPeak = (S.growPeak || 0) + S._pk; delete S._pk; }
    },
    end(){ w.spin = spin0; w.blades = blades0; w.dmg = dmg0; if (S._pk) delete S._pk; if (me.pinFree) release();
      S.f_foeStk = S.winFrames ? S.foeStk / S.winFrames : 0; S.f_canopyPct = S.winFrames ? 100 * (S.inCanopy || 0) / S.winFrames : 0;
      delete S.winFrames; delete S.foeStk; delete S.inCanopy; },
  };
}
