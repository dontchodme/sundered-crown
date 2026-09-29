#!/usr/bin/env python3
"""BENEDICTION'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v110.

    python aureole_voice_lab.py --game <a link carrying Aureole's stage 5> --rows rows.json

v82 section 4 SOUND, every word of it: "Sound: cast -- a soft choir swell (two
re-struck tones, a fifth), 0.5s; a foe entering -- a single bright note; the
blessing -- the `spark collect` voice reused; close -- the swell reversed."
The brief's stage 4 (v110's stage 6): "picture (bloom measured), voice,
carry". Rick, for the batch's art and sound: "you pick i overrule". So this lab
does not offer a spread -- it renders three to five candidates a voice beside
CONTROLS that can come back wrong, prints the numbers each pick is made on, and
PICKS by a rule written in this file (`*_RULE`, `*_why`). He overrules from one
clip.

ONE VOICE IS REUSED, BECAUSE THE DESIGN NAMES IT: the blessing plays the
EXISTING `spark {collect: true, n}` -- the heal chime Daybreak's sparks and
Zenith's blessings already play -- unchanged, n = the blessing count she now
carries, exactly as Zenith's `tickSun` calls it. It exists, so nothing is made
for it; it is measured here beside the new voices. THE SMITE HAS NO VOICE: v82
names none (the smite tick that kills files its own beat inside tickStatus).

THE FOUR EVENTS AND WHERE THEY FIRE (line numbers are sc-aureole-b12.5's):
  cast   the bare id `ult/aureole`, which `fireUlt` plays for every relic
         (16273, the generic prelude, before the halo branch). Aureole has NO
         arm today: it falls through to the shared rune-crack (measured below,
         to 1e-6, with every other relic that still does). The arms go BEFORE
         that fallback, in a row of mode `before` whose anchor is the fallback
         line itself -- so the fallback is never touched, and another relic's
         row anchored on it applies in either order. No sim line: the cast
         already plays it, once a cast.
  enter  `ult/aureole-enter` from `tickHalo`, on a line placed BEFORE the
         inside test (13667, mode `before`): on an inside tick that follows an
         outside tick IN THE SAME WINDOW -- the foe crossing into the ring.
         The ticker keeps no memory of the last tick's test, so the row keeps
         its own: `Z.voiceIn` (1 inside, 0 outside) on the window's record,
         which nothing in the simulation reads, and which is born undefined
         with every cast -- so a foe already standing inside when the halo
         rises (151 of 506 windows, runs below) is NOT an entry: the cast's
         swell has that moment. The test is the ticker's own expression,
         repeated. No debounce: the entries in a window are a median 1.03 s
         apart and 22 of 2591 are under 0.2 s (runs below).
  bless  the unchanged `spark {collect: true, n}` from `tickHalo`, right after
         `T.bless += u.bless;` (13678, mode `after`): once per blessing, on
         its frame, n = f.stacks("blessing") after the apply (Zenith, 13401).
         61% of entries land on a blessing's frame, so the entry note and the
         heal chime are measured together.
  close  `ult/aureole-close` from `tickHalo`, on a line placed BEFORE the
         window's close line (13662, mode `before`): on the frame the halo
         runs out BY ITS CLOCK with both fighters alive -- never on a death (a
         caster's death ends the fight; a close after the foe's death belongs
         to its kill flight: both are the death voice's), never once the fight
         is over (step() stops calling the tickers; a halo still up at `over`
         closes in the picture only). Tendril's, Canopy's, Zenith's and
         Lightkeeper's rule.
  Nothing here sets a hit stop or files a beat. The four voices are plain
  SFX.play calls; the picture's rows are the picture lab's, not these, and none
  of them touches `tickHalo` or the Sfx table.

THE CONTROLS, and what each one is for:
  rune-crack   what Aureole's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted (with BAR 0.364 /
               300 ms and hit@11.6 0.443 / 80 ms)
  hit@12.5     Aureole's own blow (the blade holds at 12.5, stage 5): the level
               every voice is judged against, on its quietest / loudest draw
  wall         the commonest sound in a fight: the entry note's floor
  the school   the sanctified casts with a voice of their own (read off the
               page: Daybreak's and Zenith's) -- and, from `--peer-rows`,
               Angelus's cast and close, the school's other choir on the batch
               line (the real chain carries it now)
  the type     the bow casts with a voice of their own (read off the page)
  BAR, seal    Corollary's cast; the game's other stack of fifths (220 / 330 /
               495 Hz triangles): the halo's fifth must not be the seal
  spark 1-5, Zenith's tick 0-4, hex-snap, the bowstring, clank, death   the
               small bright voices, the heal chime the entry shares a frame
               with, and the heavy ones: the entry must not be any of them
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  STEP, ONE, STRUCK, OFFBEAT, BRIGHT, BELL, RUNECRACK   the cast as Zenith's
               figure (the root, then the fifth) / the root alone / one strike
               a tone / re-struck a flat 11 ms apart, not on whole cycles (out
               of phase: Angelus's control) / in Zenith's bright timbre (a
               triangle and its octave) / with a bar's 2.76 mode for its 2nd
               partial / today's voice: each must fail its gate
  LOW, DULL, DOUBLE, TICK, SPARK   the entry two octaves down / a bare sine /
               the note and its fifth 120 ms later / dying in 30 ms / the heal
               chime itself: each must fail its gate
  AGAIN, SHORT, QUIET   the cast itself / the close over half the length / 9
               dB under: each must fail its gate
  LITERAL      the picked cast rendered dry, its samples REVERSED, played
               through the chain: the reference ENV-CORR reads the close
               against (it cannot ship -- an arm cannot reverse samples)
  RAW          the picked cast without `.frequency.value = f`: printed as a
               REFERENCE (Angelus's v104 finding: under ~D5 at an 11 ms
               spacing the slip is not a thing these rules, or an ear, can
               hear -- so it is not a control; OFFBEAT is)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT. Each candidate is generated as the JS
    body that will sit in the arm (constants rounded first) and rendered by
    evaluating that text on the synth (ironwood_voice_lab's RENDER_JS,
    imported unchanged); the row is then applied to `Sfx.prototype.play`'s
    own source and rendered again, and must match to TOL = 1e-5.
  * The shared measures are zenith_voice_lab's, ironwood_voice_lab's,
    bindweed_voice_lab's, ironhail_voice_lab's and lightkeeper_voice_lab's,
    imported unchanged: E50, TOP (the loudest 50 ms, and where it is
    centred), START (the loudest 50 ms centred in the first 100), SWELL = TOP
    - START, DIPS (drops > 3 dB below the running max on the way up),
    AUDIBLE / GONE (the 5 ms RMS above 2% of its own loudest), RISE, LATE,
    CENTROID, REG (cosine of 1/3-octave band amplitudes, 25 Hz-16 kHz, the
    median over noise draws), PITCH (FFT peak, Hann, zero-padded,
    parabolic), FLUTTER (p95 - p5 of the RMS over four periods of a pitch --
    C4 here -- at a 1 ms hop about its 100 ms average, over the audible span
    less 50 ms each end), TONAL, ENV-CORR (aligned at the audible onsets:
    v107's round 2), ONSETS, HEARD (the voice's loudest third-octave at or
    above 200 Hz over 100 ms against the score's p90 there, dB) and PHONE
    (the TOP high-passed at 200 Hz).
  * New here, each with a control that can come back wrong:
      TONES    each of the dyad's two tones: its FFT peak within 6% of it
               (cents off) and its level, over the START (20-100 ms) and over
               the CREST (the 100 ms centred on TOP): "two tones" is both
               within 30 cents and the weaker within 6 dB of the stronger in
               BOTH windows (STEP and ONE must fail)
      CHOIR    harmonic, a voice and not a chime: every spectral peak within
               20 dB of the strongest (200-3000 Hz, the crest window) lies
               within 25 cents of a whole multiple of C3 (130.81 Hz -- C4 is
               its 2nd harmonic and a just G4 its 3rd, so every partial of
               either tone is one); BELL must fail
      SOFT     no edge: the strongest spectral peak at or above 4.9x the root
               (over the crest) at least 30 dB under the root's -- the voice
               lives on its tones and their first partials; a triangle's 5th
               harmonic sits 28 dB under its note, so BRIGHT must fail
      CREST-HEARD   HEARD read over the crest window instead of the first 100
               ms (a swell is quiet at its start by design)
      BRIGHT (the entry)   its note at or over 1 kHz and an overtone (the
               strongest peak 1.5x-4x the note, first 50 ms) within 12 dB of
               it; LOW and DULL must fail
      SAME-FRAME  the entry and the heal chime (n = 3) on one frame: each
               voice's own loudest third-octave over its first 100 ms moves
               <= 1 dB for the other's presence
      RERISE   after the close's top, the most its E50 climbs back over its
               running minimum, dB
      PLACE    where the close's TOP is centred, as a fraction of its
               audible span from its onset (round 4; AGAIN must fail)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: every cast strikes for 0.25 s (below); its swell length is solved
    so its TOP is centred 340 ms after the cast, its swell depth so SWELL is
    +12 dB, and its gain to the centre of its level window (five passes);
    its AUDIBLE length then falls where it falls and is gated; a breath (where there is one) 18 dB under the tones; the entry's
    decay so it is AUDIBLE 200 ms and its gain to the centre of its window;
    the close's gain so its TOP is the cast's. Constants are rounded BEFORE
    any measured render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of v82 section 4 turned into
numbers; Code's picks, Rick's to overrule):
  * "TWO RE-STRUCK TONES, A FIFTH": two tones sounding TOGETHER, a just fifth
    -- a choir holds its notes; Zenith's brief said "a rising fifth" and
    this one does not. Each tone is held by re-striking it in phase at its own
    whole cycles nearest every 11 ms (Zenith's spacing), `.frequency.value =
    f` set on every strike (v97's toolkit finding), the first strike of a
    tone carrying 0.6 of its plateau (v97's HANDOFF). The fifth sits at 0.8 of
    the root (the school's own choir weights: Angelus, v104).
  * THE FIFTH IS C4-G4 (261.63 / 392.44 Hz), the score's III -- the key's own
    major chord -- in the choir's middle. It was chosen by measurement
    (stage6-voice/pitch_survey.py, scratch): a plain two-tone swell at every
    diatonic fifth of A minor from C4 to E5, levelled alike, read against the
    school's and the type's casts, rune-crack, BAR, the seal, the blow, the
    heal chime and Angelus's cast and close. C4-G4 is the most distinct
    (at most 0.51, Angelus's close); D4, G4 and A4 sit on Angelus's choir
    (0.80-0.92), E4 and F4 on the seal (0.77), D5 on Zenith's cast (0.91),
    C5 on Daybreak's (0.71), E5 on BAR (0.53). Every one was heard.
  * "0.5s": AUDIBLE 415-585 ms (v100's +/-17.5% reading of "0.4s", scaled).
    THE CREST lands where the ring has finished opening: the picture's 0.3 s
    expansion, plus the cast's 0.08 s hit stop if the picture's clock stops
    in it -- 0.30-0.38 s after the cast voice; the target is the middle,
    0.34 s, and the gate 300-450 ms.
  * THE STRIKE is 0.25 s long, Zenith's (v98): the length that holds a
    re-struck tone evenly. ROUND 1 solved it for AUDIBLE 500 ms instead, and
    that drove every cast to a 0.10-0.12 s strike: each strike then falls
    ~4.5 dB between re-strikes and the dyad buzzes at the strike rate (every
    cast's FLUTTER 4.1-4.9 dB, and CHOIR read the buzz's sidebands -- G4 less
    its 98 Hz strike rate, 290 Hz -- as a peak off the harmonics). Round 2
    holds the strike and lets the length follow.
  * "SOFT": no attack (a SWELL of +8..+16 dB with no DIPS: it begins quiet)
    and no edge (SOFT, above); the level stays in the batch's cast window
    (heard like a blow, never over one) -- "soft" is read as the timbre and
    the onset, as v98 read Zenith's "soft chime", not as a lower level.
  * "CHOIR": a voice, not a chime -- harmonic (CHOIR, above).
  * "A SINGLE BRIGHT NOTE": ONE onset and one pitch (it holds within 30
    cents), a NOTE (TONAL >= 15 dB), BRIGHT (above), the moment of the entry
    (its peak inside 50 ms), a note and not a tick (AUDIBLE 120-350 ms: longer
    than the house's ticks and tinks, <= 60 ms, and shorter than the p5 gap
    between entries, 0.35 s, so entries do not blur). Its pitch is C6
    (1046.50 Hz), the halo's root two octaves up: the lowest note of the
    halo's own pitch classes at or over 1 kHz, clear of the heal chime it
    shares a frame with (1.29-1.73 kHz) and of Zenith's tick (2.1-3.5 kHz).
    Its level sits between twice the wall tick and 0.7 of the blow
    (Tendril's bite window, v101).
  * "THE SWELL REVERSED": the picked cast's own figure run backward, at the
    cast's own level (v82 does not say quiet; Zenith's "reversed, quiet" had
    to say it): its release becomes a short climb on the dyad (MIRROR, as
    Zenith's close took its cast's release, v98), then its swell becomes a
    fall of the same depth over the same length; FADE starts at the top;
    SIGH falls in a straight line of amplitude instead of dB; DEEP and TIGHT
    are MIRROR with the fall carried on down to the ear's floor, or its
    length solved so the whole is as long as the cast (round 3, below).
    Measured against the LITERAL reversal.
  * THE BLESSING: `spark {collect: true, n}` unchanged, n = f.stacks
    ("blessing") after the apply -- Zenith's call, word for word.
  * REGISTER: every new voice <= 0.80 against each voice it must not be
    (listed in its rule); the entry <= 0.50 against the heal chime at every
    count (they share a frame: Zenith's tick rule, v98).

THE ROUNDS (each a run of this file; the logs in scratch stage6-voice/):
  1  no cast passed: the strike was solved for AUDIBLE 500 ms, which drove
     it to 0.10-0.12 s (FLUTTER 4.1-4.9 dB, and CHOIR read the strike-rate
     sidebands); SUNG's arm shadowed its gain. -> the strike held at 0.25 s
     (Zenith's), the crest target 0.34 s, AUDIBLE gated and not solved; the
     shadowing fixed.
  2  the cast (PURE) and the entry (CHIME) pass; NO CLOSE passed. MIRROR rang
     715 ms against the cast's 555: `_tone` ramps every strike to an
     absolute 1e-4, so a strike 20 dB down decays at about half the rate of
     one at the top, and the fall's last strikes ring on. FADE and SIGH
     start at the top, 200 ms ahead of the literal reversal's crest, and
     correlate 0.49 / 0.55. And the LITERAL reversal itself failed two gates
     the close is read on -- LATE 0.45 against "<= 0.45" (a reversal's LATE is
     1 less the cast's, 0.55) and HEARD over its first 100 ms, which is the
     reversed release, quiet by construction -- so those gates were misread:
     a reference that fails its own rule proves the rule wrong, not the
     reference. -> round 3: HEARD for the close read at its crest (as the
     cast's CREST-HEARD); LATE "its energy early" read as LATE <= 0.50, its
     energy's centre in the first half of its sound (the cast's is in the
     second; AGAIN must still fail); two MIRRORs added, DEEP (the fall
     carried on down to -34 dB, the audible floor, over the same length)
     and TIGHT (the fall's length solved so the whole is as long as the
     cast). The cast and entry rules are unchanged.
  3  TIGHT passes (ENV-CORR 0.91, LATE 0.43, audible 555 ms); DEEP still
     rings 700 ms. But the AGAIN control (the cast itself) came back wrong
     on LATE alone, 0.55 against 0.50: ENV-CORR reads the cast 0.83 against
     its own reversal (two humps of dB correlate however they lean), so
     "reversed" rested on one number's 0.05. -> round 4 adds PLACE, the
     direction read a second way: the TOP's centre within the first half of
     the sound ((TOP - onset) / AUDIBLE <= 0.50; the cast's crest sits at
     about 0.6). Nothing else changes.
  4  (the first full run) every gate passes -- the picks PURE / CHIME /
     TIGHT, AGAIN failing LATE and PLACE, the rows identical on every
     fight -- but one: in the real window the close read +2.2 dB (gate +3),
     read over its first 100 ms, which is its reversed release, a climb
     from -34 dB: round 3's HEARD misreading again, in the real-window
     reading. -> round 5 reads each swell (the cast and the close) over the
     100 ms centred on its TOP, CREST-HEARD's window, and prints the onset
     reading beside it; the entry notes and heal chimes are read at their
     onsets (their tops) as before; the AFTER and LEVEL controls unchanged.

  5  every gate passes: the swells heard at their crests in the real window
     (the cast +28.3 dB, the close +11.9; their onsets +7.2 / +2.2, printed),
     the AFTER and LEVEL controls failing as they must. The picks: cast 1
     PURE, entry 2 CHIME, close 5 TIGHT. (Run again once with the cast
     arm's comment naming the peer choir it is registered against -- the
     same numbers, bit for bit.)

THE PICKS -- see the run's own printout (stage6-voice/iter*.log; the passing
run's is the last); the rows' comments carry the same numbers.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (three arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm must reproduce
    its candidate to TOL on two noise draws; every other voice through the
    patched play (the hit at five weights with and without a crit, spark x3,
    wall, death, clank x2, seal, nova, hex-snap, aegis x2, vine x4, loose x3,
    fork, scour x4, and every ult id and kind the page's play() names) must
    be unchanged; `ult/aureole` must NOT be rune-crack any more;
  * the three tickHalo rows are applied to `Match.prototype.tickHalo`'s own
    source and run on real fights beside the unpatched one: every fight
    identical (over, clock, both fighters' hp, positions, velocities,
    charges, facing, smite and blessing counts, the arrows in the air, the
    winner, the whole haloTally and the halo's record but `voiceIn`) and
    every other voice call identical in order, kind and opts; one entry note
    per inside tick after an outside tick of the same window, none on a
    window's first tick; one heal chime per blessing, on its frame, carrying
    the count the apply left; one close per window closed by its clock with
    both alive and none otherwise; one cast voice per cast (from `fireUlt`,
    outside the ticker); the unpatched ticker plays nothing. The same rows
    plus ONE sim write (the foe nudged 1e-9 on an entry) must come back NOT
    identical, or "identical" proves nothing. (The Sfx row cannot reach the
    simulation at all: `play` returns on its first line with no audio
    context, which is every headless run.)
  * END TO END: the rows applied AS TEXT (the orchestrator's semantics:
    replace = code, after = anchor + code, before = code + anchor) to a copy
    of the game file (in a temp folder, never the repo), loaded in a fresh
    browser after the first is closed: the page loads clean, its own
    SFX.play renders the arms to the lab's text and every other voice to the
    original page's, and its fights are identical to the original page's,
    with the voice counts above. With `--also <link>` (Aureole carried onto a
    newer tip), the same, there.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both
    identically; registers against the peers' voices are printed, and the
    cast's against the school's (Angelus's cast and close) is gated.
  All anchors must occur exactly once in the game file; no row replaces its
  anchor, so a later relic's row -- or the picture's -- anchored on the same
  line still applies, in either order. Every row is ASCII.

Writes wavs to 05-reference/v110/aureole-*.wav at RAW level (gitignored).
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
# means in v98's, v99's, v101's, v107's and v108's labs. (Their module bodies
# only define things and check their own candidate sources.)
from zenith_voice_lab import (  # noqa: E402
    BANDS, BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, cos, db,
    dips_and_lin, env, env_corr, flutter, fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm  # noqa: E402
from bindweed_voice_lab import mreg, tonal  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90, heard, phone  # noqa: E402
from lightkeeper_voice_lab import LIT_JS, _wrap, onsets, own_band  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "aureole"
BLADE = 12.5                              # Aureole's dmg (stage 5: the shipped rate)
TOL = 1e-5                                # reproduction / transcription (-100 dB)
F_ROOT = 261.6256                         # C4: the halo's root (the fifth: x1.5, just)
C3 = F_ROOT / 2                           # the dyad's common fundamental
KF = 0.8                                  # the fifth's weight re the root (Angelus's choir)
EVERY = 0.011                             # a re-strike on the whole cycle nearest every 11 ms (Zenith's)
A0 = 0.6                                  # a tone's first strike carries 0.6 of its plateau (v97)
CREST_AT = 0.34                           # the swell's TOP centre: the ring open (0.30-0.38 s after the cast voice)
CAST_D = 0.25                             # a strike's length (Zenith's: what holds a re-struck tone evenly)
SWELL_DB = 12.0                           # the cast's level-matched swell
BREATH_DB = 18.0                          # a breath under the tones
F_NOTE = 1046.502                         # C6: the entry's note (the root two octaves up)
NOTE_AUD = 200.0                          # the entry's decay is solved to this (gate 120-350)
QUIET_DB = 9.0                            # the QUIET control: the batch's usual quiet close
FLUTTER_MAX = 3.0                         # zenith_voice_lab's "sustained-by-restrike" gate, dB
SCHOOL_AFF = "sanctified"
TYPE_SHAPE = "bow"


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


# =============================================================== THE CAST ===
# "a soft choir swell (two re-struck tones, a fifth), 0.5s". Every candidate is
# the same dyad (C4 and a just G4 at 0.8) re-struck in phase, swelling the same
# way; they differ in the voice: its partials, a second singer, a breath.
CAST_CANDIDATES = [
    ("1 PURE", dict(parts=[]),
     "two sines, C4 and G4, re-struck in phase and swelling together"),
    ("2 OO", dict(parts=[(2, 0.2)]),
     "each tone with its 2nd partial at 0.2 -- the 'oo' of a soft choir"),
    ("3 VOWEL", dict(parts=[(2, 0.3), (3, 0.12)]),
     "each tone with its 2nd and 3rd partials at 0.3 / 0.12 -- the school's choir voice (Angelus's VOWEL)"),
    ("4 CHORUS", dict(parts=[(2, 0.2)], chorus=4.0),
     "OO with a second singer a part, 4 cents sharp at half the level -- a choir is many voices"),
    ("5 BREATH", dict(parts=[(2, 0.2)], breath=True),
     "OO with the choir's breath: a bandpass band 500 -> 900 Hz swelling with it, 18 dB under"),
]


def _tones(sp):
    """[[ratio, weight, cents], ...] of a cast-family spec."""
    if sp.get("mode") == "one":
        t_ = [[1, 1.0, 0.0]]
    else:
        t_ = [[1, 1.0, 0.0], [1.5, KF, 0.0]]
    if sp.get("chorus"):
        t_ += [[r, round(k * 0.5, 6), sp["chorus"]] for r, k, _c in t_]
    return t_


def _strike(sp, T, gain, ind):
    """One strike of a tone (and its partials) at time T, as arm text."""
    br = sp.get("timbre") == "bright"
    ty = "triangle" if br else "sine"
    parts = [(2, 0.4)] if br else sp["parts"]
    fv = "" if sp.get("raw") else ".frequency.value = f"
    out = [f'this._tone({T}, {{ freq: f, gain: {gain}, dur: D, type:"{ty}" }}){fv};']
    if parts:
        pa = "[" + ", ".join(f"[{fmt(h)}, {fmt(k)}]" for h, k in parts) + "]"
        fv2 = "" if sp.get("raw") else ".frequency.value = f * h"
        out += [f"for (const [h, kh] of {pa})",
                f'  this._tone({T}, {{ freq: f * h, gain: {gain} * kh, dur: D, type:"sine" }}){fv2};']
    return [" " * ind + l_ for l_ in out]


def dyad_body(sp, g, sw, L, D, kb=0.0, part="both", ind=10):
    """The cast (env 'swell') and every close (env 'fade' / 'sigh', head = the
    mirrored release, a climb on the dyad) as arm text.
    sp: parts, chorus (cents), breath, mode ('dyad' / 'step' / 'struck' /
    'offbeat' / 'one'), timbre ('bright'), raw, env, head. g the gain, sw the
    swell depth (dB), L the swell's length, D a strike's length, kb the
    breath's level re g."""
    env_ = sp.get("env", "swell")
    H = sp.get("head", 0.0) or 0.0
    mode = sp.get("mode", "dyad")
    out = [f"const g = {fmt(g)}, sw = {fmt(sw)}, L = {fmt(L)}, D = {fmt(D)}, F = {fmt(F_ROOT)};"]
    if part in ("both", "tones"):
        out.append({"swell": "const lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);",
                    "fade": "const lv = (s) => g * Math.pow(10, -sw * s / L / 20);",
                    "sigh": "const lv = (s) => g * (1 - (1 - Math.pow(10, -sw / 20)) * s / L);"}[env_])
        tones = _tones(sp)
        chorus = any(c for _r, _k, c in tones)
        tarr = "[" + ", ".join((f"[{fmt(r)}, {fmt(k)}, {fmt(c)}]" if chorus else f"[{fmt(r)}, {fmt(k)}]")
                               for r, k, c in tones) + "]"
        fexp = "F * r * Math.pow(2, c / 1200)" if chorus else "F * r"
        head = "const [r, k, c] of" if chorus else "const [r, k] of"
        every = (f"{fmt(EVERY)}" if mode == "offbeat" else f"Math.max(1, Math.round(f * {fmt(EVERY)})) / f")
        if mode == "struck":
            out += [f"for ({head} {tarr}){{",
                    f"  const f = {fexp};"]
            out += [l_.replace("dur: D", "dur: L + D") for l_ in _strike(sp, "t", "k * g", 2)]
            out.append("}")
        elif mode == "step":
            out += [f"for (const [r, k, s0, s1] of [[1, 1, 0, L / 2], [1.5, {fmt(KF)}, L / 2, L]]){{",
                    f"  const f = F * r, dt = {every};",
                    f"  const q = Math.pow(0.0001 / lv(s0), dt / D);",
                    "  for (let j = 0; s0 + j * dt < s1 - 1e-9; j++){",
                    f"    const s = s0 + j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, {fmt(A0)} / (1 - q)));"]
            out += _strike(sp, "t + s", "a", 4)
            out += ["  }", "}"]
        elif H:
            # the release reversed: the dyad re-struck on the SAME grid, climbing
            # from -34 dB over H, then the swell unwinding from the top over L
            out.append(f"const H = {fmt(H)};")
            out += [f"for ({head} {tarr}){{",
                    f"  const f = {fexp}, dt = {every};",
                    "  for (let j = 0; j * dt < H + L - 1e-9; j++){",
                    "    const u = j * dt, a = k * (u < H ? g * Math.pow(10, -1.7 * (1 - u / H)) : lv(u - H));"]
            out += _strike(sp, "t + u", "a", 4)
            out += ["  }", "}"]
        else:
            out += [f"for ({head} {tarr}){{",
                    f"  const f = {fexp}, dt = {every};",
                    "  const q = Math.pow(0.0001 / lv(0), dt / D);",
                    "  for (let j = 0; j * dt < L - 1e-9; j++){",
                    f"    const s = j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, {fmt(A0)} / (1 - q)));"]
            out += _strike(sp, "t + s", "a", 4)
            out += ["  }", "}"]
    if part in ("both", "breath") and sp.get("breath"):
        dur = round(min(0.58, H + L + 0.1), 4)
        if env_ == "swell":
            f0_, f1_, atk = 500, 900, round(min(L, 0.6 * dur), 4)
        else:
            f0_, f1_, atk = 900, 500, round(min(H + 0.03, 0.6 * dur), 4)
        out.append(f'this._sweep(t, {{ f0: {f0_}, f1: {f1_}, q: 1.2, gain: g * {fmt(kb)}, dur: {fmt(dur)}, '
                   f'atk: {fmt(atk)}, type:"bandpass" }});')
    return "\n".join(" " * ind + l_ for l_ in out)


