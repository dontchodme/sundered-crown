"""REBUTTAL'S PICTURE (v70 section 6.1) as exactly-once edits to Lodestone's final link
(lodestone/links/sc-lodestone-b205.html, 6d736451a1ffc2df = the tip sc-tendril-t3 + stages 1-5).

rows() -> the deliverable rows (numbers inlined from PICK). There is NO lab variant of the rows: every
component is its own renderer method, so the harnesses hide one by replacing that method on the renderer
from outside the page, and the bytes measured are the bytes delivered. The silhouette candidates are the
one exception: SIL picks which head the rows carry (build(..., sil=...) writes a candidate page for the
lineup; the deliverable is PICK["SIL"]).

build(out)            -> ld-final.html  (the base + these rows: THE STAMP)
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "links" / "sc-lodestone-b205.html").resolve()

PICK = dict(
    DRAW=0.6,     # the cast: the rune chain lights outward from the caster's nearest wall, half-seconds (0.3s, v70 6.1)
    DARK=0.8,     # the close: the runes go dark from the far wall inward, half-seconds (0.4s, v70 6.1)
    DIE=0.2,      # the caster's fall: the whole chain goes out at once, half-seconds (0.1s)
    FLARE=0.3,    # a touch's flare, half-seconds (0.15s, v70 6.1)
    SPAN=60,      # the flare's span along the wall, units (v70 6.1)
    BOLT=0.0125,  # the wall-to-ball bar: the touch's step and the next on the MATCH clock (1.5 steps), so one frame of a 60 fps picture
    TRAIL=0.4,    # the rune-streak's length: the last 0.2s of the hurled ball's path, half-seconds
    TLIFE=0.8,    # a touch record's life (the streak fades over its second half), half-seconds (0.4s)
    NT=12,        # runes on the top and the floor
    NS=18,        # runes on each side wall
    ROFF=12,      # a rune's centre, units inside the wall line (under a ball that touches)
    RSZ=6.5,      # a rune's half-height, units
    MOTEN=28,     # rune motes shed off the lit walls (the design's field, drawn)
    MOTEP=3.2,    # a mote's cycle, half-seconds (1.6s)
    HSW=0.80,     # the square head's side, as a fraction of the weapon's art width
    SIL='"square"',
)


def src_text() -> str:
    return SRC.read_bytes().decode("utf-8")


def between(s: str, start: str, end: str) -> str:
    """The exact text from `start` up to (not including) `end`; both unique."""
    assert s.count(start) == 1, start
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j]


# ---------------------------------------------------------------------------
# 1. the fighter's picture state
FIGHTER_ANCHOR = "    this.ultRunes = null;\n    this.runeTally = null;\n"
FIGHTER_CODE = """    /* REBUTTAL'S PICTURE (v70 section 6.1), and none of it is the sim's: the
       walls go dark for 0.4s after `ultRunes` is gone (and `ultRunes` itself
       stays set through the verdict when a blow ends the match), and a
       touch's flare, bar and streak outlive the frame that touched, so the
       picture keeps its own state. On the FIGHTER and never on `m.ultFx`
       (one slot, and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation` (`tickLode`); nothing in the simulation reads any
       of it.
         lodeFade -- 1 while the walls are lit; eased to 0 as they go dark
         lodeAge  -- the presentation clock since the cast (the chain lights)
         lodeOut  -- the presentation clock since the close (the go-dark)
         lodeDie  -- 1 when the close was the caster's fall (all out at once)
         lodeU0   -- where the chain lit from: the caster's nearest wall at
                     the cast, as a fraction of the hall's loop (`lodeAt`)
         lodeU1   -- the same at the close: the dark runs from the far side
         lodeSeen -- `runeTally.touches` as last seen (a rise is a touch)
         lodeFx   -- a touch: its walls, its spot, the match time (the bar),
                     the hurled ball's path (the streak) */
    this.lodeFade = 0;
    this.lodeAge = 0;
    this.lodeOut = 0;
    this.lodeDie = 0;
    this.lodeU0 = 0;
    this.lodeU1 = 0;
    this.lodeSeen = 0;
    this.lodeFx = [];
"""

# ---------------------------------------------------------------------------
# 2. the presentation call
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickLode(dt);                  // REBUTTAL'S PICTURE (v70 section 6.1)\n"

# ---------------------------------------------------------------------------
# 3. the hall's loop (pure functions, read by the tick and the renderer)
HALL_ANCHOR = "function shellHash(a, b){\n"
HALL_CODE = """/* REBUTTAL'S WALLS (v70 section 6.1): the live hall's four walls as one loop,
   clockwise from the top-left corner; `u` is a fraction of its length. The
   hall is the CURRENT one (`m.inset`), so the runes walk in with the seals.
   Read by `tickLode` (where the caster stands at the cast and the close, and
   which walls a touch met) and by the renderer (where each rune sits). Pure
   functions of their arguments; nothing in the simulation calls them. */
