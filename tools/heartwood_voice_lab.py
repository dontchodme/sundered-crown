#!/usr/bin/env python3
"""ROOTFAST'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v112 stage 6.

    python heartwood_voice_lab.py --game <sc-heartwood-b11.html> --rows rows.json

v85 section 4, SOUND, every word of it: "cast -- a green creak, 0.4s; a root --
a short creak-and-crack (Tendril's root voice, reused, quieter at 1.0s than at
the vine's longer holds); close -- nothing." Rick, for the batch's art and
sound: "you pick i overrule". So this lab renders five or six candidates a
voice beside CONTROLS that can come back wrong, prints the numbers each pick is
made on, and PICKS by a rule written in this file (`*_RULE`). He overrules from
one clip.

THE EVENTS AND WHERE THEY FIRE (line numbers are sc-heartwood-b11's):
  cast    the bare id `ult/heartwood`, which `fireUlt` already plays for every
          relic (16270). Heartwood has NO arm on this base: it falls through to
          the shared rune-crack (so do eleven others -- measured below, to
          1e-6). The arm goes BEFORE that fallback; the fallback line is
          re-emitted unchanged. No new call.
  root    `ult/heartwood-root`, ONE plain SFX.play in `rootBlow` (13661) on the
          line after `T.rooted++;` (13670): every blow that roots -- a new hold
          or a re-root of a ball already held, both of which the sim counts in
          `rooted` and both of which the design's "every blow roots" names.
          A killing blow returns above (`if (!q.alive) return;`) and roots
          nobody, so it plays nothing (the death voice has that frame). The
          blow's own `hit` voice plays later on the SAME frame (resolveHit's
          last lines, 15152), so the two are measured TOGETHER below.
  close   nothing (the design). Measured: no voice from `tickRootfast`.

TENDRIL'S ROOT VOICE DOES NOT EXIST ON THIS BASE. The design reuses it; it is
Bindweed's stage 6 (`bindweed-root`, `bindweed_voice_lab.py` DEEP), on
`sc-tendril-fx` and later, and this base (sc-tendril-t3 -> sc-heartwood-b11)
has no such arm: `ult/bindweed-root` here IS rune-crack. So this lab MAKES
Heartwood's own arm, `heartwood-root`, as THE SAME VOICE: Tendril's arm body
read from `--tendril` (02-chain/sc-tendril-fx.html) and checked equal, line
for line, to `bindweed_voice_lab.root_body(DEEP)`, with ONE constant changed --
its gain `g` -- and nothing else. It is its own id so the row applies to this
base AND to a later tip that carries Tendril's arm, without the two touching.

THE DECLARED READINGS (words of v85 section 4 turned into numbers):
  * "A ROOT" is every rooted blow (`T.rooted`), not only a new hold
    (`T.roots`): the design's every-blow-roots, and the lab's own "roots a
    cast" (v112 section 6: the lab counted rooted blows, transitions were
    fewer). Printed beside it: the new holds.
  * "SHORT CREAK-AND-CRACK" is the reused voice's own length (Tendril's
    "0.35s", audible ~370 ms): reused means the same voice, not a shortened
    one. The rule checks the reuse kept its shape (a creak into a crack).
  * "QUIETER AT 1.0s THAN AT THE VINE'S LONGER HOLDS": the vine roots for
    rootPer 0.3 x the foe's entangle stacks (cap 4), 1.2 s at the cap where 82%
    of its bites land, and its voice has ONE level for every hold; Rootfast
    holds 1.0 s. Read as: Tendril's voice at a lower gain, its loudest draw at
    least 3 dB under Tendril's quietest. The design says quieter, not by how
    much: 3 dB is THIS LAB'S number for a step heard as quieter side by side,
    and the hold ratio's literal 20 log(1.0 / 1.2) = -1.6 dB is printed, not
    taken.
    The candidates are a LADDER of gains (the reuse leaves nothing else to
    choose); the pick is the LOUDEST that passes every gate -- the reused
    voice changed as little as the design's "quieter" and the relic's own
    blow allow.
  * THE BLOW IS THE BLOW: the root lands on the frame of the blow that made
    it, with the blow's own voice. It is never over Heartwood's blow (TOP <=
    the hit @ 11's quietest draw: the ceiling Canopy's cast and Tendril's root
    took, at the blade); and at the blows it really lands with -- the
    lightest, the median and the heaviest plain blow and the heaviest crit a
    root voice landed with in the wire run (the chaos jitter, the foe's
    damage-taken and the crit's x2.1 put them far from 11) -- the blow keeps
    its own third-octave >= 6 dB over the root alone, and the root keeps its
    own third-octave >= 6 dB over the blow alone, its crack standing clear
    after it (the crack lands 0.2 s in, when the blow has died).
  * "A GREEN CREAK": a CREAK is the house's (ironwood_voice_lab,
    bindweed_voice_lab): a train of pulses at a creak's rate (stick-slip) --
    RATE 17-83 a second and PULSED >= 0.40 -- never a held tone. GREEN is
    living wood, read against the house's DRY creak (Canopy's wither, "a dry
    creak falling in pitch", `ult/ironwood-wither`): the green creak's NOTE
    sits under the lowest note the dry creak reaches (its last 100 audible
    ms, 420 Hz: lower than the dry creak everywhere it goes), and it does not
    wither (SHIFT >= -200 cents: its last 100 audible ms do not sit more than
    200 cents under its first 100). A CREAK, NOT THE ROOT'S CRACK: the root
    is the creak-AND-crack, so the cast carries no crack: its loudest
    high-passed millisecond does not stand ALONE (< 10 dB over every other
    one 20 ms or more away; the root's crack stands 29 dB). "0.4s": AUDIBLE
    330-470 ms, GONE <= 470 ms (the band Tendril's wither took for its
    "0.4s").
  * THE CAST'S LEVEL: once a window, on the cast frame -- "heard like a blow,
    never over one" (Canopy's and Tendril's casts): TOP between 0.5x the hit
    @ 11's loudest 50 ms on its loudest draw and 1.0x on its quietest.
  * THE CASTS' OWN CONSTRUCTIONS (candidates, not readings): every pulse is
    pure arithmetic, each interval x (1 + 0.12 sin 2.4k) so the train is
    irregular with no random number (the house's creak). No `_tone` here is
    a held note except the HELD control's.

THE CONTROLS, and what each one is for:
  rune-crack   what Heartwood's cast plays TODAY; v88 published 0.608 / 450 ms
               -- reproduced before anything new is quoted (with BAR 0.364 /
               300 ms and hit@11.6 0.443 / 80 ms)
  hit@11       Heartwood's own blow (blade 11), on its quietest / loudest noise
               draw: the level every voice is judged against, and the blow the
               root lands with
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   the verdant casts with a voice of their own on this base, and
               Tendril's cast read from `--tendril`: the cast must not be them
  the type     the greatsword row's casts with a voice of their own
  DRY          Canopy's wither, the house's dry creak: as a cast it must fail
               GREEN (the reference GREEN is read against)
  CRACK        Tendril's root itself (a creak INTO a crack): as a cast it must
               fail on its crack
  HELD         KNOT's 380 Hz sine held by re-striking at its own cycles, no
               stick-slip: as a cast it must fail CREAK
  WITHER       KNOT falling 450 -> 250 Hz: as a cast it must fail GREEN
  FULL         Tendril's root at its own gain: as the root it must fail QUIETER
  FAINT        Tendril's root 24 dB down: as the root it must fail HEARD
  PARADOX-PIN  the game's other hold-landing voice: as the root it must fail
               REUSED
  BACK         Tendril's root with the crack BEFORE the creak: as the root it
               must fail REUSED
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` (bus 0.42, a compressor, the
    makeup gain) in an OfflineAudioContext at 48 kHz, the first event at t =
    1.0, on a synth built the way render.py builds one (`Object.create` of the
    Sfx prototype, render.py's xorshift noise): ironwood_voice_lab's
    RENDER_JS, imported unchanged. The chain COMPRESSES, so a gain ladder is
    not a dB ladder: every level here is measured after the chain. Noise-built
    sounds are judged on the worst of twelve draws. Nothing may sound before t
    = 1.0; a silent render stops the run.
  * A CANDIDATE IS ITS ARM'S OWN TEXT, constants rounded first, rendered by
    evaluating that text on the synth; the row is then applied to
    `Sfx.prototype.play`'s own source and rendered again, and must match to
    1e-6.
  * The shared measures are imported unchanged: zenith_voice_lab's E50, TOP,
    START, AUDIBLE, GONE, REG (cosine of 1/3-octave band amplitudes, 25 Hz-16
    kHz, the median over noise draws), IN-BAND, ENV-CORR; ironwood_voice_lab's
    LOW (share below 120 Hz) and CENTROID; bindweed_voice_lab's RATE (the
    envelope's own modulation frequency), PULSED / DEPTH (100 ms windows), HF
    CRACK (the loudest 1.5 kHz-high-passed millisecond, its time, STAND over
    the p90 before it and JUMP over 2 ms before it) and OWN BAND (the
    third-octave a voice is loudest in).
  * New here, each with a control that can come back wrong:
      NOTE    zenith_voice_lab's PITCH (FFT peak, Hann, zero-padded,
              parabolic), 60-2000 Hz, over the audible span, and over the last
              100 audible ms (the dry creak: 534 Hz, down to 420 Hz)
      SHIFT   cents that the last 100 audible ms sit from the first 100: the
              lag (12.5 c steps, parabolic) that best correlates the two
              windows' log power spectra, 60 Hz-4 kHz, each point the mean in a
              1/12-octave window on a 1/96-octave grid (ironwood_voice_lab's
              CRACK, run between two windows of one voice). A steady creak
              reads ~0 at any note; WITHER must read its fall
      ALONE   the loudest millisecond of the voice high-passed at 1.5 kHz
              (bindweed_voice_lab's HF envelope) over the loudest millisecond
              20 ms or more away from it, dB. Tendril's root +29.4, the dry
              creak +2.3, a creak's click train 0-2
      REUSED  REG against Tendril's root (draw for draw) and ENV-CORR against
              it (render.py's draw): both >= 0.95
      ON ONE FRAME   the root and a blow rendered together, at each blow the
              wire run heard (above): KEEP-ROOT = the mix over the blow alone
              in the root's own third-octave over 0.35 s; KEEP-BLOW = the mix
              over the root alone in the blow's own third-octave over 0.15 s;
              STAND-MIX = the root's crack millisecond in the MIX over the p90
              of the mix's HF envelope 60-10 ms before it
      Printed, not gated: the power centroid (CEN), NOTE-FALL (cents from
      PITCH over the first 100 audible ms to the last 100) and the first cut's
      FALL-C (the same from CENTROID 60 Hz-4 kHz).

WHAT THE FIRST CUT GOT WRONG -- recorded, not hidden. The rules were written
before the first table (run on one fight seed); that table showed an instrument
blind to what it was built to see, a second instrument reading a steady creak
as falling, and a reading of "green" (this lab's own octave) that all but one
of 33 constructions could meet only inside the verdant school's own register.
Each was changed ONCE, for the reason given, before the picks:
  * NOT A CRACK was first "the root's crack test (STAND >= 10 dB and JUMP >=
    10 dB) must fail", and every creak PASSED it (STAND +12..+21 dB): a click
    train's 1 ms HF envelope is mostly gap, so the p90 before the loudest
    click is the gap, not the other clicks. ALONE compares the loudest
    millisecond with the loudest OTHER one: the creaks read 0-2 dB, Tendril's
    root +29.4 (the CRACK control, which must fail it, does).
  * "DOES NOT WITHER" was first FALL-C (the CENTROID's fall), which read the
    steady 130 Hz GROAN as falling -181 c and a steady 110 Hz triangle -443 c
    (the pulses' clicks brighten the head) against -389 c for a creak that
    really fell 180 -> 100 Hz: it cannot tell a steady creak from a withering
    one. The first replacement tried, NOTE-FALL (PITCH's fall), smears below
    ~200 Hz (a 35 ms pulse holds a few cycles: the steady 130 Hz GROAN -338 c,
    a steady 90 Hz groan -608 c). SHIFT compares the two windows' whole
    spectra instead; both others are printed.
  * GREEN was first "the power centroid <= 0.5x the dry creak's (an octave
    under it)". Of the constructions tried under the octave (33 of them,
    90-290 Hz: sine, timber, triangle, sawtooth, square, friction grains, a
    wet give; stage6-voice/explore*.txt in the batch scratch), 32 put their
    energy where the verdant school's own casts and the blow live --
    Thornwake's creak-and-cinch 0.82-0.90, Vinesower 0.76-0.84, Paradox's pin
    0.83-0.84, the blow 0.78-0.92 -- and the one that cleared every register,
    a 90 Hz groan (DEEP, now a candidate), clears the death voice by 0.02.
    The octave was this lab's number, not the design's, and it asks more than
    "green" does: green wood is heavier and softer than seasoned wood, not a
    register apart. GREEN now reads the creak's NOTE against the whole range
    the dry creak covers -- under the lowest note it reaches -- which DEEP
    still passes, so the octave's one survivor stays in the race and the
    written tiebreak (the most distinct register) decides. GROAN, the first
    cut's pick, stays in the table as the evidence (it fails the register).
  * THE FRAME was first the hit @ 11 with and without a crit; the wire run
    showed the root voices landing with blows of 0-32 (median 16) and crits to
    66, so the frame checks run at the blows the run heard.

THE PICKS, on Chromium 151.0.7922.34, sc-heartwood-b11 aff84a04b303a402,
Tendril's voices read from sc-tendril-fx eea0cde5536955b3, fight seeds
112601-112602 (148 fights), end to end 112651 (74):

  cast    5 RISING  a sine climbing a fourth, 300 -> 400 Hz, over the first
          0.3 s (the greening runs hilt to tip in 0.3 s) and held, pulsed 28
          -> 40 a second, growing then settling. RATE 33 a second, PULSED
          0.65; NOTE 356 Hz, under the dry creak's lowest 420 (SHIFT +130 c:
          it grows); ALONE +0.3 dB (no crack); audible 390 ms; TOP -2.9 dB re
          the hit @ 11, +16.8 dB re the wall; register at most 0.75 (the dry
          creak). KNOT (0.73), TIMBER (0.74) and SAP (0.73) tie it to 0.05 and
          lose on calls (14, 28) or the order listed (SAP, 13); DEEP loses the
          register (0.78, the death voice); GROAN out (the blow, 0.84).
  root    3 G-7dB  Tendril's root body verbatim, g 0.5179 -> 0.2313: TOP
          0.0698, -4.1 dB re Tendril's (the chain compresses a 7 dB gain step
          to 4.1), -4.3 dB re the hit @ 11, +14.8 dB re the wall; REG 0.99 and
          ENV-CORR 0.99 against Tendril's; the crack at 206 ms standing +46.4
          dB; on the blow's frame (blows of 0, 16 and 32 and a crit of 66) the
          root keeps +6.9 dB in its 50 Hz third-octave, the blow +22.9 dB in
          its own, the crack +44.0 dB in the mix; register at most 0.46 (the
          cast). G-3dB and G-5dB out (-1.6 / -2.8 dB: not 3 dB quieter);
          G-9dB and G-11dB out (under the heaviest crit: +5.8 / +4.6 dB).
  close   nothing (the design): no voice from tickRootfast in 637 windows.

  In play (148 fights; 637 windows -- 557 closed by the clock, 17 by the
  caster's death, 63 by the fight's end): 637 casts and 637 cast voices; 2363
  blows in a window, 2318 rooted (1282 new holds, 1036 re-roots) and 2318 root
  voices, none on the 45 killing blows; 148/148 fights identical and every other
  SFX call identical in order and opts; the sim-write control 11/148. The root
  voices landed with blows of 0-32 (median 16) and crits to 66. In a real window
  (v Twinshade, 112602, 13 rooted blows) the cast stands +21.1 dB over
  everything else on its frame in its own third-octave (400 Hz) and the roots
  +10.9 dB (median) in theirs (50 Hz), five of the thirteen under +3 dB where the
  fight is loud. End to end: 74/74 fights identical to the unpatched page's with
  every voice count exact, and the two voices through the patched page's own
  SFX.play equal the candidates to 6e-8. Main-thread cost a call: cast 0.5 ms,
  root 0.7 ms (the hit's 0.1).

  Carried (in scratch, not a gate of this lab): heartwood_build.py's four
  stages onto sc-ironhail-fxout (39 relics, Tendril's voices on it) and the two
  rows applied unchanged: each anchor once, 76/76 fights identical to the
  carried link's, every voice count exact; there the tip's own
  ult/bindweed-root equals the body this row reuses (6e-8).

  Outside the rule's scope (printed for Rick, not gated -- the house's cast rule
  reads the school and the type): against every ult voice on that tip (101
  casts and sub-voices), RISING sits over 0.80 with five other relics' voices
  (Lastlight's cold 0.88, Cindercleave's jet 0.86, Foregone's reverse 0.81,
  Gravemourn's hand and Ironhail's cast 0.80); KNOT and SAP with three, TIMBER
  eight, DEEP thirteen (Threshmaw's cast 0.94), GROAN twenty-two. The reused
  root, Tendril's own voice, sits 0.81-0.83 against Twinshade's, Shroudmaul's,
  Grudgebearer's and Cindercleave's casts.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row is applied to `Sfx.prototype.play`'s own source and rendered:
    each arm must reproduce its candidate to 1e-6 (the root on two noise
    draws); every other voice through the patched play (the hit at five
    weights with and without a crit, spark x3, wall, death, clank, seal, nova,
    hex-snap, fork, vine x4, loose x3, aegis, the four scour voices, seven ult
    sub-voices -- `ult/bindweed-root`, rune-crack on this base, among them --
    and every other relic's cast) must be unchanged;
    `ult/heartwood` must NOT be rune-crack any more;
  * the rootBlow row is applied to the prototype's own source and run on real
    fights beside the unpatched one: every fight identical (over, clock, both
    hp, both positions and velocities, both pins, winner, the whole
    rootTally), every other SFX call identical in order and opts; one root
    voice per rooted blow, on its call, none on a killing blow, none outside a
    window; one cast voice per cast; no voice from `tickRootfast` (the close
    is silent). There is no mirror match: `Match` refuses a relic against
    itself (measured). The same row plus ONE sim write (the foe nudged 1e-9
    on a root) must come back NOT identical, or "identical" proves nothing.
    (The Sfx row cannot reach the simulation: `play` returns on its first
    line with no audio context, which is every headless run.)
  * END TO END: the rows applied AS TEXT to a copy of the game file (in a
    temporary folder, deleted after), loaded in a fresh browser once the first
    has closed (never two at once): the new voices through the patched page's
    own `SFX.play` equal the lab's candidate text rendered in that page; every
    other voice equals the unpatched page's; Heartwood's fights on both sides
    against every foe are identical to the unpatched page's, with the voice
    counts above.
  All anchors must occur exactly once in the game file, and every row's code
  re-emits its anchor exactly once (so a picture row on the same line composes
  in either order).

Writes wavs to 05-reference/v112/heartwood-*.wav at RAW level (gitignored).
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
# means in v98's, v99's and v101's labs. (The three modules' bodies only define
# things.)
from zenith_voice_lab import (  # noqa: E402
    BED_JS, NOISE_SEEDS, SR, T0, band_rms, bands, basic, cents, db, env_corr, fmt, pcm, pitch, write_wav,
    _comment)
from ironwood_voice_lab import RENDER_JS, centroid, low_share  # noqa: E402
from bindweed_voice_lab import (  # noqa: E402
    ROOT_CANDIDATES as TENDRIL_ROOTS, crack_info, hf_env, mod_rate, mreg, peak_band, pulsed_w,
    root_body as tendril_root_body)

HERE = pathlib.Path(__file__).parent
ME = "heartwood"
ROOT_ID = ME + "-root"
BLADE = 11.0                              # Heartwood's dmg (stage 5, b11)
ROOT_FOR = 1.0                            # w.ult.rootFor
VINE_HOLD_CAP = 0.3 * 4                   # Tendril: rootPer x the entangle cap
QUIETER_DB = 3.0                          # "quieter": Tendril's quietest draw less this
KEEP_DB = 6.0                             # the blow and the root each keep their own band
# the blows a root lands with: set from the wire run (the lightest, the median and
# the heaviest plain blow a root voice landed with, and the heaviest crit)
FRAME_BLOWS: list = []
SCHOOL = ["thornwake", "vinesower", "thornshear", "ironwood", "bindweed"]
TYPE = ["dawnbringer", "lightkeeper", "emberedge", "oathwound", "nightfell", "axiom"]
# Tendril's DEEP, as bindweed_voice_lab picked it (v101) and sc-tendril-fx ships it
T_SP = dict(TENDRIL_ROOTS[2][1])
T_G, T_KC, T_KT = 0.5179, 0.2683, 0.3464
ROOT_LADDER_DB = [3.0, 5.0, 7.0, 9.0, 11.0]


# =============================================================== THE CAST ===
# "a green creak, 0.4s". Every candidate is a stick-slip pulse train over 0.4 s;
# they differ in what a pulse IS, where it sits and how the train moves.
CAST_CANDIDATES = [
    ("1 GROAN", dict(pulse="timber", pitch="130", rate=(30, 42), env="swell"),
     "the FIRST CUT's green creak, kept as the evidence for the second: a timber (a 130 Hz sine and its 2.76 "
     "mode at 0.4) pulsed 30 -> 42 a second, swelling and settling"),
    ("2 DEEP", dict(pulse="sine", pitch="90", rate=(30, 42), env="swell"),
     "a 90 Hz sine groan pulsed 30 -> 42 a second, swelling and settling -- the one construction under the "
     "first cut's octave that clears every register"),
    ("3 KNOT", dict(pulse="sine", pitch="380", rate=(30, 42), env="swell"),
     "a 380 Hz sine pulsed 30 -> 42 a second, swelling and settling"),
    ("4 TIMBER", dict(pulse="timber2", pitch="360", rate=(30, 42), env="swell"),
     "a timber (a 360 Hz sine and its 2.76 mode at 0.2) pulsed 30 -> 42 a second, swelling and settling"),
    ("5 RISING", dict(pulse="sine", pitch="300 * Math.pow(4 / 3, Math.min(1, s / 0.3))", rate=(28, 40),
                      env="grow"),
     "a sine climbing a fourth, 300 -> 400 Hz, over the first 0.3 s (the greening runs hilt to tip in 0.3 s) "
     "and held, pulsed 28 -> 40 a second, growing then settling"),
    ("6 SAP", dict(pulse="sap", pitch="380", rate=(32, 32), env="swell"),
     "a 380 Hz sine, each pulse giving a minor third (a wet give), 32 a second"),
]
CPULSE = {
    "timber": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });',
               'this._tone(t + s, { freq: f * 2.76, gain: a * 0.4, dur: 0.025, type:"sine" });'],
    "timber2": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });',
                'this._tone(t + s, { freq: f * 2.76, gain: a * 0.2, dur: 0.025, type:"sine" });'],
    "sine": ['this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" });'],
    "sap": ['this._tone(t + s, { freq: f, to: f * 0.84, gain: a, dur: 0.035, type:"sine" });'],
}
CENV = {"swell": "(0.55 + 0.45 * Math.sin(Math.PI * u))",
        "grow": "(s < 0.3 ? 0.5 + 0.5 * s / 0.3 : 1 - 3 * (s - 0.3))"}


def cast_body(sp, g, ind=10):
    r0, r1 = sp["rate"]
    iv = (f"(1 / {r0})" if r0 == r1 else f"(1 / ({r0} * Math.pow({fmt(round(r1 / r0, 6))}, u)))")
    L = [f"const g = {fmt(g)};",
         "for (let s = 0, k = 0; s < 0.38; k++){",
         f"  const u = s / 0.4, f = {sp['pitch']}, a = g * {CENV[sp['env']]};",
         *["  " + l_ for l_ in CPULSE[sp["pulse"]]],
         f"  s += {iv} * (1 + 0.12 * Math.sin(k * 2.4));",
         "}"]
    return "\n".join(" " * ind + l_ for l_ in L)


def held_body(g, f=380, ind=10):
    """HELD: KNOT's sine held by re-striking at its own cycles (Zenith's and
    Tendril's technique, `.frequency.value = f` on every strike) -- a note, no
    stick-slip."""
    L = [f"const g = {fmt(g)}, f = {f};",
         "for (let s = 0; s < 0.38; s += 1 / f){",
         "  const u = s / 0.4, a = g * (0.55 + 0.45 * Math.sin(Math.PI * u));",
         '  this._tone(t + s, { freq: f, gain: a, dur: 0.035, type:"sine" }).frequency.value = f;',
         "}"]
    return "\n".join(" " * ind + l_ for l_ in L)


def alone(x, gap=20):
    """ALONE: the loudest millisecond of the voice high-passed at 1.5 kHz
    (bindweed_voice_lab's HF envelope) over the loudest millisecond at least
    `gap` ms from it, dB, and its time (ms after the event). A crack stands
    alone; a creak's clicks come as a train of near-equals."""
    import numpy as np
    e = hf_env(x)[:600]
    i = int(np.argmax(e))
    m = e.copy(); m[max(0, i - gap):i + gap + 1] = 0
    return db(float(e[i]) / max(float(m.max()), 1e-12)), float(i)


def note_info(x, a0_ms, gone_ms):
    """NOTE: PITCH (FFT peak, Hann, zero-padded, parabolic), 60-2000 Hz, over
    the audible span; NOTE-FALL: cents from PITCH over the first 100 audible ms
    to PITCH over the last 100; and that last PITCH."""
    g0 = T0 + a0_ms / 1000; g1 = T0 + gone_ms / 1000
    last = pitch(x, g1 - 0.1, g1, 60, 2000)
    return pitch(x, g0, g1, 60, 2000), cents(last, pitch(x, g0, g0 + 0.1, 60, 2000)), last


def shift(x, a0_ms, gone_ms, lo=60.0, hi=4000.0):
    """SHIFT: cents that the voice's last 100 audible ms sit from its first 100
    -- the lag (12.5 c steps, parabolic) that best correlates the two windows'
    log power spectra (Hann, zero-padded, each point the mean power in a
    1/12-octave window on a 1/96-octave grid, lo-hi). A steady creak reads ~0
    whatever its note; a creak that falls reads its fall."""
    import numpy as np
    NF = 1 << 16
    fr = np.fft.rfftfreq(NF, 1 / SR)
    grid = lo * 2 ** (np.arange(0, int(96 * math.log2(hi / lo)) + 1) / 96)
    l1 = np.searchsorted(fr, grid * 2 ** (-1 / 24)); h1 = np.searchsorted(fr, grid * 2 ** (1 / 24))

    def spec(a, b):
        seg = x[int(a * SR):int(b * SR)]
        P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NF)) ** 2
        cs = np.concatenate([[0.0], np.cumsum(P)])
        v = (cs[h1] - cs[l1]) / np.maximum(h1 - l1, 1)
        return 10 * np.log10(v + v.max() * 1e-6)
    g0 = T0 + a0_ms / 1000; g1 = T0 + gone_ms / 1000
    A, B = spec(g1 - 0.1, g1), spec(g0, g0 + 0.1)
    L = list(range(-128, 129))
    best = []
    for s_ in L:
        u, v = (A[:s_], B[-s_:]) if s_ < 0 else ((A[s_:], B[:-s_]) if s_ > 0 else (A, B))
        best.append(float(np.corrcoef(u, v)[0, 1]))
    i = int(np.argmax(best)); d = 0.0
    if 0 < i < len(best) - 1:
        y0, y1, y2 = best[i - 1], best[i], best[i + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if den else 0.0
    return (L[i] + d) * 12.5


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx|\.beat\(|hitStop", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


# =============================================================== THE ROOT ===
def tendril_arm(html, w):
    """Tendril's arm `w` on --tendril: (the whole arm block, its body -- the
    lines after its comment). Refuses an arm that is not there exactly once."""
    head = f'        }} else if (w === "{w}"){{'
    c = html.count(head)
    if c != 1:
        raise SystemExit(f"--tendril carries the arm {w!r} {c} times, not once -- it must be Bindweed's stage 6")
    i = html.index(head)
    j = html.index("\n        } else", i + len(head))
    block = html[i:j]
    k = block.index("*/") + 2
    return block, block[k:].lstrip("\n").rstrip()


def root_from_tendril(body, g):
    """THE REUSE: Tendril's own body with its gain constant changed, and nothing
    else."""
    old = f"const g = {fmt(T_G)}, "
    if body.count(old) != 1:
        raise SystemExit("Tendril's root body does not carry its gain exactly once")
    return body.replace(old, f"const g = {fmt(g)}, ", 1)


def back_body(g, ind=10):
    """BACK: Tendril's root with the crack first and the creak 0.1 s after it."""
    return tendril_root_body(T_SP, g, T_KC, T_KT, order="back", ind=ind)


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
ROOT_ANCHOR = '    T.rooted++;'

ROOT_CODE = ROOT_ANCHOR + '''
    /* ROOTFAST'S ROOT (v85 section 4: "a root -- a short creak-and-crack
       (Tendril's root voice, reused, quieter at 1.0s than at the vine's longer
       holds)"): every blow that roots, a new hold or a re-root, on the blow's
       own frame; a killing blow returned above and roots nobody, so it plays
       nothing. Plain SFX.play; nothing is read back (heartwood_voice_lab:
       fights identical). */
    SFX.play("ult", { w: "heartwood-root" });'''

# the sim-write control: the same row with the foe nudged 1e-9 on a root
ROOT_CODE_BAD = ROOT_CODE.replace('    SFX.play("ult", { w: "heartwood-root" });',
                                  '    q.vx += 1e-9;\n    SFX.play("ult", { w: "heartwood-root" });', 1)

_refuse(ROOT_CODE, "rootBlow row")


def _head(w, note):
    return f'        }} else if (w === "{w}"){{'.ljust(56) + f"// {note}"


def arms_code(C_, R_, root_text, info):
    c_cast = _comment([
        f'HEARTWOOD\'S CAST, ROOTFAST -- v85 section 4: "a green creak, 0.4s". {C_["name"].split()[1]}, of '
        f'{len(CAST_CANDIDATES)}, picked on the numbers by `heartwood_voice_lab.py` under Rick\'s "you pick i '
        f'overrule" (v112). Heartwood had no arm and fell through to rune-crack, which {info["n_rc"]} other '
        f'relics still use, so this ADDS arms before that fallback and leaves it alone.',
        f"{info['c_what']} A creak, not a note: pulses {info['c_rate']:.0f} a second (PULSED "
        f"{info['c_pulsed']:.2f}), never a held tone. Green, not dry: its note, {info['c_note']:.0f} Hz, sits "
        f"under the lowest the house's dry creak (Canopy's wither) reaches, {info['c_dry']:.0f} Hz, and it does "
        f"not wither ({info['c_nfall']:+.0f} cents first to last); no crack (that is the root's). Audible "
        f"{info['c_aud']:.0f} ms; loudest 50 ms {info['c_db']:+.1f} dB re Heartwood's blow. Register at most "
        f"{info['c_reg']:.2f} against rune-crack, the verdant and greatsword casts, Tendril's cast and root, "
        f"the dry creak, the blow and the death voice."], 10)
    c_root = _comment([
        f'THE ROOT -- "a short creak-and-crack (Tendril\'s root voice, reused, quieter at 1.0s than at the '
        f'vine\'s longer holds)" (v85 section 4). Tendril\'s root arm (`bindweed-root`, bindweed_voice_lab.py '
        f'DEEP) is not on every tip, so this is ITS BODY, VERBATIM, with one constant changed: g '
        f'{fmt(T_G)} -> {fmt(R_["g"])} ({R_["name"].split()[1]}, `heartwood_voice_lab.py`). `rootBlow` plays '
        f'it on every blow that roots.',
        f"A 260 Hz timber pulsed 33 -> 55 a second for 0.2 s into the crack, a 35 ms highpass snap over a sine "
        f"falling 60 -> 30 Hz, now {info['r_under']:.1f} dB under Tendril's (a 1.0 s hold against the vine's "
        f"1.2), {info['r_db']:+.1f} dB re Heartwood's blow and never over it. On the blow's own frame the root "
        f"keeps its third-octave {info['r_keep']:+.1f} dB over the blow and the blow its own "
        f"{info['r_blow']:+.1f} dB over the root; the crack lands {info['r_at']:.0f} ms in, after the blow. "
        f"Register {info['r_same']:.2f} against Tendril's root (the same voice), at most {info['r_reg']:.2f} "
        f"against rune-crack, the blow, the death voice and the cast."], 10)
    return (f"{_head(ME, 'the wood takes the blade')}\n"
            f"{c_cast}\n{cast_body(C_['sp'], C_['g'])}\n"
            f"{_head(ROOT_ID, 'and holds fast')}\n"
            f"{c_root}\n{root_text}\n"
            f"{SFX_ANCHOR}")


# ============================================================== THE PAGE ===
COST_JS = r"""([rows, reps, blade]) => {
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
  for (const [k, kind, p] of [["cast", "ult", { w: "heartwood" }], ["root", "ult", { w: "heartwood-root" }],
                              ["hit", "hit", { dmg: blade, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The rootBlow row, applied to the real prototype and run beside the original.
# The wrappers see every rootBlow and tickRootfast call, so a root voice is
# tied to the call that rooted, and a close is classified on the call that
# makes it.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "heartwood";
  const orig = P.rootBlow, origT = P.tickRootfast; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a rootBlow anchor occurs ${at} times in rootBlow()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const mine = [], other = [], dmgs = []; let step = 0, inRB = 0, inTR = 0, pend = false;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")){
        mine.push({ step, k: w, inRB: inRB > 0, inTR: inTR > 0, win: !!f.ultRoot, opts: JSON.stringify(p) });
        if (w === ME + "-root") pend = true;
      } else {
        other.push([step, kind, JSON.stringify(p || {})]);
        if (kind === "hit" && pend){ dmgs.push({ dmg: p.dmg, crit: !!p.crit, step }); pend = false; }
      }
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    const bad = []; let calls = 0, rooted = 0, fresh = 0, rootV = 0, kills = 0, killV = 0;
    P.rootBlow = function(self){
      const q = self === this.a ? this.b : this.a;
      const T = self.rootTally, r0 = T ? T.rooted : 0, n0 = T ? T.roots : 0, c0 = mine.length, alive0 = q.alive;
      inRB++;
      try { return impl.call(this, self); }
      finally {
        inRB--;
        const T1 = self.rootTally, dR = T1.rooted - r0, dN = T1.roots - n0;
        const v = mine.slice(c0).filter(c => c.k === ME + "-root").length;
        calls++; rooted += dR; fresh += dN; rootV += v;
        if (v !== dR) bad.push(["root voices vs rooted in one rootBlow", v, dR]);
        if (!alive0){ kills++; killV += v; }
      } };
    const wins = []; let W = null;
    P.tickRootfast = function(dt){
      const Z0 = f.ultRoot;
      if (Z0 && (!W || W.Z !== Z0)){ W = { Z: Z0, castStep: step, cast: m.t, rooted0: f.rootTally.rooted, end: null, close: null, rooted: 0 }; wins.push(W); }
      inTR++;
      try { return origT.call(this, dt); }
      finally {
        inTR--;
        if (Z0 && !f.ultRoot){
          W.end = (Z0.t >= Z0.dur && f.alive && foe.alive) ? "clock" : !f.alive ? "caster" : !foe.alive ? "foe" : "?";
          W.close = m.t; W.rooted = f.rootTally.rooted - W.rooted0;
        }
      } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; } }
    finally { P.rootBlow = orig; P.tickRootfast = origT; if (had) S.play = op; else delete S.play; }
    for (const w of wins) if (!w.end){ w.end = "over"; w.rooted = f.rootTally.rooted - w.rooted0; }
    const T = f.rootTally || {};
    if (dmgs.length !== rootV || dmgs.some((d, i) => d.step !== mine.filter(c => c.k === ME + "-root")[i].step))
      bad.push(["a root voice not followed on its step by its blow's hit voice", dmgs.length, rootV]);
    return { sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, m.a.vx, m.a.vy,
                                  m.b.vx, m.b.vy, m.a.pin, m.b.pin, m.a.stacks("entangle"), m.b.stacks("entangle"),
                                  m.winner ? m.winner.w.id : null, f.rootTally || null]),
             mine, other: JSON.stringify(other), casts: T.casts || 0, calls, rooted, fresh, rootV, kills, killV,
             bad, dmgs, wins: wins.map(w => { const { Z, ...r } = w; return r; }) };
  };
  let fights = 0, same = 0, otherSame = 0, castSame = 0; const diff = [], bad = [];
  const ends = { clock: 0, caster: 0, foe: 0, over: 0, "?": 0 };
  let casts = 0, castV = 0, calls = 0, rooted = 0, fresh = 0, rootV = 0, kills = 0, killV = 0, closeV = 0, outV = 0;
  const pick = [], dmg = {};
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    const ca = A.mine.filter(c => c.k === ME).map(c => c.step).join(","), cb = B.mine.filter(c => c.k === ME).map(c => c.step).join(",");
    if (ca === cb) castSame++;
    if (A.mine.some(c => c.k !== ME)) bad.push([fid, sd, "the UNPATCHED run played a Rootfast sub-voice"]);
    const cv = B.mine.filter(c => c.k === ME);
    casts += B.casts; castV += cv.length;
    if (cv.length !== B.casts) bad.push([fid, sd, "cast voices vs casts", cv.length, B.casts]);
    if (cv.some(c => c.inRB || c.inTR)) bad.push([fid, sd, "a cast voice from rootBlow or tickRootfast"]);
    for (const c of B.mine){
      if (c.k !== ME && c.k !== ME + "-root") bad.push([fid, sd, "an unknown Rootfast voice", c.k]);
      if (c.k === ME + "-root"){
        if (!c.inRB) bad.push([fid, sd, "a root voice outside rootBlow"]);
        if (!c.win){ outV++; bad.push([fid, sd, "a root voice with no window open"]); }
      }
      if (c.inTR) closeV++;
    }
    calls += B.calls; rooted += B.rooted; fresh += B.fresh; rootV += B.rootV; kills += B.kills; killV += B.killV;
    for (const b_ of B.bad) bad.push([fid, sd, ...b_]);
    if (B.rootV !== B.rooted) bad.push([fid, sd, "root voices vs rooted", B.rootV, B.rooted]);
    for (const d of B.dmgs){ const k = (d.crit ? "crit " : "") + (Math.round(d.dmg * 100) / 100); dmg[k] = (dmg[k] || 0) + 1; }
    for (const W of B.wins){
      ends[W.end]++;
      if (W.end === "clock") pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, rooted: W.rooted });
    }
  }
  if (closeV) bad.push(["voices from tickRootfast", closeV]);
  return { fights, same, otherSame, castSame, diff: diff.slice(0, 4), ends, casts, castV, calls, rooted, fresh,
           rootV, kills, killV, closeV, outV, dmg, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the row, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX, ME = "heartwood";
  const orig = P.rootBlow; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const ev = [];
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const tag = (kind === "ult" && typeof q.w === "string" && (q.w === ME || q.w.startsWith(ME + "-"))) ? q.w : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.rootBlow = patched;
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.rootBlow = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype, ME = "heartwood";
  const res = [];
  if (!P.rootBlow || !P.tickRootfast) return { err: "no rootBlow / tickRootfast" };
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a;
    const log = [], other = []; let inTR = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (w === ME || w.startsWith(ME + "-")) log.push([w, inTR > 0]);
      else other.push([kind, JSON.stringify(p || {})]);
      return op.call(this, kind, p); };
    const tr = P.tickRootfast;
    P.tickRootfast = function(dt){ inTR++; try { return tr.call(this, dt); } finally { inTR--; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
    finally { P.tickRootfast = tr; if (had) S.play = op; else delete S.play; }
    const T = f.rootTally || {};
    res.push({ key: [sd, fid, side].join(":"),
               sum: JSON.stringify([m.over, m.t, m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, m.a.vx, m.a.vy,
                                    m.b.vx, m.b.vy, m.a.pin, m.b.pin, m.winner ? m.winner.w.id : null,
                                    f.rootTally || null]),
               casts: T.casts || 0, rooted: T.rooted || 0, roots: T.roots || 0,
               castV: log.filter(e => e[0] === ME).length,
               rootV: log.filter(e => e[0] === ME + "-root").length,
               closeV: log.filter(e => e[1]).length,
               other: JSON.stringify(other) });
  }
  return res;
}"""


# =============================================================== PICKING ===
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms; 'a creak': over [onset + 10 "
    "ms, gone - 10 ms] RATE 17-83 a second and PULSED >= 0.40 (a pulse train at a "
    "creak's rate, never a held tone); 'green': its NOTE under the lowest note the "
    "house's dry creak reaches (Canopy's wither, its last 100 audible ms) and "
    "SHIFT >= -200 cents (it does not wither); a creak and NOT the root's "
    "crack: ALONE < 10 dB (the root's crack stands alone). Register "
    "against rune-crack, each verdant cast, Tendril's cast, each greatsword cast, "
    "the hit @ 11, the death voice, the dry creak, Paradox's pin and Tendril's "
    "root each <= 0.80. Level: TOP between 0.5x the hit @ 11's loudest 50 ms on "
    "its LOUDEST draw and 1.0x on its QUIETEST (heard like a blow, never over "
    "one). Tiebreak: the most distinct register (the highest of those, to 0.05), "
    "then the fewest calls, then the order listed.")

ROOT_RULE = (
    "'Tendril's root voice, reused': the arm is Tendril's body with only its gain "
    "changed (a text check), REG against Tendril's root >= 0.95 draw for draw and "
    "ENV-CORR >= 0.95; 'creak-and-crack': the crack STANDS >= 10 dB and JUMPS >= "
    "10 dB at >= 100 ms after the onset, AUDIBLE <= 420 ms; 'quieter at 1.0s': "
    "its loudest draw >= 3 dB under Tendril's quietest; never over the blow: its "
    "loudest draw <= the hit @ 11's quietest; heard: its quietest draw >= 2x the "
    "wall tick's loudest; on the blow's frame (the lightest, the median and the "
    "heaviest plain blow a root voice landed with in the wire run, and its "
    "heaviest crit; the worst of each): KEEP-ROOT >= 6 dB, KEEP-BLOW >= 6 dB, "
    "STAND-MIX >= 10 dB. "
    "Register against rune-crack, the hit @ 11, the death voice and the picked "
    "cast each <= 0.80. Pick: the LOUDEST that passes (the reused voice changed "
    "as little as the rule allows).")


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
    if M["gone"] > 470: why.append(f"gone at {M['gone']:.0f} ms")
    if not 17 <= M["mrate"] <= 83: why.append(f"rate {M['mrate']:.0f} a second, not a creak's 17-83")
    if M["pulsed"] < 0.40: why.append(f"pulsed {M['pulsed']:.2f} < 0.40")
    if M["note"] > lev["dry_low"]:
        why.append(f"note {M['note']:.0f} Hz, not under the dry creak's lowest {lev['dry_low']:.0f} (not green)")
    if M["shift"] < -200: why.append(f"shifts {M['shift']:+.0f} c, not >= -200 (withers)")
    if M["alone"] >= 10: why.append(f"a crack at {M['alone_at']:.0f} ms (stands alone {M['alone']:+.1f} dB)")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    return why


def root_why(M, lev):
    why = []
    if not M["text_ok"]: why.append("not Tendril's text with only g changed")
    if M["same_reg"] < 0.95: why.append(f"REG vs Tendril's root {M['same_reg']:.2f} < 0.95")
    if M["same_env"] < 0.95: why.append(f"ENV-CORR vs Tendril's root {M['same_env']:.2f} < 0.95")
    if M["stand"] < 10: why.append(f"the crack stands {M['stand']:+.1f} dB, not >= 10")
    if M["jump"] < 10: why.append(f"the crack jumps {M['jump']:+.1f} dB, not >= 10")
    if M["crack_at"] - M["a0"] < 100: why.append(f"the crack at {M['crack_at']:.0f} ms, not >= 100 after the onset")
    if M["aud"] > 420: why.append(f"audible {M['aud']:.0f} ms > 420")
    if M["top_hi"] > lev["quiet"]: why.append(f"loudest draw {M['top_hi']:.4f} > {lev['quiet']:.4f} (not quieter)")
    if M["top_hi"] > lev["blow"]: why.append(f"loudest draw {M['top_hi']:.4f} > the blow's {lev['blow']:.4f}")
    if M["top_lo"] < lev["floor"]: why.append(f"quietest draw {M['top_lo']:.4f} < {lev['floor']:.4f} (not heard)")
    if M["keep_root"] < KEEP_DB: why.append(f"keeps {M['keep_root']:+.1f} dB over the blow, not >= {KEEP_DB:g}")
    if M["keep_blow"] < KEEP_DB: why.append(f"the blow keeps {M['keep_blow']:+.1f} dB, not >= {KEEP_DB:g}")
    if M["stand_mix"] < 10: why.append(f"the crack stands {M['stand_mix']:+.1f} dB in the mix, not >= 10")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Heartwood stage 5 and none of its voices")
    ap.add_argument("--tendril", default="../02-chain/sc-tendril-fx.html",
                    help="a link carrying Tendril's voices (Bindweed stage 6): the root is read from it")
    ap.add_argument("--out", default="../05-reference/v112")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=112601)
    ap.add_argument("--e2e-seeds", type=int, default=1, help="fight seeds a pairing, end to end (0 skips it)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the checked rows here")
    a = ap.parse_args()
    import numpy as np

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    tp_ = resolve_game(a.tendril)
    thtml = tp_.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "tendril": tp_.name, "rules": {"cast": CAST_RULE, "root": ROOT_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("rootBlow", ROOT_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if ROOT_ID in html or f'}} else if (w === "{ME}"){{' in html:
        raise SystemExit(f"{gp.name} already carries Rootfast's voices -- run on stage 5")
    if 'kind:"rootfast"' not in html:
        raise SystemExit(f"{gp.name} does not carry Rootfast (stage 5)")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    rec["tendril_sha"] = hashlib.sha256(thtml.encode()).hexdigest()[:16]
    print(f"\nROOTFAST -- THE VOICES   game {gp.name} {rec['game_sha']}   Tendril's voices from {tp_.name} "
          f"{rec['tendril_sha']}")
    print("  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through Sfx.buildChain, "
          "render.py's xorshift noise;\n  a candidate is rendered from its arm's own text")

    # ---- TENDRIL'S ARMS, READ -------------------------------------------------
    TB = {w: tendril_arm(thtml, w)[1] for w in ("bindweed", "bindweed-bite", "bindweed-root", "bindweed-wither")}
    want = tendril_root_body(T_SP, T_G, T_KC, T_KT)
    if TB["bindweed-root"] != want:
        raise SystemExit("Tendril's root on --tendril is not bindweed_voice_lab's DEEP at g 0.5179, kc 0.2683, "
                         "kt 0.3464 -- the reuse would not be the shipped voice")
    print(f"  Tendril's root arm on {tp_.name}: its body equals bindweed_voice_lab.root_body(DEEP, g {fmt(T_G)}, "
          f"kc {fmt(T_KC)}, kt {fmt(T_KT)}) line for line ({len(want.splitlines())} lines)")
    for w in ("bindweed-bite", "bindweed-root", "bindweed-wither"):
        if w in html:
            raise SystemExit(f"{gp.name} carries {w} -- this lab expects a base without Tendril's voices")

    sizes = {}

    def wav(name, x):
        sizes[name] = write_wav(out / name, x)

    e2e_ref = {}
    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        mirror = page.evaluate("() => { try { new AC.Match('heartwood', 'heartwood', 1); return 'allowed'; } "
                               "catch (e) { return 'refused: ' + e.message; } }")
        print(f"  the mirror match: {mirror}")
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if ME not in ids:
            raise SystemExit("no heartwood in this build")
        row = page.evaluate("() => { const w = AC.WEAPONS.find(w => w.id === 'heartwood'); "
                            "return [w.dmg, w.ult.kind, w.ult.rootFor]; }")
        if abs(row[0] - BLADE) > 1e-9 or row[1] != "rootfast" or abs(row[2] - ROOT_FOR) > 1e-9:
            raise SystemExit(f"Heartwood's row is {row}; this lab levels against blade {BLADE}, rootfast, "
                             f"rootFor {ROOT_FOR}")
        print(f"  {len(ids)} relics; Heartwood blade {row[0]}, ult {row[1]}, rootFor {row[2]} s "
              f"(the vine's hold at the cap: {VINE_HOLD_CAP:g} s)")

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

        def body(text, p=None, seed=None):
            return R([["body", T0, text, p or {}]], seed=seed)

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, (kind, p) in [("rune-crack", ("ult", {"w": "spellbreaker"})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                ("hit@11", ("hit", {"dmg": BLADE, "crit": False})),
                                ("hit@23!", ("hit", {"dmg": 23, "crit": True})),
                                ("wall", ("wall", {})), ("death", ("death", {})),
                                ("dry-creak", ("ult", {"w": "ironwood-wither"})),
                                ("paradox-pin", ("ult", {"w": "paradox-pin"})),
                                ("tendril-root-here", ("ult", {"w": "bindweed-root"}))]:
            x = play(kind, p)
            ctl[name] = dict(basic(x), x=x, low=low_share(x))
            M = ctl[name]
            print(f"  {name:<18} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
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
            raise SystemExit("Heartwood's cast is not rune-crack today -- this lab adds its arm, so stop")
        th_rc = float(np.abs(ctl["tendril-root-here"]["x"] - rcx).max())
        print(f"  ult/bindweed-root on THIS base vs rune-crack: max |diff| {th_rc:.1e} -- "
              f"{'Tendril root voice is NOT here (it falls through), so the lab makes one' if th_rc <= 1e-6 else 'IT EXISTS HERE'}")
        if th_rc > 1e-6:
            raise SystemExit("Tendril's root voice exists on this base -- reuse it by id instead")
        rec["fallthrough"] = fall_ids
        school = [w_ for w_ in SCHOOL if w_ not in fall_ids]
        types = [w_ for w_ in TYPE if w_ not in fall_ids]
        print(f"  the verdant casts with their own voice here: {', '.join(school)} (+ Tendril's, read from "
              f"{tp_.name});  the greatsword row's: {', '.join(types)}")

        # the noise draws of every reference
        REFS = {"hit@11": ("play", "hit", {"dmg": BLADE, "crit": False}), "wall": ("play", "wall", {}),
                "rune-crack": ("play", "ult", {"w": "spellbreaker"}), "death": ("play", "death", {}),
                "dry-creak": ("play", "ult", {"w": "ironwood-wither"}),
                "paradox-pin": ("play", "ult", {"w": "paradox-pin"}),
                "tendril-cast": ("body", TB["bindweed"], {}), "tendril-root": ("body", TB["bindweed-root"], {}),
                "tendril-bite": ("body", TB["bindweed-bite"], {"n": 4}),
                "tendril-wither": ("body", TB["bindweed-wither"], {})}
        for w_ in school + types:
            REFS[w_] = ("play", "ult", {"w": w_})
        RD = {k: [] for k in REFS}
        RX = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (how, a1, a2) in REFS.items():
                x = play(a1, a2, seed=sd) if how == "play" else body(a1, a2, seed=sd)[0]
                RD[k].append(basic(x)); RX[k].append(x)
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD.items()}
        h_lo, h_hi = min(m_["top"] for m_ in RD["hit@11"]), max(m_["top"] for m_ in RD["hit@11"])
        w_hi = max(m_["top"] for m_ in RD["wall"])
        tr_lo, tr_hi = min(m_["top"] for m_ in RD["tendril-root"]), max(m_["top"] for m_ in RD["tendril-root"])
        print(f"  the hit @ 11 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD['hit@11']):.3f}-{max(m_['peak'] for m_ in RD['hit@11']):.3f};  the "
              f"wall tick: {min(m_['top'] for m_ in RD['wall']):.4f}-{w_hi:.4f};  Tendril's root: {tr_lo:.4f}-"
              f"{tr_hi:.4f} ({db(tr_lo / h_lo):+.1f} dB re the hit @ 11's quietest -- the level it would land at)")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        rec["levels"] = dict(hit11=[h_lo, h_hi], wall_hi=w_hi, tendril_root=[tr_lo, tr_hi])
        wav("heartwood-ctl-runecrack.wav", rcx)
        wav("heartwood-ctl-hit11.wav", ctl["hit@11"]["x"])
        wav("heartwood-ctl-tendril-root.wav", RX["tendril-root"][0])
        wav("heartwood-ctl-dry-creak.wav", ctl["dry-creak"]["x"])
        dry_cen = ctl["dry-creak"]["cen"]
        dry_note, dry_nfall, dry_low = note_info(ctl["dry-creak"]["x"], ctl["dry-creak"]["a0"],
                                                 ctl["dry-creak"]["gone"])
        print(f"  the house's dry creak (Canopy's wither): note {dry_note:.0f} Hz, falling {dry_nfall:+.0f} cents to "
              f"{dry_low:.0f} Hz over its last 100 audible ms (SHIFT "
              f"{shift(ctl['dry-creak']['x'], ctl['dry-creak']['a0'], ctl['dry-creak']['gone']):+.0f} c); centroid "
              f"{dry_cen:.0f} Hz; ALONE "
              f"{alone(ctl['dry-creak']['x'])[0]:+.1f} dB (Tendril's root: {alone(RX['tendril-root'][0])[0]:+.1f})")

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo, dry_low=dry_low)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a green creak, 0.4s'. Level-matched: TOP {tgt_c:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}); green: a note under {dry_low:.0f} Hz")

        def calib(fn):
            g = 0.1
            for _ in range(5):
                g = float(f"{g * tgt_c / basic(body(fn(g))[0])['top']:.4g}")
            return g

        CAST_REGS = (["rune-crack"] + school + ["tendril-cast"] + types +
                     ["hit@11", "death", "dry-creak", "paradox-pin", "tendril-root"])

        def cast_measure(name, x, draws, calls):
            M = basic(x); M.update(x=x, calls=calls, name=name)
            a_ = M["a0"] / 1000 + 0.01; b_ = M["gone"] / 1000 - 0.01
            M["mrate"] = mod_rate(x, a_, b_) if b_ - a_ >= 0.05 else 0.0
            M["pulsed"], M["rate"], M["depth"] = pulsed_w(x, a_, b_) if b_ - a_ >= 0.0999 else (0.0, 0.0, 0.0)
            M["green"] = M["cen"] / dry_cen
            g0 = T0 + M["a0"] / 1000; g1 = T0 + M["gone"] / 1000
            M["fall"] = cents(centroid(x, g1 - 0.1, g1, 60, 4000), centroid(x, g0, g0 + 0.1, 60, 4000))
            M["crack_at"], M["stand"], M["jump"] = crack_info(x, M["a0"])
            M["note"], M["nfall"], _nl = note_info(x, M["a0"], M["gone"])
            M["alone"], M["alone_at"] = alone(x)
            M["shift"] = shift(x, M["a0"], M["gone"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in CAST_REGS if not (name.endswith("DRY") and k == "dry-creak")
                         and not (name.endswith("CRACK") and k == "tendril-root")}
            return M

        def cast_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<11}{M.get('g', 0):>8.4g}{M['calls']:>6d}{M['top']:>8.4f}{M['aud']:>6.0f}"
                  f"{M['gone']:>6.0f}{M['mrate']:>6.0f}{M['pulsed']:>7.2f}{M['note']:>6.0f}{M['shift']:>7.0f}"
                  f"{M['nfall']:>7.0f}"
                  f"{M['alone']:>7.1f}{M['cen']:>6.0f}{M['fall']:>7.0f}{M['stand']:>7.1f}{max(r_.values()):>6.2f} "
                  f"({max(r_, key=r_.get)})")

        print(f"  {'cand':<11}{'g':>8}{'calls':>6}{'top':>8}{'aud':>6}{'gone':>6}{'rate':>6}{'pulse':>7}"
              f"{'note':>6}{'shift':>7}{'nfall':>7}{'alone':>7}{'cen':>6}{'cfall':>7}{'stand':>7}{'reg':>6}")
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g = calib(lambda g_, sp=sp: cast_body(sp, g_))
            x, calls = body(cast_body(sp, g))
            x2, _ = body(cast_body(sp, g))
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"cast {name} does not reproduce")
            draws = [body(cast_body(sp, g), seed=sd)[0] for sd in NOISE_SEEDS]
            M = cast_measure(name, x, draws, calls[0])
            M.update(sp=sp, g=g); M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"heartwood-cast-{name.replace(' ', '-').lower()}.wav", x)
        ctlc = []
        gh = calib(lambda g_: held_body(g_))
        xh, ch = body(held_body(gh))
        M = cast_measure("0 HELD", xh, [xh], ch[0]); M["g"] = gh; ctlc.append(M)
        wsp = dict(rows_c[2]["sp"], pitch="450 * Math.pow(250 / 450, u)")
        gw = calib(lambda g_: cast_body(wsp, g_))
        xw_, cw_ = body(cast_body(wsp, gw))
        M = cast_measure("0 WITHER", xw_, [xw_], cw_[0]); M["g"] = gw; ctlc.append(M)
        M = cast_measure("0 DRY", ctl["dry-creak"]["x"], RX["dry-creak"], 0); ctlc.append(M)
        M = cast_measure("0 CRACK", RX["tendril-root"][0], RX["tendril-root"], 0); ctlc.append(M)
        M = cast_measure("0 RUNECRACK", rcx, RX["rune-crack"], 0); ctlc.append(M)
        for M in ctlc:
            M["why"] = cast_why(M, lev_c); cast_line(M)
        wav("heartwood-cast-0-held.wav", xh)
        wav("heartwood-cast-0-wither.wav", xw_)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<10} {blurb}")
        print("    0 HELD     KNOT's sine held by re-striking at its own cycles, no stick-slip -- a control on "
              "'a creak'\n"
              "    0 WITHER   KNOT falling 450 -> 250 Hz -- a control on 'green' (it withers)\n"
              "    0 DRY      Canopy's wither, the house's dry creak -- a control on 'green'\n"
              "    0 CRACK    Tendril's root, a creak INTO a crack -- a control on 'not the root's crack'\n"
              "    0 RUNECRACK  the fallback it replaces -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<10} out: {'; '.join(M['why'])}")
        want_fail = {"0 HELD": ("rate",), "0 WITHER": ("shifts",), "0 DRY": ("note ", "shifts"),
                     "0 CRACK": ("a crack",), "0 RUNECRACK": ()}
        for M in ctlc:
            hits_ = [w_ for w_ in M["why"] if any(w_.startswith(k) for k in want_fail[M["name"]])]
            if M["why"] and (hits_ or not want_fail[M["name"]]):
                print(f"  {M['name']} (a control) comes back wrong, as it must: "
                      f"{'; '.join((hits_ or M['why'])[:3])}")
            else:
                print(f"  {M['name']} (a control) did NOT fail the gate it controls ({'; '.join(M['why'][:3]) or 'passed'})"
                      " -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"]))
        C_ = rows_c[ci]
        print(f"  PICK  {C_['name']}  g {C_['g']}, {C_['calls']} synth calls; TOP {C_['top']:.4f} = "
              f"{db(C_['top'] / h_lo):+.1f} dB re the hit @ 11 (quietest draw), {db(C_['top'] / w_hi):+.1f} dB re "
              f"the wall")

        # ---- THE rootBlow ROW ------------------------------------------------
        rb_rows = [[ROOT_ANCHOR, ROOT_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE rootBlow ROW, applied to the prototype's own source, run beside the original on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds, rb_rows])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Heartwood both sides x every foe x seeds {seeds}): {WR['same']}/"
              f"{WR['fights']} identical (over, clock, both hp, positions, velocities, pins, entangle, winner, the "
              f"whole rootTally); every other SFX call identical in order and opts in {WR['otherSame']}/"
              f"{WR['fights']}; the cast voices on the same steps in {WR['castSame']}/{WR['fights']}")
        print(f"  windows {WR['ends']}: {WR['casts']} casts -> {WR['castV']} cast voices; {WR['calls']} blows in a "
              f"window -> {WR['rooted']} rooted ({WR['fresh']} new holds, {WR['rooted'] - WR['fresh']} re-roots) -> "
              f"{WR['rootV']} root voices; {WR['kills']} killing blows in a window -> {WR['killV']} voices; "
              f"voices from tickRootfast (the close) {WR['closeV']}; root voices outside a window {WR['outV']}; "
              f"problems {WR['nbad']}")
        dm = sorted(WR["dmg"].items(), key=lambda kv: -kv[1])
        print("  the blow each root voice lands with (the hit voice on the same step): " +
              ", ".join(f"{k} x{v}" for k, v in dm[:8]))
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["castSame"] != WR["fights"] \
                or WR["nbad"] or WR["castV"] != WR["casts"] or WR["rootV"] != WR["rooted"] or WR["rootV"] == 0 \
                or WR["killV"] or WR["closeV"] or WR["outV"]:
            FAILED.append("rootBlow row")
        WB = page.evaluate(WIRE_JS, [seeds, [[ROOT_ANCHOR, ROOT_CODE_BAD]]])
        assert not errors, errors[:3]
        print(f"  the control (the row plus one sim write, the foe nudged 1e-9 on a root): {WB['same']}/"
              f"{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "castSame", "ends", "casts", "castV",
                                          "calls", "rooted", "fresh", "rootV", "kills", "killV", "closeV", "outV",
                                          "dmg", "nbad")}
        rec["wire"]["control_same"] = WB["same"]

        # the blows a root lands with, as the wire run heard them
        nc = sorted(float(k) for k, v in WR["dmg"].items() if not k.startswith("crit") for _ in range(v))
        cr = sorted(float(k.split()[1]) for k, v in WR["dmg"].items() if k.startswith("crit") for _ in range(v))
        blows = [(nc[0], False), (nc[len(nc) // 2], False), (nc[-1], False),
                 ((cr[-1] if cr else round(BLADE * 2.1)), True)]
        FRAME_BLOWS[:] = list(dict.fromkeys(blows))
        print(f"  the blows the root voices landed with: {len(nc)} plain ({nc[0]:g}-{nc[-1]:g}, median "
              f"{nc[len(nc) // 2]:g}) and {len(cr)} crits" + (f" ({cr[0]:g}-{cr[-1]:g})" if cr else "") +
              " -> the frame checks run at " + ", ".join(f"{d_:g}{'!' if c_ else ''}" for d_, c_ in FRAME_BLOWS))
        rec["frame_blows"] = FRAME_BLOWS

        # ---- THE ROOT ------------------------------------------------------
        lev_r = dict(quiet=tr_lo * 10 ** (-QUIETER_DB / 20), blow=h_lo, floor=2 * w_hi)
        print(f"\nROOT -- 'a short creak-and-crack (Tendril's root voice, reused, quieter at 1.0s than at the vine's "
              f"longer holds)'. Tendril's body verbatim, g {fmt(T_G)} scaled down a ladder; gates: loudest draw "
              f"<= {lev_r['quiet']:.4f} (Tendril's quietest - {QUIETER_DB:g} dB) and <= {lev_r['blow']:.4f} (the "
              f"blow's quietest), quietest draw >= {lev_r['floor']:.4f} (2x the wall). The hold ratio's literal "
              f"20 log({ROOT_FOR:g} / {VINE_HOLD_CAP:g}) = {20 * math.log10(ROOT_FOR / VINE_HOLD_CAP):+.1f} dB "
              f"is printed, not taken")
        tr_x = RX["tendril-root"][0]
        HX = {b_: play("hit", {"dmg": b_[0], "crit": b_[1]}) for b_ in FRAME_BLOWS}
        HB = {b_: peak_band(x_, T0, T0 + 0.15) for b_, x_ in HX.items()}
        print("  the blows a root lands with, their own third-octaves: " +
              ", ".join(f"{d_}{'!' if c_ else ''} {HB[(d_, c_)]:.0f} Hz" for d_, c_ in FRAME_BLOWS))
        ROOT_REGS = ["rune-crack", "hit@11", "death"]

        def frame(text, x_root):
            """the root and the blow on one frame (render.py's draw), at every
            blow of FRAME_BLOWS: the worst of each number."""
            rband = peak_band(x_root, T0, T0 + 0.35)
            at, _s, _j = crack_info(x_root, basic(x_root)["a0"])
            kr, kb, sm = [], [], []
            for b_ in FRAME_BLOWS:
                both = R([["body", T0, text, {}], ["play", T0, "hit", {"dmg": b_[0], "crit": b_[1]}]], new=False)[0]
                kr.append(db(band_rms(both, rband, T0, T0 + 0.35) / band_rms(HX[b_], rband, T0, T0 + 0.35)))
                kb.append(db(band_rms(both, HB[b_], T0, T0 + 0.15) / band_rms(x_root, HB[b_], T0, T0 + 0.15)))
                e = hf_env(both)
                i = int(at); pre = e[max(0, i - 60):max(1, i - 10)]
                sm.append(db(float(e[i]) / max(float(np.percentile(pre, 90)), 1e-12)))
            return min(kr), min(kb), min(sm), rband

        def root_measure(name, text, g, text_ok, draws=None, x=None, calls=0):
            if x is None:
                x, cl = body(text); calls = cl[0]
                draws = [body(text, seed=sd)[0] for sd in NOISE_SEEDS]
            M = basic(x); M.update(x=x, calls=calls, name=name, g=g, text=text, text_ok=text_ok)
            M["top_lo"] = min(basic(d_)["top"] for d_ in draws); M["top_hi"] = max(basic(d_)["top"] for d_ in draws)
            M["low"] = low_share(x)
            M["crack_at"], M["stand"], M["jump"] = crack_info(x, M["a0"])
            DB = [bands(d_[int(T0 * SR):]) for d_ in draws]
            M["DB"] = DB
            M["same_reg"] = mreg(DB, RB["tendril-root"])
            M["same_env"] = env_corr(x, tr_x)
            M["regs"] = {k: mreg(DB, RB[k]) for k in ROOT_REGS}
            M["regs"]["cast"] = mreg(DB, C_["DB"])
            M["keep_root"], M["keep_blow"], M["stand_mix"], M["band"] = frame(text, x)
            M["under"] = db(M["top"] / RD["tendril-root"][0]["top"])
            return M

        def root_line(M):
            r_ = M["regs"]
            print(f"  {M['name']:<13}{M.get('g', 0):>8.4g}{M['top']:>8.4f}{M['under']:>7.1f}{db(M['top'] / h_lo):>7.1f}"
                  f"{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}{M['aud']:>6.0f}{M['low']:>6.2f}{M['crack_at']:>6.0f}"
                  f"{M['stand']:>6.1f}{M['jump']:>6.1f}{M['same_reg']:>6.2f}{M['same_env']:>6.2f}"
                  f"{M['keep_root']:>7.1f}{M['keep_blow']:>7.1f}{M['stand_mix']:>7.1f}{max(r_.values()):>6.2f} "
                  f"({max(r_, key=r_.get)})")

        print(f"  {'cand':<13}{'g':>8}{'top':>8}{'dB/T':>7}{'dB/hit':>7}{'topW-':>8}{'topW+':>8}{'aud':>6}{'low':>6}"
              f"{'crk@':>6}{'stand':>6}{'jump':>6}{'sameR':>6}{'sameE':>6}{'keepR':>7}{'keepB':>7}{'mixSt':>7}{'reg':>6}")
        rows_r = []
        for k_db in ROOT_LADDER_DB:
            g = float(f"{T_G * 10 ** (-k_db / 20):.4g}")
            text = root_from_tendril(TB["bindweed-root"], g)
            ok_t = text == tendril_root_body(T_SP, g, T_KC, T_KT)
            name = f"{ROOT_LADDER_DB.index(k_db) + 1} G-{k_db:g}dB"
            x1, _ = body(text); x2, _ = body(text)
            if float(np.abs(x1 - x2).max()) > 1e-6:
                raise SystemExit(f"root {name} does not reproduce")
            M = root_measure(name, text, g, ok_t); M["why"] = root_why(M, lev_r)
            rows_r.append(M); root_line(M)
            wav(f"heartwood-root-{name.replace(' ', '-').lower()}.wav", x1)
        ctlr = []
        full = root_from_tendril(TB["bindweed-root"], T_G)
        ctlr.append(root_measure("0 FULL", full, T_G, True))
        gf = float(f"{T_G * 10 ** (-24 / 20):.4g}")
        ctlr.append(root_measure("0 FAINT", root_from_tendril(TB["bindweed-root"], gf), gf, True))
        pp = ctl["paradox-pin"]["x"]
        Mpp = basic(pp)
        # paradox's pin through the same measures (its text is not Tendril's)
        M = dict(Mpp, x=pp, calls=0, name="0 PARADOX-PIN", g=0.0, text_ok=False,
                 top_lo=min(m_["top"] for m_ in RD["paradox-pin"]), top_hi=max(m_["top"] for m_ in RD["paradox-pin"]),
                 low=low_share(pp))
        M["crack_at"], M["stand"], M["jump"] = crack_info(pp, M["a0"])
        M["DB"] = RB["paradox-pin"]; M["same_reg"] = mreg(RB["paradox-pin"], RB["tendril-root"])
        M["same_env"] = env_corr(pp, tr_x)
        M["regs"] = {k: mreg(M["DB"], RB[k]) for k in ROOT_REGS}; M["regs"]["cast"] = mreg(M["DB"], C_["DB"])
        M["keep_root"], M["keep_blow"], M["stand_mix"], M["band"] = 99.0, 99.0, 99.0, 0.0
        M["under"] = db(M["top"] / RD["tendril-root"][0]["top"])
        ctlr.append(M)
        g5 = rows_r[1]["g"]
        bb = back_body(g5)
        Mb = root_measure("0 BACK", bb, g5, False); ctlr.append(Mb)
        for M in ctlr:
            M["why"] = root_why(M, lev_r); root_line(M)
        wav("heartwood-root-0-back.wav", Mb["x"])
        print("    G-n dB     Tendril's root body, verbatim, its g scaled n dB down (the chain compresses: TOP moves "
              "by its own amount, dB/T)\n"
              "    0 FULL     Tendril's root at its own gain -- a control on 'quieter'\n"
              "    0 FAINT    Tendril's root 24 dB down -- a control on 'heard'\n"
              "    0 PARADOX-PIN  the game's other hold voice -- a control on 'reused' (and its frame "
              "checks are not run)\n"
              "    0 BACK     Tendril's root with the crack first -- a control on 'reused'")
        print(f"  RULE  {ROOT_RULE}")
        for M in rows_r:
            if M["why"]:
                print(f"    {M['name']:<12} out: {'; '.join(M['why'])}")
        want_r = {"0 FULL": ("(not quieter)",), "0 FAINT": ("(not heard)", "over the blow, not"),
                  "0 PARADOX-PIN": ("REG vs Tendril", "ENV-CORR vs Tendril"),
                  "0 BACK": ("REG vs Tendril", "ENV-CORR vs Tendril")}
        for M in ctlr:
            hits_ = [w_ for w_ in M["why"] if any(k in w_ for k in want_r[M["name"]])]
            if hits_:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(hits_[:3])}")
            else:
                print(f"  {M['name']} (a control) did NOT fail the gate it controls -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        print(f"  (BACK and PARADOX-PIN also fail the text check; the controls above are held to the SOUND "
              f"checks, REG and ENV-CORR against Tendril's root, which a transcription could not fake)")
        ok, fb = _gate(rows_r, "root")
        ri = fb if ok is None else max(ok, key=lambda i: rows_r[i]["top"])
        R_ = rows_r[ri]
        print(f"  PICK  {R_['name']}  g {R_['g']}: TOP {R_['top']:.4f}, {R_['under']:+.1f} dB re Tendril's root, "
              f"{db(R_['top'] / h_lo):+.1f} dB re the hit @ 11, {db(R_['top_lo'] / w_hi):+.1f} dB re the wall; on the "
              f"blow's frame (the worst of the blows the wire run heard) the root keeps {R_['keep_root']:+.1f} dB in its "
              f"{R_['band']:.0f} Hz third-octave, the blow {R_['keep_blow']:+.1f} dB in its own, the crack stands "
              f"{R_['stand_mix']:+.1f} dB")
        wav("heartwood-root-pick-with-blow.wav",
            R([["body", T0, R_["text"], {}], ["play", T0, "hit", {"dmg": BLADE, "crit": False}]], new=False)[0])

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        cdesc = dict((n_, b_) for n_, _s, b_ in CAST_CANDIDATES)[C_["name"]]
        what_cast = cdesc[0].upper() + cdesc[1:]
        info = dict(
            n_rc=["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                  "twelve", "thirteen"][min(13, len(fall_ids) - 1)],
            c_what=f"{what_cast}.", c_rate=C_["mrate"], c_pulsed=C_["pulsed"], c_note=C_["note"],
            c_dry=dry_low, c_nfall=C_["shift"], c_aud=C_["aud"], c_db=db(C_["top"] / h_lo),
            c_reg=max(C_["regs"].values()),
            r_under=-R_["under"], r_db=db(R_["top"] / h_lo), r_keep=R_["keep_root"], r_blow=R_["keep_blow"],
            r_at=R_["crack_at"], r_same=R_["same_reg"], r_reg=max(R_["regs"].values()))
        arms = arms_code(C_, R_, R_["text"], info)
        _refuse(arms, "Sfx row")
        sfx_rows = [[SFX_ANCHOR, arms]]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        chk = []
        xa1, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows)
        chk.append(("cast", float(np.abs(xa1 - C_["x"]).max())))
        for sd in (None, NOISE_SEEDS[3]):
            xr1, _ = R([["arm", T0, "ult", {"w": ROOT_ID}]], rows=sfx_rows, seed=sd)
            xr2, _ = body(R_["text"], seed=sd)
            chk.append((f"root{'' if sd is None else ' draw'}", float(np.abs(xr1 - xr2).max())))
        xt_, _ = R([["arm", T0, "ult", {"w": ROOT_ID}]], rows=sfx_rows)
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, 9, 11, 18, 50) for c_ in (False, True)]
        others += [("spark", {"collect": True, "n": 3}), ("spark", {"arm": True}), ("spark", {"collect": False}),
                   ("wall", {}), ("death", {}), ("clank", {"mass": 5}), ("seal", {}), ("nova", {"k": 1}),
                   ("hex-snap", {}), ("fork", {}), ("vine", {}), ("vine", {"plant": True}), ("vine", {"coil": True}),
                   ("vine", {"miss": True}), ("loose", {}), ("loose", {"bal": True}), ("loose", {"leaf": True}),
                   ("aegis", {"n": 3, "back": 5}), ("scour-hold", {"n": 5}), ("scour-tick", {}),
                   ("scour-woosh", {"n": 1}), ("scour-moo", {}),
                   ("ult", {"w": "ironwood-sprout"}), ("ult", {"w": "ironwood-wither"}),
                   ("ult", {"w": "morningstar-tick", "n": 2}), ("ult", {"w": "morningstar-close"}),
                   ("ult", {"w": "paradox-pin"}), ("ult", {"w": "nightfell-boom"}),
                   ("ult", {"w": "bindweed-root"})]
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
              f"scour x4, seven ult sub-voices, the {len(ids) - 1} other casts): worst max |diff| {worst[1]:.0e} "
              f"({worst[0]})")
        now_rc = float(np.abs(xa1 - rcx).max())
        root_rc = float(np.abs(xt_ - rcx).max())
        print(f"  ult/heartwood vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'};  ult/heartwood-root vs "
              f"rune-crack {root_rc:.3f}")
        if max(v for _, v in chk) > 1e-6 or worst[1] > 1e-6 or now_rc <= 1e-3 or root_rc <= 1e-3 or len(same_) < 30:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [sfx_rows, 40, BLADE])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, root_rc=root_rc, cost=cost)

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["rooted"], w["foe"], w["seed"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], rb_rows])
            assert not errors, errors[:3]
            c0t = w_["cast"]; c1t = w_["close"]
            lo_t, hi_t = c0t - 1.0, c1t + 2.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
            xo, _ = R([v_ for v_, e in zip(allv, evs) if e[3] != ROOT_ID], secs=secs, rows=sfx_rows, new=False)
            xoc, _ = R([v_ for v_, e in zip(allv, evs) if e[3] != ME], secs=secs, rows=sfx_rows, new=False)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd; xoc = xoc + bd
            cband = peak_band(C_["x"], T0, T0 + 0.4)
            ro_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == ROOT_ID]
            ca_t = [T0 + (e[0] - lo_t) for e in evs if e[3] == ME]
            ro_over = [db(band_rms(xw, R_["band"], t_, t_ + 0.35) / max(band_rms(xo, R_["band"], t_, t_ + 0.35), 1e-12))
                       for t_ in ro_t]
            ca_over = [db(band_rms(xw, cband, t_, t_ + 0.4) / max(band_rms(xoc, cband, t_, t_ + 0.4), 1e-12))
                       for t_ in ca_t]
            print(f"\nIN A REAL WINDOW -- heartwood v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0t:.2f}s, closed by its clock at {c1t:.2f}s, {w_['rooted']} rooted blows; the fight's own "
                  f"sounds and the score, with and without the new voices")
            print(f"  the cast over everything else on its frame in its own third-octave ({cband:.0f} Hz): " +
                  " ".join(f"{v:+.1f}" for v in ca_over) + " dB")
            print(f"  each root over everything else, its own blow included, in its own third-octave "
                  f"({R_['band']:.0f} Hz): " + " ".join(f"{v:+.1f}" for v in ro_over) + " dB" +
                  (f" (median {np.median(ro_over):+.1f}, min {min(ro_over):+.1f})" if ro_over else ""))
            if not ro_over or float(np.median(ro_over)) < 3 or not ca_over or min(ca_over) < 3 or len(ca_t) != 1:
                FAILED.append("a new voice not heard in a real window")
            wav("heartwood-pick-real-window.wav", xw)
            wav("heartwood-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, root_over=ro_over, cast_over=ca_over)
        else:
            print("\nIN A REAL WINDOW -- no clock close in the wire runs")
            FAILED.append("no real window")
        # the picks in order, for the ear: the cast, then three blows that root, then a plain blow
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k, t_ in enumerate((0.7, 1.25, 1.8)):
            seq += [["arm", T0 + t_, "ult", {"w": ROOT_ID}], ["arm", T0 + t_, "hit", {"dmg": BLADE, "crit": k == 2}]]
        seq += [["arm", T0 + 2.6, "hit", {"dmg": BLADE, "crit": False}]]
        wav("heartwood-pick-sequence.wav", R(seq, secs=4.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        if a.e2e_seeds > 0:
            e2e_ref["voices"] = [play(kind, p) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [[a.seed0 + 50 + k for k in range(a.e2e_seeds)]])
            assert not errors, errors[:3]
            if isinstance(e2e_ref["fights"], dict):
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- END TO END: the rows applied AS TEXT, in a second browser (the first is closed)
    rows = [dict(label="Sfx: Heartwood's cast and root arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arms),
            dict(label="rootBlow: the root voice, once per rooted blow, after T.rooted++",
                 anchor=ROOT_ANCHOR, mode="replace", code=ROOT_CODE)]
    for r_ in rows:
        if r_["code"].count(r_["anchor"]) != 1:
            raise SystemExit("a row does not re-emit its anchor exactly once")
        _refuse(r_["code"], r_["label"])
    if a.e2e_seeds > 0:
        patched = html
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit(f"end to end: an anchor occurs {patched.count(r_['anchor'])} times")
            patched = patched.replace(r_["anchor"], r_["code"], 1)
        for r_ in rows:
            if patched.count(r_["anchor"]) != 1:
                raise SystemExit("end to end: an anchor is not re-emitted exactly once")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="heartwood_e2e_"))
        try:
            tp = tmpd / "sc-heartwood-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the two rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            with game(game_path=tp) as (page, errors):
                def R2(evs, seed=None):
                    r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                    assert not errors, errors[:3]
                    return pcm(r)
                vo = max(float(np.abs(R2([["play", T0, k, p]]) - x0).max())
                         for (k, p), x0 in zip(e2e_voices, e2e_ref["voices"]))
                nd = []
                for lab_, p, text in (("cast", {"w": ME}, cast_body(C_["sp"], C_["g"])),
                                      ("root", {"w": ROOT_ID}, R_["text"])):
                    for sd in (NOISE_SEEDS[0], NOISE_SEEDS[5]):
                        x1 = R2([["play", T0, "ult", p]], seed=sd)
                        x2 = R2([["body", T0, text, {}]], seed=sd)
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
        r_ok = sum(f_["rootV"] == f_["rooted"] for f_ in F1)
        z_ok = sum(f_["closeV"] == 0 for f_ in F1)
        orig_new = sum(f_["rootV"] for f_ in e2e_ref["fights"])
        tot = {k: sum(f_[k] for f_ in F1) for k in ("casts", "rooted", "roots", "castV", "rootV", "closeV")}
        print(f"  the new voices through the patched page's own SFX.play vs the lab's candidate text in that page "
              f"(two noise draws each), max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(e2e_voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/heartwood vs rune-crack on the patched page {not_rc:.3f}")
        print(f"  {len(F1)} fights: {same}/{len(F1)} identical to the original page's, every other SFX call identical "
              f"in {osame}/{len(F1)}; per fight -- cast voices = casts {c_ok}, root voices = rooted blows {r_ok}, no "
              f"voice at a close {z_ok} (of {len(F1)}); totals {tot}; the original page played {orig_new} root "
              f"voices; page errors {page_err}")
        if max(v for _, v in nd) > 1e-6 or vo > 1e-6 or not_rc <= 1e-3 or same != len(F1) or osame != len(F1) \
                or min(c_ok, r_ok, z_ok) != len(F1) or orig_new or page_err or tot["rootV"] == 0:
            FAILED.append("end to end")
        rec["e2e"] = dict(patched_sha=psha, new=nd, others=vo, not_rc=not_rc, fights=len(F1), same=same,
                          other_same=osame, totals=tot)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "xs", "bands", "DB", "text")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), root=strip(rows_r), root_controls=strip(ctlr),
               wavs=sizes, pick={"cast": C_["name"], "cast_g": C_["g"], "root": R_["name"], "root_g": R_["g"]})
    print(f"\nTHE PICKS  cast {C_['name']}   root {R_['name']} (g {fmt(R_['g'])})   close: nothing")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    wr = rec["wire"]
    rows[0]["why"] = (
        f"Rootfast's two voices (v85 section 4), in the synth only. The arms are added BEFORE the shared "
        f"rune-crack fallback, and the fallback line is re-emitted unchanged (last), so the "
        f"{len(rec['fallthrough']) - 1} other relics that still fall through keep it and any other relic's arms row "
        f"on the same anchor composes in either order. Through the patched play() both arms reproduce their lab "
        f"candidates (worst {max(v for _, v in rec['arm_check']['chk']):.0e}; the root on two noise draws), "
        f"{len(rec['arm_check']['others'])} other voices are unchanged (worst "
        f"{max(v for _, v in rec['arm_check']['others']):.0e}), and ult/heartwood is no longer rune-crack. The "
        f"root arm is Tendril's `bindweed-root` body verbatim with only g changed ({fmt(T_G)} -> {fmt(R_['g'])}), "
        f"as its own id `heartwood-root` because Tendril's arm is not on this base. play() returns on its first "
        f"line with no audio context (every headless run), draws no random number and writes nothing the "
        f"simulation reads" + (f"; end to end the two voices through the patched page's own SFX.play equal the "
                               f"candidates (worst {max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    rows[1]["why"] = (
        f"One plain SFX.play in rootBlow on the line after T.rooted++ (the anchor re-emitted first, so a picture "
        f"row on the same line composes in either order): it can only sound where the sim has just rooted the "
        f"foe -- the window open, the foe alive (a killing blow returns above it). {wr['rootV']}/{wr['rooted']} "
        f"rooted blows voiced ({wr['fresh']} new holds and {wr['rooted'] - wr['fresh']} re-roots), "
        f"{wr['killV']} voices on {wr['kills']} killing blows, none from tickRootfast (the close is silent) and "
        f"none outside a window; {wr['castV']}/{wr['casts']} casts voiced by fireUlt's existing call; "
        f"{wr['same']}/{wr['fights']} fights identical and every other SFX call identical in order and opts; the "
        f"same row plus one sim write (the foe nudged 1e-9 on a root) comes back {wr['control_same']}/"
        f"{wr['fights']}{e2}.")
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float), encoding="utf-8")
    print("\n  NOTHING IS IN THE BUILD. The two rows are the edits; both were applied "
          "to the page's own code above, and as text to a copy of the page.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
