#!/usr/bin/env python3
"""DAYBREAK — Dawnbringer's ultimate, redesigned. Second of the big ults.

    python3 ultdawn_build.py --src sc-crucible.html --out sc-daybreak.html

Rick: "for a few seconds after the ult triggers dawnbringer gains an animation
where it radiates with white hot fire/heat. any time it connects a hit during
the ult white hot sparks fly off the point of impact and drift around the
arena. opponents hitting the sparks take damage and slight knockback and when
dawnbringer hits the sparks it gains a stacking buff that applies a small
amount of healing over time."

WHY THIS RELIC, WHY THIS SHAPE
------------------------------
Dawnbringer was the weakest ball (46-48%) while carrying the strongest ult in
the game — Judgement's flat 34 heal, measured at +9 to +32pp of winrate in
EVERY matchup (paired-seed test, heal 34 vs 0). tune.py paid for that subsidy
by starving the blade to 8.88, the weakest greatsword. Daybreak deletes the
subsidy: the cast deals nothing and heals nothing. All value flows through
FIGHTING during a 5s window — hits spray drifting sparks that burn the foe
(8 + a shove) or become healing when Dawnbringer collects them — and the
blade gets its damage back (TUNED_DB below).

Decisions from the interview, recorded:

  spark heat   "meaningful zone": 8 damage + a real shove. The balls cannot
               steer, so zone control here IS the knockback — the cloud is a
               soft wall that deflects the foe and chains bonus damage in
               the scrum.
  heal budget  weaker than the old heal, blade repaid: Blessing stacks at
               1.2 hp/s, cap 5, 6s, refresh on collect. Fully stacked and
               fed, ~36 hp over 6s — earned, not granted.
  window       5s, cadence unchanged (charge stays at Judgement's 14 — the
               interview option said "fires as often as the old Judgement
               did", and that is 14, not the 15 the label guessed).
  name         Daybreak. Cast is pure ignition; beam 18 and heal 34 are gone.

ENGINE SHAPE
------------
`kind:"radiant"` — a timed state like the forge, but the charge does NOT
gate on it: the window is the payoff, not a promise of one. Sparks are SIM
objects (they deal damage and heal), spawned only inside resolveHit under
`self.ultRadiant`, so no other match ever draws differently from the rng —
engine_ab over the other fifteen is the proof, again. Their drift is
deterministic (per-spark phase against match time, zero per-frame rng).
The Blessing heal path ALREADY existed dormant in tickStatus
(`key === "blessing"` heals off def.hps); this build adds the STATUS entry
that makes it reachable, capped and clocked like every other status.

The fight card needs no builder change (name/tip read from data at runtime);
Blessing's first landing teaches itself through the existing statusTag path,
warm-white fallback colors and all.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

TIP = "For 5s its hits spray sparks — 8 dmg to foes, healing when collected"

# The blade, repaid. Judgement's flat heal bought its winrate everywhere and
# tune.py paid with the weakest greatsword blade (8.88). Swept after the
# mechanics landed — see the sweep table in the session doc.
TUNED_DB = 9.6
# Swept on the final spark shape (3/hit, life 5.5, born fast):
#   blade 8.88 -> 52.4%   9.5 -> 59.7   10.2 -> 56.5   11.0 -> 62.3  (n=750, +-1.8pp)
# 8.88 would park it mid-table but repays nothing; Rick chose "meaningful
# zone" AND "blade repaid", and both together buy a clear #2 ball behind the
# Crucible. 10.2 is that: blade +15%, ~56%, comfortably inside the 30-70 band.

# ---------------------------------------------------------------- edits ----

ULT_OLD = ('ult:{ name:"Judgement", charge:14, kind:"beam", dmg:18, heal:34, '
           'tip:"Pillar of light: deals 18 damage, heals 34" },')
ULT_NEW = ('ult:{ name:"Daybreak", charge:14, kind:"radiant", dur:5.0,\n'
           '         sparks:3, sparkDmg:8, sparkKnock:260, sparkLife:4.2,\n'
           f'         tip:"{TIP}" }},')

DMG_OLD = ('blades:[0], reach:116, width:14, artW:40, dmg:8.88, spin:3.4, '
           'mode:"swing", arc:1.5, mass:3.0,')
DMG_NEW = (f'blades:[0], reach:116, width:14, artW:40, dmg:{TUNED_DB}, spin:3.4, '
           'mode:"swing", arc:1.5, mass:3.0,')

BLURB_OLD = ('blurb:"A greatsword that tracks its foe instead of spinning '
             'blind, and drinks the wound it opens." },')
BLURB_NEW = ('blurb:"A greatsword that tracks its foe instead of spinning '
             'blind, and scatters daybreak where it lands." },')

STATUS_OLD = """  sunder:     { name:"Sunder",     maxStacks:6, dur:5.0, taken:0.11,
                tip:"Increases damage taken by 11% per stack" },"""
STATUS_NEW = STATUS_OLD + """
  /* Earned, never granted: only collecting a Daybreak spark applies it. The
     heal path in tickStatus predates this entry — `hps` heals per stack per
     second, clocked and capped like everything else here. */
  blessing:   { name:"Blessing",   maxStacks:5, dur:6.0, hps:1.2,
                tip:"Heals 1.2 hp per second per stack" },"""

FINIT_OLD = "this.ultForge = null;     // {t, minT, cap} while the Crucible is lit"
FINIT_NEW = FINIT_OLD + """
    this.ultRadiant = null;   // {t, dur} while Daybreak burns"""

