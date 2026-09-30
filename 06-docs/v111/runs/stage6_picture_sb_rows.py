"""UNMAKING'S PICTURE (v79 section 4, "Picture") as exactly-once edits to Spellbreaker's final link
(spellbreaker/links/sc-spellbreaker-b7.5.html, da7936dccd8f5f15 = sc-tendril-t3 + spellbreaker stages 1, 2, 3, 5).

rows() -> the deliverable rows (numbers inlined from PICK). There is NO lab variant of the rows: every
component is its own renderer method, so the harnesses hide one by shadowing that method on the renderer
instance from outside the page, and the bytes measured are the bytes delivered.

build(out)            -> sb-final.html     the base + these rows: THE STAMP
build(out, fxout=1)   -> sb-final-fx.html  the same, with SPECS.spellbreaker (the bolt's 'beam' field) taken out
                        of the INLINED fx.js copy and both stamps re-cut -- what the orchestrator does to both
                        copies at the carry. That is the look as it ships, so the gates are measured on it.

THE DESIGN'S PICTURE (v79 section 4), and each reading this build makes (none a mechanic):
  "the bolt art is retired" -- drawUltOver's bolt branch (the jagged bolt, its glyphs and the cage of rings
     on the target; it drew Math.random), the banner's seat on the quarry (`onTarget`: the name landed
     where the bolt struck; it now lands on her, where the script is), and the cast record's `life` 1.4 (the
     bolt's set-piece length; the record falls to the map's own 1.5 and nothing draws from it).
     KEPT: the charge rune ULTSIG.spellbreaker ("a rune that comes APART", the name, not the bolt) and the
     banner's letter scatter (the name's own arrival; it throws UNMAKING's letters in and takes them apart).
  R1 "Cast: rune-script runs along both blades and stays (runic `core` glyphs, 0.3s)": one rune a shard,
     five a blade, on the conjured twinblade's own shards (riding each shard's drift and cant, so the script
     is IN the weapon), written hilt to tip over 0.3s behind a bright writing point, standing for the
     window. The school's `core` (#4A9EFF) over a keyline in the blade's own silhouette ink (#040814):
     core on a blade whose middle is core would vanish without it. A different run of runes on each blade.
  R2 THE CLOSE (the design gives no picture; the voice is "the hum cutting out"): the script unwrites tip
     to hilt over 0.2s -- on a clock close, a death, or the match's end (`tickUnmake` never runs again once
     `over` is set, so a script standing at the kill would otherwise stand through the verdict).
  R3 "make the DOUBLE-LENGTH stun visible -- the foe's weapon greys out (desaturated, alpha 0.6) for the
     stun's length": a hex proc AT x2 greys the weapon it stuns (the canvas's own `grayscale(1)` over the
     whole weapon, every school and every type, at alpha 0.6 where a plain stun draws it at 0.42 in colour)
     for THAT stun's own 0.4s, counted down by the stun's own countdown -- so it freezes through a hit stop
     exactly as the stun does, ends when the stun ends, and does not outlive its own 0.4s under a longer
     stun from something else (a clash). The proc is found by the foe's `hexClock` dropping (only the
     proc resets it) and its factor is the `hexStunMul` the proc read (as last seen: tickUnmake rewrites
     it later in the same step), so a proc on the step the window closes is still x2. A plain stun keeps
     the base's 0.42 dim; a shade (x1 always) never greys.
  R4 "The hex tag counts by two": a blow in the window whose second hex lands prints `HEX +2` where the
     channel's own tag printed `HEX` -- the tag the blow pushed, relabelled, found as a hex tag pushed
     since the last presentation call (tags age in tickPresentation after this ticker) on a step her
     `unmakeTally.extra` rose; not the killing blow (no second hex), not the match's first hex (its
     teaching panel prints no count). +2 is the channel's hex 1 plus `hexExtra` 1, read off the relic.
  R5 "Field: rune motes off the blades, both copies": DRAWN, not an fx.js field (fxprobe.out: the one
     ultFx slot fires once, where she cast, and the blades ride her for 8s). Tiny runes shed off both
     blades while the window is open, left where they were shed and drifting out, fading; placed by
     shellHash on their count, no rng. WORLD pass, under both balls, source-over: none of it reaches
     the bloom (CLAUDE.md 4.1c) and it cannot paint over a disc (4.1b).
  Everything but the motes is drawn inside drawWeapon, which runs in the world pass only (drawFighter is
  skipped whole in the emissive pass): the picture has no bloom share by construction; the gate
  measures it anyway, with controls that must fail.
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "links" / "sc-spellbreaker-b7.5.html").resolve()

PICK = dict(
    OPEN=0.6,      # the script's write, hilt to tip, half-seconds (v79: 0.3s)
    CLOSE=0.4,     # its unwrite, tip to hilt, half-seconds (0.2s; R2)
    GREYA=0.6,     # the greyed weapon's alpha (v79: "alpha 0.6"; a plain stun is 0.42)
    GREYF="grayscale(1)",   # the canvas filter the greyed weapon is drawn through (v79: "desaturated")
    GLYPH=0.62,    # a rune's height as a share of its shard's height (R1)
    GMIN=4.5,      # ... and its floor, units (the last shard is ~6 units tall)
    MOTER=8,       # motes shed a blade per presentation half-second (R5)
    MOTEL=1.1,     # a mote's life, half-seconds (0.55s)
    MOTEV=20,      # its drift outward, units per half-second (~40 units/s)
    MOTEMAX=48,    # the cap on one fighter's list
)


def src_text(src=None) -> str:
    p = pathlib.Path(src) if src else SRC
    return p.read_bytes().decode("utf-8")


# ---------------------------------------------------------------------------
# 1. the picture's state on the fighter
FIGHTER_ANCHOR = "    this.ultUnmake = null;\n    this.unmakeTally = null;\n    this.hexStunMul = 1;\n"
FIGHTER_CODE = """    /* UNMAKING'S PICTURE (v79 section 4), and none of it is the window: the
       script unwrites for 0.2s after `ultUnmake` is gone, the motes outlive
       it, and the grey runs on the FOE's stun, not on the window. On the
       FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast takes
       it: open item 25). Driven in `tickPresentation` (`tickUnmaking`);
       nothing in the simulation reads any of it.
         unmkFade  -- 1 while the window is open; eased to 0 over the unwrite
         unmkAge   -- the presentation clock since the cast (the write)
         unmkOut   -- the presentation clock since the close (the unwrite)
         unmkMotes -- the rune motes shed off her blades, in the hall's units
         unmkMoteAcc, unmkMoteN -- the shedding clock and the motes' count
         unmkSeenX -- her `unmakeTally.extra` as last seen (the +2 tag)
       and on EVERY fighter, as the weapon the Unmaking greys:
         unmkGrey  -- what is left of a doubled hex stun's own length
         unmkHC    -- this fighter's `hexClock` as last seen (a drop is a proc)
         unmkMul   -- its `hexStunMul` as last seen (the factor a proc reads)
         unmkStun  -- its `stun` as last seen (the grey counts down with it) */
    this.unmkFade = 0;
    this.unmkAge = 0;
    this.unmkOut = 0;
    this.unmkMotes = [];
    this.unmkMoteAcc = 0;
    this.unmkMoteN = 0;
    this.unmkSeenX = 0;
    this.unmkGrey = 0;
    this.unmkHC = 0;
    this.unmkMul = 1;
    this.unmkStun = 0;
