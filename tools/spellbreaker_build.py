#!/usr/bin/env python
"""SPELLBREAKER / UNMAKING, REDESIGNED -- hexes stun twice as long, every hit hexes twice. v111.

Built from `06-docs/v79/spellbreaker-unmaking-redesign-v79.md` (Cowork,
2026-09-26), its §5 build brief and its runs (`06-docs/v79/runs/unmaking_*`,
`tools/overlays/unmaking.js`), which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. A REDESIGN: the relic
ships in the base; its ultimate is replaced.

    stage 1   the new ultimate stubbed (1e9); the bolt out
                                          <tip> -> sc-spellbreaker-stub.html     (= arm A)
    stage 2   the stun x2 on the foe      -> sc-spellbreaker-stun.html           (brief stage 1:
                                             lab arm D --P stunMul=2 hexExtra=0)
    stage 3   the double hex              -> sc-spellbreaker-unmaking.html       (brief stage 2:
                                             lab arm D --P stunMul=2)
    stage 5   the blade (brief stage 3, "to the shipped rate"), 8.81 -> 7.5:
              the measured point nearest the shipped rate (the batch's
              redesign blade policy) -> sc-spellbreaker-b7.5.html  (stage 6 goes on it)
              Rick's two other choices, each one number away (neither is the
              carry):
              `--stage 5 --alt-row`  8.30, the twinblade row's floor and the
                                     brief's lowest grid point
                                          -> sc-spellbreaker-b8.3.html
              `--stage 5 --alt50`    7.7, the 50% crossing
                                          -> sc-spellbreaker-b7.7.html
    stage 6   the picture and the voice (brief stage 4), on stage 5's link
                                          -> sc-spellbreaker-b7.5-fx.html  THE FINAL LINK
              presentation only; no fx.js field (reading 19): the bolt's
              SPECS.spellbreaker is the orchestrator's `fx_remove.py` at the carry

§1: "For a duration Spellbreaker's hexes bite deeper: every stun a hex lands
on the enemy's weapon lasts twice as long, and every hit Spellbreaker lands
hexes twice."

Declared (§1, §3, §4; the lab `overlays/unmaking.js`, arm D, the taken arm:
no shrink, `stunMul` 2 -- the lab's DEFAULT is 1, and every settled run passed
`--P stunMul=2` -- and `hexExtra` 1, its default):
  THE STUN     while the caster's window is open, every hex stun that lands on
               the OPPONENT's weapon lasts STATUS.hex.stunFor x stunMul
               (0.2 x 2 = 0.4s). Read through the foe's own `hexStunMul` (§4).
  THE HEX      every blow the caster lands while its window is open applies
               `hexExtra` (1) more hex beside the blow's own onHit hex 1 (§4:
               "+1 hex in resolveHit on a blow by a caster with ultUnmake").
  Nothing else: no damage, no knock, no hit stop, no beat, no shrink. No rng.

THE CHARGE. The design names none. Every run it was priced on
(`unmaking_*.json`: "charge": 16.0) cast every 16 seconds of the LAB's step
clock, the harness's default, which counts hit-stop freezes. Rick,
2026-09-27, for the whole batch: "use the game's equivalent". Measured for
this fighter on the lab's arms (v111 §0): CHARGE below. (The shipped bolt
charged 13.)

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE WINDOW IS 8s: §1 says "for a duration"; every priced arm used the
     harness's dur 8.
  2. THE CHARGE is the lab's 16 converted (above).
  3. THE STUN MULTIPLIER IS THE FOE'S OWN FIELD (§4): `f.hexStunMul`, 1 on
     every fighter, recomputed for BOTH fighters on every window-ticker frame
     as a pure function of whether the OTHER fighter's Unmaking is open --
     Bloodletting's rule ("recomputed and never restored"): a fresh Match
     starts at 1 and a close puts it back on the same frame. So a runic foe's
     hexes on Spellbreaker are untouched (§4). The lab set the global
     `STATUS.hex.stunFor`, which doubled every hex stun in the match --
     Spellbreaker's own from a runic foe included: DECLARED by §4.
  4. THE FIELD IS THE TWO FIGHTERS' (Bloodletting's rule iterates the pair):
     a Twinshade shade keeps 1, where the lab's global doubled its stuns too.
     The probe counts those stuns.
  5. EVERY STUN A HEX LANDS: both reads of the hex proc -- the weapon's stun
     and `breakSpin`'s true-stun length -- are STATUS.hex.stunFor x the
     fighter's hexStunMul. A stun that lands in the window keeps its length
     after the close (it is the weapon's clock, as the lab's was).
  6. THE SECOND HEX goes where the blow's own hex goes: resolveHit's struck
     body, after the blow's onHit (so a blow on a Twinshade shade hexes the
     shade twice), on every blow the caster lands while its window is open
     ON A BODY THE BLOW LEFT ALIVE -- the lab's own guard (`if (hex &&
     foe.alive)`): the killing blow gets the channel's hex alone, as in the
     lab, and no second hex lands on a corpse. The lab applied it at the end
     of the frame to the OPPONENT when the caster's hit count rose; on a blow
     on the opponent the two leave the same stacks at the next tickStatus
     (nothing reads hex in between), and only a blow on a shade differs (the
     probe counts them). `apply`'s source is a side letter (Rick's ruling 4;
     the lab passed the Fighter; hex's source has no reader). It sits right
     after the onHit loop, before Nightfell's Deadfall comment and code, so
     that comment stays on the code it explains.
  7. THE WINDOW CLOSES on its clock or EITHER death (the lab's); the stun
     multiplier drops on the close's frame; no second hex after it.
  8. NO CAST WAITS. The design asks none, and a cast cannot find its window
     open: the charge is 14 of unfrozen time against a window of 8 on the same
     clock (the probe asserts it on every cast).
  9. NO SHRINK: arm D is the taken arm (§3: the shrink is worth +6 and costs
     the blade; "D double hex + stuns x2 (taken)"). x2, not x3 (§3; §6.3 is
     Rick's open decision, and x3 "needs a blade under the row").
 10. THE CARD is the design's own (§4, 68 characters): `Hexes stun the foe's
     weapon twice as long, and every hit hexes twice`.
 11. THE BOLT IS OUT (brief stage 1): Spellbreaker's ult block (kind "bolt",
     dmg 20, apply hex 3) is replaced. No code keys on `kind === "bolt"` (the
     builder asserts it), so no cast branch goes; fireUlt's generic tail
     stays whole -- its damage clause and its `u.apply` loop serve five other
     ult blocks (Widowmaker, Thornwake, Censer, Oathwound, Heartwood). The
     bolt's PICTURE (drawUltOver's `u.w === "spellbreaker"` lightning and
     cage, the banner's `onTarget` seat and its letter scatter, the ultFx
     `life` entry, the charge rune `ULTSIG.spellbreaker`), its cast voice
     (the rune-crack fallback) and its field spec (`SPECS.spellbreaker`, mode
     'beam') are the brief's stage 4 ("bolt's field spec out"), this builder's
     stage 6 (readings 13-20): the picture and the voice are retired and
     replaced there, and the field spec is the orchestrator's `fx_remove.py`
     at the carry (reading 19). Nothing in the simulation reads any of them.
 12. THE UNMAKING IS A STUN LENGTH AND AN apply() AND NOTHING ELSE: the ticker
     and the second hex hurt nobody, move nobody, stop nothing, file nothing
     and draw no rng.

STAGE 6, the picture and the voice (v79 §4; the art and the sound are Claude
Code's picks under Rick's "you pick i overrule", made on the labs' numbers,
v111 §5; the rows are the labs' own, byte for byte):
 13. THE PICTURE READS THE WINDOW off `ultUnmake && alive && !over` and keeps
     its own state on the fighter (`unmk*`), never on `m.ultFx` (one slot, and
     the opponent's cast takes it: open item 25). `tickUnmaking`, in
     tickPresentation, drives it: the script written along both blades over
     0.3s at the cast and unwritten tip to hilt over 0.2s at a clock close, a
     death or the verdict (`tickUnmake` never runs once `over` is set).
 14. THE GREY KEYS ON THE HEX PROC, not on the stun (`f.stun` has many
     writers): a drop in a fighter's `hexClock` (nothing else resets it), read
     with the `hexStunMul` last seen (tickUnmake rewrites it later in the same
     step). A proc at more than x1 greys the WHOLE weapon (the canvas's
     grayscale(1); alpha 0.6 where a plain stun dims to 0.42) for that stun's
     own stunFor x mul, counted down with the fighter's own stun: frozen
     through a hit stop as the stun is, gone when it is.
 15. THE TAG: a step her `unmakeTally.extra` rose is a step a blow of hers
     landed its second hex, and the hex tag that blow pushed is relabelled
     `HEX +2` (its `val`, and a flag `unmk`; the tags are the renderer's and
     nothing in the simulation reads them). Not the killing blow (no second
     hex), not the match's first hex (its teaching panel prints no count),
     never a tag on her own ball.
 16. THE MOTES ARE DRAWN, not a field (reading 19): shed off both blades while
     the window is open, placed by `shellHash` on their count (no rng), in the
     world pass under both balls, source-over (nothing the bloom sees).
 17. THE VOICES ON THE SIM PATH ARE TWO LINES: the stun voice after the hex
     proc's breakSpin, when the fighter's `hexStunMul` is over 1 (read as the
     proc's own two lines read it); the close voice before the window's close
     line, on a close BY ITS CLOCK with both alive. The cast's voice is
     fireUlt's own prologue call, `SFX.play("ult", { w: f.w.id })`, which the
     new arm now answers instead of the rune-crack fallback.
 18. NO CLOSE VOICE ON A DEATH: the death voice has that moment (Tendril's,
     Canopy's, Zenith's, Lightkeeper's and Benediction's rule); a window still
     open when the fight ends closes in the picture only.
 19. NO fx.js FIELD: a field fires once from the one ultFx slot where the
     caster stood; the picture lab measured it hers a median 0.67s of a
     window, and her hub a median 193 units from its spawn (v111 §5b). The
     bolt's `SPECS.spellbreaker` (mode 'beam') is the orchestrator's
     `fx_remove.py --relic spellbreaker` at the carry: this builder edits
     neither fx.js copy, and stage 6 refuses if its edits touched the inlined
     one.
 20. THE BOLT'S ART IS RETIRED WITH THE BOLT: drawUltOver's branch (the
     jagged bolt, its glyphs and the cage; it drew Math.random), the banner's
     seat on the quarry (the name now lands on her, the default seat) and the
     life entry 1.4 (the cast's record falls to the map's own 1.5; nothing
     draws from it). The charge rune `ULTSIG.spellbreaker` (a rune coming
     apart: the name's) and the banner's letter scatter are kept.

THE CLOCK. The window runs on the window tickers' clock, which stops through a
hit stop (Corollary's, Daybreak's, Zenith's, Canopy's, Onslaught's, Tendril's,
the hail's and the halo's convention). The lab ran it through freezes; v111 §2
measures what that is worth here.

THE BASE is asserted BY CONTENT, never by which relic is last: Spellbreaker's
row with the shipped Unmaking verbatim and its shipped blade, STATUS.hex as
priced, tickStatus's hex proc, the onHit loop, and every anchor below exactly
once. Every insert goes AFTER or BEFORE a stable line, so the builder
re-applies on a later tip that carries other new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "spellbreaker"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v79 §1, §3-§5.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v111 §0)
    "dur": 8,         # "for a duration" -- the harness's 8, every unmaking arm
    "stunMul": 2,     # §3 "x2 (taken)"; §4 hexStunMul 2 while the window is open
    "hexExtra": 1,    # §4 "+1 hex in resolveHit on a blow" -- stage 3
}
TIP = "Hexes stun the foe's weapon twice as long, and every hit hexes twice"
SHIPPED_ULT = ('''    ult:{ name:"Unmaking", charge:13, kind:"bolt", dmg:20, apply:{hex:3}, '''
               '''tip:"Fires a bolt which deals 20 damage and applies 3 Hex stacks" },
''')
SHIPPED_DMG = "8.81"
ROW_HEAD = ('''  { id:"spellbreaker", name:"Spellbreaker", aff:"runic", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:''')
HEX_PROC = '''        f.stun = Math.max(f.stun, STATUS.hex.stunFor);
        /* A TRUE STUN. Hex is the status whose entire job is shutting a
           weapon down, so it is the one that should stop a weapon being
           wound up. No-op on every relic but one. */
        this.breakSpin(f, "the hex takes the wind out of it",
                       STATUS.hex.stunFor);
'''


def ult_block(charge, hex_extra) -> str:
    return (f'''    ult:{{ name:"Unmaking", charge:{charge}, kind:"unmake", dur:{ULT["dur"]},
          stunMul:{ULT["stunMul"]},
          hexExtra:{hex_extra},          // v79: the second hex (stage 3)
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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH to check the page")
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
# THE NEW ULTIMATE, STUBBED at charge 1e9 (the clock can never reach it, and
# `fireUlt` never runs for this relic), AND THE BOLT OUT. The row keeps every
# physical stat, the school's channel (onHit hex 1) and the blurb; only the ult
# block changes. Nothing else reads the ult block's fields, so this link must
# be the lab's arm A (the relic with no ultimate) fight for fight.
S1 = [

("Unmaking becomes the hex window, stubbed",
 SHIPPED_ULT,
 '''    /* UNMAKING, REDESIGNED (v79; built v111). The bolt that hit for 20 and
       put 3 hex on the foe is retired. For the window every hex stun on the
       foe's weapon lasts `stunMul` times as long (the foe's own
       `hexStunMul`), and every blow Spellbreaker lands hexes `hexExtra` more. See
       `tickUnmake`. */
''' + ult_block("1e9", 0)),

]

# ---------------------------------------------------------------- stage 2 --
# THE STUN x2 ON THE FOE (brief stage 1: "bolt out, `f.ultUnmake` in,
# `hexStunMul` on the foe"), the second hex written but inert at 0, and the
# charge on the game's clock.
S2 = [

("Unmaking has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Unmaking", charge:1e9, kind:"unmake", dur:8,
''',
 f'''    ult:{{ name:"Unmaking", charge:{ULT["charge"]}, kind:"unmake", dur:{ULT["dur"]},   // v79 stage 2: the window opens
'''),

("the fighter carries the window and its own hex-stun multiplier",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while SPELLBREAKER's Unmaking is open (v79). null on every
       other relic and on this one outside its window. `unmakeTally` is the
       probe's count, cumulative over the fight; nothing in the simulation
       reads it.
       `hexStunMul` IS EVERY FIGHTER'S OWN: the factor on the stun a hex lands
       on THIS fighter's weapon. 1 always, except while the OTHER fighter's
       Unmaking is open, when it is that ultimate's `stunMul`; recomputed for
       both fighters on every window-ticker frame (`tickUnmake`), never raised
       and restored -- Bloodletting's rule. A shade keeps its 1. */
    this.ultUnmake = null;
    this.unmakeTally = null;
    this.hexStunMul = 1;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "unmake"){
      /* UNMAKING (v79). NOTHING RESOLVES HERE: the cast opens the window for
         `u.dur` seconds; `tickUnmake` doubles the foe's hex stuns and
         `resolveHit` adds the second hex to every blow the caster lands. No damage
         and no hex at the cast: the bolt is retired. */
      f.ultUnmake = { t: 0, dur: u.dur };
      if (!f.unmakeTally)
        f.unmakeTally = { casts: 0, frames: 0, blows: 0, extra: 0, foeHex: 0 };
      f.unmakeTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the window ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickUnmake(dt);                // UNMAKING (v79)
'''),

("tickUnmake keeps the window and recomputes both fighters' hex-stun factor",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE UNMAKING ====
     v79 §1 / §4 / §5. The window's clock, and its close on the clock or
     EITHER death. Then, for BOTH fighters on every frame, whether or not
     anybody has cast anything, the factor on the stun a hex lands on that
     fighter's weapon: the other fighter's `stunMul` while the other
     fighter's Unmaking is open, 1 otherwise. RECOMPUTED AND NEVER RESTORED
     (Bloodletting's rule): a fresh Match starts at 1, and the close puts it
     back on its own frame. tickStatus reads it at the hex proc. On the
     window tickers' clock, so all of it freezes through a hit stop. No
     hurt, no knock, no stop, no beat, no rng. */
  tickUnmake(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultUnmake;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultUnmake = null; continue; }
      f.unmakeTally.frames++;
      f.unmakeTally.foeHex += foe.stacks("hex");
    }
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a;
      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : 1;
    }
  }

  tickWinnow(dt){
'''),

("a hex stun lasts the fighter's own hexStunMul times as long",
 HEX_PROC,
 '''        /* x `hexStunMul`: 1 except while the other fighter's UNMAKING is
           open (v79 §1 "every stun a hex lands on the enemy's weapon lasts
           twice as long"; §4 reads it through the foe's own field). Both
           reads, the weapon's stun and the true stun's length. */
        f.stun = Math.max(f.stun, STATUS.hex.stunFor * f.hexStunMul);
        /* A TRUE STUN. Hex is the status whose entire job is shutting a
           weapon down, so it is the one that should stop a weapon being
           wound up. No-op on every relic but one. */
        this.breakSpin(f, "the hex takes the wind out of it",
                       STATUS.hex.stunFor * f.hexStunMul);
'''),

("every blow in the window hexes `hexExtra` more",
 '''    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit
''',
 '''    /* UNMAKING'S SECOND HEX (v79 §1 "every hit Spellbreaker lands hexes
       twice"; §4 "+1 hex in resolveHit on a blow by a caster with
       ultUnmake"). After the blow's own onHit, on the body the blow struck,
       while the caster's window is open, if the blow left it alive (the
       lab's guard: no second hex on the killing blow). A side letter for the
       source (hex has no reader of it). Inert at hexExtra 0 (stage 2). */
    if (self.ultUnmake){
      const U = self.w.ult;
      self.unmakeTally.blows++;
      if (U.hexExtra > 0 && foe.alive){
        foe.apply("hex", U.hexExtra, self === this.a ? "a" : "b");
        self.unmakeTally.extra += U.hexExtra;
      }
    }

    /* ---- THE BLOW LEAVES A FIGURE ON THE FLOOR. Rick: "when it lands a hit
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the second hex",
 '''          hexExtra:0,          // v79: the second hex (stage 3)
''',
 f'''          hexExtra:{ULT["hexExtra"]},          // v79: the second hex (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (brief stage 3: "the blade, wide on 151 at 8.3 / 8.5 / 8.8 to the
# shipped rate"; §3: "x2 is 55.2 against a shipped 49.7 and the blade (8.81)
# comes to about 8.4, the row floor"; §6.2 "the blade target" is Rick's open
# decision). THE TARGET is the design's own, THE SHIPPED RATE, read on 151:
# Spellbreaker as shipped (the bolt at 8.81, charge 13) on the base,
# relic_rate both sides, two blocks (seed0 2207 / 2317, every other relic a
# foe, 10 seeds a foe a side, 1480 fights): 720 of 1480, 48.6%. THE PICK is
# the measured point nearest it (the batch's redesign blade policy, rule (iv)
# of the orchestrator's brief; no bisection).
# Both sides, two blocks, 1480 fights a point, relic_rate on
# sc-spellbreaker-unmaking (--set dmg; 8.81 is the link itself), in wins
# against the shipped 720:
#   8.81 -> 875 (59.1%, +155)
#   the brief's grid  8.8 -> 880 (59.5%, +160)   8.5 -> 843 (57.0%, +123)
#                     8.3 -> 803 (54.3%, +83)    -- ALL ABOVE THE SHIPPED RATE
#   under the grid    8.2 -> 784 (53.0%)  8.1 -> 794 (53.6%)  8.0 -> 814 (55.0%)
#                     7.9 -> 771 (52.1%)  7.8 -> 754 (50.9%)  7.7 -> 736 (49.7%)
#                     7.6 -> 731 (49.4%, +11)  7.5 -> 728 (49.2%, +8)  <- NEAREST
#                     7.4 -> 699 (47.2%, -21)  7.2 -> 655 (44.3%)  7.0 -> 626 (42.3%)
# The line through the fifteen: 9.0 points a unit of blade; the shipped rate at
# 7.57, 50% at 7.72. The design's "about 8.4" was priced on the lab's clock,
# side A; on the engine's window clock the Unmaking reads ~6 over its lab arm
# (v111 §2, attributed with controls), so the shipped rate falls under the
# brief's grid and under the twinblade row's floor (8.3: Twinshade and
# Starwarden; the row's numbers are v76's and the base's, not v79's -- v79
# names no bound for an x2 blade). THE BRIEF NAMES NO KNOB TO MOVE FIRST (the
# shrink is the arm §3 passed over; x2 or x3 is §6.3, Rick's). So THE CARRY IS
# 7.5, the measured point nearest the shipped rate (+8 wins, +0.5 points), and
# it is said (v111 §4).
BLADE = "7.5"
# RICK'S TWO OTHER CHOICES, each one number away (neither is the carry):
#   the twinblade row's floor and the brief's lowest point: 8.3 (803 of 1480,
#     54.3%, +83 wins). `--stage 5 --alt-row` -> sc-spellbreaker-b8.3. WRITTEN
#     "8.30" -- the same double -- so that if it ever becomes the carry,
#     `chain_audit.py` (which watches single lines) can tell Spellbreaker's row
#     line from Twinshade's and Starwarden's `dmg:8.3,` (the same line, character
#     for character, at 8.3).
#   50%, the batch's standard for a new relic: 7.7 (736, 49.7%, -4 wins from
#     half; 7.8 reads +14). `--stage 5 --alt50` -> sc-spellbreaker-b7.7
ALTROW_BLADE = "8.30"
ALT50_BLADE = "7.7"


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v79 §4's picture and sound; its §5 brief stage 4,
# "picture, voice, carry; bolt's field spec out"), picked on measurements under
# Rick's "you pick i overrule" by the picture lab (scratch, `sb_rows.py`) and
# `spellbreaker_voice_lab.py` (v111 §5). PRESENTATION ONLY: engine_ab over all
# 38 relics, Spellbreaker included, is the proof, and the probe's [7]-[8] read the
# voices and the picture's hook inside the fight. The rows are byte-exact to the
# labs' own files (voice 090b35214e0efe05, 3 rows; picture 6a3c73a527df3e45, 12
# rows); the picture rows alone reproduce the picture lab's stamp
# (176458b0df4a79cd), the voice rows alone the voice lab's page
# (149b777b7f1ccb90), and the two sets give the same bytes in either order
# (ceeff797e5739e0c). No two rows share an anchor line, so none is merged.
#   THE VOICE: three arms -- the cast's crack into a hum, a lengthened stun,
#   the hum cutting out -- ADDED before the shared rune-crack fallback, which is
#   re-emitted unchanged, last; two lines on the sim path, each beside a line
#   this build's stage 2 already wrote (the stun voice after the hex proc's
#   breakSpin, the close voice before the window's own close line).
#   THE PICTURE: `tickUnmaking` in tickPresentation (the script's clock, the
#   rune motes, the HEX +2 tag, the grey); the motes in the world pass under
#   both balls; the grey and the script in drawWeapon; the bolt's art retired
#   (drawUltOver's branch, the banner's seat on the quarry, the life entry).
# COMPOSITION: eleven anchors are re-emitted and four replaced: three
# consumed, all Spellbreaker's own (the bolt's drawUltOver branch, the onTarget
# map's narrowest token `spellbreaker:1, ` and the life map's
# ` spellbreaker: 1.4,`, which leave Thornwake's, Emberedge's and the other
# entries on their lines to their own builds), and drawWeapon's dim line,
# replaced by its own text with the grey's alpha in it. The rows ride on four
# of stage 2's own lines (the fields, the hex proc's breakSpin, the window's
# close line and tickUnmake's end) and
# on shared lines every stage 6 of the batch uses as `after` / `before` anchors
# (tickPresentation's first call, the world pass's drawTree, the fx banner
# comment, shellHash, drawWeapon, the rune-crack fallback).
S6 = [

("Sfx: Spellbreaker's cast, stun and close arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "spellbreaker"){               // the weapon unmade
          /* SPELLBREAKER'S CAST, THE UNMAKING -- v79 s4: "cast -- a glass
             crack into a hum, 0.4s". DRONE, of 5, picked on the numbers by
             `spellbreaker_voice_lab.py` under Rick's "you pick i overrule"
             (v111). Spellbreaker had no arm and fell through to rune-crack,
             which eleven other relics on its stage-5 link still use, so this
             ADDS arms before that fallback and leaves it alone.

             The crack: three 6 kHz clicks at 0 / 4 / 11 ms (a fracture runs)
             and a glass rod struck at G6 with its bar modes 1 : 2.76 : 5.40 --
             23 dB tonal, its 2.76 mode 145 cents off any harmonic. Into a C4
             triangle hum (261.63 Hz) coming in at level, re-struck in phase on
             every cycle (a held note does not exist in this toolkit), each
             strike 30 ms: held 0.9 dB steady at -10.0 dB re the crack's top,
             releasing over its last 0.1 s. Audible 400 ms. Its top -2.8 dB re
             Spellbreaker's blow; the crack +30.2 dB and the hum +8.4 dB over
             the score. Register at most 0.66 against rune-crack, the runic and
             twinblade casts, BAR, hex-snap, the blow and the death voice, and
             Angelus's cast and close. */
          const g = 0.5194;
          for (const [s, k] of [[0, 1], [0.004, 0.6], [0.011, 0.8]])
            this._burst(t + s, { freq: 6000, q: 0.7, gain: g * k, dur: 0.006, type:"highpass" });
          for (const [r, k, d] of [[1, 0.5, 0.07], [2.76, 0.3, 0.045], [5.4, 0.15, 0.03]])
            this._tone(t, { freq: 1567.982 * r, gain: g * k, dur: d, type:"sine" }).frequency.value = 1567.982 * r;
          for (let s = 0.025; s < 0.415 - 1e-9; s += Math.max(1, Math.round(261.6256 * 0.004)) / 261.6256)
            this._tone(t + s, { freq: 261.6256, gain: 0.015504 * Math.pow(10, -30 * Math.max(0, (s - 0.315) / 0.1) / 20), dur: 0.03, type:"triangle" }).frequency.value = 261.6256;
        } else if (w === "spellbreaker-stun"){          // a stun, lengthened
          /* A LENGTHENED STUN -- "a stun -- hex's own snap, lengthened to
             match (0.4s tail)" (v79 s4). SIZZLE, of 5
             (`spellbreaker_voice_lab.py`). `tickStatus` plays it on each hex
             proc whose stun the window has doubled (0.4 s).

             The school's snap (played as itself), its 2.6 kHz band re-struck
             every ~15 ms (+/-20%) and its ping rung on under it at the snap's
             own proportions, held through the stun and falling 20 dB at its
             end. The snap is there at its own level (register 1.00 over its
             first 30 ms, its peak within 0.5 dB of the snap's); the tail is
             the snap's own sound (register 0.68), its loudest 50 ms -8.4 dB re
             the snap's, unbroken to the stun's end: audible 425 ms, gone by
             430. Heard +18.0 dB over the score in its tail; register at most
             0.67 against the blow, the wall tick, rune-crack, BAR, the cast
             and the runic and twinblade casts. */
          this.play("hex-snap", {});
          this._tone (t, { freq: 2500, gain: 0.07249 * 0.2244, dur: 0.401 * 2.5, type:"triangle" });
          for (let s = 0.015, k = 0; s < 0.401; k++){
            this._burst(t + s, { freq: 2600, q: 1.2, gain: 0.07249 * Math.pow(0.1, Math.pow(s / 0.401, 3)), dur: 0.022, type:"bandpass" });
            s += 0.015 * (1 + 0.2 * Math.sin(k * 2.4));
          }
        } else if (w === "spellbreaker-close"){         // and the hum cuts out
          /* THE HUM CUTS OUT -- "close -- the hum cutting out" (v79 s4). CUT,
             of 4 (`spellbreaker_voice_lab.py`): the cast's hum held 0.2 s, and
             its strikes simply stop -- it dies with the last one's 30 ms ring.

             The cast's hum (262 Hz, register 0.97 with it, -0.0 dB re its held
             level), held and then gone 23 ms after it starts to fall (30 dB),
             with no fade before it (-0.1 dB). Audible 230 ms. `tickUnmake`
             plays it when the window runs out by its clock with both alive. */
          for (let s = 0; s < 0.2 - 1e-9; s += Math.max(1, Math.round(261.6256 * 0.004)) / 261.6256)
            this._tone(t + s, { freq: 261.6256, gain: 0.01506, dur: 0.03, type:"triangle" }).frequency.value = 261.6256;
        } else {                                        // rune-crack'''),

('tickStatus: the stun voice, on a hex proc the Unmaking lengthened (hexStunMul > 1)',
 '''                       STATUS.hex.stunFor * f.hexStunMul);''',
 '''                       STATUS.hex.stunFor * f.hexStunMul);
        /* UNMAKING'S STUN (v79 s4: "a stun -- hex's own snap, lengthened to
           match (0.4s tail)"): on a hex proc whose stun the caster's window
           has lengthened -- read as the two lines above read it, through
           this fighter's `hexStunMul` (2 on the foe while the window is open,
           1 everywhere else) -- once, on the proc's frame. `> 1`, not
           `!== 1`: a body without the field stays silent. Presentation only:
           SFX.play draws nothing, is a no-op headless, and nothing here is
           read back (spellbreaker_voice_lab: fights identical). */
        if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });'''),

('tickUnmake: the close, on a clock close with both alive, before the close line',
 '''      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultUnmake = null; continue; }''',
 '''      /* UNMAKING'S CLOSE (v79 s4: "close -- the hum cutting out"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill, so both are left to the death voice (Tendril's,
         Canopy's, Zenith's, Lightkeeper's and Benediction's rule). Reads
         Z.t, Z.dur and the two alive flags; writes nothing. Presentation
         only; the next line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "spellbreaker-close" });
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultUnmake = null; continue; }'''),

('unmaking picture: fighter fields',
 '''    this.ultUnmake = null;
    this.unmakeTally = null;
    this.hexStunMul = 1;
''',
 '''    this.ultUnmake = null;
    this.unmakeTally = null;
    this.hexStunMul = 1;
    /* UNMAKING'S PICTURE (v79 section 4), and none of it is the window: the
       script unwrites for 0.2s after `ultUnmake` is gone, the motes outlive
       it, and the grey runs on the FOE's stun, not on the window. On the
       FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast takes
       it: open item 25). Driven in `tickPresentation` (`tickUnmaking`);
       nothing in the simulation reads any of it.
         unmkFade  -- 1 while the window is open; eased to 0 over the unwrite
         unmkAge   -- the presentation clock since the cast (the write)
         unmkOut   -- the presentation clock since the close (the unwrite)
         unmkMotes -- the rune motes shed off her blades, in the hall's units
         unmkMoteAcc, unmkMoteN -- the shedding clock and the motes' count
         unmkSeenX -- her `unmakeTally.extra` as last seen (the +2 tag)
       and on EVERY fighter, as the weapon the Unmaking greys:
         unmkGrey  -- what is left of a doubled hex stun's own length
         unmkHC    -- this fighter's `hexClock` as last seen (a drop is a proc)
         unmkMul   -- its `hexStunMul` as last seen (the factor a proc reads)
         unmkStun  -- its `stun` as last seen (the grey counts down with it) */
    this.unmkFade = 0;
    this.unmkAge = 0;
    this.unmkOut = 0;
    this.unmkMotes = [];
    this.unmkMoteAcc = 0;
    this.unmkMoteN = 0;
    this.unmkSeenX = 0;
    this.unmkGrey = 0;
    this.unmkHC = 0;
    this.unmkMul = 1;
    this.unmkStun = 0;
'''),

('unmaking picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickUnmaking(dt);              // UNMAKING'S PICTURE (v79 section 4)
'''),

('unmaking picture: tickUnmaking',
 '''      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : 1;
    }
  }
''',
 '''      f.hexStunMul = foe.ultUnmake ? foe.w.ult.stunMul : 1;
    }
  }

  /* ---------------------------------------------- UNMAKING'S PICTURE ---
     v79 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.6 is the
     script's 0.3s write along both blades at the cast, 0.4 its 0.2s
     unwrite at the close. The window is `ultUnmake`, and not once the caster
     falls or the match ends: `tickUnmake` never runs again once `over` is
     set, so a script standing at the kill would otherwise stand through the
     verdict. Three things, none of them a call from the simulation:
       THE MOTES, shed off both blades while the window is open, left where
         they were shed and drifting out; placed by shellHash on their count.
       THE TAG: a step her `unmakeTally.extra` rose is a step a blow of hers
         landed its second hex, and the hex tag that blow pushed (a hex tag
         pushed since the last call: tags age further down this method, after
         this runs) is relabelled `HEX +2`. Not the killing blow (no second
         hex), not the match's first hex (its panel prints no count), never a
         tag on her own ball.
       THE GREY, on the fighter the Unmaking stuns: a drop in its `hexClock`
         is a hex proc (nothing else resets it), and the proc read the
         `hexStunMul` last seen here (tickUnmake rewrites it later in the
         same step). A proc at more than x1 greys the weapon for that stun's
         own `stunFor x mul`, counted down by the fighter's own stun as it
         counts down: frozen through a hit stop as the stun is, gone when
         the stun is, never past its own length under a longer stun.
     Writes presentation fields and a tag's `val` only, and draws no rng. */
  tickUnmaking(dt){
    const a = this.a, b = this.b;
    if (!a.unmakeTally && !b.unmakeTally) return;             // <- zero burden
    for (const f of [a, b]){
      /* THE GREY, on this fighter's weapon */
      const hc = f.hexClock, st = f.stun;
      if (hc < f.unmkHC && f.unmkMul > 1)
        f.unmkGrey = STATUS.hex.stunFor * f.unmkMul;
      else if (st < f.unmkStun) f.unmkGrey -= f.unmkStun - st;
      f.unmkGrey = Math.min(f.unmkGrey, st);
      if (!(f.unmkGrey > 1e-9)) f.unmkGrey = 0;
      f.unmkHC = hc; f.unmkStun = st; f.unmkMul = f.hexStunMul;
    }
    for (const f of [a, b]){
      const T = f.unmakeTally;
      if (!T) continue;
      /* THE SCRIPT'S CLOCK */
      const Z = (this.over || !f.alive) ? null : f.ultUnmake;
      if (Z){
        if (!(f.unmkFade > 0) || f.unmkOut > 0){ f.unmkAge = 0; f.unmkOut = 0; }  // a cast
        f.unmkFade = 1;
        f.unmkAge += dt;
      } else if (f.unmkFade > 0){
        f.unmkOut += dt;
        f.unmkFade = Math.max(0, 1 - f.unmkOut / 0.4);
      }
      /* THE MOTES */
      const M = f.unmkMotes;
      for (let i = M.length - 1; i >= 0; i--){
        const o = M[i];
        o.t += dt; o.x += o.vx * dt; o.y += o.vy * dt;
        if (o.t >= 1.1) M.splice(i, 1);
      }
      if (Z){
        f.unmkMoteAcc += dt * 8;
        const R = CONFIG.physics.ballR, W = f.w.artW;
        const L = f.w.reach * this.actMods.reach * f.reachMul + 6;
        const S = f.bladeSet || f.w.blades, sd = 7919 + 31 * f.side;
        while (f.unmkMoteAcc >= 1){
          f.unmkMoteAcc -= 1;
          for (const off of S){
            const n = f.unmkMoteN++;
            const q = f.theta + off * TAU, cq = Math.cos(q), sq = Math.sin(q);
            const u = 0.28 + 0.72 * shellHash(sd, n);                 // along the blade
            const h = (shellHash(sd + 1, n) - 0.5) * W * 0.5;         // across it
            const rr = R - 6 + L * u, v = 20 * (0.6 + 0.8 * shellHash(sd + 2, n));
            const w = (shellHash(sd + 3, n) - 0.5) * 20 * 0.8;
            M.push({ x: f.x + cq * rr - sq * h, y: f.y + sq * rr + cq * h,
                     vx: cq * v - sq * w, vy: sq * v + cq * w, t: 0, n });
          }
        }
        if (M.length > 48) M.splice(0, M.length - 48);
      }
      /* THE TAG */
      const dX = T.extra - f.unmkSeenX;
      f.unmkSeenX = T.extra;
      const U = f.w.ult;
      if (dX > 0 && U.hexExtra > 0){
        let k = Math.round(dX / U.hexExtra);
        const val = "+" + ((f.w.onHit && f.w.onHit.hex || 0) + U.hexExtra);
        for (let i = this.tags.length - 1; i >= 0 && k > 0; i--){
          const g = this.tags[i];
          if (g.key !== "hex" || g.first || g.life !== g.max || g.unmk) continue;
          if (g.x === f.x && g.y === f.y) continue;           // a hex ON her
          g.val = val; g.unmk = true; k--;
        }
      }
    }
  }
'''),

('unmaking picture: the floor call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* UNMAKING'S RUNE MOTES (v79 section 4, "rune motes off the blades"),
       shed off both blades and left in the hall. The WORLD pass and under
       both balls, source-over: none of it reaches the bloom (CLAUDE.md
       section 4.1c) and none of it can be painted over a disc (4.1b). The
       script and the grey are drawn with the weapon (drawWeapon). */
    if (__world) this.drawUnmaking(m);
'''),

('unmaking picture: the drawing methods',
 '''  /* ---------------------------------------------------------------- fx --- */
  /* Sparks are drawn as streaks along their own velocity, not as dots. Dots at
''',
 '''  /* ---------------------------------------------- UNMAKING'S PICTURE ---
     v79 section 4, drawn off the fighter's `unmk*` fields -- never `m.ultFx`,
     one slot the opponent's cast takes (open item 25). One method a
     component, so each can be measured alone; nothing here keeps state or
     draws from the rng.
       drawUnmaking   the motes' pass: the world, under both balls
       _unmkMotes     one fighter's rune motes
       _unmkScript    the script on one blade (called from drawWeapon, in the
                      blade's own frame, after the shape)
       _unmkGreyed    whether this weapon is greyed this frame (drawWeapon),
       _unmkGreyFilter, _unmkGreyAlpha   and how (the design's grey)
     UNMAKING_RUNES is the script's alphabet (stroke lists in a unit box;
     its staves stand across the blade). */
  drawUnmaking(m){
    const a = m.a, b = m.b;
    if (!(a.unmkMotes && a.unmkMotes.length) && !(b.unmkMotes && b.unmkMotes.length)) return;  // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]) if (f.unmkMotes && f.unmkMotes.length) this._unmkMotes(c, m, f);
    c.globalAlpha = 1;
    c.restore();
  }
  /* A MOTE IS A RUNE, SMALL: the school's glow over a core halo, turning
     as it drifts, fading in and out over its 0.55s. */
  _unmkMotes(c, m, f){
    const P = f.aff, G = UNMAKING_RUNES;
    for (const o of f.unmkMotes){
      const k = o.t / 1.1, s = 3.4 * (1 - 0.35 * k), A = 0.85 * Math.sin(Math.PI * Math.min(1, k));
      if (!(A > 0.01)) continue;
      const g = G[o.n % G.length], r = o.n * 1.7 + k * 2.2, cr = Math.cos(r), sr = Math.sin(r);
      c.beginPath();
      for (const line of g){
        for (let j = 0; j < line.length; j++){
          const px = o.x + (line[j][0] * cr - line[j][1] * sr) * s * 2;
          const py = o.y + (line[j][0] * sr + line[j][1] * cr) * s * 2;
          j ? c.lineTo(px, py) : c.moveTo(px, py);
        }
      }
      c.globalAlpha = A * 0.55; c.strokeStyle = P.core; c.lineWidth = 2.2; c.stroke();
      c.globalAlpha = A; c.strokeStyle = P.glow; c.lineWidth = 0.9; c.stroke();
    }
  }
  /* THE SCRIPT ON ONE BLADE, in the shape's own frame (x from the hand at 0
     to the point at L). One rune a shard, written hilt to tip over the
     cast's 0.3s behind a bright writing point and unwritten tip to hilt
     over the close's 0.2s. Each rune rides its shard's own drift and cant
     (the same numbers `_twinConjured` hands `_conjure`), so the script is in
     the weapon rather than painted over it; sized to its shard's height off
     the same profile. `core` over a keyline in the blade's silhouette ink:
     the blade's middle IS core, and core on core is nothing. */
  _unmkScript(c, m, f, L, off){
    const W = f.w.artW, gap = L * 0.28, span = L - gap, bw = W * 0.52;
    const x1 = gap + span * 0.16, x2 = L * 0.97;
    const t = SHAPES._t || 0, N = 5, G = UNMAKING_RUNES, P = f.aff;
    const p = clamp(f.unmkAge / 0.6, 0, 1);
    const q = f.unmkOut > 0 ? clamp(f.unmkOut / 0.4, 0, 1) : 0;
    const A0 = c.globalAlpha, j0 = off > 0.25 ? 2 : 0;
    const prof = (x) => {
      if (x <= x1){ const s = (x - gap) / (x1 - gap);
        return [-bw * (0.46 + 0.54 * s), bw * (0.34 + 0.46 * s)]; }
      const s = clamp((x - x1) / (x2 - x1), 0, 1);
      return [-bw * (1 - 0.87 * s), bw * (0.8 - 0.69 * s)];
    };
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (let i = 0; i < N; i++){
      const w = clamp(p * N - i, 0, 1);                       // written
      const v = 1 - clamp(q * N - (N - 1 - i), 0, 1);         // not yet unwritten
      const A = w * v;
      if (!(A > 0.01)) continue;
      const cx = gap + span * (i + 0.435) / N;
      const drift = Math.sin(t * 2.1 + i * 2.3) * W * 0.065;
      const cant = Math.sin(t * 1.6 + i * 1.4) * 0.075;
      const [y0, y1] = prof(cx);
      const h = Math.max(4.5, (y1 - y0) * 0.62) * (1 + 0.35 * (1 - w));
      const g = G[(i * 3 + j0 + 5 * f.side) % G.length];
      c.save();
      c.translate(cx, drift); c.rotate(cant); c.translate(0, (y0 + y1) / 2);
      c.beginPath();
      for (const line of g)
        for (let k = 0; k < line.length; k++)
          k ? c.lineTo(line[k][0] * h, line[k][1] * h) : c.moveTo(line[k][0] * h, line[k][1] * h);
      c.globalAlpha = A0 * A * 0.9; c.strokeStyle = "#040814"; c.lineWidth = h * 0.28; c.stroke();
      c.globalAlpha = A0 * A; c.strokeStyle = P.core; c.lineWidth = h * 0.13; c.stroke();
      c.globalAlpha = A0 * A * 0.8; c.strokeStyle = P.glow; c.lineWidth = h * 0.05; c.stroke();
      c.restore();
    }
    if (p < 1 && q === 0){                                    // the writing point
      const x = gap + span * p, [y0, y1] = prof(Math.min(x, x2)), y = (y0 + y1) / 2;
      const hg = c.createRadialGradient(x, y, 0, x, y, 9);
      hg.addColorStop(0, hexA(P.glow, 0.75)); hg.addColorStop(1, hexA(P.glow, 0));
      c.globalAlpha = A0; c.fillStyle = hg;
      c.beginPath(); c.arc(x, y, 9, 0, TAU); c.fill();
      c.fillStyle = "#FFFFFF";
      c.beginPath(); c.arc(x, y, 2.2, 0, TAU); c.fill();
    }
    c.restore();
  }
  _unmkGreyed(f){ return f.unmkGrey > 0; }
  _unmkGreyFilter(f){ return "grayscale(1)"; }
  _unmkGreyAlpha(f){ return 0.6; }

  /* ---------------------------------------------------------------- fx --- */
  /* Sparks are drawn as streaks along their own velocity, not as dots. Dots at
'''),

("unmaking picture: the script's runes",
 '''function shellHash(a, b){
''',
 '''/* UNMAKING'S SCRIPT (v79 section 4): the runes `_unmkScript` writes along
   Spellbreaker's blades and `_unmkMotes` sheds off them. Stroke lists in a
   unit box, [x, y]: x along the line of script (-0.35..0.35), y down the
   stave (-0.5..0.5), which stands across the blade. Angular staves, the look
   of a carved futhark, eight of them. */
const UNMAKING_RUNES = [
  [[[0, -0.5], [0, 0.5]], [[0, -0.12], [0.3, -0.42]], [[0, 0.14], [0.3, -0.16]]],
  [[[-0.25, 0.5], [-0.25, -0.5], [0.25, -0.2], [0.25, 0.5]]],
  [[[-0.15, -0.5], [-0.15, 0.5]], [[-0.15, -0.26], [0.22, 0], [-0.15, 0.26]]],
  [[[-0.2, 0.5], [-0.2, -0.5], [0.22, -0.26], [-0.2, 0], [0.24, 0.5]]],
  [[[0.22, -0.42], [-0.2, 0], [0.22, 0.42]]],
  [[[-0.3, -0.45], [0.3, 0.45]], [[0.3, -0.45], [-0.3, 0.45]]],
  [[[0, 0.5], [0, -0.5]], [[0, -0.02], [-0.3, -0.4]], [[0, -0.02], [0.3, -0.4]]],
  [[[0, 0.5], [0, -0.5]], [[-0.28, -0.18], [0, -0.5], [0.28, -0.18]]],
];

function shellHash(a, b){
'''),

('unmaking picture: the grey (drawWeapon, the whole weapon)',
 '''  drawWeapon(m, f){
''',
 '''  drawWeapon(m, f){
    /* UNMAKING'S GREY (v79 section 4): "the foe's weapon greys out
       (desaturated, alpha 0.6) for the stun's length, so a longer stop is a
       longer grey". While a doubled hex stun runs (`unmkGrey`, set and
       counted down in `tickUnmaking`) the WHOLE weapon is drawn through the
       canvas's own grayscale -- every school, every type, the glow sprite
       and the lit blit alike (most weapons reach this canvas as one blit
       from `litWeapon`'s scratch, so the filter touches a handful of ops).
       Re-entered once, with the filter set, and back out. */
    if (!this._unmkGreying && this._unmkGreyed(f)){
      const c0 = this.ctx;
      c0.save();
      c0.filter = this._unmkGreyFilter(f);
      this._unmkGreying = true;
      try { this.drawWeapon(m, f); }
      finally { this._unmkGreying = false; c0.restore(); }
      return;
    }
'''),

("unmaking picture: the grey's alpha (drawWeapon)",
 '''
    const dim = f.stun > 0 ? 0.42 : 1;
''',
 '''
    /* ... and the greyed weapon is at the design's 0.6, where a plain stun
       dims it to 0.42 in its colours: the Unmaking's stop is the grey one. */
    const dim = f.stun > 0 ? (this._unmkGreyed(f) ? this._unmkGreyAlpha(f) : 0.42) : 1;
'''),

('unmaking picture: the script on each blade (drawWeapon)',
 '''      if (f.ultDraw){
''',
 '''      /* UNMAKING'S SCRIPT (v79 section 4), on the blade just drawn, in its
         own frame: the runes the cast writes along both blades and the close
         unwrites. `unmkFade` is 0 on every other relic, so this is one
         comparison on a field nothing else writes. */
      if (f.unmkFade > 0) this._unmkScript(c, m, f, reach + 6, off);
      if (f.ultDraw){
'''),

("unmaking picture: the bolt's set-piece retired",
 '''    /* ---- Unmaking: struck by runes, then taken apart */
    else if (u.w === "spellbreaker"){
      const strike = clamp(u.t / 0.10, 0, 1);
      const fade   = 1 - clamp((u.t - 0.45) / 0.85, 0, 1);
      if (u.t < 0.42){
        const flick = 0.55 + Math.random() * 0.45;
        c.globalAlpha = flick * (1 - clamp((u.t - 0.16) / 0.26, 0, 1));
        c.strokeStyle = "#BCDDFF"; c.lineWidth = 7;
        c.shadowColor = "#4A9EFF"; c.shadowBlur = 26;
        this._jag(c, u.x, u.y, tgt.x, tgt.y, 12, 30, 7 + Math.floor(u.t * 40), strike);
        c.strokeStyle = "#FFFFFF"; c.lineWidth = 2.4;
        this._jag(c, u.x, u.y, tgt.x, tgt.y, 12, 30, 7 + Math.floor(u.t * 40), strike);
        c.shadowBlur = 0;
        for (let i = 0; i < 4; i++){         // glyphs igniting along the bolt
          const t2 = (i + 1) / 5;
          if (t2 > strike) break;
          this._glyph(c, lerp(u.x, tgt.x, t2), lerp(u.y, tgt.y, t2),
                      9 + i * 2, u.t * 3 + i, "#BCDDFF", flick * 0.9);
        }
      }
      /* the cage: rings close on them, then come apart — the "unmaking" */
      if (u.hit && u.t > 0.10){
        const p = clamp((u.t - 0.10) / 0.34, 0, 1);
        const brk = clamp((u.t - 0.48) / 0.5, 0, 1);
        const R = CONFIG.physics.ballR;
        for (let i = 0; i < 3; i++){
          const rr = (R + 46) * (1 - p * 0.62) + i * 9;
          const segs = 6;
          for (let j = 0; j < segs; j++){
            const a0 = j * TAU / segs + u.t * (i % 2 ? -1.8 : 1.8);
            const push = brk * (26 + i * 14);
            const mid = a0 + TAU / segs / 2;
            c.save();
            c.globalAlpha = fade * (1 - brk);
            c.translate(Math.cos(mid) * push, Math.sin(mid) * push);
            c.strokeStyle = i === 1 ? "#FFFFFF" : "#4A9EFF";
            c.lineWidth = 3.4 - i * 0.7;
            c.shadowColor = "#4A9EFF"; c.shadowBlur = 14;
            c.beginPath();
            c.arc(tgt.x, tgt.y, rr, a0, a0 + TAU / segs * 0.66);
            c.stroke();
            c.restore();
          }
        }
        this._glyph(c, tgt.x, tgt.y, 20 * (1 - brk), -u.t * 2.4, "#BCDDFF",
                    fade * (1 - brk) * 0.9);
      }
    }
''',
 '''    /* ---- Unmaking's bolt (the jagged bolt with its glyphs, and the cage of
       rings that closed on the target and came apart) was the BOLT's picture;
       retired with it (v79 section 4, v111 stage 6). The Unmaking is drawn
       off the fighter: the script on her blades, the rune motes, the foe's
       greyed weapon (`drawWeapon`, `drawUnmaking`). The cast's record carries
       the CAST only, and nothing draws from it. */
'''),

("unmaking picture: the banner's seat",
 '''spellbreaker:1, ''',
 ''''''),

("unmaking picture: the cast record's life",
 ''' spellbreaker: 1.4,''',
 ''''''),

]

# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `unmk*` / `_unmk*` fields; the canvas (`c`, `c0`,
# bound only to the renderer's own context or taken as a method's first
# parameter); in tickUnmaking alone, a mote's t, x and y (the picture's own
# objects, in `unmkMotes`) and a tag's `val` and `unmk` (the relabel); in the
# Sfx arms alone, the synth's own nodes. Everything else is the simulation's.
S6_NAMES = ("tickUnmaking", "drawUnmaking", "_unmkMotes", "_unmkScript", "_unmkGreyed", "_unmkGreyFilter",
            "_unmkGreyAlpha", "_unmkGreying", "UNMAKING_RUNES", "unmkFade", "unmkAge", "unmkOut", "unmkMotes",
            "unmkMoteAcc", "unmkMoteN", "unmkSeenX", "unmkGrey", "unmkHC", "unmkMul", "unmkStun", "unmk",
            "spellbreaker-stun", "spellbreaker-close")
S6_SFX_ROW = "Sfx: Spellbreaker's cast"
S6_TICK_ROW = "unmaking picture: tickUnmaking"
# THE TWO THINGS ON THE SIM PATH, whole (reading 17): each row's added code,
# comments stripped, line for line.
S6_SIM_LINES = {
    "tickStatus: the stun voice": ['if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });'],
    "tickUnmake: the close": ['if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "spellbreaker-close" });'],
}
# THE SHARED MODULE TABLES STAGE 6 MAY READ, by exact path, and no other
# reference to one (no alias, no write: a table written holds for every later
# match on the page).
S6_TABLE_READS = ("CONFIG.physics.ballR", "CONFIG.arena.w", "CONFIG.arena.h", "STATUS.hex.stunFor", "SHAPES._t")
RUNE_CRACK = "        } else {                                        // rune-crack"
S6_ARMS = ('} else if (w === "spellbreaker"){', '} else if (w === "spellbreaker-stun"){',
           '} else if (w === "spellbreaker-close"){')


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 19)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_added(old: str, new: str) -> str:
    """A stage-6 row's ADDED code, comments out: its new text less the anchor it
    re-emits (a replace row adds all of its new text)."""
    return strip_comments(new.replace(old, "", 1) if old in new else new)


def s6_bound_once(ins: str, name: str, expr: str) -> bool:
    """`name` is bound exactly once in the insert, as `const name = expr;`, and
    assigned nowhere else."""
    b = re.findall(r"\bconst " + re.escape(name) + r" = " + re.escape(expr) + ";", ins)
    decls = re.findall(r"\b(?:const|let|var)\s+" + re.escape(name) + r"\b|[,(]\s*" + re.escape(name)
                       + r"\s*=(?!=)|(?<![\w.$])" + re.escape(name) + r"\s*=(?!=)", ins)
    return len(b) == 1 and len(decls) == 1


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, stuns, beats or knocks, never writes
    the shared weapon row or a module table (it reads five of their numbers by
    exact path), writes only what the table above names and mutates only its
    own motes. Its lines on the sim path are the two voice rows, whole, each in
    its own row; `SFX` only there; the synth's nodes and `play` only in the Sfx
    arms; the tags only in tickUnmaking. The probe's [7]-[8] and engine_ab are
    the dynamic proof. Run on every stage: it reads the table."""
    for label, old, new in S6:
        ins = s6_added(old, new)
        tick = label.startswith(S6_TICK_ROW)
        if re.search(r"\brng\b", ins) or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|breakSpin|"
                     r"takeHitstun|tickUnmake|tickStatus|tickWeapon|tickHits|spawnShot|note|checkEnd|"
                     r"statusTag|step)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        WRITE = r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)"
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*" + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        for mt in re.finditer(r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES)\b(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*", ins):
            if mt.group(0) not in S6_TABLE_READS or re.match(WRITE, ins[mt.end():]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reaches a shared "
                                 f"module table other than by the five reads it may make: {mt.group(0)!r}")
        if re.search(r"\b(beat|hurt|knock|shake|hitStop|pin|stun|stunDR|hexClock|hexStunMul|ultUnmake|"
                     r"unmakeTally|reachMul|charge|burden|status)\b" + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' hurts, knocks, "
                             "stops, stuns or writes the window or a status")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its voice alone:\n{ins}")
        elif re.search(r"\bSFX\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the stun and the close")
        if re.search(r"\b_tone\s*\(|\b_burst\s*\(|\.play\s*\(|\bfrequency\b", ins) and not sim \
                and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if re.search(r"\btags\b|\bstatusTag\b|\.val\b|\.unmk\b", ins) and not tick:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' touches the "
                             "tags outside tickUnmaking")
        if re.search(r"\bdelete\s|Object\.(assign|defineProperty|defineProperties|setPrototypeOf)\s*\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes or "
                             "redefines a property")
        # THE CANVAS: `c` and `c0` only as the renderer's own context, or a method's first parameter
        for cn in ("c", "c0"):
            for mb in re.finditer(r"\b(?:const|let|var)\s+" + cn + r"\s*=\s*([^,;\n]+)", ins):
                if mb.group(1).strip() != "this.ctx":
                    raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' binds "
                                     f"`{cn}` to {mb.group(1).strip()!r}, not the renderer's context")
            if re.search(r"(?<![\w.$])" + cn + r"\s*=(?!=)", ins.replace("const " + cn + " =", "")):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reassigns `{cn}`")
        for mw in re.finditer(r"([\w\]\)]+)\s*\.\s*(\w+)" + WRITE, ins):
            obj, prop = mw.group(1), mw.group(2)
            ok = (prop.startswith(("unmk", "_unmk")) or obj in ("c", "c0")
                  or (tick and obj == "o" and prop in ("t", "x", "y") and s6_bound_once(ins, "o", "M[i]")
                      and s6_bound_once(ins, "M", "f.unmkMotes"))
                  or (tick and obj == "g" and prop in ("val", "unmk") and s6_bound_once(ins, "g", "this.tags[i]"))
                  or (label.startswith(S6_SFX_ROW) and (obj, prop) == ("frequency", "value")))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes {obj}.{prop}")
        for mw in re.finditer(r"([\w\]\)]+)\s*\.\s*(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\s*\(", ins):
            if not (tick and mw.group(1) == "M" and s6_bound_once(ins, "M", "f.unmkMotes")):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' mutates {mw.group(1)}")
        # an index write (a destructuring `const [a, b] = ...` is a declaration, not one)
        if re.search(r"[\w\]\)]\s*\[[^\]]*\]" + WRITE, re.sub(r"\b(?:const|let|var)\s*\[[^\]]*\]", "D", ins)):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes through an index")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched; the shared
    rune-crack fallback kept once and after Spellbreaker's three arms; the
    bolt's art gone; the two voice lines each added once, each where it
    belongs; every arm, call, pass and method wired exactly once; and the only
    Math.random that goes is the retired bolt art's."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 19)")
    if s.count(RUNE_CRACK) != 1 or any(not 0 <= s.find(a) < s.find(RUNE_CRACK) for a in S6_ARMS):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Spellbreaker's arms")
    if ('u.w === "spellbreaker"' in out_code or "spellbreaker: 1.4" in out_code
            or re.search(r"onTarget\s*=\s*\{[^}]*\bspellbreaker\s*:", out_code)):
        raise SystemExit("REFUSING TO WRITE -- the bolt's art is still drawn or seated "
                         "(its drawUltOver branch, its life entry or its banner seat)")
    for need in ("this.tickUnmaking(dt);", "if (__world) this.drawUnmaking(m);", "  tickUnmaking(dt){",
                 "  drawUnmaking(m){", "const UNMAKING_RUNES = [",
                 "if (f.unmkFade > 0) this._unmkScript(c, m, f, reach + 6, off);",
                 "const dim = f.stun > 0 ? (this._unmkGreyed(f) ? this._unmkGreyAlpha(f) : 0.42) : 1;",
                 "if (!this._unmkGreying && this._unmkGreyed(f)){") + S6_ARMS:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        for ln in v:
            if out_code.count(ln) != code.count(ln) + 1:
                raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    if len(re.findall(r'this\.breakSpin\(f, "the hex takes the wind out of it",\s*STATUS\.hex\.stunFor \* '
                      r'f\.hexStunMul\);\s*if \(f\.hexStunMul > 1\) SFX\.play\("ult", \{ w: "spellbreaker-stun" '
                      r'\}\);', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- the stun voice does not follow the hex proc's own "
                         "breakSpin in tickStatus")
    tu = out_code[out_code.find("  tickUnmake(dt){"):]
    tu = tu[:tu.find("\n  }\n")]
    if len(re.findall(r'if \(Z\.t >= Z\.dur && f\.alive && foe\.alive\) SFX\.play\("ult", \{ w: '
                      r'"spellbreaker-close" \}\);\s*if \(Z\.t >= Z\.dur \|\| !f\.alive \|\| !foe\.alive\)\{ '
                      r'f\.ultUnmake = null; continue; \}', tu)) != 1:
        raise SystemExit("REFUSING TO WRITE -- the close voice is not just before the window's own "
                         "close line in tickUnmake")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickUnmaking(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickUnmaking does not follow tickNovaFx in "
                         "tickPresentation")
    if out_code.count('SFX.play("ult", { w: f.w.id });') != code.count('SFX.play("ult", { w: f.w.id });'):
        raise SystemExit("REFUSING TO WRITE -- fireUlt's cast voice moved")
    gone = sum(strip_comments(old).count("Math.random") for _l, old, new in S6 if old not in new)
    if gone != 1 or out_code.count("Math.random") != code.count("Math.random") - gone:
        raise SystemExit("REFUSING TO WRITE -- stage 6 moves a Math.random other than the retired "
                         "bolt art's one")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes its own "
          "fields, its motes and the relabel only; the stun and close voices its two lines on the sim "
          "path, each where it belongs); the inlined fx.js untouched; the rune-crack fallback kept; the "
          "bolt's art gone (its one Math.random with it); every arm, call, pass and method once")


