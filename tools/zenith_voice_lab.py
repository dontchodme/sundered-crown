#!/usr/bin/env python3
"""ZENITH'S VOICES, RENDERED AND MEASURED, AND PICKED ON THE NUMBERS. v98.

    python zenith_voice_lab.py --game ../02-chain/sc-zenith.html --rows rows.json

v71 §6.2 SOUND, every word of it: "Cast: a bright swell, 0.5s, a rising fifth
in a sustained-by-restrike tone -- the sun coming up. A tick: a soft chime,
60ms, quiet (peak <=0.35), pitch by smite count. A heal: Daybreak's
spark-collect voice (`spark`, `collect:true`) already exists and already means
'healed' -- REUSE it, pitched by blessing count; do not write a second heal
voice. Close: the swell reversed, quiet." Rick, for the batch's art and sound:
"you pick i overrule". So this lab does not offer a spread -- it renders three
to five candidates a voice beside CONTROLS that can come back wrong, prints
the numbers each pick is made on, and PICKS by a rule written in this file
(`*_RULE`, `*_why`). He overrules from one clip.

THE FOUR EVENTS AND WHERE THEY FIRE:
  cast   the bare id `ult/morningstar`, which `fireUlt` plays for every relic.
         Morningstar has NO arm today: it falls through to the shared
         rune-crack (so do Lastlight, Aureole and Censer -- measured below,
         to 6e-8). The arms go BEFORE that fallback; the fallback is not
         touched.
  tick   `ult/morningstar-tick {n}` from `tickSun`, once per tick, after the
         tick's smite and blessing are applied: n = the foe's smite stacks
         (1..4 in play; the voice is defined and distinct for 0..4).
  heal   `spark {collect:true, n}` from `tickSun` on the same frame, n = the
         caster's blessing stacks (1..5) -- the EXISTING voice, unchanged
         (Lastlight's Harrowing uses it), exactly as Lastlight calls it.
  close  `ult/morningstar-close` from `tickSun` on the frame the window runs
         out BY ITS CLOCK with the caster alive -- never on a death, never
         once the fight is over (step() stops calling the tickers).

THE CONTROLS, and what each one is for:
  rune-crack   what Morningstar's cast plays TODAY and what three of the
               school's four other casts still play; v88 published 0.608 /
               450 ms -- reproduced before anything new is quoted
  BAR          Corollary's cast (`ult/axiom`), v88: 0.364 / 300 ms
  hit@11.6     v88's published 0.443 / 80 ms (the reproduction)
  hit@24       Morningstar's own blow (blade 24.03): the level every voice
               is judged against, on its quietest / loudest noise draw
  dawn cast    Daybreak's cast (`ult/dawnbringer`, step 0 of its line): the
               school's only other cast with its own voice
  spark        the heal voice, n 1..5: the tick chime lands on its frame
  wall         the commonest sound in a fight: the tick's floor
  score        the bed, mixed as `cinema_clip` mixes it (raw, x0.9)
  RAW          the picked-family cast WITHOUT `.frequency.value = f` (v97's
               toolkit finding): must come back wrong
  STRUCK       the rising fifth as two plain strikes -- the control on
               "sustained-by-restrike": must come back wrong
  AGAIN        the cast itself, played quiet as the close -- the control on
               "reversed": must come back wrong
  LITERAL      the picked cast rendered dry, its samples REVERSED, played
               through the chain at the close's gain. A reference, never a
               candidate: it needs an async render and every clip rebuilds
               the synth synchronously (v88 §6b), so it would be SILENT.

HOW THE NUMBERS ARE MADE -- each one a thing a person can be wrong about:
  * Every render runs through `Sfx.buildChain` in an OfflineAudioContext at
    48 kHz, the first event at t = 1.0, on a synth built the way render.py
    builds one (`Object.create` of the Sfx prototype, render.py's xorshift
    noise). Noise-built sounds are judged on the worst of twelve draws.
    Nothing may sound before t = 1.0; a silent render stops the run.
  * E50 = 50 ms RMS, 5 ms hop, in dB. TOP = the loudest 50 ms (its level and
    where its window is centred). START = the loudest 50 ms centred in the
    first 100 ms. SWELL = TOP - START, dB.
  * AUDIBLE = first to last 5 ms RMS window above 2% (-34 dB) of the voice's
    own loudest 5 ms window (v88's definition). GONE = where it ends.
  * DIPS = drops of more than 3 dB below the running max of the 25 ms RMS
    (5 ms hop) on the way up to the top (v88): a single swell has none.
    LINEARITY = the RMS residual (dB) of E50 about its own straight line over
    [50 ms, TOP - 30 ms]: how evenly the swell climbs.
  * FLUTTER = p95 - p5 (dB) of the RMS over four whole periods of the lowest
    pitch sounding (1 ms hop) about its own 100 ms average, inside each
    degree's plateau (v97's metric: a steady strike reads ~0, printed).
  * PITCH = the FFT peak (Hann, zero-padded, parabolic) inside a window, in
    cents from the degree it should be. TOP NOTE = the highest spectral peak
    within 3 dB of the strongest (the timbre's own octave partial sits 6.1 dB
    under its note, so it is never read as a note): what a dyad's "second
    note" is.
  * CENTROID = the power-weighted mean frequency of the whole voice.
  * REG = cosine similarity of 1/3-octave band amplitudes (25 Hz-16 kHz),
    the median over the noise draws where either side draws noise (v88).
  * IN-BAND = RMS inside the third-octave around a pitch; the score's is the
    p90 over 250 ms windows of an 8 s bed render.
  * RISE = 10 -> 90% of the 1 ms envelope; LATE = (energy centre - audible
    start) / audible (struck ~0.2, rising > 0.5).
  * ENV-CORR = Pearson correlation of two E50 curves (dB, each floored 40 dB
    under its own top), aligned at their onsets, over the longer audible span.
  * The candidates are LEVEL-MATCHED, not hand-set, so the pick is made on
    shape: the cast's gain and swell depth are solved (four passes) to put
    TOP at the centre of its level window and SWELL at +12 dB; each tick's
    gain and decay are solved to put its loudest 50 ms at the centre of ITS
    window and its audible length at 60 ms; the close's gain is solved to sit
    9 dB under the picked cast's top. The constants are rounded BEFORE any
    measured render, so the shipped arm is bit-for-bit what was measured.

THE DECLARED CHOICES (not candidates -- words of §6.2 turned into numbers):
  * PITCH OF THE FIFTH: D5 -> A5 (587.3 -> 881.0 Hz, a just fifth). iv -> i of
    the score's A minor: the sun lands on the tonic. Measured clear of
    Daybreak's C5, of BAR's E6 bar and of rune-crack (REG, printed).
  * TIMBRE ("bright"): a triangle with a sine an octave over it at 0.4 --
    every cast candidate shares it, so the pick is on shape.
  * TICK PITCHES ("pitch by smite count"): the A-minor pentatonic C D E G A
    from the chime's own root, one degree per count 0..4, so every count is a
    different note of the score's own scale.

THE PICKS, on Chromium 151.0.7922.34, sc-zenith 9be1a7ca4832c327, fight seeds
98001-98002 (136 fights, 457 windows, 2411 ticks):

  cast   1 STEP    the root re-struck ~11 ms apart for 0.25 s, then the fifth,
                   one swell: +11.9 dB, top at 495 ms at -2.9 dB re the hit @
                   24, gone 695 ms, flutter 1.3 dB, 0 cents, centroid 1064 Hz;
                   register 0.45 rune-crack / 0.39 BAR / 0.09 Daybreak. DYAD
                   passes too (flutter 0.5, LINEARITY 0.3 against 0.6) and
                   loses the register tiebreak (0.65 against BAR). GLIDE out
                   (starts +79 c: a portamento is not two notes); LEAN out
                   (flutter 3.4 dB at the 22 ms spacing); RAW out (2 dips, the
                   top 3.7 dB down); STRUCK out (tops at 280 ms).
  tick   2 SOFT    the bar's 1 : 2.76 modes up the pentatonic C7-A7 (2093-3520
                   Hz), audible 55 ms, peak 0.205, -10.9 dB re the hit @ 24 and
                   +10.8 re the wall tick; register 0.24 against the heal and
                   0.42 against the wall (TINK 0.49, PING 0.47 lose the wall
                   tiebreak); LOW out (peak at 10 ms; 0.45 against the heal).
                   On one frame with the heal each keeps its band to 0.2 dB.
  close  1 MIRROR  a 0.17 s climb (the cast's own release, reversed), then the
                   fifth falling to the root over 0.5 s: -9.0 dB under the
                   cast's top, gone 900 ms, ENV-CORR 0.90 with the literal.
                   DROP 0.01, SHORT -0.25, LONG 0.62 out; AGAIN (the control)
                   out on pitch, LATE and ENV-CORR.
  heal   the spark collect, n = blessing stacks (1-5), unchanged.

  In play: the smite count a tick lands on is 1:377 2:334 3:313 4:1387 -- 58%
  of ticks play the top note, because the count caps at 4; 247 of 2411 ticks
  land inside the cast's first 0.75 s; one close per clock close (372), none on
  the 8 deaths or 77 fight-ends; the rows keep 136/136 fights identical and the
  control comes back 10/136. In a real window (v Shroudmaul, 98001, 13 ticks)
  every chime stands +18.7..+63.1 dB over the fight and the score in its own
  third-octave, and the blows keep their peaks.

THE ROWS ARE CHECKED HERE, NOT JUST PRINTED:
  * the Sfx row is applied to `Sfx.prototype.play`'s own source in the page
    and rendered: cast, ticks 0..4 and close must reproduce the picked
    candidates to 1e-6; `hit`, `spark` (all three forms), `ult/axiom`,
    `ult/dawnbringer` and rune-crack (`ult/spellbreaker`) through the patched
    play must be unchanged; `ult/morningstar` must NOT be rune-crack any more;
  * the two tickSun rows are applied to `Match.prototype.tickSun`'s own source
    and run on real fights beside the unpatched one: every fight identical
    (over, clock, both hp, the whole sunTally); one tick voice and one heal
    per tick, on the tick's own step; one close per window closed by its clock
    and none otherwise; the cast's bare id once per cast. The same rows plus
    ONE sim write (the tick cooldown nudged 1 ms) must come back NOT identical,
    or "identical" proves nothing.
  All anchors must occur exactly once in the game file.

THE TOOLKIT'S BUGS ARE DESIGNED AROUND, NOT FIXED: `_tone` only decays (a held
note is RE-STRUCK -- CLAUDE.md 4.5) and `_tone`'s phase is not coherent above
~500 Hz unless `.frequency.value = f` is set on the returned node (v97 §4b; the
RAW control). The lab refuses any candidate source that names Math.random, rng
or spawnFx, and any _burst over 0.55 s or _sweep over 0.58 s.

Writes wavs to 05-reference/v98/zenith-*.wav at RAW level (not normalised, so
they compare by ear the way the numbers compare; gitignored with every wav).
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
import wave

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent
SR = 48000
T0 = 1.0
ST0 = 5                                   # D5 = 440 * 2^(5/12): the root
F0 = 440 * 2 ** (ST0 / 12)
F1 = F0 * 1.5                             # the fifth (just), A5 + 2 cents
SWELL_DB = 12.0                           # the cast's level-matched swell
CLOSE_UNDER_DB = 9.0                      # the close's level-matched quiet
PENT = [0, 2, 4, 7, 9]                    # A minor pentatonic from C

# ------------------------------------------------------------- THE CAST -----
# "a bright swell, 0.5s, a rising fifth in a sustained-by-restrike tone".
# Every candidate draws the same two pitches in the same timbre and is
# level-matched; they differ in how the fifth RISES and how it is HELD.
#   mode   step: the root re-struck for the first half, the fifth for the
#                second (the root's strikes stop; its tail hands over)
#          dyad: the root re-struck throughout, the fifth joins at the half
#          glide: one exponential chirp root -> fifth, struck at its own cycles
#          struck: two plain strikes, no re-strike (a CONTROL)
#   every  re-strike spacing target, s (rounded to whole cycles)
#   D      each strike's decay (`_tone` dur), s
#   a0     a degree's first strike carries a0 of the plateau (v97 HANDOFF)
#   oct    the octave sine's share ("bright")
#   fix    `.frequency.value = f` after `_tone` (False = the RAW control)
CAST_CANDIDATES = [
    ("1 STEP", dict(mode="step", every=0.011, D=0.25, a0=0.6, oct=0.4, fix=True, L=0.5, st=ST0),
     "root re-struck 0-0.25 s, the fifth 0.25-0.5 s, one swell across both"),
    ("2 DYAD", dict(mode="dyad", every=0.011, D=0.25, a0=0.6, oct=0.4, fix=True, L=0.5, st=ST0),
     "root re-struck throughout, the fifth joins at 0.25 s: an open fifth at the top"),
    ("3 GLIDE", dict(mode="glide", every=0.011, D=0.25, a0=0.6, oct=0.4, fix=True, L=0.5, st=ST0),
     "one chirp root -> fifth over 0.5 s, struck at its own cycle starts"),
    ("4 LEAN", dict(mode="step", every=0.022, D=0.25, a0=0.6, oct=0.4, fix=True, L=0.5, st=ST0),
     "STEP at half the strikes (~22 ms apart, v97's spacing): what the rate buys"),
]
CAST_CONTROLS = [
    ("0 RAW", "STEP without `.frequency.value = f`: the plain _tone"),
    ("0 STRUCK", "the root and the fifth struck once each, 0.25 s apart"),
]

CAST_SRC = r"""((S, sp, g, sw) => (t) => {
  const f0 = 440 * Math.pow(2, sp.st / 12), f1 = f0 * 1.5, L = sp.L;
  let c = 0;
  const strike = (s, f, gg, to) => {
    const o = S._tone(t + s, { freq: f, to: to, gain: gg, dur: sp.D, type: "triangle" });
    if (sp.fix) o.frequency.value = f;
    const o2 = S._tone(t + s, { freq: 2 * f, to: to && 2 * to, gain: gg * sp.oct, dur: sp.D, type: "sine" });
    if (sp.fix) o2.frequency.value = 2 * f;
    c += 2;
  };
  const lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);
  if (sp.mode === "struck"){ strike(0, f0, lv(0), null); strike(L / 2, f1, lv(L / 2), null); return c; }
  if (sp.mode === "glide"){
    const Lg = Math.log(1.5), N = Math.max(1, Math.round(f0 * sp.every));
    for (let k = 0; ; k += N){
      const s = L / Lg * Math.log(1 + k * Lg / (f0 * L));
      if (s >= L) break;
      strike(s, f0 * Math.pow(1.5, s / L), lv(s), f0 * Math.pow(1.5, (s + sp.D) / L));
    }
    return c;
  }
  const seg = sp.mode === "dyad" ? [[f0, 0, L], [f1, L / 2, L]] : [[f0, 0, L / 2], [f1, L / 2, L]];
  for (const [f, s0, s1] of seg){
    const dt = Math.max(1, Math.round(f * sp.every)) / f;
    const q = Math.pow(0.0001 / lv(s0), dt / sp.D);
    for (let k = 0; s0 + k * dt < s1 - 1e-9; k++){
      const s = s0 + k * dt, gs = lv(s);
      strike(s, f, k ? gs : Math.max(gs, gs * sp.a0 / (1 - q)), null);
    }
  }
  return c;
})"""

# ------------------------------------------------------------- THE TICK -----
# "a soft chime, 60ms, quiet (peak <=0.35), pitch by smite count". One struck
# thing a call; n (0..4) picks the pentatonic degree from the candidate's root
# (`st` semitones over A4).
TICK_CANDIDATES = [
    ("1 TINK", dict(mode="tink", st=27),
     "a struck bar (BAR's modes 1 : 2.76 : 5.40) from C7 up the pentatonic"),
    ("2 SOFT", dict(mode="soft", st=27),
     "the bar with its top mode off and the second at 0.25: a softer strike"),
    ("3 PING", dict(mode="ping", st=27),
     "a plain triangle note with an 8 ms click -- the control on 'chime'"),
    ("4 LOW", dict(mode="tink", st=3),
     "TINK two octaves down (C5-A5), in the cast's own octave: the register alternative"),
]

TICK_SRC = r"""((S, tp, g, D) => (t, n0) => {
  const n = Math.max(0, Math.min(4, n0 | 0));
  const f = 440 * Math.pow(2, ([0, 2, 4, 7, 9][n] + tp.st) / 12);
  if (tp.mode === "tink"){
    [[1, 1.00], [2.76, 0.42], [5.40, 0.16]].forEach(([r, k]) =>
      S._tone(t, { freq: f * r, gain: g * k, dur: D, type: "triangle" }));
    return 3;
  }
  if (tp.mode === "soft"){
    [[1, 1.00], [2.76, 0.25]].forEach(([r, k]) =>
      S._tone(t, { freq: f * r, gain: g * k, dur: D, type: "triangle" }));
    return 2;
  }
  S._tone(t, { freq: f, gain: g, dur: D, type: "triangle" });
  S._burst(t, { freq: 6000, q: 0.8, gain: g * 0.8, dur: 0.008, type: "highpass" });
  return 2;
})"""

# ------------------------------------------------------------- THE CLOSE ----
# "the swell reversed, quiet". Every candidate is the PICKED cast's own
# figure run backwards -- its degrees in reverse order, its level FALLING from
# the top -- at the close's gain `gc` (x the cast's g):
#   L     the length of the fall, s (the cast's swell is 0.5 s)
#   rise  a short climb to the top before the fall: the cast's own RELEASE
#         reversed (set from the picked cast's measured release), s
#   rdb   how far under the top that climb starts, dB
CLOSE_CANDIDATES = [
    ("1 MIRROR", dict(L=0.5, rise=None, rdb=30),
     "the whole cast reversed: its release as a short climb, then the fifth "
     "falling to the root over 0.5 s"),
    ("2 DROP", dict(L=0.5, rise=0, rdb=0),
     "the swell reversed from its top: fifth -> root falling over 0.5 s"),
    ("3 SHORT", dict(L=0.3, rise=0, rdb=0),
     "DROP in 0.3 s (the picture's ring contracts over 0.3 s)"),
    ("4 LONG", dict(L=0.8, rise=0, rdb=0),
     "DROP in 0.8 s: a slower setting"),
]
CLOSE_CONTROLS = [
    ("0 AGAIN", "the cast itself at the close's gain -- not reversed"),
    ("0 LITERAL", "the picked cast's samples reversed (reference; cannot ship)"),
]

CLOSE_SRC = r"""((S, cp, sp, g, sw, gc) => (t) => {
  const f0 = 440 * Math.pow(2, sp.st / 12), f1 = f0 * 1.5, L = cp.L, R = cp.rise, top = g * gc;
  let c = 0;
  const strike = (s, f, gg, to) => {
    const o = S._tone(t + s, { freq: f, to: to, gain: gg, dur: sp.D, type: "triangle" });
    if (sp.fix) o.frequency.value = f;
    const o2 = S._tone(t + s, { freq: 2 * f, to: to && 2 * to, gain: gg * sp.oct, dur: sp.D, type: "sine" });
    if (sp.fix) o2.frequency.value = 2 * f;
    c += 2;
  };
  const lv = (s) => s < R ? top * Math.pow(10, -cp.rdb * (1 - s / R) / 20)
                          : top * Math.pow(10, -sw * (s - R) / L / 20);
  if (sp.mode === "glide"){
    const dt = Math.max(1, Math.round(f1 * sp.every)) / f1;
    for (let k = 0; k * dt < R - 1e-9; k++) strike(k * dt, f1, lv(k * dt), null);
    const Lg = Math.log(2 / 3), N = Math.max(1, Math.round(f1 * sp.every));
    for (let k = 0; ; k += N){
      const u = L / Lg * Math.log(1 + k * Lg / (f1 * L));
      if (!(u < L)) break;
      strike(R + u, f1 * Math.pow(2 / 3, u / L), lv(R + u), f1 * Math.pow(2 / 3, (u + sp.D) / L));
    }
    return c;
  }
  const seg = sp.mode === "dyad" ? [[f1, 0, R + L / 2], [f0, 0, R + L]]
                                 : [[f1, 0, R + L / 2], [f0, R + L / 2, R + L]];
  for (const [f, s0, s1] of seg){
    const dt = Math.max(1, Math.round(f * sp.every)) / f;
    const q = Math.pow(0.0001 / lv(s0), dt / sp.D);
    for (let k = 0; s0 + k * dt < s1 - 1e-9; k++){
      const s = s0 + k * dt, gs = lv(s);
      strike(s, f, k ? gs : Math.max(gs, gs * sp.a0 / (1 - q)), null);
    }
  }
  return c;
})"""

for _k, _src in (("cast", CAST_SRC), ("tick", TICK_SRC), ("close", CLOSE_SRC)):
    _bad = re.findall(r"Math\.random|\brng\b|spawnFx", _src)
    if _bad:
        raise SystemExit(f"REFUSING: the {_k} candidates name {_bad} -- a voice "
                         "must draw no random number.")

# ------------------------------------------------------------ THE ROWS -----
# Three edits to 02-chain/sc-zenith.html. The Sfx row ADDS three arms before
# the shared rune-crack fallback and re-emits the fallback's own line
# unchanged; the two tickSun rows add the calls. All generated from the picks
# and the rounded constants, then CHECKED in the page (see the docstring).
SFX_ANCHOR = '        } else {                                        // rune-crack'

CLOSE_ANCHOR = '      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }'
CLOSE_CODE = '''      /* ZENITH'S CLOSE (v71 §6.2: "the swell reversed, quiet"): on the frame
         the window runs out BY ITS CLOCK with the caster alive -- never on a
         death, and never once the fight is over, because step() stops calling
         this. Presentation only: SFX.play draws nothing, is a no-op headless,
         and nothing here is read back (zenith_voice_lab: fights identical). */
      if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "morningstar-close" });
      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }'''

TICK_ANCHOR = '      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }'
TICK_CODE = '''      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }
      /* ZENITH'S TICK AND HEAL (v71 §6.2), once per tick, after both applies:
         the chime pitched by the foe's smite stacks, and the heal is the
         EXISTING spark-collect voice pitched by the caster's blessing stacks,
         called exactly as Lastlight calls it. Plain-number opts; SFX.play is a
         no-op headless and reads nothing back (zenith_voice_lab: fights
         identical with and without these two lines). */
      SFX.play("ult", { w: "morningstar-tick", n: foe.stacks("smite") });
      if (u.bless > 0) SFX.play("spark", { collect: true, n: f.stacks("blessing") });'''


def fmt(v):
    """A constant as the arm prints it -- and as every measured render uses."""
    r = repr(float(v))
    return r[:-2] if r.endswith(".0") else r


def seg_loop(indent, gexpr, segs, sp, osc_gain="a"):
    """The re-struck degrees, as the arm writes them (CAST_SRC / CLOSE_SRC's
    segment branch, verbatim in its arithmetic)."""
    i = " " * indent
    return (
        f"{i}for (const [f, s0, s1] of {segs}){{\n"
        f"{i}  const dt = Math.max(1, Math.round(f * {fmt(sp['every'])})) / f;\n"
        f"{i}  const q = Math.pow(0.0001 / lv(s0), dt / {fmt(sp['D'])});\n"
        f"{i}  for (let k = 0; s0 + k * dt < s1 - 1e-9; k++){{\n"
        f"{i}    const s = s0 + k * dt, gs = lv(s);\n"
        f"{i}    const a = k ? gs : Math.max(gs, gs * {fmt(sp['a0'])} / (1 - q));\n"
        f"{i}    this._tone(t + s, {{ freq: f, gain: a, dur: {fmt(sp['D'])}, type:\"triangle\" }}).frequency.value = f;\n"
        f"{i}    this._tone(t + s, {{ freq: 2 * f, gain: a * {fmt(sp['oct'])}, dur: {fmt(sp['D'])}, type:\"sine\" }}).frequency.value = 2 * f;\n"
        f"{i}  }}\n"
        f"{i}}}")


def glide_loop(indent, sp, down, R="0"):
    i = " " * indent
    fs, r = ("f1", "2 / 3") if down else ("f0", "1.5")
    off = f"({R} + u)" if down else "u"
    return (
        f"{i}const Lg = Math.log({r}), N = Math.max(1, Math.round({fs} * {fmt(sp['every'])}));\n"
        f"{i}for (let k = 0; ; k += N){{\n"
        f"{i}  const u = L / Lg * Math.log(1 + k * Lg / ({fs} * L));\n"
        f"{i}  if (!(u < L)) break;\n"
        f"{i}  const f = {fs} * Math.pow({r}, u / L), to = {fs} * Math.pow({r}, (u + {fmt(sp['D'])}) / L), a = lv({off});\n"
        f"{i}  this._tone(t + {off}, {{ freq: f, to: to, gain: a, dur: {fmt(sp['D'])}, type:\"triangle\" }}).frequency.value = f;\n"
        f"{i}  this._tone(t + {off}, {{ freq: 2 * f, to: 2 * to, gain: a * {fmt(sp['oct'])}, dur: {fmt(sp['D'])}, type:\"sine\" }}).frequency.value = 2 * f;\n"
        f"{i}}}")


def _comment(paras, indent=10, width=79):
    """A /* */ block at the arm's indent, each paragraph wrapped to `width`."""
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


