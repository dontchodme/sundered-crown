#!/usr/bin/env python3
"""SLAGHEART — the dwarven flail — and IRONBLOOM, its ultimate.

The seventeenth relic, and the second `mode:"chain"` in the game.  Rick chose
the cell off the shape x school grid: greatsword is the only complete row, and
chain had exactly one relic, so a second flail is the pick that says whether
the chain model generalises at all.

    python3 slagheart_build.py --src sc-introfit.html --out sc-slagheart.html
    python3 slagheart_build.py --src sc-introfit.html --out sc-slagheart-mr.html \
                               --massref 2.681

THE RELIC.  Flail archetype — reach 96, spin 2.2, mass 3.6, the hardest single
hit in the game — carrying dwarven Sunder at **+2 a hit** rather than the usual
+1.  It lands few, enormous blows, so three connects cap the stack and it
becomes its own damage amplifier.  That is the characterisation: Grudgebearer
SPENDS Sunder, Slagheart BUILDS it, and they are the same school.

IRONBLOOM, Rick's design, in his words:

  "the flail head burns with the forges heat and if it connects within a time
   window it latches to the target causing massive hitstop and exploding
   sending its opponent flying. the explosion sends out shards of shrapnel
   that bounce around the arena and cause further damage and apply sunder if
   they connect. if they dont hit anything after a duration they explode"

`kind:"latch"`, and the four beats are:

  LIT     the head goes orange.  No banner, no damage, no assist of any kind.
          A window opens (`window` seconds) and the charge does not rebuild
          while it burns — the cooldown is owed from the RESOLUTION.
  HELD    the first melee connect inside the window does not deal damage: the
          head BITES.  The chain snaps taut between the two balls and the hall
          stops for `hold` seconds — a real freeze, the longest in the game,
          longer than a six-stack Crucible.  The shake RAMPS across it rather
          than decaying, so the beat reads as pressure building and not as a
          stall.  Rick, mid-build: "lets add some screenshake and a special
          animation to the latch hit stop too."
  BLAST   the head detonates.  The foe takes the blast, is launched over the
          speed ceiling, and `shards` splinters of hot iron are thrown into
          the hall.  The name lands HERE — you do not caption a promise.
  SHARDS  each splinter bounces off the walls up to `shardBounce` times,
          deals `shardDmg` and +`shardSunder` on a connect, and POPS at the
          end of its life if it never found anything.

WHY IT IS NOT THE CRUCIBLE, which is the real risk in a second dwarven
light-it-and-connect ultimate:

  * The Crucible PULLS.  Ironbloom has no pull, no capture term, no assist —
    if you cannot land the head, nothing happens.
  * The Crucible CONSUMES Sunder for one enormous strike.  Ironbloom's strike
    is modest and it SPRAYS Sunder: the payoff is the twenty seconds after
    the blast, not the blast.
  * The Crucible suppresses hits below a legibility floor so the wind-up is
    always seen.  Ironbloom has no floor — the flail's own 0.45 hit cooldown
    and 2.2 spin mean the earliest possible bite is several tenths away, so
    the floor would only ever waste the window.

THE SHRAPNEL IS FOE-ONLY, per Rick, following the rule every projectile in
this game already lives under (`shot.own`).  Hot iron that did not care whose
it was would be a better sentence and a worse mechanic: it breaks the one
convention that lets a viewer know who a flying object belongs to.

massRef: `--massref` re-derives the fall-rate reference for the grown roster.
It is a SEPARATE flag on purpose.  Built without it, the 16 existing relics
must be bit-identical (engine_ab proves the relic is inert); built with it,
they must not be, and the difference is the constant and nothing else.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent

# --------------------------------------------------------------------------
RELIC = r'''
  /* SLAGHEART — the second chain relic, and the dwarven answer to it.
     Gravemourn's flail is a grave-thing that lags and overshoots; this one is
     a foundry offcut on a length of pit chain. Same archetype numbers, same
     motion model, opposite school and opposite relationship to Sunder:
     Grudgebearer's Crucible spends it, Slagheart builds it two at a time.
     dmg is the tuned knob (slagheart_build.TUNED_SH). */
  { id:"slagheart", name:"Slagheart", aff:"dwarven", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:__DMG__, spin:2.2, mode:"chain", mass:3.6,
    onHit:{ sunder:2 },
    ult:{ name:"Ironbloom", charge:17, kind:"latch",
          window:__WINDOW__,
          hold:0.8, dmg:__BLAST__, launch:1800, launchFatal:2050,
          shards:9, shardDmg:__SHARD__, shardSpd:660, shardLife:2.6,
          shardBounce:3, shardSunder:1, shardR:11,
          pop:7, popR:104,
          tip:"The head latches on, then bursts — shrapnel bounces the hall, sundering" },
    blurb:"A foundry offcut on pit chain. Bites, holds, and fills the hall with hot iron." },
'''

# --------------------------------------------------------------------------
LATCH_STEP = r'''    /* THE LATCH. The head has bitten and the hall is holding its breath.
       The hold IS the freeze — this branch takes over step() entirely, so
       nothing in the simulation advances — but the match clock still runs
       (duration stays honest, exactly as hit stop does) and the presentation
       clock runs with it, so the set-piece plays through a frozen world.

       The shake is RE-ARMED here rather than decaying. decayImpactOnly takes
       90/s off it, which would leave the last third of the hold dead quiet;
       instead it ramps on t^2.2 from a tremor to a hall-rattle, so the beat
       reads as pressure building toward the blast. Rick asked for this and
       for the set-piece that rides it (drawUltOver, phase "held"). */
    if (this.latch){
      const L = this.latch;
      L.t += dt;
      this.t += dt;
      this.hitStop = Math.max(this.hitStop, 0.03);   // the renderer's punch
      this.decayImpactOnly(dt);
      const k = clamp(L.t / L.dur, 0, 1);
      /* The floor is the bite's own 18 rather than 0: decayImpactOnly takes
         90/s off the shake, so a ramp starting at 7 spent its first eighth of
         a second visibly DYING before it began to climb. Measured (the probe
         counts decaying frames and there were twelve of them). */
      this.shake = Math.max(this.shake, 18 + 40 * Math.pow(k, 2.2));
      if (L.t >= L.dur) this.blast(L);
      return;
    }
'''

# --------------------------------------------------------------------------
FIRE_LATCH = r'''    /* IRONBLOOM DOES NOT RESOLVE HERE. The head lights and a window opens.
       Everything below is skipped for the reason the aimed shot and the
       Crucible skip it: an ultimate that had already paid out before the
       head bit would make the bite decorative. No banner — the name goes on
       the blast. No pull, no assist, no legibility floor: this one you land
       yourself or you do not. */
    if (u.kind === "latch"){
      f.ultHeat = { t: 0, window: u.window || 4.5 };
      this.ultFx = { w: f.w.id, kind: "latch", phase: "lit",
                     src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                     x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: true,
                     radius: 300, aff: f.aff, t: 0,
                     /* NORMAL path: 2x. See FX_CLOCK in the builder. */
                     life: ((u.window || 4.5) + 0.4) * 2 };
      this.banner = null;
      return;
    }

'''

# --------------------------------------------------------------------------
HEAT_TICK = r'''    if (f.ultHeat){
      /* The head is lit and the window is burning. The charge does not
         rebuild while it burns — the seventeen seconds are owed from the
         RESOLUTION, bite or fizzle, or a whiff would quietly cost less than
         it says. Nothing else happens here: no pull, no spin-up, no stun
         immunity. The Crucible earns those because it promises contact;
         Ironbloom promises nothing and has to be aimed. */
      const H = f.ultHeat, u = f.w.ult;
      H.t += dt;
      if (H.t >= H.window){
        f.ultHeat = null;
        this.ultFx = { w: f.w.id, kind: "latch", phase: "fizzle",
                       src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                       x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: false,
                       radius: 300, aff: f.aff, t: 0, life: 1.8 };
        SFX.play("ult", { w: "slagheart-fizzle" });
        this.note(`${f.w.name} — the head cools`);
      }
      return;
    }
'''

# --------------------------------------------------------------------------
LATCH_HIT = r'''    /* IRONBLOOM'S BITE. A melee connect while the head is lit is not a hit —
       it is the latch, and it deals no damage of its own. `mul === undefined`
       keeps a shard or any other projectile from ever triggering it: the head
       has to arrive on the chain, which is the whole point of the mechanic.
       Returning here means none of the ordinary hit — damage, onHit sunder,
       knockback, hitstun, the CINEMA beat — happens on this frame. The blast
       pays all of it, 0.8 seconds later. */
    if (mul === undefined && self.ultHeat && self.w.ult.kind === "latch"
        && foe.alive){
      const R = CONFIG.physics.ballR, u = self.w.ult;
      self.ultHeat = null;
      /* the head is planted on the foe's shell and the chain drawn straight;
         nothing ticks it for the duration of the hold, so this is where the
         picture is set */
      const dx = foe.x - self.pivX, dy = foe.y - self.pivY;
      const dl = Math.hypot(dx, dy) || 1;
      self.headAng = Math.atan2(dy, dx);
      self.headR = Math.max(12, dl - R * 0.72);
      self.headX = self.pivX + Math.cos(self.headAng) * self.headR;
      self.headY = self.pivY + Math.sin(self.headAng) * self.headR;
      self.headAngVel = 0;
      this.latch = { src: self === this.a ? "a" : "b",
                     tgt: self === this.a ? "b" : "a",
                     t: 0, dur: u.hold || 0.8, hx, hy };
      this.ultFx = { w: self.w.id, kind: "latch", phase: "held",
                     src: this.latch.src, tgt: this.latch.tgt,
                     x: hx, y: hy, tx: foe.x, ty: foe.y, hit: true,
                     radius: 300, aff: self.aff, t: 0,
                     /* FROZEN path: 1x, the one exception. */
                     life: (u.hold || 0.8) + 0.05 };
      this.hitStop = Math.max(this.hitStop, 0.03);
      this.shake = Math.max(this.shake, 18);
      this.ring(hx, hy, "#FFB347", 5, 120, 0.5, 7);
      this.beat({ kind: "ult", side: self === this.a ? 0 : 1, x: hx, y: hy,
                  w: self.w.id, foeHpFrac: foe.hp / foe.maxHp });
      SFX.play("ult", { w: "slagheart-latch" });
      this.note(`${self.w.name} — the head bites`);
      return;
    }
'''

# --------------------------------------------------------------------------
BLAST = r'''  /* IRONBLOOM DETONATES. Called only from the latch branch of step(), on the
     frame the hold runs out, with the world still frozen around it.

     The blast itself is deliberately modest — `u.dmg`, priced through hurt()
     so a ward eats it like anything else. The ultimate's real weight is the
     nine splinters it leaves in the hall, which is what makes it Slagheart's
     and not the Crucible's: one is a single enormous strike, this is twenty
     seconds of Sunder arriving from directions nobody chose. */
  blast(L){
    const src = this[L.src], foe = this[L.tgt], u = src.w.ult;
    this.latch = null;
    const R = CONFIG.physics.ballR;
    const bx = foe.x, by = foe.y;

    if (foe.alive){
      const dmg = Math.round(u.dmg * this.actMods.dmg * foe.dmgTakenMul());
      this.hurt(foe, dmg, src);
      foe.flash = 1; foe.ringFlash = 1;
      src.dealt += dmg; src.hits++;
      this.float(foe.x, foe.y - 40, dmg, "#FFF4D0", 46);
      const fatal = foe.hp <= 0;
      if (fatal) this.finisher = 1.0;
      /* Sent flying, over the speed ceiling on purpose — `launch` raises the
         vmax clamp and the relax term spends the next second and a half
         paying it back, which from inside the physics is what several fast
         bounces off the arena looks like. The direction is away from the
         head, because that is where the charge was. */
      const kx = foe.x - src.x, ky = foe.y - src.y, kl = Math.hypot(kx, ky) || 1;
      const p = fatal ? u.launchFatal : u.launch;
      foe.vx += (kx / kl) * p; foe.vy += (ky / kl) * p;
      foe.launch = Math.max(foe.launch || 0, 1.8);
      if (!fatal) foe.takeHitstun(dmg);
    }

    /* the splinters. Deterministic angles off shellHash — no rng draw, so a
       relic that is not in the match cannot be perturbed by one that is. */
    const N = u.shards || 9;
    for (let i = 0; i < N; i++){
      const a = (i / N) * TAU + (shellHash(6151, i) - 0.5) * 0.55;
      const spd = u.shardSpd * (0.78 + shellHash(6173, i) * 0.5);
      if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();
      this.shots.push({
        /* Clear of the shell AND armed. The first build spawned these at
           R+6 — inside `R + s.r`, the hit radius — so all nine resolved on
           the foe on the frame they were born: ~50 damage and six Sunder in
           one instant, which is a burst and the exact opposite of the design.
           `arm` is the honest fix: a splinter has to leave the blast before
           it can bite, and what catches the foe afterwards is a RICOCHET. */
        own: L.src, x: bx + Math.cos(a) * (R + (u.shardR || 11) + 10),
        y: by + Math.sin(a) * (R + (u.shardR || 11) + 10),
        arm: u.shardArm || 0.12,
        x0: bx, y0: by, spd0: 0, t0: this.t,                    // CINEMA (demo)
        vx: Math.cos(a) * spd, vy: Math.sin(a) * spd,
        r: u.shardR || 11, life: u.shardLife || 2.6, max: u.shardLife || 2.6,
        grav: 0, dmgMul: (u.shardDmg || 5.5) / Math.max(0.01, src.w.dmg),
        bounce: u.shardBounce || 3,
        shard: true, pop: u.pop || 7, popR: u.popR || 104,
        over: { onHit: { sunder: u.shardSunder || 1 } },
        aff: src.aff, a,
      });
    }

    this.shake = 54;
    this.hitStop = Math.max(this.hitStop, 0.16);
    this.spawnFx(bx, by, "#FFB347", 44, 520, 0.8, 6);
    this.spawnFx(bx, by, "#FFF4D0", 26, 700, 0.55, 4);
    this.ring(bx, by, "#FFF4D0", 8, 210, 0.5, 9);
    this.ring(bx, by, "#FF6A1A", 5, 150, 0.42, 6);
    this.banner = { text: u.name, life: 2.1, max: 2.1, color: src.aff.core,
                    glow: src.aff.glow, w: src.w.id, bx, by };
    this.ultFx = { w: src.w.id, kind: "latch", phase: "blast",
                   src: L.src, tgt: L.tgt, x: bx, y: by, tx: bx, ty: by,
                   hit: true, radius: 300, aff: src.aff, t: 0, life: 3.0 };
    this.beat({ kind: "ult", side: L.src === "a" ? 0 : 1, x: bx, y: by,
                w: src.w.id, foeHpFrac: Math.max(0, foe.hp) / foe.maxHp });
    SFX.play("ult", { w: "slagheart-blast" });
    this.note(`${src.w.name} — Ironbloom`);
  }

'''

# --------------------------------------------------------------------------
SHARD_SPENT = r'''      /* --- the wall. An arrow is spent on it: "a ricocheting arrow is chaos
         the viewer cannot attribute to anything." A SPLINTER bounces, and the
         exception is argued rather than assumed — it is tethered to an event
         the viewer just watched (a blast they saw throw it), it is large and
         slow enough to follow, and its bounces are the mechanic rather than
         a side effect. It gets `bounce` of them and no more. */
      if (!dead && s.bounce > 0){
        let hitWall = false;
        if (s.x < n + s.r){ s.x = n + s.r; s.vx = Math.abs(s.vx); hitWall = true; }
        else if (s.x > A.w - n - s.r){ s.x = A.w - n - s.r; s.vx = -Math.abs(s.vx); hitWall = true; }
        if (s.y < n + s.r){ s.y = n + s.r; s.vy = Math.abs(s.vy); hitWall = true; }
        else if (s.y > A.h - n - s.r){ s.y = A.h - n - s.r; s.vy = -Math.abs(s.vy); hitWall = true; }
        if (hitWall){
          s.bounce--;
          s.vx *= 0.88; s.vy *= 0.88;
          s.a = Math.atan2(s.vy, s.vx);
          s.snap = true;          // the interpolator must not tween through a wall
          this.spawnFx(s.x, s.y, s.aff.glow, 5, 130, 0.24, 2.4);
          SFX.play("wall");
        }
      }

      /* --- the splinter pops. Rick: "if they dont hit anything after a
         duration they explode." A shard that ran out its life detonates where
         it is: a small blast that still sunders anything inside popR, so the
         hall stays dangerous right up to the last splinter. */
      if (!dead && s.shard && s.life <= 0){
        this.spawnFx(s.x, s.y, "#FFB347", 14, 300, 0.5, 4);
        this.ring(s.x, s.y, "#FF8C3A", 4, s.popR * 0.9, 0.32, 5);
        if (foe.alive && Math.hypot(s.x - foe.x, s.y - foe.y) < s.popR + R){
          const seg = { ax: s.x - 8, ay: s.y, bx: s.x + 8, by: s.y, a: 0 };
          this.resolveHit(src, foe, s.x, s.y, seg,
                          s.pop / Math.max(0.01, src.w.dmg), s.over);
        }
        this.shake = Math.min(38, this.shake + 5);
        dead = true;
      }

'''

# --------------------------------------------------------------------------
# THE SET-PIECE.  Four phases, and the one that matters is `held`: Rick asked
# for "some screenshake and a special animation to the latch hit stop too",
# and the hold is 0.8s of FROZEN WORLD — the longest freeze in the game — so
# everything the viewer sees during it has to come from the presentation
# clock.  Nothing here reads a single simulation value that changes: the two
# balls, the pivot and the bite point are all static for the duration, and
# every moving thing below is a pure function of u.t.
UNDER = r"""    if (u.w === "slagheart"){
      const heat = (x, y, r, a, c0) => {
        const g = c.createRadialGradient(x, y, 3, x, y, r);
        g.addColorStop(0, c0); g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = a; c.fillStyle = g;
        c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
      };
      if (u.phase === "lit"){
        /* the forge under the caster, breathing, and a smear of heat under
           wherever the head happens to be swinging */
        const rise = clamp(u.t / 0.3, 0, 1);
        const fade = 1 - clamp((u.t - (u.life - 0.4)) / 0.4, 0, 1);
        const pulse = 0.86 + 0.14 * Math.sin(u.t * 6.5);
        heat(src.x, src.y, 92 * pulse, 0.55 * rise * fade, "#FF6A1A4A");
        heat(src.headX, src.headY, 66 * pulse, 0.6 * rise * fade, "#FFB34755");
      }
      else if (u.phase === "held"){
        /* the floor cooks under the pair, and the heat runs along the chain */
        const k = clamp(u.t / u.life, 0, 1), e = k * k;
        heat(tgt.x, tgt.y, 90 + 150 * e, 0.5 + 0.45 * e, "#FF8C3A66");
        c.globalAlpha = 0.35 + 0.4 * e;
        c.strokeStyle = "#FF6A1A"; c.lineWidth = 10 + 26 * e;
        c.beginPath(); c.moveTo(src.pivX, src.pivY); c.lineTo(tgt.x, tgt.y); c.stroke();
        /* fissures opening in the floor under the target as it builds */
        for (let i = 0; i < 7; i++){
          const a2 = (i / 7) * TAU + shellHash(3301, i) * 0.6;
          const len = (60 + 150 * e) * (0.55 + shellHash(3307, i) * 0.7);
          c.globalAlpha = 0.75 * e;
          c.strokeStyle = "#FF6A1A"; c.lineWidth = 2 + 3 * e;
          c.shadowColor = "#FF8C3A"; c.shadowBlur = 10;
          this._jag(c, tgt.x, tgt.y, tgt.x + Math.cos(a2) * len,
                    tgt.y + Math.sin(a2) * len, 6, 11, 3311 + i, 1);
          c.shadowBlur = 0;
        }
      }
      else if (u.phase === "blast"){
        /* the floor takes it: molten cracks out of the detonation */
        const grow = clamp(u.t / 0.20, 0, 1);
        const fade = 1 - clamp((u.t - 0.55) / 0.85, 0, 1);
        for (let i = 0; i < 10; i++){
          const a2 = (i / 10) * TAU + shellHash(4801, i) * 0.5;
          const len = 230 * (0.55 + shellHash(4813, i) * 0.7) * grow;
          const ex = u.x + Math.cos(a2) * len, ey = u.y + Math.sin(a2) * len;
          c.globalAlpha = 0.85 * fade;
          c.strokeStyle = "#2E1B0A"; c.lineWidth = 8 * (1 - u.t * 0.4);
          this._jag(c, u.x, u.y, ex, ey, 7, 13, 4817 + i, 1);
          c.globalAlpha = fade;
          c.strokeStyle = "#FF8C3A"; c.lineWidth = 3 * (1 - u.t * 0.3);
          c.shadowColor = "#FF6A1A"; c.shadowBlur = 13;
          this._jag(c, u.x, u.y, ex, ey, 7, 13, 4817 + i, 1);
          c.shadowBlur = 0;
        }
        heat(u.x, u.y, 120 + 90 * grow, 0.8 * fade, "#FFB34766");
      }
      else if (u.phase === "fizzle"){
        const out = 1 - clamp(u.t / 0.85, 0, 1);
        heat(src.headX, src.headY, 80, 0.7 * out, "#FF6A1A44");
      }
    }

    else """

OVER = r"""    /* ---- Ironbloom -------------------------------------------------------
       The hold is the piece. Everything in `held` is a pure function of u.t
       because the simulation is stopped: a standing wave on the tether with
       nodes at both ends, rising in frequency and amplitude; the head going
       from orange to white; fissures of light opening across the foe's shell;
       and three charge rings collapsing inward, each one faster than the last.
       The camera shake that rides it is armed in step()'s latch branch. */
    if (u.w === "slagheart"){
      const R = CONFIG.physics.ballR;
      c.globalCompositeOperation = "lighter";

      if (u.phase === "lit"){
        const rise = clamp(u.t / 0.28, 0, 1);
        const fade = 1 - clamp((u.t - (u.life - 0.4)) / 0.4, 0, 1);
        const k2 = rise * fade;
        const hx2 = src.headX, hy2 = src.headY, HR = src.w.artW * 0.62;
        const pulse = 0.9 + 0.1 * Math.sin(u.t * 11);
        const g = c.createRadialGradient(hx2, hy2, 2, hx2, hy2, HR * 2.4 * pulse);
        g.addColorStop(0, "#FFF1C0"); g.addColorStop(0.42, "#FF8C3A99");
        g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.85 * k2; c.fillStyle = g;
        c.beginPath(); c.arc(hx2, hy2, HR * 2.4 * pulse, 0, TAU); c.fill();
        /* embers shed off the head as it swings */
        for (let i = 0; i < 10; i++){
          const ph = (u.t * (0.9 + shellHash(5501, i) * 0.7) + shellHash(5503, i)) % 1;
          const a2 = shellHash(5507, i) * TAU;
          const d = HR * (0.7 + ph * 2.4);
          c.globalAlpha = k2 * (1 - ph) * 0.8;
          c.fillStyle = i % 3 ? "#FFB347" : "#FFF1C0";
          c.beginPath();
          c.arc(hx2 + Math.cos(a2) * d, hy2 + Math.sin(a2) * d - ph * 26,
                2.6 * (1 - ph * 0.5), 0, TAU);
          c.fill();
        }
      }

      else if (u.phase === "held"){
        const k = clamp(u.t / u.life, 0, 1);
        const e = k * k, e3 = k * k * k;
        const px = src.pivX, py = src.pivY, fx = tgt.x, fy = tgt.y;
        const dx = fx - px, dy = fy - py, dl = Math.hypot(dx, dy) || 1;
        const ux = dx / dl, uy = dy / dl, nx = -uy, ny = ux;

        /* THE TETHER, taut and singing. A standing wave: zero at both ends,
           so it reads as a chain under tension rather than a wobbling rope. */
        const amp = 2 + 13 * e, freq = 26 + 120 * e;
        const draw = (w, col, al) => {
          c.globalAlpha = al; c.strokeStyle = col; c.lineWidth = w;
          c.beginPath();
          for (let i = 0; i <= 24; i++){
            const s2 = i / 24;
            const off = Math.sin(s2 * Math.PI) * Math.sin(u.t * freq + s2 * 9) * amp;
            const X = px + ux * dl * s2 + nx * off;
            const Y = py + uy * dl * s2 + ny * off;
            i ? c.lineTo(X, Y) : c.moveTo(X, Y);
          }
          c.stroke();
        };
        draw(9 + 7 * e, "#FF6A1A", 0.30 + 0.35 * e);
        draw(3.4, "#FFB347", 0.75);
        draw(1.3, "#FFF6E2", 0.55 + 0.45 * e3);

        /* The head, going white. Deliberately restrained: the first cut put a
           R*3.4 glare and a 4.6-radius corona on top of each other in lighter
           mode and the last third of the hold was a white disc with no balls
           in it — the beat has to stay a PICTURE of two things locked
           together, so the heat reads as rim and not as fill. */
        const HR = src.w.artW * 0.62;
        const gh = c.createRadialGradient(src.headX, src.headY, 2,
                                          src.headX, src.headY, HR * (1.45 + 1.1 * e));
        gh.addColorStop(0, "#FFFFFF");
        gh.addColorStop(0.30, e > 0.5 ? "#FFF6E2" : "#FFC46A");
        gh.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.60; c.fillStyle = gh;
        c.beginPath();
        c.arc(src.headX, src.headY, HR * (1.45 + 1.1 * e), 0, TAU); c.fill();

        /* fissures of light opening across the foe's shell */
        for (let i = 0; i < 9; i++){
          const a2 = (i / 9) * TAU + shellHash(5701, i) * 0.7;
          const len = R * (0.30 + 0.68 * e) * (0.6 + shellHash(5711, i) * 0.8);
          c.globalAlpha = (0.35 + 0.65 * e) * (0.5 + 0.5 * Math.sin(u.t * 30 + i));
          c.strokeStyle = e > 0.6 ? "#FFF6E2" : "#FFB347";
          c.lineWidth = 1.6 + 2.6 * e;
          c.shadowColor = "#FF8C3A"; c.shadowBlur = 12;
          this._jag(c, fx, fy, fx + Math.cos(a2) * len, fy + Math.sin(a2) * len,
                    5, 9, 5717 + i, 1);
          c.shadowBlur = 0;
        }

        /* three charge rings, collapsing inward, each faster than the last */
        for (let i = 0; i < 3; i++){
          const t0 = i * 0.26, sp = 0.30 - i * 0.06;
          const q = (u.t - t0) / sp;
          if (q <= 0 || q >= 1) continue;
          c.globalAlpha = (1 - q) * 0.75;
          c.strokeStyle = "#FFF6E2"; c.lineWidth = 2.5 + 3 * (1 - q);
          c.beginPath(); c.arc(fx, fy, R + 200 * (1 - q), 0, TAU); c.stroke();
        }

        /* the glare — a RIM on the foe's shell that brightens, not a fill.
           The stop at 0.62 keeps the middle of the gradient dark so the ball
           underneath survives right up to the blast. */
        if (e3 > 0.02){
          const gg = c.createRadialGradient(fx, fy, R * 0.55, fx, fy, R * 2.1);
          gg.addColorStop(0, "#FFF6E200");
          gg.addColorStop(0.62, "#FFE6B8" + (e3 > 0.6 ? "AA" : "77"));
          gg.addColorStop(1, "#FFF6E200");
          c.globalAlpha = 0.55 * e3; c.fillStyle = gg;
          c.beginPath(); c.arc(fx, fy, R * 2.1, 0, TAU); c.fill();
        }
      }

      else if (u.phase === "blast"){
        const q = clamp(u.t / 0.42, 0, 1);
        const fade = 1 - clamp((u.t - 0.5) / 0.9, 0, 1);
        if (q < 1){
          c.globalAlpha = (1 - q) * 0.95;
          c.strokeStyle = "#FFF6E2"; c.lineWidth = 10 * (1 - q * 0.6);
          c.beginPath(); c.arc(u.x, u.y, 30 + 470 * (1 - Math.pow(1 - q, 2.6)), 0, TAU);
          c.stroke();
          c.globalAlpha = (1 - q) * 0.6;
          c.strokeStyle = "#FF8C3A"; c.lineWidth = 5;
          c.beginPath(); c.arc(u.x, u.y, 16 + 320 * (1 - Math.pow(1 - q, 2)), 0, TAU);
          c.stroke();
        }
        const gb = c.createRadialGradient(u.x, u.y, 3, u.x, u.y, 150);
        gb.addColorStop(0, "#FFFFFF"); gb.addColorStop(0.5, "#FFB34788");
        gb.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.9 * fade * (1 - q * 0.55); c.fillStyle = gb;
        c.beginPath(); c.arc(u.x, u.y, 150, 0, TAU); c.fill();
      }

      else if (u.phase === "fizzle"){
        /* the head cools: the glow drains and the smoke goes up */
        const out = 1 - clamp(u.t / 0.85, 0, 1);
        const HR = src.w.artW * 0.62;
        const g = c.createRadialGradient(src.headX, src.headY, 2,
                                         src.headX, src.headY, HR * 2.2);
        g.addColorStop(0, "#FF8C3A"); g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.7 * out * out; c.fillStyle = g;
        c.beginPath(); c.arc(src.headX, src.headY, HR * 2.2, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        for (let i = 0; i < 7; i++){
          const ph = (u.t / 0.85 + shellHash(5901, i)) % 1;
          c.globalAlpha = out * (1 - ph) * 0.30;
          c.fillStyle = "#8A8078";
          c.beginPath();
          c.arc(src.headX + (shellHash(5903, i) - 0.5) * 34,
                src.headY - ph * 74, 4 + ph * 13, 0, TAU);
          c.fill();
        }
      }
      c.globalCompositeOperation = "source-over";
    }

    /* ---- Daybreak: white heat radiating off the whole relic ------------- */
    else """

SHARD = r"""      /* A SPLINTER OF IRONBLOOM. Not an arrow: an arrow is 9:1 and reads by
         aspect ratio, and a shard that borrowed that silhouette would read as
         a second archer on the field. This is a short hot chip that tumbles —
         deterministic tumble off its own spawn angle, so it is stable under
         the frame interpolator — with the glow carrying most of the read. */
      if (s.shard){
        const sp2 = Math.hypot(s.vx, s.vy) || 1;
        const tumble = s.a * 3 + (s.max - s.life) * 11;
        const dim = clamp(s.life / 0.5, 0, 1);
        const g2 = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 2.6);
        g2.addColorStop(0, "#FFF1C0"); g2.addColorStop(0.4, "#FF8C3A88");
        g2.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.85 * dim; c.fillStyle = g2;
        c.beginPath(); c.arc(s.x, s.y, s.r * 2.6, 0, TAU); c.fill();
        c.globalAlpha = dim;
        c.strokeStyle = "#FFE9B0"; c.lineWidth = s.r * 0.36; c.lineCap = "round";
        c.beginPath();
        c.moveTo(s.x - Math.cos(tumble) * s.r * 0.85,
                 s.y - Math.sin(tumble) * s.r * 0.85);
        c.lineTo(s.x + Math.cos(tumble) * s.r * 0.85,
                 s.y + Math.sin(tumble) * s.r * 0.85);
        c.stroke();
        c.lineCap = "butt";
        /* a short motion streak, so the direction of travel is readable */
        c.globalAlpha = 0.5 * dim;
        c.strokeStyle = "#FF8C3A"; c.lineWidth = s.r * 0.5;
        c.beginPath();
        c.moveTo(s.x - s.vx / sp2 * s.r * 2.2, s.y - s.vy / sp2 * s.r * 2.2);
        c.lineTo(s.x, s.y); c.stroke();
        continue;
      }
