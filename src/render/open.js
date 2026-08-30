/* THE IGNITION OPEN — the first two and a bit seconds of a fight, as a shot.
 *
 * Prototyped in tools/ignition_lab.py as four variants over one seed; Rick
 * watched `ignition-open-both-solo.mp4` and said make it happen. This file is
 * the "both" variant — the opening camera AND the ignition — moved out of the
 * lab's capture-time monkey patches and into the build, so the app and the mp4
 * run the same one (docs/ARCHITECTURE.md §1).
 *
 * NO IMPORTS, NO DEPENDENCIES, ONE FILE. Same rule as src/render/post.js and
 * src/render/fx.js, and for the same reason: the build is one self-contained
 * HTML file with no <script src>. Everything it needs — the match, the
 * renderer, the arena box — is handed in.
 *
 * ── THE CLOCK IS SIM TIME, AND THAT IS LOAD-BEARING ─────────────────────
 *
 * The lab drove all three parts off WALL time, which it could: during the
 * opening there are no cuts, so CINE.timeScale is 1 and wall time and match
 * time are the same number. In the build they must not be assumed equal.
 * Every function here is a pure function of `m.t`, which buys three things
 * the lab did not need and the build does:
 *
 *   1. THE POST CHAIN DRAWS EVERY FRAME FOUR TIMES (readouts, emissive,
 *      world, composite). A pure function of m.t is idempotent, so the extra
 *      passes cannot double-advance anything. fx.js and post_build.py's
 *      camera shake are the two times this project has paid for getting that
 *      wrong, and the shake presented as juddering PHYSICS.
 *   2. THE APP'S rAF AND THE CAPTURE'S FIXED CADENCE AGREE. A dropped frame
 *      in the app is fewer samples of the same shot, not a different shot.
 *   3. NO Math.random ANYWHERE. The handheld drift is the engine's own
 *      two-frequency formula (CINE.update's), evaluated at m.t.
 *
 * ── WHAT IT DOES NOT TOUCH ──────────────────────────────────────────────
 *
 * The simulation. Nothing here is read by anything the sim can see: the
 * camera is a transform, the swell is a shadowBlur multiplier, the flare is
 * drawn over the finished frame. engine_ab is expected to come back IDENTICAL,
 * and if it does not, something here is wrong rather than interesting.
 */