def arm_text(C_, K_, Z_, info):
    """The Sfx row's code: the three arms plus the fallback's own line."""
    sp, g, sw = C_["sp"], C_["g"], C_["sw"]
    tp, tg, tD = K_["tp"], K_["g"], K_["D"]
    cp, gc = Z_["cp"], Z_["gc"]
    cname, kname, zname = C_["name"].split()[1], K_["name"].split()[1], Z_["name"].split()[1]
    L = fmt(sp["L"])
    if sp["mode"] == "glide":
        cast_body = (f"          const L = {L}, lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);\n"
                     + glide_loop(10, sp, down=False))
    else:
        segs = ("[[f0, 0, L], [f1, L / 2, L]]" if sp["mode"] == "dyad"
                else "[[f0, 0, L / 2], [f1, L / 2, L]]")
        cast_body = (f"          const L = {L}, lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);\n"
                     + seg_loop(10, "g", segs, sp))
    shape = {"step": "the root re-struck for the first half and the fifth for the second",
             "dyad": "the root re-struck throughout and the fifth joining at the half",
             "glide": "one chirp from the root to the fifth, struck at its own cycle starts"}[sp["mode"]]
    R = fmt(cp["rise"])
    if sp["mode"] == "glide":
        close_body = (f"          const L = {fmt(cp['L'])}, R = {R}, top = {fmt(g)} * {fmt(gc)}, sw = {fmt(sw)};\n"
                      f"          const lv = (s) => s < R ? top * Math.pow(10, -{fmt(cp['rdb'])} * (1 - s / R) / 20)\n"
                      f"                                  : top * Math.pow(10, -sw * (s - R) / L / 20);\n"
                      f"          const dt = Math.max(1, Math.round(f1 * {fmt(sp['every'])})) / f1;\n"
                      f"          for (let k = 0; k * dt < R - 1e-9; k++){{\n"
                      f"            this._tone(t + k * dt, {{ freq: f1, gain: lv(k * dt), dur: {fmt(sp['D'])}, type:\"triangle\" }}).frequency.value = f1;\n"
                      f"            this._tone(t + k * dt, {{ freq: 2 * f1, gain: lv(k * dt) * {fmt(sp['oct'])}, dur: {fmt(sp['D'])}, type:\"sine\" }}).frequency.value = 2 * f1;\n"
                      f"          }}\n"
                      + glide_loop(10, sp, down=True, R="R"))
    else:
        segs = ("[[f1, 0, R + L / 2], [f0, 0, R + L]]" if sp["mode"] == "dyad"
                else "[[f1, 0, R + L / 2], [f0, R + L / 2, R + L]]")
        close_body = (f"          const L = {fmt(cp['L'])}, R = {R}, top = {fmt(g)} * {fmt(gc)}, sw = {fmt(sw)};\n"
                      f"          const lv = (s) => s < R ? top * Math.pow(10, -{fmt(cp['rdb'])} * (1 - s / R) / 20)\n"
                      f"                                  : top * Math.pow(10, -sw * (s - R) / L / 20);\n"
                      + seg_loop(10, "top", segs, sp))
    if tp["mode"] == "tink":
        tick_body = (f"          [[1, 1.00], [2.76, 0.42], [5.40, 0.16]].forEach(([r, k]) =>\n"
                     f"            this._tone(t, {{ freq: f * r, gain: {fmt(tg)} * k, dur: {fmt(tD)}, type:\"triangle\" }}));")
    elif tp["mode"] == "soft":
        tick_body = (f"          [[1, 1.00], [2.76, 0.25]].forEach(([r, k]) =>\n"
                     f"            this._tone(t, {{ freq: f * r, gain: {fmt(tg)} * k, dur: {fmt(tD)}, type:\"triangle\" }}));")
    else:
        tick_body = (f"          this._tone(t, {{ freq: f, gain: {fmt(tg)}, dur: {fmt(tD)}, type:\"triangle\" }});\n"
                     f"          this._burst(t, {{ freq: 6000, q: 0.8, gain: {fmt(tg)} * 0.8, dur: 0.008, type:\"highpass\" }});")
    root = {27: "C7", 3: "C5"}.get(tp["st"], f"A4+{tp['st']}")
    tdesc = {"tink": "a struck bar, BAR's modes 1 : 2.76 : 5.40",
             "soft": "a struck bar with its top mode off and the second at 0.25",
             "ping": "a triangle note on an 8 ms click"}[tp["mode"]]
    aud = (f"{info['tick_aud_lo']:.0f}" if info['tick_aud_lo'] == info['tick_aud_hi']
           else f"{info['tick_aud_lo']:.0f}-{info['tick_aud_hi']:.0f}")
    rise_txt = (f", after a {fmt(cp['rise'])} s climb that is the cast's own release reversed"
                if cp["rise"] else "")
    c_cast = _comment([
        f'ZENITH\'S CAST -- v71 §6.2: "a bright swell, 0.5s, a rising fifth in a '
        f'sustained-by-restrike tone -- the sun coming up". {cname}, of four, picked on the '
        f'numbers by `zenith_voice_lab.py` under Rick\'s "you pick i overrule" (v98). '
        f'Morningstar had no arm and fell through to rune-crack, which Lastlight, Aureole and '
        f'Censer still use, so this ADDS arms before that fallback and leaves it alone.',
        f"D5 -> A5, a just fifth (iv -> i of the score's A minor): {shape}, in a triangle with "
        f"a sine an octave over it at {fmt(sp['oct'])} -- bright, centroid {info['cen']:.0f} Hz "
        f"against Daybreak's line's {info['dawn_cen']:.0f}. It swells {info['swell']:.1f} dB, tops "
        f"out {info['top_at']:.0f} ms after the cast at {info['top_db']:+.1f} dB re Morningstar's "
        f"own blow (the hit at 24), and is gone by {info['gone']:.0f} ms. Register "
        f"{info['rc_reg']:.2f} against rune-crack, {info['bar_reg']:.2f} against Corollary's BAR, "
        f"{info['dawn_reg']:.2f} against Daybreak's cast.",
        f"A HELD NOTE DOES NOT EXIST IN THIS TOOLKIT (CLAUDE.md 4.5), so each degree is "
        f"RE-STRUCK every whole number of cycles nearest {round(sp['every'] * 1000)} ms, in phase, "
        f"each strike {fmt(sp['D'])} s long, the level climbing in a straight line in dB; a "
        f"degree's first strike carries {fmt(sp['a0'])} of the plateau. At half the strikes "
        f"(22 ms) the re-strikes read as a {info['lean_flut']:.1f} dB flutter. "
        f"`.frequency.value = f` AFTER `_tone` IS LOAD-BEARING (v97 §4b): without it the "
        f"strikes land out of phase above ~500 Hz -- the lab's RAW control dips "
        f"{info['raw_dips']} times on the way up and tops out {info['raw_db']:.1f} dB lower."])
    c_tick = _comment([
        f'A TICK -- "a soft chime, 60ms, quiet (peak <=0.35), pitch by smite count" (v71 '
        f'§6.2). {kname}, of four (`zenith_voice_lab.py`): {tdesc}. `tickSun` plays it once '
        f'per tick with n = the foe\'s smite stacks after the tick (1-4; every count 0-4 is its '
        f'own note of the A-minor pentatonic from {root}: {info["tick_pitches"]} Hz).',
        f"Audible {aud} ms, peak {info['tick_peak']:.3f} at most, {info['tick_hit_db']:+.1f} dB "
        f"re the blow and {info['tick_wall_db']:+.1f} dB re the wall tick. It lands on the same "
        f"frame as the heal -- the unchanged `spark` collect, 1.3-1.7 kHz -- and sits above it: "
        f"register {info['tick_spark_reg']:.2f} at most against any heal, and each keeps its own "
        f"band within {info['keep']:.1f} dB when the two land together."])
    c_close = _comment([
        f'CLOSE -- "the swell reversed, quiet" (v71 §6.2). {zname}, of four '
        f'(`zenith_voice_lab.py`): the cast\'s own figure run backwards, the fifth first and '
        f'falling to the root, the level falling from the top{rise_txt}. '
        f'{info["close_db"]:+.1f} dB under the cast\'s top; gone {info["close_gone"]:.0f} ms '
        f'after the window shuts. Envelope correlation {info["close_corr"]:.2f} with the literal '
        f'reversal, which cannot ship: it needs an async render, and every clip rebuilds this '
        f'synth synchronously (v88 §6b). `tickSun` plays it only when the window closes by its '
        f'clock, never on a death.'])
    return f'''        }} else if (w === "morningstar"){{                // the sun comes up
{c_cast}
          const f0 = 440 * Math.pow(2, {ST0} / 12), f1 = f0 * 1.5, g = {fmt(g)}, sw = {fmt(sw)};
{cast_body}
        }} else if (w === "morningstar-tick"){{           // the light lands
{c_tick}
          const n = Math.max(0, Math.min(4, p.n | 0));
          const f = 440 * Math.pow(2, ([0, 2, 4, 7, 9][n] + {tp['st']}) / 12);
{tick_body}
        }} else if (w === "morningstar-close"){{          // and it sets
{c_close}
          const f0 = 440 * Math.pow(2, {ST0} / 12), f1 = f0 * 1.5;
{close_body}
{SFX_ANCHOR}'''