function lodeHall(n){
  const A = CONFIG.arena, x0 = n, y0 = n, x1 = A.w - n, y1 = A.h - n;
  return { x0, y0, x1, y1, w: x1 - x0, h: y1 - y0, P: 2 * ((x1 - x0) + (y1 - y0)) };
}
/* -> [x, y, inward nx, ny, wall]: wall 0 the top, 1 the right, 2 the floor, 3 the left */
function lodeAt(G, u){
  let s = (((u % 1) + 1) % 1) * G.P;
  if (s < G.w) return [G.x0 + s, G.y0, 0, 1, 0];
  s -= G.w; if (s < G.h) return [G.x1, G.y0 + s, -1, 0, 1];
  s -= G.h; if (s < G.w) return [G.x1 - s, G.y1, 0, -1, 2];
  s -= G.w; return [G.x0, G.y1 - s, 1, 0, 3];
}
/* the point of `wall` level with (x, y), as u */
function lodeOn(G, wall, x, y){
  const cx = Math.min(G.x1, Math.max(G.x0, x)), cy = Math.min(G.y1, Math.max(G.y0, y));
  const s = wall === 0 ? cx - G.x0 : wall === 1 ? G.w + (cy - G.y0)
          : wall === 2 ? G.w + G.h + (G.x1 - cx) : 2 * G.w + G.h + (G.y1 - cy);
  return s / G.P;
}
/* the wall nearest (x, y) */
function lodeNear(G, x, y){
  const d = [y - G.y0, G.x1 - x, G.y1 - y, x - G.x0];
  let k = 0;
  for (let i = 1; i < 4; i++) if (d[i] < d[k]) k = i;
  return lodeOn(G, k, x, y);
}

"""

# ---------------------------------------------------------------------------
# 4. tickLode, after tickRunes
TICK_ANCHOR = "  tickWinnow(dt){\n"
TICK_CODE = """  /* ------------------------------------------------ REBUTTAL'S PICTURE ---
     v70 section 6.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): %DRAW% is the
     cast's 0.3s draw along the walls, %DARK% the close's 0.4s go-dark, %FLARE%
     a touch's 0.15s flare. The bar is timed on the MATCH clock (`t0`): it
     stands for the touch's step and the next -- one frame of a 60 fps
     picture -- and a hit stop that begins under it does not hold it.
     A TOUCH IS FOUND BY WATCHING `runeTally.touches` RISE, so `tickRunes`
     makes no call and keeps no record for the picture: this runs at the end
     of the step that touched (decay, after `checkEnd`), nothing between the
     touch test and here moves a ball, so the foe stands where the test found
     it, and the walls it met are the test's own sides read again (inset + R
     + pad; a corner meets two). THE WALLS ARE READ OFF `ultRunes && !over &&
     alive`: `tickRunes` never runs again once `over` is set and a blow's kill
     leaves `ultRunes` set through the verdict (v102 section 5), so the walls
     go dark at the kill -- from the far wall inward, or all at once when the
     caster is the one that fell. Writes presentation fields, `tags` and
     `taught` only, and draws no rng. */
  tickLode(dt){
    for (const f of [this.a, this.b]){
      const T = f.runeTally;
      if (!T && !(f.lodeFade > 0)) continue;                   // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      for (let i = f.lodeFx.length - 1; i >= 0; i--){
        const q = f.lodeFx[i];
        q.t += dt;
        if (q.t >= %TLIFE%){ f.lodeFx.splice(i, 1); continue; }
        /* the hurled ball's path, for the streak */
        const n = q.pts.length;
        if (foe.alive && q.t < %TLIFE% && n < 96
            && (foe.x !== q.pts[n - 3] || foe.y !== q.pts[n - 2])) q.pts.push(foe.x, foe.y, q.t);
      }
      const Z = (this.over || !f.alive) ? null : f.ultRunes;
      if (Z){
        if (!(f.lodeFade > 0) || f.lodeOut > 0){                 // a cast: the chain lights
          f.lodeAge = 0; f.lodeOut = 0; f.lodeDie = 0;
          f.lodeU0 = lodeNear(lodeHall(this.inset || 0), f.x, f.y);
        }
        f.lodeFade = 1;
        f.lodeAge += dt;
      } else if (f.lodeFade > 0){
        if (!(f.lodeOut > 0)){                                   // the close
          f.lodeU1 = lodeNear(lodeHall(this.inset || 0), f.x, f.y);
          f.lodeDie = f.alive ? 0 : 1;
        }
        f.lodeOut += dt;
        f.lodeFade = Math.max(0, 1 - f.lodeOut / (f.lodeDie ? %DIE% : %DARK%));
      }
      if (!T) continue;
      if (T.touches > f.lodeSeen){
        f.lodeSeen = T.touches;
        /* THE TOUCH. Not on the kill's step: the shatter owns that frame. */
        if (this.over || !foe.alive) continue;
        const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset || 0, e = f.w.ult.pad;
        const G = lodeHall(n), walls = [];
        if (foe.y <= n + R + e)       walls.push(0);
        if (foe.x >= A.w - n - R - e) walls.push(1);
        if (foe.y >= A.h - n - R - e) walls.push(2);
        if (foe.x <= n + R + e)       walls.push(3);
        f.lodeFx.push({ k: T.touches, walls, x: foe.x, y: foe.y, t: 0, t0: this.t, pts: [foe.x, foe.y, 0] });
        if (f.lodeFx.length > 6) f.lodeFx.shift();
        /* THE HEX TAG WITH ITS COUNT (v70 6.1: "the hex tag on the foe prints
           its count"), on every touch. ONE HEX TAG ON THE FOE AT A TIME
           (Tendril's rule): the hammer's own blow tags hex too (`resolveHit`),
           so a tag already up there takes the new count in place instead of
           a second printing over it. */
        if (foe.hp > 0){
          const k = foe.stacks("hex");
          const g = this.tags.find(g2 => g2.key === "hex" && !g2.first && g2.life > 0.3
                                         && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
          if (g) g.val = k;
          else {
            const first = !this.taught.hex && !!STATUS.hex.tip;
            if (first) this.taught.hex = true;
            this.statusTag(foe.x, foe.y, "hex", first, k);
          }
        }
      }
    }
  }

