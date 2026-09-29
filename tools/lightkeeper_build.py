#!/usr/bin/env python
"""LIGHTKEEPER / BULWARK -- the vigil greatsword's ultimate, REDESIGNED. v107.

Built from `06-docs/v77/lightkeeper-bulwark-redesign-v77.md` (Cowork,
2026-09-26), which is the input and the only input. CLAUDE.md §3 rule 0:
nothing here is a design decision.

A REDESIGN, NOT A NEW RELIC. Lightkeeper ships in the base; its nova (Bulwark,
kind "nova": 12 damage in 260, knock 180) is replaced by the design's wall.

    stage 1   the ultimate stubbed            <tip> -> sc-lightkeeper-stub.html   (arm A)
    stage 2   the wall: arrows, the shove     -> sc-lightkeeper-wall.html         (arm B)
    stage 3   the bank, 0 -> 3 / 3            -> sc-lightkeeper-bulwark.html      (arm C)
    stage 5   the blade, 10.54 -> 9.5         -> sc-lightkeeper-bulwark-b9.5.html
    stage 6   picture, voice (brief stage 4)  -> sc-lightkeeper-bulwark-b9.5-fx.html
              (on the final; the nova's field spec leaves BOTH copies of fx.js by the
              orchestrator's fx_remove.py, not here: reading 14)

The design's §5 brief stages it as "Stage 1 -- nova out, f.ultWall in, the
wall test, arrows, the shove", "Stage 2 -- the bank", "Stage 3 -- the blade",
"Stage 4 -- picture, voice, carry". This build puts a stub under them (its
stage 1, which must be arm A fight for fight) and numbers the blade 5, as the
batch does.

§1: "For a duration a wall of light stands in front of the sword, as wide as
the blade is long. Arrows die on it. An enemy that runs into it bounces off
and cannot pass. Every arrow the wall stops and every time it turns the enemy
back, the shield grows."

Declared (design §5):
  THE WALL    a segment centred `ahead` (50) along theta, half-length `half`
              (110), perpendicular to the facing; it moves with the ball and
              turns with the aim every frame.
  ARROWS      within r + `shotPad` (6) of it are removed; a net's arrow is
              `stuck`, not spliced, so `tickNet` keeps its anchors.
  A FOE       within R + `ballPad` (8) of it, not pinned, once per `cd` (0.4s),
              is knocked `shove` (500) along the wall's normal; no damage, no
              beat, no hit stop.
  THE BANK    + `bankShot` / `bankBall` (3 / 3) ward per block -- the vigil
              branch's three writes. Stage 3.

THE CHARGE. The design names none: its lab priced every arm at the harness's
default, 16 on the LAB's clock (`P` in `runs/wall_base.json` and
`wall_bank3.json`), which counts hit-stop freezes. Rick, 2026-09-27, for the
whole batch: "use the game's equivalent". Measured for this fighter on the
lab's arm C by counting frozen lab steps (v107 §0). The shipped 15 was the
nova's and goes with it.

THE WINDOW. The design's prose says only "for a duration"; its lab priced
every arm at P.dur 8 (seconds), and that is the build's `dur`, kept on the
window tickers' clock (below) like every window in the batch. The design
names no other length.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE FACING IS `theta`, the greatsword's swinging blade angle (aim + sin
     (phase) x arc), which is what the lab read (`me.theta`): the wall swings
     with the blade. The design's picture says the same ("swinging with the
     aim").
  2. EVERY LIVE SHOT IN THE HALL is an arrow to the wall, whoever loosed it (the
     lab's loop; Lightkeeper fires none), tested at `(s.r || 6) + shotPad`. A
     net arrow is made stuck with `tickShots`' own endpoint write (vx = vy = 0,
     life 1e9) and every other shot is spliced (design §5; the lab spliced
     all). A stuck arrow is already inert and is skipped.
     THE WRITE IS COPIED, THE RELEASE IS NOT. In tickShots the endpoint write
     is followed, in the same call, by `this.releaseVolleys()`, which
     detonates a Crossweave volley whose every arrow is stuck (volleyDone:
     Gloamwire's hurt, beat and hit stop). When the wall sticks the LAST live
     arrow of a volley, the release waits for the next tickShots -- one frame
     later, or after the whole freeze if a blow in tickHits starts a hit stop
     that frame -- and tickNet runs once over the fully stuck volley between
     (its shove is zero: the stuck arrows are still; strandSpent and the net
     counters are touched). Calling releaseVolleys() from the wall would put
     Gloamwire's hurt, beat and hit stop inside the wall's frame, which the
     design's "no damage, no beat, no hit stop" and the window clock both
     rule out, so the delay is the reading. The probe counts such volleys
     (second review round: 80 in its 444 fights on the final link, all in
     the 12 against Gloamwire, the only relic whose arrows are nets).
  3. THE SHOVE IS THE LAB'S: along the wall's normal, to the side of the wall
     the foe stands on (the sign of (foe - centre) . facing; 0 counts as
     ahead), so it cannot pass -- "away from the caster's side" as the lab
     computed it. H.knock's arithmetic: the direction normalised, `shove`
     added to the velocity. The prose read literally ("away from the
     caster's side": always outward) is a different fight -- a foe behind
     the wall is shoved away from the caster instead of back toward her --
     and is put to Rick with its size (v107 §6).
  4. A PINNED FOE IS NOT BLOCKED AT ALL (the lab's test: no shove, no bank, and
     the cooldown is not spent). A dead foe closes the window (7).
  5. THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, touching or not, from 0 at the
     cast (the lab's `cd -= dt` every open frame).
  6. THE BANK IS THE VIGIL BRANCH'S THREE WRITES (shield to the cap, shieldMax,
     apply("ward", 1) with no source -- the branch's own), once per block, ball
     or arrow, even at the cap (it restarts the ward's clock). No float and no
     tag: those are the picture's (stage 6).
  7. THE WINDOW CLOSES ON THE CLOCK OR EITHER DEATH (the lab's). No wither and
     no wait: the design names none, and a cast cannot come under a standing
     wall -- the charge and the window run on one clock and 8 < the charge.
  8. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).
     The probe holds it from the third review round: every shade is diffed
     field by field around every wall frame.
  9. NOTHING ELSE: no damage, no beat, no hit stop, no rng draw; the sword
     swings as ever. No insert writes a shared module table (STATUS, CONFIG,
     AFFINITIES, WEAPONS, SHAPES) or the shared weapon: the builder refuses
     one that does, by name or through an alias (third review round).

STAGE 6 -- THE PICTURE AND THE VOICE (design §5, the brief's stage 4), on the
final (stage 5's link), picked on measurements by `lightkeeper_voice_lab.py`
and the picture lab under Rick's "you pick i overrule" (v107 §5). The
readings, where the labs had to choose:
 10. THE RAISE IS THE CAST'S OWN VOICE. fireUlt's shared prelude already plays
     SFX.play("ult", { w: f.w.id }) on every cast; Lightkeeper had no arm and
     fell through to rune-crack. The raise is an Sfx arm keyed "lightkeeper",
     added before that shared fallback (which eleven other relics on the
     final still use), so the cast needs no row in the simulation.
 11. THE FOLD SOUNDS ONLY ON A CLOSE BY THE CLOCK WITH BOTH ALIVE (Tendril's,
     Canopy's and Zenith's rule): a caster's death ends the fight and a close
     after the foe's death is its kill flight's, both the death voice's; a
     wall still up when the fight ends is never closed by tickLightwall (it
     does not run once `over` is set) and folds in the picture only.
 12. THE TINKS OF ONE FRAME ARE FLAMMED: the k-th arrow the wall stops in one
     call is struck 26 ms x min(5, k) late (the nova's flam), so four arrows
     are four tinks. `k` is a `var` local to the ticker's call.
 13. THE DESIGN'S "motes along the bar (both fx.js copies)" ARE DRAWN, not a
     SPECS field: a field fires once, at the one ultFx slot's cast edge and
     spot, and the slot is Lightkeeper's for a median 0.64s of the 8s window
     (the opponent's cast takes it at once on 24 of 145); after that the
     bar's centre stands a median 181 units from the cast point, and the bar
     turns a median 7.6 rad a window. Ten motes shed off both faces of the
     bar, placed by shellHash (no rng). Rick's to overrule (Zenith's,
     Canopy's, Temper's and Quarrelstorm's precedent).
 14. THE NOVA'S FIELD SPEC (`SPECS.lightkeeper`, a 1500-particle burst) is the
     brief's "nova's field spec out", and fx.js is shared by every build in
     the batch: it leaves BOTH copies by the orchestrator's `fx_remove.py
     --relic lightkeeper`, not here. This builder asserts its inlined copy
     untouched; until the removal the stage-6 link still fires the burst at
     each cast.
 15. THE BAR IS READ OFF `ultWall && alive && !over` and folds on either, so a
     fight that ends with the wall up folds it in the verdict.
 16. A BLOCK AND AN ARROW ARE FOUND BY WATCHING `wallTally` RISE: the ticker
     makes no call for the picture. A stopped arrow is spliced before the
     picture sees it, so its scorch is placed from where each live shot will
     be after its next move (tickShots' own arithmetic, kept as plain
     numbers), nearest the wall first; an arrow loosed and stopped inside one
     step scorches where the foe's bow tip meets the bar.
 17. A CONTACT WHILE THE BAR IS STILL RISING SNAPS IT UP (Canopy's sprout
     rule): the wall is live from the cast's first frame.
 18. THE BANK SHOWS ON THE CASTER in the vigil branch's own float ("+N": its
     colour, size and seat), a block's and an arrow's alike, and nothing at
     the cap; once a window, the WARD tag (the first in a match carrying its
     one line: the vigil branch's own teaching).
 19. THE NOVA'S ART IS RETIRED WITH THE NOVA: its plate ring (drawUltUnder)
     and its eighteen plates (drawUltOver) on the ultFx slot, the life map's
     1.5 (the slot falls to the map's own 1.5: no change in what it does), and
     the charge rune's ring and shield (ULTSIG), redrawn as five ward plates
     with a bar standing up out of their front as the charge fills.
 The picks are measurements, not readings: the raise PLATE, the gong LOW-E,
 the tink PIN, the fold FADE; the picture's sizes are the design's (220 x 6,
 a 14-unit halo, 50 ahead, out of the R + 17 ward ring, a 0.25s rise and
 fold, a two-frame flash, a 0.3s scorch).

THE CLOCK. The window and the cooldown run on the window tickers' clock, which
stops through a hit stop (Corollary's, Daybreak's, Zenith's, Canopy's,
Onslaught's and Tendril's convention). The lab ran both through freezes; v99
§4, v100 §2 and v101 §2 measured what that is worth on the three builds before
this one.

THE ORDER. `tickLightwall` runs with the window tickers, after `tickTendril`:
after `tickShots` has moved and resolved this frame's arrows (the lab tested
after the whole step) and before `tickHits`.

WHAT IS RETIRED. The nova's three numbers (radius 260, dmg 12, knock 180) leave
Lightkeeper's row and its kind becomes "lightwall". The NOVA ITSELF STAYS:
Censer's Consecration is kind:"nova" (and, on this base, Widowmaker's
Exsanguinate, which its own v106 redesign takes off the nova and may carry
first) and the generic tail of `fireUlt` is theirs; the lightwall branch
returns before it. The builder reads who is still a nova and never refuses on
it: this build touches none of the nova's code.
The nova's presentation keyed on the id -- ULTSIG `lightkeeper`, the two
`u.w === "lightkeeper"` draw branches, the `life` map's 1.5, the fx.js SPECS
`lightkeeper` burst and the id's `ult` voice -- is picture and sound, and
design §5 retires it at its stage 4 ("nova's field spec out, the wall's in"):
this build's stage 6 (readings 10-19). Nothing in the simulation reads any of it.

THE BASE is asserted BY CONTENT (the features this builder needs), never by
which relic is last, so it re-applies on a later tip that carries other new
relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "lightkeeper"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). Design §5.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v107 §0)
    "dur": 8,         # the lab's window ("for a duration"; P.dur 8)
    "ahead": 50,      # "a segment centred 50 ahead along theta"
    "half": 110,      # "half-length 110" -- 220 wide
    "shotPad": 6,     # "arrows within r + 6 of it are removed"
    "ballPad": 8,     # "a foe within R + 8 of it"
    "cd": 0.4,        # "once per 0.4s"
    "shove": 500,     # "knocked 500 along the wall's normal"
    "bankBall": 3,    # "+3 ward per block (ball or arrow)" -- stage 3
    "bankShot": 3,
}
TIP = "A wall of light: arrows die on it, foes bounce off it, blocks bank ward"
# THE SHIPPED ROW, which this builder asserts before it touches it.
PHYS = ('blades:[0], reach:116, width:14, artW:40, dmg:10.54, spin:3.4, '
        'mode:"swing", arc:1.5, mass:3.0')
OLD_ULT = ('''    ult:{ name:"Bulwark", charge:15, kind:"nova", radius:260, dmg:12, knock:180,
          tip:"Nova: deals 12 damage — extra knockback" },
''')


def ult_block(charge, bank_ball, bank_shot) -> str:
    return (f'''    ult:{{ name:"Bulwark", charge:{charge}, kind:"lightwall", dur:{ULT["dur"]},
          ahead:{ULT["ahead"]}, half:{ULT["half"]}, shotPad:{ULT["shotPad"]}, ballPad:{ULT["ballPad"]}, cd:{ULT["cd"]}, shove:{ULT["shove"]},
          bankBall:{bank_ball}, bankShot:{bank_shot},          // v77: the bank (stage 3)
          tip:"{TIP}" }},
''')


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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH, so the output "
                         "cannot be syntax checked")
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
# THE NOVA OUT, THE WALL'S BLOCK IN, STUBBED at charge 1e9 (the clock can
# never reach it, `fireUlt` never runs for Lightkeeper) -- Starwarden's stage-1
# pattern, on a relic that already ships. Nothing else in the row moves, so
# this link must be the lab's arm A (the relic with no ultimate) to the fight.
S1 = [

("Bulwark's nova out, the wall's block in, stubbed",
 OLD_ULT,
 '''    /* BULWARK, REDESIGNED (v77; built v107): the nova is out and the wall is
       in. `kind:"lightwall"` (not "wall": that is an SFX kind). Stage 1
       stubs it at charge 1e9; stages 2-3 give it its wall, then its bank. */
''' + ult_block("1e9", 0, 0)),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the wall has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Bulwark", charge:1e9, kind:"lightwall", dur:8,
''',
 f'''    ult:{{ name:"Bulwark", charge:{ULT["charge"]}, kind:"lightwall", dur:{ULT["dur"]},   // v77 stage 2: the wall stands
'''),

("the fighter carries the wall's window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd} while BULWARK's wall of light stands (v77). null on every
       other relic and on this one outside its window: `tickLightwall` returns
       after a two-iteration loop that does nothing. `wallTally` is the probe's
       count, cumulative over the fight; nothing in the simulation reads it. */
    this.ultWall = null;
    this.wallTally = null;
'''),

("the cast raises the wall and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "lightwall"){
      /* BULWARK (v77). NOTHING RESOLVES HERE, and the nova's tail below is
         never reached: the cast stands the wall up for `u.dur` seconds and
         `tickLightwall` does everything the window does. `cd` starts at zero,
         so a foe already against the wall is turned back on the first frame. */
      f.ultWall = { t: 0, dur: u.dur, cd: 0 };
      if (!f.wallTally)
        f.wallTally = { casts: 0, frames: 0, shieldSum: 0, blocks: 0, arrows: 0,
                        banks: 0, banked: 0 };
      f.wallTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the wall ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickLightwall(dt);             // BULWARK (v77)
'''),

("tickLightwall stops arrows, turns the foe back and banks",
 '''  tickWinnow(dt){
''',
 '''  /* ============================================== THE WALL OF LIGHT ====
     v77 §1 / §5. While the window runs a wall stands in front of the sword:
       THE WALL    a segment centred `ahead` along `theta` (the greatsword's
                   swinging blade angle, as the lab read it), half-length
                   `half`, perpendicular to the facing. It is rebuilt every
                   frame from the ball and the blade, so it moves and turns
                   with them and there is nothing stored to keep in sync.
       ARROWS      every live shot within r + `shotPad` of it dies: a net's
                   arrow is made `stuck` with tickShots' own endpoint write
                   (so `tickNet` keeps its anchors), every other shot is
                   spliced. A stuck arrow is already inert and is skipped.
       A FOE       within R + `ballPad` of it, not pinned, the cooldown clear:
                   `shove` along the wall's normal, to the side of the wall it
                   stands on, so it cannot pass. No damage, no beat, no hit
                   stop. The cooldown runs through the whole window.
       THE BANK    + `bankShot` an arrow, + `bankBall` a block: the vigil
                   branch's three writes (shield to the cap, shieldMax, the
                   ward's clock).
     After `tickShots`, so an arrow is tested where it has moved this frame;
     before `tickHits`. The target is the OPPONENT only. On the window
     tickers' clock, so all of it freezes through a hit stop. The window
     closes on the clock or either death. */
  tickLightwall(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultWall;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }
      const u = f.w.ult, T = f.wallTally, R = CONFIG.physics.ballR;
      T.frames++;
      T.shieldSum += f.shield;
      const ux = Math.cos(f.theta), uy = Math.sin(f.theta);
      const cx = f.x + ux * u.ahead, cy = f.y + uy * u.ahead;
      const px = -uy, py = ux;
      const ax = cx - px * u.half, ay = cy - py * u.half;
      const bx = cx + px * u.half, by = cy + py * u.half;
      const W = STATUS.ward;
      for (let i = this.shots.length - 1; i >= 0; i--){
        const s = this.shots[i];
        if (s.stuck) continue;
        if (!(segDist(ax, ay, bx, by, s.x, s.y).d < (s.r || 6) + u.shotPad)) continue;
        if (s.net){ s.stuck = true; s.vx = 0; s.vy = 0; s.life = 1e9; }
        else this.shots.splice(i, 1);
        T.arrows++;
        if (u.bankShot > 0){
          const b0 = f.shield;
          f.shield = Math.min(W.cap, f.shield + u.bankShot);
          f.shieldMax = Math.max(f.shieldMax, f.shield);
          f.apply("ward", 1);                       // (re)starts the clock
          T.banks++;
          T.banked += f.shield - b0;
        }
      }
      Z.cd -= dt;
      if (Z.cd > 0 || foe.pin > 0) continue;
      if (!(segDist(ax, ay, bx, by, foe.x, foe.y).d < R + u.ballPad)) continue;
      Z.cd = u.cd;
      T.blocks++;
      const side = ((foe.x - cx) * ux + (foe.y - cy) * uy) >= 0 ? 1 : -1;
      const kx = ux * side, ky = uy * side, kl = Math.hypot(kx, ky) || 1;
      foe.vx += kx / kl * u.shove;
      foe.vy += ky / kl * u.shove;
      if (u.bankBall > 0){
        const b0 = f.shield;
        f.shield = Math.min(W.cap, f.shield + u.bankBall);
        f.shieldMax = Math.max(f.shieldMax, f.shield);
        f.apply("ward", 1);                         // (re)starts the clock
        T.banks++;
        T.banked += f.shield - b0;
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the bank",
 '''          bankBall:0, bankShot:0,          // v77: the bank (stage 3)
''',
 f'''          bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},          // v77: the bank (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (design §5 "Stage 3 -- the blade, wide on 151 at 9 / 9.5 / 10 to
# the shipped rate"; §4: "the blade comes from 10.54 to about 9.5 ... the
# build settles it wide to the shipped rate"; the handoff's row: blade ~9.5).
# The design's own default is THE SHIPPED RATE, and rule 0 takes it; open
# decision 2 ("shipped 48.5 or 50") leaves 50% to Rick, one number away.
# The shipped rate is read on 151, never the published 48.5 (handoff v87:
# every gate reads against the 151 run): the shipped nova on this base,
# relic_rate both sides, two blocks, 1480 fights, is 43.6%.
# The brief's three points, both sides, two blocks, 1480 fights a point
# (relic_rate on stage 3, every other relic a foe): 9 -> 38.4, 9.5 -> 44.3,
# 10 -> 47.6. Blade 9.5 is the measured point nearest the shipped 43.6 (+0.6
# on the unrounded rates, 44.26 - 43.65; the line puts 43.6 at 9.47). The design gives the build no knob to move
# first. Rick's other choice, 50%: blade 10 (47.6%, the line crosses 50% at
# 10.03), measured and gated as the first draft of this build (v107 §4, §6).
BLADE = 9.5

S5 = [
("the blade: the shipped rate",
 '''  { id:"lightkeeper", name:"Lightkeeper", aff:"vigil", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, dmg:10.54,''',
 f'''  {{ id:"lightkeeper", name:"Lightkeeper", aff:"vigil", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, dmg:{BLADE},'''),
]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v77 §5, the brief's "Stage 4 -- picture, voice,
# carry"), picked on measurements under Rick's "you pick i overrule" by
# `lightkeeper_voice_lab.py` and the picture lab (v107 §5). Presentation only:
# engine_ab over all 38 relics, Lightkeeper included, is the proof. The rows
# are byte-exact to the labs' own files (voice 4, picture 9; no two share an
# anchor, so none is merged; nine re-emit their anchor, four replace it). The
# picture rows alone reproduce the picture lab's stamp on the final
# (728d64f8397290a1), the voice rows alone the voice lab's (a8629a7fe94d50b9),
# and both, in either order, the same page (e3f16bf01f0e2995). Voice first,
# then picture.
#   THE VOICE: the raise is the cast's own `ult`/lightkeeper call in fireUlt's
#   shared prelude, which fell through to rune-crack (PLATE: a plate's ring
#   gliding A3 -> A4 in 0.36s, swelling); a gong a ball block (LOW-E, a plate
#   on E2), in the block branch after its tally; a tink an arrow (PIN, a small
#   plate on C8), after its tally, flammed 26 ms x min(5, k) by its index k in
#   the frame; the fold (FADE, the slide falling A4 -> A3) before the close
#   line, on a close BY THE CLOCK with both alive only (a death's close is the
#   death voice's; a wall standing when the fight ends folds in the picture
#   only). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickBulwark` in tickPresentation reads `ultWall && alive &&
#   !over`, `wallTally` rising and the shots in the air, and writes only its
#   own `bulwark*` fields, a float, a tag and `taught`: the bar (6 wide, vigil
#   pink, a pale heart, a soft 14-unit halo, ten motes off its faces) rises
#   out of the ward ring over 0.25s and folds back into it; a block flashes it
#   white for two frames; an arrow leaves a 0.3s scorch where it died on the
#   bar; a bank floats "+N" on the caster and, once a window, the WARD tag.
#   `drawBulwark` draws it over both fighters, every ball's disc cut out. The
#   nova's art is retired: the two plate branches on the ultFx slot, the life
#   map's 1.5, the charge rune's ring and shield. No beat, no stop, no fx.js
#   edit: the design's motes are drawn (reading 13), and the nova's field spec
#   (`SPECS.lightkeeper`) leaves BOTH copies by the orchestrator's
#   `fx_remove.py`, not here (fx.js is shared; reading 14).
S6 = [

("Sfx: Lightkeeper's raise, gong, tink and fold arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "lightkeeper"){                // the wall rises
          /* LIGHTKEEPER'S CAST, THE RAISE -- v77 s5: "cast -- a shield-raise
             (a rising metallic slide, 0.4s)". PLATE, of 7, picked on the
             numbers by `lightkeeper_voice_lab.py` under Rick's "you pick i
             overrule" (v107). Lightkeeper had no arm and fell through to
             rune-crack, which eleven other relics on its stage-5 link still
             used, so this ADDS arms before that fallback and leaves it alone.

             A plate's ring -- a sine with its 1.73, 2.33 and 3.91 modes (at
             0.55, 0.4 and 0.2), gliding one octave A3 -> A4 in 0.36 s and
             swelling 0.35 -> 1 as it climbs; the glide ends on A4 and rings
             there. The ring is re-struck on whole cycles of one chirp (a held
             note does not exist in this toolkit), every 2 cycles (9 ms apart
             at A3, 4.5 at A4), each strike dying over 0.06 s, with
             `.frequency.value` set on every strike. It climbs +1083 cents and
             never turns back (its largest step 7% of the climb: a slide, not
             two notes); it swells +8.0 dB to its top (not a strike) and
             flutters 2.9 dB (held, not a buzz of strikes); its 1.73x mode
             stands 249 cents off every harmonic (metal). Audible 400 ms;
             loudest 50 ms -2.8 dB re Lightkeeper's blow; +6.1 dB over the
             score where a phone hears it. Register at most 0.68 against
             rune-crack, the vigil and greatsword casts, Zenith's rising cast,
             the blow and the death voice. */
          const g = 0.02567, L = 0.36, D = 0.06;
          const r = 2, Lg = Math.log(r);
          for (const [m, km, ty] of [[1, 1, "sine"], [1.73, 0.55, "sine"], [2.33, 0.4, "sine"], [3.91, 0.2, "sine"]]){
            const fs = 220 * m, N = Math.max(1, Math.round(220 * m * 0.01));
            for (let k = 0; ; k += N){
              const u = L / Lg * Math.log(1 + k * Lg / (fs * L));
              if (!(u < L)) break;
              const f = fs * Math.pow(r, u / L), to = fs * Math.pow(r, Math.min(u + D, L) / L);
              this._tone(t + u, { freq: f, to: to, gain: g * km * (0.35 + 0.65 * u / L), dur: D, type: ty }).frequency.value = f;
            }
          }
        } else if (w === "lightkeeper-gong"){           // a foe turned back
          /* A BALL BLOCK -- "a deep gong (share <120 Hz >= 0.4, <=0.3s)" (v77
             s5). LOW-E, of 5 (`lightkeeper_voice_lab.py`). `tickLightwall`
             plays it once per block, on the frame the foe is turned back.

             One strike: a 82.41 Hz sine under the 1.73, 2.33, 3.91 and 4.11
             modes of a plate, each dying faster than the one below, a soft
             mallet (a 20 ms lowpass thump at 450 Hz). Its note 82.4 Hz holds
             (+1 cents at 80-160 ms); its 1.73x mode stands 253 cents off every
             harmonic; 0.50 of its power under 120 Hz at the worst noise draw;
             rings 235 ms and is gone by 240; loudest 50 ms -2.8 dB re the
             blow. On a phone (nothing under 200 Hz) its modes stand +13.0 dB
             over the score. Register at most 0.72 against the blow, the death
             voice, the clank, aegis, the nova, rune-crack and the raise. */
          const g = 0.09746, f = 82.41, D = 0.473;
          this._tone(t, { freq: f, gain: g * 0.5758, dur: D, type:"sine" }).frequency.value = f;
          for (const [m, a, d] of [[1.73, 0.6, 0.6], [2.33, 0.45, 0.5], [3.91, 0.35, 0.35], [4.11, 0.3, 0.3]])
            this._tone(t, { freq: f * m, gain: g * a, dur: D * d, type:"sine" }).frequency.value = f * m;
          this._burst(t, { freq: 450, q: 0.7, gain: g * 0.6, dur: 0.02, type:"lowpass" });
        } else if (w === "lightkeeper-tink"){           // an arrow dies on it
          /* AN ARROW DIES ON THE WALL -- "an arrow -- a short tink" (v77 s5).
             PIN, of 7 (`lightkeeper_voice_lab.py`). `tickLightwall` plays it
             once per arrow the wall stops, with k = the arrow's index among
             that frame's kills: the k-th is flammed 26 ms x min(5, k) (the
             nova's flam), so a frame's arrows are heard one by one.

             One strike of a 4186 Hz sine with its 1.73 mode and its 2.33 mode.
             Rise under 1 ms; audible 40 ms, gone by 45; its note stands 43 dB
             over the noise round it (a note, not a tick) and its 1.73x mode
             251 cents off every harmonic; loudest 50 ms -8.3 dB re the blow
             and +11.2 dB re the wall tick. Four on one frame: 4 onsets, the
             stack's peak 1.00x one tink's. Register at most 0.61 against the
             wall tick, hex-snap, the spark, Zenith's tick, the bowstring, the
             blow, the clank, the raise and the gong. */
          const g = 0.1029, f = 4186, D = 0.0665;
          const tt = t + Math.min(5, Math.max(0, p.k | 0)) * 0.026;   // the flam: k-th arrow of a frame
          this._tone(tt, { freq: f, gain: g, dur: D, type:"sine" }).frequency.value = f;
          for (const [m, a, d] of [[1.73, 0.5, 0.7], [2.33, 0.35, 0.5]])
            this._tone(tt, { freq: f * m, gain: g * a, dur: D * d, type:"sine" }).frequency.value = f * m;
        } else if (w === "lightkeeper-fold"){           // and it folds
          /* THE WALL FOLDS -- "close -- the slide reversed" (v77 s5). FADE, of
             3 (`lightkeeper_voice_lab.py`): the ring gliding down A4 -> A3
             from its top as its swell unwinds 1 -> 0.35.

             It falls -1082 cents (the raise climbs +1083); its envelope
             correlates 0.97 with the raise's samples literally reversed;
             audible 395 ms; loudest 50 ms -0.0 dB re the raise's (a reversal
             keeps its level). `tickLightwall` plays it when the wall runs out
             by its clock with both alive. */
          const g = 0.02597, L = 0.36, D = 0.06;
          const r = 0.5, Lg = Math.log(r);
          for (const [m, km, ty] of [[1, 1, "sine"], [1.73, 0.55, "sine"], [2.33, 0.4, "sine"], [3.91, 0.2, "sine"]]){
            const fs = 440 * m, N = Math.max(1, Math.round(220 * m * 0.01));
            for (let k = 0; ; k += N){
              const u = L / Lg * Math.log(1 + k * Lg / (fs * L));
              if (!(u < L)) break;
              const f = fs * Math.pow(r, u / L), to = fs * Math.pow(r, Math.min(u + D, L) / L);
              this._tone(t + u, { freq: f, to: to, gain: g * km * (1 - 0.65 * u / L), dur: D, type: ty }).frequency.value = f;
            }
          }
        } else {                                        // rune-crack'''),

('tickLightwall: the tink, once per arrow the wall stops, flammed by its index in the frame',
 '''        T.arrows++;''',
 '''        T.arrows++;
        /* BULWARK'S TINK (v77 s5: "an arrow -- a short tink"): one per arrow
           the wall stops, on its frame, before its bank. `tinkK` is the
           arrow's index among this frame's kills -- a `var`, hoisted to the
           ticker's call, so it starts undefined -> 0 on every frame -- and
           the arm flams by it (the nova's 26 ms), so four arrows on one frame
           are four tinks, not one loud one. Presentation only: SFX.play
           draws nothing, is a no-op headless, and nothing here is read back
           (lightkeeper_voice_lab: fights identical). */
        var tinkK = tinkK | 0;
        SFX.play("ult", { w: "lightkeeper-tink", k: tinkK++ });'''),

("tickLightwall: the gong, once per ball block, on the block's frame",
 '''      T.blocks++;''',
 '''      T.blocks++;
      /* BULWARK'S GONG (v77 s5: "a ball block -- a deep gong"): one per
         block, on the frame the foe is turned back, before its shove and its
         bank. The window's own cooldown (0.4s, on the window tickers' clock)
         makes the cadence -- no hit stop, no beat. Presentation only;
         nothing here is read back. */
      SFX.play("ult", { w: "lightkeeper-gong" });'''),

('tickLightwall: the fold, on a clock close with both alive, before the close line',
 '''      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }''',
 '''      /* BULWARK'S FOLD (v77 s5: "close -- the slide reversed"): on the
         frame the wall runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill flight, so both are left to the death voice
         (Tendril's, Canopy's and Zenith's rule); a wall still up when the
         fight ends folds in the picture only. Presentation only; the next
         line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }'''),

('bulwark picture: fighter fields',
 '''    this.ultWall = null;
    this.wallTally = null;
''',
 '''    this.ultWall = null;
    this.wallTally = null;
    /* BULWARK'S PICTURE (v77 section 5), and none of it is the sim's: the
       bar folds back into the ward ring after `ultWall` is gone, and a
       block's flash and an arrow's scorch outlive the step that made them,
       so the picture keeps its own state. On the FIGHTER and never on
       `m.ultFx` (one slot, and the opponent's cast takes it: open item 25).
       Driven in `tickPresentation` (`tickBulwark`); nothing in the
       simulation reads any of it.
         bulwarkFade   -- 1 while the wall stands; eased to 0 over the fold
         bulwarkAge    -- the presentation clock since the cast (the rise,
                          the motes)
         bulwarkOut    -- the presentation clock since the close (the fold)
         bulwarkFlash  -- a block's white flash: presentation clock left
         bulwarkSeen   -- `wallTally`'s blocks, arrows and banked, as last seen
         bulwarkShots  -- where each live shot will be after its next move,
                          as plain numbers [x, y, r, ...]: an arrow the wall
                          stops is spliced before the picture can look at it
         bulwarkScorch -- an arrow's scorch (records: its place ALONG the
                          bar, so it rides the bar as it swings)
         bulwarkTagged -- this window has had its WARD tag */
    this.bulwarkFade = 0;
    this.bulwarkAge = 0;
    this.bulwarkOut = 0;
    this.bulwarkFlash = 0;
    this.bulwarkSeen = [0, 0, 0];
    this.bulwarkShots = [];
    this.bulwarkScorch = [];
    this.bulwarkTagged = false;
'''),

('bulwark picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickBulwark(dt);               // BULWARK'S PICTURE (v77 section 5)
'''),

('bulwark picture: tickBulwark',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------------- BULWARK'S PICTURE ---
     v77 section 5, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.5 is the
     bar's 0.25s rise out of the ward ring, 0.5 its 0.25s fold back into
     it, 0.066 a block's two-frame white flash, 0.6 an arrow's 0.3s
     scorch. A BLOCK AND AN ARROW ARE FOUND BY WATCHING `wallTally` RISE, so
     `tickLightwall` makes no call for the picture. An arrow the wall stops
     is spliced out of `m.shots` before this runs, so the picture keeps, as
     plain numbers, where each live shot will be after `tickShots` next moves
     it (its own arithmetic: `vy += grav * dt`, then the step), and the
     arrows the tally says died are the ones of those nearest the wall.
     THE BAR IS READ OFF `ultWall && alive && !over`: `tickLightwall` never
     runs again once `over` is set, and a fight that ends with the wall up
     never closes it, so the fold keys on either. Writes presentation
     fields, `floats`, `tags` and `taught` only, and draws no rng. */
  tickBulwark(dt){
    for (const f of [this.a, this.b]){
      const T = f.wallTally;
      if (!T) continue;                                          // <- zero burden
      const u = f.w.ult, foe = f === this.a ? this.b : this.a;
      for (let i = f.bulwarkScorch.length - 1; i >= 0; i--){
        const q = f.bulwarkScorch[i];
        q.t += dt;
        if (q.t >= q.life) f.bulwarkScorch.splice(i, 1);
      }
      if (f.bulwarkFlash > 0) f.bulwarkFlash = Math.max(0, f.bulwarkFlash - dt);
      const Z = (this.over || !f.alive) ? null : f.ultWall;
      if (Z){
        if (!(f.bulwarkFade > 0) || f.bulwarkOut > 0){           // a cast
          f.bulwarkAge = 0; f.bulwarkOut = 0; f.bulwarkTagged = false;
        }
        f.bulwarkFade = 1;
        f.bulwarkAge += dt;
      } else if (f.bulwarkFade > 0){
        f.bulwarkAge += dt;
        f.bulwarkOut += dt;
        f.bulwarkFade = Math.max(0, 1 - f.bulwarkOut / 0.5);
        if (!(f.bulwarkFade > 0)) f.bulwarkScorch.length = 0;
      }
      const S = f.bulwarkSeen;
      const nB = T.blocks - S[0], nA = T.arrows - S[1];
      const got = Math.round(T.banked - S[2]);
      S[0] = T.blocks; S[1] = T.arrows; S[2] = T.banked;
      if (nB > 0 || nA > 0){
        /* A CONTACT WHILE THE BAR IS STILL RISING SNAPS IT UP: the wall is
           live from the cast's first frame, so nothing is ever stopped by
           light the viewer cannot see yet (Canopy's sprout rule). */
        if (Z && f.bulwarkAge < 0.5) f.bulwarkAge = 0.5;
        if (nB > 0) f.bulwarkFlash = 0.066;
        if (nA > 0){
          const ux = Math.cos(f.theta), uy = Math.sin(f.theta), px = -uy, py = ux;
          const cx = f.x + ux * u.ahead, cy = f.y + uy * u.ahead;
          const ax = cx - px * u.half, ay = cy - py * u.half;
          const bx = cx + px * u.half, by = cy + py * u.half;
          const P = f.bulwarkShots, near = [];
          for (let i = 0; i < P.length; i += 3){
            const d = segDist(ax, ay, bx, by, P[i], P[i + 1]).d;
            if (d < P[i + 2] + u.shotPad + 2) near.push([d, P[i], P[i + 1]]);
          }
          near.sort((p, q) => p[0] - q[0]);
          /* an arrow loosed and stopped inside one step was never seen: it
             left the foe's bow at `spawnShot`'s own point, R + reach along
             the foe's facing, so it scorches where that meets the bar */
          const rch = CONFIG.physics.ballR + foe.w.reach * this.actMods.reach * foe.reachMul;
          const tx = foe.x + Math.cos(foe.theta) * rch, ty = foe.y + Math.sin(foe.theta) * rch;
          for (let j = 0; j < nA; j++){
            const q = near[j], x = q ? q[1] : tx, y = q ? q[2] : ty;
            f.bulwarkScorch.push({ s: clamp((x - cx) * px + (y - cy) * py, -u.half, u.half),
                                   side: (x - cx) * ux + (y - cy) * uy >= 0 ? 1 : -1,
                                   t: 0, life: 0.6, seen: !!q });
          }
          if (f.bulwarkScorch.length > 8) f.bulwarkScorch.splice(0, f.bulwarkScorch.length - 8);
        }
        /* THE BANK, ON THE CASTER: a ward "+3" in the vigil branch's own
           float (its colour, its size, its seat), a block's and an arrow's
           alike -- both bank; and once a window the WARD tag, the first in a
           match carrying its one line (the vigil branch's own teaching). A
           shield already at the cap banks nothing and floats nothing. */
        if (got >= 1 && f.alive){
          this.float(f.x, f.y - 44, "+" + got, AFFINITIES.vigil.glow, 22 + got * 0.5);
          if (!f.bulwarkTagged){
            f.bulwarkTagged = true;
            const first = !this.taught.ward && !!STATUS.ward.tip;
            if (first) this.taught.ward = true;
            this.statusTag(f.x, f.y, "ward", first);
          }
        }
      }
      const P = f.bulwarkShots;
      P.length = 0;
      if (Z) for (const s of this.shots){
        if (s.stuck) continue;
        const vy = s.vy + (s.grav || 0) * dt;
        P.push(s.x + s.vx * dt, s.y + vy * dt, s.r || 6);
      }
    }
  }

  tickWinnow(dt){
'''),

('bulwark picture: the world call (over both fighters)',
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* BULWARK'S WALL OF LIGHT (v77 section 5), OVER BOTH FIGHTERS: it stands
       in front of the sword, which swings through it, and over the ward
       ring it rises out of; every ball's disc is cut out of it, so a foe
       pressed against it is in front of the light, never under it
       (CLAUDE.md 4.1b). World pass: its halo is drawn, not bloomed. */
    this.drawBulwark(m);
'''),

('bulwark picture: the drawing methods',
 '''  drawStatus(m, f){
''',
 '''  /* -------------------------------------------------- BULWARK'S PICTURE ---
     v77 section 5, drawn off the FIGHTER (`bulwark*`, driven by
     `tickBulwark`) and the sim's own geometry, rebuilt at draw time as
     `tickLightwall` builds it -- the centre `ahead` along theta, `half`
     either way across the facing -- so the bar is where the test is, and it
     swings with the blade because theta does. Never `m.ultFx` (one slot
     the opponent's cast takes: open item 25). Nothing draws from the rng:
     the motes are placed by shellHash. One method a component, so each can
     be measured alone.
       drawBulwark     the clip (every ball's disc cut out), then each bar
       _bulwarkAt      a point on the bar: the straight wall, blended by the
                       rise (or the fold) toward the arc of the ward ring it
                       comes out of (`_stWard`'s radius, R + 17, one plate's
                       width round the facing)
       _bulwarkHalo    the soft 14-unit halo, in vigil pink
       _bulwarkMotes   10 motes shed off both faces (the design's field, drawn)
       _bulwarkBody    the 6-wide bar and its pale heart; white on a block
       _bulwarkScorch  an arrow's scorch where it died on the bar */
  drawBulwark(m){
    if (!(m.a.bulwarkFade > 0) && !(m.b.bulwarkFade > 0)) return;
    const c = this.ctx, R = CONFIG.physics.ballR;
    c.save();
    c.beginPath();
    c.rect(-4000, -4000, 8000, 8000);
    for (const f of [m.a, m.b, ...m.shades]){
      if (f.alive === false) continue;
      c.moveTo(f.x + R * 0.98, f.y);
      c.arc(f.x, f.y, R * 0.98, 0, TAU, true);            // reverse winding = hole
    }
    c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [m.a, m.b]) if (f.bulwarkFade > 0) this._bulwarkBar(m, f);
    c.restore();
  }
  _bulwarkBar(m, f){
    const c = this.ctx, u = f.w.ult, P = AFFINITIES.vigil, R = CONFIG.physics.ballR;
    const j = clamp(f.bulwarkAge / 0.5, 0, 1), k = clamp(f.bulwarkOut / 0.5, 0, 1);
    const e = j * j * (3 - 2 * j) * (1 - k * k * (3 - 2 * k));
    /* up at once on the ring as it rises (the front of the ward lighting),
       down with the bar as it folds */
    const al = clamp((k > 0 ? 0 : 0.4) + e * 4, 0, 1);
    if (!(al > 0.004)) return;
    const th = f.theta, ux = Math.cos(th), uy = Math.sin(th);
    const G = { e, th, fx: f.x, fy: f.y, ux, uy, px: -uy, py: ux,
                cx: f.x + ux * u.ahead, cy: f.y + uy * u.ahead, half: u.half,
                rr: R + 17, phi: TAU / 5 * 0.38 };
    const N = e > 0.999 ? 1 : 12, pts = [];
    for (let i = 0; i <= N; i++) pts.push(this._bulwarkAt(G, -1 + 2 * i / N));
    this._bulwarkHalo(c, pts, al, P);
    this._bulwarkMotes(c, f, G, al, P);
    this._bulwarkBody(c, pts, al, P, f.bulwarkFlash > 0);
    this._bulwarkScorch(c, f, G, al);
  }
  _bulwarkAt(G, s){
    const bx = G.cx + G.px * s * G.half, by = G.cy + G.py * s * G.half;
    if (G.e > 0.999) return [bx, by];
    const a = G.th + s * G.phi;
    const rx = G.fx + Math.cos(a) * G.rr, ry = G.fy + Math.sin(a) * G.rr;
    return [rx + (bx - rx) * G.e, ry + (by - ry) * G.e];
  }
  _bulwarkLine(c, pts){
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    c.stroke();
  }
  /* THE HALO: 14 units either side of the bar, soft -- three strokes,
     each narrower and denser, so it falls off without a shadowBlur on a
     220-unit stroke every frame. */
  _bulwarkHalo(c, pts, al, P){
    c.strokeStyle = P.core;
    c.globalAlpha = al * 0.09; c.lineWidth = 6 + 2 * 14;
    this._bulwarkLine(c, pts);
    c.globalAlpha = al * 0.13; c.lineWidth = 6 + 14;
    this._bulwarkLine(c, pts);
    c.globalAlpha = al * 0.2; c.lineWidth = 6 + 5;
    this._bulwarkLine(c, pts);
  }
  /* MOTES OFF BOTH FACES for the whole window -- the design's field, DRAWN:
     a particle field fires once, at the cast, from the one ultFx slot,
     while the bar moves and swings with the ball for 8s. Each is placed
     along the bar by shellHash on its own count and drifts off its face. */
  _bulwarkMotes(c, f, G, al, P){
    if (!(G.e > 0.5)) return;
    c.fillStyle = P.glow;
    for (let j = 0; j < 10; j++){
      const a = f.bulwarkAge + j * 2.0 / 10, n = Math.floor(a / 2.0);
      const k = (a - n * 2.0) / 2.0;
      const h1 = shellHash(7717 + f.side, n * 16 + j), h2 = shellHash(7723 + f.side, n * 16 + j);
      const d = (h2 < 0.5 ? -1 : 1) * (3 + 16 * k);
      const q = this._bulwarkAt(G, (h1 - 0.5) * 1.84);
      c.globalAlpha = al * Math.sin(Math.PI * k) * 0.8;
      c.beginPath();
      c.arc(q[0] + G.ux * d, q[1] + G.uy * d - 6 * k, 1.1 + 1.1 * ((h1 * 7.3) % 1), 0, TAU);
      c.fill();
    }
  }
  /* THE BAR: 6 wide in vigil pink with a pale heart -- light, read by its
     value against the floor. A BLOCK FLASHES IT WHITE for two frames,
     source-over (v77). */
  _bulwarkBody(c, pts, al, P, flash){
    c.globalAlpha = al;
    c.strokeStyle = flash ? "#FFFFFF" : P.core; c.lineWidth = 6;
    this._bulwarkLine(c, pts);
    c.strokeStyle = flash ? "#FFFFFF" : P.glow; c.lineWidth = 2;
    this._bulwarkLine(c, pts);
  }
  /* AN ARROW'S SCORCH where it died, riding the bar (its place ALONG the bar
     is kept, not its place in the hall): a char mark in `_stWard`'s own
     value-break edge, gone in 0.3s (v77), and for its first 0.12s the
     strike, a white ring thrown off the spot. */
  _bulwarkScorch(c, f, G, al){
    for (const q of f.bulwarkScorch){
      const k = q.t / q.life;
      if (k >= 1) continue;
      const p = this._bulwarkAt(G, q.s / G.half);
      c.save();
      c.translate(p[0] + G.ux * q.side * 1.5, p[1] + G.uy * q.side * 1.5);
      c.rotate(Math.atan2(G.py, G.px));
      c.globalAlpha = al * (1 - k * k) * 0.9;
      c.fillStyle = "#1A0512";
      c.beginPath(); c.ellipse(0, 0, 9 * (1 - 0.3 * k), 4.2, 0, 0, TAU); c.fill();
      if (k < 0.4){
        /* the strike: a white ring thrown off the spot onto the dark floor
           round the bar, where white reads (on the pale bar it would not) */
        const h = k / 0.4;
        c.globalAlpha = al * (1 - h);
        c.strokeStyle = "#FFFFFF"; c.lineWidth = 2.2 * (1 - 0.5 * h);
        c.beginPath(); c.arc(0, 0, 4 + 14 * Math.sqrt(h), 0, TAU); c.stroke();
      }
      c.restore();
    }
  }

  drawStatus(m, f){
'''),

("bulwark picture: the nova's plate ring retired",
 '''    /* ---- Bulwark: the plates' footprint, a tiled ring ---------------------- */
    else if (u.w === "lightkeeper"){
      const ex = clamp(u.t / 0.34, 0, 1);
      const fade = 1 - clamp((u.t - 0.4) / 0.85, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      const N = 18;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.5;
        c.globalAlpha = 0.4 * fade * (1 - ex * 0.4);
        c.strokeStyle = "#F06BB8"; c.lineWidth = 2;
        c.beginPath();
        c.arc(u.x, u.y, Math.max(1, R), a, a + TAU / N * 0.62);
        c.stroke();
      }
    }
''',
 '''    /* ---- Bulwark's plate ring was the NOVA's footprint; retired with it (v77,
       v107 stage 6). The wall's picture is `drawBulwark`, off the fighter,
       where the one ultFx slot cannot erase it. */
'''),

("bulwark picture: the nova's plates retired",
 '''    /* ---- Bulwark: interlocking plates of light, let go ---------------------- */
    else if (u.w === "lightkeeper"){
      const ex = clamp(u.t / 0.34, 0, 1);
      const fade = 1 - clamp((u.t - 0.4) / 0.85, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      const N = 18;
      c.save();
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.5;
        const w = TAU / N * 0.60;
        const h = 26 * (1 - ex * 0.45);
        c.save();
        c.translate(u.x + Math.cos(a + w / 2) * R, u.y + Math.sin(a + w / 2) * R);
        /* each plate TILTS as it flies — the thing that makes this read as
           armour let go rather than a ring of light expanding */
        c.rotate(a + w / 2 + Math.PI / 2 + ex * 0.5 * (i % 2 ? 1 : -1));
        c.globalAlpha = fade * (1 - ex * 0.5);
        c.fillStyle = "#F06BB833";
        c.strokeStyle = "#FFD1EC"; c.lineWidth = 2;
        c.shadowColor = "#F06BB8"; c.shadowBlur = 12;
        const wpx = R * w;
        c.beginPath();
        c.moveTo(-wpx / 2, -h / 2); c.lineTo(wpx / 2, -h / 2 + 4);
        c.lineTo(wpx / 2, h / 2 - 4); c.lineTo(-wpx / 2, h / 2);
        c.closePath(); c.fill(); c.stroke();
        c.shadowBlur = 0;
        c.restore();
      }
      c.restore();
    }
''',
 '''    /* ---- Bulwark's plates of light let go were the NOVA's (eighteen plates
       thrown out to radius 300); retired with it (v77, v107 stage 6). The
       cast is the bar rising out of the ward ring (`drawBulwark`). */
'''),

('bulwark picture: the charge rune',
 '''  /* BULWARK -- the shield, and the shove that comes off it. */
  lightkeeper(c, t, cf, P){
    SG.ring(c, 0, 0, 0.55 + cf * 0.42, P.glow, 0.07, 0.2 + cf * 0.6);
    SG.poly(c, [[0, -0.72], [0.56, -0.42], [0.56, 0.2], [0, 0.76], [-0.56, 0.2], [-0.56, -0.42]],
            P.core, 0.85);
    SG.path(c, [[0, -0.5], [0, 0.5]], P.glow, 0.07, 0.5 + cf * 0.4);
    SG.path(c, [[-0.34, -0.1], [0.34, -0.1]], P.glow, 0.07, 0.5 + cf * 0.4);
  },
''',
 '''  /* BULWARK -- a wall of light raised out of the ward. The nova's ring and
     its shield went out with the nova (v77): five plates round the ball, and
     a bar standing up out of the front of them as the charge fills, with an
     arrow stopped dead against it. */
  lightkeeper(c, t, cf, P){
    for (let i = 0; i < 5; i++){
      const a0 = -Math.PI / 2 + i * TAU / 5 + 0.1;
      SG.arc(c, -0.42, 0, 0.36, a0, a0 + TAU / 5 - 0.2, P.core, 0.13, 0.45 + cf * 0.45);
    }
    const h = 0.2 + cf * 0.66;
    SG.path(c, [[0.18, -h], [0.18, h]], P.core, 0.26, 0.3 + cf * 0.3);
    SG.path(c, [[0.18, -h], [0.18, h]], P.glow, 0.1, 0.55 + cf * 0.45);
    SG.path(c, [[0.94, 0.02], [0.4, 0.02]], P.steel, 0.07, 0.3 + cf * 0.55);
    SG.poly(c, [[0.3, 0.02], [0.44, -0.08], [0.44, 0.12]], P.steel, 0.35 + cf * 0.6);
  },
'''),

("bulwark picture: the cast record's life",
 '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
''',
 '''              /* BULWARK's 1.5 went out with the nova (v77, v107 stage 6): the cast's
                 record falls to the map's own 1.5 and carries the CAST only -- no
                 set-piece draws from it; the wall is drawn off the fighter. */
              ironhail: 1.3, farwarden: 2.6,
'''),

]

# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`bulwarkScorch` is a suffix of `_bulwarkScorch`; the base's renderer reads
# `u.w === "lightkeeper"` in the two nova branches stage 6 retires, so the Sfx
# arm is found by its whole `} else if (w === "lightkeeper"){` line, never by
# the comparison).
S6_NAMES = ("tickBulwark", "drawBulwark", "_bulwarkBar", "_bulwarkAt", "_bulwarkLine", "_bulwarkHalo",
            "_bulwarkMotes", "_bulwarkBody", "_bulwarkScorch", "bulwarkFade", "bulwarkAge", "bulwarkOut",
            "bulwarkFlash", "bulwarkSeen", "bulwarkShots", "bulwarkScorch", "bulwarkTagged", "tinkK",
            '"lightkeeper-gong"', '"lightkeeper-tink"', '"lightkeeper-fold"')
S6_CAST_ARM = '} else if (w === "lightkeeper"){'
# What stage 6's ADDED code may write: its own bulwark* fields (and their
# arrays' length), the canvas, a scorch record's own clock, `taught.ward`, an
# oscillator's pitch, and the length of `P` (tickBulwark's alias of its own
# `bulwarkShots`). Arrays it may push to, splice, sort or index-write: its own
# bulwark* arrays, their aliases `P` (bulwarkShots) and `S` (bulwarkSeen), and
# the locals `near` and `pts`.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("bulwark") or obj.startswith("bulwark") or obj == "c"
               or (obj, prop) in {("q", "t"), ("taught", "ward"), ("frequency", "value"), ("P", "length")})
S6_ARRAY_OK = (lambda obj: obj.startswith("bulwark") or obj in ("P", "S", "near", "pts"))


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies, with fx_remove.py)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]



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


NEW_NAMES = ("ultWall", "wallTally", "tickLightwall", 'kind:"lightwall"')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-lightkeeper"):
        raise SystemExit(f"refusing {out_p.name}: this relic's links are named "
                         "sc-lightkeeper*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: a link of that name is already "
                         "on the chain")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nLIGHTKEEPER / BULWARK (redesign) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS ASSERTED BY CONTENT: the features this build needs, never
    # which relic is last.
    for need, why in (
            ("tickTendril(dt){", "no tickTendril -- the window tickers' anchor is missing"),
            ("this.tickTendril(dt);", "no tickTendril call to follow"),
            ("  tickWinnow(dt){", "no tickWinnow to precede"),
            ('if (u.kind === "tendril"){', "no tendril cast branch to precede"),
            ("this.vineTally = null;", "no vineTally field to follow"),
            ("function segDist(ax, ay, bx, by, px, py){", "segDist is not the engine's"),
            ("if (dead && s.net && !s.stuck){", "no net endpoint rule in tickShots"),
            ("if (s.stuck) continue;", "tickShots no longer skips a stuck arrow"),
            ("f.charge += dt;", "the charge is no longer pure wall time"),
    ):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    # THE NET ENDPOINT WRITE THIS BUILDER COPIES IS STILL tickShots' OWN.
    if "s.stuck = true; s.vx = 0; s.vy = 0; s.life = 1e9;" not in code:
        raise SystemExit("wrong base: tickShots' stuck write has changed")
    # THE ORDER: tickShots, then the window tickers, then tickHits.
    i_sh, i_tt = code.find("    this.tickShots(dt);"), code.find("    this.tickTendril(dt);")
    i_hits = code.find("this.tickHits(self, foe, dt);", i_tt)
    if not (0 <= i_sh < i_tt < i_hits):
        raise SystemExit("wrong base: tickTendril does not sit between tickShots "
                         "and tickHits")
    row = relic_row(code, RELIC)
    # Stage 6 goes on stage 5's link, whose blade is BLADE; the rest of the
    # profile is still the shipped one.
    phys = PHYS if A.stage != "6" else PHYS.replace("dmg:10.54,", f"dmg:{BLADE},")
    if phys not in " ".join(row.split()):
        raise SystemExit("Lightkeeper's greatsword profile has moved -- not the "
                         "shipped relic this builder redesigns")
    if "onSelf:{ ward:1 }, knockMul:1.0," not in row:
        raise SystemExit("Lightkeeper no longer carries onSelf ward 1 / knockMul 1.0")
    # THE NOVA STAYS FOR THE OTHERS (what is retired is Lightkeeper's only).
    # This build touches none of the nova's code (the lightwall branch returns
    # before the generic tail), so it needs no other relic to be a nova. It
    # READS who still is, and never refuses on it: Widowmaker's own redesign
    # (v106) takes Exsanguinate off the nova, and it may be carried first.
    novas = [nv for nv in re.findall(r'\{ id:"([a-z]+)", name:"', code)
             if nv != RELIC and 'kind:"nova"' in relic_row(code, nv)]
    print("  base  the window tickers' anchors, the net endpoint rule and the ward; "
          "Lightkeeper's shipped profile; the nova's tail kept, untouched, for "
          + (", ".join(novas) if novas else "no other relic"))

    if A.stage == "1":
        if " ".join(strip_comments(OLD_ULT).split()) not in " ".join(row.split()):
            raise SystemExit("Lightkeeper's nova is not in this source -- stage 1 "
                             "goes on the shipped relic, once")
        for name in NEW_NAMES:
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
        edits, want = S1, ult_block("1e9", 0, 0)
    else:
        if 'kind:"lightwall"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultWall" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            for name in ("wallTally", "tickLightwall"):
                if name in code:
                    raise SystemExit(f"'{name}' is already in the base")
            edits, want = S2, ult_block(ULT["charge"], 0, 0)
        elif A.stage == "3":
            if "ultWall" not in code or "bankBall:0, bankShot:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["bankBall"], ULT["bankShot"])
        elif A.stage == "6":
            # STAGE 6 GOES ON THE FINAL, ONCE: the bank 3 / 3 and the blade
            # 9.5 (stage 5's link); none of stage 6's names is in the source
            # yet (on identifier boundaries) and the Sfx has no Lightkeeper arm.
            if (f'bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},' not in row
                    or f"dmg:{BLADE}," not in row):
                raise SystemExit("stage 6 goes on the final (stage 5's link: the bank "
                                 f"{ULT['bankBall']} / {ULT['bankShot']}, blade {BLADE})")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_CAST_ARM in code:
                raise SystemExit("the Sfx already has a Lightkeeper arm -- stage 6 goes on once")
            edits, want = S6, ult_block(ULT["charge"], ULT["bankBall"], ULT["bankShot"])
        else:
            if f'bankBall:{ULT["bankBall"]}, bankShot:{ULT["bankShot"]},' not in row \
                    or "dmg:10.54," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bankBall"], ULT["bankShot"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Lightkeeper's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or moves, writes only what
    # S6_WRITE_OK names and mutates only its own arrays. It READS the window,
    # the tally, the shots and the fighters; the probe's [9]-[10] and
    # engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickLightwall|tickShots|spawnShot|move)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort|fill|copyWithin)\(", ins):
            if mw.group(2) == "fill" and mw.group(1) == "c":
                continue                                   # the canvas's fill(), not an array's
            if not S6_ARRAY_OK(mw.group(1)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_ARRAY_OK(mw.group(1).split(".")[-1]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
    if A.stage == "6":
        if inlined_fx(s) != inlined_fx(s0):
            raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                             "(the nova's field spec is the orchestrator's fx_remove.py)")
        if re.search(r'\bu\.w === "lightkeeper"', out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's art on the ultFx slot is still drawn")
        if re.search(r"\blightkeeper: 1\.5\b", out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's life entry is still in the map")
        for need, n in (('SFX.play("ult", { w: "lightkeeper-tink", k: tinkK++ });', 1),
                        ('SFX.play("ult", { w: "lightkeeper-gong" });', 1),
                        ('if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });', 1),
                        (S6_CAST_ARM, 1), ('} else if (w === "lightkeeper-gong"){', 1),
                        ('} else if (w === "lightkeeper-tink"){', 1), ('} else if (w === "lightkeeper-fold"){', 1),
                        ("this.tickBulwark(dt);", 1), ("  tickBulwark(dt){", 1),
                        ("this.drawBulwark(m);", 1), ("  drawBulwark(m){", 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields); the inlined fx.js untouched; the nova's art out; "
              "four voices and one picture hook wired once each")
    for label, _old, new in S1 + S2 + S3 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(dmg|spin|reach|blades|mass|width|arc|ult)\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins) or \
                re.search(r"\bw\.ult\.\w+\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        # THE SHARED MODULE TABLES (third review round): STATUS, CONFIG,
        # AFFINITIES, WEAPONS and SHAPES are every relic's and every later
        # match's. The inserts READ two of them (`STATUS.ward` as `W`, and
        # `CONFIG.physics.ballR`); none may write one, by its name or through
        # a local alias of it (`const W = STATUS.ward` then `W.cap = ...`).
        tables = r"(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES)"
        aliases = re.findall(r"\b(\w+)\s*=\s*" + tables + r"\b[\w.\[\]\"']*\s*[,;)]", ins)
        for nm in [tables] + [re.escape(x) for x in aliases]:
            if re.search(r"\b" + nm + r"\s*[.\[][\w.\[\]\"']*\s*(?:[-+*/%]?=(?!=)|\+\+|--)", ins) or \
                    re.search(r"(?:\+\+|--)\s*" + nm + r"\s*[.\[]", ins) or \
                    re.search(r"\bdelete\s+" + nm + r"\b", ins) or \
                    re.search(r"\bObject\.(?:assign|defineProperty|defineProperties|setPrototypeOf)\(\s*" + nm + r"\b", ins):
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes a "
                                 "shared module table (STATUS / CONFIG / AFFINITIES / "
                                 "WEAPONS / SHAPES)")
        if "this.beat(" in ins or "hitStop" in ins or "this.hurt(" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' files a beat, "
                             "a hit stop or damage (the wall does none)")
        # NOTHING ELSE (second review round): the wall's only status is the
        # bank's own ward; it stuns, pins and burdens nobody.
        if re.search(r"\.(stun|stunDR|pin|pinV|pinMax|pinFree|burden|launch)\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins) or \
                any(k != "ward" for k in re.findall(r'\.apply\(\s*"(\w+)"', ins)):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stuns, pins, "
                             "burdens or lays a status other than the bank's ward")
    if len(re.findall(r'kind:"lightwall"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one lightwall ultimate")
    if 'kind:"nova"' in relic_ult(out_code):
        raise SystemExit("REFUSING TO WRITE -- Lightkeeper still casts the nova")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    if n_ids != len(re.findall(r'\{ id:"[a-z]+", name:"', code)):
        raise SystemExit("REFUSING TO WRITE -- the roster changed size (a "
                         "redesign adds no relic)")
    print(f"  ok    one lightwall ultimate, Lightkeeper's; the nova gone from its row; "
          f"no insert draws the RNG, writes the shared weapon or a shared table, beats, stops, "
          f"hurts, stuns, pins or lays a status but the ward; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