# ------------------------------------------------------------ THE RENDER ---
# events, each rendered at its own time on ONE synth:
#   ["play",  at, kind, p]                 SFX.play(kind, p)
#   ["cast",  at, i, g, sw]                cast candidate i (CAST_SPECS)
#   ["tick",  at, i, g, D, n]              tick candidate i, count n
#   ["close", at, j, ci, g, sw, gc]        close j on cast ci's figure
#   ["lit",   at, ci, g, sw, gc]           cast ci rendered dry, reversed, x gc
#   ["arm",   at, kind, p]                 the PATCHED play (the Sfx row)
RENDER_JS = r"""async ([evs, secs, seed, specs, row]) => {
  const OC = window.OfflineAudioContext, sr = 48000;
  const proto = Object.getPrototypeOf(AC.SFX);
  const mkNoise = (oc) => {
    const n = Math.floor(sr * 0.6), nb = oc.createBuffer(1, n, sr);
    const d = nb.getChannelData(0); let s = (seed || 0x9e3779b9) >>> 0;
    for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17;
      s ^= s << 5; s >>>= 0; d[i] = (s / 4294967296) * 2 - 1; }
    return nb; };
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
  const CAST = (0, eval)(window.__zCast), TICK = (0, eval)(window.__zTick), CLOSE = (0, eval)(window.__zClose);
  let patched = null;
  if (row){
    const src = proto.play.toString();
    const at = src.split(row[0]).length - 1;
    if (at !== 1) return { err: `the Sfx anchor occurs ${at} times in play()` };
    patched = (0, eval)("(function " + src.replace(row[0], () => row[1]) + ")");
  }
  const oc = new OC(1, Math.round(sr * secs), sr);
  const Y = synth(oc, true);
  const calls = [];
  for (const e of evs){
    Y.at(e[1]);
    const before = Y.log.tone + Y.log.burst.length + Y.log.sweep.length;
    if (e[0] === "play") Y.S.play(e[2], e[3]);
    else if (e[0] === "arm") patched.call(Y.S, e[2], e[3]);
    else if (e[0] === "steady")      /* one long strike, in phase: FLUTTER's floor */
      Y.S._tone(e[1], { freq: e[2], gain: e[3], dur: e[4], type: "triangle" }).frequency.value = e[2];
    else if (e[0] === "cast") CAST(Y.S, specs.cast[e[2]], e[3], e[4])(e[1]);
    else if (e[0] === "tick") TICK(Y.S, specs.tick[e[2]], e[3], e[4])(e[1], e[5]);
    else if (e[0] === "close") CLOSE(Y.S, specs.close[e[2]], specs.cast[e[3]], e[4], e[5], e[6])(e[1]);
    else if (e[0] === "lit"){
      const dc = new OC(1, Math.round(sr * secs), sr), Z = synth(dc, false);
      Z.at(1.0); CAST(Z.S, specs.cast[e[2]], e[3], e[4])(1.0);
      const dry = (await dc.startRendering()).getChannelData(0);
      let a = 0, b = dry.length - 1; const TH = 1e-6;
      while (a < dry.length && Math.abs(dry[a]) < TH) a++;
      while (b > a && Math.abs(dry[b]) < TH) b--;
      const seg = dry.slice(a, b + 1).reverse();
      for (let i = 0; i < seg.length; i++) seg[i] *= e[5];
      const rb = oc.createBuffer(1, seg.length, sr); rb.copyToChannel(seg, 0);
      const src = oc.createBufferSource(); src.buffer = rb;
      src.connect(Y.S.bus); src.start(e[1]);
    }
    calls.push(Y.log.tone + Y.log.burst.length + Y.log.sweep.length - before);
  }
  const buf = await oc.startRendering();
  const d = buf.getChannelData(0);
  const u8 = new Uint8Array(d.buffer, d.byteOffset, d.byteLength);
  let s = ""; for (let i = 0; i < u8.length; i += 0x8000)
    s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return { pcm: btoa(s), log: Y.log, calls };
}"""

