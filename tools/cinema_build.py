#!/usr/bin/env python3
"""CINEMA — an experimental director for the big moments.  DEMO BUILD.

Patches sc-sil.html into sc-cinema.html: massive cinematic hit stop, a
slow-motion push into the point of contact, letterbox, and an audio send that
ducks the hall and drags the score down in pitch with the picture.

    python3 cinema_build.py --in sc-sil.html --out sc-cinema.html
    python3 cinema_build.py --check sc-cinema.html   # assert the sim is untouched

THE INVARIANT this build exists to keep: the director cannot change who wins.
It is enforced structurally, not by review. The only thing it does to time is
change how much WALL time the frame loop feeds the fixed-step accumulator --

    acc += raw * speed * CINE.timeScale
    while (acc >= dt) match.step(dt)

-- and the sim consumes that in identical CONFIG.physics.dt slices whatever the
rate. It never touches m.hitStop, because hit stop lives inside step() and m.t
advances through it, so lengthening THAT really would change the fight.

Every edit below is either presentation-only or an additive beat() call in the
same family as the existing note() and statusTag().
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def subN(src: str, old: str, new: str, label: str, n: int) -> str:
    """Replace exactly `n` occurrences. Used where the engine legitimately has
    the same line in two places -- both bow shot sites build their projectile
    from the identical launch expression."""
    got = src.count(old)
    if got != n:
        raise SystemExit(f"[cinema_build] anchor {label!r} matched {got} times, need {n}")
    return src.replace(old, new)


def sub1(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or fail loudly.

    A patch that silently matches zero times produces a build that looks fine
    and does nothing, which is the only failure mode of this kind of script
    that survives to the demo.
    """
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"[cinema_build] anchor {label!r} matched {n} times, need 1")
    return src.replace(old, new, 1)


# --------------------------------------------------------------------------
# 1. the sim side: a beat is a dramatic instant, recorded the way note() is.
# --------------------------------------------------------------------------
BEATS_INIT = """    this.hitStop = 0;
    this.finisher = 0;"""
BEATS_INIT_NEW = """    this.hitStop = 0;
    /* CINEMA (demo). Presentation only, in the same family as `events` and
       `tags`: a list of dramatic instants for the director to read. Nothing in
       the simulation reads it, and because a headless prescan runs the same
       code it produces the same list -- which is what lets the director see
       the whole fight before the first frame is drawn. */
    this.beats = [];
    this.finisher = 0;"""

NOTE_M = "  note(text){ this.events.push({ t:this.t, text }); }"
NOTE_M_NEW = """  note(text){ this.events.push({ t:this.t, text }); }

  /* CINEMA (demo). Write-only from the sim's point of view. */
  beat(o){
    o.t = this.t;
    this.beats.push(o);
    if (this.beats.length > 600) this.beats.shift();
  }"""

HIT_A = """    this.hitStop = Math.max(this.hitStop, stop);
    if (!fatal) foe.takeHitstun(dmg);"""
HIT_B = """    this.hitStop = Math.max(this.hitStop, stop);
    /* CINEMA (demo). `hpAfter` rather than `dmg` alone, because the director
       scores the SHARE of what was left that this hit took -- 40 points off a
       full relic is a scratch, 40 off a relic sitting on 45 is the fight. */
    /* CINEMA (demo). The kinematics, not just the number. What makes a blow
       cinematic is how hard the two things were moving when they met and how
       far the blow came from -- damage is an outcome, speed is the picture. */
    const _cs = this._cineShot;
    this.beat({ kind: "hit", side: self === this.a ? 0 : 1, x: hx, y: hy,
                dmg, crit, fatal, hpAfter: Math.max(0, foe.hp),
                hpFrac: Math.max(0, foe.hp) / foe.maxHp, maxHp: foe.maxHp,
                selfHpFrac: self.hp / self.maxHp,
                spd: self.speed, foeSpd: foe.speed,
                /* Closing speed: the magnitude of the RELATIVE velocity. Two
                   relics flying at each other is the shot; two drifting the
                   same way at the same speed is not, however fast the number
                   on either one. */
                close: Math.hypot(self.vx - foe.vx, self.vy - foe.vy),
                ranged: !!_cs,
                range: _cs ? Math.hypot(hx - _cs.x0, hy - _cs.y0) : 0,
                /* Loose time and place, so the director can film the shot
                   BEING TAKEN and not just landing -- without both ends the
                   viewer cannot tell what caused the cinematic. */
                loosT: _cs ? (_cs.t0 || 0) : 0,
                lx: _cs ? _cs.x0 : 0, ly: _cs ? _cs.y0 : 0,
                shotSpd0: _cs ? (_cs.spd0 || 0) : 0 });
    if (!fatal) foe.takeHitstun(dmg);"""