"""

# ---------------------------------------------------------------------------
# 5. the world call under both balls
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* REBUTTAL'S WALLS (v70 section 6.1): the rune chain on the live hall's
       walls, its motes, a touch's flare and the hurled ball's rune-streak.
       The WORLD pass and under both balls -- a ball on a wall stands on the
       runes it touched (CLAUDE.md section 4.1b), and none of it reaches the
       bloom (section 4.1c). */
    if (__world) this.drawLode(m);
"""

# ---------------------------------------------------------------------------
# 6. the world call over both fighters
TOP_ANCHOR = "    this.drawTreeTop(m);\n"
TOP_CODE = """    /* REBUTTAL'S BAR, over both fighters: it snaps from the wall INTO the
       ball it hexes. World pass, one frame. */
    this.drawLodeTop(m);
"""

# ---------------------------------------------------------------------------
# 7. the head's rune while the walls are lit, in drawWeapon
HEAD_ANCHOR = "        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);\n      }\n"
HEAD_CODE = """      /* REBUTTAL (v70 section 6.1): the hammer's head carries a rune while
         the walls are lit, in the shape's own frame, over the shape. Zero on
         every other relic, so this is a comparison on a field nothing else
         writes. */
      if (f.lodeFade > 0) this._lodeHead(f, reach + 6);
"""