BED_JS = r"""async ([secs]) => {
  /* the score exactly as cinema_clip mixes it: bed() on a plain bus, x0.9 */
  const ob = new OfflineAudioContext(1, Math.ceil(secs * 48000), 48000);
  const S2 = Object.create(Object.getPrototypeOf(AC.SFX));
  S2.ok = true; S2.on = true; S2.ctx = ob;
  S2.bus = ob.createGain(); S2.bus.connect(ob.destination);
  let s = 0x9e3779b9 >>> 0; const n = Math.floor(48000 * 0.6);
  const nb = ob.createBuffer(1, n, 48000), d = nb.getChannelData(0);
  for (let i = 0; i < n; i++){ s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5;
    s >>>= 0; d[i] = (s / 4294967296) * 2 - 1; }
  S2.noise = nb;
  S2.bed.call(S2, 0, secs, []);
  const b = await ob.startRendering(), x = b.getChannelData(0);
  for (let i = 0; i < x.length; i++) x[i] *= 0.9;
  const u8 = new Uint8Array(x.buffer, x.byteOffset, x.byteLength);
  let t = ""; for (let i = 0; i < u8.length; i += 0x8000)
    t += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(t);
}"""

# main-thread cost of one call through the PATCHED play
COST_JS = r"""([row, reps]) => {
  const proto = Object.getPrototypeOf(AC.SFX);
  const src = proto.play.toString();
  const patched = (0, eval)("(function " + src.replace(row[0], () => row[1]) + ")");
  const oc = new OfflineAudioContext(1, 48000 * 4, 48000);
  const S = Object.create(proto); S.ok = true; S.on = true; S.ctx = oc;
  S.bus = S.constructor.buildChain(oc, oc.destination);
  S.noise = oc.createBuffer(1, 28800, 48000);
  const med = (v) => v.slice().sort((x, y) => x - y)[v.length >> 1];
  const out = {};
  for (const [k, p] of [["cast", { w: "morningstar" }], ["tick", { w: "morningstar-tick", n: 2 }],
                        ["close", { w: "morningstar-close" }]]){
    const v = [];
    for (let i = 0; i < reps; i++){ const a = performance.now(); patched.call(S, "ult", p); v.push(performance.now() - a); }
    out[k] = med(v);
  }
  return out;
}"""

# The tickSun rows, applied to the real prototype and run beside the original;
# the survey of Zenith's windows comes out of the same runs.
WIRE_JS = r"""([seeds, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const orig = P.tickSun; let src = orig.toString();
  for (const [anc, code] of rows){
    const at = src.split(anc).length - 1;
    if (at !== 1) return { err: `a tickSun anchor occurs ${at} times in tickSun()` };
    src = src.replace(anc, () => code);
  }
  if ((0, eval)("SFX") !== S) return { err: "SFX is not AC.SFX -- the wrapper would not see the calls" };
  const patched = (0, eval)("(function " + src + ")");
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "morningstar");
  const run = (side, fid, sd, wire) => {
    const m = side ? new AC.Match(fid, "morningstar", sd) : new AC.Match("morningstar", fid, sd);
    const f = side ? m.b : m.a, foe = side ? m.a : m.b;
    const calls = []; let inSun = 0, step = 0;
    const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
    S.play = function(kind, p){
      const zen = kind === "ult" && p && typeof p.w === "string" && p.w.startsWith("morningstar");
      const heal = kind === "spark" && p && p.collect && inSun;
      if (zen || heal) calls.push({ step, t: m.t, k: heal ? "heal" : p.w, n: p.n === undefined ? null : p.n,
                                    inSun: !!inSun, stk: heal ? f.stacks("blessing") : foe.stacks("smite") });
      return op.call(this, kind, p); };
    const impl = wire ? patched : orig;
    P.tickSun = function(dt){ inSun++; try { return impl.call(this, dt); } finally { inSun--; } };
    const wins = []; let prev = null, W = null, n = 0, lastTicks = 0;
    try {
      while (!m.over && n < 170 / DT){
        step = n; m.step(DT); n++;
        const Z = f.ultSun, T = f.sunTally;
        if (Z && Z !== prev){ if (W && !W.end && prev){ W.end = "recast"; W.endStep = step; }
                              W = { cast: m.t, castStep: step, ticks: [], end: null, endStep: null }; wins.push(W); }
        if (T && T.ticks > lastTicks){ for (let k = lastTicks; k < T.ticks; k++) W && W.ticks.push([step, m.t]); lastTicks = T.ticks; }
        if (!Z && prev){ W.end = (f.alive && prev.t >= prev.dur) ? "clock" : "death"; W.endStep = step; W.close = m.t; }
        prev = Z;
      }
      if (W && !W.end) W.end = "over";
    } finally { P.tickSun = orig; if (had) S.play = op; else delete S.play; }
    const T = f.sunTally || {};
    return { sum: [m.over, +m.t.toFixed(9), +m.a.hp.toFixed(9), +m.b.hp.toFixed(9),
                   T.casts || 0, T.ticks || 0, +(T.dealt || 0).toFixed(9), T.bless || 0,
                   T.litFrames || 0, T.frames || 0], calls, wins };
  };
  let fights = 0, same = 0; const diff = [], bad = [];
  const ends = { clock: 0, death: 0, over: 0, recast: 0 };
  let casts = 0, ticks = 0, tickVoices = 0, heals = 0, closes = 0;
  const tn = [0, 0, 0, 0, 0, 0], hn = [0, 0, 0, 0, 0, 0, 0], perWin = [], gaps = [], nearCast = [0, 0];
  const pick = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const A = run(side, fid, sd, false), B = run(side, fid, sd, true);
    fights++;
    if (JSON.stringify(A.sum) === JSON.stringify(B.sum)) same++; else diff.push([side, fid, sd, A.sum, B.sum]);
    if (A.calls.some(c => c.k !== "morningstar")) bad.push([fid, sd, "the UNPATCHED run played a Zenith voice"]);
    const castV = B.calls.filter(c => c.k === "morningstar");
    if (castV.length !== B.wins.length) bad.push([fid, sd, "cast voices vs windows", castV.length, B.wins.length]);
    if (castV.some(c => c.inSun)) bad.push([fid, sd, "a cast voice from inside tickSun"]);
    for (const c of B.calls) if (c.k !== "morningstar" && !c.inSun) bad.push([fid, sd, "a Zenith voice outside tickSun", c.k]);
    const bySt = {};
    for (const c of B.calls) (bySt[c.step] = bySt[c.step] || []).push(c);
    for (const W of B.wins){
      ends[W.end]++; casts++; ticks += W.ticks.length; perWin.push(W.ticks.length);
      for (let i = 1; i < W.ticks.length; i++) gaps.push(W.ticks[i][1] - W.ticks[i - 1][1]);
      for (const [st, tt] of W.ticks) nearCast[tt - W.cast < 0.75 ? 0 : 1]++;
      const cl = B.calls.filter(c => c.k === "morningstar-close" && c.step >= W.castStep &&
                                     (W.endStep === null || c.step <= W.endStep));
      if (W.end === "clock"){
        if (cl.length !== 1) bad.push([fid, sd, "clock window closes", cl.length]);
        else if (cl[0].step !== W.endStep) bad.push([fid, sd, "close not on the window's last step", cl[0].step, W.endStep]);
      } else if (cl.length) bad.push([fid, sd, W.end + " window played a close"]);
      if (W.end === "clock" && W.ticks.length >= 5) pick.push({ side, foe: fid, seed: sd, cast: W.cast, close: W.close, ticks: W.ticks.length });
    }
    /* per step: exactly one tick voice and one heal for every tick */
    const tickSteps = {};
    for (const W of B.wins) for (const [st] of W.ticks) tickSteps[st] = (tickSteps[st] || 0) + 1;
    const keys = new Set([...Object.keys(tickSteps), ...Object.keys(bySt)]);
    for (const k of keys){
      const nt = tickSteps[k] || 0, cs = bySt[k] || [];
      const tv = cs.filter(c => c.k === "morningstar-tick"), hv = cs.filter(c => c.k === "heal");
      if (tv.length !== nt || hv.length !== nt) bad.push([fid, sd, "step " + k, "ticks", nt, "tick voices", tv.length, "heals", hv.length]);
      for (const c of tv){ tn[Math.max(0, Math.min(5, c.n))]++; if (c.n !== c.stk || c.n < 1 || c.n > 4) bad.push([fid, sd, "tick n", c.n, c.stk]); }
      for (const c of hv){ hn[Math.max(0, Math.min(6, c.n))]++; if (c.n !== c.stk || c.n < 1 || c.n > 5) bad.push([fid, sd, "heal n", c.n, c.stk]); }
      tickVoices += tv.length; heals += hv.length;
    }
    closes += B.calls.filter(c => c.k === "morningstar-close").length;
  }
  return { fights, same, diff: diff.slice(0, 4), ends, casts, ticks, tickVoices, heals, closes,
           tn, hn, perWin, gaps, nearCast, pick, bad: bad.slice(0, 12), nbad: bad.length };
}"""

# One real fight re-run with the rows, every SFX call recorded with its match
# time and whether it is one of Zenith's.
RECORD_JS = r"""([side, fid, sd, rows]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.SFX;
  const orig = P.tickSun; let src = orig.toString();
  for (const [anc, code] of rows) src = src.replace(anc, () => code);
  const patched = (0, eval)("(function " + src + ")");
  const m = side ? new AC.Match(fid, "morningstar", sd) : new AC.Match("morningstar", fid, sd);
  const ev = []; let inSun = 0;
  const had = Object.prototype.hasOwnProperty.call(S, "play"), op = S.play;
  S.play = function(kind, p){
    const zen = (kind === "ult" && p && typeof p.w === "string" && p.w.startsWith("morningstar")) ||
                (kind === "spark" && p && p.collect && inSun > 0);
    ev.push([m.t, kind, JSON.parse(JSON.stringify(p || {})), zen]);
    return op.call(this, kind, p); };
  P.tickSun = function(dt){ inSun++; try { return patched.call(this, dt); } finally { inSun--; } };
  try { let n = 0; while (!m.over && n < 170 / DT){ m.step(DT); n++; } }
  finally { P.tickSun = orig; if (had) S.play = op; else delete S.play; }
  return ev;
}"""


# ------------------------------------------------------------ MEASURING ----
def _np():
    import numpy as np
    return np


def pcm(r):
    np = _np()
    if "err" in r:
        raise SystemExit(r["err"])
    return np.frombuffer(base64.b64decode(r["pcm"]), dtype="<f4").astype(np.float64)


def env(x, win, hop=0.005):
    np = _np()
    W = int(SR * win); H = int(SR * hop)
    c = np.concatenate([[0.0], np.cumsum(x * x)])
    idx = np.arange(0, max(1, len(x) - W), H)
    return np.sqrt(np.maximum(c[idx + W] - c[idx], 0) / W), (idx + W / 2) / SR


def db(v):
    return 20 * math.log10(max(float(v), 1e-9))


BANDS = [25 * 2 ** (k / 3) for k in range(0, 29)]


def bands(y):
    np = _np()
    P = np.abs(np.fft.rfft(y)) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / SR)
    return np.array([np.sqrt(P[(fr >= fc / 2 ** (1 / 6)) & (fr < fc * 2 ** (1 / 6))].sum()) for fc in BANDS])


def cos(a, b):
    np = _np()
    return float(np.dot(a, b) / ((np.linalg.norm(a) * np.linalg.norm(b)) or 1))


def band_rms(x, fc, a, b):
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    X = np.fft.rfft(seg); fr = np.fft.rfftfreq(len(seg), 1 / SR)
    m = (fr >= fc / 2 ** (1 / 6)) & (fr < fc * 2 ** (1 / 6))
    return float(np.sqrt(2 * (np.abs(X[m]) ** 2).sum()) / len(seg))


def pitch(x, a, b, lo=150.0, hi=9000.0):
    """FFT peak (Hann, zero-padded, parabolic) over [a, b] s of x, in Hz."""
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    m = np.nonzero((fr > lo) & (fr < hi))[0]
    i = int(m[np.argmax(X[m])])
    y0, y1, y2 = np.log(X[i - 1:i + 2] + 1e-20)
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
    return (i + d) * SR / NF


def top_note(x, a, b, lo=300.0, hi=1500.0, within=3.0):
    """The HIGHEST note sounding over [a, b]: the highest-frequency spectral
    peak within `within` dB of the strongest, 300-1500 Hz. The timbre's octave
    sine (0.4, against a triangle whose fundamental is 8/pi^2 of its
    amplitude) sits 6.1 dB under its own note, so 3 dB separates a NOTE from
    the timbre's partial -- at 6 dB it read DYAD's root octave (D6) as its top
    note. Parabolic-refined."""
    np = _np()
    seg = x[int(a * SR):int(b * SR)]
    seg = seg * np.hanning(len(seg))
    NF = 1 << 18
    X = np.abs(np.fft.rfft(seg, NF)); fr = np.fft.rfftfreq(NF, 1 / SR)
    m = np.nonzero((fr > lo) & (fr < hi))[0]
    Xm = X[m]; top = Xm.max()
    pk = [k for k in range(1, len(m) - 1) if Xm[k] >= Xm[k - 1] and Xm[k] >= Xm[k + 1]
          and Xm[k] >= top * 10 ** (-within / 20)]
    i = int(m[max(pk)])
    y0, y1, y2 = np.log(X[i - 1:i + 2] + 1e-20)
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) if (y0 - 2 * y1 + y2) else 0.0
    return (i + d) * SR / NF


