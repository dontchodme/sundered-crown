#!/usr/bin/env python3
"""CANOPY'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v99.

    python ironwood_voice_lab.py --game ../02-chain/sc-canopy-w38.html --rows rows.json

v69 §7.2 SOUND, every word of it: "Cast (the rooting): a deep creak and a
ground-thud, 0.5s, share below 120 Hz >= 0.5 -- the heaviest thing in the hall
is putting down roots. The sprout (at 1.5s): two quick woody cracks, 80ms
each, a fifth apart. A bough blow: the hammer's own strike voice, pitched down
a fourth and quieter (peak <= 0.6 of the hammer's) -- a lighter head on a
longer arm. The wither: a dry creak falling in pitch, 0.4s, quiet." Rick, for
the batch's art and sound: "you pick i overrule". So this lab does not offer a
spread -- it renders three to five candidates a voice beside CONTROLS that can
come back wrong, prints the numbers each pick is made on, and PICKS by a rule
written in this file (`*_RULE`). He overrules from one clip.

THE FOUR EVENTS AND WHERE THEY FIRE:
  cast    the bare id `ult/ironwood`, which `fireUlt` plays for every relic.
          Ironwood has NO arm today: it falls through to the shared
          rune-crack (so does Censer -- measured below, to 1e-7). The arms go
          BEFORE that fallback; the fallback is not touched.
  sprout  `ult/ironwood-sprout` from `tickTree`, inside the block that makes
          the blade set, so on the frame the two new boughs exist (and are
          live for hits). Once a window, only a window that reaches 1.5 s.
  bough   the ordinary `hit` voice, which `resolveHit` plays for every blow,
          called with ONE more plain number while Ironwood's tree stands:
          `bough: w.ult.winDmg` (0.38). The hit arm grows one branch in front
          of itself for that opt; every call without it is the old arm, byte
          for byte. `dmg` stays the damage DEALT (every tool that reads the
          hit's opts reads the same number); the branch recovers the blow the
          hammer would have struck, `dmg / bough`, so the bough's voice is
          the HAMMER'S strike voice -- its weight, its jitter, its crits --
          pitched down a fourth and quieter. Outside the window the call is
          the hammer's, unchanged.
  wither  `ult/ironwood-wither` from `tickTree` on the frame the window
          closes BY ITS CLOCK with the caster alive -- never on a death, never
          once the fight is over (step() stops calling the tickers). The
          sim's 0.4 s wither starts on a death too; the VOICE does not, and
          the reason is measured below (THE WITHER ON A DEATH).

THE CONTROLS, and what each one is for:
  rune-crack   what Ironwood's cast plays TODAY (and Censer's); v88 published
               0.608 / 450 ms -- reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@24       Ironwood's own blow (blade 24): what the bough is measured
               against, and the level every voice is judged against, on its
               quietest / loudest noise draw. HAMMER: as a bough candidate it
               must come back wrong (peak ratio 1.00, no fourth)
  hit@9.12     the hit at the bough's 0.38x -- what a bough blow plays TODAY.
               PLAIN: it must come back wrong on the bough's rule (a lighter
               blow is pitched UP by the hit arm's weight, not down)
  the row      Grudgebearer, Bulwarden, Shroudmaul and Ravelbone's casts (and
               Censer's, which is rune-crack): the warhammer row the cast must
               not sound like; their own median pairwise register is printed
  death        the death voice: the cast is low and must not read as one, and
               it is what a death-close wither would sit under
  wall         the commonest sound in a fight: the quiet voices' floor
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  THUD, CREAK  the cast's two halves alone: each must fail the cast's rule
  RISE         the wither's creak rising instead of falling: must fail
  CAST-QUIET   the picked cast at the wither's level: must fail "dry"

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT. Each candidate is generated as the JS
    body that will sit in the arm (constants rounded first) and rendered by
    evaluating that text on the synth; the row is then applied to
    `Sfx.prototype.play`'s own source and rendered again, and must match to
    1e-6. There is no second transcription to get wrong.
  * The shared measures are zenith_voice_lab's, imported unchanged (E50 =
    50 ms RMS at a 5 ms hop; TOP = the loudest 50 ms; AUDIBLE = first to last
    5 ms RMS window above 2% of the voice's own loudest; GONE = where it
    ends; RISE = 10 -> 90% of the 1 ms envelope; REG = cosine of 1/3-octave
    band amplitudes, 25 Hz-16 kHz, the median over noise draws; IN-BAND =
    RMS inside the third-octave round a pitch; PITCH = FFT peak, Hann,
    zero-padded, parabolic).
  * LOW = the share of the voice's power below 120 Hz (the whole render from
    t = 1.0, through the chain) -- the spec's own number.
  * THUD-AT = where the <120 Hz band's 5 ms RMS peaks, ms after the event.
  * PULSED = how much a voice is a train of pulses at a creak's rate: the
    voice high-passed at 150 Hz (FFT), its 1 ms RMS envelope, and in 150 ms
    windows (25 ms hop) over the creak's span the highest Pearson
    autocorrelation of that envelope at lags 12-60 ms (17-83 pulses a
    second); the median over the windows, a window whose high-passed RMS is
    more than 30 dB under the voice's loudest 50 ms scoring 0 (a creak nobody
    can hear is not a creak). RATE = 1000 / the median best lag. The THUD
    control reads 0.00.
  * FALL = cents from the spectral peak (80 Hz-3 kHz, Hann, parabolic) of the
    voice's first 100 audible ms to that of its last 100.
  * WOODY = a struck bar's inharmonic mode: the crack's strongest spectral
    peak between 1.5x and 4x its note, its distance in cents from the nearest
    whole multiple of the note and its level re the note's own peak.
  * CRACK = how far the bough's noise crack sits from the hammer's: the power
    spectra of the twelve noise draws AVERAGED, each point the mean power in a
    1/12-octave window on a 1/96-octave grid, 500 Hz-8 kHz (where the crack
    lives and the sine body does not), and the lag (12.5 c, parabolic) that
    best correlates the two. BODY = the ratio of the FFT peaks of the two
    voices' first 30 ms, 25-400 Hz (the hit's falling sine at its start). A
    fourth down is 0.75 = -498 cents. (Each half reads the other half's
    candidate as 0: BODY, the candidate that shifts only the sine, reads
    CRACK -1 c.)
  * PEAK RATIO = the bough's sample peak over the hammer's, ON THE SAME noise
    draw, at the same jitter and crit; judged on its worst draw.
  * ENV-CORR = Pearson correlation of two E50 curves (dB, floored 40 dB
    under their tops), aligned at onset (zenith_voice_lab's).
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's creak is set so LOW is 0.60 (the gate's 0.5 plus a
    margin for the noise draws) and its gain so TOP sits at the centre of
    its window; the sprout's gain and decay so its loudest 50 ms is at the
    centre of ITS window and a crack is audible 80 ms; the bough's gain so
    its WORST peak ratio -- twelve draws at jitter 1, four each at jitter 0.85
    and 1.15 and on a crit -- is 0.55, the spec's 0.6 less a margin a
    session's noise buffer cannot cross; the wither's gain so it sits
    9 dB under the picked cast's top (Zenith's close). Constants are rounded
    BEFORE any measured render, so a shipped arm is bit-for-bit what was
    measured.

THE WITHER ON A DEATH -- decided, and measured: the voice plays on a CLOCK
close with the caster alive only, as Zenith's and Daybreak's closes do. A
caster's death closes the window on the frame the fight ends (the death voice
a median 0 ms later), and a foe's death ends the fight before any close
(step() stops calling the tickers), so both endings belong to the death voice.
It is a choice about the ending, not a limit: rendered at the measured
offsets, the wither would stand clear of the kill's own sounds in its band.

THE DECLARED CHOICES (not candidates -- words of §7.2 turned into numbers):
  * THE GROUND-THUD (every cast candidate): a sine falling 72 -> 28 Hz over
    0.4 s and a 140 Hz lowpass noise burst of 0.18 s at 0.6 of it. 72 Hz sits
    under the death voice's 120 Hz start and the hit's 142 Hz body, so the
    rooting is the deepest single thing in the hall.
  * THE THUD IS ON THE CAST FRAME: that frame is the one instant the picture
    has (v69 §7.1: "the ball stops dead", the pin). LATE, the creak first and
    the thud 0.34 s on, is a candidate the rule can reject on it.
  * A CREAK IS A TRAIN OF PULSES (the toolkit has no held note, CLAUDE.md
    4.5, and a creak is stick-slip): pulses slowing geometrically from 50 to
    25 a second over the creak (the bark setting), each interval x (1 + 0.12
    sin 2.4k) so the train is irregular and pure arithmetic -- no random
    number anywhere. The cast's creak swells and settles (0.55 + 0.45 sin).
  * THE SPROUT'S FIFTH: A then E, the score's i and v, RISING (the boughs
    grow out); the second crack 90 ms after the first (80 ms and 10 ms of
    air, so the two never overlap and read as two).
  * THE BOUGH'S FOURTH: every frequency of the strike x 0.75 exactly.
  * THE WITHER'S CREAK: pulses slowing from 55 to 24 a second (winding
    down), the level falling to 0.4 of its start, the pitch falling across
    0.4 s.

THE PICKS, on Chromium 151.0.7922.34, sc-canopy-w38 13f8d25aa7ebe34a, fight
seeds 99601-99602 (140 fights):

  cast    4 BEAM   the thud on the cast frame (a sine 72 -> 28 Hz and a 140 Hz
                   lowpass burst) and a timber creak: a 520 Hz sine and its 2.76
                   mode at 0.4, pulsed 50 -> 25 a second over 0.45 s. LOW 0.60 on
                   all twelve draws, the thud peaking at 10 ms, PULSED 0.63 (31 a
                   second), the creak -8.2 dB under the thud; audible 475 ms; TOP
                   -2.9 dB re the hit @ 24, +18.9 dB re the wall. Register 0.30
                   against rune-crack, at most 0.67 against the row (Shroudmaul;
                   the row's own median pair is 0.70), 0.35 against the death
                   voice, 0.34 against the hit. BAR passes too (0.76 against
                   Shroudmaul) and loses the register tiebreak; GRAIN out (LOW
                   0.31 on its worst draw -- the toolkit finding below); KNOCK out
                   (0.85 against Shroudmaul); LATE out (the thud at 356 ms).
  sprout  1 BLOCK  a woodblock (a triangle, its 2.76 mode at 0.3, an 8 ms click),
                   A5 and then E6 90 ms later: 880 / 1320 Hz (0 cents off 3:2),
                   each crack audible 80 / 75 ms, the mode -14 dB under the note;
                   loudest 50 ms -9.4 dB re the hit @ 24, +12.2 dB re the wall;
                   register at most 0.44 (rune-crack). KNOCK (an octave down)
                   passes and loses the register tiebreak (0.55 against the cast);
                   SNAP out (a 6 ms rise, 42 cents off its note); CLAVE out (not
                   woody: nothing within 50 dB of the note).
  bough   1 PITCH  the hammer's strike rebuilt from dmg / bough, every frequency
                   x 0.75: CRACK -486 c, BODY -501 c; peak 0.44 of the hammer's
                   on the same draw, 0.55 at the worst (jitter 0.85-1.15, crits);
                   loudest 50 ms -6.2 dB re the hit @ 24, +15.5 dB re the wall;
                   ENV-CORR 1.00 with the hammer's strike. TAPE passes (0.97)
                   and loses the tiebreak; BODY out (CRACK -1 c); LIGHT out (BODY
                   -222 c). PLAIN, what a bough blow plays today, comes back
                   pitched UP (BODY +286 c, CRACK +474 c) at 0.95 of the hammer.
  wither  4 BEAM   the cast's creak run the other way: a 20 ms sine and its 2.76
                   mode pulsed 55 -> 24 a second, falling 780 -> 360 Hz (FALL
                   -861 c), audible 360 ms, LOW 0.06, -9.0 dB under the cast's
                   top (-11.9 dB re the hit @ 24, +9.9 dB re the wall); register
                   at most 0.56 (the sprout). KNOCK and BAR pass (0.40 / 0.50)
                   and lose the first tiebreak (built as the cast's creak is);
                   GRAIN out (0.86 against the sprout).

  In play (140 fights; 526 windows -- 453 closed by the clock, 13 by the
  caster's death, 60 by the fight's end): 512 sprouts and 512 sprout voices,
  each on its blade set's frame; 453 withers, none on a death or a fight's end;
  2616 tree blows, every one carrying `bough`, and no other blow (883 hammer
  blows outside, 2808 foe blows, 142 ward bursts untouched); 140/140 fights
  identical and the hit-voice sequence identical but for the opt; the
  sim-write control 0/140. In a real window (v Starwarden, 99601) the sprout
  stands +16.7 dB and the wither +9.2 dB over the fight and the score in their
  own third-octaves; every blow of that fight rendered at the damage it dealt:
  the boughs 0.48 of the hammer's (median), the loudest 0.50. Main-thread cost
  a call: cast 0.9 ms, sprout 0.2, wither 0.6, bough 0.1 (the hit's own 0.1).

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules above were
written before the first table; the first table then showed four instruments
that could not see what they were built to see, and one threshold nothing
could pass. Each was changed ONCE, for the reason given, before the picks:
  * SHIFT (the bough's whole-spectrum lag) read 0 for every candidate: below
    ~60 Hz some 1/48-octave bins held no FFT line, the empty bins were the
    same in every voice, and they aligned at lag 0. Smoothed and averaged
    over the draws it still could not tell BODY (only the sine shifted) from
    PITCH (everything shifted): -537 against -558 c. It is now CRACK, on the
    band the crack lives in (BODY -1 c, PITCH -486 c).
  * PULSED read the THUD control (no creak at all) as 0.99: the high-pass's
    ringing, 60 dB down, is perfectly periodic. It now needs the window to
    be heard (the -30 dB floor), and the THUD control reads 0.00.
  * FALL took the spectral centroid, and read FRY's sawtooth falling an
    octave as +46 cents: a saw's centroid is set by the 6 kHz cap, not its
    pitch. It now takes the spectral peak (FRY -1046 c; GRAIN's 900 -> 420 Hz
    resonance -173 -> -1224 c).
  * THE SPROUT'S 'WOODY' GATE was first "the crack's centroid >= 1.3x its
    pitch", and it failed every candidate, a woodblock with a -10 dB 2.76
    mode included (1.09x): a threshold no woodblock meets measures nothing
    but the threshold. It now asks for the bar's inharmonic mode (WOODY),
    and CLAVE, the plain sine, still fails it (-51 dB).
  * The bough was first level-matched to a peak ratio of 0.50 on one draw,
    and its worst case (a crit) then sat at 0.598 against the 0.6 gate; it
    is now matched on the worst case (0.55).

A TOOLKIT FINDING (for CLAUDE.md 4.5, beside `_burst`'s 0.6 s): EVERY `_burst`
STARTS THE NOISE BUFFER AT ITS FIRST SAMPLE (`src.start(t)`, no offset). So a
train of N noise pulses is N copies of ONE slice of the session's buffer --
and the live game's buffer is `Math.random`, a new one every session. A short,
narrow noise pulse therefore swings with the session: GRAIN's creak (300 Hz,
Q 5, an effective ~1.5 ms excitation, since `_burst` ramps to 0.0001 over its
whole length) reached LOW 0.60 on render.py's draw and 0.31 on the worst of
twelve. The tonal creaks read 0.60 on all twelve. A voice that must hold a
number on every session builds its repeated grain from tones.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * both Sfx rows (the hit branch; the three ult arms) are applied to
    `Sfx.prototype.play`'s own source and rendered: each arm, and the bough
    branch at every jitter and crit, must reproduce its candidate to 1e-6;
    every other voice through the patched play (all 35 other casts, the hit
    at five weights with and without a crit, spark, wall, death, clank,
    seal, nova, hex-snap) must be unchanged; `ult/ironwood` must NOT be
    rune-crack any more;
  * the two tickTree rows and the resolveHit row are applied to the
    prototype's own sources and run on real fights beside the unpatched ones:
    every fight identical (over, clock, both hp, both positions, the whole
    treeTally), and the sequence of hit voices identical but for the one opt;
    one sprout voice on the frame each blade set appears; one wither per
    window closed by its clock and none otherwise; every blow Ironwood lands
    while the tree stands carries `bough` = winDmg and no other blow does (a
    ward's shatter plays its own `hit` inside resolveHit's call -- Lightkeeper,
    Farwarden -- and is told apart by its caller: it is not a blow and keeps
    its voice). There is no mirror match: `Match` refuses a relic against
    itself. The same rows plus ONE sim write (the foe nudged 1e-9 on a bough
    blow) must come back NOT identical, or "identical" proves nothing. (The Sfx rows cannot reach the simulation
    at all: `play` returns on its first line with no audio context, which is
    every headless run.)
  All anchors must occur exactly once in the game file.

Writes wavs to 05-reference/v99/ironwood-*.wav at RAW level (gitignored).
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

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
# The shared definitions, imported unchanged so every number here means what
# it means in v98's lab. (zenith_voice_lab's module body only checks its own
# candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    env_corr, fmt, pcm, pitch, write_wav)

HERE = pathlib.Path(__file__).parent
BLADE = 24.0                              # Ironwood's dmg (stage 5)
WIN = 0.38                                # w.ult.winDmg (stage 5)
FOURTH = 0.75                             # a just fourth down
BOUGH_WORST = 0.55                        # the bough's level-matched worst peak ratio
LOW_TARGET = 0.60                         # the cast's level-matched low share
WITHER_UNDER_DB = 9.0                     # the wither under the cast's top
SPROUT_GAP = 0.09                         # the second crack's onset, s
A5 = 880.0

# =============================================================== THE CAST ===
# "a deep creak and a ground-thud, 0.5s, share below 120 Hz >= 0.5". Every
# candidate carries the same declared thud; they differ in what a creak
# pulse IS, and in the order.
CAST_CANDIDATES = [
    ("1 GRAIN", dict(creak="grain", order="first"),
     "a 300 Hz woody resonance (bandpass noise, Q 5, 14 ms) pulsed 50 -> 25 a second"),
    ("2 KNOCK", dict(creak="knock", order="first"),
     "a 130 Hz triangle knock (28 ms) pulsed 50 -> 25 a second"),
    ("3 BAR", dict(creak="bar", order="first"),
     "a wooden bar struck: a 220 Hz triangle and its 2.76 mode (607 Hz) at 0.5, pulsed 50 -> 25 a second"),
    ("4 BEAM", dict(creak="beam", order="first"),
     "a timber ringing: a 520 Hz sine and its 2.76 mode (1435 Hz) at 0.4, pulsed 50 -> 25 a second"),
    ("5 LATE", dict(creak="beam", order="late"),
     "BEAM's creak first, 0-0.36 s, and the thud at 0.34 s (the roots landing last)"),
]
PULSE = {
    "grain": 'this._burst(t + s, { freq: 300, q: 5, gain: a, dur: 0.014, type:"bandpass" });',
    "knock": 'this._tone(t + s, { freq: 130, gain: a, dur: 0.028, type:"triangle" });',
    "bar": ('this._tone(t + s, { freq: 220, gain: a, dur: 0.026, type:"triangle" });\n'
            'this._tone(t + s, { freq: 607, gain: a * 0.5, dur: 0.018, type:"sine" });'),
    "beam": ('this._tone(t + s, { freq: 520, gain: a, dur: 0.03, type:"sine" });\n'
             'this._tone(t + s, { freq: 1435, gain: a * 0.4, dur: 0.02, type:"sine" });'),
}


def cast_body(sp, g, kc, part="both", ind=10):
    """The cast arm's body. `part` renders a half alone (the lab's THUD and
    CREAK controls and the balance gate); the arm is `both`."""
    late = sp["order"] == "late"
    th = 0.34 if late else 0.0
    c0, c1 = (0.0, 0.36) if late else (0.03, 0.48)
    tt = f"t + {fmt(th)}" if th else "t"
    L = [f"const g = {fmt(g)}, kc = {fmt(kc)};"]
    if part in ("both", "thud"):
        L += [f'this._tone ({tt}, {{ freq: 72, to: 28, gain: g, dur: 0.4, type:"sine" }});',
              f'this._burst({tt}, {{ freq: 140, q: 0.7, gain: g * 0.6, dur: 0.18, type:"lowpass" }});']
    if part in ("both", "creak"):
        L += [f"for (let s = {fmt(c0)}, k = 0; s < {fmt(c1)}; k++){{",
              f"  const u = (s - {fmt(c0)}) / {fmt(round(c1 - c0, 6))}, "
              f"a = g * kc * (0.55 + 0.45 * Math.sin(Math.PI * u));",
              *["  " + q_ for q_ in PULSE[sp["creak"]].split("\n")],
              "  s += 0.02 * Math.pow(2, u) * (1 + 0.12 * Math.sin(k * 2.4));",
              "}"]
    return "\n".join(" " * ind + l for l in L)


# ============================================================= THE SPROUT ===
# "two quick woody cracks, 80ms each, a fifth apart". `st` moves the root in
# semitones from A5; the second crack is the root x 1.5, SPROUT_GAP later.
SPROUT_CANDIDATES = [
    ("1 BLOCK", dict(body="block", st=0),
     "a woodblock: a triangle, a free bar's 2.76 mode at 0.3, an 8 ms click; A5 -> E6"),
    ("2 SNAP", dict(body="snap", st=0),
     "a twig: noise rung at the pitch (bandpass Q 14) with a 6 ms highpass click; A5 -> E6"),
    ("3 KNOCK", dict(body="block", st=-12),
     "BLOCK an octave down, A4 -> E5: a heavier knock"),
    ("4 CLAVE", dict(body="clave", st=0),
     "a clave: a plain sine with a 5 ms click; A5 -> E6 -- the control on 'woody'"),
]
CRACK = {
    "block": ['this._tone(t + s, { freq: f, gain: g, dur: D, type:"triangle" });',
              'this._tone(t + s, { freq: f * 2.76, gain: g * 0.3, dur: D * 0.5, type:"sine" });',
              'this._burst(t + s, { freq: f * 3, q: 1.5, gain: g * 0.8, dur: 0.008, type:"bandpass" });'],
    "snap": ['this._burst(t + s, { freq: f, q: 14, gain: g, dur: D, type:"bandpass" });',
             'this._burst(t + s, { freq: 4000, q: 0.7, gain: g * 0.05, dur: 0.006, type:"highpass" });'],
    "clave": ['this._tone(t + s, { freq: f, gain: g, dur: D, type:"sine" });',
              'this._burst(t + s, { freq: 5000, q: 0.7, gain: g * 0.5, dur: 0.005, type:"highpass" });'],
}


def sprout_f(sp):
    return A5 * 2 ** (sp["st"] / 12)


def sprout_body(sp, g, D, only=None, ind=10):
    f1 = sprout_f(sp)
    pairs = [f"[0, {fmt(f1)}]", f"[{fmt(SPROUT_GAP)}, {fmt(f1)} * 1.5]"]
    if only is not None:
        pairs = [pairs[only]]
    L = [f"const g = {fmt(g)}, D = {fmt(D)};",
         f"for (const [s, f] of [{', '.join(pairs)}]){{"]
    L += ["  " + c for c in CRACK[sp["body"]]]
    L += ["}"]
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE BOUGH ===
# "the hammer's own strike voice, pitched down a fourth and quieter (peak
# <= 0.6 of the hammer's)". The strike is the hit arm's, verbatim in its
# arithmetic; `k` is the fourth, `v` the level (solved), `r` a time scale.
BOUGH_CANDIDATES = [
    ("1 PITCH", dict(weight="hammer", burst=True, r=None),
     "every frequency of the hammer's strike x 0.75, its envelope unchanged"),
    ("2 TAPE", dict(weight="hammer", burst=True, r="4 / 3"),
     "the strike slowed like tape: every frequency x 0.75 and every length x 4/3"),
    ("3 BODY", dict(weight="hammer", burst=False, r=None),
     "only the strike's sine body x 0.75; its noise crack unchanged"),
    ("4 LIGHT", dict(weight="blow", burst=True, r=None),
     "the hit at the bough's OWN (dealt) weight, x 0.75 -- the lighter head taken literally"),
]


def bough_body(sp, v, ind=8):
    wexpr = ("(p.dmg || 10) / p.bough / 45" if sp["weight"] == "hammer" else "(p.dmg || 10) / 45")
    r = f" * {sp['r']}" if sp["r"] else ""
    bk = " * k" if sp["burst"] else ""
    L = [f"const w = clamp({wexpr}, 0.12, 1), k = {fmt(FOURTH)}, v = {fmt(v)};",
         f"this._burst(t, {{ freq: (2600 - 1500*w){bk}, q: 1.1, gain: (0.16 + 0.20*w) * v, "
         f"dur: (0.06 + 0.06*w){r} }});",
         f"this._tone (t, {{ freq: (190 - 90*w) * k, to: 46 * k, gain: (0.22 + 0.26*w) * v, "
         f"dur: (0.11 + 0.13*w){r}, type:\"sine\" }});",
         f"if (p.crit) this._tone(t, {{ freq: 1500 * k, to: 520 * k, gain: 0.16 * v, "
         f"dur: 0.16{r}, type:\"triangle\" }});"]
    return "\n".join(" " * ind + l for l in L)


# ============================================================= THE WITHER ===
# "a dry creak falling in pitch, 0.4s, quiet". A pulse train as the cast's
# creak is, slowing 55 -> 24 a second, its pitch falling f0 -> f1.
WITHER_CANDIDATES = [
    ("1 GRAIN", dict(pulse="grain", f0=900, f1=420, q=6),
     "GRAIN's pulse (bandpass noise, Q 6, 12 ms) with its resonance falling 900 -> 420 Hz"),
    ("2 KNOCK", dict(pulse="knock", f0=420, f1=200, q=None),
     "KNOCK's pulse (a 22 ms triangle) falling 420 -> 200 Hz"),
    ("3 BAR", dict(pulse="bar", f0=420, f1=200, q=None),
     "BAR's pulse (a 22 ms triangle and its 2.76 mode at 0.5) falling 420 -> 200 Hz"),
    ("4 BEAM", dict(pulse="beam", f0=780, f1=360, q=None),
     "BEAM's pulse (a 20 ms sine and its 2.76 mode at 0.4) falling 780 -> 360 Hz"),
]
WPULSE = {
    "grain": 'this._burst(t + s, {{ freq: f, q: {q}, gain: a, dur: 0.012, type:"bandpass" }});',
    "knock": 'this._tone(t + s, {{ freq: f, gain: a, dur: 0.022, type:"triangle" }});',
    "bar": ('this._tone(t + s, {{ freq: f, gain: a, dur: 0.022, type:"triangle" }});\n'
            'this._tone(t + s, {{ freq: f * 2.76, gain: a * 0.5, dur: 0.015, type:"sine" }});'),
    "beam": ('this._tone(t + s, {{ freq: f, gain: a, dur: 0.02, type:"sine" }});\n'
             'this._tone(t + s, {{ freq: f * 2.76, gain: a * 0.4, dur: 0.014, type:"sine" }});'),
}


def wither_body(sp, g, ind=10):
    L = [f"const g = {fmt(g)};",
         "for (let s = 0, k = 0; s < 0.37; k++){",
         f"  const u = s / 0.4, f = {fmt(sp['f0'])} * Math.pow({fmt(sp['f1'])} / {fmt(sp['f0'])}, u), "
         f"a = g * (1 - 0.6 * u);",
         *["  " + q_ for q_ in WPULSE[sp["pulse"]].format(q=fmt(sp["q"]) if sp["q"] else "").split("\n")],
         "  s += 0.018 * Math.pow(2.3333, u) * (1 + 0.12 * Math.sin(k * 2.4));",
         "}"]
    return "\n".join(" " * ind + l for l in L)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
HIT_ANCHOR = '      if (kind === "hit"){'
SPROUT_ANCHOR = '        T.sprouts++;'
WITHER_ANCHOR = '        f.treeWither = u.wither;'
RH_ANCHOR = '    SFX.play("hit", { dmg, crit });'

SPROUT_CODE = '''        T.sprouts++;
        /* CANOPY'S SPROUT (v69 §7.2: "two quick woody cracks, 80ms each, a
           fifth apart"): on the frame the two new boughs exist and are live.
           Presentation only: SFX.play draws nothing, is a no-op headless, and
           nothing here is read back (ironwood_voice_lab: fights identical). */
        SFX.play("ult", { w: "ironwood-sprout" });'''

WITHER_CODE = '''        f.treeWither = u.wither;
        /* CANOPY'S WITHER (v69 §7.2: "a dry creak falling in pitch, 0.4s,
           quiet"): only when the window runs out BY ITS CLOCK with the caster
           alive. A caster's death ends the fight on this frame, and a foe's
           death ends it before any close (step() stops calling this), so both
           endings are left to the death voice, as Zenith's and Daybreak's
           closes are. Plain SFX.play; nothing is read back. */
        if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "ironwood-wither" });'''

RH_CODE = '''    /* CANOPY'S BOUGH BLOW (v69 §7.2): while Ironwood stands as a tree the
       blow's voice is the hammer's strike pitched down a fourth and quieter.
       ONE plain number more, `bough` (the tree's damage scale), so the hit
       arm can rebuild the hammer's weight from the damage dealt; `dmg` stays
       what was dealt. `ultTree` is null on every other relic and outside the
       window, so every other call is the old one. Presentation only
       (ironwood_voice_lab: fights identical). */
    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });'''

# the sim-write control: the same resolveHit row with the foe nudged 1e-9
RH_CODE_BAD = RH_CODE.replace(
    '    SFX.play("hit", self.ultTree ?',
    '    if (self.ultTree) foe.vx += 1e-9;\n    SFX.play("hit", self.ultTree ?', 1)

_refuse(SPROUT_CODE + WITHER_CODE + RH_CODE, "sim rows")


def _wrap(paras, indent, width=79):
    import textwrap
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


def hit_row_code(B_, info):
    c = _wrap([
        f'CANOPY\'S BOUGH BLOW -- v69 §7.2: "the hammer\'s own strike voice, pitched down a '
        f'fourth and quieter (peak <= 0.6 of the hammer\'s) -- a lighter head on a longer arm". '
        f'{B_["name"].split()[1]}, of {len(BOUGH_CANDIDATES)}, picked on the numbers by `ironwood_voice_lab.py` under '
        f'Rick\'s "you pick i overrule" (v99). `resolveHit` adds `bough` (the tree\'s damage '
        f'scale, 0.38) only while Ironwood\'s tree stands, so every other call takes the old arm '
        f'below, byte for byte.',
        f"The HAMMER'S strike, not the light one: `dmg / bough` is the blow the hammer would "
        f"have struck, so the weight, the jitter and the crits are the hammer's -- the plain hit "
        f"at the bough's 9 would be pitched UP ({info['plain_body']:+.0f} cents). Every "
        f"frequency x 0.75: measured {info['shift']:+.0f} cents on the noise crack and "
        f"{info['body']:+.0f} cents on the body's start; peak {info['pk_med']:.2f} of the "
        f"hammer's on the same draw ({info['pk_max']:.2f} at the worst draw, jitter or crit), "
        f"loudest 50 ms {info['wall_db']:+.1f} dB over the wall tick. Envelope correlation "
        f"{info['corr']:.2f} with the hammer's own strike."], 8)
    return (f'      if (kind === "hit" && p.bough){{\n{c}\n{bough_body(B_["sp"], B_["v"])}\n'
            f'      }}\n      else if (kind === "hit"){{')


def arms_code(C_, S_, W_, info):
    cname, sname, wname = (X["name"].split()[1] for X in (C_, S_, W_))
    what = {"grain": "a 300 Hz woody resonance (bandpass noise) pulsed",
            "knock": "a 130 Hz triangle knock pulsed",
            "bar": "a wooden bar struck (a 220 Hz triangle and its 2.76 mode at 0.5) pulsed",
            "beam": "a timber ringing (a 520 Hz sine and its 2.76 mode at 0.4) pulsed"}[C_["sp"]["creak"]]
    c_cast = _wrap([
        f'IRONWOOD\'S CAST, THE ROOTING -- v69 §7.2: "a deep creak and a ground-thud, 0.5s, share '
        f'below 120 Hz >= 0.5 -- the heaviest thing in the hall is putting down roots". {cname}, '
        f'of {len(CAST_CANDIDATES)}, picked on the numbers by `ironwood_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v99). Ironwood had no arm and fell through to rune-crack, which Censer, '
        f'Lastlight and Aureole still use, so this ADDS arms before that fallback and leaves it '
        f'alone.',
        f"The thud lands on the cast frame, where the ball stops dead: a sine falling 72 -> 28 "
        f"Hz and a 140 Hz lowpass burst. The creak is {what} slowing from 50 to 25 a second over "
        f"0.45 s -- a held note does not exist in this toolkit (CLAUDE.md 4.5), and a creak is "
        f"stick-slip, so it is a train of pulses; each interval x (1 + 0.12 sin 2.4k) keeps it "
        f"irregular with no random number. {info['low']:.2f} of its power below 120 Hz at the "
        f"worst noise draw; audible {info['aud']:.0f} ms; its loudest 50 ms {info['top_db']:+.1f} "
        f"dB re Ironwood's blow. Register {info['reg_rc']:.2f} against rune-crack, at most "
        f"{info['reg_row']:.2f} against the warhammer row's casts, {info['reg_death']:.2f} "
        f"against the death voice."], 10)
    c_sprout = _wrap([
        f'THE SPROUT -- "two quick woody cracks, 80ms each, a fifth apart" (v69 §7.2). {sname}, '
        f'of {len(SPROUT_CANDIDATES)} (`ironwood_voice_lab.py`). `tickTree` plays it on the frame the blade set '
        f'appears, when the two new boughs are live. A then E (the score\'s i and v), rising, the '
        f'second crack 90 ms after the first: pitches {info["sp_f"]} Hz, each crack audible '
        f'{info["sp_aud"]} ms, loudest 50 ms {info["sp_db"]:+.1f} dB re the blow and '
        f'{info["sp_wall"]:+.1f} dB re the wall tick; register at most {info["sp_reg"]:.2f} '
        f'against the blow, the bough, the cast and rune-crack.'], 10)
    c_wither = _wrap([
        f'THE WITHER -- "a dry creak falling in pitch, 0.4s, quiet" (v69 §7.2). {wname}, of {len(WITHER_CANDIDATES)} '
        f'(`ironwood_voice_lab.py`): a pulse train slowing from 55 to 24 a second, its pitch '
        f'falling {info["w_fall"]:+.0f} cents, audible {info["w_aud"]:.0f} ms, '
        f'{info["w_low"]:.2f} of its power below 120 Hz (dry, where the cast is deep), '
        f'{info["w_db"]:+.1f} dB under the cast\'s top. `tickTree` plays it only when the window '
        f'closes by its clock with the caster alive, never on a death.'], 10)
    return (f'        }} else if (w === "ironwood"){{                   // the hammer takes root\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["kc"])}\n'
            f'        }} else if (w === "ironwood-sprout"){{            // two boughs break out\n'
            f'{c_sprout}\n{sprout_body(S_["sp"], S_["g"], S_["D"])}\n'
            f'        }} else if (w === "ironwood-wither"){{            // and the tree lets go\n'
            f'{c_wither}\n{wither_body(W_["sp"], W_["g"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# events, each rendered at its own time on ONE synth:
#   ["play", at, kind, p]    the page's own SFX.play
#   ["body", at, src, p]     a candidate: its arm text run as (t, p) on the synth
#   ["arm",  at, kind, p]    the PATCHED play (the Sfx rows applied)
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
  const oc = new OC(1, Math.round(sr * secs), sr);
  let cursor = 0;
  const S = Object.create(proto);
  S.ok = true; S.on = true;
  S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
    const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = mkNoise(oc);
  const log = { burst: [], sweep: [], tone: 0 };
  S._burst = function(t, o, d){ log.burst.push(o.dur); return proto._burst.call(this, t, o, d); };
  S._sweep = function(t, o, d){ log.sweep.push(o.dur); return proto._sweep.call(this, t, o, d); };
  S._tone  = function(t, o, d){ log.tone++; return proto._tone.call(this, t, o, d); };
  const fns = new Map(), calls = [];
  for (const e of evs){
    cursor = e[1];
    const before = log.tone + log.burst.length + log.sweep.length;
    if (e[0] === "play") S.play(e[2], e[3]);
    else if (e[0] === "arm") patched.call(S, e[2], e[3]);
    else if (e[0] === "body"){
      if (!fns.has(e[2])) fns.set(e[2], (0, eval)("(function(t, p){\n" + e[2] + "\n})"));
      fns.get(e[2]).call(S, e[1], e[3] || {});
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
  for (const [k, kind, p] of [["cast", "ult", { w: "ironwood" }], ["sprout", "ult", { w: "ironwood-sprout" }],
                              ["wither", "ult", { w: "ironwood-wither" }],
                              ["bough", "hit", { dmg: 9, crit: false, bough: 0.38 }],
                              ["hit", "hit", { dmg: 24, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickTree and resolveHit rows, applied to the real prototype and run beside
# the original; the survey of Canopy's windows comes out of the same runs.
WIRE_JS = r"""([seeds, treeRows, rhRow]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const origT = P.tickTree, origH = P.resolveHit;
  let srcT = origT.toString();
  for (const [anc, code] of treeRows){
    const at = srcT.split(anc).length - 1;
    if (at !== 1) return { err: `a tickTree anchor occurs ${at} times in tickTree()` };
    srcT = srcT.replace(anc, () => code);
  }
  let srcH = origH.toString();
  { const at = srcH.split(rhRow[0]).length - 1;
    if (at !== 1) return { err: `the resolveHit anchor occurs ${at} times in resolveHit()` };
    srcH = srcH.replace(rhRow[0], () => rhRow[1]); }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patT = (0, eval)("(function " + srcT + ")"), patH = (0, eval)("(function " + srcH + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "ironwood");
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, "ironwood", sd) : new AC.Match("ironwood", fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], hits = []; let step = 0, inTree = 0, rh = null;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      if (kind === "ult" && p && typeof p.w === "string" && p.w.startsWith("ironwood"))
        calls.push({ step, t: m.t, k: p.w, inTree: !!inTree });
      if (kind === "hit" && p){
        /* THE BLOW'S OWN VOICE is the one `resolveHit` plays itself. A ward that
           shatters under the blow plays its own `hit` from `shatter`, inside
           resolveHit's call (Lightkeeper, Farwarden): not a blow, never a bough. */
        const caller = rh ? ((new Error()).stack.split("\n")[2] || "") : "";
        const own = !!rh && /resolveHit/.test(caller);
        hits.push({ step, t: m.t, dmg: p.dmg, crit: !!p.crit, bough: p.bough === undefined ? null : p.bough,
                    rh: !!rh, own, mine: rh === f, tree: own && !!rh.ultTree,
                    wd: own && rh.ultTree ? rh.w.ult.winDmg : null });
      }
      if (kind === "death") calls.push({ step, t: m.t, k: "death", inTree: !!inTree });
      return op.call(this, kind, p); };
    const implT = wire ? patT : origT, implH = wire ? patH : origH;
    P.tickTree = function(dt){ inTree++; try { return implT.call(this, dt); } finally { inTree--; } };
    P.resolveHit = function(...args){ const prev = rh; rh = args[0];
      try { return implH.apply(this, args); } finally { rh = prev; } };
    const wins = []; let prevZ = null, prevBS = null, W = null, n = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const Z = f.ultTree;
        if (Z && Z !== prevZ){ if (W && !W.end && prevZ){ W.end = "recast"; W.endStep = step; }
                               W = { cast: m.t, castStep: step, sproutStep: null, end: null, endStep: null };
                               wins.push(W); }
        if (W && f.bladeSet && !prevBS) W.sproutStep = step;
        if (!Z && prevZ){ W.end = (f.alive && prevZ.t >= prevZ.dur) ? "clock" : "death";
                          W.endStep = step; W.close = m.t; }
        prevZ = Z; prevBS = f.bladeSet;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickTree = origT; P.resolveHit = origH; if (had) S.play = op; else delete S.play; }
    const T = f.treeTally || {};
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.winner ? m.winner.w.id : null, T]),
             calls, hits, wins, winDmg: f.w.ult.winDmg };
  };
  let fights = 0, same = 0, hitSeqSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, sprouts = 0, sproutV = 0, withers = 0, boughV = 0, boughWin = 0, hammerOut = 0, foeHits = 0,
      wardHits = 0;
  const pick = [], deathGap = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    const strip = (h) => JSON.stringify(h.map(x => [x.step, x.dmg, x.crit, x.mine]));
    if (strip(A.hits) === strip(B.hits)) hitSeqSame++;
    if (A.calls.some(c => c.k.startsWith("ironwood-"))) bad.push([fid, sd, "the UNPATCHED run played a Canopy voice"]);
    if (A.hits.some(h => h.bough !== null)) bad.push([fid, sd, "the UNPATCHED run played a bough"]);
    const castV = B.calls.filter(c => c.k === "ironwood");
    if (castV.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", castV.length, B.wins.length]);
    for (const c of B.calls) if (c.k.startsWith("ironwood-") && !c.inTree) bad.push([fid, sd, "a Canopy voice outside tickTree", c.k]);
    for (const h of B.hits){
      if (h.tree){ boughV++; if (h.bough !== h.wd) bad.push([fid, sd, "a tree blow without bough", h.bough]); }
      else if (h.bough !== null) bad.push([fid, sd, "a bough on a non-tree blow", h.mine, h.own]);
      else if (h.mine && h.own) hammerOut++;
      else if (h.own) foeHits++;
      else if (h.rh) wardHits++;
    }
    const sp = B.calls.filter(c => c.k === "ironwood-sprout"), wv = B.calls.filter(c => c.k === "ironwood-wither");
    sproutV += sp.length; withers += wv.length;
    for (const W of B.wins){
      ends[W.end]++; casts++;
      const inW = (c) => c.step >= W.castStep && (W.endStep === null || c.step <= W.endStep);
      const s1 = sp.filter(inW);
      if (W.sproutStep !== null){
        sprouts++;
        if (s1.length !== 1 || s1[0].step !== W.sproutStep) bad.push([fid, sd, "sprout voices", s1.length, s1.length ? s1[0].step : null, W.sproutStep]);
      } else if (s1.length) bad.push([fid, sd, "a sprout voice with no sprout"]);
      const w1 = wv.filter(inW);
      if (W.end === "clock"){
        if (w1.length !== 1 || w1[0].step !== W.endStep) bad.push([fid, sd, "clock close withers", w1.length]);
      } else if (w1.length) bad.push([fid, sd, W.end + " window played a wither"]);
      const bw = B.hits.filter(h => h.mine && h.own && h.step >= W.castStep &&
                                    (W.endStep === null || h.step < W.endStep)).length;
      boughWin += bw;
      if (W.end === "death"){
        const dv = B.calls.find(c => c.k === "death" && c.step >= W.endStep);
        const lh = B.hits.filter(h => h.step <= W.endStep).pop();
        deathGap.push([dv ? dv.t - W.close : null, lh ? W.close - lh.t : null, lh ? lh.dmg : null, lh ? lh.crit : null]);
      }
      if (W.end === "clock" && W.sproutStep !== null)
        pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, blows: bw });
    }
  }
  return { fights, same, hitSeqSame, diff: diff.slice(0, 4), ends, casts, sprouts, sproutV, withers,
           boughV, boughWin, hammerOut, foeHits, wardHits, pick, deathGap, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, treeRows, rhRow]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const origT = P.tickTree, origH = P.resolveHit;
  let srcT = origT.toString(); for (const [anc, code] of treeRows) srcT = srcT.replace(anc, () => code);
  const srcH = origH.toString().replace(rhRow[0], () => rhRow[1]);
  const patT = (0, eval)("(function " + srcT + ")"), patH = (0, eval)("(function " + srcH + ")");
  const m = side ? new AC.Match(fid, "ironwood", sd) : new AC.Match("ironwood", fid, sd);
  const f = side ? m.b : m.a;
  const ev = []; let rh = null;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    /* the blow's OWN voice is the one resolveHit plays itself (a ward's shatter
       plays its own `hit` from inside the call: not a blow) */
    const own = kind === "hit" && !!rh && /resolveHit/.test((new Error()).stack.split("\n")[2] || "");
    const tag = (kind === "ult" && typeof q.w === "string" && q.w.startsWith("ironwood-")) ? q.w
              : (kind === "hit" && q.bough !== undefined) ? "bough"
              : (own && rh === f) ? "hammer" : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickTree = patT;
  P.resolveHit = function(...args){ const prev = rh; rh = args[0];
    try { return patH.apply(this, args); } finally { rh = prev; } };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickTree = origT; P.resolveHit = origH; if (had) S.play = op; else delete S.play; }
  return ev;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def low_share(x, fc=120.0):
    np = _np()
    y = x[int(T0 * SR):]
    P = np.abs(np.fft.rfft(y)) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float(P[fr < fc].sum() / P.sum())


