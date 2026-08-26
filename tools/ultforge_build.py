#!/usr/bin/env python3
"""THE CRUCIBLE — Grudgebearer's ultimate, redesigned. First of the big ults.

    python3 ultforge_build.py --src sc-ults-all.html --out sc-crucible.html

Rick: "when the ult fires id like the ball to start glowing a deep orange to
symbolize the fires the hammer was forged in. then id like the hammer to gain
massive rotational speed and the ball to gain a black hole type effect that
draws in its opponent. then when the weapon connects it should consume all the
stacks of sunder on its opponent and deal a massive strike with increased
critical strike chance and critical strike damage based on the number of
stacks consumed" — plus, mid-build: "MASSIVE knockback ... several high speed
bounces off the arena", and "if the hit should kill ... the ball is sent
flying and shatters against the wall."

Decisions taken in the interview, recorded:

  miss case    cap 4.0s then FIZZLE. Stacks are kept, the charge rebuilds
               from the resolution. A whiffed Crucible punishes the wielder.
  scaling      +15% crit chance and +0.4x crit damage per stack consumed.
               Six stacks = certain crit at 4.5x. Zero prior stacks still
               counts the hammer's own landing sunder, so n >= 1 always.
  the pull     continuous and RAMPING: pullBase -> pullMax over pullRamp
               seconds, squared ramp — a lean that becomes a sentence.
  name         Mountainfall -> Crucible. The vessel the fires were forged
               in; a thing that consumes and pays out transmuted.
  charge       15 -> 18. At 15 the sweep put Grudgebearer at 68-70% overall
               against a 46-52% field; a 900-match charge sweep read
               15: 70.0  17: 62.2  18: 62.3  20: 57.9  22: 61.0 (+-2pp).
               18 keeps it the strongest ball by ~10pp without making the
               other fifteen extras in its show. Rick: "if its the new
               strongest ball after these changes im ok with that within
               reason." 

DESIGN, in the engine's own grammar
-----------------------------------
`kind:"forge"` is a STATE ultimate, exactly like the bow's aimedshot: fireUlt
does not resolve it, it lights it. The payoff is an ordinary MELEE CONNECT —
tickHits finds it, resolveHit prices it, same rng draw order, same jitter,
same hit-stop scale. Nothing is rotated to a target, nothing homes; the pull
is an acceleration on the foe's velocity, i.e. every knock in the game run
backwards, and the massively spun hammer connects because the foe is dragged
into its wheel.

  minT 1.05    the bow's legibility floor, borrowed: before it, the caster's
               melee registers nothing, so the wind-up cannot be over before
               the viewer has seen it. (The foe's own blows land throughout —
               the wind-up is a promise, not an invulnerability.)
  launch       the strike's impulse is over the speed ceiling ON PURPOSE.
               `f.launch` raises the vmax clamp ~2.2x and decays over 1.8s
               while the relax term pays the speed back — which, from inside
               the physics, IS "several high speed bounces off the arena."
  kill flight  a fatal strike does not end the match where it was struck.
               checkEnd holds while `killFlight` is set; move() clears it on
               the first wall, pins the ball there, and the standard death
               (fx, kill flash, shell shatter) fires against the wall, under
               a persistent crack the new `_wallCrack` draws.

WHAT THIS DELIBERATELY DOES NOT TOUCH
-------------------------------------
Non-grudgebearer matches must be BIT-IDENTICAL to the src build: every edit is
either keyed on state only a forge ult sets (`ultForge`, `launch`,
`killFlight`) or costs zero extra rng draws. `engine_ab.py --ids <the other
fifteen>` against the src file is the proof, and the mech check here asserts
determinism on the new relic too.

The fight card needs NO builder change: the card reads `ult.name` / `ult.tip`
from the data at runtime, so the rename and the new tip line land on it by
the data edit alone. tip_audit / intro_probe verify the fit.

The fireUlt life-table entry `grudgebearer: 1.7` still exists and is now shadowed
— the forge branch overwrites `this.ultFx` with its own life. Left in place
because the generic assignment above it still executes; removing the row would
change nothing and cost an anchor.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

TIP = "Pulls the foe in and consumes Sunder — +15% crit, +0.4x dmg per stack"

# ---------------------------------------------------------------- edits ----

DATA_OLD = ('ult:{ name:"Mountainfall", charge:15, kind:"nova", radius:300, '
            'dmg:14, apply:{sunder:3}, knock:460, tip:"Nova: deals 14 damage '
            'and applies 3 Sunder stacks — extra knockback" },')
DATA_NEW = ('ult:{ name:"Crucible", charge:18, kind:"forge", radius:300,\n'
            '         minT:1.05, cap:4.0, spinMul:3.4, pullBase:260, '
            'pullMax:2600, pullRamp:1.6,\n'
            '         pullBlend:5.5, strikeMul:2.0, critPer:0.15, critMulPer:0.4, '
            'launch:2400, launchFatal:2600, stopBase:0.16, stopPer:0.06,\n'
            f'         tip:"{TIP}" }},')

FIGHTER_INIT_OLD = ("this.ultDraw = null;      "
                    "// {t, dur} while an aimed shot is being drawn")
FIGHTER_INIT_NEW = FIGHTER_INIT_OLD + """
    this.ultForge = null;     // {t, minT, cap} while the Crucible is lit
    this.launch = 0;          // seconds of raised speed ceiling after its strike"""

MATCH_INIT_OLD = ("this.ultFx    = null;     "
                  "// presentation only: drives the ultimate set-piece")
MATCH_INIT_NEW = MATCH_INIT_OLD + """
    this.killFlight = null;   // a slain ball still has a wall to meet
    this.wallCrack = null;    // presentation only: where it shattered"""

TICKCHARGE_OLD = """f.charge += dt;
    if (f.charge >= f.w.ult.charge){ f.charge = 0; this.fireUlt(f, foe); }"""