"""

# ---------------------------------------------------------------------------
# 2. the presentation call
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickUnmaking(dt);              // UNMAKING'S PICTURE (v79 section 4)\n"

# ---------------------------------------------------------------------------
# 3. tickUnmaking, right after tickUnmake
TICK_ANCHOR = ("      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : 1;\n"
               "    }\n  }\n")
TICK_CODE = """
  /* ---------------------------------------------- UNMAKING'S PICTURE ---
     v79 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): %OPEN% is the
     script's 0.3s write along both blades at the cast, %CLOSE% its 0.2s
     unwrite at the close. The window is `ultUnmake`, and not once the caster
     falls or the match ends: `tickUnmake` never runs again once `over` is
     set, so a script standing at the kill would otherwise stand through the
     verdict. Three things, none of them a call from the simulation:
       THE MOTES, shed off both blades while the window is open, left where
         they were shed and drifting out; placed by shellHash on their count.
       THE TAG: a step her `unmakeTally.extra` rose is a step a blow of hers
         landed its second hex, and the hex tag that blow pushed (a hex tag
         pushed since the last call: tags age further down this method, after
         this runs) is relabelled `HEX +2`. Not the killing blow (no second
         hex), not the match's first hex (its panel prints no count), never a
         tag on her own ball.
       THE GREY, on the fighter the Unmaking stuns: a drop in its `hexClock`
         is a hex proc (nothing else resets it), and the proc read the
         `hexStunMul` last seen here (tickUnmake rewrites it later in the
         same step). A proc at more than x1 greys the weapon for that stun's
         own `stunFor x mul`, counted down by the fighter's own stun as it
         counts down: frozen through a hit stop as the stun is, gone when
         the stun is, never past its own length under a longer stun.
     Writes presentation fields and a tag's `val` only, and draws no rng. */
  tickUnmaking(dt){
    const a = this.a, b = this.b;
    if (!a.unmakeTally && !b.unmakeTally) return;             // <- zero burden
    for (const f of [a, b]){
      /* THE GREY, on this fighter's weapon */
      const hc = f.hexClock, st = f.stun;
      if (hc < f.unmkHC && f.unmkMul > 1)
        f.unmkGrey = STATUS.hex.stunFor * f.unmkMul;
      else if (st < f.unmkStun) f.unmkGrey -= f.unmkStun - st;
      f.unmkGrey = Math.min(f.unmkGrey, st);
      if (!(f.unmkGrey > 1e-9)) f.unmkGrey = 0;
      f.unmkHC = hc; f.unmkStun = st; f.unmkMul = f.hexStunMul;
    }
    for (const f of [a, b]){
      const T = f.unmakeTally;
      if (!T) continue;
      /* THE SCRIPT'S CLOCK */
      const Z = (this.over || !f.alive) ? null : f.ultUnmake;
      if (Z){
        if (!(f.unmkFade > 0) || f.unmkOut > 0){ f.unmkAge = 0; f.unmkOut = 0; }  // a cast
        f.unmkFade = 1;
        f.unmkAge += dt;
      } else if (f.unmkFade > 0){
        f.unmkOut += dt;
        f.unmkFade = Math.max(0, 1 - f.unmkOut / %CLOSE%);
      }
      /* THE MOTES */
      const M = f.unmkMotes;
      for (let i = M.length - 1; i >= 0; i--){
        const o = M[i];
        o.t += dt; o.x += o.vx * dt; o.y += o.vy * dt;
        if (o.t >= %MOTEL%) M.splice(i, 1);
      }
      if (Z){
        f.unmkMoteAcc += dt * %MOTER%;
        const R = CONFIG.physics.ballR, W = f.w.artW;
        const L = f.w.reach * this.actMods.reach * f.reachMul + 6;
        const S = f.bladeSet || f.w.blades, sd = 7919 + 31 * f.side;
        while (f.unmkMoteAcc >= 1){
          f.unmkMoteAcc -= 1;
          for (const off of S){
            const n = f.unmkMoteN++;
            const q = f.theta + off * TAU, cq = Math.cos(q), sq = Math.sin(q);
            const u = 0.28 + 0.72 * shellHash(sd, n);                 // along the blade
            const h = (shellHash(sd + 1, n) - 0.5) * W * 0.5;         // across it
            const rr = R - 6 + L * u, v = %MOTEV% * (0.6 + 0.8 * shellHash(sd + 2, n));
            const w = (shellHash(sd + 3, n) - 0.5) * %MOTEV% * 0.8;
            M.push({ x: f.x + cq * rr - sq * h, y: f.y + sq * rr + cq * h,
                     vx: cq * v - sq * w, vy: sq * v + cq * w, t: 0, n });
          }
        }
        if (M.length > %MOTEMAX%) M.splice(0, M.length - %MOTEMAX%);
      }
      /* THE TAG */
      const dX = T.extra - f.unmkSeenX;
      f.unmkSeenX = T.extra;
      const U = f.w.ult;
      if (dX > 0 && U.hexExtra > 0){
        let k = Math.round(dX / U.hexExtra);
        const val = "+" + ((f.w.onHit && f.w.onHit.hex || 0) + U.hexExtra);
        for (let i = this.tags.length - 1; i >= 0 && k > 0; i--){
          const g = this.tags[i];
          if (g.key !== "hex" || g.first || g.life !== g.max || g.unmk) continue;
          if (g.x === f.x && g.y === f.y) continue;           // a hex ON her
          g.val = val; g.unmk = true; k--;
        }
      }
    }
  }
