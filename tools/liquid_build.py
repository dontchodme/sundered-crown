#!/usr/bin/env python3
"""THE RELIC IS A VESSEL -- glass spheres full of liquid, and the liquid is the
health.

    python3 liquid_build.py --src ../02-chain/sc-health18.html \
                            --out ../02-chain/sc-liquid.html            [--leak spill|none]

WHY. Rick, 2026-08-19: *"I want to rethink the health bars that are attached to
the balls ... animated as if they are glass spheres filled with liquid ... the
liquid inside the ball to represent its health. Meaning as it looses health the
liquid drains out."*

WHAT IT REPLACES, AND WHY EACH THING GOES.

  the 4-chunk arc gauge   The v5 note argued -- correctly -- that four
                          countable chunks beat a continuous arc, because a
                          COUNT needs no scale, no reference and no estimate.
                          That finding survives here; only the instrument
                          changes. The arc was still an ANGLE, which is the
                          third-ranked visual encoding. A liquid level read
                          against marks etched in the glass is POSITION ALONG
                          A COMMON SCALE, which is the first. Same count, a
                          strictly better channel, and the third mark from the
                          top is still exactly CONFIG.desperation.at.
  the ash husk            The shrinking lit heart said "hurt" by closing in
                          from the rim. The waterline says it by falling, and
                          two overlapping statements of the same number in the
                          same pixels is one too many.
  the ember + drain tail  Both were features OF the arc. The tail becomes a
                          tide mark on the glass, which is the same
                          information -- the bite that was just taken -- in
                          the language of the object.
  the stone fracture      Rick: *"currently the balls look like stone
                          cracking, id like that to change to glass
                          cracking"*. Stone and glass do not fail the same way
                          and they do not look the same when they do. See
                          glassCracks and drawGlassFracture in the core.
  the grain sprite        It existed to stop a smooth sphere reading as glass.
                          The sphere is now glass on purpose.

WHAT IT DOES NOT TOUCH. The lifeline panel above the hall is untouched by
choice: it answers "who is winning", which is a different question from "how
badly is this relic hurt", it was measured in v5, and it is the one instrument
in the frame that can compare two relics at a fixed seat.

THE DETERMINISM CONTRACT, WHICH IS THE WHOLE RISK OF THIS BUILD. A sloshing
liquid has STATE, and every health visual before it deliberately had none. The
contract is kept in three parts:

  1. The state lives in fields no simulation code reads. Write-only, ten
     numbers per relic, and `engine_ab.py` over the full 18-relic roster is
     the proof, not the claim.
  2. It is integrated in `tickPresentation`, on the SIMULATION tick -- the
     same 120 Hz in the live page and in the offline render -- so the two
     agree frame for frame. Not on the frame clock, which would not.
  3. Nothing in it draws from `this.rng()`. Every position, bubble, frost
     crystal and leak is a pure function of `(side, index, m.t)` through
     `shellHash`, exactly as the fractures and the statuses already are.

The one physical lie is stated in the core: a ball in free flight is in free
fall, so a truly physical liquid would be weightless between bounces and would
have no level at all. The liquid is given the hall's down permanently, and only
the NON-gravitational part of the ball's acceleration drives it. Everything you
can actually see -- wall bounce, floor slam, knockback, clank -- is that part.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, sys

HERE = pathlib.Path(__file__).parent
CORE = HERE.parent / "04-experiments" / "_liquid_core.js"
PROTECTED = {"sundered-crown.html", "sc-playable.html"}


def cut(src: str, start: str, end: str, what: str) -> str:
    for m, nm in ((start, "start"), (end, "end")):
        n = src.count(m)
        if n != 1:
            sys.exit(f"! {what}: {nm} anchor matches {n} times, expected 1")
    i, j = src.index(start), src.index(end)
    if j <= i:
        sys.exit(f"! {what}: end anchor precedes start anchor")
    return src[i:j]


def replace_span(src: str, start: str, end: str, new: str, what: str) -> str:
    old = cut(src, start, end, what)
    print(f"  {what:<12} replaced {len(old):>6} chars "
          f"({hashlib.sha256(old.encode()).hexdigest()[:12]}) -> {len(new):>6}")
    return src.replace(old, new, 1)


def insert_before(src: str, anchor: str, new: str, what: str) -> str:
    n = src.count(anchor)
    if n != 1:
        sys.exit(f"! {what}: anchor matches {n} times, expected 1")
    print(f"  {what:<12} inserted {len(new):>6} chars")
    return src.replace(anchor, new + anchor, 1)


def sub(src: str, old: str, new: str, what: str) -> str:
    n = src.count(old)
    if n != 1:
        sys.exit(f"! {what}: anchor matches {n} times, expected 1")
    print(f"  {what:<12} substituted")
    return src.replace(old, new, 1)


# ===================================================================== LEAK ==
LEAK_JS = r"""/* ----------------------------------------------------------------- LEAK ---
   A crack that reaches the outside of the glass is a hole, and a hole below
   the waterline leaks. Both halves of that are enforced rather than authored:
   the vent is the first point on a fracture arm that reaches the shell, and
   the emission test asks whether the fluid is currently above it -- so a
   relic tipped by a wall bounce starts leaking from a vent that was dry a
   moment earlier, and stops when the level falls past it.

   `on` is a switch because the two versions are a real choice and the choice
   should be made on pictures. Off, the level simply falls -- honest, cheap,
   and it reads as bookkeeping. On, damage is causal on screen: hit, crack,
   spill, level down. Flip it in the console and watch the same seed twice. */
