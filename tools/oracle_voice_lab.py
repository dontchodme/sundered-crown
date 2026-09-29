#!/usr/bin/env python3
"""FORESIGHT'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v105.

    python oracle_voice_lab.py --game <Oracle's stage-5 link> --rows rows.json

v75 §6.2 SOUND, every word of it: "Cast: a rune-eye 'open' -- a filtered
inhale into a soft chime, 0.4s. The sigil: a very quiet sustained shimmer
(re-struck, 2-3 kHz band, peak <= 0.15) while it is drawn -- the only
continuous voice in the batch, and quiet on purpose. A hit: the bow's own
arrow voice plus a hex snap; pitch by count. Close: the chime reversed." The
brief's stage 6: "picture, voice, carry per design §6". Rick, for the batch's
art and sound: "you pick i overrule". So this lab does not offer a spread --
it renders three to five candidates a voice beside CONTROLS that can come back
wrong, prints the numbers each pick is made on, and PICKS by a rule written in
this file (`*_RULE`, `*_why`). He overrules from one clip.

REUSED, BECAUSE §6.2 NAMES IT: "a hex snap" is the runic school's `hex-snap`
(its own comment in play() names v75's "a hex snap" as the same sound). The
hit voice is the SCHOOL'S SNAP, its three calls transposed by count -- at
count 1 it IS `hex-snap`, sample for sample (checked below). "The bow's own
arrow voice" is the `hit` resolveHit already plays for every arrow: untouched.
NEW: the cast, the sigil's shimmer and the close (nothing in the game is an
inhale, a held shimmer or a reversed chime).

THE FOUR EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/oracle`, which `fireUlt` plays for every relic.
         Oracle has NO arm today: it falls through to the shared rune-crack
         (measured below, to 1e-6, with every other relic that still does).
         The arms go BEFORE that fallback (a row in mode `before`: the
         fallback line is not touched, so another relic's row anchored on it
         still applies, in either order). No sim line: the cast already plays.
  sigil  `ult/oracle-sigil` from `tickSight`, on the window's first frame and
         every N-th window frame after it while the window runs (a row in mode
         `after` the tally's last line, so never on the closing frame). The
         window's clock is the window tickers' clock: it stops in a hit stop,
         and so do the strikes. Each call strikes one short sine; the
         overlapping strikes ARE the held note (see the readings).
  hex    `ult/oracle-hex {n}` from `resolveHit`, right after the second hex
         is applied (mode `after` that line): once per window arrow that
         hexes twice -- a shot, the caster in its window, the foe alive and
         not a shade -- with n = foe.stacks("hex"), the count the tag now
         shows (1-5, the cap). A blade blow or an arrow outside the window
         gets no second hex and no snap. No new beat: the arrow's own hit
         beat and hit voice carry it (the task's map, and the sim's).
  close  `ult/oracle-close` from `tickSight` on the frame the window runs out
         BY ITS CLOCK with both fighters alive (mode `before` the close line;
         Canopy's and Zenith's rule) -- never on a death, never once the fight
         is over (step() stops calling the tickers).

THE CONTROLS, and what each one is for:
  rune-crack   what Oracle's cast plays TODAY; v88 published 0.608 / 450 ms --
               reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@10       Oracle's own blow (blade 10, stage 5): the level the cast is
               judged against, on its quietest / loudest noise draw; and the
               voice every snap lands ON (same frame)
  wall         the commonest sound in a fight: the sigil's ceiling (half of it)
  loose        the bow's own string, every 0.34 s: the sigil's floor
  hex-snap     the school's snap, which the hit voice transposes
  the school   the runic casts with a voice of their own (read off the page)
  the type     the bow casts with a voice of their own (read off the page)
  death        the heaviest voice in the game
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  TICK, HISS, CLICK, EXHALE, RC-NOW   the cast without its inhale / without
               its chime / with its chime struck hard / with its breath
               reversed (the band falling) / what `ult/oracle` plays today:
               each must fail its gate
  STEADY, BUZZ, GAP, LOW, LOUD, CEILING   the shimmer with no shimmer (decay
               16 s) / re-struck at 60 Hz / every 30 frames / an octave down /
               12 dB up / at a 0.2 peak: each must fail its gate
  FLAT, DOWN, BURIED   the snap at one pitch for every count / stepping down /
               20 dB under: each must fail its gate
  AGAIN        the chime forward, played as the close: must fail "reversed"
  LITERAL      the picked cast's chime rendered dry, its samples REVERSED,
               played through the chain. A reference, never a candidate: it
               needs an async render and every clip rebuilds the synth
               synchronously (v88 §6b), so it would be SILENT in a clip.

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT, generated with its constants rounded
    first and rendered by evaluating that text on the synth; the rows are then
    applied to `Sfx.prototype.play`'s own source and rendered again, and must
    match to TOL = 1e-5 (-100 dB; REPRO is printed). There is no second
    transcription to get wrong.
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's,
    bindweed_voice_lab's and ironhail_voice_lab's, imported unchanged (E50,
    TOP, PEAK, AUDIBLE, GONE, RISE, LATE, REG, IN-BAND, PITCH, ENV-CORR, TONAL,
    BREATH-RISE / DIPS / REGROW, HEARD). New here, each with a control that can
    come back wrong:
      CEN-RISE   the draw-averaged power centroid over the second half of the
                 inhale's swell over the first half's (EXHALE must fail)
      SOFT       the chime alone: its 1 ms envelope's 10 -> 90% rise, ms (CLICK
                 and TICK must fail)
      HANDOVER   |the inhale's loudest 25 ms - the chime's onset|, ms
      SHIMMER    p95 - p5 of the shimmer's 5 ms RMS (dB, 1 ms hop) over its
                 steady part: the flicker's depth (STEADY and GAP must fail)
      RATE       the peak of the 1 ms RMS envelope's spectrum, 2-80 Hz: the
                 flicker's rate (BUZZ must fail)
      BAND       the share of the steady shimmer's power in 2000-3000 Hz (LOW
                 must fail)
      OVER       the voice's 50 ms RMS inside a third-octave against the
                 score's p90 of the same (50 ms windows over 2-10 s of the
                 bed), dB -- MED / MIN over the steady part, and GONE-AT: how
                 long after the close it stays under the score for good
      OVER-HIT   the snap and Oracle's blow on one instant against the blow
                 alone, in the snap's loudest third-octave (>= 200 Hz), its
                 first 50 ms, dB (BURIED must fail)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's chime decay is solved so the voice is AUDIBLE 400 ms,
    its breath's gain puts the inhale's loudest 50 ms 3 dB under the chime's,
    and its gain puts TOP at the centre of its window; the sigil's gain puts
    its steady TOP at the centre of its window; the snap keeps the school's
    gains; the close's gain puts its TOP on the chime's. Constants are rounded
    BEFORE any measured render, so a shipped arm is bit-for-bit what was
    measured.

THE DECLARED READINGS (not candidates -- words of §6.2 turned into numbers;
every one Code's, under "you pick i overrule"):
  1. "0.4s": AUDIBLE 330-470 ms, the batch's reading (v100 Portcullis, v108
     Ironhail).
  2. "A FILTERED INHALE": one `_sweep` of band-passed noise (q 1.2) that
     swells for 0.6 of its 0.55 s -- the longest attack the toolkit allows --
     its band RISING two octaves under the chime's note through it, so it
     passes the note at its top: an inhale draws in, and "into" hands it over.
     Gates: BREATH-RISE >= 40 ms (a swell, not a strike), CEN-RISE >= 1.19 (a
     quarter octave: the band climbs), TONAL <= 10 dB (air, not a note).
  3. "INTO A SOFT CHIME": the chime enters at the inhale's top (HANDOVER <= 40
     ms, no DIP on the whole voice's way up); it is a note (TONAL >= 20 dB,
     its pitch within 25 cents of the declared note); SOFT: struck as four
     in-phase strikes over 30 ms (a mallet, not a click) -- rise >= 8 ms.
     Every constant-pitch tone sets `.frequency.value = f` (v97's finding).
  4. THE CAST'S LEVEL, the batch's cast rule: TOP between 0.5x the blow's
     loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST, every draw.
  5. "RE-STRUCK ... SUSTAINED ... WHILE IT IS DRAWN": a held note does not
     exist in this toolkit (CLAUDE.md 4.5), so the shimmer is RE-STRUCK -- by
     the window itself: tickSight strikes one short sine on the window's first
     frame and every N-th window frame after, and stops when the window does. The sine is 2640 Hz, E7 (+2 cents, the score's v), =
     22 x 120 Hz: render.py places every sound at its match time, a whole
     number of 1/120 s frames, so every strike starts in phase with every
     other and they sum as ONE held note; the ripple between strikes is the
     shimmer. (Live, off that grid, the strikes meet at arbitrary phase: the
     same note with a less regular flicker. The deliverable is the clip.)
  6. "VERY QUIET": the quietest voice in the fight -- its steady TOP between
     the bow's own string (TOP on its loudest draw; "at least as audible as
     the bow's release", Briarwand's and Culverin's floor) and half the wall
     tick's (quietest draw: the commonest sound in a fight, 6 dB under it),
     level-matched at the geometric centre; and still HEARD over the score:
     OVER-MED >= +6 dB and OVER-MIN >= +3 dB (no gap between strikes).
     "PEAK <= 0.15": the sample peak, on the steady train and in a real
     window.
  7. "SHIMMER": SHIMMER 2-6 dB (a flicker, not a flat tone, not a pulse) at a
     RATE of 4-20 Hz (a flicker the ear follows, under roughness); "2-3 kHz
     BAND": BAND >= 0.90; "WHILE IT IS DRAWN": GONE-AT <= 0.3 s after the
     close (the sigil fades over 0.3 s, §6.1), the last strike being N-1
     window frames at most before the close.
  8. "A HEX SNAP; PITCH BY COUNT": the school's snap, every frequency x
     2^(step(n)/12), n = the foe's hex count after the second hex, clamped
     1-5; count 1 = the school's snap exactly; the steps RISE with the count
     (the batch's reading of "pitch by count" -- Bindweed, Coldiron, Ironhail).
     Gates: the measured pitch within 25 cents of each declared step and
     rising >= 30 cents with every count; TOP within 3 dB of the school's snap
     at every count; OVER-HIT >= +6 dB at every count on every draw (it lands
     on the blow's frame and must not vanish under it).
  9. "THE CHIME REVERSED": the picked cast's chime, each of its modes' decay
     run backwards as a re-struck climb (strikes ~11 ms apart at whole cycles)
     that ends where the chime began and is cut there; at the chime's own
     level (TOP within 3 dB of the chime's). Gates: LATE >= 0.5, the loudest
     50 ms in the last 40% of its audible span, ENV-CORR >= 0.80 against the
     LITERAL reversal, the chime's note within 25 cents, TONAL >= 20 dB.
 10. THE CLOSE plays on the frame the window runs out by its clock with both
     fighters alive (Canopy's and Zenith's rule): a death ends the window
     silently -- the death voice is the event.

THE ROUNDS. Round 1 (the first candidates of each voice, the rules as first
written) exited 1 twice over, and both failures were one TOOLKIT FINDING:
`_tone` ramps its gain to 0.0001 ABSOLUTE, not relative, so a strike at gain g
falls 20 log10(g / 0.0001) dB over its whole dur and then stops -- whatever
the dur. (CLAUDE.md 4.5 says `_tone` "ends on an exponential ramp over its
whole length"; the ramp's END is fixed, so a quiet strike barely decays.)
  * THE SIGIL: every round-1 shimmer was still heard 1.0-2.5 s after the
    close. Its strikes (1-2.7 s long at g ~ 0.0002) fell only ~7 dB each and
    piled up twenty deep; the tail was the strike's length. Round 2 ADDS four
    shimmers of 0.3 s strikes (6-9) and three controls on that length (HELD,
    FLUTTER, GAPS -- round 1's STEADY and GAP came back wrong for the pile-up,
    not for what they are named). No sigil rule changed.
  * THE CLOSE: round 1 reversed the chime as if each mode fell 80 dB over its
    decay; the chime's strikes (g ~ 0.025) fall ~48 dB, so round 1's climbs
    were too steep, and ENV-CORR against the literal came back NEGATIVE (-0.15
    to -0.88); WHOLE's breath started before its own event and the run
    stopped. Round 2 ADDS four reversals on the chime's actual fall (each
    mode's own strike gain against 0.0001) and starts every breath at or after
    its event. No close rule changed.
Every round-1 candidate stays in the table. The cast and the snap are round
1's and passed.
  * THE REAL WINDOW (a check on the picks, not a rule a candidate is picked
    on): round 2's first full run read the close over 0.1 s either side of its
    event and got +2.0 dB -- a window that ends before the reversed chime
    reaches its top (0.32 s after its event: it CLIMBS). It is read now over
    its first 0.4 s, as the cast is; both readings are printed. The threshold
    did not move.

THE PICKS, on Chromium 151.0.7922.34, sc-oracle-b10 72dcd8aa43e5b501, fight
seeds 105701-105702 (152 fights, 571 windows):

  cast   3 SIGIL   the breath (band-passed noise 660 -> 6652 Hz, q 1.2,
                   swelling 0.33 s) into a soft E7 chime (2640 Hz with a
                   faint bar mode, four in-phase strikes over 30 ms): audible
                   395 ms, breath-rise 87 ms, the band climbing x1.27, the
                   chime 3 ms off the breath's top and rising in 23 ms, -3.2
                   to -2.4 dB re the blow; register at most 0.65 (the
                   school's snap). The A6 chimes (BELL, GLASS) read 0.81
                   against rune-crack (its 1676 Hz partial); LOW (0.63) ties
                   on register and loses the order; FIFTH 0.73.
  sigil  6 FLICK   E7 struck by tickSight every 8 window frames (15 a
                   second), each strike 0.3 s at gain 0.001924 (falling 26
                   dB, 4.5 deep): a 5.1 dB shimmer at 15 Hz, +3.0 dB re the
                   bowstring and -9.0 dB re the wall tick, +29.4 dB over the
                   score in its third-octave (+28.4 at the least), peak
                   0.0065, under the score 0.27 s after the close. SHIVER (17
                   Hz) passes and loses on calls a second; PULSE is 6.8 dB
                   deep; round 1's five are all heard 1.0-2.5 s after the
                   close.
  snap   1 SEMI    the school's snap up a semitone a count: 3003 / 3184 /
                   3377 / 3581 / 3790 Hz (5 cents at worst), +9.2 dB or more
                   over the blow it lands on, count 1 the school's snap to
                   0; register 0.63 against the wall tick (WHOLE 0.71, PENT
                   0.73 lose the register tiebreak).
  close  5 FULL    the chime's whole fall run backwards, 44 strikes 0.1 s
                   long: ENV-CORR 0.92 with the literal reversal, its top at
                   0.75 of its span, audible 325 ms, at the chime's level.
                   BREATH passes (0.93: the same to 0.02) and loses on
                   calls; VELVET tops at 0.54; round 1's four correlate
                   NEGATIVELY.

  In play: 571 casts -> 571 cast voices; 62423 strike frames -> 62423
  strikes; 2253 second hexes -> 2253 snaps, counts 2: 384, 3: 145, 4: 245,
  5: 1479 (66% at the cap -- count 1 never sounds in play: the channel's own
  hex is on first); 467 clock closes -> 467 close voices, none on the 56
  deaths or 48 fight-ends; 152/152 fights identical and every other voice
  call identical; the control comes back 3/152. A hit stop holds the window
  and the strikes with it: the longest real gap between strikes in a clock
  window is 0.258 s at the median and 1.317 s at the most, and a freeze
  longer than a strike (0.3 s) lets the shimmer fall silent until the world
  moves again. The picks among themselves: the cast, the shimmer and the
  close share E7 on purpose (register 0.85-0.96: the eye opens onto the
  sigil's note and shuts on it); the snap stands apart (0.42-0.76). Against
  the batch's other scratch voices at most 0.71 (Bindweed's wither) but the
  school's own snap (0.99, which Portcullis's row re-emits). Main-thread
  cost a call: cast 0.4 ms, sigil 0.0 ms, snap 0.2 ms, close 1.7 ms. In a
  real window (v Morningstar, 105701, 120 strikes, 14 snaps) every snap
  stands +8.1..+12.4 dB over the fight in its own third-octave, the cast
  +6.7 dB, the close as printed, and the shimmer is over the score for 100%
  of the window and adds >= 3 dB to the fight in its band for 73% of it.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (four arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the snap at
    counts -1, 0, 1-5, 9 and a missing n, on two noise draws) must reproduce
    its candidate to TOL; every other voice through the patched play (the hit
    at five weights with and without a crit, spark x3, wall, death, clank x2,
    seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork, scour x4, and
    every relic's cast and every sub-voice the ult arm names) must be
    unchanged; `ult/oracle` must NOT be rune-crack any more;
  * the tickSight and resolveHit rows are applied to their prototypes' own
    source and run on real fights beside the unpatched ones: every fight
    identical (over, clock, both hp, shields, positions, velocities, charges,
    both hex counts, the arrows in the air, winner and the whole sightTally)
    and every other voice call identical in order, kind and opts; one sigil
    strike on every N-th window frame from the first and nowhere else; one
    snap per second hex, on its step, carrying the foe's count; one close per
    window closed by its clock with both alive; one cast voice per cast; the
    unpatched runs play none of the new ids. The same rows plus ONE sim write
    (the foe nudged 1e-9 on a snap) must come back NOT identical.
  * END TO END: the rows applied AS TEXT, in their modes, to a copy of the
    game file (in a temp folder, never the repo), loaded in a fresh browser
    after the first is closed: the page loads clean, its own SFX.play renders
    the arms to the lab's text and every other voice to the original page's,
    and its fights are identical to the original page's with the right voices.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both alike.
  All anchors must occur exactly once in the game file; no row's code
  contains its anchor, so a later relic's row -- or the picture's --
  anchored on the same line still applies, in either order.

Writes wavs to 05-reference/v105/oracle-*.wav at RAW level (gitignored).
Refuses to write silence. Touches no build.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import pathlib
import re
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
# The shared definitions, imported unchanged so every number here means what
# it means in v98's, v99's, v101's and v108's labs. (Their module bodies only
# check their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env, env_corr,
    fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import low_share  # noqa: E402
from bindweed_voice_lab import tonal  # noqa: E402
from ironhail_voice_lab import _wrap, bed_p90, breath, heard, peer_name  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "oracle"
BLADE = 10.0                              # Oracle's dmg (stage 5, blade 10)
CAP = 5                                   # STATUS.hex.maxStacks (checked on the page)
COUNTS = list(range(1, CAP + 1))
FRAME = 120                               # 1 / CONFIG.physics.dt (checked on the page)
DUR = 8                                   # w.ult.dur (checked)
CAST_AUD = 400.0                          # "0.4s": the chime's decay is solved to this
AUD_LO, AUD_HI = 330.0, 470.0
INHALE_UNDER_DB = 3.0                     # the inhale's loudest 50 ms under the chime's
SW, STRIKES = 0.03, 4                     # the soft chime: four in-phase strikes over 30 ms
DI, AI = 0.55, 0.33                       # the inhale's _sweep: 0.55 s, its top at 0.6 of it
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)
A5, A6, E7G = 880.0, 1760.0, 2640.0       # E7G = 22 x 120 Hz (reading 5)
EVERY = 0.011                             # the close's re-strike spacing target (Zenith's)
FADE = 0.3                                # the sigil's fade after the close (v75 §6.1)


def close_gap(N):
    """Window frames between the last strike and the clock close: strikes on
    frames j = 1, 1 + N, ... while the window runs; the clock closes on frame
    DUR x FRAME (tickSight's close line, before the tally)."""
    jc = DUR * FRAME
    return jc - (1 + N * ((jc - 2) // N))


# ============================================================== THE CAST ===
# "a rune-eye 'open' -- a filtered inhale into a soft chime, 0.4s".
MODES = {
    "bell": [(1, 1, 1), (2.76, 0.25, 0.5)],                 # a sine and a faint bar mode
    "glass": [(1, 1, 1), (2.32, 0.3, 0.6), (4.25, 0.1, 0.4)],  # a struck glass (shell modes)
    "fifth": [(1, 1, 1), (1.5, 0.7, 1)],                    # A6 and E7: the sigil's note over it
}
CAST_CANDIDATES = [
    ("1 BELL", dict(note=A6, modes="bell"),
     "the breath into a soft A6 (1760 Hz): a sine with a faint bar mode (2.76x at 0.25)"),
    ("2 GLASS", dict(note=A6, modes="glass"),
     "the breath into a soft A6 glass: shell modes 2.32x at 0.3 and 4.25x at 0.1"),
    ("3 SIGIL", dict(note=E7G, modes="bell"),
     "the breath into the sigil's own note, E7 (2640 Hz): the eye opens onto the shimmer"),
    ("4 FIFTH", dict(note=A6, modes="fifth"),
     "the breath into A6 and E7 together (an open fifth, the sigil's note on top)"),
    ("5 LOW", dict(note=A5, modes="bell"),
     "BELL an octave down, A5 (880 Hz)"),
]
CAST_CONTROLS = [
    ("0 TICK", dict(note=A6, modes="bell", parts=("chime",), strikes=1),
     "BELL's chime alone, struck once: no inhale, a hard strike"),
    ("0 HISS", dict(note=A6, modes="bell", parts=("inhale",)),
     "BELL's inhale alone: no chime"),
    ("0 CLICK", dict(note=A6, modes="bell", strikes=1),
     "BELL with its chime struck once (hard): not soft"),
    ("0 EXHALE", dict(note=A6, modes="bell", exhale=True),
     "BELL with its breath reversed: the band FALLING from over the note, a short attack"),
]


def inhale_band(note):
    """f0 two octaves under the note, f1 so the exponential ramp passes the
    note at 0.6 of the sweep (its top)."""
    f0 = round(note / 4, 1)
    return f0, round(f0 * (note / f0) ** (1 / 0.6), 1)


def vjs(v):
    return "[" + ", ".join("[" + ", ".join(fmt(c) for c in m) + "]" for m in v) + "]"


def cast_body(sp, g, ki, dc, parts=None, ind=10):
    """The cast arm's body. `parts`: which of the inhale and the chime (the
    measure renders each alone from this same generator)."""
    parts = parts or sp.get("parts", ("inhale", "chime"))
    note = sp["note"]
    f0, f1 = inhale_band(note)
    t1 = AI if "inhale" in sp.get("parts", ("inhale", "chime")) else 0.0
    L = [f"const g = {fmt(g)};"]
    if "inhale" in parts:
        if sp.get("exhale"):
            L.append(f'this._sweep(t, {{ f0: {fmt(f1)}, f1: {fmt(f0)}, q: 1.2, gain: g * {fmt(ki)}, dur: {fmt(DI)}, '
                     f'atk: 0.02, type:"bandpass" }});')
        else:
            L.append(f'this._sweep(t, {{ f0: {fmt(f0)}, f1: {fmt(f1)}, q: 1.2, gain: g * {fmt(ki)}, dur: {fmt(DI)}, '
                     f'atk: {fmt(AI)}, type:"bandpass" }});')
    if "chime" in parts:
        n = sp.get("strikes", STRIKES)
        tt = "t" if t1 == 0 else f"t + {fmt(t1)}"
        L.append(f"for (const [r, k, d] of {vjs(MODES[sp['modes']])}){{")
        L.append(f"  const f = {fmt(note)} * r;")
        if n == 1:
            L.append(f'  this._tone({tt}, {{ freq: f, gain: g * k, dur: {fmt(dc)} * d, type:"sine" }}).frequency.value = f;')
        else:
            L.append(f"  for (let i = 0; i < {n}; i++)")
            L.append(f'    this._tone({tt} + Math.round(f * {fmt(SW)} * i / {n}) / f, {{ freq: f, gain: g * k / {n}, '
                     f'dur: {fmt(dc)} * d, type:"sine" }}).frequency.value = f;')
        L.append("}")
    return "\n".join(" " * ind + l_ for l_ in L)


# ============================================================= THE SIGIL ===
# "a very quiet sustained shimmer (re-struck, 2-3 kHz band, peak <= 0.15)
# while it is drawn". One call = one strike; tickSight re-strikes every N
# window frames. A strike is `_tone` at gain g for D s -- and `_tone` ramps
# to 0.0001 ABSOLUTE, so at this level (g ~ 0.0002-0.003) a strike falls only
# 20 log10(g / 0.0001) dB over its D and then stops (THE ROUNDS): the strikes
# overlap D x 120 / N deep, the shimmer is their staircase, the tail is D.
SIGIL_CANDIDATES = [
    ("1 FLICKER", dict(parts=[(E7G, 1.0)], N=8, D=1.333),
     "E7 (2640 Hz) struck every 8 frames (15 Hz), each strike 1.333 s long (round 1)"),
    ("2 SHIMMER", dict(parts=[(E7G, 1.0)], N=6, D=1.0),
     "E7 struck every 6 frames (20 Hz), each 1 s long (round 1)"),
    ("3 TREMOLO", dict(parts=[(E7G, 1.0)], N=12, D=2.0),
     "E7 struck every 12 frames (10 Hz), each 2 s long (round 1)"),
    ("4 SLOW", dict(parts=[(E7G, 1.0)], N=16, D=2.667),
     "E7 struck every 16 frames (7.5 Hz), each 2.667 s long (round 1)"),
    ("5 GLINT", dict(parts=[(E7G, 1.0), (2880.0, 0.35)], N=8, D=1.333),
     "FLICKER with a second in-band partial, 2880 Hz (24 x 120) at 0.35 (round 1)"),
    # ROUND 2 (see THE ROUNDS): strikes 0.3 s long, so the shimmer stops with the sigil
    ("6 FLICK", dict(parts=[(E7G, 1.0)], N=8, D=0.3),
     "round 2: E7 struck every 8 frames (15 Hz), each strike 0.3 s long"),
    ("7 SHIVER", dict(parts=[(E7G, 1.0)], N=7, D=0.3),
     "round 2: E7 struck every 7 frames (17 Hz), each 0.3 s long"),
    ("8 PULSE", dict(parts=[(E7G, 1.0)], N=10, D=0.3),
     "round 2: E7 struck every 10 frames (12 Hz), each 0.3 s long"),
    ("9 TWINKLE", dict(parts=[(E7G, 1.0), (2880.0, 0.35)], N=8, D=0.3),
     "round 2: FLICK with the second in-band partial, 2880 Hz at 0.35"),
]
SIGIL_CONTROLS = [
    ("0 STEADY", dict(parts=[(E7G, 1.0)], N=8, D=16.0), "FLICKER's strikes 16 s long (round 1)"),
    ("0 BUZZ", dict(parts=[(E7G, 1.0)], N=2, D=0.333), "E7 struck every 2 frames (60 Hz), 0.333 s long: a buzz"),
    ("0 GAP", dict(parts=[(E7G, 1.0)], N=30, D=1.333), "FLICKER struck every 30 frames (round 1)"),
    ("0 LOW", dict(parts=[(1320.0, 1.0)], N=8, D=1.333), "FLICKER an octave down (1320 Hz): out of the band"),
    ("0 LOUD", dict(parts=[(E7G, 1.0)], N=8, D=1.333, db=12.0), "FLICKER 12 dB up: not very quiet"),
    ("0 CEILING", dict(parts=[(E7G, 1.0)], N=8, D=1.333, peak=0.2), "FLICKER at a 0.2 peak: over the design's 0.15"),
    # ROUND 2's, on round 2's strike length
    ("0 HELD", dict(parts=[(E7G, 1.0)], N=2, D=0.3), "round 2: E7 struck every 2 frames, 0.3 s long: a held note, no flicker"),
    ("0 FLUTTER", dict(parts=[(E7G, 1.0)], N=4, D=0.2), "round 2: struck every 4 frames (30 Hz), 0.2 s long: too fast to flicker"),
    ("0 GAPS", dict(parts=[(E7G, 1.0)], N=30, D=0.3), "round 2: FLICK struck every 30 frames: strikes that do not meet"),
]


def sigil_body(sp, g, ind=10):
    L = [f"const g = {fmt(g)};"] if len(sp["parts"]) > 1 else []
    for f, k in sp["parts"]:
        gx = fmt(g) if len(sp["parts"]) == 1 else ("g" if k == 1 else f"g * {fmt(k)}")
        L.append(f'this._tone(t, {{ freq: {fmt(f)}, gain: {gx}, dur: {fmt(sp["D"])}, type:"sine" }}).frequency.value = {fmt(f)};')
    return "\n".join(" " * ind + l_ for l_ in L)


# ============================================================== THE SNAP ===
# "a hex snap; pitch by count": the school's snap (read off the page and
# checked), every frequency x 2^(step(n)/12).
SNAP_SRC = ('this._burst(t, { freq: 2600, q: 1.2, gain: 0.38, dur: 0.022, type:"bandpass" });\n'
            'this._burst(t, { freq: 1300, q: 1.0, gain: 0.15, dur: 0.030, type:"bandpass" });\n'
            'this._tone (t, { freq: 3100, to: 2500, gain: 0.138, dur: 0.045, type:"triangle" });')
SNAP_CANDIDATES = [
    ("1 SEMI", dict(steps=[0, 1, 2, 3, 4]), "the school's snap up a semitone a count"),
    ("2 WHOLE", dict(steps=[0, 2, 4, 6, 8]), "the school's snap up a whole tone a count"),
    ("3 PENT", dict(steps=[0, 3, 5, 7, 10]), "the school's snap up the minor pentatonic (0 3 5 7 10)"),
]
SNAP_CONTROLS = [
    ("0 FLAT", dict(steps=[0, 0, 0, 0, 0]), "the school's snap at every count: no pitch by count"),
    ("0 DOWN", dict(steps=[0, -1, -2, -3, -4]), "down a semitone a count"),
    ("0 BURIED", dict(steps=[0, 2, 4, 6, 8], gk=0.1), "WHOLE 20 dB under: lost under the blow"),
]


def snap_body(sp, ind=10):
    gk = sp.get("gk", 1.0)
    head = (f"const n = clamp(Math.round(p.n === undefined ? 1 : p.n), 1, {CAP}), "
            f"k = Math.pow(2, [{', '.join(str(s) for s in sp['steps'])}][n - 1] / 12);")
    L = [head]
    for (fq, q, gn, du) in ((2600, 1.2, 0.38, 0.022), (1300, 1.0, 0.15, 0.030)):
        L.append(f'this._burst(t, {{ freq: {fq} * k, q: {fmt(q)}, gain: {fmt(round(gn * gk, 6))}, dur: {fmt(du)}, '
                 f'type:"bandpass" }});')
    L.append(f'this._tone(t, {{ freq: 3100 * k, to: 2500 * k, gain: {fmt(round(0.138 * gk, 6))}, dur: 0.045, '
             f'type:"triangle" }});')
    return "\n".join(" " * ind + l_ for l_ in L)


# ============================================================= THE CLOSE ===
# "the chime reversed": every mode of the PICKED cast's chime, its decay run
# backwards over L as a re-struck climb, each strike decaying DS (the cut).
CLOSE_CANDIDATES = [
    ("1 MIRROR", dict(L=0.5, DS=0.1),
     "round 1: the chime's decay (taken as 80 dB over its length) run backwards from -40 dB, strikes 0.1 s"),
    ("2 SMOOTH", dict(L=0.5, DS=0.25), "round 1: MIRROR with strikes 0.25 s long"),
    ("3 SHORT", dict(L=0.25, DS=0.1), "round 1: MIRROR from -20 dB"),
    ("4 WHOLE", dict(L=0.5, DS=0.1, exhale=True),
     "round 1: MIRROR, then the breath reversed (its band falling from the note)"),
    # ROUND 2 (see THE ROUNDS): the chime's ACTUAL fall -- each mode's strike gain down to 0.0001
    ("5 FULL", dict(L=1.0, DS=0.1, floor=True),
     "round 2: the chime's whole fall run backwards, from where it fades to where it was struck; strikes 0.1 s"),
    ("6 VELVET", dict(L=1.0, DS=0.25, floor=True), "round 2: FULL with strikes 0.25 s long: a smoother climb, a softer cut"),
    ("7 HALF", dict(L=0.5, DS=0.1, floor=True), "round 2: the last half of FULL"),
    ("8 BREATH", dict(L=1.0, DS=0.1, floor=True, exhale=True),
     "round 2: FULL, then the breath reversed: the whole cast backwards"),
]


def close_body(cp, C_, gc, ind=10):
    """cp: the close's shape; C_: the picked cast (note, modes, dc). L is a
    FRACTION of the chime's decay (0.5 = from -40 dB)."""
    sp, dc = C_["sp"], C_["dc"]
    note = sp["note"]
    Ls = round(cp["L"] * dc, 4)
    L = [f"const g = {fmt(gc)}, L = {fmt(Ls)};"]
    if cp.get("floor"):
        # round 2: each mode's fall is its strike gain (the cast's g x k / STRIKES) down to 0.0001
        modes = [(r, k, d, float(f"{0.0001 * STRIKES / (C_['g'] * k):.4g}")) for (r, k, d) in MODES[sp["modes"]]]
        L.append(f"for (const [r, k, d, R] of {vjs(modes)}){{")
        L.append(f"  const f = {fmt(note)} * r, dt = Math.max(1, Math.round(f * {fmt(EVERY)})) / f, "
                 f"q = Math.pow(0.0001, dt / {fmt(cp['DS'])});")
        L.append(f"  for (let s = Math.max(0, L - {fmt(dc)} * d); s < L - 1e-9; s += dt)")
        L.append(f"    this._tone(t + s, {{ freq: f, gain: g * k * (1 - q) * Math.pow(R, (L - s) / ({fmt(dc)} * d)), "
                 f"dur: {fmt(cp['DS'])}, type:\"sine\" }}).frequency.value = f;")
    else:
        L.append(f"for (const [r, k, d] of {vjs(MODES[sp['modes']])}){{")
        L.append(f"  const f = {fmt(note)} * r, dt = Math.max(1, Math.round(f * {fmt(EVERY)})) / f, "
                 f"q = Math.pow(0.0001, dt / {fmt(cp['DS'])});")
        L.append("  for (let s = 0; s < L - 1e-9; s += dt)")
        L.append(f"    this._tone(t + s, {{ freq: f, gain: g * k * (1 - q) * Math.pow(10, -4 * (L - s) / ({fmt(dc)} * d)), "
                 f"dur: {fmt(cp['DS'])}, type:\"sine\" }}).frequency.value = f;")
    L.append("}")
    if cp.get("exhale"):
        # the breath reversed: its top on the chime's top (t + L), never before the event
        f0, f1 = inhale_band(note)
        at_ = round(min(0.22, Ls), 4)
        on = round(Ls - at_, 4)
        tt = "t" if on == 0 else f"t + {fmt(on)}"
        L.append(f'this._sweep({tt}, {{ f0: {fmt(f1)}, f1: {fmt(f0)}, q: 1.2, gain: g * {fmt(C_["ki"])}, '
                 f'dur: {fmt(DI)}, atk: {fmt(at_)}, type:"bandpass" }});')
    return "\n".join(" " * ind + l_ for l_ in L)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
SIGIL_ANCHOR = '      T.foeHex += foe.stacks("hex");'
HEX_ANCHOR = '        T.hex += self.w.ult.hex;'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultSight = null; continue; }'


def sigil_code(N):
    """Mode `after` SIGIL_ANCHOR (tickSight's last tally line)."""
    return f'''
      /* FORESIGHT'S SIGIL (v75 §6.2: "a very quiet sustained shimmer
         (re-struck, 2-3 kHz band, peak <= 0.15) while it is drawn"): a held
         note does not exist in this toolkit, so the window re-strikes it --
         on its first frame and every {N}th window frame after, while it runs
         (never on the closing frame, which `continue`s above). On the window's
         clock, so a hit stop holds the strikes as it holds the sigil.
         Presentation only: SFX.play draws nothing, is a no-op headless, and
         nothing here is read back (oracle_voice_lab: fights identical). */
      if (Math.round(Z.t / dt) % {N} === 1) SFX.play("ult", {{ w: "oracle-sigil" }});'''


HEX_CODE = '''
        /* THE SNAP (v75 §6.2: "a hit: the bow's own arrow voice plus a hex
           snap; pitch by count"): the school's snap, pitched by the count
           the foe's tag now shows, once per arrow that hexes twice. The
           arrow's own hit voice and hit beat are the engine's, untouched.
           Presentation only; nothing here is read back. */
        SFX.play("ult", { w: "oracle-hex", n: foe.stacks("hex") });'''

CLOSE_CODE = '''      /* FORESIGHT'S CLOSE (v75 §6.2: "close: the chime reversed"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive --
         never on a death, never once the fight is over (step() stops calling
         this). Presentation only; nothing here is read back. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "oracle-close" });
'''

# the sim-write control: the snap row with the foe nudged 1e-9 on a snap
HEX_CODE_BAD = HEX_CODE.replace('        SFX.play("ult", { w: "oracle-hex"',
                                '        foe.vx += 1e-9;\n        SFX.play("ult", { w: "oracle-hex"', 1)
assert HEX_CODE_BAD != HEX_CODE
_refuse(sigil_code(8) + HEX_CODE + CLOSE_CODE, "sim rows")


def as_replace(anchor, mode, code):
    """A row as the [anchor, replacement] pair its mode means (e2e2.py's
    semantics: replace = code, after = anchor + code, before = code + anchor)."""
    return [anchor, {"replace": code, "after": anchor + code, "before": code + anchor}[mode]]


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


# ============================================================== THE PAGE ===
RENDER_JS = r"""async ([evs, secs, seed, rows]) => {
  const OC = window.OfflineAudioContext, sr = 48000;
  const proto = Object.getPrototypeOf(AC.SFX);
  const mkNoise = (oc) => {
    const n = Math.floor(sr * 0.6), nb = oc.createBuffer(1, n, sr);
    const d = nb.getChannelData(0); let s = (seed || 0x9e3779b9) >>> 0;
    for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17;
      s ^= s << 5; s >>>= 0; d[i] = (s / 4294967296) * 2 - 1; }
    return nb; };
  let patched = null;
  if (rows){
    let src = proto.play.toString();
    for (const [anc, code] of rows){
      const at = src.split(anc).length - 1;
      if (at !== 1) return { err: `an Sfx anchor occurs ${at} times in play()` };
      src = src.replace(anc, () => code);
    }
    patched = (0, eval)("(function " + src + ")");
  }
  const mk = (oc, chain) => {
    let cursor = 0;
    const S = Object.create(proto);
    S.ok = true; S.on = true;
    S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
      const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
    S.bus = chain ? S.constructor.buildChain(oc, oc.destination)
                  : (() => { const g = oc.createGain(); g.connect(oc.destination); return g; })();
    S.noise = mkNoise(oc);
    return { S, at: (x) => { cursor = x; } };
  };
  const oc = new OC(1, Math.round(sr * secs), sr);
  const Y = mk(oc, true), S = Y.S;
  const log = { burst: [], sweep: [], tone: 0 };
  S._burst = function(t, o, d){ log.burst.push(o.dur); return proto._burst.call(this, t, o, d); };
  S._sweep = function(t, o, d){ log.sweep.push(o.dur); return proto._sweep.call(this, t, o, d); };
  S._tone  = function(t, o, d){ log.tone++; return proto._tone.call(this, t, o, d); };
  const fns = new Map(), calls = [];
  const body = (txt) => { if (!fns.has(txt)) fns.set(txt, (0, eval)("(function(t, p){\n" + txt + "\n})")); return fns.get(txt); };
  for (const e of evs){
    Y.at(e[1]);
    const before = log.tone + log.burst.length + log.sweep.length;
    if (e[0] === "play") S.play(e[2], e[3]);
    else if (e[0] === "arm") patched.call(S, e[2], e[3]);
    else if (e[0] === "body") body(e[2]).call(S, e[1], e[3] || {});
    else if (e[0] === "lit"){
      /* the body rendered DRY (no chain), trimmed, its samples reversed, played through the chain */
      const dc = new OC(1, Math.round(sr * 3), sr), Z = mk(dc, false);
      Z.at(0.5); body(e[2]).call(Z.S, 0.5, e[4] || {});
      const dry = (await dc.startRendering()).getChannelData(0);
      let a = 0, b = dry.length - 1; const TH = 1e-6;
      while (a < dry.length && Math.abs(dry[a]) < TH) a++;
      while (b > a && Math.abs(dry[b]) < TH) b--;
      const seg = dry.slice(a, b + 1).reverse();
      for (let i = 0; i < seg.length; i++) seg[i] *= e[3];
      const rb = oc.createBuffer(1, seg.length, sr); rb.copyToChannel(seg, 0);
      const src = oc.createBufferSource(); src.buffer = rb;
      src.connect(S.bus); src.start(e[1]);
    }
    calls.push(log.tone + log.burst.length + log.sweep.length - before);
  }
  const buf = await oc.startRendering();
  const d = buf.getChannelData(0);
  const u8 = new Uint8Array(d.buffer, d.byteOffset, d.byteLength);
  let s = ""; for (let i = 0; i < u8.length; i += 0x8000)
    s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return { pcm: btoa(s), log, calls };
}"""

COST_JS = r"""([rows, reps]) => {
  const proto = Object.getPrototypeOf(AC.SFX);
  let src = proto.play.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const oc = new OfflineAudioContext(1, 48000 * 4, 48000);
  const S = Object.create(proto); S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = oc.createBuffer(1, 28800, 48000);
  const med = (v) => v.slice().sort((x, y) => x - y)[v.length >> 1];
  const out = {};
  for (const [k, kind, p] of [["cast", "ult", { w: "oracle" }], ["sigil", "ult", { w: "oracle-sigil" }],
                              ["hex", "ult", { w: "oracle-hex", n: 3 }], ["close", "ult", { w: "oracle-close" }],
                              ["hit", "hit", { dmg: 10, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickSight and resolveHit rows, applied to the real prototypes and run
# beside the originals; the survey of Foresight's windows comes out of the
# same runs.
WIRE_JS = r"""([seeds, sightRows, hitRows, N]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "oracle";
  const CAP = AC.STATUS.hex.maxStacks;
  const oS = P.tickSight, oH = P.resolveHit;
  const patch = (fn, rows, nm) => { let src = fn.toString();
    for (const [anc, code] of rows){ const at = src.split(anc).length - 1;
      if (at !== 1) throw new Error(`a ${nm} anchor occurs ${at} times in ${nm}()`);
      src = src.replace(anc, () => code); }
    return (0, eval)("(function " + src + ")"); };
  let pS, pH;
  try { pS = patch(oS, sightRows, "tickSight"); pH = patch(oH, hitRows, "resolveHit"); }
  catch (e){ return { err: String(e) }; }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inS = 0, inH = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        calls.push({ step, t: m.t, k: w, n: p.n === undefined ? null : p.n, fh: foe.stacks("hex"),
                     inS: !!inS, inH: !!inH, keys: Object.keys(p).join(",") });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const iS = wire ? pS : oS, iH = wire ? pH : oH;
    P.tickSight = function(dt){ inS++; try { return iS.call(this, dt); } finally { inS--; } };
    P.resolveHit = function(...a){ inH++; try { return iH.apply(this, a); } finally { inH--; } };
    const exp = { cast: {}, sigil: {}, hex: {}, close: {} };
    const wins = []; let W = null, prevZ = null, prevT = -1, lc = 0, lh = 0, n = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const T = f.sightTally, Z = f.ultSight;
        if (T){
          if (T.casts > lc){ exp.cast[step] = T.casts - lc; lc = T.casts; }
          if (T.hex > lh){ exp.hex[step] = (T.hex - lh) / f.w.ult.hex; lh = T.hex; }
        }
        if (Z && Z !== prevZ){
          if (W && !W.end) W.end = "recast";
          W = { castStep: step, cast: m.t, strikes: [], hexes: 0, end: null, close: null, closeStep: null };
          wins.push(W); prevT = -1;
        }
        if (Z && Z.t !== prevT){
          if (Math.round(Z.t / DT) % N === 1){ exp.sigil[step] = 1; W.strikes.push(m.t); }
          prevT = Z.t;
        }
        if (W && exp.hex[step] && Z) W.hexes += exp.hex[step];
        if (!Z && prevZ && W && !W.end){
          W.end = prevZ.t >= prevZ.dur ? (f.alive && foe.alive ? "clock" : "clock-dead") : "death";
          W.close = m.t; W.closeStep = step;
          if (W.end === "clock") exp.close[step] = 1;
        }
        prevZ = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickSight = oS; P.resolveHit = oH; if (had) S.play = op; else delete S.play; }
    const T = f.sightTally || {};
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.shield, m.b.shield, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.a.vx, m.a.vy, m.b.vx, m.b.vy, m.a.charge, m.b.charge,
                                  m.a.stacks("hex"), m.b.stacks("hex"), m.shots.length,
                                  m.winner ? m.winner.w.id : null, T]),
             calls, other: JSON.stringify(other), exp, wins, steps: n };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, "clock-dead": 0, death: 0, over: 0, recast: 0 };
  const tot = { cast: 0, castV: 0, sigil: 0, sigilV: 0, hex: 0, hexV: 0, close: 0, closeV: 0 };
  const nh = new Array(CAP + 1).fill(0), pick = [], gaps = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a new voice"]);
    const kind = { [ME]: "cast", [ME + "-sigil"]: "sigil", [ME + "-hex"]: "hex", [ME + "-close"]: "close" };
    const byStep = {};
    for (const c of B.calls){
      if (!kind[c.k]){ bad.push([fid, sd, "an unknown oracle voice", c.k]); continue; }
      (byStep[c.step] = byStep[c.step] || { cast: 0, sigil: 0, hex: 0, close: 0 })[kind[c.k]]++;
      if (c.k === ME + "-hex"){
        if (!(Number.isInteger(c.n) && c.n >= 1 && c.n <= CAP && c.n === c.fh) || c.keys !== "w,n" || !c.inH)
          bad.push([fid, sd, "a snap's n is not the foe's count, or not in resolveHit", c.n, c.fh, c.keys]);
        else nh[c.n]++;
      } else if (c.k === ME + "-sigil" || c.k === ME + "-close"){
        if (c.keys !== "w" || !c.inS) bad.push([fid, sd, "a sigil or close voice with opts, or outside tickSight", c.k]);
      } else if (c.keys !== "w") bad.push([fid, sd, "the cast carries opts", c.keys]);
    }
    const steps = new Set([...Object.keys(byStep), ...Object.keys(B.exp.cast), ...Object.keys(B.exp.sigil),
                           ...Object.keys(B.exp.hex), ...Object.keys(B.exp.close)]);
    for (const k of steps){
      const got = byStep[k] || { cast: 0, sigil: 0, hex: 0, close: 0 };
      for (const q of ["cast", "sigil", "hex", "close"]){
        const e = B.exp[q][k] || 0;
        tot[q] += e; tot[q + "V"] += got[q];
        if (e !== got[q]) bad.push([fid, sd, "step " + k, q, "expected", e, "voiced", got[q]]);
      }
    }
    for (const W of B.wins){
      ends[W.end]++;
      if (W.end === "clock"){
        pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, strikes: W.strikes.length, hexes: W.hexes });
        const s = W.strikes;
        let g = 0; for (let i = 1; i < s.length; i++) g = Math.max(g, s[i] - s[i - 1]);
        gaps.push([g, W.close - s[s.length - 1], s.length]);
      }
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, tot, nh, pick, gaps,
           bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Foresight's.
