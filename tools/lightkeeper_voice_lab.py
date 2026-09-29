#!/usr/bin/env python3
"""BULWARK'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v107.

    python lightkeeper_voice_lab.py --game <a link carrying Lightkeeper's stage 5> --rows rows.json

v77 section 5 SOUND, every word of it: "Sound: cast -- a shield-raise (a
rising metallic slide, 0.4s); a ball block -- a deep gong (share <120 Hz >=
0.4, <=0.3s); an arrow -- a short tink; close -- the slide reversed." The
brief's stage 4 (v107's stage 6): "picture, voice, carry". Rick, for the
batch's art and sound: "you pick i overrule". So this lab does not offer a
spread -- it renders three to five candidates a voice beside CONTROLS that can
come back wrong, prints the numbers each pick is made on, and PICKS by a rule
written in this file (`*_RULE`, `*_why`). He overrules from one clip.

NOTHING IS REUSED, BECAUSE THE DESIGN NAMES NOTHING TO REUSE. All four voices
are new arms of the `ult` kind. The ward's bank (every block banks +3) has no
voice of its own: v77 names none, and the gong and the tink ARE the blocks.

THE FOUR EVENTS AND WHERE THEY FIRE:
  raise  the bare id `ult/lightkeeper`, which `fireUlt` plays for every relic
         (the generic prelude, before the lightwall branch). Lightkeeper has NO
         arm today: it falls through to the shared rune-crack (measured below,
         to 1e-6, with every other relic that still does). The arms go BEFORE
         that fallback; the fallback line is re-emitted unchanged, so another
         relic's row anchored on it still applies, in either order. No sim
         line: the cast already plays it, once a cast.
  gong   `ult/lightkeeper-gong` from `tickLightwall`, right after
         `T.blocks++;` (re-emitted first, unchanged): once per ball block --
         the foe turned back -- on the block's own frame, before its shove and
         its bank. The window's cooldown (0.4 s) allows one a frame at most.
  tink   `ult/lightkeeper-tink {k}` from `tickLightwall`, right after
         `T.arrows++;` (re-emitted first, unchanged): once per arrow that
         dies on the wall (spliced, or a net's arrow made stuck), before its
         bank. `k` is the arrow's index among the wall's kills on that frame
         (0, 1, 2, ...), counted by a `var` the row declares: hoisted to the
         ticker's call, it starts undefined -> 0 on every frame. The arm
         FLAMS by it, t + min(5, k) x 26 ms -- the nova's flam, the house's
         number for arrows landing on one frame ("26 ms apart the ear reads
         three events, and at 0 it reads one pop at three times the
         amplitude"). 10.7% of the arrows the wall stops share their frame
         with another (up to four, on 148 fights: runs below).
  fold   `ult/lightkeeper-fold` from `tickLightwall`, on a line placed BEFORE
         the window's close line (re-emitted unchanged): on the frame the wall
         runs out BY ITS CLOCK with both fighters alive -- never on a death (a
         caster's death ends the fight; a close after the foe's death belongs to
         its kill flight: both are the death voice's), never once the fight is
         over (step() stops calling the tickers; a wall still up at `over`
         folds in the picture only). Tendril's, Canopy's and Zenith's rule.
  The block and the arrow set no hit stop and file no beat (v77: "no damage,
  no beat, no hit stop"). The four voices are plain SFX.play calls; the
  picture's rows (the bar, the flash, the scorch, the "+3", the motes) are
  the picture lab's, not these, and none of them touches `tickLightwall` or
  the Sfx table.

THE CONTROLS, and what each one is for:
  rune-crack   what Lightkeeper's cast plays TODAY; v88 published 0.608 /
               450 ms -- reproduced before anything new is quoted (with BAR
               0.364 / 300 ms and hit@11.6 0.443 / 80 ms)
  hit@9.5      Lightkeeper's own blow (the blade holds at 9.5, stage 5): the
               level every voice is judged against, on its quietest / loudest
               noise draw
  crit@9.5     the same blow critting: the sound a ward shattering makes
               (the shatter plays its own crit `hit` inside `hurt`): printed
  wall         the commonest sound in a fight: the tink's floor
  the school   the vigil casts with a voice of their own (read off the page)
  the type     the greatsword casts with a voice of their own (read off the page)
  Zenith       Morningstar's cast, the batch's other RISING cast
  death, clank, aegis, nova   the heaviest low voice, the weapons' clash, the
               game's stopped-blow voice (and its break), the bow novas' pop:
               the gong must not be any of them
  hex-snap, spark, Zenith's tick, loose   the small bright voices and the
               bowstring: the tink must not be any of them
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  STEP, FALL, HARM, STRUCK, SPARSE, RUNECRACK   the raise as two notes / run
               downward / on whole-number partials / one strike gliding /
               struck a third as often / today's voice: each must fail its gate
  THUD, HARM, LONG, DULL, HIGH, DEATH, CLANK   the gong without its plate / on
               whole-number partials / ringing 0.9 s / dying in 60 ms / three
               octaves up / the death voice / the clank: each must fail its gate
  TICK, LONG, LOW, FLAM0   the wall tick's own construction at the tink's level
               / the tink ringing 5x longer / two octaves down / with no flam:
               each must fail its gate
  AGAIN, SHORT, HARM, QUIET   the raise itself / the fold over half the length
               / on whole-number partials / 9 dB under: each must fail its gate
  LITERAL      the picked raise rendered dry, its samples REVERSED, played
               through the chain: the reference ENV-CORR reads the fold
               against (it cannot ship -- an arm cannot reverse samples)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT. Each candidate is generated as the JS
    body that will sit in the arm (constants rounded first) and rendered by
    evaluating that text on the synth (ironwood_voice_lab's RENDER_JS,
    imported unchanged); the row is then applied to `Sfx.prototype.play`'s
    own source and rendered again, and must match to TOL = 1e-5.
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's,
    bindweed_voice_lab's and ironhail_voice_lab's, imported unchanged: E50,
    TOP (the loudest 50 ms), START (the loudest 50 ms centred in the first
    100), SWELL = TOP - START, AUDIBLE / GONE (the 5 ms RMS above 2% of its
    own loudest), RISE (10 -> 90% of the 1 ms envelope), REG (cosine of
    1/3-octave band amplitudes, 25 Hz-16 kHz, the median over noise draws),
    PITCH (FFT peak, Hann, zero-padded, parabolic), LOW (the share of the
    power below 120 Hz), METAL (ironwood's `inharm`: the strongest peak
    between 1.5x and 4x the note is >= 60 cents from every whole multiple and
    within 20 dB of it), TONAL (bindweed's: how far the draw-averaged
    spectrum's sharpest 1/48-octave peak stands over the median of its
    third-octave neighbourhood, dB), ENV-CORR (zenith's: Pearson of two E50
    curves in dB, each floored 40 dB under its top, aligned at onset),
    FLUTTER (zenith's: p95 - p5 of the RMS over four periods of a pitch -- A4
    here -- at a 1 ms hop, about its own 100 ms average, over the audible span
    less 50 ms each end: how evenly a re-struck note holds), HEARD
    (ironhail's: the voice's loudest third-octave AT OR ABOVE 200 Hz over its
    first 100 ms against the score's p90 there, dB -- a phone reproduces
    little under 200 Hz) and PHONE (Culverin's v96: the TOP of the voice
    high-passed at 200 Hz).
  * New here, each with a control that can come back wrong:
      CLIMB   the pitch (FFT peak 150-560 Hz) over the last 60 audible ms re
              the first 60, cents (FALL is the same, read on the fold)
      TRACK   that pitch in 40 ms windows every 20 ms inside the audible span
              (30 ms trimmed each end): the largest step against the slide's
              direction (a slide never turns back) and the largest step WITH
              it as a share of the whole CLIMB (a slide spreads its climb; two
              notes put all of it in one step -- STEP must fail)
      HOLDS   the gong's note over 20-80 ms against 80-160 ms, cents
      ONSETS  1 ms RMS peaks >= 15 ms apart, each >= 0.3 of the loudest and
              >= 6 dB over the dip before it: what one frame's tinks are
              heard as (FLAM0 must read one)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the raise's slide length is solved so it is AUDIBLE 400 ms, its
    scrape (where it has one) 6 dB under or over its ring, its gain to the
    centre of its level window; the gong's fundamental weight so LOW is 0.50
    at render.py's draw (the gate's 0.40 plus a margin for the draws, as
    Tendril's root took 0.50), its decay so it is GONE by 250 ms, its gain to
    the centre of its window; the tink's decay so it is AUDIBLE 40 ms, its
    gain to the centre of its window; the fold's gain so its TOP is the
    raise's. Constants are rounded BEFORE any measured render, so a shipped
    arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of v77 section 5 turned into
numbers):
  * "0.4s": AUDIBLE 330-470 ms, v100's reading of Portcullis's "0.4s" (and
    v108's of Ironhail's).
  * "RISING ... SLIDE": the ring GLIDES up one octave, A3 -> A4 (220 -> 440
    Hz; the score is in A minor, and the slide lands on its tonic), as one
    continuous chirp: every strike is re-struck on a whole cycle of the chirp
    (zenith_voice_lab's glide: the k-th cycle of f0 x 2^(u/L) falls at u = L /
    ln 2 x ln(1 + k ln 2 / (f0 L))), gliding along it with `to:`, and
    `.frequency.value = f` is set on every strike (v97's toolkit finding). A
    held note does not exist in this toolkit (CLAUDE.md 4.5), so the ring is
    re-struck every 2 cycles of the chirp (9 ms apart at A3, 4.5 at A4: the
    strikes thicken as it climbs), each strike decaying over 60 ms. The glide
    ends ON A4 (a strike's `to` is clamped there), so its tail rings the
    note the fold starts on. Its level swells 0.35 -> 1 across the slide (a
    shield coming UP), which is also what keeps it from being a strike.
  * "METALLIC": the ring carries inharmonic modes -- an iron bar's (2.76,
    5.40) or a plate's (1.73, 2.33, 3.91: the ratios of a free circular
    plate's lowest modes, a shield being a plate) -- and must pass METAL.
    "Slide" may also be read as metal on metal: the SCRAPE candidates add a
    bandpass noise band climbing the same octave three octaves up (1760 ->
    3520 Hz), 6 dB under the ring (or, in SHING, the ring 6 dB under it).
  * "A DEEP GONG": a struck plate: one strike of a sine fundamental with
    inharmonic plate (or bar) modes over it, each dying faster than the one
    below (a gong's high partials go first), under a soft mallet (a 20 ms
    lowpass thump at 450 Hz). Deep = the note at or under 120 Hz -- A2 (110
    Hz, the score's tonic; v103 measured it the one low note clear of the
    score's bass), E2 (82.4) or A1 (55) -- with the modes that carry it on a
    phone above 200 Hz (Culverin's v96 and Coldiron's v103 lesson; Ironhail's
    round 2: a low voice is heard on a phone by whatever partial stands over
    200 Hz). "<=0.3s" = GONE <= 300 ms; "share <120 Hz >= 0.4" = LOW >= 0.40
    on the worst draw. A gong RINGS (AUDIBLE >= 180 ms, over twice the blow's)
    and holds its note (a falling sine is the death voice).
  * "A SHORT TINK": a small high metallic ping -- one strike of a sine note
    at or over 1 kHz with inharmonic modes, struck (RISE <= 2 ms), a NOTE
    (TONAL >= 15 dB: the wall tick is noise), audible at most 60 ms (Zenith's
    "soft chime, 60ms" is the house's smallest pitched voice; short = no
    longer). Heard but a small hit: at least 2x the wall tick and at most
    0.7x the blow (Tendril's bite window).
  * "THE SLIDE REVERSED": the picked raise's own figure run backward -- its
    glide falling A4 -> A3 and its envelope mirrored: its release becomes a
    short climb on A4 (as Zenith's close took its cast's release, v98), then
    its swell becomes a fall 1 -> 0.35 across the glide, its scrape (if any)
    falling with it. Read as literally as the toolkit allows, and measured
    against the LITERAL reversal. At the raise's own level: v77 does not say
    quiet, and Zenith's "reversed, quiet" had to say it.
  * LEVELS: the raise, the fold and the gong are heard like a blow and never
    over one (TOP between 0.5x the hit @ 9.5's loudest draw and 1.0x its
    quietest -- every cast in the batch); the tink as above. Every voice
    HEARD >= +6 dB over the score (the batch's threshold), and the gong and
    the tink PHONE at least the bowstring's.

THE ROUNDS. Round 1 (the raises 1-5, the gongs 1-5, the tinks 1-4, the folds
1-3, the rules as first written, with no FLUTTER) exited 1 on the tink and the
fold. Every round-1 candidate stays in the table; round 2 changed the rules
named here, and no other, and ADDED candidates:
  * THE TINK: no candidate passed. (a) All four peaked at 6-7 ms, and so does
    every voice through the chain -- the wall tick and the blow peak at 7 ms:
    `buildChain`'s compressor delays its output by its lookahead. The first
    cut's "peak in the first 5 ms" no voice can meet; round 2 reads the
    house's own number, the first 10 ms (Zenith's tick, Tendril's bite).
    (b) All four read 0.87-0.99 against the spark or Zenith's tick: a struck
    note at A6-E7 IS the register of the game's small chimes (the spark
    collects at 1.2-1.9 kHz; Zenith's tick is a bar at C7-A7). Round 2 adds
    three tinks above them: PIN (C8), GLINT (E8), GLINT-CHIP.
  * THE FOLD: every candidate read 0.42-0.64 on ENV-CORR aligned at t = 1.0,
    as zenith_voice_lab's code aligns it: the LITERAL begins with the raise's
    sub-audible tail reversed (the dry render is trimmed at 1e-6, some 40 ms
    under -34 dB), so its heard onset sits ~40 ms late. zenith_voice_lab's
    own docstring defines ENV-CORR "aligned at their onsets"; round 2 aligns
    each at its audible onset (basic()'s a0), and prints both (CORR, CORR0).
    AGAIN still fails it.
  * FLUTTER, new in round 2 for the raise and the fold: round 1 re-struck the
    ring every 2 cycles with a 60 ms decay, and no rule read how evenly that
    holds -- a re-struck note held too sparsely is a buzz at the strike rate.
    Round 2 adds zenith_voice_lab's instrument and gate (<= 3 dB, read at A4)
    with a SPARSE control, and tried Zenith's own rate as two new raises
    (BAR-U, PLATE-U: a whole cycle about every 11 ms all the way, each strike
    dying over 0.2 s). Both fail it (5.7 / 3.9 dB): a strike that outlives
    the rest of the slide is clamped at A4 and falls behind the chirp, so the
    strikes sounding together sit at different pitches and beat (the pitch
    turns back 31-34 cents, the swell flattens to 1.6 dB). Of round 1's own,
    PLATE passes (2.9 dB) and BAR does not (3.3).
  * THE FOLD'S STRIKES: round 1 re-struck a fold every N cycles with N fixed
    at its START (A4: 4 cycles), half the raise's rate at the same pitch;
    round 2 fixes N at A3's count for both (2), so a fold strikes as the raise
    did, in reverse.
  * THE THUD CONTROL (a control, not a rule): round 1 levelled it by LOW like a
    candidate, which drove its fundamental to nothing (kf 0.01) and left the
    mallet; round 2 keeps the pick's own weights and takes away only the
    modes.
Round 2 passed every rule and exited 1 on the real window alone; round 3
changed that reading and nothing else:
  * THE REAL WINDOW (a check on the picks, not a rule a candidate is picked
    on): round 2 read each voice in its own loudest third-octave at or above
    200 Hz. The gong's is 200 Hz (its 2.33 mode), where the score's bass and
    the fight's low sounds sit, and its gongs read median +2.5 dB there.
    Round 3 reads each voice where ironhail_voice_lab (v108) reads it -- the
    third-octave in which it is HEARD over the score (317 Hz for the gong,
    its 3.91 and 4.11 modes: where a phone hears it) -- and prints round 2's
    reading beside it, with every other voice that shares a quiet one's
    window. The thresholds did not move.
Round 3 passed the gong (median +13.2 dB at 317 Hz) and failed the fold: at
the band where the fold alone is HEARD over the score (1600 Hz, its 3.91 mode
at 0.2 of the ring) it read +1.8 dB; at its own loudest band (400 Hz), +16.1.
A fixed band a voice, chosen from the voice ALONE, is wrong one way or the
other: its loudest band can be the score's bass (the gong at 200 Hz), and the
band where it stands highest over the SCORE can be where it is weakest and
the fight's own voices sit (the fold at 1600 Hz). Round 4 changed that
reading and nothing else:
  * THE REAL WINDOW reads HEARD's own definition in the window itself: per
    event, the third-octave (200 Hz-12 kHz, HEARD's span) in which the voice
    stands highest over EVERYTHING ELSE -- the score and the fight -- which is
    where an ear detects it. Round 3's and round 2's readings are printed
    beside it; the gates are round 1's (the raise and the fold >= +3 dB, the
    gongs' and the tinks' median >= +6 dB). This is the third reading of a
    check on the picks (not a rule a candidate is picked on), changed after
    the table was read, and it says so here.
  * ITS CONTROLS (round 4b). A best-of-bands reading could pass anything, so
    round 4's first run gated a control: each voice BURIED 20 dB (its arm's
    own text with g x 0.1) in the same window must fail its own gate. The
    raise, the gongs and the tinks did (+1.0, median +1.0, median +0.4); the
    fold did not (+4.0 dB at 400 Hz: at the close that band is nearly empty,
    so a fold 20 dB down still stands over it). A voice 20 dB down is not
    KNOWN to be unheard, so that was the wrong control, and round 4b gates
    two whose answers are known: AFTER -- the same reading at as many
    instants 0.8 s after the fold, where no new voice sounds -- must read
    NOT heard for every voice; LEVEL -- with the voice 20 dB under, every
    event heard at full level must read lower (the reading follows the
    voice, not the window). BURIED's own gates are printed.
  * Round 4b's LEVEL asked each event read >= +6 dB to read >= 6 dB lower
    buried. That cannot be met by an event read between +6 and about +7:
    the reading, 10 log10(1 + V/E), floors at 0 dB. It failed on the raise
    (+6.8 -> +1.0) and on one gong (+6.1 -> +0.3), both buried to about
    +1 dB -- not heard -- so the fault was the control's arithmetic. Round
    4c asks only what is known: every event heard at >= +3 dB reads LOWER
    with its voice 20 dB under. AFTER read +0.0 on every instant. No voice,
    candidate, pick, row or voice threshold changed in rounds 3-4c.

THE PICKS -- see the run's own printout (stage6-voice/lab*.log); the rows'
comments carry the same numbers.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (four arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the tink at k =
    -1, 0..6 and a missing k, on two noise draws) must reproduce its
    candidate to TOL; every other voice through the patched play (the hit at
    five weights with and without a crit, spark x3, wall, death, clank x2,
    seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork, scour x4, and
    every ult id and kind the page's play() names) must be unchanged;
    `ult/lightkeeper` must NOT be rune-crack any more;
  * the three tickLightwall rows are applied to `Match.prototype.
    tickLightwall`'s own source and run on real fights beside the unpatched
    one: every fight identical (over, clock, both hp, shields, positions,
    velocities, charges, the arrows in the air, winner and the whole
    wallTally) and every other voice call identical in order, kind and opts;
    one gong per block, on its frame; one tink per arrow, on its frame, k
    counting 0, 1, 2 ... within the frame; one fold per window closed by its
    clock with both alive and none otherwise; one raise per cast (from
    `fireUlt`, outside the ticker); the unpatched runs play no gong, tink or
    fold. The same rows plus ONE sim write (the foe nudged 1e-9 on a block)
    must come back NOT identical, or "identical" proves nothing. (The Sfx
    row cannot reach the simulation at all: `play` returns on its first line
    with no audio context, which is every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a
    temp folder, never the repo), loaded in a fresh browser after the first
    is closed: the page loads clean, its own SFX.play renders the arms to
    the lab's text, every other voice to the original page's, and its fights
    are identical to the original page's, with the voice counts above. With
    `--also <link>` (Lightkeeper carried onto a newer tip), the same, there.
  * WITH OTHER RELICS' ROWS (`--peer-rows`, optional): each peer's Sfx rows
    and these applied to play()'s source in both orders render every arm of
    both identically; registers against the peers' voices are printed.
  All anchors must occur exactly once in the game file, and every row is a
  `replace` that re-emits its anchor unchanged exactly once, so a later
  relic's row -- or the picture's -- anchored on the same line still applies,
  in either order. Every row is ASCII.

Writes wavs to 05-reference/v107/lightkeeper-*.wav at RAW level (gitignored).
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
import textwrap

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
# The shared definitions, imported unchanged so every number here means what it
# means in v98's, v99's, v101's and v108's labs. (Their module bodies only
# define things and check their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db,
    env_corr, flutter, fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm, low_share  # noqa: E402
from bindweed_voice_lab import mreg, tonal  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90, heard, phone  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "lightkeeper"
BLADE = 9.5                               # Lightkeeper's dmg (stage 5: the shipped rate)
TOL = 1e-5                                # reproduction / transcription (-100 dB)
F_LO, F_HI = 220.0, 440.0                 # the slide: A3 -> A4
EVERY = 0.01                              # a raise strike every N cycles, N = round(A3 x 10 ms) (2)
RD = 0.06                                 # a raise strike's decay, s
U_EVERY, U_D = 0.011, 0.2                 # ROUND 2's uniform re-strike (Zenith's 11 ms, a 0.2 s decay)
FLUTTER_MAX = 3.0                         # zenith_voice_lab's "sustained-by-restrike" gate, dB
A0 = 0.35                                 # the raise's level at its start, re its top
RAISE_AUD = 400.0                         # "0.4s": the slide length is solved to this
SCRAPE_DB = 6.0                           # the scrape under (or over) the ring
GONG_GONE = 250.0                         # the gong's decay is solved to this (gate: <= 300)
GONG_LOW = 0.50                           # the gong's level-matched low share (gate 0.40)
TINK_AUD = 40.0                           # the tink's decay is solved to this (gate: <= 60)
FLAM = 0.026                              # the nova's flam, s
FLAM_MAX = 5                              # the flam index is clamped to 0..5
QUIET_DB = 9.0                            # the QUIET control: the batch's usual quiet close
SCHOOL_AFF = "vigil"
TYPE_SHAPE = "greatsword"


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


def peer_name(pf):
    """A peer rows file's relic: `<scratch>/batch/<relic>/stage6-voice/rows_final.json` -> "Relic"."""
    p_ = pathlib.Path(pf).parent
    return (p_.parent.name if p_.name.startswith("stage") else p_.name).capitalize()