# ============================================================== THE ENTRY ===
# "a foe entering -- a single bright note". One strike of C6 (or, SUNG, four
# strikes on whole cycles 11 ms apart rising 0.4 -> 1, the last ringing) with
# its partials (m, level re g, decay re D).
ENTER_CANDIDATES = [
    ("1 BELL", dict(f=F_NOTE, modes=[(2.0, 0.45, 0.7), (2.4, 0.3, 0.5), (3.0, 0.2, 0.4)]),
     "a small sanctus bell on C6: its octave, its minor-tenth (2.4) and its twelfth, each dying faster"),
    ("2 CHIME", dict(f=F_NOTE, modes=[(2.0, 0.5, 0.6), (3.0, 0.25, 0.4)]),
     "a struck harmonic chime on C6: its 2nd and 3rd partials at 0.5 / 0.25"),
    ("3 SUNG", dict(f=F_NOTE, modes=[(2.0, 0.4, 1.0), (3.0, 0.2, 1.0)], sung=True),
     "the choir's own voice, one note: C6 with 2nd and 3rd partials, four quick in-phase strikes rising "
     "0.4 -> 1, then ringing"),
    ("4 GLASS", dict(f=F_NOTE, modes=[(2.76, 0.35, 0.6)]),
     "a glass rod on C6: its 2.76 mode at 0.35"),
]


