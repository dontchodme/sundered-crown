#!/usr/bin/env python3
"""TENDRIL'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v101.

    python bindweed_voice_lab.py --game ../02-chain/sc-tendril-t3.html --rows rows.json

v68 §8.2 SOUND, every word of it: "Cast -- a rising rustle-and-creak, 0.5s,
noise band-passed 400-3k with a low creak under it (a re-struck `_tone` at
70-90 Hz, since a held note does not exist here). Not a chime, not a crack:
this is growth. Bite -- a short wet snap, 60-90ms, peak <=0.45, pitched up a
semitone per entangle stack on the foe (the count in the ear -- Sentinel's hum
rule: the number of snaps is the number of bites). Root -- a low creak into a
crack, 0.35s, share below 120 Hz >= 0.4 (Deadfall's detonation register: this
is the biggest single thing the relic does). Wither -- a dry falling rustle,
0.4s, high-passed 1.5k, quiet (peak <=0.3): the tell that the window is over."
Brief stage 6: "Four voices rendered as a spread of four each in an
OfflineAudioContext and MEASURED against §8.2's registers; pick on the
numbers, send the clips." Rick, for the batch's art and sound: "you pick i
overrule". So this lab renders four or five candidates a voice beside CONTROLS
that can come back wrong, prints the numbers each pick is made on, and PICKS by
a rule written in this file (`*_RULE`, `*_why`). He overrules from one clip.

THE FOUR EVENTS AND WHERE THEY FIRE:
  cast    the bare id `ult/bindweed`, which `fireUlt` plays for every relic.
          Bindweed has NO arm today: it falls through to the shared rune-crack
          (so do eleven others -- measured below, to 1e-6). The arms go BEFORE
          that fallback; the fallback line is re-emitted unchanged.
  bite    `ult/bindweed-bite {n}` from `tickTendril`, once per bite, after the
          bite's hurt and its entangle: n = the foe's entangle stacks after the
          bite (1..4 in play; the voice is defined and distinct for 0..4). A
          bite that kills plays its snap too -- the number of snaps is the
          number of bites -- and the death voice lands on the same frame.
  root    `ult/bindweed-root` from `tickTendril`, inside the block that writes
          the pin: the window closed by its clock, both alive, the foe carrying
          entangle. One a root, never otherwise.
  wither  `ult/bindweed-wither` from `tickTendril` on the frame the window
          closes BY ITS CLOCK with both alive -- every such close, rooted or
          not; on a rooting close it sounds on the root's frame, so the two are
          measured TOGETHER below. Never on a death: a caster's death ends the
          fight, and a close after the foe's death is a kill flight's (both are
          the death voice's), as Canopy's, Zenith's and Daybreak's closes are.
  Bites set no hit stop and file no beat (v67; the killing bite's fatal beat is
  the sim's, already there). The voices are four plain SFX.play calls. The
  root's director beat and everything drawn (the greening, the floor-root, the
  runic hexagon skipped for the vine's root) are the picture's rows, not these.

THE CONTROLS, and what each one is for:
  rune-crack   what Bindweed's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted (with BAR 0.364 /
               300 ms and hit@11.6 0.443 / 80 ms)
  hit@18       Bindweed's own blow (blade 18): what every voice is levelled
               against, on its quietest / loudest noise draw
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   Thornwake, Vinesower, Thornshear and Ironwood's casts (Heartwood
               is rune-crack): the verdant casts the cast must not sound like
  the type     Gravemourn, Slagheart, Threshmaw, Paradox and Morningstar's
               casts (Portcullis is rune-crack): the flail row's
  CHIME        Morningstar's cast (a bright swell): "not a chime" -- as a cast
               it must come back wrong
  RUSTLE, CREAK, FALL   the cast's halves alone and the cast run downward:
               each must fail the cast's rule
  DRY, FLAT    the bite's snap with no body, and the bite at one pitch for
               every count: each must fail the bite's rule
  fork, hex-snap, vine plant   the house's wet split, the runic snap and the
               school's own small sound: the bite must not be any of them
  CRACK, CREAK, BACK, HELD   the root's halves alone, the crack BEFORE the
               creak, and the creak as a held tone (no stick-slip): each must
               fail the root's rule
  Deadfall, Paradox's pin   the detonation §8.2 names, and the other voice in
               the game that lands a hold: printed / the root must not be them
  RISE, CANOPY'S WITHER, CAST-QUIET   the wither run upward; Canopy's wither
               (a dry creak falling, a TONE); the picked cast at the wither's
               level: each must fail the wither's rule
  LITERAL      noise band-passed with its -3 dB edges AT 400 and 3000 Hz: the
               reading BAND's gate is set against (a reference, not a control)
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT, generated with its constants rounded
    first and rendered by evaluating that text on the synth; the row is then
    applied to `Sfx.prototype.play`'s own source and rendered again, and must
    match to 1e-6 (ironwood_voice_lab's RENDER_JS, imported unchanged).
  * The shared measures are zenith_voice_lab's and ironwood_voice_lab's,
    imported unchanged: E50, TOP, START, AUDIBLE, GONE, RISE, REG (cosine of
    1/3-octave band amplitudes, 25 Hz-16 kHz, the median over noise draws),
    IN-BAND, PITCH (FFT peak, Hann, zero-padded, parabolic), LOW (the share
    of the power below 120 Hz), CENTROID, CRACK (the lag, in cents, that
    best correlates two voices' draw-averaged spectra 500 Hz-8 kHz), and
    PULSED (the envelope autocorrelation at 12-60 ms of the voice high-passed
    at 150 Hz, windows under -30 dB scoring 0).
  * New here, each with a control that can come back wrong:
      BAND    the share of the power above 150 Hz that lies in 400-3000 Hz
      TONAL   how far the draw-averaged spectrum's sharpest peak stands over
              its neighbourhood: the mean power in a 1/48-octave window over
              the median of those windows within 1/3 octave, in dB, the max
              over the band. Averaged noise reads a few dB; a tone reads tens
      RISE-C / FALL   cents from the CENTROID (in the voice's own band) of
              its first 100 audible ms to that of its last 100
      SWELL   TOP - START (dB): a crack's loudest 50 ms is at its head
      HELD PITCH   the creak alone's FFT peak, 40-130 Hz, over its first and
              last 100 audible ms
      BODY    the bite's pitched body rendered ALONE (the lab builds every
              candidate from named parts, as ironwood_voice_lab's THUD and
              CREAK were): its pitch over its first 20 ms and the 25 ms before
              the whole snap is gone, and its loudest 50 ms re the whole's
      STEP    the bite n -> n + 1 in cents, twice: the body's start pitch and
              CRACK on the whole snap (both halves must move a semitone)
      RE-ATTACK   a second 1 ms RMS peak >= 0.5 of the first, >= 15 ms after
              it and >= 6 dB over the dip between: a second snap
      HF      the voice high-passed at 1.5 kHz (FFT), its 1 ms RMS: the
              crack is the loudest HF millisecond; STAND = it over the p90 of
              the HF envelope before it; JUMP = it over the HF 2 ms before it
      DEPTH   the median over PULSED's windows of the p90 / p10 of that
              envelope, dB: a train of pulses is deep, a held tone is flat
              (PULSED's windows are 100 ms here: the root's creak is 0.2 s)
      BELOW-1.5k   the share of the power below 1.5 kHz
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's creak ratio so its creak alone sits 6 dB under its
    rustle alone, then its gain so TOP is the centre of its window; the bite's
    decay so it is audible 75 ms (the centre of 60-90) and its gain so its
    loudest 50 ms is the centre of its window, both at n = 2; the wither's
    gain 9 dB under the picked cast's top (Canopy's and Zenith's close); the
    root's weight (the thud's gain) so LOW is 0.50 -- the gate's 0.40 plus a
    margin for the draws, as Canopy's cast took 0.60 for its 0.50 -- then its
    creak 6 dB under its crack, then its gain to the centre of its window.
    Constants are rounded BEFORE any measured render.

THE DECLARED CHOICES (not candidates -- words of §8.2 turned into numbers):
  * "RISING": the rustle's band CLIMBS (growth goes up) and so does the creak:
    the creak glides 70 -> 90 Hz, the prose's range read as the rise, and
    every rustle climbs from 400 Hz to 3 kHz, the prose's band read as the
    same rise. Its level swells too (creak 0.4 -> 1 of its top).
  * "A RE-STRUCK _tone AT 70-90 Hz": a held note re-struck at its own cycles
    (Zenith's technique; `.frequency.value = f` set on every strike, v97's
    finding); FRY reads it the other way, re-struck at a creak's 33-55 a
    second. The design's own construction, so "creak" is not measured on the
    cast beyond its pitch and its level (the root's is, below).
  * "WET": the house's own word for it -- `fork`, "A WET SPLIT ... with a
    falling body underneath", and Widowmaker's "wet slice" -- a snap over a
    pitched body that falls.
  * THE BITE'S PITCH: the body starts on A5 (the score's A) at n = 0 and every
    frequency of the snap is x 2^(n/12): A#5 on the first bite of a clean foe,
    C#6 at the cap (4).
  * THE ROOT'S "CREAK" is the house's creak (ironwood_voice_lab): a train of
    pulses, stick-slip, here QUICKENING 33 -> 55 a second (the strain before
    the give), each interval x (1 + 0.12 sin 2.4k), no random number; the
    crack at 0.2 s (EARLY moves it to 0.12): a 35 ms highpass snap at 2.6 kHz
    over a sine thud UNDER the death voice's 120 Hz start (72 -> 28 Hz,
    Canopy's ground-thud, with a 140 Hz lowpass burst; DEEP 60 -> 30 Hz alone).
  * "LOW" is the design's own number, LOW >= 0.40. Deadfall's detonation is
    printed beside it: it measures 0.05 below 120 Hz itself, so "Deadfall's
    detonation register" is read as its standing (the biggest single thing the
    relic does), and the explicit number is the gate.
  * "THE BIGGEST SINGLE THING THE RELIC DOES": the root's loudest 50 ms is at
    least 1 dB over each of the relic's three other new voices on their
    loudest draws, and its LOW the highest -- and never over the relic's own
    blow (the ceiling Canopy's cast took: heard like a blow, never over one).
  * THE WITHER'S "RUSTLE" is noise (TONAL <= 10 dB), built as the cast's
    rustle is (a chain of sweeps, or grains) and run downward.

THE PICKS, on Chromium 151.0.7922.34, sc-tendril-t3 5a6216e3b629fad4, fight seeds
101601-101602 (148 fights), end to end 101651 (74):

  cast    3 SWEEP-TRI  one bandpass sweep climbing 400 -> 3000 Hz over 0.56 s
                   (Q 0.8, its top at 335 ms) over a triangle held by re-striking
                   at its own cycles, gliding 70 -> 90 Hz and swelling. The
                   rustle climbs +533 c, the creak reads 71 -> 88 Hz, -6.0 dB
                   under it; BAND 0.65 at the worst draw (LITERAL reads 0.55),
                   TONAL 2.6 dB, SWELL +12.6 dB; audible 510 ms; TOP -2.9 dB re
                   the hit @ 18, +18.0 dB re the wall; register at most 0.69
                   (Thornshear's cast -- the verdant and flail casts' own
                   pairwise median is 0.41, their max 0.79). CHAIN-TRI (0.72)
                   ties it to 0.05 and loses on calls, 42 to 40; CHAIN-SAW (0.76)
                   and GRAIN-TRI (0.78) lose the register; FRY out (its creak
                   reads 53 Hz -- the strike rate, not the note).
  bite    1 SNAP   a 12 ms bandpass snap at 2.4 kHz over a sine falling A5 ->
                   A4, every frequency x 2^(n/12): audible 75-80 ms at every
                   count, peak 0.21 at the worst draw and count (the spec's
                   0.45), the body falling 518-565 c under the snap, every count
                   +100 c on the body and +93..+95 c on CRACK; loudest 50 ms
                   -9.0 dB re the hit @ 18, +11.9 dB re the wall; register at
                   most 0.51 (rune-crack). PLOP (0.48) ties it to 0.05 and on
                   calls and loses on the order listed; TWIG passes (0.51); SPLIT
                   out (the fork itself, 0.93, and a second snap 15 ms on).
  root    3 DEEP   BEAM's creak -- a 260 Hz sine and its 2.76 mode pulsed 33 ->
                   55 a second for 0.2 s -- into the crack: a 35 ms 2.6 kHz
                   highpass snap over a sine falling 60 -> 30 Hz. LOW 0.50 at the
                   worst draw (0.52 on render.py's), the crack at 206 ms standing
                   +43.5 dB, the creak at 42 a second (PULSED 0.76) -5.6 dB under
                   it; audible 370 ms; TOP -1.4 dB re the hit @ 18 and +1.5 dB
                   over the cast, the relic's loudest other voice; 0.31 against
                   the death voice. Register at most 0.795 (Threshmaw's cast):
                   AT the gate -- a voice that carries 0.4 of its power below
                   120 Hz sits near the flail row's low casts, and every other
                   candidate crossed it (KNOCK 0.85 Gravemourn, BEAM 0.82
                   Slagheart, GROAN 0.82 Threshmaw). EARLY out (a 0.12 s creak
                   holds no 100 ms window clear of the crack).
  wither  1 CHAIN  three overlapping bandpass sweeps (Q 0.9) falling 7 -> 4.8,
                   5 -> 3.4, 3.6 -> 2.4 kHz, each quieter: FALL -807 c, 0.01 of
                   its power below 1.5 kHz, LOW 0.00, TONAL 2.2 dB, audible 355
                   ms, gone 380 ms, peak 0.19; -9.0 dB under the cast's top,
                   +9.0 dB re the wall; register at most 0.64 (Scour's woosh).
                   HPCHAIN out (a falling highpass barely falls: -307 c); LEAVES
                   and FLAKES out (peak 0.40 / 0.52: a 12 ms grain is one slice
                   of the noise buffer struck again and again, and it spikes).

  On one frame -- every rooting close plays both -- the wither keeps its own
  third-octave (6.4 kHz) +4.9 dB over the root alone, the root its own (50 Hz)
  +66.6 dB over the wither alone.

  In play (148 fights; 476 windows -- 371 closed by the clock, 18 by the
  caster's death, 87 by the fight's end): 2882 bites and 2882 bite voices, each
  n the foe's stacks (1:243 2:49 3:230 4:2360 -- 82% at the cap, the top note;
  5 on a killing bite); 356 roots and 356 root voices; 371 withers, one per
  clock close (15 of them rooted nobody), none on a death or a fight's end;
  148/148 fights identical and every other SFX call identical in order and
  opts; the sim-write control 4/148. In a real window (v Oathwound, 101602, 14
  bites, rooted) the bites stand +14.0..+35.6 dB over the fight and the score in
  their own third-octaves (median +28.5), the wither +3.6 dB over everything
  else on its frame, the root included, and the root +26.6 dB. End to end:
  74/74 fights identical to the unpatched page's with every voice count exact,
  and the four voices through the patched page's own SFX.play equal to the
  candidates to 1.2e-7. Main-thread cost a call: cast 1.4 ms, bite 0.1, root
  0.7, wither 0.2 (the hit's 0.1).

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table; that table (one fight seed) then showed a gate the
spec's own construction cannot meet, an instrument blind to what it was built
to see, a register no candidate of the kind could pass, and a construction that
failed for a reason worth keeping. Each was changed ONCE, for the reason given,
before the picks:
  * BAND was first ">= 0.70", and every cast failed it (0.53-0.65), its own
    rustle alone included (0.58). The toolkit's only filter is a 2nd-order
    biquad, which keeps half its power inside its own -3 dB band: noise
    band-passed LITERALLY 400-3k reads 0.55 (now printed). The gate is 0.50,
    the majority of the power inside the band; the CREAK control reads 0.05.
  * THE WITHER'S REGISTER against the wall tick read 0.88-0.98 for every
    candidate. The wall tick is high-passed noise (3 kHz), the spec high-passes
    the wither (1.5k), and REG reads the spectrum, not time: a 25 ms tick and a
    355 ms falling rustle share one. It is printed, not gated; AUDIBLE and FALL
    tell the two apart.
  * THE ROOT'S CREAK: the HELD control PASSED (PULSED 0.98, DEPTH 6.1 dB). A
    note held in this toolkit is re-struck, so its envelope is itself a pulse
    train at the note's own rate (260 a second, each strike decaying ~10 dB a
    cycle); PULSED took the best lag in 12-60 ms and found a multiple of that
    period, and DEPTH read the swell. A creak is now RATE -- the envelope's own
    modulation frequency -- inside a creak's 17-83 a second (HELD reads 480),
    with PULSED >= 0.40 beside it; DEPTH is printed.
  * THE ROOT'S WEIGHT: every first-cut root read 0.85-0.90 against the death
    voice, and the fault was the construction: its thud fell 110 -> 36 Hz, the
    death voice's own 120 -> 32 Hz, and carried 0.65-0.76 of the power below
    120 Hz. The thud now sits under the death voice's start, its gain is
    level-matched so LOW is 0.50, and the root's register list took in the
    verdant and flail casts (a heavy low event in the school and the type the
    cast is checked against). The second cut reads 0.31-0.56 against the death
    voice -- and meets the flail row instead (above).
  * THE REAL WINDOW first read the root in the third-octave at its centroid,
    181 Hz, between its thud and its creak, holding little of either (+0.9
    dB). A voice's own band is now the band it is loudest in (50 Hz: +26.6).

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row is applied to `Sfx.prototype.play`'s own source and rendered:
    each arm (the bite at every count, on a noise draw) must reproduce its
    candidate to 1e-6; every other voice through the patched play (the hit at
    five weights with and without a crit, spark x3, wall, death, clank, seal,
    nova, hex-snap, fork, vine x4, loose x3, aegis, the four scour voices,
    every other relic's cast and the ult sub-voices Canopy and Zenith added)
    must be unchanged; `ult/bindweed` must NOT be rune-crack any more;
  * the three tickTendril rows are applied to the prototype's own source and
    run on real fights beside the unpatched one: every fight identical (over,
    clock, both hp, both positions, winner, the whole vineTally), and every
    other SFX call identical in order and opts; one bite voice per bite on
    its call, its n the foe's stacks at that moment (1..4); one root voice per
    root; one wither per window closed by its clock with both alive and none
    otherwise; the cast's bare id once per window. There is no mirror match:
    `Match` refuses a relic against itself (measured). The same rows plus ONE
    sim write (the foe nudged 1e-9 on a bite) must come back NOT identical,
    or "identical" proves nothing. (The Sfx rows cannot reach the simulation
    at all: `play` returns on its first line with no audio context, which is
    every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a
    temporary folder, deleted after), loaded in a fresh browser once the first
    has closed (never two at once): the four new voices through the patched
    page's own `SFX.play` equal the lab's candidate text rendered in that page;
    every other voice equals the unpatched page's; Bindweed's fights on both
    sides against every foe are identical to the unpatched page's, with the
    voice counts above.
  All anchors must occur exactly once in the game file.

Writes wavs to 05-reference/v101/bindweed-*.wav at RAW level (gitignored).
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
# The shared definitions, imported unchanged so every number here means what it
# means in v98's and v99's labs. (Both modules' bodies only define things.)
from zenith_voice_lab import (  # noqa: E402
    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    fmt, pcm, pitch, write_wav, _comment)
from ironwood_voice_lab import (  # noqa: E402
    RENDER_JS, centroid, crack_shift, low_share, pulsed)

HERE = pathlib.Path(__file__).parent
ME = "bindweed"
BLADE = 18.0                              # Bindweed's dmg (stage 5)
CREAK_UNDER_DB = 6.0                      # the cast's creak under its rustle
BITE_AUD_MS = 75.0                        # the bite's level-matched audible length
BITE_REF_N = 2                            # the count the bite is level-matched at
ROOT_CREAK_UNDER_DB = 6.0                 # the root's creak under its crack
ROOT_LOW_TARGET = 0.50                    # the root's level-matched low share (the gate's 0.4 + a margin)
WITHER_UNDER_DB = 9.0                     # the wither under the cast's top
NS = [0, 1, 2, 3, 4]                      # the counts the bite is defined for
SCHOOL = ["thornwake", "heartwood", "vinesower", "thornshear", "ironwood"]
TYPE = ["gravemourn", "slagheart", "redflail", "paradox", "morningstar", "portcullis"]


# =============================================================== THE CAST ===
# "a rising rustle-and-creak, 0.5s, noise band-passed 400-3k with a low creak
# under it (a re-struck _tone at 70-90 Hz ...)". They differ in how the rustle
# is made (one sweep, a chain of three, grains) and how the creak is struck.
CAST_CANDIDATES = [
    ("1 CHAIN-SAW", dict(rustle="chain", creak="held", wave="sawtooth"),
     "three overlapping bandpass sweeps climbing 400 -> 3000 Hz; the creak a sawtooth held by re-striking at "
     "its own cycles, 70 -> 90 Hz"),
    ("2 CHAIN-TRI", dict(rustle="chain", creak="held", wave="triangle"),
     "the same chain; the creak a triangle held the same way"),
    ("3 SWEEP-TRI", dict(rustle="sweep", creak="held", wave="triangle"),
     "one bandpass sweep 400 -> 3000 Hz over 0.56 s; the held triangle creak"),
    ("4 GRAIN-TRI", dict(rustle="grain", creak="held", wave="triangle"),
     "leaves: 35 ms bandpass grains ~50 a second, the band climbing 400 -> 3000 Hz; the held triangle creak"),
    ("5 CHAIN-FRY", dict(rustle="chain", creak="fry", wave="triangle"),
     "the chain; the creak struck at a creak's rate instead, 33 -> 55 a second, each strike 70 -> 90 Hz"),
]


def rustle_lines(sp):
    up = sp.get("dir", "up") == "up"
    if sp["rustle"] == "sweep":
        f0, f1 = (400, 3000) if up else (3000, 400)
        return [f'this._sweep(t, {{ f0: {f0}, f1: {f1}, q: 0.8, gain: g, dur: 0.56, atk: 0.33, type:"bandpass" }});']
    if sp["rustle"] == "chain":
        bd = [(400, 900), (800, 1700), (1500, 3000)]
        if not up:
            bd = [(b_, a_) for a_, b_ in reversed(bd)]
        out = []
        for s_, (a_, b_), gg in zip((0, 0.14, 0.28), bd, ("g * 0.6", "g * 0.8", "g")):
            tt = "t" if s_ == 0 else f"t + {fmt(s_)}"
            out.append(f'this._sweep({tt}, {{ f0: {a_}, f1: {b_}, q: 0.8, gain: {gg}, dur: 0.24, atk: 0.1, '
                       f'type:"bandpass" }});')
        return out
    if sp["rustle"] == "grain":
        fx = "400 * Math.pow(7.5, u)" if up else "3000 * Math.pow(1 / 7.5, u)"
        return ["for (let s = 0, k = 0; s < 0.47; k++){",
                "  const u = s / 0.5, a = g * (0.35 + 0.65 * u);",
                f'  this._burst(t + s, {{ freq: {fx}, q: 1.4, gain: a, dur: 0.035, type:"bandpass" }});',
                "  s += 0.02 * (1 + 0.3 * Math.sin(k * 2.4));",
                "}"]
    raise ValueError(sp)


def creak_lines(sp):
    up = sp.get("dir", "up") == "up"
    fx = "70 * Math.pow(90 / 70, u)" if up else "90 * Math.pow(70 / 90, u)"
    if sp["creak"] == "held":
        return ["for (let s = 0; s < 0.49;){",
                f"  const u = s / 0.5, f = {fx}, a = g * kc * (0.4 + 0.6 * u);",
                f'  this._tone(t + s, {{ freq: f, gain: a, dur: 0.05, type:"{sp["wave"]}" }}).frequency.value = f;',
                "  s += 1 / f;",
                "}"]
    if sp["creak"] == "fry":
        return ["for (let s = 0, k = 0; s < 0.49; k++){",
                f"  const u = s / 0.5, f = {fx}, a = g * kc * (0.4 + 0.6 * u);",
                f'  this._tone(t + s, {{ freq: f, gain: a, dur: 0.035, type:"{sp["wave"]}" }}).frequency.value = f;',
                "  s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));",
                "}"]
    raise ValueError(sp)


def cast_body(sp, g, kc, part="both", ind=10):
    L = [f"const g = {fmt(g)}, kc = {fmt(kc)};"]
    if part in ("both", "rustle"):
        L += rustle_lines(sp)
    if part in ("both", "creak"):
        L += creak_lines(sp)
    return "\n".join(" " * ind + l_ for l_ in L)


# =============================================================== THE BITE ===
# "a short wet snap, 60-90ms, peak <=0.45, pitched up a semitone per entangle
# stack on the foe". A snap (the CRACK part) over a falling pitched body (the
# BODY part); every frequency x k = 2^(n/12).
BITE_CANDIDATES = [
    ("1 SNAP", dict(body="snap"),
     "a 12 ms bandpass snap at 2.4 kHz over a sine body falling A5 -> A4"),
    ("2 TWIG", dict(body="twig"),
     "a 6 ms highpass click over a triangle body falling E5 -> E4"),
    ("3 SPLIT", dict(body="split"),
     "the house's wet split (`fork`) at its own ratios: a 1650 Hz burst, a sawtooth falling 430 -> 140 Hz, "
     "a 640 Hz burst 22 ms on"),
    ("4 PLOP", dict(body="plop"),
     "a ringing snap (bandpass noise at Q 9, 1100 Hz) over a sine falling 1100 -> 550 Hz"),
]
BCRACK = {
    "snap": ['this._burst(t, { freq: 2400 * k, q: 1.4, gain: g, dur: 0.012, type:"bandpass" });'],
    "twig": ['this._burst(t, { freq: 5200 * k, q: 0.9, gain: g, dur: 0.006, type:"highpass" });'],
    "split": ['this._burst(t, { freq: 1650 * k, q: 0.9, gain: g, dur: 0.045, type:"bandpass" });',
              'this._burst(t + 0.022, { freq: 640 * k, q: 1.7, gain: g * 0.73, dur: 0.09, type:"bandpass" });'],
    "plop": ['this._burst(t, { freq: 1100 * k, q: 9, gain: g, dur: 0.03, type:"bandpass" });'],
}
BBODY = {
    "snap": ['this._tone(t, { freq: 880 * k, to: 440 * k, gain: g * 0.8, dur: D, type:"sine" });'],
    "twig": ['this._tone(t, { freq: 660 * k, to: 330 * k, gain: g * 0.8, dur: D, type:"triangle" });'],
    "split": ['this._tone(t, { freq: 430 * k, to: 140 * k, gain: g * 1.13, dur: D, type:"sawtooth" });'],
    "plop": ['this._tone(t, { freq: 1100 * k, to: 550 * k, gain: g * 0.5, dur: D, type:"sine" });'],
}
KEXPR = "Math.pow(2, Math.max(0, Math.min(4, p.n | 0)) / 12)"


def bite_body(sp, g, D, part="both", flat=False, ind=10):
    L = [f"const g = {fmt(g)}, D = {fmt(D)}, k = {'1' if flat else KEXPR};"]
    if part in ("both", "crack"):
        L += BCRACK[sp["body"]]
    if part in ("both", "body") and not sp.get("dry"):
        L += BBODY[sp["body"]]
    return "\n".join(" " * ind + l_ for l_ in L)


# =============================================================== THE ROOT ===
# "a low creak into a crack, 0.35s, share below 120 Hz >= 0.4". The creak is
# a pulse train quickening into the crack; they differ in what a pulse IS and
# in where the crack lands.
ROOT_CANDIDATES = [
    ("1 KNOCK", dict(pulse="knock", c=0.2, thud=(72, 28, 0.32), lp=140),
     "a 150 Hz triangle knock pulsed 33 -> 55 a second for 0.2 s, then the crack over a 72 -> 28 Hz thud and a "
     "140 Hz lowpass burst"),
    ("2 BEAM", dict(pulse="beam", c=0.2, thud=(72, 28, 0.32), lp=140),
     "Canopy's timber an octave and a half down (a 260 Hz sine and its 2.76 mode at 0.4) pulsed, then the same "
     "crack"),
    ("3 DEEP", dict(pulse="beam", c=0.2, thud=(60, 30, 0.3), lp=None),
     "BEAM's creak, then the crack over a deeper 60 -> 30 Hz sine alone (no lowpass burst)"),
    ("4 GROAN", dict(pulse="low", c=0.2, thud=(72, 28, 0.25), lp=None),
     "the creak itself low: an 85 Hz triangle pulsed, then the crack over a 72 -> 28 Hz thud"),
    ("5 EARLY", dict(pulse="beam", c=0.12, thud=(72, 28, 0.32), lp=140),
     "BEAM cut to a 0.12 s creak: the crack comes sooner"),
]
RPULSE = {
    "knock": ['this._tone(t + s, { freq: 150, gain: a, dur: 0.03, type:"triangle" });'],
    "beam": ['this._tone(t + s, { freq: 260, gain: a, dur: 0.03, type:"sine" });',
             'this._tone(t + s, { freq: 718, gain: a * 0.4, dur: 0.02, type:"sine" });'],
    "low": ['this._tone(t + s, { freq: 85, gain: a, dur: 0.04, type:"triangle" });'],
}


def root_body(sp, g, kc, kt, part="both", order="into", held=False, ind=10):
    C = sp["c"]
    tc = f"t + {fmt(C)}" if order == "into" else "t"
    to = "t" if order == "into" else "t + 0.1"
    if held:
        creak = [f"for (let s = 0; s < {fmt(round(C - 0.012, 6))}; s += 1 / 260){{",
                 f"  const u = s / {fmt(C)}, a = g * kc * (0.45 + 0.55 * u);",
                 f'  this._tone({to} + s, {{ freq: 260, gain: a, dur: 0.03, type:"sine" }}).frequency.value = 260;',
                 "}"]
    else:
        creak = [f"for (let s = 0, k = 0; s < {fmt(round(C - 0.012, 6))}; k++){{",
                 f"  const u = s / {fmt(C)}, a = g * kc * (0.45 + 0.55 * u);",
                 *["  " + l_.replace("this._tone(t + s", f"this._tone({to} + s") for l_ in RPULSE[sp["pulse"]]],
                 "  s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));",
                 "}"]
    f0, f1, dth = sp["thud"]
    crack = [f'this._burst({tc}, {{ freq: 2600, q: 0.8, gain: g * 0.8, dur: 0.035, type:"highpass" }});',
             f'this._tone ({tc}, {{ freq: {f0}, to: {f1}, gain: g * kt, dur: {fmt(dth)}, type:"sine" }});']
    if sp.get("lp"):
        crack.append(f'this._burst({tc}, {{ freq: {sp["lp"]}, q: 0.7, gain: g * kt * 0.7, dur: 0.14, '
                     f'type:"lowpass" }});')
    L = [f"const g = {fmt(g)}, kc = {fmt(kc)}, kt = {fmt(kt)};"]
    if part in ("both", "creak"):
        L += creak
    if part in ("both", "crack"):
        L += crack
    return "\n".join(" " * ind + l_ for l_ in L)


# ============================================================= THE WITHER ===
# "a dry falling rustle, 0.4s, high-passed 1.5k, quiet (peak <=0.3)". Built as
# the cast's rustle is, run downward: a chain of three sweeps, or grains.
WITHER_CANDIDATES = [
    ("1 CHAIN", dict(kind="chain", type="bandpass"),
     "three overlapping bandpass sweeps (Q 0.9) falling 7 kHz -> 2.4 kHz, each quieter"),
    ("2 HPCHAIN", dict(kind="chain", type="highpass"),
     "the same chain as highpass sweeps, the cutoff falling 6 kHz -> 1.5 kHz"),
    ("3 LEAVES", dict(kind="grain", type="highpass"),
     "leaves dropping: 12 ms highpass grains thinning 50 -> 22 a second, the cutoff falling 6 kHz -> 1.5 kHz"),
    ("4 FLAKES", dict(kind="grain", type="bandpass"),
     "the same grains bandpassed (Q 1.5), the band falling 7 kHz -> 2.2 kHz"),
]


def wither_body(sp, g, ind=10):
    up = sp.get("dir", "down") == "up"
    L = [f"const g = {fmt(g)};"]
    if sp["kind"] == "chain":
        if sp["type"] == "bandpass":
            bd, q = [(7000, 4800), (5000, 3400), (3600, 2400)], 0.9
        else:
            bd, q = [(6000, 4000), (4200, 2500), (2700, 1500)], 0.7
        if up:
            bd = [(b_, a_) for a_, b_ in reversed(bd)]
        for s_, (a_, b_), gg in zip((0, 0.12, 0.24), bd, ("g", "g * 0.8", "g * 0.6")):
            tt = "t" if s_ == 0 else f"t + {fmt(s_)}"
            L.append(f'this._sweep({tt}, {{ f0: {a_}, f1: {b_}, q: {fmt(q)}, gain: {gg}, dur: 0.22, atk: 0.05, '
                     f'type:"{sp["type"]}" }});')
    else:
        f0, r_, q = (6000, 0.25, 0.7) if sp["type"] == "highpass" else (7000, 0.32, 1.5)
        L += ["for (let s = 0, k = 0; s < 0.37; k++){",
              "  const u = s / 0.4, a = g * (1 - 0.6 * u);",
              f'  this._burst(t + s, {{ freq: {f0} * Math.pow({fmt(r_)}, u), q: {fmt(q)}, gain: a, dur: 0.012, '
              f'type:"{sp["type"]}" }});',
              "  s += 0.02 * Math.pow(2.2, u) * (1 + 0.3 * Math.sin(k * 2.4));",
              "}"]
    return "\n".join(" " * ind + l_ for l_ in L)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
BITE_ANCHOR = ('          if (u.bitePer > 0){ foe.apply("entangle", u.bitePer, f === this.a ? "a" : "b"); '
               'T.stacks += u.bitePer; }')
WITHER_ANCHOR = '        f.vineWither = u.wither;'
ROOT_ANCHOR = '            T.roots++;'

BITE_CODE = BITE_ANCHOR + '''
          /* TENDRIL'S BITE (v68 §8.2: "a short wet snap ... pitched up a
             semitone per entangle stack on the foe"): one snap per bite, after
             the bite's hurt and its entangle, pitched by the stacks the foe now
             carries. A killing bite snaps too -- the number of snaps is the
             number of bites. Presentation only: SFX.play draws nothing, is a
             no-op headless, and nothing here is read back
             (bindweed_voice_lab: fights identical). */
          SFX.play("ult", { w: "bindweed-bite", n: foe.stacks("entangle") });'''

WITHER_CODE = WITHER_ANCHOR + '''
        /* TENDRIL'S WITHER (v68 §8.2: "a dry falling rustle, 0.4s ... the tell
           that the window is over"): on the frame the window runs out BY ITS
           CLOCK with both alive, rooted or not. A caster's death ends the
           fight, and a close after the foe's death belongs to its kill
           flight, so both are left to the death voice (Canopy's, Zenith's and
           Daybreak's rule). Plain SFX.play; nothing is read back. */
        if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "bindweed-wither" });'''

ROOT_CODE = ROOT_ANCHOR + '''
            /* TENDRIL'S ROOT (v68 §8.2: "a low creak into a crack, 0.35s"): on
               the frame the pin is written -- the clock close, both alive, the
               foe carrying entangle. Plain SFX.play; nothing is read back. */
            SFX.play("ult", { w: "bindweed-root" });'''

# the sim-write control: the same bite row with the foe nudged 1e-9 on a bite
BITE_CODE_BAD = BITE_CODE.replace(
    '          SFX.play("ult", { w: "bindweed-bite"',
    '          foe.vx += 1e-9;\n          SFX.play("ult", { w: "bindweed-bite"', 1)

_refuse(BITE_CODE + WITHER_CODE + ROOT_CODE, "sim rows")


def arms_code(C_, B_, R_, W_, info):
    cn, bn, rn, wn = (X["name"].split()[1] for X in (C_, B_, R_, W_))
    c_cast = _comment([
        f'BINDWEED\'S CAST, THE GREENING -- v68 §8.2: "a rising rustle-and-creak, 0.5s, noise band-passed '
        f'400-3k with a low creak under it (a re-struck _tone at 70-90 Hz, since a held note does not exist '
        f'here). Not a chime, not a crack: this is growth." {cn}, of {len(CAST_CANDIDATES)}, picked on the '
        f'numbers by `bindweed_voice_lab.py` under Rick\'s "you pick i overrule" (v101). Bindweed had no arm '
        f'and fell through to rune-crack, which {info["n_rc"]} other relics still use, so this ADDS arms before that '
        f'fallback and leaves it alone.',
        f"{info['c_what']} The rustle's band climbs {info['c_rise']:+.0f} cents across the voice, the creak "
        f"{info['c_f0']:.0f} -> {info['c_f1']:.0f} Hz, {info['c_creak']:+.1f} dB under the rustle; "
        f"{info['c_band']:.2f} of the power above 150 Hz inside 400-3000 Hz at the worst noise draw, no "
        f"peak standing more than {info['c_tonal']:.1f} dB over its neighbours (noise, not a chime), and it "
        f"grows {info['c_swell']:+.1f} dB from its head to its top (not a crack). Audible {info['c_aud']:.0f} "
        f"ms; loudest 50 ms {info['c_db']:+.1f} dB re Bindweed's blow. Register at most "
        f"{info['c_reg']:.2f} against rune-crack, the verdant casts, the flail row's casts, the blow and the "
        f"death voice."], 10)
    c_bite = _comment([
        f'THE BITE -- "a short wet snap, 60-90ms, peak <=0.45, pitched up a semitone per entangle stack on '
        f'the foe (the count in the ear)" (v68 §8.2). {bn}, of {len(BITE_CANDIDATES)} (`bindweed_voice_lab.py`). '
        f'`tickTendril` plays it once per bite with n = the foe\'s entangle stacks after the bite (1-4), '
        f'so every frequency is x 2^(n/12).',
        f"{info['b_what']} Audible {info['b_aud']} ms, peak {info['b_pk']:.2f} at the loudest draw and "
        f"count; the body falls at least {-info['b_fall']:.0f} cents under the snap (wet); each count "
        f"{info['b_step']} cents over the last; loudest 50 ms {info['b_db']:+.1f} dB re the blow and "
        f"{info['b_wall']:+.1f} dB re the wall tick. One snap a call. Register at most {info['b_reg']:.2f} "
        f"against the blow, the wall, fork, hex-snap, the vine's plant, rune-crack and the cast."], 10)
    c_root = _comment([
        f'THE ROOT -- "a low creak into a crack, 0.35s, share below 120 Hz >= 0.4 (Deadfall\'s detonation '
        f'register: this is the biggest single thing the relic does)" (v68 §8.2). {rn}, of '
        f'{len(ROOT_CANDIDATES)} (`bindweed_voice_lab.py`). `tickTendril` plays it on the frame the pin is '
        f'written: a clock close, both alive, the foe carrying entangle.',
        f"{info['r_what']} The creak quickens 33 -> 55 a second (the strain before the give; PULSED "
        f"{info['r_pulsed']:.2f}, {info['r_depth']:.0f} dB deep), {info['r_creak']:+.1f} dB under the crack, "
        f"which lands {info['r_at']:.0f} ms in and stands {info['r_stand']:+.0f} dB over it. "
        f"{info['r_low']:.2f} of its power below 120 Hz at the worst noise draw; audible {info['r_aud']:.0f} "
        f"ms; loudest 50 ms {info['r_db']:+.1f} dB re the blow, {info['r_over']:+.1f} dB over the loudest of "
        f"the relic's three other voices. Register {info['r_death']:.2f} against the death voice, at most "
        f"{info['r_reg']:.3f} against rune-crack, the verdant and flail casts ({info['r_regk']}'s, at the "
        f"gate: a voice this heavy sits near the flail row's low casts), the blow, Deadfall's detonation, "
        f"Paradox's pin and this relic's other three."], 10)
    c_wither = _comment([
        f'THE WITHER -- "a dry falling rustle, 0.4s, high-passed 1.5k, quiet (peak <=0.3): the tell that the '
        f'window is over" (v68 §8.2). {wn}, of {len(WITHER_CANDIDATES)} (`bindweed_voice_lab.py`): '
        f"{info['w_what']}",
        f"Falls {info['w_fall']:+.0f} cents; {info['w_hp']:.2f} of its power below 1.5 kHz and "
        f"{info['w_low']:.2f} below 120 Hz at the worst draw (dry); no peak over {info['w_tonal']:.1f} dB "
        f"(a rustle, not a tone); audible {info['w_aud']:.0f} ms; peak {info['w_pk']:.2f}; "
        f"{info['w_db']:+.1f} dB under the cast's top. `tickTendril` plays it when the window closes by its "
        f"clock with both alive -- on a rooting close, on the root's own frame, where it keeps "
        f"{info['w_keep']:+.1f} dB in its own third-octave over the root."], 10)
    return (f'        }} else if (w === "bindweed"){{                   // the chain greens\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["kc"])}\n'
            f'        }} else if (w === "bindweed-bite"){{              // a thorn goes in\n'
            f'{c_bite}\n{bite_body(B_["sp"], B_["g"], B_["D"])}\n'
            f'        }} else if (w === "bindweed-root"){{              // and takes root\n'
            f'{c_root}\n{root_body(R_["sp"], R_["g"], R_["kc"], R_["kt"])}\n'
            f'        }} else if (w === "bindweed-wither"){{            // and the vine lets go\n'
            f'{c_wither}\n{wither_body(W_["sp"], W_["g"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
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
  for (const [k, kind, p] of [["cast", "ult", { w: "bindweed" }], ["bite", "ult", { w: "bindweed-bite", n: 3 }],
                              ["root", "ult", { w: "bindweed-root" }], ["wither", "ult", { w: "bindweed-wither" }],
                              ["hit", "hit", { dmg: 18, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickTendril rows, applied to the real prototype and run beside the
# original; the survey of Tendril's windows comes out of the same runs. The
# wrapper sees every tickTendril call, so a close is classified on the call
# that makes it (a kill later on the same frame cannot confuse it).
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "bindweed";
  const orig = P.tickTendril; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickTendril anchor occurs ${at} times in tickTendril()` };
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
      const mine = kind === "ult" && p && typeof p.w === "string" && (p.w === ME || p.w.startsWith(ME + "-"));
      if (mine) calls.push({ step, t: m.t, k: p.w, n: p.n === undefined ? null : p.n, inT: !!inT,
                             stk: foe.stacks("entangle"), fhp: foe.hp });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    const wins = []; let W = null, stray = 0;
    const tal = () => f.vineTally ? [f.vineTally.bites, f.vineTally.roots] : [0, 0];
    P.tickTendril = function(dt){
      const Z0 = f.ultVine, t0 = tal(), c0 = calls.length;
      if (Z0 && (!W || W.Z !== Z0)){
        W = { Z: Z0, castStep: step, cast: m.t, bites: 0, biteV: 0, roots: 0, rootV: 0, witherV: 0,
              ns: [], badN: 0, fatalV: 0, end: null, endStep: null, close: null };
        wins.push(W);
      }
      inT++;
      try { return impl.call(this, dt); }
      finally {
        inT--;
        const t1 = tal(), mine = calls.slice(c0);
        if (Z0){
          W.bites += t1[0] - t0[0]; W.roots += t1[1] - t0[1];
          for (const c of mine){
            if (c.k === ME + "-bite"){ W.biteV++; W.ns.push(c.n);
              if (c.n !== c.stk || c.n < 1 || c.n > 4) W.badN++;
              if (c.fhp <= 0) W.fatalV++; }
            else if (c.k === ME + "-root") W.rootV++;
            else if (c.k === ME + "-wither") W.witherV++;
          }
          if (!f.ultVine){
            W.end = (Z0.t >= Z0.dur && f.alive && foe.alive) ? "clock"
                  : !f.alive ? "caster" : !foe.alive ? "foe" : "?";
            W.endStep = step; W.close = m.t;
          }
        } else stray += mine.length;
      }
    };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; } }
    finally { P.tickTendril = orig; if (had) S.play = op; else delete S.play; }
    for (const w of wins) if (!w.end) w.end = "over";
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.winner ? m.winner.w.id : null, f.vineTally || null]),
             calls, other: JSON.stringify(other), stray, wins: wins.map(w => { const { Z, ...r } = w; return r; }) };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, caster: 0, foe: 0, over: 0, "?": 0 };
  let casts = 0, bites = 0, biteV = 0, roots = 0, rootV = 0, withers = 0, fatalV = 0, clockNoRoot = 0;
  const nh = [0, 0, 0, 0, 0, 0], perWin = [], pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a Tendril voice"]);
    const castV = B.calls.filter(c => c.k === ME);
    if (castV.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", castV.length, B.wins.length]);
    if (castV.some(c => c.inT)) bad.push([fid, sd, "a cast voice from inside tickTendril"]);
    for (const c of B.calls) if (c.k !== ME && !c.inT) bad.push([fid, sd, "a Tendril voice outside tickTendril", c.k]);
    if (B.stray) bad.push([fid, sd, "Tendril voices from tickTendril with no window open", B.stray]);
    for (const W of B.wins){
      ends[W.end]++; casts++; bites += W.bites; biteV += W.biteV; roots += W.roots; rootV += W.rootV;
      withers += W.witherV; fatalV += W.fatalV; perWin.push(W.bites);
      for (const n of W.ns) nh[Math.max(0, Math.min(5, n))]++;
      if (W.biteV !== W.bites) bad.push([fid, sd, "bite voices vs bites", W.biteV, W.bites]);
      if (W.badN) bad.push([fid, sd, "a bite voice whose n is not the foe's stacks (1-4)", W.badN]);
      if (W.rootV !== W.roots || W.roots > 1) bad.push([fid, sd, "root voices vs roots", W.rootV, W.roots]);
      if (W.roots && W.end !== "clock") bad.push([fid, sd, "a root on a " + W.end + " close"]);
      if (W.witherV !== (W.end === "clock" ? 1 : 0)) bad.push([fid, sd, W.end + " close played withers", W.witherV]);
      if (W.end === "clock" && !W.roots) clockNoRoot++;
      if (W.end === "clock" && W.roots) pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, bites: W.bites });
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, bites, biteV, roots, rootV, withers,
           fatalV, clockNoRoot, nh, perWin, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "bindweed";
  const orig = P.tickTendril; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && q.w.startsWith(ME)) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickTendril = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickTendril = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "bindweed";
  const res = [];
  if (!P.tickTendril) return { err: "no tickTendril" };
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.n === undefined ? null : p.n, foe.stacks("entangle")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const tt = P.tickTendril; let clock = 0;
    P.tickTendril = function(dt){ const Z0 = f.ultVine;
      try { return tt.call(this, dt); }
      finally { if (Z0 && !f.ultVine && Z0.t >= Z0.dur && f.alive && foe.alive) clock++; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { P.tickTendril = tt; if (had) S.play = op; else delete S.play; }
    const T = f.vineTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                    m.winner ? m.winner.w.id : null, f.vineTally || null]),
               casts: T.casts || 0, bites: T.bites || 0, roots: T.roots || 0, clock,
               castV: log.filter(e => e[0] === ME).length,
               biteV: log.filter(e => e[0] === ME + "-bite").length,
               badN: log.filter(e => e[0] === ME + "-bite" && (e[1] !== e[2] || e[1] < 1 || e[1] > 4)).length,
               rootV: log.filter(e => e[0] === ME + "-root").length,
               witherV: log.filter(e => e[0] === ME + "-wither").length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def share_below(x, fc):
    return low_share(x, fc)


def band_share(x, lo, hi, above=150.0):
    """The share of the power above `above` Hz that lies in [lo, hi]."""
    np = _np()
    y = x[int(T0 * SR):]
    P = np.abs(np.fft.rfft(y)) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float(P[(fr >= lo) & (fr <= hi)].sum() / P[fr >= above].sum())


def tonal(xs, a, b, lo, hi):
    """TONAL: the draw-averaged power spectrum over [a, b] s, the mean power in
    a 1/48-octave window on a 1/48-octave grid, each over the median of those
    within 1/3 octave; the max over [lo, hi], dB."""
    np = _np()
    NF = 1 << 16
    fr = np.fft.rfftfreq(NF, 1 / SR)
    P = 0.0
    for x in xs:
        seg = x[int(a * SR):int(b * SR)]
        P = P + np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NF)) ** 2
    cs = np.concatenate([[0.0], np.cumsum(P)])
    grid = lo * 2 ** (np.arange(0, int(48 * math.log2(hi / lo)) + 1) / 48)
    l1 = np.searchsorted(fr, grid * 2 ** (-1 / 96)); h1 = np.searchsorted(fr, grid * 2 ** (1 / 96))
    nar = (cs[h1] - cs[l1]) / np.maximum(h1 - l1, 1)
    best = 0.0
    for i in range(len(grid)):
        j0, j1 = max(0, i - 16), min(len(grid), i + 17)
        med = float(np.median(nar[j0:j1]))
        if med > 0:
            best = max(best, float(nar[i]) / med)
    return 10 * math.log10(max(best, 1e-12))


def hf_env(x, fc=1500.0):
    """The voice from T0 high-passed at fc (FFT), its 1 ms RMS, 1 ms hop."""
    np = _np()
    y = x[int(T0 * SR):]
    Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fr < fc] = 0
    h = np.fft.irfft(Y, len(y))
    H = int(0.001 * SR); n = len(h) // H
    return np.sqrt((h[:n * H].reshape(n, H) ** 2).mean(axis=1))


def crack_info(x, a0_ms):
    """HF: the crack is the loudest high-passed millisecond. Its time (ms after
    the event), STAND (dB over the p90 of the HF envelope from the onset to 10
    ms before it) and JUMP (dB over the HF 2 ms before it)."""
    np = _np()
    e = hf_env(x)[:600]
    i = int(np.argmax(e))
    pre = e[int(a0_ms):max(int(a0_ms) + 1, i - 10)]
    stand = db(e[i] / max(float(np.percentile(pre, 90)), 1e-12)) if i - 10 > a0_ms + 5 else 0.0
    jump = db(e[i] / max(float(e[max(0, i - 2)]), 1e-12)) if i >= 2 else 99.0
    return float(i), stand, jump


def pulsed_w(x, a, b, win=0.1):
    """PULSED and RATE (ironwood_voice_lab's measure) with `win`-second windows,
    and DEPTH: the median over the windows of p90 / p10 of the high-passed 1 ms
    envelope, dB (a window under the -30 dB floor scores 0)."""
    np = _np()
    y = x[int(T0 * SR):]
    floor = float(env(y, 0.05)[0].max()) * 10 ** (-30 / 20)
    Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fr < 150] = 0
    h = np.fft.irfft(Y, len(y))
    H = int(0.001 * SR); n = len(h) // H
    e = np.sqrt((h[:n * H].reshape(n, H) ** 2).mean(axis=1))
    W = int(round(win * 1000))
    pk, lg, dp = [], [], []
    for w0 in range(int(round(a * 1000)), int(round(b * 1000)) - W + 1, 25):
        seg = e[w0:w0 + W]
        if math.sqrt(float((seg ** 2).mean())) < floor:
            pk.append(0.0); dp.append(0.0)
            continue
        dp.append(db(float(np.percentile(seg, 90)) / max(float(np.percentile(seg, 10)), 1e-12)))
        best, bl = -1.0, 0
        for L in range(12, min(61, W - 20)):
            u, v = seg[:-L], seg[L:]
            u = u - u.mean(); v = v - v.mean()
            den = math.sqrt(float((u * u).sum() * (v * v).sum()))
            r = float((u * v).sum() / den) if den > 0 else 0.0
            if r > best:
                best, bl = r, L
        pk.append(best); lg.append(bl)
    if not pk:
        return 0.0, 0.0, 0.0
    return float(np.median(pk)), (1000.0 / float(np.median(lg)) if lg else 0.0), float(np.median(dp))


def mod_rate(x, a, b):
    """RATE: the envelope's own modulation frequency -- the high-passed (150 Hz)
    1 ms RMS over [a, b] s, detrended, Hann, its strongest spectral peak
    between 12 and 500 Hz. A creak's pulses come 17-83 a second; a note held
    by re-striking is modulated at its own re-strike rate (260 a second)."""
    np = _np()
    y = x[int(T0 * SR):]
    Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fr < 150] = 0
    h = np.fft.irfft(Y, len(y))
    H = int(0.001 * SR); n = len(h) // H
    e = np.sqrt((h[:n * H].reshape(n, H) ** 2).mean(axis=1))[int(round(a * 1000)):int(round(b * 1000))]
    if len(e) < 20:
        return 0.0
    k = np.arange(len(e))
    e = e - np.polyval(np.polyfit(k, e, 1), k)
    E = np.abs(np.fft.rfft(e * np.hanning(len(e)), 4096)); f = np.fft.rfftfreq(4096, 0.001)
    m = (f >= 12) & (f <= 500)
    return float(f[m][int(np.argmax(E[m]))])


def peak_band(x, a, b):
    """The centre of the 1/3-octave band (25 Hz-16 kHz) in which the voice over
    [a, b] s is loudest: its OWN band (a bimodal voice's centroid can fall
    between its halves)."""
    np = _np()
    from zenith_voice_lab import BANDS
    return float(BANDS[int(np.argmax(bands(x[int(a * SR):int(b * SR)])))])


def reattack(x):
    """RE-ATTACK: the largest 1 ms RMS peak >= 15 ms after the first peak that is
    >= 0.5 of it and >= 6 dB over the dip between. None if there is none."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + 0.3) * SR)]
    H = int(0.001 * SR); n = len(y) // H
    e = np.sqrt((y[:n * H].reshape(n, H) ** 2).mean(axis=1))
    i0 = int(np.argmax(e)); best = None
    for i in range(i0 + 15, n - 1):
        if e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] >= 0.5 * e[i0]:
            dip = float(e[i0:i].min())
            if db(e[i] / max(dip, 1e-12)) >= 6 and (best is None or e[i] > e[best]):
                best = i
    return None if best is None else (float(best - i0), float(e[best] / e[i0]))