TICKCHARGE_NEW = """if (f.ultForge){
      /* The Crucible is lit. The charge does not rebuild while it burns —
         the fifteen seconds are owed from the RESOLUTION, strike or fizzle,
         or a fizzle would quietly cost four seconds less than it says. */
      const F = f.ultForge, u = f.w.ult;
      F.t += dt;
      /* The wheel cannot be stopped. Hitstun and hex would stall the sweep
         past its own cap on seeds where the foe pounds the wielder — measured
         before this line existed: the strike simply never came. An ultimate
         made of rotation that a stun can hold still is a promise the screen
         breaks, so while the forge is lit the stun burns off. */
      f.stun = 0;
      /* The singularity forms. The pull starts as a lean and ends as a
         sentence: by pullRamp seconds it redirects a cruising ball in a
         fraction of a second — "inescapable" without ever touching the foe's
         position directly. It is every knock in the game, run backwards. */
      if (foe.alive){
        const ramp = Math.min(1, F.t / u.pullRamp);
        const dx = f.x - foe.x, dy = f.y - foe.y, dl = Math.hypot(dx, dy) || 1;
        /* Two terms, both on VELOCITY, never on position. The acceleration is
           the lean — every knock in the game, run backwards. On its own it
           slingshots: measured on seed 202, the foe oscillated 620->168->322
           for four full seconds and the sweep never crossed it. A black hole
           does not oscillate its accretion, it CAPTURES it — so the second
           term bends the foe's velocity toward the infall line at a rate
           that ramps with the same clock, preserving speed. The foe spirals
           in, ballCollision holds it at contact, and the wheel gets it. */
        const acc = u.pullBase + (u.pullMax - u.pullBase) * ramp * ramp;
        foe.vx += (dx / dl) * acc * dt; foe.vy += (dy / dl) * acc * dt;
        const bl = 1 - Math.exp(-ramp * u.pullBlend * dt);
        const sp = Math.hypot(foe.vx, foe.vy);
        foe.vx += ((dx / dl) * sp - foe.vx) * bl;
        foe.vy += ((dy / dl) * sp - foe.vy) * bl;
      }
      if (F.t >= u.cap){
        /* Nothing connected. The forge gutters out and the stacks are KEPT —
           a whiffed Crucible punishes the wielder, not the foe. */
        f.ultForge = null;
        this.ultFx = { w: f.w.id, kind: "forge", phase: "fizzle",
                       src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                       x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: false,
                       radius: u.radius || 300, aff: f.aff, t: 0, life: 0.9 };
        SFX.play("ult", { w: "grudgebearer-fizzle" });
        this.note(`${f.w.name} — the Crucible gutters out`);
      }
      return;
    }
    f.charge += dt;
    if (f.charge >= f.w.ult.charge){ f.charge = 0; this.fireUlt(f, foe); }"""

VOLLEY_ANCHOR = "    /* Every bolt is a real projectile: clankable, travelling, missable."
FORGE_FIRE = """    /* THE CRUCIBLE DOES NOT RESOLVE HERE. It lights. The ball glows with the
       fires the hammer was forged in, the hammer becomes a wheel, and the
       foe is drawn in — the payoff is a MELEE CONNECT under the same rules
       every swing lives under: tickHits finds it, resolveHit prices it.
       Everything below this block is skipped for the same reason the aimed
       shot skips it: an ultimate that had already paid out before the
       hammer landed would make the hammer decorative. */
    if (u.kind === "forge"){
      f.ultForge = { t: 0, minT: u.minT || 1.0, cap: u.cap || 4.0 };
      this.ultFx = { w: f.w.id, kind: "forge", phase: "wind",
                     src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                     x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: true,
                     radius: u.radius || 300, aff: f.aff, t: 0,
                     life: (u.cap || 4.0) + 0.4 };
      /* No banner yet. The name goes on the strike, where the bow already
         put its own — you do not caption a promise. */
      this.banner = null;
      return;
    }

"""

SHAKE_OLD = ('this.shake = u.kind === "nova" && f.w.id === "grudgebearer" '
             '? 52 : 32;')
SHAKE_NEW = ("this.shake = 32;   "
             "// Mountainfall's 52 moved to the Crucible's strike")

CRIT_OLD = "    const crit = this.rng() < C.critChance;"
CRIT_NEW = """    /* THE CRUCIBLE'S STRIKE. A melee connect while the forge is lit — and
       past its legibility floor — is the ultimate resolving, priced here so
       it obeys every rule an ordinary swing obeys: same single rng draw,
       same jitter, same hit-stop scale. `n` counts the stacks the blow lands
       into, INCLUDING the one its own onHit is about to add — the hammer's
       landing is itself a sunder, and the forge burns all of it. */
    const forge = (mul === undefined && self.ultForge &&
                   self.ultForge.t >= self.ultForge.minT && self.w.ult.critPer)
      ? { n: Math.min(STATUS.sunder.maxStacks,
                      foe.stacks("sunder") + ((self.w.onHit || {}).sunder || 0)) }
      : null;
    const crit = this.rng() < (forge
      ? Math.min(1, C.critChance + self.w.ult.critPer * forge.n)
      : C.critChance);"""

DMG_OLD = """    let dmg = self.w.dmg * (mul === undefined ? 1 : mul)
            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul();"""
DMG_NEW = """    let dmg = self.w.dmg * (mul === undefined ? (forge ? self.w.ult.strikeMul : 1) : mul)
            * self.dmgMul(mods.dmg) * jitter * foe.dmgTakenMul();"""

CRITMUL_OLD = "    if (crit){ dmg *= C.critMul; self.crits++; }"
CRITMUL_NEW = ("    if (crit){ dmg *= forge ? C.critMul + self.w.ult.critMulPer"
               " * forge.n : C.critMul; self.crits++; }")

