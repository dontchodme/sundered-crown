#!/usr/bin/env python3
"""UNMAKING'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v111.

    python spellbreaker_voice_lab.py --game <a link carrying Spellbreaker's stage 5> --rows rows.json
        [--also <the same stage 5 carried onto a newer tip>] [--peer-rows <another relic's rows_final.json>]

v79 section 4 SOUND, every word of it: "Sound: cast -- a glass crack into a
hum, 0.4s; a stun -- hex's own snap, lengthened to match (0.4s tail); close --
the hum cutting out." The brief's stage 4 (v111's stage 6): "picture, voice,
carry". Rick, for the batch's art and sound: "you pick i overrule". So this lab
does not offer a spread -- it renders three to five candidates a voice beside
CONTROLS that can come back wrong, prints the numbers each pick is made on, and
PICKS by a rule written in this file (`*_RULE`, `*_why`). He overrules from one
clip.

ONE VOICE IS BUILT ON AN EXISTING ONE, BECAUSE THE DESIGN NAMES IT: "hex's own
snap" is `hex-snap`, the runic school's snap (v80 s4 / v79 / v75 name the same
sound; `corollary_voice_lab.py` made it; Axiom's Corollary plays it). The
stun's arm plays it ITSELF (`this.play("hex-snap")`), unchanged, and adds the
tail -- so the snap in the stun is the school's snap by construction, and would
follow it if it were ever re-voiced. The one candidate that cannot do that
(STRETCH, the snap's own three lines with every length scaled) writes them out.
NO VOICE FOR THE SECOND HEX: v79 names none (its picture is the tag counting by
two).

THE THREE EVENTS AND WHERE THEY FIRE (line numbers are sc-spellbreaker-b7.5's):
  cast   the bare id `ult/spellbreaker`, which `fireUlt` plays for every relic
         (the shared prologue, 16253+, before the unmake branch at 16656).
         Spellbreaker has NO arm today: it falls through to the shared
         rune-crack (measured below, to 1e-6, with every other relic that
         still does). The arms go BEFORE that fallback, in a row of mode
         `before` whose anchor is the fallback line itself -- so the fallback
         is never touched, and another relic's row anchored on it applies in
         either order. No sim line: the cast already plays it, once a cast.
  stun   `ult/spellbreaker-stun` from `tickStatus`'s hex block, right after
         the proc's `breakSpin` call (9572-9573, mode `after`): once per hex
         proc whose stun the caster's window has lengthened -- read as the
         sim reads it two lines up, `f.hexStunMul` (2 on the foe while the
         window is open, 1 everywhere else: tickUnmake 13669-13672). `> 1`,
         not `!== 1`, so a body without the field stays silent. The proc
         before the window's first tickUnmake (the cast's own step) is a x1
         proc in the sim, so it is silent here too. ~20 a window, near back to
         back (a proc every ~0.46 s of unfrozen time at the foe's ~2.5 hex, a
         0.4 s stun each): the voice is the window's texture, and is levelled
         as the snap is (under the blow).
  close  `ult/spellbreaker-close` from `tickUnmake`, on a line placed BEFORE
         the window's close line (13665, mode `before`): on the frame the
         window runs out BY ITS CLOCK with both fighters alive -- never on a
         death (a caster's death ends the fight; a close after the foe's death
         belongs to its kill), never once the fight is over (step() stops
         calling the tickers). Tendril's, Canopy's, Zenith's, Lightkeeper's
         and Benediction's rule.
  Nothing here sets a hit stop, files a beat or writes a field. The three
  voices are plain SFX.play calls (no opts but the id); the picture's rows are
  the picture lab's, not these.

THE CONTROLS, and what each one is for:
  rune-crack   what Spellbreaker's cast plays TODAY; v88 published 0.608 / 450
               ms -- reproduced before anything new is quoted (with BAR 0.364
               / 300 ms and hit@11.6 0.443 / 80 ms). Played through the id
               `__fallback__` (no arm names it), NOT `ult/spellbreaker`: after
               these rows `ult/spellbreaker` is no longer rune-crack, and every
               earlier lab's rune-crack control is `ult/spellbreaker` (see THE
               CARRY, below).
  hit@7.5      Spellbreaker's own blow (the blade is 7.5, stage 5): the level
               every voice is judged against, on its quietest / loudest draw
  wall         the commonest sound in a fight: the quiet voices' floor
  hex-snap     the school's snap: what the stun is built on (it must be there,
               at its own level) and what the cast must not be
  the school   the runic casts with a voice of their own (read off the page:
               Axiom's (BAR), Foregone's and Paradox's)
  the type     the twinblade casts with a voice of their own (read off the
               page: Widowmaker's, Twinshade's, Thornshear's, Starwarden's) --
               and, from `--peer-rows`, Angelus's cast and close, the type's
               other voice on the batch line
  BAR, death   Corollary's cast (the school's other bolt) and the death voice
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  CRACK, HUM, CLICKS, RUNECRACK   the cast's crack alone / its hum alone /
               the crack without the glass (three clicks and the hum) / today's
               voice: each must fail its gate
  PLAIN, TAIL  the hex-snap alone / RING's tail without the snap: each must
               fail its gate
  FADE, CAST   the hum held and then faded (not cut) / the cast itself: each
               must fail its gate

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
    imported unchanged: E50, TOP (the loudest 50 ms), AUDIBLE / GONE (the 5 ms
    RMS above 2% of its own loudest), RISE (10 -> 90% of the 1 ms envelope),
    CENTROID, REG (cosine of 1/3-octave band amplitudes, 25 Hz-16 kHz, the
    median over noise draws), PITCH (FFT peak, Hann, zero-padded,
    parabolic), FLUTTER (p95 - p5 of the RMS over four periods of a pitch at a
    1 ms hop about its 100 ms average), TONAL (a narrow peak over the median
    within a third-octave, draw-averaged), INHARM (a struck bar's mode: the
    strongest peak 1.5x-4x a note, its cents from a whole multiple and its
    level), HEARD (a third-octave >= 200 Hz over 100 ms against the score's
    p90 there, dB) and PHONE (the TOP high-passed at 200 Hz).
  * New here, each with a control that can come back wrong:
      SPAN-E   E50 / E25 / E5 read over a span of the voice: HELD = p95 - p5
               of E25 (dB) over a held span; LEVEL = the median E50 (or E5)
               there, dB re TOP
      INTO     the crack's centroid (the first 30 ms) over the hum's (its held
               span): the crack comes first and the hum is under it (the HUM
               control reads ~1)
      GLASS    the crack before the hum enters (1-21 ms): TONAL >= 12 dB over
               800-8000 Hz (a ring, not only clicks -- CLICKS must fail) AND
               INHARM: its strongest peak 1.5x-4x the note >= 60 cents from
               every whole multiple and within 20 dB of it (a glass rod, not a
               string)
      SNAP     the stun's first 30 ms against the hex-snap's: REG >= 0.90 and
               the sample peak within 1.5 dB (on the same draw) -- the snap is
               there, at its own level (TAIL must fail)
      TAIL-REG the stun's tail (60-400 ms) against the hex-snap: the tail is
               the snap's own sound going on
      CONT     the lowest 5 ms RMS over 50-300 ms re the voice's loudest 5 ms:
               the tail rings through the stun without a gap (>= -34 dB)
      CUT      the close's stop: from the last 5 ms window within 3 dB of its
               held level to the first 30 dB under it, ms (FADE must fail);
               PREFADE the lowest 25 ms RMS over the 100 ms before the stop
               starts, dB re held (a cut is from level, not the end of a fade)
      ONSET    the loudest 5 ms of the first 40 ms over the held level, dB (the
               hum arrives without a crack -- CAST must fail)
  * The candidates are LEVEL-MATCHED, not hand-set, so each pick is made on
    shape: the cast's gain puts its TOP at the centre of its level window, its
    hum's gain puts the hum's held E50 10 dB under the TOP, and the hum's
    length puts AUDIBLE at 400 ms (five passes); each stun tail's gain puts its
    loudest 50 ms 9 dB under the snap's TOP and its length puts AUDIBLE at 400
    ms (STRETCH has only its scale, solved for 400 ms); each close's gain puts
    its held level on the cast's hum's. Constants are rounded BEFORE any
    measured render, so a shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of v79 s4 turned into numbers;
Code's picks, Rick's to overrule):
  * "A GLASS CRACK": a fracture is a run of clicks, and glass rings: three
    6 kHz high-passed noise clicks 6 ms long at 0 / 4 / 11 ms (levels 1 / 0.6
    / 0.8), and a glass rod struck at G6 (1567.98 Hz) with its bar modes
    1 : 2.76 : 5.40 at 0.5 / 0.3 / 0.15, dying in 70 / 45 / 30 ms. Every cast
    candidate carries this crack, so the pick is on the hum.
  * "A HUM": a held tone, low and steady. THIS TOOLKIT HAS NO HELD NOTE
    (CLAUDE.md 4.5): the hum is RE-STRUCK in phase on the whole cycle nearest
    every 4 ms (every cycle, under 375 Hz), `.frequency.value = f` set on
    every strike (v97's toolkit finding), each strike 30 ms long. A 30 ms
    strike is what lets the hum CUT OUT at the close: it dies within ~20 ms of
    its last strike (a 0.25 s strike, Zenith's, would ring on ~150 ms). In the
    cast it enters 25 ms after the crack and its strikes fall 30 dB over its
    last 0.1 s (a release: the cast's hum ends; only the close's cuts). Its
    pitch and timbre are the candidates. The register survey (scratch
    stage6-voice/survey.py) found 100-180 Hz crowded -- Paradox's cast (111
    Hz), the blow's body (137-175), the death voice, Foregone and Starwarden
    -- so every candidate sits at A3-E4 or above.
  * "0.4s": AUDIBLE 330-470 ms, GONE <= 470 ms (v100's +/-17.5%).
  * "LENGTHENED TO MATCH (0.4s TAIL)": the stun it announces is 0.4 s (48
    steps, measured at stage 5): the voice is audible to 400 ms and gone by
    470. A fixed 0.4 s, as the design says -- the arm does not read the stun's
    length.
  * "THE HUM CUTTING OUT": the cast's own hum (its pitch, timbre, strike and
    held level), held 0.2 s and then stopping from level. How it stops is the
    candidates.

THE ROUNDS (each a run of this file; the logs in scratch stage6-voice/iter*.log).
The rules were written before the first table. Every change after a table was
read is here, with its reason:
  1  a crash: INHARM divided by zero on the HUM control (nothing sounds before
     the hum enters). Guarded; no rule changed.
  2  the cast and the close pass (DRONE; CUT, SAG and CLICK); NO STUN PASSED.
     STRETCH stops being a snap (its peak at 17 ms, rise 7 ms, the tail 5 dB
     OVER the snap) -- the rule's reading, kept. RING and BODY were held to
     the noise buffer's 0.55 s cap, which is a burst's, not a tone's (a lab
     bug), and never reached 0.4 s; RING, BODY and RATTLE, each ONE line of
     the snap lengthened, read TAIL-REG 0.29 / 0.46 / 0.49 against 0.60; HUM
     (the snap and the cast's hum) 0.05. And the close's tiebreak (the
     fastest CUT, to 5 ms) split CUT, SAG and CLICK on 23 / 17 / 22 ms -- under
     two cycles of the hum, a difference nobody hears (Zenith's LINEARITY
     precedent). -> round 3: each stun kind takes its own cap (a tone 3 s, a
     single burst 0.55 s, a train 0.6 s); HUM out, ECHO in (the snap's own
     three lines re-struck); the close's tiebreak leads with register, as the
     cast's does.
  3  ECHO passes every gate but CONT (-38.7 dB): re-struck every 18 ms, each
     repeat's bursts die 55 dB in 22 ms, so the train's troughs fall under the
     floor before 300 ms. -> round 4: ECHO held through the stun and falling
     at its end (-20 dB x (s/D)^3) -- "to match" the 0.4 s grey, which holds
     and then ends.
  4  CONT -36.6 dB: a train of 18 ms clicks, not a tail. -> round 5: ECHO
     re-struck every ~10 ms.
  5  ECHO passes every gate -- at 126 synth calls, 4.5 ms of main thread a
     call. The stun fires ~20 times a window (a proc every ~0.46 s); the
     batch's frequent voices cost 0.0-0.2 ms a call and its once-a-window
     casts up to 11.9. -> round 6: the stun's rule gains a cost gate, <= 40
     synth calls a stun; BODY out (A TOOLKIT FINDING: one noise burst cannot
     carry a 0.4 s tail at the level a tail needs -- `_burst` ramps to an
     absolute 1e-4, so a burst loud enough to stand 9 dB under the snap falls
     ~60 dB inside its 0.55 s cap and is gone by ~200 ms; noise is held only
     by re-striking), SIZZLE in (ECHO's idea at a quarter of the calls: the
     snap's band re-struck every ~15 ms and its ping rung on under it).
  6  SIZZLE reads TAIL-REG 0.58 (12 draws; 0.64 on 4 -- the re-struck band is
     one slice of the noise buffer repeated, so its spectrum is the draw's):
     its ring, hand-set at the snap's GAIN ratio (0.363), is continuous where
     the band is not, and swamps it. -> round 7: the ring's weight is SOLVED so
     that, in the tail, ring over train in RMS equals the snap's own ping over
     its own band in RMS (measured: 0.996).
  7  every voice passes: DRONE, SIZZLE (TAIL-REG 0.68, 30 calls, 1.2 ms), CUT.
  8  the full run (the wire, end to end, --also on the batch tip, four peers):
     every check passes, no rule changed. Then, text only: a one-tone hum's
     loop is printed in its plain form (the same arithmetic, float for float:
     x * 1 is x), the ALSO line names its link's sha, and this docstring's
     PICKS were written -- and the file was run once more in full, every
     number coming back (scratch stage6-voice/full.log, full2.log).

THE PICKS, on Chromium 151.0.7922.34, sc-spellbreaker-b7.5 da7936dccd8f5f15,
wire seeds 111601-111602 (148 fights), end to end 111651 (74), ALSO on the
same stage 5 carried onto sc-aureole-fxout (d8e16ff49c9d63e1, 82 fights):

  cast   1 DRONE   the declared glass crack (23.1 dB tonal; its 2.76 mode read
                   at 2.760x, 145 cents off any harmonic, -6 dB re the note)
                   into a C4 triangle hum (261.63 Hz) from 25 ms, held 0.9 dB
                   steady at -10.0 dB re the top, flutter 0.1, releasing over
                   its last 0.1 s: audible 400 ms, top -2.8 dB re the blow;
                   the crack +30.2 dB and the hum +8.4 dB over the score.
                   Register at most 0.66 (rune-crack -- the crack alone reads
                   0.81 against it: the hum is what sets it apart), 109 synth
                   calls, 2.2 ms. REED (0.76) and BUZZ (0.79) pass and lose
                   the register tiebreak; SWELL out (the hum still climbing at
                   100 ms: held 3.6 dB); GLASS out (660 Hz is not low; the
                   beat moves it 7.2 dB).
  stun   3 SIZZLE  the school's snap played as itself; its 2.6 kHz band
                   re-struck every ~15 ms and its ping (2500 Hz) rung on under
                   it, ring over train 0.224 (solved: the snap's own ping over
                   band in RMS, 0.996), held through the stun and falling 20 dB
                   at its end. Snap register 1.00, peak within 0.5 dB; the
                   tail's register against the snap 0.68, its loudest 50 ms
                   -8.4 dB re the snap's; audible 395-425 ms, gone by 430; no
                   gap (-30.6 dB); heard +18.0 dB in its tail; register at most
                   0.67 (Thornshear); 30 synth calls, 1.2 ms. ECHO passes all
                   but cost (126 calls, 4.5 ms); STRETCH is not a snap any
                   more; RING and RATTLE are not the snap's own sound (0.28,
                   0.49).
  close  1 CUT     the cast's hum, held 0.2 s at its held level (0.0 dB),
                   register 0.97 with it, then its strikes stop: 30 dB down 23
                   ms after it starts to fall, no fade before it (-0.1 dB),
                   audible 230 ms, heard +8.4 dB; register at most 0.19 (the
                   blow). SAG (0.30) and CLICK (0.19, one more call) pass and
                   lose the tiebreak; STUTTER out (its drop-out reads as a fade
                   before the stop, -14.6 dB).

  In play (148 fights; 712 windows: 639 closed by the clock, 17 by the
  caster's death, 56 by the fight's end): 712 cast voices; 11726 hex procs
  lengthened (every one on the foe) -> 11726 stun voices, a median 16 a clock
  window (0-35), and none of the 7878 x1 procs on the foe, 642 on
  Spellbreaker, 112 on shades; 639 closes. 148/148 fights identical (a digest
  of every step), every other voice call identical; the sim-write control
  0/148. In a real window (v Ironhail, 111601, 26 stuns) the crack stands
  +29.5 dB over the fight and the score in its own third-octave, the hum +15.3,
  the stun tails a median +20.6, the close +8.6; AFTER reads +0.0 for every
  voice and LEVEL follows every voice. End to end 74/74 and 82/82 fights
  identical, every other voice unchanged. Co-applied with Angelus's,
  Aureole's, Censer's and Lightkeeper's Sfx rows in both orders: every arm
  alike; register at most 0.73 (Aureole's cast against this close -- the C4 of
  both, printed, not a school or type voice).

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row (three arms before the rune-crack fallback) is applied to
    `Sfx.prototype.play`'s own source and rendered: each arm must reproduce
    its candidate to TOL on two noise draws; every other voice through the
    patched play (the hit at five weights with and without a crit, spark x9,
    wall, death, clank x2, seal, nova, hex-snap, fork, vine x4, loose x3,
    aegis x2, scour x4, and every ult id and kind the page's play() names)
    must be unchanged; `ult/spellbreaker` must NOT be rune-crack any more and
    `__fallback__` must still be;
  * the tickStatus row and the tickUnmake row are applied to their
    prototypes' own sources and run on real fights beside the unpatched ones:
    every fight identical (over, clock, both fighters' hp, positions,
    velocities, charges, facing, stun, hex clock, hexStunMul and hex stacks,
    the winner, both unmakeTallies, and a digest of positions, hp, stun and
    hex clock on EVERY step) and every other voice call identical in order,
    kind and opts; one stun voice on each tickStatus call whose hex proc met
    hexStunMul > 1 and none on any other (x1 procs, her own procs, shades);
    one close per window closed by its clock with both alive and none
    otherwise; one cast voice per cast (from `fireUlt`, outside the tickers);
    the unpatched tickers play nothing. The same rows plus ONE sim write (the
    stunned fighter nudged 1e-9 on a stun voice) must come back NOT identical,
    or "identical" proves nothing. (The Sfx row cannot reach the simulation at
    all: `play` returns on its first line with no audio context, which is
    every headless run.)
  * END TO END: the rows applied AS TEXT (the orchestrator's semantics:
    replace = code, after = anchor + code, before = code + anchor) to a copy of
    the game file (in a temp folder, never the repo), loaded in a fresh
    browser after the first is closed: the page loads clean, its own SFX.play
    renders the arms to the lab's text and every other voice to the original
    page's, and its fights are identical to the original page's, with the
    voice counts above. With `--also <link>`, the same, there.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both
    identically; registers against the peers' voices are printed, and the
    cast's against the type's (Angelus's cast and close) is gated.
  All anchors must occur exactly once in the game file; no row replaces its
  anchor, so a later relic's row -- or the picture's -- anchored on the same
  line still applies, in either order. Every row is ASCII.

THE CARRY -- one thing these rows change for every LATER voice lab: each of
them (zenith's through aureole's) plays rune-crack as `ult/spellbreaker` and
stops unless it reproduces v88's 0.608 / 450 ms. On a tip that carries these
rows, `ult/spellbreaker` is Unmaking's cast, so those controls must move to an
id no arm names (this lab's `__fallback__`) before they run there.

Writes wavs to 05-reference/v111/spellbreaker-*.wav at RAW level (gitignored).
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
    env, flutter, fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS, inharm  # noqa: E402
from bindweed_voice_lab import mreg, tonal  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90, heard, phone  # noqa: E402
from lightkeeper_voice_lab import _wrap  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "spellbreaker"
FALLBACK = "__fallback__"                 # an id no arm names: rune-crack, after these rows too
BLADE = 7.5                               # Spellbreaker's dmg (stage 5: the carry)
TOL = 1e-5                                # reproduction / transcription (-100 dB)
SCHOOL_AFF = "runic"
TYPE_SHAPE = "twinblade"
PEER_TYPE = {"angelus": "the sanctified twinblade (v104; the batch line)"}
F_GLASS = 1567.982                        # G6: the glass rod's note
HUM_EVERY = 0.004                         # a hum strike on the whole cycle nearest every 4 ms
HUM_D = 0.03                              # a hum strike's length: what lets the hum cut out
HUM_AT = 0.025                            # the hum enters after the crack
HUM_REL, HUM_REL_DB = 0.1, 30.0           # the cast's hum releases 30 dB over its last 0.1 s
HUM_UNDER_DB = 10.0                       # the cast's hum held 10 dB under its TOP
AUD_TGT = 400.0                           # "0.4s" (the cast) / "0.4s tail" (the stun), ms
TAIL_UNDER_DB = 9.0                       # a stun tail's loudest 50 ms under the snap's TOP
CLOSE_T = 0.2                             # the close's hum held 0.2 s, then it stops
HELD_C = (0.03, 0.12)                     # the close's held span, s
SNAP = [2600, 1.2, 0.38, 0.022, 1300, 1.0, 0.15, 0.030, 3100, 2500, 0.138, 0.045]
REASON = "the hex takes the wind out of it"
STUN_CALLS = 40                           # round 6: the stun's cost gate, synth calls a call


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


def _ind(lines, n):
    return "\n".join(" " * n + l_ for l_ in lines)


# ================================================================ THE HUM ===
# One hum, used by the cast, the close and the stun's HUM candidate: `tones`
# [[f, weight], ...] in one `type`, re-struck in phase on the whole cycle
# nearest HUM_EVERY, each strike HUM_D long, `.frequency.value` set on each.
# `lv` is a JS expression in `s` (seconds from t) for the strike's level
# re `h`; `s0`, `s1` the first strike and the end; `fexp` an optional JS
# expression for the pitch at `s` (the SAG close), else the tone's own.
def hum_lines(tones, ty, h, s0, s1, lv="1", segs=None, fexp=None):
    if len(tones) == 1 and tones[0][1] == 1.0 and not segs and not fexp:
        # one tone, one span: the plain loop (the same arithmetic as the general
        # one below, float for float: x * 1 and x * (1) are x)
        f = fmt(tones[0][0])
        g = fmt(h) if lv == "1" else f"{fmt(h)} * {lv}"
        return [f"for (let s = {fmt(s0)}; s < {fmt(s1)} - 1e-9; s += Math.max(1, Math.round({f} * {fmt(HUM_EVERY)})) / {f})",
                f'  this._tone(t + s, {{ freq: {f}, gain: {g}, dur: {fmt(HUM_D)}, type:"{ty}" }}).frequency.value = {f};']
    tarr = "[" + ", ".join(f"[{fmt(f)}, {fmt(k)}]" for f, k in tones) + "]"
    segs = segs or [(s0, s1)]
    sarr = "[" + ", ".join(f"[{fmt(a)}, {fmt(b)}]" for a, b in segs) + "]"
    L = [f"for (const [f0, kf] of {tarr})",
         f"  for (const [a0, a1] of {sarr})",
         "    for (let s = a0; s < a1 - 1e-9; ){"]
    fl = f"const f = {fexp};" if fexp else "const f = f0;"
    L += [f"      {fl}",
          f'      this._tone(t + s, {{ freq: f, gain: {fmt(h)} * kf * ({lv}), dur: {fmt(HUM_D)}, type:"{ty}" }})'
          f".frequency.value = f;",
          f"      s += Math.max(1, Math.round(f * {fmt(HUM_EVERY)})) / f;",
          "    }"]
    return L


# =============================================================== THE CAST ===
# "a glass crack into a hum, 0.4s". Every candidate carries the declared crack;
# they differ in the hum (its pitch, its timbre) and how it comes in.
CAST_CANDIDATES = [
    ("1 DRONE", dict(tones=[(261.6256, 1.0)], ty="triangle", entry="step"),
     "a C4 triangle hum (261.63 Hz) coming in at level 25 ms after the crack"),
    ("2 REED", dict(tones=[(329.6276, 1.0)], ty="square", entry="step"),
     "an E4 square hum (329.63 Hz, hollow, the score's v) coming in at level"),
    ("3 BUZZ", dict(tones=[(220.0, 1.0)], ty="sawtooth", entry="step"),
     "an A3 sawtooth hum (220 Hz, the score's tonic, an electric buzz) coming in at level"),
    ("4 SWELL", dict(tones=[(261.6256, 1.0)], ty="triangle", entry="swell"),
     "DRONE's hum swelling in from 12 dB under over 0.12 s -- the crack's energy passing into it"),
    ("5 GLASS", dict(tones=[(659.2551, 1.0), (663.2551, 0.3)], ty="sine", entry="step"),
     "the glass itself humming: E5 (659.26 Hz) with a partner 4 Hz sharp at 0.3 -- a singing glass"),
]


def crack_lines(clicks=True, glass=True):
    L = []
    if clicks:
        L += ["for (const [s, k] of [[0, 1], [0.004, 0.6], [0.011, 0.8]])",
              '  this._burst(t + s, { freq: 6000, q: 0.7, gain: g * k, dur: 0.006, type:"highpass" });']
    if glass:
        L += ["for (const [r, k, d] of [[1, 0.5, 0.07], [2.76, 0.3, 0.045], [5.4, 0.15, 0.03]])",
              f'  this._tone(t, {{ freq: {fmt(F_GLASS)} * r, gain: g * k, dur: d, type:"sine" }})'
              f".frequency.value = {fmt(F_GLASS)} * r;"]
    return L


def cast_lv(sp, S1):
    """The hum's strike level in the cast: the release over its last 0.1 s, and
    (SWELL) the entry."""
    rel = f"Math.pow(10, -{fmt(HUM_REL_DB)} * Math.max(0, (s - {fmt(round(S1 - HUM_REL, 6))}) / {fmt(HUM_REL)}) / 20)"
    if sp["entry"] == "swell":
        return (f"Math.pow(10, -12 * Math.max(0, 1 - (s - {fmt(HUM_AT)}) / 0.12) / 20) * {rel}")
    return rel


def cast_body(sp, g, kh, S1, part="both", ind=10):
    """The cast arm's body. `part`: both / crack / hum / clicks (the crack
    without its glass, and the hum) -- the controls."""
    L = [f"const g = {fmt(g)};"]
    if part in ("both", "crack"):
        L += crack_lines()
    if part == "clicks":
        L += crack_lines(glass=False)
    if part in ("both", "hum", "clicks"):
        L += hum_lines(sp["tones"], sp["ty"], round(g * kh, 6), HUM_AT, S1, lv=cast_lv(sp, S1))
    return _ind(L, ind)


# =============================================================== THE STUN ===
# "a stun -- hex's own snap, lengthened to match (0.4s tail)". Every candidate
# but STRETCH plays the school's snap ITSELF and adds a tail that starts with
# it; STRETCH is the snap's own three lines with every length x k.
STUN_CANDIDATES = [
    ("1 STRETCH", dict(kind="stretch"),
     "the snap itself lengthened: its three lines with every length x k (k solved for 0.4 s)"),
    ("2 RING", dict(kind="ring"),
     "the snap, and its ping rung on: a 2500 Hz triangle (where the ping lands) dying over 0.4 s"),
    ("3 SIZZLE", dict(kind="sizzle"),
     "the snap, its band re-struck every ~15 ms and its ping rung on under it (ECHO at a quarter of the calls: "
     "round 6), held through the stun and falling 20 dB at its end; the ring over the train as the snap's own "
     "ping over its band, in RMS (solved: round 7)"),
    ("4 RATTLE", dict(kind="rattle"),
     "the snap, and its band re-struck: 2600 Hz pings ~28 ms apart dying over 0.4 s (a jammed catch)"),
    ("5 ECHO", dict(kind="echo"),
     "the snap re-struck: its own three lines again every ~10 ms (round 5; 18 ms in rounds 3-4) at its own "
     "proportions, held through the stun and falling 20 dB at its end (-20 dB x (s/D)^3: round 4)"),
]


def stun_body(sp, kt, D, Ca=None, ind=10, snap=True, part=None):
    k_ = sp["kind"]
    if k_ == "stretch":
        s_ = SNAP
        L = [f"const k = {fmt(D)};",
             f'this._burst(t, {{ freq: {s_[0]}, q: {s_[1]}, gain: {s_[2]}, dur: {s_[3]} * k, type:"bandpass" }});',
             f'this._burst(t, {{ freq: {s_[4]}, q: {s_[5]}, gain: {s_[6]}, dur: {s_[7]} * k, type:"bandpass" }});',
             f'this._tone (t, {{ freq: {s_[8]}, to: {s_[9]}, gain: {s_[10]}, dur: {s_[11]} * k, type:"triangle" }});']
        return _ind(L, ind)
    L = ['this.play("hex-snap", {});'] if (snap and part is None) else []
    if k_ == "ring":
        L += [f'this._tone(t, {{ freq: 2500, gain: {fmt(kt)}, dur: {fmt(D)}, type:"triangle" }});']
    elif k_ == "body":        # round 2's BODY, kept for the record (see THE ROUNDS)
        L += [f'this._burst(t, {{ freq: 1300, q: 6, gain: {fmt(kt)}, dur: {fmt(D)}, type:"bandpass" }});']
    elif k_ == "sizzle":
        # the ring's weight `w` is SOLVED (round 7): the ring over the band train
        # in the tail, in RMS, as the snap's own ping over its own band
        s_ = SNAP
        if part in (None, "ring"):
            L += [f'this._tone (t, {{ freq: {s_[9]}, gain: {fmt(kt)} * {fmt(sp.get("w", 0.363))}, dur: {fmt(D)} * 2.5, '
                  f'type:"triangle" }});']
        if part in (None, "train"):
            L += [f"for (let s = 0.015, k = 0; s < {fmt(D)}; k++){{",
                  f'  this._burst(t + s, {{ freq: {s_[0]}, q: {s_[1]}, gain: {fmt(kt)} * Math.pow(0.1, Math.pow(s / {fmt(D)}, 3)), '
                  f'dur: {s_[3]}, type:"bandpass" }});',
                  "  s += 0.015 * (1 + 0.2 * Math.sin(k * 2.4));",
                  "}"]
    elif k_ == "rattle":
        L += [f"for (let s = 0.03, k = 0; s < {fmt(D)}; k++){{",
              f'  this._tone(t + s, {{ freq: 2600, gain: {fmt(kt)} * Math.pow(0.1, s / {fmt(D)}), dur: 0.012, '
              f'type:"triangle" }});',
              "  s += 0.028 * (1 + 0.15 * Math.sin(k * 2.4));",
              "}"]
    elif k_ == "echo":
        s_ = SNAP
        L += [f"for (let s = 0.01, k = 0; s < {fmt(D)}; k++){{",
              f"  const a = {fmt(kt)} * Math.pow(0.1, Math.pow(s / {fmt(D)}, 3));",
              f'  this._burst(t + s, {{ freq: {s_[0]}, q: {s_[1]}, gain: a, dur: {s_[3]}, type:"bandpass" }});',
              f'  this._burst(t + s, {{ freq: {s_[4]}, q: {s_[5]}, gain: a * {fmt(round(s_[6] / s_[2], 4))}, '
              f'dur: {s_[7]}, type:"bandpass" }});',
              f'  this._tone (t + s, {{ freq: {s_[8]}, to: {s_[9]}, gain: a * {fmt(round(s_[10] / s_[2], 4))}, '
              f'dur: {s_[11]}, type:"triangle" }});',
              "  s += 0.01 * (1 + 0.2 * Math.sin(k * 2.4));",
              "}"]
    return _ind(L, ind)


# ============================================================== THE CLOSE ===
# "close -- the hum cutting out". Every candidate is the PICKED cast's hum --
# its tones, timbre, strike -- at its held level, for CLOSE_T; they differ in
# how it stops.
CLOSE_CANDIDATES = [
    ("1 CUT", dict(kind="cut"),
     "the hum held 0.2 s, and its strikes simply stop: it dies with the last one's 30 ms ring"),
    ("2 SAG", dict(kind="sag"),
     "the hum sagging a fourth over its last 60 ms before it stops -- the power going"),
    ("3 STUTTER", dict(kind="stutter"),
     "the hum dropping out for 30 ms and catching once before it stops -- a failing contact"),
    ("4 CLICK", dict(kind="click"),
     "CUT with a relay's click where it stops"),
]


def close_body(Ca, sp, h, ind=10):
    tones, ty = Ca["sp"]["tones"], Ca["sp"]["ty"]
    k_ = sp["kind"]
    if k_ == "cut" or k_ == "click":
        L = hum_lines(tones, ty, h, 0.0, CLOSE_T)
        if k_ == "click":
            L += [f'this._burst(t + {fmt(CLOSE_T)}, {{ freq: 5000, q: 0.7, gain: {fmt(round(h * 4, 6))}, dur: 0.005, '
                  f'type:"highpass" }});']
    elif k_ == "sag":
        a_ = round(CLOSE_T - 0.06, 6)
        L = hum_lines(tones, ty, h, 0.0, CLOSE_T,
                      fexp=f"f0 * Math.pow(0.75, Math.max(0, (s - {fmt(a_)}) / 0.06))")
    elif k_ == "stutter":
        L = hum_lines(tones, ty, h, 0.0, CLOSE_T, segs=[(0.0, 0.1), (0.13, CLOSE_T)])
    elif k_ == "fade":        # the control: held 0.1 s, then falling 40 dB over 0.2 s
        L = hum_lines(tones, ty, h, 0.0, 0.3, lv="Math.pow(10, -40 * Math.max(0, (s - 0.1) / 0.2) / 20)")
    return _ind(L, ind)


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
STUN_ANCHOR = '                       STATUS.hex.stunFor * f.hexStunMul);'
CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultUnmake = null; continue; }'

STUN_CODE = '''
        /* UNMAKING'S STUN (v79 s4: "a stun -- hex's own snap, lengthened to
           match (0.4s tail)"): on a hex proc whose stun the caster's window
           has lengthened -- read as the two lines above read it, through
           this fighter's `hexStunMul` (2 on the foe while the window is open,
           1 everywhere else) -- once, on the proc's frame. `> 1`, not
           `!== 1`: a body without the field stays silent. Presentation only:
           SFX.play draws nothing, is a no-op headless, and nothing here is
           read back (spellbreaker_voice_lab: fights identical). */
        if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });'''

CLOSE_CODE = '''      /* UNMAKING'S CLOSE (v79 s4: "close -- the hum cutting out"): on the
         frame the window runs out BY ITS CLOCK with both fighters alive. A
         caster's death ends the fight, and a close after the foe's death
         belongs to its kill, so both are left to the death voice (Tendril's,
         Canopy's, Zenith's, Lightkeeper's and Benediction's rule). Reads
         Z.t, Z.dur and the two alive flags; writes nothing. Presentation
         only; the next line is the sim's own close, unchanged. */
      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "spellbreaker-close" });
'''

# the sim-write control: the stun row with the stunned fighter nudged 1e-9 on a stun voice
STUN_CODE_BAD = STUN_CODE.replace(
    '        if (f.hexStunMul > 1) SFX.play("ult", { w: "spellbreaker-stun" });',
    '        if (f.hexStunMul > 1){ f.vx += 1e-9; SFX.play("ult", { w: "spellbreaker-stun" }); }', 1)
assert STUN_CODE_BAD != STUN_CODE

SIM_ROWS = [("status", STUN_ANCHOR, "after", STUN_CODE), ("unmake", CLOSE_ANCHOR, "before", CLOSE_CODE)]
_refuse(STUN_CODE + CLOSE_CODE, "sim rows")
for _w, _a, _m, _c in SIM_ROWS:
    assert _a not in _c, "a before/after row's code must not repeat its anchor"
    assert _c.isascii(), "a row must be ASCII"
    assert (_c.endswith("\n") if _m == "before" else _c.startswith("\n")), "a row's code must join its anchor"


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


def arms_code(Ca, St, Cl, info):
    cn, sn, ln = (X["name"].split(maxsplit=1)[1] for X in (Ca, St, Cl))
    c_cast = _wrap([
        f'SPELLBREAKER\'S CAST, THE UNMAKING -- v79 s4: "cast -- a glass crack into a hum, 0.4s". {cn}, of '
        f'{info["n_cast"]}, picked on the numbers by `spellbreaker_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v111). Spellbreaker had no arm and fell through to rune-crack, which {info["n_rc"]} other '
        f'relics on its stage-5 link still use, so this ADDS arms before that fallback and leaves it alone.',
        f"The crack: three 6 kHz clicks at 0 / 4 / 11 ms (a fracture runs) and a glass rod struck at G6 with its "
        f"bar modes 1 : 2.76 : 5.40 -- {info['c_tonal']:.0f} dB tonal, its 2.76 mode {info['c_inh_c']:.0f} cents "
        f"off any harmonic. Into {info['c_what']}, re-struck in phase on every cycle (a held note does not exist "
        f"in this toolkit), each strike 30 ms: held {info['c_held']:.1f} dB steady at {info['c_hum_db']:+.1f} dB "
        f"re the crack's top, releasing over its last 0.1 s. Audible {info['c_aud']:.0f} ms. Its top "
        f"{info['c_db']:+.1f} dB re Spellbreaker's blow; the crack {info['c_heard']:+.1f} dB and the hum "
        f"{info['c_hheard']:+.1f} dB over the score. Register at most {info['c_reg']:.2f} against rune-crack, "
        f"the runic and twinblade casts, BAR, hex-snap, the blow and the death voice{info['c_peers']}."], 10)
    c_stun = _wrap([
        f'A LENGTHENED STUN -- "a stun -- hex\'s own snap, lengthened to match (0.4s tail)" (v79 s4). {sn}, of '
        f'{info["n_stun"]} (`spellbreaker_voice_lab.py`). `tickStatus` plays it on each hex proc whose stun the '
        f'window has doubled (0.4 s).',
        f"{info['s_what']} The snap is there at its own level (register {info['s_snap']:.2f} over its first "
        f"30 ms, its peak within {info['s_pk']:.1f} dB of the snap's); the tail is the snap's own sound (register {info['s_tail']:.2f}), "
        f"its loudest 50 ms {info['s_tdb']:+.1f} dB re the snap's, unbroken to the stun's end: audible "
        f"{info['s_aud']:.0f} ms, gone by {info['s_gone']:.0f}. Heard {info['s_heard']:+.1f} dB over the score "
        f"in its tail; register at most {info['s_reg']:.2f} against the blow, the wall tick, rune-crack, BAR, "
        f"the cast and the runic and twinblade casts."], 10)
    c_close = _wrap([
        f'THE HUM CUTS OUT -- "close -- the hum cutting out" (v79 s4). {ln}, of {info["n_close"]} '
        f'(`spellbreaker_voice_lab.py`): {info["l_what"]}',
        f"The cast's hum ({info['l_note']:.0f} Hz, register {info['l_hreg']:.2f} with it, "
        f"{info['l_lvl']:+.1f} dB re its held level), held and then gone {info['l_cut']:.0f} ms after it "
        f"starts to fall (30 dB), with no fade before it ({info['l_pre']:+.1f} dB). Audible "
        f"{info['l_aud']:.0f} ms. `tickUnmake` plays it when the window runs out by its clock with both alive."],
        10)
    return (f'{_arm_head(ME, "the weapon unmade")}\n'
            f'{c_cast}\n{cast_body(Ca["sp"], Ca["g"], Ca["kh"], Ca["S1"])}\n'
            f'{_arm_head(ME + "-stun", "a stun, lengthened")}\n'
            f'{c_stun}\n{stun_body(St["sp"], St["kt"], St["D"], Ca)}\n'
            f'{_arm_head(ME + "-close", "and the hum cuts out")}\n'
            f'{c_close}\n{close_body(Ca, Cl["sp"], Cl["h"])}\n')


# ============================================================== THE PAGE ===
COST_JS = r"""([rows, reps, ME]) => {
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
  for (const [k, kind, p] of [["cast", "ult", { w: ME }], ["stun", "ult", { w: ME + "-stun" }],
                              ["close", "ult", { w: ME + "-close" }], ["hex-snap", "hex-snap", {}],
                              ["hit", "hit", { dmg: 7.5, crit: false }]]){
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
  const fr = (x) => [x.hp, x.x, x.y, x.vx, x.vy, x.charge, x.theta, x.alive, x.stun, x.hexClock, x.hexStunMul,
                     x.stacks("hex")];
  const dig = (h, m) => { for (const x of [m.a, m.b])
    for (const v of [x.x, x.y, x.hp, x.stun, x.hexClock, x.vx]) h = mix(h, v); return h; };
"""

# The tickStatus and tickUnmake rows, applied to the real prototypes and run
# beside the originals; the survey of Unmaking's windows comes out of the same
# runs. Hex procs are read through tickStatus's own breakSpin call.
WIRE_JS = r"""([seeds, rows, ME, REASON]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
""" + COMMON_JS + r"""
  const oS = P.tickStatus, oU = P.tickUnmake, oB = P.breakSpin;
  const patch = (fn, rs) => { let src = fn.toString();
    for (const [anc, code] of rs){ const at = src.split(anc).length - 1;
      if (at !== 1) return { err: `an anchor occurs ${at} times in ${fn.name}()` };
      src = src.replace(anc, () => code); }
    return { fn: (0, eval)("(function " + src + ")") }; };
  const pS = patch(oS, rows.status), pU = patch(oU, rows.unmake);
  if (pS.err) return pS; if (pU.err) return pU;
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  for (const nm of ["STATUS", "CONFIG", "AFFINITIES"])
    if ((0, eval)("typeof " + nm) === "undefined") return { err: nm + " is not reachable from a patched ticker" };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    let step = 0, inS = 0, inU = 0, cur = null, h = 2166136261;
    const other = [], mine = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) mine.push([step, w, inS ? "S" : inU ? "U" : "-",
                                                         Object.keys(p).sort().join(","), m.t]);
      else other.push([step, kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const implS = wire ? pS.fn : oS, implU = wire ? pU.fn : oU;
    const st = { x2: 0, x1foe: 0, me: 0, shade: 0, v2: 0, bad: [] };
    P.breakSpin = function(g, reason, tf){
      if (inS && reason === REASON && cur) cur.push([g === foe ? "foe" : g === f ? "me" : "shade", g.hexStunMul]);
      return oB.apply(this, arguments); };
    P.tickStatus = function(g, dt){
      const c0 = mine.length, prev = cur; cur = []; inS++;
      try { return implS.call(this, g, dt); }
      finally {
        inS--;
        const v = mine.slice(c0).filter(c => c[1] === ME + "-stun").length;
        const pr = cur; cur = prev;
        if (pr.length > 1) st.bad.push(["two procs in one tickStatus", step]);
        const want = pr.length && pr[0][1] > 1 ? 1 : 0;
        for (const [who, mul] of pr){
          if (mul > 1){ st.x2++; if (who !== "foe") st.bad.push(["a x2 proc not on the foe", who, step]); }
          else if (who === "foe") st.x1foe++; else if (who === "me") st.me++; else st.shade++;
        }
        st.v2 += v;
        if (v !== want) st.bad.push(["stun voices on a tickStatus call", v, "want", want, step]);
      } };
    const wins = []; let W = null, strayClose = 0;
    P.tickUnmake = function(dt){
      const Z0 = f.ultUnmake, c0 = mine.length; inU++;
      if (Z0 && (!W || W.Z !== Z0)){
        W = { Z: Z0, castStep: step, cast: m.t, end: null, close: null, closeV: 0, stunV: 0 }; wins.push(W); }
      try { return implU.call(this, dt); }
      finally {
        inU--;
        const cl = mine.slice(c0).filter(c => c[1] === ME + "-close").length;
        if (Z0){
          W.closeV += cl;
          if (f.ultUnmake !== Z0){
            W.end = (Z0.t >= Z0.dur && f.alive && foe.alive) ? "clock" : !f.alive ? "caster" : !foe.alive ? "foe" : "?";
            W.close = m.t; W.endStep = step;
          }
        } else strayClose += cl;
      } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; h = dig(h, m); } }
    finally { P.tickStatus = oS; P.tickUnmake = oU; P.breakSpin = oB; if (had) S.play = op; else delete S.play; }
    for (const w of wins) if (!w.end) w.end = "over";
    for (const w of wins){
      w.stunV = mine.filter(c => c[1] === ME + "-stun" && c[0] >= w.castStep &&
                                 (w.endStep === undefined || c[0] <= w.endStep)).length; }
    const castV = mine.filter(c => c[1] === ME && c[2] === "-" && c[3] === "w").length;
    const where = mine.filter(c => (c[1] === ME + "-stun" && c[2] !== "S") || (c[1] === ME + "-close" && c[2] !== "U")
                                   || (c[1] === ME && c[2] !== "-") || c[3] !== "w").length;
    return { sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.winner ? m.winner.w.id : null,
                                  m.a.unmakeTally || null, m.b.unmakeTally || null, m.shots ? m.shots.length : null, h]),
             other: JSON.stringify(other), st, strayClose, castV, where, casts: f.unmakeTally ? f.unmakeTally.casts : 0,
             nMine: mine.length, wins: wins.map(w => { const { Z, ...r } = w; return r; }) };
  };
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, caster: 0, foe: 0, over: 0, "?": 0 };
  let casts = 0, castV = 0, x2 = 0, x1foe = 0, me = 0, shade = 0, stunV = 0, closes = 0, unticked = 0;
  const pick = [], perWin = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    if (A.nMine !== A.castV) bad.push([fid, sd, "the UNPATCHED tickers played a voice", A.nMine - A.castV]);
    if (B.st.bad.length) bad.push([fid, sd, ...B.st.bad[0], "(" + B.st.bad.length + ")"]);
    if (B.strayClose) bad.push([fid, sd, "a close voice with no window", B.strayClose]);
    if (B.where) bad.push([fid, sd, "a voice from the wrong place or with opts", B.where]);
    if (B.castV !== B.casts) bad.push([fid, sd, "cast voices vs casts", B.castV, B.casts]);
    casts += B.casts; castV += B.castV; unticked += B.casts - B.wins.length;
    x2 += B.st.x2; x1foe += B.st.x1foe; me += B.st.me; shade += B.st.shade; stunV += B.st.v2;
    for (const W of B.wins){
      ends[W.end]++; closes += W.closeV;
      if (W.closeV !== (W.end === "clock" ? 1 : 0)) bad.push([fid, sd, W.end + " close played closes", W.closeV]);
      if (W.end === "clock"){ perWin.push(W.stunV);
        pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, stuns: W.stunV }); }
    }
  }
  perWin.sort((x, y) => x - y);
  return { fights, same, otherSame, diff: diff.slice(0, 4), ends, casts, castV, unticked, x2, x1foe, me, shade,
           stunV, closes, pick, perWinMed: perWin.length ? perWin[perWin.length >> 1] : null,
           perWinMin: perWin.length ? perWin[0] : null, perWinMax: perWin.length ? perWin[perWin.length - 1] : null,
           bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rows, ME]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const oS = P.tickStatus, oU = P.tickUnmake;
  let sS = oS.toString(); for (const [anc, code] of rows.status) sS = sS.replace(anc, () => code);
  let sU = oU.toString(); for (const [anc, code] of rows.unmake) sU = sU.replace(anc, () => code);
  const pS = (0, eval)("(function " + sS + ")"), pU = (0, eval)("(function " + sU + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.tickStatus = pS; P.tickUnmake = pU;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickStatus = oS; P.tickUnmake = oU; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds, ME, REASON]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype;
