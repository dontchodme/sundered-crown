#!/usr/bin/env python3
"""REBUTTAL'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v102.

    python lodestone_voice_lab.py --game <a link carrying Lodestone's stage 5> --rows rows.json

v70 §6.2 SOUND, every word of it: "Cast: a rising four-note rune chime, one
per wall, 0.5s total. A touch: a sharp electric snap (<=80ms, peak <=0.5) with
the hex's own stun voice underneath if it lands; pitch steps up with the stack
count. Close: the chime reversed, quiet." The brief's stage 6: "picture,
voice, carry". Rick, for the batch's art and sound: "you pick i overrule". So
this lab does not offer a spread -- it renders three to five candidates a
voice beside CONTROLS that can come back wrong, prints the numbers each pick is
made on, and PICKS by a rule written in this file (`*_RULE`, `*_why`). He
overrules from one clip.

THE THREE EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/lodestone`, which `fireUlt` plays for every relic.
         Lodestone has NO arm today: it falls through to the shared
         rune-crack (measured below, to 1e-6, with every other relic that
         still does). The arms go BEFORE that fallback; the fallback line is
         re-emitted unchanged, so another relic's row anchored on it still
         applies, in either order. No sim line: the cast already plays.
  touch  `ult/lodestone-touch {n}` from `tickRunes`, right after the touch's
         hex lands (its apply line and tally line, re-emitted first,
         unchanged): once per touch, n = `foe.stacks("hex")` -- the count the
         foe now carries, the number its tag shows, 1..5 at the cap of 5.
         Then `hex-snap`, the hex's own voice, UNDER it on the same frame
         (reading 2 below). A touch at the cap (5 -> 5) still snaps, at 5's
         note: the hex landed (its 2.6 s clock refreshed) and added nothing.
  close  `ult/lodestone-close` from `tickRunes`, on a line placed BEFORE the
         close line (re-emitted unchanged), on the frame the window runs out
         BY ITS CLOCK with both fighters alive. Never on a death; never once
         the fight is over -- `step()` returns early after a kill, so a window
         still lit at the verdict closes nothing (stage 5's verdict finding:
         about half of all fights end lit) and plays nothing.

THE READINGS (words of §6.2 the build had to turn into a decision; each is
declared, and the alternative is Rick's):
  1. "ONE PER WALL": the chime's four notes are the four walls lit in turn --
     A C E A, the score's tonic triad up through its octave (A minor, the
     key every chime in the batch is in), one note a wall, rising. Which
     octave, which metal and how the notes are spaced inside the 0.5 s are
     the candidates.
  2. "THE HEX'S OWN STUN VOICE": read as `hex-snap`, the runic school's hex
     voice -- its own comment gathers v75 "a hex snap", v79 "hex's own snap"
     and v80 "the hex -- its snap" into it, and Corollary's echo plays it
     when its hex lands (`if (f.w.ult.hex > 0) SFX.play("hex-snap")`). The
     hex's weapon STUN itself (tickStatus's 0.2 s stun every 1.15 s a stack)
     has NO voice on any relic, and giving it one would voice every hex in
     the game, not this relic's touch -- that is Rick's, and is flagged, not
     built. "IF IT LANDS" is read as the precedent's wiring: whenever the
     touch applies its hex -- the call sits inside the touch's own
     `if (u.hex > 0)` branch, so a touch that hexes (every touch on this
     relic: hex 1) is heard with it; at the cap the apply refreshes the
     hex's clock and that is the hex landing too (counted below).
  3. "PITCH STEPS UP WITH THE STACK COUNT": one note a count, 1..5 (the hex
     cap, checked on the page), A minor pentatonic from the snap's root
     (A C D E G): every count its own note of the score's scale, >= 200 cents
     apart -- a buzz decays in 60 ms, and a semitone is not heard in 60 ms.
  4. "UNDERNEATH": the snap's loudest 50 ms at least 3 dB over the hex-snap's
     (on its loudest noise draw) at every count, and on one frame each keeps
     its own band: the hex's voice is heard under the snap, not over it and
     not lost in it.
  5. "ELECTRIC": a buzz, not a ping -- the snap's note is a square or a
     sawtooth (harmonic-rich), measured as HARM below; "SHARP": RISE <= 1 ms
     and the peak in the first 10 ms; "SNAP" (<=80ms): GONE <= 80 ms at every
     count on every draw.
  6. "0.5S TOTAL": AUDIBLE 430-570 ms, v100's reading of Portcullis's "0.4s"
     (+-70 ms) moved to 0.5.
  7. "REVERSED": Zenith's reading (v98) -- against the LITERAL reversal of the
     picked cast (rendered dry, its samples reversed; a reference that cannot
     ship, because it needs an async render and every clip rebuilds the synth
     synchronously, v88 §6b): ENV-CORR >= 0.80, and the notes fall -- it
     starts on a note at least a fifth over the root and ends on the root.
     "QUIET": its loudest 50 ms at least 6 dB under the cast's (level-matched
     9 dB under), still heard over the score.

THE CONTROLS, and what each one is for:
  rune-crack   what Lodestone's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms -- the
               school's other rune-chime
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@20.5     Lodestone's own blow (the stage-5 blade): the level the cast and
               the touch are judged against, on its quietest / loudest draw
  hex-snap     the hex's own voice, which plays under every touch
  wall         the commonest sound in a fight
  seal         the hall's own rising chime (three notes, 90 ms apart, when a
               seal closes the walls in): the cast must not be it
  zenith       Morningstar's cast, the batch's other rising chime
  the school   the runic casts with a voice of their own (read off the page)
  the type     the warhammer casts with a voice of their own (read off the page)
  burn         the `spark` burn sizzle, the game's other short electric-ish
               crackle; clank (mass 5), the weapons' clash: a touch is not a
               parry
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  CHORD, FALL, SEAL, RC-NOW   the cast's four notes struck at once / falling /
               the seal voice as the cast / what `ult/lodestone` plays today:
               each must fail its gate
  PING, FLAT, LONG, LOUD, HEX   the touch as a triangle note on a click / at
               count 1's note for every count / ringing 0.3 s / at 3x its gain
               / the hex-snap alone: each must fail its gate
  AGAIN        the picked cast played quiet as the close: must fail
  LITERAL      the picked cast's samples reversed: the close's reference

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
  * The shared measures are zenith_voice_lab's and bindweed_voice_lab's,
    imported unchanged (E50 = 50 ms RMS at a 5 ms hop; TOP = the loudest
    50 ms; PEAK = the sample peak; AUDIBLE = first to last 5 ms RMS window
    above 2% of the voice's own loudest; GONE = where it ends, from the
    event; RISE = 10 -> 90% of the 1 ms envelope; REG = cosine of 1/3-octave
    band amplitudes, 25 Hz-16 kHz, the median over noise draws; IN-BAND =
    RMS inside the third-octave round a pitch; PITCH = FFT peak, Hann,
    zero-padded, parabolic; TOP NOTE = the highest peak within 3 dB of the
    strongest; ENV-CORR = Pearson correlation of two E50 curves in dB;
    TONAL = how far the sharpest 1/48-octave peak stands over its
    third-octave neighbourhood, dB), and ironhail_voice_lab's round-2 ear
    (restated here, not imported: HEARD = the voice's loudest third-octave
    AT OR ABOVE 200 Hz against the score's p90 there, dB -- a phone speaker
    reproduces little under 200 Hz, Culverin v96 / Coldiron v103).
  * New here, each with a control that can come back wrong:
      STRIKES   for each of the chime's notes after the first, its own
                third-octave over the 40 ms after its onset against the 40 ms
                before, dB: a note struck at its onset jumps (CHORD and FALL
                must fail); the first note must be there (>= -20 dB re the
                loudest note's jump window)
      RISE0     RISE over the first note's own span (the first note is struck)
      HARM      the power in the 2nd-8th harmonics of the snap's note over
                10-45 ms (each a third-octave round k x the note) against the
                note's own third-octave, dB: a square reads ~-8, a sawtooth
                ~-3, a triangle ~-18 (PING must fail)
      STEP      the snap's PITCH over its first 3-25 ms at each count, and the
                smallest step between neighbouring counts, cents
      KEEP      the snap and the hex-snap on one frame against the snap
                alone: the snap's own note band (the hex-snap must not duck or
                cover it) and the hex-snap's 2.6 kHz band over its first 30 ms
                (HEX-OVER: how far the hex-snap stands over the snap there --
                heard under it, not lost in it), dB
      FALLS     the close's TOP NOTE over the first half of its AUDIBLE, cents
                over the root, and its PITCH over the last 100 ms, cents from
                the root
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's decay is solved so it is AUDIBLE 500 ms and its gain
    puts TOP at the centre of its window; the snap's decay is solved so it is
    GONE by 65 ms at count 1 and its gain puts TOP at the centre of its window
    at count 3; the close's gain puts TOP 9 dB under the cast's. Constants are
    rounded BEFORE any measured render, so a shipped arm is bit-for-bit what
    was measured.

THE ROUNDS. Round 1 was an iteration run (--no-wire: the voices only, no
rows), and two of its gates were wrong; both are fixed here and no other rule
changed:
  * "CHIME" was TONAL >= 20 dB, a number of this lab's own: no control could
    fail it (rune-crack read 29.5) and it put EVEN out at 19.2. It is now
    v101's line, the complement of bindweed_voice_lab's "noise, not a chime"
    (TONAL <= 10 is air): a chime is TONAL > 10 -- and a NOISE control (the
    four notes as band-passed noise bursts, struck but not notes) must fail it.
  * KEEP read the hex-snap's band on one frame against the hex-snap ALONE, so
    a snap whose own partials fill 2.6 kHz read as the hex-snap "louder" and
    was put out for it (HIGH, +4.2 dB). It now reads the hex-snap's band
    against the SNAP alone (HEX-OVER >= +3 dB: the hex-snap heard under the
    snap, not lost in it), and the snap's own band against the snap alone.
  * The cast's tiebreak gained a last clause (the unrounded register) so that
    no pick rests on the order of the candidate list.
Round 2 (the first full run: rows, wire, real window, end to end, peers --
all clean) exited 1 on the touch alone: NO candidate passed HEX-OVER. Every
round-2 snap buzzes at A4 or above, and a square's 5th and 7th harmonics
(2.2-4.1 kHz at A4-G5; the 3rd at A5-G6) land in the hex-snap's own
third-octave, so the hex-snap stood only -0.6 to +2.0 dB over the snap there:
under it, but lost in it. Round 3 ADDS two snaps an octave under the lowest
(A3 C4 D4 E4 G4, 220-392 Hz: a square's partials near 2.6 kHz are then its
11th and 13th, 21 dB down -- the low buzz of an arc, not the whine of a
spark), and makes one measurement what its definition says: TONAL is
bindweed's DRAW-AVERAGED spectrum, and round 2 read the cast candidates on one
draw -- the NOISE control read 10.2 on it and was put out only by its rise.
Every noise-built body is now read over the twelve draws (a noise-free body is
the same on every draw). No rule changed; every round-2 candidate stays in the
tables.
Round 3 passed every rule (NOISE now fails TONAL at 6.2; HUM and ARC3 pass
HEX-OVER at +4.6) and every row check, and exited 1 on the REAL WINDOW alone
(a check on the picks, not a rule a candidate is picked on): 12 of the
window's 13 touches stood +11 to +39 dB over the fight in their note's
third-octave, and ONE stood +5.3. That touch came 0.125 s after the cast, and
on the cast's frame the foe (Aureole) fired its own ultimate -- rune-crack,
since Aureole has no arm -- whose 380 Hz partial, struck 0.16 s in, sits in
the touch's own band (G4, 392 Hz): the touch alone is 0.074 there, the foe's
cast 0.031. The touch is heard over it; it is not +6 dB over it. The gate was
ironhail's for a landing (every one >= +6). Round 4 takes the batch's gate for
a FREQUENT voice instead -- Zenith's tick (v98), struck as often as this touch
is (8.5 a window): the MEDIAN touch >= +6 dB -- and keeps a floor under every
touch, >= +3 dB (at least as loud as everything else in its band: never lost).
The printout now names every sound that began up to 0.5 s before a quiet
touch, not 50 ms (the masker here began 125 ms before). Nothing else changed:
the same candidates, rules and picks.

THE PICKS, on Chromium 151.0.7922.34, sc-lodestone-b205 6d736451a1ffc2df, fight
seeds 102601-102602 (152 fights), end to end 102651 (76 fights). Round 4 left
round 3's rows byte-identical (the real-window gate is a check on the picks,
not a rule they are picked on):

  cast   5 EVEN    A4 C5 E5 A5, each note a free bar's modes (a triangle and
                   sines at 2.76x and 5.40x, the upper decaying faster), a note
                   every 125 ms: audible 495 ms, every note after the first
                   jumps +32 dB or more in its own band at its onset, the first
                   struck in under 1 ms, TONAL 19.2; TOP -2.9 dB re the hit @
                   20.5 (its quietest draw), +18.3 re the wall, +22.4 dB over
                   the score where a phone hears it; register at most 0.66
                   (Zenith's cast). All five pass; LOW, RUNE and EVEN tie on
                   the register to 0.05 and on calls (12), and EVEN is the
                   most distinct unrounded -- a hair over LOW, which is the
                   same bar with its notes 100 ms apart. CHIME and GLASS lose
                   on the register (0.76 / 0.77: rune-crack, Zenith).
  touch  7 ARC3    a 12 ms highpass crack on a held square, A3 C4 D4 E4 G4
                   (measured 218 / 260 / 292 / 329 / 391 Hz, every step 201
                   cents or more): gone by 60 ms, rise under 1 ms, peak 0.424
                   at most on every count and draw, HARM -7.5 dB (a buzz);
                   loudest 50 ms -3.9 to -3.4 dB re the blow and +6.3 dB or
                   more over the hex-snap, which still stands +4.6 dB over it
                   at 2.6 kHz on one frame; register at most 0.43 (the cast).
                   HUM passes and ties it on register and step; ARC3 has 2
                   calls to HUM's 4. Every round-2 snap (ZAP, BUZZ, ARC, HIGH,
                   CRACKLE) is out on HEX-OVER; BUZZ and ARC on the peak too.
  close  1 MIRROR  the cast's notes re-struck in phase every ~11 ms, climbing
                   as its decay reversed, cut top note first: -9.0 dB under
                   the cast's top (-12.0 re the blow), ENV-CORR 0.93 with the
                   literal reversal, starts 1200 c over the root and ends on
                   it, gone 685 ms, +11.8 dB over the score. SHARP passes at
                   0.92; DESCEND (-0.33) and SLOW (0.23) are not reversals.
                   Its cost is the one number worth watching: 153 synth calls,
                   about 6 ms of main thread once a window (printed, not gated).
  In a real window (Lodestone v Aureole, side 1, seed 102602, 13 touches, all
  at count 5): the touches stand +5.3 to +39.3 dB over the fight in their own
  band, median +20.9 (the +5.3 is 125 ms after Aureole's own cast, above);
  the cast +11.1 dB, the close +27.8 dB. 4894 touches in the 152 fights: 70%
  carry count 5, 322 land inside the cast's first 0.5 s, over the chime.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (three arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm (the touch at
    counts -1, 0, 1..5, 7 and a missing `n`, on two noise draws) must
    reproduce its candidate to TOL; every other voice through the patched
    play (the hit at five weights with and without a crit, spark x3, wall,
    death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3, fork,
    scour x4, and every relic's cast and every sub-voice the ult arm names)
    must be unchanged; `ult/lodestone` must NOT be rune-crack any more;
  * the two tickRunes rows are applied to `Match.prototype.tickRunes`'s own
    source and run on real fights beside the unpatched one: every fight
    identical (over, clock, both hp, shields, positions, velocities, charges,
    both hex counts and clocks, winner and the whole runeTally) and every
    other voice call identical in order, kind and opts; one touch voice and
    one hex-snap per touch, on its step, the touch carrying the foe's count
    right after its hex; one close per window closed by its clock with both
    alive and none otherwise; one cast voice per cast; the unpatched runs
    play no touch, no close and no hex-snap from the runes. The same rows plus
    ONE sim write (the foe nudged 1e-9 on a touch) must come back NOT
    identical, or "identical" proves nothing. (The Sfx row cannot reach the
    simulation at all: `play` returns on its first line with no audio
    context, which is every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a
    temp folder, never the repo), loaded in a fresh browser after the first
    is closed: the page loads clean, its own SFX.play renders the arms to the
    lab's text, every other voice to the original page's, and its fights are
    identical to the original page's, with one voice per touch and close.
  * WITH OTHER RELICS' ROWS (`--peer-rows`, optional): each peer's Sfx rows
    and these applied to play()'s source in both orders render every arm of
    both identically.
  All anchors must occur exactly once in the game file, and every row is a
  `replace` that re-emits its anchor unchanged exactly once, so a later
  relic's row -- or the picture's -- anchored on the same line still applies,
  in either order.

Writes wavs to 05-reference/v102/lodestone-*.wav at RAW level (gitignored).
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
# it means in v98's and v101's labs. (Their module bodies only check their own
# candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env,
    env_corr, fmt, pcm, pitch, top_note, write_wav)
from bindweed_voice_lab import tonal  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "lodestone"
BLADE = 20.5                              # Lodestone's dmg (the stage-5 blade)
MASS = 5.0                                # the warhammer's mass (the clank control)
CAP = 5                                   # STATUS.hex.maxStacks (checked on the page)
COUNTS = list(range(1, CAP + 1))
CHORD = [0, 3, 7, 12]                     # A C E A: one note a wall (reading 1)
PENT = [0, 3, 5, 7, 10]                   # A C D E G: one note a count (reading 3)
CAST_AUD = 500.0                          # "0.5s total": the decay is solved to this
AUD_LO, AUD_HI = 430.0, 570.0             # the gate (reading 6)
TOUCH_GONE = 65.0                         # the snap's decay is solved to this at count 1
GONE_MAX = 80.0                           # "<=80ms"
PEAK_MAX = 0.5                            # "peak <=0.5"
TOUCH_REF_N = 3                           # the count the snap is level-matched at
UNDER_DB = 3.0                            # the snap over the hex-snap (reading 4)
CLOSE_UNDER_DB = 9.0                      # the close's level match under the cast
TOL = 1e-5                                # reproduction / transcription (-100 dB; see REPRO)
PHONE_HZ = 200.0                          # what a phone speaker reproduces (Culverin v96)


def root_hz(st):
    return 440.0 * 2 ** (st / 12)


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# =============================================================== THE CAST ===
# "a rising four-note rune chime, one per wall, 0.5s total". Four struck notes,
# A C E A from the candidate's root, one every `dt`; each note is a partial set
# (ratio, level, wave, decay share of D). The decay D is solved to AUDIBLE 500.
TIMBRE = {
    # a free bar's modes, the upper ones decaying faster: a chime
    "bar": [(1.0, 1.0, "triangle", 1.0), (2.76, 0.35, "sine", 0.5), (5.4, 0.12, "sine", 0.25)],
    # a sine and its octave: glass, harmonic
    "glass": [(1.0, 1.0, "sine", 1.0), (2.0, 0.3, "sine", 0.6)],
    # rune-crack's own partials (1 : 2.73 : 4.41, triangles): the school's metal
    "rune": [(1.0, 1.0, "triangle", 1.0), (2.73, 0.5, "triangle", 0.7), (4.41, 0.3, "triangle", 0.5)],
    # the NOISE control: each note a band-passed noise burst at its pitch (struck, not a note)
    "noise": [],
}
CAST_CANDIDATES = [
    ("1 CHIME", dict(root=12, dt=0.1, tim="bar"),
     "a free bar's modes (1 : 2.76 : 5.40), A5 C6 E6 A6, a note every 0.1 s -- the walls lighting "
     "over the picture's 0.3 s draw"),
    ("2 LOW", dict(root=0, dt=0.1, tim="bar"),
     "CHIME an octave down: A4 C5 E5 A5"),
    ("3 GLASS", dict(root=12, dt=0.1, tim="glass"),
     "a sine and its octave at 0.3 (harmonic: glass, not a bar), A5-A6"),
    ("4 RUNE", dict(root=0, dt=0.1, tim="rune"),
     "rune-crack's own partials (1 : 2.73 : 4.41, triangles) on each note, A4-A5: the school's metal"),
    ("5 EVEN", dict(root=0, dt=0.125, tim="bar"),
     "LOW with its notes spread over the whole 0.5 s (every 0.125 s)"),
]
CAST_CONTROLS = [
    ("0 CHORD", dict(root=0, dt=0.1, tim="bar", order="chord"),
     "LOW's four notes struck at once: one chord, not four notes"),
    ("0 FALL", dict(root=0, dt=0.1, tim="bar", order="down"),
     "LOW's notes falling, A5 E5 C5 A4: not rising"),
    ("0 NOISE", dict(root=0, dt=0.1, tim="noise"),
     "LOW's four notes as band-passed noise bursts (q 1.4) at their pitches: struck, but not notes"),
]


def cast_body(sp, g, D, ind=10):
    """The cast arm's body: four struck notes, A C E A from the root."""
    order = sp.get("order", "up")
    notes = CHORD[::-1] if order == "down" else CHORD
    tk = "t" if order == "chord" else f"t + k * {fmt(sp['dt'])}"
    L = [f"const g = {fmt(g)}, D = {fmt(D)};",
         f"[{', '.join(str(s) for s in notes)}].forEach((s, k) => {{",
         f"  const f = {fmt(root_hz(sp['root']))} * Math.pow(2, s / 12), tk = {tk};"]
    if sp["tim"] == "noise":
        L.append('  this._burst(tk, { freq: f, q: 1.4, gain: g, dur: D, type:"bandpass" });')
    for (r, k, ty, dfac) in TIMBRE[sp["tim"]]:
        fx = "f" if r == 1.0 else f"f * {fmt(r)}"
        gx = "g" if k == 1.0 else f"g * {fmt(k)}"
        dx = "D" if dfac == 1.0 else f"D * {fmt(dfac)}"
        L.append(f'  this._tone(tk, {{ freq: {fx}, gain: {gx}, dur: {dx}, type:"{ty}" }});')
    L.append("});")
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE TOUCH ===
# "a sharp electric snap (<=80ms, peak <=0.5) ... pitch steps up with the stack
# count". A crack (the spark) on a buzz (the arc) at the count's note.
TOUCH_CANDIDATES = [
    ("1 ZAP", dict(root=0, wave="square", glide=0.6, crack="hp"),
     "a 12 ms highpass crack on a square that sags to 0.6 of its note (a spark's zap); A4 C5 D5 E5 G5"),
    ("2 BUZZ", dict(root=0, wave="sawtooth", glide=None, crack="hp"),
     "the crack on a held sawtooth at the count's note: a buzz"),
    ("3 ARC", dict(root=0, wave="square", glide=None, crack="hp", fifth=True),
     "the crack on a held square and a square a fifth over it at 0.5: an arc's two-tone buzz"),
    ("4 HIGH", dict(root=12, wave="square", glide=0.6, crack="hp"),
     "ZAP an octave up: A5 C6 D6 E6 G6"),
    ("5 CRACKLE", dict(root=0, wave="square", glide=None, crack="crackle"),
     "three cracks 7 and 15 ms apart (a spark's crackle) on a held square"),
    # ROUND 3 (see THE ROUNDS): an octave under the lowest, clear of the hex-snap's band
    ("6 HUM", dict(root=-12, wave="square", glide=None, crack="crackle"),
     "round 3: CRACKLE an octave down, A3 C4 D4 E4 G4 -- an arc's low buzz under the spark"),
    ("7 ARC3", dict(root=-12, wave="square", glide=None, crack="hp"),
     "round 3: one 12 ms crack on a held square, A3-G4: the plainest low arc"),
]
TOUCH_CONTROLS = [
    ("0 PING", dict(root=0, wave="triangle", glide=None, crack="click"),
     "a triangle note on an 8 ms click: a chime, not an electric snap"),
    ("0 FLAT", dict(root=0, wave="square", glide=0.6, crack="hp", fixed=root_hz(0)),
     "ZAP at count 1's note for every count"),
    ("0 LONG", dict(root=0, wave="square", glide=0.6, crack="hp", fixD=0.3),
     "ZAP ringing 0.3 s"),
    ("0 LOUD", dict(root=0, wave="square", glide=0.6, crack="hp", gmul=3.0),
     "ZAP at 3x its gain"),
]