# ---------------------------------------------------------------------------
# 8. the drawing methods
DRAW_ANCHOR = "  drawMotes(m){\n"
DRAW_CODE = """  /* ------------------------------------------------ REBUTTAL'S PICTURE ---
     v70 section 6.1. THE WALLS: a rune chain on the live hall's four walls
     (the school's core on the wall line, %NT% runes on the top and the floor
     and %NS% down each side, %ROFF% units in, so a ball touching a wall
     stands on them). THE CAST lights it outward from the caster's nearest
     wall over 0.3s -- the near wall, the two beside it, the far one last --
     and it stays lit for the window, shedding rune motes (the design's
     field, drawn: `fx.js` fires once, at the cast, on the one ultFx slot).
     A TOUCH flares the %SPAN%-unit span of wall under the foe in the glow for
     0.15s, a bar snaps from the wall into the ball for one frame, and the
     ball leaves on a rune-streak. THE CLOSE runs dark from the far wall
     inward over 0.4s; the caster's fall puts it out at once.
     No new object in the hall: everything is on the walls or the foe. The
     WORLD pass, source-over; no rng, no spawnFx, no Math.random. */
  drawLode(m){
    for (const f of [m.a, m.b]){
      if (!(f.lodeFade > 0) && !(f.lodeFx && f.lodeFx.length)) continue;   // <- zero burden
      const G = lodeHall(m.inset || 0), P = f.aff;
      if (f.lodeFade > 0){ this._lodeWalls(m, f, G, P); this._lodeMotes(m, f, G, P); }
      if (f.lodeFx.length){ this._lodeFlare(m, f, G, P); this._lodeStreak(m, f, P); }
    }
  }

  drawLodeTop(m){
    for (const f of [m.a, m.b]){
      if (!(f.lodeFx && f.lodeFx.length)) continue;                         // <- zero burden
      this._lodeBolt(m, f, lodeHall(m.inset || 0), f.aff);
    }
  }

  /* How lit the rune at `u` is: the cast's front runs out from `lodeU0` both
     ways round the loop, the close's runs back from the far side to `lodeU1`,
     each with a soft edge 2% of the loop long. */
  _lodeLit(f, u){
    if (f.lodeOut > 0){
      if (f.lodeDie) return f.lodeFade;
      const d = Math.abs(u - f.lodeU1), dd = Math.min(d, 1 - d);
      const front = 0.52 * (1 - Math.min(1, f.lodeOut / %DARK%));
      return clamp((front - dd) / 0.02, 0, 1);
    }
    const k = Math.min(1, f.lodeAge / %DRAW%), front = 0.52 * (1 - (1 - k) * (1 - k));
    const d = Math.abs(u - f.lodeU0), dd = Math.min(d, 1 - d);
    return clamp((front - dd) / 0.02, 0, 1);
  }

  /* A rune: one of six staves, in a unit box, `up` away from its wall. */
  _lodeRunePath(c, j){
    c.beginPath();
    switch (j % 6){
      case 0: c.moveTo(0, 1); c.lineTo(0, -1); c.moveTo(0, -0.15); c.lineTo(-0.62, -0.9);
              c.moveTo(0, -0.15); c.lineTo(0.62, -0.9); break;
      case 1: c.moveTo(-0.3, 1); c.lineTo(-0.3, -1); c.moveTo(-0.3, -0.5); c.lineTo(0.45, 0);
              c.lineTo(-0.3, 0.5); break;
      case 2: c.moveTo(0, -1); c.lineTo(0.62, 0); c.lineTo(0, 1); c.lineTo(-0.62, 0); c.closePath(); break;
      case 3: c.moveTo(-0.6, -1); c.lineTo(0.6, 1); c.moveTo(0.6, -1); c.lineTo(-0.6, 1); break;
      case 4: c.moveTo(0, 1); c.lineTo(0, -1); c.moveTo(-0.62, -0.38); c.lineTo(0, -1); c.lineTo(0.62, -0.38); break;
      default: c.moveTo(0.5, -1); c.lineTo(-0.4, -0.3); c.lineTo(0.4, 0.3); c.lineTo(-0.5, 1);
    }
  }

  /* Each rune's place: [u, x, y, inward nx, ny, index, wall, along]. %NT% a
     wall on the top and the floor, %NS% on each side, spaced over the CURRENT
     hall, `up` pointing into it. */
  _lodeRunes(G){
    const out = [];
    let j = 0;
    for (let wall = 0; wall < 4; wall++){
      const N = wall % 2 ? %NS% : %NT%, len = wall % 2 ? G.h : G.w;
      const s0 = wall === 0 ? 0 : wall === 1 ? G.w : wall === 2 ? G.w + G.h : 2 * G.w + G.h;
      for (let i = 0; i < N; i++, j++){
        const u = (s0 + len * (i + 0.5) / N) / G.P, p = lodeAt(G, u);
        out.push([u, p[0] + p[2] * %ROFF%, p[1] + p[3] * %ROFF%, p[2], p[3], j, wall,
                  wall % 2 ? p[1] : p[0]]);
      }
    }
    return out;
  }

  _lodeWalls(m, f, G, P){
    const c = this.ctx, full = !(f.lodeOut > 0) && f.lodeAge >= %DRAW%;
    const a0 = f.lodeDie ? f.lodeFade : 1;
    const X0 = G.x0 + 2, Y0 = G.y0 + 2, X1 = G.x1 - 2, Y1 = G.y1 - 2;
    const K = [[X0, Y0], [X1, Y0], [X1, Y1], [X0, Y1]];
    c.save();
    c.lineJoin = "round";
    /* the chain: a soft band and a hard line on the wall, 2 units in; while
       it lights or goes dark, in pieces two to a rune, each as lit as the
       loop is at its middle */
    const band = (w, col, al) => {
      c.strokeStyle = col; c.lineWidth = w;
      if (full){ c.globalAlpha = al; c.strokeRect(X0, Y0, X1 - X0, Y1 - Y0); return; }
      c.lineCap = "butt";
      for (let wall = 0; wall < 4; wall++){
        const N = 2 * (wall % 2 ? %NS% : %NT%), A0 = K[wall], A1 = K[(wall + 1) % 4];
        for (let i = 0; i < N; i++){
          const xa = A0[0] + (A1[0] - A0[0]) * i / N, ya = A0[1] + (A1[1] - A0[1]) * i / N;
          const xb = A0[0] + (A1[0] - A0[0]) * (i + 1) / N, yb = A0[1] + (A1[1] - A0[1]) * (i + 1) / N;
          const lit = this._lodeLit(f, lodeOn(G, wall, (xa + xb) / 2, (ya + yb) / 2));
          if (lit < 0.01) continue;
          c.globalAlpha = al * lit;
          c.beginPath(); c.moveTo(xa, ya); c.lineTo(xb, yb); c.stroke();
        }
      }
    };
    band(9, P.core, 0.13 * a0);
    band(2.2, P.core, 0.75 * a0);
    c.lineCap = "round";
    /* the runes */
    const RS = %RSZ%;
    for (const q of this._lodeRunes(G)){
      const lit = full ? 1 : this._lodeLit(f, q[0]);
      if (lit < 0.01) continue;
      c.save();
      c.translate(q[1], q[2]); c.rotate(Math.atan2(q[3], -q[4]));
      c.scale(RS, RS);
      c.globalAlpha = lit * a0;
      this._lodeRunePath(c, Math.floor(shellHash(9951, q[5]) * 6));
      c.strokeStyle = P.dark; c.lineWidth = 3.6 / RS; c.stroke();
      c.strokeStyle = P.core; c.lineWidth = 1.7 / RS; c.stroke();
      c.restore();
    }
    /* the draw's leading edge: a spark running out along the wall each way */
    if (!(f.lodeOut > 0) && f.lodeAge < %DRAW%){
      const k = f.lodeAge / %DRAW%, front = 0.52 * (1 - (1 - k) * (1 - k)) - 0.01;
      for (const sg of [-1, 1]){
        const p = lodeAt(G, f.lodeU0 + sg * Math.min(0.5, front));
        c.globalAlpha = 1;
        c.fillStyle = P.glow; c.beginPath(); c.arc(p[0] + p[2] * 2, p[1] + p[3] * 2, 4.2, 0, TAU); c.fill();
        c.fillStyle = "#FFFFFF"; c.beginPath(); c.arc(p[0] + p[2] * 2, p[1] + p[3] * 2, 1.8, 0, TAU); c.fill();
      }
    }
    c.restore();
  }

  /* THE FIELD, DRAWN: motes shed off the lit walls and drifting a little way
     into the hall, %MOTEN% of them, each on its own place and phase by
     shellHash on its index against the window's presentation clock. */
  _lodeMotes(m, f, G, P){
    const c = this.ctx, a0 = f.lodeDie ? f.lodeFade : 1;
    c.save();
    c.fillStyle = P.glow;
    for (let i = 0; i < %MOTEN%; i++){
      const u = shellHash(9961, i), lit = this._lodeLit(f, u);
      if (lit < 0.01) continue;
      const k = ((f.lodeAge + f.lodeOut) / %MOTEP% + shellHash(9963, i)) % 1;
      const p = lodeAt(G, u), tx = -p[3], ty = p[2], dr = (shellHash(9965, i) - 0.5) * 18 * k;
      const d = 5 + 26 * k;
      c.globalAlpha = 0.8 * Math.sin(Math.PI * k) * lit * a0;
      c.beginPath();
      c.arc(p[0] + p[2] * d + tx * dr, p[1] + p[3] * d + ty * dr, 1.3 + 0.9 * shellHash(9967, i), 0, TAU);
      c.fill();
    }
    c.restore();
  }

  /* A TOUCH'S FLARE: the %SPAN%-unit span of each wall the foe met, level
     with it (kept whole on its own wall), in the glow, source-over, 0.15s. */
  _lodeFlare(m, f, G, P){
    const c = this.ctx, H = %SPAN% / 2;
    c.save();
    c.lineCap = "round";
    const runes = this._lodeRunes(G);
    for (const q of f.lodeFx){
      if (q.t >= %FLARE%) continue;
      const k = q.t / %FLARE%, a = k < 0.12 ? 0.55 + 0.45 * k / 0.12 : 1 - (k - 0.12) / 0.88;
      for (const wall of q.walls){
        const side = wall % 2, lo = side ? G.y0 : G.x0, hi = side ? G.y1 : G.x1;
        const s = Math.max(lo + H, Math.min(hi - H, side ? q.y : q.x));
        const wx = wall === 1 ? G.x1 : G.x0, wy = wall === 2 ? G.y1 : G.y0;
        const nx = wall === 1 ? -1 : wall === 3 ? 1 : 0, ny = wall === 0 ? 1 : wall === 2 ? -1 : 0;
        const ax = side ? wx : s - H, ay = side ? s - H : wy, bx = side ? wx : s + H, by = side ? s + H : wy;
        c.globalAlpha = 0.35 * a; c.strokeStyle = P.core; c.lineWidth = 16;
        c.beginPath(); c.moveTo(ax + nx * 5, ay + ny * 5); c.lineTo(bx + nx * 5, by + ny * 5); c.stroke();
        c.globalAlpha = a; c.strokeStyle = P.glow; c.lineWidth = 5;
        c.beginPath(); c.moveTo(ax + nx * 2.5, ay + ny * 2.5); c.lineTo(bx + nx * 2.5, by + ny * 2.5); c.stroke();
        c.strokeStyle = "#FFFFFF"; c.lineWidth = 1.6;
        c.beginPath(); c.moveTo(ax + nx * 2.5, ay + ny * 2.5); c.lineTo(bx + nx * 2.5, by + ny * 2.5); c.stroke();
        /* the runes in the span flare with it */
        const RS = %RSZ% * (1.25 + 0.25 * (1 - k));
        for (const r of runes){
          if (r[6] !== wall || Math.abs(r[7] - s) > H) continue;
          c.save();
          c.translate(r[1], r[2]); c.rotate(Math.atan2(r[3], -r[4])); c.scale(RS, RS);
          c.globalAlpha = a;
          this._lodeRunePath(c, Math.floor(shellHash(9951, r[5]) * 6));
          c.strokeStyle = P.dark; c.lineWidth = 4 / RS; c.stroke();
          c.strokeStyle = P.glow; c.lineWidth = 2.2 / RS; c.stroke();
          c.restore();
        }
      }
    }
    c.restore();
  }

  /* THE RUNE-STREAK: the hurled ball's own path over its last 0.2s, drawn
     under it, tapering to the tail, with runes riding it every 26 units. */
  _lodeStreak(m, f, P){
    const c = this.ctx, RS = 5;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of f.lodeFx){
      const Q = q.pts, n = Q.length / 3;
      if (n < 2) continue;
      const fade = q.t < %TLIFE% / 2 ? 1 : 1 - (q.t - %TLIFE% / 2) / (%TLIFE% / 2);
      let run = 0;
      for (let i = 1; i < n; i++){
        const age = q.t - Q[3 * i + 2];
        if (age > %TRAIL%) continue;
        const x0 = Q[3 * i - 3], y0 = Q[3 * i - 2], x1 = Q[3 * i], y1 = Q[3 * i + 1];
        const w = 20 * (1 - age / %TRAIL%);
        c.globalAlpha = 0.45 * fade; c.strokeStyle = P.core; c.lineWidth = w;
        c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
        c.globalAlpha = 0.9 * fade; c.strokeStyle = P.glow; c.lineWidth = Math.max(1, w * 0.25);
        c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
        const d = Math.hypot(x1 - x0, y1 - y0);
        const r0 = run; run += d;
        for (let z = Math.ceil(r0 / 24) * 24; z < run; z += 24){
          const s = (z - r0) / (d || 1), x = x0 + (x1 - x0) * s, y = y0 + (y1 - y0) * s;
          c.save(); c.translate(x, y); c.rotate(Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2); c.scale(RS, RS);
          c.globalAlpha = fade * Math.min(1, 1.6 * (1 - age / %TRAIL%));
          this._lodeRunePath(c, (q.k + z / 24) | 0);
          c.strokeStyle = P.dark; c.lineWidth = 3.4 / RS; c.stroke();
          c.strokeStyle = P.glow; c.lineWidth = 1.6 / RS; c.stroke();
          c.restore();
        }
      }
    }
    c.restore();
  }

  /* THE BAR: from the wall into the ball it hexes, one frame -- a jagged
     rune-light, three kinks by shellHash on the touch's count. */
  _lodeBolt(m, f, G, P){
    const c = this.ctx, foe = f === m.a ? m.b : m.a;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of f.lodeFx){
      if (m.over || !(m.t - q.t0 < %BOLT%) || !foe.alive) continue;
      for (const wall of q.walls){
        const p = lodeAt(G, lodeOn(G, wall, q.x, q.y));
        const dx = foe.x - p[0], dy = foe.y - p[1], d = Math.hypot(dx, dy) || 1;
        const nx = -dy / d, ny = dx / d;
        const pts = [[p[0], p[1]]];
        for (let i = 1; i < 4; i++){
          const o = (shellHash(9971 + wall, q.k * 4 + i) - 0.5) * 16;
          pts.push([p[0] + dx * i / 4 + nx * o, p[1] + dy * i / 4 + ny * o]);
        }
        pts.push([foe.x, foe.y]);
        for (const [w, col] of [[6, P.dark], [3, P.glow], [1.2, "#FFFFFF"]]){
          c.globalAlpha = 1; c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
          c.stroke();
        }
      }
    }
    c.restore();
  }

  /* THE HEAD'S RUNE, in the weapon's own frame (drawWeapon's): the sigil
     etched in the head's face (`_whConjured`'s maker mark, the same ring and
     triangle at the same place) burns in the glow while the walls are lit,
     and goes dark with them. */
  _lodeHead(f, L){
    const c = this.ctx, P = f.aff, W = f.w.artW, hs = W * %HSW% / 2, sc = hs * 0.52;
    const path = () => {
      c.beginPath(); c.arc(0, 0, sc * 0.92, 0, TAU);
      for (let i = 0; i < 3; i++){
        const a = i * TAU / 3 - Math.PI / 2;
        if (i) c.lineTo(Math.cos(a) * sc * 0.60, Math.sin(a) * sc * 0.60);
        else { c.moveTo(Math.cos(a) * sc * 0.60, Math.sin(a) * sc * 0.60); }
      }
      c.closePath();
    };
    c.save();
    c.globalAlpha *= f.lodeFade;
    c.translate(L - hs, 0);
    c.lineCap = "round"; c.lineJoin = "round";
    path(); c.strokeStyle = P.dark; c.lineWidth = W * 0.11; c.stroke();
    path(); c.strokeStyle = P.glow; c.lineWidth = W * 0.055; c.stroke();
    path(); c.strokeStyle = "#FFFFFF"; c.lineWidth = W * 0.02; c.stroke();
    c.restore();
  }

"""