""" + COMMON_JS + r"""
  const res = [];
  if (!P.tickUnmake) return { err: "no tickUnmake" };
  const oS = P.tickStatus, oU = P.tickUnmake, oB = P.breakSpin;
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const log = [], other = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    let inS = 0, inU = 0, x2 = 0, clock = 0, badStun = 0, cur = null, h = 2166136261;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, inS ? "S" : inU ? "U" : "-", Object.keys(p).join(",")]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    P.breakSpin = function(g, reason){ if (inS && reason === REASON && cur) cur.push(g.hexStunMul);
      return oB.apply(this, arguments); };
    P.tickStatus = function(g, dt){ const c0 = log.length; cur = []; inS = 1;
      try { return oS.call(this, g, dt); }
      finally { inS = 0; const v = log.slice(c0).filter(e => e[0] === ME + "-stun").length;
        const want = cur.length && cur[0] > 1 ? 1 : 0; x2 += want; if (v !== want) badStun++; cur = null; } };
    P.tickUnmake = function(dt){ const Z0 = f.ultUnmake; inU = 1;
      try { return oU.call(this, dt); }
      finally { inU = 0; if (Z0 && f.ultUnmake !== Z0 && Z0.t >= Z0.dur && f.alive && foe.alive) clock++; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; h = dig(h, m); } }
    finally { P.tickStatus = oS; P.tickUnmake = oU; P.breakSpin = oB; if (had) S.play = op; else delete S.play; }
    const T = f.unmakeTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.winner ? m.winner.w.id : null,
                                    m.a.unmakeTally || null, m.b.unmakeTally || null, m.shots ? m.shots.length : null, h]),
               casts: T.casts || 0, x2, clock, badStun,
               castV: log.filter(e => e[0] === ME && e[1] === "-").length,
               stunV: log.filter(e => e[0] === ME + "-stun" && e[1] === "S").length,
               closeV: log.filter(e => e[0] === ME + "-close" && e[1] === "U").length,
               stray: log.filter(e => e[2] !== "w" || (e[0] === ME) !== (e[1] === "-")
                                      || (e[0] === ME + "-stun" && e[1] !== "S")
                                      || (e[0] === ME + "-close" && e[1] !== "U")).length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def seg(x, a, b):
    return x[int((T0 + a) * SR):int((T0 + b) * SR)]