def touch_body(sp, g, D, ind=10):
    """The snap's text. The note is read off `p.n`, clamped to 1..CAP; `fixed`
    (the FLAT control) is one note for every count."""
    if sp.get("fixed") is not None:
        head = f"const f = {fmt(round(sp['fixed'], 2))}, g = {fmt(g)}, D = {fmt(D)};"
    else:
        head = (f"const n = clamp(Math.round(p.n || 1), 1, {CAP}), "
                f"f = {fmt(root_hz(sp['root']))} * Math.pow(2, [{', '.join(str(s) for s in PENT)}][n - 1] / 12), "
                f"g = {fmt(g)}, D = {fmt(D)};")
    L = [head]
    if sp["crack"] == "hp":
        L.append('this._burst(t, { freq: 6000, q: 0.7, gain: g * 0.5, dur: 0.012, type:"highpass" });')
    elif sp["crack"] == "crackle":
        L.append('[[0, 0.5], [0.007, 0.35], [0.015, 0.22]].forEach(([s, k]) =>')
        L.append('  this._burst(t + s, { freq: 6000, q: 0.7, gain: g * k, dur: 0.006, type:"highpass" }));')
    elif sp["crack"] == "click":
        L.append('this._burst(t, { freq: 6000, q: 0.8, gain: g * 0.8, dur: 0.008, type:"highpass" });')
    if sp["glide"]:
        L.append(f'this._tone(t, {{ freq: f, to: f * {fmt(sp["glide"])}, gain: g, dur: D, type:"{sp["wave"]}" }});')
    else:
        L.append(f'this._tone(t, {{ freq: f, gain: g, dur: D, type:"{sp["wave"]}" }}).frequency.value = f;')
    if sp.get("fifth"):
        L.append(f'this._tone(t, {{ freq: f * 1.5, gain: g * 0.5, dur: D * 0.7, type:"{sp["wave"]}" }})'
                 f'.frequency.value = f * 1.5;')
    return "\n".join(" " * ind + l for l in L)