MINIT_OLD = "this.wallCrack = null;    // presentation only: where it shattered"
MINIT_NEW = MINIT_OLD + """
    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed"""

RADIANT_TICK_ANCHOR = """    if (f.ultForge){
      /* The Crucible is lit."""
RADIANT_TICK = """    if (f.ultRadiant){
      /* Daybreak burns down. Unlike the forge there is no return and no
         charge gate: the window IS the payoff, and the next ult is owed
         from the cast like any other. */
      f.ultRadiant.t += dt;
      if (f.ultRadiant.t >= f.ultRadiant.dur) f.ultRadiant = null;
    }
"""

FIRE_ANCHOR = "    /* THE CRUCIBLE DOES NOT RESOLVE HERE."
FIRE_RADIANT = """    /* DAYBREAK RESOLVES NOTHING HERE EITHER — and unlike every ultimate
       before it, it never will: no damage, no heal, no status on the cast.
       The old Judgement was a 34-hp subsidy measured at +9 to +32pp in every
       matchup, paid for with the weakest blade in the class. This is that
       budget, moved onto the FIGHT: for `dur` seconds every landed hit
       sprays sparks, and what the sparks do depends on who touches them. */
    if (u.kind === "radiant"){
      f.ultRadiant = { t: 0, dur: u.dur || 5.0 };
      this.ultFx = { w: f.w.id, kind: "radiant",
                     src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                     x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: true,
                     radius: 300, aff: f.aff, t: 0, life: (u.dur || 5.0) + 0.3 };
      return;
    }

"""

ONTARGET_OLD = ('const onTarget = { dawnbringer:1, thornwake:1, spellbreaker:1 '
                '}[f.w.id];')
ONTARGET_NEW = ("""/* Dawnbringer left this map with Judgement: the pillar fell on the
       quarry, but Daybreak ignites on the CASTER, so its name goes there. */
    const onTarget = { thornwake:1, spellbreaker:1 }[f.w.id];""")

SPARK_SPAWN_ANCHOR = ("    this.shake = Math.min(38, this.shake + (crit ? 24 : 10)"
                      " * (self.w.knockMul || 1));")
SPARK_SPAWN = """    /* DAYBREAK: a landed blow while the radiance burns throws sparks off
       the point of impact. Spawned HERE and only here, so no match without
       a radiant ultimate ever draws differently from the rng. */
    if (mul === undefined && self.ultRadiant && self.w.ult.sparks)
      for (let i = 0; i < self.w.ult.sparks; i++) this.spawnSpark(self, hx, hy);

"""