"""

# ---------------------------------------------------------------------------
# 4. the floor call (world, under both balls)
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* UNMAKING'S RUNE MOTES (v79 section 4, "rune motes off the blades"),
       shed off both blades and left in the hall. The WORLD pass and under
       both balls, source-over: none of it reaches the bloom (CLAUDE.md
       section 4.1c) and none of it can be painted over a disc (4.1b). The
       script and the grey are drawn with the weapon (drawWeapon). */
    if (__world) this.drawUnmaking(m);
"""

# ---------------------------------------------------------------------------
# 5. the drawing methods, after drawWeapon
DRAW_ANCHOR = ("  /* ---------------------------------------------------------------- fx --- */\n"
               "  /* Sparks are drawn as streaks along their own velocity, not as dots. Dots at\n")
DRAW_CODE = """  /* ---------------------------------------------- UNMAKING'S PICTURE ---
     v79 section 4, drawn off the fighter's `unmk*` fields -- never `m.ultFx`,
     one slot the opponent's cast takes (open item 25). One method a
     component, so each can be measured alone; nothing here keeps state or
     draws from the rng.
       drawUnmaking   the motes' pass: the world, under both balls
       _unmkMotes     one fighter's rune motes
       _unmkScript    the script on one blade (called from drawWeapon, in the
                      blade's own frame, after the shape)
       _unmkGreyed    whether this weapon is greyed this frame (drawWeapon),
       _unmkGreyFilter, _unmkGreyAlpha   and how (the design's grey)
     UNMAKING_RUNES is the script's alphabet (stroke lists in a unit box;
     its staves stand across the blade). */
  drawUnmaking(m){
    const a = m.a, b = m.b;
    if (!(a.unmkMotes && a.unmkMotes.length) && !(b.unmkMotes && b.unmkMotes.length)) return;  // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]) if (f.unmkMotes && f.unmkMotes.length) this._unmkMotes(c, m, f);
    c.globalAlpha = 1;
    c.restore();
  }
  /* A MOTE IS A RUNE, SMALL: the school's glow over a core halo, turning
     as it drifts, fading in and out over its %MOTEL_S%s. */
  _unmkMotes(c, m, f){
    const P = f.aff, G = UNMAKING_RUNES;
    for (const o of f.unmkMotes){
      const k = o.t / %MOTEL%, s = 3.4 * (1 - 0.35 * k), A = 0.85 * Math.sin(Math.PI * Math.min(1, k));
      if (!(A > 0.01)) continue;
      const g = G[o.n % G.length], r = o.n * 1.7 + k * 2.2, cr = Math.cos(r), sr = Math.sin(r);
      c.beginPath();
      for (const line of g){
        for (let j = 0; j < line.length; j++){
          const px = o.x + (line[j][0] * cr - line[j][1] * sr) * s * 2;
          const py = o.y + (line[j][0] * sr + line[j][1] * cr) * s * 2;
          j ? c.lineTo(px, py) : c.moveTo(px, py);
        }
      }
      c.globalAlpha = A * 0.55; c.strokeStyle = P.core; c.lineWidth = 2.2; c.stroke();
      c.globalAlpha = A; c.strokeStyle = P.glow; c.lineWidth = 0.9; c.stroke();
    }
  }
  /* THE SCRIPT ON ONE BLADE, in the shape's own frame (x from the hand at 0
     to the point at L). One rune a shard, written hilt to tip over the
     cast's 0.3s behind a bright writing point and unwritten tip to hilt
     over the close's 0.2s. Each rune rides its shard's own drift and cant
     (the same numbers `_twinConjured` hands `_conjure`), so the script is in
     the weapon rather than painted over it; sized to its shard's height off
     the same profile. `core` over a keyline in the blade's silhouette ink:
     the blade's middle IS core, and core on core is nothing. */
  _unmkScript(c, m, f, L, off){
    const W = f.w.artW, gap = L * 0.28, span = L - gap, bw = W * 0.52;
    const x1 = gap + span * 0.16, x2 = L * 0.97;
    const t = SHAPES._t || 0, N = 5, G = UNMAKING_RUNES, P = f.aff;
    const p = clamp(f.unmkAge / %OPEN%, 0, 1);
    const q = f.unmkOut > 0 ? clamp(f.unmkOut / %CLOSE%, 0, 1) : 0;
    const A0 = c.globalAlpha, j0 = off > 0.25 ? 2 : 0;
    const prof = (x) => {
      if (x <= x1){ const s = (x - gap) / (x1 - gap);
        return [-bw * (0.46 + 0.54 * s), bw * (0.34 + 0.46 * s)]; }
      const s = clamp((x - x1) / (x2 - x1), 0, 1);
      return [-bw * (1 - 0.87 * s), bw * (0.8 - 0.69 * s)];
    };
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (let i = 0; i < N; i++){
      const w = clamp(p * N - i, 0, 1);                       // written
      const v = 1 - clamp(q * N - (N - 1 - i), 0, 1);         // not yet unwritten
      const A = w * v;
      if (!(A > 0.01)) continue;
      const cx = gap + span * (i + 0.435) / N;
      const drift = Math.sin(t * 2.1 + i * 2.3) * W * 0.065;
      const cant = Math.sin(t * 1.6 + i * 1.4) * 0.075;
      const [y0, y1] = prof(cx);
      const h = Math.max(%GMIN%, (y1 - y0) * %GLYPH%) * (1 + 0.35 * (1 - w));
      const g = G[(i * 3 + j0 + 5 * f.side) % G.length];
      c.save();
      c.translate(cx, drift); c.rotate(cant); c.translate(0, (y0 + y1) / 2);
      c.beginPath();
      for (const line of g)
        for (let k = 0; k < line.length; k++)
          k ? c.lineTo(line[k][0] * h, line[k][1] * h) : c.moveTo(line[k][0] * h, line[k][1] * h);
      c.globalAlpha = A0 * A * 0.9; c.strokeStyle = "#040814"; c.lineWidth = h * 0.28; c.stroke();
      c.globalAlpha = A0 * A; c.strokeStyle = P.core; c.lineWidth = h * 0.13; c.stroke();
      c.globalAlpha = A0 * A * 0.8; c.strokeStyle = P.glow; c.lineWidth = h * 0.05; c.stroke();
      c.restore();
    }
    if (p < 1 && q === 0){                                    // the writing point
      const x = gap + span * p, [y0, y1] = prof(Math.min(x, x2)), y = (y0 + y1) / 2;
      const hg = c.createRadialGradient(x, y, 0, x, y, 9);
      hg.addColorStop(0, hexA(P.glow, 0.75)); hg.addColorStop(1, hexA(P.glow, 0));
      c.globalAlpha = A0; c.fillStyle = hg;
      c.beginPath(); c.arc(x, y, 9, 0, TAU); c.fill();
      c.fillStyle = "#FFFFFF";
      c.beginPath(); c.arc(x, y, 2.2, 0, TAU); c.fill();
    }
    c.restore();
  }
  _unmkGreyed(f){ return f.unmkGrey > 0; }
  _unmkGreyFilter(f){ return "%GREYF%"; }
  _unmkGreyAlpha(f){ return %GREYA%; }

"""

