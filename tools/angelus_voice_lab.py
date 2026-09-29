#!/usr/bin/env python3
"""ASCENSION'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v104.

    python angelus_voice_lab.py --game <a link carrying Angelus's stage 5> --rows rows.json

v74 §6.2 SOUND, every word of it: "The rise: a choir swell (three re-struck
tones a fifth and octave apart, 0.6s) -- the one voice in the game allowed to
be a chord. A shaft hit: a bright glassy tap, 70ms, quiet; blessing count in
the pitch. Close: the chord resolving down and the ball's landing thud." The
brief's stage 6: "picture, voice, carry per design §6". Rick, for the batch's
art and sound: "you pick i overrule". So this lab does not offer a spread --
it renders three to seven candidates a voice beside CONTROLS that can come
back wrong, prints the numbers each pick is made on, and PICKS by a rule
written in this file (`*_RULE`, `*_why`). He overrules from one clip.

NOTHING IS REUSED THAT DOES NOT EXIST. §6.2 names one existing sound, "the
ball's landing thud", and there is none: `move` plays the WALL TICK on every
floor contact (a 35 ms high-passed noise tick at 3 kHz, centroid 12 kHz), a
landing included. So the thud is NEW (`ult/angelus-land`), laid over that
tick on the landing's own frame; the tick still plays. "The chord" of the
close is the cast's own chord in the cast's own voice, not a voice of its own.

THE FOUR EVENTS AND WHERE THEY FIRE (the rows; line numbers are b9's):
  cast   the bare id `ult/angelus`, which `fireUlt` plays for every relic
         (16301). Angelus has NO arm today: it falls through to the shared
         rune-crack (so do Lastlight, Aureole, Censer and Spellbreaker --
         measured below, to 1e-7). The arms go BEFORE that fallback; the
         fallback line is re-emitted unchanged, last, so another relic's row
         anchored on it still applies, in either order.
  tap    `ult/angelus-shaft {n}` from `tickRise`, right after the heal's
         `T.bless += u.healPer * n;` (re-emitted first, unchanged): once per
         heal, after the caster's blessing has landed, `n` the caster's
         blessing count after it (1..5). A shaft hit is an ordinary blade blow
         and keeps its own `hit` voice; its blessing lands on the NEXT live
         step, after the blow's hit stop, so the tap sounds 67 ms after the
         blow (median; measured below) -- the heal's own moment. `n` (the
         hits delta) was 1 on every heal measured, so one tap is one shaft hit.
         A shaft hit on a Twinshade shade heals too (stage 5's reading 11), so
         it taps too. No beat is filed: the blow files its own.
  close  `ult/angelus-close` from `tickRise`, right after `f.ultRise = null;`
         (re-emitted first, unchanged), on the frame the window runs out BY
         ITS CLOCK with both fighters alive -- never on a death (a death close
         runs only in a kill flight), never once the fight is over (step()
         stops calling the tickers: stage 5's reading 10, 86 of 606 windows
         here are still open at `over` and play nothing -- the death voice has
         that moment, and the picture closes the shafts itself). The same line
         sets `falling` on `riseTally` -- the probe's tally, which nothing in
         the simulation reads -- so `move` knows the drop has begun.
  land   `ult/angelus-land` from `move`, right after the floor bounce's own
         `this.spawnFx(...)` line (a row in mode `after`): the FIRST
         floor contact after such a close, the caster alive, which clears
         `falling`. The ball drops from rest at (260, 300); 96 of 470 drops
         fall straight to the floor (0.59-1.66 s after the close, median 0.92
         s), the rest are knocked about on the way down and land later (the
         whole: 0.52-7.32 s, median 1.17 s). A knocked drop still lands, and
         thuds then. 42 closes never land (the fight ends first): no thud.

THE CONTROLS, and what each one is for:
  rune-crack   what ult/angelus plays TODAY; v88 published 0.608 / 450 ms --
               reproduced before anything new is quoted
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@9        Angelus's own blow (blade 9, stage 5): the level the cast and
               the thud are judged against, on its quietest / loudest draw
  hit@3.6      a SHAFT's blow (9 x winDmg 0.4), which the tap follows
  wall         the commonest sound in a fight, the tap's floor, and the tick
               the thud lands over
  the school   the sanctified casts with a voice of their own -- Daybreak and
               Zenith (Lastlight, Aureole and Censer ARE rune-crack)
  the type     the twinblade casts with a voice of their own -- Widowmaker,
               Twinshade, Thornshear, Starwarden (Spellbreaker IS rune-crack)
  seal         the game's other stack of fifths (220 / 330 / 495 Hz
               triangles, 90 ms apart): the chord must not be the seal
  death        the heaviest low voice: the thud must not be a death
  spark 1-5    the heal chime (the spark collect), n = the blessing count
  zt 0-4       Zenith's tick, the school's small bright chime
  hex-snap, clank, drum (`bed`'s own thump), score (the bed, mixed as
               `cinema_clip` mixes it: raw, x0.9)
  STRUCK, DYAD, OFFBEAT, RC-NOW   the chord struck once / without its octave
               / re-struck 11 ms apart flat, not at whole cycles (out of
               phase) / what ult/angelus plays today: each must fail its gate
  FLAT, LOUD, HARM, LONG, TICK   the picked tap family at one pitch for
               every count / 2.5x louder / on whole-number partials /
               ringing 200 ms / the wall tick's shape at its level
  AGAIN, UP, OTHER, GLIDE   the close resolving to the cast's own chord /
               UP to A4-E5-A5 / down to C4 (not the tonic) / gliding the
               whole way (no chord held)
  WALL, BOOM, RING, HIT   the wall tick at the thud's level / the thud
               over 450 ms / a held 110 Hz sine / the engine's blow at 9
  RAW          the chord without `.frequency.value = f` -- printed as a
               REFERENCE, not a control (see WHAT THE FIRST CUT GOT WRONG)

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
  * The shared measures are zenith_voice_lab's and ironwood_voice_lab's,
    imported unchanged: E50 = 50 ms RMS at a 5 ms hop; TOP = the loudest 50
    ms and where it is centred; START = the loudest 50 ms centred in the
    first 100 ms; SWELL = TOP - START; DIPS = drops of > 3 dB below the
    running max on the way up; FLUTTER = p95 - p5 of the RMS over four
    periods about its 100 ms average (v97; its floor, one steady strike, is
    printed); AUDIBLE = first to last 5 ms window above 2% of the loudest;
    RISE = 10 -> 90% of the 1 ms envelope; REG = cosine of 1/3-octave band
    amplitudes, 25 Hz-16 kHz, the median over noise draws; IN-BAND = RMS in
    the third-octave round a pitch, against the score's p90 there; PITCH =
    FFT peak (Hann, zero-padded, parabolic); inharm = ironwood's test (the
    strongest peak 1.5x-4x the note, its cents from a whole multiple).
  * THE CHORD (cast and close): each tone's FFT peak within 6% of it (cents
    off) and its third-octave RMS, over a stated window; FLUTTER is read at
    the chord's own period, D3 (4 periods of D3 = 8 of D4, 12 of A4).
  * THE CLOSE'S "GONE": each old tone's spectral peak within 40 cents,
    Hann-windowed (`peak_amp`), re the tonic's loudest.
  * NOISE PART: two draws of one text differ by exactly their noise-built
    part; (x1 - x2)/sqrt 2, the median over six pairs (portcullis's STONE
    method). A voice of sines reads the render floor, -180 dB.
  * THE CANDIDATES ARE LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's gain and swell depth put TOP at the centre of its
    window and SWELL at +12 dB, its decay solved to AUDIBLE 600 ms; the
    tap's gain puts its loudest 50 ms at the centre of its window at count
    3, its decay solved to 70 ms; the close sits 3 dB under the cast's TOP,
    its decay solved to 600 ms; the thud's TOP at the centre of its window,
    its decay solved to 120 ms. Constants are rounded BEFORE any measured
    render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of §6.2 turned into numbers;
Code's picks, Rick's to overrule):
  * THE CHORD is D4-A4-D5 (293.665 Hz, a just fifth, the octave), the
    score's iv; THE RESOLUTION is A3-E4-A4, its tonic, each voice DOWN a
    fourth -- iv -> i, the plagal cadence (the "Amen"). The rise hangs on the
    subdominant; the close lands home. D-A-D is also the chord that clashes
    least with the score's own four (Am, F, C, G share no semitone with it).
  * "RE-STRUCK": each tone held by re-striking it in phase at its own whole
    cycles every ~11 ms (Zenith's spacing), `.frequency.value = f` set on
    every strike (v97's toolkit rule); the first strike of a voice carries
    0.6 of its plateau (v97's HANDOFF).
  * "SWELL" crests where the rise ARRIVES: the strikes stop at 0.455 s, so
    the loudest 50 ms is centred at ~0.445 s -- the cast's 0.08 s hit stop
    plus the 0.35 s rise is 0.43 s, and the fights put the arrival 0.42 s
    after the cast voice (median; 0.42-1.75). "0.6s" is the whole voice.
  * THE TAP'S PITCH: one step of the score's A minor pentatonic a blessing
    count, from the candidate's root (counts clamped to 1..5, the cap); the
    count is the caster's own after the heal -- the one its tag shows.
  * THE CLOSE is as long as the cast (0.6 s: nothing in §6.2 gives it a
    length), its level falls 6 dB across its strikes (it settles) and sits
    3 dB under the cast's.
  * THE THUD's level sits between twice the wall tick it lands on and one
    blow; "a thud" is struck, short, low and dull (the rule's numbers).

THE PICKS, on Chromium 151.0.7922.34, sc-angelus-b9 db58100b3aa0092a, fight
seeds 104601-104602 (152 fights):

  cast   3 VOWEL   D4 A4 D5 as three sines, each strike carrying its 2nd and
                   3rd partials at 0.3 / 0.12, re-struck in phase, swelling
                   +11.9 dB to a crest at 445 ms and released: audible 605
                   ms, flutter 0.3 dB, no dips, every tone within 0.1 cents
                   and within 3 dB of the loudest; TOP -2.8 dB re the blow @ 9,
                   +16.5 re the wall; register at most 0.61 (Starwarden's
                   cast), 0.46 against the seal, 0.54 against Zenith's.
                   PURE, REED and STACK pass too and lose on register
                   (0.67-0.69, Starwarden); CHORUS is out (its 8-cent pair
                   reads D4 36 cents off over the crest).
  tap    5 SKY     a thin glass rod (sines on 1 : 2.76) at C8 D8 E8 G8 A8
                   (4186-7040 Hz) for blessing 1-5: audible 70 ms, rise 0,
                   centroid 4.8 kHz, no noise part; -9.3 dB re the shaft's
                   blow, +9.3 dB re the wall; register at most 0.51 (the wall
                   tick), 0.30 against Zenith's tick, 0.14 against the heal
                   chime. SHELL passes too and loses on register (0.52);
                   FAINT's partial is 21 dB down (not glassy); every tap
                   under C8 sits on the heal chime or Zenith's tick.
  close  1 STEP    the cast's chord and voice, the three voices stepping down
                   together at 0.15 s to A3-E4-A4, released: audible 590 ms,
                   the old tones 21.8 dB under the tonic by 300 ms, -3.0 dB
                   re the cast, the tonic +4.2 dB over twice the score;
                   register at most 0.62 (the seal), 0.91 against the cast
                   (printed: it IS the cast's chord). EARLY and SUSPEND pass
                   and lose on register (0.66-0.67); SLOW holds the old chord
                   too long (-11.2 dB at 300 ms).
  land   3 DEEP    a sine falling 95 -> 42 Hz under noise low-passed at 220
                   Hz: rise 2 ms, peak at 8 ms, audible 115 ms, all but 0.3%
                   of its power under 250 Hz, centroid 87 Hz; TOP -6.7 dB re
                   the blow @ 9, +12.7 re the wall; register at most 0.77
                   (the death voice), 0.43 against the blow (the score's drum,
                   printed, 0.83). BODY, BARE and KNOCK read 0.96-0.99
                   against the death voice; BOARD and SLAB 0.91-0.92 against
                   the blow, and under the score.

  In play (152 fights; the mirror match is refused by Match): 606 casts and
  606 cast voices; 3555 shaft hits healed and 3555 taps, each on its heal's
  step with the caster's count after it (1: 585, 2: 563, 3: 544, 4: 508,
  5: 1355 -- the cap is 38% of taps); 512 windows closed by their clock with
  both alive and 512 closes; 470 landings after them and 470 thuds; none
  for the 8 death closes or the 86 windows open at the end; 152/152 fights
  identical, every other voice call identical in order, kind and opts, and
  the caster's riseTally different by `falling` alone; the sim-write control
  1/152. The landing comes 0.52-7.32 s after the close (median 1.17 s); 42
  closes never land because the fight ends first.

  In a real window (Starwarden, Angelus side A, seed 104602: cast at 66.54
  s, closed by its clock at 77.92 s, landed at 78.76 s, 12 shaft hits healed
  at counts 1 2 3 4 5 5 5 5 5 5 5 5), the fight's own sounds and the score
  mixed as `cinema_clip` mixes them, with and without the new voices: every
  tap +6.7 to +64.5 dB over the fight in its own third-octave; the cast's
  chord +12.9 / +9.9 / +20.8 dB at D4 / A4 / D5 over the 150 ms before its
  crest; the close's tonic +7.2 dB at A4 and +4.5 at E4 (A3 itself -1.4,
  under the score's bass); the thud +12.4 dB at 79 Hz, its best
  third-octave under 250 Hz. Written to angelus-pick-real-window.wav and
  -without.wav.

  Main-thread cost a call, headless, on this PC while other builds ran:
  the cast 11.9-18.2 ms and the close 9.2-14.3 ms across runs (393 and 303
  `_tone` calls: a re-struck three-voice chord is hundreds of strikes), the
  tap and the thud 0.1 ms (see FOR RICK).

  End to end (a scratch check, not this file): the four rows applied AS
  TEXT to sc-angelus-b9 (page 32d55d74179c4335), both pages loaded, seed
  104701: 76/76 fights identical, every other voice call identical, taps ==
  blessings (1865), closes == clock closes with both alive (261), 238 thuds,
  each only after a close; the new voices through the page's own play
  within 1.2e-7 of this file's text, 37 other voices within 1.8e-7. The
  same on Angelus rebuilt by angelus_build.py onto the batch line's newest
  tip then (02-chain/sc-lodestone-b205-fx.html): 80/80. The rows carry
  onto ten tips (every anchor once, +8042 chars each) and commute with the
  picture's eight rows.

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table; that table passed four casts, no tap, no close and
one thud, and the first real window then failed the thud. Each is one of
these:
  * RAW WAS NOT A CONTROL. It was listed as the control on v97's finding
    (without `.frequency.value = f` a re-strike loses its phase above ~500
    Hz) and it passed every gate: its samples differ from PURE's by 0.087,
    but its crest by -0.2 dB and its flutter not at all -- at D4-D5 with an
    11 ms spacing the slip is not a thing these rules, or an ear, can hear.
    A control that cannot fail proves nothing, so RAW is printed as a
    reference and OFFBEAT (the strikes a flat 11 ms apart, not whole cycles:
    truly out of phase) is the control; it fails (a dip, the pitches 55-125
    cents off, the crest 12 dB down). The arms keep the line (the toolkit's
    rule).
  * THE TAP'S PITCH. The four first taps (a glass rod or bowl on E6-D7, the
    rod on A6-G7) read 0.92-1.00 against the heal chime (the spark collect,
    1.3-1.7 kHz) and Zenith's tick (C7-A7 on the same free-bar modes); the
    E6 ones were not bright (centroid 1.3-1.6 kHz). Every pure tap between
    1.3 and 3.5 kHz meets one of those two in its own third-octave, so three
    were added above Zenith's tick, on C8-A8: SKY and SHELL pass, FAINT's
    partial is 1 dB too faint. No tap rule was changed; the controls were
    moved onto SKY so each fails its own gate, not merely the register.
  * THE CLOSE'S "GONE" (an instrument fix): every close failed only "the old
    chord not gone" (-6.6 to -7.7 dB) because it was read in third-octave
    bands, and E4 (329.63 Hz) sits on the D4 band's edge (329.62) -- the
    tonic's own tones leaked into the old chord's bands. It is now read at
    each old tone's own spectral peak (within 40 cents, Hann-windowed): STEP
    -21.8 dB, EARLY -44.0, SUSPEND -13.4, SLOW -11.2 (still out). AGAIN, the
    control, reads +3.7 and fails as before.
  * THE THUD IN THE REAL WINDOW (a rule change, made once): its gate first
    read the one third-octave where the thud is loudest in isolation, 100
    Hz -- -3.6 dB, because the score's A2 bass (110 Hz) shares that band and
    two tones in one band add by their phase. Two thuds with a floor's knock
    on top were added (KNOCK, SLAB: both out on register) and the gate was
    moved to the power 40-500 Hz -- +0.8 dB, because the score's A1 bass
    carries most of that power and the ear little of it. It now reads the
    thud's BEST third-octave under 250 Hz, which is how its isolation gate
    ("heard") has read it from the start. A scratch survey (diag_thud.py:
    25 landings in 8 fights, the bed at each fight's own time) puts every
    landing +5.2 dB or more over the fight at its best band (79 or 63 Hz).

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (the four arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the tap at
    counts -1, 0, 1..5, 7 and a missing `n`) must reproduce its candidate to
    TOL; every other voice through the patched play (the hit at five weights
    with and without a crit and the bough, spark x3, wall, death, clank x2,
    seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork, scour x4, and
    every relic's cast and every sub-voice the ult arm names -- 127 voices)
    must be unchanged; `ult/angelus` must NOT be rune-crack any more;
  * the tickRise and move rows are applied to their prototypes' own source
    and run on real fights beside the unpatched ones: every fight identical
    (over, clock, both hp, positions, velocities, stuns, both blessing and
    smite counts, both blow ledgers, winner, both riseTallies but
    `falling`) and every other voice call identical in order, kind and opts;
    one tap per heal, on its step, carrying the count the heal's apply left;
    one close per window closed by its clock with both alive and none
    otherwise; one thud per first floor contact after such a close (read off
    the bounce's own spawnFx call), and none otherwise; the unpatched runs
    play none of them. The same rows plus ONE sim write (the foe nudged 1e-9
    on a tap) must come back NOT identical, or "identical" proves nothing.
    (The Sfx row cannot reach the simulation at all: `play` returns on its
    first line with no audio context, which is every headless run.)
  All anchors must occur exactly once in the game file. Three rows are a
  `replace` that re-emits its anchor unchanged exactly once; the landing's
  is an `after` (its anchor is the bounce's own spawnFx line, so its code is
  only what it adds and does not repeat that line). Either way the anchor
  survives, so a later relic's row -- or the picture's -- anchored on the
  same line still applies, in either order. No row's code (comments
  stripped) names rng, spawnFx, Math.random or ultFx. The rows are then
  applied AS TEXT, the orchestrator's way, and must give byte for byte the
  page the checks ran on.

FOR RICK TO OVERRULE ("you pick i overrule"):
  * THE COST. A three-voice re-struck chord is hundreds of `_tone` calls: the
    cast measures 12-18 ms of main thread a call here and the close 9-14 ms
    (up to a frame at 60 fps, once per cast and close; this PC was running
    other builds). The video renders offline and does not feel it; the live
    app may drop a frame at the cast, which lands in the cast's own 0.08 s
    hit stop. PURE passes every gate at a third of the calls (131; 4.7-5.1
    ms) and loses only the register tiebreak (0.67 against Starwarden's
    cast, VOWEL 0.61).
  * THE END OF A FIGHT. In 57% of fights the window is still open at the
    kill (stage 5's reading 10); `tickRise` never runs again, so there is no
    close chord and no thud there: the kill's own voices have that moment,
    and the picture shortens the shafts on its own clock. A close voice at
    the kill is the other reading; it would sound over the death voice.
  * THE TAP sits high, 4.2-7 kHz (C8-A8): the only register a pure glass tap
    has free in this game, over the heal chime and Zenith's tick.
  * THE THUD is 42-95 Hz: a phone speaker will not play it; headphones and
    the desktop will. Every higher thud tried reads as the blow or the death
    voice.
  * THE LANDING is the first floor contact after the close, so a drop the foe
    knocks about lands (and thuds) later: median 1.17 s after the close, 80%
    of drops knocked. A fixed-delay thud inside the close voice is the other
    reading of "the chord resolving down and the ball's landing thud".

Writes wavs to 05-reference/v104/angelus-*.wav at RAW level (gitignored).
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
    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, dips_and_lin, env,
    flutter, fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm, low_share, lowpass_fft  # noqa: E402

HERE = pathlib.Path(__file__).parent
RELIC = "angelus"
BLADE = 9.0                               # Angelus's dmg (stage 5)
WIN = 0.4                                 # w.ult.winDmg: a shaft hit's damage scale
SHAFT = BLADE * WIN                       # a shaft blow's dmg, which `hit` plays it at
BLESS_CAP = 5                             # STATUS.blessing.maxStacks
CAST_AUD, TAP_AUD, CLOSE_AUD, LAND_AUD = 600.0, 70.0, 600.0, 120.0
CREST = 0.455                             # the cast's strikes stop here: its loudest 50 ms is centred ~0.43 s
ARRIVE = 0.43                             # 0.08 s of the cast's hit stop + the 0.35 s rise (measured below)
SWELL_DB = 12.0                           # the cast's level-matched swell (Zenith's)
EVERY = 0.011                             # the re-strike spacing target, s (Zenith's; rounded to whole cycles)
A0 = 0.6                                  # a voice's first strike carries 0.6 of its plateau (v97 HANDOFF)
D4, A3 = 293.665, 220.0                   # the chord's root (the score's iv) and the resolution's (its tonic)
CLOSE_END = 0.35                          # the close's strikes stop here; its release is the decay
CLOSE_FALL_DB = 6.0                       # the close's level falls 6 dB across its strikes (it settles)
CLOSE_UNDER_DB = 3.0                      # the close's level match under the cast's top
PENT = [0, 3, 5, 7, 10]                   # the A minor pentatonic, from A: A C D E G
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)


def note_hz(name):
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    k = names[name[0]] + (1 if "#" in name else 0)
    octv = int(name[-1])
    return 440.0 * 2 ** ((k + 12 * (octv - 4)) / 12)


def note_name(f):
    names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    k = round(12 * math.log2(f / 55.0))
    return f"{names[k % 12]}{(k + 9) // 12 + 1}"


def pent_from(root):
    """Five pentatonic degrees upward from `root` (a note of A minor pentatonic)."""
    r = 12 * math.log2(root / 440.0)
    deg = []
    s = round(r)
    while len(deg) < 5:
        if (s % 12) in PENT:
            deg.append(round(440.0 * 2 ** (s / 12), 2))
        s += 1
    return deg


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


def vjs(V):
    return "[" + ", ".join("[" + ", ".join(fmt(v) for v in x) + "]" for x in V) + "]"


# =============================================================== THE CAST ===
# "a choir swell (three re-struck tones a fifth and octave apart, 0.6s) -- the
# one voice in the game allowed to be a chord". Every candidate is the chord
# D4-A4-D5 (root, just fifth, octave), each tone held by re-striking it in
# phase at its own whole cycles (a held note does not exist in this toolkit),
# the three swelling together to a crest at the arrival. They differ in the
# VOICE: the timbre, how the voices enter, whether each is sung by one or two.
#   voices  [ratio, level, entry s, detune cents] per sung voice
#   type    the oscillator; harm  [multiple, level] partials over each strike
CHORD = [(1.0, 1.0), (1.5, 0.8), (2.0, 0.6)]
CAST_CANDIDATES = [
    ("1 PURE", dict(voices=[(r, k, 0, 0) for r, k in CHORD], type="sine", harm=[], f=D4),
     "three sines, D4 A4 D5, re-struck in phase, swelling together: the 'oo' of a choir"),
    ("2 REED", dict(voices=[(r, k, 0, 0) for r, k in CHORD], type="triangle", harm=[], f=D4),
     "PURE on triangles (odd partials): a reedier voice"),
    ("3 VOWEL", dict(voices=[(r, k, 0, 0) for r, k in CHORD], type="sine", harm=[(2, 0.3), (3, 0.12)], f=D4),
     "PURE with each strike's 2nd and 3rd partials at 0.3 / 0.12: an 'ah' drawn in partials"),
    ("4 STACK", dict(voices=[(1.0, 1.0, 0, 0), (1.5, 0.8, 0.08, 0), (2.0, 0.6, 0.16, 0)], type="sine", harm=[],
                     f=D4),
     "PURE with the voices entering in turn, root, fifth +80 ms, octave +160 ms: the choir joining"),
    ("5 CHORUS", dict(voices=[(r, k * 0.5, 0, c) for r, k in CHORD for c in (-4, 4)], type="sine", harm=[], f=D4),
     "PURE with every tone sung by two voices 8 cents apart: an ensemble's slow shimmer"),
]


def cast_body(sp, g, sw, D, ind=10, fix=True, struck=False, drop=None, offbeat=False):
    """The cast arm's body. `fix` False is the RAW control (no `.frequency.value
    = f`); `struck` the STRUCK control (each tone struck once); `drop` a list of
    ratios to leave out (the DYAD control); `offbeat` the OFFBEAT control (the
    strikes a flat 11 ms apart, not whole cycles: out of phase)."""
    V = [v for v in sp["voices"] if not drop or v[0] not in drop]
    typ = sp["type"]
    fx = ".frequency.value = f" if fix else ""
    L = [f"const g = {fmt(g)}, sw = {fmt(sw)}, D = {fmt(D)}, L = {fmt(CREST)}, F = {fmt(sp['f'])};"]
    if struck:
        L += [f"for (const [r, k, s0, c] of {vjs(V)}){{",
              "  const f = F * r * Math.pow(2, c / 1200);",
              f"  this._tone(t, {{ freq: f, gain: g * k, dur: D, type:\"{typ}\" }}){fx};",
              "}"]
        return "\n".join(" " * ind + l for l in L)
    L += ["const lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);",
          f"for (const [r, k, s0, c] of {vjs(V)}){{",
          (f"  const f = F * r * Math.pow(2, c / 1200), dt = {fmt(EVERY)};" if offbeat else
           f"  const f = F * r * Math.pow(2, c / 1200), dt = Math.max(1, Math.round(f * {fmt(EVERY)})) / f;"),
          "  const q = Math.pow(0.0001 / lv(s0), dt / D);",
          "  for (let j = 0; s0 + j * dt < L - 1e-9; j++){",
          f"    const s = s0 + j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, {fmt(A0)} / (1 - q)));",
          f"    this._tone(t + s, {{ freq: f, gain: a, dur: D, type:\"{typ}\" }}){fx};"]
    if sp["harm"]:
        L += [f"    for (const [h, kh] of {vjs(sp['harm'])})",
              f"      this._tone(t + s, {{ freq: f * h, gain: a * kh, dur: D, type:\"{typ}\" }})"
              + (".frequency.value = f * h;" if fix else ";")]
    L += ["  }", "}"]
    return "\n".join(" " * ind + l for l in L)


# ================================================================ THE TAP ===
# "A shaft hit: a bright glassy tap, 70ms, quiet; blessing count in the pitch."
# One struck glass a call, at the pentatonic degree the caster's blessing
# count (1..5) names from the candidate's root. Glass rings in inharmonic
# modes, and it is pure: sines only, no noise.
TAP_MODES = {
    "rod": [(1, 1, 1), (2.76, 0.35, 0.6)],                       # a thin glass rod (free-bar modes)
    "bowl": [(1, 1, 1), (2.32, 0.4, 0.7), (4.25, 0.15, 0.45)],   # a struck glass bowl (shell modes)
    "thin": [(1, 1, 1), (2.76, 0.15, 0.5)],                      # the rod with its mode faint
    "shell": [(1, 1, 1), (2.32, 0.4, 0.7)],                      # a glass shell's first two modes
    "harm": [(1, 1, 1), (2, 0.35, 0.7), (3, 0.15, 0.5)],         # whole-number partials: a control
}
TAP_CANDIDATES = [
    ("1 ROD", dict(modes="rod", root="E6"),
     "a thin glass rod (sines on 1 : 2.76), E6 G6 A6 C7 D7 for blessing 1-5"),
    ("2 BOWL", dict(modes="bowl", root="E6"),
     "a struck glass bowl (sines on 1 : 2.32 : 4.25), E6-D7"),
    ("3 HIGH", dict(modes="rod", root="A6"),
     "ROD a fourth up, A6 C7 D7 E7 G7"),
    ("4 THIN", dict(modes="thin", root="E6"),
     "ROD with its upper mode at 0.15: the purest glass"),
    # added after the first table (see WHAT THE FIRST CUT GOT WRONG): above Zenith's tick, C8-A8
    ("5 SKY", dict(modes="rod", root="C8"),
     "ROD two octaves and a sixth up: C8 D8 E8 G8 A8 (4186-7040 Hz), over Zenith's tick"),
    ("6 SHELL", dict(modes="shell", root="C8"),
     "a glass shell's first two modes (sines on 1 : 2.32), C8-A8"),
    ("7 FAINT", dict(modes="thin", root="C8"),
     "THIN on C8-A8"),
]
TAP_CTL = "5 SKY"                         # the tap the controls are built on


def tap_notes(sp):
    return [pent_from(note_hz(sp["root"]))[0]] * 5 if sp.get("flat") else pent_from(note_hz(sp["root"]))


def tap_body(sp, g, D, ind=10):
    if sp.get("tick"):                      # the TICK control: the wall tick's own shape, at the tap's level
        L = [f"const g = {fmt(g)}, D = {fmt(D)};",
             'this._burst(t, { freq: 3000, q: 2.0, gain: g, dur: D, type:"highpass" });']
        return "\n".join(" " * ind + l for l in L)
    tab = ", ".join(fmt(f) for f in tap_notes(sp))
    L = [f"const n = clamp(Math.round(p.n || 0), 1, {BLESS_CAP}), g = {fmt(g)}, D = {fmt(D)};",
         f"const F = [{tab}][n - 1];",
         f"for (const [r, k, d] of {vjs(TAP_MODES[sp['modes']])})",
         '  this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;']
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE CLOSE ===
# "the chord resolving down". Every candidate is the PICKED cast's chord (its
# voices, timbre and re-strike) moving down to the score's tonic: D4-A4-D5 ->
# A3-E4-A4, each voice down a fourth -- iv -> i, the plagal cadence (the
# "Amen"). The level falls 6 dB across the strikes and the release is the
# decay. They differ in WHEN the voices move.
#   sw   per voice (root, fifth, octave): the moment it steps down, s
CLOSE_CANDIDATES = [
    ("1 STEP", dict(sw=(0.15, 0.15, 0.15)), "the three voices step down together at 0.15 s"),
    ("2 EARLY", dict(sw=(0.08, 0.08, 0.08)), "STEP at 0.08 s: the chord barely held before it moves"),
    ("3 SLOW", dict(sw=(0.22, 0.22, 0.22)), "STEP at 0.22 s: the chord held, then a short resolution"),
    ("4 SUSPEND", dict(sw=(0.12, 0.12, 0.24)), "root and fifth move at 0.12 s, the top voice holds "
                                                "(a suspension) and resolves at 0.24 s"),
]
CLOSE_CONTROLS = [
    ("0 AGAIN", dict(sw=(0.15, 0.15, 0.15), to=None), "STEP 'resolving' to the cast's own chord: no resolution"),
    ("0 UP", dict(sw=(0.15, 0.15, 0.15), to=440.0), "STEP resolving UP, to A4-E5-A5"),
    ("0 OTHER", dict(sw=(0.15, 0.15, 0.15), to=note_hz("C4")), "STEP resolving down to C4: not the tonic"),
    ("0 GLIDE", dict(glide=True), "every voice gliding from the cast's chord to the tonic's across the "
                                  "whole close: no chord held"),
]


def close_body(sp, cast_sp, g, D, ind=10):
    V = cast_sp["voices"]
    typ, H = cast_sp["type"], cast_sp["harm"]
    F0 = cast_sp["f"]
    F1 = F0 if ("to" in sp and sp["to"] is None) else sp.get("to", A3)
    L = [f"const g = {fmt(g)}, D = {fmt(D)}, E = {fmt(CLOSE_END)}, F0 = {fmt(F0)}, F1 = {fmt(F1)};",
         f"const lv = (s) => g * Math.pow(10, -{fmt(CLOSE_FALL_DB)} * s / E / 20);"]
    hl = []
    if H:
        hl = [f"      for (const [h, kh] of {vjs(H)})",
              f"        this._tone(t + s, {{ freq: f * h, gain: a * kh, dur: D, type:\"{typ}\" }}).frequency.value = f * h;"]
    if sp.get("glide"):
        L += [f"for (const [r, k, s0, c] of {vjs(V)}){{",
              "  for (let s = 0; s < E - 1e-9; ){",
              "    const f = F0 * Math.pow(F1 / F0, s / E) * r * Math.pow(2, c / 1200), a = k * lv(s);",
              f"    this._tone(t + s, {{ freq: f, gain: a, dur: D, type:\"{typ}\" }}).frequency.value = f;"]
        L += [x[2:] for x in hl]
        L += [f"    s += Math.max(1, Math.round(f * {fmt(EVERY)})) / f;", "  }", "}"]
        return "\n".join(" " * ind + l for l in L)
    VV = [(v[0], v[1], v[3], sp["sw"][[1.0, 1.5, 2.0].index(v[0])]) for v in V]
    L += [f"for (const [r, k, c, s1] of {vjs(VV)})",
          "  for (const [F, s0, s2] of [[F0, 0, s1], [F1, s1, E]]){",
          f"    const f = F * r * Math.pow(2, c / 1200), dt = Math.max(1, Math.round(f * {fmt(EVERY)})) / f;",
          "    const q = Math.pow(0.0001 / lv(s0), dt / D);",
          "    for (let j = 0; s0 + j * dt < s2 - 1e-9; j++){",
          f"      const s = s0 + j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, {fmt(A0)} / (1 - q)));",
          f"      this._tone(t + s, {{ freq: f, gain: a, dur: D, type:\"{typ}\" }}).frequency.value = f;"]
    L += hl
    L += ["    }", "  }"]
    return "\n".join(" " * ind + l for l in L)


# =============================================================== THE LAND ===
# "the ball's landing thud". The engine plays its WALL TICK on every floor
# contact (a 35 ms high-passed noise tick at 3 kHz) -- there is no thud to
# reuse, so this is a new one, laid over that tick on the landing's frame. A
# sine falling as the body meets the floor, under a short low noise (the floor).
LAND_CANDIDATES = [
    ("1 BODY", dict(f0=120, f1=50, nf=300, nq=0.7, kn=0.6, ntype="lowpass"),
     "a sine falling 120 -> 50 Hz under a short low-passed noise at 300 Hz"),
    ("2 BOARD", dict(f0=150, f1=70, nf=240, nq=1.2, kn=0.7, ntype="bandpass"),
     "a sine falling 150 -> 70 Hz under a band of noise at 240 Hz: a wooden floor"),
    ("3 DEEP", dict(f0=95, f1=42, nf=220, nq=0.7, kn=0.5, ntype="lowpass"),
     "BODY lower: 95 -> 42 Hz under noise low-passed at 220 Hz"),
    ("4 BARE", dict(f0=120, f1=50, nf=0), "BODY's sine alone"),
    # added after the first real window (see WHAT THE FIRST CUT GOT WRONG): a floor's knock over the body
    ("5 KNOCK", dict(f0=110, f1=45, nf=380, nq=0.9, kn=0.9, ntype="bandpass", nd=0.35),
     "a sine falling 110 -> 45 Hz under a short band of noise at 380 Hz: the floor's knock"),
    ("6 SLAB", dict(f0=150, f1=60, nf=450, nq=0.7, kn=0.8, ntype="lowpass", nd=0.35),
     "a sine falling 150 -> 60 Hz under a short low-passed noise at 450 Hz: a stone floor"),
]


def land_body(sp, g, D, ind=10):
    if sp.get("ring"):                      # the RING control: a held 110 Hz sine
        L = [f"const g = {fmt(g)}, D = {fmt(D)};",
             'this._tone(t, { freq: 110, gain: g, dur: D, type:"sine" }).frequency.value = 110;']
        return "\n".join(" " * ind + l for l in L)
    if sp.get("tick"):                      # the WALL control: the wall tick's shape at the thud's level
        L = [f"const g = {fmt(g)};",
             'this._burst(t, { freq: 3000, q: 2.0, gain: g, dur: 0.035, type:"highpass" });']
        return "\n".join(" " * ind + l for l in L)
    L = [f"const g = {fmt(g)}, D = {fmt(D)};",
         f'this._tone(t, {{ freq: {fmt(sp["f0"])}, to: {fmt(sp["f1"])}, gain: g, dur: D, type:"sine" }});']
    if sp["nf"]:
        L += [f'this._burst(t, {{ freq: {fmt(sp["nf"])}, q: {fmt(sp["nq"])}, gain: g * {fmt(sp["kn"])}, '
              f'dur: D * {fmt(sp.get("nd", 0.5))}, type:"{sp["ntype"]}" }});']
    return "\n".join(" " * ind + l for l in L)


# The score's own drum (`bed`'s thump, verbatim at its downbeat gain): a register reference for the thud.
DRUM_BODY = ('this._tone(t, { freq: 78, to: 34, gain: 0.1, dur: 0.30, type:"sine" });\n'
             'this._burst(t, { freq: 160, q: 0.8, gain: 0.05, dur: 0.14, type:"lowpass" });')


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
HEAL_ANCHOR = '          T.bless += u.healPer * n;'
CLOSE_ANCHOR = '        f.ultRise = null;'
LAND_ANCHOR = '      this.spawnFx(f.x, f.y, f.aff.core, 3, 90, 0.3, 2);'

HEAL_CODE = HEAL_ANCHOR + '''
          /* ASCENSION'S SHAFT HIT (v74 §6.2: "a bright glassy tap, 70ms,
             quiet; blessing count in the pitch"): once per shaft hit healed,
             after its blessing lands -- the NEXT live step after the blow,
             once the blow's own hit stop has run -- pitched by the count the
             caster now carries (1-5; at the cap the blessing refreshes and it
             taps at 5's note). The blow keeps its own `hit` voice. A shaft
             hit on a Twinshade shade heals too, so it taps too. Presentation
             only: SFX.play draws nothing, is a no-op headless, and nothing
             here is read back (angelus_voice_lab: fights identical). */
          SFX.play("ult", { w: "angelus-shaft", n: f.stacks("blessing") });'''

CLOSE_CODE = CLOSE_ANCHOR + '''
        /* ASCENSION'S CLOSE (v74 §6.2: "the chord resolving down and the
           ball's landing thud"): the chord only when the window runs out BY
           ITS CLOCK with both fighters alive -- a caster's death closes it in
           a kill flight, and a fight that ends with the window open never
           gets here (step() stops calling this), so both are left to the
           death voice, as Zenith's, Canopy's and Onslaught's closes are. The
           ball drops from here; `falling` (on `riseTally`, which nothing in
           the simulation reads) tells `move` that its next floor contact is
           the landing. Plain SFX.play; nothing is read back. */
        if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){
          SFX.play("ult", { w: "angelus-close" });
          T.falling = 1;
        }'''

LAND_CODE = LAND_ANCHOR + '''
      /* ASCENSION'S LANDING (v74 §6.2: "... and the ball's landing thud"):
         the first floor contact after the window closed by its clock, the
         caster alive -- over the wall tick this contact plays anyway, which
         is not a thud. A drop knocked about on its way down still lands, and
         thuds then. `riseTally` is the probe's tally; nothing in the
         simulation reads it. Presentation only; nothing is read back. */
      if (f.riseTally && f.riseTally.falling && f.alive && f.y >= hiY){
        f.riseTally.falling = 0;
        SFX.play("ult", { w: "angelus-land" });
      }'''

# the sim-write control: the same heal row with the foe nudged 1e-9 on a tap
HEAL_CODE_BAD = HEAL_CODE.replace(
    '          SFX.play("ult", { w: "angelus-shaft"',
    '          (f === this.a ? this.b : this.a).vx += 1e-9;\n          SFX.play("ult", { w: "angelus-shaft"', 1)

# what each row ADDS (the landing's anchor is the bounce's own spawnFx line: its row ships in mode `after`,
# the code below minus that line; the checks here run the replace pairs, and main() proves the two give one page)
_refuse(HEAL_CODE[len(HEAL_ANCHOR):] + CLOSE_CODE[len(CLOSE_ANCHOR):] + LAND_CODE[len(LAND_ANCHOR):], "sim rows")
for _c, _a in ((HEAL_CODE, HEAL_ANCHOR), (CLOSE_CODE, CLOSE_ANCHOR), (LAND_CODE, LAND_ANCHOR)):
    assert _c.count(_a) == 1 and _c.startswith(_a), "a sim row must re-emit its anchor first, exactly once"
assert HEAL_CODE_BAD != HEAL_CODE


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


NAMES = {"hit@9": "the blow", "hit@3.6": "the shaft's blow", "wall": "the wall tick", "death": "the death voice",
         "seal": "the seal", "rune-crack": "rune-crack", "hex-snap": "the runic snap", "cast": "the cast",
         "spark": "the heal chime", "zenith-tick": "Zenith's tick", "clank": "the clank", "drum": "the score's drum",
         "tap": "the tap", "close": "the close"}


def who(regs):
    k = max(regs, key=regs.get)
    return NAMES.get(k, k[0].upper() + k[1:] + "'s cast")


VOICE_WORDS = {"1 PURE": "three sines", "2 REED": "three triangles",
               "3 VOWEL": "three sines, each strike carrying its 2nd and 3rd partials at 0.3 / 0.12",
               "4 STACK": "three sines entering in turn (the fifth 80 ms after the root, the octave 160 ms)",
               "5 CHORUS": "three tones each sung by two sines 8 cents apart"}


def arms_code(C_, T_, K_, L_, info):
    names = [X["name"].split()[1] for X in (C_, T_, K_, L_)]
    c_cast = _wrap([
        f'ANGELUS\'S CAST, THE RISE -- v74 §6.2: "a choir swell (three re-struck tones a fifth and octave '
        f'apart, 0.6s) -- the one voice in the game allowed to be a chord". {names[0]}, of {info["n_cast"]}, '
        f'picked on the numbers by `angelus_voice_lab.py` under Rick\'s "you pick i overrule" (v104). Angelus '
        f'had no arm and fell through to rune-crack, which other relics still use, so this ADDS arms before '
        f'that fallback and leaves it alone.',
        f"D4, A4 and D5 (the score's iv: root, fifth, octave) as {VOICE_WORDS[C_['name']]}, each held by "
        f"re-striking it in phase at its own whole cycles every ~11 ms, swelling {C_['swell']:+.1f} dB to a "
        f"crest {C_['top_at'] * 1000:.0f} ms in -- where the rise arrives and the shafts light -- and released: "
        f"audible {C_['aud']:.0f} ms, its crest {info['c_top']:+.1f} dB re Angelus's own blow. Register at most "
        f"{info['c_reg']:.2f} ({info['c_regw']}) against rune-crack, the seal (the game's other stack of "
        f"fifths), the school's and the twinblades' casts, the death voice and the blow."], 10)
    notes = " ".join(note_name(f) for f in tap_notes(T_["sp"]))
    mw = {"rod": "a thin glass rod (sines on 1 : 2.76)", "bowl": "a struck glass bowl (sines on 1 : 2.32 : 4.25)",
          "thin": "a thin glass rod (sines on 1 : 2.76, the upper faint)",
          "shell": "a glass shell (sines on its first two modes, 1 : 2.32)"}[T_["sp"]["modes"]]
    c_tap = _wrap([
        f'A SHAFT HIT -- "a bright glassy tap, 70ms, quiet; blessing count in the pitch" (v74 §6.2). '
        f'{names[1]}, of {info["n_tap"]} (`angelus_voice_lab.py`). `tickRise` plays it once per shaft hit '
        f"healed, after the blessing lands, with `n`, the caster's blessing count (1-5).",
        f"{mw[0].upper() + mw[1:]}, one step of the score's A minor pentatonic a count: {notes} (counts "
        f"clamped to 1..5). Audible {T_['aud_lo']:.0f}-{T_['aud_hi']:.0f} ms; its loudest 50 ms "
        f"{info['t_db']:+.1f} dB re the shaft's own blow and {info['t_wall']:+.1f} dB re the wall tick; centroid "
        f"{T_['cen_lo']:.0f} Hz or more. Register at most {info['t_reg']:.2f} ({info['t_regw']}) against the "
        f"heal chime, Zenith's tick, the wall tick, the runic snap, the blow and the cast."], 10)
    c_close = _wrap([
        f'THE CLOSE -- "the chord resolving down" (v74 §6.2). {names[2]}, of {info["n_close"]} '
        f"(`angelus_voice_lab.py`): the cast's own chord and voice moving down a fourth to the score's tonic, "
        f"A3-E4-A4 (iv -> i, the plagal cadence), {K_['blurb']}; the level falls {CLOSE_FALL_DB:g} dB across it "
        f"and the release is the decay. Audible {K_['aud']:.0f} ms, its loudest 50 ms {info['k_db']:+.1f} dB re "
        f"the cast. Register at most {info['k_reg']:.2f} ({info['k_regw']}) against the seal, the death voice, "
        f"rune-crack and the blow. `tickRise` plays it only when the window closes by its clock with both "
        f"alive."], 10)
    c_land = _wrap([
        f'THE LANDING -- "and the ball\'s landing thud" (v74 §6.2). The engine plays its wall tick on every '
        f"floor contact and had no thud, so this one is new. {names[3]}, of {info['n_land']} "
        f"(`angelus_voice_lab.py`): {L_['blurb']}. Audible {L_['aud']:.0f} ms, {100 * L_['low']:.0f}% of its "
        f"power under 250 Hz, its loudest 50 ms {info['l_db']:+.1f} dB re the blow. Register at most "
        f"{info['l_reg']:.2f} ({info['l_regw']}) against the blow, the death voice, the wall tick and the "
        f"clank. `move` plays it on the first floor contact after a clock close, the caster alive."], 10)
    return (f'        }} else if (w === "angelus"){{                    // it rises\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["sw"], C_["D"])}\n'
            f'        }} else if (w === "angelus-shaft"){{              // a shaft hit healed\n'
            f'{c_tap}\n{tap_body(T_["sp"], T_["g"], T_["D"])}\n'
            f'        }} else if (w === "angelus-close"){{              // the chord resolves down\n'
            f'{c_close}\n{close_body(K_["sp"], C_["sp"], K_["g"], K_["D"])}\n'
            f'        }} else if (w === "angelus-land"){{               // and the ball lands\n'
            f'{c_land}\n{land_body(L_["sp"], L_["g"], L_["D"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# The tickRise and move rows, applied to the real prototypes and run beside the
# original; the survey of Ascension's windows comes out of the same runs.
WIRE_JS = r"""([seeds, riseRows, landRow, mirror]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, CF = AC.CONFIG;
  const oR = P.tickRise, oM = P.move;
  const patch = (fn, rows, nm) => {
    let src = fn.toString();
    for (const [a, c] of rows){
      const at = src.split(a).length - 1;
      if (at !== 1) return { err: `a ${nm} anchor occurs ${at} times in ${nm}()` };
      src = src.replace(a, () => c);
    }
    return (0, eval)("(function " + src + ")");
  };
  const pR = patch(oR, riseRows, "tickRise"), pM = patch(oM, [landRow], "move");
  if (pR.err) return pR; if (pM.err) return pM;
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const MINE = (k, p) => k === "ult" && p && typeof p.w === "string" && (p.w === "angelus" || p.w.startsWith("angelus-"));
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "angelus");
  const RT = (x) => x.riseTally ? JSON.stringify(Object.fromEntries(Object.entries(x.riseTally)
                                   .filter(([k]) => k !== "falling"))) : null;
  const run = (side, fid, sd, wire) => {
    const m = side === 1 ? new AC.Match(fid, "angelus", sd) : new AC.Match("angelus", fid, sd);
    const f = side === 1 ? m.b : m.a, foe = side === 1 ? m.a : m.b;
    const FP = Object.getPrototypeOf(m.a), oA = FP.apply;
    const calls = [], other = [], heals = [], ends = [], floors = [], hitsT = [], arr = [];
    let step = 0, inR = 0, inM = 0, n = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      if (MINE(kind, p)) calls.push({ step, t: m.t, k: p.w, n: p.n === undefined ? null : p.n, inR: !!inR,
                                      inM: !!inM, x: f.x, y: f.y, alive: f.alive, keys: Object.keys(p).join(",") });
      else { other.push([step, kind, JSON.stringify(p || {})]); if (kind === "hit") hitsT.push(m.t); }
      return op.call(this, kind, p); };
    /* instrumentation only: every blessing tickRise lands on the caster, logged after it lands */
    FP.apply = function(k, nn, s){ const r = oA.call(this, k, nn, s);
      if (k === "blessing" && this === f && inR) heals.push([step, this.stacks("blessing"), nn, s]);
      return r; };
    P.tickRise = function(dt){
      const Z = f.ultRise;
      inR++; try { return (wire ? pR : oR).call(this, dt); }
      finally { inR--;
        if (Z && !f.ultRise) ends.push([step, (Z.t >= Z.dur && f.alive) ? (foe.alive ? "clock" : "clock-foe-dead")
                                                                         : "death", m.t]); } };
    /* the floor contact, read off the bounce's own spawnFx call and the clamped y */
    P.move = function(ff, fo, dt){
      if (ff !== f) return (wire ? pM : oM).call(this, ff, fo, dt);
      let bounce = 0; const own = Object.prototype.hasOwnProperty.call(this, "spawnFx"), osp = this.spawnFx;
      this.spawnFx = function(x, y, c, k, v, l, s){
        if (k === 3 && v === 90 && l === 0.3 && s === 2 && x === ff.x && y === ff.y) bounce++;
        return osp.call(this, x, y, c, k, v, l, s); };
      inM++;
      try { return (wire ? pM : oM).call(this, ff, fo, dt); }
      finally { inM--; if (own) this.spawnFx = osp; else delete this.spawnFx;
        const hiY = CF.arena.h - this.inset - CF.physics.ballR;
        if (bounce && ff.y >= hiY) floors.push([step, ff.alive, m.t, ff.x]); } };
    let arrivals = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const T = f.riseTally;
        if (T && T.arrivals > arrivals){ arrivals = T.arrivals; arr.push(m.t); }
      }
    } finally { P.tickRise = oR; P.move = oM; FP.apply = oA; if (had) S.play = op; else delete S.play; }
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, m.a.vx, m.a.vy, m.b.vx,
                                  m.b.vy, m.a.stun, m.b.stun, m.a.stacks("blessing"), m.b.stacks("blessing"),
                                  m.a.stacks("smite"), m.b.stacks("smite"), m.a.hits, m.b.hits,
                                  m.winner ? m.winner.w.id : null, RT(m.a), RT(m.b)]),
             rt: f.riseTally ? JSON.stringify(f.riseTally) : null, rtNoFall: RT(f),
             falling: f.riseTally ? f.riseTally.falling : undefined,
             calls, other: JSON.stringify(other), heals, ends, floors, hitsT, arr, openAtOver: !!f.ultRise,
             over: m.over, t: m.t };
  };
  let fights = 0, same = 0, otherSame = 0, rtOnlyFalling = 0; const diff = [], bad = [];
  const endsN = { clock: 0, "clock-foe-dead": 0, death: 0, over: 0 };
  let casts = 0, castV = 0, heals = 0, taps = 0, closes = 0, lands = 0, wantLands = 0, unlanded = 0;
  const ns = [], tapDelay = [], fall = [], straight = [], arrive = [], clips = [], perWin = [];
  const pairs = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds) pairs.push([side, fid, sd]);
  let mirrorN = 0;
  if (mirror) for (const sd of seeds) pairs.push([2, "angelus", sd]);
  for (const [side, fid, sd] of pairs){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.rt === B.rtNoFall) rtOnlyFalling++;
    if (A.calls.some(c => c.k !== "angelus")) bad.push([fid, sd, "the UNPATCHED run played a new voice"]);
    for (const c of B.calls){
      if (c.k === "angelus-shaft" && !c.inR) bad.push([fid, sd, "a tap outside tickRise"]);
      if (c.k === "angelus-close" && !c.inR) bad.push([fid, sd, "a close outside tickRise"]);
      if (c.k === "angelus-land" && !c.inM) bad.push([fid, sd, "a landing outside move"]);
      if (c.k !== "angelus" && c.keys !== "w" && c.keys !== "w,n") bad.push([fid, sd, "opts", c.keys]);
    }
    if (side === 2){ mirrorN++; continue; }
    /* the windows: cast (the bare id fireUlt plays) -> end */
    const cv = B.calls.filter(c => c.k === "angelus");
    castV += cv.length;
    const W = cv.map((c, i) => ({ castStep: c.step, cast: c.t, end: null, endStep: null, endT: null, taps: 0 }));
    for (const e of B.ends){ const w = [...W].reverse().find(w => w.castStep <= e[0] && w.end === null);
      if (w){ w.end = e[1]; w.endStep = e[0]; w.endT = e[2]; } }
    for (const w of W){ if (w.end === null) w.end = "over"; endsN[w.end]++; casts++; }
    if (B.openAtOver !== (W.length > 0 && W[W.length - 1].end === "over")) bad.push([fid, sd, "open at over"]);
    /* the heals: one tap per heal, on its step, carrying the count after it */
    const tp = B.calls.filter(c => c.k === "angelus-shaft");
    heals += B.heals.length; taps += tp.length;
    if (tp.length !== B.heals.length) bad.push([fid, sd, "taps vs heals", tp.length, B.heals.length]);
    for (let i = 0; i < Math.min(tp.length, B.heals.length); i++){
      const c = tp[i], h = B.heals[i];
      if (c.step !== h[0]) bad.push([fid, sd, "a tap off its heal's step", c.step, h[0]]);
      if (c.n !== h[1]) bad.push([fid, sd, "the tap's count is not the caster's after the heal", c.n, h[1]]);
      if (typeof c.n !== "number" || c.n < 1 || c.n > 5) bad.push([fid, sd, "tap count out of range", c.n]);
      ns.push(c.n);
      const lh = B.hitsT.filter(x => x <= c.t); if (lh.length) tapDelay.push(c.t - lh[lh.length - 1]);
      const w = [...W].reverse().find(w => w.castStep <= c.step); if (w) w.taps++;
    }
    /* the closes: one per clock close with both alive, on its step; none otherwise */
    const cl = B.calls.filter(c => c.k === "angelus-close");
    closes += cl.length;
    const want = B.ends.filter(e => e[1] === "clock");
    if (cl.length !== want.length || cl.some((c, i) => c.step !== want[i][0]))
      bad.push([fid, sd, "closes vs clock closes", cl.length, want.length]);
    /* the landings: the first floor contact (caster alive) after each clock close, before the next cast */
    const ld = B.calls.filter(c => c.k === "angelus-land");
    lands += ld.length;
    const exp = [];
    for (const e of want){
      const nextCast = cv.find(c => c.step > e[0]);
      const fl = B.floors.find(x => x[0] > e[0] && x[1] && (!nextCast || x[0] < nextCast.step));
      if (fl) exp.push([fl[0], e[2], fl[2], fl[3]]); else unlanded++;
    }
    wantLands += exp.length;
    if (ld.length !== exp.length || ld.some((c, i) => c.step !== exp[i][0]))
      bad.push([fid, sd, "landings vs first floor contacts", ld.length, exp.length]);
    for (const x of exp){ fall.push(x[2] - x[1]); if (Math.abs(x[3] - 260) < 1e-9) straight.push(x[2] - x[1]); }
    for (const a of B.arr){ const c = [...cv].reverse().find(c => c.t <= a); if (c) arrive.push(a - c.t); }
    for (const w of W) perWin.push(w.taps);
    /* a real window for the ear: a clock close whose landing comes within 1.2 s, the fight going on after */
    for (const w of W){
      if (w.end !== "clock") continue;
      const x = exp.find(x => Math.abs(x[1] - w.endT) < 1e-9);
      if (x && x[2] - x[1] <= 1.2 && B.t - x[2] > 1.5)
        clips.push([side, fid, sd, w.cast, w.endT, x[2], w.taps]);
    }
    if (B.falling === 1 && !B.over) bad.push([fid, sd, "falling left set in a fight that did not end"]);
  }
  return { fights, same, otherSame, rtOnlyFalling, diff: diff.slice(0, 4), ends: endsN, casts, castV, heals, taps,
           closes, lands, wantLands, unlanded, ns, tapDelay, fall, straight, arrive, clips, perWin, mirrorN,
           bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Ascension's.
RECORD_JS = r"""([side, fid, sd, riseRows, landRow]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const oR = P.tickRise, oM = P.move;
  let sR = oR.toString(); for (const [a, c] of riseRows) sR = sR.replace(a, () => c);
  const pR = (0, eval)("(function " + sR + ")");
  const pM = (0, eval)("(function " + oM.toString().replace(landRow[0], () => landRow[1]) + ")");
  const m = side ? new AC.Match(fid, "angelus", sd) : new AC.Match("angelus", fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && q.w.startsWith("angelus")) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickRise = pR; P.move = pM;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickRise = oR; P.move = oM; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# main-thread cost of one candidate body (a cast of three re-struck voices is hundreds of `_tone` calls)
BODY_COST_JS = r"""([body, p, reps]) => {
  const proto = Object.getPrototypeOf(AC.SFX);
  const fn = (0, eval)("(function(t, p){\n" + body + "\n})");
  const oc = new OfflineAudioContext(1, 48000 * 4, 48000);
  const S = Object.create(proto); S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = oc.createBuffer(1, 28800, 48000);
  const v = [];
  for (let i = 0; i < reps; i++){ const a = performance.now(); fn.call(S, 0, p); v.push(performance.now() - a); }
  return v.slice().sort((x, y) => x - y)[v.length >> 1];
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
  for (const [k, kind, p] of [["cast", "ult", { w: "angelus" }], ["tap", "ult", { w: "angelus-shaft", n: 3 }],
                              ["close", "ult", { w: "angelus-close" }], ["land", "ult", { w: "angelus-land" }],
                              ["hit", "hit", { dmg: 9, crit: false }]]){
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


def noise_part(draws, a, b):
    """The noise-built part of a voice over [a, b] s after the event, re the
    whole voice there (dB): renders of one text on two noise draws differ by
    exactly the part built from the noise buffer, so (x1 - x2) / sqrt 2 is it
    (portcullis_voice_lab's STONE method), the median over six disjoint pairs.
    A voice of sines alone reads the render floor (-180)."""
    np = _np()
    i0, i1 = int((T0 + a) * SR), int((T0 + b) * SR)
    out = []
    for i in range(0, len(draws) - 1, 2):
        n = (draws[i] - draws[i + 1])[i0:i1] / math.sqrt(2)
        rn = _rms(n)
        out.append(db(rn / max(_rms(draws[i][i0:i1]), 1e-12)) if rn > 1e-9 else -180.0)
    return float(np.median(out))


def peak_amp(x, f, a, b, within=40.0):
    """The spectral peak within `within` cents of f over [a, b] s (absolute),
    Hann-windowed and zero-padded: a tone's own level, clear of a neighbour a
    whole tone away (a third-octave band is not -- see WHAT THE FIRST CUT GOT
    WRONG)."""
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    m = (fr >= f * 2 ** (-within / 1200)) & (fr <= f * 2 ** (within / 1200))
    return float(X[m].max())


def chord_at(x, freqs, a, b):
    """Each tone of a chord over [a, b] s (absolute): its FFT peak within 6% of
    it (cents off) and its third-octave RMS."""
    return [(cents(pitch(x, a, b, lo=f / 1.06, hi=f * 1.06), f), band_rms(x, f, a, b)) for f in freqs]


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v74 §6.2 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.6s': AUDIBLE 510-690 ms; 'a swell': SWELL (the loudest 50 ms re the "
    "loudest in the first 100 ms) +8..+16 dB and no DIPS on the way up (one "
    "swell); 'the rise': the loudest 50 ms centred 330-530 ms after the cast "
    "-- the swell crests where the rise arrives (0.08 s of the cast's hit "
    "stop + the 0.35 s rise; measured in the fights below); 'three ... tones "
    "a fifth and octave apart', 'a chord': over the 150 ms before the crest "
    "each of D4, A4 and D5 is sounding -- its FFT peak within 30 cents and its "
    "third-octave within 12 dB of the loudest of the three; 're-struck': "
    "FLUTTER <= 3 dB over the swell (at the chord's own period, D3); heard: "
    "over those 150 ms every tone's third-octave >= the score's p90 there, "
    "the loudest >= 2x. Register against rune-crack, the seal (the game's "
    "other stack of fifths), the sanctified and twinblade casts with a voice "
    "of their own, the death voice and the hit @ 9 each <= 0.80. Level: TOP "
    "between 0.5x the hit @ 9's loudest 50 ms on its LOUDEST draw and 1.0x on "
    "its QUIETEST (heard like a blow, never over one). Tiebreak: the lowest "
    "worst register (to 0.05), then the fewest synth calls, then the order "
    "listed.")

TAP_RULE = (
    "At EVERY count 1-5: '70ms': AUDIBLE 55-85 ms; 'a tap': RISE <= 3 ms and "
    "the peak in the first 10 ms; 'bright': the centroid >= 2000 Hz; 'glassy': "
    "pure (the noise part <= -30 dB re the whole) and ringing in inharmonic "
    "modes (the strongest peak 1.5x-4x the note >= 60 cents from every whole "
    "multiple, within 20 dB); 'quiet': the loudest 50 ms <= 0.5x the shaft "
    "blow's (the hit @ 3.6) on its quietest draw and >= 2x the wall tick's on "
    "its loudest; 'blessing count in the pitch': each count's note within 30 "
    "cents of its declared degree, and every step n -> n + 1 >= 150 cents up; "
    "heard: at count 1 the note's third-octave over 0-70 ms >= 2x the score's "
    "p90 there. Register (the worst count) against the heal chime (the spark "
    "collect, n 1-5), Zenith's tick (n 0-4), the wall tick, hex-snap, the "
    "hit @ 3.6 and the picked cast each <= 0.80. Tiebreak: the lowest worst "
    "register (to 0.05), then the fewest calls, then the order listed.")

CLOSE_RULE = (
    "'the chord': over 20-70 ms its tones are the cast's chord (D4, A4, D5: "
    "each within 30 cents, within 12 dB of the loudest); 'resolving down': "
    "over 300-450 ms its tones are the score's tonic below it (A3, E4, A4: "
    "each within 30 cents, within 12 dB of the loudest), and D4 and D5 -- the "
    "chord's tones the tonic does not share -- are gone there (each one's "
    "spectral peak within 40 cents, Hann-windowed, >= 12 dB under the "
    "tonic's loudest); the root lower than the cast's; '0.6s' (the "
    "cast's length, declared): AUDIBLE 510-690 ms; level: its loudest 50 ms "
    "<= the cast's and >= 2x the wall tick's loudest; heard: over 300-450 ms "
    "the tonic's loudest tone >= 2x the score's p90 there. Register against "
    "the seal, the death voice, rune-crack and the hit @ 9 each <= 0.80 (the "
    "cast's is printed, not gated: it IS the cast's chord). Tiebreak: the "
    "lowest worst register (to 0.05), then the fewest calls, then the order "
    "listed.")

LAND_RULE = (
    "'a ... thud': RISE <= 5 ms and the peak in the first 20 ms (a landing is "
    "struck); AUDIBLE 60-180 ms (short: not a boom); LOW: >= 0.60 of its "
    "power under 250 Hz; DULL: the centroid <= 400 Hz (no crack, no ring on "
    "top); level: TOP between 2x the wall tick's loudest 50 ms (the tick it "
    "lands over) and 1.0x the hit @ 9's on its quietest draw (never over a "
    "blow); heard: its loudest third-octave under 250 Hz over 0-80 ms >= 2x "
    "the score's p90 there (the bass and the drum live there). Register "
    "against the hit @ 9 ('the ball's', not a blow), the death voice, the "
    "wall tick and the clank each <= 0.80 (the score's drum is printed). "
    "Tiebreak: the lowest worst register (to 0.05), then the fewest calls, "
    "then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 510 <= M["aud"] <= 690: why.append(f"audible {M['aud']:.0f} ms, not 510-690")
    if not 8 <= M["swell"] <= 16: why.append(f"swell {M['swell']:+.1f} dB, not +8..+16")
    if M["dips"]: why.append(f"{M['dips']} dips on the way up")
    if not 0.330 <= M["top_at"] <= 0.530: why.append(f"crest at {M['top_at'] * 1000:.0f} ms, not 330-530")
    for (c_, b_), f_ in zip(M["chord"], M["want"]):
        if abs(c_) > 30: why.append(f"{note_name(f_)} {c_:+.0f} c off")
        if db(b_ / max(bb for _, bb in M["chord"])) < -12: why.append(f"{note_name(f_)} "
                                                                     f"{db(b_ / max(bb for _, bb in M['chord'])):+.1f} dB")
    if M["flut"] > 3: why.append(f"flutter {M['flut']:.1f} dB > 3")
    fl = lev["floors"]
    for (c_, b_), f_, fl_ in zip(M["chord"], M["want"], fl):
        if b_ < fl_ / 2: why.append(f"{note_name(f_)} under the score ({b_:.4f} < {fl_ / 2:.4f})")
    lb = max(range(3), key=lambda i: M["chord"][i][1])
    if M["chord"][lb][1] < fl[lb]: why.append(f"the loudest tone {M['chord'][lb][1]:.4f} < 2x the score "
                                              f"{fl[lb]:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def tap_why(M, lev):
    why = []
    if M["aud_lo"] < 55 or M["aud_hi"] > 85: why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 55-85")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 10: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["cen_lo"] < 2000: why.append(f"centroid {M['cen_lo']:.0f} Hz (not bright)")
    if M["nz"] > -30: why.append(f"not pure: a noise part of {M['nz']:+.1f} dB")
    if M["inh_c"] < 60 or M["inh_db"] < -20:
        why.append(f"not glassy (worst count: {M['inh_c']:.0f} c, {M['inh_db']:+.0f} dB)")
    if M["top_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["note_err"] > 30: why.append(f"a note {M['note_err']:.0f} cents off its degree")
    if M["step_min"] < 150: why.append(f"a step of {M['step_min']:+.0f} cents (< 150)")
    if M["inb"] < M["inb_floor"]: why.append(f"in-band {M['inb']:.4f} < {M['inb_floor']:.4f} (under the score)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    for (c_, b_), f_ in zip(M["c1"], M["w1"]):
        if abs(c_) > 30: why.append(f"starts {note_name(f_)} {c_:+.0f} c off")
        if db(b_ / max(bb for _, bb in M["c1"])) < -12: why.append(f"starts without {note_name(f_)}")
    for (c_, b_), f_ in zip(M["c2"], M["w2"]):
        if abs(c_) > 30: why.append(f"ends {note_name(f_)} {c_:+.0f} c off")
        if db(b_ / max(bb for _, bb in M["c2"])) < -12: why.append(f"ends without {note_name(f_)}")
    if M["gone_db"] > -12: why.append(f"the old chord not gone ({M['gone_db']:+.1f} dB)")
    if not M["down"]: why.append("not down")
    if not 510 <= M["aud"] <= 690: why.append(f"audible {M['aud']:.0f} ms, not 510-690")
    if M["top"] > lev["hi"]: why.append(f"loudest 50 ms {M['top']:.4f} > the cast's {lev['hi']:.4f}")
    if M["top"] < lev["lo"]: why.append(f"loudest 50 ms {M['top']:.4f} < {lev['lo']:.4f}")
    if M["heard"] < 1: why.append(f"the tonic under the score ({db(M['heard']):+.1f} dB re 2x its p90)")
    for k, v in M["regs"].items():
        if k != "cast" and v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def land_why(M, lev):
    why = []
    if M["rise"] > 5: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 20: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if not 60 <= M["aud"] <= 180: why.append(f"audible {M['aud']:.0f} ms, not 60-180")
    if M["low"] < 0.60: why.append(f"low share {M['low']:.2f} < 0.60")
    if M["cen"] > 400: why.append(f"centroid {M['cen']:.0f} Hz > 400 (not dull)")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 1: why.append(f"under the score ({db(M['heard']):+.1f} dB re 2x its p90 at {M['heard_f']:.0f} Hz)")
    for k, v in M["regs"].items():
        if k != "drum" and v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True,
                    help="a link carrying Angelus's stage 5 and none of its voices (v104 ran on the scratch link "
                         "sc-angelus-b9.html, db58100b3aa0092a)")
    ap.add_argument("--out", default="../05-reference/v104")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=104601)
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "tap": TAP_RULE, "close": CLOSE_RULE, "land": LAND_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickRise heal", HEAL_ANCHOR), ("tickRise close", CLOSE_ANCHOR),
                    ("move bounce", LAND_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if '"angelus-shaft"' in html or '"angelus-close"' in html or 'w === "angelus"' in html:
        raise SystemExit(f"{gp.name} already carries Ascension's voices -- run on stage 5")
    if 'u.kind === "rise"' not in html or "tickRise(dt){" not in html:
        raise SystemExit(f"{gp.name} does not carry Angelus's Ascension")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nASCENSION -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        row = page.evaluate("() => { const w = AC.WEAPONS.find(w => w.id === 'angelus'); "
                            "return w ? [w.dmg, w.ult.winDmg, w.ult.healPer, w.ult.dur, w.ult.rise, w.ult.kind, "
                            "w.aff, w.shape, AC.STATUS ? AC.STATUS.blessing.maxStacks : null] : null; }")
        print(f"  the row: dmg {row[0]}, winDmg {row[1]}, healPer {row[2]}, window {row[3]} s, rise {row[4]} s, "
              f"kind {row[5]}, {row[6]} {row[7]}; blessing cap {row[8]}")
        if row[0] != BLADE or row[1] != WIN or row[5] != "rise" or row[4] != 0.35:
            raise SystemExit("the row is not the one this lab was written for (blade 9, winDmg 0.4, rise 0.35)")
        if row[8] not in (None, BLESS_CAP):
            raise SystemExit("the blessing cap is not 5")
        kinds = page.evaluate("() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();"
                              " return [...new Set([...s.matchAll(/kind === \"([a-z-]+)\"/g)].map(m => m[1]))]; }")
        print(f"  THE SYNTH'S KINDS TODAY ({len(kinds)}): {', '.join(kinds)}")
        rec["kinds"] = kinds
        wpn = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape])")

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
        x_fb, _ = R([["play", T0, "ult", {"w": "__no_such_relic__"}]])
        own = {}
        for wid, aff, shp in wpn:
            if wid == RELIC or (aff != "sanctified" and shp != "twinblade"):
                continue
            xw_, _ = R([["play", T0, "ult", {"w": wid}]])
            own[wid] = float(np.abs(xw_ - x_fb).max())
        SCHOOL = tuple(k for k, v in own.items() if v > 1e-6 and dict((w[0], w[1]) for w in wpn)[k] == "sanctified")
        TYPE = tuple(k for k, v in own.items() if v > 1e-6 and dict((w[0], w[2]) for w in wpn)[k] == "twinblade")
        FALL = tuple(k for k, v in own.items() if v <= 1e-6)
        print("  the sanctified and twinblade casts, max |diff| vs the rune-crack fallback: " +
              ", ".join(f"{k} {v:.1e}" for k, v in own.items()))
        print(f"  with a voice of their own -- the school: {', '.join(SCHOOL) or 'none'}; the type: "
              f"{', '.join(TYPE) or 'none'}; rune-crack: {', '.join(FALL) or 'none'}")
        xa0, _ = R([["play", T0, "ult", {"w": RELIC}]])
        now_fb = float(np.abs(xa0 - x_fb).max())
        print(f"  ult/angelus today vs the fallback: max |diff| {now_fb:.1e} -- "
              f"{'it IS rune-crack' if now_fb <= 1e-6 else 'NOT the fallback'}")
        if now_fb > 1e-6:
            raise SystemExit("ult/angelus is not the rune-crack fallback -- this lab was written for a relic with "
                             "no arm")
        rec["own"] = own
        ctl = {}
        REFS = [("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                ("hit@9", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("hit@3.6", ["play", T0, "hit", {"dmg": SHAFT, "crit": False}]),
                ("wall", ["play", T0, "wall", {}]),
                ("death", ["play", T0, "death", {}]),
                ("seal", ["play", T0, "seal", {}]),
                ("clank", ["play", T0, "clank", {"mass": 1.1}]),
                ("hex-snap", ["play", T0, "hex-snap", {}]),
                ("drum", ["body", T0, DRUM_BODY, {}])]
        REFS += [(f"spark{n}", ["play", T0, "spark", {"collect": True, "n": n}]) for n in range(1, 6)]
        REFS += [(f"zt{n}", ["play", T0, "ult", {"w": "morningstar-tick", "n": n}]) for n in range(0, 5)]
        REFS += [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in SCHOOL + TYPE]
        for name, ev in REFS:
            x, _ = R([ev])
            ctl[name] = dict(basic(x), x=x, low=low_share(x))
            M = ctl[name]
            print(f"  {name:<13} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
                  f"loudest 50 ms {M['top']:.4f}   centroid {M['cen']:6.0f} Hz   low {M['low']:.2f}")
        rc_same = float(np.abs(ctl["rune-crack"]["x"] - x_fb).max())
        repro = [("rune-crack peak", ctl["rune-crack"]["peak"], 0.608, 0.01),
                 ("rune-crack audible", ctl["rune-crack"]["aud"], 450, 10),
                 ("hit@11.6 peak", ctl["hit@11.6"]["peak"], 0.443, 0.01),
                 ("hit@11.6 audible", ctl["hit@11.6"]["aud"], 80, 10)]
        bad = [f"{n}: {v:.3f} vs {p_}" for n, v, p_, t_ in repro if abs(v - p_) > t_]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
                                    f"PASS  all {len(repro)} published numbers come back") +
              f"   (ult/spellbreaker IS the fallback: {rc_same:.1e})")
        if bad or rc_same > 1e-6:
            raise SystemExit("the controls do not reproduce -- nothing new is quoted")
        # the noise draws
        D = {k: [] for k in ("hit@9", "hit@3.6", "wall", "rune-crack", "death", "seal", "clank", "hex-snap", "drum")
             + SCHOOL + TYPE + tuple(f"spark{n}" for n in range(1, 6)) + tuple(f"zt{n}" for n in range(5))}
        RD = dict(REFS)
        for sd in NOISE_SEEDS:
            for k in D:
                D[k].append(basic(R([RD[k]], seed=sd)[0]))
        h_lo, h_hi = min(m["top"] for m in D["hit@9"]), max(m["top"] for m in D["hit@9"])
        s_lo = min(m["top"] for m in D["hit@3.6"])
        w_hi = max(m["top"] for m in D["wall"])
        print(f"  the hit @ 9 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f};  the shaft's "
              f"blow, the hit @ 3.6: {s_lo:.4f}-{max(m['top'] for m in D['hit@3.6']):.4f};  the wall tick: "
              f"{min(m['top'] for m in D['wall']):.4f}-{w_hi:.4f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]

        def bedp90(f, dur=0.25):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + dur)
                                        for i in range(0, len(bseg) - int(dur * SR), 2400)], 90))

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        def reg_many(DB, keys):
            return max(reg(DB, k) for k in keys)

        rec["levels"] = dict(hit9=[h_lo, h_hi], hit36_lo=s_lo, wall_hi=w_hi)
        wav("angelus-ctl-runecrack.wav", ctl["rune-crack"]["x"])
        wav("angelus-ctl-hit9.wav", ctl["hit@9"]["x"])
        wav("angelus-ctl-seal.wav", ctl["seal"]["x"])
        wav("angelus-ctl-wall.wav", ctl["wall"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_top = math.sqrt(lev_c["lo"] * lev_c["hi"])
        want_c = [D4 * r for r, _ in CHORD]
        lev_c["floors"] = [2 * bedp90(f_, 0.15) for f_ in want_c]
        print(f"\nCAST -- 'a choir swell (three re-struck tones a fifth and octave apart, 0.6s) -- the one voice in "
              f"the game allowed to be a chord'. D4 A4 D5. Level-matched: TOP {tgt_top:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}), SWELL +{SWELL_DB:g} dB, AUDIBLE {CAST_AUD:g} ms; the score's "
              f"p90 x2 at D4 A4 D5: " + " ".join(f"{v:.4f}" for v in lev_c["floors"]))
        fl0 = [flutter(R([["body", T0, f'this._tone(t, {{ freq: {fmt(f_)}, gain: 0.02, dur: 3, type:"sine" }})'
                                        f'.frequency.value = {fmt(f_)};', {}]])[0], T0 + 0.35, T0 + 0.95, D4 / 2)
               for f_ in (D4, D4 * 1.5)]
        print(f"  FLUTTER's floor, one steady sine strike at D4 / A4 (read at D3's period): "
              f"{fl0[0]:.2f} / {fl0[1]:.2f} dB")
        if max(fl0) > 0.5:
            raise SystemExit("the flutter metric reads a steady tone as flutter -- nothing it says is usable")
        rec["flutter_floor"] = fl0

        def cx(sp, g, sw, D_, seed=None, **kw):
            return R([["body", T0, cast_body(sp, g, sw, D_, **kw), {}]], seed=seed)

        def calib_cast(sp):
            g, sw, D_ = 0.02, SWELL_DB, 0.2
            for _ in range(4):
                lo_, hi_ = math.log(0.04), math.log(1.5)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, sw, math.exp(mid))[0])["aud"] < CAST_AUD: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                M = basic(cx(sp, g, sw, D_)[0])
                g = g * tgt_top / M["top"]
                sw = sw + (SWELL_DB - (db(M["top"]) - db(M["start"])))
            return float(f"{g:.4g}"), round(sw, 2), D_

        CAST_REGS = ("rune-crack", "seal") + SCHOOL + TYPE + ("death", "hit@9")

        def cast_measure(sp, g, sw, D_, name, **kw):
            x, calls = cx(sp, g, sw, D_, **kw)
            x2, _ = cx(sp, g, sw, D_, **kw)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, sw=sw, D=D_, name=name, sp=sp, want=want_c)
            M["swell"] = db(M["top"]) - db(M["start"])
            M["dips"], M["lin"] = dips_and_lin(x, M["top_at"])
            a_, b_ = T0 + M["top_at"] - 0.15, T0 + M["top_at"]
            M["chord"] = chord_at(x, want_c, max(T0 + 0.02, a_), b_)
            M["flut"] = flutter(x, T0 + 0.12, T0 + max(0.2, min(M["top_at"], CREST) - 0.03), D4 / 2)
            DB = [bands(x[int(T0 * SR):])] * len(NOISE_SEEDS)      # sines only: every draw is this one
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in CAST_REGS}
            M["why"] = cast_why(M, lev_c)
            return M

        H_ = (f"  {'cand':<10}{'g':>8}{'sw':>6}{'D':>6}{'calls':>6}{'top':>8}{'at':>5}{'aud':>5}{'swl':>6}{'dip':>4}"
              f"{'flut':>5}  {'D4 c/dB':>9}{'A4 c/dB':>9}{'D5 c/dB':>9}{'inb D4/A4/D5':>23}"
              + "".join(f"{k[:5]:>6}" for k in CAST_REGS))
        print(H_)

        def cast_line(M):
            r_ = M["regs"]; mx = max(b for _, b in M["chord"])
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['sw']:>6.2f}{M['D']:>6.3g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['top_at'] * 1000:>5.0f}{M['aud']:>5.0f}{M['swell']:>6.1f}{M['dips']:>4d}{M['flut']:>5.1f}  "
                  + "".join(f"{c_:>+4.0f}/{db(b_ / mx):<+4.0f}" for c_, b_ in M["chord"])
                  + " " + "/".join(f"{b_:.4f}" for _, b_ in M["chord"])
                  + "".join(f"{r_[k]:>6.2f}" for k in CAST_REGS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, sw, D_ = calib_cast(sp)
            M = cast_measure(sp, g, sw, D_, name)
            M["ms"] = page.evaluate(BODY_COST_JS, [cast_body(sp, g, sw, D_), {}, 20])
            rows_c.append(M); cast_line(M)
            wav(f"angelus-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        s0 = rows_c[0]
        for name, kw in (("0 STRUCK", dict(struck=True)), ("0 DYAD", dict(drop=[2.0])),
                         ("0 OFFBEAT", dict(offbeat=True))):
            M = cast_measure(s0["sp"], s0["g"], s0["sw"], s0["D"], name, **kw)
            ctlc.append(M); cast_line(M)
            wav(f"angelus-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        # RAW is a REFERENCE, not a control (see WHAT THE FIRST CUT GOT WRONG): printed with its distance
        raw = cast_measure(s0["sp"], s0["g"], s0["sw"], s0["D"], "  RAW", fix=False)
        cast_line(raw)
        raw_d = float(np.abs(raw["x"] - s0["x"]).max())
        rec["raw_ref"] = dict(max_diff=raw_d, top_db=db(raw["top"] / s0["top"]), flut=raw["flut"], why=raw["why"])
        rcm = dict(basic(xa0), x=xa0, calls=5, g=0, sw=0, D=0, name="0 RC-NOW", sp=None, want=want_c)
        rcm["swell"] = db(rcm["top"]) - db(rcm["start"])
        rcm["dips"], rcm["lin"] = dips_and_lin(xa0, rcm["top_at"])
        rcm["chord"] = chord_at(xa0, want_c, T0 + max(0.02, rcm["top_at"] - 0.15), T0 + max(0.17, rcm["top_at"]))
        rcm["flut"] = flutter(xa0, T0 + 0.12, T0 + 0.4, D4 / 2)
        rcd = [bands(R([["play", T0, "ult", {"w": RELIC}]], seed=sd)[0][int(T0 * SR):]) for sd in NOISE_SEEDS]
        rcm["DB"] = rcd
        rcm["regs"] = {k: reg(rcd, k) for k in CAST_REGS}
        rcm["why"] = cast_why(rcm, lev_c)
        ctlc.append(rcm); cast_line(rcm)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 STRUCK   PURE's chord struck once, no re-strike, no swell -- a control\n"
              "    0 DYAD     PURE without its octave: two tones, not three -- a control\n"
              "    0 OFFBEAT  PURE with its strikes a flat 11 ms apart, not whole cycles: out of phase -- a control\n"
              "      RAW      PURE without `.frequency.value = f` (v97's toolkit finding) -- a REFERENCE\n"
              "    0 RC-NOW   what ult/angelus plays today (rune-crack) -- a control")
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
        print(f"  RAW (a reference): max |diff| vs PURE {raw_d:.4f}, its crest {db(raw['top'] / s0['top']):+.2f} dB "
              f"re PURE's, flutter {raw['flut']:.1f} dB -- "
              + ("it passes every gate, as it did in the first table: at D4-D5 and an 11 ms spacing the phase slip "
                 "is not a thing the rules can hear; the arms set the line anyway" if not raw["why"]
                 else "it fails: " + "; ".join(raw["why"][:3])))
        print("  main-thread cost of one call (median of 20; printed, not gated): " +
              ", ".join(f"{M['name'].split()[1]} {M['ms']:.1f} ms ({M['calls']} calls)" for M in rows_c))
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, sw {C_['sw']}, D {C_['D']}; {C_['calls']} synth calls; TOP "
              f"{C_['top']:.4f} = {db(C_['top'] / h_lo):+.1f} dB re the hit @ 9 (quietest draw), "
              f"{db(C_['top'] / w_hi):+.1f} dB re the wall; crest at {C_['top_at'] * 1000:.0f} ms")

        # ---- THE TAP -------------------------------------------------------
        lev_t = dict(lo=2 * w_hi, hi=0.5 * s_lo)
        tgt_t = math.sqrt(lev_t["lo"] * lev_t["hi"])
        print(f"\nTAP -- 'a bright glassy tap, 70ms, quiet; blessing count in the pitch'. Level-matched: loudest 50 ms "
              f"{tgt_t:.4f} at count 3 (the centre of {lev_t['lo']:.4f}-{lev_t['hi']:.4f}), AUDIBLE {TAP_AUD:g} ms "
              f"at count 3")

        def tx(sp, g, D_, n, seed=None):
            return R([["body", T0, tap_body(sp, g, D_), {"n": n}]], seed=seed)

        def calib_tap(sp, aud=TAP_AUD):
            g, D_ = 0.05, 0.1
            for _ in range(4):
                lo_, hi_ = math.log(0.01), math.log(1.5)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(tx(sp, g, math.exp(mid), 3)[0])["aud"] < aud: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = g * tgt_t / basic(tx(sp, g, D_, 3)[0])["top"]
            return float(f"{g:.4g}"), D_

        TREG = ("spark", "zenith-tick", "wall", "hex-snap", "hit@3.6", "cast")
        SPARKS = tuple(f"spark{n}" for n in range(1, 6))
        ZTS = tuple(f"zt{n}" for n in range(5))

        def tap_measure(sp, g, D_, name):
            M = dict(name=name, sp=sp, g=g, D=D_)
            notes = []; auds = []; rises = []; pkms = []; tops = []; cens = []; inhc = []; inhd = []; nzs = []
            regs = {k: 0.0 for k in TREG}
            xs = {}
            want = tap_notes(sp)
            for n in range(1, 6):
                x, calls = tx(sp, g, D_, n)
                if float(np.abs(x - tx(sp, g, D_, n)[0]).max()) > TOL:
                    raise SystemExit(f"tap {name} does not reproduce")
                xs[n] = x
                b_ = basic(x)
                auds.append(b_["aud"]); rises.append(b_["rise"]); pkms.append(b_["pk_ms"]); cens.append(b_["cen"])
                draws = [tx(sp, g, D_, n, seed=sd)[0] for sd in NOISE_SEEDS]
                tops.append(max(basic(d_)["top"] for d_ in draws)); tops.append(min(basic(d_)["top"] for d_ in draws))
                nzs.append(noise_part(draws, 0.0, 0.07))
                f_ = pitch(x, T0 + 0.002, T0 + 0.05, lo=500, hi=9000) if not sp.get("tick") else want[n - 1]
                notes.append(f_)
                r_, c_, d_ = inharm(x, T0 + 0.002, T0 + 0.05, f_)
                inhc.append(c_); inhd.append(d_)
                DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
                regs["spark"] = max(regs["spark"], reg_many(DB, SPARKS))
                regs["zenith-tick"] = max(regs["zenith-tick"], reg_many(DB, ZTS))
                for k in ("wall", "hex-snap", "hit@3.6"):
                    regs[k] = max(regs[k], reg(DB, k))
                regs["cast"] = max(regs["cast"], float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)])))
                if n == 1:
                    M["inb"] = band_rms(x, f_, T0, T0 + 0.07)
                    M["inb_floor"] = 2 * bedp90(f_, 0.07)
                if n == 3:
                    M["DB"] = DB; M["calls"] = calls[0]
            M["xs"] = xs; M["x"] = xs[3]; M["notes"] = notes
            M["note_err"] = max(abs(cents(f_, w_)) for f_, w_ in zip(notes, want))
            st = [cents(notes[i + 1], notes[i]) for i in range(4)]
            M["step_min"] = min(st)
            M["aud_lo"], M["aud_hi"] = min(auds), max(auds)
            M["rise"] = max(rises); M["pk_ms"] = max(pkms); M["cen_lo"] = min(cens)
            M["top_lo"], M["top_hi"] = min(tops), max(tops); M["top"] = basic(xs[3])["top"]
            M["nz"] = max(nzs); M["inh_c"] = min(inhc); M["inh_db"] = min(inhd)
            M["regs"] = regs
            M["why"] = tap_why(M, lev_t)
            r_ = regs
            print(f"  {name:<9}{g:>8.4g}{D_:>6.3g}{M['calls']:>6d}{M['aud_lo']:>5.0f}-{M['aud_hi']:<4.0f}{M['rise']:>5.0f}"
                  f"{M['pk_ms']:>5.0f}{M['cen_lo']:>6.0f}{M['nz']:>7.1f}{M['inh_c']:>5.0f}{M['inh_db']:>5.0f}"
                  f"{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}{M['note_err']:>5.0f}{M['step_min']:>6.0f}{M['inb']:>8.4f}"
                  + "".join(f"{r_[k]:>6.2f}" for k in TREG))
            return M

        print(f"  {'cand':<9}{'g':>8}{'D':>6}{'calls':>6}{'aud':>10}{'rise':>5}{'pk@':>5}{'cen':>6}{'noise':>7}"
              f"{'inhc':>5}{'inhd':>5}{'top lo':>8}{'top hi':>8}{'err':>5}{'step':>6}{'inb':>8}"
              + "".join(f"{k[:6]:>6}" for k in TREG))
        rows_t = []
        for name, sp, blurb in TAP_CANDIDATES:
            g, D_ = calib_tap(sp)
            M = tap_measure(sp, g, D_, name)
            rows_t.append(M)
            for n in (1, 3, 5):
                wav(f"angelus-tap-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        ctlt = []
        t0_ = [M for M in rows_t if M["name"] == TAP_CTL][0]
        for name, sp, g, D_ in (("0 FLAT", dict(t0_["sp"], flat=True), t0_["g"], t0_["D"]),
                                ("0 LOUD", t0_["sp"], float(f"{t0_['g'] * 2.5:.4g}"), t0_["D"]),
                                ("0 HARM", dict(t0_["sp"], modes="harm"), t0_["g"], t0_["D"]),
                                ("0 LONG", t0_["sp"], t0_["g"], None),
                                ("0 TICK", dict(t0_["sp"], tick=True), None, None)):
            if name == "0 LONG":
                _g, D_ = calib_tap(sp, aud=200.0)
            if name == "0 TICK":
                g, D_ = calib_tap(sp)
            M = tap_measure(sp, g, D_, name)
            ctlt.append(M)
            wav(f"angelus-tap-{name.replace(' ', '-').lower()}-n3.wav", M["xs"][3])
        for (name, _sp, blurb) in TAP_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 FLAT    SKY at count 1's note for every count -- a control\n"
              "    0 LOUD    SKY at 2.5x its gain -- a control\n"
              "    0 HARM    SKY on whole-number partials (1 : 2 : 3) -- a control\n"
              "    0 LONG    SKY ringing 200 ms -- a control\n"
              "    0 TICK    the wall tick's own shape (high-passed noise) at the tap's level -- a control")
        print(f"  RULE  {TAP_RULE}")
        for M in rows_t:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctlt:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_t, "tap")
        ti = fb if ok is None else min(ok, key=lambda i: (round(max(rows_t[i]["regs"].values()) / 0.05),
                                                          rows_t[i]["calls"], i))
        T_ = rows_t[ti]
        print(f"  PICK  {T_['name']}  g {T_['g']}, D {T_['D']}; notes " + " ".join(f"{f_:.0f}" for f_ in T_["notes"])
              + f" Hz at counts 1-5; loudest 50 ms {db(T_['top'] / s_lo):+.1f} dB re the hit @ 3.6, "
              f"{db(T_['top'] / w_hi):+.1f} dB re the wall")

        # ---- THE CLOSE -----------------------------------------------------
        lev_k = dict(lo=2 * w_hi, hi=C_["top"])
        tgt_k = C_["top"] * 10 ** (-CLOSE_UNDER_DB / 20)
        w1 = [D4 * r for r, _ in CHORD]
        print(f"\nCLOSE -- 'the chord resolving down'. The picked cast's chord and voice ({C_['name']}), D4-A4-D5 -> "
              f"A3-E4-A4. Level-matched: loudest 50 ms {tgt_k:.4f} ({CLOSE_UNDER_DB:g} dB under the cast's), "
              f"AUDIBLE {CLOSE_AUD:g} ms")

        def kx(sp, g, D_, seed=None):
            return R([["body", T0, close_body(sp, C_["sp"], g, D_), {}]], seed=seed)

        def calib_close(sp):
            g, D_ = C_["g"], 0.2
            for _ in range(4):
                lo_, hi_ = math.log(0.04), math.log(1.5)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(kx(sp, g, math.exp(mid))[0])["aud"] < CLOSE_AUD: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = g * tgt_k / basic(kx(sp, g, D_)[0])["top"]
            return float(f"{g:.4g}"), D_

        KREG = ("seal", "death", "rune-crack", "hit@9")

        def close_measure(sp, g, D_, name, blurb):
            x, calls = kx(sp, g, D_)
            if float(np.abs(x - kx(sp, g, D_)[0]).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, D=D_, name=name, sp=sp, blurb=blurb)
            F1 = D4 if ("to" in sp and sp["to"] is None) else sp.get("to", A3)
            w2 = [A3 * r for r, _ in CHORD]
            M["w1"], M["w2"] = w1, w2
            M["c1"] = chord_at(x, w1, T0 + 0.02, T0 + 0.07)
            M["c2"] = chord_at(x, w2, T0 + 0.30, T0 + 0.45)
            tp_ = max(peak_amp(x, f_, T0 + 0.30, T0 + 0.45) for f_ in w2)
            M["gone_db"] = max(db(peak_amp(x, f_, T0 + 0.30, T0 + 0.45) / max(tp_, 1e-12)) for f_ in (D4, 2 * D4))
            M["down"] = F1 < D4
            M["heard"] = max(b_ / (2 * bedp90(f_, 0.15)) for (_, b_), f_ in zip(M["c2"], w2))
            DB = [bands(x[int(T0 * SR):])] * len(NOISE_SEEDS)
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in KREG}
            M["regs"]["cast"] = float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)]))
            M["why"] = close_why(M, lev_k)
            return M

        print(f"  {'cand':<10}{'g':>8}{'D':>6}{'calls':>6}{'aud':>5}{'top':>8}{'  D4 A4 D5 at 20-70 ms':>24}"
              f"{'  A3 E4 A4 at 300-450 ms':>26}{'gone':>6}{'heard':>7}" + "".join(f"{k[:5]:>6}" for k in KREG + ("cast",)))

        def close_line(M):
            r_ = M["regs"]; m1 = max(b for _, b in M["c1"]); m2 = max(b for _, b in M["c2"])
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['D']:>6.3g}{M['calls']:>6d}{M['aud']:>5.0f}{M['top']:>8.4f}  "
                  + "".join(f"{c_:>+4.0f}/{db(b_ / m1):<+4.0f}" for c_, b_ in M["c1"]) + "  "
                  + "".join(f"{c_:>+4.0f}/{db(b_ / m2):<+4.0f}" for c_, b_ in M["c2"])
                  + f"{M['gone_db']:>6.1f}{db(M['heard']):>+7.1f}" + "".join(f"{r_[k]:>6.2f}" for k in KREG + ("cast",)))

        rows_k = []
        for name, sp, blurb in CLOSE_CANDIDATES:
            g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name, blurb)
            rows_k.append(M); close_line(M)
            wav(f"angelus-close-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlk = []
        for name, sp, blurb in CLOSE_CONTROLS:
            g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name, blurb)
            ctlk.append(M); close_line(M)
            wav(f"angelus-close-{name.replace(' ', '-').lower()}.wav", M["x"])
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

        # ---- THE LANDING ---------------------------------------------------
        lev_l = dict(lo=2 * w_hi, hi=1.0 * h_lo)
        tgt_l = math.sqrt(lev_l["lo"] * lev_l["hi"])
        print(f"\nLAND -- 'and the ball's landing thud'. The floor contact plays the wall tick; the thud is new. "
              f"Level-matched: TOP {tgt_l:.4f} (the centre of {lev_l['lo']:.4f}-{lev_l['hi']:.4f}), AUDIBLE "
              f"{LAND_AUD:g} ms")

        def lx(sp, g, D_, seed=None):
            return R([["body", T0, land_body(sp, g, D_), {}]], seed=seed)

        def calib_land(sp, aud=LAND_AUD):
            g, D_ = 0.2, 0.15
            for _ in range(4):
                if not sp.get("tick"):
                    lo_, hi_ = math.log(0.02), math.log(1.5)
                    for _ in range(12):
                        mid = 0.5 * (lo_ + hi_)
                        if basic(lx(sp, g, math.exp(mid))[0])["aud"] < aud: lo_ = mid
                        else: hi_ = mid
                    D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = g * tgt_l / basic(lx(sp, g, D_)[0])["top"]
            return float(f"{g:.4g}"), D_

        LREG = ("hit@9", "death", "wall", "clank", "drum")
        LOWB = [f_ for f_ in (50 * 2 ** (k / 3) for k in range(0, 8)) if f_ <= 250]

        def land_measure(fn, calls, g, D_, name, sp, blurb):
            x = fn(None)
            if float(np.abs(x - fn(None)).max()) > TOL:
                raise SystemExit(f"land {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls, g=g, D=D_, name=name, sp=sp, blurb=blurb, low=low_share(x, 250.0))
            draws = [fn(sd) for sd in NOISE_SEEDS]
            tops = [basic(d_)["top"] for d_ in draws]
            M["top_lo"], M["top_hi"] = min(tops), max(tops)
            hb = [(band_rms(x, f_, T0, T0 + 0.08) / (2 * bedp90(f_, 0.08)), f_) for f_ in LOWB]
            M["heard"], M["heard_f"] = max(hb)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in LREG}
            M["why"] = land_why(M, lev_l)
            r_ = M["regs"]
            print(f"  {name:<9}{g:>8.4g}{D_:>6.3g}{calls:>6d}{M['rise']:>5.0f}{M['pk_ms']:>5.0f}{M['aud']:>5.0f}"
                  f"{M['low']:>6.2f}{M['cen']:>6.0f}{M['top']:>8.4f}{db(M['heard']):>+7.1f}@{M['heard_f']:<4.0f}"
                  + "".join(f"{r_[k]:>6.2f}" for k in LREG))
            return M

        print(f"  {'cand':<9}{'g':>8}{'D':>6}{'calls':>6}{'rise':>5}{'pk@':>5}{'aud':>5}{'low':>6}{'cen':>6}{'top':>8}"
              f"{'heard dB@Hz':>13}" + "".join(f"{k[:6]:>6}" for k in LREG))
        rows_l = []
        for name, sp, blurb in LAND_CANDIDATES:
            g, D_ = calib_land(sp)
            calls = lx(sp, g, D_)[1][0]
            M = land_measure(lambda sd, sp=sp, g=g, D_=D_: lx(sp, g, D_, seed=sd)[0], calls, g, D_, name, sp, blurb)
            rows_l.append(M)
            wav(f"angelus-land-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctll = []
        l0 = rows_l[0]
        for name, sp in (("0 WALL", dict(tick=True)), ("0 BOOM", l0["sp"]), ("0 RING", dict(ring=True))):
            if name == "0 BOOM":
                g, D_ = calib_land(sp, aud=450.0)
            elif name == "0 RING":
                g, D_ = calib_land(dict(ring=True), aud=300.0)
            else:
                g, D_ = calib_land(sp)
            calls = lx(sp, g, D_)[1][0]
            M = land_measure(lambda sd, sp=sp, g=g, D_=D_: lx(sp, g, D_, seed=sd)[0], calls, g, D_, name, sp, "")
            ctll.append(M)
            wav(f"angelus-land-{name.replace(' ', '-').lower()}.wav", M["x"])
        M = land_measure(lambda sd: R([["play", T0, "hit", {"dmg": BLADE, "crit": False}]], seed=sd)[0], 2, 0, 0,
                         "0 HIT", None, "")
        ctll.append(M)
        for (name, _sp, blurb) in LAND_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 WALL    the wall tick's own shape at the thud's level -- a control\n"
              "    0 BOOM    BODY decaying over 450 ms -- a control\n"
              "    0 RING    a held 110 Hz sine, 300 ms -- a control\n"
              "    0 HIT     the engine's own blow at 9, played as the thud -- a control")
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
        ok, fb = _gate(rows_l, "land")
        li = fb if ok is None else min(ok, key=lambda i: (round(max(v for k, v in rows_l[i]["regs"].items()
                                                                    if k != "drum") / 0.05),
                                                          rows_l[i]["calls"], i))
        L_ = rows_l[li]
        print(f"  PICK  {L_['name']}  g {L_['g']}, D {L_['D']}; TOP {db(L_['top'] / h_lo):+.1f} dB re the hit @ 9, "
              f"{db(L_['top'] / w_hi):+.1f} dB re the wall")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   tap {T_['name']}   close {K_['name']}   land {L_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        info = dict(c_top=db(C_["top"] / h_lo), c_reg=max(C_["regs"].values()), c_regw=who(C_["regs"]),
                    t_db=db(T_["top"] / s_lo), t_wall=db(T_["top"] / w_hi), t_reg=max(T_["regs"].values()),
                    t_regw=who(T_["regs"]), k_db=db(K_["top"] / C_["top"]),
                    k_reg=max(v for k, v in K_["regs"].items() if k != "cast"),
                    k_regw=who({k: v for k, v in K_["regs"].items() if k != "cast"}),
                    l_db=db(L_["top"] / h_lo), l_reg=max(v for k, v in L_["regs"].items() if k != "drum"),
                    l_regw=who({k: v for k, v in L_["regs"].items() if k != "drum"}),
                    n_cast=len(CAST_CANDIDATES), n_tap=len(TAP_CANDIDATES), n_close=len(CLOSE_CANDIDATES),
                    n_land=len(LAND_CANDIDATES))
        arms = arms_code(C_, T_, K_, L_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        if arms.count(SFX_ANCHOR) != 1 or not arms.endswith(SFX_ANCHOR):
            raise SystemExit("the Sfx row does not re-emit its anchor exactly once, last")
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        tbt = tap_body(T_["sp"], T_["g"], T_["D"])
        rp = [float(np.abs(R([["body", T0, tbt, {"n": 5}]])[0] - R([["body", T0, tbt, {"n": 5}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the loudest tap rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        xa, _ = R([["arm", T0, "ult", {"w": RELIC}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa - C_["x"]).max())))
        for n in (-1, 0, 1, 2, 3, 4, 5, 7, None):
            p_ = {"w": "angelus-shaft"} if n is None else {"w": "angelus-shaft", "n": n}
            x1, _ = R([["arm", T0, "ult", p_]], rows=sfx_rows)
            x2, _ = R([["body", T0, tbt, {"n": min(BLESS_CAP, max(1, n or 0))}]])
            chk.append((f"tap@{n}", float(np.abs(x1 - x2).max())))
        xk, _ = R([["arm", T0, "ult", {"w": "angelus-close"}]], rows=sfx_rows)
        chk.append(("close", float(np.abs(xk - K_["x"]).max())))
        xl, _ = R([["arm", T0, "ult", {"w": "angelus-land"}]], rows=sfx_rows)
        chk.append(("land", float(np.abs(xl - L_["x"]).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (3.6, 9, 11.6, 23, 50) for c_ in (False, True)]
        others += [("hit", {"dmg": 9, "crit": False, "bough": 0.38}),
                   ("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("clank", {"mass": 1.1}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("aegis", {"n": 10, "back": 5}), ("aegis", {"broke": True}),
                   ("vine", {"plant": True}), ("vine", {"coil": True}), ("vine", {"miss": True}), ("vine", {"n": 2}),
                   ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}), ("fork", {}),
                   ("scour-hold", {"n": 3}), ("scour-tick", {"n": 2}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        others += [(k_, {}) for k_ in kinds if k_ not in {o[0] for o in others} and k_ != "ult"]
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
              f"weights x crit and the bough, spark x3, wall, death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, "
              f"loose x3, fork, scour x4, every other kind, and {len(ult_ids)} ult ids -- every relic's cast and "
              f"every sub-voice the ult arm names): worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa - x_fb).max())
        print(f"  ult/angelus vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, repro=max(rp))

        # ---- THE tickRise AND move ROWS --------------------------------------
        seeds = [a.seed0 + k for k in range(a.seeds)]
        mirror = page.evaluate("() => { try { new AC.Match('angelus', 'angelus', 1); return true; } "
                               "catch (e) { return false; } }")
        print("\nTHE tickRise AND move ROWS, applied to their prototypes' own source, run beside the originals on "
              f"real fights (the mirror match {'included' if mirror else 'refused by Match -- not run'}):")
        rise_rows = [[HEAL_ANCHOR, HEAL_CODE], [CLOSE_ANCHOR, CLOSE_CODE]]
        WR = page.evaluate(WIRE_JS, [seeds, rise_rows, [LAND_ANCHOR, LAND_CODE], mirror])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Angelus both sides x every foe x seeds {seeds}"
              f"{' + the mirror' if mirror else ''}): {WR['same']}/{WR['fights']} identical (over, clock, both hp, "
              f"positions, velocities, stuns, both blessing and smite counts, both blow ledgers, winner, both "
              f"riseTallies but `falling`); every other voice call identical in order, kind and opts in "
              f"{WR['otherSame']}/{WR['fights']}; the caster's riseTally differs by `falling` alone in "
              f"{WR['rtOnlyFalling']}/{WR['fights']}")
        ns = np.array(WR["ns"]) if WR["ns"] else np.zeros(1)
        hist = {int(k): int((ns == k).sum()) for k in range(1, 6)}
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['heals']} shaft hits "
              f"healed -> {WR['taps']} taps; {WR['ends']['clock']} clock closes with both alive -> {WR['closes']} "
              f"closes; {WR['wantLands']} landings after them -> {WR['lands']} thuds ({WR['unlanded']} fights ended "
              f"before the ball landed); problems {WR['nbad']}")
        print("  the count a tap carries: " + ", ".join(f"{k}: {v}" for k, v in hist.items() if v) +
              f"; taps a window: median {np.median(WR['perWin']) if WR['perWin'] else 0:.0f}, "
              f"max {max(WR['perWin']) if WR['perWin'] else 0}")

        def q5(v):
            v = sorted(v)
            return "/".join(f"{v[int(p_ * (len(v) - 1))]:.2f}" for p_ in (0, 0.25, 0.5, 0.75, 1)) if v else "-"
        print(f"  the tap after its shaft blow's own hit voice, s (min/q1/median/q3/max): {q5(WR['tapDelay'])}")
        print(f"  the arrival after the cast voice, s: {q5(WR['arrive'])}  (the cast's crest is centred at "
              f"{C_['top_at']:.2f} s)")
        print(f"  the landing after the close, s: {q5(WR['fall'])}; {len(WR['straight'])} of {len(WR['fall'])} fall "
              f"straight to the floor under the hang point ({q5(WR['straight'])}), the rest are knocked on the way down")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["taps"] != WR["heals"] or WR["closes"] != WR["ends"]["clock"] or WR["lands"] != WR["wantLands"] \
                or WR["heals"] == 0 or WR["castV"] != WR["casts"] or WR["ends"]["clock"] == 0 or WR["lands"] == 0 \
                or WR["rtOnlyFalling"] != WR["fights"]:
            FAILED.append("sim rows")
        WB = page.evaluate(WIRE_JS, [seeds, [[HEAL_ANCHOR, HEAL_CODE_BAD], [CLOSE_ANCHOR, CLOSE_CODE]],
                                     [LAND_ANCHOR, LAND_CODE], False])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a tap): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "rtOnlyFalling", "ends", "casts", "castV",
                                          "heals", "taps", "closes", "lands", "wantLands", "unlanded", "mirrorN",
                                          "nbad")}
        rec["wire"].update(control_same=WB["same"], count_hist=hist, tap_delay=q5(WR["tapDelay"]),
                           arrive=q5(WR["arrive"]), fall=q5(WR["fall"]), straight=[len(WR["straight"]),
                                                                                   len(WR["fall"])])
        print(f"  THE CLOSE ON A DEATH: {WR['ends']['death']} windows closed by a death (in a kill flight), "
              f"{WR['ends']['clock-foe-dead']} by the clock on the step the foe died, and {WR['ends']['over']} still "
              f"open at the fight's end play no close and no thud (checked above); those endings belong to the death "
              f"voice.")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        clips = sorted(WR["clips"], key=lambda c: -c[6])
        if not clips:
            FAILED.append("no clip: no clock close with a landing within 1.2 s")
        else:
            cside, cf, cs, c0, c1, c2, ntap = clips[0]
            EV = page.evaluate(RECORD_JS, [cside, cf, cs, rise_rows, [LAND_ANCHOR, LAND_CODE]])
            assert not errors, errors[:3]
            lo_t, hi_t = c0 - 1.0, c2 + 1.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            NEW = ("angelus-shaft", "angelus-close", "angelus-land")
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if e[3] not in NEW]
            nocast = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            xn, _ = R(nocast, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd; xn = xn + bd

            def ov(xa_, xb_, f, a_, d_):
                return db(band_rms(xa_, f, a_, a_ + d_) / max(band_rms(xb_, f, a_, a_ + d_), 1e-12))
            tn = tap_notes(T_["sp"])
            tp = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == "angelus-shaft"]
            tp_over = [ov(xw, xo, tn[min(5, max(1, n_)) - 1], t_, 0.07) for t_, n_ in tp]
            ca_t = T0 + (c0 - lo_t)
            ca_parts = [(ov(xo, xn, f_, ca_t + C_["top_at"] - 0.15, 0.15), f_) for f_ in want_c]
            cl_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "angelus-close"]
            cl_parts = [[(ov(xw, xo, f_, t_ + 0.30, 0.15), f_) for f_ in (A3, A3 * 1.5, A3 * 2)] for t_ in cl_t]
            ld_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "angelus-land"]
            # the thud is read as its isolation gate reads it: at its BEST third-octave under 250 Hz. The two
            # readings the first cut tried are printed beside it (see WHAT THE FIRST CUT GOT WRONG).
            ld_bands = [[(ov(xw, xo, f_, t_, 0.08), f_) for f_ in LOWB] for t_ in ld_t]
            ld_over = [max(B_)[0] for B_ in ld_bands]
            ld_band = [ov(xw, xo, L_["heard_f"], t_, 0.08) for t_ in ld_t]

            def lowpow(x_, a_, d_):
                """RMS over [a_, a_ + d_] of x_ band-passed 40-500 Hz by FFT."""
                seg = x_[int(a_ * SR):int((a_ + d_) * SR)]
                X = np.fft.rfft(seg); fr = np.fft.rfftfreq(len(seg), 1 / SR)
                return math.sqrt(2 * float((np.abs(X[(fr >= 40) & (fr < 500)]) ** 2).sum())) / len(seg)
            ld_pow = [db(lowpow(xw, t_, 0.08) / max(lowpow(xo, t_, 0.08), 1e-12)) for t_ in ld_t]
            print(f"\nIN A REAL WINDOW -- angelus v {cf} (side {'AB'[cside]}), seed {cs}, cast at {c0:.2f}s, closed by "
                  f"its clock at {c1:.2f}s, landed at {c2:.2f}s, {len(tp)} shaft hits healed (counts "
                  f"{' '.join(str(n_) for _, n_ in tp)}); the fight's own sounds and the score, with and without the "
                  f"new voices")
            print("  each tap over the fight in its own third-octave, 0-70 ms: " +
                  " ".join(f"{v:+.1f}" for v in tp_over) + " dB")
            print("  the cast's chord over the fight without it, the 150 ms before its crest: " +
                  " / ".join(f"{v:+.1f} @ {note_name(f_)}" for v, f_ in ca_parts) + " dB")
            print("  the close's tonic over the fight, 300-450 ms: " +
                  " | ".join(" / ".join(f"{v:+.1f} @ {note_name(f_)}" for v, f_ in P_) for P_ in cl_parts) + " dB")
            print("  the thud over the fight (its wall tick included) at its best third-octave under 250 Hz, 0-80 ms: " +
                  " ".join(f"{max(B_)[0]:+.1f} @ {max(B_)[1]:.0f} Hz" for B_ in ld_bands) + " dB  (every band: " +
                  " | ".join(" ".join(f"{v:+.1f}@{f_:.0f}" for v, f_ in B_) for B_ in ld_bands) + ")")
            print(f"    the two readings the first cut tried: its {L_['heard_f']:.0f} Hz third-octave alone " +
                  " ".join(f"{v:+.1f}" for v in ld_band) + " dB (the score's A2 bass shares that band: a phase "
                  "reading), and the power 40-500 Hz " + " ".join(f"{v:+.1f}" for v in ld_pow) +
                  " dB (the score's A1 bass carries most of that power and the ear little of it)")
            if not tp_over or min(tp_over) < 6 or max(v for v, _ in ca_parts) < 3 or not cl_parts \
                    or max(v for v, _ in cl_parts[0]) < 3 or not ld_over or min(ld_over) < 3:
                FAILED.append("a new voice not heard in a real window")
            wav("angelus-pick-real-window.wav", xw)
            wav("angelus-pick-real-window-without.wav", xo)
            rec["real"] = dict(clip=[cside, cf, cs], cast=c0, close=c1, land=c2, taps=tp, tap_over=tp_over,
                               cast_parts=ca_parts, close_parts=cl_parts, land_over=ld_over, land_bands=ld_bands,
                               land_100=ld_band, land_pow=ld_pow)
        # the four picks in order, for the ear: the cast, five shaft hits (the blow, then its tap 67 ms on) at
        # counts 1-5, the close, and the landing over its wall tick
        seq = [["arm", T0, "ult", {"w": RELIC}]]
        for k_, n_ in enumerate((1, 2, 3, 4, 5)):
            seq += [["arm", T0 + 0.9 + 0.4 * k_, "hit", {"dmg": SHAFT, "crit": False}],
                    ["arm", T0 + 0.9 + 0.4 * k_ + 0.067, "ult", {"w": "angelus-shaft", "n": n_}]]
        seq += [["arm", T0 + 3.2, "ult", {"w": "angelus-close"}],
                ["arm", T0 + 4.1, "ult", {"w": "angelus-land"}], ["arm", T0 + 4.1, "wall", {}]]
        xq_, _ = R(seq, secs=6.5, rows=sfx_rows)
        wav("angelus-pick-sequence.wav", xq_)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), tap=strip(rows_t), tap_controls=strip(ctlt),
               close=strip(rows_k), close_controls=strip(ctlk), land=strip(rows_l), land_controls=strip(ctll),
               wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_sw": C_["sw"], "cast_D": C_["D"],
                     "tap": T_["name"], "tap_g": T_["g"], "tap_D": T_["D"],
                     "close": K_["name"], "close_g": K_["g"], "close_D": K_["D"],
                     "land": L_["name"], "land_g": L_["g"], "land_D": L_["D"]})
    print(f"\nTHE PICKS  cast {C_['name']}   tap {T_['name']}   close {K_['name']}   land {L_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    AC_ = rec["arm_check"]
    wi = rec["wire"]
    whys = [
        f"v74 §6.2's voices -- the rise's choir swell, the shaft hit's glassy tap pitched by the blessing count, the "
        f"close's chord resolving down -- and the landing thud §6.2 names, which the engine did not have (it plays "
        f"only its wall tick on a floor contact). Code's picks on the numbers under Rick's 'you pick i overrule': cast "
        f"{C_['name']}, tap {T_['name']}, close {K_['name']}, land {L_['name']} (angelus_voice_lab.py). Through the "
        f"patched play() each arm reproduces its lab candidate to {max(v for _, v in AC_['chk']):.0e}; "
        f"{len(AC_['others'])} other voices unchanged (worst {max(v for _, v in AC_['others']):.0e}); ult/angelus is "
        f"no longer rune-crack ({AC_['now_rc']:.2f}). Arms added BEFORE the shared rune-crack fallback; that line is "
        f"re-emitted unchanged, last. Presentation only: play() returns on its first line headless.",
        f"The tap, at the heal's own step, after the blessing lands: {wi['taps']} taps == {wi['heals']} shaft hits "
        f"healed over {wi['fights']} fights, each carrying the caster's blessing count after the heal (1..5). Fights "
        f"identical {wi['same']}/{wi['fights']} and every other voice call identical {wi['otherSame']}/{wi['fights']} "
        f"with the rows applied; the rows plus one sim write come back identical in only "
        f"{wi['control_same']}/{wi['fights']}.",
        f"The close chord only when the window closes by its clock with both alive ({wi['closes']} closes == "
        f"{wi['ends']['clock']} such closes); none for the {wi['ends']['death']} death closes, the "
        f"{wi['ends']['clock-foe-dead']} clock closes on the step the foe died, or the {wi['ends']['over']} windows "
        f"still open at the fight's end (stage 5's reading 10: tickRise never runs again, the death voice has that "
        f"moment, the picture closes the shafts). It sets `falling` on riseTally, which the simulation never reads "
        f"(the caster's riseTally differs by `falling` alone in {wi['rtOnlyFalling']}/{wi['fights']}).",
        f"The thud on the first floor contact after a clock close, the caster alive: {wi['lands']} thuds == "
        f"{wi['wantLands']} such landings; {wi['unlanded']} fights end before the ball lands. Mode `after`, so the "
        f"row's code is only what it adds: its anchor is the bounce's own spawnFx line, which it does not repeat."]
    rows = [dict(label="Sfx: Angelus's cast, shaft-hit, close and landing arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms, why=whys[0]),
            dict(label="tickRise: the shaft-hit tap, once per shaft hit healed, after its blessing, carrying the count",
                 anchor=HEAL_ANCHOR, mode="replace", code=HEAL_CODE, why=whys[1]),
            dict(label="tickRise: the close, when the window closes by its clock with both alive; the drop is marked",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE, why=whys[2]),
            dict(label="move: the landing thud, on the first floor contact after a clock close, the caster alive",
                 anchor=LAND_ANCHOR, mode="after", code=LAND_CODE[len(LAND_ANCHOR):], why=whys[3])]
    for r_ in rows:
        if html.count(r_["anchor"]) != 1:
            raise SystemExit(f"row '{r_['label']}': the anchor is not unique")
        if (r_["mode"] == "replace" and r_["code"].count(r_["anchor"]) != 1) or \
                (r_["mode"] == "after" and r_["anchor"] in r_["code"]):
            raise SystemExit(f"row '{r_['label']}': a replace must re-emit its anchor once, an after must not")
        if any(b_ in re.sub(r"//[^\n]*", "", re.sub(r"/\*[\s\S]*?\*/", "", r_["code"]))
               for b_ in ("rng()", "spawnFx", "Math.random", "ultFx")):
            raise SystemExit(f"row '{r_['label']}': its code names rng, spawnFx, Math.random or ultFx")
    # the rows as text, the orchestrator's way, must give the page the checks above ran on
    one_ = {"replace": lambda s, a_, c_: s.replace(a_, c_, 1), "after": lambda s, a_, c_: s.replace(a_, a_ + c_, 1)}
    t_rows = html
    for r_ in rows:
        t_rows = one_[r_["mode"]](t_rows, r_["anchor"], r_["code"])
    t_pairs = html
    for a_, c_ in [[SFX_ANCHOR, arms], [HEAL_ANCHOR, HEAL_CODE], [CLOSE_ANCHOR, CLOSE_CODE], [LAND_ANCHOR, LAND_CODE]]:
        t_pairs = t_pairs.replace(a_, c_, 1)
    if t_rows != t_pairs:
        raise SystemExit("the rows as text do not give the page the rows were checked as")
    rec["patched_sha"] = hashlib.sha256(t_rows.encode()).hexdigest()[:16]
    print(f"\nTHE ROWS AS TEXT: {len(rows)} rows ({', '.join(r_['mode'] for r_ in rows)}) give {gp.name} + "
          f"{len(t_rows) - len(html)} chars, sha256[:16] {rec['patched_sha']} -- the page the checks above ran on")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The four rows are the edits; all four were applied "
          "to the page's own code above.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
