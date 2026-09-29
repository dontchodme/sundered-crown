#!/usr/bin/env python3
"""EXSANGUINATE'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v106.

    python widowmaker_voice_lab.py --game <a link carrying Widowmaker's stage 5> --rows rows.json

v76 §4 SOUND, every word of it: "cast -- a low inhale, 0.4s; the drain -- the
bleed's own drip voice reversed and pitched by the foe's stack count, quiet;
close -- nothing." The brief's stage 3 (v106's stage 6): "picture, voice,
carry". Rick, for the batch's art and sound: "you pick i overrule". So this lab
does not offer a spread -- it renders three to five candidates a voice beside
CONTROLS that can come back wrong, prints the numbers each pick is made on, and
PICKS by a rule written in this file (`*_RULE`, `*_why`). He overrules from one
clip.

THE BLEED HAS NO DRIP VOICE. §4 says to reverse "the bleed's own drip voice",
and there is none to reverse: no SFX kind and no arm is played by a hemorrhage
tick, a hemorrhage apply or anything else of the bleed's (the synth's kinds and
arms are read off the page and printed; `tickStatus`'s dps branch plays
nothing). So this lab MAKES one -- DRIP, below: a drop landing in a pool, one
struck sine whose pitch chirps UP as it rings out (the bubble's own rise) -- and
ships only its REVERSE, as the drain. The forward drip is NOT wired to the
bleed: every bleeding fight in the game would change its sound, and nobody
asked for that. It lives here as the definition the reverse is checked against
(LITERAL, and the FORWARD control), and it is flagged for Rick.

THE NOVA'S VOICE IS RETIRED. `ult/widowmaker` plays the old nova's "wet slice"
(three lines, the Sfx `ult` arm keyed on the relic, v106 §5's list). The one Sfx
row REPLACES those three lines with the inhale and adds the drain's arm beside
it. It does not touch the shared rune-crack fallback, so every other relic's
row anchored there applies in either order.

THE TWO EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/widowmaker`, which `fireUlt` already plays for every
         relic (the common head, before the drain branch). No sim line.
  drain  `ult/widowmaker-drain {n}` from `tickStatus`'s drain block, right after
         the line that books the gain (`me.drainTally.drained += me.hp - h0`,
         re-emitted unchanged), ONCE PER WHOLE HP DRAINED: when the running
         total crosses a whole number. That is the unit §4 gives the drain's
         picture ("a red '+n' floats on her every 1 hp drained (not per tick --
         `hurt`'s rounding rule)"), so the ear and the float count the same
         thing. `n` = the bleeding foe's hemorrhage stacks at that tick (1..4:
         the foe's bleed ceiling is hemorrhage's 4, v106 §6.3 / probe [9]). The
         drain block runs on live steps only, so a hit stop holds the drip as it
         holds the drain; nothing runs after `over`; a heal capped at maxHp
         drains nothing and drips nothing.
  close  nothing (§4). No row touches `tickDrain`.

THE CONTROLS, and what each one is for:
  rune-crack   v88 published 0.608 / 450 ms -- reproduced before anything new
               is quoted (with BAR 0.364 / 300 ms and hit@11.6 0.443 / 80 ms)
  the slice    what `ult/widowmaker` plays TODAY (the nova's wet slice), read
               off the anchor's own three lines and checked against the page
  hit@10.75    Widowmaker's own blow (the blade holds at 10.75): the level every
               voice is judged against, on its quietest / loudest noise draw
  wall         the commonest sound in a fight: the quiet drain's floor
  the school   the bloodsworn casts with a voice of their own (read off the page)
  the type     the twinblade casts with a voice of their own (read off the page)
  woosh        `scour-woosh`, the game's one voice made of moving air
  loose        the bowstring: a phone's floor (Culverin's and Briarwand's)
  death        the heaviest low voice in the game
  spark        `spark {collect, n}`: the house's heal voice ("already means
               healed", v71) -- the drain is a heal, and must not be that one
  fork, hex-snap, morningstar-tick   the house's wet split, the runic snap and
               Zenith's in-window tick chime: small voices the drip must not be
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  EXHALE, TICK, WHISTLE, HISS, RUMBLE, SLICE-NOW, WOOSH   the inhale with its
               bands run DOWN / its bands as fixed-filter bursts / at q 14 /
               three octaves up / an octave and a half down / the wet slice /
               the tornado: each must fail the cast's rule
  FORWARD, FLAT, LOUD, SPARK, NOISE, RAW   the drip itself (not reversed) /
               one note for every count / at the blow's level / the heal voice
               / a reversed noise swell / the reverse without
               `.frequency.value = f`: each must fail the drain's rule
  LITERAL      the drip rendered and its samples REVERSED (a reference: an arm
               cannot reverse samples -- every clip rebuilds the synth
               synchronously, v88 §6b, Zenith's MIRROR note)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT, generated with its constants rounded
    first and rendered by evaluating that text on the synth; the row is then
    applied to `Sfx.prototype.play`'s own source and rendered again, and must
    match to TOL = 1e-5 (REPRO, the same text rendered twice, is printed).
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's and
    bindweed_voice_lab's, imported unchanged (E50 = 50 ms RMS at a 5 ms hop;
    TOP = the loudest 50 ms; PEAK = the sample peak; AUDIBLE = first to last
    5 ms RMS window above 2% of the voice's own loudest; GONE = where it ends,
    from the event; RISE = 10 -> 90% of the 1 ms envelope; LATE = (energy
    centre - audible start) / audible; REG = cosine of 1/3-octave band
    amplitudes, 25 Hz-16 kHz, the median over noise draws; PITCH = FFT peak,
    Hann, zero-padded, parabolic; TONAL = bindweed's: how far the
    draw-averaged spectrum's sharpest 1/48-octave peak stands over the median
    of its third-octave neighbourhood, dB -- averaged noise reads a few dB, a
    tone tens), and five of ironhail_voice_lab's (v108; copied, not imported,
    because that lab is not on the chain yet): BREATH-RISE, DIPS / REGROW,
    CENTROID, HEARD (the loudest third-octave AT OR ABOVE 200 Hz against the
    score's p90 there, dB -- a phone reproduces little under 200 Hz) and PHONE
    (the TOP of the voice high-passed at 200 Hz, Culverin's v96).
  * New here, each with a control that can come back wrong:
      DRAWN-IN   cents from the draw-averaged power centroid (100 Hz-8 kHz) of
                 the cast's first 100 audible ms to that of its last 100 (the
                 air is drawn in: its band rises -- EXHALE must fail)
      TOP-PLACE  where the loudest 50 ms sits in AUDIBLE, 0..1 (printed; the
                 cast's tiebreak)
      E5         the drip's 5 ms RMS at a 1 ms hop (a drip is 60 ms long: the
                 50 ms measures are too coarse to see its shape):
        LAST5    where its loudest 5 ms sits in its audible span, 0..1
        SMOOTH   drops of >= 3 dB under the running top of E5 on the way up to
                 it (a swell, not a flutter -- RAW must fail)
        FALL     cents from the pitch over the first third of its audible span
                 to the last third (the drip's chirp rises; reversed, it falls
                 -- FORWARD must fail)
        LAND     the pitch over the 15 ms before its loudest 5 ms: the note it
                 lands on
        ENV-CORR5  Pearson correlation of two E5 curves in dB (each floored 40
                 dB under its own top), aligned at t = 1.0, over the span either
                 is above its floor -- against LITERAL
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's time scale is solved so it is AUDIBLE 400 ms and its gain
    puts TOP at the centre of its window; the drain's gain puts its TOP at the
    centre of ITS window at count 2. Constants are rounded BEFORE any measured
    render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of §4 turned into numbers):
  * "0.4s": AUDIBLE 330-470 ms, v100's reading of Portcullis's "0.4s" (and
    v108's of Ironhail's).
  * "AN INHALE": a breath -- air, not a note (TONAL <= 10 dB, v101's "noise, not
    a chime"); one breath (no dip, no regrowth); it swells (BREATH-RISE >= 40
    ms, the top >= 80 ms in) -- DRAWN IN: its band RISES (DRAWN-IN >= +300
    cents), the reverse of the house's exhale, whose band falls (v108's EXHALE).
    Built from `_sweep`, never `_burst` (the toolkit's own note: every `_burst`
    is a tick). THE TOOLKIT'S GEOMETRY, measured in v108 and restated here: a
    `_sweep` is a tent in dB, up 80 dB over its attack (at most 0.6 x 0.58 s)
    and down 80 over the rest, so a breath's audible climb is at most ~150 ms
    whatever it is built from, and a 0.4 s breath that is ONE hump has its top
    in the first half (a SWELL with the longest attack and a DRAW that peaks on
    it and decays over the rest of its own 0.58 s -- v108's WHOOMPH geometry).
    An inhale's top would sit LATE; the one way to put it there in this toolkit
    is a train of staggered sweeps (GRAIN), whose copies of the one noise
    buffer may comb. Both are candidates; "drawn in" is read on the band, and
    the later top breaks a tie.
  * "LOW": the power CENTROID 150-1000 Hz on every draw -- an open throat, not
    the teeth -- and still heard on a phone (HEARD >= +6 dB over its whole
    audible span, round 2 of v108).
  * "THE DRIP" (the bleed's, made here): one struck sine at the note, chirping
    UP by R over its decay D, `_tone(t, {freq: f, to: f*R, dur: D})` -- a drop
    into a pool rings up, not down. Its REVERSE, the drain: the same chirp run
    backwards -- R*f falling to f -- and the drip's own level curve (the
    `_tone`'s, g -> 0.0001 over D) run upwards, from 40 dB under its top (the
    audible part of the drip, and a margin: AUDIBLE's floor is 34 dB), ending
    where the drip began. A held or rising note does not exist in this toolkit
    (CLAUDE.md 4.5), so it is RE-STRUCK at every cycle of the falling chirp, in
    phase (Zenith's glide: the strikes sit on the chirp's own whole cycles, each
    strike continues the chirp over its own decay, and `.frequency.value = f`
    is set on every strike -- v97's toolkit finding). Each strike falls 80 dB
    per Ds = 20 ms to the toolkit's floor and is stopped there, its gain scaled
    by (1 - q) so the overlapping strikes sum to the curve. The end is the last
    strike's own fall (-34 dB in 8.5 ms): the drip's instant attack, reversed.
  * "PITCHED BY THE FOE'S STACK COUNT": the note steps UP with the count (the
    batch's reading: Bindweed's bite, Coldiron's anvil, Ironhail's thud), one
    degree of A minor pentatonic a stack -- count 1 on the score's A, then C,
    D, E (counts 1-4; the foe's ceiling is 4). The note is the one the drip
    lands on: where the reverse ends, loudest.
  * "QUIET": at most 9 dB under the blow (Canopy's and Zenith's "quiet" closes
    sat 9 dB under their casts; this one sits under a fight, so under the
    blow), and at least 2x the wall tick (v108's miss floor). Level-matched at
    the centre of that window.
  * "THE DRAIN" plays once per whole hp drained (see THE TWO EVENTS).

THE ROUNDS. The rules were written before the first table. Round 1 (candidates
1-5 of each voice) exited 1; so did round 2. Every candidate stays in the
table; each round changed what is named here, for the reason given, and no
threshold moved:
  * ROUND 2 -- THE DRAIN'S ARITHMETIC WAS WRONG, and the rule caught it: every
    reverse read ENV-CORR5 0.19-0.24 against its own LITERAL while FORWARD, the
    control, read 0.68. The first cut assumed `_tone` falls 80 dB over its
    `dur`. It ramps to an ABSOLUTE 0.0001 -- so a strike's slope is set by its
    own gain, and a quiet strike barely falls -- and then HOLDS 0.0001 for 20 ms
    before it stops, so a strike every cycle leaves ~20 residues sounding: a
    pedestal under the swell and a 20 ms tail after it. Round 2 builds the
    swell as the forward `_tone`'s own curve (g -> 0.0001 over D) run
    backwards, gives each strike a `dur` of exactly its own fall to the floor
    at 80 dB per Ds, and stops it there (`o.stop`, as Daybreak's hand-off stops
    the strikes it replaces). LITERAL is cut on the same curve.
  * ROUND 2 -- THE CAST: no candidate passed. SIP and TEETH, the low breaths,
    read 0.81-0.82 against Redflail's cast (the bloodsworn mill: 69% of its
    power under 120 Hz) and 0.80 against Starwarden's; THROAT, the band-passed
    one, 0.96 against the bowstring; GRAIN and GRAIN-T were TONAL 18-19 dB --
    six copies of the one noise buffer 40 ms apart comb. Round 2 added five:
    SIP a third up (OPEN, OPEN-T) and a sixth up (AIRY), a resonant throat
    (VOWEL, q 2), and GRAIN spaced irregularly and a third up (GRAIN-J).
  * ROUND 2 -- THE EXHALE CONTROL WAS MIS-BUILT: it swapped each segment's own
    ends but left the higher band LAST, so its breath still brightened
    (DRAWN-IN +2408 c) and it failed on register alone. It is now TEETH's band
    trajectory mirrored, which is what a breath let out is (-1842 c).
  * ROUND 3 -- ENV-CORR5 WAS MISALIGNED, not the drain: with round 2's
    arithmetic the reverse is the literal's shape to the millisecond, 12 ms
    late. The chain's DynamicsCompressor delays every render ~6 ms, so a
    reversal cut from t = 1.0 put that silence at the literal's END. LITERAL
    is now cut from the forward render's own onset, and ENV-CORR5 aligns each
    envelope at its own onset (Zenith's ENV-CORR does).
  * ROUND 3 -- THE WHISTLE CONTROL WAS MIS-BUILT, and it hid the air clause:
    round 2's WHISTLE (SIP at q 14) came back wrong on its LEVEL only, its
    TONAL 2.2 dB. A Web Audio LOWPASS's Q is a resonance in dB, not a
    bandwidth: q 14 on SIP's lowpass sweeps was a 14 dB bump (and VOWEL's q 2 a
    2 dB one), not a note. WHISTLE is now a whistle -- SIP's bands as a
    bandpass at q 14 -- and the air clause also reads TONAL-50, the sharpest
    peak in any 50 ms window (a swept note smears across a whole span's
    spectrum), against the same 10 dB.
  * ROUND 3 -- THE CAST: OPEN read 0.80 against Starwarden's cast and AIRY
    0.83 against the bowstring. Round 3 adds the band between (MID, a tritone
    up) and the drawn breath's own hiss -- air through the teeth, 3-4.5 kHz,
    where neither of them sounds -- on SIP, OPEN and MID (SIP-H, HUSH, MID-H).
  * RUN 4 (the first full run) DID NOT FINISH: the page's renderer crashed
    part way through the cast table (`Target crashed`, on a render round 3
    had made; the batch's other builds run browsers on this PC). Nothing
    measured changed; the lab now re-opens a crashed page and repeats the call
    (`Reopen`), printing each time it does.

THE PICKS, on Chromium 151.0.7922.34, sc-widowmaker-b1075 a9977a757d5772b7
(run 5, the full run, exit 0; every candidate's line is the same as round
3's, which is its reproduction; the renderer did not crash). The rows'
comments carry the same numbers.

  cast   11 MID    g 0.5386, s 0.994: two lowpass `_sweep`s, 210 -> 560 Hz
                   and, 318 ms in, 420 -> 1120 Hz. Audible 400 ms, drawn in
                   +1011 cents, breath-rise 80 ms, no dip, no regrowth,
                   centroid 301-366 Hz on every draw, TONAL 2.4 / TONAL-50
                   3.3 dB, heard +22.8 dB over the score; its loudest 50 ms
                   -3.5 to -1.4 dB re the blow's quietest draw. Register at
                   most 0.79 (Starwarden's cast; the bowstring 0.79, Redflail's
                   0.75). Two candidates pass: MID and SIP-H (0.80 against
                   Redflail's cast). They tie on register (the same 0.05 step)
                   and MID's top sits later (TOP-PLACE 0.36 against 0.35 --
                   the tiebreak at its own resolution: the two are close, and
                   SIP-H is the same breath a tritone down with the drawn hiss
                   on it, if Rick wants it). Every other candidate is out on
                   one register or more over 0.80 (the school's low mill, the
                   type's Starwarden, the bowstring), GRAIN and GRAIN-T also on
                   their comb (TONAL 18-19 dB).
  drain  5 TRI     g 0.09989: a triangle sliding down a fifth onto the note as
                   it swells, 122 strikes at count 4. Lands 906 / 1081 / 1214 /
                   1358 Hz at counts 1-4 (declared 880 / 1047 / 1175 / 1319;
                   within 57 cents, each count >= 193 cents over the last);
                   falls 284-290 cents; audible 75-80 ms; LAST5 0.86, LATE
                   0.78; ENV-CORR5 0.95 against its own drip's samples
                   reversed; TONAL 23.8 dB; its loudest 50 ms -11.3 to -10.7
                   dB re the blow, +8.3 dB or more over the wall tick; heard
                   +17.8 dB or more over the score; register at most 0.51
                   (rune-crack). DROP, SLURP and LOW pass too: DROP and SLURP
                   tie with TRI on register (0.49-0.51) and have more strikes
                   (126, 127); LOW is 0.55 against the cast. WIDE is out
                   (TONAL 12.2: an octave's slide smears the note).

  Every control comes back wrong. One at the line: WHISTLE (narrow noise at
  q 14) reads TONAL-50 10.02 dB against the air clause's 10 -- it is also
  out on its level and its length, and the clause's margin is shown by the
  slice's sawtooth tones, 27.2 dB, against the pick's 3.3.

  IN FIGHTS (148 fights, seeds 106601-106602, her both sides): 558 casts,
  558 inhales; 13120 hp drained, 13040 whole-hp crossings, 13040 drips; a
  window's median 23 drips, one every 167 ms at the cap (the closest 158
  ms), 410 of them inside a cast's first 0.4 s (they sound under the
  inhale). THE COUNT IS 2 OR 4, NEVER 1 OR 3: the blade applies hemorrhage two
  at a time (probe [5]'s onHit +2) and the foe's ceiling is 4, so a fight
  hears two notes of the four, C6 (count 2, 20%) and E6 (count 4, 80%). In a
  real window (Axiom, seed 106601, 35 drips) the median drip stands +21.7 dB
  over the fight in its note's third-octave and the inhale +15.5 dB in its
  400 Hz band.

  THE COST, FLAGGED (printed, not gated -- no rule was written for it): a
  drip is 122 synth calls at count 4, 4.7 ms of main thread a call (3.0 ms
  at count 1; the cast and the blow 0.1 ms). Daybreak's handoff step, on the
  chain, is 82 strikes and ~1.4 ms a call. About 10,700 synth calls a fight
  go to drips, against the bed's ~1,700 nodes a match. The shorts render
  their audio offline (render.py plays the game's voices into an
  OfflineAudioContext), so a clip does not pay it; live play in the app does,
  once every ~167 ms inside a window. If the app hitches, the lever is the
  strike stride -- and it is a round of its own: striking every second cycle
  modulates the note at half its pitch, a subharmonic the LAND gate may not
  see.

  THE BATCH'S OTHER NEW VOICES, FLAGGED (`--peer-rows`: printed, not gated --
  neither relic is on the stage-5 link, so the rule could not list them).
  Coldiron's anvil (Coldiron is a twinblade; its won bind rings a triangle a
  semitone a stack up from A5) shares the drip's octave and key: register
  0.88 here (the drip at count 2 against the anvil at 3), 0.87-0.92 in
  scratch where the two land on one note. Of the drain's candidates only LOW,
  an octave down, stays clear of it (0.31 at most, measured in scratch over
  every candidate and count) and it passes this rule: the one swap if Rick
  wants the two apart. Ironhail's cast (v108's bellows huff) is the inhale's
  own two-sweep geometry run the other way: register 0.93. What tells them
  apart is the direction -- the inhale's band rises +1011 cents, the huff's
  falls.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (the wet slice's three lines replaced by the two arms) is
    applied to `Sfx.prototype.play`'s own source and rendered: the cast and the
    drain at counts -1, 0, 1..4, 7 and a missing `n`, on two noise draws, must
    reproduce their candidates to TOL; every other voice through the patched
    play (the hit at five weights with and without a crit, spark x3, wall,
    death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork,
    scour x4, and every relic's cast and every sub-voice the ult arm names)
    must be unchanged; `ult/widowmaker` must NOT be the wet slice any more;
  * the tickStatus row is applied to `Match.prototype.tickStatus`'s own source
    and run on real fights beside the unpatched one: every fight identical
    (over, clock, both hp, shields, positions, velocities, charges, both
    hemorrhage counts, winner, her whole drainTally and ultDrain) and every
    other voice call identical in order, kind and opts; one drain voice on
    every step her running total crosses a whole hp and on no other, each
    inside tickStatus, inside her window, carrying the bleeding foe's count;
    one cast voice per cast; the unpatched runs play no drain voice. The same
    row plus ONE sim write (her x nudged 1e-9 on a drip) must come back NOT
    identical, or "identical" proves nothing. (The Sfx row cannot reach the
    simulation at all: `play` returns on its first line with no audio context,
    which is every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a temp
    folder, never the repo), loaded in a fresh browser after the first is
    closed: the page loads clean, its own SFX.play renders the arms to the
    lab's text, every other voice to the original page's, and its fights are
    identical to the original page's, with one drain voice per whole hp
    drained.
  * WITH OTHER RELICS' ROWS (`--peer-rows`, optional): each peer's Sfx rows and
    these applied to play()'s source in both orders render every arm of both
    identically.
  Both anchors must occur exactly once in the game file, and both rows are
  `replace` rows that re-emit their anchor's text exactly once, except the wet
  slice's three lines, which are the voice being retired.

Writes wavs to 05-reference/v106/widowmaker-*.wav at RAW level (gitignored).
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
# The shared definitions, imported unchanged so every number here means what
# it means in v98's, v99's and v101's labs (all three on the chain). Their
# module bodies only check their own candidate sources.
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, low_share  # noqa: E402
from bindweed_voice_lab import tonal  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "widowmaker"
BLADE = 10.75                             # Widowmaker's dmg (the blade holds at 10.75, v106)
CAP = 4                                   # STATUS.hemorrhage.maxStacks (checked on the page)
COUNTS = list(range(1, CAP + 1))
CAST_AUD = 400.0                          # "0.4s": the time scale is solved to this
DRIP_UNDER_DB = 9.0                       # "quiet": at most this far under the blow
DRAIN_REF_N = 2                           # the count the drain is level-matched at
SWELL_DB = 40.0                           # the reverse starts this far under its top
PENT = [0, 3, 5, 7]                       # A minor pentatonic from A: A C D E, counts 1-4
A5 = 880.0
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)

# =============================================================== THE CAST ===
# "a low inhale, 0.4s". Segments: (onset s, f0, f1, q, level, dur s, atk s,
# filter), in time units the calibration scales so the whole is AUDIBLE 400 ms.
SWELL_LP = (0.00, 150, 400, 0.7, 1.0, 0.58, 0.34, "lowpass")
DRAW_LP = (0.32, 300, 800, 0.7, 1.0, 0.58, 0.02, "lowpass")
SWELL_BP = (0.00, 180, 420, 0.9, 1.0, 0.58, 0.34, "bandpass")
DRAW_BP = (0.32, 320, 900, 0.9, 1.0, 0.58, 0.02, "bandpass")
TEETH = (0.32, 1600, 2800, 2.0, 0.25, 0.58, 0.02, "bandpass")
HISS = (0.32, 3000, 4500, 1.0, 0.15, 0.58, 0.02, "bandpass")          # round 3


def _grains(k=6, gap=0.04, lo=150.0, hi=800.0, g0=0.3, jit=0.0):
    """GRAIN: k lowpass sweeps `gap` apart, each the longest attack `_sweep`
    allows, their cutoffs climbing lo -> hi across the train and their levels
    g0 -> 1: the top on the LAST, the late top an inhale has. `jit` (round 2):
    each gap x (1 + jit sin 2.4i), no random number -- irregular spacing
    against the comb that copies of the one noise buffer make."""
    out = []; on = 0.0
    for i in range(k):
        f0 = round(lo * (hi / lo) ** (i / k)); f1 = round(lo * (hi / lo) ** ((i + 1) / k))
        lv = round(g0 ** ((k - 1 - i) / (k - 1)), 3)
        out.append((round(on, 3), f0, f1, 0.7, lv, 0.58, 0.34, "lowpass"))
        on += gap * (1 + jit * math.sin(2.4 * i))
    return out


def _x(seg, k):
    """A segment with its band scaled by k."""
    o, f0, f1, q, lv, d, a, ty = seg
    return (o, round(f0 * k), round(f1 * k), q, lv, d, a, ty)


GRAIN = _grains()
GRAIN_TEETH = (GRAIN[-1][0], 1600, 2800, 2.0, 0.25, 0.58, 0.34, "bandpass")
CAST_CANDIDATES = [
    ("1 SIP", dict(segs=[SWELL_LP, DRAW_LP]),
     "a low breath drawn through an open throat: a swell (lowpass 150 -> 400 Hz) and the draw on its top "
     "(lowpass 300 -> 800 Hz), both bands rising"),
    ("2 THROAT", dict(segs=[SWELL_BP, DRAW_BP]),
     "SIP in two bandpass bands (q 0.9): 180 -> 420 Hz and 320 -> 900 Hz"),
    ("3 TEETH", dict(segs=[SWELL_LP, DRAW_LP, TEETH]),
     "SIP with the air past the teeth on the draw: a thin band rising 1600 -> 2800 Hz (q 2) at 0.25"),
    ("4 GRAIN", dict(segs=GRAIN),
     "six lowpass sweeps 40 ms apart, cutoffs climbing 150 -> 800 Hz, levels 0.3 -> 1: the top on the last"),
    ("5 GRAIN-T", dict(segs=GRAIN + [GRAIN_TEETH]),
     "GRAIN with the teeth band (1600 -> 2800 Hz, q 2, 0.25) on its last sweep"),
    # ROUND 2 (see THE ROUNDS): between the school's low casts (SIP 0.81 against
    # Redflail's mill) and the bowstring's band (THROAT 0.96): SIP's bands raised,
    # a resonant throat, and GRAIN spaced irregularly against its comb.
    ("6 OPEN", dict(segs=[_x(SWELL_LP, 1.25), _x(DRAW_LP, 1.25)]),
     "round 2: SIP a major third up: lowpass 188 -> 500 Hz and 375 -> 1000 Hz"),
    ("7 OPEN-T", dict(segs=[_x(SWELL_LP, 1.25), _x(DRAW_LP, 1.25), TEETH]),
     "round 2: OPEN with the teeth band on the draw (1600 -> 2800 Hz, q 2, 0.25)"),
    ("8 AIRY", dict(segs=[_x(SWELL_LP, 1.6), _x(DRAW_LP, 1.6)]),
     "round 2: SIP a minor sixth up: lowpass 240 -> 640 Hz and 480 -> 1280 Hz"),
    ("9 VOWEL", dict(segs=[SWELL_LP, DRAW_LP], q=2.0),
     "round 2: SIP with its lowpass Q at 2 -- a 2 dB resonance at the cutoff (a lowpass's Q is in dB in Web "
     "Audio): the throat's formant climbing with the breath"),
    ("10 GRAIN-J", dict(segs=_grains(lo=188.0, hi=1000.0, jit=0.35)),
     "round 2: GRAIN a major third up, its gaps 40 ms x (1 + 0.35 sin 2.4i): irregular, against the comb"),
    # ROUND 3: OPEN read 0.80 against Starwarden's cast and AIRY 0.83 against the
    # bowstring: the band between them, and the drawn breath's own hiss -- air
    # through the teeth, high and thin, where neither of them sounds.
    ("11 MID", dict(segs=[_x(SWELL_LP, 1.4), _x(DRAW_LP, 1.4)]),
     "round 3: SIP a tritone up: lowpass 210 -> 560 Hz and 420 -> 1120 Hz"),
    ("12 HUSH", dict(segs=[_x(SWELL_LP, 1.25), _x(DRAW_LP, 1.25), HISS]),
     "round 3: OPEN with the drawn breath's hiss on the draw: a band rising 3000 -> 4500 Hz (q 1) at 0.15"),
    ("13 MID-H", dict(segs=[_x(SWELL_LP, 1.4), _x(DRAW_LP, 1.4), HISS]),
     "round 3: MID with the hiss"),
    ("14 SIP-H", dict(segs=[SWELL_LP, DRAW_LP, HISS]),
     "round 3: SIP with the hiss"),
]
CAST_CONTROLS = [
    # ROUND 2: round 1's EXHALE swapped each segment's own ends and left the
    # higher band LAST, so its breath still brightened (+2408 c) -- it did not run
    # the breath down. Now the band trajectory is mirrored: the swell carries the
    # draw's band falling, the draw the swell's, the teeth ride the swell falling.
    ("0 EXHALE", dict(segs=[(0.00, DRAW_LP[2], DRAW_LP[1]) + SWELL_LP[3:],
                            (0.32, SWELL_LP[2], SWELL_LP[1]) + DRAW_LP[3:],
                            (0.00, TEETH[2], TEETH[1], TEETH[3], TEETH[4], 0.58, 0.34, TEETH[7])]),
     "TEETH's breath run DOWN: the swell falling 800 -> 300 Hz, the draw 400 -> 150, the teeth 2800 -> 1600 on "
     "the swell -- a breath let out"),
    ("0 TICK", dict(segs=[SWELL_LP, DRAW_LP], burst=True),
     "SIP's bands as fixed-filter `_burst`s (instant attack): a strike, not a breath"),
    # ROUND 3: round 2's WHISTLE was SIP at q 14 -- and a Web Audio LOWPASS's Q
    # is a resonance in dB, not a bandwidth, so it was a 14 dB bump, not a note.
    # A whistle is a narrow band: SIP's two bands as a bandpass at q 14.
    ("0 WHISTLE", dict(segs=[(o, f0, f1, 14.0, k, d, a, "bandpass") for (o, f0, f1, q, k, d, a, ty) in [SWELL_LP, DRAW_LP]]),
     "SIP's bands as a bandpass at q 14: a note gliding, not air"),
    ("0 HISS", dict(segs=[SWELL_LP, DRAW_LP], fx=8.0), "SIP three octaves up (1.2 -> 6.4 kHz): not low"),
    ("0 RUMBLE", dict(segs=[SWELL_LP, DRAW_LP], fx=1 / 3), "SIP an octave and a half down (50 -> 267 Hz): a rumble"),
]


def cast_what(sp):
    """The picked cast in words, for its arm's comment (from its own segments)."""
    segs = sp["segs"]
    if len(segs) >= 6:
        g_ = [x for x in segs if x[7] == "lowpass"]
        t_ = f"Six lowpassed sweeps, {', '.join(f'{1000 * x[0]:.0f}' for x in g_)} ms in, their cutoffs climbing "              f"{g_[0][1]} -> {g_[-1][2]} Hz and their levels {g_[0][4]:g} -> 1, so the breath fills to its top on "              f"the last"
    else:
        s0, s1 = segs[0], segs[1]
        kind = "lowpassed" if s0[7] == "lowpass" else f"bandpassed (q {s0[3]:g})"
        t_ = (f"A low breath drawn in: a swell of {kind} air (its {'cutoff' if s0[7] == 'lowpass' else 'band'} "
              f"{s0[1]} -> {s0[2]} Hz, the longest attack a `_sweep` allows) and, on its top, the draw ({s1[1]} -> "
              f"{s1[2]} Hz), decaying over the rest of its 0.58 s")
        if sp.get("q"):
            t_ += f", both through a resonant filter (q {sp['q']:g})"
    for x in segs[2:] if len(segs) < 6 else segs[6:]:
        if x[1:3] == TEETH[1:3]:
            t_ += (f" -- with the air past the teeth on {'the last' if len(segs) >= 6 else 'the draw'}, a thin band "
                   f"1600 -> 2800 Hz (q 2) at 0.25")
        elif x[1:3] == HISS[1:3]:
            t_ += " -- with the drawn breath's hiss on the draw, a band 3000 -> 4500 Hz (q 1) at 0.15"
    return t_ + "."


