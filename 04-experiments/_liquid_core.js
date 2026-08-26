/* ===================================================================== *
 *  THE SUNDERED CROWN — GLASS + LIQUID                                  *
 *  This block is the SHIPPABLE core.  liquid_build.py lifts it verbatim *
 *  into the game; the lab below only wraps it in a fake hall.           *
 *                                                                       *
 *  Nothing in here draws a health BAR.  The liquid IS the health, its   *
 *  level read against graduations etched in the glass — position on a   *
 *  common scale, which is the most accurately read encoding there is,   *
 *  and the one thing the ring never was.                                *
 * ===================================================================== */

/* ---------------------------------------------------------------- SLOSH ---
   The liquid's whole state, per relic, and it is ten numbers.

   THE ONE PHYSICAL LIE, STATED. A ball in free flight is in free fall, so a
   truly physical liquid inside it would be weightless — it would leave the
   floor of the sphere, ball up in the middle, and have no level at all
   between bounces. That is real and it is unreadable: the health encoding
   depends on the surface being a LEVEL. So the liquid is given the hall's
   down permanently, and only the NON-GRAVITATIONAL part of the ball's
   acceleration drives it. Everything you can see — wall bounce, floor slam,
   a warhammer landing, a clank — is exactly that part. Free flight is calm,
   contact is violent, which is also the rhythm the fight actually has.

   THREE CHANNELS, because a real slosh is three things at once:
     tilt   the surface pivots — the antisymmetric mode, and by far the
            largest. Driven by sideways force.
     heave  the whole level jumps and settles — driven by vertical force.
            This is what a landing looks like.
     ripple two standing modes on top, at gravity-wave frequencies, which
            is what stops the surface reading as a rigid plate.

   Each is a damped harmonic oscillator, integrated semi-implicitly at the
   simulation tick. Per-school stiffness and damping is what makes blood
   heave once and stop while sanctified light rings like a struck glass.  */