KNOCK_OLD = "    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;"
KNOCK_NEW = KNOCK_OLD + """

    if (forge){
      const u = self.w.ult, n = forge.n;
      /* CONSUMED — after dmgTakenMul was read, so the blow lands on a
         sundered shell and burns the sunder in the same act. */
      delete foe.status.sunder;
      /* Sent flying. The impulse is over the speed ceiling ON PURPOSE:
         `launch` raises the vmax clamp and the relax term spends the next
         second and a half paying it back, which — from inside the physics —
         is what several high speed bounces off the arena looks like. */
      foe.vx += (kx / kl) * (fatal ? u.launchFatal : u.launch);
      foe.vy += (ky / kl) * (fatal ? u.launchFatal : u.launch);
      foe.launch = Math.max(foe.launch || 0, 1.8);
      self.ultForge = null;
      /* Rick: "even more hit stop ... increase hit stop the more stacks its
         consuming." The generic weight above already priced the blow off its
         damage; this is ON TOP, and it scales with the CONSUME — six stacks
         freeze the hall for over half a second, a one-stack strike barely
         more than a heavy crit. The freeze is the size of the meal, which
         makes the stack count legible with no number on screen. fatal still
         takes killStop via the max. */
      this.hitStop = Math.max(this.hitStop, u.stopBase + u.stopPer * n);
      this.shake = 52;
      this.banner = { text: u.name, life: 2.1, max: 2.1, color: self.aff.core,
                      glow: self.aff.glow, w: self.w.id, bx: foe.x, by: foe.y };
      this.ultFx = { w: self.w.id, kind: "forge", phase: "strike",
                     src: self === this.a ? "a" : "b",
                     tgt: self === this.a ? "b" : "a",
                     x: hx, y: hy, tx: foe.x, ty: foe.y, hit: true, stacks: n,
                     radius: u.radius || 300, aff: self.aff, t: 0, life: 1.7 };
      SFX.play("ult", { w: "grudgebearer-hit" });
      this.note(`${self.w.name} — ${u.name} consumes ${n} Sunder`);
      if (fatal)
        /* The kill does not land here. The match holds its breath while the
           ball flies — checkEnd waits on killFlight, and move() clears it
           at the first wall, where the death actually happens. */
        this.killFlight = { tgt: foe === this.a ? "a" : "b", t: 0 };
    }"""

CLAMP_OLD = ("      const sp = clamp(sp0 + (target - sp0) * k, "
             "P.speedMin, P.speedMax);")
CLAMP_NEW = """      /* A Crucible launch is allowed over the ceiling; `launch` is the
         permission and its decay is the payment plan. Zero for every ball
         that was never struck by one, in which case vmax IS speedMax. */
      if (f.launch) f.launch = Math.max(0, f.launch - dt);
      const vmax = P.speedMax * (1 + (f.launch ? 1.15 * Math.min(1, f.launch / 0.9) : 0));
      const sp = clamp(sp0 + (target - sp0) * k, P.speedMin, vmax);"""

BOUNCED_OLD = """    if (bounced){
      const a = Math.atan2(f.vy, f.vx) + (this.rng() - 0.5) * CONFIG.physics.bounceJitter;"""
BOUNCED_NEW = """    if (bounced && this.killFlight && f === this[this.killFlight.tgt]){
      /* The wall gets it. Pinned where it hit, the flight is over, and
         checkEnd — which has been holding the match open — now ends it HERE,
         so the death fx, the kill flash and the shell shatter all happen
         against the wall instead of wherever the blow was struck. */
      this.killFlight = null;
      f.vx = 0; f.vy = 0;
      this.wallCrack = { x: f.x, y: f.y, col: f.aff.core, glow: f.aff.glow,
                         nx: f.x <= loX + 1 ? 1 : f.x >= hiX - 1 ? -1 : 0,
                         ny: f.y <= loY + 1 ? 1 : f.y >= hiY - 1 ? -1 : 0,
                         t: 0, life: 2.2 };
      this.shake = 54;
    }
    if (bounced){
      const a = Math.atan2(f.vy, f.vx) + (this.rng() - 0.5) * CONFIG.physics.bounceJitter;"""

TICKHITS_OLD = "  tickHits(self, foe, dt){"
TICKHITS_NEW = """  tickHits(self, foe, dt){
    /* A dead ball on its kill flight lands no blows; a hammer that has not
       reached the Crucible's legibility floor lands none either, so the
       wind-up cannot be over before the viewer has seen it. The foe's own
       blows land throughout — a wind-up is a promise, not a ward. */
    if (this.killFlight && self.hp <= 0) return;
    if (self.ultForge && self.ultForge.t < self.ultForge.minT) return;"""

TICKFIRE_OLD = "  tickFire(f, foe, dt){"
TICKFIRE_NEW = """  tickFire(f, foe, dt){
    if (this.killFlight && f.hp <= 0) return;   // dead balls loose nothing"""

CHECKEND_OLD = """  checkEnd(){
    const a = this.a, b = this.b;"""
CHECKEND_NEW = """  checkEnd(){
    if (this.killFlight) return;   // the slain ball has a wall to meet first
    const a = this.a, b = this.b;"""

STEP_OLD = """    this.checkEnd();
    this.decay(dt);"""
STEP_NEW = """    if (this.killFlight){
      this.killFlight.t += dt;
      /* Cannot fire — a launched ball meets a wall in well under a second —
         but a flight with no upper bound is a hung match waiting to be
         discovered by someone else. The bow's cap, same reasoning. */
      if (this.killFlight.t > 2.5) this.killFlight = null;
    }
    this.checkEnd();
    this.decay(dt);"""

SPIN_OLD = """    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw ? (f.w.ult.spinMul || 1) : 1);"""
SPIN_NEW = """    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge ? (f.w.ult.spinMul || 1) : 1);"""

PRES_OLD = """    if (this.ultFx){
      this.ultFx.t += dt;
      if (this.ultFx.t > this.ultFx.life) this.ultFx = null;
    }"""
PRES_NEW = PRES_OLD + """
    if (this.wallCrack){
      this.wallCrack.t += dt;
      if (this.wallCrack.t > this.wallCrack.life) this.wallCrack = null;
    }"""

UNDERHEAD_OLD = """  drawUltUnder(m){
    const s = this._ult(m); if (!s) return;"""
UNDERHEAD_NEW = """  drawUltUnder(m){
    if (m.wallCrack) this._wallCrack(m);
    const s = this._ult(m); if (!s) return;"""

