#!/usr/bin/env python3
"""CONSECRATION'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v109.

    python censer_voice_lab.py --game <a link carrying Censer's stage 5> --rows rows.json
        [--peer-rows <batch>/<relic>/stage6-voice/rows_final.json ...]

v78 section 4 SOUND, every word of it: "cast -- a thurible swing (a
chain-rattle into a low bell, 0.5s); a disc opening -- a soft bell tone, pitch
by disc count; the smite tick -- nothing new (smite's own); the heal -- the
`spark collect` voice, reused." The brief's stage 4 (this batch's stage 6):
"picture, voice, carry". Rick, for the batch's art and sound: "you pick i
overrule". So this lab does not offer a spread -- it renders five candidates a
new voice beside CONTROLS that can come back wrong, prints the numbers each
pick is made on, and PICKS by a rule written in this file (`*_RULE`, `*_why`).
He overrules from one clip.

WHAT IS REUSED, AND WHAT IS NOT MADE:
  * THE HEAL plays the EXISTING `spark {collect: true, n}` -- the heal chime
    Daybreak's sparks and Zenith's blessings already play -- unchanged, n =
    the blessing count Censer carries after the apply, Zenith's call word for
    word. It exists, so nothing is made for it; it is measured here beside
    the new voices (the disc bell must not be it).
  * THE SMITE TICK HAS NO VOICE. v78 says "nothing new (smite's own)", and
    smite has no voice of its own in this engine: `apply("smite")` plays
    nothing, and every sanctified blow that applies smite (`onHit`) is voiced
    by the blow. So "nothing new" is nothing: no row, no arm. (A smite-tick
    voice is Rick's to ask for; FOR RICK below.)
  * The design names no close voice, so there is none.

THE THREE EVENTS AND WHERE THEY FIRE (line numbers are sc-censer-consecration-
b25.5's):
  cast   the bare id `ult/censer`, which `fireUlt` plays for every relic in its
         shared prologue (16307), before the holyground branch. Censer has NO
         arm today: it falls through to the shared rune-crack (measured below,
         to 1e-6, with every other relic that still does). The arms go BEFORE
         that fallback, in a row of mode `before` whose anchor is the fallback
         line itself -- so the fallback is never touched, and another relic's
         row anchored on it applies in either order. No sim line: the cast
         already plays it, once a cast.
  disc   `ult/censer-disc {n}` from `resolveHit`, right after the push's own
         `self.holyTally.discs++;` (14642, mode `after`, inside the push's
         `if`): once per disc planted, on the blow's frame -- the blow's own
         `hit` voice sounds on the same frame, so the bell is measured OVER a
         blow. `n` = the caster's discs standing on the ground after the push,
         the new one included (the purge has already run this step:
         `tickHolyGround` runs before the hit loop), clamped 1..5 in the arm.
  heal   the unchanged `spark {collect: true, n}` from `tickHolyGround`, right
         after the blessing's own `T.bless++;` (13701, mode `after`): once per
         blessing, on its frame, n = f.stacks("blessing") after the apply.
  Nothing here sets a hit stop, files a beat or writes a field the simulation
  reads: the rows add plain SFX.play calls, and the disc row READS
  `m.holyGround` to count (a block-scoped counter, nothing written).

THE CONTROLS, and what each one is for:
  rune-crack   what Censer's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted (with hit@11.6
               0.443 / 80 ms)
  hit@25.5     Censer's own blow (the blade, stage 5): the level every voice
               is judged against, on its quietest / loudest draw
  hit@45       the heaviest blow's voice (the hit voice's weight saturates at
               45; 18% of the blows on a disc's frame are that heavy, the
               median is 33 -- stage6-voice/survey.py): the blow the disc bell
               must be heard over, on the same frame
  wall         the commonest sound in a fight: the bell's floor
  the school   the sanctified casts with a voice of their own (read off the
               page) and, from `--peer-rows`, the batch line's
  the type     the warhammer casts with a voice of their own (read off the
               page) and, from `--peer-rows`, the batch line's
  seal, clank, death, hex-snap   the game's other stack of low tones, metal
               on metal, the heaviest low voice, the runic snap
  spark 1-5    the heal chime (the spark collect) -- the heal, reused
  zt 0-4       Zenith's tick, the school's small bright chime
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  BELL, RATTLE, HIGH, HARM, LONG, AFTER, RC-NOW   the pick without its
               rattle / without its bell / its bell two octaves up / its
               bell's partials on whole multiples of its lowest (a harmonic
               tone, not a bell) / ringing 1.5 s / the bell first and the
               rattle after it / today's voice: each must fail ITS OWN gate
  FLAT, LOUD, HARM, TICK, CLANG, SPARK   the picked disc at count 1's note
               for every count / 3 dB over its quiet bound / on whole
               multiples / dying in 40 ms / with a bar's bright modes and a
               click / the heal chime played as the disc: each must fail ITS
               OWN gate

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise: ironwood_voice_lab's RENDER_JS, imported unchanged). Noise-built
    sounds are judged on the worst of twelve draws. Nothing may sound before
    t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT. Each candidate is generated as the JS
    body that will sit in the arm (constants rounded first) and rendered by
    evaluating that text on the synth; the row is then applied to
    `Sfx.prototype.play`'s own source and rendered again, and must match to
    TOL = 1e-5 (-100 dB).
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's and
    ironhail_voice_lab's, imported unchanged: E50, TOP (the loudest 50 ms, and
    where it is centred), AUDIBLE (the 5 ms RMS above 2% of its own loudest),
    RISE, CENTROID, REG (cosine of 1/3-octave band amplitudes, 25 Hz-16 kHz,
    the median over noise draws), PITCH (FFT peak, Hann, zero-padded,
    parabolic), IN-BAND (a pitch's third-octave RMS), PHONE (TOP high-passed
    at 200 Hz); ONSETS is lightkeeper_voice_lab's (v107), copied unchanged
    (1 ms RMS peaks >= 15 ms apart, each >= 0.3 of the loudest and >= 6 dB
    over the dip since the last); NOISE PART is angelus_voice_lab's (two
    draws of one text differ by exactly their noise-built part).
  * New here, each with a control that can come back wrong:
      STRIKE   the bell's onset: the first 1 ms at which the voice low-passed
               (FFT) at 600 Hz reaches half its loudest -- a link of the
               chain rings at 3-6 kHz and has nothing there (AFTER and RATTLE
               must fail it)
      RATTLE   before the strike: ONSETS (a rattle is many), the CENTROID
               (small metal), its loudest 50 ms re the bell's (after the
               strike), its best third-octave against the score's p90
      PEAKS    the spectral peaks over a window (Hann, zero-padded) within 20
               dB of the strongest, 50 Hz-4 kHz, merged within 2%
      BELL     among the PEAKS, the most cents any lies off every whole
               multiple of the LOWEST: a bell's partials are inharmonic (the
               church bell's tierce, a minor third over its prime, is 2.4x
               its hum), a harmonic tone's are not (HARM must fail)
      LOW      the bell's strongest peak (strike + 20-200 ms) and its share of
               the power under 500 Hz (strike to end)
      OVER-BLOW  the disc bell and the heaviest blow's voice on one frame,
               both through the chain (the compressor sees both): the bell's
               note in its third-octave over 0-200 ms, re the blow alone
  * THE CANDIDATES ARE LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's bell decay is solved to AUDIBLE 500 ms, its rattle to
    6 dB under the bell (loudest 50 ms), its gain to the centre of its level
    window; the disc's decay is solved to AUDIBLE 400 ms at count 3 and its
    gain to the centre of its window there. Constants are rounded BEFORE any
    measured render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of v78 section 4 turned into
numbers; Code's picks, Rick's to overrule):
  * "A THURIBLE SWING (A CHAIN-RATTLE INTO A LOW BELL, 0.5s)": nine links of
    the chain clinking over the swing (0-0.19 s), each a short pinged pair of
    sines at 3.3-6.1 kHz (a small metal link) or a ringing band of noise
    there, rising in level toward the bell (the swing coming down); the bell
    STRUCK at 0.20 s, after the last link. "0.5s" is the whole voice:
    AUDIBLE 415-585 ms (v100's +/-17.5%). "Into": the rattle leads, 6 dB
    under the bell. "Low": the bell's strongest partial at or under 500 Hz
    and most of its power there -- a church bell on A (the score's tonic):
    hum A2, prime A3 (220 Hz), tierce, quint, nominal A4 -- or on E; its
    decay is what 0.5 s allows (a damped bell: the thurible's own, not a
    tower's).
  * "A SOFT BELL TONE, PITCH BY DISC COUNT": a small bell struck once (sines
    on a bell's inharmonic modes), one step of the score's A minor pentatonic
    a count from the candidate's root, counts clamped 1..5 (a sixth disc
    standing is 2 of 716 in the survey; it rings at 5's note). "The disc
    count" is the caster's discs STANDING after the push, the new one
    included -- the holy ground the floor shows, rising as the hammer lands
    and falling as discs expire -- not the fight's running total (which runs
    to 13 and never falls). It rings AUDIBLE 400 ms at count 3 (gate
    250-600; a caster's discs are at least 0.51 s apart, p5 0.72 s). "Soft":
    no clack (pure), mellow (its centroid within 2x its note), and quiet --
    under the blow it lands with, over the wall tick. Its register sits under
    the heal chime (1.29-1.73 kHz) that follows it (p5 0.125 s later).
  * THE BELL ON A KILLING BLOW: the disc is planted (and drawn) on the kill's
    blow too, so it rings there, over the death voice (32 of 716 discs in the
    survey). FOR RICK below.
  * THE HEAL: `spark {collect: true, n}` unchanged, n = f.stacks("blessing")
    after the apply -- Zenith's call, word for word.
  * REGISTER: every new voice <= 0.80 against each voice it must not be
    (listed in its rule), and against every voice the batch line's other
    relics add (`--peer-rows`).

THE PICKS, on Chromium 151.0.7922.34, sc-censer-consecration-b25.5
56c49ad3f0ccb3aa, fight seeds 109601-109602 (148 fights), with nine peers'
rows (Angelus, Lodestone, Lightkeeper, Widowmaker, Oracle, Portcullis,
Coldiron, Ironhail, Bindweed: 30 voices):

  cast   4 JINGLE  nine links ringing as bands of noise (Q 6, 30 ms, 3.3-6.1
                   kHz) rising in level, then a church bell struck on A at
                   206 ms (hum A2, prime A3, tierce, quint, nominal A4, and
                   the clapper's knock): audible 495 ms, 9 onsets of the
                   rattle, its centroid 4.9 kHz, 5.8 dB under the bell; the
                   bell's strongest peak 110 Hz (the hum), 99% of its power
                   under 500 Hz, its tierce 315 cents off the hum's
                   harmonics, heard +14.1 dB over the score above 200 Hz;
                   TOP -2.9 dB re the blow @ 25.5, +19.0 re the wall;
                   register at most 0.69 (Ironhail's cast, a peer), 0.57
                   against the seal, 0.41 against rune-crack, 0.56 against
                   the warhammers' casts. CHURCH, BRONZE and SWING pass too
                   (0.69-0.72) and lose on calls (33-36 to 15); DEEP passes
                   and loses on register (0.76, Lightkeeper's gong).
  disc   2 BOWL    a struck bowl (two sines on 1 : 2.71, the upper at 0.3)
                   on C5 D5 E5 G5 A5 (523-880 Hz) for 1-5 discs standing:
                   audible 400 ms at every count, pure, its centroid 1.1x
                   its note; loudest 50 ms -11.0 dB re the blow @ 25.5,
                   +11.0 re the wall; over the heaviest blow on its frame
                   +13.0 to +17.8 dB in its note's third-octave (+13.4 to
                   +19.9 with a crit); count 1 +14.0 dB over the score;
                   register at most 0.66 (Angelus's cast chord, a peer),
                   0.27 against the heal chime and Zenith's tick. CUP passes
                   and loses on register (0.68); CHAPEL, LOW and HIGH read
                   0.85 against Angelus's chord (D4 A4 D5: their notes and
                   hums land on it), HIGH also 0.92 against the heal chime
                   (its C6 and D6).
  heal   the spark collect, unchanged (1.29-1.73 kHz, +7.3 dB re the wall).
  smite  nothing.

  In play (148 fights): 456 casts and 456 cast voices; 716 discs and 716
  bells, each on its push's step with the discs standing (1: 329, 2: 224,
  3: 109, 4: 43, 5: 9, 6: 2 -- the sixth at 5's note), 32 of them on a
  killing blow; 1063 blessings and 1063 heal chimes (1: 325 ... 5: 144);
  148/148 fights identical, every other voice call identical in order,
  kind and opts; the rows plus one sim write come back identical in only
  4/148 (the survey has 2 of the 148 fights with no disc at all).
  End to end (the rows as text, a fresh browser, seed 109651): 74/74.

  In a real window (Farwarden, Censer side B, seed 109602: cast at 61.22 s,
  three discs at counts 2 3 3 and eight heals by 69.68 s), the fight's own
  sounds and the score mixed as `cinema_clip` mixes them, with and without
  the new voices: every disc bell +5.2 to +15.3 dB over the fight in its
  note's third-octave; the rattle +17.3 dB at 5 kHz; the bell +37.0 dB in
  its best third-octave at or above 200 Hz (400 Hz, its nominal: read as its
  isolation gate reads it) and +4.8 dB at its hum (110 Hz, the band the
  score's bass lives in); the heal chimes +10.3 to +33.2 dB (printed: the
  chime is reused). Written to censer-pick-real-window.wav and -without.wav.

  Main-thread cost a call: the cast 0.5 ms (15 synth calls), the disc and
  the heal under 0.1 ms.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (two arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm must reproduce
    its candidate to TOL (the disc at counts -1, 0, 1..6, 9 and a missing
    `n`, on two noise draws); every other voice through the patched play (the
    hit at five weights with and without a crit, the heal chime at n 0-6,
    spark arm and burn, wall, death, clank x2, seal, nova, hex-snap, fork,
    vine x4, loose x3, aegis x2, scour x4, every ult id and every kind the
    page's play() names) must be unchanged; `ult/censer` must NOT be
    rune-crack any more;
  * the resolveHit and tickHolyGround rows are applied to their prototypes'
    own source and run on real fights beside the unpatched ones: every fight
    identical (over, the clock, the ground's clock and every disc, both
    fighters' hp, shield, position, velocity, stun, blows, damage dealt,
    smite and blessing counts and holyTally, the winner) and every other
    voice call identical in order, kind and opts; one disc bell per disc, on
    its push's step, inside resolveHit, carrying the count of the caster's
    discs standing after it; one heal chime per blessing, on its step, inside
    tickHolyGround, carrying the count the apply left; one cast voice per
    cast; the unpatched runs play none of the new ones. The same rows plus
    ONE sim write (the foe nudged 1e-9 on a disc) must come back NOT
    identical, or "identical" proves nothing. (The Sfx row cannot reach the
    simulation at all: `play` returns on its first line with no audio
    context, which is every headless run.)
  * END TO END: the rows applied AS TEXT (the orchestrator's semantics:
    replace = code, after = anchor + code, before = code + anchor) to a copy
    of the game file (in a temp folder, never the repo), loaded in a fresh
    browser after the first is closed: the page loads clean, its own
    SFX.play renders the arms to the lab's text and every other voice to the
    original page's, and its fights are identical to the original page's,
    with the voice counts above.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both
    identically; the registers against the peers' voices are gated.
  All anchors must occur exactly once in the game file; no row replaces its
  anchor, so a later relic's row -- or the picture's -- anchored on the same
  line still applies, in either order. Every row is ASCII.

FOR RICK TO OVERRULE ("you pick i overrule"):
  * THE SMITE TICK IS SILENT (v78: "nothing new (smite's own)"; smite has no
    voice of its own). A smite-tick voice would sound 4.7 times a cast.
  * THE DISC COUNT is the discs standing, not the fight's running total and
    not the window's count (the window's index reads within a disc of it:
    same median, same p95).
  * THE BELL ON A KILLING BLOW rings over the death voice (4% of discs).
  * THE LOW BELL'S LOW END is under a phone speaker (200 Hz); its nominal and
    the rattle are not.
  * THE RATTLE IS NOISE-BUILT (bands of the synth's noise buffer, which the
    live game fills with Math.random once a session), so it varies a little
    from session to session; it is judged on the worst of twelve draws. The
    pinged rattles (CHURCH, SWING) pass as well and are the same every time;
    JINGLE won on the tiebreak (fewer synth calls, 15 to 33), not on a gate.

Writes wavs to 05-reference/v109/censer-*.wav at RAW level (gitignored).
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
# means in v98's, v99's and v108's labs. (Their module bodies only define things
# and check their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db, env, fmt, pcm, pitch,
    write_wav)
from ironwood_voice_lab import RENDER_JS, lowpass_fft  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90, phone  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "censer"
BLADE = 25.5                              # Censer's dmg (stage 5's blade)
HEAVY = 45.0                              # the hit voice's weight saturates here: w = clamp(dmg / 45, 0.12, 1)
MID = 33.0                                # the median blow on a disc's frame (stage6-voice/survey.py)
CAP = 5                                   # the disc count is clamped 1..5 in the arm
PENT = [0, 3, 5, 7, 10]                   # the A minor pentatonic, from A: A C D E G
CAST_AUD = 500.0                          # "0.5s": the bell's decay is solved to this (gate 415-585)
STRIKE = 0.20                             # the bell is struck here, after the chain's last link (0.171-0.183 s)
RATTLE_UNDER_DB = 6.0                     # the rattle's loudest 50 ms under the bell's (level-matched)
KNOCK = 0.25                              # the clapper's knock re the bell's gain
DISC_AUD = 400.0                          # the disc bell's decay is solved to this at count 3 (gate 250-600)
DISC_REF_N = 3                            # the count the disc bell is level-matched at
TOL = 1e-5                                # reproduction / transcription (-100 dB)
SCHOOL_AFF = "sanctified"
TYPE_SHAPE = "warhammer"


def _np():
    import numpy as np
    return np


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


def peer_name(pf):
    """A peer rows file's relic: `<scratch>/batch/<relic>/stage6-voice/rows_final.json` -> "Relic"."""
    p_ = pathlib.Path(pf).parent
    return (p_.parent.name if p_.name.startswith("stage") else p_.name).capitalize()