const SLOSH = {
  /* w  natural frequency (rad/s) · z  damping ratio · k  drive gain
     visc  0..1, how much the substance resists being a level at all      */
  mat: {
    sanctified: { w: 9.6, z: 0.10, k: 1.00, visc: 0.05, bub: 14, bubR: 0.9, bubV: 1.5, film: 0.30, tilt: 1.00 },
    bloodsworn: { w: 5.4, z: 0.46, k: 0.72, visc: 0.55, bub:  3, bubR: 1.5, bubV: 0.5, film: 0.75, tilt: 0.72 },
    dwarven:    { w: 4.1, z: 0.62, k: 0.55, visc: 0.80, bub:  4, bubR: 2.1, bubV: 0.35, film: 0.85, tilt: 0.58 },
    verdant:    { w: 6.8, z: 0.34, k: 0.85, visc: 0.40, bub:  7, bubR: 1.2, bubV: 0.8, film: 0.90, tilt: 0.84 },
    umbral:     { w: 5.9, z: 0.40, k: 0.78, visc: 0.50, bub:  5, bubR: 1.3, bubV: 0.6, film: 0.65, tilt: 0.78 },
    runic:      { w: 8.7, z: 0.14, k: 0.95, visc: 0.10, bub: 10, bubR: 0.8, bubV: 1.3, film: 0.25, tilt: 0.96 },
    vigil:      { w: 7.4, z: 0.26, k: 0.88, visc: 0.28, bub:  8, bubR: 1.0, bubV: 1.0, film: 0.45, tilt: 0.90 },
  },

  /* Everything below is WRITE-ONLY from the simulation's point of view. No
     field here is ever read by move, tickClank, damage or checkEnd, and none
     of it draws from this.rng() — so a match plays out identically whether
     these numbers are integrated or not. engine_ab is the proof. */
  init(f){
    f.slTilt = 0; f.slTiltV = 0;      // surface pivot, radians
    f.slHeave = 0; f.slHeaveV = 0;    // level offset, sim units
    f.slA2 = 0; f.slA2V = 0;          // symmetric ripple
    f.slA3 = 0; f.slA3V = 0;          // second ripple
    f.slVx = 0; f.slVy = 0;           // last tick's velocity, for the impulse
    f.slPx = f.x; f.slPy = f.y;       // last tick's position, for the freeze test
    f.slJolt = 0;                     // 0..1, decaying, for spray and film
    f.slDrip = 0;                     // leak phase; no rng anywhere near this
  },

  /* Per-school spring constants, derived once. The oscillator coefficients
     are pure functions of (w, z) and the four mode ratios, so recomputing
     them 480 times a second was 480 multiplies a second buying nothing. */
  prep(M){
    const mk = (wm, zm) => { const w = M.w * wm; return { k1: w * w, k2: 2 * M.z * zm * w }; };
    M._o = [mk(1, 1), mk(0.82, 1.15), mk(1.41, 0.72), mk(1.73, 0.60)];
    return M;
  },

  /* dt is the SIMULATION tick, so this runs at 120 Hz in the live page and at
     120 Hz in the offline render, and the two agree frame for frame.

     THE DRIVE IS AN IMPULSE, NOT AN ACCELERATION, and the first cut got that
     wrong in a way worth recording. It fed the measured acceleration into the
     oscillator as a forcing term — physically the right shape — and a floor
     bounce moved the surface by 0.0017 of a radius, which is a third of a
     pixel. A bounce is a WHOLE tick of a very large number: the acceleration
     exists for 1/120 s, so `force * dt` is the entire budget and it is
     nothing. What a bounce delivers is a step change in velocity, and the
     liquid's response to that is a step change in the oscillator's VELOCITY.

     Everything is driven off the velocity change the ball has already had —
     MINUS the free fall it was always going to have — so free flight is calm
     and every contact in the game drives this without a single call site
     having to know it exists. Wall bounce, floor slam, knockback from a
     warhammer, a clank, a Crucible launch: all of them are Δv.

     WRITTEN FLAT, AND THAT IS NOT PREMATURE. The readable version used a
     little `osc` closure returning `[x, v]` and destructured it four times
     per relic per tick. Measured on a 612-match sweep: 17.9 s became 26.7 s,
     a 49% tax on the whole simulation, and stubbing this one function
     recovered all of it. Four two-element arrays per relic per tick is about
     235 million throwaway allocations over that sweep — the cost was never
     the arithmetic. `verify.py` and `tune.py` run thousands of matches and
     draw none of them; they should not pay for a picture. */
  step(f, dt, gravY){
    if (f.slTilt === undefined) SLOSH.init(f);
    const M = f.slM || (f.slM = SLOSH.prep(SLOSH.mat[f.aff.key] || SLOSH.mat.runic));

    /* THE FREEZE TEST. Hit stop, the Harrowing's latch and the end of the
       match all stop calling move(), so no gravity was applied on those
       ticks — and subtracting it anyway would inject a phantom impulse every
       frozen frame and tip the liquid over during the exact beats the viewer
       is staring hardest at. The ball not having moved IS the frozen tick,
       exactly, and it costs two compares and no new coupling to the sim. */
    const moved = (f.x !== f.slPx || f.y !== f.slPy);
    f.slPx = f.x; f.slPy = f.y;
    const jx = f.vx - f.slVx;
    const jy = f.vy - f.slVy - (moved ? gravY * dt : 0);
    f.slVx = f.vx; f.slVy = f.vy;

    /* Saturating, because the roster's impulses span an order of magnitude —
       a lazy wall touch and a 2500 px/s warhammer launch must both produce a
       visible slosh, and a linear map makes one invisible or the other
       absurd. x/(|x|+k) rather than 1-exp(-|x|/k): same shape, monotone,
       smooth through zero, and one divide instead of a transcendental on the
       hot path of every headless sweep in the project. */
    const sx = jx / ((jx < 0 ? -jx : jx) + 700);
    const sy = jy / ((jy < 0 ? -jy : jy) + 700);
    const mg = Math.sqrt(sx * sx + sy * sy);
    if (mg > 0.06){ f.slJolt += mg; if (f.slJolt > 1) f.slJolt = 1; }
    f.slJolt -= dt * 2.2; if (f.slJolt < 0) f.slJolt = 0;

    const k = M.k, O = M._o;
    /* TILT — the antisymmetric mode, and the big one. Bounce off the right
       wall and the fluid keeps going right, piles up on that side, and the
       surface pivots. Per school: treacle barely tips, holy light tips all
       the way. */
    f.slTiltV += sx * 5.0 * k * M.tilt;
    /* HEAVE — the whole body drops into the floor on a landing and surges
       back. Deliberately the smallest of the three: heave is the one that
       moves the LEVEL, and the level is the health reading, so a big one
       would make the instrument lie for half a second every bounce. */
    f.slHeaveV += -sy * 1.6 * k;
    /* RIPPLE — two standing modes at gravity-wave frequencies, which go as
       sqrt(n) for a basin this size. Without them the surface is a rigid
       plate on a hinge, and a rigid plate is not a liquid. */
    f.slA2V += (-sy * 0.62 - sx * 0.40) * 1.8 * k;
    f.slA3V += ( sx * 0.55 - sy * 0.30) * 1.2 * k;

    f.slTiltV  += (-O[0].k1 * f.slTilt  - O[0].k2 * f.slTiltV ) * dt;
    f.slHeaveV += (-O[1].k1 * f.slHeave - O[1].k2 * f.slHeaveV) * dt;
    f.slA2V    += (-O[2].k1 * f.slA2    - O[2].k2 * f.slA2V   ) * dt;
    f.slA3V    += (-O[3].k1 * f.slA3    - O[3].k2 * f.slA3V   ) * dt;
    f.slTilt  += f.slTiltV  * dt;
    f.slHeave += f.slHeaveV * dt;
    f.slA2    += f.slA2V    * dt;
    f.slA3    += f.slA3V    * dt;

    /* Clamps, and each is a legibility budget rather than a physical limit.
       Past about 55 degrees a surface stops reading as a level and the whole
       encoding goes with it; past a tenth of a radius of heave the instrument
       is telling a visible lie about the number it exists to report. The
       velocity is reflected rather than zeroed, so a clamp reads as the fluid
       hitting the top of the glass instead of as a freeze.

       THE BUDGET, DERIVED, because a health readout that wobbles is a health
       readout that lies -- and my first two attempts at deriving it were both
       wrong in ways the probe caught rather than I did.

       The full scale is 1.64 R for 300 HP, so 0.01 R of surface is 1.8 HP.

       WHAT A VIEWER READS is not the surface at the centre. It is the
       boundary averaged across the width, and the width of a sphere is a
       chord -- so the average is weighted by sqrt(1-u^2), not uniform. That
       matters, and it is where attempt one went wrong: under a UNIFORM
       average the tilt and both cosine modes integrate to exactly zero, so
       the reading would be level+heave and heave alone would be the budget.
       Under the chord weight the cosines do NOT vanish. For the nth mode the
       weighted mean picks up J1(n*pi)/(n*pi/2) of its amplitude, which is
       0.181 for mode 2 and about 0.08 for mode 3. So:

         reading error  <=  heave + 0.181*A2 + 0.08*A3
                        =   0.060 + 0.0199 + 0.0080   =  0.088 R  ~=  16 HP

       and 16 HP for the few tenths of a second after a landing is a price
       worth paying for the thing being asked for. The clamps above are set
       FROM that sum, not the other way round.

       There is deliberately NO pointwise bound. Attempt two tried to bound
       the worst point on the surface and the probe returned 0.60 R against a
       claimed 0.274 -- because the tilt term is u*tan(theta), which at the
       rim with theta near its 0.92 clamp is 1.3 R on its own. That is not a
       defect: a tilted surface pivots about the centre, the ends go where the
       ends go, and the chord is zero out there anyway. Tilt is bounded by
       being unbiased, which the weighted mean above already proves, and by
       staying far from the clamp in real play, which the probe measures
       directly.

       */
    if (f.slTilt >  0.92){ f.slTilt =  0.92; f.slTiltV = -f.slTiltV * 0.35; }
    else if (f.slTilt < -0.92){ f.slTilt = -0.92; f.slTiltV = -f.slTiltV * 0.35; }
    if (f.slHeave >  0.060){ f.slHeave =  0.060; f.slHeaveV = -f.slHeaveV * 0.35; }
    else if (f.slHeave < -0.060){ f.slHeave = -0.060; f.slHeaveV = -f.slHeaveV * 0.35; }
    if (f.slA2 >  0.110){ f.slA2 =  0.110; f.slA2V = -f.slA2V * 0.35; }
    else if (f.slA2 < -0.110){ f.slA2 = -0.110; f.slA2V = -f.slA2V * 0.35; }
    if (f.slA3 >  0.100){ f.slA3 =  0.100; f.slA3V = -f.slA3V * 0.35; }
    else if (f.slA3 < -0.100){ f.slA3 = -0.100; f.slA3V = -f.slA3V * 0.35; }
  },

  /* The surface height, in ball-radius units, at horizontal offset u (also in
     radius units, -1..1). Pure function of the state above — the renderer,
     the crack-leak test and the bubble test all call this one function, so
     they cannot disagree about where the liquid is. */
  surf(f, u, lvl){
    return lvl + (f.slHeave || 0)
         + u * Math.tan(f.slTilt || 0)
         + (f.slA2 || 0) * Math.cos(Math.PI * u)
         + (f.slA3 || 0) * Math.cos(2 * Math.PI * u + 1.1);
  },
};