def cents(f, ref):
    return 1200 * math.log2(f / ref)


def flutter(x, a, b, f):
    """p95 - p5 (dB) of the RMS over four whole periods of f (1 ms hop) about
    its own 100 ms moving average, inside [a, b] (v97)."""
    np = _np()
    W = int(round(4 * SR / f)); H = int(0.001 * SR)
    o = int((a - 0.06) * SR)
    seg = x[o:int((b + 0.06) * SR)]
    c = np.concatenate([[0.0], np.cumsum(seg * seg)])
    idx = np.arange(0, len(seg) - W, H)
    e = 20 * np.log10(np.maximum(np.sqrt(np.maximum(c[idx + W] - c[idx], 0) / W), 1e-7))
    ma = np.convolve(e, np.ones(100) / 100, mode="same")
    tc = (o + idx + W / 2) / SR
    d = (e - ma)[(tc >= a) & (tc <= b)]
    return float(np.percentile(d, 95) - np.percentile(d, 5))


def basic(x):
    """The shape of a voice that starts at T0: every number the rules read."""
    np = _np()
    y = x[int(T0 * SR):]
    pk = float(np.abs(y).max())
    e5, _ = env(y, 0.005, 0.005)
    on = np.nonzero(e5 > e5.max() * 0.02)[0]
    a0, a1 = int(on[0]), int(on[-1])
    r50, c50 = env(y, 0.05)
    it = int(np.argmax(r50))
    e1, _ = env(y, 0.001, 0.001)
    m1 = e1.max(); i10 = int(np.argmax(e1 > 0.1 * m1)); i90 = int(np.argmax(e1 > 0.9 * m1))
    e2 = y ** 2
    ec = float((e2 * np.arange(len(y))).sum() / e2.sum() / SR)
    P = np.abs(np.fft.rfft(y)) ** 2; fr = np.fft.rfftfreq(len(y), 1 / SR)
    return dict(peak=pk, pk_ms=float(np.argmax(np.abs(y)) / SR * 1000), a0=a0 * 5.0,
                aud=(a1 - a0 + 1) * 5.0, gone=(a1 + 1) * 5.0, top=float(r50[it]),
                top_at=float(c50[it]), start=float(r50[c50 <= 0.10].max()), rise=float(i90 - i10),
                late=(ec * 1000 - a0 * 5.0) / max((a1 - a0 + 1) * 5.0, 1e-9),
                cen=float((P * fr).sum() / P.sum()), bands=bands(y))


def dips_and_lin(x, top_at):
    np = _np()
    y = x[int(T0 * SR):]
    e25, c25 = env(y, 0.025)
    ip = int(np.argmax(e25)); run = 0.0; dips = 0; indip = False
    for v in e25[:ip + 1]:
        run = max(run, v)
        if run > e25.max() * 0.05 and v < run * 0.708:
            if not indip:
                dips += 1
            indip = True
        else:
            indip = False
    r50, c50 = env(y, 0.05)
    e = 20 * np.log10(np.maximum(r50, 1e-5))
    k = (c50 >= 0.05) & (c50 <= top_at - 0.03)
    if k.sum() >= 3:
        A = np.vstack([c50[k], np.ones(k.sum())]).T
        coef = np.linalg.lstsq(A, e[k], rcond=None)[0]
        lin = float(np.sqrt(np.mean((e[k] - A @ coef) ** 2)))
    else:
        lin = 99.0
    return dips, lin


def env_corr(x, y):
    """ENV-CORR of two voices starting at T0 (see the docstring)."""
    np = _np()
    a = x[int(T0 * SR):]; b = y[int(T0 * SR):]
    ea, _ = env(a, 0.05); eb, _ = env(b, 0.05)
    n = min(len(ea), len(eb))
    da = 20 * np.log10(np.maximum(ea[:n], 1e-9)); dbb = 20 * np.log10(np.maximum(eb[:n], 1e-9))
    da = np.maximum(da, da.max() - 40); dbb = np.maximum(dbb, dbb.max() - 40)
    live = (da > da.max() - 40 + 1e-9) | (dbb > dbb.max() - 40 + 1e-9)
    idx = np.nonzero(live)[0]
    s = slice(0, int(idx[-1]) + 1)
    return float(np.corrcoef(da[s], dbb[s])[0, 1])


def write_wav(path, x, start=T0 - 0.05):
    """Raw level -- NOT normalised. Refuses silence (v42)."""
    np = _np()
    top = float(np.abs(x).max())
    if top < 1e-6:
        raise SystemExit(f"REFUSING TO WRITE {path.name} -- it rendered SILENCE.")
    nz = np.nonzero(np.abs(x) > top * 1e-3)[0]
    a = max(0, int(start * SR)); b = min(len(x), int(nz[-1]) + int(0.08 * SR))
    seg = np.clip(x[a:b], -1, 1)
    w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((seg * 32767).astype("<i2").tobytes())
    w.close()
    return path.stat().st_size


# --------------------------------------------------------------- PICKING ---
# THE RULES, written down before the table is read, so the table can prove a
# pick wrong. Every gate is a word of v71 §6.2 turned into a number; a rule no
# candidate passes exits 1 rather than picking the least bad.
FAILED: list = []

CAST_RULE = (
    "'a swell, 0.5s': TOP centred 400-550 ms after the cast, SWELL +8..+16 dB, "
    "no DIPS on the way up (one swell), GONE <= 850 ms; 'a rising fifth': "
    "START (20-100 ms) within 30 cents of D5 and END (400-480 ms) within 30 "
    "cents of the fifth -- two notes, the second higher; 'sustained-by-restrike': "
    "FLUTTER <= 3 dB inside each degree's plateau; 'bright': CENTROID >= 1.5x "
    "Daybreak's cast's; register vs rune-crack, Daybreak's cast and BAR each "
    "<= 0.80 (not the fallback it replaces, not the school's other cast, not the "
    "batch's other chime). Level: TOP between 0.5x the hit @ 24's loudest 50 ms "
    "on its LOUDEST draw and 1.0x on its QUIETEST (heard like a blow, never over "
    "one); START in its third-octave >= 2x the score's p90 at D5 (the swell is "
    "heard from the cast). Tiebreak: the most distinct register -- the lowest of "
    "its registers vs rune-crack, Daybreak's cast and BAR, to 0.05 -- then the "
    "evenest climb (LINEARITY, to 0.1 dB), then the fewest synth calls.")

# THE CAST TIEBREAK WAS CHANGED ONCE, AND THIS IS WHY. Its first cut was "the
# evenest climb, then the fewest calls", and it split STEP and DYAD on 0.3 dB
# of LINEARITY (0.6 against 0.3) -- a number no one can hear -- while DYAD
# costs half again the synth calls and sits 0.65 against BAR (its sustained D5
# lands in the band of BAR's 659 Hz body) where STEP sits 0.39. The build's
# own instruction names REGISTER as what the cast is picked on ("register
# distinct from rune-crack and the school's other casts"), so the tiebreak now
# leads with it. Recorded rather than hidden: the rule is the pick's.

TICK_RULE = (
    "'60ms': AUDIBLE 50-70 ms at every count; 'a chime' is struck: RISE <= 3 ms "
    "and the peak in the first 10 ms; 'peak <=0.35': the sample peak <= 0.35 at "
    "every count on every noise draw; 'quiet': the loudest 50 ms <= 0.5x the "
    "hit @ 24's on its quietest draw, and >= 2x the wall tick's on its loudest "
    "(heard over the commonest sound); 'pitch by smite count': the pitch at "
    "counts 0-4 rises, each >= 150 cents over the last; it lands on the heal's "
    "frame, so register vs the spark collect <= 0.50 at every (count, "
    "blessing) pair, and vs the wall tick <= 0.80 and vs the picked cast <= "
    "0.80. Tiebreak: the lowest worst register vs the heal (to 0.05), then vs "
    "the wall tick (to 0.05), then the fewest synth calls.")

CLOSE_RULE = (
    "'reversed': the loudest 50 ms on the fifth (within 30 cents) and the end "
    "on the root (within 30 cents) -- the fifth falls; LATE <= 0.45 (the energy "
    "sits early); after the top the level never rises more than 1.5 dB; "
    "ENV-CORR with the LITERAL reversal >= 0.80; 'quiet': the loudest 50 ms "
    "<= 0.5x the cast's (-6 dB), and its third-octave at the fifth >= 2x the "
    "score's p90 there (still heard); GONE <= 1.3 s. Tiebreak: the highest "
    "ENV-CORR (to 0.01), then the fewest synth calls.")


def _gate(rows, name):
    ok = [i for i, M in enumerate(rows) if not M["why"]]
    if not ok:
        print(f"  NO {name.upper()} CANDIDATE PASSES -- the run will exit 1")
        FAILED.append(name)
        return None, min(range(len(rows)), key=lambda i: len(rows[i]["why"]))
    return ok, None


def cast_why(M, lev):
    why = []
    if not 0.400 <= M["top_at"] <= 0.550: why.append(f"top at {M['top_at'] * 1000:.0f} ms, not 400-550")
    if not 8 <= M["swell"] <= 16: why.append(f"swell {M['swell']:+.1f} dB, not +8..+16")
    if M["dips"]: why.append(f"{M['dips']} dips on the way up")
    if M["gone"] > 850: why.append(f"gone at {M['gone']:.0f} ms > 850")
    if abs(M["c_start"]) > 30: why.append(f"starts {M['c_start']:+.0f} c off D5")
    if abs(M["c_end"]) > 30: why.append(f"ends {M['c_end']:+.0f} c off the fifth")
    if M["flut"] > 3: why.append(f"flutter {M['flut']:.1f} dB > 3")
    if M["cen"] < lev["bright"]: why.append(f"centroid {M['cen']:.0f} Hz < {lev['bright']:.0f}")
    for k in ("rc_reg", "dawn_reg", "bar_reg"):
        if M[k] > 0.80: why.append(f"{k} {M[k]:.2f} > 0.80")
    if M["top"] < lev["lo"]: why.append(f"top {M['top']:.4f} < {lev['lo']:.4f}")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f}")
    if M["inb0"] < lev["inb_floor"]: why.append(f"start in-band {M['inb0']:.4f} < {lev['inb_floor']:.4f}")
    return why


def tick_why(M, lev):
    why = []
    if not (50 <= M["aud_lo"] and M["aud_hi"] <= 70): why.append(f"audible {M['aud_lo']:.0f}-{M['aud_hi']:.0f} ms, not 50-70")
    if M["rise"] > 3: why.append(f"rise {M['rise']:.0f} ms > 3")
    if M["pk_ms"] > 10: why.append(f"peak at {M['pk_ms']:.0f} ms")
    if M["peak"] > 0.35: why.append(f"peak {M['peak']:.3f} > 0.35")
    if M["st_hi"] > lev["hi"]: why.append(f"loudest 50 ms {M['st_hi']:.4f} > {lev['hi']:.4f}")
    if M["st_lo"] < lev["lo"]: why.append(f"loudest 50 ms {M['st_lo']:.4f} < {lev['lo']:.4f}")
    if not M["rising"]: why.append("pitch does not rise with the count")
    if M["step_min"] < 150: why.append(f"a count only {M['step_min']:.0f} cents over the last")
    if M["spark_reg"] > 0.50: why.append(f"register vs the heal {M['spark_reg']:.2f} > 0.50")
    if M["wall_reg"] > 0.80: why.append(f"register vs the wall {M['wall_reg']:.2f} > 0.80")
    if M["cast_reg"] > 0.80: why.append(f"register vs the cast {M['cast_reg']:.2f} > 0.80")
    return why


def close_why(M, lev):
    why = []
    if abs(M["c_top"]) > 30: why.append(f"top {M['c_top']:+.0f} c off the fifth")
    if abs(M["c_end"]) > 30: why.append(f"ends {M['c_end']:+.0f} c off the root")
    if M["late"] > 0.45: why.append(f"late {M['late']:.2f} > 0.45")
    if M["rerise"] > 1.5: why.append(f"rises {M['rerise']:.1f} dB after the top")
    if M["corr"] < 0.80: why.append(f"env-corr {M['corr']:.2f} < 0.80")
    if M["top"] > lev["hi"]: why.append(f"top {M['top']:.4f} > {lev['hi']:.4f} (not quiet)")
    if M["inb"] < lev["inb_floor"]: why.append(f"in-band {M['inb']:.4f} < {lev['inb_floor']:.4f}")
    if M["gone"] > 1300: why.append(f"gone at {M['gone']:.0f} ms")
    return why