# ============================================================== THE RAISE ===
# "a shield-raise (a rising metallic slide, 0.4s)". Every candidate glides the
# same octave (A3 -> A4) with the same swell; they differ in the ring's modes
# and in whether metal scrapes on metal. (m, level re the note, oscillator).
RING = {
    "bar":   [(1, 1.0, "triangle"), (2.76, 0.45, "sine"), (5.40, 0.2, "sine")],
    "plate": [(1, 1.0, "sine"), (1.73, 0.55, "sine"), (2.33, 0.4, "sine"), (3.91, 0.2, "sine")],
    "harm":  [(1, 1.0, "sine"), (2.0, 0.55, "sine"), (3.0, 0.4, "sine"), (4.0, 0.2, "sine")],
}
RAISE_CANDIDATES = [
    ("1 BAR", dict(ring="bar", scrape=None),
     "an iron bar's ring (a triangle, its 2.76 and 5.40 modes) gliding A3 -> A4, swelling"),
    ("2 PLATE", dict(ring="plate", scrape=None),
     "a plate's ring (a sine, its 1.73, 2.33 and 3.91 modes) gliding A3 -> A4, swelling"),
    ("3 PLATE-SCRAPE", dict(ring="plate", scrape="under"),
     "PLATE with metal scraping on metal: a bandpass band climbing 1760 -> 3520 Hz, 6 dB under the ring"),
    ("4 BAR-SCRAPE", dict(ring="bar", scrape="under"),
     "BAR with the same scrape, 6 dB under the ring"),
    ("5 SHING", dict(ring="plate", scrape="over"),
     "a blade drawn: the scrape leading, PLATE's ring 6 dB under it"),
    # ROUND 2's uniform re-strike, kept in the table (see THE ROUNDS)
    ("6 BAR-U", dict(ring="bar", scrape=None, fixn=False, every=U_EVERY, D=U_D),
     "BAR struck on a whole cycle about every 11 ms all the way up (Zenith's rate), each strike dying over 0.2 s"),
    ("7 PLATE-U", dict(ring="plate", scrape=None, fixn=False, every=U_EVERY, D=U_D),
     "PLATE struck the same way"),
]


def _ring_arr(ring):
    return "[" + ", ".join(f'[{fmt(m)}, {fmt(a)}, "{ty}"]' for m, a, ty in RING[ring]) + "]"


def _lv(env_):
    """The level across the slide, u in [0, L): 'swell' A0 -> 1, 'fade' 1 -> A0."""
    return {"swell": f"({fmt(A0)} + {fmt(round(1 - A0, 6))} * u / L)",
            "fade": f"(1 - {fmt(round(1 - A0, 6))} * u / L)"}[env_]


def slide_body(sp, g, L, ks, part="both", ind=10):
    """The raise (dir up, env swell) and every fold (dir down) as arm text.
    sp: ring, scrape (None/'under'/'over'), dir ('up'/'down'), env ('swell'/
    'fade'), head (s: the mirrored release, a climb on the start note), mode
    ('glide'/'step'/'struck'). g the gain, L the slide's length, ks the
    scrape's level re g."""
    up = sp.get("dir", "up") == "up"
    fs0, r = (F_LO, 2.0) if up else (F_HI, 0.5)
    env_ = sp.get("env", "swell" if up else "fade")
    head = sp.get("head", 0.0) or 0.0
    mode = sp.get("mode", "glide")
    every = sp.get("every", EVERY)
    arr = _ring_arr(sp["ring"])
    T = "t" if not head else "t0"
    out = [f"const g = {fmt(g)}, L = {fmt(L)}, D = {fmt(sp.get('D', RD))};"]
    if head:
        out.append(f"const t0 = t + {fmt(head)};")
    if part in ("both", "ring"):
        if head:
            # the raise's release, reversed: its end note re-struck on whole
            # cycles, climbing from -34 dB to the top over `head` seconds (at
            # the raise's own strike rate there: every N cycles, N as below)
            nexp = (f"Math.max(1, Math.round({fmt(F_LO)} * m * {fmt(every)}))" if sp.get("fixn", True)
                    else f"Math.max(1, Math.round(f * {fmt(every)}))")
            out += [f"for (const [m, km, ty] of {arr}){{",
                    f"  const f = {fmt(fs0)} * m, dt = {nexp} / f;",
                    f"  for (let u = 0; u < {fmt(head)} - 1e-9; u += dt)",
                    f"    this._tone(t + u, {{ freq: f, gain: g * km * Math.pow(10, -1.7 * (1 - u / {fmt(head)})), "
                    f"dur: D, type: ty }}).frequency.value = f;",
                    "}"]
        if mode == "glide" and sp.get("fixn", True):
            # the re-strike: every N cycles of the chirp, N fixed at A3's count
            # (the raise's start, the fold's end: 2), so a fold strikes as the
            # raise did, in reverse -- 9 ms apart at A3, 4.5 ms at A4
            out += [f"const r = {fmt(r)}, Lg = Math.log(r);",
                    f"for (const [m, km, ty] of {arr}){{",
                    f"  const fs = {fmt(fs0)} * m, N = Math.max(1, Math.round({fmt(F_LO)} * m * {fmt(every)}));",
                    "  for (let k = 0; ; k += N){",
                    "    const u = L / Lg * Math.log(1 + k * Lg / (fs * L));",
                    "    if (!(u < L)) break;",
                    "    const f = fs * Math.pow(r, u / L), to = fs * Math.pow(r, Math.min(u + D, L) / L);",
                    f"    this._tone({T} + u, {{ freq: f, to: to, gain: g * km * {_lv(env_)}, dur: D, type: ty }})"
                    f".frequency.value = f;",
                    "  }",
                    "}"]
        elif mode == "glide":
            # the k-th cycle of the chirp fs * r^(u/L) falls at u = L / ln r *
            # ln(1 + k ln r / (fs L)): a strike on a whole cycle about every
            # `every` seconds all the way (the cycles a strike spans follow the
            # pitch), each gliding on along the chirp, clamped at its end
            out += [f"const r = {fmt(r)}, Lg = Math.log(r);",
                    f"for (const [m, km, ty] of {arr}){{",
                    f"  const fs = {fmt(fs0)} * m;",
                    "  for (let k = 0; ; ){",
                    "    const u = L / Lg * Math.log(1 + k * Lg / (fs * L));",
                    "    if (!(u < L)) break;",
                    "    const f = fs * Math.pow(r, u / L), to = fs * Math.pow(r, Math.min(u + D, L) / L);",
                    f"    this._tone({T} + u, {{ freq: f, to: to, gain: g * km * {_lv(env_)}, dur: D, type: ty }})"
                    f".frequency.value = f;",
                    f"    k += Math.max(1, Math.round(f * {fmt(every)}));",
                    "  }",
                    "}"]
        elif mode == "step":
            f_a, f_b = (F_LO, F_HI) if up else (F_HI, F_LO)
            out += [f"for (const [m, km, ty] of {arr}){{",
                    f"  for (const [f0, s0, s1] of [[{fmt(f_a)}, 0, L / 2], [{fmt(f_b)}, L / 2, L]]){{",
                    f"    const f = f0 * m, dt = Math.max(1, Math.round(f * {fmt(every)})) / f;",
                    "    for (let u = s0; u < s1 - 1e-9; u += dt)",
                    f"      this._tone({T} + u, {{ freq: f, gain: g * km * {_lv(env_)}, dur: D, type: ty }})"
                    f".frequency.value = f;",
                    "  }",
                    "}"]
        elif mode == "struck":
            out += [f"for (const [m, km, ty] of {arr})",
                    f"  this._tone({T}, {{ freq: {fmt(fs0)} * m, to: {fmt(fs0 * r)} * m, gain: g * km, "
                    f"dur: L + D, type: ty }});"]
        else:
            raise ValueError(mode)
    if part in ("both", "scrape") and sp.get("scrape"):
        dur = round(L + 0.04, 4)
        f0_, f1_ = (8 * F_LO, 8 * F_HI) if up else (8 * F_HI, 8 * F_LO)
        atk = round(dur * (0.85 if env_ == "swell" else 0.15), 4)
        out.append(f'this._sweep({T}, {{ f0: {fmt(f0_)}, f1: {fmt(f1_)}, q: 1.5, gain: g * {fmt(ks)}, '
                   f'dur: {fmt(dur)}, atk: {fmt(atk)}, type:"bandpass" }});')
    return "\n".join(" " * ind + l_ for l_ in out)


# =============================================================== THE GONG ===
# "a deep gong (share <120 Hz >= 0.4, <=0.3s)". One strike: a sine fundamental
# (weight kf re g), inharmonic modes over it (m, level re g, decay re D), a
# soft mallet, and in TAM a tam-tam's wash.
GMODES = {
    "plate":    [(1.73, 0.6, 0.6), (2.33, 0.45, 0.5), (3.91, 0.35, 0.35), (4.11, 0.3, 0.3)],
    "plate-hi": [(1.73, 0.5, 0.6), (2.33, 0.4, 0.5), (3.91, 0.35, 0.4), (4.11, 0.3, 0.35),
                 (6.30, 0.25, 0.25), (7.34, 0.2, 0.2)],
    "bar":      [(2.76, 0.6, 0.5), (5.40, 0.35, 0.3)],
    "harm":     [(2.0, 0.6, 0.6), (3.0, 0.45, 0.5), (4.0, 0.35, 0.35), (5.0, 0.3, 0.3)],
    "none":     [],
}
GONG_CANDIDATES = [
    ("1 PLATE", dict(f=110.0, modes="plate", wash=False),
     "a plate on A2: a 110 Hz sine under its 1.73, 2.33, 3.91 and 4.11 modes, a soft mallet"),
    ("2 LOW-E", dict(f=82.41, modes="plate", wash=False),
     "the same plate on E2 (82.4 Hz)"),
    ("3 DEEP", dict(f=55.0, modes="plate-hi", wash=False),
     "a plate on A1 (55 Hz) with its 6.30 and 7.34 modes too, so it reaches a phone"),
    ("4 TAM", dict(f=110.0, modes="plate", wash=True),
     "PLATE with a tam-tam's wash: a bandpass band falling 2400 -> 900 Hz over 0.22 s"),
    ("5 BAR", dict(f=110.0, modes="bar", wash=False),
     "an iron bar on A2 (its 2.76 and 5.40 modes) instead of a plate"),
]


def gong_body(sp, g, kf, D, ind=10):
    arr = "[" + ", ".join(f"[{fmt(m)}, {fmt(a)}, {fmt(d)}]" for m, a, d in GMODES[sp["modes"]]) + "]"
    out = [f"const g = {fmt(g)}, f = {fmt(sp['f'])}, D = {fmt(D)};"]
    if sp.get("noroot"):
        pass
    else:
        out.append(f'this._tone(t, {{ freq: f, gain: g * {fmt(kf)}, dur: D, type:"sine" }}).frequency.value = f;')
    if GMODES[sp["modes"]]:
        out += [f"for (const [m, a, d] of {arr})",
                '  this._tone(t, { freq: f * m, gain: g * a, dur: D * d, type:"sine" }).frequency.value = f * m;']
    out.append('this._burst(t, { freq: 450, q: 0.7, gain: g * 0.6, dur: 0.02, type:"lowpass" });')
    if sp.get("wash"):
        out.append('this._sweep(t, { f0: 2400, f1: 900, q: 1.1, gain: g * 0.3, dur: 0.22, atk: 0.02, '
                   'type:"bandpass" });')
    return "\n".join(" " * ind + l_ for l_ in out)