def lowpass_fft(y, fc):
    np = _np()
    Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fr >= fc] = 0
    return np.fft.irfft(Y, len(y))


def thud_at(x):
    """ms after the event where the <120 Hz band's 5 ms RMS peaks."""
    np = _np()
    y = lowpass_fft(x[int(T0 * SR):], 120.0)
    e, c = env(y, 0.005, 0.001)
    return float(c[int(np.argmax(e))] * 1000)


def pulsed(x, a, b):
    """PULSED and RATE over [a, b] s after the event (see the docstring). A
    window whose high-passed RMS is more than 30 dB under the voice's own
    loudest 50 ms scores 0: a creak nobody can hear is not a creak (the first
    cut had no floor and read the THUD control's filter ringing, far down,
    as 0.99)."""
    np = _np()
    y = x[int(T0 * SR):]
    floor = float(env(y, 0.05)[0].max()) * 10 ** (-30 / 20)
    Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fr < 150] = 0
    h = np.fft.irfft(Y, len(y))
    H = int(0.001 * SR); n = len(h) // H
    e = np.sqrt((h[:n * H].reshape(n, H) ** 2).mean(axis=1))
    pk, lg = [], []
    for w0 in range(int(round(a * 1000)), int(round(b * 1000)) - 150 + 1, 25):
        seg = e[w0:w0 + 150]
        if math.sqrt(float((seg ** 2).mean())) < floor:
            pk.append(0.0)
            continue
        best, bl = -1.0, 0
        for L in range(12, 61):
            u, v = seg[:-L], seg[L:]
            u = u - u.mean(); v = v - v.mean()
            den = math.sqrt(float((u * u).sum() * (v * v).sum()))
            r = float((u * v).sum() / den) if den > 0 else 0.0
            if r > best:
                best, bl = r, L
        pk.append(best); lg.append(bl)
    if not pk:
        return 0.0, 0.0
    return float(np.median(pk)), (1000.0 / float(np.median(lg)) if lg else 0.0)


