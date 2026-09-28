"""QUARRELSTORM'S PICTURE (v83 section 4) as exactly-once edits to Ironhail's final link
(ironhail/links/sc-ironhail-sunder.html, 1bedab05b9803465 = the base with stages 1-3).

rows() -> the deliverable rows (numbers inlined from PICK). There is NO lab variant of the rows: every
component is its own renderer method, so the harnesses hide one by replacing that method on the renderer
from outside the page, and the bytes measured are the bytes delivered.

build(out)            -> ih-final.html     (the base + these rows: THE STAMP)
build(out, fxout=1)   -> ih-final-fx.html  (the same + SPECS.ironhail out of the inlined fx.js copy with the
                                            stamp re-cut, which is what the orchestrator's sync_fx does to
                                            both copies; the look as it ships). SCRATCH ONLY.
"""
from __future__ import annotations
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "links" / "sc-ironhail-sunder.html").resolve()
FXJS = pathlib.Path(r"C:\dev\sundered-crown\src\render\fx.js")

PICK = dict(
    IGN=0.3,      # the limbs' ignition at the cast, half-seconds (0.15s)
    COOL=1.0,     # the limbs' cool after the close, half-seconds (0.5s)
    PUFF=0.8,     # a landing's splash + dust + sparks, half-seconds (0.4s)
    MISSP=0.6,    # a miss's splash + dust, half-seconds (0.3s)
    MOTE=2.0,     # the iron-spark motes' life, half-seconds (1.0s)
    END=0.5,      # a bolt the kill leaves in the air fades over this, half-seconds (0.25s)
    RUNE=14,      # the rune's radius (v83 section 4: r 14)
    SPARKN=6,     # sparks a landing (v83 section 4: 6)
    MOTEN=4,      # iron-spark motes a landing (the design's field, drawn)
    HOTB='"#8A2C0A"',   # the limbs' body in the window: a forge's dull red
    HOTF='"#F08A30"',   # the limbs' edge: forge-orange (Temper's, the same school's forge)
    HOTH='"#FFE2A8"',   # the limbs' heart, only while hot
    DUST='"#6E5434"',   # the dust
    MISSC='"#8A6A3A"',  # a miss's splash ring (the retired nova's floor-dust brown)
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
FIGHTER_ANCHOR = "    this.ultHail = null;\n    this.hailTally = null;\n"
FIGHTER_CODE = """    /* QUARRELSTORM'S PICTURE (v83 section 4), and none of it is the sim's:
       the limbs cool after `ultHail` is gone, and a landing's puff outlives
       its bolt (`tickHail` splices it), so the picture keeps its own state.
       On the FIGHTER and never on `m.ultFx` (one slot, and the opponent's
       cast takes it: open item 25). Driven in `tickPresentation`
       (`tickQuarrel`); nothing in the simulation reads any of it.
         quarrelFade -- 1 while the hail falls; eased to 0 over the cool
         quarrelAge  -- the presentation clock since the cast (the ignition)
         quarrelOut  -- the presentation clock since the close (the cool)
         quarrelEnd  -- the presentation clock since the match ended: a bolt
                        the kill leaves in the air fades on it
         quarrelSeen -- `hailTally`'s landed and missed, as last seen
         quarrelAir  -- this side's bolts in the air, as last seen: the
                        MATCH's own records, read and never written
         quarrelFx   -- a landing's or a miss's puff (records) */
    this.quarrelFade = 0;
    this.quarrelAge = 0;
    this.quarrelOut = 0;
    this.quarrelEnd = 0;
    this.quarrelSeen = [0, 0];
    this.quarrelAir = [];
    this.quarrelFx = [];
"""

# ---------------------------------------------------------------------------
# 2. the presentation call
PCALL_ANCHOR = "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n"
PCALL_CODE = "    this.tickQuarrel(dt);               // QUARRELSTORM'S PICTURE (v83 section 4)\n"

# ---------------------------------------------------------------------------
# 3. tickQuarrel, after tickHail
TICK_ANCHOR = "  tickWinnow(dt){\n"
TICK_CODE = """  /* --------------------------------------------- QUARRELSTORM'S PICTURE ---
     v83 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): %IGN% is the
     limbs' 0.15s ignition, %COOL% their 0.5s cool, %PUFF% a landing's 0.4s
     puff, %MISSP% a miss's 0.3s, %MOTE% the motes' 1s. A BOLT THAT RESOLVES IS
     FOUND BY WATCHING `hailTally` RISE, so `tickHail` makes no call for the
     picture: the bolt that left `m.hail` is the one this side had in the air
     last step, and whether it landed is the tally's word, not a guess (one
     bolt of a side is in the air at a time, dropCd > fallT on one clock;
     two at once are read off `tickHail`'s own test). THE LIMBS ARE READ OFF
     `ultHail && !over`: `tickHail` never runs again once `over` is set, so
     they cool at the verdict, and a bolt the kill leaves in the air fades
     rather than hanging through the panel. Writes presentation fields,
     `tags` and `taught` only, and draws no rng (shellHash). */
  tickQuarrel(dt){
    for (const f of [this.a, this.b]){
      const T = f.hailTally;
      if (!T && !(f.quarrelFade > 0)) continue;                // <- zero burden
      const side = f === this.a ? "a" : "b", foe = f === this.a ? this.b : this.a;
      const Rb = CONFIG.physics.ballR;
      for (let i = f.quarrelFx.length - 1; i >= 0; i--){
        const q = f.quarrelFx[i];
        q.t += dt;
        if (q.t >= q.life) f.quarrelFx.splice(i, 1);
      }
      const Z = (this.over || !f.alive) ? null : f.ultHail;
      if (Z){
        if (!(f.quarrelFade > 0) || f.quarrelOut > 0){ f.quarrelAge = 0; f.quarrelOut = 0; }   // a cast
        f.quarrelFade = 1;
        f.quarrelAge += dt;
      } else if (f.quarrelFade > 0){
        f.quarrelOut += dt;
        f.quarrelFade = Math.max(0, 1 - f.quarrelOut / %COOL%);
      }
      if (this.over) f.quarrelEnd += dt;
      if (!T) continue;
      const nl = T.landed - f.quarrelSeen[0], nm = T.missed - f.quarrelSeen[1];
      if (nl > 0 || nm > 0){
        const u = f.w.ult, gone = f.quarrelAir.filter(d => this.hail.indexOf(d) < 0);
        for (let j = 0; j < gone.length; j++){
          const d = gone[j];
          const hit = gone.length === 1 ? nl > 0
                    : foe.alive && Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + Rb;
          const n = f.quarrelSeen[0] + f.quarrelSeen[1] + j + 1;
          f.quarrelFx.push({ x: d.x, y: d.y, r: u.hitR, t: 0, hit, n, s: side === "a" ? 0 : 1,
                             puff: hit ? %PUFF% : %MISSP%, life: hit ? Math.max(%PUFF%, %MOTE%) : %MISSP% });
          /* THE SUNDER TAG ON THE FOE TICKS UP, with its count, on the foe's
             rim toward the spot. ONE SUNDER TAG ON THE FOE AT A TIME
             (Tendril's and Temper's rule): a tag already up there -- the
             bow's own, or the last bolt's -- takes the new count in place
             instead of a second printing over it. A killing landing tags
             nothing: the shatter owns that frame. */
          if (hit && foe.alive && foe.hp > 0){
            const k = foe.stacks("sunder"), a = Math.atan2(d.y - foe.y, d.x - foe.x);
            const g = this.tags.find(g2 => g2.key === "sunder" && !g2.first && g2.life > 0.3
                                           && Math.hypot(g2.x - foe.x, g2.y - foe.y) < Rb * 3);
            if (g) g.val = k;
            else {
              const first = !this.taught.sunder && !!STATUS.sunder.tip;
              if (first) this.taught.sunder = true;
              this.statusTag(foe.x + Math.cos(a) * Rb, foe.y + Math.sin(a) * Rb, "sunder", first, k);
            }
          }
        }
        if (f.quarrelFx.length > 12) f.quarrelFx.splice(0, f.quarrelFx.length - 12);
      }
      f.quarrelSeen[0] = T.landed; f.quarrelSeen[1] = T.missed;
      f.quarrelAir.length = 0;
      for (const d of this.hail) if (d.side === side) f.quarrelAir.push(d);
    }
  }

"""

# ---------------------------------------------------------------------------
# 4. the ground call (world, under both balls)
GROUND_ANCHOR = "    if (__world) this.drawTree(m);\n"
GROUND_CODE = """    /* QUARRELSTORM'S GROUND (v83 section 4): each bolt's rune on the spot it
       will land on, the ring closing on it as it falls, a landing's splash
       and dust. The WORLD pass and under both balls -- the rune is on the
       floor (the sigils' rule: a figure drawn over the ball standing in it
       says the opposite), and nothing of it reaches the bloom. */
    if (__world) this.drawQuarrel(m);
"""

# ---------------------------------------------------------------------------
# 5. the emissive call (over both fighters)
GLOW_ANCHOR = "    this.drawSunTop(m);\n"
GLOW_CODE = """    /* QUARRELSTORM'S BOLTS, SPARKS AND MOTES, OVER BOTH FIGHTERS: a bolt falls
       in front of everything in the hall and a landing throws its sparks up
       off whatever it hit. Light, so this pass -- the bow's own shots are
       drawn here too, and a falling bolt is one of them. */
    this.drawQuarrelGlow(m);
"""

# ---------------------------------------------------------------------------
# 6. the limbs' hook in drawWeapon (in the weapon's own rotated frame)
LIMB_ANCHOR = "        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);\n      }\n"
LIMB_CODE = """      /* QUARRELSTORM (v83 section 4): the bow's limbs glow forge-orange for
         the window and cool after it, drawn over the shape in the frame the
         shape was drawn in. `quarrelFade` is 0 on every other relic, so this
         is one comparison on a field nothing else writes. */
      if (f.quarrelFade > 0 && f.w.shape === "bow")
        this._quarrelLimbs(c, reach + 6, f.w.artW, f);
"""

# ---------------------------------------------------------------------------
# 7. the drawing methods
DRAW_ANCHOR = "  drawMotes(m){\n"
DRAW_CODE = """  /* ------------------------------------------------ QUARRELSTORM'S PICTURE ---
     v83 section 4, drawn off the MATCH's bolts (`m.hail`, each {x, y, t,
     side}: the sim's own records, read and never written) and the fighter's
     `quarrel*` fields -- never `m.ultFx`, one slot the opponent's cast takes
     (open item 25). A bolt in the air is drawn from its own fall, `t /
     fallT` on the window's clock, so it hangs where the sim holds it through
     a hit stop; nothing here keeps state per bolt and nothing draws from the
     rng (shellHash on the landing's count). One method a component, so each
     can be measured alone.
       drawQuarrel      WORLD, under both balls: a landing's splash ring
                        (out to the bolt's reach) and dust; each bolt's rune
                        and the ring closing on it from that reach.
       drawQuarrelGlow  EMISSIVE, over both fighters: each bolt falling from
                        the top of the live hall (the bow's own shot, streak
                        and dart, pointing down); a landing's six sparks and
                        its iron-spark motes (the design's field, drawn). */
  drawQuarrel(m){
    const FA = m.a.quarrelFx, FB = m.b.quarrelFx;
    if (!m.hail.length && !FA.length && !FB.length) return;
    const c = this.ctx, D = AFFINITIES.dwarven;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of FA) this._quarrelSplash(c, q, D);
    for (const q of FB) this._quarrelSplash(c, q, D);
    for (const q of FA) this._quarrelDust(c, q);
    for (const q of FB) this._quarrelDust(c, q);
    for (const d of m.hail){
      const f = m[d.side], u = f.w.ult;
      const al = m.over ? 1 - clamp(f.quarrelEnd / %END%, 0, 1) : 1;
      if (!(al > 0)) continue;
      const p = clamp(d.t / u.fallT, 0, 1);
      this._quarrelRing(c, d, p, u.hitR, al, D);
      this._quarrelRune(c, d, al, D);
    }
    c.restore();
  }
  /* THE SPLASH: a ring out to the bolt's reach, `hitR` -- a foe whose shell
     touches it was struck, which is `tickHail`'s own test drawn. Struck in
     the school's glow; a miss in dust. */
  _quarrelSplash(c, q, D){
    const k = q.t / q.puff;
    if (k >= 1) return;
    const e = 1 - Math.pow(1 - clamp(k / 0.4, 0, 1), 3);
    c.globalAlpha = (1 - k) * (q.hit ? 0.75 : 0.45);
    c.strokeStyle = q.hit ? D.glow : %MISSC%;
    c.lineWidth = (q.hit ? 3.4 : 2.4) * (1 - 0.6 * k);
    c.beginPath(); c.arc(q.x, q.y, %RUNE% + (q.r - %RUNE%) * e, 0, TAU); c.stroke();
  }
  /* THE DUST: five soft blobs kicked out and up off the spot. */
  _quarrelDust(c, q){
    const k = q.t / q.puff;
    if (k >= 1) return;
    const e = 1 - Math.pow(1 - clamp(k / 0.4, 0, 1), 3);
    c.fillStyle = %DUST%;
    c.globalAlpha = (1 - k) * (1 - k) * (q.hit ? 0.5 : 0.32);
    for (let j = 0; j < 5; j++){
      const h = shellHash(9931 + q.s, q.n * 8 + j);
      const a = j * TAU / 5 + h * 0.9, dd = (8 + 30 * e) * (0.7 + 0.5 * h);
      c.beginPath();
      c.arc(q.x + Math.cos(a) * dd, q.y + Math.sin(a) * dd * 0.7 - 14 * e,
            4 + 7 * e * (0.6 + 0.4 * h), 0, TAU);
      c.fill();
    }
  }
  /* THE RING CLOSING ON THE RUNE, from the bolt's reach in to the rune as
     the bolt falls: where it will land, and how soon. */
  _quarrelRing(c, d, p, hitR, al, D){
    c.globalAlpha = al * (0.35 + 0.45 * p);
    c.strokeStyle = D.glow; c.lineWidth = 1.6 + 1.6 * p;
    c.beginPath(); c.arc(d.x, d.y, %RUNE% + (hitR - %RUNE%) * (1 - p), 0, TAU); c.stroke();
  }
  /* THE RUNE: dwarven dark, r %RUNE%, ringed and crossed in the school's core. */
  _quarrelRune(c, d, al, D){
    c.globalAlpha = al * 0.92;
    c.fillStyle = D.dark;
    c.beginPath(); c.arc(d.x, d.y, %RUNE%, 0, TAU); c.fill();
    c.strokeStyle = D.core; c.lineWidth = 2.4;
    c.beginPath(); c.arc(d.x, d.y, %RUNE%, 0, TAU); c.stroke();
    c.lineWidth = 2;
    c.beginPath();
    for (let i = 0; i < 4; i++){
      const a = i * TAU / 4 + TAU / 8;
      c.moveTo(d.x + Math.cos(a) * %RUNE% * 0.3, d.y + Math.sin(a) * %RUNE% * 0.3);
      c.lineTo(d.x + Math.cos(a) * %RUNE% * 0.78, d.y + Math.sin(a) * %RUNE% * 0.78);
    }
    c.stroke();
  }
  drawQuarrelGlow(m){
    const FA = m.a.quarrelFx, FB = m.b.quarrelFx;
    if (!m.hail.length && !FA.length && !FB.length) return;
    const c = this.ctx, D = AFFINITIES.dwarven;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round"; c.lineJoin = "round";
    for (const d of m.hail){
      const f = m[d.side], u = f.w.ult;
      const al = m.over ? 1 - clamp(f.quarrelEnd / %END%, 0, 1) : 1;
      if (!(al > 0)) continue;
      const p = clamp(d.t / u.fallT, 0, 1);
      /* FROM THE TOP OF THE LIVE HALL (the seals walk `inset` in) to the
         spot, gathering speed: a third of the way in the first half. */
      const top = Math.min((m.inset || 0) + 12, d.y);
      const hy = top + (d.y - top) * (p * p * 0.35 + p * 0.65);
      const r = (f.w.shot && f.w.shot.r) || 24;
      this._quarrelStreak(c, d.x, top, hy, r, al, D);
      this._quarrelDart(c, d.x, hy, r, al);
    }
    for (const q of FA){ this._quarrelSparks(c, q, D); this._quarrelMotes(c, q, D); }
    for (const q of FB){ this._quarrelSparks(c, q, D); this._quarrelMotes(c, q, D); }
    c.restore();
  }
  /* THE STREAK: the bow's own shot's gradient (dark to core to glow), stood
     on end, never above the ceiling it fell from. */
  _quarrelStreak(c, x, top, hy, r, al, D){
    const tl = Math.min(110, hy - top + 8);
    if (!(tl > 1)) return;
    const g = c.createLinearGradient(x, hy - tl, x, hy);
    g.addColorStop(0, D.dark + "00");
    g.addColorStop(0.55, D.core + "88");
    g.addColorStop(1, D.glow);
    c.globalAlpha = al;
    c.strokeStyle = g; c.lineWidth = r * 0.30;
    c.beginPath(); c.moveTo(x, hy - tl); c.lineTo(x, hy); c.stroke();
  }
  /* THE DART: the bow's own shot's head, pointing down. */
  _quarrelDart(c, x, hy, r, al){
    c.globalAlpha = al;
    c.fillStyle = "#FFF4D0";
    c.beginPath();
    c.moveTo(x, hy + r * 1.05);
    c.lineTo(x + r * 0.42, hy - r * 0.55);
    c.lineTo(x, hy - r * 0.20);
    c.lineTo(x - r * 0.42, hy - r * 0.55);
    c.closePath(); c.fill();
  }
  /* SIX SPARKS off a landing, fanned up out of the spot and falling back,
     each a short streak along its own path. Turned by the landing's count. */
  _quarrelSparks(c, q, D){
    if (!q.hit) return;
    const k = q.t / q.puff;
    if (k >= 1) return;
    c.lineWidth = 2.2 * (1 - 0.5 * k);
    for (let j = 0; j < %SPARKN%; j++){
      const h1 = shellHash(9941 + q.s, q.n * 8 + j), h2 = shellHash(9947 + q.s, q.n * 8 + j);
      const a = -Math.PI / 2 + ((j + 0.5) / %SPARKN% - 0.5) * 2.6 + (h1 - 0.5) * 0.35;
      const v = 150 + 110 * h2, t = q.t;
      const vx = Math.cos(a) * v, vy = Math.sin(a) * v + 520 * t;
      const x = q.x + Math.cos(a) * v * t, y = q.y + Math.sin(a) * v * t + 260 * t * t;
      c.globalAlpha = 1 - k;
      c.strokeStyle = j % 2 ? D.glow : "#FFD9A0";
      c.beginPath(); c.moveTo(x, y); c.lineTo(x - vx * 0.045, y - vy * 0.045); c.stroke();
    }
  }
  /* IRON-SPARK MOTES off a landing (the design's field, drawn: a particle
     field fires once, at the cast, on the one ultFx slot, and these are on
     every landing for the whole window): %MOTEN% embers rising off the spot. */
  _quarrelMotes(c, q, D){
    if (!q.hit) return;
    const k = q.t / %MOTE%;
    if (k >= 1) return;
    c.fillStyle = D.glow;
    for (let j = 0; j < %MOTEN%; j++){
      const h1 = shellHash(9953 + q.s, q.n * 8 + j), h2 = shellHash(9959 + q.s, q.n * 8 + j);
      const t = q.t;
      c.globalAlpha = Math.sin(Math.PI * k) * 0.85;
      c.beginPath();
      c.arc(q.x + (h1 - 0.5) * 44 + Math.sin(t * 3 + j * 1.7) * 5,
            q.y - 6 - t * (20 + 16 * h2), 1.3 + 1.1 * h2, 0, TAU);
      c.fill();
    }
  }
  /* THE LIMBS IN THE FORGE: SHAPES.bow's own limb path, verbatim, stroked
     over the shape at a forge's dull red, a forge-orange edge and, while it
     is hot, a pale heart; the rivets redrawn on top so the plate still
     reads. Up over the ignition, down over the cool. */
  _quarrelLimbs(c, L, W, f){
    const h = clamp(f.quarrelAge / %IGN%, 0, 1) * f.quarrelFade;
    if (!(h > 0.004)) return;
    const lh = W * 0.95, rx = L * 0.13, a0 = c.globalAlpha;
    const limb = (wd, col) => {
      c.strokeStyle = col; c.lineWidth = Math.max(1, wd);
      c.beginPath();
      c.moveTo(rx - L*0.06, -lh);
      c.quadraticCurveTo(rx + L*0.34, -lh*0.44, rx + L*0.17, 0);
      c.quadraticCurveTo(rx + L*0.34,  lh*0.44, rx - L*0.06,  lh);
      c.stroke();
    };
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    c.globalAlpha = a0 * h;
    limb(W * 0.13, %HOTB%);
    limb(W * 0.065, %HOTF%);
    c.globalAlpha = a0 * h * h;
    limb(W * 0.024, %HOTH%);
    c.globalAlpha = a0;
    for (const sg of [-1, 1]){
      for (let i = 0; i < 3; i++){
        const u = 0.22 + i * 0.29, it = 1 - u;
        const qx = it*it*(rx - L*0.06) + 2*it*u*(rx + L*0.34) + u*u*(rx + L*0.17);
        const qy = it*it*(sg * lh) + 2*it*u*(sg * lh * 0.44);
        c.fillStyle = SHAPES._ink(f.aff.dark, 9.71);
        c.beginPath(); c.arc(qx, qy, W*0.075, 0, TAU); c.fill();
        c.fillStyle = f.aff.steel;
        c.beginPath(); c.arc(qx, qy, W*0.042, 0, TAU); c.fill();
      }
    }
    c.restore();
  }

"""


# ---------------------------------------------------------------------------
# 8-9. the nova's floor dust and release flash, retired
def under_old(s):
    return between(s, "    /* ---- Quarrelstorm: the dust the release blows off the floor ------------ */\n",
                   "\n    /* ---- Bulwark: the plates' footprint, a tiled ring ---------------------- */\n")


def over_old(s):
    return between(s, "    /* ---- Quarrelstorm: the RELEASE. Not arrows — drawShots draws those ----- */\n",
                   "\n    /* ---- Bulwark: interlocking plates of light, let go ---------------------- */\n")


UNDER_CODE = """    /* ---- Quarrelstorm's floor dust was the NOVA's; retired with it (v83,
       v108 stage 6). The hail's picture is `drawQuarrel`, off the fighter
       and the match's bolts, where the one ultFx slot cannot erase it. */
"""
OVER_CODE = """    /* ---- Quarrelstorm's release was the NOVA's (fourteen arrow streaks and
       the mount's kick ring); retired with it (v83, v108 stage 6). The cast
       is the limbs igniting and the first bolt's rune (`drawQuarrel`). */
"""


# ---------------------------------------------------------------------------
# 10. the charge rune
def sig_old(s):
    return between(s, "  /* QUARRELSTORM -- eight heads going out. The nova of arrows, counted. */\n",
                   "  /* BULWARK -- the shield, and the shove that comes off it. */\n")


SIG_CODE = """  /* QUARRELSTORM -- iron falling on a mark. The nova's eight heads went out
     with the nova (v83): three bolts drop onto a crossed rune, lower as the
     charge fills, and are on it at the moment it goes off. */
  ironhail(c, t, cf, P){
    SG.ring(c, 0, 0.52, 0.24, P.glow, 0.07, 0.4 + cf * 0.55);
    SG.path(c, [[-0.1, 0.42], [0.1, 0.62]], P.glow, 0.05, 0.3 + cf * 0.5);
    SG.path(c, [[0.1, 0.42], [-0.1, 0.62]], P.glow, 0.05, 0.3 + cf * 0.5);
    for (let i = 0; i < 3; i++){
      const x = (i - 1) * 0.44, lag = i === 1 ? 0 : 0.14;
      const y = -0.78 + Math.max(0, cf - lag) / (1 - lag) * 0.95 - (i === 1 ? 0 : 0.1);
      SG.path(c, [[x, y - 0.42], [x, y]], P.core, 0.075, 0.45 + cf * 0.5);
      SG.poly(c, [[x, y + 0.2], [x + 0.13, y - 0.02], [x - 0.13, y - 0.02]], P.core, 0.55 + cf * 0.45);
    }
  },
"""


# ---------------------------------------------------------------------------
# 11-12. the banner's letters
SPREAD_ANCHOR = "                     ironhail: 46, farwarden: 118 }[b.w];\n"
SPREAD_CODE = "                     farwarden: 118 }[b.w];   // Quarrelstorm's letters fall: no spread (v108)\n"


def banner_old(s):
    return between(s, '    else if (b.w === "ironhail"){\n', '    else if (b.w === "spellbreaker"){\n')


BANNER_CODE = """    else if (b.w === "ironhail"){
      /* THE LETTERS FALL, each on its own bolt: Quarrelstorm is iron hail
         now (v83), so the name drops out of the ceiling letter by letter, a
         streak over each, and lands on the line. The fan of fourteen arrows
         the letters used to converge from went out with the nova. */
      const fall = (i) => 1 - ease(clamp((age - i * 0.022) / 0.16, 0, 1));
      fn = (i) => { const s = fall(i); return { dy: -s * 300 * k, a: 1 - s * 0.35 }; };
      if (age < 0.5){
        c.save();
        c.globalCompositeOperation = "lighter";
        c.shadowBlur = 0;
        c.strokeStyle = glow; c.lineCap = "round";
        c.font = `700 ${size}px 'Atkinson Hyperlegible Next',sans-serif`;
        const ws = [];
        let tot = -track;
        for (const ch of b.text){ const w = c.measureText(ch).width; ws.push(w); tot += w + track; }
        let lx = cx - tot / 2;
        for (let i = 0; i < b.text.length; i++){
          const s = fall(i), mx = lx + ws[i] / 2;
          lx += ws[i] + track;
          if (s < 0.01) continue;
          const ly = y - size * 0.78 - s * 300 * k;
          c.globalAlpha = s * 0.7;
          c.lineWidth = (1.5 + 2.5 * s) * k;
          c.beginPath(); c.moveTo(mx, ly - (40 + 90 * s) * k); c.lineTo(mx, ly); c.stroke();
        }
        c.restore();
      }
    }
"""


def rows():
    s = src_text()

    def fill(code):
        for k, v in PICK.items():
            code = code.replace("%" + k + "%", str(v))
        left = re.findall(r"%[A-Z_]+%", code)
        assert not left, left
        return code

    R = [
        dict(label="quarrelstorm picture: fighter fields", anchor=FIGHTER_ANCHOR, mode="after", code=FIGHTER_CODE,
             why="The picture's own state on the fighter (the limbs cool past ultHail; a landing's puff outlives its bolt, which tickHail splices); never m.ultFx (open item 25). Read by nothing in the sim."),
        dict(label="quarrelstorm picture: the presentation call", anchor=PCALL_ANCHOR, mode="after", code=PCALL_CODE,
             why="tickPresentation runs through hit stops and after the match; one call to tickQuarrel."),
        dict(label="quarrelstorm picture: tickQuarrel", anchor=TICK_ANCHOR, mode="before", code=TICK_CODE,
             why="Drives the limbs (ignite at the cast, hold, cool 0.5s off ultHail && !over) and each resolved bolt, found by hailTally.landed/missed rising and the bolt that left m.hail (read, never written): a puff record at its spot, hit or miss by the tally, and on a hit the SUNDER tag on the foe with its count (in place if one is up). Writes presentation fields, tags and taught only; shellHash, no rng."),
        dict(label="quarrelstorm picture: the ground call (world, under both balls)", anchor=GROUND_ANCHOR, mode="after", code=GROUND_CODE,
             why="World pass under both balls: the runes, the closing rings, the splash and the dust (bloom share 0)."),
        dict(label="quarrelstorm picture: the emissive call (over both fighters)", anchor=GLOW_ANCHOR, mode="after", code=GLOW_CODE,
             why="Emissive pass over both fighters, beside the bow's own shots: the falling bolts, the sparks, the motes."),
        dict(label="quarrelstorm picture: the limbs' hook in drawWeapon", anchor=LIMB_ANCHOR, mode="after", code=LIMB_CODE,
             why="While quarrelFade > 0 the bow's limbs are stroked forge-orange over the shape, in the shape's own frame; SHAPES.bow is untouched, so every other bow draws as before."),
        dict(label="quarrelstorm picture: the drawing methods", anchor=DRAW_ANCHOR, mode="before", code=DRAW_CODE,
             why="drawQuarrel / drawQuarrelGlow and one method a component (splash, dust, ring, rune, streak, dart, sparks, motes, limbs)."),
        dict(label="quarrelstorm picture: the nova's floor dust retired", anchor=under_old(s), mode="replace", code=UNDER_CODE,
             why="drawUltUnder's ironhail branch was the NOVA's release dust (a 210-unit ring off the caster); the nova is out (v108 stage 1), so its picture goes too."),
        dict(label="quarrelstorm picture: the nova's release flash retired", anchor=over_old(s), mode="replace", code=OVER_CODE,
             why="drawUltOver's ironhail branch was the NOVA's release (14 arrow streaks, 'N == u.shots', and the kick ring); retired with the nova."),
        dict(label="quarrelstorm picture: the charge rune", anchor=sig_old(s), mode="replace", code=SIG_CODE,
             why="ULTSIG.ironhail drew the nova's eight heads going out; now three bolts dropping onto a crossed rune, assembling with the charge."),
        dict(label="quarrelstorm picture: the banner's spread", anchor=SPREAD_ANCHOR, mode="replace", code=SPREAD_CODE,
             why="The banner's clamp reserved 46 a letter for the fan's horizontal throw; the falling letters have none."),
        dict(label="quarrelstorm picture: the banner's letters fall", anchor=banner_old(s), mode="replace", code=BANNER_CODE,
             why="The banner's letters converged in a fan (the nova's); they now drop from above, a streak over each (Daybreak's rising letters, the other way)."),
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


FX_OLD = """    /* A VOLLEY IS MANY SHOTS, so it emits across nearly its whole life. */
    ironhail: { mode: 'beam', n: 1300, sp: [50, 240], grav: 140, drag: 1.4,
                life: [0.22, 0.65], heavy: 0.03, size: [0.6, 1.7],
                spawn: 0.80, up: 0 },
"""


def fx_out(s: str):
    """SPECS.ironhail out of the INLINED copy, stamp re-cut -- exactly what the orchestrator's
    sync_fx_remove does to both copies (dawn_build.py's shape). Scratch: fx.js is not touched."""
    mod = FXJS.read_text(encoding="utf-8")
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n", s)
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    assert s[head.end():tm.start()].rstrip("\n") == mod.rstrip(), "fx.js and the inlined copy DIVERGED"
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
    s = src if src is not None else src_text()
    R = rows()
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
    n, d, _ = build(HERE / "ih-final.html")
    print(f"ih-final.html: {n} script blocks parse, {d:+d} chars, stamp {stamp_of((HERE / 'ih-final.html').read_bytes().decode('utf-8'))}")
    n, d, info = build(HERE / "ih-final-fx.html", fxout=True)
    print(f"ih-final-fx.html: {n} script blocks parse, {d:+d} chars, fx.js stamp {info['fx_old'][:16]} -> {info['fx_new'][:16]}")