ULT_A = """    this.hitStop = Math.max(this.hitStop, 0.08);
    SFX.play("ult", { w: f.w.id });"""
ULT_B = """    this.hitStop = Math.max(this.hitStop, 0.08);
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: f.x, y: f.y,
                w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });   // CINEMA (demo)
    SFX.play("ult", { w: f.w.id });"""

CLANK_A = """    this.hitStop = Math.max(this.hitStop, C.stop);
    this.shake   = Math.max(this.shake, C.shake);"""
CLANK_B = """    this.hitStop = Math.max(this.hitStop, C.stop);
    this.beat({ kind: "clank", x: hx, y: hy,                        // CINEMA
                streak: this.clankStreak, decisive: !!decisive,
                spd: Math.max(A.speed, B.speed),
                close: Math.hypot(A.vx - B.vx, A.vy - B.vy) });
    this.shake   = Math.max(this.shake, C.shake);"""

# --------------------------------------------------------------------------
# 2. the camera: the renderer's existing punch slot, generalised.
# --------------------------------------------------------------------------
CAM_A = """    const punch = m.hitStop > 0 ? 1 + Math.min(0.022, m.hitStop * 0.16) : 1;
    c.translate(this.pad + ox, this.arenaTop + oy);
    c.beginPath(); c.rect(0, 0, this.aw, this.ah); c.clip();
    c.translate(this.aw/2, this.ah/2); c.scale(punch, punch); c.translate(-this.aw/2, -this.ah/2);"""