const LEAK = { on: true, rate: 34, burst: 3.4, cap: 260 };

function tickDrips(m, dt){
  const A = CONFIG.arena, R = CONFIG.physics.ballR;
  if (!m.drips) m.drips = [];
  for (let i = m.drips.length - 1; i >= 0; i--){
    const d = m.drips[i];
    d.vy += 900 * dt;                        // the hall's own gravity
    d.x += d.vx * dt; d.y += d.vy * dt;
    if (d.y > A.h - 14 && !d.splat){         // it lands, and it stays landed
      d.y = A.h - 14; d.vx *= 0.2; d.vy = 0; d.splat = 1;
      d.life = Math.min(d.life, 0.75);
    }
    d.life -= dt;
    if (d.life <= 0) m.drips.splice(i, 1);
  }
  if (!LEAK.on) return;
  for (const f of [m.a, m.b]){
    if (!f.alive) continue;
    const frac = clamp(f.hp / CONFIG.combat.baseHP, 0, 1);
    const dmg = 1 - frac, lvl = lvlOf(frac);
    const vents = glassVents(f.side), sites = glassCracks(f.side);
    /* Which vents are open AND wet, right now. */
    const open = [];
    for (const v of vents){
      if (siteGrow(sites[v.i], dmg) < v.at + 0.05) continue;
      const depth = v.y - SLOSH.surf(f, v.x, lvl);
      if (depth <= 0.02) continue;           // above the waterline; dry
      open.push([v, depth]);
    }
    if (!open.length){ f.slDrip = 0; continue; }
    /* Rate scales with how many holes there are and how deep they sit -- head
       of pressure, which is the one thing about a leak everybody already
       knows. No rng: the phase accumulator picks the vent. */
    let head = 0;
    for (const [, d] of open) head += d;
    /* A HIT MUST SPURT, and the first cut did not. Emission was a flat rate
       against the head of pressure, so the spill was an even dribble that
       looked the same during a clean exchange as it did the instant a
       warhammer landed -- and "hit, crack, spill" is the ENTIRE argument for
       this feature. `slJolt` is already the contact impulse the slosh runs
       on, decaying at 2.2/s, so multiplying the rate by it costs nothing and
       ties the spurt to the blow that caused it rather than to the clock. */
    f.slDrip += dt * LEAK.rate * Math.min(2.2, head)
              * (1 + LEAK.burst * (f.slJolt || 0));
    let guard = 0;
    while (f.slDrip >= 1 && guard++ < 6){
      f.slDrip -= 1;
      if (m.drips.length >= LEAK.cap) break;
      const k = Math.floor(f.slDrip * 997 + m.t * 61) % open.length;
      const [v, depth] = open[(k + guard) % open.length];
      const h1 = shellHash(f.side * 53 + guard, Math.floor(m.t * 120) % 1024);
      const h2 = shellHash(f.side * 59 + guard, (Math.floor(m.t * 120) + 7) % 1024);
      const jet = 40 + depth * 190 + (f.slJolt || 0) * 130;   // pressure, plus the blow
      const sp = (h1 - 0.5) * 1.15;          // spread
      const ca = Math.cos(sp), sa = Math.sin(sp);
      const nx = v.x * ca - v.y * sa, ny = v.x * sa + v.y * ca;
      m.drips.push({
        x: f.x + v.x * R, y: f.y + v.y * R,
        vx: f.vx * 0.35 + nx * jet, vy: f.vy * 0.35 + ny * jet,
        /* smaller than the first cut by half. At 1.4-3.6 sim units these
           read as bubbles leaving the ball rather than as liquid; the
           spray wants many small drops, not few fat ones. */
        r: 0.7 + h2 * 1.5, c: f.aff.core, g: f.aff.glow,
        life: 1.1 + h2 * 0.9, splat: 0,
      });
    }
  }
}
"""

DRIP_DRAW = r"""  /* The spill. Drawn under the relics and over the hall, because it has left
     the vessel and it has not left the world: it falls under the hall's own
     900, it lands on the floor, and it stays there long enough to say that
     the relic is losing something real. */
  drawDrips(m){
    if (!m.drips || !m.drips.length) return;
    const c = this.ctx;
    c.save();
    for (const d of m.drips){
      const k = Math.max(0, Math.min(1, d.life / 1.1));
      c.globalAlpha = d.splat ? k * 0.5 : 0.55 + k * 0.4;
      c.fillStyle = d.c;
      if (d.splat){
        c.beginPath();
        c.ellipse(d.x, d.y, d.r * (2.2 - k), d.r * 0.42, 0, 0, TAU);
        c.fill();
      } else {
        /* stretched along its own travel: a falling drop is not a circle,
           and the streak is what makes it read as fast at 30 fps */
        const sp = Math.hypot(d.vx, d.vy) || 1;
        c.save();
        c.translate(d.x, d.y);
        c.rotate(Math.atan2(d.vy, d.vx));
        c.beginPath();
        c.ellipse(0, 0, d.r * (1 + Math.min(2.6, sp / 260)), d.r, 0, 0, TAU);
        c.fill();
        c.globalAlpha *= 0.5;
        c.fillStyle = d.g;
        c.beginPath(); c.ellipse(-d.r * 0.3, -d.r * 0.25, d.r * 0.45, d.r * 0.4, 0, 0, TAU);
        c.fill();
        c.restore();
      }
    }
    c.restore();
  }

