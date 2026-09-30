"""BLOODPRICE'S PICTURE (v81 section 4) as exactly-once edits to Goreshard's final link
(goreshard/links/sc-goreshard-b10.25.html, 8eb3c1634184c1bd = the base with stages 1, 2 and 5).

rows() -> the deliverable rows (numbers inlined from PICK). There is NO lab variant of the rows: every
component is its own renderer method, so the harnesses hide one by replacing that method on the renderer
from outside the page, and the bytes measured are the bytes delivered.

build(out)            -> gs-final.html     (the base + these rows: THE STAMP)
build(out, fxout=1)   -> gs-final-fx.html  (the same + SPECS.oathwound out of the inlined fx.js copy with the
                                            stamp re-cut, which is what the orchestrator's sync_fx does to
                                            both copies; the look as it ships). SCRATCH ONLY.
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "links" / "sc-goreshard-b10.25.html").resolve()
BASE_SHA16 = "8eb3c1634184c1bd"

PICK = dict(
    RUN=0.6,       # the cast: the red runs from the guard to the point, half-seconds (0.3s)
    DRAIN=0.7,     # the close: the red drains back from the point into the guard, half-seconds (0.35s)
    GLOWT=0.16,    # the glow's ease toward its stack level, half-seconds (0.08s)
    G0=0.2,        # the glow's alpha at 0 foe stacks (v81 section 4: 0 -> 4 maps 0.2 -> 0.8)
    G1=0.15,       # ...and per stack
    BLUR=18,       # the window glow sprite's blur
    GW=1.6,        # the window glow sprite is baked off the blade at 1.6x its width (gs_explore2: the stack
                   # ladder 0.2 -> 0.8 moves |dL| 0.109 on 8130 px against 0.076 on 5353 at the rest sprite's
                   # own width and blur 20; the weapon reads 0.113 against 0.100)
    ART='"#D02A40"',   # arterial red: the blade's steel for the window (gs_explore: the lightest red tried that
                       # still reads as blood, weapon |dL| 0.100 against 0.092 / 0.084 for the darker two)
    RATE=5,        # blood motes shed per half-second (10 a second) while the window is open
    DLIFE=1.3,     # a mote's life, half-seconds (0.65s)
    GRAV=560,      # a mote's fall, units/s^2
    RIM='"#3A0610"',   # a mote's dark rim: it reads on a white foe as well as on the floor
    FLOATK=0.1,    # a priced blow's float: x(1 + FLOATK x the stacks it paid on)
)


def src_text(src=None) -> str:
    return src if src is not None else SRC.read_bytes().decode("utf-8")


def between(s: str, start: str, end: str) -> str:
    """The exact text from `start` up to (not including) `end`; both unique."""
    assert s.count(start) == 1, start
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j]


# ---------------------------------------------------------------------------
# 1. the fighter's picture state
FIGHTER_ANCHOR = "    this.ultPrice = null;\n    this.priceTally = null;\n"
FIGHTER_CODE = """    /* BLOODPRICE'S PICTURE (v81 section 4), and none of it is the window:
       the red outlives `ultPrice` by its drain, and a mote by its fall. On
       the FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast
       takes it: open item 25). Driven in `tickPresentation` (`tickGore`);
       nothing in the simulation reads any of it.
         goreFade  -- 1 while the window is open and the match is on; eased
                      to 0 over the drain after the close, the caster's fall
                      or the match's end
         goreAge   -- the presentation clock since the cast (the red's run)
         goreOut   -- the presentation clock since the close (the drain);
                      0 while the window is open
         goreGlow  -- the blade's glow alpha, eased toward 0.2 + 0.15 x the
                      foe's Hemorrhage stacks, read live
         goreSeen  -- `priceTally.casts`, as last seen (a cast is it rising)
         goreAcc, goreDropN -- the motes' emission clock and their count
         goreDrops -- the blood motes in flight, in world space
         goreTh, goreT, goreW -- theta and the match clock at the last look,
                      and the blade's sweep (rad/s) they give */
    this.goreFade = 0;
    this.goreAge = 0;
    this.goreOut = 0;
    this.goreGlow = 1;
    this.goreSeen = 0;
    this.goreAcc = 0;
    this.goreDropN = 0;
    this.goreDrops = [];
    this.goreTh = 0;
    this.goreT = -1;
    this.goreW = 0;