CAM_B = """    const punch = m.hitStop > 0 ? 1 + Math.min(0.022, m.hitStop * 0.16) : 1;
    c.translate(this.pad + ox, this.arenaTop + oy);
    /* CINEMA (demo). During a cut the clip breathes 70px past the arena so
       impact bursts, streaks and rings at a WALL contact spill onto the bled
       floor instead of being guillotined at the wall line -- part of "action
       getting cut off" at the bottom was the arena rect itself amputating
       effect art centred on a wall-adjacent blow. Normal play keeps the exact
       original clip. */
    const cineSpill = (typeof CINE !== "undefined" && CINE.on && CINE.cut) ? 70 : 0;
    c.beginPath(); c.rect(-cineSpill, -cineSpill,
                          this.aw + cineSpill * 2, this.ah + cineSpill * 2); c.clip();
    c.translate(this.aw/2, this.ah/2); c.scale(punch, punch); c.translate(-this.aw/2, -this.ah/2);

    /* CINEMA (demo). The push, about the point of contact rather than about
       the middle of the hall.

       At zoom z a strict "never show past the wall" rule allows the centre to
       travel only (1 - 1/z) of half the frame. MEASURED: at the 1.38x this
       build uses, that is 72 sim units of a 260-unit half-arena -- so the
       clamp, not `bias`, was governing every off-centre contact, and raising
       bias was a no-op. Lean and push are not independent levers; travel is a
       function of zoom.

       So the rule is relaxed by CINE.overscan, and drawArena's base fill is
       extended by the same margin so the camera leaning past the wall shows
       more hall floor rather than a colour seam. */
    if (typeof CINE !== "undefined" && CINE.on && CINE.zoom > 1.0001){
      let z = CINE.zoom, over = 1 + (CINE.overscan || 0);
      const mx = (this.aw / 2) * (1 - 1 / z) * over;
      const my = (this.ah / 2) * (1 - 1 / z) * over;
      let px = clamp((CINE.fx + CINE.hx) * this.scale, this.aw/2 - mx, this.aw/2 + mx);
      let py = clamp((CINE.fy + CINE.hy) * this.scale, this.ah/2 - my, this.ah/2 + my);
      /* THE ACTION MUST BE ON SCREEN — and the action is not a point.

         The first fix here clamped the FOCUS POINT into the frame and its
         probe verified exactly that, which is why it passed while play kept
         showing cut-off action: a relic has a radius that the zoom multiplies
         (34 sim units is ~150px of body at 1080p whip zoom), and the letterbox
         eats the frame edges on top of it. Measured before this version:
         8/8 wall-adjacent set-pieces clipped relic body, by 137-376px at
         540-wide (cinema_edge_probe.py).

         So the constraint is now physical: BOTH relics' magnified bodies must
         sit inside the usable frame (viewport minus the current letterbox),
         solved per relic from fs = y*z - py*(z-1). When the two relics are too
         far apart to both fit at this zoom, the one nearer the focus wins --
         the contact must be visible, the rebounding loser may leave. This
         clamp WINS over the lean clamp above; the camera centre may leave the
         viewport entirely to satisfy it, and the floor bleed covers what that
         reveals. */
      if (z > 1.02 && m){
        const mm = Math.min(this.aw, this.ah) * 0.05;
        const barH = this.ah * 0.115 * (CINE.bars || 0);
        /* FEASIBILITY FIRST: pull back before choosing who to amputate. The
           per-relic clamp below can only pick a winner when both bodies
           cannot fit at this zoom -- and the frame probe showed exactly that
           happening in volley gaps, a relic up to 157px out of frame at the
           sides while the camera panned between distant blows. A camera
           operator does not crop a fighter off; they go wide. So compute the
           largest zoom at which both discs plus effect pad fit the usable
           frame, and use it when it is smaller than the director's ask. The
           pad (+22su) covers floats and impact art that hang off a relic,
           which relic-disc math alone missed -- and which is what "action
           getting cut off" looks like from the couch even when the disc is
           technically framed. Continuous in relic positions, so the pull-back
           reads as a move, not a cut. */
        const padSu = 34 + 22;
        const dx = Math.abs(m.a.x - m.b.x) * this.scale;
        const dy = Math.abs(m.a.y - m.b.y) * this.scale;
        const zx = (this.aw - 2 * mm) / Math.max(1, dx + 2 * padSu * this.scale);
        const zy = (this.ah - 2 * barH - 2 * mm) / Math.max(1, dy + 2 * padSu * this.scale);
        z = Math.max(1.02, Math.min(z, zx, zy));
        const rp = padSu * this.scale * z + mm;
        let lo = -1e9, hi = 1e9, lox = -1e9, hix = 1e9;
        /* Farther-from-focus FIRST, so the nearer relic is applied last and
           wins any conflict. The first version sorted descending and then
           reversed -- nearer first, farther overwriting it -- which handed the
           frame to a distant archer while the victim it had just shot fell out
           of the bottom of the shot. The probe caught it because it reports
           WHO clipped and how far from focus they were: 87su, i.e. the victim. */
        const pts = [m.a, m.b].sort((a2, b2) =>
          Math.hypot(b2.x - CINE.fx, b2.y - CINE.fy) -
          Math.hypot(a2.x - CINE.fx, a2.y - CINE.fy));
        for (const f of pts){
          const xs = f.x * this.scale, ys = f.y * this.scale;
          const l2 = (ys * z - (this.ah - barH - rp)) / (z - 1);
          const h2 = (ys * z - (barH + rp)) / (z - 1);
          const lx2 = (xs * z - (this.aw - rp)) / (z - 1);
          const hx2 = (xs * z - rp) / (z - 1);
          if (Math.max(lo, l2) <= Math.min(hi, h2)){
            lo = Math.max(lo, l2); hi = Math.min(hi, h2);
          } else { lo = l2; hi = h2; }        // nearer relic, applied last, wins
          if (Math.max(lox, lx2) <= Math.min(hix, hx2)){
            lox = Math.max(lox, lx2); hix = Math.min(hix, hx2);
          } else { lox = lx2; hix = hx2; }
        }
        px = clamp(px, lox, hix);
        py = clamp(py, lo, hi);
      }
      c.translate(px, py); c.scale(z, z); c.translate(-px, -py);
      this._cineFocus = [px, py];
      this._cineCam = [px, py, z];
    } else { this._cineFocus = null; this._cineCam = null; }"""

OVER_A = """    this.drawTags(m);
    c.restore();"""
OVER_B = """    this.drawTags(m);
    if (typeof CINE !== "undefined" && CINE.on && CINE.streak > 0.01)
      this.drawCineStreaks(m);
    c.restore();

    if (typeof CINE !== "undefined" && CINE.on) this.drawCine(m);"""

# The overlay itself, appended as a Renderer method. Anchored on the existing
# arena drawer so it lands inside the class.
FILL_A = """  drawArena(m){
    const c = this.ctx, W = this.aw, H = this.ah;
    c.fillStyle = "#100C16"; c.fillRect(0, 0, W, H);"""