"""

# ============================================================== THE SHATTER ==
SHATTER_JS = r"""  /* DEATH IS THE VESSEL FAILING, and it has two halves that a stone shell did
     not have: the glass goes, and what was inside it goes with it.

     The old version came apart into thirteen ANNULAR shards, which was right
     for a stone shell -- a curved plate off a curved surface. Glass does not
     do that. It breaks into flat slivers with straight edges, and it throws
     them, and every one of them catches light on one face. So the shards here
     are triangles struck from the centre with jittered radii, each spinning
     about its own centroid, each with one lit edge.

     And the liquid leaves. Whatever was still in the glass at the killing
     blow is thrown out as a burst of drops that fall under the hall's gravity
     -- so a relic that dies at 2 HP barely stains the floor and one killed
     from a third of its life empties itself across the hall. The size of the
     death is the size of the loss, stated by the same fluid that has been
     stating it for the whole fight. */
  drawShatter(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR;
    const age = m.deathAge, life = 2.1, hold = 0.08;
    if (age > life) return;
    const k = clamp(age / life, 0, 1);
    const fly = Math.max(0, age - hold);
    const frac = clamp((f.deathHp == null ? f.hp : f.deathHp) / CONFIG.combat.baseHP, 0, 1);
    const N = 15;
    c.save();
    c.lineJoin = "miter";

    /* the flash of the vessel giving way */
    if (age < 0.22){
      const e = 1 - age / 0.22;
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = e * 0.85;
      const fg = c.createRadialGradient(f.x, f.y, 0, f.x, f.y, R * (1 + (1 - e) * 2.4));
      fg.addColorStop(0, "#FFFFFF");
      fg.addColorStop(0.4, f.aff.glow);
      fg.addColorStop(1, hexA(f.aff.core, 0));
      c.fillStyle = fg;
      c.beginPath(); c.arc(f.x, f.y, R * (1 + (1 - e) * 2.4), 0, TAU); c.fill();
      c.restore();
    }

    /* THE LIQUID, LEAVING. Count scales on what was left, so the death of a
       relic finished at 2 HP looks nothing like the death of one taken from
       a third of its life -- and the difference is the fluid, which is the
       thing the viewer has been reading all fight. */
    const NL = Math.round(6 + frac * 34);
    for (let i = 0; i < NL; i++){
      const h1 = shellHash(f.side * 313 + 1, i * 3 + 1);
      const h2 = shellHash(f.side * 313 + 1, i * 3 + 2);
      const a = h1 * TAU;
      const sp = (90 + h2 * 300);
      const dx = Math.cos(a) * sp * fly;
      const dy = Math.sin(a) * sp * fly + 900 * 0.5 * fly * fly;
      const rr = (1.6 + h2 * 3.0) * (1 - k * 0.4);
      c.globalAlpha = Math.max(0, 1 - k * 1.15) * (0.55 + h1 * 0.45);
      c.fillStyle = h2 > 0.72 ? f.aff.glow : f.aff.core;
      c.beginPath(); c.arc(f.x + dx, f.y + dy, rr, 0, TAU); c.fill();
    }
    c.globalAlpha = 1;

    /* THE GLASS. Flat slivers, straight edges, one lit face each. */
    for (let i = 0; i < N; i++){
      const j0 = (shellHash(f.side * 23, i)     - 0.5) * 0.34;
      const j1 = (shellHash(f.side * 23, i + 1) - 0.5) * 0.34;
      const a0 = (i / N) * TAU + j0, a1 = ((i + 1) / N) * TAU + j1;
      const mid = (a0 + a1) / 2;
      const r0 = R * (0.55 + shellHash(f.side * 41, i) * 0.45);
      const r1 = R * (0.62 + shellHash(f.side * 43, i) * 0.38);
      const spd = 55 + shellHash(f.side * 13, i) * 150;
      const dist = spd * fly * (1 - k * 0.4);
      const spin = (shellHash(f.side * 17, i) - 0.5) * 9.0 * fly;
      c.save();
      c.globalAlpha = Math.max(0, 1 - k * k * 1.1);
      c.translate(f.x + Math.cos(mid) * dist,
                  f.y + Math.sin(mid) * dist + 130 * fly * fly);
      c.rotate(spin);
      const p = new Path2D();
      p.moveTo(0, 0);
      p.lineTo(Math.cos(a0) * r0, Math.sin(a0) * r0);
      p.lineTo(Math.cos(mid) * R * (0.9 + shellHash(f.side * 47, i) * 0.2),
               Math.sin(mid) * R * (0.9 + shellHash(f.side * 47, i) * 0.2));
      p.lineTo(Math.cos(a1) * r1, Math.sin(a1) * r1);
      p.closePath();
      const g = c.createLinearGradient(Math.cos(mid) * -R, Math.sin(mid) * -R,
                                       Math.cos(mid) * R, Math.sin(mid) * R);
      g.addColorStop(0, hexA(f.aff.dark, 0.85));
      g.addColorStop(0.5, hexA(mix(f.aff.dark, "#05040A", 0.5), 0.9));
      g.addColorStop(1, hexA("#0C0913", 0.9));
      c.fillStyle = g;
      c.fill(p);
      /* the lit edge -- one face of a sliver catches the hall and the rest
         does not, and that asymmetry is the entire difference between a
         shard of glass and a wedge of grey */
      c.strokeStyle = hexA("#FFFFFF", 0.55 * (1 - k));
      c.lineWidth = 1.1;
      c.beginPath();
      c.moveTo(0, 0);
      c.lineTo(Math.cos(a0) * r0, Math.sin(a0) * r0);
      c.stroke();
      c.strokeStyle = hexA(f.aff.glow, 0.4 * (1 - k));
      c.lineWidth = 0.9;
      c.stroke(p);
      c.restore();
    }
    c.restore();
  }