BALLCOL_OLD = "  ballCollision(){"
BALLCOL_NEW = """  /* ------------------------------------------------------ Daybreak sparks ---
     Simulation objects, not fx: they deal damage and they heal, so they live
     in the tick and are capped like shots. Drift is DETERMINISTIC — a phase
     rolled at spawn against the match clock, no per-frame rng — so a paused
     and resumed render replays identically. */
  spawnSpark(f, x, y){
    if (this.sparks.length >= 48) this.sparks.shift();
    const a = this.rng() * TAU;
    /* born FAST — they scatter clear of the scrum before settling into
       drift, or the foe standing at the impact eats the whole batch and the
       "drift around the arena" Rick asked for never exists. Measured: at
       spawn speed 60-180 the ball sat at 68-76% winrate on splash alone. */
    const sp = 220 + this.rng() * 140;
    this.sparks.push({ own: f === this.a ? "a" : "b", x, y,
                       vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 30,
                       ph: this.rng() * TAU,
                       life: f.w.ult.sparkLife || 7.0 });
  }

  tickSparks(dt){
    if (!this.sparks.length) return;
    const R = CONFIG.physics.ballR, A = CONFIG.arena;
    const lo = this.inset + 8, hiX = A.w - this.inset - 8, hiY = A.h - this.inset - 8;
    for (let i = this.sparks.length - 1; i >= 0; i--){
      const s = this.sparks[i];
      s.life -= dt;
      if (s.life <= 0){ this.sparks.splice(i, 1); continue; }
      /* the drift: damped, faintly buoyant, wandering on its own phase */
      s.vx += Math.cos(s.ph + this.t * 2.2) * 30 * dt;
      s.vy += (Math.sin(s.ph * 1.7 + this.t * 1.9) * 30 - 9) * dt;
      const damp = 1 - Math.min(1, (s.life > 3.2 ? 1.4 : 0.35) * dt);
      s.vx *= damp; s.vy *= damp;
      s.x += s.vx * dt; s.y += s.vy * dt;
      if (s.x < lo){ s.x = lo; s.vx = Math.abs(s.vx); }
      if (s.x > hiX){ s.x = hiX; s.vx = -Math.abs(s.vx); }
      if (s.y < lo){ s.y = lo; s.vy = Math.abs(s.vy); }
      if (s.y > hiY){ s.y = hiY; s.vy = -Math.abs(s.vy); }

      /* first ball to touch it takes it — owner first, deterministically */
      let taken = false;
      for (const key of ["a", "b"]){
        const f = this[key];
        if (!f.alive) continue;
        if (Math.hypot(f.x - s.x, f.y - s.y) > R + 10) continue;
        const owner = this[s.own];
        if (key === s.own){
          /* collected: the light banked as Blessing */
          f.apply("blessing", 1);
          const first = !this.taught.blessing && !!STATUS.blessing.tip;
          if (first) this.taught.blessing = true;
          this.statusTag(f.x, f.y, "blessing", first);
          f.mend = Math.max(f.mend || 0, 0.8);
          this.spawnFx(s.x, s.y, "#FFF6E2", 5, 120, 0.35, 3);
          SFX.play("spark", { collect: true, n: f.stacks("blessing") });
        } else {
          /* burned: the light spent as harm, and a shove — the cloud is a
             soft wall, and this is the wall pushing */
          const dmg = Math.round(this.actMods.dmg *
                                 (owner.w.ult.sparkDmg || 8) * f.dmgTakenMul());
          this.hurt(f, dmg, owner);
          owner.dealt += dmg;
          const dl = Math.hypot(f.x - s.x, f.y - s.y) || 1;
          const kn = owner.w.ult.sparkKnock || 260;
          f.vx += ((f.x - s.x) / dl) * kn; f.vy += ((f.y - s.y) / dl) * kn;
          f.flash = Math.max(f.flash, 0.5);
          this.float(s.x, s.y - 18, dmg, "#FFF6E2", 24);
          this.spawnFx(s.x, s.y, "#FFD98A", 8, 200, 0.4, 3.5);
          SFX.play("spark", { collect: false });
        }
        taken = true;
        break;
      }
      if (taken) this.sparks.splice(i, 1);
    }
  }

  ballCollision(){"""

STEP_OLD = """    this.tickClank(dt);
    this.tickShots(dt);"""
STEP_NEW = """    this.tickClank(dt);
    this.tickShots(dt);
    this.tickSparks(dt);"""

DRAW_OLD = """    this.drawShots(m);
    this.drawUltName(m);"""