def as_replace(anchor, mode, code):
    """A row as the [anchor, replacement] pair its mode means (the orchestrator's
    semantics: replace = code, after = anchor + code, before = code + anchor)."""
    return [anchor, {"replace": code, "after": anchor + code, "before": code + anchor}[mode]]


def note_hz(name):
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    k = names[name[0]] + (1 if "#" in name else 0)
    return 440.0 * 2 ** ((k + 12 * (int(name[-1]) - 4)) / 12)


def note_name(f):
    names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    k = round(12 * math.log2(f / 55.0))
    return f"{names[k % 12]}{(k + 9) // 12 + 1}"


def pent_from(root):
    """Five pentatonic degrees upward from `root` (a note of A minor pentatonic)."""
    s = round(12 * math.log2(root / 440.0))
    deg = []
    while len(deg) < 5:
        if (s % 12) in PENT:
            deg.append(round(440.0 * 2 ** (s / 12), 2))
        s += 1
    return deg


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


def marr(M):
    return "[" + ", ".join("[" + ", ".join(fmt(v) for v in x) + "]" for x in M) + "]"


def harm_modes(modes):
    """The HARM control's modes: every ratio moved to the nearest whole multiple
    of the lowest (a harmonic tone with the bell's levels and decays)."""
    lo = min(r for r, _k, _d in modes)
    return [(round(r / lo) * lo, k, d) for r, k, d in modes]


# =============================================================== THE CAST ===
# "a thurible swing (a chain-rattle into a low bell, 0.5s)". Every candidate is
# the chain's nine links clinking over the swing, rising in level, and the bell
# struck at 0.20 s after the last; they differ in the links (pinged metal, or
# ringing bands of noise; evenly or quickening) and in the bell.
#   links  [s, f, k]: when (s after the cast), the link's ring (Hz), its level re the rattle's
LINKS = {
    "even": [(0.000, 4100, 0.45), (0.019, 5300, 0.52), (0.041, 3700, 0.58), (0.057, 6100, 0.64),
             (0.082, 4600, 0.71), (0.101, 3300, 0.77), (0.126, 5700, 0.84), (0.148, 4300, 0.92),
             (0.171, 5000, 1.0)],
    "accel": [(0.000, 4100, 0.40), (0.036, 5300, 0.48), (0.068, 3700, 0.56), (0.096, 6100, 0.64),
              (0.120, 4600, 0.72), (0.140, 3300, 0.80), (0.157, 5700, 0.88), (0.171, 4300, 0.95),
              (0.183, 5000, 1.0)],
}
#   bell modes (ratio re the prime, level, decay re D): a church bell's hum, prime, tierce, quint, nominal
CHURCH = [(0.5, 0.5, 1.5), (1.0, 0.7, 1.0), (1.2, 0.55, 0.8), (1.5, 0.3, 0.6), (2.0, 1.0, 0.5)]
BELLS = {
    "church": CHURCH,
    "bronze": CHURCH + [(2.5, 0.35, 0.35), (3.0, 0.3, 0.3), (4.0, 0.2, 0.25)],
}
CAST_CANDIDATES = [
    ("1 CHURCH", dict(links="even", rattle="ping", bell="church", f=220.0),
     "nine pinged links (two sines, 1 : 1.47, and a tick of noise) rising in level, then a church bell on A: "
     "hum A2, prime A3, tierce, quint, nominal A4"),
    ("2 DEEP", dict(links="even", rattle="ping", bell="church", f=164.81),
     "CHURCH with the bell on E: prime E3 (164.8 Hz), nominal E4"),
    ("3 BRONZE", dict(links="even", rattle="ping", bell="bronze", f=220.0),
     "CHURCH with the bell's upper partials too (2.5, 3 and 4x its prime): a brighter bronze"),
    ("4 JINGLE", dict(links="even", rattle="jingle", bell="church", f=220.0),
     "CHURCH with each link a ringing band of noise (Q 6, 30 ms) instead of pinged sines"),
    ("5 SWING", dict(links="accel", rattle="ping", bell="church", f=220.0),
     "CHURCH with the links quickening (36 ms apart to 12) as the censer swings down into the bell"),
]


def cast_modes(sp):
    m = BELLS[sp["bell"]]
    return harm_modes(m) if sp.get("harm") else m


def cast_body(sp, g, kr, D, part="both", ind=10):
    """The cast arm's body. part: both / rattle / bell. sp: links, rattle (ping /
    jingle), bell, f (the prime), and the controls' harm, strike, rattle_at."""
    S = sp.get("strike", STRIKE)
    L = [f"const g = {fmt(g)}, kr = {fmt(kr)}, D = {fmt(D)}, S = {fmt(S)}, F = {fmt(sp['f'])};"]
    if part in ("both", "rattle"):
        off = sp.get("rattle_at", 0.0)
        li = [f"[{fmt(round(s + off, 6))}, {fmt(f)}, {fmt(k)}]" for s, f, k in LINKS[sp["links"]]]
        L.append("for (const [s, f, k] of [" + ", ".join(li[:3]) + ",")
        L.append("                         " + ", ".join(li[3:6]) + ",")
        L.append("                         " + ", ".join(li[6:]) + "]){")
        if sp["rattle"] == "ping":
            L += ['  this._tone(t + s, { freq: f, gain: g * kr * k, dur: 0.02, type:"sine" }).frequency.value = f;',
                  '  this._tone(t + s, { freq: f * 1.47, gain: g * kr * k * 0.5, dur: 0.012, type:"sine" })'
                  '.frequency.value = f * 1.47;',
                  '  this._burst(t + s, { freq: f * 1.9, q: 3, gain: g * kr * k * 0.6, dur: 0.006, type:"bandpass" });']
        else:
            L += ['  this._burst(t + s, { freq: f, q: 6, gain: g * kr * k, dur: 0.03, type:"bandpass" });']
        L.append("}")
    if part in ("both", "bell"):
        L += [f"for (const [r, k, d] of {marr(cast_modes(sp))})",
              '  this._tone(t + S, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;',
              f'this._burst(t + S, {{ freq: F * 4, q: 0.9, gain: g * {fmt(KNOCK)}, dur: 0.012, type:"bandpass" }});']
    return "\n".join(" " * ind + l_ for l_ in L)


# =============================================================== THE DISC ===
# "a soft bell tone, pitch by disc count". A small bell struck once, one step of
# the score's A minor pentatonic a count from the candidate's root.
#   modes (ratio re the note, level, decay re D)
DMODES = {
    "chapel": [(0.5, 0.3, 1.3), (1.0, 1.0, 1.0), (1.2, 0.4, 0.8), (1.5, 0.2, 0.7), (2.0, 0.35, 0.55)],
    "bowl": [(1.0, 1.0, 1.0), (2.71, 0.3, 0.55)],
    "cup": [(1.0, 1.0, 1.0), (2.32, 0.3, 0.6), (3.9, 0.1, 0.35)],
    "clang": [(1.0, 1.0, 1.0), (2.76, 0.7, 0.7), (5.40, 0.6, 0.5), (8.93, 0.5, 0.35)],
}
DISC_CANDIDATES = [
    ("1 CHAPEL", dict(modes="chapel", root="C5"),
     "a small church bell (hum, prime, tierce, quint, nominal) on C5 D5 E5 G5 A5 for counts 1-5"),
    ("2 BOWL", dict(modes="bowl", root="C5"),
     "a struck bowl (sines on 1 : 2.71), C5-A5"),
    ("3 CUP", dict(modes="cup", root="C5"),
     "a cup bell (sines on 1 : 2.32 : 3.9), C5-A5"),
    ("4 LOW", dict(modes="chapel", root="A4"),
     "CHAPEL a third down: A4 C5 D5 E5 G5"),
    ("5 HIGH", dict(modes="chapel", root="E5"),
     "CHAPEL a third up: E5 G5 A5 C6 D6"),
]