"""

# =============================================================== THE RELIC ==
FIGHTER_JS = r"""    /* THE RELIC IS A VESSEL, and the fluid in it is its life.

       Everything that used to live here -- the affinity-gradient shell, the
       ash husk closing in from the rim, the baked grain, the five-pass stone
       fracture, the spall, and the whole four-chunk arc gauge with its ember,
       its drain tail and its Curse cap -- is replaced by one call. Not
       because those were bad (v5's count survived three sheets and a roster
       audit) but because they were six statements of one number in six weak
       channels, and a liquid level against etched marks is one statement of
       it in the strongest channel there is.

       The count is NOT lost. It is the four graduations, the third of which
       is still exactly CONFIG.desperation.at, so the frame the fluid falls
       past it is still the frame the simulation changes gear. What changed is
       that the viewer now reads a POSITION rather than judging an ANGLE. */
    if (f.desperate){
      c.save();
      const pulse = 1 + Math.sin(m.t * 12) * 0.14;
      c.globalAlpha = 0.5;
      c.strokeStyle = "#E0433F"; c.lineWidth = 4;
      c.shadowColor = "#E0433F"; c.shadowBlur = 30;
      c.beginPath(); c.arc(f.x, f.y, R*1.5*pulse, 0, TAU); c.stroke();
      c.restore();
    }

    drawGlassRelic(c, m, f, R, { base: CONFIG.combat.baseHP });