"""

# ---------------------------------------------------------------------------
# 2. the presentation call
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickGore(dt);                 // BLOODPRICE'S PICTURE (v81 section 4)\n"

# ---------------------------------------------------------------------------
# 3. tickGore, after tickPrice
TICK_ANCHOR = '      f.priceTally.foeStk += foe.stacks("hemorrhage");\n    }\n  }\n'
TICK_CODE = """
  /* ------------------------------------------------ BLOODPRICE'S PICTURE ---
     v81 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step and once in a
     hit stop): %RUN% is the cast's 0.3s run of red from the guard to the
     point, %DRAIN% the close's 0.35s drain, %GLOWT% the glow's ease, %DLIFE% a
     mote's life. THE WINDOW IS READ OFF `ultPrice && !over`, with both
     fighters standing: `tickPrice` never runs again once `over` is set, and
     about one window in seven is still set when the match ends (the kill
     lands in `tickHits`, after `tickPrice`), so the blade drains at the
     verdict instead of holding red through the panel. THE CAST IS FOUND BY
     WATCHING `priceTally.casts` RISE, so `fireUlt` makes no call for the
     picture. THE GLOW reads the foe's Hemorrhage live (`stacks` is a pure
     read): 0.2 + 0.15 a stack, as v81 maps it. THE MOTES are shed off the
     four back-edge barbs and the point in turn while the window is open,
     jittered by shellHash on their count, carrying a third of the blade's
     sweep, and fall. Writes presentation fields only; no rng. */
  tickGore(dt){
    for (const f of [this.a, this.b]){
      const T = f.priceTally;
      if (!T) continue;                                       // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      /* the blade's sweep, off the match clock (it runs in a hit stop too,
         where theta holds and this reads 0) */
      if (this.t !== f.goreT){
        if (f.goreT >= 0) f.goreW = (f.theta - f.goreTh) / (this.t - f.goreT);
        f.goreTh = f.theta; f.goreT = this.t;
      }
      const open = !!f.ultPrice && !this.over && f.alive && foe.alive;
      if (T.casts !== f.goreSeen){
        f.goreSeen = T.casts;
        if (open){ f.goreAge = 0; f.goreOut = 0; f.goreGlow = 1; }   // a cast
      }
      if (open){
        f.goreFade = 1; f.goreOut = 0;
        f.goreAge += dt;
        const n = Math.min(4, foe.stacks("hemorrhage"));
        f.goreGlow += (%G0% + %G1% * n - f.goreGlow) * Math.min(1, dt / %GLOWT%);
        f.goreAcc += dt * %RATE%;
        while (f.goreAcc >= 1){
          f.goreAcc -= 1;
          this._goreShed(f);
        }
      } else if (f.goreFade > 0){
        f.goreOut += dt;
        f.goreFade = Math.max(0, 1 - f.goreOut / %DRAIN%);
      }
      for (let i = f.goreDrops.length - 1; i >= 0; i--){
        f.goreDrops[i].t += dt;
        if (f.goreDrops[i].t >= %DLIFE%) f.goreDrops.splice(i, 1);
      }
    }
  }

  /* one mote, off a barb's hooked tip (or the point), where `_gsBarbed`
     draws it this frame: the blade's own frame turned into the hall's */
  _goreShed(f){
    const R = CONFIG.physics.ballR, L = f.w.reach * this.actMods.reach * f.reachMul + 6;
    const bh = f.w.artW * 0.19, n = f.goreDropN++, j = n % 5;
    const h1 = shellHash(8111 + f.side, n), h2 = shellHash(8117 + f.side, n);
    const lx = j < 4 ? L * (0.34 + 0.14 * j) - L * 0.075 + (h1 - 0.5) * L * 0.05 : L * (0.97 + 0.03 * h1);
    const ly = j < 4 ? bh * 2.1 : (h1 - 0.5) * bh;
    const a = f.theta + (f.bladeSet || f.w.blades)[0] * TAU, ca = Math.cos(a), sa = Math.sin(a);
    const rx = R - 6 + lx;
    const x = f.x + ca * rx - sa * ly, y = f.y + sa * rx + ca * ly;
    /* a third of the sweep at that radius, and a little out along the blade */
    const w = clamp(f.goreW, -12, 12) * 0.33, rr = Math.hypot(rx, ly);
    const vx = -sa * w * rr + ca * (10 + 30 * h2), vy = ca * w * rr + sa * (10 + 30 * h2) - 20;
    f.goreDrops.push({ x, y, vx, vy, t: 0, n });
    if (f.goreDrops.length > 40) f.goreDrops.shift();
  }