def disc_notes(sp):
    n_ = pent_from(note_hz(sp["root"]))
    return [n_[0]] * 5 if sp.get("flat") else n_


def disc_modes(sp):
    m = DMODES[sp["modes"]]
    return harm_modes(m) if sp.get("harm") else m


def disc_body(sp, g, D, ind=10):
    if sp.get("spark"):                     # the SPARK control: the heal chime's own shape, as the disc
        L = [f"const n = clamp(Math.round(p.n || 0), 1, {CAP});",
             'this._tone(t, { freq: 1180 + n * 110, gain: 0.05, dur: 0.20, type:"triangle" });']
        return "\n".join(" " * ind + l_ for l_ in L)
    tab = ", ".join(fmt(f) for f in disc_notes(sp))
    L = [f"const n = clamp(Math.round(p.n || 0), 1, {CAP}), g = {fmt(g)}, D = {fmt(D)};",
         f"const F = [{tab}][n - 1];",
         f"for (const [r, k, d] of {marr(disc_modes(sp))})",
         '  this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;']
    if sp.get("click"):
        L.append('this._burst(t, { freq: 5000, q: 1, gain: g * 0.8, dur: 0.006, type:"highpass" });')
    return "\n".join(" " * ind + l_ for l_ in L)


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
DISC_ANCHOR = '      self.holyTally.discs++;'
HEAL_ANCHOR = '          T.bless++;'

DISC_CODE = '''
      /* CONSECRATION'S DISC (v78 s4: "a disc opening -- a soft bell tone,
         pitch by disc count"): once per disc planted, on the blow's frame,
         `n` the caster's discs standing on the ground now, this one
         included (the purge ran earlier this step, in tickHolyGround). The
         blow keeps its own `hit` voice. A block-scoped count that READS
         the ground and writes nothing; SFX.play is a no-op headless and
         nothing is read back (censer_voice_lab: fights identical). */
      { const sd_ = self === this.a ? "a" : "b";
        let n_ = 0;
        for (const d_ of this.holyGround) if (d_.side === sd_) n_++;
        SFX.play("ult", { w: "censer-disc", n: n_ }); }'''

HEAL_CODE = '''
          /* CONSECRATION'S HEAL (v78 s4: "the heal -- the `spark collect`
             voice, reused"): the EXISTING heal chime, unchanged, once per
             blessing, after the apply, with the count Censer now carries --
             Zenith's call word for word. Presentation only; nothing is read
             back (censer_voice_lab: fights identical). */
          SFX.play("spark", { collect: true, n: f.stacks("blessing") });'''

# the sim-write control: the disc row with the foe nudged 1e-9 on a disc
DISC_CODE_BAD = DISC_CODE.replace('        SFX.play("ult", { w: "censer-disc"',
                                  '        foe.vx += 1e-9;\n        SFX.play("ult", { w: "censer-disc"', 1)
assert DISC_CODE_BAD != DISC_CODE
_refuse(re.sub(r"/\*.*?\*/", "", DISC_CODE + HEAL_CODE, flags=re.S), "sim rows")
SIM_ROWS = [(DISC_ANCHOR, "after", DISC_CODE), (HEAL_ANCHOR, "after", HEAL_CODE)]