"""

SFX_SH = r"""        } else if (w === "slagheart"){                  // the head takes heat
          this._tone (t, { freq: 60, to: 190, gain: 0.42, dur: 1.3, type:"sine" });
          this._burst(t, { freq: 300, q: 0.6, gain: 0.26, dur: 1.4, type:"lowpass" });
          this._burst(t + 0.30, { freq: 5000, q: 0.9, gain: 0.09, dur: 0.9, type:"highpass" });
        } else if (w === "slagheart-latch"){             // the bite, and the whine
          this._burst(t, { freq: 1400, q: 2.2, gain: 0.40, dur: 0.16 });
          this._tone (t, { freq: 150, to: 62, gain: 0.44, dur: 0.30, type:"square" });
          this._tone (t + 0.06, { freq: 240, to: 1500, gain: 0.16, dur: 0.74, type:"sawtooth" });
          this._burst(t + 0.10, { freq: 2600, q: 1.4, gain: 0.10, dur: 0.70, type:"highpass" });
        } else if (w === "slagheart-blast"){             // it lets go
          this._tone (t, { freq: 260, to: 26, gain: 0.62, dur: 1.0, type:"sine" });
          this._burst(t, { freq: 200, q: 0.4, gain: 0.55, dur: 0.9, type:"lowpass" });
          this._burst(t + 0.02, { freq: 3800, q: 0.7, gain: 0.30, dur: 0.5, type:"highpass" });
          this._burst(t + 0.22, { freq: 6200, q: 1.1, gain: 0.12, dur: 0.8, type:"highpass" });
        } else if (w === "slagheart-fizzle"){            // it cools, unfired
          this._tone (t, { freq: 170, to: 52, gain: 0.20, dur: 0.7, type:"sine" });
          this._burst(t, { freq: 3000, q: 0.7, gain: 0.13, dur: 0.8, type:"highpass" });
        } else if (w === "thornwake"){                  // creak and cinch"""

# --------------------------------------------------------------------------
# THE FX CLOCK RUNS AT ~2x SIM TIME ON THE NORMAL PATH.  Measured on this
# build: `ultFx.t` advances 1.945x per second of match time while the world
# is running, and exactly 1.0x while it is frozen.  The cause is that
# `decay(dt)` calls `decayImpactOnly(dt)` (which ticks presentation) and then
# calls `tickPresentation(dt)` again itself, so a normal frame ticks the
# set-piece twice.  Every `life` number already in the engine was tuned
# against that, so this builder follows the convention rather than fixing the
# double-tick — fixing it would silently halve all sixteen existing
# set-pieces.  Credit: flagged in SLAGBURST-PATCH.md; verified here before
# being believed.
#
# THE CONSEQUENCE FOR IRONBLOOM, which shipped wrong in the first build:
#   lit     runs on the NORMAL path  -> life must be 2x the window it covers.
#           At life 6.4 the head's glow died 3.3s into a 6.0s window, so the
#           tell for the relic's signature state was absent for nearly half
#           of it.
#   blast   normal path              -> 2x
#   fizzle  normal path              -> 2x
#   held    runs INSIDE step()'s latch branch, which ticks presentation ONCE
#           -> 1x, and its life stays 1x the hold.  This exception does not
#           exist anywhere else in the game because no other set-piece owns
#           a frozen branch of its own.
FX_CLOCK = 2.0

STAMP = ("<!-- GENERATED by slagheart_build.py — Slagheart and Ironbloom. "
         "Edit the builder, not this file. -->\n")

# tuned knobs live here, never in the generated file
# TUNED. Landed by verify.py --n 60 over all 136 pairings, not by feel:
#   dmg 38.5 -> 42.4%  ·  40.0 -> 45.3%  ·  41.0 -> 45.9%
#   dmg 42.5 + shard 7.5 -> 51.5%  <-- shipped, inside Rick's 46-52 field
#   dmg 44.0 + shard 7.5 -> 54.0%  (over)
# Both knobs moved together on purpose: the design says the weight lives in
# the aftermath, so the melee stays under Gravemourn's 44.1 and the splinters
# carry the difference.
TUNED_SH = { "dmg": 42.5, "blast": 26, "shard": 7.5, "window": 6.0 }

# physics.massRef, re-derived for the SEVENTEEN-relic roster: mean(sqrt(mass))^2,
# the value that makes the mean fall multiplier exactly 1.000.  massref_probe.py
# asserts it.  Shipped by default because Rick chose to close the drift in this
# build; --no-massref rebuilds against the old 2.509 so engine_ab can still
# prove the RELIC is inert independently of the CONSTANT.
MASSREF = 2.680


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sc-introfit.html")
    ap.add_argument("--out", default="sc-slagheart.html")
    ap.add_argument("--massref", type=float, default=None,
                    help=f"physics.massRef override (default {MASSREF})")
    ap.add_argument("--no-massref", action="store_true",
                    help="leave massRef at the source's value — the build that "
                         "lets engine_ab prove the relic alone is inert")
    ap.add_argument("--dmg", type=float, default=None)
    ap.add_argument("--blast", type=float, default=None)
    ap.add_argument("--shard", type=float, default=None)
    ap.add_argument("--window", type=float, default=None)
    a = ap.parse_args()
    src, out = HERE / a.src, HERE / a.out
    if out.name in ("sundered-crown.html", "sc-base.html"):
        sys.exit("refusing to write the live line / the chain root")

    t = src.read_text()
    print(f"src {a.src}  {hashlib.sha256(t.encode()).hexdigest()[:16]}")

    relic = (RELIC
             .replace("__DMG__", str(a.dmg if a.dmg is not None else TUNED_SH["dmg"]))
             .replace("__BLAST__", str(a.blast if a.blast is not None else TUNED_SH["blast"]))
             .replace("__SHARD__", str(a.shard if a.shard is not None else TUNED_SH["shard"]))
             .replace("__WINDOW__", str(a.window if a.window is not None else TUNED_SH["window"])))

    edits = [
        # ---- the relic, after Gravemourn (the other chain relic) ----------
        ('    blurb:"A chain, not an arm. It lags, overshoots and whips — and it eats maximum life for good." },',
         '    blurb:"A chain, not an arm. It lags, overshoots and whips — and it eats maximum life for good." },\n'
         + relic.rstrip("\n")),

        # ---- match + fighter state ----------------------------------------
        ("    this.shots = [];          // live projectiles, oldest first",
         "    this.shots = [];          // live projectiles, oldest first\n"
         "    this.latch = null;        // {src,tgt,t,dur} while Ironbloom holds"),
        ("    this.ultForge = null;     // {t, minT, cap} while the Crucible is lit",
         "    this.ultForge = null;     // {t, minT, cap} while the Crucible is lit\n"
         "    this.ultHeat = null;      // {t, window} while Ironbloom's head is lit"),

        # ---- step(): the hold takes over the frame ------------------------
        ("    if (this.hitStop > 0){\n      this.hitStop -= dt;",
         LATCH_STEP + "    if (this.hitStop > 0){\n      this.hitStop -= dt;"),

        # ---- fireUlt ------------------------------------------------------
        ('    if (u.kind === "volley" && f.w.shot){',
         FIRE_LATCH + '    if (u.kind === "volley" && f.w.shot){'),
        ("              emberedge: 1.5 }[f.w.id] || 1.5,",
         "              emberedge: 1.5, slagheart: 4.9 }[f.w.id] || 1.5,"),

        # ---- TWO DELETED MECHANICS, AND WHY THE WINDOW IS THE ONLY KNOB.
        #
        # Ironbloom bites on ~61% of its casts.  Grudgebearer's Crucible, the
        # game's other conditional ultimate, strikes on 85% -- and that gap
        # was worth two attempts to close before it was understood.
        #
        #   1. A SPIN-UP, the bow's mechanic ("massive weapon rotation speed
        #      until the bow is pointed at the enemy"):
        #        spinMul 1.0, window 4.5   bite 52% +-5   hits/s 0.210
        #        spinMul 2.6, window 4.5   bite 55% +-5   hits/s 0.208
        #        spinMul 3.4, window 5.0   bite 62% +-5
        #        spinMul 2.6, window 6.0   bite 69% +-4
        #      2.6x the swing rate bought three points, inside the error bar,
        #      and moved hits/s not at all.  The bow's constraint is FACING,
        #      which spin fixes by definition; the flail's is DISTANCE.
        #
        #   2. A CHAIN PAYOUT -- lit head swings on a longer chain, which does
        #      address distance:
        #        reachMul 1.0   bite 61% +-3  (155/256 casts)
        #        reachMul 1.5   bite 63% +-3  (163/260 casts)
        #      Two points.  Also inside the error bar.
        #
        # THE REASON BOTH FAILED: the bite rate is not a weapon property at
        # all.  Slagheart's natural connect gap is 6.2s, the window is 6.0s,
        # and 1 - exp(-6.0/6.2) = 62% -- which is the measurement, to within
        # a point.  It is a Poisson trial on the foe's position, and no knob
        # on the WEAPON moves the foe.  The Crucible gets 85% because it PULLS
        # the foe onto the hammer: it promises contact, so it was given a
        # mechanism for contact.  Ironbloom promises nothing and is not given
        # one, by design -- that is the whole distinction between the two
        # dwarven ultimates, and closing the gap would have erased it.
        #
        # So the window is the only honest knob, and slagheart_probe [10]
        # asserts the Poisson prediction rather than a threshold: if the
        # observed rate ever drifts off 1 - exp(-window/gap), something is
        # eating casts and that is a bug, not a balance question.

        # ---- NO SPIN-UP. This is a deleted mechanic, kept as a comment
        # because the measurement that killed it is worth more than the code.
        #
        # The obvious fix for a 4.5s window that only caught a hit 52% of the
        # time was the bow's: "the ball gains massive weapon rotation speed
        # until the bow is pointed at the enemy and then fires."  Wired the
        # same way (ultHeat joins ultDraw/ultForge on ult.spinMul) and swept:
        #
        #     spinMul 1.0, window 4.5    latch 52% +-5    hits/s 0.210
        #     spinMul 2.6, window 4.5    latch 55% +-5    hits/s 0.208
        #     spinMul 3.4, window 5.0    latch 62% +-5    hits/s 0.235
        #     spinMul 2.6, window 6.0    latch 69% +-4    hits/s 0.229
        #
        # 2.6x the swing rate bought THREE POINTS, inside the error bar, and
        # moved hits/s not at all.  The reason is that the two ults are gated
        # on different things: the bow's constraint is FACING, which spin
        # fixes by definition, and the flail's is DISTANCE, which spin does
        # not touch at all.  The window is the only real knob, so the window
        # is the knob that moved.  A spin-up kept for the look would have been
        # a mechanic that lies about doing something.

        # ---- the window ---------------------------------------------------
        ("    if (f.ultForge){\n      /* The Crucible is lit.",
         HEAT_TICK + "    if (f.ultForge){\n      /* The Crucible is lit."),

        # ---- resolveHit: the bite, and the shard's status override --------
        ("  resolveHit(self, foe, hx, hy, seg, mul){\n",
         "  resolveHit(self, foe, hx, hy, seg, mul, over){\n" + LATCH_HIT),
        ("    for (const [k, n] of Object.entries(self.w.onHit || {})){",
         "    /* `over.onHit` lets one call site state its own statuses without\n"
         "       giving tune.py a second knob or the weapon a second field: a\n"
         "       splinter of Ironbloom sunders ONCE, where the head that threw\n"
         "       it sunders twice. Undefined everywhere else. */\n"
         "    for (const [k, n] of Object.entries(\n"
         "           (over && over.onHit) || self.w.onHit || {})){"),

        # ---- tickShots: bounce, then pop ----------------------------------
        ("      /* --- spent. No bounce: a ricocheting arrow is chaos the viewer cannot",
         SHARD_SPENT
         + "      /* --- spent. No bounce: a ricocheting arrow is chaos the viewer cannot"),

        # ---- the set-piece --------------------------------------------------
        ('    if (u.w === "dawnbringer"){\n'
         '      /* Daybreak on the floor: a breathing pool of dawn under the LIVE',
         UNDER + 'if (u.w === "dawnbringer"){\n'
         '      /* Daybreak on the floor: a breathing pool of dawn under the LIVE'),
        ("    /* ---- Daybreak: white heat radiating off the whole relic ------------- */\n"
         '    if (u.w === "dawnbringer"){',
         OVER + 'if (u.w === "dawnbringer"){'),
        ("    for (const s of m.shots){\n"
         "      const sp = Math.hypot(s.vx, s.vy) || 1;",
         "    for (const s of m.shots){\n" + SHARD
         + "      const sp = Math.hypot(s.vx, s.vy) || 1;"),
        ('        } else if (w === "thornwake"){                  // creak and cinch',
         SFX_SH),

        # ---- the splinter's arming fuse and its own status list -----------
        ('      const src = s.own === "a" ? this.a : this.b;',
         "      if (s.arm > 0) s.arm -= dt;\n"
         '      const src = s.own === "a" ? this.a : this.b;'),
        ("      if (!dead && foe.alive && src.alive\n"
         "          && Math.hypot(s.x - foe.x, s.y - foe.y) < R + s.r){",
         "      if (!dead && foe.alive && src.alive && !(s.arm > 0)\n"
         "          && Math.hypot(s.x - foe.x, s.y - foe.y) < R + s.r){"),
        ("        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul);",
         "        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul, s.over);"),

        # ---- the blast, as a method ---------------------------------------
        ("  checkEnd(){", BLAST + "  checkEnd(){"),
    ]

    for old, new in edits:
        n = t.count(old)
        if n != 1:
            sys.exit(f"anchor x{n}: {old.splitlines()[0][:72]!r}")
        t = t.replace(old, new, 1)
        print(f"  anchor {old.splitlines()[0].strip()[:66]}")

    mref = None if a.no_massref else (a.massref if a.massref is not None else MASSREF)
    if mref is not None:
        import re
        m = re.search(r"massRef:\s*([0-9.]+)", t)
        if not m:
            sys.exit("no massRef in source")
        print(f"  massRef {m.group(1)} -> {mref}")
        t = t[:m.start()] + f"massRef: {mref}" + t[m.end():]

    if not t.startswith("<!--"):
        t = STAMP + t
    out.write_text(t)
    print(f"out {a.out}  {hashlib.sha256(t.encode()).hexdigest()[:16]}  {len(t)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