# ---------------------------------------------------------------------------
# 9. THE SILHOUETTE (v70 6.1: "a rune-etched square head on a dark haft, first cut"), inside the runic
#    warhammer's own route only. Candidates for the lineup; the deliverable is PICK["SIL"].
def sil_old(s):
    return between(s, "  /* -------------------------------------------------------------- RUNIC --\n"
                      "     IN PIECES, HELD BY NOTHING. The grammar's second type.",
                   "  /* ------------------------------------------------------------ VERDANT --\n")


SIL_HEAD = """  /* -------------------------------------------------------------- RUNIC --
     LODESTONE'S HAMMER (v70 section 6.1, "a rune-etched square head on a
     dark haft, first cut"). This route was the runic grammar's conjured
     hammer -- three slices held in formation, no haft, a sigil where a hand
     would be -- which no relic drew until Lodestone, the school's first
     warhammer. Measured at the app's 453x805 among the seven hammers
     (the weapon's |dL| over the floor, median of 5 frames):
     %SILWHY%.
     Runic's grammar is kept in the ETCHING: the school's triangle-in-ring
     sigil (`_makerMark`) cut into the face, and it burns while the walls are
     lit (`_lodeHead`). Only a runic warhammer reaches this route; every
     other school's hammer is untouched.
     THE HEAD IS SIZED OFF THE WIDTH, NOT THE LENGTH (Canopy's lesson on
     `_whGrown`): a square block %HSW% x W on a side at the end of the reach,
     and the haft runs from the ball to it. */
  _whConjured(c, L, W, p){
    const hs = W * %HSW% / 2, xb = L - 2 * hs, hw = W * 0.075;
%SILBODY%
  },

"""