"""

# ---------------------------------------------------------------------------
# 4. drawWeapon's hook
HOOK_ANCHOR = "    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;\n"
HOOK_CODE = """    /* BLOODPRICE (v81 section 4): through the window, and the drain after
       it, the blade draws itself (`drawGoreWeapon`) -- arterial red, its glow
       following the foe's Hemorrhage -- off the same blade set, reach and
       angles `bladeSegments` tests. `goreFade` is 0 on every other relic, so
       this is one comparison on a field nothing else writes. `w` is never
       written: it is the mirror match's too. */
    if (f.goreFade > 0 && this.drawGoreWeapon(m, f, reach, dim)) return;
"""

# ---------------------------------------------------------------------------
# 5. the motes' pass
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* BLOODPRICE'S MOTES (v81 section 4: "blood motes off the blade"): shed
       off the barbs for the window and falling. The WORLD pass and under both
       balls: nothing of it reaches the bloom (CLAUDE.md section 4.1c) and no
       ball's disc is painted over (4.1b). */
    if (__world) this.drawGoreDrops(m);
"""

# ---------------------------------------------------------------------------
# 6. the drawing methods
DRAW_ANCHOR = "  drawMotes(m){\n"
DRAW_CODE = """  /* ================================================ BLOODPRICE ========
     v81 section 4: "the beam art is retired. Cast: the blade darkens to
     arterial red for the window; the blade's glow SCALES with the foe's
     current stack count (0 -> 4 maps alpha 0.2 -> 0.8), so 'harder the more
     you bleed' is on the sword itself; the damage float on a scaled blow is
     drawn larger. Field: blood motes off the blade."

     THE CAST: the red runs down the blade from the guard to the point in
     0.3s, a bright front crossing it, fastest at the start: it is moving
     inside the cast's own stop. THE WINDOW: the blade is arterial red
     (the school's steel swapped for %ART%: the blade, its barbs and its
     swept guard; the honed edge, grip, pommel and the fed notch are the
     school's own, so the barbed silhouette reads as it does at rest), and
     its glow climbs as the foe bleeds and sinks as the bleed runs out: the
     blade's own glow sprite, baked off it at %GW%x its width, in the school's
     bright `glow` instead of its `core`, ADDED (`lighter`, the world pass:
     nothing of it reaches the bloom) at 0.2 + 0.15 a foe stack. Baked once
     by `weaponGlow`'s own cache (one more key a reach), never per frame; the
     alpha is the blit's. Measured (gs_explore): the stacks' 0.2 -> 0.8
     moves three times the pixels, three times as far, as the rest sprite's
     red would (|dL| 0.109 on 8130 px against 0.036 on 2566; 0.076 on 5353
     at the rest sprite's own width). THE CLOSE: the red drains back from the point
     into the guard in 0.35s, and the glow crossfades back to the rest
     pose's. The float is `resolveHit`'s own, larger.

     IT HANGS OFF THE FIGHTER (`goreFade`, `goreAge`, `goreOut`, `goreGlow`,
     `goreDrops`), never `m.ultFx` (open item 25). PRESENTATION ONLY: no rng,
     no spawnFx, no Math.random -- shellHash and the clocks -- and nothing
     here writes a field the simulation reads. */
  drawGoreWeapon(m, f, reach, dim){
    const c = this.ctx, R = CONFIG.physics.ballR, L = reach + 6, W = f.w.artW;
    const run = !(f.goreOut > 0);
    /* the run eases OUT, so the red is already a third of the way down the
       blade inside the cast's own 0.08s stop (this clock runs through it);
       the drain eases in and out */
    const u = run ? clamp(f.goreAge / %RUN%, 0, 1) : 1 - clamp(f.goreOut / %DRAIN%, 0, 1);
    const e = run ? 1 - (1 - u) * (1 - u) : u * u * (3 - 2 * u);
    const x1 = L * (0.13 + 0.92 * e);                    // the red's front, from the guard
    const P = this._gorePal(f.aff, 0);
    for (const off of (f.bladeSet || f.w.blades)){
      const a = f.theta + off * TAU;
      c.save();
      c.translate(f.x, f.y);
      c.rotate(a);
      c.translate(R - 6, 0);
      this._goreGlow(c, f, L, W, e, dim);
      c.globalAlpha = dim;
      if (x1 < L * 1.02) this._goreSteel(c, f, L, W, a, f.aff, null);
      if (x1 > L * 0.14) this._goreSteel(c, f, L, W, a, P, x1 < L * 1.02 ? x1 : null);
      if (e > 0.02 && e < 0.98) this._goreFront(c, f, L, W, x1, dim * (run ? 1 - e * 0.5 : 0.5));
      c.restore();
    }
    return true;
  }

  /* the school's palettes for the window, cached per school: 0 the blade
     (its steel arterial), 1 the glow (its `core` -- the colour `weaponGlow`
     bakes -- the school's bright `glow`) */
  _gorePal(aff, k){
    const C = this._gorePals || (this._gorePals = {}), id = aff.key + k;
    return C[id] || (C[id] = Object.assign({}, aff, k ? { core: aff.glow } : { steel: %ART% }));
  }

  /* THE GLOW: the rest pose's own sprite fading out as the red runs in (and
     back as it drains), and the window's, added at the stacks' alpha */
  _goreGlow(c, f, L, W, e, dim){
    if (e < 0.999){
      const g0 = weaponGlow(f.w.shape, L, W, f.aff, f.drawK, 20);
      c.globalAlpha = dim * (1 - e);
      c.drawImage(g0.cv, g0.ox, g0.oy);
    }
    if (e > 0.001){
      const g = weaponGlow(f.w.shape, L, W * %GW%, this._gorePal(f.aff, 1), f.drawK, %BLUR%);
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = clamp(dim * e * f.goreGlow, 0, 1);
      c.drawImage(g.cv, g.ox, g.oy);
      c.restore();
    }
  }

  /* THE BLADE in a palette, clipped behind the red's front when it has one */
  _goreSteel(c, f, L, W, a, P, x1){
    if (x1 != null){
      c.save();
      c.beginPath(); c.rect(-L * 0.2, -W * 3, x1 + L * 0.2, W * 6); c.clip();
    }
    if (!litWeapon(c, f.w.shape, L, W, P, f.drawK, a)){
      const fn = SHAPES[f.w.shape];
      if (fn) fn(c, L, W, P, f.drawK);
    }
    if (x1 != null) c.restore();
  }

  /* THE FRONT: a bright seam across the blade where the red has reached */
  _goreFront(c, f, L, W, x1, al){
    const bh = W * 0.19, xs = Math.min(x1, L * 0.995);
    const hh = xs < L * 0.795 ? bh * 1.05 : bh * 0.9 * (L - xs) / (L * 0.205) + 1;
    c.globalAlpha = clamp(al, 0, 1);
    c.strokeStyle = f.aff.glow; c.lineWidth = Math.max(1.5, W * 0.06); c.lineCap = "round";
    c.beginPath(); c.moveTo(xs, -hh); c.lineTo(xs, hh); c.stroke();
  }

  /* THE MOTES: drops of blood off the barbs, falling, each drawn along its
     own velocity with a dark rim, so it reads on a white foe as well as on
     the floor. Clipped to the hall. */
  drawGoreDrops(m){
    const a = m.a, b = m.b;
    if (!a.goreDrops.length && !b.goreDrops.length) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    for (const f of [a, b]){
      for (const q of f.goreDrops){
        const s = q.t * 0.5, k = q.t / %DLIFE%;
        const x = q.x + q.vx * s, y = q.y + q.vy * s + %GRAV% * 0.5 * s * s;
        const vx = q.vx, vy = q.vy + %GRAV% * s, sp = Math.hypot(vx, vy) || 1;
        const r = 1.7 + 0.9 * shellHash(8123 + f.side, q.n), st = Math.min(5, sp * 0.012);
        c.save();
        c.translate(x, y); c.rotate(Math.atan2(vy, vx));
        c.globalAlpha = clamp((1 - k) * 1.5, 0, 1) * Math.min(1, k * 10 + 0.2);
        c.fillStyle = %RIM%;
        c.beginPath(); c.ellipse(-st * 0.5, 0, r + 0.9 + st, r + 0.9, 0, 0, TAU); c.fill();
        c.fillStyle = f.aff.core;
        c.beginPath(); c.ellipse(-st * 0.5, 0, r + st, r, 0, 0, TAU); c.fill();
        c.restore();
      }
    }
    c.restore();
  }

"""