FILL_B = """  drawArena(m){
    const c = this.ctx, W = this.aw, H = this.ah;
    /* CINEMA (demo): bled outward so a camera leaning past the wall reveals
       more floor instead of a hard colour seam against the page background.
       Everything else in here still draws to the true W x H, so the walls, the
       collapse and every hitbox are exactly where they were. */
    /* 260, not 140: the physical visibility clamp can push the camera centre
       ~470px past the wall at 1080p whip zoom, revealing ~180px of beyond-wall
       floor. 140 left a seam exactly in the shots the clamp had just saved. */
    const BLEED = (typeof CINE !== "undefined" && CINE.on) ? 260 : 0;
    c.fillStyle = "#100C16";
    c.fillRect(-BLEED, -BLEED, W + BLEED * 2, H + BLEED * 2);"""

OVER_M_A = """  /* ------------------------------------------------------------- arena --- */
  drawArena(m){"""
OVER_M_B = """  /* --------------------------------------------------------- CINEMA ---
     Demo overlays. All of it is drawn AFTER the arena content and reads only
     CINE, so removing this method and its two call sites removes the feature
     without touching a line of anything else.

       wash    a desaturating scrim -- the world drains while the moment holds
       bars    letterbox. The single cheapest signal that says "this is a shot"
       flash   the frame of contact
       streaks radial smear from the point of impact, three frames of it */
  drawCine(m){
    const c = this.ctx;
    const x = this.pad, y = this.arenaTop, w = this.aw, h = this.ah;

    /* Sim coords -> screen, THROUGH the cinematic camera. The overlay draws
       after c.restore(), so anything anchored to the world has to apply the
       same fixed-point transform the arena was drawn with or it will detach
       the moment the lens moves. */
    const cam = this._cineCam;
    const S = (sx, sy) => {
      let lx = sx * this.scale, ly = sy * this.scale;
      if (cam){ lx = cam[0] + (lx - cam[0]) * cam[2];
                ly = cam[1] + (ly - cam[1]) * cam[2]; }
      return [x + lx, y + ly];
    };

    /* THE TRACER -- a ranged set-piece has to show the shot being TAKEN and
       the shot LANDING, or the viewer cannot tell what caused the cinematic.
       Three parts: a ring blooming at the loose point, a fading line down the
       flight, and a comet head riding where the bolt is. All in the shooter's
       gold, clipped to the arena. */
    if (CINE.tracer){
      const T = CINE.tracer;
      const [ax, ay] = S(T.lx, T.ly);
      const [bx2, by2] = S(T.cx, T.cy);
      const hx2 = ax + (bx2 - ax) * T.prog, hy2 = ay + (by2 - ay) * T.prog;
      c.save();
      c.beginPath(); c.rect(x, y, w, h); c.clip();
      c.globalCompositeOperation = "lighter";
      /* the loose: a ring that blooms and fades over the first half second */
      const ra = clamp(1 - T.age / 0.55, 0, 1);
      if (ra > 0){
        c.globalAlpha = 0.5 * ra;
        c.strokeStyle = "#FFE9A8"; c.lineWidth = 2.5;
        c.beginPath(); c.arc(ax, ay, 14 + (1 - ra) * 46, 0, TAU); c.stroke();
        c.globalAlpha = 0.28 * ra;
        c.beginPath(); c.arc(ax, ay, 6 + (1 - ra) * 20, 0, TAU); c.stroke();
      }
      /* the flight: brightest just behind the head, gone at the tail */
      const grad = c.createLinearGradient(ax, ay, hx2, hy2);
      grad.addColorStop(0, "rgba(255,233,168,0)");
      grad.addColorStop(0.72, "rgba(255,233,168,0.10)");
      grad.addColorStop(1, "rgba(255,244,208,0.55)");
      c.strokeStyle = grad; c.lineWidth = 2.2; c.globalAlpha = 1;
      c.beginPath(); c.moveTo(ax, ay); c.lineTo(hx2, hy2); c.stroke();
      /* the head */
      const hg = c.createRadialGradient(hx2, hy2, 0, hx2, hy2, 26);
      hg.addColorStop(0, "rgba(255,248,220,0.85)");
      hg.addColorStop(0.4, "rgba(255,236,180,0.30)");
      hg.addColorStop(1, "rgba(255,230,160,0)");
      c.fillStyle = hg;
      c.beginPath(); c.arc(hx2, hy2, 26, 0, TAU); c.fill();
      c.restore();
    }
    /* The focus in SCREEN space, left behind by the camera. Both the vignette
       and the burst are centred on it rather than on the middle of the hall --
       measured A/B: a full-frame scrim at 0.75 was invisible against an
       already-desaturated arena, and a full-frame additive flash at 0.55
       blew the whole picture to flat beige. Both failures had the same cause:
       treating the frame as the subject. The subject is the point of contact. */
    const fx = x + (this._cineFocus ? this._cineFocus[0] : w / 2);
    const fy = y + (this._cineFocus ? this._cineFocus[1] : h / 2);
    const R = Math.hypot(w, h) * 0.62;

    if (CINE.wash > 0.01){
      c.save();
      c.beginPath(); c.rect(x, y, w, h); c.clip();
      const g = c.createRadialGradient(fx, fy, R * 0.13, fx, fy, R);
      g.addColorStop(0, "rgba(6,4,12,0)");
      g.addColorStop(0.45, "rgba(6,4,12," + (0.30 * CINE.wash).toFixed(3) + ")");
      g.addColorStop(1, "rgba(4,3,9," + (0.86 * CINE.wash).toFixed(3) + ")");
      c.fillStyle = g; c.fillRect(x, y, w, h);
      c.restore();
    }

    if (CINE.flash > 0.01){
      c.save();
      c.beginPath(); c.rect(x, y, w, h); c.clip();
      c.globalCompositeOperation = "lighter";
      const g = c.createRadialGradient(fx, fy, 0, fx, fy, R * 0.52);
      const a = Math.min(0.38, CINE.flash * 0.38);
      g.addColorStop(0, "rgba(255,244,208," + a.toFixed(3) + ")");
      g.addColorStop(0.35, "rgba(255,236,180," + (a * 0.45).toFixed(3) + ")");
      g.addColorStop(1, "rgba(255,230,160,0)");
      c.fillStyle = g; c.fillRect(x, y, w, h);
      c.restore();
    }

    if (0){
    }

    if (CINE.bars > 0.01){
      const bh = h * 0.115 * CINE.bars;
      c.save();
      c.fillStyle = "#05040A";
      c.fillRect(x, y, w, bh); c.fillRect(x, y + h - bh, w, bh);
      c.globalAlpha = 0.5; c.strokeStyle = "#C9A22755"; c.lineWidth = 1;
      c.beginPath();
      c.moveTo(x, y + bh + 0.5); c.lineTo(x + w, y + bh + 0.5);
      c.moveTo(x, y + h - bh - 0.5); c.lineTo(x + w, y + h - bh - 0.5);
      c.stroke();
      c.restore();
    }
  }

  /* Radial smear, drawn inside the arena transform so it sits with the fight
     rather than on top of the letterbox. */
  drawCineStreaks(m){
    const c = this.ctx, s = CINE.streak;
    const fx = CINE.fx, fy = CINE.fy;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    for (let i = 0; i < 22; i++){
      const a = (i / 22) * TAU + (i % 3) * 0.14;
      const r0 = 70 + (i % 5) * 26, len = 120 + (i % 7) * 60 * s;
      c.globalAlpha = 0.05 + 0.10 * s * (0.4 + (i % 3) * 0.3);
      c.strokeStyle = i % 2 ? "#FFF4D0" : "#C9A227";
      c.lineWidth = 1.2 + (i % 3) * 1.1;
      c.beginPath();
      c.moveTo(fx + Math.cos(a) * r0, fy + Math.sin(a) * r0);
      c.lineTo(fx + Math.cos(a) * (r0 + len), fy + Math.sin(a) * (r0 + len));
      c.stroke();
    }
    c.restore();
  }

  /* ------------------------------------------------------------- arena --- */
  drawArena(m){"""