(function (root) {
  'use strict';

  var VERSION = 1;

  /* ---------------------------------------------------------- the shot ---
     Fighter A, hard cut to fighter B, pull wide — timed so the pull lands
     just before a ~2.3s first clank arms the scrunch. `at` is the subject and
     it is put at frame CENTRE, not leaned toward: an opening shot frames one
     relic, which is the whole reason the feasibility clamp has to stand down
     for it (see cam()). */
  var SHOTS = [
    { t0: 0.00, t1: 0.85, at: 'a', z0: 2.25, z1: 2.02 },
    { t0: 0.85, t1: 1.55, at: 'b', z0: 2.25, z1: 2.02 },
    { t0: 1.55, t1: 2.35, from: 'b', to: 'center',
      z0: 2.02, z1: 1.00, ease: 'smooth' }
  ];

  /* ---------------------------------------------------------- the look ---
     THE SETTINGS LIVE HERE, not in the builder's glue. Same rule post_build.py
     states for SWBPost.SPREAD: a second copy of "which opening" in the glue is
     how a build ends up shipping something nobody picked. These are the
     numbers off the clip Rick approved — the lab's "both" variant. */
  var LOOK = {
    flareA: 0.10,      // when relic A ignites, sim seconds
    flareB: 0.95,      // and B — staggered onto the cut, which is what
                       // separates "both" from the ignition-only variant
    flareLife: 0.90,   // one flare, start to gone
    swellDur: 0.95,    // the global glow power-on
    swellFrom: 0.30,   // every shadowBlur in the hall starts at 30% ...
    swellPeak: 1.42,   // ... overshoots ...
                       // ... and lands on exactly 1.0, which is identity.
    handheld: 2.6,     // sim units, scaled by how far in the lens is
    relicSu: 34,       // the relic's own radius, in sim units: what the
                       // subject-fit clamp at the end of cam() keeps in frame
    /* How far past the strict wall bound the opening may lean, replacing
       CINE.overscan (0.55) for its window only. At the shipped value a corner
       spawn pins against the frame edge and the subject never reaches centre;
       the floor bleed covers the difference. CINE is not mutated — this is
       applied to this module's own clamp. */
    overscan: 0.95
  };

  var DUR = SHOTS[SHOTS.length - 1].t1;

  function lerp(a, b, u) { return a + (b - a) * u; }
  function easeOutCubic(u) { return 1 - Math.pow(1 - u, 3); }
  function smooth(u) { return u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u); }
  function eob(u, c) {                                    // ease-out-back
    u = Math.min(1, Math.max(0, u));
    var c1 = c === undefined ? 1.70158 : c, c3 = c1 + 1;
    return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2);
  }

  /* The opening is over the moment the card is up (m.t is held at zero while
     it is, so without this the shot would play against a frozen hall), and the
     moment its own clock runs out. */
  function live(m, t) {
    return !!(root.SWBOpen && root.SWBOpen.on) && !!m &&
           !(m.introT > 0) && m.t >= 0 && m.t < t;
  }

  /* ------------------------------------------------------- 1. THE CAMERA ---
     Returns [px, py, z] in DEVICE pixels for the renderer's fixed-point
     transform, or null when the opening does not own the camera.

     WHY THIS CANNOT GO THROUGH CINE. The renderer's both-relics-must-fit
     feasibility clamp is correct for every mid-fight cut and is exactly why an
     opening shot cannot exist without a caller like this one: at spawn
     separation (~503 su) it pulls any asked zoom back to ~1.0. So the opening
     does not ask CINE for a zoom it would then have taken away — it computes
     its own transform and the renderer uses it instead. The lean clamp below
     still applies; only the feasibility clamp stands down, and only for these
     2.35 seconds. */
  function cam(m, r, A) {
    if (!live(m, DUR) || !r || !A) return null;
    var t = m.t, shot = null, i;
    for (i = 0; i < SHOTS.length; i++)
      if (t >= SHOTS[i].t0 && t < SHOTS[i].t1) { shot = SHOTS[i]; break; }
    if (!shot) return null;

    var pos = function (id) {
      return id === 'a' ? [m.a.x, m.a.y]
           : id === 'b' ? [m.b.x, m.b.y]
           : id === 'mid' ? [(m.a.x + m.b.x) / 2, (m.a.y + m.b.y) / 2]
           : [A.w / 2, A.h / 2];
    };
    var u = (t - shot.t0) / (shot.t1 - shot.t0);
    var e = shot.ease === 'smooth' ? smooth(u) : easeOutCubic(u);
    var p0 = pos(shot.from || shot.at), p1 = pos(shot.to || shot.at);
    var sx = lerp(p0[0], p1[0], e), sy = lerp(p0[1], p1[1], e);
    var z = lerp(shot.z0, shot.z1, e);
    if (z <= 1.02) return null;               // nothing left to own

    /* THE RENDERER ZOOMS ABOUT ITS FOCUS, so the focus point keeps its screen
       position — which leaves a corner spawn magnified in its corner. To put
       the SUBJECT at frame centre C, solve for the pivot p from
       s' = p + z(s - p) = C  ->  p = (C - z*s) / (1 - z). Blend back to C as z
       approaches 1, where the transform tends to identity and the formula
       tends to a pole. */
    var sc = r.scale;
    var Cx = r.aw / 2, Cy = r.ah / 2;
    var spx = sx * sc, spy = sy * sc, px, py, w;
    if (z > 1.06) {
      px = (Cx - z * spx) / (1 - z);
      py = (Cy - z * spy) / (1 - z);
      w = Math.min(1, (z - 1.02) / 0.30);
      px = lerp(Cx, px, w); py = lerp(Cy, py, w);
    } else { px = Cx; py = Cy; }

    /* HANDHELD. The engine's own two-frequency drift (CINE.update's formula),
       evaluated at sim time rather than accumulated, at a smaller amplitude
       and scaled by how far the lens is in — a wide frame does not wobble.
       Deliberately not random: identical every replay. */
    var amp = LOOK.handheld * Math.min(1, (z - 1) / 0.6);
    var hx = (Math.sin(t * 2.30) * 0.62 + Math.sin(t * 3.71 + 1.1) * 0.38) * amp;
    var hy = (Math.sin(t * 1.93 + 0.6) * 0.58 + Math.sin(t * 4.17) * 0.42) * amp;
    px += hx * sc; py += hy * sc;

    /* The lean clamp, at this module's overscan. Same rule the renderer
       applies to CINE: the centre may travel (1 - 1/z) of half the frame,
       relaxed by overscan, and the floor bleed covers what leaning past the
       wall reveals. */
    var over = 1 + LOOK.overscan;
    var mx = (r.aw / 2) * (1 - 1 / z) * over;
    var my = (r.ah / 2) * (1 - 1 / z) * over;
    px = Math.min(Math.max(px, r.aw / 2 - mx), r.aw / 2 + mx);
    py = Math.min(Math.max(py, r.ah / 2 - my), r.ah / 2 + my);

    /* AND THE SUBJECT MUST BE IN FRAME, which WINS over the lean clamp — the
       same precedence, and the same solve, the renderer applies to a cut.

       This is the guarantee the feasibility clamp normally provides and which
       the opening switches off, so it has to be re-established for the one
       relic being filmed. It is not theoretical: with only the lean clamp, a
       subject caught against a wall grazes the frame edge by up to 12.5px of a
       1625px frame (ignition_probe.py, swept over twelve pairings). Small, but
       it is the ball being cut in half, and the pull-back the renderer would
       otherwise do is not available inside a shot that has to hold its zoom.

       From ls = px + (s·sc - px)·z, the subject's disc sits inside the frame
       for px in [(s·sc·z - (aw - rr))/(z - 1), (s·sc·z - rr)/(z - 1)]. */
    var rr = LOOK.relicSu * sc * z;
    var loX = (spx * z - (r.aw - rr)) / (z - 1), hiX = (spx * z - rr) / (z - 1);
    var loY = (spy * z - (r.ah - rr)) / (z - 1), hiY = (spy * z - rr) / (z - 1);
    if (loX <= hiX) px = Math.min(Math.max(px, loX), hiX);
    if (loY <= hiY) py = Math.min(Math.max(py, loY), hiY);
    return [px, py, z];
  }

  /* -------------------------------------------------------- 2. THE SWELL ---
     Every glow in the hall powers on: 0.30 -> overshoot 1.42 -> exactly 1.0.

     ONE PROPERTY, FIFTY-TWO SITES. The art sets `shadowBlur` in fifty-two
     places and none of them is going to learn about the opening, so the
     multiplier is applied in an accessor on the prototype — the same trick,
     the same canvas guard, as cinema_clip.py's BLUR_SCALE_JS.

     INSTALLED ONLY WHILE IT IS NEEDED. At mul === 1 the accessor is exact
     identity, but it is still an accessor on a property the renderer writes
     dozens of times a frame for the whole fight. So it goes on when the
     opening starts and comes off — restoring the captured native descriptor —
     the moment the multiplier returns to 1. Cost outside 0.95s: zero. */
  var _base = null, _R = null;

  function _install(r) {
    if (_base) { _R = r; return; }
    if (typeof CanvasRenderingContext2D === 'undefined') return;
    var proto = CanvasRenderingContext2D.prototype;
    var base = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
    if (!base || !base.set) return;
    _base = base; _R = r;
    Object.defineProperty(proto, 'shadowBlur', {
      configurable: true,
      get: function () { return base.get.call(this); },
      set: function (v) {
        var S = root.SWBOpen, cv = this.canvas;
        if (v && S && S.mul !== 1 && cv && _R &&
            (cv === _R.cv || cv === _R._bbuf)) v = v * S.mul;
        base.set.call(this, v);
      }
    });
  }

  function _restore() {
    if (!_base) return;
    Object.defineProperty(CanvasRenderingContext2D.prototype, 'shadowBlur', _base);
    _base = null; _R = null;
  }

  function swell(m, r) {
    var S = root.SWBOpen;
    if (!live(m, LOOK.swellDur)) {
      if (S.mul !== 1) { S.mul = 1; }
      _restore();
      return 1;
    }
    var u = m.t / LOOK.swellDur;
    S.mul = u < 0.5 ? lerp(LOOK.swellFrom, LOOK.swellPeak, easeOutCubic(u / 0.5))
                    : lerp(LOOK.swellPeak, 1.0, smooth((u - 0.5) / 0.5));
    _install(r);
    return S.mul;
  }

  /* -------------------------------------------------------- 3. THE FLARE ---
     Drawn OVER the finished frame, in sim coordinates, through the renderer's
     real transform.

     AND "OVER THE FINISHED FRAME" IS A DECISION, NOT A CONVENIENCE. fx.js
     hooks inside drawUltOver precisely so its fields reach the bloom. This
     does the opposite on purpose: the flare Rick approved was drawn after the
     composite, so it is NOT bloomed, and moving it into the emissive pass
     would hand a white core at 0.95 alpha to a chain that is already the
     largest single light source this project has measured (CLAUDE.md §4.1d).
     Ship the picture that was approved. */
  function flare(m, r) {
    if (!live(m, LOOK.flareB + LOOK.flareLife) || !r) return 0;
    var c = r.ctx, jobs = [[m.a, LOOK.flareA], [m.b, LOOK.flareB]], drawn = 0, i;
    c.save();
    /* The transform Renderer.draw builds, replicated: device scale, the arena
       origin, the cinematic fixed point, then sim units. Shake and punch are
       zero before first contact, which is the only window this draws in. */
    c.setTransform(r.k, 0, 0, r.k, 0, 0);
    c.translate(r.pad, r.arenaTop);
    if (r._cineCam) {
      c.translate(r._cineCam[0], r._cineCam[1]);
      c.scale(r._cineCam[2], r._cineCam[2]);
      c.translate(-r._cineCam[0], -r._cineCam[1]);
    }
    c.scale(r.scale, r.scale);
    c.globalCompositeOperation = 'lighter';
    for (i = 0; i < jobs.length; i++) {
      var f = jobs[i][0], t = m.t - jobs[i][1];
      if (!f || !f.aff || t < 0 || t > LOOK.flareLife) continue;
      drawn++;
      /* the corona — the relic's OWN affinity glow, overshooting and settling.
         Six palettes, so the two relics ignite in their own colours. */
      var R = 96 * eob(Math.min(1, t / 0.55), 2.2);
      var ca = t < 0.20 ? 0.80 * (t / 0.20)
                        : 0.80 * Math.pow(1 - (t - 0.20) / 0.70, 1.4);
      if (ca > 0.01 && R > 1) {
        var g = c.createRadialGradient(f.x, f.y, 2, f.x, f.y, R);
        g.addColorStop(0, f.aff.glow);
        g.addColorStop(0.55, f.aff.core);
        g.addColorStop(1, 'rgba(0,0,0,0)');
        c.globalAlpha = ca;
        c.fillStyle = g;
        c.beginPath(); c.arc(f.x, f.y, R, 0, Math.PI * 2); c.fill();
      }
      /* the expanding ring — the strike's report */
      var ru = Math.min(1, t / 0.62);
      if (ru < 1) {
        c.globalAlpha = 0.55 * (1 - ru);
        c.strokeStyle = f.aff.core;
        c.lineWidth = 9 * (1 - ru) + 1.5;
        c.beginPath();
        c.arc(f.x, f.y, 20 + 150 * easeOutCubic(ru), 0, Math.PI * 2);
        c.stroke();
      }
      /* the white core strike, three or four frames of it */
      if (t < 0.14) {
        var cu = t / 0.14;
        c.globalAlpha = 0.95 * Math.pow(1 - cu, 0.8);
        c.fillStyle = '#FFFFFF';
        c.beginPath(); c.arc(f.x, f.y, 12 + 36 * cu, 0, Math.PI * 2); c.fill();
      }
    }
    c.restore();
    c.globalAlpha = 1;
    c.globalCompositeOperation = 'source-over';
    return drawn;
  }

  root.SWBOpen = {
    VERSION: VERSION,
    on: true,
    mul: 1,            // the live shadowBlur multiplier; 1 is identity
    DUR: DUR,
    SHOTS: SHOTS,
    LOOK: LOOK,
    cam: cam,
    swell: swell,
    flare: flare,
    /* for the probes: what the opening is doing at a given sim time, without
       a renderer or a frame */
    phase: function (t) {
      return t >= DUR ? 'released'
           : t >= LOOK.flareB + LOOK.flareLife ? 'pull'
           : t >= LOOK.swellDur ? 'flares' : 'ignite';
    }
  };
})(typeof window !== 'undefined' ? window : this);