def note_body(sp, g, D, ind=10):
    arr = "[" + ", ".join(f"[{fmt(m)}, {fmt(a)}, {fmt(d)}]" for m, a, d in sp["modes"]) + "]"
    out = [f"const g = {fmt(g)}, f = {fmt(sp['f'])}, D = {fmt(D)};"]
    if sp.get("spark"):
        return "\n".join(" " * ind + l_ for l_ in
                         [f"const g = {fmt(g)};",
                          'this._tone(t, { freq: 1180 + 3 * 110, gain: g, dur: 0.20, type:"triangle" });'])

    def strike(T, G, ind_):
        o = [f'this._tone({T}, {{ freq: f, gain: {G}, dur: D, type:"sine" }}).frequency.value = f;']
        if sp["modes"]:
            o += [f"for (const [m, km, d] of {arr})",
                  f'  this._tone({T}, {{ freq: f * m, gain: {G} * km, dur: D * d, type:"sine" }})'
                  f'.frequency.value = f * m;']
        return [" " * ind_ + l_ for l_ in o]
    if sp.get("sung"):
        out += ["const dt = Math.max(1, Math.round(f * 0.011)) / f;",
                "for (let j = 0; j < 4; j++){",
                "  const s = j * dt, a = g * (0.4 + 0.2 * j);"]
        out += strike("t + s", "a", 2)
        out.append("}")
    else:
        out += strike("t", "g", 0)
    if sp.get("double"):
        out += ["{", "  const f = " + fmt(sp["f"] * 1.5) + ";"]
        out += strike("t + 0.12", "g", 2)
        out.append("}")
    return "\n".join(" " * ind + l_ for l_ in out)


# ============================================================== THE CLOSE ===
# "the swell reversed". Every candidate is the PICKED cast run backward:
#   MIRROR  its release as a short climb on the dyad (the measured release),
#           then the swell unwinding: the level falling sw dB over L
#   FADE    the same without the climb (the fall struck at its top)
#   SIGH    FADE falling in a straight line of amplitude, not of dB
CLOSE_CANDIDATES = [
    ("1 MIRROR", dict(env="fade", head="release"),
     "the whole cast reversed: its release as a short climb on the dyad, then the swell unwinding"),
    ("2 FADE", dict(env="fade", head=0.0),
     "the dyad from its top, the swell unwinding (the level falling the cast's depth over its length)"),
    ("3 SIGH", dict(env="sigh", head=0.0),
     "FADE falling in a straight line of amplitude instead of dB"),
    # ROUND 3 (see THE ROUNDS): a strike cannot stop, so a reversed onset rings on
    ("4 DEEP", dict(env="fade", head="release", depth=34.0),
     "MIRROR whose fall goes on down to the ear's floor (-34 dB) over the same length: the reversed onset is a "
     "stop, and a strike rings, so the fall carries it under hearing"),
    ("5 TIGHT", dict(env="fade", head="release", fit=True),
     "MIRROR with the fall's length solved so the whole is as long as the cast (the strikes' ring counted in)"),
]


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
ENTER_ANCHOR = '      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;'
BLESS_ANCHOR = '        T.bless += u.bless;'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHalo = null; continue; }'

ENTER_CODE = '''      /* BENEDICTION'S ENTRY (v82 s4: "a foe entering -- a single bright
         note"): an inside tick that follows an outside tick of the same
         window -- the foe crossing into the ring. `Z.voiceIn` is the voice's
         own memory of the last tick's inside test (1 / 0): born undefined
         with every cast, so a foe already inside when the halo rises is not
         an entry (the cast's swell has that moment). Nothing in the
         simulation reads it; the test is the ticker's own, repeated.
         Presentation only (aureole_voice_lab: fights identical). */
      const voiceIn = Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R;
      if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });
      Z.voiceIn = voiceIn ? 1 : 0;
'''

BLESS_CODE = '''
        /* BENEDICTION'S BLESSING (v82 s4: "the blessing -- the `spark
           collect` voice reused"): the EXISTING heal chime, unchanged, called
           as Zenith's tickSun calls it -- n = the blessing she now carries.
           Once per blessing, on its frame. Presentation only; nothing here
           is read back. */
        SFX.play("spark", { collect: true, n: f.stacks("blessing") });'''

CLOSE_CODE = '''      /* BENEDICTION'S CLOSE (v82 s4: "close -- the swell reversed"): on
         the frame the halo runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill flight, so both are left to the death voice
         (Tendril's, Canopy's, Zenith's and Lightkeeper's rule); a halo still
         up when the fight ends closes in the picture only. Presentation
         only; the next line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });
'''

# the sim-write control: the entry row with the foe nudged 1e-9 on an entry
ENTER_CODE_BAD = ENTER_CODE.replace(
    '      if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });',
    '      if (voiceIn && Z.voiceIn === 0){ foe.vx += 1e-9; SFX.play("ult", { w: "aureole-enter" }); }', 1)
assert ENTER_CODE_BAD != ENTER_CODE

SIM_ROWS = [(ENTER_ANCHOR, "before", ENTER_CODE), (BLESS_ANCHOR, "after", BLESS_CODE),
            (CLOSE_ANCHOR, "before", CLOSE_CODE)]
_refuse(ENTER_CODE + BLESS_CODE + CLOSE_CODE, "sim rows")
for _a, _m, _c in SIM_ROWS:
    assert _a not in _c, "a before/after row's code must not repeat its anchor"
    assert _c.isascii(), "a row must be ASCII"
    assert (_c.endswith("\n") if _m == "before" else _c.startswith("\n")), "a row's code must join its anchor"


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


def arms_code(Ca, En, Cl, info):
    cn, en, ln = (X["name"].split(maxsplit=1)[1] for X in (Ca, En, Cl))
    c_cast = _wrap([
        f'AUREOLE\'S CAST, THE HALO RISES -- v82 s4: "cast -- a soft choir swell (two re-struck tones, a '
        f'fifth), 0.5s". {cn}, of {info["n_cast"]}, picked on the numbers by `aureole_voice_lab.py` under '
        f'Rick\'s "you pick i overrule" (v110). Aureole had no arm and fell through to rune-crack, which '
        f'{info["n_rc"]} other relics on its stage-5 link still used, so this ADDS arms before that fallback '
        f'and leaves it alone.',
        f"{info['c_what']} Each tone is held by re-striking it in phase at its own whole cycles nearest every "
        f"11 ms (a held note does not exist in this toolkit), each strike {info['c_D']:g} s long, with "
        f"`.frequency.value` set on every strike, the first carrying 0.6 of its plateau. It swells "
        f"{info['c_swell']:+.1f} dB with no dip to a crest {info['c_at']:.0f} ms after the cast -- as the ring "
        f"finishes opening -- and is gone by {info['c_gone']:.0f} ms (audible {info['c_aud']:.0f}); both "
        f"tones within {info['c_cents']:.1f} cents and {info['c_bal']:.1f} dB of each other from the start to "
        f"the crest; flutter {info['c_flut']:.1f} dB; every partial a harmonic of C3 (a voice, not a chime), "
        f"nothing over 4.9x the root within {-info['c_soft']:.0f} dB of it (no edge). Its crest "
        f"{info['c_db']:+.1f} dB re Aureole's blow; {info['c_heard']:+.1f} dB over the score at its crest. "
        f"Register at most {info['c_reg']:.2f} against rune-crack, the sanctified and bow casts, BAR, the "
        f"seal, the blow and the death voice{info['c_peers']}."], 10)
    c_enter = _wrap([
        f'A FOE ENTERS THE HALO -- "a foe entering -- a single bright note" (v82 s4). {en}, of '
        f'{info["n_enter"]} (`aureole_voice_lab.py`). `tickHalo` plays it on an inside tick that follows an '
        f'outside tick of the same window.',
        f"{info['e_what']} One onset; its note {info['e_note']:.0f} Hz holds ({info['e_hold']:+.1f} cents) and "
        f"stands {info['e_tonal']:.0f} dB over the noise round it; its {info['e_ratio']:.2f}x partial "
        f"{info['e_lvl']:+.1f} dB re the note (bright); peak at {info['e_pk']:.0f} ms, audible "
        f"{info['e_aud']:.0f} ms; loudest 50 ms {info['e_db']:+.1f} dB re the blow and {info['e_wall']:+.1f} dB "
        f"re the wall tick. It shares a frame with the heal chime on most entries: register at most "
        f"{info['e_spark']:.2f} against it at any count, each keeping its own band within "
        f"{info['e_mask']:.1f} dB; at most {info['e_reg']:.2f} against the wall tick, hex-snap, the spark, "
        f"Zenith's tick, the bowstring, the blow, the clank and the cast."], 10)
    c_close = _wrap([
        f'THE HALO CLOSES -- "close -- the swell reversed" (v82 s4). {ln}, of {info["n_close"]} '
        f'(`aureole_voice_lab.py`): {info["l_what"]}',
        f"Its envelope correlates {info['l_corr']:.2f} with the cast's samples literally reversed; LATE "
        f"{info['l_late']:.2f} (the cast's {info['c_late']:.2f}); audible {info['l_aud']:.0f} ms; loudest 50 ms "
        f"{info['l_db']:+.1f} dB re the cast's (a reversal keeps its level). `tickHalo` plays it when the halo "
        f"runs out by its clock with both alive."], 10)
    return (f'{_arm_head(ME, "the halo rises")}\n'
            f'{c_cast}\n{dyad_body(Ca["sp"], Ca["g"], Ca["sw"], Ca["L"], Ca["D"], Ca["kb"])}\n'
            f'{_arm_head(ME + "-enter", "a foe comes inside")}\n'
            f'{c_enter}\n{note_body(En["sp"], En["g"], En["D"])}\n'
            f'{_arm_head(ME + "-close", "and it closes")}\n'
            f'{c_close}\n{dyad_body(Cl["sp"], Cl["g"], Cl["sw"], Cl["L"], Cl["D"], Cl["kb"])}\n')


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
  for (const [k, kind, p] of [["cast", "ult", { w: "aureole" }], ["enter", "ult", { w: "aureole-enter" }],
                              ["close", "ult", { w: "aureole-close" }], ["spark", "spark", { collect: true, n: 3 }],
                              ["hit", "hit", { dmg: 12.5, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickHalo rows, applied to the real prototype and run beside the original;
# the survey of Benediction's windows comes out of the same runs. The wrapper
# sees every tickHalo call, so each tick's entry, blessing and close are read
# on the call that makes them.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "aureole";
  const R = AC.CONFIG.physics.ballR;
  const orig = P.tickHalo; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickHalo anchor occurs ${at} times in tickHalo()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  for (const nm of ["STATUS", "CONFIG"])
    if ((0, eval)("typeof " + nm) === "undefined") return { err: nm + " is not reachable from the patched ticker" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = [], other = []; let step = 0, inL = 0, castV = 0, castBad = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = p && typeof p.w === "string" ? p.w : "";
      if (inL) calls.push({ step, kind, w, n: p && p.n !== undefined ? p.n : null, collect: !!(p && p.collect),
                            keys: Object.keys(p || {}).sort().join(",") });
      else {
        other.push([step, kind, JSON.stringify(p || {})]);
        if (kind === "ult" && w === ME){ castV++; if (Object.keys(p).join(",") !== "w") castBad++; }
        if (kind === "ult" && w.startsWith(ME + "-")) castBad += 1000;
      }
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    const wins = []; let W = null, stray = 0;
    P.tickHalo = function(dt){
      const Z0 = f.ultHalo, b0 = f.haloTally ? f.haloTally.bless : 0, c0 = calls.length;
      if (Z0 && (!W || W.Z !== Z0)){
        W = { Z: Z0, castStep: step, cast: m.t, prev: null, firstIn: null, ticks: 0, entries: 0, enterV: 0,
              blessings: 0, blessV: 0, closeV: 0, badEnter: 0, badBless: 0, badKeys: 0, nh: [0, 0, 0, 0, 0, 0, 0],
              withBless: 0, end: null, close: null, enterT: [] };
        wins.push(W);
      }
      inL++;
      try { return impl.call(this, dt); }
      finally {
        inL--;
        const mine = calls.slice(c0);
        if (Z0){
          const e = mine.filter(c => c.kind === "ult" && c.w === ME + "-enter");
          const bl = mine.filter(c => c.kind === "spark");
          const cl = mine.filter(c => c.kind === "ult" && c.w === ME + "-close");
          if (mine.length !== e.length + bl.length + cl.length) W.badKeys += 1000;
          W.enterV += e.length; W.blessV += bl.length; W.closeV += cl.length;
          for (const c of e.concat(cl)) if (c.keys !== "w") W.badKeys++;
          const nb = (f.haloTally ? f.haloTally.bless : 0) - b0 > 0 ? 1 : 0;
          W.blessings += nb;
          if (bl.length !== nb) W.badBless++;
          for (const c of bl){
            if (c.keys !== "collect,n" || !c.collect || c.n !== f.stacks("blessing")) W.badBless++;
            W.nh[Math.min(6, Math.max(0, c.n | 0))]++;
          }
          if (f.ultHalo === Z0){
            const inside = Math.hypot(foe.x - f.x, foe.y - f.y) < f.w.ult.haloR + R;
            if (W.prev === null) W.firstIn = inside;
            const ent = inside && W.prev === false;
            if (ent){ W.entries++; W.enterT.push(m.t); if (nb) W.withBless++; }
            if (e.length !== (ent ? 1 : 0)) W.badEnter++;
            W.prev = inside; W.ticks++;
          } else {
            if (e.length || bl.length) W.badEnter++;
            W.end = (Z0.t >= Z0.dur && f.alive && foe.alive) ? "clock"
                  : !f.alive ? "caster" : !foe.alive ? "foe" : "?";
            W.close = m.t;
          }
        } else stray += mine.length;
      }
    };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; } }
    finally { P.tickHalo = orig; if (had) S.play = op; else delete S.play; }
    for (const w of wins) if (!w.end) w.end = "over";
    const fr = (x) => [x.hp, x.x, x.y, x.vx, x.vy, x.charge, x.theta, x.alive,
                       x.stacks("smite"), x.stacks("blessing")];
    const Z = f.ultHalo, vIn = Z ? (Z.voiceIn === undefined ? "u" : Z.voiceIn) : "-";
    const Zs = Z ? Object.keys(Z).filter(k => k !== "voiceIn").sort().map(k => [k, Z[k]]) : null;
    return { sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.shots.length,
                                  m.shots.map(s => [s.x, s.y, s.vx, s.vy]),
                                  m.winner ? m.winner.w.id : null, f.haloTally || null, Zs]),
             vIn, calls, other: JSON.stringify(other), stray, castV, castBad,
             casts: f.haloTally ? f.haloTally.casts : 0,
             wins: wins.map(w => { const { Z, ...r } = w; return r; }) };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, caster: 0, foe: 0, over: 0, "?": 0 };
  let casts = 0, castV = 0, castT = 0, unticked = 0, entries = 0, enterV = 0, blessings = 0, blessV = 0, closes = 0;
  let firstIn = 0, withBless = 0, zOpen = 0; const nh = [0, 0, 0, 0, 0, 0, 0], pick = [], gaps = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.calls.length) bad.push([fid, sd, "the UNPATCHED ticker played", A.calls.length]);
    if (B.vIn !== "-") zOpen++;
    if (B.castV !== B.casts || B.castBad) bad.push([fid, sd, "cast voices vs casts", B.castV, B.casts, B.castBad]);
    castT += B.casts; castV += B.castV; unticked += B.casts - B.wins.length;
    if (B.stray) bad.push([fid, sd, "halo voices from tickHalo with no halo standing", B.stray]);
    casts += B.wins.length;
    for (const W of B.wins){
      ends[W.end]++; entries += W.entries; enterV += W.enterV; blessings += W.blessings; blessV += W.blessV;
      closes += W.closeV; withBless += W.withBless; if (W.firstIn) firstIn++;
      W.nh.forEach((v, i) => nh[i] += v);
      for (let i = 1; i < W.enterT.length; i++) gaps.push(W.enterT[i] - W.enterT[i - 1]);
      if (W.badEnter) bad.push([fid, sd, "an entry note where there was no entry (or none where there was)", W.badEnter]);
      if (W.badBless) bad.push([fid, sd, "a heal chime that is not one per blessing with its count", W.badBless]);
      if (W.badKeys) bad.push([fid, sd, "a halo voice with unexpected opts", W.badKeys]);
      if (W.closeV !== (W.end === "clock" ? 1 : 0)) bad.push([fid, sd, W.end + " close played closes", W.closeV]);
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close,
                                         entries: W.entries, blessings: W.blessings, firstIn: W.firstIn });
    }
  }
  gaps.sort((x, y) => x - y);
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, castT, unticked, entries, enterV,
           blessings, blessV, closes, firstIn, withBless, zOpen, nh, pick,
           gapMin: gaps.length ? gaps[0] : null, gapP5: gaps.length ? gaps[Math.floor(gaps.length * 0.05)] : null,
           gapMed: gaps.length ? gaps[gaps.length >> 1] : null, gaps02: gaps.filter(g => g < 0.2).length,
           ngaps: gaps.length, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is ("bless" = a heal chime from inside tickHalo).
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "aureole";
  const orig = P.tickHalo; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = []; let inL = 0;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w
              : (inL && kind === "spark") ? "bless" : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickHalo = function(dt){ inL++; try { return patched.call(this, dt); } finally { inL--; } };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickHalo = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "aureole";
  const R = AC.CONFIG.physics.ballR;
  const res = [];
  if (!P.tickHalo) return { err: "no tickHalo" };
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    let inL = 0;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, inL, null]);
      else if (inL && kind === "spark") log.push(["bless", inL, p.n]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const th = P.tickHalo; let clock = 0, entries = 0, blessings = 0, badN = 0, prevZ = null, prev = null;
    P.tickHalo = function(dt){
      const Z0 = f.ultHalo, b0 = f.haloTally ? f.haloTally.bless : 0, c0 = log.length;
      if (Z0 !== prevZ){ prevZ = Z0; prev = null; }
      inL = 1;
      try { return th.call(this, dt); }
      finally {
        inL = 0;
        if (Z0){
          if ((f.haloTally ? f.haloTally.bless : 0) > b0) blessings++;
          for (const e of log.slice(c0)) if (e[0] === "bless" && e[2] !== f.stacks("blessing")) badN++;
          if (f.ultHalo === Z0){
            const inside = Math.hypot(foe.x - f.x, foe.y - f.y) < f.w.ult.haloR + R;
            if (inside && prev === false) entries++;
            prev = inside;
          } else if (Z0.t >= Z0.dur && f.alive && foe.alive) clock++;
        }
      } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { P.tickHalo = th; if (had) S.play = op; else delete S.play; }
    const T = f.haloTally || {};
    const fr = (x) => [x.hp, x.x, x.y, x.vx, x.vy, x.charge, x.theta, x.alive, x.stacks("smite"), x.stacks("blessing")];
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.shots.length,
                                    m.winner ? m.winner.w.id : null, f.haloTally || null]),
               casts: T.casts || 0, entries, blessings, clock, badN,
               castV: log.filter(e => e[0] === ME && !e[1]).length,
               enterV: log.filter(e => e[0] === ME + "-enter" && e[1]).length,
               blessV: log.filter(e => e[0] === "bless").length,
               closeV: log.filter(e => e[0] === ME + "-close" && e[1]).length,
               stray: log.filter(e => e[0] !== "bless" && (e[0] === ME) === !!e[1]).length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def _spec(x, a, b):
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    return np.abs(np.fft.rfft(seg, NF)), np.fft.rfftfreq(NF, 1 / SR)


