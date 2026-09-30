"""ROOTFAST'S PICTURE (v85 section 4, the brief's stage 4 = the build's stage 6) as exactly-once edits to
Heartwood's final link (heartwood/links/sc-heartwood-b11.html, aff84a04b303a402 = sc-tendril-t3 + stages 1,2,3,5).

rows(src) -> the deliverable rows (numbers inlined from PICK). NO lab variant: every component is its own
renderer method, so the harnesses hide one by shadowing that method on the renderer from outside the page, and
the bytes measured are the bytes delivered (Ironhail's stage-6 pattern).

THE ROOT IS TENDRIL'S PICTURE, REUSED (v85 section 4: "the Tendril floor-root picture (four thorn shoots up the
rim, dark with core tips, for the pin's length; the runic hexagon skipped)"). These rows only MARK the held ball
(`twineHeld`, `twineRootFade`, `twineHeldAge`, `twineHeldOut`) when a root lands; Tendril's own `tickTwine`
(generic over both balls), `_twineRoot` (drawn from `drawTwine` / `drawTwineTop`) and `_drawField`'s guard
`!(f.twineHeld > 0)` grow it, hold it, wilt it and leave Paradox's hexagon off the ball. That picture is Bindweed's
stage 6, on 02-chain/sc-tendril-fx and every later tip, and NOT on this base: on the stamp link (b11 + rows) the
markers are inert and a held ball still draws the hexagon. The picture's gates are therefore measured on the real
carry (tools/heartwood_build.py 1,2,3,5 --src 02-chain/sc-tendril-fx.html, then these rows).

build(out, src=None, fxout=False) -> the page (fxout: SPECS.heartwood out of the INLINED fx.js copy, stamp re-cut
from that copy -- what the orchestrator's fx_remove does to both copies; scratch only, fx.js is never touched).
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
BASE = (HERE.parent / "links" / "sc-heartwood-b11.html").resolve()
TIP = HERE / "carry" / "hw-on-sc-tendril-fx.html"

PICK = dict(
    GREEN=0.6,      # the cast's greening, hilt to tip, half-seconds (v85: 0.3s)
    WITHER=0.8,     # the close's wither, tip to hilt, half-seconds (0.4s; Tendril's)
    STEP=12,        # one leaf pair per 12 units of blade (Tendril's leaf scale)
    LEAFL=8.4,      # a scale leaf's length, units
    LEAFA=0.85,     # ... and its angle off the blade, radians (forward and out)
    MOTES=1.6,      # leaf motes per presentation-second (x2 on the normal path: 3.2/s)
    MOTELIFE=2.4,   # half-seconds (1.2s)
    BITLIFE=1.5,    # the wither's falling leaves, half-seconds (0.75s)
    GRAV=420,       # ... their fall
)


def src_text(p=None) -> str:
    return pathlib.Path(p or BASE).read_bytes().decode("utf-8")


# ---------------------------------------------------------------------------
# 1. the fighter's picture state
FIGHTER_ANCHOR = "    this.ultRoot = null;\n    this.rootTally = null;\n"
FIGHTER_CODE = """    /* ROOTFAST'S PICTURE (v85 section 4), and none of it is the window: the
       green outlives `ultRoot` by its 0.4s wither, so the picture keeps its
       own state. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickGrove`); nothing in the simulation reads any of it. `grove`, not
       `root`: the simulation owns `rootTally`, `rootBlow` and `rootFor`.
         groveFade -- 1 while the window stands; eased to 0 over the wither
           after the close or the match's end; 0 at once when the caster falls
         groveAge -- the presentation clock since the cast (the greening)
         groveOut -- the presentation clock since the close (the wither)
         groveRoots, groveRooted -- the holds and the roots already shown
           (`rootTally.roots`, `rootTally.rooted`)
         groveMotes -- leaf motes shed off the green blade (records): the
           sprout's leaves at the cast, then sparse ones for the window
         groveSprout -- stations of the leaf scale the cast's green has passed
         groveBits -- the wither's falling leaves (records)
         groveDrop -- leaf pairs the wither has let go, from the tip
         groveMoteN, groveMoteAcc -- the motes' count and spawn accumulator
       THE ROOT IS TENDRIL'S PICTURE, REUSED (v85 section 4): a root marks
       the held ball's `twineHeld` / `twineRootFade` / `twineHeldAge` /
       `twineHeldOut`, and Tendril's own `tickTwine`, `_twineRoot` and
       `_drawField`'s held-ball guard grow the four shoots, hold them for the
       pin, wilt them, and leave Paradox's hexagon off the ball. */
    this.groveFade = 0;
    this.groveAge = 0;
    this.groveOut = 0;
    this.groveRoots = 0;
    this.groveRooted = 0;
    this.groveMotes = [];
    this.groveSprout = 0;
    this.groveBits = [];
    this.groveDrop = 0;
    this.groveMoteN = 0;
    this.groveMoteAcc = 0;