SIL_BODIES = {
    # a pale steel block (the value every hammer head in the row carries), core-blue etching
    "square": dict(SILWHY=("the conjured slices 0.243 on 2850 u2, this square head 0.239 on"
                           + chr(10) + "     4361 u2 -- first of the seven, the other six 0.126-0.219 on 4100-6000"
                           + chr(10) + "     u2: as legible, and a hammer-sized object"), SILBODY="""\
    c.fillStyle = SHAPES._shade(p.dark, 1.15, 0.15);            // the dark haft
    c.fillRect(0, -hw, xb + 2, hw * 2);
    c.fillStyle = SHAPES._shade(p.dark, 2.4, 0.25);             // its two iron collars
    c.fillRect(xb - W * 0.10, -hw * 1.45, W * 0.07, hw * 2.9);
    c.fillRect(-L * 0.02, -W * 0.10, L * 0.05, W * 0.20);
    const head = (cc) => { cc.beginPath(); cc.rect(xb, -hs, 2 * hs, 2 * hs); };
    head(c); c.fillStyle = p.steel; c.fill();
    c.save(); c.shadowBlur = 0; c.globalAlpha = SHAPES._lit(c);  /* world light */
    head(c); c.clip();
    c.fillStyle = SHAPES._facet(p.steel, p.dark, 0.30);          // the lower face
    c.fillRect(xb, hs * 0.30, 2 * hs, hs * 0.75);
    c.fillStyle = SHAPES._facet(p.steel, p.dark, 0.62);          // the underside
    c.fillRect(xb, hs * 0.74, 2 * hs, hs * 0.30);
    c.restore();
    head(c);
    c.strokeStyle = SHAPES._shade(p.dark, 1.0, 0.2); c.lineWidth = Math.max(1, W * 0.05); c.stroke();
    /* the etching: a border cut round the face and the school's sigil in it */
    c.strokeStyle = SHAPES._facet(p.steel, p.dark, 0.72); c.lineWidth = Math.max(0.8, W * 0.028);
    c.strokeRect(xb + hs * 0.22, -hs * 0.78, 2 * hs - hs * 0.44, hs * 1.56);
    SHAPES._makerMark(c, xb + hs, 0, hs * 0.52, W, p);
    c.fillStyle = p.core;                                        // the striking face
    c.fillRect(L - W * 0.035, -hs, W * 0.035, 2 * hs);"""),
    # a dark stone block (a lodestone is black ore) with a pale steel rim, core-blue etching
    "stone": dict(SILWHY="(a candidate: 0.185)", SILBODY="""\
    c.fillStyle = SHAPES._shade(p.dark, 1.15, 0.15);            // the dark haft
    c.fillRect(0, -hw, xb + 2, hw * 2);
    c.fillStyle = SHAPES._shade(p.dark, 2.4, 0.25);             // its two iron collars
    c.fillRect(xb - W * 0.10, -hw * 1.45, W * 0.07, hw * 2.9);
    c.fillRect(-L * 0.02, -W * 0.10, L * 0.05, W * 0.20);
    const head = (cc) => { cc.beginPath(); cc.rect(xb, -hs, 2 * hs, 2 * hs); };
    head(c); c.fillStyle = SHAPES._shade(p.dark, 1.9, 0.35); c.fill();
    c.save(); c.shadowBlur = 0; c.globalAlpha = SHAPES._lit(c);  /* world light */
    head(c); c.clip();
    c.fillStyle = SHAPES._shade(p.dark, 3.2, 0.35);               // the lit upper face
    c.fillRect(xb, -hs, 2 * hs, hs * 0.42);
    c.fillStyle = SHAPES._shade(p.dark, 0.9, 0.35);               // the underside
    c.fillRect(xb, hs * 0.70, 2 * hs, hs * 0.34);
    c.restore();
    head(c);
    c.strokeStyle = p.steel; c.lineWidth = Math.max(1, W * 0.05); c.stroke();
    SHAPES._makerMark(c, xb + hs, 0, hs * 0.55, W, p);
    c.fillStyle = p.core;                                        // the striking face
    c.fillRect(L - W * 0.035, -hs, W * 0.035, 2 * hs);"""),
}


