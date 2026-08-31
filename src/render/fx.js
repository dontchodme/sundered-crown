/* THE EFFECTS RUNTIME — deterministic particle fields for the ultimates.
 *
 * docs/FX-RUNTIME-BRIEF.md §3.2. Loaded by the app and INLINED into the build
 * by tools/fx_build.py, byte for byte, so the app and the mp4 run the same
 * one. If those two ever differ, docs/ARCHITECTURE.md §1's guarantee is gone
 * and gone quietly.
 *
 * NO IMPORTS, NO DEPENDENCIES, ONE FILE. Same rule as src/render/post.js and
 * for the same reason: the build is one self-contained HTML file with no
 * <script src>, and that rule is why all 211 tools still work.
 *
 * ── WHAT THIS IS NOT ────────────────────────────────────────────────────
 *
 * §3.2 asked for a GPU system: state in a texture, ping-pong integrated,
 * thousands of instances sharing post.js's context. It is not that, and the
 * measurement is why. On the real hardware at the app's 453x805, 420 Canvas 2D
 * particles cost 1.64 ms against 4.77 ms of headroom and 900 cost 4.28
 * (tools/ult_particle_lab.py --cost). The "about a dozen sprites per frame"
 * figure that premise rested on was really about `shadowBlur`: the existing
 * art's sprites each drag a full-canvas shadow and these carry none.
 *
 * A GPU runtime buys headroom nobody currently needs and costs a session. If a
 * spec ever wants tens of thousands of particles, that is when it earns its
 * keep -- and this file's shape (spawn as data, integrate on a fixed dt, draw
 * in one pass) is the same shape that port would take.
 *
 * ── DETERMINISM, AND IT IS THE WHOLE GAME (brief §6) ────────────────────
 *
 * `(build, relics, seed)` names a fight, render_ab.py hashes frames, and
 * cinema_clip must rebuild a clip from its seed. So:
 *
 *   1. NO Math.random, ANYWHERE. Randomness is mulberry32 -- the same
 *      generator the sim's seed uses -- keyed on the cast, never the global.
 *   2. THE FIELD IS AGED OFF SIM TIME, NOT FRAME TIME. `stepTo(t)` integrates
 *      from wherever it is to `ultFx.t`, in fixed dt chunks. A field advanced
 *      by wall-clock frame time is a clip that cannot be rebuilt, and it would
 *      also differ between the app's rAF and the capture's fixed cadence.
 *   3. AND THAT MAKES IT IDEMPOTENT, which is load-bearing. The post chain
 *      draws every frame TWICE -- readouts pass, then world pass -- so any
 *      hook inside drawUltOver runs twice per composited frame. Stepping BY a
 *      delta would double-step; stepping TO an absolute time is a no-op the
 *      second time. post_build.py had to fix exactly this for the camera
 *      shake after it read as juddering physics; this file cannot have that
 *      bug by construction.
 *
 * The cast seed is built from sim state only -- the fight's seed, the relic,
 * the caster, and the cast position quantised -- so it is identical in the app
 * and in the capture, and it still varies between two casts of the same ult in
 * one fight.
 */