DRAW_NEW = """    this.drawShots(m);
    this.drawSparks(m);
    this.drawUltName(m);"""

ULTNAME_OLD = "  drawUltName(m){"
ULTNAME_NEW = """  /* Daybreak's drift. Each spark is a MODEL, not a dot — Rick: "i cant see
     the sparks. they need their own models/animation." A four-point sun
     shard: two crossed rhombi turning on the spark's own phase, a white
     core, two flame licks cycling upward, a birth streak while it is still
     flying fast, and a gutter at the end of its life. 48 at most; every
     stroke is small and nothing blurs. */
  _sparkStar(c, r, squash){
    c.beginPath();
    c.moveTo(0, -r);
    c.quadraticCurveTo(r * squash, -r * squash, r, 0);
    c.quadraticCurveTo(r * squash, r * squash, 0, r);
    c.quadraticCurveTo(-r * squash, r * squash, -r, 0);
    c.quadraticCurveTo(-r * squash, -r * squash, 0, -r);
    c.closePath();
  }

  drawSparks(m){
    if (!m.sparks || !m.sparks.length) return;
    const c = this.ctx;
    c.save();
    c.globalCompositeOperation = "lighter";
    for (const s of m.sparks){
      const born = clamp((s.life > 3.2 ? 4.2 - s.life : 1) / 0.35, 0, 1);
      const dying = clamp(s.life / 0.7, 0, 1);
      const pulse = 0.82 + 0.18 * Math.sin(m.t * 10 + s.ph * 3);
      const R = (10 + 4 * Math.sin(s.ph)) * (0.55 + 0.45 * born) * (0.5 + 0.5 * dying);
      const a = born * dying;
      /* birth streak: while it still moves fast it IS its own motion */
      const sp = Math.hypot(s.vx, s.vy);
      if (sp > 90){
        const k2 = Math.min(1, sp / 300);
        c.globalAlpha = a * 0.55 * k2;
        c.strokeStyle = "#FFD98A"; c.lineWidth = 3.4;
        c.lineCap = "round";
        c.beginPath();
        c.moveTo(s.x - (s.vx / sp) * 26 * k2, s.y - (s.vy / sp) * 26 * k2);
        c.lineTo(s.x, s.y);
        c.stroke();
      }
      /* halo */
      const g = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, R * 2.4);
      g.addColorStop(0, "#FFF6E2AA"); g.addColorStop(1, "#FFD98A00");
      c.globalAlpha = a * 0.8 * pulse;
      c.fillStyle = g;
      c.beginPath(); c.arc(s.x, s.y, R * 2.4, 0, TAU); c.fill();
      /* the shard: two crossed rhombi, turning */
      c.save();
      c.translate(s.x, s.y);
      c.rotate(s.ph + m.t * (0.9 + 0.4 * Math.sin(s.ph * 2)));
      c.globalAlpha = a * pulse;
      c.fillStyle = "#FFF6E2";
      this._sparkStar(c, R, 0.22); c.fill();
      c.rotate(Math.PI / 4);
      c.globalAlpha = a * pulse * 0.7;
      c.fillStyle = "#FFD98A";
      this._sparkStar(c, R * 0.62, 0.26); c.fill();
      c.restore();
      /* flame licks: two small tongues, cycling upward off the shard */
      for (let i = 0; i < 2; i++){
        const lp = (m.t * (1.3 + 0.3 * i) + s.ph * (1 + i)) % 1;
        const lx = s.x + Math.sin(s.ph * 4 + i * 2.6) * R * 0.5;
        c.globalAlpha = a * (1 - lp) * 0.7;
        c.strokeStyle = i ? "#FFD98A" : "#FFFFFF";
        c.lineWidth = 2.2 - i * 0.8;
        c.lineCap = "round";
        c.beginPath();
        c.moveTo(lx, s.y - R * 0.4 - lp * 3);
        c.quadraticCurveTo(lx + Math.sin(lp * 9 + s.ph) * 3.5, s.y - R - lp * 9,
                           lx + Math.sin(lp * 7 + s.ph) * 2, s.y - R * 0.7 - lp * 16);
        c.stroke();
      }
      /* the core */
      c.globalAlpha = a;
      c.fillStyle = "#FFFFFF";
      c.beginPath(); c.arc(s.x, s.y, Math.max(1.6, R * 0.28), 0, TAU); c.fill();
    }
    c.restore();
  }

  drawUltName(m){"""