"""

# ---------------------------------------------------------------------------
# 2. the presentation clock: one call at the head of tickPresentation
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickGrove(dt);                 // ROOTFAST'S PICTURE (v85 section 4)\n"

TICK_ANCHOR = "  tickWinnow(dt){\n"
TICK_CODE = """  /* ------------------------------------------------ ROOTFAST'S PICTURE ---
     v85 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step and once in a
     hit stop, so the cast's greening plays through the cast's own 0.08s
     stop): %GREEN% is the 0.3s greening, %WITHER% the 0.4s wither. Everything
     is read off the simulation -- the window, the blade's own angle and
     reach, the tally's counters rising -- so the simulation makes no call for
     it, and nothing here writes a field the simulation reads: the picture's
     own fields, the held ball's four `twine*` markers (read only by Tendril's
     root picture and `_drawField`'s guard) and a tag's printed count.
     Not after the match and not once the caster falls: `tickRootfast` never
     runs again once `over` is set, so `ultRoot` would otherwise stand
     through the verdict. */
  tickGrove(dt){
    const R = CONFIG.physics.ballR, ST = %STEP%;
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a, T = f.rootTally;
      for (let i = f.groveMotes.length - 1; i >= 0; i--){
        f.groveMotes[i].t += dt;
        if (f.groveMotes[i].t >= %MOTELIFE%) f.groveMotes.splice(i, 1);
      }
      for (let i = f.groveBits.length - 1; i >= 0; i--){
        f.groveBits[i].t += dt;
        if (f.groveBits[i].t >= %BITLIFE%) f.groveBits.splice(i, 1);
      }
      if (!T) continue;
      /* A BALL THAT HOLDS ITSELF IS ITS OWN PICTURE'S: Canopy roots its own
         ball for its window (`pin` with `pinFree`, re-set every step), and
         its own aerial roots draw that hold. A root landing on it marks
         nothing, and a root it already carried lets go when its own takes
         over -- the shoots would otherwise stand for the canopy's whole
         window, saying this sword holds a ball it does not. Heartwood's
         opponent is rooted by nothing else, so every mark here is this
         caster's. */
      if (foe.twineHeld && foe.pinFree) foe.twineHeld = 0;
      /* THE ROOT, off the tally: `rooted` counts every root, `roots` the new
         holds (a ball that was not already held). A new hold brings the four
         shoots up out of the floor; a re-root of a held ball keeps them up
         and fresh (the pin is back at its full second, so the wilt goes).
         A killing blow roots nobody, and `rootBlow` counts neither. */
      if (T.rooted !== f.groveRooted){
        const hold = T.roots !== f.groveRoots;
        f.groveRooted = T.rooted; f.groveRoots = T.roots;
        if (foe.alive && foe.pin > 0){
          if (!foe.pinFree){
            if (hold || !(foe.twineRootFade > 0)) foe.twineHeldAge = 0;
            foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldOut = 0;
          }
          /* A ROOTED FOE CARRIES THE ENTANGLE TAG, WITH ITS COUNT. The blow
             tagged ENTANGLE at the contact this step (`resolveHit`, before
             the root's +1, and with no count); that tag now prints the count
             the root leaves. The first-ever tag is the teaching panel and
             prints no count, so it is left alone. */
          const n = foe.stacks("entangle");
          for (let i = this.tags.length - 1; i >= 0; i--){
            const g = this.tags[i];
            if (g.key !== "entangle" || g.max - g.life > 0.1
                || Math.hypot(g.x - foe.x, g.y - foe.y) >= R * 3) continue;
            if (!g.first) g.val = n;
            break;
          }
        }
      }
      const Z = (this.over || !f.alive) ? null : f.ultRoot;
      if (Z){
        if (!(f.groveFade > 0) || f.groveOut > 0){                // a new window
          f.groveAge = 0; f.groveOut = 0; f.groveDrop = 0; f.groveSprout = 0;
        }
        f.groveFade = 1;
        f.groveAge += dt;
        /* THE SPROUT: as the green's front passes each station of the leaf
           scale, the pair there sheds a leaf -- the blade bursts into leaf at
           the cast. Then LEAF MOTES shed off it, sparse, for the window. Both
           drawn, in place of a field on the one ultFx slot; placed by the
           blade and by shellHash on their count: no rng. */
        {
          const B = this.groveBlade(f), xF = B.L * (Math.min(1, f.groveAge / %GREEN%) * 1.04 - 0.02);
          const n = Math.floor(B.L * 0.74 / ST);
          while (f.groveSprout < n && B.L * 0.20 + (f.groveSprout + 1) * ST <= xF){
            const k = ++f.groveSprout, x = B.L * 0.20 + k * ST, y = this.groveHalf(B.L, f.w.artW, x);
            for (const sd of [-1, 1])
              f.groveMotes.push({ x: B.x + B.ux * x - B.uy * y * sd, y: B.y + B.uy * x + B.ux * y * sd,
                                  t: 0, n: f.groveMoteN++, big: 1 });
          }
        }
        f.groveMoteAcc += dt * %MOTES%;
        while (f.groveMoteAcc >= 1){
          f.groveMoteAcc -= 1;
          const B = this.groveBlade(f), k = f.groveMoteN++;
          const x = B.L * (0.28 + 0.66 * shellHash(9851 + f.side, k));
          if (x > B.L * (Math.min(1, f.groveAge / %GREEN%) * 1.04 - 0.02)) continue;
          const y = (shellHash(9853 + f.side, k) - 0.5) * 1.6 * this.groveHalf(B.L, f.w.artW, x);
          f.groveMotes.push({ x: B.x + B.ux * x - B.uy * y, y: B.y + B.uy * x + B.ux * y, t: 0, n: k });
        }
        if (f.groveMotes.length > 24) f.groveMotes.splice(0, f.groveMotes.length - 24);
      } else if (f.groveFade > 0){
        if (!f.alive){ f.groveFade = 0; f.groveOut = 0; continue; }   // the shatter owns it
        f.groveFade = Math.max(0, f.groveFade - dt / %WITHER%);
        f.groveOut += dt;
        /* THE BROWN RUNS TIP TO HILT (reaching the hilt at three quarters of
           the wither), and each leaf pair it passes lets go: the same
           stations `_groveScale` draws, on the blade as it stands. */
        const B = this.groveBlade(f), fr = Math.min(1, f.groveOut / %WITHER% / 0.75);
        const n = Math.floor(B.L * 0.74 / ST);
        let passed = 0;
        for (let k = 1; k <= n; k++) if (B.L * 0.20 + k * ST >= (1 - fr) * B.L) passed++;
        const ang = Math.atan2(B.uy, B.ux);
        while (f.groveDrop < passed){
          const k = n - f.groveDrop++;
          if (k < 1) break;
          const x = B.L * 0.20 + k * ST, y = this.groveHalf(B.L, f.w.artW, x);
          for (const sd of [-1, 1])
            f.groveBits.push({ x: B.x + B.ux * x - B.uy * y * sd, y: B.y + B.uy * x + B.ux * y * sd,
                               a: ang + sd * %LEAFA%, t: 0,
                               vx: (shellHash(9855 + f.side, k * 2 + sd) - 0.5) * 60,
                               vy: -10 - 30 * shellHash(9857 + f.side, k * 2 + sd),
                               spin: (shellHash(9859 + f.side, k * 2 + sd) - 0.5) * 7 });
        }
      }
    }
  }

  /* The blade in the hall, exactly as `drawWeapon` draws it: its base at
     R - 6 out along the swing angle, its axis, its length (the art's
     `reach + 6`). Heartwood swings one blade (`blades:[0]`). Pure. */
  groveBlade(f){
    const R = CONFIG.physics.ballR, a = f.theta + (f.bladeSet || f.w.blades)[0] * TAU;
    const ux = Math.cos(a), uy = Math.sin(a);
    return { x: f.x + ux * (R - 6), y: f.y + uy * (R - 6), ux, uy,
             L: f.w.reach * this.actMods.reach * f.reachMul + 6 };
  }
  /* The leaf blade's half-width at `x` along it (`_gsGrown`'s margin, art
     width `W`). Pure. */
  groveHalf(L, W, x){
    const u = clamp((x - L * 0.20) / (L * 0.80), 0, 1);
    return W * 0.19 * 1.5 * Math.sin(Math.PI * u) * 0.96;
  }

