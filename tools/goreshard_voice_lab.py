#!/usr/bin/env python3
"""BLOODPRICE'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v114.

    python goreshard_voice_lab.py --game <a link carrying Goreshard's stage 5 (Bloodprice)> --rows rows.json
        [--also <the same stage 5 carried onto a newer tip>] [--peer-rows <another relic's rows_final.json>]

v81 s4 SOUND, every word of it: "Sound: cast -- a wet drawn-blade hiss, 0.4s;
a scaled blow -- the sword's strike voice pitched DOWN by the stack count
(bigger = lower); close -- nothing." The brief (v81 s5) has three stages; its
stage 3, "picture, voice, carry", is the batch's stage 6, and this is its
voice. Rick, for the batch's art and sound: "you pick i overrule". So this lab
does not offer a spread -- it renders three to five candidates a voice beside
CONTROLS that can come back wrong, prints the numbers each pick is made on,
and PICKS by a rule written in this file (`*_RULE`, `*_why`). He overrules
from one clip.

Goreshard's id is `oathwound` (the roster's one id / name mismatch, v81 "Why").

THE THREE EVENTS AND WHERE THEY FIRE (line numbers are sc-goreshard-b10.25's):
  cast   the bare id `ult/oathwound`, which `fireUlt` plays for every relic
         (16254, after the 0.08 s cast stop and the ult beat). Goreshard has
         NO arm today: it falls through to the shared rune-crack (measured
         below, to 1e-6, with every other relic that still does). The arm goes
         BEFORE that fallback, in a row of mode `before` whose anchor is the
         fallback line itself -- so the fallback is never touched, and another
         relic's row anchored there applies in either order. No sim line: the
         cast already plays it, once a cast.
  blow   a SCALED blow -- one Goreshard lands in the window on a body carrying
         Hemorrhage (`priceN` > 0, 14419: the stacks the blow was priced on,
         read before its own onHit) -- plays the ordinary `hit` voice with ONE
         plain number more, `price: priceN`. A window blow on a body with no
         Hemorrhage is x1 (1 + 0.30 x 0): not scaled, so it keeps the plain
         call. The row sits BEFORE resolveHit's hit-voice line (15136, mode
         `before`): `if (priceN > 0) SFX.play("hit", { dmg, crit, price:
         priceN }); else` -- and that line, Canopy's `bough` call, follows
         unchanged, so every other call is the old one. `priceN` is 0 whenever
         the window is shut and on every other relic (`ultPrice` is null).
         The hit arm grows one branch, `kind === "hit" && p.price`, placed
         BEFORE the plain arm (mode `before` on the plain arm's line): every
         call without `price` takes the arms below it, byte for byte.
  close  nothing (v81 s4: "close -- nothing"). Checked: no voice is added to
         tickPrice or anywhere else, and none plays at a close.
  Nothing here sets a hit stop, files a beat or writes a field.

THE DECLARED READINGS (words of v81 s4 turned into numbers; Code's picks,
Rick's to overrule):
  * "THE SWORD'S STRIKE VOICE": the hit arm as it plays this blow -- at the
    damage DEALT, so its weight, its level, its jitter and its crits are the
    blow's own ("size tracks damage": a priced blow that deals 22 is as heavy
    as any 22). The stack count moves only its PITCH, on top: every frequency
    of the strike (the crack's band, the body's sine and its glide, the
    crit's triangle) x 2^(-c n / 1200), `c` the candidate's interval a
    stack. (Canopy's bough rebuilt the HAMMER'S weight from the dealt damage
    because its design asked for "quieter" and a fourth down from the
    hammer; v81 asks for neither, and the weight at the dealt damage is
    already lower and heavier as the price grows -- the controls show by
    how much.)
  * "BY THE STACK COUNT": the number the blow was priced on, `priceN`
    (0-4), passed as `price`. The arm holds 4's voice above 4
    (`Math.min(p.price, 4)`): Hemorrhage's cap is 4 today (checked on the
    page), and open decision 3 (Bloodletting's cap of 8) must not be able
    to push the strike below what was measured here.
  * "0.4s": AUDIBLE 330-470 ms, GONE <= 470 ms (v100's +/-17.5%).
  * "A DRAWN-BLADE HISS" -- THE DRAW, every cast candidate's: a bandpass
    noise band (Q 5, a blade's scrape, narrower than air) RISING 2.6 -> 8 kHz
    in two overlapping strokes, 2.6 -> 4.6 kHz over 0.36 s (attack 80 ms)
    and, 0.16 s on, 4.1 -> 8 kHz (attack 100 ms), its length solved for
    AUDIBLE 400 ms. Rising: a blade drawn out, the scrape climbing to the
    tip. TWO strokes because A TOOLKIT FINDING (for CLAUDE.md 4.5, beside
    `_burst`'s 0.6 s and v111's burst tail): a single `_sweep` cannot be
    audible 0.4 s at a blow's level -- its ramps run to an absolute 1e-4, so
    it is audible (2% of its loudest) at most 0.58 x 34 / (20 log10(g /
    1e-4)) s: 0.27 s at the gain a blow's level needs (g ~0.6), 0.4 s only
    at g ~0.03. The band sits at 2.6-8 kHz because the scratch survey
    (stage6-voice/survey3.py) found every broad hiss under 2.5 kHz inside
    the tornado's woosh (0.86-0.94) and a 3 kHz highpass inside the wall
    tick (0.97).
  * "WET": a liquid under the hiss, how is the candidates: bubbles, a
    squelch, the retired wet slice's falling saws (the project's own "wet",
    Widowmaker's nova cast, retired by v106), drops. Each is level-matched so
    that the wet, rendered ALONE, is HEARD +9 dB over the score's p90 in its
    own third-octave (159-1270 Hz), and gated at +6 dB on its worst noise
    draw; and it must MOVE (a liquid glides). (Round 1 read the wet as a
    SHARE of the voice's power, 0.20 matched / 0.12 gated -- see THE ROUNDS.)

THE CONTROLS, and what each one is for:
  rune-crack   what Goreshard's cast plays TODAY; v88 published 0.608 / 450
               ms -- reproduced before anything new is quoted (with BAR
               0.364 / 300 ms and hit@11.6 0.443 / 80 ms). Played through the
               id `__fallback__` (no arm names it): on a tip that carries
               Unmaking's voices `ult/spellbreaker` is no longer rune-crack.
  hit@10.25    Goreshard's own blow (the blade is 10.25, stage 5): the level
               every voice is judged against, on its quietest / loudest draw
  wall         the commonest sound in a fight: the quiet voices' floor
  the school   the bloodsworn casts with a voice of their own (read off the
               page) -- and from `--also` / `--peer-rows`, Widowmaker's new
               inhale on the batch line
  the type     the greatsword casts with a voice of their own (read off the
               page) -- and from `--also` / `--peer-rows`, Lightkeeper's and
               Heartwood's
  woosh        `scour-woosh`, the tornado's: the other swept noise in the game
  death        the death voice: a priced blow pitched down must not read as one
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  DRY, STILL, HUM, FAINT, RUNECRACK   the draw alone / the draw not rising /
               the draw over a held note / BUBBLE with its wet 12 dB down /
               today's voice: each must fail its gate
  PLAIN, UP    the hit at the dealt damage (what a priced blow plays TODAY) /
               the stack count pitching it UP: each must fail its gate

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
    REG (cosine of 1/3-octave band amplitudes, 25 Hz-16 kHz, the median over
    noise draws), PITCH (FFT peak, Hann, zero-padded, parabolic), ENV-CORR
    (Pearson of two E50 curves in dB), CRACK (v99: the lag, 12.5 c steps,
    that best correlates two draw-averaged spectra at 500 Hz-8 kHz, where the
    strike's crack lives and its body does not), HEARD (a third-octave >= 200
    Hz over 100 ms against the score's p90 there, dB) and PHONE (the TOP
    high-passed at 200 Hz).
  * New here, each with a control that can come back wrong:
      HISS     the share of the voice's power at >= 2 kHz (RUNECRACK fails)
      DRAWN    the power centroid at 2-12 kHz of the first audible 100 ms
               and of the last, cents (STILL fails); SWELL, the >= 2 kHz
               1 ms envelope's 10 -> 90% rise, ms
      WET      the share of the voice's power at 150-1500 Hz (printed)
      WET-HEARD  the wet rendered alone: over the 100 ms around its band's
               loudest 50 ms, its best third-octave centred 159-1270 Hz
               against the score's p90 there, dB (DRY and FAINT fail)
      MOVING   on the wet rendered alone: the strongest peak at 150-1500 Hz
               in 20 ms windows (10 ms hop, Hann, zero-padded) whose band RMS
               is within 20 dB of the band's loudest window: p95 - p5 of
               those peaks, cents (a liquid glides; HUM, a held note, fails)
      CRACK3   v99's CRACK on 1/3-octave-smoothed spectra with the reference
               rendered on OTHER noise draws (round 2; PLAIN and UP fail)
      BODY     the blow's body: cents between the FFT peaks (25-400 Hz) of
               two voices' first 30 ms (v99's)
      SPREAD   the CRACK and BODY the damage roll moves the PLAIN hit by at a
               stack count: the hit at the dealt damage x 0.85 against x 1.15
               (the jitter's whole range, CONFIG.chaos.dmgJitter 0.30)
  * The cast candidates are LEVEL-MATCHED, not hand-set, so each pick is made
    on shape: the wet's gain puts WET-HEARD at +9 dB, the draw's second stroke's
    length puts AUDIBLE at 400 ms, and the gain puts TOP at the centre of its
    level window (five passes). The blow candidates are not levelled: their
    level IS the blow's. Constants are rounded BEFORE any measured render, so
    a shipped arm is bit-for-bit what was measured.

THE ROUNDS (each a run of this file; the logs in scratch stage6-voice/). The
rules were written before the first table. Every change after a table was
read is here, with its reason:
  ROUND 1 (r1.log, --no-wire). Reproduction PASS. NO cast and NO blow
    candidate passed.
    - BLOW, CRACK was blind here: v99's lag search on the SAME noise draws
      read SPREAD at 2 stacks as 10 c where the arithmetic says ~140, and
      SEMI at 1 stack as -6 c (shared noise fine structure pins the lag at
      0; crossing the list order changes nothing). Scratch survey5.py:
      DISJOINT draws and 1/3-octave windows track the arithmetic within ~25
      c (SEMI n1 -82 against -100, n2 -200 / -200) -> CRACK3.
    - BLOW, "REG > 0.80 with the plain hit" failed every candidate, SEMI at
      0.73: at this weight the register IS the pitch, so any drop heard over
      the dice leaves the 0.80 line. The gate contradicted "pitched down"
      and is printed, not gated. "REG <= 0.80 against the death voice":
      PLAIN, today's hit at the same damage, reads 0.85 itself (the hit and
      the death share the low register), so the gate would fail today's
      voice; printed, not gated, and "not a death" is read as NOT A BOOM:
      AUDIBLE at 4 stacks, crit or not, <= 1.25x the plain hit's (the
      death voice is 620 ms, the hit 80). SEMI prints 0.97 against the
      death voice (PLAIN 0.85, TONE 0.69) -- declared, for Rick's ear.
    - BLOW TIEBREAK: "the largest drop" was held down only by the REG-with-
      plain gate; without it, it takes the octave. Changed to the SMALLEST
      drop at 4 stacks (to 50 c) that clears every gate -- the least change
      that is still heard over the dice keeps it "the sword's strike
      voice". A change made after a table was read: recorded as such; the
      runner-up is one constant (`c`).
    - CAST: BUBBLE, SLICK and DRIP sat 0.80-0.83 against the woosh at WET
      0.20; SQUELCH's worst-draw share 0.10. Scratch survey6.py: a wet heard
      +6..+10 dB over the score's p90 in its band takes only 0.04-0.12 of
      the power, and at 0.12 the tonal wets already sit 0.78-0.80 against
      the woosh. So the SHARE was the wrong reading of "wet": WET-HEARD
      (+6 dB gated, +9 matched) replaces it.
  ROUND 2 (r2.log). The blow resolved: CRACK3 tracks; SEMI, TONE, THIRD pass;
    TAPE out (audible 1.79x: a boom), BODY out (its crack does not move);
    PLAIN and UP fail as they must -> SEMI. The cast: the HUM control PASSED
    (MOVING 1373 c -- read on the whole voice, the peak search landed on the
    draw's noise skirt, which wanders), and SQUELCH / DRIP read wet-heard
    3.3 / 4.9 dB on their worst draw for the same reason -> WET-HEARD and
    MOVING are read on the wet rendered ALONE (`part="wet"`), and a FAINT
    control (BUBBLE's wet 12 dB down) must fail WET-HEARD.
  ROUND 3 (r3.log). Every control fails on the gate it is for (DRY, STILL,
    HUM, FAINT, RUNECRACK; PLAIN, UP). SQUELCH out (wet heard +3.3 dB);
    BUBBLE, SLICK, DRIP pass; DRIP the most distinct register (0.71 at
    most, against the woosh). The picks stand from here.
  FINAL (final.log): the same rules with the wire, end to end, the batch
    line's newest link (`--also`) and the other relics' voice rows
    (`--peer-rows`). No rule changed.

THE PICKS:
  cast   4 DRIP -- the declared draw (a Q 5 scrape rising 2.6 -> 8 kHz in two
         strokes) with three drops off the blade as it clears (sines at
         0.17 / 0.25 / 0.31 s, 760 / 880 / 1010 Hz, each chirping up 1.5x
         over 80 ms). g 0.5095, kw 0.03921, second stroke 0.49 s.
  blow   1 SEMI -- the plain strike at the damage dealt, every frequency down
         a semitone a stack (a major third at 4).
  close  nothing.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the two Sfx rows (the priced-blow branch before the plain hit arm; the
    cast arm before the rune-crack fallback) are applied to
    `Sfx.prototype.play`'s own source and rendered: the cast arm must
    reproduce its candidate to TOL on two noise draws and the priced branch
    its candidate at every stack count 1-4 x jitter x crit; every other voice
    through the patched play (the hit at five weights with and without a
    crit, Canopy's bough at three, spark x9, wall, death, clank x2, seal,
    nova, hex-snap, fork, vine x4, loose x3, aegis x2, scour x4, a hit whose
    `price` is 0, and every ult id and kind the page's play() names) must be
    unchanged; `ult/oathwound` must NOT be rune-crack any more and
    `__fallback__` must still be;
  * the resolveHit row is applied to the prototype's own source and run on
    real fights beside the unpatched one: every fight identical (over,
    clock, both fighters' hp, positions, velocities, stacks, the winner,
    both priceTallies, and a digest of positions, velocities and hp on EVERY
    step) and every other voice call identical in order, kind and opts (the
    hit's opts with `price` taken out); every window blow Goreshard lands
    on a body with Hemorrhage carries `price` = the stacks it was priced on
    (read off priceTally's own blows / stk, which resolveHit counts) and no
    other call carries it (her blows outside the window, her x1 window
    blows, the foe's blows, a ward's shatter -- its own `hit` inside
    resolveHit's call, told apart by its caller); one cast voice per cast
    (from `fireUlt`), no other Goreshard voice anywhere and nothing played
    inside tickPrice; the unpatched page plays no `price`. The same row plus
    ONE sim write (the struck body nudged 1e-9 on a priced blow) must come
    back NOT identical, or "identical" proves nothing. (The Sfx rows cannot
    reach the simulation at all: `play` returns on its first line with no
    audio context, which is every headless run.)
  * END TO END: the rows applied AS TEXT (the orchestrator's semantics:
    replace = code, after = anchor + code, before = code + anchor) to a copy
    of the game file (in a temp folder, never the repo), loaded in a fresh
    browser after the first is closed: the page loads clean, its own
    SFX.play renders the arms to the lab's text and every other voice to the
    original page's, and its fights are identical to the original page's,
    with the voice counts above. With `--also <link>`, the same, there, and
    the picked cast's register against THAT page's bloodsworn and greatsword
    casts is gated too.
  * WITH OTHER RELICS' ROWS (`--peer-rows`): each peer's Sfx rows and these
    applied to play()'s source in both orders render every arm of both
    identically; the cast's register against a school or type peer's cast
    is gated, the rest printed.
  All anchors must occur exactly once in the game file; no row replaces its
  anchor, so a later relic's row -- or the picture's -- anchored on the same
  line still applies, in either order. Every row is ASCII.

Writes wavs to 05-reference/v114/goreshard-*.wav at RAW level (gitignored).
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
    env, env_corr, fmt, pcm, pitch, write_wav)
from ironwood_voice_lab import RENDER_JS  # noqa: E402
from bindweed_voice_lab import mreg  # noqa: E402
from ironhail_voice_lab import PHONE_HZ, bed_p90, phone  # noqa: E402
from lightkeeper_voice_lab import _wrap  # noqa: E402

HERE = pathlib.Path(__file__).parent
ME = "oathwound"                          # Goreshard's id
NAME = "Goreshard"
FALLBACK = "__fallback__"                 # an id no arm names: rune-crack, after these rows too
BLADE = 10.25                             # Goreshard's dmg (stage 5)
PER_STACK = 0.3                           # w.ult.perStack (v81; checked on the page)
CAP = 4                                   # STATUS.hemorrhage.maxStacks (checked on the page)
CRIT_MUL = 2.1                            # CONFIG.chaos.critMul (checked)
JIT = [0.85, 1.0, 1.15]                   # CONFIG.chaos.dmgJitter 0.30: the roll's whole range
TOL = 1e-5                                # reproduction / transcription (-100 dB)
SCHOOL_AFF = "bloodsworn"
TYPE_SHAPE = "greatsword"
PEER_SCHOOL = {"widowmaker": "the bloodsworn twinblade (v106; the batch line)"}
PEER_TYPE = {"lightkeeper": "the vigil greatsword (v107; the batch line)",
             "heartwood": "the verdant greatsword (v113; in flight)"}
AUD_TGT = 400.0                           # "0.4s", ms
WET_TGT = 9.0                             # round 2: the wet level-matched to be HEARD +9 dB over the score
WET_GATE = 6.0                            # ... and gated at the batch's +6 dB, on the worst draw
WET_BAND = (150.0, 1500.0)
OTHER_SEEDS = [(0x2545F491 * (k + 19)) & 0xffffffff or 1 for k in range(12)]   # round 2: CRACK3's reference draws
HISS_LO = 2000.0
Q_DRAW = 5
DRAW = [(0.0, 2600, 4600, 0.36, 0.08), (0.16, 4100, 8000, None, 0.10)]   # s, f0, f1, dur (None: solved), atk

# the plain hit arm, as the page has it (checked against play()'s own source):
# the priced branch is this arithmetic with every frequency x k
PLAIN_ARM = [
    'const w = clamp((p.dmg || 10) / 45, 0.12, 1);          // 0..1 weight',
    'this._burst(t, { freq: 2600 - 1500*w, q: 1.1, gain: 0.16 + 0.20*w, dur: 0.06 + 0.06*w });',
    'this._tone (t, { freq: 190 - 90*w, to: 46, gain: 0.22 + 0.26*w, dur: 0.11 + 0.13*w, type:"sine" });',
    'if (p.crit) this._tone(t, { freq: 1500, to: 520, gain: 0.16, dur: 0.16, type:"triangle" });']


def _refuse(src, what):
    bad = re.findall(r"Math\.random|\brng\b|spawnFx|ultFx", src)
    if bad:
        raise SystemExit(f"REFUSING: the {what} names {bad} -- a voice draws no random number "
                         "and touches no simulation slot.")


def peer_name(pf):
    """A peer rows file's relic: `<scratch>/batch/<relic>/stage6-voice/rows_final.json` -> "relic"."""
    p_ = pathlib.Path(pf).parent
    return (p_.parent.name if p_.name.startswith("stage") else p_.name).lower()


