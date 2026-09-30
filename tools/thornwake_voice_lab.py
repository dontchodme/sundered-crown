#!/usr/bin/env python3
"""BRAMBLESNARE'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v113.

    python thornwake_voice_lab.py --game <a link carrying Thornwake's stage 5> --rows rows.json
        [--also <the same stage 5 carried onto a newer tip>] [--peer-rows <another relic's rows_final.json>]
        [--tendril ../02-chain/sc-tendril-fx.html]

v84 section 4 SOUND, every word of it: "Sound: cast -- a rustle-and-creak,
0.4s; a bramble opening -- a dry crackle; the snare -- a short creak and crack
(Tendril's root voice, reused); a bite -- a soft snap." The build brief (s5,
"Stage 4 -- picture, voice, carry"; the batch's stage 6). Rick, for the batch's
art and sound: "you pick i overrule". So this lab does not offer a spread -- it
renders three to five candidates a voice beside CONTROLS that can come back
wrong, prints the numbers each pick is made on, and PICKS by a rule written in
this file (`*_RULE`, `*_why`). He overrules from one clip.

THE PICKS, on Chromium 151.0.7922.34, sc-thornwake-b26.5 fd5031063ecb6807,
wire seeds 113601-113602 (148 fights), end to end 113651 (74), ALSO on the same
stage 5 carried onto sc-spellbreaker-fxout (f7c32e86063abb8d, 82 fights):

  cast    8 NEEDLES  narrow bandpass grains (Q 8, 30 ms) ~60 a second, their
                   centres wandering 2310-3900 Hz, swelling to the middle; under
                   them a 330 Hz timber (a sine and its 2.76 mode at 0.4) pulsed
                   slowing 45 -> 28 a second. The rustle alone is noise (TONAL
                   7.0 dB), centred 3215-3752 Hz on every draw, its loudest
                   millisecond 117 ms in; the creak alone 37 pulses a second
                   (PULSED 0.74), -2.9 dB re the rustle; each owns a band (+37 /
                   +40 dB). Audible 395 ms; TOP -3.1 dB re the blow; heard +30.3
                   dB over the score. Register at most 0.77 (Scour's woosh);
                   0.65 against Thornshear's and Heartwood's (batch line) casts,
                   0.62 against the creak and cinch it replaces. 53 synth calls,
                   2.0 ms. SPINES (0.78) passes and loses the register tiebreak;
                   THORNS out (its rustle centred to 4143 Hz), BURRS out (to
                   4075 Hz, and 0.80 Scour's woosh), LEAVES and BOUGH out (0.93
                   Scour's woosh, 0.81-0.82 Thornshear's leaves), BRUSH out (0.85
                   fork), BRIAR out (centred to 4922 Hz).
  crackle 5 KNOTS  8 ms bandpass clicks (Q 6) ~33 a second at centres wandering
                   1185-2160 Hz, spaced x (1 + 0.45 sin 2.4k), thinning: 10
                   clicks, IRREG 0.30, DEPTH 20.6 dB; dry (B500 0.022, LOW
                   0.002, TONAL 2.3 dB); audible 280 ms; TOP -11.1 dB re the blow
                   (0.026-0.054 over the draws); heard +17.6 dB over the score
                   after the blow's body; register at most 0.73 (Scour's tick).
                   10 synth calls, 0.6 ms. SPLINTERS out (a draw under the level
                   window, 0.83 Scour's tick); SNAPS, OPEN and EMBERS out (0.96-
                   0.97 the wall tick, 0.90-0.91 Tendril's wither), TWIGS out
                   (0.95 Scour's tick).
  snare   (reused) Tendril's root, its body transcribed: equal to Tendril's own
                   arm to 1.5e-07 over 12 draws (OFF 4.7e-05); audible 355-370
                   ms, TOP -2.5 dB re the blow, LOW 0.50, the crack at 206 ms
                   +43.5 dB. Register at most 0.85 (Cindercleave's cast, a
                   scythe cast) -- REPORTED, not gated. 18 synth calls, 0.5 ms.
  bite    1 STEM   a 10 ms bandpass snap at 1.1 kHz (Q 1.2) over a sine falling
                   620 -> 420 Hz: rise 1 ms, one snap, audible 65 ms; TOP -11.0
                   dB re the blow, +11.0 dB re the wall tick; the snap's first
                   10 ms centred at 678 Hz at most; heard +12.8 dB; register at
                   most 0.39 (fork). 2 synth calls, 0.1 ms. PRICK (0.55) and PAD
                   (0.60) pass and lose the tiebreak; KNOT out (0.85 fork).

  In play (148 fights): 490 casts -> 490 cast voices; 856 brambles planted ->
  856 crackles; 1781 snares -> 1781 snare voices; 4287 bites -> 4287 bite
  voices (all 9 killing bites among them); a cast brings 1.75 crackles, 3.63
  snares and 8.75 bites; 1374 steps snare and bite at once, the snare first
  every time. 148/148 fights identical and every other SFX call identical; the
  sim-write control 1/148. In a real window (v Twinshade, 113601, cast at
  15.17 s: 2 crackles, 7 snares, 14 bites) the cast stands +32.6 dB over the
  fight and the score in its own third-octave, the crackles +9.0 / +14.2, the
  bites a median +14.0, the snares' creak a median +10.5 and their crack
  +32.9; AFTER +0.0 everywhere, LEVEL follows every voice. End to end 74/74 and
  82/82 fights identical; on sc-spellbreaker-fxout, which carries Tendril's
  voices, the snare equals that page's own `ult/bindweed-root` to 1.2e-07.
  Co-applied with Heartwood's, Bindweed's, Spellbreaker's and Widowmaker's Sfx
  rows in both orders: every arm alike; the snare reads 0.99-1.00 against
  Heartwood's and Tendril's roots (the same voice, as both designs ask) and the
  crackle 0.87 against Spellbreaker's stun (printed).

  FOR RICK'S LISTEN: the snare is Tendril's root as the design asks, and it is
  heavy -- -2.5 dB re the blow, half its power under 120 Hz -- where Tendril
  plays it at most once a window, Thornwake plays it ~3.6 times a cast.

ONE VOICE IS AN EXISTING ONE, BECAUSE THE DESIGN NAMES IT: "the snare -- a
short creak and crack (Tendril's root voice, reused)". Tendril's root is
`ult/bindweed-root` (bindweed_voice_lab.py's DEEP, v101), and it is NOT ON THIS
BASE: Thornwake's stage 5 stands on sc-tendril-t3, and Tendril's voices landed
one link later, on sc-tendril-fx. A reuse that plays `bindweed-root` would fall
through to rune-crack here. So the snare is MADE -- its own arm,
`ult/thornwake-snare`, whose body is Tendril's arm body TRANSCRIBED (nine lines,
byte for byte; read out of `--tendril` and checked against the copy in this
file) -- and this lab proves the transcription: rendered on this synth it
equals Tendril's own arm (applied to this page's play() from sc-tendril-fx's
text) to TOL on every noise draw, a copy one constant off must NOT (the
control), and with `--also` on a tip that carries Tendril's voices it equals
that page's own `ult/bindweed-root`. The snare is not picked and not
level-matched ("reused"); its numbers are printed and its standing in a real
fight is REPORTED, not gated (a failing gate here would be a design question,
not a pick). It does not follow a later re-voicing of Tendril's root.

THE FOUR EVENTS AND WHERE THEY FIRE (line numbers are sc-thornwake-b26.5's):
  cast     the bare id `ult/thornwake`, which `fireUlt` plays for every relic
           (the shared prologue, 16339). Thornwake HAS an arm today: the freeze's
           "creak and cinch" (6324-6327). v84 retires the freeze, and the arm
           goes with it: ONE row REPLACES those four lines (their text is the
           anchor, Widowmaker's v106 precedent) with the four arms below. The
           shared rune-crack fallback is not touched. No sim line: the cast
           already plays it, once a cast.
  crackle  `ult/thornwake-crackle` from `plantBramble`, after
           `f.brambleTally.planted++` (13741, mode `after`): once per bramble
           planted, on the landing blow's own frame (the blow's hit voice
           lands on the same frame, from later in resolveHit). 1.61 a cast
           (stage 5's probe on this link; 1.75 in this lab's 148 fights).
  snare    `ult/thornwake-snare` from `tickBramble`, after `T.snares++`
           (13708, mode `after`): the frame the pin is written -- the foe's
           centre entering one of the caster's brambles. 3.46 a cast (stage 5's
           probe; 3.63 here). A planting blow puts the foe inside a bramble
           at once, so the usual snare is the first unfrozen step after that
           blow's hit stop.
  bite     `ult/thornwake-bite` from `tickBramble`, after `f.brambleCd =
           u.tickCd` (13712, mode `after`): once per bite, on the line every
           bite starts with, ahead of its entangle and its hurt on the same
           step (the same instant in the mix). NOT after `T.ticks++`, the
           first choice: that line is Thornwake's alone on this base, but the
           batch line's newer tips carry a second one (a smite ticker's), so
           it would stop being an anchor at the carry (round 4). A killing
           bite snaps too (the number of snaps is the number of bites,
           Tendril's rule); its fatal beat is the sim's, further on. On an
           entry frame with the thorns' cooldown clear the snare's voice and
           the bite's land together, in that order. 8.17 a cast (stage 5's
           probe; 8.75 here).
  THERE IS NO CLOSE VOICE (v84 names none; the brambles outlive the window)
  and no voice for a bramble expiring (the picture browns it). Nothing here
  sets a hit stop, files a beat or writes a field; the four voices are plain
  SFX.play calls whose only opt is the id. The picture's rows are the picture
  lab's, not these.

THE CONTROLS, and what each one is for:
  rune-crack   the shared fallback; v88 published 0.608 / 450 ms -- reproduced
               before anything new is quoted (with BAR 0.364 / 300 ms and
               hit@11.6 0.443 / 80 ms). Played through `__fallback__`, an id no
               arm names (spellbreaker_voice_lab's carry note).
  hit@26.5     Thornwake's own blow (the blade is 26.5, stage 5): the level
               every voice is judged against, on its quietest / loudest draw
  wall         the commonest sound in a fight: the quiet voices' floor
  OLD          the freeze's "creak and cinch", which the cast replaces:
               printed, and after the rows `ult/thornwake` must no longer be it
  the school   the verdant casts with a voice of their own (read off the page),
               and Tendril's four voices, from `--tendril` (not on this base)
  the type     the scythe casts with a voice of their own (read off the page)
  the house    fork, hex-snap, the vine's plant, the spark's burn, the clank,
               Scour's tick and woosh, BAR and the death voice
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  RUSTLE, CREAK, HELD   the cast's rustle alone, its creak alone, and its creak
               as a held re-struck note (no stick-slip): each must fail the
               cast's rule
  HISS, EVEN, WET   one swell of the crackle's band with no clicks, the
               crackle's clicks evenly spaced, and a body under every click:
               each must fail the crackle's rule
  BRIGHT, SLOW, DOUBLE, LOUD   the bite three times higher, with a 25 ms
               attack, struck twice, and six times louder: each must fail the
               bite's rule
  OFF          the snare with one constant 1e-4 off: must NOT equal Tendril's
               root (or the reuse check proves nothing)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT: generated as the JS body that will sit
    in the arm (constants rounded first) and rendered by evaluating that text
    on the synth (ironwood_voice_lab's RENDER_JS, imported unchanged); the row
    is then applied to `Sfx.prototype.play`'s own source and rendered again,
    and must match to TOL = 1e-5.
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's,
    bindweed_voice_lab's, ironhail_voice_lab's and spellbreaker_voice_lab's,
    imported unchanged: E50, TOP (the loudest 50 ms), AUDIBLE / GONE (5 ms RMS
    above 2% of its own loudest), RISE (10 -> 90% of the 1 ms envelope),
    CENTROID, REG (cosine of 1/3-octave band amplitudes, 25 Hz-16 kHz, the
    median over noise draws), TONAL, LOW (the share of the power below 120
    Hz), RATE and PULSED (a creak: the envelope's own modulation, 17-83 a
    second, and its autocorrelation, 100 ms windows -- bindweed's root), CRACK
    (the loudest high-passed millisecond, its STAND and JUMP), RE-ATTACK and
    HEARD (a third-octave >= 200 Hz over 100 ms against the score's p90, dB).
  * New here, each with a control that can come back wrong:
      OWN      a part of the cast alone against the other part alone: the
               third-octave (100 Hz-12 kHz) in which it stands highest over the
               other, over the cast's span, dB. Both parts must own a band:
               the rustle and the creak are two things heard, not one
      CLICKS   the crackle's onsets: peaks of its 1 ms RMS high-passed at 1.5
               kHz (bindweed's HF envelope) within 20 dB of its loudest, each at
               least 6 dB over the dip since the last one (HISS reads few)
      IRREG    the coefficient of variation of the intervals between CLICKS
               (EVEN reads ~0)
      DEPTH    p90 over p10 of that envelope across the crackle's span, dB
      B500     the share of the power below 500 Hz (dry: no body; WET fails)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's creak so its creak alone sits 3 dB under its rustle
    alone, its length so AUDIBLE is 400 ms, its gain so its TOP is the centre
    of its window; the crackle's length so AUDIBLE is 300 ms and its gain to
    the centre of its window; the bite's decay so AUDIBLE is 65 ms and its gain
    to the centre of its window. Constants are rounded BEFORE any measured
    render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (words of v84 s4 turned into numbers -- Code's picks,
Rick's to overrule):
  * "0.4s": AUDIBLE 330-470 ms on every draw, GONE <= 470 (v100's +/-17.5%).
  * "A RUSTLE": noise (TONAL <= 10 dB over 300-8000 Hz, the rustle alone),
    leaves and brush -- its centroid 400-4000 Hz on every draw (not a hiss,
    not a rumble; the house's rustles sit there: Tendril's 400-3k band, the
    leaf volley's 2.1 kHz) -- and not struck (the rustle alone's RISE >= 30
    ms: its loudest millisecond is not its head).
  * "A CREAK": the house's creak, as bindweed_voice_lab measured Tendril's
    root -- stick-slip, a train of pulses: the creak alone's RATE 17-83 a
    second and PULSED >= 0.40. Every candidate's creak is a pulse train whose
    intervals run x (1 + 0.12 sin 2.4k) (no random number), SLOWING across the
    cast (a bough bending under the load: 45 -> 28 a second).
  * "RUSTLE-AND-CREAK": two things heard at once -- each OWNS a third-octave
    (+6 dB over the other alone), the creak alone within -9..+3 dB of the
    rustle alone (level-matched to -3: the rustle is named first). v68's
    Tendril cast is the school's own "rustle-and-creak" ("rising", 0.5 s);
    Thornwake's is not rising, and must not sound like it (register).
  * "A BRAMBLE OPENING": the bramble grows out over 0.3 s (v84 s4 picture),
    so the crackle is the opening's length: AUDIBLE 250-350 ms, GONE <= 350.
    "A CRACKLE": a run of small dry clicks at irregular intervals -- CLICKS >=
    6, IRREG >= 0.15, DEPTH >= 12 dB. "DRY": no body and no ring -- LOW <=
    0.02 and B500 <= 0.05 on the worst draw, TONAL <= 10 dB over 1-12 kHz.
    Heard but under the blow it lands with (fork's rule: "the blow is the event
    and this is what the event did"): TOP between 2x the wall tick's (its
    loudest draw) and 0.5x the blow's (its quietest), and HEARD over 100-200
    ms (after the blow's body) >= +6 dB.
  * "A SNAP": struck -- RISE <= 3 ms, the peak in the first 10 ms -- one snap
    a call (no RE-ATTACK: the number of snaps is the number of bites), short
    (AUDIBLE 30-100 ms, GONE <= 110). "SOFT": quiet and dull -- TOP between 2x
    the wall tick's (loudest draw) and 0.5x the blow's (quietest draw), and the
    SNAP dull: the centroid of its first 10 ms <= 2000 Hz on every draw (round
    2; hex-snap, the house's bright snap, reads 4.4 kHz there, and Tendril's
    bite 1.1-1.3 kHz, its falling body setting it -- printed beside the table).
  * Every new voice's register <= 0.80 against the list its rule names (the
    blow and rune-crack in every list; the cast's adds the verdant and scythe
    casts, Tendril's voices and the house's; the crackle's and the bite's the
    house's small sounds) -- and against the voices picked before it (the
    snare first, then the cast, the bite, the crackle). Tiebreak: the most
    distinct register (to 0.05), then the fewest synth calls, then the order
    listed.

THE ROUNDS (each a run of this file; the logs in scratch stage6-voice/iter*.log
and run*.log). The rules were written before the first table. Every change after
a table was read is here, with its reason:
  1  four candidates a voice, the rules as written. NO CAST PASSED: every
     rustle read 0.84-0.93 against Scour's woosh (a band of noise), LEAVES and
     BOUGH 0.81-0.82 against Thornshear's cast (its leaves at 2.6 kHz), and
     BRIAR's rustle centred at 3.9-4.9 kHz. NO CRACKLE PASSED: every
     high-passed click read 0.95-0.97 against the wall tick and 0.87-0.91
     against Tendril's wither -- a high-passed click IS the wall tick's
     spectrum. The bite's BRIGHT control PASSED: the whole voice's centroid is
     its body's (STEM 617 Hz, x3 1893 Hz) and cannot see the snap. -> round 2:
     the bite's "soft" reads the SNAP, the centroid of its first 10 ms (BRIGHT
     now reads 2339 Hz and fails). No cast or crackle gate moved; new
     candidates instead -- two narrower, higher rustles (THORNS Q 5, BURRS Q 4)
     and two crackles of narrow mid-band clicks (KNOTS Q 6, SPLINTERS Q 8),
     from a scratch survey (stage6-voice/explore*.py) that found narrow bands
     clear of the woosh, the wall tick and the wither.
  2  the bite (STEM, 0.39) and the crackle (KNOTS, 0.73) pass. THORNS out on
     its rustle's centroid alone (3436-4143 Hz, over the declared 4000), BURRS
     on that and Scour's woosh (0.80). -> round 3: two rustles in THORNS' band
     pulled down 200 Hz and narrower still (SPINES Q 6, NEEDLES Q 8).
  3  every voice passes: NEEDLES (0.77) over SPINES (0.78) on the tiebreak.
  4  the full run -- after checking every anchor on the dry carries first:
     `T.ticks++`, the bite's first anchor, occurs TWICE on the batch line's
     newer tips (a smite ticker's, on the sc-spellbreaker-fxout and
     sc-aureole-fxout carries), so it would stop being an anchor at the
     carry; the bite's row moved to `f.brambleCd = u.tickCd`, the line every
     bite starts with (the same step). Every check passed. Then, text only:
     the arms' comments name their nearest register, and this docstring's
     PICKS were written -- and the file was run once more in full (scratch
     stage6-voice/run_final.log), every number coming back. (That run was
     first cut off inside the peer checks when the session running it
     exited; it was run again whole, ALL CHECKS PASS: the same picks, voice
     counts and fights as round 4, the rows differing from round 4's in the
     arms' comments only. The per-cast figures in THE FOUR EVENTS were then
     corrected in this docstring alone: they had been stage 3's.)

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (the old arm's four lines replaced by four arms) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm must reproduce
    its candidate to TOL on two noise draws; every other voice through the
    patched play (the hit at five weights with and without a crit, spark x9,
    wall, death, clank x2, seal, nova, hex-snap, fork, vine x4, loose x3, aegis
    x2, scour x4, and every ult id and kind the page's play() names) must be
    unchanged; `ult/thornwake` must NOT be the old arm any more and
    `__fallback__` must still be rune-crack;
  * the plantBramble row and the two tickBramble rows are applied to their
    prototypes' own sources and run on real fights beside the unpatched ones:
    every fight identical (over, clock, both fighters' hp, positions,
    velocities, charges, facing, pins, entangle, the thorns' cooldown and
    inside flag, the winner, both brambleTallies, the brambles' count and
    clock, and a digest of positions, hp, pin and the brambles on EVERY step)
    and every other voice call identical in order, kind and opts; one crackle
    per bramble planted, one snare voice per snare and one bite voice per bite
    (each counted inside its own call); one cast voice per cast (from
    `fireUlt`, outside both); the unpatched functions play nothing. The same
    rows plus ONE sim write (the foe nudged 1e-9 on a bite voice) must come
    back NOT identical, or "identical" proves nothing. (The Sfx row cannot
    reach the simulation at all: `play` returns on its first line with no
    audio context, which is every headless run.)
  * END TO END: the rows applied AS TEXT (the orchestrator's semantics:
    replace = code, after = anchor + code, before = code + anchor) to a copy
    of the game file (in a temp folder, never the repo), loaded in a fresh
    browser after the first is closed: the page loads clean, its own SFX.play
    renders the arms to the lab's text and every other voice to the original
    page's, and its fights are identical to the original page's, with the
    voice counts above. With `--also <link>`, the same there -- and there, when
    it carries Tendril's voices, the snare equals the page's own
    `ult/bindweed-root`.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both
    identically; registers against the peers' voices are printed.
  All anchors must occur exactly once in the game file; the three sim rows
  re-emit their anchors unchanged (another row on the same line applies in
  either order), and the one Sfx row retires only Thornwake's own arm. Every
  row is ASCII.

THE CARRY -- one thing these rows change for every LATER voice lab: labs that
read the verdant or scythe casts off the page (bindweed_voice_lab's SCHOOL,
heartwood_voice_lab's, any scythe relic's type list) will read Bramblesnare's
cast as `ult/thornwake` on a tip that carries these rows, not the freeze's
creak and cinch.

Writes wavs to 05-reference/v113/thornwake-*.wav at RAW level (gitignored).
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
# means in v98's, v99's, v101's, v107's and v111's labs. (Their module bodies
# only define things and check their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cos, db, env, fmt, pcm, write_wav)
from ironwood_voice_lab import RENDER_JS, low_share  # noqa: E402
from bindweed_voice_lab import crack_info, hf_env, mod_rate, mreg, pulsed_w, reattack, tonal  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90  # noqa: E402
from lightkeeper_voice_lab import _wrap  # noqa: E402
from spellbreaker_voice_lab import as_replace, cen, heard_at, peer_name, seg  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "thornwake"
FALLBACK = "__fallback__"                 # an id no arm names: rune-crack
BLADE = 26.5                              # Thornwake's dmg (stage 5)
TOL = 1e-5                                # reproduction / transcription (-100 dB)
SCHOOL_AFF = "verdant"
TYPE_SHAPE = "scythe"
PEER_SCHOOL = {"heartwood": "Rootfast (v112), the verdant greatsword on the batch line"}
CAST_AUD, CRACK_AUD, BITE_AUD = 400.0, 300.0, 65.0   # the level-matched lengths, ms
CREAK_UNDER_DB = 3.0                      # the cast's creak alone under its rustle alone

# The retired arm: the freeze's cast voice, the anchor of the Sfx row (replace).
OLD_ARM = ('        } else if (w === "thornwake"){                  // creak and cinch\n'
           '          this._burst(t, { freq: 700, q: 3.0, gain: 0.24, dur: 0.6 });\n'
           '          this._tone (t, { freq: 150, to: 420, gain: 0.16, dur: 0.55, type:"triangle" });\n'
           '          this._tone (t + 0.34, { freq: 300, to: 120, gain: 0.14, dur: 0.3, type:"square" });')

# Tendril's root (v101 DEEP), its arm body as sc-tendril-fx carries it -- the
# snare's body, transcribed. Checked against `--tendril` at run time.
TENDRIL_ROOT = (
    '          const g = 0.5179, kc = 0.2683, kt = 0.3464;\n'
    '          for (let s = 0, k = 0; s < 0.188; k++){\n'
    '            const u = s / 0.2, a = g * kc * (0.45 + 0.55 * u);\n'
    '            this._tone(t + s, { freq: 260, gain: a, dur: 0.03, type:"sine" });\n'
    '            this._tone(t + s, { freq: 718, gain: a * 0.4, dur: 0.02, type:"sine" });\n'
    '            s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));\n'
    '          }\n'
    '          this._burst(t + 0.2, { freq: 2600, q: 0.8, gain: g * 0.8, dur: 0.035, type:"highpass" });\n'
    '          this._tone (t + 0.2, { freq: 60, to: 30, gain: g * kt, dur: 0.3, type:"sine" });')
TENDRIL_ROOT_SHA = "c5f203750ce3ed89"     # sha256[:16] of the body with its trailing newline
SNARE_OFF = TENDRIL_ROOT.replace("const g = 0.5179,", "const g = 0.518,", 1)   # the OFF control
assert SNARE_OFF != TENDRIL_ROOT


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


def _ind(lines, n):
    return "\n".join(" " * n + l_ for l_ in lines)


def sig4(v):
    return float(f"{v:.4g}")


# =============================================================== THE CAST ===
# "a rustle-and-creak, 0.4s". Every candidate is a rustle (noise) and a creak
# (a pulse train, slowing 45 -> 28 a second) over one span L; they differ in
# what the rustle is made of and what a creak pulse is.
CAST_CANDIDATES = [
    ("1 LEAVES", dict(rustle="leaves", creak="timber"),
     "leaves: 30 ms bandpass grains (Q 1.2) ~60 a second, centres wandering 820-2380 Hz, swelling to the "
     "middle; the creak a 330 Hz timber (a sine and its 2.76 mode at 0.4) pulsed 45 -> 28 a second"),
    ("2 BRUSH", dict(rustle="brush", creak="timber"),
     "brush: two overlapping bandpass sweeps (Q 0.7), 600 -> 1800 Hz and back 1800 -> 900 Hz; the same creak"),
    ("3 BRIAR", dict(rustle="briar", creak="timber"),
     "thorns: LEAVES' grains higher and drier (Q 0.9, centres 1730-3900 Hz); the same creak"),
    ("4 BOUGH", dict(rustle="leaves", creak="bough"),
     "LEAVES' rustle; the creak a heavier bough -- a 165 Hz triangle and its 2.76 mode at 0.4"),
    ("5 THORNS", dict(rustle="thorns", creak="timber"),
     "thorns: narrow grains (Q 5), centres wandering 2460-4160 Hz, swelling to the middle (round 2); the same "
     "creak"),
    ("6 BURRS", dict(rustle="burrs", creak="timber"),
     "burrs: grains a little wider (Q 4), centres wandering 2140-4200 Hz (round 2); the same creak"),
    ("7 SPINES", dict(rustle="spines", creak="timber"),
     "spines: narrow grains (Q 6), centres wandering 2310-3900 Hz (round 3); the same creak"),
    ("8 NEEDLES", dict(rustle="needles", creak="timber"),
     "needles: narrower grains (Q 8), centres wandering 2310-3900 Hz (round 3); the same creak"),
]
CAST_CONTROLS = [
    ("0 RUSTLE", dict(rustle="leaves", creak=None), "LEAVES' rustle alone -- a control on 'and-creak'"),
    ("0 CREAK", dict(rustle=None, creak="timber"), "LEAVES' creak alone -- a control on 'a rustle'"),
    ("0 HELD", dict(rustle="leaves", creak="held"),
     "LEAVES with its creak a held note (the 330 Hz timber re-struck at its own cycles) -- a control on 'creak'"),
]


def rustle_lines(sp, L):
    r_ = sp["rustle"]
    if r_ in ("leaves", "briar", "thorns", "burrs", "spines", "needles"):
        fx, q = {"leaves": ("1400 * Math.pow(1.7, Math.sin(k * 1.7))", "1.2"),
                 "briar": ("2600 * Math.pow(1.5, Math.sin(k * 1.7))", "0.9"),
                 "thorns": ("3200 * Math.pow(1.3, Math.sin(k * 1.7))", "5"),
                 "burrs": ("3000 * Math.pow(1.4, Math.sin(k * 1.7))", "4"),
                 "spines": ("3000 * Math.pow(1.3, Math.sin(k * 1.7))", "6"),
                 "needles": ("3000 * Math.pow(1.3, Math.sin(k * 1.7))", "8")}[r_]
        return [f"for (let s = 0, k = 0; s < {fmt(round(L - 0.03, 4))}; k++){{",
                f"  const u = s / {fmt(L)}, a = g * (0.3 + 0.7 * Math.sin(Math.PI * Math.min(1, u / 0.9)));",
                f'  this._burst(t + s, {{ freq: {fx}, q: {q}, gain: a, dur: 0.03, type:"bandpass" }});',
                "  s += 0.016 * (1 + 0.4 * Math.sin(k * 2.4));",
                "}"]
    if r_ == "brush":
        d_, a1 = round(L * 0.62, 4), round(L * 0.3, 4)
        return [f'this._sweep(t, {{ f0: 600, f1: 1800, q: 0.7, gain: g, dur: {fmt(d_)}, atk: {fmt(a1)}, '
                f'type:"bandpass" }});',
                f'this._sweep(t + {fmt(a1)}, {{ f0: 1800, f1: 900, q: 0.7, gain: g * 0.8, dur: {fmt(d_)}, '
                f'atk: {fmt(round(L * 0.12, 4))}, type:"bandpass" }});']
    raise ValueError(sp)


CPULSE = {
    "timber": ['this._tone(t + s, { freq: 330, gain: a, dur: 0.03, type:"sine" });',
               'this._tone(t + s, { freq: 911, gain: a * 0.4, dur: 0.02, type:"sine" });'],
    "bough": ['this._tone(t + s, { freq: 165, gain: a, dur: 0.035, type:"triangle" });',
              'this._tone(t + s, { freq: 455, gain: a * 0.4, dur: 0.025, type:"sine" });'],
}


def creak_lines(sp, L):
    c_ = sp["creak"]
    end = fmt(round(L - 0.03, 4))
    lv = f"const u = s / {fmt(L)}, a = g * kc * (0.6 + 0.4 * Math.sin(Math.PI * u));"
    if c_ == "held":
        return [f"for (let s = 0.02; s < {end}; s += 1 / 330){{",
                f"  {lv}",
                '  this._tone(t + s, { freq: 330, gain: a, dur: 0.03, type:"sine" }).frequency.value = 330;',
                "}"]
    return [f"for (let s = 0.02, k = 0; s < {end}; k++){{",
            f"  {lv}",
            *["  " + l_ for l_ in CPULSE[c_]],
            "  s += 0.022 * Math.pow(1.6, u) * (1 + 0.12 * Math.sin(k * 2.4));",
            "}"]


def cast_body(sp, g, kc, L, part="both", ind=10):
    L_ = [f"const g = {fmt(g)}, kc = {fmt(kc)};"]
    if part in ("both", "rustle") and sp["rustle"]:
        L_ += rustle_lines(sp, L)
    if part in ("both", "creak") and sp["creak"]:
        L_ += creak_lines(sp, L)
    return _ind(L_, ind)


# ============================================================ THE CRACKLE ===
# "a bramble opening -- a dry crackle". Every candidate is a run of short noise
# clicks over the bramble's 0.3 s growth, spaced x (1 + 0.45 sin 2.4k); they
# differ in what a click is and how the run goes.
CRACKLE_CANDIDATES = [
    ("1 SNAPS", dict(kind="snaps"),
     "5 ms highpass clicks (2.5 kHz) ~33 a second, irregular, thinning in level as it opens"),
    ("2 OPEN", dict(kind="open"),
     "the same clicks QUICKENING 22 -> 50 a second and growing, as the bramble grows out"),
    ("3 TWIGS", dict(kind="twigs"),
     "6 ms bandpass clicks (Q 3) at centres wandering 1.6-4.5 kHz: twigs of different sizes"),
    ("4 EMBERS", dict(kind="embers"),
     "pops ~24 a second, every other one with a smaller pop 8 ms after it (a fire's crackle)"),
    ("5 KNOTS", dict(kind="knots"),
     "8 ms narrow bandpass clicks (Q 6) at centres wandering 1185-2160 Hz: knots in dry wood (round 2)"),
    ("6 SPLINTERS", dict(kind="splinters"),
     "8 ms narrower clicks (Q 8) at centres wandering 1480-2700 Hz: splinters (round 2)"),
]
CRACKLE_CONTROLS = [
    ("0 HISS", dict(kind="hiss"), "one swell of SNAPS' band, no clicks -- a control on 'a crackle'"),
    ("0 EVEN", dict(kind="even"), "SNAPS' clicks evenly spaced -- a control on 'a crackle' (irregular)"),
    ("0 WET", dict(kind="wet"), "SNAPS with a falling sine body under every click -- a control on 'dry'"),
]


def crackle_body(sp, g, S, ind=10):
    k_ = sp["kind"]
    Sf = fmt(S)
    L = [f"const g = {fmt(g)};"]
    if k_ == "hiss":
        L += [f'this._sweep(t, {{ f0: 2500, f1: 2500, q: 0.7, gain: g, dur: {Sf}, atk: 0.05, type:"highpass" }});']
        return _ind(L, ind)
    step = {"snaps": "0.03 * (1 + 0.45 * Math.sin(k * 2.4))",
            "wet": "0.03 * (1 + 0.45 * Math.sin(k * 2.4))",
            "even": "0.03",
            "open": "0.045 * Math.pow(0.45, u) * (1 + 0.45 * Math.sin(k * 2.4))",
            "twigs": "0.03 * (1 + 0.45 * Math.sin(k * 2.4))",
            "knots": "0.03 * (1 + 0.45 * Math.sin(k * 2.4))",
            "splinters": "0.03 * (1 + 0.45 * Math.sin(k * 2.4))",
            "embers": "0.042 * (1 + 0.45 * Math.sin(k * 2.4))"}[k_]
    lv = "g * (0.5 + 0.5 * u)" if k_ == "open" else "g * (1 - 0.4 * u)"
    L += [f"for (let s = 0, k = 0; s < {Sf}; k++){{",
          f"  const u = s / {Sf}, a = {lv};"]
    if k_ == "twigs":
        L += ['  this._burst(t + s, { freq: 2700 * Math.pow(1.65, Math.sin(k * 1.9)), q: 3, gain: a, dur: 0.006, '
              'type:"bandpass" });']
    elif k_ in ("knots", "splinters"):
        fx, q = ("1600 * Math.pow(1.35, Math.sin(k * 1.9))", "6") if k_ == "knots" else \
            ("2000 * Math.pow(1.35, Math.sin(k * 1.9))", "8")
        L += [f'  this._burst(t + s, {{ freq: {fx}, q: {q}, gain: a, dur: 0.008, type:"bandpass" }});']
    else:
        L += ['  this._burst(t + s, { freq: 2500, q: 0.7, gain: a, dur: 0.005, type:"highpass" });']
    if k_ == "embers":
        L += ['  if (k % 2 === 0) this._burst(t + s + 0.008, { freq: 3500, q: 0.7, gain: a * 0.45, dur: 0.004, '
              'type:"highpass" });']
    if k_ == "wet":
        L += ['  this._tone(t + s, { freq: 300, to: 150, gain: a * 2, dur: 0.05, type:"sine" });']
    L += [f"  s += {step};", "}"]
    return _ind(L, ind)


# =============================================================== THE BITE ===
# "a bite -- a soft snap". A short noise snap over a small falling body; they
# differ in the snap's filter and the body's pitch.
BITE_CANDIDATES = [
    ("1 STEM", dict(kind="stem"), "a 10 ms bandpass snap at 1.1 kHz (Q 1.2) over a sine falling 620 -> 420 Hz"),
    ("2 KNOT", dict(kind="knot"), "a 12 ms lowpass snap (1.8 kHz) over a triangle falling 440 -> 330 Hz"),
    ("3 PRICK", dict(kind="prick"), "a 6 ms bandpass snap at 1.6 kHz (Q 2) over a sine falling 1200 -> 900 Hz"),
    ("4 PAD", dict(kind="pad"), "a 15 ms lowpass snap (900 Hz) over a sine falling 300 -> 220 Hz"),
]
BITE_CONTROLS = [
    ("0 BRIGHT", dict(kind="stem", mul=3.0), "STEM with every frequency x 3 -- a control on 'soft' (dull)"),
    ("0 SLOW", dict(kind="slow"), "STEM's band as a swell (25 ms attack), no snap -- a control on 'a snap'"),
    ("0 DOUBLE", dict(kind="stem", twice=True), "STEM struck twice, 30 ms apart -- a control on one snap"),
    ("0 LOUD", dict(kind="stem", loud=6.0), "STEM six times louder -- a control on 'soft' (quiet)"),
]
BPARTS = {
    "stem": ('this._burst({T}, {{ freq: {a}, q: 1.2, gain: g, dur: 0.01, type:"bandpass" }});',
             'this._tone({T}, {{ freq: {b}, to: {c}, gain: g * 0.6, dur: D, type:"sine" }});', (1100, 620, 420)),
    "knot": ('this._burst({T}, {{ freq: {a}, q: 0.7, gain: g, dur: 0.012, type:"lowpass" }});',
             'this._tone({T}, {{ freq: {b}, to: {c}, gain: g * 0.6, dur: D, type:"triangle" }});', (1800, 440, 330)),
    "prick": ('this._burst({T}, {{ freq: {a}, q: 2, gain: g, dur: 0.006, type:"bandpass" }});',
              'this._tone({T}, {{ freq: {b}, to: {c}, gain: g * 0.4, dur: D, type:"sine" }});', (1600, 1200, 900)),
    "pad": ('this._burst({T}, {{ freq: {a}, q: 0.7, gain: g, dur: 0.015, type:"lowpass" }});',
            'this._tone({T}, {{ freq: {b}, to: {c}, gain: g * 0.7, dur: D, type:"sine" }});', (900, 300, 220)),
}


def bite_body(sp, g, D, ind=10):
    k_ = sp["kind"]
    gg = g * sp.get("loud", 1.0)
    L = [f"const g = {fmt(round(gg, 6))}, D = {fmt(D)};"]
    if k_ == "slow":
        L += ['this._sweep(t, { f0: 1100, f1: 1100, q: 1.2, gain: g, dur: D, atk: 0.025, type:"bandpass" });']
        return _ind(L, ind)
    b_, t_, (a, b, c) = BPARTS[k_]
    m_ = sp.get("mul", 1.0)
    a, b, c = (fmt(round(v * m_, 4)) for v in (a, b, c))
    for T in (["t", "t + 0.03"] if sp.get("twice") else ["t"]):
        L += [b_.format(T=T, a=a), t_.format(T=T, b=b, c=c)]
    return _ind(L, ind)


# ================================================================ THE ROWS ==
CRACKLE_ANCHOR = '    f.brambleTally.planted++;'
SNARE_ANCHOR = '            T.snares++;'
BITE_ANCHOR = '          f.brambleCd = u.tickCd;'

CRACKLE_CODE = '''
    /* BRAMBLESNARE'S CRACKLE (v84 s4 SOUND: "a bramble opening -- a dry
       crackle"): once per bramble planted, on the landing blow's own frame,
       after the count. Presentation only: SFX.play draws nothing, is a no-op
       headless, and nothing here is read back (thornwake_voice_lab: fights
       identical). */
    SFX.play("ult", { w: "thornwake-crackle" });'''

SNARE_CODE = '''
            /* BRAMBLESNARE'S SNARE (v84 s4 SOUND: "the snare -- a short creak
               and crack (Tendril's root voice, reused)"): on the frame the pin
               is written -- the foe stepping into a bramble -- after the count.
               Plain SFX.play; nothing is read back. */
            SFX.play("ult", { w: "thornwake-snare" });'''

BITE_CODE = '''
          /* BRAMBLESNARE'S BITE (v84 s4 SOUND: "a bite -- a soft snap"): one
             snap per bite, on the bite's own step, as the thorns' cooldown is
             re-armed -- the line every bite starts with -- ahead of its
             entangle and its hurt on the same step. A killing bite snaps too
             (the number of snaps is the number of bites); its fatal beat is
             the sim's, below. Presentation only: SFX.play draws nothing, is a
             no-op headless, and nothing here is read back
             (thornwake_voice_lab: fights identical). */
          SFX.play("ult", { w: "thornwake-bite" });'''

# the sim-write control: the bite row with the foe nudged 1e-9 on a bite voice
BITE_CODE_BAD = BITE_CODE.replace('          SFX.play("ult", { w: "thornwake-bite" });',
                                  '          foe.vx += 1e-9; SFX.play("ult", { w: "thornwake-bite" });', 1)
assert BITE_CODE_BAD != BITE_CODE

SIM_ROWS = [("plant", CRACKLE_ANCHOR, "after", CRACKLE_CODE), ("tick", SNARE_ANCHOR, "after", SNARE_CODE),
            ("tick", BITE_ANCHOR, "after", BITE_CODE)]
_refuse(CRACKLE_CODE + SNARE_CODE + BITE_CODE, "sim rows")
for _w, _a, _m, _c in SIM_ROWS:
    assert _a not in _c, "a before/after row's code must not repeat its anchor"
    assert _c.isascii(), "a row must be ASCII"
    assert (_c.endswith("\n") if _m == "before" else _c.startswith("\n")), "a row's code must join its anchor"


RNAME = {"scour woosh": "Scour's woosh", "scour tick": "Scour's tick", "fork": "fork", "wall": "the wall tick",
         "hit": "the blow", "T:cast": "Tendril's cast", "T:bite2": "Tendril's bite", "T:bite4": "Tendril's bite",
         "T:root": "Tendril's root", "T:wither": "Tendril's wither", "cast": "the cast", "snare": "the snare",
         "bite": "the bite", "vine plant": "the vine's plant", "spark burn": "the spark's burn"}


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


def arms_code(Ca, Cr, Bi, info):
    cn, rn, bn = (X["name"].split(maxsplit=1)[1] for X in (Ca, Cr, Bi))
    c_cast = _wrap([
        f'BRAMBLESNARE\'S CAST -- v84 s4: "cast -- a rustle-and-creak, 0.4s". {cn}, of {info["n_cast"]}, picked '
        f'on the numbers by `thornwake_voice_lab.py` under Rick\'s "you pick i overrule" (v113). It REPLACES the '
        f'freeze\'s "creak and cinch" -- the three lines that were this arm -- which the redesign retires with the '
        f'freeze (v84 s5); nothing else in the synth moved.',
        f"{info['c_what']} The rustle is noise (no peak over {info['c_tonal']:.1f} dB), centred at "
        f"{info['c_cen0']:.0f}-{info['c_cen1']:.0f} Hz on every noise draw and not struck (its loudest millisecond "
        f"{info['c_rise']:.0f} ms in); the creak is stick-slip, {info['c_rate']:.0f} pulses a second (PULSED "
        f"{info['c_pulsed']:.2f}), {info['c_cdb']:+.1f} dB re the rustle, and each owns a third-octave (the rustle "
        f"+{info['c_rown']:.0f} dB, the creak +{info['c_cown']:.0f} dB over the other). Audible "
        f"{info['c_aud']:.0f} ms; its loudest 50 ms {info['c_db']:+.1f} dB re Thornwake's blow. Register at most "
        f"{info['c_reg']:.2f} ({info['c_regk']}) against rune-crack, the verdant and scythe casts (Tendril's among "
        f"them), the house's voices, the blow, the death voice and the snare."], 10)
    c_crk = _wrap([
        f'A BRAMBLE OPENS -- "a bramble opening -- a dry crackle" (v84 s4). {rn}, of {info["n_crk"]} '
        f'(`thornwake_voice_lab.py`). `plantBramble` plays it once per bramble, on the landing blow\'s frame.',
        f"{info['r_what']} {info['r_clicks']} clicks or more at irregular intervals (their spacing varies "
        f"{info['r_irreg']:.2f} of its mean), {info['r_depth']:.0f} dB deep; dry -- {info['r_b500']:.3f} of its "
        f"power below 500 Hz and no ring (no peak over {info['r_tonal']:.1f} dB). Audible {info['r_aud']:.0f} ms, "
        f"the bramble's 0.3 s growth; its loudest 50 ms {info['r_db']:+.1f} dB re the blow it lands with, heard "
        f"{info['r_heard']:+.1f} dB over the score after the blow's body. Register at most {info['r_reg']:.2f} "
        f"({info['r_regk']}) against the blow, the wall tick, rune-crack, fork, hex-snap, the vine's plant, the "
        f"spark's burn, Scour's tick, Tendril's bite and wither, the cast, the bite and the snare."], 10)
    c_snr = _wrap([
        f'THE SNARE -- "the snare -- a short creak and crack (Tendril\'s root voice, reused)" (v84 s4). Tendril\'s '
        f'root (`ult/bindweed-root`, v101 DEEP) is not on the link this was built on, so this arm is made here: its '
        f'body is that arm\'s nine lines, transcribed unchanged (`thornwake_voice_lab.py` renders it equal to '
        f'Tendril\'s own to {info["s_same"]:.0e}). `tickBramble` plays it on the frame the pin is written.',
        f"Canopy's timber an octave and a half down (a 260 Hz sine and its 2.76 mode at 0.4) pulsed for 0.2 s, "
        f"then a highpass crack over a sine falling 60 -> 30 Hz: audible {info['s_aud']:.0f} ms, its loudest 50 ms "
        f"{info['s_db']:+.1f} dB re Thornwake's blow, {info['s_low']:.2f} of its power below 120 Hz."], 10)
    c_bite = _wrap([
        f'A BITE -- "a bite -- a soft snap" (v84 s4). {bn}, of {info["n_bite"]} (`thornwake_voice_lab.py`). '
        f'`tickBramble` plays it once per bite (every 0.5 s of unfrozen time in a bramble), a killing bite too.',
        f"{info['b_what']} Struck (rise {info['b_rise']:.0f} ms, one snap), audible "
        f"{info['b_aud0']:.0f}{'' if info['b_aud0'] == info['b_aud1'] else '-%.0f' % info['b_aud1']} ms; soft -- "
        f"its loudest 50 ms {info['b_db']:+.1f} dB re the blow and {info['b_wdb']:+.1f} dB re the wall tick, the "
        f"snap's first 10 ms centred at {info['b_cen']:.0f} Hz at most. Register at most {info['b_reg']:.2f} "
        f"({info['b_regk']}) against the blow, the wall, fork, hex-snap, the vine's plant, Tendril's bite, "
        f"rune-crack, the cast and the snare."], 10)
    return (f'{_arm_head(ME, "the thorns wake")}\n'
            f'{c_cast}\n{cast_body(Ca["sp"], Ca["g"], Ca["kc"], Ca["L"])}\n'
            f'{_arm_head(ME + "-crackle", "a bramble opens")}\n'
            f'{c_crk}\n{crackle_body(Cr["sp"], Cr["g"], Cr["S"])}\n'
            f'{_arm_head(ME + "-snare", "and the foe is snared")}\n'
            f'{c_snr}\n{TENDRIL_ROOT}\n'
            f'{_arm_head(ME + "-bite", "and bitten")}\n'
            f'{c_bite}\n{bite_body(Bi["sp"], Bi["g"], Bi["D"])}')


# ============================================================== THE PAGE ===
COST_JS = r"""([rows, reps, ME, BLADE]) => {
  const proto = Object.getPrototypeOf(AC.SFX);
  let src = proto.play.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const oc = new OfflineAudioContext(1, 48000 * 4, 48000);
  const S = Object.create(proto); S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = oc.createBuffer(1, 28800, 48000);
  S.play = patched;
  const med = (v) => v.slice().sort((x, y) => x - y)[v.length >> 1];
  const out = {};
  for (const [k, kind, p] of [["cast", "ult", { w: ME }], ["crackle", "ult", { w: ME + "-crackle" }],
                              ["snare", "ult", { w: ME + "-snare" }], ["bite", "ult", { w: ME + "-bite" }],
                              ["hit", "hit", { dmg: BLADE, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The per-step digest and the fighter snapshot, shared by WIRE_JS and FIGHTS_JS.
COMMON_JS = r"""
  const F64 = new Float64Array(1), U32 = new Uint32Array(F64.buffer);
  const mix = (h, v) => { F64[0] = +v; h = Math.imul(h ^ U32[0], 16777619) >>> 0;
                          return Math.imul(h ^ U32[1], 16777619) >>> 0; };
  const fr = (x) => [x.hp, x.x, x.y, x.vx, x.vy, x.charge, x.theta, x.alive, x.pin, x.pinMax, x.pinFree,
                     x.stacks("entangle"), x.brambleCd, x.brambleIn, x.ultBramble ? x.ultBramble.t : null];
  const dig = (h, m) => { for (const x of [m.a, m.b])
      for (const v of [x.x, x.y, x.hp, x.pin, x.vx, x.stacks("entangle")]) h = mix(h, v);
    h = mix(h, m.brambles ? m.brambles.length : -1); h = mix(h, m.brambleT || 0); return h; };
  const sumOf = (m, h) => JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.winner ? m.winner.w.id : null,
    m.a.brambleTally || null, m.b.brambleTally || null, m.brambles ? m.brambles.map(b => [b.x, b.y, b.t0, b.side]) : null,
    m.brambleT, h]);
"""

# The plantBramble and tickBramble rows, applied to the real prototypes and run
# beside the originals; the survey of the windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows, ME]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
""" + COMMON_JS + r"""
  const oT = P.tickBramble, oP = P.plantBramble;
  if (!oT || !oP) return { err: "no tickBramble / plantBramble on this page" };
  const patch = (fn, rs) => { let src = fn.toString();
    for (const [anc, code] of rs){ const at = src.split(anc).length - 1;
      if (at !== 1) return { err: `an anchor occurs ${at} times in ${fn.name}()` };
      src = src.replace(anc, () => code); }
    return { fn: (0, eval)("(function " + src + ")") }; };
  const pT = patch(oT, rows.tick), pP = patch(oP, rows.plant);
  if (pT.err) return pT; if (pP.err) return pP;
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  for (const nm of ["CONFIG", "clamp"])
    if ((0, eval)("typeof " + nm) === "undefined") return { err: nm + " is not reachable from a patched ticker" };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a;
    let step = 0, inT = 0, inP = 0, h = 2166136261;
    const other = [], mine = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) mine.push([step, w, inT ? "T" : inP ? "P" : "-",
                                                         Object.keys(p).sort().join(","), m.t]);
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const implT = wire ? pT.fn : oT, implP = wire ? pP.fn : oP;
    const tal = () => { const T = f.brambleTally; return T ? [T.planted, T.snares, T.ticks, T.kills] : [0, 0, 0, 0]; };
    const st = { planted: 0, snares: 0, ticks: 0, kills: 0, killBites: 0, crackV: 0, snareV: 0, biteV: 0,
                 together: 0, order: 0, bad: [] };
    P.plantBramble = function(g, q){
      const c0 = mine.length, t0 = tal(); inP++;
      try { return implP.call(this, g, q); }
      finally {
        inP--;
        const t1 = tal(), v = mine.slice(c0), dv = v.filter(c => c[1] === ME + "-crackle").length;
        st.planted += t1[0] - t0[0]; st.crackV += dv;
        if (g !== f) st.bad.push(["a plant by the other side", step]);
        if (dv !== t1[0] - t0[0] || v.length !== dv) st.bad.push(["crackle voices vs planted", dv, t1[0] - t0[0], step]);
      } };
    P.tickBramble = function(dt){
      const c0 = mine.length, t0 = tal(); inT++;
      try { return implT.call(this, dt); }
      finally {
        inT--;
        const t1 = tal(), v = mine.slice(c0);
        const sv = v.filter(c => c[1] === ME + "-snare").length, bv = v.filter(c => c[1] === ME + "-bite").length;
        st.snares += t1[1] - t0[1]; st.ticks += t1[2] - t0[2]; st.kills += t1[3] - t0[3];
        if (t1[3] > t0[3] && bv >= t1[3] - t0[3]) st.killBites += t1[3] - t0[3];
        st.snareV += sv; st.biteV += bv;
        if (sv && bv){ st.together++; if (v[0][1] === ME + "-snare") st.order++; }
        if (sv !== t1[1] - t0[1]) st.bad.push(["snare voices vs snares", sv, t1[1] - t0[1], step]);
        if (bv !== t1[2] - t0[2]) st.bad.push(["bite voices vs bites", bv, t1[2] - t0[2], step]);
        if (v.length !== sv + bv) st.bad.push(["another voice from tickBramble", step]);
      } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; h = dig(h, m); } }
    finally { P.tickBramble = oT; P.plantBramble = oP; if (had) S.play = op; else delete S.play; }
    const T = f.brambleTally || {};
    const castV = mine.filter(c => c[1] === ME && c[2] === "-" && c[3] === "w").length;
    const where = mine.filter(c => (c[1] === ME + "-crackle" && c[2] !== "P")
                                   || ((c[1] === ME + "-snare" || c[1] === ME + "-bite") && c[2] !== "T")
                                   || (c[1] === ME && c[2] !== "-") || c[3] !== "w").length;
    const cv = mine.filter(c => c[1] === ME);
    const wins = cv.map((c, i) => {
      const t0 = c[4], t1 = i + 1 < cv.length ? cv[i + 1][4] : Infinity;
      const sub = mine.filter(q => q[4] >= t0 && q[4] < t1 && q[1] !== ME);
      return { side, foe: fid, seed: sd, cast: t0, next: t1 === Infinity ? null : t1,
               crackles: sub.filter(q => q[1] === ME + "-crackle").length,
               snares: sub.filter(q => q[1] === ME + "-snare").length,
               bites: sub.filter(q => q[1] === ME + "-bite").length,
               last: sub.length ? sub[sub.length - 1][4] : t0 }; });
    return { sum: sumOf(m, h), other: JSON.stringify(other), st, castV, where, casts: T.casts || 0,
             nMine: mine.length, wins, over: m.t };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const tot = { casts: 0, castV: 0, planted: 0, crackV: 0, snares: 0, snareV: 0, ticks: 0, biteV: 0, kills: 0,
                killBites: 0, together: 0, order: 0 };
  const pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.nMine !== A.castV) bad.push([fid, sd, "the UNPATCHED functions played a voice", A.nMine - A.castV]);
    if (B.st.bad.length) bad.push([fid, sd, ...B.st.bad[0], "(" + B.st.bad.length + ")"]);
    if (B.where) bad.push([fid, sd, "a voice from the wrong place or with opts", B.where]);
    if (B.castV !== B.casts) bad.push([fid, sd, "cast voices vs casts", B.castV, B.casts]);
    tot.casts += B.casts; tot.castV += B.castV;
    for (const k of ["planted", "crackV", "snares", "snareV", "ticks", "biteV", "kills", "killBites", "together", "order"])
      tot[k] += B.st[k];
    for (const W of B.wins) pick.push(W);
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), tot, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rows, ME]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const oT = P.tickBramble, oP = P.plantBramble;
  let sT = oT.toString(); for (const [anc, code] of rows.tick) sT = sT.replace(anc, () => code);
  let sP = oP.toString(); for (const [anc, code] of rows.plant) sP = sP.replace(anc, () => code);
  const pT = (0, eval)("(function " + sT + ")"), pP = (0, eval)("(function " + sP + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickBramble = pT; P.plantBramble = pP;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickBramble = oT; P.plantBramble = oP; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds, ME]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype;