def sil_row(s, sil):
    if sil == "conjured":
        return None
    B = SIL_BODIES[sil]
    code = SIL_HEAD
    for k, v in B.items():
        code = code.replace("%" + k + "%", str(v))
    return dict(label="rebuttal picture: the runic warhammer, a rune-etched square head on a dark haft",
                anchor=sil_old(s), mode="replace", code=code,
                why="v70 6.1's silhouette: the runic warhammer's route (_whConjured, three conjured slices, never drawn before Lodestone) redrawn as the design's first cut; measured at the app's size among the seven hammers.")


def rows(sil=None):
    s = src_text()
    pick = dict(PICK)
    if sil is not None:
        pick["SIL"] = '"%s"' % sil

    def fill(code):
        for k, v in pick.items():
            code = code.replace("%" + k + "%", str(v))
        left = re.findall(r"%[A-Z_]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="rebuttal picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the walls go dark 0.4s past ultRunes, which a blow's kill leaves set through the verdict; a touch's flare, bar and streak outlive the frame that touched); never m.ultFx (open item 25). Read by nothing in the sim."),
        dict(label="rebuttal picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickLode."),
        dict(label="rebuttal picture: the hall's loop", anchor=HALL_ANCHOR, mode="before", code=HALL_CODE,
             why="Pure functions: the live hall's four walls as one loop (lodeHall, lodeAt, lodeOn, lodeNear), read by tickLode and the renderer; nothing in the sim calls them."),
        dict(label="rebuttal picture: tickLode", anchor=TICK_ANCHOR, mode="before", code=TICK_CODE,
             why="Drives the walls (light at the cast from the caster's nearest wall, hold, go dark off ultRunes && !over && alive) and each touch, found by runeTally.touches rising: a record of its walls (the touch test's own sides, read again) and spot, the hurled ball's path for the streak, and the HEX tag on the foe with its count (in place if one is up). Writes presentation fields, tags and taught only; shellHash, no rng."),
        dict(label="rebuttal picture: the world call (under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls: the rune chain, its motes, a touch's flare and the rune-streak (bloom share 0)."),
        dict(label="rebuttal picture: the world call (over both fighters)", anchor=TOP_ANCHOR, mode="after", code=TOP_CODE,
             why="World pass over both fighters: the one-frame bar from the wall into the ball."),
        dict(label="rebuttal picture: the head's rune in drawWeapon", anchor=HEAD_ANCHOR, mode="after", code=HEAD_CODE,
             why="While lodeFade > 0 a rune is drawn on the hammer's head in the shape's own frame; SHAPES is untouched by it, so the glow cache and every other hammer draw as before."),
        dict(label="rebuttal picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawLode / drawLodeTop and one method a component (walls, motes, flare, streak, bar, head rune)."),
    ]
    sr = sil_row(s, pick["SIL"].strip('"'))
    if sr is not None:
        R.append(sr)
    for r in R:
        r["code"] = fill(r["code"])
    return R