def cen(x, a, b):
    """The power-weighted mean frequency over [a, b] s after the event, Hz."""
    np = _np()
    y = seg(x, a, b)
    P = np.abs(np.fft.rfft(y * np.hanning(len(y)), 1 << 15)) ** 2
    fr = np.fft.rfftfreq(1 << 15, 1 / SR)
    return float((P * fr).sum() / max(P.sum(), 1e-30))


def e_span(x, win, a, b, hop=0.001):
    """The RMS envelope (window `win`, 1 ms hop) of the voice, the windows
    CENTRED in [a, b] s after the event, dB."""
    np = _np()
    y = x[int(T0 * SR):]
    r, c = env(y, win, hop)
    k = (c >= a) & (c <= b)
    return 20 * np.log10(np.maximum(r[k], 1e-9)), c[k]


def top_db(x):
    return db(basic(x)["top"])


def held_var(x, a, b):
    """HELD: p95 - p5 of E25 over [a, b], dB."""
    np = _np()
    e, _ = e_span(x, 0.025, a + 0.0125, b - 0.0125)
    return float(np.percentile(e, 95) - np.percentile(e, 5)) if len(e) else 99.0


def span_level(x, a, b, win=0.05):
    np = _np()
    e, _ = e_span(x, win, a + win / 2, b - win / 2)
    return float(np.median(e)) if len(e) else -180.0


