// BULWARK, REDESIGNED (v77, Lightkeeper): for the window the greatsword IS the shield — the blade blocks:
// any foe blade that touches Lightkeeper's blade (a bind) is won regardless of mass, and the block BANKS ward
// (bankPer); arrows that touch the blade die and bank too. Every blow it lands banks its FULL damage (bankMul)
// instead of 0.55. arms: B = the block (binds won + arrows die, no bank) · C = B + banking on blocks · D = C + full-damage banking on blows
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const w = me.w, mass0 = w.mass, bankPer = P.bankPer ?? 10, bankMul = P.bankMul ?? 1.0, blockMass = P.blockMass ?? 12;
  const block = true, bankBlock = arm === "C" || arm === "D", bankBlow = arm === "D";
  const Wd = AC.STATUS.ward;
  let clanks = 0, hits = 0, dealt = 0;
  const bank = (n) => { if (!me.alive || n <= 0) return 0; const b0 = me.shield; me.shield = Math.min(Wd.cap, me.shield + n); me.shieldMax = Math.max(me.shieldMax, me.shield); me.apply("ward", 1); return me.shield - b0; };
  return {
    onCast(t){ clanks = me.clanks; hits = me.hits; dealt = me.dealt; if (block) w.mass = blockMass; },
    onFrame(t, dt, open){
      if (!open) return;
      S.winFrames = (S.winFrames || 0) + 1; S.shieldSum = (S.shieldSum || 0) + me.shield;
      if (me.clanks > clanks){ clanks = me.clanks; S.blocks = (S.blocks || 0) + 1; if (bankBlock) S.banked = (S.banked || 0) + bank(bankPer); }
      // arrows that touch the blade die
      if (block && m.shots.length){ const segs = m.bladeSegments(me);
        for (let i = m.shots.length - 1; i >= 0; i--){ const s = m.shots[i]; if (s.stuck) continue;
          for (const sg of segs){ if (H.segDist(s.x, s.y, sg.ax, sg.ay, sg.bx, sg.by) < (s.r || 6) + w.width * 0.5){ m.shots.splice(i, 1); S.arrows = (S.arrows || 0) + 1; if (bankBlock) S.banked = (S.banked || 0) + bank(bankPer * 0.5); break; } } } }
      if (bankBlow && me.hits > hits){ const d = me.dealt - dealt; dealt = me.dealt; hits = me.hits; if (d > 0) S.banked = (S.banked || 0) + bank(d * (bankMul - Wd.bank)); }
    },
    onClose(){ w.mass = mass0; },
    end(){ w.mass = mass0; S.f_shield = S.winFrames ? S.shieldSum / S.winFrames : 0; delete S.winFrames; delete S.shieldSum; },
  };
}