# ---------------------------------------------------------------------------
# 7. the float, larger on a priced blow
FLOAT_ANCHOR = "    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1);\n"
FLOAT_CODE = """    /* BLOODPRICE (v81 section 4): "the damage float on a scaled blow is
       drawn larger" -- x(1 + %FLOATK% x the stacks the blow paid on). `priceN`
       is 0 on every blow the price did not scale (its window shut, the struck
       body not bleeding, every other relic), and x1 is exact, so every other
       float is the old size. Presentation only: `floats` is aged, drawn and
       lerped, and nothing in the simulation reads it. */
    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + %FLOATK% * priceN);
"""

# ---------------------------------------------------------------------------
# 8-9. the beam's pool and its seam, retired
UNDER_HEAD = "    /* ---- Bloodprice: what runs out of the wound, on the floor -------------- */\n"
OVER_HEAD = "    /* ---- Bloodprice: a seam torn open in the air, and the oath that holds -- */\n"


def branch(s: str, head: str) -> str:
    """The retired branch whole: its header comment through the `}` that closes it (the text up to the
    blank line before the next section's header)."""
    assert s.count(head) == 1, head
    i = s.index(head)
    j = s.index("\n\n    /* ---- ", i)
    return s[i:j + 1]


UNDER_CODE = """    /* ---- Bloodprice's pool was the BEAM's (the floor under the struck foe,
       and its rivulets, for the record's 1.5); retired with it (v81, v114
       stage 6). The window's picture is the blade itself (`drawGoreWeapon`),
       off the fighter, where the one ultFx slot cannot erase it. */
"""
OVER_CODE = """    /* ---- Bloodprice's seam was the BEAM's (the wound torn in the air over
       the quarry, its drops and the tether back to the caster); retired with
       it (v81, v114 stage 6). The cast is the red running down the blade. */
"""