# the script's alphabet, a table beside SHAPES' helpers (module scope, after shellHash)
RUNES_ANCHOR = "function shellHash(a, b){\n"
RUNES_CODE = """/* UNMAKING'S SCRIPT (v79 section 4): the runes `_unmkScript` writes along
   Spellbreaker's blades and `_unmkMotes` sheds off them. Stroke lists in a
   unit box, [x, y]: x along the line of script (-0.35..0.35), y down the
   stave (-0.5..0.5), which stands across the blade. Angular staves, the look
   of a carved futhark, eight of them. */
const UNMAKING_RUNES = [
  [[[0, -0.5], [0, 0.5]], [[0, -0.12], [0.3, -0.42]], [[0, 0.14], [0.3, -0.16]]],
  [[[-0.25, 0.5], [-0.25, -0.5], [0.25, -0.2], [0.25, 0.5]]],
  [[[-0.15, -0.5], [-0.15, 0.5]], [[-0.15, -0.26], [0.22, 0], [-0.15, 0.26]]],
  [[[-0.2, 0.5], [-0.2, -0.5], [0.22, -0.26], [-0.2, 0], [0.24, 0.5]]],
  [[[0.22, -0.42], [-0.2, 0], [0.22, 0.42]]],
  [[[-0.3, -0.45], [0.3, 0.45]], [[0.3, -0.45], [-0.3, 0.45]]],
  [[[0, 0.5], [0, -0.5]], [[0, -0.02], [-0.3, -0.4]], [[0, -0.02], [0.3, -0.4]]],
  [[[0, 0.5], [0, -0.5]], [[-0.28, -0.18], [0, -0.5], [0.28, -0.18]]],
];

"""