STAGE_OUT = {"1": "sc-spellbreaker-stub", "2": "sc-spellbreaker-stun", "3": "sc-spellbreaker-unmaking",
             "5": "sc-spellbreaker-b7.5", "5 --alt-row": "sc-spellbreaker-b8.3",
             "5 --alt50": "sc-spellbreaker-b7.7", "6": "sc-spellbreaker-b7.5-fx"}
NAMES = ("ultUnmake", "unmakeTally", "tickUnmake", "hexStunMul")


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


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


def ult_rows(code: str) -> list:
    """Every WEAPONS row's ult block, (id, block)."""
    out = []
    for m in re.finditer(r'\{ id:"([a-z]+)", name:"', code):
        row = code[m.start():code.find("blurb:", m.start())]
        j = row.find("ult:{")
        if j >= 0:
            out.append((m.group(1), row[j:row.find("},", j) + 2]))
    return out


def s5_edits(blade: str) -> list:
    return [
        ("the blade: the measured point nearest the shipped rate",
         ROW_HEAD + f"{SHIPPED_DMG},",
         ROW_HEAD + f"{blade},"),
    ]


# THE CARRY'S BLADE AS A MODULE-LEVEL TABLE, so `tools/chain_audit.py` (which
# reads module-level `(label, old, new)` tables, never a function's return)
# watches the blade like every other insert (Aureole's v110 review): a tip that
# puts Spellbreaker back at 8.81 reads "S5:... LOST". Rick's two other choices
# are deliberately NOT tables: the carry is 7.5, and a table for 8.30 or 7.7
# would read as LOST on the final link.
S5 = s5_edits(BLADE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--alt50", action="store_true",
                    help="stage 5 only: write Rick's other choice, the 50%% crossing (blade "
                         f"{ALT50_BLADE}); NOT the carry")
    ap.add_argument("--alt-row", action="store_true",
                    help="stage 5 only: write Rick's other choice, the twinblade row's floor "
                         f"(blade {ALTROW_BLADE}); NOT the carry")
    A = ap.parse_args()
    if (A.alt50 or A.alt_row) and A.stage != "5":
        raise SystemExit("--alt50 / --alt-row are stage 5's")
    if A.alt50 and A.alt_row:
        raise SystemExit("one blade a link: --alt50 or --alt-row")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-spellbreaker"):
        raise SystemExit(f"refusing {out_p.name}: this builder's links are sc-spellbreaker*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: 02-chain already has a link of that name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    S5_BLADE = ALT50_BLADE if A.alt50 else ALTROW_BLADE if A.alt_row else BLADE
    if A.stage == "5" and S5_BLADE is None:
        raise SystemExit("stage 5: the blade is not measured yet (v111 §4)")

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nSPELLBREAKER / UNMAKING (REDESIGN) -- stage {A.stage}"
          f"{' --alt50' if A.alt50 else ' --alt-row' if A.alt_row else ''}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The relic this builder redesigns, with its shipped
    # body; the engine's gates the Unmaking pays through; the window clock.
    row = relic_row(code, RELIC)
    for need, why in (('aff:"runic", shape:"twinblade"', "Spellbreaker is not the runic twinblade"),
                      ('blades:[0,0.5], reach:62, width:8, artW:30,', "Spellbreaker's blade set has moved"),
                      ('spin:5.7, mode:"spin", mass:1.1,', "Spellbreaker's spin or mass has moved"),
                      ("onHit:{ hex:1 }", "Spellbreaker does not carry the runic channel, hex 1")):
        if need not in row:
            raise SystemExit(f"wrong base: {why}")
    for need, why in (("apply(key, n, src){", "no Fighter.apply(key, n, src)"),
                      ("get alive(){ return this.hp > 0; }", "no Fighter.alive"),
                      ("stacks(", "no Fighter.stacks"),
                      ("fireUlt(f, foe){", "no fireUlt"),
                      ("breakSpin(f, reason, trueFor){", "no breakSpin(f, reason, trueFor)")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'\n  hex:\s+\{ name:"Hex",\s+maxStacks:5, dur:2\.6, stunEvery:1\.15, stunFor:0\.20,', code):
        raise SystemExit("wrong base: STATUS.hex is not the one priced (5 stacks, 2.6s, every 1.15, 0.20s)")
    # THE ONHIT LOOP THE SECOND HEX SITS BESIDE: every blow's statuses go
    # through apply() in resolveHit.
    rh = code[code.find("  resolveHit(self, foe, hx, hy, seg, mul, over){"):]
    rh = rh[:rh.find("\n  }\n")]
    if not re.search(r"for \(const \[k, n\] of Object\.entries\(\s*\(over && over\.onHit\) \|\| self\.w\.onHit \|\| \{\}\)\)\{"
                     r"[\s\S]*?foe\.apply\(k, n\);", rh):
        raise SystemExit("wrong base: resolveHit's onHit loop has moved")
    if "self.hits++;" not in rh:
        raise SystemExit("wrong base: resolveHit does not count the blow")
    # THE WINDOW CLOCK: a hit stop returns from step() before the window tickers.
    st = code[code.find("  step(dt){"):]
    hs = st.find("if (this.hitStop > 0){")
    tt = st.find("this.tickTendril(dt);")
    if tt < 0:
        raise SystemExit("wrong base: no `this.tickTendril(dt);` in step() -- the Unmaking's ticker "
                         "goes after Tendril's (v68), so this is not the Tendril lineage")
    if hs < 0 or not hs < st.find("return;", hs) < tt:
        raise SystemExit("wrong base: the window tickers do not stop in a hit stop")
    if re.search(r'kind\s*===?\s*"bolt"', code):
        raise SystemExit("wrong base: code keys on kind \"bolt\" -- the bolt has a branch to retire")
    if A.stage == "1":
        for name in NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")
        if '"unmake"' in code:
            raise SystemExit("the kind \"unmake\" is already in the base")
        if s0.count(SHIPPED_ULT) != 1:
            raise SystemExit("wrong base: Spellbreaker does not carry the shipped Unmaking")
        if f"dmg:{SHIPPED_DMG}," not in row:
            raise SystemExit("wrong base: Spellbreaker is not at its shipped blade")
        bolts = [rid for rid, blk in ult_rows(code) if 'kind:"bolt"' in blk]
        if bolts != [RELIC]:
            raise SystemExit(f"wrong base: the bolt ultimates are {bolts}, not Spellbreaker's alone")
        if s0.count(HEX_PROC) != 1:
            raise SystemExit("wrong base: tickStatus's hex proc is not the one this builder reads")
    print("  base  Spellbreaker's shipped body (runic twinblade, hex 1); apply / stacks / "
          "STATUS.hex as priced and its proc; resolveHit's onHit loop; the window tickers "
          "stop in a hit stop; no code keys on the bolt")

    blade = SHIPPED_DMG
    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"unmake"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if not free_name("tickUnmake", code) or "charge:1e9" not in row:
                raise SystemExit("stage 2 goes on stage 1, once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if free_name("tickUnmake", code) or "hexExtra:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["hexExtra"])
        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: the second hex on, the blade BLADE
            # names (never Rick's two other links), the Unmaking's ticker, none
            # of stage 6's names in the source yet (on identifier boundaries),
            # and what the picture and the voice read there.
            if (f'hexExtra:{ULT["hexExtra"]},' not in row or f"dmg:{BLADE}," not in row
                    or free_name("tickUnmake", code)):
                raise SystemExit("stage 6 goes on stage 5 (the second hex on, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_ARMS[0] in code:
                raise SystemExit("Spellbreaker's cast voice is already in this source -- stage 6 goes on once")
            for need, why in (("function shellHash(", "no shellHash (the motes' hash, never the RNG)"),
                              ("function hexA(", "no hexA (the writing point's glow)"),
                              ("const clamp = ", "no clamp"),
                              ("  statusTag(x, y, key, first, val){", "no statusTag (the tag the relabel reads)"),
                              ("life: first ? 2.5 : 0.9, max: first ? 2.5 : 0.9,", "a tag's life / max have moved"),
                              ("  drawWeapon(m, f){", "no drawWeapon(m, f)"),
                              ("if (__world) this.drawTree(m);", "no world-pass drawTree call to follow"),
                              ("  tickPresentation(dt){\n    this.tickNovaFx(dt);", "tickPresentation does not open "
                               "with tickNovaFx"),
                              ('SFX.play("ult", { w: f.w.id });', "fireUlt no longer voices the cast by id"),
                              ('else if (kind === "hex-snap"){', "no hex-snap voice for the stun to play"),
                              ("this.bladeSet = null;", "no bladeSet (the motes' blades)")):
                if need not in code:
                    raise SystemExit(f"wrong base for stage 6: {why}")
            # THE GREY'S PROC TEST (reading 14): the hex clock is written by the
            # constructor and by tickStatus's cadence alone (+= and the reset).
            if len(re.findall(r"\bhexClock\s*(?:=(?!=)|\+=|-=)", code)) != 3:
                raise SystemExit("wrong base for stage 6: something else writes hexClock -- the grey's "
                                 "proc test (a drop in the hex clock) no longer means a proc")
            blade = BLADE
            edits, want = S6, ult_block(ULT["charge"], ULT["hexExtra"])
        else:
            if f'hexExtra:{ULT["hexExtra"]},' not in row or f"dmg:{SHIPPED_DMG}," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            blade = S5_BLADE
            edits = S5 if blade == BLADE else s5_edits(blade)
            want = ult_block(ULT["charge"], ULT["hexExtra"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Spellbreaker's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:104]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if f"dmg:{blade}," not in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    if A.stage != "6" and out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    if out_code.count("Math.random") > code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    s6_static_checks()
    for label, old, new in S1 + S2 + S3 + S5 + s5_edits(ALTROW_BLADE) + s5_edits(ALT50_BLADE):
        # THE ADDED CODE: a row is judged on the lines it adds, comments out, so
        # a line it re-emits unchanged (an anchor, the hex proc's breakSpin
        # call) is not counted as its own.
        kept = set(strip_comments(old).splitlines())
        ins = "\n".join(ln for ln in strip_comments(new).splitlines() if ln not in kept)
        # THE TWO LINES THE DESIGN ASKS FOR THAT WOULD TRIP THE SCAN, allowed BY EXACT
        # TEXT and nowhere else: the hex proc's own stun, rewritten with the factor
        # (v79 §1 "every stun a hex lands ... lasts twice as long"), and the second hex
        # (§4 "+1 hex in resolveHit"). A copy of either line anywhere else, or any
        # other write to a stun or a status, refuses.
        ALLOWED = {
            "a hex stun lasts the fighter's own hexStunMul times as long":
                "        f.stun = Math.max(f.stun, STATUS.hex.stunFor * f.hexStunMul);",
            "every blow in the window hexes `hexExtra` more":
                '        foe.apply("hex", U.hexExtra, self === this.a ? "a" : "b");',
        }
        ok_line = ALLOWED.get(label)
        if ok_line is not None:
            if ins.splitlines().count(ok_line) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' does not carry its "
                                 "one allowed line exactly once")
            ins = "\n".join(ln for ln in ins.splitlines() if ln != ok_line)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        WRITE = r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)"
        if re.search(r"\bw\.(spin|reach|dmg|blades|mass)" + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        # THE SHARED MODULE TABLES (Lightkeeper's third review): a write to STATUS, CONFIG,
        # AFFINITIES, WEAPONS or SHAPES holds for every later match on the page -- the lab's
        # global stunFor was exactly that. By name, or through a local alias of one.
        TABLES = r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES)\b"
        if (re.search(TABLES + r"(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*" + WRITE, ins)
                or re.search(r"\b(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*" + TABLES, ins)):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes (or aliases) a "
                             "shared module table")
        if re.search(r"\.(hurt|heal|resolveHit|shatter|knock|beat|spawnShot|breakSpin|takeHitstun)\(", ins) \
                or re.search(r"\b(hitStop|pin|pinFree|vx|vy|x|y|theta|hp|shield|shieldMax)" + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' hurts, moves, "
                             "stops or files a beat (v79: a stun length and a hex, nothing else)")
        # A STUN, A STATUS OR A WEAPON'S CADENCE OR REACH (v111's review): the Unmaking is a
        # stun LENGTH on the hex proc and one apply() -- no stun of its own (`stun`,
        # `stunDR`), no status written by hand, no hex cadence (`hexClock`), no shrink
        # (`reachMul`: the lab's arms B/C, which §3 passed over), no charge or burden. The
        # two lines the design asks for are allowed above by exact text; any other write,
        # alias or apply() refuses.
        if (re.search(r"\b(stun|stunDR|hexClock|reachMul|charge|burden)" + WRITE, ins)
                or re.search(r"\.status\b(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*" + WRITE, ins)
                or re.search(r"\b(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*[^;\n]*\.status\b", ins)
                or re.search(r"\bdelete\s+[^;\n]*\.status\b", ins)
                or re.search(r"Object\.assign\s*\(\s*[^,\n]*\.status\b", ins)
                or re.search(r"\.apply\s*\(", ins)):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stuns, writes a status, "
                             "moves a weapon's hex clock, reach, charge or burden, or applies a status "
                             "(v79: a stun length and one hex, nothing else)")
    if len(re.findall(r'kind:"unmake"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one Unmaking ultimate")
    if 'kind:"bolt"' in out_code:
        raise SystemExit("REFUSING TO WRITE -- the bolt is still here")
    if A.stage != "1":
        # the simulation's reads of the hex stun; the picture's one read (tickUnmaking's
        # grey, `STATUS.hex.stunFor * f.unmkMul`, the factor the proc read) is not the sim's
        sim_code = out_code
        i = sim_code.find("  tickUnmaking(dt){")
        if i >= 0:
            j = sim_code.find("\n  }\n", i)
            if sim_code[i:j].count("STATUS.hex.stunFor") != 1 or "STATUS.hex.stunFor * f.unmkMul" not in sim_code[i:j]:
                raise SystemExit("REFUSING TO WRITE -- the picture reads the hex stun other than as its grey")
            sim_code = sim_code[:i] + sim_code[j:]
        if (sim_code.count("STATUS.hex.stunFor * f.hexStunMul") != 2
                or re.search(r"STATUS\.hex\.stunFor(?!\s*\*\s*f\.hexStunMul)", sim_code)):
            raise SystemExit("REFUSING TO WRITE -- a hex stun is read without the fighter's hexStunMul")
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one Unmaking ultimate, Spellbreaker's; the bolt out; no insert draws the RNG, "
          f"writes the shared weapon or a module table, hurts, moves, stops, files a beat, stuns, "
          f"writes a status, a hex clock, a reach, a charge or a burden beyond the design's two lines; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
