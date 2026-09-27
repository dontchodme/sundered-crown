#!/usr/bin/env python
"""WATCHLIGHT / BEACON -- the vigil staff, the staff row's fourth. v92.

Built from `06-docs/v92/WATCHLIGHT-BUILD-BRIEF.md` and `vigil-staff-design-v92.md`
(Cowork, 2026-09-27), the row's `06-docs/v89/STAFF-ROW-v89.md` §1/§6 -- the
input and the only input (CLAUDE.md §3 rule 0). Rick: "build them all".

    stage 1   the relic, its ultimate STUBBED          sc-cipher-fx -> sc-watchlight
    stage 2   the spell: WARDBOLT (the shove)          sc-watchlight -> sc-wardbolt
    stage 3   the ultimate: BEACON (the lantern)       sc-wardbolt -> sc-beacon
    stage 5   the blade: 9.3, the design's, MEASURED   (no link -- nothing moved)
    stage 6   picture, voices, the blade's note        sc-beacon -> sc-watchlight-fx

THE BASE is the staff branch's tip (Culverin, Briarwand, Cipher 1-6); several
anchors are those builds' own lines, so the staves carry together, in order.

THE READINGS, where the build has to choose:
  1. THE SHOVE IS COPIED AT SPAWN (§5: "`spawnShot` copies `knock`"). The lab
     set it from `fresh()`, AFTER the step a bolt was loosed on -- so a bolt
     that landed on its first step carried no shove there. The artifact
     Briarwand's fan and Cipher's wall-stop both had; measured at stage 2.
  2. THE LANTERN IS PLACED at the caster's centre clamped inside the inset
     (§5), and then HOLDS ITS PLACE while the hall closes, as the lab's did.
  3. A FULL HALL REFUSES A LANTERN SHOT (`maxLive`, §5 "refused, counted"),
     and the lantern tries again the next step: the lab moved `next` only
     when a shot left, so a refusal delays the cadence and loses nothing.
  4. THE WINDOW keeps its 8s on the engine's window clock, which stops
     through hit stop (Cipher's measurement, v94 build §3); the charge is
     the lab's 16 in the game's clock, measured for this fighter.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC, BUILDER = "watchlight", "watchlight_build.py"
BLADE = 9.3                    # brief §2 stage 1: "stubbed relic at 9.3"; stage 5 settles it
WARD = 2.5                     # Farwarden's onSelf, the bow row's and the staff's (design §5)
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.34, speed=400, r=26, life=3.4, grav=0, dmgMul=1.0, knock=420,
             spell="wardbolt", tip="Bolts of light shove the foe · clankable")
CARD = "Sets down a lantern that fires at the foe. Every hit banks ward"
ULT_NAME, ULT_KIND = "Beacon", "beacon"
# Design §5, brief §0. `charge` is the lab's 16 in the game's clock, measured.
ULT = {"charge": 14, "dur": 8, "every": 1.2, "speed": 420, "r": 22, "life": 3.0, "dmgMul": 0.6, "knock": 150}
ULT_KEYS = list(ULT)
BLURB = ("A pale rod with a lantern caged in its head. It throws light that shoves, "
         "and for eight seconds it sets the lamp down to keep the watch.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm B of design §3.1, the vigil BOW
     body at the staff's blade and the bow's ward 2.5 -- which stage 2's
     wardbolt is measured against.
'''
ULT_STUB = f'''    /* BEACON. STUBBED AT `charge:1e9` IN STAGE 1. `kind:"{ULT_KIND}"` is its
       own; the card is Cowork's (design §6), in at stage 1. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''
S1_BLADE_PARA = f'''     `dmg` {fnum(BLADE)} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 9.3 on Chromium 141, and stage 5 settles it wide on 151. */'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* WATCHLIGHT -- THE VIGIL STAFF, the staff row's fourth relic. Built from
     `06-docs/v92/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Vigil banks what it
     deals as a plate, and on a bow the bank has to be 2.5x (Farwarden's
     `onSelf`, and its comment says why): the staff keeps the bow's 2.5,
     worth +17 at the staff's blade on its own (design §3.1).

{S1_SHOT_PARA}
{S1_BLADE_PARA}
  {{ id:"{RELIC}", name:"Watchlight", aff:"vigil", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onSelf:{{ ward:{fnum(WARD)} }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [("Watchlight joins the roster, its ultimate stubbed",
             '''

];
/* The single source of truth for "which status does this relic teach".''',
             relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".''')]


S2_SHOT_PARA = '''     THE SPELL IS WARDBOLT (design §1, §5): a heavy bolt of light every
     0.34s along the facing -- wider than an arrow (r 26, 400 px/s) -- and a
     foe it lands on is SHOVED 420 along the bolt's travel (`knock`, the
     field the foe branch of `tickShots` already applies for Reprisal).
     Every landing banks ward at the bow's 2.5. The shove measured FREE at
     660 an arm (-2 against the bow at ward 2.5) and is kept for the
     picture (§3.1).
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Watchlight looses the wardbolt",
 f'''  {{ id:"{RELIC}", name:"Watchlight", aff:"vigil", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Watchlight", aff:"vigil", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("spawnShot: a wardbolt carries its shove from the barrel",
 '''      if (S.sigilLife){ s.bounce = 1; s.glyph = true; }
''',
 '''      if (S.sigilLife){ s.bounce = 1; s.glyph = true; }
      /* WATCHLIGHT'S WARDBOLT (v92 §5): `spawnShot` copies `knock`, AT SPAWN
         -- the lab set it one step late, so a bolt that landed on its first
         step shoved nothing there. The foe branch of `tickShots` applies it
         along the bolt's travel, as it does Reprisal's. */
      if (S.knock !== undefined) s.knock = S.knock;
'''),

("the wardbolt is drawn (first cut)",
 '''      /* CIPHER'S RUNES ON SCREEN (v94 §6.1).''',
 '''      /* WATCHLIGHT'S WARDBOLT -- FIRST CUT, for stage 2's film; the picture is
         stage 6's. "A broad, short bolt of light (r 26, drawn wider than it
         is long) with a bright head" (v92 §6.1). Off the shot's own state;
         no rng. */
      if (s.spell === "wardbolt"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.translate(s.x, s.y); c.rotate(Math.atan2(s.vy, s.vx));
        c.globalAlpha = 0.45; c.fillStyle = pal.core;
        c.beginPath(); c.ellipse(-s.r * 0.35, 0, s.r * 0.7, s.r, 0, 0, TAU); c.fill();
        c.globalAlpha = 0.9; c.fillStyle = pal.glow;
        c.beginPath(); c.ellipse(s.r * 0.1, 0, s.r * 0.32, s.r * 0.78, 0, 0, TAU); c.fill();
        c.restore();
        continue;
      }
      /* CIPHER'S RUNES ON SCREEN (v94 §6.1).'''),
    ]


ULT_NOTE = '''    /* BEACON (design §1, §5). The staff sets a lantern down where it stands;
       for `dur` seconds the lantern fires a bolt of its own at the foe every
       `every` s -- aimed at where the foe IS, no lead, at `speed`, `r`,
       `dmgMul` of the blade, shoving `knock` -- and every lantern hit banks
       ward to the caster through the relic's own onSelf. A second source of
       fire that AIMS, so the staff keeps sweeping (+29 over the spell, §3.1).
       A lantern at 0.5s reads 97%: the cadence is the design's knob and it
       is 1.2s -- not to be "fixed" downward (brief §0).

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v92/watchlight-build-v92.md`. */
'''


def s3_edits(U: dict):
    return [
("Beacon is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Beacon's lantern",
 '''    this.convergeLit = 0;
''',
 '''    this.convergeLit = 0;
    /* {t, dur, x, y, next} while BEACON's lantern stands (v92): where it was
       set down, the window's clock, and when it fires next. null otherwise:
       `tickBeacon` returns after a two-iteration loop. `beaconTally` is the
       probe's; nothing in the sim reads it. */
    this.ultBeacon = null;
    this.beaconTally = null;
'''),

("the cast sets the lantern down and resolves nothing",
 '''    if (u.kind === "converge"){
''',
 '''    if (u.kind === "beacon"){
      /* BEACON (v92). The lantern is SET DOWN at the caster's centre, clamped
         inside the inset (§5), and fires from `tickBeacon` -- its first shot
         on this step. `m.ultFx` is the cast flash only (open item 25). */
      const A = CONFIG.arena, n = this.inset;
      f.ultBeacon = { t: 0, dur: u.dur, x: clamp(f.x, n, A.w - n), y: clamp(f.y, n, A.h - n), next: 0 };
      if (!f.beaconTally) f.beaconTally = { casts: 0, fired: 0, refused: 0 };
      f.beaconTally.casts++;
      return;
    }
    if (u.kind === "converge"){
'''),

("the lantern ticks with the window tickers",
 '''    this.tickConverge(dt);              // CONVERGENCE (v94): the runes leave the walls
''',
 '''    this.tickConverge(dt);              // CONVERGENCE (v94): the runes leave the walls
    this.tickBeacon(dt);                // BEACON (v92): the lantern keeps the watch
'''),

("tickBeacon: the lantern fires at the foe",
 '''  /* =============================================== CONVERGENCE ========''',
 '''  /* ==================================================== BEACON ========
     v92 §5, and the lab (`overlays/staff_vigil.js`) where the prose is
     silent. Every `every` seconds of the window -- the first on the cast's
     own step -- while both are alive, a shot is pushed from the lantern at
     atan2(foe - lantern), NO lead: `speed`, `r`, `life`, `dmgMul`, `knock`,
     `own` the caster's, `lamp` (the art). It is a shot in every other
     respect: clankable, the wall kills it, `resolveHit(caster, ...)` lands
     it and banks ward through the relic's own onSelf, and it files as a
     shot does (`x0, y0, t0`). A full hall (`maxLive`) REFUSES it -- counted
     -- and the lantern tries again on the next step: the lab moved `next`
     only when a shot left.

     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step. The lantern holds its place while the hall closes,
     as the lab's did. */
  tickBeacon(dt){
    for (const f of [this.a, this.b]){
      const B = f.ultBeacon;
      if (!B) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultBeacon = null; continue; }
      B.t += dt;
      if (B.t >= B.dur){ f.ultBeacon = null; continue; }
      if (B.t < B.next) continue;
      const T = f.beaconTally;
      if (this.shots.length >= CONFIG.shot.maxLive){ T.refused++; continue; }
      const u = f.w.ult, a = Math.atan2(foe.y - B.y, foe.x - B.x);
      B.next += u.every;
      this.shots.push({
        own: f === this.a ? "a" : "b", x: B.x, y: B.y, x0: B.x, y0: B.y,
        spd0: 0, t0: this.t,                 // CINEMA: a lantern shot files as a shot does
        vx: Math.cos(a) * u.speed, vy: Math.sin(a) * u.speed,
        r: u.r, life: u.life, max: u.life, grav: 0, dmgMul: u.dmgMul,
        seed: false, aff: f.aff, a, knock: u.knock, lamp: true,
      });
      T.fired++;
    }
  }

  /* =============================================== CONVERGENCE ========'''),

("the lantern's shot is drawn (first cut)",
 '''      /* WATCHLIGHT'S WARDBOLT -- FIRST CUT, for stage 2's film; the picture is''',
 '''      /* THE LANTERN'S SHOT -- FIRST CUT, for stage 3's film: "a smaller bolt
         leaves it straight at the foe with a short trail" (v92 §6.1). */
      if (s.lamp){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 0.5; c.strokeStyle = pal.core; c.lineWidth = s.r * 0.6; c.lineCap = "round";
        c.beginPath(); c.moveTo(s.x - ux * s.r * 1.8, s.y - uy * s.r * 1.8); c.lineTo(s.x, s.y); c.stroke();
        c.globalAlpha = 0.9; c.fillStyle = pal.glow;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.55, 0, TAU); c.fill();
        c.restore();
        continue;
      }
      /* WATCHLIGHT'S WARDBOLT -- FIRST CUT, for stage 2's film; the picture is'''),

("drawBeacon: the lantern on the floor (first cut)",
 '''  /* CONVERGENCE ON SCREEN (v94 §6.1):''',
 '''  /* BEACON'S LANTERN -- FIRST CUT, for stage 3's film (v92 §6.1): "a small
     cage r 20 with the same core, a ground ring r 28 under it". Off the
     fighter's own `ultBeacon`; no rng. The picture is stage 6's. */
  drawBeacon(m){
    const c = this.ctx;
    for (const f of [m.a, m.b]){
      const B = f.ultBeacon;
      if (!B) continue;
      const pal = f.aff;
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = 0.5; c.strokeStyle = pal.glow; c.lineWidth = 2;
      c.beginPath(); c.arc(B.x, B.y, 28, 0, TAU); c.stroke();
      c.globalAlpha = 0.85; c.fillStyle = pal.core;
      c.beginPath(); c.arc(B.x, B.y, 9, 0, TAU); c.fill();
      c.globalAlpha = 0.9; c.strokeStyle = pal.glow; c.lineWidth = 2.4;
      c.strokeRect(B.x - 14, B.y - 20, 28, 40);
      c.restore();
    }
  }

  /* CONVERGENCE ON SCREEN (v94 §6.1):'''),

("drawBeacon is drawn with the shots",
 '''    this.drawConverge(m);        // CONVERGENCE's ring and motes (v94 §6.1)
''',
 '''    this.drawConverge(m);        // CONVERGENCE's ring and motes (v94 §6.1)
    this.drawBeacon(m);          // BEACON's lantern (v92 §6.1)
'''),
    ]


# THE PICKED VOICES, from watchlight_voice_lab.py (runs/build/stage6_voice_lab.json), verbatim.
VOICES = {
    'cast': '\n  S._burst(t, { freq: 440, q: 1.2, gain: 0.1198, dur: 0.045, type:"bandpass" });\n  S._burst(t + 0.045, { freq: 600, q: 1.8, gain: 0.0599, dur: 0.03, type:"bandpass" });\n  S._tone (t, { freq: 210, to: 150, gain: 0.07189, dur: 0.07, type:"triangle" });\n  S._tone (t + 0.08, { freq: 1397, gain: 0.0599, dur: 0.44, type:"sine" });\n  S._tone (t + 0.08, { freq: 2093, gain: 0.02396, dur: 0.30, type:"sine" });',
    'lamp': '\n  const n = Math.max(1, Math.min(8, p.n | 0)), k = Math.pow(2, (n - 1) / 12);\n  S._burst(t, { freq: 1520 * k, q: 1.6, gain: 0.04501, dur: 0.04, type:"bandpass" });',
    'thump': '\n  S._tone (t, { freq: 120, to: 60, gain: 0.1198, dur: 0.10, type:"triangle" });',
    'close': '\n  S._sweep(t + 0, { f0: 1397, f1: 1397, q: 40, gain: 0.3367, dur: 0.3, atk: 0.18, type:"bandpass" });\n  S._sweep(t + 0, { f0: 2093, f1: 2093, q: 40, gain: 0.1347, dur: 0.3, atk: 0.18, type:"bandpass" });\n  S._sweep(t + 0.08, { f0: 1397, f1: 1397, q: 40, gain: 0.8419, dur: 0.3, atk: 0.18, type:"bandpass" });\n  S._sweep(t + 0.08, { f0: 2093, f1: 2093, q: 40, gain: 0.3367, dur: 0.3, atk: 0.18, type:"bandpass" });',
}
VOICE_PICKS = {'cast': 'SETDOWN', 'lamp': 'BRIGHTEST', 'thump': 'DRUM', 'close': 'STAGGER2'}


# ---------------------------------------------------------------- stage 5 --
# THE BLADE IS THE DESIGN'S, MEASURED: wide on 151, both sides, two seed
# blocks, 1480 fights a row -- 9.1 46.2%, 9.3 49.4%, 9.6 51.2%. Nothing moves,
# so stage 5 has no link of its own; the relic's note says so in stage 6's.
S5_BLADE_PARA = f'''     `dmg` {fnum(BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of every
     pairing, two seed blocks, 1480 fights a row, no bisection -- 9.1 reads
     46.2%, 9.3 49.4%, 9.6 51.2%. THE DESIGN'S OWN NUMBER, and the build IS
     its lab: stage 1 is arm B to the decimal (23.8%), the spell reads 22.0%
     against arm S's 19.1% because the lab gave the shove one step late
     (19.1% exactly with that put back), and the whole relic 49.7% against
     arm U's 50.2% on the lab's field. The number lives in
     `watchlight_build.BLADE`. */'''


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule". PRESENTATION ONLY: SFX.play (a no-op headless),
# render-only fields, drawing code -- no rng, no spawnFx. engine_ab over all
# 38, Watchlight included, is the proof. The voices are
# `watchlight_voice_lab.py`'s picks (two rounds), pasted verbatim; each arm
# opens `const S = this;`.


def arm(key: str, indent: str) -> str:
    body = VOICES[key].strip("\n")
    lines = [indent + "const S = this;"] + [indent + (l[2:] if l.startswith("  ") else l) for l in body.splitlines()]
    return "\n".join(lines)


def s6_edits():
    s2 = {l: n for l, o, n in s2_edits(fnum(BLADE))}
    s3 = {l: n for l, o, n in s3_edits(dict(ULT))}
    bolt_cut = s2["the wardbolt is drawn (first cut)"]
    bolt_cut = bolt_cut[:bolt_cut.index("      /* CIPHER'S RUNES ON SCREEN (v94 §6.1).")]
    lamp_cut = s3["the lantern's shot is drawn (first cut)"]
    lamp_cut = lamp_cut[:lamp_cut.index("      /* WATCHLIGHT'S WARDBOLT -- FIRST CUT, for stage 2's film; the picture is")]
    beacon_cut = s3["drawBeacon: the lantern on the floor (first cut)"]
    beacon_cut = beacon_cut[:beacon_cut.index("  /* CONVERGENCE ON SCREEN (v94 §6.1):")]
    return [

("the relic's note says the blade is measured", S1_BLADE_PARA, S5_BLADE_PARA),

("Sfx: Beacon's cast, the lantern's shot, the thump and the close",
 '''        } else if (w === "cipher"){                     // the rune-ring opens
''',
 '''        } else if (w === "watchlight"){                 // a lamp set down
          /* BEACON'S CAST -- design §6.2: "a lamp being set down -- a wooden
             knock into a glass chime, 0.35s". SETDOWN (`watchlight_voice_lab.py`,
             two rounds, Rick's "you pick i overrule"): a knock and a settle,
             then a two-partial chime on F6, 6 dB under a wardbolt's blow,
             audible 350 ms, striking (its top 105 ms in, never a swell).
             Watchlight fell through to the rune-crack until now. */
''' + arm("cast", "          ") + '''
        } else if (w === "watchlight-lamp"){            // the lantern fires
          /* A LANTERN SHOT -- "the staff's own shot voice, filtered brighter
             and quieter (it is the smaller bolt), pitched by the lantern's
             count". BRIGHTEST: the staff's release (a 380 Hz burst) carried
             to 1520 Hz, 3 dB under it, up a semitone a shot -- `p.n` is the
             shot's count in this window. */
''' + arm("lamp", "          ") + '''
        } else if (w === "watchlight-thump"){           // a wardbolt shoves
          /* THE SHOVE -- "the game's hit voice with a low thump under it when
             knock >= 400". DRUM: a falling triangle 120 -> 60 Hz, 8 dB under
             the hit, and the one of three still heard ON A PHONE (6 dB over
             the release there; the pure sine thump vanished). Its own arm,
             played after the hit voice, so no other relic's hit can move. */
''' + arm("thump", "          ") + '''
        } else if (w === "watchlight-close"){           // the lantern goes out
          /* CLOSE -- "the chime reversed, short": the cast's two partials as
             narrow bands of noise swelling and cut off, two swells 0.08s
             apart; 185 ms, loudest 135 ms in. Played by `tickBeacon` when the
             window runs out by its clock, never on a death. */
''' + arm("close", "          ") + '''
        } else if (w === "cipher"){                     // the rune-ring opens
'''),

("the lantern's shot is heard, counted, and flares",
 '''      B.next += u.every;
''',
 '''      B.next += u.every;
      /* HEARD AND SEEN (§6.1-6.2): the lantern's own voice pitched by its
         count in this window, and the flare's clock. Neither is read by the
         simulation. */
      B.n = (B.n || 0) + 1; B.shotT = B.t;
      SFX.play("ult", { w: "watchlight-lamp", n: B.n });
'''),

("the window running out by its clock is heard",
 '''      if (B.t >= B.dur){ f.ultBeacon = null; continue; }
''',
 '''      if (B.t >= B.dur){ SFX.play("ult", { w: "watchlight-close" }); f.ultBeacon = null; continue; }
'''),

("the lantern's picture keeps its own clock",
 '''      T.fired++;
    }
  }
''',
 '''      T.fired++;
    }
    /* THE PICTURE'S CLOCK: 1 while the lantern stands, down over 0.4s after
       ("the lantern gutters and goes out over 0.4s"), and where it stood, so
       it goes out where it was. On the fighter; read by `drawBeacon` alone. */
    for (const f of [this.a, this.b]){
      const B = f.ultBeacon;
      if (B){ f.beaconFade = 1; f.beaconX = B.x; f.beaconY = B.y; f.beaconAge = B.t; }
      else f.beaconFade = Math.max(0, f.beaconFade - dt / 0.4);
    }
  }
'''),

("the fighter carries the lantern's picture",
 '''    this.ultBeacon = null;
    this.beaconTally = null;
''',
 '''    this.ultBeacon = null;
    this.beaconTally = null;
    /* THE LANTERN'S PICTURE (v92 §6.1): its fade, where it stood, and its
       window's age. Render-only. */
    this.beaconFade = 0;
    this.beaconX = 0;
    this.beaconY = 0;
    this.beaconAge = 0;
'''),

("a wardbolt's shove is heard under the hit",
 '''          SFX.play("ult", { w: "cipher-hex", n: foe.stacks("hex") });
          this.ring(foe.x, foe.y, s.aff.glow, 12, 60, 0.32, 3);
        }
''',
 '''          SFX.play("ult", { w: "cipher-hex", n: foe.stacks("hex") });
          this.ring(foe.x, foe.y, s.aff.glow, 12, 60, 0.32, 3);
        }
        /* WATCHLIGHT'S SHOVE, HEARD (v92 §6.2): a low thump under the hit voice
           when the bolt's knock is 400 or more -- a wardbolt's 420, never the
           lantern's 150. */
        if (s.spell === "wardbolt" && s.knock >= 400) SFX.play("ult", { w: "watchlight-thump" });
'''),

("the staff's vigil head: Code's pick, and why",
 '''CONVERGENCE lights exactly that ring. B and C stay
   until Rick has seen it. */
''',
 '''CONVERGENCE lights exactly that ring. B and C stay
   until Rick has seen it. */
/* THE VIGIL HEAD IS "A" -- Code's pick for Watchlight, the same ruling: the
   CAGE lantern on its bracket, because design §6.1 asks for "a lantern-cage
   head; a warm vigil core burns in the cage" and BEACON takes exactly that
   lamp down to the floor. B and C stay until Rick has seen it. */
'''),

("the wardbolt: a broad short bolt of light",
 bolt_cut,
 '''      /* WATCHLIGHT'S WARDBOLT ON SCREEN (v92 §6.1): "a broad, short bolt of
         light (r 26, drawn wider than it is long) with a bright head". A soft
         body, a brighter front, a short streak behind it -- flat shapes under
         `lighter`, off the shot's own state; no rng. */
      if (s.spell === "wardbolt"){
        const pal = s.aff;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.translate(s.x, s.y); c.rotate(Math.atan2(s.vy, s.vx));
        c.globalAlpha = 0.28; c.strokeStyle = pal.core; c.lineWidth = s.r * 0.9; c.lineCap = "round";
        c.beginPath(); c.moveTo(-s.r * 1.6, 0); c.lineTo(-s.r * 0.4, 0); c.stroke();
        c.globalAlpha = 0.45; c.fillStyle = pal.core;
        c.beginPath(); c.ellipse(-s.r * 0.35, 0, s.r * 0.7, s.r, 0, 0, TAU); c.fill();
        c.globalAlpha = 0.9; c.fillStyle = pal.glow;
        c.beginPath(); c.ellipse(s.r * 0.1, 0, s.r * 0.32, s.r * 0.78, 0, 0, TAU); c.fill();
        c.globalAlpha = 0.9; c.fillStyle = "#FFFFFF";
        c.beginPath(); c.ellipse(s.r * 0.22, 0, s.r * 0.12, s.r * 0.46, 0, 0, TAU); c.fill();
        c.restore();
        continue;
      }
'''),

("the lantern's shot: the smaller bolt with a short trail",
 lamp_cut,
 '''      /* THE LANTERN'S SHOT ON SCREEN (v92 §6.1): "a smaller bolt leaves it
         straight at the foe with a short trail" -- the wardbolt's colours at
         the lantern's size, a trail instead of a body. */
      if (s.lamp){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        c.save();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 0.5; c.strokeStyle = pal.core; c.lineWidth = s.r * 0.6; c.lineCap = "round";
        c.beginPath(); c.moveTo(s.x - ux * s.r * 1.8, s.y - uy * s.r * 1.8); c.lineTo(s.x, s.y); c.stroke();
        c.globalAlpha = 0.3; c.fillStyle = pal.glow;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.9, 0, TAU); c.fill();
        c.globalAlpha = 0.95; c.fillStyle = pal.glow;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.5, 0, TAU); c.fill();
        c.restore();
        continue;
      }
'''),

("drawBeacon: the lantern, its flare and its motes, and the staff's empty cage",
 beacon_cut,
 '''  /* BEACON ON SCREEN (v92 §6.1). "Cast: the cage opens; a lantern is LEFT
     on the floor where the caster was -- a small cage r 20 with the same
     core, a ground ring r 28 under it -- and the caster moves on without it.
     The lantern is the tell ... A lantern shot: the lantern flares ...
     Close: the lantern gutters and goes out over 0.4s; the cage on the staff
     closes. Field: pale motes rising from the lantern." DRAWN, not an fx.js
     field (the one `m.ultFx` slot is erased by the opponent's cast, and
     `src/render/fx.js` is shared by both chain lines) -- all of it off the
     fighter's own `beaconFade` and `ultBeacon`.

     THE STAFF'S CAGE is vigil head "A"'s own (STAFF.vigil): its light sits at
     0.83 of the drawn staff (1.7x the sim's L, from R - 6), the cage 0.34 of
     the drawn length long and 0.66 of the drawn width (1.3x artW) tall.
     While the lantern stands the cage is dark -- the light is on the floor
     -- and it comes back as the lantern goes out.

     No rng: `shellHash` and the window's own clock. */
  drawBeacon(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const k = f.beaconFade;
      if (!(k > 0.01)) continue;
      const pal = f.aff, B = f.ultBeacon, x = f.beaconX, y = f.beaconY, T = f.beaconAge;
      const iron = SHAPES._ink(pal.dark, 9.7);
      /* the gutter: once the window has shut the light flickers down */
      const gut = B ? 1 : k * (0.65 + 0.35 * Math.sin(m.t * 47));
      const fl = B && B.shotT !== undefined ? clamp(1 - (B.t - B.shotT) / 0.18, 0, 1) : 0;
      c.save();
      /* the ground ring and its pool */
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = 0.12 * gut; c.fillStyle = pal.core;
      c.beginPath(); c.arc(x, y, 28, 0, TAU); c.fill();
      c.globalAlpha = 0.5 * gut; c.strokeStyle = pal.glow; c.lineWidth = 2;
      c.beginPath(); c.arc(x, y, 28, 0, TAU); c.stroke();
      /* the light in the cage, and the flare on every shot */
      c.fillStyle = pal.glow;
      c.globalAlpha = 0.16 * gut + 0.35 * fl; c.beginPath(); c.arc(x, y - 4, 24 + 14 * fl, 0, TAU); c.fill();
      c.globalAlpha = 0.35 * gut; c.beginPath(); c.arc(x, y - 4, 13, 0, TAU); c.fill();
      c.fillStyle = pal.core;
      c.globalAlpha = 0.95 * gut; c.beginPath(); c.arc(x, y - 4, 7, 0, TAU); c.fill();
      /* the motes rising off it */
      for (let i = 0; i < 8; i++){
        const ph = ((B ? T : f.beaconAge) * (0.45 + 0.3 * shellHash(9911, i)) + shellHash(9913, i)) % 1;
        c.globalAlpha = 0.55 * gut * Math.sin(ph * Math.PI);
        c.fillStyle = i % 3 ? pal.glow : "#FFF6DA";
        c.beginPath();
        c.arc(x + (shellHash(9915, i) - 0.5) * 30 + Math.sin(ph * 6 + i) * 4, y - 12 - ph * 58, 2.1, 0, TAU);
        c.fill();
      }
      /* the cage itself: iron, drawn over its light -- a frame, three bars, a
         roof and a ring to carry it by */
      c.globalCompositeOperation = "source-over";
      c.globalAlpha = Math.min(1, 0.4 + 0.6 * k);
      c.strokeStyle = iron; c.lineWidth = 2.6; c.lineJoin = "round";
      c.strokeRect(x - 13, y - 20, 26, 32);
      c.lineWidth = 1.8;
      for (const u of [-6.5, 0, 6.5]){ c.beginPath(); c.moveTo(x + u, y - 20); c.lineTo(x + u, y + 12); c.stroke(); }
      c.lineWidth = 2.6;
      c.beginPath(); c.moveTo(x - 15, y - 20); c.lineTo(x, y - 28); c.lineTo(x + 15, y - 20); c.stroke();
      c.beginPath(); c.arc(x, y - 31, 3.2, 0, TAU); c.stroke();
      /* THE STAFF'S CAGE, EMPTY while the lantern is out, relit as it goes */
      if (f.alive){
        const reach = f.w.reach * m.actMods.reach * f.reachMul;
        const Lq = (reach + 6) * 1.7, Wq = f.w.artW * 1.3;
        const hd = R - 6 + Lq * 0.83;
        c.translate(f.x + Math.cos(f.theta) * hd, f.y + Math.sin(f.theta) * hd);
        c.rotate(f.theta);
        c.globalAlpha = 0.82 * k;
        c.fillStyle = pal.dark;
        c.fillRect(-Lq * 0.15, -Wq * 0.28 + Wq * 0.03, Lq * 0.30, Wq * 0.56);
        c.fillStyle = iron;
        for (const u of [-0.057, 0.057]) c.fillRect(Lq * u - Wq * 0.025, -Wq * 0.30 + Wq * 0.03, Wq * 0.05, Wq * 0.60);
      }
      c.restore();
    }
  }

'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        return 6 if "beaconFade" in code else 3
    return 2 if "knock:" in re.search(r"shot:\{([^}]*)\}", ent).group(1) else 1


def all_stages():
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("6", s6_edits())]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "6"])
    ap.add_argument("--src"); ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nWATCHLIGHT / BEACON -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8"); s = s0
    print(f"\nWATCHLIGHT / BEACON -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"cipher"' not in code or "convergeLit" not in code:
        raise SystemExit("wrong base: no Cipher stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin, Briarwand and Cipher stages 1-6 in it")
    have = stage_of(code)
    want = {1: 0, 2: 1, 3: 2, 6: 3}[stage]
    if have != want:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built on stage {want}")
    if stage == 1:
        check_bow_body(code); edits = s1_edits()
    elif stage == 2:
        edits = s2_edits(re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1))
    elif stage == 3:
        edits = s3_edits(dict(ULT))
    else:
        edits = s6_edits()
    for label, old, new in edits:
        s = one(s, old, new, label)
    out = strip_comments(s)
    shot = SPELL if stage >= 2 else BOW_SHOT
    ent = check_entry(out, RELIC, shot, BLADE, stubbed=(stage <= 2))
    if f"onSelf:{{ ward:{fnum(WARD)} }}" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {RELIC}'s ward bank is not the bow's {WARD}")
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 2 and out.count("if (S.knock !== undefined) s.knock = S.knock;") != 1:
        raise SystemExit("REFUSING TO WRITE -- the shove is not copied at spawn exactly once")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickBeacon(dt){", "this.tickBeacon(dt);", 'u.kind === "beacon"', "lamp: true,"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    check_no_rng(edits)
    if out.count('shape:"staff"') != 4:
        raise SystemExit("REFUSING TO WRITE -- expected exactly four staves in the roster")
    print(f"  ok    relic  staff, the bow's body, ward {WARD}, {'the wardbolt' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    four staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