# --------------------------------------------------------------------------
# 3. the loop: the one line that makes all of it safe.
# --------------------------------------------------------------------------
LOOP_A = """    if (!window.__frozen){
      acc += raw * speed;
      const dt = CONFIG.physics.dt;
      let steps = 0;
      while (acc >= dt && steps < 40){ match.step(dt); acc -= dt; steps++; }
    }
    renderer.draw(match);"""
LOOP_B = """    /* CINEMA (demo). One loop body, in CINE.pump, shared with the offline
       clip renderer so the two cannot drift apart. It hands the accumulator
       WALL time scaled by the director; the sim still consumes it in identical
       CONFIG.physics.dt slices, so the sequence of steps -- and therefore the
       winner, the duration in match time, and every statistic -- is what it
       would have been at 1.0. Slowing the picture cannot slow the fight.

       `alpha` is how far the display clock sits between the last fixed step
       and the next one. At a 0.07x drop a step lands only every 7th rendered
       frame, so without this the world updates at 8 Hz behind a 60 Hz display
       and the slow motion visibly stutters. */
    const alpha = (typeof CINE !== "undefined")
      ? (window.__frozen ? 0 : CINE.pump(raw, match, speed))
      : (() => { if (window.__frozen) return 0;
                 acc += raw * speed; const dt = CONFIG.physics.dt; let n = 0;
                 while (acc >= dt && n < 40){ match.step(dt); acc -= dt; n++; }
                 return 0; })();
    if (typeof CINE !== "undefined" && alpha > 0) CINE.drawLerped(renderer, match, alpha);
    else renderer.draw(match);"""

