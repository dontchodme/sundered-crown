  /* THE DEADFALL'S SIGILS, ON THE FLOOR OF THE HALL.

     Rick's §1: "the hit leaves behind an echo bomb (thinking a pentagram
     imprinted on the battlefield) the echos slowly begin to crackle with the
     same purple electricity."

     ── ONE FIGURE IS ONE MINE, AND THAT IS RICK OFF THE FIRST BUILD ────────

     The first cut made the pentagram five charges on a ring, because v52 §3b
     measured the ring as the only arrangement that produces a chain: five
     points 60 units apart set off 5.7 of each other, where one bomb a blow
     chains 0.25 times a fight and is not a chain at all.

     He watched it and said the thing the numbers could not:

         "i can tell the difference between armed and arming pretty easily.
          but what isnt legible is the explosion itself. currently each
          pentagram spawns a bunch of mini bombs. not opposed to this
          direction but my vision was the pentagram was 1 large mine not a
          cluster of small ones."

     Five charges at `stamp/5` put five 3-damage numbers over the ball across
     42 milliseconds. That reads as noise, and no probe could tell you so: the
     damage, the win rate, the chain counters and the beats were all correct.

     **So the drawn figure IS the hit box now.** Five points because a
     pentagram has five points, one trigger, one blast, one number. The chain
     that survives is FIGURE TO FIGURE — a shove out of one mine into the next
     one standing on the floor — which is a chain a viewer can actually follow,
     because each link is a whole explosion.

     ── THE ONE THING THIS PICTURE HAS TO DO ────────────────────────────────

     ARMED MUST NOT LOOK LIKE ARMING. v52 §3c: with a fuse the crackle was a
     COUNTDOWN and the tension was time; with a mine it is an ARMING animation
     and the tension is space. Rick confirmed off the first build that this
     reads, so the four separations below are KEPT AS THEY ARE and nothing in
     this rework is allowed to weaken them:

       ARMING   incomplete   the ring and the star are DRAWN IN over `arm`
                             seconds, so the figure is visibly unfinished
                flickering   every stroke jitters off `shellHash` per frame
                loose        crackle arcs jump BETWEEN the points, unattached
                thin         no core, no lit ground

       ARMED    complete     the figure closes, and it closes with a SNAP
                steady       the jitter stops dead. Stillness is the tell.
                bound        solid star lines
                lit          ONE core at the centre — the mine itself — and
                             the ground it covers, out to `rad`

     ── AND IT MUST NOT READ AS CONVERSE ────────────────────────────────────

     v52 §4. Foregone already puts sigils on this floor and blooms them, so the
     two floor-marking ultimates have to be told apart at a glance: Converse is
     runic BLUE, drawn as a route the caster walked, detonated in a sweep. This
     is umbral PURPLE, discrete closed figures stamped where blood was drawn,
     and it waits. The figure is stroked in `A.core` and never in `A.glow`:
     #DDB8FF over a bright ball reads as WHITE, which is the one thing these
     must not do.

     ── THE POSITIONS ARE THE SIMULATION'S ──────────────────────────────────

     Nothing here recomputes where anything is. `g.x/g.y` is what the proximity
     test in `tickDeadfall` reads and `g.rad` is the radius it reads it at, so
     the lit ground and the live trigger are the same number. The class of bug
     CLAUDE.md §4.1 exists for is not available to this block. */
  drawSigils(m){
    const c = this.ctx, A = AFFINITIES.umbral;

    /* ---- THE BLAST, FIRST, so a live figure draws over it ---------------
       A mine that simply vanished on the frame it fired was the whole of
       Rick's complaint: the explosion has to be the loudest thing the
       ultimate does, and the figure is what explodes. So the pentagram
       leaves by BECOMING the blast — it expands, thickens, whitens and goes.
       Presentation only, aged on `m.sigilFlash` beside `rings` and `floats`,
       and nothing in the simulation reads it. */
    const F = m.sigilFlash;
    if (F && F.length){
      for (const b of F){
        const u = clamp(b.t / b.life, 0, 1);
        const k = 1 - u;
        const sc = 1 + u * 1.35;
        c.save();
        c.globalCompositeOperation = "lighter";
        /* the shock out to the trigger radius — the ground it actually
           covered, drawn once, so the size of the mine is stated at the one
           moment a viewer is looking straight at it */
        c.globalAlpha = k * k * 0.55;
        c.strokeStyle = A.glow;
        c.lineWidth = 3 + k * 7;
        c.beginPath();
        c.arc(b.x, b.y, b.rad * (0.35 + u * 0.85), 0, TAU);
        c.stroke();
        /* and the figure itself, thrown outward */
        c.globalAlpha = k * 0.95;
        c.strokeStyle = u < 0.45 ? "#FFFFFF" : A.glow;
        c.lineWidth = 2 + k * 3.5;
        c.shadowColor = A.core; c.shadowBlur = 24 * k;
        const N = b.pts.length;
        c.beginPath();
        for (let i = 0; i < N; i++){
          const p = b.pts[(i * 2) % N];
          const x = b.x + (p.x - b.x) * sc, y = b.y + (p.y - b.y) * sc;
          i ? c.lineTo(x, y) : c.moveTo(x, y);
        }
        c.closePath(); c.stroke();
        c.beginPath();
        c.arc(b.x, b.y, b.ring * sc, 0, TAU);
        c.stroke();
        c.shadowBlur = 0;
        c.restore();
      }
    }

    const S = m.sigils;
    if (!S || !S.length) return;
    for (const g of S){
      const armed = g.t >= g.arm;
      const frac  = armed ? 1 : clamp(g.t / g.arm, 0, 1);
      /* THE SNAP: 0.32s of flare on the frame the figure goes live. */
      const snap  = armed ? clamp(1 - (g.t - g.arm) / 0.32, 0, 1) : 0;
      /* the flicker is a per-FRAME hash on an arming figure and is frozen the
         instant it arms. Stillness is what says "this is now a thing that
         happens to you". */
      const fl = armed ? 0 : (shellHash(g.seed + 7, (g.t * 34) | 0) - 0.5) * 2;
      const P = g.pts, N = P.length;

      c.save();
      c.globalCompositeOperation = "lighter";

      /* ---- THE GROUND THE MINE COVERS, out to its own trigger radius.
              ARMED ONLY, and faint. Nothing else in this game draws its own
              hit box; this one has to, because the hit box IS the mechanic
              and a viewer has to know which floor not to be standing on. */
      if (armed){
        const pulse = 0.5 + 0.5 * Math.sin(g.t * 2.6);
        c.globalAlpha = 0.09 + 0.05 * pulse + snap * 0.20;
        const gr = c.createRadialGradient(g.x, g.y, 1, g.x, g.y, g.rad);
        gr.addColorStop(0, A.core + "BB");
        gr.addColorStop(0.6, A.core + "3A");
        gr.addColorStop(1, A.core + "00");
        c.fillStyle = gr;
        c.beginPath(); c.arc(g.x, g.y, g.rad, 0, TAU); c.fill();
      }

      /* ---- the ring the figure is drawn on ---------------------------- */
      c.globalAlpha = armed ? 0.34 + 0.10 * Math.sin(g.t * 2.4) + snap * 0.5
                            : (0.34 + 0.22 * frac) * (0.75 + fl * 0.25);
      c.strokeStyle = A.core;
      c.lineWidth = armed ? 2.4 + snap * 2.6 : 1.6;
      c.beginPath();
      c.arc(g.x, g.y, g.ring, -Math.PI / 2, -Math.PI / 2 + TAU * frac);
      c.stroke();

      /* ---- the star: point i to point i+2, which is what makes it a
              pentagram rather than a pentagon ---------------------------- */
      for (let i = 0; i < N; i++){
        const a = P[i], b = P[(i + 2) % N];
        const seg = clamp((frac - i / (N * 1.6)) * 2.2, 0, 1);
        if (seg <= 0) continue;
        c.globalAlpha = armed ? 0.55 + snap * 0.45 : 0.30 + 0.28 * frac;
        c.strokeStyle = A.core;
        c.lineWidth = armed ? 2.4 + snap * 1.8 : 1.5;
        if (armed){
          c.beginPath(); c.moveTo(a.x, a.y); c.lineTo(b.x, b.y); c.stroke();
        } else {
          /* ARMING IS DRAWN, NOT SHOWN: the line grows and it wanders. */
          this._jag(c, a.x, a.y, b.x, b.y, 7, 5.5 + fl * 3,
                    g.seed * 13 + i, seg);
        }
      }

      /* ---- THE MINE. One core at the centre, and it is the whole of the
              difference from the first build: five lamps on a ring said five
              bombs, because that is what it was. */
      if (armed){
        const pulse = 0.5 + 0.5 * Math.sin(g.t * 3.1);
        c.globalAlpha = 0.9;
        c.fillStyle = "#FFFFFF";
        c.shadowColor = A.core; c.shadowBlur = 16 + pulse * 10 + snap * 26;
        c.beginPath();
        c.arc(g.x, g.y, 4.6 + pulse * 1.6 + snap * 4.0, 0, TAU);
        c.fill();
        c.shadowBlur = 0;
        c.globalAlpha = 0.5 + 0.3 * pulse;
        c.strokeStyle = A.glow; c.lineWidth = 1.6;
        c.beginPath();
        c.arc(g.x, g.y, 10 + pulse * 3.5 + snap * 8, 0, TAU);
        c.stroke();
      } else {
        /* arming: the points are sparks being coaxed into existence, and the
           crackle between them is UNATTACHED */
        for (let i = 0; i < N; i++){
          c.globalAlpha = (0.45 + 0.3 * frac) * (0.6 + 0.4 * Math.abs(fl));
          c.fillStyle = A.core;
          c.beginPath();
          c.arc(P[i].x, P[i].y, 1.6 + frac * 1.6, 0, TAU);
          c.fill();
          if (i % 2 === 0 && frac > 0.15){
            const nb = P[(i + 1) % N];
            c.globalAlpha = (0.20 + 0.30 * frac) * Math.abs(fl);
            c.strokeStyle = A.glow; c.lineWidth = 1.0;
            this._jag(c, P[i].x, P[i].y, nb.x, nb.y, 6, 9,
                      g.seed * 29 + i + ((g.t * 22) | 0), 1);
          }
        }
      }
      c.restore();
    }
  }

  /* THE CRACKLE, AND IT IS READ OFF THE FIGHTER RATHER THAN OFF `m.ultFx`.

     Rick's §1 opens "nightfell crackles with purple electricity ... for the
     duration of the ult", so this is not an event at the cast, it is the
     STATE the relic is in while its window is open -- and it is the only
     thing on screen that says the next blow will leave a figure behind.

     ── AND `m.ultFx` COULD NOT CARRY IT. MEASURED. ─────────────────────────

     `ultFx` is ONE SLOT on the match. The opponent casting anything at all
     overwrites it, and that cast's own `life` then expires and nulls it. Over
     four seeds an opponent, counting frames in which Nightfell's window was
     open:

         vs ironhail      0.0% of the window still showed this relic's fx
         vs bulwarden    20.8%
         vs twinshade    47.6%
         vs grudgebearer 57.5%
         vs axiom        97.9%
         vs emberedge    99.1%

     A window ultimate whose art is on `ultFx` is therefore INVISIBLE for most
     of its own window against half the roster, and nothing in this repo can
     see that: the sim is untouched, every probe is green and the win rate does
     not move by a thousandth. So the crackle hangs off `f.ultDeadfall` and
     `f.deadfallFade`, which belong to the fighter and cannot be taken away by
     somebody else's cast.

     ONE FUNCTION, DRAWN TWICE. `over` false is the ground it is standing on,
     under both balls; `over` true is the electricity on the shell, above
     them. Same shape as `drawVines(m, false/true)`, and for the same reason:
     the two halves are one effect and splitting them into two methods is how
     they drift apart. */
  drawCrackle(m, over){
    for (const f of [m.a, m.b]){
      const fade = f.deadfallFade;
      if (!(fade > 0.01)) continue;
      const c = this.ctx, A = f.aff, R = CONFIG.physics.ballR;
      /* the age of the window, in SIM seconds off the fighter's own clock --
         not the fx clock, which runs at 2x and is not this relic's to read */
      const t = f.ultDeadfall ? f.ultDeadfall.t : 0;
      if (!over){
        c.save();
        c.globalAlpha = 0.55 * fade;
        const g = c.createRadialGradient(f.x, f.y, R * 0.4, f.x, f.y, R * 3.1);
        g.addColorStop(0, "#2A0A4088"); g.addColorStop(0.55, "#1A063033");
        g.addColorStop(1, "#1A063000");
        c.fillStyle = g;
        c.beginPath(); c.arc(f.x, f.y, R * 3.1, 0, TAU); c.fill();
        /* the charge running to earth -- short arcs off the ball into the
           floor around it, re-seeded every frame so it never settles */
        c.globalCompositeOperation = "lighter";
        c.strokeStyle = A.core; c.lineWidth = 1.3;
        for (let i = 0; i < 4; i++){
          const fr = ((t * 14) | 0) * 4;
          const a = shellHash(71, i + fr) * TAU;
          const rr = R * (1.5 + shellHash(72, i + fr) * 1.5);
          c.globalAlpha = 0.34 * fade;
          this._jag(c, f.x, f.y, f.x + Math.cos(a) * rr,
                    f.y + Math.sin(a) * rr, 5, 6, 730 + i + fr, 1);
        }
        c.restore();
        continue;
      }
      /* WHAT IS DELIBERATELY NOT HERE: a wash, a disc, or anything with area.
         CLAUDE.md §4.1c -- alpha is invisible to the bloom and REACH is not --
         and this school has already blown the chain out once. Lightning is
         thin by nature, which is the whole reason it is safe to make bright. */
      const fr = (t * 18) | 0;                   // the crackle re-seeds fast
      c.save();
      c.globalCompositeOperation = "lighter";
      for (let i = 0; i < 5; i++){                    // arcs that hug the shell
        const a0 = shellHash(61, i + fr * 5) * TAU;
        const a1 = a0 + 0.7 + shellHash(62, i + fr * 5) * 1.5;
        const rr = R * (1.02 + shellHash(63, i + fr * 5) * 0.30);
        c.globalAlpha = fade * (0.45 + 0.45 * shellHash(64, i + fr * 5));
        c.strokeStyle = i % 2 ? A.glow : A.core;
        c.lineWidth = i % 2 ? 1.3 : 2.2;
        c.shadowColor = A.core; c.shadowBlur = 12;
        this._jag(c, f.x + Math.cos(a0) * rr, f.y + Math.sin(a0) * rr,
                  f.x + Math.cos(a1) * rr, f.y + Math.sin(a1) * rr,
                  7, 7, 640 + i + fr, 1);
      }
      c.shadowBlur = 0;
      for (let i = 0; i < 2; i++){         // and two that leave it entirely --
        const a = shellHash(65, i + fr * 2) * TAU;   // the relic is SHEDDING
        const rr = R * (1.9 + shellHash(66, i + fr * 2) * 1.1);
        c.globalAlpha = fade * 0.38;
        c.strokeStyle = A.glow; c.lineWidth = 1.1;
        this._jag(c, f.x + Math.cos(a) * R, f.y + Math.sin(a) * R,
                  f.x + Math.cos(a) * rr, f.y + Math.sin(a) * rr,
                  6, 9, 660 + i + fr, 1);
      }
      c.restore();
    }
  }