def cast_body(sp, g, s, ind=10):
    """The cast arm's body: every segment's onset, dur and atk scaled by `s`."""
    L = [f"const g = {fmt(g)};"]
    for (o, f0, f1, q, k, d, a, ty) in sp["segs"]:
        on = round(o * s, 4); du = round(d * s, 4); at = round(a * s, 4)
        tt = "t" if on == 0 else f"t + {fmt(on)}"
        gx = "g" if k == 1 else f"g * {fmt(k)}"
        fx = sp.get("fx", 1.0); q_ = sp.get("q", q)
        if sp.get("burst"):
            fc = round(math.sqrt(f0 * f1) * fx, 1)
            L.append(f'this._burst({tt}, {{ freq: {fmt(fc)}, q: {fmt(q_)}, gain: {gx}, dur: {fmt(du)}, '
                     f'type:"{ty}" }});')
        else:
            L.append(f'this._sweep({tt}, {{ f0: {fmt(round(f0 * fx, 1))}, f1: {fmt(round(f1 * fx, 1))}, q: {fmt(q_)}, '
                     f'gain: {gx}, dur: {fmt(du)}, atk: {fmt(at)}, type:"{ty}" }});')
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE DRAIN ===
# "the bleed's own drip voice reversed and pitched by the foe's stack count,
# quiet". Every candidate is a DRIP (root, R, D, body) and its reverse.
DRAIN_CANDIDATES = [
    ("1 DROP", dict(root=A5, R=1.5, D=0.12, Ds=0.02, body="sine", click=False),
     "a drop that rings up a fifth over 0.12 s, reversed: a sine sliding down a fifth onto the note as it swells, "
     "and stopping"),
    ("2 SLURP", dict(root=A5, R=1.5, D=0.12, Ds=0.02, body="sine", click=True),
     "DROP with the drop's contact, reversed, at its end: a 6 ms 3.5 kHz tick where it stops"),
    ("3 LOW", dict(root=A5 / 2, R=1.5, D=0.12, Ds=0.02, body="sine", click=False),
     "DROP an octave down (A4 -> E5): a thicker drop, half the strikes"),
    ("4 WIDE", dict(root=A5, R=2.0, D=0.12, Ds=0.02, body="sine", click=False),
     "DROP whose drip rings up an OCTAVE: the reverse slides down an octave"),
    ("5 TRI", dict(root=A5, R=1.5, D=0.12, Ds=0.02, body="triangle", click=False),
     "DROP with a triangle body: its odd harmonics over the note"),
]
DRAIN_CONTROLS = [
    ("0 FORWARD", "DROP's drip itself, not reversed (the drip as the bleed would play it)"),
    ("0 FLAT", "DROP at count 1's note for every count"),
    ("0 LOUD", "DROP at the blow's level (its TOP at the hit @ 10.75's quietest draw)"),
    ("0 SPARK", "the house's heal voice, `spark {collect, n}` at n = the count, as it plays"),
    ("0 NOISE", "a reversed noise swell: a bandpass `_sweep` (q 3) falling 1.5 f -> f, its top at 0.6 of 80 ms"),
    ("0 RAW", "DROP without `.frequency.value = f` on its strikes, at DROP's own gain"),
]
CLICK = 'this._burst(t + D - u0, { freq: 3500, q: 1.2, gain: g * 0.3, dur: 0.006, type:"bandpass" });'
CLICK_FWD = 'this._burst(t, { freq: 3500, q: 1.2, gain: g * 0.3, dur: 0.006, type:"bandpass" });'