ULTM_OLD = "  _ult(m){"
ULTM_NEW = """  /* Where the Crucible's kill met the arena. The cracks grow in over a
     sixth of a second and then SIT there under the death shatter — a wall
     that takes a relic at that speed is not the same wall afterwards. */
  _wallCrack(m){
    const W = m.wallCrack, c = this.ctx;
    const grow = clamp(W.t / 0.16, 0, 1);
    const fade = 1 - clamp((W.t - W.life + 0.6) / 0.6, 0, 1);
    const base = Math.atan2(W.ny, W.nx);            // into the hall
    c.save();
    c.lineCap = "round";
    for (let i = 0; i < 9; i++){
      const a = base + (shellHash(83, i) - 0.5) * 2.4;
      const len = (34 + shellHash(97, i) * 92) * grow;
      const ex = W.x + Math.cos(a) * len, ey = W.y + Math.sin(a) * len;
      c.globalAlpha = 0.8 * fade;
      c.strokeStyle = "#11131A"; c.lineWidth = 3.4;
      this._jag(c, W.x, W.y, ex, ey, 6, 7, 610 + i, 1);
      c.globalAlpha = 0.35 * fade;
      c.strokeStyle = W.glow; c.lineWidth = 1.2;
      this._jag(c, W.x, W.y, ex, ey, 6, 7, 610 + i, 1);
    }
    c.restore();
  }

  _ult(m){"""

# ------------------------------------------------------ the set-piece art ----

UNDER_MARK = ('    else if (u.w === "grudgebearer"){\n'
              '      /* The floor itself comes apart.')
UNDER_NEW = '''    else if (u.w === "grudgebearer"){
      if (u.phase === "strike"){
        /* the floor takes the blow: molten cracks out of the impact */
        const grow = clamp(u.t / 0.22, 0, 1);
        const fade = 1 - clamp((u.t - 0.7) / 0.9, 0, 1);
        for (let i = 0; i < 8; i++){
          const a = (i / 8) * TAU + shellHash(4242, i) * 0.5;
          const len = 190 * (0.6 + shellHash(1717, i) * 0.6) * grow;
          const ex = u.x + Math.cos(a) * len, ey = u.y + Math.sin(a) * len;
          c.globalAlpha = 0.85 * fade;
          c.strokeStyle = "#2E1B0A"; c.lineWidth = 7 * (1 - u.t * 0.35);
          this._jag(c, u.x, u.y, ex, ey, 7, 12, 910 + i, 1);
          c.globalAlpha = fade;
          c.strokeStyle = "#FF8C3A"; c.lineWidth = 2.6 * (1 - u.t * 0.3);
          c.shadowColor = "#FF6A1A"; c.shadowBlur = 12;
          this._jag(c, u.x, u.y, ex, ey, 7, 12, 910 + i, 1);
          c.shadowBlur = 0;
        }
      }
      else if (u.phase === "fizzle"){
        /* the light pool dies where the caster stands */
        const out = 1 - clamp(u.t / 0.85, 0, 1);
        const g = c.createRadialGradient(src.x, src.y, 4, src.x, src.y, 110);
        g.addColorStop(0, "#FF6A1A55"); g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.8 * out;
        c.fillStyle = g;
        c.beginPath(); c.arc(src.x, src.y, 110, 0, TAU); c.fill();
      }
      else {
        /* WIND. The forge light on the floor, and the floor being TAKEN:
           the pool breathes under the ball while the grit of the arena
           streams inward in tightening spirals — accretion, drawn with the
           same vocabulary as the motes the hall already floats. Anchored to
           the LIVE caster, because unlike every other set-piece this one
           lasts seconds and the caster does not stand still for it. */
        const r = clamp(u.t / 1.6, 0, 1);
        const pulse = 0.85 + 0.15 * Math.sin(u.t * 9);
        const g = c.createRadialGradient(src.x, src.y, 6, src.x, src.y, 120 * pulse);
        g.addColorStop(0, "#FF6A1A66"); g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.85 * r;
        c.fillStyle = g;
        c.beginPath(); c.arc(src.x, src.y, 120 * pulse, 0, TAU); c.fill();
        for (let i = 0; i < 14; i++){
          const ph = (u.t * (0.55 + shellHash(21, i) * 0.5) + shellHash(11, i)) % 1;
          const d = 300 * (1 - ph);
          const a = shellHash(31, i) * TAU + u.t * 1.6 + ph * 2.4;
          c.globalAlpha = r * (1 - ph) * 0.55;
          c.strokeStyle = i % 3 ? "#7A5A38" : "#E8A34E";
          c.lineWidth = 2.2;
          c.beginPath();
          c.arc(src.x, src.y, Math.max(2, d), a, a + 0.5 + ph * 0.5);
          c.stroke();
        }
      }
    }'''

OVER_MARK = ('    /* ---- Mountainfall: something enormous lands */\n'
             '    else if (u.w === "grudgebearer"){')