# render.py's seed first, then eleven other draws
NOISE_SEEDS = [0x9e3779b9] + [(0x2545F491 * (k + 7)) & 0xffffffff or 1 for k in range(11)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-zenith.html")
    ap.add_argument("--out", default="../05-reference/v98")
    ap.add_argument("--seeds", type=int, default=2, help="fight seeds a pairing (the wire check)")
    ap.add_argument("--seed0", type=int, default=98001)
    ap.add_argument("--json", default=None)
    ap.add_argument("--rows", default=None, help="write the three checked rows here")
    a = ap.parse_args()
    np = _np()

    gp = resolve_game(a.game)
    html = gp.read_text(encoding="utf-8")
    out = (HERE / a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"game": gp.name, "rules": {"cast": CAST_RULE, "tick": TICK_RULE, "close": CLOSE_RULE}}
    for nm, anc in (("Sfx", SFX_ANCHOR), ("tickSun close", CLOSE_ANCHOR), ("tickSun tick", TICK_ANCHOR)):
        c = html.count(anc)
        if c != 1:
            raise SystemExit(f"the {nm} anchor occurs {c} times in {gp.name} -- not a row")
    if "morningstar-tick" in html or "morningstar-close" in html:
        raise SystemExit(f"{gp.name} already carries Zenith's voices -- run on stage 4")
    rec["game_sha"] = hashlib.sha256(html.encode()).hexdigest()[:16]
    print(f"\nZENITH -- THE VOICES   game {gp.name} {rec['game_sha']}")
    print("  E50 = 50 ms RMS (5 ms hop); TOP = loudest 50 ms; START = loudest 50 ms in the first "
          "100 ms; SWELL = TOP - START\n"
          "  AUDIBLE = 5 ms RMS above 2% of its own max; DIPS = >3 dB dips of the 25 ms RMS on the "
          "way up; LIN = E50's RMS residual about a line\n"
          "  FLUTTER = p95-p5 of 4-period RMS about its 100 ms mean; REG = 1/3-octave cosine; "
          "IN-BAND = third-octave RMS at a pitch\n"
          "  every render: OfflineAudioContext 48 kHz, first event at t = 1.0, through "
          "Sfx.buildChain, render.py's xorshift noise")

    specs = {"cast": [c[1] for c in CAST_CANDIDATES] +
                     [dict(CAST_CANDIDATES[0][1], fix=False), dict(CAST_CANDIDATES[0][1], mode="struck", D=0.6)],
             "tick": [c[1] for c in TICK_CANDIDATES],
             "close": [c[1] for c in CLOSE_CANDIDATES]}
    RAW_I, STRUCK_I = len(CAST_CANDIDATES), len(CAST_CANDIDATES) + 1

    with game(game_path=gp) as (page, errors):
        ua = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
        print(f"  runtime Chromium {ua}")
        rec["chromium"] = ua
        page.evaluate("([a, b, c]) => { window.__zCast = a; window.__zTick = b; window.__zClose = c; }",
                      [CAST_SRC, TICK_SRC, CLOSE_SRC])

        def R(evs, secs=3.0, seed=None, row=None):
            r = page.evaluate(RENDER_JS, [evs, secs, seed, specs, row])
            assert not errors, errors[:3]
            x = pcm(r)
            for d_ in r["log"]["burst"]:
                if d_ > 0.55: raise SystemExit(f"REFUSING: a _burst of {d_}s in {evs[:2]}")
            for d_ in r["log"]["sweep"]:
                if d_ > 0.58: raise SystemExit(f"REFUSING: a _sweep of {d_}s in {evs[:2]}")
            if float(np.abs(x).max()) < 1e-6:
                raise SystemExit(f"SILENT render: {evs[:2]}")
            if min(e[1] for e in evs) >= T0 and float(np.abs(x[:int(T0 * SR) - 2]).max()) > 1e-6:
                raise SystemExit(f"sound BEFORE t=1.0 in {evs[:2]}")
            return x, r["calls"]

        sizes = {}

        def wav(name, x):
            sizes[name] = write_wav(out / name, x)

        # ---- CONTROLS ------------------------------------------------------
        print("\nCONTROLS -- v88 published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms, "
              "hit@11.6 0.443 / 80 ms. They must come back.")
        ctl = {}
        for name, ev in (("rune-crack", ["play", T0, "ult", {"w": "spellbreaker"}]),
                         ("BAR", ["play", T0, "ult", {"w": "axiom"}]),
                         ("hit@11.6", ["play", T0, "hit", {"dmg": 11.6, "crit": False}]),
                         ("hit@24", ["play", T0, "hit", {"dmg": 24.03, "crit": False}]),
                         ("dawn cast", ["play", T0, "ult", {"w": "dawnbringer"}]),
                         ("wall", ["play", T0, "wall", {}]),
                         ("morningstar now", ["play", T0, "ult", {"w": "morningstar"}]),
                         ("lastlight", ["play", T0, "ult", {"w": "lastlight"}]),
                         ("aureole", ["play", T0, "ult", {"w": "aureole"}]),
                         ("censer", ["play", T0, "ult", {"w": "censer"}])):
            x, _ = R([ev])
            ctl[name] = dict(basic(x), x=x)
            M = ctl[name]
            print(f"  {name:<16} peak {M['peak']:.3f} at {M['pk_ms']:4.0f} ms   audible {M['aud']:5.0f} ms   "
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
        fall = {k: float(np.abs(ctl[k]["x"] - rcx).max()) for k in ("morningstar now", "lastlight", "aureole", "censer")}
        print("  ARE rune-crack today (max |diff| vs ult/spellbreaker): " +
              ", ".join(f"{k} {v:.1e}" for k, v in fall.items()))
        if max(fall.values()) > 1e-6:
            raise SystemExit("a relic this lab says falls through to rune-crack does not")
        rec["fallthrough"] = fall
        sparks = {}
        for n_ in range(1, 6):
            x, _ = R([["play", T0, "spark", {"collect": True, "n": n_}]])
            sparks[n_] = dict(basic(x), x=x)
        print("  spark collect n 1-5: loudest 50 ms " +
              " ".join(f"{sparks[n_]['top']:.4f}" for n_ in sparks) + ", pitch " +
              " ".join(f"{pitch(sparks[n_]['x'], T0, T0 + 0.1):.0f}" for n_ in sparks) + " Hz")
        wav("zenith-ctl-runecrack.wav", rcx)
        wav("zenith-ctl-hit24.wav", ctl["hit@24"]["x"])
        wav("zenith-ctl-spark3.wav", sparks[3]["x"])
        wav("zenith-ctl-dawncast.wav", ctl["dawn cast"]["x"])
        wav("zenith-ctl-bar.wav", ctl["BAR"]["x"])
        # the noise draws
        HD, WD, RCD, BD = [], [], [], []
        for sd in NOISE_SEEDS:
            HD.append(basic(R([["play", T0, "hit", {"dmg": 24.03, "crit": False}]], seed=sd)[0]))
            WD.append(basic(R([["play", T0, "wall", {}]], seed=sd)[0]))
            RCD.append(basic(R([["play", T0, "ult", {"w": "spellbreaker"}]], seed=sd)[0]))
            BD.append(basic(R([["play", T0, "ult", {"w": "axiom"}]], seed=sd)[0]))
        h_lo, h_hi = min(m["top"] for m in HD), max(m["top"] for m in HD)
        w_hi = max(m["top"] for m in WD)
        print(f"  the hit @ 24 across {len(NOISE_SEEDS)} draws: loudest 50 ms {h_lo:.4f}-{h_hi:.4f}, peak "
              f"{min(m['peak'] for m in HD):.3f}-{max(m['peak'] for m in HD):.3f};  the wall tick: "
              f"{min(m['top'] for m in WD):.4f}-{w_hi:.4f}")
        bed = np.frombuffer(base64.b64decode(page.evaluate(BED_JS, [24.0])), dtype="<f4").astype(np.float64)
        bseg = bed[int(2 * SR):int(10 * SR)]

        def bedp90(f):
            return float(np.percentile([band_rms(bseg, f, i / SR, i / SR + 0.25)
                                        for i in range(0, len(bseg) - 12000, 2400)], 90))
        b0, b1 = bedp90(F0), bedp90(F1)
        print(f"  the score's p90 in-band (clip mix): D5 {b0:.5f}, A5 {b1:.5f}")
        rec["levels"] = dict(hit24=[h_lo, h_hi], wall_hi=w_hi, bed_d5=b0, bed_a5=b1)

        def mreg(xb, D_):
            return float(np.median([cos(xb, d["bands"]) for d in D_]))

        # ---- THE CAST ------------------------------------------------------
        lev_c = dict(lo=0.5 * h_hi, hi=1.0 * h_lo, inb_floor=2 * b0, bright=1.5 * ctl["dawn cast"]["cen"])
        tgt_top = math.sqrt(lev_c["lo"] * lev_c["hi"])
        print(f"\nCAST -- 'a bright swell, 0.5s, a rising fifth in a sustained-by-restrike tone'. "
              f"D5 -> A5, triangle + octave sine.\n  level-matched: TOP {tgt_top:.4f} (the centre of "
              f"{lev_c['lo']:.4f}-{lev_c['hi']:.4f}), SWELL +{SWELL_DB:g} dB")

        def calib_cast(i):
            g, sw = 0.03, SWELL_DB
            for _ in range(4):
                M = basic(R([["cast", T0, i, g, sw]])[0])
                g = g * tgt_top / M["top"]
                sw = sw + (SWELL_DB - (db(M["top"]) - db(M["start"])))
            return float(f"{g:.4g}"), round(sw, 2)

        def cast_measure(i, g, sw):
            x, calls = R([["cast", T0, i, g, sw]])
            x2, _ = R([["cast", T0, i, g, sw]])
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"cast {i} does not reproduce")
            M = basic(x)
            M["x"] = x; M["calls"] = calls[0]; M["g"] = g; M["sw"] = sw
            M["swell"] = db(M["top"]) - db(M["start"])
            M["dips"], M["lin"] = dips_and_lin(x, M["top_at"])
            M["c_start"] = cents(pitch(x, T0 + 0.02, T0 + 0.10, lo=300, hi=1500), F0)
            M["c_end"] = cents(top_note(x, T0 + 0.40, T0 + 0.48), F1)
            sp = specs["cast"][i]
            f2 = F0 if sp["mode"] == "dyad" else F1
            M["flut"] = max(flutter(x, T0 + 0.06, T0 + 0.22, F0), flutter(x, T0 + 0.31, T0 + 0.46, f2))
            M["rc_reg"] = mreg(M["bands"], RCD)
            M["dawn_reg"] = cos(M["bands"], ctl["dawn cast"]["bands"])
            M["bar_reg"] = mreg(M["bands"], BD)
            M["inb0"] = band_rms(x, F0, T0 + 0.02, T0 + 0.12)
            return M

        # the flutter metric's floor: ONE steady strike must read ~0
        fl0 = [flutter(R([["steady", T0, f_, 0.02, 3.0]])[0], T0 + 0.35, T0 + 0.95, f_) for f_ in (F0, F1)]
        print(f"  FLUTTER's floor, one steady triangle strike: D5 {fl0[0]:.2f} dB, A5 {fl0[1]:.2f} dB")
        if max(fl0) > 0.5:
            raise SystemExit("the flutter metric reads a steady tone as flutter -- nothing it says is usable")
        rec["flutter_floor"] = fl0
        H_ = (f"  {'cand':<10}{'g':>8}{'sw dB':>7}{'calls':>6}{'top':>8}{'at ms':>6}{'swell':>6}{'dips':>5}"
              f"{'lin':>5}{'gone':>6}{'c0':>5}{'c1':>5}{'flut':>5}{'cen':>6}{'rc':>5}{'dawn':>5}{'bar':>5}{'inb0':>8}")
        print(H_)
        rows_c = []
        for i, (name, sp, blurb) in enumerate(CAST_CANDIDATES):
            g, sw = calib_cast(i)
            M = cast_measure(i, g, sw); M["name"] = name; M["sp"] = sp
            M["why"] = cast_why(M, lev_c)
            rows_c.append(M)
            wav(f"zenith-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        ctlc = []
        for i, name in ((RAW_I, "0 RAW"), (STRUCK_I, "0 STRUCK")):
            M = cast_measure(i, rows_c[0]["g"], rows_c[0]["sw"]); M["name"] = name
            M["sp"] = specs["cast"][i]; M["why"] = cast_why(M, lev_c)
            ctlc.append(M)
            wav(f"zenith-cast-{name.replace(' ', '-').lower()}.wav", M["x"])
        for M in rows_c + ctlc:
            print(f"  {M['name']:<10}{M['g']:>8.4g}{M['sw']:>7.2f}{M['calls']:>6d}{M['top']:>8.4f}{M['top_at'] * 1000:>6.0f}"
                  f"{M['swell']:>6.1f}{M['dips']:>5d}{M['lin']:>5.1f}{M['gone']:>6.0f}{M['c_start']:>5.0f}{M['c_end']:>5.0f}"
                  f"{M['flut']:>5.1f}{M['cen']:>6.0f}{M['rc_reg']:>5.2f}{M['dawn_reg']:>5.2f}{M['bar_reg']:>5.2f}{M['inb0']:>8.4f}")
        for (name, _sp, blurb) in CAST_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        for name, blurb in CAST_CONTROLS:
            print(f"    {name:<9} {blurb}")
        print(f"  gates: top {lev_c['lo']:.4f}-{lev_c['hi']:.4f}, start in-band >= {lev_c['inb_floor']:.4f}, "
              f"centroid >= {lev_c['bright']:.0f} Hz")
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
        ci = fb if ok is None else min(ok, key=lambda i: (round(max(rows_c[i]["rc_reg"], rows_c[i]["dawn_reg"],
                                                                     rows_c[i]["bar_reg"]) / 0.05),
                                                          round(rows_c[i]["lin"], 1), rows_c[i]["calls"]))
        C_ = rows_c[ci]
        rel = C_["gone"] / 1000 - C_["top_at"] - 0.025
        print(f"  PICK  {C_['name']}  g {C_['g']}, swell {C_['sw']} dB going in, {C_['calls']} synth calls; "
              f"TOP {C_['top']:.4f} = {db(C_['top'] / h_lo):+.1f} dB re the hit @ 24 (quietest draw), "
              f"{db(C_['top'] / w_hi):+.1f} dB re the wall; START {db(C_['start'] / h_lo):+.1f} dB re the hit; "
              f"release {rel * 1000:.0f} ms from the top")

        # ---- THE TICK ------------------------------------------------------
        lev_t = dict(lo=2 * w_hi, hi=0.5 * h_lo)
        tgt_t = math.sqrt(lev_t["lo"] * lev_t["hi"])
        print(f"\nTICK -- 'a soft chime, 60ms, quiet (peak <=0.35), pitch by smite count'. Level-matched: "
              f"loudest 50 ms {tgt_t:.4f} (the centre of {lev_t['lo']:.4f}-{lev_t['hi']:.4f}), audible 60 ms at count 2")

        def calib_tick(i):
            g, D = 0.08, 0.10
            for _ in range(5):
                M = basic(R([["tick", T0, i, g, D, 2]])[0])
                g = g * tgt_t / M["top"]
                D = D * 60.0 / M["aud"]
            return float(f"{g:.4g}"), round(D, 3)

        rows_t = []
        print(f"  {'cand':<9}{'g':>8}{'D s':>7}{'calls':>6}{'aud ms':>9}{'peak':>7}{'rise':>5}{'pk@':>5}"
              f"{'st50':>15}{'pitches Hz (count 0-4)':>34}{'step c':>7}{'heal':>6}{'wall':>6}{'cast':>6}")
        for i, (name, tp, blurb) in enumerate(TICK_CANDIDATES):
            g, D = calib_tick(i)
            per = []
            for n_ in range(5):
                x, calls = R([["tick", T0, i, g, D, n_]])
                x2, _ = R([["tick", T0, i, g, D, n_]])
                if float(np.abs(x - x2).max()) > 1e-6:
                    raise SystemExit(f"tick {name} does not reproduce")
                M = basic(x); M["x"] = x; M["calls"] = calls[0]
                M["pitch"] = pitch(x, T0, T0 + 0.06, lo=200, hi=9000)
                draws = [basic(R([["tick", T0, i, g, D, n_]], seed=sd)[0]) for sd in NOISE_SEEDS] \
                    if tp["mode"] == "ping" else [M]
                M["draws"] = draws
                per.append(M)
                if n_ in (1, 4):
                    wav(f"zenith-tick-{name.replace(' ', '-').lower()}-n{n_}.wav", x)
            T = dict(name=name, tp=tp, g=g, D=D, per=per, calls=per[0]["calls"])
            T["aud_lo"] = min(p["aud"] for p in per); T["aud_hi"] = max(p["aud"] for p in per)
            T["rise"] = max(p["rise"] for p in per); T["pk_ms"] = max(p["pk_ms"] for p in per)
            T["peak"] = max(d["peak"] for p in per for d in p["draws"])
            T["st_lo"] = min(d["top"] for p in per for d in p["draws"])
            T["st_hi"] = max(d["top"] for p in per for d in p["draws"])
            ps = [p["pitch"] for p in per]
            T["pitches"] = ps
            T["rising"] = all(ps[k] > ps[k - 1] for k in range(1, 5))
            T["step_min"] = min(cents(ps[k], ps[k - 1]) for k in range(1, 5))
            T["spark_reg"] = max(float(np.median([cos(d["bands"], sparks[m_]["bands"]) for d in p["draws"]]))
                                 for p in per for m_ in sparks)
            T["wall_reg"] = max(float(np.median([cos(d["bands"], w_["bands"]) for d, w_ in
                                                 zip(p["draws"] * (12 // len(p["draws"])), WD)]))
                                for p in per)
            T["cast_reg"] = max(cos(p["bands"], C_["bands"]) for p in per)
            T["why"] = tick_why(T, lev_t)
            rows_t.append(T)
            print(f"  {name:<9}{g:>8.4g}{D:>7.3f}{T['calls']:>6d}{T['aud_lo']:>5.0f}-{T['aud_hi']:<3.0f}"
                  f"{T['peak']:>7.3f}{T['rise']:>5.0f}{T['pk_ms']:>5.0f}{T['st_lo']:>8.4f}-{T['st_hi']:<6.4f}"
                  f"{' '.join(f'{v:5.0f}' for v in ps):>34}{T['step_min']:>7.0f}{T['spark_reg']:>6.2f}"
                  f"{T['wall_reg']:>6.2f}{T['cast_reg']:>6.2f}")
        for (name, _tp, blurb) in TICK_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        print(f"  gates: loudest 50 ms {lev_t['lo']:.4f}-{lev_t['hi']:.4f}, peak <= 0.35")
        print(f"  RULE  {TICK_RULE}")
        for T in rows_t:
            if T["why"]:
                print(f"    {T['name']:<9} out: {'; '.join(T['why'])}")
        ok, fb = _gate(rows_t, "tick")
        ki = fb if ok is None else min(ok, key=lambda i: (round(rows_t[i]["spark_reg"] / 0.05),
                                                          round(rows_t[i]["wall_reg"] / 0.05),
                                                          rows_t[i]["calls"]))
        K_ = rows_t[ki]
        print(f"  PICK  {K_['name']}  g {K_['g']}, D {K_['D']} s; loudest 50 ms {db(K_['st_hi'] / h_lo):+.1f} dB re "
              f"the hit @ 24, {db(K_['st_lo'] / w_hi):+.1f} dB re the wall; {db(K_['st_hi'] / sparks[3]['top']):+.1f} dB "
              f"re the heal it lands with")
        # the chime and the heal on one frame: does each keep itself?
        keep = []
        for n_ in range(1, 5):
            for m_ in (1, 3, 5):
                xl, _ = R([["tick", T0, ki, K_["g"], K_["D"], n_], ["play", T0, "spark", {"collect": True, "n": m_}]])
                fk = K_["pitches"][n_]; fs = pitch(sparks[m_]["x"], T0, T0 + 0.1)
                keep.append((n_, m_, db(band_rms(xl, fk, T0, T0 + 0.06) / band_rms(K_["per"][n_]["x"], fk, T0, T0 + 0.06)),
                             db(band_rms(xl, fs, T0, T0 + 0.12) / band_rms(sparks[m_]["x"], fs, T0, T0 + 0.12))))
                if (n_, m_) == (2, 3):
                    wav("zenith-tick-and-heal.wav", xl)
        print(f"  ON ONE FRAME with the heal (counts 1-4 x blessing 1/3/5): the chime keeps "
              f"{min(k[2] for k in keep):+.1f}..{max(k[2] for k in keep):+.1f} dB of itself in its band, the heal "
              f"{min(k[3] for k in keep):+.1f}..{max(k[3] for k in keep):+.1f} dB")
        rec["tick_heal_keep"] = keep

        # ---- THE CLOSE -----------------------------------------------------
        rise = max(0.05, round(rel, 2))
        specs["close"][0] = dict(specs["close"][0], rise=rise)
        cast_top = C_["top"]
        lev_z = dict(hi=0.5 * cast_top, inb_floor=2 * b1)
        tgt_z = cast_top * 10 ** (-CLOSE_UNDER_DB / 20)
        print(f"\nCLOSE -- 'the swell reversed, quiet', on {C_['name']}'s figure. MIRROR's climb = the pick's own "
              f"release, {rise} s. Level-matched {CLOSE_UNDER_DB:g} dB under the cast's top ({tgt_z:.4f})")

        def calib_close(j):
            gc = 0.3
            for _ in range(4):
                M = basic(R([["close", T0, j, ci, C_["g"], C_["sw"], gc]])[0])
                gc = gc * tgt_z / M["top"]
            return float(f"{gc:.3g}")

        # the literal reference and the AGAIN control, at DROP's gain
        gc_ref = calib_close(1)
        xlit, _ = R([["lit", T0, ci, C_["g"], C_["sw"], gc_ref]])
        LIT = basic(xlit)
        wav("zenith-close-0-literal.wav", xlit)

        def close_measure(x, calls):
            M = basic(x); M["x"] = x; M["calls"] = calls
            ta = M["top_at"]
            M["c_top"] = cents(top_note(x, T0 + max(0.0, ta - 0.04), T0 + ta + 0.04), F1)
            g1 = M["gone"] / 1000
            M["c_end"] = cents(pitch(x, T0 + g1 - 0.25, T0 + g1 - 0.10, lo=300, hi=1500), F0)
            y = x[int(T0 * SR):]
            r50, c50 = env(y, 0.05)
            e = 20 * np.log10(np.maximum(r50, 1e-6))
            it = int(np.argmax(r50)); seg = e[it:]
            k_ = seg > e[it] - 34
            seg = seg[:int(np.argmin(k_)) if not k_.all() else len(seg)]
            M["rerise"] = float((seg - np.minimum.accumulate(seg)).max()) if len(seg) else 0.0
            M["corr"] = env_corr(x, xlit)
            M["inb"] = band_rms(x, F1, T0 + max(0.0, ta - 0.075), T0 + ta + 0.075)
            return M

        rows_z = []
        print(f"  {'cand':<10}{'gc':>7}{'calls':>6}{'top':>8}{'dB/cast':>8}{'at ms':>6}{'c top':>6}{'c end':>6}"
              f"{'late':>6}{'rerise':>7}{'corr':>6}{'gone':>6}{'inb':>8}")
        for j, (name, cp, blurb) in enumerate(CLOSE_CANDIDATES):
            gc = calib_close(j)
            x, calls = R([["close", T0, j, ci, C_["g"], C_["sw"], gc]])
            x2, _ = R([["close", T0, j, ci, C_["g"], C_["sw"], gc]])
            if float(np.abs(x - x2).max()) > 1e-6:
                raise SystemExit(f"close {name} does not reproduce")
            M = close_measure(x, calls[0]); M.update(name=name, cp=specs["close"][j], gc=gc)
            M["why"] = close_why(M, lev_z)
            rows_z.append(M)
            wav(f"zenith-close-{name.replace(' ', '-').lower()}.wav", x)
        xa, ca = R([["cast", T0, ci, C_["g"] * gc_ref, C_["sw"]]])
        AG = close_measure(xa, ca[0]); AG.update(name="0 AGAIN", gc=gc_ref); AG["why"] = close_why(AG, lev_z)
        LM = close_measure(xlit, 0); LM.update(name="0 LITERAL", gc=gc_ref); LM["why"] = close_why(LM, lev_z)
        for M in rows_z + [AG, LM]:
            print(f"  {M['name']:<10}{M['gc']:>7.3g}{M['calls']:>6d}{M['top']:>8.4f}{db(M['top'] / cast_top):>8.1f}"
                  f"{M['top_at'] * 1000:>6.0f}{M['c_top']:>6.0f}{M['c_end']:>6.0f}{M['late']:>6.2f}{M['rerise']:>7.1f}"
                  f"{M['corr']:>6.2f}{M['gone']:>6.0f}{M['inb']:>8.4f}")
        for (name, _cp, blurb) in CLOSE_CANDIDATES:
            print(f"    {name:<9} {blurb}")
        for name, blurb in CLOSE_CONTROLS:
            print(f"    {name:<9} {blurb}")
        print(f"  gates: top <= {lev_z['hi']:.4f}, in-band at the fifth >= {lev_z['inb_floor']:.4f}")
        print(f"  RULE  {CLOSE_RULE}")
        for M in rows_z:
            if M["why"]:
                print(f"    {M['name']:<9} out: {'; '.join(M['why'])}")
        if AG["why"]:
            print(f"  AGAIN (the control) comes back wrong, as it must: {'; '.join(AG['why'][:3])}")
        else:
            print("  AGAIN PASSED -- 'reversed' cannot fail, so it proves nothing")
            FAILED.append("again control")
        print(f"  LITERAL (the reference) {'passes' if not LM['why'] else 'fails: ' + '; '.join(LM['why'])} "
              f"-- what a shippable reversal is measured against")
        wav("zenith-close-0-again.wav", xa)
        ok, fb = _gate(rows_z, "close")
        zi = fb if ok is None else min(ok, key=lambda i: (-round(rows_z[i]["corr"], 2), rows_z[i]["calls"]))
        Z_ = rows_z[zi]
        print(f"  PICK  {Z_['name']}  gc {Z_['gc']} ({db(Z_['top'] / cast_top):+.1f} dB re the cast's top, "
              f"{db(Z_['top'] / h_lo):+.1f} re the hit @ 24), corr {Z_['corr']:.2f}, gone {Z_['gone']:.0f} ms")

        # ---- THE SFX ROW, GENERATED AND CHECKED ------------------------------
        tick_pitches = "-".join(f"{p:.0f}" for p in K_["pitches"])
        raw_M = ctlc[0]
        info = dict(cen=C_["cen"], dawn_cen=ctl["dawn cast"]["cen"], swell=C_["swell"], top_at=C_["top_at"] * 1000,
                    top_db=db(C_["top"] / h_lo), gone=C_["gone"], rc_reg=C_["rc_reg"], dawn_reg=C_["dawn_reg"],
                    tick_pitches=tick_pitches,
                    tick_peak=K_["peak"], tick_hit_db=db(K_["st_hi"] / h_lo), tick_wall_db=db(K_["st_lo"] / w_hi),
                    tick_spark_reg=K_["spark_reg"], close_db=db(Z_["top"] / cast_top),
                    close_gone=Z_["gone"], close_corr=Z_["corr"], bar_reg=C_["bar_reg"],
                    lean_flut=rows_c[3]["flut"], raw_dips=raw_M["dips"], raw_db=db(C_["top"] / raw_M["top"]),
                    tick_aud_lo=K_["aud_lo"], tick_aud_hi=K_["aud_hi"],
                    keep=-min(min(k[2], k[3]) for k in keep))
        C_["sp"] = specs["cast"][ci]
        Z_["cp"] = specs["close"][zi]
        arm = arm_text(C_, K_, Z_, info)
        bad_src = re.findall(r"Math\.random|\brng\b|spawnFx", arm + CLOSE_CODE + TICK_CODE)
        if bad_src:
            raise SystemExit(f"REFUSING: the rows name {bad_src}")
        row = [SFX_ANCHOR, arm]
        print("\nTHE SFX ROW, applied to Sfx.prototype.play's own source and rendered:")
        chk = []
        xa1, _ = R([["arm", T0, "ult", {"w": "morningstar"}]], row=row)
        chk.append(("cast", float(np.abs(xa1 - C_["x"]).max())))
        for n_ in range(5):
            xt, _ = R([["arm", T0, "ult", {"w": "morningstar-tick", "n": n_}]], row=row)
            chk.append((f"tick n{n_}", float(np.abs(xt - K_["per"][n_]["x"]).max())))
        xz, _ = R([["arm", T0, "ult", {"w": "morningstar-close"}]], row=row)
        chk.append(("close", float(np.abs(xz - Z_["x"]).max())))
        print("  the arms vs the picked candidates, max |diff|: " + ", ".join(f"{k} {v:.1e}" for k, v in chk))
        same_ = []
        for kind, p in (("hit", {"dmg": 24.03, "crit": False}), ("spark", {"collect": True, "n": 3}),
                        ("spark", {"arm": True}), ("spark", {"collect": False}), ("ult", {"w": "axiom"}),
                        ("ult", {"w": "dawnbringer"}), ("ult", {"w": "spellbreaker"}), ("ult", {"w": "lastlight"}),
                        ("wall", {})):
            x1, _ = R([["play", T0, kind, p]]); x2, _ = R([["arm", T0, kind, p]], row=row)
            same_.append((kind + ("/" + str(p.get("w", p.get("n", ""))) if p else ""), float(np.abs(x1 - x2).max())))
        print("  every other voice through the patched play vs the original, max |diff|: " +
              ", ".join(f"{k} {v:.0e}" for k, v in same_))
        now_rc = float(np.abs(xa1 - rcx).max())
        print(f"  ult/morningstar vs rune-crack after the row: max |diff| {now_rc:.3f} -- "
              f"{'no longer the fallback' if now_rc > 1e-3 else 'STILL THE FALLBACK'}")
        if max(v for _, v in chk) > 1e-6 or max(v for _, v in same_) > 1e-6 or now_rc <= 1e-3:
            FAILED.append("sfx row")
        cost = page.evaluate(COST_JS, [row, 40])
        print(f"  main-thread cost a call (median of 40, performance.now() at its headless resolution): "
              f"cast {cost['cast']:.2f} ms, tick {cost['tick']:.2f} ms, close {cost['close']:.2f} ms")
        rec["arm_check"] = dict(chk=chk, others=same_, now_rc=now_rc, cost=cost)

        # ---- THE tickSun ROWS ----------------------------------------------
        rows_ts = [[CLOSE_ANCHOR, CLOSE_CODE], [TICK_ANCHOR, TICK_CODE]]
        seeds = [a.seed0 + k for k in range(a.seeds)]
        print("\nTHE tickSun ROWS, applied to Match.prototype.tickSun's own source, run beside the "
              "original on real fights:")
        WR = page.evaluate(WIRE_JS, [seeds, rows_ts])
        assert not errors, errors[:3]
        if "err" in WR:
            raise SystemExit(WR["err"])
        print(f"  {WR['fights']} fights (Morningstar both sides x every foe x seeds {seeds}): {WR['same']}/"
              f"{WR['fights']} identical (over, clock, both hp, the whole sunTally)")
        pw = np.array(WR["perWin"]); gps = np.array(WR["gaps"]) if WR["gaps"] else np.array([0.0])
        print(f"  windows {WR['ends']}: {WR['casts']} casts, {WR['ticks']} ticks ({pw.mean():.2f} a window, max "
              f"{pw.max()}), {WR['tickVoices']} tick voices, {WR['heals']} heals, {WR['closes']} closes;  "
              f"problems {WR['nbad']}")
        print(f"  tick counts n (smite after the tick): " + " ".join(f"{k}:{v}" for k, v in enumerate(WR['tn']) if v) +
              f";  heal n (blessing): " + " ".join(f"{k}:{v}" for k, v in enumerate(WR['hn']) if v))
        print(f"  ticks inside the cast's first 0.75 s (over its swell): {WR['nearCast'][0]} of {WR['ticks']}; "
              f"tick spacing in match time min {gps.min():.3f} s, p50 {np.median(gps):.3f} s")
        for b_ in WR["bad"]:
            print(f"    {b_}")
        if WR["same"] != WR["fights"] or WR["nbad"] or WR["closes"] != WR["ends"]["clock"] \
                or WR["tickVoices"] != WR["ticks"] or WR["heals"] != WR["ticks"]:
            FAILED.append("tickSun rows")
        badc = [[CLOSE_ANCHOR, CLOSE_CODE.replace("      if (f.alive && Z.t >= Z.dur)",
                                                  "      Z.cd -= 0.001;\n      if (f.alive && Z.t >= Z.dur)", 1)],
                [TICK_ANCHOR, TICK_CODE]]
        WB = page.evaluate(WIRE_JS, [seeds, badc])
        assert not errors, errors[:3]
        print(f"  the control (the rows plus one sim write, Z.cd -= 0.001): {WB['same']}/{WB['fights']} identical -- "
              f"{'it fails, as it must' if WB['same'] < WB['fights'] else 'IT PASSED: the check is blind'}")
        if WB["same"] == WB["fights"]:
            FAILED.append("identity control")
        rec["wire"] = {k: WR[k] for k in ("fights", "same", "ends", "casts", "ticks", "tickVoices", "heals",
                                          "closes", "tn", "hn", "nearCast", "nbad")}
        rec["wire"]["control_same"] = WB["same"]

        # ---- THE PICKS IN A REAL WINDOW -------------------------------------
        cand = sorted(WR["pick"], key=lambda w: (-w["ticks"], w["foe"], w["seed"]))
        if cand:
            w_ = cand[0]
            EV = page.evaluate(RECORD_JS, [w_["side"], w_["foe"], w_["seed"], rows_ts])
            c0 = w_["cast"]; c1 = w_["close"]
            lo_t, hi_t = c0 - 1.0, c1 + 2.0
            evs = [e for e in EV if lo_t <= e[0] <= hi_t]
            allv = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs]
            without = [["arm", T0 + (e[0] - lo_t), e[1], e[2]] for e in evs if not e[3]]
            secs = T0 + (hi_t - lo_t) + 1.0
            xw, _ = R(allv, secs=secs, row=row)
            xo, _ = R(without, secs=secs, row=row)
            bd = bed[:len(xw)]
            xw = xw + bd; xo = xo + bd
            ticks_ = [(T0 + (e[0] - lo_t), e[2].get("n", 0)) for e in evs if e[1] == "ult" and e[2].get("w") == "morningstar-tick"]
            over = [db(band_rms(xw, K_["pitches"][min(4, n_)], t_, t_ + 0.06) /
                       max(band_rms(xo, K_["pitches"][min(4, n_)], t_, t_ + 0.06), 1e-12)) for t_, n_ in ticks_]
            tc = T0 + (c0 - lo_t)
            cast_over = db(band_rms(xw, F1, tc + 0.35, tc + 0.5) / max(band_rms(xo, F1, tc + 0.35, tc + 0.5), 1e-12))
            tz = T0 + (c1 - lo_t)
            close_over = db(band_rms(xw, F1, tz, tz + 0.15) / max(band_rms(xo, F1, tz, tz + 0.15), 1e-12))
            hits = [T0 + (e[0] - lo_t) for e in evs if e[1] == "hit" and c0 <= e[0] <= c1]
            hk = [float(np.abs(xw[int(h * SR):int((h + 0.03) * SR)]).max() /
                        max(np.abs(xo[int(h * SR):int((h + 0.03) * SR)]).max(), 1e-9)) for h in hits]
            print(f"\nIN A REAL WINDOW -- morningstar v {w_['foe']} (side {w_['side']}), seed {w_['seed']}, cast at "
                  f"{c0:.2f}s, closed by its clock at {c1:.2f}s, {w_['ticks']} ticks; the fight's own {len(without)} "
                  f"sounds and the score, with and without Zenith's")
            print(f"  each tick chime over the fight in its own third-octave: " + " ".join(f"{v:+.1f}" for v in over) +
                  f" dB (median {float(np.median(over)):+.1f})")
            print(f"  the cast's top over the fight at A5 {cast_over:+.1f} dB; the close {close_over:+.1f} dB")
            if hk:
                print(f"  the {len(hk)} blows inside the window keep {min(hk):.2f}-{max(hk):.2f} of their peak "
                      f"(median {float(np.median(hk)):.2f})")
            if over and float(np.median(over)) < 6:
                FAILED.append("tick not heard in a real window")
            wav("zenith-pick-real-window.wav", xw)
            wav("zenith-pick-real-window-without.wav", xo)
            rec["real"] = dict(win=w_, tick_over=over, cast_over=cast_over, close_over=close_over, blow_keep=hk)
        # the three picks back to back, for the ear
        xs, _ = R([["arm", T0, "ult", {"w": "morningstar"}]] +
                  [["arm", T0 + 0.9 + 0.4 * k, "ult", {"w": "morningstar-tick", "n": min(4, k + 1)}] for k in range(5)] +
                  [["arm", T0 + 0.9 + 0.4 * k, "spark", {"collect": True, "n": min(5, k + 1)}] for k in range(5)] +
                  [["arm", T0 + 3.2, "ult", {"w": "morningstar-close"}]], secs=6.0, row=row)
        wav("zenith-pick-sequence.wav", xs)

    def strip(L):
        return [{k: v for k, v in M.items() if k not in ("x", "bands", "per", "draws")} for M in L]

    rec.update(cast=strip(rows_c), cast_controls=strip(ctlc), tick=[{k: v for k, v in T.items() if k != "per"}
                                                                    for T in rows_t],
               close=strip(rows_z), wavs=sizes,
               pick={"cast": C_["name"], "tick": K_["name"], "close": Z_["name"], "cast_g": C_["g"],
                     "cast_sw": C_["sw"], "tick_g": K_["g"], "tick_D": K_["D"], "close_gc": Z_["gc"],
                     "close_rise": Z_["cp"]["rise"]})
    print(f"\nTHE PICKS  cast {C_['name']}   tick {K_['name']}   close {Z_['name']}   (heal: the spark collect, unchanged)")
    print(f"WAVS   {out}  ({len(sizes)} files, {sum(sizes.values()) // 1024} KB, raw level)")
    rows = [dict(label="Sfx: Zenith's cast, tick and close arms, before the shared rune-crack fallback",
                 anchor=SFX_ANCHOR, mode="replace", code=arm),
            dict(label="tickSun: the close, when the window runs out by its clock with the caster alive",
                 anchor=CLOSE_ANCHOR, mode="replace", code=CLOSE_CODE),
            dict(label="tickSun: the tick chime and the heal (spark collect), once per tick",
                 anchor=TICK_ANCHOR, mode="replace", code=TICK_CODE)]
    if a.rows:
        pathlib.Path(a.rows).write_text(json.dumps(rows, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rec, indent=1, default=float))
    print("\n  NOTHING IS IN THE BUILD. The three rows are the edits; all three were applied "
          "to the page's own code above.")
    if FAILED:
        print(f"\nEXIT 1 -- failed: {', '.join(FAILED)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
