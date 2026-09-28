#!/usr/bin/env python3
"""TEMPER'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v103.

    python coldiron_voice_lab.py --game <a link carrying Coldiron's stage 5> --rows rows.json

v73 §6.2 SOUND, every word of it: "Cast: a quench hiss into a low iron ring,
0.5s. A won bind: an anvil strike (a hard metallic hit with a 0.3s ring, peak
<= 0.6) over the engine's clank voice; pitch steps up with the sunder count.
Close: the ring dying, 0.4s." The brief's stage 6: "picture, voice, carry per
design §6". Rick, for the batch's art and sound: "you pick i overrule". So
this lab does not offer a spread -- it renders three to five candidates a
voice beside CONTROLS that can come back wrong, prints the numbers each pick is
made on, and PICKS by a rule written in this file (`*_RULE`, `*_why`). He
overrules from one clip.

NOTHING IS REUSED THAT DOES NOT EXIST. The one existing voice §6.2 names is
"the engine's clank voice", and it is untouched: `resolveClank` plays it on
every bind, a won one included, with `mass: max(mA, mB)` -- 5 in the window,
so it already hears the iron. The anvil is laid OVER it, on the same frame.
"The ring" of the close is the cast's own ring (the same modes on the same
note), not a voice of its own.

THE THREE EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/coldiron`, which `fireUlt` plays for every relic.
         Coldiron has NO arm today: it falls through to the shared rune-crack
         (so does Ironhail -- measured below, to 1e-6). The arms go BEFORE
         that fallback; the fallback line is re-emitted unchanged, so another
         relic's row anchored on it still applies, in either order.
  anvil  `ult/coldiron-anvil {n}` from `resolveClank`, right after
         `T.applied += u.bind;` -- inside the clause that runs when the bind
         is decisive and won by a fighter whose window is open, after the
         loser has taken its `bind` sunder. `n` is the LOSER'S sunder count
         after that apply: the count the stack tag shows, 2..9 at cap 9 (the
         foe's -- or a Twinshade shade's, when a shade loses the bind: shades
         bind too, and take the sunder themselves). With
         `bind` at 2 (the settled row) the clause's `if (u.bind > 0)` holds on
         every won bind, so every won bind strikes it (checked: anvil voices
         == won binds, each on its bind's step). A won bind at the cap (9 ->
         9) still strikes, at 9's note. No beat is filed: the clank files
         its own.
  close  `ult/coldiron-close` from `tickTemper` on the frame the window runs
         out BY ITS CLOCK with both fighters alive (the clause's own test,
         read at its own line) -- never on a death (a death close runs only
         in a kill flight), never once the fight is over (step() stops
         calling the tickers; a window still open at `over` plays nothing).
         The line goes after the window's `f.massMul = 1;`, which is
         re-emitted unchanged first.

THE CONTROLS, and what each one is for:
  rune-crack   what Coldiron's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@9.3      Coldiron's own blow (blade 9.3, stage 5): the level every voice
               is judged against, on its quietest / loudest noise draw
  crit@9.3     the same blow critting: the sound a ward shattering makes too
               (the shatter plays its own crit `hit` inside `hurt`)
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   the dwarven casts with a voice of their own -- Slagheart,
               Emberedge, Cindercleave, Grudgebearer (Ironhail IS rune-crack)
  the type     the twinblade casts -- Widowmaker, Twinshade, Thornshear,
               Starwarden (Spellbreaker IS rune-crack)
  clank@5      the engine's clank at the iron's mass: what the anvil lands on
  death        the heaviest low voice in the game: the ring must not be one
  hex-snap     the batch's other small bright voice
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  NOHISS, NORING, SAME, HIGH, HARM, RC-NOW   the cast without its hiss /
               without its ring / its ring struck on the cast's frame with
               the hiss (no "into") / its ring two octaves up / its ring on
               whole-number partials / what `ult/coldiron` plays today: each
               must fail its gate
  FLAT, TICK, HARM, LOUD, CLANK   the anvil at one pitch for every count /
               ringing 50 ms / on whole-number partials / 1.25x louder / the
               engine's own clank at mass 5 played as the anvil: each must
               fail its gate
  STRUCK, HELD, OTHER, SHORT   the close with a strike's click / held flat and
               cut at 0.4 s / on a note a fifth off the cast's ring / dying in
               0.15 s: each must fail its gate

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
  * The shared measures are zenith_voice_lab's and ironwood_voice_lab's,
    imported unchanged (E50 = 50 ms RMS at a 5 ms hop; TOP = the loudest 50
    ms; PEAK = the sample peak; AUDIBLE = first to last 5 ms RMS window above
    2% of the voice's own loudest; GONE = where it ends; RISE = 10 -> 90% of
    the 1 ms envelope; REG = cosine of 1/3-octave band amplitudes, 25 Hz-16
    kHz, the median over noise draws; IN-BAND = RMS inside the third-octave
    round a pitch; PITCH = FFT peak, Hann, zero-padded, parabolic; METAL =
    ironwood's inharmonic-mode test: the strongest peak between 1.5x and 4x
    the note is >= 60 cents from every whole multiple of it and within 20 dB).
  * THE HISS is the only part of a cast built from the noise buffer, so two
    renders on two noise draws differ by exactly it (and the compressor's
    reaction to it): the NOISE PART of a pair is (x1 - x2) / sqrt 2, the
    median over six disjoint pairs of the twelve draws (portcullis_voice_lab's
    STONE method). LEAD = its RMS over 0-100 ms re the whole voice's there
    (dB); BRIGHT = its power centroid over 0-150 ms (Hz: a hiss, not a thunk);
    SPAN = its own audible span (ms: a hiss is sustained, a tick is not);
    HISS-END = its RMS over the voice's last 100 audible ms re its own loudest
    50 ms (dB: it hands over, and what is left is the ring).
  * THE RING is the voice under 700 Hz (FFT low-pass). NOTE = the FFT peak
    60-700 Hz over 150-450 ms (after the hiss); ORDER = ms from the noise
    part's loudest 50 ms to the ring band's loudest 50 ms (the hiss INTO the
    ring: it comes first); RING-END = the note's third-octave over the last
    100 audible ms re its own loudest 50 ms (dB: the ring carries the voice to
    its end); TAIL-LOW = the share of the power under 700 Hz in the last 150
    audible ms.
  * THE ANVIL is measured at every count 1..9 (the arm's domain: `bind` 2 puts
    a won bind's count at 2..9). PITCH = the FFT peak 300 Hz-9 kHz over 5-60
    ms; RING = the note's third-octave over 200-250 ms re 0-50 ms (dB);
    OVER-CLANK = the anvil and the clank at mass 5 rendered on one frame
    against the clank alone, the note's third-octave over 0-80 ms (dB).
  * THE CLOSE: DYING = its loudest 50 ms is its first (centred <= 60 ms), it
    never rises >= 1 dB after it, and HOLD (the span of the 5 ms RMS within 6
    dB of its loudest, as a share of AUDIBLE) <= 0.40 -- a ring dying falls
    through -6 dB early and takes the rest of its length to fade; a held tone
    that is cut holds. UNSTRUCK = no strike under it: the share of its power
    above 2 kHz over 0-30 ms <= 0.05 (the whole voice high-passed by FFT, then
    windowed, so a window's own edges add nothing), and its noise part over
    0-30 ms <= -40 dB re the whole (a ring dying is the ring going on, not a
    new blow).
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's gain puts TOP at the centre of its window, its ring
    alone's loudest 50 ms equals its hiss alone's (RING_DB 0) and the ring's
    decay is solved so the voice is AUDIBLE 500 ms; the anvil's gain puts its
    sample peak at 0.54 (0.9 of §6.2's 0.6) at its loudest count on render.py's
    draw and its decay is solved to 300 ms audible at count 5; the close's
    gain puts its loudest 50 ms at the centre of its window and its decay is
    solved to 400 ms audible. Constants are rounded BEFORE any measured
    render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of §6.2 turned into numbers):
  * THE HISS enters on the cast's frame; THE RING enters 0.08 s after it
    (RING_AT), under the hiss, so the hiss leads INTO it.
  * "LOW": the ring's note below middle C (262 Hz).
  * THE RING'S NOTE in the score's key (A minor): A2 or A3 (the tonic), E2
    (the fifth). THE RING'S MODES: a bar (1 : 2.76 : 5.40), a plate (1 : 1.59
    : 2.14 : 2.65), or the free-free bar's first four modes voiced in its
    overtones (1 : 2.76 : 5.40 : 8.93 at 1 / 0.8 / 0.6 / 0.4, "iron").
  * THE ANVIL'S PITCH: one step of the score's scale a stack, A minor
    pentatonic (A C D E G) from A5 at count 1 to E7 at count 9 (SEMI steps a
    semitone instead; LOW starts an octave down). Counts are clamped to 1..9:
    the foe's ceiling is 9 while the iron holds, so no count past 9 exists.
  * THE ANVIL'S CONTACT: a 12 ms bandpass click at 5 kHz, at 0.8 of the
    note's gain, in every candidate (the hammer meeting the face).
  * "PEAK <= 0.6" is the anvil's own sample peak (the clause describes the
    anvil); the anvil and the clank on one frame are printed beside it, and
    must not clip (< 1.0).
  * Every tone of constant pitch has `.frequency.value = f` set (v97's
    toolkit finding: without it a strike's phase is not where it was
    scheduled); glides do not.

THE PICKS, on Chromium 151.0.7922.34, sc-coldiron-temper-b93 324b42d5b36fac98,
fight seeds 103601-103602 (152 fights):

  cast   7 STEAM   a narrow noise band (q 2.5) falling 7.5 -> 5 kHz over 0.32
                   s, and under it from 80 ms an iron bar on A2 voiced in its
                   overtones (sines on 1 : 2.76 : 5.40 : 8.93 at 1 / 0.8 / 0.6 /
                   0.4): audible 490 ms; the hiss leads the first 100 ms (-1.1
                   dB re the whole), centroid 7.7 kHz, spans 160 ms and is
                   silent by the end; the ring's loudest 50 ms 70 ms after the
                   hiss's; METAL (2.76x, 144 c off a harmonic), RING-END -21.8
                   dB, TAIL-LOW 1.00, in-band 0.029 (twice the score's p90 there
                   is 0.018); TOP -2.9 dB re the hit @ 9.3, +16.5 re the wall;
                   register at most 0.79 (Emberedge's cast). HUSH passes and
                   ties it on register (0.78) and calls: the order listed
                   breaks the tie. BAR, PLATE, SPIT and IRON lose on Emberedge
                   (0.84-0.88); TENOR and DEEP sit under the score.
  anvil  3 SEMI    a struck steel block (a triangle on the note, sines on its
                   2.76 and 5.40 modes) under a 12 ms 5 kHz click, a semitone a
                   stack, A5 (880 Hz) at count 1 to F6 (1397 Hz) at 9: rise 0
                   ms, peak at 9 ms, audible 295-300 ms, RING -20.5 dB at
                   200-250 ms, the sample peak <= 0.536 on every count and draw
                   (0.861 with the clank on its frame), +10.2 dB or more over
                   the clank in its own band; register at most 0.54 (the runic
                   snap). BAR passes and loses the tiebreak (0.73, rune-crack);
                   PLATE (+9.2 dB over the clank) and LOW (+6.2 dB, and its
                   peak at 11 ms) are out.
  close  3 BARE    the cast's ring on A2 without its top mode, not struck:
                   audible 395 ms, its loudest 50 ms its first and never rising
                   after, HOLD 0.20, nothing above 2 kHz at its start and no
                   noise part; -8.2 dB under the cast, +8.2 over the wall; heard
                   by its 2.76 mode (304 Hz), +3.1 dB over twice the score there
                   (its fundamental, 0.012, is not); register at most 0.76 (the
                   death voice), 0.75 against the cast (it IS the cast's ring:
                   printed, not gated). FADE and DROOP pass and tie it on
                   register (0.74); BARE has the fewest calls.

  In play (152 fights; the mirror match is refused by Match): 540 casts and
  540 cast voices; 1629 won binds and 1629 anvil voices, each on its bind's
  step, carrying the loser's count after the bind's sunder (2: 84, 3: 60, 4:
  86, 5: 75, 6: 82, 7: 75, 8: 86, 9: 1081 -- 1242 past 6; 933 on a loser
  already at its ceiling, the count unchanged; 15 against a Twinshade shade,
  with the shade's count); 436 windows closed by their clock and 436 closes,
  none for the 14 closed by a death or the 90 still open at the fight's end;
  152/152 fights identical and every other voice call identical in order, kind
  and opts; the sim-write control 24/152. In the clip (v Spellbreaker, 99015:
  the cast at 15.83 s, the clock close at 25.16 s, 6 won binds at counts 2 4 6
  8 9 9) every anvil stands +10.1..+28.5 dB over the fight (its clank
  included) in its own third-octave, the close +3.3 dB at 304 Hz, the cast's
  ring +13.6 dB at its loudest partial and its hiss +21.5 dB. Main-thread cost
  a call, at the headless timer's 0.1 ms resolution: 0.1-0.2 ms (the clank's
  own 0.2-0.3). Applied AS TEXT to a copy of the link (a scratch end-to-end, one
  browser at a time, seed 103701): the page loads clean, its own play renders
  the three voices to the lab's text (<= 1.2e-7, the anvil at every count) and
  36 others to the original page's (<= 1.5e-7), and 76/76 fights are
  identical, every other voice call identical, one anvil per won bind (845)
  and one close per clock close (222).

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table; that table (four casts, four anvils, three closes)
passed two anvils and failed every cast and every close, and each failure was
one fact about where A2 sits:
  * THE CAST: BAR, PLATE and SPIT read 0.87-0.88 against Emberedge's cast;
    TENOR (A3) passed every register but sat under the score's bass (in-band
    0.037 < 0.089). A2 (110 Hz) is the ONE low note clear of the score (its
    p90 there 0.0088; 0.041 at E2, 0.040 at G2, 0.046 at B2, 0.050 at D3 and
    E3, 0.044 at A3) -- and it lies in the third-octave where Emberedge's cast
    and the death voice both peak. Two candidates were added and fail: DEEP
    (the bar on E2: under the score, 0.035 < 0.082) and IRON (the bar on A2
    voiced in its overtones: 0.84 against Emberedge). Two more were added:
    STEAM and HUSH, IRON's bar under a NARROWER quench (q 2.5 / q 4) --
    Emberedge's cast is broadband above its low peak, and a wide hiss matched
    that floor. No rule was changed for the cast.
  * THE CLOSE: every close on BAR's ring read 0.89-0.90 against the death
    voice (a triangle's A2 is nearly all in the death voice's band), and every
    one sat under the score at its fundamental (0.0149 < 0.0176). The first
    follows the cast: on IRON's ring the closes read 0.74-0.76. The second is
    a RULE CHANGE, made once: the close's in-band was read at the ring's
    fundamental; it is now read at the LOUDEST of its partials (HEARD). The
    cast's words say "low", so its in-band stays at the fundamental (a ring
    heard only by its overtones is not low); the close's say "the ring", which
    the NOTE gate already ties to the cast's, and whether it is heard is
    whichever partial stands over the score -- on a phone speaker, which does
    not reproduce 110 Hz at all, the partials are all anyone hears. The
    fundamental's in-band is still printed beside it.
  * THE REAL WINDOW's cast gate first read the ring at its fundamental. In the
    clip the score under the cast is playing A2 -- the ring's own note, by
    design the tonic -- and two sines at one frequency add by their phase: the
    with/without ratio there read -0.7 dB, and could read anything from about
    -12 to +5 dB, which says nothing about hearing it. The gate now reads the
    ring's LOUDEST partial, as the close's HEARD does; every partial is
    printed (the fundamental's -0.7 dB among them). No other gate moved.
  * THE WIRE CHECK first matched each anvil to a sunder landing on the FOE, and
    15 of 1629 anvils had none: binds won against a Twinshade SHADE, which
    binds too and takes the sunder itself. The voice was right (it carries the
    loser's count); the instrument was wrong, and now matches the sunder on
    whichever fighter lost the bind.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (the three arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the anvil at
    counts -1, 0, 1..9, 12 and a missing `n`) must reproduce its candidate to
    TOL; every other voice through the patched play (the hit at five weights
    with and without a crit, spark x3, wall, death, clank x2, seal, nova,
    hex-snap, aegis x2, vine x4, loose x3, fork, scour x4, and every relic's
    cast and every sub-voice the ult arm names) must be unchanged;
    `ult/coldiron` must NOT be rune-crack any more;
  * the resolveClank and tickTemper rows are applied to their prototypes' own
    source and run on real fights beside the unpatched ones: every fight
    identical (over, clock, both hp, positions, velocities, stuns, both sunder
    counts, winner, the clank count and both temperTallies) and every other
    voice call identical in order, kind and opts; one anvil voice per won
    bind, on its step, carrying the count the loser's sunder apply (`bind`,
    from Coldiron's side letter) left on that step; one close per window closed
    by its clock with both alive and none otherwise; the unpatched runs play
    neither. The same rows plus ONE sim write (the loser nudged 1e-9 on a won
    bind) must come back NOT identical, or "identical" proves nothing. (The Sfx
    row cannot reach the simulation at all: `play` returns on its first line
    with no audio context, which is every headless run.)
  All anchors must occur exactly once in the game file, and every row is a
  `replace` that re-emits its anchor unchanged exactly once, so a later
  relic's row -- or the picture's -- anchored on the same line still applies,
  in either order.

Writes wavs to 05-reference/v103/coldiron-*.wav at RAW level (gitignored).
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
import sys
import textwrap

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
# The shared definitions, imported unchanged so every number here means what
# it means in v98's and v99's labs. (Their module bodies only check their own
# candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm, low_share, lowpass_fft  # noqa: E402

HERE = pathlib.Path(__file__).parent
RELIC = "coldiron"
BLADE = 9.3                               # Coldiron's dmg (stage 5)
CAP = 9                                   # w.ult.cap: the foe's ceiling while the iron holds
BIND = 2                                  # w.ult.bind
IRON = 5.0                                # w.ult.mass: the clank's mass in the window
PEAK_MAX = 0.6                            # §6.2: "peak <= 0.6"
ANVIL_PK = 0.54                           # the anvil's level match: 0.9 of PEAK_MAX
CAST_AUD, ANVIL_AUD, CLOSE_AUD = 500.0, 300.0, 400.0   # "0.5s", "a 0.3s ring", "0.4s"
RING_AT = 0.08                            # the ring enters 80 ms into the hiss
RING_DB = 0.0                             # the ring alone's loudest 50 ms re the hiss alone's
LOW_HZ = 262.0                            # "low": under middle C
RING_LP = 700.0                           # the ring band
A2, A3, A4, E2 = 110.0, 220.0, 440.0, 82.41
PENT_A5 = [880.0, 1046.5, 1174.66, 1318.51, 1567.98, 1760.0, 2093.0, 2349.32, 2637.02]
COUNTS = list(range(1, CAP + 1))
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)

# =============================================================== THE CAST ===
# "a quench hiss into a low iron ring, 0.5s". Every candidate's ring enters at
# RING_AT under its hiss; they differ in what the hiss and the ring ARE.
HISS = {
    "sweep": 'this._sweep(t, { f0: 6500, f1: 2800, q: 0.8, gain: g, dur: 0.32, atk: 0.012 });',
    "burst": 'this._burst(t, { freq: 4500, q: 0.7, gain: g, dur: 0.3, type:"highpass" });',
    # added after the first table (see WHAT THE FIRST CUT GOT WRONG)
    "steam": 'this._sweep(t, { f0: 7500, f1: 5000, q: 2.5, gain: g, dur: 0.32, atk: 0.012 });',
    "hush": 'this._sweep(t, { f0: 6000, f1: 5000, q: 4, gain: g, dur: 0.32, atk: 0.012 });',
}
# [ratio, level, decay share] per mode, and the oscillator
RING = {
    "bar": ([(1, 1, 1), (2.76, 0.45, 0.7), (5.4, 0.2, 0.45)], "triangle"),
    "plate": ([(1, 1, 1), (1.59, 0.7, 0.8), (2.14, 0.5, 0.65), (2.65, 0.35, 0.55)], "sine"),
    # the free-free bar's first four modes, voiced in its overtones (added after the first table)
    "iron": ([(1, 1, 1), (2.76, 0.8, 0.8), (5.4, 0.6, 0.6), (8.93, 0.4, 0.45)], "sine"),
    "harm": ([(1, 1, 1), (2, 0.45, 0.7), (3, 0.2, 0.45)], "triangle"),       # a control
}


def modes_js(modes):
    return "[" + ", ".join("[" + ", ".join(fmt(v) for v in m) + "]" for m in modes) + "]"
CAST_CANDIDATES = [
    ("1 BAR", dict(hiss="sweep", ring="bar", f=A2),
     "a quench: a noise band falling 6.5 -> 2.8 kHz over 0.32 s (12 ms attack), and an iron bar on A2 "
     "(triangles on 1 : 2.76 : 5.40) entering under it at 80 ms"),
    ("2 PLATE", dict(hiss="sweep", ring="plate", f=A2),
     "BAR's quench over an iron plate on A2 (sines on 1 : 1.59 : 2.14 : 2.65)"),
    ("3 SPIT", dict(hiss="burst", ring="bar", f=A2),
     "BAR with the hiss a fixed high-passed burst (4.5 kHz, 0.3 s, instant attack): the spit of the plunge"),
    ("4 TENOR", dict(hiss="sweep", ring="bar", f=A3),
     "BAR with the bar an octave up, on A3"),
    # added after the first table (see WHAT THE FIRST CUT GOT WRONG)
    ("5 DEEP", dict(hiss="sweep", ring="bar", f=E2),
     "BAR with the bar a fourth down, on E2 (82.4 Hz, the score's fifth)"),
    ("6 IRON", dict(hiss="sweep", ring="iron", f=A2),
     "BAR's quench over a bar on A2 voiced in its overtones: sines on 1 : 2.76 : 5.40 : 8.93 at 1 / 0.8 / 0.6 / 0.4"),
    ("7 STEAM", dict(hiss="steam", ring="iron", f=A2),
     "IRON's bar under a narrower quench: a band (q 2.5) falling 7.5 -> 5 kHz over 0.32 s"),
    ("8 HUSH", dict(hiss="hush", ring="iron", f=A2),
     "IRON's bar under the narrowest quench: a band (q 4) settling 6 -> 5 kHz over 0.32 s"),
]


def ring_lines(ring, F, at, gexpr, Dexpr, droop=False, held=None, drop_top=False):
    modes, typ = RING[ring]
    if drop_top:
        modes = modes[:-1]
    at_ = "t" if at == 0 else f"t + {fmt(at)}"
    L = [f"for (const [r, k, d] of {modes_js(modes)})"]
    if held is not None:
        L += ["{",
              f"  const o = this._tone({at_}, {{ freq: F * r, gain: {gexpr} * k, dur: 8, type:\"{typ}\" }});",
              f"  o.frequency.value = F * r; o.stop({at_} + {fmt(held)});",
              "}"]
    elif droop:
        L += [f"  this._tone({at_}, {{ freq: F * r, to: F * r * 0.9439, gain: {gexpr} * k, dur: {Dexpr} * d, "
              f"type:\"{typ}\" }});"]
    else:
        L += [f"  this._tone({at_}, {{ freq: F * r, gain: {gexpr} * k, dur: {Dexpr} * d, type:\"{typ}\" }})"
              f".frequency.value = F * r;"]
    return L


def cast_body(sp, g, kr, D, part="both", ind=10):
    """The cast arm's body. `part`: "both" (the arm), "hiss" (the hiss alone:
    the NORING control and the balance), "ring" (the ring alone: the NOHISS
    control and the balance). `sp["at"]` overrides RING_AT (the SAME control)."""
    at = sp.get("at", RING_AT)
    L = [f"const g = {fmt(g)}, kr = {fmt(kr)}, D = {fmt(D)}, F = {fmt(sp['f'])};"]
    if part in ("both", "hiss"):
        L += [HISS[sp["hiss"]]]
    if part in ("both", "ring"):
        L += ring_lines(sp["ring"], sp["f"], at, "g * kr", "D")
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE ANVIL ===
# "an anvil strike (a hard metallic hit with a 0.3s ring, peak <= 0.6) over
# the engine's clank voice; pitch steps up with the sunder count".
ANVIL_MODES = {
    "bar": '[[1, 1, 1, "triangle"], [2.76, 0.5, 0.6, "sine"], [5.4, 0.25, 0.35, "sine"]]',
    "plate": '[[1, 1, 1, "sine"], [1.59, 0.7, 0.8, "sine"], [2.14, 0.5, 0.65, "sine"], [2.65, 0.35, 0.5, "sine"]]',
    "harm": '[[1, 1, 1, "triangle"], [2, 0.5, 0.6, "sine"], [3, 0.25, 0.35, "sine"]]',          # a control
}
ANVIL_CANDIDATES = [
    ("1 BAR", dict(modes="bar", step="pent", base=1),
     "a struck steel block: a triangle on the note and sines on its free-bar modes 2.76 / 5.40, the A minor "
     "pentatonic from A5 (count 1) to E7 (count 9), a 5 kHz contact click"),
    ("2 PLATE", dict(modes="plate", step="pent", base=1),
     "BAR's scale and click on a steel plate (sines on 1 : 1.59 : 2.14 : 2.65)"),
    ("3 SEMI", dict(modes="bar", step="semi", base=1),
     "BAR stepping a semitone a stack from A5 (count 9 on F6)"),
    ("4 LOW", dict(modes="bar", step="pent", base=0.5),
     "BAR an octave down: A4 (count 1) to E6 (count 9)"),
]


def anvil_f(sp, n):
    n = min(CAP, max(1, int(round(n))))
    if sp["step"] == "flat":
        return PENT_A5[0] * sp["base"]
    if sp["step"] == "semi":
        return PENT_A5[0] * sp["base"] * 2 ** ((n - 1) / 12)
    return PENT_A5[n - 1] * sp["base"]


def anvil_body(sp, g, D, ind=10):
    if sp["step"] == "pent":
        tab = ", ".join(fmt(round(f * sp["base"], 3)) for f in PENT_A5)
        fl = f"const F = [{tab}][n - 1];"
    elif sp["step"] == "semi":
        fl = f"const F = {fmt(PENT_A5[0] * sp['base'])} * Math.pow(2, (n - 1) / 12);"
    else:
        fl = f"const F = {fmt(PENT_A5[0] * sp['base'])};"
    L = [f"const n = clamp(Math.round(p.n || 0), 1, {CAP}), g = {fmt(g)}, D = {fmt(D)};",
         fl,
         'this._burst(t, { freq: 5000, q: 1, gain: g * 0.8, dur: 0.012, type:"bandpass" });',
         f"for (const [r, k, d, y] of {ANVIL_MODES[sp['modes']]})",
         "  this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type: y }).frequency.value = F * r;"]
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE CLOSE ===
# "the ring dying, 0.4s": the cast's ring (its modes, its note), not struck.
CLOSE_CANDIDATES = [
    ("1 FADE", dict(kind="fade"), "the cast's ring, every mode, dying over 0.4 s"),
    ("2 DROOP", dict(kind="droop"), "FADE with every mode sinking a semitone over its decay (the iron cooling)"),
    ("3 BARE", dict(kind="bare"), "FADE without the ring's top mode (the first to die in a struck bar)"),
]
CLOSE_CONTROLS = [
    ("0 STRUCK", dict(kind="struck"), "FADE with the anvil's contact click at its start -- a new strike"),
    ("0 HELD", dict(kind="held"), "FADE's modes held flat and cut at 0.4 s"),
    ("0 OTHER", dict(kind="other"), "FADE a fifth up from the cast's ring"),
    ("0 SHORT", dict(kind="fade", aud=150.0), "FADE dying in 0.15 s"),
]


def close_body(sp, cast_sp, g, D, ind=10):
    ring = cast_sp["ring"]
    F = cast_sp["f"] * (1.5 if sp["kind"] == "other" else 1.0)
    L = [f"const g = {fmt(g)}, D = {fmt(D)}, F = {fmt(F)};"]
    if sp["kind"] == "struck":
        L += ['this._burst(t, { freq: 5000, q: 1, gain: g * 0.8, dur: 0.012, type:"bandpass" });']
    if sp["kind"] == "held":
        L += ring_lines(ring, F, 0, "g", "D", held=0.4)
    elif sp["kind"] == "droop":
        L += ring_lines(ring, F, 0, "g", "D", droop=True)
    elif sp["kind"] == "bare":
        L += ring_lines(ring, F, 0, "g", "D", drop_top=True)
    else:
        L += ring_lines(ring, F, 0, "g", "D")
    return "\n".join(" " * ind + l for l in L)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
ANVIL_ANCHOR = '        T.applied += u.bind;'
CLOSE_ANCHOR = '        f.massMul = 1;'

ANVIL_CODE = ANVIL_ANCHOR + '''
        /* COLDIRON'S ANVIL (v73 §6.2: "an anvil strike ... over the engine's
           clank voice; pitch steps up with the sunder count"): on the won
           bind's own frame, after the loser has taken its sunder, carrying
           the loser's count -- the one its tag shows, 2..9 (the foe's, or a
           Twinshade shade's when a shade loses the bind). With `bind` 2
           every won bind reaches this line, the cap included (9 -> 9 still
           strikes). The clank below plays its own voice as it always has.
           Presentation only: SFX.play draws nothing, is a no-op headless, and
           nothing here is read back (coldiron_voice_lab: fights identical). */
        SFX.play("ult", { w: "coldiron-anvil", n: temperL.stacks("sunder") });'''

CLOSE_CODE = CLOSE_ANCHOR + '''
        /* TEMPER'S CLOSE (v73 §6.2: "the ring dying, 0.4s"): only when the
           window runs out BY ITS CLOCK with both fighters alive -- this
           clause's own test. A death closes it only in a kill flight, and a
           fight that ends with the window open never gets here (step() stops
           calling this), so both are left to the death voice, as Zenith's,
           Canopy's and Onslaught's closes are. Plain SFX.play; nothing is
           read back. */
        if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "coldiron-close" });'''

# the sim-write control: the same anvil row with the loser nudged 1e-9
ANVIL_CODE_BAD = ANVIL_CODE.replace(
    '        SFX.play("ult", { w: "coldiron-anvil"',
    '        temperL.vx += 1e-9;\n        SFX.play("ult", { w: "coldiron-anvil"', 1)

_refuse(ANVIL_CODE + CLOSE_CODE, "sim rows")
for _c, _a in ((ANVIL_CODE, ANVIL_ANCHOR), (CLOSE_CODE, CLOSE_ANCHOR)):
    assert _c.count(_a) == 1 and _c.startswith(_a), "a sim row must re-emit its anchor first, exactly once"
assert ANVIL_CODE_BAD != ANVIL_CODE


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


def note_name(f):
    names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    k = round(12 * math.log2(f / 55.0))
    return f"{names[k % 12]}{(k + 9) // 12 + 1}"


NAMES = {"clank@5": "the clank", "hit@9.3": "the blow", "crit@9.3": "the crit", "death": "the death voice",
         "hex-snap": "the runic snap", "rune-crack": "rune-crack", "wall": "the wall tick", "cast": "the cast",
         "anvil": "the anvil"}


def who(regs):
    k = max(regs, key=regs.get)
    return NAMES.get(k, k[0].upper() + k[1:] + "'s cast")


def arms_code(C_, A_, K_, info):
    cname, aname, kname = (X["name"].split()[1] for X in (C_, A_, K_))
    hiss = {"sweep": "a noise band falling from 6.5 to 2.8 kHz over 0.32 s with a 12 ms attack",
            "burst": "a fixed high-passed noise burst at 4.5 kHz, 0.3 s",
            "steam": "a narrow noise band (q 2.5) falling from 7.5 to 5 kHz over 0.32 s with a 12 ms attack",
            "hush": "a narrow noise band (q 4) settling from 6 to 5 kHz over 0.32 s with a 12 ms attack"}[
        C_["sp"]["hiss"]]
    ring = {"bar": "an iron bar (triangles on the note and its free-bar modes 2.76 and 5.40)",
            "plate": "an iron plate (sines on the note and its plate modes 1.59, 2.14, 2.65)",
            "iron": "an iron bar voiced in its overtones (sines on the note and its free-bar modes 2.76, 5.40 and "
                    "8.93)"}[C_["sp"]["ring"]]
    rnote = note_name(C_["sp"]["f"])
    role = {"A": "the score's tonic", "E": "the score's fifth"}.get(rnote[0], "in the score's scale")
    kwhat = {"fade": ", every mode", "droop": ", every mode sinking a semitone as it dies",
             "bare": " without its top mode (the first to die in a struck bar)"}[K_["sp"]["kind"]]
    c_cast = _wrap([
        f'COLDIRON\'S CAST, THE QUENCH -- v73 §6.2: "a quench hiss into a low iron ring, 0.5s". {cname}, of '
        f'{info["n_cast"]}, picked on the numbers by `coldiron_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v103). Coldiron had no arm and fell through to rune-crack, which Ironhail and '
        f'Spellbreaker still use, so this ADDS arms before that fallback and leaves it alone.',
        f"The hiss is {hiss}; the ring is {ring} on {rnote} ({role}), entering under the hiss "
        f"80 ms in and ringing on alone. Audible {info['c_aud']:.0f} ms; the hiss leads the first 100 ms "
        f"({info['c_lead']:+.1f} dB re the whole) and is "
        + ("silent over the last 100" if info['c_hend'] < -120 else f"{info['c_hend']:+.1f} dB in the last 100")
        + f" audible ms, the ring's loudest 50 ms {info['c_order']:.0f} ms after the hiss's; the loudest 50 ms "
        f"{info['c_top']:+.1f} dB re Coldiron's own blow. Register at most {info['c_reg']:.2f} "
        f"({info['c_regw']}) against rune-crack, the dwarven and twinblade casts, the clank, the death voice "
        f"and the blow."], 10)
    step = {"pent": "one step of the score's A minor pentatonic a stack",
            "semi": "a semitone a stack"}[A_["sp"]["step"]]
    what = {"bar": "a struck steel block (a triangle on the note, sines on its free-bar modes 2.76 and 5.40)",
            "plate": "a struck steel plate (sines on 1 : 1.59 : 2.14 : 2.65)"}[A_["sp"]["modes"]]
    c_anvil = _wrap([
        f'THE ANVIL -- "an anvil strike (a hard metallic hit with a 0.3s ring, peak <= 0.6) over the '
        f'engine\'s clank voice; pitch steps up with the sunder count" (v73 §6.2). {aname}, of '
        f'{info["n_anvil"]} (`coldiron_voice_lab.py`). `resolveClank` plays it on a won bind with `n`, the '
        f"loser's sunder count after the bind's sunder, over the clank it lands on.",
        f"{what[0].upper() + what[1:]} under a 5 kHz contact click, {step}: {info['a_lo']} at count 1 to "
        f"{info['a_hi']} at 9 (counts clamped to 1..9, the ceiling while the iron holds). Audible "
        f"{info['a_aud']} ms; peak at most {info['a_pk']:.3f} on any count or noise draw; "
        f"{info['a_over']:+.1f} dB or more over the clank in its own band. Register at most "
        f"{info['a_reg']:.2f} ({info['a_regw']}) against the clank, the blow, its crit, the wall tick, the "
        f"runic snap, rune-crack and the cast."], 10)
    c_close = _wrap([
        f'THE RING DIES -- "the ring dying, 0.4s" (v73 §6.2). {kname}, of {info["n_close"]} '
        f"(`coldiron_voice_lab.py`): the cast's own ring on {rnote}{kwhat}, not struck again -- it starts "
        f"at its loudest, {info['k_db']:+.1f} dB under the cast, and fades over {info['k_aud']:.0f} ms, heard "
        f"over the score by its {info['k_hf']:.0f} Hz mode ({info['k_heard']:+.1f} dB over twice the score "
        f"there). Register at most {info['k_reg']:.2f} ({info['k_regw']}) against the clank, the blow, the "
        f"death voice, rune-crack and the anvil. `tickTemper` plays it only when the window closes by its "
        f"clock with both alive."], 10)
    return (f'        }} else if (w === "coldiron"){{                   // the blades are quenched\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["kr"], C_["D"])}\n'
            f'        }} else if (w === "coldiron-anvil"){{             // a bind won on the anvil\n'
            f'{c_anvil}\n{anvil_body(A_["sp"], A_["g"], A_["D"])}\n'
            f'        }} else if (w === "coldiron-close"){{             // and the iron cools\n'
            f'{c_close}\n{close_body(K_["sp"], C_["sp"], K_["g"], K_["D"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# The resolveClank and tickTemper rows, applied to the real prototypes and run
# beside the original; the survey of Temper's windows comes out of the same runs.
WIRE_JS = r"""([seeds, clankRow, temperRow, mirror]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const oC = P.resolveClank, oT = P.tickTemper;
  const patch = (fn, row, nm) => {
    const src = fn.toString(), at = src.split(row[0]).length - 1;
    if (at !== 1) return { err: `the ${nm} anchor occurs ${at} times in ${nm}()` };
    return (0, eval)("(function " + src.replace(row[0], () => row[1]) + ")");
  };
  const pC = patch(oC, clankRow, "resolveClank"), pT = patch(oT, temperRow, "tickTemper");
  if (pC.err) return pC; if (pT.err) return pT;
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const MINE = (k, p) => k === "ult" && p && typeof p.w === "string" && (p.w === "coldiron" || p.w.startsWith("coldiron-"));
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "coldiron");
  const run = (side, fid, sd, wire, mirrorRun) => {
    const m = side ? new AC.Match(fid, "coldiron", sd) : new AC.Match("coldiron", fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b, me = f === m.a ? "a" : "b";
    const FP = Object.getPrototypeOf(m.a), oA = FP.apply;
    const calls = [], other = [], applies = []; let step = 0, inC = 0, inT = 0, n = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      if (MINE(kind, p)) calls.push({ step, t: m.t, k: p.w, n: p.n === undefined ? null : p.n,
                                      inC: !!inC, inT: !!inT, fs: foe.stacks("sunder"), cap: foe.sunderCap });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    /* instrumentation only: every sunder a bind lands (on the foe, or on a Twinshade shade, which binds
       too), logged after it lands */
    FP.apply = function(k, nn, s){ const b0 = this.stacks("sunder"), r = oA.call(this, k, nn, s);
      if (k === "sunder" && this !== f && inC) applies.push([step, nn, s, this.stacks("sunder"), true, b0, this === foe]);
      return r; };
    const ends = [];
    P.resolveClank = function(A, B, hx, hy){ inC++; try { return (wire ? pC : oC).call(this, A, B, hx, hy); } finally { inC--; } };
    P.tickTemper = function(dt){
      const Z = f.ultTemper, fa = f.alive, oa = foe.alive;
      inT++; try { return (wire ? pT : oT).call(this, dt); }
      finally { inT--; if (Z && !f.ultTemper) ends.push([step, (Z.t >= Z.dur && fa && oa) ? "clock" : "death"]); } };
    const wins = [], wonSteps = {}; let prev = null, W = null, lastWon = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n;
        m.step(DT); n++;
        const Z = f.ultTemper, T = f.temperTally;
        const e = ends.length && ends[ends.length - 1][0] === step ? ends[ends.length - 1] : null;
        if (e && W && !W.end){ W.end = e[1]; W.endStep = step; W.close = m.t; }
        if (Z && Z !== prev){ if (W && !W.end){ W.end = "recast"; W.endStep = step; }
                              W = { cast: m.t, castStep: step, end: null, endStep: null, won: 0, ns: [] }; wins.push(W); }
        if (T && T.won > lastWon){ wonSteps[step] = T.won - lastWon; if (W) W.won += T.won - lastWon; lastWon = T.won; }
        prev = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.resolveClank = oC; P.tickTemper = oT; FP.apply = oA; if (had) S.play = op; else delete S.play; }
    const TT = (x) => x.temperTally ? JSON.stringify(x.temperTally) : null;
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, m.a.vx, m.a.vy, m.b.vx,
                                  m.b.vy, m.a.stun, m.b.stun, m.a.stacks("sunder"), m.b.stacks("sunder"),
                                  m.winner ? m.winner.w.id : null, m.clankCount, TT(m.a), TT(m.b)]),
             calls, other: JSON.stringify(other), wins, wonSteps, applies, me, openAtOver: !!f.ultTemper };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const endsN = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, castV = 0, won = 0, anvilV = 0, closes = 0, atCap = 0, mirrorV = 0, shadeV = 0;
  const ns = [], perWin = [], pick = [];
  const pairs = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds) pairs.push([side, fid, sd]);
  if (mirror) for (const sd of seeds) pairs.push([2, "coldiron", sd]);
  for (const [side, fid, sd] of pairs){
    let A, B;
    if (side === 2){ A = run(0, fid, sd, false, true); B = run(0, fid, sd, true, true); }
    else { A = run(side, fid, sd, false); B = run(side, fid, sd, true); }
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== "coldiron")) bad.push([fid, sd, "the UNPATCHED run played a Temper voice"]);
    for (const c of B.calls){
      if (c.k === "coldiron-anvil" && !c.inC) bad.push([fid, sd, "an anvil outside resolveClank"]);
      if (c.k === "coldiron-close" && !c.inT) bad.push([fid, sd, "a close outside tickTemper"]);
    }
    if (side === 2){ mirrorV += B.calls.filter(c => c.k === "coldiron-anvil").length; continue; }
    const cv = B.calls.filter(c => c.k === "coldiron");
    castV += cv.length;
    if (cv.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", cv.length, B.wins.length]);
    /* per step: one anvil per won bind, carrying the count the loser's sunder apply left */
    const byStep = {};
    for (const c of B.calls) if (c.k === "coldiron-anvil") (byStep[c.step] = byStep[c.step] || []).push(c);
    const keys = new Set([...Object.keys(B.wonSteps), ...Object.keys(byStep)]);
    for (const k of keys){
      const av = byStep[k] || [], nw = B.wonSteps[k] || 0;
      if (av.length !== nw) bad.push([fid, sd, "step " + k, "won", nw, "anvils", av.length]);
      const ap = B.applies.filter(a => String(a[0]) === k && a[1] === 2 && a[2] === B.me && a[4]);
      for (let i = 0; i < av.length; i++){
        const c = av[i], a = ap[i];
        if (!a) { bad.push([fid, sd, "an anvil with no bind sunder on its step"]); continue; }
        if (c.n !== a[3]) bad.push([fid, sd, "the anvil's count is not the loser's after its bind", c.n, a[3]]);
        if (!a[6]) shadeV++;
        if (typeof c.n !== "number" || c.n < 1 || c.n > 9) bad.push([fid, sd, "anvil count out of range", c.n]);
        ns.push(c.n);
        if (a[5] === a[3]) atCap++;         /* the loser already at its ceiling: 9 -> 9 */
      }
      anvilV += av.length; won += nw;
    }
    const cl = B.calls.filter(c => c.k === "coldiron-close");
    closes += cl.length;
    for (const W of B.wins){
      endsN[W.end]++; casts++; perWin.push(W.won);
      const c1 = cl.filter(c => c.step >= W.castStep && (W.endStep === null || c.step <= W.endStep));
      if (W.end === "clock"){
        if (c1.length !== 1 || c1[0].step !== W.endStep) bad.push([fid, sd, "clock close voices", c1.length]);
      } else if (c1.length) bad.push([fid, sd, W.end + " window played a close"]);
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, won: W.won });
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends: endsN, casts, castV, won, anvilV, closes, atCap,
           mirrorV, shadeV, ns, perWin, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Temper's.