"""

# ---------------------------------------------------------------------------
# 3. the render call: the world pass, under both balls
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* ROOTFAST'S GROUND (v85 section 4): the leaf motes shed off the green
       blade and the wither's falling leaves. The WORLD pass and under both
       balls: nothing of it reaches the bloom (CLAUDE.md section 4.1c) and no
       ball's disc is painted over (4.1b). The root's four shoots are
       Tendril's own calls (`drawTwine`, `drawTwineTop`). */
    if (__world) this.drawGrove(m);
"""

# ---------------------------------------------------------------------------
# 4. drawWeapon's hook, in the blade's own frame
HOOK_ANCHOR = "        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);\n      }\n"
HOOK_CODE = """      /* ROOTFAST (v85 section 4): for the window the verdant blade greens,
         hilt to tip over the cast's 0.3s, with a leaf scale along it, and
         withers after the close (`_groveBlade`), over the shape in the
         shape's own frame. `groveFade` is 0 on every other relic, so this
         is one comparison on a field nothing else writes. */
      if (f.groveFade > 0 && f.w.shape === "greatsword") this._groveBlade(c, m, f, reach + 6, f.w.artW);
"""

# ---------------------------------------------------------------------------
# 5. the drawing methods, before drawMotes
DRAW_ANCHOR = "  drawMotes(m){\n"
DRAW_CODE = """  /* --------------------------------------------------------- THE GROVE ---
     ROOTFAST (v85 section 4). THE CAST: the sword greens from hilt to tip
     over 0.3s -- sap up the grip, then the leaf blade from steel to living
     green, a bright front crossing it -- and the leaf scale sprouts along
     both margins as the green passes: a pair every 12 units, Tendril's scale
     on a sword. THE WINDOW: the blade stays green and sheds leaf motes (drawn,
     in place of a field on the one ultFx slot); the cast's sprout sheds a
     leaf off each pair as the green reaches it. THE ROOT is Tendril's four
     shoots out of the floor, up the held ball's rim, for the pin's second,
     in place of Paradox's hexagon (marked in `tickGrove`, drawn by
     `_twineRoot`); the blow's ENTANGLE tag carries the count the root
     leaves. THE CLOSE: brown runs tip to hilt over 0.4s and every leaf pair
     it passes lets go and falls; the green fades and the steel is back.

     IT HANGS OFF THE FIGHTER (`groveFade`, `groveAge`, `groveOut`, the
     records), never `m.ultFx` (open item 25). PRESENTATION ONLY: no rng, no
     spawnFx, no Math.random -- shellHash and the clocks -- and nothing here
     writes a field the simulation reads. */
  drawGrove(m){
    const a = m.a, b = m.b;
    if (!a.groveMotes.length && !b.groveMotes.length
        && !a.groveBits.length && !b.groveBits.length) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.groveMotes.length) this._groveMotes(f);
      if (f.groveBits.length) this._groveBits(f);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE LEAF MOTES: shed off the blade, drifting down and swaying -- the
     sprout's leaves as the scale draws them (the school's core, a dark
     edge), the window's sparse ones small and pale */
  _groveMotes(f){
    const c = this.ctx, P = f.aff;
    c.lineWidth = 1;
    for (const q of f.groveMotes){
      const s = q.t * 0.5, k = q.t / %MOTELIFE%, h = shellHash(9861 + f.side, q.n);
      const x = q.x + Math.sin(s * 3.1 + h * 6.28) * 5 + (h - 0.5) * 18 * s;
      const y = q.y + 18 * s + 10 * s * s;
      c.globalAlpha = 0.9 * (1 - k) * Math.min(1, k * 8);
      c.beginPath();
      if (q.big){
        this._groveLeaf(c, x, y, s * 2.4 + h * 6.28, %LEAFL%, %LEAFL% * 0.42);
        c.fillStyle = P.core; c.fill(); c.strokeStyle = P.dark; c.stroke();
      } else {
        this._groveLeaf(c, x, y, s * 2.4 + h * 6.28, 4.4, 1.8);
        c.fillStyle = P.glow; c.fill();
      }
    }
  }

  /* THE WITHER'S LEAVES, falling off the blade */
  _groveBits(f){
    const c = this.ctx;
    for (const d of f.groveBits){
      const s = d.t * 0.5, k = d.t / %BITLIFE%;
      c.save();
      c.translate(d.x + d.vx * s, d.y + d.vy * s + %GRAV% * s * s);
      c.rotate(d.a + d.spin * s);
      c.globalAlpha = (1 - k * k) * 0.95;
      c.beginPath(); this._groveLeaf(c, 0, 0, 0, %LEAFL%, %LEAFL% * 0.4);
      c.fillStyle = "#8A7A3A"; c.fill();
      c.strokeStyle = "#2A2012"; c.lineWidth = 1; c.stroke();
      c.restore();
    }
  }

  /* THE BLADE, from `drawWeapon`, in the blade's frame (x along it from its
     base, the art's length `L` and width `W`), over the shape just drawn. */
  _groveBlade(c, m, f, L, W){
    const live = !!(f.ultRoot && !m.over && f.alive);
    const g = live ? Math.min(1, f.groveAge / %GREEN%) : 1;
    const b = live ? 0 : Math.min(1, f.groveOut / %WITHER%), fr = Math.min(1, b / 0.75);
    const q = clamp((b - 0.6) / 0.4, 0, 1), al = 1 - q * q * (3 - 2 * q);
    if (!(al > 0.01)) return;
    const xF = L * (g * 1.04 - 0.02);                  // the green's front, from the grip
    const xB = L * (1 - fr);                           // the brown's front, from the tip
    c.save();
    c.globalAlpha *= al;
    c.lineCap = "round"; c.lineJoin = "round";
    this._groveGreen(c, L, W, f.aff, xF, xB);
    this._groveScale(c, L, W, f.aff, xF, xB, f.groveDrop);
    if (g < 1) this._groveFront(c, L, W, f.aff, xF, g);
    c.restore();
  }

  /* The leaf blade gone living: `_gsGrown`'s own outline, filled green up to
     the front (a lit upper margin, the school's core a shade down, a dark
     underside: picked on measurement, the most change against the steel that
     keeps the blade off the floor -- |dL| 0.189 and dE 32 against the steel,
     0.164 against the floor where the steel is 0.188), sap
     up the grip, the midrib and veins re-cut dark with a pale seam; past the
     brown's front, dead. */
  _groveGreen(c, L, W, P, xF, xB){
    const bh = W * 0.19, x1 = Math.min(xF, L * 1.02);
    if (!(x1 > -L * 0.02)) return;
    const leaf = () => {
      c.beginPath(); c.moveTo(L * 0.20, 0);
      c.bezierCurveTo(L * 0.34, -bh * 1.55, L * 0.72, -bh * 1.45, L, 0);
      c.bezierCurveTo(L * 0.72, bh * 1.45, L * 0.34, bh * 1.55, L * 0.20, 0);
      c.closePath();
    };
    c.save();
    c.beginPath(); c.rect(-L * 0.05, -W * 2, x1 + L * 0.05, W * 4); c.clip();
    c.strokeStyle = P.core; c.lineWidth = Math.max(1, W * 0.06);          // sap up the grip
    c.beginPath(); c.moveTo(-L * 0.01, W * 0.02); c.lineTo(L * 0.20, 0); c.stroke();
    leaf();
    const gr = c.createLinearGradient(0, -bh * 1.5, 0, bh * 1.5);
    gr.addColorStop(0, mix(P.core, P.glow, 0.15)); gr.addColorStop(0.45, mix(P.core, P.dark, 0.2));
    gr.addColorStop(1, mix(P.core, P.dark, 0.7));
    c.fillStyle = gr; c.fill();
    if (xB < x1){                                                          // the dead part
      c.save();
      c.beginPath(); c.rect(xB, -W * 2, L * 1.1 - xB, W * 4); c.clip();
      leaf();
      const gb = c.createLinearGradient(0, -bh * 1.5, 0, bh * 1.5);
      gb.addColorStop(0, "#8A7A3A"); gb.addColorStop(0.5, "#6E5B2E"); gb.addColorStop(1, "#2A2012");
      c.fillStyle = gb; c.fill();
      c.restore();
    }
    c.strokeStyle = P.dark;                                                // the midrib
    c.lineWidth = Math.max(1, W * 0.05);
    c.beginPath(); c.moveTo(L * 0.22, 0); c.lineTo(L * 0.98, 0); c.stroke();
    c.lineWidth = Math.max(1, W * 0.026);                                  // and its veins
    c.beginPath();
    for (let i = 1; i <= 5; i++){
      const u = i / 6, x = L * (0.24 + 0.68 * u), y = bh * 1.40 * Math.sin(Math.PI * u);
      for (const sg of [-1, 1]){ c.moveTo(x - L * 0.05, 0); c.lineTo(x + L * 0.03, sg * y * 0.72); }
    }
    c.stroke();
    c.globalAlpha *= 0.6; c.strokeStyle = P.glow; c.lineWidth = Math.max(0.8, W * 0.018);
    c.beginPath(); c.moveTo(L * 0.24, -W * 0.012); c.lineTo(Math.min(xB, L * 0.94), -W * 0.012); c.stroke();
    c.restore();
  }

  /* THE LEAF SCALE: a leaf pair every 12 units along both margins, each
     sprouting as the green's front passes it; dead past the brown's front,
     and the `drop` pairs nearest the tip already let go. */
  _groveScale(c, L, W, P, xF, xB, drop){
    const ST = %STEP%, n = Math.floor(L * 0.74 / ST), live = [], dead = [];
    for (let k = 1; k <= n - drop; k++){
      const x = L * 0.20 + ST * k, sc = clamp((xF - x) / (ST * 0.8), 0, 1);
      if (!(sc > 0.02)) continue;
      const u = (x - L * 0.20) / (L * 0.80), y = W * 0.19 * 1.5 * Math.sin(Math.PI * u) * 0.96;
      (x > xB ? dead : live).push([x, y, sc]);
    }
    for (const [list, fill, edge] of [[live, P.core, P.dark], [dead, "#8A7A3A", "#2A2012"]]){
      if (!list.length) continue;
      c.beginPath();
      for (const [x, y, sc] of list)
        for (const sd of [-1, 1])
          this._groveLeaf(c, x - ST * 0.25, sd * (y - 1.4), sd * %LEAFA%, %LEAFL% * sc, %LEAFL% * sc * 0.42);
      c.fillStyle = fill; c.fill();
      c.strokeStyle = edge; c.lineWidth = 1.1; c.stroke();
    }
  }

  /* The green's front crossing the blade in the cast's 0.3s: a pale bar */
  _groveFront(c, L, W, P, xF, g){
    if (!(xF > 0)) return;
    const h = xF < L * 0.20 ? W * 0.10
            : W * 0.19 * 1.5 * Math.sin(Math.PI * clamp((xF - L * 0.20) / (L * 0.80), 0, 1)) + 2.5;
    c.globalAlpha *= 0.35 + 0.65 * (1 - g);
    c.strokeStyle = P.glow; c.lineWidth = 2.6;
    c.beginPath(); c.moveTo(xF, -h); c.lineTo(xF, h); c.stroke();
  }

  /* One leaf, base at (x, y), pointing along `a`: added to the current path. */
  _groveLeaf(c, x, y, a, L, W){
    const ux = Math.cos(a), uy = Math.sin(a);
    c.moveTo(x, y);
    c.quadraticCurveTo(x + ux * L * 0.5 - uy * W, y + uy * L * 0.5 + ux * W, x + ux * L, y + uy * L);
    c.quadraticCurveTo(x + ux * L * 0.5 + uy * W, y + uy * L * 0.5 - ux * W, x, y);
  }

"""