# ---------------------------------------------------------------------------
# 6. drawWeapon: the grey (the whole weapon, desaturated) and its alpha
GREYW_ANCHOR = "  drawWeapon(m, f){\n"
GREYW_CODE = """    /* UNMAKING'S GREY (v79 section 4): "the foe's weapon greys out
       (desaturated, alpha 0.6) for the stun's length, so a longer stop is a
       longer grey". While a doubled hex stun runs (`unmkGrey`, set and
       counted down in `tickUnmaking`) the WHOLE weapon is drawn through the
       canvas's own grayscale -- every school, every type, the glow sprite
       and the lit blit alike (most weapons reach this canvas as one blit
       from `litWeapon`'s scratch, so the filter touches a handful of ops).
       Re-entered once, with the filter set, and back out. */
    if (!this._unmkGreying && this._unmkGreyed(f)){
      const c0 = this.ctx;
      c0.save();
      c0.filter = this._unmkGreyFilter(f);
      this._unmkGreying = true;
      try { this.drawWeapon(m, f); }
      finally { this._unmkGreying = false; c0.restore(); }
      return;
    }
"""
# anchored on the newline before the line: a newer tip (Angelus's ascend draw) carries the same line indented six
# spaces, and a four-space anchor matches inside it (order.py found it on sc-aureole-fxout)
DIM_ANCHOR = "\n    const dim = f.stun > 0 ? 0.42 : 1;\n"
DIM_CODE = """
    /* ... and the greyed weapon is at the design's 0.6, where a plain stun
       dims it to 0.42 in its colours: the Unmaking's stop is the grey one. */
    const dim = f.stun > 0 ? (this._unmkGreyed(f) ? this._unmkGreyAlpha(f) : 0.42) : 1;
"""