def loudest(x, a, b, win=0.05):
    e, _ = e_span(x, win, a + win / 2, b - win / 2)
    return float(e.max()) if len(e) else -180.0


def heard_at(x, p90, a, lo=PHONE_HZ, hi=12000.0):
    """HEARD over the 100 ms from `a` s after the event (the score's p90 is read
    over 100 ms windows): the best third-octave >= 200 Hz, dB, and where."""
    b_ = bands(seg(x, a, a + 0.1))
    best = max(((b_[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))
    return db(best[0]), best[1]


def cut_ms(x, a_held, b_held):
    """CUT and PREFADE (see the docstring): the close's stop, read on the 5 ms
    RMS at a 1 ms hop against its held level (the median over the held span)."""
    np = _np()
    y = x[int(T0 * SR):]
    r5, c5 = env(y, 0.005, 0.001)
    e5 = 20 * np.log10(np.maximum(r5, 1e-9))
    k = (c5 >= a_held) & (c5 <= b_held)
    held = float(np.median(e5[k]))
    on = np.nonzero(e5 >= held - 3)[0]
    i0 = int(on[-1])
    after = np.nonzero(e5[i0:] <= held - 30)[0]
    if not len(after):
        return 999.0, -99.0, held, float(c5[i0])
    i1 = i0 + int(after[0])
    cut = (c5[i1] - c5[i0]) * 1000
    r25, c25 = env(y, 0.025, 0.001)
    e25 = 20 * np.log10(np.maximum(r25, 1e-9))
    held25 = float(np.median(e25[(c25 >= a_held) & (c25 <= b_held)]))
    kk = (c25 >= c5[i0] - 0.1) & (c25 <= c5[i0] - 0.0125)
    pre = float(e25[kk].min() - held25) if kk.any() else -99.0
    return float(cut), pre, held, float(c5[i0])


def onset_over(x, a_held, b_held):
    """ONSET: the loudest 5 ms of the first 40 ms over the held level (5 ms, median), dB."""
    np = _np()
    e, _ = e_span(x, 0.005, 0.0025, 0.04)
    eh, _ = e_span(x, 0.005, a_held, b_held)
    return float(e.max() - np.median(eh))


def cont_db(x, a=0.05, b=0.30):
    """CONT: the lowest 5 ms RMS over [a, b] re the voice's loudest 5 ms, dB."""
    np = _np()
    y = x[int(T0 * SR):]
    r, c = env(y, 0.005, 0.001)
    e = 20 * np.log10(np.maximum(r, 1e-9))
    k = (c >= a) & (c <= b)
    return float(e[k].min() - e.max())


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v79 s4 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms; 'a glass crack': struck (RISE <= 3 ms, the peak "
    "in the first 10 ms), bright (the first 30 ms's centroid >= 3 kHz) and glass: over 1-21 ms "
    "(before the hum) TONAL >= 12 dB over 800-8000 Hz and INHARM -- the strongest peak 1.5x-4x its "
    "note >= 60 cents from every whole multiple and within 20 dB of it; 'into a hum': over the hum's "
    "held span (100 ms to its release) a note (TONAL >= 15 dB, 60-2000 Hz), low (its FFT peak, "
    "60-1000 Hz, <= 400 Hz), held (HELD <= 3 dB, FLUTTER <= 3 dB at its note), under the crack (INTO "
    ">= 4) and heard (HEARD over 100 ms from 120 ms >= +6 dB); the crack heard (HEARD over its first "
    "100 ms >= +6 dB). Level: TOP between 0.5x the blow's loudest 50 ms on its LOUDEST draw and 1.0x "
    "on its QUIETEST, on every draw; the hum's held E50 between 16 and 4 dB under TOP. Register "
    "against rune-crack, each runic and twinblade cast with a voice of its own, BAR, hex-snap, the "
    "blow and the death voice -- and Angelus's cast and close when its rows are given -- each <= "
    "0.80. Tiebreak: the most distinct register (to 0.05), then the fewest synth calls, then the "
    "order listed.")

STUN_RULE = (
    "'hex's own snap': SNAP -- the first 30 ms's register against the hex-snap's first 30 ms >= 0.90 "
    "and its sample peak within 1.5 dB of the hex-snap's on the same draw, struck (RISE <= 3 ms, the "
    "peak in the first 10 ms), on every draw; 'lengthened': the tail is the snap's own -- TAIL-REG "
    "(60-400 ms against the hex-snap) >= 0.60; '(0.4s tail)' 'to match' the 0.4 s stun: AUDIBLE "
    "330-470 ms, GONE <= 470 ms, and CONT >= -34 dB (no gap before 300 ms); the snap leads: the "
    "tail's loudest 50 ms (60 ms on) 15-5 dB under the snap's TOP; heard: HEARD over 100 ms from 100 "
    "ms >= +6 dB. Register against the blow, the wall tick, rune-crack, BAR, the picked cast and each "
    "runic and twinblade cast with a voice of its own each <= 0.80. Its cost (round 6): <= 40 synth "
    "calls a stun -- it fires ~20 times a window. Tiebreak: the highest TAIL-REG "
    "(the most the snap's own, to 0.05), then the fewest synth calls, then the order listed.")

CLOSE_RULE = (
    "'the hum': over its held span (30-120 ms) its note within 30 cents of the cast's hum's, its "
    "register against the cast's hum (its held span) >= 0.90, its level within 3 dB of the cast's "
    "hum's, and no crack (ONSET <= +6 dB); 'cutting out': CUT <= 40 ms and PREFADE >= -3 dB (from "
    "level, not the end of a fade); the length: AUDIBLE 150-300 ms, GONE <= 300 ms; heard: HEARD "
    "over 100 ms from 30 ms >= +6 dB. Register against rune-crack, the blow, the wall tick, the death "
    "voice, hex-snap and the picked stun each <= 0.80. Tiebreak (round 3): the most distinct "
    "register (to 0.05), then the fewest synth calls, then the order listed.")


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
    if not 330 <= M["aud"] <= 470: why.append(f"audible {M['aud']:.0f} ms, not 330-470")
    if M["gone"] > 470: why.append(f"gone at {M['gone']:.0f} ms > 470")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms > 3 (not struck)")
    if M["pk_ms"] > 10: why.append(f"peaks at {M['pk_ms']:.0f} ms (not a crack)")
    if M["c_cen"] < 3000: why.append(f"crack centroid {M['c_cen']:.0f} Hz < 3000 (not bright)")
    if M["g_tonal"] < 12: why.append(f"the crack's ring {M['g_tonal']:.1f} dB tonal < 12 (clicks, not glass)")
    if M["g_inh_c"] < 60 or M["g_inh_db"] < -20:
        why.append(f"the crack's partial at {M['g_inh_r']:.2f}x is {M['g_inh_c']:.0f} c from a harmonic, "
                   f"{M['g_inh_db']:+.0f} dB (not glass)")
    if M["h_none"]:
        why.append("no hum")
    else:
        if M["h_tonal"] < 15: why.append(f"the hum {M['h_tonal']:.1f} dB tonal < 15 (not a note)")
        if M["h_note"] > 400: why.append(f"the hum's note {M['h_note']:.0f} Hz > 400 (not low)")
        if M["h_held"] > 3: why.append(f"the hum moves {M['h_held']:.1f} dB (not held)")
        if M["h_flut"] > 3: why.append(f"the hum flutters {M['h_flut']:.1f} dB")
        if M["into"] < 4: why.append(f"into {M['into']:.1f} < 4 (the crack is not over the hum)")
        if M["h_heard"] < 6: why.append(f"the hum heard {M['h_heard']:+.1f} dB < +6")
        if not -16 <= M["h_db"] <= -4: why.append(f"the hum {M['h_db']:+.1f} dB re the top, not -16..-4")
    if M["heard"] < 6: why.append(f"the crack heard {M['heard']:+.1f} dB < +6")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    _regs_why(M, why)
    return why


def stun_why(M, lev):
    why = []
    if M["snap_reg"] < 0.90: why.append(f"snap register {M['snap_reg']:.2f} < 0.90 (not the snap)")
    if M["snap_pk"] > 1.5: why.append(f"snap peak {M['snap_pk']:.1f} dB off the hex-snap's")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms > 3")
    if M["pk_ms"] > 10: why.append(f"peaks at {M['pk_ms']:.0f} ms")
    if M["tail_reg"] < 0.60: why.append(f"tail register {M['tail_reg']:.2f} < 0.60 (not the snap's own)")
    if not (330 <= M["aud_lo"] and M["aud_hi"] <= 470):
        why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 330-470")
    if M["gone_hi"] > 470: why.append(f"gone at {M['gone_hi']:.0f} ms > 470")
    if M["cont"] < -34: why.append(f"a gap: {M['cont']:+.1f} dB before 300 ms")
    if not -15 <= M["tail_db"] <= -5: why.append(f"the tail {M['tail_db']:+.1f} dB re the snap, not -15..-5")
    if M["t_heard"] < 6: why.append(f"the tail heard {M['t_heard']:+.1f} dB < +6")
    if M["calls"] > STUN_CALLS: why.append(f"{M['calls']} synth calls > {STUN_CALLS} (it fires ~20 times a window)")
    _regs_why(M, why)
    return why


def close_why(M, lev):
    why = []
    if abs(M["c_note"]) > 30: why.append(f"its note {M['c_note']:+.0f} c off the cast's hum")
    if M["h_reg"] < 0.90: why.append(f"register vs the cast's hum {M['h_reg']:.2f} < 0.90 (not the hum)")
    if abs(M["lvl"]) > 3: why.append(f"held {M['lvl']:+.1f} dB re the cast's hum")
    if M["onset"] > 6: why.append(f"onset {M['onset']:+.1f} dB over held (a crack)")
    if M["cut"] > 40: why.append(f"cut {M['cut']:.0f} ms > 40 (not cutting out)")
    if M["pre"] < -3: why.append(f"prefade {M['pre']:+.1f} dB (it fades before it stops)")
    if not 150 <= M["aud"] <= 300: why.append(f"audible {M['aud']:.0f} ms, not 150-300")
    if M["gone"] > 300: why.append(f"gone at {M['gone']:.0f} ms > 300")
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


def _slug(name):
    return name.replace(" ", "-").lower()


def sig4(v):
    return float(f"{v:.4g}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Spellbreaker's stage 5 (the Unmaking)")
    ap.add_argument("--also", action="append", default=[],
                    help="another link carrying it (e.g. carried onto a newer tip): the rows as text there")
    ap.add_argument("--out", default="../05-reference/v111")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=111601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "stun": STUN_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("tickStatus hex proc", STUN_ANCHOR),
                    ("tickUnmake close", CLOSE_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("spellbreaker-stun", "spellbreaker-close", '(w === "spellbreaker")', FALLBACK):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nUNMAKING -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
                           "w.ult && w.ult.stunMul, w.ult && w.ult.dur])")
        ids = [w_[0] for w_ in W_]
        if ME not in ids:
            raise SystemExit("no spellbreaker in this build")
        me = [w_ for w_ in W_ if w_[0] == ME][0]
        if abs(me[3] - BLADE) > 1e-9 or me[4] != "unmake" or me[5] != 2:
            raise SystemExit(f"Spellbreaker is {me} -- this lab levels against blade {BLADE} and an unmake x2")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        if play_src.count(SFX_ANCHOR) != 1:
            raise SystemExit("the Sfx anchor is not in play() exactly once")
        # the snap the STRETCH candidate writes out must be the page's own
        m_ = re.search(r'else if \(kind === "hex-snap"\)\{.*?\*/\s*(this\._burst.*?type:"triangle" \}\);)',
                       play_src, re.S)
        nums = [float(v) for v in re.findall(r"(?<![a-z])(\d+(?:\.\d+)?)", m_.group(1))] if m_ else []
        if nums != [float(v) for v in SNAP]:
            raise SystemExit(f"the page's hex-snap is not the one this lab writes out: {nums}")
        if page.evaluate("() => AC.STATUS ? AC.STATUS.hex.stunFor : (0, eval)('STATUS').hex.stunFor") != 0.2:
            raise SystemExit("STATUS.hex.stunFor is not 0.2 -- the stun is not 0.4 s in a window")

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
        for name, (kind, p) in [("rune-crack", ("ult", {"w": FALLBACK})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                (f"hit@{BLADE:g}", ("hit", {"dmg": BLADE, "crit": False})),
                                ("wall", ("wall", {})), ("death", ("death", {})), ("hex-snap", ("hex-snap", {}))]:
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
        if ME not in fall_ids:
            raise SystemExit("Spellbreaker's cast is not rune-crack today -- this lab adds its arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_[0] for w_ in W_ if w_[1] == SCHOOL_AFF and w_[0] not in fall_ids]
        types = [w_[0] for w_ in W_ if w_[2] == TYPE_SHAPE and w_[0] not in fall_ids]
        print(f"  the runic casts with their own voice: {', '.join(school) or '-'};  the twinblade casts': "
              f"{', '.join(types) or '-'}")

        # the noise draws of every reference
        REFS = {"hit": ("hit", {"dmg": BLADE, "crit": False}), "wall": ("wall", {}),
                "rune-crack": ("ult", {"w": FALLBACK}), "death": ("death", {}), "BAR": ("ult", {"w": "axiom"}),
                "hex-snap": ("hex-snap", {}), "clank": ("clank", {"mass": 1.1})}
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
        # the hex-snap's first 30 ms, per draw (SNAP)
        SNAP30 = [bands(seg(x, 0.0, 0.03)) for x in RX["hex-snap"]]
        snap_pk = [float(np.abs(x).max()) for x in RX["hex-snap"]]
        snap_top = [m_["top"] for m_ in RD_["hex-snap"]]
        # the type's voices on the batch line (Angelus), from its own rows
        peer_regs, peer_names = [], []
        for pf, prow in peer_sfx:
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            for w_ in sorted(set(re.findall(r'w === "([a-z-]+)"', "".join(c for _a, c in ps)))):
                base_ = w_.split("-")[0]
                if base_ in PEER_TYPE and (w_ == base_ or w_.endswith("-close")):
                    RB["peer:" + w_] = [bands(R([["arm", T0, "ult", {"w": w_}]], rows=ps, new=False)[0][int(T0 * SR):])]
                    peer_regs.append("peer:" + w_)
                    if peer_name(pf) not in peer_names:
                        peer_names.append(peer_name(pf))
        h_lo, h_hi = min(m_["top"] for m_ in RD_["hit"]), max(m_["top"] for m_ in RD_["hit"])
        w_hi = max(m_["top"] for m_ in RD_["wall"])
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD_['hit']):.3f}-{max(m_['peak'] for m_ in RD_['hit']):.3f};  the wall "
              f"tick: {min(m_['top'] for m_ in RD_['wall']):.4f}-{w_hi:.4f};  the hex-snap: loudest 50 ms "
              f"{min(snap_top):.4f}-{max(snap_top):.4f}, peak {min(snap_pk):.3f}-{max(snap_pk):.3f}")
        if peer_regs:
            print(f"  the type's voices on the batch line, from --peer-rows: {', '.join(peer_regs)}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        p90 = bed_p90(bed[int(2 * SR):int(10 * SR)])
        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi, snap_top=[min(snap_top), max(snap_top)],
                             snap_peak=[min(snap_pk), max(snap_pk)])
        wav("spellbreaker-ctl-runecrack.wav", rcx)
        wav(f"spellbreaker-ctl-hit{BLADE:g}.wav", ctl[f"hit@{BLADE:g}"]["x"])
        wav("spellbreaker-ctl-hexsnap.wav", ctl["hex-snap"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a glass crack into a hum, 0.4s'. The declared crack (three 6 kHz clicks, a glass rod "
              f"at G6); the hum re-struck every cycle, 30 ms strikes. Level-matched: TOP {tgt_c:.4f} (the centre "
              f"of {lev_c['lo']:.4f}-{lev_c['hi']:.4f}), the hum held {HUM_UNDER_DB:g} dB under it, AUDIBLE "
              f"{AUD_TGT:g} ms")

        def cx(sp, g, kh, S1, part="both", seed=None):
            return R([["body", T0, cast_body(sp, g, kh, S1, part), {}]], seed=seed)

        def hum_span(S1):
            return 0.10, round(S1 - HUM_REL - 0.005, 4)

        def calib_cast(sp):
            g, kh, S1 = 0.3, 0.05, 0.35
            for _ in range(6):
                x = cx(sp, g, kh, S1)[0]
                B = basic(x)
                S1 = round(min(0.6, max(0.2, S1 + (AUD_TGT - B["aud"]) / 1000)), 4)
                x = cx(sp, g, kh, S1)[0]
                a_, b_ = hum_span(S1)
                hdb = span_level(x, a_, b_) - top_db(x)
                kh = sig4(kh * 10 ** ((-HUM_UNDER_DB - hdb) / 20))
                g = sig4(g * tgt_c / basic(cx(sp, g, kh, S1)[0])["top"])
            return g, kh, S1

        CAST_REGS = ["rune-crack"] + school + types + ["BAR", "hex-snap", "hit", "death"] + peer_regs

        def cast_measure(name, x, draws, calls, S1, regs=CAST_REGS):
            M = basic(x); M.update(x=x, calls=calls, name=name, S1=S1)
            M["gone"] = max(basic(d_)["gone"] for d_ in draws)
            M["c_cen"] = cen(x, 0.0, 0.03)
            M["g_tonal"] = tonal(draws, T0 + 0.001, T0 + 0.021, 800, 8000)
            if float(np.abs(seg(x, 0.001, 0.021)).max()) > 1e-6:
                M["g_note"] = pitch(x, T0 + 0.001, T0 + 0.021, lo=800, hi=8000)
                M["g_inh_r"], M["g_inh_c"], M["g_inh_db"] = inharm(x, T0 + 0.001, T0 + 0.021, M["g_note"])
            else:                                   # nothing sounds before the hum (the HUM control)
                M["g_note"], M["g_inh_r"], M["g_inh_c"], M["g_inh_db"] = 0.0, 0.0, 0.0, -99.0
            a_, b_ = hum_span(S1) if S1 else (0.10, 0.28)
            M["span"] = (a_, b_)
            hs = seg(x, a_, b_)
            M["h_none"] = float(np.sqrt((hs ** 2).mean())) < 1e-5
            if not M["h_none"]:
                M["h_tonal"] = tonal(draws, T0 + a_, T0 + b_, 60, 2000)
                M["h_note"] = pitch(x, T0 + a_, T0 + b_, lo=60, hi=1000)
                M["h_held"] = held_var(x, a_, b_)
                M["h_flut"] = flutter(x, T0 + a_ + 0.06, T0 + b_ - 0.06, M["h_note"]) if b_ - a_ >= 0.13 else 99.0
                M["into"] = M["c_cen"] / max(cen(x, a_, b_), 1e-9)
                M["h_heard"], M["h_hfc"] = heard_at(x, p90, 0.12)
                M["h_db"] = span_level(x, a_, b_) - top_db(x)
                M["h_e5"] = span_level(x, a_, b_, win=0.005)
                M["h_bands"] = bands(hs)
            else:
                for k in ("h_tonal", "h_note", "h_held", "h_flut", "into", "h_heard", "h_db", "h_e5"):
                    M[k] = float("nan")
            M["heard"], M["heard_fc"] = heard_at(x, p90, 0.0)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws)
            M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in regs}
            return M

        def f_(v, spec):
            return format(v, spec) if v == v else "  -"

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<12}{M.get('g', 0):>8.4g}{M.get('kh', 0):>8.4g}{M.get('S1', 0) or 0:>7.3f}"
                  f"{M['calls']:>6d}{M['top']:>8.4f}{M['aud']:>5.0f}{M['gone']:>5.0f}{M['rise']:>4.0f}{M['pk_ms']:>4.0f}"
                  f"{M['c_cen']:>7.0f}{M['g_tonal']:>6.1f}{M['g_inh_c']:>5.0f}{M['g_inh_db']:>5.0f}"
                  f"{f_(M['h_tonal'], '>6.1f')}{f_(M['h_note'], '>6.0f')}{f_(M['h_held'], '>5.1f')}"
                  f"{f_(M['h_flut'], '>5.1f')}{f_(M['into'], '>6.1f')}{f_(M['h_db'], '>6.1f')}"
                  f"{M['heard']:>6.1f}{f_(M['h_heard'], '>6.1f')}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<12}{'g':>8}{'kh':>8}{'S1':>7}{'calls':>6}{'top':>8}{'aud':>5}{'gone':>5}{'rs':>4}{'pk':>4}"
              f"{'crkC':>7}{'glsT':>6}{'inhC':>5}{'inhD':>5}{'humT':>6}{'note':>6}{'held':>5}{'flut':>5}{'into':>6}"
              f"{'humdB':>6}{'hrd':>6}{'hrdH':>6}{'reg':>6}")
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g, kh, S1 = calib_cast(sp)
            x, calls = cx(sp, g, kh, S1)
            x2, _ = cx(sp, g, kh, S1)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"cast {name} does not reproduce")
            draws = [cx(sp, g, kh, S1, seed=sd)[0] for sd in NOISE_SEEDS]
            M = cast_measure(name, x, draws, calls[0], S1)
            M.update(sp=sp, g=g, kh=kh); M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"spellbreaker-cast-{_slug(name)}.wav", x)
        # the controls, on DRONE and its levels
        c0 = rows_c[0]
        ctlc = []
        for cname, part in (("0 CRACK", "crack"), ("0 HUM", "hum"), ("0 CLICKS", "clicks")):
            dr = [cx(c0["sp"], c0["g"], c0["kh"], c0["S1"], part, seed=sd)[0] for sd in NOISE_SEEDS]
            xc, cc = cx(c0["sp"], c0["g"], c0["kh"], c0["S1"], part)
            M = cast_measure(cname, xc, dr, cc[0], c0["S1"])
            M.update(g=c0["g"], kh=c0["kh"]); ctlc.append(M)
            wav(f"spellbreaker-cast-{_slug(cname)}.wav", xc)
        M = cast_measure("0 RUNECRACK", rcx, RX["rune-crack"], 0, None); ctlc.append(M)
        for M in ctlc:
            M["why"] = cast_why(M, lev_c); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<12} {blurb}")
        print("    0 CRACK      DRONE's crack alone -- a control on 'into a hum'\n"
              "    0 HUM        DRONE's hum alone -- a control on 'a glass crack'\n"
              "    0 CLICKS     DRONE with the crack's clicks but not its glass -- a control on 'glass'\n"
              "    0 RUNECRACK  the fallback it replaces")
        _show(rows_c, ctlc, CAST_RULE, "cast")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        Ca = rows_c[ci]
        print(f"  PICK  {Ca['name']}  g {Ca['g']}, kh {Ca['kh']}, S1 {Ca['S1']}, {Ca['calls']} synth calls; TOP "
              f"{Ca['top']:.4f} = {db(Ca['top'] / h_lo):+.1f} dB re the hit @ {BLADE:g} (quietest draw); the hum "
              f"{Ca['h_note']:.1f} Hz at {Ca['h_db']:+.1f} dB re TOP")

        # ---- THE STUN ------------------------------------------------------
        print(f"\nSTUN -- 'hex's own snap, lengthened to match (0.4s tail)'. The snap is `this.play(\"hex-snap\")` "
              f"(STRETCH writes its three lines out). Level-matched: each tail's loudest 50 ms {TAIL_UNDER_DB:g} dB "
              f"under the snap's TOP, AUDIBLE {AUD_TGT:g} ms")

        def sx(sp, kt, D, seed=None, snap=True, part=None):
            return R([["body", T0, stun_body(sp, kt, D, Ca, snap=snap, part=part), {}]], seed=seed)

        def rms(x, a, b):
            return float(np.sqrt((seg(x, a, b) ** 2).mean()))
        # the snap's own ping over its own band, in RMS over each line's length (render.py's draw)
        s_ = SNAP
        xb_ = R([["body", T0, f'this._burst(t, {{ freq: {s_[0]}, q: {s_[1]}, gain: {s_[2]}, dur: {s_[3]}, '
                              f'type:"bandpass" }});', {}]])[0]
        xp_ = R([["body", T0, f'this._tone (t, {{ freq: {s_[8]}, to: {s_[9]}, gain: {s_[10]}, dur: {s_[11]}, '
                              f'type:"triangle" }});', {}]])[0]
        PING_BAND = rms(xp_, 0.0, s_[11]) / rms(xb_, 0.0, s_[3])
        print(f"  the snap's own ping over its band, RMS over each line's length: {PING_BAND:.3f} "
              f"({db(PING_BAND):+.1f} dB) -- SIZZLE's ring is solved to it")

        s_top0 = snap_top[0]

        def tail_db(x, top_ref):
            return loudest(x, 0.06, 0.6) - db(top_ref)

        def calib_stun(sp):
            if sp["kind"] == "stretch":
                k = 9.0
                for _ in range(6):
                    B = basic(sx(sp, 0, k)[0])
                    k = sig4(min(18.0, max(1.0, k * AUD_TGT / max(B["aud"], 1.0))))
                return 0.0, k
            kt, D = {"ring": 0.02, "body": 0.05, "rattle": 0.03, "echo": 0.1, "sizzle": 0.1}[sp["kind"]], 0.45
            # ROUND 3: the cap is the kind's own -- a single burst is held to the
            # 0.6 s noise buffer (0.55), a tone is not (RING took the burst's cap
            # in round 2 and could not reach 0.4 s), a train's length is its own
            cap = {"ring": 3.0, "body": 0.55, "rattle": 0.6, "echo": 0.6, "sizzle": 0.6}[sp["kind"]]
            for _ in range(8):
                if sp["kind"] == "sizzle":
                    xr = sx(sp, kt, D, part="ring")[0]; xt = sx(sp, kt, D, part="train")[0]
                    sp["w"] = sig4(sp.get("w", 0.363) * PING_BAND / (rms(xr, 0.06, 0.3) / rms(xt, 0.06, 0.3)))
                x = sx(sp, kt, D)[0]
                kt = sig4(kt * 10 ** ((-TAIL_UNDER_DB - tail_db(x, s_top0)) / 20))
                B = basic(sx(sp, kt, D)[0])
                D = round(min(cap, max(0.1, D * AUD_TGT / max(B["aud"], 1.0))), 3)
            return kt, D

        STUN_REGS = ["hit", "wall", "rune-crack", "BAR"] + school + types

        def stun_measure(name, sp, kt, D, snap=True, x_=None, draws_=None, calls_=0):
            if x_ is None:
                x, calls = sx(sp, kt, D, snap=snap)
                draws = [sx(sp, kt, D, seed=sd, snap=snap)[0] for sd in NOISE_SEEDS]
                calls_ = calls[0]
            else:
                x, draws = x_, draws_
            M = basic(x); M.update(x=x, calls=calls_, name=name, sp=sp, kt=kt, D=D)
            Bd = [basic(d_) for d_ in draws]
            M["aud_lo"] = min(b_["aud"] for b_ in Bd); M["aud_hi"] = max(b_["aud"] for b_ in Bd)
            M["gone_hi"] = max(b_["gone"] for b_ in Bd)
            M["rise"] = max(b_["rise"] for b_ in Bd); M["pk_ms"] = max(b_["pk_ms"] for b_ in Bd)
            M["snap_reg"] = float(np.median([cos(bands(seg(d_, 0.0, 0.03)), SNAP30[i]) for i, d_ in enumerate(draws)]))
            M["snap_pk"] = max(abs(db(float(np.abs(d_).max()) / snap_pk[i])) for i, d_ in enumerate(draws))
            M["tail_reg"] = float(np.median([cos(bands(seg(d_, 0.06, 0.4)), RB["hex-snap"][i])
                                             for i, d_ in enumerate(draws)]))
            M["cont"] = min(cont_db(d_) for d_ in draws)
            M["tail_db"] = max(tail_db(d_, snap_top[i]) for i, d_ in enumerate(draws))
            M["t_heard"] = min(heard_at(d_, p90, 0.1)[0] for d_ in draws)
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in STUN_REGS}
            M["regs"]["cast"] = mreg(DB, Ca["DB"])
            M["snapself"] = mreg(DB, RB["hex-snap"])
            return M

        def stun_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<11}{M['kt']:>8.4g}{M['D']:>7.4g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud_lo']:>5.0f}"
                  f"{M['aud_hi']:>5.0f}{M['gone_hi']:>5.0f}{M['rise']:>4.0f}{M['pk_ms']:>4.0f}{M['snap_reg']:>6.2f}"
                  f"{M['snap_pk']:>6.1f}{M['tail_reg']:>6.2f}{M['cont']:>7.1f}{M['tail_db']:>7.1f}{M['t_heard']:>6.1f}"
                  f"{M['snapself']:>6.2f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<11}{'kt':>8}{'D/k':>7}{'calls':>6}{'top':>8}{'audL':>5}{'audH':>5}{'gone':>5}{'rs':>4}"
              f"{'pk':>4}{'snapR':>6}{'snpPk':>6}{'tailR':>6}{'cont':>7}{'tailDb':>7}{'hrdT':>6}{'self':>6}{'reg':>6}")
        rows_s = []
        for name, sp0, _b in STUN_CANDIDATES:
            sp = dict(sp0)
            kt, D = calib_stun(sp)
            x1, _ = sx(sp, kt, D); x2, _ = sx(sp, kt, D)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"stun {name} does not reproduce")
            M = stun_measure(name, sp, kt, D); M["why"] = stun_why(M, None)
            rows_s.append(M); stun_line(M)
            wav(f"spellbreaker-stun-{_slug(name)}.wav", M["x"])
        ctls = []
        M = stun_measure("0 PLAIN", dict(kind="plain"), 0.0, 0.0, x_=RX["hex-snap"][0], draws_=RX["hex-snap"],
                         calls_=3)
        ctls.append(M)
        r0 = rows_s[1]
        M = stun_measure("0 TAIL", r0["sp"], r0["kt"], r0["D"], snap=False); ctls.append(M)
        wav("spellbreaker-stun-0-tail.wav", M["x"])
        for M in ctls:
            M["why"] = stun_why(M, None); stun_line(M)
        for (name, _sp, blurb) in STUN_CANDIDATES:
            print(f"    {name:<11} {blurb}")
        print("    0 PLAIN     the hex-snap itself -- a control on 'lengthened (0.4s tail)'\n"
              "    0 TAIL      RING's tail without the snap -- a control on 'hex's own snap'")
        _show(rows_s, ctls, STUN_RULE, "stun")
        ok, fb = _gate(rows_s, "stun")
        si = fb if ok is None else min(ok, key=lambda i: (-round(rows_s[i]["tail_reg"] / 0.05), rows_s[i]["calls"], i))
        St = rows_s[si]
        print(f"  PICK  {St['name']}  kt {St['kt']}, D/k {St['D']}, {St['calls']} synth calls; audible "
              f"{St['aud_lo']:.0f}-{St['aud_hi']:.0f} ms; the tail {St['tail_db']:+.1f} dB re the snap; loudest 50 ms "
              f"{db(St['top'] / h_lo):+.1f} dB re the blow, {db(St['top'] / w_hi):+.1f} dB re the wall")

        # ---- THE CLOSE -----------------------------------------------------
        ha, hb = Ca["span"]
        cast_hum_bands = Ca["h_bands"]
        print(f"\nCLOSE -- 'the hum cutting out', on {Ca['name']}'s hum ({Ca['h_note']:.1f} Hz). Level-matched: its "
              f"held level (5 ms RMS, {HELD_C[0]:g}-{HELD_C[1]:g} s) on the cast's hum's ({Ca['h_e5']:+.1f} dB)")

        def lx(sp, h):
            return R([["body", T0, close_body(Ca, sp, h), {}]])

        def calib_close(sp):
            h = round(Ca["g"] * Ca["kh"], 6)
            for _ in range(4):
                x = lx(sp, h)[0]
                h = sig4(h * 10 ** ((Ca["h_e5"] - span_level(x, *HELD_C, win=0.005)) / 20))
            return h

        CLOSE_REGS = ["rune-crack", "hit", "wall", "death", "hex-snap"]

        def close_measure(name, sp, x, calls, h=0.0):
            M = basic(x); M.update(x=x, calls=calls, name=name, sp=sp, h=h)
            M["note"] = pitch(x, T0 + HELD_C[0], T0 + HELD_C[1], lo=60, hi=1000)
            M["c_note"] = cents(M["note"], Ca["h_note"])
            M["h_reg"] = cos(bands(seg(x, *HELD_C)), cast_hum_bands)
            M["lvl"] = span_level(x, *HELD_C, win=0.005) - Ca["h_e5"]
            M["onset"] = onset_over(x, *HELD_C)
            M["cut"], M["pre"], M["held"], M["cut_at"] = cut_ms(x, *HELD_C)
            M["heard"], M["heard_fc"] = heard_at(x, p90, HELD_C[0])
            DB = [bands(x[int(T0 * SR):])]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CLOSE_REGS}
            M["regs"]["stun"] = mreg(DB, St["DB"])
            return M

        def close_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<11}{M['h']:>9.4g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud']:>5.0f}{M['gone']:>5.0f}"
                  f"{M['note']:>7.1f}{M['c_note']:>6.0f}{M['h_reg']:>6.2f}{M['lvl']:>6.1f}{M['onset']:>7.1f}"
                  f"{M['cut']:>6.0f}{M['pre']:>7.1f}{M['heard']:>7.1f}{max(r_.values()):>6.2f} ({max(r_, key=r_.get)})")

        print(f"  {'cand':<11}{'h':>9}{'calls':>6}{'top':>8}{'aud':>5}{'gone':>5}{'note':>7}{'c':>6}{'hReg':>6}"
              f"{'lvl':>6}{'onset':>7}{'cut':>6}{'pre':>7}{'heard':>7}{'reg':>6}")
        rows_l = []
        for name, sp, _b in CLOSE_CANDIDATES:
            h = calib_close(sp)
            x, calls = lx(sp, h)
            x2, _ = lx(sp, h)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"close {name} does not reproduce")
            M = close_measure(name, sp, x, calls[0], h); M["why"] = close_why(M, None)
            rows_l.append(M); close_line(M)
            wav(f"spellbreaker-close-{_slug(name)}.wav", x)
        ctll = []
        fsp = dict(kind="fade")
        hf = calib_close(fsp)
        xf, cf = lx(fsp, hf)
        ctll.append(close_measure("0 FADE", fsp, xf, cf[0], hf))
        wav("spellbreaker-close-0-fade.wav", xf)
        ctll.append(close_measure("0 CAST", Ca["sp"], Ca["x"], Ca["calls"], 0.0))
        for M in ctll:
            M["why"] = close_why(M, None); close_line(M)
        for (name, _sp, blurb) in CLOSE_CANDIDATES:
            print(f"    {name:<11} {blurb}")
        print("    0 FADE      the hum held 0.1 s and then faded 40 dB over 0.2 s -- a control on 'cutting out'\n"
              "    0 CAST      the cast itself -- a control on 'the hum' (it cracks first)")
        _show(rows_l, ctll, CLOSE_RULE, "close")
        ok, fb = _gate(rows_l, "close")
        li = fb if ok is None else min(ok, key=lambda i: (round(max(rows_l[i]["regs"].values()) / 0.05),
                                                          rows_l[i]["calls"], i))
        Cl = rows_l[li]
        print(f"  PICK  {Cl['name']}  h {Cl['h']}; cut {Cl['cut']:.0f} ms, prefade {Cl['pre']:+.1f} dB; "
              f"{Cl['lvl']:+.1f} dB re the cast's hum")

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        hum_what = {("triangle", 261.6256): "a C4 triangle hum (261.63 Hz)",
                    ("square", 329.6276): "an E4 square hum (329.63 Hz, hollow)",
                    ("sawtooth", 220.0): "an A3 sawtooth hum (220 Hz, an electric buzz)",
                    ("sine", 659.2551): "the glass's own hum (E5, 659.26 Hz, and a partner 4 Hz sharp)"}
        c_what = hum_what[(Ca["sp"]["ty"], Ca["sp"]["tones"][0][0])] + (
            " swelling in from 12 dB under" if Ca["sp"]["entry"] == "swell" else " coming in at level")
        s_what = {"stretch": "The school's snap itself, lengthened: its own three lines with every length x "
                             f"{St['D']:g}.",
                  "ring": "The school's snap (played as itself), and its ping rung on: a 2500 Hz triangle -- where "
                          "the ping lands -- dying over the stun.",
                  "body": "The school's snap (played as itself), and its 1.3 kHz body rung on: a narrow noise band "
                          "dying over the stun.",
                  "sizzle": "The school's snap (played as itself), its 2.6 kHz band re-struck every ~15 ms "
                            "(+/-20%) and its ping rung on under it at the snap's own proportions, held through the "
                            "stun and falling 20 dB at its end.",
                  "rattle": "The school's snap (played as itself), and its band re-struck: 2600 Hz pings ~28 ms "
                            "apart dying over the stun, a jammed catch.",
                  "echo": "The school's snap (played as itself), and re-struck: its own three lines again every "
                          "~10 ms (+/-20%) at its own proportions, held through the stun and falling 20 dB at its end -- the "
                          "snap going on for as long as the weapon is stopped."}[
            St["sp"]["kind"]]
        l_what = {"cut": "the cast's hum held 0.2 s, and its strikes simply stop -- it dies with the last one's "
                         "30 ms ring.",
                  "sag": "the cast's hum held 0.2 s, sagging a fourth over its last 60 ms, and stopping.",
                  "stutter": "the cast's hum, dropping out once and catching, and stopping.",
                  "click": "the cast's hum held 0.2 s and stopping on a relay's click."}[Cl["sp"]["kind"]]
        n_names = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                   "twelve", "thirteen", "fourteen", "fifteen"]
        nrc = len(fall_ids) - 1
        info = dict(
            n_cast=len(CAST_CANDIDATES), n_stun=len(STUN_CANDIDATES), n_close=len(CLOSE_CANDIDATES),
            n_rc=n_names[nrc] if nrc <= 15 else str(nrc),
            c_peers="".join(f", and {n_}'s cast and close" for n_ in peer_names),
            c_tonal=Ca["g_tonal"], c_inh_c=Ca["g_inh_c"], c_what=c_what, c_held=Ca["h_held"], c_hum_db=Ca["h_db"],
            c_aud=Ca["aud"], c_db=db(Ca["top"] / h_lo), c_heard=Ca["heard"], c_hheard=Ca["h_heard"],
            c_reg=max(Ca["regs"].values()),
            s_what=s_what, s_snap=St["snap_reg"], s_pk=St["snap_pk"],
            s_tail=St["tail_reg"], s_tdb=St["tail_db"], s_aud=St["aud_hi"], s_gone=St["gone_hi"],
            s_heard=St["t_heard"], s_reg=max(St["regs"].values()),
            l_what=l_what, l_note=Cl["note"], l_hreg=Cl["h_reg"], l_lvl=Cl["lvl"], l_cut=Cl["cut"],
            l_pre=Cl["pre"], l_aud=Cl["aud"])
        arms = arms_code(Ca, St, Cl, info)
        _refuse(arms, "Sfx row")
        if not arms.isascii():
            raise SystemExit("the Sfx row is not ASCII")
        if SFX_ANCHOR in arms or not arms.endswith("\n"):
            raise SystemExit("the Sfx row must sit before its anchor without repeating it")
        sfx_rows = [as_replace(SFX_ANCHOR, "before", arms)]
        print("\nTHE SFX ROW (mode `before` the rune-crack fallback), applied to Sfx.prototype.play's own source and "
              "rendered:")
        NEWP = [("cast", {"w": ME}, cast_body(Ca["sp"], Ca["g"], Ca["kh"], Ca["S1"])),
                ("stun", {"w": ME + "-stun"}, stun_body(St["sp"], St["kt"], St["D"], Ca)),
                ("close", {"w": ME + "-close"}, close_body(Ca, Cl["sp"], Cl["h"]))]
        chk = []
        for sd in (None, NOISE_SEEDS[3]):
            dr = "" if sd is None else " draw"
            for lab_, p_, body in NEWP:
                x1, _ = R([["arm", T0, "ult", p_]], rows=sfx_rows, seed=sd)
                x2, _ = R([["body", T0, body, {}]], seed=sd)
                chk.append((lab_ + dr, float(np.abs(x1 - x2).max())))
                if lab_ == "cast" and sd is None:
                    xa0 = x1
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, BLADE, 12.5, 18, 50) for c_ in (False, True)]
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
              f"hex-snap, fork, vine x4, loose x3, aegis x2, scour x4, {len(ult_ids)} ult ids -- every relic's cast, "
              f"every sub-voice the ult arm names and the bare fallback -- and every kind play() names): worst max "
              f"|diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa0 - rcx).max())
        fb_rc = float(np.abs(R([["arm", T0, "ult", {"w": FALLBACK}]], rows=sfx_rows, new=False)[0] - rcx).max())
        print(f"  ult/spellbreaker vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'};  ult/{FALLBACK} after the row: "
              f"{fb_rc:.0e} -- {'still rune-crack' if fb_rc <= 1e-6 else 'CHANGED'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or fb_rc > 1e-6 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40, ME])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, fallback=fb_rc, cost=cost, n_others=len(same_))

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
            mine = [("ult", {"w": ME}), ("ult", {"w": ME + "-stun"}), ("ult", {"w": ME + "-close"})]
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
                           for nm, X_ in (("cast", Ca), ("stun", St), ("close", Cl))}
            worst_p = max(((max(v.values()), k + "/" + max(v, key=v.get)) for k, v in prg.items()),
                          default=(0.0, "-"))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders "
                  f"render every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e}); "
                  f"register of the three against its voices at most {worst_p[0]:.2f} ({worst_p[1]}) -- printed")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine, regs=prg))
        rec["peers"] = peers

        # ---- THE tickStatus AND tickUnmake ROWS -------------------------------
        srows = {"status": [as_replace(STUN_ANCHOR, "after", STUN_CODE)],
                 "unmake": [as_replace(CLOSE_ANCHOR, "before", CLOSE_CODE)]}
        srows_bad = {"status": [as_replace(STUN_ANCHOR, "after", STUN_CODE_BAD)], "unmake": srows["unmake"]}
        seeds = [a.seed0 + k for k in range(a.seeds)]
        WR = None
        if not a.no_wire:
            print("\nTHE tickStatus AND tickUnmake ROWS, applied to the prototypes' own sources, run beside the "
                  "originals on real fights:")
            WR = page.evaluate(WIRE_JS, [seeds, srows, ME, REASON])
            assert not errors, errors[:3]
            if "err" in WR:
                raise SystemExit(WR["err"])
            print(f"  {WR['fights']} fights (Spellbreaker both sides x every foe x seeds {seeds}): {WR['same']}/"
                  f"{WR['fights']} identical (over, clock, both fighters' hp, positions, velocities, charges, facing, "
                  f"stun, hex clock, hexStunMul, hex stacks, winner, both unmakeTallies, and a digest of every "
                  f"step); every other SFX call identical in order and opts in {WR['otherSame']}/{WR['fights']}")
            print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices ({WR['unticked']} cast "
                  f"on a fight's last step, never ticked); hex procs: {WR['x2']} lengthened (x2, all on the foe) -> "
                  f"{WR['stunV']} stun voices; silent: {WR['x1foe']} x1 procs on the foe, {WR['me']} on "
                  f"Spellbreaker, {WR['shade']} on shades; stun voices a clock window: median {WR['perWinMed']} "
                  f"(min {WR['perWinMin']}, max {WR['perWinMax']}); {WR['closes']} closes; problems {WR['nbad']}")
            for b_ in WR["bad"]:
                print(f"    {b_}")
            if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                    or WR["closes"] != WR["ends"]["clock"] or WR["stunV"] != WR["x2"] or WR["castV"] != WR["casts"] \
                    or WR["stunV"] == 0 or WR["closes"] == 0 or WR["x1foe"] == 0:
                FAILED.append("tickStatus / tickUnmake rows")
            WB = page.evaluate(WIRE_JS, [seeds, srows_bad, ME, REASON])
            assert not errors, errors[:3]
            print(f"  the control (the rows plus one sim write, the stunned fighter nudged 1e-9 on a stun voice): "
                  f"{WB['same']}/{WB['fights']} identical -- "
                  f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
            if WB["same"] == WB["fights"]:
                FAILED.append("identity control")
            rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "ends", "casts", "castV", "unticked",
                                              "x2", "x1foe", "me", "shade", "stunV", "closes", "perWinMed",
                                              "perWinMin", "perWinMax", "nbad")}
            rec["wire"]["control_same"] = WB["same"]

            # ---- THE PICKS IN A REAL WINDOW ---------------------------------
            # v107's round-4c reading (aureole_voice_lab's, as a method): per event,
            # the third-octave (200 Hz-12 kHz) in which the voice stands highest over
            # everything else in THIS window (the score and the fight). The cast's
            # crack over its first 100 ms and its hum over 120-220 ms; each stun
            # over its tail, 100-300 ms after its snap; the close over its held
            # 100 ms. Gates: the crack, the close and the stuns' median >= +3 dB
            # (the hum printed). Two controls that can come back wrong: AFTER (the
            # same reading 0.8 s after the close, no new voice sounding: NOT
            # heard) and LEVEL (every event heard at >= +3 dB reads LOWER with its
            # voice 20 dB under).
            cand = sorted(WR["pick"], key=lambda w: (-w["stuns"], w["foe"], w["seed"]))
            if cand:
                w_ = cand[len(cand) // 4]
                EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], srows, ME])
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
                BURY = 0.1
                bury_body = {ME: cast_body(Ca["sp"], round(Ca["g"] * BURY, 6), Ca["kh"], Ca["S1"]),
                             ME + "-stun": (stun_body(St["sp"], St["kt"] * BURY, St["D"], Ca)
                                            .replace('this.play("hex-snap", {});',
                                                     'this._burst(t, { freq: 2600, q: 1.2, gain: 0.038, dur: 0.022, type:"bandpass" });\n'
                                                     'this._burst(t, { freq: 1300, q: 1.0, gain: 0.015, dur: 0.030, type:"bandpass" });\n'
                                                     'this._tone (t, { freq: 3100, to: 2500, gain: 0.0138, dur: 0.045, type:"triangle" });')
                                            if St["sp"]["kind"] != "stretch" else
                                            stun_body(St["sp"], 0, St["D"]).replace("gain: 0.38", "gain: 0.038")
                                            .replace("gain: 0.15", "gain: 0.015").replace("gain: 0.138", "gain: 0.0138")),
                             ME + "-close": close_body(Ca, Cl["sp"], round(Cl["h"] * BURY, 6))}
                RWB = [fc_ for fc_ in BANDS if PHONE_HZ <= fc_ <= 12000.0]

                def over_at(xa, xb_, fc_, t_, w_):
                    return db(band_rms(xa, fc_, t_, t_ + w_) / max(band_rms(xb_, fc_, t_, t_ + w_), 1e-12))

                def best_band(xa, xb_, t_, w_):
                    return max((over_at(xa, xb_, fc_, t_, w_), fc_) for fc_ in RWB)
                READ = {ME: [(0.0, 0.1), (0.12, 0.1)], ME + "-stun": [(0.1, 0.2)], ME + "-close": [(HELD_C[0], 0.1)]}
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
                        t_after = T0 + (c1t - lo_t) + 0.8
                        ta = [t_after + 0.05 * i_ for i_ in range(min(len(ts), 12))
                              if t_after + 0.05 * i_ + win_ <= T0 + (hi_t - lo_t)]
                        res_a[(tag, j_)] = [best_band(xw, xo, t_, win_)[0] for t_ in ta]
                        res_b[(tag, j_)] = [best_band(xb, xo, t_, win_)[0] for t_ in ts]
                        level_ok[(tag, j_)] = all(b_ < v_ for v_, b_ in zip(res[(tag, j_)], res_b[(tag, j_)])
                                                  if v_ >= 3)
                GATED = {(ME, 0): "min", (ME + "-stun", 0): "median", (ME + "-close", 0): "min"}

                def gate_of(r, key):
                    if not r.get(key):
                        return None
                    v = r[key]
                    return (min(v) if GATED[key] == "min" else float(np.median(v))) >= 3
                G4 = {k: gate_of(res, k) for k in GATED}
                GA = {k: gate_of(res_a, k) for k in GATED}
                print(f"\nIN A REAL WINDOW -- spellbreaker v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast "
                      f"at {c0t:.2f}s, closed by its clock at {c1t:.2f}s, {w_['stuns']} stun voices; the fight's own "
                      f"sounds and the score, with and without each new voice. Each event read in the third-octave "
                      f"(200 Hz-12 kHz) where it stands highest over everything else (v107's round 4c; the band "
                      f"after the @). Gates: the crack and the close >= +3 dB, the stun tails' median >= +3 dB; the "
                      f"hum printed. Controls: AFTER (0.8 s after the close, no new voice: must read NOT heard) and "
                      f"LEVEL (each voice 20 dB under: every event heard at >= +3 must read lower)")

                def fmt_v(v):
                    return " ".join(f"{x_:+.1f}" for x_ in v) + (f" (median {np.median(v):+.1f})" if len(v) > 1 else "")

                def ok_(g_):
                    return "absent" if g_ is None else ("heard" if g_ else "NOT heard")
                for key, nm in (((ME, 0), "the cast's crack (0-100 ms)"), ((ME, 1), "the cast's hum (120-220 ms)"),
                                ((ME + "-stun", 0), "each stun's tail (100-300 ms)"),
                                ((ME + "-close", 0), "the close's held hum")):
                    if not res.get(key):
                        print(f"  {nm}: none in this window")
                        continue
                    vals = res[key]; at_ = res[key + ("@",)]
                    shown = " ".join(f"{x_:+.1f}@{f_:.0f}" for x_, f_ in list(zip(vals, at_))[:24]) + \
                        (" ..." if len(vals) > 24 else "")
                    print(f"  {nm}: {shown}" + (f" (median {np.median(vals):+.1f})" if len(vals) > 1 else "") +
                          (f" dB -- {ok_(G4[key])}" if key in G4 else " dB (printed)"))
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
                if not all(level_ok.get(k, True) for k in GATED):
                    print("  the LEVEL control: the reading does not follow a voice's level")
                    FAILED.append("real-window control (level)")
                else:
                    print("  the LEVEL control: every event heard at >= +3 dB reads lower with its voice 20 dB under, "
                          "as it must")
                wav("spellbreaker-pick-real-window.wav", xw)
                xo_all = R([e_ for e_, e in zip(allv, evs) if not e[3]], secs=secs, rows=sfx_rows, new=False)[0] + bd
                wav("spellbreaker-pick-real-window-without.wav", xo_all)
                rec["real"] = dict(win=w_, over={str(k): v for k, v in res.items()},
                                   buried={str(k): v for k, v in res_b.items()},
                                   after={str(k): v for k, v in res_a.items()},
                                   level_ok={str(k): v for k, v in level_ok.items()},
                                   gates={"round4c": {str(k): v for k, v in G4.items()},
                                          "after": {str(k): v for k, v in GA.items()}})
            else:
                print("\nIN A REAL WINDOW -- no clock close in the wire runs")
                FAILED.append("no real window")
        # the picks in order, for the ear: the cast, stuns among blows, the close, a blow
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, t_ in enumerate((0.55, 1.0, 1.47, 1.95, 2.4)):
            seq += [["arm", T0 + t_, "ult", {"w": ME + "-stun"}]]
            seq += [["arm", T0 + t_ + 0.21, "hit", {"dmg": BLADE, "crit": False}]]
        seq += [["arm", T0 + 3.1, "ult", {"w": ME + "-close"}], ["arm", T0 + 3.6, "hit", {"dmg": BLADE, "crit": False}]]
        wav("spellbreaker-pick-sequence.wav", R(seq, secs=5.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0 and not a.no_wire:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds, ME, REASON])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: Spellbreaker's cast, stun and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="before", code=arms),
            dict(label="tickStatus: the stun voice, on a hex proc the Unmaking lengthened (hexStunMul > 1)",
                 anchor=STUN_ANCHOR, mode="after", code=STUN_CODE),
            dict(label="tickUnmake: the close, on a clock close with both alive, before the close line",
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
            for lab_, p, body in NEWP:
                x1 = R2([["play", T0, "ult", p]], seed=NOISE_SEEDS[5])
                x2 = R2([["body", T0, body, {}]], seed=NOISE_SEEDS[5])
                nd.append((lab_, float(np.abs(x1 - x2).max())))
            rcp = R2([["play", T0, "ult", {"w": FALLBACK}]])
            not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
            F1 = page.evaluate(FIGHTS_JS, [e2e_seeds, ME, REASON])
            assert not errors, errors[:3]
            if isinstance(F1, dict):
                raise SystemExit(F1["err"])
            page_err = len(errors)
        F0 = {f_["key"]: f_ for f_ in ref_fights}
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1)
        s_ok = sum(f_["stunV"] == f_["x2"] and f_["badStun"] == 0 for f_ in F1)
        l_ok = sum(f_["closeV"] == f_["clock"] for f_ in F1)
        w_ok = sum(f_["stray"] == 0 for f_ in F1)
        orig_new = sum(f_["stunV"] + f_["closeV"] for f_ in ref_fights)
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "x2", "clock", "castV", "stunV", "closeV")}
        print(f"  the three new voices through the patched page's own SFX.play vs the lab's candidate text in that "
              f"page, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/spellbreaker vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's (a digest of every step "
              f"included), every other SFX call identical in {osame}/{len(F1)}; per fight -- cast voices = casts "
              f"{c_ok}, stun voices = lengthened procs {s_ok}, closes = clock closes {l_ok}, every voice where it "
              f"belongs {w_ok} (of {len(F1)}); totals {tot}; the original page played {orig_new} of them; page "
              f"errors {page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1)
                   or osame != len(F1) or min(c_ok, s_ok, l_ok, w_ok) != len(F1) or orig_new or page_err
                   or tot["stunV"] == 0 or tot["closeV"] == 0)
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same, other_same=osame, totals=tot,
                    page_errors=page_err)

    if a.e2e_seeds > 0 and not a.no_wire:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="spellbreaker_e2e_"))
        try:
            tp = tmpd / "sc-spellbreaker-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the three rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    # ---- ALSO: the rows on another link carrying Spellbreaker's stage 5 -------
    rec["also"] = []
    for spec in ([] if a.no_wire else a.also):
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
            W2 = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape])")
            u2 = sorted(set(re.findall(r'w === "([a-z-]+)"', ps2)) | set(ids2) | {FALLBACK})
            k2 = sorted(set(re.findall(r'kind === "([a-z-]+)"', ps2)) - {"ult", "hit"})
            voices2 = [v_ for v_ in e2e_voices if v_[0] != "ult" or v_[1]["w"] in u2]
            voices2 += [("ult", {"w": w_, "n": 2}) for w_ in u2
                        if w_ != ME and not w_.startswith(ME + "-") and ("ult", {"w": w_, "n": 2}) not in voices2]
            voices2 += [(k_, {}) for k_ in k2 if (k_, {}) not in voices2]
            ref_v = [R3([["play", T0, k, p]]) for k, p in voices2]
            ref_f = page.evaluate(FIGHTS_JS, [e2e_seeds, ME, REASON])
            assert not errors, errors[:3]
        for pid, why_ in PEER_TYPE.items():
            got = [w_ for w_ in W2 if w_[0] == pid]
            print(f"  {pid} on {ap_.name}: {got[0][1:] if got else 'absent'} -- declared {why_}")
            if got and got[0][2] != TYPE_SHAPE:
                FAILED.append(f"{pid} is not a {TYPE_SHAPE}")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="spellbreaker_also_"))
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
        return [{k: v for k, v in M.items() if k not in ("x", "bands", "DB", "h_bands", "sp")} | {"sp": M.get("sp")}
                for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), stun=strip(rows_s), stun_controls=strip(ctls),
               close=strip(rows_l), close_controls=strip(ctll), wavs=sizes,
               pick={"cast": Ca["name"], "cast_g": Ca["g"], "cast_kh": Ca["kh"], "cast_S1": Ca["S1"],
                     "stun": St["name"], "stun_kt": St["kt"], "stun_D": St["D"], "close": Cl["name"],
                     "close_h": Cl["h"]})
    print(f"\nTHE PICKS  cast {Ca['name']}   stun {St['name']}   close {Cl['name']}")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    al = "".join(f"; the same stage 5 carried onto another tip ({X['game']} {X['sha']}): {X['same']}/{X['fights']}"
                 for X in rec["also"])
    wr = rec.get("wire")
    rows[0]["why"] = (
        f"The three voices of v79 s4, in the synth only. The arms go BEFORE the shared rune-crack fallback (mode "
        f"`before`, its anchor the fallback line itself), so the {len(rec['fallthrough']) - 1} other relics that "
        f"still fall through keep it and another relic's row anchored there applies in either order. Through the "
        f"patched play() every arm reproduces its lab candidate (worst "
        f"{max(v for _, v in rec['arm_check']['chk']):.0e}, on two noise draws), "
        f"{rec['arm_check']['n_others']} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), ult/spellbreaker is no longer rune-crack and the "
        f"bare fallback still is. play() returns on its first line with no audio context (every headless run), "
        f"draws no random number and writes nothing the simulation reads"
        + (f"; end to end the three voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    if wr:
        rows[1]["why"] = (
            f"After the hex proc's breakSpin call (kept unchanged): one guarded SFX.play reading only "
            f"f.hexStunMul, the factor the sim's own two lines above read. {wr['stunV']}/{wr['x2']} lengthened "
            f"procs voiced, none of the {wr['x1foe']} x1 procs on the foe, {wr['me']} on Spellbreaker or "
            f"{wr['shade']} on shades; {wr['same']}/{wr['fights']} fights identical (a digest of every step "
            f"included) and every other SFX call identical in order and opts; the rows plus one sim write come back "
            f"{wr['control_same']}/{wr['fights']}{e2}{al}. Writes nothing; no field for the probe's allowed set.")
        rows[2]["why"] = (
            f"One guarded SFX.play before the window's own close line (kept unchanged), reading only Z.t, Z.dur and "
            f"the two alive flags: a clock close with both alive. {wr['closes']} closes for {wr['ends']['clock']} "
            f"clock closes, none on the {wr['ends']['caster'] + wr['ends']['foe']} closes a death made or the "
            f"{wr['ends']['over']} windows the fight's end cut off; nothing is read back{e2}.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist")
                                                   else float(o)), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The three rows are the edits; all three were applied "
          "to the page's own code above" + ("" if a.no_wire else ", and as text to a copy of the page") + ".")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