# ============================================================== THE PAGE ===
# The resolveHit and tickHolyGround rows, applied to the real prototypes and run
# beside the originals; the survey of Consecration's windows comes out of the
# same runs.
WIRE_JS = r"""([seeds, rhRows, hgRows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "censer";
  const oH = P.resolveHit, oG = P.tickHolyGround;
  const patch = (fn, rows, nm) => {
    let src = fn.toString();
    for (const [a, c] of rows){
      const at = src.split(a).length - 1;
      if (at !== 1) return { err: `a ${nm} anchor occurs ${at} times in ${nm}()` };
      src = src.replace(a, () => c);
    }
    return (0, eval)("(function " + src + ")");
  };
  const pH = patch(oH, rhRows, "resolveHit"), pG = patch(oG, hgRows, "tickHolyGround");
  if (pH.err) return pH; if (pG.err) return pG;
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b, sl = side ? "b" : "a";
    const mine = [], other = [], pushes = [], blesses = [], casts = [];
    let step = 0, inH = 0, inG = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-"))
        mine.push({ step, t: m.t, k: w, n: p.n === undefined ? null : p.n, inH: !!inH, inG: !!inG,
                    keys: Object.keys(p).join(",") });
      else if (kind === "spark" && inG)
        mine.push({ step, t: m.t, k: "heal", n: p.n, collect: p.collect, inH: !!inH, inG: !!inG,
                    keys: Object.keys(p).join(",") });
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    P.resolveHit = function(...args){
      const d0 = f.holyTally ? f.holyTally.discs : 0;
      inH++;
      try { return (wire ? pH : oH).apply(this, args); }
      finally { inH--;
        if (f.holyTally && f.holyTally.discs > d0)
          pushes.push([step, m.holyGround.filter(d => d.side === sl).length, f.holyTally.discs - d0, foe.alive, m.t]); } };
    P.tickHolyGround = function(dt){
      const b0 = f.holyTally ? f.holyTally.bless : 0;
      inG++;
      try { return (wire ? pG : oG).call(this, dt); }
      finally { inG--;
        if (f.holyTally && f.holyTally.bless > b0) blesses.push([step, f.stacks("blessing"), f.holyTally.bless - b0, m.t]); } };
    let n = 0, c0 = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        if (f.holyTally && f.holyTally.casts > c0){ c0 = f.holyTally.casts; casts.push([step, m.t]); }
      }
    } finally { P.resolveHit = oH; P.tickHolyGround = oG; if (had) S.play = op; else delete S.play; }
    const fr = (x) => [x.hp, x.shield, x.x, x.y, x.vx, x.vy, x.stun, x.alive, x.hits, x.dealt,
                       x.stacks("smite"), x.stacks("blessing"), x.holyTally ? JSON.stringify(x.holyTally) : null];
    return { sum: JSON.stringify([m.over, m.t, m.holyT, JSON.stringify(m.holyGround), fr(m.a), fr(m.b),
                                  m.winner ? m.winner.w.id : null]),
             mine, other: JSON.stringify(other), pushes, blesses, casts, t: m.t, over: m.over };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  let casts = 0, castV = 0, discs = 0, discV = 0, blessings = 0, healV = 0, killBells = 0;
  const ns = [], hn = [], clips = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.mine.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a new voice"]);
    const cv = B.mine.filter(c => c.k === ME), dv = B.mine.filter(c => c.k === "censer-disc"),
          hv = B.mine.filter(c => c.k === "heal");
    casts += B.casts.length; castV += cv.length;
    if (cv.length !== B.casts.length || cv.some((c, i) => c.step !== B.casts[i][0] || c.inH || c.inG || c.keys !== "w"))
      bad.push([fid, sd, "cast voices vs casts", cv.length, B.casts.length]);
    discs += B.pushes.length; discV += dv.length;
    if (dv.length !== B.pushes.length) bad.push([fid, sd, "disc bells vs discs", dv.length, B.pushes.length]);
    for (let i = 0; i < Math.min(dv.length, B.pushes.length); i++){
      const c = dv[i], q = B.pushes[i];
      if (c.step !== q[0]) bad.push([fid, sd, "a disc bell off its push's step", c.step, q[0]]);
      if (!c.inH || c.inG) bad.push([fid, sd, "a disc bell outside resolveHit"]);
      if (c.n !== q[1]) bad.push([fid, sd, "the bell's count is not the discs standing", c.n, q[1]]);
      if (q[2] !== 1) bad.push([fid, sd, "two discs from one resolveHit", q[2]]);
      if (c.keys !== "w,n") bad.push([fid, sd, "disc opts", c.keys]);
      ns.push(c.n);
      if (!q[3]) killBells++;
    }
    blessings += B.blesses.length; healV += hv.length;
    if (hv.length !== B.blesses.length) bad.push([fid, sd, "heal chimes vs blessings", hv.length, B.blesses.length]);
    for (let i = 0; i < Math.min(hv.length, B.blesses.length); i++){
      const c = hv[i], q = B.blesses[i];
      if (c.step !== q[0]) bad.push([fid, sd, "a heal chime off its blessing's step", c.step, q[0]]);
      if (!c.inG || c.inH) bad.push([fid, sd, "a heal chime outside tickHolyGround"]);
      if (c.n !== q[1]) bad.push([fid, sd, "the chime's count is not the blessing after the apply", c.n, q[1]]);
      if (c.collect !== true || c.keys !== "collect,n") bad.push([fid, sd, "heal opts", c.keys]);
      hn.push(c.n);
    }
    /* a real window for the ear: a cast, its discs and heals before the next cast */
    for (let i = 0; i < B.casts.length; i++){
      const t0 = B.casts[i][1], t1 = i + 1 < B.casts.length ? B.casts[i + 1][1] : 1e9;
      const d_ = B.pushes.filter(q => q[4] >= t0 && q[4] < t1 && q[3]), h_ = B.blesses.filter(q => q[3] >= t0 && q[3] < t1);
      const last = Math.max(t0, ...d_.map(q => q[4]), ...h_.map(q => q[3]));
      if (d_.length >= 2 && last - t0 <= 9.5 && B.t - last > 1.5)
        clips.push([side, fid, sd, t0, last, d_.length, h_.length]);
    }
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), casts, castV, discs, discV, blessings, healV, killBells,
           ns, hn, clips, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Consecration's (the heal: a spark inside tickHolyGround).
RECORD_JS = r"""([side, fid, sd, rhRows, hgRows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "censer";
  const oH = P.resolveHit, oG = P.tickHolyGround;
  let sH = oH.toString(); for (const [a, c] of rhRows) sH = sH.replace(a, () => c);
  let sG = oG.toString(); for (const [a, c] of hgRows) sG = sG.replace(a, () => c);
  const pH = (0, eval)("(function " + sH + ")"), pG = (0, eval)("(function " + sG + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = []; let inG = 0;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && q.w.startsWith(ME)) ? q.w
              : (kind === "spark" && inG) ? "heal" : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.resolveHit = pH;
  P.tickHolyGround = function(dt){ inG++; try { return pG.call(this, dt); } finally { inG--; } };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.resolveHit = oH; P.tickHolyGround = oG; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# The fights a page plays with ITS OWN code (the end-to-end check): the rows are
# in the page's text, so this only wraps the two methods to know where a call
# came from, and records.
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "censer";
  const res = [];
  if (!P.tickHolyGround) return { err: "no tickHolyGround" };
  const oH = P.resolveHit, oG = P.tickHolyGround;
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, sl = side ? "b" : "a";
    const log = [], other = [];
    let inH = 0, inG = 0, badN = 0, stray = 0, discs = 0, blessings = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME){ log.push("cast"); if (inH || inG) stray++; }
      else if (w === ME + "-disc"){ log.push("disc"); if (!inH) stray++;
        if (p.n !== m.holyGround.filter(d => d.side === sl).length) badN++; }
      else if (w.startsWith(ME + "-")){ log.push(w); stray++; }
      else if (kind === "spark" && inG){ log.push("heal"); if (p.n !== f.stacks("blessing") || p.collect !== true) badN++; }
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    P.resolveHit = function(...a){ const d0 = f.holyTally ? f.holyTally.discs : 0; inH++;
      try { return oH.apply(this, a); } finally { inH--; if (f.holyTally) discs += f.holyTally.discs - d0; } };
    P.tickHolyGround = function(dt){ const b0 = f.holyTally ? f.holyTally.bless : 0; inG++;
      try { return oG.call(this, dt); } finally { inG--; if (f.holyTally) blessings += f.holyTally.bless - b0; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { P.resolveHit = oH; P.tickHolyGround = oG; if (had) S.play = op; else delete S.play; }
    const fr = (x) => [x.hp, x.shield, x.x, x.y, x.vx, x.vy, x.stun, x.alive, x.hits, x.dealt,
                       x.stacks("smite"), x.stacks("blessing"), x.holyTally ? JSON.stringify(x.holyTally) : null];
    const T = f.holyTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.holyT, JSON.stringify(m.holyGround), fr(m.a), fr(m.b),
                                    m.winner ? m.winner.w.id : null]),
               other: JSON.stringify(other), casts: T.casts || 0, discs, blessings,
               castV: log.filter(x => x === "cast").length, discV: log.filter(x => x === "disc").length,
               healV: log.filter(x => x === "heal").length, badN, stray });
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
  for (const [k, kind, p] of [["cast", "ult", { w: "censer" }], ["disc", "ult", { w: "censer-disc", n: 3 }],
                              ["heal", "spark", { collect: true, n: 3 }], ["hit", "hit", { dmg: 25.5, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""


# ============================================================ MEASURING ====
def _rms(v):
    return math.sqrt(float((v ** 2).mean())) if len(v) else 0.0


def noise_part(draws, a, b):
    """The noise-built part of a voice over [a, b] s after the event, re the
    whole voice there (dB): renders of one text on two noise draws differ by
    exactly the part built from the noise buffer, so (x1 - x2) / sqrt 2 is it
    (angelus_voice_lab's, portcullis's STONE method), the median over six
    disjoint pairs. A voice of sines alone reads the render floor (-180)."""
    np = _np()
    i0, i1 = int((T0 + a) * SR), int((T0 + b) * SR)
    out = []
    for i in range(0, len(draws) - 1, 2):
        n = (draws[i] - draws[i + 1])[i0:i1] / math.sqrt(2)
        rn = _rms(n)
        out.append(db(rn / max(_rms(draws[i][i0:i1]), 1e-12)) if rn > 1e-9 else -180.0)
    return float(np.median(out))


def onsets_seg(y):
    """ONSETS (lightkeeper_voice_lab's, v107, unchanged but for taking the
    segment): 1 ms RMS peaks >= 15 ms apart, each >= 0.3 of the loudest and
    >= 6 dB over the minimum since the previous onset (or the start). ms."""
    np = _np()
    H = int(0.001 * SR); n = len(y) // H
    if n < 3:
        return []
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


def strike_of(x, fc=600.0, secs=1.2):
    """STRIKE: the first 1 ms (s after the event) at which the voice low-passed
    at `fc` reaches half its loudest, and that loudest re the whole voice's
    1 ms peak (a voice with no bell has nothing there)."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + secs) * SR)]
    yl = lowpass_fft(y, fc)
    H = int(0.001 * SR); n = len(y) // H
    el = np.sqrt((yl[:n * H].reshape(n, H) ** 2).mean(axis=1))
    ea = np.sqrt((y[:n * H].reshape(n, H) ** 2).mean(axis=1))
    i = int(np.argmax(el >= 0.5 * el.max()))
    return i / 1000.0, db(float(el.max()) / max(float(ea.max()), 1e-12))


def centroid_seg(y):
    np = _np()
    P = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float((P * fr).sum() / max(P.sum(), 1e-30))


def spec_peaks(x, a, b, lo=50.0, hi=4000.0, within=20.0):
    """PEAKS: the spectral peaks over [a, b] s (absolute; Hann, zero-padded)
    within `within` dB of the strongest in [lo, hi], merged within 2% (the
    stronger kept), ascending: [(Hz, amplitude)]."""
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    m = np.nonzero((fr >= lo) & (fr <= hi))[0]
    Xm = X[m]; top = float(Xm.max())
    pk = [k for k in range(1, len(m) - 1) if Xm[k] >= Xm[k - 1] and Xm[k] > Xm[k + 1]
          and Xm[k] >= top * 10 ** (-within / 20)]
    out = []
    for k in sorted(pk, key=lambda k: -Xm[k]):
        f = float(fr[m[k]])
        if all(abs(math.log(f / g_)) > 0.02 for g_, _ in out):
            out.append((f, float(Xm[k])))
    return sorted(out)


def late_onsets(x, st, secs=0.6, fc=2000.0):
    """The rattle's onsets AFTER the strike (+30 ms): 1 ms RMS peaks of the
    voice high-passed (FFT) at `fc`, >= 15 ms apart, each >= 0.3 of the
    rattle's loudest before the strike (of the whole, if nothing came
    before). A rattle that leads INTO the bell has none."""
    np = _np()
    y = x[int(T0 * SR):int((T0 + secs) * SR)]
    yh = y - lowpass_fft(y, fc)
    H = int(0.001 * SR); n = len(y) // H
    e = np.sqrt((yh[:n * H].reshape(n, H) ** 2).mean(axis=1))
    i0 = int(round(st * 1000))
    ref = float(e[:i0].max()) if i0 > 20 else float(e.max())
    got = []
    for i in range(max(1, i0 + 30), n - 1):
        if e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] >= 0.3 * ref and (not got or i - got[-1] >= 15):
            got.append(i)
    return len(got)


def bell_of(peaks):
    """BELL: (the lowest peak Hz, the strongest peak Hz, the most cents any
    other peak lies off every whole multiple of the lowest, how many peaks)."""
    if not peaks:
        return 0.0, 0.0, 0.0, 0
    f0 = peaks[0][0]
    fs = max(peaks, key=lambda z: z[1])[0]
    inh = 0.0
    for f, _a in peaks[1:]:
        k = max(1, round(f / f0))
        inh = max(inh, abs(cents(f, k * f0)))
    return f0, fs, inh, len(peaks)


def low_after(x, a, fc=500.0):
    """The share of the power over [a, end] (absolute s) under fc."""
    np = _np()
    y = x[int(a * SR):]
    P = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float(P[fr < fc].sum() / max(P.sum(), 1e-30))


def heard_at(x, a, p90, win=0.1, lo=PHONE_HZ, hi=12000.0):
    """HEARD over [a, a + win] (absolute s): ironhail's reading moved off the
    voice's start -- the loudest ratio of its third-octaves at or above `lo` to
    the score's p90 in the same third-octave (p90 read over `win`), dB, and
    where."""
    b = bands(x[int(a * SR):int(a * SR) + int(win * SR)])
    best = max(((b[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))
    return db(best[0]), best[1]


def top_between(x, a, b):
    """The loudest 50 ms (5 ms hop) whose window lies inside [a, b] s after the event."""
    np = _np()
    y = x[int((T0 + a) * SR):int((T0 + b) * SR)]
    if len(y) < int(0.05 * SR) + 2:
        return 0.0
    r, _ = env(y, 0.05)
    return float(r.max())


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v78 section 4 turned into a number; a rule
# no candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.5s': AUDIBLE 415-585 ms (v100's +/-17.5%); 'a chain-rattle': before the "
    "bell's STRIKE at least 5 ONSETS (a rattle of links, not one knock), its "
    "centroid >= 2500 Hz (small metal), its loudest 50 ms 3-12 dB under the "
    "bell's (heard, and leading into it) and its best third-octave over the 100 "
    "ms before the strike >= 2x the score's p90 there; 'into a low bell': a bell "
    "there (the voice low-passed at 600 Hz peaks within 12 dB of the voice), "
    "STRUCK at 150-280 ms, after every onset of the rattle; LOW: its strongest "
    "peak (strike + 20-200 ms) <= 500 Hz and >= 0.5 of its power (strike to end) "
    "under 500 Hz; a BELL: a peak within 20 dB of its strongest lies >= 60 cents "
    "off every whole multiple of its lowest (a harmonic tone is not a bell); "
    "heard: its best third-octave at or above 200 Hz over the strike's first 100 "
    "ms >= 2x the score's p90 there (a phone plays it). Level: TOP between 0.5x "
    "the blow's (hit @ 25.5) loudest 50 ms on its loudest draw and 1.0x on its "
    "quietest, on every noise draw. Register against rune-crack, the school's "
    "and the type's casts with a voice of their own, the seal, the death voice, "
    "the clank, the blow and every peer voice (--peer-rows) each <= 0.80. "
    "Tiebreak: the lowest worst register (to 0.05), then the fewest synth calls, "
    "then the order listed.")

DISC_RULE = (
    "At EVERY count 1-5: 'a ... bell tone': a BELL (a peak within 20 dB of the "
    "strongest >= 60 cents off every whole multiple of the lowest, 5-150 ms) "
    "that rings (AUDIBLE 250-600 ms); 'soft': pure (the noise part <= -30 dB re "
    "the whole: no clack), mellow (the centroid <= 2x the note), and quiet: its "
    "loudest 50 ms <= 0.5x the blow's (hit @ 25.5) on its quietest draw and >= "
    "2x the wall tick's on its loudest; 'pitch by disc count': each count's note "
    "(the strongest peak 300-2000 Hz, 5-100 ms) within 30 cents of its declared "
    "degree, and every step n -> n + 1 >= 150 cents up; heard: at count 1 the "
    "note's third-octave over 0-100 ms >= 2x the score's p90 there, and at every "
    "count OVER the heaviest blow's voice (hit @ 45, its loudest draw) on the "
    "same frame, both through the chain: the note's third-octave over 0-200 ms "
    ">= +6 dB over the blow alone. Register (the worst count, the median over "
    "noise draws) against the heal chime (spark collect n 1-5), Zenith's tick "
    "(n 0-4), the wall tick, hex-snap, the blow, rune-crack, the picked cast and "
    "every peer voice each <= 0.80. Tiebreak: the lowest worst register (to "
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
    if not 415 <= M["aud"] <= 585: why.append(f"audible {M['aud']:.0f} ms, not 415-585")
    if M["bell_db"] < -12:
        why.append(f"no bell (under 600 Hz it peaks {M['bell_db']:+.1f} dB re the voice)")
    if not 0.150 <= M["strike"] <= 0.280: why.append(f"the strike at {M['strike'] * 1000:.0f} ms, not 150-280")
    if M["n_on"] < 5: why.append(f"no rattle: {M['n_on']} onsets before the strike (< 5)")
    if M["late_on"]: why.append(f"{M['late_on']} rattle onsets after the strike (not 'into')")
    if M["r_cen"] < 2500: why.append(f"the rattle's centroid {M['r_cen']:.0f} Hz (< 2500: not small metal)")
    if not 3 <= M["r_under"] <= 12: why.append(f"the rattle {M['r_under']:+.1f} dB under the bell, not 3-12")
    if M["r_heard"] < 6: why.append(f"the rattle under the score ({M['r_heard']:+.1f} dB re its p90)")
    if M["b_strong"] > 500: why.append(f"not low: the bell's strongest peak {M['b_strong']:.0f} Hz > 500")
    if M["b_low"] < 0.5: why.append(f"not low: {M['b_low']:.2f} of its power under 500 Hz")
    if M["b_inh"] < 60: why.append(f"not a bell: every peak within {M['b_inh']:.0f} c of a harmonic")
    if M["b_heard"] < 6: why.append(f"the bell under the score ({M['b_heard']:+.1f} dB re its p90)")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"too loud: top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def disc_why(M, lev):
    why = []
    if M["aud_lo"] < 250 or M["aud_hi"] > 600:
        why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 250-600 (it does not ring as a bell)")
    if M["inh"] < 60: why.append(f"not a bell (worst count: every peak within {M['inh']:.0f} c of a harmonic)")
    if M["nz"] > -30: why.append(f"not pure: a noise part of {M['nz']:+.1f} dB (a clack)")
    if M["cen_x"] > 2.0: why.append(f"not mellow: the centroid {M['cen_x']:.2f}x the note")
    if M["top_hi"] > lev["hi"]: why.append(f"too loud: loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["note_err"] > 30: why.append(f"a note {M['note_err']:.0f} cents off its degree")
    if M["step_min"] < 150: why.append(f"a step of {M['step_min']:+.0f} cents (< 150)")
    if M["heard1"] < 6: why.append(f"count 1 under the score ({M['heard1']:+.1f} dB re its p90)")
    if M["over_blow"] < 6: why.append(f"under the blow on its frame ({M['over_blow']:+.1f} dB, the worst count)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


NAMES = {"hit": "the blow", "wall": "the wall tick", "death": "the death voice", "seal": "the seal",
         "rune-crack": "rune-crack", "hex-snap": "the runic snap", "cast": "the cast", "spark": "the heal chime",
         "zenith-tick": "Zenith's tick", "clank": "the clank"}


def who(regs):
    k = max(regs, key=regs.get)
    if k.startswith("peer:"):
        rel, _, sub = k[5:].partition("-")
        return f"{rel.capitalize()}'s {sub or 'cast'}, on the batch line"
    return NAMES.get(k, k[0].upper() + k[1:] + "'s cast")


CAST_WORDS = {
    "1 CHURCH": "nine links of the chain pinged (two sines, 1 : 1.47, at 3.3-6.1 kHz, and a tick of noise), rising in "
                "level, then a church bell struck on A: hum A2, prime A3, tierce, quint and nominal A4, with the "
                "clapper's knock",
    "2 DEEP": "nine links of the chain pinged (two sines, 1 : 1.47, at 3.3-6.1 kHz, and a tick of noise), rising in "
              "level, then a church bell struck on E: hum E2, prime E3, tierce, quint and nominal E4, with the "
              "clapper's knock",
    "3 BRONZE": "nine links of the chain pinged (two sines, 1 : 1.47, at 3.3-6.1 kHz, and a tick of noise), rising in "
                "level, then a church bell struck on A with its upper partials: hum A2, prime A3, tierce, quint, "
                "nominal A4, and 2.5, 3 and 4x the prime, with the clapper's knock",
    "4 JINGLE": "nine links of the chain ringing as bands of noise (Q 6, 30 ms, 3.3-6.1 kHz), rising in level, then a "
                "church bell struck on A: hum A2, prime A3, tierce, quint and nominal A4, with the clapper's knock",
    "5 SWING": "nine links of the chain pinged (two sines, 1 : 1.47, at 3.3-6.1 kHz, and a tick of noise), quickening "
               "from 36 ms apart to 12 and rising in level as the censer swings down, then a church bell struck on "
               "A: hum A2, prime A3, tierce, quint and nominal A4, with the clapper's knock",
}
DISC_WORDS = {
    "1 CHAPEL": "a small church bell (sines on its hum, prime, tierce, quint and nominal)",
    "2 BOWL": "a struck bowl (two sines on its 1 : 2.71 modes, the upper at 0.3 and dying half as long)",
    "3 CUP": "a cup bell (sines on its 1 : 2.32 : 3.9 modes)",
    "4 LOW": "a small church bell (sines on its hum, prime, tierce, quint and nominal)",
    "5 HIGH": "a small church bell (sines on its hum, prime, tierce, quint and nominal)",
}


def arms_code(C_, K_, info):
    names = [X["name"].split()[1] for X in (C_, K_)]
    c_cast = _wrap([
        f'CENSER\'S CAST, THE SWING -- v78 s4: "a thurible swing (a chain-rattle into a low bell, 0.5s)". '
        f'{names[0]}, of {info["n_cast"]}, picked on the numbers by `censer_voice_lab.py` under Rick\'s "you '
        f'pick i overrule" (v109). Censer had no arm and fell through to rune-crack, which other relics still '
        f'use, so this ADDS arms before that fallback and leaves it alone.',
        f"{CAST_WORDS[C_['name']][0].upper() + CAST_WORDS[C_['name']][1:]}. The bell struck "
        f"{C_['strike'] * 1000:.0f} ms in, after "
        f"{C_['n_on']} onsets of the rattle ({C_['r_under']:.1f} dB under it, centroid {C_['r_cen']:.0f} Hz); "
        f"audible {C_['aud']:.0f} ms; the bell's strongest peak {C_['b_strong']:.0f} Hz, {100 * C_['b_low']:.0f}% "
        f"of its power under 500 Hz; loudest 50 ms {info['c_top']:+.1f} dB re Censer's own blow. Register at "
        f"most {info['c_reg']:.2f} ({info['c_regw']}) against rune-crack, the school's and the warhammers' "
        f"casts, the seal, the death voice, the clank, the blow and the batch line's other voices."], 10)
    notes = " ".join(note_name(f) for f in disc_notes(K_["sp"]))
    c_disc = _wrap([
        f'A DISC OPENING -- "a soft bell tone, pitch by disc count" (v78 s4). {names[1]}, of {info["n_disc"]} '
        f"(`censer_voice_lab.py`). `resolveHit` plays it once per disc planted, on the blow's frame, with `n`, "
        f"the caster's discs standing on the ground after the push.",
        f"{DISC_WORDS[K_['name']][0].upper() + DISC_WORDS[K_['name']][1:]}: one step of the score's A minor "
        f"pentatonic a disc, "
        f"{notes} (counts clamped to 1..{CAP}). Audible "
        + (f"{K_['aud_lo']:.0f}" if round(K_['aud_lo']) == round(K_['aud_hi'])
           else f"{K_['aud_lo']:.0f}-{K_['aud_hi']:.0f}")
        + f" ms at every count; its loudest "
        f"50 ms {info['d_db']:+.1f} dB re the blow and {info['d_wall']:+.1f} dB re the wall tick; over the "
        f"heaviest blow on its frame by {K_['over_blow']:+.1f} dB or more in its note's third-octave. Register "
        f"at most {info['d_reg']:.2f} ({info['d_regw']}) against the heal chime that follows it, Zenith's tick, "
        f"the wall tick, the runic snap, the blow, rune-crack, the cast and the batch line's other voices."], 10)
    return (f'        }} else if (w === "censer"){{                     // the censer swings\n'
            f'{c_cast}\n{cast_body(C_["sp"], C_["g"], C_["kr"], C_["D"])}\n'
            f'        }} else if (w === "censer-disc"){{                // and the ground is consecrated\n'
            f'{c_disc}\n{disc_body(K_["sp"], K_["g"], K_["D"])}\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True,
                    help="a link carrying Censer's stage 5 and none of its voices (v109 ran on the scratch link "
                         "sc-censer-consecration-b25.5.html, 56c49ad3f0ccb3aa)")
    ap.add_argument("--out", default="../05-reference/v109")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=109601)
    ap.add_argument("--e2e-seeds", type=int, default=1, help="fight seeds a pairing, end to end (0 skips it)")
    ap.add_argument("--peer-rows", action="append", default=[],
                    help="another relic's stage-6 voice rows_final.json: co-apply its Sfx rows with these, and "
                         "gate the registers against its voices")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    ap.add_argument("--no-wire", action="store_true", help="the voices only (iteration)")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "disc": DISC_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("resolveHit disc push", DISC_ANCHOR),
                    ("tickHolyGround blessing", HEAL_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("censer-disc", '(w === "censer")'):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    if 'u.kind === "holyground"' not in html or "tickHolyGround(dt){" not in html:
        raise SystemExit(f"{gp.name} does not carry Censer's Consecration")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nCONSECRATION -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
        row = page.evaluate("() => { const w = AC.WEAPONS.find(w => w.id === 'censer'); "
                            "return w ? [w.dmg, w.aff, w.shape, w.ult.kind, w.ult.groundR, w.ult.groundLife, "
                            "w.ult.bless, w.mass, AC.STATUS ? AC.STATUS.blessing.maxStacks : null] : null; }")
        print(f"  the row: dmg {row[0]}, {row[1]} {row[2]}, kind {row[3]}, groundR {row[4]}, groundLife {row[5]} s, "
              f"bless {row[6]}, mass {row[7]}; blessing cap {row[8]}")
        if row[0] != BLADE or row[3] != "holyground" or row[1] != SCHOOL_AFF or row[2] != TYPE_SHAPE:
            raise SystemExit("the row is not the one this lab was written for (blade 25.5, holyground, "
                             "sanctified warhammer)")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        if play_src.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx anchor is not in play() exactly once")
        kinds = sorted(set(re.findall(r'kind === "([a-z-]+)"', play_src)))
        print(f"  THE SYNTH'S KINDS TODAY ({len(kinds)}): {', '.join(kinds)}")
        rec["kinds"] = kinds
        wpn = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape])")

        def R(evs, secs=3.0, seed=None, rows=None, new=True):
            for e in evs:
                if e[0] == "body":
                    _refuse(e[2], "candidate")
            r = page.evaluate(RENDER_JS, [evs, secs, seed, rows])
            assert not errors, errors[:3]
            x = pcm(r)
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

        def play(kind, p, seed=None):
            return R([["play", T0, kind, p]], seed=seed, new=False)[0]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms and hit@11.6 0.443 / 80 ms. They must come back.")
        x_fb = play("ult", {"w": "__no_such_relic__"})
        own = {}
        for wid, aff, shp in wpn:
            if wid == ME:
                continue
            xw_ = play("ult", {"w": wid})
            own[wid] = float(np.abs(xw_ - x_fb).max())
        FALL = [k for k, v in own.items() if v <= 1e-6]
        SCHOOL = [w_[0] for w_ in wpn if w_[0] != ME and w_[1] == SCHOOL_AFF and own[w_[0]] > 1e-6]
        TYPES = [w_[0] for w_ in wpn if w_[0] != ME and w_[2] == TYPE_SHAPE and own[w_[0]] > 1e-6]
        print(f"  relics falling through to rune-crack today ({len(FALL)} besides Censer): {', '.join(FALL)}")
        print(f"  with a voice of their own -- the school ({SCHOOL_AFF}): {', '.join(SCHOOL) or 'none'}; the type "
              f"({TYPE_SHAPE}): {', '.join(TYPES) or 'none'}")
        xa0 = play("ult", {"w": ME})
        now_fb = float(np.abs(xa0 - x_fb).max())
        print(f"  ult/censer today vs the fallback: max |diff| {now_fb:.1e} -- "
              f"{'it IS rune-crack' if now_fb <= 1e-6 else 'NOT the fallback'}")
        if now_fb > 1e-6:
            raise SystemExit("ult/censer is not the rune-crack fallback -- this lab was written for a relic with no arm")
        rec.update(fallthrough=FALL, school=SCHOOL, types=TYPES)
        REFS = {"rune-crack": ("ult", {"w": "__no_such_relic__"}), "hit@11.6": ("hit", {"dmg": 11.6, "crit": False}),
                "hit": ("hit", {"dmg": BLADE, "crit": False}), "hit@45": ("hit", {"dmg": HEAVY, "crit": False}),
                "hit@45!": ("hit", {"dmg": HEAVY, "crit": True}), "hit@33": ("hit", {"dmg": MID, "crit": False}),
                "wall": ("wall", {}), "death": ("death", {}), "seal": ("seal", {}), "clank": ("clank", {"mass": 5.0}),
                "hex-snap": ("hex-snap", {})}
        REFS.update({f"spark{n}": ("spark", {"collect": True, "n": n}) for n in range(1, 6)})
        REFS.update({f"zt{n}": ("ult", {"w": "morningstar-tick", "n": n}) for n in range(0, 5)})
        REFS.update({w_: ("ult", {"w": w_}) for w_ in SCHOOL + TYPES})
        ctl = {}
        for name, (kind, p) in REFS.items():
            x = play(kind, p)
            ctl[name] = dict(basic(x), x=x)
        for name in ("rune-crack", "hit@11.6", "hit", "hit@45", "wall", "death", "seal", "clank", "spark3", "zt2"):
            M = ctl[name]
            print(f"  {name:<11} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
                  f"loudest 50 ms {M['top']:.4f}   centroid {M['cen']:6.0f} Hz")
        repro = [("rune-crack peak", ctl["rune-crack"]["peak"], 0.608, 0.01),
                 ("rune-crack audible", ctl["rune-crack"]["aud"], 450, 10),
                 ("hit@11.6 peak", ctl["hit@11.6"]["peak"], 0.443, 0.01),
                 ("hit@11.6 audible", ctl["hit@11.6"]["aud"], 80, 10)]
        bad = [f"{n}: {v:.3f} vs {p_}" for n, v, p_, t_ in repro if abs(v - p_) > t_]
        print("  reproduction: " + ("FAIL -- " + "; ".join(bad) if bad else
                                    f"PASS  all {len(repro)} published numbers come back"))
        if bad:
            raise SystemExit("the controls do not reproduce -- nothing new is quoted")
        # the noise draws of every reference
        D = {k: [] for k in REFS}
        RX = {k: [] for k in ("hit@45",)}
        for sd in NOISE_SEEDS:
            for k, (kind, p) in REFS.items():
                x = play(kind, p, seed=sd)
                D[k].append(basic(x))
                if k in RX:
                    RX[k].append(x)
        h_lo, h_hi = min(m_["top"] for m_ in D["hit"]), max(m_["top"] for m_ in D["hit"])
        w_hi = max(m_["top"] for m_ in D["wall"])
        hv_i = int(np.argmax([m_["top"] for m_ in D["hit@45"]]))
        HEAVY_SEED = NOISE_SEEDS[hv_i]
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f};  the hit "
              f"@ {HEAVY:g}: {min(m_['top'] for m_ in D['hit@45']):.4f}-{max(m_['top'] for m_ in D['hit@45']):.4f} "
              f"(its loudest draw: seed #{hv_i});  the wall tick: {min(m_['top'] for m_ in D['wall']):.4f}-{w_hi:.4f}")
        RB = {k: [m_["bands"] for m_ in v] for k, v in D.items()}
        # the batch line's other voices, from their own rows
        peer_regs = []
        peer_rows_ok = []
        for pf, prow in peer_sfx:
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            if not ps:
                continue
            peer_rows_ok.append((pf, ps))
            pids = sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _, c in ps))))
            for w_ in pids:
                RB["peer:" + w_] = [bands(R([["arm", T0, "ult", {"w": w_, "n": 3, "k": 1, "shield": 45}]], rows=ps,
                                            seed=sd, new=False)[0][int(T0 * SR):]) for sd in NOISE_SEEDS]
                peer_regs.append("peer:" + w_)
        if peer_regs:
            print(f"  the batch line's other voices, from --peer-rows ({len(peer_regs)}): "
                  f"{', '.join(r_[5:] for r_ in peer_regs)}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]
        p90b = bed_p90(bseg, 0.1, 0.05)

        def bedp90(f, dur=0.1):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + dur)
                                        for i in range(0, len(bseg) - int(dur * SR), 2400)], 90))

        def reg(DB, key):
            DK = RB[key]
            if len(DB) == 1 or len(DK) == 1:
                return float(np.median([cos(p_, q_) for p_ in DB for q_ in DK]))
            return float(np.median([cos(DB[i], DK[i]) for i in range(min(len(DB), len(DK)))]))

        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, heavy_seed=HEAVY_SEED)
        wav("censer-ctl-runecrack.wav", ctl["rune-crack"]["x"])
        wav("censer-ctl-hit25.wav", ctl["hit"]["x"])
        wav("censer-ctl-hit45.wav", ctl["hit@45"]["x"])
        wav("censer-ctl-wall.wav", ctl["wall"]["x"])
        wav("censer-ctl-heal-n3.wav", ctl["spark3"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a thurible swing (a chain-rattle into a low bell, 0.5s)'. Level-matched: TOP {tgt_c:.4f} (the "
              f"centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the rattle {RATTLE_UNDER_DB:g} dB under the bell, "
              f"AUDIBLE {CAST_AUD:g} ms")

        def cx(sp, g, kr, D_, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kr, D_, part=part), {}]], seed=seed)

        def calib_cast(sp, aud=CAST_AUD):
            g, kr, D_ = 0.05, 0.5, 0.3
            for _ in range(4):
                lo_, hi_ = math.log(0.03), math.log(6.0)
                for _ in range(13):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, kr, math.exp(mid))[0])["aud"] < aud: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                tb = basic(cx(sp, g, kr, D_, part="bell")[0])["top"]
                tr = basic(cx(sp, g, kr, D_, part="rattle")[0])["top"]
                kr = kr * 10 ** ((db(tb) - RATTLE_UNDER_DB - db(tr)) / 20)
                g = g * tgt_c / basic(cx(sp, g, kr, D_)[0])["top"]
            return float(f"{g:.4g}"), float(f"{kr:.4g}"), D_

        CAST_REGS = ["rune-crack"] + SCHOOL + TYPES + ["seal", "death", "clank", "hit"] + peer_regs

        def cast_measure(fn, name, sp, g, kr, D_, blurb, calls=None):
            """fn(seed) -> the voice rendered on that noise draw."""
            x = fn(None)
            if float(np.abs(x - fn(None)).max()) > TOL:
                raise SystemExit(f"cast {name} does not reproduce")
            M = basic(x); M.update(x=x, name=name, sp=sp, g=g, kr=kr, D=D_, blurb=blurb, calls=calls)
            st, bdb = strike_of(x)
            M["strike"], M["bell_db"] = st, bdb
            y = x[int(T0 * SR):int((T0 + max(st - 0.005, 0.0)) * SR)]
            on = onsets_seg(y) if len(y) > int(0.02 * SR) else []
            M["n_on"] = len(on)
            M["late_on"] = late_onsets(x, st)
            M["r_cen"] = centroid_seg(y) if len(y) > 64 else 0.0
            rt = top_between(x, 0.0, max(st - 0.005, 0.0))
            bt = top_between(x, st, 1.5)
            M["r_under"] = db(bt / max(rt, 1e-12)) if rt > 0 else 99.0
            M["r_heard"] = heard_at(x, T0 + max(st - 0.105, 0.0), p90b)[0] if st >= 0.02 else -99.0
            pk = spec_peaks(x, T0 + st + 0.02, T0 + st + 0.2)
            f0, fs, inh, npk = bell_of(pk)
            M.update(b_f0=f0, b_strong=fs, b_inh=inh, b_npk=npk, b_low=low_after(x, T0 + st))
            M["b_heard"], M["b_heard_f"] = heard_at(x, T0 + st, p90b)
            M["phone_db"] = db(phone(x) / M["top"])
            draws = [fn(sd) for sd in NOISE_SEEDS]
            tops = [basic(d_)["top"] for d_ in draws]
            M["top_lo"], M["top_hi"] = min(tops), max(tops)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: reg(DB, k) for k in CAST_REGS}
            M["why"] = cast_why(M, lev_c)
            r_ = M["regs"]
            print(f"  {name:<10}{g:>8.4g}{kr:>7.3g}{D_:>6.3g}{(calls or 0):>6d}{M['aud']:>5.0f}{st * 1000:>5.0f}"
                  f"{bdb:>6.1f}{M['n_on']:>4d}{M['r_cen']:>6.0f}{M['r_under']:>6.1f}{M['r_heard']:>6.1f}"
                  f"{fs:>6.0f}{M['b_low']:>5.2f}{inh:>5.0f}{M['b_heard']:>6.1f}{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}"
                  f"{M['phone_db']:>6.1f}  worst reg {max(r_.values()):.2f} ({max(r_, key=r_.get)})")
            return M

        print(f"  {'cand':<10}{'g':>8}{'kr':>7}{'D':>6}{'calls':>6}{'aud':>5}{'strk':>5}{'bell':>6}{'ons':>4}"
              f"{'r cen':>6}{'r und':>6}{'r hrd':>6}{'b pk':>6}{'b lo':>5}{'inh':>5}{'b hrd':>6}{'top lo':>8}"
              f"{'top hi':>8}{'phone':>6}")
        rows_c = []
        for name, sp, blurb in CAST_CANDIDATES:
            g, kr, D_ = calib_cast(sp)
            calls = cx(sp, g, kr, D_)[1][0]
            M = cast_measure(lambda sd, sp=sp, g=g, kr=kr, D_=D_: cx(sp, g, kr, D_, seed=sd)[0], name, sp, g, kr,
                             D_, blurb, calls)
            M["ms"] = None
            rows_c.append(M)
            wav(f"censer-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for name, sp, blurb in CAST_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    registers (" + ", ".join(k.replace("peer:", "") for k in CAST_REGS) + "):")
        for M in rows_c:
            print(f"    {M['name']:<10} " + " ".join(f"{v:.2f}" for v in M["regs"].values()))
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, kr {C_['kr']}, D {C_['D']}; {C_['calls']} synth calls; TOP "
              f"{C_['top']:.4f} = {db(C_['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g} (quietest draw), "
              f"{db(C_['top'] / w_hi):+.1f} dB re the wall")
        # the controls, built on the PICK: each must fail its OWN gate
        ctlc = []
        s0 = C_["sp"]
        CCTL = [("0 BELL", dict(part="bell"), ["no rattle"]),
                ("0 RATTLE", dict(part="rattle"), ["no bell", "not low", "not a bell"]),
                ("0 HIGH", dict(sp=dict(s0, f=s0["f"] * 4)), ["not low"]),
                ("0 HARM", dict(sp=dict(s0, harm=True)), ["not a bell"]),
                ("0 LONG", dict(aud=1500.0), ["audible"]),
                ("0 AFTER", dict(sp=dict(s0, strike=0.0, rattle_at=STRIKE)), ["strike", "into"])]
        for name, kw, own_ in CCTL:
            sp = kw.get("sp", s0)
            g, kr, D_ = C_["g"], C_["kr"], C_["D"]
            if "aud" in kw:
                lo_, hi_ = math.log(0.03), math.log(8.0)
                for _ in range(13):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(cx(sp, g, kr, math.exp(mid))[0])["aud"] < kw["aud"]: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
            part = kw.get("part", "both")
            M = cast_measure(lambda sd, sp=sp, g=g, kr=kr, D_=D_, part=part: cx(sp, g, kr, D_, part=part, seed=sd)[0],
                             name, sp, g, kr, D_, "", cx(sp, g, kr, D_, part=part)[1][0])
            M["own"] = own_
            ctlc.append(M)
            wav(f"censer-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        M = cast_measure(lambda sd: play("ult", {"w": ME}, seed=sd), "0 RC-NOW", None, 0, 0, 0, "", 5)
        M["own"] = [""]
        ctlc.append(M)
        print("    0 BELL     the pick's bell alone, no rattle -- a control\n"
              "    0 RATTLE   the pick's rattle alone, no bell -- a control\n"
              "    0 HIGH     the pick with its bell two octaves up -- a control\n"
              "    0 HARM     the pick with its bell's partials on whole multiples of its lowest -- a control\n"
              "    0 LONG     the pick's bell ringing 1.5 s -- a control\n"
              "    0 AFTER    the pick's bell struck first, its rattle after it -- a control\n"
              "    0 RC-NOW   what ult/censer plays today (rune-crack) -- a control")
        for M in ctlc:
            hit_own = any(o_ in w_ for o_ in M["own"] for w_ in M["why"])
            if M["why"] and hit_own:
                print(f"  {M['name']} (a control) comes back wrong on its own gate, as it must: "
                      f"{'; '.join(w_ for w_ in M['why'] if any(o_ in w_ for o_ in M['own']))[:200]}")
            else:
                print(f"  {M['name']} (a control) did NOT fail its own gate ({'; '.join(M['why'])[:160] or 'passed'}) "
                      f"-- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")

        # ---- THE DISC ------------------------------------------------------
        lev_d = dict(lo=2 * w_hi, hi=0.5 * h_lo)
        tgt_d = math.sqrt(lev_d["lo"] * lev_d["hi"])
        print(f"\nDISC -- 'a soft bell tone, pitch by disc count'. Level-matched: loudest 50 ms {tgt_d:.4f} at count "
              f"{DISC_REF_N} (the centre of {lev_d['lo']:.4f}-{lev_d['hi']:.4f}), AUDIBLE {DISC_AUD:g} ms at count "
              f"{DISC_REF_N}; over the blow: the hit @ {HEAVY:g} on its loudest draw")

        def dx(sp, g, D_, n, seed=None):
            return R([["body", T0, disc_body(sp, g, D_), {"n": n}]], seed=seed)

        def calib_disc(sp, aud=DISC_AUD):
            g, D_ = 0.02, 0.4
            for _ in range(4):
                lo_, hi_ = math.log(0.01), math.log(4.0)
                for _ in range(13):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(dx(sp, g, math.exp(mid), DISC_REF_N)[0])["aud"] < aud: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
                g = g * tgt_d / basic(dx(sp, g, D_, DISC_REF_N)[0])["top"]
            return float(f"{g:.4g}"), D_

        SPARKS = [f"spark{n}" for n in range(1, 6)]
        ZTS = [f"zt{n}" for n in range(5)]
        x_heavy = play("hit", {"dmg": HEAVY, "crit": False}, seed=HEAVY_SEED)
        x_heavy_c = play("hit", {"dmg": HEAVY, "crit": True}, seed=HEAVY_SEED)
        x_mid = play("hit", {"dmg": MID, "crit": False}, seed=HEAVY_SEED)
        RB["cast"] = C_["DB"]
        DREGS = ["spark", "zenith-tick", "wall", "hex-snap", "hit", "rune-crack", "cast"] + peer_regs

        def disc_measure(sp, g, D_, name, blurb, fn=None):
            """fn(n, seed) -> the voice at count n on that draw (default: the candidate's text)."""
            fn = fn or (lambda n, seed=None: dx(sp, g, D_, n, seed=seed)[0])
            M = dict(name=name, sp=sp, g=g, D=D_, blurb=blurb)
            want = disc_notes(sp) if not sp.get("spark") else [1180 + n * 110 for n in range(1, 6)]
            notes, auds, tops, cenx, inhs, nzs, ob, obc, obm = [], [], [], [], [], [], [], [], []
            regs = {k: 0.0 for k in DREGS}
            xs = {}
            for n in range(1, 6):
                x = fn(n)
                if float(np.abs(x - fn(n)).max()) > TOL:
                    raise SystemExit(f"disc {name} does not reproduce")
                xs[n] = x
                b_ = basic(x)
                auds.append(b_["aud"])
                f_ = pitch(x, T0 + 0.005, T0 + 0.1, lo=300, hi=2000)
                notes.append(f_)
                cenx.append(b_["cen"] / f_)
                inhs.append(bell_of(spec_peaks(x, T0 + 0.005, T0 + 0.15))[2])
                draws = [fn(n, sd) for sd in NOISE_SEEDS]
                tt = [basic(d_)["top"] for d_ in draws]
                tops += [min(tt), max(tt)]
                nzs.append(noise_part(draws, 0.0, 0.1))
                DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
                regs["spark"] = max(regs["spark"], max(reg(DB, k) for k in SPARKS))
                regs["zenith-tick"] = max(regs["zenith-tick"], max(reg(DB, k) for k in ZTS))
                for k in ("wall", "hex-snap", "hit", "rune-crack", "cast") + tuple(peer_regs):
                    regs[k] = max(regs[k], reg(DB, k))
                if n == 1:
                    M["heard1"] = db(band_rms(x, f_, T0, T0 + 0.1) / bedp90(f_, 0.1))
                # over the heaviest blow on the same frame (both through the chain)
                wn = want[n - 1]
                xb = R([["body", T0, disc_body(sp, g, D_), {"n": n}], ["play", T0, "hit", {"dmg": HEAVY, "crit": False}]],
                       seed=HEAVY_SEED)[0] if not name.startswith("0 SPARK") else \
                    R([["play", T0, "spark", {"collect": True, "n": n}], ["play", T0, "hit", {"dmg": HEAVY, "crit": False}]],
                      seed=HEAVY_SEED, new=False)[0]
                ob.append(db(band_rms(xb, wn, T0, T0 + 0.2) / max(band_rms(x_heavy, wn, T0, T0 + 0.2), 1e-12)))
                if n in (1, 5):
                    xbc = R([["body", T0, disc_body(sp, g, D_), {"n": n}],
                             ["play", T0, "hit", {"dmg": HEAVY, "crit": True}]], seed=HEAVY_SEED)[0] \
                        if not name.startswith("0 SPARK") else xb
                    obc.append(db(band_rms(xbc, wn, T0, T0 + 0.2) / max(band_rms(x_heavy_c, wn, T0, T0 + 0.2), 1e-12)))
                    xbm = R([["body", T0, disc_body(sp, g, D_), {"n": n}],
                             ["play", T0, "hit", {"dmg": MID, "crit": False}]], seed=HEAVY_SEED)[0] \
                        if not name.startswith("0 SPARK") else xb
                    obm.append(db(band_rms(xbm, wn, T0, T0 + 0.2) / max(band_rms(x_mid, wn, T0, T0 + 0.2), 1e-12)))
                if n == DISC_REF_N:
                    M["DB"] = DB
                    M["calls"] = R([["body", T0, disc_body(sp, g, D_), {"n": n}]])[1][0]
            M["xs"] = xs; M["x"] = xs[DISC_REF_N]; M["notes"] = notes
            M["note_err"] = max(abs(cents(f_, w_)) for f_, w_ in zip(notes, want))
            M["step_min"] = min(cents(notes[i + 1], notes[i]) for i in range(4))
            M["aud_lo"], M["aud_hi"] = min(auds), max(auds)
            M["top_lo"], M["top_hi"] = min(tops), max(tops)
            M["top"] = basic(xs[DISC_REF_N])["top"]
            M["cen_x"] = max(cenx); M["inh"] = min(inhs); M["nz"] = max(nzs)
            M["over_blow"] = min(ob); M["over_blow_all"] = ob; M["over_crit"] = obc; M["over_mid"] = obm
            M["regs"] = regs
            M["why"] = disc_why(M, lev_d)
            r_ = regs
            print(f"  {name:<10}{g:>8.4g}{D_:>6.3g}{M['calls']:>6d}{M['aud_lo']:>5.0f}-{M['aud_hi']:<4.0f}{M['inh']:>5.0f}"
                  f"{M['nz']:>7.1f}{M['cen_x']:>5.2f}{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}{M['note_err']:>5.0f}"
                  f"{M['step_min']:>6.0f}{M['heard1']:>6.1f}{M['over_blow']:>6.1f}"
                  + "".join(f"{r_[k]:>6.2f}" for k in DREGS[:7])
                  + (f"  peers {max(r_[k] for k in peer_regs):.2f} ({max(peer_regs, key=lambda k: r_[k])[5:]})"
                     if peer_regs else ""))
            return M

        print(f"  {'cand':<10}{'g':>8}{'D':>6}{'calls':>6}{'aud':>10}{'inh':>5}{'noise':>7}{'cenx':>5}{'top lo':>8}"
              f"{'top hi':>8}{'err':>5}{'step':>6}{'hrd1':>6}{'oblow':>6}"
              + "".join(f"{k[:6]:>6}" for k in DREGS[:7]))
        rows_d = []
        for name, sp, blurb in DISC_CANDIDATES:
            g, D_ = calib_disc(sp)
            M = disc_measure(sp, g, D_, name, blurb)
            rows_d.append(M)
            for n in (1, 3, 5):
                wav(f"censer-disc-{name.replace(' ', '-').lower()}-n{n}.wav", M["xs"][n])
        for (name, _sp, blurb) in DISC_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print(f"  RULE  {DISC_RULE}")
        for M in rows_d:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        ok, fb = _gate(rows_d, "disc")
        di = fb if ok is None else min(ok, key=lambda i: (round(max(rows_d[i]["regs"].values()) / 0.05),
                                                          rows_d[i]["calls"], i))
        K_ = rows_d[di]
        print(f"  PICK  {K_['name']}  g {K_['g']}, D {K_['D']}; notes " + " ".join(f"{f_:.0f}" for f_ in K_["notes"])
              + f" Hz at counts 1-5; loudest 50 ms {db(K_['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g}, "
              f"{db(K_['top'] / w_hi):+.1f} dB re the wall; over the heaviest blow "
              + " ".join(f"{v:+.1f}" for v in K_["over_blow_all"]) + " dB (counts 1-5); with a crit (counts 1, 5) "
              + " ".join(f"{v:+.1f}" for v in K_["over_crit"]) + "; over the median blow (@ 33) "
              + " ".join(f"{v:+.1f}" for v in K_["over_mid"]))
        # the controls, on the PICK
        k0 = K_["sp"]
        loud_g = float(f"{K_['g'] * (lev_d['hi'] / K_['top_hi']) * 10 ** (3 / 20):.4g}")
        DCTL = [("0 FLAT", dict(k0, flat=True), K_["g"], K_["D"], ["note", "step"]),
                ("0 LOUD", k0, loud_g, K_["D"], ["too loud"]),
                ("0 HARM", dict(k0, harm=True), K_["g"], K_["D"], ["not a bell"]),
                ("0 TICK", k0, K_["g"], None, ["audible"]),
                ("0 CLANG", dict(k0, modes="clang", click=True), K_["g"], K_["D"], ["not pure", "not mellow"]),
                ("0 SPARK", dict(k0, spark=True), 0, 0, ["register vs spark", "not a bell"])]
        ctld = []
        for name, sp, g, D_, own_ in DCTL:
            if D_ is None:
                lo_, hi_ = math.log(0.005), math.log(1.0)
                for _ in range(13):
                    mid = 0.5 * (lo_ + hi_)
                    if basic(dx(sp, g, math.exp(mid), DISC_REF_N)[0])["aud"] < 40.0: lo_ = mid
                    else: hi_ = mid
                D_ = float(f"{math.exp(0.5 * (lo_ + hi_)):.3g}")
            if sp.get("spark"):
                M = disc_measure(sp, g, D_, name, "",
                                 fn=lambda n, seed=None: play("spark", {"collect": True, "n": n}, seed=seed))
            else:
                M = disc_measure(sp, g, D_, name, "")
            M["own"] = own_
            ctld.append(M)
            wav(f"censer-disc-{name.replace(' ', '-').lower()}-n3.wav", M["xs"][3])
        print("    0 FLAT     the pick at count 1's note for every count -- a control\n"
              "    0 LOUD     the pick 3 dB over its quiet bound -- a control\n"
              "    0 HARM     the pick's partials on whole multiples of its lowest -- a control\n"
              "    0 TICK     the pick dying in 40 ms -- a control\n"
              "    0 CLANG    the pick on a bar's bright modes (2.76, 5.40, 8.93) with a click -- a control\n"
              "    0 SPARK    the heal chime itself played as the disc -- a control")
        for M in ctld:
            hit_own = any(o_ in w_ for o_ in M["own"] for w_ in M["why"])
            if M["why"] and hit_own:
                print(f"  {M['name']} (a control) comes back wrong on its own gate, as it must: "
                      f"{'; '.join(w_ for w_ in M['why'] if any(o_ in w_ for o_ in M['own']))[:200]}")
            else:
                print(f"  {M['name']} (a control) did NOT fail its own gate ({'; '.join(M['why'])[:160] or 'passed'}) "
                      f"-- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")

        # ---- THE HEAL, REUSED ----------------------------------------------
        print("\nHEAL -- 'the `spark collect` voice, reused': unchanged, n = the blessing Censer carries after the apply.")
        for n in (1, 3, 5):
            M = ctl[f"spark{n}"] if f"spark{n}" in ctl else None
            if M:
                print(f"  spark collect n {n}: {1180 + n * 110} Hz, audible {M['aud']:.0f} ms, loudest 50 ms "
                      f"{M['top']:.4f} ({db(M['top'] / w_hi):+.1f} dB re the wall), heard "
                      f"{heard_at(M['x'], T0, p90b)[0]:+.1f} dB re the score's p90")
        # the disc bell and the heal chime on one frame (3 of 1063 heals in the survey)
        xs_ = R([["body", T0, disc_body(k0, K_["g"], K_["D"]), {"n": 3}], ["play", T0, "spark", {"collect": True, "n": 3}]])[0]
        xsp = ctl["spark3"]["x"]
        bn = K_["notes"][2]
        sf = [db(band_rms(xs_, bn, T0, T0 + 0.1) / band_rms(K_["xs"][3], bn, T0, T0 + 0.1)),
              db(band_rms(xs_, 1180 + 330, T0, T0 + 0.1) / band_rms(xsp, 1180 + 330, T0, T0 + 0.1))]
        print(f"  the disc bell (n 3) and the heal chime (n 3) on one frame: the bell's note band moves {sf[0]:+.2f} dB, "
              f"the chime's {sf[1]:+.2f} dB -- printed (the survey: 3 of 1063 heals within 0.1 s of a disc)")
        rec["same_frame"] = sf

        if a.no_wire:
            print(f"\nTHE PICKS  cast {C_['name']}   disc {K_['name']}   heal: the spark collect, unchanged")
            print("  (--no-wire: the rows are not generated or checked)")
            return 1 if FAILED else 0

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        info = dict(c_top=db(C_["top"] / h_lo), c_reg=max(C_["regs"].values()), c_regw=who(C_["regs"]),
                    d_db=db(K_["top"] / h_lo), d_wall=db(K_["top"] / w_hi), d_reg=max(K_["regs"].values()),
                    d_regw=who(K_["regs"]), n_cast=len(CAST_CANDIDATES), n_disc=len(DISC_CANDIDATES))
        arms = arms_code(C_, K_, info)
        _refuse(re.sub(r"/\*.*?\*/", "", arms, flags=re.S), "Sfx row")
        if SFX_ANCHOR in arms or not arms.endswith("\n"):
            raise SystemExit("the Sfx row must not repeat its anchor and must end its last line")
        sfx_rows = [as_replace(SFX_ANCHOR, "before", arms)]
        print("\nTHE SFX ROW (mode `before`, its anchor the fallback line), applied to Sfx.prototype.play's own source "
              "and rendered:")
        dbt = disc_body(k0, K_["g"], K_["D"])
        cbt = cast_body(C_["sp"], C_["g"], C_["kr"], C_["D"])
        chk = []
        for sd in (None, NOISE_SEEDS[5]):
            xa, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows, seed=sd)
            chk.append((f"cast{'' if sd is None else '@5'}", float(np.abs(xa - R([["body", T0, cbt, {}]], seed=sd)[0]).max())))
        for n in (-1, 0, 1, 2, 3, 4, 5, 6, 9, None):
            p_ = {"w": "censer-disc"} if n is None else {"w": "censer-disc", "n": n}
            x1, _ = R([["arm", T0, "ult", p_]], rows=sfx_rows)
            x2, _ = R([["body", T0, dbt, {"n": min(CAP, max(1, n or 0))}]])
            chk.append((f"disc@{n}", float(np.abs(x1 - x2).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (3.6, 9, BLADE, HEAVY, 50) for c_ in (False, True)]
        others += [("hit", {"dmg": 9, "crit": False, "bough": 0.38})]
        others += [("spark", {"collect": True, "n": n}) for n in range(0, 7)]
        others += [("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("clank", {"mass": 1.1}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("aegis", {"n": 10, "back": 5}), ("aegis", {"broke": True}),
                   ("vine", {"plant": True}), ("vine", {"coil": True}), ("vine", {"miss": True}), ("vine", {"n": 2}),
                   ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}), ("fork", {}),
                   ("scour-hold", {"n": 3}), ("scour-tick", {"n": 2}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        others += [(k_, {}) for k_ in kinds if k_ not in {o[0] for o in others} and k_ not in ("ult",)]
        ult_ids = sorted(set(re.findall(r'w === "([a-z-]+)"', play_src)) | {w_[0] for w_ in wpn})
        ult_ids = [w_ for w_ in ult_ids if w_ != ME and not w_.startswith(ME + "-")]
        others += [("ult", {"w": w_, "n": 2, "dmg": 20}) for w_ in ult_ids]
        same_ = []
        for kind_, p_ in others:
            x1 = play(kind_, p_); x2, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows, new=False)
            same_.append((kind_ + "/" + str(p_.get("w", p_.get("dmg", p_.get("n", p_.get("mass", ""))))) +
                          ("!" if p_.get("crit") else ""), float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices: the hit at 5 weights "
              f"x crit and the bough, the heal chime at n 0-6, spark arm and burn, wall, death, clank x2, seal, nova, "
              f"hex-snap, aegis x2, vine x4, loose x3, fork, scour x4, every other kind, and {len(ult_ids)} ult ids -- "
              f"every relic's cast and every sub-voice the ult arm names): worst max |diff| {worst[1]:.0e} ({worst[0]})")
        xa, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows)
        now_rc = float(np.abs(xa - x_fb).max())
        print(f"  ult/censer vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, n_others=len(same_))
        e2e_voices = others

        # ---- WITH OTHER RELICS' ROWS ------------------------------------------
        peers = []
        for pf, ps in peer_rows_ok:
            pids = sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _, c in ps))))
            A_ = sfx_rows + ps; B_ = ps + sfx_rows
            mine = [("ult", {"w": ME}), ("ult", {"w": ME + "-disc", "n": 1}), ("ult", {"w": ME + "-disc", "n": 5})]
            evs = mine + [("ult", {"w": w_, "n": 3, "k": 1, "shield": 45}) for w_ in pids]
            dmax, dmine = 0.0, 0.0
            for kind_, p_ in evs:
                xa_, _ = R([["arm", T0, kind_, p_]], rows=A_, new=False)
                xb_, _ = R([["arm", T0, kind_, p_]], rows=B_, new=False)
                dmax = max(dmax, float(np.abs(xa_ - xb_).max()))
                if str(p_.get("w", "")).startswith(ME):
                    xs2, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows, new=False)
                    dmine = max(dmine, float(np.abs(xa_ - xs2).max()))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids)}): both orders render every "
                  f"arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e})")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {peer_name(pf)}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids, both_orders=dmax, mine=dmine))
        rec["peers"] = peers

        # ---- THE resolveHit AND tickHolyGround ROWS --------------------------
        seeds = [a.seed0 + k for k in range(a.seeds)]
        rh = [as_replace(DISC_ANCHOR, "after", DISC_CODE)]
        hg = [as_replace(HEAL_ANCHOR, "after", HEAL_CODE)]
        print("\nTHE resolveHit AND tickHolyGround ROWS, applied to their prototypes' own source, run beside the "
              "originals on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds, rh, hg])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Censer both sides x every foe x seeds {seeds}): {WR['same']}/{WR['fights']} "
              f"identical (over, the clock, the ground's clock and every disc, both fighters' hp, shield, position, "
              f"velocity, stun, blows, damage, smite and blessing counts and holyTally, the winner); every other voice "
              f"call identical in order, kind and opts in {WR['otherSame']}/{WR['fights']}")
        ns = np.array(WR["ns"]) if WR["ns"] else np.zeros(1)
        hn = np.array(WR["hn"]) if WR["hn"] else np.zeros(1)
        hist = {int(k): int((ns == k).sum()) for k in range(1, 8) if (ns == k).sum()}
        hhist = {int(k): int((hn == k).sum()) for k in range(0, 7) if (hn == k).sum()}
        print(f"  {WR['casts']} casts -> {WR['castV']} cast voices; {WR['discs']} discs -> {WR['discV']} disc bells "
              f"({WR['killBells']} on a killing blow); {WR['blessings']} blessings -> {WR['healV']} heal chimes; "
              f"problems {WR['nbad']}")
        print(f"  the count a disc bell carries: {hist}; the count a heal chime carries: {hhist}")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                or WR["discV"] != WR["discs"] or WR["healV"] != WR["blessings"] or WR["castV"] != WR["casts"] \
                or WR["discs"] == 0 or WR["blessings"] == 0 or WR["casts"] == 0:
            FAILED.append("sim rows")
        WB = page.evaluate(WIRE_JS, [seeds, [as_replace(DISC_ANCHOR, "after", DISC_CODE_BAD)], hg])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on a disc): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "casts", "castV", "discs", "discV",
                                          "blessings", "healV", "killBells", "nbad")}
        rec["wire"].update(control_same=WB["same"], count_hist=hist, heal_hist=hhist)

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        clips = sorted(WR["clips"], key=lambda c: (-(c[5] + c[6]), c[4] - c[3]))
        if not clips:
            FAILED.append("no clip: no window with two discs")
        else:
            cside, cf, cs, c0, c1, nd_, nh_ = clips[0]
            EV = page.evaluate(RECORD_JS, [cside, cf, cs, rh, hg])
            assert not errors, errors[:3]
            lo_t, hi_t = c0 - 1.0, c1 + 1.5
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if e[3] not in ("censer-disc", "heal")]
            nocast = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
            xo, _ = R(without, secs=secs, rows=sfx_rows, new=False)
            xn, _ = R(nocast, secs=secs, rows=sfx_rows, new=False)
            bd = np.resize(bed, len(xw)) if len(bed) < len(xw) else bed[:len(xw)]
            xw = xw + bd; xo = xo + bd; xn = xn + bd

            def ov(xa_, xb_, f, a_, d_):
                return db(band_rms(xa_, f, a_, a_ + d_) / max(band_rms(xb_, f, a_, a_ + d_), 1e-12))
            dn = disc_notes(k0)
            dsc = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == "censer-disc"]
            d_over = [ov(xw, xo, dn[min(CAP, max(1, n_)) - 1], t_, 0.2) for t_, n_ in dsc]
            hl = [(T0 + (e[0] - lo_t), e[2].get("n")) for e in evs if e[3] == "heal"]
            h_over = [ov(xw, xo, 1180 + n_ * 110, t_, 0.1) for t_, n_ in hl]
            ca_t = T0 + (c0 - lo_t)
            # the bell is read as its isolation gate reads it: at its BEST third-octave at or above 200 Hz over
            # the strike's first 150 ms (a phone's). Its strongest peak, the hum, is printed beside: the score's
            # bass lives in that band.
            fb_ = C_["b_heard_f"]
            c_bell = ov(xo, xn, fb_, ca_t + C_["strike"], 0.15)
            c_hum = ov(xo, xn, C_["b_strong"], ca_t + C_["strike"], 0.15)
            rb_ = max((v_, fc) for v_, fc in zip(bands(C_["x"][int(T0 * SR):int((T0 + C_["strike"]) * SR)]), BANDS)
                      if fc >= 2000)[1]
            c_rat = ov(xo, xn, rb_, ca_t + max(C_["strike"] - 0.1, 0.0), 0.1)
            print(f"\nIN A REAL WINDOW -- censer v {cf} (side {'AB'[cside]}), seed {cs}, cast at {c0:.2f}s, {nd_} discs "
                  f"and {nh_} heals by {c1:.2f}s (counts {' '.join(str(n_) for _, n_ in dsc)}); the fight's own sounds "
                  f"and the score, with and without the new voices")
            print("  each disc bell over the fight in its note's third-octave, 0-200 ms: " +
                  " ".join(f"{v:+.1f}" for v in d_over) + " dB")
            print("  each heal chime over the fight in its own third-octave, 0-100 ms (printed; the chime is "
                  "reused): " + " ".join(f"{v:+.1f}" for v in h_over) + " dB")
            print(f"  the cast over the fight without it: the bell {c_bell:+.1f} dB in its best third-octave at or "
                  f"above 200 Hz ({fb_:.0f} Hz) over the strike's 150 ms (its hum, {C_['b_strong']:.0f} Hz, "
                  f"{c_hum:+.1f} dB: the score's bass shares that band); the rattle {c_rat:+.1f} dB at {rb_:.0f} Hz "
                  f"over the 100 ms before the strike")
            if not d_over or min(d_over) < 3 or c_bell < 3 or c_rat < 3:
                FAILED.append("a new voice not heard in a real window")
            wav("censer-pick-real-window.wav", xw)
            wav("censer-pick-real-window-without.wav", xo)
            rec["real"] = dict(clip=[cside, cf, cs], cast=c0, last=c1, discs=dsc, disc_over=d_over, heals=hl,
                               heal_over=h_over, cast_bell=c_bell, cast_bell_f=fb_, cast_hum=c_hum,
                               cast_rattle=c_rat)
        # the picks in order, for the ear: the cast, three blows each with its disc bell, a heal chime after one
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, (t_, n_) in enumerate(((1.2, 1), (2.4, 2), (3.3, 3))):
            seq += [["arm", T0 + t_, "hit", {"dmg": MID, "crit": False}],
                    ["arm", T0 + t_, "ult", {"w": ME + "-disc", "n": n_}]]
        seq += [["arm", T0 + 2.6, "spark", {"collect": True, "n": 1}], ["arm", T0 + 3.6, "spark", {"collect": True, "n": 2}]]
        wav("censer-pick-sequence.wav", R(seq, secs=6.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: Censer's cast (the thurible swing) and disc-bell arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="before", code=arms),
            dict(label="resolveHit: the disc bell, once per disc planted, with the caster's discs standing",
                 anchor=DISC_ANCHOR, mode="after", code=DISC_CODE),
            dict(label="tickHolyGround: the heal chime (spark collect, unchanged), once per blessing, with the count",
                 anchor=HEAL_ANCHOR, mode="after", code=HEAL_CODE)]
    for r_ in rows:
        if not (r_["code"].isascii() and r_["anchor"].isascii()):
            raise SystemExit(f"a row is not ASCII: {r_['label']}")
        _refuse(re.sub(r"/\*.*?\*/", "", r_["code"], flags=re.S), r_["label"])
        if r_["mode"] != "replace" and r_["anchor"] in r_["code"]:
            raise SystemExit(f"row '{r_['label']}': a before/after row must not repeat its anchor")

    def apply_text(src_html, what):
        patched = src_html
        for r_ in rows:
            c = patched.count(r_["anchor"])
            if c != 1:
                raise SystemExit(f"{what}: an anchor occurs {c} times")
            an, rep = as_replace(r_["anchor"], r_["mode"], r_["code"])
            patched = patched.replace(an, rep, 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"{what}: an anchor is not kept exactly once")
        return patched

    NEWP = [("cast", {"w": ME}, cast_body(C_["sp"], C_["g"], C_["kr"], C_["D"]), {}),
            ("disc@1", {"w": ME + "-disc", "n": 1}, disc_body(K_["sp"], K_["g"], K_["D"]), {"n": 1}),
            ("disc@5", {"w": ME + "-disc", "n": 5}, disc_body(K_["sp"], K_["g"], K_["D"]), {"n": 5})]

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
            rcp = R2([["play", T0, "ult", {"w": "__no_such_relic__"}]])
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
        d_ok = sum(f_["discV"] == f_["discs"] and f_["badN"] == 0 for f_ in F1)
        h_ok = sum(f_["healV"] == f_["blessings"] for f_ in F1)
        s_ok = sum(f_["stray"] == 0 for f_ in F1)
        orig_new = sum(f_["discV"] + f_["healV"] for f_ in ref_fights)
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "discs", "blessings", "castV", "discV", "healV")}
        print(f"  the new voices through the patched page's own SFX.play vs the lab's candidate text in that page, "
              f"max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/censer vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, disc bells = discs (with the count) "
              f"{d_ok}, heal chimes = blessings (with the count) {h_ok}, every voice where it belongs {s_ok} (of "
              f"{len(F1)}); totals {tot}; the original page played {orig_new} disc bells or heal chimes; page errors "
              f"{page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1)
                   or osame != len(F1) or min(c_ok, d_ok, h_ok, s_ok) != len(F1) or orig_new or page_err
                   or tot["discV"] == 0 or tot["healV"] == 0 or tot["castV"] == 0)
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same, other_same=osame, totals=tot,
                    page_errors=page_err)

    if a.e2e_seeds > 0:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="censer_e2e_"))
        try:
            tp = tmpd / "sc-censer-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the three rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
    rec["patched_sha"] = hashlib.sha256(apply_text(html, "sha").encode()).hexdigest()[:16]

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), disc=strip(rows_d), disc_controls=strip(ctld),
               wavs=sizes,
               pick={"cast": C_["name"], "cast_g": C_["g"], "cast_kr": C_["kr"], "cast_D": C_["D"],
                     "disc": K_["name"], "disc_g": K_["g"], "disc_D": K_["D"]})
    print(f"\nTHE PICKS  cast {C_['name']}   disc {K_['name']}   heal: the spark collect, unchanged   smite tick: "
          f"silent (no voice exists; 'nothing new')")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    wr = rec["wire"]
    rows[0]["why"] = (
        f"v78 s4's two new voices, in the synth only: the cast's thurible swing (a chain-rattle into a low bell) "
        f"and the disc's soft bell pitched by the discs standing; the heal is the existing spark collect and the "
        f"smite tick has no voice. Code's picks on the numbers under Rick's 'you pick i overrule': cast "
        f"{C_['name']}, disc {K_['name']} (censer_voice_lab.py). The arms go BEFORE the shared rune-crack fallback "
        f"(mode `before`, its anchor the fallback line itself), so the {len(rec['fallthrough'])} other relics that "
        f"still fall through keep it and another relic's row anchored there applies in either order. Through the "
        f"patched play() each arm reproduces its lab candidate (worst "
        f"{max(v for _, v in rec['arm_check']['chk']):.0e}), {rec['arm_check']['n_others']} other voices are "
        f"unchanged (worst {max(v for _, v in rec['arm_check']['others']):.0e}), and ult/censer is no longer "
        f"rune-crack. play() returns on its first line with no audio context (every headless run), draws no random "
        f"number and writes nothing the simulation reads"
        + (f"; end to end the new voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    rows[1]["why"] = (
        f"After the push's own `holyTally.discs++` (kept unchanged, inside the push's if): a block-scoped count of "
        f"the caster's discs standing (it READS m.holyGround, writes nothing) and one SFX.play. {wr['discV']}/"
        f"{wr['discs']} discs voiced over {wr['fights']} fights, each on its push's step with the count standing "
        f"after it ({wr['count_hist']}); {wr['same']}/{wr['fights']} fights identical and every other SFX call "
        f"identical in order and opts; the rows plus one sim write come back {wr['control_same']}/{wr['fights']}{e2}.")
    rows[2]["why"] = (
        f"After the blessing's own `T.bless++` (kept unchanged): the existing spark collect with n = the blessing "
        f"Censer now carries, Zenith's call word for word. {wr['healV']}/{wr['blessings']} blessings voiced, each "
        f"with the count its apply left ({wr['heal_hist']}); nothing is read back{e2}.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print(f"\nTHE ROWS AS TEXT: {len(rows)} rows ({', '.join(r_['mode'] for r_ in rows)}) give {gp.name} "
          f"sha256[:16] {rec['patched_sha']}")
    print("\n  NOTHING IS IN THE BUILD. The three rows are the edits; all three were applied "
          "to the page's own code above, and as text to a copy of the page.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
