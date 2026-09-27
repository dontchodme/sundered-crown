// DAYBREAK, RICK'S CIRCLE (v99, Dawnbringer). Rick, 2026-09-27: "daybreak begins at a point of contact after a
// hit and grows in a circle from that point." The cast ARMS the blade; the first blow that lands after it breaks
// the dawn WHERE IT LANDED: a circle of sunlight anchored to that point grows from nothing and stays for `dur`
// seconds from the contact. A foe inside the circle is smitten +1 and takes tickDmg every tickCd (the v86 line's
// numbers, so the two mechanics price against each other on the same feed). The caster gets nothing.
//
// arms (the harness's letters; the mechanic reads its shape off them):
//   C  the circle grows for the WHOLE dur (r 0 -> rMax linearly over dur) — "the sun rises for eight seconds"
//   D  the circle grows over growT seconds to rMax and HOLDS there for the rest of dur — "the sun is up"
//   E  as D, but the circle is centred on the FOE at contact and FOLLOWS the foe (a control: the mechanic with
//      the counterplay removed, to price what anchoring costs — not a candidate)
// P: rMax (px), growT (s, arm D/E), dur (s from CONTACT), tickCd, tickDmg, smite, armMax (s the arming lasts;
//    0 = until a blow lands), reArm (1 = a new cast while a circle runs re-arms the blade; 0 = ignored)
({P, AC, m, me, foe, arm, S, rnd, H}) => {
  const rMax = P.rMax ?? 220, growT = P.growT ?? 1.5, tickCd = P.tickCd ?? 0.5, tickDmg = P.tickDmg ?? 2,
        smite = P.smite ?? 1, armMax = P.armMax ?? 0, reArm = P.reArm ?? 1;
  const follow = arm === "E";
  let armed = false, armedAt = 0, hits0 = 0;
  let C = null;                                    // the circle: { x, y, t0 }
  let cd = 0;
  const radius = (age) => {
    if (arm === "C") return rMax * Math.min(1, age / P.dur);
    return rMax * Math.min(1, age / growT);
  };
  return {
    onCast(t){
      S.casts_ = (S.casts_ || 0) + 1;
      if (C && !reArm) return;
      armed = true; armedAt = t; hits0 = me.hits;
    },
    onFrame(t, dt, open){
      // THE CONTACT. me.hits counts landed blows (resolveHit's own counter); the first one after the cast
      // breaks the dawn at the foe's centre (the build uses the blow's hit point, within ballR of this).
      if (armed){
        if (armMax > 0 && t - armedAt > armMax){ armed = false; S.f_armLapsed = (S.f_armLapsed || 0) + 1; }
        else if (me.hits > hits0 && foe.alive){
          armed = false;
          C = { x: foe.x, y: foe.y, t0: t };
          cd = 0;
          S.breaks = (S.breaks || 0) + 1;
          S.armWait = (S.armWait || 0) + (t - armedAt);
        }
      }
      if (!C) return;
      const age = t - C.t0;
      if (age >= P.dur || !me.alive){ C = null; return; }
      S.sunFrames = (S.sunFrames || 0) + 1;
      if (follow && foe.alive){ C.x = foe.x; C.y = foe.y; }
      const r = radius(age);
      cd -= dt;
      const inside = foe.alive && Math.hypot(foe.x - C.x, foe.y - C.y) < r + H.R;
      if (!inside) return;
      S.foeIn = (S.foeIn || 0) + 1;
      if (cd > 0) return;
      cd = tickCd;
      foe.apply("smite", smite, me);
      S.dmg = (S.dmg || 0) + H.hurt(foe, tickDmg, me);
      S.ticks = (S.ticks || 0) + 1;
    },
    onClose(t, reason){},
    end(){
      // per FIGHT: how long the blade waited for its blow, and how much of the sun's life the foe spent inside it
      S.f_armWait = S.breaks ? S.armWait / S.breaks : 0;
      S.f_foeInPct = S.sunFrames ? 100 * (S.foeIn || 0) / S.sunFrames : 0;
      S.f_breaks = S.breaks || 0;
      delete S.armWait; delete S.sunFrames; delete S.foeIn; delete S.casts_; delete S.breaks;
    },
  };
}