SFX_ANCHOR = '      else if (kind === "wall"){'
SFX_SPARK = """      else if (kind === "spark"){
        /* frequent by design, so quiet by design: the collect chime climbs
           with the stack it just banked, the burn is a short sizzle */
        if (p && p.collect){
          this._tone (t, { freq: 1180 + (p.n || 0) * 110, gain: 0.05, dur: 0.20, type:"triangle" });
        } else {
          this._burst(t, { freq: 4200, q: 1.4, gain: 0.07, dur: 0.06, type:"highpass" });
          this._tone (t, { freq: 520, to: 180, gain: 0.05, dur: 0.10, type:"sine" });
        }
      }
"""

# ------------------------------------------------------ the set-piece art ----

UNDER_MARK = ('    if (u.w === "dawnbringer"){\n'
              '      /* the mark the light is about to fall on */')
UNDER_NEW = '''    if (u.w === "dawnbringer"){
      /* Daybreak on the floor: a breathing pool of dawn under the LIVE
         caster — this piece runs five seconds and the caster keeps moving.
         The old target rings left with Judgement; nothing falls anymore. */
      const rise = clamp(u.t / 0.35, 0, 1);
      const fade = 1 - clamp((u.t - (u.life - 0.5)) / 0.5, 0, 1);
      const pulse = 0.88 + 0.12 * Math.sin(u.t * 7);
      const g = c.createRadialGradient(src.x, src.y, 5, src.x, src.y, 105 * pulse);
      g.addColorStop(0, "#FFF6E255"); g.addColorStop(1, "#FFF6E200");
      c.globalAlpha = 0.8 * rise * fade;
      c.fillStyle = g;
      c.beginPath(); c.arc(src.x, src.y, 105 * pulse, 0, TAU); c.fill();
    }'''

OVER_MARK = ('    /* ---- Judgement: a pillar of light falls, and the caster is '
             'made whole */\n    if (u.w === "dawnbringer"){')
OVER_NEW = '''    /* ---- Daybreak: white heat radiating off the whole relic ------------- */
    if (u.w === "dawnbringer"){
      const R = CONFIG.physics.ballR;
      const rise = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - (u.life - 0.5)) / 0.5, 0, 1);
      const k2 = rise * fade;
      /* THE CORONA IS A RING, NOT A DISC, AND THE HOLE IS THE POINT.
       *
       * It was a disc from stop 0 = #FFFFFF at the centre, drawn with
       * `lighter` straight over a relic body already sitting at 0.892 luma.
       * The ball was not lit by Daybreak, it was ERASED by it: measured on
       * the caster's disc, 0.499 bare -> 0.905 at the peak with 58% of the
       * disc past 0.98, and only +0.041 of that came from the bloom. Rick
       * watched it and said the white balls were washed out; the bloom got
       * the blame and the bloom was a bystander.
       *
       * The gradient's own numbers are UNCHANGED -- same stops, same reach,
       * same alpha -- so the light around the ball is exactly as bright as it
       * was. All that changed is that nothing is painted over the body.
       *
       * THE HOLE HAS TO BE CUT IN THE PATH. A radial gradient with an inner
       * radius still fills its inner circle with colorStop(0), so moving the
       * inner radius out to R alone would have left the white centre exactly
       * where it was and looked like the fix had done nothing. The second arc
       * is wound backwards to subtract it. */
      c.globalCompositeOperation = "lighter";
      const pulse = 0.92 + 0.08 * Math.sin(u.t * 13);
      const g = c.createRadialGradient(src.x, src.y, R * 0.94, src.x, src.y, R * 2.3 * pulse);
      g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.4, "#FFF6E288");
      g.addColorStop(1, "#FFD98A00");
      c.globalAlpha = 0.8 * k2;
      c.fillStyle = g;
      c.beginPath(); c.arc(src.x, src.y, R * 2.3 * pulse, 0, TAU);
      c.arc(src.x, src.y, R * 0.94, TAU, 0, true); c.fill();
      /* flame tongues: deterministic flicker, licking upward off the shell */
      for (let i = 0; i < 9; i++){
        const a0 = (i / 9) * TAU + Math.sin(u.t * (2.1 + shellHash(19, i)) + i) * 0.25;
        const flick = 0.55 + 0.45 * Math.sin(u.t * (9 + shellHash(29, i) * 5) + i * 2.1);
        const len = (R * 0.9 + shellHash(39, i) * R * 0.8) * flick;
        const bx = src.x + Math.cos(a0) * (R + 2), by = src.y + Math.sin(a0) * (R + 2);
        const tx2 = src.x + Math.cos(a0) * (R + 2 + len * 0.4) - 0 ;
        const ty2 = by - len;                       // heat goes UP
        c.globalAlpha = k2 * 0.55 * flick;
        c.strokeStyle = i % 3 ? "#FFF6E2" : "#FFFFFF";
        c.lineWidth = 3.2 - (i % 3);
        c.beginPath();
        c.moveTo(bx, by);
        c.quadraticCurveTo(bx + Math.cos(a0) * len * 0.3, by - len * 0.5, tx2, ty2);
        c.stroke();
      }
      /* the ignition ring, once, at the cast */
      const ring = clamp(u.t / 0.4, 0, 1);
      if (ring < 1){
        c.globalAlpha = (1 - ring) * 0.9;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 4 * (1 - ring * 0.5);
        c.shadowColor = "#FFFFFF"; c.shadowBlur = 16;
        c.beginPath(); c.arc(src.x, src.y, R + 130 * ring, 0, TAU); c.stroke();
        c.shadowBlur = 0;
      }
      c.globalCompositeOperation = "source-over";
    }'''

