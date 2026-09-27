#!/usr/bin/env python
"""MORNINGSTAR / ZENITH -- the sanctified flail, a NEW relic. v98.

Built from `06-docs/v71/MORNINGSTAR-BUILD-BRIEF.md` and
`sanctified-flail-design-v71.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-morningstar.html
    stage 2   the light and the smite     -> sc-sun.html      (arm B)
    stage 3   the burn                    -> sc-burn.html     (arm C)
    stage 4   the heal                    -> sc-zenith.html   (arm D)
    stage 5   the blade                   confirm 24.03 wide on 151 (no link unless it moves)
    stage 6   picture, voice              -> sc-zenith-fx.html (no field: drawn embers, v98 §4)

§1 (the brief's §0): "For a duration the flail's head becomes a sun. An enemy
in its light is smitten and burned for as long as it stays there, and every
burn heals the one swinging it. The head still hits like a flail head."

Declared (design §5, brief §0-§1): the light is a disc of radius 100 on the
flail HEAD; the foe is lit when its centre is within 100 + R. A tick every
0.4s while lit: `hurt(foe, 3, f)` (ward first, nothing else), smite +1, then
blessing +1 on the caster. Blessing heals through the existing `tickStatus`
branch. No `resolveHit` change, no stun, no pin, no knock.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter the engine's clock runs 0.897 of the lab's (the lab's 16 =
the engine's ~14.35), so 14.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE TICK'S ORDER is the prose's: hurt, then smite, then blessing (the lab
     does smite first; no fight can tell).
  2. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract). Smite ticks
     damage, and its fatal DOT beat is attributed by that letter.
  3. THE TICK THAT KILLS files its own fatal hit beat (the engine's rule for a
     side-channel kill); no other tick files one.
  4. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab lights only
     `foe`; Corollary's reading 3).
  5. THE CADENCE is the lab's: a 0.4s cooldown running through the whole
     window, firing on the first lit frame it is clear.
  6. THE BLESSING is per TICK and unconditional on damage dealt (§5 as
     written), so a tick a ward swallows still blesses.

THE CLOCK. The window and the cooldown run on the window tickers' clock, which
stops through a hit stop (Corollary's and Daybreak's convention).

THE BASE is the chain tip, `sc-daybreak-fx.html`, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "morningstar"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling)
    "dur": 8,         # "the window 8s"
    "r": 100,         # "disc radius 100 on the HEAD"
    "tick": 0.4,      # "every 0.4s while lit"
    "smite": 1,       # "smite +1"
    "tickDmg": 3,     # "hurt 3" -- stage 3
    "bless": 1,       # "then blessing +1 on the caster" -- stage 4
}
TIP = "The head becomes a sun: its light smites foes, and each burn heals it"
# Gravemourn's flail profile, the lab's donor (cell_ults_on.TYPE_DONOR), and
# the type's own blade: "24.03 -- UNCHANGED".
PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:24.03, spin:2.2, '
        'mode:"chain", mass:3.6')
BLURB = ("A flail whose head becomes a sun: its light smites and burns, and "
         "every burn heals the one swinging it.")


def ult_block(charge, tick_dmg: int, bless: int) -> str:
    return (f'''    ult:{{ name:"Zenith", charge:{charge}, kind:"sun", dur:{ULT["dur"]},
          r:{ULT["r"]}, tick:{ULT["tick"]}, smite:{ULT["smite"]},
          tickDmg:{tick_dmg},        // v71: the burn (stage 3)
          bless:{bless},          // v71: the heal (stage 4)
          tip:"{TIP}" }},''')


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 "parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip()
                                               .splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


# ---------------------------------------------------------------- stage 1 --
# THE RELIC, APPENDED AFTER STARWARDEN, ITS ULTIMATE STUBBED at charge 1e9 (the
# clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back.
ROW_ANCHOR = ('''    blurb:"A ring of light worn like a sash, and a star at the heart of it. Whatever touches either one goes on burning." },

];''')

S1 = [

("morningstar joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* MORNINGSTAR / ZENITH (v71; built v98) -- THE SANCTIFIED FLAIL, the 35th
     relic built. Gravemourn's flail profile and the type's own blade, 24.03
     (the lab's donor; "UNCHANGED"), and the school's channel, onHit smite.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its light,
     its burn and its heal, one number at a time. */
  {{ id:"morningstar", name:"Morningstar", aff:"sanctified", shape:"flail",
    {PHYS},
    onHit:{{ smite:1 }},
{ult_block("1e9", 0, 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the sun has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Zenith", charge:1e9, kind:"sun", dur:8,
''',
 f'''    ult:{{ name:"Zenith", charge:{ULT["charge"]}, kind:"sun", dur:{ULT["dur"]},   // v71 stage 2: the sun lights
'''),

("the fighter carries the sun's window",
 '''    this.ultDawn = null;
    this.dawnTally = null;
''',
 '''    this.ultDawn = null;
    this.dawnTally = null;
    /* {t, dur, cd} while ZENITH's sun burns on the flail head (v71). null on
       every other relic and on this one outside its window: `tickSun` returns
       after a two-iteration loop that does nothing. `sunTally` is the probe's
       count, cumulative over the fight; nothing in the simulation reads it. */
    this.ultSun = null;
    this.sunTally = null;
'''),

("the cast lights the sun and resolves nothing",
 '''    if (u.kind === "dawn"){
''',
 '''    if (u.kind === "sun"){
      /* ZENITH (v71). NOTHING RESOLVES HERE: the cast turns the flail's head
         into a sun for `u.dur` seconds, and `tickSun` does everything the
         window does. `cd` starts at zero, so a foe already in the light is
         struck on the first frame. */
      f.ultSun = { t: 0, dur: u.dur, cd: 0 };
      if (!f.sunTally)
        f.sunTally = { casts: 0, ticks: 0, dealt: 0, bless: 0,
                       litFrames: 0, frames: 0 };
      f.sunTally.casts++;
      return;
    }
    if (u.kind === "dawn"){
'''),

("the sun ticks with the window tickers",
 '''    this.tickDawn(dt);                  // DAYBREAK (v86)
''',
 '''    this.tickDawn(dt);                  // DAYBREAK (v86)
    this.tickSun(dt);                   // ZENITH (v71)
'''),

("tickSun burns in the light of the head",
 '''  tickWinnow(dt){
''',
 '''  /* =================================================== THE SUN ========
     v71 §5 / brief §0: while the window runs the flail's HEAD is a sun of
     radius `r`. A foe whose centre is within `r` + R of the head is lit, and
     every `tick` seconds while lit: `hurt(foe, tickDmg, f)` -- ward first and
     NOTHING ELSE: no crit, no knock, no hit stop, no hitstun -- then smite
     +`smite`, then blessing +`bless` on the caster (it heals through
     tickStatus). No beat, except the tick that KILLS, which files its own
     (the engine's rule for a side-channel kill).

     The HEAD is `f.headX/Y`, which tickWeapon moved earlier this step, so the
     light is tested where the head is now. The target is the OPPONENT only.
     THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, lit or not, and a tick fires
     on the first lit frame it is clear (the lab's cadence, and what was
     priced). On the window tickers' clock, so it freezes through a hit stop.
     `apply`'s source is a side letter (Fighter.apply's contract). */
  tickSun(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultSun;
      if (!Z) continue;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }
      const u = f.w.ult, T = f.sunTally;
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      Z.cd -= dt;
      T.frames++;
      if (!foe.alive
          || !(Math.hypot(foe.x - f.headX, foe.y - f.headY) < u.r + R)) continue;
      T.litFrames++;
      if (Z.cd > 0) continue;
      Z.cd = u.tick;
      T.ticks++;
      const side = f === this.a ? "a" : "b";
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.tickDmg, f);
      T.dealt += before - (foe.hp + foe.shield);
      foe.apply("smite", u.smite, side);
      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }
      if (wasUp && foe.hp <= 0)
        this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                    x: foe.x, y: foe.y, dmg: u.tickDmg, crit: false,
                    fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                    selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                    ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                    shotSpd0: 0, sun: true });
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the burn",
 '''          tickDmg:0,        // v71: the burn (stage 3)
''',
 f'''          tickDmg:{ULT["tickDmg"]},        // v71: the burn (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the heal",
 '''          bless:0,          // v71: the heal (stage 4)
''',
 f'''          bless:{ULT["bless"]},          // v71: the heal (stage 4)
'''),
]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v71 §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule" by `zenith_voice_lab.py` and the picture lab
# (v98 §4). Presentation only: engine_ab over all 35 relics, Morningstar
# included, is the proof. The tick's voice row and its picture row share the
# blessing line and are merged into one edit.
S6 = [

("Sfx: Zenith's cast, tick and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "morningstar"){                // the sun comes up
          /* ZENITH'S CAST -- v71 §6.2: "a bright swell, 0.5s, a rising fifth
             in a sustained-by-restrike tone -- the sun coming up". STEP, of
             four, picked on the numbers by `zenith_voice_lab.py` under Rick's
             "you pick i overrule" (v98). Morningstar had no arm and fell
             through to rune-crack, which Lastlight, Aureole and Censer still
             use, so this ADDS arms before that fallback and leaves it alone.

             D5 -> A5, a just fifth (iv -> i of the score's A minor): the root
             re-struck for the first half and the fifth for the second, in a
             triangle with a sine an octave over it at 0.4 -- bright, centroid
             1064 Hz against Daybreak's line's 542. It swells 11.9 dB, tops out
             495 ms after the cast at -2.9 dB re Morningstar's own blow (the
             hit at 24), and is gone by 695 ms. Register 0.45 against
             rune-crack, 0.39 against Corollary's BAR, 0.09 against Daybreak's
             cast.

             A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md 4.5), so
             each degree is RE-STRUCK every whole number of cycles nearest 11
             ms, in phase, each strike 0.25 s long, the level climbing in a
             straight line in dB; a degree's first strike carries 0.6 of the
             plateau. At half the strikes (22 ms) the re-strikes read as a 3.4
             dB flutter. `.frequency.value = f` AFTER `_tone` IS LOAD-BEARING
             (v97 §4b): without it the strikes land out of phase above ~500 Hz
             -- the lab's RAW control dips 2 times on the way up and tops out
             3.7 dB lower. */
          const f0 = 440 * Math.pow(2, 5 / 12), f1 = f0 * 1.5, g = 0.02736, sw = 18.47;
          const L = 0.5, lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);
          for (const [f, s0, s1] of [[f0, 0, L / 2], [f1, L / 2, L]]){
            const dt = Math.max(1, Math.round(f * 0.011)) / f;
            const q = Math.pow(0.0001 / lv(s0), dt / 0.25);
            for (let k = 0; s0 + k * dt < s1 - 1e-9; k++){
              const s = s0 + k * dt, gs = lv(s);
              const a = k ? gs : Math.max(gs, gs * 0.6 / (1 - q));
              this._tone(t + s, { freq: f, gain: a, dur: 0.25, type:"triangle" }).frequency.value = f;
              this._tone(t + s, { freq: 2 * f, gain: a * 0.4, dur: 0.25, type:"sine" }).frequency.value = 2 * f;
            }
          }
        } else if (w === "morningstar-tick"){           // the light lands
          /* A TICK -- "a soft chime, 60ms, quiet (peak <=0.35), pitch by smite
             count" (v71 §6.2). SOFT, of four (`zenith_voice_lab.py`): a struck
             bar with its top mode off and the second at 0.25. `tickSun` plays
             it once per tick with n = the foe's smite stacks after the tick
             (1-4; every count 0-4 is its own note of the A-minor pentatonic
             from C7: 2093-2349-2637-3136-3520 Hz).

             Audible 55 ms, peak 0.205 at most, -10.9 dB re the blow and +10.8
             dB re the wall tick. It lands on the same frame as the heal -- the
             unchanged `spark` collect, 1.3-1.7 kHz -- and sits above it:
             register 0.24 at most against any heal, and each keeps its own
             band within 0.2 dB when the two land together. */
          const n = Math.max(0, Math.min(4, p.n | 0));
          const f = 440 * Math.pow(2, ([0, 2, 4, 7, 9][n] + 27) / 12);
          [[1, 1.00], [2.76, 0.25]].forEach(([r, k]) =>
            this._tone(t, { freq: f * r, gain: 0.1106 * k, dur: 0.092, type:"triangle" }));
        } else if (w === "morningstar-close"){          // and it sets
          /* CLOSE -- "the swell reversed, quiet" (v71 §6.2). MIRROR, of four
             (`zenith_voice_lab.py`): the cast's own figure run backwards, the
             fifth first and falling to the root, the level falling from the
             top, after a 0.17 s climb that is the cast's own release reversed.
             -9.0 dB under the cast's top; gone 900 ms after the window shuts.
             Envelope correlation 0.90 with the literal reversal, which cannot
             ship: it needs an async render, and every clip rebuilds this synth
             synchronously (v88 §6b). `tickSun` plays it only when the window
             closes by its clock, never on a death. */
          const f0 = 440 * Math.pow(2, 5 / 12), f1 = f0 * 1.5;
          const L = 0.5, R = 0.17, top = 0.02736 * 0.289, sw = 18.47;
          const lv = (s) => s < R ? top * Math.pow(10, -30 * (1 - s / R) / 20)
                                  : top * Math.pow(10, -sw * (s - R) / L / 20);
          for (const [f, s0, s1] of [[f1, 0, R + L / 2], [f0, R + L / 2, R + L]]){
            const dt = Math.max(1, Math.round(f * 0.011)) / f;
            const q = Math.pow(0.0001 / lv(s0), dt / 0.25);
            for (let k = 0; s0 + k * dt < s1 - 1e-9; k++){
              const s = s0 + k * dt, gs = lv(s);
              const a = k ? gs : Math.max(gs, gs * 0.6 / (1 - q));
              this._tone(t + s, { freq: f, gain: a, dur: 0.25, type:"triangle" }).frequency.value = f;
              this._tone(t + s, { freq: 2 * f, gain: a * 0.4, dur: 0.25, type:"sine" }).frequency.value = 2 * f;
            }
          }
        } else {                                        // rune-crack'''),

('tickSun: the close, when the window runs out by its clock with the caster alive',
 '''      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }''',
 '''      /* ZENITH'S CLOSE (v71 §6.2: "the swell reversed, quiet"): on the frame
         the window runs out BY ITS CLOCK with the caster alive -- never on a
         death, and never once the fight is over, because step() stops calling
         this. Presentation only: SFX.play draws nothing, is a no-op headless,
         and nothing here is read back (zenith_voice_lab: fights identical). */
      if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "morningstar-close" });
      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }'''),

("the tick: its chime, the heal's voice and its picture (voice + picture rows, merged)",
 '''      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }
''',
 '''      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }
      /* ZENITH'S TICK AND HEAL (v71 §6.2), once per tick, after both applies:
         the chime pitched by the foe's smite stacks, and the heal is the
         EXISTING spark-collect voice pitched by the caster's blessing stacks,
         called exactly as Lastlight calls it. Plain-number opts; SFX.play is a
         no-op headless and reads nothing back (zenith_voice_lab: fights
         identical with and without these two lines). */
      SFX.play("ult", { w: "morningstar-tick", n: foe.stacks("smite") });
      if (u.bless > 0) SFX.play("spark", { collect: true, n: f.stacks("blessing") });
      this.sunShown(f, foe);                   // the picture's (v71 section 6.1)
'''),

('zenith picture: fighter fields',
 '''    this.ultSun = null;
    this.sunTally = null;
''',
 '''    this.ultSun = null;
    this.sunTally = null;
    /* ZENITH'S PICTURE (v71 section 6.1), and none of it is the window: the
       sun outlives `ultSun` by the 0.3s its ring takes to contract into the
       head, so the picture keeps its own state. On the FIGHTER and never on
       `m.ultFx` (one slot, and the opponent's cast takes it: open item 25).
       Driven in `tickPresentation`, except `sunTagged`, which `sunShown`
       sets; nothing in the simulation reads any of it.
         sunFade     1 while the sun burns; eased to 0 over 0.3s after the
                     window closes, the caster falls, or the match ends
         sunAge      the presentation clock since the cast (the ignition)
         sunLitFade  the lit foe's rim of light, up while it is in the sun
         sunTagged   this lit stretch has had its SMITE and BLESSING tags */
    this.sunFade = 0;
    this.sunAge = 0;
    this.sunLitFade = 0;
    this.sunTagged = false;
'''),

("zenith picture: the match's tick records",
 '''    this.echoFx = [];
''',
 '''    this.echoFx = [];
    /* AND ZENITH'S TICKS: the spark-fall onto the foe and the gold thread back
       to the caster, one record a tick. Pushed by `sunShown` (tickSun's one
       call into the picture), aged in `tickPresentation`, drawn by `drawSun`
       and `drawSunTop`. A RECORD, NOT A PARTICLE FIELD, and not `m.ultFx`.
       Nothing in the simulation reads it. */
    this.sunFx = [];
'''),

('zenith picture: sunShown',
 '''  /* =================================================== THE SUN ========''',
 '''  /* ZENITH'S TICK, SHOWN (v71 section 6.1). Called once from `tickSun`, after
     the tick has resolved and before a fatal beat, and changes none of it.
     It files the tick's picture record (the spark-fall and the thread), and
     on the FIRST tick of each lit stretch it tags the foe SMITE and the
     caster BLESSING -- Corona's and Daybreak's rule: at 2.5 ticks a second a
     tag a tick would print a dozen of each over one window. The ball draws
     its own smite count (`_stSmite`). `tickPresentation` re-arms the flag on
     the first frame the foe is out of the light.

     PRESENTATION ONLY. `sunFx`, the flag, `tags` and `taught` are read by
     nothing in the simulation; no rng, no spawnFx. */
  sunShown(f, foe){
    const X = this.sunFx;
    X.push({ f, foe, t: 0, life: 0.6, n: f.sunTally.ticks });
    if (X.length > 8) X.shift();
    if (f.sunTagged || !(foe.hp > 0)) return;  // the killing tick: the shatter says it
    f.sunTagged = true;
    const fs = !this.taught.smite && !!STATUS.smite.tip;
    if (fs) this.taught.smite = true;
    this.statusTag(foe.x, foe.y, "smite", fs);
    const fb = !this.taught.blessing && !!STATUS.blessing.tip;
    if (fb) this.taught.blessing = true;
    this.statusTag(f.x, f.y, "blessing", fb);
  }

  /* =================================================== THE SUN ========'''),

('zenith picture: its clocks in tickPresentation',
 '''          f.dawnLitFade = Math.max(0, f.dawnLitFade - dt / 0.7);
          f.dawnAge += dt;
        }
      }
''',
 '''          f.dawnLitFade = Math.max(0, f.dawnLitFade - dt / 0.7);
          f.dawnAge += dt;
        }
      }
      /* AND THE SUN'S. Every `life` in this method is in HALF-SECONDS (it runs
         twice a normal step): 0.5 is the cast's 0.25s ignition (read off
         `sunAge` by the draw) and 0.6 the close's 0.3s contraction. Through a
         hit stop the window's clock stops and this one keeps playing, so the
         sun stays lit and its embers keep rising. Not after the match:
         `tickSun` never runs again once `over` is set, so a window open at the
         kill would otherwise burn through the whole verdict. The lit test is
         `tickSun`'s own, so the picture is where the light is. */
      { const Z = this.over ? null : f.ultSun;
        if (Z){
          if (!(f.sunFade > 0)) f.sunAge = 0;               // a new sun
          f.sunFade = 1;
          f.sunAge += dt;
        } else if (f.sunFade > 0){
          f.sunFade = Math.max(0, f.sunFade - dt / 0.6);
          f.sunAge += dt;
        }
        const foe = f === this.a ? this.b : this.a;
        const lit = !!Z && foe.alive && Math.hypot(foe.x - f.headX, foe.y - f.headY)
                    < f.w.ult.r + CONFIG.physics.ballR;
        if (!lit) f.sunTagged = false;
        if (lit || f.sunLitFade > 0)
          f.sunLitFade = lit ? Math.min(1, f.sunLitFade + dt / 0.2)
                             : Math.max(0, f.sunLitFade - dt / 0.5);
      }
'''),

('zenith picture: the tick records age',
 '''    for (let i = this.echoFx.length - 1; i >= 0; i--){
      const e = this.echoFx[i];
      e.t += dt;
      if (e.t >= e.life) this.echoFx.splice(i, 1);
    }
''',
 '''    for (let i = this.echoFx.length - 1; i >= 0; i--){
      const e = this.echoFx[i];
      e.t += dt;
      if (e.t >= e.life) this.echoFx.splice(i, 1);
    }
    /* ZENITH'S TICK RECORDS, on the same clock (half-seconds: 0.6 is the
       0.3s spark-fall, the thread's 0.15s is 0.3 of it). A killing tick's
       thread still plays under the verdict (its sparks do not: the shatter
       owns that foe); the list is empty 0.3s after the last tick, so nothing
       needs clearing at the end. */
    for (let i = this.sunFx.length - 1; i >= 0; i--){
      const e = this.sunFx[i];
      e.t += dt;
      if (e.t >= e.life) this.sunFx.splice(i, 1);
    }
'''),

('zenith picture: the floor call (world pass, under both balls)',
 '''    if (__world) this.drawDawn(m);
''',
 '''    if (__world) this.drawDawn(m);
    /* ZENITH'S SUN, ON THE FLOOR: the ring, its rays, the lit ground inside it,
       the embers, the lit foe's rim and the tick's thread. The WORLD pass and
       under both balls -- the ring runs through the caster's own shell (the
       head swings at ~96 from it and the ring is 100 round the head), and
       CLAUDE.md section 4.1b: a light drawn over a near-white body erases it. */
    if (__world) this.drawSun(m);
'''),

('zenith picture: the top call (over both fighters)',
 '''    this.drawEcho(m);
''',
 '''    /* ZENITH'S CORE AND ITS SPARKS, OVER BOTH FIGHTERS: the core sits ON the
       head and the sparks land ON the foe. Light, so this pass: the hot core
       is what the bloom makes a sun of (measured under the gate). */
    this.drawSunTop(m);
    this.drawEcho(m);
'''),

('zenith picture: drawSun and drawSunTop',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------------- THE SUN ---
     ZENITH (v71 section 6.1). For the window the flail's head is a sun, and
     the sun is a RING, not a disc: a 10-unit band at 0.35 at the light's own
     radius (`u.r`, where `tickSun` tests), the hole cut in the path, the
     ground inside it lit at <= 0.05, and eight rays from a hot core on the head
     out to the band, turning with the head's tumble. SUNLIGHT, NOT WHITE --
     Rick on Daybreak's clip, 2026-09-27: "more like sunlight glowing rather
     than the dull white": gold with a hot heart, embers that cool as they
     rise. It ignites over 0.25s (the ring grows out of the head) and at the
     close it contracts back into the head over 0.3s and the head cools.

     WHAT IT DOES, SHOWN ONCE A TICK: four sparks fall onto the foe, and a
     gold thread runs from the foe back to the caster for 0.15s -- the burn,
     and the heal it pays. A foe in the light wears a rim of it.

     IT HANGS OFF THE FIGHTER (`sunFade`, `sunAge`, `sunLitFade`) and the
     match's tick records (`sunFx`), never `m.ultFx`: one slot, and the
     opponent's cast takes it (open item 25).

     TWO PASSES. `drawSun` is the WORLD pass under both balls, so every
     shell is painted over it -- the old Daybreak drew a white corona under
     `lighter` over a 0.89-luma body and ERASED it (CLAUDE.md section 4.1b), and
     this ring runs through the caster's own shell. `drawSunTop` draws the
     core ON the head and the sparks ON the foe, over both fighters.

     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- the embers and
     sparks are shellHash against the match clock (and the death clock after
     the kill) -- and nothing here writes a field the simulation reads. */
  drawSun(m){
    const a = m.a, b = m.b, X = m.sunFx;
    if (!(a.sunFade > 0) && !(b.sunFade > 0) && !(X && X.length)) return;   // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR, T = m.t + (m.deathAge || 0);
    c.save();
    const n = m.inset || 0;                                  // the live hall only
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    for (const f of [a, b]){
      const fade = f.sunFade;
      if (!(fade > 0)) continue;
      const hx = f.headX, hy = f.headY;
      const s = Math.min(1, f.sunAge / 0.5);                 // half-seconds
      const kI = 1 - (1 - s) * (1 - s);                        // ignition, eased out
      const k = Math.min(kI, 1 - (1 - fade) * (1 - fade));     // and the close
      const rr = f.w.ult.r * k, hw = 10 / 2;
      const on = Math.min(1, s * 3) * Math.min(1, fade * 2);
      /* THE LIT GROUND: the inside of the sun, <= 0.05 at the head and half
         that at the band. Enough to say "this is lit", not enough to be a disc. */
      if (rr > hw + 2){
        const g = c.createRadialGradient(hx, hy, 0, hx, hy, rr - hw);
        g.addColorStop(0, "rgba(255,212,120," + (0.05 * on).toFixed(3) + ")");
        g.addColorStop(1, "rgba(255,190,90," + (0.05 * 0.5 * on).toFixed(3) + ")");
        c.fillStyle = g;
        c.beginPath(); c.arc(hx, hy, rr - hw, 0, TAU); c.fill();
      }
      /* EIGHT RAYS from the core to the ring, turning with the head's tumble
         (`headSpin`). One path, one gradient: hot at the core, gone at the band. */
      const rc = 12 + 2, re = rr - hw - 1;
      if (re > rc + 4){
        const g = c.createRadialGradient(hx, hy, rc, hx, hy, re);
        g.addColorStop(0, "rgba(255,236,170," + (0.3 * on).toFixed(3) + ")");
        g.addColorStop(0.55, "rgba(255,196,74," + (0.3 * 0.45 * on).toFixed(3) + ")");
        g.addColorStop(1, "rgba(255,170,50,0)");
        c.fillStyle = g;
        c.beginPath();
        for (let i = 0; i < 8; i++){
          const q = f.headSpin + i * TAU / 8, cq = Math.cos(q), sq = Math.sin(q);
          c.moveTo(hx + cq * rc - sq * 2.2, hy + sq * rc + cq * 2.2);
          c.lineTo(hx + cq * re, hy + sq * re);
          c.lineTo(hx + cq * rc + sq * 2.2, hy + sq * rc - cq * 2.2);
          c.closePath();
        }
        c.fill();
      }
      /* THE RING: a 10-unit band at 0.35, WITH THE HOLE CUT IN THE PATH (a
         radial gradient with an inner radius still fills its inner circle
         with colorStop(0) -- CLAUDE.md section 4.1b). Sunlight, not white: gold
         at the edges and a hot line at its heart, then a drawn glow outside it
         that the bloom never sees. */
      { const r0 = Math.max(0, rr - hw), r1 = rr + hw, A = 0.35 * on;
        const g = c.createRadialGradient(hx, hy, r0, hx, hy, r1);
        g.addColorStop(0, "rgba(255,168,48," + (A * 0.35).toFixed(3) + ")");
        g.addColorStop(0.3, "rgba(255,200,84," + (A * 0.85).toFixed(3) + ")");
        g.addColorStop(0.5, "rgba(255,240,186," + A.toFixed(3) + ")");
        g.addColorStop(0.7, "rgba(255,200,84," + (A * 0.85).toFixed(3) + ")");
        g.addColorStop(1, "rgba(255,168,48," + (A * 0.35).toFixed(3) + ")");
        c.fillStyle = g;
        c.beginPath();
        c.arc(hx, hy, r1, 0, TAU);
        if (r0 > 0) c.arc(hx, hy, r0, TAU, 0, true);         // the hole
        c.fill();
        const r2 = r1 + 8 * k;
        const h = c.createRadialGradient(hx, hy, r1, hx, hy, r2);
        h.addColorStop(0, "rgba(255,176,56," + (0.1 * on).toFixed(3) + ")");
        h.addColorStop(1, "rgba(255,150,40,0)");
        c.fillStyle = h;
        c.beginPath();
        c.arc(hx, hy, r2, 0, TAU);
        c.arc(hx, hy, r1, TAU, 0, true);
        c.fill();
      }
      /* THE EMBERS (the design's ember-mote field, drawn: the one ultFx slot
         fires a field once, at the cast, where the caster stood). Born on the
         band, rising and cooling -- hot, gold, ember -- off pure time. */
      for (let i = 0; i < 20; i++){
        const ph = (T * (0.45 + 0.35 * shellHash(9201, i)) + shellHash(9203, i)) % 1;
        const q = TAU * shellHash(9205, i);
        const r0 = rr + (shellHash(9207, i) - 0.5) * 10;
        const mx = hx + Math.cos(q) * r0 + Math.sin(T * 1.7 + i * 2.3) * 3;
        const my = hy + Math.sin(q) * r0 - ph * 38;
        c.globalAlpha = 0.75 * on * Math.sin(ph * Math.PI);
        c.fillStyle = ph < 0.3 ? "#FFE9A8" : (ph < 0.65 ? "#FFB547" : "#E0761C");
        c.beginPath();
        c.arc(mx, my, 1.7 * (1 - 0.45 * ph) * (0.7 + 0.6 * shellHash(9209, i)), 0, TAU);
        c.fill();
      }
      c.globalAlpha = 1;
      /* THE LIT FOE: a rim of sunlight round its shell while it stands in the
         light. Drawn here, under the ball, so the shell covers its inside:
         it can only ever be a rim. */
      const foe = f === a ? b : a, L = f.sunLitFade * on;
      if (L > 0.01 && foe.alive){
        const g = c.createRadialGradient(foe.x, foe.y, R, foe.x, foe.y, R + 8);
        g.addColorStop(0, "rgba(255,214,110," + (0.6 * L).toFixed(3) + ")");
        g.addColorStop(1, "rgba(255,170,50,0)");
        c.fillStyle = g;
        c.beginPath();
        c.arc(foe.x, foe.y, R + 8, 0, TAU);
        c.arc(foe.x, foe.y, R - 1, TAU, 0, true);
        c.fill();
      }
    }
    /* THE THREAD: from the foe's shell to the caster's for 0.15s on every tick
       -- "what it burns, heals" -- with a bead of light running down it into
       the caster. Rim to rim and under both balls: nothing of it is ever
       inside a shell (drawn centre to centre it showed through the caster's
       glass, +0.02 on its disc). */
    if (X) for (const e of X){
      const kt = e.t / 0.3;
      if (kt >= 1) continue;
      const F = e.foe, S = e.f, dx = S.x - F.x, dy = S.y - F.y, d = Math.hypot(dx, dy);
      if (d < 2 * R + 4) continue;                      // touching: no room for a line
      const ux = dx / d, uy = dy / d, x0 = F.x + ux * R, y0 = F.y + uy * R;
      const x1 = S.x - ux * R, y1 = S.y - uy * R, al = 0.85 * (1 - kt * kt);
      c.lineCap = "round";
      c.globalAlpha = al;
      c.strokeStyle = "#FFC24A"; c.lineWidth = 2.4;
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
      c.strokeStyle = "#FFF3C4"; c.lineWidth = 2.4 * 0.4; c.stroke();
      const kb = 1 - (1 - kt) * (1 - kt);
      c.globalAlpha = Math.min(1, al * 1.2);
      c.fillStyle = "#FFF3C4";
      c.beginPath(); c.arc(x0 + (x1 - x0) * kb, y0 + (y1 - y0) * kb, 3.2, 0, TAU); c.fill();
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* ...and the core on the head and the sparks on the foe, over both
     fighters (see `drawSun`). */
  drawSunTop(m){
    const a = m.a, b = m.b, X = m.sunFx;
    if (!(a.sunFade > 0) && !(b.sunFade > 0) && !(X && X.length)) return;   // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR, T = m.t + (m.deathAge || 0);
    c.save();
    for (const f of [a, b]){
      const fade = f.sunFade;
      if (!(fade > 0)) continue;
      const hx = f.headX, hy = f.headY;
      const s = Math.min(1, f.sunAge / 0.5);                 // half-seconds
      const kI = 1 - (1 - s) * (1 - s);                        // ignition, eased out
      const k = Math.min(kI, 1 - (1 - fade) * (1 - fade));     // and the close
      const rr = f.w.ult.r * k, hw = 10 / 2;
      const on = Math.min(1, s * 3) * Math.min(1, fade * 2);
      /* THE CORE: r <= 14, source-over, ON the head (the faceted rim still
         shows round it). Brightens with the ignition; the head cools with
         the close. It keeps the head's layer: `a` is drawn over `b`, so when
         the caster is `b` the foe's shell is cut out of the core, exactly as
         it covers the head -- a core floating over a foe that hides its own
         head measured +0.07 to +0.11 on that foe's disc. */
      { const heat = Math.min(kI, fade), rc0 = 12 * (0.6 + 0.4 * heat);
        const cut = f === b && a.alive;
        if (cut){
          c.save();
          c.beginPath(); c.rect(hx - 20, hy - 20, 40, 40); c.arc(a.x, a.y, R, 0, TAU); c.clip("evenodd");
        }
        const g = c.createRadialGradient(hx, hy, 0, hx, hy, rc0);
        g.addColorStop(0, "rgba(255,251,236," + heat.toFixed(3) + ")");
        g.addColorStop(0.5, "rgba(255,243,196," + (0.92 * heat).toFixed(3) + ")");
        g.addColorStop(1, "rgba(255,196,80,0)");
        c.fillStyle = g;
        c.beginPath(); c.arc(hx, hy, rc0, 0, TAU); c.fill();
        if (cut) c.restore();
      }
    }
    /* THE SPARK-FALL: four sparks drop onto the top of the foe's shell on
       every tick and go out as they land (0.3s). Placed by shellHash on the
       tick's count -- no rng -- and carried with the foe as it moves. The
       CASTER's shell is cut out of them: with the caster just above the foe
       they fell across its near-white disc (+0.016 on it). */
    if (X) for (const e of X){
      const ks = e.t / 0.6;
      if (ks >= 1 || !e.foe.alive) continue;
      const F = e.foe, S = e.f;
      c.save();
      c.beginPath(); c.rect(F.x - 30, F.y - R - 70, 60, 70 + R); c.arc(S.x, S.y, R, 0, TAU); c.clip("evenodd");
      c.lineCap = "round";
      for (let i = 0; i < 4; i++){
        const hs = shellHash(9301 + (e.n % 16), i);
        const ox = (i - 1.5) * 8 + (hs - 0.5) * 6;
        const kf = Math.min(1, Math.max(0, (ks - i * 0.07) / 0.72));
        if (kf <= 0) continue;
        const yl = F.y - Math.sqrt(Math.max(0, R * R - ox * ox));
        const y0 = yl - 40 * (0.8 + 0.4 * hs);
        const y = y0 + (yl - y0) * kf * kf;
        const al = 0.95 * (kf < 0.85 ? 1 : (1 - kf) / 0.15);
        c.globalAlpha = al * 0.8;
        c.strokeStyle = "#FFB547"; c.lineWidth = 2.2;
        c.beginPath(); c.moveTo(F.x + ox, y - 13 * kf); c.lineTo(F.x + ox, y); c.stroke();
        c.globalAlpha = al;
        c.fillStyle = "#FFF3C4";
        c.beginPath(); c.arc(F.x + ox, y, 2.4, 0, TAU); c.fill();
      }
      c.restore();
    }
    c.globalAlpha = 1;
    c.restore();
  }

  drawMotes(m){
'''),

('zenith picture: the faceted gold head',
 '''  /* ---------------------------------------------------------- SANCTIFIED --
     RADIANT AND PIERCED. THE CELL'S FLAIR: a spiked ball with holes in it and
     light coming out is a CENSER, which is both the correct liturgical object
     and the only version of this weapon that has ever been swung in a church.
     The halo is a ring around the equator rather than behind the head, because
     a sphere has no behind. */
  _fhRadiant(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.strokeStyle = p.core; c.lineWidth = Math.max(1, D*0.030);  // the ring
    c.beginPath(); c.ellipse(0, 0, r*2.05, r*0.62, 0, 0, TAU); c.stroke();

    c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);            // finials
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.16) * r * 0.94, Math.sin(a - 0.16) * r * 0.94);
      c.lineTo(Math.cos(a + 0.16) * r * 0.94, Math.sin(a + 0.16) * r * 0.94);
      c.lineTo(Math.cos(a) * r * 1.52,        Math.sin(a) * r * 1.52);
      c.closePath(); c.fill();
      c.fillStyle = p.glow;
      c.beginPath();
      c.arc(Math.cos(a) * r * 1.66, Math.sin(a) * r * 1.66, r * 0.16, 0, TAU);
      c.fill();
      c.fillStyle = SHAPES._shade(p.steel, 0.58, 0.42);
    }
    SHAPES._fhBall(c, D, p);
    c.save();                                                     // pierced
    c.globalCompositeOperation = "destination-out";
    for (let i = 0; i < 6; i++){
      const a = (i / 6) * TAU + 0.5;
      c.beginPath();
      c.arc(Math.cos(a) * r * 0.52, Math.sin(a) * r * 0.52, r * 0.19, 0, TAU);
      c.fill();
    }
    c.restore();
    c.save();                                                     // light inside
    c.globalCompositeOperation = "lighter";
    c.fillStyle = p.glow; c.globalAlpha = 0.55;
    c.beginPath(); c.arc(0, 0, r*0.34, 0, TAU); c.fill();
    c.restore();
    c.restore();
  },
''',
 '''  /* ---------------------------------------------------------- SANCTIFIED --
     A FACETED GOLD HEAD (v71 section 6.1, Morningstar's "first cut"): a cut
     octagon -- a table and eight crown facets -- with eight pyramidal spikes,
     every face in one of four golds by where it faces in the WORLD, so the
     head glints as it tumbles. Gold and not the school's white on purpose:
     the sanctified steel is #FFFFFF, the haft is already that pale, and a
     white head on a white ball is the one thing the school cannot afford
     (CLAUDE.md section 4.1b). A dark rim keeps the silhouette on a white foe.
     Only a sanctified flail draws this, and Morningstar is the only one. */
  _fhRadiant(c, D, p, spin){
    const r = D * 0.34, LIGHT = -2.36;             // the world's light: up and left
    const GOLD = ["#6E4812", "#B7801F", "#E8B447", "#FFE39A"];
    const tone = (q) => GOLD[Math.max(0, Math.min(3, Math.floor((Math.cos(q + spin - LIGHT) + 1) * 2)))];
    c.save();
    c.rotate(spin);
    c.lineJoin = "round";
    for (let i = 0; i < 8; i++){                                  // the spikes
      const q = (i / 8) * TAU, w = 0.21;
      const x0 = Math.cos(q - w) * r * 0.9, y0 = Math.sin(q - w) * r * 0.9;
      const x1 = Math.cos(q + w) * r * 0.9, y1 = Math.sin(q + w) * r * 0.9;
      const tx = Math.cos(q) * r * 1.6, ty = Math.sin(q) * r * 1.6;
      const mx = Math.cos(q) * r * 0.9, my = Math.sin(q) * r * 0.9;
      c.fillStyle = "#3A260A";
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(tx * 1.04, ty * 1.04); c.lineTo(x1, y1); c.closePath(); c.fill();
      c.fillStyle = tone(q - 0.9);
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(tx, ty); c.lineTo(mx, my); c.closePath(); c.fill();
      c.fillStyle = tone(q + 0.9);
      c.beginPath(); c.moveTo(x1, y1); c.lineTo(tx, ty); c.lineTo(mx, my); c.closePath(); c.fill();
    }
    const O = [], I = [];                                         // the cut body
    for (let i = 0; i < 8; i++){
      const q = ((i + 0.5) / 8) * TAU;
      O.push([Math.cos(q) * r, Math.sin(q) * r]);
      I.push([Math.cos(q) * r * 0.5, Math.sin(q) * r * 0.5]);
    }
    c.fillStyle = "#3A260A";
    c.beginPath();
    for (let i = 0; i < 8; i++) c.lineTo(O[i][0] * 1.07, O[i][1] * 1.07);
    c.closePath(); c.fill();
    for (let i = 0; i < 8; i++){
      const j = (i + 1) % 8;
      c.fillStyle = tone(((i + 1) / 8) * TAU);
      c.beginPath();
      c.moveTo(O[i][0], O[i][1]); c.lineTo(O[j][0], O[j][1]);
      c.lineTo(I[j][0], I[j][1]); c.lineTo(I[i][0], I[i][1]);
      c.closePath(); c.fill();
    }
    c.fillStyle = GOLD[3];                                        // the table
    c.beginPath();
    for (let i = 0; i < 8; i++) c.lineTo(I[i][0], I[i][1]);
    c.closePath(); c.fill();
    c.strokeStyle = "#8A5A14"; c.lineWidth = Math.max(0.8, D * 0.018);
    c.stroke();
    c.restore();
  },
'''),

]

STAGE_OUT = {"1": "sc-morningstar", "2": "sc-sun", "3": "sc-burn", "4": "sc-zenith",
             "6": "sc-zenith-fx"}


def relic_ult(code: str) -> str:
    i = code.find('id:"morningstar"')
    if i < 0:
        raise SystemExit("no Morningstar in this source")
    j = code.find("ult:{", i)
    k = code.find("},", j)
    return code[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nMORNINGSTAR / ZENITH -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Corollary
    # at charge 14 and Daybreak through its stage 3.
    for need, why in (('name:"Corollary", charge:14', "no Corollary at charge 14"),
                      ("dawnShown", "no Daybreak stage 3 -- not the chain tip")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    # AND THE DONOR'S FLAIL PROFILE IS STILL WHAT THIS BUILDER COPIES.
    g = code[code.find('id:"gravemourn"'):]
    if PHYS not in g[:400]:
        raise SystemExit("Gravemourn's flail profile has moved -- the donor is "
                         "not what this builder copies")
    print("  base  the chain tip (Corollary c14, Daybreak stage 3); the donor's "
          "flail profile holds")

    if A.stage == "1":
        if 'id:"morningstar"' in code:
            raise SystemExit("this source already carries Morningstar -- built")
        edits, want = S1, ult_block("1e9", 0, 0)
    else:
        if 'id:"morningstar"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultSun" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0, 0)
        elif A.stage == "3":
            if "ultSun" not in code:
                raise SystemExit("stage 3 needs stage 2 under it")
            edits, want = S3, ult_block(ULT["charge"], ULT["tickDmg"], 0)
        elif A.stage == "4":
            if f'tickDmg:{ULT["tickDmg"]},' not in code:
                raise SystemExit("stage 4 needs stage 3 under it")
            edits, want = S4, ult_block(ULT["charge"], ULT["tickDmg"], ULT["bless"])
        else:
            if f'bless:{ULT["bless"]},' not in code or "sunShown" in code:
                raise SystemExit("stage 6 goes on stage 4, once")
            edits, want = S6, ult_block(ULT["charge"], ULT["tickDmg"], ULT["bless"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Morningstar's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S4 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the RNG")
    for label, _old, new in S6:
        if "ultFx" in strip_comments(new):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' uses the one "
                             "ultFx slot (open item 25)")
    if len(re.findall(r'kind:"sun"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one sun ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one sun ultimate, Morningstar's; no insert draws the RNG; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