/* THE LEVEL, and why it is not the whole diameter. hpFrac 0 leaves a sliver
   in the bottom of the glass rather than a dry sphere, and hpFrac 1 leaves a
   thumb of headspace at the top rather than a solid ball — a vial filled to
   the brim reads as a solid object, and the whole point is that this one is a
   container. The band is also where Curse's dead cap lives. */
const MARKS = { mode: "none" };      // "none" | "desperation" | "ticks"

/* THE FRACTURE, OFF BY DEFAULT. Rick, on sight of the first in-game build:
   *"i also think the glass cracking is a bit distracting and im not sure we
   need it ... lets add it back later if we feel like we need it"*.

   The whole pattern is kept and so is its optics work -- glassCracks,
   drawGlassFracture, the chipped silhouette and the vents are all live code
   behind this switch, because the argument for a second damage channel is a
   real one and it may well come back. What it costs while it is off is
   honestly stated: the relic's health is now carried by the LEVEL and by
   nothing else on the ball, plus the vapour and the halo, which are both
   restatements of the same number rather than independent readings.

   It also switches off the leak. A spill needs a hole, the holes are where
   the fracture arms reach the shell, and liquid jetting out of a visibly
   intact sphere reads as a defect rather than as damage. Turning FRACTURE.on
   back on in the console restores the cracks, the chipped silhouette and the
   spill together, which is the honest bundle. */
const FRACTURE = { on: false };
const LV_TOP = -0.84, LV_BOT = 0.80;
function lvlOf(frac){ return LV_TOP + (1 - frac) * (LV_BOT - LV_TOP); }

/* ------------------------------------------------------- GLASS FRACTURE ---
   Stone and glass do not break the same way and the old pattern was stone:
   jagged runs inward from the rim, wobbling where they hit the grain. Glass
   has no grain. It fails from a POINT, and the signature is unmistakable —
   the one everybody has seen in a windscreen:

     the crush zone   a small pulverised star where the thing actually hit
     radial arms      near-straight lines fleeing the point, kinking sharply
                      and only occasionally, because there is nothing to
                      deflect them but the stress field itself
     hackle rings     arcs at growing radius, scalloped between the arms,
                      and they arrive AFTER the radials, which is the real
                      sequence and the reason it reads as a process

   And the optics invert. A crack in stone is a dark gap: the note on the old
   pattern says "the dark has to dominate", and it was right about stone. A
   crack in glass is a mirror — an internal surface at a steep angle to the
   eye, total-internally-reflecting whatever light there is. It is the
   BRIGHTEST thing on the object, with only a hairline of true dark in it.
   That single inversion is most of what says glass.

   Still a pure function of (side, index). No simulation RNG, no animation
   state: each site owns a damage threshold and grows in over a window as
   damage crosses it, so a heal retracts the whole network by itself, in
   reverse, exactly as the stone version did. */
const GLASS_CACHE = {};
function glassCracks(side){
  if (GLASS_CACHE[side]) return GLASS_CACHE[side];
  const N = 6, out = [];

  /* One arm: near-straight, with rare hard kinks. The old stone run used a
     large angular wobble everywhere; this uses almost none, and then turns
     sharply once or twice. Straightness is the tell — a wandering line reads
     as drawn on the surface, a straight line that suddenly forks reads as
     something that failed. */
  const arm = (seed, x0, y0, a0, len, steps) => {
    const pts = [[x0, y0]];
    let x = x0, y = y0, a = a0;
    for (let s = 0; s < steps; s++){
      const kink = shellHash(seed, s * 7 + 3) > 0.78 ? 1 : 0;
      a += kink ? (shellHash(seed, s * 7 + 5) - 0.5) * 0.85
                : (shellHash(seed, s * 7 + 5) - 0.5) * 0.07;
      const st = len / steps;
      x += Math.cos(a) * st; y += Math.sin(a) * st;
      pts.push([x, y]);
      if (x * x + y * y > 1.35) break;       // off the shell; the clip finishes it
    }
    return pts;
  };

  for (let i = 0; i < N; i++){
    const h = (k) => shellHash(side * 91 + 17, i * 13 + k);
    /* Thresholds walk up the damage range so sites arrive steadily through
       the fight rather than all at once, with scatter so it never looks
       metered. Seven sites over 300 HP is one every ~43 points. */
    const thr = 0.10 + (i / N) * 0.74 + (h(1) - 0.5) * 0.06;
    const sa  = i * 2.399963 + h(2) * 0.7;          // golden angle, well spread
    const sr  = 0.16 + h(3) * 0.66;                 // biased off-centre
    const sx  = Math.cos(sa) * sr, sy = Math.sin(sa) * sr;

    const na = 3 + Math.floor(h(4) * 3);            // 3..5 radials
    const arms = [];
    for (let b = 0; b < na; b++){
      const aa = (b / na) * Math.PI * 2 + h(5) * 1.3
               + (shellHash(side * 31 + i, b * 3 + 1) - 0.5) * 0.42;
      const len = (0.17 + shellHash(side * 31 + i, b * 3 + 2) * 0.34);
      arms.push({ pts: arm(side * 401 + i * 11 + b, sx, sy, aa, len, 4),
                  w: 0.55 + shellHash(side * 31 + i, b * 3 + 3) * 0.9 });
    }

    /* Hackle rings, scalloped between the arms rather than circular — a true
       ring crack bows outward between the radials that anchor it. */
    const nr = 1 + (h(6) > 0.62 ? 1 : 0);
    const rings = [];
    for (let k = 0; k < nr; k++){
      const rad = (0.075 + k * 0.085 + h(7 + k) * 0.055);
      const pts = [];
      const M = 16;
      for (let s = 0; s <= M; s++){
        const a = (s / M) * Math.PI * 2;
        const bow = 1 + Math.cos(a * na - h(5) * 1.3 * na) * 0.085;
        pts.push([sx + Math.cos(a) * rad * bow, sy + Math.sin(a) * rad * bow]);
      }
      rings.push({ pts, delay: 0.34 + k * 0.24, w: 0.38 + h(9 + k) * 0.34 });
    }

    out.push({ thr, sx, sy, sr, arms, rings,
               /* a site out near the rim takes a straight-edged bite out of
                  the silhouette; glass does not chip in rounded scallops */
               chip: sr > 0.62 && h(12) > 0.52,
               chipA: sa, chipW: 0.10 + h(13) * 0.10 });
  }
  return (GLASS_CACHE[side] = out);
}