# --------------------------------------------------------------------------
# 4. audio: splice the send between the SFX bus and the destination.
# --------------------------------------------------------------------------
AUD_A = """        this.bus = Sfx.buildChain(this.ctx, this.ctx.destination);"""
AUD_B = """        /* CINEMA (demo). The whole mix now lands on the director's send --
           a lowpass, a convolution hall and a duck -- instead of straight on
           the destination. With CINE off the send is flat and inaudible. */
        this.bus = Sfx.buildChain(this.ctx, CineAudio.build(this.ctx));"""

# --------------------------------------------------------------------------
# 5. newMatch: take a seed (so the same fight can be replayed with the
#    director off), run the prescan, and render the bed to tape.
# --------------------------------------------------------------------------
NEW_A = """function newMatch(idA, idB){
  if (idA === idB){
    const alts = WEAPONS.filter(w => w.id !== idA);
    idB = alts[Math.floor(Math.random()*alts.length)].id;
    selB.value = idB;
  }
  const seed = (Math.random() * 4294967296) >>> 0;
  match = new Match(idA, idB, seed);"""
NEW_B = """function newMatch(idA, idB, seedIn){
  if (idA === idB){
    const alts = WEAPONS.filter(w => w.id !== idA);
    idB = alts[Math.floor(Math.random()*alts.length)].id;
    selB.value = idB;
  }
  /* CINEMA (demo): an explicit seed, so the SAME fight can be replayed with
     the director off. That A/B is the whole argument -- if the two runs do not
     end identically, the feature is wrong. */
  const seed = seedIn !== undefined ? (seedIn >>> 0)
                                    : (Math.random() * 4294967296) >>> 0;
  window.__lastSeed = seed;
  match = new Match(idA, idB, seed);"""

BED_A = """  if (bedHandle){ bedHandle.stop(); bedHandle = null; }
  if (SFX.ctx){
    const t0 = SFX.ctx.currentTime;
    bedHandle = SFX.bed(t0, CONFIG.timeout + CONFIG.intro.dur + 6,
                        CONFIG.acts.slice(1).map(a => t0 + match.introT + a.t));
  }
  loggedCount = 0;"""
BED_B = """  if (bedHandle){ bedHandle.stop(); bedHandle = null; }
  CineAudio.stopBed();
  if (SFX.ctx){
    const dur = CONFIG.timeout + CONFIG.intro.dur + 6;
    const seals = CONFIG.acts.slice(1).map(a => match.introT + a.t);
    if (CINE.on && CINE.tape){
      /* CINEMA (demo). The score is pre-scheduled automation against real
         time, so slowing the sim cannot slow it -- during a set-piece the
         picture would drag while the music walked on, which is the commonest
         way this effect gets built wrong. So render the bed ONCE through an
         OfflineAudioContext using SFX.bed() unmodified, then play the result
         as one buffer whose playbackRate the director can ramp. The music now
         slows AND DROPS IN PITCH with the picture. */
      CineAudio.renderBed(dur, seals).then(buf => {
        if (buf && match && match.t < 1.0) bedHandle = CineAudio.startBed(buf);
        else if (!buf && SFX.ctx){
          const t0 = SFX.ctx.currentTime;
          bedHandle = SFX.bed(t0, dur, seals.map(t => t0 + t));
        }
      });
    } else {
      const t0 = SFX.ctx.currentTime;
      bedHandle = SFX.bed(t0, dur, seals.map(t => t0 + t));
    }
  }

  /* CINEMA (demo): watch the whole fight, then choose the shots. */
  CINE.reset();
  if (CINE.on){
    const p = cinePlan(idA, idB, seed);
    CINE.plan = p.cuts; CINE.scored = p.scored; CINE.planErr = p.err;
  } else { CINE.plan = []; CINE.scored = []; }
  if (window.__cinePanel) window.__cinePanel.refresh();

  loggedCount = 0;"""

