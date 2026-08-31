  /* THE DEADFALL'S SIGILS, ON THE FLOOR OF THE HALL.

     Rick's §1: "the hit leaves behind an echo bomb (thinking a pentagram
     imprinted on the battlefield) the echos slowly begin to crackle with the
     same purple electricity."

     ── THE ONE THING THIS PICTURE HAS TO DO ────────────────────────────────

     ARMED MUST NOT LOOK LIKE ARMING. v52 §3c: with a fuse the crackle was a
     COUNTDOWN and the tension was time; with a mine it is an ARMING animation
     and the tension is space. A viewer who cannot tell a live sigil from a
     crackling one cannot see the mechanic at all — the hall just has purple
     marks on it — and every number in `06-docs/v52/echoes-v52.md` is then
     measuring something nobody can watch. It is the F3 gate and it is the
     only check in this stage no tool can run.

     So the two states are made different in FOUR ways at once, because any
     one of them can be lost to a small phone screen, to the bloom, or to a
     dark frame:

       ARMING   incomplete   the ring and the star are DRAWN IN over `arm`
                             seconds, so the figure is visibly unfinished
                flickering   every stroke jitters off `shellHash` per frame
                dim          no node lamps, thin lines, low alpha
                loose        crackle arcs jump BETWEEN the points, unattached

       ARMED    complete     the figure closes, and it closes with a SNAP —
                             a one-off flare at the instant it goes live
                steady       the jitter stops dead. Stillness is the tell.
                lit          each live charge carries a lamp at its own radius
                bound        the star lines are solid and the ring is filled

     THE SNAP IS THE MOST IMPORTANT FRAME. A state change a viewer misses is
     a state change that did not happen, and the sigil is on the floor behind
     two moving balls; it will not be looked at unless something makes it
     worth looking at.

     ── AND IT MUST NOT READ AS CONVERSE ────────────────────────────────────

     v52 §4. Foregone already puts sigils on this floor and blooms them, so
     the two floor-marking ultimates in the game have to be told apart at a
     glance: Converse is runic BLUE, drawn as a route the caster walked, and
     it detonates in a sweep. This is umbral PURPLE, drawn as discrete closed
     figures stamped where blood was drawn, and it waits.

     ── THE POSITIONS ARE THE SIMULATION'S ──────────────────────────────────

     Nothing here recomputes where a charge is. `g.ch[i].x/y` is what the
     proximity test in `tickDeadfall` reads, so the drawn node and the live
     trigger are the same number — the class of bug CLAUDE.md §4.1 exists for
     is not available to this block. */
  drawSigils(m){
    const S = m.sigils;
    if (!S || !S.length) return;
    const c = this.ctx, A = AFFINITIES.umbral;
    for (const g of S){
      const armed = g.t >= g.arm;
      const frac  = armed ? 1 : clamp(g.t / g.arm, 0, 1);
      /* THE SNAP: 0.32s of flare on the frame the figure goes live, and it is
         the only thing in this block that is loud. */
      const snap  = armed ? clamp(1 - (g.t - g.arm) / 0.32, 0, 1) : 0;
      const live  = [];
      for (const ch of g.ch) if (!ch.dead) live.push(ch);
      if (!live.length) continue;
      /* the flicker is a per-FRAME hash on a arming figure and is frozen the
         instant it arms. Stillness is what says "this is now a thing that
         happens to you". */
      const fl = armed ? 0 : (shellHash(g.seed + 7, (g.t * 34) | 0) - 0.5) * 2;

      c.save();
      c.globalCompositeOperation = "lighter";

      /* ---- the ring the charges sit on -------------------------------- */
      /* ARMING WAS 0.16 AND THAT WAS NOT DIM, IT WAS INVISIBLE. Photographed
         off a real match at 19.8s (`deadfall_sheet.py`), the crackling figure
         did not read at all against the arena's own gold motif -- so the
         viewer saw sigils APPEAR already live, and the arming beat, which is
         the whole tension of a mine, did not exist on screen. The two states
         are separated by SHAPE, MOTION and COLOUR here; darkness was doing
         none of that work and was hiding one of them. */
      c.globalAlpha = armed ? 0.34 + 0.10 * Math.sin(g.t * 2.4) + snap * 0.5
                            : (0.34 + 0.22 * frac) * (0.75 + fl * 0.25);
      c.strokeStyle = A.core;
      c.lineWidth = armed ? 2.4 + snap * 2.6 : 1.6;
      c.beginPath();
      c.arc(g.x, g.y, g.ring, -Math.PI / 2, -Math.PI / 2 + TAU * frac);
      c.stroke();

      /* ---- the star: point i to point i+2, which is what makes it a
              pentagram rather than a pentagon ------------------------------ */
      const N = g.ch.length;
      for (let i = 0; i < N; i++){
        const a = g.ch[i], b = g.ch[(i + 2) % N];
        /* A SPENT NODE TAKES ITS LINES WITH IT. The figure comes apart as it
           is walked through, so what is left on the floor is a count of what
           is left to walk into — the state of the trap, drawn as the trap. */
        if (a.dead || b.dead) continue;
        const seg = clamp((frac - i / (N * 1.6)) * 2.2, 0, 1);
        if (seg <= 0) continue;
        c.globalAlpha = armed ? 0.55 + snap * 0.45 : 0.30 + 0.28 * frac;
        /* AND THE FIGURE IS UMBRAL PURPLE, NOT WHITE. `A.glow` is #DDB8FF and
           over a bright ball it reads as white -- which is the one thing v52
           §4 says these must not do, because Foregone's Converse already puts
           lines on this floor and the two floor-marking ultimates have to be
           told apart at a glance. The core colour carries the figure; the
           near-white is spent only on the lamps. */
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

      /* ---- the charges themselves ------------------------------------- */
      for (let i = 0; i < N; i++){
        const ch = g.ch[i];
        if (ch.dead) continue;
        if (armed){
          /* THE LAMP IS DRAWN AT THE CHARGE'S OWN TRIGGER RADIUS, faintly, so
             the ground a viewer must not walk on is the ground that is lit.
             Nothing else in this game draws its own hit box; this one has to,
             because the hit box IS the mechanic. */
          const pulse = 0.5 + 0.5 * Math.sin(g.t * 3.1 + i * 1.26);
          c.globalAlpha = 0.10 + 0.05 * pulse + snap * 0.22;
          const gr = c.createRadialGradient(ch.x, ch.y, 1, ch.x, ch.y, g.rad);
          gr.addColorStop(0, A.core + "AA");
          gr.addColorStop(0.55, A.core + "44");
          gr.addColorStop(1, A.core + "00");
          c.fillStyle = gr;
          c.beginPath(); c.arc(ch.x, ch.y, g.rad, 0, TAU); c.fill();

          c.globalAlpha = 0.85 + snap * 0.15;
          c.fillStyle = A.glow;
          c.shadowColor = A.core; c.shadowBlur = 12 + snap * 22;
          c.beginPath();
          c.arc(ch.x, ch.y, 3.4 + pulse * 1.1 + snap * 3.0, 0, TAU);
          c.fill();
          c.shadowBlur = 0;
        } else {
          /* arming: a spark being coaxed into existence, and the crackle is
             UNATTACHED — it jumps between the points that are not there yet */
          c.globalAlpha = (0.45 + 0.3 * frac) * (0.6 + 0.4 * Math.abs(fl));
          c.fillStyle = A.core;
          c.beginPath();
          c.arc(ch.x, ch.y, 1.6 + frac * 1.6, 0, TAU);
          c.fill();
          if (i % 2 === 0 && frac > 0.15){
            const nb = g.ch[(i + 1) % N];
            c.globalAlpha = (0.20 + 0.30 * frac) * Math.abs(fl);
            c.strokeStyle = A.glow; c.lineWidth = 1.0;
            this._jag(c, ch.x, ch.y, nb.x, nb.y, 6, 9,
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

