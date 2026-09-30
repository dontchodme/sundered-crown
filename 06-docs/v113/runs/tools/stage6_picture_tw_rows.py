"""BRAMBLESNARE'S PICTURE (v84 section 4, "Picture") as exactly-once edits to Thornwake's final link
(thornwake/links/sc-thornwake-b26.5.html, fd5031063ecb6807 = sc-tendril-t3 + thornwake stages 1, 2, 3, 5).

rows() -> the deliverable rows (numbers inlined from PICK). There is NO lab variant of the rows: every
component is its own renderer method, so the harnesses hide one by shadowing that method on the renderer
instance from outside the page, and the bytes measured are the bytes delivered.

build(out)            -> tw-final.html     the base + these rows: THE STAMP
build(out, fxout=1)   -> tw-final-fx.html  the same, with SPECS.thornwake (the freeze's frost, with its FREEZE
                        comment) taken out of the INLINED fx.js copy and both stamps re-cut: the page
                        tools/fx_remove.py computes (fx_out; fx_remove itself REFUSES on this page, fx_diag.out;
                        src/render/fx.js is never read or written) -- what the orchestrator does to both copies at
                        the carry. That is the look as it ships, so the gates are measured on it.

READINGS (the design leaves these to the build; each declared, none a mechanic; Rick overrules):
  R1 A BRAMBLE is the sim's bramble: centre (b.x, b.y), radius read live off its caster (`w.ult.patchR`, 80),
     "a tangle of dark-green thorn strokes on the floor (verdant `dark` with `core` highlights, r 80,
     source-over, alpha 0.5)": seven thorned canes arching through it, each starting within half its radius of
     the hit point and bending one way or the other to its edge, each with a short offshoot -- canes that
     cross, a tangle and not a wheel -- each a `dark` stroke with a `core` seam, `core` thorns along it --
     inside the bramble's own r 80, so a ball is IN one (the sim's test: its centre within patchR + R) when its shell reaches the tangle. (A faint
     `dark` ground shade under it was tried and dropped: |dL| 0.026 on the hall's dark floor, m1.) The
     canes are placed by shellHash on the bramble's own planting step and position (no rng), and cached on
     the picture's record when the bramble first exists. WORLD pass, under both balls, source-over: floor,
     and nothing of it reaches the bloom (CLAUDE.md 4.1c); no ball's disc can be painted over (4.1b).
  R2 THE GROWTH (design: "growing out from the hit point over 0.3s") runs on the PRESENTATION clock, from
     the frame the bramble exists: the blow that plants it sets a hit stop, the brambles' clock
     (`brambleT`) stops in it, and a picture on the sim clock would sit at nothing through exactly the
     frames the viewer is watching (v54's lesson; Consecration's disc did the same). The tangle is revealed
     outward from the hit point (a clip circle growing to the bramble's radius). THE BROWNING ("in its last second") runs on the bramble's SIM age
     (`m.brambleT - b.t0` against `patchLife`, 6), the life the sim gives it: the colours turn from green to
     dead brown over its last second, and it fades over its last 0.25s so it does not pop; it reaches 0 on
     the step the sim removes it. A bramble outlives the window by up to 6s and works for its whole life
     (the sim tests brambles while any lives), so it is drawn for its whole life at one strength.
  R3 THE SNARE (design: "four thorn shoots up the foe's rim for the pin's length (the Tendril root
     picture, reused)"): Tendril's root picture (bindweed stage 6, `_twineRoot`) is NOT on this base, so
     its drawing is carried here under this picture's own names, the same picture: four shoots, `dark`
     strands with a `core` seam, grow 0.12s, clench round the rim in 0.1s more, dry through the pin's last
     30%, and wilt 0.2s after it lets go. ONE CHANGE, declared: Tendril's stalks rise from the hall's
     floor (its root comes out of the ground); these rise out of the bramble the ball is caught in, from
     1.55 R under its centre -- a stalk from the hall's floor would say the floor caught it. The held ball
     is `foe.pin > 0 && !foe.pinFree` from the frame `brambleTally.snares` rises until the pin runs out
     (`brierHeld`, on the held ball, presentation only), and `_drawField`'s hexagon is kept off that ball by
     a return inserted BEFORE its guard line (its last block): no existing line is edited, so the row
     composes with Tendril's guard on the chain (`&& !(f.twineHeld > 0)`) and with any other row anchored
     on that line. `pinFree` is not touched; the weapon stays locked.
  R4 THE BITE: the thorns' bite (`brambleTally.ticks` rising) flashes four thorns out of the foe's rim on
     the side of the bramble it stands in (the nearest of the caster's brambles; underneath when it stands
     on the centre) for 0.12s -- Tendril's bite flash, reused with the snare. "The entangle tag counts":
     Tendril's rule -- a bite whose count is not the one last printed tags ENTANGLE and the count on the
     foe, one tag up at a time (0.9s), none while the count sits at its cap; and ONE ENTANGLE TAG ON THE
     FOE AT A TIME: the scythe's own blow tags ENTANGLE too (`resolveHit`), so a tag already up there
     takes the count instead of a second printing over it. Found by watching the tally rise: the sim
     makes no call for the picture.
  R5 THE CAST (design: "the scythe's blade greens for the window"): the crescent (`SHAPES._scCrescent`,
     the verdant scythe's own blade) is filled green over its pale steel -- `core` at the edge to `dark` at
     the heel -- with its cutting edge and inner thorns relit in `core`, drawn in `drawWeapon`'s own blade
     frame (so it rides the blade and is clipped by the foe's shell exactly as the blade is), in the world
     pass. It greens over 0.25s at the cast, holds while the window is open, and fades over 0.3s at the
     close, a death or the verdict (`tickBramble` never runs once `over` is set). Dimmed with a stunned
     weapon. The resting silhouette (`SHAPES._scGrown`) is unchanged.
  R6 THE FIELD (design: "leaf motes off each bramble, both copies"): DRAWN, not an fx.js field (tw_fxprobe:
     the one ultFx slot fires once, at the cast, where Thornwake stood, and no bramble exists then; every
     bramble is planted later, at a blow, at the struck ball, and lives up to 6s past the window). Four
     leaves a bramble lift off it, turn and fade, placed by shellHash on the bramble's planting step and
     the match clock (and the death clock after the kill): no rng, and they keep moving through a hit stop.
  R7 AFTER THE KILL the brambles fade out over 0.3s (they are frozen with the sim, and the verdict is not
     the place for a stale floor), as every window picture in the batch closes at the verdict.
  R8 THE FREEZE'S PICTURE IS RETIRED: drawUltUnder's thornwake branch (the floor roots from caster to
     quarry) and drawUltOver's (the thorns on the pinned quarry), the ultFx life entry (`thornwake: 2.4`: the
     cast's record falls to the map's own 1.5 and nothing draws from it), and fireUlt's `onTarget` entry
     (`thornwake:1`): the cast is now the caster's (its blade greens), so the banner stands on the caster.
     KEPT: the banner's arrival (the letters cinch in between two thorn vines -- the name is kept and
     still snares) and the charge rune ULTSIG.thornwake ("a thorn ring that closes as the charge fills":
     it reads as the snare, which the ultimate still is). SPECS.thornwake goes out of both fx.js copies at
     the carry (the orchestrator's `fx_remove.py --relic thornwake`; `build(fxout=True)` does it to the
     inlined copy here, in scratch, to measure the shipped look). The cast voice is the voice lab's.
  R9 THE SILHOUETTE: SHAPES._scGrown is the shipped verdant scythe; measured among the seven scythes
     (scythe_sil.py) and left alone if it reads.
  NAMES: `brier*` (`tickBrier`, `drawBrier`, `drawBrierTop`, `_brier*`, the fighter's `brier*` fields) --
     free on the base, the chain tip and the staff line; not `bramble*` (the simulation's), `vine*` (the
     Thicket's), `twine*` / `bindweed-*` (Tendril's), `cons*` / `holy*` (Consecration's), `briar*`
     (Briarwand's, on the staff line).
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "links" / "sc-thornwake-b26.5.html").resolve()
TOOLS = pathlib.Path(r"C:\dev\sundered-crown\tools")
PY = r"C:\Users\Ye\AppData\Local\Programs\Python\Python313\python.exe"

PICK = dict(
    OPEN=0.6,      # a bramble's growth out of the hit point, half-seconds (v84: 0.3s)
    BROWN=1.0,     # its browning over the last of its life, SIM seconds (v84: its last second)
    GONE=0.25,     # its fade at the very end, SIM seconds (R2: so it does not pop)
    END=0.6,       # the brambles' fade after the kill, half-seconds (0.3s; R7)
    IGNITE=0.5,    # the blade greening at the cast, half-seconds (0.25s; R5)
    CLOSE=0.6,     # the blade's green going at the close, half-seconds (0.3s; R5)
    ALPHA=0.5,     # the tangle (v84: alpha 0.5)
    CANES=7,       # long canes arching through a bramble, each with an offshoot (R1)
    CANEW=4.2,     # a cane's dark stroke, units
    SEAMW=1.4,     # its core seam, units
    THORN=6.5,     # a thorn's length, units
    MOTEN=4,       # leaves a bramble (R6)
    MOTEUP=30,     # how far a leaf lifts over its life, units
    GREEN=0.85,    # the blade's green, over its steel (R5)
    RGROW=0.24,    # the snare's shoots reach the rim in 0.12s (Tendril's)
    RCLENCH=0.2,   # ... and close round it in 0.1s more (Tendril's)
    WILT=0.4,      # ... and wilt away 0.2s after the hold lets go (Tendril's)
    ROOTD=1.55,    # where the shoots rise from: this many R under the held ball's centre (R3)
    FLASH=0.24,    # a bite's thorn flash, half-seconds (0.12s; Tendril's)
    FLASHL=20,     # ... its longest thorn, units (Tendril's)
    TAGT=1.8,      # one bramble tag up at a time: a tag's own 0.9s, half-seconds (Tendril's)
)
BROWND = "#2A2012"     # a dead cane (Tendril's wilt colours)
BROWNS = "#6E5B2E"     # a dead seam
SHOOT = "#2E8A45"      # the blade's green between core and dark


def src_text(src=None) -> str:
    p = pathlib.Path(src) if src else SRC
    return p.read_bytes().decode("utf-8")


# ---------------------------------------------------------------------------
# 1. the fighter's picture state
FIGHTER_ANCHOR = "    this.ultBramble = null;\n    this.brambleCd = 0;\n    this.brambleIn = false;\n    this.brambleTally = null;\n"
FIGHTER_CODE = """    /* BRAMBLESNARE'S PICTURE (v84 section 4), and none of it is the window:
       the blade's green fades 0.3s past `ultBramble`, a bramble outlives the
       window and grows on a clock that runs through the hit stop of the blow
       that planted it, and the snare's shoots outlive the pin, so the picture
       keeps its own state. On the FIGHTER and never on `m.ultFx` (one slot,
       and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation` (`tickBrier`); nothing in the simulation reads any
       of it. `brier`, not `bramble` (the simulation's own names).
         brierGreen -- the blade's green: 1 while the window is open; eased
                       to 0 over the close
         brierAge   -- the presentation clock since the cast (the greening)
         brierOut   -- the presentation clock since the close
         brierEnd   -- the presentation clock since the verdict (they go)
         brierPic   -- this caster's brambles as the picture knows them:
                       {b, age, g}, `b` the simulation's own bramble (read,
                       never written), `age` the presentation clock since it
                       was planted, `g` its canes (placed once, by shellHash)
         brierSeen  -- `brambleTally`'s snares and ticks as last seen
         brierTagN, brierTagT -- the count the bramble's ENTANGLE tag last
                       printed, and how long that tag is still up
         brierBite  -- the bite flashes on the foe's rim {a, t}
       and ON THE HELD BALL, the snare's quarry:
         brierHeld  -- 1 exactly while a Bramblesnare snare's pin holds this
                       ball. Its one reader outside this picture is
                       `_drawField`, which leaves Paradox's hexagon off it
                       (the shoots are its picture); `pinFree` is not
                       touched, so the weapon stays locked
         brierRootFade, brierHeldAge, brierHeldOut -- the shoots' own fade,
                       the clock since the snare, and since the hold let go */
    this.brierGreen = 0;
    this.brierAge = 0;
    this.brierOut = 0;
    this.brierEnd = 0;
    this.brierPic = [];
    this.brierSeen = [0, 0];
    this.brierTagN = 0;
    this.brierTagT = 0;
    this.brierBite = [];
    this.brierHeld = 0;
    this.brierRootFade = 0;
    this.brierHeldAge = 0;
    this.brierHeldOut = 0;
