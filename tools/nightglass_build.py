#!/usr/bin/env python
"""NIGHTGLASS / BACKLASH -- the umbral staff, the staff row's seventh and last. v91.

Built from `06-docs/v91/NIGHTGLASS-BUILD-BRIEF.md` and `umbral-staff-design-v91.md`
(Cowork, 2026-09-27), the row's `06-docs/v89/STAFF-ROW-v89.md` §1/§6 -- the
input and the only input (CLAUDE.md §3 rule 0). Rick: "build them all".

    stage 1   the relic, its ultimate STUBBED          sc-bloodwick-fx -> sc-nightglass
    stage 2   the spell: SHADEBOLT (the ricochet)      sc-nightglass -> sc-shadebolt
    stage 3   the ultimate: BACKLASH (the shroud)      sc-shadebolt -> sc-backlash
    stage 5   the blade, wide on 151: 7.3 -> 6.25        sc-backlash -> sc-backlash-blade
    stage 6   the picture and the voices               sc-backlash-blade -> sc-nightglass-fx

THE BASE is the staff branch's tip (Culverin, Briarwand, Cipher, Watchlight,
Crozier, Bloodwick); several anchors are those builds' own lines.

THE READINGS, where the build has to choose:
  1. THE BOUNCE IS COPIED AT SPAWN (§5: "`spawnShot` copies `bounce`"). The lab
     set it from `fresh()`, one step late -- every staff lab's artifact -- so a
     bolt loosed into a wall died there. Measured at stage 2.
  2. THE HOOK IS `hurt()` (§5, brief §1), and what is thrown back is what
     LANDED -- the drop in hp + ward around the debit, the lab's own quantity.
     Every blow `resolveHit` lands comes through `hurt()`. The status ticks do
     not (`tickStatus` debits hp directly), and a tick is a fraction of a point
     a step, so round(tick * 0.5) is 0 -- the lab's per-frame watch rounded
     them away the same way unless a blow landed on the same frame.
  3. A REFLECTED BLOW NEVER REFLECTS AGAIN, by a flag held while it resolves.
     §5's intent in its own words; its named guard (`src.ultShroud`) would ALSO
     stop ordinary blows being reflected whenever both fighters are shrouded,
     which the design does not ask for. (Only a mirror match can tell them
     apart, and neither `verify` nor any sweep plays one.)
  4. NO REFLECTION ONCE EITHER IS DOWN -- the lab's `foe.alive && me.alive`.
  5. THE WINDOW keeps its 8s on the engine's window clock (Cipher's
     measurement, v94 build §3); the charge is the lab's 16 in the game's
     clock, measured for this fighter.
  6. THE FLASH IS "AT THE POINT OF CONTACT" (§6.1), so stage 6 has `resolveHit`
     hand `hurt()` its `hx, hy` -- two trailing arguments nothing but the
     picture reads; from every other caller the flash faces the source.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC, BUILDER = "nightglass", "nightglass_build.py"
BLADE = 7.3                    # brief §2 stage 1: "stubbed relic at 7.3"; stage 5 settles it
# Stage 5, measured wide on 151 (both sides, two seed blocks, 1600 fights a
# row, no bisection): 6.0 46.2%, 6.25 48.1%, 6.375 52.7%, 6.5 55.9%
# (06-docs/v91/runs/build/stage5_*).
TUNED_BLADE = 6.25
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.34, speed=380, r=22, life=4.0, grav=0, dmgMul=1.0, bounce=2,
             spell="shadebolt", tip="Bolts ricochet off two walls · clankable")
CARD = "Shrouded: half of every blow it takes is thrown back, and it curses"
ULT_NAME, ULT_KIND = "Backlash", "backlash"
# Design §5, brief §0. `charge` is the lab's 16 in the game's clock, measured.
ULT = {"charge": 14, "dur": 8, "refl": 0.5}
ULT_KEYS = list(ULT)
BLURB = ("A black rod headed with obsidian glass. Its bolts come back off the walls, "
         "and for eight seconds whatever strikes it is struck in turn.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the umbral BOW
     body at the staff's blade -- which stage 2's shadebolt is measured
     against.
'''
ULT_STUB = f'''    /* BACKLASH. STUBBED AT `charge:1e9` IN STAGE 1. `kind:"{ULT_KIND}"` is its
       own; the card is Cowork's (design §6), in at stage 1. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''
S1_BLADE_PARA = f'''     `dmg` {fnum(BLADE)} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 7.6 on Chromium 141, and stage 5 settles it wide on 151. */'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* NIGHTGLASS -- THE UMBRAL STAFF, the staff row's seventh relic. Built from
     `06-docs/v91/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Umbral curses and
     remembers; the umbral bow body is the row's weakest (0.3% at this
     blade), and the misses coming back is the school's oldest sentence (v61).

{S1_SHOT_PARA}
{S1_BLADE_PARA}
  {{ id:"{RELIC}", name:"Nightglass", aff:"umbral", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ curse:1 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [("Nightglass joins the roster, its ultimate stubbed",
             '''

];
/* The single source of truth for "which status does this relic teach".''',
             relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".''')]


S2_SHOT_PARA = '''     THE SPELL IS SHADEBOLT (design §1, §5): a bolt of shadow every 0.34s
     along the facing at an arrow's speed that does not die on the wall -- it
     RICOCHETS, twice (`bounce` 2: the wall branch of `tickShots` already
     bounces a shot with bounce left, 0.88 a wall), and every landing curses.
     Two more shots for the price of one (§3): the bolt lands ~36 blows a
     fight where the arrow lands 18, so this is the lowest blade in the game.
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Nightglass looses the shadebolt",
 f'''  {{ id:"{RELIC}", name:"Nightglass", aff:"umbral", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Nightglass", aff:"umbral", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("spawnShot: a shadebolt carries its bounces from the barrel",
 '''        SFX.play("ult", { w: "bloodwick-slot" });   // "a soft tick as each drop takes its slot" (§6.2)
      }
''',
 '''        SFX.play("ult", { w: "bloodwick-slot" });   // "a soft tick as each drop takes its slot" (§6.2)
      }
      /* NIGHTGLASS'S SHADEBOLT (v91 §5): `spawnShot` copies `bounce`, AT SPAWN --
         the lab set it one step late, so a bolt loosed into a wall died there.
         The wall branch of `tickShots` does the rest. */
      if (S.bounce !== undefined) s.bounce = S.bounce;
'''),

("the shadebolt is drawn (first cut)",
 '''      /* BLOODWICK'S GLOBULE ON SCREEN (v90 §6.1):''',
 '''      /* NIGHTGLASS'S SHADEBOLT -- FIRST CUT, for stage 2's film; the picture is
         stage 6's. "A dark bolt with a short violet trail" (v91 §6.1); the
         wall's own splash and `snap` are the engine's. Off the shot's own
         state; no rng. */
      if (s.spell === "shadebolt"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        c.save();
        c.lineCap = "round";
        c.globalAlpha = 0.6; c.strokeStyle = pal.core; c.lineWidth = s.r * 0.6;
        c.beginPath(); c.moveTo(s.x - ux * s.r * 2.2, s.y - uy * s.r * 2.2); c.lineTo(s.x, s.y); c.stroke();
        c.globalAlpha = 1; c.fillStyle = pal.dark;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.fill();
        c.strokeStyle = pal.glow; c.lineWidth = 2;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.stroke();
        c.restore();
        continue;
      }
      /* BLOODWICK'S GLOBULE ON SCREEN (v90 §6.1):'''),
    ]


ULT_NOTE = '''    /* BACKLASH (design §1, §5). For `dur` seconds the caster is shrouded:
       every blow it takes is thrown straight back -- `refl` of what landed,
       at once, as a blow of its own through `hurt()` -- and the reflected blow
       curses the foe with its own memory. Umbral's mechanic (it remembers
       blows and pays them back) turned onto the blows the caster TAKES; at
       refl 1.0 the relic was untouchable (98%) and 0.5 was kept (§3).

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v91/nightglass-build-v91.md`. */
'''


def s3_edits(U: dict):
    return [
("Backlash is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Backlash's shroud",
 '''    this.gyreAge = 0;
''',
 '''    this.gyreAge = 0;
    /* {t, dur} while BACKLASH's shroud is up (v91). null otherwise:
       `tickShroud` returns after a two-iteration loop, and `hurt()` reads it.
       `shroudTally` is the probe's; nothing in the sim reads it. */
    this.ultShroud = null;
    this.shroudTally = null;
'''),

("the cast raises the shroud and resolves nothing",
 '''    if (u.kind === "gyre"){
''',
 '''    if (u.kind === "backlash"){
      /* BACKLASH (v91). NOTHING RESOLVES HERE: the shroud answers in `hurt()`.
         `m.ultFx` is the cast flash only (open item 25). */
      f.ultShroud = { t: 0, dur: u.dur };
      if (!f.shroudTally) f.shroudTally = { casts: 0, taken: 0, back: 0, count: 0 };
      f.shroudTally.casts++;
      return;
    }
    if (u.kind === "gyre"){
'''),

("hurt(): what lands on a shrouded fighter is read around the debit",
 '''  hurt(foe, dmg, src){
    if (foe.shield > 0 && dmg > 0){
''',
 '''  hurt(foe, dmg, src){
    /* BACKLASH (v91 §5): what LANDS on a shrouded fighter -- hp and ward -- is
       read around the debit below. 0 and unread for everyone else. */
    const pool0 = foe.ultShroud ? foe.hp + foe.shield : 0;
    if (foe.shield > 0 && dmg > 0){
'''),

("hurt(): the shroud throws half of it back",
 '''    if (dmg > 0) foe.hp -= dmg;
  }
''',
 '''    if (dmg > 0) foe.hp -= dmg;
    /* BACKLASH'S HOOK (v91 §5): "the hook is in `hurt()` -- the one function
       every source of damage goes through -- after the pool and the hp are
       debited". A blow from anybody else that lands on a shrouded fighter is
       thrown back by `shroudBack`; a reflected blow never reflects again
       (`_reflecting`, held while one resolves). */
    if (foe.ultShroud && src && src !== foe && !this._reflecting)
      this.shroudBack(foe, pool0 - (foe.hp + foe.shield));
  }
'''),

("the shroud ticks with the window tickers",
 '''    this.gyrePicture(dt);               // ...and the lane's and the flame's light
''',
 '''    this.gyrePicture(dt);               // ...and the lane's and the flame's light
    this.tickShroud(dt);                // BACKLASH (v91): the shroud
'''),

("tickShroud and shroudBack: the window, and the blow thrown back",
 '''  /* ====================================================== GYRE ========''',
 '''  /* ================================================== BACKLASH ========
     v91 §5, and the lab (`overlays/staff_umbral.js`) where the prose is
     silent. The window is a clock; the answer is `shroudBack`, called from
     `hurt()`. THE CLOCK is the window tickers' and stops through a hit stop;
     the lab's counted every step. */
  tickShroud(dt){
    for (const f of [this.a, this.b]){
      const W = f.ultShroud;
      if (!W) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultShroud = null; continue; }
      W.t += dt;
      if (W.t >= W.dur) f.ultShroud = null;
    }
  }

  /* THE BLOW THROWN BACK (v91 §5): back = round(taken * refl), dealt to the
     foe through `hurt()` with the caster as its source (so the foe's own ward
     takes it first), then `pushCurse(back, 1)` and `apply("curse", 1)` --
     the memory before the clock, exactly as `resolveHit` does an onHit curse.
     Only while both stand (the lab's `foe.alive && me.alive`). THE DIRECTOR
     CANNOT SEE `hurt()` (rule 3), so a reflected blow of 4 or more files a
     `hit` beat at the foe, `ranged:false`, and a fatal one always does. */
  shroudBack(f, taken){
    const opp = f === this.a ? this.b : this.a, T = f.shroudTally;
    const back = Math.round(taken * f.w.ult.refl);
    T.taken += taken;
    if (!(back > 0) || !f.alive || !opp.alive) return;
    this._reflecting = true;
    this.hurt(opp, back, f);
    this._reflecting = false;
    opp.pushCurse(back, 1);
    opp.apply("curse", 1, f === this.a ? "a" : "b");
    T.back += back; T.count++;
    const fatal = opp.hp <= 0;
    if (back >= 4 || fatal)
      this.beat({ kind: "hit", side: f === this.a ? 0 : 1, x: opp.x, y: opp.y,
                  dmg: back, crit: false, fatal, hpAfter: Math.max(0, opp.hp),
                  hpFrac: Math.max(0, opp.hp) / opp.maxHp, maxHp: opp.maxHp,
                  selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: opp.speed,
                  close: Math.hypot(f.vx - opp.vx, f.vy - opp.vy), ranged: false });
  }

  /* ====================================================== GYRE ========'''),

("the shroud is drawn (first cut)",
 '''    this.drawGyre(m);            // GYRE's lane, flame and motes (v90 §6.1)
''',
 '''    this.drawGyre(m);            // GYRE's lane, flame and motes (v90 §6.1)
    /* BACKLASH's shroud -- FIRST CUT, for stage 3's film: "a soft dark disc
       r 48 with a violet rim (alpha 0.5) that breathes" (v91 §6.1). */
    for (const f of [m.a, m.b]){
      if (!f.ultShroud || !f.alive) continue;
      const c = this.ctx, br = 0.85 + 0.15 * Math.sin(f.ultShroud.t * 5);
      c.save();
      c.globalAlpha = 0.35; c.fillStyle = f.aff.dark;
      c.beginPath(); c.arc(f.x, f.y, 48 * br, 0, TAU); c.fill();
      c.globalAlpha = 0.5; c.strokeStyle = f.aff.core; c.lineWidth = 2.5;
      c.beginPath(); c.arc(f.x, f.y, 48 * br, 0, TAU); c.stroke();
      c.restore();
    }
'''),
    ]


# ---------------------------------------------------------------- stage 5 --
S5_BLADE_PARA = f'''     `dmg` {fnum(TUNED_BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of every
     pairing, two seed blocks, 1600 fights a row, no bisection -- 6.0 reads
     46.2%, 6.25 48.1% (48.0 / 48.2), 6.375 52.7%, 6.5 55.9%: a steep curve,
     and 6.25 the measured row nearer 50%. 1.05 UNDER THE DESIGN'S 7.3, THE
     ROW'S LARGEST CUT, AND THE LAB IS WHY: it gave a bolt its bounces one
     step late, so a bolt loosed INTO a wall died there where it ricochets
     here -- with that put back the spell IS arm S (18.2%) where the build
     reads 34.7%. The lowest blade in the game. Provisional until the row
     re-prices (v89 §8.2). The number lives in `nightglass_build.TUNED_BLADE`. */'''


def s5_edits():
    b = BODY
    return [
("the relic's note says the blade is measured", S1_BLADE_PARA, S5_BLADE_PARA),
("Nightglass's blade is the measured one",
 f'''  {{ id:"{RELIC}", name:"Nightglass", aff:"umbral", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:''',
 f'''  {{ id:"{RELIC}", name:"Nightglass", aff:"umbral", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(TUNED_BLADE)}, spin:'''),
    ]


# THE PICKED VOICES, from nightglass_voice_lab.py (runs/build/stage6_voice_lab.json), verbatim.
VOICES = {
    'cast': '\n  S._sweep(t, { f0: 5000, f1: 9000, q: 0.7, gain: 0.05213, dur: 0.34, atk: 0.2, type:"highpass" });\n  S._tone (t + 0.26, { freq: 220, gain: 0.06256, dur: 0.42, type:"sine" });\n  S._tone (t + 0.26, { freq: 663, gain: 0.01877, dur: 0.28, type:"sine" });',
    'echo': '\n  const w = Math.max(0.12, Math.min(1, (p.dmg || 10) / 45)), e = t + 0.06;\n  S._burst(e, { freq: (2600 - 1500 * w) / 2, q: 1.1, gain: 0.1458, dur: 0.07 + 0.06 * w, type:"bandpass" });\n  S._tone (e, { freq: 190 - 90 * w, to: 60, gain: 0.1167, dur: 0.12 + 0.13 * w, type:"triangle" });',
    'close': '\n  S._sweep(t + 0, { f0: 220, f1: 220, q: 40, gain: 0.6593, dur: 0.45, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0, { f0: 663, f1: 663, q: 40, gain: 0.1979, dur: 0.45, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.12, { f0: 220, f1: 220, q: 40, gain: 1.648, dur: 0.45, atk: 0.27, type:"bandpass" });\n  S._sweep(t + 0.12, { f0: 663, f1: 663, q: 40, gain: 0.4946, dur: 0.45, atk: 0.27, type:"bandpass" });',
}
VOICE_PICKS = {'cast': 'REVCYM', 'echo': 'DARK', 'close': 'STAGGER'}


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule". PRESENTATION ONLY: SFX.play (a no-op headless),
# this.float / this.statusTag / a fighter's `flash` (read by the renderer
# alone), render-only fields, drawing code -- no rng, no spawnFx. engine_ab
# over all 41, Nightglass included, is the proof. The voices are
# `nightglass_voice_lab.py`'s picks (two rounds), pasted verbatim; each arm
# opens `const S = this;`.


def arm(key: str, indent: str) -> str:
    body = VOICES[key].strip("\n")
    lines = [indent + "const S = this;"] + [indent + (l[2:] if l.startswith("  ") else l) for l in body.splitlines()]
    return "\n".join(lines)


def s6_edits():
    s2 = {l: n for l, o, n in s2_edits(fnum(BLADE))}
    s3 = {l: n for l, o, n in s3_edits(dict(ULT))}
    bolt_cut = s2["the shadebolt is drawn (first cut)"]
    bolt_cut = bolt_cut[:bolt_cut.index("      /* BLOODWICK'S GLOBULE ON SCREEN (v90 §6.1):")]
    shroud_cut = s3["the shroud is drawn (first cut)"]
    shroud_cut = shroud_cut[shroud_cut.index("    /* BACKLASH's shroud -- FIRST CUT"):]
    return [

("Sfx: Backlash's cast, the echo and the close",
 '''        } else if (w === "bloodwick"){                  // the wick catches
''',
 '''        } else if (w === "nightglass"){                 // the glass goes dark
          /* BACKLASH'S CAST -- design §6.2: "a reversed cymbal into a low glass
             tone, 0.4s". REVCYM (`nightglass_voice_lab.py`, two rounds, Rick's
             "you pick i overrule"): a highpassed hiss swelling for a third of
             a second into a sine glass tone at 220 Hz and its twelfth, 6 dB
             under a blow thrown back, audible 430 ms, the loudest of three on
             a phone. Nightglass fell through to the rune-crack. */
''' + arm("cast", "          ") + '''
        } else if (w === "nightglass-echo"){            // the blow comes back
          /* THE ECHO -- "the game's own hit voice, then 60ms later a dark echo
             of it (the same voice, an octave down, filtered) -- the reflection
             IS the echo". DARK: the hit voice's own burst an octave down and
             its falling tone as a triangle, 60 ms late, weighted by the blow
             thrown back (`p.dmg`), 6 dB under it. (The tone keeps its pitch:
             an octave down puts it at 23-50 Hz, where no phone carries it.) */
''' + arm("echo", "          ") + '''
        } else if (w === "nightglass-close"){           // the glass tone fades
          /* CLOSE -- "the glass tone fading up and out": the cast's own glass
             tone, its two partials as narrow bands of noise that swell and cut
             off, struck twice 0.12s apart (a held note does not exist in this
             toolkit, §4.5, and one swell from silence is heard for only its
             last fifth of a second), 10 dB under a blow, audible 275 ms.
             Played by `tickShroud` when the window runs out by its clock,
             never on a death. */
''' + arm("close", "          ") + '''
        } else if (w === "bloodwick"){                  // the wick catches
'''),

("resolveHit hands hurt() the point of contact",
 '''    this.hurt(foe, dmg, self);
    foe.flash = 1;
    foe.ringFlash = 1;
    self.hits++; self.dealt += dmg;''',
 '''    this.hurt(foe, dmg, self, hx, hy);   // the point is for BACKLASH's picture alone (v91 §6.1)
    foe.flash = 1;
    foe.ringFlash = 1;
    self.hits++; self.dealt += dmg;'''),

("hurt() takes the point of contact, for the picture",
 '''  hurt(foe, dmg, src){
    /* BACKLASH (v91 §5): what LANDS on a shrouded fighter -- hp and ward -- is
       read around the debit below. 0 and unread for everyone else. */''',
 '''  hurt(foe, dmg, src, hx, hy){
    /* BACKLASH (v91 §5): what LANDS on a shrouded fighter -- hp and ward -- is
       read around the debit below. 0 and unread for everyone else. `hx, hy`
       is the point of contact, handed in by `resolveHit` alone and read by
       nothing but the shroud's flash (§6.1); undefined from every other
       caller, where the flash faces the source instead. */'''),

("the shroud is handed the point",
 '''      this.shroudBack(foe, pool0 - (foe.hp + foe.shield));''',
 '''      this.shroudBack(foe, pool0 - (foe.hp + foe.shield), src, hx, hy);'''),

("shroudBack: the blow thrown back is seen and heard",
 '''  shroudBack(f, taken){
    const opp = f === this.a ? this.b : this.a, T = f.shroudTally;''',
 '''  shroudBack(f, taken, src, hx, hy){
    const opp = f === this.a ? this.b : this.a, T = f.shroudTally;'''),

("the blow thrown back: the flash, the shard, the float, the tag, the echo",
 '''    T.back += back; T.count++;
    const fatal = opp.hp <= 0;''',
 '''    T.back += back; T.count++;
    /* THE BLOW THROWN BACK, SEEN AND HEARD (§6.1-6.2): "the shroud flashes
       at the point of contact and a dark shard (a bolt-shaped streak, 0.15s)
       leaps from the caster to the foe; the reflected damage floats in violet
       at the foe; the curse tag ticks" -- and the echo, 60 ms behind the hit
       voice. The flash and the shard are aged by `shroudPresent`; the float,
       the tag and the foe's flash are the engine's own, as Revenant's hand
       and Deadfall's mine use them. Read by the renderer alone; no rng. */
    const ax = hx === undefined ? src.x : hx, ay = hy === undefined ? src.y : hy;
    f.shroudFlash.push({ a: Math.atan2(ay - f.y, ax - f.x), t: 0, life: 0.5 });
    f.shroudShards.push({ t: 0, life: 0.3, n: back });
    opp.flash = 1; opp.ringFlash = 1;
    this.float(opp.x, opp.y - 40, back, AFFINITIES.umbral.glow, 30 + back * 0.6);
    const first = !this.taught.curse && !!STATUS.curse.tip;
    if (first) this.taught.curse = true;
    this.statusTag(opp.x, opp.y, "curse", first, Math.round(opp.curseSum()));
    SFX.play("ult", { w: "nightglass-echo", dmg: back });
    const fatal = opp.hp <= 0;'''),

("the window running out by its clock is heard",
 '''      if (W.t >= W.dur) f.ultShroud = null;''',
 '''      if (W.t >= W.dur){ SFX.play("ult", { w: "nightglass-close" }); f.ultShroud = null; }'''),

("the fighter carries the shroud's picture",
 '''    this.ultShroud = null;
    this.shroudTally = null;
''',
 '''    this.ultShroud = null;
    this.shroudTally = null;
    /* BACKLASH'S PICTURE (v91 §6.1): the shroud's fade and age, a flash where
       each blow landed on it, a shard for each blow thrown back. Render-only,
       kept by `shroudPresent`. */
    this.shroudFade = 0;
    this.shroudAge = 0;
    this.shroudFlash = [];
    this.shroudShards = [];
'''),

("the picture's clocks run on the presentation clock",
 '''    this.tickNovaFx(dt);
''',
 '''    this.tickNovaFx(dt);
    this.shroudPresent(dt);             // BACKLASH's shroud, flashes and shards (v91 §6.1)
'''),

("shroudPresent: the shroud's fade and lift, the flashes and the shards",
 '''  /* THE BLOW THROWN BACK (v91 §5): back = round(taken * refl), dealt to the''',
 '''  /* BACKLASH'S PICTURE CLOCKS (v91 §6.1). ON `tickPresentation` AND NOT WITH
     THE WINDOW, for two reasons this engine has already paid for: a blow
     thrown back always shares a frame with an impact, and a hit stop runs
     `decayImpactOnly`, so a flash or a shard on the normal path would freeze
     for exactly the frames the viewer is staring hardest at (v54); and the
     match can end inside the window, where `step()` returns from `over`
     before the window tickers, so a fade kept there would hold the shroud
     over the winner for the whole verdict. Here it lifts. `life` IS IN
     HALF-SECONDS (this clock runs at 2x): the shard's 0.3 is the design's
     0.15s and the lift's 0.8 its 0.4s. */
  shroudPresent(dt){
    for (const f of [this.a, this.b]){
      const W = f.ultShroud;
      if (W && f.alive && !this.over){ f.shroudFade = 1; f.shroudAge = W.t; }
      else f.shroudFade = Math.max(0, f.shroudFade - dt / 0.8);
      if (f.shroudFlash.length){
        for (const F of f.shroudFlash) F.t += dt;
        f.shroudFlash = f.shroudFlash.filter(F => F.t < F.life);
      }
      if (f.shroudShards.length){
        for (const S of f.shroudShards) S.t += dt;
        f.shroudShards = f.shroudShards.filter(S => S.t < S.life);
      }
    }
  }

  /* THE BLOW THROWN BACK (v91 §5): back = round(taken * refl), dealt to the'''),

("the umbral staff's head: Code's pick, and why",
 '''   flares exactly that flame. B and C stay until Rick has seen it. */
''',
 '''   flares exactly that flame. B and C stay until Rick has seen it. */
/* THE UMBRAL HEAD IS "A" -- Code's pick for Nightglass, the same ruling: the
   CLAW holding a black glass orb, because design §6.1 asks for "a black rod
   with an obsidian head, a dim violet core inside the glass" and "a staff
   whose head is a mirror", and BACKLASH turns exactly that glass black-bright.
   B and C stay until Rick has seen it. */
'''),

("the shadebolt: a dark dart with a violet trail",
 bolt_cut,
 '''      /* NIGHTGLASS'S SHADEBOLT ON SCREEN (v91 §6.1): "a dark bolt with a short
         violet trail; on each wall it snaps and leaves a small dark splash --
         the viewer sees it turn". The bolt is a dark dart along its own
         velocity with a pale violet edge (a dark body alone vanishes on this
         hall) and a violet core, the trail a tapering violet stroke. At a wall
         the engine's own splash (five motes, drawn off the match rng, so left
         exactly as it is), `snap` and the wall's voice make the turn. Off the
         shot's own state; no rng. */
      if (s.spell === "shadebolt"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        const r = s.r, nx = -uy, ny = ux;
        c.save();
        c.lineCap = "round";
        c.globalAlpha = 0.3; c.strokeStyle = pal.core; c.lineWidth = r * 0.75;
        c.beginPath(); c.moveTo(s.x - ux * r * 2.4, s.y - uy * r * 2.4); c.lineTo(s.x - ux * r * 0.4, s.y - uy * r * 0.4); c.stroke();
        c.globalAlpha = 0.7; c.lineWidth = r * 0.3;
        c.beginPath(); c.moveTo(s.x - ux * r * 1.7, s.y - uy * r * 1.7); c.lineTo(s.x, s.y); c.stroke();
        c.globalAlpha = 1; c.fillStyle = pal.dark; c.strokeStyle = pal.glow; c.lineWidth = 2;
        c.beginPath();
        c.moveTo(s.x + ux * r * 0.95, s.y + uy * r * 0.95);
        c.quadraticCurveTo(s.x + nx * r * 1.0, s.y + ny * r * 1.0, s.x - ux * r * 0.75, s.y - uy * r * 0.75);
        c.quadraticCurveTo(s.x - nx * r * 1.0, s.y - ny * r * 1.0, s.x + ux * r * 0.95, s.y + uy * r * 0.95);
        c.closePath(); c.fill(); c.stroke();
        c.globalAlpha = 0.9; c.fillStyle = pal.core;
        c.beginPath(); c.arc(s.x + ux * r * 0.15, s.y + uy * r * 0.15, r * 0.17, 0, TAU); c.fill();
        c.restore();
        continue;
      }
'''),

("drawShroud replaces the first-cut shroud",
 shroud_cut,
 '''    this.drawShroud(m);          // BACKLASH's shroud, glass, flashes and shards (v91 §6.1)
'''),

("drawShroud: the shroud, the glass, the flash, the shard, the smoke",
 '''  /* GYRE ON SCREEN (v90 §6.1):''',
 '''  /* BACKLASH ON SCREEN (v91 §6.1): "Cast: the glass goes black-bright; a
     shroud is drawn on the ball -- a soft dark disc r 48 with a violet rim
     (alpha 0.5) that breathes. A blow taken: the shroud flashes at the point
     of contact and a dark shard (a bolt-shaped streak, 0.15s) leaps from the
     caster to the foe ... Close: the shroud lifts as smoke (0.4s) ... Field:
     dark motes drawn INTO the shroud." DRAWN, not an fx.js field (the one
     `m.ultFx` slot is erased by the opponent's cast, and `src/render/fx.js` is
     shared by both chain lines) -- off the fighter's own `shroudFade`,
     `shroudFlash` and `shroudShards`.

     THE DISC IS A RING OF DARK AND NOT A LID: its gradient's inner stop is
     transparent and sits inside the ball's own rim, because a radial gradient
     fills its inner circle with stop 0 (§4.1b) and a dark lid would take the
     ball out of its own fight. On this near-black hall the dark alone does not
     read, so the rim, the motes' edges and the shard's edge carry the violet.
     THE GLASS is umbral head "A"'s own (STAFF.umbral): at 0.80 of the drawn
     staff, radius 0.27 of the drawn width (1.7x the sim's L, 1.3x artW).
     No rng. */
  drawShroud(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      if (!f.alive) continue;
      const pal = f.aff, foe = f === m.a ? m.b : m.a;
      /* THE SHARDS: a dark dart with a violet edge, leaping from inside the
         caster's rim to past the foe's centre, easing out over its 0.15s,
         longer for a bigger blow. PAST THE CENTRE, because nearly every blow
         thrown back was a blow that touched: the balls are in contact, and a
         shard running rim to rim has nowhere to go -- the first cut drew it
         six units long, in the seam between them. Over both balls, it reads. */
      for (const S of f.shroudShards){
        const u = Math.min(1, S.t / S.life), e = 1 - (1 - u) * (1 - u);
        const dx = foe.x - f.x, dy = foe.y - f.y, d = Math.hypot(dx, dy) || 1, ux = dx / d, uy = dy / d;
        const s0 = R * 0.6, s1 = d + R * 0.3;
        const hd = s0 + (s1 - s0) * e, tl = Math.max(s0, hd - 44 - Math.min(30, S.n * 1.2));
        const hx = f.x + ux * hd, hy = f.y + uy * hd, tx = f.x + ux * tl, ty = f.y + uy * tl;
        const w = 5 + Math.min(6, S.n * 0.25), mx = tx + (hx - tx) * 0.7, my = ty + (hy - ty) * 0.7;
        c.save();
        c.globalAlpha = 1 - 0.5 * u;
        c.fillStyle = pal.dark; c.strokeStyle = pal.core; c.lineWidth = 1.6;
        c.beginPath(); c.moveTo(hx, hy); c.lineTo(mx - uy * w, my + ux * w); c.lineTo(tx, ty); c.lineTo(mx + uy * w, my - ux * w); c.closePath();
        c.fill(); c.stroke();
        c.restore();
      }
      const k = f.shroudFade;
      if (!(k > 0.01)) continue;
      const T = f.shroudAge, lift = 1 - k;             // 0 while it stands, -> 1 as it lifts
      const br = 1 + 0.06 * Math.sin(T * 4.2);
      const rr = 48 * br * (1 + 0.35 * lift), cy = f.y - 26 * lift;
      c.save();
      /* the soft dark disc -- a ring of dark hugging the ball */
      const g = c.createRadialGradient(f.x, cy, R * 0.8, f.x, cy, rr * 1.06);
      g.addColorStop(0, pal.dark + "00"); g.addColorStop(0.6, pal.dark + "B0"); g.addColorStop(1, pal.dark + "00");
      c.globalAlpha = k; c.fillStyle = g;
      c.beginPath(); c.arc(f.x, cy, rr * 1.06, 0, TAU); c.fill();
      /* the violet rim, alpha 0.5, breathing with it */
      c.globalAlpha = 0.5 * k; c.strokeStyle = pal.core; c.lineWidth = 2.5;
      c.beginPath(); c.arc(f.x, cy, rr, 0, TAU); c.stroke();
      if (lift > 0.001){
        /* the lift: the shroud rises and spreads as smoke */
        for (let i = 0; i < 7; i++){
          const a = TAU * i / 7 + shellHash(9977, i);
          const px = f.x + Math.cos(a) * rr * 0.85, py = cy + Math.sin(a) * rr * 0.5 - 34 * lift * (0.6 + 0.8 * shellHash(9979, i));
          const pr = 9 + 16 * lift;
          c.globalAlpha = 0.5 * k; c.fillStyle = pal.dark;
          c.beginPath(); c.arc(px, py, pr, 0, TAU); c.fill();
          c.globalAlpha = 0.3 * k; c.strokeStyle = pal.core; c.lineWidth = 1.2;
          c.beginPath(); c.arc(px, py, pr, 0, TAU); c.stroke();
        }
      } else {
        /* the field: dark motes drawn INTO the shroud */
        c.fillStyle = pal.dark; c.strokeStyle = pal.core; c.lineWidth = 1.2;
        for (let i = 0; i < 10; i++){
          const ph = (T * (0.45 + 0.25 * shellHash(9971, i)) + shellHash(9973, i)) % 1;
          const a = TAU * shellHash(9975, i) - T * 0.6, r2 = 48 * (1.9 - 0.9 * ph);
          c.globalAlpha = 0.9 * k * Math.sin(ph * Math.PI);
          c.beginPath(); c.arc(f.x + Math.cos(a) * r2, f.y + Math.sin(a) * r2, 2.8, 0, TAU); c.fill(); c.stroke();
        }
      }
      /* the flash where a blow landed on it */
      c.globalCompositeOperation = "lighter";
      for (const F of f.shroudFlash){
        const q = 1 - F.t / F.life;
        c.globalAlpha = 0.9 * q; c.strokeStyle = pal.glow; c.lineWidth = 1 + 4 * q;
        c.beginPath(); c.arc(f.x, cy, rr, F.a - 0.55, F.a + 0.55); c.stroke();
        c.globalAlpha = 0.6 * q; c.fillStyle = pal.core;
        c.beginPath(); c.arc(f.x + Math.cos(F.a) * rr, cy + Math.sin(F.a) * rr, 5 + 7 * q, 0, TAU); c.fill();
      }
      c.globalCompositeOperation = "source-over";
      c.restore();
      /* the glass, black-bright: deepened to black, a bright violet rim and a
         glint, for as long as the shroud stands */
      const reach = f.w.reach * m.actMods.reach * f.reachMul;
      const Lq = (reach + 6) * 1.7, Wq = f.w.artW * 1.3, gx = Lq * 0.80, gr = Wq * 0.27;
      c.save();
      c.translate(f.x, f.y); c.rotate(f.theta); c.translate(R - 6, 0);
      c.globalAlpha = 0.85 * k; c.fillStyle = "#000000";
      c.beginPath(); c.arc(gx, 0, gr, 0, TAU); c.fill();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = 0.9 * k; c.strokeStyle = pal.core; c.lineWidth = Math.max(1.5, Wq * 0.05);
      c.beginPath(); c.arc(gx, 0, gr * 1.08, 0, TAU); c.stroke();
      c.globalAlpha = k; c.fillStyle = pal.glow;
      c.beginPath(); c.arc(gx - gr * 0.35, -gr * 0.35, gr * 0.16, 0, TAU); c.fill();
      c.restore();
    }
  }

  /* GYRE ON SCREEN (v90 §6.1):'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        if "shroudFade" in code:
            return 6
        return 5 if f"dmg:{fnum(TUNED_BLADE)}," in ent else 3
    return 2 if "bounce:" in re.search(r"shot:\{([^}]*)\}", ent).group(1) else 1


def all_stages():
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("5", s5_edits()), ("6", s6_edits())]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"])
    ap.add_argument("--src"); ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nNIGHTGLASS / BACKLASH -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8"); s = s0
    print(f"\nNIGHTGLASS / BACKLASH -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"bloodwick"' not in code or "gyreFade" not in code:
        raise SystemExit("wrong base: no Bloodwick stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin through Bloodwick in it")
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
    if "onHit:{ curse:1 }" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {RELIC} does not curse 1 on hit")
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 2 and out.count("if (S.bounce !== undefined) s.bounce = S.bounce;") != 1:
        raise SystemExit("REFUSING TO WRITE -- the bounce is not copied at spawn exactly once")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        hook = (("shroudBack(f, taken, src, hx, hy){", "this.shroudBack(foe, pool0 - (foe.hp + foe.shield), src, hx, hy);")
                if stage >= 6 else ("shroudBack(f, taken){", "this.shroudBack(foe, pool0 - (foe.hp + foe.shield));"))
        for need in ("tickShroud(dt){", "this.tickShroud(dt);", 'u.kind === "backlash"', *hook, "this._reflecting = true;"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    if stage >= 6:
        for need, n in (("this.hurt(foe, dmg, self, hx, hy);", 1), ("  hurt(foe, dmg, src, hx, hy){", 1),
                        ("shroudPresent(dt){", 1), ("this.shroudPresent(dt);", 1), ("drawShroud(m){", 1),
                        ("this.drawShroud(m);", 1), ('w: "nightglass-echo", dmg: back', 1),
                        ('SFX.play("ult", { w: "nightglass-close" })', 1), ('w === "nightglass"', 1),
                        ('w === "nightglass-echo"', 1), ('w === "nightglass-close"', 1)):
            if out.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is there {out.count(need)} times, not {n}")
        if "FIRST CUT" in s[s.index("NIGHTGLASS'S SHADEBOLT"):s.index("NIGHTGLASS'S SHADEBOLT") + 60]:
            raise SystemExit("REFUSING TO WRITE -- the first-cut shadebolt survived")
        for k in VOICES:
            if s.count(arm(k, "          ")) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- the {k} voice is not the picked body, exactly once")
        print("  ok    voices " + ", ".join(f"{k} {VOICE_PICKS[k]}" for k in VOICES) + "; the shroud, the glass, the flash, the shard, the smoke drawn")
    check_no_rng(edits)
    if out.count('shape:"staff"') != 7:
        raise SystemExit("REFUSING TO WRITE -- expected exactly seven staves in the roster")
    print(f"  ok    relic  staff, the bow's body, curse 1, {'the shadebolt' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    seven staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