SHELL_MARK = "/* ------------------------------------------------------------------ SHELL */"

TAIL_A = """newMatch(selA.value, selB.value);
requestAnimationFrame(frame);"""
TAIL_B = """newMatch(selA.value, selB.value);
requestAnimationFrame(frame);
__CINE_PANEL__"""


def build(src_path: pathlib.Path, out_path: pathlib.Path) -> None:
    src = src_path.read_text()
    module = (HERE / "_cinema_module.js").read_text()
    panel = (HERE / "_cinema_panel.js").read_text()

    if "CINEMA" in src and "CINE.update" in src:
        raise SystemExit("[cinema_build] input already patched")

    src = sub1(src, BEATS_INIT, BEATS_INIT_NEW, "Match ctor")
    src = sub1(src, NOTE_M, NOTE_M_NEW, "note()")
    src = sub1(src, HIT_A, HIT_B, "resolveHit")
    src = sub1(src, SHOT1_A, SHOT1_B, "shot origin")
    src = sub1(src, SHOT2_A, SHOT2_B, "ult shot origin")
    src = sub1(src, TICK_A, TICK_B, "shot context")
    src = sub1(src, ULT_A, ULT_B, "ultimate")
    src = sub1(src, CLANK_A, CLANK_B, "clank")
    src = sub1(src, CAM_A, CAM_B, "camera")
    src = sub1(src, OVER_A, OVER_B, "overlay calls")
    src = sub1(src, FILL_A, FILL_B, "arena bleed")
    src = sub1(src, OVER_M_A, OVER_M_B, "overlay methods")
    src = sub1(src, LOOP_A, LOOP_B, "frame loop")
    src = sub1(src, AUD_A, AUD_B, "audio send")
    src = sub1(src, FIN_A, FIN_B, "kill flash envelope")
    src = sub1(src, NEW_A, NEW_B, "newMatch seed")
    src = sub1(src, BED_A, BED_B, "bed")
    src = sub1(src, SHELL_MARK, module + "\n\n" + SHELL_MARK, "module insert")
    src = sub1(src, TAIL_A, TAIL_B.replace("__CINE_PANEL__", panel), "panel insert")

    out_path.write_text(src)
    h = hashlib.sha256(src.encode()).hexdigest()
    nbytes = len(src.encode("utf-8"))
    print(f"[cinema_build] wrote {out_path}  {nbytes:,} bytes  sha256 {h[:16]}")


# --------------------------------------------------------------------------
# the check. Not "does it look right" -- does the director provably not touch
# the sim. Grep-level, cheap, and runs without a browser.
# --------------------------------------------------------------------------
FIN_A = """    if (m.finisher > 0){
      c.save();
      c.globalAlpha = Math.min(0.5, m.finisher * 0.5);"""
FIN_B = """    if (m.finisher > 0){
      c.save();
      /* THE KILL FLASH -- its own pass, and it applies with the director off
         too, because the problem predates the director.

         It was a full-frame #FFF4D0 at 0.5 alpha for a full second: about
         thirty frames of the picture washed flat beige at the exact moment the
         match is decided. Two faults, the same one twice. (1) The frame is not
         the subject -- the blow is, so this is now a radial burst centred on
         the relic that just died, bright at the point of impact and gone by
         the edges. (2) It lives in m.finisher, which decays with the SIM, so
         under a 0.24x set-piece the one second became four; while a cut runs
         it is clamped against the director's wall clock instead.

         Presentation only. m.finisher is read, never written. */
      const env = (typeof CINE !== "undefined" && CINE.on && CINE.cut)
        ? Math.min(CINE.wallFlash, m.finisher)
        : Math.min(1, m.finisher);
      const dead = m.loser || m.b;
      const kx = this.pad + dead.x * this.scale;
      const ky = this.arenaTop + dead.y * this.scale;
      const KR = Math.hypot(this.aw, this.ah) * 0.55;
      c.beginPath(); c.rect(this.pad, this.arenaTop, this.aw, this.ah); c.clip();
      c.globalCompositeOperation = "lighter";
      const kg = c.createRadialGradient(kx, ky, 0, kx, ky, KR);
      const ka = Math.min(0.46, env * 0.46);
      kg.addColorStop(0, "rgba(255,244,208," + ka.toFixed(3) + ")");
      kg.addColorStop(0.30, "rgba(255,240,196," + (ka * 0.42).toFixed(3) + ")");
      kg.addColorStop(1, "rgba(255,232,170,0)");
      c.fillStyle = kg;
      c.fillRect(this.pad, this.arenaTop, this.aw, this.ah);
      c.restore();
    }
    if (0){
      c.save();
      c.globalAlpha = 0;"""