# ---------------------------------------------------------------------------
# 6. the freeze's picture, retired
UNDER_HEAD = "    /* ---- Rootfast: the root PLATE, spreading from the quarry outward ------- */\n"
UNDER_CODE = """    /* ---- Rootfast's root plate was the FREEZE's (eleven roots run out from
       the quarry at the cast, over the record's 2.2); retired with it (v85,
       v112 stage 6). The root is now every blow's, drawn off the held ball
       (Tendril's four shoots, `_twineRoot`), and the window's picture hangs
       off the caster (`_groveBlade`, `drawGrove`), where the one ultFx slot
       cannot erase it. */
"""
OVER_HEAD = "    /* ---- Rootfast: a cage grown UP over the quarry, then browning ---------- */\n"
OVER_CODE = """    /* ---- Rootfast's cage was the FREEZE's (nine stems arching over the
       quarry, browning over the record's 2.2); retired with it (v85, v112
       stage 6). The cast is the blade greening hilt to tip (`_groveBlade`). */
"""
LIFE_ANCHOR = "              oathwound: 1.5, heartwood: 2.2, "
LIFE_CODE = """              /* ROOTFAST IS NO LONGER A FREEZE (v85; v112 stage 6): its 2.2
                 went out with the root plate and the cage, so the first line
                 above is Bramblesnare's alone. The cast's record falls to the map's
                 own 1.5 and carries the CAST only -- nothing draws from it. */
              oathwound: 1.5, """