RECORD_JS = r"""([side, fid, sd, clankRow, temperRow]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const oC = P.resolveClank, oT = P.tickTemper;
  const pC = (0, eval)("(function " + oC.toString().replace(clankRow[0], () => clankRow[1]) + ")");
  const pT = (0, eval)("(function " + oT.toString().replace(temperRow[0], () => temperRow[1]) + ")");
  const m = side ? new AC.Match(fid, "coldiron", sd) : new AC.Match("coldiron", fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && q.w.startsWith("coldiron")) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.resolveClank = pC; P.tickTemper = pT;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.resolveClank = oC; P.tickTemper = oT; if (had) S.play = op; else delete S.play; }
  return ev;
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
  for (const [k, kind, p] of [["cast", "ult", { w: "coldiron" }], ["anvil", "ult", { w: "coldiron-anvil", n: 5 }],
                              ["close", "ult", { w: "coldiron-close" }], ["clank", "clank", { mass: 5 }],
                              ["hit", "hit", { dmg: 9.3, crit: false }]]){
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


def _rms(v):
    return math.sqrt(float((v ** 2).mean())) if len(v) else 0.0


def span(y, frac=0.02):
    """First/last 5 ms RMS window above `frac` of the loudest, ms; (0, 0) if silent."""
    np = _np()
    e5, _ = env(y, 0.005, 0.005)
    if e5.max() <= 1e-12:
        return 0.0, 0.0
    on = np.nonzero(e5 > e5.max() * frac)[0]
    return float(on[0] * 5.0), float((on[-1] + 1) * 5.0)


def top_at(y):
    """Centre of the loudest 50 ms, ms after the event; None if silent."""
    np = _np()
    r50, c50 = env(y, 0.05)
    if r50.max() <= 1e-12:
        return None, 0.0
    i = int(np.argmax(r50))
    return float(c50[i] * 1000), float(r50[i])


def hiss(draws, aud_ms, a0_ms):
    """LEAD, BRIGHT, SPAN, HISS-END and the noise part's loudest-50-ms centre
    (see the docstring), medians over six disjoint pairs of the draws. A noise
    part whose loudest 50 ms is more than 100 dB under the voice's own is the
    render floor (renders of one text differ by ~1e-7), not a hiss: it reads as
    none, so no shape is measured on it (the NOHISS control)."""
    np = _np()
    ld, br, sp, he, ta = [], [], [], [], []
    i0 = int(T0 * SR)
    fr = np.fft.rfftfreq(1 << 14, 1 / SR)
    a1 = (a0_ms + aud_ms) / 1000
    for i in range(0, len(draws) - 1, 2):
        n = ((draws[i] - draws[i + 1]) / math.sqrt(2))[i0:]
        x = draws[i][i0:]
        if top_at(n)[1] < 1e-5 * top_at(x)[1]:
            n = np.zeros_like(n)
        rn = _rms(n[:int(0.1 * SR)])
        ld.append(db(rn / max(_rms(x[:int(0.1 * SR)]), 1e-12)) if rn > 0 else -180.0)
        seg = n[:int(0.15 * SR)]
        P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 14)) ** 2
        br.append(float((P * fr).sum() / P.sum()) if P.sum() > 1e-30 else 0.0)
        s0, s1 = span(n)
        sp.append(s1 - s0)
        t_, top_ = top_at(n)
        ta.append(t_ if t_ is not None else 0.0)
        end = n[int(max(0.0, a1 - 0.1) * SR):int(a1 * SR)]
        he.append(db(_rms(end) / top_) if top_ > 0 else -180.0)
    return (float(np.median(ld)), float(np.median(br)), float(np.median(sp)), float(np.median(he)),
            float(np.median(ta)))


def ring(x, aud_ms, a0_ms):
    """The ring: NOTE, METAL, RING-END, TAIL-LOW, the ring band's loudest-50-ms
    centre, and its IN-BAND (0.10-0.35 s)."""
    np = _np()
    y = x[int(T0 * SR):]
    note = pitch(x, T0 + 0.15, T0 + 0.45, lo=60, hi=RING_LP)
    r, c, d = inharm(x, T0 + 0.15, T0 + 0.45, note)
    a1 = (a0_ms + aud_ms) / 1000
    top_b = max(band_rms(x, note, T0 + k * 0.025, T0 + k * 0.025 + 0.05) for k in range(0, 18))
    end_db = db(band_rms(x, note, T0 + max(0.0, a1 - 0.1), T0 + a1) / max(top_b, 1e-12))
    lo = lowpass_fft(y, RING_LP)
    a = max(0.0, a1 - 0.15)
    s_all, s_lo = y[int(a * SR):int(a1 * SR)], lo[int(a * SR):int(a1 * SR)]
    tail = float((s_lo ** 2).sum() / max((s_all ** 2).sum(), 1e-30))
    rt, _ = top_at(lo)
    inb = band_rms(x, note, T0 + 0.10, T0 + 0.35)
    return note, r, c, d, end_db, tail, rt, inb


def dying(x):
    """DYING (see the docstring): the loudest 50 ms's centre (ms), the largest
    rise after it inside AUDIBLE (dB), HOLD."""
    np = _np()
    y = x[int(T0 * SR):]
    a0, a1 = span(y)
    e, c = env(y, 0.05)
    live = (c * 1000 >= a0) & (c * 1000 <= a1)
    e, c = e[live], c[live]
    im = int(np.argmax(e))
    after = 20 * np.log10(np.maximum(e[im:], 1e-9))
    rise = float(max(0.0, (after - np.minimum.accumulate(after)).max())) if len(after) else 0.0
    e5, _ = env(y, 0.005, 0.005)
    mx = e5.max()
    on = np.nonzero(e5 > mx * 0.02)[0]
    w6 = np.nonzero(e5 > mx * 10 ** (-6 / 20))[0]
    hold = (w6[-1] - w6[0] + 1) / (on[-1] - on[0] + 1)
    return float(c[im] * 1000), rise, float(hold)


def unstruck(x, draws):
    """UNSTRUCK: the share of the power above 2 kHz over 0-30 ms, and the noise
    part over 0-30 ms re the whole (dB, median over pairs)."""
    np = _np()
    i0, i1 = int(T0 * SR), int((T0 + 0.03) * SR)
    y = x[i0:]
    hp = y - lowpass_fft(y, 2000.0)            # the whole voice filtered, then the window taken: no leakage
    k = i1 - i0
    hf = float((hp[:k] ** 2).sum() / max((y[:k] ** 2).sum(), 1e-30))
    nz = []
    for i in range(0, len(draws) - 1, 2):
        n = (draws[i] - draws[i + 1])[i0:i1] / math.sqrt(2)
        rn = _rms(n)
        nz.append(db(rn / max(_rms(draws[i][i0:i1]), 1e-12)) if rn > 0 else -180.0)
    return hf, float(np.median(nz))


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v73 §6.2 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.5s': AUDIBLE 430-570 ms; 'a quench hiss': the noise part LEADS the "
    "first 100 ms (LEAD >= -6 dB re the whole), is BRIGHT (its centroid over "
    "0-150 ms >= 2500 Hz: a hiss, not a thunk) and sustained (SPAN >= 150 ms: "
    "a hiss, not a tick); 'into': the ring band's loudest 50 ms comes >= 40 ms "
    "after the noise part's (ORDER), and the hiss is gone by the end (HISS-END "
    "<= -20 dB); 'a low iron ring': the NOTE is the declared one (within 30 "
    "cents) and under 262 Hz, METAL (its strongest peak between 1.5x and 4x "
    ">= 60 cents from every whole multiple, within 20 dB), it carries to the "
    "end (RING-END >= -30 dB) and what is left is the ring (TAIL-LOW >= "
    "0.80); heard: the note's third-octave over 0.10-0.35 s >= 2x the score's "
    "p90 there. Register against rune-crack, the school's casts (Slagheart, "
    "Emberedge, Cindercleave, Grudgebearer), the type's (Widowmaker, "
    "Twinshade, Thornshear, Starwarden), the clank @ 5, the death voice and "
    "the hit @ 9.3 each <= 0.80 (not the fallback it replaces, not a row-mate, "
    "not a parry, not a death, not a blow). Level: TOP between 0.5x the hit @ "
    "9.3's loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST (heard "
    "like a blow, never over one). Tiebreak: the most distinct register (the "
    "lowest worst, to 0.05), then the fewest calls, then the order listed.")

ANVIL_RULE = (
    "At EVERY count 1-9: 'a hard ... hit': RISE <= 3 ms and the peak in the "
    "first 10 ms; 'metallic': METAL at the note; 'a 0.3s ring': AUDIBLE "
    "255-345 ms and RING (the note's third-octave over 200-250 ms re 0-50 ms) "
    ">= -30 dB; 'peak <= 0.6': the sample peak <= 0.60 on every noise draw, "
    "and with the clank @ 5 on the same frame < 1.0 (it does not clip); 'over "
    "the engine's clank voice': OVER-CLANK >= +10 dB; 'pitch steps up with "
    "the sunder count': the note is the declared one (within 30 cents) and "
    "every step n -> n + 1 rises >= 80 cents (a step, not a glide); heard: at "
    "count 1 the note's third-octave over 0-80 ms >= 2x the score's p90 there. "
    "Register (the worst count) against the clank @ 5, the hit @ 9.3, the crit "
    "@ 9.3 (the shatter's voice), the wall, hex-snap, rune-crack and the picked "
    "cast each <= 0.80. Tiebreak: the lowest worst register (to 0.05), then "
    "the fewest calls, then the order listed.")

CLOSE_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'the ring': the NOTE (60-700 Hz, first 150 "
    "ms) within 30 cents of the picked cast's ring note, and METAL; 'dying': "
    "DYING (its loudest 50 ms centred <= 60 ms, no rise >= 1 dB after it, "
    "HOLD <= 0.40) and UNSTRUCK (the share above 2 kHz over 0-30 ms <= 0.05 "
    "and the noise part there <= -40 dB); level: its loudest 50 ms <= 0.5x "
    "the picked cast's and >= 2x the wall tick's (loudest draw); heard: the "
    "loudest of its partials (the ring's modes on its note) over 0-0.25 s >= "
    "2x the score's p90 in that partial's third-octave. Register "
    "against the clank @ 5, the hit @ 9.3, the death voice, rune-crack and "
    "the picked anvil (count 5) each <= 0.80 (the cast's is printed, not "
    "gated: it IS the cast's ring). Tiebreak: the lowest worst register (to "
    "0.05), then the fewest calls, then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 430 <= M["aud"] <= 570: why.append(f"audible {M['aud']:.0f} ms, not 430-570")
    if M["lead"] < -6: why.append(f"the hiss does not lead ({M['lead']:+.1f} dB)")
    if M["bright"] < 2500: why.append(f"the hiss is not bright (centroid {M['bright']:.0f} Hz)")
    if M["hspan"] < 150: why.append(f"the hiss spans {M['hspan']:.0f} ms (< 150)")
    if M["order"] < 40: why.append(f"the ring's loudest 50 ms {M['order']:.0f} ms after the hiss's (< 40: not 'into')")
    if M["hend"] > -20: why.append(f"the hiss is not gone by the end ({M['hend']:+.1f} dB)")
    if abs(cents(M["note"], M["want"])) > 30: why.append(f"the note {M['note']:.1f} Hz, not {M['want']:.1f}")
    if M["note"] >= LOW_HZ: why.append(f"the ring at {M['note']:.0f} Hz is not low")
    if M["inh_c"] < 60 or M["inh_db"] < -20:
        why.append(f"not metal: its partial at {M['inh_r']:.2f}x is {M['inh_c']:.0f} c from a whole "
                   f"multiple, {M['inh_db']:+.0f} dB")
    if M["rend"] < -30: why.append(f"the ring does not carry to the end ({M['rend']:+.1f} dB)")
    if M["tail"] < 0.80: why.append(f"tail-low {M['tail']:.2f} < 0.80")
    if M["inb"] < lev["inb"]: why.append(f"in-band {M['inb']:.4f} < {lev['inb']:.4f} (under the score)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def anvil_why(M, lev):
    why = []
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 10: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["inh_c"] < 60 or M["inh_db"] < -20:
        why.append(f"not metal (worst count: {M['inh_c']:.0f} c, {M['inh_db']:+.0f} dB)")
    if M["aud_lo"] < 255 or M["aud_hi"] > 345: why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 255-345")
    if M["ring"] < -30: why.append(f"the note does not ring ({M['ring']:+.1f} dB by 200 ms)")
    if M["pk_all"] > PEAK_MAX: why.append(f"peak {M['pk_all']:.3f} > {PEAK_MAX}")
    if M["pk_both"] >= 1.0: why.append(f"with the clank it clips ({M['pk_both']:.3f})")
    if M["over"] < 10: why.append(f"over the clank {M['over']:+.1f} dB < +10")
    if M["note_err"] > 30: why.append(f"a note {M['note_err']:.0f} cents off its declared pitch")
    if M["step_min"] < 80: why.append(f"a step of {M['step_min']:+.0f} cents (< 80: not stepping up)")
    if M["inb"] < lev["inb"]: why.append(f"in-band {M['inb']:.4f} < {lev['inb']:.4f} (under the score)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if abs(M["off"]) > 30: why.append(f"the note {M['note']:.1f} Hz is {M['off']:+.0f} c off the cast's ring")
    if M["inh_c"] < 60 or M["inh_db"] < -20:
        why.append(f"not metal: its partial at {M['inh_r']:.2f}x is {M['inh_c']:.0f} c from a whole "
                   f"multiple, {M['inh_db']:+.0f} dB")
    if M["tat"] > 60: why.append(f"its loudest 50 ms at {M['tat']:.0f} ms (not dying from the start)")
    if M["rise_after"] >= 1: why.append(f"rises {M['rise_after']:.1f} dB after its loudest")
    if M["hold"] > 0.40: why.append(f"hold {M['hold']:.2f} > 0.40 (held, not dying)")
    if M["hf"] > 0.05: why.append(f"struck: {100 * M['hf']:.0f}% of 0-30 ms above 2 kHz")
    if M["nz"] > -40: why.append(f"struck: a noise part of {M['nz']:+.1f} dB at its start")
    if M["top"] > lev["hi"]: why.append(f"loudest 50 ms {M['top']:.4f} > {lev['hi']:.4f}")
    if M["top"] < lev["lo"]: why.append(f"loudest 50 ms {M['top']:.4f} < {lev['lo']:.4f}")
    if M["heard"] < 1: why.append(f"no partial over the score (the best, {M['heard_f']:.0f} Hz, "
                                  f"{db(M['heard']):+.1f} dB re 2x the score's p90 there)")
    for k, v in M["regs"].items():
        if k != "cast" and v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True,
                    help="a link carrying Coldiron's stage 5 and none of its voices (v103 ran on the scratch link "
                         "sc-coldiron-temper-b93.html, 324b42d5b36fac98)")
    ap.add_argument("--out", default="../05-reference/v103")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=103601)
    ap.add_argument("--clip", default="spellbreaker:99015:0",
                    help="the real window: foe:seed:side (stage 6's clip, runs/bind_pick.txt)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "anvil": ANVIL_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("resolveClank", ANVIL_ANCHOR), ("tickTemper", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if '"coldiron-anvil"' in html or '"coldiron-close"' in html or 'w === "coldiron"' in html:
        raise SystemExit(f"{gp.name} already carries Temper's voices -- run on stage 5")
    if 'kind: "temper"' not in html and 'kind:"temper"' not in html:
        raise SystemExit(f"{gp.name} does not carry Coldiron's Temper")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nTEMPER -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        row = page.evaluate("() => { const w = AC.WEAPONS.find(w => w.id === 'coldiron'); "
                            "return w ? [w.dmg, w.mass, w.ult.cap, w.ult.bind, w.ult.mass, w.ult.dur, w.aff, w.shape] : null; }")
        print(f"  the row: dmg {row[0]}, mass {row[1]}, cap {row[2]}, bind {row[3]}, iron {row[4]}, window {row[5]} s, "
              f"{row[6]} {row[7]}")
        if row[0] != BLADE or row[2] != CAP or row[3] != BIND or row[4] != IRON:
            raise SystemExit("the row is not the one this lab was written for (blade 9.3, cap 9, bind 2, mass 5)")
        kinds = page.evaluate("() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();"
                              " return [...new Set([...s.matchAll(/kind === \"([a-z-]+)\"/g)].map(m => m[1]))]; }")
        print(f"  THE SYNTH'S KINDS TODAY ({len(kinds)}): {', '.join(kinds)}")
        if "clank" not in kinds:
            raise SystemExit("the engine's clank voice is gone -- §6.2 lays the anvil over it")
        rec["kinds"] = kinds

        def R(evs, secs=3.0, seed=None, rows=None):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            new = any(e[0] == "body" or (e[0] == "arm" and e[2] == "ult" and
                                         str(e[3].get("w", "")).startswith(RELIC)) for e in evs)
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

        sizes = {}

        def wav(name, x):
            sizes[name] = write_wav(out / name, x)

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms and hit@11.6 0.443 / 80 ms. They must come back.")
        SCHOOL = ("slagheart", "emberedge", "cindercleave", "grudgebearer")
        TYPE = ("widowmaker", "twinshade", "thornshear", "starwarden")
        FALL = ("coldiron", "ironhail", "spellbreaker")
        ctl = {}
        REFS = [("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                ("hit@9.3", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("crit@9.3", ["play", T0, "hit", {"dmg": BLADE, "crit": True}]),
                ("wall", ["play", T0, "wall", {}]),
                ("death", ["play", T0, "death", {}]),
                ("clank@5", ["play", T0, "clank", {"mass": IRON}]),
                ("clank@1.1", ["play", T0, "clank", {"mass": 1.1}]),
                ("hex-snap", ["play", T0, "hex-snap", {}])]
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
                 ("hit@11.6 peak", ctl["hit@11.6"]["peak"], 0.443, 0.01),
                 ("hit@11.6 audible", ctl["hit@11.6"]["aud"], 80, 10)]
        bad = [f"{n}: {v:.3f} vs {p_}" for n, v, p_, t_ in repro if abs(v - p_) > t_]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
                                    f"PASS  all {len(repro)} published numbers come back"))
        if bad:
            raise SystemExit("the controls do not reproduce -- nothing new is quoted")
        rcx = ctl["rune-crack"]["x"]
        fall = {k: float(np.abs(ctl[f"{k} now"]["x"] - rcx).max()) for k in FALL}
        print("  ARE rune-crack today (max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if max(fall.values()) > 1e-6:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        # the noise draws
        D = {k: [] for k in ("hit@9.3", "crit@9.3", "wall", "rune-crack", "death", "clank@5", "hex-snap")
             + SCHOOL + TYPE}
        for sd in NOISE_SEEDS:
            for k in D:
                ev = dict(REFS)[k]
                D[k].append(basic(R([ev], seed=sd)[0]))
        h_lo, h_hi = min(m["top"] for m in D["hit@9.3"]), max(m["top"] for m in D["hit@9.3"])
        w_hi = max(m["top"] for m in D["wall"])
        print(f"  the hit @ 9.3 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m['peak'] for m in D['hit@9.3']):.3f}-{max(m['peak'] for m in D['hit@9.3']):.3f};  the wall "
              f"tick: {min(m['top'] for m in D['wall']):.4f}-{w_hi:.4f};  the clank @ 5: peak "
              f"{min(m['peak'] for m in D['clank@5']):.3f}-{max(m['peak'] for m in D['clank@5']):.3f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]

        def bedp90(f, dur=0.25):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + dur)
                                        for i in range(0, len(bseg) - int(dur * SR), 2400)], 90))

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        rec["levels"] = dict(hit93=[h_lo, h_hi], wall_hi=w_hi)
        wav("coldiron-ctl-runecrack.wav", rcx)
        wav("coldiron-ctl-hit93.wav", ctl["hit@9.3"]["x"])
        wav("coldiron-ctl-clank5.wav", ctl["clank@5"]["x"])
        wav("coldiron-ctl-death.wav", ctl["death"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_top = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a quench hiss into a low iron ring, 0.5s'. Level-matched: TOP {tgt_top:.4f} (the centre "
              f"of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the ring alone {RING_DB:+g} dB re the hiss alone, "
              f"AUDIBLE {CAST_AUD:g} ms")

        def cx(sp, g, kr, D_, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kr, D_, part), {}]], seed=seed)

        def calib_cast(sp):
            g, kr, D_ = 0.1, 1.0, 1.0
            for _ in range(4):
                lo_, hi_ = math.log(0.2), math.log(4.0)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, kr, math.exp(mid))[0])["aud"] < CAST_AUD: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                ht = basic(cx(sp, g, kr, D_, "hiss")[0])["top"]
                rt = basic(cx(sp, g, kr, D_, "ring")[0])["top"]
                kr = kr * (ht * 10 ** (RING_DB / 20)) / rt
                g = g * tgt_top / basic(cx(sp, g, kr, D_)[0])["top"]
            return float(f"{g:.4g}"), float(f"{kr:.4g}"), D_

        CAST_REGS = ("rune-crack",) + SCHOOL + TYPE + ("clank@5", "death", "hit@9.3")

        def cast_measure(sp, g, kr, D_, part="both", name=""):
            x, calls = cx(sp, g, kr, D_, part)
            x2, _ = cx(sp, g, kr, D_, part)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, kr=kr, D=D_, name=name, sp=sp, want=sp["f"])
            draws = [cx(sp, g, kr, D_, part, seed=sd)[0] for sd in NOISE_SEEDS]
            return cast_metrics(M, x, draws)

        def cast_metrics(M, x, draws):
            M["lead"], M["bright"], M["hspan"], M["hend"], hta = hiss(draws, M["aud"], M["a0"])
            (M["note"], M["inh_r"], M["inh_c"], M["inh_db"], M["rend"], M["tail"], rta,
             M["inb"]) = ring(x, M["aud"], M["a0"])
            M["order"] = (rta - hta) if rta is not None else -999.0
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in CAST_REGS}
            M["why"] = cast_why(M, dict(lev_c, inb=2 * bedp90(M["note"])))
            return M

        H_ = (f"  {'cand':<9}{'g':>7}{'kr':>7}{'D':>6}{'calls':>6}{'top':>8}{'aud':>5}{'lead':>6}{'brt':>6}{'span':>5}"
              f"{'hend':>6}{'ordr':>5}{'note':>7}{'inh x/c/dB':>15}{'rend':>6}{'tail':>6}{'inb':>8}"
              + "".join(f"{k[:4]:>5}" for k in ("rc",) + SCHOOL + TYPE + ("clnk", "dth", "hit")))
        print(H_)

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>7.4g}{M['kr']:>7.4g}{M['D']:>6.3g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['aud']:>5.0f}{M['lead']:>6.1f}{M['bright']:>6.0f}{M['hspan']:>5.0f}{M['hend']:>6.1f}"
                  f"{M['order']:>5.0f}{M['note']:>7.1f}{M['inh_r']:>6.2f}/{M['inh_c']:>3.0f}/{M['inh_db']:<+4.0f}"
                  f"{M['rend']:>6.1f}{M['tail']:>6.2f}{M['inb']:>8.4f}"
                  + "".join(f"{r_[k]:>5.2f}" for k in CAST_REGS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, kr, D_ = calib_cast(sp)
            M = cast_measure(sp, g, kr, D_, name=name)
            M["ring_db"] = db(basic(cx(sp, g, kr, D_, "ring")[0])["top"] / basic(cx(sp, g, kr, D_, "hiss")[0])["top"])
            rows_c.append(M); cast_line(M)
            wav(f"coldiron-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        s0 = rows_c[0]
        for part, sp, name in (("ring", s0["sp"], "0 NOHISS"), ("hiss", s0["sp"], "0 NORING"),
                               ("both", dict(s0["sp"], at=0.0), "0 SAME"),
                               ("both", dict(s0["sp"], f=A4), "0 HIGH"),
                               ("both", dict(s0["sp"], ring="harm"), "0 HARM")):
            M = cast_measure(sp, s0["g"], s0["kr"], s0["D"], part, name=name)
            ctlc.append(M); cast_line(M)
            wav(f"coldiron-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        rcm = dict(basic(rcx), x=rcx, calls=5, g=0, kr=0, D=0, name="0 RC-NOW", sp=None, want=s0["sp"]["f"])
        rcd = [R([["play", T0, "ult", {"w": RELIC}]], seed=sd)[0] for sd in NOISE_SEEDS]
        cast_metrics(rcm, rcx, rcd)
        ctlc.append(rcm); cast_line(rcm)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 NOHISS  BAR's ring alone -- a control\n"
              "    0 NORING  BAR's hiss alone -- a control\n"
              "    0 SAME    BAR with the ring struck on the cast's frame, with the hiss -- a control\n"
              "    0 HIGH    BAR with the ring two octaves up (A4) -- a control\n"
              "    0 HARM    BAR with the ring on whole-number partials (1 : 2 : 3) -- a control\n"
              "    0 RC-NOW  what ult/coldiron plays today (rune-crack) -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctlc:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, kr {C_['kr']}, D {C_['D']}; {C_['calls']} synth calls; TOP "
              f"{C_['top']:.4f} = {db(C_['top'] / h_lo):+.1f} dB re the hit @ 9.3 (quietest draw), "
              f"{db(C_['top'] / w_hi):+.1f} dB re the wall; the ring {C_['ring_db']:+.1f} dB re the hiss (each alone)")

        # ---- THE ANVIL -----------------------------------------------------
        print(f"\nANVIL -- 'an anvil strike (a hard metallic hit with a 0.3s ring, peak <= 0.6) over the engine's "
              f"clank voice; pitch steps up with the sunder count'. Level-matched: the sample peak {ANVIL_PK} at its "
              f"loudest count (render.py's draw), AUDIBLE {ANVIL_AUD:g} ms at count 5")
        clank5 = ctl["clank@5"]["x"]

        def ax(sp, g, D_, n, seed=None):
            return R([["body", T0, anvil_body(sp, g, D_), {"n": n}]], seed=seed)

        def calib_anvil(sp):
            g, D_ = 0.2, 0.7
            for _ in range(4):
                lo_, hi_ = math.log(0.05), math.log(3.0)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(ax(sp, g, math.exp(mid), 5)[0])["aud"] < ANVIL_AUD: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                pk = max(float(np.abs(ax(sp, g, D_, n)[0]).max()) for n in COUNTS)
                g = g * ANVIL_PK / pk
            return float(f"{g:.4g}"), D_

        anvil_inb_floor = {}
        AN_REGS = ("clank@5", "hit@9.3", "crit@9.3", "wall", "hex-snap", "rune-crack")

        def anvil_measure(fn, calls, g, D_, name, sp, want):
            M = dict(name=name, sp=sp, g=g, D=D_, calls=calls)
            notes, rises, pkms, auds, pks, rings, overs, inhc, inhd, both = [], [], [], [], [], [], [], [], [], []
            regs = {k: 0.0 for k in AN_REGS + ("cast",)}
            xs = {}
            for n in COUNTS:
                x = fn(n, None)
                if float(np.abs(x - fn(n, None)).max()) > TOL:
                    raise SystemExit(f"anvil {name} does not reproduce")
                xs[n] = x
                b_ = basic(x)
                rises.append(b_["rise"]); pkms.append(b_["pk_ms"]); auds.append(b_["aud"])
                draws = [fn(n, sd) for sd in NOISE_SEEDS]
                pks.append(max(float(np.abs(d_[int(T0 * SR):]).max()) for d_ in draws))
                f_ = pitch(x, T0 + 0.005, T0 + 0.06, lo=300, hi=9000)
                notes.append(f_)
                r_, c_, d_ = inharm(x, T0 + 0.005, T0 + 0.06, f_)
                inhc.append(c_); inhd.append(d_)
                rings.append(db(band_rms(x, f_, T0 + 0.20, T0 + 0.25) / max(band_rms(x, f_, T0, T0 + 0.05), 1e-12)))
                xb = fn.both(n)            # the anvil and the clank on one frame, through one chain
                both.append(float(np.abs(xb[int(T0 * SR):]).max()))
                overs.append(db(band_rms(xb, f_, T0, T0 + 0.08) / max(band_rms(clank5, f_, T0, T0 + 0.08), 1e-12)))
                DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
                for k in AN_REGS:
                    regs[k] = max(regs[k], reg(DB, k))
                regs["cast"] = max(regs["cast"], float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)])))
                if n == 5:
                    M["DB"] = DB
                if n == 1:
                    M["inb"] = band_rms(x, f_, T0, T0 + 0.08)
                    M["inb_floor"] = 2 * bedp90(f_, 0.08)
            M["xs"] = xs; M["x"] = xs[5]
            M["notes"] = notes
            M["note_err"] = max(abs(cents(f_, want(n))) for f_, n in zip(notes, COUNTS))
            st = [cents(notes[i + 1], notes[i]) for i in range(len(notes) - 1)]
            M["steps"] = st; M["step_min"] = min(st)
            M["rise"] = max(rises); M["pk_ms"] = max(pkms); M["aud_lo"] = min(auds); M["aud_hi"] = max(auds)
            M["pk_all"] = max(pks); M["pk_by_n"] = pks; M["pk_both"] = max(both)
            M["ring"] = min(rings); M["over"] = min(overs); M["over_by_n"] = overs
            M["inh_c"] = min(inhc); M["inh_db"] = min(inhd)
            M["regs"] = regs
            M["top"] = basic(xs[5])["top"]
            M["why"] = anvil_why(M, dict(inb=M["inb_floor"]))
            r_ = M["regs"]
            print(f"  {name:<9}{g:>7.4g}{D_:>6.3g}{M['calls']:>6d}{M['rise']:>5.0f}{M['pk_ms']:>5.0f}"
                  f"{M['aud_lo']:>6.0f}-{M['aud_hi']:<4.0f}{M['ring']:>6.1f}{M['pk_all']:>7.3f}{M['pk_both']:>7.3f}"
                  f"{M['over']:>6.1f}{M['note_err']:>5.0f}{M['step_min']:>6.0f}{M['inh_c']:>5.0f}{M['inh_db']:>5.0f}"
                  f"{M['inb']:>8.4f}" + "".join(f"{r_[k]:>5.2f}" for k in AN_REGS + ("cast",)))
            return M

        class Body:
            def __init__(self, sp, g, D_):
                self.sp, self.g, self.D = sp, g, D_

            def __call__(self, n, seed):
                return ax(self.sp, self.g, self.D, n, seed=seed)[0]

            def both(self, n):
                return R([["body", T0, anvil_body(self.sp, self.g, self.D), {"n": n}],
                          ["play", T0, "clank", {"mass": IRON}]])[0]

        class Clank:
            def __call__(self, n, seed):
                return R([["play", T0, "clank", {"mass": IRON}]], seed=seed)[0]

            def both(self, n):
                return R([["play", T0, "clank", {"mass": IRON}], ["play", T0, "clank", {"mass": IRON}]])[0]

        print(f"  {'cand':<9}{'g':>7}{'D':>6}{'calls':>6}{'rise':>5}{'pk@':>5}{'aud':>11}{'ring':>6}{'peak':>7}"
              f"{'+clnk':>7}{'over':>6}{'err':>5}{'step':>6}{'inhc':>5}{'inhd':>5}{'inb':>8}"
              + "".join(f"{k[:5]:>5}" for k in AN_REGS + ("cast",)))
        rows_a = []
        for name, sp, blurb in ANVIL_CANDIDATES:
            g, D_ = calib_anvil(sp)
            calls = ax(sp, g, D_, 5)[1][0]
            M = anvil_measure(Body(sp, g, D_), calls, g, D_, name, sp, lambda n, sp=sp: anvil_f(sp, n))
            rows_a.append(M)
            for n in (1, 5, 9):
                wav(f"coldiron-anvil-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
            wav(f"coldiron-anvil-{name.replace(' ', '-').lower()}-n9-on-clank.wav", Body(sp, g, D_).both(9))
        ctla = []
        a0_ = rows_a[0]
        for name, sp, g, D_ in (("0 FLAT", dict(a0_["sp"], step="flat"), a0_["g"], a0_["D"]),
                                ("0 TICK", a0_["sp"], a0_["g"], 0.07),
                                ("0 HARM", dict(a0_["sp"], modes="harm"), a0_["g"], a0_["D"]),
                                ("0 LOUD", a0_["sp"], float(f"{a0_['g'] * 1.25:.4g}"), a0_["D"])):
            calls = ax(sp, g, D_, 5)[1][0]
            M = anvil_measure(Body(sp, g, D_), calls, g, D_, name, sp, lambda n: anvil_f(a0_["sp"], n))
            ctla.append(M)
            wav(f"coldiron-anvil-{name.replace(' ', '-').lower()}-n5.wav", M["xs"][5])
        M = anvil_measure(Clank(), 7, 0, 0, "0 CLANK", None, lambda n: anvil_f(a0_["sp"], n))
        ctla.append(M)
        for (name, _sp, blurb) in ANVIL_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 FLAT    BAR at A5 for every count -- a control\n"
              "    0 TICK    BAR ringing 50 ms -- a control\n"
              "    0 HARM    BAR on whole-number partials (1 : 2 : 3) -- a control\n"
              "    0 LOUD    BAR at 1.25x its gain -- a control\n"
              "    0 CLANK   the engine's own clank at mass 5, played as the anvil -- a control")
        print(f"  RULE  {ANVIL_RULE}")
        for M in rows_a:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctla:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_a, "anvil")
        ai = fb if ok is None else min(ok, key=lambda i: (round(max(rows_a[i]["regs"].values()) / 0.05),
                                                          rows_a[i]["calls"], i))
        A_ = rows_a[ai]
        print(f"  PICK  {A_['name']}  g {A_['g']}, D {A_['D']}; notes " +
              " ".join(f"{f_:.0f}" for f_ in A_["notes"]) + f" Hz at counts 1-9; peak <= {A_['pk_all']:.3f} "
              f"(every count and draw), {A_['pk_both']:.3f} with the clank; over the clank "
              f"{A_['over']:+.1f} dB or more; loudest 50 ms {db(A_['top'] / h_lo):+.1f} dB re the hit @ 9.3")

        # ---- THE CLOSE -----------------------------------------------------
        lev_k = dict(lo=2 * w_hi, hi=0.5 * C_["top"])
        tgt_k = math.sqrt(lev_k["lo"] * lev_k["hi"])
        print(f"\nCLOSE -- 'the ring dying, 0.4s'. Level-matched: loudest 50 ms {tgt_k:.4f} (the centre of "
              f"{lev_k['lo']:.4f}-{lev_k['hi']:.4f}), AUDIBLE {CLOSE_AUD:g} ms; the ring is the picked cast's "
              f"({C_['name']}: {C_['sp']['ring']} on {C_['sp']['f']:g} Hz)")

        def kx(sp, g, D_, seed=None):
            return R([["body", T0, close_body(sp, C_["sp"], g, D_), {}]], seed=seed)

        def calib_close(sp):
            g, D_ = 0.1, 1.0
            aud = sp.get("aud", CLOSE_AUD)
            for _ in range(4):
                if sp["kind"] != "held":
                    lo_, hi_ = math.log(0.05), math.log(4.0)
                    for _ in range(12):
                        mid = 0.5 * (lo_ + hi_)
                        if basic(kx(sp, g, math.exp(mid))[0])["aud"] < aud: lo_ = mid
                        else: hi_ = mid
                    D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = g * tgt_k / basic(kx(sp, g, D_)[0])["top"]
            return float(f"{g:.4g}"), D_

        KREG = ("clank@5", "hit@9.3", "death", "rune-crack")

        def close_measure(sp, g, D_, name):
            x, calls = kx(sp, g, D_)
            x2, _ = kx(sp, g, D_)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, D=D_, name=name, sp=sp)
            draws = [kx(sp, g, D_, seed=sd)[0] for sd in NOISE_SEEDS]
            M["note"] = pitch(x, T0, T0 + 0.15, lo=60, hi=RING_LP)
            M["off"] = cents(M["note"], C_["note"])
            M["inh_r"], M["inh_c"], M["inh_db"] = inharm(x, T0, T0 + 0.2, M["note"])
            M["tat"], M["rise_after"], M["hold"] = dying(x)
            M["hf"], M["nz"] = unstruck(x, draws)
            M["inb"] = band_rms(x, M["note"], T0, T0 + 0.25)
            M["inb_floor"] = 2 * bedp90(M["note"])
            # HEARD: the loudest of its partials against the score (see WHAT THE FIRST CUT GOT WRONG)
            hr = []
            for r_, k_, d_ in RING[C_["sp"]["ring"]][0]:
                f_ = M["note"] * r_
                hr.append((band_rms(x, f_, T0, T0 + 0.25) / (2 * bedp90(f_)), f_))
            M["heard"], M["heard_f"] = max(hr)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in KREG}
            M["regs"]["anvil"] = float(np.median([cos(DB[i], A_["DB"][i]) for i in range(12)]))
            M["regs"]["cast"] = float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)]))
            M["why"] = close_why(M, lev_k)
            return M

        print(f"  {'cand':<10}{'g':>8}{'D':>7}{'calls':>6}{'aud':>5}{'top':>8}{'note':>7}{'off':>5}{'inh c/dB':>10}"
              f"{'tat':>5}{'riseA':>6}{'hold':>6}{'hf':>6}{'nz':>7}{'inb':>8}{'heard dB@Hz':>13}"
              + "".join(f"{k[:5]:>6}" for k in KREG + ("anvil", "cast")))

        def close_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['D']:>7.3g}{M['calls']:>6d}{M['aud']:>5.0f}{M['top']:>8.4f}"
                  f"{M['note']:>7.1f}{M['off']:>5.0f}{M['inh_c']:>5.0f}/{M['inh_db']:<+4.0f}{M['tat']:>5.0f}"
                  f"{M['rise_after']:>6.1f}{M['hold']:>6.2f}{M['hf']:>6.3f}{M['nz']:>7.1f}{M['inb']:>8.4f}"
                  f"{db(M['heard']):>+7.1f}@{M['heard_f']:<5.0f}"
                  + "".join(f"{r_[k]:>6.2f}" for k in KREG + ("anvil", "cast")))

        rows_k = []
        for name, sp, blurb in CLOSE_CANDIDATES:
            g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name)
            rows_k.append(M); close_line(M)
            wav(f"coldiron-close-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlk = []
        k0 = rows_k[0]
        for name, sp, blurb in CLOSE_CONTROLS:
            if sp["kind"] in ("struck", "other", "held"):
                g, D_ = k0["g"], k0["D"]
            else:
                g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name)
            ctlk.append(M); close_line(M)
            wav(f"coldiron-close-{name.replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in CLOSE_CANDIDATES + CLOSE_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print(f"  RULE  {CLOSE_RULE}")
        for M in rows_k:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlk:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_k, "close")
        ki = fb if ok is None else min(ok, key=lambda i: (round(max(v for k, v in rows_k[i]["regs"].items()
                                                                    if k != "cast") / 0.05),
                                                          rows_k[i]["calls"], i))
        K_ = rows_k[ki]
        print(f"  PICK  {K_['name']}  g {K_['g']}, D {K_['D']}; loudest 50 ms {db(K_['top'] / C_['top']):+.1f} dB re "
              f"the cast, {db(K_['top'] / w_hi):+.1f} dB re the wall")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   anvil {A_['name']}   close {K_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        info = dict(c_aud=C_["aud"], c_top=db(C_["top"] / h_lo), c_lead=C_["lead"], c_hend=C_["hend"],
                    c_order=C_["order"], c_reg=max(C_["regs"].values()), c_regw=who(C_["regs"]),
                    a_lo=note_name(A_["notes"][0]), a_hi=note_name(A_["notes"][-1]),
                    a_aud=f"{A_['aud_lo']:.0f}-{A_['aud_hi']:.0f}", a_pk=A_["pk_all"], a_over=A_["over"],
                    a_reg=max(A_["regs"].values()), a_regw=who(A_["regs"]),
                    k_db=db(K_["top"] / C_["top"]), k_aud=K_["aud"],
                    k_reg=max(v for k, v in K_["regs"].items() if k != "cast"),
                    k_regw=who({k: v for k, v in K_["regs"].items() if k != "cast"}),
                    k_hf=K_["heard_f"], k_heard=db(K_["heard"]),
                    n_cast=len(CAST_CANDIDATES), n_anvil=len(ANVIL_CANDIDATES), n_close=len(CLOSE_CANDIDATES))
        arms = arms_code(C_, A_, K_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        if arms.count(SFX_ANCHOR) != 1 or not arms.endswith(SFX_ANCHOR):
            raise SystemExit("the Sfx row does not re-emit its anchor exactly once, last")
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        abt = anvil_body(A_["sp"], A_["g"], A_["D"])
        rp = [float(np.abs(R([["body", T0, abt, {"n": 9}]])[0] - R([["body", T0, abt, {"n": 9}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the loudest anvil rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        xa, _ = R([["arm", T0, "ult", {"w": RELIC}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa - C_["x"]).max())))
        for n in (-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, None):
            p_ = {"w": "coldiron-anvil"} if n is None else {"w": "coldiron-anvil", "n": n}
            x1, _ = R([["arm", T0, "ult", p_]], rows=sfx_rows)
            x2, _ = R([["body", T0, abt, {"n": min(CAP, max(1, n or 0))}]])
            chk.append((f"anvil@{n}", float(np.abs(x1 - x2).max())))
        xk, _ = R([["arm", T0, "ult", {"w": "coldiron-close"}]], rows=sfx_rows)
        chk.append(("close", float(np.abs(xk - K_["x"]).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9.3, 11.6, 23, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("clank", {"mass": 1.1}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("aegis", {"n": 10, "back": 5}), ("aegis", {"broke": True}),
                   ("vine", {"plant": True}), ("vine", {"coil": True}), ("vine", {"miss": True}), ("vine", {"n": 2}),
                   ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}), ("fork", {}),
                   ("scour-hold", {"n": 3}), ("scour-tick", {"n": 2}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = page.evaluate(r"""() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();
            const a = [...s.matchAll(/w === "([a-z-]+)"/g)].map(m => m[1]);
            return [...new Set([...AC.WEAPONS.map(w => w.id), ...a])]; }""")
        ult_ids = [w_ for w_ in ult_ids if w_ != RELIC and not w_.startswith(RELIC + "-")]
        others += [("ult", {"w": w_, "n": 2, "dmg": 20}) for w_ in ult_ids]
        same_ = []
        for kind_, p_ in others:
            x1, _ = R([["play", T0, kind_, p_]]); x2, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows)
            same_.append((kind_ + "/" + str(p_.get("w", p_.get("dmg", p_.get("n", p_.get("mass", ""))))) +
                          ("!" if p_.get("crit") else ""), float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, spark x3, wall, death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3, "
              f"fork, scour x4, and {len(ult_ids)} ult ids -- every relic's cast and every sub-voice the ult arm "
              f"names): worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa - rcx).max())
        print(f"  ult/coldiron vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, repro=max(rp))

        # ---- THE resolveClank AND tickTemper ROWS -----------------------------
        seeds = [a.seed0 + k for k in range(a.seeds)]
        mirror = page.evaluate("() => { try { new AC.Match('coldiron', 'coldiron', 1); return true; } "
                               "catch (e) { return false; } }")
        print("\nTHE resolveClank AND tickTemper ROWS, applied to their prototypes' own source, run beside the "
              f"originals on real fights (the mirror match {'included' if mirror else 'refused by Match -- not run'}):")
        WR = page.evaluate(WIRE_JS, [seeds, [ANVIL_ANCHOR, ANVIL_CODE], [CLOSE_ANCHOR, CLOSE_CODE], mirror])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Coldiron both sides x every foe x seeds {seeds}"
              f"{' + the mirror' if mirror else ''}): {WR['same']}/{WR['fights']} identical (over, clock, both hp, "
              f"positions, velocities, stuns, both sunder counts, winner, the clank count, both temperTallies); "
              f"every other voice call identical in order, kind and opts in {WR['otherSame']}/{WR['fights']}")
        ns = np.array(WR["ns"]) if WR["ns"] else np.zeros(1)
        hist = {int(k): int((ns == k).sum()) for k in range(1, 10)}
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['won']} won binds -> "
              f"{WR['anvilV']} anvil voices ({WR['atCap']} on a loser already at its ceiling, the count unchanged; "
              f"{WR['shadeV']} won against a Twinshade "
              f"shade, carrying the shade's count); {WR['closes']} closes; problems "
              f"{WR['nbad']}")
        print("  the count an anvil carries: " + ", ".join(f"{k}: {v}" for k, v in hist.items() if v) +
              f"  ({int((ns > 6).sum())} past 6); won binds a window: median "
              f"{np.median(WR['perWin']) if WR['perWin'] else 0:.0f}, max {max(WR['perWin']) if WR['perWin'] else 0}")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["anvilV"] != WR["won"] or WR["closes"] != WR["ends"]["clock"] \
                or WR["won"] == 0 or WR["castV"] != WR["casts"] or WR["ends"]["clock"] == 0:
            FAILED.append("sim rows")
        WB = page.evaluate(WIRE_JS, [seeds, [ANVIL_ANCHOR, ANVIL_CODE_BAD], [CLOSE_ANCHOR, CLOSE_CODE], False])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the loser nudged 1e-9 on a won bind): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "won", "anvilV",
                                          "closes", "atCap", "mirrorV", "shadeV", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        rec["wire"]["count_hist"] = hist
        print(f"  THE CLOSE ON A DEATH: {WR['ends']['death']} windows closed by a death (in a kill flight) and "
              f"{WR['ends']['over']} by the fight's end play no close (checked above); both endings belong to the "
              f"death voice (Zenith's, Canopy's and Onslaught's rule).")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cf, cs, cside = a.clip.split(":")
        cs, cside = int(cs), int(cside)
        EV = page.evaluate(RECORD_JS, [cside, cf, cs, [ANVIL_ANCHOR, ANVIL_CODE], [CLOSE_ANCHOR, CLOSE_CODE]])
        assert not errors, errors[:3]
        casts_t = [e[0] for e in EV if e[3] == RELIC]
        closes_t = [e[0] for e in EV if e[3] == "coldiron-close"]
        if not casts_t or not closes_t:
            FAILED.append("the clip has no cast or no clock close")
        else:
            c0 = casts_t[0]; c1 = min([t_ for t_ in closes_t if t_ > c0] or [c0 + 60.0])
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs
                       if e[3] not in ("coldiron-anvil", "coldiron-close")]
            nocast = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            xn, _ = R(nocast, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd; xn = xn + bd
            an = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == "coldiron-anvil"]
            cl_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "coldiron-close"]
            ca_t = T0 + (c0 - lo_t)

            def ov(xa_, xb_, f, a_, d_):
                return db(band_rms(xa_, f, a_, a_ + d_) / max(band_rms(xb_, f, a_, a_ + d_), 1e-12))
            an_over = [ov(xw, xo, anvil_f(A_["sp"], n_), t_, 0.08) for t_, n_ in an]
            cl_over = [ov(xw, xo, K_["heard_f"], t_, 0.25) for t_ in cl_t]
            cl_over0 = [ov(xw, xo, C_["note"], t_, 0.25) for t_ in cl_t]
            ca_parts = [(ov(xo, xn, C_["note"] * r_, ca_t + 0.1, 0.25), C_["note"] * r_)
                        for r_, _k, _d in RING[C_["sp"]["ring"]][0]]
            ca_over, ca_f = max(ca_parts)
            ca_hiss = ov(xo, xn, 4000.0, ca_t, 0.1)
            print(f"\nIN A REAL WINDOW -- coldiron v {cf} (side {'AB'[cside]}), seed {cs}, cast at {c0:.2f}s, closed by "
                  f"its clock at {c1:.2f}s, {len(an)} won binds (counts {' '.join(str(n_) for _, n_ in an)}); the "
                  f"fight's own sounds and the score, with and without the anvil and close voices")
            print("  each anvil over the fight (its clank included) in its own third-octave, 0-80 ms: " +
                  " ".join(f"{v:+.1f}" for v in an_over) + " dB")
            print(f"  the close over the fight at its loudest partial ({K_['heard_f']:.0f} Hz), 0-250 ms: " +
                  " ".join(f"{v:+.1f}" for v in cl_over) + " dB (at the ring's note: " +
                  " ".join(f"{v:+.1f}" for v in cl_over0) +
                  f" dB);  the cast's ring over the fight without it, 100-350 ms, at its loudest partial "
                  f"({ca_f:.0f} Hz): {ca_over:+.1f} dB (partials " +
                  " / ".join(f"{v:+.1f} @ {f_:.0f}" for v, f_ in ca_parts) + "), its hiss "
                    f"(4 kHz, 0-100 ms): {ca_hiss:+.1f} dB")
            if (an_over and min(an_over) < 6) or (cl_over and min(cl_over) < 3) or ca_over < 3 or ca_hiss < 3 \
                    or len(an) == 0:
                FAILED.append("a new voice not heard in a real window")
            wav("coldiron-pick-real-window.wav", xw)
            wav("coldiron-pick-real-window-without.wav", xo)
            rec["real"] = dict(clip=a.clip, cast=c0, close=c1, anvils=an, anvil_over=an_over, close_over=cl_over,
                               close_over_note=cl_over0,
                               cast_over=ca_over, cast_parts=ca_parts, cast_hiss=ca_hiss)
        # the three picks in order, for the ear: the cast, the anvil at 2 4 6 8 9 over its clank, the close
        seq = [["arm", T0, "ult", {"w": RELIC}]]
        for k_, n_ in enumerate((2, 4, 6, 8, 9)):
            seq += [["arm", T0 + 0.9 + 0.55 * k_, "ult", {"w": "coldiron-anvil", "n": n_}],
                    ["arm", T0 + 0.9 + 0.55 * k_, "clank", {"mass": IRON}]]
        seq += [["arm", T0 + 4.0, "ult", {"w": "coldiron-close"}], ["arm", T0 + 4.8, "hit", {"dmg": BLADE, "crit": False}]]
        xq_, _ = R(seq, secs=7.0, rows=sfx_rows)
        wav("coldiron-pick-sequence.wav", xq_)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), anvil=strip(rows_a), anvil_controls=strip(ctla),
               close=strip(rows_k), close_controls=strip(ctlk), wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_kr": C_["kr"], "cast_D": C_["D"],
                     "anvil": A_["name"], "anvil_g": A_["g"], "anvil_D": A_["D"],
                     "close": K_["name"], "close_g": K_["g"], "close_D": K_["D"]})
    print(f"\nTHE PICKS  cast {C_['name']}   anvil {A_['name']}   close {K_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    rows = [dict(label="Sfx: Coldiron's cast, anvil and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="resolveClank: the anvil voice on a won bind, after the loser's sunder, carrying its count",
                 anchor=ANVIL_ANCHOR, mode="replace", code=ANVIL_CODE),
            dict(label="tickTemper: the close voice, when the window closes by its clock with both alive",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE)]
    for r_ in rows:
        if html.count(r_["anchor"]) != 1 or r_["code"].count(r_["anchor"]) != 1:
            raise SystemExit(f"row '{r_['label']}': the anchor is not unique, or not re-emitted once")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The three rows are the edits; all three were applied "
          "to the page's own code above.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