SHOT1_A = """      x: f.x + ca * (R + reach), y: f.y + sa * (R + reach),
      vx: ca * S.speed, vy: sa * S.speed,"""
SHOT1_B = """      x: f.x + ca * (R + reach), y: f.y + sa * (R + reach),
      /* CINEMA (demo): where it was loosed from, and how fast the archer was
         moving at the time. Dead data as far as the sim is concerned -- nothing
         reads it but the director, which prices a long shot by how far the bolt
         actually travelled rather than by what it hit. */
      x0: f.x, y0: f.y, spd0: f.speed, t0: this.t,
      vx: ca * S.speed, vy: sa * S.speed,"""

SHOT2_A = """      x: f.x + ca * (R + reach), y: f.y + sa * (R + reach),
      vx: ca * v, vy: sa * v,"""
SHOT2_B = """      x: f.x + ca * (R + reach), y: f.y + sa * (R + reach),
      x0: f.x, y0: f.y, spd0: f.speed, t0: this.t,           // CINEMA (demo)
      vx: ca * v, vy: sa * v,"""

TICK_A = """        this.shotHits++;
        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul);"""
TICK_B = """        this.shotHits++;
        /* CINEMA (demo): resolveHit does not take the projectile, and the
           director needs to know the bolt's flight to price the shot. Handed
           over on the instance for the duration of the call and cleared
           immediately, so nothing can read a stale one. */
        this._cineShot = s;
        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul);
        this._cineShot = null;"""

FORBIDDEN = [
    (r"CINE[^\n]*\.hp\s*=", "director writes hp"),
    (r"CINE[^\n]*\.hitStop\s*=", "director writes hitStop"),
    (r"CINE[^\n]*\.rng", "director touches the RNG"),
    (r"CINE[^\n]*match\.step", "director steps the sim"),
]


def check(path: pathlib.Path) -> int:
    src = path.read_text()
    bad = []
    for pat, why in FORBIDDEN:
        for mo in re.finditer(pat, src):
            bad.append(f"  {why}: {src[max(0,mo.start()-40):mo.end()+20]!r}")

    # The module may only be reached through these three surfaces.
    if "CINE.pump(raw, match, speed)" not in src:
        bad.append("  frame loop is not routed through CINE.pump")
    if "CINE.drawLerped" not in src:
        bad.append("  draw is not routed through the interpolator")
    if "CINE.zoom" not in src:
        bad.append("  camera hook missing")

    # Anything inside the Match class that mentions CINE is a smell: the sim is
    # supposed to be unaware the director exists.
    # Bound the slice at the NEXT top-level class, not at simulate() -- the
    # Renderer sits between them and the renderer is allowed to know.
    mstart = src.index("\nclass Match {")
    mend = src.index("\nclass ", mstart + 1)
    body = src[mstart:mend]
    # Identifier use, not the word in a comment: `CINE.` / `CINE[` / `CineAudio.`
    ref = re.findall(r"\b(?:CINE|CineAudio)\s*[.\[(]", body)
    if ref:
        bad.append(f"  the sim references the director: {ref[:3]}")

    print(f"[cinema_build] check {path.name}")
    print(f"  beats emitted from sim : {body.count('this.beat(')}")
    print(f"  director -> sim writes : {len(bad)}")
    for b in bad:
        print(b)
    print("  RESULT:", "FAIL" if bad else "PASS")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="sc-sil.html")
    ap.add_argument("--out", dest="out", default="sc-cinema.html")
    ap.add_argument("--check", dest="check", default=None)
    a = ap.parse_args()
    if a.check:
        return check(pathlib.Path(a.check))
    build(pathlib.Path(a.src), pathlib.Path(a.out))
    return check(pathlib.Path(a.out))


if __name__ == "__main__":
    sys.exit(main())