def centroid(x, a, b, lo=150.0, hi=6000.0):
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    P = np.abs(np.fft.rfft(seg, 1 << 15)) ** 2; fr = np.fft.rfftfreq(1 << 15, 1 / SR)
    m = (fr >= lo) & (fr <= hi)
    return float((P[m] * fr[m]).sum() / P[m].sum())


def avgspec(xs, lo_f=500.0, hi_f=8000.0, secs=0.4):
    """The power spectra of a voice's noise draws AVERAGED, each point the
    mean power in a 1/12-octave window, on a 1/96-octave grid, in dB."""
    np = _np()
    NF = 1 << 17
    fr = np.fft.rfftfreq(NF, 1 / SR)
    P = 0.0
    for x in xs:
        y = x[int(T0 * SR):int((T0 + secs) * SR)]
        P = P + np.abs(np.fft.rfft(y, NF)) ** 2
    cs = np.concatenate([[0.0], np.cumsum(P)])
    grid = lo_f * 2 ** (np.arange(0, 96 * math.log2(hi_f / lo_f) + 1) / 96)
    lo = np.searchsorted(fr, grid * 2 ** (-1 / 24)); hi = np.searchsorted(fr, grid * 2 ** (1 / 24))
    out = (cs[hi] - cs[lo]) / np.maximum(hi - lo, 1)
    return 10 * np.log10(out + out.max() * 1e-9)