def _parab(X, i, NF=1 << 18):
    np = _np()
    y0, y1, y2 = np.log(X[i - 1:i + 2] + 1e-20)
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
    return (i + d) * SR / NF


def tone_at(X, fr, f):
    """TONES: the FFT peak within 6% of f -- (cents off f, level dB)."""
    np = _np()
    m = np.nonzero((fr > f * 0.94) & (fr < f * 1.06))[0]
    i = int(m[np.argmax(X[m])])
    return cents(_parab(X, i), f), db(float(X[i]))


def tones_at(x, a, b):
    """Both tones over [a, b] s: the larger cents off, the weaker re the stronger (dB), each tone's (c, lvl)."""
    X, fr = _spec(x, a, b)
    r0 = tone_at(X, fr, F_ROOT)
    r1 = tone_at(X, fr, F_ROOT * 1.5)
    return max(abs(r0[0]), abs(r1[0])), -abs(r0[1] - r1[1]), (r0, r1)


def harm_off(x, a, b, f0=C3, lo=200.0, hi=3000.0, within=20.0):
    """CHOIR: the worst cents between a spectral peak (within `within` dB of
    the strongest, lo-hi) and the nearest whole multiple of f0; and where."""
    np = _np()
    X, fr = _spec(x, a, b)
    m = np.nonzero((fr > lo) & (fr < hi))[0]
    Xm = X[m]; top = Xm.max()
    worst, at = 0.0, 0.0
    for k in range(1, len(m) - 1):
        if Xm[k] >= Xm[k - 1] and Xm[k] >= Xm[k + 1] and Xm[k] >= top * 10 ** (-within / 20):
            fp = _parab(X, int(m[k]))
            n = max(1, round(fp / f0))
            off = abs(cents(fp, n * f0))
            if off > worst:
                worst, at = off, fp
    return worst, at


def edge(x, a, b, f_root=F_ROOT, mult=4.9, hi=12000.0):
    """SOFT: the strongest peak at or above mult x the root, re the root's, dB."""
    np = _np()
    X, fr = _spec(x, a, b)
    ref = float(X[(fr > f_root * 0.94) & (fr < f_root * 1.06)].max())
    top = float(X[(fr >= mult * f_root) & (fr <= hi)].max())
    return db(top / ref)


def crest_heard(x, p90, B):
    """CREST-HEARD: HEARD read over the 100 ms centred on TOP."""
    np = _np()
    a = int((T0 + B["top_at"] - 0.05) * SR)
    y = np.concatenate([x[:int(T0 * SR)], x[a:]])
    return heard(y, p90)


def rerise(x, B):
    """RERISE: after the top, the most E50 climbs back over its running minimum, dB."""
    np = _np()
    y = x[int(T0 * SR):]
    r50, c50 = env(y, 0.05)
    e = 20 * np.log10(np.maximum(r50, 1e-9))
    k = (c50 >= B["top_at"]) & (c50 <= B["gone"] / 1000)
    e = e[k]
    if len(e) < 2:
        return 0.0
    run = np.minimum.accumulate(e)
    return float((e - run).max())


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v82 section 4 turned into a number; a
# rule no candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.5s': AUDIBLE 415-585 ms; 'swell': SWELL +8..+16 dB, no DIPS on the way up, "
    "TOP centred 300-450 ms after the cast (the ring open); 'two re-struck tones, a "
    "fifth': TONES -- C4 and G4 each within 30 cents and the weaker within 6 dB of the "
    "stronger over the START (20-100 ms) AND over the CREST (sounding together), held "
    "evenly: FLUTTER <= 3 dB (read at C4); 'choir': CHOIR -- every peak within 20 dB "
    "of the strongest (200-3000 Hz, the crest) within 25 cents of a harmonic of C3; "
    "'soft': SOFT -- nothing at or over 4.9x the root within 30 dB of it. Heard: "
    "CREST-HEARD >= +6 dB and HEARD (the first 100 ms) >= 0 dB. Register against "
    "rune-crack, each sanctified and bow cast with a voice of its own, BAR, the seal, "
    "the hit @ 12.5 and the death voice -- and Angelus's cast and close when its rows "
    "are given -- each <= 0.80. Level: TOP between 0.5x the hit @ 12.5's loudest 50 ms "
    "on its LOUDEST draw and 1.0x on its QUIETEST (heard like a blow, never over one), "
    "on every draw. Tiebreak: the most distinct register (to 0.05), then the fewest "
    "synth calls, then the order listed.")

ENTER_RULE = (
    "'single': one ONSET (0-400 ms); 'note': TONAL >= 15 dB over 500-12000 Hz and it "
    "holds (the pitch over 60-120 ms within 30 cents of 10-60 ms); 'bright': its note "
    "(FFT peak 500-12000 Hz, first 50 ms) >= 1000 Hz and its strongest overtone "
    "(1.5x-4x the note, first 50 ms) within 12 dB of it; 'entering' is a moment: the "
    "peak inside 50 ms, and a note, not a tick: AUDIBLE 120-350 ms. Level: its loudest "
    "50 ms >= 2x the wall tick's (loudest draw) and <= 0.7x the hit @ 12.5's (quietest "
    "draw); HEARD >= +6 dB; PHONE >= the bowstring's. It shares a frame with the heal "
    "chime: register against the spark collect at every count 1-5 <= 0.50 and "
    "SAME-FRAME <= 1 dB each way; register against the wall tick, hex-snap, the spark "
    "arm and burn, Zenith's tick (0-4), the bowstring, the hit @ 12.5, the clank and "
    "the picked cast each <= 0.80. Tiebreak: the lowest register against the heal "
    "chime (to 0.05), then the most distinct register overall (to 0.05), then the "
    "fewest synth calls, then the order listed.")