def note_of(sp, n):
    """The declared note of count n (clamped to 1..CAP): the note the drip lands on."""
    n = min(CAP, max(1, n))
    return sp["root"] * 2 ** (PENT[n - 1] / 12)


def drain_body(sp, g, ind=10, fixed_n=None, forward=False, raw=False, noise=False):
    """The drain arm's text (or a control's). The note is read off `p.n`,
    clamped to 1..CAP; `fixed_n` pins it (FLAT)."""
    nexpr = (f"const n = {fixed_n}" if fixed_n is not None else f"const n = clamp(Math.round(p.n || 1), 1, {CAP})")
    L = [f"{nexpr}, f = {fmt(sp['root'])} * Math.pow(2, [{', '.join(str(s) for s in PENT)}][n - 1] / 12);"]
    if noise:
        L.append(f"const g = {fmt(g)};")
        L.append('this._sweep(t, { f0: f * 1.5, f1: f, q: 3, gain: g, dur: 0.08, atk: 0.048, type:"bandpass" });')
        return "\n".join(" " * ind + l for l in L)
    if forward:
        L.append(f"const g = {fmt(g)}, D = {fmt(sp['D'])}, R = {fmt(sp['R'])};")
        L.append(f'this._tone(t, {{ freq: f, to: f * R, gain: g, dur: D, type:"{sp["body"]}" }}).frequency.value = f;')
        if sp["click"]:
            L.append(CLICK_FWD)
        return "\n".join(" " * ind + l for l in L)
    # ROUND 2 (see THE ROUNDS): `_tone` ramps to an ABSOLUTE 0.0001 and holds it
    # 20 ms, so a strike's slope is set by its own gain and every strike leaves a
    # residue. The swell is the forward `_tone`'s own curve, g -> 0.0001 over D,
    # run backwards from SWELL_DB under its top; each strike lasts exactly as long
    # as it takes to fall 80 dB per Ds to the floor, and is stopped there.
    L.append(f"const g = {fmt(g)}, D = {fmt(sp['D'])}, R = {fmt(sp['R'])}, Ds = {fmt(sp['Ds'])}, "
             f"u0 = D * (1 - {fmt(SWELL_DB / 20)} / Math.log10(g / 0.0001));")
    L.append("const fs = f * R, Lg = Math.log(1 / R);")
    L.append("for (let k = Math.ceil(fs * D * (Math.pow(R, -u0 / D) - 1) / Lg); ; k++){")
    L.append("  const u = D / Lg * Math.log(1 + k * Lg / (fs * D));")
    L.append("  if (!(u < D)) break;")
    L.append("  const fu = fs * Math.pow(R, -u / D), q = Math.pow(10, -4 / (fu * Ds));")
    L.append("  const a = g * Math.pow(0.0001 / g, 1 - u / D) * (1 - q), d = Ds * Math.log10(a / 0.0001) / 4;")
    L.append("  if (!(d > 0)) continue;")
    L.append(f"  const o = this._tone(t + u - u0, {{ freq: fu, to: fu * Math.pow(R, -d / D), gain: a, dur: d, "
             f"type:\"{sp['body']}\" }});")
    L.append("  " + ("" if raw else "o.frequency.value = fu; ") + "o.stop(t + u - u0 + d);")
    L.append("}")
    if sp["click"]:
        L.append(CLICK)
    return "\n".join(" " * ind + l for l in L)


def peer_name(pf):
    """A peer rows file's relic: `<scratch>/batch/<relic>/stage6-voice/rows_final.json` -> "Relic"."""
    p_ = pathlib.Path(pf).parent
    return (p_.parent.name if p_.name.startswith("stage") else p_.name).capitalize()


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
# The retired voice: the nova's "wet slice", the Sfx `ult` arm keyed on the relic.
SLICE_HEAD = '        } else if (w === "widowmaker"){                 // a wet slice'
SLICE_BODY = ('          this._burst(t, { freq: 3400, q: 1.6, gain: 0.34, dur: 0.20 });\n'
              '          this._tone (t, { freq: 900, to: 240, gain: 0.20, dur: 0.28, type:"sawtooth" });\n'
              '          this._tone (t + 0.10, { freq: 620, to: 180, gain: 0.14, dur: 0.34, type:"sawtooth" });')