# the script, in the blade loop, after the shape
SCRIPT_ANCHOR = "      if (f.ultDraw){\n"
SCRIPT_CODE = """      /* UNMAKING'S SCRIPT (v79 section 4), on the blade just drawn, in its
         own frame: the runes the cast writes along both blades and the close
         unwrites. `unmkFade` is 0 on every other relic, so this is one
         comparison on a field nothing else writes. */
      if (f.unmkFade > 0) this._unmkScript(c, m, f, reach + 6, off);
"""


# ---------------------------------------------------------------------------
# 7. the bolt's picture, retired
def over_old(s):
    a = "    /* ---- Unmaking: struck by runes, then taken apart */\n    else if (u.w === \"spellbreaker\"){\n"
    i = s.index(a)
    e = "\n\n    /* ---- Bloodprice: a seam torn open in the air"
    j = s.index(e, i)
    return s[i:j + 1]          # through the branch's closing "    }\n"


OVER_CODE = """    /* ---- Unmaking's bolt (the jagged bolt with its glyphs, and the cage of
       rings that closed on the target and came apart) was the BOLT's picture;
       retired with it (v79 section 4, v111 stage 6). The Unmaking is drawn
       off the fighter: the script on her blades, the rune motes, the foe's
       greyed weapon (`drawWeapon`, `drawUnmaking`). The cast's record carries
       the CAST only, and nothing draws from it. */
"""
SEAT_ANCHOR = "spellbreaker:1, "
SEAT_CODE = ""
LIFE_ANCHOR = " spellbreaker: 1.4,"
LIFE_CODE = ""


