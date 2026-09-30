#!/usr/bin/env python
"""COLDIRON / TEMPER -- the dwarven twinblade, a NEW relic. v103.

Built from `06-docs/v73/COLDIRON-BUILD-BRIEF.md` and
`dwarven-twinblade-design-v73.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-coldiron.html
    stage 2   the mass                    -> sc-coldiron-mass.html   (arm B)
    stage 3   sunder on a won bind        -> sc-coldiron-bind.html   (arm C)
    stage 4   the cap                     -> sc-coldiron-temper.html (arm D, cap 9)
    stage 5   the blade                   -> sc-coldiron-temper-b<blade>.html
    stage 6   picture, voice              -> sc-coldiron-temper-fx.html (no field: forge sparks drawn, v103 §7)

§1: "For a duration the twin blades are forged into cold iron. They are as
heavy as a warhammer, so every bind the twinblade takes, it wins -- the enemy's
weapon is thrown back instead of its own -- and each bind it wins sunders the
enemy. While the iron holds, sunder stacks past its limit."

Declared (design §5, brief §0-§1):
  THE MASS    `f.massMul` (1 on every fighter, always, but Coldiron's window)
              multiplies `w.mass` at EVERY read of it in the engine, and the
              builder refuses if a read lacks it. The reads, all four sites:
                resolveClank's shares   `A.w.mass * A.massMul`, `B.w.mass * B.massMul`
                move's gravity          (w.mass * massMul + burden x burdenMass)
                the hit stop's gravity  the same term, character for character
                                        (the brief's "decayImpactOnly's gravity":
                                        the frozen path of `step`, beside it)
                the liquid's gravity    the same term (SLOSH; write-only picture,
                                        but it must feel the gravity the ball feels)
              `ballCollision` reads no mass; `massRef` is a constant (2.68), so no
              derivation of it exists to carry. The burden term is untouched: the
              multiplier is on `w.mass`, which is what the lab's write moved.
              Set at the cast to `ult.mass / w.mass` (5.0 / 1.1; 1.1 x that is 5
              exactly in doubles, so a bind is bit-identical to the lab's w.mass = 5),
              back to 1 at the close. The shared weapon is never written.
  A WON BIND  in `resolveClank`, after `aWins`: when the bind is decisive and the
              winner has `ultTemper`, the loser takes apply("sunder", bind, the
              winner's side letter). Nothing else in the clank changes; the clank
              files its own beat and nothing more.
  THE CAP     `f.sunderCap`, read by `apply` for sunder exactly as `bleedCap` is
              for hemorrhage; RECOMPUTED IN `tickTemper` FOR BOTH FIGHTERS EVERY
              FRAME from whether the OTHER fighter's window is open (Bloodletting's
              rule: no paired write to forget). Stacks above 6 when the window drops
              are not trimmed; they run out on sunder's own 5s clock (`apply`
              already refuses to add to a fighter over its ceiling). Every sunder
              that lands still refreshes that clock even when it adds nothing (the
              engine's whole-status expiry; the lab's `apply` did the same), so while
              the blade keeps landing they mostly outlast the window (v103 §3, an
              item for Rick in §6).
  THE WINDOW  8s on the window tickers' clock; nothing waits (design §5).

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm D at cap 9 (v103 §0, a scratch copy of the lab
that counts frozen steps).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CAP IS THE FOE'S OWN (the brief and design §5, explicit: "per-fighter,
     ... on the foe BEING sundered"). The lab lifted `STATUS.sunder.maxStacks`
     globally for the window, which also let a dwarven foe sunder COLDIRON past 6
     while its own window was open; the build does not. Twinshade's shades keep
     the status's 6 (the brief's "both fighters").
  2. A WON BIND SUNDERS THE LOSER OF THAT BIND (the brief's `loser.apply`). The
     lab sundered the opponent even when the bind was against one of Twinshade's
     shades; the two readings differ only while shades stand.
  3. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract, Rick's standing
     ruling); the brief wrote the Fighter. Sunder has no reader of its source.
  4. THE WINDOW CLOSES ON EITHER DEATH WHILE THE MATCH STILL RUNS (the lab's;
     the docs are silent), and the close restores the mass. That is a death in a
     kill flight (Ravelbone's wire, the Crucible's forge), the only live frames
     after a death. ON AN ORDINARY KILL THE WINDOW IS STILL SET AT `over`:
     `checkEnd` follows `tickTemper` in the killing step, and nothing ticks after
     `over`. No fight can change; a picture drawn off `f.ultTemper` must read
     `f.ultTemper && !m.over` (or treat `over` as the close).
  5. THE MASS IS SET AT THE CAST, so a bind on the cast's own frame is already
     iron (the lab's cast came between two steps, before the whole step it
     opened). The cap is the brief's per-frame recomputation, so a bind on the
     cast's frame still meets the 6 (one frame, and a foe under 6 anyway).
  6. THE MASS REACHES GRAVITY TOO (design §5: "the lab priced it in"): a mass-5
     ball falls with gravity x (5 / 2.68)^0.5 = 1.37 of the config's, where the
     twinblade's own 1.1 gives 0.64.
  7. NAMES. The brief's `f.ultIron` and `tickIron` are prefixes of the staff
     row's `ultIronfall` / `tickIronfall` (yert's branch), and its tally would
     have been `ironTally`, which Ironfall already uses: the window is
     `ultTemper`, the ticker `tickTemper`, the tally `temperTally`, the kind
     "temper" (the tickVine / tickVines trap; Bindweed's precedent). The brief's
     `massMul` and `sunderCap` are free on every link and kept.

THE CLOCK. The window runs on the window tickers' clock, which stops through a
hit stop (every window of the batch). The lab's ran through freezes. The brief
sketches the window as `f.ultIron = { t0, end }`, a match-time shape; the build
keeps `{t, dur}` with `t` advanced by `tickTemper` only, on the window tickers'
clock -- Rick's standing ruling for every window cadence ("they stop in a hit
stop") replaces the sketch's shape, not its 8 seconds.

STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
and sound are Code's picks under "you pick i overrule"; v103 §7):
  8. THE ANVIL CARRIES THE LOSER'S COUNT after the bind's sunder, the one its
     tag shows (2..9 at bind 2, cap 9) -- a Twinshade shade's when a shade
     loses the bind; a won bind at the cap (9 -> 9) still strikes, at 9's note.
  9. THE CLOSE VOICE IS THE CLOCK CLOSE'S (both alive): a death close (a kill
     flight) and a window still set at `over` play nothing and are left to the
     death voice (Zenith's, Canopy's and Onslaught's rule). The picture reads
     `ultTemper && !over` (reading 4), so the blades cool at the verdict.
 10. "THE SUNDER TAG ON THE FOE TICKING UP": a won bind prints the loser's
     count on its rim toward the bind, one sunder tag on the foe at a time (a
     tag already up takes the new count in place); the blade's own sunder tag
     carries its count while the foe's ceiling is raised (Bloodletting's rule
     one status along). Past 6 it prints in dwarven's glow, and the ball shows
     the flakes past 6, hot.
 11. "FORGE SPARKS OFF THE BLADES" ARE DRAWN, not an fx.js field: a field rides
     the one ultFx slot, which Coldiron holds for a median 0.65s of its 8s
     window, and it fires once, at the cast; 31 of 427 won binds came while the
     slot was still Coldiron's.
 12. THE SILHOUETTE: `_tbBuilt`, the dwarven twinblade route that only Coldiron
     draws, becomes two riveted cleavers (the rivets on the outline, open item
     34's rule); the window draws the same shape 1.4x wide in its iron palette.

THE BASE is asserted by CONTENT (the sites and features this builder needs),
never by which relic is last, so it re-applies on a later tip that carries other
new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "coldiron"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v103 §0)
    "dur": 8,         # "the window 8s every 16s"
    "mass": 5.0,      # "massMul 5.0/1.1 for the window" -- as heavy as a warhammer
    "bind": 2,        # "a won bind apply('sunder', 2, f)" -- stage 3
    "cap": 9,         # "the foe's sunderCap = 9 while the caster's window is open" -- stage 4
}
CAP0 = 6              # STATUS.sunder.maxStacks, asserted: the cap's inert value
TIP = "Blades of cold iron: it wins binds, and each win sunders past the cap"
# Widowmaker's twinblade profile, the lab's donor (the brief: "Widowmaker's
# twinblade profile"), and the lab's blade, 11.95, until stage 5.
PHYS = ('blades:[0,0.5], reach:62, width:8, artW:30, dmg:11.95, spin:5.7, '
        'mode:"spin", mass:1.1')
# THE DONOR IS ASSERTED BY ITS PHYSICAL PROFILE, NOT ITS BLADE. Coldiron's
# 11.95 is the lab's number, written here, and nothing reads Widowmaker's row;
# the batch's Widowmaker redesign (v106) moves Widowmaker's own blade, and this
# builder must still re-apply on a tip that carries it. Nor does it assert the
# other twinblades or the other dwarven relics: they are not what it needs.
DONOR = re.compile(r'blades:\[0,0\.5\], reach:62, width:8, artW:30, dmg:[0-9.]+, '
                   r'spin:5\.7, mode:"spin", mass:1\.1')
BLURB = ("A twinblade forged into cold iron: it wins every bind it takes, and every "
         "bind it wins sunders the foe past the cap.")
# Every name this relic adds; each must be free on the base at stage 1.
NAMES = ("ultTemper", "temperTally", "sunderCap", "massMul", "tickTemper", 'kind:"temper"',
         'id:"coldiron"', "temperW", "temperL")


def ult_block(charge, bind, cap) -> str:
    return (f'''    ult:{{ name:"Temper", charge:{charge}, kind:"temper", dur:{ULT["dur"]},
          mass:{ULT["mass"]},          // v73: the cold iron's weight (stage 2)
          bind:{bind},          // v73: sunder on a won bind (stage 3)
          cap:{cap},          // v73: the foe's sunder cap while the iron holds (stage 4)
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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH, the page cannot be checked")
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
# THE RELIC, APPENDED AT THE END OF THE WEAPONS ARRAY, ITS ULTIMATE STUBBED at
# charge 1e9 (the clock can never reach it, `fireUlt` never runs) --
# Starwarden's stage-1 pattern. The anchor is the "];" that closes the array and
# the comment that follows it, which names no relic, so a build carried before
# or after this one composes. Every other table keyed by relic id falls back,
# and SHAPES.twinblade already routes dwarven to `_tbBuilt`, which no shipped
# relic has drawn.
ROW_ANCHOR = '''
];
/* The single source of truth for "which status does this relic teach".'''

S1 = [

("coldiron joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 f'''
  /* COLDIRON / TEMPER (v73; built v103) -- THE DWARVEN TWINBLADE, a new
     relic. Widowmaker's twinblade profile and its blade, 11.95 (the lab's
     donor; stage 5 settles it), and the school's channel, onHit sunder 1.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its mass,
     the sunder on a won bind, then the cap. */
  {{ id:"coldiron", name:"Coldiron", aff:"dwarven", shape:"twinblade",
    {PHYS},
    onHit:{{ sunder:1 }},
{ult_block("1e9", 0, CAP0)}
    blurb:"{BLURB}" }},
''' + ROW_ANCHOR),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the iron has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Temper", charge:1e9, kind:"temper", dur:8,
''',
 f'''    ult:{{ name:"Temper", charge:{ULT["charge"]}, kind:"temper", dur:{ULT["dur"]},   // v73 stage 2: the blades turn to iron
'''),

("the fighter carries the iron, its mass and the sunder ceiling",
 '''    this.bleedCap = STATUS.hemorrhage.maxStacks;
''',
 '''    this.bleedCap = STATUS.hemorrhage.maxStacks;
    /* TEMPER (v73). `sunderCap` is the ceiling `apply` reads for SUNDER on
       this fighter, the way `bleedCap` is hemorrhage's: the status's own 6
       except while the OTHER fighter's cold iron holds, and `tickTemper`
       recomputes it for both fighters every frame -- no raise, no restore.
       `massMul` multiplies `w.mass` at every read of it in the engine (the
       clank's shares, `move`'s gravity, the hit stop's gravity, the liquid's):
       1 on every fighter always, and on Coldiron outside its window, so every
       product is the one it was. `ultTemper` is {t, dur} while the window runs,
       null otherwise: `tickTemper` returns after two short loops that change
       nothing. `temperTally` is the probe's count, cumulative over the fight;
       nothing in the simulation reads it. */
    this.sunderCap = STATUS.sunder.maxStacks;
    this.massMul = 1;
    this.ultTemper = null;
    this.temperTally = null;
'''),

("sunder reads the fighter's own ceiling",
 '''    const cap = key === "hemorrhage" ? this.bleedCap : ''',
 '''    /* SUNDER READS THE FIGHTER'S OWN CEILING TOO (TEMPER, v73): `sunderCap` is
       the status's 6 on every fighter in every match but the foe of a Coldiron
       whose window is open, and the not-trimmed rule below is the design's:
       stacks above 6 when the window drops run out on sunder's own clock. */
    const cap = key === "hemorrhage" ? this.bleedCap : key === "sunder" ? this.sunderCap : '''),

("the hit stop's gravity carries the iron's mass",
 '''        f.vy += HP.gravity * Math.pow((f.w.mass + f.burden * f.burdenMass)
''',
 '''        /* `massMul` (TEMPER, v73) is 1 but on Coldiron's window. */
        f.vy += HP.gravity * Math.pow((f.w.mass * f.massMul + f.burden * f.burdenMass)
'''),

("the liquid feels the gravity the ball feels",
 '''          (f.w.mass + f.burden * f.burdenMass) / _P.massRef, _P.massWeight));
''',
 '''          (f.w.mass * f.massMul + f.burden * f.burdenMass) / _P.massRef, _P.massWeight));   // massMul: TEMPER (v73)
'''),

("move's gravity carries the iron's mass",
 '''    f.vy += P.gravity * Math.pow((f.w.mass + f.burden * f.burdenMass)
''',
 '''    /* `massMul` (TEMPER, v73) is 1 but on Coldiron's window: cold iron falls
       like the warhammer it weighs as. The hit stop's gravity is this term,
       character for character. */
    f.vy += P.gravity * Math.pow((f.w.mass * f.massMul + f.burden * f.burdenMass)
'''),

("the clank weighs the iron",
 '''    const mA = A.w.mass, mB = B.w.mass;
''',
 '''    /* `massMul` (TEMPER, v73) is 1 on every fighter but a Coldiron inside its
       window, where 1.1 x 5.0/1.1 is 5 exactly: the lightest weapon weighs
       what a warhammer weighs. */
    const mA = A.w.mass * A.massMul, mB = B.w.mass * B.massMul;
'''),

("a bind the iron wins sunders the loser",
 '''    const aWins = shareA < shareB;
''',
 '''    const aWins = shareA < shareB;
    /* TEMPER (v73): EACH BIND THE COLD IRON WINS SUNDERS THE LOSER. Decisive
       and won by a fighter whose window is open: the loser of the bind takes
       `bind` sunder through its own ceiling, the source a side letter. Nothing
       else in the clank changes, and the clank files its own beat. `ultTemper`
       is null on every other fighter, so this is one false test. */
    const temperW = aWins ? A : B;
    if (decisive && temperW.ultTemper){
      const temperL = temperW === A ? B : A, T = temperW.temperTally, u = temperW.w.ult;
      T.won++;
      if (u.bind > 0){
        temperL.apply("sunder", u.bind, temperW === this.a ? "a" : "b");
        T.applied += u.bind;
      }
    }
'''),

("the cast forges the iron and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "temper"){
      /* TEMPER (v73). NOTHING RESOLVES HERE: the cast makes the blades cold
         iron for `u.dur` seconds. The mass is set now -- 1.1 x 5.0/1.1 is 5
         exactly -- so a bind on this very frame is already iron; `tickTemper`
         keeps the clock, closes the window and holds the foe's ceiling up.
         The shared weapon is never written. */
      f.ultTemper = { t: 0, dur: u.dur };
      f.massMul = u.mass / f.w.mass;
      if (!f.temperTally) f.temperTally = { casts: 0, frames: 0, won: 0, applied: 0 };
      f.temperTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the iron ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickTemper(dt);                // TEMPER (v73)
'''),

("tickTemper keeps the window and the ceiling",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================= THE COLD IRON =====
     v73 §1 / §5, brief §0-§1. While the window runs the twinblade weighs
     `ult.mass` (set at the cast; `massMul` carries it to every mass read) and
     every bind it wins sunders the loser (`resolveClank`). This keeps the
     clock -- the window tickers', so it freezes through a hit stop -- and
     closes the window at `dur` or on EITHER death, putting the mass back.

     THE CEILING, RECOMPUTED AND NEVER RESTORED (Bloodletting's rule, the
     design's §5): both fighters, every frame, whether or not anybody has
     cast. A fighter's `sunderCap` is `ult.cap` while the OTHER fighter's iron
     holds and the status's own 6 otherwise, so a fresh Match starts at 6, a
     window that expires puts it back on the same frame, and there is no
     paired write to forget. Stacks already above 6 when it drops are not
     trimmed: `apply` adds nothing to a fighter over its ceiling, and they run
     out on sunder's own 5s clock. Nothing here moves anybody, draws the RNG,
     stops the world or files a beat. */
  tickTemper(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultTemper;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){
        f.ultTemper = null;
        f.massMul = 1;
        continue;
      }
      f.temperTally.frames++;
    }
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a;
      f.sunderCap = foe.ultTemper ? foe.w.ult.cap : STATUS.sunder.maxStacks;
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("sunder on a won bind",
 '''          bind:0,          // v73: sunder on a won bind (stage 3)
''',
 f'''          bind:{ULT["bind"]},          // v73: sunder on a won bind (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the cap",
 f'''          cap:{CAP0},          // v73: the foe's sunder cap while the iron holds (stage 4)
''',
 f'''          cap:{ULT["cap"]},          // v73: the foe's sunder cap while the iron holds (stage 4)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief §2 stage 5: "Wide on 151 at 8.8 / 9.3 / 9.8. Expect 9-9.5").
# Both sides, two blocks, 1520 fights a point (relic_rate, every other relic a
# foe): 8.8 -> 48.7, 9.3 -> 48.4, 9.8 -> 54.9; a straight line through the six
# block readings crosses 50% at ~9.2. 9.3 is the measured point inside the
# brief's band and nearest the crossing (the design's own "crossing near 9.3").
# The brief names no knob for this stage, and none moves: nothing else changes.
BLADE = 9.3

S5 = [] if BLADE is None else [
("the blade: at the crossing",
 '''  { id:"coldiron", name:"Coldiron", aff:"dwarven", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:11.95,''',
 f'''  {{ id:"coldiron", name:"Coldiron", aff:"dwarven", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:{BLADE},'''),
]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v73 §6.1-6.2, brief §2 stage 6), picked on
# measurements under Rick's "you pick i overrule" by `coldiron_voice_lab.py`
# and the picture lab (v103 §7). Presentation only: engine_ab over all 39
# relics, Coldiron included, is the proof. The rows are byte-exact to the
# labs' own files (voice 3, picture 11; no two share an anchor, so none is
# merged); the picture rows alone reproduce the picture lab's stamp
# (94bb7580047f01bc) on sc-coldiron-temper-b93. Voice first, then picture; the
# other order writes the same bytes.
#   THE VOICE: the cast (fireUlt's own `ult`/coldiron call, which fell
#   through to rune-crack: the quench), the anvil on every won bind (inside
#   resolveClank's iron clause, after the loser's sunder, pitched by the
#   loser's count), and the close (a clock close with both alive; never on
#   a death, never after `over`). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickIron` in tickPresentation reads `ultTemper && !over`,
#   `temperTally.won` rising and the clank's own beat, and writes only its
#   own `iron*` fields, a tag's count and colour, and `taught`. The blades
#   quench, hold black iron 1.4x wide and cool back to steel; a won bind
#   rings the anvil ring and throws forge sparks; sunder past 6 prints and
#   spalls in the forge's glow; `_tbBuilt` (the dwarven twinblade, which
#   only Coldiron draws) becomes two riveted cleavers. No beat, no stop.
#   No fx.js field: the forge sparks are drawn (v103 §7, Rick's to overrule).
#   NAMES: the labs'. `tickIron` is a prefix of the staff row's
#   `tickIronfall` (not on this tip; the tickVine / tickVines trap), so
#   every stage-6 name check below is on identifier boundaries.
S6 = [

("Sfx: Coldiron's cast, anvil and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "coldiron"){                   // the blades are quenched
          /* COLDIRON'S CAST, THE QUENCH -- v73 §6.2: "a quench hiss into a low
             iron ring, 0.5s". STEAM, of 8, picked on the numbers by
             `coldiron_voice_lab.py` under Rick's "you pick i overrule" (v103).
             Coldiron had no arm and fell through to rune-crack, which Ironhail
             and Spellbreaker still use, so this ADDS arms before that fallback
             and leaves it alone.

             The hiss is a narrow noise band (q 2.5) falling from 7.5 to 5 kHz
             over 0.32 s with a 12 ms attack; the ring is an iron bar voiced in
             its overtones (sines on the note and its free-bar modes 2.76, 5.40
             and 8.93) on A2 (the score's tonic), entering under the hiss 80 ms
             in and ringing on alone. Audible 490 ms; the hiss leads the first
             100 ms (-1.1 dB re the whole) and is silent over the last 100
             audible ms, the ring's loudest 50 ms 70 ms after the hiss's; the
             loudest 50 ms -2.9 dB re Coldiron's own blow. Register at most
             0.79 (Emberedge's cast) against rune-crack, the dwarven and
             twinblade casts, the clank, the death voice and the blow. */
          const g = 0.4146, kr = 0.1353, D = 0.792, F = 110;
          this._sweep(t, { f0: 7500, f1: 5000, q: 2.5, gain: g, dur: 0.32, atk: 0.012 });
          for (const [r, k, d] of [[1, 1, 1], [2.76, 0.8, 0.8], [5.4, 0.6, 0.6], [8.93, 0.4, 0.45]])
            this._tone(t + 0.08, { freq: F * r, gain: g * kr * k, dur: D * d, type:"sine" }).frequency.value = F * r;
        } else if (w === "coldiron-anvil"){             // a bind won on the anvil
          /* THE ANVIL -- "an anvil strike (a hard metallic hit with a 0.3s
             ring, peak <= 0.6) over the engine's clank voice; pitch steps up
             with the sunder count" (v73 §6.2). SEMI, of 4
             (`coldiron_voice_lab.py`). `resolveClank` plays it on a won bind
             with `n`, the loser's sunder count after the bind's sunder, over
             the clank it lands on.

             A struck steel block (a triangle on the note, sines on its
             free-bar modes 2.76 and 5.40) under a 5 kHz contact click, a
             semitone a stack: A5 at count 1 to F6 at 9 (counts clamped to
             1..9, the ceiling while the iron holds). Audible 295-300 ms; peak
             at most 0.536 on any count or noise draw; +10.2 dB or more over
             the clank in its own band. Register at most 0.54 (the runic snap)
             against the clank, the blow, its crit, the wall tick, the runic
             snap, rune-crack and the cast. */
          const n = clamp(Math.round(p.n || 0), 1, 9), g = 0.2549, D = 0.549;
          const F = 880 * Math.pow(2, (n - 1) / 12);
          this._burst(t, { freq: 5000, q: 1, gain: g * 0.8, dur: 0.012, type:"bandpass" });
          for (const [r, k, d, y] of [[1, 1, 1, "triangle"], [2.76, 0.5, 0.6, "sine"], [5.4, 0.25, 0.35, "sine"]])
            this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type: y }).frequency.value = F * r;
        } else if (w === "coldiron-close"){             // and the iron cools
          /* THE RING DIES -- "the ring dying, 0.4s" (v73 §6.2). BARE, of 3
             (`coldiron_voice_lab.py`): the cast's own ring on A2 without its
             top mode (the first to die in a struck bar), not struck again --
             it starts at its loudest, -8.2 dB under the cast, and fades over
             395 ms, heard over the score by its 304 Hz mode (+3.1 dB over
             twice the score there). Register at most 0.76 (the death voice)
             against the clank, the blow, the death voice, rune-crack and the
             anvil. `tickTemper` plays it only when the window closes by its
             clock with both alive. */
          const g = 0.0228, D = 0.576, F = 110;
          for (const [r, k, d] of [[1, 1, 1], [2.76, 0.8, 0.8], [5.4, 0.6, 0.6]])
            this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;
        } else {                                        // rune-crack'''),

("resolveClank: the anvil voice on a won bind, after the loser's sunder, carrying its count",
 '''        T.applied += u.bind;''',
 '''        T.applied += u.bind;
        /* COLDIRON'S ANVIL (v73 §6.2: "an anvil strike ... over the engine's
           clank voice; pitch steps up with the sunder count"): on the won
           bind's own frame, after the loser has taken its sunder, carrying
           the loser's count -- the one its tag shows, 2..9 (the foe's, or a
           Twinshade shade's when a shade loses the bind). With `bind` 2
           every won bind reaches this line, the cap included (9 -> 9 still
           strikes). The clank below plays its own voice as it always has.
           Presentation only: SFX.play draws nothing, is a no-op headless, and
           nothing here is read back (coldiron_voice_lab: fights identical). */
        SFX.play("ult", { w: "coldiron-anvil", n: temperL.stacks("sunder") });'''),

('tickTemper: the close voice, when the window closes by its clock with both alive',
 '''        f.massMul = 1;''',
 '''        f.massMul = 1;
        /* TEMPER'S CLOSE (v73 §6.2: "the ring dying, 0.4s"): only when the
           window runs out BY ITS CLOCK with both fighters alive -- this
           clause's own test. A death closes it only in a kill flight, and a
           fight that ends with the window open never gets here (step() stops
           calling this), so both are left to the death voice, as Zenith's,
           Canopy's and Onslaught's closes are. Plain SFX.play; nothing is
           read back. */
        if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "coldiron-close" });'''),

('temper picture: fighter fields',
 '''    this.temperTally = null;
''',
 '''    this.temperTally = null;
    /* TEMPER'S PICTURE (v73 section 6.1), and none of it is the window: the
       blades cool for 0.4s after `ultTemper` is gone, and a won bind's ring
       and sparks outlive the bind, so the picture keeps its own state. On the
       FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast takes
       it: open item 25). Driven in `tickPresentation` (`tickIron`); nothing in
       the simulation reads any of it.
         ironFade -- 1 while the iron holds; eased to 0 over the cool
         ironAge  -- the presentation clock since the cast (the quench)
         ironOut  -- the presentation clock since the close (the cool)
         ironSeen -- `temperTally.won` as last seen (a rise is a won bind)
         ironRings  -- the anvil rings at the binds' contacts (records)
         ironSparks -- the forge sparks thrown off the blades (records) */
    this.ironFade = 0;
    this.ironAge = 0;
    this.ironOut = 0;
    this.ironSeen = 0;
    this.ironRings = [];
    this.ironSparks = [];
'''),

('temper picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickIron(dt);                  // TEMPER'S PICTURE (v73 section 6.1)
'''),

('temper picture: tickIron',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------------ TEMPER'S PICTURE ---
     v73 section 6.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.6 is the
     cast's 0.3s quench, 0.8 the close's 0.4s cool, 0.5 the anvil ring's
     0.25s. A WON BIND IS FOUND BY WATCHING `temperTally.won` RISE, so
     `resolveClank` makes no call for the picture; its contact is the clank's
     own beat read back (a won bind files no beat of its own). Through a hit
     stop the window's clock stops and this one keeps playing, so the quench,
     a ring and its sparks finish. THE IRON IS READ OFF `ultTemper && !over`:
     `tickTemper` never runs again once `over` is set, and on an ordinary kill
     the window is still open then, so the blades cool at the verdict; the
     caster's fall hands the ball to the shatter. Writes presentation fields,
     `tags` and `taught` only, and draws no rng (shellHash). */
  tickIron(dt){
    for (const f of [this.a, this.b]){
      const T = f.temperTally;
      if (!T && !(f.ironFade > 0)) continue;                    // <- zero burden
      const foe = f === this.a ? this.b : this.a, Rb = CONFIG.physics.ballR;
      for (let i = f.ironRings.length - 1; i >= 0; i--){
        f.ironRings[i].t += dt;
        if (f.ironRings[i].t >= 0.5) f.ironRings.splice(i, 1);
      }
      for (let i = f.ironSparks.length - 1; i >= 0; i--){
        f.ironSparks[i].t += dt;
        if (f.ironSparks[i].t >= f.ironSparks[i].life) f.ironSparks.splice(i, 1);
      }
      const Z = (this.over || !f.alive) ? null : f.ultTemper;
      if (Z){
        if (!(f.ironFade > 0) || f.ironOut > 0){ f.ironAge = 0; f.ironOut = 0; }   // a cast: the quench
        f.ironFade = 1;
        f.ironAge += dt;
      } else if (f.ironFade > 0){
        f.ironOut += dt;
        f.ironFade = f.alive ? Math.max(0, 1 - f.ironOut / 0.8) : 0;
      }
      if (T && T.won > f.ironSeen){
        f.ironSeen = T.won;
        const side = f === this.a ? 0 : 1;
        let B = null;
        for (let i = this.beats.length - 1, k = 0; i >= 0 && k < 32; i--, k++){
          const b = this.beats[i];
          if (b.kind === "clank" && b.decisive && b.t === this.t){ B = b; break; }
        }
        const hx = B ? B.x : (f.x + foe.x) / 2, hy = B ? B.y : (f.y + foe.y) / 2;
        /* THE ANVIL RING: six sparks struck out of the contact, turned by the
           bind's count, never by the rng. */
        f.ironRings.push({ x: hx, y: hy, a: shellHash(9901 + side, T.won) * TAU / 6, t: 0 });
        if (f.ironRings.length > 4) f.ironRings.shift();
        /* FORGE SPARKS OFF THE BLADES (the design's field, drawn: a particle
           field fires once, at the cast, on the one ultFx slot): 5 a blade,
           struck off the outer part of each edge and flung with the spin. */
        const L = f.w.reach * this.actMods.reach * f.reachMul + 6, sp = f.spinDir || 1;
        for (const off of (f.bladeSet || f.w.blades)){
          const a0 = f.theta + off * TAU, ca = Math.cos(a0), sa = Math.sin(a0);
          for (let j = 0; j < 5; j++){
            const key = T.won * 16 + j + Math.round(off * 8);
            const h1 = shellHash(9911 + side, key), h2 = shellHash(9913 + side, key);
            const r = Rb - 6 + L * (0.45 + 0.52 * h1), tv = sp * (150 + 170 * h2), rv = 50 + 110 * h1;
            f.ironSparks.push({ x: f.x + ca * r, y: f.y + sa * r,
                                vx: ca * rv - sa * tv, vy: sa * rv + ca * tv - 70,
                                t: 0, life: 0.7 + 0.5 * h2 });
          }
        }
        if (f.ironSparks.length > 40) f.ironSparks.splice(0, f.ironSparks.length - 40);
        /* THE SUNDER TAG ON THE FOE TICKS UP, with its count, on the foe's rim
           toward the bind. ONE SUNDER TAG ON THE FOE AT A TIME (Tendril's
           rule): the blades' own tags carry the count in the window too
           (`resolveHit`), so a tag already up there takes the new count in
           place instead of a second printing over it. Past 6 the count prints
           in the forge's glow (`statusTag`). */
        if (foe.alive && foe.hp > 0){
          const n = foe.stacks("sunder"), a = Math.atan2(hy - foe.y, hx - foe.x);
          const g = this.tags.find(g2 => g2.key === "sunder" && !g2.first && g2.life > 0.3
                                         && Math.hypot(g2.x - foe.x, g2.y - foe.y) < Rb * 3);
          if (g){
            const af = Object.values(AFFINITIES).find(q => q.status === "sunder");
            g.val = n;
            if (af) g.c = n > STATUS.sunder.maxStacks ? af.glow : af.core;
          } else {
            const first = !this.taught.sunder && !!STATUS.sunder.tip;
            if (first) this.taught.sunder = true;
            this.statusTag(foe.x + Math.cos(a) * Rb, foe.y + Math.sin(a) * Rb, "sunder", first, n);
          }
        }
      }
    }
  }

  tickWinnow(dt){
'''),

("temper picture: a sunder tag past 6 in the forge's glow",
 '''                     c: aff ? aff.core : "#EDE3D0",
''',
 '''                     /* PAST THE CAP IS A COLOUR (TEMPER, v73 section 6.1):
                        a SUNDER count above the status's own 6 -- which only a
                        foe under Coldiron's cold iron can reach -- prints in
                        the forge's glow, not the school's core. */
                     c: aff ? ((key === "sunder" && val > STATUS.sunder.maxStacks) ? aff.glow : aff.core)
                            : "#EDE3D0",
'''),

("temper picture: the blade's sunder tag carries its count in the window",
 '''                   : (k === "hemorrhage"
                      && foe.bleedCap > STATUS.hemorrhage.maxStacks)
                     ? foe.stacks("hemorrhage") : 0);
''',
 '''                   : (k === "hemorrhage"
                      && foe.bleedCap > STATUS.hemorrhage.maxStacks)
                     ? foe.stacks("hemorrhage")
                   /* AND SUNDER CARRIES ITS COUNT WHILE COLDIRON'S CEILING IS UP
                      (TEMPER, v73 section 6.1: "the sunder tag on the foe
                      ticking up"), Bloodletting's rule one status along: 7, 8
                      and 9 are only reachable in that window. Zero in every
                      match with no cold iron in it. */
                   : (k === "sunder" && foe.sunderCap > STATUS.sunder.maxStacks)
                     ? foe.stacks("sunder") : 0);
'''),

('temper picture: sunder past 6 on the ball',
 '''    if ((n = f.stacks("sunder")))     this._stSunder(m, f, R, n);
''',
 '''    if ((n = f.stacks("sunder")))     this._stSunder(m, f, R, n);
    /* TEMPER (v73): 7, 8 and 9 spall hot (`_stSunderPast`). */
    if (f.stacks("sunder") > STATUS.sunder.maxStacks) this._stSunderPast(m, f, R, f.stacks("sunder"));
'''),

('temper picture: the dwarven twinblade, two broad riveted cleavers',
 '''  /* DWARVEN. Bolted, and the point is a CHISEL -- the same tell as the dwarven
     greatsword, which is what makes the two read as one workshop. */
  _tbBuilt(c, L, W, p){
    const bh = W * 0.17;
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);
    SHAPES._twinDagger(c, L, W, p);
    c.fillStyle = iron; c.strokeStyle = dark;
    c.lineWidth = Math.max(1, W*0.030);
    c.beginPath();                                             // the chisel
    c.moveTo(L*0.86, -bh*0.62); c.lineTo(L*1.02, -bh*0.52);
    c.lineTo(L*1.02,  bh*0.52); c.lineTo(L*0.86,  bh*0.62);
    c.closePath(); c.fill(); c.stroke();
    c.fillRect(L*0.36, -bh*1.28, L*0.055, bh*2.56);            // a collar
    c.strokeRect(L*0.36, -bh*1.28, L*0.055, bh*2.56);
    c.fillStyle = dark;
    for (const rx of [0.50, 0.64, 0.78]){
      c.beginPath(); c.arc(L*rx, 0, W*0.048, 0, TAU); c.fill();
    }
  },

''',
 '''  /* DWARVEN. TWO BROAD RIVETED CLEAVERS (v73 section 6.1, first cut), and
     the end is still a CHISEL -- squared and cut back on the edge side, the
     dwarven greatsword's tell, so the two read as one workshop. Built to open
     item 34's rule: THE RIVETS ARE ON THE OUTLINE, NOT ON TOP. Three heads
     stand half out of the spine, in the same path as the blade, so they are
     part of the silhouette that spins; the old cut's three were dots on the
     centre line and read as nothing (|dL| 0.111 at the app's size, last of
     the six twinblades). The edge is a bright ground bevel under a honed line
     in the school's glow; the collar is a squared iron block. Coldiron is the
     only dwarven twinblade, and TEMPER draws this same shape in its iron
     palette, 1.4x wide (`drawIronWeapon`). */
  _tbBuilt(c, L, W, p){
    const iron = SHAPES._shade(p.steel, 0.70, 0.42);
    const dark = SHAPES._shade(p.steel, 0.22, 0.55);
    c.lineJoin = "round"; c.lineCap = "butt";
    c.fillStyle = SHAPES._shade(p.dark, 1.20, 0.30);            // wrapped grip
    c.fillRect(0, -W*0.085, L*0.30, W*0.17);
    c.strokeStyle = "#12100C"; c.lineWidth = Math.max(1, W*0.045);
    for (let i = 1; i <= 5; i++){
      const gx = L * 0.30 * (i/6);
      c.beginPath(); c.moveTo(gx, -W*0.085); c.lineTo(gx + L*0.028, W*0.085); c.stroke();
    }
    c.fillStyle = p.core;                                      // pommel
    c.beginPath(); c.arc(-L*0.018, 0, W*0.105, 0, TAU); c.fill();
    /* the cleaver: spine (-y) with the three rivet heads standing out of it,
       the squared chisel end, the bellied edge (+y), the heel */
    const x0 = L*0.35, x1 = L, ys = -W*0.20, ye0 = W*0.24, ye1 = W*0.38, rr = W*0.09;
    const RX = [0.52, 0.68, 0.84];
    const edge = () => {
      c.moveTo(x1 - L*0.045, ye1);
      c.quadraticCurveTo(L*0.62, ye1 + W*0.02, x0 + L*0.03, ye0);
    };
    const outline = () => {
      c.beginPath();
      c.moveTo(x0, ys);
      for (const rx of RX){ c.lineTo(L*rx - rr, ys); c.arc(L*rx, ys, rr, Math.PI, 0); }
      c.lineTo(x1, ys);
      c.lineTo(x1 - L*0.045, ye1);
      c.quadraticCurveTo(L*0.62, ye1 + W*0.02, x0 + L*0.03, ye0);
      c.lineTo(x0, ye0 * 0.55);
      c.closePath();
    };
    outline(); c.fillStyle = SHAPES._shade(p.steel, 1.2, 0.1); c.fill();
    c.save();
    outline(); c.clip();                                       // everything inside the blade
    c.save(); c.shadowBlur = 0; c.globalAlpha = SHAPES._lit(c);  /* world light */
    c.fillStyle = SHAPES._facet(p.steel, p.dark, 0.60);        // shadowed flat
    c.fillRect(x0 - 2, W*0.02, x1 - x0 + 4, W*0.12);
    c.restore();
    c.strokeStyle = p.bevel || SHAPES._shade(p.steel, 1.75, 0.1);   // the ground bevel
    c.lineWidth = W*0.20;
    c.beginPath(); edge(); c.stroke();
    c.fillStyle = SHAPES._shade(p.steel, 0.95, 0.2);           // the forged spine
    c.fillRect(x0, ys - rr, x1 - x0, rr + W*0.05);
    c.restore();
    for (const rx of RX){                                      // the rivet heads
      c.fillStyle = SHAPES._shade(p.steel, 1.25, 0.2);
      c.beginPath(); c.arc(L*rx, ys, rr * 0.62, 0, TAU); c.fill();
      c.fillStyle = dark;
      c.beginPath(); c.arc(L*rx + rr * 0.12, ys + rr * 0.12, rr * 0.30, 0, TAU); c.fill();
    }
    c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.05);  // the honed edge
    c.beginPath(); edge(); c.stroke();
    c.fillStyle = iron; c.strokeStyle = dark;                   // the collar
    c.lineWidth = Math.max(1, W*0.030);
    c.fillRect(L*0.30, -W*0.30, L*0.055, W*0.60);
    c.strokeRect(L*0.30, -W*0.30, L*0.055, W*0.60);
    outline(); c.strokeStyle = dark; c.lineWidth = Math.max(1, W*0.03); c.stroke();
  },

'''),

('temper picture: the iron palette',
 '''const _glowCache = new Map();
''',
 '''/* TEMPER'S IRON (v73 section 6.1): the palette a Coldiron blade is drawn in
   along the quench and the cool. `p` runs 0 (forge-hot, the cast's flash) ->
   1 (black iron: the school's `dark` flat, its steel edge -- the bevel and
   the honed line -- gone matte grey) -> 2
   (the school's own steel and glow, the cool done), quantized to 1/16, so
   this holds at most 33 palettes a school. `key` and `core` stay, so the
   shape routes as it does at rest and the glow sprite is the rest pose's. */
const _ironPal = new Map();
function ironPalette(aff, p){
  const q = Math.round(clamp(p, 0, 2) * 16) / 16, id = aff.key + "|" + q;
  let o = _ironPal.get(id);
  if (o) return o;
  const HOTF = "#F08A30", HOTE = "#FFF2C8";
  const IRONF = aff.dark, IRONE = SHAPES._shade(aff.steel, 0.80, 0.6), IRONB = SHAPES._shade(aff.steel, 1.0, 0.6);
  const BEV = SHAPES._shade(aff.steel, 1.75, 0.1);             // the rest pose's bevel (_tbBuilt)
  const fill = q <= 1 ? SHAPES._facet(HOTF, IRONF, q) : SHAPES._facet(IRONF, aff.steel, q - 1);
  const edge = q <= 1 ? SHAPES._facet(HOTE, IRONE, q) : SHAPES._facet(IRONE, aff.glow, q - 1);
  const bevel = q <= 1 ? SHAPES._facet(HOTE, IRONB, q) : SHAPES._facet(IRONB, BEV, q - 1);
  o = Object.assign({}, aff, { steel: fill, glow: edge, bevel });
  _ironPal.set(id, o);
  return o;
}

const _glowCache = new Map();
'''),

("temper picture: drawWeapon's iron hook",
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
''',
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
    /* TEMPER'S COLD IRON (v73 section 6.1): through the quench, the window
       and the cool the blades draw themselves (`drawIronWeapon`) off the same
       blade set, reach and angles `bladeSegments` tests. `ironFade` is 0 on
       every other relic, so this is one comparison on a field nothing else
       writes. `w` is never written: it is the mirror match's too. */
    if (f.ironFade > 0 && this.drawIronWeapon(m, f, reach, dim)) return;
'''),

('temper picture: the over-fighter call (world)',
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* TEMPER'S WON BINDS, over both fighters: the anvil ring at the contact
       and the forge sparks off the blades. World pass, source-over, so nothing
       of it reaches the bloom (CLAUDE.md section 4.1c). */
    this.drawIronTop(m);
'''),

('temper picture: drawIronWeapon / drawIronTop / _stSunderPast',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------ THE COLD IRON ---
     TEMPER (v73 section 6.1). THE CAST: the two blades QUENCH -- they flash
     forge-orange, white-hot along each edge, and cool to black iron over
     0.3s (the school's `dark` flat, its steel edge gone matte) while they
     thicken to 1.4x: the mass, visible. THE WINDOW: black iron. THE CLOSE:
     black back to steel over 0.4s, thinning as it goes, no debris; and the
     same at the verdict when the match ends with the window open. The ball
     does not change. IT HANGS OFF THE FIGHTER (`ironFade`, `ironAge`,
     `ironOut`), never `m.ultFx`. PRESENTATION ONLY: no rng, no spawnFx, no
     Math.random, and `w` (shared by the mirror match) is never written --
     the width is a local. */
  drawIronWeapon(m, f, reach, dim){
    const c = this.ctx, R = CONFIG.physics.ballR, L = reach + 6;
    const live = f.ultTemper && !m.over && f.alive;
    let p, k;
    if (live){ const u = clamp(f.ironAge / 0.6, 0, 1); p = u * u; k = u * u * (3 - 2 * u); }
    else { const v = clamp(f.ironOut / 0.8, 0, 1); p = 1 + v; k = 1 - v * v * (3 - 2 * v); }
    const pal = ironPalette(f.aff, p), W = f.w.artW * (1 + (1.4 - 1) * k);
    for (const off of (f.bladeSet || f.w.blades)){
      const a = f.theta + off * TAU;
      c.save();
      c.globalAlpha = dim;
      c.translate(f.x, f.y);
      c.rotate(a);
      c.translate(R - 6, 0);
      const _g = weaponGlow(f.w.shape, L, W, pal, f.drawK, 20);
      c.drawImage(_g.cv, _g.ox, _g.oy);
      if (!litWeapon(c, f.w.shape, L, W, pal, f.drawK, a)){
        const fn = SHAPES[f.w.shape];
        if (fn) fn(c, L, W, pal, f.drawK);
      }
      c.restore();
    }
    return true;
  }

  /* A WON BIND (v73 section 6.1): the engine's own clank already throws the
     loser's weapon back. Over it, the ANVIL RING -- six sparks struck
     radially out of the contact, white-hot in a glow sheath, 0.25s -- and
     the FORGE SPARKS thrown off both blades with the spin, falling. World
     pass, source-over; every record is placed by shellHash, and the sparks'
     flight is a pure function of their clock. */
  drawIronTop(m){
    const a = m.a, b = m.b;
    if (!a.ironRings.length && !b.ironRings.length
        && !a.ironSparks.length && !b.ironSparks.length) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round";
    for (const f of [a, b]){
      for (const q of f.ironRings){
        const u = clamp(q.t / 0.5, 0, 1), e = 1 - (1 - u) * (1 - u);
        const r0 = 5 + 24 * e, r1 = r0 + 6 + 12 * (1 - u), al = 1 - u * u;
        for (let i = 0; i < 6; i++){
          const t = q.a + i * TAU / 6, ct = Math.cos(t), st = Math.sin(t);
          c.globalAlpha = al * 0.85; c.strokeStyle = f.aff.glow; c.lineWidth = 4.6 - 2.2 * u;
          c.beginPath(); c.moveTo(q.x + ct * r0, q.y + st * r0); c.lineTo(q.x + ct * r1, q.y + st * r1); c.stroke();
          c.globalAlpha = al; c.strokeStyle = "#FFF3DA"; c.lineWidth = 2.0 - 0.9 * u;
          c.beginPath(); c.moveTo(q.x + ct * r0, q.y + st * r0); c.lineTo(q.x + ct * r1, q.y + st * r1); c.stroke();
        }
      }
      for (const q of f.ironSparks){
        const s = q.t * 0.5, u = q.t / q.life;
        const x = q.x + q.vx * s, y = q.y + q.vy * s + 260 * s * s;
        const vx = q.vx, vy = q.vy + 520 * s, sp = Math.hypot(vx, vy) || 1;
        const tl = Math.min(16, 3 + sp * 0.03);
        c.globalAlpha = clamp((1 - u) * 1.6, 0, 1);
        c.strokeStyle = u < 0.35 ? "#FFE9B8" : f.aff.glow; c.lineWidth = 2.0 - u;
        c.beginPath(); c.moveTo(x, y); c.lineTo(x - vx / sp * tl, y - vy / sp * tl); c.stroke();
      }
    }
    c.restore();
  }

  /* SUNDER PAST THE CAP (v73 section 6.1: "past the cap is a colour"). The
     six flakes are `_stSunder`'s; a ball the cold iron has sundered to 7, 8
     or 9 shows the rest here, spalled HOT -- the same flake in the forge's
     glow, the colour its tag prints in past 6. Stacks above 6 outlive the
     window on sunder's own clock, and so do these. Nothing on a ball at 6 or
     under. */
  _stSunderPast(m, f, R, n){
    const c = this.ctx, N = Math.min(12, n);
    const G = AFFINITIES.dwarven.glow;
    c.save();
    for (let i = 6; i < N; i++){
      const a   = shellHash(907 + f.side, i) * TAU;
      const wid = 0.26 + shellHash(929 + f.side, i) * 0.20;
      const lift = 2.6 + Math.sin(m.t * 3.1 + i * 1.9) * 1.1;
      const ca = Math.cos(a), sa = Math.sin(a);
      c.globalAlpha = 0.95;
      const sg = c.createRadialGradient(f.x + ca * R * 0.9, f.y + sa * R * 0.9, 0,
                                        f.x + ca * R * 0.9, f.y + sa * R * 0.9, R * wid * 1.6);
      sg.addColorStop(0, "#FFF6DC");
      sg.addColorStop(0.5, G + "AA");
      sg.addColorStop(1, G + "00");
      c.fillStyle = sg;
      c.beginPath();
      c.arc(f.x, f.y, R * 1.0, a - wid / 2, a + wid / 2);
      c.arc(f.x, f.y, R * 0.72, a + wid / 2, a - wid / 2, true);
      c.closePath(); c.fill();
      c.save();
      c.translate(f.x + ca * (R * 0.95 + lift), f.y + sa * (R * 0.95 + lift));
      c.rotate(a + Math.PI / 2);
      c.globalAlpha = 1;
      const fw = R * wid * 1.15, fh = R * 0.13;
      const fg = c.createLinearGradient(0, -fh, 0, fh);
      fg.addColorStop(0, "#FFF6DC");
      fg.addColorStop(0.55, G);
      fg.addColorStop(1, "#6A2E08");
      c.fillStyle = fg;
      c.beginPath();
      c.moveTo(-fw, 0);
      c.quadraticCurveTo(0, -fh * 2.0, fw, 0);
      c.quadraticCurveTo(0,  fh * 0.5, -fw, 0);
      c.closePath(); c.fill();
      c.strokeStyle = G; c.lineWidth = 1.6; c.stroke();
      c.restore();
    }
    c.restore();
  }

  drawMotes(m){
'''),

]

# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`tickIron` is a prefix of the staff row's `tickIronfall`).
S6_NAMES = ("tickIron", "drawIronWeapon", "drawIronTop", "ironPalette", "_ironPal",
            "_stSunderPast", "ironFade", "ironRings", "ironSparks", '"coldiron-anvil"',
            '"coldiron-close"', 'w === "coldiron"')
# What stage 6's ADDED code may write: its own iron* fields (any object), the
# canvas, a tag's count and colour, a record's clock, `taught`, and an
# oscillator's pitch.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("iron") or obj == "c" or prop == "val"
               or (obj, prop) == ("g", "c") or (prop == "t" and obj.endswith("]"))
               or obj == "taught" or (obj, prop) == ("frequency", "value"))


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def stage_out(stage: str) -> str:
    return {"1": "sc-coldiron", "2": "sc-coldiron-mass", "3": "sc-coldiron-bind",
            "4": "sc-coldiron-temper",
            "5": f"sc-coldiron-temper-b{str(BLADE).replace('.', '')}",
            "6": "sc-coldiron-temper-fx"}[stage]


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


# THE CAST'S OWN READ DEFINES THE MULTIPLIER (5.0 / 1.1); it is not a use of
# the mass, and it is the one `w.mass` read that must NOT carry massMul.
CAST_READ = "f.massMul = u.mass / f.w.mass;"


def mass_audit(code: str, cast: bool) -> int:
    """Every `.mass` read in the (comment-stripped) engine, the cast's aside:
    five `w.mass` reads at the four declared sites and the clank voice's
    `p.mass` parameter. Refuses anything else -- a new read is a site this
    build has not declared, and Coldiron's mass would not reach it."""
    if code.count(CAST_READ) != (1 if cast else 0):
        raise SystemExit(f"REFUSING -- the cast's mass read appears {code.count(CAST_READ)} times")
    c = code.replace(CAST_READ, "")
    reads = [c[m.start() - 12:m.end() + 22].replace("\n", " ") for m in re.finditer(r"\.mass\b", c)]
    n_w = len(re.findall(r"\bw\.mass\b", c))
    n_p = len(re.findall(r"\bp\.mass\b", c))
    if len(reads) != n_w + n_p or n_p != 1 or n_w != 5:
        raise SystemExit("REFUSING -- a `.mass` read this builder has not declared "
                         f"({n_w} w.mass, {n_p} p.mass, {len(reads)} in all; the "
                         "declared list is 5 + the clank voice's 1):\n  " + "\n  ".join(reads))
    return n_w


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
    if A.stage == "5" and BLADE is None:
        raise SystemExit("stage 5 is not settled yet: BLADE is None")

    # READ AS BYTES: read_text() turns CRLF into LF, so this refusal could never fire (found by
    # thornwake_build.py, v113; for an LF source the two reads are the same text, so no link moves).
    s0 = src_p.read_bytes().decode("utf-8")
    if "\r" in s0:
        raise SystemExit("the source has CRLF line endings -- not a chain link")
    s = s0
    print(f"\nCOLDIRON / TEMPER -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS ASSERTED BY CONTENT: the sites this builder edits and the
    # features it stands on, never which relic happens to be last.
    for need, why in (
            ("tickTendril(dt){", "no Tendril ticker (the anchor this ticker follows)"),
            ("resolveClank(A, B, hx, hy){", "no resolveClank"),
            ("const decisive = Math.abs(shareA - shareB) > 0.16;",
             "the clank's decisive rule is not the one the lab rebuilt"),
            ("const wA = Math.pow(mA, 1.7), wB = Math.pow(mB, 1.7), tot = wA + wB;",
             "the clank's shares are not mass^1.7"),
            ("this.bleedCap = STATUS.hemorrhage.maxStacks;", "no per-fighter bleed ceiling"),
            ("if (cur.stacks < cap) cur.stacks = Math.min(cap, cur.stacks + n);",
             "apply trims a fighter above its ceiling -- the not-trimmed rule is gone"),
            ("dmgTakenMul(){ return 1 + STATUS.sunder.taken * this.stacks(\"sunder\"); }",
             "sunder's damage-taken read has moved"),
            ("f.charge += dt;", "the charge is not pure normal-path time")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'sunder:\s*\{ name:"Sunder",\s+maxStacks:6, dur:5\.0, taken:0\.11,', code):
        raise SystemExit("wrong base: STATUS.sunder is not {6 stacks, 5s, +11%}")
    # THE DONOR'S TWINBLADE PROFILE (its physics, not its blade) IS STILL WHAT
    # THIS BUILDER COPIES, AND THE DWARVEN TWINBLADE ART IS WHERE IT WAS.
    if not DONOR.search(" ".join(relic_row(code, "widowmaker").split())):
        raise SystemExit("Widowmaker's twinblade profile has moved -- the donor is "
                         "not what this builder copies")
    if not re.search(r'if \(key === "dwarven"\)\s+return SHAPES\._tbBuilt\(', code):
        raise SystemExit("SHAPES.twinblade no longer routes dwarven to _tbBuilt")
    # EVERY MASS READ IS ONE THIS BUILDER KNOWS. On the base: five `w.mass`
    # reads at the four declared sites and the clank voice's `p.mass`
    # parameter. A new read anywhere is a site this build has not declared.
    mass_audit(code, cast=A.stage not in ("1", "2"))
    if A.stage == "1":
        for name in NAMES:
            if re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code):
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  the clank's mass rule, the per-fighter ceiling, the not-trimmed "
          "apply, STATUS.sunder, Widowmaker's physical profile and the dwarven "
          "twinblade art hold; every mass read is declared")

    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0, CAP0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultTemper" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0, CAP0)
        elif A.stage == "3":
            if "ultTemper" not in code or "bind:0," not in relic_ult(code):
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["bind"], CAP0)
        elif A.stage == "4":
            if f'bind:{ULT["bind"]},' not in relic_ult(code) or f"cap:{CAP0}," not in relic_ult(code):
                raise SystemExit("stage 4 goes on stage 3, once")
            edits, want = S4, ult_block(ULT["charge"], ULT["bind"], ULT["cap"])
        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: Coldiron's ult block is stage 5's to
            # the character and its blade is stage 5's; none of stage 6's names
            # is in the source yet (on identifier boundaries).
            want = ult_block(ULT["charge"], ULT["bind"], ULT["cap"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{BLADE}," not in relic_row(code, RELIC)):
                raise SystemExit("stage 6 goes on stage 5: Coldiron's ult block or blade is not stage 5's")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            edits = S6
        else:
            if f'cap:{ULT["cap"]},' not in relic_ult(code) or "dmg:11.95," not in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 4, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bind"], ULT["cap"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Coldiron's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or shatters, and writes only
    # what S6_WRITE_OK names. It READS the window, the tally and the clank's
    # beat; the probe's [8]-[9] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
    for label, _old, new in S1 + S2 + S3 + S4 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        # THE SHARED WEAPON (the mirror match shares one `w`): no insert writes
        # any field of it -- the art's width, the ult block and the on-hit row
        # included. Widened at stage 6 on the review's note (it missed a bare
        # `w.X *=`, w.width, w.artW, w.ult.* and w.onHit).
        if re.search(r"\bw\.(dmg|spin|reach|blades|mass|width|artW|ult|onHit)\b[\w.]*\s*[-+*/]?=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if "STATUS.sunder.maxStacks =" in ins or re.search(r"maxStacks\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes a "
                             "status's global ceiling")
    if len(re.findall(r'kind:"temper"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one temper ultimate")
    # THE MASS REACHES EVERY READ (design §5: "the builder refuses if any read
    # lacks it").
    mass_audit(out_code, cast=A.stage != "1")
    if A.stage != "1":
        mc = out_code.replace(CAST_READ, "")
        bare = [m.start() for m in re.finditer(r"\bw\.mass\b(?! \* [A-Za-z]+\.massMul\b)", mc)]
        if bare:
            raise SystemExit("REFUSING TO WRITE -- a `w.mass` read without massMul: "
                             + "; ".join(mc[i - 30:i + 30].replace("\n", " ") for i in bare))
        n_mm = len(re.findall(r"\bw\.mass \* [A-Za-z]+\.massMul\b", mc))
        if n_mm != 5:
            raise SystemExit(f"REFUSING TO WRITE -- {n_mm} massMul reads, the declared list is 5")
        # apply's ceiling line READS sunderCap for sunder. Asserted as a clause of
        # the line, not the whole line, so a later relic's own per-fighter
        # ceiling clause on the same line does not make this builder refuse.
        cap_lines = [ln for ln in out_code.splitlines() if re.match(r"\s*const cap = key === ", ln)]
        if len(cap_lines) != 1 or 'key === "sunder" ? this.sunderCap :' not in cap_lines[0]:
            raise SystemExit("REFUSING TO WRITE -- apply does not read sunderCap for sunder")
        print("  ok    massMul at all 5 w.mass reads (the clank x2, move, the hit stop, "
              "the liquid); apply reads sunderCap")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one temper ultimate, Coldiron's; no insert draws the RNG, uses "
          f"the ultFx slot or writes the shared weapon or a global ceiling; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