EDITS = [
    ("ult data (Daybreak)",       ULT_OLD,       ULT_NEW),
    ("blade damage, repaid",      DMG_OLD,       DMG_NEW),
    ("blurb",                     BLURB_OLD,     BLURB_NEW),
    ("STATUS.blessing",           STATUS_OLD,    STATUS_NEW),
    ("fighter init",              FINIT_OLD,     FINIT_NEW),
    ("match init sparks",         MINIT_OLD,     MINIT_NEW),
    ("radiant window tick",       RADIANT_TICK_ANCHOR, RADIANT_TICK + RADIANT_TICK_ANCHOR),
    ("fireUlt radiant branch",    FIRE_ANCHOR,   FIRE_RADIANT + FIRE_ANCHOR),
    ("banner anchor map",         ONTARGET_OLD,  ONTARGET_NEW),
    ("resolveHit spark spawn",    SPARK_SPAWN_ANCHOR, SPARK_SPAWN + SPARK_SPAWN_ANCHOR),
    ("spark sim (spawn/tick)",    BALLCOL_OLD,   BALLCOL_NEW),
    ("step tickSparks",           STEP_OLD,      STEP_NEW),
    ("render drawSparks",         DRAW_OLD,      DRAW_NEW),
    ("drawSparks method",         ULTNAME_OLD,   ULTNAME_NEW),
    ("spark SFX",                 SFX_ANCHOR,    SFX_SPARK + SFX_ANCHOR),
]