"""

# ================================================================== STATUS ==
CURSE_JS = r"""  _stCurse(m, f, R, n){
    const c = this.ctx, N = Math.min(8, n) * 3;
    /* THE SHROUD IS GONE and the ring marker with it. Both were built for a
       stone shell with an arc gauge on it: the shroud was a dark band pulled
       against the inside of the shell, which is now the exact annulus the
       fluid meets the glass at, and the marker pointed at a ring that no
       longer exists.

       What Curse does -- eat maximum life, permanently -- is now stated by
       the vessel itself: `drawGlassRelic` frosts the top of the glass down to
       maxHp, and that is the part of the container the liquid can never reach
       again. It is a better statement than the old one for a reason worth
       keeping: the umbral arc at the far end of the health ring read as
       HEALTH to anyone who had not read the code, and a dead, frosted, empty
       band above the fill line cannot be read as health by anybody.

       What is left here is the mechanism: motes leaving and never coming
       back. They now leave FROM the dead band rather than from everywhere,
       so the thing being taken and the place it is taken from are the same
       place on screen. */
    const maxFrac = clamp(f.maxHp / CONFIG.combat.baseHP, 0, 1);
    const y0 = lvlOf(1) * R, y1 = lvlOf(maxFrac) * R;
    c.save();
    c.globalCompositeOperation = "lighter";
    for (let i = 0; i < N; i++){
      const ph = (m.t * 0.46 + shellHash(1103 + f.side, i)) % 1;
      const hx = shellHash(1117 + f.side, i);
      const px = f.x + (hx * 2 - 1) * R * 0.78;
      const py = f.y + (y0 + (y1 - y0) * shellHash(1129 + f.side, i))
                 - ph * ph * 46 - ph * 12;
      c.globalAlpha = (1 - ph) * (1 - ph * 0.4) * 0.95;
      c.fillStyle = ph < 0.35 ? "#E4CCFF" : "#A45CF0";
      c.beginPath(); c.arc(px, py, 3.4 * (1 - ph * 0.55), 0, TAU); c.fill();
      if (ph < 0.5){                       // a wisp, so it reads as leaving
        c.globalAlpha *= 0.55;
        c.strokeStyle = "#A45CF0"; c.lineWidth = 1.6;
        c.beginPath(); c.moveTo(px, py); c.lineTo(px, py + 9); c.stroke();
      }
    }
    c.restore();
  }
"""

SUNDER_JS = r"""  _stSunder(m, f, R, n){
    const c = this.ctx, N = Math.min(6, n);
    /* SUNDER ON GLASS. The old version lifted armour PLATES off a stone
       shell, dark gaps behind them -- exactly right for stone and impossible
       for glass, which has no plates and no layers to lift.

       What glass does under repeated impact is SPALL: a shallow, curved flake
       lets go of the outer wall and leaves a bright scalloped scar. That is
       the same mechanic in the right material -- the wall is thinner, so the
       next blow does more (+11% damage taken) -- and it is still legible with
       the colour removed, because the read is a lifting silhouette and a
       bright pit, not a hue.

       It is also deliberately NOT a fracture: a flake has a smooth conchoidal
       edge and no radial arms, so a viewer can tell a sundered relic from a
       cracked one at a glance, which is the whole reason a status gets its
       own picture. */
    c.save();
    for (let i = 0; i < N; i++){
      const a   = shellHash(907 + f.side, i) * TAU;
      const wid = 0.26 + shellHash(929 + f.side, i) * 0.20;
      const lift = 2.6 + Math.sin(m.t * 3.1 + i * 1.9) * 1.1;
      const ca = Math.cos(a), sa = Math.sin(a);

      /* the scar: a bright pit in the wall where the flake used to be */
      c.globalAlpha = 0.85;
      const sg = c.createRadialGradient(f.x + ca * R * 0.9, f.y + sa * R * 0.9, 0,
                                        f.x + ca * R * 0.9, f.y + sa * R * 0.9, R * wid * 1.6);
      sg.addColorStop(0, "#FFE7C6CC");
      sg.addColorStop(0.5, "#E0994A66");
      sg.addColorStop(1, "#E0994A00");
      c.fillStyle = sg;
      c.beginPath();
      c.arc(f.x, f.y, R * 1.0, a - wid / 2, a + wid / 2);
      c.arc(f.x, f.y, R * 0.72, a + wid / 2, a - wid / 2, true);
      c.closePath(); c.fill();

      /* the flake itself, on its way off: a lens, not a plate */
      c.save();
      c.translate(f.x + ca * (R * 0.95 + lift), f.y + sa * (R * 0.95 + lift));
      c.rotate(a + Math.PI / 2);
      c.globalAlpha = 0.92;
      const fw = R * wid * 1.15, fh = R * 0.13;
      const fg = c.createLinearGradient(0, -fh, 0, fh);
      fg.addColorStop(0, "#FFF2DE");
      fg.addColorStop(0.55, "#C98A4A");
      fg.addColorStop(1, "#3A2410");
      c.fillStyle = fg;
      c.beginPath();
      c.moveTo(-fw, 0);
      c.quadraticCurveTo(0, -fh * 2.0, fw, 0);
      c.quadraticCurveTo(0,  fh * 0.5, -fw, 0);
      c.closePath(); c.fill();
      c.strokeStyle = "#FFD9A0"; c.lineWidth = 0.9; c.stroke();
      c.restore();
    }
    c.restore();
  }