RECORD_JS = r"""([side, fid, sd, sightRows, hitRows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "oracle";
  const oS = P.tickSight, oH = P.resolveHit;
  const patch = (fn, rows) => { let src = fn.toString();
    for (const [anc, code] of rows) src = src.replace(anc, () => code);
    return (0, eval)("(function " + src + ")"); };
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickSight = patch(oS, sightRows); P.resolveHit = patch(oH, hitRows);
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickSight = oS; P.resolveHit = oH; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds, N]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, ME = "oracle";
  const CAP = AC.STATUS.hex.maxStacks;
  const res = [];
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.n === undefined ? null : p.n, foe.stacks("hex")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    let n = 0, strikes = 0, closes = 0, prevZ = null, prevT = -1;
    try {
      while (!m.over && n < 170 / DT){
        m.step(DT); n++;
        const Z = f.ultSight;
        if (Z && Z !== prevZ) prevT = -1;
        if (Z && Z.t !== prevT){ if (Math.round(Z.t / DT) % N === 1) strikes++; prevT = Z.t; }
        if (!Z && prevZ && prevZ.t >= prevZ.dur && f.alive && foe.alive) closes++;
        prevZ = Z;
      }
    } finally { if (had) S.play = op; else delete S.play; }
    const T = f.sightTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                    m.a.stacks("hex"), m.b.stacks("hex"),
                                    m.winner ? m.winner.w.id : null, f.sightTally || null]),
               casts: T.casts || 0, hexes: (T.hex || 0) / f.w.ult.hex, strikes, closes,
               castV: log.filter(e => e[0] === ME).length,
               sigilV: log.filter(e => e[0] === ME + "-sigil").length,
               hexV: log.filter(e => e[0] === ME + "-hex").length,
               badN: log.filter(e => e[0] === ME + "-hex" && (e[1] !== e[2] || e[1] < 1 || e[1] > CAP)).length,
               closeV: log.filter(e => e[0] === ME + "-close").length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def bandpass(x, lo, hi):
    np = _np()
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X[(fr < lo) | (fr >= hi)] = 0
    return np.fft.irfft(X, len(x))


def third(x, fc):
    return bandpass(x, fc / 2 ** (1 / 6), fc * 2 ** (1 / 6))


def band_of(f):
    """The BANDS third-octave a frequency sits in."""
    np = _np()
    return BANDS[int(np.argmin([abs(math.log(fc / f)) for fc in BANDS]))]


def centroid_seg(draws, a, b):
    """The draw-averaged power centroid over [a, b] s (Hann, 2^14)."""
    np = _np()
    NF = 1 << 14
    P = 0.0
    for x in draws:
        seg = x[int(a * SR):int(b * SR)]
        P = P + np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NF)) ** 2
    fr = np.fft.rfftfreq(NF, 1 / SR)
    return float((P * fr).sum() / P.sum())


def mod_rate(x, a, b):
    """RATE: the peak of the 1 ms RMS envelope's spectrum (dB, detrended), 2-80 Hz."""
    np = _np()
    e, c = env(x, 0.001, 0.001)
    m = (c >= a) & (c <= b)
    y = 20 * np.log10(np.maximum(e[m], 1e-9))
    y = y - np.convolve(y, np.ones(250) / 250, mode="same")
    y = y[125:-125] if len(y) > 400 else y
    Y = np.abs(np.fft.rfft(y * np.hanning(len(y)), 1 << 16)); fr = np.fft.rfftfreq(1 << 16, 0.001)
    k = (fr >= 2) & (fr <= 80)
    return float(fr[k][np.argmax(Y[k])])


