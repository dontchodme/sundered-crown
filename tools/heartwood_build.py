#!/usr/bin/env python
"""HEARTWOOD / ROOTFAST, REDESIGNED -- every blow roots the foe where it stands. v112.

Built from `06-docs/v85/heartwood-rootfast-redesign-v85.md` (Cowork,
2026-09-26), its §5 build brief and its runs (`06-docs/v85/runs/rootfast_*`,
`tools/overlays/rootfast.js`), which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. A REDESIGN: the relic
ships in the base; its ultimate, the one-shot freeze, is replaced.

    stage 1   the new ultimate stubbed (1e9); the freeze out of the row
                                          <tip> -> sc-heartwood-stub.html     (= arm A)
    stage 2   the root on every blow, no extra entangle; charge on the game's clock
                                          -> sc-heartwood-root.html     (arm B at 1.0; brief stage 1)
    stage 3   the entangle, extraEnt 0 -> 1
                                          -> sc-heartwood-rootfast.html (arm C at 1.0; brief stage 2)
    stage 5   the blade (brief stage 3), 12.65 -> 11: the measured point whose
              win rate BOTH SIDES is nearest 50% -- RICK'S RULING, 2026-09-29,
              after the design was written: "you pick the blades. do whatevers
              best for balance." It replaces the design's own target ("Rick's
              target", §6.2: leave 12.65, or 11.5-12 for 50), which v112 §4
              measures beside it.     -> sc-heartwood-b11.html      (the final ruleset)
    stage 6   the picture and the voice (the brief's stage 4), on stage 5's link,
              presentation only (v112 §6)   -> sc-heartwood-b11-fx.html   THE FINAL LINK

THE CARRY is stages 1, 2, 3, 5 and 6. Stage 6's link is the final; stage 5's
is the last that moves a fight (stage 6 moves none: engine_ab, v112 §6a).

§1: "For a duration every blow the sword lands roots the enemy where it
stands -- ball and weapon -- for a second, and entangles it. The knock that
would have thrown it across the hall has nothing to throw; the next swing
finds it still there."

Declared (§4, the lab `overlays/rootfast.js` at the taken point `--P rootFor=1.0`):
  THE WINDOW  `dur` 8 on the window tickers' clock (`tickRootfast`).
  THE ROOT    on every blow Heartwood lands inside the window: pin `rootFor`
              (1.0) on the foe -- Grasp's write: `pinV` stored unless a longer
              hold already stands, `pin` / `pinMax` max'd, `pinFree` NOT touched,
              so `tickStasis` locks the weapon too.
  THE ORDER   (§4: "Declare that order in the build") resolveHit's knock is
              applied FIRST and the pin freezes it: the root is written inside
              `resolveHit` on the line after the ordinary knock, so `pinV` is the
              vector the ball was hit with; `move()` resumes it a second later
              and zeroes an upward resume (the engine's Stasis clamp).
  THE FEED    `foe.apply("entangle", extraEnt)` on top of the channel's 2 --
              stage 3.
  No damage change: the blow is the sword's own; the root hurts nobody, files
  no beat, sets no hit stop and moves nothing.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CHARGE IS THE DESIGN'S 15 ON THE GAME'S CLOCK: 13 (v112 §0, flagged
     for Rick). §4 says "Charge 15 (the relic's)", and the prose is explicit,
     so it is the design's charge; Rick's batch ruling reads every design's
     charge on the lab's step clock, which counts hit-stop freezes, and
     converts it per fighter ("use the game's equivalent"). Measured for this
     fighter on the lab's arm C at 1.0 and charge 15 (the census, v112 §0):
     15 x (1 - the frozen share) is 13.0. THE LAB NEVER RAN 15: every
     rootfast_* run cast every 16 lab seconds (`"charge": 16.0`, the harness
     default), which converts to 14 (CHARGE_ALT_LAB16), and the shipped
     relic's own engine charge is 15 (CHARGE_ALT_SHIPPED). v112 §2 adds the
     lab at charge 15 so the built stages read against a like-for-like arm,
     and v112 §4 prices 14 and 15 at the shipped blade, one number away.
  2. THE WINDOW IS 8s (§4 "window 8"; the lab's dur 8).
  3. THE ROOT'S LENGTH IS 1.0 (§3 "root 1.0 (taken)", §4 "pin 1.0", §5's
     stage 0 `--P rootFor=1.0`). The lab's `rootFor` DEFAULTS TO 0.45, the
     rejected first pricing (arms B and C of rootfast_base); every lab arm
     this build reads passes 1.0. §6.3 (1.0 against 0.8) is Rick's feel call.
  4. THE ORDER is the design's (above), and it is the lab's: the lab pinned
     after the whole step, after the knock, and nothing between the knock and
     the step's end reads or writes the rooted foe's velocity or pin.
  5. GRASP'S WRITE, the lab's `H.pin` to the letter: `pinV` captured iff the
     hold standing is not longer than `rootFor`; `pinFree` untouched.
  6. THE TARGET IS THE OPPONENT (the lab's `foe`): a blow landed on one of
     Twinshade's shades roots Twinshade -- the lab counted every `me.hits`,
     and Corollary's echo made the same reading. A killing blow roots
     nobody (the lab's `if (foe.alive)`).
  7. THE ENTANGLE goes on after the channel's own 2 (the lab applied it after
     the step; entangle's cap and clock make the two orders the same stacks).
     Its SOURCE IS A SIDE LETTER (Rick's ruling 4; the lab passed the
     Fighter; entangle has no reader of its source).
  8. NOTHING ELSE: no damage change, no beat, no hit stop, no move, no stun
     write (`tickStasis` writes the weapon lock from the pin, as for every
     hold). `f.hits` and `f.dealt` stay the sword's.
  9. THE WINDOW CLOSES on its clock or EITHER death (the lab's).
 10. NO CAST WAITS. The design asks none; the charge is unfrozen time and the
     window 8 on the same clock, so a cast cannot find its window open (the
     probe asserts it).
 11. THE CARD is the design's own, 72 characters.
 12. THE FREEZE IS OUT (brief stage 1 "freeze out"): Heartwood's row loses
     radius 230, dmg 9, apply entangle 3 and freeze 1.3. `kind:"freeze"` has no
     code of its own (no `u.kind === "freeze"` anywhere): the one-shot was
     fireUlt's generic tail (`u.freeze`, `u.dmg`, `u.apply`, `u.radius`), and
     that tail STAYS -- Thornwake's Bramblesnare still casts through it on this
     base (it is being redesigned too, and either may be carried first). So
     nothing in the simulation is retired but the row.
 13. WHAT STAYED FOR STAGE 6 (the brief's stage 4), all presentation and read
     by nothing in the simulation: drawUltUnder's root plate and drawUltOver's
     cage keyed `u.w === "heartwood"` (the freeze's picture, which played at
     the cast through stage 5), `ULTSIG.heartwood` (the charge sigil), the
     `ultFx` life entry (2.2), the cast voice (there was no heartwood arm; the
     shared fallback played) and `SPECS.heartwood` in both copies of fx.js.
     Stage 6 retires the plate, the cage and the life entry and gives the cast
     its own voice (readings 14-22); the charge sigil stays (it already says
     "roots going down and GRIPPING"); SPECS.heartwood is the orchestrator's
     `fx_remove` at the carry, never this builder (reading 20).

STAGE 6, THE PICTURE AND THE VOICE (v85 §4's picture and sound; §5's brief
stage 4, "picture, voice, carry"). Rows by the picture lab (scratch
`stage6-picture/hw_rows.py`, 9 rows) and `heartwood_voice_lab.py` (2 rows),
byte-exact to their files (the S6 table's header); v112 §6 carries every
number they were picked on. The labs' declared readings, kept:
 14. PRESENTATION ONLY. Nothing stage 6 adds is read by the simulation; the
     proof is engine_ab over every relic (Heartwood included) and the probe's
     [9]-[10], which read the voices and the picture's hook inside the fight.
 15. THE VOICE: v85 §4's two ("cast -- a green creak, 0.4s; a root -- a short
     creak-and-crack (Tendril's root voice, reused, quieter at 1.0s than at the
     vine's longer holds); close -- nothing"). Two arms are ADDED before the
     shared rune-crack fallback, which is re-emitted unchanged (eleven other
     relics still fall through to it). The cast is fireUlt's own prologue voice
     (`w: f.w.id`), unchanged, so it sounds once a cast. The root is one
     `SFX.play` in rootBlow after `T.rooted++;`: EVERY ROOTED BLOW, a new hold
     or a re-root (the design's "every blow roots"), none on a killing blow
     (it returns above), none at a close (there is no close voice).
 16. THE ROOT'S VOICE IS TENDRIL'S, TRANSCRIBED: Tendril's `bindweed-root` is
     not on this base (it landed on sc-tendril-fx), so `heartwood-root` is its
     arm body verbatim with one constant changed, g 0.5179 -> 0.2313 ("quieter":
     read as at least 3 dB under Tendril's quietest draw, the loudest rung that
     passes; the 3 dB is the lab's number, not the design's).
 17. THE PICTURE is on the FIGHTER (`grove*`, never `root*`, the simulation's),
     never on `m.ultFx` (one slot the opponent's cast takes: open item 25), and
     driven in tickPresentation (`tickGrove`, on the presentation clock, so the
     cast's 0.3s greening plays through the cast's own 0.08s stop), reading the
     window, the blade and the tally's counters rising: the verdant blade
     greens hilt to tip with a leaf scale (drawWeapon, over the shape, in its
     own frame -- SHAPES untouched), sheds a leaf off each pair as the green
     passes and sparse leaf motes for the window (drawn, the world pass under
     both balls), and at a close (the clock's, or the kill) withers tip to
     hilt over 0.4s, its leaves falling; at the caster's fall it is gone at
     once.
 18. THE ROOT IS TENDRIL'S PICTURE, REUSED (v85 §4): a root marks the held
     ball's `twineHeld` / `twineRootFade` / `twineHeldAge` / `twineHeldOut`,
     and Tendril's own tickTwine, `_twineRoot` and `_drawField`'s guard grow
     the four shoots, hold them for the pin and keep Paradox's hexagon off.
     That picture is on sc-tendril-fx and every later tip and NOT on this
     base: on a link built on sc-tendril-t3 the markers are inert and a held
     ball still draws the hexagon (the builder says so when it builds). A ball
     that holds itself (Canopy: pin with pinFree) is its own picture's: a root
     marks nothing on it and lets go of a mark it carried.
 19. THE TAG: the blow's own ENTANGLE tag (tagged at the contact, before the
     root's +1, with no count) prints the count the root leaves (Tendril's
     rule); the first-ever tag, the teaching panel, is left alone.
 20. NO FIELD (fx_spec NONE). The design asks "leaf motes off the blade, both
     copies"; a SPECS field fires once at the cast, from the one ultFx slot the
     opponent's cast takes, so the motes are drawn off the blade instead
     (Zenith's, Canopy's and Tendril's precedent). `SPECS.heartwood` -- the
     FREEZE's leaf-fall -- is retired by the orchestrator's `fx_remove` at the
     carry, in both copies, never by this builder: stage 6 refuses if its
     edits touched the inlined fx.js.
 21. THE FREEZE'S ART IS RETIRED: drawUltUnder's plate and drawUltOver's cage
     (replaced by comments), and the life entry `heartwood: 2.2` (the cast's
     record falls to the map's 1.5 and nothing draws from it).
 22. THE SCAN FOR STAGE 6 (`s6_static_checks`, `s6_output_checks`): no RNG,
     no ultFx, no Object./Reflect./eval/new, no call but CALL_OK_S6 (the
     picture's own methods, the canvas, Math, clamp / mix / shellHash, the
     motes' and bits' own arrays, `foe.stacks`, and -- each in its own row --
     the synth in the Sfx arms and SFX.play in the root's one line), writes
     only `grove*` fields, the canvas, the held ball's four `twine*` markers
     and a tag's count (tickGrove only), declared locals and nothing by index;
     the retired rows nothing but comments; in the page, the arms before the
     rune-crack fallback, the root's voice once where it belongs, every call
     and method once, the inlined fx.js untouched and the Math.random count
     unmoved.

THE CLOCK. The window runs on the window tickers' clock, which stops through a
hit stop (every batch build's convention). The lab ran it through freezes;
v112 §2 measures what that is worth here. The pin's own second is the
engine's `tickStasis` clock, which the lab shared.

THE SCAN (reading 8, made whole after the Spellbreaker review's finding 3,
and its calls made an allowlist after the v112 review's finding 2): every
insert's ADDED code (its re-emitted anchor taken out) draws no RNG, takes no
ultFx slot, writes no shared weapon and no pinFree, stops, beats, hurts or
stuns nothing, CALLS ONLY CALL_OK (the window's ticker, the root, Math.max and
the one entangle; `if` / `for`; the two method headers) -- no Object./Reflect.,
no call through a bracket or a call's result, no `new`, no arrow -- applies
nothing but the design's entangle line, deletes nothing, and writes only
WRITE_OK: the window, the tally, the clock and Grasp's three fields. 26
negative copies refuse (v112 §1, `runs/builder_negatives.txt`).

THE BASE is asserted BY CONTENT, never by which relic is last: Heartwood's row
with the shipped Rootfast, the engine gates the root pays through, and every
anchor below exactly once. Every insert goes AFTER or BEFORE a stable line
and re-emits it, so the builder re-applies on a later tip that carries other
new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "heartwood"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v85 §3-§5.
ULT = {
    "charge": 13,     # §4 "Charge 15", on the game's clock (Rick's batch ruling; measured, v112 §0) -- reading 1
    "dur": 8,         # §4 "window 8"
    "rootFor": 1.0,   # §3 "root 1.0 (taken)"; the lab defaults 0.45 (the rejected first pricing)
    "extraEnt": 1,    # §4 "entangle +1 on every hit ... on top of the channel's 2" -- stage 3
}
CHARGE_ALT_LAB16 = 14      # the lab's priced 16, converted (v112 §4; not built)
CHARGE_ALT_SHIPPED = 15    # the shipped relic's own engine charge, unconverted (v112 §4; not built)
TIP = "Every blow roots the foe where it stands, ball and weapon, and entangles"
SHIPPED_ULT = '''    ult:{ name:"Rootfast", charge:15, kind:"freeze", radius:230, dmg:9, apply:{entangle:3},
          freeze:1.3, tip:"Roots for 1.3 seconds, deals 9 damage and applies 3 Entangle stacks" },
'''
SHIPPED_DMG = "12.65"
ROW_HEAD = '''  { id:"heartwood", name:"Heartwood", aff:"verdant", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, spin:3.4, mode:"swing", arc:1.5, mass:3.0, dmg:'''


def ult_block(charge, extra_ent) -> str:
    return (f'''    ult:{{ name:"Rootfast", charge:{charge}, kind:"rootfast", dur:{ULT["dur"]},
          rootFor:{ULT["rootFor"]},
          extraEnt:{extra_ent},          // v85: the entangle (stage 3)
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
# `fireUlt` never runs for this relic), AND THE FREEZE OUT OF THE ROW. The row
# keeps every physical stat, the school's channel and the blurb; only the ult
# block changes. Nothing else reads the ult block's fields, so this link must
# be the lab's arm A (the relic with no ultimate) fight for fight.
S1 = [

("Rootfast becomes the root on every blow, stubbed; the freeze out of the row",
 SHIPPED_ULT,
 '''    /* ROOTFAST, REDESIGNED (v85; built v112): EVERY BLOW ROOTS. The one-shot
       freeze (radius 230, 9 damage, 3 entangle, 1.3s) is out of this row. For
       the window every blow the sword lands pins the foe `rootFor` seconds,
       ball and weapon, and entangles it `extraEnt` more. See `rootBlow` and
       `tickRootfast`. */
''' + ult_block("1e9", 0)),

]

# ---------------------------------------------------------------- stage 2 --
# THE ROOT (brief stage 1: "freeze out, `f.ultRoot` in, the pin on hit"), the
# extra entangle written but inert at 0, and the design's charge on the game's clock.
S2 = [

("the root has a charge: the design's 15 on the game's clock",
 '''    ult:{ name:"Rootfast", charge:1e9, kind:"rootfast", dur:8,
''',
 f'''    ult:{{ name:"Rootfast", charge:{ULT["charge"]}, kind:"rootfast", dur:{ULT["dur"]},   // v85 stage 2: every blow roots
'''),

("the fighter carries the root's window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while HEARTWOOD's Rootfast window is open (v85). null on every
       other relic and on this one outside its window: `resolveHit` reads it
       once, on the line after the knock, and `tickRootfast`'s loop is two
       iterations that do nothing. `rootTally` is the probe's count,
       cumulative over the fight; nothing in the simulation reads it. */
    this.ultRoot = null;
    this.rootTally = null;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "echo"){
''',
 '''    if (u.kind === "rootfast"){
      /* ROOTFAST (v85). NOTHING RESOLVES HERE: the cast opens the window for
         `u.dur` seconds, and every blow the sword lands inside it roots the
         foe (`rootBlow`, from `resolveHit`). The freeze's one-shot -- the
         generic tail's damage, entangle and stun -- is out of this relic's
         row, and this branch returns before that tail. */
      f.ultRoot = { t: 0, dur: u.dur };
      if (!f.rootTally)
        f.rootTally = { casts: 0, frames: 0, blows: 0, rooted: 0, roots: 0, ent: 0 };
      f.rootTally.casts++;
      return;
    }
    if (u.kind === "echo"){
'''),

("the window ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickRootfast(dt);              // ROOTFAST (v85)
'''),

("a blow inside the window roots, on the line after its knock",
 '''    const power = CONFIG.combat.knock * (self.w.knockMul || 1)
                * (crit ? 1.5 : 1) * kMul;
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;
''',
 '''    const power = CONFIG.combat.knock * (self.w.knockMul || 1)
                * (crit ? 1.5 : 1) * kMul;
    foe.vx += (kx / kl) * power; foe.vy += (ky / kl) * power;
    /* ROOTFAST (v85 §4): THE KNOCK ABOVE IS APPLIED AND THEN FROZEN BY THE
       PIN. A blow Heartwood lands while its window is open roots the foe on
       this line, so `pinV` keeps the vector the ball was just hit with and
       `move()` resumes it when the hold lifts. `ultRoot` is null on every
       other relic and outside the window, so this is one comparison. */
    if (self.ultRoot && (self === this.a || self === this.b)) this.rootBlow(self);
'''),

("tickRootfast keeps the window; rootBlow roots",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ ROOTFAST ==========
     v85 §1 / §4 / §5. THE WINDOW (`f.ultRoot`) runs `dur` on the window
     tickers' clock, so it freezes through a hit stop, and closes on its clock
     or either death. Nothing else happens here: the root is the blow's. */
  tickRootfast(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultRoot;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRoot = null; continue; }
      f.rootTally.frames++;
    }
  }

  /* A BLOW LANDED INSIDE THE WINDOW, called from `resolveHit` on the line
     after the knock. THE TARGET IS THE OPPONENT (a blow on a Twinshade shade
     roots Twinshade), and a killing blow roots nobody. GRASP'S WRITE: `pinV`
     is stored unless a longer hold already stands, `pin` and `pinMax` are
     max'd, and `pinFree` is NOT touched, so `tickStasis` locks the weapon too.
     Then entangle `extraEnt`, by side letter, on top of the channel's own.
     No damage, no knock, no beat, no hit stop. */
  rootBlow(f){
    const q = f === this.a ? this.b : this.a, u = f.w.ult, T = f.rootTally;
    T.blows++;
    if (!q.alive) return;
    const hold = u.rootFor;
    if (!(q.pin > 0)) T.roots++;
    if (!(q.pin > hold)) q.pinV = [q.vx, q.vy];
    q.pin = Math.max(q.pin, hold);
    q.pinMax = Math.max(q.pinMax, hold);
    T.rooted++;
    if (u.extraEnt > 0){ q.apply("entangle", u.extraEnt, f === this.a ? "a" : "b"); T.ent += u.extraEnt; }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the entangle",
 '''          extraEnt:0,          // v85: the entangle (stage 3)
''',
 f'''          extraEnt:{ULT["extraEnt"]},          // v85: the entangle (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE: THE MEASURED POINT NEAREST 50% BOTH SIDES (Rick, 2026-09-29: "you
# pick the blades. do whatevers best for balance."). The design's brief stage
# 3 was "the blade: Rick's target (§6); wide on 151", and §6.2 offered two
# ("Leave the blade and lift the relic, or bring the blade to 11.5-12 for 50");
# the ruling settles it at 50 for every redesign. The design gives the build no
# knob to move before the blade (§6.3's root length is a feel call, not a build
# knob), so none moved. Both sides (relic_rate: every other relic a foe, 10
# seeds a foe a side, 740 fights a block), seed0 2207 + 2317, 1480 fights a
# point, charge 13, on stage 3's link with `--set dmg=` (v112 §4):
#   10 -> 44.5   10.5 -> 47.9   11 -> 51.4   11.5 -> 55.7   12 -> 57.4
#   12.65 -> 58.6 (stage 3's link itself; the design's "leave the blade")
# 11 is the measured point nearest 50% (761 of 1480, +21 wins from half; 10.5
# is -31). The crossing is ~10.8 -- under the design's "11.5-12 for 50",
# because the built window is ~9.4s of match time where the lab's was 8 (v112
# §2). The shipped freeze reads 32.4% on the same seeds.
BLADE = "11"


def s5_edits(blade: str) -> list:
    return [
        ("the blade: the measured point nearest 50% both sides (Rick's ruling)",
         ROW_HEAD + SHIPPED_DMG + ",",
         ROW_HEAD + blade + ","),
    ]


# THE CARRY'S BLADE AS A MODULE-LEVEL TABLE, so `tools/chain_audit.py` (which
# reads module-level `(label, old, new)` tables, never a function's return)
# watches the blade like every other insert: a tip that puts Heartwood back at
# 12.65 reads "S5:... LOST".
S5 = s5_edits(BLADE)


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v85 §4's picture and sound; its §5 brief stage 4,
# "picture, voice, carry"), picked on measurements under Rick's "you pick i
# overrule" by the picture lab (scratch, `stage6-picture/hw_rows.py`, 9 rows)
# and `heartwood_voice_lab.py` (2 rows), v112 §6. PRESENTATION ONLY: engine_ab
# over all 38 relics, Heartwood included, is the proof, and the probe's [9]-[10]
# read the voices and the picture's hook inside the fight. The rows are
# byte-exact to the labs' own files (voice 4c38682da549a943, picture
# 184f5cb47c0bb5e7); the picture rows alone reproduce the picture lab's stamp
# (4ce2e98655411557), the voice rows alone the voice lab's end-to-end page
# (6a19b58add3cf38e), and the two sets give the same bytes in either order
# (ceba5e801f4cf91b). No two rows share an anchor line, so none is merged.
#   THE VOICE: two arms added BEFORE the shared rune-crack fallback, which is
#   re-emitted unchanged (Heartwood had no arm and fell through to it): the
#   cast (RISING, "a green creak, 0.4s") and the root (`heartwood-root`,
#   Tendril's root voice transcribed with its gain 0.5179 -> 0.2313). One line
#   on the sim path: SFX.play after `T.rooted++;` in rootBlow (every rooted
#   blow; a killing blow returns above it). The cast is fireUlt's own prologue
#   voice (`w: f.w.id`), unchanged. There is no close voice.
#   THE PICTURE: `tickGrove` in tickPresentation (the blade's green, the
#   sprout and the leaf motes, the wither and its leaves, the held ball's four
#   `twine*` markers for Tendril's root picture, the ENTANGLE tag's count);
#   the motes and the falling leaves in the world pass under both balls; the
#   blade greening in drawWeapon; the freeze's art retired (drawUltUnder's
#   plate, drawUltOver's cage, the life entry 2.2).
S6 = [

("Sfx: Heartwood's cast and root arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "heartwood"){                  // the wood takes the blade
          /* HEARTWOOD'S CAST, ROOTFAST -- v85 section 4: "a green creak,
             0.4s". RISING, of 6, picked on the numbers by
             `heartwood_voice_lab.py` under Rick's "you pick i overrule"
             (v112). Heartwood had no arm and fell through to rune-crack, which
             eleven other relics still use, so this ADDS arms before that
             fallback and leaves it alone.

             A sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s (the
             greening runs hilt to tip in 0.3 s) and held, pulsed 28 -> 40 a
             second, growing then settling. A creak, not a note: pulses 33 a
             second (PULSED 0.65), never a held tone. Green, not dry: its note,
             356 Hz, sits under the lowest the house's dry creak (Canopy's
             wither) reaches, 420 Hz, and it does not wither (+130 cents first
             to last); no crack (that is the root's). Audible 390 ms; loudest
             50 ms -2.9 dB re Heartwood's blow. Register at most 0.75 against
             rune-crack, the verdant and greatsword casts, Tendril's cast and
             root, the dry creak, the blow and the death voice. */
          const g = 0.2768;
          for (let s = 0, k = 0; s < 0.38; k++){
            const u = s / 0.4, f = 300 * Math.pow(4 / 3, Math.min(1, s / 0.3)), a = g * (s < 0.3 ? 0.5 + 0.5 * s / 0.3 : 1 - 3 * (s - 0.3));
            this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });
            s += (1 / (28 * Math.pow(1.428571, u))) * (1 + 0.12 * Math.sin(k * 2.4));
          }
        } else if (w === "heartwood-root"){             // and holds fast
          /* THE ROOT -- "a short creak-and-crack (Tendril's root voice,
             reused, quieter at 1.0s than at the vine's longer holds)" (v85
             section 4). Tendril's root arm (`bindweed-root`,
             bindweed_voice_lab.py DEEP) is not on every tip, so this is ITS
             BODY, VERBATIM, with one constant changed: g 0.5179 -> 0.2313
             (G-7dB, `heartwood_voice_lab.py`). `rootBlow` plays it on every
             blow that roots.

             A 260 Hz timber pulsed 33 -> 55 a second for 0.2 s into the crack,
             a 35 ms highpass snap over a sine falling 60 -> 30 Hz, now 4.1 dB
             under Tendril's (a 1.0 s hold against the vine's 1.2), -4.3 dB re
             Heartwood's blow and never over it. On the blow's own frame the
             root keeps its third-octave +6.9 dB over the blow and the blow its
             own +22.9 dB over the root; the crack lands 206 ms in, after the
             blow. Register 0.99 against Tendril's root (the same voice), at
             most 0.46 against rune-crack, the blow, the death voice and the
             cast. */
          const g = 0.2313, kc = 0.2683, kt = 0.3464;
          for (let s = 0, k = 0; s < 0.188; k++){
            const u = s / 0.2, a = g * kc * (0.45 + 0.55 * u);
            this._tone(t + s, { freq: 260, gain: a, dur: 0.03, type:"sine" });
            this._tone(t + s, { freq: 718, gain: a * 0.4, dur: 0.02, type:"sine" });
            s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
          this._burst(t + 0.2, { freq: 2600, q: 0.8, gain: g * 0.8, dur: 0.035, type:"highpass" });
          this._tone (t + 0.2, { freq: 60, to: 30, gain: g * kt, dur: 0.3, type:"sine" });
        } else {                                        // rune-crack'''),

('rootBlow: the root voice, once per rooted blow, after T.rooted++',
 '''    T.rooted++;''',
 '''    T.rooted++;
    /* ROOTFAST'S ROOT (v85 section 4: "a root -- a short creak-and-crack
       (Tendril's root voice, reused, quieter at 1.0s than at the vine's longer
       holds)"): every blow that roots, a new hold or a re-root, on the blow's
       own frame; a killing blow returned above and roots nobody, so it plays
       nothing. Plain SFX.play; nothing is read back (heartwood_voice_lab:
       fights identical). */
    SFX.play("ult", { w: "heartwood-root" });'''),

('rootfast picture: fighter fields',
 '''    this.ultRoot = null;
    this.rootTally = null;
''',
 '''    this.ultRoot = null;
    this.rootTally = null;
    /* ROOTFAST'S PICTURE (v85 section 4), and none of it is the window: the
       green outlives `ultRoot` by its 0.4s wither, so the picture keeps its
       own state. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickGrove`); nothing in the simulation reads any of it. `grove`, not
       `root`: the simulation owns `rootTally`, `rootBlow` and `rootFor`.
         groveFade -- 1 while the window stands; eased to 0 over the wither
           after the close or the match's end; 0 at once when the caster falls
         groveAge -- the presentation clock since the cast (the greening)
         groveOut -- the presentation clock since the close (the wither)
         groveRoots, groveRooted -- the holds and the roots already shown
           (`rootTally.roots`, `rootTally.rooted`)
         groveMotes -- leaf motes shed off the green blade (records): the
           sprout's leaves at the cast, then sparse ones for the window
         groveSprout -- stations of the leaf scale the cast's green has passed
         groveBits -- the wither's falling leaves (records)
         groveDrop -- leaf pairs the wither has let go, from the tip
         groveMoteN, groveMoteAcc -- the motes' count and spawn accumulator
       THE ROOT IS TENDRIL'S PICTURE, REUSED (v85 section 4): a root marks
       the held ball's `twineHeld` / `twineRootFade` / `twineHeldAge` /
       `twineHeldOut`, and Tendril's own `tickTwine`, `_twineRoot` and
       `_drawField`'s held-ball guard grow the four shoots, hold them for the
       pin, wilt them, and leave Paradox's hexagon off the ball. */
    this.groveFade = 0;
    this.groveAge = 0;
    this.groveOut = 0;
    this.groveRoots = 0;
    this.groveRooted = 0;
    this.groveMotes = [];
    this.groveSprout = 0;
    this.groveBits = [];
    this.groveDrop = 0;
    this.groveMoteN = 0;
    this.groveMoteAcc = 0;
'''),

('rootfast picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickGrove(dt);                 // ROOTFAST'S PICTURE (v85 section 4)
'''),

('rootfast picture: tickGrove',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------------ ROOTFAST'S PICTURE ---
     v85 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step and once in a
     hit stop, so the cast's greening plays through the cast's own 0.08s
     stop): 0.6 is the 0.3s greening, 0.8 the 0.4s wither. Everything
     is read off the simulation -- the window, the blade's own angle and
     reach, the tally's counters rising -- so the simulation makes no call for
     it, and nothing here writes a field the simulation reads: the picture's
     own fields, the held ball's four `twine*` markers (read only by Tendril's
     root picture and `_drawField`'s guard) and a tag's printed count.
     Not after the match and not once the caster falls: `tickRootfast` never
     runs again once `over` is set, so `ultRoot` would otherwise stand
     through the verdict. */
  tickGrove(dt){
    const R = CONFIG.physics.ballR, ST = 12;
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a, T = f.rootTally;
      for (let i = f.groveMotes.length - 1; i >= 0; i--){
        f.groveMotes[i].t += dt;
        if (f.groveMotes[i].t >= 2.4) f.groveMotes.splice(i, 1);
      }
      for (let i = f.groveBits.length - 1; i >= 0; i--){
        f.groveBits[i].t += dt;
        if (f.groveBits[i].t >= 1.5) f.groveBits.splice(i, 1);
      }
      if (!T) continue;
      /* A BALL THAT HOLDS ITSELF IS ITS OWN PICTURE'S: Canopy roots its own
         ball for its window (`pin` with `pinFree`, re-set every step), and
         its own aerial roots draw that hold. A root landing on it marks
         nothing, and a root it already carried lets go when its own takes
         over -- the shoots would otherwise stand for the canopy's whole
         window, saying this sword holds a ball it does not. Heartwood's
         opponent is rooted by nothing else, so every mark here is this
         caster's. */
      if (foe.twineHeld && foe.pinFree) foe.twineHeld = 0;
      /* THE ROOT, off the tally: `rooted` counts every root, `roots` the new
         holds (a ball that was not already held). A new hold brings the four
         shoots up out of the floor; a re-root of a held ball keeps them up
         and fresh (the pin is back at its full second, so the wilt goes).
         A killing blow roots nobody, and `rootBlow` counts neither. */
      if (T.rooted !== f.groveRooted){
        const hold = T.roots !== f.groveRoots;
        f.groveRooted = T.rooted; f.groveRoots = T.roots;
        if (foe.alive && foe.pin > 0){
          if (!foe.pinFree){
            if (hold || !(foe.twineRootFade > 0)) foe.twineHeldAge = 0;
            foe.twineHeld = 1; foe.twineRootFade = 1; foe.twineHeldOut = 0;
          }
          /* A ROOTED FOE CARRIES THE ENTANGLE TAG, WITH ITS COUNT. The blow
             tagged ENTANGLE at the contact this step (`resolveHit`, before
             the root's +1, and with no count); that tag now prints the count
             the root leaves. The first-ever tag is the teaching panel and
             prints no count, so it is left alone. */
          const n = foe.stacks("entangle");
          for (let i = this.tags.length - 1; i >= 0; i--){
            const g = this.tags[i];
            if (g.key !== "entangle" || g.max - g.life > 0.1
                || Math.hypot(g.x - foe.x, g.y - foe.y) >= R * 3) continue;
            if (!g.first) g.val = n;
            break;
          }
        }
      }
      const Z = (this.over || !f.alive) ? null : f.ultRoot;
      if (Z){
        if (!(f.groveFade > 0) || f.groveOut > 0){                // a new window
          f.groveAge = 0; f.groveOut = 0; f.groveDrop = 0; f.groveSprout = 0;
        }
        f.groveFade = 1;
        f.groveAge += dt;
        /* THE SPROUT: as the green's front passes each station of the leaf
           scale, the pair there sheds a leaf -- the blade bursts into leaf at
           the cast. Then LEAF MOTES shed off it, sparse, for the window. Both
           drawn, in place of a field on the one ultFx slot; placed by the
           blade and by shellHash on their count: no rng. */
        {
          const B = this.groveBlade(f), xF = B.L * (Math.min(1, f.groveAge / 0.6) * 1.04 - 0.02);
          const n = Math.floor(B.L * 0.74 / ST);
          while (f.groveSprout < n && B.L * 0.20 + (f.groveSprout + 1) * ST <= xF){
            const k = ++f.groveSprout, x = B.L * 0.20 + k * ST, y = this.groveHalf(B.L, f.w.artW, x);
            for (const sd of [-1, 1])
              f.groveMotes.push({ x: B.x + B.ux * x - B.uy * y * sd, y: B.y + B.uy * x + B.ux * y * sd,
                                  t: 0, n: f.groveMoteN++, big: 1 });
          }
        }
        f.groveMoteAcc += dt * 1.6;
        while (f.groveMoteAcc >= 1){
          f.groveMoteAcc -= 1;
          const B = this.groveBlade(f), k = f.groveMoteN++;
          const x = B.L * (0.28 + 0.66 * shellHash(9851 + f.side, k));
          if (x > B.L * (Math.min(1, f.groveAge / 0.6) * 1.04 - 0.02)) continue;
          const y = (shellHash(9853 + f.side, k) - 0.5) * 1.6 * this.groveHalf(B.L, f.w.artW, x);
          f.groveMotes.push({ x: B.x + B.ux * x - B.uy * y, y: B.y + B.uy * x + B.ux * y, t: 0, n: k });
        }
        if (f.groveMotes.length > 24) f.groveMotes.splice(0, f.groveMotes.length - 24);
      } else if (f.groveFade > 0){
        if (!f.alive){ f.groveFade = 0; f.groveOut = 0; continue; }   // the shatter owns it
        f.groveFade = Math.max(0, f.groveFade - dt / 0.8);
        f.groveOut += dt;
        /* THE BROWN RUNS TIP TO HILT (reaching the hilt at three quarters of
           the wither), and each leaf pair it passes lets go: the same
           stations `_groveScale` draws, on the blade as it stands. */
        const B = this.groveBlade(f), fr = Math.min(1, f.groveOut / 0.8 / 0.75);
        const n = Math.floor(B.L * 0.74 / ST);
        let passed = 0;
        for (let k = 1; k <= n; k++) if (B.L * 0.20 + k * ST >= (1 - fr) * B.L) passed++;
        const ang = Math.atan2(B.uy, B.ux);
        while (f.groveDrop < passed){
          const k = n - f.groveDrop++;
          if (k < 1) break;
          const x = B.L * 0.20 + k * ST, y = this.groveHalf(B.L, f.w.artW, x);
          for (const sd of [-1, 1])
            f.groveBits.push({ x: B.x + B.ux * x - B.uy * y * sd, y: B.y + B.uy * x + B.ux * y * sd,
                               a: ang + sd * 0.85, t: 0,
                               vx: (shellHash(9855 + f.side, k * 2 + sd) - 0.5) * 60,
                               vy: -10 - 30 * shellHash(9857 + f.side, k * 2 + sd),
                               spin: (shellHash(9859 + f.side, k * 2 + sd) - 0.5) * 7 });
        }
      }
    }
  }

  /* The blade in the hall, exactly as `drawWeapon` draws it: its base at
     R - 6 out along the swing angle, its axis, its length (the art's
     `reach + 6`). Heartwood swings one blade (`blades:[0]`). Pure. */
  groveBlade(f){
    const R = CONFIG.physics.ballR, a = f.theta + (f.bladeSet || f.w.blades)[0] * TAU;
    const ux = Math.cos(a), uy = Math.sin(a);
    return { x: f.x + ux * (R - 6), y: f.y + uy * (R - 6), ux, uy,
             L: f.w.reach * this.actMods.reach * f.reachMul + 6 };
  }
  /* The leaf blade's half-width at `x` along it (`_gsGrown`'s margin, art
     width `W`). Pure. */
  groveHalf(L, W, x){
    const u = clamp((x - L * 0.20) / (L * 0.80), 0, 1);
    return W * 0.19 * 1.5 * Math.sin(Math.PI * u) * 0.96;
  }

  tickWinnow(dt){
'''),

('rootfast picture: the ground call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* ROOTFAST'S GROUND (v85 section 4): the leaf motes shed off the green
       blade and the wither's falling leaves. The WORLD pass and under both
       balls: nothing of it reaches the bloom (CLAUDE.md section 4.1c) and no
       ball's disc is painted over (4.1b). The root's four shoots are
       Tendril's own calls (`drawTwine`, `drawTwineTop`). */
    if (__world) this.drawGrove(m);
'''),

("rootfast picture: the blade's hook in drawWeapon",
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
''',
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
      /* ROOTFAST (v85 section 4): for the window the verdant blade greens,
         hilt to tip over the cast's 0.3s, with a leaf scale along it, and
         withers after the close (`_groveBlade`), over the shape in the
         shape's own frame. `groveFade` is 0 on every other relic, so this
         is one comparison on a field nothing else writes. */
      if (f.groveFade > 0 && f.w.shape === "greatsword") this._groveBlade(c, m, f, reach + 6, f.w.artW);
'''),

('rootfast picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* --------------------------------------------------------- THE GROVE ---
     ROOTFAST (v85 section 4). THE CAST: the sword greens from hilt to tip
     over 0.3s -- sap up the grip, then the leaf blade from steel to living
     green, a bright front crossing it -- and the leaf scale sprouts along
     both margins as the green passes: a pair every 12 units, Tendril's scale
     on a sword. THE WINDOW: the blade stays green and sheds leaf motes (drawn,
     in place of a field on the one ultFx slot); the cast's sprout sheds a
     leaf off each pair as the green reaches it. THE ROOT is Tendril's four
     shoots out of the floor, up the held ball's rim, for the pin's second,
     in place of Paradox's hexagon (marked in `tickGrove`, drawn by
     `_twineRoot`); the blow's ENTANGLE tag carries the count the root
     leaves. THE CLOSE: brown runs tip to hilt over 0.4s and every leaf pair
     it passes lets go and falls; the green fades and the steel is back.

     IT HANGS OFF THE FIGHTER (`groveFade`, `groveAge`, `groveOut`, the
     records), never `m.ultFx` (open item 25). PRESENTATION ONLY: no rng, no
     spawnFx, no Math.random -- shellHash and the clocks -- and nothing here
     writes a field the simulation reads. */
  drawGrove(m){
    const a = m.a, b = m.b;
    if (!a.groveMotes.length && !b.groveMotes.length
        && !a.groveBits.length && !b.groveBits.length) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.groveMotes.length) this._groveMotes(f);
      if (f.groveBits.length) this._groveBits(f);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE LEAF MOTES: shed off the blade, drifting down and swaying -- the
     sprout's leaves as the scale draws them (the school's core, a dark
     edge), the window's sparse ones small and pale */
  _groveMotes(f){
    const c = this.ctx, P = f.aff;
    c.lineWidth = 1;
    for (const q of f.groveMotes){
      const s = q.t * 0.5, k = q.t / 2.4, h = shellHash(9861 + f.side, q.n);
      const x = q.x + Math.sin(s * 3.1 + h * 6.28) * 5 + (h - 0.5) * 18 * s;
      const y = q.y + 18 * s + 10 * s * s;
      c.globalAlpha = 0.9 * (1 - k) * Math.min(1, k * 8);
      c.beginPath();
      if (q.big){
        this._groveLeaf(c, x, y, s * 2.4 + h * 6.28, 8.4, 8.4 * 0.42);
        c.fillStyle = P.core; c.fill(); c.strokeStyle = P.dark; c.stroke();
      } else {
        this._groveLeaf(c, x, y, s * 2.4 + h * 6.28, 4.4, 1.8);
        c.fillStyle = P.glow; c.fill();
      }
    }
  }

  /* THE WITHER'S LEAVES, falling off the blade */
  _groveBits(f){
    const c = this.ctx;
    for (const d of f.groveBits){
      const s = d.t * 0.5, k = d.t / 1.5;
      c.save();
      c.translate(d.x + d.vx * s, d.y + d.vy * s + 420 * s * s);
      c.rotate(d.a + d.spin * s);
      c.globalAlpha = (1 - k * k) * 0.95;
      c.beginPath(); this._groveLeaf(c, 0, 0, 0, 8.4, 8.4 * 0.4);
      c.fillStyle = "#8A7A3A"; c.fill();
      c.strokeStyle = "#2A2012"; c.lineWidth = 1; c.stroke();
      c.restore();
    }
  }

  /* THE BLADE, from `drawWeapon`, in the blade's frame (x along it from its
     base, the art's length `L` and width `W`), over the shape just drawn. */
  _groveBlade(c, m, f, L, W){
    const live = !!(f.ultRoot && !m.over && f.alive);
    const g = live ? Math.min(1, f.groveAge / 0.6) : 1;
    const b = live ? 0 : Math.min(1, f.groveOut / 0.8), fr = Math.min(1, b / 0.75);
    const q = clamp((b - 0.6) / 0.4, 0, 1), al = 1 - q * q * (3 - 2 * q);
    if (!(al > 0.01)) return;
    const xF = L * (g * 1.04 - 0.02);                  // the green's front, from the grip
    const xB = L * (1 - fr);                           // the brown's front, from the tip
    c.save();
    c.globalAlpha *= al;
    c.lineCap = "round"; c.lineJoin = "round";
    this._groveGreen(c, L, W, f.aff, xF, xB);
    this._groveScale(c, L, W, f.aff, xF, xB, f.groveDrop);
    if (g < 1) this._groveFront(c, L, W, f.aff, xF, g);
    c.restore();
  }

  /* The leaf blade gone living: `_gsGrown`'s own outline, filled green up to
     the front (a lit upper margin, the school's core a shade down, a dark
     underside: picked on measurement, the most change against the steel that
     keeps the blade off the floor -- |dL| 0.189 and dE 32 against the steel,
     0.164 against the floor where the steel is 0.188), sap
     up the grip, the midrib and veins re-cut dark with a pale seam; past the
     brown's front, dead. */
  _groveGreen(c, L, W, P, xF, xB){
    const bh = W * 0.19, x1 = Math.min(xF, L * 1.02);
    if (!(x1 > -L * 0.02)) return;
    const leaf = () => {
      c.beginPath(); c.moveTo(L * 0.20, 0);
      c.bezierCurveTo(L * 0.34, -bh * 1.55, L * 0.72, -bh * 1.45, L, 0);
      c.bezierCurveTo(L * 0.72, bh * 1.45, L * 0.34, bh * 1.55, L * 0.20, 0);
      c.closePath();
    };
    c.save();
    c.beginPath(); c.rect(-L * 0.05, -W * 2, x1 + L * 0.05, W * 4); c.clip();
    c.strokeStyle = P.core; c.lineWidth = Math.max(1, W * 0.06);          // sap up the grip
    c.beginPath(); c.moveTo(-L * 0.01, W * 0.02); c.lineTo(L * 0.20, 0); c.stroke();
    leaf();
    const gr = c.createLinearGradient(0, -bh * 1.5, 0, bh * 1.5);
    gr.addColorStop(0, mix(P.core, P.glow, 0.15)); gr.addColorStop(0.45, mix(P.core, P.dark, 0.2));
    gr.addColorStop(1, mix(P.core, P.dark, 0.7));
    c.fillStyle = gr; c.fill();
    if (xB < x1){                                                          // the dead part
      c.save();
      c.beginPath(); c.rect(xB, -W * 2, L * 1.1 - xB, W * 4); c.clip();
      leaf();
      const gb = c.createLinearGradient(0, -bh * 1.5, 0, bh * 1.5);
      gb.addColorStop(0, "#8A7A3A"); gb.addColorStop(0.5, "#6E5B2E"); gb.addColorStop(1, "#2A2012");
      c.fillStyle = gb; c.fill();
      c.restore();
    }
    c.strokeStyle = P.dark;                                                // the midrib
    c.lineWidth = Math.max(1, W * 0.05);
    c.beginPath(); c.moveTo(L * 0.22, 0); c.lineTo(L * 0.98, 0); c.stroke();
    c.lineWidth = Math.max(1, W * 0.026);                                  // and its veins
    c.beginPath();
    for (let i = 1; i <= 5; i++){
      const u = i / 6, x = L * (0.24 + 0.68 * u), y = bh * 1.40 * Math.sin(Math.PI * u);
      for (const sg of [-1, 1]){ c.moveTo(x - L * 0.05, 0); c.lineTo(x + L * 0.03, sg * y * 0.72); }
    }
    c.stroke();
    c.globalAlpha *= 0.6; c.strokeStyle = P.glow; c.lineWidth = Math.max(0.8, W * 0.018);
    c.beginPath(); c.moveTo(L * 0.24, -W * 0.012); c.lineTo(Math.min(xB, L * 0.94), -W * 0.012); c.stroke();
    c.restore();
  }

  /* THE LEAF SCALE: a leaf pair every 12 units along both margins, each
     sprouting as the green's front passes it; dead past the brown's front,
     and the `drop` pairs nearest the tip already let go. */
  _groveScale(c, L, W, P, xF, xB, drop){
    const ST = 12, n = Math.floor(L * 0.74 / ST), live = [], dead = [];
    for (let k = 1; k <= n - drop; k++){
      const x = L * 0.20 + ST * k, sc = clamp((xF - x) / (ST * 0.8), 0, 1);
      if (!(sc > 0.02)) continue;
      const u = (x - L * 0.20) / (L * 0.80), y = W * 0.19 * 1.5 * Math.sin(Math.PI * u) * 0.96;
      (x > xB ? dead : live).push([x, y, sc]);
    }
    for (const [list, fill, edge] of [[live, P.core, P.dark], [dead, "#8A7A3A", "#2A2012"]]){
      if (!list.length) continue;
      c.beginPath();
      for (const [x, y, sc] of list)
        for (const sd of [-1, 1])
          this._groveLeaf(c, x - ST * 0.25, sd * (y - 1.4), sd * 0.85, 8.4 * sc, 8.4 * sc * 0.42);
      c.fillStyle = fill; c.fill();
      c.strokeStyle = edge; c.lineWidth = 1.1; c.stroke();
    }
  }

  /* The green's front crossing the blade in the cast's 0.3s: a pale bar */
  _groveFront(c, L, W, P, xF, g){
    if (!(xF > 0)) return;
    const h = xF < L * 0.20 ? W * 0.10
            : W * 0.19 * 1.5 * Math.sin(Math.PI * clamp((xF - L * 0.20) / (L * 0.80), 0, 1)) + 2.5;
    c.globalAlpha *= 0.35 + 0.65 * (1 - g);
    c.strokeStyle = P.glow; c.lineWidth = 2.6;
    c.beginPath(); c.moveTo(xF, -h); c.lineTo(xF, h); c.stroke();
  }

  /* One leaf, base at (x, y), pointing along `a`: added to the current path. */
  _groveLeaf(c, x, y, a, L, W){
    const ux = Math.cos(a), uy = Math.sin(a);
    c.moveTo(x, y);
    c.quadraticCurveTo(x + ux * L * 0.5 - uy * W, y + uy * L * 0.5 + ux * W, x + ux * L, y + uy * L);
    c.quadraticCurveTo(x + ux * L * 0.5 + uy * W, y + uy * L * 0.5 - ux * W, x, y);
  }

  drawMotes(m){
'''),

("rootfast picture: the freeze's root plate retired",
 '''    /* ---- Rootfast: the root PLATE, spreading from the quarry outward ------- */
    else if (u.w === "heartwood"){
      const grow = clamp(u.t / 0.42, 0, 1);
      const brown = clamp((u.t - u.life * 0.62) / (u.life * 0.38), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.80) / (u.life * 0.20), 0, 1);
      const N = 11;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + shellHash(71, i) * 0.5;
        const len = 132 * grow * (0.55 + shellHash(72, i) * 0.7);
        c.globalAlpha = 0.85 * fade;
        /* Roots run from the TARGET, not the caster — this is the whole
           difference from Bramblesnare and it has to be visible on the floor
           before the cage above it explains itself. */
        c.strokeStyle = brown > 0 ? "#4A3418" : "#0D3A1A";
        c.lineWidth = 6 - (i % 3);
        this._jag(c, tgt.x, tgt.y, tgt.x + Math.cos(a) * len,
                  tgt.y + Math.sin(a) * len * 0.5, 7, 15, 700 + i, grow);
        c.globalAlpha = 0.5 * fade * (1 - brown);
        c.strokeStyle = "#2E6B2C"; c.lineWidth = 2;
        this._jag(c, tgt.x, tgt.y, tgt.x + Math.cos(a) * len,
                  tgt.y + Math.sin(a) * len * 0.5, 7, 15, 700 + i, grow);
      }
    }
''',
 '''    /* ---- Rootfast's root plate was the FREEZE's (eleven roots run out from
       the quarry at the cast, over the record's 2.2); retired with it (v85,
       v112 stage 6). The root is now every blow's, drawn off the held ball
       (Tendril's four shoots, `_twineRoot`), and the window's picture hangs
       off the caster (`_groveBlade`, `drawGrove`), where the one ultFx slot
       cannot erase it. */
'''),

("rootfast picture: the freeze's cage retired",
 '''    /* ---- Rootfast: a cage grown UP over the quarry, then browning ---------- */
    else if (u.w === "heartwood"){
      const grow = clamp(u.t / 0.40, 0, 1);
      const brown = clamp((u.t - u.life * 0.62) / (u.life * 0.30), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.78) / (u.life * 0.22), 0, 1);
      const R = CONFIG.physics.ballR;
      const N = 9;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU;
        const h = (R + 78) * grow;
        const bx = tgt.x + Math.cos(a) * (R + 16);
        const by = tgt.y + Math.sin(a) * (R + 16);
        c.globalAlpha = fade * (0.9 - brown * 0.3);
        c.strokeStyle = brown > 0.5 ? "#5A4420" : "#2E6B2C";
        c.lineWidth = 5.2 - (i % 3) * 0.9;
        c.shadowColor = brown > 0.5 ? "#00000000" : "#4FD06B";
        c.shadowBlur = brown > 0.5 ? 0 : 12;
        /* Each stem rises and BENDS IN over the quarry — the cage closes.
           Bramblesnare's roots stay on the floor and never arch. */
        c.beginPath();
        c.moveTo(bx, by);
        c.quadraticCurveTo(bx, by - h * 0.8, tgt.x + Math.cos(a) * 6, by - h);
        c.stroke();
        c.shadowBlur = 0;
        if (grow > 0.5){                      // leaves unfurling on the stems
          for (let j = 1; j <= 2; j++){
            const t2 = j / 3;
            const lx = lerp(bx, tgt.x + Math.cos(a) * 6, t2);
            const ly = lerp(by, by - h, t2);
            c.globalAlpha = fade * (1 - brown) * 0.85 * clamp((grow - 0.5) * 2, 0, 1);
            c.fillStyle = "#BCF7C7";
            c.save(); c.translate(lx, ly); c.rotate(a + j * 1.1);
            c.beginPath(); c.ellipse(0, 0, 8, 3.4, 0, 0, TAU); c.fill();
            c.restore();
          }
        }
      }
    }
''',
 '''    /* ---- Rootfast's cage was the FREEZE's (nine stems arching over the
       quarry, browning over the record's 2.2); retired with it (v85, v112
       stage 6). The cast is the blade greening hilt to tip (`_groveBlade`). */
'''),

("rootfast picture: the cast record's life",
 '''              oathwound: 1.5, heartwood: 2.2, ''',
 '''              /* ROOTFAST IS NO LONGER A FREEZE (v85; v112 stage 6): its 2.2
                 went out with the root plate and the cage, so the first line
                 above is Bramblesnare's alone. The cast's record falls to the map's
                 own 1.5 and carries the CAST only -- nothing draws from it. */
              oathwound: 1.5, '''),

]

# ------------------------------------------------------- the insert scan --
# WHAT STAGES 1-5's ADDED CODE MAY WRITE (reading 8): the window record and the
# tally on the fighter (and the tally's counters), the window's clock, and the
# three fields of Grasp's write on the opponent. `pinFree` is refused above; the
# one status is the design's entangle, by side letter, on this exact line.
WRITE_OK = {("this", "ultRoot"), ("this", "rootTally"), ("f", "ultRoot"), ("f", "rootTally"),
            ("rootTally", "casts"), ("rootTally", "frames"), ("Z", "t"),
            ("T", "blows"), ("T", "roots"), ("T", "rooted"), ("T", "ent"),
            ("q", "pinV"), ("q", "pin"), ("q", "pinMax")}
APPLY_LINE = '.apply("entangle", u.extraEnt, f === this.a ? "a" : "b")'
# WHAT IT MAY CALL, AND NOTHING ELSE: the window's ticker (from step), the root (from resolveHit),
# Math.max (Grasp's max'd pin) and the one entangle (APPLY_LINE); `if` / `for`; the two method headers.
CALL_OK = {("this", "tickRootfast"), ("this", "rootBlow"), ("Math", "max"), ("q", "apply")}
KEYWORD_PAREN = {"if", "for"}
METHOD_DEFS = {"tickRootfast", "rootBlow"}

# ------------------------------------------------------ the stage-6 scan --
# STAGE 6 IS PRESENTATION (reading 22). The rows a rule binds to, by the head
# of their label (each must match exactly one row of S6):
S6_SFX_ROW = "Sfx: Heartwood's cast and root arms"
S6_FIELDS_ROW = "rootfast picture: fighter fields"
S6_TICK_ROW = "rootfast picture: tickGrove"
S6_DRAW_ROW = "rootfast picture: the drawing methods"
# the one-line rows: their added code (comments out) is exactly this line
S6_ONE_LINE = {
    "rootBlow: the root voice": ['SFX.play("ult", { w: "heartwood-root" });'],
    "rootfast picture: the presentation call": ["this.tickGrove(dt);"],
    "rootfast picture: the ground call": ["if (__world) this.drawGrove(m);"],
    "rootfast picture: the blade's hook in drawWeapon":
        ['if (f.groveFade > 0 && f.w.shape === "greatsword") this._groveBlade(c, m, f, reach + 6, f.w.artW);'],
    "rootfast picture: the cast record's life": ["oathwound: 1.5,"],
}
S6_VOICE_LINE = S6_ONE_LINE["rootBlow: the root voice"][0]
# the retiring rows: comments only
S6_RETIRED = ("rootfast picture: the freeze's root plate retired", "rootfast picture: the freeze's cage retired")
# the Sfx arms, before the shared fallback (kept once, re-emitted unchanged)
S6_ARMS = ('} else if (w === "heartwood"){', '} else if (w === "heartwood-root"){')
RUNE_CRACK = "        } else {                                        // rune-crack"
# THE PICTURE'S OWN METHODS (tickGrove, groveBlade and groveHalf on the Match;
# the rest on the renderer), each defined once and called only as `this.<name>`
S6_METHODS = ("tickGrove", "groveBlade", "groveHalf", "drawGrove", "_groveMotes", "_groveBits", "_groveBlade",
              "_groveGreen", "_groveScale", "_groveFront", "_groveLeaf")
# WHAT STAGE 6's ADDED CODE MAY CALL, AND NOTHING ELSE (an allowlist, as the
# stage 1-5 scan's): the picture's own methods, Math, the page's pure helpers
# clamp / mix / shellHash, `foe.stacks` (a read); and, each only in its own
# row, the canvas and the gradients (the drawing methods), the motes' and
# bits' own arrays (tickGrove), the synth (the Sfx arms) and SFX.play (the
# root's one line). `if` / `for` / `while`; the method headers.
S6_CALL_ANY = ({("this", k) for k in S6_METHODS}
               | {("Math", k) for k in ("min", "max", "sin", "cos", "atan2", "floor", "hypot", "pow")}
               | {(None, k) for k in ("clamp", "mix", "shellHash")})
S6_CALL_ROW = {
    S6_SFX_ROW: {("this", "_tone"), ("this", "_burst")},
    "rootBlow: the root voice": {("SFX", "play")},
    S6_TICK_ROW: {("foe", "stacks"), ("f.groveMotes", "push"), ("f.groveMotes", "splice"),
                  ("f.groveBits", "push"), ("f.groveBits", "splice")},
    S6_DRAW_ROW: {("c", k) for k in ("save", "restore", "beginPath", "rect", "clip", "moveTo", "lineTo", "stroke",
                                     "fill", "bezierCurveTo", "quadraticCurveTo", "closePath", "createLinearGradient",
                                     "translate", "rotate")}
                 | {("gr", "addColorStop"), ("gb", "addColorStop"), (None, "leaf"), (")", "push")},
}
# exact lines a row-bound rule allows (whitespace normalised): the drawing
# methods' one local arrow and its one call through a parenthesis; tickGrove's
# record clocks and the tag's printed count
S6_DRAW_ARROW = "const leaf = () => {"
S6_DRAW_PAREN = "(x > xB ? dead : live).push([x, y, sc]);"
S6_TICK_WRITES = {("f.groveMotes[i]", "t"): "f.groveMotes[i].t += dt;",
                  ("f.groveBits[i]", "t"): "f.groveBits[i].t += dt;",
                  ("g", "val"): "if (!g.first) g.val = n;"}
S6_TWINE = ("twineHeld", "twineRootFade", "twineHeldAge", "twineHeldOut")
S6_CANVAS = ("fillStyle", "strokeStyle", "lineWidth", "globalAlpha", "lineCap", "lineJoin")
S6_TABLE_READS = {"CONFIG.physics.ballR", "CONFIG.arena"}
S6_WRITE = r"\s*(?:=(?![=>])|\+=|-=|\*=|/=|\+\+|--)"
S6_RECV = r"(?<![\w$.])((?:this|[A-Za-z_$][\w$]*)(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*)"
S6_NAMES = ("tickGrove", "drawGrove", "groveFade", "_groveBlade", '"heartwood-root"')


def s6_added(old: str, new: str) -> str:
    """A stage-6 row's ADDED code, comments out: its new text less the anchor it
    re-emits (a replace row that re-emits nothing adds all of its new text)."""
    return strip_comments(new.replace(old, "", 1) if old in new else new)


def s6_lines(ins: str) -> list:
    return [" ".join(ln.split()) for ln in ins.splitlines() if ln.strip()]


def s6_calls(ins: str):
    """Every `name(` in the code, with its receiver: the dotted path before a
    `.`, or ')' / ']' for a call through a parenthesis or an index, or None."""
    for mc in re.finditer(r"([\w$]+)\s*\(", ins):
        j = mc.start() - 1
        while j >= 0 and ins[j] in " \t\n":
            j -= 1
        recv = None
        if j >= 0 and ins[j] == ".":
            k = j - 1
            while k >= 0 and ins[k] in " \t\n":
                k -= 1
            if k >= 0 and ins[k] in ")]":
                recv = ins[k]
            else:
                mr = re.search(r"((?:[\w$]+(?:\[[^\]]*\])?\s*\.\s*)*[\w$]+(?:\[[^\]]*\])?)\s*$", ins[:k + 1])
                recv = re.sub(r"\s+", "", mr.group(1)) if mr else "?"
        line = ins[ins.rfind("\n", 0, mc.start()) + 1:ins.find("\n", mc.start()) if "\n" in ins[mc.start():] else len(ins)]
        yield recv, mc.group(1), " ".join(line.split())


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION (reading 22). Its ADDED code (a row's re-emitted
    anchor aside) draws no RNG, never takes the one ultFx slot (open item 25),
    reaches no Object / Reflect / eval / new / global, CALLS only the allowlist
    (the picture's own methods, Math, the page's pure helpers, `foe.stacks`;
    the canvas, the arrays, the synth and SFX.play each only in its own row),
    WRITES only `grove*` fields (the fighter's constructor, tickGrove), the
    canvas (the drawing methods), the held ball's four `twine*` markers, two
    record clocks and a tag's count (tickGrove, by exact line) and locals it
    declares, nothing through an index or a destructuring, and reads no module
    table but two CONFIG entries. SFX only in the root's one line; the synth
    only in the Sfx arms; the tags only in tickGrove; the one-line rows whole;
    the retired rows nothing but comments. The probe's [9]-[10] and engine_ab
    are the dynamic proof. Run on every stage: it reads the table."""
    labels = [lb for lb, _o, _n in S6]
    for key in list(S6_ONE_LINE) + list(S6_RETIRED) + [S6_SFX_ROW, S6_FIELDS_ROW, S6_TICK_ROW, S6_DRAW_ROW]:
        if sum(1 for lb in labels if lb.startswith(key)) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's table has not exactly one row '{key}...'")
    for label, old, new in S6:
        ins = s6_added(old, new)
        lines = s6_lines(ins)
        row = next((k for k in S6_CALL_ROW if label.startswith(k)), None)
        tick, draw = label.startswith(S6_TICK_ROW), label.startswith(S6_DRAW_ROW)
        sfx, fields = label.startswith(S6_SFX_ROW), label.startswith(S6_FIELDS_ROW)
        one = next((k for k in S6_ONE_LINE if label.startswith(k)), None)
        if re.search(r"\brng\b", ins) or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws the RNG or uses the one ultFx slot")
        banned = re.search(r"\b(Object|Reflect|Function|eval|globalThis|window|document|new|delete|with|Proxy|"
                           r"setTimeout|setInterval|requestAnimationFrame|import)\b|`|[\])]\s*\(", ins)
        if banned:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' uses {banned.group(0)!r}")
        arrows = [ln for ln in lines if "=>" in ln]
        if arrows and not (draw and arrows == [S6_DRAW_ARROW]):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' has an arrow: {arrows}")
        # THE CALLS, AN ALLOWLIST
        for recv, name, line in s6_calls(ins):
            if recv is None and name in ("if", "for", "while"):
                continue
            if recv is None and name in S6_METHODS and re.fullmatch(re.escape(name) + r"\([\w, ]*\)\{", line):
                continue                                       # a method header
            if (recv, name) in S6_CALL_ANY or (row and (recv, name) in S6_CALL_ROW[row]):
                if recv == ")" and line != S6_DRAW_PAREN:
                    raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls through a parenthesis: {line!r}")
                continue
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls {(recv + '.') if recv else ''}"
                             f"{name}(): not the picture's own, Math, clamp / mix / shellHash or its row's own (reading 22)")
        if draw and (sum(ln.startswith(S6_DRAW_ARROW) for ln in lines) != 1
                     or len(re.findall(r"(?<![\w$.])leaf\s*=(?![=>])", ins)) != 1):
            raise SystemExit("REFUSING TO WRITE -- the drawing methods do not bind `leaf` exactly once, as the arrow")
        # THE MODULE TABLES: two reads, no writes
        for mt in re.finditer(r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES|POSTFX|SLOSH|AC|SFX)\b"
                              r"(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*", ins):
            path = re.sub(r"\s+", "", mt.group(0))
            if path == "SFX.play" and one == "rootBlow: the root voice":
                continue
            if path not in S6_TABLE_READS or re.match(S6_WRITE, ins[mt.end():]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reaches a module table: {path!r}")
        # THE WRITES, AN ALLOWLIST
        if re.search(r"[\]}]\s*(?:=(?![=>])|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes through an index or a destructuring")
        for mw in list(re.finditer(S6_RECV + r"\s*\.\s*([A-Za-z_$][\w$]*)" + S6_WRITE, ins)) + \
                  list(re.finditer(r"(?:\+\+|--)\s*" + S6_RECV + r"\s*\.\s*([A-Za-z_$][\w$]*)", ins)):
            recv, prop = re.sub(r"\s+", "", mw.group(1)), mw.group(2)
            ok = ((fields and recv == "this" and prop.startswith("grove"))
                  or (tick and recv == "f" and prop.startswith("grove"))
                  or (tick and recv == "foe" and prop in S6_TWINE)
                  or (tick and (recv, prop) in S6_TICK_WRITES and lines.count(S6_TICK_WRITES[(recv, prop)]) == 1)
                  or (draw and recv == "c" and prop in S6_CANVAS))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes {recv}.{prop} (reading 22: "
                                 "its own grove* fields, the canvas, the held ball's twine* markers and a tag's count only)")
        for mb in re.finditer(r"(?<![\w$.\]\)])([A-Za-z_$][\w$]*)\s*(?:=(?![=>])|\+=|-=|\*=|/=|\+\+|--)", ins):
            nm = mb.group(1)
            if nm in ("const", "let", "var"):
                continue
            if not re.search(r"\b(?:const|let|var)\b[^;{]*?(?<![\w$.])" + re.escape(nm) + r"\s*=(?![=>])", ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' assigns `{nm}`, which it does not "
                                 "declare (a write outside the picture)")
        for mb in re.finditer(r"(?:\+\+|--)\s*([A-Za-z_$][\w$]*)(?![\w$.\[])", ins):
            if not re.search(r"\b(?:const|let|var)\b[^;{]*?(?<![\w$.])" + re.escape(mb.group(1)) + r"\s*=(?![=>])", ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' steps `{mb.group(1)}`, which it does not declare")
        # THE ROWS' OWN SHAPES
        if one and lines != S6_ONE_LINE[one]:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's one-line row ('{label}') is not that line alone:\n{ins}")
        if any(label.startswith(k) for k in S6_RETIRED) and lines:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's retiring row ('{label}') adds code:\n{ins}")
        if re.search(r"\bSFX\b", ins) and one != "rootBlow: the root voice":
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice outside the root's one line")
        if re.search(r"\b_tone\b|\b_burst\b|\b_sweep\b|\bctx\.currentTime\b", ins) and not sfx:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the synth outside the Sfx arms")
        if sfx and [ln for ln in lines if ln.startswith("} else if (w ===")] != list(S6_ARMS):
            raise SystemExit("REFUSING TO WRITE -- the Sfx row does not add exactly Heartwood's two arms")
        if re.search(r"\btags\b|\btaught\b|\.val\b|\.first\b", ins) and not tick:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' touches the tags outside tickGrove")
        if re.search(r"\btwine\w*", ins) and not tick:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' touches Tendril's markers outside tickGrove")
        # THE CANVAS: `c` only as the renderer's own context, or a method's first parameter
        for mb in re.finditer(r"\b(?:const|let|var)\s+c\s*=\s*([^,;\n]+)", ins):
            if mb.group(1).strip() != "this.ctx":
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' binds `c` to {mb.group(1).strip()!r}")
        if len(re.findall(r"(?<![\w$.])c\s*=(?![=>])", ins)) != len(re.findall(r"\b(?:const|let|var)\s+c\s*=\s*this\.ctx\b", ins)):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reassigns `c`")


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone -- SPECS.heartwood goes by the orchestrator's fx_remove at
    the carry, never by this builder (reading 20)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched; Heartwood's
    two arms before the shared rune-crack fallback, which is kept once; the
    freeze's art gone; the root's voice added once, in rootBlow, after the
    killing blow's return and on the line after `T.rooted++;`; fireUlt's cast
    voice unmoved; every call, pass and method wired exactly once; and no
    Math.random added or taken away."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy (no field: reading 20)")
    if s.count(RUNE_CRACK) != 1 or any(not 0 <= s.find(a) < s.find(RUNE_CRACK) for a in S6_ARMS):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, once, after Heartwood's arms")
    if 'u.w === "heartwood"' in out_code or re.search(r"\bheartwood\s*:\s*2\.2\b", out_code):
        raise SystemExit("REFUSING TO WRITE -- the freeze's art is still drawn (its drawUlt branches or its life entry)")
    need = ["this.tickGrove(dt);", "if (__world) this.drawGrove(m);", S6_ONE_LINE["rootfast picture: the blade's hook in drawWeapon"][0],
            S6_VOICE_LINE] + list(S6_ARMS)
    for nm in S6_METHODS:
        hd = re.findall(r"\n  " + re.escape(nm) + r"\([\w, ]*\)\{", out_code)
        if len(hd) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- the method {nm} is not defined exactly once ({len(hd)})")
    for ln in need:
        if out_code.count(ln) != code.count(ln) + 1 or code.count(ln):
            raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    i0 = out_code.find("\n  rootBlow(f){")
    i1 = out_code.find("\n  }\n", i0)
    body = " ".join(out_code[i0:i1].split())
    if not re.search(r'if \(!q\.alive\) return; .*T\.rooted\+\+; SFX\.play\("ult", \{ w: "heartwood-root" \}\); '
                     r'if \(u\.extraEnt > 0\)\{ q\.apply\("entangle"', body):
        raise SystemExit("REFUSING TO WRITE -- the root's voice is not in rootBlow, after the killing blow's return, "
                         "on the line after `T.rooted++;`")
    if out_code.count('SFX.play("ult", { w: f.w.id });') != code.count('SFX.play("ult", { w: f.w.id });'):
        raise SystemExit("REFUSING TO WRITE -- fireUlt's cast voice moved")
    if len(re.findall(r"\bSFX\.play\(", out_code)) != len(re.findall(r"\bSFX\.play\(", code)) + 1:
        raise SystemExit("REFUSING TO WRITE -- stage 6 adds a voice call other than the root's")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickGrove(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickGrove does not follow tickNovaFx in tickPresentation")
    if not re.search(r"if \(__world\) this\.drawTree\(m\);\n(?:\s*/\*[\s\S]*?\*/)?\s*if \(__world\) this\.drawGrove\(m\);", s):
        raise SystemExit("REFUSING TO WRITE -- the ground call does not follow the world pass's drawTree")
    if not re.search(r"if \(fn\) fn\(c, reach \+ 6, f\.w\.artW, pal, f\.drawK\);\n      \}\n(?:\s*/\*[\s\S]*?\*/)?\s*"
                     r"if \(f\.groveFade > 0 && f\.w\.shape === \"greatsword\"\) this\._groveBlade\(", s):
        raise SystemExit("REFUSING TO WRITE -- the blade's hook does not follow drawWeapon's shape")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- stage 6 adds or takes away a Math.random")
    tendril = "_twineRoot(" in code and "!(f.twineHeld > 0)" in code
    print("  ok    stage 6: presentation only (no RNG, no ultFx, calls only CALL_OK_S6, writes its own grove* "
          "fields, the canvas, the held ball's twine* markers and a tag's count only); the inlined fx.js untouched; "
          "the rune-crack fallback kept after Heartwood's two arms; the root's voice once, in rootBlow after "
          "T.rooted++; the freeze's art gone; every call, pass and method once")
    print("  note  Tendril's root picture " + ("IS on this source: a root draws the four shoots" if tendril else
          "is NOT on this source (it lands on sc-tendril-fx): the root's markers are inert here and a held ball "
          "draws Paradox's hexagon (reading 18)"))

# ---------------------------------------------------------------- naming --
NAMES =("ultRoot", "rootTally", "tickRootfast", "rootBlow", 'kind:"rootfast"', '"rootfast"')
STAGE_OUT = {"1": "sc-heartwood-stub", "2": "sc-heartwood-root", "3": "sc-heartwood-rootfast",
             "5": "sc-heartwood-b11", "6": "sc-heartwood-b11-fx"}


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    if A.stage in ("5", "6") and (BLADE is None or BLADE == SHIPPED_DMG):
        raise SystemExit(f"stage {A.stage}: the blade is not measured yet (BLADE)")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-heartwood"):
        raise SystemExit(f"refusing {out_p.name}: this builder's links are sc-heartwood*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: 02-chain already has a link of that name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    # READ AS BYTES: read_text() turns CRLF into LF, so this refusal could never fire (found by
    # thornwake_build.py, v113; for an LF source the two reads are the same text, so no link moves).
    s0 = src_p.read_bytes().decode("utf-8")
    if "\r" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nHEARTWOOD / ROOTFAST (REDESIGN) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The relic this builder redesigns, with its body;
    # the engine's gates the root pays through; the window clock.
    row = relic_row(code, RELIC)
    for need, why in (('shape:"greatsword"', "Heartwood is not a greatsword"),
                      ('mode:"swing"', "Heartwood does not swing"),
                      ('aff:"verdant"', "Heartwood is not verdant"),
                      ("onHit:{ entangle:2 }", "Heartwood does not carry the verdant channel")):
        if need not in row:
            raise SystemExit(f"wrong base: {why}")
    if " ".join((ROW_HEAD).split()) not in " ".join(row.split()):
        raise SystemExit("wrong base: Heartwood's greatsword profile has moved")
    for need, why in (("hurt(foe, dmg, src){", "no hurt(foe, dmg, src) gate"),
                      ("apply(key, n, src){", "no Fighter.apply(key, n, src)"),
                      ("get alive(){ return this.hp > 0; }", "no Fighter.alive"),
                      ("resolveHit(self, foe, hx, hy, seg, mul, over){", "no resolveHit"),
                      ("self.hits++; self.dealt += dmg;", "resolveHit no longer counts the blow"),
                      ("fireUlt(f, foe){", "no fireUlt"),
                      ("tickStasis(dt){", "no tickStasis"),
                      ("if (!f.pinFree) f.stun = Math.max(f.stun, f.pin);",
                       "tickStasis no longer locks the weapon of a hold without pinFree"),
                      ("if (f.pin > 0) return;", "move() no longer holds a pinned ball"),
                      ("f.vy = Math.max(0, f.pinV[1]);", "move() no longer resumes pinV (the Stasis clamp)")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'\n  entangle:\s+\{ name:"Entangle",', code):
        raise SystemExit("wrong base: no STATUS.entangle")
    # THE WINDOW CLOCK: a hit stop returns from step() before the window
    # tickers, and the tickers run before the hit loops.
    st = code[code.find("  step(dt){"):]
    hs = st.find("if (this.hitStop > 0){")
    tt = st.find("this.tickTendril(dt);")
    th = st.find("this.tickHits(self, foe, dt);")
    if tt < 0:
        raise SystemExit("wrong base: no `this.tickTendril(dt);` in step() -- the root's ticker "
                         "goes after Tendril's (v68), so this is not the Tendril lineage")
    if hs < 0 or not hs < st.find("return;", hs) < tt:
        raise SystemExit("wrong base: the window tickers do not stop in a hit stop")
    if not tt < th:
        raise SystemExit("wrong base: the window tickers do not run before the hit loops")
    # WHO ELSE CASTS THROUGH THE FREEZE'S GENERIC TAIL (read, never refused on:
    # Thornwake is being redesigned too, and either may be carried first).
    freezers = [rid for rid in re.findall(r'\{ id:"([a-z]+)", name:"', code)
                if 'kind:"freeze"' in relic_row(code, rid)]
    # THE NAMES THIS BUILD ADDS ARE FREE ON THE BASE.
    if A.stage == "1":
        for name in NAMES + S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")
        if s0.count(SHIPPED_ULT) != 1:
            raise SystemExit("wrong base: Heartwood does not carry the shipped Rootfast")
        if f"dmg:{SHIPPED_DMG}," not in row:
            raise SystemExit("wrong base: Heartwood is not at its shipped blade")
    print("  base  Heartwood's shipped body (verdant greatsword, swing, entangle 2); hurt / apply / "
          "resolveHit's count / tickStasis's lock / move's hold and resume; the window tickers stop "
          "in a hit stop and run before the hit loops")
    if A.stage == "1":
        print(f"  note  kind \"freeze\" on this base: {', '.join(freezers) or 'none'} -- its generic tail "
              "stays (reading 12)")

    blade = SHIPPED_DMG                 # stages 1-3 keep the shipped blade; stage 5 writes BLADE
    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"rootfast"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if not free_name("tickRootfast", code) or "charge:1e9" not in row:
                raise SystemExit("stage 2 goes on stage 1, once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if free_name("tickRootfast", code) or "extraEnt:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["extraEnt"])
        elif A.stage == "5":
            want = ult_block(ULT["charge"], ULT["extraEnt"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 5 goes on stage 3 (the entangle on, blade 12.65), once")
            blade = BLADE
            edits = S5
        else:
            # STAGE 6 GOES ON STAGE 5: the entangle on, the blade BLADE, and none of
            # stage 6's names in the source yet (the picture and the voice go on once).
            want = ult_block(ULT["charge"], ULT["extraEnt"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{BLADE}," not in row or free_name("tickRootfast", code)):
                raise SystemExit(f"stage 6 goes on stage 5 (the entangle on, blade {BLADE}), once")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            blade = BLADE
            edits = S6
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Heartwood's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:104]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if f"dmg:{blade}," not in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades|ult|mass|onHit)\s*=[^=]", ins) or \
           re.search(r"\bw\.ult\.\w+\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if "pinFree" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' touches "
                             "pinFree (the root is Grasp's write)")
        if re.search(r"hitStop\s*=|\.beat\(|\.hurt\(|\.stun\s*=", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stops the world, files a beat, "
                             "hurts or stuns (reading 8)")
        # WHAT THE ADDED CODE MAY DO, AND NOTHING ELSE (reading 8): the anchor each row re-emits
        # is taken out first. It calls no simulation verb but the one entangle, the design's own
        # line; it writes only the window, the tally, the clock and the three fields of Grasp's pin.
        added = strip_comments(new.replace(_old, "", 1) if _old and _old in new else new)
        # THE CALLS ARE AN ALLOWLIST, not a list of refusals (the v112 review's finding 2): every
        # `name(` in the added code is the window's ticker, the root, Math.max, the one entangle or
        # the `if` / `for` of the code itself -- or one of the two method headers. Anything else
        # (another verb, Object./Reflect., a call through a bracket or a call's result, `new`, an
        # arrow, a tagged template) refuses.
        banned = re.search(r"\b(Object|Reflect|Function|eval|globalThis|window|new)\b|=>|`|[\])]\s*\(",
                           added)
        if banned:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' uses {banned.group(0)!r}: the "
                             "root is a pin and an entangle, nothing else (reading 8)")
        for mc in re.finditer(r"(?:([\w$]+)\s*\.\s*)?([\w$]+)\s*\(", added):
            recv, name = mc.group(1), mc.group(2)
            if recv is None and name in KEYWORD_PAREN:
                continue
            if (recv, name) in CALL_OK:
                continue
            line = added[added.rfind("\n", 0, mc.start()) + 1:added.find("\n", mc.start())]
            if recv is None and name in METHOD_DEFS and re.fullmatch(r"  " + name + r"\(\w+\)\{", line):
                continue
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' calls "
                             f"{(recv + '.') if recv else ''}{name}(): the added code may call only "
                             f"{sorted(f'{r}.{n}' for r, n in CALL_OK)} (reading 8)")
        applies = re.findall(r"\.apply\([^;]*\)", added)
        if applies and applies != [APPLY_LINE]:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' applies {applies}: the only "
                             f"status is the design's entangle, {APPLY_LINE}")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", added):
            if (mw.group(1), mw.group(2)) not in WRITE_OK:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes "
                                 f"{mw.group(1)}.{mw.group(2)} (reading 8: the window, the tally, "
                                 "the clock and Grasp's pin only)")
        if re.search(r"\bdelete\b|\[[^\]]*\]\s*=(?!=)", added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' deletes or writes by index")
    s6_static_checks()                  # every stage: it reads the table (reading 22)
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    if len(re.findall(r'kind:"rootfast"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one rootfast ultimate")
    if 'kind:"freeze"' in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the freeze is still in Heartwood's row")
    if A.stage != "1" and out_code.count("this.rootBlow(self)") != 1:
        raise SystemExit("REFUSING TO WRITE -- the root is not called exactly once, from resolveHit")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one rootfast ultimate, Heartwood's; the freeze out of its row; no insert draws "
          f"the RNG, writes the shared weapon, touches pinFree, stops, beats or hurts; the added "
          f"code calls only {len(CALL_OK)} allowed calls and writes only WRITE_OK; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