"""

SLOSH_FIELDS = r"""    /* THE LIQUID'S STATE. Ten numbers, plus the bookkeeping the integrator
       needs, and NOTHING in the simulation reads any of them -- move,
       tickClank, damage and checkEnd never touch a field on this block.
       engine_ab.py over all eighteen relics is what proves that rather than
       this comment.

       Declared here rather than lazily on first tick because it is 40% of the
       whole simulation's runtime. Adding them on the fly changed every
       Fighter's hidden class AFTER move() and tickClank() had specialised on
       the original shape; a 612-match sweep went 17.7s to 24.8s and stubbing
       the integrator recovered all of it. A headless sweep draws nothing and
       should not pay for a picture. */
    this.slTilt  = 0; this.slTiltV  = 0;   // surface pivot, radians
    this.slHeave = 0; this.slHeaveV = 0;   // level offset, radius units
    this.slA2    = 0; this.slA2V    = 0;   // symmetric ripple
    this.slA3    = 0; this.slA3V    = 0;   // second ripple
    this.slVx = this.vx; this.slVy = this.vy;   // last tick's velocity
    this.slPx = 0; this.slPy = 0;               // last tick's position
    this.slJolt = 0;      // 0..1, decaying: drives the film and the spray
    this.slDrip = 0;      // leak phase accumulator; no rng anywhere near it
    this.slM = null;      // this school's spring constants, resolved once
"""

# ============================================================ THE SIM HOOK ==
SLOSH_LIVE = r"""    /* A HEADLESS SWEEP DOES NOT INTEGRATE A PICTURE.

       `simulate()` builds a Match, steps it to the end and reads `summary()`.
       It never draws, and verify.py and tune.py call it thousands of times.
       Measured on a 612-match sweep: with the liquid integrating, 17.5s ->
       24.9s, and stubbing the integrator recovered every bit of it. 215 ns a
       call in isolation does not explain 6.4 s across the sweep -- the cost
       is the extra work on the hot tick, not the arithmetic in it -- but the
       fix is the same either way and it is not a micro-optimisation: a
       balance run should never pay for a visual feature.

       Default TRUE, so anything that constructs a Match and draws it gets the
       liquid without asking: the live page, render.py, every shot tool. Only
       `simulate()` turns it off, at the one line that is by definition
       headless. Nothing observable changes -- no simulation code reads a
       slosh field, which engine_ab.py proves over all eighteen relics. */
    this.slLive = true;