def depth(x, a, b):
    """SHIMMER: p95 - p5 of the 5 ms RMS (dB, 1 ms hop) over [a, b] s."""
    np = _np()
    e, c = env(x, 0.005, 0.001)
    m = (c >= a) & (c <= b)
    y = 20 * np.log10(np.maximum(e[m], 1e-9))
    return float(np.percentile(y, 95) - np.percentile(y, 5))


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v75 §6.2 turned into a number (the
# readings in the docstring); a rule no candidate passes exits 1 rather than
# picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'a filtered inhale': the breath alone swells "
    "(BREATH-RISE >= 40 ms), its band climbs (CEN-RISE >= 1.19 over its swell) "
    "and it is air (TONAL <= 10 dB); 'into': the chime's onset within 40 ms of "
    "the breath's top and no DIP on the whole voice's way up; 'a soft chime': "
    "the chime alone a note (TONAL >= 20 dB, within 25 cents of its declared "
    "note) with a soft onset (RISE >= 8 ms). Level: TOP between 0.5x the blow's "
    "loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST, every draw. "
    "Register against rune-crack, the school's and the type's casts, the "
    "school's snap, the bowstring, the blow and the death voice each <= 0.80. "
    "Tiebreak: the most distinct register (the highest of those, to 0.05), then "
    "the fewest calls.")