# ---------------------------------------------------------------------------
# 10. the charge rune
def sig_old(s):
    return between(s, "  /* BLOODPRICE -- a beam, and the toll paid under it. */\n",
                   "  /* ROOTFAST -- roots going down and GRIPPING. Anchored, not thrown. */\n")


SIG_CODE = """  /* BLOODPRICE -- the sword that is paid in blood. The beam and the pool
     under it went out with the beam (v81): a greatsword laid across the
     rune, reddening from the guard to the point as the charge fills, its
     glow rising with it, and blood running off its edge. */
  oathwound(c, t, cf, P){
    const ux = 0.7071, uy = -0.7071, px = 0.7071, py = 0.7071;
    const gx = -0.40, gy = 0.40, len = 1.50, hw = 0.12;
    const at = (s, d) => [gx + ux * s * len + px * d, gy + uy * s * len + py * d];
    SG.path(c, [at(0.02, 0), at(1, 0)], P.core, 0.46, 0.08 + cf * 0.34);
    SG.path(c, [at(-0.30, 0), at(0, 0)], P.dark, 0.13, 0.9);
    SG.path(c, [at(0, -0.28), at(0, 0.28)], P.core, 0.1, 0.9);
    SG.poly(c, [at(0.03, -hw), at(0.84, -hw * 0.9), at(1, 0), at(0.84, hw * 0.9), at(0.03, hw)], P.steel, 0.9);
    const k = 0.03 + 0.97 * cf;
    if (k > 0.05){
      const e = Math.min(k, 0.84);
      const pts = [at(0.03, -hw), at(e, -hw * (1 - 0.1 * e / 0.84)), at(e, hw * (1 - 0.1 * e / 0.84)), at(0.03, hw)];
      if (k > 0.84) pts.splice(2, 0, at(k, hw * 0.9 * (1 - k) / 0.16), at(k, -hw * 0.9 * (1 - k) / 0.16));
      SG.poly(c, pts, %ART%, 0.92);
    }
    for (let i = 0; i < 2; i++){
      const u = (t * 0.7 + i * 0.5) % 1, [x0, y0] = at(0.35 + i * 0.3, hw * 1.2);
      SG.disc(c, x0, y0 + u * 0.55, 0.055, P.core, (1 - u) * (0.25 + cf * 0.7));
    }
  },
"""


