#!/usr/bin/env python
"""WIDOWMAKER / EXSANGUINATE, REDESIGNED -- the bleed drains into her. v106.

Built from `06-docs/v76/widowmaker-exsanguinate-redesign-v76.md` (Cowork,
2026-09-26), §5 its build brief, which is the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. A REDESIGN: the relic
ships in the base; its nova is replaced.

    stage 1   the ultimate stubbed      <tip> -> sc-widowmaker-stub.html
              the new ult block at charge 1e9 (the nova unreachable) -- the
              lab's arm A, fight for fight
    stage 2   the drain                 -> sc-widowmaker-drain.html
              the design's stage 1 ("the nova out, f.ultDrain in, tickStatus's
              branch"), the charge on the game's clock (the lab's arm B)
    stage 5   the blade                 -> sc-widowmaker-b<blade>.html
              the design's stage 2 ("the blade, wide on 151")
    stage 6   picture and voice         -> sc-widowmaker-b1075-fx.html
              the design's stage 3, on the final (stage 5's link). The carry is
              the orchestrator's: stages 1, 2, 5 and 6, then SPECS.widowmaker out
              of both fx.js copies by tools/fx_remove.py (reading 16), not here.

§1: "For a duration the enemy's bleeding drains into Widowmaker. Every tick of
Hemorrhage on the enemy heals her by the same amount. Her blades are
unchanged; the wound does the work."

Declared (v76 §2-§5):
  THE CAST     opens a window of `dur` seconds and resolves nothing: no
               damage, no knock, no stun, no status. The nova's radius, dmg,
               apply and knock are deleted from the row (§4: "the nova's
               `radius` and `apply` are deleted").
  THE DRAIN    in `tickStatus`'s dps branch: while her window is open, every
               hemorrhage tick on her opponent -- d = dps x stacks x dt x
               dmgTakenMul, the engine's own tick, untouched -- heals her by d,
               capped at her maxHp. hp and nothing else (§4: "Blessing is NOT
               used (this is hp, not a status)"): no float, no beat, no stop.
  THE BLADES   unchanged: the twinblade's blow and its onHit hemorrhage 2, to
               hemorrhage's own ceiling of 4, which the drain does not lift
               (reading 10).

THE CHARGE. The design states none; its lab cast every 16s of its own step
clock (`ult_overlay`'s default, `drain_full`'s P). Rick, 2026-09-27, for the
whole batch: "use the game's equivalent". Measured for this fighter on the
lab's arm B (v106 §0: the census).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE WINDOW IS 8s: the design says "for a duration" and names no number;
     its lab ran `ult_overlay`'s default window, 8, and that is what was
     priced (`drain_full`: dur 8.0).
  2. THE DRAINER IS THE BLEEDING FIGHTER'S OPPONENT. §4 reads `st.src` and
     says hemorrhage's source "is written by apply (since v66)". On this base
     it is not: only Corona's burn and the batch's ultimates write a source,
     and the blade's onHit apply passes none, so every hemorrhage stack in the
     game has `src` undefined. Writing one onto every blade's bleed would touch
     every bloodsworn relic's status. The build takes the engine's own
     attribution for hemorrhage instead -- tickStatus's fatal-tick beat:
     "hemorrhage and smite still fall back to the other fighter" -- which is
     also what the lab priced (it drained the opponent's whole bleed). `src
     !== f` holds by construction; a source, if a later build writes one, must
     name her.
  3. A SHADE'S BLEED DRAINS NOTHING. Twinshade's shades tick their own
     statuses; the lab's `foe` is the opponent, never a shade.
  4. A TICK ON A FIGHTER ALREADY DEAD DRAINS NOTHING (the kill flight keeps
     ticking a corpse); the killing tick itself drains ("every tick"). The lab
     drained neither; the fight is decided either way.
  5. THE WINDOW CLOSES BY ITS CLOCK OR ON A DEATH THAT `tickDrain` SEES (the
     lab's close is either death). A kill landed LATER in the same step -- a
     blow in `tickHits`, after the window tickers -- ends the match with the
     window still set: `step` runs no ticker after `over`, so that window
     never closes (about one window in eight; the probe counts them, [1]).
     Nothing in the simulation reads `ultDrain` after `over`; stage 6's thread,
     drawn off `ultDrain`, must stop at `over`.
  6. NO WAIT CLAUSE. The lab's schedule never opened a window on a running
     one, and at charge 14 against a window of 8 on one clock the engine
     cannot either; the probe asserts it ([8]), and that every cast comes
     exactly 14 s of her live clock after the last (the probe pins 14 and 8
     from ULT below, never from the row it tests).
  7. THE CARD IS WRITTEN AT STAGE 1 (the design lists it at its stage 2): the
     stub is the new ult block, and the nova's card would describe a cast that
     is gone. It is 62 characters (v76 §4 prints "(66)").
  8. THE NOVA'S PICTURE AND VOICE STILL PLAY AT THE CAST in stages 2-5: the
     burst of fangs keyed on `u.w === "widowmaker"`, `SPECS.widowmaker`'s burst
     field and the "wet slice" ult voice are keyed on the relic, not the kind.
     Stage 6 (the design's stage 3) retires them, as Corollary's stage 4
     retired Axiom's bolt art. Nothing in the simulation reads any of them.
     With `radius` gone from the row, fireUlt's ultFx record falls back to
     `u.radius || 300`, so the kept fang burst opens to 300 px, not 240,
     until stage 6 retires it (presentation only).
  9. HP AND NOTHING ELSE (§4: "Blessing is NOT used (this is hp, not a
     status)"; §5: "the drain files none"; §3: "Lifesteal is Triplicate's
     (umbral) and is not taken"): no status on her, no lifesteal, no float,
     no beat, no stop, no knock. The cast resolves nothing and keeps
     `fireUlt`'s common banner, 0.08 stop and ult beat. The builder refuses an
     insert that applies, beats, stops, floats or knocks; the probe's [6]
     (the cast moves nothing on either fighter), [7] (the drain tick files
     nothing) and [10] (the drain is her only heal: no Blessing, no lifesteal,
     her hp rising nowhere else).
  10. THE DRAIN LIFTS NO CAP. §6.3: "Whether the drain should ALSO lift her
     own cap (Bloodletting's 8) -- not priced; a second payoff on one ultimate
     ... and left out." That cap is the hemorrhage STACK ceiling --
     Bloodletting's `cap:8`, the bleeding fighter's `bleedCap`, recomputed in
     `tickSpectre` -- not her maxHp. The build lifts nothing: her foe's bleed
     ceiling stays hemorrhage's own 4 (no spectre of hers can stand to raise
     it), and the probe's [9] holds it from the definition. The heal's own cap
     at her maxHp is §2's ("heals `hp` by it, capped at `maxHp`"), the probe's
     [3]; her maxHp never moves.
  11. THE BLADE HOLDS THE SHIPPED WIN RATE (§3, §5 stage 2): the stage-5
     comment at TUNED below says how it was measured and what the band's 50
     would take instead (Rick's §6.2).

STAGE 6, THE PICTURE AND THE VOICE (the design's stage 3; v76 §4: "her shell
flushes dark red for 0.25s and a thin red thread appears from the foe's bleed
drips to her shell for as long as the foe bleeds inside the window ... a red
'+n' floats on her every 1 hp drained ... Close: the thread snaps. No new
object"; the voice "cast -- a low inhale, 0.4s", "the drain -- the bleed's own
drip voice reversed and pitched by the foe's stack count, quiet"). Picked on
measurements under Rick's "you pick i overrule" (v106 §5); the rows are the
labs', byte-exact. Declared:
  12. THE "+n" IS FILED IN `tickPresentation` (`tickSiphon`), NEVER IN
      `tickStatus`: "the drain files none" (§5), and the probe's [7] holds a
      drain tick to no float. One "+n" each time her drained total crosses a
      whole hp (hurt()'s rule: no float for a fraction).
  13. THE PICTURE FINDS THE CAST AND THE DRAIN BY WATCHING `drainTally` RISE
      (`casts`, `drained`), so neither `fireUlt` nor `tickStatus` makes a call
      for it. The one stage-6 call on the sim path is the drip VOICE, in
      tickStatus's drain block: once per whole hp crossed, n = the bleeding
      foe's hemorrhage stacks (a read). SFX.play draws nothing, writes nothing
      the simulation reads and returns on its first line with no audio context.
  14. THE THREAD IS READ OFF `ultDrain && !over`, both standing and the foe
      bleeding: about one window in eight is still set at `over` (reading 5),
      so the thread snaps at the verdict instead of hanging on the corpse.
  15. THE CLOSE HAS NO VOICE (v76 §4). Its picture is the snap -- on the
      clock, a death or the verdict alike.
  16. THE NOVA'S ART IS RETIRED (reading 8): drawUltOver's fang burst; the
      "wet slice" (its three lines replaced IN PLACE by the inhale, so the
      shared rune-crack fallback is untouched); the banner's fan and drops (the
      word now fills from the foot) and its spread entry. The ultFx `life`
      entry keeps its number, annotated as the cast's record (Daybreak's and
      Corollary's precedent). `SPECS.widowmaker`, the nova's particle field,
      is the one piece left: it leaves BOTH copies of fx.js at the carry, by
      the orchestrator's `tools/fx_remove.py` (fx.js is shared), and this
      builder edits neither -- stage 6 refuses if the inlined copy moved.
      Its three lines only: `fx_remove` as written also takes the comment
      directly above the entry, and that is the NOVAS section header, which
      heads Lightkeeper's and Censer's entries too (module stamp 024d7a84...
      with it, f710f845... without -- the picture lab's gated removal; v106
      §5b).
      `ULTSIG.widowmaker`, the charge sigil ("a drop, and a ring drawn INTO
      it"), is not named by the design and is kept.

WHAT IS RETIRED, and what is not. Widowmaker's nova block (radius 240, dmg 16,
apply hemorrhage 3, knock 200, its card) is deleted. `kind:"nova"` and its cast
branch stay: Bulwark and Consecration (Lightkeeper, Censer) still use them on
this base. The builder reads who is still a nova and never refuses on it: both
are being redesigned too, and either may be carried first. `Match.drain()` (the
lifesteal's mote stream) is a different thing with a similar name and is not
touched.

THE CLOCK. The window runs on the window tickers' clock, which stops through a
hit stop -- and so does the bleed it drains (`tickStatus` does not run in one).
The lab's window ran through freezes, and its drain paid a tick on frozen steps
where the engine's bleed does not tick at all (v106 §2 measures both).

THE BASE is asserted by content (the features this builder needs), never by
which relic is last, so the links re-apply onto a later tip that carries
other new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "widowmaker"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9).
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v106 §0)
    "dur": 8,         # the lab's window ("for a duration"; reading 1)
}
TIP = "Her foe's bleeding drains into her: every tick of it heals her"   # v76 §4
# THE SHIPPED ROW, the donor of every number this build keeps.
SHIP_HEAD = ('''  { id:"widowmaker", name:"Widowmaker", aff:"bloodsworn", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:11.95, spin:5.7, mode:"spin", mass:1.1,
    onHit:{ hemorrhage:2 },
''')
SHIP_ULT = ('''    ult:{ name:"Exsanguinate", charge:14, kind:"nova", radius:240, dmg:16, apply:{hemorrhage:3}, knock:200, tip:"Nova: deals 16 damage and applies 3 Hemorrhage stacks" },
''')


def ult_block(charge) -> str:
    return (f'''    /* EXSANGUINATE, REDESIGNED (v76; built v106): the nova is gone. For
       `dur` seconds her foe's bleeding drains into her -- every hemorrhage
       tick on the foe heals her by the same amount (tickStatus). */
    ult:{{ name:"Exsanguinate", charge:{charge}, kind:"drain", dur:{ULT["dur"]},
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
# THE NOVA OUT OF THE ROW, THE NEW BLOCK IN, STUBBED at charge 1e9: the clock
# can never reach it and `fireUlt` never runs, so this is the lab's arm A (the
# relic with its ultimate suppressed) and must equal it fight for fight.
S1 = [
("Exsanguinate's nova block out, the drain's block in, stubbed",
 SHIP_ULT,
 ult_block("1e9")),
]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the drain has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Exsanguinate", charge:1e9, kind:"drain", dur:8,
''',
 f'''    ult:{{ name:"Exsanguinate", charge:{ULT["charge"]}, kind:"drain", dur:{ULT["dur"]},   // v76 stage 1: the drain
'''),

("the fighter carries the drain's window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while EXSANGUINATE's window is open (v76). null on every other
       relic and on this one outside its window: `tickDrain` returns after a
       two-iteration loop that does nothing, and `tickStatus` reads it only on
       a hemorrhage tick. `drainTally` is the probe's count, cumulative over
       the fight; nothing in the simulation reads it. */
    this.ultDrain = null;
    this.drainTally = null;
'''),

("the foe's bleed drains into her, in tickStatus's dps branch",
 '''        const d = def.dps * st.stacks * dt * f.dmgTakenMul();
        f.hp -= d;
''',
 '''        const d = def.dps * st.stacks * dt * f.dmgTakenMul();
        f.hp -= d;
        /* EXSANGUINATE (v76): THE FOE'S BLEEDING DRAINS INTO WIDOWMAKER. While
           her window is open, every hemorrhage tick on her opponent heals her
           by the same amount, `d`, capped at her maxHp -- hp and nothing else:
           no status (Blessing is not used), no float, no beat, no stop. The
           tick itself is read, never changed.
           THE DRAINER IS THE BLEEDING FIGHTER'S OPPONENT, the engine's own
           attribution for hemorrhage (the fatal-tick beat below: "hemorrhage
           and smite still fall back to the other fighter"). v76 §4 reads
           `st.src`, but no hemorrhage on this base carries one (the blade's
           onHit apply passes none); a source, if a later build writes one,
           must name her. A shade's bleed drains nothing, and neither does a
           tick on a fighter already dead. `ultDrain` is null on every other
           relic and outside her window. */
        if (key === "hemorrhage" && hp0 > 0){
          const me = f === this.a ? this.b : f === this.b ? this.a : null;
          if (me && me.ultDrain && me.alive
              && (!st.src || st.src === (me === this.a ? "a" : "b"))){
            const h0 = me.hp;
            me.hp = Math.min(me.maxHp, me.hp + d);
            me.drainTally.ticks++;
            me.drainTally.drained += me.hp - h0;
          }
        }
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "drain"){
      /* EXSANGUINATE (v76). NOTHING RESOLVES HERE: no damage, no knock, no
         stun, no status -- the nova's radius, dmg, apply and knock are gone
         from the row. The cast opens the window for `u.dur` seconds, and
         `tickStatus` pays the drain while it is open. */
      f.ultDrain = { t: 0, dur: u.dur };
      if (!f.drainTally)
        f.drainTally = { casts: 0, frames: 0, foeStk: 0, ticks: 0, drained: 0 };
      f.drainTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the window ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickDrain(dt);                 // EXSANGUINATE (v76)
'''),

("tickDrain keeps the window's clock",
 '''  tickWinnow(dt){
''',
 '''  /* ============================================== EXSANGUINATE ========
     v76 §1/§4. The window's clock and nothing else: the drain itself is in
     `tickStatus`'s dps branch, where the tick is. On the window tickers'
     clock, so it stops through a hit stop, as the bleed it drains does. The
     window closes by its clock or on a death this ticker sees. A kill landed
     later in the same step (`tickHits`) ends the match with the window still
     set: `step` runs no ticker after `over`, and nothing in the simulation
     reads `ultDrain` then -- a picture drawn off it must stop at `over`.
     The probe's window-frame counts live here; nothing in the simulation
     reads them. */
  tickDrain(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultDrain;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; continue; }
      f.drainTally.frames++;
      f.drainTally.foeStk += foe.stacks("hemorrhage");
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE HOLDS THE SHIPPED WIN RATE. The design says so three times: §3
# "The build settles it wide on 151 to the SHIPPED win rate, not to 50 -- a
# redesign keeps the fighter where it was"; §5 stage 2 "the blade, wide on 151
# at 10.5 / 10.75 / 11, target the SHIPPED win rate (~46-50)"; the v87
# handoff "~10.7". §6.2 leaves the target to Rick ("the shipped 46 or the
# band's 50"), so the build takes the design's own default and flags the other.
# The design names no other knob, and none moved.
# Both sides, two blocks, 1480 fights a point (relic_rate, every other relic a
# foe): 10.5 -> 46.1, 10.75 -> 47.0, 11 -> 49.2, 11.25 -> 51.5, 11.95 -> 55.5;
# the shipped relic (the nova, 11.95) reads 46.7 on the same fights. 10.75 is
# the measured point nearest the shipped 46.7 (+0.3; 10.5 is -0.6), inside the
# brief's 10.5 / 10.75 / 11, the design's "~10.6-10.8" and the twinblade row
# (8.3-11.95). THE BAND'S 50 INSTEAD is 11 (49.2, the measured point nearest
# the crossing, ~11.1): Rick's other choice under §6.2, one number here.
TUNED = {"dmg": 10.75}

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v76 §4; the design's stage 3), picked on
# measurements under Rick's "you pick i overrule" by the picture lab and
# `widowmaker_voice_lab.py` (v106 §5). PRESENTATION ONLY: engine_ab over all
# 38 relics, Widowmaker included, is the proof, and the probe's [11]-[12] read
# the voices and the picture's hook inside the fight. The rows are byte-exact
# to the labs' own files (voice ff78068cbe2fa1f2, 2 rows; picture
# 42121c10265e101c, 10 rows); the picture rows alone reproduce the picture
# lab's stamp (518477d4537ec077), the voice rows alone the voice lab's page
# (373f16b7e0a85770), and the two sets give the same bytes in either order.
#   THE VOICE: the cast's inhale REPLACES the nova's "wet slice" arm in place
#   (the shared rune-crack fallback is not touched); the drain's reversed drip
#   is the one call stage 6 puts on the sim path -- tickStatus's drain block,
#   once per whole hp drained, n = the bleeding foe's hemorrhage stacks. The
#   close plays nothing.
#   THE PICTURE: `tickSiphon` in tickPresentation reads `drainTally` rising
#   (casts: the flush; drained: the "+n") and `ultDrain && !over` (the
#   thread; the snap at the close), and writes only its own `siphon*` fields
#   and `floats`. The thread is drawn in the world pass under both balls, the
#   flush over them. The nova's art is retired: drawUltOver's fang burst, the
#   banner's fan and drops (the word fills) and its spread entry; the ultFx
#   `life` entry keeps its number (the cast's record). No fx.js edit:
#   `SPECS.widowmaker` leaves BOTH copies at the carry by `tools/fx_remove.py`
#   (reading 16).
S6 = [

("Sfx: Exsanguinate's inhale and drain arms, replacing the nova's wet slice",
 '''        } else if (w === "widowmaker"){                 // a wet slice
          this._burst(t, { freq: 3400, q: 1.6, gain: 0.34, dur: 0.20 });
          this._tone (t, { freq: 900, to: 240, gain: 0.20, dur: 0.28, type:"sawtooth" });
          this._tone (t + 0.10, { freq: 620, to: 180, gain: 0.14, dur: 0.34, type:"sawtooth" });''',
 '''        } else if (w === "widowmaker"){                 // she draws breath
          /* EXSANGUINATE'S CAST, THE INHALE -- v76 §4: "cast -- a low inhale,
             0.4s". MID, of 14, picked on the numbers by
             `widowmaker_voice_lab.py` under Rick's "you pick i overrule"
             (v106). It REPLACES the nova's "wet slice" -- the three lines that
             were this arm -- which the redesign retires with the nova (v106
             §5); nothing else in the synth moved.

             A low breath drawn in: a swell of lowpassed air (its cutoff 210 ->
             560 Hz, the longest attack a `_sweep` allows) and, on its top, the
             draw (420 -> 1120 Hz), decaying over the rest of its 0.58 s. It is
             drawn IN: its band rises +1011 cents from its first 100 ms to its
             last. It swells to its top (the last 10 -> 90% in 80 ms), never
             dips on the way up and never grows again after it; its power
             centres at 301-366 Hz on every noise draw (low), and in no 50 ms
             of it does a peak stand more than 3.3 dB over its neighbours (air,
             not a note). Audible 400 ms; its loudest 50 ms -2.8 dB re
             Widowmaker's blow. Register at most 0.79 against rune-crack, the
             bloodsworn and twinblade casts, the tornado's woosh, the
             bowstring, the blow and the death voice. */
          const g = 0.5386;
          this._sweep(t, { f0: 210, f1: 560, q: 0.7, gain: g, dur: 0.5765, atk: 0.338, type:"lowpass" });
          this._sweep(t + 0.3181, { f0: 420, f1: 1120, q: 0.7, gain: g, dur: 0.5765, atk: 0.0199, type:"lowpass" });
        } else if (w === "widowmaker-drain"){           // a drop drawn back up
          /* THE DRAIN -- "the bleed's own drip voice reversed and pitched by
             the foe's stack count, quiet" (v76 §4). TRI, of 5
             (`widowmaker_voice_lab.py`). The bleed has no drip voice, so the
             lab made one -- a drop into a pool, a sine chirping up 1.5x over
             0.12 s -- and this is its REVERSE: a triangle sliding down a fifth
             onto the note as it swells, and stopping. `tickStatus` plays it
             once per whole hp drained, with n = the bleeding foe's hemorrhage
             stacks (1-4).

             A held or rising note does not exist in this toolkit (CLAUDE.md
             4.5), so the swell is re-struck at every cycle of the falling
             chirp, on the chirp's own whole cycles, `.frequency.value` set on
             each (v97); each strike decays over Ds and is scaled by (1 - q) so
             the strikes sum to the drip's own exponential, run upwards from 40
             dB under its top. It lands on 880 / 1047 / 1175 / 1319 Hz at
             counts 1-4 (measured within 57 cents), falling 284 cents onto it;
             audible 75-80 ms, its loudest 5 ms in the last 14% of it, ENV-CORR
             0.95 with the drip's own samples reversed; 122 strikes at count 4.
             Quiet: its loudest 50 ms -11.3 to -10.7 dB re the blow, +8.3 dB or
             more re the wall tick; register at most 0.51 against the blow, the
             wall tick, the heal (spark), the fork, the hex snap, Zenith's
             tick, rune-crack and the cast. The close plays nothing (v76 §4). */
          const n = clamp(Math.round(p.n || 1), 1, 4), f = 880 * Math.pow(2, [0, 3, 5, 7][n - 1] / 12);
          const g = 0.09989, D = 0.12, R = 1.5, Ds = 0.02, u0 = D * (1 - 2 / Math.log10(g / 0.0001));
          const fs = f * R, Lg = Math.log(1 / R);
          for (let k = Math.ceil(fs * D * (Math.pow(R, -u0 / D) - 1) / Lg); ; k++){
            const u = D / Lg * Math.log(1 + k * Lg / (fs * D));
            if (!(u < D)) break;
            const fu = fs * Math.pow(R, -u / D), q = Math.pow(10, -4 / (fu * Ds));
            const a = g * Math.pow(0.0001 / g, 1 - u / D) * (1 - q), d = Ds * Math.log10(a / 0.0001) / 4;
            if (!(d > 0)) continue;
            const o = this._tone(t + u - u0, { freq: fu, to: fu * Math.pow(R, -d / D), gain: a, dur: d, type:"triangle" });
            o.frequency.value = fu; o.stop(t + u - u0 + d);
          }'''),

("tickStatus: the drain's drip, once per whole hp drained, after the gain is booked",
 '''            me.drainTally.drained += me.hp - h0;''',
 '''            const k0 = Math.floor(me.drainTally.drained);
            me.drainTally.drained += me.hp - h0;
            /* EXSANGUINATE'S DRIP (v76 §4: "the drain -- the bleed's own drip
               voice reversed and pitched by the foe's stack count, quiet"): one
               reversed drip each time the running total crosses a whole hp --
               the unit of the drain's "+n" (§4) -- pitched by the bleeding
               foe's hemorrhage stacks. `k0` is a local; the total is read, not
               written. Presentation only: SFX.play draws nothing, is a no-op
               headless, and nothing here is read back (widowmaker_voice_lab:
               fights identical). */
            if (Math.floor(me.drainTally.drained) > k0)
              SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") });'''),

('exsanguinate picture: fighter fields',
 '''    this.ultDrain = null;
    this.drainTally = null;
''',
 '''    this.ultDrain = null;
    this.drainTally = null;
    /* EXSANGUINATE'S PICTURE (v76 section 4), and none of it is the sim's:
       the thread outlives `ultDrain` by the snap, and the flush is a clock
       of its own. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickSiphon`); nothing in the simulation reads any of it.
         siphonFade -- the thread's reach, 0 at the foe's drip to 1 at her
                       shell: up while the foe bleeds inside the window
         siphonAge  -- the presentation clock since the cast (the flush)
         siphonSeen -- `drainTally.casts`, as last seen (a cast is it rising)
         siphonHp   -- the whole hp of `drainTally.drained` already floated
         siphonSide -- which end of the drips' arc the thread leaves from
                       while she is above the foe (held, so it cannot flick)
         siphonSnap -- the close: where the thread hung when it snapped */
    this.siphonFade = 0;
    this.siphonAge = 99;
    this.siphonSeen = 0;
    this.siphonHp = 0;
    this.siphonSide = 1;
    this.siphonSnap = null;
'''),

('exsanguinate picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickSiphon(dt);               // EXSANGUINATE'S PICTURE (v76 section 4)
'''),

('exsanguinate picture: tickSiphon',
 '''  tickWinnow(dt){
''',
 '''  /* --------------------------------------------- EXSANGUINATE'S PICTURE ---
     v76 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.5 is the
     cast's 0.25s flush, 0.24 the thread's 0.12s reach, 0.3 its 0.15s draw
     back when the foe stops bleeding, 0.6 the close's 0.3s snap. THE CAST
     IS FOUND BY WATCHING `drainTally.casts` RISE and THE DRAIN BY WATCHING
     `drainTally.drained` RISE, so neither `fireUlt` nor `tickStatus` makes a
     call for the picture. THE THREAD IS READ OFF `ultDrain && !over`, with
     both fighters standing and the foe bleeding: `tickDrain` never runs again
     once `over` is set, and about one window in eight is still set when the
     match ends (the kill lands in `tickHits`, after `tickDrain`), so the
     thread snaps at the verdict instead of hanging through the panel.
     THE "+n" IS THE ENGINE'S OWN `float`, filed HERE and never in
     `tickStatus` -- "the drain files none" -- one each time the fight's
     drained total crosses a whole hp (`hurt`'s rule: no float for a
     fraction). Writes presentation fields and `floats` only; no rng. */
  tickSiphon(dt){
    for (const f of [this.a, this.b]){
      const T = f.drainTally;
      if (!T) continue;                                       // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      if (T.casts !== f.siphonSeen){ f.siphonSeen = T.casts; f.siphonAge = 0; }   // a cast
      else if (f.siphonAge < 99) f.siphonAge += dt;
      /* the side of the drips' arc the thread leaves from while she is above
         the foe, held until she is 0.3 rad past the top */
      const th = Math.atan2(f.y - foe.y, f.x - foe.x);
      if (th > -1.2708 && th < 1.5708) f.siphonSide = 1;
      else if (th < -1.8708 || th > 1.5708) f.siphonSide = -1;
      const open = !!f.ultDrain && !this.over && f.alive && foe.alive;
      if (open && foe.stacks("hemorrhage") > 0) f.siphonFade = Math.min(1, f.siphonFade + dt / 0.24);
      else if (open) f.siphonFade = Math.max(0, f.siphonFade - dt / 0.3);
      else if (f.siphonFade > 0){
        /* THE CLOSE -- the clock, a death, or the verdict: the thread snaps
           where it hangs */
        f.siphonSnap = { t: 0, fx: foe.x, fy: foe.y, sx: f.x, sy: f.y, side: f.siphonSide,
                         g: 1 - (1 - f.siphonFade) * (1 - f.siphonFade) };
        f.siphonFade = 0;
      }
      if (f.siphonSnap){
        f.siphonSnap.t += dt;
        if (f.siphonSnap.t >= 0.6) f.siphonSnap = null;
      }
      const w = Math.floor(T.drained);
      if (w > f.siphonHp){
        const n = w - f.siphonHp;
        f.siphonHp = w;
        this.float(f.x + (shellHash(1931, w) - 0.5) * 16, f.y - 42, "+" + n, "#FF4F63", 30 + n * 0.7);
      }
    }
  }

  tickWinnow(dt){
'''),

("exsanguinate picture: the thread's call (world, under both balls)",
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* EXSANGUINATE'S THREAD (v76 section 4): from the foe's bleed drips to
       her shell, its beads, and its snap at the close. The WORLD pass and
       under both balls, rim to rim: nothing of it is inside a shell, and
       nothing of it reaches the bloom. */
    if (__world) this.drawSiphon(m);
'''),

("exsanguinate picture: the flush's call (world, over both fighters)",
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* EXSANGUINATE'S FLUSH, ON her shell (v76 section 4: "her shell flushes
       dark red for 0.25s"): over both fighters, world pass, a darkening. */
    this.drawSiphonTop(m);
'''),

('exsanguinate picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ================================================ EXSANGUINATE ======
     v76 section 4: "her shell flushes dark red for 0.25s and a thin red
     thread appears from the foe's bleed drips to her shell for as long as
     the foe bleeds inside the window -- the 'drains into her' line (Zenith's
     heal thread, in blood) ... a red '+n' floats on her every 1 hp drained
     ... Close: the thread snaps. No new object."

     THE THREAD leaves the foe's shell on the drips' own arc (`_stBleed`:
     0.44 to PI - 0.44, the underside), at the point of it nearest her, and
     curves out of the wound before it turns for her, so it never crosses the
     foe. It reaches her in 0.12s at the cast (or when the foe starts
     bleeding), and draws back into the wound in 0.15s when the foe stops.
     THREE BEADS RUN DOWN IT, placed by her drained total, so they move only
     when a tick pays her -- faster with more stacks, still at her full hp,
     frozen in a hit stop -- and one enters her shell per whole hp, on the
     frame its "+1" floats. THE CLOSE: it breaks at its middle, the two
     halves whip back into the wound and into her with a bead on each torn
     end, and the tear throws six short strands and five drops that fall.

     IT HANGS OFF THE FIGHTER (`siphonFade`, `siphonSnap`, `siphonAge`),
     never `m.ultFx` (open item 25). World pass: the thread under both balls,
     the flush over them. PRESENTATION ONLY: no rng, no spawnFx, no
     Math.random (shellHash), and nothing here writes a field the simulation
     reads. */
  drawSiphon(m){
    const a = m.a, b = m.b;
    if (!(a.siphonFade > 0) && !(b.siphonFade > 0) && !a.siphonSnap && !b.siphonSnap) return;   // <- zero burden
    const c = this.ctx;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.siphonFade > 0) this._siphonThread(c, f, f === a ? b : a);
      if (f.siphonSnap) this._siphonSnap(c, f);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* the thread's four points, the foe's drip to her rim; null when the
     shells are too close for a line */
  _siphonPath(fx, fy, sx, sy, side){
    const R = CONFIG.physics.ballR, dx = sx - fx, dy = sy - fy, d = Math.hypot(dx, dy);
    if (d < 2 * R + 10) return null;
    const th = Math.atan2(dy, dx), lo = 0.44, hi = Math.PI - 0.44;
    const a0 = th >= lo && th <= hi ? th : th >= 0 ? (th < lo ? lo : hi) : (side < 0 ? hi : lo);
    const ca = Math.cos(a0), sa = Math.sin(a0), L1 = Math.min(70, d * 0.34);
    const x0 = fx + ca * R, y0 = fy + sa * R, x1 = x0 + ca * L1, y1 = y0 + sa * L1;
    let ex = x1 - sx, ey = y1 - sy;
    const el = Math.hypot(ex, ey) || 1, L2 = Math.min(44, d * 0.22);
    ex /= el; ey /= el;
    return [x0, y0, x1, y1, sx + ex * (R + L2), sy + ey * (R + L2), sx + ex * R, sy + ey * R];
  }

  _siphonAt(P, t){
    const u = 1 - t, k0 = u * u * u, k1 = 3 * u * u * t, k2 = 3 * u * t * t, k3 = t * t * t;
    return [k0 * P[0] + k1 * P[2] + k2 * P[4] + k3 * P[6], k0 * P[1] + k1 * P[3] + k2 * P[5] + k3 * P[7]];
  }

  /* the stretch [t0, t1] of the thread, stroked dark then red */
  _siphonCord(c, P, t0, t1, al){
    if (!(t1 > t0 + 0.002)) return;
    c.beginPath();
    for (let i = 0; i <= 18; i++){
      const q = this._siphonAt(P, t0 + (t1 - t0) * i / 18);
      i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1]);
    }
    c.globalAlpha = 0.9 * al; c.strokeStyle = "#4A0810"; c.lineWidth = 3.4; c.stroke();
    c.globalAlpha = al; c.strokeStyle = "#E0283F"; c.lineWidth = 1.5; c.stroke();
  }

  _siphonThread(c, f, foe){
    const P = this._siphonPath(foe.x, foe.y, f.x, f.y, f.siphonSide);
    if (!P) return;
    const g = 1 - (1 - f.siphonFade) * (1 - f.siphonFade);        // its reach, eased out
    this._siphonCord(c, P, 0, g, 1);
    this._siphonBeads(c, f, P, g);
  }

  /* the beads, placed by her drained total: one enters her per whole hp */
  _siphonBeads(c, f, P, g){
    const D = f.drainTally ? f.drainTally.drained : 0;
    for (let j = 0; j < 3; j++){
      const q = ((D + j) / 3) % 1;
      if (q > g) continue;
      const p = this._siphonAt(P, q), s = Math.min(1, q / 0.08, (1 - q) / 0.08);
      c.globalAlpha = s;
      c.fillStyle = "#F03A52";
      c.beginPath(); c.arc(p[0], p[1], 3.1, 0, TAU); c.fill();
      c.strokeStyle = "#4A0810"; c.lineWidth = 1.1; c.stroke();
    }
  }

  _siphonSnap(c, f){
    const S = f.siphonSnap, k = S.t / 0.6;
    if (!(k < 1)) return;
    const P = this._siphonPath(S.fx, S.fy, S.sx, S.sy, S.side);
    if (!P) return;
    const e = 1 - (1 - k) * (1 - k) * (1 - k), mid = S.g * 0.5, al = 1 - k;
    this._siphonCord(c, P, 0, mid * (1 - e), al);                  // into the wound
    this._siphonCord(c, P, mid + (S.g - mid) * e, S.g, al);        // and into her
    /* the two torn ends, each a bead running home */
    c.fillStyle = "#F03A52";
    for (const t of [mid * (1 - e), mid + (S.g - mid) * e]){
      const p = this._siphonAt(P, t);
      c.globalAlpha = al; c.beginPath(); c.arc(p[0], p[1], 3.1, 0, TAU); c.fill();
    }
    /* the tear: six short strands flying off the break, and five drops falling */
    const q = this._siphonAt(P, mid), tt = S.t * 0.5;             // seconds
    if (k < 0.5){
      const kk = k / 0.5;
      c.globalAlpha = 1 - kk; c.strokeStyle = "#E0283F"; c.lineWidth = 1.6;
      c.beginPath();
      for (let i = 0; i < 6; i++){
        const an = i * TAU / 6 + shellHash(1947, i), r0 = 3 + 12 * kk, r1 = r0 + 7 * (1 - kk);
        c.moveTo(q[0] + Math.cos(an) * r0, q[1] + Math.sin(an) * r0);
        c.lineTo(q[0] + Math.cos(an) * r1, q[1] + Math.sin(an) * r1);
      }
      c.stroke();
    }
    for (let i = 0; i < 5; i++){
      c.globalAlpha = al;
      c.beginPath();
      c.arc(q[0] + (shellHash(1941, i) - 0.5) * (8 + 90 * tt),
            q[1] - 60 * tt * shellHash(1943, i) + 420 * tt * tt, 2.6, 0, TAU);
      c.fill();
    }
  }

  /* ...and the cast's flush on her shell, over both fighters (see
     `drawSiphon`). It keeps the shells' layer: `a` is drawn over `b`, so
     when she is `b` the foe's shell is cut out of it. */
  drawSiphonTop(m){
    const a = m.a, b = m.b;
    if (!(a.siphonAge < 0.5) && !(b.siphonAge < 0.5)) return;   // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    c.save();
    for (const f of [a, b]){
      if (!(f.siphonAge < 0.5) || !f.alive) continue;
      const k = f.siphonAge / 0.5, env = k < 0.18 ? k / 0.18 : 1 - (k - 0.18) / 0.82;
      c.save();
      if (f === b && a.alive){
        c.beginPath();
        c.rect(f.x - R - 2, f.y - R - 2, 2 * R + 4, 2 * R + 4); c.arc(a.x, a.y, R, 0, TAU);
        c.clip("evenodd");
      }
      const g = c.createRadialGradient(f.x, f.y, 0, f.x, f.y, R - 1);
      g.addColorStop(0, "rgba(96,8,22," + (0.55 * env).toFixed(3) + ")");
      g.addColorStop(1, "rgba(70,4,14," + (0.82 * env).toFixed(3) + ")");
      c.fillStyle = g;
      c.beginPath(); c.arc(f.x, f.y, R - 1, 0, TAU); c.fill();
      c.restore();
    }
    c.restore();
  }

  drawMotes(m){
'''),

("exsanguinate picture: the nova's burst retired",
 '''    /* ---- Exsanguinate: a burst of blades, then the blood is drawn out */
    else if (u.w === "widowmaker"){
      const ex = clamp(u.t / 0.34, 0, 1);
      const fade = 1 - clamp((u.t - 0.3) / 0.75, 0, 1);
      const rad = u.radius * (1 - Math.pow(1 - ex, 2.2));
      const N = 14;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 2.2;
        const bx = u.x + Math.cos(a) * rad, by = u.y + Math.sin(a) * rad;
        c.save();
        c.translate(bx, by); c.rotate(a + Math.PI / 2 + u.t * 6);
        c.globalAlpha = fade * (1 - ex * 0.35);
        c.fillStyle = "#E03A4E";
        c.shadowColor = "#FF97A2"; c.shadowBlur = 14;
        c.beginPath();                                    // a crescent fang
        c.moveTo(0, -13); c.quadraticCurveTo(9, 0, 0, 13);
        c.quadraticCurveTo(3.4, 0, 0, -13);
        c.fill();
        c.restore();
      }
      c.globalAlpha = fade * 0.9;
      c.strokeStyle = "#E03A4E"; c.lineWidth = 5 * (1 - ex * 0.7);
      c.shadowColor = "#E03A4E"; c.shadowBlur = 20;
      c.beginPath(); c.arc(u.x, u.y, rad, 0, TAU); c.stroke();
      c.shadowBlur = 0;
      /* threads of blood pulled back to the caster */
      if (u.hit && u.t > 0.22){
        const p = clamp((u.t - 0.22) / 0.9, 0, 1);
        for (let i = 0; i < 5; i++){
          c.globalAlpha = (1 - p) * 0.85;
          c.strokeStyle = "#8E1226"; c.lineWidth = 2.4;
          this._jag(c, tgt.x, tgt.y, src.x, src.y, 8, 30, 77 + i, 1);
          const q = (p * 1.4 + i * 0.2) % 1;
          const bx = lerp(tgt.x, src.x, q), by = lerp(tgt.y, src.y, q);
          c.globalAlpha = (1 - p) * 0.95;
          c.fillStyle = "#E03A4E";
          c.beginPath(); c.arc(bx, by, 4.2, 0, TAU); c.fill();
        }
      }
    }
''',
 '''    /* ---- EXSANGUINATE'S BURST OF BLADES IS RETIRED WITH THE NOVA (v76; built
       v106): the fang ring, its 300-unit sweep and the threads pulled back
       off the quarry were the nova's. The drain draws off the FIGHTER
       (`drawSiphon`), where the one ultFx slot cannot erase it. */
'''),

("exsanguinate picture: the ultFx life entry retired to the cast's record",
 '''      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
''',
 '''      /* EXSANGUINATE (v106) IS NO LONGER A SET-PIECE ON THIS SLOT either.
         Its window is drawn off the fighter (`drawSiphon`, `drawSiphonTop`),
         where the one slot cannot erase it; the burst of blades that read
         this record is retired and its field spec is out, so its entry
         below carries the CAST's record and nothing draws from it -- as
         for Daybreak and Corollary. The number is kept: the record's
         lifetime is the cast's, and changing it would move nothing drawn. */
      life: { dawnbringer: 1.6, widowmaker: 1.3, grudgebearer: 1.7,
'''),

("exsanguinate picture: the banner's spread",
 '''    const spread = { widowmaker: 52, thornwake: 64, gravemourn: 30,
''',
 '''    const spread = { thornwake: 64, gravemourn: 30,
'''),

("exsanguinate picture: the banner's letters fill",
 '''    else if (b.w === "widowmaker"){
      fn = (i, N) => ({ dx: (i - (N - 1) / 2) * (1 - ease(inK)) * 52 * k });
      if (out > 0){
        c.save();
        c.shadowBlur = 0; c.globalAlpha = out * 0.85;
        c.strokeStyle = "#8E1226"; c.lineWidth = 3 * k; c.lineCap = "round";
        for (let i = 0; i < 9; i++){
          const dx = (H(31, i) - 0.5) * w46 * scale;
          c.beginPath();
          c.moveTo(cx + dx, y + 8 * k);
          c.lineTo(cx + dx, y + (8 + out * out * (26 + H(37, i) * 50)) * k);
          c.stroke();
        }
        c.restore();
      }
    }
''',
 '''    else if (b.w === "widowmaker"){
      /* EXSANGUINATE (v76; built v106). The fan the letters were thrown out
         of was the nova's burst, and the drops that ran off the word were
         the blood leaving; both are retired with it. THE WORD FILLS: every
         letter is there in its outline from the first frame and the red
         rises in it from the foot, left to right -- a level coming up, which
         is what the drain does to her. The letters are drawn here, the fill
         clipped; `_letters` is handed a zero alpha. */
      c.font = `700 ${size}px 'Atkinson Hyperlegible Next',sans-serif`;
      const ws = [];
      let tot = -track;
      for (const ch of b.text){ const w = c.measureText(ch).width; ws.push(w); tot += w + track; }
      let lx0 = cx - tot / 2;
      const top = cy - size * 0.8, bot = cy + size * 0.26;
      for (let i = 0; i < N; i++){
        const lx = lx0 + ws[i] / 2, v = clamp((age - 0.02 - i * 0.014) / 0.18, 0, 1);
        const e = 1 - (1 - v) * (1 - v), lev = bot - (bot - top) * e;
        c.strokeText(b.text[i], lx, cy);
        c.fillStyle = "#3A0610";
        c.fillText(b.text[i], lx, cy);
        c.fillStyle = col;
        if (e > 0){
          c.save();
          c.beginPath(); c.rect(lx - ws[i], lev, ws[i] * 2, bot - lev + size * 0.1); c.clip();
          c.fillText(b.text[i], lx, cy);
          c.restore();
        }
        lx0 += ws[i] + track;
      }
      fn = () => ({ a: 0 });
    }
'''),

]

STAGE_OUT = {"1": "sc-widowmaker-stub", "2": "sc-widowmaker-drain", "5": "sc-widowmaker-b1075",
             "6": "sc-widowmaker-b1075-fx"}

# STAGE 6'S NAMES, free on the base on identifier boundaries (`drawSiphon` is a
# prefix of `drawSiphonTop`), and what its inserts may write: their own
# `siphon*` fields, the snap's clock, the canvas and the synth's own nodes, and
# the banner's local widths. Everything else is the simulation's.
S6_NAMES = ("tickSiphon", "drawSiphon", "drawSiphonTop", "_siphonPath", "_siphonAt", "_siphonCord",
            "_siphonThread", "_siphonBeads", "_siphonSnap", "siphonFade", "siphonAge", "siphonSeen",
            "siphonHp", "siphonSide", "siphonSnap", "widowmaker-drain")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("siphon") or (obj, prop) in {("siphonSnap", "t"),
                                                                             ("frequency", "value")}
               or obj == "c")
S6_ARRAY_OK = (lambda obj: obj == "ws")
S6_DRIP = 'SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") });'


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies, tools/fx_remove.py)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


S5 = [
("the blade: to the shipped win rate",
 SHIP_HEAD,
 SHIP_HEAD.replace("dmg:11.95,", f"dmg:{TUNED['dmg']},")),
]


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
    ap.add_argument("--stage", choices=["1", "2", "5", "6"], required=True)
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
    if not out_p.name.startswith("sc-widowmaker"):
        raise SystemExit(f"a link of this build is named sc-widowmaker*: {out_p.name}")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"{out_p.name} is already a link on the chain -- pick "
                         "another name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nWIDOWMAKER / EXSANGUINATE -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The features this builder needs, never which relic
    # is last: the shipped Widowmaker row (the blade, the channel), the
    # hemorrhage tick in tickStatus's dps branch and its fall-back attribution,
    # the status source contract, and the four anchors the inserts compose on.
    head = SHIP_HEAD if A.stage != "6" else SHIP_HEAD.replace("dmg:11.95,", f"dmg:{TUNED['dmg']},")
    if head not in s0:
        raise SystemExit("wrong base: Widowmaker's row (twinblade, "
                         + ("11.95" if A.stage != "6" else f"stage 5's {TUNED['dmg']}")
                         + ", hemorrhage 2) has moved")
    if not re.search(r'hemorrhage:\s*\{ name:"Hemorrhage", maxStacks:4, dur:3\.2, dps:1\.5,', code):
        raise SystemExit("wrong base: STATUS.hemorrhage is not dps 1.5")
    if not re.search(r"if \(def\.dps && key !== \"blessing\"\)\{\s*const hp0 = f\.hp;\s*"
                     r"const d = def\.dps \* st\.stacks \* dt \* f\.dmgTakenMul\(\);\s*f\.hp -= d;", code):
        raise SystemExit("wrong base: tickStatus's dps tick is not the one this "
                         "builder reads")
    if "(f === this.a ? this.b : this.a);" not in code or "apply(key, n, src){" not in code:
        raise SystemExit("wrong base: the status source contract or the tick's "
                         "fall-back attribution has moved")
    for anchor in ('    if (u.kind === "tendril"){\n',
                   '    this.tickTendril(dt);               // TENDRIL (v68)\n',
                   '  tickWinnow(dt){\n', '    this.vineTally = null;\n'):
        if s0.count(anchor) != 1:
            raise SystemExit(f"wrong base: anchor {anchor.strip()!r} is not there "
                             "exactly once")
    # THE NOVA STAYS FOR THE OTHERS (what is retired is Widowmaker's row only).
    # This build touches none of the nova's code (the drain's branch returns
    # before the generic tail), so it needs no other relic to be a nova. It
    # READS who still is and never refuses on it: Lightkeeper's redesign
    # (Bulwark) and Censer's (Consecration) take their relics off the nova too,
    # and either may be carried first.
    novas = [nv for nv in re.findall(r'\{ id:"([a-z]+)", name:"', code)
             if nv != RELIC and 'kind:"nova"' in relic_row(code, nv)]
    # THE NAMES THIS RELIC ADDS ARE FREE ON THE BASE. (`drain(` is the
    # lifesteal's mote stream, `this.drains` its list: neither is used here.)
    if A.stage == "1":
        for name in ("ultDrain", "drainTally", "tickDrain", 'kind:"drain"', '"drain"'):
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  Widowmaker's shipped row, the hemorrhage tick, the source "
          "contract and the four anchors hold; the nova's tail kept, untouched, "
          "for " + (", ".join(novas) if novas else "no other relic"))

    if A.stage == "1":
        if SHIP_ULT not in s0:
            raise SystemExit("this source does not carry the shipped nova -- built?")
        edits, want = S1, ult_block("1e9")
    elif A.stage == "2":
        if 'kind:"drain", dur:' not in code or "charge:1e9, kind:\"drain\"" not in code:
            raise SystemExit("stage 2 goes on stage 1")
        if "ultDrain" in code:
            raise SystemExit("this source already carries stage 2 -- built")
        edits, want = S2, ult_block(ULT["charge"])
    elif A.stage == "5":
        if f'charge:{ULT["charge"]}, kind:"drain"' not in code or "tickDrain(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want = S5, ult_block(ULT["charge"])
    else:
        # STAGE 6 GOES ON STAGE 5, ONCE: the drain at its charge, the blade
        # TUNED names, none of stage 6's names in the source yet (on identifier
        # boundaries), and the picture's hash function there to read.
        if (f'charge:{ULT["charge"]}, kind:"drain"' not in code or "tickDrain(dt){" not in code
                or f'dmg:{TUNED["dmg"]},' not in relic_row(code, RELIC)):
            raise SystemExit("stage 6 goes on stage 5 (the drain, at the blade TUNED names)")
        for name in S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
        if "function shellHash(" not in code:
            raise SystemExit("wrong base: no shellHash (the picture's hash, never the RNG)")
        edits, want = S6, ult_block(ULT["charge"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Widowmaker's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    row = relic_row(out_code, RELIC)
    for gone in ("radius:", "apply:", "knock:", 'kind:"nova"'):
        if gone in row:
            raise SystemExit(f"REFUSING TO WRITE -- the nova's {gone} is still on "
                             "Widowmaker's row")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    dmg = re.search(r"dmg:([\d.]+),", row).group(1)
    print(f"  ok    blade {dmg}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor aside)
    # draws no RNG, never takes the one ultFx slot (open item 25), calls
    # nothing that hurts, applies, resolves, beats or knocks, writes only what
    # S6_WRITE_OK names and mutates only the banner's local widths. The drip
    # voice is its one line on the sim path and the "+n" float its one match
    # write (the picture's presentation list), each in its own row only. The
    # probe's [11]-[12] and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickDrain|tickStatus|spawnShot|note)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if "float(" in ins and label != "exsanguinate picture: tickSiphon":
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' floats a "
                             "number outside tickSiphon (the drain files none)")
        if label.startswith("tickStatus"):
            if [ln.strip() for ln in ins.splitlines() if ln.strip()] != [
                    "const k0 = Math.floor(me.drainTally.drained);",
                    "if (Math.floor(me.drainTally.drained) > k0)", S6_DRIP]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"is not the drip voice alone:\n{ins}")
        elif "SFX" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside tickStatus's drain block")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort)\(", ins):
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
                             "(SPECS.widowmaker is the orchestrator's fx_remove)")
        for gone, why in (('u.w === "widowmaker"', "the nova's fang burst on the ultFx slot"),
                          ("freq: 3400, q: 1.6, gain: 0.34, dur: 0.20", "the nova's wet slice"),
                          ("widowmaker: 52,", "the banner's spread for the nova's fan")):
            if gone in out_code:
                raise SystemExit(f"REFUSING TO WRITE -- {why} is still here")
        for need, n in ((S6_DRIP, 1), ("this.tickSiphon(dt);", 1), ("this.drawSiphon(m);", 1),
                        ("this.drawSiphonTop(m);", 1), ('} else if (w === "widowmaker"){', 1),
                        ('} else if (w === "widowmaker-drain"){', 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields; the drip voice its one line on the sim path, the \"+n\" "
              "filed in tickSiphon); the inlined fx.js untouched; the nova's burst, slice, "
              "fan and spread out; the inhale, the drip, the thread, the flush wired once each")
    for label, _old, new in S1 + S2 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades|ult|onHit)\s*=[^=]", ins) or \
           re.search(r"\bw\.ult\.[A-Za-z]+\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        # THE DRAIN IS hp AND NOTHING ELSE (v76 §4-§5): no status, no beat,
        # no stop, no float, no knock -- the picture is stage 6's.
        for bad in (".apply(", "beat(", "hitStop", "float(", "SFX", ".vx", ".vy",
                    ".stun", "hurt("):
            if bad in ins:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' carries "
                                 f"'{bad}': the drain is hp and nothing else")
    if len(re.findall(r'kind:"drain"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one drain ultimate")
    n_nova = len(re.findall(r'kind:"nova"', out_code))   # read, never a refusal
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one drain ultimate, Widowmaker's; {n_nova} other nova row(s) "
          f"left as they were; no insert draws the RNG, writes the shared weapon, "
          f"or applies, beats, stops, floats or knocks; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