# ============================================================== THE CLOSE ===
# "the chime reversed, quiet". Every candidate is the PICKED cast's own four
# notes, falling:
#   mirror   each note RE-STRUCK (every whole number of cycles nearest `every`,
#            in phase) at a level CLIMBING as the cast's decay reversed, cut at
#            its mirrored onset -- the top note first, the root last (the
#            literal reversal's shape: all four swell, and drop out from the
#            top down); each strike `Ds` long, so the cut takes Ds
#   descend  the cast's notes struck FALLING at its own spacing and decay
CLOSE_CANDIDATES = [
    ("1 MIRROR", dict(mode="mirror", Ds=0.1, every=0.011, stretch=1.0),
     "each note swells (re-struck ~11 ms apart, climbing as the cast's decay reversed) and cuts at its "
     "mirrored onset: the top note drops out first, the root last"),
    ("2 SHARP", dict(mode="mirror", Ds=0.05, every=0.011, stretch=1.0),
     "MIRROR with 50 ms strikes: a harder cut"),
    ("3 DESCEND", dict(mode="descend", stretch=1.0),
     "the cast's notes struck falling, A-E-C-A, at its own spacing and decay"),
    ("4 SLOW", dict(mode="mirror", Ds=0.1, every=0.011, stretch=1.6),
     "MIRROR over 1.6x the time: a slower going-dark"),
]
CLOSE_FLOOR_DB = 40.0                     # a mirrored note's climb starts this far under its top


def close_body(cp, csp, cg, cD, gc, ind=10):
    """The close's text, on the picked cast's figure (csp, cg, cD)."""
    tim = TIMBRE[csp["tim"]]
    st = cp.get("stretch", 1.0)
    dt, D = csp["dt"] * st, cD * st
    F = fmt(root_hz(csp["root"]))
    if cp["mode"] == "descend":
        L = [f"const g = {fmt(round(cg * gc, 6))}, D = {fmt(round(D, 4))};",
             f"[{', '.join(str(s) for s in CHORD[::-1])}].forEach((s, k) => {{",
             f"  const f = {F} * Math.pow(2, s / 12), tk = t + k * {fmt(round(dt, 4))};"]
        for (r, k, ty, dfac) in tim:
            fx = "f" if r == 1.0 else f"f * {fmt(r)}"
            gx = "g" if k == 1.0 else f"g * {fmt(k)}"
            dx = "D" if dfac == 1.0 else f"D * {fmt(dfac)}"
            L.append(f'  this._tone(tk, {{ freq: {fx}, gain: {gx}, dur: {dx}, type:"{ty}" }});')
        L.append("});")
        return "\n".join(" " * ind + l for l in L)
    # mirror: the literal reversal is (3 dt + D) long; note k (rising index)
    # cuts at c = (3 dt + D) - k dt; each partial climbs as its own decay
    # (80 dB-ish from its gain to 0.0001 over D x dfac) reversed.
    A = 20 * math.log10(0.0001 / cg)          # the cast's fundamental: dB from its gain to its floor
    L = [f"const top = {fmt(round(cg * gc, 6))}, D = {fmt(round(D, 4))}, A = {fmt(round(A, 3))};",
         f"[{', '.join(str(s) for s in CHORD)}].forEach((s, k) => {{",
         f"  const f = {F} * Math.pow(2, s / 12), c = {fmt(round(3 * dt, 4))} + D - k * {fmt(round(dt, 4))};",
         f"  const dt = Math.max(1, Math.round(f * {fmt(cp['every'])})) / f;",
         f"  const s0 = Math.max(0, c - D * {fmt(round(CLOSE_FLOOR_DB, 1))} / -A);",
         f"  for (let j = Math.ceil(s0 / dt); j * dt < c - 1e-9; j++){{",
         f"    const u = c - j * dt;"]
    for (r, k, ty, dfac) in tim:
        fx = "f" if r == 1.0 else f"f * {fmt(r)}"
        kx = "" if k == 1.0 else f" * {fmt(k)}"
        dd = "D" if dfac == 1.0 else f"(D * {fmt(dfac)})"
        L.append(f'    this._tone(t + j * dt, {{ freq: {fx}, gain: top{kx} * Math.pow(10, A * u / {dd} / 20), '
                 f'dur: {fmt(cp["Ds"])}, type:"{ty}" }}).frequency.value = {fx};')
    L += ["  }", "});"]
    return "\n".join(" " * ind + l for l in L)


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
TOUCH_ANCHOR = '        T.hexes += u.hex;'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultRunes = null; continue; }'

TOUCH_CODE = TOUCH_ANCHOR + '''
        /* REBUTTAL'S TOUCH (v70 §6.2: "a sharp electric snap (<=80ms, peak
           <=0.5) with the hex's own stun voice underneath if it lands; pitch
           steps up with the stack count"): once per touch, after its hex
           lands, pitched by the count the foe now carries (the tag's number,
           1-5; at the cap the hex's clock refreshes and it snaps at 5's
           note), and under it the hex's own voice, `hex-snap` -- the runic
           school's, the one Corollary's echo plays when its hex lands.
           Presentation only: SFX.play draws nothing, is a no-op headless,
           and nothing here is read back (lodestone_voice_lab: fights
           identical). */
        SFX.play("ult", { w: "lodestone-touch", n: foe.stacks("hex") });
        SFX.play("hex-snap");'''

CLOSE_CODE = '''      /* REBUTTAL'S CLOSE (v70 §6.2: "the chime reversed, quiet"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive --
         never on a death, and never once the fight is over (step() stops
         calling this after a kill, so a window still lit at the verdict
         plays nothing). Presentation only; nothing here is read back. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "lodestone-close" });
''' + CLOSE_ANCHOR

# the sim-write control: the same touch row with the foe nudged 1e-9 on a touch
TOUCH_CODE_BAD = TOUCH_CODE.replace(
    '        SFX.play("ult", { w: "lodestone-touch"',
    '        foe.vx += 1e-9;\n        SFX.play("ult", { w: "lodestone-touch"', 1)

_refuse(TOUCH_CODE + CLOSE_CODE, "sim rows")
for _c, _a in ((TOUCH_CODE, TOUCH_ANCHOR), (CLOSE_CODE, CLOSE_ANCHOR)):
    assert _c.count(_a) == 1, "a sim row must re-emit its anchor exactly once"
assert TOUCH_CODE_BAD != TOUCH_CODE


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


def peer_name(pf):
    """A peer rows file's relic: `<scratch>/batch/<relic>/stage6-voice/rows_final.json` -> "Relic"."""
    p_ = pathlib.Path(pf).parent
    return (p_.parent.name if p_.name.startswith("stage") else p_.name).capitalize()


def arms_code(C_, K_, Z_, info):
    cn, kn, zn = (X["name"].split()[1] for X in (C_, K_, Z_))
    c_cast = _wrap([
        f'LODESTONE\'S CAST, THE WALLS RUNED -- v70 §6.2: "a rising four-note rune chime, one per wall, '
        f'0.5s total". {cn}, of {info["n_cast"]}, picked on the numbers by `lodestone_voice_lab.py` under '
        f'Rick\'s "you pick i overrule" (v102). Lodestone had no arm and fell through to rune-crack, which '
        f'{info["n_rc"]} other relics on its stage-5 link still use, so this ADDS arms before that fallback '
        f'and leaves it alone.',
        f"One note a wall: A C E A, the score's tonic triad up through its octave, from {info['c_root']}, "
        f"{info['c_what']}, a note every {info['c_dt'] * 1000:.0f} ms, each struck (rise "
        f"{info['c_rise']:.0f} ms) and each jumping {info['c_jump']:.0f} dB or more in its own band at its "
        f"onset. Audible {info['c_aud']:.0f} ms; its loudest 50 ms {info['c_top']:+.1f} dB re Lodestone's "
        f"blow; {info['c_heard']:+.1f} dB over the score where a phone hears it. Register at most "
        f"{info['c_reg']:.2f} against rune-crack, the runic and warhammer casts, the seal's chime, "
        f"Zenith's cast and the blow."], 10)
    c_touch = _wrap([
        f'A WALL ANSWERS -- "a sharp electric snap (<=80ms, peak <=0.5) with the hex\'s own stun voice '
        f'underneath if it lands; pitch steps up with the stack count" (v70 §6.2). {kn}, of '
        f'{info["n_touch"]} (`lodestone_voice_lab.py`). `tickRunes` plays it once per touch, after the '
        f'hex lands, with n = the foe\'s hex count (the tag\'s number, 1-{CAP}), and `hex-snap` under it.',
        f"{info['k_what']} The note steps up the A-minor pentatonic with the count, {info['k_notes']} Hz at "
        f"1-{CAP} (measured {info['k_pp']} Hz, every step {info['k_step']:.0f} cents or more). Rise "
        f"{'under 1' if info['k_rise'] < 1 else format(info['k_rise'], '.0f')} ms; gone by "
        f"{info['k_gone']:.0f} ms and peak {info['k_peak']:.3f} at most, at every count and draw; its "
        f"harmonics {info['k_harm']:+.1f} dB re its note (a buzz); its loudest 50 ms {info['k_db0']:+.1f} to "
        f"{info['k_db1']:+.1f} dB re the blow and {info['k_over']:+.1f} dB or more over the hex-snap, which "
        f"still stands {info['k_hex']:+.1f} dB or more over it at 2.6 kHz. Register at most {info['k_reg']:.2f} "
        f"against the hex-snap, the wall tick, the blow, rune-crack, the clank, the burn and the cast."], 10)
    c_close = _wrap([
        f'THE RUNES GO DARK -- "the chime reversed, quiet" (v70 §6.2). {zn}, of {info["n_close"]} '
        f'(`lodestone_voice_lab.py`): {info["z_what"]} {info["z_db"]:+.1f} dB under the cast\'s top; gone '
        f'{info["z_gone"]:.0f} ms after the window shuts. Envelope correlation {info["z_corr"]:.2f} with the '
        f'literal reversal, which cannot ship: it needs an async render, and every clip rebuilds this synth '
        f'synchronously (v88 §6b). `tickRunes` plays it only when the window closes by its clock with both '
        f'fighters alive, never on a death and never at the verdict.'], 10)
    return (f'{_arm_head(ME, "the walls are runed")}\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["D"])}\n'
            f'{_arm_head(ME + "-touch", "a wall answers")}\n'
            f'{c_touch}\n{touch_body(K_["sp"], K_["g"], K_["D"])}\n'
            f'{_arm_head(ME + "-close", "and the runes go dark")}\n'
            f'{c_close}\n{close_body(Z_["cp"], C_["sp"], C_["g"], C_["D"], Z_["gc"])}\n'
            f'{SFX_ANCHOR}')