def replace_block(s: str, marker: str, new_block: str, name: str) -> str:
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
  const mk = (seed) => { const m = new AC.Match("dawnbringer", "heartwood", seed);
                         m.introT = 0; return m; };
  const db = AC.WEAPONS.find(w => w.id === "dawnbringer");

  out.data = { noCastDmg: db.ult.dmg === undefined, noCastHeal: db.ult.heal === undefined,
               kind: db.ult.kind, blessing: !!AC.STATUS.blessing };

  { // A: cast -> radiant state, banner at the CASTER, charge not gated
    const m = mk(101);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultRadiant && g++ < 600) m.step(dt);
    const lit = !!m.a.ultRadiant && m.ultFx && m.ultFx.kind === "radiant";
    const banner = m.banner ? m.banner.text : null;
    const nearCaster = m.banner &&
      Math.hypot(m.banner.bx - m.ultFx.x, m.banner.by - m.ultFx.y) < 1;
    const c0 = m.a.charge;
    for (let i = 0; i < 60; i++) m.step(dt);
    out.A = { lit, banner, nearCaster, chargeRuns: m.a.charge > c0,
              stillLit: !!m.a.ultRadiant };
  }

  { // B: hits during the window spray sparks; window ends at dur
    const m = mk(202);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.charge = m.a.w.ult.charge - 0.01;
    let g = 0; while (!m.a.ultRadiant && g++ < 600) m.step(dt);
    const hits0 = m.a.hits;
    let peak = 0;
    g = 0; while (m.a.ultRadiant && g++ < 900){ m.step(dt);
      peak = Math.max(peak, m.sparks.length); }
    out.B = { hitsInWindow: m.a.hits - hits0, peakSparks: peak,
              ended: !m.a.ultRadiant };
  }

  { // C: a foe touching a spark burns and is shoved; owner collecting banks
    // Blessing and heals over time; stacks cap at 5
    const m = mk(303);
    m.a.hp = m.a.maxHp = 4000; m.b.hp = m.b.maxHp = 4000;
    m.a.x = 200; m.a.y = 400; m.b.x = 800; m.b.y = 1200;
    m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
    m.sparks.push({ own: "a", x: m.b.x + 20, y: m.b.y, vx: 0, vy: 0,
                    ph: 1, life: 5 });
    const bhp0 = m.b.hp, bvx0 = m.b.vx;
    m.step(dt);
    const burned = bhp0 - m.b.hp, shoved = Math.abs(m.b.vx - bvx0) > 100;
    // collection: park sparks on the caster
    m.a.hp = 3800;
    for (let i = 0; i < 7; i++)
      m.sparks.push({ own: "a", x: m.a.x + 10, y: m.a.y, vx: 0, vy: 0,
                      ph: i, life: 5 });
    for (let i = 0; i < 8; i++) m.step(dt);
    const stacks = m.a.stacks("blessing");
    const hp1 = m.a.hp;
    for (let i = 0; i < 240; i++) m.step(dt);   // 2s of Blessing
    out.C = { burned, shoved, sparkGone: m.sparks.length < 8,
              stacks, healed: +(m.a.hp - hp1).toFixed(1) };
  }

  { // D: spark cap holds
    const m = mk(404);
    for (let i = 0; i < 60; i++) m.spawnSpark(m.a, 500, 500);
    out.D = { cap: m.sparks.length };
  }

  { // E: determinism
    const r1 = AC.simulate("dawnbringer", "heartwood", 999);
    const r2 = AC.simulate("dawnbringer", "heartwood", 999);
    out.E = { same: JSON.stringify(r1) === JSON.stringify(r2) };
  }
  return out;
}
"""

ART_JS = r"""
() => {
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){};
  const m = new AC.Match("dawnbringer", "heartwood", 4242);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.34; m.a.y = A.h * 0.42;
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
  for (const t of [0.1, 1.2, 2.6, 4.2, 5.1]){
    m.ultFx = { w: "dawnbringer", kind: "radiant", src: "a", tgt: "b",
                x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y, hit: true,
                radius: 300, aff: m.a.aff, t, life: 5.3 };
    let threw = null, px = 0;
    try { const a = grab(); m.ultFx = null; const b = grab(); px = diff(a, b); }
    catch (e) { threw = String(e); }
    out.push({ what: "radiant", t, px, threw });
  }
  m.ultFx = null;
  for (let i = 0; i < 12; i++)
    m.sparks.push({ own: "a", x: 200 + i * 55, y: 700 + (i % 4) * 90,
                    vx: 0, vy: 0, ph: i, life: 4 });
  { const a = grab(); m.sparks = []; const b = grab();
    out.push({ what: "sparks", t: 0, px: diff(a, b), threw: null }); }
  return out;
}
"""

REGRESS_JS = r"""
(ids) => {
  const out = [];
  for (const id of ids){
    const w = AC.WEAPONS.find(x => x.id === id);
    const foe = id === "heartwood" ? "axiom" : "heartwood";
    const m = new AC.Match(id, foe, 0x9A11 + 7);
    AC.setResolution(1080, 1920);
    const f = m.a, fo = m.b;
    let threw = null, peak = 0;
    const phases = id === "grudgebearer" ? ["wind", "strike"] : [null];
    for (const ph of phases){
      for (const t of [0.05, 0.25, 0.5, 0.9, 1.3]){
        m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
                    x: f.x, y: f.y, tx: fo.x, ty: fo.y, hit: true, stacks: 4,
                    radius: w.ult.radius || 300, aff: f.aff, t: t, life: 2.2,
                    shots: w.ult.shots || 0 };
        if (ph) m.ultFx.phase = ph;
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
    }
    out.push({ id, threw, peak });
  }
  return out;
}
"""

OTHERS = ["widowmaker", "grudgebearer", "thornwake", "gravemourn", "spellbreaker",
          "oathwound", "heartwood", "nightfell", "axiom", "ironhail",
          "lightkeeper", "farwarden", "aureole", "censer", "emberedge"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-crucible.html")
    ap.add_argument("--out", default="sc-daybreak.html")
    ap.add_argument("--no-check", action="store_true")
    A = ap.parse_args()

    if pathlib.Path(A.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    if len(TIP) > 72:
        print(f"! ult tip is {len(TIP)} chars, cap 72", file=sys.stderr); return 1
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
        print(f"  [ultdawn] {name}")

    s = replace_block(s, OVER_MARK, OVER_NEW, "drawUltOver dawnbringer")
    print("  [ultdawn] drawUltOver: Judgement pillar -> Daybreak corona")
    s = replace_block(s, UNDER_MARK, UNDER_NEW, "drawUltUnder dawnbringer")
    print("  [ultdawn] drawUltUnder: target rings -> dawn pool")

    doc = "<!DOCTYPE html>\n"
    i = s.find(doc)
    if i < 0:
        print("! no doctype", file=sys.stderr); return 4
    stamp = (f"<!-- GENERATED by ultdawn_build.py --src {A.src} — "
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
    with game(game_path=out.resolve()) as (page, errors):
        art = page.evaluate(ART_JS)
        mech = page.evaluate(MECH_JS)
        reg = page.evaluate(REGRESS_JS, OTHERS)
        if errors:
            print(f"! page errors: {errors[:4]}", file=sys.stderr)
            out.unlink(); return 5

    print("\n  ART — pixel diff per sample (fail < 200):")
    for r in art:
        ok = r["px"] >= 200 and not r["threw"]
        if r["threw"]: bad.append(f"art {r['what']} t={r['t']}: threw {r['threw'][:70]}")
        elif r["px"] < 200: bad.append(f"art {r['what']} t={r['t']}: {r['px']} px")
        print(f"    {r['what']:<9} t={r['t']:<5} {r['px']:>7}{'' if ok else '  <-- FAIL'}")

    print("\n  MECH:")
    print("   ", json.dumps(mech, indent=2).replace("\n", "\n    "))
    m = mech
    checks = [
        ("data: no cast dmg/heal, radiant, blessing exists",
         m["data"]["noCastDmg"] and m["data"]["noCastHeal"] and
         m["data"]["kind"] == "radiant" and m["data"]["blessing"]),
        ("A lit + banner Daybreak at caster",
         m["A"]["lit"] and m["A"]["banner"] == "Daybreak" and m["A"]["nearCaster"]),
        ("A charge not gated by the window", bool(m["A"]["chargeRuns"])),
        ("A still lit after 0.5s", bool(m["A"]["stillLit"])),
        ("B hits spray sparks", m["B"]["hitsInWindow"] > 0 and m["B"]["peakSparks"] > 0),
        ("B window ends", bool(m["B"]["ended"])),
        ("C foe burned ~8 and shoved",
         m["C"]["burned"] >= 6 and m["C"]["burned"] <= 14 and m["C"]["shoved"]
         and m["C"]["sparkGone"]),
        ("C blessing capped at 5", m["C"]["stacks"] == 5),
        ("C heals over time", m["C"]["healed"] > 6),
        ("D spark cap 48", m["D"]["cap"] == 48),
        ("E deterministic", bool(m["E"]["same"])),
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
        print("  ULTDAWN CHECK FAILED:")
        for b in bad: print("   ", b)
        out.unlink(); print(f"\n  {A.out} deleted.")
        return 6
    print("  ultdawn check PASS — Daybreak ignites, sprays, burns, feeds, and ends;")
    print("  the other fifteen untouched. Run engine_ab.py for the bit-identity proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
