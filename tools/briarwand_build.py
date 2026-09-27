#!/usr/bin/env python
"""BRIARWAND / BLOOM -- the verdant staff, the staff row's second. v93.

Built from `06-docs/v93/BRIARWAND-BUILD-BRIEF.md` and
`verdant-staff-design-v93.md` (Cowork, 2026-09-27), the row's
`06-docs/v89/STAFF-ROW-v89.md` §1/§6. Those are the input and the only input
(CLAUDE.md §3 rule 0). Rick, 2026-09-27: "go ahead with the rest" / "build
them all".

    stage 1   the relic, its ultimate STUBBED           sc-ironfall-fx -> sc-briarwand
    stage 2   the spell: THORNBURST (the fan)           sc-briarwand -> sc-thornburst
    stage 3   the ultimate: BLOOM (the drifting cloud)  sc-thornburst -> sc-bloom
    stage 5   the blade, wide on 151: 17 -> 15.25       sc-bloom -> sc-bloom-blade
    stage 6   picture, voices, drawn pollen             sc-bloom-blade -> sc-bloom-fx

THE BASE is the staff branch's tip, `sc-ironfall-fx.html` (sc-leaf + Culverin
stages 1-6): the STAFF art and `shape:"staff"` are already in it, and several
anchors below are Culverin's own lines, so the two carry together, in order.

TWO NAMES THE BRIEF USES ARE NOT THE ONES BUILT, AND NEITHER IS A DESIGN CHOICE:
  * `f.ultBloom` is the THICKET's (Vinesower's seed window) -- `spawnShot` reads
    it on every shot. Briarwand's cloud lives in `f.ultPollen`, the lab's own
    name for it. `kind:"bloom"` is free (the Thicket is `seedfall`) and is used.
  * The spell's shot block gains `spell:"thornburst"` beside the design's
    numbers, for the renderer (Culverin's `spell` line in `spawnShot`).
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC = "briarwand"
BUILDER = "briarwand_build.py"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9).
BLADE = 17                     # brief §2 stage 1: "stubbed relic at 17"; stage 5 settles it
# STAGE 5 -- THE BLADE, MEASURED WIDE ON 151, on sc-bloom at charge 14: both
# sides of every pairing, all 35 foes, two seed blocks (2207, 5003), 2100
# fights a point, no bisection (v48/v56/v66). Coarse first (700 a point):
# 14 40.7%, 15 50.7%, 16 54.7%, 17 60.7%. Then wide:
#     14.75 45.7% (44.2 / 47.2)     15.25 50.1% (51.1 / 49.0)
#     15.0  48.5% (48.6 / 48.4)     15.5  51.8% (51.0 / 52.7)
# 15.25 is the measured row nearest 50%; the honest interval is 15.0-15.5.
# 1.25 UNDER THE DESIGN'S 16.5, AND THE REASON IS THE LAB, NOT THE BUILD: the
# priced overlay added the fan's side thorns only when the middle thorn
# survived its first step, so it priced a fan missing ~22% of its side thorns
# (build doc §2). PROVISIONAL: v89 §8.2 re-prices the row against all seven.
TUNED_BLADE = 15.25
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.42, speed=440, r=16, life=1.2, grav=0, dmgMul=0.6, fan=3, spread=0.28,
             spell="thornburst", tip="Throws a fan of three thorns · clankable")
CARD = "A pollen cloud drifts after the foe: inside it, entangle and bites"
ULT_NAME, ULT_KIND = "Bloom", "bloom"
# Design §5 and brief §0. `charge` is the lab's 16 in the game's clock (the
# batch's ruling, "use the game's equivalent"), measured for this fighter.
ULT = {"charge": 14, "dur": 8, "cloudR": 110, "drift": 90, "every": 0.4, "bite": 2.5, "stk": 1}
ULT_KEYS = list(ULT)
BLURB = ("A briar rod that throws its own thorns, three at a time. For eight seconds "
         "its pollen goes looking for you.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


# ---------------------------------------------------------------- stage 1 --
S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the verdant BOW
     body at the staff's blade -- which stage 2's fan is measured against.
'''

ULT_STUB = f'''    /* BLOOM. STUBBED AT `charge:1e9` IN STAGE 1 (the "OFF" every stubbed relic
       since v55b has used). `kind:"{ULT_KIND}"` is its own; the card is
       Cowork's (design §6), in at stage 1 so `tip_audit` measures the real
       line. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* BRIARWAND -- THE VERDANT STAFF, the staff row's second relic. Built from
     `06-docs/v93/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Verdant's status slows
     (entangle) and is worth most where it is CONTINUOUS -- so the spell lands
     many small hits and the ultimate keeps the foe entangled without having
     to land anything (design, "why this cell").

{S1_SHOT_PARA}
     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 16.5 on Chromium 141, and stage 5 settles it wide on 151. */
  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{BLADE}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ entangle:2 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [
("Briarwand joins the roster, its ultimate stubbed",
 '''

];
/* The single source of truth for "which status does this relic teach".''',
 relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".'''),
    ]


# ---------------------------------------------------------------- stage 2 --
S2_SHOT_PARA = '''     THE SPELL IS THORNBURST (design §1, §5): every 0.42s not one thorn but a
     FAN of three -- one along the facing and one either side at 0.28 rad --
     fast (440) and short-lived (life 1.2: they reach ~500 and stop), each 0.6
     of a blow, each that lands entangling 2. `fan`/`spread` are the only new
     fields and `tickFire` reads them (the volley loop's shape); `spawnShot`
     is untouched but for a `quiet` flag, so every other caller is the same
     call it always was. The first fan priced (0.45, life 0.8) was WORSE than
     the bow (design §3): this is the second, and it is the bow's equal.
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Briarwand looses the thorns",
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("tickFire looses a staff's fan",
 '''      f.ultNet.fired++;
      if (--f.ultNet.left <= 0) f.ultNet = null;
      return;
    }
    this.spawnShot(f);
  }
''',
 '''      f.ultNet.fired++;
      if (--f.ultNet.left <= 0) f.ultNet = null;
      return;
    }
    /* A STAFF'S FAN (v93, Briarwand's Thornburst): `fan` shots every cadence,
       the middle one along the facing and the rest at -spread, +spread,
       -2 spread ... in that order -- the lab's order (`overlays/staff_verdant.js`
       looses the middle thorn first). ONE loose voice a fan: the side shots are
       `quiet`, because three transients on one frame are one louder click
       (Thornshear's leaf volley found it first). Undefined `fan` on every other
       relic, so this is a comparison against undefined and falls through. */
    if (S.fan > 1){
      this.spawnShot(f);
      for (let k = 1; k < S.fan; k++)
        this.spawnShot(f, f.theta + S.spread * Math.ceil(k / 2) * (k % 2 ? -1 : 1), true);
      return;
    }
    this.spawnShot(f);
  }
'''),

("spawnShot takes a quiet flag",
 '''  spawnShot(f, angle){
''',
 '''  spawnShot(f, angle, quiet){
'''),

("  ...and a quiet shot makes no release sound",
 '''    SFX.play("loose", { bal: !!f.ultBal, spell: S.spell });
''',
 '''    if (!quiet) SFX.play("loose", { bal: !!f.ultBal, spell: S.spell });
'''),
    ]


# ---------------------------------------------------------------- stage 3 --
ULT_NOTE = '''    /* BLOOM (design §1, §5). A cloud of pollen leaves the staff (`cloudR`) and
       drifts after the foe at `drift` px/s for `dur` seconds; a foe inside it
       is bitten for `bite` and entangled +`stk` every `every` seconds. The
       DRIFT IS THE MECHANIC: a cloud that stays where it was cast holds the foe
       28% of the window against 57% and prices at +0 (design §3). The foe at
       ~3.7 of 4 entangle on the average window frame is the payload; the bite
       is the visible part of it.

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK: the lab's charge
       counts hit-stop freezes and the engine's does not (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v93/briarwand-build-v93.md`. Nothing waits. */
'''


def s3_edits(U: dict):
    return [
("Bloom is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Bloom's cloud",
 '''    this.ironfallFade = 0;
''',
 '''    this.ironfallFade = 0;
    /* {t, dur, x, y, next, bitten} while BLOOM's cloud is out (v93). NOT
       `ultBloom`, which is the Thicket's. null on every other relic and on this
       one outside its window: `tickPollen` returns after a two-iteration loop
       that does nothing. `pollenTally` is the probe's count; nothing in the
       simulation reads it. */
    this.ultPollen = null;
    this.pollenTally = null;
'''),

("the cast lets the cloud go and resolves nothing",
 '''    if (u.kind === "ironfall"){
''',
 '''    if (u.kind === "bloom"){
      /* BLOOM (v93). NOTHING RESOLVES HERE: the cloud leaves the caster's
         centre and `tickPollen` does the rest. `next` 0 makes the first bite
         free, as the lab's was (`nextTick = t` at its cast). `m.ultFx` carries
         the cast flash only (one slot: open item 25); the cloud is drawn off
         `f.ultPollen`. */
      f.ultPollen = { t: 0, dur: u.dur, x: f.x, y: f.y, next: 0, bitten: false };
      if (!f.pollenTally)
        f.pollenTally = { casts: 0, frames: 0, inFrames: 0, bites: 0, dealt: 0 };
      f.pollenTally.casts++;
      return;
    }
    if (u.kind === "ironfall"){
'''),

("the cloud drifts with the window tickers",
 '''    this.tickIronfall(dt);
''',
 '''    this.tickIronfall(dt);
    this.tickPollen(dt);                // BLOOM (v93): the cloud drifts and bites
'''),

("tickPollen drifts the cloud and bites",
 '''  /* ================================================== IRONFALL ========''',
 '''  /* ===================================================== BLOOM ========
     v93 §5, and the lab (`overlays/staff_verdant.js`) where the prose is
     silent. The cloud starts on the caster's centre and each step moves toward
     the foe by min(distance, drift * dt). It is CLAMPED TO THE INSET (§5:
     "walls do not stop it (it is clamped to the inset)"); the lab needed no
     clamp, because a cloud moving along the line to a foe inside the hall
     stays inside it -- except when the hall closes behind a lagging cloud.

     INSIDE is |foe - cloud| < cloudR + R. Every `every` seconds while the foe
     is inside -- the cooldown runs from the last bite, and the first bite of a
     cast is free -- the foe takes `bite` through `hurt` (ward first; no crit,
     no knock, no hit stop: "the bite is a tick") and `stk` entangle, its
     source a side letter (Fighter.apply's contract).

     BEATS (brief §1, rule 3). `hurt` is invisible to the director, so the
     FIRST bite of each cast files one `hit` beat, and a bite that KILLS files
     its own fatal one -- the engine's rule for every side-channel kill.

     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step, freezes included (the difference the charge carries).
     The cloud and its bite timer therefore hold still through a freeze, with
     the rest of the hall. */
  tickPollen(dt){
    for (const f of [this.a, this.b]){
      const P = f.ultPollen;
      if (!P) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultPollen = null; continue; }
      P.t += dt;
      if (P.t >= P.dur){ f.ultPollen = null; continue; }
      const u = f.w.ult, R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset;
      const dx = foe.x - P.x, dy = foe.y - P.y, l = Math.hypot(dx, dy) || 1;
      const st = Math.min(l, u.drift * dt);
      P.x = clamp(P.x + dx / l * st, n, A.w - n);
      P.y = clamp(P.y + dy / l * st, n, A.h - n);
      const T = f.pollenTally;
      T.frames++;
      if (Math.hypot(foe.x - P.x, foe.y - P.y) >= u.cloudR + R) continue;
      T.inFrames++;
      if (P.t < P.next) continue;
      P.next = P.t + u.every;
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.bite, f);
      foe.apply("entangle", u.stk, f === this.a ? "a" : "b");
      T.bites++; T.dealt += before - (foe.hp + foe.shield);
      const fatal = wasUp && foe.hp <= 0;
      if (fatal || !P.bitten)
        this.beat({ kind: "hit", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                    dmg: u.bite, crit: false, fatal,
                    hpAfter: Math.max(0, foe.hp), hpFrac: Math.max(0, foe.hp) / foe.maxHp,
                    maxHp: foe.maxHp, selfHpFrac: f.hp / f.maxHp,
                    spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy), bloom: true });
      P.bitten = true;
    }
  }

  /* ================================================== IRONFALL ========'''),

("the thorn and the cloud are drawn (first cuts)",
 '''      if (s.spell === "slug"){
''',
 '''      /* BRIARWAND'S THORN (v93 §6.1) -- FIRST CUT, for stage 3's film; the
         picture is stage 6's. "Three slim thorns (r 16, drawn long and narrow)
         fanning from the bud -- the fan IS the picture; at 1.2s they drop and
         fade." A thorn is drawn along its own heading, sinks and fades over its
         last quarter second, and borrows nothing from the arrow's streak.
         Derived from the shot's own state; no rng. */
      if (s.spell === "thornburst"){
        const fade = clamp(s.life / 0.25, 0, 1);
        const drop = (1 - fade) * 10;
        const L = s.r * 1.9, W = s.r * 0.26;
        c.save();
        c.translate(s.x, s.y + drop); c.rotate(s.a);
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = fade;
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.7);
        c.beginPath(); c.moveTo(L * 1.08, 0); c.lineTo(-L * 0.62, -W * 1.35); c.lineTo(-L * 0.62, W * 1.35); c.closePath(); c.fill();
        c.fillStyle = s.aff.core;
        c.beginPath(); c.moveTo(L, 0); c.lineTo(-L * 0.55, -W); c.lineTo(-L * 0.55, W); c.closePath(); c.fill();
        c.strokeStyle = s.aff.glow; c.lineWidth = 1;
        c.beginPath(); c.moveTo(-L * 0.5, 0); c.lineTo(L * 0.85, 0); c.stroke();
        c.restore();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 1;
        continue;
      }
      if (s.spell === "slug"){
'''),

("drawPollen: the cloud (first cut)",
 '''  drawShots(m){
''',
 '''  /* BLOOM'S CLOUD (v93 §6.1) -- FIRST CUT, for stage 3's film. "A soft disc
     r 110, verdant glow at alpha 0.22 with a brighter drifting inner texture
     (12 slow motes circling inside it), and it visibly leaves the caster and
     goes after the foe." Off `f.ultPollen` (the fighter's, never `m.ultFx`).
     No rng: the motes are `shellHash` and the window's own clock. */
  drawPollen(m){
    const c = this.ctx;
    for (const f of [m.a, m.b]){
      const P = f.ultPollen;
      if (!P) continue;
      const r = f.w.ult.cloudR, pal = f.aff;
      c.save();
      c.globalCompositeOperation = "lighter";
      const g = c.createRadialGradient(P.x, P.y, r * 0.15, P.x, P.y, r);
      g.addColorStop(0, pal.glow + "4D"); g.addColorStop(0.7, pal.core + "33"); g.addColorStop(1, pal.core + "00");
      c.fillStyle = g;
      c.beginPath(); c.arc(P.x, P.y, r, 0, TAU); c.fill();
      for (let i = 0; i < 12; i++){
        const a = TAU * shellHash(9701, i) + P.t * (0.35 + 0.3 * shellHash(9703, i)) * (i % 2 ? 1 : -1);
        const rr = r * (0.25 + 0.6 * shellHash(9705, i));
        c.globalAlpha = 0.55;
        c.fillStyle = i % 3 ? pal.glow : "#FFF7C8";
        c.beginPath(); c.arc(P.x + Math.cos(a) * rr, P.y + Math.sin(a) * rr, 2.6, 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  drawShots(m){
'''),

("drawPollen is drawn with the shots",
 '''    this.drawIronfall(m);        // IRONFALL on the staff (v96 §6.1)
''',
 '''    this.drawIronfall(m);        // IRONFALL on the staff (v96 §6.1)
    this.drawPollen(m);          // BLOOM's cloud (v93 §6.1)
'''),
    ]


# ---------------------------------------------------------------- stage 5 --
S1_BLADE_PARA = f'''     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 16.5 on Chromium 141, and stage 5 settles it wide on 151. */'''

S5_BLADE_PARA = f'''     `dmg` {fnum(TUNED_BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of every
     pairing, two seed blocks, 2100 fights a point, no bisection -- 14.75
     reads 45.7%, 15.0 48.5%, 15.25 50.1%, 15.5 51.8%. 1.25 UNDER THE
     DESIGN'S 16.5 BECAUSE THE PRICED LAB UNDER-FIRED THE FAN (it added the
     side thorns only when the middle one survived its first step); this is
     the fan §1 describes, and the blade pays for it. Provisional until the
     row re-prices (v89 §8.2). The number lives in
     `briarwand_build.TUNED_BLADE`. */'''


def s5_edits():
    b = BODY
    return [
("the relic's note says the blade is measured", S1_BLADE_PARA, S5_BLADE_PARA),
("Briarwand's blade is the measured one",
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:''',
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(TUNED_BLADE)}, spin:'''),
    ]


# THE PICKED VOICES, from briarwand_voice_lab.py (runs/build/stage6_voice_lab.json), verbatim.
VOICES = {
    'cast': '\n  S._sweep(t, { f0: 350, f1: 1400, q: 0.6, gain: 0.364, dur: 0.30, atk: 0.14, type:"bandpass" });\n  [0.22, 0.27, 0.31, 0.36, 0.40].forEach((d, i) =>\n    S._burst(t + d, { freq: 3200 + i * 300, q: 1.5, gain: 0.1092, dur: 0.05, type:"bandpass" }));',
    'rustle': '\n\n  S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.03674, dur: 0.40, atk: 0.20 });',
    'bite': '\n  const n = Math.max(1, Math.min(4, p.n | 0));\n  S._burst(t, { freq: 1700 + n * 220, q: 2.5, gain: 0.1214, dur: 0.03, type:"bandpass" });\n  S._tone (t, { freq: 620 + n * 90, to: 380 + n * 50, gain: 0.08094, dur: 0.05, type:"triangle" });',
    'close': '\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 1.0 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.0);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.6739 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.1);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.4541 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.2);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.306 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.3);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.2062 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.4);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.1389 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.5);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.0936 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.6);\n  (function(t){ S._sweep(t, { f0: 2600, f1: 3400, q: 0.9, gain: 0.0631 * 0.03674, dur: 0.40, atk: 0.20 }); })(t + 0.7);',
}
VOICE_PICKS = {'cast': 'EXHALE', 'rustle': 'LEAVES2', 'bite': 'SNAP', 'close': 'FADE'}
VOICE_GAPS = {'rustle': 0.1}


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule". PRESENTATION ONLY: SFX.play (a no-op headless),
# this.ring / this.float / statusTag (presentation lists), render-only fields,
# drawing code -- no rng, no spawnFx. engine_ab over all 36, Briarwand included,
# is the proof. The voices are `briarwand_voice_lab.py`'s picks (two rounds; the
# rustle had to OVERLAP to hold), pasted verbatim; `S` is the synth (each arm
# opens `const S = this;`, because the close strikes inside small functions,
# where `this` would not be the synth).
RUSTLE_GAP = VOICE_GAPS["rustle"]


def arm(key: str, indent: str) -> str:
    body = VOICES[key].strip("\n")
    lines = [indent + "const S = this;"] + [indent + (l[2:] if l.startswith("  ") else l) for l in body.splitlines()]
    return "\n".join(lines)


def s6_edits():
    s3 = {l: n for l, o, n in s3_edits(dict(ULT))}
    first_cut = s3["drawPollen: the cloud (first cut)"]
    return [

("Sfx: Bloom's cast, rustle, bite and close",
 '''        } else if (w === "culverin"){                   // the ratchet, then the boom
''',
 '''        } else if (w === "briarwand"){                  // the bud opens
          /* BLOOM'S CAST -- design §6.2: "a soft exhale into a rustle, 0.4s (the
             bud opening)." EXHALE (`briarwand_voice_lab.py`, Rick's "you pick
             i overrule"): a band of noise swelling up from 350 to 1400 Hz, then
             five rustles climbing -- 350 ms, 6 dB under a thorn's blow, its
             top 70 ms in (an exhale swells; it does not strike). Briarwand fell
             through to the shared rune-crack until now. */
''' + arm("cast", "          ") + '''
        } else if (w === "briarwand-rustle"){           // the cloud, holding
          /* THE CLOUD'S RUSTLE -- "a very quiet sustained rustle while the foe
             is inside it (peak <= 0.12)". LEAVES2 (round 2): one sweep
             2.6-3.4 kHz, re-struck by `tickPollen` every %GAP% s while the foe is
             inside, so the strikes OVERLAP -- round 1 struck every 0.25 s and
             every candidate pulsed by 33 dB or more, because every primitive
             here decays on an exponential ramp. Held, it flutters 7 dB, peaks
             at 0.045 and sits 20 dB under a thorn's blow. */
''' + arm("rustle", "          ") + '''
        } else if (w === "briarwand-bite"){             // a bite, pitched by the count
          /* A BITE -- "a short vegetable snap, pitched by entangle count".
             SNAP: a bandpassed crack and a falling triangle, 35 ms, 14 dB under
             a thorn's blow, rising 5.8 semitones from one stack to four.
             `p.n` is the foe's entangle stacks after the bite. */
''' + arm("bite", "          ") + '''
        } else if (w === "briarwand-close"){            // and the rustle goes
          /* CLOSE -- "the rustle fading": the rustle's own strike at its own
             gap, falling to -24 dB over 0.8 s. Played by `tickPollen` when the
             window runs out by its clock, never on a death. */
''' + arm("close", "          ") + '''
        } else if (w === "culverin"){                   // the ratchet, then the boom
'''.replace("%GAP%", fnum(RUSTLE_GAP))),

("the cloud carries its rustle's clock",
 '''      f.ultPollen = { t: 0, dur: u.dur, x: f.x, y: f.y, next: 0, bitten: false };
''',
 '''      f.ultPollen = { t: 0, dur: u.dur, x: f.x, y: f.y, next: 0, bitten: false, rs: 0 };
'''),

("tickPollen: the rustle, while the foe is inside",
 '''      T.inFrames++;
      if (P.t < P.next) continue;
''',
 '''      T.inFrames++;
      /* THE RUSTLE (design §6.2), re-struck every %GAP% s of the window while the
         foe is inside -- so the strikes overlap and it HOLDS. `rs` is its
         clock; nothing in the simulation reads it. */
      if (P.t >= P.rs){ P.rs = P.t + %GAP%; SFX.play("ult", { w: "briarwand-rustle" }); }
      if (P.t < P.next) continue;
'''.replace("%GAP%", fnum(RUSTLE_GAP))),

("tickPollen: a bite is heard, flashes and floats",
 '''      foe.apply("entangle", u.stk, f === this.a ? "a" : "b");
      T.bites++; T.dealt += before - (foe.hp + foe.shield);
''',
 '''      foe.apply("entangle", u.stk, f === this.a ? "a" : "b");
      T.bites++; T.dealt += before - (foe.hp + foe.shield);
      /* A BITE, SHOWN (design §6.1-6.2): the snap pitched by the foe's
         entangle count, a small green flash on the foe, the bite's number
         floating small, and the ENTANGLE tag on the cast's first bite (a tag
         every 0.4s would print a dozen over one window: Zenith's rule). All
         presentation: SFX.play, ring, float and statusTag draw no rng. */
      SFX.play("ult", { w: "briarwand-bite", n: foe.stacks("entangle") });
      this.ring(foe.x, foe.y, f.aff.glow, 30, 54, 0.30, 3);
      this.float(foe.x, foe.y - 44, u.bite, f.aff.glow, 20);
      if (!P.bitten && foe.hp > 0){
        const first = !this.taught.entangle && !!STATUS.entangle.tip;
        if (first) this.taught.entangle = true;
        this.statusTag(foe.x, foe.y, "entangle", first);
      }
'''),

("tickPollen: the close, when the window runs out by its clock",
 '''      if (P.t >= P.dur){ f.ultPollen = null; continue; }
      const u = f.w.ult, R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset;
''',
 '''      if (P.t >= P.dur){ SFX.play("ult", { w: "briarwand-close" }); f.ultPollen = null; continue; }
      const u = f.w.ult, R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset;
'''),

("tickPollen: the picture's clock and the cloud's last place",
 '''      P.bitten = true;
    }
  }
''',
 '''      P.bitten = true;
    }
    /* THE PICTURE'S CLOCK: 1 while the cloud is out, down over 0.5s after
       ("the cloud thins to nothing over 0.5s"), and where it was, so it thins
       where it stood. On the fighter; read by `drawPollen` alone. */
    for (const f of [this.a, this.b]){
      if (f.ultPollen){ f.pollenFade = 1; f.pollenX = f.ultPollen.x; f.pollenY = f.ultPollen.y; f.pollenAge = f.ultPollen.t; }
      else f.pollenFade = Math.max(0, f.pollenFade - dt / 0.5);
    }
  }
'''),

("the fighter carries the cloud's picture",
 '''    this.ultPollen = null;
    this.pollenTally = null;
''',
 '''    this.ultPollen = null;
    this.pollenTally = null;
    /* THE CLOUD'S PICTURE (v93 §6.1): its fade, where it last was, and the
       window's age for the head's opening. Render-only. */
    this.pollenFade = 0;
    this.pollenX = 0;
    this.pollenY = 0;
    this.pollenAge = 0;
'''),

("the staff's verdant head: Code's pick",
 '''pick: { bloodsworn:"A", umbral:"A", vigil:"A", verdant:"A", runic:"A", sanctified:"A", dwarven:"A" },''',
 '''pick: { bloodsworn:"A", umbral:"A", vigil:"A", verdant:"C", runic:"A", sanctified:"A", dwarven:"A" },'''),

("  ...and why",
 '''   spec's defaults until their own builds pick. */
''',
 '''   spec's defaults until their own builds pick. */
/* THE VERDANT HEAD IS "C" -- Code's pick for Briarwand under the same ruling:
   the open five-petal flower about a lit heart, because the ultimate is
   BLOOM and its pollen comes off a flower (design §6.1: "a bud at the head
   ... the bud opens"). A and B stay until Rick has seen it. */
'''),

("drawPollen: the cloud thins, the head opens, the pollen rises",
 first_cut,
 '''  /* BLOOM ON SCREEN (v93 §6.1). "Cast: the bud opens; a cloud detaches -- a
     soft disc r 110, verdant glow at alpha 0.22 with a brighter drifting
     inner texture (12 slow motes circling inside it), and it visibly leaves
     the caster and goes after the foe ... Close: the cloud thins to nothing
     over 0.5s. Field: pollen motes." DRAWN, not an fx.js field (the one
     `m.ultFx` slot is erased by the opponent's cast, and `src/render/fx.js`
     is shared by both chain lines) -- all of it off the fighter's own state.

     THE HEAD is the flower's heart, 0.81 of the drawn staff (1.7x the sim's
     L) out from the ball's edge -- where all three verdant candidates hold
     their light. For the first 0.4s of a window five petals open out of it.

     No rng: `shellHash` and the window's own clock. */
  drawPollen(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const k = f.pollenFade;
      if (!(k > 0.01)) continue;
      const r = f.w.ult.cloudR, pal = f.aff, T = f.pollenAge, x = f.pollenX, y = f.pollenY;
      c.save();
      c.globalCompositeOperation = "lighter";
      const g = c.createRadialGradient(x, y, r * 0.15, x, y, r);
      g.addColorStop(0, pal.glow + "4D"); g.addColorStop(0.7, pal.core + "33"); g.addColorStop(1, pal.core + "00");
      c.globalAlpha = k;
      c.fillStyle = g;
      c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
      for (let i = 0; i < 12; i++){
        const a = TAU * shellHash(9701, i) + T * (0.35 + 0.3 * shellHash(9703, i)) * (i % 2 ? 1 : -1);
        const rr = r * (0.25 + 0.6 * shellHash(9705, i));
        c.globalAlpha = 0.55 * k;
        c.fillStyle = i % 3 ? pal.glow : "#FFF7C8";
        c.beginPath(); c.arc(x + Math.cos(a) * rr, y + Math.sin(a) * rr, 2.6, 0, TAU); c.fill();
      }
      /* THE POLLEN RISING OFF IT: ten motes, drifting up and out of the cloud. */
      for (let i = 0; i < 10; i++){
        const ph = (T * (0.35 + 0.25 * shellHash(9711, i)) + shellHash(9713, i)) % 1;
        const px = x + (shellHash(9715, i) - 0.5) * r * 1.4 + Math.sin(T * 1.3 + i) * 6;
        const py = y + (shellHash(9717, i) - 0.3) * r * 0.8 - ph * 70;
        c.globalAlpha = 0.6 * k * Math.sin(ph * Math.PI);
        c.fillStyle = "#EFFFC4";
        c.beginPath(); c.arc(px, py, 2.4, 0, TAU); c.fill();
      }
      /* THE HEAD: a glow on the flower's heart while the window runs, and
         the petals opening out of it for the first 0.4s. */
      if (f.alive){
        const reach = f.w.reach * m.actMods.reach * f.reachMul;
        const hd = R - 6 + (reach + 6) * 1.7 * 0.81;
        const hx = f.x + Math.cos(f.theta) * hd, hy = f.y + Math.sin(f.theta) * hd;
        const hg = c.createRadialGradient(hx, hy, 1, hx, hy, 30);
        hg.addColorStop(0, pal.glow + "CC"); hg.addColorStop(1, pal.core + "00");
        c.globalAlpha = 0.7 * k;
        c.fillStyle = hg;
        c.beginPath(); c.arc(hx, hy, 30, 0, TAU); c.fill();
        if (f.ultPollen && T < 0.4){
          const o = T / 0.4;
          c.globalAlpha = 0.8 * (1 - o);
          c.fillStyle = pal.glow;
          for (let i = 0; i < 5; i++){
            const a = f.theta + i * TAU / 5, d = 8 + 34 * o;
            c.beginPath(); c.ellipse(hx + Math.cos(a) * d, hy + Math.sin(a) * d, 9, 4.5, a, 0, TAU); c.fill();
          }
        }
      }
      c.restore();
    }
  }

  drawShots(m){
'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        if "pollenFade" in code:
            return 6
        return 5 if f"dmg:{fnum(TUNED_BLADE)}," in ent else 3
    return 2 if "fan:3" in ent else 1


def all_stages():
    st = [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("5", s5_edits())]
    if "s6_edits" in globals():
        st.append(("6", s6_edits()))
    return st


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"])
    ap.add_argument("--src")
    ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nBRIARWAND / BLOOM -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nBRIARWAND / BLOOM -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"culverin"' not in code or "drawIronfall(m){" not in code:
        raise SystemExit("wrong base: no Culverin stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin stages 1-6 in it")
    have = stage_of(code)
    prev = {1: 0, 2: 1, 3: 2, 5: 3, 6: 5}[stage]
    if have != prev:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built on stage {prev}")
    if stage == 1:
        check_bow_body(code)
        edits = s1_edits()
    elif stage == 2:
        dmg = re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1)
        edits = s2_edits(dmg)
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
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickPollen(dt){", "this.tickPollen(dt);", 'u.kind === "bloom"', "drawPollen(m){"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        if 'kind:"bloom"' in out and out.count('kind:"bloom"') != 1:
            raise SystemExit("REFUSING TO WRITE -- more than one bloom ultimate")
        if "ultPollen" not in out:
            raise SystemExit("REFUSING TO WRITE -- no ultPollen")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    if stage >= 2 and out.count("if (S.fan > 1){") != 1:
        raise SystemExit("REFUSING TO WRITE -- the fan loop is not there exactly once")
    if stage >= 6:
        for w in ("briarwand", "briarwand-rustle", "briarwand-bite", "briarwand-close"):
            if out.count(f'w === "{w}"') != 1:
                raise SystemExit(f"REFUSING TO WRITE -- the {w} voice arm is not there exactly once")
        for key in VOICES:
            eng = strip_comments(arm(key, "")).split()
            if " ".join(eng) not in " ".join(out.split()):
                raise SystemExit(f"REFUSING TO WRITE -- the {key} voice shipped is not the picked body")
        if 'verdant:"C"' not in out or "pollenFade" not in out:
            raise SystemExit("REFUSING TO WRITE -- the head's pick or the cloud's fade is missing")
        print("  ok    voices  " + ", ".join(f"{k} {VOICE_PICKS[k]}" for k in VOICES)
              + f"  (the rustle re-struck every {RUSTLE_GAP} s) -- every arm the picked body")
    check_no_rng(edits)
    if out.count('shape:"staff"') != 2:
        raise SystemExit("REFUSING TO WRITE -- expected exactly two staves in the roster")
    print(f"  ok    relic  shape staff, the bow's body, "
          f"{'the thorns' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    two staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    print("\n  GATE -- in this order, and each can fail:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <the 35> --n 10")
    print(f"    python briarwand_probe.py --game {A.out}")
    print(f"    python verify.py --game {A.out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