OVER_NEW = '''    /* ---- Crucible: the forge lights, the hall bends inward, the blow ---- */
    else if (u.w === "grudgebearer"){
      const R = CONFIG.physics.ballR;
      if (u.phase === "strike"){
        /* the payoff: the singularity collapses INTO the blow and the blow
           pays it back out as heat. `stacks` sizes the flare and the slag —
           six sunder read bigger than one without a word of text. */
        const n = u.stacks || 0;
        const flash = 1 - clamp(u.t / 0.14, 0, 1);
        if (flash > 0){
          c.globalCompositeOperation = "lighter";
          const g = c.createRadialGradient(u.x, u.y, 2, u.x, u.y, 150);
          g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.4, "#FFD9A0");
          g.addColorStop(1, "#FF6A1A00");
          c.globalAlpha = flash;
          c.fillStyle = g;
          c.beginPath(); c.arc(u.x, u.y, 150, 0, TAU); c.fill();
          c.globalCompositeOperation = "source-over";
        }
        const imp = 1 - clamp(u.t / 0.20, 0, 1);       // the horizon, imploding
        if (imp > 0){
          c.globalAlpha = imp * 0.8;
          c.strokeStyle = "#0A0710"; c.lineWidth = 9 * imp;
          c.beginPath(); c.arc(u.x, u.y, R * 1.6 * imp, 0, TAU); c.stroke();
        }
        const ex = clamp(u.t / 0.45, 0, 1);
        const fade = 1 - clamp((u.t - 0.5) / 1.1, 0, 1);
        const rad = (150 + n * 28) * (1 - Math.pow(1 - ex, 2.6));
        c.globalAlpha = fade;
        c.strokeStyle = "#FFE7C2"; c.lineWidth = 5 * (1 - ex * 0.6);
        c.shadowColor = "#FF6A1A"; c.shadowBlur = 18;
        c.beginPath(); c.arc(u.x, u.y, rad, 0, TAU); c.stroke();
        c.shadowBlur = 0;
        for (let i = 0; i < 4 + n * 3; i++){           // the consumed, as slag
          const a = shellHash(131, i) * TAU;
          const d = rad * (0.4 + shellHash(141, i) * 0.7);
          c.globalAlpha = fade * 0.85;
          c.fillStyle = i % 3 ? "#FF8C3A" : "#FFD9A0";
          c.save();
          c.translate(u.x + Math.cos(a) * d, u.y + Math.sin(a) * d - ex * 26);
          c.rotate(u.t * 7 + i);
          const sz = 2.5 + shellHash(151, i) * 5;
          c.fillRect(-sz / 2, -sz / 2, sz, sz);
          c.restore();
        }
        const fl = clamp((u.t - 0.04) / 0.30, 0, 1);   // the flare column
        const fh = (70 + n * 34) * fl;
        if (fh > 0){
          c.globalCompositeOperation = "lighter";
          c.globalAlpha = fade * 0.7 * fl;
          const g2 = c.createLinearGradient(u.x, u.y, u.x, u.y - fh);
          g2.addColorStop(0, "#FFD9A0AA"); g2.addColorStop(1, "#FF6A1A00");
          c.fillStyle = g2;
          c.fillRect(u.x - 10, u.y - fh, 20, fh);
          c.globalCompositeOperation = "source-over";
        }
      }
      else if (u.phase === "fizzle"){
        /* the horizon lets go and the heat guts out DOWNWARD — a thing that
           failed, not a thing that ended */
        const out = 1 - clamp(u.t / 0.88, 0, 1);
        c.globalAlpha = out * 0.5;
        c.strokeStyle = "#0A0710"; c.lineWidth = 8 * out;
        c.beginPath();
        c.arc(src.x, src.y, R * (1.55 + (1 - out) * 0.9), 0, TAU); c.stroke();
        for (let i = 0; i < 8; i++){
          const ph = clamp(u.t * 1.4 - shellHash(161, i) * 0.3, 0, 1);
          c.globalAlpha = out * (1 - ph) * 0.8;
          c.fillStyle = i % 2 ? "#FF8C3A" : "#E8A34E";
          c.beginPath();
          c.arc(src.x + (shellHash(171, i) - 0.5) * 70,
                src.y + ph * 60 + (shellHash(181, i) - 0.5) * 20,
                2.6 * (1 - ph * 0.5), 0, TAU);
          c.fill();
        }
      }
      else {
        /* WIND: the deep-orange forge glow, the event horizon, accretion
           streamers, the hammer's wheel of heat, and the foe's dust torn
           down the pull. All anchored to the LIVE fighters — this piece
           runs seconds and both of them keep moving. */
        const r = clamp(u.t / 1.6, 0, 1);
        const pulse = 0.9 + 0.1 * Math.sin(u.t * 11);
        c.globalCompositeOperation = "lighter";
        const g = c.createRadialGradient(src.x, src.y, 2, src.x, src.y, R * 2.6 * pulse);
        g.addColorStop(0, "#FFD9A0"); g.addColorStop(0.45, "#FF6A1A88");
        g.addColorStop(1, "#FF6A1A00");
        c.globalAlpha = 0.75 * r;
        c.fillStyle = g;
        c.beginPath(); c.arc(src.x, src.y, R * 2.6 * pulse, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 0.55 * r;                       // the event horizon
        c.strokeStyle = "#0A0710"; c.lineWidth = 10;
        c.beginPath(); c.arc(src.x, src.y, R * 1.55, 0, TAU); c.stroke();
        c.globalAlpha = 0.9 * r;                        // lensed rim, running
        c.strokeStyle = "#FFE7C2"; c.lineWidth = 1.6;
        c.shadowColor = "#FF8C3A"; c.shadowBlur = 14;
        c.beginPath();
        c.arc(src.x, src.y, R * 1.72, u.t * 5.2, u.t * 5.2 + 4.6);
        c.stroke();
        c.shadowBlur = 0;
        for (let i = 0; i < 3; i++){                    // accretion streamers
          const a0 = u.t * (6.4 + i * 0.6) + i * (TAU / 3);
          c.globalAlpha = r * 0.7;
          c.strokeStyle = i ? "#E8A34E" : "#FF7A2A";
          c.lineWidth = 2.6;
          c.beginPath();
          for (let q = 0; q < 10; q++){
            const t2 = q / 9;
            const rr = R * (3.4 - 1.6 * t2);
            const aa = a0 + t2 * 2.2;
            const px = src.x + Math.cos(aa) * rr, py = src.y + Math.sin(aa) * rr;
            q ? c.lineTo(px, py) : c.moveTo(px, py);
          }
          c.stroke();
        }
        /* the hammer's wheel: the spin itself is real (tickWeapon runs it at
           spinMul); this is the heat it leaves behind the head */
        const reach = src.w.reach + 14;
        for (let k2 = 0; k2 < 6; k2++){
          c.globalAlpha = r * 0.5 * (1 - k2 / 6);
          c.strokeStyle = k2 % 2 ? "#FFB36B" : "#FFE7C2";
          c.lineWidth = 12 - k2 * 1.4;
          c.beginPath();
          c.arc(src.x, src.y, reach, src.theta - 0.16 - k2 * 0.34,
                src.theta - k2 * 0.34);
          c.stroke();
        }
        for (let i = 0; i < 6; i++){                    // dust down the pull
          const ph = (u.t * 1.3 + shellHash(61, i)) % 1;
          const px = lerp(tgt.x, src.x, ph), py = lerp(tgt.y, src.y, ph);
          c.globalAlpha = r * (1 - ph) * 0.5;
          c.fillStyle = "#E8A34E";
          c.beginPath();
          c.arc(px + (shellHash(71, i) - 0.5) * 22 * (1 - ph),
                py + (shellHash(81, i) - 0.5) * 22 * (1 - ph),
                2.4 - ph, 0, TAU);
          c.fill();
        }
      }
    }'''