def mreg(D_a, D_b):
    """REG between two lists of per-draw bands (median over draws), or one."""
    np = _np()
    if len(D_a) == 1 or len(D_b) == 1:
        return float(np.median([cos(p_, q_) for p_ in D_a for q_ in D_b]))
    return float(np.median([cos(D_a[i], D_b[i]) for i in range(min(len(D_a), len(D_b)))]))


# =============================================================== PICKING ===
FAILED: list = []

CAST_RULE = (
    "'0.5s': AUDIBLE 400-600 ms; 'rising': the rustle alone climbs (RISE-C >= +400 "
    "cents, its centroid 300 Hz-6 kHz) and the creak alone is HELD PITCH 63-77 Hz at "
    "its start and 81-99 Hz at its end (70 -> 90 +/- 10%); 'noise band-passed "
    "400-3k': BAND >= 0.50 on the WORST of twelve noise draws and TONAL <= 10 dB "
    "over 400-3000 Hz (noise -- 'not a chime'); 'a low creak under it': the creak "
    "alone's loudest 50 ms 1-12 dB under the rustle alone's (under it, not "
    "buried); 'not a crack': SWELL >= +3 dB (a crack's loudest 50 ms is its head). "
    "Register against rune-crack, each verdant cast, each flail cast, the hit @ "
    "18 and the death voice each <= 0.80. Level: TOP between 0.5x the hit @ 18's "
    "loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST (heard like a "
    "blow, never over one). Tiebreak: the most distinct register (the highest "
    "of those, to 0.05), then the fewest calls, then the order listed.")