SFX_ANCHOR = SLICE_HEAD + "\n" + SLICE_BODY
DRAIN_ANCHOR = '            me.drainTally.drained += me.hp - h0;'

DRAIN_CODE = '''            const k0 = Math.floor(me.drainTally.drained);
''' + DRAIN_ANCHOR + '''
            /* EXSANGUINATE'S DRIP (v76 §4: "the drain -- the bleed's own drip
               voice reversed and pitched by the foe's stack count, quiet"): one
               reversed drip each time the running total crosses a whole hp --
               the unit of the drain's "+n" (§4) -- pitched by the bleeding
               foe's hemorrhage stacks. `k0` is a local; the total is read, not
               written. Presentation only: SFX.play draws nothing, is a no-op
               headless, and nothing here is read back (widowmaker_voice_lab:
               fights identical). */
            if (Math.floor(me.drainTally.drained) > k0)
              SFX.play("ult", { w: "widowmaker-drain", n: f.stacks("hemorrhage") });'''

# the sim-write control: the same row with her x nudged 1e-9 on a drip
DRAIN_CODE_BAD = DRAIN_CODE.replace(
    '              SFX.play("ult", { w: "widowmaker-drain"',
    '              { me.x += 1e-9; SFX.play("ult", { w: "widowmaker-drain"', 1).replace(
    'n: f.stacks("hemorrhage") });', 'n: f.stacks("hemorrhage") }); }', 1)

_refuse(DRAIN_CODE, "sim row")
assert DRAIN_CODE.count(DRAIN_ANCHOR) == 1, "the sim row must re-emit its anchor exactly once"
assert DRAIN_CODE_BAD != DRAIN_CODE and "me.x += 1e-9" in DRAIN_CODE_BAD


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


def arms_code(C_, K_, info):
    cn, kn = (X["name"].split()[1] for X in (C_, K_))
    c_cast = _wrap([
        f'EXSANGUINATE\'S CAST, THE INHALE -- v76 §4: "cast -- a low inhale, 0.4s". {cn}, of '
        f'{info["n_cast"]}, picked on the numbers by `widowmaker_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v106). It REPLACES the nova\'s "wet slice" -- the three lines that were this arm -- '
        f'which the redesign retires with the nova (v106 §5); nothing else in the synth moved.',
        f"{info['c_what']} It is drawn IN: its band rises {info['c_in']:+.0f} cents from its first 100 ms to "
        f"its last. It swells to its top (the last 10 -> 90% in {info['c_rise']:.0f} ms), never dips on the way "
        f"up and never grows again after it; its power centres at {info['c_cen0']:.0f}-{info['c_cen1']:.0f} Hz "
        f"on every noise draw (low), and in no 50 ms of it does a peak stand more than {info['c_tonal']:.1f} dB "
        f"over its neighbours (air, not a note). Audible {info['c_aud']:.0f} ms; its loudest 50 ms {info['c_top']:+.1f} dB re "
        f"Widowmaker's blow. Register at most {info['c_reg']:.2f} against rune-crack, the bloodsworn and "
        f"twinblade casts, the tornado's woosh, the bowstring, the blow and the death voice."], 10)
    c_drain = _wrap([
        f'THE DRAIN -- "the bleed\'s own drip voice reversed and pitched by the foe\'s stack count, quiet" '
        f'(v76 §4). {kn}, of {info["n_drain"]} (`widowmaker_voice_lab.py`). The bleed has no drip voice, so '
        f'the lab made one -- a drop into a pool, a sine chirping up {info["k_R"]}x over {info["k_D"]:g} s -- and '
        f'this is its REVERSE: {info["k_what"]}. `tickStatus` plays it once per whole hp drained, with n = '
        f'the bleeding foe\'s hemorrhage stacks (1-{CAP}).',
        f"A held or rising note does not exist in this toolkit (CLAUDE.md 4.5), so the swell is re-struck at "
        f"every cycle of the falling chirp, on the chirp's own whole cycles, `.frequency.value` set on each "
        f"(v97); each strike decays over Ds and is scaled by (1 - q) so the strikes sum to the drip's own "
        f"exponential, run upwards from 40 dB under its top. It lands on {info['k_notes']} Hz at counts 1-{CAP} "
        f"(measured within {info['k_err']:.0f} cents), falling {-info['k_fall']:.0f} cents onto it; audible "
        f"{info['k_aud0']:.0f}-{info['k_aud1']:.0f} ms, its loudest 5 ms in the last "
        f"{100 * (1 - info['k_last']):.0f}% of it, ENV-CORR {info['k_corr']:.2f} with the drip's own samples "
        f"reversed; {info['k_calls']} strikes at count {CAP}. Quiet: its loudest 50 ms {info['k_db0']:+.1f} to "
        f"{info['k_db1']:+.1f} dB re the blow, {info['k_wall']:+.1f} dB or more re the wall tick; register at "
        f"most {info['k_reg']:.2f} against the blow, the wall tick, the heal (spark), the fork, the hex snap, "
        f"Zenith's tick, rune-crack and the cast. The close plays nothing (v76 §4)."], 10)
    return (f'{_arm_head(ME, "she draws breath")}\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["s"])}\n'
            f'{_arm_head(ME + "-drain", "a drop drawn back up")}\n'
            f'{c_drain}\n{drain_body(K_["sp"], K_["g"])}')


# ============================================================== THE PAGE ===
# The tickStatus row, applied to the real prototype and run beside the
# original; the survey of Exsanguinate's windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "widowmaker";
  const CAP = AC.STATUS.hemorrhage.maxStacks;
  const orig = P.tickStatus; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickStatus anchor occurs ${at} times in tickStatus()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inT = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        calls.push({ step, k: w, n: p.n === undefined ? null : p.n, fs: foe.stacks("hemorrhage"),
                     win: !!f.ultDrain, alive: f.alive, foeAlive: foe.alive, over: !!m.over, inT: !!inT,
                     keys: Object.keys(p).join(",") });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    P.tickStatus = function(g, dt){ inT++; try { return impl.call(this, g, dt); } finally { inT--; } };
    const dripSteps = {}, castSteps = {}, wins = [];
    let n = 0, lc = 0, prev = null, W = null;
    try {
      while (!m.over && n < 170 / DT){
        const T0_ = f.drainTally, k0 = T0_ ? Math.floor(T0_.drained) : 0;
        step = n; m.step(DT); n++;
        const T = f.drainTally, Z = f.ultDrain;
        if (T){
          const k1 = Math.floor(T.drained);
          if (k1 > k0) dripSteps[step] = k1 - k0;
          if (T.casts > lc){ castSteps[step] = T.casts - lc; lc = T.casts; }
        }
        if (Z && Z !== prev){ if (W && !W.end){ W.end = "recast"; W.endStep = step; }
                              W = { cast: m.t, castStep: step, end: null, endStep: null, close: null };
                              wins.push(W); }
        if (!Z && prev && W && !W.end){ W.end = (prev.t >= prev.dur) ? "clock" : "death"; W.endStep = step;
                                        W.close = m.t; }
        prev = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickStatus = orig; if (had) S.play = op; else delete S.play; }
    const T = f.drainTally || {};
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.shield, m.b.shield, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.a.vx, m.a.vy, m.b.vx, m.b.vy, m.a.charge, m.b.charge,
                                  m.a.stacks("hemorrhage"), m.b.stacks("hemorrhage"),
                                  m.winner ? m.winner.w.id : null, T, f.ultDrain]),
             calls, other: JSON.stringify(other), dripSteps, castSteps, wins, T, steps: n };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, castV = 0, drips = 0, dripV = 0, fatal = 0, inCast = 0, gapMin = 1e9, drained = 0;
  const nh = new Array(CAP + 2).fill(0), gaps = [], perWin = [], pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a drain voice"]);
    const byStep = {};
    for (const c of B.calls) (byStep[c.step] = byStep[c.step] || []).push(c);
    const keys = new Set([...Object.keys(B.dripSteps), ...Object.keys(B.castSteps), ...Object.keys(byStep)]);
    for (const k of keys){
      const cs = byStep[k] || [];
      const dv = cs.filter(c => c.k === ME + "-drain"), cv = cs.filter(c => c.k === ME);
      const nd = B.dripSteps[k] || 0, nc = B.castSteps[k] || 0;
      if (dv.length !== nd || cv.length !== nc)
        bad.push([fid, sd, "step " + k, "drip", nd, dv.length, "cast", nc, cv.length]);
      for (const c of dv){
        if (!(Number.isInteger(c.n) && c.n >= 1 && c.n <= CAP && c.n === c.fs) || c.keys !== "w,n")
          bad.push([fid, sd, "a drip's n is not the bleeding foe's count", c.n, c.fs, c.keys]);
        else nh[c.n]++;
        if (!c.inT || !c.win || !c.alive || c.over) bad.push([fid, sd, "a drip outside tickStatus / her window",
                                                                c.inT, c.win, c.alive, c.over]);
        if (!c.foeAlive) fatal++;
      }
      for (const c of cv) if (c.keys !== "w") bad.push([fid, sd, "the cast carries opts", c.keys]);
      drips += nd; dripV += dv.length; casts += nc; castV += cv.length;
    }
    const ds = Object.keys(B.dripSteps).map(Number).sort((x, y) => x - y);
    for (const W of B.wins){
      ends[W.end]++;
      const hi = W.endStep === null ? B.steps : W.endStep;
      const inW = ds.filter(s => s >= W.castStep && s <= hi);
      perWin.push(inW.length);
      inCast += inW.filter(s => s - W.castStep < 0.4 / DT).length;
      for (let i = 1; i < inW.length; i++){ gaps.push(inW[i] - inW[i - 1]); gapMin = Math.min(gapMin, inW[i] - inW[i - 1]); }
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, drips: inW.length });
    }
    drained += B.T.drained || 0;
  }
  gaps.sort((x, y) => x - y);
  const q = (v, p) => v.length ? v[Math.min(v.length - 1, Math.floor(p * v.length))] : null;
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, drips, dripV, fatal, inCast, nh,
           drained, gapMin: gapMin * DT, gapP5: q(gaps, 0.05) * DT, gapMed: q(gaps, 0.5) * DT,
           perWinMed: q(perWin.slice().sort((x, y) => x - y), 0.5), pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the row, every SFX call recorded with its match
