#!/usr/bin/env python
"""BINDWEED / TENDRIL -- the verdant flail, a NEW relic. v101.

Built from `06-docs/v68/BINDWEED-BUILD-BRIEF.md` and
`verdant-flail-design-v68.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-bindweed.html
    stage 2   the seek and the growth     -> sc-vine.html     (the seek+growth arm)
    stage 3   the bites                   -> sc-bites.html    (arm C)
    stage 4   the root and the wither     -> sc-tendril.html  (arm D)
    stage 5   the turn, the blade         -> sc-tendril-t3.html (turn 4 -> 3, dmg 19 -> 18)
    stage 6   picture, voice              -> sc-tendril-fx.html (no field: drawn leaf motes, v101 §5)

§1 (the brief's §0): "For a duration the whole chain becomes a living thorned
vine. It turns toward the enemy and grows until it reaches them, and it draws
back in when they come closer, so the head -- still a flail head, still hitting
like one -- is always where the enemy is. Anywhere the vine touches them it
bites: a small hit that leaves entangle, over and over while it stays on them.
When the duration ends the vine withers, and the thorns it left take root: the
enemy is held where it stands, ball and weapon, for a moment for every
entangle stack it carries."

Declared (design §4-§7, brief §0-§1):
  THE SEEK    for the window the facing turns toward the foe at `turn` rad/s
              the shortest way round, instead of advancing by spin; the chain's
              spin is 0, so its drive is 0 (the spring, sag, damping and
              extension are the engine's own).
  THE GROWTH  reachMul moves at `grow` a second toward (d - R) / (reach x
              mods.reach), both directions, clamped [1, growCap].
  A BITE      the foe's centre within R + vineW of the pivot -> head segment,
              once per `biteCd`: hurt(foe, biteDmg, f) -- ward first, nothing
              else -- and entangle +bitePer. No knock, no stop, no beat, no
              resolveHit.
  THE ROOT    at the window's clock close with both alive: pin rootPer x the
              foe's entangle stacks, ball and weapon (Grasp's write, no pinFree).
  THE WITHER  0.4s; the next cast waits for it.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm D (v101 §0).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CHAIN'S SPIN IS 0 FOR THE WINDOW, not only its drive. The lab zeroed
     the weapon's spin, which zeroes the drive AND leaves the extension's
     normaliser at its 0.5 floor, so a small sway throws the head out; the
     brief's "drive = 0" and "the extension untouched" are both that. The build
     zeroes `spin` in tickWeapon for this fighter, and never writes the shared
     weapon (the mirror match shares it).
  2. THE VINE KEEPS TURNING WHILE STUNNED (the brief leaves it to the build;
     the lab turned it, and that is what was priced).
  3. REACH RETURNS TO 1 AT THE CLOSE (design §7 and the lab). The brief's
     "eased back over the wither" is the wither's picture, not the hit box.
  4. NO PER-BITE REACH KICK. The lab's arms add 0.05 of reach a bite; the
     prose has none. v101 §2 prices the difference.
  5. EITHER DEATH ENDS THE WINDOW AND ROOTS NOBODY (the brief); the lab closed
     only on its clock.
  6. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; the lab and the
     brief wrote the Fighter, and entangle has no reader of it).
  7. A BITE THAT KILLS files its own fatal hit beat (Rick's standing rule for
     a side-channel kill); no other bite files one.
  8. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).

THE CLOCK. The window, the turn, the growth, the bite's cooldown and the
wither run on the window tickers' clock, which stops through a hit stop
(Corollary's, Daybreak's, Zenith's, Canopy's and Onslaught's convention). The
lab ran all of them through freezes; v99 §4 and v100 §2 measured what that is
worth on the two builds before this one.

THE BASE is the chain tip, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "bindweed"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v101 §0)
    "dur": 8,         # "the window 8s"
    "turn": 4,        # "facing turns toward the foe at 4 rad/s"
    "grow": 0.3,      # "reachMul eased at 0.3/s"
    "growCap": 3.0,   # "clamped [1, 3.0]"
    "vineW": 8,       # "within R + 8 of the pivot -> head segment"
    "biteDmg": 2,     # "2 damage (ward absorbs first)" -- stage 3
    "bitePer": 1,     # "+ 1 entangle" -- stage 3
    "biteCd": 0.3,    # "every 0.30s while touching"
    "rootPer": 0.3,   # "pin 0.30s x entangle stacks" -- stage 4
    "wither": 0.4,    # "the next cast waits for the wither to finish (0.4s)"
}
TIP = "The chain becomes a vine that hunts the foe. Bites entangle, then root"
# Gravemourn's flail profile, the lab's donor (vine_price.py), and the lab's
# blade, 19 ("a placeholder -- stage 5 owns it").
PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:19, spin:2.2, '
        'mode:"chain", mass:3.6')
DONOR_PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:24.03, spin:2.2, '
              'mode:"chain", mass:3.6')
VERDANT = ("thornwake", "heartwood", "vinesower", "thornshear", "ironwood")
BLURB = ("A flail whose chain becomes a living vine: it hunts the foe, bites it "
         "with thorns, and roots it where it stands.")


def ult_block(charge, bite_dmg, bite_per, root_per) -> str:
    return (f'''    ult:{{ name:"Tendril", charge:{charge}, kind:"tendril", dur:{ULT["dur"]},
          turn:{ULT["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},
          biteDmg:{bite_dmg}, bitePer:{bite_per},          // v68: the bites (stage 3)
          biteCd:{ULT["biteCd"]},
          rootPer:{root_per},          // v68: the root (stage 4)
          wither:{ULT["wither"]},
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
# THE RELIC, APPENDED AFTER PORTCULLIS, ITS ULTIMATE STUBBED at charge 1e9
# (the clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back, and SHAPES.flailHead
# already routes verdant to `_fhGrown`, which no shipped relic has drawn.
ROW_ANCHOR = ('''    blurb:"A flail whose ball becomes the weapon: it charges, every slam hits for the shield it carries, and every slam banks more." },

];''')

S1 = [

("bindweed joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* BINDWEED / TENDRIL (v68; built v101) -- THE VERDANT FLAIL, the 38th relic
     built. Gravemourn's flail profile (the lab's donor) at the lab's blade,
     19 (stage 5 settles it), and the school's channel, onHit entangle 2.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its seek and
     growth, its bites, then its root. */
  {{ id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    {PHYS},
    onHit:{{ entangle:2 }},
{ult_block("1e9", 0, 0, 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the vine has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Tendril", charge:1e9, kind:"tendril", dur:8,
''',
 f'''    ult:{{ name:"Tendril", charge:{ULT["charge"]}, kind:"tendril", dur:{ULT["dur"]},   // v68 stage 2: the vine seeks and grows
'''),

("the fighter carries the vine",
 '''    this.ultRam = null;
    this.ramTally = null;
''',
 '''    this.ultRam = null;
    this.ramTally = null;
    /* {t, dur, cd} while TENDRIL's vine hunts (v68). null on every other relic
       and on this one outside its window: `tickTendril` returns after a
       two-iteration loop that does nothing, and tickWeapon's chain branch
       reads it once. `vineWither` is the seconds left of the wither, which the
       next cast waits for. `vineTally` is the probe's count, cumulative over
       the fight; nothing in the simulation reads it. */
    this.ultVine = null;
    this.vineWither = 0;
    this.vineTally = null;
'''),

("the vine does not spin",
 '''    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge || f.ultWire ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);
''',
 '''    /* TENDRIL (v68): THE VINE DOES NOT SPIN. `spin` is 0 for the whole
       window, as the lab priced it (it zeroed the weapon's spin; the build
       must never write the shared weapon), so the chain's drive is 0 and the
       extension's normaliser below sits at its 0.5 floor -- a small sway
       throws the head out, and that sway is the picture. `ultVine` is null on
       every other relic, so theirs is the same product. */
    const spin = (f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge || f.ultWire ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);
'''),

("the vine turns toward the foe",
 '''      if (f.stun <= 0) f.theta += spin * dt * f.spinDir;
      const drive = f.stun > 0 ? 0 : spin * f.spinDir;
''',
 '''      /* TENDRIL'S SEEK (v68 §5): for the window the facing turns toward the
         foe at `turn` rad/s the shortest way round -- stunned or not, as the
         lab turned it -- instead of advancing by spin. */
      if (f.ultVine){
        if (foe.alive){
          const want = Math.atan2(foe.y - f.y, foe.x - f.x);
          const dl = Math.atan2(Math.sin(want - f.theta), Math.cos(want - f.theta));
          const k = f.w.ult.turn * dt;
          f.theta += clamp(dl, -k, k);
        }
      } else if (f.stun <= 0) f.theta += spin * dt * f.spinDir;
      const drive = f.stun > 0 ? 0 : spin * f.spinDir;
'''),

("the cast opens the vine and resolves nothing",
 '''    if (u.kind === "ram"){
''',
 '''    if (u.kind === "tendril"){
      /* TENDRIL (v68). NOTHING RESOLVES HERE: the cast turns the chain into a
         vine for `u.dur` seconds, and tickWeapon (the seek) and `tickTendril`
         (the growth, the bites, the root) do everything the window does. `cd`
         starts at zero, so a foe already touching is bitten on the first
         frame. */
      f.ultVine = { t: 0, dur: u.dur, cd: 0 };
      if (!f.vineTally)
        f.vineTally = { casts: 0, frames: 0, touchFrames: 0, bites: 0, dealt: 0,
                        stacks: 0, foeStk: 0, peak: 1, roots: 0, rootSec: 0 };
      f.vineTally.casts++;
      return;
    }
    if (u.kind === "ram"){
'''),

("the vine ticks with the window tickers",
 '''    this.tickRam(dt);                   // ONSLAUGHT (v72)
''',
 '''    this.tickRam(dt);                   // ONSLAUGHT (v72)
    this.tickTendril(dt);               // TENDRIL (v68)
'''),

("a cast waits for the last vine's wither",
 '''    if (f.charge >= f.w.ult.charge && !f.ultCorona && !f.ultTree && !f.treeWither){
''',
 '''    if (f.charge >= f.w.ult.charge && !f.ultCorona && !f.ultTree && !f.treeWither
        && !f.ultVine && !f.vineWither){       // TENDRIL (v68): one vine at a time
'''),

("tickTendril grows, bites and roots",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ THE TENDRIL ========
     v68 §4-§7, brief §0-§1. While the window runs (tickWeapon turns the vine
     toward the foe; this does the rest):
       THE GROWTH  reachMul moves at `grow` a second toward the foe's rim in
                   units of the type's reach, (d - R) / (reach x mods.reach),
                   both directions, clamped [1, growCap]. Every reach read
                   carries it, so the drawn vine and the hit segment grow
                   together; tickWeapon uses it next frame, as the lab did.
       A BITE      the foe's centre within R + vineW of the pivot -> head
                   segment and the cooldown clear: hurt(foe, biteDmg, f) --
                   ward first and NOTHING ELSE: no knock, no stop, no stagger,
                   no resolveHit -- then entangle +bitePer. The cooldown runs
                   through the whole window, touching or not. A bite that
                   kills files its own fatal hit beat; no other bite files one.
       THE CLOSE   by the clock, or EITHER death: reach back to 1 and `wither`
                   seconds that the next cast waits for. Only a clock close
                   with both alive roots: pin rootPer x the foe's entangle
                   stacks, ball and weapon -- Grasp's write, no pinFree, so
                   `tickStasis` locks the weapon.
     The target is the OPPONENT only. On the window tickers' clock, so all of
     it freezes through a hit stop. `apply`'s source is a side letter. */
  tickTendril(dt){
    for (const f of [this.a, this.b]){
      if (f.vineWither > 0) f.vineWither = Math.max(0, f.vineWither - dt);
      const Z = f.ultVine;
      if (!Z) continue;
      const u = f.w.ult, T = f.vineTally;
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){
        f.ultVine = null;
        f.reachMul = 1;
        f.vineWither = u.wither;
        if (Z.t >= Z.dur && f.alive && foe.alive && u.rootPer > 0){
          const n = foe.stacks("entangle");
          if (n > 0){
            const hold = u.rootPer * n;
            foe.pin = Math.max(foe.pin, hold);
            foe.pinMax = Math.max(foe.pinMax, hold);
            if (!(foe.pin > hold)) foe.pinV = [foe.vx, foe.vy];
            T.roots++;
            T.rootSec += hold;
          }
        }
        continue;
      }
      T.frames++;
      const dd = Math.hypot(foe.x - f.x, foe.y - f.y);
      const want = clamp((dd - R) / (f.w.reach * this.actMods.reach), 1, u.growCap);
      if (f.reachMul < want) f.reachMul = Math.min(want, f.reachMul + u.grow * dt);
      else if (f.reachMul > want) f.reachMul = Math.max(want, f.reachMul - u.grow * dt);
      if (f.reachMul > T.peak) T.peak = f.reachMul;
      Z.cd -= dt;
      if (segDist(f.pivX, f.pivY, f.headX, f.headY, foe.x, foe.y).d < R + u.vineW){
        T.touchFrames++;
        if ((u.biteDmg > 0 || u.bitePer > 0) && Z.cd <= 0){
          Z.cd = u.biteCd;
          T.bites++;
          const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
          if (u.biteDmg > 0) this.hurt(foe, u.biteDmg, f);
          T.dealt += before - (foe.hp + foe.shield);
          if (u.bitePer > 0){ foe.apply("entangle", u.bitePer, f === this.a ? "a" : "b"); T.stacks += u.bitePer; }
          if (wasUp && foe.hp <= 0)
            this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                        x: foe.x, y: foe.y, dmg: u.biteDmg, crit: false,
                        fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                        selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                        close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                        ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                        shotSpd0: 0, tendril: true });
        }
      }
      T.foeStk += foe.stacks("entangle");
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the bites",
 '''          biteDmg:0, bitePer:0,          // v68: the bites (stage 3)
''',
 f'''          biteDmg:{ULT["biteDmg"]}, bitePer:{ULT["bitePer"]},          // v68: the bites (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the root",
 '''          rootPer:0,          // v68: the root (stage 4)
''',
 f'''          rootPer:{ULT["rootPer"]},          // v68: the root (stage 4)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE TURN AND THE BLADE (brief §2 stage 5: "If the band does not land inside
# 17-19.5, move `turn` inside 3-5 FIRST and say so"). Both sides, two blocks,
# ~1480 fights a point (relic_rate): at the designed turn 4, blade 17 reads
# 54.7, so the crossing is ~15.5 -- outside the band. At turn 3: 17 -> 45.7,
# 18 -> 48.6, 19 -> 55.6, the crossing ~18.2, inside the brief's "expect
# 17.5-18.5"; at 3.5 it would fall just under 17. Why the built relic reads over
# the lab at 4: the engine's window is ~9.6s of match time where the lab's was 8
# (v101 §2, measured with the lab at dur 9.6).
TUNED = {"turn": 3, "dmg": 18}

S5 = [
("the turn: the build's knob, inside 3-5",
 f'''          turn:{ULT["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},
''',
 f'''          turn:{TUNED["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},   // v68 stage 5: turn {ULT["turn"]} -> {TUNED["turn"]}, the build's knob
'''),
("the blade: at the crossing",
 '''  { id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:19,''',
 f'''  {{ id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:{TUNED["dmg"]},'''),
]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v68 §8.1-8.2, brief stage 6), picked on
# measurements under Rick's "you pick i overrule" by `bindweed_voice_lab.py`
# and the picture lab (v101 §5). Presentation only: engine_ab over all 38
# relics, Bindweed included, is the proof. The rows are byte-exact to the
# labs' own files (voice 4, picture 11; no two share an anchor, so none is
# merged); the picture rows alone reproduce the picture lab's stamp
# (ef4bd13fe968d99c) on sc-tendril-t3. Voice first, then picture; the other order
# writes the same bytes.
#   THE VOICE: the cast (fireUlt's own `ult`/bindweed call, which fell through
#   to rune-crack), a bite (once per bite, pitched by the foe's entangle
#   stacks AFTER the bite -- a killing bite snaps too), the root (on the frame
#   the pin is written) and the wither (a clock close with both alive,
#   rooted or not; never on a death). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickTwine` in tickPresentation reads the window, the chain's
#   pivot and head and the tally's counters rising, and writes only its own
#   `twine*` fields, `tags` and `taught`. The root files one write-only
#   'ult' beat (the brief: the root files a beat; no hit stop). The runic
#   hexagon is left off a ball the root holds (v68 open decision 6) through
#   a presentation marker, `twineHeld`; `pinFree` is read, never written.
#   No fx.js field: leaf motes are drawn instead (v101 §5, Rick's to overrule).
S6 = [

("Sfx: Bindweed's cast, bite, root and wither arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "bindweed"){                   // the chain greens
          /* BINDWEED'S CAST, THE GREENING -- v68 §8.2: "a rising
             rustle-and-creak, 0.5s, noise band-passed 400-3k with a low creak
             under it (a re-struck _tone at 70-90 Hz, since a held note does
             not exist here). Not a chime, not a crack: this is growth."
             SWEEP-TRI, of 5, picked on the numbers by `bindweed_voice_lab.py`
             under Rick's "you pick i overrule" (v101). Bindweed had no arm and
             fell through to rune-crack, which eleven other relics still use,
             so this ADDS arms before that fallback and leaves it alone.

             One bandpass sweep climbs 400 -> 3000 Hz over 0.56 s; under it a
             triangle held by re-striking at its own cycles (a held note does
             not exist in this toolkit, CLAUDE.md 4.5), gliding 70 -> 90 Hz and
             swelling. The rustle's band climbs +533 cents across the voice,
             the creak 71 -> 88 Hz, -6.0 dB under the rustle; 0.65 of the power
             above 150 Hz inside 400-3000 Hz at the worst noise draw, no peak
             standing more than 2.6 dB over its neighbours (noise, not a
             chime), and it grows +12.6 dB from its head to its top (not a
             crack). Audible 510 ms; loudest 50 ms -2.9 dB re Bindweed's blow.
             Register at most 0.69 against rune-crack, the verdant casts, the
             flail row's casts, the blow and the death voice. */
          const g = 0.4445, kc = 0.1446;
          this._sweep(t, { f0: 400, f1: 3000, q: 0.8, gain: g, dur: 0.56, atk: 0.33, type:"bandpass" });
          for (let s = 0; s < 0.49;){
            const u = s / 0.5, f = 70 * Math.pow(90 / 70, u), a = g * kc * (0.4 + 0.6 * u);
            this._tone(t + s, { freq: f, gain: a, dur: 0.05, type:"triangle" }).frequency.value = f;
            s += 1 / f;
          }
        } else if (w === "bindweed-bite"){              // a thorn goes in
          /* THE BITE -- "a short wet snap, 60-90ms, peak <=0.45, pitched up a
             semitone per entangle stack on the foe (the count in the ear)"
             (v68 §8.2). SNAP, of 4 (`bindweed_voice_lab.py`). `tickTendril`
             plays it once per bite with n = the foe's entangle stacks after
             the bite (1-4), so every frequency is x 2^(n/12).

             A 12 ms bandpass snap at 2.4 kHz over a sine body falling A5 -> A4
             (the score's A, a semitone up per stack: A#5 on a clean foe's
             first bite, C#6 at the cap). Audible 75-80 ms, peak 0.21 at the
             loudest draw and count; the body falls at least 518 cents under
             the snap (wet); each count +100 cents over the last; loudest 50 ms
             -9.0 dB re the blow and +11.9 dB re the wall tick. One snap a
             call. Register at most 0.51 against the blow, the wall, fork,
             hex-snap, the vine's plant, rune-crack and the cast. */
          const g = 0.1111, D = 0.126, k = Math.pow(2, Math.max(0, Math.min(4, p.n | 0)) / 12);
          this._burst(t, { freq: 2400 * k, q: 1.4, gain: g, dur: 0.012, type:"bandpass" });
          this._tone(t, { freq: 880 * k, to: 440 * k, gain: g * 0.8, dur: D, type:"sine" });
        } else if (w === "bindweed-root"){              // and takes root
          /* THE ROOT -- "a low creak into a crack, 0.35s, share below 120 Hz
             >= 0.4 (Deadfall's detonation register: this is the biggest single
             thing the relic does)" (v68 §8.2). DEEP, of 5
             (`bindweed_voice_lab.py`). `tickTendril` plays it on the frame the
             pin is written: a clock close, both alive, the foe carrying
             entangle.

             Canopy's timber an octave and a half down (a 260 Hz sine and its
             2.76 mode at 0.4) pulsed for 0.2 s, then the crack: a 35 ms
             highpass snap over a sine falling 60 -> 30 Hz, the weight under
             the death voice's 120 Hz start so it never reads as a death. The
             creak quickens 33 -> 55 a second (the strain before the give;
             PULSED 0.76, 26 dB deep), -5.6 dB under the crack, which lands 206
             ms in and stands +44 dB over it. 0.50 of its power below 120 Hz at
             the worst noise draw; audible 370 ms; loudest 50 ms -1.4 dB re the
             blow, +1.5 dB over the loudest of the relic's three other voices.
             Register 0.31 against the death voice, at most 0.795 against
             rune-crack, the verdant and flail casts (Threshmaw's, at the gate:
             a voice this heavy sits near the flail row's low casts), the blow,
             Deadfall's detonation, Paradox's pin and this relic's other three. */
          const g = 0.5179, kc = 0.2683, kt = 0.3464;
          for (let s = 0, k = 0; s < 0.188; k++){
            const u = s / 0.2, a = g * kc * (0.45 + 0.55 * u);
            this._tone(t + s, { freq: 260, gain: a, dur: 0.03, type:"sine" });
            this._tone(t + s, { freq: 718, gain: a * 0.4, dur: 0.02, type:"sine" });
            s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
          this._burst(t + 0.2, { freq: 2600, q: 0.8, gain: g * 0.8, dur: 0.035, type:"highpass" });
          this._tone (t + 0.2, { freq: 60, to: 30, gain: g * kt, dur: 0.3, type:"sine" });
        } else if (w === "bindweed-wither"){            // and the vine lets go
          /* THE WITHER -- "a dry falling rustle, 0.4s, high-passed 1.5k, quiet
             (peak <=0.3): the tell that the window is over" (v68 §8.2). CHAIN,
             of 4 (`bindweed_voice_lab.py`): three overlapping bandpass sweeps
             (Q 0.9) falling 7 -> 4.8, 5 -> 3.4 and 3.6 -> 2.4 kHz, each
             quieter -- the cast's chain run downward.

             Falls -807 cents; 0.01 of its power below 1.5 kHz and 0.00 below
             120 Hz at the worst draw (dry); no peak over 2.2 dB (a rustle, not
             a tone); audible 355 ms; peak 0.19; -9.0 dB under the cast's top.
             `tickTendril` plays it when the window closes by its clock with
             both alive -- on a rooting close, on the root's own frame, where
             it keeps +4.9 dB in its own third-octave over the root. */
          const g = 0.1184;
          this._sweep(t, { f0: 7000, f1: 4800, q: 0.9, gain: g, dur: 0.22, atk: 0.05, type:"bandpass" });
          this._sweep(t + 0.12, { f0: 5000, f1: 3400, q: 0.9, gain: g * 0.8, dur: 0.22, atk: 0.05, type:"bandpass" });
          this._sweep(t + 0.24, { f0: 3600, f1: 2400, q: 0.9, gain: g * 0.6, dur: 0.22, atk: 0.05, type:"bandpass" });
        } else {                                        // rune-crack'''),

("tickTendril: the bite voice, once per bite, after the bite's hurt and entangle",
 '''          if (u.bitePer > 0){ foe.apply("entangle", u.bitePer, f === this.a ? "a" : "b"); T.stacks += u.bitePer; }''',
 '''          if (u.bitePer > 0){ foe.apply("entangle", u.bitePer, f === this.a ? "a" : "b"); T.stacks += u.bitePer; }
          /* TENDRIL'S BITE (v68 §8.2: "a short wet snap ... pitched up a
             semitone per entangle stack on the foe"): one snap per bite, after
             the bite's hurt and its entangle, pitched by the stacks the foe now
             carries. A killing bite snaps too -- the number of snaps is the
             number of bites. Presentation only: SFX.play draws nothing, is a
             no-op headless, and nothing here is read back
             (bindweed_voice_lab: fights identical). */
          SFX.play("ult", { w: "bindweed-bite", n: foe.stacks("entangle") });'''),

('tickTendril: the wither voice, on a clock close with both alive',
 '''        f.vineWither = u.wither;''',
 '''        f.vineWither = u.wither;
        /* TENDRIL'S WITHER (v68 §8.2: "a dry falling rustle, 0.4s ... the tell
           that the window is over"): on the frame the window runs out BY ITS
           CLOCK with both alive, rooted or not. A caster's death ends the
           fight, and a close after the foe's death belongs to its kill
           flight, so both are left to the death voice (Canopy's, Zenith's and
           Daybreak's rule). Plain SFX.play; nothing is read back. */
        if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "bindweed-wither" });'''),

('tickTendril: the root voice, on the frame the pin is written',
 '''            T.roots++;''',
 '''            T.roots++;
            /* TENDRIL'S ROOT (v68 §8.2: "a low creak into a crack, 0.35s"): on
               the frame the pin is written -- the clock close, both alive, the
               foe carrying entangle. Plain SFX.play; nothing is read back. */
            SFX.play("ult", { w: "bindweed-root" });'''),

('tendril picture: fighter fields',
 '''    this.ultVine = null;
    this.vineWither = 0;
    this.vineTally = null;
''',
 '''    this.ultVine = null;
    this.vineWither = 0;
    this.vineTally = null;
    /* TENDRIL'S PICTURE (v68 section 8.1), and none of it is the window:
       the vine outlives `ultVine` by its 0.4s wither and the root outlives it
       by the hold, so the picture keeps its own state. On the FIGHTER and
       never on `m.ultFx` (one slot, and the opponent's cast takes it: open
       item 25). Driven in `tickPresentation` (`tickTwine`); nothing in the
       simulation reads any of it. `twine`, not `vine`: the Thicket owns
       `vines`, `tickVines`, `drawVines` and the SFX kind "vine".
         twineFade -- 1 while the vine stands; eased to 0 over the wither
           after the close, the caster's fall or the match's end
         twineAge -- the presentation clock since the cast (the greening)
         twineOut -- the presentation clock since the close (the wither)
         twineSeen, twineRootSeen -- bites and roots already shown
           (`vineTally.bites`, `vineTally.roots`)
         twineTagN, twineTagT -- the count the vine's ENTANGLE tag last
           printed, and how long that tag is still up
         twineFlash -- the bite flashes (an angle on the foe's rim, a clock)
         twineMotes -- leaf motes shed along the vine (records)
         twineBits -- the wither's falling leaves and vine (records)
         twineDrop -- leaf pairs the wither's brown has let go
         twineMoteN, twineMoteAcc -- the motes' count and spawn accumulator
       and ON THE HELD BALL, the vine's quarry:
         twineHeld -- 1 exactly while a Tendril root's pin holds this ball.
           Its one reader outside this picture is `_drawField`'s held-ball
           guard, which leaves Paradox's hexagon off it (v68 open decision
           6); `pinFree` is not touched, so the weapon stays locked
         twineRootFade, twineHeldAge, twineHeldOut -- the shoots' own fade,
           the clock since the root, and since the hold let go */
    this.twineFade = 0;
    this.twineAge = 0;
    this.twineOut = 0;
    this.twineSeen = 0;
    this.twineRootSeen = 0;
    this.twineTagN = 0;
    this.twineTagT = 0;
    this.twineFlash = [];
    this.twineMotes = [];
    this.twineBits = [];
    this.twineDrop = 0;
    this.twineMoteN = 0;
    this.twineMoteAcc = 0;
    this.twineHeld = 0;
    this.twineRootFade = 0;
    this.twineHeldAge = 0;
    this.twineHeldOut = 0;
'''),

('tendril picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickTwine(dt);                 // TENDRIL'S PICTURE (v68 section 8.1)
'''),

('tendril picture: tickTwine',
 '''      T.foeStk += foe.stacks("entangle");
    }
  }
''',
 '''      T.foeStk += foe.stacks("entangle");
    }
  }

  /* ------------------------------------------------ TENDRIL'S PICTURE ---
     v68 section 8.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.6 is the
     cast's 0.30s greening, 0.8 the close's 0.4s wither, 0.24 a bite's
     0.12s thorn flash. Everything is read off the simulation -- the window,
     the chain's own pivot and head, the tally's counters rising -- so the
     simulation makes no call for it, and nothing here writes a field the
     simulation reads: the picture's own fields, `tags` and `taught` only.
     Not after the match and not once the caster falls: `tickTendril` never
     runs again once `over` is set, so a vine standing at the kill would
     otherwise stand through the verdict. */
  tickTwine(dt){
    const R = CONFIG.physics.ballR, ST = 12;
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a, T = f.vineTally;
      /* THE HELD BALL (this fighter as a vine's quarry). `twineHeld` is 1
         exactly while the root's pin holds -- frozen with it through the
         verdict -- and `twineRootFade` is the shoots' own tail. */
      if (f.twineHeld && !(f.pin > 0 && f.alive)) f.twineHeld = 0;
      if (f.twineRootFade > 0){
        if (!f.alive) f.twineRootFade = 0;
        else if (f.twineHeld && !this.over) f.twineHeldAge += dt;
        else {
          f.twineHeldOut += dt;
          f.twineRootFade = Math.max(0, 1 - f.twineHeldOut / 0.4);
        }
      }
      for (let i = f.twineFlash.length - 1; i >= 0; i--){
        f.twineFlash[i].t += dt;
        if (f.twineFlash[i].t >= 0.24) f.twineFlash.splice(i, 1);
      }
      for (let i = f.twineMotes.length - 1; i >= 0; i--){
        f.twineMotes[i].t += dt;
        if (f.twineMotes[i].t >= 2.2) f.twineMotes.splice(i, 1);
      }
      for (let i = f.twineBits.length - 1; i >= 0; i--){
        f.twineBits[i].t += dt;
        if (f.twineBits[i].t >= f.twineBits[i].life) f.twineBits.splice(i, 1);
      }
      if (f.twineTagT > 0) f.twineTagT -= dt;
      if (!T) continue;
      /* THE ROOT: a clock close with both alive wrote the foe's pin this
         step, and the tally's count is how this knows. */
      if (T.roots !== f.twineRootSeen){
        f.twineRootSeen = T.roots;
        if (foe.alive && foe.pin > 0){
          foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldAge = 0; foe.twineHeldOut = 0;
        }
      }
      /* THE BITES the tally shows: a thorn flash on the foe's rim where the
         tested segment is nearest it, and ENTANGLE with its count whenever
         the count a bite leaves is not the one the vine last printed -- the
         first bite of a window, and each step of the climb -- one vine tag
         up at a time, so a flurry never stacks them, and none while the
         count sits at its cap (the ball's own trailing vines carry it). ONE
         ENTANGLE TAG ON THE FOE AT A TIME: the head's own blow tags it too
         (`resolveHit`), so a tag already up there takes the count instead of
         a second printing over it, and a head's tag that lands while the
         vine's is up takes the count and the vine's goes. */
      while (f.twineSeen < T.bites){
        f.twineSeen++;
        if (!foe.alive) continue;
        const q = segDist(f.pivX, f.pivY, f.headX, f.headY, foe.x, foe.y);
        const a = Math.atan2(q.y - foe.y, q.x - foe.x);
        f.twineFlash.push({ a, t: 0 });
        const n = foe.stacks("entangle");
        if (foe.hp > 0 && n !== f.twineTagN && !(f.twineTagT > 0)){
          f.twineTagN = n; f.twineTagT = 1.8;
          const g = this.tags.find(g2 => g2.key === "entangle" && !g2.first && g2.life > 0.3
                                         && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
          if (g) g.val = n;
          else {
            const first = !this.taught.entangle && !!STATUS.entangle.tip;
            if (first) this.taught.entangle = true;
            this.statusTag(foe.x + Math.cos(a) * R, foe.y + Math.sin(a) * R, "entangle", first, n);
            this.tags[this.tags.length - 1].twine = true;
          }
        }
      }
      if (f.twineTagT > 0 && foe.alive){
        const near = this.tags.filter(g2 => g2.key === "entangle" && !g2.first
                                            && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
        if (near.some(g2 => g2.twine) && near.some(g2 => !g2.twine)){
          for (const g2 of near){
            if (g2.twine) this.tags.splice(this.tags.indexOf(g2), 1);
            else g2.val = foe.stacks("entangle");
          }
        }
      }
      const Z = (this.over || !f.alive) ? null : f.ultVine;
      if (Z){
        if (!(f.twineFade > 0) || f.twineOut > 0){                // a new vine
          f.twineAge = 0; f.twineOut = 0; f.twineTagN = 0;
          f.twineDrop = 0;
        }
        f.twineFade = 1;
        f.twineAge += dt;
        /* LEAF MOTES shed along the vine, sparse -- drawn, in place of a
           field on the one ultFx slot. Placed by shellHash on their count:
           no rng. */
        f.twineMoteAcc += dt * 2.0;
        while (f.twineMoteAcc >= 1){
          f.twineMoteAcc -= 1;
          const s = 0.12 + 0.80 * shellHash(9811 + f.side, f.twineMoteN);
          f.twineMotes.push({ x: f.pivX + (f.headX - f.pivX) * s, y: f.pivY + (f.headY - f.pivY) * s,
                              t: 0, n: f.twineMoteN++ });
        }
        if (f.twineMotes.length > 24) f.twineMotes.splice(0, f.twineMotes.length - 24);
      } else if (f.twineFade > 0){
        const first = !(f.twineOut > 0);
        const V = twineCurve(f, f.w.reach * this.actMods.reach * f.reachMul, 1);
        const pt = (s) => { const u = 1 - s;
          return [u * u * V.px + 2 * u * s * V.mx + s * s * V.hx, u * u * V.py + 2 * u * s * V.my + s * s * V.hy]; };
        const ang = Math.atan2(V.hy - V.py, V.hx - V.px);
        if (first && !this.over && f.alive){
          /* THE CLOSE. The simulation closed the window and the chain is
             back at its rest length from the next frame: the vine beyond it
             breaks off where it stood and falls -- a length of dead vine and
             its leaf pair per station. At the match's end the chain stays
             where it froze and withers in place; on the caster's death the
             shatter owns it. */
          const L1 = f.w.reach * this.actMods.reach * (1 - CONFIG.chain.hilt);
          for (let k = Math.max(1, Math.ceil(L1 / ST)); k * ST < V.d - 18; k++){
            const p = pt(k * ST / V.d);
            f.twineBits.push({ x: p[0], y: p[1], a: ang, stem: 1, t: 0, life: 1.5,
                               vx: (shellHash(9821 + f.side, k) - 0.5) * 70,
                               vy: -20 - 50 * shellHash(9823 + f.side, k),
                               spin: (shellHash(9825 + f.side, k) - 0.5) * 8 });
          }
        }
        f.twineFade = Math.max(0, f.twineFade - dt / 0.8);
        f.twineOut += dt;
        /* THE BROWN RUNS HEAD TO HAFT, and each leaf pair it passes lets go:
           the same stations `drawTwineWither` draws, on the chain as it is. */
        if (!first && f.alive){
          const fr = Math.min(1, f.twineOut / 0.8 / 0.75);
          const n = Math.max(0, Math.floor((V.d - 18) / ST));
          let passed = 0;
          for (let k = 1; k <= n; k++) if (k * ST >= (1 - fr) * V.d) passed++;
          while (f.twineDrop < passed){
            const k = n - f.twineDrop++;
            if (k < 1) break;
            const p = pt(k * ST / V.d);
            f.twineBits.push({ x: p[0], y: p[1], a: ang, stem: 0, t: 0, life: 1.5,
                               vx: (shellHash(9827 + f.side, k) - 0.5) * 60,
                               vy: -10 - 30 * shellHash(9829 + f.side, k),
                               spin: (shellHash(9831 + f.side, k) - 0.5) * 7 });
          }
        }
      }
    }
  }
'''),

("tendril picture: the root's beat",
 '''            T.rootSec += hold;
''',
 '''            T.rootSec += hold;
            /* THE DIRECTOR HAS TO BE TOLD (brief stage 6: "a ball stopping
               dead is a moment"). A control event with no damage and no
               contact, so nothing else in the frame files anything -- Paradox's
               hold and Ravelbone's catch file the same beat. Written to a list
               the simulation never reads, and no hit stop. */
            this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                        w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
'''),

('tendril picture: the held-ball guard',
 '''    if (f.pin > 0 && !f.pinFree){
      /* HELD BY THE STASIS FIELD. `pinFree` is the guard and it is not
''',
 '''    /* AND NOT ON A BALL TENDRIL'S ROOT HOLDS (v68 section 7, open decision
       6): that hold has its own picture, the shoots out of the floor
       (`_twineRoot`). `twineHeld` is presentation state, 1 exactly while
       the root's pin holds; `pinFree` stays 0, so the weapon is locked. */
    if (f.pin > 0 && !f.pinFree && !(f.twineHeld > 0)){
      /* HELD BY THE STASIS FIELD. `pinFree` is the guard and it is not
'''),

("tendril picture: drawWeapon's vine hook",
 '''    if (f.w.mode === "chain"){
      /* chain links from the relic to the head, then the head itself */
''',
 '''    if (f.w.mode === "chain"){
      /* chain links from the relic to the head, then the head itself */
      /* TENDRIL'S VINE (v68 section 8.1): while the window stands the vine
         draws itself (`drawTwineWeapon`) off the chain's own pivot and head --
         the line the bite tests. `ultVine` is null on every other relic, so
         this is one comparison on a field nothing else writes. */
      if (f.ultVine && !m.over && f.alive && this.drawTwineWeapon(m, f, reach, dim)) return;
'''),

("tendril picture: drawWeapon's wither hook",
 '''        SHAPES.flailHead(c, f.w.artW, pal, f.headSpin);
      }
''',
 '''        SHAPES.flailHead(c, f.w.artW, pal, f.headSpin);
      }
      /* ...AND AS IT WITHERS, over the chain drawn above at its tested
         length: the vine browns head to haft and lets go (`drawTwineWither`).
         `twineFade` is 0 on every other relic. */
      if (f.twineFade > 0 && !(f.ultVine && !m.over)){
        c.shadowBlur = 0; c.translate(-f.headX, -f.headY);
        this.drawTwineWither(m, f, dim);
      }
'''),

('tendril picture: the ground call',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* TENDRIL'S GROUND (v68 section 8.1): the leaf motes off the vine and the
       root's stalks out of the floor. The WORLD pass and under both balls;
       nothing of it reaches the bloom (CLAUDE.md section 4.1c). */
    if (__world) this.drawTwine(m);
'''),

('tendril picture: the over-fighter call',
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* TENDRIL OVER BOTH FIGHTERS: the window's rim on the caster, a bite's
       thorn flash on the foe's rim, the root clenched round the held ball and
       the wither's falling leaves. World pass, source-over (v68: the flash
       is source-over), so the white sanctified shell is never lit away. */
    this.drawTwineTop(m);
'''),

('tendril picture: twineCurve / twineLeaf',
 '''const _glowCache = new Map();
''',
 '''/* TENDRIL'S CURVE (v68 section 8.1): the chain's own quadratic from the
   pivot to the head -- the slack bow `drawWeapon` gives it -- scaled by `k`
   (1 the chain's bow, 0 the straight line the bite tests). A pure function
   of the fighter, read by the wither's picture and by `tickTwine`, so the
   leaves let go where they are drawn. */
function twineCurve(f, reach, k){
  const px = f.pivX ?? f.x, py = f.pivY ?? f.y;
  const dx = f.headX - px, dy = f.headY - py, d = Math.hypot(dx, dy) || 1;
  const chainLen = reach * (1 - CONFIG.chain.hilt);
  const bow = clamp(1 - d / chainLen, 0, 1) * chainLen * 0.55 * -Math.sign(f.headAngVel || 1) * k;
  return { px, py, hx: f.headX, hy: f.headY, d,
           mx: px + dx * 0.5 - (dy / d) * bow, my: py + dy * 0.5 + (dx / d) * bow };
}
/* One leaf, base at (x, y), pointing along `a`: added to the current path. */
function twineLeaf(c, x, y, a, L, W){
  const ux = Math.cos(a), uy = Math.sin(a);
  c.moveTo(x, y);
  c.quadraticCurveTo(x + ux * L * 0.5 - uy * W, y + uy * L * 0.5 + ux * W, x + ux * L, y + uy * L);
  c.quadraticCurveTo(x + ux * L * 0.5 + uy * W, y + uy * L * 0.5 - ux * W, x, y);
}

const _glowCache = new Map();
'''),

('tendril picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ---------------------------------------------------------- THE VINE ---
     TENDRIL (v68 section 8.1). THE CAST: the chain greens from haft to head
     over 0.30s -- the haft to bark, `dark` with a living `core` seam; each
     station of the chain sprouts its leaf pair and its thorn as the green
     passes it; the head is wrapped in bramble as it arrives -- and the
     chain's slack bow lets go, because the vine is drawn ON THE LINE THE
     BITE TESTS, pivot to head (in the window that bow is a median 0.7 units
     off the line and past the bite's 8 on 2% of steps, so it is a small
     move, but it is the true one). THE REACH IS THE ANIMATION: nothing but the
     chain's own pivot and head moves it (`reachMul` moves the haft, the vine
     and the hit segment together), and the LEAF SCALE -- a pair every 12
     units from the pivot, the newest growing in -- counts its length. Its
     leaves stand ~8 units off the axis, which is the bite's own reach
     (`vineW`): where the leaves touch the foe, it bites. A BITE flashes
     thorns on the foe's rim where the line is nearest it and tags ENTANGLE
     with its count. THE TELL is a thin green rim on the caster's shell and
     the vine itself. THE WITHER: brown runs head to haft over 0.4s over the
     chain, which is back at its rest length; the vine beyond it breaks off
     and falls, and every leaf pair the brown passes lets go. THE ROOT: four
     shoots out of the floor, up the held ball's rim, clenched for the pin
     and wilting as it runs out -- in place of Paradox's hexagon.

     IT HANGS OFF THE FIGHTER (`twineFade`, `twineAge`, `twineOut`, the
     records, `twineHeld` on the quarry), never `m.ultFx` (open item 25).
     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- shellHash and
     the clocks -- and nothing here writes a field the simulation reads. */
  drawTwine(m){
    const a = m.a, b = m.b;
    if (!a.twineMotes.length && !b.twineMotes.length
        && !(a.twineRootFade > 0) && !(b.twineRootFade > 0)) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.twineMotes.length){
        /* THE LEAF MOTES: shed along the vine, drifting down and swaying */
        c.fillStyle = f.aff.glow;
        for (const q of f.twineMotes){
          const s = q.t * 0.5, k = q.t / 2.2, h = shellHash(9841 + f.side, q.n);
          const x = q.x + Math.sin(s * 3.3 + h * 6.28) * 5 + (h - 0.5) * 18 * s;
          const y = q.y + 20 * s + 8 * s * s;
          c.globalAlpha = 0.85 * (1 - k) * Math.min(1, k * 8);
          c.beginPath(); twineLeaf(c, x, y, s * 2.2 + h * 6.28, 4.2, 1.7); c.fill();
        }
      }
      if (f.twineRootFade > 0) this._twineRoot(m, f, 0);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  drawTwineTop(m){
    const a = m.a, b = m.b;
    if (!(a.twineFade > 0) && !(b.twineFade > 0) && !a.twineFlash.length && !b.twineFlash.length
        && !a.twineBits.length && !b.twineBits.length
        && !(a.twineRootFade > 0) && !(b.twineRootFade > 0)) return;   // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR, A = CONFIG.arena, n = m.inset || 0, ST = 12;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const P = f.aff, foe = f === a ? b : a;
      /* THE WINDOW'S TELL: a thin green rim on the caster's shell */
      if (f.alive && f.twineFade > 0){
        const on = (f.ultVine && !m.over) ? Math.min(1, f.twineAge / 0.6) : f.twineFade;
        c.globalAlpha = 0.85 * on; c.strokeStyle = P.core; c.lineWidth = 2.4;
        c.beginPath(); c.arc(f.x, f.y, R + 2.2, 0, TAU); c.stroke();
      }
      /* A BITE: four thorns flash out of the foe's rim where the vine
         touches it, glow over a dark edge, 0.12s. No freeze (v67). */
      if (f.twineFlash.length && foe.alive){
        for (const F of f.twineFlash){
          const k = F.t / 0.24, bx = foe.x + Math.cos(F.a) * (R - 2), by = foe.y + Math.sin(F.a) * (R - 2);
          c.globalAlpha = 1 - k * k;
          c.beginPath();
          for (const o of [-0.7, -0.3, 0.3, 0.7]){
            const q = F.a + o, L = 20 * (Math.abs(o) > 0.5 ? 0.7 : 1) * (1 + 0.3 * (1 - k));
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
      if (f.twineRootFade > 0) this._twineRoot(m, f, 1);
      /* THE WITHER'S LEAVES, AND THE VINE THAT BROKE OFF, falling */
      if (f.twineBits.length){
        for (const d of f.twineBits){
          const s = d.t * 0.5, k = d.t / d.life;
          c.save();
          c.translate(d.x + d.vx * s, d.y + d.vy * s + 420 * s * s);
          c.rotate(d.a + d.spin * s);
          c.globalAlpha = (1 - k * k) * 0.95;
          if (d.stem){
            c.beginPath(); c.moveTo(-ST / 2, 0); c.lineTo(ST / 2, 0);
            c.strokeStyle = "#2A2012"; c.lineWidth = 5.6; c.stroke();
            c.strokeStyle = "#6E5B2E"; c.lineWidth = 2.4; c.stroke();
          }
          c.beginPath();
          twineLeaf(c, 0, -1.5, -0.95, 7, 2.9); twineLeaf(c, 0, 1.5, 0.95, 7, 2.9);
          c.fillStyle = "#8A7A3A"; c.fill();
          c.strokeStyle = "#2A2012"; c.lineWidth = 1; c.stroke();
          c.restore();
        }
      }
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE ROOT: `part` 0 the stalks out of the floor (under both balls), 1 the
     clench round the rim (over them). The shoots grow up in 0.12s, close
     round the rim in 0.1s more, hold for the pin, dry through its last 30%,
     and fade 0.2s after it lets go. The school's vine grammar (`_stEntangle`):
     `dark` strands, a `core` seam, `core` tips; the CASTER's school, so it
     is verdant on whatever ball it holds. In mid-air the stalks still come
     up from the floor -- the held ball is standing on them (Canopy's aerial
     roots). */
  _twineRoot(m, f, part){
    const c = this.ctx, R = CONFIG.physics.ballR, A = CONFIG.arena, P = AFFINITIES.verdant;
    const yF = A.h - (m.inset || 0);
    const grow = Math.min(1, f.twineHeldAge / 0.24);
    const cl = clamp((f.twineHeldAge - 0.24) / 0.2, 0, 1), ce = 1 - (1 - cl) * (1 - cl);
    const left = f.twineHeld ? clamp(f.pin / Math.max(0.01, f.pinMax || 1), 0, 1) : 0;
    const wilt = clamp((0.3 - left) / 0.3, 0, 1);
    const dk = mix(P.dark, "#2A2012", wilt), sm = mix(P.core, "#6E5B2E", wilt);
    c.globalAlpha = f.twineRootFade;
    for (let i = 0; i < 4; i++){
      const sd = i < 2 ? -1 : 1, o = i % 2;
      const qa = sd < 0 ? Math.PI - (o ? 0.62 : 0.16) : (o ? 0.62 : 0.16);    // where it meets the rim
      const cx = f.x + Math.cos(qa) * (R + 1.5), cy = f.y + Math.sin(qa) * (R + 1.5);
      if (part === 0){
        /* up out of the floor, then climbing onto the rim along it, so the
           clench carries on the way the stalk was already going */
        const fx = f.x + sd * R * (o ? 0.45 : 1.25), fy = Math.max(yF, cy), h = fy - cy;
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
  }

  /* THE STANDING VINE, from `drawWeapon`: the haft, the vine, the head,
     whole. Returns true. */
  drawTwineWeapon(m, f, reach, dim){
    const c = this.ctx, R = CONFIG.physics.ballR, P = f.aff, W = f.w.artW;
    const g = Math.min(1, f.twineAge / 0.6);
    const V = twineCurve(f, reach, 1 - g);             // the chain's bow lets go as it greens
    const ux = Math.cos(f.theta), uy = Math.sin(f.theta);
    const hx0 = f.x + ux * R * 0.40, hy0 = f.y + uy * R * 0.40, hw = f.w.width * 0.26;
    const Lh = Math.hypot(V.px - hx0, V.py - hy0);
    const dF = g * (Lh + V.d + 18);                // the green's front, from the butt
    const sF = clamp((dF - Lh) / V.d, 0, 1);
    c.save();
    /* THE STUN DIMS THE HAFT ONLY, as it does the chain's (`drawWeapon` sets
       the alpha back to 1 after the haft): a stunned vine still turns and
       still bites, so it is not drawn as if it had stopped. */
    c.globalAlpha = dim;
    c.lineCap = "round"; c.lineJoin = "round";
    this._twineHaft(c, hx0, hy0, V.px, V.py, hw, P, clamp(dF / Math.max(1, Lh), 0, 1), 0);
    c.globalAlpha = 1;
    if (sF < 1) this._twineLinks(c, f, V, sF);
    this._twineBody(c, m, f, V, P, sF, dF - Lh, 0, 0, 2.2 * g);
    c.save();
    c.translate(f.headX, f.headY);
    c.shadowColor = P.core; c.shadowBlur = 22;
    if (!litWeapon(c, 'flailHead', W, W, P, f.headSpin, 0)) SHAPES.flailHead(c, W, P, f.headSpin);
    c.shadowBlur = 0;
    this._twineBramble(c, W, P, f.headSpin, clamp((dF - Lh - V.d) / 18, 0, 1), 0);
    c.restore();
    c.restore();
    return true;
  }

  /* THE WITHER, over the grey chain `drawWeapon` has just drawn at its tested
     length: the vine on the chain's own curve, brown running head to haft
     (reaching the haft at three quarters of the 0.4s), then fading, so the
     chain is grey again. */
  drawTwineWither(m, f, dim){
    const c = this.ctx, R = CONFIG.physics.ballR, P = f.aff, W = f.w.artW;
    const b = Math.min(1, f.twineOut / 0.8), fr = Math.min(1, b / 0.75);
    const q = clamp((b - 0.6) / 0.4, 0, 1), al = 1 - q * q * (3 - 2 * q);
    if (!(al > 0.01)) return;
    const V = twineCurve(f, f.w.reach * m.actMods.reach * f.reachMul, 1);
    const ux = Math.cos(f.theta), uy = Math.sin(f.theta);
    const hx0 = f.x + ux * R * 0.40, hy0 = f.y + uy * R * 0.40, hw = f.w.width * 0.26;
    c.save();
    c.globalAlpha = al * dim;
    c.lineCap = "round"; c.lineJoin = "round";
    this._twineHaft(c, hx0, hy0, V.px, V.py, hw, P, 1, clamp((fr - 0.8) / 0.2, 0, 1));
    c.globalAlpha = al;
    this._twineBody(c, m, f, V, P, 1, 1e9, f.twineDrop, fr, 0);
    c.translate(f.headX, f.headY);
    this._twineBramble(c, W, P, f.headSpin, 1 - b, Math.min(1, fr * 3));
    c.restore();
  }

  /* The haft: the steel as `drawWeapon` draws it, and the BARK over it from
     the butt to `gk` of its length -- `dark` (v68: the steel goes to dark,
     not to white), a living `core` seam, a lit `glow` ridge, turns of vine
     where the grip was, and the knot the vine grows from. `bk` dries it. */
  _twineHaft(c, hx0, hy0, px, py, hw, P, gk, bk){
    const L = Math.hypot(px - hx0, py - hy0) || 1, ux = (px - hx0) / L, uy = (py - hy0) / L;
    const nx = -uy, ny = ux, al0 = c.globalAlpha;
    const quad = (e, w0, w1, fill) => {
      const x1 = hx0 + ux * L * e, y1 = hy0 + uy * L * e, we = w0 + (w1 - w0) * e;
      c.beginPath();
      c.moveTo(hx0 + nx * w0, hy0 + ny * w0); c.lineTo(x1 + nx * we, y1 + ny * we);
      c.lineTo(x1 - nx * we, y1 - ny * we); c.lineTo(hx0 - nx * w0, hy0 - ny * w0);
      c.closePath(); c.fillStyle = fill; c.fill();
    };
    if (gk < 1){
      quad(1, hw * 1.35, hw * 0.95, "#2C242F");
      quad(1, hw * 1.00, hw * 0.66, P.steel);
      c.globalAlpha = al0 * 0.45; quad(1, hw * 0.34, hw * 0.22, "#FFFFFF"); c.globalAlpha = al0;
      c.strokeStyle = "#00000066"; c.lineWidth = hw * 0.34;
      for (let i = 1; i <= 5; i++){
        const t = 0.10 + i * 0.11, gx = hx0 + ux * L * t, gy = hy0 + uy * L * t;
        c.beginPath(); c.moveTo(gx + nx * hw, gy + ny * hw); c.lineTo(gx - nx * hw, gy - ny * hw); c.stroke();
      }
      c.fillStyle = "#5B5060"; c.beginPath(); c.arc(hx0, hy0, hw * 1.5, 0, TAU); c.fill();
      c.fillStyle = P.core; c.beginPath(); c.arc(hx0, hy0, hw * 0.6, 0, TAU); c.fill();
    }
    if (!(gk > 0)) return;
    const bark = bk > 0 ? mix(P.dark, "#2A2012", bk) : P.dark;
    const seam = bk > 0 ? mix(P.core, "#6E5B2E", bk) : P.core;
    quad(gk, hw * 1.35, hw * 0.95, "#04140A");
    quad(gk, hw * 1.08, hw * 0.72, bark);
    const x1 = hx0 + ux * L * gk, y1 = hy0 + uy * L * gk;
    for (const [off, col, w, al] of [[hw * 0.28, seam, Math.max(1, hw * 0.22), 0.95],
                                     [-hw * 0.55, bk > 0 ? seam : P.glow, Math.max(0.8, hw * 0.12), 0.55]]){
      c.globalAlpha = al0 * al; c.strokeStyle = col; c.lineWidth = w;
      c.beginPath(); c.moveTo(hx0 + nx * off, hy0 + ny * off);
      c.lineTo(x1 + nx * off * 0.75, y1 + ny * off * 0.75); c.stroke();
    }
    c.globalAlpha = al0;
    c.strokeStyle = seam; c.lineWidth = hw * 0.26;
    for (let i = 1; i <= 3; i++){
      const t = 0.12 + i * 0.16;
      if (t > gk) break;
      const gx = hx0 + ux * L * t, gy = hy0 + uy * L * t;
      c.beginPath();
      c.moveTo(gx + nx * hw * 1.05 - ux * hw * 0.5, gy + ny * hw * 1.05 - uy * hw * 0.5);
      c.lineTo(gx - nx * hw * 1.05 + ux * hw * 0.5, gy - ny * hw * 1.05 + uy * hw * 0.5);
      c.stroke();
    }
    c.fillStyle = "#04140A"; c.beginPath(); c.arc(hx0, hy0, hw * 1.5, 0, TAU); c.fill();
    c.fillStyle = seam; c.beginPath(); c.arc(hx0, hy0, hw * 0.6, 0, TAU); c.fill();
    if (gk >= 1){
      c.fillStyle = bark; c.beginPath(); c.arc(px, py, hw * 1.1, 0, TAU); c.fill();
      c.strokeStyle = seam; c.lineWidth = Math.max(1, hw * 0.3);
      c.beginPath(); c.arc(px, py, hw * 0.75, 0.3, 2.6); c.stroke();
    }
  }

  /* The chain ahead of the green's front, as `drawWeapon` draws it: the
     swivel, the links the green has not reached, the loop the head hangs
     from. Only in the 0.30s of the greening. */
  _twineLinks(c, f, V, sF){
    const hw = f.w.width * 0.26;
    const at = (t) => { const u = 1 - t;
      return [u * u * V.px + 2 * u * t * V.mx + t * t * V.hx, u * u * V.py + 2 * u * t * V.my + t * t * V.hy]; };
    if (sF <= 0){
      c.strokeStyle = "#8E8496"; c.lineWidth = hw * 0.5;
      c.beginPath(); c.arc(V.px, V.py, hw * 1.05, 0, TAU); c.stroke();
      c.fillStyle = "#3A3038"; c.beginPath(); c.arc(V.px, V.py, hw * 0.5, 0, TAU); c.fill();
    }
    const links = 5, LR = f.w.width * 0.31;
    for (let i = 1; i <= links; i++){
      const t = i / (links + 0.6);
      if (t <= sF) continue;
      const [lx, ly] = at(t), [ax2, ay2] = at(Math.min(1, t + 0.02));
      const edge = i % 2 === 0;
      c.save();
      c.translate(lx, ly); c.rotate(Math.atan2(ay2 - ly, ax2 - lx));
      c.lineWidth = LR * 0.44; c.strokeStyle = "#241E29";
      c.beginPath(); c.ellipse(0, 0, LR * 1.28, edge ? LR * 0.34 : LR * 0.82, 0, 0, TAU); c.stroke();
      c.strokeStyle = edge ? "#7E7488" : "#B3AABD"; c.lineWidth = LR * 0.26;
      c.beginPath(); c.ellipse(0, 0, LR * 1.20, edge ? LR * 0.30 : LR * 0.76, 0, 0, TAU); c.stroke();
      c.restore();
    }
    if (sF < 0.9){
      const [tx2, ty2] = at(0.90);
      c.strokeStyle = "#9A90A4"; c.lineWidth = f.w.width * 0.10;
      c.beginPath(); c.arc((tx2 + V.hx) / 2, (ty2 + V.hy) / 2, f.w.width * 0.20, 0, TAU); c.stroke();
    }
  }

  /* The vine along `V` up to share `s1` of the chain (0 the pivot, 1 the
     head): a `dark` strand with a `core` seam and a `glow` light, and THE
     LEAF SCALE -- a leaf pair every 12 units from the pivot and a thorn
     between each, the newest growing in as the vine lengthens. `reachTo`:
     how far along the leaves have sprouted (the greening's front); `drop`:
     the pairs the wither has let go, from the head; `brown`: the share from
     the head that has died; `wave`: the living sway, pinned at both ends. */
  _twineBody(c, m, f, V, P, s1, reachTo, drop, brown, wave){
    const ST = 12, L = V.d, al0 = c.globalAlpha, sB = Math.min(s1, 1 - brown);
    const nx = -(V.hy - V.py) / L, ny = (V.hx - V.px) / L, ph = m.t * 5 + f.side * 1.7;
    const at = (s) => { const u = 1 - s, w = wave * Math.sin(Math.PI * s) * Math.sin(s * L / 11 - ph);
      return [u * u * V.px + 2 * u * s * V.mx + s * s * V.hx + nx * w,
              u * u * V.py + 2 * u * s * V.my + s * s * V.hy + ny * w]; };
    const run = (a0, a1, cols) => {
      if (!(a1 > a0)) return;
      const n = Math.max(2, Math.ceil(L * (a1 - a0) / 7)), pts = [];
      for (let i = 0; i <= n; i++) pts.push(at(a0 + (a1 - a0) * i / n));
      for (const [col, w, al] of cols){
        c.globalAlpha = al0 * al; c.strokeStyle = col; c.lineWidth = w;
        c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
        for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
        c.stroke();
      }
    };
    run(0, sB, [[P.dark, 7.2, 1], [P.core, 3.2, 1], [P.glow, 1.1, 0.55]]);
    run(sB, Math.min(1, s1), [["#2A2012", 6.4, 1], ["#6E5B2E", 2.8, 1]]);
    /* the leaf scale and the thorns, one path each */
    const nSt = Math.max(0, Math.floor((L - 18) / ST));
    const tan = (s) => { const p = at(Math.max(0, s - 0.01)), q = at(Math.min(1, s + 0.01));
      return Math.atan2(q[1] - p[1], q[0] - p[0]); };
    const leaves = [], thorns = [];
    for (let k = 1; k <= nSt; k++){
      const pos = k * ST, s = pos / L;
      if (s > sB || k > nSt - drop) break;
      const sc = Math.min(clamp((reachTo - pos) / (ST * 0.8), 0, 1), clamp((L - 18 - pos) / ST + 1, 0, 1));
      if (!(sc > 0.02)) continue;
      const p = at(s), a = tan(s), cn = Math.cos(a + Math.PI / 2), sn = Math.sin(a + Math.PI / 2);
      leaves.push([p, a, sc, cn, sn]);
      const s2 = (pos + ST / 2) / L;
      if (s2 < sB && pos + ST / 2 < L - 18) thorns.push([at(s2), tan(s2), sc, k % 2 ? 1 : -1]);
    }
    c.globalAlpha = al0;
    if (leaves.length){
      c.beginPath();
      for (const [p, a, sc, cn, sn] of leaves)
        for (const sd of [-1, 1])
          twineLeaf(c, p[0] + cn * sd * 1.6, p[1] + sn * sd * 1.6, a + sd * 0.95, 7.6 * sc, 7.6 * sc * 0.40);
      c.fillStyle = P.core; c.fill();
      c.strokeStyle = P.dark; c.lineWidth = 1.1; c.stroke();
    }
    if (thorns.length){
      c.beginPath();
      for (const [p, a, sc, sd] of thorns){
        const cn = Math.cos(a + Math.PI / 2) * sd, sn = Math.sin(a + Math.PI / 2) * sd, ca = Math.cos(a), sa = Math.sin(a);
        c.moveTo(p[0] + cn * 2.4 - ca * 1.3, p[1] + sn * 2.4 - sa * 1.3);
        c.lineTo(p[0] + cn * (2.4 + 4.6 * sc) + ca * 1.6, p[1] + sn * (2.4 + 4.6 * sc) + sa * 1.6);
        c.lineTo(p[0] + cn * 2.4 + ca * 1.3, p[1] + sn * 2.4 + sa * 1.3);
        c.closePath();
      }
      c.fillStyle = P.glow; c.fill();
    }
    c.globalAlpha = al0;
  }

  /* The head wrapped in bramble: three strands round it and seven thorns,
     turning with the head's own tumble. `k` how far round they have grown,
     `bk` dried. In the head's own frame. */
  _twineBramble(c, W, P, spin, k, bk){
    if (!(k > 0)) return;
    const r = W * 0.34;
    const dk = bk > 0 ? mix(P.dark, "#2A2012", bk) : P.dark;
    const cr = bk > 0 ? mix(P.core, "#6E5B2E", bk) : P.core;
    c.save();
    c.rotate(spin * 0.7 + 0.5);
    c.lineCap = "round";
    for (let j = 0; j < 3; j++){
      const rr = r * (0.98 + 0.10 * j);
      for (const [col, w] of [[dk, W * 0.095], [cr, W * 0.040]]){
        c.strokeStyle = col; c.lineWidth = w;
        c.beginPath(); c.ellipse(0, 0, rr, rr * 0.86, j * TAU / 3, 0, 2.4 * k); c.stroke();
      }
    }
    c.fillStyle = bk > 0 ? cr : P.glow;
    c.beginPath();
    for (let j = 0; j < 7 && j / 7 < k; j++){
      const a = j * TAU / 7 + 0.3, ux = Math.cos(a), uy = Math.sin(a), x = ux * r * 1.02, y = uy * r * 1.02;
      c.moveTo(x - uy * W * 0.035, y + ux * W * 0.035);
      c.lineTo(x + ux * W * 0.14, y + uy * W * 0.14);
      c.lineTo(x + uy * W * 0.035, y - ux * W * 0.035);
      c.closePath();
    }
    c.fill();
    c.restore();
  }

  drawMotes(m){
'''),

]

# The names stage 6 adds, free on the base (the Thicket owns vine/vines/tickVines/drawVines).
S6_NAMES = ("tickTwine", "drawTwine", "twineHeld", "twineCurve", '"bindweed-bite"',
            '"bindweed-root"', '"bindweed-wither"', 'w === "bindweed"')
# What stage 6's ADDED code may write: its own twine* fields (any object), the
# canvas, a tag's count, a record's clock, `taught`, and an oscillator's pitch.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("twine") or obj == "c" or prop == "val"
               or (prop == "t" and obj.endswith("]")) or obj == "taught"
               or (obj, prop) == ("frequency", "value"))

STAGE_OUT = {"1": "sc-bindweed", "2": "sc-vine", "3": "sc-bites", "4": "sc-tendril",
             "5": "sc-tendril-t3", "6": "sc-tendril-fx"}


def relic_row(code: str, rid: str) -> str:
    i = code.find(f'{{ id:"{rid}"')
    if i < 0:
        raise SystemExit(f"no {rid} in this source")
    return code[i:code.find("blurb:", i)]


def relic_ult(code: str) -> str:
    row = relic_row(code, RELIC)
    j = row.find("ult:{")
    k = row.find("},", j)
    return row[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4", "5", "6"], required=True)
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
    print(f"\nBINDWEED / TENDRIL -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Onslaught
    # through its stage 5.
    if "tickRam(dt){" not in code or "bank:8," not in code:
        raise SystemExit("wrong base: no Onslaught stage 3 -- not the chain tip")
    if "dmg:23," not in relic_row(code, "portcullis"):
        raise SystemExit("wrong base: Portcullis is not at its stage-5 blade")
    # AND THE DONOR'S FLAIL PROFILE IS STILL WHAT THIS BUILDER COPIES; THE
    # SCHOOL'S CHANNEL AND THE VERDANT FLAIL HEAD ARE WHERE THEY WERE.
    if DONOR_PHYS not in " ".join(relic_row(code, "gravemourn").split()):
        raise SystemExit("Gravemourn's flail profile has moved -- the donor is "
                         "not what this builder copies")
    for v in VERDANT:
        if "onHit:{ entangle:2 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, entangle 2")
    if not re.search(r'if \(key === "verdant"\)\s+return SHAPES\._fhGrown\(', code):
        raise SystemExit("SHAPES.flailHead no longer routes verdant to _fhGrown")
    # THE NAMES THIS RELIC ADDS ARE FREE ON THE BASE ("vine" is the Thicket's
    # SFX kind and `tickVines` its ticker, so neither is used here).
    if A.stage == "1":
        for name in ("ultVine", "vineTally", "vineWither", "tickTendril", 'kind:"tendril"'):
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  the chain tip (Onslaught stage 5); the donor's flail profile, the "
          "verdant channel and the verdant head hold")

    if A.stage == "1":
        if f'id:"{RELIC}"' in code:
            raise SystemExit("this source already carries Bindweed -- built")
        edits, want = S1, ult_block("1e9", 0, 0, 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultVine" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0, 0, 0)
        elif A.stage == "3":
            if "ultVine" not in code or "biteDmg:0, bitePer:0," not in code:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"], 0)
        elif A.stage == "5":
            if f'rootPer:{ULT["rootPer"]},' not in code or f'turn:{ULT["turn"]},' not in code:
                raise SystemExit("stage 5 goes on stage 4, once")
            edits = S5
            want = ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"], ULT["rootPer"]).replace(
                f'turn:{ULT["turn"]},', f'turn:{TUNED["turn"]},')
        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: Bindweed's ult block is stage 5's to
            # the character and its blade is stage 5's; none of stage 6's names
            # is in the source yet.
            want = ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"], ULT["rootPer"]).replace(
                f'turn:{ULT["turn"]},', f'turn:{TUNED["turn"]},')
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f'dmg:{TUNED["dmg"]},' not in relic_row(code, RELIC)):
                raise SystemExit("stage 6 goes on stage 5: Bindweed's ult block or blade is not stage 5's")
            for name in S6_NAMES:
                if name in code:
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            edits = S6
        else:
            if f'biteDmg:{ULT["biteDmg"]},' not in code or "rootPer:0," not in code:
                raise SystemExit("stage 4 goes on stage 3, once")
            edits, want = S4, ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"],
                                        ULT["rootPer"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Bindweed's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or shatters, and writes only
    # what S6_WRITE_OK names. It may READ `pinFree` (the held-ball guard); the
    # probe's [11] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|shatter|fireUlt|knock)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
    for label, _old, new in S1 + S2 + S3 + S4 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if "pinFree" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' touches "
                             "pinFree (the root is Grasp's write)")
    if len(re.findall(r'kind:"tendril"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one tendril ultimate")
    # THE REACH THE VINE GROWS IS READ WHERE IT MATTERS (scoped, as Canopy's).
    if A.stage != "1":
        if not re.search(r'if \(f\.w\.mode === "chain"\)\{[\s\S]*?const reach = f\.w\.reach \* mods\.reach \* f\.reachMul;', out_code):
            raise SystemExit("REFUSING TO WRITE -- the chain's reach does not carry reachMul")
        print("  ok    reachMul at the chain (site 2)")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one tendril ultimate, Bindweed's; no insert draws the RNG, "
          f"writes the shared weapon or touches pinFree; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