BITE_RULE = (
    "At EVERY count 0-4: '60-90ms': AUDIBLE 60-90 ms; 'a snap': RISE <= 3 ms, "
    "the peak in the first 10 ms, and no RE-ATTACK (one snap a call: the number "
    "of snaps is the number of bites); 'peak <=0.45': the sample peak <= 0.45 on "
    "every noise draw; 'wet': a BODY that falls >= 300 cents from its first 20 "
    "ms to the snap's end and is heard (its loudest 50 ms within 12 dB of the "
    "whole's); heard but a small hit: loudest 50 ms >= 2x the wall tick's "
    "(loudest draw) on its quietest draw and <= 0.7x the hit @ 18's (quietest "
    "draw) on its loudest. 'pitched up a semitone per stack': every STEP n -> n "
    "+ 1 within 20 cents of +100 on the body AND within 25 cents on CRACK. "
    "Register (n = 2) against the hit @ 18, the wall, fork, hex-snap, the vine's "
    "plant, rune-crack and the picked cast each <= 0.80. Tiebreak: the lowest "
    "worst register (to 0.05), then the fewest calls, then the order listed.")

WITHER_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms; 'falling': FALL (its "
    "centroid, 1.5-16 kHz, last 100 audible ms re the first) <= -400 cents; "
    "'high-passed 1.5k': BELOW-1.5k <= 0.15 on the worst draw; 'dry': LOW <= "
    "0.02 on the worst draw (no body) and GONE as above (no tail); 'rustle': "
    "TONAL <= 10 dB over 1.5-12 kHz (noise, not a tone); 'quiet (peak <=0.3)': "
    "the sample peak <= 0.30 on every draw, its loudest 50 ms <= 0.5x the picked "
    "cast's and >= 2x the wall tick's (loudest draw) on its quietest draw. "
    "Register against rune-crack, the hit @ 18, the picked bite, the picked "
    "cast, Canopy's wither and Scour's woosh each <= 0.80 (the wall tick's is "
    "printed: it is high-passed noise too). Tiebreak: built "
    "as the picked cast's rustle is (the greening and the wither one sound run "
    "the other way: a chain for a chain, grains for grains), then the most "
    "distinct register (to 0.05), then the fewest calls, then the order listed.")