SIGIL_RULE = (
    "'2-3 kHz band': BAND >= 0.90; 'peak <= 0.15': PEAK <= 0.15; 'very quiet': "
    "steady TOP between the bowstring's (loudest draw) and half the wall tick's "
    "(quietest draw); still heard: OVER-MED >= +6 dB and OVER-MIN >= +3 dB over "
    "the score in its third-octave; 'shimmer': SHIMMER 2-6 dB at a RATE of 4-20 "
    "Hz; 'while it is drawn': under the score for good by 0.3 s after the close "
    "(the last strike N-1 frames before it). Register of the steady shimmer "
    "against the wall tick, the bowstring, the blow, rune-crack and the death "
    "voice each <= 0.80 (against the school's snap and the cast: printed -- "
    "§6.2 puts the snap and the shimmer in one band; one is 25 ms, one 8 s). "
    "Tiebreak: the most distinct register (to 0.05), then the fewest calls a "
    "second.")

SNAP_RULE = (
    "'pitch by count': the snap's pitch at every count within 25 cents of its "
    "declared step from count 1 and rising >= 30 cents with every count; 'a hex "
    "snap': count 1 IS the school's snap (to TOL) and TOP within 3 dB of the "
    "school's at every count; heard ON the blow: OVER-HIT >= +6 dB at every count "
    "on every draw. Register (count 3) against the blow, the wall tick, the "
    "bowstring, rune-crack and the death voice each <= 0.80. Tiebreak: the most "
    "distinct register (to 0.05), then the count heard best (the largest "
    "smallest step, to 10 cents), then the fewest calls.")