def crack_shift(xa, xb):
    """CRACK: cents that voice a's noise crack sits from voice b's -- the lag
    (12.5 c steps, parabolic) that best correlates their averaged spectra
    between 500 Hz and 8 kHz, where the strike's crack lives and its sine
    body (under 200 Hz) does not. Negative: a is lower."""
    np = _np()
    A, B = avgspec(xa), avgspec(xb)
    S = list(range(-160, 81))
    best = []
    for s_ in S:
        if s_ < 0:
            u, v = A[:s_], B[-s_:]
        elif s_ > 0:
            u, v = A[s_:], B[:-s_]
        else:
            u, v = A, B
        best.append(float(np.corrcoef(u, v)[0, 1]))
    i = int(np.argmax(best)); d = 0.0
    if 0 < i < len(best) - 1:
        y0, y1, y2 = best[i - 1], best[i], best[i + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if den else 0.0
    return (S[i] + d) * 12.5


def inharm(x, a, b, f):
    """A crack's strongest spectral peak between 1.5x and 4x its note: its
    ratio to the note, its cents from the nearest whole multiple, and its
    level re the note's own peak (dB). A struck bar's modes are inharmonic
    (1 : 2.76 : 5.40); a plain tone's partials are whole multiples or
    nothing."""
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    note = float(X[(fr > f * 0.97) & (fr < f * 1.03)].max())
    m = np.nonzero((fr >= 1.5 * f) & (fr <= 4 * f))[0]
    i = int(m[np.argmax(X[m])])
    fp = float(fr[i]); r = fp / f; k = max(1, round(r))
    return r, abs(cents(fp, k * f)), db(float(X[i]) / note)


def onsets2(x):
    """The two strongest onsets of a voice: peaks of its 1 ms RMS at least 40
    ms apart, in time order, ms after the event, with their levels."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + 0.5) * SR)]
    H = int(0.001 * SR); n = len(y) // H
    e = np.sqrt((y[:n * H].reshape(n, H) ** 2).mean(axis=1))
    pk = [i for i in range(1, n - 1) if e[i] >= e[i - 1] and e[i] >= e[i + 1]]
    pk.sort(key=lambda i: -e[i])
    got = []
    for i in pk:
        if all(abs(i - j) >= 40 for j in got):
            got.append(i)
        if len(got) == 2:
            break
    got.sort()
    return [(float(i), float(e[i] / e.max())) for i in got]


def mreg(xb, D_):
    _np()
    return float(sorted(cos(xb, d["bands"]) for d in D_)[len(D_) // 2])


# =============================================================== PICKING ===
FAILED: list = []

CAST_RULE = (
    "'0.5s': AUDIBLE 400-600 ms; 'share below 120 Hz >= 0.5': LOW >= 0.50 on the "
    "WORST of twelve noise draws; 'a ground-thud': the <120 Hz band peaks within "
    "60 ms of the cast (the frame the ball stops dead); 'a deep creak': PULSED "
    ">= 0.40 over the creak's span, the creak alone (its loudest 50 ms) no more "
    "than 12 dB under the thud alone (heard, not buried). Register against "
    "rune-crack, each of the warhammer row's casts, the death voice and the hit "
    "@ 24 each <= 0.80 (not the fallback it replaces, not a row-mate, not a "
    "death, not a blow). Level: TOP between 0.5x the hit @ 24's loudest 50 ms on "
    "its LOUDEST draw and 1.0x on its QUIETEST (heard like a blow, never over "
    "one). Tiebreak: the most distinct register (the highest of those six, to "
    "0.05), then the clearest creak (PULSED, to 0.05), then the fewest calls.")

SPROUT_RULE = (
    "'two ... cracks': two onsets, the second within 5 ms of 90 ms after the "
    "first and at least 0.3 of the first's level; '80ms each': each crack alone "
    "AUDIBLE 70-90 ms, struck (RISE <= 3 ms, its peak in the first 10 ms); 'a "
    "fifth apart': crack 2's pitch over crack 1's within 30 cents of 3:2; "
    "'woody': a struck bar, not a plain tone -- the FFT peak is the declared note "
    "(within 30 cents) AND the crack's strongest peak between 1.5x and 4x the "
    "note lies >= 60 cents from every whole multiple and within 20 dB of the "
    "note; "
    "heard: loudest 50 ms between 2x the wall tick's (loudest draw) and 0.7x the "
    "hit @ 24's (quietest draw), and crack 1's third-octave >= 2x the score's "
    "p90 there. Register against the hit @ 24, the picked bough, the picked "
    "cast and rune-crack each <= 0.80. Tiebreak: the lowest worst register (to "
    "0.05), then the fewest calls.")

BOUGH_RULE = (
    "'pitched down a fourth': CRACK within 30 cents of -498 (x 0.75) AND BODY "
    "within 30 cents of -498, at the hammer's own blow; 'peak <= 0.6 of the "
    "hammer's': the PEAK RATIO <= 0.60 on every noise draw at jitter 0.85 / 1 / "
    "1.15 and on a crit; 'quieter' but a blow: RISE <= 3 ms, the peak in the "
    "first 15 ms, and its loudest 50 ms >= 2x the wall tick's on its loudest "
    "draw (heard over the commonest sound). Tiebreak: the highest ENV-CORR "
    "with the hammer's strike ('the hammer's own strike voice', to 0.01), then "
    "the fewest calls.")

WITHER_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms; 'falling in pitch': FALL "
    "(the spectral peak, 80 Hz-3 kHz, of the last 100 audible ms against the "
    "first) <= -400 cents; 'a creak': PULSED >= 0.40 over 20-380 ms; 'dry': LOW <= "
    "0.20 on the worst draw (not the cast's deep body, and no tail); 'quiet': "
    "the loudest 50 ms <= 0.5x the picked cast's and >= 2x the wall tick's on "
    "its loudest draw. Register against rune-crack, the hit @ 24, the picked "
    "bough and the picked sprout each <= 0.80. Tiebreak: the creak built as "
    "the picked cast's is (the rooting and the unrooting are one sound, run "
    "the other way), then the most distinct register (to 0.05), then the "
    "fewest calls.")


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
    if M["low_min"] < 0.50: why.append(f"low {M['low_min']:.2f} < 0.50")
    if M["thud_at"] > 60: why.append(f"the thud peaks at {M['thud_at']:.0f} ms, not <= 60")
    if M["pulsed"] < 0.40: why.append(f"pulsed {M['pulsed']:.2f} < 0.40")
    if M["creak_db"] < -12: why.append(f"creak {M['creak_db']:+.1f} dB re the thud, under -12")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def sprout_why(M, lev):
    why = []
    o = M["on"]
    if len(o) < 2: why.append("one onset")
    else:
        if abs(o[1][0] - o[0][0] - SPROUT_GAP * 1000) > 5: why.append(f"onsets {o[1][0] - o[0][0]:.0f} ms apart")
        if o[1][1] < 0.3: why.append(f"second crack at {o[1][1]:.2f} of the first")
    for j, C in enumerate(M["cracks"]):
        if not 70 <= C["aud"] <= 90: why.append(f"crack {j + 1} audible {C['aud']:.0f} ms")
        if C["rise"] > 3: why.append(f"crack {j + 1} rise {C['rise']:.0f} ms")
        if C["pk_ms"] > 10: why.append(f"crack {j + 1} peaks at {C['pk_ms']:.0f} ms")
        if abs(C["c_note"]) > 30: why.append(f"crack {j + 1} {C['c_note']:+.0f} c off its note")
        if C["inh_c"] < 60 or C["inh_db"] < -20:
            why.append(f"crack {j + 1} not woody: its partial at {C['inh_r']:.2f}x is {C['inh_c']:.0f} c "
                       f"from a whole multiple, {C['inh_db']:+.0f} dB")
    if abs(M["c_fifth"]) > 30: why.append(f"the fifth {M['c_fifth']:+.0f} c off 3:2")
    if M["top_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["inb"] < lev["inb"]: why.append(f"in-band {M['inb']:.4f} < {lev['inb']:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def bough_why(M, lev):
    why = []
    if abs(M["shift"] + 498) > 30: why.append(f"crack {M['shift']:+.0f} c, not -498 +/- 30")
    if abs(M["body"] + 498) > 30: why.append(f"body {M['body']:+.0f} c, not -498 +/- 30")
    if M["pk_max"] > 0.60: why.append(f"peak ratio {M['pk_max']:.2f} > 0.60 (worst)")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 15: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    return why


def wither_why(M, lev):
    why = []
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["gone"] > 470: why.append(f"gone at {M['gone']:.0f} ms")
    if M["fall"] > -400: why.append(f"fall {M['fall']:+.0f} c, not <= -400")
    if M["pulsed"] < 0.40: why.append(f"pulsed {M['pulsed']:.2f} < 0.40")
    if M["low_max"] > 0.20: why.append(f"low {M['low_max']:.2f} > 0.20 (not dry)")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-canopy-w38.html")
    ap.add_argument("--out", default="../05-reference/v99")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=99601)
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the five checked rows here")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "sprout": SPROUT_RULE, "bough": BOUGH_RULE,
                                      "wither": WITHER_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("Sfx hit", HIT_ANCHOR), ("tickTree sprout", SPROUT_ANCHOR),
                    ("tickTree wither", WITHER_ANCHOR), ("resolveHit", RH_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if "ironwood-sprout" in html or "p.bough" in html:
        raise SystemExit(f"{gp.name} already carries Canopy's voices -- run on stage 5")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nCANOPY -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    specs_cast = [c[1] for c in CAST_CANDIDATES]
    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua

        def R(evs, secs=3.0, seed=None, rows=None):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            # the toolkit's length traps (CLAUDE.md 4.5) are refused in the NEW
            # voices only; the old ones (the death voice's 0.6 s burst) are controls
            new = any(e[0] == "body" or (e[0] == "arm" and (
                (e[2] == "ult" and str(e[3].get("w", "")).startswith("ironwood")) or
                e[3].get("bough") is not None)) for e in evs)
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
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        ROW = ("grudgebearer", "bulwarden", "shroudmaul", "ravelbone")
        for name, ev in ([("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                          ("BAR", ["play", T0, "ult", {"w": "axiom"}]),
                          ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                          ("hit@24", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                          ("hit@9.12", ["play", T0, "hit", {"dmg": BLADE * WIN, "crit": False}]),
                          ("wall", ["play", T0, "wall", {}]),
                          ("death", ["play", T0, "death", {}]),
                          ("ironwood now", ["play", T0, "ult", {"w": "ironwood"}]),
                          ("censer", ["play", T0, "ult", {"w": "censer"}])] +
                         [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in ROW]):
            x, _ = R([ev])
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
        fall = {k: float(np.abs(ctl[k]["x"] - rcx).max()) for k in ("ironwood now", "censer")}
        print("  ARE rune-crack today (max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if max(fall.values()) > 1e-6:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        # the noise draws
        HD, WD, RCD, DD = [], [], [], []
        ROWD = {r_: [] for r_ in ROW}
        for sd in NOISE_SEEDS:
            HD.append(basic(R([["play", T0, "hit", {"dmg": BLADE, "crit": False}]], seed=sd)[0]))
            WD.append(basic(R([["play", T0, "wall", {}]], seed=sd)[0]))
            RCD.append(basic(R([["play", T0, "ult", {"w": "spellbreaker"}]], seed=sd)[0]))
            DD.append(basic(R([["play", T0, "death", {}]], seed=sd)[0]))
            for r_ in ROW:
                ROWD[r_].append(basic(R([["play", T0, "ult", {"w": r_}]], seed=sd)[0]))
        h_lo, h_hi = min(m["top"] for m in HD), max(m["top"] for m in HD)
        w_hi = max(m["top"] for m in WD)
        print(f"  the hit @ 24 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m['peak'] for m in HD):.3f}-{max(m['peak'] for m in HD):.3f};  the wall tick: "
              f"{min(m['top'] for m in WD):.4f}-{w_hi:.4f}")
        pairs = [(ROW[i], ROW[j]) for i in range(4) for j in range(i + 1, 4)]
        pr = {f"{p_}/{q_}": mreg(ROWD[p_][0]["bands"], ROWD[q_]) for p_, q_ in pairs}
        print("  the warhammer row's own registers: " + ", ".join(f"{k} {v:.2f}" for k, v in pr.items()) +
              f"  (median {float(np.median(list(pr.values()))):.2f}; the gate is 0.80)")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]

        def bedp90(f):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + 0.25)
                                        for i in range(0, len(bseg) - 12000, 2400)], 90))
        rec["levels"] = dict(hit24=[h_lo, h_hi], wall_hi=w_hi, row_regs=pr)
        wav("ironwood-ctl-runecrack.wav", rcx)
        wav("ironwood-ctl-hit24.wav", ctl["hit@24"]["x"])
        wav("ironwood-ctl-hit9.wav", ctl["hit@9.12"]["x"])
        wav("ironwood-ctl-grudgebearer.wav", ctl["grudgebearer"]["x"])
        wav("ironwood-ctl-death.wav", ctl["death"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_top = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a deep creak and a ground-thud, 0.5s, share below 120 Hz >= 0.5'. Level-matched: "
              f"LOW {LOW_TARGET:g} on render.py's draw, TOP {tgt_top:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f})")

        def cx(sp, g, kc, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kc, part), {}]], seed=seed)

        def calib_cast(sp):
            g, kc = 0.3, 0.3
            for _ in range(3):
                lo_, hi_ = math.log(1e-3), math.log(1e3)
                for _ in range(10):
                    mid = 0.5 * (lo_ + hi_)
                    s_ = low_share(cx(sp, g, math.exp(mid))[0])
                    if s_ > LOW_TARGET: lo_ = mid
                    else: hi_ = mid
                kc = math.exp(0.5 * (lo_ + hi_))
                M = basic(cx(sp, g, kc)[0])
                g = g * tgt_top / M["top"]
            return float(f"{g:.4g}"), float(f"{kc:.4g}")

        def cast_measure(sp, g, kc, part="both"):
            x, calls = cx(sp, g, kc, part)
            x2, _ = cx(sp, g, kc, part)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, kc=kc)
            draws = [cx(sp, g, kc, part, seed=sd)[0] for sd in NOISE_SEEDS]
            M["low"] = low_share(x); M["low_min"] = min(low_share(d_) for d_ in draws)
            M["thud_at"] = thud_at(x)
            late = sp["order"] == "late"
            M["pulsed"], M["rate"] = pulsed(x, 0.02 if late else 0.05, 0.36 if late else 0.48)
            DB = [dict(bands=bands(d_[int(T0 * SR):])) for d_ in draws]
            M["DB"] = [d_["bands"] for d_ in DB]
            M["regs"] = {"rune-crack": float(np.median([cos(DB[i]["bands"], RCD[i]["bands"]) for i in range(12)])),
                         "death": float(np.median([cos(DB[i]["bands"], DD[i]["bands"]) for i in range(12)])),
                         "hit@24": float(np.median([cos(DB[i]["bands"], HD[i]["bands"]) for i in range(12)]))}
            for r_ in ROW:
                M["regs"][r_] = float(np.median([cos(DB[i]["bands"], ROWD[r_][i]["bands"]) for i in range(12)]))
            if part == "both":
                tx = basic(cx(sp, g, kc, "thud")[0]); cr = basic(cx(sp, g, kc, "creak")[0])
                M["creak_db"] = db(cr["top"] / tx["top"])
            else:
                M["creak_db"] = -99.0 if part == "thud" else 0.0
            return M

        H_ = (f"  {'cand':<9}{'g':>8}{'kc':>8}{'calls':>6}{'top':>8}{'aud':>6}{'low':>6}{'lowW':>6}{'thud@':>6}"
              f"{'pulse':>6}{'rate':>6}{'crk dB':>7}{'rc':>5}{'grud':>5}{'bulw':>5}{'shrd':>5}{'ravl':>5}"
              f"{'death':>6}{'hit':>5}")
        print(H_)

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>8.4g}{M['kc']:>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud']:>6.0f}"
                  f"{M['low']:>6.2f}{M['low_min']:>6.2f}{M['thud_at']:>6.0f}{M['pulsed']:>6.2f}{M['rate']:>6.0f}"
                  f"{M['creak_db']:>7.1f}{r_['rune-crack']:>5.2f}{r_['grudgebearer']:>5.2f}{r_['bulwarden']:>5.2f}"
                  f"{r_['shroudmaul']:>5.2f}{r_['ravelbone']:>5.2f}{r_['death']:>6.2f}{r_['hit@24']:>5.2f}")

        rows_c = []
        for i, (name, sp, blurb) in enumerate(CAST_CANDIDATES):
            g, kc = calib_cast(sp)
            M = cast_measure(sp, g, kc); M.update(name=name, sp=sp)
            M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"ironwood-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for part, name in (("thud", "0 THUD"), ("creak", "0 CREAK")):
            M = cast_measure(rows_c[0]["sp"], rows_c[0]["g"], rows_c[0]["kc"], part)
            M.update(name=name, sp=rows_c[0]["sp"]); M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
            wav(f"ironwood-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 THUD    the thud alone (no creak) -- a control\n"
              "    0 CREAK   GRAIN's creak alone (no thud) -- a control")
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
                                                          -round(rows_c[i]["pulsed"] / 0.05), rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, kc {C_['kc']}, {C_['calls']} synth calls; TOP {C_['top']:.4f} = "
              f"{db(C_['top'] / h_lo):+.1f} dB re the hit @ 24 (quietest draw), {db(C_['top'] / w_hi):+.1f} dB re "
              f"the wall; LOW {C_['low_min']:.2f} worst draw; creak {C_['creak_db']:+.1f} dB re the thud")

        # ---- THE BOUGH -----------------------------------------------------
        print(f"\nBOUGH -- 'the hammer's own strike voice, pitched down a fourth and quieter (peak <= 0.6 of "
              f"the hammer's)'. Level-matched: the WORST peak ratio (12 draws x jitter x crit) {BOUGH_WORST:g}")
        JIT = [0.85, 1.0, 1.15]

        def dealt(j, crit, scale):
            v = BLADE * scale * j * (2.1 if crit else 1.0)
            return float(math.floor(v + 0.5))          # Math.round for positives

        def bx(sp, v, j=1.0, crit=False, seed=None):
            p = {"dmg": dealt(j, crit, WIN), "crit": crit, "bough": WIN}
            return R([["body", T0, bough_body(sp, v), p]], seed=seed)

        def hx(j=1.0, crit=False, seed=None, scale=1.0):
            return R([["play", T0, "hit", {"dmg": dealt(j, crit, scale), "crit": crit}]], seed=seed)[0]

        hit_cache = {}

        def hammer(j, crit, sd):
            k = (j, crit, sd)
            if k not in hit_cache:
                hit_cache[k] = hx(j, crit, sd)
            return hit_cache[k]

        def worst_ratio(sp, v):
            w_ = 0.0
            for j in JIT:
                for crit in (False, True):
                    for sd in (NOISE_SEEDS if (j == 1.0 and not crit) else NOISE_SEEDS[:4]):
                        w_ = max(w_, float(np.abs(bx(sp, v, j, crit, sd)[0]).max()) /
                                 float(np.abs(hammer(j, crit, sd)).max()))
            return w_

        def calib_bough(sp):
            v = 0.3
            for _ in range(4):
                v = float(f"{v * BOUGH_WORST / worst_ratio(sp, v):.4g}")
            return v

        def bough_measure(x, calls, draws_fn, name):
            M = basic(x); M["x"] = x; M["calls"] = calls
            href = hammer(1.0, False, None)
            M["shift"] = crack_shift([draws_fn(1.0, False, sd) for sd in NOISE_SEEDS],
                                     [hammer(1.0, False, sd) for sd in NOISE_SEEDS])
            M["body"] = cents(pitch(x, T0, T0 + 0.03, lo=25, hi=400), pitch(href, T0, T0 + 0.03, lo=25, hi=400))
            ratios, base, tops = [], [], []
            for j in JIT:
                for crit in (False, True):
                    for sd in (NOISE_SEEDS if (j == 1.0 and not crit) else NOISE_SEEDS[:4]):
                        xb = draws_fn(j, crit, sd)
                        r_ = float(np.abs(xb).max()) / float(np.abs(hammer(j, crit, sd)).max())
                        ratios.append(r_)
                        if j == 1.0 and not crit:
                            base.append(r_); tops.append(basic(xb)["top"])
            M["pk_med"] = float(np.median(base))
            M["pk_max"] = max(ratios)
            M["top_lo"] = min(tops) if tops else M["top"]
            M["corr"] = env_corr(x, href)
            M["name"] = name
            return M

        rows_b = []
        print(f"  {'cand':<9}{'v':>8}{'calls':>6}{'crack c':>8}{'body c':>7}{'pk med':>7}{'pk max':>7}{'rise':>5}"
              f"{'pk@':>5}{'aud':>5}{'top lo':>8}{'wall dB':>8}{'corr':>6}")

        def bough_line(M):
            print(f"  {M['name']:<9}{M.get('v', 0):>8.4g}{M['calls']:>6d}{M['shift']:>8.0f}{M['body']:>7.0f}"
                  f"{M['pk_med']:>7.2f}{M['pk_max']:>7.2f}{M['rise']:>5.0f}{M['pk_ms']:>5.0f}{M['aud']:>5.0f}"
                  f"{M['top_lo']:>8.4f}{db(M['top_lo'] / w_hi):>8.1f}{M['corr']:>6.2f}")

        lev_b = dict(lo=2 * w_hi)
        for i, (name, sp, blurb) in enumerate(BOUGH_CANDIDATES):
            v = calib_bough(sp)
            x, calls = bx(sp, v)
            x2, _ = bx(sp, v)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"bough {name} does not reproduce")
            M = bough_measure(x, calls[0], lambda j, c, sd, sp=sp, v=v: bx(sp, v, j, c, sd)[0], name)
            M.update(sp=sp, v=v); M["why"] = bough_why(M, lev_b)
            rows_b.append(M); bough_line(M)
            wav(f"ironwood-bough-{name.replace(' ', '-').lower()}.wav", x)
        ctlb = []
        for name, scale in (("0 PLAIN", WIN), ("0 HAMMER", 1.0)):
            x = hx(1.0, False, None, scale=scale)
            M = bough_measure(x, 3, lambda j, c, sd, scale=scale: hx(j, c, sd, scale=scale), name)
            M["v"] = 0; M["why"] = bough_why(M, lev_b)
            ctlb.append(M); bough_line(M)
        for (name, _sp, blurb) in BOUGH_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 PLAIN   the hit at the bough's 9 (0.38 x 24): what a bough blow plays TODAY -- a control\n"
              "    0 HAMMER  the hit at 24 itself -- a control")
        print(f"  gates: loudest 50 ms >= {lev_b['lo']:.4f}")
        print(f"  RULE  {BOUGH_RULE}")
        for M in rows_b:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctlb:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_b, "bough")
        bi = fb if ok is None else min(ok, key=lambda i: (-round(rows_b[i]["corr"], 2), rows_b[i]["calls"]))
        B_ = rows_b[bi]
        print(f"  PICK  {B_['name']}  v {B_['v']}; crack {B_['shift']:+.0f} c, body {B_['body']:+.0f} c; peak "
              f"{B_['pk_med']:.2f} of the hammer's (worst {B_['pk_max']:.2f}); loudest 50 ms "
              f"{db(B_['top'] / h_lo):+.1f} dB re the hit @ 24, {db(B_['top_lo'] / w_hi):+.1f} dB re the wall")

        # ---- THE SPROUT ----------------------------------------------------
        lev_s = dict(lo=2 * w_hi, hi=0.7 * h_lo)
        tgt_s = math.sqrt(lev_s["lo"] * lev_s["hi"])
        print(f"\nSPROUT -- 'two quick woody cracks, 80ms each, a fifth apart'. Level-matched: loudest 50 ms "
              f"{tgt_s:.4f} (the centre of {lev_s['lo']:.4f}-{lev_s['hi']:.4f}), crack 1 audible 80 ms")

        def sx(sp, g, D, only=None, seed=None):
            return R([["body", T0, sprout_body(sp, g, D, only), {}]], seed=seed)

        def calib_sprout(sp):
            g, D = 0.1, 0.1
            for _ in range(5):
                D = D * 80.0 / basic(sx(sp, g, D, only=0)[0])["aud"]
                D = float(f"{D:.3g}")
                g = g * tgt_s / basic(sx(sp, g, D)[0])["top"]
            return float(f"{g:.4g}"), round(D, 3)

        BX = B_["x"]
        BDB = [bands(bx(B_["sp"], B_["v"], 1.0, False, sd)[0][int(T0 * SR):]) for sd in NOISE_SEEDS]
        rows_s = []
        print(f"  {'cand':<9}{'g':>8}{'D':>7}{'calls':>6}{'onsets ms':>12}{'2nd':>5}{'aud1':>5}{'aud2':>5}"
              f"{'f1':>7}{'f2':>7}{'5th c':>6}{'inh x/dB':>10}{'top':>15}{'inb':>8}{'hit':>5}{'bgh':>5}{'cast':>5}{'rc':>5}")
        for i, (name, sp, blurb) in enumerate(SPROUT_CANDIDATES):
            g, D = calib_sprout(sp)
            x, calls = sx(sp, g, D)
            x2, _ = sx(sp, g, D)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"sprout {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, D=D, name=name, sp=sp)
            M["on"] = onsets2(x)
            f1 = sprout_f(sp)
            cracks = []
            for j, fn in ((0, f1), (1, f1 * 1.5)):
                xc = sx(sp, g, D, only=j)[0]
                # crack j alone was scheduled at its own offset: re-time to its onset
                off = SPROUT_GAP if j else 0.0
                yc = np.concatenate([xc[:int(T0 * SR)], xc[int((T0 + off) * SR):]])
                C = basic(yc)
                C["pitch"] = pitch(yc, T0, T0 + 0.06, lo=200, hi=8000)
                C["c_note"] = cents(C["pitch"], fn)
                C["cen_ratio"] = centroid(yc, T0, T0 + 0.08) / C["pitch"]
                C["inh_r"], C["inh_c"], C["inh_db"] = inharm(yc, T0, T0 + 0.06, C["pitch"])
                cracks.append(C)
            M["cracks"] = cracks
            M["c_fifth"] = cents(cracks[1]["pitch"] / cracks[0]["pitch"], 1.5)
            draws = [x] if sp["body"] in () else [sx(sp, g, D, seed=sd)[0] for sd in NOISE_SEEDS]
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws); M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            M["inb"] = band_rms(x, f1, T0, T0 + 0.06)
            M["inb_floor"] = 2 * bedp90(f1)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["regs"] = {"hit@24": float(np.median([cos(DB[k], HD[k]["bands"]) for k in range(12)])),
                         "bough": float(np.median([cos(DB[k], BDB[k]) for k in range(12)])),
                         "cast": float(np.median([cos(DB[k], C_["DB"][k]) for k in range(12)])),
                         "rune-crack": float(np.median([cos(DB[k], RCD[k]["bands"]) for k in range(12)]))}
            M["why"] = sprout_why(M, dict(lev_s, inb=M["inb_floor"]))
            rows_s.append(M)
            on = M["on"]
            ons = f"{on[0][0]:.0f}/{on[1][0]:.0f}" if len(on) > 1 else "one"
            print(f"  {name:<9}{g:>8.4g}{D:>7.3f}{M['calls']:>6d}{ons:>12}{(on[1][1] if len(on) > 1 else 0):>5.2f}"
                  f"{cracks[0]['aud']:>5.0f}{cracks[1]['aud']:>5.0f}{cracks[0]['pitch']:>7.0f}{cracks[1]['pitch']:>7.0f}"
                  f"{M['c_fifth']:>6.0f}{cracks[0]['inh_r']:>5.2f}/{cracks[0]['inh_db']:<+4.0f}{M['top_lo']:>8.4f}-{M['top_hi']:<6.4f}"
                  f"{M['inb']:>8.4f}{M['regs']['hit@24']:>5.2f}{M['regs']['bough']:>5.2f}{M['regs']['cast']:>5.2f}"
                  f"{M['regs']['rune-crack']:>5.2f}")
            wav(f"ironwood-sprout-{name.replace(' ', '-').lower()}.wav", x)
        for (name, _sp, blurb) in SPROUT_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print(f"  RULE  {SPROUT_RULE}")
        for M in rows_s:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        ok, fb = _gate(rows_s, "sprout")
        si = fb if ok is None else min(ok, key=lambda i: (round(max(rows_s[i]["regs"].values()) / 0.05),
                                                          rows_s[i]["calls"]))
        S_ = rows_s[si]
        print(f"  PICK  {S_['name']}  g {S_['g']}, D {S_['D']} s; loudest 50 ms {db(S_['top_hi'] / h_lo):+.1f} dB re "
              f"the hit @ 24, {db(S_['top_lo'] / w_hi):+.1f} dB re the wall")

        # ---- THE WITHER ----------------------------------------------------
        cast_top = C_["top"]
        lev_w = dict(hi=0.5 * cast_top, lo=2 * w_hi)
        tgt_w = cast_top * 10 ** (-WITHER_UNDER_DB / 20)
        print(f"\nWITHER -- 'a dry creak falling in pitch, 0.4s, quiet'. Level-matched {WITHER_UNDER_DB:g} dB under "
              f"the cast's top ({tgt_w:.4f})")

        def wx(sp, g, seed=None):
            return R([["body", T0, wither_body(sp, g), {}]], seed=seed)

        def calib_wither(sp):
            g = 0.1
            for _ in range(4):
                g = g * tgt_w / basic(wx(sp, g)[0])["top"]
            return float(f"{g:.4g}")

        SX = S_["x"]

        def wither_measure(x, calls, draws, name):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            a0 = T0 + M["a0"] / 1000; a1 = T0 + M["gone"] / 1000
            M["fall"] = cents(pitch(x, a1 - 0.1, a1, lo=80, hi=3000), pitch(x, a0, a0 + 0.1, lo=80, hi=3000))
            M["pulsed"], M["rate"] = pulsed(x, 0.02, 0.38)
            M["low_max"] = max(low_share(d_) for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["regs"] = {"rune-crack": float(np.median([cos(DB[k], RCD[k]["bands"]) for k in range(len(DB))])),
                         "hit@24": float(np.median([cos(DB[k], HD[k]["bands"]) for k in range(len(DB))])),
                         "bough": cos(DB[0], bands(BX[int(T0 * SR):])),
                         "sprout": cos(DB[0], bands(SX[int(T0 * SR):]))}
            M["reg_death"] = float(np.median([cos(DB[k], DD[k]["bands"]) for k in range(len(DB))]))
            return M

        rows_w = []
        print(f"  {'cand':<10}{'g':>8}{'calls':>6}{'top':>8}{'dB/cast':>8}{'aud':>5}{'gone':>6}{'fall c':>7}"
              f"{'pulse':>6}{'rate':>6}{'lowW':>6}{'rc':>5}{'hit':>5}{'bgh':>5}{'sprt':>5}")

        def wither_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M.get('g', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{db(M['top'] / cast_top):>8.1f}"
                  f"{M['aud']:>5.0f}{M['gone']:>6.0f}{M['fall']:>7.0f}{M['pulsed']:>6.2f}{M['rate']:>6.0f}"
                  f"{M['low_max']:>6.2f}{r_['rune-crack']:>5.2f}{r_['hit@24']:>5.2f}{r_['bough']:>5.2f}{r_['sprout']:>5.2f}")

        for i, (name, sp, blurb) in enumerate(WITHER_CANDIDATES):
            g = calib_wither(sp)
            x, calls = wx(sp, g)
            x2, _ = wx(sp, g)
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"wither {name} does not reproduce")
            draws = [wx(sp, g, seed=sd)[0] for sd in NOISE_SEEDS] if sp["pulse"] == "grain" else [x]
            M = wither_measure(x, calls[0], draws, name); M.update(g=g, sp=sp)
            M["why"] = wither_why(M, lev_w)
            rows_w.append(M); wither_line(M)
            wav(f"ironwood-wither-{name.replace(' ', '-').lower()}.wav", x)
        rsp = dict(WITHER_CANDIDATES[0][1], f0=WITHER_CANDIDATES[0][1]["f1"], f1=WITHER_CANDIDATES[0][1]["f0"])
        xr, cr_ = wx(rsp, rows_w[0]["g"])
        RI = wither_measure(xr, cr_[0], [wx(rsp, rows_w[0]["g"], seed=sd)[0] for sd in NOISE_SEEDS], "0 RISE")
        RI["g"] = rows_w[0]["g"]; RI["why"] = wither_why(RI, lev_w)
        gq = float(f"{C_['g'] * 10 ** (-WITHER_UNDER_DB / 20):.4g}")
        xq, cq_ = cx(C_["sp"], gq, C_["kc"])
        CQ = wither_measure(xq, cq_[0], [cx(C_["sp"], gq, C_["kc"], seed=sd)[0] for sd in NOISE_SEEDS], "0 CASTQ")
        CQ["g"] = gq; CQ["why"] = wither_why(CQ, lev_w)
        for M in (RI, CQ):
            wither_line(M)
        wav("ironwood-wither-0-rise.wav", xr)
        for (name, _sp, blurb) in WITHER_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 RISE    GRAIN's creak rising 420 -> 900 Hz -- a control\n"
              "    0 CASTQ   the picked cast at 9 dB under its top -- a control")
        print(f"  gates: top {lev_w['lo']:.4f}-{lev_w['hi']:.4f}")
        print(f"  RULE  {WITHER_RULE}")
        for M in rows_w:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in (RI, CQ):
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_w, "wither")
        wi = fb if ok is None else min(ok, key=lambda i: (0 if rows_w[i]["sp"]["pulse"] == C_["sp"]["creak"] else 1,
                                                          round(max(rows_w[i]["regs"].values()) / 0.05),
                                                          rows_w[i]["calls"]))
        W_ = rows_w[wi]
        print(f"  PICK  {W_['name']}  g {W_['g']}; {db(W_['top'] / cast_top):+.1f} dB re the cast's top, "
              f"{db(W_['top'] / h_lo):+.1f} re the hit @ 24, {db(W_['top'] / w_hi):+.1f} re the wall; fall "
              f"{W_['fall']:+.0f} c")

        # ---- THE SFX ROWS, GENERATED AND CHECKED -----------------------------
        info_h = dict(shift=B_["shift"], body=B_["body"], pk_med=B_["pk_med"], pk_max=B_["pk_max"],
                      wall_db=db(B_["top_lo"] / w_hi), corr=B_["corr"], plain_body=ctlb[0]["body"])
        hit_code = hit_row_code(B_, info_h)
        sp_f = "-".join(f"{c['pitch']:.0f}" for c in S_["cracks"])
        sp_aud = "/".join(f"{c['aud']:.0f}" for c in S_["cracks"])
        info_a = dict(low=C_["low_min"], aud=C_["aud"], top_db=db(C_["top"] / h_lo),
                      reg_rc=C_["regs"]["rune-crack"], reg_row=max(C_["regs"][r_] for r_ in ROW),
                      reg_death=C_["regs"]["death"], sp_f=sp_f, sp_aud=sp_aud,
                      sp_db=db(S_["top_hi"] / h_lo), sp_wall=db(S_["top_lo"] / w_hi),
                      sp_reg=max(S_["regs"].values()), w_fall=W_["fall"], w_aud=W_["aud"],
                      w_low=W_["low_max"], w_db=db(W_["top"] / cast_top))
        arms = arms_code(C_, S_, W_, info_a)
        _refuse(hit_code + arms, "Sfx rows")
        sfx_rows = [[HIT_ANCHOR, hit_code], [SFX_ANCHOR, arms]]
        print("\nTHE SFX ROWS, applied to Sfx.prototype.play's own source and rendered:")
        chk = []
        xa1, _ = R([["arm", T0, "ult", {"w": "ironwood"}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa1 - C_["x"]).max())))
        xs1, _ = R([["arm", T0, "ult", {"w": "ironwood-sprout"}]], rows=sfx_rows)
        chk.append(("sprout", float(np.abs(xs1 - S_["x"]).max())))
        xw1, _ = R([["arm", T0, "ult", {"w": "ironwood-wither"}]], rows=sfx_rows)
        chk.append(("wither", float(np.abs(xw1 - W_["x"]).max())))
        for j in JIT:
            for crit in (False, True):
                p = {"dmg": dealt(j, crit, WIN), "crit": crit, "bough": WIN}
                xb1, _ = R([["arm", T0, "hit", p]], rows=sfx_rows, seed=NOISE_SEEDS[3])
                xb2, _ = R([["body", T0, bough_body(B_["sp"], B_["v"]), p]], seed=NOISE_SEEDS[3])
                chk.append((f"bough j{j}{'c' if crit else ''}", float(np.abs(xb1 - xb2).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11.6, 24, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("seal", {}), ("nova", {"k": 1}),
                   ("hex-snap", {})]
        ids = [w_ for w_ in page.evaluate("() => AC.WEAPONS.map(w => w.id)") if w_ != "ironwood"]
        others += [("ult", {"w": w_}) for w_ in ids]
        same_ = []
        for kind, p in others:
            x1, _ = R([["play", T0, kind, p]]); x2, _ = R([["arm", T0, kind, p]], rows=sfx_rows)
            same_.append((kind + "/" + str(p.get("w", p.get("dmg", ""))) + ("!" if p.get("crit") else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, spark x3, wall, death, clank, seal, nova, hex-snap, the {len(ids)} other casts): "
              f"worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa1 - rcx).max())
        print(f"  ult/ironwood vs rune-crack after the rows: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > 1e-6 or worst[1] > 1e-6 or now_rc <= 1e-3:
            FAILED.append("sfx rows")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost)

        # ---- THE tickTree AND resolveHit ROWS ------------------------------
        tree_rows = [[SPROUT_ANCHOR, SPROUT_CODE], [WITHER_ANCHOR, WITHER_CODE]]
        rh_row = [RH_ANCHOR, RH_CODE]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickTree AND resolveHit ROWS, applied to the prototype's own sources, run beside the "
              "originals on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds, tree_rows, rh_row])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Ironwood both sides x every foe x seeds {seeds}): {WR['same']}/"
              f"{WR['fights']} identical (over, clock, both hp, both positions, winner, the whole treeTally); "
              f"the hit-voice sequence identical but for `bough` in {WR['hitSeqSame']}/{WR['fights']}")
        print(f"  windows {WR['ends']}: {WR['casts']} casts, {WR['sprouts']} sprouts -> {WR['sproutV']} sprout voices, "
              f"{WR['withers']} withers; {WR['boughV']} bough voices ({WR['boughWin']} tree blows), "
              f"{WR['hammerOut']} Ironwood blows outside at the hammer's voice, {WR['foeHits']} foe blows and "
              f"{WR['wardHits']} ward bursts (a shatter's own `hit`) untouched;  problems {WR['nbad']}")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["hitSeqSame"] != WR["fights"] or WR["nbad"] \
                or WR["withers"] != WR["ends"]["clock"] or WR["sproutV"] != WR["sprouts"] \
                or WR["boughV"] != WR["boughWin"] or WR["boughV"] == 0:
            FAILED.append("tickTree / resolveHit rows")
        WB = page.evaluate(WIRE_JS, [seeds, tree_rows, [RH_ANCHOR, RH_CODE_BAD]])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a bough blow): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "hitSeqSame", "ends", "casts", "sprouts", "sproutV",
                                          "withers", "boughV", "boughWin", "hammerOut", "foeHits", "wardHits",
                                          "nbad")}
        rec["wire"]["control_same"] = WB["same"]

        # ---- THE WITHER ON A DEATH ------------------------------------------
        dg = [d_ for d_ in WR["deathGap"] if d_[0] is not None and d_[1] is not None]
        print(f"\nTHE WITHER ON A DEATH -- {WR['ends']['death']} windows closed by the caster's death:")
        if dg:
            to_death = np.array([d_[0] for d_ in dg]); from_hit = np.array([d_[1] for d_ in dg])
            print(f"  the close comes {np.median(from_hit) * 1000:.0f} ms (median; p90 "
                  f"{np.percentile(from_hit, 90) * 1000:.0f}) after the killing blow's voice and "
                  f"{np.median(to_death) * 1000:.0f} ms (median; p10 {np.percentile(to_death, 10) * 1000:.0f}) "
                  f"before the death voice")
            kd = float(np.median([d_[2] for d_ in dg if d_[2] is not None]))
            th_ = float(np.median(from_hit)); td_ = float(np.median(to_death))
            evs = [["play", T0, "hit", {"dmg": kd, "crit": False}],
                   ["arm", T0 + th_, "ult", {"w": "ironwood-wither"}],
                   ["play", T0 + th_ + td_, "death", {}]]
            xm, _ = R(evs, rows=sfx_rows)
            xk, _ = R([evs[0], evs[2]], rows=sfx_rows)
            a0 = T0 + th_; a1 = a0 + 0.4
            fw = centroid(W_["x"], T0, T0 + 0.4)
            win_in = band_rms(W_["x"], fw, T0, T0 + 0.4)
            kill_in = band_rms(xk, fw, a0, a1)
            keep = db(band_rms(xm, fw, a0, a1) / max(kill_in, 1e-12))
            print(f"  rendered at those medians (the killing blow at its median {kd:.0f}, the wither, the death "
                  f"voice): the wither lifts its own third-octave ({fw:.0f} Hz) {keep:+.1f} dB over the kill's "
                  f"sounds, which stand {db(kill_in / win_in):+.1f} dB against the wither alone there -- it would "
                  f"NOT be buried, so this is a choice about the ending, not a masking limit")
            rec["death_close"] = dict(n=len(dg), from_hit=float(np.median(from_hit)), to_death=float(np.median(to_death)),
                                      keep_db=keep, kill_vs_wither_db=db(kill_in / win_in))
            wav("ironwood-wither-on-death.wav", xm)
        else:
            print("  none measured")
        print(f"  DECIDED: clock close with the caster alive only (Zenith's and Daybreak's rule). A caster's death "
              f"ends the fight on the close's own frame (the death voice a median 0 ms later), exactly as the "
              f"{WR['ends']['over']} windows the foe's death ended were never closed at all: 'never once the fight "
              f"is over' leaves BOTH endings to the death voice.")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["blows"], w["foe"], w["seed"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], tree_rows, rh_row])
            assert not errors, errors[:3]
            c0 = w_["cast"]; c1 = w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 2.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs
                       if e[3] not in ("ironwood-sprout", "ironwood-wither")]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd
            sp_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "ironwood-sprout"]
            wi_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "ironwood-wither"]
            f1 = sprout_f(S_["sp"])
            sp_over = [db(band_rms(xw, f1, t_, t_ + 0.06) / max(band_rms(xo, f1, t_, t_ + 0.06), 1e-12))
                       for t_ in sp_t]
            fw = centroid(W_["x"], T0, T0 + 0.4)
            wi_over = [db(band_rms(xw, fw, t_, t_ + 0.4) / max(band_rms(xo, fw, t_, t_ + 0.4), 1e-12)) for t_ in wi_t]
            # every blow Ironwood lands in the WHOLE fight, rendered alone at the damage it dealt
            # (acts, statuses, jitter and crits included) through the patched play
            pk = lambda e: float(np.abs(R([["arm", T0, "hit", e[2]]], rows=sfx_rows)[0]).max())  # noqa: E731
            bp = [pk(e) for e in EV if e[3] == "bough" and not e[2].get("crit")]
            hp = [pk(e) for e in EV if e[3] == "hammer" and not e[2].get("crit")]
            bc = [pk(e) for e in EV if e[3] == "bough" and e[2].get("crit")]
            hc = [pk(e) for e in EV if e[3] == "hammer" and e[2].get("crit")]
            nb_ = sum(1 for e in EV if e[3] == "bough")
            print(f"\nIN A REAL WINDOW -- ironwood v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {w_['blows']} bough blows; the fight's own "
                  f"sounds and the score, with and without the sprout and the wither")
            print(f"  the sprout over the fight in its own third-octave: " + " ".join(f"{v:+.1f}" for v in sp_over) +
                  " dB;  the wither: " + " ".join(f"{v:+.1f}" for v in wi_over) + " dB")
            if bp:
                print(f"  every blow of the fight rendered alone at the damage it dealt ({nb_} bough, "
                      f"{len(hp) + len(hc)} hammer): plain blows -- bough median {np.median(bp):.3f} (max "
                      f"{max(bp):.3f}), hammer median {np.median(hp):.3f}: {np.median(bp) / np.median(hp):.2f} of the "
                      f"hammer's, the loudest bough {max(bp) / np.median(hp):.2f}" +
                      (f"; crits -- bough {np.median(bc):.3f}, hammer {np.median(hc):.3f}" if bc and hc else
                       f"; crits: {len(bc)} bough, {len(hc)} hammer"))
                if max(bp) / np.median(hp) > 0.60:
                    FAILED.append("a real bough blow over 0.6 of the hammer's")
            if (sp_over and min(sp_over) < 6) or (wi_over and min(wi_over) < 3):
                FAILED.append("a new voice not heard in a real window")
            wav("ironwood-pick-real-window.wav", xw)
            wav("ironwood-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, sprout_over=sp_over, wither_over=wi_over, bough_pk=bp, hammer_pk=hp)
        # the four picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": "ironwood"}], ["arm", T0 + 1.5, "ult", {"w": "ironwood-sprout"}]]
        seq += [["arm", T0 + 2.1 + 0.45 * k, "hit", {"dmg": 9, "crit": False, "bough": WIN}] for k in range(3)]
        seq += [["arm", T0 + 3.6, "ult", {"w": "ironwood-wither"}], ["arm", T0 + 4.6, "hit", {"dmg": 24, "crit": False}]]
        xq_, _ = R(seq, secs=6.5, rows=sfx_rows)
        wav("ironwood-pick-sequence.wav", xq_)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "bands", "cracks", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), bough=strip(rows_b), bough_controls=strip(ctlb),
               sprout=strip(rows_s), wither=strip(rows_w), wither_controls=strip([RI, CQ]), wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_kc": C_["kc"], "bough": B_["name"],
                     "bough_v": B_["v"], "sprout": S_["name"], "sprout_g": S_["g"], "sprout_D": S_["D"],
                     "wither": W_["name"], "wither_g": W_["g"]})
    print(f"\nTHE PICKS  cast {C_['name']}   sprout {S_['name']}   bough {B_['name']}   wither {W_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    rows = [dict(label="Sfx: the bough blow -- a branch in front of the hit arm, taken only with `bough`",
                 anchor=HIT_ANCHOR, mode="replace", code=hit_code),
            dict(label="Sfx: Ironwood's cast, sprout and wither arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickTree: the sprout voice, on the frame the blade set appears",
                 anchor=SPROUT_ANCHOR, mode="replace", code=SPROUT_CODE),
            dict(label="tickTree: the wither voice, when the window closes by its clock with the caster alive",
                 anchor=WITHER_ANCHOR, mode="replace", code=WITHER_CODE),
            dict(label="resolveHit: the hit voice carries `bough` while the tree stands",
                 anchor=RH_ANCHOR, mode="replace", code=RH_CODE)]
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The five rows are the edits; all five were applied "
          "to the page's own code above.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