SFX_OLD = '''} else if (w === "grudgebearer"){               // the ground
          this._tone (t, { freq: 96, to: 26, gain: 0.60, dur: 1.0, type:"sine" });
          this._burst(t, { freq: 300, q: 0.5, gain: 0.42, dur: 0.7, type:"lowpass" });
          this._burst(t + 0.09, { freq: 120, q: 0.4, gain: 0.30, dur: 0.9, type:"lowpass" });
        } else if (w === "thornwake"){'''
SFX_NEW = '''} else if (w === "grudgebearer"){               // the forge lights, the spin winds
          this._tone (t, { freq: 46, to: 138, gain: 0.50, dur: 1.5, type:"sine" });
          this._tone (t + 0.10, { freq: 170, to: 660, gain: 0.15, dur: 1.4, type:"sawtooth" });
          this._burst(t, { freq: 240, q: 0.6, gain: 0.30, dur: 1.5, type:"lowpass" });
          this._burst(t + 0.55, { freq: 900, q: 1.2, gain: 0.10, dur: 0.9, type:"lowpass" });
        } else if (w === "grudgebearer-hit"){           // the implosion pays out
          this._tone (t, { freq: 320, to: 24, gain: 0.60, dur: 0.9, type:"sine" });
          this._burst(t, { freq: 260, q: 0.5, gain: 0.50, dur: 0.8, type:"lowpass" });
          this._burst(t + 0.05, { freq: 2400, q: 1.0, gain: 0.16, dur: 0.3, type:"highpass" });
        } else if (w === "grudgebearer-fizzle"){        // the draught dies
          this._tone (t, { freq: 130, to: 40, gain: 0.22, dur: 0.7, type:"sine" });
          this._burst(t, { freq: 420, q: 0.8, gain: 0.12, dur: 0.6, type:"lowpass" });
        } else if (w === "thornwake"){'''

EDITS = [
    ("ult data (Crucible)",        DATA_OLD,        DATA_NEW),
    ("fighter init",               FIGHTER_INIT_OLD, FIGHTER_INIT_NEW),
    ("match init",                 MATCH_INIT_OLD,  MATCH_INIT_NEW),
    ("tickCharge forge state",     TICKCHARGE_OLD,  TICKCHARGE_NEW),
    ("fireUlt cast shake",         SHAKE_OLD,       SHAKE_NEW),
    ("fireUlt forge branch",       VOLLEY_ANCHOR,   FORGE_FIRE + VOLLEY_ANCHOR),
    ("resolveHit crit chance",     CRIT_OLD,        CRIT_NEW),
    ("resolveHit strike mul",      DMG_OLD,         DMG_NEW),
    ("resolveHit crit mul",        CRITMUL_OLD,     CRITMUL_NEW),
    ("resolveHit forge payoff",    KNOCK_OLD,       KNOCK_NEW),
    ("move launch ceiling",        CLAMP_OLD,       CLAMP_NEW),
    ("move wall shatter",          BOUNCED_OLD,     BOUNCED_NEW),
    ("tickHits gates",             TICKHITS_OLD,    TICKHITS_NEW),
    ("tickFire gate",              TICKFIRE_OLD,    TICKFIRE_NEW),
    ("checkEnd hold",              CHECKEND_OLD,    CHECKEND_NEW),
    ("step killFlight clock",      STEP_OLD,        STEP_NEW),
    ("tickWeapon forge spin",      SPIN_OLD,        SPIN_NEW),
    ("tickPresentation wallCrack", PRES_OLD,        PRES_NEW),
    ("drawUltUnder wallCrack",     UNDERHEAD_OLD,   UNDERHEAD_NEW),
    ("_wallCrack method",          ULTM_OLD,        ULTM_NEW),
    ("ult SFX (cast/hit/fizzle)",  SFX_OLD,         SFX_NEW),
]


