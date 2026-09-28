#!/usr/bin/env python
"""CIPHER / CONVERGENCE -- the runic staff, the staff row's third. v94.

Built from `06-docs/v94/CIPHER-BUILD-BRIEF.md` and `runic-staff-design-v94.md`
(Cowork, 2026-09-27), the row's `06-docs/v89/STAFF-ROW-v89.md` §1/§6 -- the
input and the only input (CLAUDE.md §3 rule 0). Rick: "build them all".

    stage 1   the relic, its ultimate STUBBED          sc-bloom-fx -> sc-cipher
    stage 2   the spell: GLYPH (the wall-stop)         sc-cipher -> sc-glyph
    stage 3   the ultimate: CONVERGENCE (the recall)   sc-glyph -> sc-converge
    stage 5   the blade, wide on 151: 11 -> 8.875       sc-converge -> sc-converge-blade
    stage 6   picture, voices                          sc-converge-blade -> sc-cipher-fx

THE BASE is the staff branch's tip (Culverin 1-6, Briarwand 1-6); several
anchors are those builds' own lines, so the staves carry together, in order.

THE READINGS, where the build has to choose:
  1. THE SIGIL'S NUMBERS are flat shot fields (`sigilLife`, `sigilHex`) where
     the design writes `sigil: { life, hex }` -- the shot block's writer and
     every check handle numbers; the meaning is the design's.
  2. `bounce 1` IS SET AT SPAWN, as the design declares (§5: "`spawnShot`
     sets `bounce 1`"). The lab tagged it after the bolt's first step, so a
     bolt loosed INTO a wall was spent by the engine before it could be
     tagged and never hung -- Briarwand's fan had the same shape (v93 build
     §2). Measured at stage 2.
  3. LAID ORDER is the order the sigils were laid (`laid`, the match clock),
     as §5 says; the lab used the array order, which is SPAWN order.
  4b. (stage 5) READING 2 IS WORTH +14 POINTS AND THE ENGINE'S WINDOW +5: the
     build with the lab's tagging put back is the lab's arm S to the decimal
     (30.5%) and its arm Y at the engine's window (55.5% against 56.8%), so the
     blade pays for both -- 11 -> 8.875 (v94 build §4).
  4. A SIGIL STILL WAITING WHEN THE WINDOW CLOSES STILL LAUNCHES, as the lab's
     did (its launch loop ran whatever the window): the window holds its
     state until no sigil of the caster's is waiting (Corollary's queue, the
     same shape).
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC, BUILDER = "cipher", "cipher_build.py"
BLADE = 11                     # brief §2 stage 1: "stubbed relic at 11"; stage 5 settles it
# Stage 5, measured wide on 151 (both sides, two seed blocks, 1440 fights a row,
# no bisection): 8.75 47.1%, 8.875 49.2%, 9.0 52.0% (06-docs/v94/runs/build/stage5_*).
TUNED_BLADE = 8.875
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.34, speed=380, r=22, life=3.4, grav=0, dmgMul=1.0, sigilLife=4.0, sigilHex=2,
             spell="glyph", tip="Bolts stop on walls as runes · clankable")
CARD = "Every rune on the walls leaves it and hunts the foe, hexing"
ULT_NAME, ULT_KIND = "Convergence", "converge"
# Design §5, brief §0. `charge` is the lab's 16 in the game's clock, measured.
ULT = {"charge": 14, "dur": 8, "gap": 0.25, "fuse": 0.5, "home": 3, "speed": 380, "life": 3.0}
ULT_KEYS = list(ULT)
BLURB = ("A slate rod written root to head. What it misses it keeps on the walls, "
         "and for eight seconds it calls them all back.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the runic BOW
     body at the staff's blade -- which stage 2's glyph is measured against.
'''
ULT_STUB = f'''    /* CONVERGENCE. STUBBED AT `charge:1e9` IN STAGE 1. `kind:"{ULT_KIND}"` is
       its own; the card is Cowork's (design §6), in at stage 1. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''
S1_BLADE_PARA = f'''     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 11 on Chromium 141, and stage 5 settles it wide on 151. */'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* CIPHER -- THE RUNIC STAFF, the staff row's third relic. Built from
     `06-docs/v94/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Runic knows things in
     advance and writes them down -- so the staff writes its misses on the
     walls and then reads them back (design, "why this cell").

{S1_SHOT_PARA}
{S1_BLADE_PARA}
  {{ id:"{RELIC}", name:"Cipher", aff:"runic", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{BLADE}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ hex:1 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [("Cipher joins the roster, its ultimate stubbed",
             '''

];
/* The single source of truth for "which status does this relic teach".''',
             relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".''')]


S2_SHOT_PARA = '''     THE SPELL IS GLYPH (design §1, §5): a rune bolt every 0.34s at an
     arrow's speed (r 22). One that lands hexes 1. One that reaches a wall
     does not die: it STOPS there and hangs as a sigil for `sigilLife` s, and
     a foe that touches it takes the blow and is hexed `sigilHex`. A sigil is
     a stationary SHOT -- the foe's blade clanks it away (the counterplay),
     its life runs out, and nothing else in the engine had to learn it
     exists. `r` stays 22: a bigger sigil sits inside the wall and the wall
     kills it (design §5, measured). The wall-stop alone is +22 (§3.1).
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Cipher looses the glyph",
 f'''  {{ id:"{RELIC}", name:"Cipher", aff:"runic", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Cipher", aff:"runic", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("spawnShot: a glyph leaves with one bounce",
 '''      s.spell = S.spell; s.sx = s.x; s.sy = s.y;
    }
''',
 '''      s.spell = S.spell; s.sx = s.x; s.sy = s.y;
      /* CIPHER'S GLYPH (v94 §5): one bounce, AT SPAWN, so the wall branch of
         `tickShots` can turn it into a sigil the moment a wall spends it --
         including a bolt loosed INTO a wall, which the lab (tagging after the
         first step) lost. `glyph` marks it for that branch. */
      if (S.sigilLife){ s.bounce = 1; s.glyph = true; }
    }
'''),

("tickShots: a glyph that a wall stops hangs as a sigil",
 '''          if (s.kunai) this.kunaiRung(s, src);
        }
      }
''',
 '''          if (s.kunai) this.kunaiRung(s, src);
          /* THE WALL-STOP (v94 §5): a glyph whose one bounce the wall has just
             spent STOPS where it hit and hangs -- five assignments and a flag,
             and it is still a shot: `resolveHit` pays its touch (the sigil's
             hex through `over`), a blade clanks it, its life runs out. `laid`
             is the match clock, so CONVERGENCE can read the order the sigils
             were laid in. A FLOWN rune (`flown`) never comes back through here:
             it has no bounce left, and the wall kills it as any shot. */
          if (s.glyph && s.bounce === 0 && !s.flown){
            const G = src.w.shot;
            s.sigil = true; s.vx = 0; s.vy = 0; s.grav = 0;
            s.life = G.sigilLife; s.max = G.sigilLife;
            s.over = { onHit: { hex: G.sigilHex } };
            s.laid = this.t;
          }
        }
      }
'''),
    ]


ULT_NOTE = '''    /* CONVERGENCE (design §1, §5). For `dur` seconds the runes come off the
       walls: every sigil hanging at the cast leaves its wall `gap` s apart in
       the order it was laid, and every sigil laid inside the window leaves
       `fuse` s after it is laid -- each flies at the foe at `speed`, homing
       `home` rad/s, for `life` s, and its blow is the sigil's (hex 2).
       Seekers made of misses (+26 in the design's first cut); detonating the
       same sigils priced at +0 and is not what was built.

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v94/cipher-build-v94.md`. */
'''


def s3_edits(U: dict):
    return [
("Convergence is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Convergence's window",
 '''    this.pollenAge = 0;
''',
 '''    this.pollenAge = 0;
    /* {t, dur, cast} while CONVERGENCE's window is open (v94) -- and after it
       closes, until no sigil of this fighter's is still waiting to leave (the
       lab launched those whatever the window; Corollary's queue has the same
       shape). null otherwise: `tickConverge` returns after a two-iteration
       loop. `convergeTally` is the probe's; nothing in the sim reads it. */
    this.ultConverge = null;
    this.convergeTally = null;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "bloom"){
''',
 '''    if (u.kind === "converge"){
      /* CONVERGENCE (v94). NOTHING RESOLVES HERE: `tickConverge` fuses the
         hanging sigils on its first step (the window's `cast` flag) and
         launches them. `m.ultFx` is the cast flash only (open item 25). */
      f.ultConverge = { t: 0, dur: u.dur, cast: true };
      if (!f.convergeTally) f.convergeTally = { casts: 0, atCast: 0, fused: 0, launched: 0 };
      f.convergeTally.casts++;
      return;
    }
    if (u.kind === "bloom"){
'''),

("the recall ticks with the window tickers",
 '''    this.tickPollen(dt);                // BLOOM (v93): the cloud drifts and bites
''',
 '''    this.tickPollen(dt);                // BLOOM (v93): the cloud drifts and bites
    this.tickConverge(dt);              // CONVERGENCE (v94): the runes leave the walls
'''),

("tickConverge fuses and launches the runes",
 '''  /* ===================================================== BLOOM ========''',
 '''  /* =============================================== CONVERGENCE ========
     v94 §5, and the lab (`overlays/staff_runic.js`) where the prose is silent.
     On the window's FIRST step every sigil of the caster's that is hanging
     gets `fuse = gap * k` on the window's clock, k in LAID order (`laid`);
     inside the window, a sigil laid afterwards gets `fuse = t + fuse` on the
     step it appears. When the clock reaches a fuse the rune leaves: velocity
     `speed` at the foe, `home`, `life`, no longer a sigil, `flown` -- and
     `tickShots` does the rest (the homing, the hit with the sigil's hex 2,
     the parry, the wall that kills it).

     A FUSED SIGIL STILL LAUNCHES AFTER THE WINDOW CLOSES (the lab's launch
     loop ran whatever the window), so the state is kept until no sigil of
     the caster's is waiting, and dropped on a death or the end.

     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step (the difference the charge conversion carries). */
  tickConverge(dt){
    for (const f of [this.a, this.b]){
      const C = f.ultConverge;
      if (!C) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultConverge = null; continue; }
      C.t += dt;
      const u = f.w.ult, own = f === this.a ? "a" : "b", T = f.convergeTally;
      if (C.cast){
        C.cast = false;
        const hang = this.shots.filter(s => s.own === own && s.sigil && s.fuse === undefined)
                               .sort((p, q) => p.laid - q.laid);
        hang.forEach((s, k) => { s.fuse = u.gap * k; });
        T.atCast += hang.length;
      }
      let waiting = 0;
      for (const s of this.shots){
        if (s.own !== own || !s.sigil) continue;
        if (s.fuse === undefined){
          if (C.t < C.dur){ s.fuse = C.t + u.fuse; T.fused++; } else continue;
        }
        if (C.t < s.fuse){ waiting++; continue; }
        const a = Math.atan2(foe.y - s.y, foe.x - s.x);
        s.vx = Math.cos(a) * u.speed; s.vy = Math.sin(a) * u.speed; s.a = a;
        s.home = u.home; s.life = u.life; s.max = u.life;
        s.sigil = false; s.flown = true; s.fuse = undefined; s.flownAt = this.t;
        T.launched++;
      }
      if (C.t >= C.dur && !waiting) f.ultConverge = null;
    }
  }

  /* ===================================================== BLOOM ========'''),

("the glyph, the sigil and the flown rune are drawn (first cuts)",
 '''      if (s.spell === "thornburst"){
''',
 '''      /* CIPHER'S RUNES (v94 §6.1) -- FIRST CUTS, for stage 3's film; the
         picture is stage 6's. A bolt is a rune glyph with a short trail; on
         the wall it STOPS and hangs as a sigil (the glyph in a ring, `glow`,
         breathing over its life); a flown rune is the glyph again, trailing,
         and for its first 0.2s a thin sight-line to the foe. Derived from the
         shot's own state; no rng. */
      if (s.spell === "glyph"){
        const pal = s.aff, age = s.max - s.life;
        c.save();
        c.globalCompositeOperation = "lighter";
        if (s.sigil){
          const br = 0.75 + 0.25 * Math.sin(age * 5 + s.laid * 3);
          const fade = clamp(s.life / 0.4, 0, 1);
          c.globalAlpha = 0.6 * br * fade;
          c.strokeStyle = pal.glow; c.lineWidth = 2.4;
          c.beginPath(); c.arc(s.x, s.y, s.r, 0, TAU); c.stroke();
        } else {
          const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
          c.globalAlpha = 0.55;
          c.strokeStyle = pal.core; c.lineWidth = s.r * 0.5;
          c.beginPath(); c.moveTo(s.x - ux * s.r * 2.2, s.y - uy * s.r * 2.2); c.lineTo(s.x, s.y); c.stroke();
          if (s.flown && m.t - s.flownAt < 0.2){
            const foe = s.own === "a" ? m.b : m.a;
            c.globalAlpha = 0.35; c.lineWidth = 1.2; c.strokeStyle = pal.glow;
            c.beginPath(); c.moveTo(s.x, s.y); c.lineTo(foe.x, foe.y); c.stroke();
          }
        }
        /* THE GLYPH: three strokes of a rune, turning slowly, in the school's
           light -- the same mark hanging or flying. */
        c.globalAlpha = s.sigil ? 0.9 : 1;
        c.translate(s.x, s.y); c.rotate(s.sigil ? age * 0.6 : s.a);
        c.strokeStyle = pal.glow; c.lineWidth = 2.2; c.lineCap = "round";
        const q = s.r * 0.55;
        c.beginPath();
        c.moveTo(-q, -q * 0.8); c.lineTo(q * 0.2, 0); c.lineTo(-q, q * 0.8);
        c.moveTo(q * 0.2, -q); c.lineTo(q * 0.2, q);
        c.moveTo(q * 0.2, 0); c.lineTo(q, 0);
        c.stroke();
        c.restore();
        continue;
      }
      if (s.spell === "thornburst"){
'''),
    ]


# ---------------------------------------------------------------- stage 5 --
S5_BLADE_PARA = f'''     `dmg` {fnum(TUNED_BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of every
     pairing, two seed blocks, 1440 fights a row, no bisection -- 8.75 reads
     47.1%, 8.875 49.2%, 9.0 52.0%. 2.1 UNDER THE DESIGN'S 11, AND BOTH HALVES
     ARE MEASURED: a bolt loosed INTO a wall hangs (§5 tags at spawn; the lab
     tagged after the first step and lost it -- a quarter of every sigil, +14
     at 11), and the engine's 8s window is 9.78 of the lab's seconds, because
     its clock stops through hit stop (+5). Put the lab's tagging back and the
     build IS the lab: 30.5% against arm S's 30.5%. Provisional until the row
     re-prices (v89 §8.2). The number lives in `cipher_build.TUNED_BLADE`. */'''

S3_CLOCK = '''     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step (the difference the charge conversion carries). */'''
S5_CLOCK = '''     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step. The charge conversion carries that for the CHARGE;
     the WINDOW keeps its 8s on this clock, which is 9.78 of the lab's seconds
     (18% of a window's steps are frozen) and worth +5 at the design's blade --
     measured, and paid for by stage 5's blade (v94 build §4). */'''


def s5_edits():
    b = BODY
    return [
("the relic's note says the blade is measured", S1_BLADE_PARA, S5_BLADE_PARA),
("Cipher's blade is the measured one",
 f'''  {{ id:"{RELIC}", name:"Cipher", aff:"runic", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:''',
 f'''  {{ id:"{RELIC}", name:"Cipher", aff:"runic", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(TUNED_BLADE)}, spin:'''),
("the relic's note on tickConverge's clock says what the blade carries", S3_CLOCK, S5_CLOCK),
    ]


# THE PICKED VOICES, from cipher_voice_lab.py (runs/build/stage6_voice_lab.json), verbatim.
VOICES = {
    'cast': '\n  S._sweep(t, { f0: 500, f1: 2600, q: 0.7, gain: 0.1072, dur: 0.32, atk: 0.19, type:"bandpass" });\n  S._tone (t + 0.26, { freq: 1318, gain: 0.05358, dur: 0.45, type:"sine" });\n  S._tone (t + 0.26, { freq: 1976, gain: 0.02679, dur: 0.35, type:"sine" });\n  S._tone (t + 0.26, { freq: 2637, gain: 0.01607, dur: 0.25, type:"sine" });',
    'tap': '\n  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);\n  S._burst(t, { freq: 1100 * k, q: 3.0, gain: 0.08981, dur: 0.025, type:"bandpass" });\n  S._tone (t, { freq: 420 * k, to: 260 * k, gain: 0.05389, dur: 0.04, type:"triangle" });',
    'leave': '\n  S._tone (t, { freq: 880, to: 990, gain: 0.06857, dur: 0.07, type:"triangle" });',
    'hex': '\n  const n = Math.max(1, Math.min(5, p.n | 0)), k = Math.pow(2, (n - 1) * 1.5 / 12);\n  S._tone (t, { freq: 1760 * k, to: 1320 * k, gain: 0.09852, dur: 0.08, type:"triangle" });\n  S._burst(t, { freq: 4000, q: 1.5, gain: 0.07389, dur: 0.015, type:"highpass" });',
    'close': '\n  S._sweep(t + 0, { f0: 1318, f1: 1318, q: 40, gain: 0.2783, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0, { f0: 1976, f1: 1976, q: 40, gain: 0.1392, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0, { f0: 2637, f1: 2637, q: 40, gain: 0.0835, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.1, { f0: 1318, f1: 1318, q: 40, gain: 0.5565, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.1, { f0: 1976, f1: 1976, q: 40, gain: 0.2783, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.1, { f0: 2637, f1: 2637, q: 40, gain: 0.167, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.2, { f0: 1318, f1: 1318, q: 40, gain: 1.113, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.2, { f0: 1976, f1: 1976, q: 40, gain: 0.5565, dur: 0.4, atk: 0.24, type:"bandpass" });\n  S._sweep(t + 0.2, { f0: 2637, f1: 2637, q: 40, gain: 0.3338, dur: 0.4, atk: 0.24, type:"bandpass" });',
}
VOICE_PICKS = {'cast': 'INHALE', 'tap': 'STONE', 'leave': 'PLUCK', 'hex': 'GLINT', 'close': 'STAGGER'}


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule". PRESENTATION ONLY: SFX.play (a no-op headless),
# this.ring and statusTag (presentation lists), render-only fields, drawing
# code -- no rng, no spawnFx, and the wall's one spawnFx is left exactly where
# it was. engine_ab over all 37, Cipher included, is the proof. The voices are
# `cipher_voice_lab.py`'s picks (two rounds; the reversed chime had to be
# three swells to be heard as one), pasted verbatim; each arm opens
# `const S = this;`.


def arm(key: str, indent: str) -> str:
    body = VOICES[key].strip("\n")
    lines = [indent + "const S = this;"] + [indent + (l[2:] if l.startswith("  ") else l) for l in body.splitlines()]
    return "\n".join(lines)


# THE CARRY (staff_carry.py, 2026-09-27). On the design batch's line Coldiron
# (v103) gave the status tag's value expression a SUNDER clause after the
# hemorrhage one, so there the hex clause goes in between them; on the staff
# branch the expression still ends at the hemorrhage clause. The same hex
# clause either way -- and the staff branch's form is untouched, so this
# builder still reproduces every link it wrote there.
SUNDER_TAG = '                   : (k === "sunder" && foe.sunderCap > STATUS.sunder.maxStacks)'
HEX_CLAUSE = '''                   /* AND A RUNE'S BLOW PRINTS THE COUNT (v94 §6.1: "the hex
                      tag ticks by two") -- a sigil or a flown rune, never the
                      bolt's own hex 1. */
                   : (k === "hex" && this._cineShot && this._cineShot.spell === "glyph"
                      && (this._cineShot.sigil || this._cineShot.flown))
'''


def hex_tag_edit(carried: bool):
    if not carried:
        return ("the hex tag counts a rune's two",
                '''                   : (k === "hemorrhage"
                      && foe.bleedCap > STATUS.hemorrhage.maxStacks)
                     ? foe.stacks("hemorrhage") : 0);
''',
                '''                   : (k === "hemorrhage"
                      && foe.bleedCap > STATUS.hemorrhage.maxStacks)
                     ? foe.stacks("hemorrhage")
''' + HEX_CLAUSE + '''                     ? foe.stacks("hex") : 0);
''')
    return ("the hex tag counts a rune's two",
            '''                     ? foe.stacks("hemorrhage")
                   /* AND SUNDER CARRIES ITS COUNT''',
            '''                     ? foe.stacks("hemorrhage")
''' + HEX_CLAUSE + '''                     ? foe.stacks("hex")
                   /* AND SUNDER CARRIES ITS COUNT''')


def s6_edits(carried: bool = False):
    s3 = {l: n for l, o, n in s3_edits(dict(ULT))}
    first_cut = s3["the glyph, the sigil and the flown rune are drawn (first cuts)"]
    return [

("Sfx: Convergence's cast, the wall-stop, the leave, the hex snap and the close",
 '''        } else if (w === "briarwand"){                  // the bud opens
''',
 '''        } else if (w === "cipher"){                     // the rune-ring opens
          /* CONVERGENCE'S CAST -- design §6.2: "a rune-ring 'open' (v75's
             register, the same school) -- an inhale into a chime, 0.4s".
             INHALE (`cipher_voice_lab.py`, Rick's "you pick i overrule"): a
             band of noise rising 500 -> 2600 Hz into a three-partial chime on
             E6, 6 dB under a glyph's blow, loudest 175 ms in (an inhale swells
             INTO the chime; it does not strike). The taps follow, one a rune,
             from `tickConverge`. Cipher fell through to the rune-crack until now. */
''' + arm("cast", "          ") + '''
        } else if (w === "cipher-tap"){                 // a bolt stops on the wall
          /* THE WALL-STOP -- "a short stone tap (the bolt has stopped) -- quiet,
             pitched by how many are hanging". STONE: a bandpassed knock and a
             falling triangle, 30 ms, 18 dB under a glyph's blow, up a semitone
             a sigil (5.2 from one to six). `p.n` counts this one. It REPLACES
             the shared "wall" for a glyph the wall stops: the bolt did not
             bounce. */
''' + arm("tap", "          ") + '''
        } else if (w === "cipher-leave"){               // a rune leaves its wall
          /* "One soft tap per rune as it leaves, in sequence." PLUCK: a
             triangle lifting 880 -> 990 Hz, 45 ms, 14 dB under a glyph's blow
             -- the least like the wall-stop of three (REG 0.06), so a rune
             leaving is not heard as one landing. */
''' + arm("leave", "          ") + '''
        } else if (w === "cipher-hex"){                 // a rune's blow hexes
          /* A RUNE LANDS -- "the bow's own arrow voice plus a hex snap"
             (pitched by count, v75's). GLINT: a falling triangle and a
             highpassed tick, 50 ms, 10 dB under the blow it rides on and the
             least like it; up 1.5 semitones a stack. `p.n` is the foe's hex
             after the blow. */
''' + arm("hex", "          ") + '''
        } else if (w === "cipher-close"){               // the ring shuts
          /* CLOSE -- "the chime reversed": the cast's own three partials as
             narrow bands of noise SWELLING and cut off, three swells 0.1s
             apart, because a single swell from -80 dB is heard for only its
             last fifth of a second. Loudest 280 ms in, of 355. Played by
             `tickConverge` when the window runs out by its clock, never on a
             death. */
''' + arm("close", "          ") + '''
        } else if (w === "briarwand"){                  // the bud opens
'''),

("the wall: a glyph the wall stops is not a bounce",
 '''          this.spawnFx(s.x, s.y, s.aff.glow, 5, 130, 0.24, 2.4);
          SFX.play("wall");
''',
 '''          this.spawnFx(s.x, s.y, s.aff.glow, 5, 130, 0.24, 2.4);
          /* CIPHER (v94 §6.2): a glyph the wall STOPS taps below instead --
             it did not bounce. The spawnFx above stays for every shot: it
             draws the match rng. */
          if (!(s.glyph && s.bounce === 0 && !s.flown)) SFX.play("wall");
'''),

("the wall-stop is heard, pitched by the count",
 '''            s.laid = this.t;
          }
''',
 '''            s.laid = this.t;
            /* THE WALL-STOP, HEARD (§6.2): "a short stone tap -- quiet, pitched
               by how many are hanging", this one counted. Read, never kept. */
            let hung = 0;
            for (const q of this.shots) if (q.own === s.own && q.sigil) hung++;
            SFX.play("ult", { w: "cipher-tap", n: hung });
          }
'''),

("a rune leaving its wall taps",
 '''        T.launched++;
''',
 '''        T.launched++;
        SFX.play("ult", { w: "cipher-leave" });   // "one soft tap per rune as it leaves" (§6.2)
'''),

("the window running out by its clock is heard",
 '''      C.t += dt;
      const u = f.w.ult, own = f === this.a ? "a" : "b", T = f.convergeTally;
''',
 '''      C.t += dt;
      /* "Close: the chime reversed" (§6.2) -- when the window runs out by its
         clock, once, and never on a death (the branch above returns first).
         The state lives on while fused runes drain; the close does not wait. */
      if (C.t >= C.dur && !C.closed){ C.closed = true; SFX.play("ult", { w: "cipher-close" }); }
      const u = f.w.ult, own = f === this.a ? "a" : "b", T = f.convergeTally;
'''),

("the head's ring is lit while the window runs",
 '''      if (C.t >= C.dur && !waiting) f.ultConverge = null;
    }
  }
''',
 '''      if (C.t >= C.dur && !waiting) f.ultConverge = null;
    }
    /* THE HEAD'S RING, LIT (v94 §6.1): 1 while the window runs, down over
       0.4s after it ("Close: the ring dims"). On the fighter; read by
       `drawConverge` alone. */
    for (const f of [this.a, this.b]){
      const C = f.ultConverge;
      f.convergeLit = C && C.t < C.dur ? 1 : Math.max(0, f.convergeLit - dt / 0.4);
    }
  }
'''),

("the fighter carries the ring's light",
 '''    this.ultConverge = null;
    this.convergeTally = null;
''',
 '''    this.ultConverge = null;
    this.convergeTally = null;
    /* THE HEAD'S RING (v94 §6.1): lit 1 in the window, dimming after it.
       Render-only. */
    this.convergeLit = 0;
'''),

("a rune's blow snaps and flares on the foe",
 '''        this._cineShot = s;
        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul, s.over);
        this._cineShot = null;
        /* Along the BOLT's travel, not away from the shooter. A shot that
''',
 '''        this._cineShot = s;
        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul, s.over);
        this._cineShot = null;
        /* CIPHER'S RUNE LANDS (v94 §6.1-6.2): a sigil's or a flown rune's
           blow -- the hex-2 one -- snaps, pitched by the foe's hex, and flares
           on the foe in the school's light. SFX.play and ring draw no rng. */
        if (s.spell === "glyph" && (s.sigil || s.flown)){
          SFX.play("ult", { w: "cipher-hex", n: foe.stacks("hex") });
          this.ring(foe.x, foe.y, s.aff.glow, 12, 60, 0.32, 3);
        }
        /* Along the BOLT's travel, not away from the shooter. A shot that
'''),

hex_tag_edit(carried),

("the staff's runic head: Code's pick, and why",
 '''   ... the bud opens"). A and B stay until Rick has seen it. */
''',
 '''   ... the bud opens"). A and B stay until Rick has seen it. */
/* THE RUNIC HEAD IS "A" -- Code's pick for Cipher, the same ruling: the open
   ring holding an orb (Rick's ref 3), because design §6.1 asks for "an open
   ring" at the head and CONVERGENCE lights exactly that ring. B and C stay
   until Rick has seen it. */
'''),

("the glyph, the sigil and the flown rune: the flash, the flare, the sight-line",
 first_cut,
 '''      /* CIPHER'S RUNES ON SCREEN (v94 §6.1). "A bolt drawn as a rune glyph
         with a short trail; on the wall it STOPS with a small flash and sits
         as a sigil (r 22, the glyph, `glow` at alpha 0.6, breathing over its
         4s) ... every hanging rune flares in sequence (0.25s apart -- the
         order they were laid) and leaves its wall, and each one draws a thin
         sight-line from itself to the foe for its first 0.2s of flight ...
         a rune that lands on a wall flares and leaves it 0.5s later."

         THE FLARE is read off the rune's own `fuse` against its caster's
         window clock, so it peaks on the step the rune leaves -- the
         sequence, the in-window half second and the drain after the window
         are all the same picture. THE STOP is the sigil's first 0.15s.
         Derived from the shot's own state and flat discs (no gradient per
         rune: GRAIN_CACHE); no rng. */
      if (s.spell === "glyph"){
        const pal = s.aff, age = s.max - s.life;
        const own = s.own === "a" ? m.a : m.b, C = own.ultConverge;
        c.save();
        c.globalCompositeOperation = "lighter";
        let ga = 1;
        if (s.sigil){
          const br = 0.75 + 0.25 * Math.sin(age * 5 + s.laid * 3);
          const fade = clamp(s.life / 0.4, 0, 1);
          const fl = C && s.fuse !== undefined ? clamp(1 - (s.fuse - C.t) / 0.25, 0, 1) : 0;
          if (fl > 0){
            c.fillStyle = pal.glow;
            c.globalAlpha = 0.18 * fl; c.beginPath(); c.arc(s.x, s.y, s.r * 1.9, 0, TAU); c.fill();
            c.globalAlpha = 0.30 * fl; c.beginPath(); c.arc(s.x, s.y, s.r * 1.2, 0, TAU); c.fill();
          }
          c.globalAlpha = clamp(0.6 * br + 0.4 * fl, 0, 1) * fade;
          c.strokeStyle = pal.glow; c.lineWidth = 2.4 + 2 * fl;
          c.beginPath(); c.arc(s.x, s.y, s.r * (1 + 0.3 * fl), 0, TAU); c.stroke();
          if (age < 0.15){
            const q = age / 0.15;
            c.globalAlpha = 0.9 * (1 - q); c.lineWidth = 3;
            c.strokeStyle = "#FFFFFF";
            c.beginPath(); c.arc(s.x, s.y, s.r * (0.5 + 1.3 * q), 0, TAU); c.stroke();
          }
          ga = clamp(0.6 * br + 0.4 * fl, 0, 1) * fade;
        } else {
          const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
          const tl = s.r * (s.flown ? 3.2 : 2.2);
          c.globalAlpha = 0.55;
          c.strokeStyle = pal.core; c.lineWidth = s.r * 0.5; c.lineCap = "round";
          c.beginPath(); c.moveTo(s.x - ux * tl, s.y - uy * tl); c.lineTo(s.x, s.y); c.stroke();
          if (s.flown && m.t - s.flownAt < 0.2){
            const foe = s.own === "a" ? m.b : m.a;
            c.globalAlpha = 0.45 * (1 - (m.t - s.flownAt) / 0.2); c.lineWidth = 1.2; c.strokeStyle = pal.glow;
            c.beginPath(); c.moveTo(s.x, s.y); c.lineTo(foe.x, foe.y); c.stroke();
          }
        }
        /* THE GLYPH: three strokes of a rune in the school's light -- the same
           mark hanging or flying, turning slowly on the wall. */
        c.globalAlpha = ga;
        c.translate(s.x, s.y); c.rotate(s.sigil ? age * 0.6 : s.a);
        c.strokeStyle = pal.glow; c.lineWidth = 2.2; c.lineCap = "round";
        const q = s.r * 0.55;
        c.beginPath();
        c.moveTo(-q, -q * 0.8); c.lineTo(q * 0.2, 0); c.lineTo(-q, q * 0.8);
        c.moveTo(q * 0.2, -q); c.lineTo(q * 0.2, q);
        c.moveTo(q * 0.2, 0); c.lineTo(q, 0);
        c.stroke();
        c.restore();
        continue;
      }
      if (s.spell === "thornburst"){
'''),

("drawConverge: the head's ring and the rune motes",
 '''  /* BLOOM ON SCREEN (v93 §6.1).''',
 '''  /* CONVERGENCE ON SCREEN (v94 §6.1): "Cast: the ring at the head lights
     ... Close: the ring dims. Field: rune motes drifting off the walls toward
     the centre." DRAWN, not an fx.js field (the one `m.ultFx` slot is erased
     by the opponent's cast, and `src/render/fx.js` is shared by both chain
     lines) -- off the fighter's own `convergeLit`.

     THE RING is runic head "A"'s own (STAFF.runic): 0.80 of the drawn staff
     (1.7x the sim's L, from R - 6), radius 0.33 of the drawn width (1.3x
     artW). It flashes for the window's first 0.3s.

     THE MOTES leave the four walls and drift a little over halfway to the
     centre, on the match clock (`m.t`), so they do not jump when the window
     drops its state during the dim. No rng: `shellHash`. */
  drawConverge(m){
    const c = this.ctx, R = CONFIG.physics.ballR, A = CONFIG.arena;
    for (const f of [m.a, m.b]){
      const k = f.convergeLit;
      if (!(k > 0.01)) continue;
      const pal = f.aff, C = f.ultConverge;
      c.save();
      c.globalCompositeOperation = "lighter";
      if (f.alive){
        const reach = f.w.reach * m.actMods.reach * f.reachMul;
        const hd = R - 6 + (reach + 6) * 1.7 * 0.80, hr = f.w.artW * 1.3 * 0.33;
        const hx = f.x + Math.cos(f.theta) * hd, hy = f.y + Math.sin(f.theta) * hd;
        const fl = C && C.t < 0.3 ? 1 - C.t / 0.3 : 0;
        const g = c.createRadialGradient(hx, hy, hr * 0.4, hx, hy, hr * 2.4);
        g.addColorStop(0, pal.glow + "99"); g.addColorStop(1, pal.core + "00");
        c.globalAlpha = k * (0.55 + 0.45 * fl);
        c.fillStyle = g; c.beginPath(); c.arc(hx, hy, hr * 2.4, 0, TAU); c.fill();
        c.globalAlpha = k * (0.8 + 0.2 * fl);
        c.strokeStyle = pal.glow; c.lineWidth = 3 + 3 * fl;
        c.beginPath(); c.arc(hx, hy, hr, 0, TAU); c.stroke();
      }
      const n = m.inset, cx = A.w / 2, cy = A.h / 2;
      for (let i = 0; i < 18; i++){
        const side = i % 4, u = shellHash(9811, i);
        const sx = side === 0 ? n : side === 1 ? A.w - n : n + u * (A.w - 2 * n);
        const sy = side === 2 ? n : side === 3 ? A.h - n : n + u * (A.h - 2 * n);
        const ph = (m.t * (0.22 + 0.12 * shellHash(9813, i)) + shellHash(9815, i)) % 1;
        c.globalAlpha = 0.55 * k * Math.sin(ph * Math.PI);
        c.fillStyle = i % 3 ? pal.glow : pal.core;
        c.beginPath(); c.arc(sx + (cx - sx) * ph * 0.55, sy + (cy - sy) * ph * 0.55, 2.3, 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  /* BLOOM ON SCREEN (v93 §6.1).'''),

("drawConverge is drawn with the shots",
 '''    this.drawPollen(m);          // BLOOM's cloud (v93 §6.1)
''',
 '''    this.drawPollen(m);          // BLOOM's cloud (v93 §6.1)
    this.drawConverge(m);        // CONVERGENCE's ring and motes (v94 §6.1)
'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        if "convergeLit" in code:
            return 6
        return 5 if f"dmg:{fnum(TUNED_BLADE)}," in ent else 3
    return 2 if "sigilLife:" in ent else 1


def all_stages(carried: bool = False):
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("5", s5_edits()), ("6", s6_edits(carried))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"])
    ap.add_argument("--src"); ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nCIPHER / CONVERGENCE -- the insert audit against {A.audit}")
        tip_p = (HERE / A.audit).resolve()
        return audit(all_stages(SUNDER_TAG in tip_p.read_text(encoding="utf-8")), tip_p)
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8"); s = s0
    print(f"\nCIPHER / CONVERGENCE -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"briarwand"' not in code or "pollenFade" not in code:
        raise SystemExit("wrong base: no Briarwand stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin and Briarwand stages 1-6 in it")
    have = stage_of(code)
    want = {1: 0, 2: 1, 3: 2, 5: 3, 6: 5}[stage]
    if have != want:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built on stage {want}")
    if stage == 1:
        check_bow_body(code); edits = s1_edits()
    elif stage == 2:
        edits = s2_edits(re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1))
    elif stage == 3:
        edits = s3_edits(dict(ULT))
    elif stage == 5:
        edits = s5_edits()
    else:
        edits = s6_edits(SUNDER_TAG in s0)
    for label, old, new in edits:
        s = one(s, old, new, label)
    out = strip_comments(s)
    shot = SPELL if stage >= 2 else BOW_SHOT
    ent = check_entry(out, RELIC, shot, TUNED_BLADE if stage >= 5 else BLADE, stubbed=(stage <= 2))
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 2 and out.count("if (s.glyph && s.bounce === 0 && !s.flown){") != 1:
        raise SystemExit("REFUSING TO WRITE -- the wall-stop is not there exactly once")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickConverge(dt){", "this.tickConverge(dt);", 'u.kind === "converge"'):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    check_no_rng(edits)
    if out.count('shape:"staff"') != 3:
        raise SystemExit("REFUSING TO WRITE -- expected exactly three staves in the roster")
    print(f"  ok    relic  staff, the bow's body, {'the glyph' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    three staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