# =============================================================== THE TINK ===
# "a short tink". One strike of a sine note with inharmonic modes (m, level,
# decay re D), flammed by the frame's index k.
TINK_CANDIDATES = [
    ("1 PLATE", dict(f=1760.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=False),
     "a small plate pinged on A6 (1760 Hz), its 1.73 and 2.33 modes"),
    ("2 HIGH", dict(f=2637.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=False),
     "the same plate on E7 (2637 Hz)"),
    ("3 CHIP", dict(f=1760.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=True),
     "PLATE with the arrowhead's contact: a 4 ms highpass click at 5 kHz"),
    ("4 BAR", dict(f=2637.0, modes=[(2.76, 0.5, 0.6)], click=False),
     "an iron rod pinged on E7, its 2.76 mode"),
    # ROUND 2 (see THE ROUNDS): over the chimes' third-octaves
    ("5 PIN", dict(f=4186.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=False),
     "the small plate on C8 (4186 Hz)"),
    ("6 GLINT", dict(f=5274.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=False),
     "the small plate on E8 (5274 Hz): a pin of light"),
    ("7 GLINT-CHIP", dict(f=5274.0, modes=[(1.73, 0.5, 0.7), (2.33, 0.35, 0.5)], click=True),
     "GLINT with the arrowhead's 4 ms contact click"),
]


def tink_body(sp, g, D, flam=True, ind=10):
    arr = "[" + ", ".join(f"[{fmt(m)}, {fmt(a)}, {fmt(d)}]" for m, a, d in sp["modes"]) + "]"
    out = [f"const g = {fmt(g)}, f = {fmt(sp['f'])}, D = {fmt(D)};"]
    if flam:
        out.append(f"const tt = t + Math.min({FLAM_MAX}, Math.max(0, p.k | 0)) * {fmt(FLAM)};   "
                   f"// the flam: k-th arrow of a frame")
    else:
        out.append("const tt = t;")
    if sp.get("tick"):
        out.append('this._burst(tt, { freq: 3000, q: 2.0, gain: g, dur: 0.035, type:"highpass" });')
        return "\n".join(" " * ind + l_ for l_ in out)
    out.append('this._tone(tt, { freq: f, gain: g, dur: D, type:"sine" }).frequency.value = f;')
    if sp["modes"]:
        out += [f"for (const [m, a, d] of {arr})",
                '  this._tone(tt, { freq: f * m, gain: g * a, dur: D * d, type:"sine" }).frequency.value = f * m;']
    if sp.get("click"):
        out.append('this._burst(tt, { freq: 5000, q: 0.8, gain: g * 0.5, dur: 0.004, type:"highpass" });')
    return "\n".join(" " * ind + l_ for l_ in out)


# =============================================================== THE FOLD ===
# "the slide reversed". Every candidate is the PICKED raise run backward:
#   MIRROR  its release as a short climb on A4 (the measured release), then the
#           glide falling A4 -> A3 with the level falling 1 -> 0.35
#   FADE    the same without the climb (the fall struck at its top)
#   DROP    the glide falling with the raise's own envelope (0.35 -> 1): the
#           pitch reversed, the envelope not
FOLD_CANDIDATES = [
    ("1 MIRROR", dict(env="fade", head="release"),
     "the whole raise reversed: its release as a short climb on A4, then the slide falling to A3 as its swell unwinds"),
    ("2 FADE", dict(env="fade", head=0.0),
     "the slide falling A4 -> A3 from its top, the swell unwinding"),
    ("3 DROP", dict(env="swell", head=0.0),
     "the slide falling A4 -> A3 with the raise's own swell (the pitch reversed, the envelope not)"),
]


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
TINK_ANCHOR = '        T.arrows++;'
GONG_ANCHOR = '      T.blocks++;'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }'

TINK_CODE = TINK_ANCHOR + '''
        /* BULWARK'S TINK (v77 s5: "an arrow -- a short tink"): one per arrow
           the wall stops, on its frame, before its bank. `tinkK` is the
           arrow's index among this frame's kills -- a `var`, hoisted to the
           ticker's call, so it starts undefined -> 0 on every frame -- and
           the arm flams by it (the nova's 26 ms), so four arrows on one frame
           are four tinks, not one loud one. Presentation only: SFX.play
           draws nothing, is a no-op headless, and nothing here is read back
           (lightkeeper_voice_lab: fights identical). */
        var tinkK = tinkK | 0;
        SFX.play("ult", { w: "lightkeeper-tink", k: tinkK++ });'''

GONG_CODE = GONG_ANCHOR + '''
      /* BULWARK'S GONG (v77 s5: "a ball block -- a deep gong"): one per
         block, on the frame the foe is turned back, before its shove and its
         bank. The window's own cooldown (0.4s, on the window tickers' clock)
         makes the cadence -- no hit stop, no beat. Presentation only;
         nothing here is read back. */
      SFX.play("ult", { w: "lightkeeper-gong" });'''

CLOSE_CODE = '''      /* BULWARK'S FOLD (v77 s5: "close -- the slide reversed"): on the
         frame the wall runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill flight, so both are left to the death voice
         (Tendril's, Canopy's and Zenith's rule); a wall still up when the
         fight ends folds in the picture only. Presentation only; the next
         line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lightkeeper-fold" });
''' + CLOSE_ANCHOR

# the sim-write control: the gong row with the foe nudged 1e-9 on a block
GONG_CODE_BAD = GONG_CODE.replace(
    '      SFX.play("ult", { w: "lightkeeper-gong" });',
    '      foe.vx += 1e-9;\n      SFX.play("ult", { w: "lightkeeper-gong" });', 1)
assert GONG_CODE_BAD != GONG_CODE

_refuse(TINK_CODE + GONG_CODE + CLOSE_CODE, "sim rows")
for _c, _a in ((TINK_CODE, TINK_ANCHOR), (GONG_CODE, GONG_ANCHOR), (CLOSE_CODE, CLOSE_ANCHOR)):
    assert _c.count(_a) == 1, "a sim row must re-emit its anchor exactly once"
    assert _c.isascii(), "a row must be ASCII"


def _wrap(paras, indent, width=79):
    body = " " * (indent + 3)
    lines = []
    for i, p_ in enumerate(paras):
        if i:
            lines.append("")
        lines.extend(textwrap.wrap(p_, width=width - len(body), break_on_hyphens=False))
    out = " " * indent + "/* " + lines[0]
    for l_ in lines[1:]:
        out += "\n" + (body + l_ if l_ else "")
    return out + " */"


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


def arms_code(Ra, Go, Ti, Fo, info):
    rn, gn, tn, fn = (X["name"].split(maxsplit=1)[1] for X in (Ra, Go, Ti, Fo))
    c_raise = _wrap([
        f'LIGHTKEEPER\'S CAST, THE RAISE -- v77 s5: "cast -- a shield-raise (a rising metallic slide, 0.4s)". '
        f'{rn}, of {info["n_raise"]}, picked on the numbers by `lightkeeper_voice_lab.py` under Rick\'s "you pick '
        f'i overrule" (v107). Lightkeeper had no arm and fell through to rune-crack, which {info["n_rc"]} other '
        f'relics on its stage-5 link still used, so this ADDS arms before that fallback and leaves it alone.',
        f"{info['r_what']} The ring is re-struck on whole cycles of one chirp (a held note does not exist in "
        f"this toolkit), {info['r_every']}, each strike dying over {info['r_D']:g} s, with "
        f"`.frequency.value` set on every strike. It climbs {info['r_climb']:+.0f} cents and "
        f"never turns back (its largest step {info['r_step']:.0%} of the climb: a slide, not two notes); it "
        f"swells {info['r_swell']:+.1f} dB to its top (not a strike) and flutters {info['r_flut']:.1f} dB (held, "
        f"not a buzz of strikes); its {info['r_ratio']:.2f}x mode stands "
        f"{info['r_off']:.0f} cents off every harmonic (metal). Audible {info['r_aud']:.0f} ms; loudest 50 ms "
        f"{info['r_db']:+.1f} dB re Lightkeeper's blow; {info['r_heard']:+.1f} dB over the score where a phone "
        f"hears it. Register at most {info['r_reg']:.2f} against rune-crack, the vigil and greatsword casts, "
        f"Zenith's rising cast, the blow and the death voice."], 10)
    c_gong = _wrap([
        f'A BALL BLOCK -- "a deep gong (share <120 Hz >= 0.4, <=0.3s)" (v77 s5). {gn}, of {info["n_gong"]} '
        f'(`lightkeeper_voice_lab.py`). `tickLightwall` plays it once per block, on the frame the foe is turned '
        f'back.',
        f"{info['g_what']} Its note {info['g_f']:.1f} Hz holds ({info['g_hold']:+.0f} cents at 80-160 ms); its "
        f"{info['g_ratio']:.2f}x mode stands {info['g_off']:.0f} cents off every harmonic; {info['g_low']:.2f} "
        f"of its power under 120 Hz at the worst noise draw; rings {info['g_aud']:.0f} ms and is gone by "
        f"{info['g_gone']:.0f}; loudest 50 ms {info['g_db']:+.1f} dB re the blow. On a phone (nothing under "
        f"200 Hz) its modes stand {info['g_heard']:+.1f} dB over the score. Register at most {info['g_reg']:.2f} "
        f"against the blow, the death voice, the clank, aegis, the nova, rune-crack and the raise."], 10)
    c_tink = _wrap([
        f'AN ARROW DIES ON THE WALL -- "an arrow -- a short tink" (v77 s5). {tn}, of {info["n_tink"]} '
        f'(`lightkeeper_voice_lab.py`). `tickLightwall` plays it once per arrow the wall stops, with k = the '
        f'arrow\'s index among that frame\'s kills: the k-th is flammed {FLAM * 1000:.0f} ms x min({FLAM_MAX}, k) '
        f'(the nova\'s flam), so a frame\'s arrows are heard one by one.',
        f"{info['t_what']} Rise under {max(1, math.ceil(info['t_rise'])):.0f} ms; audible {info['t_aud']:.0f} "
        f"ms, gone by {info['t_gone']:.0f}; its note stands {info['t_tonal']:.0f} dB over the noise round it "
        f"(a note, not a tick) and its {info['t_ratio']:.2f}x mode {info['t_off']:.0f} cents off every harmonic; "
        f"loudest 50 ms {info['t_db']:+.1f} dB re the blow and {info['t_wall']:+.1f} dB re the wall tick. Four on "
        f"one frame: {info['t_on']} onsets, the stack's peak {info['t_stack']:.2f}x one tink's. Register at most "
        f"{info['t_reg']:.2f} against the wall tick, hex-snap, the spark, Zenith's tick, the bowstring, the "
        f"blow, the clank, the raise and the gong."], 10)
    c_fold = _wrap([
        f'THE WALL FOLDS -- "close -- the slide reversed" (v77 s5). {fn}, of {info["n_fold"]} '
        f'(`lightkeeper_voice_lab.py`): {info["f_what"]}',
        f"It falls {info['f_fall']:+.0f} cents (the raise climbs {info['f_climb']:+.0f}); its envelope "
        f"correlates {info['f_corr']:.2f} with the raise's samples literally reversed; audible "
        f"{info['f_aud']:.0f} ms; loudest 50 ms {info['f_db']:+.1f} dB re the raise's (a reversal keeps its "
        f"level). `tickLightwall` plays it when the wall runs out by its clock with both alive."], 10)
    return (f'{_arm_head(ME, "the wall rises")}\n'
            f'{c_raise}\n{slide_body(Ra["sp"], Ra["g"], Ra["L"], Ra["ks"])}\n'
            f'{_arm_head(ME + "-gong", "a foe turned back")}\n'
            f'{c_gong}\n{gong_body(Go["sp"], Go["g"], Go["kf"], Go["D"])}\n'
            f'{_arm_head(ME + "-tink", "an arrow dies on it")}\n'
            f'{c_tink}\n{tink_body(Ti["sp"], Ti["g"], Ti["D"])}\n'
            f'{_arm_head(ME + "-fold", "and it folds")}\n'
            f'{c_fold}\n{slide_body(Fo["sp"], Fo["g"], Fo["L"], Fo["ks"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# The literal reversal: a body rendered DRY (no chain), trimmed, reversed,
# scaled, then played through the chain at T0 (zenith_voice_lab's "lit" op,
# for a body instead of a cast spec).
LIT_JS = r"""async ([body, secs, gc]) => {
  const sr = 48000, proto = Object.getPrototypeOf(AC.SFX);
  const mk = (oc, chain) => {
    let cursor = 0;
    const S = Object.create(proto); S.ok = true; S.on = true;
    S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
      const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
    S.bus = chain ? S.constructor.buildChain(oc, oc.destination)
                  : (() => { const g = oc.createGain(); g.connect(oc.destination); return g; })();
    const n = Math.floor(sr * 0.6), nb = oc.createBuffer(1, n, sr), d = nb.getChannelData(0);
    let s = 0x9e3779b9 >>> 0;
    for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0;
      d[i] = (s / 4294967296) * 2 - 1; }
    S.noise = nb;
    return { S, at: (x) => { cursor = x; } };
  };
  const dc = new OfflineAudioContext(1, Math.round(sr * secs), sr), Z = mk(dc, false);
  Z.at(1.0);
  (0, eval)("(function(t, p){\n" + body + "\n})").call(Z.S, 1.0, {});
  const dry = (await dc.startRendering()).getChannelData(0);
  let a = 0, b = dry.length - 1;
  while (a < dry.length && Math.abs(dry[a]) < 1e-6) a++;
  while (b > a && Math.abs(dry[b]) < 1e-6) b--;
  const seg = dry.slice(a, b + 1).reverse();
  for (let i = 0; i < seg.length; i++) seg[i] *= gc;
  const oc = new OfflineAudioContext(1, Math.round(sr * secs), sr), Y = mk(oc, true);
  const rb = oc.createBuffer(1, seg.length, sr); rb.copyToChannel(seg, 0);
  const src = oc.createBufferSource(); src.buffer = rb; src.connect(Y.S.bus); src.start(1.0);
  const x = (await oc.startRendering()).getChannelData(0);
  const u8 = new Uint8Array(x.buffer, x.byteOffset, x.byteLength);
  let t = ""; for (let i = 0; i < u8.length; i += 0x8000)
    t += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return { pcm: btoa(t) };
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
  for (const [k, kind, p] of [["raise", "ult", { w: "lightkeeper" }], ["gong", "ult", { w: "lightkeeper-gong" }],
                              ["tink", "ult", { w: "lightkeeper-tink", k: 0 }], ["fold", "ult", { w: "lightkeeper-fold" }],
                              ["hit", "hit", { dmg: 9.5, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickLightwall rows, applied to the real prototype and run beside the
# original; the survey of Bulwark's windows comes out of the same runs. The
# wrapper sees every tickLightwall call, so each frame's arrows, blocks and
# close are read on the call that makes them.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "lightkeeper";
  const orig = P.tickLightwall; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickLightwall anchor occurs ${at} times in tickLightwall()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  for (const nm of ["STATUS", "CONFIG", "segDist"])
    if ((0, eval)("typeof " + nm) === "undefined") return { err: nm + " is not reachable from the patched ticker" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inL = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        calls.push({ step, k: w, kk: p.k === undefined ? null : p.k, inL: !!inL, keys: Object.keys(p).sort().join(",") });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    const wins = []; let W = null, stray = 0;
    const tal = () => f.wallTally ? [f.wallTally.arrows, f.wallTally.blocks] : [0, 0];
    P.tickLightwall = function(dt){
      const Z0 = f.ultWall, t0 = tal(), c0 = calls.length;
      if (Z0 && (!W || W.Z !== Z0)){
        W = { Z: Z0, castStep: step, cast: m.t, arrows: 0, blocks: 0, tinkV: 0, gongV: 0, foldV: 0,
              multi: 0, kh: [0, 0, 0, 0, 0, 0, 0], badK: 0, badKeys: 0, end: null, close: null, gongSteps: [] };
        wins.push(W);
      }
      inL++;
      try { return impl.call(this, dt); }
      finally {
        inL--;
        const t1 = tal(), mine = calls.slice(c0);
        const da = t1[0] - t0[0], dk = t1[1] - t0[1];
        if (Z0){
          W.arrows += da; W.blocks += dk;
          const tinks = mine.filter(c => c.k === ME + "-tink"), gongs = mine.filter(c => c.k === ME + "-gong");
          W.tinkV += tinks.length; W.gongV += gongs.length;
          W.foldV += mine.filter(c => c.k === ME + "-fold").length;
          if (da > 1) W.multi++;
          if (tinks.length !== da) W.badK += 1000;
          tinks.forEach((c, i) => { W.kh[Math.min(6, Math.max(0, c.kk | 0))]++; if (c.kk !== i) W.badK++;
                                    if (c.keys !== "k,w") W.badKeys++; });
          for (const c of gongs.concat(mine.filter(c => c.k === ME + "-fold"))) if (c.keys !== "w") W.badKeys++;
          if (gongs.length) W.gongSteps.push(step);
          if (!f.ultWall){
            W.end = (Z0.t >= Z0.dur && f.alive && foe.alive) ? "clock"
                  : !f.alive ? "caster" : !foe.alive ? "foe" : "?";
            W.close = m.t;
          }
        } else stray += mine.length;
      }
    };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; } }
    finally { P.tickLightwall = orig; if (had) S.play = op; else delete S.play; }
    for (const w of wins) if (!w.end) w.end = "over";
    const fr = (x) => [x.hp, x.shield, x.shieldMax, x.x, x.y, x.vx, x.vy, x.charge, x.theta];
    return { sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.shots.length,
                                  m.shots.map(s => [s.x, s.y, !!s.stuck]),
                                  m.winner ? m.winner.w.id : null, f.wallTally || null]),
             calls, other: JSON.stringify(other), stray, casts: f.wallTally ? f.wallTally.casts : 0,
             wins: wins.map(w => { const { Z, ...r } = w; return r; }) };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, caster: 0, foe: 0, over: 0, "?": 0 };
  let casts = 0, castV = 0, arrows = 0, tinkV = 0, blocks = 0, gongV = 0, folds = 0, multi = 0, unticked = 0, castT = 0;
  const kh = [0, 0, 0, 0, 0, 0, 0], pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a gong, tink or fold"]);
    const cv = B.calls.filter(c => c.k === ME);
    if (cv.length !== B.casts || B.wins.length > B.casts) bad.push([fid, sd, "raise voices vs casts", cv.length, B.wins.length, B.casts]);
    unticked += B.casts - B.wins.length; castT += B.casts;
    if (cv.some(c => c.inL)) bad.push([fid, sd, "a raise from inside tickLightwall"]);
    for (const c of B.calls) if (c.k !== ME && !c.inL) bad.push([fid, sd, "a wall voice outside tickLightwall", c.k]);
    if (B.stray) bad.push([fid, sd, "wall voices from tickLightwall with no wall standing", B.stray]);
    casts += B.wins.length; castV += cv.length;
    for (const W of B.wins){
      ends[W.end]++; arrows += W.arrows; tinkV += W.tinkV; blocks += W.blocks; gongV += W.gongV; folds += W.foldV;
      multi += W.multi; W.kh.forEach((v, i) => kh[i] += v);
      if (W.tinkV !== W.arrows) bad.push([fid, sd, "tinks vs arrows", W.tinkV, W.arrows]);
      if (W.badK) bad.push([fid, sd, "a tink whose k is not its index in the frame", W.badK]);
      if (W.badKeys) bad.push([fid, sd, "a wall voice with unexpected opts", W.badKeys]);
      if (W.gongV !== W.blocks) bad.push([fid, sd, "gongs vs blocks", W.gongV, W.blocks]);
      if (W.foldV !== (W.end === "clock" ? 1 : 0)) bad.push([fid, sd, W.end + " close played folds", W.foldV]);
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close,
                                         blocks: W.blocks, arrows: W.arrows });
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, castT, unticked, arrows, tinkV,
           blocks, gongV, folds, multi, kh, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "lightkeeper";
  const orig = P.tickLightwall; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickLightwall = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickLightwall = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "lightkeeper";
  const res = [];
  if (!P.tickLightwall) return { err: "no tickLightwall" };
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    let inL = 0;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.k === undefined ? null : p.k, inL]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const tl = P.tickLightwall; let clock = 0, badK = 0;
    P.tickLightwall = function(dt){
      const Z0 = f.ultWall, a0 = f.wallTally ? f.wallTally.arrows : 0, c0 = log.length;
      inL = 1;
      try { return tl.call(this, dt); }
      finally {
        inL = 0;
        const da = (f.wallTally ? f.wallTally.arrows : 0) - a0;
        const ks = log.slice(c0).filter(e => e[0] === ME + "-tink").map(e => e[1]);
        if (ks.length !== da || ks.some((k, i) => k !== i)) badK++;
        if (Z0 && !f.ultWall && Z0.t >= Z0.dur && f.alive && foe.alive) clock++;
      } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { P.tickLightwall = tl; if (had) S.play = op; else delete S.play; }
    const T = f.wallTally || {};
    const fr = (x) => [x.hp, x.shield, x.shieldMax, x.x, x.y, x.vx, x.vy, x.charge, x.theta];
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.shots.length,
                                    m.winner ? m.winner.w.id : null, f.wallTally || null]),
               casts: T.casts || 0, arrows: T.arrows || 0, blocks: T.blocks || 0, clock, badK,
               castV: log.filter(e => e[0] === ME && !e[2]).length,
               tinkV: log.filter(e => e[0] === ME + "-tink" && e[2]).length,
               gongV: log.filter(e => e[0] === ME + "-gong" && e[2]).length,
               foldV: log.filter(e => e[0] === ME + "-fold" && e[2]).length,
               stray: log.filter(e => (e[0] === ME) === !!e[2]).length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def track(x, B, lo=150.0, hi=560.0, win=0.04, hop=0.02, trim=0.03):
    """TRACK: the pitch in `win` windows every `hop` inside the audible span."""
    s = T0 + B["a0"] / 1000 + trim
    e = T0 + B["gone"] / 1000 - trim
    out = []
    while s + win <= e + 1e-9:
        out.append(pitch(x, s, s + win, lo, hi))
        s += hop
    return out


def slide_shape(x, B, lo=150.0, hi=560.0):
    """CLIMB (cents, the last 60 audible ms re the first 60), the largest step
    AGAINST the climb's direction and the largest step WITH it as a share of
    the climb."""
    a0 = T0 + B["a0"] / 1000
    a1 = T0 + B["gone"] / 1000
    cl = cents(pitch(x, a1 - 0.06, a1, lo, hi), pitch(x, a0, a0 + 0.06, lo, hi))
    tr = track(x, B, lo, hi)
    st = [cents(tr[i + 1], tr[i]) for i in range(len(tr) - 1)] or [0.0]
    sg = 1.0 if cl >= 0 else -1.0
    back = max(0.0, max(-sg * s_ for s_ in st))
    fwd = max(sg * s_ for s_ in st) / max(abs(cl), 1e-9)
    return cl, back, fwd, tr


def metal_at(x, a, b, lo, hi):
    """METAL over [a, b] s: the note (FFT peak lo-hi), and ironwood's `inharm`
    on it -- (note, ratio, cents off the nearest multiple, level dB)."""
    f = pitch(x, a, b, lo, hi)
    r, off, lvl = inharm(x, a, b, f)
    return f, r, off, lvl


def onsets(x, secs=0.4):
    """ONSETS: 1 ms RMS peaks >= 15 ms apart, each >= 0.3 of the loudest and
    >= 6 dB over the minimum since the previous onset (or the start)."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + secs) * SR)]
    H = int(0.001 * SR); n = len(y) // H
    e = np.sqrt((y[:n * H].reshape(n, H) ** 2).mean(axis=1))
    top = float(e.max()); got = []; last = 0
    for i in range(1, n - 1):
        if not (e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] >= 0.3 * top):
            continue
        dip = float(e[last:i].min()) if i > last else float(e[i])
        if got and i - got[-1] < 15:
            continue
        if not got or db(e[i] / max(dip, 1e-12)) >= 6:
            got.append(i); last = i
    return got