def branch(s: str, head: str) -> str:
    """The retired branch whole: its header comment through the `}` that closes it (the text up to the
    blank line before the next section's header)."""
    i = s.index(head)
    assert s.count(head) == 1, head
    j = s.index("\n\n    /* ---- ", i)
    old = s[i:j + 1]
    assert old.rstrip().endswith("}") and 'else if (u.w === "heartwood"){' in old, old[-200:]
    return old


def rows(s: str | None = None):
    s = s if s is not None else src_text()

    def fill(code):
        for k, v in PICK.items():
            code = code.replace("%" + k + "%", repr(v) if not isinstance(v, str) else v)
        left = re.findall(r"%[A-Z_]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="rootfast picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the green outlives ultRoot by its wither); never m.ultFx (open item 25). Read by nothing in the simulation."),
        dict(label="rootfast picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickGrove."),
        dict(label="rootfast picture: tickGrove", anchor=TICK_ANCHOR, mode="before", code=TICK_CODE,
             why="Drives the greening (off ultRoot && !over && alive), the leaf motes (shellHash), the wither and its falling leaves; marks the held ball for Tendril's root picture on rootTally.rooted rising (a new hold on rootTally.roots rising) and sets the blow's own ENTANGLE tag's count after the root's +1. Writes presentation fields, the twine* markers and a tag's val only."),
        dict(label="rootfast picture: the ground call (world, under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls: the leaf motes and the wither's leaves (bloom share 0; no disc painted over)."),
        dict(label="rootfast picture: the blade's hook in drawWeapon", anchor=HOOK_ANCHOR, mode="after", code=HOOK_CODE,
             why="While groveFade > 0 the verdant blade is drawn green with its leaf scale over the shape, in the shape's own frame; SHAPES.greatsword/_gsGrown untouched, so the resting silhouette and every other greatsword are the shipped ones."),
        dict(label="rootfast picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawGrove and one method a component: _groveMotes, _groveBits, _groveBlade (_groveGreen, _groveScale, _groveFront), _groveLeaf."),
        dict(label="rootfast picture: the freeze's root plate retired", anchor=branch(s, UNDER_HEAD), mode="replace", code=UNDER_CODE,
             why="drawUltUnder's heartwood branch was the FREEZE's plate (eleven roots from the quarry at radius 300 now that u.radius is gone); the freeze is out (v112 stage 1), so its picture goes too."),
        dict(label="rootfast picture: the freeze's cage retired", anchor=branch(s, OVER_HEAD), mode="replace", code=OVER_CODE,
             why="drawUltOver's heartwood branch was the FREEZE's cage over the quarry; retired with the freeze."),
        dict(label="rootfast picture: the cast record's life", anchor=LIFE_ANCHOR, mode="replace", code=LIFE_CODE,
             why="heartwood: 2.2 was long because the freeze's art explained a hold; nothing draws from the record now, so it falls to the map's 1.5 (the cast's record only)."),
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