# ============================================================== THE PAGE ===
# events, each rendered at its own time on ONE synth:
#   ["play", at, kind, p]      the page's own SFX.play
#   ["body", at, src, p]       a candidate: its arm text run as (t, p) on the synth
#   ["arm",  at, kind, p]      the PATCHED play (the Sfx rows applied)
#   ["lit",  at, src, gain]    a body rendered DRY (no chain), trimmed, its
#                              samples reversed, x gain, into the chain at `at`
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
  const fns = new Map();
  const fn = (src) => { if (!fns.has(src)) fns.set(src, (0, eval)("(function(t, p){\n" + src + "\n})")); return fns.get(src); };
  const synth = (oc, chain) => {
    let cursor = 0;
    const S = Object.create(proto);
    S.ok = true; S.on = true;
    S.ctx = new Proxy(oc, { get(o, k){ if (k === "currentTime") return cursor;
      const v = Reflect.get(o, k); return typeof v === "function" ? v.bind(o) : v; } });
    S.bus = chain ? S.constructor.buildChain(oc, oc.destination)
                  : (() => { const g = oc.createGain(); g.connect(oc.destination); return g; })();
    S.noise = mkNoise(oc);
    const log = { burst: [], sweep: [], tone: 0 };
    S._burst = function(t, o, d){ log.burst.push(o.dur); return proto._burst.call(this, t, o, d); };
    S._sweep = function(t, o, d){ log.sweep.push(o.dur); return proto._sweep.call(this, t, o, d); };
    S._tone  = function(t, o, d){ log.tone++; return proto._tone.call(this, t, o, d); };
    return { S, log, at: (x) => { cursor = x; } };
  };
  const oc = new OC(1, Math.round(sr * secs), sr);
  const Y = synth(oc, true), S = Y.S, log = Y.log;
  const calls = [];
  for (const e of evs){
    Y.at(e[1]);
    const before = log.tone + log.burst.length + log.sweep.length;
    if (e[0] === "play") S.play(e[2], e[3]);
    else if (e[0] === "arm") patched.call(S, e[2], e[3]);
    else if (e[0] === "body") fn(e[2]).call(S, e[1], e[3] || {});
    else if (e[0] === "lit"){
      const dc = new OC(1, Math.round(sr * secs), sr), Z = synth(dc, false);
      Z.at(1.0); fn(e[2]).call(Z.S, 1.0, {});
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

# The tickRunes rows, applied to the real prototype and run beside the
# original; the survey of Rebuttal's windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "lodestone";
  const CAP = AC.STATUS.hex.maxStacks;
  const orig = P.tickRunes; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickRunes anchor occurs ${at} times in tickRunes()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inR = 0, hxBefore = 0, aliveIn = true;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-") || (kind === "hex-snap" && inR))
        calls.push({ step, k: kind === "hex-snap" ? "hex-snap" : w, n: p && p.n !== undefined ? p.n : null,
                     fs: foe.stacks("hex"), before: hxBefore, inR: !!inR,
                     keys: p ? Object.keys(p).join(",") : "" });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    P.tickRunes = function(dt){ inR++; hxBefore = foe.stacks("hex"); aliveIn = f.alive && foe.alive;
                                try { return impl.call(this, dt); } finally { inR--; } };
    const touchSteps = {}, castSteps = {}, wins = [];
    let n = 0, lt = 0, lc = 0, prev = null, W = null;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const T = f.runeTally, Z = f.ultRunes;
        if (T){
          if (T.touches > lt){ touchSteps[step] = T.touches - lt; lt = T.touches; }
          if (T.casts > lc){ castSteps[step] = T.casts - lc; lc = T.casts; }
        }
        if (Z && Z !== prev){ if (W && !W.end){ W.end = "recast"; W.endStep = step; }
                              W = { cast: m.t, castStep: step, end: null, endStep: null, close: null };
                              wins.push(W); }
        if (!Z && prev && W && !W.end){
          W.end = prev.t >= prev.dur ? (aliveIn ? "clock" : "clockDead") : "death"; W.endStep = step; W.close = m.t; }
        prev = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickRunes = orig; if (had) S.play = op; else delete S.play; }
    const T = f.runeTally || {};
    const st = (x) => x.status.hex ? [x.status.hex.stacks, x.status.hex.t] : null;
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.shield, m.b.shield, m.a.x, m.a.y, m.b.x, m.b.y,
                                  m.a.vx, m.a.vy, m.b.vx, m.b.vy, m.a.charge, m.b.charge, st(m.a), st(m.b),
                                  m.a.hexClock, m.b.hexClock, m.winner ? m.winner.w.id : null, T]),
             calls, other: JSON.stringify(other), touchSteps, castSteps, wins, T, steps: n };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, clockDead: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, castV = 0, touch = 0, touchV = 0, snaps = 0, closes = 0, rose = 0, atCap = 0, early = 0;
  const nh = new Array(CAP + 1).fill(0), pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a touch, close or rune hex-snap"]);
    for (const c of B.calls) if (c.k !== ME && !c.inR) bad.push([fid, sd, "a rune voice outside tickRunes", c.k]);
    for (const c of B.calls) if (c.k === ME && c.inR) bad.push([fid, sd, "the cast voice from inside tickRunes"]);
    const byStep = {};
    for (const c of B.calls) (byStep[c.step] = byStep[c.step] || []).push(c);
    const keys = new Set([...Object.keys(B.touchSteps), ...Object.keys(B.castSteps), ...Object.keys(byStep)]);
    for (const k of keys){
      const cs = byStep[k] || [];
      const tv = cs.filter(c => c.k === ME + "-touch"), hv = cs.filter(c => c.k === "hex-snap"),
            cv = cs.filter(c => c.k === ME);
      const nt = B.touchSteps[k] || 0, nc = B.castSteps[k] || 0;
      if (tv.length !== nt || hv.length !== nt || cv.length !== nc)
        bad.push([fid, sd, "step " + k, "touch", nt, tv.length, "hex-snap", hv.length, "cast", nc, cv.length]);
      for (const c of tv){
        if (!(Number.isInteger(c.n) && c.n >= 1 && c.n <= CAP && c.n === c.fs) || c.keys !== "w,n")
          bad.push([fid, sd, "a touch voice's n is not the foe's count", c.n, c.fs, c.keys]);
        else { nh[c.n]++; if (c.n > c.before) rose++; else atCap++; }
      }
      for (const c of hv) if (c.keys !== "") bad.push([fid, sd, "the hex-snap carries opts", c.keys]);
      for (const c of cv) if (c.keys !== "w") bad.push([fid, sd, "the cast carries opts", c.keys]);
      touch += nt; touchV += tv.length; snaps += hv.length; casts += nc; castV += cv.length;
    }
    for (const W of B.wins){
      ends[W.end]++;
      const cl = B.calls.filter(c => c.k === ME + "-close" && c.step >= W.castStep &&
                                     (W.endStep === null || c.step <= W.endStep));
      if (W.end === "clock"){
        if (cl.length !== 1) bad.push([fid, sd, "clock window closes", cl.length]);
        else if (cl[0].step !== W.endStep) bad.push([fid, sd, "close not on the window's last step", cl[0].step, W.endStep]);
        const nt = Object.keys(B.touchSteps).filter(s => +s >= W.castStep && +s <= W.endStep).length;
        pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, touches: nt });
      } else if (cl.length) bad.push([fid, sd, W.end + " window played a close"]);
      for (const s of Object.keys(B.touchSteps)) if (+s >= W.castStep && +s < W.castStep + 60) early++;
    }
    closes += B.calls.filter(c => c.k === ME + "-close").length;
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, touch, touchV, snaps, closes,
           rose, atCap, early, nh, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Rebuttal's (the hex-snap under a touch is).
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "lodestone";
  const orig = P.tickRunes; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = []; let inR = 0;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w
              : (kind === "hex-snap" && inR) ? "hex-snap" : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickRunes = function(dt){ inR++; try { return patched.call(this, dt); } finally { inR--; } };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickRunes = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "lodestone";
  const CAP = AC.STATUS.hex.maxStacks;
  const res = [];
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = []; let inR = 0, aliveIn = true;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    const orig = P.tickRunes;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, p.n === undefined ? null : p.n, foe.stacks("hex")]);
      else if (kind === "hex-snap" && inR) log.push(["hex-snap", null, null]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    P.tickRunes = function(dt){ inR++; aliveIn = f.alive && foe.alive; try { return orig.call(this, dt); } finally { inR--; } };
    let n = 0, pz = null, clocks = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++;
            const Z = f.ultRunes; if (!Z && pz && pz.t >= pz.dur && aliveIn) clocks++; pz = Z; } }
    finally { P.tickRunes = orig; if (had) S.play = op; else delete S.play; }
    const T = f.runeTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y,
                                    m.a.stacks("hex"), m.b.stacks("hex"),
                                    m.winner ? m.winner.w.id : null, f.runeTally || null]),
               casts: T.casts || 0, touches: T.touches || 0, clocks,
               castV: log.filter(e => e[0] === ME).length,
               touchV: log.filter(e => e[0] === ME + "-touch").length,
               badN: log.filter(e => e[0] === ME + "-touch" && (e[1] !== e[2] || e[1] < 1 || e[1] > CAP)).length,
               snapV: log.filter(e => e[0] === "hex-snap").length,
               closeV: log.filter(e => e[0] === ME + "-close").length,
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
  for (const [k, kind, p] of [["cast", "ult", { w: "lodestone" }], ["touch", "ult", { w: "lodestone-touch", n: 3 }],
                              ["close", "ult", { w: "lodestone-close" }], ["hex-snap", "hex-snap", {}],
                              ["hit", "hit", { dmg: 20.5, crit: false }]]){
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


def bed_p90(bseg, win=0.1, hop=0.05):
    np = _np()
    W = int(win * SR); H = int(hop * SR)
    B = np.array([bands(bseg[i:i + W]) for i in range(0, len(bseg) - W, H)])
    return np.percentile(B, 90, axis=0)


def heard(x, p90, a=0.0, win=0.1, lo=PHONE_HZ, hi=12000.0):
    """HEARD (ironhail_voice_lab's round-2 definition, restated): the loudest
    ratio of the voice's third-octaves centred at or above `lo`, over
    [a, a + win] s from the event, to the score's p90 in the same
    third-octave, dB, and where."""
    y = x[int((T0 + a) * SR):int((T0 + a) * SR) + int(win * SR)]
    b = bands(y)
    best = max(((b[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))
    return db(best[0]), best[1]


def rise_in(x, a, b):
    """RISE (10 -> 90% of the 1 ms envelope, ms) over [a, b] s from the event."""
    np = _np()
    y = x[int((T0 + a) * SR):int((T0 + b) * SR)]
    e1, _ = env(y, 0.001, 0.001)
    m1 = e1.max()
    return float(int(np.argmax(e1 > 0.9 * m1)) - int(np.argmax(e1 > 0.1 * m1)))


def strikes(x, sp):
    """STRIKES: each note after the first, its third-octave over the 40 ms after
    its onset against the 40 ms before, dB (rising schedule); and the first
    note's presence, dB re the loudest note's after-window."""
    dt = sp["dt"]
    f = [root_hz(sp["root"]) * 2 ** (s / 12) for s in CHORD]
    after = [band_rms(x, f[k], T0 + k * dt + 0.002, T0 + k * dt + 0.042) for k in range(4)]
    before = [band_rms(x, f[k], T0 + k * dt - 0.038, T0 + k * dt + 0.002) for k in range(4)]
    jumps = [db(after[k] / max(before[k], 1e-12)) for k in range(1, 4)]
    first = db(after[0] / max(after))
    return jumps, first


def harm(x, a=0.010, b=0.045):
    """HARM: the power in harmonics 2-8 of the note (the FFT peak 150-4000 Hz
    over [a, b]) against the note's own third-octave, dB."""
    np = _np()
    f0 = pitch(x, T0 + a, T0 + b, lo=150.0, hi=4000.0)
    seg = x[int((T0 + a) * SR):int((T0 + b) * SR)]
    P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 16)) ** 2
    fr = np.fft.rfftfreq(1 << 16, 1 / SR)

    def band(fc):
        return float(P[(fr >= fc / 2 ** (1 / 6)) & (fr < fc * 2 ** (1 / 6))].sum())
    return 10 * math.log10(max(sum(band(k * f0) for k in range(2, 9)), 1e-30) / max(band(f0), 1e-30)), f0


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v70 §6.2 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.5s total': AUDIBLE 430-570 ms; 'four-note ... rising, one per wall': "
    "each of A C E A struck at its own onset in rising order -- STRIKES: every "
    "note after the first jumps >= 6 dB in its own third-octave at its onset, "
    "and the first is there (>= -20 dB re the loudest); 'chime': the first note "
    "struck (RISE0 <= 3 ms) and TONAL > 10 dB (notes, not noise: v101's line). "
    "Heard: TOP "
    "between 0.5x the hit @ 20.5's loudest 50 ms on its LOUDEST draw and 1.0x on "
    "its QUIETEST (heard like a blow, never over one), and HEARD (at or above "
    "200 Hz, the first 100 ms) >= +6 dB over the score. Register against "
    "rune-crack, the school's casts and the type's (read off the page), the "
    "seal's chime, Zenith's cast and the hit @ 20.5 each <= 0.80. Tiebreak: the "
    "most distinct register (the highest of those, to 0.05), then the fewest "
    "synth calls, then the most distinct register unrounded.")