CLOSE_RULE = (
    "'the swell reversed' -- the envelope: ENV-CORR with the LITERAL reversal >= 0.80 "
    "(aligned at the audible onsets), LATE <= 0.50 (its energy early: its centre in the "
    "first half of its sound, where the cast's 0.55 is in the second -- round 3), PLACE <= 0.50 "
    "(its top in the first half of its sound: (TOP - onset) / AUDIBLE -- round 4), and after its "
    "top it never climbs back more than 1.5 dB (RERISE); the figure: TONES over its "
    "top (both tones, within 30 cents and 6 dB), CHOIR and SOFT as the cast's, "
    "FLUTTER <= 3 dB; the length: AUDIBLE within 15% of the cast's; the level: TOP "
    "within 3 dB of the cast's (a reversal keeps its level; v82 does not say quiet). "
    "Heard: CREST-HEARD >= +6 dB (round 3; round 2 read the first 100 ms). Tiebreak: the highest ENV-CORR (to 0.01), then the fewest "
    "synth calls, then the order listed.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def _regs_why(M, why, cap=0.80, keys=None):
    for k, v in M["regs"].items():
        if (keys is None or k in keys) and v > cap:
            why.append(f"register vs {k} {v:.2f} > {cap:.2f}")


def cast_why(M, lev):
    why = []
    if not 415 <= M["aud"] <= 585: why.append(f"audible {M['aud']:.0f} ms, not 415-585")
    if not 8 <= M["swell"] <= 16: why.append(f"swell {M['swell']:+.1f} dB, not +8..+16")
    if M["dips"]: why.append(f"{M['dips']} dips on the way up")
    if not 0.300 <= M["top_at"] <= 0.450: why.append(f"top at {M['top_at'] * 1000:.0f} ms, not 300-450")
    for w_ in ("s", "c"):
        nm = {"s": "start", "c": "crest"}[w_]
        if M[f"tc_{w_}"] > 30: why.append(f"a tone {M[f'tc_{w_}']:.0f} c off at the {nm}")
        if M[f"tb_{w_}"] < -6: why.append(f"the weaker tone {M[f'tb_{w_}']:+.1f} dB at the {nm} (not two tones)")
    if M["flut"] > FLUTTER_MAX: why.append(f"flutter {M['flut']:.1f} dB > {FLUTTER_MAX:g}")
    if M["harm"] > 25: why.append(f"a peak {M['harm']:.0f} c off the harmonics at {M['harm_at']:.0f} Hz (not a voice)")
    if M["soft"] > -30: why.append(f"an edge {M['soft']:+.1f} dB re the root at >= 4.9x (not soft)")
    if M["heard_c"] < 6: why.append(f"crest heard {M['heard_c']:+.1f} dB < +6")
    if M["heard"] < 0: why.append(f"start heard {M['heard']:+.1f} dB < 0")
    _regs_why(M, why)
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    return why


def enter_why(M, lev):
    why = []
    if M["n_on"] != 1: why.append(f"{M['n_on']} onsets (not single)")
    if M["tonal"] < 15: why.append(f"tonal {M['tonal']:.1f} dB < 15 (not a note)")
    if abs(M["hold"]) > 30: why.append(f"its pitch moves {M['hold']:+.0f} c")
    if M["note"] < 1000: why.append(f"its note {M['note']:.0f} Hz < 1000 (not bright)")
    if M["over"] < -12: why.append(f"its overtone {M['over']:+.1f} dB re the note (not bright)")
    if M["pk_ms"] > 50: why.append(f"peaks at {M['pk_ms']:.0f} ms")
    if not 120 <= M["aud_max"] <= 350: why.append(f"audible {M['aud_max']:.0f} ms, not 120-350")
    if M["top_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    if M["phone_min"] < lev["phone"]: why.append(f"phone {M['phone_min']:.4f} < the bowstring's {lev['phone']:.4f}")
    if M["spark_reg"] > 0.50: why.append(f"register vs the heal chime {M['spark_reg']:.2f} > 0.50")
    if M["mask"] > 1.0: why.append(f"on one frame with the heal chime a band moves {M['mask']:.1f} dB > 1")
    _regs_why(M, why)
    return why


def close_why(M, lev):
    why = []
    if M["corr"] < 0.80: why.append(f"env-corr {M['corr']:.2f} < 0.80")
    if M["late"] > 0.50: why.append(f"late {M['late']:.2f} > 0.50")
    if M["place"] > 0.50: why.append(f"its top at {M['place']:.2f} of its sound, not in the first half")
    if M["rerise"] > 1.5: why.append(f"climbs {M['rerise']:.1f} dB after its top")
    if M["tc_c"] > 30: why.append(f"a tone {M['tc_c']:.0f} c off at its top")
    if M["tb_c"] < -6: why.append(f"the weaker tone {M['tb_c']:+.1f} dB at its top")
    if M["harm"] > 25: why.append(f"a peak {M['harm']:.0f} c off the harmonics")
    if M["soft"] > -30: why.append(f"an edge {M['soft']:+.1f} dB (not soft)")
    if M["flut"] > FLUTTER_MAX: why.append(f"flutter {M['flut']:.1f} dB > {FLUTTER_MAX:g}")
    if abs(M["aud"] - lev["aud"]) > 0.15 * lev["aud"]:
        why.append(f"audible {M['aud']:.0f} ms, not {lev['aud']:.0f} +/- 15%")
    if abs(db(M["top"] / lev["top"])) > 3: why.append(f"top {db(M['top'] / lev['top']):+.1f} dB re the cast")
    if M["heard_c"] < 6: why.append(f"crest heard {M['heard_c']:+.1f} dB < +6")
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


def _slug(name):
    return name.replace(" ", "-").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Aureole's stage 5 (the halo and its blessing)")
    ap.add_argument("--also", action="append", default=[],
                    help="another link carrying Aureole (e.g. carried onto a newer tip): the rows as text there")
    ap.add_argument("--out", default="../05-reference/v110")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=110601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "enter": ENTER_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickHalo inside test", ENTER_ANCHOR),
                    ("tickHalo blessing", BLESS_ANCHOR), ("tickHalo close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("aureole-enter", "aureole-close", '(w === "aureole")', "voiceIn"):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nBENEDICTION -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
        W_ = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape, w.dmg, w.ult && w.ult.kind])")
        ids = [w_[0] for w_ in W_]
        if ME not in ids:
            raise SystemExit("no aureole in this build")
        me = [w_ for w_ in W_ if w_[0] == ME][0]
        if abs(me[3] - BLADE) > 1e-9 or me[4] != "halo":
            raise SystemExit(f"Aureole is {me} -- this lab levels against blade {BLADE} and a halo")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        if play_src.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx anchor is not in play() exactly once")

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

        def play(kind, p, seed=None):
            return R([["play", T0, kind, p]], seed=seed, new=False)[0]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, (kind, p) in [("rune-crack", ("ult", {"w": "spellbreaker"})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                ("hit@12.5", ("hit", {"dmg": BLADE, "crit": False})),
                                ("wall", ("wall", {})), ("death", ("death", {})), ("seal", ("seal", {})),
                                ("loose", ("loose", {"bal": False})), ("spark3", ("spark", {"collect": True, "n": 3})),
                                ("zenith", ("ult", {"w": "morningstar"}))]:
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
        print(f"  rune-crack today (max |diff| <= 1e-6 vs ult/spellbreaker), {len(fall_ids)} relics: "
              + ", ".join(fall_ids))
        if ME not in fall_ids:
            raise SystemExit("Aureole's cast is not rune-crack today -- this lab adds its arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_[0] for w_ in W_ if w_[1] == SCHOOL_AFF and w_[0] not in fall_ids]
        types = [w_[0] for w_ in W_ if w_[2] == TYPE_SHAPE and w_[0] not in fall_ids]
        print(f"  the sanctified casts with their own voice: {', '.join(school) or '-'};  the bow casts': "
              f"{', '.join(types) or '-'}")

        # the noise draws of every reference
        REFS = {"hit": ("hit", {"dmg": BLADE, "crit": False}), "wall": ("wall", {}),
                "rune-crack": ("ult", {"w": "spellbreaker"}), "death": ("death", {}), "BAR": ("ult", {"w": "axiom"}),
                "seal": ("seal", {}), "clank": ("clank", {"mass": 3}), "hex-snap": ("hex-snap", {}),
                "spark-arm": ("spark", {"arm": True}), "spark-burn": ("spark", {"collect": False}),
                "loose": ("loose", {"bal": False})}
        for n_ in range(1, 6):
            REFS[f"spark{n_}"] = ("spark", {"collect": True, "n": n_})
        for n_ in range(0, 5):
            REFS[f"zenith-tick{n_}"] = ("ult", {"w": "morningstar-tick", "n": n_})
        for w_ in school + types:
            REFS[w_] = ("ult", {"w": w_})
        RD_ = {k: [] for k in REFS}
        RX = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (kind, p) in REFS.items():
                x = play(kind, p, seed=sd)
                RX[k].append(x)
                RD_[k].append(basic(x))
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD_.items()}
        # the school's other choir on the batch line (Angelus), from its own rows
        peer_regs, peer_names = [], []
        for pf, prow in peer_sfx:
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            for w_ in ("angelus", "angelus-close"):
                if any(f'w === "{w_}"' in c for _a, c in ps):
                    RB["peer:" + w_] = [bands(R([["arm", T0, "ult", {"w": w_}]], rows=ps, new=False)[0][int(T0 * SR):])]
                    peer_regs.append("peer:" + w_)
                    if peer_name(pf) not in peer_names:
                        peer_names.append(peer_name(pf))
        h_lo, h_hi = min(m_["top"] for m_ in RD_["hit"]), max(m_["top"] for m_ in RD_["hit"])
        w_hi = max(m_["top"] for m_ in RD_["wall"])
        ph_bow = max(phone(x) for x in RX["loose"])
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD_['hit']):.3f}-{max(m_['peak'] for m_ in RD_['hit']):.3f};  the wall "
              f"tick: {min(m_['top'] for m_ in RD_['wall']):.4f}-{w_hi:.4f};  PHONE: the bowstring {ph_bow:.4f} "
              f"(loudest draw)")
        if peer_regs:
            print(f"  the school's choir on the batch line, from --peer-rows: {', '.join(peer_regs)}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        p90 = bed_p90(bed[int(2 * SR):int(10 * SR)])
        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, phone_bow=ph_bow)
        wav("aureole-ctl-runecrack.wav", rcx)
        wav("aureole-ctl-hit12.5.wav", ctl["hit@12.5"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a soft choir swell (two re-struck tones, a fifth), 0.5s'. C4-G4 (just), the fifth at "
              f"{KF:g}, each strike {CAST_D:g} s. Level-matched: the swell's length so "
              f"TOP is centred {CREST_AT * 1000:.0f} ms in, its depth so SWELL is +{SWELL_DB:g} dB, TOP {tgt_c:.4f} "
              f"(the centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}); a breath {BREATH_DB:g} dB under")

        def cx(sp, g, sw, L, D, kb=0.0, part="both", seed=None):
            return R([["body", T0, dyad_body(sp, g, sw, L, D, kb, part), {}]], seed=seed)

        def calib_cast(sp):
            g, sw, L, D, kb = 0.012, 14.0, 0.35, CAST_D, 0.3
            for _ in range(5):
                if sp.get("breath"):
                    tt = basic(cx(sp, g, sw, L, D, kb, "tones")[0])["top"]
                    bt = basic(cx(sp, g, sw, L, D, kb, "breath")[0])["top"]
                    kb = float(f"{kb * tt * 10 ** (-BREATH_DB / 20) / bt:.4g}")
                B = basic(cx(sp, g, sw, L, D, kb)[0])
                L = round(min(0.5, max(0.2, L + (CREST_AT - B["top_at"]))), 3)
                sw = round(min(24.0, max(4.0, sw + (SWELL_DB - db(B["top"] / max(B["start"], 1e-12))))), 2)
                g = float(f"{g * tgt_c / basic(cx(sp, g, sw, L, D, kb)[0])['top']:.4g}")
            return g, sw, L, D, kb

        CAST_REGS = ["rune-crack"] + school + types + ["BAR", "seal", "hit", "death"] + peer_regs

        def dyad_measure(name, x, draws, calls, regs=CAST_REGS):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            M["swell"] = db(M["top"] / max(M["start"], 1e-12))
            M["dips"], M["lin"] = dips_and_lin(x, M["top_at"])
            M["tc_s"], M["tb_s"], M["t_s"] = tones_at(x, T0 + 0.02, T0 + 0.10)
            ca, cb = T0 + M["top_at"] - 0.05, T0 + M["top_at"] + 0.05
            M["tc_c"], M["tb_c"], M["t_c"] = tones_at(x, ca, cb)
            fa, fb_ = T0 + M["a0"] / 1000 + 0.05, T0 + M["gone"] / 1000 - 0.05
            M["flut"] = flutter(x, fa, fb_, F_ROOT) if fb_ - fa >= 0.12 else 99.0
            M["harm"], M["harm_at"] = harm_off(x, ca, cb)
            M["soft"] = edge(x, ca, cb)
            M["heard"], M["heard_fc"] = heard(x, p90)
            M["heard_c"], M["heard_cfc"] = crest_heard(x, p90, M)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in regs}
            return M

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<12}{M.get('g', 0):>8.4g}{M.get('sw', 0):>6.4g}{M.get('L', 0):>6.3f}"
                  f"{M.get('D', 0):>6.3f}{M['calls']:>6d}{M['top']:>8.4f}{M['top_at'] * 1000:>5.0f}{M['aud']:>5.0f}"
                  f"{M['swell']:>6.1f}{M['dips']:>3d}{M['tc_s']:>5.0f}{M['tb_s']:>6.1f}{M['tc_c']:>5.0f}"
                  f"{M['tb_c']:>6.1f}{M['flut']:>5.1f}{M['harm']:>6.0f}{M['soft']:>7.1f}{M['heard']:>6.1f}"
                  f"{M['heard_c']:>6.1f}{M['cen']:>6.0f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        hdr_c = (f"  {'cand':<12}{'g':>8}{'sw':>6}{'L':>6}{'D':>6}{'calls':>6}{'top':>8}{'@ms':>5}{'aud':>5}"
                 f"{'swell':>6}{'dp':>3}{'c0':>5}{'b0':>6}{'cC':>5}{'bC':>6}{'flut':>5}{'harm':>6}{'edge':>7}"
                 f"{'hrd0':>6}{'hrdC':>6}{'cen':>6}{'reg':>6}")
        print(hdr_c)
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g, sw, L, D, kb = calib_cast(sp)
            x, calls = cx(sp, g, sw, L, D, kb)
            x2, _ = cx(sp, g, sw, L, D, kb)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"cast {name} does not reproduce")
            draws = [cx(sp, g, sw, L, D, kb, seed=sd)[0] for sd in NOISE_SEEDS] if sp.get("breath") else [x]
            M = dyad_measure(name, x, draws, calls[0])
            M.update(sp=sp, g=g, sw=sw, L=L, D=D, kb=kb); M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"aureole-cast-{_slug(name)}.wav", x)
        # the controls, on VOWEL (the school's choir voice) and its levels
        c0 = rows_c[2]
        ctlc = []
        for cname, csp in (("0 STEP", dict(c0["sp"], mode="step")), ("0 ONE", dict(c0["sp"], mode="one")),
                           ("0 STRUCK", dict(c0["sp"], mode="struck")),
                           ("0 OFFBEAT", dict(c0["sp"], mode="offbeat")),
                           ("0 BRIGHT", dict(c0["sp"], timbre="bright")),
                           ("0 BELL", dict(c0["sp"], parts=[(2.76, 0.3), (3, 0.12)]))):
            xc, cc = cx(csp, c0["g"], c0["sw"], c0["L"], c0["D"], c0["kb"])
            M = dyad_measure(cname, xc, [xc], cc[0]); M.update(sp=csp, g=c0["g"], sw=c0["sw"], L=c0["L"],
                                                             D=c0["D"], kb=c0["kb"])
            ctlc.append(M)
            wav(f"aureole-cast-{_slug(cname)}.wav", xc)
        M = dyad_measure("0 RUNECRACK", rcx, RX["rune-crack"], 0); ctlc.append(M)
        for M in ctlc:
            M["why"] = cast_why(M, lev_c); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<12} {blurb}")
        print("    0 STEP       VOWEL as Zenith's figure: the root for half the swell, then the fifth -- a control on "
              "'two tones' (together)\n"
              "    0 ONE        VOWEL's root alone -- a control on 'two tones'\n"
              "    0 STRUCK     VOWEL's two tones struck once each, ringing -- a control on 'swell' / 're-struck'\n"
              "    0 OFFBEAT    VOWEL re-struck a flat 11 ms apart, not on whole cycles (out of phase) -- a control "
              "on 're-struck' (Angelus's)\n"
              "    0 BRIGHT     VOWEL in Zenith's bright timbre (a triangle and its octave at 0.4) -- a control on "
              "'soft'\n"
              "    0 BELL       VOWEL with a bar's 2.76 mode for its 2nd partial -- a control on 'choir' (a voice)\n"
              "    0 RUNECRACK  the fallback it replaces")
        _show(rows_c, ctlc, CAST_RULE, "cast")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"]))
        Ca = rows_c[ci]
        print(f"  PICK  {Ca['name']}  g {Ca['g']}, sw {Ca['sw']}, L {Ca['L']}, D {Ca['D']}, kb {Ca['kb']}, "
              f"{Ca['calls']} synth calls; TOP {Ca['top']:.4f} = {db(Ca['top'] / h_lo):+.1f} dB re the hit @ "
              f"{BLADE:g} (quietest draw) at {Ca['top_at'] * 1000:.0f} ms; release {Ca['gone'] - 1000 * Ca['L']:.0f} ms")
        # RAW, a reference (not a control): the pick without .frequency.value = f
        xr, _ = cx(dict(Ca["sp"], raw=True), Ca["g"], Ca["sw"], Ca["L"], Ca["D"], Ca["kb"])
        MR = dyad_measure("  RAW", xr, [xr], 0)
        MR["why"] = cast_why(MR, lev_c)
        print(f"  RAW (a reference): max |diff| vs the pick {float(np.abs(xr - Ca['x']).max()):.3f}, top "
              f"{db(MR['top'] / Ca['top']):+.1f} dB, flutter {MR['flut']:.1f}, dips {MR['dips']} -- "
              f"{'passes' if not MR['why'] else 'fails: ' + '; '.join(MR['why'][:3])}")
        wav("aureole-cast-0-raw.wav", xr)

        # ---- THE ENTRY -----------------------------------------------------
        lev_e = dict(lo=2 * w_hi, hi=0.7 * h_lo, phone=ph_bow)
        tgt_e = math.sqrt(lev_e["lo"] * lev_e["hi"])
        print(f"\nENTRY -- 'a foe entering -- a single bright note'. C6 ({F_NOTE:g} Hz). Level-matched: the decay so "
              f"it is AUDIBLE {NOTE_AUD:g} ms, the loudest 50 ms {tgt_e:.4f} (the centre of {lev_e['lo']:.4f}-"
              f"{lev_e['hi']:.4f})")

        def ex(sp, g, D, seed=None):
            return R([["body", T0, note_body(sp, g, D), {}]], seed=seed)

        def calib_note(sp, aud=NOTE_AUD, fixD=None):
            g, D = 0.05, 0.4
            for _ in range(5):
                if fixD is None:
                    D = float(f"{min(3.0, max(0.005, D * aud / max(basic(ex(sp, g, D)[0])['aud'], 1.0))):.3g}")
                else:
                    D = fixD
                g = float(f"{g * tgt_e / basic(ex(sp, g, D)[0])['top']:.4g}")
            return g, D

        ENTER_REGS = ["wall", "hex-snap", "spark-arm", "spark-burn", "loose", "hit", "clank"] + \
            [f"zenith-tick{n_}" for n_ in range(5)]
        xs3 = RX["spark3"][0]

        def note_measure(name, sp, g, D):
            x, calls = ex(sp, g, D)
            draws = [x]
            M = basic(x); M.update(x=x, calls=calls[0], name=name, sp=sp, g=g, D=D)
            M["aud_max"] = max(basic(d_)["aud"] for d_ in draws)
            M["note"] = pitch(x, T0, T0 + 0.05, 500, 12000)
            M["ratio"], _off, M["over"] = inharm(x, T0, T0 + 0.05, M["note"])
            M["hold"] = cents(pitch(x, T0 + 0.06, T0 + 0.12, 500, 12000), pitch(x, T0 + 0.01, T0 + 0.06, 500, 12000))
            M["tonal"] = tonal(draws, T0, T0 + 0.1, 500, 12000)
            M["n_on"] = len(onsets(x))
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            M["heard"], M["heard_fc"] = heard(x, p90)
            M["phone_min"] = min(phone(d_) for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in ENTER_REGS}
            M["regs"]["cast"] = mreg(DB, Ca["DB"])
            M["sparks"] = {n_: mreg(DB, RB[f"spark{n_}"]) for n_ in range(1, 6)}
            M["spark_reg"] = max(M["sparks"].values())
            # SAME-FRAME: each voice's own loudest third-octave (first 100 ms, >= 200 Hz)
            # with and without the other on its frame -- rendered through the chain
            # together (the compressor is shared), the larger move, dB
            body = note_body(sp, g, D)
            xb, _ = R([["body", T0, body, {}], ["play", T0, "spark", {"collect": True, "n": 3}]], new=False)
            fe = own_band(x, T0, T0 + 0.1)
            fs = own_band(xs3, T0, T0 + 0.1)
            m1 = abs(db(band_rms(xb, fe, T0, T0 + 0.1) / max(band_rms(x, fe, T0, T0 + 0.1), 1e-12)))
            m2 = abs(db(band_rms(xb, fs, T0, T0 + 0.1) / max(band_rms(xs3, fs, T0, T0 + 0.1), 1e-12)))
            M["mask"] = max(m1, m2); M["mask_bands"] = (fe, fs)
            return M

        def enter_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['D']:>7.3g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud_max']:>5.0f}"
                  f"{M['pk_ms']:>5.0f}{M['n_on']:>4d}{M['note']:>7.0f}{M['hold']:>6.1f}{M['ratio']:>6.2f}"
                  f"{M['over']:>7.1f}{M['tonal']:>7.1f}{M['heard']:>7.1f}{M['phone_min']:>8.4f}{M['spark_reg']:>6.2f}"
                  f"{M['mask']:>6.2f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<10}{'g':>8}{'D':>7}{'calls':>6}{'top':>8}{'aud':>5}{'pk':>5}{'on':>4}{'note':>7}{'hold':>6}"
              f"{'over':>6}{'lvl':>7}{'tonal':>7}{'heard':>7}{'phone':>8}{'spark':>6}{'mask':>6}{'reg':>6}")
        rows_e = []
        for name, sp, _b in ENTER_CANDIDATES:
            g, D = calib_note(sp)
            x1, _ = ex(sp, g, D); x2, _ = ex(sp, g, D)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"entry {name} does not reproduce")
            M = note_measure(name, sp, g, D); M["why"] = enter_why(M, lev_e)
            rows_e.append(M); enter_line(M)
            wav(f"aureole-enter-{_slug(name)}.wav", M["x"])
        e0 = rows_e[1]
        ctle = []
        lsp = dict(e0["sp"], f=F_NOTE / 4)
        cg, cD = calib_note(lsp)
        ctle.append(note_measure("0 LOW", lsp, cg, cD))
        dsp = dict(e0["sp"], modes=[])
        cg, cD = calib_note(dsp)
        ctle.append(note_measure("0 DULL", dsp, cg, cD))
        ctle.append(note_measure("0 DOUBLE", dict(e0["sp"], double=True), e0["g"], e0["D"]))
        cg, cD = calib_note(e0["sp"], aud=30.0)
        ctle.append(note_measure("0 TICK", e0["sp"], cg, cD))
        ssp = dict(e0["sp"], spark=True)
        cg, _cD = calib_note(ssp, fixD=0.2)
        ctle.append(note_measure("0 SPARK", ssp, cg, 0.2))
        for M in ctle:
            M["why"] = enter_why(M, lev_e); enter_line(M)
            wav(f"aureole-enter-{_slug(M['name'])}.wav", M["x"])
        for (name, _sp, blurb) in ENTER_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 LOW      CHIME two octaves down (C4), levelled the same way -- a control on 'bright' (>= 1 kHz)\n"
              "    0 DULL     CHIME's note as a bare sine -- a control on 'bright' (an overtone)\n"
              "    0 DOUBLE   CHIME and its fifth 120 ms later -- a control on 'single'\n"
              "    0 TICK     CHIME dying in 30 ms -- a control on 'a note, not a tick'\n"
              "    0 SPARK    the heal chime's own shape (n = 3) at the entry's level -- a control on the register "
              "against the heal chime")
        _show(rows_e, ctle, ENTER_RULE, "entry")
        ok, fb = _gate(rows_e, "entry")
        ei = fb if ok is None else min(ok, key=lambda i: (round(rows_e[i]["spark_reg"] / 0.05),
                                                          round(max(rows_e[i]["regs"].values()) / 0.05),
                                                          rows_e[i]["calls"]))
        En = rows_e[ei]
        print(f"  PICK  {En['name']}  g {En['g']}, D {En['D']}; loudest 50 ms {db(En['top'] / h_lo):+.1f} dB re the "
              f"hit @ {BLADE:g}, {db(En['top_lo'] / w_hi):+.1f} dB re the wall; register vs the heal chime "
              f"{En['spark_reg']:.2f} (n " + " ".join(f"{k}:{v:.2f}" for k, v in En["sparks"].items()) + ")")

        # ---- THE BLESSING (the existing voice, measured) ----------------------
        print("\nBLESSING -- 'the blessing -- the `spark collect` voice reused': unchanged, n = the blessing count.")
        bl_info = {}
        for n_ in range(1, 6):
            xs = RX[f"spark{n_}"][0]
            Bs = basic(xs)
            hs, hfc = heard(xs, p90)
            bl_info[n_] = dict(top=Bs["top"], aud=Bs["aud"], heard=hs,
                               enter=mreg(RB[f"spark{n_}"], En["DB"]), cast=mreg(RB[f"spark{n_}"], Ca["DB"]))
            print(f"  n {n_}: pitch {pitch(xs, T0, T0 + 0.05, 500, 4000):.0f} Hz, loudest 50 ms {Bs['top']:.4f} "
                  f"({db(Bs['top'] / h_lo):+.1f} dB re the blow), audible {Bs['aud']:.0f} ms, heard {hs:+.1f} dB at "
                  f"{hfc:.0f} Hz; register vs the entry {bl_info[n_]['enter']:.2f}, vs the cast "
                  f"{bl_info[n_]['cast']:.2f}")
        rec["blessing"] = bl_info

        # ---- THE CLOSE -----------------------------------------------------
        release = max(0.01, round((Ca["gone"] - 1000 * Ca["L"]) / 1000 / 0.005) * 0.005)
        release = round(release, 3)
        print(f"\nCLOSE -- 'the swell reversed', on {Ca['name']}'s figure. MIRROR's climb = the pick's own release, "
              f"{release * 1000:.0f} ms. Level-matched: TOP = the cast's ({Ca['top']:.4f})")

        def close_sp(csp):
            s_ = dict(Ca["sp"], env=csp["env"])
            s_["head"] = release if csp.get("head") == "release" else (csp.get("head") or 0.0)
            return s_

        def calib_close(fsp, sw, L, target, fit=False):
            g = Ca["g"]
            for _ in range(4):
                if fit:
                    B_ = basic(cx(fsp, g, sw, L, Ca["D"], Ca["kb"])[0])
                    L = round(min(0.6, max(0.1, L + (Ca["aud"] - B_["aud"]) / 1000)), 3)
                g = float(f"{g * target / basic(cx(fsp, g, sw, L, Ca['D'], Ca['kb'])[0])['top']:.4g}")
            return g, L

        cbody = dyad_body(Ca["sp"], Ca["g"], Ca["sw"], Ca["L"], Ca["D"], Ca["kb"])
        gc = 1.0
        for _ in range(3):
            xl = pcm(page.evaluate(LIT_JS, [cbody, 3.0, gc]))
            gc = float(f"{gc * Ca['top'] / basic(xl)['top']:.4g}")
        xlit = pcm(page.evaluate(LIT_JS, [cbody, 3.0, gc]))
        assert not errors, errors[:3]
        if float(np.abs(xlit).max()) < 1e-6:
            raise SystemExit("the LITERAL rendered silence")
        wav("aureole-close-0-literal.wav", xlit)
        lev_l = dict(aud=Ca["aud"], top=Ca["top"])

        def at_onset(x):
            s_ = int(basic(x)["a0"] / 1000 * SR)
            return np.concatenate([x[s_:], np.zeros(s_)])

        xlit_on = at_onset(xlit)

        def close_measure(name, x, draws, calls):
            M = dyad_measure(name, x, draws, calls, regs=["rune-crack", "seal", "death"])
            M["corr"] = env_corr(at_onset(x), xlit_on)
            M["corr0"] = env_corr(x, xlit)
            M["rerise"] = rerise(x, M)
            M["place"] = (M["top_at"] * 1000 - M["a0"]) / max(M["aud"], 1e-9)
            return M

        def close_line(M):
            print(f"  {M['name']:<11}{M.get('g', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}"
                  f"{db(M['top'] / Ca['top']):>7.1f}{M['aud']:>6.0f}{M['late']:>6.2f}{M['place']:>6.2f}"
                  f"{M['rerise']:>7.1f}"
                  f"{M['corr']:>6.2f}{M['corr0']:>6.2f}{M['tc_c']:>5.0f}{M['tb_c']:>6.1f}{M['flut']:>5.1f}"
                  f"{M['harm']:>6.0f}{M['soft']:>7.1f}{M['heard']:>7.1f}{M['heard_c']:>7.1f}{M.get('sw', 0):>6.4g}"
                  f"{M.get('L', 0):>6.3f}{mreg(M['DB'], Ca['DB']):>6.2f}")

        print(f"  {'cand':<11}{'g':>8}{'calls':>6}{'top':>8}{'dB/c':>7}{'aud':>6}{'late':>6}{'place':>6}{'rerise':>7}{'corr':>6}"
              f"{'corr0':>6}{'cC':>5}{'bC':>6}{'flut':>5}{'harm':>6}{'edge':>7}{'hrd0':>7}{'hrdC':>7}{'sw':>6}{'L':>6}"
              f"{'cast':>6}")
        rows_l = []
        for name, csp, _b in CLOSE_CANDIDATES:
            fsp = close_sp(csp)
            sw_ = csp.get("depth", Ca["sw"])
            g, L_ = calib_close(fsp, sw_, Ca["L"], Ca["top"], fit=csp.get("fit", False))
            x, calls = cx(fsp, g, sw_, L_, Ca["D"], Ca["kb"])
            x2, _ = cx(fsp, g, sw_, L_, Ca["D"], Ca["kb"])
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            draws = ([cx(fsp, g, sw_, L_, Ca["D"], Ca["kb"], seed=sd)[0] for sd in NOISE_SEEDS]
                     if fsp.get("breath") else [x])
            M = close_measure(name, x, draws, calls[0])
            M.update(sp=fsp, g=g, sw=sw_, L=L_, D=Ca["D"], kb=Ca["kb"]); M["why"] = close_why(M, lev_l)
            rows_l.append(M); close_line(M)
            wav(f"aureole-close-{_slug(name)}.wav", x)
        m0 = rows_l[0]
        ctll = []
        M = close_measure("0 AGAIN", Ca["x"], [Ca["x"]], Ca["calls"]); M.update(g=Ca["g"], sw=Ca["sw"], L=Ca["L"])
        ctll.append(M)
        ssp = dict(m0["sp"], head=round(release / 2, 4))
        xs_, cs_ = cx(ssp, m0["g"], Ca["sw"], round(Ca["L"] / 2, 3), round(Ca["D"] / 2, 3), Ca["kb"])
        M = close_measure("0 SHORT", xs_, [xs_], cs_[0]); M["g"] = m0["g"]; ctll.append(M)
        gq = float(f"{m0['g'] * 10 ** (-QUIET_DB / 20):.4g}")
        xq_, cq_ = cx(m0["sp"], gq, Ca["sw"], Ca["L"], Ca["D"], Ca["kb"])
        M = close_measure("0 QUIET", xq_, [xq_], cq_[0]); M["g"] = gq; ctll.append(M)
        LM = close_measure("0 LITERAL", xlit, [xlit], 0); LM["g"] = gc
        for M in ctll:
            M["why"] = close_why(M, lev_l); close_line(M)
            if M["name"] != "0 AGAIN":
                wav(f"aureole-close-{_slug(M['name'])}.wav", M["x"])
        LM["why"] = close_why(LM, lev_l); close_line(LM)
        for (name, _sp, blurb) in CLOSE_CANDIDATES:
            print(f"    {name:<11} {blurb}")
        print("    0 AGAIN     the cast itself -- a control on 'reversed'\n"
              "    0 SHORT     MIRROR over half the length (and half the strike) -- a control on the length\n"
              f"    0 QUIET     MIRROR {QUIET_DB:g} dB under -- a control on the level (the batch's usual quiet close)\n"
              "    0 LITERAL   the cast's samples reversed -- the reference (cannot ship)")
        _show(rows_l, ctll, CLOSE_RULE, "close")
        print(f"  LITERAL (the reference) {'passes' if not LM['why'] else 'fails: ' + '; '.join(LM['why'])}")
        ok, fb = _gate(rows_l, "close")
        li = fb if ok is None else min(ok, key=lambda i: (-round(rows_l[i]["corr"], 2), rows_l[i]["calls"]))
        Cl = rows_l[li]
        print(f"  PICK  {Cl['name']}  g {Cl['g']}; ENV-CORR {Cl['corr']:.2f}; LATE {Cl['late']:.2f}; "
              f"{db(Cl['top'] / Ca['top']):+.1f} dB re the cast")

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        part_what = {(): "two sines",
                     ((2, 0.2),): "two sines, each strike carrying its 2nd partial at 0.2 (the 'oo' of a soft choir)",
                     ((2, 0.3), (3, 0.12)): "two sines, each strike carrying its 2nd and 3rd partials at 0.3 / 0.12"}
        pw = part_what.get(tuple(Ca["sp"]["parts"]), "two sines with partials " + str(Ca["sp"]["parts"]))
        c_what = (f"C4 and a just G4 (261.63 / 392.44 Hz, the score's III), the fifth at {KF:g} of the root, as {pw}"
                  + (", doubled by a second singer 4 cents sharp at half the level" if Ca["sp"].get("chorus") else "")
                  + (", over the choir's breath (a bandpass band 500 -> 900 Hz, 18 dB under)"
                     if Ca["sp"].get("breath") else "") + ".")
        e_what = {"1 BELL": "A small sanctus bell struck on C6 (1046.50 Hz, the halo's root two octaves up): its "
                            "octave, its minor tenth (2.4) and its twelfth over it, each dying faster.",
                  "2 CHIME": "A harmonic chime struck on C6 (1046.50 Hz, the halo's root two octaves up): its 2nd and "
                             "3rd partials at 0.5 / 0.25, each dying faster.",
                  "3 SUNG": "One sung note, C6 (1046.50 Hz, the halo's root two octaves up) with its 2nd and 3rd "
                            "partials: four quick in-phase strikes rising 0.4 -> 1, then ringing.",
                  "4 GLASS": "A glass rod struck on C6 (1046.50 Hz, the halo's root two octaves up), its 2.76 mode at "
                             "0.35."}[En["name"]]
        l_what = {"1 MIRROR": f"the cast run backward -- its release as a {release * 1000:.0f} ms climb on the dyad, "
                              f"then the swell unwinding, the level falling {Cl['sw']:g} dB over {Cl['L']:g} s.",
                  "2 FADE": f"the dyad from its top, the swell unwinding, the level falling {Cl['sw']:g} dB over "
                            f"{Cl['L']:g} s.",
                  "3 SIGH": f"the dyad from its top, falling in a straight line of amplitude to {Cl['sw']:g} dB "
                            f"under over {Cl['L']:g} s.",
                  "4 DEEP": f"the cast run backward -- its release as a {release * 1000:.0f} ms climb on the dyad, "
                            f"then the swell unwinding over the cast's own {Cl['L']:g} s, but on down to the ear's "
                            f"floor ({Cl['sw']:g} dB): the reversed onset is a stop, and a strike rings, so the fall "
                            f"carries it under hearing.",
                  "5 TIGHT": f"the cast run backward -- its release as a {release * 1000:.0f} ms climb on the dyad, "
                             f"then the swell unwinding {Cl['sw']:g} dB over {Cl['L']:g} s, the fall's length solved "
                             f"so the whole is as long as the cast."}[Cl["name"]]
        n_names = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                   "twelve", "thirteen", "fourteen", "fifteen"]
        nrc = len(fall_ids) - 1
        info = dict(
            n_cast=len(CAST_CANDIDATES), n_enter=len(ENTER_CANDIDATES), n_close=len(CLOSE_CANDIDATES),
            c_peers="".join(f", and {n_}'s cast and close" for n_ in peer_names),
            n_rc=n_names[nrc] if nrc <= 15 else str(nrc),
            c_what=c_what, c_D=Ca["D"], c_swell=Ca["swell"], c_at=Ca["top_at"] * 1000, c_gone=Ca["gone"],
            c_aud=Ca["aud"], c_cents=max(Ca["tc_s"], Ca["tc_c"]), c_bal=-min(Ca["tb_s"], Ca["tb_c"]),
            c_flut=Ca["flut"], c_soft=Ca["soft"], c_db=db(Ca["top"] / h_lo), c_heard=Ca["heard_c"],
            c_reg=max(Ca["regs"].values()), c_late=Ca["late"],
            e_what=e_what, e_note=En["note"], e_hold=En["hold"], e_tonal=En["tonal"], e_ratio=En["ratio"],
            e_lvl=En["over"], e_pk=En["pk_ms"], e_aud=En["aud_max"], e_db=db(En["top"] / h_lo),
            e_wall=db(En["top_lo"] / w_hi), e_spark=En["spark_reg"], e_mask=En["mask"],
            e_reg=max(En["regs"].values()),
            l_what=l_what, l_corr=Cl["corr"], l_late=Cl["late"], l_aud=Cl["aud"], l_db=db(Cl["top"] / Ca["top"]))
        arms = arms_code(Ca, En, Cl, info)
        _refuse(arms, "Sfx row")
        if not arms.isascii():
            raise SystemExit("the Sfx row is not ASCII")
        if SFX_ANCHOR in arms or not arms.endswith("\n"):
            raise SystemExit("the Sfx row must sit before its anchor without repeating it")
        sfx_rows = [as_replace(SFX_ANCHOR, "before", arms)]
        print("\nTHE SFX ROW (mode `before` the rune-crack fallback), applied to Sfx.prototype.play's own source and "
              "rendered:")
        chk = []
        for sd in (None, NOISE_SEEDS[3]):
            dr = "" if sd is None else " draw"
            xa1, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows, seed=sd)
            xa2, _ = cx(Ca["sp"], Ca["g"], Ca["sw"], Ca["L"], Ca["D"], Ca["kb"], seed=sd)
            chk.append(("cast" + dr, float(np.abs(xa1 - xa2).max())))
            if sd is None:
                xa0 = xa1
            xe1, _ = R([["arm", T0, "ult", {"w": ME + "-enter"}]], rows=sfx_rows, seed=sd)
            xe2, _ = ex(En["sp"], En["g"], En["D"], seed=sd)
            chk.append(("enter" + dr, float(np.abs(xe1 - xe2).max())))
            xl1, _ = R([["arm", T0, "ult", {"w": ME + "-close"}]], rows=sfx_rows, seed=sd)
            xl2, _ = cx(Cl["sp"], Cl["g"], Cl["sw"], Cl["L"], Cl["D"], Cl["kb"], seed=sd)
            chk.append(("close" + dr, float(np.abs(xl1 - xl2).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9.5, 12.5, 18, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": n_}) for n_ in range(0, 7)]
        others += [("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 3}), ("clank", {"mass": 5}), ("seal", {}),
                   ("nova", {"k": 1}), ("hex-snap", {}), ("fork", {}), ("vine", {}), ("vine", {"plant": True}),
                   ("vine", {"coil": True}), ("vine", {"miss": True}), ("loose", {}), ("loose", {"bal": True}),
                   ("loose", {"leaf": True}), ("aegis", {"n": 3, "back": 5}), ("aegis", {"broke": True}),
                   ("scour-hold", {"n": 5}), ("scour-tick", {}), ("scour-woosh", {"n": 1}), ("scour-moo", {})]
        ult_ids = sorted(set(re.findall(r'w === "([a-z-]+)"', play_src)) | set(ids))
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
              f"hex-snap, fork, vine x4, loose x3, aegis x2, scour x4, {len(ult_ids)} ult ids -- every relic's cast "
              f"and every sub-voice the ult arm names -- and every kind play() names): worst max |diff| "
              f"{worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa0 - rcx).max())
        print(f"  ult/aureole vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost, n_others=len(same_))

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
            mine = [("ult", {"w": ME}), ("ult", {"w": ME + "-enter"}), ("ult", {"w": ME + "-close"})]
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
                           for nm, X_ in (("cast", Ca), ("enter", En), ("close", Cl))}
            worst_p = max(((max(v.values()), k + "/" + max(v, key=v.get)) for k, v in prg.items()),
                          default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders "
                  f"render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the three against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) -- printed")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=prg))
        rec["peers"] = peers

        # ---- THE tickHalo ROWS ----------------------------------------------
        trows = [as_replace(an, md, co) for an, md, co in SIM_ROWS]
        trows_bad = [as_replace(ENTER_ANCHOR, "before", ENTER_CODE_BAD)] + trows[1:]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        WR = None
        if not a.no_wire:
            print("\nTHE tickHalo ROWS, applied to Match.prototype.tickHalo's own source, run beside the original on "
                  "real fights:")
            WR = page.evaluate(WIRE_JS, [seeds, trows])
            assert not errors, errors[:3]
            if "err" in WR:
                raise SystemExit(WR["err"])
            print(f"  {WR['fights']} fights (Aureole both sides x every foe x seeds {seeds}): {WR['same']}/"
                  f"{WR['fights']} identical (over, clock, both fighters' hp, positions, velocities, charges, facing, "
                  f"smite and blessing counts, the arrows in the air, winner, the whole haloTally and the halo's "
                  f"record but voiceIn); every other SFX call identical in order and opts in {WR['otherSame']}/"
                  f"{WR['fights']}; {WR['zOpen']} fights end with the halo up (its record differs by voiceIn alone)")
            nh = WR["nh"]
            print(f"  windows {WR['ends']}: {WR['castT']} casts -> {WR['castV']} cast voices ({WR['unticked']} cast "
                  f"on a fight's last step, never ticked); {WR['firstIn']} windows open with the foe inside (no "
                  f"entry); {WR['entries']} entries -> {WR['enterV']} entry notes ({WR['withBless']} on a blessing's "
                  f"frame; gaps min {WR['gapMin']:.3f} s, p5 {WR['gapP5']:.3f}, median {WR['gapMed']:.3f}, "
                  f"{WR['gaps02']} of {WR['ngaps']} under 0.2 s); {WR['blessings']} blessings -> {WR['blessV']} heal "
                  f"chimes (n " + " ".join(f"{i}:{v}" for i, v in enumerate(nh) if v) + f"); {WR['closes']} closes; "
                  f"problems {WR['nbad']}")
            for b_ in WR["bad"]:
                print(f"    {b_}")
            if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                    or WR["closes"] != WR["ends"]["clock"] or WR["enterV"] != WR["entries"] \
                    or WR["blessV"] != WR["blessings"] or WR["castV"] != WR["castT"] \
                    or WR["enterV"] == 0 or WR["blessV"] == 0 or WR["closes"] == 0:
                FAILED.append("tickHalo rows")
            WB = page.evaluate(WIRE_JS, [seeds, trows_bad])
            assert not errors, errors[:3]
            print(f"  the control (the rows plus one sim write, the foe nudged 1e-9 on an entry): {WB['same']}/"
                  f"{WB['fights']} identical -- "
                  f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
            if WB["same"] == WB["fights"]:
                FAILED.append("identity control")
            rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "castT",
                                              "unticked", "entries", "enterV", "withBless", "firstIn", "blessings",
                                              "blessV", "closes", "nh", "zOpen", "gapMin", "gapP5", "gapMed",
                                              "gaps02", "ngaps", "nbad")}
            rec["wire"]["control_same"] = WB["same"]

            # ---- THE PICKS IN A REAL WINDOW ---------------------------------
            # v107's round-4c reading, imported as a method: per event, the third-
            # octave (200 Hz-12 kHz) in which the voice stands highest over
            # everything else in THIS window (the score and the fight). Gates: the
            # cast and the close >= +3 dB, the entry notes' median >= +6 dB. Two
            # controls that can come back wrong: AFTER (the same reading 0.8 s after
            # the close, no new voice sounding: NOT heard) and LEVEL (every event
            # heard at >= +3 dB reads LOWER with its voice 20 dB under).
            cand = sorted(WR["pick"], key=lambda w: (w["firstIn"], -(min(w["entries"], 6) * 3 + w["blessings"]),
                                                     w["foe"], w["seed"]))
            if cand:
                w_ = cand[0]
                EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], trows])
                assert not errors, errors[:3]
                c0t = w_["cast"]; c1t = w_["close"]
                lo_t, hi_t = c0t - 1.0, c1t + 2.0
                evs = [e for e in EV if lo_t <= e[0] <= hi_t]
                allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
                secs = T0 + (hi_t - lo_t) + 1.0
                xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
                bd = bed[:len(xw)]
                if len(bd) < len(xw):
                    bd = np.concatenate([bd, np.zeros(len(xw) - len(bd))])
                xw = xw + bd
                res, res_b, res_a = {}, {}, {}
                level_ok = {}
                BURY = 0.1
                bury_body = {ME: dyad_body(Ca["sp"], Ca["g"] * BURY, Ca["sw"], Ca["L"], Ca["D"], Ca["kb"]),
                             ME + "-enter": note_body(En["sp"], En["g"] * BURY, En["D"]),
                             ME + "-close": dyad_body(Cl["sp"], Cl["g"] * BURY, Cl["sw"], Cl["L"], Cl["D"], Cl["kb"])}
                RWB = [fc_ for fc_ in BANDS if PHONE_HZ <= fc_ <= 12000.0]

                def over_at(xa, xb_, fc_, t_, w_):
                    return db(band_rms(xa, fc_, t_, t_ + w_) / max(band_rms(xb_, fc_, t_, t_ + w_), 1e-12))

                def best_band(xa, xb_, t_, w_):
                    return max((over_at(xa, xb_, fc_, t_, w_), fc_) for fc_ in RWB)
                # ROUND 5: a swell is read over the 100 ms centred on its TOP (CREST-HEARD's
                # window); its onset reading (round 4's) is printed beside it
                crest_off = {ME: max(0.0, Ca["top_at"] - 0.05), ME + "-close": max(0.0, Cl["top_at"] - 0.05)}
                for tag, win_ in ((ME, 0.1), (ME + "-enter", 0.05), (ME + "-close", 0.1), ("bless", 0.05)):
                    ts = [T0 + (e[0] - lo_t) + crest_off.get(tag, 0.0) for e in evs if e[3] == tag]
                    if not ts:
                        res[tag] = res_b[tag] = res_a[tag] = []
                        continue
                    xo = R([e_ for e_, e in zip(allv, evs) if e[3] != tag], secs=secs, rows=sfx_rows,
                           new=False)[0] + bd
                    bb = [best_band(xw, xo, t_, win_) for t_ in ts]
                    if tag in crest_off:
                        res[tag + "0"] = [best_band(xw, xo, t_ - crest_off[tag], win_)[0] for t_ in ts]
                    res[tag] = [v_ for v_, _ in bb]
                    res[tag + "@"] = [fc_ for _, fc_ in bb]
                    t_after = T0 + (c1t - lo_t) + 0.8
                    ta = [t_after + 0.05 * i_ for i_ in range(len(ts))
                          if t_after + 0.05 * i_ + win_ <= T0 + (hi_t - lo_t)]
                    res_a[tag] = [best_band(xw, xo, t_, win_)[0] for t_ in ta]
                    if tag in bury_body:
                        xb = R([(["body", e_[1], bury_body[tag], e_[3]] if e[3] == tag else e_)
                                for e_, e in zip(allv, evs)], secs=secs, rows=sfx_rows, new=False)[0] + bd
                        res_b[tag] = [best_band(xb, xo, t_, win_)[0] for t_ in ts]
                        level_ok[tag] = all(b_ < v_ for v_, b_ in zip(res[tag], res_b[tag]) if v_ >= 3)
                    else:
                        res_b[tag] = []

                def gates(r):
                    def med(v):
                        return float(np.median(v))
                    return {ME: (min(r[ME]) >= 3) if r.get(ME) else None,
                            ME + "-enter": (med(r[ME + "-enter"]) >= 6) if r.get(ME + "-enter") else None,
                            ME + "-close": (min(r[ME + "-close"]) >= 3) if r.get(ME + "-close") else None}
                G4, GA = gates(res), gates(res_a)
                print(f"\nIN A REAL WINDOW -- aureole v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                      f"{c0t:.2f}s, closed by its clock at {c1t:.2f}s, {w_['entries']} entries and "
                      f"{w_['blessings']} blessings; the fight's own sounds and the score, with and without each "
                      f"new voice. Each event read in the third-octave (200 Hz-12 kHz) where it stands highest over "
                      f"everything else (v107's round 4c; the band after the @) -- the entry notes and heal chimes over "
                      f"their first 50 ms, the two swells over the 100 ms centred on their TOP (round 5: the cast "
                      f"+{crest_off[ME] * 1000:.0f} ms, the close +{crest_off[ME + '-close'] * 1000:.0f} ms; their onset "
                      f"reading printed beside it). Gates: the cast and the close >= +3 "
                      f"dB, the entry notes' median >= +6 dB; the heal chime (an existing voice) printed. Controls: "
                      f"AFTER (0.8 s after the close, no new voice: must read NOT heard) and LEVEL (each voice 20 dB "
                      f"under: every event heard at >= +3 must read lower)")

                def fmt_v(v):
                    return " ".join(f"{x_:+.1f}" for x_ in v) + (f" (median {np.median(v):+.1f})" if len(v) > 1 else "")

                def ok_(g_):
                    return "absent" if g_ is None else ("heard" if g_ else "NOT heard")
                for tag, nm in ((ME, "the cast"), (ME + "-enter", "each entry note"), (ME + "-close", "the close"),
                                ("bless", "each heal chime")):
                    if not res.get(tag):
                        print(f"  {nm}: none in this window")
                        continue
                    print(f"  {nm}: " + " ".join(f"{x_:+.1f}@{f_:.0f}" for x_, f_ in zip(res[tag], res[tag + '@'])) +
                          (f" (median {np.median(res[tag]):+.1f})" if len(res[tag]) > 1 else "") +
                          (f" dB -- {ok_(G4[tag])}" if tag in G4 else " dB (printed)") +
                          (f";  over its first 100 ms (round 4's reading): "
                           + " ".join(f"{x_:+.1f}" for x_ in res[tag + "0"]) if tag + "0" in res else ""))
                    print(f"      AFTER: {fmt_v(res_a[tag]) if res_a[tag] else 'no room'}"
                          + (f" -- {ok_(GA[tag])}" if tag in GA else "")
                          + (f";  BURIED: {fmt_v(res_b[tag])};  LEVEL: "
                             f"{'follows' if level_ok[tag] else 'DOES NOT follow'} the voice" if tag in level_ok else ""))
                if not res.get(ME) or not res.get(ME + "-enter") or not res.get(ME + "-close") or \
                        not all(g_ is not False for g_ in G4.values()):
                    FAILED.append("a new voice not heard in a real window")
                if any(g_ is not False for g_ in GA.values()):
                    print("  the AFTER control is heard (or has no room) -- the reading cannot come back wrong")
                    FAILED.append("real-window control (after)")
                else:
                    print("  the AFTER control (no new voice sounding) reads NOT heard for every voice, as it must")
                if not all(level_ok.get(t_, True) for t_ in (ME, ME + "-enter", ME + "-close")):
                    print("  the LEVEL control: the reading does not follow a voice's level")
                    FAILED.append("real-window control (level)")
                else:
                    print("  the LEVEL control: every event heard at >= +3 dB reads lower with its voice 20 dB under, "
                          "as it must")
                wav("aureole-pick-real-window.wav", xw)
                xo_all = R([e_ for e_, e in zip(allv, evs) if not e[3]], secs=secs, rows=sfx_rows, new=False)[0] + bd
                wav("aureole-pick-real-window-without.wav", xo_all)
                rec["real"] = dict(win=w_, over=res, buried=res_b, after=res_a, level_ok=level_ok,
                                   gates={"round4c": G4, "after": GA})
            else:
                print("\nIN A REAL WINDOW -- no clock close in the wire runs")
                FAILED.append("no real window")
        # the picks in order, for the ear: the cast, entries (each with its heal chime), a blow, the close
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, t_ in enumerate((0.9, 1.7, 2.6)):
            seq += [["arm", T0 + t_, "ult", {"w": ME + "-enter"}],
                    ["arm", T0 + t_, "spark", {"collect": True, "n": k_ + 1}]]
        seq += [["arm", T0 + 3.1, "hit", {"dmg": BLADE, "crit": False}], ["arm", T0 + 3.5, "spark",
                                                                          {"collect": True, "n": 4}]]
        seq += [["arm", T0 + 4.2, "ult", {"w": ME + "-close"}]]
        wav("aureole-pick-sequence.wav", R(seq, secs=6.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: Aureole's cast, entry and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="before", code=arms),
            dict(label="tickHalo: the entry note, on an inside tick after an outside tick of the same window",
                 anchor=ENTER_ANCHOR, mode="before", code=ENTER_CODE),
            dict(label="tickHalo: the heal chime (spark collect, unchanged), once per blessing, with the count",
                 anchor=BLESS_ANCHOR, mode="after", code=BLESS_CODE),
            dict(label="tickHalo: the close, on a clock close with both alive, before the close line",
                 anchor=CLOSE_ANCHOR, mode="before", code=CLOSE_CODE)]
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
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"{what}: an anchor is not kept exactly once")
        return patched

    NEWP = [("cast", {"w": ME}, dyad_body(Ca["sp"], Ca["g"], Ca["sw"], Ca["L"], Ca["D"], Ca["kb"]), {}),
            ("enter", {"w": ME + "-enter"}, note_body(En["sp"], En["g"], En["D"]), {}),
            ("close", {"w": ME + "-close"}, dyad_body(Cl["sp"], Cl["g"], Cl["sw"], Cl["L"], Cl["D"], Cl["kb"]), {})]

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
            rcp = R2([["play", T0, "ult", {"w": "spellbreaker"}]])
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
        e_ok = sum(f_["enterV"] == f_["entries"] for f_ in F1)
        b_ok = sum(f_["blessV"] == f_["blessings"] and f_["badN"] == 0 for f_ in F1)
        l_ok = sum(f_["closeV"] == f_["clock"] for f_ in F1)
        s_ok = sum(f_["stray"] == 0 for f_ in F1)
        orig_new = sum(f_["enterV"] + f_["blessV"] + f_["closeV"] for f_ in ref_fights)
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "entries", "blessings", "clock", "castV", "enterV",
                                                    "blessV", "closeV")}
        print(f"  the three new voices through the patched page's own SFX.play vs the lab's candidate text in that "
              f"page, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/aureole vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, entry notes = entries {e_ok}, heal "
              f"chimes = blessings (with the count) {b_ok}, closes = clock closes {l_ok}, every voice where it "
              f"belongs {s_ok} (of {len(F1)}); totals {tot}; the original page played {orig_new} of them from "
              f"tickHalo; page errors {page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1)
                   or osame != len(F1) or min(c_ok, e_ok, b_ok, l_ok, s_ok) != len(F1) or orig_new or page_err
                   or tot["enterV"] == 0 or tot["blessV"] == 0 or tot["closeV"] == 0)
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same, other_same=osame, totals=tot,
                    page_errors=page_err)

    if a.e2e_seeds > 0:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="aureole_e2e_"))
        try:
            tp = tmpd / "sc-aureole-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the four rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    # ---- ALSO: the rows on another link carrying Aureole ------------------------
    rec["also"] = []
    for spec in a.also:
        ap_ = resolve_game(spec)
        h2 = ap_.read_text(encoding="utf-8")
        s2 = hashlib.sha256(h2.encode()).hexdigest()[:16]
        p2 = apply_text(h2, ap_.name)
        print(f"\nALSO -- {ap_.name} {s2}: every anchor once, every row applies and keeps it; the original page "
              f"first (a browser), then the patched one (another, after it closes)")
        with game(game_path=ap_) as (page, errors):
            def R3(evs, seed=None):
                r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                assert not errors, errors[:3]
                return pcm(r)
            ps2 = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
            ids2 = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
            u2 = sorted(set(re.findall(r'w === "([a-z-]+)"', ps2)) | set(ids2))
            k2 = sorted(set(re.findall(r'kind === "([a-z-]+)"', ps2)) - {"ult", "hit"})
            voices2 = [v_ for v_ in e2e_voices if v_[0] != "ult" or v_[1]["w"] in u2]
            voices2 += [("ult", {"w": w_, "n": 2}) for w_ in u2
                        if w_ != ME and not w_.startswith(ME + "-") and ("ult", {"w": w_, "n": 2}) not in voices2]
            voices2 += [(k_, {}) for k_ in k2 if (k_, {}) not in voices2]
            ref_v = [R3([["play", T0, k, p]]) for k, p in voices2]
            ref_f = page.evaluate(FIGHTS_JS, [e2e_seeds])
            assert not errors, errors[:3]
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="aureole_also_"))
        try:
            tp = tmpd / ap_.name
            tp.write_text(p2, encoding="utf-8", newline="")
            keep = e2e_voices
            e2e_voices = voices2
            try:
                E = e2e_page(tp, ref_v, ref_f, ap_.name)
            finally:
                e2e_voices = keep
            E.update(game=ap_.name, sha=s2, patched_sha=hashlib.sha256(p2.encode()).hexdigest()[:16],
                     voices=len(voices2))
            rec["also"].append(E)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "x4", "bands", "DB", "t_s", "t_c")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), enter=strip(rows_e), enter_controls=strip(ctle),
               close=strip(rows_l), close_controls=strip(ctll + [LM]), wavs=sizes, release=release, literal_gc=gc,
               pick={"cast": Ca["name"], "cast_g": Ca["g"], "cast_sw": Ca["sw"], "cast_L": Ca["L"],
                     "cast_D": Ca["D"], "cast_kb": Ca["kb"], "enter": En["name"], "enter_g": En["g"],
                     "enter_D": En["D"], "close": Cl["name"], "close_g": Cl["g"]})
    print(f"\nTHE PICKS  cast {Ca['name']}   entry {En['name']}   close {Cl['name']}   blessing: the spark collect, "
          f"unchanged")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    al = "".join(f"; on {X['game']} too ({X['same']}/{X['fights']})" for X in rec["also"])
    wr = rec.get("wire")
    rows[0]["why"] = (
        f"The three new voices of v82 s4, in the synth only (the fourth, the blessing, is the existing spark collect). "
        f"The arms go BEFORE the shared rune-crack fallback (mode `before`, its anchor the fallback line itself), so "
        f"the {len(rec['fallthrough']) - 1} other relics that still fall through keep it and another relic's row "
        f"anchored there applies in either order. Through the patched play() every arm reproduces its lab "
        f"candidate (worst {max(v for _, v in rec['arm_check']['chk']):.0e}, on two noise draws), "
        f"{rec['arm_check']['n_others']} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), and ult/aureole is no longer rune-crack. play() "
        f"returns on its first line with no audio context (every headless run), draws no random number and writes "
        f"nothing the simulation reads" + (f"; end to end the three voices through the patched page's own SFX.play "
                                           f"equal the candidates (worst {max(v for _, v in E2['new']):.0e})"
                                           if E2 else "") + ".")
    if wr:
        rows[1]["why"] = (
            f"Before tickHalo's inside test (kept unchanged): the same test repeated into a const, one SFX.play when "
            f"it is true after a false one in the same window, and the answer kept on the halo's record as "
            f"`voiceIn` -- a field nothing in the simulation reads, born undefined with each cast. {wr['enterV']}/"
            f"{wr['entries']} entries voiced ({wr['firstIn']} windows opened with the foe already inside: no entry); "
            f"{wr['same']}/{wr['fights']} fights identical and every other SFX call identical in order and opts; the "
            f"rows plus one sim write come back {wr['control_same']}/{wr['fights']}{e2}{al}.")
        rows[2]["why"] = (
            f"After the blessing's own tally line (kept unchanged): the existing spark collect with n = the "
            f"blessing she now carries, Zenith's call word for word. {wr['blessV']}/{wr['blessings']} blessings "
            f"voiced, each with the count its apply left; nothing is read back{e2}.")
        rows[3]["why"] = (
            f"One guarded SFX.play before the window's own close line (kept unchanged), reading only Z.t, Z.dur and "
            f"the two alive flags: a clock close with both alive. {wr['closes']} closes for {wr['ends']['clock']} "
            f"clock closes, none on the {wr['ends']['caster'] + wr['ends']['foe']} closes a death made or the "
            f"{wr['ends']['over']} halos the fight's end cut off; nothing is read back{e2}.")
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