FX_OLD = """    heartwood: { mode: 'fall', n: 1050, sp: [30, 120], grav: 110, drag: 1.0,
                 life: [0.80, 1.70], heavy: 0.02, size: [0.6, 1.9],
                 spawn: 0.85, up: 0 },
"""
FX_HEAD = re.compile(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n")


def fx_out(s: str):
    """SPECS.heartwood out of the INLINED copy, its stamp re-cut from that copy (the base's inlined copy is the
    reference: src/render/fx.js on disk follows the batch line's tip and may differ). Scratch only."""
    head = FX_HEAD.search(s)
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    mod = s[head.end():tm.start()]
    assert mod.count(FX_OLD) == 1 and s.count(FX_OLD) == 1, "SPECS.heartwood is not the base's text"
    mod2 = mod.replace(FX_OLD, "", 1)
    old = head.group(1)
    new = hashlib.sha256((mod2.rstrip("\n") + "\n").encode("utf-8")).hexdigest()
    s = s.replace(FX_OLD, "", 1).replace(old, new).replace(old[:16], new[:16])
    return s, old, new


def build(out: pathlib.Path, src=None, fxout=False):
    s = src_text(src)
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
    pathlib.Path(out).write_bytes(o.encode("utf-8"))
    return n, len(o) - len(s), info


def stamp_of(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


def stamp() -> str:
    s = src_text()
    return stamp_of(apply_all(s, rows(s)))


if __name__ == "__main__":
    for name, src, fx in (("hw-final.html", None, False), ("hw-final-fx.html", None, True),
                          ("hw-tip.html", TIP, False), ("hw-tip-fx.html", TIP, True)):
        n, d, info = build(HERE / name, src, fx)
        print(f"{name}: {n} script blocks parse, {d:+d} chars, sha {stamp_of((HERE / name).read_bytes().decode('utf-8'))}"
              + (f", fx.js stamp {info['fx_old'][:16]} -> {info['fx_new'][:16]}" if info else ""))
    print("STAMP (b11 + rows only):", stamp())