"""

SLOSH_HOOK = r"""      if (f.hp >= f.hpGhost) f.hpGhost = f.hp;
      else f.hpGhost += (f.hp - f.hpGhost) * (1 - Math.exp(-5.5 * dt));
      /* THE LIQUID. Integrated here, on the SIMULATION tick, for the same
         reason the ultimate clock and the status tags are here: this runs on
         the frozen path as well as the normal one, so the fluid keeps moving
         through a hit stop -- which is exactly when a viewer is staring at
         the ball and exactly when a frozen surface would read as a stall.

         It is passed the gravity THIS relic actually feels, not the config
         constant: `move` scales gravity by (mass/massRef)^massWeight, so
         Grudgebearer at 5.0 falls harder than Spellbreaker at 1.0. Subtract
         the wrong number and free flight stops cancelling, and every relic in
         the roster develops a permanent list to one side.

         Write-only. Nothing in the simulation reads a single field it sets,
         and it draws no rng. engine_ab.py over all eighteen ids is the proof. */
      if (this.slLive){
        const _P = CONFIG.physics;
        SLOSH.step(f, dt, _P.gravity * Math.pow(
          (f.w.mass + f.burden * f.burdenMass) / _P.massRef, _P.massWeight));
      }
    }
    if (this.slLive) tickDrips(this, dt);"""


# ==================================================================== MAIN ==
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-health18.html")
    ap.add_argument("--out", default="../02-chain/sc-liquid.html")
    ap.add_argument("--leak", choices=("spill", "none"), default="spill",
                    help="spill: droplets leave the crack and fall in the hall. "
                         "none: the level simply falls.")
    ap.add_argument("--fracture", choices=("on", "off"), default="off",
                    help="glass cracking. CUT FOR GOOD 2026-08-19 -- built properly, "
                         "fixed twice, rendered as a frame-for-frame A/B on one seed, "
                         "and turned down. Read 06-docs/LIQUID-NOTES.md 4b BEFORE "
                         "turning this on to see what it looks like; it is already "
                         "recorded there. off also forces --leak none: a spill needs "
                         "a hole and the holes were the crack arms.")
    ap.add_argument("--marks", choices=("none", "desperation", "ticks"), default="none",
                    help="graduations etched in the glass. Rick dropped these on "
                         "sight of the first sheet; kept as a switch.")
    a = ap.parse_args()

    src_p, out_p = pathlib.Path(a.src), pathlib.Path(a.out)
    if out_p.name in PROTECTED:
        sys.exit(f"! refusing to write {out_p.name}: that file is verified")
    if not src_p.exists():
        sys.exit(f"! missing {src_p}")
    if not CORE.exists():
        sys.exit(f"! missing {CORE} -- the core is shared with liquid_lab.py "
                 f"so the lab and the game cannot drift")
    s = src_p.read_text(encoding="utf-8")
    print(f"=== LIQUID  {src_p.name} "
          f"({hashlib.sha256(s.encode()).hexdigest()[:16]})  "
          f"leak={a.leak} marks={a.marks} ===")

    # ---- PREFLIGHT. Refuse rather than produce a plausible wrong build. ----
    for need in ("const AFFINITIES = {", "function shellHash(a, b){",
                 "  tickPresentation(dt){", "  drawFighter(m, f){"):
        if s.count(need) != 1:
            sys.exit(f"! preflight: expected exactly one {need!r}, found {s.count(need)}")
    if "drawGlassRelic" in s:
        sys.exit("! preflight: source already contains drawGlassRelic — "
                 "this builder is not idempotent and must not be run twice")

    if a.fracture == "off" and a.leak == "spill":
        print("  note: --fracture off forces --leak none. The vents ARE the crack\n"
              "        arms that reach the shell, so with no fracture there is no hole,\n"
              "        and liquid leaving an intact sphere reads as a defect.")
        a.leak = "none"

    core = CORE.read_text(encoding="utf-8")
    core = core.replace("const FRACTURE = { on: false };",
                        f'const FRACTURE = {{ on: {"true" if a.fracture == "on" else "false"} }};')
    core = core.replace('const MARKS = { mode: "none" };',
                        f'const MARKS = {{ mode: "{a.marks}" }};')
    leak_js = LEAK_JS.replace("const LEAK = { on: true,",
                              f"const LEAK = {{ on: {'true' if a.leak == 'spill' else 'false'},")

    # 1. retire the stone model FIRST. Order matters and getting it wrong is
    #    caught rather than shipped: the removal span ends at the RENDERER
    #    banner, so inserting the core before that banner first would make the
    #    removal swallow the core whole. The postflight caught exactly that.
    s = replace_span(s, "const SHELL_CACHE = {};\nfunction shellCracks(side){",
                     "/* ---------------------------------------------------------------- RENDERER */",
                     "/* The stone fracture pattern (shellCracks / SHELL_CACHE) was removed\n"
                     "   here: it is replaced by glassCracks, and a retired model left in\n"
                     "   place is a trap for whoever reads this next. It is recoverable from\n"
                     "   sc-health18.html, which is the tip this was built from. */\n\n",
                     "rm shellCracks")

    # 2. the core, in front of the renderer: it needs AFFINITIES and shellHash,
    #    both of which are defined well above this point.
    s = insert_before(s, "/* ---------------------------------------------------------------- RENDERER */",
                      core + "\n" + leak_js + "\n", "core+leak")

    s = replace_span(s, "  /* ----------------------------------------------------------- fighter --- */",
                     "  /* The loser used to simply vanish on the killing blow",
                     "  /* ----------------------------------------------------------- fighter --- */\n"
                     "  /* corePath was removed with the stone fracture: the chipped silhouette\n"
                     "     is now glassPath, which cuts straight-edged chords rather than\n"
                     "     rounded scallops, because glass does not chip in scallops. */\n\n",
                     "rm corePath")

    # 3. the slosh, on the simulation tick
    s = replace_span(s,
        "      if (f.hp >= f.hpGhost) f.hpGhost = f.hp;",
        "  }\n\n  decayImpactOnly(dt){",
        SLOSH_HOOK + "\n  }\n\n  decayImpactOnly(dt){", "slosh hook")

    # 3b. THE FIELDS ARE DECLARED IN THE CONSTRUCTOR, and that is a
    #     measurement, not a style preference. Adding the fourteen slosh
    #     fields lazily on first tick made every Fighter change hidden class
    #     after the simulation's hot paths had already specialised on the
    #     original shape. Measured on a 612-match sweep: 17.7s -> 24.8s, a 40%
    #     tax on a build that draws nothing. Declared up front, every Fighter
    #     is born with its final shape and move()/tickClank() stay monomorphic.
    s = sub(s, "    this.trail = [];",
            SLOSH_FIELDS + "    this.trail = [];", "slosh fields")

    s = sub(s, "    this.deathAge = 0;        // presentation only: drives the shatter",
            SLOSH_LIVE + "    this.deathAge = 0;        // presentation only: drives the shatter",
            "slLive")
    s = sub(s, "function simulate(idA, idB, seed){\n  const m = new Match(idA, idB, seed);",
            "function simulate(idA, idB, seed){\n  const m = new Match(idA, idB, seed);\n"
            "  m.slLive = false;          // headless: see the note on Match.slLive",
            "simulate headless")

    # 4. what the glass was at the moment it failed -- write-only, set once
    s = sub(s, "      this.loser.hp = Math.max(0, this.loser.hp);",
            "      this.loser.hp = Math.max(0, this.loser.hp);\n"
            "      /* What was still in the glass when it failed. hp is clamped to zero\n"
            "         on this very line, so it cannot be read back afterwards, and the\n"
            "         ghost is the only record of what the killing blow took. Drives the\n"
            "         size of the spill in drawShatter, and nothing else. Presentation. */\n"
            "      this.loser.deathHp = Math.max(0, this.loser.hpGhost == null\n"
            "                                        ? this.loser.hp : this.loser.hpGhost);",
            "deathHp")

    # 5. the relic itself
    s = replace_span(s, "    const base   = CONFIG.combat.baseHP;",
                     "    if (f.stun > 0){                                   // staggered",
                     FIGHTER_JS, "the relic")

    # 6. death
    s = replace_span(s, "  drawShatter(m, f){", "  /* THE BALL, ON ITS OWN SURFACE.",
                     SHATTER_JS, "the shatter")

    # 7. the two statuses that stone made sense of and glass does not
    s = replace_span(s, "  _stCurse(m, f, R, n){",
                     "  /* HEX — the weapon is jammed", CURSE_JS + "\n", "curse")
    s = replace_span(s, "  _stSunder(m, f, R, n){",
                     "  /* ENTANGLE — it is being held back.", SUNDER_JS + "\n", "sunder")

    # 8. the spill, drawn under the relics and over the hall
    s = insert_before(s, "  drawFighter(m, f){", DRIP_DRAW, "drawDrips")
    s = sub(s, "    this.drawFighter(m, m.b);\n    this.drawFighter(m, m.a);",
            "    this.drawDrips(m);\n    this.drawFighter(m, m.b);\n    this.drawFighter(m, m.a);",
            "drip call")

    # ---- POSTFLIGHT ----
    for gone in ("shellCracks(", "this.corePath(", "grainSprite(f.side"):
        if gone in s:
            sys.exit(f"! postflight: {gone!r} still referenced after the swap")
    for need in ("drawGlassRelic(c, m, f, R,", "SLOSH.step(f, dt,", "tickDrips(this, dt)",
                 "function glassCracks(side){", "function glassPath(f, R, dmg, cx, cy){"):
        if s.count(need) < 1:
            sys.exit(f"! postflight: {need!r} missing from the build")

    out_p.write_text(s, encoding="utf-8")
    print(f"\n  -> {out_p}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  ({len(s):,} chars, {len(s) - len(src_p.read_text(encoding="utf-8")):+,})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