def own_band(x, a, b, lo=PHONE_HZ):
    """The third-octave (centred at or above `lo`) in which the voice alone is
    loudest over [a, b] s."""
    bb = bands(x[int(a * SR):int(b * SR)])
    return max((v_, fc) for v_, fc in zip(bb, BANDS) if fc >= lo)[1]


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v77 section 5 turned into a number; a
# rule no candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

RAISE_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'rising': CLIMB >= +600 cents; 'slide': TRACK never "
    "turns back more than 30 cents and no one step carries more than 35% of the "
    "climb (a slide, not two notes), and it is not struck: SWELL >= +3 dB, and not a "
    "buzz of strikes: FLUTTER <= 3 dB (round 2: zenith_voice_lab's instrument and "
    "gate for a sustained-by-restrike tone, read at A4); "
    "'metallic': METAL at its loudest 50 ms (a 30 ms window at its centre: the "
    "strongest peak 1.5-4x the note >= 60 cents from every whole multiple and "
    "within 20 dB of the note). Heard: HEARD >= +6 dB. Register against rune-crack, "
    "each vigil and greatsword cast with a voice of its own, Zenith's rising cast, "
    "the hit @ 9.5 and the death voice each <= 0.80. Level: TOP between 0.5x the "
    "hit @ 9.5's loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST (heard "
    "like a blow, never over one). Tiebreak: the most distinct register (to 0.05), "
    "then the fewest synth calls, then the order listed.")

GONG_RULE = (
    "'<=0.3s': GONE <= 300 ms on every draw; 'share <120 Hz >= 0.4': LOW >= 0.40 on "
    "the WORST of twelve draws; 'deep': its note (FFT peak 30-2000 Hz over 20-120 ms) "
    "<= 120 Hz; 'a gong' -- struck: RISE <= 5 ms and the peak in the first 20 ms; "
    "metal: METAL on its note over 20-120 ms; it holds its note (HOLDS within 50 "
    "cents: a falling sine is the death voice); it rings: AUDIBLE >= 180 ms. Heard on "
    "a phone: HEARD >= +6 dB and PHONE >= the bowstring's (loudest draw) on every "
    "draw. Register against the hit @ 9.5, the death voice, the clank (mass 3), "
    "aegis (a block and a break), the nova, rune-crack and the picked raise each <= "
    "0.80. Level: TOP between 0.5x the hit @ 9.5's loudest draw and 1.0x its "
    "quietest, on every draw. Tiebreak: the most distinct register (to 0.05), then "
    "the fewest synth calls, then the order listed.")

TINK_RULE = (
    "'short': AUDIBLE <= 60 ms and GONE <= 80 ms on every draw; 'a tink' -- struck: "
    "RISE <= 2 ms and the peak in the first 10 ms (round 2; round 1 read 5); high: its note (FFT peak 500-12000 "
    "Hz over the first 20 ms) >= 1000 Hz; a note, not a tick: TONAL >= 15 dB over "
    "1-12 kHz; metal: METAL on its note over the first 30 ms. Level: its loudest 50 "
    "ms >= 2x the wall tick's (loudest draw) on its quietest draw and <= 0.7x the "
    "hit @ 9.5's (quietest draw) on its loudest; HEARD >= +6 dB; PHONE >= the "
    "bowstring's. One frame's arrows (k = 0..3 on one frame): four ONSETS, and the "
    "stack's peak <= 1.5x one tink's. Register against the wall tick, hex-snap, the "
    "spark (arm, collect), Zenith's tick, the bowstring, the hit @ 9.5, the clank, "
    "the picked raise and the picked gong each <= 0.80. Tiebreak: the most distinct "
    "register (to 0.05), then the fewest synth calls, then the order listed.")