TOUCH_RULE = (
    "'<=80ms': GONE <= 80 ms at every count on every draw; 'sharp': RISE <= 1 ms "
    "and the peak in the first 10 ms at every count; 'electric': HARM >= -12 dB "
    "at every count (a buzz, not a ping); 'peak <=0.5': the sample peak <= 0.5 "
    "at every count on every draw; 'pitch steps up with the stack count': the "
    "PITCH (3-25 ms) rises >= 150 cents with every count 1-5; 'the hex's own "
    "stun voice underneath': the loudest 50 ms at every count on every draw at "
    "least 3 dB over the hex-snap's loudest draw and at most 1.0x the hit @ "
    "20.5's quietest (never over a blow), and on one frame with the hex-snap "
    "the snap keeps its own band within 1.5 dB of the snap alone and the "
    "hex-snap stands >= +3 dB over the snap in its own 2.6 kHz band (HEX-OVER: "
    "heard under it, not lost in it); heard: "
    "HEARD (at or above 200 Hz) >= +6 dB at every count. Register (at count 3) "
    "against the hex-snap, the wall tick, the hit @ 20.5, rune-crack, the clank, "
    "the burn and the picked cast each <= 0.80. Tiebreak: the most distinct "
    "register (to 0.05), then the count heard best (the largest smallest step, "
    "to 10 cents), then the fewest calls.")