def as_replace(anchor, mode, code):
    """A row as the [anchor, replacement] pair its mode means (the orchestrator's
    semantics: replace = code, after = anchor + code, before = code + anchor)."""
    return [anchor, {"replace": code, "after": anchor + code, "before": code + anchor}[mode]]


def sig4(v):
    return float(f"{v:.4g}")


# =============================================================== THE CAST ===
# "a wet drawn-blade hiss, 0.4s". Every candidate carries the declared draw
# (DRAW); they differ in what the wet IS.
CAST_CANDIDATES = [
    ("1 BUBBLE", dict(wet="bubble"),
     "bubbles under the draw: sine chirps rising 1.6x in 28 ms, 434-806 Hz, every ~34 ms (+/-20%)"),
    ("2 SQUELCH", dict(wet="squelch"),
     "a squelch under the draw: a resonant noise band (Q 8) sliding 300 -> 900 Hz"),
    ("3 SLICK", dict(wet="slick"),
     "the retired wet slice's saws under the draw: sawtooths falling 660 -> 240 and 480 -> 180 Hz"),
    ("4 DRIP", dict(wet="drip"),
     "drops off the blade as it clears: three sines chirping up 1.5x over 80 ms, 760 / 880 / 1010 Hz"),
]
WET = {
    "bubble": ["for (let s = 0.03, k = 0; s < 0.36; k++){",
               "  const f = 620 * (1 + 0.3 * Math.sin(k * 2.4));",
               '  this._tone(t + s, { freq: f, to: f * 1.6, gain: g * kw, dur: 0.028, type:"sine" });',
               "  s += 0.034 * (1 + 0.2 * Math.sin(k * 1.7));",
               "}"],
    "squelch": ['this._sweep(t + 0.02, { f0: 300, f1: 900, q: 8, gain: g * kw, dur: 0.42, atk: 0.12, type:"bandpass" });'],
    "slick": ['this._tone(t + 0.03, { freq: 660, to: 240, gain: g * kw, dur: 0.34, type:"sawtooth" });',
              'this._tone(t + 0.12, { freq: 480, to: 180, gain: g * kw * 0.7, dur: 0.30, type:"sawtooth" });'],
    "drip": ["for (const [s, f] of [[0.17, 760], [0.25, 880], [0.31, 1010]])",
             '  this._tone(t + s, { freq: f, to: f * 1.5, gain: g * kw, dur: 0.08, type:"sine" });'],
    "hum": ['this._tone(t + 0.03, { freq: 620, gain: g * kw, dur: 0.40, type:"sine" });'],
}


def draw_lines(D2, still=False):
    L = []
    for s, f0, f1, d, atk in DRAW:
        tt = "t" if s == 0 else f"t + {fmt(s)}"
        f0_, f1_ = (DRAW[0][1], DRAW[0][1]) if still else (f0, f1)
        L.append(f'this._sweep({tt}, {{ f0: {f0_}, f1: {f1_}, q: {Q_DRAW}, gain: g, '
                 f'dur: {fmt(D2 if d is None else d)}, atk: {fmt(atk)}, type:"bandpass" }});')
    return L


def cast_body(sp, g, kw, D2, ind=10, part="both"):
    """The cast arm's body. `sp["wet"]` None is the DRY control; `still` the
    STILL control (the draw's bands held). `part` "wet" renders the wet alone
    (round 3: what WET-HEARD and MOVING read)."""
    wet = sp.get("wet")
    L = [f"const g = {fmt(g)}" + (f", kw = {fmt(kw)};" if wet else ";")]
    if part == "both":
        L += draw_lines(D2, still=sp.get("still", False))
    if wet:
        L += WET[wet]
    return "\n".join(" " * ind + l_ for l_ in L)


# ======================================================= THE PRICED BLOW ===
# "the sword's strike voice pitched DOWN by the stack count (bigger = lower)".
# The plain arm's arithmetic verbatim at the dealt damage, every frequency x k,
# k = 2^(-c n / 1200). `crack` False leaves the crack (and the crit) alone;
# `tape` also stretches every length by 1 / k.
BLOW_CANDIDATES = [
    ("1 SEMI", dict(c=100, crack=True, tape=False),
     "every frequency of the strike down a semitone a stack (4 stacks: a major third)"),
    ("2 TONE", dict(c=200, crack=True, tape=False),
     "every frequency down a whole tone a stack (4 stacks: a minor sixth)"),
    ("3 THIRD", dict(c=300, crack=True, tape=False),
     "every frequency down a minor third a stack (4 stacks: an octave)"),
    ("4 TAPE", dict(c=200, crack=True, tape=True),
     "TONE slowed like tape: every frequency down a whole tone a stack and every length x 1/k"),
    ("5 BODY", dict(c=200, crack=False, tape=False),
     "only the strike's sine body down a whole tone a stack; its crack (and crit) unchanged"),
]


def blow_body(sp, ind=8):
    sign = "" if sp.get("up") else "-"
    kc = " * k" if sp["crack"] else ""
    r = " / k" if sp["tape"] else ""
    L = [f"const w = clamp((p.dmg || 10) / 45, 0.12, 1), n = Math.min(p.price, {CAP}), "
         f"k = Math.pow(2, {sign}n * {fmt(sp['c'])} / 1200);",
         f"this._burst(t, {{ freq: (2600 - 1500*w){kc}, q: 1.1, gain: 0.16 + 0.20*w, dur: (0.06 + 0.06*w){r} }});",
         f"this._tone (t, {{ freq: (190 - 90*w) * k, to: 46 * k, gain: 0.22 + 0.26*w, dur: (0.11 + 0.13*w){r}, "
         f"type:\"sine\" }});",
         f"if (p.crit) this._tone(t, {{ freq: 1500{kc}, to: 520{kc}, gain: 0.16, dur: 0.16{r}, type:\"triangle\" }});"]
    return "\n".join(" " * ind + l_ for l_ in L)


# ================================================================ THE ROWS ==
SFX_ANCHOR = '        } else {                                        // rune-crack'
HIT_ANCHOR = '      else if (kind === "hit"){'
RH_ANCHOR = '    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });'

