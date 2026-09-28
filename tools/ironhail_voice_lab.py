#!/usr/bin/env python3
"""QUARRELSTORM'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v108.

    python ironhail_voice_lab.py --game <a link carrying Ironhail's stage 3> --rows rows.json

v83 §4 SOUND, every word of it: "cast -- a forge-bellows huff, 0.4s; a landing
-- a short iron thud (<=0.15s), pitched by sunder count; a miss -- a quieter
thud; close -- nothing." The brief's stage 4 (v108's stage 6): "picture,
voice, carry". Rick, for the batch's art and sound: "you pick i overrule". So
this lab does not offer a spread -- it renders three to five candidates a
voice beside CONTROLS that can come back wrong, prints the numbers each pick
is made on, and PICKS by a rule written in this file (`*_RULE`, `*_why`). He
overrules from one clip.

NOTHING IS REUSED, BECAUSE §4 NAMES NOTHING TO REUSE. All three voices are new
arms of the `ult` kind. THE CLOSE HAS NO VOICE: §4 says "close -- nothing", so
no row touches the window's close line.

THE THREE EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/ironhail`, which `fireUlt` plays for every relic.
         Ironhail has NO arm today: it falls through to the shared rune-crack
         (measured below, to 1e-6, with every other relic that still does).
         The arms go BEFORE that fallback; the fallback line is re-emitted
         unchanged, so another relic's row anchored on it still applies, in
         either order. No sim line: the cast already plays.
  land   `ult/ironhail-land {n}` from `tickHail`, right after the landing's
         sunder line (re-emitted first, unchanged): once per landed bolt,
         after its hurt and its sunder, `n` = `foe.stacks("sunder")` -- the
         count the foe now carries, the number its tag shows, 1..6 at the cap
         of 6 (every sunder on it, the bow's own onHit sunder included). A
         landing at the cap (6 -> 6) still thuds, at 6's note. A killing
         landing thuds too (it is a landing), under the death voice; its own
         fatal hit beat is the sim's, untouched. A ward that shatters on a
         landing plays its own crit voice inside `hurt`, on the same frame.
  miss   `ult/ironhail-miss` from `tickHail`, on a line placed BEFORE the miss
         line, which is re-emitted unchanged: that line's own test, read
         first (a read -- `foe.alive` and two positions -- and guarded by the
         anchor itself: if the test ever changes, the anchor stops matching
         and the row refuses to apply). So a bolt the sim counts as missed
         thuds once, on its landing frame -- including a bolt that falls on
         the step its foe died (the floor still takes it; counted below). A
         miss carries no count: it sunders nothing.

THE CONTROLS, and what each one is for:
  rune-crack   what Ironhail's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@16.23    Ironhail's own blow (the blade holds at 16.23): the level every
               voice is judged against, on its quietest / loudest noise draw
  hit@4        the engine's own hit voice at a landing's damage: printed
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   the dwarven casts with a voice of their own (read off the page)
  the type     the bow casts with a voice of their own (read off the page)
  woosh        `scour-woosh`, the game's one voice made of moving air: a
               bellows is air too, and must not be the tornado
  loose        the bow's own string, on every shot
  clank        the weapons' clash (mass 3): the landing is not a parry
  death        the heaviest low voice in the game: a thud must not be one
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  TICK, WHISTLE, HISS, DOUBLE, WOOSH, RC-NOW, RUMBLE   the cast's bands as
               fixed-filter bursts (a strike) / at q 14 (a note) / three
               octaves up (a quench, not a bellows) / two half-length huffs
               0.25 s apart / the tornado's woosh / what `ult/ironhail` plays
               today / WHOOMPH an octave and a half down (round 2): each must
               fail its gate
  FLAT, LONG, WOOD, CLICK, BLOW   the landing at one pitch for every count /
               ringing 0.45 s / without its iron / its contact click alone /
               the engine's hit at a landing's 4 damage: each must fail its
               gate
  LOUD, FAINT, HISS   the miss at the landing's own level / 30 dB under it /
               a noise puff: each must fail its gate

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT. Each candidate is generated as the JS
    body that will sit in the arm (constants rounded first) and rendered by
    evaluating that text on the synth; the rows are then applied to
    `Sfx.prototype.play`'s own source and rendered again, and must match to
    TOL = 1e-5 (-100 dB; REPRO, the same text rendered twice, is printed).
    There is no second transcription to get wrong.
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's and
    bindweed_voice_lab's, imported unchanged (E50 = 50 ms RMS at a 5 ms hop;
    TOP = the loudest 50 ms; PEAK = the sample peak; AUDIBLE = first to last
    5 ms RMS window above 2% of the voice's own loudest; GONE = where it ends,
    from the event; RISE = 10 -> 90% of the 1 ms envelope; REG = cosine of
    1/3-octave band amplitudes, 25 Hz-16 kHz, the median over noise draws;
    IN-BAND = RMS inside the third-octave round a pitch; PITCH = FFT peak,
    Hann, zero-padded, parabolic; METAL = ironwood's inharmonic-mode test: the
    strongest peak between 1.5x and 4x the note is >= 60 cents from every
    whole multiple and within 20 dB of it; TONAL = bindweed's: how far the
    draw-averaged spectrum's sharpest 1/48-octave peak stands over the median
    of its third-octave neighbourhood, dB -- averaged noise reads a few dB, a
    tone tens).
  * New here, each with a control that can come back wrong:
      BREATH-RISE  the draw-averaged 5 ms power envelope's 10 -> 90% climb, ms
                   (noise's 1 ms envelope is too jagged to time a swell on one
                   draw; TICK must read ~0)
      DIPS / REGROW  on the draw-averaged 25 ms envelope, inside AUDIBLE: dips
                   of >= 3 dB under the running top on the way up to the
                   loudest window, and the largest climb (dB) over the running
                   minimum after it -- one breath swells once and falls once
                   (DOUBLE must fail)
      CENTROID     the power centroid from t = 1.0, Hz, on every draw
      LOW400       the share of the power below 400 Hz from t = 1.0 (a thud
                   is low: CLICK and HISS must fail)
      BODY PITCH   the FFT peak 40-400 Hz over 30-130 ms (after the punch)
      IRON         METAL on the body pitch over 30-90 ms (WOOD must fail)
      HEARD        the voice's loudest third-octave AT OR ABOVE 200 Hz over its
                   first 100 ms against the score's p90 in that third-octave
                   (the bed's 100 ms windows, 2-10 s, 50 ms hop), dB -- read at
                   its LOUDEST such third-octave from the start (Coldiron's
                   v103 lesson: a low body under the score's bass is heard, on
                   a phone speaker, by whatever partial stands over it; round
                   2: and a phone does not reproduce under 200 Hz, so no band
                   under it may carry the voice -- DEAD must fail)
      PHONE        Culverin's (v96): the TOP of the voice high-passed (FFT) at
                   200 Hz -- what a phone speaker reproduces; the deliverable is
                   watched on phones (round 2; FAINT must fail)
      PHONE-PITCH  the FFT peak 200-2000 Hz over 30-130 ms: the note a phone
                   hears the count by (round 2; FLAT and DEEP must fail)
      PHONE-NOTE   that peak's third-octave over the first 100 ms against the
                   score's p90 there, dB (round 2; DEEP must fail)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's time scale is solved so it is AUDIBLE 400 ms and its
    gain puts TOP at the centre of its window; the landing's decay is solved
    so it is GONE by 120 ms at count 1 and its gain puts TOP at the centre of
    its window at count 3; the miss's gain puts TOP 6 dB under the landing's
    at count 3, its decay the landing's own. Constants are rounded BEFORE any
    measured render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of §4 turned into numbers):
  * "0.4s": AUDIBLE 330-470 ms, v100's reading of Portcullis's "0.4s".
  * "A HUFF": a breath -- it swells (BREATH-RISE >= 40 ms), it is one breath
    (no dip, no regrowth), and it is air, not a note (TONAL <= 10 dB, v101's
    "noise, not a chime"). A single `_sweep` cannot be AUDIBLE 400 ms (its
    decay reaches 0.0001 at `dur`, capped at the 0.6 s noise buffer), so a
    breath is two overlapping sweeps, as `scour-woosh` is (CLAUDE.md 4.5).
    Built from `_sweep`, never `_burst`: the toolkit's own note says every
    `_burst` is a tick by construction. (Round 2's geometry: a `_sweep` is a
    tent in dB -- up 80 dB over its attack, down 80 over the rest -- so the
    longest one hump two sweeps can make is a SWELL with the longest attack
    `_sweep` allows (0.6 x 0.58 s) and a HUFF that peaks WITH it and decays
    over the rest of its own 0.58 s: about 0.43 x (0.35 + 0.56) s above -34
    dB. Staggered tops are two humps.)
  * "FORGE-BELLOWS": a big slow push of air into a fire, not a quench's hiss
    (Coldiron's STEAM centres at 7.7 kHz) and not a rumble: the power
    CENTROID 150-2000 Hz on every draw.
  * "SHORT (<=0.15s)": GONE <= 150 ms, at every count on every draw.
  * "A THUD": an impact (RISE <= 5 ms, the peak in the first 15 ms), low
    (LOW400 >= 0.50 at every count on every draw), in a sine or triangle
    body under a falling punch (the body's octave -> the body, 30 ms) and a
    12 ms 2.5 kHz contact click (the bolt meeting the foe).
  * "IRON": the body carries an inharmonic partial -- a bar mode (2.76) or
    plate modes (1.59, 2.14) -- that passes METAL at every count.
  * "PITCHED BY SUNDER COUNT", ON A PHONE (round 2): the count must reach the
    device the video is watched on -- PHONE-PITCH rises >= 30 cents with every
    count and PHONE-NOTE >= +6 dB at every count (HEARD's own threshold).
  * "PITCHED BY SUNDER COUNT": the body's note steps UP with the foe's count
    after the landing (1..6), the batch's reading -- Bindweed's bite (v68,
    "pitched up a semitone per entangle stack") and Coldiron's anvil (v73,
    "pitch steps up with the sunder count") -- from A2 (110 Hz, the score's
    tonic; Coldiron's v103 measured it the one low note clear of the score's
    bass), a semitone a stack (A2 -> D3) or, in PENT, a step of A minor
    pentatonic (A2 C3 D3 E3 G3 A3). Counts are clamped to 1..6 (the cap).
    Every constant-pitch tone has `.frequency.value = f` set (v97's toolkit
    finding); the punch glides and does not.
  * "A QUIETER THUD": the picked landing's own thud, 6 dB under it (level
    match; the gate is >= 3 dB under the landing's quietest count on its
    loudest draw), at COUNT 0's note -- one step under a first landing, since
    a miss sunders nothing -- and still a thud, still heard.
  * LEVELS: the cast and a landing are heard like a blow and never over one
    (TOP between 0.5x the hit @ 16.23's loudest draw and 1.0x its quietest --
    the engine's own hit voice puts a blow of 4 there too, printed); a miss is
    at least 2x the wall tick and quieter than every landing, and (round 2)
    its PHONE at least the bowstring's.

THE ROUNDS. Round 1 (candidates 1-5 of each voice, the rules above as first
written) exited 1, and two of its answers were wrong on the device the video
is made for. Every round-1 candidate stays in the table; round 2 ADDS
candidates and changes the rules named here, and no other:
  * THE CAST: no candidate passed. Every round-1 breath read 0.91-0.99 against
    the tornado's woosh and 0.82-0.94 against the bowstring (a band-passed
    noise sweep through 300-1400 Hz IS the woosh's register), and every one
    was two humps, not one breath: two exponential `_sweep` envelopes, the
    second starting as the first falls, dip and regrow 11-12 dB. Round 2 adds
    four breaths built on the one geometry that is one hump -- THE SWELL (a
    sweep whose attack is its longest allowed, 0.6 of 0.58 s) and THE HUFF (a
    sweep with a 20 ms attack whose top lands ON the swell's and whose 0.56 s
    decay outlasts it; a sum of two tents is one hump when the later peaks with
    the earlier), in a lowpass register UNDER the woosh and the bowstring
    (150-400 Hz), with and without a thin nozzle band. And one control, RUMBLE
    (WHOOMPH an octave and a half down, 50-133 Hz: not a bellows, a rumble).
    No cast rule changed, except that its real-window check now reads the
    cast's loudest third-octave AT OR ABOVE 200 Hz (below).
  * THE LANDING: round 1 picked 4 DEEP, the bolt on A1 (55-73 Hz), the only
    candidate under 0.80 against the blow and the death voice -- and on a
    phone speaker, which reproduces little under 200 Hz, DEEP's count is not
    there at all: its strongest partial over 200 Hz is 12 dB UNDER the score
    and does not rise with the count. That is Culverin's v96 round-3 lesson
    ("the first thud picked was 57 dB down above 200 Hz") and Coldiron's v103
    ("on a phone speaker ... the partials are all anyone hears"). Round 2 adds
    four bolts on A2 whose iron bar mode (2.76x, 304-405 Hz, where a phone
    speaks) is as loud as the body or louder, and two gates, both on the words
    "pitched by sunder count": PHONE-PITCH (the strongest peak 200-2000 Hz,
    30-130 ms, rises >= 30 cents with every count) and PHONE-NOTE (that peak's
    third-octave over the first 100 ms stands >= +6 dB over the score's p90 --
    HEARD's own threshold). HEARD itself is now read at the loudest
    third-octave AT OR ABOVE 200 Hz, for every voice.
  * THE MISS: round 1 picked 3 DEAD at count 0's note of DEEP (51.9 Hz), with
    no click: on a phone, nothing. The same HEARD (>= 200 Hz), and PHONE (the
    TOP of the voice high-passed at 200 Hz, Culverin's measure) at least the
    bowstring's (Briarwand's and Culverin's floor for every voice: "at least
    as audible there as the bow's release"). The miss candidates are built on
    the picked landing, so they change with it.
  * THE REAL WINDOW (a check on the picks, not a rule a candidate is picked
    on): its bands are now read at or above 200 Hz, like HEARD, and each
    landing and miss is read over its own first 50 ms (its TOP window) rather
    than 100 ms. Round 2's first run read one landing +4.9 dB over 100 ms:
    Cindercleave's fire jet began 58 ms AFTER the thud, inside the window, and
    a sound that begins after a thud's loudest 50 ms cannot hide it. Both
    readings are printed, with every other voice that shares a quiet one's
    100 ms. The thresholds did not move.

THE PICKS -- filled in from the run (see the run's own printout; the rows'
comments carry the same numbers).

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (the three arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the landing at
    counts -1, 0, 1..6, 9 and a missing `n`, on two noise draws) must
    reproduce its candidate to TOL; every other voice through the patched
    play (the hit at five weights with and without a crit, spark x3, wall,
    death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork,
    scour x4, and every relic's cast and every sub-voice the ult arm names)
    must be unchanged; `ult/ironhail` must NOT be rune-crack any more;
  * the two tickHail rows are applied to `Match.prototype.tickHail`'s own
    source and run on real fights beside the unpatched one: every fight
    identical (over, clock, both hp, shields, positions, velocities, charges,
    both sunder counts, the bolts in the air, winner and the whole hailTally)
    and every other voice call identical in order, kind and opts; one landing
    voice per landing, on its step, carrying the foe's count right after its
    sunder; one miss voice per miss, on its step; one cast voice per cast; the
    unpatched runs play no landing or miss. The same rows plus ONE sim write
    (the foe nudged 1e-9 on a landing) must come back NOT identical, or
    "identical" proves nothing. (The Sfx row cannot reach the simulation at
    all: `play` returns on its first line with no audio context, which is
    every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a
    temp folder, never the repo), loaded in a fresh browser after the first
    is closed: the page loads clean, its own SFX.play renders the arms to the
    lab's text, every other voice to the original page's, and its fights are
    identical to the original page's, with one voice per landing and miss.
  * WITH OTHER RELICS' ROWS (`--peer-rows`, optional): each peer's Sfx rows
    and these applied to play()'s source in both orders render every arm of
    both identically.
  All anchors must occur exactly once in the game file, and every row is a
  `replace` that re-emits its anchor unchanged exactly once, so a later
  relic's row -- or the picture's -- anchored on the same line still applies,
  in either order.

Writes wavs to 05-reference/v108/ironhail-*.wav at RAW level (gitignored).
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
# it means in v98's, v99's and v101's labs. (Their module bodies only check
# their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm, low_share  # noqa: E402
from bindweed_voice_lab import tonal  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "ironhail"
BLADE = 16.23                             # Ironhail's dmg (the blade holds at the shipped 16.23)
DROP = 4.0                                # w.ult.dropDmg
CAP = 6                                   # STATUS.sunder.maxStacks (checked on the page)
COUNTS = list(range(1, CAP + 1))
CAST_AUD = 400.0                          # "0.4s": the time scale is solved to this
LAND_GONE = 120.0                         # the landing's decay is solved to this (gate: <= 150)
GONE_MAX = 150.0                          # "<=0.15s"
LAND_REF_N = 3                            # the count the landing is level-matched at
MISS_UNDER_DB = 6.0                       # the miss's level match under the landing
A2 = 110.0
STEPS = {"semi": [0, 1, 2, 3, 4, 5], "pent": [0, 3, 5, 7, 10, 12]}
UNDER = {"semi": 1, "pent": 2}            # count 0's note: one step under count 1 (G#2 / G2)
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)

# =============================================================== THE CAST ===
# "a forge-bellows huff, 0.4s". A breath is two overlapping `_sweep`s (see the
# docstring): (onset s, f0, f1, q, level, dur s, atk s, filter), in time units
# the calibration scales so the whole is AUDIBLE 400 ms.
BREATH = {
    "push":   [(0.00, 300, 600, 0.8, 1.0, 0.30, 0.18, "bandpass"),
               (0.12, 600, 1200, 0.8, 0.9, 0.34, 0.10, "bandpass")],
    "exhale": [(0.00, 1400, 800, 0.8, 1.0, 0.26, 0.10, "bandpass"),
               (0.08, 800, 350, 0.8, 0.9, 0.38, 0.08, "bandpass")],
    "arc":    [(0.00, 350, 1000, 0.8, 1.0, 0.28, 0.16, "bandpass"),
               (0.14, 1000, 400, 0.8, 0.9, 0.36, 0.08, "bandpass")],
}
ROAR = (0.10, 120, 280, 0.6, 0.8, 0.40, 0.16, "lowpass")
# ROUND 2 (see THE ROUNDS): the swell (the longest attack `_sweep` allows, 0.6 x
# 0.58 s) and the huff (a 20 ms attack whose top lands on the swell's, decaying
# over the rest of its 0.58 s) -- one hump -- in a lowpass register under the
# woosh and the bowstring, and a thin nozzle band (q 2-2.5) over it or not.
WHOOMPH = [(0.00, 150, 300, 0.7, 1.0, 0.58, 0.34, "lowpass"),
           (0.32, 400, 150, 0.7, 1.0, 0.58, 0.02, "lowpass")]
NOZZLE = {"bellows": (0.32, 3000, 2200, 2.0, 0.30, 0.58, 0.02, "bandpass"),
          "nozzle": (0.32, 3500, 2500, 2.5, 0.25, 0.58, 0.02, "bandpass"),
          "forge": (0.32, 2600, 1800, 2.0, 0.30, 0.58, 0.02, "bandpass")}
CAST_CANDIDATES = [
    ("1 PUSH", dict(segs=BREATH["push"]),
     "the boards pressed: one breath whose band climbs 300 -> 1200 Hz as the pressure builds (bandpass, q 0.8)"),
    ("2 EXHALE", dict(segs=BREATH["exhale"]),
     "the air let go: one breath whose band falls 1400 -> 350 Hz"),
    ("3 ARC", dict(segs=BREATH["arc"]),
     "a breath that climbs and falls, 350 -> 1000 -> 400 Hz"),
    ("4 ROAR", dict(segs=BREATH["exhale"] + [ROAR]),
     "EXHALE with the forge answering: a lowpass roar swelling 120 -> 280 Hz under it, at 0.8"),
    ("5 LOW", dict(segs=[(o, f0 / 2, f1 / 2, q, k, d, a, ty) for (o, f0, f1, q, k, d, a, ty) in BREATH["exhale"]]),
     "EXHALE an octave down (700 -> 175 Hz): a bigger bellows"),
    ("6 WHOOMPH", dict(segs=WHOOMPH),
     "round 2: the swell (lowpass 150 -> 300 Hz) and the huff on its top (lowpass 400 -> 150 Hz): the chamber's push"),
    ("7 BELLOWS", dict(segs=WHOOMPH + [NOZZLE["bellows"]]),
     "WHOOMPH with the nozzle's air over it: a thin band 3000 -> 2200 Hz (q 2) at 0.3, on the huff"),
    ("8 NOZZLE", dict(segs=[WHOOMPH[0], WHOOMPH[1], NOZZLE["nozzle"]]),
     "WHOOMPH with a thinner, higher nozzle: 3500 -> 2500 Hz (q 2.5) at 0.25"),
    ("9 FORGE", dict(segs=[WHOOMPH[0], WHOOMPH[1][:4] + (0.8,) + WHOOMPH[1][5:], NOZZLE["forge"]]),
     "BELLOWS with the huff at 0.8 and the nozzle lower, 2600 -> 1800 Hz: more air, less push"),
]
_half = [(o * 0.55, f0, f1, q, k, d * 0.55, a * 0.55, ty) for (o, f0, f1, q, k, d, a, ty) in BREATH["push"]]
CAST_CONTROLS = [
    ("0 TICK", dict(segs=BREATH["push"], burst=True),
     "PUSH's two bands as fixed-filter `_burst`s (instant attack): a strike, not a breath"),
    ("0 WHISTLE", dict(segs=BREATH["push"], q=14.0), "PUSH at q 14: a note, not air"),
    ("0 HISS", dict(segs=BREATH["push"], fx=8.0), "PUSH three octaves up (2.4 -> 9.6 kHz): a quench, not a bellows"),
    ("0 DOUBLE", dict(segs=_half + [(0.25 + s[0],) + s[1:] for s in _half]),
     "two half-length PUSH huffs 0.25 s apart: two breaths"),
    ("0 RUMBLE", dict(segs=[(o, round(f0 / 3), round(f1 / 3), q, k, d, a, ty) for (o, f0, f1, q, k, d, a, ty) in WHOOMPH]),
     "WHOOMPH an octave and a half down (50 -> 100 / 133 -> 50 Hz): a rumble, not a bellows"),
]


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
            L.append(f'this._sweep({tt}, {{ f0: {fmt(f0 * fx)}, f1: {fmt(f1 * fx)}, q: {fmt(q_)}, gain: {gx}, '
                     f'dur: {fmt(du)}, atk: {fmt(at)}, type:"{ty}" }});')
    return "\n".join(" " * ind + l for l in L)


# ============================================================ THE LANDING ===
# "a short iron thud (<=0.15s), pitched by sunder count".
LAND_CANDIDATES = [
    ("1 BOLT", dict(body="sine", punch=True, iron="bar", root=A2, steps="semi"),
     "a sine body under a falling punch, an iron bar mode (a triangle at 2.76x) and a contact click; a semitone a stack"),
    ("2 PLATE", dict(body="sine", punch=True, iron="plate", root=A2, steps="semi"),
     "BOLT with plate modes (sines at 1.59x and 2.14x) for its iron"),
    ("3 BLOCK", dict(body="triangle", punch=False, iron="bar", root=A2, steps="semi"),
     "a triangle body (no punch), the bar mode and the click: a harder, drier block"),
    ("4 DEEP", dict(body="sine", punch=True, iron="bar", root=A2 / 2, steps="semi"),
     "BOLT an octave down (A1 -> D2): a heavier bolt"),
    ("5 PENT", dict(body="sine", punch=True, iron="bar", root=A2, steps="pent"),
     "BOLT stepping A minor pentatonic (A2 C3 D3 E3 G3 A3): the count across an octave"),
    # ROUND 2 (see THE ROUNDS): on A2, with the iron a phone can hear the count by
    ("6 RING", dict(body="sine", punch=True, iron="ring", root=A2, steps="semi"),
     "round 2: BOLT with its bar mode as loud as the body and the bar's next mode (5.40x, a sine at 0.35)"),
    ("7 RINGING", dict(body="sine", punch=True, iron="ringl", root=A2, steps="semi"),
     "RING with the bar mode ringing 0.8 of the body's decay (not 0.5)"),
    ("8 HEAVY", dict(body="sine", punch=True, iron="heavy", root=A2, steps="semi"),
     "RING with the bar mode at 1.5x the body and the 5.40x mode at 0.5: more iron than thud"),
    ("9 BAR", dict(body="sine", punch=True, iron="bar1", root=A2, steps="semi"),
     "BOLT with its bar mode as loud as the body, and nothing else added"),
]
LAND_PARTS = ("punch", "body", "iron", "click")
IRON = {
    "bar": ['this._tone(t, { freq: f * 2.76, gain: g * 0.5, dur: D * 0.5, type:"triangle" }).frequency.value = f * 2.76;'],
    "plate": ['for (const [r, k] of [[1.59, 0.5], [2.14, 0.35]])',
              '  this._tone(t, { freq: f * r, gain: g * k, dur: D * 0.5, type:"sine" }).frequency.value = f * r;'],
    "ring": ['this._tone(t, { freq: f * 2.76, gain: g, dur: D * 0.5, type:"triangle" }).frequency.value = f * 2.76;',
             'this._tone(t, { freq: f * 5.4, gain: g * 0.35, dur: D * 0.35, type:"sine" }).frequency.value = f * 5.4;'],
    "ringl": ['this._tone(t, { freq: f * 2.76, gain: g, dur: D * 0.8, type:"triangle" }).frequency.value = f * 2.76;',
              'this._tone(t, { freq: f * 5.4, gain: g * 0.35, dur: D * 0.35, type:"sine" }).frequency.value = f * 5.4;'],
    "heavy": ['this._tone(t, { freq: f * 2.76, gain: g * 1.5, dur: D * 0.5, type:"triangle" }).frequency.value = f * 2.76;',
              'this._tone(t, { freq: f * 5.4, gain: g * 0.5, dur: D * 0.35, type:"sine" }).frequency.value = f * 5.4;'],
    "bar1": ['this._tone(t, { freq: f * 2.76, gain: g, dur: D * 0.5, type:"triangle" }).frequency.value = f * 2.76;'],
}


def note_of(sp, n):
    """The declared note of count n (0 = the miss's: one step under count 1)."""
    if n == 0:
        return sp["root"] * 2 ** (-UNDER[sp["steps"]] / 12)
    return sp["root"] * 2 ** (STEPS[sp["steps"]][n - 1] / 12)


def land_body(sp, g, D, parts=LAND_PARTS, fixed=None, dust=False, ind=10):
    """The thud's text. `fixed`: a constant note (the miss, and the FLAT
    control); otherwise the note is read off `p.n`, clamped to 1..CAP."""
    if fixed is not None:
        head = f"const f = {fmt(round(fixed, 2))}, g = {fmt(g)}, D = {fmt(D)};"
    elif sp["steps"] == "semi":
        head = (f"const n = clamp(Math.round(p.n || 1), 1, {CAP}), f = {fmt(sp['root'])} * Math.pow(2, (n - 1) / 12), "
                f"g = {fmt(g)}, D = {fmt(D)};")
    else:
        head = (f"const n = clamp(Math.round(p.n || 1), 1, {CAP}), "
                f"f = {fmt(sp['root'])} * Math.pow(2, [{', '.join(str(s) for s in STEPS[sp['steps']])}][n - 1] / 12), "
                f"g = {fmt(g)}, D = {fmt(D)};")
    L = [head]
    if "punch" in parts and sp["punch"]:
        L.append('this._tone(t, { freq: f * 2, to: f, gain: g * 0.6, dur: 0.03, type:"sine" });')
    if "body" in parts:
        L.append(f'this._tone(t, {{ freq: f, gain: g, dur: D, type:"{sp["body"]}" }}).frequency.value = f;')
    if "iron" in parts:
        L += IRON[sp["iron"]]
    if "click" in parts:
        L.append('this._burst(t, { freq: 2500, q: 1.2, gain: g * 0.4, dur: 0.012, type:"bandpass" });')
    if dust:
        L.append('this._sweep(t, { f0: 900, f1: 300, q: 0.7, gain: g * 0.5, dur: 0.09, atk: 0.015, type:"lowpass" });')
    return "\n".join(" " * ind + l for l in L)


# =============================================================== THE MISS ===
# "a quieter thud": the picked landing's own parts, at count 0's note.
MISS_CANDIDATES = [
    ("1 SAME", dict(parts=LAND_PARTS), "the landing's own thud at count 0's note, 6 dB under"),
    ("2 DULL", dict(parts=("punch", "body", "click")), "the thud without its iron: the bolt into the floor, not the foe"),
    ("3 DEAD", dict(parts=("punch", "body")), "DULL without the contact click: the floor takes it"),
    ("4 DUST", dict(parts=("punch", "body", "click"), dust=True), "DULL with a short lowpass dust puff (90 ms)"),
]
MISS_CONTROLS = [
    ("0 LOUD", dict(parts=LAND_PARTS, db=0.0), "SAME at the landing's own level"),
    ("0 FAINT", dict(parts=LAND_PARTS, db=-30.0), "SAME 30 dB under the landing"),
    ("0 HISS", dict(hiss=True), "a noise puff (a 3.5 kHz band, 80 ms): not a thud"),
]
HISS_BODY = 'this._burst(t, { freq: 3500, q: 0.9, gain: g, dur: 0.08, type:"bandpass" });'


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
SFX_ANCHOR = '        } else {                                        // rune-crack'
LAND_ANCHOR = '      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }'
MISS_ANCHOR = ('      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; '
               'continue; }')

LAND_CODE = LAND_ANCHOR + '''
      /* QUARRELSTORM'S LANDING (v83 §4: "a landing -- a short iron thud
         (<=0.15s), pitched by sunder count"): one thud per landed bolt,
         after its hurt and its sunder, pitched by the count the foe now
         carries -- the number its tag shows, 1-6. A killing landing thuds
         too, under the death voice. Presentation only: SFX.play draws
         nothing, is a no-op headless, and nothing here is read back
         (ironhail_voice_lab: fights identical). */
      SFX.play("ult", { w: "ironhail-land", n: foe.stacks("sunder") });'''

MISS_CODE = '''      /* QUARRELSTORM'S MISS (v83 §4: "a miss -- a quieter thud"): the next
         line's own test, read here first -- a read of foe.alive and two
         positions, and the anchor guards it (if that line changes, this row
         stops applying) -- so a bolt the sim counts as missed thuds once,
         on its landing frame, a bolt falling on the step its foe died
         included. Presentation only; nothing here is read back. */
      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R))
        SFX.play("ult", { w: "ironhail-miss" });
''' + MISS_ANCHOR

# the sim-write control: the same landing row with the foe nudged 1e-9 on a landing
LAND_CODE_BAD = LAND_CODE.replace(
    '      SFX.play("ult", { w: "ironhail-land"',
    '      foe.vx += 1e-9;\n      SFX.play("ult", { w: "ironhail-land"', 1)

_refuse(LAND_CODE + MISS_CODE, "sim rows")
for _c, _a in ((LAND_CODE, LAND_ANCHOR), (MISS_CODE, MISS_ANCHOR)):
    assert _c.count(_a) == 1, "a sim row must re-emit its anchor exactly once"


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


def arms_code(C_, L_, M_, info):
    cn, ln, mn = (X["name"].split()[1] for X in (C_, L_, M_))
    c_cast = _wrap([
        f'IRONHAIL\'S CAST, THE BELLOWS -- v83 §4: "cast -- a forge-bellows huff, 0.4s". {cn}, of '
        f'{info["n_cast"]}, picked on the numbers by `ironhail_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v108). Ironhail had no arm and fell through to rune-crack, which {info["n_rc"]} other '
        f'relics on its stage-5 link still used, so this ADDS arms before that fallback and leaves it alone.',
        f"{info['c_what']} {info['c_how']}: it swells to its top (the last 10 -> 90% in {info['c_rise']:.0f} ms), "
        f"never dips on the way up "
        f"and never grows again after its top; its power centres at {info['c_cen0']:.0f}-{info['c_cen1']:.0f} "
        f"Hz on every noise draw (a bellows, not a quench's hiss), and no peak stands more than "
        f"{info['c_tonal']:.1f} dB over its neighbours (air, not a note). Audible {info['c_aud']:.0f} ms; "
        f"its loudest 50 ms {info['c_top']:+.1f} dB re Ironhail's blow. Register at most "
        f"{info['c_reg']:.2f} against rune-crack, the dwarven and bow casts, the tornado's woosh, the "
        f"bowstring, the blow and the death voice."], 10)
    c_land = _wrap([
        f'A BOLT LANDS -- "a landing -- a short iron thud (<=0.15s), pitched by sunder count" (v83 §4). '
        f'{ln}, of {info["n_land"]} (`ironhail_voice_lab.py`). `tickHail` plays it once per landed bolt, '
        f'after its hurt and its sunder, with n = the foe\'s sunder count (the tag\'s number, 1-{CAP}).',
        f"{info['l_what']} The note steps up with the count, {info['l_notes']} Hz at 1-{CAP} (measured "
        f"within {info['l_err']:.0f} cents). Rise "
        f"{'under 1' if info['l_rise'] < 1 else format(info['l_rise'], '.0f')} ms; gone by {info['l_gone']:.0f} ms "
        f"at every count and draw; {info['l_low']:.2f} of its power under 400 Hz at the worst; its iron "
        f"partial {info['l_iron']:.0f} cents off every harmonic; its loudest 50 ms {info['l_db0']:+.1f} to "
        f"{info['l_db1']:+.1f} dB re the blow. On a phone (nothing under 200 Hz) the count is its iron, "
        f"{info['l_pp']} Hz, {info['l_pnote']:+.1f} dB or more over the score's p90. Register at most "
        f"{info['l_reg']:.2f} against the blow, the clank, the bowstring, the death voice, rune-crack and the "
        f"cast."], 10)
    c_miss = _wrap([
        f'A BOLT MISSES -- "a miss -- a quieter thud" (v83 §4). {mn}, of {info["n_miss"]} '
        f'(`ironhail_voice_lab.py`): {info["m_what"]}, at count 0\'s note ({info["m_f"]:.1f} Hz, one step '
        f'under a first landing -- a miss sunders nothing). {info["m_under"]:.1f} dB under the quietest '
        f'landing on its loudest draw, gone by {info["m_gone"]:.0f} ms, {info["m_low"]:.2f} of its power under '
        f'400 Hz, {info["m_heard"]:+.1f} dB over the score in its loudest third-octave over 200 Hz (where a phone '
        f'hears it); register at most '
        f'{info["m_reg"]:.2f} against the blow, the clank, the bowstring, the death voice, rune-crack and the '
        f'cast. `tickHail` plays it once per missed bolt. The close plays nothing (v83 §4).'], 10)
    return (f'{_arm_head(ME, "the bellows huff")}\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["s"])}\n'
            f'{_arm_head(ME + "-land", "a bolt lands")}\n'
            f'{c_land}\n{land_body(L_["sp"], L_["g"], L_["D"])}\n'
            f'{_arm_head(ME + "-miss", "a bolt falls short")}\n'
            f'{c_miss}\n{land_body(L_["sp"], M_["g"], L_["D"], parts=M_["sp"]["parts"], fixed=M_["f"], dust=M_["sp"].get("dust", False))}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# The tickHail rows, applied to the real prototype and run beside the original;
# the survey of Quarrelstorm's windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "ironhail";
  const CAP = AC.STATUS.sunder.maxStacks;
  const orig = P.tickHail; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickHail anchor occurs ${at} times in tickHail()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inH = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        calls.push({ step, k: w, n: p.n === undefined ? null : p.n, fs: foe.stacks("sunder"), alive: foe.alive,
                     inH: !!inH, keys: Object.keys(p).join(",") });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    P.tickHail = function(dt){ inH++; try { return impl.call(this, dt); } finally { inH--; } };
    const landSteps = {}, missSteps = {}, castSteps = {}, wins = [];
    let n = 0, ll = 0, lm = 0, lc = 0, prev = null, W = null;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const T = f.hailTally, Z = f.ultHail;
        if (T){
          if (T.landed > ll){ landSteps[step] = T.landed - ll; ll = T.landed; }
          if (T.missed > lm){ missSteps[step] = T.missed - lm; lm = T.missed; }
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
    } finally { P.tickHail = orig; if (had) S.play = op; else delete S.play; }
    const T = f.hailTally || {};
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.shield, m.b.shield, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.a.vx, m.a.vy, m.b.vx, m.b.vy, m.a.charge, m.b.charge,
                                  m.a.stacks("sunder"), m.b.stacks("sunder"), m.hail.length,
                                  m.winner ? m.winner.w.id : null, T]),
             calls, other: JSON.stringify(other), landSteps, missSteps, castSteps, wins, T, steps: n };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, castV = 0, land = 0, landV = 0, miss = 0, missV = 0, fatalLand = 0, deadMiss = 0, atCap = 0;
  const nh = new Array(CAP + 1).fill(0), pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a landing or miss voice"]);
    for (const c of B.calls) if (c.k !== ME && !c.inH) bad.push([fid, sd, "a hail voice outside tickHail", c.k]);
    const byStep = {};
    for (const c of B.calls) (byStep[c.step] = byStep[c.step] || []).push(c);
    const keys = new Set([...Object.keys(B.landSteps), ...Object.keys(B.missSteps), ...Object.keys(B.castSteps),
                          ...Object.keys(byStep)]);
    for (const k of keys){
      const cs = byStep[k] || [];
      const lv = cs.filter(c => c.k === ME + "-land"), mv = cs.filter(c => c.k === ME + "-miss"),
            cv = cs.filter(c => c.k === ME);
      const nl = B.landSteps[k] || 0, nm = B.missSteps[k] || 0, nc = B.castSteps[k] || 0;
      if (lv.length !== nl || mv.length !== nm || cv.length !== nc)
        bad.push([fid, sd, "step " + k, "land", nl, lv.length, "miss", nm, mv.length, "cast", nc, cv.length]);
      for (const c of lv){
        if (!(Number.isInteger(c.n) && c.n >= 1 && c.n <= CAP && c.n === c.fs) || c.keys !== "w,n")
          bad.push([fid, sd, "a landing voice's n is not the foe's count", c.n, c.fs, c.keys]);
        else nh[c.n]++;
        if (!c.alive) fatalLand++;
      }
      for (const c of mv){
        if (c.n !== null || c.keys !== "w") bad.push([fid, sd, "a miss voice carries opts", c.keys]);
        if (!c.alive) deadMiss++;
      }
      for (const c of cv) if (c.keys !== "w") bad.push([fid, sd, "the cast carries opts", c.keys]);
      land += nl; landV += lv.length; miss += nm; missV += mv.length; casts += nc; castV += cv.length;
    }
    for (const W of B.wins){
      ends[W.end]++;
      if (W.end === "clock"){
        const hi = W.endStep + 60;
        const nl = Object.keys(B.landSteps).filter(s => +s >= W.castStep && +s <= hi).length;
        const nm = Object.keys(B.missSteps).filter(s => +s >= W.castStep && +s <= hi).length;
        pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, land: nl, miss: nm });
      }
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, land, landV, miss, missV,
           fatalLand, deadMiss, nh, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Quarrelstorm's.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "ironhail";
  const orig = P.tickHail; let src = orig.toString();
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
  P.tickHail = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickHail = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, ME = "ironhail";
  const CAP = AC.STATUS.sunder.maxStacks;
  const res = [];
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.n === undefined ? null : p.n, foe.stacks("sunder")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { if (had) S.play = op; else delete S.play; }
    const T = f.hailTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                    m.a.stacks("sunder"), m.b.stacks("sunder"),
                                    m.winner ? m.winner.w.id : null, f.hailTally || null]),
               casts: T.casts || 0, landed: T.landed || 0, missed: T.missed || 0,
               castV: log.filter(e => e[0] === ME).length,
               landV: log.filter(e => e[0] === ME + "-land").length,
               badN: log.filter(e => e[0] === ME + "-land" && (e[1] !== e[2] || e[1] < 1 || e[1] > CAP)).length,
               missV: log.filter(e => e[0] === ME + "-miss").length,
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
  for (const [k, kind, p] of [["cast", "ult", { w: "ironhail" }], ["land", "ult", { w: "ironhail-land", n: 3 }],
                              ["miss", "ult", { w: "ironhail-miss" }], ["hit", "hit", { dmg: 16.23, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def breath(draws, aud_a0, aud_ms):
    """BREATH-RISE (ms), DIPS and REGROW (dB) on the draw-averaged envelopes
    (see the docstring), inside AUDIBLE."""
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


def heard(x, p90, win=0.1, lo=PHONE_HZ, hi=12000.0):
    """HEARD: the loudest ratio of the voice's third-octaves (centred at or
    above `lo`: round 2) over its first `win` s to the score's p90 in the same
    third-octave, dB, and where."""
    y = x[int(T0 * SR):int(T0 * SR) + int(win * SR)]
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


def phone_note(x, p90):
    """PHONE-PITCH (the FFT peak 200-2000 Hz over 30-130 ms) and PHONE-NOTE
    (its third-octave over the first 100 ms against the score's p90, dB)."""
    np = _np()
    pp = pitch(x, T0 + 0.03, T0 + 0.13, lo=PHONE_HZ, hi=2000.0)
    i = int(np.argmin([abs(math.log(fc / pp)) for fc in BANDS]))
    b = bands(x[int(T0 * SR):int((T0 + 0.1) * SR)])
    return pp, db(b[i] / max(p90[i], 1e-12))


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v83 §4 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'a huff' (a breath): BREATH-RISE >= 40 ms, the "
    "loudest 50 ms centred >= 80 ms in, no DIP on the way up and no REGROW >= 2 "
    "dB after its top (one breath), TONAL <= 10 dB (air, not a note); 'forge-"
    "bellows': the power CENTROID 150-2000 Hz on every draw (not a quench's "
    "hiss, not a rumble). Register against rune-crack, the school's casts and "
    "the type's (read off the page), the tornado's woosh, the bowstring, the "
    "hit @ 16.23 and the death voice each <= 0.80. Level: TOP between 0.5x the "
    "hit @ 16.23's loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST, "
    "on every draw (heard like a blow, never over one). Tiebreak: the most "
    "distinct register (the highest of those, to 0.05), then the fewest calls.")

LAND_RULE = (
    "'short (<=0.15s)': GONE <= 150 ms at every count on every draw; 'a thud': "
    "RISE <= 5 ms and the peak in the first 15 ms at every count, LOW400 >= 0.50 "
    "at every count on every draw; 'iron': METAL on the body pitch (30-90 ms) at "
    "every count; 'pitched by sunder count': the BODY PITCH within 25 cents of "
    "its declared note at every count 1-6, rising with every count; heard: "
    "loudest 50 ms between 0.5x the hit @ 16.23's loudest draw and 1.0x its "
    "quietest at every count on every draw, and HEARD (at or above 200 Hz) >= +6 dB "
    "at every count; ON A PHONE (round 2): PHONE-PITCH rising >= 30 cents with "
    "every count and PHONE-NOTE >= +6 dB at every count. "
    "Register (at count 3) against the hit @ 16.23, the clank, the bowstring, the "
    "death voice, rune-crack and the picked cast each <= 0.80 (not a blow, not "
    "a parry, not the bow, not a death). Tiebreak: the most distinct register "
    "(to 0.05), then the count heard best (the largest smallest step between "
    "neighbouring counts, to 10 cents), then the fewest calls.")

MISS_RULE = (
    "'a thud': GONE <= 150 ms, RISE <= 5 ms, the peak in the first 15 ms, LOW400 "
    ">= 0.50 on every draw; 'quieter': its loudest 50 ms on its LOUDEST draw at "
    "least 3 dB under the landing's quietest count on its QUIETEST draw; still "
    "heard: its loudest 50 ms >= 2x the wall tick's (loudest draw) on its "
    "quietest draw, HEARD (at or above 200 Hz) >= +6 dB, and (round 2) PHONE on "
    "its quietest draw >= the bowstring's on its loudest. Register against the hit @ 16.23, the "
    "clank, the bowstring, the death voice, rune-crack and the picked cast "
    "each <= 0.80 (against the landing: printed -- it IS a thud). Tiebreak: the "
    "most distinct register (to 0.05), then the fewest calls.")


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
    if M["brise"] < 40: why.append(f"breath-rise {M['brise']:.0f} ms < 40 (a strike)")
    if M["top_at"] * 1000 < 80: why.append(f"loudest 50 ms at {M['top_at'] * 1000:.0f} ms (< 80)")
    if M["dips"]: why.append(f"{M['dips']} dip(s) on the way up (not one breath)")
    if M["regrow"] >= 2: why.append(f"regrows {M['regrow']:.1f} dB after its top (not one breath)")
    if M["tonal"] > 10: why.append(f"tonal {M['tonal']:.1f} dB > 10 (a note)")
    if M["cen_lo"] < 150 or M["cen_hi"] > 2000:
        why.append(f"centroid {M['cen_lo']:.0f}-{M['cen_hi']:.0f} Hz, not 150-2000")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (quietest draw)")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (loudest draw)")
    return why


def land_why(M, lev):
    why = []
    if M["gone_max"] > GONE_MAX: why.append(f"gone at {M['gone_max']:.0f} ms (> {GONE_MAX:.0f})")
    if M["rise_max"] > 5: why.append(f"rise {M['rise_max']:.0f} ms")
    if M["pk_max"] > 15: why.append(f"peak at {M['pk_max']:.0f} ms")
    if M["low_min"] < 0.50: why.append(f"low400 {M['low_min']:.2f} < 0.50 (not a thud)")
    if M["iron_c"] < 60 or M["iron_db"] < -20:
        why.append(f"not iron: its partial {M['iron_c']:.0f} c from a harmonic, {M['iron_db']:+.0f} dB (worst count)")
    if M["perr"] > 25: why.append(f"a count's pitch {M['perr']:.0f} cents off its note")
    if not M["rising"]: why.append("the pitch does not rise with every count")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    if not M["prise"]: why.append("on a phone the count does not rise (" +
                                  "/".join(f"{p_:.0f}" for p_ in M["ppitch"]) + " Hz)")
    if M["pnote"] < 6: why.append(f"on a phone the count's note is {M['pnote']:+.1f} dB over the score (< +6)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def miss_why(M, lev):
    why = []
    if M["gone_max"] > GONE_MAX: why.append(f"gone at {M['gone_max']:.0f} ms (> {GONE_MAX:.0f})")
    if M["rise_max"] > 5: why.append(f"rise {M['rise_max']:.0f} ms")
    if M["pk_max"] > 15: why.append(f"peak at {M['pk_max']:.0f} ms")
    if M["low_min"] < 0.50: why.append(f"low400 {M['low_min']:.2f} < 0.50 (not a thud)")
    if M["under"] > -3: why.append(f"only {M['under']:+.1f} dB re the quietest landing (not quieter)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (2x the wall)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    if M["phone_lo"] < lev["phone"]:
        why.append(f"phone {M['phone_lo']:.5f} < the bowstring's {lev['phone']:.5f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Ironhail's stage 3 (the hail and its sunder)")
    ap.add_argument("--out", default="../05-reference/v108")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=108601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "land": LAND_RULE, "miss": MISS_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickHail landing", LAND_ANCHOR), ("tickHail miss", MISS_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    # (the renderer's own `u.w === "ironhail"` / `b.w === "ironhail"` -- the old nova's
    # picture -- is not a voice: only a bare `w === "ironhail"`, play()'s own spelling, is)
    if '"ironhail-land"' in html or '"ironhail-miss"' in html or re.search(r'(?<![\w.])w === "ironhail"', html):
        raise SystemExit(f"{gp.name} already carries Quarrelstorm's voices -- run on the stage-3 link")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nQUARRELSTORM -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
          const me = AC.WEAPONS.find(w => w.id === "ironhail");
          return { arms, kinds, cap: AC.STATUS.sunder.maxStacks, dmg: me.dmg, u: me.ult,
                   W: AC.WEAPONS.map(w => [w.id, w.aff, w.shape]) };
        }""")
        if info0["cap"] != CAP:
            raise SystemExit(f"STATUS.sunder.maxStacks is {info0['cap']}, not {CAP}")
        if abs(info0["dmg"] - BLADE) > 1e-9 or info0["u"].get("kind") != "hail" or info0["u"].get("dropDmg") != DROP \
                or info0["u"].get("sunder") != 1:
            raise SystemExit(f"Ironhail on this page is not stage 3's: dmg {info0['dmg']}, ult {info0['u']}")
        print(f"  Ironhail: blade {info0['dmg']}, ult {info0['u']['kind']} dropDmg {info0['u']['dropDmg']} sunder "
              f"{info0['u']['sunder']} fallT {info0['u']['fallT']} dropCd {info0['u']['dropCd']}; sunder cap {CAP}")
        arms_now = set(info0["arms"])
        SCHOOL = tuple(w for w, aff, sh in info0["W"] if aff == "dwarven" and w != ME and w in arms_now)
        TYPE = tuple(w for w, aff, sh in info0["W"] if sh == "bow" and w != ME and w in arms_now)
        FALL = tuple(w for w, aff, sh in info0["W"] if w not in arms_now)
        print(f"  the school's casts (dwarven, with an arm): {', '.join(SCHOOL)};  the type's (bow): {', '.join(TYPE)}")
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
                ("hit@16.23", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("hit@4", ["play", T0, "hit", {"dmg": DROP, "crit": False}]),
                ("wall", ["play", T0, "wall", {}]),
                ("death", ["play", T0, "death", {}]),
                ("clank", ["play", T0, "clank", {"mass": 3}]),
                ("loose", ["play", T0, "loose", {}]),
                ("woosh", ["play", T0, "scour-woosh", {"n": 0}])]
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
        if max(fall.values()) > 1e-6 or ME not in fall:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        n_rc = len(FALL) - 1
        # the noise draws
        DKEYS = ("hit@16.23", "hit@4", "wall", "rune-crack", "death", "clank", "loose", "woosh") + SCHOOL + TYPE
        D = {k: [] for k in DKEYS}
        for sd in NOISE_SEEDS:
            for k in D:
                x_ = R([dict(REFS)[k]], seed=sd)[0]
                D[k].append(dict(basic(x_), phone=phone(x_)))
        h_lo, h_hi = min(m["top"] for m in D["hit@16.23"]), max(m["top"] for m in D["hit@16.23"])
        h_ph = min(m["phone"] for m in D["hit@16.23"])      # PHONE: the blow's on its quietest draw
        l_ph = max(m["phone"] for m in D["loose"])          # the bowstring's on its loudest (the floor)
        print(f"  PHONE (the TOP over 200 Hz): the hit @ 16.23 {h_ph:.4f} (quietest draw), the bowstring {l_ph:.5f} "
              f"(loudest draw) = {db(l_ph / h_ph):+.1f} dB re the blow")
        w_hi = max(m["top"] for m in D["wall"])
        h4 = [m["top"] for m in D["hit@4"]]
        print(f"  the hit @ 16.23 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f};  the wall tick "
              f"{min(m['top'] for m in D['wall']):.4f}-{w_hi:.4f};  the engine's hit @ 4 (a landing's damage) "
              f"{min(h4):.4f}-{max(h4):.4f} = {db(min(h4) / h_lo):+.1f} to {db(max(h4) / h_hi):+.1f} dB re the blow")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        P90 = bed_p90(bseg)

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        def reg_to(DB, DB2):
            return float(np.median([cos(DB[i], DB2[i]) for i in range(len(DB))]))

        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, hit4=[min(h4), max(h4)], hit_phone=h_ph, loose_phone=l_ph)
        wav("ironhail-ctl-runecrack.wav", rcx)
        wav("ironhail-ctl-hit16.wav", ctl["hit@16.23"]["x"])
        wav("ironhail-ctl-woosh.wav", ctl["woosh"]["x"])
        wav("ironhail-ctl-loose.wav", ctl["loose"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a forge-bellows huff, 0.4s'. Level-matched: TOP {tgt_c:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the time scale solved to AUDIBLE {CAST_AUD:g} ms. "
              f"'phone' = PHONE dB re the blow's (printed, not gated)")

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

        CREFS = ("rune-crack",) + SCHOOL + TYPE + ("woosh", "loose", "hit@16.23", "death")

        def cast_metrics(M, draws):
            bs = [basic(d_) for d_ in draws]
            M["top_lo"] = min(b_["top"] for b_ in bs); M["top_hi"] = max(b_["top"] for b_ in bs)
            cens = [centroid(d_) for d_ in draws]
            M["cen_lo"], M["cen_hi"] = min(cens), max(cens)
            M["brise"], M["dips"], M["regrow"] = breath(draws, M["a0"], M["aud"])
            M["tonal"] = tonal(draws, T0 + M["a0"] / 1000, T0 + (M["a0"] + M["aud"]) / 1000, 100.0, 8000.0)
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
        abbr.update({"rune-crack": "rc", "hit@16.23": "hit", "death": "dth"})
        print(f"  {'cand':<10}{'g':>7}{'s':>6}{'calls':>6}{'top':>16}{'aud':>5}{'@top':>5}{'brise':>6}{'dips':>5}"
              f"{'regr':>5}{'tonal':>6}{'centroid':>12}{'phone':>6}" + "".join(f"{abbr[k]:>5}" for k in CREFS))

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>7.4g}{M['s']:>6.3g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}"
                  f"{M['aud']:>5.0f}{M['top_at'] * 1000:>5.0f}{M['brise']:>6.0f}{M['dips']:>5d}{M['regrow']:>5.1f}"
                  f"{M['tonal']:>6.1f}{M['cen_lo']:>6.0f}-{M['cen_hi']:<5.0f}{db(M['phone_lo'] / h_ph):>+6.1f}"
                  + "".join(f"{r_[k]:>5.2f}" for k in CREFS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, s = calib_cast(sp)
            M = cast_measure(sp, g, s, name)
            rows_c.append(M); cast_line(M)
            wav(f"ironhail-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for name, sp, blurb in CAST_CONTROLS:
            g, s = calib_cast(sp)
            M = cast_measure(sp, g, s, name)
            ctlc.append(M); cast_line(M)
            wav(f"ironhail-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for name, ev in (("0 WOOSH", ["play", T0, "scour-woosh", {"n": 0}]),
                         ("0 RC-NOW", ["play", T0, "ult", {"w": ME}])):
            x, calls = R([ev])
            M = basic(x); M.update(x=x, calls=calls[0], g=0.0, s=0.0, name=name, sp=None)
            cast_metrics(M, [R([ev], seed=sd)[0] for sd in NOISE_SEEDS])
            M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES + CAST_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print("    0 WOOSH    `scour-woosh` (the tornado) played as the cast -- a control\n"
              "    0 RC-NOW   what ult/ironhail plays today (rune-crack) -- a control")
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
        print(f"  PICK  {C_['name']}  g {C_['g']}, s {C_['s']}; {C_['calls']} synth calls; TOP "
              f"{db(C_['top_lo'] / h_lo):+.1f} to {db(C_['top_hi'] / h_lo):+.1f} dB re the hit @ 16.23 (quietest "
              f"draw), {db(C_['top_lo'] / w_hi):+.1f} dB or more re the wall")

        # ---- THE LANDING ---------------------------------------------------
        lev_l = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_l = math.sqrt(lev_l["lo"] * lev_l["hi"])
        print(f"\nLANDING -- 'a short iron thud (<=0.15s), pitched by sunder count'. Level-matched: TOP {tgt_l:.4f} at "
              f"count {LAND_REF_N} (the centre of {lev_l['lo']:.4f}-{lev_l['hi']:.4f}), the decay solved to GONE "
              f"{LAND_GONE:g} ms at count 1. 'heard' at or above 200 Hz")

        def lx(sp, g, D_, n, parts=LAND_PARTS, fixed=None, dust=False, seed=None):
            return R([["body", T0, land_body(sp, g, D_, parts, fixed, dust), {"n": n}]], secs=2.0, seed=seed)

        def calib_land(sp, parts=LAND_PARTS, fixD=None):
            g, D_ = 0.3, 0.25 if fixD is None else fixD
            for _ in range(3):
                if fixD is None and "body" in parts:
                    lo_, hi_ = math.log(0.03), math.log(1.5)
                    for _ in range(12):
                        mid = 0.5 * (lo_ + hi_)
                        if basic(lx(sp, g, math.exp(mid), 1, parts)[0])["gone"] < LAND_GONE: lo_ = mid
                        else: hi_ = mid
                    D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = float(f"{g * tgt_l / basic(lx(sp, g, D_, LAND_REF_N, parts)[0])['top']:.4g}")
            return g, D_

        LREFS = ("hit@16.23", "clank", "loose", "death", "rune-crack")

        def land_measure(rfn, name, sp, g, D_, calls, notes):
            """rfn(n, seed) -> the voice at count n. `notes`: the declared note
            of each count (None: no declared pitch)."""
            M = {"name": name, "sp": sp, "g": g, "D": D_, "calls": calls}
            xs, pit, tops, gones, rises, pks, lows, irons, hrd = {}, [], [], [], [], [], [], [], []
            ppit, pnotes, phs = [], [], []
            for n in COUNTS:
                x = rfn(n, None)
                if float(np.abs(x - rfn(n, None)).max()) > TOL:
                    raise SystemExit(f"landing {name} does not reproduce")
                xs[n] = x
                b_ = basic(x)
                rises.append(b_["rise"]); pks.append(b_["pk_ms"])
                p_ = pitch(x, T0 + 0.03, T0 + 0.13, lo=40, hi=400)
                pit.append(p_)
                r_, c_, d_ = inharm(x, T0 + 0.03, T0 + 0.09, p_)
                irons.append((c_, d_, r_))
                hrd.append(heard(x, P90))
                pp_, pn_ = phone_note(x, P90)
                ppit.append(pp_); pnotes.append(pn_)
                draws = [rfn(n, sd) for sd in NOISE_SEEDS]
                for d0 in [x] + draws:
                    bd = basic(d0)
                    tops.append(bd["top"]); gones.append(bd["gone"]); lows.append(low_share(d0, 400.0))
                    phs.append(phone(d0))
                if n == LAND_REF_N:
                    M["DB"] = [bands(d0[int(T0 * SR):]) for d0 in draws]
            M.update(xs=xs, x=xs[LAND_REF_N], pitch=pit, top_lo=min(tops), top_hi=max(tops), gone_max=max(gones),
                     rise_max=max(rises), pk_max=max(pks), low_min=min(lows),
                     iron_c=min(i_[0] for i_ in irons), iron_db=min(i_[1] for i_ in irons),
                     iron_r=[i_[2] for i_ in irons], heard=min(h_[0] for h_ in hrd), heard_at=[h_[1] for h_ in hrd],
                     heard_all=[h_[0] for h_ in hrd], ppitch=ppit, pnote=min(pnotes), pnote_all=pnotes,
                     prise=all(ppit[i + 1] > ppit[i] * 2 ** (30 / 1200) for i in range(len(ppit) - 1)),
                     phone_lo=min(phs))
            if notes is None:
                M["perr"] = 999.0
            else:
                M["perr"] = max(abs(cents(p_, f_)) for p_, f_ in zip(pit, notes))
            M["rising"] = all(pit[i + 1] > pit[i] * 2 ** (30 / 1200) for i in range(len(pit) - 1))
            M["minstep"] = min(cents(pit[i + 1], pit[i]) for i in range(len(pit) - 1))
            M["regs"] = {k: reg(M["DB"], k) for k in LREFS}
            M["regs"]["cast"] = reg_to(M["DB"], C_["DB"])
            M["why"] = land_why(M, lev_l)
            return M

        print(f"  {'cand':<9}{'g':>7}{'D':>6}{'calls':>6}{'top':>16}{'gone':>5}{'rise':>5}{'pk@':>4}{'low4':>6}"
              f"{'iron c/dB':>11}{'pitch Hz (count 1-6)':>38}{'err':>5}{'step':>5}{'heard':>7}"
              + "".join(f"{k[:4]:>5}" for k in ("hit", "clank", "loose", "dth", "rc", "cast")))

        def land_line(M):
            r_ = M["regs"]
            ps = "/".join(f"{p_:.0f}" for p_ in M["pitch"])
            print(f"  {M['name']:<9}{M['g']:>7.4g}{M['D']:>6.3g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}"
                  f"{M['gone_max']:>5.0f}{M['rise_max']:>5.0f}{M['pk_max']:>4.0f}{M['low_min']:>6.2f}"
                  f"{M['iron_c']:>6.0f}/{M['iron_db']:<+4.0f}{ps:>38}{min(M['perr'], 999):>5.0f}{M['minstep']:>5.0f}"
                  f"{M['heard']:>+7.1f}" +
                  "".join(f"{r_[k]:>5.2f}" for k in ("hit@16.23", "clank", "loose", "death", "rune-crack", "cast")))
            print(f"  {'':<9}  on a phone: PHONE {db(M['phone_lo'] / h_ph):+.1f} dB re the blow's; the count's note "
                  + "/".join(f"{p_:.0f}" for p_ in M["ppitch"]) + " Hz, over the score "
                  + " ".join(f"{v:+.1f}" for v in M["pnote_all"]) + " dB")

        rows_l = []
        for name, sp, blurb in LAND_CANDIDATES:
            g, D_ = calib_land(sp)
            calls = lx(sp, g, D_, 1)[1][0]
            M = land_measure(lambda n, sd, sp=sp, g=g, D_=D_: lx(sp, g, D_, n, seed=sd)[0], name, sp, g, D_, calls,
                             [note_of(sp, n) for n in COUNTS])
            rows_l.append(M); land_line(M)
            for n in (1, CAP):
                wav(f"ironhail-land-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        ctll = []
        s0 = rows_l[0]
        sp0 = s0["sp"]
        # FLAT: count 1's note for every count
        M = land_measure(lambda n, sd: lx(sp0, s0["g"], s0["D"], n, fixed=note_of(sp0, 1), seed=sd)[0], "0 FLAT", sp0,
                         s0["g"], s0["D"], s0["calls"], [note_of(sp0, n) for n in COUNTS])
        ctll.append(M)
        # LONG: ringing 0.45 s
        gL, _ = calib_land(sp0, fixD=0.45)
        M = land_measure(lambda n, sd: lx(sp0, gL, 0.45, n, seed=sd)[0], "0 LONG", sp0, gL, 0.45, s0["calls"],
                         [note_of(sp0, n) for n in COUNTS])
        ctll.append(M)
        # WOOD: no iron
        pw = ("punch", "body", "click")
        gW, DW = calib_land(sp0, pw)
        M = land_measure(lambda n, sd: lx(sp0, gW, DW, n, pw, seed=sd)[0], "0 WOOD", sp0, gW, DW,
                         lx(sp0, gW, DW, 1, pw)[1][0], [note_of(sp0, n) for n in COUNTS])
        ctll.append(M)
        # CLICK: the contact click alone
        pc = ("click",)
        gC, _ = calib_land(sp0, pc, fixD=s0["D"])
        M = land_measure(lambda n, sd: lx(sp0, gC, s0["D"], n, pc, seed=sd)[0], "0 CLICK", sp0, gC, s0["D"], 1,
                         [note_of(sp0, n) for n in COUNTS])
        ctll.append(M)
        # BLOW: the engine's hit at a landing's damage
        M = land_measure(lambda n, sd: R([["play", T0, "hit", {"dmg": DROP, "crit": False}]], secs=2.0, seed=sd)[0],
                         "0 BLOW", sp0, 0.0, 0.0, 2, [note_of(sp0, n) for n in COUNTS])
        ctll.append(M)
        for M in ctll:
            land_line(M)
            wav(f"ironhail-land-{M['name'].replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in LAND_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 FLAT    BOLT at count 1's note for every count -- a control\n"
              "    0 LONG    BOLT ringing 0.45 s -- a control\n"
              "    0 WOOD    BOLT without its iron -- a control\n"
              "    0 CLICK   BOLT's contact click alone -- a control\n"
              "    0 BLOW    the engine's hit at a landing's 4 damage -- a control")
        print(f"  RULE  {LAND_RULE}")
        for M in rows_l:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctll:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_l, "landing")
        li = fb if ok is None else min(ok, key=lambda i: (round(max(rows_l[i]["regs"].values()) / 0.05),
                                                          -round(rows_l[i]["minstep"] / 10), rows_l[i]["calls"]))
        L_ = rows_l[li]
        print(f"  PICK  {L_['name']}  g {L_['g']}, D {L_['D']}; notes " +
              " / ".join(f"{p_:.1f}" for p_ in L_["pitch"]) + f" Hz; loudest 50 ms {db(L_['top_lo'] / h_lo):+.1f} to "
              f"{db(L_['top_hi'] / h_lo):+.1f} dB re the hit @ 16.23 (quietest draw); heard "
              + " ".join(f"{h_:+.1f}@{f_:.0f}" for h_, f_ in zip(L_["heard_all"], L_["heard_at"])))

        # ---- THE MISS ------------------------------------------------------
        land_top_ref = basic(L_["xs"][LAND_REF_N])["top"]
        tgt_m = land_top_ref * 10 ** (-MISS_UNDER_DB / 20)
        f_miss = round(note_of(L_["sp"], 0), 2)
        lev_m = dict(lo=2 * w_hi, phone=l_ph)
        print(f"\nMISS -- 'a quieter thud'. The picked landing's parts at count 0's note ({f_miss} Hz), its decay "
              f"{L_['D']}; level-matched: TOP {tgt_m:.4f} ({MISS_UNDER_DB:g} dB under the landing's at count "
              f"{LAND_REF_N}). 'heard' at or above 200 Hz; 'phone' dB re the bowstring's PHONE (the floor)")

        def mx(parts, g, dust=False, hiss=False, seed=None):
            body = (f"const g = {fmt(g)};\n" + " " * 10 + HISS_BODY) if hiss else None
            if hiss:
                body = " " * 10 + body
                return R([["body", T0, body, {}]], secs=2.0, seed=seed)
            return R([["body", T0, land_body(L_["sp"], g, L_["D"], parts, f_miss, dust), {}]], secs=2.0, seed=seed)

        def calib_miss(sp, target):
            g = 0.1
            for _ in range(4):
                g = float(f"{g * target / basic(mx(sp.get('parts'), g, sp.get('dust', False), sp.get('hiss', False))[0])['top']:.4g}")
            return g

        MREFS = LREFS

        def miss_measure(sp, g, name):
            f_ = lambda sd: mx(sp.get("parts"), g, sp.get("dust", False), sp.get("hiss", False), seed=sd)  # noqa: E731
            x, calls = f_(None)
            if float(np.abs(x - f_(None)[0]).max()) > TOL:
                raise SystemExit(f"miss {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, name=name, sp=sp, f=f_miss)
            draws = [x] + [f_(sd)[0] for sd in NOISE_SEEDS]
            bs = [basic(d0) for d0 in draws]
            M.update(top_lo=min(b_["top"] for b_ in bs), top_hi=max(b_["top"] for b_ in bs),
                     gone_max=max(b_["gone"] for b_ in bs), rise_max=M["rise"], pk_max=M["pk_ms"],
                     low_min=min(low_share(d0, 400.0) for d0 in draws), phone_lo=min(phone(d0) for d0 in draws))
            M["under"] = db(M["top_hi"] / L_["top_lo"])
            M["heard"], M["heard_at"] = heard(x, P90)
            M["pitch"] = pitch(x, T0 + 0.03, T0 + 0.13, lo=40, hi=400)
            DB = [bands(d0[int(T0 * SR):]) for d0 in draws[1:]]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in MREFS}
            M["regs"]["cast"] = reg_to(DB, C_["DB"])
            M["reg_land"] = reg_to(DB, L_["DB"])
            M["why"] = miss_why(M, lev_m)
            return M

        print(f"  {'cand':<9}{'g':>8}{'calls':>6}{'top':>16}{'under':>7}{'gone':>5}{'rise':>5}{'pk@':>4}{'low4':>6}"
              f"{'pitch':>7}{'heard':>11}{'phone':>7}" + "".join(f"{k[:4]:>5}" for k in ("hit", "clank", "loose", "dth", "rc", "cast"))
              + f"{'land':>6}")

        def miss_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>8.4g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}{M['under']:>+7.1f}"
                  f"{M['gone_max']:>5.0f}{M['rise_max']:>5.0f}{M['pk_max']:>4.0f}{M['low_min']:>6.2f}{M['pitch']:>7.1f}"
                  f"{M['heard']:>+6.1f}@{M['heard_at']:<4.0f}{db(M['phone_lo'] / l_ph):>+7.1f}" +
                  "".join(f"{r_[k]:>5.2f}" for k in ("hit@16.23", "clank", "loose", "death", "rune-crack", "cast"))
                  + f"{M['reg_land']:>6.2f}")

        rows_m = []
        for name, sp, blurb in MISS_CANDIDATES:
            g = calib_miss(sp, tgt_m)
            M = miss_measure(sp, g, name)
            rows_m.append(M); miss_line(M)
            wav(f"ironhail-miss-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlm = []
        for name, sp, blurb in MISS_CONTROLS:
            g = calib_miss(sp, land_top_ref * 10 ** (sp["db"] / 20) if "db" in sp else tgt_m)
            M = miss_measure(sp, g, name)
            ctlm.append(M); miss_line(M)
            wav(f"ironhail-miss-{name.replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in MISS_CANDIDATES + MISS_CONTROLS:
            print(f"    {name:<9} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print(f"  RULE  {MISS_RULE}")
        for M in rows_m:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctlm:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_m, "miss")
        mi = fb if ok is None else min(ok, key=lambda i: (round(max(rows_m[i]["regs"].values()) / 0.05),
                                                          rows_m[i]["calls"]))
        M_ = rows_m[mi]
        print(f"  PICK  {M_['name']}  g {M_['g']}; {M_['under']:+.1f} dB re the quietest landing; loudest 50 ms "
              f"{db(M_['top_lo'] / w_hi):+.1f} dB or more re the wall; heard {M_['heard']:+.1f} dB at "
              f"{M_['heard_at']:.0f} Hz")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   landing {L_['name']}   miss {M_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        what_c = {"1 PUSH": "A breath whose band climbs 300 -> 1200 Hz as the boards press.",
                  "2 EXHALE": "A breath whose band falls 1400 -> 350 Hz as the air is let go.",
                  "3 ARC": "A breath that climbs 350 -> 1000 Hz and falls back to 400.",
                  "4 ROAR": "A breath whose band falls 1400 -> 350 Hz, and under it the forge answering, a lowpass "
                            "roar swelling 120 -> 280 Hz.",
                  "5 LOW": "A big breath whose band falls 700 -> 175 Hz.",
                  "6 WHOOMPH": "The bellows' chamber pushed: a swell of lowpassed air (its cutoff 150 -> 300 Hz) "
                               "and, on its top, the huff (400 -> 150 Hz).",
                  "7 BELLOWS": "The bellows' chamber pushed -- a swell of lowpassed air (its cutoff 150 -> 300 Hz) "
                               "and, on its top, the huff (400 -> 150 Hz) -- with the nozzle's air over the huff, a "
                               "thin band 3000 -> 2200 Hz (q 2) at 0.3.",
                  "8 NOZZLE": "The bellows' chamber pushed -- a swell of lowpassed air (its cutoff 150 -> 300 Hz) "
                              "and, on its top, the huff (400 -> 150 Hz) -- with the nozzle's air over the huff, a "
                              "thin band 3500 -> 2500 Hz (q 2.5) at 0.25.",
                  "9 FORGE": "The bellows' chamber pushed -- a swell of lowpassed air (its cutoff 150 -> 300 Hz) "
                             "and, on its top, the huff at 0.8 (400 -> 150 Hz) -- with the nozzle's air over the "
                             "huff, a thin band 2600 -> 1800 Hz (q 2) at 0.3."}[C_["name"]]
        how_c = ("Two overlapping sweeps make one breath, since one `_sweep` cannot outlast the noise buffer "
                 "(CLAUDE.md 4.5)" if int(C_["name"].split()[0]) <= 5 else
                 "The swell has the longest attack a `_sweep` allows and the huff peaks on its top and outlasts it -- "
                 "the one way two sweeps make one hump, since one `_sweep` cannot outlast the noise buffer "
                 "(CLAUDE.md 4.5)")
        iron_w = {"bar": "an iron bar mode (a triangle at 2.76x)", "plate": "iron plate modes (sines at 1.59x and 2.14x)",
                  "ring": "an iron bar struck -- its first mode (a triangle at 2.76x) as loud as the body, its second "
                          "(a sine at 5.40x) at 0.35 --",
                  "ringl": "an iron bar struck -- its first mode (a triangle at 2.76x) as loud as the body and ringing "
                           "0.8 of its decay, its second (a sine at 5.40x) at 0.35 --",
                  "heavy": "an iron bar struck hard -- its first mode (a triangle at 2.76x) at 1.5x the body, its "
                           "second (a sine at 5.40x) at 0.5 --",
                  "bar1": "an iron bar mode as loud as the body (a triangle at 2.76x)"}
        what_l = (f"A {L_['sp']['body']} body" + (" under a falling punch (its octave down to it, 30 ms)"
                                                   if L_["sp"]["punch"] else "") +
                  f", {iron_w[L_['sp']['iron']]} and a 12 ms 2.5 kHz contact click (the bolt meeting the foe).")
        what_m = {"1 SAME": "the landing's own thud", "2 DULL": "the landing's thud without its iron (a bolt into "
                  "the floor, not into the foe)", "3 DEAD": "the landing's body and punch alone (no iron, no click)",
                  "4 DUST": "the landing's thud without its iron, with a short lowpass dust puff"}[M_["name"]]
        info = dict(n_cast=len(CAST_CANDIDATES), n_land=len(LAND_CANDIDATES), n_miss=len(MISS_CANDIDATES), n_rc=n_rc,
                    c_what=what_c, c_how=how_c, c_rise=C_["brise"], c_cen0=C_["cen_lo"], c_cen1=C_["cen_hi"], c_tonal=C_["tonal"],
                    c_aud=C_["aud"], c_top=db(C_["top"] / h_lo), c_reg=max(C_["regs"].values()),
                    l_what=what_l, l_notes=" / ".join(f"{note_of(L_['sp'], n):.0f}" for n in COUNTS),
                    l_err=L_["perr"], l_rise=L_["rise_max"], l_gone=L_["gone_max"], l_low=L_["low_min"],
                    l_iron=L_["iron_c"], l_db0=db(L_["top_lo"] / h_lo), l_db1=db(L_["top_hi"] / h_lo),
                    l_heard=L_["heard"], l_reg=max(L_["regs"].values()), l_pnote=L_["pnote"],
                    l_pp=" / ".join(f"{p_:.0f}" for p_ in L_["ppitch"]),
                    m_what=what_m, m_f=f_miss, m_under=M_["under"], m_gone=M_["gone_max"], m_low=M_["low_min"],
                    m_heard=M_["heard"], m_reg=max(M_["regs"].values()))
        arms = arms_code(C_, L_, M_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        if arms.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx row does not re-emit its anchor exactly once")
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        lbt = land_body(L_["sp"], L_["g"], L_["D"])
        rp = [float(np.abs(R([["body", T0, lbt, {"n": CAP}]])[0] - R([["body", T0, lbt, {"n": CAP}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the loudest landing rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        cbt = cast_body(C_["sp"], C_["g"], C_["s"])
        mbt = land_body(L_["sp"], M_["g"], L_["D"], M_["sp"]["parts"], f_miss, M_["sp"].get("dust", False))
        for sd in (None, NOISE_SEEDS[5]):
            tag = "" if sd is None else "'"
            xa, _ = R([["arm", T0, "ult", {"w": ME}]], seed=sd, rows=sfx_rows)
            chk.append(("cast" + tag, float(np.abs(xa - R([["body", T0, cbt, {}]], seed=sd)[0]).max())))
            for n in (-1, 0, 1, 2, 3, 4, 5, 6, 9, None):
                p1 = {"w": ME + "-land"} if n is None else {"w": ME + "-land", "n": n}
                x1, _ = R([["arm", T0, "ult", p1]], seed=sd, rows=sfx_rows)
                nn = 1 if n is None else min(CAP, max(1, n))
                x2, _ = R([["body", T0, lbt, {"n": nn}]], seed=sd)
                chk.append((f"land@{n}{tag}", float(np.abs(x1 - x2).max())))
            xm, _ = R([["arm", T0, "ult", {"w": ME + "-miss"}]], seed=sd, rows=sfx_rows)
            chk.append(("miss" + tag, float(np.abs(xm - R([["body", T0, mbt, {}]], seed=sd)[0]).max())))
            if sd is None:
                xa0, xm0 = xa, xm
        print("  the arms vs the picked candidates, max |diff| (render.py's draw and a second): " +
              ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11.6, 16.23, 50) for c_ in (False, True)]
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
        now_rc = float(np.abs(xa0 - rcx).max())
        print(f"  ult/ironhail vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, repro=max(rp))

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
            evs = [("ult", {"w": ME}), ("ult", {"w": ME + "-miss"})] + [("ult", {"w": ME + "-land", "n": n}) for n in COUNTS]
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
                pr[w_] = [cos(bands(C_["x"][int(T0 * SR):]), bp), cos(bands(L_["xs"][LAND_REF_N][int(T0 * SR):]), bp),
                          cos(bands(M_["x"][int(T0 * SR):]), bp)]
            worst_p = max(((max(v), k) for k, v in pr.items()), default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both "
                  f"orders render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the cast / landing / miss against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) "
                  f"-- printed, not gated")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=pr))
        rec["peers"] = peers

        # ---- THE tickHail ROWS ---------------------------------------------
        trows = [[LAND_ANCHOR, LAND_CODE], [MISS_ANCHOR, MISS_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickHail ROWS, applied to Match.prototype.tickHail's own source, run beside the original on real "
              "fights (the mirror match is refused by Match -- 'A relic cannot fight itself'):")
        WR = page.evaluate(WIRE_JS, [seeds, trows])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Ironhail both sides x every foe x seeds {seeds}): {WR['same']}/{WR['fights']} "
              f"identical (over, clock, both hp, shields, positions, velocities, charges, both sunder counts, the "
              f"bolts in the air, winner, the whole hailTally); every other voice call identical in order, kind and "
              f"opts in {WR['otherSame']}/{WR['fights']}")
        nh = WR["nh"]
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['land']} landings -> "
              f"{WR['landV']} landing voices ({WR['fatalLand']} killing); {WR['miss']} misses -> {WR['missV']} miss "
              f"voices ({WR['deadMiss']} on the step the foe died); problems {WR['nbad']}")
        print("  the count a landing carries (the foe's sunder after it): " +
              ", ".join(f"{n}: {nh[n]}" for n in COUNTS) +
              f" ({100 * nh[CAP] / max(1, sum(nh)):.0f}% at the cap)")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["landV"] != WR["land"] or WR["missV"] != WR["miss"] or WR["castV"] != WR["casts"] \
                or WR["land"] == 0 or WR["miss"] == 0:
            FAILED.append("tickHail rows")
        WB = page.evaluate(WIRE_JS, [seeds, [[LAND_ANCHOR, LAND_CODE_BAD], trows[1]]])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a landing): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "land", "landV",
                                          "miss", "missV", "fatalLand", "deadMiss", "nh", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        print(f"  THE CLOSE: {WR['ends']['clock']} windows closed by their clock, {WR['ends']['death']} by a death and "
              f"{WR['ends']['over']} by the fight's end -- none plays anything (v83 §4: 'close -- nothing'; no row "
              f"touches the close line)")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted([w for w in WR["pick"] if w["miss"] > 0],
                      key=lambda w: (-w["land"], w["foe"], w["seed"], w["side"]))
        if cand:
            w_ = cand[0]
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
            ld = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == ME + "-land"]
            ms = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME + "-miss"]
            others_at = [(T0 + (e[0] - lo_t), e[1] + ("/" + e[2]["w"] if e[1] == "ult" and "w" in e[2] else ""))
                         for e in evs if not e[3]]

            def near(t_):
                return ", ".join(f"{k_} {1000 * (u_ - t_):+.0f} ms" for u_, k_ in others_at if -0.05 <= u_ - t_ <= 0.1)
            ct = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME]

            def ov(f, a_, d_):
                return db(band_rms(xw, f, a_, a_ + d_) / max(band_rms(xo, f, a_, a_ + d_), 1e-12))
            # ROUND 2: read over the voice's own TOP window (its first 50 ms -- a thud's loudest 50 ms is
            # its first), not 100 ms: round 2's first run read one landing +4.9 dB over 100 ms because
            # Cindercleave's fire jet started 58 ms AFTER it, inside the window -- a sound that starts
            # after the thud's loudest 50 ms cannot hide it. Both readings are printed.
            HW = 0.05
            l_over = [ov(L_["heard_at"][min(CAP, max(1, n)) - 1], t_, HW) for t_, n in ld]
            m_over = [ov(M_["heard_at"], t_, HW) for t_ in ms]
            l_100 = [ov(L_["heard_at"][min(CAP, max(1, n)) - 1], t_, 0.1) for t_, n in ld]
            m_100 = [ov(M_["heard_at"], t_, 0.1) for t_ in ms]
            bc = bands(C_["x"][int(T0 * SR):int((T0 + 0.4) * SR)])
            fc_c = max((v_, fc) for v_, fc in zip(bc, BANDS) if fc >= PHONE_HZ)[1]   # round 2: where a phone hears it
            c_over = [ov(fc_c, t_, 0.4) for t_ in ct]
            print(f"\nIN A REAL WINDOW -- ironhail v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {len(ld)} landings and {len(ms)} misses; the fight's "
                  f"own sounds and the score, with and without the three voices")
            print("  each landing over the fight in its loudest third-octave at or above 200 Hz, its first 50 ms: " +
                  " ".join(f"{v:+.1f}" for v in l_over) + " dB (counts " + " ".join(str(n) for _, n in ld) + ");"
                  "  over 100 ms: " + " ".join(f"{v:+.1f}" for v in l_100))
            print("  each miss, 50 ms: " + " ".join(f"{v:+.1f}" for v in m_over) + ";  100 ms: " +
                  " ".join(f"{v:+.1f}" for v in m_100) + f" dB;  the cast ({fc_c:.0f} Hz, 0.4 s): " +
                  " ".join(f"{v:+.1f}" for v in c_over) + " dB")
            for (t_, n), v1 in zip(ld, l_100):
                if v1 < 8:
                    print(f"    the landing at {t_ - T0 + lo_t:.3f}s (count {n}, {v1:+.1f} dB over 100 ms) shares its "
                          f"100 ms with: {near(t_) or 'nothing'}")
            for t_, v1 in zip(ms, m_100):
                if v1 < 5:
                    print(f"    the miss at {t_ - T0 + lo_t:.3f}s ({v1:+.1f} dB over 100 ms) shares its 100 ms with: "
                          f"{near(t_) or 'nothing'}")
            if (l_over and min(l_over) < 6) or (m_over and min(m_over) < 3) or (c_over and min(c_over) < 6):
                FAILED.append("a new voice not heard in a real window")
            wav("ironhail-pick-real-window.wav", xw)
            wav("ironhail-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, land_over=l_over, miss_over=m_over, cast_over=c_over, land_100=l_100,
                               miss_100=m_100,
                               counts=[n for _, n in ld])
        # the picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, n in enumerate(COUNTS):
            seq += [["arm", T0 + 0.8 + 0.4 * (2 * k_), "ult", {"w": ME + "-land", "n": n}],
                    ["arm", T0 + 0.8 + 0.4 * (2 * k_ + 1), "ult", {"w": ME + "-miss"}]]
        seq += [["arm", T0 + 6.0, "hit", {"dmg": BLADE, "crit": False}]]
        xq_, _ = R(seq, secs=8.0, rows=sfx_rows)
        wav("ironhail-pick-sequence.wav", xq_)

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_voices = [(k_, p_) for k_, p_ in others if k_ != "ult"][:36] + \
                     [("ult", {"w": w_}) for w_ in ult_ids if w_ in {w for w, _a, _s in info0["W"]}][:12]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [R([["play", T0, k_, p_]])[0] for k_, p_ in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
            assert not errors, errors[:3]
            e2e_ref["new"] = {"cast": C_["x"], "miss": M_["x"]}
            for n in COUNTS:
                e2e_ref["new"][f"land n{n}"] = L_["xs"][n]

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Ironhail's cast, landing and miss arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickHail: the landing voice, once per landed bolt, after its hurt and its sunder",
                 anchor=LAND_ANCHOR, mode="replace", code=LAND_CODE),
            dict(label="tickHail: the miss voice, once per missed bolt, before the miss line",
                 anchor=MISS_ANCHOR, mode="replace", code=MISS_CODE)]
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit("end to end: an anchor is not re-emitted exactly once")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="ironhail_e2e_"))
        try:
            tp = tmpd / "sc-ironhail-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the three rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            with game(game_path=tp) as (page, errors):
                def R2(evs, secs=3.0, seed=None):
                    r = page.evaluate(RENDER_JS, [evs, secs, seed, None])
                    assert not errors, errors[:3]
                    return pcm(r)
                vo = max(float(np.abs(R2([["play", T0, k_, p_]]) - x0).max())
                         for (k_, p_), x0 in zip(e2e_voices, e2e_ref["voices"]))
                NEWP = [("cast", {"w": ME}, 3.0), ("miss", {"w": ME + "-miss"}, 2.0)]
                NEWP += [(f"land n{n}", {"w": ME + "-land", "n": n}, 2.0) for n in COUNTS]
                nd = [(lab_, float(np.abs(R2([["play", T0, "ult", p_]], secs=s_) - e2e_ref["new"][lab_]).max()))
                      for lab_, p_, s_ in NEWP]
                rcp = R2([["play", T0, "ult", {"w": "spellbreaker"}]])
                not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
                F1 = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
                assert not errors, errors[:3]
                page_err = len(errors)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
        F0 = {f_["key"]: f_ for f_ in e2e_ref["fights"]}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        l_ok = sum(f_["landV"] == f_["landed"] and f_["badN"] == 0 for f_ in F1)
        m_ok = sum(f_["missV"] == f_["missed"] for f_ in F1)
        orig_new = sum(f_["landV"] + f_["missV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "landed", "missed", "castV", "landV", "missV")}
        print("  the three voices through the patched page's own SFX.play vs the lab's candidate text, max |diff|: " +
              ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/ironhail vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, landing voices = landings (n the foe's "
              f"count) {l_ok}, miss voices = misses {m_ok} (of {len(F1)}); totals {tot}; the original page played "
              f"{orig_new} landing/miss voices; page errors {page_err}")
        if max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1) or osame != len(F1) \
                or min(c_ok, l_ok, m_ok) != len(F1) or orig_new or page_err:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same,
                          other_same=osame, totals=tot)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB", "sp")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), land=strip(rows_l), land_controls=strip(ctll),
               miss=strip(rows_m), miss_controls=strip(ctlm), wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_s": C_["s"], "land": L_["name"], "land_g": L_["g"],
                     "land_D": L_["D"], "miss": M_["name"], "miss_g": M_["g"], "miss_f": f_miss})
    print(f"\nTHE PICKS  cast {C_['name']}   landing {L_['name']}   miss {M_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    # WHY each row is safe, in the numbers this run measured
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
        f"The three voices (v83 §4), in the synth only; the close has none. The arms are added BEFORE the shared "
        f"rune-crack fallback, and the fallback line is re-emitted unchanged, so the relics that still "
        f"fall through keep it ({n_rc} others on this link). Through the patched play() every arm reproduces its "
        f"lab candidate (worst "
        f"{max(v for _, v in ac['chk']):.0e}; the landing at counts -1, 0, 1-6, 9 and a missing n, on two noise "
        f"draws), {len(ac['others'])} other voices are unchanged (worst {max(v for _, v in ac['others']):.0e}), and "
        f"ult/ironhail is no longer rune-crack. play() returns on its first line with no audio context (every "
        f"headless run), draws no random number and writes nothing the simulation reads"
        + (f"; end to end the three voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + pe + ".")
    rows[1]["why"] = (
        f"One plain SFX.play in tickHail's landing, after the hurt and the sunder, so n is the count the foe now "
        f"carries (foe.stacks is a read). {wr['landV']}/{wr['land']} landings voiced, each n equal to the foe's "
        f"count (1-{CAP}; {100 * wr['nh'][CAP] / max(1, sum(wr['nh'])):.0f}% at the cap; {wr['fatalLand']} killing); "
        f"{wr['same']}/{wr['fights']} fights identical and every other SFX call identical in order and opts; the "
        f"same rows plus one sim write (the foe nudged 1e-9 on a landing) come back {wr['control_same']}/"
        f"{wr['fights']}{e2}.")
    rows[2]["why"] = (
        f"One guarded SFX.play BEFORE the miss line, which is re-emitted unchanged: the line's own test, read first "
        f"(foe.alive and two positions), and the anchor guards it -- if the test ever changes the row stops "
        f"applying. {wr['missV']}/{wr['miss']} misses voiced, each on its landing step ({wr['deadMiss']} on the step "
        f"the foe died); no miss voice anywhere else; nothing is read back{e2}.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The three rows are the edits; all three were applied "
          "to the page's own code above, and as text to a copy of the page.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