""" + COMMON_JS + r"""
  const res = [];
  if (!P.tickBramble) return { err: "no tickBramble" };
  const oT = P.tickBramble, oP = P.plantBramble;
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    let inT = 0, inP = 0, h = 2166136261;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, inT ? "T" : inP ? "P" : "-", Object.keys(p).join(",")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    P.tickBramble = function(dt){ inT = 1; try { return oT.call(this, dt); } finally { inT = 0; } };
    P.plantBramble = function(g, q){ inP = 1; try { return oP.call(this, g, q); } finally { inP = 0; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; h = dig(h, m); } }
    finally { P.tickBramble = oT; P.plantBramble = oP; if (had) S.play = op; else delete S.play; }
    const T = f.brambleTally || {};
    res.push({ key: [sd, fid, side].join(":"), sum: sumOf(m, h),
               casts: T.casts || 0, planted: T.planted || 0, snares: T.snares || 0, ticks: T.ticks || 0,
               castV: log.filter(e => e[0] === ME && e[1] === "-").length,
               crackV: log.filter(e => e[0] === ME + "-crackle" && e[1] === "P").length,
               snareV: log.filter(e => e[0] === ME + "-snare" && e[1] === "T").length,
               biteV: log.filter(e => e[0] === ME + "-bite" && e[1] === "T").length,
               stray: log.filter(e => e[2] !== "w" || (e[0] === ME) !== (e[1] === "-")
                                      || (e[0] === ME + "-crackle" && e[1] !== "P")
                                      || ((e[0] === ME + "-snare" || e[0] === ME + "-bite") && e[1] !== "T")).length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def clicks(x, a, b, fc=1500.0):
    """CLICKS and IRREG over [a, b] s after the event (see the docstring):
    the onsets' count and the coefficient of variation of their intervals.
    The envelope is read with a silent millisecond before it (nothing sounds
    before the event), so a click on the event's own first millisecond
    counts."""
    np = _np()
    e = np.concatenate([[0.0], hf_env(x, fc), [0.0]])
    j0, j1 = int(round(a * 1000)) + 1, min(len(e) - 2, int(round(b * 1000)) + 1)
    top = float(e[j0:j1 + 1].max()) if j1 > j0 else 0.0
    if top <= 0:
        return 0, 0.0
    on, dip = [], 0.0
    for j in range(j0, j1 + 1):
        dip = min(dip, float(e[j]))
        if e[j] >= e[j - 1] and e[j] >= e[j + 1] and e[j] >= top * 0.1 and e[j] >= 2.0 * dip:
            on.append(j)
            dip = float("inf")
    if len(on) < 3:
        return len(on), 0.0
    d = np.diff(on).astype(float)
    return len(on), float(d.std() / d.mean())


def depth(x, a, b, fc=1500.0):
    """DEPTH: p90 / p10 of the 1 ms high-passed envelope over [a, b] s, dB."""
    np = _np()
    e = hf_env(x, fc)[int(round(a * 1000)):int(round(b * 1000))]
    return db(float(np.percentile(e, 90)) / max(float(np.percentile(e, 10)), 1e-12))


def own(xa, xb, a, b, lo=100.0, hi=12000.0):
    """OWN: the third-octave (lo-hi) in which xa over [a, b] s after the event
    stands highest over xb, dB, and where."""
    ba = bands(seg(xa, a, b)); bb = bands(seg(xb, a, b))
    return max(((db(ba[i] / max(bb[i], 1e-12)), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v84 s4 turned into a number (THE DECLARED
# CHOICES); a rule no candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms on every draw; 'a rustle': the rustle alone is noise "
    "(TONAL <= 10 dB over 300-8000 Hz), its centroid 400-4000 Hz on every draw, not struck (RISE >= 30 ms); "
    "'a creak': the creak alone's RATE 17-83 a second and PULSED >= 0.40; 'rustle-and-creak': each part OWNS "
    "a third-octave (>= +6 dB over the other alone) and the creak alone is within -9..+3 dB of the rustle "
    "alone; heard (HEARD over its first 100 ms >= +6 dB). Level: TOP between 0.5x the blow's loudest 50 ms on "
    "its LOUDEST draw and 1.0x on its QUIETEST, on every draw. Register against rune-crack, each verdant and "
    "scythe cast with a voice of its own, Tendril's four voices, the house's, the blow, the death voice and "
    "the snare each <= 0.80. Tiebreak: the most distinct register (to 0.05), then the fewest synth calls, "
    "then the order listed.")

CRACKLE_RULE = (
    "'opening' (the bramble's 0.3 s growth): AUDIBLE 250-350 ms and GONE <= 350 ms on every draw; 'a "
    "crackle': CLICKS >= 6, IRREG >= 0.15 and DEPTH >= 12 dB on every draw; 'dry': LOW <= 0.02 and B500 <= "
    "0.05 on the worst draw and TONAL <= 10 dB over 1-12 kHz; under the blow and heard: TOP between 2x the "
    "wall tick's (loudest draw) and 0.5x the blow's (quietest draw) on every draw, HEARD over 100-200 ms >= "
    "+6 dB on every draw. Register against the blow, the wall tick, rune-crack, fork, hex-snap, the vine's "
    "plant, the spark's burn, Scour's tick, Tendril's bite and wither, the picked cast, bite and the snare "
    "each <= 0.80. Tiebreak: the most distinct register (to 0.05), then the fewest synth calls, then the "
    "order listed.")

BITE_RULE = (
    "'a snap': RISE <= 3 ms and the peak in the first 10 ms on every draw, no RE-ATTACK on any (one snap a "
    "call); short: AUDIBLE 30-100 ms, GONE <= 110 ms; 'soft': TOP between 2x the wall tick's (loudest draw) "
    "and 0.5x the blow's (quietest draw) on every draw and the snap dull: the CENTROID of its first 10 ms <= "
    "2000 Hz on every draw (round 2); heard (HEARD "
    "over its first 100 ms >= +6 dB). Register against the blow, the wall tick, fork, hex-snap, the vine's "
    "plant, Tendril's bite (at 2 and 4 stacks), rune-crack, the picked cast and the snare each <= 0.80. "
    "Tiebreak: the most distinct register (to 0.05), then the fewest synth calls, then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def _regs_why(M, why, cap=0.80):
    for k, v in M["regs"].items():
        if v > cap:
            why.append(f"register vs {k} {v:.2f} > {cap:.2f}")


def cast_why(M, lev):
    why = []
    if not (330 <= M["aud_lo"] and M["aud_hi"] <= 470): why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms")
    if M["gone_hi"] > 470: why.append(f"gone at {M['gone_hi']:.0f} ms > 470")
    if M["r_none"]:
        why.append("no rustle")
    else:
        if M["r_tonal"] > 10: why.append(f"the rustle {M['r_tonal']:.1f} dB tonal > 10 (not noise)")
        if not (400 <= M["r_cen0"] and M["r_cen1"] <= 4000):
            why.append(f"the rustle centred {M['r_cen0']:.0f}-{M['r_cen1']:.0f} Hz, not 400-4000")
        if M["r_rise"] < 30: why.append(f"the rustle's rise {M['r_rise']:.0f} ms < 30 (struck)")
    if M["c_none"]:
        why.append("no creak")
    else:
        if not 17 <= M["c_rate"] <= 83: why.append(f"the creak's rate {M['c_rate']:.0f}/s, not 17-83 (not stick-slip)")
        if M["c_pulsed"] < 0.40: why.append(f"the creak's PULSED {M['c_pulsed']:.2f} < 0.40")
    if M["r_none"] or M["c_none"]:
        why.append("not a rustle AND a creak")
    else:
        if M["r_own"] < 6: why.append(f"the rustle owns no band ({M['r_own']:+.1f} dB)")
        if M["c_own"] < 6: why.append(f"the creak owns no band ({M['c_own']:+.1f} dB)")
        if not -9 <= M["c_db"] <= 3: why.append(f"the creak {M['c_db']:+.1f} dB re the rustle, not -9..+3")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    _regs_why(M, why)
    return why


def crackle_why(M, lev):
    why = []
    if not (250 <= M["aud_lo"] and M["aud_hi"] <= 350): why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms")
    if M["gone_hi"] > 350: why.append(f"gone at {M['gone_hi']:.0f} ms > 350")
    if M["clicks"] < 6: why.append(f"{M['clicks']} clicks < 6 (not a crackle)")
    if M["irreg"] < 0.15: why.append(f"IRREG {M['irreg']:.2f} < 0.15 (a regular train)")
    if M["depth"] < 12: why.append(f"depth {M['depth']:.1f} dB < 12 (not clicks)")
    if M["low"] > 0.02: why.append(f"LOW {M['low']:.3f} > 0.02 (a body)")
    if M["b500"] > 0.05: why.append(f"B500 {M['b500']:.3f} > 0.05 (not dry)")
    if M["tonal"] > 10: why.append(f"tonal {M['tonal']:.1f} dB > 10 (a ring)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6 after the blow's body")
    _regs_why(M, why)
    return why


def bite_why(M, lev):
    why = []
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms > 3 (not struck)")
    if M["pk_ms"] > 10: why.append(f"peaks at {M['pk_ms']:.0f} ms (not a snap)")
    if M["re"]: why.append(f"a second snap on {M['re']} draw(s)")
    if not (30 <= M["aud_lo"] and M["aud_hi"] <= 100): why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms")
    if M["gone_hi"] > 110: why.append(f"gone at {M['gone_hi']:.0f} ms > 110")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f} (not soft)")
    if M["cen_hi"] > 2000: why.append(f"the snap centred {M['cen_hi']:.0f} Hz > 2000 (bright, not soft)")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    _regs_why(M, why)
    return why


def _show(rows, ctls, rule, name):
    print(f"  RULE  {rule}")
    for M in rows:
        if M["why"]:
            print(f"    {M['name']:<12} out: {'; '.join(M['why'][:6])}" + (" ..." if len(M["why"]) > 6 else ""))
    for M in ctls:
        if M["why"]:
            print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
        else:
            print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
            FAILED.append(f"{name} {M['name'].lower()} control")


def top2(r_):
    """The two highest registers of a voice, printed."""
    k2 = sorted(r_, key=r_.get, reverse=True)[:2]
    return ", ".join(f"{r_[k]:.2f} {k}" for k in k2)


def _slug(name):
    return name.replace(" ", "-").lower()


def tendril_arms(path):
    """Tendril's four arms (sc-tendril-fx), as the text between its cast arm's
    head and the rune-crack fallback, and its root arm's body."""
    s = pathlib.Path(path).read_text(encoding="utf-8")
    i = s.index('        } else if (w === "bindweed"){')
    j = s.index('        } else {                                        // rune-crack', i)
    arms = s[i:j]
    r0 = s.index('        } else if (w === "bindweed-root"){', i)
    r1 = s.index('        } else if (w === "bindweed-wither"){', r0)
    arm = s[r0:r1]
    body = arm[arm.index("*/\n") + 3:]
    return arms, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Thornwake's stage 5 (Bramblesnare)")
    ap.add_argument("--also", action="append", default=[],
                    help="another link carrying it (e.g. carried onto a newer tip): the rows as text there")
    ap.add_argument("--tendril", default="../02-chain/sc-tendril-fx.html",
                    help="a link carrying Tendril's voices (the snare's source and the school's references)")
    ap.add_argument("--out", default="../05-reference/v113")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=113601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "crackle": CRACKLE_RULE, "bite": BITE_RULE}}
    for nm, anc in (("the old thornwake arm", OLD_ARM), ("plantBramble planted", CRACKLE_ANCHOR),
                    ("tickBramble snares", SNARE_ANCHOR), ("tickBramble ticks", BITE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("thornwake-crackle", "thornwake-snare", "thornwake-bite", FALLBACK):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    tp_ = (HERE / a.tendril).resolve() if not pathlib.Path(a.tendril).is_absolute() else pathlib.Path(a.tendril)
    t_arms, t_body = tendril_arms(tp_)
    t_sha = hashlib.sha256(t_body.encode()).hexdigest()[:16]
    if t_body != TENDRIL_ROOT + "\n" or t_sha != TENDRIL_ROOT_SHA:
        raise SystemExit(f"Tendril's root on {tp_.name} ({t_sha}) is not the body this lab transcribes")
    rec["tendril"] = dict(link=tp_.name, sha=hashlib.sha256(tp_.read_bytes()).hexdigest()[:16], root_body=t_sha)
    print(f"\nBRAMBLESNARE -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print(f"  Tendril's voices from {tp_.name} {rec['tendril']['sha']}: its root's body {t_sha}, "
          f"{len(t_body)} bytes -- the snare's, transcribed (byte-identical to this file's copy)")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    sizes = {}

    def wav(name, x):
        sizes[name] = write_wav(out / name, x)

    peer_sfx = []
    for pf in a.peer_rows:
        prow = json.loads(pathlib.Path(pf).read_text(encoding="utf-8"))
        prow = prow["rows"] if isinstance(prow, dict) else prow
        peer_sfx.append((pf, prow))

    e2e_ref = {}
    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        W_ = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape, w.dmg, w.ult && w.ult.kind, "
                           "w.ult && w.ult.patchLife, w.ult && w.ult.rootFor, w.ult && w.ult.tickCd])")
        ids = [w_[0] for w_ in W_]
        if ME not in ids:
            raise SystemExit("no thornwake in this build")
        me = [w_ for w_ in W_ if w_[0] == ME][0]
        if abs(me[3] - BLADE) > 1e-9 or me[4] != "bramble" or me[5] != 6 or me[6] != 0.6 or me[7] != 0.5:
            raise SystemExit(f"Thornwake is {me} -- this lab levels against blade {BLADE} and the v84 bramble")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        if play_src.count(OLD_ARM) != 1:
            raise SystemExit("the old thornwake arm is not in play() exactly once")
        RC_ANCHOR = '        } else {                                        // rune-crack'
        if play_src.count(RC_ANCHOR) != 1:
            raise SystemExit("the rune-crack fallback is not in play() exactly once")
        if '"bindweed-root"' in play_src:
            print("  NOTE: this page already carries Tendril's voices; the references are still read from "
                  f"{tp_.name}")
        trows = [as_replace(RC_ANCHOR, "before", t_arms)]

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

        def play(kind, p, seed=None, rows=None):
            if rows:
                return R([["arm", T0, kind, p]], seed=seed, rows=rows, new=False)[0]
            return R([["play", T0, kind, p]], seed=seed, new=False)[0]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, (kind, p) in [("rune-crack", ("ult", {"w": FALLBACK})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                (f"hit@{BLADE:g}", ("hit", {"dmg": BLADE, "crit": False})),
                                ("wall", ("wall", {})), ("death", ("death", {})), ("OLD", ("ult", {"w": ME}))]:
            x = play(kind, p)
            ctl[name] = dict(basic(x), x=x)
            M = ctl[name]
            print(f"  {name:<14} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
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
        fall_ids = [w_ for w_ in ids if float(np.abs(play("ult", {"w": w_}) - rcx).max()) <= 1e-6]
        print(f"  rune-crack today (max |diff| <= 1e-6 vs ult/{FALLBACK}), {len(fall_ids)} relics: "
              + ", ".join(fall_ids))
        if ME in fall_ids:
            raise SystemExit("Thornwake's cast is rune-crack today -- this lab replaces its own arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_[0] for w_ in W_ if w_[1] == SCHOOL_AFF and w_[0] not in fall_ids and w_[0] != ME]
        types = [w_[0] for w_ in W_ if w_[2] == TYPE_SHAPE and w_[0] not in fall_ids and w_[0] != ME]
        print(f"  the verdant casts with their own voice: {', '.join(school) or '-'};  the scythe casts': "
              f"{', '.join(types) or '-'}")
        # the snare's source, rendered through THIS page's play() with Tendril's arms added
        xt = play("ult", {"w": "bindweed-root"}, rows=trows)
        if float(np.abs(xt - rcx).max()) <= 1e-6:
            raise SystemExit("Tendril's root renders as rune-crack -- its arms did not apply")

        # the noise draws of every reference
        REFS = {"hit": ("hit", {"dmg": BLADE, "crit": False}, None), "wall": ("wall", {}, None),
                "rune-crack": ("ult", {"w": FALLBACK}, None), "death": ("death", {}, None),
                "BAR": ("ult", {"w": "axiom"}, None), "hex-snap": ("hex-snap", {}, None),
                "fork": ("fork", {}, None), "vine plant": ("vine", {"plant": True}, None),
                "spark burn": ("spark", {}, None), "scour tick": ("scour-tick", {}, None),
                "scour woosh": ("scour-woosh", {"n": 1}, None), "clank": ("clank", {"mass": 1.1}, None),
                "OLD": ("ult", {"w": ME}, None),
                "T:cast": ("ult", {"w": "bindweed"}, trows), "T:bite2": ("ult", {"w": "bindweed-bite", "n": 2}, trows),
                "T:bite4": ("ult", {"w": "bindweed-bite", "n": 4}, trows),
                "T:root": ("ult", {"w": "bindweed-root"}, trows), "T:wither": ("ult", {"w": "bindweed-wither"}, trows)}
        for w_ in school + types:
            REFS[w_] = ("ult", {"w": w_}, None)
        RD_ = {k: [] for k in REFS}
        RX = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (kind, p, rw) in REFS.items():
                x = play(kind, p, seed=sd, rows=rw)
                RX[k].append(x)
                RD_[k].append(basic(x))
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD_.items()}
        # the school's voices on the batch line (Heartwood's), from their own rows
        peer_regs, peer_names = [], []
        for pf, prow in peer_sfx:
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            for w_ in sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _a, c in ps)))):
                base_ = w_.split("-")[0]
                if base_ in PEER_SCHOOL:
                    RB["peer:" + w_] = [bands(R([["arm", T0, "ult", {"w": w_}]], rows=ps, new=False)[0][int(T0 * SR):])]
                    peer_regs.append("peer:" + w_)
                    if peer_name(pf) not in peer_names:
                        peer_names.append(peer_name(pf))
        h_lo, h_hi = min(m_["top"] for m_ in RD_["hit"]), max(m_["top"] for m_ in RD_["hit"])
        w_hi = max(m_["top"] for m_ in RD_["wall"])
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD_['hit']):.3f}-{max(m_['peak'] for m_ in RD_['hit']):.3f};  the wall "
              f"tick: {min(m_['top'] for m_ in RD_['wall']):.4f}-{w_hi:.4f}")
        if peer_regs:
            print(f"  the school's voices on the batch line, from --peer-rows: {', '.join(peer_regs)}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        p90 = bed_p90(bed[int(2 * SR):int(10 * SR)])
        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi)
        wav("thornwake-ctl-runecrack.wav", rcx)
        wav(f"thornwake-ctl-hit{BLADE:g}.wav", ctl[f"hit@{BLADE:g}"]["x"])
        wav("thornwake-ctl-old-cast.wav", ctl["OLD"]["x"])
        wav("thornwake-ctl-tendril-root.wav", xt)

        # ---- THE SNARE: Tendril's root, transcribed ----------------------------
        print("\nSNARE -- 'a short creak and crack (Tendril's root voice, reused)'. Its body is Tendril's root "
              "arm's, transcribed; rendered here from this file's text and against Tendril's own arm (applied "
              "to this page's play() from its link's text) on every noise draw")
        snd = [R([["body", T0, TENDRIL_ROOT, {}]], seed=sd)[0] for sd in NOISE_SEEDS]
        same_t = max(float(np.abs(d_ - RX["T:root"][i]).max()) for i, d_ in enumerate(snd))
        off_t = max(float(np.abs(R([["body", T0, SNARE_OFF, {}]], seed=sd)[0] - RX["T:root"][i]).max())
                    for i, sd in enumerate(NOISE_SEEDS[:2]))
        xs, cs_ = R([["body", T0, TENDRIL_ROOT, {}]])
        Sn = basic(xs); Sn.update(x=xs, name="SNARE", calls=cs_[0])
        Sn["aud_lo"] = min(basic(d_)["aud"] for d_ in snd); Sn["aud_hi"] = max(basic(d_)["aud"] for d_ in snd)
        Sn["low"] = min(low_share(d_) for d_ in snd)
        Sn["crack_at"], Sn["stand"], Sn["jump"] = crack_info(xs, Sn["a0"])
        Sn["heard"], Sn["heard_fc"] = heard_at(xs, p90, 0.0)
        Sn["DB"] = [bands(d_[int(T0 * SR):]) for d_ in snd]
        SN_REGS = ["hit", "wall", "rune-crack", "death", "OLD", "T:cast", "T:bite4", "T:wither"] + school + types
        Sn["regs"] = {k: mreg(Sn["DB"], RB[k]) for k in SN_REGS}
        print(f"  the snare vs Tendril's root, max |diff| over {len(NOISE_SEEDS)} draws: {same_t:.1e} "
              f"({'the same voice' if same_t <= TOL else 'NOT THE SAME'});  the OFF control (g 0.518): "
              f"{off_t:.1e} ({'differs, as it must' if off_t > TOL else 'IT MATCHED: the check is blind'})")
        if same_t > TOL:
            FAILED.append("the snare is not Tendril's root")
        if off_t <= TOL:
            FAILED.append("snare off control")
        r_ = Sn["regs"]
        print(f"  audible {Sn['aud_lo']:.0f}-{Sn['aud_hi']:.0f} ms, loudest 50 ms {Sn['top']:.4f} = "
              f"{db(Sn['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g} (quietest draw), {db(Sn['top'] / w_hi):+.1f} "
              f"dB re the wall; LOW {Sn['low']:.2f} (worst draw); the crack at {Sn['crack_at']:.0f} ms standing "
              f"{Sn['stand']:+.1f} dB; heard {Sn['heard']:+.1f} dB @ {Sn['heard_fc']:.0f} Hz; {Sn['calls']} synth "
              f"calls; register at most {max(r_.values()):.2f} ({max(r_, key=r_.get)}) -- printed, not gated "
              f"(the design's own voice)")
        wav("thornwake-snare.wav", xs)
        rec["snare"] = dict(same=same_t, off=off_t, aud=[Sn["aud_lo"], Sn["aud_hi"]], top=Sn["top"],
                            db_hit=db(Sn["top"] / h_lo), low=Sn["low"], crack_at=Sn["crack_at"], stand=Sn["stand"],
                            heard=Sn["heard"], calls=Sn["calls"], regs=Sn["regs"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a rustle-and-creak, 0.4s'. Level-matched: the creak alone {CREAK_UNDER_DB:g} dB under the "
              f"rustle alone, AUDIBLE {CAST_AUD:g} ms, TOP {tgt_c:.4f} (the centre of {lev_c['lo']:.4f}-"
              f"{lev_c['hi']:.4f})")

        def cx(sp, g, kc, L, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kc, L, part), {}]], seed=seed)

        def calib_cast(sp):
            g, kc, L = 0.1, 0.5, 0.4
            for _ in range(6):
                B = basic(cx(sp, g, kc, L)[0])
                L = round(min(0.6, max(0.25, L + (CAST_AUD - B["aud"]) / 1000)), 4)
                tr = basic(cx(sp, g, kc, L, "rustle")[0])["top"]
                tc = basic(cx(sp, g, kc, L, "creak")[0])["top"]
                kc = sig4(kc * 10 ** ((-CREAK_UNDER_DB - db(tc / tr)) / 20))
                g = sig4(g * tgt_c / basic(cx(sp, g, kc, L)[0])["top"])
            return g, kc, L

        CAST_REGS = (["rune-crack", "hit", "death", "BAR", "hex-snap", "fork", "scour woosh", "T:cast", "T:root",
                      "T:wither"] + school + types + peer_regs)

        def cast_measure(name, sp, g, kc, L):
            x, calls = cx(sp, g, kc, L)
            draws = [cx(sp, g, kc, L, seed=sd)[0] for sd in NOISE_SEEDS]
            M = basic(x); M.update(x=x, calls=calls[0], name=name, sp=sp, g=g, kc=kc, L=L)
            Bd = [basic(d_) for d_ in draws]
            M["aud_lo"] = min(b_["aud"] for b_ in Bd); M["aud_hi"] = max(b_["aud"] for b_ in Bd)
            M["gone_hi"] = max(b_["gone"] for b_ in Bd)
            M["top_lo"] = min(b_["top"] for b_ in Bd); M["top_hi"] = max(b_["top"] for b_ in Bd)
            a_, b_ = 0.02, L - 0.03
            M["r_none"], M["c_none"] = not sp["rustle"], not sp["creak"]
            xr = xc = None
            if sp["rustle"]:
                rd = [cx(sp, g, kc, L, "rustle", seed=sd)[0] for sd in NOISE_SEEDS]
                xr = cx(sp, g, kc, L, "rustle")[0]
                M["r_tonal"] = tonal(rd, T0 + a_, T0 + b_, 300, 8000)
                cs2 = [cen(d_, 0.0, L) for d_ in rd]
                M["r_cen0"], M["r_cen1"] = min(cs2), max(cs2)
                M["r_rise"] = min(basic(d_)["rise"] for d_ in rd)
                M["r_top"] = basic(xr)["top"]
            if sp["creak"]:
                xc = cx(sp, g, kc, L, "creak")[0]
                M["c_rate"] = mod_rate(xc, a_ + 0.01, b_)
                M["c_pulsed"], _r, M["c_depth"] = pulsed_w(xc, a_, b_, win=0.1)
                M["c_top"] = basic(xc)["top"]
            if xr is not None and xc is not None:
                M["c_db"] = db(M["c_top"] / M["r_top"])
                M["r_own"], M["r_own_fc"] = own(xr, xc, a_, b_)
                M["c_own"], M["c_own_fc"] = own(xc, xr, a_, b_)
            for k in ("r_tonal", "r_cen0", "r_cen1", "r_rise", "c_rate", "c_pulsed", "c_depth", "c_db", "r_own",
                      "c_own"):
                M.setdefault(k, float("nan"))
            M["heard"], M["heard_fc"] = min((heard_at(d_, p90, 0.0) for d_ in draws), key=lambda z: z[0])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CAST_REGS}
            M["regs"]["snare"] = mreg(DB, Sn["DB"])
            M["reg_old"] = mreg(DB, RB["OLD"])
            return M

        def f_(v, spec):
            return format(v, spec) if v == v else "  -"

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['kc']:>8.4g}{M['L']:>7.3f}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{M['aud_lo']:>5.0f}{M['aud_hi']:>5.0f}{M['gone_hi']:>5.0f}{f_(M['r_tonal'], '>6.1f')}"
                  f"{f_(M['r_cen0'], '>6.0f')}{f_(M['r_cen1'], '>6.0f')}{f_(M['r_rise'], '>5.0f')}"
                  f"{f_(M['c_rate'], '>6.0f')}{f_(M['c_pulsed'], '>6.2f')}{f_(M['c_db'], '>6.1f')}"
                  f"{f_(M['r_own'], '>6.1f')}{f_(M['c_own'], '>6.1f')}{M['heard']:>6.1f}"
                  f"  {top2(r_)}; old {M['reg_old']:.2f}")

        print(f"  {'cand':<10}{'g':>8}{'kc':>8}{'L':>7}{'calls':>6}{'top':>8}{'audL':>5}{'audH':>5}{'gone':>5}"
              f"{'rTon':>6}{'rCen0':>6}{'rCen1':>6}{'rRis':>5}{'cRate':>6}{'cPul':>6}{'cdB':>6}{'rOwn':>6}{'cOwn':>6}"
              f"{'hrd':>6}{'reg':>6}")
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g, kc, L = calib_cast(sp)
            x1, _ = cx(sp, g, kc, L); x2, _ = cx(sp, g, kc, L)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"cast {name} does not reproduce")
            M = cast_measure(name, sp, g, kc, L); M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"thornwake-cast-{_slug(name)}.wav", M["x"])
        c0 = rows_c[0]
        ctlc = []
        for cname, sp, _b in CAST_CONTROLS:
            M = cast_measure(cname, sp, c0["g"], c0["kc"], c0["L"]); ctlc.append(M)
            wav(f"thornwake-cast-{_slug(cname)}.wav", M["x"])
        for M in ctlc:
            M["why"] = cast_why(M, lev_c); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES + CAST_CONTROLS:
            print(f"    {name:<10} {blurb}")
        _show(rows_c, ctlc, CAST_RULE, "cast")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        Ca = rows_c[ci]
        print(f"  PICK  {Ca['name']}  g {Ca['g']}, kc {Ca['kc']}, L {Ca['L']}, {Ca['calls']} synth calls; TOP "
              f"{Ca['top']:.4f} = {db(Ca['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g} (quietest draw)")

        # ---- THE BITE ------------------------------------------------------
        lev_s = dict(lo=2.0 * w_hi, hi=0.5 * h_lo)
        tgt_s = math.sqrt(lev_s["lo"] * lev_s["hi"])
        print(f"\nBITE -- 'a soft snap'. Level-matched: AUDIBLE {BITE_AUD:g} ms, TOP {tgt_s:.4f} (the centre of "
              f"{lev_s['lo']:.4f}-{lev_s['hi']:.4f}: 2x the wall tick, 0.5x the blow)")

        def bx(sp, g, D, seed=None):
            return R([["body", T0, bite_body(sp, g, D), {}]], seed=seed)

        def calib_bite(sp):
            g, D = 0.1, 0.06
            for _ in range(6):
                B = basic(bx(sp, g, D)[0])
                D = round(min(0.3, max(0.02, D * BITE_AUD / max(B["aud"], 1.0))), 4)
                g = sig4(g * tgt_s / basic(bx(sp, g, D)[0])["top"])
            return g, D

        BITE_REGS = ["hit", "wall", "fork", "hex-snap", "vine plant", "T:bite2", "T:bite4", "rune-crack"]

        def bite_measure(name, sp, g, D):
            x, calls = bx(sp, g, D)
            draws = [bx(sp, g, D, seed=sd)[0] for sd in NOISE_SEEDS]
            M = basic(x); M.update(x=x, calls=calls[0], name=name, sp=sp, g=g, D=D)
            Bd = [basic(d_) for d_ in draws]
            M["aud_lo"] = min(b_["aud"] for b_ in Bd); M["aud_hi"] = max(b_["aud"] for b_ in Bd)
            M["gone_hi"] = max(b_["gone"] for b_ in Bd)
            M["rise"] = max(b_["rise"] for b_ in Bd); M["pk_ms"] = max(b_["pk_ms"] for b_ in Bd)
            M["top_lo"] = min(b_["top"] for b_ in Bd); M["top_hi"] = max(b_["top"] for b_ in Bd)
            M["cen_hi"] = max(cen(d_, 0.0, 0.01) for d_ in draws)   # round 2: the SNAP's (first 10 ms)
            M["re"] = sum(reattack(d_) is not None for d_ in draws)
            M["heard"], M["heard_fc"] = min((heard_at(d_, p90, 0.0) for d_ in draws), key=lambda z: z[0])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in BITE_REGS}
            M["regs"]["cast"] = mreg(DB, Ca["DB"])
            M["regs"]["snare"] = mreg(DB, Sn["DB"])
            return M

        def bite_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['D']:>7.4g}{M['calls']:>6d}{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}"
                  f"{M['aud_lo']:>5.0f}{M['aud_hi']:>5.0f}{M['gone_hi']:>5.0f}{M['rise']:>4.0f}{M['pk_ms']:>4.0f}"
                  f"{M['re']:>3d}{M['cen_hi']:>7.0f}{M['heard']:>6.1f}  {top2(r_)}")

        print("  the house's snaps, the same reading (the centroid of the first 10 ms, the highest of 12 draws): " +
              ", ".join(f"{k} {max(cen(d_, 0.0, 0.01) for d_ in RX[k]):.0f} Hz"
                        for k in ("T:bite2", "T:bite4", "hex-snap", "fork", "vine plant")))
        print(f"  {'cand':<10}{'g':>8}{'D':>7}{'calls':>6}{'topL':>8}{'topH':>8}{'audL':>5}{'audH':>5}{'gone':>5}"
              f"{'rs':>4}{'pk':>4}{'re':>3}{'snpC':>7}{'hrd':>6}{'reg':>6}")
        rows_b = []
        for name, sp, _b in BITE_CANDIDATES:
            g, D = calib_bite(sp)
            x1, _ = bx(sp, g, D); x2, _ = bx(sp, g, D)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"bite {name} does not reproduce")
            M = bite_measure(name, sp, g, D); M["why"] = bite_why(M, lev_s)
            rows_b.append(M); bite_line(M)
            wav(f"thornwake-bite-{_slug(name)}.wav", M["x"])
        b0 = rows_b[0]
        ctlb = []
        for cname, sp, _b in BITE_CONTROLS:
            M = bite_measure(cname, sp, b0["g"], b0["D"]); ctlb.append(M)
        for M in ctlb:
            M["why"] = bite_why(M, lev_s); bite_line(M)
        for (name, _sp, blurb) in BITE_CANDIDATES + BITE_CONTROLS:
            print(f"    {name:<10} {blurb}")
        _show(rows_b, ctlb, BITE_RULE, "bite")
        ok, fb = _gate(rows_b, "bite")
        bi = fb if ok is None else min(ok, key=lambda i: (round(max(rows_b[i]["regs"].values()) / 0.05),
                                                          rows_b[i]["calls"], i))
        Bi = rows_b[bi]
        print(f"  PICK  {Bi['name']}  g {Bi['g']}, D {Bi['D']}, {Bi['calls']} synth calls; loudest 50 ms "
              f"{db(Bi['top'] / h_lo):+.1f} dB re the blow, {db(Bi['top'] / w_hi):+.1f} dB re the wall")

        # ---- THE CRACKLE ---------------------------------------------------
        print(f"\nCRACKLE -- 'a bramble opening -- a dry crackle'. Level-matched: AUDIBLE {CRACK_AUD:g} ms (the "
              f"bramble's 0.3 s growth), TOP {tgt_s:.4f} (the centre of {lev_s['lo']:.4f}-{lev_s['hi']:.4f})")

        def rx(sp, g, S, seed=None):
            return R([["body", T0, crackle_body(sp, g, S), {}]], seed=seed)

        def calib_crackle(sp):
            g, S = 0.1, 0.28
            for _ in range(6):
                B = basic(rx(sp, g, S)[0])
                S = round(min(0.5, max(0.1, S + (CRACK_AUD - B["aud"]) / 1000)), 4)
                g = sig4(g * tgt_s / basic(rx(sp, g, S)[0])["top"])
            return g, S

        CRK_REGS = ["hit", "wall", "rune-crack", "fork", "hex-snap", "vine plant", "spark burn", "scour tick",
                    "T:bite4", "T:wither"]

        def crackle_measure(name, sp, g, S):
            x, calls = rx(sp, g, S)
            draws = [rx(sp, g, S, seed=sd)[0] for sd in NOISE_SEEDS]
            M = basic(x); M.update(x=x, calls=calls[0], name=name, sp=sp, g=g, S=S)
            Bd = [basic(d_) for d_ in draws]
            M["aud_lo"] = min(b_["aud"] for b_ in Bd); M["aud_hi"] = max(b_["aud"] for b_ in Bd)
            M["gone_hi"] = max(b_["gone"] for b_ in Bd)
            M["top_lo"] = min(b_["top"] for b_ in Bd); M["top_hi"] = max(b_["top"] for b_ in Bd)
            ci_ = [clicks(d_, 0.0, S + 0.01) for d_ in draws]
            M["clicks"] = min(c_[0] for c_ in ci_); M["irreg"] = min(c_[1] for c_ in ci_)
            M["depth"] = min(depth(d_, 0.005, max(0.02, S - 0.005)) for d_ in draws)
            M["low"] = max(low_share(d_) for d_ in draws)
            M["b500"] = max(low_share(d_, 500.0) for d_ in draws)
            M["tonal"] = tonal(draws, T0, T0 + S + 0.01, 1000, 12000)
            M["heard"], M["heard_fc"] = min((heard_at(d_, p90, 0.1) for d_ in draws), key=lambda z: z[0])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CRK_REGS}
            M["regs"]["cast"] = mreg(DB, Ca["DB"])
            M["regs"]["bite"] = mreg(DB, Bi["DB"])
            M["regs"]["snare"] = mreg(DB, Sn["DB"])
            return M

        def crackle_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['S']:>7.4g}{M['calls']:>6d}{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}"
                  f"{M['aud_lo']:>5.0f}{M['aud_hi']:>5.0f}{M['gone_hi']:>5.0f}{M['clicks']:>5d}{M['irreg']:>6.2f}"
                  f"{M['depth']:>6.1f}{M['low']:>7.3f}{M['b500']:>7.3f}{M['tonal']:>6.1f}{M['heard']:>6.1f}"
                  f"  {top2(r_)}")

        print(f"  {'cand':<10}{'g':>8}{'S':>7}{'calls':>6}{'topL':>8}{'topH':>8}{'audL':>5}{'audH':>5}{'gone':>5}"
              f"{'clk':>5}{'irr':>6}{'dep':>6}{'low':>7}{'b500':>7}{'ton':>6}{'hrd':>6}{'reg':>6}")
        rows_r = []
        for name, sp, _b in CRACKLE_CANDIDATES:
            g, S = calib_crackle(sp)
            x1, _ = rx(sp, g, S); x2, _ = rx(sp, g, S)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"crackle {name} does not reproduce")
            M = crackle_measure(name, sp, g, S); M["why"] = crackle_why(M, lev_s)
            rows_r.append(M); crackle_line(M)
            wav(f"thornwake-crackle-{_slug(name)}.wav", M["x"])
        r0 = rows_r[0]
        ctlr = []
        for cname, sp, _b in CRACKLE_CONTROLS:
            M = crackle_measure(cname, sp, r0["g"], r0["S"]); ctlr.append(M)
        for M in ctlr:
            M["why"] = crackle_why(M, lev_s); crackle_line(M)
        for (name, _sp, blurb) in CRACKLE_CANDIDATES + CRACKLE_CONTROLS:
            print(f"    {name:<10} {blurb}")
        _show(rows_r, ctlr, CRACKLE_RULE, "crackle")
        ok, fb = _gate(rows_r, "crackle")
        ri = fb if ok is None else min(ok, key=lambda i: (round(max(rows_r[i]["regs"].values()) / 0.05),
                                                          rows_r[i]["calls"], i))
        Cr = rows_r[ri]
        print(f"  PICK  {Cr['name']}  g {Cr['g']}, S {Cr['S']}, {Cr['calls']} synth calls; loudest 50 ms "
              f"{db(Cr['top'] / h_lo):+.1f} dB re the blow, {db(Cr['top'] / w_hi):+.1f} dB re the wall")

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        c_what = {"leaves": "Leaves: 30 ms bandpass grains ~60 a second, their centres wandering 820-2380 Hz, "
                            "swelling to the middle and falling away; under them",
                  "brush": "Brush: two overlapping bandpass sweeps, 600 -> 1800 Hz and back 1800 -> 900; under "
                           "them",
                  "briar": "Thorns: bandpass grains ~60 a second, centres wandering 1730-3900 Hz, swelling to the "
                           "middle; under them",
                  "thorns": "Thorns: narrow bandpass grains (Q 5) ~60 a second, 30 ms each, their centres wandering "
                            "2460-4160 Hz, swelling to the middle and falling away; under them",
                  "burrs": "Burrs: bandpass grains (Q 4) ~60 a second, 30 ms each, their centres wandering "
                           "2140-4200 Hz, swelling to the middle and falling away; under them",
                  "spines": "Spines: narrow bandpass grains (Q 6) ~60 a second, 30 ms each, their centres "
                            "wandering 2310-3900 Hz, swelling to the middle and falling away; under them",
                  "needles": "Needles: narrow bandpass grains (Q 8) ~60 a second, 30 ms each, their centres "
                             "wandering 2310-3900 Hz, swelling to the middle and falling away; under them"}[
            Ca["sp"]["rustle"]] + \
            {"timber": " a 330 Hz timber (a sine and its 2.76 mode at 0.4) pulsed slowing 45 -> 28 a second, each "
                       "interval x (1 + 0.12 sin 2.4k) -- a bough bending (a held note does not exist in this "
                       "toolkit, and a creak is stick-slip).",
             "bough": " a heavier bough, a 165 Hz triangle and its 2.76 mode at 0.4, pulsed slowing 45 -> 28 a "
                      "second, each interval x (1 + 0.12 sin 2.4k) (a creak is stick-slip)."}[Ca["sp"]["creak"]]
        r_what = {"snaps": "5 ms highpass clicks (2.5 kHz) ~33 a second, each interval x (1 + 0.45 sin 2.4k), "
                           "thinning as it goes.",
                  "open": "5 ms highpass clicks (2.5 kHz) quickening 22 -> 50 a second and growing as the bramble "
                          "grows out, each interval x (1 + 0.45 sin 2.4k).",
                  "twigs": "6 ms bandpass clicks (Q 3) at centres wandering 1.6-4.5 kHz, ~33 a second, each "
                           "interval x (1 + 0.45 sin 2.4k): twigs of different sizes.",
                  "embers": "5 ms highpass pops ~24 a second, every other one with a smaller pop 8 ms after it (a "
                            "fire's crackle), each interval x (1 + 0.45 sin 2.4k).",
                  "knots": "8 ms narrow bandpass clicks (Q 6) ~33 a second at centres wandering 1185-2160 Hz -- "
                           "knots in dry wood -- each interval x (1 + 0.45 sin 2.4k), thinning as it goes.",
                  "splinters": "8 ms narrow bandpass clicks (Q 8) ~33 a second at centres wandering 1480-2700 Hz "
                               "-- splinters -- each interval x (1 + 0.45 sin 2.4k), thinning as it goes."}[
            Cr["sp"]["kind"]]
        b_what = {"stem": "A 10 ms bandpass snap at 1.1 kHz over a sine falling 620 -> 420 Hz.",
                  "knot": "A 12 ms lowpass snap (1.8 kHz) over a triangle falling 440 -> 330 Hz.",
                  "prick": "A 6 ms bandpass snap at 1.6 kHz over a sine falling 1200 -> 900 Hz.",
                  "pad": "A 15 ms lowpass snap (900 Hz) over a sine falling 300 -> 220 Hz."}[Bi["sp"]["kind"]]
        info = dict(
            n_cast=len(CAST_CANDIDATES), n_crk=len(CRACKLE_CANDIDATES), n_bite=len(BITE_CANDIDATES),
            c_what=c_what, c_tonal=Ca["r_tonal"], c_cen0=Ca["r_cen0"], c_cen1=Ca["r_cen1"], c_rise=Ca["r_rise"],
            c_rate=Ca["c_rate"], c_pulsed=Ca["c_pulsed"], c_cdb=Ca["c_db"], c_rown=Ca["r_own"], c_cown=Ca["c_own"],
            c_aud=Ca["aud"], c_db=db(Ca["top"] / h_lo), c_reg=max(Ca["regs"].values()),
            c_regk=RNAME.get(max(Ca["regs"], key=Ca["regs"].get), max(Ca["regs"], key=Ca["regs"].get)),
            r_regk=RNAME.get(max(Cr["regs"], key=Cr["regs"].get), max(Cr["regs"], key=Cr["regs"].get)),
            b_regk=RNAME.get(max(Bi["regs"], key=Bi["regs"].get), max(Bi["regs"], key=Bi["regs"].get)),
            r_what=r_what, r_clicks=Cr["clicks"], r_irreg=Cr["irreg"], r_depth=Cr["depth"], r_b500=Cr["b500"],
            r_tonal=Cr["tonal"], r_aud=Cr["aud"], r_db=db(Cr["top"] / h_lo), r_heard=Cr["heard"],
            r_reg=max(Cr["regs"].values()),
            s_same=max(same_t, 1e-9), s_aud=Sn["aud"], s_db=db(Sn["top"] / h_lo), s_low=Sn["low"],
            b_what=b_what, b_rise=Bi["rise"], b_aud0=Bi["aud_lo"], b_aud1=Bi["aud_hi"], b_db=db(Bi["top"] / h_lo),
            b_wdb=db(Bi["top"] / w_hi), b_cen=Bi["cen_hi"], b_reg=max(Bi["regs"].values()))
        arms = arms_code(Ca, Cr, Bi, info)
        _refuse(re.sub(r"/\*.*?\*/", "", arms, flags=re.S), "Sfx row")
        if not arms.isascii():
            raise SystemExit("the Sfx row is not ASCII")
        if OLD_ARM in arms or arms.endswith("\n"):
            raise SystemExit("the Sfx row must replace its anchor and end where the old arm ended")
        sfx_rows = [as_replace(OLD_ARM, "replace", arms)]
        print("\nTHE SFX ROW (mode `replace`: the old arm's four lines -> four arms), applied to "
              "Sfx.prototype.play's own source and rendered:")
        NEWP = [("cast", {"w": ME}, cast_body(Ca["sp"], Ca["g"], Ca["kc"], Ca["L"])),
                ("crackle", {"w": ME + "-crackle"}, crackle_body(Cr["sp"], Cr["g"], Cr["S"])),
                ("snare", {"w": ME + "-snare"}, TENDRIL_ROOT),
                ("bite", {"w": ME + "-bite"}, bite_body(Bi["sp"], Bi["g"], Bi["D"]))]
        chk = []
        for sd in (None, NOISE_SEEDS[3]):
            dr = "" if sd is None else " draw"
            for lab_, p_, body in NEWP:
                x1, _ = R([["arm", T0, "ult", p_]], rows=sfx_rows, seed=sd)
                x2, _ = R([["body", T0, body, {}]], seed=sd)
                chk.append((lab_ + dr, float(np.abs(x1 - x2).max())))
                if lab_ == "cast" and sd is None:
                    xa0 = x1
                if lab_ == "snare":
                    chk.append(("snare vs Tendril's root" + dr,
                                float(np.abs(x1 - play("ult", {"w": "bindweed-root"}, seed=sd, rows=trows)).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 12.5, 18, BLADE, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": n_}) for n_ in range(0, 7)]
        others += [("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 1.1}), ("clank", {"mass": 5}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("fork", {}), ("vine", {}), ("vine", {"plant": True}),
                   ("vine", {"coil": True}), ("vine", {"miss": True}), ("loose", {}), ("loose", {"bal": True}),
                   ("loose", {"leaf": True}), ("aegis", {"n": 3, "back": 5}), ("aegis", {"broke": True}),
                   ("scour-hold", {"n": 5}), ("scour-tick", {}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = sorted(set(re.findall(r'w === "([a-z-]+)"', play_src)) | set(ids) | {FALLBACK})
        ult_ids = [w_ for w_ in ult_ids if w_ != ME and not w_.startswith(ME + "-")]
        others += [("ult", {"w": w_, "n": 2}) for w_ in ult_ids]
        kinds_ = sorted(set(re.findall(r'kind === "([a-z-]+)"', play_src)) - {"ult", "hit"})
        others += [(k_, {}) for k_ in kinds_ if (k_, {}) not in others]
        e2e_voices = others
        same_ = []
        for kind, p in others:
            x1 = play(kind, p); x2, _ = R([["arm", T0, kind, p]], rows=sfx_rows, new=False)
            same_.append((kind + "/" + str(p.get("w", p.get("dmg", p.get("n", "")))) + ("!" if p.get("crit") else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 "
              f"weights x crit, the heal chime at n 0-6, spark arm and burn, wall, death, clank x2, seal, nova, "
              f"hex-snap, fork, vine x4, loose x3, aegis x2, scour x4, {len(ult_ids)} ult ids -- every other relic's "
              f"cast, every sub-voice the ult arm names and the bare fallback -- and every kind play() names): worst "
              f"max |diff| {worst[1]:.0e} ({worst[0]})")
        now_old = float(np.abs(xa0 - ctl["OLD"]["x"]).max())
        fb_rc = float(np.abs(R([["arm", T0, "ult", {"w": FALLBACK}]], rows=sfx_rows, new=False)[0] - rcx).max())
        print(f"  ult/thornwake vs the old arm after the row: max |diff| {now_old:.3f} -- "
              f"{'no longer the creak and cinch' if now_old > 1e-3 else 'STILL THE OLD ARM'};  ult/{FALLBACK} after "
              f"the row: {fb_rc:.0e} -- {'still rune-crack' if fb_rc <= 1e-6 else 'CHANGED'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_old <= 1e-3 or fb_rc > 1e-6 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40, ME, BLADE])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_old=now_old, fallback=fb_rc, cost=cost, n_others=len(same_))

        # ---- WITH OTHER RELICS' ROWS ------------------------------------------
        peers = []
        for pf, prow in peer_sfx:
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            if not ps:
                print(f"  peer {pf}: no row anchored in play() -- skipped")
                continue
            pids = sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _, c in ps))))
            pk_ = sorted(set(re.findall(r'kind === "([a-z-]+)"', "".join(c for _, c in ps))))
            A_ = sfx_rows + ps; B_ = ps + sfx_rows
            mine = [("ult", {"w": ME}), ("ult", {"w": ME + "-crackle"}), ("ult", {"w": ME + "-snare"}),
                    ("ult", {"w": ME + "-bite"})]
            evs = mine + [("ult", {"w": w_, "n": 3, "k": 1, "shield": 45}) for w_ in pids] + [(k_, {}) for k_ in pk_]
            dmax, dmine = 0.0, 0.0
            PX = {}
            for kind_, p_ in evs:
                xa_, _ = R([["arm", T0, kind_, p_]], rows=A_, new=False)
                xb_, _ = R([["arm", T0, kind_, p_]], rows=B_, new=False)
                dmax = max(dmax, float(np.abs(xa_ - xb_).max()))
                if str(p_.get("w", "")).startswith(ME):
                    xs_, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows, new=False)
                    dmine = max(dmine, float(np.abs(xa_ - xs_).max()))
                else:
                    PX[(kind_, p_.get("w", kind_))] = xa_
            prg = {}
            for (kind_, w_), xp in PX.items():
                bp = bands(xp[int(T0 * SR):])
                prg[w_] = {nm: cos(bands(X_["x"][int(T0 * SR):]), bp)
                           for nm, X_ in (("cast", Ca), ("crackle", Cr), ("snare", Sn), ("bite", Bi))}
            worst_p = max(((max(v.values()), k + "/" + max(v, key=v.get)) for k, v in prg.items()),
                          default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders "
                  f"render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the four against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) -- printed")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=prg))
        rec["peers"] = peers

        # ---- THE plantBramble AND tickBramble ROWS -----------------------------
        srows = {"plant": [as_replace(CRACKLE_ANCHOR, "after", CRACKLE_CODE)],
                 "tick": [as_replace(SNARE_ANCHOR, "after", SNARE_CODE), as_replace(BITE_ANCHOR, "after", BITE_CODE)]}
        srows_bad = {"plant": srows["plant"],
                     "tick": [as_replace(SNARE_ANCHOR, "after", SNARE_CODE),
                              as_replace(BITE_ANCHOR, "after", BITE_CODE_BAD)]}
        seeds = [a.seed0 + k for k in range(a.seeds)]
        WR = None
        if not a.no_wire:
            print("\nTHE plantBramble AND tickBramble ROWS, applied to the prototypes' own sources, run beside the "
                  "originals on real fights:")
            WR = page.evaluate(WIRE_JS, [seeds, srows, ME])
            assert not errors, errors[:3]
            if "err" in WR:
                raise SystemExit(WR["err"])
            T_ = WR["tot"]
            print(f"  {WR['fights']} fights (Thornwake both sides x every foe x seeds {seeds}): {WR['same']}/"
                  f"{WR['fights']} identical (over, clock, both fighters' hp, positions, velocities, charges, facing, "
                  f"pins, entangle, the thorns' cooldown and inside flag, the window's clock, the winner, both "
                  f"brambleTallies, every bramble and the brambles' clock, and a digest of every step); every other "
                  f"SFX call identical in order and opts in {WR['otherSame']}/{WR['fights']}")
            print(f"  {T_['casts']} casts -> {T_['castV']} cast voices; {T_['planted']} brambles planted -> "
                  f"{T_['crackV']} crackles; {T_['snares']} snares -> {T_['snareV']} snare voices; {T_['ticks']} "
                  f"bites -> {T_['biteV']} bite voices ({T_['kills']} killing bites, {T_['killBites']} of them "
                  f"voiced); a snare and a bite on one tickBramble {T_['together']} times, the snare first "
                  f"{T_['order']}; problems {WR['nbad']}")
            for b_ in WR["bad"]:
                print(f"    {b_}")
            if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                    or T_["castV"] != T_["casts"] or T_["crackV"] != T_["planted"] or T_["snareV"] != T_["snares"] \
                    or T_["biteV"] != T_["ticks"] or T_["killBites"] != T_["kills"] or T_["order"] != T_["together"] \
                    or min(T_["crackV"], T_["snareV"], T_["biteV"]) == 0:
                FAILED.append("plantBramble / tickBramble rows")
            WB = page.evaluate(WIRE_JS, [seeds, srows_bad, ME])
            assert not errors, errors[:3]
            print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a bite voice): "
                  f"{WB['same']}/{WB['fights']} identical -- "
                  f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
            if WB["same"] == WB["fights"]:
                FAILED.append("identity control")
            rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "nbad")}
            rec["wire"].update(T_)
            rec["wire"]["control_same"] = WB["same"]
            wins = WR["pick"]
            per = sorted(w_["bites"] for w_ in wins)
            rec["wire"]["per_cast"] = dict(n=len(wins), crackles=sum(w_["crackles"] for w_ in wins) / max(1, len(wins)),
                                           snares=sum(w_["snares"] for w_ in wins) / max(1, len(wins)),
                                           bites=sum(w_["bites"] for w_ in wins) / max(1, len(wins)))
            print(f"  per cast (the voices from one cast to the next, {len(wins)} casts): crackles "
                  f"{rec['wire']['per_cast']['crackles']:.2f}, snares {rec['wire']['per_cast']['snares']:.2f}, bites "
                  f"{rec['wire']['per_cast']['bites']:.2f} (median {per[len(per) // 2] if per else 0})")

            # ---- THE PICKS IN A REAL WINDOW ---------------------------------
            # v107's round-4c reading (aureole's and spellbreaker's, as a method):
            # per event, the third-octave (200 Hz-12 kHz) in which the voice
            # stands highest over everything else in THIS stretch of fight (the
            # score and the fight's own sounds). Gates: the cast (first 100 ms),
            # the crackles' median (100-300 ms, after the blow's body) and the
            # bites' median (first 60 ms) >= +3 dB; the snare -- the design's own
            # voice -- REPORTED. Controls: AFTER (the same reading 0.9 s after the
            # last new voice, none sounding: NOT heard) and LEVEL (every event
            # heard at >= +3 dB reads LOWER with its voice 20 dB under).
            cand = [w_ for w_ in wins if w_["crackles"] >= 1 and w_["snares"] >= 1 and w_["bites"] >= 3
                    and w_["next"] is not None and w_["next"] - w_["last"] >= 1.5]
            cand.sort(key=lambda w: (-w["bites"], w["foe"], w["seed"], w["cast"]))
            if cand:
                w_ = cand[len(cand) // 4]
                EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], srows, ME])
                assert not errors, errors[:3]
                c0t = w_["cast"]; lt = w_["last"]
                lo_t, hi_t = c0t - 1.0, min(lt + 2.2, w_["next"] - 0.01)
                evs = [e for e in EV if lo_t <= e[0] <= hi_t]
                allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
                secs = T0 + (hi_t - lo_t) + 1.0
                xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
                bd = bed[:len(xw)]
                if len(bd) < len(xw):
                    bd = np.concatenate([bd, np.zeros(len(xw) - len(bd))])
                xw = xw + bd
                BURY = 0.1

                def bury(body):
                    return re.sub(r"const g = ([0-9.e-]+)", lambda m_: f"const g = {fmt(round(float(m_.group(1)) * BURY, 7))}",
                                  body, count=1)
                bury_body = {ME: bury(cast_body(Ca["sp"], Ca["g"], Ca["kc"], Ca["L"])),
                             ME + "-crackle": bury(crackle_body(Cr["sp"], Cr["g"], Cr["S"])),
                             ME + "-snare": bury(TENDRIL_ROOT),
                             ME + "-bite": bury(bite_body(Bi["sp"], Bi["g"], Bi["D"]))}
                RWB = [fc_ for fc_ in BANDS if PHONE_HZ <= fc_ <= 12000.0]

                def over_at(xa, xb_, fc_, t_, w2):
                    return db(band_rms(xa, fc_, t_, t_ + w2) / max(band_rms(xb_, fc_, t_, t_ + w2), 1e-12))

                def best_band(xa, xb_, t_, w2):
                    return max((over_at(xa, xb_, fc_, t_, w2), fc_) for fc_ in RWB)
                READ = {ME: [(0.0, 0.1), (0.15, 0.1)], ME + "-crackle": [(0.1, 0.2)],
                        ME + "-snare": [(0.0, 0.1), (0.2, 0.1)], ME + "-bite": [(0.0, 0.06)]}
                GATED = {(ME, 0): "min", (ME + "-crackle", 0): "median", (ME + "-bite", 0): "median"}
                last_mine = max(e[0] for e in evs if e[3])
                res, res_b, res_a, level_ok = {}, {}, {}, {}
                for tag, reads in READ.items():
                    ts0 = [T0 + (e[0] - lo_t) for e in evs if e[3] == tag]
                    if not ts0:
                        for j_ in range(len(reads)):
                            res[(tag, j_)] = res_b[(tag, j_)] = res_a[(tag, j_)] = []
                        continue
                    xo = R([e_ for e_, e in zip(allv, evs) if e[3] != tag], secs=secs, rows=sfx_rows,
                           new=False)[0] + bd
                    xb = R([(["body", e_[1], bury_body[tag], {}] if e[3] == tag else e_)
                            for e_, e in zip(allv, evs)], secs=secs, rows=sfx_rows, new=False)[0] + bd
                    for j_, (off, win_) in enumerate(reads):
                        ts = [t_ + off for t_ in ts0]
                        bb = [best_band(xw, xo, t_, win_) for t_ in ts]
                        res[(tag, j_)] = [v_ for v_, _ in bb]
                        res[(tag, j_, "@")] = [fc_ for _, fc_ in bb]
                        t_after = T0 + (last_mine - lo_t) + 0.9
                        ta = [t_after + 0.05 * i_ for i_ in range(min(len(ts), 12))
                              if t_after + 0.05 * i_ + win_ <= T0 + (hi_t - lo_t)]
                        res_a[(tag, j_)] = [best_band(xw, xo, t_, win_)[0] for t_ in ta]
                        res_b[(tag, j_)] = [best_band(xb, xo, t_, win_)[0] for t_ in ts]
                        level_ok[(tag, j_)] = all(b_ < v_ for v_, b_ in zip(res[(tag, j_)], res_b[(tag, j_)])
                                                  if v_ >= 3)

                def gate_of(r, key):
                    if not r.get(key):
                        return None
                    v = r[key]
                    return (min(v) if GATED[key] == "min" else float(np.median(v))) >= 3
                G4 = {k: gate_of(res, k) for k in GATED}
                GA = {k: gate_of(res_a, k) for k in GATED}
                print(f"\nIN A REAL WINDOW -- thornwake v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                      f"{c0t:.2f}s, {w_['crackles']} crackles, {w_['snares']} snares and {w_['bites']} bites before "
                      f"the next cast at {w_['next']:.2f}s (read to {hi_t:.2f}s); the fight's own sounds and the "
                      f"score, with and without each new voice. Each event read in the third-octave (200 Hz-12 kHz) "
                      f"where it stands highest over everything else (v107's round 4c; the band after the @). Gates: "
                      f"the cast >= +3 dB, the crackles' and the bites' median >= +3 dB; the snare reported. "
                      f"Controls: AFTER (0.9 s after the last new voice, none sounding: must read NOT heard) and "
                      f"LEVEL (each voice 20 dB under: every event heard at >= +3 must read lower)")

                def fmt_v(v):
                    return " ".join(f"{x_:+.1f}" for x_ in v) + (f" (median {np.median(v):+.1f})" if len(v) > 1 else "")

                def ok_(g_):
                    return "absent" if g_ is None else ("heard" if g_ else "NOT heard")
                for key, nm in (((ME, 0), "the cast (0-100 ms)"), ((ME, 1), "the cast (150-250 ms)"),
                                ((ME + "-crackle", 0), "each crackle (100-300 ms)"),
                                ((ME + "-snare", 0), "each snare's creak (0-100 ms)"),
                                ((ME + "-snare", 1), "each snare's crack (200-300 ms)"),
                                ((ME + "-bite", 0), "each bite (0-60 ms)")):
                    if not res.get(key):
                        print(f"  {nm}: none in this window")
                        continue
                    vals = res[key]; at_ = res[key + ("@",)]
                    shown = " ".join(f"{x_:+.1f}@{f2:.0f}" for x_, f2 in list(zip(vals, at_))[:24]) + \
                        (" ..." if len(vals) > 24 else "")
                    print(f"  {nm}: {shown}" + (f" (median {np.median(vals):+.1f})" if len(vals) > 1 else "") +
                          (f" dB -- {ok_(G4[key])}" if key in G4 else " dB (reported)"))
                    print(f"      AFTER: {fmt_v(res_a[key]) if res_a[key] else 'no room'}"
                          + (f" -- {ok_(GA[key])}" if key in GA else "")
                          + f";  BURIED: median {np.median(res_b[key]):+.1f};  LEVEL: "
                          f"{'follows' if level_ok[key] else 'DOES NOT follow'} the voice")
                if not all(g_ is True for g_ in G4.values()):
                    FAILED.append("a new voice not heard in a real window")
                if any(g_ is not False for g_ in GA.values()):
                    print("  the AFTER control is heard (or has no room) -- the reading cannot come back wrong")
                    FAILED.append("real-window control (after)")
                else:
                    print("  the AFTER control (no new voice sounding) reads NOT heard for every voice, as it must")
                if not all(level_ok.get(k, True) for k in list(GATED) + [(ME + "-snare", 0), (ME + "-snare", 1)]):
                    print("  the LEVEL control: the reading does not follow a voice's level")
                    FAILED.append("real-window control (level)")
                else:
                    print("  the LEVEL control: every event heard at >= +3 dB reads lower with its voice 20 dB under, "
                          "as it must")
                wav("thornwake-pick-real-window.wav", xw)
                xo_all = R([e_ for e_, e in zip(allv, evs) if not e[3]], secs=secs, rows=sfx_rows, new=False)[0] + bd
                wav("thornwake-pick-real-window-without.wav", xo_all)
                rec["real"] = dict(win=w_, over={str(k): v for k, v in res.items()},
                                   buried={str(k): v for k, v in res_b.items()},
                                   after={str(k): v for k, v in res_a.items()},
                                   level_ok={str(k): v for k, v in level_ok.items()},
                                   gates={"round4c": {str(k): v for k, v in G4.items()},
                                          "after": {str(k): v for k, v in GA.items()}})
            else:
                print("\nIN A REAL WINDOW -- no cast with a crackle, a snare and three bites in the wire runs")
                FAILED.append("no real window")
        # the picks in order, for the ear: a blow planting a bramble, the snare
        # and the bites, the cast before them
        hitp = {"dmg": BLADE, "crit": False}
        seq = [["arm", T0, "ult", {"w": ME}]]
        for t_ in (0.9, 2.6):
            seq += [["arm", T0 + t_, "hit", hitp], ["arm", T0 + t_, "ult", {"w": ME + "-crackle"}],
                    ["arm", T0 + t_ + 0.1, "ult", {"w": ME + "-snare"}], ["arm", T0 + t_ + 0.1, "ult", {"w": ME + "-bite"}],
                    ["arm", T0 + t_ + 0.6, "ult", {"w": ME + "-bite"}], ["arm", T0 + t_ + 1.1, "ult", {"w": ME + "-bite"}]]
        wav("thornwake-pick-sequence.wav", R(seq, secs=6.0, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0 and not a.no_wire:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: Bramblesnare's cast, crackle, snare and bite arms, replacing the freeze's creak and cinch",
                 anchor=OLD_ARM, mode="replace", code=arms),
            dict(label="plantBramble: the crackle, once per bramble planted, after the count",
                 anchor=CRACKLE_ANCHOR, mode="after", code=CRACKLE_CODE),
            dict(label="tickBramble: the snare's voice (Tendril's root), on the frame the pin is written",
                 anchor=SNARE_ANCHOR, mode="after", code=SNARE_CODE),
            dict(label="tickBramble: the bite's soft snap, once per bite, as the thorns' cooldown is re-armed",
                 anchor=BITE_ANCHOR, mode="after", code=BITE_CODE)]
    for r_ in rows:
        if not (r_["code"].isascii() and r_["anchor"].isascii()):
            raise SystemExit(f"a row is not ASCII: {r_['label']}")
        _refuse(re.sub(r"/\*.*?\*/", "", r_["code"], flags=re.S), r_["label"])

    def apply_text(src_html, what):
        patched = src_html
        for r_ in rows:
            c = patched.count(r_["anchor"])
            if c != 1:
                raise SystemExit(f"{what}: an anchor occurs {c} times")
            an, rep = as_replace(r_["anchor"], r_["mode"], r_["code"])
            patched = patched.replace(an, rep, 1)
        for r_ in rows:
            want = 0 if r_["mode"] == "replace" else 1
            if patched.count(r_["anchor"]) != want:
                raise SystemExit(f"{what}: an anchor is not kept as its mode says")
        return patched

    def e2e_page(tp, ref_voices, ref_fights, label, root_ref=False):
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
            for lab_, p, body in NEWP:
                x1 = R2([["play", T0, "ult", p]], seed=NOISE_SEEDS[5])
                x2 = R2([["body", T0, body, {}]], seed=NOISE_SEEDS[5])
                nd.append((lab_, float(np.abs(x1 - x2).max())))
            if root_ref:
                xr1 = R2([["play", T0, "ult", {"w": ME + "-snare"}]], seed=NOISE_SEEDS[5])
                xr2 = R2([["play", T0, "ult", {"w": "bindweed-root"}]], seed=NOISE_SEEDS[5])
                nd.append(("snare vs this page's own bindweed-root", float(np.abs(xr1 - xr2).max())))
            xo_ = R2([["play", T0, "ult", {"w": ME}]])
            not_old = float(np.abs(xo_[:len(ctl_old)] - ctl_old).max())
            F1 = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
            if isinstance(F1, dict):
                raise SystemExit(F1["err"])
            page_err = len(errors)
        F0 = {f_["key"]: f_ for f_ in ref_fights}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        ok_n = {k: sum(f_[v] == f_[c] for f_ in F1) for k, v, c in
                (("cast", "castV", "casts"), ("crackle", "crackV", "planted"), ("snare", "snareV", "snares"),
                 ("bite", "biteV", "ticks"))}
        w_ok = sum(f_["stray"] == 0 for f_ in F1)
        orig_new = sum(f_["crackV"] + f_["snareV"] + f_["biteV"] for f_ in ref_fights)
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "planted", "snares", "ticks", "castV", "crackV",
                                                     "snareV", "biteV")}
        print(f"  the four voices through the patched page's own SFX.play vs the lab's candidate text in that page, "
              f"max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/thornwake vs the old creak and cinch on the patched page {not_old:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's (a digest of every step "
              f"included), every other SFX call identical in {osame}/{len(F1)}; per fight -- " +
              ", ".join(f"{k} voices = {k}s {v}" for k, v in ok_n.items()) +
              f", every voice where it belongs {w_ok} (of {len(F1)}); totals {tot}; the original page played "
              f"{orig_new} of the three sim voices; page errors {page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_old <= 1e-3 or same != len(F1)
                   or osame != len(F1) or min(list(ok_n.values()) + [w_ok]) != len(F1) or orig_new or page_err
                   or min(tot["crackV"], tot["snareV"], tot["biteV"]) == 0)
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_old=not_old, fights=len(F1), same=same, other_same=osame, totals=tot,
                    page_errors=page_err)

    ctl_old = ctl["OLD"]["x"]
    if a.e2e_seeds > 0 and not a.no_wire:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="thornwake_e2e_"))
        try:
            tp = tmpd / "sc-thornwake-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the four rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"({len(patched) - len(html):+d} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    # ---- ALSO: the rows on another link carrying Thornwake's stage 5 ----------
    rec["also"] = []
    for spec in ([] if a.no_wire else a.also):
        ap_ = resolve_game(spec)
        h2 = ap_.read_text(encoding="utf-8")
        s2 = hashlib.sha256(h2.encode()).hexdigest()[:16]
        p2 = apply_text(h2, ap_.name)
        has_root = '"bindweed-root"' in h2
        print(f"\nALSO -- {ap_.name} {s2} ({'carries' if has_root else 'does not carry'} Tendril's voices): every "
              f"anchor once, every row applies as its mode says; the original page first (a browser), then the "
              f"patched one (another, after it closes)")
        with game(game_path=ap_) as (page, errors):
            def R3(evs, seed=None):
                r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                assert not errors, errors[:3]
                return pcm(r)
            ps2 = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
            ids2 = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
            u2 = sorted(set(re.findall(r'w === "([a-z-]+)"', ps2)) | set(ids2) | {FALLBACK})
            k2 = sorted(set(re.findall(r'kind === "([a-z-]+)"', ps2)) - {"ult", "hit"})
            voices2 = [v_ for v_ in e2e_voices if v_[0] != "ult" or v_[1]["w"] in u2]
            voices2 += [("ult", {"w": w_, "n": 2}) for w_ in u2
                        if w_ != ME and not w_.startswith(ME + "-") and ("ult", {"w": w_, "n": 2}) not in voices2]
            voices2 += [(k_, {}) for k_ in k2 if (k_, {}) not in voices2]
            ref_v = [R3([["play", T0, k, p]]) for k, p in voices2]
            ref_f = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="thornwake_also_"))
        try:
            tp = tmpd / ap_.name
            tp.write_text(p2, encoding="utf-8", newline="")
            keep = e2e_voices
            e2e_voices = voices2
            try:
                E = e2e_page(tp, ref_v, ref_f, ap_.name, root_ref=has_root)
            finally:
                e2e_voices = keep
            E.update(game=ap_.name, sha=s2, patched_sha=hashlib.sha256(p2.encode()).hexdigest()[:16],
                     voices=len(voices2), tendril=has_root)
            rec["also"].append(E)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "bands", "DB", "sp")} | {"sp": M.get("sp")}
                for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), crackle=strip(rows_r), crackle_controls=strip(ctlr),
               bite=strip(rows_b), bite_controls=strip(ctlb), wavs=sizes,
               pick={"cast": Ca["name"], "cast_g": Ca["g"], "cast_kc": Ca["kc"], "cast_L": Ca["L"],
                     "crackle": Cr["name"], "crackle_g": Cr["g"], "crackle_S": Cr["S"],
                     "bite": Bi["name"], "bite_g": Bi["g"], "bite_D": Bi["D"], "snare": "Tendril's root (DEEP)"})
    print(f"\nTHE PICKS  cast {Ca['name']}   crackle {Cr['name']}   snare Tendril's root (reused)   bite {Bi['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    al = "".join(f"; the same stage 5 carried onto another tip ({X['game']} {X['sha']}): {X['same']}/{X['fights']}"
                 for X in rec["also"])
    wr = rec.get("wire")
    rows[0]["why"] = (
        f"The four voices of v84 s4, in the synth only; there is no close voice. The row REPLACES the four lines of "
        f"the freeze's 'creak and cinch' -- the arm keyed on this relic, which v84 retires with the freeze -- and "
        f"adds the crackle's, the snare's and the bite's arms beside it; it does not touch the shared rune-crack "
        f"fallback. The snare's body is Tendril's root arm's, transcribed (not on this base; equal to Tendril's own "
        f"to {max(v for k, v in rec['arm_check']['chk'] if 'Tendril' in k):.0e}). Through the patched play() every "
        f"arm reproduces its lab candidate (worst {max(v for _, v in rec['arm_check']['chk']):.0e}, on two noise "
        f"draws), {rec['arm_check']['n_others']} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), ult/thornwake is no longer the old arm and the bare "
        f"fallback is still rune-crack. play() returns on its first line with no audio context (every headless "
        f"run), draws no random number and writes nothing the simulation reads"
        + (f"; end to end the four voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    if wr:
        common = (f"{wr['same']}/{wr['fights']} fights identical (a digest of every step included) and every other "
                  f"SFX call identical in order and opts; the rows plus one sim write come back "
                  f"{wr['control_same']}/{wr['fights']}{e2}{al}. Writes nothing; no field for the probe's allowed set.")
        rows[1]["why"] = (
            f"One SFX.play after the plant's count (kept unchanged), reading nothing: {wr['crackV']}/{wr['planted']} "
            f"brambles planted voiced, each inside plantBramble, none elsewhere; " + common)
        rows[2]["why"] = (
            f"One SFX.play after the snare's count (kept unchanged), inside the entry block that writes the pin: "
            f"{wr['snareV']}/{wr['snares']} snares voiced, each inside tickBramble (live steps only), none elsewhere; "
            + common)
        rows[3]["why"] = (
            f"One SFX.play after the line that re-arms the thorns' cooldown (kept unchanged) -- every bite's first "
            f"line, on its own step, ahead of its entangle and hurt: {wr['biteV']}/{wr['ticks']} "
            f"bites voiced ({wr['killBites']}/{wr['kills']} killing bites among them), each inside tickBramble, "
            f"none elsewhere; on the {wr['together']} steps that snare and bite at once the snare sounds first; "
            + common)
    rec["rows"] = rows
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1, ensure_ascii=True), encoding="utf-8", newline="")
        print(f"ROWS   {a.rows}  ({len(rows)} rows)")
    if a.json:
        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, float) and o != o:
                return None
            if hasattr(o, "item"):
                return o.item()
            return o
        pathlib.Path(a.json).write_text(json.dumps(clean(rec), indent=1), encoding="utf-8")
    if FAILED:
        print(f"\nFAILED: {FAILED}")
        sys.exit(1)
    print("\nALL CHECKS PASS")


if __name__ == "__main__":
    main()