def replace_block(s: str, marker: str, new_block: str, name: str) -> str:
    """Replace an `else if (...){ ... }` block located by its opening marker,
    scanning to the matching close brace. The blocks this touches contain no
    braces inside string literals — the page-load check would catch it if
    that ever stops being true."""
    i = s.find(marker)
    if i < 0 or s.find(marker, i + 1) >= 0:
        raise SystemExit(f"! block marker for {name} not unique")
    j = s.index("{", i)
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{": depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0: break
        k += 1
    return s[:i] + new_block + s[k + 1:]


# ------------------------------------------------------------- checks ----

MECH_JS = r"""
() => {
  const out = {};
  const dt = 1 / 120;
  const mk = (seed) => { const m = new AC.Match("grudgebearer", "axiom", seed);
                         m.introT = 0; return m; };

  { // A: cast -> wind state, banner deferred, the pull closes distance
    const m = mk(101);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultForge && g++ < 600) m.step(dt);
    const wind = !!m.a.ultForge && m.ultFx && m.ultFx.kind === "forge"
                 && m.ultFx.phase === "wind";
    const noBanner = !m.banner;
    const d0 = Math.hypot(m.b.x - m.a.x, m.b.y - m.a.y);
    let minD = d0;
    for (let i = 0; i < 520 && m.a.ultForge; i++){ m.step(dt);
      minD = Math.min(minD, Math.hypot(m.b.x - m.a.x, m.b.y - m.a.y)); }
    out.A = { wind, noBanner, d0: Math.round(d0), minD: Math.round(minD) };
  }

  { // B: the strike — stacks consumed, launch, banner, overspeed
    const m = mk(202);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultForge && g++ < 600) m.step(dt);
    m.b.apply("sunder", 6);
    const before = m.b.stacks("sunder");
    g = 0; while (m.a.ultForge && g++ < 900) m.step(dt);
    const struck = m.ultFx && m.ultFx.phase === "strike";
    const stacksFx = m.ultFx ? m.ultFx.stacks : null;
    const consumed = m.b.stacks("sunder") === 0;
    const launched = m.b.launch > 0;
    const banner = m.banner ? m.banner.text : null;
    const stop = m.hitStop;
    let top = 0;
    for (let i = 0; i < 200; i++){ m.step(dt);
      top = Math.max(top, Math.hypot(m.b.vx, m.b.vy)); }
    out.B = { struck, before, stacksFx, consumed, launched, banner,
              hitStop: +stop.toFixed(2), topSpeed: Math.round(top) };
  }

  { // C: the fizzle — minT pushed past cap, stacks KEPT, charge rebuilds
    const m = mk(303);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultForge && g++ < 600) m.step(dt);
    m.a.ultForge.minT = 99;               // no strike can happen
    m.b.apply("sunder", 4);
    g = 0; while (m.a.ultForge && g++ < 800) m.step(dt);
    const fizzled = m.ultFx && m.ultFx.phase === "fizzle";
    const kept = m.b.stacks("sunder") > 0;
    const c0 = m.a.charge;
    for (let i = 0; i < 120; i++) m.step(dt);
    out.C = { fizzled, kept, rebuild: m.a.charge > c0, noBanner: !m.banner ||
              (m.banner.text !== "Crucible") };
  }

  { // D: the kill flight — match holds, ball meets a wall, dies THERE
    const m = mk(404);
    m.a.hp = m.a.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultForge && g++ < 600) m.step(dt);
    m.b.apply("sunder", 6);
    m.b.hp = 3;                            // the strike must kill
    g = 0; while (m.a.ultForge && g++ < 700) m.step(dt);
    const flight = !!m.killFlight;
    const heldOpen = !m.over;
    g = 0; while (!m.over && g++ < 500) m.step(dt);
    const A = AC.CONFIG.arena;
    const lx = m.loser ? m.loser.x : -1, ly = m.loser ? m.loser.y : -1;
    out.D = { flight, heldOpen, over: m.over, reason: m.reason,
              crack: !!m.wallCrack,
              wallDist: m.loser ? Math.round(Math.min(lx, A.w - lx, ly, A.h - ly)) : -1 };
  }

  { // E: determinism — same seed, same summary, twice
    const r1 = AC.simulate("grudgebearer", "axiom", 999);
    const r2 = AC.simulate("grudgebearer", "axiom", 999);
    out.E = { same: JSON.stringify(r1) === JSON.stringify(r2) };
  }
  return out;
}
"""

ART_JS = r"""
() => {
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){};
  const m = new AC.Match("grudgebearer", "axiom", 4242);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.30; m.a.y = A.h * 0.36;
  m.b.x = A.w * 0.72; m.b.y = A.h * 0.66;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const grab = () => { c.setTransform(1,0,0,1,0,0); c.fillStyle = "#000";
                       c.fillRect(0,0,1080,1920); AC.__draw(m);
                       return c.getImageData(0,0,1080,1920).data; };
  const diff = (a, b) => { let n = 0;
    for (let i = 0; i < a.length; i += 16)
      if (Math.abs(a[i]-b[i]) + Math.abs(a[i+1]-b[i+1]) + Math.abs(a[i+2]-b[i+2]) > 12) n++;
    return n; };
  const out = [];
  const fx = (phase, t, x, y) => ({ w: "grudgebearer", kind: "forge", phase,
    src: "a", tgt: "b", x, y, tx: m.b.x, ty: m.b.y, hit: true, stacks: 5,
    radius: 300, aff: m.a.aff, t, life: 4.4 });
  for (const [phase, ts, x, y] of [
      ["wind",   [0.3, 1.2, 2.4, 3.6], m.a.x, m.a.y],
      ["strike", [0.05, 0.3, 0.9, 1.4], m.b.x, m.b.y],
      ["fizzle", [0.05, 0.35, 0.6], m.a.x, m.a.y]]){
    for (const t of ts){
      m.ultFx = fx(phase, t, x, y);
      let threw = null, px = 0;
      try { const a = grab(); m.ultFx = null; const b = grab(); px = diff(a, b); }
      catch (e) { threw = String(e); }
      out.push({ phase, t, px, threw });
    }
  }
  // the wall crack draws
  m.ultFx = null;
  m.wallCrack = { x: 20, y: A.h * 0.5, col: "#9C6326", glow: "#E8A34E",
                  nx: 1, ny: 0, t: 0.3, life: 2.2 };
  { const a = grab(); m.wallCrack = null; const b = grab();
    out.push({ phase: "wallcrack", t: 0.3, px: diff(a, b), threw: null }); }
  return out;
}
"""

# every OTHER relic's set-piece must still draw — the ultart2 check, rerun
REGRESS_JS = r"""
(ids) => {
  const out = [];
  for (const id of ids){
    const w = AC.WEAPONS.find(x => x.id === id);
    const foe = id === "dawnbringer" ? "grudgebearer" : "dawnbringer";
    const m = new AC.Match(id, foe, 0x9A11 + 7);
    AC.setResolution(1080, 1920);
    const f = m.a, fo = m.b;
    let threw = null, peak = 0;
    for (const t of [0.05, 0.25, 0.5, 0.9, 1.3]){
      m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
                  x: f.x, y: f.y, tx: fo.x, ty: fo.y, hit: true,
                  radius: w.ult.radius || 300, aff: f.aff, t: t, life: 2.2,
                  shots: w.ult.shots || 0 };
      const cv = document.getElementById('cv'), c = cv.getContext('2d');
      c.setTransform(1,0,0,1,0,0); c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      try { AC.__draw(m); } catch (e) { threw = String(e); break; }
      const a = c.getImageData(0,0,1080,1920).data;
      m.ultFx = null;
      c.setTransform(1,0,0,1,0,0); c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      AC.__draw(m);
      const b = c.getImageData(0,0,1080,1920).data;
      let d = 0;
      for (let i = 0; i < a.length; i += 16)
        if (Math.abs(a[i]-b[i]) + Math.abs(a[i+1]-b[i+1]) + Math.abs(a[i+2]-b[i+2]) > 12) d++;
      peak = Math.max(peak, d);
    }
    out.push({ id, threw, peak });
  }
  return out;
}
"""

OTHERS = ["dawnbringer", "widowmaker", "thornwake", "gravemourn", "spellbreaker",
          "oathwound", "heartwood", "nightfell", "axiom", "ironhail",
          "lightkeeper", "farwarden", "aureole", "censer", "emberedge"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-ults-all.html")
    ap.add_argument("--out", default="sc-crucible.html")
    ap.add_argument("--no-check", action="store_true")
    A = ap.parse_args()

    if pathlib.Path(A.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    if len(TIP) > 72:
        print(f"! ult tip is {len(TIP)} chars, cap 72", file=sys.stderr)
        return 1
    src = HERE / A.src
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr); return 2
    s = src.read_text(encoding="utf-8")

    for name, old, _ in EDITS:
        n = s.count(old)
        if n != 1:
            print(f"! anchor '{name}' appears {n} times, expected 1", file=sys.stderr)
            return 3
    for name, old, new in EDITS:
        s = s.replace(old, new, 1)
        print(f"  [ultforge] {name}")

    s = replace_block(s, OVER_MARK, OVER_NEW, "drawUltOver grudgebearer")
    print("  [ultforge] drawUltOver: Mountainfall -> Crucible (3 phases)")
    s = replace_block(s, UNDER_MARK, UNDER_NEW, "drawUltUnder grudgebearer")
    print("  [ultforge] drawUltUnder: Mountainfall -> Crucible (3 phases)")

    doc = "<!DOCTYPE html>\n"
    i = s.find(doc)
    if i < 0:
        print("! no doctype", file=sys.stderr); return 4
    stamp = (f"<!-- GENERATED by ultforge_build.py --src {A.src} — "
             f"do not hand-edit or tune in place -->")
    s = s[:i + len(doc)] + stamp + "\n" + s[i + len(doc):]

    out = HERE / A.out
    out.write_text(s, encoding="utf-8")
    print(f"{A.src} -> {A.out}   sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}")
    if A.no_check:
        print("  ! checks skipped"); return 0

    sys.path.insert(0, str(HERE))
    from scpage import game
    bad = []
    with game(game_path=out) as (page, errors):
        art = page.evaluate(ART_JS)
        mech = page.evaluate(MECH_JS)
        reg = page.evaluate(REGRESS_JS, OTHERS)
        if errors:
            print(f"! page errors: {errors[:4]}", file=sys.stderr)
            out.unlink(); return 5

    print("\n  ART — pixel diff per phase sample (fail < 200):")
    for r in art:
        flag = "" if (r["px"] >= 200 and not r["threw"]) else "  <-- FAIL"
        if r["threw"]: bad.append(f"art {r['phase']} t={r['t']}: threw {r['threw'][:70]}")
        elif r["px"] < 200: bad.append(f"art {r['phase']} t={r['t']}: {r['px']} px")
        print(f"    {r['phase']:<10} t={r['t']:<5} {r['px']:>7}{flag}")

    print("\n  MECH:")
    print("   ", json.dumps(mech, indent=2).replace("\n", "\n    "))
    m = mech
    checks = [
        ("A wind state + no banner", m["A"]["wind"] and m["A"]["noBanner"]),
        ("A pull closes distance",   m["A"]["minD"] < m["A"]["d0"] - 100),
        ("B strike happened",        bool(m["B"]["struck"])),
        ("B stacks consumed",        m["B"]["consumed"] and m["B"]["before"] == 6),
        ("B fx carries stack count", m["B"]["stacksFx"] == 6),
        ("B launch + overspeed",     m["B"]["launched"] and
                                     m["B"]["topSpeed"] > 1400),
        ("B banner on the strike",   m["B"]["banner"] == "Crucible"),
        ("B freeze scales with meal", m["B"]["hitStop"] >= 0.16 + 0.06 * 6 - 0.01),
        ("C fizzle at cap",          bool(m["C"]["fizzled"])),
        ("C stacks kept",            bool(m["C"]["kept"])),
        ("C charge rebuilds",        bool(m["C"]["rebuild"])),
        ("D kill held for flight",   m["D"]["flight"] and m["D"]["heldOpen"]),
        ("D died slain at a wall",   m["D"]["over"] and m["D"]["reason"] == "slain"
                                     and m["D"]["wallDist"] < 120),
        ("D wall crack present",     bool(m["D"]["crack"])),
        ("E deterministic",          bool(m["E"]["same"])),
    ]
    for name, ok in checks:
        print(f"    {'PASS' if ok else 'FAIL'}  {name}")
        if not ok: bad.append(f"mech: {name}")

    print("\n  REGRESSION — the other fifteen set-pieces still draw:")
    for r in reg:
        ok = not r["threw"] and r["peak"] >= 200
        if not ok: bad.append(f"regress {r['id']}: threw={r['threw']} peak={r['peak']}")
        print(f"    {r['id']:<13} peak {r['peak']:>6}  {'ok' if ok else 'FAIL'}")

    print()
    if bad:
        print("  ULTFORGE CHECK FAILED:")
        for b in bad: print("   ", b)
        out.unlink(); print(f"\n  {A.out} deleted.")
        return 6
    print("  ultforge check PASS — Crucible winds, strikes, fizzles, and kills"
          " against the wall;")
    print("  the other fifteen relics untouched. Run engine_ab.py for the"
          " bit-identity proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