/* How far along a site's growth we are, 0..1, given total damage. Radials
   fill first, rings follow — `delay` is a fraction of this same window. */
function siteGrow(ck, dmg){ return Math.max(0, Math.min(1, (dmg - ck.thr) / 0.12)); }

/* ------------------------------------------------------- THE SILHOUETTE ---
   Glass does not chip in rounded scallops. A site out near the rim takes a
   straight-edged bite — a chord — and the depth of the chord is the growth.
   Silhouette is still the strongest channel there is: it survives motion
   blur, thumbnail scale and peripheral vision, none of which a hairline or a
   hue does. */
function glassPath(f, R, dmg, cx, cy){
  cx = cx === undefined ? f.x : cx;
  cy = cy === undefined ? f.y : cy;
  const p = new Path2D();
  const cuts = [];
  /* No fracture, no chip. A straight-edged bite out of the rim with no
     crack running to it does not read as damage, it reads as a rendering
     fault -- the notch and the split have to ship together or neither. */
  if (FRACTURE.on) for (const ck of glassCracks(f.side)){
    if (!ck.chip) continue;
    const g = siteGrow(ck, dmg);
    if (g < 0.55) continue;
    const depth = ck.chipW * 0.62 * (g - 0.55) / 0.45;
    cuts.push([ck.chipA, 1 - depth, Math.acos(Math.max(0, Math.min(1, 1 - depth)))]);
  }
  const N = 128;
  for (let i = 0; i <= N; i++){
    const a = (i / N) * Math.PI * 2;
    let rad = 1;
    for (const [ca, d, halfW] of cuts){
      let da = ((a - ca) % (Math.PI * 2) + Math.PI * 3) % (Math.PI * 2) - Math.PI;
      if (Math.abs(da) < halfW) rad = Math.min(rad, d / Math.cos(da));
    }
    const x = cx + Math.cos(a) * rad * R, y = cy + Math.sin(a) * rad * R;
    i ? p.lineTo(x, y) : p.moveTo(x, y);
  }
  p.closePath();
  return p;
}

/* The body of liquid, as a closed path in ball-local units times R. Sampled
   wide of the shell on both sides and carried well below it, so the shell
   clip is what gives it its edges — which is exactly right, because the
   glass is what gives the real liquid its edges too. */
function liquidPoly(f, R, lvl){
  const p = new Path2D();
  const M = 30;
  for (let i = 0; i <= M; i++){
    const u = -1.25 + (i / M) * 2.5;
    const y = SLOSH.surf(f, u, lvl) * R;
    i ? p.lineTo(u * R, y) : p.moveTo(u * R, y);
  }
  p.lineTo(1.25 * R, 2.0 * R);
  p.lineTo(-1.25 * R, 2.0 * R);
  p.closePath();
  return p;
}
function headPoly(f, R, lvl){         // the headspace: everything above it
  const p = new Path2D();
  const M = 30;
  for (let i = 0; i <= M; i++){
    const u = -1.25 + (i / M) * 2.5;
    const y = SLOSH.surf(f, u, lvl) * R;
    i ? p.lineTo(u * R, y) : p.moveTo(u * R, y);
  }
  p.lineTo(1.25 * R, -2.0 * R);
  p.lineTo(-1.25 * R, -2.0 * R);
  p.closePath();
  return p;
}

/* Colour helpers. #RRGGBB + alpha 0..1 -> #RRGGBBAA, because every colour in
   this game is already a hex literal and mixing in rgba() strings would mean
   two conventions in one file. */
function hexA(h, a){
  const v = Math.max(0, Math.min(255, Math.round(a * 255))).toString(16);
  return h + (v.length < 2 ? "0" + v : v);
}
function mix(h1, h2, t){
  const p = (h, i) => parseInt(h.slice(1 + i * 2, 3 + i * 2), 16);
  const o = [0, 1, 2].map(i => Math.round(p(h1, i) + (p(h2, i) - p(h1, i)) * t));
  return "#" + o.map(v => v.toString(16).padStart(2, "0")).join("");
}

/* ====================================================== THE RELIC ITSELF ===
   Draw order is the whole effect and it is the order light actually takes:

     the far wall of the glass          (dark interior, dimmest at the rim)
     what is inside it                  (vapour above, liquid below)
     the boundary between them          (meniscus, and the tide the last hit left)
     what is etched INTO the glass      (graduations, the Curse cap)
     what is broken IN the glass        (fracture)
     what reflects OFF the near wall    (rim light, speculars, caustic)

   Get that order wrong in either direction and it stops being a container:
   speculars under the liquid make it a painted ball, and graduations under
   the liquid make them float in the fluid instead of being scratched in the
   wall.                                                                    */