# time and whether it is one of Exsanguinate's.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "widowmaker";
  const orig = P.tickStatus; let src = orig.toString();
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
  P.tickStatus = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickStatus = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, ME = "widowmaker";
  const CAP = AC.STATUS.hemorrhage.maxStacks;
  const res = [];
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.n === undefined ? null : p.n, foe.stacks("hemorrhage")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { if (had) S.play = op; else delete S.play; }
    const T = f.drainTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                    m.a.stacks("hemorrhage"), m.b.stacks("hemorrhage"),
                                    m.winner ? m.winner.w.id : null, f.drainTally || null]),
               casts: T.casts || 0, drips: Math.floor(T.drained || 0),
               castV: log.filter(e => e[0] === ME).length,
               dripV: log.filter(e => e[0] === ME + "-drain").length,
               badN: log.filter(e => e[0] === ME + "-drain" && (e[1] !== e[2] || e[1] < 1 || e[1] > CAP)).length,
               other: JSON.stringify(other) });
  }
  return res;
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
  for (const [k, kind, p] of [["cast", "ult", { w: "widowmaker" }], ["drain n1", "ult", { w: "widowmaker-drain", n: 1 }],
                              ["drain n4", "ult", { w: "widowmaker-drain", n: 4 }],
                              ["hit", "hit", { dmg: 10.75, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""


class Reopen:
    """The page, re-opened when its renderer crashes. Run 4 (the first full
    run) died on `Page.evaluate: Target crashed` part way through the cast
    table, on a render round 3 had already made -- this PC runs the batch's
    other builds' browsers beside this one, and the renderer is the first
    thing to go when memory runs short. Every evaluate in this lab is a pure
    function of its arguments (a render builds its own synth on a fresh
    OfflineAudioContext; the fight checks restore every prototype they patch,
    and a fresh page has the originals), so a crash re-opens the same file in a
    fresh page of the same browser and repeats the call, at most twice. Each
    one is printed and counted in the record; the numbers cannot tell."""

    def __init__(self, page, errors, path):
        self.p, self.errors, self.path, self.n = page, errors, pathlib.Path(path), 0

    def evaluate(self, js, arg=None):
        for k in range(3):
            try:
                return self.p.evaluate(js) if arg is None else self.p.evaluate(js, arg)
            except Exception as e:  # noqa: BLE001 -- only a crash is retried; the rest re-raise
                if "crashed" not in str(e).lower() or k == 2:
                    raise
                self.n += 1
                print(f"  [the page's renderer crashed ({str(e).splitlines()[0][:60]}); a fresh page on the same "
                      f"file, the call repeated]", flush=True)
                br = self.p.context.browser
                try:
                    self.p.close()
                except Exception:  # noqa: BLE001
                    pass
                pg = br.new_page(viewport={"width": 620, "height": 1000})
                pg.on("pageerror", lambda e_: self.errors.append(f"pageerror: {e_}"))
                pg.on("console", lambda m: self.errors.append(f"console.{m.type}: {m.text}")
                      if m.type == "error" else None)
                pg.goto(self.path.as_uri())
                pg.wait_for_function("window.AC && window.AC.WEAPONS && window.__fontsReady !== false",
                                     timeout=20000)
                self.p = pg


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


# -- ironhail_voice_lab's (v108), copied unchanged: that lab is not on the chain.
def breath(draws, aud_a0, aud_ms):
    """BREATH-RISE (ms), DIPS and REGROW (dB) on the draw-averaged envelopes,
    inside AUDIBLE."""
    np = _np()
    ys = [d_[int(T0 * SR):] for d_ in draws]
    n = min(len(y) for y in ys)
    P5 = np.mean([env(y[:n], 0.005, 0.001)[0] ** 2 for y in ys], axis=0)
    e5 = np.sqrt(P5)
    m5 = e5.max()
    i10 = int(np.argmax(e5 > 0.1 * m5)); i90 = int(np.argmax(e5 > 0.9 * m5))
    rise = float(i90 - i10)                          # 1 ms hop
    P25 = [env(y[:n], 0.025, 0.005) for y in ys]
    c25 = P25[0][1]
    e25 = np.sqrt(np.mean([p_[0] ** 2 for p_ in P25], axis=0))
    live = (c25 >= aud_a0 / 1000) & (c25 <= (aud_a0 + aud_ms) / 1000)
    e, c = e25[live], c25[live]
    ip = int(np.argmax(e))
    run = 0.0; dips = 0; indip = False
    for v in e[:ip + 1]:
        run = max(run, v)
        if run > e.max() * 0.05 and v < run * 10 ** (-3 / 20):
            if not indip:
                dips += 1
            indip = True
        else:
            indip = False
    after = 20 * np.log10(np.maximum(e[ip:], 1e-9))
    regrow = float(max(0.0, (after - np.minimum.accumulate(after)).max())) if len(after) else 0.0
    return rise, dips, regrow


def centroid(x):
    np = _np()
    y = x[int(T0 * SR):]
    P = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float((P * fr).sum() / P.sum())


def bed_p90(bseg, win=0.1, hop=0.05):
    np = _np()
    W = int(win * SR); H = int(hop * SR)
    B = np.array([bands(bseg[i:i + W]) for i in range(0, len(bseg) - W, H)])
    return np.percentile(B, 90, axis=0)


PHONE_HZ = 200.0                          # what a phone speaker reproduces (Culverin v96)


def heard(x, p90, win=0.1, lo=PHONE_HZ, hi=12000.0, start=T0):
    """HEARD: the loudest ratio of the voice's third-octaves (centred at or
    above `lo`) over [start, start + win] s to the score's p90 in the same
    third-octave, dB, and where."""
    y = x[int(start * SR):int(start * SR) + int(win * SR)]
    b = bands(y)
    best = max(((b[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))
    return db(best[0]), best[1]


def phone(x):
    """PHONE, Culverin's (v96): the TOP (loudest 50 ms, 5 ms hop) of the voice
    from t = 1.0 high-passed (FFT) at 200 Hz."""
    np = _np()
    y = x[int(T0 * SR):]
    Y = np.fft.rfft(y); fy = np.fft.rfftfreq(len(y), 1 / SR); Y[fy < PHONE_HZ] = 0
    r, _ = env(np.fft.irfft(Y, n=len(y)), 0.05)
    return float(r.max())
# -- end of the copy.


def tonal50(draws, a0_ms, aud_ms, lo=100.0, hi=8000.0, w=0.05, hop=0.025):
    """TONAL-50 (round 3): bindweed's TONAL on the draw-averaged spectrum of
    each 50 ms window (25 ms hop) inside AUDIBLE, the largest. A swept note
    smears across a whole span's spectrum -- round 2's WHISTLE (q 14, swept)
    read 2.2 dB over the span -- and stands in any 50 ms of it."""
    a = T0 + a0_ms / 1000; b = a + aud_ms / 1000
    best, s0 = 0.0, a
    while s0 + w <= b + 1e-9:
        best = max(best, tonal(draws, s0, s0 + w, lo, hi))
        s0 += hop
    return best


def drawn_in(draws, a0_ms, aud_ms, lo=100.0, hi=8000.0, w=0.1):
    """DRAWN-IN: cents from the draw-averaged power centroid (lo..hi) over the
    first `w` s of AUDIBLE to that over its last `w` s."""
    np = _np()
    a = T0 + a0_ms / 1000; b = a + aud_ms / 1000

    def cen(s0, s1):
        P = 0.0
        for x in draws:
            seg = x[int(s0 * SR):int(s1 * SR)]
            P = P + np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(int(s1 * SR) - int(s0 * SR), 1 / SR)
        m = (fr >= lo) & (fr <= hi)
        return float((P[m] * fr[m]).sum() / P[m].sum())
    return cents(cen(b - w, b), cen(a, a + w))


def e5(x):
    """E5: the 5 ms RMS at a 1 ms hop from T0, and its window centres (s)."""
    return env(x[int(T0 * SR):], 0.005, 0.001)


def drip_shape(x):
    """The drip's shape on E5 (see the docstring): LAST5, SMOOTH, FALL, LAND."""
    np = _np()
    e, c = e5(x)
    m = float(e.max())
    on = np.nonzero(e > 0.02 * m)[0]
    i0, i1 = int(on[0]), int(on[-1])
    it = int(np.argmax(e))
    run = 0.0; dips = 0; indip = False
    for v in e[i0:it + 1]:
        run = max(run, v)
        if run > 0.05 * m and v < run * 10 ** (-3 / 20):
            if not indip:
                dips += 1
            indip = True
        else:
            indip = False
    a0, a1 = float(c[i0]), float(c[i1])
    span = a1 - a0
    p1 = pitch(x, T0 + a0, T0 + a0 + span / 3, lo=150, hi=9000)
    p3 = pitch(x, T0 + a1 - span / 3, T0 + a1, lo=150, hi=9000)
    land = pitch(x, T0 + float(c[it]) - 0.015, T0 + float(c[it]), lo=150, hi=9000)
    return dict(last=(it - i0) / max(i1 - i0, 1), dips=dips, fall=cents(p3, p1), land=land,
                a0_ms=a0 * 1000, a1_ms=a1 * 1000, top5_ms=float(c[it]) * 1000)


def env_corr5(x, y):
    """ENV-CORR5 (see the docstring): each E5 in dB floored 40 dB under its own
    top, ALIGNED AT ITS OWN ONSET (its first window above that floor -- round 2:
    the chain's compressor delays every render ~6 ms, see literal()), over the
    longer live span."""
    np = _np()

    def cur(z):
        e, _ = e5(z)
        d = 20 * np.log10(np.maximum(e, 1e-9))
        d = np.maximum(d, d.max() - 40)
        live = np.nonzero(d > d.max() - 40 + 1e-9)[0]
        return d[int(live[0]):int(live[-1]) + 1], d.max() - 40
    a, fa = cur(x); b, fb = cur(y)
    n = max(len(a), len(b))
    a = np.concatenate([a, np.full(n - len(a), fa)]); b = np.concatenate([b, np.full(n - len(b), fb)])
    return float(np.corrcoef(a, b)[0, 1])


def literal(fwd, sp, g):
    """LITERAL: the forward drip's first (D - u0) s -- down to SWELL_DB under
    its onset on its own curve, g -> 0.0001 over D -- its samples reversed.
    ROUND 2: taken from the render's own ONSET, not from t = 1.0: the chain's
    DynamicsCompressor delays everything ~6 ms, and a reversal taken from 1.0
    put that silence at the literal's end and moved it ~12 ms early (round
    2's first run read ENV-CORR5 0.27 on the right shape)."""
    np = _np()
    Lr = int(round(sp["D"] * (SWELL_DB / 20) / math.log10(g / 0.0001) * SR))
    i0 = int(T0 * SR)
    y = fwd[i0:]
    on = int(np.nonzero(np.abs(y) > np.abs(y).max() * 1e-3)[0][0])
    out = np.zeros_like(fwd)
    out[i0 + on:i0 + on + Lr] = y[on:on + Lr][::-1]
    return out


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v76 §4 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'an inhale' (a breath drawn IN): air, TONAL <= 10 dB over its audible span "
    "and (round 3) TONAL-50 <= 10 dB in every 50 ms of it; one breath, no DIP on "
    "the way up and no REGROW >= 2 dB after its top; it swells, BREATH-RISE >= 40 ms and the loudest 50 ms "
    "centred >= 80 ms in; DRAWN IN, its band RISES: DRAWN-IN >= +300 cents; 'low': the power CENTROID "
    "150-1000 Hz on every draw, and heard on a phone: HEARD (its loudest third-octave at or above 200 Hz, "
    "over its whole audible span) >= +6 dB over the score's p90. Register against rune-crack, the school's "
    "casts and the type's (read off the page), the tornado's woosh, the bowstring, the hit @ 10.75 and the "
    "death voice each <= 0.80. Level: TOP between 0.5x the hit @ 10.75's loudest 50 ms on its LOUDEST draw "
    "and 1.0x on its QUIETEST, on every draw (heard like a blow, never over one). Tiebreak: the most "
    "distinct register (to 0.05), then the LATER top (an inhale fills to its end: TOP-PLACE, to 0.1), then "
    "the fewest calls.")

DRAIN_RULE = (
    "'a drip': TONAL >= 15 dB over 300 Hz-8 kHz across its audible span (a pitched drop, not air) and "
    "AUDIBLE 25-120 ms at every count (a drop, gone before the next at the cap's 6 a second); 'reversed': "
    "its loudest 5 ms in the last 30% of its audible span (LAST5 >= 0.70) and LATE >= 0.55 at every count, "
    "its pitch FALLING >= 100 cents from the first third of its audible span to the last (the drip's rising "
    "chirp, run backwards) at every count, ENV-CORR5 >= 0.85 against LITERAL (its own drip's samples "
    "reversed) at count 2, and SMOOTH -- no drop of 3 dB under E5's running top on the way up, at every "
    "count (a swell, not a flutter); 'pitched by the foe's stack count': at counts 1-4 the note it lands on "
    "(LAND) within 100 cents of its declared note, and rising >= 150 cents with every count; 'quiet': its "
    "loudest 50 ms at every count on every draw at most 9 dB under the hit @ 10.75's QUIETEST draw and at "
    "least 2x the wall tick's LOUDEST; still heard: HEARD (at or above 200 Hz) >= +6 dB over the score's p90 "
    "at every count, and PHONE >= the bowstring's (loudest draw) at every count on every draw. Register "
    "(count 2) against the hit @ 10.75, the wall tick, the heal (spark collect n 2), the fork, the hex snap, "
    "Zenith's tick (n 2), rune-crack and the picked cast each <= 0.80. Tiebreak: the most distinct register "
    "(to 0.05), then the fewest synth calls at count 4, then the order listed.")

REAL_RULE = (
    "IN A REAL WINDOW (a check on the picks, not a rule a candidate is picked on): the fight's own sounds "
    "and the score with and without the two voices; the cast >= +6 dB over the rest in its loudest "
    "third-octave at or above 200 Hz over 0.4 s; the MEDIAN drip >= +3 dB over the rest in its landing "
    "note's third-octave over its own span (a quiet trickle under a fight is heard as a stream), every drip "
    "printed with what shares its span.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["tonal"] > 10: why.append(f"tonal {M['tonal']:.1f} dB > 10 (a note)")
    if M["tonal50"] > 10: why.append(f"tonal-50 {M['tonal50']:.1f} dB > 10 (a note in some 50 ms)")
    if M["dips"]: why.append(f"{M['dips']} dip(s) on the way up (not one breath)")
    if M["regrow"] >= 2: why.append(f"regrows {M['regrow']:.1f} dB after its top (not one breath)")
    if M["brise"] < 40: why.append(f"breath-rise {M['brise']:.0f} ms < 40 (a strike)")
    if M["top_at"] * 1000 < 80: why.append(f"loudest 50 ms at {M['top_at'] * 1000:.0f} ms (< 80)")
    if M["din"] < 300: why.append(f"drawn-in {M['din']:+.0f} cents < +300 (not drawn in)")
    if M["cen_lo"] < 150 or M["cen_hi"] > 1000:
        why.append(f"centroid {M['cen_lo']:.0f}-{M['cen_hi']:.0f} Hz, not 150-1000 (not low)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score (>= 200 Hz)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (quietest draw)")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (loudest draw)")
    return why


def drain_why(M, lev):
    why = []
    if M["tonal"] < 15: why.append(f"tonal {M['tonal']:.1f} dB < 15 (not a pitched drop)")
    if M["aud_lo"] < 25 or M["aud_hi"] > 120: why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 25-120")
    if M["last_min"] < 0.70: why.append(f"loudest 5 ms at {M['last_min']:.2f} of its span (< 0.70: not reversed)")
    if M["late_min"] < 0.55: why.append(f"LATE {M['late_min']:.2f} < 0.55 (not reversed)")
    if M["fall_max"] > -100: why.append(f"pitch moves {M['fall_max']:+.0f} cents (does not fall >= 100)")
    if M["corr"] < 0.85: why.append(f"ENV-CORR5 {M['corr']:.2f} < 0.85 against the drip reversed")
    if M["dips"]: why.append(f"{M['dips']} dip(s) on the way up (a flutter, not a swell)")
    if M["perr"] > 100: why.append(f"a count lands {M['perr']:.0f} cents off its note")
    if M["minstep"] < 150: why.append(f"the smallest step between counts is {M['minstep']:.0f} cents (< 150)")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (under 2x the wall)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    if M["phone_lo"] < lev["phone"]: why.append(f"phone {M['phone_lo']:.5f} < the bowstring's {lev['phone']:.5f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Widowmaker's stage 5 (the drain)")
    ap.add_argument("--out", default="../05-reference/v106")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=106601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "drain": DRAIN_RULE, "real": REAL_RULE}}
    for nm, anc in (("Sfx wet slice", SFX_ANCHOR), ("tickStatus drain", DRAIN_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if '"widowmaker-drain"' in html:
        raise SystemExit(f"{gp.name} already carries Exsanguinate's drain voice -- run on the stage-5 link")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nEXSANGUINATE -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")
    sizes = {}

    def wav(name, x):
        sizes[name] = write_wav(out / name, x)

    e2e_ref = {}
    with game(game_path=gp) as (page_, errors):
        page = Reopen(page_, errors, gp)
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        info0 = page.evaluate("""() => {
          const s = Object.getPrototypeOf(AC.SFX).play.toString();
          const arms = [...new Set([...s.matchAll(/w === "([a-z-]+)"/g)].map(m => m[1]))];
          const kinds = [...new Set([...s.matchAll(/kind === "([a-z-]+)"/g)].map(m => m[1]))];
          const me = AC.WEAPONS.find(w => w.id === "widowmaker");
          const ts = AC.Match.prototype.tickStatus.toString();
          return { arms, kinds, cap: AC.STATUS.hemorrhage.maxStacks, dmg: me.dmg, u: me.ult,
                   tsPlays: (ts.match(/SFX\\.play/g) || []).length,
                   bleedArms: arms.filter(a => /bleed|hemo|drip|blood(?!mirror)/.test(a)),
                   W: AC.WEAPONS.map(w => [w.id, w.aff, w.shape]) };
        }""")
        if info0["cap"] != CAP:
            raise SystemExit(f"STATUS.hemorrhage.maxStacks is {info0['cap']}, not {CAP}")
        u0 = info0["u"]
        if abs(info0["dmg"] - BLADE) > 1e-9 or u0.get("kind") != "drain" or u0.get("dur") != 8 or u0.get("charge") != 14:
            raise SystemExit(f"Widowmaker on this page is not stage 5's: dmg {info0['dmg']}, ult {u0}")
        print(f"  Widowmaker: blade {info0['dmg']}, ult {u0['name']} kind {u0['kind']} dur {u0['dur']} charge "
              f"{u0['charge']}; hemorrhage cap {CAP}")
        print(f"  THE BLEED'S OWN VOICE: tickStatus plays {info0['tsPlays']} SFX call(s); arms named for a bleed "
              f"or a drip: {info0['bleedArms'] or 'none'}  -- so the lab MAKES the drip (see the docstring)")
        rec["bleed_voice"] = dict(tickStatus_plays=info0["tsPlays"], arms=info0["bleedArms"])
        if info0["tsPlays"] or info0["bleedArms"]:
            raise SystemExit("the bleed has a voice on this page -- §4 says to reverse it; this lab made its own")
        arms_now = set(info0["arms"])
        SCHOOL = tuple(w for w, aff, sh in info0["W"] if aff == "bloodsworn" and w != ME and w in arms_now)
        TYPE = tuple(w for w, aff, sh in info0["W"] if sh == "twinblade" and w != ME and w in arms_now)
        FALL = tuple(w for w, aff, sh in info0["W"] if w not in arms_now)
        print(f"  the school's casts (bloodsworn, with an arm): {', '.join(SCHOOL) or '-'};  "
              f"the type's (twinblade): {', '.join(TYPE) or '-'}")
        print(f"  THE SYNTH'S KINDS ({len(info0['kinds'])}): {', '.join(info0['kinds'])}")
        rec.update(school=SCHOOL, type=TYPE, kinds=info0["kinds"])

        def R(evs, secs=3.0, seed=None, rows=None):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            new = any(e[0] == "body" or (e[0] == "arm" and e[2] == "ult" and str(e[3].get("w", "")).startswith(ME))
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
                ("hit@10.75", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("wall", ["play", T0, "wall", {}]),
                ("death", ["play", T0, "death", {}]),
                ("loose", ["play", T0, "loose", {}]),
                ("woosh", ["play", T0, "scour-woosh", {"n": 0}]),
                ("spark", ["play", T0, "spark", {"collect": True, "n": DRAIN_REF_N}]),
                ("fork", ["play", T0, "fork", {}]),
                ("hex-snap", ["play", T0, "hex-snap", {}]),
                ("zenith-tick", ["play", T0, "ult", {"w": "morningstar-tick", "n": DRAIN_REF_N}]),
                ("slice", ["play", T0, "ult", {"w": ME}])]
        REFS += [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in SCHOOL + TYPE]
        REFS += [(f"{r_} now", ["play", T0, "ult", {"w": r_}]) for r_ in FALL]
        for name, ev in REFS:
            x, _ = R([ev])
            ctl[name] = dict(basic(x), x=x, low=low_share(x))
            M = ctl[name]
            if not name.endswith(" now"):
                print(f"  {name:<13} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
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
        fall = {k: float(np.abs(ctl[f"{k} now"]["x"] - rcx).max()) for k in FALL}
        print(f"  ARE rune-crack today ({len(FALL)} relics with no arm; max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if FALL and max(fall.values()) > 1e-6:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        if ME in fall:
            raise SystemExit("ult/widowmaker falls through to rune-crack -- the wet slice this lab retires is gone")
        rec["fallthrough"] = fall
        # the wet slice: ult/widowmaker today IS the anchor's own three lines
        slx, _ = R([["body", T0, SLICE_BODY, {}]])
        sl_same = float(np.abs(slx - ctl["slice"]["x"]).max())
        print(f"  ult/widowmaker today vs the anchor's own three lines rendered as a body: max |diff| {sl_same:.1e} "
              f"-- {'the anchor IS what plays' if sl_same <= TOL else 'THE ANCHOR IS NOT WHAT PLAYS'}")
        if sl_same > TOL:
            raise SystemExit("the wet slice anchor is not the voice ult/widowmaker plays")
        rec["slice_is_anchor"] = sl_same
        # the noise draws
        DKEYS = ("hit@10.75", "wall", "rune-crack", "death", "loose", "woosh", "spark", "fork", "hex-snap",
                 "zenith-tick", "slice") + SCHOOL + TYPE
        D = {k: [] for k in DKEYS}
        for sd in NOISE_SEEDS:
            for k in D:
                x_ = R([dict(REFS)[k]], seed=sd)[0]
                D[k].append(dict(basic(x_), phone=phone(x_)))
        h_lo, h_hi = min(m["top"] for m in D["hit@10.75"]), max(m["top"] for m in D["hit@10.75"])
        h_ph = min(m["phone"] for m in D["hit@10.75"])
        l_ph = max(m["phone"] for m in D["loose"])
        w_hi = max(m["top"] for m in D["wall"])
        print(f"  the hit @ 10.75 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f};  the wall tick "
              f"{min(m['top'] for m in D['wall']):.4f}-{w_hi:.4f};  PHONE: the blow {h_ph:.4f} (quietest draw), the "
              f"bowstring {l_ph:.5f} (loudest draw) = {db(l_ph / h_ph):+.1f} dB re the blow")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        P90 = bed_p90(bseg)

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        def reg_to(DB, DB2):
            return float(np.median([cos(DB[i], DB2[i]) for i in range(len(DB))]))

        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, hit_phone=h_ph, loose_phone=l_ph)
        wav("widowmaker-ctl-slice.wav", ctl["slice"]["x"])
        wav("widowmaker-ctl-hit1075.wav", ctl["hit@10.75"]["x"])
        wav("widowmaker-ctl-woosh.wav", ctl["woosh"]["x"])
        wav("widowmaker-ctl-spark.wav", ctl["spark"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a low inhale, 0.4s'. Level-matched: TOP {tgt_c:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the time scale solved to AUDIBLE {CAST_AUD:g} ms "
              f"(capped where a 0.58 s sweep runs out). 'heard' over its audible span, at or above 200 Hz")

        def cx(sp, g, s, seed=None):
            return R([["body", T0, cast_body(sp, g, s), {}]], seed=seed)

        def calib_cast(sp):
            g, s = 0.3, 1.0
            smax = 0.58 / max(d for (_o, _a, _b, _q, _k, d, _t, _ty) in sp["segs"])
            for _ in range(3):
                lo_, hi_ = math.log(0.4), math.log(smax)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, math.exp(mid))[0])["aud"] < CAST_AUD: lo_ = mid
                    else: hi_ = mid
                s = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                s = min(s, float(f"{smax:.3g}") if float(f"{smax:.3g}") <= smax else smax * 0.999)
                g = float(f"{g * tgt_c / basic(cx(sp, g, s)[0])['top']:.4g}")
            return g, s

        CREFS = ("rune-crack",) + SCHOOL + TYPE + ("woosh", "loose", "hit@10.75", "death")

        def cast_metrics(M, draws):
            bs = [basic(d_) for d_ in draws]
            M["top_lo"] = min(b_["top"] for b_ in bs); M["top_hi"] = max(b_["top"] for b_ in bs)
            cens = [centroid(d_) for d_ in draws]
            M["cen_lo"], M["cen_hi"] = min(cens), max(cens)
            M["brise"], M["dips"], M["regrow"] = breath(draws, M["a0"], M["aud"])
            M["tonal"] = tonal(draws, T0 + M["a0"] / 1000, T0 + (M["a0"] + M["aud"]) / 1000, 100.0, 8000.0)
            M["tonal50"] = tonal50(draws, M["a0"], M["aud"])
            M["din"] = drawn_in(draws, M["a0"], M["aud"])
            M["place"] = (M["top_at"] * 1000 - M["a0"]) / max(M["aud"], 1e-9)
            M["heard"], M["heard_at"] = heard(draws[0], P90, win=(M["a0"] + M["aud"]) / 1000)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in CREFS}
            M["phone_lo"] = min(phone(d_) for d_ in draws)

        def cast_measure(sp, g, s, name):
            x, calls = cx(sp, g, s)
            x2, _ = cx(sp, g, s)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, s=s, name=name, sp=sp)
            cast_metrics(M, [cx(sp, g, s, seed=sd)[0] for sd in NOISE_SEEDS])
            M["why"] = cast_why(M, lev_c)
            return M

        abbr = {k: k[:4] for k in CREFS}
        abbr.update({"rune-crack": "rc", "hit@10.75": "hit", "death": "dth"})
        print(f"  {'cand':<11}{'g':>7}{'s':>6}{'calls':>6}{'top':>16}{'aud':>5}{'@top':>5}{'place':>6}{'brise':>6}"
              f"{'dips':>5}{'regr':>5}{'tonal':>6}{'t50':>5}{'in c':>6}{'centroid':>12}{'heard':>7}"
              + "".join(f"{abbr[k]:>5}" for k in CREFS))

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<11}{M['g']:>7.4g}{M['s']:>6.3g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}"
                  f"{M['aud']:>5.0f}{M['top_at'] * 1000:>5.0f}{M['place']:>6.2f}{M['brise']:>6.0f}{M['dips']:>5d}"
                  f"{M['regrow']:>5.1f}{M['tonal']:>6.1f}{M['tonal50']:>5.1f}{M['din']:>+6.0f}{M['cen_lo']:>6.0f}-{M['cen_hi']:<5.0f}"
                  f"{M['heard']:>+7.1f}" + "".join(f"{r_[k]:>5.2f}" for k in CREFS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, s = calib_cast(sp)
            M = cast_measure(sp, g, s, name)
            rows_c.append(M); cast_line(M)
            wav(f"widowmaker-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for name, sp, blurb in CAST_CONTROLS:
            g, s = calib_cast(sp)
            M = cast_measure(sp, g, s, name)
            ctlc.append(M); cast_line(M)
            wav(f"widowmaker-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for name, ev in (("0 SLICE-NOW", ["play", T0, "ult", {"w": ME}]),
                         ("0 WOOSH", ["play", T0, "scour-woosh", {"n": 0}])):
            x, calls = R([ev])
            M = basic(x); M.update(x=x, calls=calls[0], g=0.0, s=0.0, name=name, sp=None)
            cast_metrics(M, [R([ev], seed=sd)[0] for sd in NOISE_SEEDS])
            M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES + CAST_CONTROLS:
            print(f"    {name:<11} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print("    0 SLICE-NOW what ult/widowmaker plays today (the nova's wet slice) -- a control\n"
              "    0 WOOSH     `scour-woosh` (the tornado) played as the cast -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<11} out: {'; '.join(M['why'])}")
        for M in ctlc:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          -round(rows_c[i]["place"] / 0.1), rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, s {C_['s']}; {C_['calls']} synth calls; TOP "
              f"{db(C_['top_lo'] / h_lo):+.1f} to {db(C_['top_hi'] / h_lo):+.1f} dB re the hit @ 10.75 (quietest "
              f"draw), top-place {C_['place']:.2f}, drawn in {C_['din']:+.0f} cents")

        # ---- THE DRAIN -----------------------------------------------------
        lev_d = dict(lo=2 * w_hi, hi=h_lo * 10 ** (-DRIP_UNDER_DB / 20), phone=l_ph)
        if lev_d["lo"] >= lev_d["hi"]:
            FAILED.append("drain level window empty")
            print(f"  THE DRAIN'S LEVEL WINDOW IS EMPTY: 2x the wall {lev_d['lo']:.4f} >= the blow -9 dB "
                  f"{lev_d['hi']:.4f}")
        tgt_d = math.sqrt(lev_d["lo"] * lev_d["hi"])
        print(f"\nDRAIN -- 'the bleed's own drip voice reversed and pitched by the foe's stack count, quiet'. "
              f"Level-matched: TOP {tgt_d:.4f} at count {DRAIN_REF_N} (the centre of {lev_d['lo']:.4f}-"
              f"{lev_d['hi']:.4f}: 2x the wall tick's loudest draw .. {DRIP_UNDER_DB:g} dB under the blow's "
              f"quietest). Notes: A minor pentatonic from each candidate's root, counts 1-{CAP}")

        def dx(sp, g, n, seed=None, **kw):
            return R([["body", T0, drain_body(sp, g, **kw), {"n": n}]], secs=2.0, seed=seed)

        def calib_drain(sp, target, **kw):
            g = 0.05
            for _ in range(4):
                g = float(f"{g * target / basic(dx(sp, g, DRAIN_REF_N, **kw)[0])['top']:.4g}")
            return g

        DREFS = ("hit@10.75", "wall", "spark", "fork", "hex-snap", "zenith-tick", "rune-crack")

        def drain_measure(rfn, name, sp, g, notes, lit_fn=None, has_noise=False):
            """rfn(n, seed) -> (x, calls) at count n; notes: each count's declared note."""
            M = {"name": name, "sp": sp, "g": g}
            xs, lands, shapes, tops, auds, lates, phs, hrd, tonals, calls = {}, [], [], [], [], [], [], [], [], {}
            for n in COUNTS:
                x, cl = rfn(n, None)
                if float(np.abs(x - rfn(n, None)[0]).max()) > TOL:
                    raise SystemExit(f"drain {name} does not reproduce")
                xs[n] = x; calls[n] = cl[0]
                sh = drip_shape(x)
                shapes.append(sh); lands.append(sh["land"])
                draws = [rfn(n, sd)[0] for sd in NOISE_SEEDS] if has_noise else [x]
                for d0 in [x] + draws:
                    bd = basic(d0)
                    tops.append(bd["top"]); auds.append(bd["aud"]); lates.append(bd["late"]); phs.append(phone(d0))
                tonals.append(tonal(draws, T0 + sh["a0_ms"] / 1000, T0 + sh["a1_ms"] / 1000 + 0.005, 300.0, 8000.0))
                hrd.append(heard(x, P90))
                if n == DRAIN_REF_N:
                    M["DB"] = [bands(d0[int(T0 * SR):]) for d0 in (draws if has_noise else [x] * len(NOISE_SEEDS))]
            M.update(xs=xs, x=xs[DRAIN_REF_N], calls=calls[CAP], land=lands, top_lo=min(tops), top_hi=max(tops),
                     aud_lo=min(auds), aud_hi=max(auds), late_min=min(lates), phone_lo=min(phs),
                     last_min=min(s_["last"] for s_ in shapes), fall_max=max(s_["fall"] for s_ in shapes),
                     falls=[s_["fall"] for s_ in shapes], dips=sum(s_["dips"] for s_ in shapes),
                     tonal=min(tonals), heard=min(h_[0] for h_ in hrd), heard_at=[h_[1] for h_ in hrd],
                     heard_all=[h_[0] for h_ in hrd])
            M["perr"] = max(abs(cents(p_, f_)) for p_, f_ in zip(lands, notes))
            M["minstep"] = min(cents(lands[i + 1], lands[i]) for i in range(len(lands) - 1))
            M["corr"] = env_corr5(xs[DRAIN_REF_N], lit_fn(DRAIN_REF_N)) if lit_fn else float("nan")
            M["regs"] = {k: reg(M["DB"], k) for k in DREFS}
            M["regs"]["cast"] = reg_to(M["DB"], C_["DB"])
            M["why"] = drain_why(M, lev_d)
            return M

        print(f"  {'cand':<10}{'g':>8}{'calls':>6}{'top':>16}{'aud':>9}{'late':>5}{'last5':>6}{'fall c':>7}{'corr':>6}"
              f"{'dips':>5}{'tonal':>6}{'land Hz (count 1-4)':>22}{'err':>5}{'step':>5}{'heard':>7}"
              + "".join(f"{k[:5]:>6}" for k in DREFS + ("cast",)))

        def drain_line(M):
            r_ = M["regs"]
            ls = "/".join(f"{p_:.0f}" for p_ in M["land"])
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}"
                  f"{M['aud_lo']:>4.0f}-{M['aud_hi']:<4.0f}{M['late_min']:>5.2f}{M['last_min']:>6.2f}"
                  f"{M['fall_max']:>+7.0f}{M['corr']:>6.2f}{M['dips']:>5d}{M['tonal']:>6.1f}{ls:>22}"
                  f"{min(M['perr'], 9999):>5.0f}{M['minstep']:>5.0f}{M['heard']:>+7.1f}"
                  + "".join(f"{r_[k]:>6.2f}" for k in DREFS + ("cast",)))
            print(f"  {'':<10}  phone {db(M['phone_lo'] / l_ph):+.1f} dB re the bowstring's; heard per count "
                  + " ".join(f"{h_:+.1f}@{f_:.0f}" for h_, f_ in zip(M["heard_all"], M["heard_at"]))
                  + f"; the fall per count " + "/".join(f"{v_:+.0f}" for v_ in M["falls"]) + " c")

        rows_k = []
        for name, sp, blurb in DRAIN_CANDIDATES:
            g = calib_drain(sp, tgt_d)
            fwd_g = g
            M = drain_measure(lambda n, sd, sp=sp, g=g: dx(sp, g, n, seed=sd), name, sp, g,
                              [note_of(sp, n) for n in COUNTS],
                              lit_fn=lambda n, sp=sp, fg=fwd_g: literal(dx(sp, fg, n, forward=True)[0], sp, fg),
                              has_noise=bool(sp["click"]))
            rows_k.append(M); drain_line(M)
            for n in (1, CAP):
                wav(f"widowmaker-drain-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        s0 = rows_k[0]; sp0 = s0["sp"]
        notes0 = [note_of(sp0, n) for n in COUNTS]
        lit0 = lambda n: literal(dx(sp0, s0["g"], n, forward=True)[0], sp0, s0["g"])  # noqa: E731
        ctlk = []
        gF = calib_drain(sp0, tgt_d, forward=True)
        ctlk.append(drain_measure(lambda n, sd: dx(sp0, gF, n, seed=sd, forward=True), "0 FORWARD", sp0, gF, notes0,
                                  lit_fn=lit0))
        ctlk.append(drain_measure(lambda n, sd: dx(sp0, s0["g"], n, seed=sd, fixed_n=1), "0 FLAT", sp0, s0["g"],
                                  notes0, lit_fn=lit0))
        gL = calib_drain(sp0, h_lo)
        ctlk.append(drain_measure(lambda n, sd: dx(sp0, gL, n, seed=sd), "0 LOUD", sp0, gL, notes0, lit_fn=lit0))
        ctlk.append(drain_measure(lambda n, sd: R([["play", T0, "spark", {"collect": True, "n": n}]], secs=2.0,
                                                  seed=sd), "0 SPARK", sp0, 0.0, notes0, lit_fn=lit0))
        gN = calib_drain(sp0, tgt_d, noise=True)
        ctlk.append(drain_measure(lambda n, sd: dx(sp0, gN, n, seed=sd, noise=True), "0 NOISE", sp0, gN, notes0,
                                  lit_fn=lit0, has_noise=True))
        ctlk.append(drain_measure(lambda n, sd: dx(sp0, s0["g"], n, seed=sd, raw=True), "0 RAW", sp0, s0["g"],
                                  notes0, lit_fn=lit0))
        for M in ctlk:
            drain_line(M)
            wav(f"widowmaker-drain-{M['name'].replace(' ', '-').lower()}.wav", M["x"])
        wav("widowmaker-drain-literal.wav", lit0(DRAIN_REF_N))
        wav("widowmaker-drip-forward-n2.wav", dx(sp0, gF, DRAIN_REF_N, forward=True)[0])
        for (name, _sp, blurb) in DRAIN_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        for (name, blurb) in DRAIN_CONTROLS:
            print(f"    {name:<10} {blurb} -- a control")
        print(f"  RULE  {DRAIN_RULE}")
        for M in rows_k:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlk:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_k, "drain")
        ki = fb if ok is None else min(ok, key=lambda i: (round(max(rows_k[i]["regs"].values()) / 0.05),
                                                          rows_k[i]["calls"], i))
        K_ = rows_k[ki]
        print(f"  PICK  {K_['name']}  g {K_['g']}; lands " + " / ".join(f"{p_:.1f}" for p_ in K_["land"]) +
              f" Hz; loudest 50 ms {db(K_['top_lo'] / h_lo):+.1f} to {db(K_['top_hi'] / h_lo):+.1f} dB re the "
              f"hit @ 10.75 (quietest draw), {db(K_['top_lo'] / w_hi):+.1f} dB or more re the wall; "
              f"{K_['calls']} strikes at count {CAP}")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   drain {K_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        what_c = cast_what(C_["sp"])
        what_k = {"1 DROP": "a sine sliding down a fifth onto the note as it swells, and stopping",
                  "2 SLURP": "a sine sliding down a fifth onto the note as it swells, and stopping on the drop's "
                             "contact reversed, a 6 ms 3.5 kHz tick",
                  "3 LOW": "a sine sliding down a fifth onto the note (an octave under DROP's) as it swells, and "
                           "stopping",
                  "4 WIDE": "a sine sliding down an octave onto the note as it swells, and stopping",
                  "5 TRI": "a triangle sliding down a fifth onto the note as it swells, and stopping"}[K_["name"]]
        sh_ = [drip_shape(K_["xs"][n]) for n in COUNTS]
        info = dict(n_cast=len(CAST_CANDIDATES), n_drain=len(DRAIN_CANDIDATES),
                    c_what=what_c, c_in=C_["din"], c_rise=C_["brise"], c_cen0=C_["cen_lo"], c_cen1=C_["cen_hi"],
                    c_tonal=C_["tonal50"], c_aud=C_["aud"], c_top=db(C_["top"] / h_lo), c_reg=max(C_["regs"].values()),
                    k_what=what_k, k_R=fmt(K_["sp"]["R"]), k_D=K_["sp"]["D"],
                    k_notes=" / ".join(f"{note_of(K_['sp'], n):.0f}" for n in COUNTS), k_err=K_["perr"],
                    k_fall=max(s_["fall"] for s_ in sh_), k_aud0=K_["aud_lo"], k_aud1=K_["aud_hi"],
                    k_last=K_["last_min"], k_corr=K_["corr"], k_calls=K_["calls"],
                    k_db0=db(K_["top_lo"] / h_lo), k_db1=db(K_["top_hi"] / h_lo), k_wall=db(K_["top_lo"] / w_hi),
                    k_reg=max(K_["regs"].values()))
        arms = arms_code(C_, K_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        kbt = drain_body(K_["sp"], K_["g"])
        rp = [float(np.abs(R([["body", T0, kbt, {"n": CAP}]])[0] - R([["body", T0, kbt, {"n": CAP}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the top drip rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        cbt = cast_body(C_["sp"], C_["g"], C_["s"])
        for sd in (None, NOISE_SEEDS[5]):
            tag = "" if sd is None else "'"
            xa, _ = R([["arm", T0, "ult", {"w": ME}]], seed=sd, rows=sfx_rows)
            chk.append(("cast" + tag, float(np.abs(xa - R([["body", T0, cbt, {}]], seed=sd)[0]).max())))
            for n in (-1, 0, 1, 2, 3, 4, 7, None):
                p1 = {"w": ME + "-drain"} if n is None else {"w": ME + "-drain", "n": n}
                x1, _ = R([["arm", T0, "ult", p1]], seed=sd, rows=sfx_rows)
                nn = 1 if n is None else min(CAP, max(1, n))
                x2, _ = R([["body", T0, kbt, {"n": nn}]], seed=sd)
                chk.append((f"drain@{n}{tag}", float(np.abs(x1 - x2).max())))
            if sd is None:
                xa0 = xa
        print("  the arms vs the picked candidates, max |diff| (render.py's draw and a second): " +
              ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 10.75, 16.23, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 3}), ("clank", {"mass": 5}), ("seal", {}),
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
        now_sl = float(np.abs(xa0 - ctl["slice"]["x"]).max())
        print(f"  ult/widowmaker vs the wet slice after the row: max |diff| {now_sl:.3f} -- "
              f"{'the slice is retired' if now_sl > 1e-3 else 'STILL THE SLICE'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_sl <= 1e-3:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_slice=now_sl, cost=cost, repro=max(rp))

        # ---- WITH OTHER RELICS' ROWS ------------------------------------------
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
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
            evs = [("ult", {"w": ME})] + [("ult", {"w": ME + "-drain", "n": n}) for n in COUNTS]
            evs += [("ult", {"w": w_, "n": 3, "shield": 45}) for w_ in pids] + [(k_, {}) for k_ in pk_]
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
            pr = {}
            for (kind_, w_), xp in PX.items():
                bp = bands(xp[int(T0 * SR):])
                pr[w_] = [cos(bands(C_["x"][int(T0 * SR):]), bp), cos(bands(K_["x"][int(T0 * SR):]), bp)]
            worst_p = max(((max(v), k) for k, v in pr.items()), default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both "
                  f"orders render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the cast / drain against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) "
                  f"-- printed, not gated")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=pr))
        rec["peers"] = peers

        # ---- THE tickStatus ROW --------------------------------------------
        trows = [[DRAIN_ANCHOR, DRAIN_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickStatus ROW, applied to Match.prototype.tickStatus's own source, run beside the original on "
              "real fights (the mirror match is refused by Match -- 'A relic cannot fight itself'):")
        WR = page.evaluate(WIRE_JS, [seeds, trows])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Widowmaker both sides x every foe x seeds {seeds}): {WR['same']}/{WR['fights']} "
              f"identical (over, clock, both hp, shields, positions, velocities, charges, both hemorrhage counts, "
              f"winner, her whole drainTally and ultDrain); every other voice call identical in order, kind and opts "
              f"in {WR['otherSame']}/{WR['fights']}")
        nh = WR["nh"]
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['drained']:.0f} hp "
              f"drained -> {WR['drips']} whole-hp crossings -> {WR['dripV']} drips ({WR['fatal']} on the bleed's "
              f"killing tick); problems {WR['nbad']}")
        print("  the count a drip carries (the bleeding foe's hemorrhage stacks): " +
              ", ".join(f"{n}: {nh[n]}" for n in COUNTS) +
              f" ({100 * nh[CAP] / max(1, sum(nh)):.0f}% at the cap);  drips a window (median) {WR['perWinMed']}; "
              f"the gap between drips in a window: min {1000 * WR['gapMin']:.0f} ms, p5 {1000 * WR['gapP5']:.0f} ms, "
              f"median {1000 * WR['gapMed']:.0f} ms (match time, hit stops included); "
              f"{WR['inCast']} drips inside a cast's first 0.4 s")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["dripV"] != WR["drips"] or WR["castV"] != WR["casts"] or WR["drips"] == 0:
            FAILED.append("tickStatus row")
        if 1000 * WR["gapMin"] < K_["aud_hi"]:
            print(f"  NOTE: the closest two drips ({1000 * WR['gapMin']:.0f} ms) are closer than a drip is long "
                  f"({K_['aud_hi']:.0f} ms): they overlap there (printed, not gated)")
        WB = page.evaluate(WIRE_JS, [seeds, [[DRAIN_ANCHOR, DRAIN_CODE_BAD]]])
        assert not errors, errors[:3]
        print(f"  the control (the row plus one sim write, her x nudged 1e-9 on a drip): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "drips", "dripV",
                                          "fatal", "inCast", "nh", "drained", "gapMin", "gapP5", "gapMed",
                                          "perWinMed", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        print(f"  THE CLOSE: {WR['ends']['clock']} windows closed by their clock, {WR['ends']['death']} by a death and "
              f"{WR['ends']['over']} by the fight's end -- none plays anything (v76 §4: 'close -- nothing'; no row "
              f"touches tickDrain)")
        print(f"  synth calls the drain adds: {K_['calls']} a drip at count {CAP}; about "
              f"{WR['dripV'] * K_['calls'] / max(1, WR['fights']):.0f} a fight (the bed schedules ~1700 nodes a match)")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["drips"], w["foe"], w["seed"], w["side"]))
        print(f"\n{REAL_RULE}")
        if cand:
            w_ = cand[len(cand) // 4]           # a busy window, not the busiest
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], trows])
            assert not errors, errors[:3]
            c0, c1 = w_["cast"], w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            if len(bd) < len(xw):
                bd = np.concatenate([bd, np.zeros(len(xw) - len(bd))])
            xw = xw + bd; xo = xo + bd
            dr = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == ME + "-drain"]
            ct = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME]
            others_at = [(T0 + (e[0] - lo_t), e[1] + ("/" + e[2]["w"] if e[1] == "ult" and "w" in e[2] else ""))
                         for e in evs if not e[3]]

            def near(t_, a_=-0.05, b_=0.1):
                return ", ".join(f"{k_} {1000 * (u_ - t_):+.0f} ms" for u_, k_ in others_at if a_ <= u_ - t_ <= b_)

            def ov(f, a_, d_):
                return db(band_rms(xw, f, a_, a_ + d_) / max(band_rms(xo, f, a_, a_ + d_), 1e-12))
            span = K_["aud_hi"] / 1000 + 0.01
            d_over = [ov(note_of(K_["sp"], n), t_, span) for t_, n in dr]
            bc = bands(C_["x"][int(T0 * SR):int((T0 + 0.4) * SR)])
            fc_c = max((v_, fc) for v_, fc in zip(bc, BANDS) if fc >= PHONE_HZ)[1]
            c_over = [ov(fc_c, t_, 0.4) for t_ in ct]
            med = float(np.median(d_over)) if d_over else float("nan")
            print(f"IN A REAL WINDOW -- widowmaker v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {len(dr)} drips; the fight's own sounds and the "
                  f"score, with and without the two voices")
            print("  each drip over the fight in its landing note's third-octave over its own span: " +
                  " ".join(f"{v:+.1f}" for v in d_over) + f" dB (median {med:+.1f}; counts " +
                  "".join(str(n) for _, n in dr) + f");  the cast ({fc_c:.0f} Hz, 0.4 s): " +
                  " ".join(f"{v:+.1f}" for v in c_over) + " dB")
            for (t_, n), v1 in zip(dr, d_over):
                if v1 < 3:
                    print(f"    the drip at {t_ - T0 + lo_t:.3f}s (count {n}, {v1:+.1f} dB) shares its span with: "
                          f"{near(t_, -0.05, span) or 'nothing'}")
            if (not d_over) or med < 3 or (c_over and min(c_over) < 6):
                FAILED.append("a new voice not heard in a real window")
            wav("widowmaker-pick-real-window.wav", xw)
            wav("widowmaker-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, drip_over=d_over, drip_median=med, cast_over=c_over,
                               counts=[n for _, n in dr])
        # the picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, n in enumerate(COUNTS):
            for j in range(3):
                seq.append(["arm", T0 + 0.8 + 0.9 * k_ + 0.25 * j, "ult", {"w": ME + "-drain", "n": n}])
        seq += [["arm", T0 + 4.8, "hit", {"dmg": BLADE, "crit": False}]]
        xq_, _ = R(seq, secs=7.0, rows=sfx_rows)
        wav("widowmaker-pick-sequence.wav", xq_)

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_voices = [(k_, p_) for k_, p_ in others if k_ != "ult"][:36] + \
                     [("ult", {"w": w_}) for w_ in ult_ids if w_ in {w for w, _a, _s in info0["W"]}][:12]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [R([["play", T0, k_, p_]])[0] for k_, p_ in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
            assert not errors, errors[:3]
            e2e_ref["new"] = {"cast": C_["x"]}
            for n in COUNTS:
                e2e_ref["new"][f"drain n{n}"] = K_["xs"][n]

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Exsanguinate's inhale and drain arms, replacing the nova's wet slice",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickStatus: the drain's drip, once per whole hp drained, after the gain is booked",
                 anchor=DRAIN_ANCHOR, mode="replace", code=DRAIN_CODE)]
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        if patched.count(DRAIN_ANCHOR) != 1 or patched.count(SFX_ANCHOR) != 0:
            raise SystemExit("end to end: the drain anchor is not re-emitted once, or the slice survives")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="widowmaker_e2e_"))
        try:
            tp = tmpd / "sc-widowmaker-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the two rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            with game(game_path=tp) as (page_, errors):
                page2 = Reopen(page_, errors, tp)

                def R2(evs, secs=3.0, seed=None):
                    r = page2.evaluate(RENDER_JS, [evs, secs, seed, None])
                    assert not errors, errors[:3]
                    return pcm(r)
                vo = max(float(np.abs(R2([["play", T0, k_, p_]]) - x0).max())
                         for (k_, p_), x0 in zip(e2e_voices, e2e_ref["voices"]))
                NEWP = [("cast", {"w": ME}, 3.0)] + [(f"drain n{n}", {"w": ME + "-drain", "n": n}, 2.0) for n in COUNTS]
                nd = [(lab_, float(np.abs(R2([["play", T0, "ult", p_]], secs=s_) - e2e_ref["new"][lab_]).max()))
                      for lab_, p_, s_ in NEWP]
                F1 = page2.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
                assert not errors, errors[:3]
                page_err = len(errors)
                rec["crashes_e2e"] = page2.n
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
        F0 = {f_["key"]: f_ for f_ in e2e_ref["fights"]}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        d_ok = sum(f_["dripV"] == f_["drips"] and f_["badN"] == 0 for f_ in F1)
        orig_new = sum(f_["dripV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "drips", "castV", "dripV")}
        print("  the two voices through the patched page's own SFX.play vs the lab's candidate text, max |diff|: " +
              ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, drips = whole hp drained (n the foe's "
              f"count) {d_ok} (of {len(F1)}); totals {tot}; the original page played {orig_new} drips; page errors "
              f"{page_err}")
        if max(v for _, v in nd) > TOL or vo > TOL or same != len(F1) or osame != len(F1) \
                or min(c_ok, d_ok) != len(F1) or orig_new or page_err:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, fights=len(F1), same=same, other_same=osame, totals=tot)

    rec["crashes"] = page.n
    if page.n or rec.get("crashes_e2e"):
        print(f"\n  the renderer crashed {page.n} + {rec.get('crashes_e2e', 0)} time(s); each call was repeated on a "
              f"fresh page (see Reopen)")

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB", "sp")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), drain=strip(rows_k), drain_controls=strip(ctlk),
               wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_s": C_["s"], "drain": K_["name"], "drain_g": K_["g"]})
    print(f"\nTHE PICKS  cast {C_['name']}   drain {K_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text to a copy of the page: {E2['same']}/{E2['fights']} fights "
          f"identical to the unpatched page's" if E2 else "")
    wr = rec["wire"]
    ac = rec["arm_check"]
    pn = [peer_name(p_["file"]) for p_ in rec["peers"]]
    pw = [n_ + "'s" for n_ in pn]
    pw = (", ".join(pw[:-1]) + " and " + pw[-1]) if len(pw) > 1 else "".join(pw)
    pe = (f"; with {pw} Sfx rows (the batch's scratch builds) applied too, in either order, every arm of both "
          f"renders alike" if pn else "")
    rows[0]["why"] = (
        f"The two voices of v76 §4, in the synth only; the close has none. The row REPLACES the three lines of "
        f"the nova's 'wet slice' -- the voice keyed on the relic that v106 §5 retires -- and adds the drain's arm "
        f"beside it; it does not touch the shared rune-crack fallback. Through the patched play() every arm "
        f"reproduces its lab candidate (worst {max(v for _, v in ac['chk']):.0e}; the drain at counts -1, 0, 1-4, 7 "
        f"and a missing n, on two noise draws), {len(ac['others'])} other voices are unchanged (worst "
        f"{max(v for _, v in ac['others']):.0e}), and ult/widowmaker is no longer the slice. play() returns on its "
        f"first line with no audio context (every headless run), draws no random number and writes nothing the "
        f"simulation reads"
        + (f"; end to end the two voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + pe + ".")
    rows[1]["why"] = (
        f"One guarded SFX.play in tickStatus's drain block, after the line that books the gain (re-emitted "
        f"unchanged), with a local `k0` read before it: a drip each time her running total crosses a whole hp, n = "
        f"the bleeding foe's hemorrhage stacks (a read). {wr['dripV']}/{wr['drips']} whole-hp crossings voiced, "
        f"none elsewhere, each inside her window and inside tickStatus (live steps only), each n the foe's count "
        f"(1-{CAP}; {100 * wr['nh'][CAP] / max(1, sum(wr['nh'])):.0f}% at the cap); {wr['same']}/{wr['fights']} "
        f"fights identical and every other SFX call identical in order and opts; the same row plus one sim write "
        f"(her x nudged 1e-9 on a drip) comes back {wr['control_same']}/{wr['fights']}{e2}. No float, beat, stop "
        f"or array entry: probe [6], [7] and [10] are untouched.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The two rows are the edits; both were applied "
          "to the page's own code above, and as text to a copy of the page.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
