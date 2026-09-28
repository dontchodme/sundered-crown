#!/usr/bin/env python
"""CROZIER / RADIANCE -- the sanctified staff, the staff row's fifth. v95.

Built from `06-docs/v95/CROZIER-BUILD-BRIEF.md` and `sanctified-staff-design-v95.md`
(Cowork, 2026-09-27), the row's `06-docs/v89/STAFF-ROW-v89.md` §1/§6 -- the
input and the only input (CLAUDE.md §3 rule 0). Rick: "build them all".

    stage 1   the relic, its ultimate STUBBED          sc-watchlight-fx -> sc-crozier
    stage 2   the spell: LANCE (the pierce)            sc-crozier -> sc-lance
    stage 3   the ultimate: RADIANCE (the growth)      sc-lance -> sc-radiance
    stage 5   the blade, wide on 151: 14.5 -> 12.75      sc-radiance -> sc-radiance-blade
    stage 6   picture, voices                          sc-radiance-blade -> sc-crozier-fx

THE BASE is the staff branch's tip (Culverin, Briarwand, Cipher, Watchlight);
several anchors are those builds' own lines, so the staves carry together.

THE READINGS, where the build has to choose:
  1. THE PIERCE IS THE ENGINE'S (§5: "the blade-segment loop is skipped for a
     shot with `pierce` ... the ball test is unchanged and lands it at R + r").
     The lab FAKED it: it showed the engine a shot of r 1, armed so no engine
     test could reach it, and ran its own ball test at the true radius after
     the step. Two things follow and both are measured, not assumed: the lab's
     WALLS saw r 1, where the build's see the declared r (up to 70 on a grown
     shaft, which dies when its edge reaches stone); and the lab tagged a
     lance one step late (`fresh()`), so on its first step it was an ordinary,
     clankable arrow.
  2. THE GROWTH RUNS ON THE MATCH CLOCK (§5: `k = min(1, (t - born) / 0.4)`),
     as the lab's did on its harness clock: both run through a freeze. It is
     applied before the move and every test, and a lance in flight when the
     window shuts keeps growing (§5).
  3. THE WINDOW keeps its 8s on the engine's window clock (Cipher's
     measurement, v94 build §3); the charge is the lab's 16 in the game's
     clock, measured for this fighter.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC, BUILDER = "crozier", "crozier_build.py"
BLADE = 14.5                   # brief §2 stage 1: "stubbed relic at 14.5"; stage 5 settles it
# Stage 5, measured wide on 151 (both sides, 1520 fights a block, no bisection):
# 12.5 47.5% (three blocks), 12.75 50.3% (three blocks: 46.7 / 54.1 / 50.0),
# 13.0 54.3% (06-docs/v95/runs/build/stage5_*).
TUNED_BLADE = 12.75
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.34, speed=560, r=16, life=2.5, grav=0, dmgMul=1.0, pierce=True,
             spell="lance", tip="Needles of light no blade can parry")
CARD = "Every lance grows as it flies: the farther, the bigger and harder"
ULT_NAME, ULT_KIND = "Radiance", "radiance"
# Design §5, brief §0: over growT seconds of flight r 16 -> growR and the blow
# 1x -> growMul. `charge` is the lab's 16 in the game's clock, measured.
ULT = {"charge": 14, "dur": 8, "growT": 0.4, "growR": 70, "growMul": 3}
ULT_KEYS = list(ULT)
BLURB = ("A gilt crook with a bead of light in its curl. It throws needles no blade "
         "can turn, and for eight seconds each one grows into a shaft as it flies.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the sanctified
     BOW body at the staff's blade -- which stage 2's lance is measured
     against.
'''
ULT_STUB = f'''    /* RADIANCE. STUBBED AT `charge:1e9` IN STAGE 1. `kind:"{ULT_KIND}"` is its
       own; the card is Cowork's (design §6), in at stage 1. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''
S1_BLADE_PARA = f'''     `dmg` {fnum(BLADE)} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 14.3 on Chromium 141, and stage 5 settles it wide on 151. */'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* CROZIER -- THE SANCTIFIED STAFF, the staff row's fifth relic. Built from
     `06-docs/v95/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Sanctified smites;
     the sanctified bow body is the row's best (28.2% at this blade), and the
     cell's problem was an ultimate that is not already one of the school's
     five -- the first one priced was Benediction with a staff in it and was
     rejected for that (design §3).

{S1_SHOT_PARA}
{S1_BLADE_PARA}
  {{ id:"{RELIC}", name:"Crozier", aff:"sanctified", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ smite:1 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [("Crozier joins the roster, its ultimate stubbed",
             '''

];
/* The single source of truth for "which status does this relic teach".''',
             relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".''')]


S2_SHOT_PARA = '''     THE SPELL IS LANCE (design §1, §5): a needle of light every 0.34s along
     the facing -- the fastest shot in the game (560) and the thinnest (r 16)
     -- that NO BLADE CAN PARRY: `pierce`, and `tickShots` skips the
     blade-segment loop for it, so it passes the foe's weapon and lands only
     on the foe. A landing smites. A fast shot is a worse shot in this engine
     (7.6 lance blows a fight where the arrow lands 17, §3), and the lance
     is ten points under the bow at the same blade: the pierce is kept for
     the picture and for the one matchup it changes.
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Crozier looses the lance",
 f'''  {{ id:"{RELIC}", name:"Crozier", aff:"sanctified", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Crozier", aff:"sanctified", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("spawnShot: a lance carries its pierce from the barrel",
 '''      if (S.knock !== undefined) s.knock = S.knock;
''',
 '''      if (S.knock !== undefined) s.knock = S.knock;
      /* CROZIER'S LANCE (v95 §5): `spawnShot` copies `pierce`, AT SPAWN -- the
         lab tagged it one step late, so on its first step its lance was an
         ordinary arrow a blade could bat down. */
      if (S.pierce) s.pierce = true;
'''),

("tickShots: no blade can parry a pierce",
 '''      for (const q of segs){
''',
 '''      /* THE PIERCE (v95 §5): the one shot in the game no blade can parry --
         the blade-segment loop is skipped for it, and the ball test below is
         unchanged and lands it at R + r. */
      if (!s.pierce) for (const q of segs){
'''),

("the lance is drawn (first cut)",
 '''      /* WATCHLIGHT'S WARDBOLT ON SCREEN (v92 §6.1):''',
 '''      /* CROZIER'S LANCE -- FIRST CUT, for stage 2's film; the picture is stage
         6's. "A thin bright line (r 16, drawn as a 60-px streak)" (v95 §6.1);
         a grown one widens with the r it has grown to. Off the shot's own
         state; no rng. */
      if (s.spell === "lance"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        const len = 60 + (s.r - 16) * 1.2;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.lineCap = "round";
        c.globalAlpha = 0.45; c.strokeStyle = pal.core; c.lineWidth = Math.max(3, s.r * 0.9);
        c.beginPath(); c.moveTo(s.x - ux * len, s.y - uy * len); c.lineTo(s.x, s.y); c.stroke();
        c.globalAlpha = 0.9; c.strokeStyle = pal.glow; c.lineWidth = Math.max(1.5, s.r * 0.3);
        c.beginPath(); c.moveTo(s.x - ux * len * 0.8, s.y - uy * len * 0.8); c.lineTo(s.x, s.y); c.stroke();
        c.restore();
        continue;
      }
      /* WATCHLIGHT'S WARDBOLT ON SCREEN (v92 §6.1):'''),
    ]


ULT_NOTE = '''    /* RADIANCE (design §1, §5). For `dur` seconds every lance GROWS as it
       flies: over its first `growT` s (about 220 px) it swells from a needle
       (r 16) to a shaft (r `growR`) and its blow from 1x to `growMul` x. The
       farther it has come, the bigger and harder; up close it is still a
       needle. Range -- the type's own game -- paid for the first time (+34 over
       the spell, §3.1). Sanctum, a smiting and healing ring on the caster,
       priced +42 and was REJECTED as Benediction's: not built here.

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v95/crozier-build-v95.md`. */
'''


def s3_edits(U: dict):
    return [
("Radiance is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Radiance's window",
 '''    this.beaconAge = 0;
''',
 '''    this.beaconAge = 0;
    /* {t, dur} while RADIANCE's window is open (v95): a lance loosed inside
       it grows. null otherwise: `tickRadiance` returns after a two-iteration
       loop. `radianceTally` is the probe's; nothing in the sim reads it. */
    this.ultRadiance = null;
    this.radianceTally = null;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "beacon"){
''',
 '''    if (u.kind === "radiance"){
      /* RADIANCE (v95). NOTHING RESOLVES HERE: `spawnShot` gives a lance loosed
         while the window is open its growth, and `tickShots` grows it. `m.ultFx`
         is the cast flash only (open item 25). */
      f.ultRadiance = { t: 0, dur: u.dur };
      if (!f.radianceTally) f.radianceTally = { casts: 0, grown: 0 };
      f.radianceTally.casts++;
      return;
    }
    if (u.kind === "beacon"){
'''),

("spawnShot: a lance loosed in the window will grow",
 '''      if (S.pierce) s.pierce = true;
''',
 '''      if (S.pierce) s.pierce = true;
      /* RADIANCE (v95 §5): a lance loosed while the window is open carries its
         growth -- when it was born, on the match clock, and where the ramp runs
         from and to. `tickShots` grows it; the window does not have to be open
         for that, only for the loosing. */
      if (f.ultRadiance && S.pierce){
        const u = f.w.ult;
        s.grow = { born: this.t, T: u.growT, r0: s.r, r1: u.growR, m0: s.dmgMul, mul: u.growMul, k: 0 };
        f.radianceTally.grown++;
      }
'''),

("tickShots: the lance grows before it moves",
 '''        if (s.trail.length > 24) s.trail.splice(0, 2);
      }
      s.vy += s.grav * dt;
''',
 '''        if (s.trail.length > 24) s.trail.splice(0, 2);
      }
      /* RADIANCE'S GROWTH (v95 §5): k = min(1, (t - born) / T), r = r0 + (r1 -
         r0) k, dmgMul = m0 (1 + (mul - 1) k) -- before the move and every
         test, so the wall, the ball and the picture all see the size it has
         grown to. A shaft dies when its EDGE reaches stone (the lab's walls saw
         r 1: v95 build §3). On the match clock, as the lab's harness clock. */
      if (s.grow){
        const G = s.grow, k = Math.min(1, (this.t - G.born) / G.T);
        s.r = G.r0 + (G.r1 - G.r0) * k; s.dmgMul = G.m0 * (1 + (G.mul - 1) * k); G.k = k;
      }
      s.vy += s.grav * dt;
'''),

("the window ticks with the window tickers",
 '''    this.tickBeacon(dt);                // BEACON (v92): the lantern keeps the watch
''',
 '''    this.tickBeacon(dt);                // BEACON (v92): the lantern keeps the watch
    this.tickRadiance(dt);              // RADIANCE (v95): the lances grow
'''),

("tickRadiance: the window's clock",
 '''  /* ==================================================== BEACON ========''',
 '''  /* ================================================== RADIANCE ========
     v95 §5. The window is only a clock: while it runs a loosed lance is given
     its growth (`spawnShot`), and the growing is `tickShots`'s. THE CLOCK is
     the window tickers' and stops through a hit stop; the lab's counted every
     step. */
  tickRadiance(dt){
    for (const f of [this.a, this.b]){
      const W = f.ultRadiance;
      if (!W) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultRadiance = null; continue; }
      W.t += dt;
      if (W.t >= W.dur) f.ultRadiance = null;
    }
  }

  /* ==================================================== BEACON ========'''),

("a grown landing of 20 or more files as a crit, for the director",
 '''                dmg, crit, fatal, hpAfter: Math.max(0, foe.hp),
''',
 '''                /* A GROWN LANCE THAT LANDS FOR 20 OR MORE IS A CRIT TO THE
                   DIRECTOR (v95 brief §1), so the shaft is filmed. The beat
                   only; the blow is what it was. */
                dmg, crit: crit || !!(_cs && _cs.grow && dmg >= 20), fatal, hpAfter: Math.max(0, foe.hp),
'''),
    ]


# ---------------------------------------------------------------- stage 5 --
S5_BLADE_PARA = f'''     `dmg` {fnum(TUNED_BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of every
     pairing, 1520 fights a seed block, no bisection -- 12.5 reads 47.5% and
     12.75 50.3% over three blocks (46.7 / 54.1 / 50.0: the third settled a
     swing larger than the step), 13.0 54.3%. 1.75 UNDER THE DESIGN'S 14.5,
     AND THE LAB IS WHY: it faked the pierce with an armed r-1 shot tagged one
     step late, so a lance loosed point-blank into a blade was an ordinary
     arrow and was batted down. The build's is the engine's from the barrel
     (§5), and the lab emulated on the build reproduces arm S exactly (18.5%)
     where the build reads 24.4%. Provisional until the row re-prices (v89
     §8.2). The number lives in `crozier_build.TUNED_BLADE`. */'''


def s5_edits():
    b = BODY
    return [
("the relic's note says the blade is measured", S1_BLADE_PARA, S5_BLADE_PARA),
("Crozier's blade is the measured one",
 f'''  {{ id:"{RELIC}", name:"Crozier", aff:"sanctified", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:''',
 f'''  {{ id:"{RELIC}", name:"Crozier", aff:"sanctified", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(TUNED_BLADE)}, spin:'''),
    ]


# THE PICKED VOICES, from crozier_voice_lab.py (runs/build/stage6_voice_lab.json), verbatim.
VOICES = {
    'tick': '\n  S._burst(t, { freq: 5200, q: 3.0, gain: 0.03061, dur: 0.015, type:"bandpass" });\n  S._tone (t, { freq: 3136, gain: 0.01224, dur: 0.03, type:"sine" });',
    'pierce': '\n  S._burst(t, { freq: 5200, q: 3.0, gain: 0.01046, dur: 0.015, type:"bandpass" });\n  S._tone (t, { freq: 3136, gain: 0.004182, dur: 0.03, type:"sine" });\n  S._tone (t + 0.008, { freq: 2637, gain: 0.006148, dur: 0.22, type:"sine" });\n  S._tone (t + 0.008, { freq: 3951, gain: 0.003416, dur: 0.154, type:"sine" });',
    'cast': '\n  S._sweep(t + 0, { f0: 465.5, f1: 523, q: 24, gain: 0.4856, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0, { f0: 586.5, f1: 659, q: 24, gain: 0.3561, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0, { f0: 697.8, f1: 784, q: 24, gain: 0.2914, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.12, { f0: 465.5, f1: 523, q: 24, gain: 1.214, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.12, { f0: 586.5, f1: 659, q: 24, gain: 0.8902, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.12, { f0: 697.8, f1: 784, q: 24, gain: 0.7284, dur: 0.46, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.1, { f0: 900, f1: 2600, q: 0.8, gain: 0.1214, dur: 0.46, atk: 0.27, type:"bandpass" });',
    'bloom': '\n  const k = Math.max(0, Math.min(1, p.k === undefined ? 1 : p.k));\n  S._sweep(t, { f0: 500, f1: 180, q: 0.9, gain: 0.133 * k, dur: 0.18, atk: 0.03, type:"lowpass" });\n  S._tone (t, { freq: 130, to: 75, gain: 0.0798 * k, dur: 0.15, type:"sine" });',
    'close': '\n  S._tone (t, { freq: 523, to: 465.5, gain: 0.04062, dur: 0.42, type:"sine" });\n  S._tone (t, { freq: 659, to: 586.5, gain: 0.02843, dur: 0.42, type:"sine" });\n  S._tone (t, { freq: 784, to: 697.8, gain: 0.02275, dur: 0.42, type:"sine" });',
}
VOICE_PICKS = {'tick': 'NEEDLE', 'pierce': 'RING', 'cast': 'CHOIR', 'bloom': 'WARM', 'close': 'FALL'}


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule". PRESENTATION ONLY: SFX.play (a no-op headless),
# this.ring (a presentation list), render-only fields, drawing code -- no rng,
# no spawnFx. engine_ab over all 39, Crozier included, is the proof. The voices
# are `crozier_voice_lab.py`'s picks (four rounds), pasted verbatim; each arm
# opens `const S = this;`.
#
# THE SHAFT'S BLOOM GATES (design §6.1, §4.1b/c) are asserted on the text by
# `main`: no layer over alpha 0.55, the bloom no wider than 1.3 r, and never
# white at the centre -- sanctified's own `glow` IS #FFFFFF and its `core` a
# near-white cream, so the shaft is drawn in the crook's GILT under
# `source-over`, where layers blend and cannot add up to white.


def arm(key: str, indent: str) -> str:
    body = VOICES[key].strip("\n")
    lines = [indent + "const S = this;"] + [indent + (l[2:] if l.startswith("  ") else l) for l in body.splitlines()]
    return "\n".join(lines)


SHAFT_START = "        if (k > 0){"
SHAFT_END = "        } else {"


def s6_edits():
    s2 = {l: n for l, o, n in s2_edits(fnum(BLADE))}
    lance_cut = s2["the lance is drawn (first cut)"]
    lance_cut = lance_cut[:lance_cut.index("      /* WATCHLIGHT'S WARDBOLT ON SCREEN (v92 §6.1):")]
    s2g = s2["tickShots: no blade can parry a pierce"]
    return [

("the lance's release is its own: a needle's tick",
 '''          this._tone (t, { freq: 118, to: 58, gain: 0.08046, dur: 0.12, type:"triangle" });
        } else {
''',
 '''          this._tone (t, { freq: 118, to: 58, gain: 0.08046, dur: 0.12, type:"triangle" });
        } else if (p.spell === "lance"){
          /* CROZIER'S LANCE LEAVING -- design §6.2: "a very short bright tick
             (the needle), pitched high". NEEDLE, of three (`crozier_voice_lab.py`,
             four rounds, Rick's "you pick i overrule"): a bandpassed 5.2 kHz
             tick and a 3.1 kHz sine, 30 ms, at the generic release's level --
             a shot leaving sits under the shots landing (the comment above).
             Round 1 took a 12.5 kHz click, a hiss with no pitch at all. */
''' + arm("tick", "          ") + '''
        } else {
'''),

("Sfx: Radiance's cast, the pierce, the bloom and the close",
 '''        } else if (w === "watchlight"){                 // a lamp set down
''',
 '''        } else if (w === "crozier"){                    // the choir rises
          /* RADIANCE'S CAST -- design §6.2: "a rising choir swell, 0.4s (the
             school's register: Zenith, Daybreak)". CHOIR: a C-major chord of
             narrow noise bands swelling up into pitch -- two swells, the first
             at 0.4 -- and a breath rising under it, 6 dB under a lance's blow,
             loudest 200 ms into 300. Crozier fell through to the rune-crack. */
''' + arm("cast", "          ") + '''
        } else if (w === "crozier-pierce"){             // a lance goes through a blade
          /* "On a pierce the same tick with a glassy after-ring": the needle's
             tick and two high sines ringing a fifth of a second, 3 dB over the
             release. Played the step a lance enters a foe blade's reach. */
''' + arm("pierce", "          ") + '''
        } else if (w === "crozier-bloom"){              // a grown lance lands
          /* "The hit voice with a low bloom under it that scales with k": WARM,
             a lowpass sweep 500 -> 180 Hz and a sine under it, 8 dB under the
             hit at k = 1 and 12.9 dB quieter at k = 0.2 -- the one of three
             loudest on a phone. `p.k` is the lance's growth. */
''' + arm("bloom", "          ") + '''
        } else if (w === "crozier-close"){              // the swell reversed
          /* CLOSE -- "the swell reversed": the cast rose INTO its chord; this
             starts on it and falls away, each partial gliding down by the
             ratio the cast rose by. Played by `tickRadiance` when the window
             runs out by its clock, never on a death. */
''' + arm("close", "          ") + '''
        } else if (w === "watchlight"){                 // a lamp set down
'''),

("a lance through a blade is shown and heard",
 s2g,
 '''      /* THE PIERCE (v95 §5): the one shot in the game no blade can parry --
         the blade-segment loop is skipped for it, and the ball test below is
         unchanged and lands it at R + r.

         ...AND IT IS SHOWN GOING THROUGH (§6.1: "passes THROUGH a blade with a
         small white flick where it crossed") and HEARD (§6.2: "the same tick
         with a glassy after-ring") -- once each time it enters a blade's
         reach. The parry's own test, and nothing but a ring and a voice come
         of it: `through` is the lance's, and nothing in the simulation reads
         it. */
      if (s.pierce){
        let near = false;
        for (const q of segs)
          if (segDist(q.ax, q.ay, q.bx, q.by, s.x, s.y).d < s.r + foe.w.width * 0.5 + CONFIG.shot.pad){ near = true; break; }
        if (near && !s.through){ this.ring(s.x, s.y, "#FFFFFF", 2, 18, 0.14, 2); SFX.play("ult", { w: "crozier-pierce" }); }
        s.through = near;
      }
      if (!s.pierce) for (const q of segs){
'''),

("a lance's landing flares to its size, and a grown one blooms",
 '''        if (s.spell === "wardbolt" && s.knock >= 400) SFX.play("ult", { w: "watchlight-thump" });
''',
 '''        if (s.spell === "wardbolt" && s.knock >= 400) SFX.play("ult", { w: "watchlight-thump" });
        /* CROZIER'S LANCE LANDS (v95 §6.1-6.2): "a flare sized to the shaft",
           and under the hit voice "a low bloom that scales with k" for a grown
           one. The smite tag is the hit's own. */
        if (s.spell === "lance"){
          this.ring(foe.x, foe.y, s.aff.core, s.r * 0.4, s.r * 1.3, 0.28, 3);
          if (s.grow) SFX.play("ult", { w: "crozier-bloom", k: s.grow.k });
        }
'''),

("the window running out by its clock is heard, and the picture keeps its clock",
 '''      if (W.t >= W.dur) f.ultRadiance = null;
    }
  }
''',
 '''      if (W.t >= W.dur){ SFX.play("ult", { w: "crozier-close" }); f.ultRadiance = null; }
    }
    /* THE PICTURE'S CLOCK: 1 while the window runs, down over 0.4s after it
       ("the bead dims"), and the window's age for the cast's flare. On the
       fighter; read by `drawRadiance` alone. */
    for (const f of [this.a, this.b]){
      const W = f.ultRadiance;
      if (W){ f.radianceFade = 1; f.radianceAge = W.t; }
      else f.radianceFade = Math.max(0, f.radianceFade - dt / 0.4);
    }
  }
'''),

("the fighter carries the bead's light",
 '''    this.radianceTally = null;
''',
 '''    this.radianceTally = null;
    /* THE BEAD'S LIGHT (v95 §6.1): its fade and its window's age. Render-only. */
    this.radianceFade = 0;
    this.radianceAge = 0;
'''),

("the staff's sanctified head: Code's pick, and why",
 '''lamp down to the floor. B and C stay until Rick has seen it. */
''',
 '''lamp down to the floor. B and C stay until Rick has seen it. */
/* THE SANCTIFIED HEAD IS "A" -- Code's pick for Crozier, the same ruling: the
   CROOK, the pole curled over with a bead of light in the curl, because design
   §6.1 asks for "a gilt rod with a crook at the head (the crozier's curl), a
   sanctified core bead in the curl" -- which is A to the word. B and C stay
   until Rick has seen it. */
'''),

("the lance: a needle, and a shaft that grows under the bloom gates",
 lance_cut,
 '''      /* CROZIER'S LANCE ON SCREEN (v95 §6.1). "A thin bright line (r 16,
         drawn as a 60-px streak) ... A grown lance: the streak widens as it
         flies -- by 220 px it is a shaft of light r 70 with a soft bloom
         (§4.1b/c's gates: peak alpha 0.55, bloom radius <= 1.3x r, never
         white at centre)." THE SHAFT IS ITS HIT RADIUS: the body is drawn at
         the r the ball test uses, so a shaft that looks like it connected
         did. It is the crook's GILT under `source-over`, because sanctified's
         glow is #FFFFFF and layers under `lighter` add toward it. Motes stream
         off a grown lance (the field), off its own age; no rng. */
      if (s.spell === "lance"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        const k = s.grow ? s.grow.k : 0, len = 60 + 160 * k;
        const tx = s.x - ux * len, ty = s.y - uy * len;
        c.save();
        c.lineCap = "round";
        if (k > 0){
          const gilt = SHAPES._shade(pal.dark, 2.0, 0.1);
          c.globalCompositeOperation = "source-over";
          c.strokeStyle = gilt;
          c.globalAlpha = 0.14; c.lineWidth = 2 * s.r * 1.3;
          c.beginPath(); c.moveTo(tx, ty); c.lineTo(s.x, s.y); c.stroke();
          c.globalAlpha = 0.30; c.lineWidth = 2 * s.r;
          c.beginPath(); c.moveTo(tx, ty); c.lineTo(s.x, s.y); c.stroke();
          c.globalAlpha = 0.55; c.strokeStyle = pal.core; c.lineWidth = Math.max(2, s.r * 0.35);
          c.beginPath(); c.moveTo(s.x - ux * len * 0.85, s.y - uy * len * 0.85); c.lineTo(s.x, s.y); c.stroke();
          c.fillStyle = gilt;
          for (let i = 0; i < 6; i++){
            const ph = ((s.max - s.life) * 2.2 + i / 6) % 1;
            const off = (i % 2 ? 1 : -1) * s.r * (0.3 + 0.5 * ph);
            c.globalAlpha = 0.45 * (1 - ph);
            c.beginPath(); c.arc(tx + ux * len * (1 - ph) - uy * off, ty + uy * len * (1 - ph) + ux * off, 2.2, 0, TAU); c.fill();
          }
        } else {
          c.globalCompositeOperation = "lighter";
          c.globalAlpha = 0.45; c.strokeStyle = pal.core; c.lineWidth = 5;
          c.beginPath(); c.moveTo(tx, ty); c.lineTo(s.x, s.y); c.stroke();
          c.globalAlpha = 0.95; c.strokeStyle = pal.glow; c.lineWidth = 2;
          c.beginPath(); c.moveTo(s.x - ux * len * 0.8, s.y - uy * len * 0.8); c.lineTo(s.x, s.y); c.stroke();
        }
        c.restore();
        continue;
      }
'''),

("drawRadiance: the halo on the crook and the bead's flare",
 '''  /* BEACON ON SCREEN (v92 §6.1).''',
 '''  /* RADIANCE ON SCREEN (v95 §6.1): "Cast: the bead flares; a thin halo ring
     on the staff head ... Close: the bead dims; shafts in flight finish."
     Off the fighter's own `radianceFade`.

     THE BEAD is sanctified head "A"'s own (STAFF.sanctified): the curl's
     centre at 0.70 of the drawn staff (1.7x the sim's L, from R - 6) and
     0.053 of the drawn width (1.3x artW) further on. The halo is a thin ring
     about it; the flare is the window's first 0.3s. No rng. */
  drawRadiance(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const k = f.radianceFade;
      if (!(k > 0.01) || !f.alive) continue;
      const pal = f.aff, reach = f.w.reach * m.actMods.reach * f.reachMul;
      const Lq = (reach + 6) * 1.7, Wq = f.w.artW * 1.3;
      const hd = R - 6 + Lq * 0.70 + Wq * 0.053;
      const bx = f.x + Math.cos(f.theta) * hd, by = f.y + Math.sin(f.theta) * hd;
      const fl = f.ultRadiance && f.radianceAge < 0.3 ? 1 - f.radianceAge / 0.3 : 0;
      const gilt = SHAPES._shade(pal.dark, 2.0, 0.1);
      c.save();
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = 0.75 * k; c.strokeStyle = gilt; c.lineWidth = 2;
      c.beginPath(); c.arc(bx, by, Wq * 0.24, 0, TAU); c.stroke();
      c.globalAlpha = 0.5 * k; c.strokeStyle = pal.core; c.lineWidth = 1;
      c.beginPath(); c.arc(bx, by, Wq * 0.24, 0, TAU); c.stroke();
      if (fl > 0){
        c.globalAlpha = 0.45 * fl; c.fillStyle = gilt;
        c.beginPath(); c.arc(bx, by, Wq * (0.2 + 0.25 * fl), 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  /* BEACON ON SCREEN (v92 §6.1).'''),

("drawRadiance is drawn with the shots",
 '''    this.drawBeacon(m);          // BEACON's lantern (v92 §6.1)
''',
 '''    this.drawBeacon(m);          // BEACON's lantern (v92 §6.1)
    this.drawRadiance(m);        // RADIANCE's halo and bead (v95 §6.1)
'''),
    ]


def shaft_gates(code: str) -> None:
    """§4.1b/c's gates, on the shaft's own drawing: no layer over alpha 0.55,
    the bloom no wider than 1.3 r, and no white in it."""
    i = code.index("CROZIER'S LANCE ON SCREEN")
    blk = code[code.index(SHAFT_START, i):code.index(SHAFT_END, i)]
    alphas = [float(x) for x in re.findall(r"globalAlpha = ([\d.]+)", blk)]
    widths = [float(x) for x in re.findall(r"lineWidth = 2 \* s\.r \* ([\d.]+)", blk)]
    if not alphas or max(alphas) > 0.55:
        raise SystemExit(f"REFUSING TO WRITE -- a shaft layer over alpha 0.55: {alphas}")
    if widths and max(widths) > 1.3:
        raise SystemExit(f"REFUSING TO WRITE -- the shaft's bloom is wider than 1.3 r: {widths}")
    if "#FFF" in blk.upper() or "pal.glow" in blk or '"lighter"' in blk:
        raise SystemExit("REFUSING TO WRITE -- the shaft reaches for white (or `lighter`)")
    print(f"  ok    shaft  peak alpha {max(alphas)}, bloom {max(widths) if widths else 1.0} r, no white, source-over")


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        if "radianceFade" in code:
            return 6
        return 5 if f"dmg:{fnum(TUNED_BLADE)}," in ent else 3
    return 2 if "pierce:" in re.search(r"shot:\{([^}]*)\}", ent).group(1) else 1


def all_stages():
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("5", s5_edits()), ("6", s6_edits())]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"])
    ap.add_argument("--src"); ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nCROZIER / RADIANCE -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8"); s = s0
    print(f"\nCROZIER / RADIANCE -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"watchlight"' not in code or "beaconFade" not in code:
        raise SystemExit("wrong base: no Watchlight stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin, Briarwand, Cipher and Watchlight in it")
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
        edits = s6_edits()
    for label, old, new in edits:
        s = one(s, old, new, label)
    out = strip_comments(s)
    shot = SPELL if stage >= 2 else BOW_SHOT
    ent = check_entry(out, RELIC, shot, TUNED_BLADE if stage >= 5 else BLADE, stubbed=(stage <= 2))
    if "onHit:{ smite:1 }" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {RELIC} does not smite 1 on hit")
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 2:
        for need in ("if (S.pierce) s.pierce = true;", "if (!s.pierce) for (const q of segs){"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickRadiance(dt){", "this.tickRadiance(dt);", 'u.kind === "radiance"', "if (s.grow){"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    if stage >= 6:
        shaft_gates(s)
    check_no_rng(edits)
    if out.count('shape:"staff"') != 5:
        raise SystemExit("REFUSING TO WRITE -- expected exactly five staves in the roster")
    print(f"  ok    relic  staff, the bow's body, smite 1, {'the lance' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    five staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