function drawGlassRelic(c, m, f, R, o){
  o = o || {};
  const A = f.aff, MT = SLOSH.mat[A.key] || SLOSH.mat.runic;
  const base = o.base || 300;
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));
  const hpFrac    = cl(f.hp / base, 0, 1);
  const maxFrac   = cl(f.maxHp / base, 0, 1);
  const ghostFrac = cl((f.hpGhost == null ? f.hp : f.hpGhost) / base, 0, 1);
  const dmg = 1 - hpFrac;
  const lvl = lvlOf(hpFrac), glv = lvlOf(ghostFrac);
  const t = m.t;
  const mend = f.mend > 0;

  const shell = glassPath(f, R, dmg, 0, 0);
  const liq   = liquidPoly(f, R, lvl);
  const head  = headPoly(f, R, lvl);

  c.save();
  c.translate(f.x, f.y);

  /* 0. THE HALO. A full relic throws its own light into the hall and a
     drained one does not, so the glow is one more reading of the same number
     — and it is the one that works at thumbnail size, where the level itself
     is four pixels of travel. */
  c.save();
  c.shadowColor = A.core;
  c.shadowBlur = 8 + hpFrac * 26;
  c.fillStyle = hexA(mix(A.dark, "#05040A", 0.6), 0.95);
  c.fill(shell);
  c.restore();

  /* 1. THE FAR WALL. Nearly black, lifted a little toward the school's own
     dark at the centre so an empty relic is still identifiably itself. */
  const gi = c.createRadialGradient(-R * 0.2, -R * 0.25, R * 0.1, 0, 0, R);
  gi.addColorStop(0, mix(A.dark, "#07060C", 0.80));
  gi.addColorStop(0.72, mix(A.dark, "#05040A", 0.90));
  gi.addColorStop(1, "#040308F0");
  c.fillStyle = gi;
  c.fill(shell);

  c.save();
  c.clip(shell);

  /* 2a. VAPOUR. What the liquid leaves behind is not nothing — it is the
     relic's own substance, off the boil, and it fills the headspace as the
     glass empties. This is what keeps a dying relic identifiable: at 8 HP
     there is almost no liquid left to carry the colour, and the fog is the
     only thing still saying which school this is. */
  if (dmg > 0.015){
    c.save();
    c.clip(head);
    const dens = Math.min(1, dmg * 1.15);
    for (let i = 0; i < 5; i++){
      const h1 = shellHash(f.side * 61 + 7, i * 3 + 1);
      const h2 = shellHash(f.side * 61 + 7, i * 3 + 2);
      const ph = t * (0.07 + h1 * 0.11) + h2 * 6.283;
      const vx = Math.sin(ph) * R * 0.46 + (h1 - 0.5) * R * 0.5;
      const vy = lvl * R - R * (0.10 + h2 * 0.42)
               + Math.cos(ph * 0.77) * R * 0.16;
      const rr = R * (0.34 + h1 * 0.30);
      const vg = c.createRadialGradient(vx, vy, 0, vx, vy, rr);
      vg.addColorStop(0, hexA(A.glow, 0.16 * dens));
      vg.addColorStop(0.55, hexA(A.core, 0.075 * dens));
      vg.addColorStop(1, hexA(A.core, 0));
      c.fillStyle = vg;
      c.beginPath(); c.arc(vx, vy, rr, 0, Math.PI * 2); c.fill();
    }
    c.restore();
  }

  /* 2b. THE LIQUID. The gradient runs along the surface NORMAL, not down the
     screen — so when the relic is thrown into a wall and the surface pivots
     forty degrees, the light in the fluid pivots with it. Down the screen
     was the first cut and it read as a painted-on gradient the instant the
     ball was struck, which is the exact moment anyone is looking. */
  const th = f.slTilt || 0;
  const nx = Math.sin(th), ny = Math.cos(th);      // unit normal, into the fluid
  const s0x = -Math.sin(th) * 0, s0y = lvl * R;
  const lg = c.createLinearGradient(s0x, s0y, s0x + nx * R * 2.0, s0y + ny * R * 2.0);
  const hot = mix(A.core, "#FFFFFF", 0.30);
  lg.addColorStop(0.00, mend ? "#FFF4D0" : hot);
  lg.addColorStop(0.10, A.core);
  lg.addColorStop(0.52, mix(A.core, A.dark, 0.55));
  lg.addColorStop(1.00, A.dark);
  c.save();
  c.clip(liq);
  c.fillStyle = lg;
  c.fillRect(-R * 1.3, -R * 1.3, R * 2.6, R * 2.6);

  /* The submerged rim. Light entering the glass from behind the fluid is bent
     back along the wall, so the boundary between liquid and glass is the
     brightest part of the fluid — and because the clip is (shell AND liquid)
     this lands on exactly the arc that is actually wet. It is also, with no
     extra work, a second statement of the level: the bright rim stops where
     the liquid does. */
  c.strokeStyle = hexA(mix(A.glow, "#FFFFFF", 0.2), 0.55);
  c.lineWidth = 3.2;
  c.stroke(shell);
  c.strokeStyle = hexA(A.glow, 0.9);
  c.lineWidth = 1.1;
  c.stroke(shell);

  /* Bubbles, rising from the floor of the glass to the surface. Count, size
     and rate are the school's: sanctified fizzes, dwarven turns over three
     fat slow ones, blood barely moves. Position is a pure function of
     (side, index, t) — never rng, so this is identical in the live page and
     in the offline render. */
  const NB = MT.bub;
  for (let i = 0; i < NB; i++){
    const h1 = shellHash(f.side * 131 + 5, i * 5 + 1);
    const h2 = shellHash(f.side * 131 + 5, i * 5 + 2);
    const h3 = shellHash(f.side * 131 + 5, i * 5 + 3);
    const u  = (h1 * 2 - 1) * 0.80;
    const flr = Math.sqrt(Math.max(0.02, 1 - u * u));       // inside of the sphere
    const srf = SLOSH.surf(f, u, lvl);
    if (srf >= flr - 0.06) continue;                         // no fluid at this u
    const ph = (t * (0.20 + h2 * 0.34) * MT.bubV + h3) % 1;
    const by = flr + (srf - flr) * ph;
    const bx = u + Math.sin(t * (1.6 + h2 * 2.2) + h3 * 6.283) * 0.035;
    const br = (0.016 + h3 * 0.028) * MT.bubR * R * (0.55 + ph * 0.75);
    c.globalAlpha = (1 - ph) * 0.42 + 0.16;
    /* a bubble is a hole in the fluid, not a dot painted on it: a dark
       shadow under it and a bright lip on the lit side */
    c.fillStyle = hexA("#05040A", 0.30);
    c.beginPath(); c.arc(bx * R + br * 0.2, by * R + br * 0.25, br, 0, Math.PI * 2); c.fill();
    c.fillStyle = hexA(mix(A.glow, "#FFFFFF", 0.45), 0.85);
    c.beginPath(); c.arc(bx * R - br * 0.22, by * R - br * 0.26, br * 0.72, 0, Math.PI * 2); c.fill();
  }
  c.globalAlpha = 1;
  c.restore();

  /* 2c. THE FILM. The fluid does not leave a dry wall behind — it drags a
     sheet up the glass and that sheet runs back down. Alpha rides slJolt, so
     it appears on the frames after contact and is gone a moment later, which
     is when a real film is visible and when it is not. Sap clings, holy light
     barely wets the glass at all. */
  if ((f.slJolt || 0) > 0.02 && MT.film > 0){
    c.save();
    c.clip(head);
    c.strokeStyle = hexA(A.core, Math.min(0.5, f.slJolt * 0.55 * MT.film));
    c.lineWidth = 4.5;
    c.stroke(shell);
    c.restore();
  }

  /* 3a. THE TIDE. hpGhost lags hp by a few tenths, so the band between the
     two surfaces IS the bite that was just taken. The old gauge said this
     with a pale arc; here it is a wet mark the fluid has just fallen away
     from, which is the same information in the language of the object. */
  if (ghostFrac > hpFrac + 0.002){
    const band = new Path2D();
    const Mn = 26;
    for (let i = 0; i <= Mn; i++){
      const u = -1.2 + (i / Mn) * 2.4;
      const y = SLOSH.surf(f, u, lvl) * R;
      i ? band.lineTo(u * R, y) : band.moveTo(u * R, y);
    }
    for (let i = Mn; i >= 0; i--){
      const u = -1.2 + (i / Mn) * 2.4;
      band.lineTo(u * R, SLOSH.surf(f, u, glv) * R);
    }
    band.closePath();
    /* The first cut filled this cream at 0.30 and the sheet read it as a
       SECOND FLUID sitting on top of the first — a layer of oil, not a mark.
       It is glass the liquid has just left: the school's own colour, thin,
       with one bright line at the high-water edge. */
    c.fillStyle = hexA(A.core, 0.085);
    c.fill(band);
    c.save();
    c.clip(band);
    c.strokeStyle = hexA("#FFE9C0", 0.30); c.lineWidth = 1.4;
    c.stroke(band);
    c.restore();
  }

  /* 3b. THE MENISCUS. Two strokes and they are not the same thing: a hairline
     of true dark where the surface turns away from the eye, and a bright
     line where it turns toward it. One stroke alone reads as a line drawn
     across the ball; two read as an edge. */
  const men = new Path2D();
  const Ms = 30;
  for (let i = 0; i <= Ms; i++){
    const u = -1.15 + (i / Ms) * 2.3;
    const y = SLOSH.surf(f, u, lvl) * R;
    i ? men.lineTo(u * R, y) : men.moveTo(u * R, y);
  }
  c.lineJoin = "round"; c.lineCap = "round";
  /* TWO STROKES AND THEY ARE NOT INTERCHANGEABLE. A shadow band a little
     BELOW the surface, inside the fluid, and a bright hairline exactly ON it.
     Either one alone fails on half the roster: a white line on Dawnbringer's
     near-white liquid is invisible, and a dark line on Nightfell's is. One of
     each guarantees the boundary separates by VALUE whatever it sits on —
     the same principle the ward plates and the gauge bevel already record. */
  c.save();
  c.clip(liq);
  c.strokeStyle = hexA("#05040A", 0.50); c.lineWidth = 3.4;
  c.save(); c.translate(0, 2.0); c.stroke(men); c.restore();
  c.restore();
  c.save();
  c.shadowColor = mend ? "#FFF4D0" : A.glow; c.shadowBlur = 7;
  c.strokeStyle = mend ? "#FFF4D0" : mix(A.glow, "#FFFFFF", 0.55);
  c.lineWidth = 1.7;
  c.stroke(men);
  c.restore();

  c.restore();     /* ---- out of the shell clip for the etch and the optics */
  c.restore();     /* ---- out of the translate; the rest re-enters it       */
  c.save();
  c.translate(f.x, f.y);
  c.save();
  c.clip(shell);

  /* 4a. CURSE'S DEAD CAP. Maximum life eaten for good is the part of the
     glass the liquid can never reach again — frosted, and drawn at the TOP
     where a full relic's fluid used to be. The old ring drew it in umbral at
     the far end of the health arc, where a viewer who has not read the code
     reads it as health. Here it is unmistakably not health: it is the part of
     the vessel that is finished. */
  if (maxFrac < 0.999){
    const y0 = lvlOf(1) * R, y1 = lvlOf(maxFrac) * R;
    c.save();
    const fg = c.createLinearGradient(0, y0 - R * 0.06, 0, y1);
    fg.addColorStop(0, hexA(AFF_UMBRAL.dark, 0.85));
    fg.addColorStop(1, hexA(AFF_UMBRAL.core, 0.30));
    c.fillStyle = fg;
    c.fillRect(-R, y0 - R * 0.3, R * 2, (y1 - y0) + R * 0.3);
    /* frost: deterministic crystals so it reads as the glass going bad
       rather than as a purple wash laid over it */
    c.globalAlpha = 0.5;
    c.fillStyle = hexA(AFF_UMBRAL.glow, 0.5);
    for (let i = 0; i < 22; i++){
      const h1 = shellHash(f.side * 211, i * 3 + 1), h2 = shellHash(f.side * 211, i * 3 + 2);
      const fx = (h1 * 2 - 1) * R * 0.95;
      const fy = y0 + (y1 - y0) * h2;
      const s = 0.7 + h1 * 1.5;
      c.beginPath(); c.arc(fx, fy, s, 0, Math.PI * 2); c.fill();
    }
    c.globalAlpha = 1;
    c.strokeStyle = hexA(AFF_UMBRAL.core, 0.75); c.lineWidth = 1.2;
    c.beginPath(); c.moveTo(-R, y1); c.lineTo(R, y1); c.stroke();
    c.restore();
  }

  /* 4b. THE GRADUATIONS. The v5 finding was that four countable chunks beat a
     continuous arc, because a count needs no scale, no reference and no
     estimate — and it survives motion blur, a thumbnail and peripheral
     vision. That finding is kept; only the instrument changed. The chunks are
     now the four bands of a measuring vessel and the liquid is the level, so
     the reading is POSITION ON A COMMON SCALE, which is the most accurately
     read encoding there is and strictly better than the angle it replaces.

     The third line from the top is at 0.25 = CONFIG.desperation.at, so the
     frame the liquid falls past it is the frame the simulation changes gear.
     Etched, not painted: a dark groove with a lit lip above it, because that
     is what a scratch in glass looks like and it is legible over fluid,
     vapour and fracture alike. Horizontal in WORLD space and never in the
     liquid's — the glass does not tip, and if the scale tipped with the fluid
     there would be nothing to read the fluid against. */
  /* 4b. THE GRADUATIONS -- OFF BY DEFAULT.

     v5 established that four countable chunks beat a continuous arc, and that
     finding is not being thrown away lightly. But the marks were built for an
     arc that had no reference of its own, and a vessel does not have that
     problem: the glass IS the scale. Full is the top of the sphere, empty is
     the bottom, both ends are always on screen, and the reading is a position
     between two fixed points a viewer can see without being told. The marks
     were answering a question the new instrument does not ask, and on the
     first sheet they read as a clock face painted on a marble.

     What is genuinely lost is the ONE boundary that is not arbitrary:
     CONFIG.desperation.at, the frame the simulation changes gear. `MARKS.mode
     = "desperation"` draws that line and nothing else; `"ticks"` restores all
     four. Both live in the page so the choice can be re-made on pictures
     rather than from memory. */
  const MK = MARKS.mode;
  if (MK !== "none"){
    for (let q = 1; q <= 4; q++){
      const fr = q / 4;
      const major = q === 1;                          // the desperation line
      if (MK === "desperation" && !major) continue;
      if (fr > maxFrac + 0.001) continue;             // eaten by Curse; no mark
      const y = lvlOf(fr) * R;
      const halfW = Math.sqrt(Math.max(0, R * R - y * y));
      const len = (major ? 0.30 : 0.20) * R;
      c.lineCap = "butt";
      for (const dir of [-1, 1]){
        const xe = dir * halfW, xi = dir * Math.max(0, halfW - len);
        c.strokeStyle = hexA("#05040A", 0.62);
        c.lineWidth = major ? 2.6 : 1.9;
        c.beginPath(); c.moveTo(xi, y + 0.8); c.lineTo(xe, y + 0.8); c.stroke();
        c.strokeStyle = hexA("#FFFFFF", major ? 0.72 : 0.46);
        c.lineWidth = major ? 1.7 : 1.15;
        c.beginPath(); c.moveTo(xi, y - 0.4); c.lineTo(xe, y - 0.4); c.stroke();
      }
      if (major){
        c.strokeStyle = hexA("#FFFFFF", 0.22);
        c.lineWidth = 1.1;
        c.beginPath(); c.moveTo(-halfW, y - 0.4); c.lineTo(halfW, y - 0.4); c.stroke();
      }
    }
  }

  /* 5. THE FRACTURE. */
  if (FRACTURE.on) drawGlassFracture(c, m, f, R, dmg, lvl);

  c.restore();      /* out of the shell clip */

  /* 6. THE NEAR WALL — everything that reflects off the outside of the glass.
     All of it on TOP of the fluid, because that is where it physically is,
     and putting any of it underneath is what makes a glass ball read as a
     painted marble. Light is upper-left, the same direction every other
     gradient in this game already uses. */
  /* thickness: the wall is dark where you look through the most of it */
  const wall = c.createRadialGradient(0, 0, R * 0.62, 0, 0, R);
  wall.addColorStop(0, "#00000000");
  wall.addColorStop(0.86, hexA("#080610", 0.30));
  wall.addColorStop(1, hexA("#080610", 0.72));
  c.fillStyle = wall;
  c.fill(shell);

  /* the lit rim: bright where the light strikes, and a cold bounce opposite */
  c.save();
  c.lineJoin = "round";
  c.strokeStyle = hexA("#FFFFFF", 0.22); c.lineWidth = 1.4;
  c.stroke(shell);
  c.beginPath();
  c.arc(0, 0, R * 0.97, Math.PI * 1.02, Math.PI * 1.62);
  c.strokeStyle = hexA("#FFFFFF", 0.52); c.lineWidth = 1.7;
  c.shadowColor = "#FFFFFF"; c.shadowBlur = 4;
  c.stroke();
  c.beginPath();
  c.arc(0, 0, R * 0.94, Math.PI * 0.08, Math.PI * 0.66);
  c.strokeStyle = hexA(mix(A.glow, "#FFFFFF", 0.4), 0.30 + hpFrac * 0.26);
  c.lineWidth = 2.1; c.shadowColor = A.glow; c.shadowBlur = 7;
  c.stroke();
  c.restore();

  /* the speculars. Two of them, hard and small, because that is what a hard
     smooth surface does and a single soft blob is what plastic does. */
  c.save();
  c.globalCompositeOperation = "lighter";
  const sg = c.createRadialGradient(-R * 0.40, -R * 0.44, 0, -R * 0.40, -R * 0.44, R * 0.58);
  sg.addColorStop(0, hexA("#FFFFFF", 0.15));
  sg.addColorStop(1, "#FFFFFF00");
  c.fillStyle = sg;
  c.beginPath(); c.arc(-R * 0.40, -R * 0.44, R * 0.58, 0, Math.PI * 2); c.fill();

  c.fillStyle = hexA("#FFFFFF", 0.62);
  c.save();
  c.translate(-R * 0.40, -R * 0.46); c.rotate(-0.62);
  c.beginPath(); c.ellipse(0, 0, R * 0.20, R * 0.075, 0, 0, Math.PI * 2); c.fill();
  c.restore();
  c.fillStyle = hexA("#FFFFFF", 0.50);
  c.save();
  c.translate(-R * 0.62, -R * 0.16); c.rotate(-0.62);
  c.beginPath(); c.ellipse(0, 0, R * 0.10, R * 0.05, 0, 0, Math.PI * 2); c.fill();
  c.restore();
  c.restore();
  c.restore();
}

