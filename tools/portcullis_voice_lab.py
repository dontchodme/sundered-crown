#!/usr/bin/env python3
"""ONSLAUGHT'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v100.

    python portcullis_voice_lab.py --game ../02-chain/sc-tendril-t3.html --rows rows.json

v72 §7.2 SOUND, every word of it: "Cast: a metal-on-stone clang and a low hum
settling, 0.4s. A slam: a heavy gated thud (share below 120 Hz >= 0.45,
<= 0.25s), louder with the shield (peak 0.35 -> 0.65 across 0 -> 90). A bank:
the ward's existing bank voice, reused. Close: plates falling -- three short
clinks." The brief's stage 6: "picture, voice, carry per design §7". Rick, for
the batch's art and sound: "you pick i overrule". So this lab does not offer a
spread -- it renders three to five candidates a voice beside CONTROLS that can
come back wrong, prints the numbers each pick is made on, and PICKS by a rule
written in this file (`*_RULE`, `*_why`). He overrules from one clip.

THE WARD HAS NO BANK VOICE. §7.2 says to reuse "the ward's existing bank
voice"; there is none. The synth's kinds are hit, nova, clank, scour-*, ult,
hex-snap, seal, death, loose, fork, spark, aegis, vine and wall, and nothing
plays when a ward banks: resolveHit's vigil branch banks 0.55 of every vigil
blow in silence, and a ward that breaks plays the ordinary `hit` (a crit)
from inside `hurt`. The nearest thing, `spark {collect}`, is the SANCTIFIED
school's heal chime (Daybreak, Zenith). So this lab MAKES one -- `ward-bank`,
the ward's own kind (as v88 made `hex-snap` the runic school's own kind rather
than an Axiom sub-voice) -- and says so. It is played here ONLY by Onslaught's
bank. Giving it to the vigil branch's bank as well would change the sound of
every vigil relic's fights, and no doc asks for that: flagged, not done.

THE FOUR EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/portcullis`, which `fireUlt` plays for every relic.
         Portcullis has NO arm today: it falls through to the shared
         rune-crack (so do Lightkeeper, Farwarden and Bindweed -- measured
         below, to 1e-6). The arms go BEFORE that fallback; the fallback line
         is re-emitted unchanged, so a later relic's row anchored on it still
         applies.
  slam   `ult/portcullis-slam {shield}` from `tickRam`, right after
         `T.slams++;` -- on the slam's own frame, carrying the shield the ball
         brings INTO the slam (the one the slam hits for, 0.25 x shield,
         before the bank). A slam at no shield is still a slam (it knocks
         and banks), so it still thuds, at the quiet end.
  bank   `ward-bank` from `tickRam`, after the bank's three writes: once per
         bank, and every slam banks (the brief: "Slams = banks, asserted") --
         so the bank voice lands on the slam's frame, on top of the thud. At
         the cap the bank adds nothing but still restarts the ward's clock;
         it still sounds (counted below).
  close  `ult/portcullis-close` from `tickRam` on the frame the window runs out
         BY ITS CLOCK with the caster alive -- never on a death, never once
         the fight is over (step() stops calling the tickers). The line goes
         BEFORE the window's own close line, which is re-emitted unchanged.

THE CONTROLS, and what each one is for:
  rune-crack   what Portcullis's cast plays TODAY; v88 published 0.608 /
               450 ms -- reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@23       Portcullis's own blow (blade 23, stage 5): the level every
               voice is judged against, on its quietest / loudest noise draw
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   the vigil casts with a voice of their own -- Bulwarden, Vesper,
               Starwarden (Lightkeeper and Farwarden ARE rune-crack)
  the type     the flail casts -- Gravemourn, Slagheart, Threshmaw, Paradox,
               Morningstar (Bindweed IS rune-crack)
  clank        the weapons' own clash (mass 3.6, the flail's): the one metal
               voice in a fight; the cast must not read as a parry
  death        the heaviest low voice in the game: the slam must not be one
  spark        `spark {collect:true, n:3}`: the sanctified bank chime -- the
               ward's bank must not be the blessing's
  shatter      `hit {crit}` at 20: what a ward breaking sounds like today --
               the ward's bank must not sound like the ward breaking
  hex-snap     the batch's other small bright voice
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  BELL, NOHUM, CLANG   the cast without its stone / without its hum / the
               stone and the hum without the clang: each must fail its gate
  HELD         the cast's hum held flat and cut at 0.4 s: must fail 'settling'
  RC-NOW       what `ult/portcullis` plays today, measured as a cast: must fail
  PLAIN, LONG, FLAT    the slam as a plain decaying thud / gated at 0.35 s /
               at one level for every shield: each must fail its gate
  SPARK, LONG  the spark collect itself played as the bank / a bank that
               rings 0.5 s: each must fail its gate
  TWO, RING, TINK, LATE    two clinks / clinks that ring 0.3 s / plain sine
               clinks / three clinks spread over 0.46 s: each must fail its
               gate

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
    TOL = 1e-5 (-100 dB; REPRO, the same text rendered twice, is printed:
    1.2e-7 on the picks, and once 1.25e-6 on the loudest slam through the
    compressor, so 1e-6 is the render floor, not a tolerance). There is no
    second transcription to get wrong.
  * The shared measures are zenith_voice_lab's and ironwood_voice_lab's,
    imported unchanged (E50 = 50 ms RMS at a 5 ms hop; TOP = the loudest 50
    ms; PEAK = the sample peak; AUDIBLE = first to last 5 ms RMS window above
    2% of the voice's own loudest; GONE = where it ends; RISE = 10 -> 90% of
    the 1 ms envelope; REG = cosine of 1/3-octave band amplitudes, 25 Hz-16
    kHz, the median over noise draws; IN-BAND = RMS inside the third-octave
    round a pitch; PITCH = FFT peak, Hann, zero-padded, parabolic; LOW = the
    share of the power below 120 Hz, the whole render from t = 1.0 -- the
    spec's own number; WOODY's inharmonic-mode test, here called METAL).
  * GATED = a sound that holds and is then cut, not one that dies away: HOLD
    = the span of the 5 ms RMS within 6 dB of its own loudest window, as a
    share of AUDIBLE; CUT = ms from the last window within 6 dB to the end of
    AUDIBLE. A plain thud decays through -6 dB in a fifth of its length and
    takes most of it to fall the rest (the PLAIN control).
  * STONE = the cast's dry impact. The stone is the only part of a cast built
    from the noise buffer, so two renders on two noise draws differ by
    exactly it (and the compressor's reaction to it): the NOISE PART of a
    pair is (x1 - x2) / sqrt 2, the median over six disjoint pairs of the
    twelve draws. STONE = its RMS over 0-40 ms re the whole voice's there
    (dB); DRY = its RMS over 60-120 ms re its own 0-40 ms (dB: a stone does
    not ring); DULL = its power centroid over 0-40 ms (Hz: a thunk, not a
    hiss). The BELL control (no stone) reads -146 dB.
  * CLANG = the cast's metal: its note (the FFT peak, 150 Hz-4 kHz, first 60
    ms) and METAL (the strongest peak between 1.5x and 4x the note is >= 60
    cents from every whole multiple of it and within 20 dB of it: a struck
    bar or plate, not a string), RING (the note's third-octave in 100-150 ms
    is within 20 dB of 0-50 ms: a clang rings, a thunk does not) and LEADS
    (that third-octave over 0-50 ms within 10 dB of the whole voice's RMS
    there: the clang is the loud thing, not a partial of the hum).
  * HUM = the band under 150 Hz (FFT low-pass): TAIL-LOW = its share of the
    power in the last 150 ms of AUDIBLE (what is left at the end is the
    hum); SETTLE = its E50 at 300 ms against its own loudest (dB) and its
    largest rise after that loudest (dB) -- a hum settling falls and never
    swells again.
  * ONSETS = peaks of the 1 ms RMS at least 40 ms apart and at least 0.25 of
    the loudest, in time order.
  * OVER-SLAM = how far the bank lifts its own third-octave (its spectral
    peak) over the slam it lands on: the bank and the loudest slam (shield
    90) rendered on one frame against the slam alone, 0-80 ms, dB.
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's gain puts TOP at the centre of its window, its hum sits
    6 dB under its clang (each alone, loudest 50 ms), its stone reads STONE
    -9 dB and the hum's decay is solved so the voice is AUDIBLE 400 ms; the
    slam's gain is a quadratic in
    the shield solved so PEAK is exactly 0.35 / 0.50 / 0.65 at 0 / 45 / 90;
    the bank's and the close's gains put their loudest 50 ms at the centre
    of theirs, and each clink's decay is solved to 50 ms audible. Constants
    are rounded BEFORE any measured render, so a shipped arm is bit-for-bit
    what was measured.

THE DECLARED CHOICES (not candidates -- words of §7.2 turned into numbers):
  * THE STONE (every cast candidate): a lowpass noise burst at 600 Hz, 60 ms
    -- the dry thunk of iron landing on stone, which does not ring.
  * THE HUM (every cast candidate): the score's tonic, a triangle at A2 (110
    Hz) over a sine at A1 (55 Hz) at 0.5, one strike decaying -- it settles
    into silence rather than being cut.
  * THE CLANG'S NOTE: E4 (329.6 Hz), the score's fifth; LOW an octave down.
  * THE SLAM'S BODY: A1 (55 Hz), the score's root (TOM: E2, its fifth);
    every held tone has `.frequency.value = f` set (v97's toolkit finding:
    without it a strike's phase is not where it was scheduled) and is
    stopped at a WHOLE number of cycles (0.2 s = 11 of 55 Hz, 22 of 110 Hz;
    TOM 16 of 82.41 Hz), so the gate cuts on a zero crossing. Every slam
    carries a 150 -> 55 Hz punch (50 ms) and a 1.8 kHz contact click (20
    ms). The shield in the opts is clamped to 0..90 (the ward's cap).
  * THE SLAM'S SHIELD is the one the ball carries INTO the slam, read on the
    line after `T.slams++` -- the shield this slam hits for (0.25 x it),
    before the bank adds 8. The picture floats the same number.
  * THE CLINK (every close candidate): a small plate -- modes 1 : 1.59 :
    2.14 at 1 : 0.6 : 0.4, sines -- struck, its decay solved to 50 ms.
  * THE CLOSE INSIDE THE PICTURE'S FALL: every candidate's third clink lands
    by 0.25 s (§7.1: "the plates crack and fall ... 0.3s").

THE PICKS, on Chromium 151.0.7922.34, sc-tendril-t3 5a6216e3b629fad4, fight
seeds 100601-100602 (148 fights):

  cast   1 BAR     a 600 Hz stone thunk, an iron bar struck on E4 (triangles on
                   1 : 2.76 : 5.40) and the A2/A1 hum settling: audible 400 ms,
                   METAL (2.76x, 147 c off a harmonic), RING -10.2 dB, LEADS
                   -2.6 dB, STONE -9.0 dB (DRY -33.7, DULL 458 Hz), TAIL-LOW
                   0.85, the hum -17.2 dB at 300 ms; TOP -2.7 dB re the hit @ 23,
                   +18.9 re the wall; register at most 0.71 (Paradox; 0.37
                   against rune-crack, 0.35 the clank). GRILLE ties it on
                   register and loses on calls (9); PLATE (0.73), CLANK (0.74)
                   and LOW (0.79) lose the register tiebreak.
  slam   4 TOM     a held E2 sine and E3 triangle cut at 16 cycles (0.194 s),
                   peak 0.350 / 0.427 / 0.500 / 0.574 / 0.650 at shield 0 /
                   22.5 / 45 / 67.5 / 90 (worst draw 0.011 off the line), LOW
                   0.84, gone 200 ms, HOLD 0.95, CUT 10 ms; register at most
                   0.40 (the hit, the death voice). SINE passes and loses the
                   register tiebreak (0.50 against the cast, whose hum is A);
                   NOISE out (0.046 off the peak line on a noise draw); STACK
                   out (a 30 ms cut: a re-strike decays, it is not gated).
  bank   1 LATCH   (the ward's NEW voice, `ward-bank`) C7 then E7 35 ms apart,
                   each a struck tick with a bar mode: audible 65 ms, +13.9 dB
                   over the loudest slam in its band, -9.3 dB re the hit @ 23,
                   +12.3 re the wall; register at most 0.48 (hex-snap), 0.21
                   against the spark collect. CHARGE passes and loses the
                   register tiebreak (0.59 against rune-crack); PLATE out (0.82
                   against the spark collect -- the blessing's chime); SHIMMER
                   out (+7.1 dB over the slam, 0.87 against hex-snap).
  close  1 FALL    three plates, E6 / D6 / C6 at 0 / 0.10 / 0.23 s, each audible
                   50 ms, -9.3 dB re the hit @ 23, +12.3 re the wall; register at
                   most 0.65 (rune-crack). BOUNCE and SCATTER pass and tie it on
                   register (to 0.05) and calls; FALL is the one that falls.

  In play (148 fights, 528 windows -- 439 closed by the clock, 16 by the
  caster's death, 73 by the fight's end): 2058 slams and 2058 slam voices, each
  on its slam's step carrying the shield it hit for (38% at 0; median 8.6, p90
  48.2); 2058 banks and 2058 bank voices (23 at the cap); 439 closes, none on a
  death or a fight's end; 148/148 fights identical and every other voice call
  identical in order, kind and opts; the sim-write control 3/148. In a real
  window (v Thornwake, 100602, 9 slams) every slam stands +7.5..+57.7 dB, every
  bank +19.7..+48.1 dB and the close +31.1 dB over the fight and the score in
  their own third-octaves. Main-thread cost a call, at the headless timer's
  0.1 ms resolution, over two runs: cast 0.2 ms, slam 0.1-0.2, bank 0.1, close
  0.2-0.3 (the hit's own 0.1). The mirror match is refused by Match, so there
  is none to run. Applied AS TEXT to a copy of the tip (a scratch end-to-end,
  one browser at a time, seed 100701): the page loads clean, its own play
  renders the four voices to the lab's text (<= 1.2e-7) and 26 others to the
  original page's, and 74/74 fights are identical.

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table; that table showed three instruments that could not
see what they were built to see and one declared constant nothing could hear.
Each was changed ONCE, for the reason given, before the picks:
  * STONE was first "the share of the attack's power in third-octaves that
    fall >= 20 dB by 60 ms", and the BELL control (no stone) read 0.11
    against the candidates' 0.10: a bar's fast 5.40 mode is "dry" by that
    definition. It is now the noise part of a draw pair (BELL -146 dB).
  * The CLANG control (the stone and the hum, no clang) passed METAL and
    RING on the hum's own triangle harmonics -- 5:3 is inharmonic to the
    3rd -- so LEADS was added (it reads -10.3 dB there); and the note band
    started at 250 Hz, which read LOW's E3 by its 2.76 mode (now 150 Hz).
  * SETTLE's "rise after the peak" read the silence after the voice (the
    FFT low-pass's floor, +32 dB); it is now read inside AUDIBLE only.
  * THE STONE ITSELF, first 420 Hz / 50 ms at 0.9 of the clang's gain, read
    STONE -16 dB (under every candidate's -12 dB gate): it is now 600 Hz /
    60 ms and level-matched to -9 dB.
  * The close's tiebreak ended on the list's order: three candidates tie on
    register to 0.05 and on calls. A third key from §7.2's own word was
    added: the one whose clinks FALL (each lower than the last).
  * The reproduction tolerance was 1e-6, and two renders of one loud slam
    text once differed by 1.25e-6 through the compressor: TOL is 1e-5.

THE BANK AT THE CAP: every slam banks (the brief's "Slams = banks"), and at
the cap the bank adds nothing but still restarts the ward's clock; its voice
still sounds (23 of 2058 banks). A reading, declared; Rick's to overrule.

WHAT IS FLAGGED, NOT DONE: `ward-bank` is played only by Onslaught. The vigil
branch's own bank (0.55 of every vigil blow, five shipped relics) stays
silent; giving it the voice would change every vigil relic's fights' sound,
and no doc asks for that.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * both Sfx rows (the three ult arms before the rune-crack fallback; the
    `ward-bank` kind before hex-snap) are applied to `Sfx.prototype.play`'s
    own source and rendered: each arm, and the slam at ten shields (-3 and
    120 clamped), must reproduce its candidate to TOL; every other voice
    through the patched play (every relic's cast and every sub-voice the ult
    arm names -- 91 ids --, the hit at five weights with and without a crit,
    spark x3, wall, death, clank x2, seal, nova, hex-snap, aegis x2, vine x4,
    loose x3, fork, scour x4: 125) must be unchanged; `ult/portcullis` must NOT be
    rune-crack any more;
  * the three tickRam rows are applied to `Match.prototype.tickRam`'s own
    source and run on real fights beside the unpatched one: every fight
    identical (over, clock, both hp, both shields, both positions, winner,
    the whole ramTally) and every other voice call identical in order, kind
    and opts; one slam voice per slam on its step, carrying the shield the
    slam hit for (the bank voice then reads it banked, to the cap); one bank
    voice per bank; one close per window closed by its clock with the caster
    alive and none otherwise; the unpatched runs play none of the four. The
    same rows plus ONE sim write (the foe nudged 1e-9 on a slam) must come
    back NOT identical, or "identical" proves nothing. (The Sfx rows cannot
    reach the simulation at all: `play` returns on its first line with no
    audio context, which is every headless run.)
  All anchors must occur exactly once in the game file, and every row is a
  `replace` that re-emits its anchor unchanged exactly once, so a later
  relic's row anchored on the same line (the rune-crack fallback, hex-snap)
  still applies, in either order.

Writes wavs to 05-reference/v100/portcullis-*.wav at RAW level (gitignored).
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
BLADE = 23.0                              # Portcullis's dmg (stage 5)
CAP = 90.0                                # STATUS.ward.cap
SHARE = 0.25                              # w.ult.share
BANK = 8.0                                # w.ult.bank
PK0, PK1 = 0.35, 0.65                     # §7.2: "peak 0.35 -> 0.65 across 0 -> 90"
HUM_UNDER_DB = 6.0                        # the cast's hum under its clang (each alone)
STONE_DB = -9.0                           # the cast's stone, level-matched (STONE)
CAST_AUD = 400.0                          # "0.4s": the hum's decay solved to this
CLINK_AUD = 50.0                          # each clink's decay solved to this
E4, A1, A2 = 329.63, 55.0, 110.0
GATE_S = 0.2                              # the slam's gate: 11 cycles of A1
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)

# =============================================================== THE CAST ===
# "a metal-on-stone clang and a low hum settling, 0.4s". Every candidate
# carries the same declared stone and hum; they differ in what the clang IS.
CAST_CANDIDATES = [
    ("1 BAR", dict(clang="bar", f=E4),
     "an iron bar struck: triangles on E4 and its free-bar modes 2.76 / 5.40 at 0.45 / 0.2"),
    ("2 PLATE", dict(clang="plate", f=E4),
     "an iron plate struck: sines on E4 and its plate modes 1.59 / 2.14 / 2.65 at 0.7 / 0.5 / 0.35"),
    ("3 GRILLE", dict(clang="grille", f=E4),
     "two bars 3% apart (E4 and E4 x 1.03), beating: the grille's bars struck together"),
    ("4 LOW", dict(clang="bar", f=E4 / 2),
     "BAR an octave down (E3): the heavier gate"),
    ("5 CLANK", dict(clang="clank", f=E4),
     "the weapon clank's own partials (1 : 2.41 : 3.83 : 5.17 : 7.02) on E4"),
]
CLANG = {
    "bar": ['for (const [r, k, d] of [[1, 1, 0.55], [2.76, 0.45, 0.4], [5.4, 0.2, 0.25]])',
            '  this._tone(t, { freq: F * r, gain: g * k, dur: d, type:"triangle" });'],
    "plate": ['for (const [r, k, d] of [[1, 1, 0.55], [1.59, 0.7, 0.45], [2.14, 0.5, 0.35], [2.65, 0.35, 0.3]])',
              '  this._tone(t, { freq: F * r, gain: g * k, dur: d, type:"sine" });'],
    "grille": ['for (const b of [1, 1.03]) for (const [r, k, d] of [[1, 0.6, 0.55], [2.76, 0.27, 0.4], [5.4, 0.12, 0.25]])',
               '  this._tone(t, { freq: F * b * r, gain: g * k, dur: d, type:"triangle" });'],
    "clank": ['[1, 2.41, 3.83, 5.17, 7.02].forEach((r, i) =>',
              '  this._tone(t + i * 0.0015, { freq: F * r, gain: g / (i + 1.1), dur: 0.55 - i * 0.06, type:"triangle" }));'],
}


def cast_body(sp, g, kh, dh, ks, part="both", held=False, ind=10):
    """The cast arm's body. `part`: "both" (the arm), "clang" (clang + stone,
    no hum: the NOHUM control and the balance), "hum" (the hum alone: the
    balance), "nostone" (the BELL control), "nocl" (stone + hum: the CLANG
    control). `held`: the hum held flat and cut at 0.4 s (the HELD control)."""
    L = [f"const g = {fmt(g)}, kh = {fmt(kh)}, ks = {fmt(ks)}, F = {fmt(sp['f'])};"]
    if part in ("both", "clang", "nocl"):
        L += ['this._burst(t, { freq: 600, q: 0.8, gain: g * ks, dur: 0.06, type:"lowpass" });']
    if part in ("both", "clang", "nostone"):
        L += CLANG[sp["clang"]]
    if part in ("both", "hum", "nostone", "nocl"):
        if held:
            L += ['const h1 = this._tone(t, { freq: 110, gain: g * kh, dur: 8, type:"triangle" });',
                  'h1.frequency.value = 110; h1.stop(t + 0.4);',
                  'const h2 = this._tone(t, { freq: 55, gain: g * kh * 0.5, dur: 8, type:"sine" });',
                  'h2.frequency.value = 55; h2.stop(t + 0.4);']
        else:
            L += [f'this._tone(t, {{ freq: 110, gain: g * kh, dur: {fmt(dh)}, type:"triangle" }}).frequency.value = 110;',
                  f'this._tone(t, {{ freq: 55, gain: g * kh * 0.5, dur: {fmt(dh)}, type:"sine" }}).frequency.value = 55;']
    return "\n".join(" " * ind + l for l in L)


# =============================================================== THE SLAM ===
# "a heavy gated thud (share below 120 Hz >= 0.45, <= 0.25s), louder with the
# shield (peak 0.35 -> 0.65 across 0 -> 90)". g = A + B u + C u^2, u = the
# shield / 90, solved so PEAK is 0.35 / 0.50 / 0.65 at u = 0 / 0.5 / 1.
SLAM_CANDIDATES = [
    ("1 SINE", dict(body="sine", gate=GATE_S),
     "a held A1 sine and an A2 triangle at 0.5, cut together at 0.2 s; a 150 -> 55 Hz punch and a contact click"),
    ("2 NOISE", dict(body="noise", gate=GATE_S),
     "a held A1 sine and a 300 Hz lowpass noise body at 0.6, cut together at 0.2 s (a gated room); punch and click"),
    ("3 STACK", dict(body="stack", gate=GATE_S),
     "the body RE-STRUCK every two cycles of A1 for 0.2 s (sine + A2 triangle), no stop; punch and click"),
    ("4 TOM", dict(body="tom", gate=16 / 82.41),
     "SINE a fifth up: E2 (82.4 Hz) and E3, cut at 16 cycles (0.194 s)"),
]
SLAM_BODY = {
    "sine": ['const o1 = this._tone(t, { freq: 55, gain: g, dur: 2, type:"sine" });',
             'o1.frequency.value = 55; o1.stop(t + G);',
             'const o2 = this._tone(t, { freq: 110, gain: g * 0.5, dur: 2, type:"triangle" });',
             'o2.frequency.value = 110; o2.stop(t + G);'],
    "noise": ['const o1 = this._tone(t, { freq: 55, gain: g, dur: 2, type:"sine" });',
              'o1.frequency.value = 55; o1.stop(t + G);',
              'this._burst(t, { freq: 300, q: 0.7, gain: g * 0.6, dur: 0.55, type:"lowpass" }).stop(t + G);'],
    "stack": ['for (let s = 0; s < G - 1e-9; s += 2 / 55){',
              '  this._tone(t + s, { freq: 55, gain: g, dur: 0.07, type:"sine" }).frequency.value = 55;',
              '  this._tone(t + s, { freq: 110, gain: g * 0.5, dur: 0.06, type:"triangle" }).frequency.value = 110;',
              '}'],
    "tom": ['const o1 = this._tone(t, { freq: 82.41, gain: g, dur: 2, type:"sine" });',
            'o1.frequency.value = 82.41; o1.stop(t + G);',
            'const o2 = this._tone(t, { freq: 164.81, gain: g * 0.5, dur: 2, type:"triangle" });',
            'o2.frequency.value = 164.81; o2.stop(t + G);'],
    # PLAIN (a control): SINE's body with no gate -- each tone simply decays
    "plain": ['this._tone(t, { freq: 55, gain: g, dur: G, type:"sine" }).frequency.value = 55;',
              'this._tone(t, { freq: 110, gain: g * 0.5, dur: G, type:"triangle" }).frequency.value = 110;'],
}
SLAM_TOP = ['this._tone(t, { freq: 150, to: 55, gain: g * 0.5, dur: 0.05, type:"sine" });',
            'this._burst(t, { freq: 1800, q: 1.2, gain: g * 0.3, dur: 0.02, type:"bandpass" });']


def slam_body(sp, A, B, C, ind=10, flat=None):
    gx = (f"{fmt(A)} + {fmt(B)} * u + {fmt(C)} * u * u" if flat is None else fmt(flat))
    L = [f"const u = clamp((p.shield || 0) / {fmt(CAP)}, 0, 1), g = {gx}, G = {fmt(round(sp['gate'], 6))};"]
    L += SLAM_BODY[sp["body"]] + SLAM_TOP
    return "\n".join(" " * ind + l for l in L)


# =============================================================== THE BANK ===
# None exists; this is the ward's new one. It lands on the slam's frame.
BANK_CANDIDATES = [
    ("1 LATCH", dict(kind="latch"),
     "a latch catching: two quick struck ticks rising a third (C7 then E7, 35 ms apart), each with a bar mode"),
    ("2 CHARGE", dict(kind="charge"),
     "a rising glint: a triangle climbing an octave, E6 -> E7, over 0.12 s, a sine an octave over it"),
    ("3 PLATE", dict(kind="plate"),
     "a small bright plate ping on A6 (plate modes 1 : 1.59 : 2.14), 0.15 s"),
    ("4 SHIMMER", dict(kind="shimmer"),
     "a noise band sweeping up, 1.5 -> 5 kHz over 0.14 s (the ward filling)"),
]
BANK_CONTROLS = [
    ("0 SPARK", None, "the spark collect itself (n 3), played as the bank: the blessing's chime"),
    ("0 LONG", dict(kind="plate-long"), "PLATE ringing 0.5 s"),
]
BANK_BODY = {
    "latch": ['for (const [s, f] of [[0, 2093], [0.035, 2637.02]]){',
              '  this._tone(t + s, { freq: f, gain: g, dur: 0.05, type:"triangle" });',
              '  this._tone(t + s, { freq: f * 2.76, gain: g * 0.3, dur: 0.03, type:"sine" });',
              '}'],
    "charge": ['this._tone(t, { freq: 1318.5, to: 2637, gain: g, dur: 0.12, type:"triangle" });',
               'this._tone(t, { freq: 2637, to: 5274, gain: g * 0.3, dur: 0.1, type:"sine" });'],
    "plate": ['for (const [r, k] of [[1, 1], [1.59, 0.6], [2.14, 0.4]])',
              '  this._tone(t, { freq: 1760 * r, gain: g * k, dur: 0.15, type:"sine" });'],
    "shimmer": ['this._sweep(t, { f0: 1500, f1: 5000, q: 1.2, gain: g, dur: 0.14, atk: 0.07 });'],
    "plate-long": ['for (const [r, k] of [[1, 1], [1.59, 0.6], [2.14, 0.4]])',
                   '  this._tone(t, { freq: 1760 * r, gain: g * k, dur: 0.5, type:"sine" });'],
}


def bank_body(sp, g, ind=8):
    L = [f"const g = {fmt(g)};"] + BANK_BODY[sp["kind"]]
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE CLOSE ===
# "plates falling -- three short clinks". [onset s, freq Hz, level] per clink.
CLOSE_CANDIDATES = [
    ("1 FALL", dict(clinks=[[0, 1318.51, 1], [0.1, 1174.66, 0.9], [0.23, 1046.5, 0.8]], metal=True),
     "three plates, each a step lower (E6, D6, C6: the score's pentatonic down), 0.10 / 0.13 s apart"),
    ("2 BOUNCE", dict(clinks=[[0, 1318.51, 1], [0.14, 1318.51, 0.7], [0.23, 1318.51, 0.5]], metal=True),
     "one plate bouncing to rest: E6 three times, 0.14 / 0.09 s apart, each quieter"),
    ("3 SCATTER", dict(clinks=[[0, 1174.66, 1], [0.08, 1396.91, 0.85], [0.21, 1046.5, 0.9]], metal=True),
     "three plates landing out of order: D6, F6, C6 at 0 / 0.08 / 0.21 s"),
]
CLOSE_CONTROLS = [
    ("0 TWO", dict(clinks=[[0, 1318.51, 1], [0.1, 1174.66, 0.9]], metal=True), "FALL's first two clinks"),
    ("0 RING", dict(clinks=[[0, 1318.51, 1], [0.1, 1174.66, 0.9], [0.23, 1046.5, 0.8]], metal=True, D=0.3),
     "FALL with every clink ringing 0.3 s"),
    ("0 TINK", dict(clinks=[[0, 1318.51, 1], [0.1, 1174.66, 0.9], [0.23, 1046.5, 0.8]], metal=False),
     "FALL with plain sine clinks (no plate modes)"),
    ("0 LATE", dict(clinks=[[0, 1318.51, 1], [0.2, 1174.66, 0.9], [0.46, 1046.5, 0.8]], metal=True),
     "FALL spread over 0.46 s, past the picture's fall"),
]


def close_body(sp, g, D, only=None, ind=10):
    cl = sp["clinks"] if only is None else [sp["clinks"][only]]
    arr = ", ".join(f"[{fmt(s)}, {fmt(f)}, {fmt(k)}]" for s, f, k in cl)
    D = sp.get("D", D)
    L = [f"const g = {fmt(g)}, D = {fmt(D)};",
         f"for (const [s, f, k] of [{arr}])"]
    if sp["metal"]:
        L += ["  for (const [r, m] of [[1, 1], [1.59, 0.6], [2.14, 0.4]])",
              '    this._tone(t + s, { freq: f * r, gain: g * k * m, dur: D, type:"sine" });']
    else:
        L += ['  this._tone(t + s, { freq: f, gain: g * k, dur: D, type:"sine" });']
    return "\n".join(" " * ind + l for l in L)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
KIND_ANCHOR = '      else if (kind === "hex-snap"){'
SLAM_ANCHOR = '      T.slams++;'
BANK_ANCHOR = '        T.banked += f.shield - b0;'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive){ f.ultRam = null; continue; }'

SLAM_CODE = '''      T.slams++;
      /* ONSLAUGHT'S SLAM (v72 §7.2: "a heavy gated thud ..., louder with the
         shield"): on the slam's own frame, carrying the shield the ball
         brings into it -- the one this slam hits for, before the bank. A
         slam at no shield still knocks and banks, so it still thuds, at the
         quiet end. Presentation only: SFX.play draws nothing, is a no-op
         headless, and nothing here is read back (portcullis_voice_lab:
         fights identical). */
      SFX.play("ult", { w: "portcullis-slam", shield: f.shield });'''

BANK_CODE = '''        T.banked += f.shield - b0;
        /* THE WARD'S BANK (v72 §7.2: "the ward's existing bank voice,
           reused" -- the synth had none, so `ward-bank` is new, the ward's
           own kind). Once per bank, and every slam banks; at the cap the
           bank adds nothing but restarts the ward's clock, and still sounds.
           Plain SFX.play; nothing is read back. */
        SFX.play("ward-bank");'''

CLOSE_CODE = '''      /* ONSLAUGHT'S CLOSE (v72 §7.2: "plates falling -- three short
         clinks"): only when the window runs out BY ITS CLOCK with the caster
         alive. A caster's death ends the fight on this frame, and a foe's
         death ends it before any close (step() stops calling this), so both
         endings are left to the death voice, as Zenith's, Daybreak's and
         Canopy's closes are. Plain SFX.play; nothing is read back. */
      if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "portcullis-close" });
''' + CLOSE_ANCHOR

# the sim-write control: the same slam row with the foe nudged 1e-9
SLAM_CODE_BAD = SLAM_CODE.replace(
    '      SFX.play("ult", { w: "portcullis-slam"',
    '      foe.vx += 1e-9;\n      SFX.play("ult", { w: "portcullis-slam"', 1)

_refuse(SLAM_CODE + BANK_CODE + CLOSE_CODE, "sim rows")
for _c, _a in ((SLAM_CODE, SLAM_ANCHOR), (BANK_CODE, BANK_ANCHOR), (CLOSE_CODE, CLOSE_ANCHOR)):
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


def arms_code(C_, S_, K_, info):
    cname, sname, kname = (X["name"].split()[1] for X in (C_, S_, K_))
    what = {"bar": "an iron bar struck (triangles on the note and its free-bar modes 2.76 and 5.40)",
            "plate": "an iron plate struck (sines on the note and its plate modes 1.59, 2.14, 2.65)",
            "grille": "two iron bars 3% apart struck together, beating",
            "clank": "the weapon clank's own partials on the note"}[C_["sp"]["clang"]]
    note = "E4" if abs(C_["sp"]["f"] - E4) < 1 else "E3"
    c_cast = _wrap([
        f'PORTCULLIS\'S CAST, THE GATE COMES DOWN -- v72 §7.2: "a metal-on-stone clang and a low hum '
        f'settling, 0.4s". {cname}, of {info["n_cast"]}, picked on the numbers by `portcullis_voice_lab.py` '
        f'under Rick\'s "you pick i overrule" (v100). Portcullis had no arm and fell through to rune-crack, '
        f'which Lightkeeper, Farwarden and Bindweed still use, so this ADDS arms before that fallback and '
        f'leaves it alone.',
        f"The stone is a lowpass noise burst, 60 ms, that does not ring; the clang is {what}, on {note} "
        f"(the score's fifth); the hum is the score's tonic, A2 over A1, one strike that settles into silence. "
        f"Audible {info['c_aud']:.0f} ms; the loudest 50 ms {info['c_top']:+.1f} dB re Portcullis's own blow; "
        f"the hum {info['c_hum']:+.1f} dB under the clang; the stone {info['c_stone']:+.1f} dB re the attack. "
        f"Register at most {info['c_reg']:.2f} against rune-crack, the vigil and flail casts, the clank, the "
        f"death voice and the blow."], 10)
    body_what = {"sine": "a held A1 sine and an A2 triangle",
                 "noise": "a held A1 sine and a lowpass noise body",
                 "stack": "a re-struck A1 body",
                 "tom": "a held E2 sine and an E3 triangle"}[S_["sp"]["body"]]
    c_slam = _wrap([
        f'ONSLAUGHT\'S SLAM -- "a heavy gated thud (share below 120 Hz >= 0.45, <= 0.25s), louder with the '
        f'shield (peak 0.35 -> 0.65 across 0 -> 90)" (v72 §7.2). {sname}, of {info["n_slam"]} '
        f'(`portcullis_voice_lab.py`). `tickRam` plays it on the slam\'s frame with `shield`, the shield the '
        f'slam hit for, before the bank.',
        f"{body_what[0].upper() + body_what[1:]}, cut together on a zero crossing (whole cycles; "
        f"`.frequency.value = f` keeps each tone's phase where it was scheduled), under a falling punch and a "
        f"contact click. The gain is a quadratic in the shield, solved so the peak is 0.35 / 0.50 / 0.65 at "
        f"0 / 45 / 90: measured " + " / ".join(f"{v:.3f}" for v in info["s_pk"]) + f" at 0 / 22.5 / 45 / "
        f"67.5 / 90. {info['s_low']:.2f} of its power below 120 Hz at the worst noise draw; gone by "
        f"{info['s_gone']:.0f} ms; within 6 dB of its loudest for {100 * info['s_hold']:.0f}% of its length, "
        f"then cut in {info['s_cut']:.0f} ms. Register at most {info['s_reg']:.2f} against the blow, the "
        f"death voice, rune-crack and the cast."], 10)
    c_close = _wrap([
        f'THE PLATES FALL -- "plates falling -- three short clinks" (v72 §7.2). {kname}, of '
        f'{info["n_close"]} (`portcullis_voice_lab.py`): three small plates struck (modes 1 : 1.59 : 2.14), '
        f'at {info["k_at"]} s, each lower than the last ({info["k_hz"]} Hz), inside the picture\'s 0.3 s '
        f'fall; each clink audible {info["k_aud"]} ms; '
        f'register at most {info["k_reg"]:.2f} against the clank, the blow, rune-crack, the bank and the cast. '
        f'`tickRam` plays it only when the window closes by its clock with the caster alive, never on a '
        f'death.'], 10)
    return (f'        }} else if (w === "portcullis"){{                 // the gate comes down\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["kh"], C_["dh"], C_["ks"])}\n'
            f'        }} else if (w === "portcullis-slam"){{            // the shell hits the foe\n'
            f'{c_slam}\n{slam_body(S_["sp"], S_["A"], S_["B"], S_["C"])}\n'
            f'        }} else if (w === "portcullis-close"){{           // and the plates fall\n'
            f'{c_close}\n{close_body(K_["sp"], K_["g"], K_["D"])}\n'
            f'{SFX_ANCHOR}')


def kind_code(B_, info):
    bname = B_["name"].split()[1]
    what = {"latch": "a latch catching: two quick struck ticks rising a third, C7 then E7, 35 ms apart, each "
                     "with a bar mode",
            "charge": "a rising glint: a triangle climbing an octave, E6 to E7, with a sine an octave over it",
            "plate": "a small bright plate ping on A6",
            "shimmer": "a noise band sweeping up, 1.5 to 5 kHz"}[B_["sp"]["kind"]]
    c = _wrap([
        f'THE WARD\'S BANK -- v72 §7.2 asks for "the ward\'s existing bank voice, reused". There was none: '
        f'nothing played when a ward banked (a ward that breaks plays the ordinary hit, a crit). So this is '
        f'the ward\'s own new kind, as hex-snap is the runic school\'s. {bname}, of {info["n_bank"]}, picked '
        f'on the numbers by `portcullis_voice_lab.py` under Rick\'s "you pick i overrule" (v100).',
        f"{what[0].upper() + what[1:]}. Onslaught's bank plays it on the slam's frame, so it stands "
        f"{info['b_over']:+.1f} dB over the loudest slam in its own band; audible {info['b_aud']:.0f} ms; its "
        f"loudest 50 ms {info['b_db']:+.1f} dB re Portcullis's blow; register at most {info['b_reg']:.2f} "
        f"against the spark collect (the blessing's chime), the shatter, the clank, the runic snap, "
        f"rune-crack, the slam and the cast. Only Onslaught plays it: the vigil blow's own bank stays silent, "
        f"as it always has."], 8)
    return (f'      else if (kind === "ward-bank"){{\n{c}\n{bank_body(B_["sp"], B_["g"])}\n      }}\n'
            f'{KIND_ANCHOR}')


# ============================================================== THE PAGE ===
# The tickRam rows, applied to the real prototype and run beside the original;
# the survey of Onslaught's windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows, mirror]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const orig = P.tickRam; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickRam anchor occurs ${at} times in tickRam()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const NEW = (k, p) => (k === "ult" && p && typeof p.w === "string" && p.w.startsWith("portcullis-")) || k === "ward-bank";
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "portcullis");
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, "portcullis", sd) : new AC.Match("portcullis", fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inRam = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      if (NEW(kind, p) || (kind === "ult" && p && p.w === "portcullis"))
        calls.push({ step, t: m.t, k: kind === "ward-bank" ? "bank" : p.w, shield: p && p.shield !== undefined ? p.shield : null,
                     fs: f.shield, inRam: !!inRam, mine: true });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    P.tickRam = function(dt){ inRam++; try { return impl.call(this, dt); } finally { inRam--; } };
    const wins = [], slamSteps = {}, bankSteps = {}; let prev = null, W = null, n = 0, ls = 0, lb = 0, capBanks = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n;
        const s0 = f.shield;
        m.step(DT); n++;
        const Z = f.ultRam, T = f.ramTally;
        if (Z && Z !== prev){ if (W && !W.end && prev){ W.end = "recast"; W.endStep = step; }
                              W = { cast: m.t, castStep: step, end: null, endStep: null, slams: 0 }; wins.push(W); }
        if (T){
          if (T.slams > ls){ slamSteps[step] = T.slams - ls; if (W) W.slams += T.slams - ls; ls = T.slams; }
          if (T.banks > lb){ bankSteps[step] = T.banks - lb; lb = T.banks; }
        }
        if (!Z && prev){ W.end = (f.alive && prev.t >= prev.dur) ? "clock" : "death"; W.endStep = step; W.close = m.t; }
        prev = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickRam = orig; if (had) S.play = op; else delete S.play; }
    const T = f.ramTally || {};
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.shield, m.b.shield, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.a.vx, m.a.vy, m.b.vx, m.b.vy, m.winner ? m.winner.w.id : null, T]),
             calls, other: JSON.stringify(other), wins, slamSteps, bankSteps, T };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, slams = 0, slamV = 0, banks = 0, bankV = 0, closes = 0, castV = 0, atCap = 0, zeroSl = 0,
      mirrorSlamV = 0;
  const shields = [], pick = [], perWin = [];
  const pairs = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds) pairs.push([side, fid, sd]);
  if (mirror) for (const sd of seeds) pairs.push([2, "portcullis", sd]);
  for (const [side, fid, sd] of pairs){
    let A, B;
    if (side === 2){
      /* the mirror: both balls are Portcullis; each side is checked from side a */
      try { A = run(0, fid, sd, false); B = run(0, fid, sd, true); }
      catch (e){ bad.push(["mirror", String(e)]); continue; }
    } else { A = run(side, fid, sd, false); B = run(side, fid, sd, true); }
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== "portcullis")) bad.push([fid, sd, "the UNPATCHED run played an Onslaught voice"]);
    for (const c of B.calls) if (c.k !== "portcullis" && !c.inRam) bad.push([fid, sd, "an Onslaught voice outside tickRam", c.k]);
    /* the mirror is checked for identity only: both balls cast, slam and bank, and the counts
       below are one fighter's */
    if (side === 2){ mirrorSlamV += B.calls.filter(c => c.k === "portcullis-slam").length; continue; }
    const cv = B.calls.filter(c => c.k === "portcullis");
    castV += cv.length;
    if (cv.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", cv.length, B.wins.length]);
    /* per step: one slam voice per slam, one bank voice per bank */
    const byStep = {};
    for (const c of B.calls) (byStep[c.step] = byStep[c.step] || []).push(c);
    const keys = new Set([...Object.keys(B.slamSteps), ...Object.keys(B.bankSteps), ...Object.keys(byStep)]);
    for (const k of keys){
      const cs = byStep[k] || [];
      const sv = cs.filter(c => c.k === "portcullis-slam"), bv = cs.filter(c => c.k === "bank");
      const ns = B.slamSteps[k] || 0, nb = B.bankSteps[k] || 0;
      if (sv.length !== ns || bv.length !== nb) bad.push([fid, sd, "step " + k, "slams", ns, sv.length, "banks", nb, bv.length]);
      for (let i = 0; i < sv.length; i++){
        const s = sv[i].shield;
        if (typeof s !== "number" || s !== sv[i].fs) bad.push([fid, sd, "a slam voice's shield is not the ball's", s, sv[i].fs]);
        if (s < 0 || s > 90) bad.push([fid, sd, "slam shield out of range", s]);
        shields.push(s);
        if (s === 0) zeroSl++;
        const b = bv[i];
        if (!b) continue;
        if (Math.abs(b.fs - Math.min(90, s + 8)) > 1e-9) bad.push([fid, sd, "the bank voice does not read the slam's shield banked", s, b.fs]);
        if (s >= 90) atCap++;
      }
      slamV += sv.length; bankV += bv.length; slams += ns; banks += nb;
    }
    const cl = B.calls.filter(c => c.k === "portcullis-close");
    closes += cl.length;
    for (const W of B.wins){
      ends[W.end]++; casts++; perWin.push(W.slams);
      const c1 = cl.filter(c => c.step >= W.castStep && (W.endStep === null || c.step <= W.endStep));
      if (W.end === "clock"){
        if (c1.length !== 1 || c1[0].step !== W.endStep) bad.push([fid, sd, "clock close voices", c1.length]);
      } else if (c1.length) bad.push([fid, sd, W.end + " window played a close"]);
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, slams: W.slams });
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, slams, slamV, banks, bankV, closes,
           atCap, zeroSl, mirrorSlamV, shields, perWin, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Onslaught's.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const orig = P.tickRam; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, "portcullis", sd) : new AC.Match("portcullis", fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = kind === "ward-bank" ? "bank" : (kind === "ult" && typeof q.w === "string" &&
                q.w.startsWith("portcullis")) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickRam = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickRam = orig; if (had) S.play = op; else delete S.play; }
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
  for (const [k, kind, p] of [["cast", "ult", { w: "portcullis" }], ["slam", "ult", { w: "portcullis-slam", shield: 45 }],
                              ["bank", "ward-bank", {}], ["close", "ult", { w: "portcullis-close" }],
                              ["hit", "hit", { dmg: 23, crit: false }]]){
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


def gated(x):
    """HOLD (share of AUDIBLE within 6 dB of the loudest 5 ms window) and CUT
    (ms from the last window within 6 dB to the end of AUDIBLE)."""
    np = _np()
    y = x[int(T0 * SR):]
    e5, _ = env(y, 0.005, 0.005)
    mx = e5.max()
    on = np.nonzero(e5 > mx * 0.02)[0]
    w6 = np.nonzero(e5 > mx * 10 ** (-6 / 20))[0]
    aud = (on[-1] - on[0] + 1) * 5.0
    return (w6[-1] - w6[0] + 1) * 5.0 / aud, float((on[-1] - w6[-1]) * 5.0)


def stone(draws):
    """STONE, DRY and DULL (see the docstring). The stone is the only part of
    a cast built from the noise buffer, so two renders on two noise draws
    differ by exactly it (and by the compressor's reaction to it, which is
    small): the NOISE PART of a draw pair is (x1 - x2) / sqrt 2. Median over
    six disjoint pairs of the twelve draws.
      STONE  its RMS over 0-40 ms against the whole voice's there, dB
      DRY    its RMS over 60-120 ms against its own 0-40 ms, dB
      DULL   its power centroid over 0-40 ms, Hz"""
    np = _np()
    st, dr, du = [], [], []
    a, b = int(T0 * SR), int((T0 + 0.04) * SR)
    c0, c1 = int((T0 + 0.06) * SR), int((T0 + 0.12) * SR)
    fr = np.fft.rfftfreq(1 << 14, 1 / SR)
    for i in range(0, len(draws) - 1, 2):
        n = (draws[i] - draws[i + 1]) / math.sqrt(2)
        rn = math.sqrt(float((n[a:b] ** 2).mean()))
        rx = math.sqrt(float((draws[i][a:b] ** 2).mean()))
        st.append(db(rn / max(rx, 1e-12)))
        dr.append(db(math.sqrt(float((n[c0:c1] ** 2).mean())) / max(rn, 1e-12)))
        P = np.abs(np.fft.rfft(n[a:b] * np.hanning(b - a), 1 << 14)) ** 2
        du.append(float((P * fr).sum() / max(P.sum(), 1e-30)))
    return float(np.median(st)), float(np.median(dr)), float(np.median(du))


def clang(x):
    """The clang's NOTE (FFT peak, 150 Hz-4 kHz, first 60 ms), METAL (ratio,
    cents, dB of its strongest partial 1.5x-4x), RING (its third-octave at
    100-150 ms re 0-50 ms, dB) and LEVEL (its third-octave over 0-50 ms re the
    whole voice's RMS there, dB)."""
    np = _np()
    note = pitch(x, T0, T0 + 0.06, lo=150, hi=4000)
    r, c, d = inharm(x, T0, T0 + 0.06, note)
    b0 = band_rms(x, note, T0, T0 + 0.05)
    ring = db(band_rms(x, note, T0 + 0.10, T0 + 0.15) / max(b0, 1e-12))
    seg = x[int(T0 * SR):int((T0 + 0.05) * SR)]
    lvl = db(b0 / max(math.sqrt(float((seg ** 2).mean())), 1e-12))
    return note, r, c, d, ring, lvl


def hum(x, aud_ms, a0_ms):
    """TAIL-LOW and SETTLE (see the docstring), inside the audible span."""
    np = _np()
    y = x[int(T0 * SR):]
    lo = lowpass_fft(y, 150.0)
    a0 = a0_ms / 1000
    a1 = (a0_ms + aud_ms) / 1000
    a = max(0.0, a1 - 0.15)
    seg_all = y[int(a * SR):int(a1 * SR)]; seg_lo = lo[int(a * SR):int(a1 * SR)]
    tail = float((seg_lo ** 2).sum() / max((seg_all ** 2).sum(), 1e-30))
    e, c = env(lo, 0.05)
    live = (c >= a0) & (c <= a1)
    e, c = e[live], c[live]
    im = int(np.argmax(e))
    at300 = db(float(e[int(np.argmin(np.abs(c - 0.3)))]) / float(e[im]))
    after = 20 * np.log10(np.maximum(e[im:], 1e-9))
    rise = float(max(0.0, (after - np.minimum.accumulate(after)).max())) if len(after) else 0.0
    return tail, at300, rise


def onsets_n(x, span=0.5, gap=40, floor=0.25):
    """Peaks of the 1 ms RMS at least `gap` ms apart and at least `floor` of the
    loudest, in time order: (ms after the event, level re the loudest)."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + span) * SR)]
    H = int(0.001 * SR); n = len(y) // H
    e = np.sqrt((y[:n * H].reshape(n, H) ** 2).mean(axis=1))
    pk = [i for i in range(1, n - 1) if e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] >= floor * e.max()]
    pk.sort(key=lambda i: -e[i])
    got = []
    for i in pk:
        if all(abs(i - j) >= gap for j in got):
            got.append(i)
    got.sort()
    return [(float(i), float(e[i] / e.max())) for i in got]


def speak(x, a, b, lo=500.0, hi=12000.0):
    return pitch(x, a, b, lo=lo, hi=hi)


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v72 §7.2 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms; 'a metal ... clang': the note (150 Hz-4 kHz, "
    "first 60 ms) is METAL (its strongest peak between 1.5x and 4x lies >= 60 "
    "cents from every whole multiple, within 20 dB), RINGS (its third-octave "
    "in 100-150 ms within 20 dB of 0-50 ms) and LEADS (that third-octave over "
    "0-50 ms within 10 dB of the whole voice's RMS there); 'on stone': a dry "
    "noise impact under the ring -- STONE >= -12 dB, DRY <= -20 dB, DULL <= "
    "1500 Hz (a thunk, not a hiss); 'a low hum': TAIL-LOW >= 0.50 (what is left at the "
    "end is under 150 Hz); 'settling': the hum band 300 ms in >= 10 dB under its "
    "own loudest, and never rising >= 1 dB after it. Register against "
    "rune-crack, the school's casts (Bulwarden, Vesper, Starwarden), the type's "
    "(Gravemourn, Slagheart, Threshmaw, Paradox, Morningstar), the clank, the "
    "death voice and the hit @ 23 each <= 0.80 (not the fallback it replaces, "
    "not a row-mate, not a parry, not a death, not a blow). Level: TOP between "
    "0.5x the hit @ 23's loudest 50 ms on its LOUDEST draw and 1.0x on its "
    "QUIETEST (heard like a blow, never over one). Tiebreak: the most distinct "
    "register (the highest of those twelve, to 0.05), then the fewest calls.")

SLAM_RULE = (
    "'share below 120 Hz >= 0.45': LOW >= 0.45 on the WORST draw at every "
    "shield; '<= 0.25s': GONE <= 250 ms at every shield; 'gated': HOLD >= 0.5 "
    "and CUT <= 20 ms at every shield; 'a thud': RISE <= 5 ms, the peak in the "
    "first 15 ms; 'peak 0.35 -> 0.65 across 0 -> 90': PEAK within 0.02 of 0.35 + "
    "0.30 x shield / 90 at shields 0, 22.5, 45, 67.5, 90 on render.py's draw and "
    "within 0.03 on every draw, rising with every step; heard: at shield 0 its "
    "third-octave at its body's pitch >= 2x the score's p90 there. Register "
    "against the hit @ 23, the death voice, rune-crack and the picked cast each "
    "<= 0.80 (a slam is not a blow, not a death). Tiebreak: the most distinct "
    "register (to 0.05), then the fewest calls.")

BANK_RULE = (
    "No doc number exists for this voice (it is new); the gates are what it must "
    "do in play. 'on every slam': OVER-SLAM >= +10 dB (heard on the loudest "
    "slam's own frame) and AUDIBLE <= 200 ms (over well before the next slam, "
    ">= 0.5 s on); heard: loudest 50 ms between 2x the wall tick's (loudest "
    "draw) and 0.7x the hit @ 23's (quietest draw) on every draw; 'the ward's', "
    "not another's: register against the spark collect (the blessing's bank), "
    "the shatter (the ward breaking), the clank, hex-snap, rune-crack, the "
    "picked slam and the picked cast each <= 0.80. Tiebreak: the lowest worst "
    "register (to 0.05), then the fewest calls.")

CLOSE_RULE = (
    "'three': exactly three ONSETS in the first 0.5 s; 'short': each clink "
    "alone AUDIBLE <= 80 ms and the whole GONE <= 400 ms; 'clinks' (small metal "
    "struck): each clink RISE <= 3 ms with its peak in its first 10 ms, its "
    "note >= 1 kHz, and METAL (its strongest peak between 1.5x and 4x the "
    "note >= 60 cents from every whole multiple, within 20 dB); 'plates "
    "falling' inside the picture's 0.3 s fall: the third onset <= 300 ms; "
    "heard: loudest 50 ms between 2x the wall tick's and 0.7x the hit @ 23's, "
    "and the first clink's third-octave >= 2x the score's p90 there. Register "
    "against the clank, the hit @ 23, rune-crack, the picked bank and the "
    "picked cast each <= 0.80. Tiebreak: the lowest worst register (to 0.05), "
    "then the clinks FALLING ('plates falling': each lower than the last), then "
    "the fewest calls.")


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
    if M["inh_c"] < 60 or M["inh_db"] < -20:
        why.append(f"not metal: its partial at {M['inh_r']:.2f}x is {M['inh_c']:.0f} c from a whole "
                   f"multiple, {M['inh_db']:+.0f} dB")
    if M["ring"] < -20: why.append(f"the clang does not ring ({M['ring']:+.1f} dB by 100 ms)")
    if M["lead"] < -10: why.append(f"the clang does not lead ({M['lead']:+.1f} dB re the attack)")
    if M["stone"] < -12: why.append(f"stone {M['stone']:+.1f} dB < -12")
    if M["dry"] > -20: why.append(f"the stone rings ({M['dry']:+.1f} dB by 60 ms)")
    if M["dull"] > 1500: why.append(f"the stone is a hiss (centroid {M['dull']:.0f} Hz)")
    if M["tail"] < 0.50: why.append(f"tail-low {M['tail']:.2f} < 0.50 (no hum left)")
    if M["at300"] > -10: why.append(f"the hum {M['at300']:+.1f} dB at 300 ms (not settling)")
    if M["hrise"] >= 1: why.append(f"the hum rises {M['hrise']:.1f} dB after its peak")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def slam_why(M, lev):
    why = []
    if M["low_min"] < 0.45: why.append(f"low {M['low_min']:.2f} < 0.45 (worst)")
    if M["gone_max"] > 250: why.append(f"gone at {M['gone_max']:.0f} ms (> 250)")
    if M["hold_min"] < 0.5: why.append(f"hold {M['hold_min']:.2f} < 0.5 (not gated)")
    if M["cut_max"] > 20: why.append(f"cut {M['cut_max']:.0f} ms > 20 (not gated)")
    if M["rise"] > 5: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 15: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["pk_err"] > 0.02: why.append(f"peak off the line by {M['pk_err']:.3f} (render.py's draw)")
    if M["pk_err_all"] > 0.03: why.append(f"peak off the line by {M['pk_err_all']:.3f} (worst draw)")
    if not M["rising"]: why.append("peak not rising with the shield")
    if M["inb"] < lev["inb"]: why.append(f"in-band {M['inb']:.4f} < {lev['inb']:.4f} (under the score)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def bank_why(M, lev):
    why = []
    if M["over"] < 10: why.append(f"over the slam {M['over']:+.1f} dB < +10")
    if M["aud"] > 200: why.append(f"audible {M['aud']:.0f} ms > 200")
    if M["top_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    o = M["on"]
    if len(o) != 3: why.append(f"{len(o)} onsets, not three")
    elif o[2][0] > 300: why.append(f"the third clink at {o[2][0]:.0f} ms (> 300)")
    if M["gone"] > 400: why.append(f"gone at {M['gone']:.0f} ms")
    for j, C in enumerate(M["clinks"]):
        if C["aud"] > 80: why.append(f"clink {j + 1} audible {C['aud']:.0f} ms")
        if C["rise"] > 3: why.append(f"clink {j + 1} rise {C['rise']:.0f} ms")
        if C["pk_ms"] > 10: why.append(f"clink {j + 1} peaks at {C['pk_ms']:.0f} ms")
        if C["pitch"] < 1000: why.append(f"clink {j + 1} at {C['pitch']:.0f} Hz")
        if C["inh_c"] < 60 or C["inh_db"] < -20:
            why.append(f"clink {j + 1} not metal: its partial at {C['inh_r']:.2f}x is {C['inh_c']:.0f} c from "
                       f"a whole multiple, {C['inh_db']:+.0f} dB")
    if M["top"] > lev["hi"]: why.append(f"loudest 50 ms {M['top']:.4f} > {lev['hi']:.4f}")
    if M["top"] < lev["lo"]: why.append(f"loudest 50 ms {M['top']:.4f} < {lev['lo']:.4f}")
    if M["inb"] < M["inb_floor"]: why.append(f"in-band {M['inb']:.4f} < {M['inb_floor']:.4f} (under the score)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-tendril-t3.html")
    ap.add_argument("--out", default="../05-reference/v100")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=100601)
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "slam": SLAM_RULE, "bank": BANK_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("Sfx hex-snap", KIND_ANCHOR), ("tickRam slam", SLAM_ANCHOR),
                    ("tickRam bank", BANK_ANCHOR), ("tickRam close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if "portcullis-slam" in html or '"ward-bank"' in html:
        raise SystemExit(f"{gp.name} already carries Onslaught's voices -- run on stage 5")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nONSLAUGHT -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        kinds = page.evaluate("() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();"
                              " return [...new Set([...s.matchAll(/kind === \"([a-z-]+)\"/g)].map(m => m[1]))]; }")
        print(f"  THE SYNTH'S KINDS TODAY ({len(kinds)}): {', '.join(kinds)} -- "
              f"{'no ward or bank voice' if not any('ward' in k or 'bank' in k for k in kinds) else 'A WARD VOICE EXISTS'}")
        if any("ward" in k or "bank" in k for k in kinds):
            raise SystemExit("a ward/bank kind exists -- reuse it (the design says so), do not make one")
        rec["kinds"] = kinds

        def R(evs, secs=3.0, seed=None, rows=None):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
            new = any(e[0] == "body" or (e[0] == "arm" and (
                (e[2] == "ult" and str(e[3].get("w", "")).startswith("portcullis")) or e[2] == "ward-bank"))
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

        sizes = {}

        def wav(name, x):
            sizes[name] = write_wav(out / name, x)

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        SCHOOL = ("bulwarden", "vesper", "starwarden")
        TYPE = ("gravemourn", "slagheart", "redflail", "paradox", "morningstar")
        FALL = ("portcullis", "lightkeeper", "farwarden", "bindweed")
        ctl = {}
        REFS = [("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                ("BAR", ["play", T0, "ult", {"w": "axiom"}]),
                ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                ("hit@23", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("wall", ["play", T0, "wall", {}]),
                ("death", ["play", T0, "death", {}]),
                ("clank", ["play", T0, "clank", {"mass": 3.6}]),
                ("spark", ["play", T0, "spark", {"collect": True, "n": 3}]),
                ("shatter", ["play", T0, "hit", {"dmg": 20, "crit": True}]),
                ("hex-snap", ["play", T0, "hex-snap", {}])]
        REFS += [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in SCHOOL + TYPE]
        REFS += [(f"{r_} now", ["play", T0, "ult", {"w": r_}]) for r_ in FALL]
        for name, ev in REFS:
            x, _ = R([ev])
            ctl[name] = dict(basic(x), x=x, low=low_share(x))
            M = ctl[name]
            if not name.endswith(" now"):
                print(f"  {name:<12} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
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
        print("  ARE rune-crack today (max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if max(fall.values()) > 1e-6:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        # the noise draws
        D = {k: [] for k in ("hit@23", "wall", "rune-crack", "death", "clank", "spark", "shatter", "hex-snap")
             + SCHOOL + TYPE}
        for sd in NOISE_SEEDS:
            for k in D:
                ev = dict(REFS)[k]
                D[k].append(basic(R([ev], seed=sd)[0]))
        h_lo, h_hi = min(m["top"] for m in D["hit@23"]), max(m["top"] for m in D["hit@23"])
        w_hi = max(m["top"] for m in D["wall"])
        print(f"  the hit @ 23 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m['peak'] for m in D['hit@23']):.3f}-{max(m['peak'] for m in D['hit@23']):.3f};  the wall "
              f"tick: {min(m['top'] for m in D['wall']):.4f}-{w_hi:.4f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]

        def bedp90(f):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + 0.25)
                                        for i in range(0, len(bseg) - 12000, 2400)], 90))

        def reg(DB, key):
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        rec["levels"] = dict(hit23=[h_lo, h_hi], wall_hi=w_hi)
        wav("portcullis-ctl-runecrack.wav", rcx)
        wav("portcullis-ctl-hit23.wav", ctl["hit@23"]["x"])
        wav("portcullis-ctl-clank.wav", ctl["clank"]["x"])
        wav("portcullis-ctl-death.wav", ctl["death"]["x"])
        wav("portcullis-ctl-spark.wav", ctl["spark"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_top = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a metal-on-stone clang and a low hum settling, 0.4s'. Level-matched: TOP {tgt_top:.4f} "
              f"(the centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the hum {HUM_UNDER_DB:g} dB under the clang, "
              f"AUDIBLE {CAST_AUD:g} ms")

        def cx(sp, g, kh, dh, ks, part="both", held=False, seed=None):
            return R([["body", T0, cast_body(sp, g, kh, dh, ks, part, held), {}]], seed=seed)

        def calib_cast(sp):
            g, kh, dh, ks = 0.3, 0.5, 1.0, 2.4
            for _ in range(4):
                lo_, hi_ = math.log(0.2), math.log(4.0)
                for _ in range(12):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, kh, math.exp(mid), ks)[0])["aud"] < CAST_AUD: lo_ = mid
                    else: hi_ = mid
                dh = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                ct = basic(cx(sp, g, kh, dh, ks, "clang")[0])["top"]
                ht = basic(cx(sp, g, kh, dh, ks, "hum")[0])["top"]
                kh = kh * (ct * 10 ** (-HUM_UNDER_DB / 20)) / ht
                st_ = stone([cx(sp, g, kh, dh, ks, seed=sd)[0] for sd in NOISE_SEEDS])[0]
                ks = ks * 10 ** ((STONE_DB - st_) / 20)
                g = g * tgt_top / basic(cx(sp, g, kh, dh, ks)[0])["top"]
            return float(f"{g:.4g}"), float(f"{kh:.4g}"), dh, float(f"{ks:.4g}")

        def cast_metrics(M, x, draws):
            M["note"], M["inh_r"], M["inh_c"], M["inh_db"], M["ring"], M["lead"] = clang(x)
            M["stone"], M["dry"], M["dull"] = stone(draws)
            M["tail"], M["at300"], M["hrise"] = hum(x, M["aud"], M["a0"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in ("rune-crack",) + SCHOOL + TYPE + ("clank", "death", "hit@23")}

        def cast_measure(sp, g, kh, dh, ks, part="both", held=False):
            x, calls = cx(sp, g, kh, dh, ks, part, held)
            x2, _ = cx(sp, g, kh, dh, ks, part, held)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, kh=kh, dh=dh, ks=ks)
            draws = [cx(sp, g, kh, dh, ks, part, held, seed=sd)[0] for sd in NOISE_SEEDS]
            cast_metrics(M, x, draws)
            if part == "both" and not held:
                M["hum_db"] = db(basic(cx(sp, g, kh, dh, ks, "hum")[0])["top"] /
                                 basic(cx(sp, g, kh, dh, ks, "clang")[0])["top"])
            return M

        H_ = (f"  {'cand':<9}{'g':>7}{'kh':>7}{'dh':>6}{'ks':>6}{'calls':>6}{'top':>8}{'aud':>5}{'note':>6}{'inh x/c/dB':>15}"
              f"{'ring':>6}{'lead':>6}{'stone':>6}{'dry':>6}{'dull':>6}{'tail':>6}{'@300':>6}{'rise':>5}{'rc':>5}{'bulw':>5}{'vesp':>5}{'star':>5}"
              f"{'grav':>5}{'slag':>5}{'thr':>5}{'para':>5}{'morn':>5}{'clnk':>5}{'dth':>5}{'hit':>5}")
        print(H_)

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>7.4g}{M['kh']:>7.4g}{M['dh']:>6.3g}{M['ks']:>6.3g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['aud']:>5.0f}{M['note']:>6.0f}{M['inh_r']:>6.2f}/{M['inh_c']:>3.0f}/{M['inh_db']:<+4.0f}"
                  f"{M['ring']:>6.1f}{M['lead']:>6.1f}{M['stone']:>6.1f}{M['dry']:>6.1f}{M['dull']:>6.0f}"
                  f"{M['tail']:>6.2f}{M['at300']:>6.1f}{M['hrise']:>5.1f}"
                  + "".join(f"{r_[k]:>5.2f}" for k in ("rune-crack",) + SCHOOL + TYPE + ("clank", "death", "hit@23")))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, kh, dh, ks = calib_cast(sp)
            M = cast_measure(sp, g, kh, dh, ks); M.update(name=name, sp=sp)
            M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"portcullis-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        s0 = rows_c[0]
        for part, held, name in (("nostone", False, "0 BELL"), ("clang", False, "0 NOHUM"),
                                 ("nocl", False, "0 CLANG"), ("both", True, "0 HELD")):
            M = cast_measure(s0["sp"], s0["g"], s0["kh"], s0["dh"], s0["ks"], part, held)
            M.update(name=name, sp=s0["sp"]); M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
            wav(f"portcullis-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        rcm = dict(basic(rcx), x=rcx, calls=5, g=0, kh=0, dh=0, ks=0, name="0 RC-NOW")
        rcd = [R([["play", T0, "ult", {"w": "portcullis"}]], seed=sd)[0] for sd in NOISE_SEEDS]
        cast_metrics(rcm, rcx, rcd)
        rcm["why"] = cast_why(rcm, lev_c)
        ctlc.append(rcm); cast_line(rcm)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 BELL    BAR without the stone -- a control\n"
              "    0 NOHUM   BAR without the hum -- a control\n"
              "    0 CLANG   BAR's stone and hum, no clang -- a control\n"
              "    0 HELD    BAR with its hum held flat and cut at 0.4 s -- a control\n"
              "    0 RC-NOW  what ult/portcullis plays today (rune-crack) -- a control")
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
                                                          rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, kh {C_['kh']}, dh {C_['dh']}, ks {C_['ks']}; {C_['calls']} synth calls; TOP "
              f"{C_['top']:.4f} = {db(C_['top'] / h_lo):+.1f} dB re the hit @ 23 (quietest draw), "
              f"{db(C_['top'] / w_hi):+.1f} dB re the wall; the hum {C_['hum_db']:+.1f} dB re the clang")

        # ---- THE SLAM ------------------------------------------------------
        US = [0.0, 0.25, 0.5, 0.75, 1.0]
        print(f"\nSLAM -- 'a heavy gated thud (share below 120 Hz >= 0.45, <= 0.25s), louder with the shield (peak "
              f"0.35 -> 0.65 across 0 -> 90)'. Level-matched: g = A + B u + C u^2 solved to PEAK 0.35 / 0.50 / "
              f"0.65 at u = 0 / 0.5 / 1")

        def slx(sp, A, B, C, shield, seed=None, flat=None):
            return R([["body", T0, slam_body(sp, A, B, C, flat=flat), {"shield": shield}]], seed=seed)

        def solve_g(sp, target):
            lo_, hi_ = math.log(0.01), math.log(3.0)
            for _ in range(22):
                mid = 0.5 * (lo_ + hi_)
                if basic(slx(sp, 0, 0, 0, 0, flat=math.exp(mid))[0])["peak"] < target: lo_ = mid
                else: hi_ = mid
            return math.exp(0.5 * (lo_ + hi_))

        def calib_slam(sp):
            g0, gm, g1 = (solve_g(sp, PK0), solve_g(sp, 0.5 * (PK0 + PK1)), solve_g(sp, PK1))
            A = g0; B = 4 * gm - 3 * g0 - g1; C = 2 * g1 + 2 * g0 - 4 * gm
            return float(f"{A:.4g}"), float(f"{B:.4g}"), float(f"{C:.4g}")

        slam_inb_floor = 2 * bedp90(A1)
        slam_inb_floor_tom = 2 * bedp90(82.41)

        def slam_measure(sp, A, B, C, name, flat=None):
            M = {"name": name, "sp": sp, "A": A, "B": B, "C": C}
            pk, pk_all, lows, gones, holds, cuts = [], [], [], [], [], []
            xs = {}
            for u in US:
                x, calls = slx(sp, A, B, C, u * CAP, flat=flat)
                x2, _ = slx(sp, A, B, C, u * CAP, flat=flat)
                if float(np.abs(x - x2).max()) > TOL:
                    raise SystemExit(f"slam {name} does not reproduce")
                xs[u] = x
                b_ = basic(x); pk.append(b_["peak"])
                hold_, cut_ = gated(x); holds.append(hold_); cuts.append(cut_)
                gones.append(b_["gone"])
                draws = [slx(sp, A, B, C, u * CAP, seed=sd, flat=flat)[0] for sd in NOISE_SEEDS]
                for d_ in draws:
                    pk_all.append((u, float(np.abs(d_[int(T0 * SR):]).max())))
                    lows.append(low_share(d_))
                    gones.append(basic(d_)["gone"])
                if u == 0.5:
                    M["DB"] = [bands(d_[int(T0 * SR):]) for d_ in draws]
                M["calls"] = calls[0]
            line = lambda u: PK0 + (PK1 - PK0) * u  # noqa: E731
            M["pk"] = pk
            M["pk_err"] = max(abs(p_ - line(u)) for p_, u in zip(pk, US))
            M["pk_err_all"] = max(abs(p_ - line(u)) for u, p_ in pk_all)
            M["rising"] = all(pk[i + 1] > pk[i] for i in range(len(pk) - 1))
            M["low_min"] = min(lows); M["gone_max"] = max(gones)
            M["hold_min"] = min(holds); M["cut_max"] = max(cuts)
            bm = basic(xs[0.5])
            M.update(rise=bm["rise"], pk_ms=bm["pk_ms"], aud=bm["aud"], top=bm["top"], x=xs[0.5], xs=xs,
                     low=low_share(xs[0.5]))
            f_ = 82.41 if sp["body"] == "tom" else A1
            M["inb"] = band_rms(xs[0.0], f_, T0, T0 + 0.2)
            M["regs"] = {k: reg(M["DB"], k) for k in ("hit@23", "death", "rune-crack")}
            M["regs"]["cast"] = float(np.median([cos(M["DB"][i], C_["DB"][i]) for i in range(12)]))
            M["why"] = slam_why(M, dict(inb=slam_inb_floor_tom if sp["body"] == "tom" else slam_inb_floor))
            return M

        print(f"  {'cand':<9}{'A':>8}{'B':>8}{'C':>8}{'calls':>6}" + "".join(f"{'pk' + str(int(u * 90)):>7}" for u in US) +
              f"{'err':>6}{'errW':>6}{'lowW':>6}{'gone':>6}{'hold':>6}{'cut':>5}{'rise':>5}{'pk@':>5}{'inb':>8}"
              f"{'hit':>5}{'dth':>5}{'rc':>5}{'cast':>5}")

        def slam_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['A']:>8.4g}{M['B']:>8.4g}{M['C']:>8.4g}{M['calls']:>6d}" +
                  "".join(f"{p_:>7.3f}" for p_ in M["pk"]) +
                  f"{M['pk_err']:>6.3f}{M['pk_err_all']:>6.3f}{M['low_min']:>6.2f}{M['gone_max']:>6.0f}"
                  f"{M['hold_min']:>6.2f}{M['cut_max']:>5.0f}{M['rise']:>5.0f}{M['pk_ms']:>5.0f}{M['inb']:>8.4f}"
                  f"{r_['hit@23']:>5.2f}{r_['death']:>5.2f}{r_['rune-crack']:>5.2f}{r_['cast']:>5.2f}")

        rows_s = []
        for name, sp, blurb in SLAM_CANDIDATES:
            A, B, C = calib_slam(sp)
            M = slam_measure(sp, A, B, C, name)
            rows_s.append(M); slam_line(M)
            for u in (0.0, 1.0):
                wav(f"portcullis-slam-{name.replace(' ', '-').lower()}-{int(u * 90)}.wav", M["xs"][u])
        ctls = []
        s0 = rows_s[0]
        for name, sp, flat in (("0 PLAIN", dict(body="plain", gate=0.35), None),
                               ("0 LONG", dict(s0["sp"], gate=0.35), None),
                               ("0 FLAT", s0["sp"], "mid")):
            if flat == "mid":
                A_, B_, C_s = s0["A"], s0["B"], s0["C"]
                fl = float(f"{A_ + 0.5 * B_ + 0.25 * C_s:.4g}")
                M = slam_measure(sp, A_, B_, C_s, name, flat=fl)
            else:
                A_, B_, C_s = calib_slam(sp)
                M = slam_measure(sp, A_, B_, C_s, name)
            ctls.append(M); slam_line(M)
            wav(f"portcullis-slam-{name.replace(' ', '-').lower()}.wav", M["x"])
        for (name, _sp, blurb) in SLAM_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print("    0 PLAIN   SINE's body with no gate, each tone decaying over 0.35 s -- a control\n"
              "    0 LONG    SINE gated at 0.35 s -- a control\n"
              "    0 FLAT    SINE at its shield-45 gain for every shield -- a control")
        print(f"  gates: in-band at shield 0 >= {slam_inb_floor:.4f} (2x the score's p90 at A1)")
        print(f"  RULE  {SLAM_RULE}")
        for M in rows_s:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        for M in ctls:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_s, "slam")
        si = fb if ok is None else min(ok, key=lambda i: (round(max(rows_s[i]["regs"].values()) / 0.05),
                                                          rows_s[i]["calls"]))
        S_ = rows_s[si]
        print(f"  PICK  {S_['name']}  g = {S_['A']} + {S_['B']} u + {S_['C']} u^2; peaks "
              + " / ".join(f"{p_:.3f}" for p_ in S_["pk"]) + f" at shield 0-90; LOW {S_['low_min']:.2f} worst; "
              f"gone {S_['gone_max']:.0f} ms; hold {S_['hold_min']:.2f}, cut {S_['cut_max']:.0f} ms")

        # ---- THE BANK ------------------------------------------------------
        lev_b = dict(lo=2 * w_hi, hi=0.7 * h_lo)
        tgt_b = math.sqrt(lev_b["lo"] * lev_b["hi"])
        print(f"\nBANK -- the ward's bank voice: NONE EXISTS, so this is `ward-bank`, new. Level-matched: loudest "
              f"50 ms {tgt_b:.4f} (the centre of {lev_b['lo']:.4f}-{lev_b['hi']:.4f})")

        def bkx(sp, g, seed=None):
            return R([["body", T0, bank_body(sp, g), {}]], seed=seed)

        def calib_bank(sp):
            g = 0.1
            for _ in range(5):
                g = g * tgt_b / basic(bkx(sp, g)[0])["top"]
            return float(f"{g:.4g}")

        slam90 = S_["xs"][1.0]
        rows_b = []
        slam_body_txt = slam_body(S_["sp"], S_["A"], S_["B"], S_["C"])
        print(f"  {'cand':<10}{'g':>8}{'calls':>6}{'top':>16}{'aud':>5}{'pitch':>7}{'over':>7}{'sprk':>5}{'shat':>5}"
              f"{'clnk':>5}{'hexs':>5}{'rc':>5}{'slam':>5}{'cast':>5}")
        def bank_measure(fn, calls, g, name, sp):
            x = fn(None)
            if float(np.abs(x - fn(None)).max()) > TOL:
                raise SystemExit(f"bank {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls, g=g, name=name, sp=sp)
            draws = [fn(sd) for sd in NOISE_SEEDS]
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws); M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            M["pitch"] = pitch(x, T0, T0 + 0.08, lo=500, hi=12000)
            evb = (["body", T0, bank_body(sp, g), {}] if sp is not None else
                   ["play", T0, "spark", {"collect": True, "n": 3}])
            both, _ = R([["body", T0, slam_body_txt, {"shield": CAP}], evb])
            M["both"] = both
            M["over"] = db(band_rms(both, M["pitch"], T0, T0 + 0.08) /
                           max(band_rms(slam90, M["pitch"], T0, T0 + 0.08), 1e-12))
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {"spark": reg(DB, "spark"), "shatter": reg(DB, "shatter"), "clank": reg(DB, "clank"),
                         "hex-snap": reg(DB, "hex-snap"), "rune-crack": reg(DB, "rune-crack"),
                         "slam": float(np.median([cos(DB[i], S_["DB"][i]) for i in range(12)])),
                         "cast": float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)]))}
            M["why"] = bank_why(M, lev_b)
            r_ = M["regs"]
            print(f"  {name:<10}{g:>8.4g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}{M['aud']:>5.0f}"
                  f"{M['pitch']:>7.0f}{M['over']:>7.1f}" +
                  "".join(f"{r_[k]:>5.2f}" for k in ("spark", "shatter", "clank", "hex-snap", "rune-crack", "slam",
                                                     "cast")))
            wav(f"portcullis-bank-{name.replace(' ', '-').lower()}.wav", x)
            wav(f"portcullis-bank-{name.replace(' ', '-').lower()}-on-slam90.wav", both)
            return M

        for name, sp, blurb in BANK_CANDIDATES:
            g = calib_bank(sp)
            calls = bkx(sp, g)[1][0]
            rows_b.append(bank_measure(lambda sd, sp=sp, g=g: bkx(sp, g, seed=sd)[0], calls, g, name, sp))
        ctlb = []
        for name, sp, blurb in BANK_CONTROLS:
            if sp is None:
                ctlb.append(bank_measure(lambda sd: R([["play", T0, "spark", {"collect": True, "n": 3}]], seed=sd)[0],
                                         1, 0.05, name, None))
            else:
                g = calib_bank(sp)
                ctlb.append(bank_measure(lambda sd, sp=sp, g=g: bkx(sp, g, seed=sd)[0], bkx(sp, g)[1][0], g, name, sp))
        for (name, _sp, blurb) in BANK_CANDIDATES + BANK_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print(f"  RULE  {BANK_RULE}")
        for M in rows_b:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlb:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_b, "bank")
        bi = fb if ok is None else min(ok, key=lambda i: (round(max(rows_b[i]["regs"].values()) / 0.05),
                                                          rows_b[i]["calls"]))
        B_ = rows_b[bi]
        print(f"  PICK  {B_['name']}  g {B_['g']}; loudest 50 ms {db(B_['top_hi'] / h_lo):+.1f} dB re the hit @ 23, "
              f"{db(B_['top_lo'] / w_hi):+.1f} dB re the wall; over the loudest slam {B_['over']:+.1f} dB in its band")

        # ---- THE CLOSE -----------------------------------------------------
        lev_k = dict(lo=2 * w_hi, hi=0.7 * h_lo)
        tgt_k = math.sqrt(lev_k["lo"] * lev_k["hi"])
        print(f"\nCLOSE -- 'plates falling -- three short clinks'. Level-matched: loudest 50 ms {tgt_k:.4f} (the "
              f"centre of {lev_k['lo']:.4f}-{lev_k['hi']:.4f}), each clink audible {CLINK_AUD:g} ms")

        def kx(sp, g, D_, only=None, seed=None):
            return R([["body", T0, close_body(sp, g, D_, only), {}]], seed=seed)

        def calib_close(sp):
            g, D_ = 0.1, 0.1
            for _ in range(5):
                if "D" not in sp:
                    D_ = float(f"{D_ * CLINK_AUD / basic(kx(sp, g, D_, only=0)[0])['aud']:.3g}")
                g = g * tgt_k / basic(kx(sp, g, D_)[0])["top"]
            return float(f"{g:.4g}"), D_

        def close_measure(sp, g, D_, name):
            x, calls = kx(sp, g, D_)
            x2, _ = kx(sp, g, D_)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, D=D_, name=name, sp=sp)
            M["on"] = onsets_n(x)
            cl = []
            for j, (s_, f_, k_) in enumerate(sp["clinks"]):
                xc = kx(sp, g, D_, only=j)[0]
                yc = np.concatenate([xc[:int(T0 * SR)], xc[int((T0 + s_) * SR):]])
                C = basic(yc)
                C["pitch"] = pitch(yc, T0, T0 + 0.04, lo=300, hi=12000)
                C["inh_r"], C["inh_c"], C["inh_db"] = inharm(yc, T0, T0 + 0.04, C["pitch"])
                cl.append(C)
            M["clinks"] = cl
            f1 = sp["clinks"][0][1]
            M["inb"] = band_rms(x, f1, T0, T0 + 0.05)
            M["inb_floor"] = 2 * bedp90(f1)
            DB = [bands(x[int(T0 * SR):])] * 12          # tonal: every draw is this one
            M["DB"] = DB
            M["regs"] = {"clank": reg(DB, "clank"), "hit@23": reg(DB, "hit@23"), "rune-crack": reg(DB, "rune-crack"),
                         "bank": float(np.median([cos(DB[i], B_["DB"][i]) for i in range(12)])),
                         "cast": float(np.median([cos(DB[i], C_["DB"][i]) for i in range(12)]))}
            M["why"] = close_why(M, lev_k)
            return M

        print(f"  {'cand':<10}{'g':>8}{'D':>7}{'calls':>6}{'onsets ms':>16}{'aud':>13}{'Hz':>17}{'inh c':>13}"
              f"{'top':>8}{'gone':>5}{'inb':>8}{'clnk':>5}{'hit':>5}{'rc':>5}{'bank':>5}{'cast':>5}")

        def close_line(M):
            r_ = M["regs"]
            ons = "/".join(f"{o[0]:.0f}" for o in M["on"])
            auds = "/".join("%.0f" % c_["aud"] for c_ in M["clinks"])
            hzs = "/".join("%.0f" % c_["pitch"] for c_ in M["clinks"])
            inhs = "/".join("%.0f" % c_["inh_c"] for c_ in M["clinks"])
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['D']:>7.3g}{M['calls']:>6d}{ons:>16}{auds:>13}{hzs:>17}{inhs:>13}"
                  f"{M['top']:>8.4f}{M['gone']:>5.0f}{M['inb']:>8.4f}" +
                  "".join(f"{r_[k]:>5.2f}" for k in ("clank", "hit@23", "rune-crack", "bank", "cast")))

        rows_k = []
        for name, sp, blurb in CLOSE_CANDIDATES:
            g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name)
            rows_k.append(M); close_line(M)
            wav(f"portcullis-close-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlk = []
        for name, sp, blurb in CLOSE_CONTROLS:
            g, D_ = calib_close(sp)
            M = close_measure(sp, g, D_, name)
            ctlk.append(M); close_line(M)
            wav(f"portcullis-close-{name.replace(' ', '-').lower()}.wav", M["x"])
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
        def falls(M):
            f_ = [c_["pitch"] for c_ in M["clinks"]]
            return all(f_[j + 1] < f_[j] * 2 ** (-30 / 1200) for j in range(len(f_) - 1))
        ki = fb if ok is None else min(ok, key=lambda i: (round(max(rows_k[i]["regs"].values()) / 0.05),
                                                          0 if falls(rows_k[i]) else 1, rows_k[i]["calls"]))
        K_ = rows_k[ki]
        print(f"  PICK  {K_['name']}  g {K_['g']}, D {K_['D']}; loudest 50 ms {db(K_['top'] / h_lo):+.1f} dB re the "
              f"hit @ 23, {db(K_['top'] / w_hi):+.1f} dB re the wall")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   slam {S_['name']}   bank {B_['name']}   close {K_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROWS, GENERATED AND CHECKED -----------------------------
        info = dict(c_aud=C_["aud"], c_top=db(C_["top"] / h_lo), c_hum=C_["hum_db"], c_reg=max(C_["regs"].values()),
                    c_stone=C_["stone"], s_pk=S_["pk"], s_low=S_["low_min"], s_gone=S_["gone_max"],
                    s_hold=S_["hold_min"], s_cut=S_["cut_max"], s_reg=max(S_["regs"].values()),
                    b_over=B_["over"], b_aud=B_["aud"], b_reg=max(B_["regs"].values()), b_db=db(B_["top_hi"] / h_lo),
                    k_aud="/".join("%.0f" % c_["aud"] for c_ in K_["clinks"]),
                    k_at=" / ".join(fmt(c_[0]) for c_ in K_["sp"]["clinks"]),
                    k_hz=" / ".join("%.0f" % c_[1] for c_ in K_["sp"]["clinks"]), k_reg=max(K_["regs"].values()),
                    n_cast=len(CAST_CANDIDATES), n_slam=len(SLAM_CANDIDATES), n_bank=len(BANK_CANDIDATES),
                    n_close=len(CLOSE_CANDIDATES))
        arms = arms_code(C_, S_, K_, info)
        kind = kind_code(B_, info)
        _refuse(arms + kind, "Sfx rows")
        sfx_rows = [[SFX_ANCHOR, arms], [KIND_ANCHOR, kind]]
        for anc, code in sfx_rows:
            if code.count(anc) != 1:
                raise SystemExit("an Sfx row does not re-emit its anchor exactly once")
        print("\nTHE SFX ROWS, applied to Sfx.prototype.play's own source and rendered:")
        sbt = slam_body(S_["sp"], S_["A"], S_["B"], S_["C"])
        rp = [float(np.abs(R([["body", T0, sbt, {"shield": CAP}]])[0] - R([["body", T0, sbt, {"shield": CAP}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the loudest slam rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        xa, _ = R([["arm", T0, "ult", {"w": "portcullis"}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa - C_["x"]).max())))
        for sh in (0, 4.5, 11.25, 22.5, 45, 67.5, 81, 90, 120, -3):
            x1, _ = R([["arm", T0, "ult", {"w": "portcullis-slam", "shield": sh}]], rows=sfx_rows)
            x2, _ = R([["body", T0, sbt, {"shield": min(CAP, max(0, sh))}]])
            chk.append((f"slam@{sh:g}", float(np.abs(x1 - x2).max())))
        xb, _ = R([["arm", T0, "ward-bank", {}]], rows=sfx_rows)
        chk.append(("bank", float(np.abs(xb - B_["x"]).max())))
        xk, _ = R([["arm", T0, "ult", {"w": "portcullis-close"}]], rows=sfx_rows)
        chk.append(("close", float(np.abs(xk - K_["x"]).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11.6, 23, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 3.6}), ("clank", {"mass": 5}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("aegis", {"n": 10, "back": 5}), ("aegis", {"broke": True}),
                   ("vine", {"plant": True}), ("vine", {"coil": True}), ("vine", {"miss": True}), ("vine", {"n": 2}),
                   ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}), ("fork", {}),
                   ("scour-hold", {"n": 3}), ("scour-tick", {"n": 2}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = page.evaluate(r"""() => { const s = Object.getPrototypeOf(AC.SFX).play.toString();
            const a = [...s.matchAll(/w === "([a-z-]+)"/g)].map(m => m[1]);
            return [...new Set([...AC.WEAPONS.map(w => w.id), ...a])]; }""")
        ult_ids = [w_ for w_ in ult_ids if not w_.startswith("portcullis")]
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
        now_rc = float(np.abs(xa - rcx).max())
        print(f"  ult/portcullis vs rune-crack after the rows: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3:
            FAILED.append("sfx rows")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, repro=max(rp))

        # ---- THE tickRam ROWS ----------------------------------------------
        tram = [[SLAM_ANCHOR, SLAM_CODE], [BANK_ANCHOR, BANK_CODE], [CLOSE_ANCHOR, CLOSE_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        mirror = page.evaluate("() => { try { new AC.Match('portcullis', 'portcullis', 1); return true; } "
                               "catch (e) { return false; } }")
        print("\nTHE tickRam ROWS, applied to Match.prototype.tickRam's own source, run beside the original on real "
              f"fights (the mirror match {'included' if mirror else 'refused by Match -- not run'}):")
        WR = page.evaluate(WIRE_JS, [seeds, tram, mirror])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Portcullis both sides x every foe x seeds {seeds}"
              f"{' + the mirror' if mirror else ''}): {WR['same']}/{WR['fights']} identical (over, clock, both hp, "
              f"both shields, both positions and velocities, winner, the whole ramTally); every other voice call "
              f"identical in order, kind and opts in {WR['otherSame']}/{WR['fights']}")
        shs = np.array(WR["shields"]) if WR["shields"] else np.zeros(1)
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['slams']} slams -> "
              f"{WR['slamV']} slam voices; {WR['banks']} banks -> {WR['bankV']} bank voices ({WR['atCap']} at the cap); "
              f"{WR['closes']} closes; problems {WR['nbad']}")
        print(f"  the shield a slam carries: {WR['zeroSl']} of {len(WR['shields'])} at 0 "
              f"({100 * WR['zeroSl'] / max(1, len(WR['shields'])):.0f}%), median {np.median(shs):.1f}, p90 "
              f"{np.percentile(shs, 90):.1f}, max {shs.max():.1f}; slams a window: median "
              f"{np.median(WR['perWin']) if WR['perWin'] else 0:.0f}, max {max(WR['perWin']) if WR['perWin'] else 0}")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["slamV"] != WR["slams"] or WR["bankV"] != WR["banks"] or WR["closes"] != WR["ends"]["clock"] \
                or WR["slams"] == 0 or WR["castV"] != WR["casts"]:
            FAILED.append("tickRam rows")
        WB = page.evaluate(WIRE_JS, [seeds, [[SLAM_ANCHOR, SLAM_CODE_BAD], tram[1], tram[2]], False])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a slam): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "slams", "slamV",
                                          "banks", "bankV", "closes", "atCap", "zeroSl", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        rec["wire"]["shield_q"] = [float(np.percentile(shs, q)) for q in (10, 50, 90)]
        print(f"  THE CLOSE ON A DEATH: {WR['ends']['death']} windows closed by the caster's death and "
              f"{WR['ends']['over']} by the fight's end play no close (checked above); a caster's death ends the "
              f"fight on the close's own frame and a foe's before any close, so both endings belong to the death "
              f"voice (Zenith's, Daybreak's and Canopy's rule).")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["slams"], w["foe"], w["seed"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], tram])
            assert not errors, errors[:3]
            c0, c1 = w_["cast"], w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs
                       if e[3] not in ("portcullis-slam", "bank", "portcullis-close")]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd
            fs_ = 82.41 if S_["sp"]["body"] == "tom" else A1
            sl_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "portcullis-slam"]
            bk_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "bank"]
            cl_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == "portcullis-close"]

            def ov(f, a_, d_):
                return db(band_rms(xw, f, a_, a_ + d_) / max(band_rms(xo, f, a_, a_ + d_), 1e-12))
            sl_over = [ov(fs_, t_, 0.2) for t_ in sl_t]
            bk_over = [ov(B_["pitch"], t_, 0.06) for t_ in bk_t]
            cl_over = [ov(K_["clinks"][0]["pitch"], t_, 0.05) for t_ in cl_t]
            sl_sh = [e[2].get("shield") for e in evs if e[3] == "portcullis-slam"]
            print(f"\nIN A REAL WINDOW -- portcullis v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {w_['slams']} slams; the fight's own sounds and the "
                  f"score, with and without the slam, bank and close voices")
            print("  each slam over the fight in its own third-octave: " +
                  " ".join(f"{v:+.1f}" for v in sl_over) + " dB (shields " + " ".join(f"{v:.0f}" for v in sl_sh) + ")")
            print("  each bank: " + " ".join(f"{v:+.1f}" for v in bk_over) + " dB;  the close: " +
                  " ".join(f"{v:+.1f}" for v in cl_over) + " dB")
            if (sl_over and min(sl_over) < 6) or (bk_over and min(bk_over) < 6) or (cl_over and min(cl_over) < 3):
                FAILED.append("a new voice not heard in a real window")
            wav("portcullis-pick-real-window.wav", xw)
            wav("portcullis-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, slam_over=sl_over, bank_over=bk_over, close_over=cl_over, shields=sl_sh)
        # the four picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": "portcullis"}]]
        for k_, sh in enumerate((0, 45, 90)):
            seq += [["arm", T0 + 0.8 + 0.6 * k_, "ult", {"w": "portcullis-slam", "shield": sh}],
                    ["arm", T0 + 0.8 + 0.6 * k_, "ward-bank", {}]]
        seq += [["arm", T0 + 2.9, "ult", {"w": "portcullis-close"}], ["arm", T0 + 3.6, "hit", {"dmg": 23, "crit": False}]]
        xq_, _ = R(seq, secs=6.0, rows=sfx_rows)
        wav("portcullis-pick-sequence.wav", xq_)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "clinks", "DB", "both")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), slam=strip(rows_s), slam_controls=strip(ctls),
               bank=strip(rows_b), bank_controls=strip(ctlb), close=strip(rows_k), close_controls=strip(ctlk),
               wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_kh": C_["kh"], "cast_dh": C_["dh"],
                     "cast_ks": C_["ks"], "slam": S_["name"], "slam_ABC": [S_["A"], S_["B"], S_["C"]],
                     "bank": B_["name"], "bank_g": B_["g"], "close": K_["name"], "close_g": K_["g"],
                     "close_D": K_["D"]})
    print(f"\nTHE PICKS  cast {C_['name']}   slam {S_['name']}   bank {B_['name']}   close {K_['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    rows = [dict(label="Sfx: Portcullis's cast, slam and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="Sfx: the ward's bank voice -- a new kind, `ward-bank`, before hex-snap",
                 anchor=KIND_ANCHOR, mode="replace", code=kind),
            dict(label="tickRam: the slam voice, on the slam's frame, carrying the shield it hit for",
                 anchor=SLAM_ANCHOR, mode="replace", code=SLAM_CODE),
            dict(label="tickRam: the ward's bank voice, after the bank's three writes",
                 anchor=BANK_ANCHOR, mode="replace", code=BANK_CODE),
            dict(label="tickRam: the close voice, when the window closes by its clock with the caster alive",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE)]
    for r_ in rows:
        if html.count(r_["anchor"]) != 1 or r_["code"].count(r_["anchor"]) != 1:
            raise SystemExit(f"row '{r_['label']}': the anchor is not unique, or not re-emitted once")
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