def rows(src=None):
    s = src_text(src)

    def fill(code):
        for k, v in PICK.items():
            code = code.replace("%" + k + "%", str(v))
        left = re.findall(r"%[A-Z_0-9]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="bloodprice picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the red's run and drain, the glow's level, the cast last seen, the motes in flight, the blade's sweep); never m.ultFx (open item 25). Read by nothing in the sim."),
        dict(label="bloodprice picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickGore."),
        dict(label="bloodprice picture: tickGore", anchor=TICK_ANCHOR, mode="after", code=TICK_CODE,
             why="Finds the cast by priceTally.casts rising; drives the red (run 0.3s at the cast, drain 0.35s at the close, the caster's fall or over) off ultPrice && !over && both alive; eases the glow toward 0.2 + 0.15 x the foe's Hemorrhage read live; sheds the blood motes off the barbs (shellHash, no rng). Writes presentation fields only."),
        dict(label="bloodprice picture: drawWeapon's blade hook", anchor=HOOK_ANCHOR, mode="after", code=HOOK_CODE,
             why="While goreFade > 0 the blade draws itself (drawGoreWeapon) off the same blade set, reach and angles bladeSegments tests; w is never written."),
        dict(label="bloodprice picture: the motes' call (world, under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls: the falling blood motes (bloom share 0; no ball's disc painted over)."),
        dict(label="bloodprice picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawGoreWeapon (the glow: the rest sprite crossfading to the window's, the school's bright glow added at 0.2 + 0.15 a foe stack, both from weaponGlow's cache; the blade in the school's palette with its steel arterial, clipped behind the red's front during the run and the drain; the front's seam) and drawGoreDrops."),
        dict(label="bloodprice picture: the priced blow's float, larger", anchor=FLOAT_ANCHOR, mode="replace", code=FLOAT_CODE,
             why="v81 section 4: the damage float on a scaled blow is drawn larger, x(1 + 0.1 x priceN); priceN is 0 on every other blow, so every other float is byte-for-byte the old size. floats are presentation only."),
        dict(label="bloodprice picture: the beam's pool retired", anchor=branch(s, UNDER_HEAD), mode="replace", code=UNDER_CODE,
             why="drawUltUnder's oathwound branch was the BEAM's pool under the struck foe; the beam is out (v114 stage 1), so its picture goes too."),
        dict(label="bloodprice picture: the beam's seam retired", anchor=branch(s, OVER_HEAD), mode="replace", code=OVER_CODE,
             why="drawUltOver's oathwound branch was the BEAM's seam torn over the quarry, its drops and the tether; retired with the beam."),
        dict(label="bloodprice picture: the charge rune", anchor=sig_old(s), mode="replace", code=SIG_CODE,
             why="ULTSIG.oathwound drew a beam and the pool under it; now a greatsword across the rune that reddens from the guard to the point as the charge fills, its glow rising, blood running off its edge."),
    ]
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