const AFF_UMBRAL = AFFINITIES.umbral;

/* --------------------------------------------------------- THE FRACTURE ---
   Four passes, and the order is the inversion. Stone wanted the dark to
   dominate — a crack in rock is a gap, and the note on the old pattern said
   so and was right. Glass is the opposite: the fracture is an internal
   surface at a steep angle to the eye, so it reflects, and it is the
   BRIGHTEST thing on the object with a hairline of true dark inside it.

     bloom   light scattering out of the whole network
     lens    the fracture surface itself, wide and pale — the body of it
     core    a hairline of real dark, the gap seen edge on
     spec    a hard white lip offset to the lit side, which is the sparkle

   Batched by quantised width into one Path2D per bucket per pass, for the
   reason the old note gives at length: the cost is CALL COUNT, and stroking
   1700 two-point paths costs 86 ms while stroking 40 batched ones costs 3. */
function drawGlassFracture(c, m, f, R, dmg, lvl){
  const sites = glassCracks(f.side);
  const A = f.aff;
  const mend = f.mend > 0;
  const tint = mend ? "#FFF4D0" : mix("#FFFFFF", A.glow, 0.35);

  const PASSES = [
    { style: tint,        w: 4.0, alpha: 0.055, blur: 12, light: true },
    { style: tint,        w: 1.7, alpha: 0.17, blur: 0 },
    { style: "#05040A",   w: 0.55, alpha: 0.62, blur: 0 },
    { style: mend ? "#FFF4D0" : "#FFFFFF", w: 0.62, alpha: 0.55, blur: 0, off: -0.9 },
  ];
  const QUANT = 0.5;
  const breathe = 0.88 + Math.sin(m.t * 2.1 + f.side * 2) * 0.12;
  const flare = 1 + (f.flash || 0) * 1.4;

  c.save();
  c.lineCap = "round"; c.lineJoin = "round";
  for (const P of PASSES){
    const bins = new Map();
    let any = 0;
    const add = (pts, n, wmul, off) => {
      n = Math.min(n, pts.length);
      for (let i = 1; i < n; i++){
        const lw = Math.max(0.3, P.w * wmul * (1 - (i / pts.length) * 0.45));
        const key = Math.max(1, Math.round(lw / QUANT));
        let p = bins.get(key);
        if (!p) bins.set(key, p = new Path2D());
        let x0 = pts[i - 1][0] * R, y0 = pts[i - 1][1] * R;
        let x1 = pts[i][0] * R,     y1 = pts[i][1] * R;
        if (off){
          const dx = x1 - x0, dy = y1 - y0, dl = Math.hypot(dx, dy) || 1;
          const ox = -dy / dl * off, oy = dx / dl * off;
          x0 += ox; y0 += oy; x1 += ox; y1 += oy;
        }
        p.moveTo(x0, y0); p.lineTo(x1, y1);
      }
    };
    for (const ck of sites){
      const g = siteGrow(ck, dmg);
      if (g <= 0) continue;
      any = Math.max(any, g);
      for (const ar of ck.arms) add(ar.pts, Math.max(2, Math.ceil(ar.pts.length * g)), ar.w, P.off);
      for (const rg of ck.rings){
        if (g <= rg.delay) continue;
        const rgg = Math.min(1, (g - rg.delay) / (1 - rg.delay));
        add(rg.pts, Math.max(2, Math.ceil(rg.pts.length * rgg)), rg.w, P.off);
      }
    }
    if (!bins.size) continue;
    c.strokeStyle = P.style;
    c.globalAlpha = P.alpha * (P.light ? breathe * flare : 1);
    /* One blurred stroke for the whole network, shadow-only and translated
       off-canvas so the geometry underneath is untouched. After a 13px
       gaussian a 5-wide line and a 2-wide line are the same smudge, so the
       buckets buy nothing here and cost a full blur each. */
    if (P.blur){
      const merged = new Path2D();
      let wsum = 0;
      for (const [k, path] of bins){ merged.addPath(path); wsum += k * QUANT; }
      const tf = c.getTransform(), OFF = 1e5;
      c.save();
      c.shadowColor = P.style; c.shadowBlur = P.blur;
      c.shadowOffsetX = OFF * tf.a;
      c.translate(-OFF, 0);
      c.lineWidth = wsum / bins.size;
      c.stroke(merged);
      c.restore();
    } else {
      for (const [k, path] of bins){ c.lineWidth = k * QUANT; c.stroke(path); }
    }
  }
  c.globalAlpha = 1;

  /* THE CRUSH ZONE. Where the thing actually hit, the glass is not cracked,
     it is powder — a few pulverised grains and a hot point. It is what turns
     a spray of lines into an impact, and it is the cheapest element here. */
  for (const ck of sites){
    const g = siteGrow(ck, dmg);
    if (g < 0.30) continue;
    const cx = ck.sx * R, cy = ck.sy * R;
    c.save();
    c.globalCompositeOperation = "lighter";
    const cg = c.createRadialGradient(cx, cy, 0, cx, cy, R * 0.10 * g);
    cg.addColorStop(0, hexA("#FFFFFF", 0.30 * g));
    cg.addColorStop(0.4, hexA(mend ? "#FFF4D0" : A.glow, 0.12 * g));
    cg.addColorStop(1, hexA(A.glow, 0));
    c.fillStyle = cg;
    c.beginPath(); c.arc(cx, cy, R * 0.10 * g, 0, Math.PI * 2); c.fill();
    c.restore();
    c.fillStyle = hexA("#FFFFFF", 0.42 * g);
    for (let s = 0; s < 4; s++){
      const h1 = shellHash(f.side * 77 + 3, s * 3 + 1), h2 = shellHash(f.side * 77 + 3, s * 3 + 2);
      const a = h1 * Math.PI * 2, d = (0.015 + h2 * 0.035) * R * g;
      const sz = (0.35 + h2 * 0.7) * g;
      c.beginPath();
      c.moveTo(cx + Math.cos(a) * d - sz, cy + Math.sin(a) * d);
      c.lineTo(cx + Math.cos(a) * d, cy + Math.sin(a) * d - sz * 0.9);
      c.lineTo(cx + Math.cos(a) * d + sz * 0.85, cy + Math.sin(a) * d + sz * 0.5);
      c.closePath(); c.fill();
    }
  }
  c.restore();
}