RH_CODE = '''    /* BLOODPRICE'S SCALED BLOW (v81 s4: "a scaled blow -- the sword's strike
       voice pitched DOWN by the stack count (bigger = lower)"): ONE plain
       number more, `price`, the Hemorrhage stacks this blow was priced on
       (`priceN`, read above, before its own onHit), and only when it is > 0:
       a window blow on a body with no Hemorrhage is x1 and keeps the plain
       call. `priceN` is 0 whenever the window is shut and on every other
       relic, so they take the `else` -- the line below, Canopy's call,
       unchanged. `dmg` stays what was dealt. Reads priceN, dmg and crit;
       writes nothing. Presentation only (goreshard_voice_lab: fights
       identical). */
    if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });
    else
'''

# the sim-write control: the same row with the struck body nudged 1e-9 on a priced blow
RH_CODE_BAD = RH_CODE.replace(
    '    if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });',
    '    if (priceN > 0){ foe.vx += 1e-9; SFX.play("hit", { dmg, crit, price: priceN }); }', 1)
assert RH_CODE_BAD != RH_CODE
_refuse(RH_CODE, "resolveHit row")
assert RH_ANCHOR not in RH_CODE and RH_CODE.isascii() and RH_CODE.endswith("\n")


def _arm_head(w, tag):
    s = f'        }} else if (w === "{w}"){{'
    return s + " " * max(1, 56 - len(s)) + "// " + tag


def hit_row_code(Bl, info):
    c = _wrap([
        f'BLOODPRICE\'S SCALED BLOW -- v81 s4: "a scaled blow -- the sword\'s strike voice pitched DOWN by the '
        f'stack count (bigger = lower)". {Bl["name"].split(maxsplit=1)[1]}, of {info["n_blow"]}, picked on the '
        f'numbers by `goreshard_voice_lab.py` under Rick\'s "you pick i overrule" (v114). `resolveHit` adds '
        f'`price` (the Hemorrhage stacks the blow was priced on, 1-4) only to a scaled Goreshard blow, so every '
        f'other call takes the arms below, byte for byte.',
        f"The strike as the plain arm plays this blow -- at the damage dealt, so its weight, level, jitter and "
        f"crits are the blow's -- with every frequency x 2^(-{info['c']:g} n / 1200): {info['what']}. Against "
        f"the plain hit at the same damage it falls {info['crack']} cents on the crack and {info['body']} on "
        f"the body at 1-4 stacks; at 2 and 4 (the counts a window has) that is {info['over2']} and "
        f"{info['over4']} x what the damage roll moves the plain hit by. Its peak within {info['pk']:.1f} dB of "
        f"the plain hit's; register {info['reg']:.2f} with it at 4 stacks (still that voice), "
        f"{info['death']:.2f} against the death voice. Held at 4's voice above 4 (Hemorrhage's cap)."], 8)
    return (f'      else if (kind === "hit" && p.price){{\n{c}\n{blow_body(Bl["sp"])}\n      }}\n')