ROOT_RULE = (
    "'0.35s': AUDIBLE 290-420 ms; 'share below 120 Hz >= 0.4': LOW >= 0.40 on the "
    "WORST of twelve draws; 'a crack': the loudest HF millisecond STANDS >= 10 "
    "dB over the p90 of the HF before it and JUMPS >= 10 dB in 2 ms; 'into': it "
    "lands >= 100 ms after the onset; 'a creak': over [onset + 10 ms, crack - "
    "10 ms], RATE 17-83 a second (a pulse train at a creak's rate) and PULSED >= "
    "0.40 (100 ms windows), and the creak alone 1-12 dB under the crack alone (it "
    "leads in, heard). 'The biggest single "
    "thing the relic does': TOP >= 1 dB over the picked cast's, the picked "
    "wither's and the picked bite's loudest draw at any count, its LOW (render.py's "
    "draw) over the picked cast's, and TOP <= the hit @ 18's on its QUIETEST "
    "draw (never over a blow). Register against rune-crack, each verdant cast, "
    "each flail cast, the hit @ 18, the death voice, Deadfall's detonation, "
    "Paradox's pin, the picked cast, bite and wither each <= 0.80. Tiebreak: the "
    "most distinct register (to 0.05), "
    "then the fewest calls, then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 400 <= M["aud"] <= 600: why.append(f"audible {M['aud']:.0f} ms, not 400-600")
    if M["rise_c"] < 400: why.append(f"the rustle climbs {M['rise_c']:+.0f} c, not >= +400")
    if not 63 <= M["cf0"] <= 77: why.append(f"the creak starts at {M['cf0']:.0f} Hz, not 63-77")
    if not 81 <= M["cf1"] <= 99: why.append(f"the creak ends at {M['cf1']:.0f} Hz, not 81-99")
    if M["band_min"] < 0.50: why.append(f"band {M['band_min']:.2f} < 0.50")
    if M["tonal"] > 10: why.append(f"tonal {M['tonal']:.1f} dB > 10 (a chime)")
    if not -12 <= M["creak_db"] <= -1: why.append(f"creak {M['creak_db']:+.1f} dB re the rustle, not -12..-1")
    if M["swell"] < 3: why.append(f"swell {M['swell']:+.1f} dB < +3 (a crack)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def bite_why(M, lev):
    why = []
    for n, P_ in M["per"].items():
        if not 60 <= P_["aud"] <= 90: why.append(f"n{n} audible {P_['aud']:.0f} ms")
        if P_["rise"] > 3: why.append(f"n{n} rise {P_['rise']:.0f} ms")
        if P_["pk_ms"] > 10: why.append(f"n{n} peaks at {P_['pk_ms']:.0f} ms")
        if P_["re"] is not None: why.append(f"n{n} a second snap {P_['re'][0]:.0f} ms on at {P_['re'][1]:.2f}")
        if P_["pk_max"] > 0.45: why.append(f"n{n} peak {P_['pk_max']:.3f} > 0.45")
        if P_["body_fall"] is None: why.append(f"n{n} no body (dry)")
        else:
            if P_["body_fall"] > -300: why.append(f"n{n} body falls {P_['body_fall']:+.0f} c, not <= -300")
            if P_["body_db"] < -12: why.append(f"n{n} body {P_['body_db']:+.1f} dB, buried")
        if P_["top_hi"] > lev["hi"]: why.append(f"n{n} loudest 50 ms {P_['top_hi']:.4f} > {lev['hi']:.4f}")
        if P_["top_lo"] < lev["lo"]: why.append(f"n{n} loudest 50 ms {P_['top_lo']:.4f} < {lev['lo']:.4f}")
    for j, s_ in enumerate(M["step_body"]):
        if s_ is None or abs(s_ - 100) > 20: why.append(f"body step {j}->{j + 1} " + ("n/a" if s_ is None else f"{s_:+.0f} c"))
    for j, s_ in enumerate(M["step_crack"]):
        if abs(s_ - 100) > 25: why.append(f"crack step {j}->{j + 1} {s_:+.0f} c")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def wither_why(M, lev):
    why = []
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["gone"] > 470: why.append(f"gone at {M['gone']:.0f} ms")
    if M["fall"] > -400: why.append(f"fall {M['fall']:+.0f} c, not <= -400")
    if M["hp_max"] > 0.15: why.append(f"{M['hp_max']:.2f} below 1.5 kHz > 0.15")
    if M["low_max"] > 0.02: why.append(f"low {M['low_max']:.3f} > 0.02 (not dry)")
    if M["tonal"] > 10: why.append(f"tonal {M['tonal']:.1f} dB > 10 (a tone)")
    if M["pk_max"] > 0.30: why.append(f"peak {M['pk_max']:.3f} > 0.30")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def root_why(M, lev):
    why = []
    if not 290 <= M["aud"] <= 420: why.append(f"audible {M['aud']:.0f} ms, not 290-420")
    if M["low_min"] < 0.40: why.append(f"low {M['low_min']:.2f} < 0.40")
    if M["stand"] < 10: why.append(f"the crack stands {M['stand']:+.1f} dB, not >= 10")
    if M["jump"] < 10: why.append(f"the crack jumps {M['jump']:+.1f} dB, not >= 10")
    if M["crack_at"] - M["a0"] < 100: why.append(f"the crack at {M['crack_at']:.0f} ms, not >= 100 after the onset")
    if not 17 <= M["mrate"] <= 83: why.append(f"rate {M['mrate']:.0f} a second, not a creak's 17-83")
    if M["pulsed"] < 0.40: why.append(f"pulsed {M['pulsed']:.2f} < 0.40")
    if not -12 <= M["creak_db"] <= -1: why.append(f"creak {M['creak_db']:+.1f} dB re the crack, not -12..-1")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f} (not the biggest)")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f} (over a blow)")
    if M["low"] <= lev["low"]: why.append(f"low {M['low']:.2f} <= the cast's {lev['low']:.2f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-tendril-t3.html")
    ap.add_argument("--out", default="../05-reference/v101")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=101601)
    ap.add_argument("--e2e-seeds", type=int, default=1, help="fight seeds a pairing, end to end (0 skips it)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the four checked rows here")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "bite": BITE_RULE, "wither": WITHER_RULE,
                                      "root": ROOT_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickTendril bite", BITE_ANCHOR),
                    ("tickTendril wither", WITHER_ANCHOR), ("tickTendril root", ROOT_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if "bindweed-bite" in html or "bindweed-root" in html or "bindweed-wither" in html:
        raise SystemExit(f"{gp.name} already carries Tendril's voices -- run on stage 5")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nTENDRIL -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
        mirror = page.evaluate("() => { try { new AC.Match('bindweed', 'bindweed', 1); return 'allowed'; } "
                               "catch (e) { return 'refused: ' + e.message; } }")
        print(f"  the mirror match: {mirror}")
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if ME not in ids:
            raise SystemExit("no bindweed in this build")
        blade = page.evaluate("() => AC.WEAPONS.find(w => w.id === 'bindweed').dmg")
        if abs(blade - BLADE) > 1e-9:
            raise SystemExit(f"Bindweed's blade is {blade}, this lab levels against {BLADE}")

        def R(evs, secs=3.0, seed=None, rows=None, new=True):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            if new and len(evs) == 1 and e[0] in ("body", "arm"):
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
                                ("hit@18", ("hit", {"dmg": BLADE, "crit": False})),
                                ("wall", ("wall", {})), ("death", ("death", {})),
                                ("deadfall", ("ult", {"w": "nightfell-boom"})),
                                ("paradox-pin", ("ult", {"w": "paradox-pin"})),
                                ("canopy-wither", ("ult", {"w": "ironwood-wither"})),
                                ("chime", ("ult", {"w": "morningstar"}))]:
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
            raise SystemExit("Bindweed's cast is not rune-crack today -- this lab adds its arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_ for w_ in SCHOOL if w_ not in fall_ids]
        types = [w_ for w_ in TYPE if w_ not in fall_ids]
        print(f"  the verdant casts with their own voice: {', '.join(school)};  the flail row's: {', '.join(types)}")
        print(f"  Deadfall's detonation below 120 Hz: {ctl['deadfall']['low']:.2f} -- the spec's 0.4 is the "
              f"root's gate; the detonation is its standing, not its number")

        # the noise draws of every reference
        REFS = {"hit@18": ("hit", {"dmg": BLADE, "crit": False}), "wall": ("wall", {}),
                "rune-crack": ("ult", {"w": "spellbreaker"}), "death": ("death", {}),
                "fork": ("fork", {}), "hex-snap": ("hex-snap", {}), "vine-plant": ("vine", {"plant": True}),
                "deadfall": ("ult", {"w": "nightfell-boom"}), "paradox-pin": ("ult", {"w": "paradox-pin"}),
                "canopy-wither": ("ult", {"w": "ironwood-wither"}), "woosh": ("scour-woosh", {"n": 0})}
        for w_ in school + types:
            REFS[w_] = ("ult", {"w": w_})
        RD = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (kind, p) in REFS.items():
                RD[k].append(basic(play(kind, p, seed=sd)))
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD.items()}
        h_lo, h_hi = min(m_["top"] for m_ in RD["hit@18"]), max(m_["top"] for m_ in RD["hit@18"])
        w_hi = max(m_["top"] for m_ in RD["wall"])
        print(f"  the hit @ 18 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD['hit@18']):.3f}-{max(m_['peak'] for m_ in RD['hit@18']):.3f};  "
              f"the wall tick: {min(m_['top'] for m_ in RD['wall']):.4f}-{w_hi:.4f}")
        row_ids = school + types
        pr = {f"{p_}/{q_}": mreg(RB[p_], RB[q_]) for i_, p_ in enumerate(row_ids) for q_ in row_ids[i_ + 1:]}
        print(f"  the verdant and flail casts' own registers, pairwise: median {float(np.median(list(pr.values()))):.2f}, "
              f"max {max(pr.values()):.2f} ({max(pr, key=pr.get)}); the gate is 0.80")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        rec["levels"] = dict(hit18=[h_lo, h_hi], wall_hi=w_hi, row_regs_median=float(np.median(list(pr.values()))))
        wav("bindweed-ctl-runecrack.wav", rcx)
        wav("bindweed-ctl-hit18.wav", ctl["hit@18"]["x"])
        wav("bindweed-ctl-deadfall.wav", ctl["deadfall"]["x"])
        wav("bindweed-ctl-paradox-pin.wav", ctl["paradox-pin"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a rising rustle-and-creak, 0.5s, noise band-passed 400-3k with a low creak under it'. "
              f"Level-matched: the creak alone {CREAK_UNDER_DB:g} dB under the rustle alone, TOP {tgt_c:.4f} (the "
              f"centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f})")

        def cx(sp, g, kc, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kc, part), {}]], seed=seed)

        def calib_cast(sp):
            g, kc = 0.1, 0.5
            for _ in range(4):
                rt = basic(cx(sp, g, kc, "rustle")[0])["top"]; ct = basic(cx(sp, g, kc, "creak")[0])["top"]
                kc = float(f"{kc * rt * 10 ** (-CREAK_UNDER_DB / 20) / ct:.4g}")
                g = float(f"{g * tgt_c / basic(cx(sp, g, kc)[0])['top']:.4g}")
            return g, kc

        CAST_REGS = ["rune-crack"] + school + types + ["hit@18", "death"]

        def cast_measure(name, x, draws, rus, cre, calls):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            M["band_min"] = min(band_share(d_, 400, 3000) for d_ in draws)
            M["tonal"] = tonal(draws, T0, T0 + 0.6, 400, 3000)
            M["swell"] = db(M["top"] / max(M["start"], 1e-12))
            if rus is not None:
                Br = basic(rus); ra0 = T0 + Br["a0"] / 1000; ra1 = T0 + Br["gone"] / 1000
                M["rise_c"] = cents(centroid(rus, ra1 - 0.1, ra1, 300, 6000), centroid(rus, ra0, ra0 + 0.1, 300, 6000))
            else:
                M["rise_c"] = -9999.0; Br = None
            if cre is not None:
                Bc = basic(cre); ca0 = T0 + Bc["a0"] / 1000; ca1 = T0 + Bc["gone"] / 1000
                M["cf0"] = pitch(cre, ca0, ca0 + 0.1, 40, 130); M["cf1"] = pitch(cre, ca1 - 0.1, ca1, 40, 130)
            else:
                M["cf0"] = M["cf1"] = 0.0; Bc = None
            M["creak_db"] = db(Bc["top"] / Br["top"]) if (Br and Bc) else (-99.0 if Br else 99.0)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CAST_REGS}
            return M

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<12}{M.get('g', 0):>8.4g}{M.get('kc', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['aud']:>6.0f}{M['rise_c']:>7.0f}{M['cf0']:>6.1f}{M['cf1']:>6.1f}{M['band_min']:>6.2f}"
                  f"{M['tonal']:>6.1f}{M['creak_db']:>7.1f}{M['swell']:>6.1f}{max(r_.values()):>6.2f} "
                  f"({max(r_, key=r_.get)})")

        print(f"  {'cand':<12}{'g':>8}{'kc':>8}{'calls':>6}{'top':>8}{'aud':>6}{'rise c':>7}{'cf0':>6}{'cf1':>6}"
              f"{'bandW':>6}{'tonal':>6}{'crk dB':>7}{'swell':>6}{'reg':>6}")
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g, kc = calib_cast(sp)
            x, calls = cx(sp, g, kc)
            x2, _ = cx(sp, g, kc)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"cast {name} does not reproduce")
            draws = [cx(sp, g, kc, seed=sd)[0] for sd in NOISE_SEEDS]
            M = cast_measure(name, x, draws, cx(sp, g, kc, "rustle")[0], cx(sp, g, kc, "creak")[0], calls[0])
            M.update(sp=sp, g=g, kc=kc); M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"bindweed-cast-{name.replace(' ', '-').lower()}.wav", x)
        # the controls: the second candidate's halves, it run downward, and the chime
        c0 = rows_c[1]
        ctlc = []
        rx = cx(c0["sp"], c0["g"], c0["kc"], "rustle")[0]
        M = cast_measure("0 RUSTLE", rx, [cx(c0["sp"], c0["g"], c0["kc"], "rustle", seed=sd)[0] for sd in NOISE_SEEDS],
                         rx, None, 3); ctlc.append(M)
        kx = cx(c0["sp"], c0["g"], c0["kc"], "creak")[0]
        M = cast_measure("0 CREAK", kx, [kx], None, kx, 40); ctlc.append(M)
        dsp = dict(c0["sp"], dir="down")
        fx_, fc_ = cx(dsp, c0["g"], c0["kc"])
        M = cast_measure("0 FALL", fx_, [cx(dsp, c0["g"], c0["kc"], seed=sd)[0] for sd in NOISE_SEEDS],
                         cx(dsp, c0["g"], c0["kc"], "rustle")[0], cx(dsp, c0["g"], c0["kc"], "creak")[0], fc_[0])
        ctlc.append(M)
        chx = ctl["chime"]["x"]
        M = cast_measure("0 CHIME", chx, [chx], chx, chx, 0); ctlc.append(M)
        M = cast_measure("0 RUNECRACK", rcx, [play("ult", {"w": "spellbreaker"}, seed=sd) for sd in NOISE_SEEDS],
                         rcx, rcx, 0); ctlc.append(M)
        for M in ctlc:
            M["why"] = cast_why(M, lev_c); cast_line(M)
        wav("bindweed-cast-0-fall.wav", fx_)
        # the reference BAND's gate is read against: the prose's band built LITERALLY
        lit = ('const g = 0.1;\n'
               'this._sweep(t, { f0: 1095, f1: 1095, q: 0.421, gain: g, dur: 0.5, atk: 0.3, type:"bandpass" });')
        lit_band = min(band_share(R([["body", T0, lit, {}]], seed=sd)[0], 400, 3000) for sd in NOISE_SEEDS)
        print(f"  LITERAL -- a reference, not a candidate: noise band-passed with its -3 dB edges AT 400 and 3000 Hz "
              f"(the toolkit's biquad at 1095 Hz, Q 0.42), held: BAND {lit_band:.2f} at its worst draw. A 2nd-order "
              f"bandpass keeps half its power inside its own -3 dB band, so the gate is 0.50, not the first cut's 0.70")
        rec["literal_band"] = lit_band
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<12} {blurb}")
        print("    0 RUSTLE     CHAIN-TRI's rustle alone -- a control\n"
              "    0 CREAK      its creak alone -- a control\n"
              "    0 FALL       CHAIN-TRI run downward (the bands falling, the creak 90 -> 70 Hz) -- a control\n"
              "    0 CHIME      Morningstar's cast, a bright swell: 'not a chime' -- a control\n"
              "    0 RUNECRACK  the fallback it replaces, a crack: 'not a crack' -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<12} out: {'; '.join(M['why'])}")
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
        C_["low"] = low_share(C_["x"])
        print(f"  PICK  {C_['name']}  g {C_['g']}, kc {C_['kc']}, {C_['calls']} synth calls; TOP {C_['top']:.4f} = "
              f"{db(C_['top'] / h_lo):+.1f} dB re the hit @ 18 (quietest draw), {db(C_['top'] / w_hi):+.1f} dB re "
              f"the wall; LOW {C_['low']:.2f}")

        # ---- THE BITE ------------------------------------------------------
        lev_b = dict(lo=2 * w_hi, hi=0.7 * h_lo)
        tgt_b = math.sqrt(lev_b["lo"] * lev_b["hi"])
        print(f"\nBITE -- 'a short wet snap, 60-90ms, peak <=0.45, pitched up a semitone per entangle stack'. "
              f"Level-matched at n = {BITE_REF_N}: audible {BITE_AUD_MS:g} ms, loudest 50 ms {tgt_b:.4f} (the "
              f"centre of {lev_b['lo']:.4f}-{lev_b['hi']:.4f})")

        def bx(sp, g, D, n, part="both", seed=None, flat=False):
            return R([["body", T0, bite_body(sp, g, D, part, flat), {"n": n}]], seed=seed)

        def calib_bite(sp, flat=False):
            g, D = 0.1, 0.15
            for _ in range(5):
                if not sp.get("dry"):
                    D = float(f"{D * BITE_AUD_MS / basic(bx(sp, g, D, BITE_REF_N, flat=flat)[0])['aud']:.3g}")
                g = float(f"{g * tgt_b / basic(bx(sp, g, D, BITE_REF_N, flat=flat)[0])['top']:.4g}")
            return g, D

        BITE_REGS = ["hit@18", "wall", "fork", "hex-snap", "vine-plant", "rune-crack"]

        def bite_measure(name, sp, g, D, flat=False):
            M = dict(name=name, sp=sp, g=g, D=D, per={}, flat=flat)
            xs, dr = {}, {}
            for n in NS:
                x, calls = bx(sp, g, D, n, flat=flat)
                draws = [bx(sp, g, D, n, seed=sd, flat=flat)[0] for sd in NOISE_SEEDS]
                B = basic(x)
                P_ = dict(aud=B["aud"], rise=B["rise"], pk_ms=B["pk_ms"], top=B["top"], re=reattack(x),
                          pk_max=max(float(np.abs(d_).max()) for d_ in draws),
                          top_hi=max(basic(d_)["top"] for d_ in draws), top_lo=min(basic(d_)["top"] for d_ in draws))
                if sp.get("dry"):
                    P_.update(body_fall=None, body_db=-99.0, bf0=None)
                else:
                    bd = bx(sp, g, D, n, "body", flat=flat)[0]
                    g1 = T0 + B["gone"] / 1000
                    P_["bf0"] = pitch(bd, T0 + 0.002, T0 + 0.022, 100, 6000)
                    P_["body_fall"] = cents(pitch(bd, g1 - 0.025, g1, 100, 6000), P_["bf0"])
                    P_["body_db"] = db(basic(bd)["top"] / B["top"])
                M["per"][n] = P_
                xs[n], dr[n] = x, draws
                if n == BITE_REF_N:
                    M["calls"] = calls[0]; M["x"] = x; M["top"] = B["top"]
                    M["DB"] = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["xs"] = xs
            M["step_body"] = [(cents(M["per"][n + 1]["bf0"], M["per"][n]["bf0"]) if M["per"][n]["bf0"] else None)
                              for n in NS[:-1]]
            M["step_crack"] = [crack_shift(dr[n + 1], dr[n]) for n in NS[:-1]]
            M["regs"] = {k: mreg(M["DB"], RB[k]) for k in BITE_REGS}
            M["regs"]["cast"] = mreg(M["DB"], C_["DB"])
            return M

        def bite_line(M):
            per = M["per"]; r_ = M["regs"]
            auds = "/".join(f"{per[n]['aud']:.0f}" for n in NS)
            fl = min((per[n]["body_fall"] for n in NS if per[n]["body_fall"] is not None), default=float("nan"), key=abs)
            sb = "/".join("--" if s_ is None else f"{s_:.0f}" for s_ in M["step_body"])
            sc = "/".join(f"{s_:.0f}" for s_ in M["step_crack"])
            print(f"  {M['name']:<9}{M['g']:>8.4g}{M['D']:>7.3g}{M.get('calls', 0):>6d}{auds:>16}"
                  f"{max(per[n]['pk_max'] for n in NS):>7.3f}{fl:>7.0f}{min(per[n]['body_db'] for n in NS):>7.1f}"
                  f"{sb:>17}{sc:>17}{min(per[n]['top_lo'] for n in NS):>8.4f}-{max(per[n]['top_hi'] for n in NS):<7.4f}"
                  f"{max(r_.values()):>5.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<9}{'g':>8}{'D':>7}{'calls':>6}{'aud n0-4 ms':>16}{'pk max':>7}{'fall':>7}{'body':>7}"
              f"{'body steps c':>17}{'crack steps c':>17}{'loudest 50 ms':>16}{'reg':>6}")
        rows_b = []
        for name, sp, _b in BITE_CANDIDATES:
            g, D = calib_bite(sp)
            x1, _ = bx(sp, g, D, BITE_REF_N); x2, _ = bx(sp, g, D, BITE_REF_N)
            if float(np.abs(x1 - x2).max()) > 1e-6:
                raise SystemExit(f"bite {name} does not reproduce")
            M = bite_measure(name, sp, g, D); M["why"] = bite_why(M, lev_b)
            rows_b.append(M); bite_line(M)
            for n in (1, 4):
                wav(f"bindweed-bite-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        s0 = rows_b[0]
        dry = dict(s0["sp"], dry=True)
        gd, Dd = calib_bite(dry)
        ctlb = [bite_measure("0 DRY", dry, gd, Dd), bite_measure("0 FLAT", s0["sp"], s0["g"], s0["D"], flat=True)]
        for M in ctlb:
            M["why"] = bite_why(M, lev_b); bite_line(M)
        wav("bindweed-bite-0-dry.wav", ctlb[0]["xs"][2])
        for (name, _sp, blurb) in BITE_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 DRY     SNAP's snap with no body -- a control\n"
              "    0 FLAT    SNAP at one pitch for every count -- a control")
        print(f"  RULE  {BITE_RULE}")
        for M in rows_b:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'][:6])}" + (" ..." if len(M["why"]) > 6 else ""))
        for M in ctlb:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_b, "bite")
        bi = fb if ok is None else min(ok, key=lambda i: (round(max(rows_b[i]["regs"].values()) / 0.05),
                                                          rows_b[i]["calls"]))
        B_ = rows_b[bi]
        bt_hi = max(B_["per"][n]["top_hi"] for n in NS)
        print(f"  PICK  {B_['name']}  g {B_['g']}, D {B_['D']} s; at n = {BITE_REF_N} loudest 50 ms "
              f"{db(B_['top'] / h_lo):+.1f} dB re the hit @ 18, {db(B_['top'] / w_hi):+.1f} dB re the wall; body "
              f"pitches n0-4 " + "/".join(f"{B_['per'][n]['bf0']:.0f}" for n in NS) + " Hz")

        # ---- THE WITHER ----------------------------------------------------
        cast_top = C_["top"]
        lev_w = dict(hi=0.5 * cast_top, lo=2 * w_hi)
        tgt_w = cast_top * 10 ** (-WITHER_UNDER_DB / 20)
        print(f"\nWITHER -- 'a dry falling rustle, 0.4s, high-passed 1.5k, quiet (peak <=0.3)'. Level-matched "
              f"{WITHER_UNDER_DB:g} dB under the cast's top ({tgt_w:.4f})")

        def wx(sp, g, seed=None):
            return R([["body", T0, wither_body(sp, g), {}]], seed=seed)

        def calib_wither(sp):
            g = 0.1
            for _ in range(4):
                g = float(f"{g * tgt_w / basic(wx(sp, g)[0])['top']:.4g}")
            return g

        WITHER_REGS = ["rune-crack", "hit@18", "canopy-wither", "woosh"]

        def wither_measure(name, x, draws, calls):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            a0 = T0 + M["a0"] / 1000; a1 = T0 + M["gone"] / 1000
            M["fall"] = cents(centroid(x, a1 - 0.1, a1, 1500, 16000), centroid(x, a0, a0 + 0.1, 1500, 16000))
            M["hp_max"] = max(share_below(d_, 1500) for d_ in draws)
            M["low_max"] = max(low_share(d_) for d_ in draws)
            M["tonal"] = tonal(draws, T0, T0 + 0.5, 1500, 12000)
            M["pk_max"] = max(float(np.abs(d_).max()) for d_ in draws)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in WITHER_REGS}
            M["regs"]["bite"] = mreg(DB, B_["DB"])
            M["regs"]["cast"] = mreg(DB, C_["DB"])
            M["reg_wall"] = mreg(DB, RB["wall"])
            return M

        def wither_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<11}{M.get('g', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{db(M['top'] / cast_top):>8.1f}"
                  f"{M['aud']:>5.0f}{M['gone']:>6.0f}{M['fall']:>7.0f}{M['hp_max']:>7.2f}{M['low_max']:>7.3f}"
                  f"{M['tonal']:>7.1f}{M['pk_max']:>7.3f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})"
                  f"   wall {M['reg_wall']:.2f}")

        print(f"  {'cand':<11}{'g':>8}{'calls':>6}{'top':>8}{'dB/cast':>8}{'aud':>5}{'gone':>6}{'fall c':>7}"
              f"{'<1.5kW':>7}{'lowW':>7}{'tonal':>7}{'pk max':>7}{'reg':>6}")
        rows_w = []
        for name, sp, _b in WITHER_CANDIDATES:
            g = calib_wither(sp)
            x, calls = wx(sp, g)
            x2, _ = wx(sp, g)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"wither {name} does not reproduce")
            M = wither_measure(name, x, [wx(sp, g, seed=sd)[0] for sd in NOISE_SEEDS], calls[0])
            M.update(g=g, sp=sp); M["why"] = wither_why(M, lev_w)
            rows_w.append(M); wither_line(M)
            wav(f"bindweed-wither-{name.replace(' ', '-').lower()}.wav", x)
        w0 = rows_w[0]
        rsp = dict(w0["sp"], dir="up")
        xr, cr_ = wx(rsp, w0["g"])
        RI = wither_measure("0 RISE", xr, [wx(rsp, w0["g"], seed=sd)[0] for sd in NOISE_SEEDS], cr_[0])
        RI["g"] = w0["g"]
        cwx = ctl["canopy-wither"]["x"]
        CW = wither_measure("0 CANOPY", cwx, [cwx], 0)
        gq = float(f"{C_['g'] * 10 ** (-WITHER_UNDER_DB / 20):.4g}")
        xq, cq_ = cx(C_["sp"], gq, C_["kc"])
        CQ = wither_measure("0 CASTQ", xq, [cx(C_["sp"], gq, C_["kc"], seed=sd)[0] for sd in NOISE_SEEDS], cq_[0])
        CQ["g"] = gq
        for M in (RI, CW, CQ):
            M["why"] = wither_why(M, lev_w); wither_line(M)
        wav("bindweed-wither-0-rise.wav", xr)
        for (name, _sp, blurb) in WITHER_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 RISE     CHAIN run upward -- a control\n"
              "    0 CANOPY   Canopy's wither, 'a dry creak falling in pitch' -- a tone, a control\n"
              "    0 CASTQ    the picked cast at 9 dB under its top -- a control")
        print(f"  gates: loudest 50 ms {lev_w['lo']:.4f}-{lev_w['hi']:.4f}")
        print(f"  RULE  {WITHER_RULE}")
        for M in rows_w:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in (RI, CW, CQ):
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_w, "wither")
        same_build = {"chain": "chain", "sweep": "chain", "grain": "grain"}[C_["sp"]["rustle"]]
        wi = fb if ok is None else min(ok, key=lambda i: (0 if rows_w[i]["sp"]["kind"] == same_build else 1,
                                                          round(max(rows_w[i]["regs"].values()) / 0.05),
                                                          rows_w[i]["calls"]))
        W_ = rows_w[wi]
        print(f"  PICK  {W_['name']}  g {W_['g']}; {db(W_['top'] / cast_top):+.1f} dB re the cast's top, "
              f"{db(W_['top'] / h_lo):+.1f} re the hit @ 18, {db(W_['top_lo'] / w_hi):+.1f} re the wall; fall "
              f"{W_['fall']:+.0f} c")

        # ---- THE ROOT ------------------------------------------------------
        loud = {"cast": C_["top"], "bite": bt_hi, "wither": max(basic(wx(W_["sp"], W_["g"], seed=sd)[0])["top"]
                                                                for sd in NOISE_SEEDS)}
        lev_r = dict(lo=max(loud.values()) * 10 ** (1 / 20), hi=h_lo, low=C_["low"])
        tgt_r = math.sqrt(lev_r["lo"] * lev_r["hi"])
        print(f"\nROOT -- 'a low creak into a crack, 0.35s, share below 120 Hz >= 0.4'. Level-matched: the creak "
              f"alone {ROOT_CREAK_UNDER_DB:g} dB under the crack alone, TOP {tgt_r:.4f} (the centre of "
              f"{lev_r['lo']:.4f}, 1 dB over the relic's loudest other voice ({max(loud, key=loud.get)}), and "
              f"{lev_r['hi']:.4f}, the hit @ 18's quietest draw)")
        if lev_r["lo"] >= lev_r["hi"]:
            print("  THE ROOT'S LEVEL WINDOW IS EMPTY -- the relic's other voices are already as loud as its blow")
            FAILED.append("root level window")

        def rx(sp, g, kc, kt, part="both", seed=None, order="into", held=False):
            return R([["body", T0, root_body(sp, g, kc, kt, part, order, held), {}]], seed=seed)

        def calib_root(sp, held=False):
            """the weight (kt) so LOW is ROOT_LOW_TARGET, the creak (kc) 6 dB under
            the crack, the gain (g) to the centre of the window; four passes"""
            g, kc, kt = 0.2, 0.5, 1.0
            for _ in range(4):
                lo_, hi_ = math.log(1e-2), math.log(1e2)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if low_share(rx(sp, g, kc, math.exp(mid), held=held)[0]) > ROOT_LOW_TARGET: hi_ = mid
                    else: lo_ = mid
                kt = float(f"{math.exp(0.5 * (lo_ + hi_)):.4g}")
                ct = basic(rx(sp, g, kc, kt, "crack", held=held)[0])["top"]
                kk = basic(rx(sp, g, kc, kt, "creak", held=held)[0])["top"]
                kc = float(f"{kc * ct * 10 ** (-ROOT_CREAK_UNDER_DB / 20) / kk:.4g}")
                g = float(f"{g * tgt_r / basic(rx(sp, g, kc, kt, held=held)[0])['top']:.4g}")
            return g, kc, kt

        ROOT_REGS = ["rune-crack"] + school + types + ["hit@18", "death", "deadfall", "paradox-pin"]

        def root_measure(name, x, draws, calls, c, creak=None, crack=None):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            M["low"] = low_share(x); M["low_min"] = min(low_share(d_) for d_ in draws)
            M["crack_at"], M["stand"], M["jump"] = crack_info(x, M["a0"])
            a = M["a0"] / 1000 + 0.01; b = min(c, M["crack_at"] / 1000) - 0.01
            M["pulsed"], M["rate"], M["depth"] = pulsed_w(x, a, b) if b - a >= 0.0999 else (0.0, 0.0, 0.0)
            M["mrate"] = mod_rate(x, a, b) if b - a >= 0.05 else 0.0
            if creak is not None and crack is not None:
                M["creak_db"] = db(basic(creak)["top"] / basic(crack)["top"])
            else:
                M["creak_db"] = -99.0 if creak is None else 99.0
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in ROOT_REGS}
            for k, X in (("cast", C_), ("bite", B_), ("wither", W_)):
                M["regs"][k] = mreg(DB, X["DB"])
            return M

        def root_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M.get('g', 0):>8.4g}{M.get('kc', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['aud']:>6.0f}{M['low']:>6.2f}{M['low_min']:>6.2f}{M['crack_at']:>7.0f}{M['stand']:>7.1f}"
                  f"{M['jump']:>6.1f}{M['pulsed']:>7.2f}{M['mrate']:>6.0f}{M['depth']:>6.1f}{M['creak_db']:>7.1f}"
                  f"{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<10}{'g':>8}{'kc':>8}{'calls':>6}{'top':>8}{'aud':>6}{'low':>6}{'lowW':>6}{'crk@':>7}"
              f"{'stand':>7}{'jump':>6}{'pulse':>7}{'rate':>6}{'depth':>6}{'crk dB':>7}{'reg':>6}")
        rows_r = []
        for name, sp, _b in ROOT_CANDIDATES:
            g, kc, kt = calib_root(sp)
            x, calls = rx(sp, g, kc, kt)
            x2, _ = rx(sp, g, kc, kt)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"root {name} does not reproduce")
            M = root_measure(name, x, [rx(sp, g, kc, kt, seed=sd)[0] for sd in NOISE_SEEDS], calls[0], sp["c"],
                             rx(sp, g, kc, kt, "creak")[0], rx(sp, g, kc, kt, "crack")[0])
            M.update(sp=sp, g=g, kc=kc, kt=kt); M["why"] = root_why(M, lev_r)
            rows_r.append(M); root_line(M)
            wav(f"bindweed-root-{name.replace(' ', '-').lower()}.wav", x)
        r1 = rows_r[1]                                    # BEAM: the controls are built on it
        sp1, g1, k1, t1 = r1["sp"], r1["g"], r1["kc"], r1["kt"]
        ctlr = []
        xk_ = rx(sp1, g1, k1, t1, "crack")[0]
        ctlr.append(root_measure("0 CRACK", xk_, [rx(sp1, g1, k1, t1, "crack", seed=sd)[0] for sd in NOISE_SEEDS],
                                 3, sp1["c"], None, xk_))
        xc_ = rx(sp1, g1, k1, t1, "creak")[0]
        ctlr.append(root_measure("0 CREAK", xc_, [xc_], 20, sp1["c"], xc_, None))
        xb_ = rx(sp1, g1, k1, t1, order="back")[0]
        ctlr.append(root_measure("0 BACK", xb_, [rx(sp1, g1, k1, t1, order="back", seed=sd)[0] for sd in NOISE_SEEDS],
                                 23, sp1["c"], rx(sp1, g1, k1, t1, "creak", order="back")[0],
                                 rx(sp1, g1, k1, t1, "crack", order="back")[0]))
        gh, kh, th = calib_root(sp1, held=True)
        xh_ = rx(sp1, gh, kh, th, held=True)[0]
        M = root_measure("0 HELD", xh_, [rx(sp1, gh, kh, th, held=True, seed=sd)[0] for sd in NOISE_SEEDS], 50,
                         sp1["c"], rx(sp1, gh, kh, th, "creak", held=True)[0],
                         rx(sp1, gh, kh, th, "crack", held=True)[0])
        M.update(g=gh, kc=kh, kt=th); ctlr.append(M)
        for M in ctlr:
            M["why"] = root_why(M, lev_r); root_line(M)
        wav("bindweed-root-0-back.wav", xb_)
        wav("bindweed-root-0-held.wav", xh_)
        for (name, _sp, blurb) in ROOT_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 CRACK    BEAM's crack alone -- a control\n"
              "    0 CREAK    its creak alone -- a control\n"
              "    0 BACK     the crack first, the creak after it -- a control on 'into'\n"
              "    0 HELD     the creak as a HELD 260 Hz tone, no stick-slip -- a control on 'a creak'")
        print(f"  gates: loudest 50 ms {lev_r['lo']:.4f}-{lev_r['hi']:.4f}, LOW over the cast's {lev_r['low']:.2f}")
        print(f"  RULE  {ROOT_RULE}")
        for M in rows_r:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlr:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_r, "root")
        ri = fb if ok is None else min(ok, key=lambda i: (round(max(rows_r[i]["regs"].values()) / 0.05),
                                                          rows_r[i]["calls"]))
        R_ = rows_r[ri]
        print(f"  PICK  {R_['name']}  g {R_['g']}, kc {R_['kc']}, kt {R_['kt']}; TOP {db(R_['top'] / h_lo):+.1f} dB re the hit @ 18, "
              f"{db(R_['top'] / max(loud.values())):+.1f} dB over the loudest other voice; LOW {R_['low_min']:.2f} "
              f"worst draw (Deadfall's detonation {ctl['deadfall']['low']:.2f})")

        # ---- THE ROOT AND THE WITHER ON ONE FRAME ---------------------------
        rb = root_body(R_["sp"], R_["g"], R_["kc"], R_["kt"]); wb = wither_body(W_["sp"], W_["g"])
        both = R([["body", T0, rb, {}], ["body", T0, wb, {}]])[0]
        fw = peak_band(W_["x"], T0, T0 + 0.4)
        fr_ = peak_band(R_["x"], T0, T0 + 0.35)
        keep_w = db(band_rms(both, fw, T0, T0 + 0.4) / band_rms(R_["x"], fw, T0, T0 + 0.4))
        keep_r = db(band_rms(both, fr_, T0, T0 + 0.35) / band_rms(W_["x"], fr_, T0, T0 + 0.35))
        own_w = db(band_rms(both, fw, T0, T0 + 0.4) / band_rms(W_["x"], fw, T0, T0 + 0.4))
        own_r = db(band_rms(both, fr_, T0, T0 + 0.35) / band_rms(R_["x"], fr_, T0, T0 + 0.35))
        print(f"\nTHE ROOT AND THE WITHER ON ONE FRAME (a rooting close plays both): the wither lifts its own "
              f"third-octave ({fw:.0f} Hz) {keep_w:+.1f} dB over the root alone, and the root its own ({fr_:.0f} Hz) "
              f"{keep_r:+.1f} dB over the wither alone; each moves {own_w:+.1f} / {own_r:+.1f} dB from itself alone")
        rec["coplay"] = dict(wither_over_root=keep_w, root_over_wither=keep_r, wither_self=own_w, root_self=own_r)
        wav("bindweed-root-and-wither.wav", both)

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        def what_cast(sp):
            r_ = {"chain": "Three overlapping bandpass sweeps climb 400 -> 900, 800 -> 1700 and 1500 -> 3000 Hz, "
                           "each louder than the last;",
                  "sweep": "One bandpass sweep climbs 400 -> 3000 Hz over 0.56 s;",
                  "grain": "Leaves: 35 ms bandpass grains about fifty a second, the band climbing 400 -> 3000 "
                           "Hz and the level with it;"}[sp["rustle"]]
            c_ = {"held": f"under it a {sp['wave']} held by re-striking at its own cycles (a held note does "
                          f"not exist in this toolkit, CLAUDE.md 4.5), gliding 70 -> 90 Hz and swelling.",
                  "fry": f"under it a {sp['wave']} re-struck at a creak's rate, quickening 33 -> 55 a second, "
                         f"each strike 70 -> 90 Hz."}[sp["creak"]]
            return r_ + " " + c_
        bite_what = {"snap": "A 12 ms bandpass snap at 2.4 kHz over a sine body falling A5 -> A4 (the score's A, "
                             "a semitone up per stack: A#5 on a clean foe's first bite, C#6 at the cap).",
                     "twig": "A 6 ms highpass click over a triangle body falling E5 -> E4, a semitone up per stack.",
                     "split": "The house's wet split (`fork`) at its own ratios, a semitone up per stack.",
                     "plop": "A ringing snap (bandpass noise at Q 9, 1100 Hz) over a sine falling 1100 -> 550 "
                             "Hz, a semitone up per stack."}[B_["sp"]["body"]]
        th0, th1, _thd = R_["sp"]["thud"]
        root_what = {"knock": "A 150 Hz triangle knock pulsed for",
                     "beam": "Canopy's timber an octave and a half down (a 260 Hz sine and its 2.76 mode at "
                             "0.4) pulsed for",
                     "low": "The creak itself low, an 85 Hz triangle, pulsed for"}[R_["sp"]["pulse"]] + \
            f" {R_['sp']['c']:g} s, then the crack: a 35 ms highpass snap over a sine falling {th0} -> {th1} Hz" + \
            (f" and a {R_['sp']['lp']} Hz lowpass burst" if R_["sp"].get("lp") else "") + \
            ", the weight under the death voice's 120 Hz start so it never reads as a death."
        wither_what = {("chain", "bandpass"): "three overlapping bandpass sweeps (Q 0.9) falling 7 -> 4.8, 5 -> "
                                              "3.4 and 3.6 -> 2.4 kHz, each quieter -- the cast's chain run "
                                              "downward.",
                       ("chain", "highpass"): "three overlapping highpass sweeps, the cutoff falling 6 kHz -> "
                                              "1.5 kHz -- the cast's chain run downward.",
                       ("grain", "highpass"): "leaves dropping: 12 ms highpass grains thinning 50 -> 22 a "
                                              "second, the cutoff falling 6 kHz -> 1.5 kHz.",
                       ("grain", "bandpass"): "flakes: 12 ms bandpass grains (Q 1.5) thinning 50 -> 22 a "
                                              "second, the band falling 7 -> 2.2 kHz."}[
            (W_["sp"]["kind"], W_["sp"]["type"])]
        per = B_["per"]
        info = dict(
            n_rc=["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                  "twelve"][min(12, len(fall_ids) - 1)],
            c_what=what_cast(C_["sp"]), c_rise=C_["rise_c"], c_f0=C_["cf0"], c_f1=C_["cf1"],
            c_creak=C_["creak_db"], c_band=C_["band_min"], c_tonal=C_["tonal"], c_swell=C_["swell"],
            c_aud=C_["aud"], c_db=db(C_["top"] / h_lo), c_reg=max(C_["regs"].values()),
            b_what=bite_what, b_aud="-".join(f"{v:.0f}" for v in (min(per[n]["aud"] for n in NS),
                                                                   max(per[n]["aud"] for n in NS))),
            b_pk=max(per[n]["pk_max"] for n in NS),
            b_fall=max((per[n]["body_fall"] for n in NS if per[n]["body_fall"] is not None), default=0.0),
            b_step=" to ".join(sorted({f"{v:+.0f}" for v in (
                min([s_ for s_ in B_["step_body"] if s_ is not None] or [0]),
                max([s_ for s_ in B_["step_body"] if s_ is not None] or [0]))})),
            b_db=db(B_["top"] / h_lo), b_wall=db(min(per[n]["top_lo"] for n in NS) / w_hi),
            b_reg=max(B_["regs"].values()),
            r_what=root_what, r_pulsed=R_["pulsed"], r_depth=R_["depth"], r_creak=R_["creak_db"],
            r_at=R_["crack_at"], r_stand=R_["stand"], r_low=R_["low_min"], r_aud=R_["aud"],
            r_db=db(R_["top"] / h_lo), r_over=db(R_["top"] / max(loud.values())), r_reg=max(R_["regs"].values()),
            r_death=R_["regs"]["death"],
            r_regk={"redflail": "Threshmaw", "gravemourn": "Gravemourn", "slagheart": "Slagheart",
                    "paradox": "Paradox", "morningstar": "Morningstar", "ironwood": "Ironwood",
                    "thornwake": "Thornwake", "vinesower": "Vinesower", "thornshear": "Thornshear"}.get(
                max(R_["regs"], key=R_["regs"].get), max(R_["regs"], key=R_["regs"].get)),
            w_what=wither_what, w_fall=W_["fall"], w_hp=W_["hp_max"], w_low=W_["low_max"], w_tonal=W_["tonal"],
            w_aud=W_["aud"], w_pk=W_["pk_max"], w_db=db(W_["top"] / cast_top), w_keep=keep_w)
        arms = arms_code(C_, B_, R_, W_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        chk = []
        xa1, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa1 - C_["x"]).max())))
        for n in NS:
            for sd in (None, NOISE_SEEDS[3]):
                xb1, _ = R([["arm", T0, "ult", {"w": ME + "-bite", "n": n}]], rows=sfx_rows, seed=sd)
                xb2, _ = bx(B_["sp"], B_["g"], B_["D"], n, seed=sd)
                chk.append((f"bite n{n}{'' if sd is None else ' draw'}", float(np.abs(xb1 - xb2).max())))
        xr1, _ = R([["arm", T0, "ult", {"w": ME + "-root"}]], rows=sfx_rows)
        chk.append(("root", float(np.abs(xr1 - R_["x"]).max())))
        xw1, _ = R([["arm", T0, "ult", {"w": ME + "-wither"}]], rows=sfx_rows)
        chk.append(("wither", float(np.abs(xw1 - W_["x"]).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11.6, 18, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("seal", {}), ("nova", {"k": 1}),
                   ("hex-snap", {}), ("fork", {}), ("vine", {}), ("vine", {"plant": True}), ("vine", {"coil": True}),
                   ("vine", {"miss": True}), ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}),
                   ("aegis", {"n": 3, "back": 5}), ("scour-hold", {"n": 5}), ("scour-tick", {}),
                   ("scour-woosh", {"n": 1}), ("scour-moo", {}),
                   ("ult", {"w": "ironwood-sprout"}), ("ult", {"w": "ironwood-wither"}),
                   ("ult", {"w": "morningstar-tick", "n": 2}), ("ult", {"w": "morningstar-close"}),
                   ("ult", {"w": "paradox-pin"}), ("ult", {"w": "nightfell-boom"})]
        others += [("ult", {"w": w_}) for w_ in ids if w_ != ME]
        e2e_voices = others
        same_ = []
        for kind, p in others:
            x1 = play(kind, p); x2, _ = R([["arm", T0, kind, p]], rows=sfx_rows, new=False)
            same_.append((kind + "/" + str(p.get("w", p.get("dmg", ""))) + ("!" if p.get("crit") else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, spark x3, wall, death, clank, seal, nova, hex-snap, fork, vine x4, loose x3, aegis, "
              f"scour x4, six ult sub-voices, the {len(ids) - 1} other casts): worst max |diff| {worst[1]:.0e} "
              f"({worst[0]})")
        now_rc = float(np.abs(xa1 - rcx).max())
        print(f"  ult/bindweed vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > 1e-6 or worst[1] > 1e-6 or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost)

        # ---- THE tickTendril ROWS ------------------------------------------
        tend_rows = [[BITE_ANCHOR, BITE_CODE], [WITHER_ANCHOR, WITHER_CODE], [ROOT_ANCHOR, ROOT_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickTendril ROWS, applied to the prototype's own source, run beside the original on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds, tend_rows])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Bindweed both sides x every foe x seeds {seeds}): {WR['same']}/"
              f"{WR['fights']} identical (over, clock, both hp, both positions, winner, the whole vineTally); every "
              f"other SFX call identical in order and opts in {WR['otherSame']}/{WR['fights']}")
        nh = WR["nh"]
        print(f"  windows {WR['ends']}: {WR['casts']} casts; {WR['bites']} bites -> {WR['biteV']} bite voices "
              f"({WR['fatalV']} on a killing bite), n = 1:{nh[1]} 2:{nh[2]} 3:{nh[3]} 4:{nh[4]}; {WR['roots']} roots -> "
              f"{WR['rootV']} root voices; {WR['withers']} withers ({WR['clockNoRoot']} on a clock close that rooted "
              f"nobody); problems {WR['nbad']}")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["withers"] != WR["ends"]["clock"] or WR["biteV"] != WR["bites"] \
                or WR["rootV"] != WR["roots"] or WR["biteV"] == 0 or WR["rootV"] == 0:
            FAILED.append("tickTendril rows")
        WB = page.evaluate(WIRE_JS, [seeds, [[BITE_ANCHOR, BITE_CODE_BAD], [WITHER_ANCHOR, WITHER_CODE],
                                             [ROOT_ANCHOR, ROOT_CODE]]])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a bite): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        pw_ = np.array(WR["perWin"]) if WR["perWin"] else np.zeros(1)
        print(f"  bites a window: median {np.median(pw_):.0f}, mean {pw_.mean():.1f}, p90 {np.percentile(pw_, 90):.0f}; "
              f"{100 * nh[4] / max(1, sum(nh)):.0f}% of snaps at the cap (the top note)")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "bites", "biteV", "roots",
                                          "rootV", "withers", "fatalV", "clockNoRoot", "nh", "nbad")}
        rec["wire"]["control_same"] = WB["same"]

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["bites"], w["foe"], w["seed"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], tend_rows])
            assert not errors, errors[:3]
            c0t = w_["cast"]; c1t = w_["close"]
            lo_t, hi_t = c0t - 1.0, c1t + 2.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            NEWV = (ME + "-bite", ME + "-root", ME + "-wither")
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if e[3] not in NEWV]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
            xo, _ = R(without, secs=secs, rows=sfx_rows, new=False)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd
            bite_ev = [(T0 + (e[0] - lo_t), e[2].get("n", 0)) for e in evs if e[3] == ME + "-bite"]
            b_over = [db(band_rms(xw, per[min(4, max(0, n))]["bf0"], t_, t_ + 0.06) /
                         max(band_rms(xo, per[min(4, max(0, n))]["bf0"], t_, t_ + 0.06), 1e-12)) for t_, n in bite_ev]
            wi_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME + "-wither"]
            ro_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME + "-root"]
            # the wither over everything else INCLUDING the root on its frame, and the root likewise
            xo_w = R([e_ for e_, e in zip(allv, evs) if e[3] != ME + "-wither"], secs=secs, rows=sfx_rows,
                     new=False)[0] + bd
            xo_r = R([e_ for e_, e in zip(allv, evs) if e[3] != ME + "-root"], secs=secs, rows=sfx_rows,
                     new=False)[0] + bd
            wi_over = [db(band_rms(xw, fw, t_, t_ + 0.4) / max(band_rms(xo_w, fw, t_, t_ + 0.4), 1e-12)) for t_ in wi_t]
            ro_over = [db(band_rms(xw, fr_, t_, t_ + 0.35) / max(band_rms(xo_r, fr_, t_, t_ + 0.35), 1e-12))
                       for t_ in ro_t]
            ca_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME]
            print(f"\nIN A REAL WINDOW -- bindweed v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0t:.2f}s, closed by its clock at {c1t:.2f}s and rooted, {w_['bites']} bites; the fight's own "
                  f"sounds and the score, with and without the new voices")
            print(f"  each bite over the fight in its own third-octave (its body's pitch): " +
                  " ".join(f"{v:+.1f}" for v in b_over) + " dB" +
                  (f" (median {np.median(b_over):+.1f})" if b_over else ""))
            print(f"  the wither over everything else on its frame, the root included: " +
                  " ".join(f"{v:+.1f}" for v in wi_over) + " dB;  the root over everything else, the wither "
                  "included: " + " ".join(f"{v:+.1f}" for v in ro_over) + " dB")
            if (b_over and float(np.median(b_over)) < 6) or (wi_over and min(wi_over) < 3) or \
                    (ro_over and min(ro_over) < 3) or not (b_over and wi_over and ro_over) or len(ca_t) != 1:
                FAILED.append("a new voice not heard in a real window")
            wav("bindweed-pick-real-window.wav", xw)
            wav("bindweed-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, bite_over=b_over, wither_over=wi_over, root_over=ro_over)
        else:
            print("\nIN A REAL WINDOW -- no rooted clock close in the wire runs")
            FAILED.append("no real window")
        # the four picks in order, for the ear: the cast, bites climbing the count, a blow, the close
        seq = [["arm", T0, "ult", {"w": ME}]]
        seq += [["arm", T0 + 0.8 + 0.34 * k, "ult", {"w": ME + "-bite", "n": n}] for k, n in enumerate((1, 2, 3, 4, 4))]
        seq += [["arm", T0 + 2.6, "hit", {"dmg": BLADE, "crit": False}]]
        seq += [["arm", T0 + 3.3, "ult", {"w": ME + "-wither"}], ["arm", T0 + 3.3, "ult", {"w": ME + "-root"}]]
        wav("bindweed-pick-sequence.wav", R(seq, secs=5.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Bindweed's cast, bite, root and wither arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickTendril: the bite voice, once per bite, after the bite's hurt and entangle",
                 anchor=BITE_ANCHOR, mode="replace", code=BITE_CODE),
            dict(label="tickTendril: the wither voice, on a clock close with both alive",
                 anchor=WITHER_ANCHOR, mode="replace", code=WITHER_CODE),
            dict(label="tickTendril: the root voice, on the frame the pin is written",
                 anchor=ROOT_ANCHOR, mode="replace", code=ROOT_CODE)]
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit("end to end: an anchor is not re-emitted exactly once")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="bindweed_e2e_"))
        try:
            tp = tmpd / "sc-tendril-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the four rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            with game(game_path=tp) as (page, errors):
                def R2(evs, seed=None):
                    r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                    assert not errors, errors[:3]
                    return pcm(r)
                vo = max(float(np.abs(R2([["play", T0, k, p]]) - x0).max())
                         for (k, p), x0 in zip(e2e_voices, e2e_ref["voices"]))
                NEWP = [("cast", {"w": ME}, cast_body(C_["sp"], C_["g"], C_["kc"]), {})]
                NEWP += [(f"bite n{n}", {"w": ME + "-bite", "n": n}, bite_body(B_["sp"], B_["g"], B_["D"]), {"n": n})
                         for n in NS]
                NEWP += [("root", {"w": ME + "-root"}, root_body(R_["sp"], R_["g"], R_["kc"], R_["kt"]), {}),
                         ("wither", {"w": ME + "-wither"}, wither_body(W_["sp"], W_["g"]), {})]
                nd = []
                for lab_, p, body, bp in NEWP:
                    x1 = R2([["play", T0, "ult", p]], seed=NOISE_SEEDS[5])
                    x2 = R2([["body", T0, body, bp]], seed=NOISE_SEEDS[5])
                    nd.append((lab_, float(np.abs(x1 - x2).max())))
                rcp = R2([["play", T0, "ult", {"w": "spellbreaker"}]])
                not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
                F1 = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
                assert not errors, errors[:3]
                if isinstance(F1, dict):
                    raise SystemExit(F1["err"])
                page_err = len(errors)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
        F0 = {f_["key"]: f_ for f_ in e2e_ref["fights"]}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        b_ok = sum(f_["biteV"] == f_["bites"] and f_["badN"] == 0 for f_ in F1)
        r_ok = sum(f_["rootV"] == f_["roots"] for f_ in F1)
        w_ok = sum(f_["witherV"] == f_["clock"] for f_ in F1)
        orig_new = sum(f_["biteV"] + f_["rootV"] + f_["witherV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "bites", "roots", "clock", "biteV", "rootV", "witherV")}
        print(f"  the four new voices through the patched page's own SFX.play vs the lab's candidate text in that "
              f"page, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/bindweed vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, bite voices = bites (n the foe's "
              f"stacks) {b_ok}, root voices = roots {r_ok}, withers = clock closes {w_ok} (of {len(F1)}); totals "
              f"{tot}; the original page played {orig_new} new voices; page errors {page_err}")
        if max(v for _, v in nd) > 1e-6 or vo > 1e-6 or not_rc <= 1e-3 or same != len(F1) or osame != len(F1) \
                or min(c_ok, b_ok, r_ok, w_ok) != len(F1) or orig_new or page_err:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same,
                          other_same=osame, totals=tot)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), bite=strip(rows_b), bite_controls=strip(ctlb),
               wither=strip(rows_w), wither_controls=strip([RI, CW, CQ]), root=strip(rows_r),
               root_controls=strip(ctlr), wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_kc": C_["kc"], "bite": B_["name"],
                     "bite_g": B_["g"], "bite_D": B_["D"], "root": R_["name"], "root_g": R_["g"],
                     "root_kc": R_["kc"], "root_kt": R_["kt"], "wither": W_["name"], "wither_g": W_["g"]})
    print(f"\nTHE PICKS  cast {C_['name']}   bite {B_['name']}   root {R_['name']}   wither {W_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    wr = rec["wire"]
    rows[0]["why"] = (
        f"The four voices (v68 §8.2), in the synth only. The arms are added BEFORE the shared rune-crack fallback, "
        f"and the fallback line is re-emitted unchanged, so the {len(rec['fallthrough']) - 1} other relics that "
        f"still fall through keep it. Through the patched play() every arm reproduces its lab candidate (worst "
        f"{max(v for _, v in rec['arm_check']['chk']):.0e}; the bite at every count 0-4, on two noise draws), "
        f"{len(rec['arm_check']['others'])} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), and ult/bindweed is no longer rune-crack. play() "
        f"returns on its first line with no audio context (every headless run), draws no random number and "
        f"writes nothing the simulation reads" + (f"; end to end the four voices through the patched page's own "
                                                   f"SFX.play equal the candidates (worst "
                                                   f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    rows[1]["why"] = (
        f"One plain SFX.play in tickTendril's bite block, after the bite's hurt and its entangle, so n is the "
        f"stacks the foe now carries (foe.stacks is a read). The bite's own cooldown, on the window tickers' clock, "
        f"makes the cadence -- no hit stop, no beat. {wr['biteV']}/{wr['bites']} bites voiced, each n equal to the "
        f"foe's stacks (1-4; {100 * wr['nh'][4] / max(1, sum(wr['nh'])):.0f}% at the cap); {wr['same']}/"
        f"{wr['fights']} fights identical and every other SFX call identical in order and opts; the same rows plus "
        f"one sim write (the foe nudged 1e-9 on a bite) come back {wr['control_same']}/{wr['fights']}{e2}.")
    rows[2]["why"] = (
        f"One guarded SFX.play on tickTendril's close branch, after the wither clock is set: a clock close with "
        f"both alive (the root's own condition without the stack count), so every rooting close and the few that "
        f"root nobody. {wr['withers']} withers for {wr['ends']['clock']} clock closes, none on the "
        f"{wr['ends']['caster']} closes the caster's death made or the {wr['ends']['over']} windows the fight's "
        f"end cut off; nothing is read back{e2}.")
    rows[3]["why"] = (
        f"One plain SFX.play inside the pin write's own block, after T.roots++: it can only sound where the sim "
        f"has just rooted the foe (clock close, both alive, entangle > 0). {wr['rootV']}/{wr['roots']} roots "
        f"voiced, one a window at most; nothing is read back{e2}.")
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
