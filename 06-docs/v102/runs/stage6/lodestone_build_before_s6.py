#!/usr/bin/env python
"""LODESTONE / REBUTTAL -- the runic warhammer, a NEW relic. v102.

Built from `06-docs/v70/LODESTONE-BUILD-BRIEF.md` and
`runic-warhammer-design-v70.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-lodestone.html
    stage 2   the hex on touch, no hurl   -> sc-lodestone-runes.html     (arm H)
    stage 3   the hurl                    -> sc-lodestone-rebuttal.html  (arm C)
    stage 4   (none: the brief has three stages)
    stage 5   the blade                   -> sc-lodestone-b205.html      (20.5)
    stage 6   picture, voice, field       (not written yet)

§1: "For a duration the four walls of the hall are runed. Every time the
enemy's ball touches a wall the rune under it flares, hexes them, and hurls
them straight back at the hammer. The hammer's own knock throws them into the
wall in the first place, so the fight becomes a rally: hit, wall, hurled back,
hit. The walls do no damage -- they hand the enemy back."

Declared (design §5, brief §0-§1):
  THE WINDOW  8s; `f.ultRunes = {t, dur, cd}`, null elsewhere. The brief's
              §1 gives the state as `{ t0, end, cd }`, which reads as
              timestamps; on this engine a timestamp sits on `m.t`, which runs
              through hit stops, so that shape IS the lab's clock (8
              match-seconds). It is built as `{t, dur, cd}`, `t` counted on the
              window tickers' clock -- the batch's standing ruling (THE CLOCK,
              below); v102 §2's lab-clock control prices the difference.
  A TOUCH     the foe's centre within inset + R + 1.5 of any side (the CURRENT
              inset: the runes walk in with the seals), the foe alive and not
              pinned, once per 0.5s. The engine clamps a ball at n + R, so this
              is a contact test, not a proximity one.
  THE HEX     foe.apply("hex", 1, side) per touch, the real status.
  THE HURL    foe.vx, vy = 700 x unit(caster - foe) -- an ASSIGNMENT, not an
              impulse. No damage, no resolveHit, no beat, no hit stop. Nothing
              writes f.stun or f.pin.
  The caster's own touches do nothing. The next cast waits for nothing.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm C (v102 §0, the census).

THE READINGS, where the build had to choose and the doc, the lab or the engine
decides:
  1. THE WINDOW CLOSES ON THE CLOCK OR EITHER DEATH (the lab closes on either
     death; the design is silent). A dead foe cannot touch anything, and a dead
     caster's runes hand the foe back to nobody. ON THIS ENGINE THE FOE-DEATH
     CLOSE IS UNREACHABLE: the only thing Lodestone does that can kill is a
     blow, in `tickHits`, after `tickRunes`; that step's `checkEnd` ends the
     match and `step` returns early from then on, so `tickRunes` never runs
     again. A kill by a blow therefore ENDS THE MATCH WITH `ultRunes` STILL SET
     (the lab closed on `m.over` as well). The simulation never reads it after
     the verdict; a picture must gate on `!m.over` (v102 §5). Kept as the lab's
     reading; the probe counts caster-death and foe-death closes apart.
  2. THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, touching or not, and starts
     clear at the cast (the lab's `cd = 0` at onCast; `cd -= dt` every window
     frame), so a foe already on a wall is touched on the first frame. ONE
     FRAME: `Z.t += dt` comes before the close test, so the cast step's own
     tick is window frame 1 and the 960th tick closes the window -- 959
     working frames where the lab's window is open for 960, 1/120s short on
     the window clock. Nothing measurable moves with it (v102 §0).
  3. A PINNED FOE IS NOT TOUCHED, and its frames still spend the cooldown
     (the lab's `cd -= dt` comes before its pin test and its return).
  4. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract, Rick's ruling);
     the lab passed the Fighter. Hex reads no source (no dps, no feed).
  5. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).
  6. THE HURL IS ASSIGNED ON THE WINDOW FRAME OF THE TOUCH, in the window
     tickers' slot (after `ballCollision`, before `tickHits`): a blow landing on
     that same frame knocks on top of the hurl. The lab assigned after the
     whole step, over the blow's knock. v102 §2 prices the order.
  7. THE HAMMER IS GRUDGEBEARER'S PROFILE AND ITS BLADE, 23.5, until stage 5
     (the lab's donor, `cell_ults_on.TYPE_DONOR`, and every shipped hammer's
     profile); the school's channel, onHit hex 1.
  8. THE BLURB is COMPOSED BY THE BUILD, not a quoted line: the batch's
     "A <type> that ..." pattern (Canopy's, Onslaught's, Tendril's builds did
     the same), from §1's words, "hurls them straight back at the hammer".
     The design's title line reads "The walls are runed: whoever touches one
     is hexed and hurled back at the hammer"; the card (68) is the brief's.

THE CLOCK. The window and the touch cooldown run on the window tickers' clock,
which stops through a hit stop (Corollary's, Daybreak's, Zenith's, Canopy's,
Onslaught's and Tendril's convention). The lab ran both through freezes, and
touched walls during them; v102 §2 measures what that is worth here.

THE BASE is asserted BY CONTENT: the window tickers' slot after Tendril's, the
anchors this builder needs, the donor's hammer profile, the runic channel, the
runic hammer head's route, hex's numbers and the wall clamp at n + R. It never
asserts which relic is last, so it re-applies on a tip that carries more.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "lodestone"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v102 §0)
    "dur": 8,         # "the window 8s every 16s"
    "pad": 1.5,       # "foe centre within inset + R + 1.5 on any side"
    "cd": 0.5,        # "once per 0.5s"
    "hex": 1,         # "apply("hex", 1, f)"
    "hurl": 700,      # "foe.vx, vy = 700 x unit(caster - foe)" -- stage 3
}
TIP = "The walls are runed: a foe that touches one is hexed and hurled back"
# Grudgebearer's hammer profile, the lab's donor (cell_ults_on.TYPE_DONOR) and
# the whole type's; dmg 23.5 is its blade, which stage 5 settles.
DONOR_PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.50, spin:1.6, '
              'mode:"spin", mass:5.0, knockMul:2.3')
PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.5, spin:1.6, '
        'mode:"spin", mass:5.0, knockMul:2.3')
HAMMERS = ("grudgebearer", "censer", "bulwarden", "shroudmaul", "ravelbone")
RUNIC = ("spellbreaker", "axiom", "foregone", "paradox")
BLURB = ("A hammer that runes the hall: whoever touches a wall is hexed and "
         "hurled straight back at the hammer.")
HEX_DEF = 'hex:        { name:"Hex",        maxStacks:5, dur:2.6, stunEvery:1.15, stunFor:0.20,'
CLAMP = "    const loX = n + R, hiX = A.w - n - R, loY = n + R, hiY = A.h - n - R;\n"
# The names this relic adds; each must be free on the base.
NAMES = ("ultRunes", "runeTally", "tickRunes", 'kind:"runes"', 'id:"lodestone"')


def ult_block(charge, hurl) -> str:
    return (f'''    ult:{{ name:"Rebuttal", charge:{charge}, kind:"runes", dur:{ULT["dur"]},
          pad:{ULT["pad"]}, cd:{ULT["cd"]}, hex:{ULT["hex"]},
          hurl:{hurl},          // v70: the hurl (stage 3)
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
# THE RELIC, APPENDED AT THE END OF THE WEAPONS ARRAY, ITS ULTIMATE STUBBED at
# charge 1e9 (the clock can never reach it, `fireUlt` never runs) --
# Starwarden's stage-1 pattern. The anchor is the array's closing and the
# comment under it, which names no relic, so a row another build appends first
# still leaves it in place. Every other table keyed by relic id falls back, and
# SHAPES.warhammer already routes runic to `_whConjured`, which no shipped
# relic has drawn.
ROW_ANCHOR = '\n\n];\n/* The single source of truth for "which status does this relic teach".'

S1 = [

("lodestone joins the roster at the end of the array, its ultimate stubbed",
 ROW_ANCHOR,
 f'''

  /* LODESTONE / REBUTTAL (v70; built v102) -- THE RUNIC WARHAMMER. A new
     relic. Grudgebearer's hammer profile (the lab's donor and the whole
     type's) on the donor's blade until stage 5 settles its own; the school's
     channel, onHit hex 1. The ultimate is stubbed at stage 1 (charge 1e9);
     stages 2-3 give it its runed walls and their hex, then the hurl. */
  {{ id:"{RELIC}", name:"Lodestone", aff:"runic", shape:"warhammer",
    {PHYS},
    onHit:{{ hex:1 }},
{ult_block("1e9", 0)}
    blurb:"{BLURB}" }},''' + ROW_ANCHOR),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the runes have a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Rebuttal", charge:1e9, kind:"runes", dur:8,
''',
 f'''    ult:{{ name:"Rebuttal", charge:{ULT["charge"]}, kind:"runes", dur:{ULT["dur"]},   // v70 stage 2: the walls are runed
'''),

("the fighter carries the runed walls",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd} while LODESTONE's walls are runed (v70). null on every
       other relic and on this one outside its window: `tickRunes` returns
       after a two-iteration loop that does nothing. `runeTally` is the
       probe's count, cumulative over the fight; nothing in the simulation
       reads it. */
    this.ultRunes = null;
    this.runeTally = null;
'''),

("the cast runes the walls and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "runes"){
      /* REBUTTAL (v70). NOTHING RESOLVES HERE: the cast runes the four walls
         for `u.dur` seconds and `tickRunes` does everything the window does.
         `cd` starts at zero, so a foe already on a wall is touched on the
         first frame (the lab's). */
      f.ultRunes = { t: 0, dur: u.dur, cd: 0 };
      if (!f.runeTally)
        f.runeTally = { casts: 0, frames: 0, touches: 0, hexes: 0, hurls: 0,
                        foeStk: 0 };
      f.runeTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the runes tick with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickRunes(dt);                 // REBUTTAL (v70)
'''),

("tickRunes touches, hexes and hurls",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE RUNES =======
     v70 §1 / §5, brief §0-§1. While the window runs the four walls are
     runed, on the CURRENT inset (they walk in with the seals):
       A TOUCH   the foe's centre within inset + R + pad of any side, the foe
                 alive and not pinned, the cooldown clear. The engine clamps a
                 ball at n + R, so this is contact. Once per `cd`; the
                 cooldown runs through the whole window, touching or not.
       THE HEX   apply("hex", hex) on the foe, the real status, by side letter.
       THE HURL  the foe's velocity ASSIGNED to hurl x unit(caster - foe):
                 the wall answers with its own throw; `move` spends it next
                 step. Not an impulse.
     No damage, no resolveHit, no beat, no hit stop; nothing writes stun or
     pin. The caster's own touches do nothing, and the target is the OPPONENT
     only. The window closes on its clock or either death. On the window
     tickers' clock, so all of it freezes through a hit stop. */
  tickRunes(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultRunes;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }
      const u = f.w.ult, T = f.runeTally;
      T.frames++;
      T.foeStk += foe.stacks("hex");
      Z.cd -= dt;
      if (foe.pin > 0 || Z.cd > 0) continue;
      const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset, e = u.pad;
      if (!(foe.x <= n + R + e || foe.x >= A.w - n - R - e ||
            foe.y <= n + R + e || foe.y >= A.h - n - R - e)) continue;
      Z.cd = u.cd;
      T.touches++;
      if (u.hurl > 0){
        const dx = f.x - foe.x, dy = f.y - foe.y, d = Math.hypot(dx, dy) || 1;
        foe.vx = dx / d * u.hurl;
        foe.vy = dy / d * u.hurl;
        T.hurls++;
      }
      if (u.hex > 0){
        foe.apply("hex", u.hex, f === this.a ? "a" : "b");
        T.hexes += u.hex;
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the hurl",
 '''          hurl:0,          // v70: the hurl (stage 3)
''',
 f'''          hurl:{ULT["hurl"]},          // v70: the hurl (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief header: "The build owns the blade"; brief §2 stage 5:
# "Wide, both sides, two blocks, 21 / 22 / 23 on 151. Expect 21.5-22."; the
# v87 handoff: every design blade is a bracket, and every build settles its
# blade wide, both sides, two blocks, on 151). Both sides, two blocks, 1520
# fights a point (relic_rate, 38 foes; v102 §4): 19 -> 43.4, 20 -> 45.3,
# 20.5 -> 49.0, 21 -> 53.9, 21.5 -> 53.6, 22 -> 54.0, 23 -> 57.2,
# 23.5 -> 57.8 (the integers first; 20.5, 21.5 and 23.5 added after an
# earlier cut had picked 21 -- v102 §4 says the order).
# THE CRITERION THAT PICKS IT: the measured point whose POOLED RATE IS
# NEAREST 50% -- 20.5 at 49.0% (0.8 SE under) against 21's 53.9% (3.0 SE
# over); the two points that bracket 50% cross, locally, at about 20.6.
# BY BLADE DISTANCE TO A FITTED LINE IT IS 21: a line through all eight
# crosses at 20.78 (3.36 points a damage point), 0.22 from 21 and 0.28 from
# 20.5, and predicts 50.7% at 21 and 49.0% at 20.5 (v100 and v101 wrote "the
# measured point nearest the crossing"; there both criteria picked the same
# blade, here they part). The curve is not a line -- flat from 21 to 22,
# the hammer's kill steps; the eight points scatter 1.7 points around the fit
# against a 1.3 binomial SE -- so the build reads the measured rates and
# puts 20.5 against 21 to Rick (v102 §6). Above Bulwarden's 20.1, the
# design's row floor. The brief's forecast, 21.5-22, is where the LAB crosses
# on 151 (50.4% at 21.5); the built relic reads 53.6% there, the window
# clock's +4 (v102 §2, §4). No knob moves: the brief names none (§3 closes
# the hurl speed, the cadence and the bite).
BLADE = 20.5

S5 = [
("the blade: the measured point whose pooled rate is nearest 50%",
 '''  { id:"lodestone", name:"Lodestone", aff:"runic", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:23.5,''',
 f'''  {{ id:"lodestone", name:"Lodestone", aff:"runic", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:{BLADE},'''),
]

STAGE_OUT = {"1": "sc-lodestone", "2": "sc-lodestone-runes", "3": "sc-lodestone-rebuttal",
             "5": "sc-lodestone-b205"}


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


def assert_base(code: str, stage: str) -> None:
    """THE BASE BY CONTENT: every feature this builder reads or anchors on."""
    for need, why in (("tickTendril(dt){", "no tickTendril -- the window tickers' slot this "
                                           "builder follows is not there"),
                      ("this.tickTendril(dt);", "no tickTendril call"),
                      ("tickWinnow(dt){", "no tickWinnow"),
                      ("this.vineTally = null;", "no vineTally field line"),
                      ('if (u.kind === "tendril"){', "no tendril cast branch"),
                      ("if (f.charge >= f.w.ult.charge && !f.ultCorona", "no cast line"),
                      ("this.inset", "no inset"),
                      ('if (key === "runic")      return SHAPES._whConjured(',
                       "SHAPES.warhammer no longer routes runic to _whConjured")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if strip_comments(CLAMP) not in code:
        raise SystemExit("wrong base: `move` no longer clamps a ball at n + R -- the touch "
                         "would stop being a contact test")
    if HEX_DEF not in code:
        raise SystemExit("wrong base: STATUS.hex is not {5 stacks, 2.6s, a 0.2s stun every 1.15s}")
    if DONOR_PHYS not in relic_row(code, "grudgebearer"):
        raise SystemExit("Grudgebearer's hammer profile has moved -- the donor is not what "
                         "this builder copies")
    for h in HAMMERS:
        row = " ".join(relic_row(code, h).split())
        if not re.search(r'shape:"warhammer",\s*blades:\[0\], reach:76, width:26, '
                         r'artW:54, dmg:[\d.]+, spin:1\.6, mode:"spin", mass:5\.0, '
                         r'knockMul:2\.3', row):
            raise SystemExit(f"{h} is not the type's hammer profile any more")
    for v in RUNIC:
        if "onHit:{ hex:1 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, hex 1")
    if stage == "1":
        for name in NAMES:
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)
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
        raise SystemExit("stage 5 has no blade yet -- v102 §4 sets it")

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nLODESTONE / REBUTTAL -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    assert_base(code, A.stage)
    print("  base  by content: the window tickers' slot, the anchors, the five hammers' "
          "profile, the runic channel, the runic hammer head, hex, the wall clamp")

    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        blk0 = relic_ult(code)
        if A.stage == "2":
            if "ultRunes" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultRunes" not in code or "hurl:0," not in blk0:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["hurl"])
        else:
            if f'hurl:{ULT["hurl"]},' not in blk0 or "dmg:23.5," not in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["hurl"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Lodestone's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + (S5 if BLADE is not None else []):
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(dmg|spin|reach|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        # THE WALLS DO NO DAMAGE AND HOLD NOTHING (brief §1: "Nothing writes
        # f.stun or f.pin; nothing goes through resolveHit"; design §5: no
        # beat, no hit stop).
        if re.search(r"\.(stun|pin|pinMax|pinFree|pinV|hitStop)\s*=[^=]", ins) or \
           re.search(r"\b(resolveHit|hurt|beat)\s*\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stuns, pins, "
                             "stops, hurts or files a beat")
    if len(re.findall(r'kind:"runes"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one runes ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    last = re.findall(r'\{ id:"([a-z]+)", name:"', out_code)[-1]
    print(f"  ok    one runes ultimate, Lodestone's; no insert draws the RNG, writes the "
          f"shared weapon, stuns, pins, stops, hurts or files a beat; {n_ids} relics "
          f"in the roster (last in the array: {last})")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