CLOSE_RULE = (
    "'reversed': LATE >= 0.5, the loudest 50 ms centred in the last 40% of the "
    "audible span, ENV-CORR >= 0.80 against the LITERAL reversal of the picked "
    "chime; 'the chime': the chime's note within 25 cents over its loudest "
    "100 ms, TONAL >= 20 dB, TOP within 3 dB of the chime's own. Register "
    "against the cast: printed. Tiebreak: the closest to the literal "
    "(ENV-CORR, to 0.02), then the fewest calls.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not AUD_LO <= M["aud"] <= AUD_HI: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["brise"] is None or M["brise"] < 40:
        why.append("no breath" if M["brise"] is None else f"breath-rise {M['brise']:.0f} ms < 40 (a strike)")
    if M["cenrise"] is None or M["cenrise"] < 1.19:
        why.append("no breath" if M["cenrise"] is None else f"the band climbs x{M['cenrise']:.2f} < 1.19")
    if M["itonal"] is not None and M["itonal"] > 10: why.append(f"the breath is tonal {M['itonal']:.1f} dB > 10")
    if M["hand"] is None or M["hand"] > 40:
        why.append("no handover" if M["hand"] is None else f"the chime {M['hand']:.0f} ms off the breath's top")
    if M["dips"]: why.append(f"{M['dips']} dip(s) on the way up")
    if M["ctonal"] is None or M["ctonal"] < 20:
        why.append("no chime" if M["ctonal"] is None else f"the chime is not a note (tonal {M['ctonal']:.1f} dB)")
    if M["cerr"] is not None and M["cerr"] > 25: why.append(f"the chime {M['cerr']:.0f} cents off its note")
    if M["soft"] is not None and M["soft"] < 8: why.append(f"the chime's rise {M['soft']:.0f} ms < 8 (a click)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (quietest draw)")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (loudest draw)")
    return why


def sigil_why(M, lev):
    why = []
    if M["band"] < 0.90: why.append(f"band {M['band']:.2f} < 0.90")
    if M["peak"] > 0.15: why.append(f"peak {M['peak']:.3f} > 0.15")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.5f} < the bowstring's {lev['lo']:.5f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.5f} > half the wall tick's {lev['hi']:.5f}")
    if M["omed"] < 6: why.append(f"over the score {M['omed']:+.1f} dB (median) < +6")
    if M["omin"] < 3: why.append(f"over the score {M['omin']:+.1f} dB (min) < +3: a gap")
    if not 2 <= M["depth"] <= 6: why.append(f"shimmer {M['depth']:.1f} dB, not 2-6")
    if not 4 <= M["rate"] <= 20: why.append(f"rate {M['rate']:.1f} Hz, not 4-20")
    if M["gone"] > FADE: why.append(f"heard {M['gone']:.2f} s after the close (> {FADE})")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def snap_why(M, lev):
    why = []
    if M["perr"] > 25: why.append(f"a count's pitch {M['perr']:.0f} cents off its step")
    if not M["rising"]: why.append("the pitch does not rise >= 30 cents with every count")
    if M["dtop"] > 3: why.append(f"TOP {M['dtop']:.1f} dB off the school's snap")
    if M["overhit"] < 6: why.append(f"over the blow {M['overhit']:+.1f} dB < +6 (worst count and draw)")
    if not M["is_school"]: why.append("count 1 is not the school's snap")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    if M["late"] < 0.5: why.append(f"late {M['late']:.2f} < 0.5")
    if M["top_pos"] < 0.6: why.append(f"its loudest 50 ms at {M['top_pos']:.2f} of its span (< 0.60)")
    if M["ecorr"] < 0.80: why.append(f"env-corr {M['ecorr']:.2f} < 0.80 with the literal")
    if M["perr"] > 25: why.append(f"{M['perr']:.0f} cents off the chime's note")
    if M["tonal"] < 20: why.append(f"tonal {M['tonal']:.1f} dB < 20")
    if abs(M["dtop"]) > 3: why.append(f"TOP {M['dtop']:+.1f} dB re the chime's")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="Oracle's stage-5 link (the relic built, no voices)")
    ap.add_argument("--out", default="../05-reference/v105")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=105701)
    ap.add_argument("--e2e-seeds", type=int, default=1, help="fight seeds a pairing, end to end (0 skips it)")
    ap.add_argument("--peer-rows", action="append", default=[],
                    help="another relic's rows json: its Sfx rows are co-applied with these, both orders")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "sigil": SIGIL_RULE, "snap": SNAP_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickSight tally", SIGIL_ANCHOR), ("resolveHit second hex", HEX_ANCHOR),
                    ("tickSight close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if re.search(r'w === "oracle(-[a-z]+)?"', html) or '"oracle-sigil"' in html or '"oracle-hex"' in html:
        raise SystemExit(f"{gp.name} already carries Foresight's voices -- run on the stage-5 link")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nFORESIGHT -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")
    sizes = {}

    def wav(name, x):
        sizes[name] = write_wav(out / name, x)

    e2e_ref = {}
    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        info0 = page.evaluate("""() => {
          const s = Object.getPrototypeOf(AC.SFX).play.toString();
          const arms = [...new Set([...s.matchAll(/w === "([a-z-]+)"/g)].map(m => m[1]))];
          const kinds = [...new Set([...s.matchAll(/kind === "([a-z-]+)"/g)].map(m => m[1]))];
          const i = s.indexOf('kind === "hex-snap"'), j = s.indexOf('else if (kind === "seal")', i);
          const me = AC.WEAPONS.find(w => w.id === "oracle");
          return { arms, kinds, cap: AC.STATUS.hex.maxStacks, dmg: me.dmg, u: me.ult, shot: me.shot,
                   dt: AC.CONFIG.physics.dt, snap: s.slice(i, j),
                   W: AC.WEAPONS.map(w => [w.id, w.aff, w.shape]) };
        }""")
        if info0["cap"] != CAP:
            raise SystemExit(f"STATUS.hex.maxStacks is {info0['cap']}, not {CAP}")
        if abs(1 / info0["dt"] - FRAME) > 1e-9:
            raise SystemExit(f"physics dt is {info0['dt']}, not 1/{FRAME}")
        u0 = info0["u"]
        if abs(info0["dmg"] - BLADE) > 1e-9 or u0.get("kind") != "sight" or u0.get("dur") != DUR or u0.get("hex") != 1:
            raise SystemExit(f"Oracle on this page is not stage 5's: dmg {info0['dmg']}, ult {u0}")
        snap_lines = [l_.strip() for l_ in info0["snap"].splitlines() if l_.strip().startswith("this._")]
        if "\n".join(snap_lines) != SNAP_SRC:
            raise SystemExit("the page's hex-snap is not the school's snap this lab transposes:\n" + "\n".join(snap_lines))
        print(f"  Oracle: blade {info0['dmg']}, ult {u0['kind']} dur {u0['dur']} hex {u0['hex']} turn {u0['turn']}; "
              f"hex cap {CAP}; the school's hex-snap read off play(): the three calls this lab transposes")
        arms_now = set(info0["arms"])
        SCHOOL = tuple(w for w, aff, sh in info0["W"] if aff == "runic" and w != ME and w in arms_now)
        TYPE = tuple(w for w, aff, sh in info0["W"] if sh == "bow" and w != ME and w in arms_now)
        FALL = tuple(w for w, aff, sh in info0["W"] if w not in arms_now)
        print(f"  the school's casts (runic, with an arm): {', '.join(SCHOOL)};  the type's (bow): {', '.join(TYPE)}")
        print(f"  THE SYNTH'S KINDS ({len(info0['kinds'])}): {', '.join(info0['kinds'])}")
        rec.update(school=SCHOOL, type=TYPE, kinds=info0["kinds"])

        def R(evs, secs=3.0, seed=None, rows=None):
            for e in evs:
                if e[0] in ("body", "lit"):
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            new = any(e[0] in ("body", "lit") or (e[0] == "arm" and e[2] == "ult" and str(e[3].get("w", "")).startswith(ME))
                      for e in evs)
            if new and len(evs) == 1:
                for d_ in r["log"]["burst"]:
                    if d_ > 0.55: raise SystemExit(f"REFUSING: a _burst of {d_}s")
                for d_ in r["log"]["sweep"]:
                    if d_ > 0.58: raise SystemExit(f"REFUSING: a _sweep of {d_}s")
            if float(np.abs(x).max()) < 1e-6:
                raise SystemExit(f"SILENT render: {str(evs[:1])[:120]}")
            if min(e[1] for e in evs) >= T0 and float(np.abs(x[:int(T0 * SR) - 2]).max()) > 1e-6:
                raise SystemExit("sound BEFORE t=1.0")
            return x, r["calls"]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        REFS = [("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                ("BAR", ["play", T0, "ult", {"w": "axiom"}]),
                ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                ("hit@10", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("wall", ["play", T0, "wall", {}]),
                ("loose", ["play", T0, "loose", {}]),
                ("hex-snap", ["play", T0, "hex-snap", {}]),
                ("death", ["play", T0, "death", {}]),
                ("clank", ["play", T0, "clank", {"mass": 1.6}])]
        REFS += [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in SCHOOL + TYPE if r_ != "axiom"]
        REFS += [(f"{r_} now", ["play", T0, "ult", {"w": r_}]) for r_ in FALL]
        for name, ev in REFS:
            x, _ = R([ev])
            ctl[name] = dict(basic(x), x=x)
            M = ctl[name]
            if not name.endswith(" now"):
                print(f"  {name:<13} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
                      f"loudest 50 ms {M['top']:.4f}   centroid {M['cen']:6.0f} Hz")
        repro = [("rune-crack peak", ctl["rune-crack"]["peak"], 0.608, 0.01),
                 ("rune-crack audible", ctl["rune-crack"]["aud"], 450, 10),
                 ("BAR peak", ctl["BAR"]["peak"], 0.364, 0.01), ("BAR audible", ctl["BAR"]["aud"], 300, 10),
                 ("hit@11.6 peak", ctl["hit@11.6"]["peak"], 0.443, 0.01),
                 ("hit@11.6 audible", ctl["hit@11.6"]["aud"], 80, 10)]
        bad = [f"{n}: {v:.3f} vs {p_}" for n, v, p_, t_ in repro if abs(v - p_) > t_]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
                                    f"PASS  all {len(repro)} published numbers come back"))
        if bad:
            raise SystemExit("the controls do not reproduce -- nothing new is quoted")
        rcx = ctl["rune-crack"]["x"]
        fall = {k: float(np.abs(ctl[f"{k} now"]["x"] - rcx).max()) for k in FALL}
        print(f"  ARE rune-crack today ({len(FALL)} relics with no arm; max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if max(fall.values()) > 1e-6 or ME not in fall:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        n_rc = len(FALL) - 1
        SCH = tuple(("BAR" if r_ == "axiom" else r_) for r_ in SCHOOL)
        DKEYS = ("hit@10", "wall", "loose", "hex-snap", "rune-crack", "death") + SCH + TYPE
        D = {k: [] for k in DKEYS}
        for sd in NOISE_SEEDS:
            for k in D:
                x_ = R([dict(REFS)[k]], seed=sd)[0]
                D[k].append(basic(x_))
        h_lo, h_hi = min(m["top"] for m in D["hit@10"]), max(m["top"] for m in D["hit@10"])
        w_lo = min(m["top"] for m in D["wall"])
        l_hi = max(m["top"] for m in D["loose"])
        s_top = basic(ctl["hex-snap"]["x"])["top"]
        print(f"  across {len(NOISE_SEEDS)} draws: the blow (hit @ {BLADE:g}) loudest 50 ms {h_lo:.4f}-{h_hi:.4f}; the wall "
              f"tick {w_lo:.4f}-{max(m['top'] for m in D['wall']):.4f}; the bowstring "
              f"{min(m['top'] for m in D['loose']):.5f}-{l_hi:.5f}; the school's snap "
              f"{min(m['top'] for m in D['hex-snap']):.4f}-{max(m['top'] for m in D['hex-snap']):.4f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        P90 = bed_p90(bseg)
        SC50 = {}

        def score50(fc):
            """the score's p90 of the 50 ms RMS inside the third-octave at fc"""
            if fc not in SC50:
                e_, _c = env(third(bseg, fc), 0.05, 0.005)
                SC50[fc] = float(np.percentile(e_, 90))
            return SC50[fc]

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        def reg_to(DB, DB2):
            return float(np.median([cos(DB[i], DB2[i]) for i in range(len(DB))]))

        rec["levels"] = dict(hit=[h_lo, h_hi], wall_lo=w_lo, loose_hi=l_hi, snap_top=s_top)
        wav("oracle-ctl-runecrack.wav", rcx)
        wav("oracle-ctl-hit10.wav", ctl["hit@10"]["x"])
        wav("oracle-ctl-hexsnap.wav", ctl["hex-snap"]["x"])
        wav("oracle-ctl-loose.wav", ctl["loose"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a rune-eye open: a filtered inhale into a soft chime, 0.4s'. Level-matched: TOP {tgt_c:.4f} "
              f"(the centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}); the chime's decay solved to AUDIBLE {CAST_AUD:g} ms; "
              f"the breath {INHALE_UNDER_DB:g} dB under the chime")

        def cx(sp, g, ki, dc, parts=None, seed=None):
            return R([["body", T0, cast_body(sp, g, ki, dc, parts), {}]], seed=seed)

        def calib_cast(sp):
            parts = sp.get("parts", ("inhale", "chime"))
            g, ki, dc = 0.1, 4.0, 0.6
            for _ in range(3):
                if "inhale" in parts and "chime" in parts:
                    ti = basic(cx(sp, g, ki, dc, ("inhale",))[0])["top"]
                    tc = basic(cx(sp, g, ki, dc, ("chime",))[0])["top"]
                    ki = float(f"{ki * tc * 10 ** (-INHALE_UNDER_DB / 20) / ti:.4g}")
                if "chime" in parts:
                    lo_, hi_ = math.log(0.1), math.log(3.0)
                    for _ in range(12):
                        mid = 0.5 * (lo_ + hi_)
                        if basic(cx(sp, g, ki, math.exp(mid))[0])["aud"] < CAST_AUD: lo_ = mid
                        else: hi_ = mid
                    dc = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = float(f"{g * tgt_c / basic(cx(sp, g, ki, dc)[0])['top']:.4g}")
            return g, ki, dc

        CREFS = ("rune-crack",) + SCH + TYPE + ("hex-snap", "loose", "hit@10", "death")

        def cast_measure(sp, g, ki, dc, name):
            parts = sp.get("parts", ("inhale", "chime"))
            x, calls = cx(sp, g, ki, dc)
            if float(np.abs(x - cx(sp, g, ki, dc)[0]).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x)
            M.update(x=x, calls=calls[0], g=g, ki=ki, dc=dc, name=name, sp=sp)
            draws = [cx(sp, g, ki, dc, seed=sd)[0] for sd in NOISE_SEEDS]
            bs = [basic(d_) for d_ in draws]
            M["top_lo"] = min(b_["top"] for b_ in bs); M["top_hi"] = max(b_["top"] for b_ in bs)
            M["dips"] = breath(draws, M["a0"], M["aud"])[1]
            M["brise"] = M["cenrise"] = M["itonal"] = M["hand"] = None
            M["ctonal"] = M["cerr"] = M["soft"] = M["cpitch"] = None
            if "inhale" in parts:
                idr = [cx(sp, g, ki, dc, ("inhale",), seed=sd)[0] for sd in NOISE_SEEDS]
                ib = basic(idr[0])
                M["brise"] = breath(idr, ib["a0"], ib["aud"])[0]
                itop = float(np.mean([basic(d_)["top_at"] for d_ in idr]))
                a_, b_ = T0 + ib["a0"] / 1000, T0 + itop
                if b_ - a_ > 0.02:
                    m_ = 0.5 * (a_ + b_)
                    M["cenrise"] = centroid_seg(idr, m_, b_) / centroid_seg(idr, a_, m_)
                else:
                    M["cenrise"] = 0.0
                M["itonal"] = tonal(idr, a_, b_ + 0.01, 100.0, 8000.0)
                e25 = [env(d_[int(T0 * SR):], 0.025, 0.001) for d_ in idr]
                ec = np.mean([e_[0] for e_ in e25], axis=0)
                M["itop_ms"] = float(e25[0][1][int(np.argmax(ec))] * 1000)
            if "chime" in parts:
                xc = cx(sp, g, ki, dc, ("chime",))[0]
                cb = basic(xc)
                M["soft"] = cb["rise"]
                e1, c1 = env(xc[int(T0 * SR):], 0.001, 0.001)
                M["con_ms"] = float(c1[int(np.argmax(e1 > 0.1 * e1.max()))] * 1000)
                t1 = T0 + M["con_ms"] / 1000
                note = sp["note"]
                M["cpitch"] = pitch(xc, t1 + 0.03, t1 + 0.15, lo=note * 0.8, hi=note * 1.25)
                M["cerr"] = abs(cents(M["cpitch"], note))
                M["ctonal"] = tonal([xc], t1 + 0.01, t1 + 0.2, 200.0, 12000.0)
                M["ctop"] = cb["top"]
                M["cx"] = xc
                if "inhale" in parts:
                    M["hand"] = abs(M["itop_ms"] - M["con_ms"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in CREFS}
            M["why"] = cast_why(M, lev_c)
            return M

        abbr = {k: k[:4] for k in CREFS}
        abbr.update({"rune-crack": "rc", "hit@10": "hit", "death": "dth", "hex-snap": "snap", "loose": "strg"})

        def f_(v, spec, none="-"):
            return none if v is None else format(v, spec)

        print(f"  {'cand':<10}{'g':>7}{'ki':>7}{'dc':>6}{'calls':>6}{'top':>16}{'aud':>5}{'brise':>6}{'cen^':>5}"
              f"{'iton':>5}{'hand':>5}{'dips':>5}{'cton':>5}{'c-err':>6}{'soft':>5}" + "".join(f"{abbr[k]:>5}" for k in CREFS))

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>7.4g}{M['ki']:>7.4g}{M['dc']:>6.3g}{M['calls']:>6d}"
                  f"{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}{M['aud']:>5.0f}{f_(M['brise'], '.0f'):>6}"
                  f"{f_(M['cenrise'], '.2f'):>5}{f_(M['itonal'], '.1f'):>5}{f_(M['hand'], '.0f'):>5}{M['dips']:>5d}"
                  f"{f_(M['ctonal'], '.0f'):>5}{f_(M['cerr'], '.0f'):>6}{f_(M['soft'], '.0f'):>5}"
                  + "".join(f"{r_[k]:>5.2f}" for k in CREFS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, ki, dc = calib_cast(sp)
            M = cast_measure(sp, g, ki, dc, name)
            rows_c.append(M); cast_line(M)
            wav(f"oracle-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for name, sp, blurb in CAST_CONTROLS:
            g, ki, dc = calib_cast(sp)
            M = cast_measure(sp, g, ki, dc, name)
            ctlc.append(M); cast_line(M)
            wav(f"oracle-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        x, calls = R([["play", T0, "ult", {"w": ME}]])
        M = basic(x)
        M.update(x=x, calls=calls[0], g=0.0, ki=0.0, dc=0.0, name="0 RC-NOW", sp=None, dips=0, brise=None,
                 cenrise=None, itonal=None, hand=None, ctonal=None, cerr=None, soft=None)
        draws = [R([["play", T0, "ult", {"w": ME}]], seed=sd)[0] for sd in NOISE_SEEDS]
        M["top_lo"] = min(basic(d_)["top"] for d_ in draws); M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
        M["regs"] = {k: reg([bands(d_[int(T0 * SR):]) for d_ in draws], k) for k in CREFS}
        M["why"] = cast_why(M, lev_c)
        ctlc.append(M); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES + CAST_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print("    0 RC-NOW   what ult/oracle plays today (rune-crack) -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlc:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, breath x{C_['ki']}, chime decay {C_['dc']} s; {C_['calls']} synth calls; "
              f"TOP {db(C_['top_lo'] / h_lo):+.1f} to {db(C_['top_hi'] / h_lo):+.1f} dB re the blow (quietest draw); "
              f"the chime alone {C_['ctop']:.4f}")

        # ---- THE SIGIL -----------------------------------------------------
        lev_s = dict(lo=l_hi, hi=0.5 * w_lo)
        tgt_s = math.sqrt(lev_s["lo"] * lev_s["hi"])
        TRAIN = 2.4                                  # seconds of strikes; then the close
        print(f"\nSIGIL -- 'a very quiet sustained shimmer (re-struck, 2-3 kHz band, peak <= 0.15) while it is drawn'. "
              f"Level-matched: steady TOP {tgt_s:.5f} (the centre of {lev_s['lo']:.5f}, the bowstring's loudest, and "
              f"{lev_s['hi']:.5f}, half the wall tick's quietest). A train of strikes N/120 s apart for {TRAIN} s, then "
              f"the close N-1 frames at most after the last strike; 'over' = dB over the score's p90 in the third-octave")

        def train(sp, g, secs=TRAIN):
            N = sp["N"]
            k_ = int(round(secs * FRAME / N))
            ts = [T0 + i * N / FRAME for i in range(k_)]
            body = sigil_body(sp, g)
            return R([["body", t_, body, {}] for t_ in ts], secs=T0 + secs + 2.5), ts

        def calib_sigil(sp):
            g = 0.002
            tgt = tgt_s * 10 ** (sp.get("db", 0.0) / 20)
            for _ in range(4):
                (x_, _c), ts = train(sp, g)
                M_ = basic(x_)
                if "peak" in sp:
                    g = float(f"{g * sp['peak'] / M_['peak']:.4g}")
                else:
                    e_, c_ = env(x_, 0.05)
                    st = (c_ >= ts[0] + 0.6) & (c_ <= ts[-1])
                    g = float(f"{g * tgt / float(e_[st].max()):.4g}")
            return g

        SREFS = ("wall", "loose", "hit@10", "rune-crack", "death")

        def sigil_measure(sp, g, name):
            (x, calls), ts = train(sp, g)
            (x2, _), _ = train(sp, g)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a sigil render does not reproduce")
            a_, b_ = ts[0] + 0.6, ts[-1]
            e_, c_ = env(x, 0.05)
            st = (c_ >= a_) & (c_ <= b_)
            M = dict(name=name, sp=sp, g=g, x=x, calls=calls[0], cps=calls[0] * FRAME / sp["N"])
            M["top"] = float(e_[st].max()); M["peak"] = float(np.abs(x).max())
            seg = x[int(a_ * SR):int(b_ * SR)]
            P = np.abs(np.fft.rfft(seg)) ** 2; fr = np.fft.rfftfreq(len(seg), 1 / SR)
            M["band"] = float(P[(fr >= 2000) & (fr <= 3000)].sum() / P.sum())
            f0_ = max(sp["parts"], key=lambda p_: p_[1])[0]
            fc = band_of(f0_)
            eb, cb = env(third(x, fc), 0.05, 0.005)
            ov = 20 * np.log10(np.maximum(eb, 1e-12) / score50(fc))
            m_ = (cb >= a_) & (cb <= b_)
            M["omed"] = float(np.median(ov[m_])); M["omin"] = float(ov[m_].min()); M["fc"] = fc
            M["depth"] = depth(x, a_, b_)
            M["rate"] = mod_rate(x, a_, b_)
            gap = close_gap(sp["N"])
            tc = ts[-1] + gap / FRAME
            heardc = np.nonzero((cb > ts[-1]) & (ov >= 0))[0]
            M["gone"] = float(max(0.0, (cb[heardc[-1]] + 0.025 - tc) if len(heardc) else 0.0))
            M["gap"] = gap
            M["DB"] = [bands(seg)] * len(NOISE_SEEDS)
            M["regs"] = {k: reg(M["DB"], k) for k in SREFS}
            M["reg_snap"] = reg(M["DB"], "hex-snap")
            M["why"] = sigil_why(M, lev_s)
            return M

        print(f"  {'cand':<10}{'g':>9}{'N':>4}{'D':>7}{'/s':>6}{'top':>9}{'peak':>7}{'band':>6}{'o-med':>7}{'o-min':>7}"
              f"{'shim':>6}{'rate':>6}{'gone':>6}" + "".join(f"{abbr.get(k, k[:4]):>5}" for k in SREFS) + f"{'snap':>6}")

        def sigil_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>9.4g}{M['sp']['N']:>4d}{M['sp']['D']:>7.4g}{M['cps']:>6.1f}{M['top']:>9.5f}"
                  f"{M['peak']:>7.4f}{M['band']:>6.2f}{M['omed']:>+7.1f}{M['omin']:>+7.1f}{M['depth']:>6.1f}{M['rate']:>6.1f}"
                  f"{M['gone']:>6.2f}" + "".join(f"{r_[k]:>5.2f}" for k in SREFS) + f"{M['reg_snap']:>6.2f}")

        rows_s = []
        for name, sp, blurb in SIGIL_CANDIDATES:
            M = sigil_measure(sp, calib_sigil(sp), name)
            rows_s.append(M); sigil_line(M)
            wav(f"oracle-sigil-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctls = []
        for name, sp, blurb in SIGIL_CONTROLS:
            M = sigil_measure(sp, calib_sigil(sp), name)
            ctls.append(M); sigil_line(M)
            wav(f"oracle-sigil-{name.replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in SIGIL_CANDIDATES + SIGIL_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print(f"  RULE  {SIGIL_RULE}")
        for M in rows_s:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctls:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_s, "sigil")
        si = fb if ok is None else min(ok, key=lambda i: (round(max(rows_s[i]["regs"].values()) / 0.05),
                                                          rows_s[i]["cps"]))
        S_ = rows_s[si]
        NS = S_["sp"]["N"]
        print(f"  PICK  {S_['name']}  g {S_['g']}, every {NS} window frames ({FRAME / NS:g} strikes a second, "
              f"{S_['cps']:.1f} synth calls a second); steady TOP {S_['top']:.5f} = {db(S_['top'] / l_hi):+.1f} dB re the "
              f"bowstring, {db(S_['top'] / w_lo):+.1f} dB re the wall tick, {db(S_['top'] / h_lo):+.1f} dB re the blow; "
              f"peak {S_['peak']:.4f}")

        # ---- THE SNAP ------------------------------------------------------
        print(f"\nSNAP -- 'the bow's own arrow voice plus a hex snap; pitch by count'. The school's snap at its own gains; "
              f"'over-hit' = the snap on the blow (hit @ {BLADE:g}) against the blow alone, in the snap's loudest "
              f"third-octave, first 50 ms, worst count and draw")

        def sx(sp, n, seed=None, with_hit=False):
            evs = [["body", T0, snap_body(sp), {"n": n}]]
            if with_hit:
                evs.append(["play", T0, "hit", {"dmg": BLADE, "crit": False}])
            return R(evs, secs=2.0, seed=seed)

        SNREFS = ("hit@10", "wall", "loose", "rune-crack", "death")
        hitx = {sd: R([["play", T0, "hit", {"dmg": BLADE, "crit": False}]], secs=2.0, seed=sd)[0]
                for sd in [None] + NOISE_SEEDS}
        snap0 = R([["play", T0, "hex-snap", {}]], secs=2.0)[0]

        def spec_avg(xs, a_, b_):
            NF = 1 << 16
            P_ = 0.0
            for x_ in xs:
                seg = x_[int(a_ * SR):int(b_ * SR)]
                P_ = P_ + np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NF)) ** 2
            fr = np.fft.rfftfreq(NF, 1 / SR)
            k = (fr >= 1500) & (fr <= 9000)
            i = int(np.nonzero(k)[0][np.argmax(P_[k])])
            y0, y1, y2 = np.log(P_[i - 1:i + 2] + 1e-30)
            d_ = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
            return (i + d_) * SR / NF

        def snap_measure(sp, name):
            M = dict(name=name, sp=sp)
            pit, tops, over, xs = [], [], [], {}
            for n in COUNTS:
                x, calls = sx(sp, n)
                if float(np.abs(x - sx(sp, n)[0]).max()) > TOL:
                    raise SystemExit(f"snap {name} does not reproduce")
                xs[n] = x
                M["calls"] = calls[0]
                draws = [sx(sp, n, seed=sd)[0] for sd in NOISE_SEEDS]
                pit.append(spec_avg(draws, T0, T0 + 0.045))
                tops.append(basic(x)["top"])
                bb = bands(x[int(T0 * SR):int((T0 + 0.05) * SR)])
                fc = max((v_, fc_) for v_, fc_ in zip(bb, BANDS) if fc_ >= 200)[1]
                for sd in [None] + NOISE_SEEDS:
                    xw = sx(sp, n, seed=sd, with_hit=True)[0]
                    over.append(db(band_rms(xw, fc, T0, T0 + 0.05) / max(band_rms(hitx[sd], fc, T0, T0 + 0.05), 1e-12)))
                if n == 3:
                    M["DB"] = [bands(d_[int(T0 * SR):]) for d_ in draws]
            steps = [cents(p_, pit[0]) for p_ in pit]
            M.update(xs=xs, x=xs[3], pitch=pit, steps=steps, tops=tops,
                     perr=max(abs(s_ - 100 * d_) for s_, d_ in zip(steps, sp["steps"])),
                     rising=all(steps[i + 1] - steps[i] >= 30 for i in range(len(steps) - 1)),
                     minstep=min(steps[i + 1] - steps[i] for i in range(len(steps) - 1)),
                     dtop=max(abs(db(t_ / s_top)) for t_ in tops), overhit=min(over),
                     is_school=float(np.abs(xs[1] - snap0).max()) <= TOL)
            M["regs"] = {k: reg(M["DB"], k) for k in SNREFS}
            M["reg_school"] = reg(M["DB"], "hex-snap")
            M["reg_sigil"] = reg_to(M["DB"], S_["DB"])
            M["why"] = snap_why(M, None)
            return M

        print(f"  {'cand':<9}{'calls':>6}{'pitch Hz (count 1-5)':>32}{'steps c':>26}{'err':>5}{'dtop':>6}{'o-hit':>7}"
              + "".join(f"{abbr.get(k, k[:4]):>5}" for k in SNREFS) + f"{'schl':>6}{'sigl':>6}")

        def snap_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['calls']:>6d}{'/'.join(f'{p_:.0f}' for p_ in M['pitch']):>32}"
                  f"{'/'.join(f'{s_:.0f}' for s_ in M['steps']):>26}{M['perr']:>5.0f}{M['dtop']:>6.1f}{M['overhit']:>+7.1f}"
                  + "".join(f"{r_[k]:>5.2f}" for k in SNREFS) + f"{M['reg_school']:>6.2f}{M['reg_sigil']:>6.2f}")

        rows_k = []
        for name, sp, blurb in SNAP_CANDIDATES:
            M = snap_measure(sp, name)
            rows_k.append(M); snap_line(M)
            for n in (1, CAP):
                wav(f"oracle-hex-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        ctlk = []
        for name, sp, blurb in SNAP_CONTROLS:
            M = snap_measure(sp, name)
            ctlk.append(M); snap_line(M)
        for (name, _sp, blurb) in SNAP_CANDIDATES + SNAP_CONTROLS:
            print(f"    {name:<9} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print(f"  RULE  {SNAP_RULE}")
        for M in rows_k:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctlk:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_k, "snap")
        ki_ = fb if ok is None else min(ok, key=lambda i: (round(max(rows_k[i]["regs"].values()) / 0.05),
                                                           -round(rows_k[i]["minstep"] / 10), rows_k[i]["calls"]))
        K_ = rows_k[ki_]
        print(f"  PICK  {K_['name']}  steps {K_['sp']['steps']} semitones at counts 1-5; pitch "
              + " / ".join(f"{p_:.0f}" for p_ in K_["pitch"]) + f" Hz; over the blow {K_['overhit']:+.1f} dB or more")

        # ---- THE CLOSE -----------------------------------------------------
        chime_top = C_["ctop"]
        cbody = cast_body(C_["sp"], C_["g"], C_["ki"], C_["dc"], ("chime",))
        print(f"\nCLOSE -- 'the chime reversed'. The picked cast's chime ({C_['name']}, decay {C_['dc']} s), its modes run "
              f"backwards; level-matched: TOP {chime_top:.4f} (the chime's own)")

        def zx(cp, gc, seed=None):
            return R([["body", T0, close_body(cp, C_, gc), {}]], seed=seed)

        def calib_close(cp):
            gc = C_["g"]
            for _ in range(3):
                gc = float(f"{gc * chime_top / basic(zx(cp, gc)[0])['top']:.4g}")
            return gc

        lit, _ = R([["lit", T0, cbody, 1.0, {}]])
        wav("oracle-close-0-literal.wav", lit)
        note = C_["sp"]["note"]

        def close_measure(x, calls, name, gc, cp):
            M = basic(x)
            M.update(x=x, calls=calls, name=name, gc=gc, cp=cp)
            a0, a1 = M["a0"] / 1000, (M["a0"] + M["aud"]) / 1000
            M["top_pos"] = (M["top_at"] - a0) / max(a1 - a0, 1e-9)
            M["ecorr"] = env_corr(x, lit)
            e_, c_ = env(x, 0.1)
            tt = float(c_[int(np.argmax(e_))])
            M["pitch"] = pitch(x, tt - 0.05, tt + 0.05, lo=note * 0.8, hi=note * 1.25)
            M["perr"] = abs(cents(M["pitch"], note))
            M["tonal"] = tonal([x], T0 + a0, T0 + a1, 200.0, 12000.0)
            M["dtop"] = db(M["top"] / chime_top)
            M["reg_cast"] = cos(bands(x[int(T0 * SR):]), bands(C_["x"][int(T0 * SR):]))
            M["why"] = close_why(M, None)
            return M

        print(f"  {'cand':<10}{'gc':>8}{'calls':>6}{'top':>8}{'dtop':>6}{'aud':>5}{'@top':>6}{'late':>6}{'ecorr':>7}"
              f"{'pitch':>8}{'tonal':>6}{'cast':>6}")

        def close_line(M):
            print(f"  {M['name']:<10}{M['gc']:>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{M['dtop']:>+6.1f}{M['aud']:>5.0f}"
                  f"{M['top_pos']:>6.2f}{M['late']:>6.2f}{M['ecorr']:>7.2f}{M['pitch']:>8.1f}{M['tonal']:>6.1f}"
                  f"{M['reg_cast']:>6.2f}")

        rows_z = []
        for name, cp, blurb in CLOSE_CANDIDATES:
            gc = calib_close(cp)
            x, calls = zx(cp, gc)
            if float(np.abs(x - zx(cp, gc)[0]).max()) > TOL:
                raise SystemExit("a close render does not reproduce")
            M = close_measure(x, calls[0], name, gc, cp)
            if cp.get("exhale"):
                M["top_lo"] = min(basic(zx(cp, gc, seed=sd)[0])["top"] for sd in NOISE_SEEDS)
            rows_z.append(M); close_line(M)
            wav(f"oracle-close-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlz = []
        g_again = float(f"{1.0:.4g}")
        xa_, ca_ = R([["body", T0, cbody, {}]])
        M = close_measure(xa_, ca_[0], "0 AGAIN", g_again, None)
        ctlz.append(M); close_line(M)
        M = close_measure(lit, 1, "0 LITERAL", 1.0, None)
        close_line(M)
        print("    " + "\n    ".join(f"{n_:<10} {b_}" for n_, _c, b_ in CLOSE_CANDIDATES))
        print("    0 AGAIN    the chime forward, played as the close -- a control\n"
              "    0 LITERAL  the chime's samples reversed (reference; cannot ship; the ENV-CORR target)")
        print(f"  RULE  {CLOSE_RULE}")
        for M in rows_z:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlz:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_z, "close")
        zi = fb if ok is None else min(ok, key=lambda i: (-round(rows_z[i]["ecorr"] / 0.02), rows_z[i]["calls"]))
        Z_ = rows_z[zi]
        print(f"  PICK  {Z_['name']}  gain {Z_['gc']}; ENV-CORR {Z_['ecorr']:.2f} with the literal; {Z_['calls']} synth calls")

        # ---- REGISTERS AMONG THE FOUR ----------------------------------------
        four = {"cast": C_["x"], "sigil": S_["x"][int((T0 + 0.6) * SR):], "snap": K_["x"], "close": Z_["x"]}
        fb4 = {k: bands(v[int(T0 * SR):] if k != "sigil" else v) for k, v in four.items()}
        print("\n  register among the four picks: " + ", ".join(
            f"{a_}/{b_} {cos(fb4[a_], fb4[b_]):.2f}" for i, a_ in enumerate(fb4) for b_ in list(fb4)[i + 1:]))
        rec["regs4"] = {f"{a_}/{b_}": cos(fb4[a_], fb4[b_]) for i, a_ in enumerate(fb4) for b_ in list(fb4)[i + 1:]}

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   sigil {S_['name']}   snap {K_['name']}   close {Z_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        cn, sn, kn, zn = (X["name"].split()[1] for X in (C_, S_, K_, Z_))
        what_c = {"1 BELL": "a sine at A6 (1760 Hz) with a faint bar mode (2.76x at 0.25)",
                  "2 GLASS": "an A6 glass (1760 Hz; shell modes 2.32x at 0.3 and 4.25x at 0.1)",
                  "3 SIGIL": "the sigil's own note, E7 (2640 Hz), with a faint bar mode",
                  "4 FIFTH": "A6 and E7 together (1760 and 2640 Hz, the sigil's note on top)",
                  "5 LOW": "a sine at A5 (880 Hz) with a faint bar mode"}[C_["name"]]
        f0c, f1c = inhale_band(C_["sp"]["note"])
        c_cast = _wrap([
            f'ORACLE\'S CAST, THE EYE OPENING -- v75 §6.2: "cast: a rune-eye \'open\' -- a filtered inhale into a soft '
            f'chime, 0.4s". {cn}, of {len(CAST_CANDIDATES)}, picked on the numbers by `oracle_voice_lab.py` under Rick\'s '
            f'"you pick i overrule" (v105). Oracle had no arm and fell through to rune-crack, which {n_rc} other '
            f'relics on its stage-5 link still use, so this ADDS arms before that fallback and leaves it alone.',
            f"The breath: band-passed noise swelling for {AI:g} s (the longest attack a `_sweep` allows), its band "
            f"climbing {f0c:g} -> {f1c:g} Hz so it passes the chime's note at its top (x{C_['cenrise']:.2f} over its "
            f"swell, rise {C_['brise']:.0f} ms, no peak more than {C_['itonal']:.1f} dB over its neighbours: air). At "
            f"its top ({C_['hand']:.0f} ms off) the chime: {what_c}, struck as four in-phase strikes over 30 ms, so it "
            f"enters in {C_['soft']:.0f} ms and not as a click. Audible {C_['aud']:.0f} ms; loudest 50 ms "
            f"{db(C_['top_lo'] / h_lo):+.1f} to {db(C_['top_hi'] / h_lo):+.1f} dB re the blow. Register at most "
            f"{max(C_['regs'].values()):.2f} against rune-crack, the runic and bow casts, the school's snap, the "
            f"bowstring, the blow and the death voice."], 10)
        c_sig = _wrap([
            f'THE SIGIL\'S SHIMMER -- "a very quiet sustained shimmer (re-struck, 2-3 kHz band, peak <= 0.15) while '
            f'it is drawn" (v75 §6.2). {sn}, of {len(SIGIL_CANDIDATES)} (`oracle_voice_lab.py`). One strike a call: '
            f'`tickSight` re-strikes it on the window\'s first frame and every {NS}th window frame after, so the '
            f'strikes are the held note (CLAUDE.md 4.5) and stop with the window.',
            f"{', '.join(f'{f:g} Hz' for f, _k in S_['sp']['parts'])} (whole multiples of 120 Hz: a clip places every "
            f"strike on a 1/120 s frame, so they all start in phase and sum as one note); each strike {S_['sp']['D']:g} "
            f"s long, falling {20 * math.log10(S_['g'] / 0.0001):.0f} dB before it stops (`_tone` ramps to 0.0001 "
            f"absolute), so {S_['sp']['D'] * FRAME / NS:.1f} overlap: a {S_['depth']:.1f} dB shimmer at "
            f"{S_['rate']:.0f} Hz. Steady loudest 50 ms {db(S_['top'] / l_hi):+.1f} dB "
            f"re the bowstring and {db(S_['top'] / w_lo):+.1f} dB re the wall tick (the quietest voice in the fight), "
            f"{S_['omed']:+.1f} dB over the score in its third-octave ({S_['omin']:+.1f} at the least); peak "
            f"{S_['peak']:.4f}; {100 * S_['band']:.0f}% of its power in 2-3 kHz; under the score {S_['gone']:.2f} s "
            f"after the close."], 10)
        c_hex = _wrap([
            f'A WINDOW ARROW HEXES TWICE -- "a hit: the bow\'s own arrow voice plus a hex snap; pitch by count" '
            f'(v75 §6.2). {kn}, of {len(SNAP_CANDIDATES)} (`oracle_voice_lab.py`): the school\'s own snap (the '
            f'`hex-snap` below), every frequency x 2^(step / 12), step {", ".join(str(s_) for s_ in K_["sp"]["steps"])} '
            f'semitones at counts 1-{CAP}, n = the count the foe\'s tag shows after the second hex; at count 1 it IS '
            f'the school\'s snap. `resolveHit` plays it on the arrow\'s own frame, over the arrow\'s own hit voice.',
            f"Measured pitch {' / '.join(f'{p_:.0f}' for p_ in K_['pitch'])} Hz; on the blow it stands "
            f"{K_['overhit']:+.1f} dB or more over it in its own third-octave; register at most "
            f"{max(K_['regs'].values()):.2f} against the blow, the wall tick, the bowstring, rune-crack and the death "
            f"voice."], 10)
        c_close = _wrap([
            f'THE EYE SHUTS -- "close: the chime reversed" (v75 §6.2). {zn}, of {len(CLOSE_CANDIDATES)} '
            f'(`oracle_voice_lab.py`): every mode of the cast\'s chime, its fall run backwards as a climb re-struck '
            f'at whole cycles ~11 ms apart, ending where the chime began, cut there. ENV-CORR {Z_["ecorr"]:.2f} with the '
            f'chime\'s own samples reversed; loudest 50 ms {abs(Z_["dtop"]):.1f} dB off the chime\'s; audible '
            f'{Z_["aud"]:.0f} ms. `tickSight` plays it once, on the frame the window runs out by its clock with both '
            f'fighters alive.'], 10)
        arms = (f'{_arm_head(ME, "the rune-eye opens")}\n{c_cast}\n'
                f'{cast_body(C_["sp"], C_["g"], C_["ki"], C_["dc"])}\n'
                f'{_arm_head(ME + "-sigil", "the sigil shimmers")}\n{c_sig}\n{sigil_body(S_["sp"], S_["g"])}\n'
                f'{_arm_head(ME + "-hex", "an arrow hexes twice")}\n{c_hex}\n{snap_body(K_["sp"])}\n'
                f'{_arm_head(ME + "-close", "the eye shuts")}\n{c_close}\n{close_body(Z_["cp"], C_, Z_["gc"])}\n')
        _refuse(arms, "Sfx row")
        if SFX_ANCHOR in arms:
            raise SystemExit("the Sfx row carries its own anchor")
        sfx_rows = [as_replace(SFX_ANCHOR, "before", arms)]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        kbt = snap_body(K_["sp"])
        rp = [float(np.abs(R([["body", T0, kbt, {"n": CAP}]])[0] - R([["body", T0, kbt, {"n": CAP}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the top snap rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        cbt = cast_body(C_["sp"], C_["g"], C_["ki"], C_["dc"])
        sbt = sigil_body(S_["sp"], S_["g"])
        zbt = close_body(Z_["cp"], C_, Z_["gc"])
        for sd in (None, NOISE_SEEDS[5]):
            tag = "" if sd is None else "'"
            xa, _ = R([["arm", T0, "ult", {"w": ME}]], seed=sd, rows=sfx_rows)
            chk.append(("cast" + tag, float(np.abs(xa - R([["body", T0, cbt, {}]], seed=sd)[0]).max())))
            xs_, _ = R([["arm", T0, "ult", {"w": ME + "-sigil"}]], seed=sd, rows=sfx_rows)
            chk.append(("sigil" + tag, float(np.abs(xs_ - R([["body", T0, sbt, {}]], seed=sd)[0]).max())))
            for n in (-1, 0, 1, 2, 3, 4, 5, 9, None):
                p1 = {"w": ME + "-hex"} if n is None else {"w": ME + "-hex", "n": n}
                x1, _ = R([["arm", T0, "ult", p1]], seed=sd, rows=sfx_rows)
                nn = 1 if n is None else min(CAP, max(1, n))
                x2, _ = R([["body", T0, kbt, {"n": nn}]], seed=sd)
                chk.append((f"hex@{n}{tag}", float(np.abs(x1 - x2).max())))
            xz, _ = R([["arm", T0, "ult", {"w": ME + "-close"}]], seed=sd, rows=sfx_rows)
            chk.append(("close" + tag, float(np.abs(xz - R([["body", T0, zbt, {}]], seed=sd)[0]).max())))
            if sd is None:
                xa0 = xa
        x1s, _ = R([["arm", T0, "ult", {"w": ME + "-hex", "n": 1}]], rows=sfx_rows)
        is_school = float(np.abs(x1s - R([["play", T0, "hex-snap", {}]])[0]).max())
        print("  the arms vs the picked candidates, max |diff| (render.py's draw and a second): " +
              ", ".join(f"{k} {v:.1e}" for k, v in chk))
        print(f"  ult/oracle-hex at count 1 vs the school's hex-snap: max |diff| {is_school:.1e}")
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 10, 16.23, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 3}), ("clank", {"mass": 1.6}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("aegis", {"n": 10, "back": 5}), ("aegis", {"broke": True}),
                   ("vine", {"plant": True}), ("vine", {"coil": True}), ("vine", {"miss": True}), ("vine", {"n": 2}),
                   ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}), ("fork", {}),
                   ("scour-hold", {"n": 3}), ("scour-tick", {"n": 2}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = page.evaluate(r"""() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();
            const a = [...s.matchAll(/w === "([a-z-]+)"/g)].map(m => m[1]);
            return [...new Set([...AC.WEAPONS.map(w => w.id), ...a])]; }""")
        ult_ids = [w_ for w_ in ult_ids if w_ != ME and not w_.startswith(ME + "-")]
        others += [("ult", {"w": w_, "n": 2, "dmg": 20}) for w_ in ult_ids]
        same_ = []
        for kind_, p_ in others:
            x1, _ = R([["play", T0, kind_, p_]]); x2, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows)
            same_.append((kind_ + "/" + str(p_.get("w", p_.get("dmg", p_.get("n", "")))) + ("!" if p_.get("crit") else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, spark x3, wall, death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3, "
              f"fork, scour x4, and {len(ult_ids)} ult ids -- every relic's cast and every sub-voice the ult arm "
              f"names): worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa0 - rcx).max())
        print(f"  ult/oracle vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or is_school > TOL:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, repro=max(rp), is_school=is_school)

        # ---- WITH OTHER RELICS' ROWS ------------------------------------------
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        peers = []
        for pf in a.peer_rows:
            prow = json.loads(pathlib.Path(pf).read_text(encoding="utf-8"))
            prow = prow["rows"] if isinstance(prow, dict) else prow
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            if not ps:
                print(f"  peer {pf}: no row anchored in play() -- skipped")
                continue
            pids = sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _, c in ps))))
            pk_ = sorted(set(re.findall(r'kind === "([a-z-]+)"', "".join(c for _, c in ps))))
            A_ = sfx_rows + ps; B_ = ps + sfx_rows
            evs = [("ult", {"w": ME}), ("ult", {"w": ME + "-sigil"}), ("ult", {"w": ME + "-close"})] + \
                  [("ult", {"w": ME + "-hex", "n": n}) for n in COUNTS]
            evs += [("ult", {"w": w_, "n": 3, "shield": 45}) for w_ in pids] + [(k_, {}) for k_ in pk_]
            dmax, dmine = 0.0, 0.0
            pr = {}
            for kind_, p_ in evs:
                xa_, _ = R([["arm", T0, kind_, p_]], rows=A_); xb_, _ = R([["arm", T0, kind_, p_]], rows=B_)
                dmax = max(dmax, float(np.abs(xa_ - xb_).max()))
                if str(p_.get("w", "")).startswith(ME):
                    xs_, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows)
                    dmine = max(dmine, float(np.abs(xa_ - xs_).max()))
                else:
                    bp = bands(xa_[int(T0 * SR):])
                    pr[p_.get("w", kind_)] = max(cos(fb4[k4], bp) for k4 in fb4)
            worst_p = max(((v, k) for k, v in pr.items()), default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders render "
                  f"every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); register of "
                  f"the four picks against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) -- printed, not gated")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=pr))
        rec["peers"] = peers

        # ---- THE tickSight AND resolveHit ROWS ------------------------------
        SIG_CODE = sigil_code(NS)
        srows = [as_replace(SIGIL_ANCHOR, "after", SIG_CODE), as_replace(CLOSE_ANCHOR, "before", CLOSE_CODE)]
        hrows = [as_replace(HEX_ANCHOR, "after", HEX_CODE)]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickSight AND resolveHit ROWS, applied to their prototypes' own source, run beside the originals "
              "on real fights (the mirror match is refused by Match):")
        WR = page.evaluate(WIRE_JS, [seeds, srows, hrows, NS])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        tt = WR["tot"]
        print(f"  {WR['fights']} fights (Oracle both sides x every foe x seeds {seeds}): {WR['same']}/{WR['fights']} "
              f"identical (over, clock, both hp, shields, positions, velocities, charges, both hex counts, the arrows "
              f"in the air, winner, the whole sightTally); every other voice call identical in order, kind and opts in "
              f"{WR['otherSame']}/{WR['fights']}")
        print(f"  windows {WR['ends']}: {tt['cast']} casts -> {tt['castV']} cast voices; {tt['sigil']} strike frames -> "
              f"{tt['sigilV']} sigil strikes; {tt['hex']} second hexes -> {tt['hexV']} snaps; {tt['close']} clock closes "
              f"with both alive -> {tt['closeV']} close voices; problems {WR['nbad']}")
        nh = WR["nh"]
        print("  the count a snap carries (the foe's hex after the second hex): " +
              ", ".join(f"{n}: {nh[n]}" for n in COUNTS) + f" ({100 * nh[CAP] / max(1, sum(nh)):.0f}% at the cap)")
        gp_ = np.array([g_[0] for g_ in WR["gaps"]]); tl_ = np.array([g_[1] for g_ in WR["gaps"]])
        if len(gp_):
            print(f"  in the {len(gp_)} clock windows: the longest real gap between strikes (hit stops hold them) median "
                  f"{np.median(gp_):.3f} s, p90 {np.percentile(gp_, 90):.3f}, max {gp_.max():.3f} (the train's "
                  f"{NS / FRAME:.3f}); the close {np.median(tl_):.3f} s after the last strike (median; max {tl_.max():.3f})")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or tt["castV"] != tt["cast"] or tt["sigilV"] != tt["sigil"] or tt["hexV"] != tt["hex"] \
                or tt["closeV"] != tt["close"] or 0 in (tt["cast"], tt["sigil"], tt["hex"], tt["close"]):
            FAILED.append("sim rows")
        WB = page.evaluate(WIRE_JS, [seeds, srows, [as_replace(HEX_ANCHOR, "after", HEX_CODE_BAD)], NS])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a snap): {WB['same']}/{WB['fights']} "
              f"identical -- {'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "tot", "nh", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        rec["wire"]["gap_max"] = float(gp_.max()) if len(gp_) else None

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["hexes"], w["foe"], w["seed"], w["side"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], srows, hrows])
            assert not errors, errors[:3]
            c0, c1 = w_["cast"], w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            secs = T0 + (hi_t - lo_t) + 1.0
            at = lambda e: T0 + (e[0] - lo_t)  # noqa: E731

            def mix(keep):
                return R([["arm", at(e), e[1], e[2]] for e in evs if keep(e)], secs=secs, rows=sfx_rows)[0]
            new = {ME, ME + "-sigil", ME + "-hex", ME + "-close"}
            xw = mix(lambda e: True)
            xo = mix(lambda e: e[3] not in new)
            xs_only = mix(lambda e: e[3] == ME + "-sigil")
            wo = {k: mix(lambda e, k=k: e[3] != k) for k in new}
            bd = bed[:len(xw)]
            if len(bd) < len(xw):
                bd = np.concatenate([bd, np.zeros(len(xw) - len(bd))])
            xw = xw + bd; xo = xo + bd
            for k in wo:
                wo[k] = wo[k] + bd
            tc_ = [at(e) for e in evs if e[3] == ME]
            tz_ = [at(e) for e in evs if e[3] == ME + "-close"]
            tk_ = [(at(e), e[2].get("n")) for e in evs if e[3] == ME + "-hex"]
            ts_ = [at(e) for e in evs if e[3] == ME + "-sigil"]

            def ov(xa_, xb_, f, a_, d_):
                return db(band_rms(xa_, f, a_, a_ + d_) / max(band_rms(xb_, f, a_, a_ + d_), 1e-12))
            bc = bands(C_["x"][int(T0 * SR):int((T0 + 0.4) * SR)])
            fc_c = max((v_, fc) for v_, fc in zip(bc, BANDS) if fc >= 200)[1]
            c_over = [ov(xw, wo[ME], fc_c, t_, 0.4) for t_ in tc_]
            k_over = []
            for t_, n in tk_:
                xk = K_["xs"][min(CAP, max(1, n))]
                bk = bands(xk[int(T0 * SR):int((T0 + 0.05) * SR)])
                fk = max((v_, fc) for v_, fc in zip(bk, BANDS) if fc >= 200)[1]
                k_over.append(ov(xw, wo[ME + "-hex"], fk, t_, 0.05))
            bz = bands(Z_["x"][int(T0 * SR):])
            fc_z = max((v_, fc) for v_, fc in zip(bz, BANDS) if fc >= 200)[1]
            z_over = [ov(xw, wo[ME + "-close"], fc_z, t_, 0.4) for t_ in tz_]       # its own span: it climbs
            z_around = [ov(xw, wo[ME + "-close"], fc_z, t_ - 0.1, 0.2) for t_ in tz_]   # round 2's first reading
            # the shimmer: alone against the score (heard), and in the fight (with vs without it)
            fcs = S_["fc"]
            e1, cs1 = env(third(xs_only, fcs), 0.05, 0.005)
            osc = 20 * np.log10(np.maximum(e1, 1e-12) / score50(fcs))
            wa_, wb_ = ts_[0] + 0.3, (tz_[0] if tz_ else at([c1]))
            mm = (cs1 >= wa_) & (cs1 <= wb_)
            heard_frac = float((osc[mm] >= 0).mean())
            e2, _ = env(third(xw, fcs), 0.05, 0.005); e3, _ = env(third(wo[ME + "-sigil"], fcs), 0.05, 0.005)
            fight_frac = float((20 * np.log10(np.maximum(e2[mm], 1e-12) / np.maximum(e3[mm], 1e-12)) >= 3).mean())
            after = np.nonzero((cs1 > wb_) & (osc >= 0))[0]
            gone_real = float(cs1[after[-1]] + 0.025 - wb_) if len(after) else 0.0
            pk_real = float(np.abs(xs_only).max())
            print(f"\nIN A REAL WINDOW -- oracle v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at {c0:.2f}s, "
                  f"closed by its clock at {c1:.2f}s ({c1 - c0:.2f} s: its hit stops), {len(ts_)} strikes, {len(tk_)} snaps; "
                  f"the fight's own sounds and the score, with and without each new voice")
            print(f"  the cast over the fight ({fc_c:.0f} Hz, 0.4 s): " + " ".join(f"{v:+.1f}" for v in c_over) +
                  f" dB;  the close ({fc_z:.0f} Hz, its first 0.4 s): " + " ".join(f"{v:+.1f}" for v in z_over) +
                  " dB (0.1 s either side of its event, round 2's first reading: " +
                  " ".join(f"{v:+.1f}" for v in z_around) + " dB)")
            print("  each snap over the fight (its loudest third-octave, first 50 ms, the arrow's hit voice in both): " +
                  " ".join(f"{v:+.1f}" for v in k_over) + " dB (counts " + " ".join(str(n) for _, n in tk_) + ")")
            print(f"  the shimmer alone over the score in its third-octave ({fcs:.0f} Hz) for {100 * heard_frac:.1f}% of the "
                  f"window (from the first strike + 0.3 s to the close); in the fight it adds >= 3 dB there for "
                  f"{100 * fight_frac:.1f}% of it; under the score {gone_real:.2f} s after the close; peak {pk_real:.4f}")
            if (c_over and min(c_over) < 6) or (k_over and min(k_over) < 6) or (z_over and min(z_over) < 6) \
                    or heard_frac < 0.95 or gone_real > FADE or pk_real > 0.15:
                FAILED.append("a new voice not heard, or not gone, in a real window")
            wav("oracle-pick-real-window.wav", xw)
            wav("oracle-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, cast_over=c_over, close_over=z_over, close_around=z_around, snap_over=k_over,
                               counts=[n for _, n in tk_], sigil_heard=heard_frac, sigil_fight=fight_frac,
                               sigil_gone=gone_real, sigil_peak=pk_real)
        # the picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": ME}]]
        seq += [["arm", T0 + i * NS / FRAME, "ult", {"w": ME + "-sigil"}] for i in range(int(3.0 * FRAME / NS))]
        seq += [["arm", T0 + 0.8 + 0.4 * k_, "hit", {"dmg": BLADE, "crit": False}] for k_ in range(CAP)]
        seq += [["arm", T0 + 0.8 + 0.4 * k_, "ult", {"w": ME + "-hex", "n": n}] for k_, n in enumerate(COUNTS)]
        seq += [["arm", T0 + 3.0 + close_gap(NS) / FRAME - NS / FRAME, "ult", {"w": ME + "-close"}]]
        xq_, _ = R(seq, secs=6.0, rows=sfx_rows)
        wav("oracle-pick-sequence.wav", xq_)

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_voices = [(k_, p_) for k_, p_ in others if k_ != "ult"][:36] + \
                     [("ult", {"w": w_}) for w_ in ult_ids if w_ in {w for w, _a, _s in info0["W"]}][:12]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [R([["play", T0, k_, p_]])[0] for k_, p_ in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)], NS])
            assert not errors, errors[:3]
            e2e_ref["new"] = {"cast": R([["body", T0, cbt, {}]])[0], "sigil": R([["body", T0, sbt, {}]])[0],
                              "close": R([["body", T0, zbt, {}]])[0]}
            for n in COUNTS:
                e2e_ref["new"][f"hex n{n}"] = R([["body", T0, kbt, {"n": n}]])[0]

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Oracle's cast, sigil, snap and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="before", code=arms),
            dict(label="tickSight: the sigil's shimmer, re-struck every %d window frames while the window runs" % NS,
                 anchor=SIGIL_ANCHOR, mode="after", code=SIG_CODE),
            dict(label="resolveHit: the snap, pitched by the foe's hex count, once per second hex",
                 anchor=HEX_ANCHOR, mode="after", code=HEX_CODE),
            dict(label="tickSight: the close voice, on a clock close with both fighters alive",
                 anchor=CLOSE_ANCHOR, mode="before", code=CLOSE_CODE)]
    for r_ in rows:
        _refuse(r_["code"], "row " + r_["label"])
        if r_["anchor"] in r_["code"]:
            raise SystemExit(f"row '{r_['label']}' carries its own anchor")
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], as_replace(r_["anchor"], r_["mode"], r_["code"])[1], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit("end to end: an anchor no longer occurs exactly once")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="oracle_e2e_"))
        try:
            tp = tmpd / "sc-oracle-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the four rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            with game(game_path=tp) as (page, errors):
                def R2(evs, secs=3.0, seed=None):
                    r = page.evaluate(RENDER_JS, [evs, secs, seed, None])
                    assert not errors, errors[:3]
                    return pcm(r)
                vo = max(float(np.abs(R2([["play", T0, k_, p_]]) - x0).max())
                         for (k_, p_), x0 in zip(e2e_voices, e2e_ref["voices"]))
                NEWP = [("cast", {"w": ME}), ("sigil", {"w": ME + "-sigil"}), ("close", {"w": ME + "-close"})]
                NEWP += [(f"hex n{n}", {"w": ME + "-hex", "n": n}) for n in COUNTS]
                nd = [(lab_, float(np.abs(R2([["play", T0, "ult", p_]]) - e2e_ref["new"][lab_]).max()))
                      for lab_, p_ in NEWP]
                rcp = R2([["play", T0, "ult", {"w": "spellbreaker"}]])
                not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
                F1 = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)], NS])
                assert not errors, errors[:3]
                page_err = len(errors)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
        F0 = {f_["key"]: f_ for f_ in e2e_ref["fights"]}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        s_ok = sum(f_["sigilV"] == f_["strikes"] for f_ in F1)
        h_ok = sum(f_["hexV"] == f_["hexes"] and f_["badN"] == 0 for f_ in F1)
        z_ok = sum(f_["closeV"] == f_["closes"] for f_ in F1)
        orig_new = sum(f_["sigilV"] + f_["hexV"] + f_["closeV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "castV", "strikes", "sigilV", "hexes", "hexV",
                                                    "closes", "closeV")}
        print("  the four voices through the patched page's own SFX.play vs the lab's candidate text, max |diff|: " +
              ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/oracle vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, sigil strikes = strike frames {s_ok}, "
              f"snaps = second hexes (n the foe's count) {h_ok}, closes = clock closes {z_ok} (of {len(F1)}); totals "
              f"{tot}; the original page played {orig_new} of the new voices; page errors {page_err}")
        if max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1) or osame != len(F1) \
                or min(c_ok, s_ok, h_ok, z_ok) != len(F1) or orig_new or page_err:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same,
                          other_same=osame, totals=tot, chars=len(patched) - len(html))

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB", "sp", "cx", "cp")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), sigil=strip(rows_s), sigil_controls=strip(ctls),
               snap=strip(rows_k), snap_controls=strip(ctlk), close=strip(rows_z), close_controls=strip(ctlz),
               wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_ki": C_["ki"], "cast_dc": C_["dc"],
                     "sigil": S_["name"], "sigil_g": S_["g"], "sigil_N": NS, "snap": K_["name"],
                     "close": Z_["name"], "close_g": Z_["gc"]})
    print(f"\nTHE PICKS  cast {C_['name']}   sigil {S_['name']}   snap {K_['name']}   close {Z_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text to a copy of the page: {E2['same']}/{E2['fights']} fights "
          f"identical to the unpatched page's" if E2 else "")
    wr = rec["wire"]; tt = wr["tot"]
    ac = rec["arm_check"]
    pn = [peer_name(p_["file"]) for p_ in rec["peers"]]
    pw = [n_ + "'s" for n_ in pn]
    pw = (", ".join(pw[:-1]) + " and " + pw[-1]) if len(pw) > 1 else "".join(pw)
    pe = (f"; with {pw} Sfx rows (the batch's scratch builds) applied too, in either order, every arm of both "
          f"renders alike" if pn else "")
    rows[0]["why"] = (
        f"The four voices (v75 §6.2), in the synth only. The arms go BEFORE the shared rune-crack fallback and the "
        f"row never touches the fallback line, so the relics that still fall through keep it ({n_rc} others on this "
        f"link) and another row anchored on that line still applies. Through the patched play() every arm reproduces "
        f"its lab candidate (worst {max(v for _, v in ac['chk']):.0e}; the snap at counts -1, 0, 1-5, 9 and a missing n, "
        f"on two noise draws), the snap at count 1 is the school's hex-snap ({ac['is_school']:.0e}), "
        f"{len(ac['others'])} other voices are unchanged (worst {max(v for _, v in ac['others']):.0e}), and ult/oracle "
        f"is no longer rune-crack. play() returns on its first line with no audio context (every headless run), draws "
        f"no random number and writes nothing the simulation reads"
        + (f"; end to end the four voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + pe + ".")
    rows[1]["why"] = (
        f"One plain SFX.play after tickSight's last tally line -- inside the running window, so never on the closing "
        f"frame -- on window frames 1, 1+{NS}, 1+{2 * NS}...: Math.round(Z.t / dt) reads the window's own clock, "
        f"which stops in a hit stop. {tt['sigilV']}/{tt['sigil']} strike frames voiced, none elsewhere; "
        f"{wr['same']}/{wr['fights']} fights identical and every other SFX call identical in order and opts; the "
        f"same rows plus one sim write come back {wr['control_same']}/{wr['fights']}{e2}.")
    rows[2]["why"] = (
        f"One plain SFX.play right after the second hex is applied (inside its own guard: a shot, the caster in "
        f"its window, the foe alive and not a shade), so n is the count the foe now carries (foe.stacks is a read). "
        f"{tt['hexV']}/{tt['hex']} second hexes voiced, each n equal to the foe's count (1-{CAP}; "
        f"{100 * wr['nh'][CAP] / max(1, sum(wr['nh'])):.0f}% at the cap); the same rows plus one sim write (the foe "
        f"nudged 1e-9 on a snap) come back {wr['control_same']}/{wr['fights']} identical{e2}.")
    rows[3]["why"] = (
        f"One guarded SFX.play BEFORE the close line, which the row leaves untouched: Z.t >= Z.dur with both alive is "
        f"a read of the line's own test, so it plays exactly on a clock close. {tt['closeV']}/{tt['close']} clock "
        f"closes voiced; none on the {wr['ends'].get('death', 0)} deaths or {wr['ends'].get('clock-dead', 0)} clock "
        f"closes with a fighter down; nothing is read back{e2}.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The four rows are the edits; all four were applied "
          "to the page's own code above, and as text to a copy of the page.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