CLOSE_RULE = (
    "'reversed': ENV-CORR with the LITERAL reversal of the picked cast >= 0.80, "
    "and the notes fall -- the TOP NOTE over the first half of AUDIBLE at least "
    "700 cents over the root, the PITCH over the last 100 ms within 50 cents of "
    "the root; 'quiet': the loudest 50 ms <= 0.5x the cast's (-6 dB), still "
    "heard: HEARD (at or above 200 Hz) over its loudest 100 ms >= +6 dB over the "
    "score; GONE <= 1300 ms. Tiebreak: the highest ENV-CORR (to 0.01), then the "
    "fewest synth calls.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not AUD_LO <= M["aud"] <= AUD_HI: why.append(f"audible {M['aud']:.0f} ms, not {AUD_LO:.0f}-{AUD_HI:.0f}")
    if M["jump"] < 6: why.append(f"a note jumps only {M['jump']:+.1f} dB at its onset (not four struck notes, rising)")
    if M["first"] < -20: why.append(f"the first note {M['first']:+.1f} dB re the loudest")
    if M["rise0"] > 3: why.append(f"the first note rises in {M['rise0']:.0f} ms (not struck)")
    if M["tonal"] <= 10: why.append(f"tonal {M['tonal']:.1f} dB <= 10 (noise, not notes)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def touch_why(M, lev):
    why = []
    if M["gone_max"] > GONE_MAX: why.append(f"gone at {M['gone_max']:.0f} ms (> {GONE_MAX:.0f})")
    if M["rise_max"] > 1: why.append(f"rise {M['rise_max']:.0f} ms (> 1)")
    if M["pk_max"] > 10: why.append(f"peak at {M['pk_max']:.0f} ms (> 10)")
    if M["harm_min"] < -12: why.append(f"harmonics {M['harm_min']:+.1f} dB re its note (< -12: not a buzz)")
    if M["peak_max"] > PEAK_MAX: why.append(f"peak {M['peak_max']:.3f} > {PEAK_MAX}")
    if not M["rising"]: why.append("the pitch does not step up with every count (" +
                                   "/".join(f"{p_:.0f}" for p_ in M["pitch"]) + " Hz)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f} (not over the hex-snap)")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (over the blow)")
    if "keep_snap" in M and M["keep_snap"] < -1.5:
        why.append(f"on one frame with the hex-snap it keeps {M['keep_snap']:+.1f} dB of its band")
    if "hex_over" in M and M["hex_over"] < 3:
        why.append(f"on one frame the hex-snap stands only {M['hex_over']:+.1f} dB over it at 2.6 kHz (lost in it)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    if M["corr"] < 0.80: why.append(f"env-corr {M['corr']:.2f} < 0.80")
    if M["c_first"] < 700: why.append(f"its first half's top note only {M['c_first']:+.0f} c over the root")
    if abs(M["c_last"]) > 50: why.append(f"ends {M['c_last']:+.0f} c off the root")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 over the score")
    if M["gone"] > 1300: why.append(f"gone at {M['gone']:.0f} ms")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Lodestone's stage 5 (the runes, the hurl, the blade)")
    ap.add_argument("--out", default="../05-reference/v102")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=102601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "touch": TOUCH_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickRunes touch", TOUCH_ANCHOR), ("tickRunes close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if '"lodestone-touch"' in html or '"lodestone-close"' in html or re.search(r'(?<![\w.])w === "lodestone"', html):
        raise SystemExit(f"{gp.name} already carries Rebuttal's voices -- run on the stage-5 link")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nREBUTTAL -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
          const me = AC.WEAPONS.find(w => w.id === "lodestone");
          return { arms, kinds, cap: AC.STATUS.hex.maxStacks, dmg: me.dmg, mass: me.mass, u: me.ult,
                   W: AC.WEAPONS.map(w => [w.id, w.aff, w.shape]) };
        }""")
        if info0["cap"] != CAP:
            raise SystemExit(f"STATUS.hex.maxStacks is {info0['cap']}, not {CAP}")
        u0 = info0["u"]
        if abs(info0["dmg"] - BLADE) > 1e-9 or u0.get("kind") != "runes" or u0.get("hex") != 1 \
                or u0.get("dur") != 8 or u0.get("hurl") != 700 or info0["mass"] != MASS:
            raise SystemExit(f"Lodestone on this page is not stage 5's: dmg {info0['dmg']}, ult {u0}")
        print(f"  Lodestone: blade {info0['dmg']}, mass {info0['mass']}, ult {u0['kind']} dur {u0['dur']} hex "
              f"{u0['hex']} hurl {u0['hurl']} cd {u0['cd']} pad {u0['pad']} charge {u0['charge']}; hex cap {CAP}")
        arms_now = set(info0["arms"])
        SCHOOL = tuple(w for w, aff, sh in info0["W"] if aff == "runic" and w != ME and w in arms_now)
        TYPE = tuple(w for w, aff, sh in info0["W"] if sh == "warhammer" and w != ME and w in arms_now)
        FALL = tuple(w for w, aff, sh in info0["W"] if w not in arms_now)
        print(f"  the school's casts (runic, with an arm): {', '.join(SCHOOL)};  the type's (warhammer): "
              f"{', '.join(TYPE)}")
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
                ("hit@20.5", ["play", T0, "hit", {"dmg": BLADE, "crit": False}]),
                ("hex-snap", ["play", T0, "hex-snap", {}]),
                ("wall", ["play", T0, "wall", {}]),
                ("seal", ["play", T0, "seal", {}]),
                ("zenith", ["play", T0, "ult", {"w": "morningstar"}]),
                ("clank", ["play", T0, "clank", {"mass": MASS}]),
                ("burn", ["play", T0, "spark", {}]),
                ("death", ["play", T0, "death", {}])]
        REFS += [(r_, ["play", T0, "ult", {"w": r_}]) for r_ in SCHOOL + TYPE if r_ != "axiom"]
        REFS += [(f"{r_} now", ["play", T0, "ult", {"w": r_}]) for r_ in FALL]
        RD = dict(REFS)
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
        # the noise draws
        SCH = tuple("BAR" if r_ == "axiom" else r_ for r_ in SCHOOL)
        DKEYS = ("hit@20.5", "wall", "rune-crack", "hex-snap", "seal", "zenith", "clank", "burn") + SCH + TYPE
        D = {k: [] for k in DKEYS}
        for sd in NOISE_SEEDS:
            for k in D:
                x_ = R([RD[k]], seed=sd)[0]
                D[k].append(basic(x_))
        h_lo, h_hi = min(m["top"] for m in D["hit@20.5"]), max(m["top"] for m in D["hit@20.5"])
        x_lo, x_hi = min(m["top"] for m in D["hex-snap"]), max(m["top"] for m in D["hex-snap"])
        w_hi = max(m["top"] for m in D["wall"])
        print(f"  across {len(NOISE_SEEDS)} draws, loudest 50 ms: the hit @ 20.5 {h_lo:.4f}-{h_hi:.4f} (peak "
              f"{min(m['peak'] for m in D['hit@20.5']):.3f}-{max(m['peak'] for m in D['hit@20.5']):.3f}); the hex-snap "
              f"{x_lo:.4f}-{x_hi:.4f} = {db(x_hi / h_lo):+.1f} dB re the blow at most; the wall tick up to {w_hi:.4f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        P90 = bed_p90(bseg)

        def reg(DB, key):
            DB = DB if isinstance(DB, list) else [DB] * len(NOISE_SEEDS)
            return float(np.median([cos(DB[i], D[key][i]["bands"]) for i in range(len(DB))]))

        def reg_to(DB, DB2):
            DB = DB if isinstance(DB, list) else [DB] * len(NOISE_SEEDS)
            DB2 = DB2 if isinstance(DB2, list) else [DB2] * len(NOISE_SEEDS)
            return float(np.median([cos(DB[i], DB2[i]) for i in range(len(DB))]))

        rec["levels"] = dict(hit=[h_lo, h_hi], hexsnap=[x_lo, x_hi], wall_hi=w_hi)
        wav("lodestone-ctl-runecrack.wav", rcx)
        wav("lodestone-ctl-hit20.wav", ctl["hit@20.5"]["x"])
        wav("lodestone-ctl-hexsnap.wav", ctl["hex-snap"]["x"])
        wav("lodestone-ctl-seal.wav", ctl["seal"]["x"])
        wav("lodestone-ctl-bar.wav", ctl["BAR"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a rising four-note rune chime, one per wall, 0.5s total'. A C E A from the root. "
              f"Level-matched: TOP {tgt_c:.4f} (the centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the decay "
              f"solved to AUDIBLE {CAST_AUD:g} ms")

        def cx(sp, g, D_, seed=None):
            return R([["body", T0, cast_body(sp, g, D_), {}]], secs=2.5, seed=seed)

        def calib_cast(sp):
            g, D_ = 0.15, 0.25
            for _ in range(3):
                # a noise burst cannot outlast the 0.6 s buffer (CLAUDE.md 4.5; the lab refuses > 0.55 s)
                lo_, hi_ = math.log(0.03), math.log(0.55 if sp["tim"] == "noise" else 1.5)
                for _ in range(14):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, math.exp(mid))[0])["aud"] < CAST_AUD: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = float(f"{g * tgt_c / basic(cx(sp, g, D_)[0])['top']:.4g}")
            return g, D_

        CREFS = ("rune-crack",) + SCH + TYPE + ("seal", "zenith", "hit@20.5")

        def cast_measure(sp, g, D_, name):
            x, calls = cx(sp, g, D_)
            x2, _ = cx(sp, g, D_)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit("a cast render does not reproduce")
            M = basic(x); M.update(x=x, calls=calls[0], g=g, D=D_, name=name, sp=sp)
            # a noise-built body is read over the twelve draws (round 3); a noise-free one is the same on each
            noisy = "_burst" in cast_body(sp, g, D_) or "_sweep" in cast_body(sp, g, D_)
            draws = [cx(sp, g, D_, seed=sd)[0] for sd in (NOISE_SEEDS if noisy else NOISE_SEEDS[:2])]
            bs = [basic(d_) for d_ in draws + [x]]
            M["top_lo"] = min(b_["top"] for b_ in bs); M["top_hi"] = max(b_["top"] for b_ in bs)
            M["jumps"], M["first"] = strikes(x, dict(sp, order="up"))
            M["jump"] = min(M["jumps"])
            M["rise0"] = rise_in(x, 0.0, sp["dt"] if sp.get("order", "up") != "chord" else 0.1)
            M["tonal"] = tonal(draws if noisy else [x], T0 + M["a0"] / 1000, T0 + (M["a0"] + M["aud"]) / 1000,
                               200.0, 8000.0)
            M["heard"], M["heard_at"] = heard(x, P90)
            M["DB"] = bands(x[int(T0 * SR):])
            M["regs"] = {k: reg(M["DB"], k) for k in CREFS}
            M["why"] = cast_why(M, lev_c)
            return M

        abbr = {k: k[:4] for k in CREFS}
        abbr.update({"rune-crack": "rc", "hit@20.5": "hit", "zenith": "zen"})
        print(f"  {'cand':<9}{'g':>7}{'D':>6}{'calls':>6}{'top':>8}{'aud':>5}{'@top':>5}{'jumps dB':>16}{'1st':>6}"
              f"{'rise0':>6}{'tonal':>6}{'heard':>7}{'cen':>6}" + "".join(f"{abbr[k]:>5}" for k in CREFS))

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<9}{M['g']:>7.4g}{M['D']:>6.3g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud']:>5.0f}"
                  f"{M['top_at'] * 1000:>5.0f}{'/'.join(f'{j:.0f}' for j in M['jumps']):>16}{M['first']:>6.1f}"
                  f"{M['rise0']:>6.0f}{M['tonal']:>6.1f}{M['heard']:>+7.1f}{M['cen']:>6.0f}"
                  + "".join(f"{r_[k]:>5.2f}" for k in CREFS))

        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, D_ = calib_cast(sp)
            M = cast_measure(sp, g, D_, name)
            rows_c.append(M); cast_line(M)
            wav(f"lodestone-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for name, sp, blurb in CAST_CONTROLS:
            g, D_ = calib_cast(sp)
            M = cast_measure(sp, g, D_, name)
            ctlc.append(M); cast_line(M)
            wav(f"lodestone-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for name, ev in (("0 SEAL", RD["seal"]), ("0 RC-NOW", ["play", T0, "ult", {"w": ME}])):
            x, calls = R([ev], secs=2.5)
            M = basic(x); M.update(x=x, calls=calls[0], g=0.0, D=0.0, name=name, sp=None)
            draws = [R([ev], secs=2.5, seed=sd)[0] for sd in NOISE_SEEDS]
            bs = [basic(d_) for d_ in draws]
            M["top_lo"] = min(b_["top"] for b_ in bs); M["top_hi"] = max(b_["top"] for b_ in bs)
            M["jumps"], M["first"] = strikes(x, CAST_CANDIDATES[1][1]); M["jump"] = min(M["jumps"])
            M["rise0"] = rise_in(x, 0.0, 0.1)
            M["tonal"] = tonal(draws, T0 + M["a0"] / 1000, T0 + (M["a0"] + M["aud"]) / 1000, 200.0, 8000.0)
            M["heard"], M["heard_at"] = heard(x, P90)
            M["DB"] = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["regs"] = {k: reg(M["DB"], k) for k in CREFS}
            M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES + CAST_CONTROLS:
            print(f"    {name:<9} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print("    0 SEAL    the seal's own chime played as the cast -- a control\n"
              "    0 RC-NOW  what ult/lodestone plays today (rune-crack) -- a control")
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
                                                          rows_c[i]["calls"], max(rows_c[i]["regs"].values())))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, D {C_['D']}; {C_['calls']} synth calls; TOP "
              f"{db(C_['top'] / h_lo):+.1f} dB re the hit @ 20.5 (quietest draw), {db(C_['top'] / w_hi):+.1f} dB re "
              f"the wall; notes jump {C_['jump']:+.1f} dB or more at their onsets")

        # ---- THE TOUCH -----------------------------------------------------
        lev_k = dict(lo=x_hi * 10 ** (UNDER_DB / 20), hi=1.0 * h_lo)
        tgt_k = math.sqrt(lev_k["lo"] * lev_k["hi"])
        print(f"\nTOUCH -- 'a sharp electric snap (<=80ms, peak <=0.5) with the hex's own stun voice underneath if "
              f"it lands; pitch steps up with the stack count'.\n  Level-matched: TOP {tgt_k:.4f} at count "
              f"{TOUCH_REF_N} (the centre of {lev_k['lo']:.4f}-{lev_k['hi']:.4f}: {UNDER_DB:g} dB over the hex-snap's "
              f"loudest draw .. the blow's quietest), the decay solved to GONE {TOUCH_GONE:g} ms at count 1")

        def kx(sp, g, D_, n, seed=None):
            return R([["body", T0, touch_body(sp, g, D_), {"n": n}]], secs=1.5, seed=seed)

        def calib_touch(sp):
            g, D_ = 0.1, 0.06 if sp.get("fixD") is None else sp["fixD"]
            for _ in range(3):
                if sp.get("fixD") is None:
                    lo_, hi_ = math.log(0.01), math.log(0.5)
                    for _ in range(14):
                        mid = 0.5 * (lo_ + hi_)
                        if basic(kx(sp, g, math.exp(mid), 1)[0])["gone"] < TOUCH_GONE: lo_ = mid
                        else: hi_ = mid
                    D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = float(f"{g * tgt_k / basic(kx(sp, g, D_, TOUCH_REF_N)[0])['top']:.4g}")
            if sp.get("gmul"):
                g = float(f"{g * sp['gmul']:.4g}")
            return g, D_

        KREFS = ("hex-snap", "wall", "hit@20.5", "rune-crack", "clank", "burn")

        def touch_measure(rfn, name, sp, g, D_, calls, both=True):
            """rfn(n, seed) -> the snap at count n."""
            M = {"name": name, "sp": sp, "g": g, "D": D_, "calls": calls}
            xs, pit, tops, gones, rises, pks, peaks, harms, hrd = {}, [], [], [], [], [], [], [], []
            for n in COUNTS:
                x = rfn(n, None)
                if float(np.abs(x - rfn(n, None)).max()) > TOL:
                    raise SystemExit(f"touch {name} does not reproduce")
                xs[n] = x
                b_ = basic(x)
                rises.append(b_["rise"]); pks.append(b_["pk_ms"])
                pit.append(pitch(x, T0 + 0.003, T0 + 0.025, lo=150.0, hi=4000.0))
                harms.append(harm(x)[0])
                hrd.append(heard(x, P90))
                draws = [rfn(n, sd) for sd in NOISE_SEEDS]
                for d0 in [x] + draws:
                    bd = basic(d0)
                    tops.append(bd["top"]); gones.append(bd["gone"]); peaks.append(bd["peak"])
                if n == TOUCH_REF_N:
                    M["DB"] = [bands(d0[int(T0 * SR):]) for d0 in draws]
            M.update(xs=xs, x=xs[TOUCH_REF_N], pitch=pit, top_lo=min(tops), top_hi=max(tops), gone_max=max(gones),
                     rise_max=max(rises), pk_max=max(pks), peak_max=max(peaks), harm_min=min(harms), harms=harms,
                     heard=min(h_[0] for h_ in hrd), heard_at=[h_[1] for h_ in hrd])
            M["rising"] = all(pit[i + 1] > pit[i] * 2 ** (150 / 1200) for i in range(len(pit) - 1))
            M["minstep"] = min(cents(pit[i + 1], pit[i]) for i in range(len(pit) - 1))
            M["regs"] = {k: reg(M["DB"], k) for k in KREFS}
            M["regs"]["cast"] = reg_to(M["DB"], C_["DB"])
            if both:
                # ON ONE FRAME with the hex-snap: each in its own band, together vs alone
                ks, kh = [], []
                for n in COUNTS:
                    xb = rfn(n, None, with_hex=True)
                    fk = pit[n - 1]
                    ks.append(db(band_rms(xb, fk, T0, T0 + 0.05) / band_rms(xs[n], fk, T0, T0 + 0.05)))
                    kh.append(db(band_rms(xb, 2600.0, T0, T0 + 0.03) / band_rms(xs[n], 2600.0, T0, T0 + 0.03)))
                M["keep_snap"] = min(ks); M["hex_over"] = min(kh)
                M["keep_all"] = (ks, kh)
            M["why"] = touch_why(M, lev_k)
            return M

        def mk_rfn(sp, g, D_):
            body = touch_body(sp, g, D_)

            def f_(n, sd, with_hex=False):
                evs = [["body", T0, body, {"n": n}]]
                if with_hex:
                    evs.append(["play", T0, "hex-snap", {}])
                return R(evs, secs=1.5, seed=sd)[0]
            return f_

        print(f"  {'cand':<10}{'g':>7}{'D':>7}{'calls':>6}{'top':>16}{'gone':>5}{'rise':>5}{'pk@':>4}{'peak':>7}"
              f"{'harm':>6}{'pitch Hz (count 1-5)':>28}{'step':>5}{'heard':>7}{'keep/hex':>11}"
              + "".join(f"{k[:4]:>5}" for k in ("hex", "wall", "hit", "rc", "clnk", "burn", "cast")))

        def touch_line(M):
            r_ = M["regs"]
            ps = "/".join(f"{p_:.0f}" for p_ in M["pitch"])
            kp = f"{M['keep_snap']:+.1f}/{M['hex_over']:+.1f}" if "keep_snap" in M else "-"
            print(f"  {M['name']:<10}{M['g']:>7.4g}{M['D']:>7.3g}{M['calls']:>6d}{M['top_lo']:>8.4f}-{M['top_hi']:<7.4f}"
                  f"{M['gone_max']:>5.0f}{M['rise_max']:>5.0f}{M['pk_max']:>4.0f}{M['peak_max']:>7.3f}"
                  f"{M['harm_min']:>6.1f}{ps:>28}{M['minstep']:>5.0f}{M['heard']:>+7.1f}{kp:>11}" +
                  "".join(f"{r_[k]:>5.2f}" for k in KREFS + ("cast",)))

        rows_k = []
        for name, sp, blurb in TOUCH_CANDIDATES:
            g, D_ = calib_touch(sp)
            rfn = mk_rfn(sp, g, D_)
            calls = R([["body", T0, touch_body(sp, g, D_), {"n": 1}]], secs=1.5)[1][0]
            M = touch_measure(rfn, name, sp, g, D_, calls)
            rows_k.append(M); touch_line(M)
            for n in (1, CAP):
                wav(f"lodestone-touch-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
            wav(f"lodestone-touch-{name.replace(' ', '-').lower()}-n3-hexsnap.wav", rfn(3, None, with_hex=True))
        ctlk = []
        for name, sp, blurb in TOUCH_CONTROLS:
            g, D_ = calib_touch(sp)
            rfn = mk_rfn(sp, g, D_)
            calls = R([["body", T0, touch_body(sp, g, D_), {"n": 1}]], secs=1.5)[1][0]
            M = touch_measure(rfn, name, sp, g, D_, calls)
            ctlk.append(M); touch_line(M)
            wav(f"lodestone-touch-{name.replace(' ', '-').lower()}.wav", M["x"])
        # HEX: the hex-snap alone, as the touch
        M = touch_measure(lambda n, sd, with_hex=False: R([["play", T0, "hex-snap", {}]] +
                                                         ([["play", T0, "hex-snap", {}]] if with_hex else []),
                                                         secs=1.5, seed=sd)[0],
                          "0 HEX", {"root": 0}, 0.0, 0.0, 3, both=False)
        ctlk.append(M); touch_line(M)
        for (name, _sp, blurb) in TOUCH_CANDIDATES + TOUCH_CONTROLS:
            print(f"    {name:<10} {blurb}" + (" -- a control" if name.startswith("0") else ""))
        print("    0 HEX      the hex-snap alone, as the touch -- a control")
        print("  'keep/hex' = on one frame with the hex-snap, against the snap alone: the snap's own band / the "
              "2.6 kHz band (HEX-OVER), dB (the worst count)")
        print(f"  RULE  {TOUCH_RULE}")
        for M in rows_k:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        for M in ctlk:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_k, "touch")
        ki = fb if ok is None else min(ok, key=lambda i: (round(max(rows_k[i]["regs"].values()) / 0.05),
                                                          -round(rows_k[i]["minstep"] / 10), rows_k[i]["calls"]))
        K_ = rows_k[ki]
        print(f"  PICK  {K_['name']}  g {K_['g']}, D {K_['D']}; notes " +
              " / ".join(f"{p_:.0f}" for p_ in K_["pitch"]) + f" Hz; loudest 50 ms {db(K_['top_lo'] / h_lo):+.1f} to "
              f"{db(K_['top_hi'] / h_lo):+.1f} dB re the hit @ 20.5 (quietest draw), {db(K_['top_lo'] / x_hi):+.1f} dB "
              f"or more over the hex-snap; peak {K_['peak_max']:.3f} at most")

        # ---- THE CLOSE -----------------------------------------------------
        cast_top = C_["top"]
        lev_z = dict(hi=0.5 * cast_top)
        tgt_z = cast_top * 10 ** (-CLOSE_UNDER_DB / 20)
        f_root = root_hz(C_["sp"]["root"])
        print(f"\nCLOSE -- 'the chime reversed, quiet', on {C_['name']}'s figure. Level-matched {CLOSE_UNDER_DB:g} dB "
              f"under the cast's top ({tgt_z:.4f})")

        def zx(cp, gc):
            return R([["body", T0, close_body(cp, C_["sp"], C_["g"], C_["D"], gc), {}]], secs=3.0)

        def calib_close(cp):
            gc = 0.3
            for _ in range(4):
                gc = float(f"{gc * tgt_z / basic(zx(cp, gc)[0])['top']:.3g}")
            return gc

        # the literal reference (the picked cast dry, reversed, x gc) and AGAIN
        cbt = cast_body(C_["sp"], C_["g"], C_["D"])
        gl = 0.3
        for _ in range(4):
            gl = gl * tgt_z / basic(R([["lit", T0, cbt, gl]], secs=3.0)[0])["top"]
        xlit, _ = R([["lit", T0, cbt, gl]], secs=3.0)
        wav("lodestone-close-0-literal.wav", xlit)

        def close_measure(x, calls, name, cp, gc):
            M = basic(x); M.update(x=x, calls=calls, name=name, cp=cp, gc=gc)
            a0, aud = M["a0"] / 1000, M["aud"] / 1000
            M["c_first"] = cents(top_note(x, T0 + a0, T0 + a0 + aud / 2, lo=300.0, hi=4000.0), f_root)
            M["c_last"] = cents(pitch(x, T0 + a0 + aud - 0.1, T0 + a0 + aud, lo=300.0, hi=4000.0), f_root)
            M["corr"] = env_corr(x, xlit)
            M["heard"], M["heard_at"] = heard(x, P90, a=max(0.0, M["top_at"] - 0.05))
            M["why"] = close_why(M, lev_z)
            return M

        rows_z = []
        print(f"  {'cand':<10}{'gc':>7}{'calls':>6}{'top':>8}{'dB/cast':>8}{'at ms':>6}{'1st c':>7}{'end c':>7}"
              f"{'late':>6}{'corr':>6}{'gone':>6}{'heard':>7}")

        def close_line(M):
            print(f"  {M['name']:<10}{M['gc']:>7.3g}{M['calls']:>6d}{M['top']:>8.4f}{db(M['top'] / cast_top):>8.1f}"
                  f"{M['top_at'] * 1000:>6.0f}{M['c_first']:>7.0f}{M['c_last']:>7.0f}{M['late']:>6.2f}"
                  f"{M['corr']:>6.2f}{M['gone']:>6.0f}{M['heard']:>+7.1f}")

        for name, cp, blurb in CLOSE_CANDIDATES:
            gc = calib_close(cp)
            x, calls = zx(cp, gc)
            x2, _ = zx(cp, gc)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            M = close_measure(x, calls[0], name, cp, gc)
            rows_z.append(M); close_line(M)
            wav(f"lodestone-close-{name.replace(' ', '-').lower()}.wav", x)
        xa, ca = R([["body", T0, cast_body(C_["sp"], round(C_["g"] * gl, 6), C_["D"]), {}]], secs=3.0)
        AG = close_measure(xa, ca[0], "0 AGAIN", None, gl)
        LM = close_measure(xlit, 0, "0 LITERAL", None, gl)
        close_line(AG); close_line(LM)
        wav("lodestone-close-0-again.wav", xa)
        for (name, _cp, blurb) in CLOSE_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 AGAIN    the picked cast itself, quiet -- a control\n"
              "    0 LITERAL  the picked cast's samples reversed (the reference; cannot ship)")
        print(f"  RULE  {CLOSE_RULE}")
        for M in rows_z:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        if AG["why"]:
            print(f"  AGAIN (the control) comes back wrong, as it must: {'; '.join(AG['why'][:3])}")
        else:
            print("  AGAIN PASSED -- 'reversed' cannot fail, so it proves nothing")
            FAILED.append("again control")
        print(f"  LITERAL (the reference) {'passes' if not LM['why'] else 'fails: ' + '; '.join(LM['why'])} "
              f"-- what a shippable reversal is measured against")
        ok, fb = _gate(rows_z, "close")
        zi = fb if ok is None else min(ok, key=lambda i: (-round(rows_z[i]["corr"], 2), rows_z[i]["calls"]))
        Z_ = rows_z[zi]
        print(f"  PICK  {Z_['name']}  gc {Z_['gc']} ({db(Z_['top'] / cast_top):+.1f} dB re the cast's top, "
              f"{db(Z_['top'] / h_lo):+.1f} re the hit @ 20.5), corr {Z_['corr']:.2f}, gone {Z_['gone']:.0f} ms")

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   touch {K_['name']}   close {Z_['name']}")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        root_nm = {0: "A4", 12: "A5", -12: "A3"}   # the cast's root
        what_c = {"bar": "each note a free bar's modes (a triangle and sines at 2.76x and 5.40x, the upper decaying faster)",
                  "glass": "each note a sine and its octave at 0.3",
                  "rune": "each note rune-crack's own partials (triangles at 1 : 2.73 : 4.41)"}[C_["sp"]["tim"]]
        what_k = {"1 ZAP": "A 12 ms highpass crack (the spark) on a square that sags to 0.6 of its note over its decay "
                           "(the zap).",
                  "2 BUZZ": "A 12 ms highpass crack (the spark) on a held sawtooth at the count's note (the buzz).",
                  "3 ARC": "A 12 ms highpass crack (the spark) on a held square at the count's note and a square a fifth "
                           "over it at 0.5 (the arc).",
                  "4 HIGH": "A 12 ms highpass crack (the spark) on a square that sags to 0.6 of its note over its decay "
                            "(the zap).",
                  "5 CRACKLE": "Three highpass cracks 7 and 15 ms apart (the spark's crackle) on a held square at the "
                               "count's note.",
                  "6 HUM": "Three highpass cracks 7 and 15 ms apart (the spark's crackle) on a held square at the "
                           "count's note, low -- an arc's buzz, its partials clear of the hex-snap's 2.6 kHz.",
                  "7 ARC3": "A 12 ms highpass crack (the spark) on a held square at the count's note, low -- an "
                            "arc's buzz, its partials clear of the hex-snap's 2.6 kHz."}[K_["name"]]
        what_z = {"mirror": (f"the cast's four notes, each RE-STRUCK every whole number of cycles nearest "
                             f"{round(Z_['cp'].get('every', 0.011) * 1000)} ms (in phase: `.frequency.value = f`, v97 "
                             f"§4b) at a level climbing as the cast's own decay reversed, each cut at its mirrored "
                             f"onset -- all four swell and drop out from the top down, the root last."),
                  "descend": "the cast's four notes struck falling, A-E-C-A, at its own spacing and decay."}[Z_["cp"]["mode"]]
        kn = " / ".join(f"{root_hz(K_['sp']['root']) * 2 ** (s / 12):.0f}" for s in PENT)
        info = dict(n_cast=len(CAST_CANDIDATES), n_touch=len(TOUCH_CANDIDATES), n_close=len(CLOSE_CANDIDATES),
                    n_rc=n_rc, c_root=root_nm.get(C_["sp"]["root"], "?"), c_what=what_c, c_dt=C_["sp"]["dt"],
                    c_rise=C_["rise0"], c_jump=C_["jump"], c_aud=C_["aud"], c_top=db(C_["top"] / h_lo),
                    c_heard=C_["heard"], c_reg=max(C_["regs"].values()),
                    k_what=what_k, k_notes=kn, k_pp=" / ".join(f"{p_:.0f}" for p_ in K_["pitch"]),
                    k_step=K_["minstep"], k_rise=K_["rise_max"], k_gone=K_["gone_max"], k_peak=K_["peak_max"],
                    k_harm=K_["harm_min"], k_db0=db(K_["top_lo"] / h_lo), k_db1=db(K_["top_hi"] / h_lo),
                    k_over=db(K_["top_lo"] / x_hi), k_hex=K_["hex_over"], k_reg=max(K_["regs"].values()),
                    z_what=what_z, z_db=db(Z_["top"] / cast_top), z_gone=Z_["gone"], z_corr=Z_["corr"])
        arms = arms_code(C_, K_, Z_, info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        if arms.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx row does not re-emit its anchor exactly once")
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        kbt = touch_body(K_["sp"], K_["g"], K_["D"])
        rp = [float(np.abs(R([["body", T0, kbt, {"n": CAP}]])[0] - R([["body", T0, kbt, {"n": CAP}]])[0]).max())
              for _ in range(3)]
        print(f"  REPRO -- the render floor: the loudest snap rendered twice from the same text differs by at most "
              f"{max(rp):.1e} (three tries); the tolerance is {TOL:.0e}")
        chk = []
        zbt = close_body(Z_["cp"], C_["sp"], C_["g"], C_["D"], Z_["gc"])
        for sd in (None, NOISE_SEEDS[5]):
            tag = "" if sd is None else "'"
            xa1, _ = R([["arm", T0, "ult", {"w": ME}]], seed=sd, rows=sfx_rows)
            chk.append(("cast" + tag, float(np.abs(xa1 - R([["body", T0, cbt, {}]], seed=sd)[0]).max())))
            for n in (-1, 0, 1, 2, 3, 4, 5, 7, None):
                p1 = {"w": ME + "-touch"} if n is None else {"w": ME + "-touch", "n": n}
                x1, _ = R([["arm", T0, "ult", p1]], seed=sd, rows=sfx_rows)
                nn = 1 if n is None else min(CAP, max(1, n))
                x2, _ = R([["body", T0, kbt, {"n": nn}]], seed=sd)
                chk.append((f"touch@{n}{tag}", float(np.abs(x1 - x2).max())))
            xz1, _ = R([["arm", T0, "ult", {"w": ME + "-close"}]], seed=sd, rows=sfx_rows)
            chk.append(("close" + tag, float(np.abs(xz1 - R([["body", T0, zbt, {}]], seed=sd)[0]).max())))
            if sd is None:
                xa0 = xa1
        print("  the arms vs the picked candidates, max |diff| (render.py's draw and a second): " +
              ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11.6, 20.5, 50) for c_ in (False, True)]
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
        print(f"  ult/lodestone vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
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
            evs = [("ult", {"w": ME}), ("ult", {"w": ME + "-close"})] + [("ult", {"w": ME + "-touch", "n": n}) for n in COUNTS]
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
                pr[w_] = [cos(bands(C_["x"][int(T0 * SR):]), bp), cos(bands(K_["x"][int(T0 * SR):]), bp),
                          cos(bands(Z_["x"][int(T0 * SR):]), bp)]
            worst_p = max(((max(v), k) for k, v in pr.items()), default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both "
                  f"orders render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the cast / touch / close against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) "
                  f"-- printed, not gated")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=pr))
        rec["peers"] = peers

        # ---- THE tickRunes ROWS --------------------------------------------
        trows = [[TOUCH_ANCHOR, TOUCH_CODE], [CLOSE_ANCHOR, CLOSE_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickRunes ROWS, applied to Match.prototype.tickRunes's own source, run beside the original on real "
              "fights (the mirror match is refused by Match -- 'A relic cannot fight itself'):")
        WR = page.evaluate(WIRE_JS, [seeds, trows])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Lodestone both sides x every foe x seeds {seeds}): {WR['same']}/{WR['fights']} "
              f"identical (over, clock, both hp, shields, positions, velocities, charges, both hex counts, clocks and "
              f"hex stun clocks, winner, the whole runeTally); every other voice call identical in order, kind and "
              f"opts in {WR['otherSame']}/{WR['fights']}")
        nh = WR["nh"]
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['touch']} touches -> "
              f"{WR['touchV']} touch voices and {WR['snaps']} hex-snaps; {WR['closes']} closes; problems {WR['nbad']}")
        print("  the count a touch carries (the foe's hex after it): " + ", ".join(f"{n}: {nh[n]}" for n in COUNTS) +
              f" ({100 * nh[CAP] / max(1, sum(nh)):.0f}% at 5); a stack added on {WR['rose']}, the cap refreshed on "
              f"{WR['atCap']}; {WR['early']} touches inside the cast's first 0.5 s (over the chime)")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["touchV"] != WR["touch"] or WR["snaps"] != WR["touch"] or WR["castV"] != WR["casts"] \
                or WR["closes"] != WR["ends"]["clock"] or WR["touch"] == 0 or WR["ends"]["clock"] == 0:
            FAILED.append("tickRunes rows")
        WB = page.evaluate(WIRE_JS, [seeds, [[TOUCH_ANCHOR, TOUCH_CODE_BAD], trows[1]]])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a touch): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "touch", "touchV",
                                          "snaps", "closes", "rose", "atCap", "early", "nh", "nbad")}
        rec["wire"]["control_same"] = WB["same"]
        print(f"  THE CLOSE: {WR['ends']['clock']} windows closed by their clock with both alive -> {WR['closes']} "
              f"close voices; {WR['ends']['clockDead']} closed on their clock's frame with a fighter already dead, "
              f"{WR['ends']['death']} by a death, {WR['ends']['over']} still lit when the fight ended and "
              f"{WR['ends']['recast']} re-cast: none of those plays a close")

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["touches"], w["foe"], w["seed"], w["side"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], trows])
            assert not errors, errors[:3]
            c0, c1 = w_["cast"], w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.5
            xw, _ = R(allv, secs=secs, rows=sfx_rows)
            xo, _ = R(without, secs=secs, rows=sfx_rows)
            bd = bed[:len(xw)]
            if len(bd) < len(xw):
                bd = np.concatenate([bd, np.zeros(len(xw) - len(bd))])
            xw = xw + bd; xo = xo + bd
            td = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == ME + "-touch"]
            ct = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME]
            zt = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME + "-close"]
            others_at = [(T0 + (e[0] - lo_t), e[1] + ("/" + e[2]["w"] if e[1] == "ult" and "w" in e[2] else ""))
                         for e in evs if not e[3]]

            def near(t_):
                # round 4: up to 0.5 s before (a long voice begun earlier still sounds), 0.1 s after
                return ", ".join(f"{k_} {1000 * (u_ - t_):+.0f} ms" for u_, k_ in others_at if -0.5 <= u_ - t_ <= 0.1)

            def ov(f, a_, d_):
                return db(band_rms(xw, f, a_, a_ + d_) / max(band_rms(xo, f, a_, a_ + d_), 1e-12))

            def loud_band(x, a_, d_):
                b_ = bands(x[int((T0 + a_) * SR):int((T0 + a_ + d_) * SR)])
                return max((v_, fc) for v_, fc in zip(b_, BANDS) if fc >= PHONE_HZ)[1]
            kb = {n: loud_band(K_["xs"][n], 0.0, 0.05) for n in COUNTS}
            t_over = [ov(kb[min(CAP, max(1, n))], t_, 0.05) for t_, n in td]
            fc_c = loud_band(C_["x"], 0.0, 0.5)
            c_over = [ov(fc_c, t_, 0.5) for t_ in ct]
            fc_z = loud_band(Z_["x"], max(0.0, Z_["top_at"] - 0.05), 0.1)
            z_over = [ov(fc_z, t_ + max(0.0, Z_["top_at"] - 0.05), 0.1) for t_ in zt]
            print(f"\nIN A REAL WINDOW -- lodestone v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {len(td)} touches; the fight's own sounds and the "
                  f"score, with and without Rebuttal's voices (the hex-snaps under the touches are Rebuttal's)")
            print("  each touch over the fight in its loudest third-octave at or above 200 Hz, its first 50 ms: " +
                  " ".join(f"{v:+.1f}" for v in t_over) + " dB (counts " + " ".join(str(n) for _, n in td) + ")" +
                  (f"; median {float(np.median(t_over)):+.1f}, least {min(t_over):+.1f}" if t_over else ""))
            print(f"  the cast ({fc_c:.0f} Hz, 0.5 s): " + " ".join(f"{v:+.1f}" for v in c_over) +
                  f" dB;  the close ({fc_z:.0f} Hz, its loudest 100 ms): " + " ".join(f"{v:+.1f}" for v in z_over) + " dB")
            for (t_, n), v1 in zip(td, t_over):
                if v1 < 8:
                    print(f"    the touch at {t_ - T0 + lo_t:.3f}s (count {n}, {v1:+.1f} dB) sounds with (begun up to "
                          f"0.5 s before, or 0.1 s after): {near(t_) or 'nothing'}")
            # round 4: a frequent voice's gate (Zenith's tick, v98) -- the median >= +6 -- and a floor, >= +3, under every one
            if (t_over and (float(np.median(t_over)) < 6 or min(t_over) < 3)) or (c_over and min(c_over) < 6) \
                    or (z_over and min(z_over) < 3):
                FAILED.append("a new voice not heard in a real window")
            wav("lodestone-pick-real-window.wav", xw)
            wav("lodestone-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, touch_over=t_over, cast_over=c_over, close_over=z_over,
                               counts=[n for _, n in td])
        # the picks in order, for the ear
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, n in enumerate(COUNTS + [CAP]):
            seq += [["arm", T0 + 1.0 + 0.5 * k_, "ult", {"w": ME + "-touch", "n": n}],
                    ["arm", T0 + 1.0 + 0.5 * k_, "hex-snap", {}]]
        seq += [["arm", T0 + 4.5, "hit", {"dmg": BLADE, "crit": False}], ["arm", T0 + 5.5, "ult", {"w": ME + "-close"}]]
        xq_, _ = R(seq, secs=8.0, rows=sfx_rows)
        wav("lodestone-pick-sequence.wav", xq_)

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_voices = [(k_, p_) for k_, p_ in others if k_ != "ult"][:36] + \
                     [("ult", {"w": w_}) for w_ in ult_ids if w_ in {w for w, _a, _s in info0["W"]}][:12]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [R([["play", T0, k_, p_]])[0] for k_, p_ in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
            assert not errors, errors[:3]
            e2e_ref["new"] = {"cast": C_["x"], "close": Z_["x"]}
            for n in COUNTS:
                e2e_ref["new"][f"touch n{n}"] = K_["xs"][n]

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Lodestone's cast, touch and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="tickRunes: the touch voice and the hex-snap under it, once per touch, after its hex",
                 anchor=TOUCH_ANCHOR, mode="replace", code=TOUCH_CODE),
            dict(label="tickRunes: the close, when the window runs out by its clock with both fighters alive",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE)]
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit("end to end: an anchor is not re-emitted exactly once")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="lodestone_e2e_"))
        try:
            tp = tmpd / "sc-lodestone-voices.html"
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
                NEWP = [("cast", {"w": ME}, 2.5), ("close", {"w": ME + "-close"}, 3.0)]
                NEWP += [(f"touch n{n}", {"w": ME + "-touch", "n": n}, 1.5) for n in COUNTS]
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
        t_ok = sum(f_["touchV"] == f_["touches"] and f_["snapV"] == f_["touches"] and f_["badN"] == 0 for f_ in F1)
        z_ok = sum(f_["closeV"] == f_["clocks"] for f_ in F1)
        orig_new = sum(f_["touchV"] + f_["snapV"] + f_["closeV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "touches", "clocks", "castV", "touchV", "snapV", "closeV")}
        print("  the three voices through the patched page's own SFX.play vs the lab's candidate text, max |diff|: " +
              ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/lodestone vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, touch voices and hex-snaps = touches "
              f"(n the foe's count) {t_ok}, close voices = clock closes {z_ok} (of {len(F1)}); totals {tot}; the "
              f"original page played {orig_new} touch/hex-snap/close voices from the runes; page errors {page_err}")
        if max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1) or osame != len(F1) \
                or min(c_ok, t_ok, z_ok) != len(F1) or orig_new or page_err:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same,
                          other_same=osame, totals=tot)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB", "sp", "cp", "keep_all")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), touch=strip(rows_k), touch_controls=strip(ctlk),
               close=strip(rows_z), close_controls=strip([AG, LM]), wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_D": C_["D"], "touch": K_["name"], "touch_g": K_["g"],
                     "touch_D": K_["D"], "close": Z_["name"], "close_gc": Z_["gc"]})
    print(f"\nTHE PICKS  cast {C_['name']}   touch {K_['name']}   close {Z_['name']}")
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
        f"The three voices (v70 §6.2), in the synth only. The arms are added BEFORE the shared rune-crack fallback, "
        f"and the fallback line is re-emitted unchanged, so the relics that still fall through keep it ({n_rc} "
        f"others on this link). Through the patched play() every arm reproduces its lab candidate (worst "
        f"{max(v for _, v in ac['chk']):.0e}; the touch at counts -1, 0, 1-5, 7 and a missing n, on two noise "
        f"draws), {len(ac['others'])} other voices are unchanged (worst {max(v for _, v in ac['others']):.0e}), and "
        f"ult/lodestone is no longer rune-crack. play() returns on its first line with no audio context (every "
        f"headless run), draws no random number and writes nothing the simulation reads"
        + (f"; end to end the three voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + pe + ".")
    rows[1]["why"] = (
        f"Two plain SFX.play calls in tickRunes's hex branch, after the apply and the tally, so n is the count the "
        f"foe now carries (foe.stacks is a read) and the hex-snap is heard whenever the touch hexes (reading 2). "
        f"{wr['touchV']}/{wr['touch']} touches voiced and {wr['snaps']} hex-snaps, each n equal to the foe's count "
        f"(1-{CAP}; {100 * wr['nh'][CAP] / max(1, sum(wr['nh'])):.0f}% at 5; a stack added on {wr['rose']}, the cap "
        f"refreshed on {wr['atCap']}); {wr['same']}/{wr['fights']} fights identical and every other SFX call "
        f"identical in order and opts; the same rows plus one sim write (the foe nudged 1e-9 on a touch) come back "
        f"{wr['control_same']}/{wr['fights']}{e2}.")
    rows[2]["why"] = (
        f"One guarded SFX.play BEFORE the close line, which is re-emitted unchanged: a clock close with both fighters "
        f"alive (Z.t >= Z.dur is the line's own clock test, read after its own increment). {wr['closes']} close "
        f"voices for {wr['ends']['clock']} clock closes; none for the {wr['ends']['death']} death closes or the "
        f"{wr['ends']['over']} windows still lit at the verdict (tickRunes is not called once the fight is over); "
        f"nothing is read back{e2}.")
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