def cast_arm_code(Ca, info):
    c = _wrap([
        f'GORESHARD\'S CAST, BLOODPRICE -- v81 s4: "cast -- a wet drawn-blade hiss, 0.4s". '
        f'{Ca["name"].split(maxsplit=1)[1]}, of {info["n_cast"]}, picked on the numbers by '
        f'`goreshard_voice_lab.py` under Rick\'s "you pick i overrule" (v114). Goreshard had no arm and fell '
        f'through to rune-crack, which {info["n_rc"]} other relics on its stage-5 link still use, so this ADDS '
        f'an arm before that fallback and leaves it alone. The beam it replaces had no voice of its own.',
        f"The draw: a scrape (bandpass noise, Q 5) rising 2.6 -> 8 kHz in two overlapping strokes -- a single "
        f"`_sweep` runs to an absolute 1e-4 and cannot be audible 0.4 s at a blow's level -- climbing "
        f"{info['drawn']:+.0f} cents from its first 100 ms to its last and swelling in {info['swell']:.0f} ms "
        f"(drawn, not struck); {info['hiss']:.2f} of its power at 2 kHz and up. Under it, {info['what']}: "
        f"{info['wet']:.2f} of the power at 150-1500 Hz, gliding over {info['moving']:.0f} cents. Audible "
        f"{info['aud']:.0f} ms; its top {info['top_db']:+.1f} dB re Goreshard's blow, heard {info['heard']:+.1f} "
        f"dB over the score. Register at most {info['reg']:.2f} ({info['reg_k']}) against rune-crack, the "
        f"bloodsworn and greatsword casts, the tornado's woosh, the blow and the death voice{info['peers']}."],
        10)
    return f'{_arm_head(ME, "the blade drawn, wet")}\n{c}\n{cast_body(Ca["sp"], Ca["g"], Ca["kw"], Ca["D2"])}\n'


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
  for (const [k, kind, p] of [["cast", "ult", { w: ME }], ["priced", "hit", { dmg: 23, crit: false, price: 4 }],
                              ["hit", "hit", { dmg: 10, crit: false }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, kind, p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The per-step digest and the fighter snapshot, shared by WIRE_JS and FIGHTS_JS;
# and the voice log every run keeps (the blow's OWN voice is the one resolveHit
# plays itself: a ward that shatters under it plays its own `hit` from inside
# the call, from `shatter`, and is not a blow).
COMMON_JS = r"""
  const F64 = new Float64Array(1), U32 = new Uint32Array(F64.buffer);
  const mix = (h, v) => { F64[0] = +v; h = Math.imul(h ^ U32[0], 16777619) >>> 0;
                          return Math.imul(h ^ U32[1], 16777619) >>> 0; };
  const fr = (x) => [x.hp, x.x, x.y, x.vx, x.vy, x.alive, x.stun, x.charge, x.stacks("hemorrhage")];
  const dig = (h, m) => { for (const x of [m.a, m.b])
    for (const v of [x.x, x.y, x.vx, x.vy, x.hp]) h = mix(h, v); return h; };
  const caller = () => ((new Error()).stack.split("\n")[3] || "");
  const tally = (f) => f.priceTally ? [f.priceTally.blows, f.priceTally.stk] : [0, 0];
"""

# The resolveHit row, applied to the real prototype and run beside the original;
# the survey of Bloodprice's blows comes out of the same runs.
RUN_JS = r"""
  const run = (P, S, ME, side, fid, sd, implH, implT, DT) => {
    const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    let step = 0, h = 2166136261, rh = null, depth = 0, inT = 0, maxDepth = 0;
    const other = [], mine = [], blows = [], bad = [];
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const w = kind === "ult" && p && typeof p.w === "string" ? p.w : "";
      if (inT) bad.push(["a voice inside tickPrice", kind, w, step]);
      if (w === ME || w.startsWith(ME + "-")) mine.push([step, w, Object.keys(p).sort().join(","), rh ? 1 : 0]);
      else {
        const q = Object.assign({}, p || {}); const pr = q.price; delete q.price;
        other.push([step, kind, JSON.stringify(q)]);
        if (kind === "hit" && rh){
          const own = /resolveHit/.test(caller());
          rh.voices.push([own ? 1 : 0, pr === undefined ? null : pr]);
        } else if (pr !== undefined) bad.push(["price on a call outside resolveHit", kind, step]);
      }
      return op.call(this, kind, p); };
    const oH = P.resolveHit, oT = P.tickPrice;
    P.resolveHit = function(...args){
      const self = args[0], t0 = tally(f), prev = rh; rh = { voices: [] }; depth++;
      maxDepth = Math.max(maxDepth, depth);
      try { return implH.apply(this, args); }
      finally {
        depth--; const cur = rh; rh = prev; const t1 = tally(f);
        const own = cur.voices.filter(v => v[0]);
        blows.push([step, self === f ? 1 : 0, t1[0] - t0[0], t1[1] - t0[1], own.length,
                    own.length ? own[0][1] : null, cur.voices.filter(v => !v[0] && v[1] !== null).length,
                    cur.voices.filter(v => !v[0]).length]);
      } };
    P.tickPrice = function(dt){ inT++; try { return implT.call(this, dt); } finally { inT--; } };
    let n = 0;
    try { while (!m.over && n < 170 / DT){ step = n; m.step(DT); n++; h = dig(h, m); } }
    finally { P.resolveHit = oH; P.tickPrice = oT; if (had) S.play = op; else delete S.play; }
    const T = f.priceTally || {};
    return { sum: JSON.stringify([m.over, m.t, fr(m.a), fr(m.b), m.winner ? m.winner.w.id : null,
                                  m.a.priceTally || null, m.b.priceTally || null, h]),
             other: JSON.stringify(other), mine, blows, bad, casts: T.casts || 0, maxDepth };
  };
  /* the blows a run logged, judged: [step, mine, dBlows, dStk, ownVoices, price, strayPriced, shatters] */
  const judge = (R, wired) => {
    const c = { win: 0, win0: 0, priced: 0, pricedV: 0, outside: 0, foeB: 0, shat: 0, hist: [0, 0, 0, 0, 0, 0],
                noVoice: 0, bad: [] };
    for (const [st, mineB, dB, dS, nOwn, pr, stray, sh] of R.blows){
      c.shat += sh;
      if (stray) c.bad.push(["a price on a shatter's hit", st]);
      if (nOwn > 1) c.bad.push(["two own hit voices in one resolveHit", st]);
      if (mineB && dB === 1){
        c.win++; c.hist[Math.min(5, Math.max(0, Math.round(dS)))]++;
        const want = (wired && dS > 0) ? dS : null;
        if (dS > 0) c.priced++; else c.win0++;
        if (!nOwn){ c.noVoice++; continue; }
        if (pr !== want) c.bad.push(["a window blow's price", dS, "voiced", pr, st]);
        else if (pr !== null) c.pricedV++;
      } else {
        if (dB !== 0) c.bad.push(["the tally moved on a blow that is not hers", dB, st]);
        if (mineB) c.outside++; else c.foeB++;
        if (pr !== null) c.bad.push(["a price outside the window or on a foe's blow", pr, st]);
      }
    }
    const castV = R.mine.filter(v => v[1] === ME && v[2] === "w" && !v[3]).length;
    const stray = R.mine.filter(v => v[1] !== ME || v[2] !== "w" || v[3]).length;
    if (castV !== R.casts) c.bad.push(["cast voices vs casts", castV, R.casts]);
    if (stray) c.bad.push(["a Goreshard voice that is not the cast", stray]);
    for (const b of R.bad) c.bad.push(b);
    if (R.maxDepth > 1) c.bad.push(["a resolveHit inside a resolveHit", R.maxDepth]);
    c.castV = castV; c.casts = R.casts;
    return c;
  };
"""

WIRE_JS = r"""([seeds, rhRow, ME]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
""" + COMMON_JS + RUN_JS + r"""
  const oH = P.resolveHit, oT = P.tickPrice;
  if (!oT) return { err: "no tickPrice -- not a Bloodprice build" };
  let src = oH.toString();
  { const at = src.split(rhRow[0]).length - 1;
    if (at !== 1) return { err: `the resolveHit anchor occurs ${at} times in resolveHit()` };
    src = src.replace(rhRow[0], () => rhRow[1]); }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  for (const nm of ["STATUS", "CONFIG", "AFFINITIES", "clamp"])
    if ((0, eval)("typeof " + nm) === "undefined") return { err: nm + " is not reachable from a patched resolveHit" };
  const pH = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== ME);
  let fights = 0, same = 0, otherSame = 0; const diff = [], bad = [];
  const tot = { win: 0, win0: 0, priced: 0, pricedV: 0, outside: 0, foeB: 0, shat: 0, noVoice: 0, casts: 0, castV: 0,
                hist: [0, 0, 0, 0, 0, 0] };
  const pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(P, S, ME, side, fid, sd, oH, oT, DT), B = run(P, S, ME, side, fid, sd, pH, oT, DT);
    fights++;
    if (A.sum === B.sum) same++; else diff.push([side, fid, sd]);
    if (A.other === B.other) otherSame++;
    const cA = judge(A, false), cB = judge(B, true);
    for (const b of cA.bad) bad.push([fid, sd, "UNPATCHED", ...b]);
    for (const b of cB.bad) bad.push([fid, sd, ...b]);
    for (const k of ["win", "win0", "priced", "pricedV", "outside", "foeB", "shat", "noVoice", "casts", "castV"])
      tot[k] += cB[k];
    for (let i = 0; i < 6; i++) tot.hist[i] += cB.hist[i];
    if (cB.pricedV) pick.push({ side, foe: fid, seed: sd, priced: cB.pricedV });
  }
  return { fights, same, otherSame, diff: diff.slice(0, 4), tot, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the row, every SFX call recorded with its match
# time and what it is.
RECORD_JS = r"""([side, fid, sd, rhRow, ME]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
""" + COMMON_JS + r"""
  const oH = P.resolveHit;
  const pH = (0, eval)("(function " + oH.toString().replace(rhRow[0], () => rhRow[1]) + ")");
  const m = side ? new AC.Match(fid, ME, sd) : new AC.Match(ME, fid, sd);
  const f = side ? m.b : m.a;
  const ev = [], wins = []; let rh = null, W = null;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const q = JSON.parse(JSON.stringify(p || {}));
    const own = kind === "hit" && !!rh && /resolveHit/.test(caller());
    const tag = (kind === "ult" && q.w === ME) ? "cast" : (kind === "hit" && q.price !== undefined) ? "priced"
              : (own && rh === f) ? "blow" : "";
    ev.push([m.t, kind, q, tag]);
    return op.call(this, kind, p); };
  P.resolveHit = function(...args){ const prev = rh; rh = args[0];
    try { return pH.apply(this, args); } finally { rh = prev; } };
  try { let n = 0; while (!m.over && n < 170 / DT){
          const Z0 = f.ultPrice; m.step(DT); n++;
          if (f.ultPrice && f.ultPrice !== Z0){ W = { cast: m.t, close: null }; wins.push(W); }
          if (!f.ultPrice && Z0 && W) W.close = m.t; } }
  finally { P.resolveHit = oH; if (had) S.play = op; else delete S.play; }
  return { ev, wins };
}"""

# End to end: the page's OWN code (the rows applied as text, or not at all).
FIGHTS_JS = r"""([seeds, ME]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.SFX, P = AC.Match.prototype;
""" + COMMON_JS + RUN_JS + r"""
  if (!P.tickPrice) return { err: "no tickPrice" };
  const oH = P.resolveHit, oT = P.tickPrice, res = [];
  const wired = (0, eval)("SFX").play.toString().includes("p.price");
  for (const sd of seeds) for (const fid of AC.WEAPONS.map(w => w.id).filter(i => i !== ME)) for (const side of [0, 1]){
    const R = run(P, S, ME, side, fid, sd, oH, oT, DT);
    const c = judge(R, P.resolveHit.toString().includes("price: priceN"));
    res.push({ key: [sd, fid, side].join(":"), sum: R.sum, other: R.other, casts: c.casts, castV: c.castV,
               priced: c.priced, pricedV: c.pricedV, win: c.win, bad: c.bad.length, bad0: c.bad.slice(0, 2) });
  }
  return { res, wired };
}"""


# ============================================================ MEASURING ====
def _np():
    import numpy as np
    return np


def seg(x, a, b):
    return x[int((T0 + a) * SR):int((T0 + b) * SR)]


def share(x, lo, hi):
    """The share of the voice's power (from t = 1.0) in [lo, hi) Hz."""
    np = _np()
    y = x[int(T0 * SR):]
    P = np.abs(np.fft.rfft(y)) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / SR)
    return float(P[(fr >= lo) & (fr < hi)].sum() / max(P.sum(), 1e-30))


def cen_band(x, a, b, lo, hi):
    """The power centroid at [lo, hi] Hz over [a, b] s after the event."""
    np = _np()
    y = seg(x, a, b)
    P = np.abs(np.fft.rfft(y * np.hanning(len(y)), 1 << 15)) ** 2
    fr = np.fft.rfftfreq(1 << 15, 1 / SR)
    m = (fr >= lo) & (fr <= hi)
    return float((P[m] * fr[m]).sum() / max(P[m].sum(), 1e-30))


def hp_env(x, fc, lo_=None):
    """The voice from t = 1.0 band-limited (FFT) to [fc, lo_) Hz: its 1 ms RMS at a 1 ms hop."""
    np = _np()
    y = x[int(T0 * SR):]
    Y = np.fft.rfft(y); fy = np.fft.rfftfreq(len(y), 1 / SR)
    Y[fy < fc] = 0
    if lo_:
        Y[fy >= lo_] = 0
    h = np.fft.irfft(Y, len(y))
    H = int(0.001 * SR); n = len(h) // H
    return h, np.sqrt((h[:n * H].reshape(n, H) ** 2).mean(axis=1))


def drawn(x, B):
    """DRAWN: cents from the 2-12 kHz centroid of the first audible 100 ms to that of the last."""
    a0 = B["a0"] / 1000; a1 = B["gone"] / 1000
    return cents(cen_band(x, a1 - 0.1, a1, HISS_LO, 12000), cen_band(x, a0, a0 + 0.1, HISS_LO, 12000))


def swell(x):
    """SWELL: the >= 2 kHz 1 ms envelope's 10 -> 90% rise, ms."""
    np = _np()
    _h, e = hp_env(x, HISS_LO)
    m1 = e.max()
    return float(np.argmax(e > 0.9 * m1) - np.argmax(e > 0.1 * m1))


def moving(x):
    """MOVING: p95 - p5 (cents) of the strongest 150-1500 Hz peak in 20 ms
    windows (10 ms hop) whose band RMS is within 20 dB of the band's loudest."""
    np = _np()
    h, _e = hp_env(x, WET_BAND[0], WET_BAND[1])
    W = int(0.02 * SR); H = int(0.01 * SR); NF = 1 << 14
    fr = np.fft.rfftfreq(NF, 1 / SR); m = np.nonzero((fr >= WET_BAND[0]) & (fr <= WET_BAND[1]))[0]
    rms, pk = [], []
    hw = np.hanning(W)
    for i in range(0, len(h) - W, H):
        s_ = h[i:i + W]
        rms.append(float(np.sqrt((s_ ** 2).mean())))
        X = np.abs(np.fft.rfft(s_ * hw, NF))
        pk.append(float(fr[m[int(np.argmax(X[m]))]]))
    rms = np.array(rms); pk = np.array(pk)
    k = rms >= rms.max() * 10 ** (-20 / 20)
    if k.sum() < 2:
        return 0.0
    c_ = 1200 * np.log2(pk[k] / pk[k].min())
    return float(np.percentile(c_, 95) - np.percentile(c_, 5))


def heard_top(x, p90, lo=PHONE_HZ, hi=12000.0):
    """HEARD over the voice's loudest 100 ms (centred on its TOP): its best
    third-octave >= 200 Hz against the score's p90 there, dB, and where."""
    B = basic(x)
    a = max(0.0, B["top_at"] - 0.05)
    b_ = bands(seg(x, a, a + 0.1))
    best = max(((b_[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if lo <= fc <= hi))
    return db(best[0]), best[1]


def avgspec3(xs, lo_f=500.0, hi_f=8000.0, secs=0.4):
    """v99's avgspec with 1/3-octave windows (round 2): the power spectra of a
    voice's noise draws averaged, each point the mean power in a 1/3-octave
    window on a 1/96-octave grid, in dB."""
    np = _np()
    NF = 1 << 17
    fr = np.fft.rfftfreq(NF, 1 / SR)
    P = 0.0
    for x in xs:
        y = x[int(T0 * SR):int((T0 + secs) * SR)]
        P = P + np.abs(np.fft.rfft(y, NF)) ** 2
    cs = np.concatenate([[0.0], np.cumsum(P)])
    grid = lo_f * 2 ** (np.arange(0, 96 * math.log2(hi_f / lo_f) + 1) / 96)
    lo = np.searchsorted(fr, grid * 2 ** (-1 / 6)); hi = np.searchsorted(fr, grid * 2 ** (1 / 6))
    out = (cs[hi] - cs[lo]) / np.maximum(hi - lo, 1)
    return 10 * np.log10(out + out.max() * 1e-9)


def crack3(xa, xb):
    """CRACK3 (round 2): cents that voice a's noise crack sits from voice b's --
    v99's lag search (12.5 c steps, parabolic, 500 Hz-8 kHz) on 1/3-octave
    spectra, `xb` rendered on OTHER noise draws than `xa`. Negative: a is lower."""
    np = _np()
    A, B = avgspec3(xa), avgspec3(xb)
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


def wet_heard(x, p90):
    """WET-HEARD (round 2): over the 100 ms centred on the loudest 50 ms of the
    voice's 150-1500 Hz band, its best third-octave centred 159-1270 Hz against
    the score's p90 there, dB, and where."""
    np = _np()
    h, _e = hp_env(x, WET_BAND[0], WET_BAND[1])
    r50, c50 = env(h, 0.05)
    a = max(0.0, float(c50[int(np.argmax(r50))]) - 0.05)
    b_ = bands(seg(x, a, a + 0.1))
    best = max(((b_[i] / max(p90[i], 1e-12), fc) for i, fc in enumerate(BANDS) if 150 <= fc <= 1300))
    return db(best[0]), best[1]


def body_c(x, ref):
    return cents(pitch(x, T0, T0 + 0.03, lo=25, hi=400), pitch(ref, T0, T0 + 0.03, lo=25, hi=400))


# =============================================================== PICKING ===
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v81 s4 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'0.4s': AUDIBLE 330-470 ms and GONE <= 470 ms on every noise draw; 'hiss': HISS (the share of the power "
    "at >= 2 kHz) >= 0.50 on every draw -- the hiss carries it; 'drawn-blade': the hiss band RISES (DRAWN >= +600 "
    "cents, first audible 100 ms to last: a blade drawn out, the scrape climbing to the tip) and SWELLS (10 -> 90% "
    "in >= 20 ms: drawn, not struck); 'wet': a liquid under the hiss -- the wet rendered alone HEARD in its own band "
    "(WET-HEARD, the best third-octave at 159-1270 Hz over the score's p90) >= +6 dB on the worst draw, and MOVING "
    ">= 400 cents (a liquid glides; a held note does not). Level: TOP between 0.5x the "
    "blow's loudest 50 ms on its LOUDEST draw and 1.0x on its QUIETEST, on every draw; heard: its loudest 100 ms "
    ">= +6 dB over the score's p90 in its best third-octave >= 200 Hz. Register against rune-crack, each "
    "bloodsworn and greatsword cast with a voice of its own, the tornado's woosh (the game's other swept noise), "
    "the blow and the death voice -- and a school or type peer's cast -- each <= 0.80. Tiebreak: the most "
    "distinct register (to 0.05), then the fewest synth calls, then the order listed.")

BLOW_RULE = (
    "Each candidate is the plain hit arm at the damage DEALT with its frequencies scaled by the stack count n. "
    "'pitched DOWN by the stack count (bigger = lower)': against the plain hit at the same dealt damage, CRACK "
    "and BODY each fall by >= 50 cents with every stack from 1 to 4; heard over the dice: at 2 and 4 stacks (the "
    "counts a window has) each drop >= SPREAD there (what the damage roll's whole range moves the plain hit by); "
    "'the sword's strike voice': a strike at 4 stacks (RISE <= 3 ms, the peak in the first 15 ms), its sample "
    "peak within 1.5 dB of the plain hit's on the same draw at every n x jitter 0.85 / 1 / 1.15 x crit (its level "
    "is its damage's), and at 4 stacks ENV-CORR >= 0.90 and REG > 0.80 with the plain hit at the same damage "
    "(still that voice, on the batch's own 0.80 line); not a death: REG <= 0.80 against the death voice at 4 "
    "stacks, crit or not; heard on a phone: PHONE at 4 stacks >= -6 dB re the plain hit's. Tiebreak: the largest "
    "drop at 4 stacks (the mean of CRACK and BODY, to 50 cents -- the price the most legible), then the fewest "
    "synth calls, then the order listed. ROUND 2 (see THE ROUNDS): CRACK is CRACK3; the two REG gates are printed, "
    "not gated; 'a strike, not a boom': AUDIBLE at 4 stacks, crit or not, <= 1.25x the plain hit's at the same "
    "damage; the tiebreak is the SMALLEST drop at 4 stacks (to 50 cents) that clears every gate.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 330 <= M["aud_lo"] <= M["aud_hi"] <= 470:
        why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 330-470")
    if M["gone_hi"] > 470: why.append(f"gone at {M['gone_hi']:.0f} ms")
    if M["hiss_lo"] < 0.50: why.append(f"hiss {M['hiss_lo']:.2f} < 0.50")
    if M["drawn"] < 600: why.append(f"drawn {M['drawn']:+.0f} c, not >= +600")
    if M["swell"] < 20: why.append(f"swell {M['swell']:.0f} ms < 20 (struck)")
    if M["wheard_lo"] < WET_GATE: why.append(f"wet heard {M['wheard_lo']:+.1f} dB < +{WET_GATE:g}")
    if M["moving"] < 400: why.append(f"moving {M['moving']:.0f} c < 400")
    if M["top_lo"] < lev["lo"]: why.append(f"top {M['top_lo']:.4f} < {lev['lo']:.4f}")
    if M["top_hi"] > lev["hi"]: why.append(f"top {M['top_hi']:.4f} > {lev['hi']:.4f}")
    if M["heard"] < 6: why.append(f"heard {M['heard']:+.1f} dB < +6")
    for k, v in M["regs"].items():
        if v > 0.80: why.append(f"register vs {k} {v:.2f} > 0.80")
    return why


def blow_why(M):
    why = []
    for n in range(1, CAP + 1):
        cr, bo = M["crack"][n], M["body"][n]
        pc, pb = (M["crack"][n - 1], M["body"][n - 1]) if n > 1 else (0.0, 0.0)
        if cr - pc > -50: why.append(f"crack {pc:+.0f} -> {cr:+.0f} c at {n - 1} -> {n} stacks, not down >= 50")
        if bo - pb > -50: why.append(f"body {pb:+.0f} -> {bo:+.0f} c at {n - 1} -> {n} stacks, not down >= 50")
    for n in (2, 4):
        if -M["crack"][n] < M["spread_c"][n]:
            why.append(f"crack {M['crack'][n]:+.0f} c at {n} stacks inside the dice's {M['spread_c'][n]:.0f}")
        if -M["body"][n] < M["spread_b"][n]:
            why.append(f"body {M['body'][n]:+.0f} c at {n} stacks inside the dice's {M['spread_b'][n]:.0f}")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms")
    if M["pk_ms"] > 15: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["pk_db"] > 1.5: why.append(f"peak {M['pk_db']:.1f} dB off the plain hit's")
    if M["corr"] < 0.90: why.append(f"env-corr {M['corr']:.2f} < 0.90")
    if M["aud_r"] > 1.25: why.append(f"audible {M['aud_r']:.2f}x the plain hit's at 4 stacks (a boom, not a strike)")
    if M["phone_db"] < -6: why.append(f"phone {M['phone_db']:+.1f} dB < -6")
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="a link carrying Goreshard's stage 5 (Bloodprice)")
    ap.add_argument("--also", action="append", default=[],
                    help="another link carrying it (e.g. carried onto a newer tip): the rows as text there")
    ap.add_argument("--out", default="../05-reference/v114")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=114601)
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
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "blow": BLOW_RULE}}
    for nm, anc in (("Sfx fallback", SFX_ANCHOR), ("Sfx plain hit arm", HIT_ANCHOR),
                    ("resolveHit hit voice", RH_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    for nm in ("p.price", "price: priceN", f'(w === "{ME}")', FALLBACK):
        if nm in html:
            raise SystemExit(f"{gp.name} already names {nm!r} -- run on stage 5, before the voices")
    if "const priceN = self.ultPrice ? foe.stacks(\"hemorrhage\") : 0;" not in html:
        raise SystemExit("no priceN line in resolveHit -- not Bloodprice's stage 5")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nBLOODPRICE -- THE VOICES   game {gp.name} {rec['game_sha']}")
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
                           "w.ult && w.ult.perStack, w.name])")
        ids = [w_[0] for w_ in W_]
        if ME not in ids:
            raise SystemExit("no oathwound in this build")
        me = [w_ for w_ in W_ if w_[0] == ME][0]
        if abs(me[3] - BLADE) > 1e-9 or me[4] != "price" or abs((me[5] or 0) - PER_STACK) > 1e-12 or me[6] != NAME:
            raise SystemExit(f"Goreshard is {me} -- this lab levels against blade {BLADE} and a price of {PER_STACK}")
        cfg = page.evaluate("() => { const S_ = (0, eval)('STATUS'), C_ = AC.CONFIG.chaos; "
                            "return [S_.hemorrhage.maxStacks, C_.critMul, C_.dmgJitter]; }")
        if cfg != [CAP, CRIT_MUL, 0.3]:
            raise SystemExit(f"hemorrhage cap / critMul / dmgJitter are {cfg}, not [{CAP}, {CRIT_MUL}, 0.3]")
        print(f"  Goreshard: blade {me[3]}, ult {me[4]} perStack {me[5]}; Hemorrhage cap {cfg[0]}, crit x{cfg[1]}, "
              f"jitter +/-{cfg[2] / 2:.0%}")
        play_src = page.evaluate("() => Object.getPrototypeOf(AC.SFX).play.toString()")
        for anc in (SFX_ANCHOR, HIT_ANCHOR):
            if play_src.count(anc) != 1:
                raise SystemExit("an Sfx anchor is not in play() exactly once")
        plain = HIT_ANCHOR + "\n" + "\n".join("        " + l_ for l_ in PLAIN_ARM) + "\n      }"
        if plain not in play_src:
            raise SystemExit("the page's plain hit arm is not the one this lab transcribes")
        print("  the page's plain hit arm is the four lines this lab transcribes (checked verbatim)")

        def R(evs, secs=3.0, seed=None, rows=None, new=True, allow_silent=False):
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
            if float(np.abs(x).max()) < 1e-6 and not allow_silent:
                raise SystemExit(f"SILENT render: {str(evs[:1])[:160]}")
            if min(e[1] for e in evs) >= T0 and float(np.abs(x[:int(T0 * SR) - 2]).max()) > 1e-6:
                raise SystemExit("sound BEFORE t=1.0")
            return x, r["calls"]

        def play(kind, p, seed=None, allow_silent=False):
            return R([["play", T0, kind, p]], seed=seed, new=False, allow_silent=allow_silent)[0]

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, (kind, p) in [("rune-crack", ("ult", {"w": FALLBACK})), ("BAR", ("ult", {"w": "axiom"})),
                                ("hit@11.6", ("hit", {"dmg": 11.6, "crit": False})),
                                (f"hit@{BLADE:g}", ("hit", {"dmg": BLADE, "crit": False})),
                                ("wall", ("wall", {})), ("death", ("death", {})),
                                ("woosh", ("scour-woosh", {"n": 1}))]:
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
            raise SystemExit("Goreshard's cast is not rune-crack today -- this lab adds its arm, so stop")
        rec["fallthrough"] = fall_ids
        school = [w_[0] for w_ in W_ if w_[1] == SCHOOL_AFF and w_[0] not in fall_ids]
        types = [w_[0] for w_ in W_ if w_[2] == TYPE_SHAPE and w_[0] not in fall_ids]
        print(f"  the bloodsworn casts with their own voice: {', '.join(school) or '-'};  the greatsword casts': "
              f"{', '.join(types) or '-'}")
        rec["school"], rec["type"] = school, types

        # the noise draws of every reference
        REFS = {"hit": ("hit", {"dmg": BLADE, "crit": False}), "wall": ("wall", {}),
                "rune-crack": ("ult", {"w": FALLBACK}), "death": ("death", {}), "woosh": ("scour-woosh", {"n": 1})}
        for w_ in school + types:
            REFS[w_] = ("ult", {"w": w_})
        RD_ = {k: [] for k in REFS}
        for sd in NOISE_SEEDS:
            for k, (kind, p) in REFS.items():
                RD_[k].append(basic(play(kind, p, seed=sd)))
        RB = {k: [m_["bands"] for m_ in v] for k, v in RD_.items()}
        # the school's and the type's voices on the batch line, from their own rows
        peer_regs = []
        for pf, prow in peer_sfx:
            pn = peer_name(pf)
            if pn not in PEER_SCHOOL and pn not in PEER_TYPE:
                continue
            ps = [as_replace(r_["anchor"], r_.get("mode", "replace"), r_["code"]) for r_ in prow
                  if play_src.count(r_["anchor"]) == 1]
            if not ps or f'w === "{pn}"' not in "".join(c for _a, c in ps):
                print(f"  peer {pn}: no cast arm that applies on this page -- skipped")
                continue
            RB["peer:" + pn] = [bands(R([["arm", T0, "ult", {"w": pn}]], rows=ps, new=False, seed=sd)[0][int(T0 * SR):])
                                for sd in NOISE_SEEDS]
            peer_regs.append("peer:" + pn)
        h_lo, h_hi = min(m_["top"] for m_ in RD_["hit"]), max(m_["top"] for m_ in RD_["hit"])
        w_hi = max(m_["top"] for m_ in RD_["wall"])
        print(f"  the hit @ {BLADE:g} across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m_['peak'] for m_ in RD_['hit']):.3f}-{max(m_['peak'] for m_ in RD_['hit']):.3f};  the wall "
              f"tick: {min(m_['top'] for m_ in RD_['wall']):.4f}-{w_hi:.4f}")
        if peer_regs:
            print(f"  the school's and type's voices on the batch line, from --peer-rows: {', '.join(peer_regs)}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        p90 = bed_p90(bed[int(2 * SR):int(10 * SR)])
        rec["levels"] = dict(hit=[h_lo, h_hi], wall_hi=w_hi)
        wav("goreshard-ctl-runecrack.wav", rcx)
        wav(f"goreshard-ctl-hit{BLADE:g}.wav", ctl[f"hit@{BLADE:g}"]["x"])
        wav("goreshard-ctl-woosh.wav", ctl["woosh"]["x"])

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo)
        tgt_c = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a wet drawn-blade hiss, 0.4s'. The declared draw (a Q {Q_DRAW} scrape rising 2.6 -> 8 kHz in "
              f"two strokes); the wet is the candidate. Level-matched: WET-HEARD +{WET_TGT:g} dB, AUDIBLE {AUD_TGT:g} ms, TOP "
              f"{tgt_c:.4f} (the centre of {lev_c['lo']:.4f}-{lev_c['hi']:.4f})")

        def cx(sp, g, kw, D2, seed=None, part="both"):
            return R([["body", T0, cast_body(sp, g, kw, D2, part=part), {}]], seed=seed)

        def calib_cast(sp):
            g, kw, D2 = 0.6, ((1.0 if sp["wet"] == "squelch" else 0.06) if sp.get("wet") else 0.0), 0.45
            for _ in range(5):
                B = basic(cx(sp, g, kw, D2)[0])
                D2 = round(min(0.58, max(0.2, D2 + (AUD_TGT - B["aud"]) / 1000)), 4)
                if sp.get("wet"):
                    wh = wet_heard(cx(sp, g, kw, D2, part="wet")[0], p90)[0]
                    kw = sig4(kw * 10 ** ((WET_TGT - wh) / 20))
                g = sig4(g * tgt_c / basic(cx(sp, g, kw, D2)[0])["top"])
            return g, kw, D2

        CAST_REGS = ["rune-crack"] + school + types + ["woosh", "hit", "death"] + peer_regs

        def cast_measure(name, x, draws, calls, wets, regs=CAST_REGS):
            """`wets`: the wet rendered alone on each draw (None: no wet part)."""
            M = basic(x); M.update(x=x, calls=calls, name=name)
            BD = [basic(d_) for d_ in draws]
            M["aud_lo"] = min(b_["aud"] for b_ in BD); M["aud_hi"] = max(b_["aud"] for b_ in BD)
            M["gone_hi"] = max(b_["gone"] for b_ in BD)
            M["top_lo"] = min(b_["top"] for b_ in BD); M["top_hi"] = max(b_["top"] for b_ in BD)
            M["hiss_lo"] = min(share(d_, HISS_LO, SR / 2 + 1) for d_ in draws)
            M["wet"] = share(x, *WET_BAND); M["wet_lo"] = min(share(d_, *WET_BAND) for d_ in draws)
            if wets:
                M["wheard"], M["wheard_fc"] = wet_heard(wets[0], p90)
                M["wheard_lo"] = min(wet_heard(d_, p90)[0] for d_ in wets)
            else:
                M["wheard"], M["wheard_fc"], M["wheard_lo"] = -99.0, 0.0, -99.0
            M["drawn"] = drawn(x, M); M["swell"] = swell(x)
            M["moving"] = moving(wets[0]) if wets else 0.0
            M["heard"], M["heard_fc"] = heard_top(x, p90)
            DB = [b_["bands"] for b_ in BD]
            M["DB"] = DB
            M["regs"] = {k: mreg(DB, RB[k]) for k in regs}
            M["reg_wall"] = mreg(DB, RB["wall"])
            return M

        def cast_line(M):
            r_ = M["regs"]
            k_ = max(r_, key=r_.get)
            print(f"  {M['name']:<12}{M.get('g', 0):>7.4g}{M.get('kw', 0):>7.4g}{M.get('D2', 0):>6.3f}{M['calls']:>6d}"
                  f"{M['top_lo']:>8.4f}{M['top_hi']:>8.4f}{M['aud_lo']:>5.0f}{M['aud_hi']:>5.0f}{M['gone_hi']:>5.0f}"
                  f"{M['hiss_lo']:>6.2f}{M['drawn']:>7.0f}{M['swell']:>5.0f}{M['wet_lo']:>6.2f}{M['wheard_lo']:>6.1f}"
                  f"{M['moving']:>7.0f}"
                  f"{M['heard']:>6.1f}{M['reg_wall']:>6.2f}{r_[k_]:>6.2f} ({k_})")

        print(f"  {'cand':<12}{'g':>7}{'kw':>7}{'D2':>6}{'calls':>6}{'top lo':>8}{'top hi':>8}{'aud':>5}{'-':>5}"
              f"{'gone':>5}{'hiss':>6}{'drawn':>7}{'swl':>5}{'wet':>6}{'wHrd':>6}{'moving':>7}{'hrd':>6}{'wall':>6}"
              f"{'reg':>6}")
        rows_c = []
        for name, sp, _b in CAST_CANDIDATES:
            g, kw, D2 = calib_cast(sp)
            x, calls = cx(sp, g, kw, D2)
            x2, _ = cx(sp, g, kw, D2)
            if float(np.abs(x - x2).max()) > TOL:
                raise SystemExit(f"cast {name} does not reproduce")
            draws = [cx(sp, g, kw, D2, seed=sd)[0] for sd in NOISE_SEEDS]
            wets = [cx(sp, g, kw, D2, seed=sd, part="wet")[0] for sd in NOISE_SEEDS]
            M = cast_measure(name, x, draws, calls[0], wets)
            M.update(sp=sp, g=g, kw=kw, D2=D2)
            M["why"] = cast_why(M, lev_c)
            rows_c.append(M); cast_line(M)
            wav(f"goreshard-cast-{name.split()[1].lower()}.wav", x)
        ctlc = []
        C0 = rows_c[0]
        for name, sp in (("0 DRY", dict(wet=None)), ("0 STILL", dict(C0["sp"], still=True)),
                         ("0 HUM", dict(wet="hum")), ("0 FAINT", dict(C0["sp"]))):
            g, kw, D2 = calib_cast(sp)
            if name == "0 FAINT":
                kw = sig4(kw * 10 ** (-12 / 20))
            x, calls = cx(sp, g, kw, D2)
            draws = [cx(sp, g, kw, D2, seed=sd)[0] for sd in NOISE_SEEDS]
            wets = [cx(sp, g, kw, D2, seed=sd, part="wet")[0] for sd in NOISE_SEEDS] if sp.get("wet") else None
            M = cast_measure(name, x, draws, calls[0], wets); M.update(sp=sp, g=g, kw=kw, D2=D2)
            M["why"] = cast_why(M, lev_c)
            ctlc.append(M); cast_line(M)
            wav(f"goreshard-cast-ctl-{name.split()[1].lower()}.wav", x)
        rcd = [play("ult", {"w": FALLBACK}, seed=sd) for sd in NOISE_SEEDS]
        M = cast_measure("0 RUNECRACK", rcx, rcd, 5, rcd)
        M["why"] = cast_why(M, lev_c); ctlc.append(M); cast_line(M)
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<11} {blurb}")
        print("    0 DRY       the draw alone (no wet) -- a control\n"
              "    0 STILL     BUBBLE with both strokes held at 2.6 kHz (not rising) -- a control\n"
              "    0 HUM       the draw over a held 620 Hz sine, heard as the wets are -- a control\n"
              "    0 FAINT     BUBBLE with its wet 12 dB down -- a control\n"
              "    0 RUNECRACK what the cast plays today -- a control")
        print(f"  RULE  {CAST_RULE}")
        for M in rows_c:
            if M["why"]:
                print(f"    {M['name']:<11} out: {'; '.join(M['why'])}")
        for M in ctlc:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- it cannot fail, so the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        need = {"0 DRY": "wet heard", "0 STILL": "drawn", "0 HUM": "moving", "0 FAINT": "wet heard",
                "0 RUNECRACK": "hiss"}
        for M in ctlc:
            if M["why"] and not any(w_.startswith(need[M["name"]]) for w_ in M["why"]):
                print(f"  {M['name']} fails, but NOT on '{need[M['name']]}' -- the gate it is for is blind")
                FAILED.append(M["name"].lower() + " control blind")
        ok, fb = _gate(rows_c, "cast")
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["regs"].values()) / 0.05),
                                                          rows_c[i]["calls"], i))
        Ca = rows_c[ci]
        rk = max(Ca["regs"], key=Ca["regs"].get)
        print(f"  PICK  {Ca['name']}  g {Ca['g']}, kw {Ca['kw']}, D2 {Ca['D2']}, {Ca['calls']} synth calls; TOP "
              f"{db(Ca['top'] / h_lo):+.1f} dB re the blow (quietest draw), {db(Ca['top'] / w_hi):+.1f} dB re the wall; "
              f"register at most {Ca['regs'][rk]:.2f} ({rk}); the wall tick {Ca['reg_wall']:.2f} (a 35 ms tick: printed)")

        # ---- THE PRICED BLOW -----------------------------------------------
        print("\nSCALED BLOW -- 'the sword's strike voice pitched DOWN by the stack count (bigger = lower)'. The plain "
              "hit at the damage dealt, every frequency x 2^(-c n / 1200); not levelled (its level is the blow's)")

        def dealt(n, j=1.0, crit=False):
            v = BLADE * (1 + PER_STACK * n) * j * (CRIT_MUL if crit else 1.0)
            return float(math.floor(v + 0.5))           # Math.round, for positives

        pcache = {}

        def plain_x(d, crit=False, seed=None):
            k = (d, crit, seed)
            if k not in pcache:
                pcache[k] = play("hit", {"dmg": d, "crit": crit}, seed=seed)
            return pcache[k]

        def bx(sp, n, j=1.0, crit=False, seed=None):
            return R([["body", T0, blow_body(sp), {"dmg": dealt(n, j, crit), "crit": crit, "price": n}]], seed=seed)

        # SPREAD: the damage roll's whole range, on the plain hit, at each count
        spread_c, spread_b = {}, {}
        for n in (2, 4):
            lo_d, hi_d = dealt(n, JIT[0]), dealt(n, JIT[2])
            spread_c[n] = -crack3([plain_x(hi_d, seed=sd) for sd in NOISE_SEEDS],
                                  [plain_x(lo_d, seed=sd) for sd in OTHER_SEEDS])
            spread_b[n] = -body_c(plain_x(hi_d), plain_x(lo_d))
        print("  SPREAD (the plain hit at the dealt damage x 1.15 against x 0.85): " +
              ", ".join(f"{n} stacks ({dealt(n, JIT[0]):g}-{dealt(n, JIT[2]):g}) crack {spread_c[n]:.0f} c, body "
                        f"{spread_b[n]:.0f} c" for n in (2, 4)))
        # what the weight alone does today, n stacks against none (PLAIN's own drop)
        wt_c = {n: crack3([plain_x(dealt(n), seed=sd) for sd in NOISE_SEEDS],
                          [plain_x(dealt(0), seed=sd) for sd in OTHER_SEEDS]) for n in (2, 4)}
        wt_b = {n: body_c(plain_x(dealt(n)), plain_x(dealt(0))) for n in (2, 4)}
        print("  the WEIGHT alone today (the plain hit at the dealt damage, n stacks against 0): " +
              ", ".join(f"{n} stacks ({dealt(n):g} vs {dealt(0):g}) crack {wt_c[n]:+.0f} c, body {wt_b[n]:+.0f} c"
                        for n in (2, 4)))
        rec["spread"] = dict(crack=spread_c, body=spread_b, weight_crack=wt_c, weight_body=wt_b)

        def blow_measure(name, sp, fn):
            """fn(n, j, crit, seed) -> the voice. `sp` None: PLAIN."""
            M = dict(name=name, sp=sp, crack={}, body={})
            for n in range(1, CAP + 1):
                d = dealt(n)
                M["crack"][n] = crack3([fn(n, 1.0, False, sd) for sd in NOISE_SEEDS],
                                       [plain_x(d, seed=sd) for sd in OTHER_SEEDS])
                M["body"][n] = body_c(fn(n, 1.0, False, None), plain_x(d))
            M["spread_c"], M["spread_b"] = spread_c, spread_b
            x4 = fn(CAP, 1.0, False, None)
            B4 = basic(x4); M.update(rise=B4["rise"], pk_ms=B4["pk_ms"], x=x4, calls=0)
            pkd = 0.0
            for n in range(1, CAP + 1):
                for j in JIT:
                    for crit in (False, True):
                        for sd in NOISE_SEEDS[:4]:
                            r_ = db(float(np.abs(fn(n, j, crit, sd)).max()) /
                                    float(np.abs(plain_x(dealt(n, j, crit), crit, sd)).max()))
                            pkd = max(pkd, abs(r_))
            M["pk_db"] = pkd
            ref4 = plain_x(dealt(CAP))
            M["corr"] = env_corr(x4, ref4)
            D4 = [bands(fn(CAP, 1.0, False, sd)[int(T0 * SR):]) for sd in NOISE_SEEDS]
            P4 = [bands(plain_x(dealt(CAP), seed=sd)[int(T0 * SR):]) for sd in NOISE_SEEDS]
            M["reg_plain"] = mreg(D4, P4)
            D4c = [bands(fn(CAP, 1.0, True, sd)[int(T0 * SR):]) for sd in NOISE_SEEDS]
            M["reg_death"] = max(mreg(D4, RB["death"]), mreg(D4c, RB["death"]))
            M["phone_db"] = db(phone(x4) / phone(ref4))
            M["aud_r"] = max(basic(x4)["aud"] / basic(ref4)["aud"],
                             basic(fn(CAP, 1.0, True, None))["aud"] / basic(plain_x(dealt(CAP, 1.0, True), True))["aud"])
            M["drop4"] = -(M["crack"][CAP] + M["body"][CAP]) / 2
            return M

        def blow_line(M):
            print(f"  {M['name']:<9}{M['calls']:>6d}  " +
                  " ".join(f"{M['crack'][n]:+5.0f}/{M['body'][n]:+5.0f}" for n in range(1, CAP + 1)) +
                  f"{M['rise']:>5.0f}{M['pk_ms']:>5.0f}{M['pk_db']:>6.1f}{M['corr']:>6.2f}{M['reg_plain']:>6.2f}"
                  f"{M['reg_death']:>6.2f}{M['phone_db']:>7.1f}{M['aud_r']:>6.2f}{M['drop4']:>7.0f}")

        print(f"  {'cand':<9}{'calls':>6}  {'crack/body c at 1':>11} {'2':>11} {'3':>11} {'4':>11}{'rise':>5}{'pk@':>5}"
              f"{'pk dB':>6}{'corr':>6}{'plain':>6}{'death':>6}{'phone':>7}{'audR':>6}{'drop4':>7}")
        rows_b = []
        for name, sp, _b in BLOW_CANDIDATES:
            x1, c1 = bx(sp, 2)
            x2, _ = bx(sp, 2)
            if float(np.abs(x1 - x2).max()) > TOL:
                raise SystemExit(f"blow {name} does not reproduce")
            M = blow_measure(name, sp, lambda n, j, c, sd, sp=sp: bx(sp, n, j, c, sd)[0])
            M["calls"] = c1[0]
            M["why"] = blow_why(M)
            rows_b.append(M); blow_line(M)
            for n in (2, 4):
                wav(f"goreshard-blow-{name.split()[1].lower()}-n{n}.wav", bx(sp, n)[0])
        ctlb = []
        Mp = blow_measure("0 PLAIN", None, lambda n, j, c, sd: plain_x(dealt(n, j, c), c, sd))
        Mp["calls"] = 2; Mp["why"] = blow_why(Mp); ctlb.append(Mp); blow_line(Mp)
        upsp = dict(BLOW_CANDIDATES[1][1], up=True)
        Mu = blow_measure("0 UP", upsp, lambda n, j, c, sd: bx(upsp, n, j, c, sd)[0])
        Mu["calls"] = rows_b[1]["calls"]; Mu["why"] = blow_why(Mu); ctlb.append(Mu); blow_line(Mu)
        for (name, _sp, blurb) in BLOW_CANDIDATES:
            print(f"    {name:<8} {blurb}")
        print("    0 PLAIN  the hit at the dealt damage: what a scaled blow plays TODAY -- a control\n"
              "    0 UP     TONE's interval upward (bigger = higher) -- a control")
        print(f"  RULE  {BLOW_RULE}")
        for M in rows_b:
            if M["why"]:
                print(f"    {M['name']:<8} out: {'; '.join(M['why'])}")
        for M in ctlb:
            if M["why"]:
                print(f"  {M['name']} (a control) comes back wrong, as it must: {'; '.join(M['why'][:3])}")
            else:
                print(f"  {M['name']} (a control) PASSED -- the rule proves nothing")
                FAILED.append(M["name"].lower() + " control")
        ok, fb = _gate(rows_b, "blow")
        bi = fb if ok is None else min(ok, key=lambda i: (round(rows_b[i]["drop4"] / 50), rows_b[i]["calls"], i))
        Bl = rows_b[bi]
        print(f"  PICK  {Bl['name']}  {Bl['calls']} synth calls; at 1-4 stacks crack " +
              "/".join(f"{Bl['crack'][n]:+.0f}" for n in range(1, CAP + 1)) + " c, body " +
              "/".join(f"{Bl['body'][n]:+.0f}" for n in range(1, CAP + 1)) +
              f" c against the plain hit at the same damage; register {Bl['reg_plain']:.2f} with it at 4")

        # ---- THE SFX ROWS, GENERATED AND CHECKED -----------------------------
        wet_what = {"bubble": "bubbles -- sine chirps rising 1.6x in 28 ms at 434-806 Hz, every ~34 ms",
                    "squelch": "a squelch -- a resonant noise band (Q 8) sliding 300 -> 900 Hz",
                    "slick": "the retired wet slice's falling saws (660 -> 240 and 480 -> 180 Hz)",
                    "drip": "three drops off the blade as it clears, each a sine chirping up 1.5x"}
        n_names = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                   "twelve", "thirteen", "fourteen", "fifteen"]
        nrc = len(fall_ids) - 1
        peer_txt = "".join(f", and {p_.split(':')[1].capitalize()}'s cast" for p_ in peer_regs)
        info_c = dict(n_cast=len(CAST_CANDIDATES), n_rc=n_names[nrc] if nrc <= 15 else str(nrc),
                      drawn=Ca["drawn"], swell=Ca["swell"], hiss=Ca["hiss_lo"], what=wet_what[Ca["sp"]["wet"]],
                      wet=Ca["wet"], moving=Ca["moving"], aud=Ca["aud"], top_db=db(Ca["top"] / h_lo),
                      heard=Ca["heard"], reg=Ca["regs"][rk], reg_k=rk.replace("peer:", ""), peers=peer_txt)
        blow_what = {100: "a semitone a stack, a major third at 4", 200: "a whole tone a stack, a minor sixth at 4",
                     300: "a minor third a stack, an octave at 4"}[Bl["sp"]["c"]]
        if Bl["sp"]["tape"]:
            blow_what += ", every length x 1/k (slowed like tape)"
        if not Bl["sp"]["crack"]:
            blow_what += ", the sine body only"
        info_b = dict(n_blow=len(BLOW_CANDIDATES), c=Bl["sp"]["c"], what=blow_what,
                      crack="/".join(f"{-Bl['crack'][n]:.0f}" for n in range(1, CAP + 1)),
                      body="/".join(f"{-Bl['body'][n]:.0f}" for n in range(1, CAP + 1)),
                      over2=f"{min(-Bl['crack'][2] / spread_c[2], -Bl['body'][2] / spread_b[2]):.1f}",
                      over4=f"{min(-Bl['crack'][4] / spread_c[4], -Bl['body'][4] / spread_b[4]):.1f}",
                      pk=Bl["pk_db"], reg=Bl["reg_plain"], death=Bl["reg_death"])
        cast_code = cast_arm_code(Ca, info_c)
        hit_code = hit_row_code(Bl, info_b)
        for nm_, cd_, an_ in (("cast", cast_code, SFX_ANCHOR), ("hit", hit_code, HIT_ANCHOR)):
            _refuse(cd_, f"Sfx {nm_} row")
            if not cd_.isascii():
                raise SystemExit(f"the Sfx {nm_} row is not ASCII")
            if an_ in cd_ or not cd_.endswith("\n"):
                raise SystemExit(f"the Sfx {nm_} row must sit before its anchor without repeating it")
        sfx_rows = [as_replace(HIT_ANCHOR, "before", hit_code), as_replace(SFX_ANCHOR, "before", cast_code)]
        print("\nTHE SFX ROWS (mode `before` the plain hit arm; mode `before` the rune-crack fallback), applied to "
              "Sfx.prototype.play's own source and rendered:")
        chk = []
        cbody = cast_body(Ca["sp"], Ca["g"], Ca["kw"], Ca["D2"])
        for sd in (None, NOISE_SEEDS[3]):
            x1, _ = R([["arm", T0, "ult", {"w": ME}]], rows=sfx_rows, seed=sd)
            x2, _ = R([["body", T0, cbody, {}]], seed=sd)
            chk.append(("cast" + ("" if sd is None else " draw"), float(np.abs(x1 - x2).max())))
            if sd is None:
                xa0 = x1
        bbody = blow_body(Bl["sp"])
        wb = 0.0
        for n in range(1, CAP + 2):                      # 5: above the cap, held at 4's voice
            for j in JIT:
                for crit in (False, True):
                    p_ = {"dmg": dealt(min(n, CAP), j, crit), "crit": crit, "price": n}
                    x1, _ = R([["arm", T0, "hit", p_]], rows=sfx_rows, seed=NOISE_SEEDS[5])
                    x2, _ = R([["body", T0, bbody, p_]], seed=NOISE_SEEDS[5])
                    wb = max(wb, float(np.abs(x1 - x2).max()))
        chk.append(("blow n1-5 x jitter x crit", wb))
        cap_d = float(np.abs(R([["arm", T0, "hit", {"dmg": 23, "crit": False, "price": CAP + 2}]], rows=sfx_rows)[0] -
                             R([["arm", T0, "hit", {"dmg": 23, "crit": False, "price": CAP}]], rows=sfx_rows)[0]).max())
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk) +
              f";  price {CAP + 2} vs {CAP} (held at the cap): {cap_d:.1e}")
        others = [("hit", {"dmg": d_, "crit": c_}) for d_ in (5, BLADE, 16, 23, 50) for c_ in (False, True)]
        others += [("hit", {"dmg": 16, "crit": False, "price": 0})]
        others += [("hit", {"dmg": d_, "crit": c_, "bough": 0.38}) for d_ in (5, 9, 20) for c_ in (False, True)]
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
        silent = 0
        for kind, p in others:
            x1 = play(kind, p, allow_silent=True)
            x2, _ = R([["arm", T0, kind, p]], rows=sfx_rows, new=False, allow_silent=True)
            silent += float(np.abs(x1).max()) < 1e-6
            same_.append((kind + "/" + str(p.get("w", p.get("dmg", p.get("n", "")))) + ("!" if p.get("crit") else "")
                          + ("b" if p.get("bough") else "") + ("$0" if "price" in p else ""),
                          float(np.abs(x1 - x2).max())))
        worst = max(same_, key=lambda z: z[1])
        print(f"  every other voice through the patched play vs the original ({len(same_)} voices, {silent} of them "
              f"silent by design with empty opts: the hit at 5 weights x crit, a hit whose price is 0, Canopy's "
              f"bough at 3 x crit, the heal chime at n 0-6, spark arm and burn, wall, death, clank x2, seal, nova, "
              f"hex-snap, fork, vine x4, loose x3, aegis x2, scour x4, {len(ult_ids)} ult ids -- every relic's "
              f"cast, every sub-voice the ult arm names and the bare fallback -- and every kind play() names): "
              f"worst max |diff| {worst[1]:.0e} ({worst[0]})")
        now_rc = float(np.abs(xa0 - rcx).max())
        fb_rc = float(np.abs(R([["arm", T0, "ult", {"w": FALLBACK}]], rows=sfx_rows, new=False)[0] - rcx).max())
        print(f"  ult/{ME} vs rune-crack after the rows: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'};  ult/{FALLBACK} after the "
              f"rows: {fb_rc:.0e} -- {'still rune-crack' if fb_rc <= 1e-6 else 'CHANGED'}")
        if max(v for _, v in chk) > TOL or worst[1] > TOL or now_rc <= 1e-3 or fb_rc > 1e-6 or len(same_) < 30 \
                or cap_d > TOL:
            FAILED.append("sfx rows")
        cost = page.evaluate(COST_JS, [sfx_rows, 40, ME])
        print("  main-thread cost a call (median of 40, performance.now() at its headless resolution): " +
              ", ".join(f"{k} {v:.2f} ms" for k, v in cost.items()))
        rec["arm_check"] = dict(chk=chk, cap=cap_d, others=same_, now_rc=now_rc, fallback=fb_rc, cost=cost,
                                n_others=len(same_))

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
            mine = [("ult", {"w": ME}), ("hit", {"dmg": 23, "crit": False, "price": 4}),
                    ("hit", {"dmg": 16, "crit": True, "price": 2})]
            evs = mine + [("ult", {"w": w_, "n": 3, "k": 1, "shield": 45}) for w_ in pids] + [(k_, {}) for k_ in pk_]
            dmax, dmine = 0.0, 0.0
            for kind_, p_ in evs:
                xa_, _ = R([["arm", T0, kind_, p_]], rows=A_, new=False, allow_silent=True)
                xb_, _ = R([["arm", T0, kind_, p_]], rows=B_, new=False, allow_silent=True)
                dmax = max(dmax, float(np.abs(xa_ - xb_).max()))
                if (kind_, p_) in mine:
                    xs_, _ = R([["arm", T0, kind_, p_]], rows=sfx_rows, new=False)
                    dmine = max(dmine, float(np.abs(xa_ - xs_).max()))
            print(f"  WITH {peer_name(pf)}'s {len(ps)} Sfx row(s) (arms {', '.join(pids + pk_)}): both orders render "
                  f"every arm alike (max |diff| {dmax:.1e}); these arms unchanged by them ({dmine:.1e})")
            if dmax > TOL or dmine > TOL:
                FAILED.append(f"co-apply {pf}")
            peers.append(dict(file=str(pf), rows=len(ps), ids=pids + pk_, both_orders=dmax, mine=dmine))
        rec["peers"] = peers

        # ---- THE resolveHit ROW ---------------------------------------------
        rh_row = as_replace(RH_ANCHOR, "before", RH_CODE)
        rh_bad = as_replace(RH_ANCHOR, "before", RH_CODE_BAD)
        seeds = [a.seed0 + k for k in range(a.seeds)]
        WR = None
        if not a.no_wire:
            print("\nTHE resolveHit ROW (mode `before` the hit-voice line), applied to the prototype's own source, "
                  "run beside the original on real fights:")
            WR = page.evaluate(WIRE_JS, [seeds, rh_row, ME])
            assert not errors, errors[:3]
            if "err" in WR:
                raise SystemExit(WR["err"])
            T_ = WR["tot"]
            print(f"  {WR['fights']} fights (Goreshard both sides x every foe x seeds {seeds}): {WR['same']}/"
                  f"{WR['fights']} identical (over, clock, both fighters' hp, positions, velocities, stun, charge, "
                  f"Hemorrhage, winner, both priceTallies, and a digest of every step); every other SFX call "
                  f"identical in order and opts (the hit's `price` taken out) in {WR['otherSame']}/{WR['fights']}")
            print(f"  {T_['casts']} casts -> {T_['castV']} cast voices; {T_['win']} window blows by stacks priced on "
                  f"(0-4): {T_['hist'][:5]} -> {T_['pricedV']} priced voices for {T_['priced']} scaled blows "
                  f"({T_['noVoice']} blows with no voice of their own, both pages), {T_['win0']} x1 window blows "
                  f"plain; untouched: {T_['outside']} Goreshard blows outside the window, {T_['foeB']} foe blows, "
                  f"{T_['shat']} ward bursts; problems {WR['nbad']}")
            for b_ in WR["bad"]:
                print(f"    {b_}")
            if WR["same"] != WR["fights"] or WR["otherSame"] != WR["fights"] or WR["nbad"] \
                    or T_["pricedV"] != T_["priced"] - T_["noVoice"] or T_["pricedV"] == 0 \
                    or T_["castV"] != T_["casts"]:
                FAILED.append("resolveHit row")
            WB = page.evaluate(WIRE_JS, [seeds, rh_bad, ME])
            assert not errors, errors[:3]
            print(f"  the control (the row plus one sim write, the struck body nudged 1e-9 on a priced blow): "
                  f"{WB['same']}/{WB['fights']} identical -- "
                  f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
            if WB["same"] == WB["fights"]:
                FAILED.append("identity control")
            rec["wire"] = {k: WR[k] for k in ("fights", "same", "otherSame", "tot", "nbad")}
            rec["wire"]["control_same"] = WB["same"]

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        if WR and WR["pick"]:
            w_ = sorted(WR["pick"], key=lambda z: (-z["priced"], z["foe"], z["seed"], z["side"]))[0]
            RC = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], rh_row, ME])
            assert not errors, errors[:3]
            EV = RC["ev"]
            pr_ = [e for e in EV if e[3] == "priced"]
            W0 = [W for W in RC["wins"] if any(W["cast"] - 0.05 <= e[0] <= (W["close"] or 1e9) for e in pr_)]
            W0 = max(W0, key=lambda W: sum(1 for e in pr_ if W["cast"] - 0.05 <= e[0] <= (W["close"] or 1e9)))
            c0 = W0["cast"]; c1 = W0["close"] or max(e[0] for e in EV)
            lo_t, hi_t = c0 - 1.0, c1 + 1.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            base_ = [["play", T0 + (e[0] - lo_t), e[1], {k: v for k, v in e[2].items() if k != "price"}]
                     for e in evs if e[3] != "cast"]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, rows=sfx_rows, new=False)
            xo, _ = R(base_, secs=secs, new=False)
            bd = np.resize(bed, len(xw))
            xw = xw + bd; xo = xo + bd
            ct = [T0 + (e[0] - lo_t) for e in evs if e[3] == "cast"]
            fc_ = Ca["heard_fc"]
            cast_over = [db(band_rms(xw, fc_, t_, t_ + 0.4) / max(band_rms(xo, fc_, t_, t_ + 0.4), 1e-12))
                         for t_ in ct]
            # every scaled blow of the window, rendered alone: its pitch against the plain call's
            pb = []
            for e in evs:
                if e[3] != "priced":
                    continue
                xp_, _ = R([["arm", T0, "hit", e[2]]], rows=sfx_rows, new=False)
                q_ = {k: v for k, v in e[2].items() if k != "price"}
                pb.append((e[2]["price"], e[2]["dmg"], bool(e[2].get("crit")), body_c(xp_, plain_x(q_["dmg"], q_["crit"]))))
            nm_ = [w__[6] for w__ in W_ if w__[0] == w_["foe"]][0]
            print(f"\nIN A REAL WINDOW -- Goreshard v {nm_} (side {w_['side']}), seed {w_['seed']}, cast at {c0:.2f}s, "
                  f"closed at {c1:.2f}s; the fight's own sounds and the score, with the new voices and without")
            print(f"  the cast over the fight in its own third-octave ({fc_:.0f} Hz), 0.4 s: " +
                  " ".join(f"{v:+.1f}" for v in cast_over) + " dB")
            if pb:
                print(f"  the window's {len(pb)} scaled blows, each alone at the damage it dealt (stacks, dmg, crit -> "
                      f"body cents re the plain call): " +
                      ", ".join(f"{n_}/{d_:g}{'!' if c_ else ''} {b_:+.0f}" for n_, d_, c_, b_ in pb))
            if cast_over and min(cast_over) < 6:
                FAILED.append("the cast not heard in a real window")
            wav("goreshard-pick-real-window.wav", xw)
            wav("goreshard-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, cast_over=cast_over, priced=pb)
        elif not a.no_wire:
            FAILED.append("no real window")
        # the picks in order, for the ear: the cast, blows at 0 / 2 / 4 stacks, a plain blow
        seq = [["arm", T0, "ult", {"w": ME}]]
        for k_, n_ in enumerate((0, 2, 4, 2, 4, 0)):
            p_ = {"dmg": dealt(n_), "crit": False}
            if n_:
                p_["price"] = n_
            seq += [["arm", T0 + 0.75 + 0.42 * k_, "hit", p_]]
        wav("goreshard-pick-sequence.wav", R(seq, secs=5.5, rows=sfx_rows, new=False)[0])

        # ---- THE UNPATCHED PAGE'S OWN NUMBERS, for the end-to-end check -----
        e2e_seeds = [a.seed0 + 50 + k for k in range(a.e2e_seeds)]
        if a.e2e_seeds > 0 and not a.no_wire:
            e2e_ref["voices"] = [play(kind, p, allow_silent=True) for kind, p in e2e_voices]
            e2e_ref["fights"] = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
            if "err" in e2e_ref["fights"]:
                raise SystemExit(e2e_ref["fights"]["err"])

    # ---- THE ROWS --------------------------------------------------------------
    rows = [dict(label="Sfx: the scaled blow -- a branch before the plain hit arm, taken only with `price`",
                 anchor=HIT_ANCHOR, mode="before", code=hit_code),
            dict(label="Sfx: Goreshard's cast arm, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="before", code=cast_code),
            dict(label="resolveHit: a scaled blow's hit voice carries `price` (priceN > 0), before the hit-voice line",
                 anchor=RH_ANCHOR, mode="before", code=RH_CODE)]
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

    NEWP = [("cast", "ult", {"w": ME}, cbody)] + [
        (f"blow n{n_}{'!' if c_ else ''}", "hit", {"dmg": dealt(n_, 1.0, c_), "crit": c_, "price": n_}, bbody)
        for n_ in (1, 2, 4) for c_ in (False, True)]

    def e2e_page(tp, ref_voices, ref_fights, label, voices, school_=None, type_=None):
        """Load a patched page; its own play() vs the lab's text and vs the
        unpatched page's voices; its fights vs the unpatched page's."""
        regs_ = {}
        with game(game_path=tp) as (page, errors):
            def R2(evs, seed=None):
                r = page.evaluate(RENDER_JS, [evs, 3.0, seed, None])
                assert not errors, errors[:3]
                return pcm(r)
            vo = max(float(np.abs(R2([["play", T0, k, p]]) - x0).max())
                     for (k, p), x0 in zip(voices, ref_voices))
            nd = []
            for lab_, kind_, p, body in NEWP:
                x1 = R2([["play", T0, kind_, p]], seed=NOISE_SEEDS[5])
                x2 = R2([["body", T0, body, p]], seed=NOISE_SEEDS[5])
                nd.append((lab_, float(np.abs(x1 - x2).max())))
            rcp = R2([["play", T0, "ult", {"w": FALLBACK}]])
            not_rc = float(np.abs(R2([["play", T0, "ult", {"w": ME}]]) - rcp).max())
            for w_ in (school_ or []) + (type_ or []):
                DB_ = [bands(R2([["play", T0, "ult", {"w": w_}]], seed=sd)[int(T0 * SR):]) for sd in NOISE_SEEDS]
                regs_[w_] = mreg(Ca["DB"], DB_)
            F1 = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
            if "err" in F1:
                raise SystemExit(F1["err"])
            page_err = len(errors)
        F0 = {f_["key"]: f_ for f_ in ref_fights["res"]}
        F1r = F1["res"]
        same = sum(F0[f_["key"]]["sum"] == f_["sum"] for f_ in F1r)
        osame = sum(F0[f_["key"]]["other"] == f_["other"] for f_ in F1r)
        c_ok = sum(f_["castV"] == f_["casts"] for f_ in F1r)
        b_ok = sum(f_["bad"] == 0 for f_ in F1r)
        orig_priced = sum(f_["pricedV"] for f_ in ref_fights["res"])
        orig_bad = sum(f_["bad"] for f_ in ref_fights["res"])
        tot = {k: sum(f_[k] for f_ in F1r) for k in ("casts", "castV", "win", "priced", "pricedV")}
        print(f"  the new voices through the patched page's own SFX.play vs the lab's candidate text in that page, "
              f"max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in nd))
        print(f"  every other voice ({len(voices)}), the patched page vs the original page: worst max |diff| "
              f"{vo:.1e};  ult/{ME} vs rune-crack on the patched page {not_rc:.3f}")
        if regs_:
            print("  the picked cast's register against this page's bloodsworn and greatsword casts: " +
                  ", ".join(f"{k} {v:.2f}" for k, v in regs_.items()))
        print(f"  {len(F1r)} fights: {same}/{len(F1r)} identical to the original page's (a digest of every step "
              f"included), every other SFX call identical in {osame}/{len(F1r)}; per fight -- cast voices = casts "
              f"{c_ok}, every scaled blow voiced with its stacks and nothing else priced {b_ok} (of {len(F1r)}); "
              f"totals {tot}; the original page priced {orig_priced} (its judge's problems {orig_bad} -- it must "
              f"voice none); page errors {page_err}")
        ok_ = not (max(v for _, v in nd) > TOL or vo > TOL or not_rc <= 1e-3 or same != len(F1r)
                   or osame != len(F1r) or min(c_ok, b_ok) != len(F1r) or orig_priced or page_err
                   or tot["pricedV"] == 0 or not F1["wired"] or (regs_ and max(regs_.values()) > 0.80))
        if not ok_:
            FAILED.append(f"end to end ({label})")
        return dict(new=nd, others=vo, not_rc=not_rc, fights=len(F1r), same=same, other_same=osame, totals=tot,
                    page_errors=page_err, regs=regs_)

    if a.e2e_seeds > 0 and not a.no_wire:
        patched = apply_text(html, "end to end")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="goreshard_e2e_"))
        try:
            tp = tmpd / "sc-goreshard-voices.html"
            tp.write_text(patched, encoding="utf-8", newline="")
            psha = hashlib.sha256(patched.encode()).hexdigest()[:16]
            print(f"\nEND TO END -- the three rows applied as text: {gp.name} {rec['game_sha']} -> {psha} "
                  f"(+{len(patched) - len(html)} chars), loaded in a fresh browser")
            E = e2e_page(tp, e2e_ref["voices"], e2e_ref["fights"], gp.name, e2e_voices)
            E["patched_sha"] = psha
            rec["e2e"] = E
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    # ---- ALSO: the rows on another link carrying Goreshard's stage 5 ----------
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
            W2 = page.evaluate("() => AC.WEAPONS.map(w => [w.id, w.aff, w.shape])")
            ids2 = [w__[0] for w__ in W2]
            u2 = sorted(set(re.findall(r'w === "([a-z-]+)"', ps2)) | set(ids2) | {FALLBACK})
            k2 = sorted(set(re.findall(r'kind === "([a-z-]+)"', ps2)) - {"ult", "hit"})
            voices2 = [v_ for v_ in e2e_voices if v_[0] != "ult" or v_[1]["w"] in u2]
            voices2 += [("ult", {"w": w_, "n": 2}) for w_ in u2
                        if w_ != ME and not w_.startswith(ME + "-") and ("ult", {"w": w_, "n": 2}) not in voices2]
            voices2 += [(k_, {}) for k_ in k2 if (k_, {}) not in voices2]
            ref_v = [R3([["play", T0, k, p]]) for k, p in voices2]
            rc2 = R3([["play", T0, "ult", {"w": FALLBACK}]])
            fall2 = [w_ for w_ in ids2 if float(np.abs(R3([["play", T0, "ult", {"w": w_}]]) - rc2).max()) <= 1e-6]
            ref_f = page.evaluate(FIGHTS_JS, [e2e_seeds, ME])
            assert not errors, errors[:3]
        sch2 = [w__[0] for w__ in W2 if w__[1] == SCHOOL_AFF and w__[0] not in fall2]
        typ2 = [w__[0] for w__ in W2 if w__[2] == TYPE_SHAPE and w__[0] not in fall2]
        print(f"  {len(ids2)} relics; its bloodsworn casts with a voice of their own: {', '.join(sch2)}; its "
              f"greatsword casts': {', '.join(typ2)}")
        tmpd = pathlib.Path(tempfile.mkdtemp(prefix="goreshard_also_"))
        try:
            tp = tmpd / ap_.name
            tp.write_text(p2, encoding="utf-8", newline="")
            E = e2e_page(tp, ref_v, ref_f, ap_.name, voices2, sch2, typ2)
            E.update(game=ap_.name, sha=s2, patched_sha=hashlib.sha256(p2.encode()).hexdigest()[:16],
                     voices=len(voices2))
            rec["also"].append(E)
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "bands", "DB")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), blow=strip(rows_b), blow_controls=strip(ctlb),
               wavs=sizes, pick={"cast": Ca["name"], "cast_g": Ca["g"], "cast_kw": Ca["kw"], "cast_D2": Ca["D2"],
                                 "blow": Bl["name"], "blow_c": Bl["sp"]["c"]})
    print(f"\nTHE PICKS  cast {Ca['name']}   scaled blow {Bl['name']}   close: nothing (v81 s4)")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")

    # WHY each row is safe, in the numbers this run measured
    E2 = rec.get("e2e")
    e2 = (f"; end to end, the rows applied as text: {E2['same']}/{E2['fights']} fights identical to the unpatched "
          f"page's" if E2 else "")
    al = "".join(f"; the same stage 5 carried onto the batch line's tip ({X['game']} {X['sha']}): "
                 f"{X['same']}/{X['fights']}" for X in rec["also"])
    ac = rec["arm_check"]
    rows[0]["why"] = (
        f"The scaled blow's voice, in the synth only: one branch BEFORE the plain hit arm (mode `before`, its anchor "
        f"the plain arm's own first line, kept), taken only when a call carries `price` -- which only the "
        f"resolveHit row adds. Through the patched play() it reproduces its lab candidate at 1-5 stacks x jitter x "
        f"crit (worst {max(v for k, v in ac['chk'] if k.startswith('blow')):.0e}); every hit without `price` (five "
        f"weights x crit, a price of 0, Canopy's bough) and {ac['n_others']} voices in all are unchanged (worst "
        f"{max(v for _, v in ac['others']):.0e}). play() returns on its first line with no audio context (every "
        f"headless run), draws no random number and writes nothing the simulation reads.")
    rows[1]["why"] = (
        f"Goreshard's cast voice, in the synth only. The arm goes BEFORE the shared rune-crack fallback (mode "
        f"`before`, its anchor the fallback line itself), so the {len(rec['fallthrough']) - 1} other relics that "
        f"still fall through keep it and another relic's row anchored there applies in either order. It reproduces "
        f"its lab candidate (worst {max(v for k, v in ac['chk'] if k.startswith('cast')):.0e}, two noise draws); "
        f"ult/{ME} is no longer rune-crack and the bare fallback still is. fireUlt already plays ult/{ME} once a "
        f"cast: no sim line"
        + (f"; end to end the new voices through the patched page's own SFX.play equal the candidates (worst "
           f"{max(v for _, v in E2['new']):.0e})" if E2 else "") + ".")
    wr = rec.get("wire")
    if wr:
        T_ = wr["tot"]
        rows[2]["why"] = (
            f"Before the hit-voice line (kept unchanged, the `else`): one guarded SFX.play reading only priceN, dmg "
            f"and crit, consts the lines above computed. {T_['pricedV']}/{T_['priced'] - T_['noVoice']} scaled "
            f"blows voiced with `price` = the stacks priceTally counted for them, none of the {T_['win0']} x1 window "
            f"blows, {T_['outside']} blows outside the window, {T_['foeB']} foe blows or {T_['shat']} ward bursts; "
            f"{wr['same']}/{wr['fights']} fights identical (a digest of every step included) and every other SFX "
            f"call identical in order and opts; the row plus one sim write comes back "
            f"{wr['control_same']}/{wr['fights']}{e2}{al}. Writes nothing; no field for the probe's allowed set.")
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