"""

# ---------------------------------------------------------------------------
# 2. the presentation call
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickBrier(dt);                 // BRAMBLESNARE'S PICTURE (v84 section 4)\n"

# ---------------------------------------------------------------------------
# 3. tickBrier, after the simulation's own bramble methods
TICK_ANCHOR = "  tickWinnow(dt){\n"
TICK_CODE = """  /* ------------------------------------------- BRAMBLESNARE'S PICTURE ---
     v84 section 4, on the presentation clock. HALF-SECONDS, like every `life`
     in `tickPresentation` (it runs twice a normal step): %IGNITE% is the blade's
     0.25s greening at the cast, %CLOSE% its 0.3s fade at the close, %OPEN% a
     bramble's 0.3s growth, %END% the brambles' 0.3s fade after the kill, %RGROW% + %RCLENCH%
     the snare's shoots growing and clenching (0.12s + 0.1s), %WILT% their wilt
     after the hold (0.2s), %FLASH% a bite's thorn flash (0.12s). The window is
     `ultBramble`, and not once the caster falls or the match ends:
     `tickBramble` never runs again once `over` is set, so a window open at
     the kill would otherwise stay green through the verdict. THE BRAMBLES are
     the simulation's own (`m.brambles`, read, never written): each gets a
     picture record the frame it exists -- its canes placed once, by
     shellHash on its own planting step and position -- and loses it the
     frame the simulation removes it. THE SNARE, THE BITES AND THE TAG are
     found by watching `brambleTally.snares` and `.ticks` rise, so
     `tickBramble` makes no call for the picture. THE TAG RULE (Tendril's): a
     bite whose count is not the one last printed tags ENTANGLE and the count
     on the foe, one tag up at a time, none while the count sits at its cap;
     and one ENTANGLE tag on the foe at a time -- a tag already up there (the
     scythe's own blow tags it) takes the count instead. Writes presentation
     fields, `tags` and `taught` only, and draws no rng. */
  tickBrier(dt){
    const G = this.brambles, R = CONFIG.physics.ballR;
    for (const f of [this.a, this.b]){
      /* THE HELD BALL (this fighter as a snare's quarry): `brierHeld` is 1
         exactly while the snare's pin holds -- frozen with it through the
         verdict -- and `brierRootFade` is the shoots' own tail. */
      if (f.brierHeld && !(f.pin > 0 && f.alive)) f.brierHeld = 0;
      if (f.brierRootFade > 0){
        if (!f.alive) f.brierRootFade = 0;
        else if (f.brierHeld && !this.over) f.brierHeldAge += dt;
        else {
          f.brierHeldOut += dt;
          f.brierRootFade = Math.max(0, 1 - f.brierHeldOut / %WILT%);
        }
      }
      const T = f.brambleTally;
      if (!T && !(f.brierGreen > 0) && !f.brierPic.length) continue;   // <- zero burden
      const foe = f === this.a ? this.b : this.a, side = f === this.a ? "a" : "b";
      const Z = (this.over || !f.alive) ? null : f.ultBramble;
      if (Z){
        if (!(f.brierGreen > 0) || f.brierOut > 0){ f.brierAge = 0; f.brierOut = 0; }   // a cast
        f.brierGreen = 1;
        f.brierAge += dt;
      } else if (f.brierGreen > 0){
        f.brierOut += dt;
        f.brierGreen = Math.max(0, 1 - f.brierOut / %CLOSE%);
      }
      const P = f.brierPic;
      for (let i = P.length - 1; i >= 0; i--) if (G.indexOf(P[i].b) < 0) P.splice(i, 1);
      for (const b of G)
        if (b.side === side && !P.some(p => p.b === b)) P.push({ b, age: 0, g: this._brierCanes(f, b) });
      for (const p of P) p.age += dt;
      if (this.over) f.brierEnd += dt;
      for (let i = f.brierBite.length - 1; i >= 0; i--){
        f.brierBite[i].t += dt;
        if (f.brierBite[i].t >= %FLASH%) f.brierBite.splice(i, 1);
      }
      if (f.brierTagT > 0) f.brierTagT -= dt;
      if (!T) continue;
      const S = f.brierSeen, dS = T.snares - S[0], dK = T.ticks - S[1];
      S[0] = T.snares; S[1] = T.ticks;
      /* THE SNARE: the thorns' test pinned the foe this step, and the
         tally's count is how this knows. */
      if (dS > 0 && foe.alive && foe.pin > 0 && !foe.pinFree){
        if (!foe.brierHeld) foe.brierHeldAge = 0;
        foe.brierHeld = 1; foe.brierRootFade = 1; foe.brierHeldOut = 0;
      }
      if (!(dK > 0) || !foe.alive) continue;
      /* THE BITE: four thorns flash out of the foe's rim on the side of the
         bramble it stands in (underneath when it stands on the centre) */
      let q = null, qd = 1e9;
      for (const b of G){
        if (b.side !== side) continue;
        const d = Math.hypot(b.x - foe.x, b.y - foe.y);
        if (d < qd){ qd = d; q = b; }
      }
      f.brierBite.push({ a: q && qd > 4 ? Math.atan2(q.y - foe.y, q.x - foe.x) : Math.PI / 2, t: 0 });
      if (!(foe.hp > 0)) continue;
      const n = foe.stacks("entangle");
      const g = this.tags.find(g2 => g2.key === "entangle" && g2.life > 0.3
                                     && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
      if (g){ if (!g.first) g.val = n; }
      else if (n !== f.brierTagN && !(f.brierTagT > 0)){
        f.brierTagN = n; f.brierTagT = %TAGT%;
        const first = !this.taught.entangle && !!STATUS.entangle.tip;
        if (first) this.taught.entangle = true;
        this.statusTag(foe.x, foe.y, "entangle", first, n);
      }
    }
  }
  /* ONE BRAMBLE'S CANES, placed once when it first exists: %CANES% long canes
     arching through it -- each starts within half its radius of the hit
     point, sets off outward and bends, one way or the other, until it
     reaches the edge -- and a short offshoot off each, with thorns along
     them all: canes that cross each other, a tangle and not a wheel. By
     shellHash on the bramble's own planting step and position, so a
     bramble is the same tangle for its whole life and no rng is drawn.
     Points are relative to its centre. */
  _brierCanes(f, b){
    const Rp = f.w.ult.patchR, sd = 7300 + ((Math.round(b.t0 * 120) * 13
               + Math.round(b.x) * 7 + Math.round(b.y) * 3) % 4093 + 4093) % 4093;
    const H = (i, j) => shellHash(sd + j, i);
    const canes = [], thorns = [], lim = Rp * 0.97;
    const grow = (x, y, h, turn, n, st, id) => {
      const pts = [[x, y]];
      for (let j = 0; j < n; j++){
        h += turn * (0.7 + 0.6 * H(id * 16 + j, 9));
        const nx = x + Math.cos(h) * st, ny = y + Math.sin(h) * st;
        if (Math.hypot(nx, ny) > lim) break;
        x = nx; y = ny; pts.push([x, y]);
        if (j % 2 === 1){
          const tx = Math.cos(h), ty = Math.sin(h), sg = (j >> 1) % 2 ? 1 : -1;
          thorns.push([x, y, tx, ty, sg]);
        }
      }
      if (pts.length > 1) canes.push(pts);
      return pts;
    };
    for (let i = 0; i < %CANES%; i++){
      const a = TAU * (i + H(i, 0)) / %CANES%, r0 = Rp * 0.5 * Math.sqrt(H(i, 1));
      const x0 = Math.cos(a) * r0, y0 = Math.sin(a) * r0;
      const h0 = a + (H(i, 2) - 0.5) * 2.2, turn = (H(i, 3) < 0.5 ? -1 : 1) * (0.07 + 0.1 * H(i, 4));
      const pts = grow(x0, y0, h0, turn, 16, Rp * 0.085, i);
      if (pts.length > 5){
        const q = pts[2 + Math.floor(H(i, 5) * (pts.length - 4))];
        grow(q[0], q[1], h0 + (H(i, 6) < 0.5 ? -1.1 : 1.1), -turn * 1.3, 6, Rp * 0.07, i + 40);
      }
    }
    return { canes, thorns, sd };
  }

"""

# ---------------------------------------------------------------------------
# 4. the floor call (world, under both balls)
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* BRAMBLESNARE'S BRAMBLES (v84 section 4): the thorn tangles on the floor,
       the leaves lifting off them, and the snare's stalks rising out of the
       bramble under a held ball. FLOOR: the WORLD pass, under both balls,
       source-over -- nothing of it reaches the bloom (CLAUDE.md 4.1c) and no
       ball's disc can be painted over (4.1b). */
    if (__world) this.drawBrier(m);
"""

# ---------------------------------------------------------------------------
# 5. over both fighters (world)
TOP_ANCHOR = "    this.drawTreeTop(m);\n"
TOP_CODE = """    /* BRAMBLESNARE OVER BOTH FIGHTERS: the snare's shoots clenched round the
       held ball's rim and a bite's thorn flash on the foe's rim. World pass,
       source-over (Tendril's picture), so no shell is lit away. */
    this.drawBrierTop(m);
"""

# ---------------------------------------------------------------------------
# 6. the blade greening, in drawWeapon's own blade frame
BLADE_ANCHOR = "      if (f.ultDraw){\n"
BLADE_CODE = """      /* BRAMBLESNARE (v84 section 4): "the scythe's blade greens for the
         window" -- drawn here, in the blade's own frame, so it rides the
         blade and the foe's shell clips it as it clips the blade.
         `brierGreen` is 0 on every other relic. */
      if (f.brierGreen > 0 && f.w.shape === "scythe") this._brierBlade(c, f, reach + 6, dim * wk);
"""

# ---------------------------------------------------------------------------
# 7. the hexagon kept off a ball the snare holds
FIELD_ANCHOR = "    if (f.pin > 0 && !f.pinFree"
FIELD_CODE = """    /* AND NOT ON A BALL BRAMBLESNARE'S SNARE HOLDS (v84 section 4: its
       picture is "four thorn shoots up the foe's rim for the pin's length",
       `_brierRoot`). `brierHeld` is presentation state, 1 exactly while the
       snare's pin holds; `pinFree` stays 0, so the weapon is locked. The
       hexagon is this method's last block, so this returns past it alone. */
    if (f.brierHeld > 0 && f.pin > 0 && !f.pinFree) return;
"""

# ---------------------------------------------------------------------------
# 8. the drawing methods
DRAW_ANCHOR = "  drawMotes(m){\n"
DRAW_CODE = """  /* ------------------------------------------- BRAMBLESNARE'S PICTURE ---
     v84 section 4, drawn off the fighter's `brier*` fields and the
     simulation's own brambles (`m.brambles`, read) -- never `m.ultFx`, one
     slot the opponent's cast takes (open item 25). A BRAMBLE IS FLOOR: a
     tangle of thorned canes in the school's `dark` with `core` seams and
     thorns, at %ALPHA% (the design's), inside the sim's own radius (`patchR`, read off
     the caster, so the edge is where the test is).
     It grows out of the hit point over 0.3s (the presentation clock) and
     browns over the last second of its life (the sim's), and it is drawn
     for its whole life: it works for its whole life. WORLD pass, under both
     balls, source-over: nothing under `lighter` and nothing the bloom can
     see. One method a component, so each can be measured alone; nothing
     here keeps state or draws from the rng.
       drawBrier      the floor pass: clipped to the live hall
       _brierGeom     one bramble this frame: centre, growth, browning, alpha
       _brierTangle   its canes, seams and thorns
       _brierMotes    leaves lifting off every bramble (the design's field, drawn)
       _brierRoot     the snare: stalks out of the bramble (part 0, under the
                      ball) and the shoots clenched round its rim (part 1, over)
       drawBrierTop   over both fighters: the clench and a bite's thorn flash
       _brierBite     a bite: four thorns out of the foe's rim
       _brierBlade    the blade greening (from `drawWeapon`, in its frame) */
  drawBrier(m){
    const a = m.a, b = m.b;
    if (!a.brierPic.length && !b.brierPic.length
        && !(a.brierRootFade > 0) && !(b.brierRootFade > 0)) return;       // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.brierPic.length){
        const end = m.over ? Math.max(0, 1 - f.brierEnd / %END%) : 1;
        if (end > 0.004){
          for (const p of f.brierPic){
            const g = this._brierGeom(m, f, p, end);
            if (!g) continue;
            this._brierTangle(c, g);
          }
          this._brierMotes(c, m, f, end);
        }
      }
      if (f.brierRootFade > 0) this._brierRoot(m, f, 0);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* the growth on the presentation clock (it plays through the planting
     blow's hit stop); the browning and the fade on the bramble's sim age, so
     it reaches 0 on the step the simulation removes it */
  _brierGeom(m, f, p, end){
    const b = p.b, u = f.w.ult, P = AFFINITIES.verdant;
    const s = Math.min(1, p.age / %OPEN%), k = 1 - (1 - s) * (1 - s);
    const left = u.patchLife - (m.brambleT - b.t0);
    const br = clamp(1 - left / %BROWN%, 0, 1), fl = clamp(left / %GONE%, 0, 1);
    const A = end * fl * Math.min(1, s * 4);
    if (!(A > 0.004)) return null;
    return { x: b.x, y: b.y, R: u.patchR, k, A, g: p.g,
             dk: br > 0 ? mix(P.dark, "%BROWND%", br) : P.dark,
             sm: br > 0 ? mix(P.core, "%BROWNS%", br) : P.core };
  }
  /* THE TANGLE: all of it, clipped to how far out of the hit point it has
     grown (no clip once grown): one path for the dark strokes, one for the
     seams, one for the thorns */
  _brierTangle(c, g){
    const x0 = g.x, y0 = g.y;
    const clip = g.k < 0.999;
    if (clip){ c.save(); c.beginPath(); c.arc(x0, y0, Math.max(0.5, g.R * g.k), 0, TAU); c.clip(); }
    c.globalAlpha = g.A * %ALPHA%;
    c.beginPath();
    for (const pts of g.g.canes){
      c.moveTo(x0 + pts[0][0], y0 + pts[0][1]);
      for (let j = 1; j < pts.length; j++) c.lineTo(x0 + pts[j][0], y0 + pts[j][1]);
    }
    c.strokeStyle = g.dk; c.lineWidth = %CANEW%; c.stroke();
    c.strokeStyle = g.sm; c.lineWidth = %SEAMW%; c.stroke();
    c.fillStyle = g.sm;
    c.beginPath();
    for (const [px, py, tx, ty, sg] of g.g.thorns){
      const nx = -ty * sg, ny = tx * sg, x = x0 + px, y = y0 + py;
      c.moveTo(x + nx * 1.6 - tx * 2.2, y + ny * 1.6 - ty * 2.2);
      c.lineTo(x + nx * %THORN% + tx * 1.4, y + ny * %THORN% + ty * 1.4);
      c.lineTo(x + nx * 1.6 + tx * 2.4, y + ny * 1.6 + ty * 2.4);
      c.closePath();
    }
    c.fill();
    if (clip) c.restore();
  }
  /* LEAVES LIFTING OFF EVERY BRAMBLE (the design's field, drawn: a SPECS
     field fires once, at the cast, where Thornwake stood, and no bramble
     exists then). %MOTEN% a bramble, born inside it, lifting %MOTEUP% units, turning
     and fading; placed by shellHash on the bramble's own seed and the match
     clock (the death clock after the kill), so they keep moving through a
     hit stop. */
  _brierMotes(c, m, f, end){
    const T = m.t + (m.deathAge || 0);
    for (const p of f.brierPic){
      const g = this._brierGeom(m, f, p, end);
      if (!g) continue;
      const sd = g.g.sd + 500;
      c.fillStyle = g.sm;
      for (let i = 0; i < %MOTEN%; i++){
        const ph = (T * (0.55 + 0.25 * shellHash(sd, i)) + shellHash(sd + 1, i)) % 1;
        const q = TAU * shellHash(sd + 2, i), rr = g.R * g.k * Math.sqrt(shellHash(sd + 3, i)) * 0.85;
        const x = g.x + Math.cos(q) * rr + Math.sin(T * 1.6 + i * 2.3) * 5;
        const y = g.y + Math.sin(q) * rr - ph * %MOTEUP%;
        const ang = T * (1.4 + shellHash(sd + 4, i)) + i * 1.7, ca = Math.cos(ang), sa = Math.sin(ang);
        c.globalAlpha = 0.8 * g.A * Math.sin(ph * Math.PI);
        c.beginPath();
        c.moveTo(x - ca * 4.2, y - sa * 4.2);
        c.quadraticCurveTo(x - sa * 2.2, y + ca * 2.2, x + ca * 4.2, y + sa * 4.2);
        c.quadraticCurveTo(x + sa * 2.2, y - ca * 2.2, x - ca * 4.2, y - sa * 4.2);
        c.fill();
      }
    }
  }
  /* THE SNARE (Tendril's root picture, reused): `part` 0 the stalks out of
     the bramble (under both balls), 1 the clench round the rim (over them).
     The shoots grow up in 0.12s, close round the rim in 0.1s more, hold for
     the pin, dry through its last 30%, and fade 0.2s after it lets go.
     `dark` strands, a `core` seam, `core` tips: the caster's school, verdant
     on whatever ball it holds. The stalks rise out of the bramble the ball
     is caught in, from %ROOTD% R under its centre -- not the hall's floor, which
     is Tendril's (its root comes out of the ground). */
  _brierRoot(m, f, part){
    const c = this.ctx, R = CONFIG.physics.ballR, P = AFFINITIES.verdant;
    const grow = Math.min(1, f.brierHeldAge / %RGROW%);
    const cl = clamp((f.brierHeldAge - %RGROW%) / %RCLENCH%, 0, 1), ce = 1 - (1 - cl) * (1 - cl);
    const left = f.brierHeld ? clamp(f.pin / Math.max(0.01, f.pinMax || 1), 0, 1) : 0;
    const wilt = clamp((0.3 - left) / 0.3, 0, 1);
    const dk = mix(P.dark, "%BROWND%", wilt), sm = mix(P.core, "%BROWNS%", wilt);
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    c.globalAlpha = f.brierRootFade;
    for (let i = 0; i < 4; i++){
      const sd = i < 2 ? -1 : 1, o = i % 2;
      const qa = sd < 0 ? Math.PI - (o ? 0.62 : 0.16) : (o ? 0.62 : 0.16);    // where it meets the rim
      const cx = f.x + Math.cos(qa) * (R + 1.5), cy = f.y + Math.sin(qa) * (R + 1.5);
      if (part === 0){
        /* up out of the bramble, then climbing onto the rim along it, so the
           clench carries on the way the stalk was already going */
        const fx = f.x + sd * R * (o ? 0.45 : 1.25), fy = f.y + R * %ROOTD%, h = fy - cy;
        const ta = qa - sd * Math.PI / 2, x1 = fx, y1 = fy - h * 0.45;
        const x2 = cx - Math.cos(ta) * R * 0.8, y2 = cy - Math.sin(ta) * R * 0.8;
        const pts = [];
        for (let j = 0; j <= 16; j++){
          const t = grow * j / 16, u = 1 - t;
          pts.push([u * u * u * fx + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t * t * t * cx,
                    u * u * u * fy + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t * t * t * cy]);
        }
        for (const [col, w] of [[dk, 5.4], [sm, 2.0]]){
          c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
          for (let j = 1; j < pts.length; j++) c.lineTo(pts[j][0], pts[j][1]);
          c.stroke();
        }
        c.fillStyle = sm;                              // thorns up the stalk
        c.beginPath();
        for (let j = 3; j < pts.length - 1; j += 3){
          const p = pts[j], q = pts[j + 1], dx = q[0] - p[0], dy = q[1] - p[1], dl = Math.hypot(dx, dy) || 1;
          const s2 = (j / 3) % 2 ? 1 : -1, nx = -dy / dl * s2, ny = dx / dl * s2;
          c.moveTo(p[0] + nx * 2.2, p[1] + ny * 2.2);
          c.lineTo(p[0] + nx * 7 + dx / dl * 2, p[1] + ny * 7 + dy / dl * 2);
          c.lineTo(p[0] + nx * 2.2 + dx / dl * 3.4, p[1] + ny * 2.2 + dy / dl * 3.4);
          c.closePath();
        }
        c.fill();
      } else if (grow >= 1 && ce > 0){
        const span = (1.05 - 0.55 * wilt) * ce, a1 = qa - sd * span;
        for (const [col, w] of [[dk, 5.4], [sm, 2.0]]){
          c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.arc(f.x, f.y, R + 1.5, qa, a1, sd > 0); c.stroke();
        }
        const tx = f.x + Math.cos(a1) * (R + 1.5), ty = f.y + Math.sin(a1) * (R + 1.5);
        const da = a1 - sd * Math.PI / 2, nx = -Math.sin(da), ny = Math.cos(da);
        c.fillStyle = wilt > 0.5 ? sm : P.core;
        c.beginPath();
        c.moveTo(tx + nx * 3, ty + ny * 3);
        c.lineTo(tx + Math.cos(da) * 8, ty + Math.sin(da) * 8);
        c.lineTo(tx - nx * 3, ty - ny * 3);
        c.closePath(); c.fill();
      }
    }
    c.restore();
  }
  drawBrierTop(m){
    const a = m.a, b = m.b;
    if (!(a.brierRootFade > 0) && !(b.brierRootFade > 0)
        && !a.brierBite.length && !b.brierBite.length) return;           // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const foe = f === a ? b : a;
      if (f.brierBite.length && foe.alive) this._brierBite(c, f, foe);
      if (f.brierRootFade > 0) this._brierRoot(m, f, 1);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* A BITE: four thorns flash out of the foe's rim on the side of the bramble
     it stands in, glow over a dark edge, 0.12s. No freeze (Tendril's flash). */
  _brierBite(c, f, foe){
    const R = CONFIG.physics.ballR, P = AFFINITIES.verdant;
    for (const F of f.brierBite){
      const k = F.t / %FLASH%, bx = foe.x + Math.cos(F.a) * (R - 2), by = foe.y + Math.sin(F.a) * (R - 2);
      c.globalAlpha = 1 - k * k;
      c.beginPath();
      for (const o of [-0.7, -0.3, 0.3, 0.7]){
        const q = F.a + o, L = %FLASHL% * (Math.abs(o) > 0.5 ? 0.7 : 1) * (1 + 0.3 * (1 - k));
        const cq = Math.cos(q), sq = Math.sin(q);
        c.moveTo(bx - sq * 3.4, by + cq * 3.4);
        c.lineTo(bx + cq * L, by + sq * L);
        c.lineTo(bx + sq * 3.4, by - cq * 3.4);
        c.closePath();
      }
      c.fillStyle = P.glow; c.fill();
      c.strokeStyle = P.dark; c.lineWidth = 1.6; c.stroke();
      c.beginPath(); c.arc(bx, by, 4.2 * (1 - 0.5 * k), 0, TAU); c.fill(); c.stroke();
    }
  }
  /* THE BLADE GREENS (v84: "the scythe's blade greens for the window"): the
     verdant scythe's crescent (`SHAPES._scCrescent`, the blade `_scGrown`
     fills pale) filled green over its steel -- `core` at the edge to `dark`
     at the heel -- and its edge and inner thorns relit in `core`. In
     `drawWeapon`'s blade frame (L the drawn reach, W the art width). Greens
     over 0.25s, fades over 0.3s; `al` carries the stunned weapon's dimming. */
  _brierBlade(c, f, L, al){
    const s = Math.min(1, f.brierAge / %IGNITE%), k = Math.min(1 - (1 - s) * (1 - s), f.brierGreen);
    if (!(k > 0.004)) return;
    const W = f.w.artW, P = AFFINITIES.verdant;
    c.save();
    SHAPES._scCrescent(c, L, W);
    const g = c.createLinearGradient(L * 0.55, -W, L * 0.95, W * 0.2);
    g.addColorStop(0, P.core); g.addColorStop(0.55, "%SHOOT%"); g.addColorStop(1, P.dark);
    c.globalAlpha = al * k * %GREEN%;
    c.fillStyle = g; c.fill();
    c.fillStyle = P.core;
    for (let i = 1; i <= 6; i++){
      const q = SHAPES._scOuter(L, W, i / 7);
      c.beginPath();
      c.moveTo(q.x - q.nx * W * 0.04, q.y - q.ny * W * 0.04);
      c.lineTo(q.x - q.nx * W * 0.19 + Math.cos(q.a) * W * 0.11,
               q.y - q.ny * W * 0.19 + Math.sin(q.a) * W * 0.11);
      c.lineTo(q.x - q.nx * W * 0.05 + Math.cos(q.a) * W * 0.13,
               q.y - q.ny * W * 0.05 + Math.sin(q.a) * W * 0.13);
      c.closePath(); c.fill();
    }
    c.globalAlpha = al * k;
    c.strokeStyle = P.core; c.lineWidth = Math.max(1, W * 0.05);
    c.lineCap = "round";
    c.beginPath();
    c.moveTo(L * 0.70, W * 0.20);
    c.bezierCurveTo(L * 1.02, -W * 0.20, L * 0.98, -W * 0.95, L * 0.56, -W * 1.32);
    c.stroke();
    c.restore();
  }

"""


# ---------------------------------------------------------------------------
# 9-10. the freeze's floor roots and its thorns on the quarry, retired
def _branch(s, head):
    i = s.index(head)
    j = s.index('else if (u.w === "thornwake"){', i) + len('else if (u.w === "thornwake")')
    d = 0
    k = j
    while True:
        ch = s[k]
        if ch == "{": d += 1
        elif ch == "}":
            d -= 1
            if d == 0: break
        k += 1
    assert s[k + 1] == "\n", repr(s[k:k + 5])
    return s[i:k + 2]


def under_old(s):
    return _branch(s, '    else if (u.w === "thornwake"){\n      /* roots running along the floor from caster to quarry */')


def over_old(s):
    return _branch(s, '    /* ---- Bramblesnare: they are pinned, and you can see the thorns */\n    else if (u.w === "thornwake"){')


UNDER_CODE = """    /* ---- Bramblesnare's floor roots, caster to quarry, were the FREEZE's
       (v84 retired the 1.6s root; v113 stage 6). The brambles are
       `drawBrier`, off the fighter and the simulation's own brambles, where
       the one ultFx slot cannot erase them; the cast's record now carries the
       CAST only and nothing draws from it. */
"""
OVER_CODE = """    /* ---- Bramblesnare's thorns on the pinned quarry were the FREEZE's;
       retired with it (v84, v113 stage 6). The snare's shoots are
       `_brierRoot`, the cast is the blade greening (`_brierBlade`). */
"""

# ---------------------------------------------------------------------------
# 11. the cast record's life, and 12. the banner's anchor
LIFE_ANCHOR = "thornwake: 2.4, "
ONTARGET_ANCHOR = "thornwake:1, "


def rows(src=None):
    s = src_text(src)
    pk = dict(PICK, BROWND=BROWND, BROWNS=BROWNS, SHOOT=SHOOT)

    def fill(code):
        for k, v in pk.items():
            code = code.replace("%" + k + "%", str(v))
        left = re.findall(r"%[A-Z_0-9]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="brier picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the blade's green fades 0.3s past ultBramble; each bramble's growth clock runs through the planting blow's hit stop; the snare's shoots on the held ball; the tag's count); never m.ultFx (open item 25). Read by nothing in the sim."),
        dict(label="brier picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickBrier."),
        dict(label="brier picture: tickBrier and the canes", anchor=TICK_ANCHOR, mode="before", code=TICK_CODE,
             why="Drives the blade's green (0.25s up at the cast; 0.3s down at a clock close, a death or the verdict), keeps a picture record per bramble of m.brambles (read, never written; its growth clock and its canes, placed once by shellHash), the snare's shoots on the held ball (brambleTally.snares rising), the bite flashes and the ENTANGLE tag rule (brambleTally.ticks rising). Writes presentation fields, tags and taught only; no rng."),
        dict(label="brier picture: the floor call (world, under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls, source-over: the thorn tangles, the leaves lifting off them, the snare's stalks (bloom share 0; no ball's disc can be painted over)."),
        dict(label="brier picture: over both fighters (world)", anchor=TOP_ANCHOR, mode="after", code=TOP_CODE,
             why="The snare's shoots clenched round the held ball's rim and a bite's thorn flash, over both fighters in the world pass (Tendril's picture), beside Canopy's bark."),
        dict(label="brier picture: the blade greens (drawWeapon)", anchor=BLADE_ANCHOR, mode="before", code=BLADE_CODE,
             why="The design's cast: the scythe's blade greens for the window, drawn in drawWeapon's own blade frame after the shape, so it rides the blade and is clipped by the foe's shell as the blade is. brierGreen is 0 on every other relic."),
        dict(label="brier picture: the hexagon off a snared ball", anchor=FIELD_ANCHOR, mode="before", code=FIELD_CODE,
             why="The brief: _drawField's hexagon must not draw on the snare. A return inserted before the guard (the method's last block) for a ball whose pin is Bramblesnare's; no existing line edited, so it composes with Tendril's guard on the chain and any row anchored on that line."),
        dict(label="brier picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawBrier and one method a component (geometry, tangle, leaves, the snare's stalks/clench), drawBrierTop, the bite flash and the blade's green."),
        dict(label="brier picture: the freeze's floor roots retired", anchor=under_old(s), mode="replace", code=UNDER_CODE,
             why="drawUltUnder's thornwake branch drew the FREEZE's roots running along the floor from caster to quarry at every cast; the freeze is out (v113 stage 1), so its picture goes too."),
        dict(label="brier picture: the freeze's thorns on the quarry retired", anchor=over_old(s), mode="replace", code=OVER_CODE,
             why="drawUltOver's thornwake branch drew nine glowing thorn vines on the PINNED quarry for the record's 2.4s; nothing pins at the cast now, so it went on a free ball. Retired with the freeze."),
        dict(label="brier picture: the cast record's life", anchor=LIFE_ANCHOR, mode="replace", code="",
             why="The ultFx life entry 2.4 was the freeze's ('the art has to still be on screen while the hold it is explaining is in force'); with nothing drawn from the slot the cast's record falls to the map's own 1.5. The narrowest anchor, so the other entries on the line are left for their own builds."),
        dict(label="brier picture: the banner on the caster", anchor=ONTARGET_ANCHOR, mode="replace", code="",
             why="fireUlt's onTarget entry stood the cast banner on the quarry, where the freeze landed; the cast is now the caster's (its blade greens), so the banner stands there. Presentation only (this.banner); the narrowest anchor, so Emberedge's entry is left."),
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


FX_OLD = """    thornwake: { mode: 'fall', n: 1100, sp: [30, 120], grav: 110, drag: 1.0,
                 life: [0.80, 1.80], heavy: 0.02, size: [0.6, 1.9],
                 spawn: 0.85, up: 0 },
"""
FX_BLOCK = """    /* A FREEZE HOLDS, so its frost settles slowly and lasts -- the same
       reason the art is long: the hold it explains is still in force. */
""" + FX_OLD
HEAD = re.compile(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n")
TAIL = re.compile(r"/\* -+ THE ULT FIELDS -+")


def fx_out(s: str, work=None):
    """SPECS.thornwake (with its FREEZE comment) out of the INLINED copy, and both stamps re-cut: exactly the page
    tools/fx_remove.py computes (its `spec_block`, imported read-only, must name the same 331 bytes). NOT by running
    fx_remove.py itself: on this page it REFUSES (fx_diag.out) -- its difflib check aligns the 5-line removal one
    line early, because Vinesower's last line `spawn: 0.85, up: 0 },` is the same text as Thornwake's, and then
    compares a rotation of the block to the block. The page it would write is this one (checked below: only the
    block and the stamps move, as a multiset of lines). The disk fx.js follows the batch tip, so it is NOT read
    here. Scratch only."""
    sys.path.insert(0, str(TOOLS))
    import fx_remove as FXR
    h = HEAD.search(s)
    t = TAIL.search(s, h.end())
    NL = chr(10)
    mod = s[h.end():t.start()].rstrip(NL) + NL
    old = h.group(1)
    assert hashlib.sha256(mod.encode("utf-8")).hexdigest() == old, "inlined copy != its own stamp"
    blk = FXR.spec_block(mod, "thornwake")
    assert blk == FX_BLOCK, "fx_remove's spec_block is not the 331-byte block"
    assert mod.count(FX_BLOCK) == 1 and s.count(FX_BLOCK) == 1
    mod2 = mod.replace(FX_BLOCK, "", 1)
    new = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    o = s.replace(FX_BLOCK, "", 1).replace(old, new).replace(old[:16], new[:16])
    assert FXR.inlined(o)[1] == mod2.rstrip()
    import collections, difflib
    gone, came = [], []
    for op in difflib.unified_diff(s.split(NL), o.split(NL), n=0, lineterm=""):
        if op.startswith(("---", "+++", "@@")):
            continue
        (gone if op[0] == "-" else came).append(op[1:])
    st = [ln for ln in gone if old[:16] in ln]
    assert collections.Counter(ln for ln in gone if old[:16] not in ln) == collections.Counter(FX_BLOCK.rstrip(NL).split(NL))
    assert [ln.replace(old, new).replace(old[:16], new[:16]) for ln in st] == came
    assert o.count("thornwake: { mode:") == 0
    return o, old, new, ""


def build(out: pathlib.Path, fxout=False, src=None, R=None):
    s = src_text(src)
    R = R if R is not None else rows(src)
    o = apply_all(s, R)
    info = {}
    if fxout:
        o, old, new, _ = fx_out(o)
        info = {"fx_old": old[:16], "fx_new": new[:16]}
    for bad in ("rng()", "spawnFx", "Math.random", "ultFx"):
        for r in R:
            assert bad not in strip_comments(r["code"]), (r["label"], bad)
    assert strip_comments(o).count("Math.random") == strip_comments(s).count("Math.random")
    n = syntax_check(o)
    out.write_bytes(o.encode("utf-8"))
    info.update(blocks=n, delta=len(o) - len(s), stamp=stamp_of(o))
    return info


def stamp_of(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    print("tw-final.html   ", build(HERE / "tw-final.html"))
    print("tw-final-fx.html", build(HERE / "tw-final-fx.html", fxout=True))