/* ------------------------------------------------------------- THE VENT ---
   A crack that reaches the outside of the glass is a hole, and a hole below
   the waterline leaks. Both halves of that sentence are enforced here: the
   vent is the first point on any arm that reaches the shell, and the leak
   test asks whether the fluid is currently above it — so a relic tipped by a
   wall bounce starts leaking from a vent that was dry a moment ago, and stops
   when the level falls past it. Nothing about that had to be authored. */
const VENT_CACHE = {};
function glassVents(side){
  if (VENT_CACHE[side]) return VENT_CACHE[side];
  const out = [];
  glassCracks(side).forEach((ck, i) => {
    /* THE IMPACT POINT IS ITSELF A HOLE, and leaving it out was a real
       omission rather than a conservative choice. A stone through a
       windscreen takes material out AT the impact -- the crush zone is
       pulverised glass, which is to say a gap -- and the radial arms are
       what happens after. Measured on the first exercise of this code: with
       arm-tip vents alone, only 2 to 3 of a relic's arms ever reach the
       shell at all, and the first drop of a 44-second fight fell at 29.4 s.
       Two thirds of the fight showed cracks and no spill, which breaks the
       one causal chain the whole feature exists to state.

       Gated on the site sitting near the rim, because a hole in the middle
       of the projected disc is a hole facing the viewer, and liquid leaving
       through it does not go anywhere this renderer can draw. Same test the
       silhouette chip uses, and for the same reason. */
    if (ck.sr > 0.58){
      const d = Math.hypot(ck.sx, ck.sy) || 1;
      out.push({ i, x: ck.sx / d * 0.97, y: ck.sy / d * 0.97,
                 a: Math.atan2(ck.sy, ck.sx), at: 0.30 });
    }
    for (const ar of ck.arms){
      for (let k = 1; k < ar.pts.length; k++){
        const [x, y] = ar.pts[k];
        const d = Math.hypot(x, y);
        if (d >= 0.94){
          const s = 0.97 / d;
          out.push({ i, x: x * s, y: y * s, a: Math.atan2(y, x),
                     /* how far into the site's growth the arm reaches out */
                     at: k / (ar.pts.length - 1) });
          break;
        }
      }
    }
  });
  return (VENT_CACHE[side] = out);
}