def one(src: str, anchor: str, code: str, mode: str, label: str) -> str:
    d_old = anchor.count("/*") - anchor.count("*/")
    new = {"before": code + anchor, "after": anchor + code, "replace": code}[mode]
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new and mode != "replace":
        raise SystemExit(f"BLOCK {label}: comment balance {d_old:+d} -> {d_new:+d}")
    if mode == "replace" and (code.count("/*") - code.count("*/")) != 0:
        raise SystemExit(f"BLOCK {label}: replacement comment balance")
    n = src.count(anchor)
    if n != 1:
        raise SystemExit(f"ANCHOR {label}: expected 1 occurrence, found {n}")
    return src.replace(anchor, new, 1)


def apply_all(src: str, R) -> str:
    for r in R:
        src = one(src, r["anchor"], r["code"], r["mode"], r["label"])
    return src


def syntax_check(html: str) -> int:
    node = shutil.which("node")
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit("DOES NOT PARSE:\n" + (r.stderr or "")[:2000])
    return len(blocks)


def strip_comments(t: str) -> str:
    return re.sub(r"//[^\n]*", "", re.sub(r"/\*[\s\S]*?\*/", "", t))


def build(out: pathlib.Path, src=None, sil=None):
    s = src if src is not None else src_text()
    R = rows(sil)
    o = apply_all(s, R)
    for bad in ("rng()", "spawnFx", "Math.random", "ultFx"):
        for r in R:
            assert bad not in strip_comments(r["code"]), (r["label"], bad)
    assert strip_comments(o).count("Math.random") == strip_comments(s).count("Math.random")
    n = syntax_check(o)
    out.write_bytes(o.encode("utf-8"))
    return n, len(o) - len(s)


def stamp_of(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    n, d = build(HERE / "ld-final.html")
    print(f"ld-final.html: {n} script blocks parse, {d:+d} chars, stamp {stamp_of((HERE / 'ld-final.html').read_bytes().decode('utf-8'))}")