def rows(src=None):
    s = src_text(src)
    pk = dict(PICK, MOTEL_S=round(PICK["MOTEL"] / 2, 3))

    def fill(code):
        for k, v in pk.items():
            code = code.replace("%" + k + "%", str(v))
        left = re.findall(r"%[A-Z_0-9]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="unmaking picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the script unwrites 0.2s past ultUnmake; the motes outlive it; the grey runs on the FOE's stun, not on the window); never m.ultFx (open item 25). Read by nothing in the sim."),
        dict(label="unmaking picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickUnmaking."),
        dict(label="unmaking picture: tickUnmaking", anchor=TICK_ANCHOR, mode="after", code=TICK_CODE,
             why="Drives the script (write 0.3s at the cast; unwrite 0.2s at a clock close, a death or the verdict), sheds the rune motes (shellHash on their count), relabels the blow's HEX tag HEX +2 on a step her unmakeTally.extra rose, and greys a weapon for a doubled hex stun's own 0.4s (the proc found by hexClock dropping, its factor the hexStunMul it read). Writes presentation fields and a tag's val only; no rng; no call from the sim."),
        dict(label="unmaking picture: the floor call (world, under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls, source-over: the rune motes (bloom share 0; no ball's disc can be painted over)."),
        dict(label="unmaking picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawUnmaking and one method a component (motes, the script on a blade, the grey test), after drawWeapon."),
        dict(label="unmaking picture: the script's runes", anchor=RUNES_ANCHOR, mode="before", code=RUNES_CODE,
             why="UNMAKING_RUNES, the eight-stave alphabet the script and the motes draw (module scope, beside shellHash)."),
        dict(label="unmaking picture: the grey (drawWeapon, the whole weapon)", anchor=GREYW_ANCHOR, mode="after", code=GREYW_CODE,
             why="While a doubled hex stun runs, the whole weapon is drawn through grayscale(1): every school and type, glow sprite and lit blit alike (v79: 'the foe's weapon greys out (desaturated ...) for the stun's length')."),
        dict(label="unmaking picture: the grey's alpha (drawWeapon)", anchor=DIM_ANCHOR, mode="replace", code=DIM_CODE,
             why="The greyed weapon at the design's alpha 0.6; a plain stun keeps the base's 0.42 dim in colour."),
        dict(label="unmaking picture: the script on each blade (drawWeapon)", anchor=SCRIPT_ANCHOR, mode="before", code=SCRIPT_CODE,
             why="The runes on the blade just drawn, in its own frame (v79: 'rune-script runs along both blades and stays')."),
        dict(label="unmaking picture: the bolt's set-piece retired", anchor=over_old(s), mode="replace", code=OVER_CODE,
             why="drawUltOver's spellbreaker branch was the BOLT's picture (the jagged bolt with glyphs, the cage of rings on the target; it drew Math.random); the bolt is out (v111 stage 1), so its picture goes too (v79: 'the bolt art is retired')."),
        dict(label="unmaking picture: the banner's seat", anchor=SEAT_ANCHOR, mode="replace", code=SEAT_CODE,
             why="fireUlt seated the name on the quarry, where the bolt struck; the Unmaking is written on her blades, so the name lands on her (the default seat). The narrowest anchor, so Thornwake's and Emberedge's seats on the same line are left alone."),
        dict(label="unmaking picture: the cast record's life", anchor=LIFE_ANCHOR, mode="replace", code=LIFE_CODE,
             why="The ultFx life entry 1.4 was the bolt's set-piece length; with nothing drawn from the slot the cast's record falls to the map's own 1.5. The narrowest anchor, so the other entries on the line are left for their own builds."),
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
    if mode == "replace" and (code.count("/*") - code.count("*/")) != (anchor.count("/*") - anchor.count("*/")):
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


FX_OLD = """    spellbreaker: { mode: 'beam', n: 1200, sp: [40, 200], grav: -40,
                    drag: 1.6, life: [0.25, 0.70], heavy: 0.0,
                    size: [0.6, 1.8], spawn: 0.35, up: 0 },
"""
HEAD = re.compile(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n")
TAIL = re.compile(r"/\* -+ THE ULT FIELDS -+")


def fx_out(s: str):
    """SPECS.spellbreaker (the bolt's field) out of the INLINED copy, both stamps re-cut from the inlined module
    itself -- what fx_remove.py does to both copies at the carry. The disk fx.js follows the batch tip, so it
    is NOT read here. Scratch only."""
    h = HEAD.search(s)
    t = TAIL.search(s, h.end())
    mod = s[h.end():t.start()].rstrip("\n") + "\n"
    old = h.group(1)
    assert hashlib.sha256(mod.encode("utf-8")).hexdigest() == old, "inlined copy != its own stamp"
    assert mod.count(FX_OLD) == 1 and s.count(FX_OLD) == 1
    mod2 = mod.replace(FX_OLD, "", 1)
    new = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    o = s.replace(FX_OLD, "", 1).replace(old, new).replace(old[:16], new[:16])
    h2 = HEAD.search(o)
    t2 = TAIL.search(o, h2.end())
    assert o[h2.end():t2.start()].rstrip("\n") + "\n" == mod2
    return o, old, new


def build(out: pathlib.Path, fxout=False, src=None, R=None):
    s = src_text(src)
    R = R if R is not None else rows(src)
    o = apply_all(s, R)
    info = {}
    if fxout:
        o, old, new = fx_out(o)
        info = {"fx_old": old[:16], "fx_new": new[:16]}
    for bad in ("rng()", "spawnFx", "Math.random", "ultFx"):
        for r in R:
            assert bad not in strip_comments(r["code"]), (r["label"], bad)
    mr0, mr1 = strip_comments(s).count("Math.random"), strip_comments(o).count("Math.random")
    assert mr1 == mr0 - 1, (mr0, mr1)        # the bolt branch's flicker, retired; none added
    n = syntax_check(o)
    out.write_bytes(o.encode("utf-8"))
    info.update(blocks=n, delta=len(o) - len(s), stamp=stamp_of(o), math_random=(mr0, mr1))
    return info


def stamp_of(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    print("sb-final.html   ", build(HERE / "sb-final.html"))
    print("sb-final-fx.html", build(HERE / "sb-final-fx.html", fxout=True))