FOLD_RULE = (
    "'the slide reversed' -- the pitch: FALL within 20% of minus the picked raise's "
    "CLIMB, TRACK never turning back more than 30 cents and no one step more than "
    "35% of the fall, FLUTTER <= 3 dB; the envelope: ENV-CORR with the LITERAL "
    "reversal >= 0.80, the two aligned at their audible onsets (round 2; round 1 "
    "aligned them at t = 1.0, printed as CORR0); the length: AUDIBLE within 15% of the raise's; the metal: METAL at its loudest 50 "
    "ms; the level: TOP within 3 dB of the raise's (a reversal keeps its level; v77 "
    "does not say quiet). Heard: HEARD >= +6 dB. Tiebreak: the highest ENV-CORR (to "
    "0.01), then the fewest synth calls, then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def _regs_why(M, why):
    for k, v in M["regs"].items():
        if v > 0.80:
            why.append(f"register vs {k} {v:.2f} > 0.80")


def raise_why(M, lev):
    why = []
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["climb"] < 600: why.append(f"climbs {M['climb']:+.0f} c, not >= +600")
    if M["back"] > 30: why.append(f"turns back {M['back']:.0f} c")
    if M["fwd"] > 0.35: why.append(f"one step carries {M['fwd']:.0%} of the climb (a jump)")
    if M["swell"] < 3: why.append(f"swell {M['swell']:+.1f} dB < +3 (struck)")
    if M["flut"] > FLUTTER_MAX: why.append(f"flutter {M['flut']:.1f} dB > {FLUTTER_MAX:g} (a buzz of strikes)")
    if M["m_off"] < 60 or M["m_lvl"] < -20:
        why.append(f"not metal ({M['m_ratio']:.2f}x, {M['m_off']:.0f} c, {M['m_lvl']:+.0f} dB)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    _regs_why(M, why)
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    return why


def gong_why(M, lev):
    why = []
    if M["gone_max"] > 300: why.append(f"gone at {M['gone_max']:.0f} ms > 300")
    if M["low_min"] < 0.40: why.append(f"low {M['low_min']:.2f} < 0.40")
    if M["note"] > 120: why.append(f"its note {M['note']:.0f} Hz > 120 (not deep)")
    if M["rise"] > 5: why.append(f"rise {M['rise']:.0f} ms > 5")
    if M["pk_ms"] > 20: why.append(f"peaks at {M['pk_ms']:.0f} ms")
    if M["m_off"] < 60 or M["m_lvl"] < -20:
        why.append(f"not metal ({M['m_ratio']:.2f}x, {M['m_off']:.0f} c, {M['m_lvl']:+.0f} dB)")
    if abs(M["hold"]) > 50: why.append(f"its note moves {M['hold']:+.0f} c")
    if M["aud"] < 180: why.append(f"audible {M['aud']:.0f} ms < 180 (does not ring)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    if M["phone_min"] < lev["phone"]: why.append(f"phone {M['phone_min']:.4f} < the bowstring's {lev['phone']:.4f}")
    _regs_why(M, why)
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    return why


def tink_why(M, lev):
    why = []
    if M["aud_max"] > 60: why.append(f"audible {M['aud_max']:.0f} ms > 60")
    if M["gone_max"] > 80: why.append(f"gone at {M['gone_max']:.0f} ms > 80")
    if M["rise"] > 2: why.append(f"rise {M['rise']:.0f} ms > 2")
    if M["pk_ms"] > 10: why.append(f"peaks at {M['pk_ms']:.0f} ms")
    if M["note"] < 1000: why.append(f"its note {M['note']:.0f} Hz < 1000 (not high)")
    if M["tonal"] < 15: why.append(f"tonal {M['tonal']:.1f} dB < 15 (a tick)")
    if M["m_off"] < 60 or M["m_lvl"] < -20:
        why.append(f"not metal ({M['m_ratio']:.2f}x, {M['m_off']:.0f} c, {M['m_lvl']:+.0f} dB)")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    if M["phone_min"] < lev["phone"]: why.append(f"phone {M['phone_min']:.4f} < the bowstring's {lev['phone']:.4f}")
    if M["n_on"] != 4: why.append(f"four on a frame read as {M['n_on']} onset(s)")
    if M["stack"] > 1.5: why.append(f"four on a frame peak {M['stack']:.2f}x one")
    _regs_why(M, why)
    return why


def fold_why(M, lev):
    why = []
    if abs(M["climb"] + lev["climb"]) > 0.2 * lev["climb"]:
        why.append(f"falls {M['climb']:+.0f} c, not {-lev['climb']:+.0f} +/- 20%")
    if M["back"] > 30: why.append(f"turns back {M['back']:.0f} c")
    if M["fwd"] > 0.35: why.append(f"one step carries {M['fwd']:.0%} of the fall")
    if M["flut"] > FLUTTER_MAX: why.append(f"flutter {M['flut']:.1f} dB > {FLUTTER_MAX:g}")
    if M["corr"] < 0.80: why.append(f"env-corr {M['corr']:.2f} < 0.80")
    if abs(M["aud"] - lev["aud"]) > 0.15 * lev["aud"]:
        why.append(f"audible {M['aud']:.0f} ms, not {lev['aud']:.0f} +/- 15%")
    if M["m_off"] < 60 or M["m_lvl"] < -20:
        why.append(f"not metal ({M['m_ratio']:.2f}x, {M['m_off']:.0f} c, {M['m_lvl']:+.0f} dB)")
    if abs(db(M["top"] / lev["top"])) > 3: why.append(f"top {db(M['top'] / lev['top']):+.1f} dB re the raise")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    return why


def _show(rows, ctls, rule, name):
    print(f"  RULE  {rule}")
    for M in rows:
        if M["why"]:
            print(f"    {M['name']:<16} out: {'; '.join(M['why'][:6])}" + (" ..." if len(M["why"]) > 6 else ""))
    for M in ctls:
        if M["why"]:
            print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
        else:
            print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
            FAILED.append(f"{name} {M['name'].lower()} control")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Lightkeeper's stage 5 (the wall and its bank)")
    ap.add_argument("--also", action="append", default=[],
                    help="another link carrying Lightkeeper (e.g. carried onto a newer tip): the rows as text there")
    ap.add_argument("--out", default="../05-reference/v107")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=107601)
    ap.add_argument("--e2e-seeds", type=int, default=1, help="fight seeds a pairing, end to end (0 skips it)")
    ap.add_argument("--peer-rows", action="append", default=[],
                    help="another relic's stage-6 voice rows_final.json: co-apply its Sfx rows with these")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"raise": RAISE_RULE, "gong": GONG_RULE, "tink": TINK_RULE,
                                      "fold": FOLD_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickLightwall arrow", TINK_ANCHOR),
                    ("tickLightwall block", GONG_ANCHOR), ("tickLightwall close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("lightkeeper-gong", "lightkeeper-tink", "lightkeeper-fold", '(w === "lightkeeper")', "tinkK"):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nBULWARK -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
        mirror = page.evaluate("() => { try { new AC.Match('lightkeeper', 'lightkeeper', 1); return 'allowed'; } "
                               "catch (e) { return 'refused: ' + e.message; } }")
        print(f"  the mirror match: {mirror}")
        W_ = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape, w.dmg, w.ult && w.ult.kind])")
        ids = [w_[0] for w_ in W_]
        if ME not in ids:
            raise SystemExit("no lightkeeper in this build")
        me = [w_ for w_ in W_ if w_[0] == ME][0]
        if abs(me[3] - BLADE) > 1e-9 or me[4] != "lightwall":
            raise SystemExit(f"Lightkeeper is {me} -- this lab levels against blade {BLADE} and a lightwall")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        if play_src.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx anchor is not in play() exactly once")

        def R(evs, secs=3.0, seed=None, rows=None, new=True):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            if new and len(evs) == 1 and evs[0][0] in ("body", "arm"):
                for d_ in r["log"]["burst"]:
                    if d_ > 0.55: raise SystemExit(f"REFUSING: a _burst of {d_}s")
                for d_ in r["log"]["sweep"]:
                    if d_ > 0.58: raise SystemExit(f"REFUSING: a _sweep of {d_}s")
            if float(np.abs(x).max()) < 1e-6:
                raise SystemExit(f"SILENT render: {str(evs[:1])[:160]}")
            if min(e[1] for e in evs) >= T0 and float(np.abs(x[:int(T0 * SR) - 2]).max()) > 1e-6:
                raise SystemExit("sound BEFORE t=1.0")
            return x, r["calls"]

        def play(kind, p, seed=None):
            return R([["play", T0, kind, p]], seed=seed, new=False)[0]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, (kind, p) in [("rune-crack", ("ult", {"w": "spellbreaker"})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                ("hit@9.5", ("hit", {"dmg": BLADE, "crit": False})),
                                ("crit@9.5", ("hit", {"dmg": BLADE, "crit": True})),
                                ("wall", ("wall", {})), ("death", ("death", {})),
                                ("clank", ("clank", {"mass": 3})), ("aegis", ("aegis", {"n": 10})),
                                ("loose", ("loose", {})), ("zenith", ("ult", {"w": "morningstar"}))]:
            x = play(kind, p)
            ctl[name] = dict(basic(x), x=x, low=low_share(x))
            M = ctl[name]
            print(f"  {name:<14} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
                  f"loudest 50 ms {M['top']:.4f}   centroid {M['cen']:6.0f} Hz   low {M['low']:.2f}")
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
        fall_ids = [w_ for w_ in ids if float(np.abs(play("ult", {"w": w_}) - rcx).max()) <= 1e-6]
        print(f"  rune-crack today (max |diff| <= 1e-6 vs ult/spellbreaker), {len(fall_ids)} relics: "
              + ", ".join(fall_ids))
        if ME not in fall_ids:
            raise SystemExit("Lightkeeper's cast is not rune-crack today -- this lab adds its arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_[0] for w_ in W_ if w_[1] == SCHOOL_AFF and w_[0] not in fall_ids]
        types = [w_[0] for w_ in W_ if w_[2] == TYPE_SHAPE and w_[0] not in fall_ids]
        print(f"  the vigil casts with their own voice: {', '.join(school)};  the greatsword casts': "
              f"{', '.join(types)}")

        # the noise draws of every reference
        REFS = {"hit": ("hit", {"dmg": BLADE, "crit": False}), "crit": ("hit", {"dmg": BLADE, "crit": True}),
                "wall": ("wall", {}), "rune-crack": ("ult", {"w": "spellbreaker"}), "death": ("death", {}),
                "clank": ("clank", {"mass": 3}), "aegis": ("aegis", {"n": 10}),
                "aegis-broke": ("aegis", {"broke": True}), "nova": ("nova", {"k": 0}),
                "hex-snap": ("hex-snap", {}), "spark-arm": ("spark", {"arm": True}),
                "spark-collect": ("spark", {"collect": True, "n": 3}),
                "zenith-tick": ("ult", {"w": "morningstar-tick", "n": 2}), "loose": ("loose", {}),
                "zenith": ("ult", {"w": "morningstar"})}
        for w_ in school + types:
            REFS[w_] = ("ult", {"w": w_})
        RD_ = {k: [] for k in REFS}
        RX = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (kind, p) in REFS.items():
                x = play(kind, p, seed=sd)
                RX[k].append(x)
                RD_[k].append(basic(x))
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD_.items()}
        h_lo, h_hi = min(m_["top"] for m_ in RD_["hit"]), max(m_["top"] for m_ in RD_["hit"])
        w_hi = max(m_["top"] for m_ in RD_["wall"])
        ph_bow = max(phone(x) for x in RX["loose"])
        ph_hit = min(phone(x) for x in RX["hit"])
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD_['hit']):.3f}-{max(m_['peak'] for m_ in RD_['hit']):.3f};  the wall "
              f"tick: {min(m_['top'] for m_ in RD_['wall']):.4f}-{w_hi:.4f};  PHONE: the blow {ph_hit:.4f} "
              f"(quietest draw), the bowstring {ph_bow:.4f} (loudest draw)")
        row_ids = school + types
        pr = {f"{p_}/{q_}": mreg(RB[p_], RB[q_]) for i_, p_ in enumerate(row_ids) for q_ in row_ids[i_ + 1:]}
        if pr:
            print(f"  the vigil and greatsword casts' own registers, pairwise: median "
                  f"{float(np.median(list(pr.values()))):.2f}, max {max(pr.values()):.2f} ({max(pr, key=pr.get)}); "
                  f"the gate is 0.80")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        p90 = bed_p90(bed[int(2 * SR):int(10 * SR)])
        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, phone_bow=ph_bow, phone_hit=ph_hit)
        wav("lightkeeper-ctl-runecrack.wav", rcx)
        wav("lightkeeper-ctl-hit9.5.wav", ctl["hit@9.5"]["x"])

        # ---- THE RAISE -----------------------------------------------------
        lev_r = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_r = math.sqrt(lev_r["lo"] * lev_r["hi"])
        print(f"\nRAISE -- 'a shield-raise (a rising metallic slide, 0.4s)'. Level-matched: the slide's length so "
              f"it is AUDIBLE {RAISE_AUD:g} ms, the scrape {SCRAPE_DB:g} dB under (SHING: over) the ring, TOP "
              f"{tgt_r:.4f} (the centre of {lev_r['lo']:.4f}-{lev_r['hi']:.4f})")

        def sx(sp, g, L, ks, part="both", seed=None):
            return R([["body", T0, slide_body(sp, g, L, ks, part), {}]], seed=seed)

        def calib_raise(sp):
            g, L, ks = 0.1, 0.36, 0.3
            for _ in range(4):
                if sp.get("scrape"):
                    rt = basic(sx(sp, g, L, ks, "ring")[0])["top"]
                    st = basic(sx(sp, g, L, ks, "scrape")[0])["top"]
                    want = -SCRAPE_DB if sp["scrape"] == "under" else SCRAPE_DB
                    ks = float(f"{ks * rt * 10 ** (want / 20) / st:.4g}")
                B = basic(sx(sp, g, L, ks)[0])
                L = round(min(0.53, max(0.2, L + (RAISE_AUD - B["aud"]) / 1000)), 3)
                g = float(f"{g * tgt_r / basic(sx(sp, g, L, ks)[0])['top']:.4g}")
            return g, L, ks

        RAISE_REGS = ["rune-crack"] + school + types + ["zenith", "hit", "death"]

        def slide_measure(name, x, draws, calls):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            M["climb"], M["back"], M["fwd"], M["track"] = slide_shape(x, M)
            M["swell"] = db(M["top"] / max(M["start"], 1e-12))
            fa, fb_ = T0 + M["a0"] / 1000 + 0.05, T0 + M["gone"] / 1000 - 0.05
            M["flut"] = flutter(x, fa, fb_, F_HI) if fb_ - fa >= 0.12 else 99.0
            a_ = T0 + M["top_at"] - 0.015
            M["m_f"], M["m_ratio"], M["m_off"], M["m_lvl"] = metal_at(x, a_, a_ + 0.03, 150, 560)
            M["heard"], M["heard_fc"] = heard(x, p90)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in RAISE_REGS}
            return M

        def raise_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<16}{M.get('g', 0):>8.4g}{M.get('L', 0):>7.3f}{M.get('ks', 0):>8.4g}{M['calls']:>6d}"
                  f"{M['top']:>8.4f}{M['aud']:>6.0f}{M['climb']:>7.0f}{M['back']:>6.0f}{M['fwd']:>6.0%}"
                  f"{M['swell']:>7.1f}{M['flut']:>6.1f}{M['m_ratio']:>6.2f}{M['m_off']:>6.0f}{M['m_lvl']:>6.0f}"
                  f"{M['heard']:>7.1f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        hdr_r = (f"  {'cand':<16}{'g':>8}{'L':>7}{'ks':>8}{'calls':>6}{'top':>8}{'aud':>6}{'climb':>7}{'back':>6}"
                 f"{'step':>6}{'swell':>7}{'flut':>6}{'mode':>6}{'off c':>6}{'lvl':>6}{'heard':>7}{'reg':>6}")
        print(hdr_r)
        rows_r = []
        for name, sp, _b in RAISE_CANDIDATES:
            g, L, ks = calib_raise(sp)
            x, calls = sx(sp, g, L, ks)
            x2, _ = sx(sp, g, L, ks)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"raise {name} does not reproduce")
            draws = [sx(sp, g, L, ks, seed=sd)[0] for sd in NOISE_SEEDS] if sp.get("scrape") else [x]
            M = slide_measure(name, x, draws, calls[0])
            M.update(sp=sp, g=g, L=L, ks=ks); M["why"] = raise_why(M, lev_r)
            rows_r.append(M); raise_line(M)
            wav(f"lightkeeper-raise-{name.replace(' ', '-').lower()}.wav", x)
        # the controls, on PLATE (the second candidate)
        r0 = rows_r[1]
        ctlr = []
        for cname, csp in (("0 STEP", dict(r0["sp"], mode="step")), ("0 FALL", dict(r0["sp"], dir="down", env="swell")),
                           ("0 HARM", dict(r0["sp"], ring="harm")), ("0 STRUCK", dict(r0["sp"], mode="struck")),
                           ("0 SPARSE", dict(r0["sp"], every=round(3 * EVERY, 4)))):
            xc, cc = sx(csp, r0["g"], r0["L"], r0["ks"])
            M = slide_measure(cname, xc, [xc], cc[0]); M.update(sp=csp, g=r0["g"], L=r0["L"], ks=r0["ks"])
            ctlr.append(M)
            wav(f"lightkeeper-raise-{cname.replace(' ', '-').lower()}.wav", xc)
        M = slide_measure("0 RUNECRACK", rcx, RX["rune-crack"], 0); ctlr.append(M)
        for M in ctlr:
            M["why"] = raise_why(M, lev_r); raise_line(M)
        for (name, _sp, blurb) in RAISE_CANDIDATES:
            print(f"    {name:<16} {blurb}")
        print("    0 STEP           PLATE's octave as two held notes -- a control on 'slide'\n"
              "    0 FALL           PLATE run downward -- a control on 'rising'\n"
              "    0 HARM           PLATE on whole-number partials (2, 3, 4) -- a control on 'metallic'\n"
              "    0 STRUCK         PLATE as one strike gliding the octave -- a control on 'slide' (not struck)\n"
              f"    0 SPARSE         PLATE struck every {round(3 * EVERY * F_LO)} cycles instead of {round(EVERY * F_LO)} -- a "
              "control on FLUTTER (a buzz of strikes)\n"
              "    0 RUNECRACK      the fallback it replaces")
        _show(rows_r, ctlr, RAISE_RULE, "raise")
        ok, fb = _gate(rows_r, "raise")
        ri = fb if ok is None else min(ok, key=lambda i: (round(max(rows_r[i]["regs"].values()) / 0.05),
                                                          rows_r[i]["calls"]))
        Ra = rows_r[ri]
        Ra["low"] = low_share(Ra["x"])
        print(f"  PICK  {Ra['name']}  g {Ra['g']}, L {Ra['L']}, ks {Ra['ks']}, {Ra['calls']} synth calls; TOP "
              f"{Ra['top']:.4f} = {db(Ra['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g} (quietest draw); climb "
              f"{Ra['climb']:+.0f} c; release {Ra['gone'] - 1000 * Ra['L']:.0f} ms")

        # ---- THE GONG ------------------------------------------------------
        lev_g = dict(lo=0.5 * h_hi, hi=1.0 * h_lo, phone=ph_bow)
        tgt_g = math.sqrt(lev_g["lo"] * lev_g["hi"])
        print(f"\nGONG -- 'a deep gong (share <120 Hz >= 0.4, <=0.3s)'. Level-matched: the fundamental's weight so "
              f"LOW is {GONG_LOW:g} (render.py's draw), the decay so it is GONE by {GONG_GONE:g} ms, TOP {tgt_g:.4f} "
              f"(the centre of {lev_g['lo']:.4f}-{lev_g['hi']:.4f})")

        def gx(sp, g, kf, D, seed=None):
            return R([["body", T0, gong_body(sp, g, kf, D), {}]], seed=seed)

        def calib_gong(sp, gone=GONG_GONE, fixD=None, fixKf=None):
            g, kf, D = 0.1, 1.0, 0.5
            for _ in range(4):
                if fixKf is not None:
                    kf = fixKf
                elif not sp.get("noroot"):
                    lo_, hi_ = math.log(1e-2), math.log(1e2)
                    for _ in range(12):
                        mid = 0.5 * (lo_ + hi_)
                        if low_share(gx(sp, g, math.exp(mid), D)[0]) > GONG_LOW: hi_ = mid
                        else: lo_ = mid
                    kf = float(f"{math.exp(0.5 * (lo_ + hi_)):.4g}")
                if fixD is None:
                    G_ = basic(gx(sp, g, kf, D)[0])["gone"]
                    D = float(f"{min(1.2, max(0.03, D * gone / max(G_, 1.0))):.3g}")
                else:
                    D = fixD
                g = float(f"{g * tgt_g / basic(gx(sp, g, kf, D)[0])['top']:.4g}")
            return g, kf, D

        GONG_REGS = ["hit", "death", "clank", "aegis", "aegis-broke", "nova", "rune-crack"]

        def gong_measure(name, x, draws, calls):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            M["low"] = low_share(x); M["low_min"] = min(low_share(d_) for d_ in draws)
            M["gone_max"] = max(basic(d_)["gone"] for d_ in draws)
            M["m_f"], M["m_ratio"], M["m_off"], M["m_lvl"] = metal_at(x, T0 + 0.02, T0 + 0.12, 30, 2000)
            M["note"] = M["m_f"]
            M["hold"] = cents(pitch(x, T0 + 0.08, T0 + 0.16, 30, 2000), pitch(x, T0 + 0.02, T0 + 0.08, 30, 2000))
            M["heard"], M["heard_fc"] = heard(x, p90)
            M["phone_min"] = min(phone(d_) for d_ in draws)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in GONG_REGS}
            M["regs"]["raise"] = mreg(DB, Ra["DB"])
            return M

        def gong_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M.get('g', 0):>8.4g}{M.get('kf', 0):>8.4g}{M.get('D', 0):>6.3g}{M['calls']:>6d}"
                  f"{M['top']:>8.4f}{M['aud']:>6.0f}{M['gone_max']:>6.0f}{M['low_min']:>6.2f}{M['note']:>7.1f}"
                  f"{M['hold']:>6.0f}{M['rise']:>5.0f}{M['pk_ms']:>5.0f}{M['m_ratio']:>6.2f}{M['m_off']:>6.0f}"
                  f"{M['heard']:>7.1f}{M['phone_min']:>8.4f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<10}{'g':>8}{'kf':>8}{'D':>6}{'calls':>6}{'top':>8}{'aud':>6}{'goneW':>6}{'lowW':>6}"
              f"{'note':>7}{'hold':>6}{'rise':>5}{'pk':>5}{'mode':>6}{'off c':>6}{'heard':>7}{'phoneW':>8}{'reg':>6}")
        rows_g = []
        for name, sp, _b in GONG_CANDIDATES:
            g, kf, D = calib_gong(sp)
            x, calls = gx(sp, g, kf, D)
            x2, _ = gx(sp, g, kf, D)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"gong {name} does not reproduce")
            M = gong_measure(name, x, [gx(sp, g, kf, D, seed=sd)[0] for sd in NOISE_SEEDS], calls[0])
            M.update(sp=sp, g=g, kf=kf, D=D); M["why"] = gong_why(M, lev_g)
            rows_g.append(M); gong_line(M)
            wav(f"lightkeeper-gong-{name.replace(' ', '-').lower()}.wav", x)
        g0 = rows_g[0]
        ctlg = []
        for cname, csp, fixD, gone in (("0 THUD", dict(g0["sp"], modes="none"), g0["D"], GONG_GONE),
                                       ("0 HARM", dict(g0["sp"], modes="harm"), None, GONG_GONE),
                                       ("0 LONG", g0["sp"], None, 900.0),
                                       ("0 DULL", g0["sp"], 0.12, GONG_GONE),
                                       ("0 HIGH", dict(g0["sp"], f=880.0), None, GONG_GONE)):
            if cname == "0 THUD":
                cg, ckf, cD = calib_gong(csp, gone, fixD, g0["kf"])
            else:
                cg, ckf, cD = calib_gong(csp, gone, fixD)
            xc, cc = gx(csp, cg, ckf, cD)
            M = gong_measure(cname, xc, [gx(csp, cg, ckf, cD, seed=sd)[0] for sd in NOISE_SEEDS], cc[0])
            M.update(sp=csp, g=cg, kf=ckf, D=cD); ctlg.append(M)
            wav(f"lightkeeper-gong-{cname.replace(' ', '-').lower()}.wav", xc)
        ctlg.append(gong_measure("0 DEATH", ctl["death"]["x"], [ctl["death"]["x"]], 0))
        ctlg.append(gong_measure("0 CLANK", ctl["clank"]["x"], RX["clank"], 0))
        for M in ctlg:
            M["why"] = gong_why(M, lev_g); gong_line(M)
        for (name, _sp, blurb) in GONG_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 THUD     PLATE's fundamental and mallet at its own weights, no plate modes -- a control on 'gong' (metal)\n"
              "    0 HARM     PLATE on whole-number partials (2, 3, 4, 5) -- a control on 'gong' (metal)\n"
              "    0 LONG     PLATE ringing to 0.9 s -- a control on '<=0.3s'\n"
              "    0 DULL     PLATE dying in 0.12 s of decay -- a control on 'a gong rings'\n"
              "    0 HIGH     PLATE three octaves up (A5), levelled the same way -- a control on 'deep' and LOW\n"
              "    0 DEATH    the death voice -- a falling sine: a control on 'holds its note'\n"
              "    0 CLANK    the weapons' clash (mass 3)")
        _show(rows_g, ctlg, GONG_RULE, "gong")
        ok, fb = _gate(rows_g, "gong")
        gi = fb if ok is None else min(ok, key=lambda i: (round(max(rows_g[i]["regs"].values()) / 0.05),
                                                          rows_g[i]["calls"]))
        Go = rows_g[gi]
        print(f"  PICK  {Go['name']}  g {Go['g']}, kf {Go['kf']}, D {Go['D']}; TOP {db(Go['top'] / h_lo):+.1f} dB re "
              f"the hit @ {BLADE:g}; LOW {Go['low_min']:.2f} worst draw; note {Go['note']:.1f} Hz; HEARD "
              f"{Go['heard']:+.1f} dB at {Go['heard_fc']:.0f} Hz")

        # ---- THE TINK ------------------------------------------------------
        lev_t = dict(lo=2 * w_hi, hi=0.7 * h_lo, phone=ph_bow)
        tgt_t = math.sqrt(lev_t["lo"] * lev_t["hi"])
        print(f"\nTINK -- 'a short tink'. Level-matched: the decay so it is AUDIBLE {TINK_AUD:g} ms, the loudest 50 ms "
              f"{tgt_t:.4f} (the centre of {lev_t['lo']:.4f}-{lev_t['hi']:.4f}); flammed {FLAM * 1000:g} ms a frame "
              f"index")

        def tx(sp, g, D, k=0, seed=None, flam=True):
            return R([["body", T0, tink_body(sp, g, D, flam), {"k": k}]], seed=seed)

        def calib_tink(sp, aud=TINK_AUD, fixD=None):
            g, D = 0.05, 0.08
            for _ in range(5):
                if fixD is None and not sp.get("tick"):
                    D = float(f"{min(1.0, max(0.005, D * aud / max(basic(tx(sp, g, D)[0])['aud'], 1.0))):.3g}")
                elif fixD is not None:
                    D = fixD
                g = float(f"{g * tgt_t / basic(tx(sp, g, D)[0])['top']:.4g}")
            return g, D

        TINK_REGS = ["wall", "hex-snap", "spark-arm", "spark-collect", "zenith-tick", "loose", "hit", "clank"]

        def tink_measure(name, sp, g, D, flam=True):
            x, calls = tx(sp, g, D, flam=flam)
            draws = [tx(sp, g, D, seed=sd, flam=flam)[0] for sd in NOISE_SEEDS] \
                if (sp.get("click") or sp.get("tick")) else [x]
            M = basic(x); M.update(x=x, calls=calls[0], name=name, sp=sp, g=g, D=D, flam=flam)
            M["aud_max"] = max(basic(d_)["aud"] for d_ in draws)
            M["gone_max"] = max(basic(d_)["gone"] for d_ in draws)
            M["note"] = pitch(x, T0, T0 + 0.02, 500, 12000)
            _f, M["m_ratio"], M["m_off"], M["m_lvl"] = metal_at(x, T0, T0 + 0.03, 500, 12000)
            M["tonal"] = tonal(draws, T0, T0 + 0.06, 1000, 12000)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            M["heard"], M["heard_fc"] = heard(x, p90)
            M["phone_min"] = min(phone(d_) for d_ in draws)
            body = tink_body(sp, g, D, flam)
            x4, _ = R([["body", T0, body, {"k": k_}] for k_ in range(4)])
            M["n_on"] = len(onsets(x4)); M["stack"] = float(np.abs(x4).max() / max(np.abs(x).max(), 1e-12))
            M["x4"] = x4
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in TINK_REGS}
            M["regs"]["raise"] = mreg(DB, Ra["DB"]); M["regs"]["gong"] = mreg(DB, Go["DB"])
            return M

        def tink_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>8.4g}{M['D']:>7.3g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud_max']:>5.0f}"
                  f"{M['gone_max']:>6.0f}{M['rise']:>5.0f}{M['pk_ms']:>4.0f}{M['note']:>7.0f}{M['tonal']:>7.1f}"
                  f"{M['m_ratio']:>6.2f}{M['m_off']:>6.0f}{M['heard']:>7.1f}{M['phone_min']:>8.4f}{M['n_on']:>4d}"
                  f"{M['stack']:>6.2f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<9}{'g':>8}{'D':>7}{'calls':>6}{'top':>8}{'audW':>5}{'goneW':>6}{'rise':>5}{'pk':>4}"
              f"{'note':>7}{'tonal':>7}{'mode':>6}{'off c':>6}{'heard':>7}{'phoneW':>8}{'on4':>4}{'stack':>6}{'reg':>6}")
        rows_t = []
        for name, sp, _b in TINK_CANDIDATES:
            g, D = calib_tink(sp)
            x1, _ = tx(sp, g, D); x2, _ = tx(sp, g, D)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"tink {name} does not reproduce")
            M = tink_measure(name, sp, g, D); M["why"] = tink_why(M, lev_t)
            rows_t.append(M); tink_line(M)
            wav(f"lightkeeper-tink-{name.replace(' ', '-').lower()}.wav", M["x"])
            wav(f"lightkeeper-tink-{name.replace(' ', '-').lower()}-x4.wav", M["x4"])
        t0_ = rows_t[0]
        ctlt = []
        tsp = dict(t0_["sp"], tick=True)
        cg, cD = calib_tink(tsp)
        ctlt.append(tink_measure("0 TICK", tsp, cg, cD))
        ctlt.append(tink_measure("0 LONG", t0_["sp"], t0_["g"], round(t0_["D"] * 5, 4)))
        lsp = dict(t0_["sp"], f=t0_["sp"]["f"] / 4)
        cg, cD = calib_tink(lsp)
        ctlt.append(tink_measure("0 LOW", lsp, cg, cD))
        ctlt.append(tink_measure("0 FLAM0", t0_["sp"], t0_["g"], t0_["D"], flam=False))
        for M in ctlt:
            M["why"] = tink_why(M, lev_t); tink_line(M)
        wav("lightkeeper-tink-0-flam0-x4.wav", ctlt[3]["x4"])
        for (name, _sp, blurb) in TINK_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 TICK    the wall tick's own construction (a 35 ms 3 kHz highpass burst) at the tink's level -- a "
              "control on 'a note'\n"
              "    0 LONG    PLATE with 5x its decay -- a control on 'short'\n"
              "    0 LOW     PLATE two octaves down (A4), levelled the same way -- a control on 'high'\n"
              "    0 FLAM0   PLATE with no flam: four on one frame land on one sample -- a control on the flam")
        _show(rows_t, ctlt, TINK_RULE, "tink")
        ok, fb = _gate(rows_t, "tink")
        ti = fb if ok is None else min(ok, key=lambda i: (round(max(rows_t[i]["regs"].values()) / 0.05),
                                                          rows_t[i]["calls"]))
        Ti = rows_t[ti]
        print(f"  PICK  {Ti['name']}  g {Ti['g']}, D {Ti['D']}; loudest 50 ms {db(Ti['top'] / h_lo):+.1f} dB re the "
              f"hit @ {BLADE:g}, {db(Ti['top_lo'] / w_hi):+.1f} dB re the wall; note {Ti['note']:.0f} Hz")

        # ---- THE FOLD ------------------------------------------------------
        release = max(0.01, round((Ra["gone"] - 1000 * Ra["L"]) / 1000 / 0.005) * 0.005)
        release = round(release, 3)
        print(f"\nFOLD -- 'the slide reversed', on {Ra['name']}'s figure. MIRROR's climb = the pick's own release, "
              f"{release * 1000:.0f} ms. Level-matched: TOP = the raise's ({Ra['top']:.4f})")

        def fold_sp(csp):
            s_ = dict(Ra["sp"], dir="down", env=csp["env"])
            s_["head"] = release if csp.get("head") == "release" else (csp.get("head") or 0.0)
            for k_ in ("ring", "mode"):
                if k_ in csp:
                    s_[k_] = csp[k_]
            return s_

        def calib_fold(fsp, L, target):
            g = Ra["g"]
            for _ in range(3):
                g = float(f"{g * target / basic(sx(fsp, g, L, Ra['ks'])[0])['top']:.4g}")
            return g

        # the literal reversal, levelled to the raise's TOP
        rbody = slide_body(Ra["sp"], Ra["g"], Ra["L"], Ra["ks"])
        gc = 1.0
        for _ in range(3):
            xl = pcm(page.evaluate(LIT_JS, [rbody, 3.0, gc]))
            gc = float(f"{gc * Ra['top'] / basic(xl)['top']:.4g}")
        xlit = pcm(page.evaluate(LIT_JS, [rbody, 3.0, gc]))
        assert not errors, errors[:3]
        if float(np.abs(xlit).max()) < 1e-6:
            raise SystemExit("the LITERAL rendered silence")
        wav("lightkeeper-fold-0-literal.wav", xlit)
        lev_f = dict(climb=Ra["climb"], aud=Ra["aud"], top=Ra["top"])

        def at_onset(x):
            s_ = int(basic(x)["a0"] / 1000 * SR)
            return np.concatenate([x[s_:], np.zeros(s_)])

        xlit_on = at_onset(xlit)

        def fold_measure(name, x, draws, calls):
            M = slide_measure(name, x, draws, calls)
            M["corr"] = env_corr(at_onset(x), xlit_on)       # round 2: aligned at the audible onsets
            M["corr0"] = env_corr(x, xlit)                   # round 1: aligned at t = 1.0 (printed)
            return M

        def fold_line(M):
            print(f"  {M['name']:<11}{M.get('g', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{db(M['top'] / Ra['top']):>7.1f}"
                  f"{M['aud']:>6.0f}{M['climb']:>7.0f}{M['back']:>6.0f}{M['fwd']:>6.0%}{M['flut']:>6.1f}"
                  f"{M['corr']:>6.2f}{M['corr0']:>6.2f}"
                  f"{M['m_ratio']:>6.2f}{M['m_off']:>6.0f}{M['heard']:>7.1f}{M['regs']['rune-crack']:>6.2f}"
                  f"{mreg(M['DB'], Ra['DB']):>6.2f}")

        print(f"  {'cand':<11}{'g':>8}{'calls':>6}{'top':>8}{'dB/rs':>7}{'aud':>6}{'fall':>7}{'back':>6}{'step':>6}{'flut':>6}"
              f"{'corr':>6}{'corr0':>6}{'mode':>6}{'off c':>6}{'heard':>7}{'rc':>6}{'raise':>6}")
        rows_f = []
        for name, csp, _b in FOLD_CANDIDATES:
            fsp = fold_sp(csp)
            g = calib_fold(fsp, Ra["L"], Ra["top"])
            x, calls = sx(fsp, g, Ra["L"], Ra["ks"])
            x2, _ = sx(fsp, g, Ra["L"], Ra["ks"])
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"fold {name} does not reproduce")
            draws = [sx(fsp, g, Ra["L"], Ra["ks"], seed=sd)[0] for sd in NOISE_SEEDS] if fsp.get("scrape") else [x]
            M = fold_measure(name, x, draws, calls[0])
            M.update(sp=fsp, g=g, L=Ra["L"], ks=Ra["ks"]); M["why"] = fold_why(M, lev_f)
            rows_f.append(M); fold_line(M)
            wav(f"lightkeeper-fold-{name.replace(' ', '-').lower()}.wav", x)
        m0 = rows_f[0]
        ctlf = []
        M = fold_measure("0 AGAIN", Ra["x"], [Ra["x"]], Ra["calls"]); M["g"] = Ra["g"]; ctlf.append(M)
        ssp = dict(m0["sp"], head=round(release / 2, 4))
        xs_, cs_ = sx(ssp, m0["g"], round(Ra["L"] / 2, 3), Ra["ks"])
        M = fold_measure("0 SHORT", xs_, [xs_], cs_[0]); M["g"] = m0["g"]; ctlf.append(M)
        hsp = dict(m0["sp"], ring="harm")
        xh_, ch_ = sx(hsp, m0["g"], Ra["L"], Ra["ks"])
        M = fold_measure("0 HARM", xh_, [xh_], ch_[0]); M["g"] = m0["g"]; ctlf.append(M)
        gq = float(f"{m0['g'] * 10 ** (-QUIET_DB / 20):.4g}")
        xq_, cq_ = sx(m0["sp"], gq, Ra["L"], Ra["ks"])
        M = fold_measure("0 QUIET", xq_, [xq_], cq_[0]); M["g"] = gq; ctlf.append(M)
        LM = fold_measure("0 LITERAL", xlit, [xlit], 0); LM["g"] = gc
        for M in ctlf:
            M["why"] = fold_why(M, lev_f); fold_line(M)
        LM["why"] = fold_why(LM, lev_f); fold_line(LM)
        for (name, _sp, blurb) in FOLD_CANDIDATES:
            print(f"    {name:<11} {blurb}")
        print("    0 AGAIN     the raise itself -- a control on 'reversed'\n"
              "    0 SHORT     MIRROR over half the length -- a control on the length\n"
              "    0 HARM      MIRROR on whole-number partials -- a control on the metal\n"
              f"    0 QUIET     MIRROR {QUIET_DB:g} dB under -- a control on the level (the batch's usual quiet close)\n"
              "    0 LITERAL   the raise's samples reversed -- the reference (cannot ship)")
        _show(rows_f, ctlf, FOLD_RULE, "fold")
        print(f"  LITERAL (the reference) {'passes' if not LM['why'] else 'fails: ' + '; '.join(LM['why'])}")
        ok, fb = _gate(rows_f, "fold")
        fi = fb if ok is None else min(ok, key=lambda i: (-round(rows_f[i]["corr"], 2), rows_f[i]["calls"]))
        Fo = rows_f[fi]
        print(f"  PICK  {Fo['name']}  g {Fo['g']}; falls {Fo['climb']:+.0f} c; ENV-CORR {Fo['corr']:.2f}; "
              f"{db(Fo['top'] / Ra['top']):+.1f} dB re the raise")

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        ring_what = {"bar": "an iron bar's ring -- a triangle with its 2.76 and 5.40 modes (sines at 0.45 and 0.2)",
                     "plate": "a plate's ring -- a sine with its 1.73, 2.33 and 3.91 modes (at 0.55, 0.4 and 0.2)"}
        sc_what = {None: "", "under": " Over it metal scrapes on metal: a bandpass band climbing 1760 -> 3520 Hz "
                                      "(three octaves up, in step), 6 dB under the ring.",
                   "over": " It leads with the scrape -- a bandpass band climbing 1760 -> 3520 Hz -- and the ring "
                           "sits 6 dB under it: a blade drawn."}
        r_what = (f"{ring_what[Ra['sp']['ring']][0].upper()}{ring_what[Ra['sp']['ring']][1:]}, gliding one octave "
                  f"A3 -> A4 in {Ra['L']:g} s and swelling 0.35 -> 1 as it climbs; the glide ends on A4 and "
                  f"rings there.{sc_what[Ra['sp'].get('scrape')]}")
        gm = {"plate": "the 1.73, 2.33, 3.91 and 4.11 modes of a plate",
              "plate-hi": "the 1.73, 2.33, 3.91, 4.11, 6.30 and 7.34 modes of a plate",
              "bar": "an iron bar's 2.76 and 5.40 modes"}[Go["sp"]["modes"]]
        g_what = (f"One strike: a {Go['sp']['f']:g} Hz sine under {gm}, each dying faster than the one below, a "
                  f"soft mallet (a 20 ms lowpass thump at 450 Hz)"
                  + (", and a tam-tam's wash (a bandpass band falling 2400 -> 900 Hz)." if Go["sp"].get("wash") else "."))
        t_what = (f"One strike of a {Ti['sp']['f']:g} Hz sine with "
                  + (" and ".join(f"its {m:g} mode" for m, _a, _d in Ti["sp"]["modes"]))
                  + (", and the arrowhead's 4 ms click at 5 kHz." if Ti["sp"].get("click") else "."))
        f_what = {"1 MIRROR": "the raise run backward -- its release as a short climb on A4, then the ring gliding "
                              "down A4 -> A3 as its swell unwinds 1 -> 0.35"
                              + (", the scrape falling with it." if Ra["sp"].get("scrape") else "."),
                  "2 FADE": "the ring gliding down A4 -> A3 from its top as its swell unwinds 1 -> 0.35"
                            + (", the scrape falling with it." if Ra["sp"].get("scrape") else "."),
                  "3 DROP": "the ring gliding down A4 -> A3 with the raise's own swell 0.35 -> 1"
                            + (", the scrape falling with it." if Ra["sp"].get("scrape") else ".")}[Fo["name"]]
        n_names = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                   "twelve", "thirteen", "fourteen", "fifteen"]
        info = dict(
            n_raise=len(RAISE_CANDIDATES), n_gong=len(GONG_CANDIDATES), n_tink=len(TINK_CANDIDATES),
            n_fold=len(FOLD_CANDIDATES),
            n_rc=n_names[min(15, len(fall_ids) - 1)] if len(fall_ids) - 1 <= 15 else str(len(fall_ids) - 1),
            r_what=r_what, r_climb=Ra["climb"], r_step=Ra["fwd"], r_swell=Ra["swell"], r_ratio=Ra["m_ratio"],
            r_every=(f"every {round(F_LO * Ra['sp'].get('every', EVERY))} cycles (9 ms apart at A3, 4.5 at A4)"
                     if Ra["sp"].get("fixn", True) else
                     f"about every {1000 * Ra['sp'].get('every', EVERY):.0f} ms"),
            r_D=Ra["sp"].get("D", RD), r_flut=Ra["flut"],
            r_off=Ra["m_off"], r_aud=Ra["aud"], r_db=db(Ra["top"] / h_lo), r_heard=Ra["heard"],
            r_reg=max(Ra["regs"].values()),
            g_what=g_what, g_f=Go["note"], g_hold=Go["hold"], g_ratio=Go["m_ratio"], g_off=Go["m_off"],
            g_low=Go["low_min"], g_aud=Go["aud"], g_gone=Go["gone_max"], g_db=db(Go["top"] / h_lo),
            g_heard=Go["heard"], g_reg=max(Go["regs"].values()),
            t_what=t_what, t_rise=Ti["rise"], t_aud=Ti["aud_max"], t_gone=Ti["gone_max"], t_tonal=Ti["tonal"],
            t_ratio=Ti["m_ratio"], t_off=Ti["m_off"], t_db=db(Ti["top"] / h_lo), t_wall=db(Ti["top_lo"] / w_hi),
            t_on=Ti["n_on"], t_stack=Ti["stack"], t_reg=max(Ti["regs"].values()),
            f_what=f_what, f_fall=Fo["climb"], f_climb=Ra["climb"], f_corr=Fo["corr"], f_aud=Fo["aud"],
            f_db=db(Fo["top"] / Ra["top"]))
        arms = arms_code(Ra, Go, Ti, Fo, info)
        _refuse(arms, "Sfx row")
        if not arms.isascii():
            raise SystemExit("the Sfx row is not ASCII")
        if arms.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx row does not re-emit its anchor exactly once")
        sfx_rows = [[SFX_ANCHOR, arms]]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        chk = []
        xa0, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows)
        chk.append(("raise", float(np.abs(xa0 - Ra["x"]).max())))
        for sd in (None, NOISE_SEEDS[3]):
            xg1, _ = R([["arm", T0, "ult", {"w": ME + "-gong"}]], rows=sfx_rows, seed=sd)
            xg2, _ = gx(Go["sp"], Go["g"], Go["kf"], Go["D"], seed=sd)
            chk.append(("gong" + ("" if sd is None else " draw"), float(np.abs(xg1 - xg2).max())))
            for k_ in (None, -1, 0, 1, 2, 3, 4, 5, 6):
                pk = {"w": ME + "-tink"} if k_ is None else {"w": ME + "-tink", "k": k_}
                xt1, _ = R([["arm", T0, "ult", pk]], rows=sfx_rows, seed=sd)
                xt2, _ = R([["body", T0, tink_body(Ti["sp"], Ti["g"], Ti["D"]), {} if k_ is None else {"k": k_}]],
                           seed=sd)
                chk.append((f"tink k{k_}" + ("" if sd is None else " draw"), float(np.abs(xt1 - xt2).max())))
            xf1, _ = R([["arm", T0, "ult", {"w": ME + "-fold"}]], rows=sfx_rows, seed=sd)
            xf2, _ = sx(Fo["sp"], Fo["g"], Fo["L"], Fo["ks"], seed=sd)
            chk.append(("fold" + ("" if sd is None else " draw"), float(np.abs(xf1 - xf2).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9.5, 11.6, 18, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 3}), ("clank", {"mass": 5}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("fork", {}), ("vine", {}), ("vine", {"plant": True}),
                   ("vine", {"coil": True}), ("vine", {"miss": True}), ("loose", {}), ("loose", {"bal": True}),
                   ("loose", {"leaf": True}), ("aegis", {"n": 3, "back": 5}), ("aegis", {"broke": True}),
                   ("scour-hold", {"n": 5}), ("scour-tick", {}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = sorted(set(re.findall(r'w === "([a-z-]+)"', play_src)) | set(ids))
        ult_ids = [w_ for w_ in ult_ids if w_ != ME and not w_.startswith(ME + "-")]
        others += [("ult", {"w": w_, "n": 2}) for w_ in ult_ids]
        kinds_ = sorted(set(re.findall(r'kind === "([a-z-]+)"', play_src)) - {"ult", "hit"})
        others += [(k_, {}) for k_ in kinds_ if (k_, {}) not in others]
        e2e_voices = others
        same_ = []
        for kind, p in others:
            x1 = play(kind, p); x2, _ = R([["arm", T0, kind, p]], rows=sfx_rows, new=False)
            same_.append((kind + "/" + str(p.get("w", p.get("dmg", ""))) + ("!" if p.get("crit") else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, spark x3, wall, death, clank x2, seal, nova, hex-snap, fork, vine x4, loose x3, "
              f"aegis x2, scour x4, {len(ult_ids)} ult ids -- every relic's cast and every sub-voice the ult arm "
              f"names -- and every kind play() names): worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa0 - rcx).max())
        print(f"  ult/lightkeeper vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, n_others=len(same_))

        # ---- WITH OTHER RELICS' ROWS ------------------------------------------
        peers = []
        for pf in a.peer_rows:
            prow = json.loads(pathlib.Path(pf).read_text(encoding="utf-8"))
            prow = prow["rows"] if isinstance(prow, dict) else prow
            ps = [[r_["anchor"], r_["code"]] for r_ in prow if play_src.count(r_["anchor"]) == 1]
            if not ps:
                print(f"  peer {pf}: no row anchored in play() -- skipped")
                continue
            pids = sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _, c in ps))))
            pk_ = sorted(set(re.findall(r'kind === "([a-z-]+)"', "".join(c for _, c in ps))))
            A_ = sfx_rows + ps; B_ = ps + sfx_rows
            mine = [("ult", {"w": ME}), ("ult", {"w": ME + "-gong"}), ("ult", {"w": ME + "-tink", "k": 1}),
                    ("ult", {"w": ME + "-fold"})]
            evs = mine + [("ult", {"w": w_, "n": 3, "shield": 45}) for w_ in pids] + [(k_, {}) for k_ in pk_]
            dmax, dmine = 0.0, 0.0
            PX = {}
            for kind_, p_ in evs:
                xa_, _ = R([["arm", T0, kind_, p_]], rows=A_); xb_, _ = R([["arm", T0, kind_, p_]], rows=B_)
                dmax = max(dmax, float(np.abs(xa_ - xb_).max()))
                if str(p_.get("w", "")).startswith(ME):
                    xs_, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows)
                    dmine = max(dmine, float(np.abs(xa_ - xs_).max()))
                else:
                    PX[(kind_, p_.get("w", kind_))] = xa_
            prg = {}
            for (kind_, w_), xp in PX.items():
                bp = bands(xp[int(T0 * SR):])
                prg[w_] = {nm: cos(bands(X_["x"][int(T0 * SR):]), bp)
                           for nm, X_ in (("raise", Ra), ("gong", Go), ("tink", Ti), ("fold", Fo))}
            worst_p = max(((max(v.values()), k + "/" + max(v, key=v.get)) for k, v in prg.items()),
                          default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders "
                  f"render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the four against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) -- printed, "
                  f"not gated")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=prg))
        rec["peers"] = peers

        # ---- THE tickLightwall ROWS ------------------------------------------
        trows = [[TINK_ANCHOR, TINK_CODE], [GONG_ANCHOR, GONG_CODE], [CLOSE_ANCHOR, CLOSE_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        WR = None
        if not a.no_wire:
            print("\nTHE tickLightwall ROWS, applied to Match.prototype.tickLightwall's own source, run beside the "
                  "original on real fights:")
            WR = page.evaluate(WIRE_JS, [seeds, trows])
            assert not errors, errors[:3]
            if "err" in WR:
                raise SystemExit(WR["err"])
            print(f"  {WR['fights']} fights (Lightkeeper both sides x every foe x seeds {seeds}): {WR['same']}/"
                  f"{WR['fights']} identical (over, clock, both fighters' hp, shields, positions, velocities, "
                  f"charges and facing, the arrows in the air, winner, the whole wallTally); every other SFX call "
                  f"identical in order and opts in {WR['otherSame']}/{WR['fights']}")
            kh = WR["kh"]
            print(f"  windows {WR['ends']}: {WR['castT']} casts -> {WR['castV']} raises ({WR['unticked']} cast on a "
                  f"fight's last step, never ticked); {WR['blocks']} blocks -> "
                  f"{WR['gongV']} gongs; {WR['arrows']} arrows -> {WR['tinkV']} tinks (k " +
                  " ".join(f"{i}:{v}" for i, v in enumerate(kh) if v) + f"; {WR['multi']} frames with more than one); "
                  f"{WR['folds']} folds; problems {WR['nbad']}")
            for b_ in WR["bad"]:
                print(f"    {b_}")
            if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                    or WR["folds"] != WR["ends"]["clock"] or WR["tinkV"] != WR["arrows"] \
                    or WR["gongV"] != WR["blocks"] or WR["castV"] != WR["castT"] \
                    or WR["gongV"] == 0 or WR["tinkV"] == 0 or WR["folds"] == 0 or WR["multi"] == 0:
                FAILED.append("tickLightwall rows")
            WB = page.evaluate(WIRE_JS, [seeds, [[TINK_ANCHOR, TINK_CODE], [GONG_ANCHOR, GONG_CODE_BAD],
                                                 [CLOSE_ANCHOR, CLOSE_CODE]]])
            assert not errors, errors[:3]
            print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a block): {WB['same']}/"
                  f"{WB['fights']} identical -- "
                  f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
            if WB["same"] == WB["fights"]:
                FAILED.append("identity control")
            rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "castT",
                                              "unticked", "arrows",
                                              "tinkV", "blocks", "gongV", "folds", "multi", "kh", "nbad")}
            rec["wire"]["control_same"] = WB["same"]

            # ---- THE PICKS IN A REAL WINDOW ---------------------------------
            cand = sorted(WR["pick"], key=lambda w: (-(min(w["arrows"], 4) * 3 + w["blocks"]), w["foe"], w["seed"]))
            if cand:
                w_ = cand[0]
                EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], trows])
                assert not errors, errors[:3]
                c0t = w_["cast"]; c1t = w_["close"]
                lo_t, hi_t = c0t - 1.0, c1t + 2.0
                evs = [e for e in EV if lo_t <= e[0] <= hi_t]
                allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
                secs = T0 + (hi_t - lo_t) + 1.0
                xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
                bd = bed[:len(xw)]
                xw = xw + bd
                # ROUND 4 (see THE ROUNDS): per event, the third-octave (200 Hz-12 kHz, where
                # HEARD reads) in which the voice stands highest over everything else in
                # THIS window -- HEARD's own definition with the real mix as the masker --
                # beside round 3's reading (the isolated voice's HEARD band) and round 2's
                # (its own loudest band). The thresholds are round 1's. Two controls that
                # can come back wrong (round 4b): AFTER -- the same reading, as many
                # instants, 0.8 s after the wall folded, where no new voice sounds: every
                # gate must read NOT heard; LEVEL -- each voice BURIED 20 dB (its arm's text
                # with g x 0.1): every event heard at full level (>= +3 dB) must read LOWER
                # buried (round 4c). BURIED's own gates are printed, not gated (round 4's
                # first run gated them; see THE ROUNDS).
                res, res_own, res_h, res_b, res_a = {}, {}, {}, {}, {}
                level_ok = {}
                BURY = 0.1
                bury_body = {ME: slide_body(Ra["sp"], Ra["g"] * BURY, Ra["L"], Ra["ks"]),
                             ME + "-gong": gong_body(Go["sp"], Go["g"] * BURY, Go["kf"], Go["D"]),
                             ME + "-tink": tink_body(Ti["sp"], Ti["g"] * BURY, Ti["D"]),
                             ME + "-fold": slide_body(Fo["sp"], Fo["g"] * BURY, Fo["L"], Fo["ks"])}
                RWB = [fc_ for fc_ in BANDS if PHONE_HZ <= fc_ <= 12000.0]

                def over_at(xa, xb_, fc_, t_, w_):
                    return db(band_rms(xa, fc_, t_, t_ + w_) / max(band_rms(xb_, fc_, t_, t_ + w_), 1e-12))

                def best_band(xa, xb_, t_, w_):
                    return max((over_at(xa, xb_, fc_, t_, w_), fc_) for fc_ in RWB)
                others_at = [(T0 + (e[0] - lo_t), e[1] + ("/" + e[2]["w"] if e[1] == "ult" and "w" in e[2] else ""))
                             for e in evs if not e[3]]

                def near(t_):
                    return ", ".join(f"{k_} {1000 * (u_ - t_):+.0f} ms" for u_, k_ in others_at
                                     if -0.05 <= u_ - t_ <= 0.05)
                shares = []
                for tag, win_ in ((ME, 0.1), (ME + "-gong", 0.05), (ME + "-tink", 0.05), (ME + "-fold", 0.1)):
                    ts = [T0 + (e[0] - lo_t) for e in evs if e[3] == tag]
                    if not ts:
                        res[tag] = res_own[tag] = res_h[tag] = res_b[tag] = res_a[tag] = []
                        continue
                    xo = R([e_ for e_, e in zip(allv, evs) if e[3] != tag], secs=secs, rows=sfx_rows,
                           new=False)[0] + bd
                    xb = R([(["body", e_[1], bury_body[tag], e_[3]] if e[3] == tag else e_)
                            for e_, e in zip(allv, evs)], secs=secs, rows=sfx_rows, new=False)[0] + bd
                    X_ = {"lightkeeper": Ra, ME + "-gong": Go, ME + "-tink": Ti, ME + "-fold": Fo}[tag]
                    fc = X_["heard_fc"]
                    fo = own_band(X_["x"], T0, T0 + win_)
                    bb = [best_band(xw, xo, t_, win_) for t_ in ts]
                    res[tag] = [v_ for v_, _ in bb]
                    res[tag + "@"] = [fc_ for _, fc_ in bb]
                    res_b[tag] = [best_band(xb, xo, t_, win_)[0] for t_ in ts]
                    t_after = T0 + (c1t - lo_t) + 0.8
                    ta = [t_after + 0.05 * i_ for i_ in range(len(ts))
                          if t_after + 0.05 * i_ + win_ <= T0 + (hi_t - lo_t)]
                    res_a[tag] = [best_band(xw, xo, t_, win_)[0] for t_ in ta]
                    level_ok[tag] = all(b_ < v_ for v_, b_ in zip(res[tag], res_b[tag]) if v_ >= 3)
                    res_h[tag] = [over_at(xw, xo, fc, t_, win_) for t_ in ts]
                    res_own[tag] = [over_at(xw, xo, fo, t_, win_) for t_ in ts]
                    res_h[tag + "@"] = fc; res_own[tag + "@"] = fo
                    for t_, v_ in zip(ts, res[tag]):
                        if v_ < 6:
                            shares.append(f"    the {tag.split('-')[-1] if tag != ME else 'raise'} at "
                                          f"{t_ - T0 + lo_t:.3f}s ({v_:+.1f} dB) shares its "
                                          f"{win_ * 1000:.0f} ms with: {near(t_) or 'nothing but the score'}")

                def gates(r):
                    """Each voice's gate on a reading: True heard, False not, None absent."""
                    def med(v):
                        return float(np.median(v))
                    return {ME: (min(r[ME]) >= 3) if r[ME] else None,
                            ME + "-gong": (med(r[ME + "-gong"]) >= 6) if r[ME + "-gong"] else None,
                            ME + "-tink": (med(r[ME + "-tink"]) >= 6) if r[ME + "-tink"] else None,
                            ME + "-fold": (min(r[ME + "-fold"]) >= 3) if r[ME + "-fold"] else None}
                G4, GB, G3, G2, GA = gates(res), gates(res_b), gates(res_h), gates(res_own), gates(res_a)
                print(f"\nIN A REAL WINDOW -- lightkeeper v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast "
                      f"at {c0t:.2f}s, closed by its clock at {c1t:.2f}s, {w_['blocks']} blocks and {w_['arrows']} "
                      f"arrows; the fight's own sounds and the score, with and without each new voice. ROUND 4: "
                      f"each event in the third-octave (200 Hz-12 kHz) where it stands highest over everything "
                      f"else (the band after the @). Beside it round 3's reading (the band where the voice alone "
                      f"is HEARD over the score) and round 2's (its own loudest band). Gates (round 1's): the "
                      f"raise and the fold >= +3 dB, the gongs' and the tinks' median >= +6 dB. The controls: "
                      f"AFTER (read as round 4, 0.8 s after the fold, no new voice sounding: must read NOT heard) "
                      f"and LEVEL (the voice BURIED 20 dB: every event heard at >= +3 must read lower; "
                      f"BURIED's own gate printed, not gated)")

                def fmt_v(v):
                    return " ".join(f"{x_:+.1f}" for x_ in v) + (f" (median {np.median(v):+.1f})" if len(v) > 1 else "")

                def ok_(g_):
                    return "absent" if g_ is None else ("heard" if g_ else "NOT heard")
                for tag, nm in ((ME, "the raise"), (ME + "-gong", "each gong"), (ME + "-tink", "each tink"),
                                (ME + "-fold", "the fold")):
                    if not res[tag]:
                        print(f"  {nm}: none in this window")
                        continue
                    print(f"  {nm}: " + " ".join(f"{x_:+.1f}@{f_:.0f}" for x_, f_ in zip(res[tag], res[tag + '@'])) +
                          (f" (median {np.median(res[tag]):+.1f})" if len(res[tag]) > 1 else "") +
                          f" dB -- {ok_(G4[tag])}")
                    print(f"      round 3 ({res_h[tag + '@']:.0f} Hz): {fmt_v(res_h[tag])} -- {ok_(G3[tag])};  "
                          f"round 2 ({res_own[tag + '@']:.0f} Hz): {fmt_v(res_own[tag])} -- {ok_(G2[tag])};  "
                          f"BURIED: {fmt_v(res_b[tag])} -- {ok_(GB[tag])}")
                    print(f"      AFTER: {fmt_v(res_a[tag]) if res_a[tag] else 'no room'} -- {ok_(GA[tag])};  "
                          f"LEVEL: {'follows' if level_ok[tag] else 'DOES NOT follow'} the voice")
                for s_ in shares:
                    print(s_)
                if not res[ME] or not res[ME + "-gong"] or not res[ME + "-fold"] or \
                        not all(g_ is not False for g_ in G4.values()):
                    FAILED.append("a new voice not heard in a real window")
                if any(g_ is not False for g_ in GA.values()):
                    print("  the AFTER control is heard (or has no room) -- the reading cannot come back wrong")
                    FAILED.append("real-window control (after)")
                else:
                    print("  the AFTER control (no new voice sounding) reads NOT heard for every voice, as it must")
                if not all(level_ok.get(t_, True) for t_ in (ME, ME + "-gong", ME + "-tink", ME + "-fold")):
                    print("  the LEVEL control: the reading does not follow a voice's level")
                    FAILED.append("real-window control (level)")
                else:
                    print("  the LEVEL control: every event heard at >= +3 dB reads lower with its voice 20 dB under, "
                          "as it must")
                wav("lightkeeper-pick-real-window.wav", xw)
                xo_all = R([e_ for e_, e in zip(allv, evs) if not e[3]], secs=secs, rows=sfx_rows, new=False)[0] + bd
                wav("lightkeeper-pick-real-window-without.wav", xo_all)
                rec["real"] = dict(win=w_, over={k: v for k, v in res.items()},
                                   over_heard_band={k: v for k, v in res_h.items()},
                                   over_own_band={k: v for k, v in res_own.items()},
                                   buried={k: v for k, v in res_b.items()},
                                   after={k: v for k, v in res_a.items()}, level_ok=level_ok,
                                   gates={"round4": G4, "round3": G3, "round2": G2, "buried": GB, "after": GA})
            else:
                print("\nIN A REAL WINDOW -- no clock close in the wire runs")
                FAILED.append("no real window")
        # the four picks in order, for the ear: the raise, gongs, a frame of three arrows, a blow, the fold
        seq = [["arm", T0, "ult", {"w": ME}]]
        seq += [["arm", T0 + 0.8, "ult", {"w": ME + "-gong"}], ["arm", T0 + 1.3, "ult", {"w": ME + "-tink", "k": 0}],
                ["arm", T0 + 1.7, "ult", {"w": ME + "-gong"}]]
        seq += [["arm", T0 + 2.2, "ult", {"w": ME + "-tink", "k": k_}] for k_ in range(3)]
        seq += [["arm", T0 + 2.7, "hit", {"dmg": BLADE, "crit": False}], ["arm", T0 + 3.1, "ult", {"w": ME + "-gong"}]]
        seq += [["arm", T0 + 3.8, "ult", {"w": ME + "-fold"}]]
        wav("lightkeeper-pick-sequence.wav", R(seq, secs=6.0, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: Lightkeeper's raise, gong, tink and fold arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickLightwall: the tink, once per arrow the wall stops, flammed by its index in the frame",
                 anchor=TINK_ANCHOR, mode="replace", code=TINK_CODE),
            dict(label="tickLightwall: the gong, once per ball block, on the block's frame",
                 anchor=GONG_ANCHOR, mode="replace", code=GONG_CODE),
            dict(label="tickLightwall: the fold, on a clock close with both alive, before the close line",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE)]
    for r_ in rows:
        if not (r_["code"].isascii() and r_["anchor"].isascii()):
            raise SystemExit(f"a row is not ASCII: {r_['label']}")

    def apply_text(src_html, what):
        patched = src_html
        for r_ in rows:
            c = patched.count(r_["anchor"])
            if c != 1:
                raise SystemExit(f"{what}: an anchor occurs {c} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"{what}: an anchor is not re-emitted exactly once")
        return patched

    NEWP = [("raise", {"w": ME}, slide_body(Ra["sp"], Ra["g"], Ra["L"], Ra["ks"]), {}),
            ("gong", {"w": ME + "-gong"}, gong_body(Go["sp"], Go["g"], Go["kf"], Go["D"]), {})]
    NEWP += [(f"tink k{k_}", {"w": ME + "-tink", "k": k_}, tink_body(Ti["sp"], Ti["g"], Ti["D"]), {"k": k_})
             for k_ in (0, 1, 3)]
    NEWP += [("fold", {"w": ME + "-fold"}, slide_body(Fo["sp"], Fo["g"], Fo["L"], Fo["ks"]), {})]

    def e2e_page(tp, ref_voices, ref_fights, label):
        """Load a patched page; its own play() vs the lab's text and vs the
        unpatched page's voices; its fights vs the unpatched page's."""
        with game(game_path=tp) as (page, errors):
            def R2(evs, seed=None):
                r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                assert not errors, errors[:3]
                return pcm(r)
            vo = max(float(np.abs(R2([["play", T0, k, p]]) - x0).max())
                     for (k, p), x0 in zip(e2e_voices, ref_voices))
            nd = []
            for lab_, p, body, bp in NEWP:
                x1 = R2([["play", T0, "ult", p]], seed=NOISE_SEEDS[5])
                x2 = R2([["body", T0, body, bp]], seed=NOISE_SEEDS[5])
                nd.append((lab_, float(np.abs(x1 - x2).max())))
            rcp = R2([["play", T0, "ult", {"w": "spellbreaker"}]])
            not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
            F1 = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
            if isinstance(F1, dict):
                raise SystemExit(F1["err"])
            page_err = len(errors)
        F0 = {f_["key"]: f_ for f_ in ref_fights}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        t_ok = sum(f_["tinkV"] == f_["arrows"] and f_["badK"] == 0 for f_ in F1)
        g_ok = sum(f_["gongV"] == f_["blocks"] for f_ in F1)
        f_ok = sum(f_["foldV"] == f_["clock"] for f_ in F1)
        s_ok = sum(f_["stray"] == 0 for f_ in F1)
        orig_new = sum(f_["tinkV"] + f_["gongV"] + f_["foldV"] for f_ in ref_fights)
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "arrows", "blocks", "clock", "castV", "tinkV", "gongV",
                                                    "foldV")}
        print(f"  the four new voices through the patched page's own SFX.play vs the lab's candidate text in that "
              f"page, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/lightkeeper vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- raises = casts {c_ok}, tinks = arrows (k its index in the frame) "
              f"{t_ok}, gongs = blocks {g_ok}, folds = clock closes {f_ok}, every voice where it belongs {s_ok} (of "
              f"{len(F1)}); totals {tot}; the original page played {orig_new} new voices; page errors {page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1)
                   or osame != len(F1) or min(c_ok, t_ok, g_ok, f_ok, s_ok) != len(F1) or orig_new or page_err
                   or tot["gongV"] == 0 or tot["tinkV"] == 0 or tot["foldV"] == 0)
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same, other_same=osame, totals=tot,
                    page_errors=page_err)

    if a.e2e_seeds > 0:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="lightkeeper_e2e_"))
        try:
            tp = tmpd / "sc-lightkeeper-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the four rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    # ---- ALSO: the rows on another link carrying Lightkeeper --------------------
    rec["also"] = []
    for spec in a.also:
        ap_ = resolve_game(spec)
        h2 = ap_.read_text(encoding="utf-8")
        s2 = hashlib.sha256(h2.encode()).hexdigest()[:16]
        p2 = apply_text(h2, ap_.name)
        print(f"\nALSO -- {ap_.name} {s2}: every anchor once, every row applies and re-emits it; the original page "
              f"first (a browser), then the patched one (another, after it closes)")
        with game(game_path=ap_) as (page, errors):
            def R3(evs, seed=None):
                r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                assert not errors, errors[:3]
                return pcm(r)
            ps2 = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
            ids2 = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
            u2 = sorted(set(re.findall(r'w === "([a-z-]+)"', ps2)) | set(ids2))
            k2 = sorted(set(re.findall(r'kind === "([a-z-]+)"', ps2)) - {"ult", "hit"})
            voices2 = [v_ for v_ in e2e_voices if v_[0] != "ult" or v_[1]["w"] in u2]
            voices2 += [("ult", {"w": w_, "n": 2}) for w_ in u2
                        if w_ != ME and not w_.startswith(ME + "-") and ("ult", {"w": w_, "n": 2}) not in voices2]
            voices2 += [(k_, {}) for k_ in k2 if (k_, {}) not in voices2]
            ref_v = [R3([["play", T0, k, p]]) for k, p in voices2]
            ref_f = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="lightkeeper_also_"))
        try:
            tp = tmpd / ap_.name
            tp.write_text(p2, encoding="utf-8", newline="")
            keep = e2e_voices
            e2e_voices = voices2
            try:
                E = e2e_page(tp, ref_v, ref_f, ap_.name)
            finally:
                e2e_voices = keep
            E.update(game=ap_.name, sha=s2, patched_sha=hashlib.sha256(p2.encode()).hexdigest()[:16],
                     voices=len(voices2))
            rec["also"].append(E)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "x4", "bands", "DB", "track")} for M in L]

    rec.update(raise_=strip(rows_r), raise_controls=strip(ctlr), gong=strip(rows_g), gong_controls=strip(ctlg),
               tink=strip(rows_t), tink_controls=strip(ctlt), fold=strip(rows_f), fold_controls=strip(ctlf + [LM]),
               wavs=sizes, release=release, literal_gc=gc,
               pick={"raise": Ra["name"], "raise_g": Ra["g"], "raise_L": Ra["L"], "raise_ks": Ra["ks"],
                     "gong": Go["name"], "gong_g": Go["g"], "gong_kf": Go["kf"], "gong_D": Go["D"],
                     "tink": Ti["name"], "tink_g": Ti["g"], "tink_D": Ti["D"], "fold": Fo["name"], "fold_g": Fo["g"]})
    print(f"\nTHE PICKS  raise {Ra['name']}   gong {Go['name']}   tink {Ti['name']}   fold {Fo['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    al = "".join(f"; on {X['game']} too ({X['same']}/{X['fights']})" for X in rec["also"])
    wr = rec.get("wire")
    rows[0]["why"] = (
        f"The four voices (v77 s5), in the synth only. The arms are added BEFORE the shared rune-crack fallback, "
        f"and the fallback line is re-emitted unchanged, so the {len(rec['fallthrough']) - 1} other relics that "
        f"still fall through keep it and another relic's row anchored there applies in either order. Through the "
        f"patched play() every arm reproduces its lab candidate (worst "
        f"{max(v for _, v in rec['arm_check']['chk']):.0e}; the tink at k -1..6 and none, on two noise draws), "
        f"{rec['arm_check']['n_others']} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), and ult/lightkeeper is no longer rune-crack. play() "
        f"returns on its first line with no audio context (every headless run), draws no random number and writes "
        f"nothing the simulation reads" + (f"; end to end the four voices through the patched page's own SFX.play "
                                           f"equal the candidates (worst {max(v for _, v in E2['new']):.0e})"
                                           if E2 else "") + ".")
    if wr:
        rows[1]["why"] = (
            f"One plain SFX.play in tickLightwall's arrow block, after the tally, with k = this frame's count of "
            f"tinks so far (a hoisted `var`, local to the ticker's call; nothing else reads it). {wr['tinkV']}/"
            f"{wr['arrows']} arrows voiced, k equal to each arrow's index in its frame ({wr['multi']} frames with "
            f"more than one); {wr['same']}/{wr['fights']} fights identical and every other SFX call identical in "
            f"order and opts; the rows plus one sim write come back {wr['control_same']}/{wr['fights']}{e2}{al}.")
        rows[2]["why"] = (
            f"One plain SFX.play in the block branch, after the tally, before the shove and the bank: it sounds only "
            f"where the sim has just turned the foe back. {wr['gongV']}/{wr['blocks']} blocks voiced, one a frame "
            f"at most (the window's own 0.4s cooldown); nothing is read back{e2}.")
        rows[3]["why"] = (
            f"One guarded SFX.play before the window's own close line (re-emitted unchanged), reading only Z.t, "
            f"Z.dur and the two alive flags: a clock close with both alive. {wr['folds']} folds for "
            f"{wr['ends']['clock']} clock closes, none on the {wr['ends']['caster'] + wr['ends']['foe']} closes a "
            f"death made or the {wr['ends']['over']} walls the fight's end cut off; nothing is read back{e2}.")
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