FX_OLD = """    oathwound: { mode: 'beam', n: 1250, sp: [25, 140], grav: -60, drag: 1.3,
                 life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
                 spawn: 0.50, up: 0 },
"""


def fx_out(s: str):
    """SPECS.oathwound out of the INLINED copy, stamp re-cut -- exactly what the orchestrator's
    sync_fx_remove does to both copies. Scratch: fx.js is not touched. fx.js ON DISK follows the batch
    line's tip, so the module is rebuilt from the BASE'S INLINED COPY, proved by its own stamp."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    mod = s[head.end():tm.start()].rstrip("\n") + "\n"
    assert hashlib.sha256(mod.encode("utf-8")).hexdigest() == head.group(1), "inlined copy does not match its stamp"
    assert mod.count(FX_OLD) == 1 and s.count(FX_OLD) == 1
    mod2 = mod.replace(FX_OLD, "", 1)
    s = s.replace(FX_OLD, "", 1)
    old, new = head.group(1), hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    s = s.replace(old, new).replace(old[:16], new[:16])
    head2 = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm2 = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head2.end())
    assert s[head2.end():tm2.start()].rstrip("\n") == mod2.rstrip()
    return s, old, new


def build(out: pathlib.Path, fxout=False, src=None):
    s = src_text(src)
    if src is None:
        assert hashlib.sha256(s.encode("utf-8")).hexdigest()[:16] == BASE_SHA16, "base moved"
    R = rows(s)
    o = apply_all(s, R)
    info = {}
    if fxout:
        o, old, new = fx_out(o)
        info = {"fx_old": old, "fx_new": new}
    for bad in ("rng()", "spawnFx", "Math.random", "ultFx"):
        for r in R:
            assert bad not in strip_comments(r["code"]), (r["label"], bad)
    assert strip_comments(o).count("Math.random") == strip_comments(s).count("Math.random")
    n = syntax_check(o)
    out.write_bytes(o.encode("utf-8"))
    return n, len(o) - len(s), info


def stamp_of(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    n, d, _ = build(HERE / "gs-final.html")
    print(f"gs-final.html: {n} script blocks parse, {d:+d} chars, stamp {stamp_of((HERE / 'gs-final.html').read_bytes().decode('utf-8'))}")
    n, d, info = build(HERE / "gs-final-fx.html", fxout=True)
    print(f"gs-final-fx.html: {n} script blocks parse, {d:+d} chars, fx.js stamp {info['fx_old'][:16]} -> {info['fx_new'][:16]}, page {stamp_of((HERE / 'gs-final-fx.html').read_bytes().decode('utf-8'))}")