(function (root) {
  'use strict';

  var VERSION = 'fx-1';

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* A cheap string hash, so a relic id can contribute to a seed without a
     lookup table that would have to be kept in step with the roster. */
  function hashStr(s) {
    var h = 2166136261, i;
    for (i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  /* THE SPECS. Twenty-five set-pieces as data against six emitter modes and
   * one implementation -- which is the claim docs/FX-RUNTIME-BRIEF.md §4
   * makes about why this moves the roster ceiling, demonstrated rather than
   * argued. Rick approved the density on 2026-08-28 ("dont push it further
   * than this") after four relics and then the whole roster.
   *
   *   mode   burst | beam | field | swirl | fall | implode
   *   n      particles at full density
   *   sp     [min, max] initial speed, arena units/s, sampled squared so most
   *          are slow and a few carry -- a uniform speed reads as a shell
   *   grav   arena units/s^2. NEGATIVE RISES, and it is most of what separates
   *          an explosion from a nova from a beam
   *   drag   exponential velocity decay per second
   *   life   [min, max] seconds per particle
   *   heavy  fraction that are tumbling debris rather than motes
   *   size   [min, max] radius in arena units
   *   spawn  seconds over which the field emits; 0 means all at once
   *   up     initial upward bias on a burst
   *
   * COLOURS ARE DELIBERATELY ABSENT. Every field reads the relic's own
   * affinity at draw time, because a per-relic palette is exactly the kind of
   * tuned number CLAUDE.md §4.9 says not to strand -- and the schools already
   * own their colour. */
  var SPECS = {
    /* ---- BURSTS: something is thrown outward from a point ------------- */
    /* THE EXPLOSION. Hard radial, heavy gravity, tumbling debris. */
    emberedge: { mode: 'burst', n: 1890, sp: [90, 710], grav: 520, drag: 1.9,
                 life: [0.40, 1.05], heavy: 0.14, size: [0.9, 2.8],
                 spawn: 0.0, up: 40 },
    /* AN ANVIL. The forge strike is the only other one that throws real
       debris -- it is metalwork, so it carries the highest heavy fraction. */
    grudgebearer: { mode: 'burst', n: 1500, sp: [140, 660], grav: 620,
                    drag: 2.0, life: [0.35, 0.95], heavy: 0.22,
                    size: [0.9, 2.6], spawn: 0.06, up: 60 },
    /* A LATCH THAT LETS GO. Ironbloom blooms outward off the foe. */
    slagheart: { mode: 'burst', n: 1450, sp: [120, 520], grav: 440, drag: 2.1,
                 life: [0.45, 1.20], heavy: 0.12, size: [0.9, 2.6],
                 spawn: 0.10, up: 30 },
    /* THREE AT ONCE. Triplicate splits, so the field is wide and thin. */
    twinshade: { mode: 'burst', n: 1350, sp: [200, 640], grav: 180, drag: 2.4,
                 life: [0.30, 0.80], heavy: 0.04, size: [0.8, 2.2],
                 spawn: 0.12, up: 0 },

    /* ---- NOVAS: a burst that does NOT fall --------------------------- */
    widowmaker: { mode: 'burst', n: 1620, sp: [240, 620], grav: 90, drag: 2.6,
                  life: [0.30, 0.75], heavy: 0.05, size: [0.8, 2.2],
                  spawn: 0.05, up: 0 },
    lightkeeper: { mode: 'burst', n: 1500, sp: [210, 560], grav: 70,
                   drag: 2.5, life: [0.35, 0.85], heavy: 0.03,
                   size: [0.8, 2.2], spawn: 0.05, up: 0 },
    censer: { mode: 'burst', n: 1500, sp: [180, 540], grav: 40, drag: 2.2,
              life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
              spawn: 0.08, up: 20 },
    /* DEADFALL DISCHARGES, AND `atSelf` IS A FLAG NO OTHER SPEC CARRIES.
       A `burst` is drawn at the FOE -- right for the four novas above it,
       which are cast AT somebody, and wrong for a window that opens on its
       own caster. Eclipse was a nova and this entry was its dark, slow one;
       DEADFALL resolves nothing at the cast, so 1400 particles over the
       quarry would say the ultimate landed on them while nothing landed on
       anyone. It is now SPARKS COMING OFF THE BALL: fast out, almost no
       gravity, heavy drag and a short life, so they leave rather than fall,
       and they are gone before the first figure has finished arming. */
    nightfell: { mode: 'burst', n: 1100, sp: [200, 700], grav: 40, drag: 3.2,
                 life: [0.22, 0.60], heavy: 0.0, size: [0.6, 1.8],
                 spawn: 0.10, up: 0, atSelf: 1 },
    /* DAYBREAK RISES, IT DOES NOT DETONATE, and it stays sparse in the middle
       ON PURPOSE. CLAUDE.md §4.1b is the record of this relic's art blowing
       out over a body already at 0.892 luma -- "the ball was not lit, it was
       erased". Piling embers onto that centre would recreate exactly the
       fault that section exists to prevent. */
    dawnbringer: { mode: 'burst', n: 1350, sp: [120, 470], grav: -90,
                   drag: 1.8, life: [0.45, 1.15], heavy: 0.0,
                   size: [0.7, 2.1], spawn: 0.10, up: 110 },

    /* ---- BEAMS AND BOLTS: it travels, so it sheds along its length ---- */
    /* Negative gravity is what stops a beam reading as an explosion pointed
       sideways. */
    aureole: { mode: 'beam', n: 1350, sp: [20, 120], grav: -120, drag: 1.2,
               life: [0.45, 1.10], heavy: 0.0, size: [0.7, 2.0],
               spawn: 0.55, up: 0 },
    oathwound: { mode: 'beam', n: 1250, sp: [25, 140], grav: -60, drag: 1.3,
                 life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
                 spawn: 0.50, up: 0 },
    spellbreaker: { mode: 'beam', n: 1200, sp: [40, 200], grav: -40,
                    drag: 1.6, life: [0.25, 0.70], heavy: 0.0,
                    size: [0.6, 1.8], spawn: 0.35, up: 0 },
    axiom: { mode: 'beam', n: 1200, sp: [40, 190], grav: -40, drag: 1.6,
             life: [0.28, 0.72], heavy: 0.0, size: [0.6, 1.8],
             spawn: 0.35, up: 0 },
    /* A VOLLEY IS MANY SHOTS, so it emits across nearly its whole life. */
    ironhail: { mode: 'beam', n: 1300, sp: [50, 240], grav: 140, drag: 1.4,
                life: [0.22, 0.65], heavy: 0.03, size: [0.6, 1.7],
                spawn: 0.80, up: 0 },
    /* ONE AIMED SHOT: sparse and late. An aimedshot holds a DRAW until the
       bow's facing comes round, so almost everything arrives at once. */
    farwarden: { mode: 'beam', n: 900, sp: [60, 260], grav: 120, drag: 1.5,
                 life: [0.20, 0.60], heavy: 0.02, size: [0.6, 1.8],
                 spawn: 0.25, up: 0 },
    marrowdraw: { mode: 'beam', n: 1100, sp: [45, 220], grav: 150, drag: 1.5,
                  life: [0.25, 0.70], heavy: 0.04, size: [0.7, 1.9],
                  spawn: 0.40, up: 0 },

    /* ---- FIELDS: nothing is thrown, the air fills -------------------- */
    lastlight: { mode: 'field', n: 1530, sp: [8, 55], grav: -30, drag: 0.8,
                 life: [0.60, 1.40], heavy: 0.0, size: [0.6, 1.8],
                 spawn: 0.75, up: 0 },
    /* RETRACE IS THE TELEGRAPH. §4.1d measured it as the largest light source
       in the game -- 565,816 emissive px -- and concluded it is bright ON
       PURPOSE, because an ultimate nothing can interrupt has to be legible
       before it lands. So: wide, slow, and no second bright core. */
    foregone: { mode: 'field', n: 1400, sp: [6, 40], grav: -16, drag: 0.7,
                life: [0.70, 1.60], heavy: 0.0, size: [0.6, 1.7],
                spawn: 0.80, up: 0 },
    /* STASIS. Nearly still by definition -- the one field whose motes should
       look STOPPED rather than drifting. */
    paradox: { mode: 'field', n: 1300, sp: [2, 18], grav: -4, drag: 0.4,
               life: [0.90, 2.00], heavy: 0.0, size: [0.6, 1.6],
               spawn: 0.85, up: 0 },

    /* ---- SWIRLS: something orbits the wielder ------------------------ */
    redflail: { mode: 'swirl', n: 1300, sp: [180, 420], grav: 60, drag: 1.0,
                life: [0.35, 0.90], heavy: 0.06, size: [0.7, 2.0],
                spawn: 0.70, up: 0 },
    bulwarden: { mode: 'swirl', n: 1200, sp: [90, 240], grav: -20, drag: 0.8,
                 life: [0.60, 1.50], heavy: 0.0, size: [0.6, 1.8],
                 spawn: 0.85, up: 0, ccw: true },

    /* ---- FALLS: it arrives rather than escapes ----------------------- */
    vinesower: { mode: 'fall', n: 1000, sp: [60, 220], grav: 260, drag: 0.9,
                 life: [0.60, 1.50], heavy: 0.05, size: [0.7, 2.1],
                 spawn: 0.85, up: 0 },
    /* A FREEZE HOLDS, so its frost settles slowly and lasts -- the same
       reason the art is long: the hold it explains is still in force. */
    thornwake: { mode: 'fall', n: 1100, sp: [30, 120], grav: 110, drag: 1.0,
                 life: [0.80, 1.80], heavy: 0.02, size: [0.6, 1.9],
                 spawn: 0.85, up: 0 },
    heartwood: { mode: 'fall', n: 1050, sp: [30, 120], grav: 110, drag: 1.0,
                 life: [0.80, 1.70], heavy: 0.02, size: [0.6, 1.9],
                 spawn: 0.85, up: 0 },

    /* THE WINNOWING. A FALL, not a burst: the one set-piece in the game whose
       objects are already doing the throwing, so the field must not compete
       with seventy kunai for the same read. Leaves come DOWN through the hall
       behind them -- slow, long-lived, barely any speed of their own, and the
       widest spawn band of any fall because the whole hall is in play rather
       than one point in it. */
    thornshear: { mode: 'fall', n: 1150, sp: [20, 110], grav: 70, drag: 1.1,
                  life: [0.90, 2.00], heavy: 0.03, size: [0.7, 2.0],
                  spawn: 0.90, up: 0 },
    /* THE SENTINEL. A SWIRL and not a beam, and the choice is the mechanic:
       `mode: 'beam'` spawns along the cast-time axis and FREEZES there, which
       is right for the seven instantaneous shafts that carry it and wrong for
       the one beam in the game that turns -- the motes would sit on a bearing
       the beam left two seconds ago. A swirl holds them at a radius instead,
       tangential rather than launched, which is what a turning thing looks
       like and is the honest picture of the design's §6.1: the light is not
       thrown, the room is being swept. Slow, long-lived and sparse, because
       the shaft is already the brightest object in the frame and this must
       not compete with it (§4.1b, twice, on this school). */
    vesper: { mode: 'swirl', n: 1050, sp: [40, 150], grav: -14, drag: 0.7,
              life: [0.90, 2.10], heavy: 0.0, size: [0.6, 1.9],
              spawn: 0.85, up: 0 },
    /* ---- IMPLOSION: a burst run backwards ---------------------------- */
    /* Dirge is the only pull in the game. Running a ring INWARD is the
       cheapest possible way to say "this is not one of those" -- which is the
       trick Slagburst's own fuse art already uses. */
    gravemourn: { mode: 'implode', n: 1250, sp: [140, 420], grav: 0,
                  drag: 0.55, life: [0.40, 1.00], heavy: 0.03,
                  size: [0.7, 2.0], spawn: 0.55, up: 0 }
  };

  function Field() {
    this.parts = [];
    this.spec = null;
    this.t = 0;
    this.scale = 1;
  }

  Field.prototype.clear = function () {
    this.parts.length = 0;
    this.spec = null;
    this.t = 0;
  };

  /* SPAWNED AS DATA. Particle i always draws the same numbers in the same
     order from the same seed, so two runs of a clip are bit-identical and a
     difference between two builds is the spec and nothing else. */
  Field.prototype.spawn = function (spec, seed, geom, scale) {
    this.clear();
    if (!spec) return;
    this.spec = spec;
    this.scale = (scale === undefined || scale === null) ? 1 : scale;
    var n = Math.round(spec.n * this.scale);
    if (n <= 0) return;
    var rnd = mulberry32((seed | 0) ^ 0x51AB1E);
    var L = geom || {}, i;
    var dx = (L.tx - L.x) || 0, dy = (L.ty - L.y) || 0;
    var len = Math.sqrt(dx * dx + dy * dy) || 1;
    var radius = L.radius || 200;
    for (i = 0; i < n; i++) {
      var a = rnd() * Math.PI * 2;
      /* squared, so most are slow and a few carry */
      var sp = spec.sp[0] + rnd() * rnd() * (spec.sp[1] - spec.sp[0]);
      var ox = 0, oy = 0, vx, vy, u, rr, b, dir;
      if (spec.mode === 'beam') {
        u = rnd();
        ox = dx * u; oy = dy * u;
        ox += (-dy / len) * (rnd() - 0.5) * 26;
        oy += (dx / len) * (rnd() - 0.5) * 26;
        vx = Math.cos(a) * sp * 0.4; vy = Math.sin(a) * sp * 0.4;
      } else if (spec.mode === 'field') {
        /* sqrt so the disc fills evenly instead of clustering at the middle */
        rr = Math.sqrt(rnd()) * radius;
        ox = Math.cos(a) * rr; oy = Math.sin(a) * rr;
        b = rnd() * Math.PI * 2;
        vx = Math.cos(b) * sp; vy = Math.sin(b) * sp;
      } else if (spec.mode === 'swirl') {
        /* TANGENTIAL, not radial: held at a radius rather than launched from
           the middle, which is the whole difference from a nova. */
        rr = (0.35 + 0.65 * Math.sqrt(rnd())) * radius;
        ox = Math.cos(a) * rr; oy = Math.sin(a) * rr;
        dir = spec.ccw ? -1 : 1;
        vx = -Math.sin(a) * sp * dir; vy = Math.cos(a) * sp * dir;
      } else if (spec.mode === 'fall') {
        /* spawned across a band ABOVE the point and let down onto it, so the
           motes arrive rather than escape. Wider than tall: the arena is
           520x740 and a square spawn box reads as a column. */
        ox = (rnd() - 0.5) * 2 * radius;
        oy = -radius * (0.4 + rnd() * 0.9);
        vx = (rnd() - 0.5) * sp * 0.5; vy = sp * 0.5;
      } else if (spec.mode === 'implode') {
        rr = (0.7 + 0.3 * rnd()) * radius;
        ox = Math.cos(a) * rr; oy = Math.sin(a) * rr;
        vx = -Math.cos(a) * sp; vy = -Math.sin(a) * sp;
      } else {
        vx = Math.cos(a) * sp; vy = Math.sin(a) * sp - (spec.up || 0);
      }
      var heavy = rnd() < (spec.heavy || 0);
      this.parts.push({
        x: ox, y: oy, vx: vx, vy: vy,
        birth: rnd() * (spec.spawn || 0),
        life: spec.life[0] + rnd() * (spec.life[1] - spec.life[0]),
        age: -1,
        r: heavy ? 2.6 + rnd() * 3.4
                 : spec.size[0] + rnd() * (spec.size[1] - spec.size[0]),
        spin: (rnd() - 0.5) * 18,
        rot: rnd() * 6.28,
        heavy: heavy,
        seedv: rnd()
      });
    }
  };

  /* INTEGRATE TO AN ABSOLUTE SIM TIME, in fixed dt chunks.
   *
   * Absolute rather than by-a-delta is the whole reason this is safe to call
   * from inside drawUltOver, which the post chain runs TWICE per composited
   * frame. A second call with the same `t` does nothing. See the header.
   *
   * The step cap is a backstop, not a policy: a clip that skipped four
   * seconds of sim would otherwise spin 480 iterations here. It is high
   * enough that no real frame reaches it. */
  Field.prototype.stepTo = function (t, dt) {
    var S = this.spec;
    if (!S || !(dt > 0)) return;
    var guard = 0;
    var decay = Math.exp(-S.drag * dt);
    while (this.t + dt <= t && guard++ < 400) {
      this.t += dt;
      for (var i = 0; i < this.parts.length; i++) {
        var p = this.parts[i];
        if (this.t < p.birth) continue;
        if (p.age < 0) p.age = 0;
        if (p.age > p.life) continue;
        p.age += dt;
        p.vx *= decay;
        p.vy = p.vy * decay + S.grav * dt;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.rot += p.spin * dt;
      }
    }
  };

  Field.prototype.alive = function () {
    for (var i = 0; i < this.parts.length; i++) {
      var p = this.parts[i];
      if (p.age >= 0 && p.age <= p.life) return true;
      if (this.t < p.birth) return true;
    }
    return false;
  };

  /* MOTES ADDITIVE, DEBRIS NOT. The bloom reads the emissive layer, so a mote
     drawn `lighter` becomes light while a chunk that is not stays an object.
     CLAUDE.md §4.1b: a thing that is only ever added is not an object, it is
     a hole -- which is how Daybreak's ball stopped being one. */
  Field.prototype.draw = function (c, cx, cy, aff) {
    if (!this.spec || !this.parts.length) return;
    var hot = '#FFF6E2';
    var mid = (aff && aff.core) || '#FF9A3C';
    var cool = (aff && aff.dark) || '#8C2A0A';
    c.save();
    c.translate(cx, cy);
    for (var i = 0; i < this.parts.length; i++) {
      var p = this.parts[i];
      if (p.age < 0 || p.age > p.life) continue;
      var k = p.age / p.life, fade = 1 - k * k;
      if (p.heavy) {
        c.globalCompositeOperation = 'source-over';
        c.globalAlpha = 0.85 * fade;
        c.save();
        c.translate(p.x, p.y);
        c.rotate(p.rot);
        c.fillStyle = '#1A0A05';
        c.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 1.2);
        c.globalCompositeOperation = 'lighter';
        c.globalAlpha = fade * (0.5 + 0.5 * p.seedv);
        c.fillStyle = k < 0.5 ? mid : cool;
        c.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 0.35);
        c.restore();
      } else {
        c.globalCompositeOperation = 'lighter';
        c.globalAlpha = fade;
        /* cooling: white -> the school's core -> its dark. One flat colour
           never says a particle is losing energy. */
        c.fillStyle = k < 0.25 ? hot : (k < 0.62 ? mid : cool);
        c.beginPath();
        c.arc(p.x, p.y, p.r * (1 - 0.45 * k), 0, 6.2832);
        c.fill();
      }
    }
    c.restore();
  };

  /* THE CAST SEED, FROM SIM STATE ONLY.
   *
   * Not from a renderer-side counter and not from wall time: either would
   * differ between the app's rAF cadence and the capture's fixed one, and the
   * whole point is that they cannot. The fight's seed, the relic, the caster
   * and the cast POSITION quantised -- so it is identical everywhere and still
   * varies between two casts of the same ult in one fight. */
  function castSeed(matchSeed, u) {
    var h = (matchSeed | 0) ^ hashStr(String(u.w) + '|' + String(u.src));
    h ^= Math.imul(Math.round((u.x || 0) * 16) | 0, 0x9E3779B1);
    h ^= Math.imul(Math.round((u.y || 0) * 16) | 0, 0x85EBCA77);
    return h >>> 0;
  }

  root.SWBFx = {
    VERSION: VERSION,
    SPECS: SPECS,
    create: function () { return new Field(); },
    castSeed: castSeed,
    mulberry32: mulberry32
  };
})(typeof window !== 'undefined' ? window : this);
